#!/usr/bin/env python3
"""Paper B+D coordinator items 1-2 (manuscript/reviews/BD_RESPONSE_TO_REVIEWERS.md): POST HOC, DESCRIPTIVE, DEV.
No verdict; D0's and B-R1's decided outcomes and files are unchanged. Laptop CPU only.

    python3 scripts/paperB/bd_coordinator_items.py --selftest      synthetic data only
    NCS_DATA=.session_backup/machines/n2/ncs-data python3 scripts/paperB/bd_coordinator_items.py run

Inputs (each sha-checked before use):
- manuscript/journal_draft_B/figs/fig_values_B.json (b7635d15): per-adapter mean CIDEr-D on the 187 D0 images.
- .session_backup/2026-10-29/b_d0/decide.json (15dd925f) and .session_backup/2026-10-29/b_r1/decide.json (a6627047).
- The decided dev300 predictions: 15 forward B-1 adapters (.session_backup/machines/M4/root/outputs/b1_scaling) and
  6 reverse B-R1 adapters (.session_backup/machines/M2/root/outputs/b_r1), each checked against its SHA256SUMS.
- The two panels from d0.panels (D0 RULE pins checked by d0.check_rule), kit B and the protocol-card VnCoreNLP jar.
Output: data/results/paperB/bd_coordinator_items.json and its .sha256. No caption text is printed or written.

Item 1: per-seed own/other slopes and gaps in both directions, and a two-stage (seed, then image) bootstrap.
Item 2: forward and reverse gaps under BLEU-4 (corpus), ROUGE-L, chrF (sentence level, best reference, mean over
images) and CIDEr-D with document frequencies pooled over both panels (one document per image = its K and O
references), on D0's scorer text (RDRSegmenter, lower-cased, trailing punctuation stripped from hypotheses).
Also checked: the decided D0 run's id order (string-sorted per-image values read as int-sorted, LOG l.701) applied to
these per-image scores must reproduce D0's decided CIs, i.e. d0.py's text processing is the decided run's.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/results/paperB/bd_coordinator_items.json"
FIG_VALUES = ROOT / "manuscript/journal_draft_B/figs/fig_values_B.json"
PINS = {FIG_VALUES: "b7635d15a8e80b75c401807f6071b1b2d4f0196513fe22f3ec8096afe59d0076",
        ROOT / ".session_backup/2026-10-29/b_d0/decide.json":
            "15dd925f5cba3159fec102bb5238108d9d109860e20bed50c800c6b1875580a1",
        ROOT / ".session_backup/2026-10-29/b_r1/decide.json":
            "a6627047c590c8179d84bea2886d3ccf679876b4d737301d101651a541ff2c9e"}
LABEL = "POST HOC, DESCRIPTIVE, DEV (Paper B+D coordinator items 1-2); no verdict, decided outcomes unchanged"
TWO_STAGE_SEED = 1  # seed draws; image draws reuse D0's default_rng(0) index matrix
TOL = 1e-6


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def xc_of(x: np.ndarray) -> np.ndarray:
    return x - x.mean()


def per_seed(x: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """OLS slope per seed; Y (S, L, ...) -> (S, ...)."""
    xc = xc_of(x)
    return np.tensordot(Y - Y.mean(1, keepdims=True), xc, axes=([1], [0])) / (xc @ xc)


def ci(d: np.ndarray) -> list[float]:
    return [float(v) for v in np.percentile(d, [2.5, 97.5])]


# ------------------------------------------------------------------------------------------------ metrics
def chrf(hyp: str, refs: list[str], n: int = 6, beta: float = 2.0) -> float:
    """sacrebleu-style sentence chrF (whitespace and VnCoreNLP '_' removed; P and R averaged over orders 1..n, then
    F-beta), best reference; x100."""
    def grams(s: str, k: int) -> Counter:
        s = s.replace("_", "").replace(" ", "")
        return Counter(s[i:i + k] for i in range(len(s) - k + 1))

    best = 0.0
    for r in refs:
        P, R = [], []
        for k in range(1, n + 1):
            h, g = grams(hyp, k), grams(r, k)
            if not h or not g:
                continue
            m = sum((h & g).values())
            P.append(m / sum(h.values()))
            R.append(m / sum(g.values()))
        if not P:
            continue
        p, rr = np.mean(P), np.mean(R)
        f = 0.0 if p + rr == 0 else (1 + beta ** 2) * p * rr / (beta ** 2 * p + rr)
        best = max(best, float(f))
    return 100 * best


def bleu_stats(hyp: str, refs: list[str], ngrams) -> np.ndarray:
    """kit B bleu4's sufficient statistics of one image: correct[4], guess[4], hyp len, closest ref len."""
    h = hyp.split()
    maxc: dict = {}
    for r in refs:
        for g, c in ngrams(r).items():
            maxc[g] = max(maxc.get(g, 0), c)
    correct = [0] * 4
    for g, c in ngrams(hyp).items():
        correct[len(g) - 1] += min(maxc.get(g, 0), c)
    lens = [len(r.split()) for r in refs]
    return np.array(correct + [max(0, len(h) - k) for k in range(4)] + [len(h), min((abs(x - len(h)), x)
                                                                                    for x in lens)[1]], float)


