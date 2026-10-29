#!/usr/bin/env python3
"""Paper B, D0 dev gate (CC-158 W4): the decided B-1 dev300 adapters scored against the KTVIC panel (own) and the
OpenViIC-train panel (other) of the same 187 images. Rule: manuscript/prereg/2026-10-29_b_d0/RULE.md.

    python3 scripts/b_d0/d0.py --selftest        synthetic data only
    NCS_DATA=... NCS_DATASET=ktvic python3 scripts/b_d0/d0.py run      CPU, once

No caption text is printed or written by this file.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts"), str(ROOT / "scripts/b1_scaling")]

RULE = ROOT / "manuscript/prereg/2026-10-29_b_d0/RULE.md"
RULE_SHA256 = "72345e1c3cd1c467920ad03b9d2f2ca0209e395d7725d64005424e5bc57d8bee"
LOG = ROOT / ".session_backup/2026-10-13/decisions/LOG.md"
OUT = ROOT / ".session_backup/2026-10-29/b_d0/decide.json"
M4 = ROOT / ".session_backup/machines/M4/root/outputs/b1_scaling"
KIT_B = ROOT / ".session_backup/2026-10-21/zenodo_build/code/scripts/kit_b"
PINS = {"data/splits/ktvic_dev300.txt": "cee024f8bb76846b1623e36d1861caccc4d13874db87544213a1f18f3de6898c",
        "data/ktvic_openviic_refs.json": "4eb02cc43841bae4f844ee74d4c01b58e677dc8d6abafdd998c9f5b5706f725d",
        "data/datasets/openviic/uit-openviic-annotation-train.json":
            "d757520e76b8490df6c7275c2beb8b3ecef0342635a436bea8c3cfd07eb49df0",
        "data/datasets/ktvic/train_data.json": "72ee9b57c350fb5f215e1f04701c515a51e5e415240e51a77c8ce00ce6316a0f",
        f"{M4.relative_to(ROOT)}/SHA256SUMS": "7855927583f38b557857da632db904aad10ffc88fa51044bbdd338fae2ab58a1",
        f"{M4.relative_to(ROOT)}/ledger.json": "4afa3f44fa2da731f6fa6b8e02182b40328340f455443e334db36a4f1faab394",
        f"{M4.relative_to(ROOT)}/decide.json": "b44a76fe6456e6c037fc5578b701f949e73515973b5f68263236e65d65addaf9"}
IDS_SHA256, N_IDS = "ba5069452fc8cf8cf644b057ba36775f6d2d001054a510adf7d1c23074e3bbb3", 187
SEEDS, LEVELS = (42, 43, 44), {"L1": 216, "L2": 433, "L3": 867, "L4": 1734, "L5": 3469}
K_MAX, SESOI, B, BOOT_SEED, DEV_TWIN = 5, 1.0, 2000, 0, "2004"
X = np.log2(list(LEVELS.values()))


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run_name(s: int, lv: str) -> str:
    return f"b1_s{s}_{lv}"


def select(i: str, pool: list[str], k: int) -> list[str]:
    """RULE §3: the k captions with the smallest sha256("{id}|{caption}")."""
    return sorted(pool, key=lambda c: hashlib.sha256(f"{i}|{c}".encode()).hexdigest())[:k]


def dedup(caps) -> list[str]:
    out = []
    for c in (c.strip() for c in caps):
        if c and c not in out:
            out.append(c)
    return out


# ------------------------------------------------------------------------------------------------ statistics
def fe_slope(x: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """b1.fe_slope: common slope with seed fixed effects, Y (S, L, ...)."""
    xc = x - x.mean()
    return np.tensordot(xc, Y - Y.mean(1, keepdims=True), axes=([0], [1])).mean(0) / (xc @ xc)


def ci(d: np.ndarray) -> list[float]:
    return [float(v) for v in np.percentile(d, [2.5, 97.5])]


def grid(C: dict[str, np.ndarray], idx: np.ndarray, keep: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Point means (S, L) over kept images and bootstrap means (S, L, B) over the kept draws of idx."""
    M = keep[idx]
    Y = np.array([[C[run_name(s, lv)][keep].mean() for lv in LEVELS] for s in SEEDS])
    D = np.array([[(C[run_name(s, lv)][idx] * M).sum(1) / M.sum(1) for lv in LEVELS] for s in SEEDS])
    return Y, D


