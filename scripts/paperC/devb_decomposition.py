#!/usr/bin/env python3
"""Paper C, stage-B (dev-B) decomposition of InternVL3's ret - rand contrast at its frozen tau = 0.10 and at
tau = -inf. POST HOC, dev data only (CP-116 Q4/W11); not a test look and not a registered result.

CPU only. Reads the stage-2 ledger L2 (numbers and image ids only) and decide_final.json, both pinned by sha256.
Registered bootstrap (stage-1 score.boot, unchanged): B = 2000, numpy default_rng(0), integers(0, n, (B, n)),
percentile 95% CI, the ledger's pinned image order. Asserts:
  - tau = 0.10 ret - rand equals decide_final ov_dev_b / xm_dev500 InternVL3 vs_rand exactly;
  - tau = -inf ret - rand equals the judge recompute of CC-103 l.34 at 3 decimals.

  python3 scripts/paperC/devb_decomposition.py            writes data/results/paperC/devb_decomposition.json
"""
import hashlib
import json
from pathlib import Path

import numpy as np

R = Path(__file__).resolve().parents[2]
L2 = R / ".session_backup/machines/M3/root/outputs/c_stage2/ledger.jsonl"
DF = R / ".session_backup/2026-10-22/c_stage2/final/decide_final.json"
OUT = R / "data/results/paperC/devb_decomposition.json"
PIN = {L2: "be716482c6f934e975bdbc58927cfc42a4c0ff589c9c5f95affd67c03eac0938",
       DF: "92a1f0e992cb974f0d2dfc59a765d1adbfa89338a6d7eed267edd583e2cd162b"}
SETS = {"ov_dev_b": ("c2_internvl3_8b_ov_dev_b-ret-k4-last-T2", "c2_internvl3_8b_ov_dev_b-rand-k4-T2", 925),
        "xm_dev500": ("c2_internvl3_8b_xm_dev500-ret-k4-last-T2", "c2_internvl3_8b_xm_dev500-rand-k4-T2", 500)}
DF_KEY = {"ov_dev_b": ("ov_dev_b", "gate"), "xm_dev500": ("xm_dev500", "detail")}
CC103 = {"ov_dev_b": (5.356, 3.527, 7.119), "xm_dev500": (1.541, -2.120, 5.250)}  # CC-103 l.34


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def boot(x: np.ndarray) -> dict:
    idx = np.random.default_rng(0).integers(0, len(x), (2000, len(x)))
    lo, hi = np.percentile(x[idx].mean(1), [2.5, 97.5])
    return {"d": float(x.mean()), "lo": float(lo), "hi": float(hi)}


def main() -> None:
    for p, h in PIN.items():
        assert sha(p) == h, f"{p.name} sha256 is not the pinned {h[:8]}"
    rows = [json.loads(line) for line in L2.read_text().splitlines()]
    df = json.loads(DF.read_text())

    def get(rid: str, tau: str) -> dict:
        hit = [r for r in rows if r["run_id"] == rid and r["tau"] == tau]
        assert len(hit) == 1, (rid, tau, len(hit))
        return hit[0]

    out = {"label": "POST HOC, DEV-B ONLY (CP-116 W11); no test data", "inputs": {"L2": PIN[L2], "decide_final": PIN[DF]},
           "bootstrap": "B=2000, default_rng(0), integers(0,n,(B,n)), percentile 95%", "sets": {}}
    for ds, (ret_id, rand_id, n) in SETS.items():
        c = {(arm, t): get(rid, t) for arm, rid in (("ret", ret_id), ("rand", rand_id)) for t in ("0.10", "-inf")}
        ids = {tuple(r["per_image"]["ids"]) for r in c.values()}
        assert len(ids) == 1 and len(next(iter(ids))) == n, ds
        x = {k: np.array(r["per_image"]["cider_s"], float) for k, r in c.items()}
        res = {
            "ret_minus_rand_tau010": boot(x["ret", "0.10"] - x["rand", "0.10"]),
            "ret_minus_rand_tauneginf": boot(x["ret", "-inf"] - x["rand", "-inf"]),
            "ret_tau010_minus_tauneginf": boot(x["ret", "0.10"] - x["ret", "-inf"]),
            "rand_tau010_minus_tauneginf": boot(x["rand", "0.10"] - x["rand", "-inf"]),
            "ledger_cider_s": {f"{a}@{t}": c[a, t]["cider_s"] for a, t in c},
            "n": n,
        }
        top, sub = DF_KEY[ds]
        ref = df[top][sub]["per_model"]["internvl3_8b"]["vs_rand"]
        got = res["ret_minus_rand_tau010"]
        assert all(got[k] == ref[k] for k in ("d", "lo", "hi")), (ds, got, ref)
        neg = res["ret_minus_rand_tauneginf"]
        assert tuple(round(neg[k], 3) for k in ("d", "lo", "hi")) == CC103[ds], (ds, neg)
        out["sets"][ds] = res
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1) + "\n")
    print("asserts ok; wrote", OUT.relative_to(R), sha(OUT))


if __name__ == "__main__":
    main()
