#!/usr/bin/env python3
"""K2 Gate 0/0b dev pilot (CC-119 ruling 4, W1-W8, W19-W21): the target ceiling of gold-edited self-distillation on
UIT-ViIC val 924. Rule: manuscript/prereg/2026-10-27_grl_pilot/K2_GATE0_RULE.md. A ceiling only, never a result.

    python3 scripts/grl/k2_gate0.py --selftest                                         CPU, synthetic rows
    python3 scripts/grl/k2_gate0.py manifest --out PROBE.tsv                           M3 CPU: 40 UT-2402 probe rows
    python3 scripts/grl/k2_gate0.py reg --dataset probe|val --n-new N --manifest TSV --out REG.json
    python3 scripts/grl/k2_gate0.py freeze --probe PREDS --probe-log LOG --out FREEZE.json   CPU: max_new_tokens + cap
    python3 scripts/grl/k2_gate0.py score --preds PREDS --freeze FREEZE --mem-log L --out GATE0.json   CPU

Decoding is scripts/lb/decode_hf_vlm.py, unchanged, driven by a registration this script writes from the B-N1
registration's Qwen3-VL-8B block (snapshot pins, venv, batch 4, processor kwargs, bf16, sdpa) and the detailed prompt.
Editor (pinned, W5): units are maximal runs ending at . , ; : ! ? or a newline; a unit is deleted if it names a
COCO-80 class (matcher v1) absent from the image's gold, or fails the language check (CJK or out-of-script
characters). A cap-hit caption first loses its last unit unless that ends in . ! ? (W3, both rows).
Scoring (W20, W21): matcher v2; gold = COCO-2014 instance classes (gold_instances.json, the G-RL gold); a class named
only in a negated or hedged unit is a hallucination and never a true positive (grl/reward.py semantics).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent), str(HERE.parents[1])]
import common as K  # noqa: E402
import reward as RW  # noqa: E402
from rl_reward import syllables  # noqa: E402

BN1 = "manuscript/prereg/2026-10-19_b_n1_vi_leaderboard.json"
BN1_SHA = "9ff02dc259258de1add426abd02131f2122e3476a81f9a076066ed6d74906134"
G = {  # frozen now (CC-119 W1); never moved after Gate 0
    "sesoi_chair_i": 3.0, "margin_recall": 2.0, "stop_a_recall_drop": 1.0, "stop_b_chair_drop": 5.0,
    "stop_c_words": 0.90, "unasserted_share_max": 0.5, "ceiling_hours": 5.0, "cap_factor": 1.2,  # CC-124 W2
    "probe_images": 40, "probe_n_new": 1024, "n_new_ladder": (256, 384, 512, 768, 1024), "cut_share_max": 0.10,
    "boot_b": 2000, "boot_seed": 0, "load_hours": 0.1,
    "p1_gap_min": 6.0, "p1_hw_max": 3.0,  # Ken K14 P1 (registered secondary): 2 x SESOI, half-width < SESOI
}
UNIT_RE = re.compile(r"[^.,;:!?\n]+[.,;:!?\n]*|[.,;:!?\n]+")
CLOSED_RE = re.compile(r"[.!?…]\s*$")


# ------------------------------------------------------------------------------------------------ editor
def units(c: str) -> list[str]:
    return UNIT_RE.findall(c)


def untruncate(c: str, hit_max: bool) -> str:
    """W3: a cap-hit caption loses its last unit unless that unit ends in . ! ? (an unfinished clause)."""
    u = units(c)
    return "".join(u[:-1] if hit_max and u and not CLOSED_RE.search(u[-1]) else u).strip()


def language_ok(u: str) -> bool:
    from clean_supervision import CJK_RE, OUT_OF_SCRIPT_RE

    return not CJK_RE.search(u) and not OUT_OF_SCRIPT_RE.search(u)


LEX_V2_ONLY = re.compile(r"\b((bóng|ghi) bàn|bàn thắng)\b", re.I)  # v1 "dining table" hits that LEX_V2 rewrites away


def lex_v2_artefact(u: str, gold: set[str]) -> bool:
    """W9 diagnostic: a deleted unit whose only gold-absent v1 class is a LEX_V2-rewritten dining-table hit."""
    absent = set(RW.ordered(u, "v1")[0]) - gold
    return absent == {"dining table"} and bool(LEX_V2_ONLY.search(u)) and "dining table" not in RW.ordered(u, "v2")[0]


def edit(c: str, gold: set[str]) -> tuple[str, list[str]]:
    """(edited caption, deleted units)."""
    keep, gone = [], []
    for u in units(c):
        (keep if language_ok(u) and set(RW.ordered(u, "v1")[0]) <= gold else gone).append(u)
    out = "".join(keep).strip()
    return (out[:-1] + "." if out and out[-1] in ",;:" else out), gone


# ------------------------------------------------------------------------------------------------ scoring
def row(c: str, gold: set[str], gold_u: set[str]) -> dict:
    """Per-caption counts. A = asserted v2 classes, U = classes named only in negated or hedged units."""
    said, hedged = RW.unasserted(c)
    a = set(RW.ordered(said, "v2")[0])
    u = set(RW.ordered(hedged, "v2")[0]) - a
    m = set(RW.ordered(c, "v2")[0])
    return {"tp": len(a & gold), "hal": len((a - gold) | u), "men": len(a | u), "g": len(gold),
            "hal_ex": len(a - gold), "men_ex": len(a),  # unasserted mentions excluded (W20 diagnostic)
            "hal_plain": len(m - gold), "men_plain": len(m),  # negation-blind matcher (as score_coco_probe)
            "hal_union": len((a - gold_u) | u), "men_union": len(a | u),  # instances ∪ reference classes (W21 diag.)
            "v1_eq_v2": set(RW.ordered(c, "v1")[0]) == m, "words": len(syllables(c)), "vi": RW.vietnamese_only(c),
            "ord": [x for x in RW.ordered(said, "v2")[0]]}  # asserted classes in order of first mention (P1 matched F1)


def rates(rows: list[dict], idx=None) -> dict:
    """CHAIR_i = sum hal / sum men x100 (pooled), R = sum tp / sum g x100; idx: (B, n) bootstrap draws."""
    def s(k):
        x = np.array([r[k] for r in rows], float)
        return x.sum() if idx is None else x[idx].sum(1)
    div = lambda a, b: 100 * a / np.maximum(b, 1)  # noqa: E731
    return {"CHAIR_i": div(s("hal"), s("men")), "R": div(s("tp"), s("g")), "CHAIR_i_unasserted_excluded":
            div(s("hal_ex"), s("men_ex")), "CHAIR_i_negation_blind": div(s("hal_plain"), s("men_plain")),
            "CHAIR_i_union_gold": div(s("hal_union"), s("men_union"))}


# ------------------------------------------------------------------------------------------------ P1 frontier (Ken K14)
def cut(c: str, k: int) -> str:
    """The first k clauses of a caption, with the pinned editor's splitter (W5)."""
    return "".join(units(c)[:k]).strip()