def bleu_from(S: np.ndarray) -> np.ndarray:
    """Corpus BLEU-4 (x100) from summed statistics (..., 10), kit B's smoothing constants."""
    tiny, small = 1e-15, 1e-9
    b = np.prod((S[..., 0:4] + tiny) / (S[..., 4:8] + small), axis=-1) ** 0.25
    ratio = (S[..., 8] + tiny) / (S[..., 9] + small)
    return 100 * np.where(ratio < 1, b * np.exp(1 - 1 / ratio), b)


# ------------------------------------------------------------------------------------------------ slopes
def level_draws(v: np.ndarray, W: np.ndarray, bleu: bool) -> tuple[float, np.ndarray]:
    """Point and bootstrap values of one adapter on one panel; W (B, n) = image counts of each draw."""
    if bleu:
        return float(bleu_from(v.sum(0))), bleu_from(W @ v)
    return float(v.mean()), W @ v / W.shape[1]


def grid(V: dict, seeds, levels, name, W, bleu) -> tuple[np.ndarray, np.ndarray]:
    pts = [[level_draws(V[name(s, lv)], W, bleu) for lv in levels] for s in seeds]
    return np.array([[p[0] for p in r] for r in pts]), np.array([[p[1] for p in r] for r in pts])


def direction(Vown: dict, Voth: dict, seeds, levels, name, x, W, bleu=False, seed_draw=None) -> dict:
    """Own/other slopes (seed fixed effects), gap, image-bootstrap CIs, per-seed points; with seed_draw (B, S) also
    the two-stage CIs (seeds resampled with replacement, then the images of the same draw)."""
    (Yo, Do), (Yt, Dt) = grid(Vown, seeds, levels, name, W, bleu), grid(Voth, seeds, levels, name, W, bleu)
    po, pt = per_seed(x, Yo), per_seed(x, Yt)
    do, dt = per_seed(x, Do), per_seed(x, Dt)  # (S, B)
    out = {"b_own": float(po.mean()), "b_own_ci95": ci(do.mean(0)), "b_other": float(pt.mean()),
           "b_other_ci95": ci(dt.mean(0)), "gap": float(po.mean() - pt.mean()), "gap_ci95": ci(do.mean(0) - dt.mean(0)),
           "per_seed": {str(s): {"b_own": float(a), "b_other": float(b), "gap": float(a - b)}
                        for s, a, b in zip(seeds, po, pt)},
           "mean_own_by_level": Yo.mean(0).tolist(), "mean_other_by_level": Yt.mean(0).tolist()}
    if seed_draw is not None:
        cols = np.arange(do.shape[1])
        two = lambda d: d[seed_draw, cols[:, None]].mean(1)  # noqa: E731  (B,)
        out["two_stage"] = {"b_own_ci95": ci(two(do)), "b_other_ci95": ci(two(dt)), "gap_ci95": ci(two(do) - two(dt))}
    return out


