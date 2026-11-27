"""W4 overlap rule (prereg §3.5): exact sha + the committed W25 near-duplicate rule (CC-153), on descriptors only.

Rule = scripts/w25/w25.py rule() with build_memory.near, both unchanged (sha d6d12780, e771b92d):
excluded = byte-identical OR (min(pHash, dHash) <= 10 using x's mirrored hashes AND SSCD >= 0.5) OR SSCD > 0.75.
`near` mirrors only the x side, so x is always the set that loses images:
(a) x = training pool vs KTVIC test, UIT-ViIC test, Karpathy test, tier 3 -> hits leave the pool;
(b) x = Karpathy test and x = tier 3, each vs UIT-ViIC test -> hits leave that scoring set.
Feature dict per set: ids (list), sha (list), phash, dhash, phash_m, dhash_m (uint64), sscd (float32, L2-normalised).
"""
from __future__ import annotations

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