def interp(pts: list[tuple[float, float]], r_star: float) -> tuple[float, bool]:
    """(frontier CHAIR_i at recall r_star, clamped?) on the piecewise-linear curve through (R_k, C_k), k = 1, 2, ...
    R_k is non-decreasing in k. Bracket = the first k with R_k >= r_star and the point before it; equal recalls take
    the first k that reaches r_star. Outside [R_1, R_max] the end point is used and the result is flagged."""
    if r_star <= pts[0][0]:
        return pts[0][1], r_star < pts[0][0]
    for (r0, c0), (r1, c1) in zip(pts, pts[1:]):
        if r0 <= r_star <= r1:
            return (c0 if r1 == r0 else c0 + (c1 - c0) * (r_star - r0) / (r1 - r0)), False
    return pts[-1][1], True


def matched_f1(x: list[dict], y: list[dict]) -> tuple[float, float]:
    """Paper A's matched prefix (first k = min counts, in order of first mention) on the asserted v2 classes: micro F1
    x100 of x and of y at matched count."""
    out = []
    for rows in (x, y):
        tp = men = g = 0
        for a, b in zip(x, y):
            k = min(len(a["ord"]), len(b["ord"]))
            pre = (a if rows is x else b)["ord"][:k]
            tp += sum(1 for c in pre if c in a["gold"])
            men += k
            g += a["g"]
        p, r = tp / max(men, 1), tp / max(g, 1)
        out.append(100 * (2 * p * r / (p + r) if p + r else 0.0))
    return out[0], out[1]


