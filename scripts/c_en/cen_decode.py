#!/usr/bin/env python3
"""C-EN decodes and InternVL3's guard: the 12-run grid, the English prompts (direct translations of C's), the
English guard port, the verifier pass and the CC-113 r5 smoke check. Prereg 2026-10-27_c_en/PREREG.md §2, §5, §9.

  python3 scripts/c_en/cen_decode.py --selftest                                       CPU, synthetic only
  python3 scripts/c_en/cen_decode.py runs --set S [--model M] [--arm A ...]
  python  scripts/c_en/cen_decode.py decode --run-ids R ... --snapshot DIR --memory M --captions C --exemplars X \
      --images DIR --out-dir D --expect-head H                                       GPU, venv-lb, M3
  python  scripts/c_en/cen_decode.py items --set S --runs R ... --zs Z --memory M --captions C --out I   CPU
  python  scripts/c_en/cen_decode.py verify --set S --items I --images DIR --snapshot DIR --out CACHE \
      --expect-head H                                                                GPU, venv-lb, M3
The CC-113 r5 smoke check is the same decode / items / verify path with --set smoke: the first 16 memory
clusters' members[0] images queried against the memory (cen_memory.py exemplars --set smoke); no score.
Decoding is the committed LB decoder (make_generate, decode_slices, write_output), greedy, 60 new tokens, the B-N1
model blocks. Outputs hold captions and are never committed. Nothing here prints a caption.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / "scripts/c_stage2"), str(HERE.parents[1] / "scripts")]
import cen_fetch as F  # noqa: E402
import cen_memory as M  # noqa: E402  (registers the test sets in decode_icl.DATASETS)
import stage2 as S2  # noqa: E402  frozen config, run spec; checks the stage-1 shas on import
import score_coco_probe as SC  # noqa: E402  the committed English COCO-80 matcher (en_classes, synonyms)

C, G, lb, BM = S2.C, S2.G, S2.lb, M.BM
SCHEMA, LABEL = "vsps.c_en.v1", "TEST, ONE LOOK PER SET"
ARMS = ("ret", "rand", "zs")  # CC-107 r5
SETS = M.TEST_SETS + ("smoke",)
OUT_ROOT = Path("/root/outputs/c_en")
# Direct translations of decode_icl.HEADER / LINE / TAILS (CC-107 r5); nothing else changes
HEADER = ("Below are captions of a few other images. These captions only show the writing style; "
          "they do not describe the image to be captioned.")
LINE = "Example {i}: {caption}"
TAILS = {
    "T1": ("Write a caption for this image in ONE short English sentence, in the style of the examples. "
           "Only state what is actually visible in the image. Do not list items or explain."),
    "T2": ("Write a caption for this image in ONE short English sentence, in the style of the examples. "
           "Do not list items or explain."),
}
EN_TEMPLATE_SHA256 = "b329e57a62d67a5afa62ff04503ed30992028839eb65284c3c6cae93a64ed713"  # template_sha(), asserted by the selftest
ZS_EN_SHA256 = "0cdbdf77fae4c04bdf4cd626a9eaf9adec5ef0411aac5d816f6c916a69604893"  # evaluate.PROMPTS["short_en"]
N_NEW = 60
SMOKE_N = M.SMOKE_N
# guard port (PREREG §2): SPLIT and function_end of guard.py / rl_reward.py, translated
SPLIT = re.compile(r"(\s*[,;]\s*|\s+(?:and|together with|beside|next to|near|in front of|behind|before|after|on|"
                   r"under|in)\s+)")
END = re.compile(r"[.!?…]+$")
FUNCTION_END = {"of", "and", "with", "at", "on", "in", "a", "an", "the", "some", "has", "is", "are", "for", "beside"}
SYN = SC.load_synonyms()
CLASSES = sorted(set(SYN.values()))
EN_NP = {c: ("an " if c[0] in "aeiou" else "a ") + c for c in CLASSES}  # S2's {np}, for COCO-80 classes
VERIFIER = "qwen3vl_8b"


def template_sha() -> str:
    return C.sha(json.dumps({"header": HEADER, "line": LINE, "tails": TAILS}, ensure_ascii=False, sort_keys=True))


def prompt(tpl: str, captions: list[str]) -> str:
    return "\n".join([HEADER, *[LINE.format(i=n, caption=c) for n, c in enumerate(captions, 1)], TAILS[tpl]])


def zs_prompt() -> str:
    return lb.prompt_text({"decode": {"prompts": {"short_en": {"text_sha256": ZS_EN_SHA256}}}}, "short_en")


def out_ok(p: Path) -> Path:
    if os.environ.get("VSPS_MACHINE_ID") and not Path(p).resolve().is_relative_to(OUT_ROOT):
        raise SystemExit(f"REFUSED: {p} is not under {OUT_ROOT}")
    return Path(p)


# ------------------------------------------------------------------------------------------------ grid
def spec(cfg: dict, ds: str, model: str, arm: str) -> dict:
    if ds not in SETS or arm not in ARMS:
        raise SystemExit(f"REFUSED: no C-EN run for {ds} / {arm}")
    s = S2.spec(cfg, ds, model, arm)
    return {**s, "run_id": "cen_" + s["run_id"].removeprefix("c2_")}


def grid(cfg: dict, sets=M.TEST_SETS) -> dict[str, dict]:
    return {s["run_id"]: s for s in (spec(cfg, d, m, a) for d in sets for m in C.MODELS for a in ARMS)}


def guarded_model(cfg: dict, model: str) -> bool:
    """Only a finite frozen tau gets the verifier (PT §4): InternVL3 at 0.10, on ret and rand."""
    return cfg["models"][model]["tau"] not in S2.INFINITE


# ------------------------------------------------------------------------------------------------ examples
def items_of(ds: str, rec_dir: Path = F.REC_DIR) -> list[tuple[str, str, str]]:
    """[(id, file, sha256)] of a test set in pinned order, from its list and complete hash-only record."""
    import cen_pool as P

    return [(str(i), f, h) for i, f, h in P.rows_of(ds, rec_dir)]


def check_exemplars(items: list, s: dict, ex: dict, memory: dict, refused: set[str]) -> dict[str, list[str]]:
    """{id: cluster ids}: k distinct examples; none is the image itself or holds a test-side sha256."""
    members = {m["cid"]: {x[2] for x in m["members"]} for m in memory["memory"]}
    out = {}
    for i, _f, h in items:
        cids = C.exemplar_ids(s, i, ex)
        if len(cids) != s["k"] or len(set(cids)) != len(cids):
            raise SystemExit(f"{s['run_id']} {i}: not {s['k']} distinct examples")
        shas = set().union(*(members[c] for c in cids)) if cids else set()
        if h in shas or shas & refused:
            raise SystemExit(f"REFUSED: {s['run_id']} {i}: an example is the image itself or a test-side image")
        out[i] = cids
    return out


def load_captions(path: Path, memory_path: Path) -> dict[str, str]:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    if d.get("what") != "memory" or d.get("memory_sha256") != F.sha_file(memory_path):
        raise SystemExit(f"{path}: not the caption store of this memory")
    return d["captions"]


def texts_for(s: dict, items: list, exids: dict, caps: dict[str, str], zs: str) -> dict[str, str]:
    return {i: zs if s["arm"] == "zs" else prompt(s["tpl"], [caps[c] for c in exids[i]]) for i, _f, _h in items}


# ------------------------------------------------------------------------------------------------ decode (GPU)
def decode_runs(a) -> None:
    F.host_ok(a.expect_head)
    cfg = S2.frozen()
    g = grid(cfg, SETS)
    if any(r not in g for r in a.run_ids):
        raise SystemExit("not a C-EN run")
    specs = [g[r] for r in a.run_ids]
    if len({(s["model"], s["dataset"]) for s in specs}) != 1:
        raise SystemExit("one model and one set per process")
    ds = specs[0]["dataset"]
    memory = json.loads(a.memory.read_text(encoding="utf-8"))
    ex = json.loads(a.exemplars.read_text(encoding="utf-8"))
    if ex.get("set") != ds or ex.get("memory_sha256") != F.sha_file(a.memory):
        raise SystemExit("the example lists are not this set's on this memory")
    items = smoke_items(memory) if ds == "smoke" else items_of(ds)
    refused = test_side_shas()
    outs = [out_ok(a.out_dir / f"{s['run_id']}.preds.json") for s in specs]
    if any(o.exists() for o in outs):
        raise SystemExit("an output exists; a run is decoded once")
    plan = [(s, check_exemplars(items, s, ex, memory, refused)) for s in specs]  # every refusal before the load
    caps = load_captions(a.captions, a.memory)
    reg = C.registration()
    m = reg["models"][specs[0]["model"]]
    if lb.packages() != reg["venv"]["packages"]:
        raise SystemExit("package versions differ from the B-N1 venv")
    lb.check_snapshot(m, a.snapshot)
    proc, net = lb.load(m, a.snapshot, "cuda:0")
    for (s, exids), out in zip(plan, outs):
        decode_one(s, items, exids, out, caps, proc, net, m, a)


def decode_one(s, items, exids, out, caps, proc, net, m, a) -> None:
    import torch

    started = lb.utc()
    zs = zs_prompt()
    texts = texts_for(s, items, exids, caps, zs)
    base = lb.make_generate(proc, net, zs, N_NEW, a.images)

    def gen(sl):
        return base(sl, [texts[i] for i, _f, _h in sl])

    kw = {"max_new_tokens": N_NEW, "do_sample": False, "num_beams": 1}
    tsha = {i: C.sha(t) for i, t in texts.items()}
    part = Path(str(out) + ".partial.jsonl")
    resumed = part.exists()
    rows = lb.decode_slices(items, m["batch_size"], gen, part,
                            lb.run_key(EN_TEMPLATE_SHA256, s, m, kw, json.dumps(tsha, sort_keys=True), items))
    solo = [gen([it])[0][0] for it in items[:m["batch_size"]]] if m["batch_size"] > 1 else []
    status = lb.git("status", "--porcelain", "--untracked-files=no")
    prov = {"schema": lb.SCHEMA, "c_schema": SCHEMA, "label": LABEL, "prereg_id": "C-EN test prereg",
            "prereg_sha256": F.sha_file(F.ROOT / F.PDIR / "PREREG.md"), "run_id": s["run_id"], "spec": s,
            "model": s["model"], "hub_id": m["hub_id"], "revision": m["revision"], "dataset": s["dataset"],
            "prompt_mode": "short_en" if s["arm"] == "zs" else f"icl-en-{s['tpl']}",
            "prompt_text_sha256": ZS_EN_SHA256 if s["arm"] == "zs" else EN_TEMPLATE_SHA256,
            "prompt_sha256_per_image": tsha, "exemplars": exids, "manifest_sha256": C.sha(json.dumps(items)),
            "memory_sha256": F.sha_file(a.memory), "exemplars_sha256": F.sha_file(a.exemplars),
            "captions_sha256": F.sha_file(a.captions), "frozen_config_sha256": S2.PINS[S2.FROZEN],
            "decoder_sha256": C.PINS["scripts/lb/decode_hf_vlm.py"], "wrapper_sha256": F.sha_file(Path(__file__)),
            "max_new_tokens": N_NEW, "batch_size": m["batch_size"], "dtype": m["dtype"],
            "attn_implementation": m["attn_implementation"], "processor_kwargs": m["processor_kwargs"],
            "generation_config": net.generation_config.to_diff_dict(), "machine_id": os.environ.get("VSPS_MACHINE_ID"),
            "git_head": lb.git("rev-parse", "HEAD"), "git_dirty": None if status is None else bool(status),
            "job_sha256": os.environ.get("VSPS_JOB_SHA256"), "venv_freeze_sha256": os.environ.get(
                "VSPS_VENV_FREEZE_SHA256"), "packages": lb.packages(), "n_images": len(items), "resumed": resumed,
            "started_utc": started, "finished_utc": lb.utc(),
            "parity_slice0": {"n": len(solo), "identical": sum(x == r["caption"] for x, r in zip(solo, rows))},
            "gpu": torch.cuda.get_device_name(0), "cuda": torch.version.cuda, "generate_kwargs": kw}
    lb.write_output(out, prov, rows)
    print(f"wrote {out.name}")


def test_side_shas(rec_dir: Path = F.REC_DIR) -> set[str]:
    return {v[2] for s in F.TEST_SIDE for v in F.read_rec(rec_dir / f"{s}.sha256.tsv").values()}


def smoke_items(memory: dict) -> list[tuple[str, str, str]]:
    """The first SMOKE_N clusters' members[0]: memory train/restval images, never a test image."""
    return [(m["cid"], m["members"][0][1], m["members"][0][2]) for m in memory["memory"][:SMOKE_N]]