def gate(g: float, g_lo: float, rel_lo: float) -> tuple[str, str]:
    """RULE §5, its clauses in written order."""
    if g < SESOI:
        return "NO_GO", "gap_below_sesoi"
    if g_lo <= 0:
        return "NO_GO", "gap_ci_includes_0"
    if rel_lo <= 0:
        return "NO_GO", "scale_only"
    return "GO", "all_three_hold"


def slopes(CK: dict, CO: dict, idx: np.ndarray, keep: np.ndarray) -> dict:
    (YK, DK), (YO, DO) = grid(CK, idx, keep), grid(CO, idx, keep)
    bK, bO = float(fe_slope(X, YK)), float(fe_slope(X, YO))
    gd = fe_slope(X, DK) - fe_slope(X, DO)
    rK, rO = 100 * fe_slope(X, np.log(YK)), 100 * fe_slope(X, np.log(YO))
    rd = 100 * (fe_slope(X, np.log(DK)) - fe_slope(X, np.log(DO)))
    xc = X - X.mean()
    per_seed = lambda Y: ((Y - Y.mean(1, keepdims=True)) @ xc / (xc @ xc)).tolist()  # noqa: E731
    g, g_lo, rel_lo = bK - bO, ci(gd)[0], ci(rd)[0]
    v, why = gate(g, g_lo, rel_lo)
    return {"n_images": int(keep.sum()), "b_K": bK, "b_K_ci95": ci(fe_slope(X, DK)), "b_O": bO,
            "b_O_ci95": ci(fe_slope(X, DO)), "g": g, "g_ci95": ci(gd), "ratio_bO_bK": bO / bK,
            "ratio_ci95": ci(fe_slope(X, DO) / fe_slope(X, DK)), "r_K_pct": float(rK), "r_O_pct": float(rO),
            "g_rel_pct": float(rK - rO), "g_rel_ci95": ci(rd), "per_seed_b_K": per_seed(YK),
            "per_seed_b_O": per_seed(YO), "mean_K_L1_L5": [float(YK[:, 0].mean()), float(YK[:, 4].mean())],
            "mean_O_L1_L5": [float(YO[:, 0].mean()), float(YO[:, 4].mean())], "rule_applied": {"verdict": v,
                                                                                                 "reason": why}}


def f1_slopes(rows: dict, idx: np.ndarray, keep: np.ndarray, scores) -> dict:
    """rows[gold][run] = per-image object_prf rows; corpus F1 per point and per draw, fixed-effects slopes."""
    out, kept = {}, np.flatnonzero(keep)
    draws = [r[keep[r]] for r in idx]
    for gold, rr in rows.items():
        Y = np.array([[scores([rr[run_name(s, lv)][j] for j in kept])["F1"] for lv in LEVELS] for s in SEEDS])
        D = np.array([[[scores([rr[run_name(s, lv)][j] for j in d])["F1"] for d in draws] for lv in LEVELS]
                      for s in SEEDS])
        out[gold] = {"F1": {run_name(s, lv): float(Y[a, b]) for a, s in enumerate(SEEDS)
                            for b, lv in enumerate(LEVELS)}, "b": float(fe_slope(X, Y)), "ci95": ci(fe_slope(X, D)),
                     "sd_seed_L5": float(Y[:, 4].std(ddof=1)), "_draws": fe_slope(X, D)}
    if "K" in out and "O" in out:
        out["gap_K_minus_O"] = {"b": out["K"]["b"] - out["O"]["b"], "ci95": ci(out["K"]["_draws"] - out["O"]["_draws"])}
    for v in out.values():
        v.pop("_draws", None)
    return out