def p1_frontier(zs_caps: list[str], ed: list[dict], gold: list[set], gold_u: list[set], idx: np.ndarray) -> dict:
    """Ken K14 P1, registered secondary with its own verdict (K2_GATE0_RULE §6b). Gap_ceiling = CHAIR_i(frontier at
    R_edited) - CHAIR_i(edited); paired image bootstrap, frontier and edited on the same resample. Check T: some k
    meets G1 as written (dR >= -2.0, dCHAIR_i <= -3.0) against the uncut zero-shot. Never changes Gate 0's verdict."""
    kmax = max(len(units(c)) for c in zs_caps)
    rows_k = [[row(cut(c, k), g, gu) for c, g, gu in zip(zs_caps, gold, gold_u)] for k in range(1, kmax + 1)]
    pts = [(float(rates(rk)["R"]), float(rates(rk)["CHAIR_i"])) for rk in rows_k]
    full = pts[-1]  # k = kmax holds every caption uncut
    pe = rates(ed)
    r_ed, c_ed = float(pe["R"]), float(pe["CHAIR_i"])
    c_front, clamped = interp(pts, r_ed)
    gap = c_front - c_ed
    bk = [rates(rk, idx) for rk in rows_k]
    be = rates(ed, idx)
    draws = []
    for b in range(idx.shape[0]):
        p = [(float(x["R"][b]), float(x["CHAIR_i"][b])) for x in bk]
        draws.append(interp(p, float(be["R"][b]))[0] - float(be["CHAIR_i"][b]))
    lo, hi = np.percentile(draws, [2.5, 97.5])
    hw = float((hi - lo) / 2)
    t_hits = [k + 1 for k, (r, c) in enumerate(pts[:-1]) if r - full[0] >= -G["margin_recall"]
              and c - full[1] <= -G["sesoi_chair_i"]]
    if gap >= G["p1_gap_min"] and hw < G["p1_hw_max"] and not clamped:
        verdict = "P1-GO"  # CC-125: a clamped frontier is not a same-recall comparison, so a GO becomes INCONCLUSIVE
    elif gap < G["p1_gap_min"]:
        verdict = "P1-NO-GO"
    else:
        verdict = "P1-INCONCLUSIVE"  # gap clears 2 x SESOI but the half-width does not resolve it, or clamped
    f = lambda x: round(float(x), 4)  # noqa: E731
    return {"verdict": verdict, "label": "Ken K14 P1, registered secondary; data shared with Gate 0 (W7); never a "
            "method result and never a Gate 0 stop",
            "gap_ceiling": f(gap), "gap_ci95": [f(lo), f(hi)], "half_width": f(hw), "R_edited": f(r_ed),
            "CHAIR_i_edited": f(c_ed), "CHAIR_i_frontier_at_R_edited": f(c_front), "frontier_clamped": clamped,
            "frontier_points_R_CHAIR_by_k": [[f(r), f(c)] for r, c in pts], "k_max": kmax,
            "check_T_truncation_meets_G1": bool(t_hits), "check_T_k": t_hits,
            "flag_for_judge": "G1 comparator must become the frontier" if t_hits else None,
            "nogo_text": ("K2 headline under G1 not safe: ceiling does not clear the truncation frontier by 2xSESOI"
                          if verdict == "P1-NO-GO" else None)}


def decide(zs: list[dict], ed: list[dict], deleted: list[list[str]], meta: dict, gold: list[set] | None = None) -> dict:
    """Gate 0/0b STOP rules (a)-(e). Any one fires -> STOP (a negative pilot). GO means only that the ceiling exists.
    gold: per-image gold beside `deleted`, for the W9 diagnostic."""
    n = len(zs)
    idx = np.random.default_rng(G["boot_seed"]).integers(0, n, (G["boot_b"], n))
    pz, pe = rates(zs), rates(ed)
    bz, be = rates(zs, idx), rates(ed, idx)
    d_ch, d_r = pe["CHAIR_i"] - pz["CHAIR_i"], pe["R"] - pz["R"]  # edit - zero-shot
    hw = lambda x: float(np.diff(np.percentile(x, [2.5, 97.5]))[0] / 2)  # noqa: E731
    hw_ch, hw_r = hw(be["CHAIR_i"] - bz["CHAIR_i"]), hw(be["R"] - bz["R"])
    drop, drop_ex = -d_ch, pz["CHAIR_i_unasserted_excluded"] - pe["CHAIR_i_unasserted_excluded"]
    from_unasserted = 1 - drop_ex / drop if drop > 0 else 0.0
    gone = [u for d in deleted for u in d]
    artefacts = sum(lex_v2_artefact(u, g) for d, g in zip(deleted, gold or [set()] * len(deleted)) for u in d)
    neg_share = float(np.mean([bool(RW.NEG_RE.search(u) or RW.unasserted(u)[1]) for u in gone])) if gone else 0.0
    wz, we = np.mean([r["words"] for r in zs]), np.mean([r["words"] for r in ed])
    stop = {
        "(a) edit lowers R by > 1.0": d_r < -G["stop_a_recall_drop"],
        "(b) edit lowers CHAIR_i by < 5.0": drop < G["stop_b_chair_drop"],
        "(c) Gate 0b: edited words < 90% of zero-shot": we < G["stop_c_words"] * wz,
        "(d) ceiling < 2 x SESOI, or a half-width >= its SESOI (STOP-only)":
            drop < 2 * G["sesoi_chair_i"] or hw_ch >= G["sesoi_chair_i"] or hw_r >= G["margin_recall"],
        "(e) W20: most of the CHAIR_i drop comes from negated or hedged mentions":
            from_unasserted > G["unasserted_share_max"],
    }
    f = lambda x: round(float(x), 4)  # noqa: E731
    stop = {k: bool(v) for k, v in stop.items()}
    return {"verdict": "STOP" if any(stop.values()) else "GO", "stop_rules": stop,
            "fired": [k for k, v in stop.items() if v],
            "label": "K2 Gate 0/0b: TARGET CEILING ONLY (val gold edits val captions); never a method result",
            "n_images": n, "zero_shot": {k: f(v) for k, v in pz.items()}, "edited": {k: f(v) for k, v in pe.items()},
            "delta_edit_minus_zs": {"CHAIR_i": f(d_ch), "R": f(d_r), "half_width_CHAIR_i": f(hw_ch),
                                    "half_width_R": f(hw_r)},
            "chair_drop_share_from_unasserted": f(from_unasserted), "deleted_units": len(gone),
            "deleted_units_negated_or_hedged_share": f(neg_share),
            "deleted_units_lex_v2_dining_table_artefact": int(artefacts),  # W9: v1 editor, v2 would not flag them
            "words_mean": {"zs": f(wz), "edited": f(we)},
            "vietnamese_only_pct_zs": f(100 * np.mean([r["vi"] for r in zs])),
            "v1_eq_v2_pct_zs": f(100 * np.mean([r["v1_eq_v2"] for r in zs])), **meta,
            "sesoi_frozen": {"CHAIR_i": -G["sesoi_chair_i"], "recall_margin": -G["margin_recall"]}}