# ------------------------------------------------------------------------------------------------ English guard
def classes(text: str) -> list[str]:
    """COCO-80 classes a caption names (score_coco_probe.en_classes), in order of first mention."""
    found = SC.en_classes(text, SYN)
    low = text.lower()
    return sorted(found, key=lambda c: min((low.find(w) for w, k in SYN.items() if k == c and w in low), default=0))


def neighbour_only(caption: str, zs_caption: str, shown: list[str]) -> list[str]:
    zs = SC.en_classes(zs_caption, SYN)
    ex = set().union(*(SC.en_classes(c, SYN) for c in shown)) if shown else set()
    return [o for o in classes(caption) if o not in zs and o in ex]


def function_end(text: str) -> bool:
    w = re.sub(r"[^\w\s]", " ", text.lower()).split()
    return bool(w) and w[-1] in FUNCTION_END


def delete(caption: str, rejected: set[str], zs_caption: str) -> tuple[str, str]:
    """guard.delete, translated: units at , ; and the SPLIT words; a unit naming a rejected class is dropped with
    the separator before it; the subject unit, an empty or function-word end, or a changed class set falls back to
    the zero-shot caption."""
    if not rejected:
        return caption, "kept"
    body = caption.strip()
    m = END.search(body)
    end, body = (m.group(), body[:m.start()]) if m else ("", body)
    parts = SPLIT.split(body)
    units = list(zip([""] + parts[1::2], parts[0::2]))
    drop = [bool(SC.en_classes(u, SYN) & rejected) for _s, u in units]
    if drop[0]:
        return zs_caption, "fallback"
    out = "".join(s + u for (s, u), d in zip(units, drop) if not d).strip()
    if not out or SC.en_classes(out, SYN) != SC.en_classes(caption, SYN) - rejected or function_end(out):
        return zs_caption, "fallback"
    return out + end, "deleted"