# ------------------------------------------------------------------------------------------------ data
def check_rule() -> None:
    if sha(RULE) != RULE_SHA256:
        raise SystemExit("RULE.md changed since it was logged")
    if RULE_SHA256 not in LOG.read_text(encoding="utf-8"):
        raise SystemExit("RULE.md sha256 is not in LOG.md: log the rule before scoring")
    for f, h in PINS.items():
        if sha(ROOT / f) != h:
            raise SystemExit(f"{f}: sha256 differs from the pin")


def panels(dev_refs: dict[str, list[str]]) -> tuple[list[str], dict, dict, dict]:
    pairs = json.loads((ROOT / "data/ktvic_openviic_refs.json").read_text(encoding="utf-8"))["_pairs"]["train"]
    ov = json.loads((ROOT / "data/datasets/openviic/uit-openviic-annotation-train.json").read_text(encoding="utf-8"))
    dev = [x.strip() for x in (ROOT / "data/splits/ktvic_dev300.txt").read_text().split() if x.strip()]
    ids = sorted((i for i in dev if any(c[1] == "train" for c in pairs.get(i, []))), key=int)
    if len(ids) != N_IDS or hashlib.sha256(("\n".join(ids) + "\n").encode()).hexdigest() != IDS_SHA256:
        raise SystemExit("the 187-image set does not reproduce")
    o_pool = {i: dedup(c for f, s, *_ in pairs[i] if s == "train" for c in ov[f]["captions"]) for i in ids}
    k_pool = {i: dedup(dev_refs[i]) for i in ids}
    k = {i: min(K_MAX, len(o_pool[i]), len(k_pool[i])) for i in ids}
    return ids, {i: select(i, k_pool[i], k[i]) for i in ids}, {i: select(i, o_pool[i], k[i]) for i in ids}, \
        {i: (len(k_pool[i]), len(o_pool[i])) for i in ids}


def load_preds() -> dict[str, dict[str, str]]:
    sums = {ln.split()[1].lstrip("./"): ln.split()[0] for ln in (M4 / "SHA256SUMS").read_text().splitlines() if ln}
    import b1
    out = {}
    for s in SEEDS:
        for lv in LEVELS:
            res = M4 / f"{run_name(s, lv)}-dev300-short.json"
            for p in (res, res.with_suffix(".preds.json")):
                if sums.get(p.name) != sha(p):
                    raise SystemExit(f"{p.name}: not the decided B-1 output")
            out[run_name(s, lv)] = b1.dev_preds(res)
    return out


def in_order(cider, hyps: dict[str, str], ids: list[str]) -> np.ndarray:
    """Cider.per_image returns values in sorted(str) id order; re-index them to ids' order."""
    got = dict(zip(sorted(ids), cider.per_image({i: hyps[i] for i in ids})))
    return np.array([got[i] for i in ids], float)


