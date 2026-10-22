#!/usr/bin/env python3
"""Paper E' pilot (EXPLORATORY / DEV-PILOT, CC-098; not confirmatory): three zero-shot greedy Vietnamese arms.
Note: manuscript/prereg/2026-10-23_eprime_pilot/PILOT_NOTE.md.

  D  direct Vietnamese caption (C's/B's registered short prompt, image)
  T  English caption (image), then a text-only translation by the same model (no image)
  A  English caption (image), then a Vietnamese caption written with the image AND the English caption

  python scripts/eprime_pilot/decode_pilot.py --selftest              CPU, no data
  python scripts/eprime_pilot/decode_pilot.py decode --model M --snapshot DIR --lists L --out-dir D     GPU
Model loading, fixed batch slices, resume, the greedy call and the text-only path are C's and the LB decoder's,
imported unchanged (scripts/c_stage2/stage2.py, decode2.py). Outputs: <run>.preds.json per (model, set, arm), arm
en being the shared first step of T and A. Caption text stays in those files; it is never printed or committed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "scripts/c_stage2"))
import decode2 as D2  # noqa: E402  text_only_generate; imports stage2, which checks the stage-1 shas first
import stage2 as S2  # noqa: E402

C, lb = S2.C, S2.lb
LABEL = "EXPLORATORY / DEV-PILOT (CC-098), not confirmatory"
SCHEMA = "vsps.eprime_pilot.v1"
PILOT = "manuscript/prereg/2026-10-23_eprime_pilot"
XM300 = f"{PILOT}/xm_dev300.tsv"
XM300_SHA256 = "b633153409eb1992c5d1857f8f8928471a01e5ac6103d2b9ab5ce6459726a443"
MODELS = C.MODELS
SETS = {"ktvic_dev299": {"src": "ktvic", "image_dir": "ktvic/images"},
        "xm_dev300": {"src": "xm3600", "image_dir": "c_xm_dev500/images"}}
ARMS = ("en", "t", "d", "a")  # en first: T and A both need it; t second: its text-only path is checked early
EN_PROMPT = "Describe this image in ONE short English sentence, like a caption. Do not list items or explain."
EN_PROMPT_SHA256 = "0cdbdf77fae4c04bdf4cd626a9eaf9adec5ef0411aac5d816f6c916a69604893"  # = evaluate.PROMPTS["short_en"], Paper A's English short prompt
T_PROMPT = ("Dịch chú thích ảnh tiếng Anh sau sang tiếng Việt. Chỉ viết MỘT câu tiếng Việt ngắn gọn, "
            "giống chú thích ảnh. Không giải thích.\nChú thích tiếng Anh: {en}")
A_ANCHOR = "Chú thích tiếng Anh của bức ảnh này (chỉ để tham khảo, có thể thiếu hoặc sai): {en}\n"  # + the D prompt
MAX_EMPTY = 0.2  # a text-only arm with more empty captions than this stops the job (path untested on a GPU)


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


# ------------------------------------------------------------------------------------------------ sets
def xm300_rows(xm_dev500: list) -> list:
    """The first 300 XM-dev500 rows in sorted id order (no seed)."""
    return sorted((tuple(r) for r in xm_dev500), key=lambda r: r[0])[:300]


def manifest(name: str, lists: dict) -> list[tuple[str, str, str]]:
    """[(id, file, sha256)] of a pilot set, refused if any row is a test image of A, B or C (stage-2 carve-out rule)."""
    if name == "ktvic_dev299":
        rows = C.manifest("ktvic_dev299", lists)  # pinned dev299.tsv, stage-1 refusal
    else:
        rows = xm300_rows(S2.manifest2("xm_dev500", lists))
        if lb.sha256_file(ROOT / XM300) != XM300_SHA256:
            raise SystemExit(f"{XM300}: sha256 differs from the pin")
        if "".join("\t".join(r) + "\n" for r in rows) != (ROOT / XM300).read_text(encoding="utf-8"):
            raise SystemExit(f"{XM300}: not the first 300 sorted XM-dev500 rows of lists.json")
    ids2, hashes2 = S2.refused2(lists)
    C.refuse_rows(rows, SETS[name]["src"], ids2, hashes2 | {r[2] for r in lists["sets"]["xm_test2500"]})
    return rows


def check_disjoint(rows_by_set: dict, lists: dict) -> dict:
    """Counts only: pilot images against C's XM-test2500 and the still-refused shas (OV-test, A, B). All must be 0."""
    test = {r[2] for r in lists["sets"]["xm_test2500"]} | S2.refused2(lists)[1]  # refused2: refuse minus the carve-out
    return {n: sum(r[2] in test for r in rows) for n, rows in rows_by_set.items()}


# ------------------------------------------------------------------------------------------------ one arm
def prompts(arm: str, ids: list, en: dict | None, zs: str) -> dict[str, str]:
    if arm == "en":
        return {i: EN_PROMPT for i in ids}
    if arm == "d":
        return {i: zs for i in ids}
    if arm == "t":
        return {i: T_PROMPT.format(en=en[i]) for i in ids}
    return {i: A_ANCHOR.format(en=en[i]) + zs for i in ids}


