#!/usr/bin/env python3
"""Paper C stage 1 (EXPLORATORY / DEV): a zero-shot VLM captions an image with k Vietnamese captions of memory
images as text-only in-context examples. Design: manuscript/prereg/2026-10-22_c_stage1/DESIGN.md (sha256 pinned).

Loading, fixed batch slices, resume and the greedy call are the committed LB decoder's (scripts/lb/decode_hf_vlm.py,
pinned), imported unchanged: its make_generate takes one prompt text per image. Models, revisions, snapshot pins,
venv, batch sizes and the 60 new tokens of the short prompt come from the B-N1 registration. New here: the prompt
templates, the example block, the run grid and the refusal of test and dev-B images.

  python scripts/c_stage1/decode_icl.py --selftest                       CPU, no data
  python scripts/c_stage1/decode_icl.py --list-runs [--dataset D]
  python scripts/c_stage1/decode_icl.py --run-ids R [R ...] --snapshot DIR --lists L --exemplars E --out-dir DIR
Writes <run>.preds.json (LB schema plus the example ids and prompt sha256 per image; never a prompt text) and a
.sha256 sidecar. Memory captions are read at run time from $NCS_DATA and never written.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts"), str(ROOT / "scripts/lb")]
import decode_hf_vlm as lb  # noqa: E402  committed LB decoder (pinned by B-N1), reused unchanged

LABEL = "EXPLORATORY / DEV"
SCHEMA = "vsps.c_stage1.v1"
DESIGN = "manuscript/prereg/2026-10-22_c_stage1/DESIGN.md"
B_N1 = "manuscript/prereg/2026-10-19_b_n1_vi_leaderboard.json"
EXCL = "manuscript/prereg/2026-10-21_dev_pools/exclusion.json"
DEV299 = "manuscript/prereg/2026-10-21_dev_pools/ktvic_dev299.tsv"
PINS = {
    DESIGN: "eacc9a9c737cec278c77ce5acd3b07422c9b0f7e661624ec42ba0454050ed53f",
    B_N1: "9ff02dc259258de1add426abd02131f2122e3476a81f9a076066ed6d74906134",
    "scripts/lb/decode_hf_vlm.py": "e2de18811e2ffeb61ed72cb2399d41123e9a8f6ccd73a5ec35f778dcbe2f5ac4",
    EXCL: "c52a96d18925b974878ae1a970c3f9133fb3482216676fd41871eeabb68cc77f",
    DEV299: "a4ac7fdbd904f2205845705f5235b9748225a83a07854b58e59a755b85e4186e",
}
LISTS_SHA256 = "5c479f03e8be544f4cd12b5d997b5dc92b6c622df061760cd02f6ba82f6b4371"  # lists addendum (DESIGN §2.6, LISTS_ADDENDUM.md)
MODELS = ("qwen25vl_7b", "internvl3_8b")
DATASETS = {"ktvic_dev299": {"src": "ktvic", "image_dir": "ktvic/images"},
            "ov_dev_a": {"src": "openviic", "image_dir": "openviic/images"}}
KS = (2, 4, 8)
HEADER = ("Dưới đây là chú thích của một vài bức ảnh khác. Các chú thích này chỉ cho thấy cách viết, "
          "chúng không mô tả bức ảnh cần chú thích.")
LINE = "Ví dụ {i}: {caption}"
TAILS = {
    "T1": ("Hãy viết chú thích cho bức ảnh này bằng MỘT câu tiếng Việt ngắn gọn, theo cách viết của các ví dụ. "
           "Chỉ nêu những gì thực sự nhìn thấy trong ảnh. Không liệt kê, không giải thích."),
    "T2": ("Hãy viết chú thích cho bức ảnh này bằng MỘT câu tiếng Việt ngắn gọn, theo cách viết của các ví dụ. "
           "Không liệt kê, không giải thích."),
}
TEMPLATE_SHA256 = "7478361a133cf3944ce4e9952fd32cd97660cd747cb2f45bfdda30cd8a4a3a00"
ZS_PROMPT_SHA256 = "8870589c4a32307cbbeb68e363490007682237c0b5a3a1ee7e21cb91fce93886"  # evaluate.PROMPTS["short"]


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def template_sha() -> str:
    return sha(json.dumps({"header": HEADER, "line": LINE, "tails": TAILS}, ensure_ascii=False, sort_keys=True))


def pinned(rel: str) -> Path:
    p = ROOT / rel
    if lb.sha256_file(p) != PINS[rel]:
        raise SystemExit(f"{rel}: sha256 differs from the pin in {Path(__file__).name}")
    return p


def registration() -> dict:
    pinned(DESIGN)
    pinned("scripts/lb/decode_hf_vlm.py")
    if template_sha() != TEMPLATE_SHA256:
        raise SystemExit("the prompt templates differ from the design's sha256")
    return lb.load_prereg(pinned(B_N1))


# ------------------------------------------------------------------------------------------------ run grid
def grid() -> dict[str, dict]:
    """Every stage-1 run, by id. Per (dataset, model): zero-shot; retrieval k x order with T1, and k=4 last with T2;
    random and fixed examples at each k with T1. DESIGN §4 says which of them each phase decodes."""
    arms = [{"arm": "zs", "k": 0, "order": None, "tpl": None}]
    arms += [{"arm": "ret", "k": k, "order": o, "tpl": "T1"} for k in KS for o in ("first", "last")]
    arms += [{"arm": "ret", "k": 4, "order": "last", "tpl": "T2"}]
    arms += [{"arm": a, "k": k, "order": None, "tpl": t} for a in ("rand", "fix") for k in KS for t in ("T1", "T2")]
    out = {}
    for ds in DATASETS:
        for m in MODELS:
            for a in arms:
                tag = "zs" if a["arm"] == "zs" else "-".join(
                    x for x in (a["arm"], f"k{a['k']}", a["order"], a["tpl"]) if x)
                rid = f"c1_{m}_{ds}-{tag}"
                out[rid] = {"run_id": rid, "dataset": ds, "model": m, **a}
    return out


def run_spec(run_id: str) -> dict:
    spec = grid().get(run_id)
    if spec is None:
        raise SystemExit(f"{run_id}: not a stage-1 run")
    return spec


# ------------------------------------------------------------------------------------------------ lists and refusal
def load_lists(path: Path, pin: str | None = LISTS_SHA256) -> dict:
    """lists.json (DESIGN §2): the dev-A manifest, the memory clusters and the refused images; pinned by sha256."""
    if pin is None:
        raise SystemExit("lists.json is not pinned yet: the lists addendum must be committed before any decode")
    if lb.sha256_file(path) != pin:
        raise SystemExit(f"{path}: sha256 differs from the pinned lists.json")
    lists = json.loads(Path(path).read_text(encoding="utf-8"))
    if lists.get("design_sha256") != PINS[DESIGN]:
        raise SystemExit(f"{path}: built under another design")
    return lists


def load_exemplars(path: Path, lists_path: Path) -> dict:
    ex = json.loads(Path(path).read_text(encoding="utf-8"))
    if ex.get("lists_sha256") != lb.sha256_file(lists_path) or ex.get("design_sha256") != PINS[DESIGN]:
        raise SystemExit(f"{path}: not built from this lists.json under this design")
    return ex


def refused(lists: dict) -> tuple[dict[str, set[str]], set[str]]:
    """(ids by namespace, image sha256s) never decoded in stage 1: every test set of A and B (exclusion.json), the
    OpenViIC test set, OV-dev-B and XM3600 (lists.json `refuse`)."""
    ex = json.loads(pinned(EXCL).read_text(encoding="utf-8"))
    ids = {ns: {str(x) for v in sets.values() for x in v} for ns, sets in ex["ids"].items()}
    ids["openviic"] = set(lists["refuse"]["openviic_files"])
    hashes = {h for v in ex["image_sha256"].values() for h in v} | set(lists["refuse"]["image_sha256"])
    return ids, hashes


def refuse_rows(rows: list, ns: str, ids: dict, hashes: set) -> None:
    bad = [i for i, _f, h in rows if i in ids.get(ns, set()) or h in hashes]
    if bad:
        raise SystemExit(f"REFUSED: {len(bad)} test or dev-B image(s) in the input, e.g. {bad[:3]}")


def manifest(ds: str, lists: dict) -> list[tuple[str, str, str]]:
    """[(id, file, image sha256)] of a stage-1 dev set, refused if any row is a test or dev-B image."""
    if ds == "ktvic_dev299":
        rows = [tuple(x.split("\t")) for x in pinned(DEV299).read_text(encoding="utf-8").splitlines()]
    else:
        rows = [tuple(r) for r in lists["sets"][ds]]
    if len({r[0] for r in rows}) != len(rows) or any(len(r) != 3 for r in rows):
        raise SystemExit(f"{ds}: not distinct (id, file, sha256) rows")
    refuse_rows(rows, DATASETS[ds]["src"], *refused(lists))
    return rows


# ------------------------------------------------------------------------------------------------ prompts
def memory_captions(lists: dict, data: Path | None = None) -> dict[str, dict[str, str]]:
    """{cluster id: {source: caption}}: the first released caption of each member, read from $NCS_DATA."""
    data = data or lb.DATA
    kt = json.loads((data / "datasets/ktvic/train_data.json").read_text(encoding="utf-8"))
    first: dict[str, str] = {}
    for a in kt["annotations"]:
        first.setdefault(str(a["image_id"]), a["caption"])
    ov = json.loads((data / "datasets/openviic/uit-openviic-annotation-train.json").read_text(encoding="utf-8"))
    out = {}
    for m in lists["memory"]:
        caps: dict[str, str] = {}
        for src, i, _f, _h in m["members"]:
            caps.setdefault(src, " ".join((first[i] if src == "ktvic" else ov[i]["captions"][0]).split()))
        out[m["cid"]] = caps
    return out


def shown(caps: dict[str, str], src: str) -> str:
    """The caption shown for a cluster: its copy from the query's own dataset if it has one, else its first member's."""
    return caps.get(src) or next(iter(caps.values()))


def exemplar_ids(spec: dict, qid: str, ex: dict) -> list[str]:
    """Cluster ids shown to one image, in prompt order. Retrieval: by cosine, most similar first or last."""
    k, ds = spec["k"], spec["dataset"]
    if spec["arm"] == "ret":
        ids = [c for c, _cos in ex["ret"][ds][qid][:k]]
        return ids[::-1] if spec["order"] == "last" else ids
    if spec["arm"] == "rand":
        return ex["rand"][ds][qid][:k]
    if spec["arm"] == "fix":
        return ex["fix"][ds][:k]
    return []


def prompt(tpl: str, captions: list[str]) -> str:
    lines = [LINE.format(i=n, caption=c) for n, c in enumerate(captions, 1)]
    return "\n".join([HEADER, *lines, TAILS[tpl]])


def check_exemplars(rows: list, spec: dict, ex: dict, lists: dict) -> dict[str, list[str]]:
    """{image id: cluster ids}; refused if an example is a refused image or a copy of the image it is shown with."""
    members = {m["cid"]: {h for *_x, h in m["members"]} for m in lists["memory"]}
    _ids, hashes = refused(lists)
    out = {}
    for i, _f, h in rows:
        cids = exemplar_ids(spec, i, ex)
        if len(cids) != spec["k"] or len(set(cids)) != len(cids):
            raise SystemExit(f"{spec['run_id']} {i}: not {spec['k']} distinct examples")
        shas = set().union(*(members[c] for c in cids)) if cids else set()
        if h in shas or shas & hashes:
            raise SystemExit(f"REFUSED: {spec['run_id']} {i}: an example is the image itself or a refused image")
        out[i] = cids
    return out


# ------------------------------------------------------------------------------------------------ GPU
def decode_runs(run_ids: list[str], snapshot: Path, lists_path: Path, ex_path: Path, out_dir: Path) -> None:
    specs = [run_spec(r) for r in run_ids]
    if len({s["model"] for s in specs}) != 1:
        raise SystemExit("one model per process")
    lists = load_lists(lists_path)
    ex = load_exemplars(ex_path, lists_path)
    reg = registration()
    m = reg["models"][specs[0]["model"]]
    if lb.packages() != reg["venv"]["packages"]:
        raise SystemExit(f"package versions {lb.packages()} differ from the B-N1 venv")
    lb.check_snapshot(m, snapshot)
    outs = [out_dir / f"{s['run_id']}.preds.json" for s in specs]
    if any(o.exists() for o in outs):
        raise SystemExit("an output exists; a run is decoded once")
    plan = []
    for s in specs:  # every refusal before the model loads
        items = manifest(s["dataset"], lists)
        plan.append((s, items, check_exemplars(items, s, ex, lists)))
    ctx = {"caps": memory_captions(lists), "zs": lb.prompt_text(reg, "short"), "m": m, "ex_path": ex_path,
           "n_new": reg["decode"]["max_new_tokens"]["short"]}
    ctx["proc"], ctx["net"] = lb.load(m, snapshot, "cuda:0")
    for (s, items, exids), out in zip(plan, outs):
        decode_one(s, items, exids, out, ctx)


def decode_one(s: dict, items: list, exids: dict, out: Path, ctx: dict) -> None:
    """One run with the loaded model; ctx holds the memory captions, zero-shot prompt, model block and model."""
    import torch

    proc, net, m, caps, zs, n_new = (ctx[k] for k in ("proc", "net", "m", "caps", "zs", "n_new"))
    started = lb.utc()
    src = DATASETS[s["dataset"]]["src"]
    texts = {i: zs if s["arm"] == "zs" else prompt(s["tpl"], [shown(caps[c], src) for c in exids[i]])
             for i, _f, _h in items}
    base = lb.make_generate(proc, net, zs, n_new, lb.DATA / "datasets" / DATASETS[s["dataset"]]["image_dir"])

    def gen(sl):
        return base(sl, [texts[i] for i, _f, _h in sl])

    kw = {"max_new_tokens": n_new, "do_sample": False, "num_beams": 1}
    tsha = {i: sha(t) for i, t in texts.items()}
    part = Path(str(out) + ".partial.jsonl")
    resumed = part.exists()
    key = lb.run_key(PINS[B_N1], s, m, kw, json.dumps(tsha, sort_keys=True), items)
    rows = lb.decode_slices(items, m["batch_size"], gen, part, key)
    solo = [gen([it])[0][0] for it in items[:m["batch_size"]]] if m["batch_size"] > 1 else []
    status = lb.git("status", "--porcelain", "--untracked-files=no")
    prov = {"schema": lb.SCHEMA, "c_schema": SCHEMA, "label": LABEL, "design": DESIGN, "design_sha256": PINS[DESIGN],
            "prereg_id": "B-N1 model blocks (no registration for stage 1)", "prereg_sha256": PINS[B_N1],
            "decoder_sha256": PINS["scripts/lb/decode_hf_vlm.py"], "wrapper_sha256": lb.sha256_file(Path(__file__)),
            "run_id": s["run_id"], "spec": s, "model": s["model"], "hub_id": m["hub_id"], "revision": m["revision"],
            "dataset": s["dataset"], "prompt_mode": "short" if s["arm"] == "zs" else f"icl-{s['tpl']}",
            "prompt_text_sha256": ZS_PROMPT_SHA256 if s["arm"] == "zs" else TEMPLATE_SHA256,
            "prompt_sha256_per_image": tsha, "exemplars": exids, "manifest_sha256": sha(json.dumps(items)),
            "lists_sha256": LISTS_SHA256, "exemplars_sha256": lb.sha256_file(ctx["ex_path"]),
            "max_new_tokens": n_new,
            "batch_size": m["batch_size"], "dtype": m["dtype"], "attn_implementation": m["attn_implementation"],
            "processor_kwargs": m["processor_kwargs"], "generation_config": net.generation_config.to_diff_dict(),
            "machine_id": os.environ.get("VSPS_MACHINE_ID"), "git_head": lb.git("rev-parse", "HEAD"),
            "git_dirty": None if status is None else bool(status), "job_sha256": os.environ.get("VSPS_JOB_SHA256"),
            "venv_freeze_sha256": os.environ.get("VSPS_VENV_FREEZE_SHA256"), "packages": lb.packages(),
            "n_images": len(items), "resumed": resumed, "started_utc": started, "finished_utc": lb.utc(),
            "parity_slice0": {"n": len(solo), "identical": sum(a == r["caption"] for a, r in zip(solo, rows))},
            "gpu": torch.cuda.get_device_name(0), "cuda": torch.version.cuda, "generate_kwargs": kw}
    lb.write_output(out, prov, rows)
    print(f"wrote {out}")


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def refuses(fn) -> bool:
    try:
        fn()
    except SystemExit as stop:
        return bool(str(stop))
    return False


def fake_lists(tmp: Path) -> tuple[Path, Path, dict]:
    """A synthetic lists.json / exemplars.json pair (ids made up for the test, no dataset content)."""
    h = lambda s: sha(s)  # noqa: E731
    lists = {"design_sha256": PINS[DESIGN], "refuse": {"openviic_files": ["t1.jpg", "b1.jpg"],
                                                       "image_sha256": [h("t1"), h("b1")]},
             "sets": {"ov_dev_a": [["a1.jpg", "a1.jpg", h("a1")], ["a2.jpg", "a2.jpg", h("a2")]]},
             "memory": [{"cid": f"m{n}", "members": [["openviic", f"x{n}.jpg", f"x{n}.jpg", h(f"x{n}")]]}
                        for n in range(9)]}
    lp = tmp / "lists.json"
    lp.write_text(json.dumps(lists), encoding="utf-8")
    ret = {q: [[f"m{n}", 0.9 - n / 10] for n in range(8)] for q in ("a1.jpg", "a2.jpg")}
    ex = {"design_sha256": PINS[DESIGN], "lists_sha256": lb.sha256_file(lp), "ret": {"ov_dev_a": ret},
          "rand": {"ov_dev_a": {q: [f"m{n}" for n in (8, 1, 3, 5, 7, 0, 2, 4)] for q in ret}},
          "fix": {"ov_dev_a": [f"m{n}" for n in (6, 2, 4, 0, 1, 3, 5, 7)]}}
    ep = tmp / "exemplars.json"
    ep.write_text(json.dumps(ex), encoding="utf-8")
    return lp, ep, lists


def selftest() -> None:
    reg = registration()
    g = grid()
    per = len(g) // (len(DATASETS) * len(MODELS))
    assert per == 1 + 6 + 1 + 12 and len(g) == len(set(g)), "grid size"
    assert all(m in reg["models"] for m in MODELS)
    zs = lb.prompt_text(reg, "short")
    assert sha(zs) == ZS_PROMPT_SHA256 and reg["decode"]["max_new_tokens"]["short"] == 60
    p = prompt("T1", ["câu mẫu một", "câu mẫu hai"])
    assert p.splitlines() == [HEADER, "Ví dụ 1: câu mẫu một", "Ví dụ 2: câu mẫu hai", TAILS["T1"]]
    with tempfile.TemporaryDirectory() as tmp:
        lp, ep, lists = fake_lists(Path(tmp))
        if LISTS_SHA256 is None:
            assert refuses(lambda: load_lists(lp)), "unpinned lists must be refused"
        assert refuses(lambda: load_lists(lp, "0" * 64)), "a changed lists.json must be refused"
        lists = load_lists(lp, lb.sha256_file(lp))
        ex = load_exemplars(ep, lp)
        ids, hashes = refused(lists)
        for rows, ns in (([("1", "00000000001.jpg", "0" * 64)], "ktvic"),       # KTVIC test id 1
                         ([("x", "x.jpg", next(iter(hashes)))], "ktvic"),        # a refused image sha256
                         ([("t1.jpg", "t1.jpg", "1" * 64)], "openviic")):        # an OpenViIC test file
            assert refuses(lambda: refuse_rows(rows, ns, ids, hashes)), "a test or dev-B image must be refused"
        rows = manifest("ov_dev_a", lists)
        assert len(manifest("ktvic_dev299", lists)) == 299
        last = run_spec("c1_qwen25vl_7b_ov_dev_a-ret-k4-last-T1")
        first = run_spec("c1_qwen25vl_7b_ov_dev_a-ret-k4-first-T1")
        assert exemplar_ids(last, "a1.jpg", ex) == exemplar_ids(first, "a1.jpg", ex)[::-1] == ["m3", "m2", "m1", "m0"]
        k2 = run_spec("c1_qwen25vl_7b_ov_dev_a-rand-k2-T1")
        assert exemplar_ids(k2, "a1.jpg", ex) == exemplar_ids(run_spec(k2["run_id"].replace("k2", "k8")),
                                                              "a1.jpg", ex)[:2], "examples nest across k"
        assert check_exemplars(rows, last, ex, lists)["a2.jpg"] == ["m3", "m2", "m1", "m0"]
        own = {**lists, "memory": lists["memory"] + [{"cid": "m9", "members": [["openviic", "a1.jpg", "a1.jpg",
                                                                                rows[0][2]]]}]}
        ex_self = {**ex, "ret": {"ov_dev_a": {**ex["ret"]["ov_dev_a"], "a1.jpg": [["m9", 1.0]] + ex["ret"][
            "ov_dev_a"]["a1.jpg"][:7]}}}
        assert refuses(lambda: check_exemplars(rows, last, ex_self, own)), "an image must never see itself"
        key = lambda t: lb.run_key("r", last, {}, {}, t, rows)  # noqa: E731
        assert key("a") != key("b"), "the resume key must depend on the prompts"
        assert refuses(lambda: decode_runs([last["run_id"]], Path(tmp), lp, ep, Path(tmp))), "unpinned: no decode"
    print(f"selftest ok: {len(g)} runs, prompts, refusal, examples, resume key")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--list-runs", action="store_true")
    ap.add_argument("--dataset", choices=sorted(DATASETS))
    ap.add_argument("--run-ids", nargs="+")
    ap.add_argument("--snapshot", type=Path)
    ap.add_argument("--lists", type=Path)
    ap.add_argument("--exemplars", type=Path)
    ap.add_argument("--out-dir", type=Path)
    a = ap.parse_args()
    if a.selftest:
        selftest()
    elif a.list_runs:
        print("\n".join(r for r, s in grid().items() if a.dataset in (None, s["dataset"])))
    elif a.run_ids and a.snapshot and a.lists and a.exemplars and a.out_dir:
        decode_runs(a.run_ids, a.snapshot, a.lists, a.exemplars, a.out_dir)
    else:
        ap.error("choose --selftest, --list-runs, or --run-ids --snapshot --lists --exemplars --out-dir")


if __name__ == "__main__":
    main()
