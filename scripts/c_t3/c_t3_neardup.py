#!/usr/bin/env python3
"""C-T3 test-side near-duplicate pass (PI-1030f: test = full near-dup), CPU, M1 (machine id m3) only, run once in the
job preflight before any decode. Rule = W25 RULE §3 unchanged (w25.rule: C1 byte-identical OR C2 build_memory.near
OR C3 SSCD cosine > 0.75; SSCD >= 0.5 reported only), the rule W25-K1 applied. Flickr30K test (1,000) is compared with
the COCO memory (C-EN feats_memory.npz, 112,320 rows, pinned), the carve (1,000), val (1,014) and the earlier test files.
The decision stays on all 1,000 test images; `c_t3.py t3 --exclude` prints the dedup row beside it. Output: file
names, counts and shas only; no caption, prediction or score; no pair is ever shown to anyone.

    python3 scripts/c_t3/c_t3_neardup.py --selftest                                   CPU, synthetic features
    $FT scripts/c_t3/c_t3_neardup.py run --test D --val D --carve D --mem-feats NPZ --mem-files F --mem-root D \
        --sscd PT --out O                                                             M1 (m3), venv-cenfeat
Each D holds images/ and manifest.json {file: sha256}.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "w25"))
import w25  # noqa: E402  rule, load, KEYS, ok_sscd, bm (build_memory.features / near, unchanged)

LABEL = "TIER 3 / TEST, ONE LOOK (C-T3)"
FEATS_MEMORY_SHA256 = "caf4a62199fccfe903e3a553a3717673d62a32ae07a2e289c2a706d70132e437"  # C-EN SHA256SUMS_feats
COUNTS = {"test": 1000, "val": 1014, "carve": 1000}
PARITY_N = 50  # CC-190 W7 form: features recomputed here equal the pinned memory rows


def sub(f: dict, idx) -> dict:
    idx = list(idx)
    return {"sha": [f["sha"][i] for i in idx], **{k: f[k][idx] for k in w25.KEYS}}


def staged(folder: Path, name: str, sscd: str, workers: int) -> tuple[list[str], dict]:
    """(sorted file names, features) of one staged set; every file sha-checked against its manifest."""
    man = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    names = sorted(man)
    if len(names) != COUNTS[name]:
        raise SystemExit(f"FAULT: {folder} holds {len(names)} files, not {COUNTS[name]}")
    paths = [folder / "images" / n for n in names]
    if any(w25.K.sha_file(p) != man[n] for p, n in zip(paths, names)):
        raise SystemExit(f"FAULT: a {name} image differs from its manifest")
    f = w25.bm().features(paths, sscd, workers=workers, retry_truncated=True)
    if f["unreadable"]:
        raise SystemExit(f"FAULT: {len(f['unreadable'])} unreadable {name} images (back to the judge, before any decode)")
    f["truncated_names"] = [[names[i], b] for i, b in f["truncated"]]  # CC-202 W3: disclosure only, never an exclusion
    return names, f


def parity(mem: dict, new: dict) -> dict:
    """Memory images featured here vs the pinned rows of the same sha: hashes equal, SSCD cosine >= 0.999."""
    at = {h: n for n, h in enumerate(mem["sha"])}
    rows = [at.get(h) for h in new["sha"]]
    if None in rows:
        raise SystemExit("FAULT: a parity image is not a row of the pinned memory features")
    same = all(np.array_equal(mem[k][rows], new[k]) for k in w25.KEYS[:4])
    x, y = mem["sscd"][rows], new["sscd"]
    cos = (x * y).sum(1) / (np.linalg.norm(x, axis=1) * np.linalg.norm(y, axis=1))
    rec = {"n": len(rows), "hashes_equal": bool(same), "sscd_cos_min": float(cos.min())}
    if not same or not (cos >= 0.999).all():
        raise SystemExit(f"FAULT: feature parity failed {rec}")
    return rec


def truncated_record(sets: dict[str, dict]) -> dict[str, list]:
    """CC-202 W3: per staged set, [file, bytes lost] of images decoded with retry_truncated (disclosure only)."""
    return {k: f["truncated_names"] for k, f in sets.items()}


def masks(x: dict, y: dict) -> dict[str, np.ndarray]:
    return w25.rule(x, y, w25.bm().near)


def decide(names: list[str], test: dict, refs: dict[str, dict]) -> dict:
    """Per reference set: test files matched under C1+C2, C3, the union (excluded) and the SSCD >= 0.5 count. Within
    test, a file is excluded when it matches an earlier file (sorted order), as C-T2 dupcheck's within-val rule."""
    out = {}
    for ref, y in refs.items():
        m = masks(test, y)
        out[ref] = {k: [names[i] for i in np.flatnonzero(m[k])] for k in ("C1_C2_registered", "C3_sscd_0.75", "excluded")}
        out[ref]["report_sscd_0.5"] = int(m["report_sscd_0.5"].sum())
    w = {k: np.zeros(len(names), bool) for k in ("C1_C2_registered", "C3_sscd_0.75", "excluded", "report_sscd_0.5")}
    for i in range(1, len(names)):
        m = masks(sub(test, [i]), sub(test, range(i)))
        for k in w:
            w[k][i] = m[k][0]
    out["within_test"] = {k: [names[i] for i in np.flatnonzero(w[k])] for k in ("C1_C2_registered", "C3_sscd_0.75", "excluded")}
    out["within_test"]["report_sscd_0.5"] = int(w["report_sscd_0.5"].sum())
    return {"sets": out, "exclude": sorted({f for v in out.values() for f in v["excluded"]})}


