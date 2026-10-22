#!/usr/bin/env python3
"""Single-writer exchangeability audit of a 5-reference caption set (Paper B, Section 3.2).

Statistics per split (object sets from the v2 matcher, rescap.chair.objects_in):
1) adjacent-doubleton share: of the object classes named by exactly two of an image's five references, the share
   named by adjacent slots (i, i+1); null under exchangeable slots 2/K = 0.40; binomial z; 1,000-draw image
   bootstrap 95% CI (seed 0);
2) Jaccard similarity of the two references' object sets by slot lag; lag-1 minus mean of lags 2-4, with CI;
3) per-slot mention counts and leave-one-out precision, and the {1,3} vs {1,2} two-reference gold comparison.
Aggregates only: no caption text is stored or printed.

    NCS_DATA=/path/to/ncs-data python scripts/kit_b/exchangeability_audit.py --out exch.json
    python scripts/kit_b/exchangeability_audit.py --selftest

Reads $NCS_DATA/datasets/ktvic/{test,train}_data.json and, if present, the dev300 image list
$NCS_DATA/splits/ktvic_dev300.txt (scripts/ktvic_dev_split.py regenerates it). --extra NAME=PATH adds any
COCO-format caption file with five references per image.
The functions load_coco_json_sets and audit_k5 are copied unchanged from the authors' audit script
c3_n2_exchangeability_all_datasets.py (sha256 e2bb5de6ac95c81c247156ae8006ca8deca9e1f23fa6e02e5b1cac76302cf17e).
This is NOT scripts/caption_exchangeability.py, a different, registered statistic (per-image adjacent vs
non-adjacent pair overlap).
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np

CODE = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(CODE), str(CODE / "scripts")]
DATA = Path(os.environ.get("NCS_DATA", Path.home() / "ncs-data"))
DS = DATA / "datasets"

from rescap.chair import objects_in  # noqa: E402

B_BOOT = 1000


def load_coco_json_sets(path: Path, extract_fn, k_target: int = 5, subset_ids: set[str] | None = None) -> tuple[list[list[set]], list[list[set]], dict]:
    """Load COCO-format or OpenViIC-format annotations into ordered per-image object sets."""
    d = json.loads(path.read_text(encoding="utf-8"))
    per_id: dict[str, list[tuple[int, str]]] = defaultdict(list)
    if isinstance(d, dict) and "annotations" not in d:
        # OpenViIC format: {image_name: {"captions": [...]}}
        for iid, v in d.items():
            if subset_ids is not None and str(iid) not in subset_ids:
                continue
            caps = v.get("captions", []) if isinstance(v, dict) else (v if isinstance(v, list) else [])
            for j, c in enumerate(caps):
                if c:
                    per_id[str(iid)].append((j, c))
        del d
    else:
        anns = d["annotations"] if isinstance(d, dict) and "annotations" in d else d
        for idx, a in enumerate(anns):
            if not isinstance(a, dict):
                continue
            cap = a.get("caption")
            if not cap:
                continue
            iid = str(a.get("image_id", a.get("id", idx)))
            if subset_ids is not None and iid not in subset_ids:
                continue
            sort_key = a.get("id", idx)
            try:
                sort_key = int(sort_key)
            except (ValueError, TypeError):
                sort_key = idx
            per_id[iid].append((sort_key, cap))
        del d, anns

    lengths = Counter(len(v) for v in per_id.values())
    exact_k = [[extract_fn(c) for _, c in sorted(v, key=lambda x: x[0])] for v in per_id.values() if len(v) == k_target]
    first_k = [[extract_fn(c) for _, c in sorted(v, key=lambda x: x[0])[:k_target]] for v in per_id.values() if len(v) >= k_target]
    meta = {
        "total_images": len(per_id),
        "refs_per_image_hist": {str(k): int(v) for k, v in sorted(lengths.items())},
        f"images_exact_{k_target}": len(exact_k),
        f"images_ge_{k_target}": len(first_k),
    }
    return exact_k, first_k, meta


def audit_k5(name: str, per_image: list[list[set]], seed: int = 0) -> dict:
    """Compute all 3 N2 exchangeability statistics + L2 D3 predictions on a K=5 dataset."""
    n = len(per_image)
    if n == 0:
        return {"images": 0}
    K = 5
    lags = [1, 2, 3, 4]
    null_adj = 2.0 / K  # 0.400

    # Per-image arrays:
    # DL: (n, 4) doubleton counts by lag 1..4
    # JS, JN: (n, 4) Jaccard sum and count by lag 1..4
    # JMAT_S, JMAT_N: (5, 5) pair Jaccard matrix
    # Qk: (n, 5) frequency counts Q1..Q5
    DL = np.zeros((n, 4), dtype=float)
    JS = np.zeros((n, 4), dtype=float)
    JN = np.zeros((n, 4), dtype=float)
    JMAT_S = np.zeros((5, 5), dtype=float)
    JMAT_N = np.zeros((5, 5), dtype=float)
    Qk = np.zeros((n, 5), dtype=float)
    slot_m = np.zeros((n, 5), dtype=float)
    slot_tp_loo = np.zeros((n, 5), dtype=float)
    g12_len = np.zeros(n, dtype=float)
    g13_len = np.zeros(n, dtype=float)
    tp45_vs_12 = np.zeros(n, dtype=float)
    tp45_vs_13 = np.zeros(n, dtype=float)
    m45 = np.zeros(n, dtype=float)

    for idx, sets in enumerate(per_image):
        u_all = set().union(*sets)
        for o in u_all:
            slots = [r for r in range(5) if o in sets[r]]
            k_freq = len(slots)
            Qk[idx, k_freq - 1] += 1.0
            if k_freq == 2:
                DL[idx, slots[1] - slots[0] - 1] += 1.0
        for a, b in combinations(range(5), 2):
            u = sets[a] | sets[b]
            if u:
                jval = len(sets[a] & sets[b]) / len(u)
                JS[idx, b - a - 1] += jval
                JN[idx, b - a - 1] += 1.0
                JMAT_S[a, b] += jval
                JMAT_S[b, a] += jval
                JMAT_N[a, b] += 1.0
                JMAT_N[b, a] += 1.0
        for r in range(5):
            JMAT_S[r, r] += 1.0 if sets[r] else 0.0
            JMAT_N[r, r] += 1.0 if sets[r] else 0.0
            slot_m[idx, r] = len(sets[r])
            others = set().union(*(sets[q] for q in range(5) if q != r))
            slot_tp_loo[idx, r] = len(sets[r] & others)

        g12 = sets[0] | sets[1]
        g13 = sets[0] | sets[2]
        g12_len[idx] = len(g12)
        g13_len[idx] = len(g13)
        tp45_vs_12[idx] = len(sets[3] & g12) + len(sets[4] & g12)
        tp45_vs_13[idx] = len(sets[3] & g13) + len(sets[4] & g13)
        m45[idx] = len(sets[3]) + len(sets[4])

    def agg(w: np.ndarray):
        dl = w @ DL
        js = w @ JS
        jn = w @ JN
        tot_d = float(dl.sum())
        share = dl / max(tot_d, 1.0)
        jac = js / np.maximum(jn, 1.0)
        jac_diff = float(jac[0] - jac[1:].mean())
        # Non-empty Gbar for {1,2} and {1,3}
        m12 = g12_len > 0
        m13 = g13_len > 0
        gbar12 = float((w[m12] @ g12_len[m12]) / max(w[m12].sum(), 1.0))
        gbar13 = float((w[m13] @ g13_len[m13]) / max(w[m13].sum(), 1.0))
        gbar12_all = float((w @ g12_len) / w.sum())
        gbar13_all = float((w @ g13_len) / w.sum())
        m45_sum = float(w @ m45)
        p45_12 = 100.0 * float(w @ tp45_vs_12) / max(m45_sum, 1.0)
        p45_13 = 100.0 * float(w @ tp45_vs_13) / max(m45_sum, 1.0)
        # Chao2 Q0 all-pairs vs non-adjacent doubleton density
        qk = w @ Qk
        q1, q2 = float(qk[0]), float(qk[1])
        # Non-adjacent doubletons = lags 2,3,4 (6 of 10 pairs -> scale by 10/6)
        q2_nonadj_scaled = float(dl[1:].sum()) * (10.0 / 6.0)
        chao2_q0_all = ((K - 1.0) / K) * (q1 ** 2) / (2.0 * max(q2, 1.0))
        chao2_q0_nonadj = ((K - 1.0) / K) * (q1 ** 2) / (2.0 * max(q2_nonadj_scaled, 1.0))
        return (
            tot_d,
            share,
            jac,
            jac_diff,
            gbar12,
            gbar13,
            gbar12_all,
            gbar13_all,
            p45_12,
            p45_13,
            chao2_q0_all / w.sum(),
            chao2_q0_nonadj / w.sum(),
        )

    pt = agg(np.ones(n))
    tot_d, share, jac, jac_diff, gbar12, gbar13, gbar12_all, gbar13_all, p45_12, p45_13, q0_all, q0_nonadj = pt

    rng = np.random.default_rng(seed)
    W = rng.multinomial(n, np.full(n, 1.0 / n), size=B_BOOT).astype(float)
    bs = [agg(w) for w in W]

    ci = lambda arr, digits=4: [
        round(float(np.percentile(arr, 2.5)), digits),
        round(float(np.percentile(arr, 97.5)), digits),
    ]

    adj_sh = float(share[0])
    z_binom = (adj_sh - null_adj) / math.sqrt(null_adj * (1.0 - null_adj) / max(tot_d, 1.0))
    jmat = np.round(JMAT_S / np.maximum(JMAT_N, 1.0), 4)
    slot_m_mean = (slot_m.sum(axis=0) / n).tolist()
    slot_p_loo = (100.0 * slot_tp_loo.sum(axis=0) / np.maximum(slot_m.sum(axis=0), 1.0)).tolist()
    slot_p_grad = max(slot_p_loo) - min(slot_p_loo)
    slot_p_12_minus_345 = float(np.mean(slot_p_loo[:2]) - np.mean(slot_p_loo[2:]))
    q0_rel_diff_pct = 100.0 * abs(q0_nonadj - q0_all) / max(q0_all, 1e-9)

    return {
        "images": n,
        "K": K,
        "total_doubletons": int(round(tot_d)),
        "doubletons_per_img": round(tot_d / n, 4),
        # Stat 1: Adjacent-doubleton share
        "adjacent_share": round(adj_sh, 4),
        "adjacent_share_null": null_adj,
        "adjacent_share_z_vs_null": round(z_binom, 2),
        "adjacent_share_ci95": ci([b[1][0] for b in bs], 4),
        "lag_share": {str(d): round(float(share[k]), 4) for k, d in enumerate(lags)},
        # Stat 2: Jaccard matrix and lag decay
        "jaccard_by_lag": {str(d): round(float(jac[k]), 4) for k, d in enumerate(lags)},
        "jac_lag1_minus_mean_lag2to4": round(jac_diff, 4),
        "jac_diff_ci95": ci([b[3] for b in bs], 4),
        "jaccard_5x5": jmat.tolist(),
        # Stat 3: Per-slot gradient & {1,3} vs {1,2}
        "slot_mentions_per_img": [round(x, 3) for x in slot_m_mean],
        "slot_loo_precision_pct": [round(x, 2) for x in slot_p_loo],
        "slot_precision_range_pp": round(slot_p_grad, 2),
        "slot_precision_12_minus_345_pp": round(slot_p_12_minus_345, 2),
        "pair_13_vs_12": {
            "Gbar_12_nonempty": round(gbar12, 3),
            "Gbar_13_nonempty": round(gbar13, 3),
            "delta_Gbar_nonempty": round(gbar13 - gbar12, 3),
            "delta_Gbar_ci95": ci([b[5] - b[4] for b in bs], 3),
            "Gbar_12_all_img": round(gbar12_all, 3),
            "Gbar_13_all_img": round(gbar13_all, 3),
            "slots45_P_vs_12_pct": round(p45_12, 2),
            "slots45_P_vs_13_pct": round(p45_13, 2),
            "delta_slots45_P_pp": round(p45_13 - p45_12, 2),
            "delta_slots45_P_ci95": ci([b[9] - b[8] for b in bs], 2),
        },
        # Chao2 Q0 comparison (L2 D3 prediction a)
        "chao2_q0_per_img": {
            "all_pairs_q0": round(q0_all, 3),
            "nonadj_pairs_q0": round(q0_nonadj, 3),
            "rel_diff_pct": round(q0_rel_diff_pct, 2),
            "ratio_nonadj_over_all": round(q0_nonadj / max(q0_all, 1e-9), 3),
        },
    }


def selftest() -> None:
    """Synthetic sets: a chain (neighbours share) gives adjacent share 1; slots far apart give 0."""
    chain = [[{"a"}, {"a"}, {"b"}, {"b"}, {"c"}]] * 40
    far = [[{"a"}, {"b"}, {"a"}, {"c"}, {"b"}]] * 40
    r1, r2 = audit_k5("chain", chain), audit_k5("far", far)
    assert r1["adjacent_share"] == 1.0 and r1["total_doubletons"] == 80, r1
    assert r2["adjacent_share"] == 0.0 and r2["jac_lag1_minus_mean_lag2to4"] < 0, r2
    print("selftest ok")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path, help="output JSON (aggregates only)")
    ap.add_argument("--extra", action="append", default=[], metavar="NAME=PATH")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    vi_lex_fn = lambda c: set(objects_in(c))  # noqa: E731
    dev = DATA / "splits/ktvic_dev300.txt"
    jobs = [("ktvic_test_objects_in", DS / "ktvic/test_data.json", None),
            ("ktvic_train_objects_in", DS / "ktvic/train_data.json", None)]
    if dev.exists():
        jobs.append(("ktvic_dev300_objects_in", DS / "ktvic/train_data.json", set(dev.read_text("utf-8").split())))
    jobs += [(n, Path(p), None) for n, p in (e.split("=", 1) for e in a.extra)]
    meta_out, datasets_out = {}, {}
    for name, path, sub_ids in jobs:
        ex5, _, meta = load_coco_json_sets(path, vi_lex_fn, 5, sub_ids)
        meta_out[name] = meta
        datasets_out[name] = audit_k5(name, ex5, seed=0)
    out = {"dataset_metadata": meta_out, "k5_exchangeability_audit": datasets_out}
    if a.out:
        a.out.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
    for k, v in datasets_out.items():
        print(f"{k:28s} n={v['images']:5d} adjacent_share={v['adjacent_share']:.4f} {v['adjacent_share_ci95']} "
              f"jac_lag1-lag2to4={v['jac_lag1_minus_mean_lag2to4']:+.4f}")


if __name__ == "__main__":
    main()
