#!/usr/bin/env python3
"""G-RL Gate 1 dev scorer (UIT-ViIC val 924, Vietnamese, CPU). Rule: manuscript/prereg/2026-10-27_grl_pilot/
PILOT_RULE.md §6. Writes numbers only; refuses to overwrite (one look).

    python3 scripts/grl/score_dev.py --selftest                                    CPU, synthetic systems
    python3 scripts/grl/score_dev.py --dir D --out SCORES.json                     D holds <sys>-val924-detailed.preds.json
                                                                                   for sys in base sftref rft grl
Gold: gold_instances.json (COCO-2014 instance classes, the reward's gold). Primary matcher v2; v1 beside it.
P = sum tp / sum mentions, R = sum tp / sum |gold| (micro, x100), F1 = 2PR/(P+R). Matched count (Paper A's matched
prefix, scripts/c_stage1/score.py cm): per image both captions keep their first k = min(count_X, count_Y) classes in
order of first mention. Paired image bootstrap, B = 2000, numpy default_rng(0), one resample shared by every contrast.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent), str(HERE.parents[1])]
import common as K  # noqa: E402
import reward as RW  # noqa: E402
from rl_reward import syllables  # noqa: E402

SYSTEMS = ("base", "sftref", "rft", "grl")
CONTRASTS = (("grl", "sftref"), ("grl", "rft"), ("grl", "base"), ("rft", "sftref"), ("sftref", "base"), ("rft", "base"))


def caption_row(c: str, g: set[str]) -> dict:
    from rescap.chair import objects_in

    v2, rest = RW.ordered(c, "v2")
    v1 = RW.ordered(c, "v1")[0]
    hedged = RW.unasserted(c)[1]
    return {"v2": v2, "v1": v1, "g": g, "syl": len(syllables(c)), "vi": RW.vietnamese_only(c),
            "hedge": bool(hedged and RW.ordered(hedged, "v2")[0]), "noncoco": len(objects_in(rest)),
            "list": RW.list_style(c)}


def prf(tp, m, g) -> np.ndarray:
    """tp, m, g: (draws, n) or (n,) per-image counts -> (P, R, F1) x100 over the last axis."""
    T, M, G = (np.asarray(x, float).sum(-1) for x in (tp, m, g))
    p, r = T / np.maximum(M, 1), T / np.maximum(G, 1)
    return 100 * np.stack([p, r, np.where(p + r > 0, 2 * p * r / np.maximum(p + r, 1e-12), 0.0)])


def counts(rows: list[dict], ver: str, k=None):
    m = [r[ver] if k is None else r[ver][:kk] for r, kk in zip(rows, k if k is not None else [None] * len(rows))]
    return (np.array([len(set(x) & r["g"]) for x, r in zip(m, rows)]), np.array([len(x) for x in m]),
            np.array([len(r["g"]) for r in rows]))


def system_summary(rows: list[dict]) -> dict:
    out = {}
    for ver in ("v2", "v1"):
        p, r, f = prf(*counts(rows, ver))
        out[ver] = {"P": float(p), "R": float(r), "F1": float(f),
                    "classes_per_caption": float(np.mean([len(x[ver]) for x in rows]))}
    out |= {"vi_only_pct": 100 * float(np.mean([r["vi"] for r in rows])),
            "syllables_mean": float(np.mean([r["syl"] for r in rows])),
            "hedged_caption_pct": 100 * float(np.mean([r["hedge"] for r in rows])),
            "list_style_pct": 100 * float(np.mean([r["list"] for r in rows])),
            "noncoco_nouns_per_caption": float(np.mean([r["noncoco"] for r in rows])),
            "v1_eq_v2_pct": 100 * float(np.mean([set(r["v1"]) == set(r["v2"]) for r in rows]))}
    return out


def contrast(x: list[dict], y: list[dict], idx: np.ndarray) -> dict:
    """x - y: raw (P, R, F1) under v2 and v1, and matched-count F1 under v2; point and 95% percentile CI."""
    def d(cx, cy):
        pt = prf(*cx) - prf(*cy)
        bs = prf(*(a[idx] for a in cx)) - prf(*(a[idx] for a in cy))
        lo, hi = np.percentile(bs, [2.5, 97.5], axis=1)
        return {k: [round(float(pt[j]), 4), round(float(lo[j]), 4), round(float(hi[j]), 4)]
                for j, k in enumerate(("P", "R", "F1"))}
    k = [min(len(a["v2"]), len(b["v2"])) for a, b in zip(x, y)]
    return {"v2": d(counts(x, "v2"), counts(y, "v2")), "v1": d(counts(x, "v1"), counts(y, "v1")),
            "matched_v2": d(counts(x, "v2", k), counts(y, "v2", k)), "matched_k_mean": float(np.mean(k))}


def score(preds: dict[str, dict[str, str]], gold: dict[int, set[str]], ids: list[int]) -> dict:
    for s, p in preds.items():
        if sorted(map(int, p)) != ids:
            raise SystemExit(f"{s}: its predictions are not exactly the {len(ids)} val images")
    rows = {s: [caption_row(p[str(i)], gold[i]) for i in ids] for s, p in preds.items()}
    idx = np.random.default_rng(K.GATE1["boot_seed"]).integers(0, len(ids), (K.GATE1["boot_b"], len(ids)))
    return {"schema": "vsps.grl.dev_scores.v1", "label": "PILOT / DEV (UIT-ViIC val 924; not confirmatory)",
            "n_images": len(ids), "matcher_primary": "v2", "gold": "COCO-2014 instances (gold_instances.json)",
            "systems": {s: system_summary(r) for s, r in rows.items()},
            "contrasts": {f"{a}-{b}": contrast(rows[a], rows[b], idx) for a, b in CONTRASTS if a in rows and b in rows}}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir")
    ap.add_argument("--out")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return 0
    out = Path(a.out)
    if out.exists():
        raise SystemExit(f"REFUSED: {out} exists (one look)")
    preds = {s: json.loads((Path(a.dir) / f"{s}-val924-detailed.preds.json").read_text(encoding="utf-8"))
             for s in SYSTEMS}
    res = score(preds, K.gold(), K.ids("val924"))
    out.write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps({s: v["v2"] for s, v in res["systems"].items()}))
    return 0


def selftest() -> None:
    gold = {i: {"person", "sports ball"} for i in range(60)}
    ids = list(range(60))
    full, one, wrong = "một người cầm quả bóng", "một người", "một người và con chó"
    preds = {"base": {str(i): wrong for i in ids}, "sftref": {str(i): one for i in ids},
             "rft": {str(i): one for i in ids}, "grl": {str(i): full for i in ids}}
    res = score(preds, gold, ids)
    s = res["systems"]
    assert s["grl"]["v2"]["F1"] == 100.0 and abs(s["sftref"]["v2"]["F1"] - 100 * 2 / 3) < 1e-9, s
    assert abs(s["base"]["v2"]["P"] - 50.0) < 1e-9 and s["base"]["v2"]["classes_per_caption"] == 2
    c = res["contrasts"]["grl-sftref"]
    assert c["v2"]["F1"][1] > 0 and abs(c["v2"]["F1"][0] - 100 / 3) < 1e-3, c
    # matched prefix: k = 1, both name "person" first -> equal F1 at matched count
    assert c["matched_v2"]["F1"] == [0.0, 0.0, 0.0] and c["matched_k_mean"] == 1.0, c
    assert res["contrasts"]["rft-sftref"]["v2"]["F1"] == [0.0, 0.0, 0.0]
    h = score({"base": {str(i): "một người, có vẻ là con chó" for i in ids}}, gold, ids)["systems"]["base"]
    assert h["hedged_caption_pct"] == 100.0, h
    try:
        score({"base": {"0": one}}, gold, ids)
    except SystemExit as e:
        assert "not exactly" in str(e), e
    else:
        raise AssertionError("a partial prediction file was scored")
    print("score_dev selftest ok")


if __name__ == "__main__":
    sys.exit(main())
