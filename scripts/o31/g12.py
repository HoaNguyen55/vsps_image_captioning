"""O31 GPU jobs (host only; laptop runs are synthetic tests). `$PY -I -B g12.py <cmd> ...`, VSPS_REPO = pinned snapshot.

  stage1         G1 part 1: --stage NCS_DATA --train NCS_DATA/datasets/ktvic/train_data.json --records-tar TAR
                 --release TREE (git archive 1f30d09) --qwen SNAP --vintern SNAP (both $HF_HOME cache snapshots)
                 --out G1 (the 69 KTVIC-train images without records; ERRATUM_O31_3)
  probe          G1 part 2 (vintern, --out G1: same launch.json clock) / G2 (internvl3, one job, E4): --family --records DIR [DIR ...] [--exclude FILE] --images DIR
                 --snapshot SNAP --out OUT [--refused-sha FILE]   (default refused list: exclusion.json, pinned)
  decode         one arm: --system --snapshot SNAP [--adapter DIR] --items TSV --images DIR --lang vi|en --batch 1|8
                 [--parity-record FILE] [--en-prompt TEXT] --out PREFIX   (bf16 base, E5; --lang en needs the E6 prompt)
  parity-decode  Q13: one system on the 50 dev images at batch 1 and 8 -> OUT/<system>.tokens.json (token ids only)
  parity-decide  Q13: the three systems' token files -> OUT/parity.json (decode.parity)
  smoke          H-G: --family vintern|internvl3|student --snapshot SNAP --images DIR --names F1..F5
                 (already-explored M-HalDetect val images only, CC-501 ruling 6) -> OUT/smoke_<family>.json
Every command writes counts, shas and token ids only to its log; captions go to the preds files on the host.
"""
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, os.environ.get("O31_SRC", str(Path(__file__).resolve().parent / "src")))  # O31_SRC: tests only

from o31 import decode, probe, stage1  # noqa: E402

SMOKE_QUESTIONS = ("Trong ảnh có người không?", "Trong ảnh có xe không?", "Trong ảnh có chó không?",
                   "Trong ảnh có bàn không?")


def sha(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def image_loader(folder: Path, refused: set):
    from PIL import Image

    def load(name):
        if refused and sha(folder / name) in refused:
            raise SystemExit(f"FAULT {name} is a refused image (sha listed)")
        return Image.open(folder / name).convert("RGB")
    return load


def cmd_stage1(a) -> int:
    stage1.check_env()
    stage1.check_qwen(a.qwen)  # runs repo(), which puts scripts/vsps_j_m0 on the path
    import m0

    stage1.check_vintern(a.vintern)
    m0.check_model(a.vintern)
    gen = stage1.use_release(a.release)  # ERRATUM_O31_3 F1: stage-1 code of 1f30d09, loaded after the HEAD checks
    new = stage1.prepare(a.stage, a.train, a.records_tar, gen)
    return stage1.run(a.out, a.stage, new, gen)


def cmd_probe(a) -> int:
    if a.family == "internvl3":
        probe.g2_inputs(a.records, a.exclude)
    recs = probe.records(a.records, a.exclude)
    items = probe.work(recs, a.family)
    refused = set(a.refused_sha.read_text().split()) if a.refused_sha else probe.refused_shas()
    names = sorted(r["file_name"] for r in recs)
    fn, info = probe.load(a.family, a.snapshot)
    (a.out).mkdir(parents=True, exist_ok=True)
    (a.out / "model.json").write_text(json.dumps(info) + "\n")
    (a.out / "inputs.json").write_text(json.dumps({  # CC-519 N1
        "family": a.family, "n_records": len(recs), "file_names_sha256": probe.sha_lines(names),
        "exclude_sha256": sha(a.exclude) if a.exclude else None, "refused_sha256": probe.sha_lines(sorted(refused)),
        "n_refused": len(refused), "snapshot_revision": info.get("revision")}) + "\n")
    return probe.probe_job(fn, items, a.out, a.family, image_loader(a.images, refused))


def cmd_decode(a) -> int:
    rec = json.loads(a.parity_record.read_text()) if a.parity_record else {}
    cfg = decode.check({"system": a.system, "batch": a.batch, "lang": a.lang, "adapter": a.adapter,
                        "parity_passed": decode.parity_passed(rec)})
    prompt = decode.PROMPTS[a.lang] if a.lang == "vi" else a.en_prompt
    if not prompt:
        raise SystemExit("REFUSED --lang en needs --en-prompt, the ERRATUM_O31_2 E6 string")
    if prompt != decode.PROMPTS[a.lang]:
        raise SystemExit("REFUSED --en-prompt differs from the ERRATUM_O31_2 E6 string")
    model, proc, info = decode.load_student(a.snapshot, a.adapter)
    res = decode.run(decode.make_generate(model, proc, prompt), decode.read_items(a.items), a.images, a.out, cfg["batch"])
    Path(str(a.out) + ".run.json").write_text(json.dumps({**info, "system": a.system, "lang": a.lang,
                                                          "batch": cfg["batch"], "prompt_sha256":
                                                          hashlib.sha256(prompt.encode()).hexdigest(),
                                                          "preds_sha256": res["sha256"], "n": res["n"]}) + "\n")
    return 0


def cmd_parity_decode(a) -> int:
    items = decode.read_items(a.items)
    if len(items) != decode.PARITY_N:
        raise SystemExit("REFUSED the Q13 check uses exactly 50 dev images")
    model, proc, _info = decode.load_student(a.snapshot, a.adapter)
    gen = decode.make_generate(model, proc, decode.PROMPTS["vi"])
    a.out.mkdir(parents=True, exist_ok=True)
    tok = {}
    for b in (1, 8):
        r = decode.run(gen, items, a.images, a.out / f"{a.system}.b{b}", b, keep_tokens=True)
        tok[f"b{b}"] = {row["image_id"]: row["ids"] for row in r["rows"]}
    (a.out / f"{a.system}.tokens.json").write_text(json.dumps(tok) + "\n")
    return 0


def cmd_parity_decide(a) -> int:
    t = {s: json.loads((a.out / f"{s}.tokens.json").read_text()) for s in decode.SYSTEMS}
    res = decode.parity({s: v["b1"] for s, v in t.items()}, {s: v["b8"] for s, v in t.items()})
    (a.out / "parity.json").write_text(json.dumps(res) + "\n")
    print(json.dumps({"batch": res["batch"], "systems_with_mismatch": sorted(res["mismatches"])}))
    return 0


def first_diff(a: list, b: list):
    """First index where two token-id lists differ (a length difference counts at the shorter length); None if equal."""
    if a == b:
        return None
    return next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))


