#!/usr/bin/env python3
"""Paper B, D0 masked re-read (CC-161 W6): POST HOC, DESCRIPTIVE, DEV. D0's forward slopes on masked draws of D0's
(2000, 187) matrix; D0's decide.json is never rewritten. Also the B-R1 design CI half-widths (W8).

    python3 scripts/b_r1/d0_reread.py --selftest
    NCS_DATA=... python3 scripts/b_r1/d0_reread.py run          laptop CPU, once, after its LOG spec line

Masks: (a) the dev ids of the 187 with a B-1 train near-twin (r1_lists.json); (b) 2004 alone (replaces D0's void
minus-2004 row, LOG l.701); (c) dev ids whose selected K reference exactly equals the first caption of a B-1 L5
training image; (d) a | c. Hold rule (logged before the run): mask (d) g < 1.0 or CI_lo(g) <= 0 -> B-R1 HELD.
No caption text is printed or written.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts"), str(ROOT / "scripts/b1_scaling"), str(ROOT / "scripts/b_d0")]

import d0  # noqa: E402  d0.py 0d87a953 (in_order fixed)

LISTS = ROOT / "manuscript/prereg/2026-10-29_b_r1/r1_lists.json"
LISTS_SHA256 = "571dfedf16bd39dfa4e94f6f0873c89241d7ffb61ef9a86c38ffa4a4e4db289c"
B1_LISTS = ROOT / "manuscript/prereg/2026-10-28_b1_scaling/b1_lists.json"
D0_DECIDE_SHA256 = "15dd925f5cba3159fec102bb5238108d9d109860e20bed50c800c6b1875580a1"
OUT = ROOT / ".session_backup/2026-10-29/b_d0_reread/reread.json"
LABEL = "POST HOC, DESCRIPTIVE, DEV (D0 masked re-read, CC-161 W6); D0's GO verdict is unchanged by it"
DESIGN = {"seeds": (42, 43), "levels": ("L1", "L3", "L4")}  # B-R1's x values, forward data (W8)
Z80 = (1.96 + 0.84) / 1.96  # 80% power, two-sided 5%: MDE = Z80 x CI half-width


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def first_captions(train_json: Path) -> dict[str, str]:
    """build_gold_sft.py's training caption: the first non-empty stripped caption of each image in file order."""
    out = {}
    for a in json.loads(train_json.read_text(encoding="utf-8"))["annotations"]:
        c = (a.get("caption") or "").strip()
        if c:
            out.setdefault(str(a["image_id"]), c)
    return out


def scored(preds: dict, ids: list[str], K: dict, O: dict, E4, PA, sigma: float = 6.0) -> dict:
    """D0's scorer: RDRSegmenter, lower-cased, trailing punctuation stripped, one Cider per panel (its selected refs),
    per-image values in ids' order. sigma = inf drops the length penalty (kit B P8 form)."""
    texts = sorted({p[i] for p in preds.values() for i in ids} | {c for P in (K, O) for i in ids for c in P[i]})
    seg = dict(zip(texts, (t.lower() for t in E4.rdr(texts))))
    hyp = {r: {i: " ".join(PA.strip_trailing_punct_tokens(seg[p[i]].split())) for i in ids} for r, p in preds.items()}
    out = {}
    for n, P in (("K", K), ("O", O)):
        c = E4.Cider({i: [seg[x] for x in P[i]] for i in ids}, sigma=sigma)
        out[n] = {r: d0.in_order(c, h, ids) for r, h in hyp.items()}
    return out


def fit(C: dict, seeds, levels, idx, keep, name) -> tuple[np.ndarray, np.ndarray]:
    """Point means (S, L) over kept images and bootstrap means (S, L, B) over the kept draws (d0.grid's rule)."""
    M = keep[idx]
    Y = np.array([[C[name(s, lv)][keep].mean() for lv in levels] for s in seeds])
    D = np.array([[(C[name(s, lv)][idx] * M).sum(1) / M.sum(1) for lv in levels] for s in seeds])
    return Y, D


def row(CK: dict, CO: dict, idx, keep) -> dict:
    """d0.slopes without its verdict field (a descriptive row never reads as a verdict)."""
    r = d0.slopes(CK, CO, idx, keep)
    r.pop("rule_applied")
    return r


def hold(r: dict) -> bool:
    """The pre-fixed consequence on mask (d)."""
    return r["g"] < d0.SESOI or r["g_ci95"][0] <= 0


def design_halfwidths(CK: dict, CO: dict, idx, keep) -> dict:
    """CI half-widths of b_K, b_O and g at B-R1's design (seeds 42/43 x L1/L3/L4) on D0's forward data."""
    x = np.log2([d0.LEVELS[lv] for lv in DESIGN["levels"]])
    (_, DK), (_, DO) = (fit(C, DESIGN["seeds"], DESIGN["levels"], idx, keep, d0.run_name) for C in (CK, CO))
    hw = {k: float(np.diff(d0.ci(v))[0] / 2) for k, v in
          (("b_K", d0.fe_slope(x, DK)), ("b_O", d0.fe_slope(x, DO)), ("g", d0.fe_slope(x, DK) - d0.fe_slope(x, DO)))}
    return {"ci_halfwidth": hw, "mde80": {k: Z80 * v for k, v in hw.items()}}