def guarded(caption: str, zs_caption: str, shown: list[str], score: dict, tau: float) -> tuple[str, list, list, str]:
    no = neighbour_only(caption, zs_caption, shown)
    rej = [o for o in no if tau == math.inf or (tau > -math.inf and score[o] < tau)]
    out, how = delete(caption, set(rej), zs_caption)
    return out, no, rej, how


def items(runs: list[dict], zs: dict, caps: dict[str, str]) -> list[dict]:
    out = {}
    for r in runs:
        for i, cap in r["predictions"].items():
            for o in neighbour_only(cap, zs["predictions"][i], [caps[c] for c in r["exemplars"][i]]):
                out[(r["dataset"], i, o)] = {"dataset": r["dataset"], "image_id": i, "class": o}
    return [out[k] for k in sorted(out)]


def cmd_items(a) -> None:
    cfg = S2.frozen()
    runs, zs = [G.read_preds(p) for p in a.runs], G.read_preds(a.zs)
    model = zs["model"]
    want = {spec(cfg, a.set, model, arm)["run_id"] for arm in ("ret", "rand")} if guarded_model(cfg, model) else set()
    if not want or {r["run_id"] for r in runs} != want or zs["run_id"] != spec(cfg, a.set, model, "zs")["run_id"]:
        raise SystemExit("items: exactly InternVL3's ret and rand runs and its zs run of this set")
    if any(r.get("c_schema") != SCHEMA for r in runs + [zs]):
        raise SystemExit("items: not C-EN runs")
    rows = items(runs, zs, load_captions(a.captions, a.memory))
    out_ok(a.out).write_text("".join(json.dumps({**r, "generator": model}) + "\n" for r in rows), encoding="utf-8")
    print(f"{len(rows)} neighbour-only items")