# ------------------------------------------------------------------------------------------------ run
def cmd_run() -> None:
    if OUT.exists():
        raise SystemExit(f"{OUT} exists")
    for p, h in PINS.items():
        if sha(p) != h:
            raise SystemExit(f"{p.relative_to(ROOT)} differs from its pin")
    sys.path.insert(0, str(ROOT / "scripts/b_r1"))
    import matched as MT  # B-R1's paths and loaders, via b_r1 -> d0, d0_reread
    R, d0, RR = MT.R, MT.d0, MT.RR
    d0.check_rule()
    sums = {ln.split()[1].lstrip("./"): ln.split()[0] for ln in (R.MIRROR / "SHA256SUMS").read_text().splitlines() if ln}
    rev = {}
    for s in R.SEEDS:
        for lv in R.LEVELS:
            res = R.MIRROR / f"{R.run_name(s, lv)}-dev300-short.json"
            for p in (res, res.with_suffix(".preds.json")):
                if sums.get(p.name) != sha(p):
                    raise SystemExit(f"{p.name}: not the B-R1 job output")
            rev[R.run_name(s, lv)] = R.b1.dev_preds(res)
    fwd = d0.load_preds()  # sha-checked against the B-1 mirror's SHA256SUMS
    E4, PA, kit_sha = R.b1.load_kit(d0.KIT_B)
    ids, K, O, _ = d0.panels(R.SP.dev_refs())
    preds = fwd | rev
    dec = json.loads(R.D0_DECIDE.read_text(encoding="utf-8"))
    br1 = json.loads(MT.BR1_DECIDE.read_text(encoding="utf-8"))
    figv = json.loads(FIG_VALUES.read_text(encoding="utf-8"))
    n = len(ids)
    idx = np.random.default_rng(d0.BOOT_SEED).integers(0, n, (d0.B, n))
    W = np.stack([np.bincount(r, minlength=n) for r in idx]).astype(float)
    gates = {}

    # ---- gate 1: per-panel-df CIDEr-D (sigma 6) reproduces fig_values means and the decided slopes
    C6 = RR.scored(preds, ids, K, O, E4, PA)
    worst = max(abs(C6[p][r].mean() - figv[d][r][p]) for d, runs in (("forward", fwd), ("reverse", rev))
                for r in runs for p in "KO")
    gates["fig_values_means_max_abs_diff"] = float(worst)
    F = direction(C6["K"], C6["O"], d0.SEEDS, d0.LEVELS, d0.run_name, d0.X, W)
    Rv = direction(C6["O"], C6["K"], R.SEEDS, R.LEVELS, R.run_name, R.X, W)
    want = [(F["b_own"], dec["primary"]["b_K"]), (F["b_other"], dec["primary"]["b_O"]), (F["gap"], dec["primary"]["g"]),
            (Rv["b_own"], br1["primary"]["b_O_own"]), (Rv["b_other"], br1["primary"]["b_K_other"]),
            (Rv["gap"], br1["primary"]["g_R"])]
    want += [(F["per_seed"][str(s)]["b_own"], v) for s, v in zip(d0.SEEDS, dec["primary"]["per_seed_b_K"])]
    want += [(F["per_seed"][str(s)]["b_other"], v) for s, v in zip(d0.SEEDS, dec["primary"]["per_seed_b_O"])]
    gates["decided_slopes_max_abs_diff"] = float(max(abs(a - b) for a, b in want))
    # B-R1's decided CIs used in_order with D0's index matrix: they must reproduce exactly
    gates["br1_ci_max_abs_diff"] = float(max(abs(a - b) for k, kk in (("b_own_ci95", "b_O_ci95"),
                                                                          ("b_other_ci95", "b_K_ci95"),
                                                                          ("gap_ci95", "g_R_ci95"))
                                             for a, b in zip(Rv[k], br1["primary"][kk])))
    if max(gates.values()) > TOL:
        raise SystemExit(f"gate failed: {gates}")

    # ---- d0.py version check: the decided run read string-sorted per-image values as int-sorted (LOG l.701)
    pos = {i: k for k, i in enumerate(ids)}
    perm = np.array([pos[i] for i in sorted(ids)])
    old = {p: {r: v[perm] for r, v in C6[p].items() if r in fwd} for p in "KO"}
    o = d0.slopes(old["K"], old["O"], idx, np.ones(n, bool))
    old_diff = max(abs(a - b) for k in ("b_K_ci95", "b_O_ci95", "g_ci95", "g_rel_ci95")
                   for a, b in zip(o[k], dec["primary"][k]))
    gates["decided_d0_ci_with_old_order_max_abs_diff"] = float(old_diff)
    if old_diff > TOL:
        raise SystemExit(f"the old-order check did not reproduce D0's decided CIs: {old_diff}")

    # ---- item 1: per-seed values and the two-stage bootstrap
    rng = np.random.default_rng(TWO_STAGE_SEED)
    sdF = rng.integers(0, len(d0.SEEDS), (d0.B, len(d0.SEEDS)))
    sdR = rng.integers(0, len(R.SEEDS), (d0.B, len(R.SEEDS)))
    item1 = {"forward": direction(C6["K"], C6["O"], d0.SEEDS, d0.LEVELS, d0.run_name, d0.X, W, seed_draw=sdF),
             "reverse": direction(C6["O"], C6["K"], R.SEEDS, R.LEVELS, R.run_name, R.X, W, seed_draw=sdR),
             "note": "own = the training captions' panel (forward K, reverse O). Two-stage: seeds drawn with "
                     "replacement (numpy default_rng(1)), images from D0's default_rng(0) matrix, same draw for own "
                     "and other. With two reverse seeds only three seed draws exist, so the reverse two-stage "
                     "interval is degenerate and is not interpreted."}

    # ---- item 2: metric-robustness rows
    texts = sorted({p[i] for p in preds.values() for i in ids} | {c for P in (K, O) for i in ids for c in P[i]})
    seg = dict(zip(texts, (t.lower() for t in E4.rdr(texts))))
    hyp = {r: {i: " ".join(PA.strip_trailing_punct_tokens(seg[p[i]].split())) for i in ids} for r, p in preds.items()}
    ref = {"K": {i: [seg[c] for c in K[i]] for i in ids}, "O": {i: [seg[c] for c in O[i]] for i in ids}}
    pooled_df = [ref["K"][i] + ref["O"][i] for i in ids]
    M = {"BLEU-4": {}, "ROUGE-L": {}, "chrF": {}, "CIDEr-D_pooled_df": {}}
    for p in "KO":
        cp = E4.Cider(ref[p], sigma=6.0, df_refs=pooled_df)  # df is order-free
        M["CIDEr-D_pooled_df"][p] = {r: d0.in_order(cp, h, ids) for r, h in hyp.items()}
        M["BLEU-4"][p] = {r: np.stack([bleu_stats(h[i], ref[p][i], E4.ngrams) for i in ids]) for r, h in hyp.items()}
        M["ROUGE-L"][p] = {r: np.array([E4.rouge_l({i: ref[p][i]}, {i: h[i]}) for i in ids]) for r, h in hyp.items()}
        M["chrF"][p] = {r: np.array([chrf(h[i], ref[p][i]) for i in ids]) for r, h in hyp.items()}
        for r, h in hyp.items():  # kit B's own corpus BLEU-4 and ROUGE-L equal the stats-based values
            gb = abs(bleu_from(M["BLEU-4"][p][r].sum(0)) - E4.bleu4(ref[p], h))
            gr = abs(M["ROUGE-L"][p][r].mean() - E4.rouge_l(ref[p], h))
            gates["kit_bleu_rouge_max_abs_diff"] = float(max(gates.get("kit_bleu_rouge_max_abs_diff", 0.0), gb, gr))
    if gates["kit_bleu_rouge_max_abs_diff"] > TOL:
        raise SystemExit(f"gate failed: {gates}")
    item2 = {}
    for m, V in M.items():
        b = m == "BLEU-4"
        item2[m] = {"forward": direction(V["K"], V["O"], d0.SEEDS, d0.LEVELS, d0.run_name, d0.X, W, b),
                    "reverse": direction(V["O"], V["K"], R.SEEDS, R.LEVELS, R.run_name, R.X, W, b)}
    item2["CIDEr-D_per_panel_df (decided scorer, for reference)"] = {"forward": F, "reverse": Rv}
    item2["note"] = ("BLEU-4 is corpus-level (kit B, closest reference length); ROUGE-L is kit B's per-image mean; "
                     "chrF is sentence chrF (char 1-6-grams, beta 2, best reference) averaged over images; pooled-df "
                     "CIDEr-D uses one df document per image holding both panels' selected references (log 187), "
                     "sigma 6. All on D0's scorer text. Image-bootstrap CIs on D0's index matrix (B = 2000), seed "
                     "fixed effects, own minus other.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "label": LABEL, "n_images": n, "gates": gates, "tolerance": TOL,
        "d0_version_check": "d0.py 89f102c2 (decided run) is not in git; the only logged change to 0d87a953 is the "
                            "in_order id mapping (LOG l.701). Applying the old mapping to these per-image scores "
                            "reproduces D0's decided b_K, b_O, g and g_rel CIs (gate above), so the text processing "
                            "of d0.py l.202-204 is the decided run's. New CIs use in_order, as B-R1's decided run did.",
        "item1_per_seed_and_two_stage": item1, "item2_metric_robustness": item2,
        "provenance": {"script_sha256": sha(Path(__file__)), "inputs": {str(p.relative_to(ROOT)): h
                                                                       for p, h in PINS.items()},
                       "kit_b": kit_sha, "jar_sha256": sha(E4.VNC / "VnCoreNLP-1.2.jar"),
                       "b1_mirror_sums": sha(d0.M4 / "SHA256SUMS"), "br1_mirror_sums": sha(R.MIRROR / "SHA256SUMS")},
    }, indent=1) + "\n", encoding="utf-8")
    (OUT.parent / (OUT.name + ".sha256")).write_text(f"{sha(OUT)}  {OUT.relative_to(ROOT)}\n")
    print(f"wrote {OUT.relative_to(ROOT)} {sha(OUT)[:8]}; gates {gates}")