def empty_share(preds: dict) -> float:
    return sum(not v.strip() for v in preds.values()) / max(len(preds), 1)


def run_arm(run_id: str, arm: str, ds: str, items: list, texts: dict, gen, ctx: dict, out: Path) -> dict:
    """Decode one arm (resumable) and write the LB-schema output; returns {image id: caption}. An existing output
    is read back, not decoded again."""
    if out.exists():
        return json.loads(out.read_text(encoding="utf-8"))["predictions"]
    m, kw, started = ctx["m"], {"max_new_tokens": ctx["n_new"], "do_sample": False, "num_beams": 1}, lb.utc()
    tsha = {i: sha(t) for i, t in texts.items()}
    part = Path(str(out) + ".partial.jsonl")
    resumed = part.exists()
    spec = {"run_id": run_id, "arm": arm, "dataset": ds, "model": ctx["model"]}
    rows = lb.decode_slices(items, m["batch_size"], lambda sl: gen(sl, [texts[i] for i, _f, _h in sl]), part,
                            lb.run_key(ctx["reg_sha"], spec, m, kw, json.dumps(tsha, sort_keys=True), items))
    solo = [gen([it], [texts[it[0]]])[0][0] for it in items[:m["batch_size"]]] if m["batch_size"] > 1 else []
    status = lb.git("status", "--porcelain", "--untracked-files=no")
    prov = {"schema": lb.SCHEMA, "label": LABEL, "pilot_schema": SCHEMA, "prereg_id": "E' pilot (CC-098)",
            "prereg_sha256": ctx["note_sha256"], "decoder_sha256": ctx["decoder_sha256"], "run_id": run_id,
            "arm": arm, "model": ctx["model"], "hub_id": m["hub_id"], "revision": m["revision"], "dataset": ds,
            "image_input": arm != "t", "prompt_mode": f"eprime-{arm}", "prompt_text_sha256": ctx["prompt_sha"][arm],
            "prompt_sha256_per_image": tsha, "manifest_sha256": C.sha(json.dumps(items)),
            "max_new_tokens": ctx["n_new"], "batch_size": m["batch_size"], "dtype": m["dtype"],
            "attn_implementation": m["attn_implementation"], "processor_kwargs": m["processor_kwargs"],
            "generation_config": ctx["gen_cfg"], "machine_id": os.environ.get("VSPS_MACHINE_ID"),
            "git_head": lb.git("rev-parse", "HEAD"), "git_dirty": None if status is None else bool(status),
            "job_sha256": os.environ.get("VSPS_JOB_SHA256"), "venv_freeze_sha256": os.environ.get(
                "VSPS_VENV_FREEZE_SHA256"), "packages": ctx["packages"], "n_images": len(items), "resumed": resumed,
            "parity_slice0": {"n": len(solo), "identical": sum(a == r["caption"] for a, r in zip(solo, rows))},
            "started_utc": started, "finished_utc": lb.utc(), "generate_kwargs": kw}
    lb.write_output(out, prov, rows)
    return {r["image_id"]: r["caption"] for r in rows}


def decode_set(ds: str, items: list, gens: dict, ctx: dict, out_dir: Path) -> None:
    ids = [i for i, _f, _h in items]
    got: dict[str, dict] = {}
    for arm in ARMS:
        texts = prompts(arm, ids, got.get("en"), ctx["zs"])
        gen = gens["text"] if arm == "t" else gens["image"]
        rid = f"ep_{ctx['model']}_{ds}-{arm}"
        got[arm] = run_arm(rid, arm, ds, items, texts, gen, ctx, out_dir / f"{rid}.preds.json")
        if arm in ("en", "t") and empty_share(got[arm]) > MAX_EMPTY:
            raise SystemExit(f"{rid}: {empty_share(got[arm]):.0%} empty captions; stop and tell the operator")