def cmd_run() -> None:
    if OUT.exists():
        raise SystemExit(f"{OUT} exists; the re-read runs once")
    d0.check_rule()
    if sha(d0.OUT) != D0_DECIDE_SHA256 or sha(LISTS) != LISTS_SHA256:
        raise SystemExit("D0 decide.json or r1_lists.json differs from its pin")
    import b1
    import scaling_probe as SP
    from evaluate import KTVIC

    if sha(KTVIC / "train_data.json") != d0.PINS["data/datasets/ktvic/train_data.json"]:
        raise SystemExit("SP.dev_refs would read an unpinned train_data.json")

    E4, PA, kit_sha = b1.load_kit(d0.KIT_B)
    preds, (ids, K, O, _) = d0.load_preds(), d0.panels(SP.dev_refs())
    C = scored(preds, ids, K, O, E4, PA)
    idx = np.random.default_rng(d0.BOOT_SEED).integers(0, len(ids), (d0.B, len(ids)))
    twins = set(json.loads(LISTS.read_text(encoding="utf-8"))["dev_ids_with_a_train_twin"])
    l5 = set(json.loads(B1_LISTS.read_text(encoding="utf-8"))["levels"]["L5"]["ids"])
    train_caps = {c for i, c in first_captions(ROOT / "data/datasets/ktvic/train_data.json").items() if i in l5}
    template = {i for i in ids if any(c.strip() in train_caps for c in K[i])}
    masks = {"a_dev_twins": twins, "b_2004": {d0.DEV_TWIN}, "c_exact_caption": template,
             "d_union": twins | template}
    rows, dropped = {}, {}
    for name, drop in masks.items():
        keep = np.array([i not in drop for i in ids])
        rows[name], dropped[name] = row(C["K"], C["O"], idx, keep), sorted(set(ids) & drop, key=int)
    allk = np.ones(len(ids), bool)
    held = hold(rows["d_union"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "label": LABEL, "b_r1": "HELD" if held else "PROCEED",
        "hold_rule": "mask d_union: g < 1.0 or CI_lo(g) <= 0 -> B-R1 HELD (CC-161 W6)",
        "rows": rows, "dropped_ids": dropped, "n_dropped": {k: len(v) for k, v in dropped.items()},
        "full_recomputed": row(C["K"], C["O"], idx, allk),
        "note": "CIs recomputed with in_order; they differ numerically from D0's decided CIs (points equal)",
        "b_r1_design": design_halfwidths(C["K"], C["O"], idx, allk),
        "provenance": {"script_sha256": sha(Path(__file__)), "d0_py_sha256": sha(ROOT / "scripts/b_d0/d0.py"),
                       "d0_decide_sha256": D0_DECIDE_SHA256, "lists_sha256": LISTS_SHA256, "kit_b": kit_sha},
    }, indent=1) + "\n", encoding="utf-8")
    print(f"re-read done: B-R1 {'HELD' if held else 'PROCEED'}")


def selftest() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as t:
        p = Path(t) / "tr.json"
        p.write_text(json.dumps({"annotations": [{"image_id": 1, "caption": " "}, {"image_id": 1, "caption": "a "},
                                                 {"image_id": 1, "caption": "b"}, {"image_id": 2, "caption": "c"}]}))
        assert first_captions(p) == {"1": "a", "2": "c"}
    assert hold({"g": 0.9, "g_ci95": [0.1, 2]}) and hold({"g": 3, "g_ci95": [0.0, 6]})
    assert not hold({"g": 3, "g_ci95": [0.5, 6]})
    n, rng = 187, np.random.default_rng(1)
    idx = np.random.default_rng(0).integers(0, n, (300, n))
    noise = rng.normal(0, 3, n)
    CK = {d0.run_name(s, lv): 100 + 10 * x + noise for s in d0.SEEDS for lv, x in zip(d0.LEVELS, d0.X)}
    CO = {d0.run_name(s, lv): 50 + 1 * x + noise for s in d0.SEEDS for lv, x in zip(d0.LEVELS, d0.X)}
    keep = np.ones(n, bool)
    keep[:8] = False
    r = row(CK, CO, idx, keep)
    assert "rule_applied" not in r and r["n_images"] == n - 8 and abs(r["g"] - 9) < 1e-9
    hw = design_halfwidths(CK, CO, idx, np.ones(n, bool))
    assert hw["ci_halfwidth"]["g"] < 1e-9 and hw["mde80"]["b_K"] >= hw["ci_halfwidth"]["b_K"]
    print("d0_reread selftest ok")


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