# ------------------------------------------------------------------------------------------------ probe / freeze
def slice_steps(rows: list[dict], n_new: int, batch: int) -> float:
    """Mean decode steps per batch slice at cap n_new: the longest natural length in the slice, capped."""
    L = [math.inf if r["hit_max"] else r["n_tokens"] for r in rows]
    return float(np.mean([min(max(L[k:k + batch]), n_new) for k in range(0, len(L), batch)]))


def slice_rate(log: str, batch: int) -> float:
    """s/img between the first and last 'slice k/n' line of a decoder log whose lines start with an epoch time
    (the job prefixes them), so model loading and the batch-1 parity pass are not counted."""
    t = [float(m.group(1)) for m in re.finditer(r"^(\d+(?:\.\d+)?) slice \d+/\d+", log, re.M)]
    if len(t) < 2:
        raise SystemExit("probe log has fewer than 2 timed slice lines")
    return (t[-1] - t[0]) / ((len(t) - 1) * batch)


def freeze(probe: dict, log: str) -> dict:
    """W3 + cap: the smallest ladder value cutting < 10% of the probe captions, and the Gate-0 cap from the probe rate
    scaled by decode steps. A verdict NOT-RUN (cost) if none qualifies or the cap would exceed the 5 GPU-h ceiling
    (CC-124 W2 amends CC-119 r4's 2 GPU-h, which was computed at the forbidden 160 tokens): it goes to the PI and is
    never a negative pilot."""
    ids = list(probe["predictions"])
    rows = [{"n_tokens": probe["n_tokens"][i], "hit_max": probe["hit_max"][i]} for i in ids]
    s_probe = slice_rate(log, probe["batch_size"])
    cut = {n: float(np.mean([r["hit_max"] or r["n_tokens"] > n for r in rows])) for n in G["n_new_ladder"]}
    ok = [n for n in G["n_new_ladder"] if cut[n] < G["cut_share_max"]]
    b = probe["batch_size"]
    rec = {"probe_images": len(ids), "probe_n_new": probe["max_new_tokens"], "s_per_image_probe": s_probe,
           "cut_share_by_n_new": cut, "probe_prereg_sha256": probe["prereg_sha256"]}
    if not ok:
        return rec | {"verdict": "NOT-RUN", "class": "cost -> TO-PI",
                      "why": "no max_new_tokens <= 1024 cuts < 10% of probe captions"}
    n = ok[0]
    s_img = s_probe * slice_steps(rows, n, b) / slice_steps(rows, probe["max_new_tokens"], b)
    proj = K.N_VAL * s_img / 3600 + G["load_hours"]
    cap = math.ceil(10 * G["cap_factor"] * proj) / 10
    rec |= {"max_new_tokens": n, "s_per_image_projected": s_img, "projected_gpuh": proj, "cap_gpuh": cap}
    if cap > G["ceiling_hours"]:
        return rec | {"verdict": "NOT-RUN", "class": "cost -> TO-PI",
                      "why": f"cap {cap} GPU-h > the {G['ceiling_hours']} GPU-h ceiling"}
    return rec | {"verdict": "GO"}


# ------------------------------------------------------------------------------------------------ files
def probe_manifest(out: Path) -> None:
    """The first 40 UT-2402 ids of the seed-0 schedule (train images: no val image is decoded before the freeze),
    with the staged image sha256 (images.sha256 written by common.stage)."""
    from train import schedule

    sha = {f: h for h, f in (x.split("  ") for x in (K.UV / "images.sha256").read_text().splitlines())}
    names = {str(im["id"]): im["file_name"] for im in json.loads((K.UV / "train_data.json").read_text())["images"]}
    pick = schedule([str(i) for i in K.ids("ut2402")], K.N_TRAIN, K.CFG["seed"])[:G["probe_images"]]
    out.write_text("".join(f"{i}\t{names[i]}\t{sha[names[i]]}\n" for i in pick))