def cmd_smoke(a) -> int:
    probe.explored(a.names, a.images)
    load = image_loader(a.images, set())
    a.out.mkdir(parents=True, exist_ok=True)
    if a.family == "student":
        model, proc, info = decode.load_student(a.snapshot, None)
        gen = decode.make_generate(model, proc, decode.PROMPTS["vi"])
        ims = [load(n) for n in a.names]
        r1 = [gen([im])[0] for im in ims]
        b1 = [t[0] for t in r1]
        b1r = [gen([im])[0][0] for im in ims]
        b5 = [t[0] for t in gen(ims)]
        same = [t[0] for t in gen([ims[0]] * 5)]
        diff = [first_diff(x, y) for x, y in zip(b1, b5)]
        rec = {**info, "n": 5, "n_tokens": [len(x) for x in b1], "n_tokens_b5": [len(x) for x in b5],
               "hit_max_b1": [t[2] for t in r1], "stop_id_b1": [None if t[2] else t[0][-1] for t in r1],
               "repeat_equal_b1": b1 == b1r, "token_equal_b5": b1 == b5, "b5_first_diff": diff,
               "b5_n_diff": sum(d is not None for d in diff),
               "same_image_b5_equal": all(x == b1[0] for x in same),
               "ok_student": b1 == b1r and all(t[1] for t in r1)}
    else:
        fn, info = probe.load(a.family, a.snapshot)
        items = [(n, [(probe.qkey(q), q) for q in SMOKE_QUESTIONS]) for n in a.names]
        rows1 = probe.probe_rows(fn, items, 1, load)
        rec = {**info, "smoke": probe.smoke(rows1)}
        if 8 in probe.FAMILIES[a.family]["batch"]:
            p = probe.batch_parity(rows1, probe.probe_rows(fn, items, 8, load), 5)
            rec["parity_5_images"] = {k: p[k] for k in ("n_probes", "n_bad", "max_abs_diff")}
    rec["image_sha256"] = {n: sha(a.images / n) for n in a.names}
    (a.out / f"smoke_{a.family}.json").write_text(json.dumps(rec) + "\n")
    ok = rec.get("smoke", {}).get("ok", True) and rec.get("ok_student", True)
    print(json.dumps({"family": a.family, "ok": ok}))
    return 0 if ok else 2


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("stage1")
    for k in ("--stage", "--train", "--records-tar", "--release", "--qwen", "--vintern", "--out"):
        g.add_argument(k, type=Path, required=True)
    p = sub.add_parser("probe")
    p.add_argument("--family", choices=sorted(probe.FAMILIES), required=True)
    p.add_argument("--records", type=Path, nargs="+", required=True)
    p.add_argument("--exclude", type=Path)
    p.add_argument("--images", type=Path, required=True)
    p.add_argument("--snapshot", type=Path, required=True)
    p.add_argument("--refused-sha", type=Path)
    p.add_argument("--out", type=Path, required=True)
    for name in ("decode", "parity-decode"):
        d = sub.add_parser(name)
        d.add_argument("--system", choices=decode.ARMS, required=True)
        d.add_argument("--snapshot", type=Path, required=True)
        d.add_argument("--adapter", type=Path)
        d.add_argument("--items", type=Path, required=True)
        d.add_argument("--images", type=Path, required=True)
        d.add_argument("--out", type=Path, required=True)
        if name == "decode":
            d.add_argument("--lang", choices=("vi", "en"), required=True)
            d.add_argument("--en-prompt")
            d.add_argument("--batch", type=int, required=True)
            d.add_argument("--parity-record", type=Path)
    d = sub.add_parser("parity-decide")
    d.add_argument("--out", type=Path, required=True)
    s = sub.add_parser("smoke")
    s.add_argument("--family", choices=("vintern", "internvl3", "student"), required=True)
    s.add_argument("--snapshot", type=Path, required=True)
    s.add_argument("--images", type=Path, required=True)
    s.add_argument("--names", nargs="+", required=True)
    s.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    return {"stage1": cmd_stage1, "probe": cmd_probe, "decode": cmd_decode, "parity-decode": cmd_parity_decode,
            "parity-decide": cmd_parity_decide, "smoke": cmd_smoke}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