def vp_en() -> dict:
    return {**G.s2()["verifier_protocol"], "english_class_map": EN_NP}


def stop_marker(out: Path, ds: str) -> Path:
    return out.parent / f"{ds}_VERIFIER_STOP.json"


def registered_fill(out: Path, ds: str, fill):
    """The Qwen3-VL answer-position stop is registered and final for the set (PT §7.6): marker, exit 3."""
    try:
        return fill()
    except SystemExit as e:
        if "not the answer position" not in str(e):
            raise
        stop_marker(out, ds).write_text(json.dumps({"set": ds, "stop": str(e), "utc": lb.utc()}) + "\n")
        print(f"REGISTERED VERIFIER STOP on {ds}")
        sys.exit(3)


def cmd_verify(a) -> None:
    F.host_ok(a.expect_head)
    out = out_ok(a.out)
    if stop_marker(out, a.set).exists():
        sys.exit(3)
    todo = [json.loads(x) for x in Path(a.items).read_text(encoding="utf-8").splitlines() if x]
    if {t["generator"] for t in todo} - {"internvl3_8b"}:
        raise SystemExit("only InternVL3's items are verified")
    rows = smoke_items(json.loads(a.memory.read_text())) if a.set == "smoke" else items_of(a.set)
    paths = {(a.set, i): (a.images / f, h) for i, f, h in rows}
    if any((t["dataset"], t["image_id"]) not in paths for t in todo):
        raise SystemExit("REFUSED: an item image is not in the set")
    reg = C.registration()
    if lb.packages() != reg["venv"]["packages"]:
        raise SystemExit("the verifier runs in the B-N1 venv")
    lb.check_snapshot(reg["models"][VERIFIER], a.snapshot)
    load, ask, about = G.hf_verifier(reg["models"][VERIFIER], a.snapshot)

    def checked(path_sha):
        path, h = path_sha
        if F.sha_file(path) != h:
            raise SystemExit(f"{path.name}: sha256 differs from the record")
        return load(path)

    n = registered_fill(out, a.set, lambda: G.fill(out, todo, paths, (checked, ask), vp_en(), VERIFIER))
    mass = sorted(about.pop("yes_no_mass"))
    about["yes_no_mass_median"] = mass[len(mass) // 2] if mass else None
    Path(str(out) + ".about.json").write_text(json.dumps({**about, "verifier": VERIFIER, "label": LABEL,
                                                          "new_rows": n, "packages": lb.packages()}) + "\n")


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def selftest() -> None:
    assert template_sha() == EN_TEMPLATE_SHA256, f"template sha {template_sha()}"
    assert C.sha(zs_prompt()) == ZS_EN_SHA256, "the zero-shot prompt is evaluate.PROMPTS['short_en']"
    cfg = S2.frozen()
    g = grid(cfg)
    assert len(g) == 12 and all(r.startswith("cen_") for r in g), "2 sets x 2 backbones x 3 arms"
    assert {s["arm"] for s in g.values()} == set(ARMS) and not any("fix" in r or "blind" in r for r in g)
    q = spec(cfg, "coco_test", "qwen25vl_7b", "ret")
    iv = spec(cfg, "coco_test", "internvl3_8b", "ret")
    assert (q["k"], q["order"], q["tpl"], iv["k"], iv["order"], iv["tpl"]) == (8, "first", "T1", 4, "last", "T2")
    assert not guarded_model(cfg, "qwen25vl_7b") and guarded_model(cfg, "internvl3_8b"), "frozen tau"
    assert F.refuses(lambda: spec(cfg, "coco_kval", "qwen25vl_7b", "ret")), "Karpathy val is never decoded"
    assert F.refuses(lambda: spec(cfg, "coco_test", "qwen25vl_7b", "fix")), "no fix arm"
    p = prompt("T2", ["one example", "two example"])
    assert p.splitlines() == [HEADER, "Example 1: one example", "Example 2: two example", TAILS["T2"]]
    # examples: refusal of the image itself and of a test-side sha
    memory = {"memory": [{"cid": f"e{n:06d}", "members": [[n, f"f{n}.jpg", f"s{n}"]]} for n in range(10)]}
    ex = {"ret": {"coco_test": {"1": [[f"e{n:06d}", 0.9 - n / 20] for n in range(8)]}},
          "rand": {"coco_test": {"1": [f"e{n:06d}" for n in (9, 8, 7, 6, 5, 4, 3, 2)]}}}
    it = [("1", "x.jpg", "q1")]
    assert check_exemplars(it, iv, ex, memory, set())["1"] == ["e000003", "e000002", "e000001", "e000000"], "last"
    assert F.refuses(lambda: check_exemplars([("1", "x.jpg", "s2")], iv, ex, memory, set())), "the image itself"
    assert F.refuses(lambda: check_exemplars(it, q, ex, memory, {"s5"})), "a test-side sha"
    assert len(smoke_items({"memory": memory["memory"] * 2})) == SMOKE_N
    # English guard, on sentences written for this test
    assert set(EN_NP) == set(SYN.values()) and EN_NP["apple"] == "an apple" and EN_NP["dog"] == "a dog"
    cap = "a zebra waiting beside a motorcycle on a violet moon."
    shown = ["a red motorcycle parked by a tower"]
    zs = "a zebra with a hat on a moon"
    assert neighbour_only(cap, zs, shown) == ["motorcycle"] and neighbour_only(cap, "a zebra", ["a dog"]) == []
    assert delete(cap, {"motorcycle"}, "zs") == ("a zebra waiting on a violet moon.", "deleted")
    assert delete("two dogs and a table", {"dining table"}, "zs") == ("two dogs", "deleted")
    assert delete("a table and two dogs", {"dining table"}, "zs") == ("zs", "fallback"), "the subject is never cut"
    assert delete("a motorcycle", {"motorcycle"}, "zs") == ("zs", "fallback")
    assert delete("a dog beside the, a bicycle", {"bicycle"}, "zs") == ("zs", "fallback"), "function-word end"
    assert delete(cap, set(), "zs") == (cap, "kept")
    for c in (cap, "two dogs, a table; three chairs in a room"):
        for o in classes(c):
            out, how = delete(c, {o}, "zs")
            assert how == "fallback" or SC.en_classes(out, SYN) == SC.en_classes(c, SYN) - {o}, (c, o)
    sc = {"motorcycle": 0.15}
    assert guarded(cap, zs, shown, sc, 0.1)[2] == [] and guarded(cap, zs, shown, sc, 0.2)[2] == ["motorcycle"]
    assert guarded(cap, zs, shown, {}, -math.inf)[2] == [] and guarded(cap, zs, shown, {}, math.inf)[2] == ["motorcycle"]
    run = {"dataset": "coco_test", "predictions": {"1": cap}, "exemplars": {"1": ["e000000"]}}
    assert items([run], {"predictions": {"1": zs}}, {"e000000": shown[0]}) == [
        {"dataset": "coco_test", "image_id": "1", "class": "motorcycle"}]
    vp = vp_en()
    assert vp["question_template"].format(np=vp["english_class_map"]["motorcycle"]) == \
        "Is there a motorcycle in the image? Answer yes or no."
    with tempfile.TemporaryDirectory() as tmp:
        cache = Path(tmp) / "c.jsonl"
        todo = [{"dataset": "coco_test", "image_id": i, "class": o, "generator": "internvl3_8b"}
                for i in ("1", "2") for o in ("dog", "motorcycle")]
        n = G.fill(cache, todo, {("coco_test", i): i for i in ("1", "2")},
                   (lambda p: p, lambda q, px: 0.25 if px is None else 0.75), vp, VERIFIER)
        assert n == 4 and all(json.loads(x)["p_with"] == 0.75 for x in cache.read_text().splitlines())
        try:
            registered_fill(cache, "coco_test", lambda: G.answer_position_check([0.1] * 20))
            raise AssertionError("the answer-position stop did not fire")
        except SystemExit as e:
            assert e.code == 3 and stop_marker(cache, "coco_test").is_file()
    print("selftest ok: 12 cen_ runs (ret, rand, zs; frozen k/order/tpl/tau), English templates pinned, zs = "
          "short_en, examples refuse the image itself and test-side shas, smoke on memory images only, English "
          "guard (neighbour-only, deletion invariant, subject and function-word fallback, thresholds), S2 question "
          "with the COCO-80 class map, verifier cache, registered verifier stop")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("runs")
    p.add_argument("--set", choices=SETS, required=True)
    p.add_argument("--model", choices=C.MODELS)
    p.add_argument("--arm", nargs="+", choices=ARMS, default=list(ARMS))
    p = sub.add_parser("decode")
    p.add_argument("--run-ids", nargs="+", required=True)
    for k in ("snapshot", "memory", "captions", "exemplars", "images", "out-dir"):
        p.add_argument(f"--{k}", type=Path, required=True)
    p.add_argument("--expect-head", required=True)
    p = sub.add_parser("items")
    p.add_argument("--set", choices=SETS, required=True)
    p.add_argument("--runs", nargs="+", type=Path, required=True)
    for k in ("zs", "memory", "captions", "out"):
        p.add_argument(f"--{k}", type=Path, required=True)
    p = sub.add_parser("verify")
    p.add_argument("--set", choices=SETS, required=True)
    for k in ("items", "images", "snapshot", "memory", "out"):
        p.add_argument(f"--{k}", type=Path, required=True)
    p.add_argument("--expect-head", required=True)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    handlers = {"runs": lambda: print(" ".join(spec(S2.frozen(), a.set, m, arm)["run_id"] for m in
                                               ([a.model] if a.model else C.MODELS) for arm in a.arm)),
                "decode": lambda: decode_runs(a), "items": lambda: cmd_items(a), "verify": lambda: cmd_verify(a)}
    handlers.get(a.cmd, lambda: ap.error("mode?"))()


if __name__ == "__main__":
    main()