def registration(dataset: str, n_new: int, manifest: Path) -> dict:
    """An LB registration (vsps.lb_prereg.v1) for one K2 run, from B-N1's pinned Qwen3-VL-8B block."""
    bn1 = K.ROOT / BN1
    if K.sha_file(bn1) != BN1_SHA:
        raise SystemExit("REFUSED: the B-N1 registration differs from its pin")
    r = json.loads(bn1.read_text(encoding="utf-8"))
    n = G["probe_images"] if dataset == "probe" else K.N_VAL
    run = f"k2g0_qwen3vl_8b_{dataset}-detailed"
    return {"schema": r["schema"], "prereg_id": "2026-10-27_grl_pilot/K2_GATE0", "venv": r["venv"],
            "models": {"qwen3vl_8b": r["models"]["qwen3vl_8b"]}, "decoder": r["decoder"],
            "decode": {"prompts": {"detailed": r["decode"]["prompts"]["detailed"]},
                       "max_new_tokens": {"detailed": n_new}},
            "datasets": {dataset: {"manifest": {"path": str(manifest), "sha256": K.sha_file(manifest)},
                                   "n_images": n, "image_dir": "uitviic/images"}},
            "runs": [{"run_id": run, "model": "qwen3vl_8b", "dataset": dataset, "prompt_mode": "detailed"}],
            "source": {"b_n1_sha256": BN1_SHA}}


def val_ids_ok(manifest: Path) -> None:
    """W19: the val manifest is exactly val-924, with 0 ids in Karpathy val/test or the C-EN lists, and 0 image
    sha256 in C-EN's three test-side records (which also cover NoCaps val)."""
    rows = [x.split("\t") for x in manifest.read_text().splitlines()]
    ids = {int(r[0]) for r in rows}
    cen = {int(x.split("\t")[0]) for k in ("kval", "test") for x in
           (K.ROOT / f"manuscript/prereg/2026-10-27_c_en/cen_coco_{k}.tsv").read_text().splitlines()[1:]}
    bad_ids, _ = K.refused_sets()
    side = {h for s in K.CEN_TEST_SIDE for h in re.findall(r"\b[0-9a-f]{64}\b", (K.CEN_REC / f"{s}.sha256.tsv").read_text())}
    if ids != set(K.ids("val924")) or ids & (cen | bad_ids) or {r[2] for r in rows} & side:
        raise SystemExit("REFUSED: the val manifest overlaps a protected set (W19)")


def cmd_score(a) -> int:
    out = Path(a.out)
    if out.exists():
        raise SystemExit(f"REFUSED: {out} exists (one look)")
    p = json.loads(Path(a.preds).read_text(encoding="utf-8"))
    fz = json.loads(Path(a.freeze).read_text())
    if p["max_new_tokens"] != fz["max_new_tokens"] or sorted(map(int, p["predictions"])) != K.ids("val924"):
        raise SystemExit("REFUSED: the decode is not the frozen val-924 run")
    gold = K.gold()
    refs: dict[int, set] = {}
    for x in json.loads((K.UV / "val_data.json").read_text(encoding="utf-8"))["annotations"]:
        refs.setdefault(int(x["image_id"]), set()).update(RW.ordered(x["caption"], "v2")[0])
    zs, ed, gone, caps, golds, golds_u = [], [], [], [], [], []
    for i in K.ids("val924"):
        c = untruncate(p["predictions"][str(i)], p["hit_max"][str(i)])
        e, d = edit(c, gold[i])
        gu = gold[i] | refs.get(i, set())
        zs.append(row(c, gold[i], gu) | {"gold": gold[i]})
        ed.append(row(e, gold[i], gu) | {"gold": gold[i]})
        gone.append(d)
        caps.append(c)
        golds.append(gold[i])
        golds_u.append(gu)
    mem = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", Path(a.mem_log).read_text())] if a.mem_log else []
    meta = {"max_new_tokens": p["max_new_tokens"], "cap_hit_pct": 100 * float(np.mean(list(p["hit_max"].values()))),
            "s_per_image": None, "peak_gpu_mem_gib": max(mem) / 1024 if mem else None, "decode_sha256": K.sha_file(Path(a.preds)),
            "freeze": fz}
    from datetime import datetime
    t = lambda k: datetime.fromisoformat(p[k].replace("Z", "+00:00")).timestamp()  # noqa: E731
    meta["s_per_image"] = (t("finished_utc") - t("started_utc")) / len(p["predictions"])
    rec = decide(zs, ed, gone, meta, golds)
    out.write_text(json.dumps(rec, indent=1, default=float) + "\n")  # CC-125 X1: Gate 0 is decided before any P1 code
    if rec["verdict"] == "STOP":
        stop_md(out.parent / "STOP.md", rec)
    p1 = p1_stage(out, rec, (caps, zs, ed, golds, golds_u), meta)
    print(json.dumps({"verdict": rec["verdict"], "fired": rec["fired"], "p1": p1}))
    return 0