def decode_model(model: str, snapshot: Path, lists_path: Path, out_dir: Path) -> None:
    lists = C.load_lists(lists_path)
    reg = C.registration()
    m = reg["models"][model]
    if lb.packages() != reg["venv"]["packages"]:
        raise SystemExit(f"package versions {lb.packages()} differ from the B-N1 venv")
    lb.check_snapshot(m, snapshot)
    plan = {ds: manifest(ds, lists) for ds in SETS}  # every refusal before the model loads
    if any(check_disjoint(plan, lists).values()):
        raise SystemExit("REFUSED: a pilot image is in a C or A test set")
    S2.check_folder("xm_dev500", lists)
    zs, n_new = lb.prompt_text(reg, "short"), reg["decode"]["max_new_tokens"]["short"]
    if sha(zs) != C.ZS_PROMPT_SHA256 or sha(EN_PROMPT) != EN_PROMPT_SHA256:
        raise SystemExit("a prompt differs from its pin")
    out_dir.mkdir(parents=True, exist_ok=True)
    proc, net = lb.load(m, snapshot, "cuda:0")
    ctx = {"m": m, "model": model, "zs": zs, "n_new": n_new, "reg_sha": C.PINS[C.B_N1], "packages": lb.packages(),
           "note_sha256": lb.sha256_file(ROOT / PILOT / "PILOT_NOTE.md"), "gen_cfg": net.generation_config.to_diff_dict(),
           "decoder_sha256": lb.sha256_file(Path(__file__)), "prompt_sha": {
               "en": sha(EN_PROMPT), "d": C.ZS_PROMPT_SHA256, "t": sha(T_PROMPT), "a": sha(A_ANCHOR + zs)}}
    for ds, items in plan.items():
        folder = lb.DATA / "datasets" / SETS[ds]["image_dir"]
        gens = {"image": lb.make_generate(proc, net, zs, n_new, folder), "text": D2.text_only_generate(proc, net, n_new)}
        decode_set(ds, items, gens, ctx, out_dir)
        print(f"done {model} {ds}")


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def selftest() -> None:
    # sets: the committed tsv is the first 300 sorted XM-dev500 rows, disjoint from every test/refused sha
    lists = C.load_lists(ROOT / "manuscript/prereg/2026-10-22_c_stage1/lists.json")
    assert lb.sha256_file(ROOT / XM300) == XM300_SHA256
    kt, xm = (manifest(n, lists) for n in SETS)
    assert (len(kt), len(xm)) == (299, 300) and [r[0] for r in xm] == sorted(r[0] for r in xm)
    assert check_disjoint({"kt": kt, "xm": xm}, lists) == {"kt": 0, "xm": 0}
    assert xm300_rows([("b", "f", "h"), ("a", "f", "h")] * 200)[:2] == [("a", "f", "h")] * 2
    assert C.refuses(lambda: C.refuse_rows([("x", "f", lists["sets"]["xm_test2500"][0][2])], "xm3600",
                                           *S2.refused2(lists))), "an XM-test2500 image is refused"
    # prompts: T carries the English text and no instruction to look; A carries it plus the registered D prompt
    en = {"i1": "w1 w2"}
    p = {a: prompts(a, ["i1"], en, "ZS")["i1"] for a in ARMS}
    assert p["en"] == EN_PROMPT and p["d"] == "ZS" and "w1 w2" in p["t"] and "ZS" not in p["t"]
    assert p["a"] == A_ANCHOR.format(en="w1 w2") + "ZS" and sha(EN_PROMPT) == EN_PROMPT_SHA256
    assert EN_PROMPT in (ROOT / "scripts/evaluate.py").read_text(encoding="utf-8"), "EN prompt = evaluate.PROMPTS"
    assert empty_share({"a": "", "b": " ", "c": "w1"}) == 2 / 3
    # an arm run with a fake generator: LB-schema output, resume, read-back without decoding
    items = [(f"i{n}", f"i{n}.jpg", "0" * 64) for n in range(5)]
    calls = []

    def gen(sl, texts):
        calls.append(len(sl))
        return [(f"w{n}", 2, False) for n in range(len(sl))]

    ctx = {"m": {"batch_size": 2, "hub_id": "h", "revision": "r", "dtype": "d", "attn_implementation": "x",
                 "processor_kwargs": {}}, "model": "qwen25vl_7b", "n_new": 60, "reg_sha": "0" * 64, "packages": {},
           "note_sha256": "0" * 64, "gen_cfg": {}, "decoder_sha256": "0" * 64, "prompt_sha": {a: "0" * 64 for a in ARMS}}
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "r.preds.json"
        texts = prompts("d", [i for i, _f, _h in items], None, "ZS")
        got = run_arm("r", "d", "xm_dev300", items, texts, gen, ctx, out)
        n_calls = len(calls)
        assert set(got) == {i for i, _f, _h in items} and json.loads(out.read_text())["image_input"] is True
        assert run_arm("r", "d", "xm_dev300", items, texts, gen, ctx, out) == got and len(calls) == n_calls
        lb.validate_output(out.read_text())
        t = run_arm("rt", "t", "xm_dev300", items, texts, gen, ctx, Path(tmp) / "rt.preds.json")
        assert json.loads((Path(tmp) / "rt.preds.json").read_text())["image_input"] is False and len(t) == 5
        assert C.refuses(lambda: decode_set("xm_dev300", items, {"image": gen, "text": lambda sl, tx: [("", 1, False)] *
                                                                  len(sl)}, {**ctx, "zs": "ZS"}, Path(tmp))), \
            "empty text-only captions stop the job"
    print("selftest ok: sets (299 + first 300 sorted, 0 in test/refused), prompts, arm output/resume, empty-text stop")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("decode")
    p.add_argument("--model", choices=MODELS, required=True)
    p.add_argument("--snapshot", type=Path, required=True)
    p.add_argument("--lists", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.cmd != "decode":
        ap.error("decode or --selftest")
    decode_model(a.model, a.snapshot, a.lists, a.out_dir)


if __name__ == "__main__":
    main()
