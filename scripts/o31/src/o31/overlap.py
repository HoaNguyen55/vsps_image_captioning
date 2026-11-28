"""W4 overlap rule (prereg §3.5): exact sha + the committed W25 near-duplicate rule (CC-153), on descriptors only.

Rule = scripts/w25/w25.py rule() with build_memory.near, both unchanged (sha d6d12780, e771b92d):
excluded = byte-identical OR (min(pHash, dHash) <= 10 using x's mirrored hashes AND SSCD >= 0.5) OR SSCD > 0.75.
`near` mirrors only the x side, so x is always the set that loses images:
(a) x = training pool vs KTVIC test, UIT-ViIC test, Karpathy test, tier 3 -> hits leave the pool;
(b) x = Karpathy test and x = tier 3, each vs UIT-ViIC test -> hits leave that scoring set.
Feature dict per set: ids (list), sha (list), phash, dhash, phash_m, dhash_m (uint64), sscd (float32, L2-normalised).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

from . import repo

POOL_VS = ("ktvic_test", "uit_test", "karpathy_test", "tier3")
SCORING_VS_UIT = ("karpathy_test", "tier3")


def rule(fx: dict, fy: dict) -> dict:
    repo()
    import build_memory
    import w25

    return w25.rule(fx, fy, build_memory.near)


def w4_pass(feats: dict[str, dict]) -> dict:
    """{set: removed ids} plus counts per comparison; sets absent from `feats` are skipped and named."""
    out = {"removed": {}, "counts": {}, "skipped": []}
    pool = feats["pool"]
    hit = np.zeros(len(pool["ids"]), bool)
    for y in POOL_VS:
        if y not in feats:
            out["skipped"].append(f"pool_vs_{y}")
            continue
        r = rule(pool, feats[y])
        hit |= r["excluded"]
        out["counts"][f"pool_vs_{y}"] = {k: int(v.sum()) for k, v in r.items()}
    out["removed"]["pool"] = sorted(np.asarray(pool["ids"])[hit].tolist())
    for x in SCORING_VS_UIT:
        if x not in feats or "uit_test" not in feats:
            out["skipped"].append(f"{x}_vs_uit_test")
            continue
        r = rule(feats[x], feats["uit_test"])
        out["counts"][f"{x}_vs_uit_test"] = {k: int(v.sum()) for k, v in r.items()}
        out["removed"][x] = sorted(np.asarray(feats[x]["ids"])[r["excluded"]].tolist())
    return out


# ------------------------------------------------------------------ §3.5 launcher steps (ERRATUM_O31_2 E2)
# Feature files use the W25 npz form (w25.save / w25.load): ids, sha, phash, dhash, phash_m, dhash_m, sscd, unreadable.
EXPECT_N = {"pool": 3767, "ktvic_test": 558, "uit_test": 231, "karpathy_test": 5000, "tier3": 4224}
LISTS = {  # set -> (tracked id list, its sha256, column of the image sha256 or None)
    "ktvic_test": ("data/lb/sets/ktvic_test.tsv", "456243c0cfc82b0c3cc4ad52c694e11b4d9702f3ca14cd8103c3a82cd74a90eb", 2),
    "uit_test": ("data/lb/sets/uitviic_test.tsv", "dbadc28724d7a07b599325cd996084934d76e6c4c6a885e64e8de333d6a6665b", 2),
    "karpathy_test": ("manuscript/prereg/2026-10-27_c_en/cen_coco_test.tsv",
                      "67555b281d87b01a0f742214da552be0f7c4f4977f543db98a9acd2901787eb1", None),
}
KV_FEATS_SHA = "9783f7a669aa1b0a6df8e8a78aa3586fb7009f376d8151442ac3acc7da580a7e"  # C-EN feats_coco_kval (w25.CEN_FEATS)


def set_rows(name: str, train_items: list[dict] | None = None) -> list[tuple[str, str, str | None]]:
    """[(id, file, image sha256 or None)] of a set. pool: KTVIC train file names minus the 2 byte twins (id = file
    name, the key of the records and of P1's --exclude); the others: their tracked, sha-pinned id lists."""
    from .stage1 import N_TRAIN, TWINS

    if name == "pool":
        names = [i["file_name"] for i in train_items or []]
        if len(set(names)) != N_TRAIN or not set(TWINS) <= set(names):
            raise SystemExit(f"FAULT KTVIC train lists {len(set(names))} images, not {N_TRAIN} with both twins")
        rows = [(n, n, None) for n in sorted(set(names) - set(TWINS))]
    else:
        root = repo()
        rel, want, col = LISTS[name]
        if hashlib.sha256((root / rel).read_bytes()).hexdigest() != want:
            raise SystemExit(f"FAULT {rel} differs from its pin")
        lines = [x.split("\t") for x in (root / rel).read_text(encoding="utf-8").splitlines() if x and x[0] != "#"]
        rows = [(x[0], x[1], x[col] if col is not None else None) for x in lines]
    if len(rows) != EXPECT_N[name] or len({r[0] for r in rows}) != len(rows):
        raise SystemExit(f"FAULT {name}: {len(rows)} rows, expected {EXPECT_N[name]} distinct")
    return rows


def feats(name: str, rows: list, images: Path, sscd: Path, out: Path, workers: int = 4, features=None) -> dict:
    """Descriptors of one set (on the PI's PC): build_memory.features unchanged, SSCD weights at the W25 pin; every
    image readable and, where the list pins it, byte-equal to its sha. Writes `out` (W25 npz) and returns counts."""
    repo()
    import w25

    if out.exists() or out.suffix != ".npz":
        raise SystemExit(f"REFUSED: {out} exists or is not an .npz name")
    paths = [images / f for _i, f, _s in rows]
    f = (features or w25.bm().features)(paths, w25.ok_sscd(sscd), workers=workers)
    if f["unreadable"]:
        raise SystemExit(f"FAULT {name}: {len(f['unreadable'])} image(s) cannot be hashed")
    if any(s is not None and s != got for (_i, _f, s), got in zip(rows, f["sha"])):
        raise SystemExit(f"FAULT {name}: an image differs from the sha in its id list")
    tmp = out.with_name(f".{out.name}")
    w25.save(tmp, [i for i, _f, _s in rows], f, set=name, n=len(rows))
    tmp.rename(out)
    return {"set": name, "n": len(rows)}


def kv_feats(kval: Path, out: Path, kv_ids=None) -> dict:
    """KV-4,224 descriptors (laptop; E1 O-H8 keeps every tier-3-derived byte off the PC): the rows of C-EN's
    feats_coco_kval.npz (W25 memory of CC-153, pin 9783f7a6) whose ids are KV-4,224 rebuilt as in M0 (m0.kv4224:
    scripts/grl/id_counts.py counts() on its pinned inputs, ids pin 86d93863). No KV image is read."""
    repo()
    import w25

    kv = w25.load(kval, KV_FEATS_SHA)
    if kv_ids is None:
        import m0

        kv_ids = m0.kv4224
    want = {str(i) for i in kv_ids()}
    keep = [k for k, i in enumerate(kv["ids"]) if str(i) in want]
    if len(want) != EXPECT_N["tier3"] or len(keep) != len(want) or kv["unreadable"]:
        raise SystemExit(f"FAULT KV-4,224: {len(keep)} of {len(want)} ids found in the KV features")
    sub = {"sha": [kv["sha"][k] for k in keep], **{x: kv[x][keep] for x in ("phash", "dhash", "phash_m", "dhash_m", "sscd")},
           "unreadable": []}
    w25.save(out, [str(kv["ids"][k]) for k in keep], sub, set="tier3", n=len(keep))
    return {"set": "tier3", "n": len(keep)}


def run_pass(feat_files: dict, out: Path, expect: dict | None = None) -> dict:
    """The registered §3.5 pass (laptop): all five sets required; writes w4_pass.json (removed ids, counts, input
    shas) and exclude_p1.txt = the 2 byte twins plus every part (a) hit (P1's --exclude, ERRATUM_O31_2 E2)."""
    repo()
    import w25

    from .stage1 import TWINS

    expect = expect or EXPECT_N
    if set(feat_files) != set(EXPECT_N):
        raise SystemExit(f"REFUSED the pass needs exactly the sets {sorted(EXPECT_N)}")
    if not all(Path(p).is_file() for p in feat_files.values()):
        raise SystemExit("REFUSED a feature file is missing")
    fs, shas = {}, {}
    for k, p in feat_files.items():
        f = w25.load(p)
        if len(f["ids"]) != expect[k] or len(set(f["ids"])) != len(f["ids"]) or f["unreadable"]:
            raise SystemExit(f"FAULT {k}: {len(f['ids'])} rows, expected {expect[k]} distinct readable")
        fs[k] = {**f, "ids": [str(i) for i in f["ids"]]}
        shas[k] = hashlib.sha256(Path(p).read_bytes()).hexdigest()
    res = w4_pass(fs)
    if res["skipped"]:
        raise SystemExit(f"FAULT comparisons skipped: {res['skipped']}")
    out.mkdir(parents=True, exist_ok=True)
    excl = sorted(set(TWINS) | set(res["removed"]["pool"]))
    (out / "exclude_p1.txt").write_text("".join(f"{n}\n" for n in excl), encoding="utf-8")
    rec = {**res, "inputs_sha256": shas, "n_exclude_p1": len(excl),
           "exclude_p1_sha256": hashlib.sha256((out / "exclude_p1.txt").read_bytes()).hexdigest(),
           "note": "tier3 = KV-4,224 (E2); its part (b) removals apply only in prereg §3.4 branch 1"}
    (out / "w4_pass.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    return rec