def p1_stage(out: Path, rec: dict, data: tuple, meta: dict) -> str:
    """CC-125 X1: P1 after the Gate 0 record, inside try/except. data = (zero-shot captions, zs rows, edited rows,
    gold, gold-union) per val image. On success gate0_decide.json is rewritten with only
    `p1_truncation_frontier` added (Gate 0 keys unchanged) and P1_VERDICT.md is written; on any exception
    P1_VERDICT.md says P1-ERROR and gate0_decide.json stays as written. Returns the P1 verdict string."""
    verdict_md = out.parent / "P1_VERDICT.md"
    caps, zs, ed, golds, golds_u = data
    try:
        idx = np.random.default_rng(G["boot_seed"]).integers(0, len(zs), (G["boot_b"], len(zs)))
        p1 = p1_frontier(caps, ed, golds, golds_u, idx)
        m_ed, m_zs = matched_f1(ed, zs)
        p1 |= {"matched_count_F1_edited": round(m_ed, 4), "matched_count_F1_zero_shot": round(m_zs, 4),
               "cap_hit_pct": meta.get("cap_hit_pct"), "words_mean": rec["words_mean"]}
    except Exception as e:  # noqa: BLE001  the registered secondary must never leave Gate 0 undecided
        verdict_md.write_text(f"# Ken K14 P1 (registered secondary): P1-ERROR (not run)\n\n- {type(e).__name__}: {e}\n"
                              "- Gate 0's own verdict stands as written in gate0_decide.json.\n")
        return "P1-ERROR"
    rec = json.loads(out.read_text(encoding="utf-8")) | {"p1_truncation_frontier": p1}
    out.write_text(json.dumps(rec, indent=1, default=float) + "\n")
    verdict_md.write_text(
        f"# Ken K14 P1 (registered secondary): {p1['verdict']}\n\n" + (f"- {p1['nogo_text']}\n" if p1["nogo_text"] else "")
        + (f"- FLAG FOR JUDGE: {p1['flag_for_judge']} (check T true at k = {p1['check_T_k']})\n" if p1["flag_for_judge"] else "")
        + "- Gate 0's own verdict is unchanged by P1.\n\n```json\n" + json.dumps(p1, indent=1, default=float) + "\n```\n")
    return p1["verdict"]


def stop_md(p: Path, rec: dict) -> None:
    """W8: a STOP writes STOP.md with the measured values; no rerun, no tuned retry. A cost NOT-RUN (CC-124 W2) is
    labelled as such: it goes to the PI and is never a negative pilot."""
    head = ("# K2 Gate 0/0b NOT RUN (cost) -> TO-PI; not a negative pilot\n\n" if rec["verdict"] == "NOT-RUN"
            else "# K2 Gate 0/0b STOP: negative pilot (no rerun)\n\n")
    p.write_text(head + "\n".join(f"- {k}" for k in rec.get("fired", [rec.get("why")]))
                 + "\n\n```json\n" + json.dumps({k: v for k, v in rec.items() if k != "stop_rules"}, indent=1,
                                                default=float) + "\n```\n")