def selftest() -> None:
    x = np.log2([216, 867, 1734])
    Y = np.array([1 + 2 * x, 5 + 3 * x])  # (S=2, L=3)
    assert np.allclose(per_seed(x, Y), [2, 3])
    assert abs(chrf("ab cd", ["ab cd"]) - 100) < 1e-9 and chrf("xy", ["ab"]) == 0.0
    assert chrf("a_b", ["ab"]) == chrf("ab", ["a b"]) == 100.0
    ng = lambda s: Counter(tuple(s.split()[j:j + k]) for k in range(1, 5) for j in range(len(s.split()) - k + 1))  # noqa
    S = bleu_stats("a b c d", ["a b c d"], ng)
    assert abs(bleu_from(S) - 100) < 1e-6 and bleu_from(bleu_stats("a b", ["a b c d"], ng)) < 1
    n, B = 50, 200
    rng = np.random.default_rng(3)
    idx = rng.integers(0, n, (B, n))
    W = np.stack([np.bincount(r, minlength=n) for r in idx]).astype(float)
    noise = rng.normal(0, 1, n)
    own = {f"s{s}_{k}": 10 + 4 * xi + s + noise for s in (1, 2) for k, xi in zip("abc", x)}
    oth = {f"s{s}_{k}": 10 + 1 * xi + noise for s in (1, 2) for k, xi in zip("abc", x)}
    r = direction(own, oth, (1, 2), "abc", lambda s, k: f"s{s}_{k}", x, W, seed_draw=rng.integers(0, 2, (B, 2)))
    assert abs(r["gap"] - 3) < 1e-9 and abs(r["per_seed"]["1"]["gap"] - 3) < 1e-9
    assert r["two_stage"]["gap_ci95"][0] <= 3 <= r["two_stage"]["gap_ci95"][1]
    print("bd_coordinator_items selftest ok")


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