def cmd_run() -> None:
    if OUT.exists():
        raise SystemExit(f"{OUT} exists; D0 runs once")
    check_rule()
    import b1
    import scaling_probe as SP
    import score_coco_probe as sc
    from evaluate import KTVIC
    from object_prf import image_counts, scores
    from rescap.chair import objects_in

    if sha(KTVIC / "train_data.json") != PINS["data/datasets/ktvic/train_data.json"]:
        raise SystemExit("SP.dev_refs would read an unpinned train_data.json")
    E4, PA, kit_sha = b1.load_kit(KIT_B)
    preds, dev_refs = load_preds(), SP.dev_refs()
    led = json.loads((M4 / "ledger.json").read_text(encoding="utf-8"))["rows"]

    # RULE §7.4 reproduction gate (a decided number, not a look)
    rep = b1.score_rows(preds, dev_refs, E4, PA)
    worst = max(abs(np.mean(rep[r]["cider_s"]) - np.mean(led[r]["cider_s"])) for r in preds)
    if worst > 1e-3:
        raise SystemExit(f"reproduction gate failed: max |diff| {worst:.5f}")

    ids, K, O, sizes = panels(dev_refs)
    texts = sorted({p[i] for p in preds.values() for i in ids} | {c for P in (K, O) for i in ids for c in P[i]})
    seg = dict(zip(texts, (t.lower() for t in E4.rdr(texts))))
    hyp = {r: {i: " ".join(PA.strip_trailing_punct_tokens(seg[p[i]].split())) for i in ids} for r, p in preds.items()}
    cK, cO = (E4.Cider({i: [seg[c] for c in P[i]] for i in ids}) for P in (K, O))
    CK = {r: in_order(cK, h, ids) for r, h in hyp.items()}
    CO = {r: in_order(cO, h, ids) for r, h in hyp.items()}

    idx = np.random.default_rng(BOOT_SEED).integers(0, len(ids), (B, len(ids)))
    allk = np.ones(len(ids), bool)
    primary = slopes(CK, CO, idx, allk)

    terms = sc.load_vi_terms()
    match = {"v2": lambda t: set(sc.vi_objects(t, terms, "v2")), "b1_exact": lambda t: set(objects_in(t))}
    objects = {}
    for name, fn in match.items():
        gold = {"K": {i: set().union(*(fn(c) for c in K[i])) for i in ids},
                "O": {i: set().union(*(fn(c) for c in O[i])) for i in ids}}
        gold["union"] = {i: gold["K"][i] | gold["O"][i] for i in ids}
        rows = {gk: {r: [image_counts(fn(p[i]), g[i], lambda o: {o}) for i in ids] for r, p in preds.items()}
                for gk, g in gold.items()}
        objects[name] = f1_slopes(rows, idx, allk, scores)

    v, why = primary["rule_applied"]["verdict"], primary["rule_applied"]["reason"]
    u = objects["v2"]["union"]
    fixes = {"P1_SESOI": max(1.0, 0.5 * primary["g"]) if v == "GO" else None,
             "P2_margin_F1": max(2.0, abs(u["b"]), 2 * u["sd_seed_L5"]),
             "formulas": "P1 = max(1.0, 0.5 g) on GO; P2 = max(2.0, |b_F1 union v2|, 2 SD_seed F1 union v2 at L5)"}

    no2004 = np.array([i != DEV_TWIN for i in ids])
    k5 = np.array([min(sizes[i]) >= K_MAX for i in ids])
    # exact-k=5 row: on these images k_i == 5 already; df rebuilt from their references only, other images masked
    sub = [i for i, ok in zip(ids, k5) if ok]
    c5 = {n: E4.Cider({i: [seg[c] for c in P[i]] for i in sub}) for n, P in (("K", K), ("O", O))}
    pos = [ids.index(i) for i in sub]

    def full(c, h):
        v = np.zeros(len(ids))
        v[pos] = in_order(c, h, sub)
        return v
    CK5 = {r: full(c5["K"], h) for r, h in hyp.items()}
    CO5 = {r: full(c5["O"], h) for r, h in hyp.items()}
    four = lambda t: {tuple(t.split()[j:j + 4]) for j in range(max(0, len(t.split()) - 3))}  # noqa: E731
    jac = [max((len(four(seg[o]) & four(seg[k])) / max(1, len(four(seg[o]) | four(seg[k]))) for k in K[i]))
           for i in ids for o in O[i]]
    from rl_reward import syllables
    desc = {"minus_2004": slopes(CK, CO, idx, no2004), "exact_k5_images": slopes(CK5, CO5, idx, k5),
            "panel": {"mean_k": float(np.mean([len(K[i]) for i in ids])),
                      "k_counts": {str(k): int(sum(len(K[i]) == k for i in ids)) for k in range(1, 6)},
                      "mean_ref_syllables_K": float(np.mean([len(syllables(c)) for i in ids for c in K[i]])),
                      "mean_ref_syllables_O": float(np.mean([len(syllables(c)) for i in ids for c in O[i]])),
                      "share_O_ref_equal_to_a_K_ref": float(np.mean([seg[o] in {seg[k] for k in K[i]}
                                                                     for i in ids for o in O[i]])),
                      "mean_best_4gram_jaccard_O_to_K": float(np.mean(jac))}}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "label": "D0 DEV GATE (KTVIC dev300 / OpenViIC-train panel, 187 images; development data, not a test result)",
        "rule": {"path": str(RULE.relative_to(ROOT)), "sha256": RULE_SHA256}, "verdict": v, "reason": why,
        "primary": primary, "objects": objects, "fixes_for_full_study": fixes, "descriptive": desc,
        "reproduction_gate": {"max_abs_diff_vs_ledger": float(worst), "tolerance": 1e-3, "passed": True},
        "bootstrap": {"B": B, "rng": f"numpy default_rng({BOOT_SEED})", "n_images": len(ids), "paired": True},
        "provenance": {"ncs_data": os.environ.get("NCS_DATA", ""), "jar_sha256": sha(E4.VNC / "VnCoreNLP-1.2.jar"),
                       "kit_b": kit_sha, "pins": PINS, "ids_sha256": IDS_SHA256, "script_sha256": sha(Path(__file__))},
    }, indent=1) + "\n", encoding="utf-8")
    print(f"D0 {v} ({why}): g = {primary['g']:+.2f} {primary['g_ci95']}, g_rel = {primary['g_rel_pct']:+.2f}% "
          f"{primary['g_rel_ci95']}")