# ------------------------------------------------------------------------------------------------ selftest
def selftest() -> None:
    g = {"person", "sports ball"}
    assert untruncate("một người cầm quả bóng. con chó đang", True) == "một người cầm quả bóng."
    assert untruncate("một người cầm quả bóng. con chó đang", False).endswith("đang")
    e, d = edit("một người cầm quả bóng, cạnh con chó. bầu trời xanh.", g)
    assert e == "một người cầm quả bóng, bầu trời xanh." and d == [" cạnh con chó."], (e, d)
    e, d = edit("một người, cạnh con chó", g)
    assert e == "một người." and len(d) == 1, (e, d)
    assert edit("một người 人.", g)[0] == ""  # language check deletes the unit
    r = row("một người, không có con chó.", g, g)
    assert r["tp"] == 1 and r["hal"] == 1 and r["men"] == 2 and r["hal_ex"] == 0 and r["hal_plain"] == 1, r
    # decide: 60 images, zs names a wrong dog in a separate unit, edit removes it
    n = 60
    zs = [row("một người cầm quả bóng, cạnh con chó.", g, g) for _ in range(n)]
    eds = [edit("một người cầm quả bóng, cạnh con chó.", g) for _ in range(n)]
    ed = [row(x, g, g) for x, _ in eds]
    res = decide(zs, ed, [x for _, x in eds], {})
    assert res["zero_shot"]["CHAIR_i"] == round(100 / 3, 4) and res["edited"]["CHAIR_i"] == 0.0, res
    assert res["fired"] == ["(c) Gate 0b: edited words < 90% of zero-shot"], res["fired"]  # 5 of 8 words kept
    head = ("một người khoác áo sọc tím lấp lánh đang tâng quả bóng bạc lơ lửng giữa bãi cát vàng óng dưới mái "
            "vòm kính cong queo cạnh hàng cờ đuôi nheo phất phơ")  # CC-125 X5: synthetic, 0 caption 6-grams
    long = head + ", cạnh con chó."
    eds = [edit(long, g) for _ in range(n)]
    res = decide([row(long, g, g) for _ in range(n)], [row(x, g, g) for x, _ in eds], [x for _, x in eds], {})
    assert res["verdict"] == "GO" and res["delta_edit_minus_zs"]["R"] == 0.0, res
    neg = head + ", không có con chó."
    eds = [edit(neg, g) for _ in range(n)]
    res = decide([row(neg, g, g) for _ in range(n)], [row(x, g, g) for x, _ in eds], [x for _, x in eds], {})
    assert "(e) W20: most of the CHAIR_i drop comes from negated or hedged mentions" in res["fired"], res
    # freeze: every natural length 300 -> 256 cuts all, 384 cuts none; 5 s/img -> cap 1.7 GPU-h
    probe = {"predictions": {str(k): "" for k in range(40)}, "batch_size": 4, "max_new_tokens": 1024,
             "n_tokens": {str(k): 300 for k in range(40)}, "hit_max": {str(k): False for k in range(40)},
             "prereg_sha256": "x"}
    log = lambda sec: "loading\n" + "".join(f"{100 + k * 4 * sec} slice {k + 1}/10\n" for k in range(10))  # noqa: E731
    fz = freeze(probe, log(5))
    assert fz["verdict"] == "GO" and fz["max_new_tokens"] == 384 and abs(fz["s_per_image_projected"] - 5.0) < 1e-9, fz
    assert fz["cap_gpuh"] == 1.7, fz
    probe["hit_max"] = {str(k): k < 4 for k in range(40)}
    assert freeze(probe, log(5))["verdict"] == "NOT-RUN"  # 4/40 cut at every value
    probe["hit_max"] = {str(k): False for k in range(40)}
    nr = freeze(probe, log(30))  # 924 x 30 s -> cap 9.4 > 5 GPU-h
    assert nr["verdict"] == "NOT-RUN" and nr["cap_gpuh"] == 9.4 and nr["class"] == "cost -> TO-PI", nr
    assert freeze(probe, log(15))["verdict"] == "GO"  # cap 4.8 <= 5
    # W9: a deleted "ghi bàn" unit is a LEX_V2 artefact; a real dining table is not
    assert lex_v2_artefact(" cầu thủ ghi bàn.", g) and not lex_v2_artefact(" cạnh cái bàn ăn.", g)
    eds = [edit("một người cầm quả bóng trên sân, cầu thủ ghi bàn.", g) for _ in range(3)]
    assert decide([row("x", g, g)] * 3, [row(x, g, g) for x, _ in eds], [d for _, d in eds], {}, [g] * 3)[
        "deleted_units_lex_v2_dining_table_artefact"] == 3
    assert hashlib.sha256(b"").hexdigest() and slice_steps([{"n_tokens": 5, "hit_max": False}] * 4, 3, 4) == 3
    # P1 frontier (Ken K14): synthetic clauses; idx of 50 draws over n identical images gives half-width 0
    assert cut("a, b. c", 2) == "a, b." and cut("a, b. c", 9) == "a, b. c"
    assert interp([(0, 100), (100, 50)], 50) == (75.0, False) and interp([(0, 100), (100, 50)], 120) == (50, True)
    assert interp([(33, 0), (67, 0), (100, 0), (100, 25)], 100) == (0, False)  # equal recalls: the first k reaching it
    n = 30
    ix = np.random.default_rng(0).integers(0, n, (50, n))
    P1 = lambda zs_c, g: p1_frontier([zs_c] * n, [row(edit(zs_c, g)[0], g, g) | {"gold": g}] * n,  # noqa: E731
                                     [g] * n, [g] * n, ix)
    # hallucinations early: the edit beats every prefix at its recall -> P1-GO, T false
    r1 = P1("một con chó cạnh cái bàn, một người cầm quả bóng trên sân.", {"person", "sports ball"})
    assert r1["verdict"] == "P1-GO" and r1["gap_ceiling"] == 50.0 and r1["half_width"] == 0.0, r1
    assert r1["frontier_points_R_CHAIR_by_k"] == [[0.0, 100.0], [100.0, 50.0]] and not r1["check_T_truncation_meets_G1"]
    # hallucination last: cutting to k = 1 already meets G1 as written -> T true, gap 0 -> P1-NO-GO + judge flag
    r2 = P1("một người cầm quả bóng trên sân, cạnh con chó.", {"person", "sports ball"})
    assert r2["verdict"] == "P1-NO-GO" and r2["check_T_k"] == [1] and r2["flag_for_judge"] and r2["nogo_text"], r2
    # recall rises with k, hallucination only in the last clause: frontier(R_edited) = 0 -> NO-GO; the k = 3 cut keeps
    # full recall and drops the hallucination, so truncation meets G1 as written: T true at k = 3
    r3 = P1("một người, quả bóng, con chó, cái bàn.", {"person", "sports ball", "dog"})
    assert r3["verdict"] == "P1-NO-GO" and r3["gap_ceiling"] == 0.0 and r3["check_T_k"] == [3], r3
    assert r3["frontier_points_R_CHAIR_by_k"][:3] == [[round(100 / 3, 4), 0.0], [round(200 / 3, 4), 0.0], [100.0, 0.0]]
    # CC-125 X1: all-empty captions raise IndexError inside p1_frontier (the judge's degenerate input); p1_stage must
    # leave Gate 0's record intact and write P1-ERROR. Also: a clamped frontier never yields P1-GO.
    import tempfile
    try:
        p1_frontier([""] * 3, [row("", set(), set()) | {"gold": set()}] * 3, [set()] * 3, [set()] * 3, ix[:, :3])
    except IndexError as e:
        assert "index" in str(e).lower(), e  # the judge's reproduction: pts[-1] on an empty frontier
    else:
        raise AssertionError("the degenerate input no longer raises; update this case")
    with tempfile.TemporaryDirectory() as t:
        out = Path(t) / "gate0_decide.json"
        stub = {"verdict": "GO", "words_mean": {"zs": 1.0, "edited": 1.0}}
        out.write_text(json.dumps(stub) + "\n")
        v = p1_stage(out, stub, ([""] * 3, [row("", set(), set())] * 3, [row("", set(), set()) | {"gold": set()}] * 3,
                                 [set()] * 3, [set()] * 3), {"cap_hit_pct": 0.0})
        assert v == "P1-ERROR" and json.loads(out.read_text()) == stub, (v, out.read_text())
        assert (Path(t) / "P1_VERDICT.md").read_text().startswith("# Ken K14 P1 (registered secondary): P1-ERROR")
        gg = {"person", "sports ball"}
        zc = "một con chó cạnh cái bàn, một người cầm quả bóng trên sân."
        v = p1_stage(out, stub, ([zc] * n, [row(zc, gg, gg) | {"gold": gg}] * n,
                                 [row(edit(zc, gg)[0], gg, gg) | {"gold": gg}] * n, [gg] * n, [gg] * n), {"cap_hit_pct": 0.0})
        j = json.loads(out.read_text())
        assert v == "P1-GO" and j["verdict"] == "GO" and j["p1_truncation_frontier"]["verdict"] == "P1-GO", j
    assert interp([(50, 20), (100, 10)], 30)[1] is True  # R_edited below R_1: clamped
    g = {"person", "sports ball"}
    zr = [row("một con chó, một người cầm quả bóng.", g, g) | {"gold": g}] * 2
    er = [row("một người cầm quả bóng.", g, g) | {"gold": g}] * 2
    # matched count k = 2: the edited prefix [person, ball] is all gold (F1 100); the zero-shot prefix [dog, person]
    # has tp 1 of 2 mentions and 1 of 2 gold (P .5, R .5, F1 50)
    assert matched_f1(er, zr) == (100.0, 50.0), matched_f1(er, zr)

    print("k2_gate0 selftest ok")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", nargs="?", choices=("manifest", "reg", "freeze", "score"))
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--dataset", choices=("probe", "val"))
    ap.add_argument("--n-new", type=int)
    ap.add_argument("--manifest")
    ap.add_argument("--probe")
    ap.add_argument("--probe-log")
    ap.add_argument("--preds")
    ap.add_argument("--freeze")
    ap.add_argument("--mem-log")
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return 0
    if a.cmd == "manifest":
        probe_manifest(Path(a.out))
    elif a.cmd == "reg":
        m = Path(a.manifest)
        if a.dataset == "val":
            val_ids_ok(m)
        Path(a.out).write_text(json.dumps(registration(a.dataset, a.n_new, m), indent=1) + "\n")
    elif a.cmd == "freeze":
        rec = freeze(json.loads(Path(a.probe).read_text(encoding="utf-8")), Path(a.probe_log).read_text())
        Path(a.out).write_text(json.dumps(rec, indent=1) + "\n")
        if rec["verdict"] != "GO":
            stop_md(Path(a.out).parent / "STOP.md", rec)
        print(json.dumps(rec))
    else:
        return cmd_score(a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