def cmd_run(a) -> None:
    try:
        mid = Path("/root/.vsps_machine_id").read_text().strip().lower()
    except OSError:
        mid = ""
    if mid != "m3":
        raise SystemExit("REFUSED: the test-side pass runs on M1 (machine id m3) only")
    if Path(a.out).exists():
        raise SystemExit(f"REFUSED: {a.out} exists; the pass runs once")
    sscd = w25.ok_sscd(Path(a.sscd))
    mem = w25.load(Path(a.mem_feats), FEATS_MEMORY_SHA256)
    files = json.loads(Path(a.mem_files).read_text(encoding="utf-8"))  # {cid: [file, sha256]}
    pick = [files[c] for c in sorted(files)[:PARITY_N]]
    par = parity(mem, w25.bm().features([Path(a.mem_root) / f for f, _h in pick], sscd, workers=a.workers))
    names, test = staged(Path(a.test), "test", sscd, a.workers)
    refs = {"coco_memory": mem}
    for name in ("carve", "val"):
        refs[name] = staged(Path(getattr(a, name)), name, sscd, a.workers)[1]
    res = decide(names, test, refs)
    res["truncated"] = truncated_record({"test": test, "carve": refs["carve"], "val": refs["val"]})
    inputs = {"feats_memory": FEATS_MEMORY_SHA256, "sscd": w25.SSCD_SHA,
              **{f"{n}_manifest": w25.K.sha_file(Path(getattr(a, n)) / "manifest.json") for n in ("test", "val", "carve")}}
    Path(a.out).write_text(json.dumps({"label": LABEL, "rule": "W25 RULE §3: C1 or C2 or C3 (PI-1030f test = full near-dup)",
                                       "parity": par, "inputs_sha256": inputs, **res}, indent=1) + "\n")
    print(json.dumps({k: len(v["excluded"]) for k, v in res["sets"].items()} | {"exclude": len(res["exclude"])}))


def selftest() -> None:
    rng = np.random.default_rng(0)

    def fake(n: int, tag: str) -> dict:
        v = rng.normal(size=(n, 512)).astype(np.float32)
        v /= np.linalg.norm(v, axis=1, keepdims=True)
        h = rng.integers(0, 2**63, (4, n), dtype=np.int64).astype(np.uint64)
        return {"sha": [f"{tag}{i}" for i in range(n)], "phash": h[0], "dhash": h[1], "phash_m": h[2], "dhash_m": h[3],
                "sscd": v}

    test, mem = fake(6, "t"), fake(20, "m")
    mem["sha"][3] = test["sha"][0]  # C1: byte-identical
    mem["sscd"][5] = test["sscd"][1]  # C3: SSCD cosine 1 > 0.75 (hashes differ)
    test["sha"][5], test["sscd"][5] = test["sha"][2], test["sscd"][2]  # within test: file 5 repeats file 2
    for k in w25.KEYS[:4]:
        test[k][5] = test[k][2]
    names = [f"f{i}.jpg" for i in range(6)]
    r = decide(names, test, {"coco_memory": mem, "carve": fake(5, "c")})
    s = r["sets"]
    assert s["coco_memory"]["C1_C2_registered"] == ["f0.jpg"] and s["coco_memory"]["C3_sscd_0.75"] == ["f1.jpg"]
    assert s["coco_memory"]["excluded"] == ["f0.jpg", "f1.jpg"] and s["carve"]["excluded"] == []
    assert s["within_test"]["excluded"] == ["f5.jpg"], "the later file of a within-test pair"
    assert r["exclude"] == ["f0.jpg", "f1.jpg", "f5.jpg"]
    tr = truncated_record({"test": {**test, "truncated_names": [["f3.jpg", 12]]}, "val": {"truncated_names": []}})
    assert tr == {"test": [["f3.jpg", 12]], "val": []} and "f3.jpg" not in r["exclude"], "truncated: disclosure only"
    assert parity(mem, sub(mem, [3, 4]))["hashes_equal"]
    bad = sub(mem, [3, 4])
    bad["phash"] = bad["phash"] ^ np.uint64(1)
    try:
        parity(mem, bad)
        raise AssertionError("parity must FAULT")
    except SystemExit as e:
        assert "FAULT" in str(e)
    print("selftest ok: W25 RULE §3 per set (C1, C3, union), within-test later file, parity FAULT, truncated record")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sp = ap.add_subparsers(dest="cmd")
    p = sp.add_parser("run")
    for k in ("test", "val", "carve", "mem_feats", "mem_files", "mem_root", "sscd", "out"):
        p.add_argument("--" + k.replace("_", "-"), type=Path, required=True)
    p.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.cmd == "run":
        return cmd_run(a)
    ap.print_help()


if __name__ == "__main__":
    main()