# ------------------------------------------------------------------------------------------------ selftest
def selftest() -> None:
    assert select("7", ["a", "b", "c"], 2) == select("7", ["c", "b", "a"], 2)  # order-free
    assert dedup([" a", "a", "", "b "]) == ["a", "b"]
    n = 187
    rng = np.random.default_rng(1)
    idx = np.random.default_rng(BOOT_SEED).integers(0, n, (300, n))
    keep = np.ones(n, bool)

    def make(slope_k: float, slope_o: float, base_o: float = 60.0) -> tuple[dict, dict]:
        noise = rng.normal(0, 3, n)
        CK = {run_name(s, lv): 100 + slope_k * x + noise + s % 3 for s in SEEDS for lv, x in zip(LEVELS, X)}
        CO = {run_name(s, lv): base_o + slope_o * x + noise + s % 3 for s in SEEDS for lv, x in zip(LEVELS, X)}
        return CK, CO

    r = slopes(*make(10.0, 3.0), idx, keep)
    assert abs(r["b_K"] - 10) < 0.01 and abs(r["b_O"] - 3) < 0.01 and abs(r["g"] - 7) < 0.02
    assert r["rule_applied"]["verdict"] == "GO"
    r = slopes(*make(10.0, 9.8, 100.0), idx, keep)
    assert r["rule_applied"] == {"verdict": "NO_GO", "reason": "gap_below_sesoi"}
    # absolute gap from scale alone: O is K at 60% of the level (same relative slope) -> scale_only
    CK, _ = make(10.0, 0.0)
    CO = {k: 0.6 * v for k, v in CK.items()}
    assert slopes(CK, CO, idx, keep)["rule_applied"]["reason"] == "scale_only"
    assert gate(2.0, -0.1, 1.0) == ("NO_GO", "gap_ci_includes_0")
    # masked row drops an image from points and draws
    m = keep.copy(); m[0] = False
    assert slopes(*make(10.0, 3.0), idx, m)["n_images"] == n - 1
    # object F1 slope: F1 rises with level under gold K, flat under gold O
    from object_prf import scores
    gold = lambda j: {"x", "y"}  # noqa: E731
    rows = {"K": {}, "O": {}}
    for s in SEEDS:
        for j, lv in enumerate(LEVELS):
            hitK = [{"x", "y"} if (i % 5) < j + 1 else {"z"} for i in range(n)]
            rows["K"][run_name(s, lv)] = [(len(h & gold(i)), len(h), 0, len(h & gold(i)) / 2, 0, 0)
                                          for i, h in enumerate(hitK)]
            rows["O"][run_name(s, lv)] = [(1, 1, 0, 0.5, 0, 0)] * n
    f = f1_slopes(rows, idx[:50], keep, scores)
    assert f["K"]["b"] > 5 and abs(f["O"]["b"]) < 1e-9 and f["gap_K_minus_O"]["b"] > 5
    print("b_d0 selftest ok")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", choices=["run"])
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
    elif a.cmd == "run":
        cmd_run()
    else:
        ap.print_help()
