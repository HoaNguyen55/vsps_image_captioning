#!/usr/bin/env python3
"""C-ATTR-DEV statistics (CPU, on the rented host: PI-1111j; the laptop keeps the 444 copy and the hashes only).
Registration manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_DEV_PREREG_v1_1.md §7 (estimands, one image-bootstrap index
matrix per set, the p-like statistic, labels, the one DETECTED rule with Holm step-down at family-wise one-sided 0.025,
nomination, variance and the fixed-set ANOVA), §8 (copy bound, units (i) and (ii), companions), §9 (the document-
frequency sensitivity row), §7.9 (the post hoc swap δ), addendum v1.2 V4 (scoring order), CC-331 X1-X3, CC-332 notes,
CC-338 S1-S5, CC-346 SC1-SC5. Label on every output: DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY.

  python -I -B scripts/c_attr/c_attr_score.py --selftest                       planted data only
  python -I -B scripts/c_attr/c_attr_score.py stage verify|ova|close|ovb|rest|posthoc --prev SHA ...   S1, the host
      scoring order, one stage per call (scripts/c_attr/c_attr_score_job.sh; run document C_ATTR_SCORING_RUN_DOC_v1.md)
  python -I -B scripts/c_attr/c_attr_score.py score ... [--nomination F] [--verdict V]   = c_attr.py score (V4 gates)
  python -I -B scripts/c_attr/c_attr_score.py nominate --ledger L ... --parity P ... --out c_attr_nomination.json
  python -I -B scripts/c_attr/c_attr_score.py summary --ledger L ... [--nomination F] --parity P ... --out S
  python -I -B scripts/c_attr/c_attr_score.py copybound --set S --zs Z --ret R --rand D [--blind B] --kit-b K
                                                        --c-lists L --c2-ledger G --c2-run Q --out O     §8
  python -I -B scripts/c_attr/c_attr_score.py stage b3verify --b3-sums SHA | b3k5|b3rest --prev SHA    block 3
      (C_ATTR_BLOCK3_SCORING_RUN_DOC_v1.md, CC-368 ruling 12): its own work folder /root/c_attr_score_b3; the K5
      verdict in its own file before any other block-3 row; refused at and after K7 (2026-11-16 12:00 VN)

Outputs hold ids and numbers only; nothing prints a caption. lmcap_rand / lmcap_perm rows are a re-implementation of
the LMCap recipe by this study; ret_img vs rand_img rows are an image-caption-pair prompt format, as used by RAGCap;
not RAGCap. No row says that a published system was tested.
"""
from __future__ import annotations

import argparse
import calendar
import hashlib
import importlib.metadata
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import c_attr as A  # noqa: E402

SESOI, ALPHA = A.SESOI, 0.025  # §7.4: +2.0; family-wise one-sided alpha (X1)
SPLIT = "split of a known τ_sel"  # X2: every τ_pair / τ_marg row on OV-dev-A or OV-dev-B
KNOWN_SUM = ("ov_dev_a", "ov_dev_b")
OLD3 = ("qwen25vl_7b", "internvl3_8b", "aya_vision_8b")
NOMINATORS = ("qwen25vl_7b", "internvl3_8b")  # §7.5 item 1
REG_RDF = {"ov_dev_a": (1, 2, 1), "ov_dev_b": (3, 2, 5), "xm_dev500": (3, 2, 5), "f30k_val": (3, 2, 0)}  # §7.2
#: addendum v1.2 (CC-340): row labels (V1, V6, CC-338 S2), the nomination file it accepts, the v1.1 file it refuses
REG12 = "C_ATTR_DEV_ADDENDUM_v1_2.md (block 1b, batch size 1)"
V11_NAME = "c_attr_nomination_v11.json"
B1_NOTE = "batch size 1; registered in v1.2 after K1 fired, on string-identity counts only"
BATCHED = "A1 not met; batched decode; descriptive"
SEL_B1 = "batch-1 re-decode of a known τ_sel"
HOST_FB = "base arms re-decoded on the new host"
B1_COLS = ("ret", "rand_d0", "perm_p1", "perm_p2")  # SC4: the OV-dev-A columns of every D1-PASS nominator
#: §9 sensitivity row: fixed before any 1b score (CC-346 ruling 2), independent of the OV-dev-A outcome
SENS_B, SENS_MODEL = 200, "qwen25vl_7b"  # the first 200 rows of OV-dev-B's shared index matrix; Qwen2.5-VL tau_pair, tau_marg
UNITS = ("i_syllables", "ii_words")  # §8: (i) whitespace syllables, (ii) RDRSegmenter words
COMPANION = "descriptive; never called a bound"
SWAP_TIER = "POST HOC; size-confounded (full COCO memory, 111,927 clusters, against the Flickr30K-train memory, 28,000)"
LENGTH_GAP = 0.10  # §7.9 rule L
#: S1: the host layout of the scoring order
WORK = Path("/root/c_attr_score")
SRC = {"b1": Path("/root/outputs/c_attr_b1"), "b": Path("/root/outputs/c_attr")}
CL = A.ROOT / "manuscript/prereg/2026-10-22_c_stage1/lists.json"
KIT = A.ROOT / "scripts/kit_b"
FILES = {"verify": "VERIFY.json", "ova": "c_attr_nomination.json", "close": "c_attr_nomination.json",
         "ovb": "VERDICT.json", "rest": "SUMMARY.json", "posthoc": "POSTHOC.json",
         "b3verify": "VERIFY.json", "b3k5": "K5.json", "b3rest": "B3_SUMMARY.json"}
PREV = {"ova": "VERIFY.json", "close": "VERIFY.json", "ovb": "c_attr_nomination.json", "rest": "VERDICT.json",
        "posthoc": "SUMMARY.json", "b3k5": "VERIFY.json", "b3rest": "K5.json"}
#: block 3 (C_ATTR_BLOCK3_RUN_DOC_v1_1.md §8, CC-368 ruling 12 and N4): its own work folder, chain and strings
B3_STAGES = ("b3verify", "b3k5", "b3rest")
WORK_B3, SRC_B3 = Path("/root/c_attr_score_b3"), Path("/root/outputs/c_attr_b3")
REG_B3 = ("C_ATTR_DEV_PREREG_v1_1.md §6.5, §7.10 with addendum v1.2 V8 (block 3, batch size 1); "
          "C_ATTR_BLOCK3_RUN_DOC_v1_1.md (CC-368)")
K7_UTC = "2026-11-16T05:00:00Z"  # v1.1 §10.1 K7 = 2026-11-16 12:00 VN, the only hard date (CC-368 ruling 6)
K7_TS = calendar.timegm(time.strptime(K7_UTC, "%Y-%m-%dT%H:%M:%SZ"))
CLOCK = time.time
B3_RUNNERS = ("lmcap", "qwen25vl_7b")
B3_NOM, B3_NOM_SHA256 = "c_attr_nomination.json", "559c18c1ba173cfbfed488d2bb7f7d797b66d681bd69aec51944f0c4e88ebdfa"
B3_REFS = {"datasets/openviic/uit-openviic-annotation-dev.json":  # CC-362: hash only, never opened by anyone
           "550cfe06b06084976e81286531f7f4e52bea717e29004c699ccaf1e48919bdff",
           "datasets/c_xm_dev500/xm_dev500_data.json": "0da82355b65ab284fe55fc0d3c4101090301767347a02721890556618ca4905f"}
B3_BATCH = "batch size 1 (addendum v1.2 V8)"  # CC-368 O9
B3_DECODES = "all arms decoded on one host in block 3; stored decodes not used (CC-368)"  # CC-368 ruling 3, N1
E6 = {"lmcap": "re-implementation of the LMCap recipe by this study; not the authors' code (no licence); "
               "not a statement about the published numbers",
      "qwen25vl_7b": "image-caption-pair prompt format, as used by RAGCap; not RAGCap"}  # erratum 1 E6
B3_EST = (("lmcap", "tau_sel", "lmcap_ri|lmcap", "lmcap_rand|lmcap"),  # v1.1 §7.10
          ("lmcap", "tau_pair", "lmcap_ri|lmcap", "lmcap_perm|lmcap"),
          ("lmcap", "tau_marg", "lmcap_perm|lmcap", "lmcap_rand|lmcap"),
          ("qwen25vl_7b", "tau_sel_img", "qwen25vl_7b|ret_img", "qwen25vl_7b|rand_d0_img"))
B3_TIER = {  # OV-dev-B, CC-368 O8: no row carries "split of a known τ_sel"
    "lmcap|tau_sel": "K5 positive control (v1.1 §7.10, §10.1): first look at the contrast; the lmcap_ri level was "
                     "seen in C-T1 (ret - lmcap_ri)",
    "lmcap|tau_pair": "first look (not a split of a known τ_sel: the sum was not known)",
    "lmcap|tau_marg": "first look (not a split of a known τ_sel: the sum was not known)",
    "qwen25vl_7b|tau_sel_img": "first look; its ret_img side was seen in C-T1"}
B3_XM = "no rule (v1.1 §7.8)"
TEXT_SEL = {"ov_dev_b": "VERDICT.json :: sets.ov_dev_b.rows.qwen25vl_7b|tau_sel (sha256 a69a0ec2…, CC-363; batch 1)",
            "xm_dev500": "SUMMARY.json :: sets.xm_dev500.rows.qwen25vl_7b|tau_sel (sha256 1d78cd20…, CC-363; batch 1)"}
K5_RULE = "LMCap τ_sel on OV-dev-B DETECTED iff θ̂ >= +2.0 and p <= 0.025, m = 1 (v1.1 §7.4, §7.10, §10.1 K5)"
K5_OUT = {"DETECTED": "K5 not fired",
          "NOT DETECTED": "K5 fired: the positive control failed; the word 'test' is dropped; third-party rows are "
                          "printed without interpretation (v1.1 §10.1, §7.12)",
          "NOT RUN": "K5 NOT RUN: the CC-363 ruling 5 line stands (no 'test': the positive control was not run); "
                     "third-party rows are printed without interpretation (CC-368 ruling 6)"}
UNINTERPRETED = "printed without interpretation (K5 not DETECTED)"
TEST_NAME = re.compile(r"(?:^|[-_.])test(?:[-_.\d]|$)|" + "|".join(A.TEST_SETS))  # binding 1: refused by name


def is_b1(run_id: str) -> bool:
    return "b1" in run_id.split("-")


def split_b1(led: list[dict]) -> tuple[list[dict], list[dict]]:
    """V2: batch-1 rows ('-b1' run ids) and every other row (batched block-1, stored); never mixed in one contrast."""
    b1 = [r for r in led if is_b1(r.get("run_id", ""))]
    return b1, [r for r in led if not is_b1(r.get("run_id", ""))]


def nomination(path) -> dict:
    """V4: the v1.2 nomination file; c_attr_nomination_v11.json is refused by name and by content (V1)."""
    if not path or not Path(path).is_file():
        raise SystemExit("REFUSED: no v1.2 nomination file (V4)")
    rec = json.loads(Path(path).read_text(encoding="utf-8"))
    if Path(path).name == V11_NAME or rec.get("registration") != REG12 or "K1" in str(rec.get("reason", "")):
        raise SystemExit(f"REFUSED: {Path(path).name} is not a v1.2 nomination file (the v1.1 K1 file never licenses)")
    return rec


def released(a) -> bool:
    """V4 (3): batched outputs only after the batch-1 OV-dev-B verdict (a v1.2 summary holding OV-dev-B) or, by the
    release clause, an empty v1.2 nomination file. The LOG lines that must precede both are the operator's (stage)."""
    if a.verdict:
        v = json.loads(Path(a.verdict).read_text(encoding="utf-8"))
        return v.get("registration") == REG12 and "ov_dev_b" in v.get("sets", {}) and bool(v.get("nomination_sha256"))
    return bool(a.nomination) and nomination(a.nomination)["nominated"] == []


def v4_gate(a) -> None:
    """v1.2 V4 and CC-338 S4. c_attr.cmd_score calls this first, so every caller of `score` passes here (SC1)."""
    runs = [json.loads(Path(p).read_text(encoding="utf-8")) for p in a.runs]
    at = [r for r in runs if str(r.get("run_id", "")).startswith("at_")]
    b1 = [r for r in at if is_b1(r["run_id"])]
    if any(r.get("spec", {}).get("batch_size") != 1 for r in b1):
        raise SystemExit("REFUSED: a '-b1' run that was not decoded at batch size 1")
    ovb = [r for r in runs if str(r.get("run_id", "")).startswith("at_") or r.get("spec", {}).get("arm") == "perm"]
    if a.set == "ov_dev_b" and ovb:  # §7.5 item 2, Binding 8, CC-338 S4, v1.2 V4 (1)
        nomination(a.nomination)
        print(f"nomination file sha256 {A.sha(a.nomination)}")
    if len(b1) < len(at) and not released(a):  # v1.2 V4 (3)
        raise SystemExit("REFUSED: batched block-1 outputs are scored only after the batch-1 OV-dev-B verdict (V4)")


def parity(paths) -> dict:
    """CC-338 S2 / v1.2 V3: {model: {host_parity, A1, D1}} from parity/STEP10_<m>.json and STEP1B0_<m>.json. A FAIL
    in any file stands against a PASS in another, in any order (V3: a D1 failure on either host removes it; SC3)."""
    out = {}
    for p in paths or []:
        r = json.loads(Path(p).read_text(encoding="utf-8"))
        cur = out.setdefault(r["model"], {})
        for k in ("host_parity", "A1", "D1"):
            if k in r:
                cur[k] = "FAIL" if "FAIL" in (cur.get(k), r[k]) else r[k]
    return out


# ------------------------------------------------------------------------------------------------ §7.3-7.4
def summary(point: float, bm: np.ndarray) -> dict:
    lo, hi, lo90, hi90 = np.percentile(bm, [2.5, 97.5, 5, 95])
    return {"d": float(point), "lo": float(lo), "hi": float(hi), "lo90": float(lo90), "hi90": float(hi90),
            "p": float((1 + np.sum(bm <= 0)) / (len(bm) + 1)), "_bm": bm}


def pair(a, b, idx: np.ndarray) -> dict:
    """Paired image bootstrap of mean(a - b): the same resampled images for both arms."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    rows = idx  # one index matrix per set, shared by every contrast on that set (§7.3)
    return summary(a.mean() - b.mean(), a[rows].mean(1) - b[rows].mean(1))


def detected(claims: dict[str, tuple[float, float]], alpha: float = ALPHA) -> set[str]:
    """§7.4 DETECTED over one family {name: (point, p)}: Holm step-down at family-wise one-sided alpha, the j-th
    smallest p against alpha / (m - j + 1), and point >= +2.0; stop at the first failure (strict reading: a claim that
    fails either condition ends the step-down). A row outside every family is a family of m = 1."""
    m, out = len(claims), set()
    for j, (k, (d, p)) in enumerate(sorted(claims.items(), key=lambda kv: (kv[1][1], kv[0])), 1):
        if not (d >= SESOI and p <= alpha / (m - j + 1)):
            break
        out.add(k)
    return out


def label(s: dict, is_detected: bool) -> str:
    """Mutually exclusive labels, first match: DETECTED, REVERSED (95% upper < 0), NEGLIGIBLE (90% interval inside
    (-2.0, +2.0)), UNRESOLVED."""
    if is_detected:
        return "DETECTED"
    if s["hi"] < 0:
        return "REVERSED"
    if s["lo90"] > -SESOI and s["hi90"] < SESOI:
        return "NEGLIGIBLE"
    return "UNRESOLVED"


def draw_keys(per: dict, m: str, arm: str) -> list[str]:
    """The columns of one arm's draws (rand_d<j>, perm_p<j>, fix_f<j>). The X2 masked columns ('..._m3') that the
    scorer writes beside every run are not draws and never enter a draw mean (found with SC1-SC5)."""
    return sorted(k for k in per if re.fullmatch(rf"{re.escape(m)}\|{arm}\d+", k))


def arm_mean(per: dict, m: str, arm: str) -> tuple[np.ndarray | None, int]:
    """Per-image mean over the draws / permutations / fixed sets present for (model, arm), and their number."""
    keys = draw_keys(per, m, arm)
    return (np.mean([per[k] for k in keys], axis=0), len(keys)) if keys else (None, 0)


def set_rows(per: dict, ds: str, idx: np.ndarray) -> dict[str, dict]:
    """§7.2 estimands per backbone on one set: tau_any, tau_sel, tau_marg, tau_pair, and the rand d1 - d2 placebo."""
    rows = {}
    for m in sorted({k.split("|")[0] for k in per}):
        zs, ret = per.get(f"{m}|zs"), per.get(f"{m}|ret")
        rand, r = arm_mean(per, m, "rand_d")
        perm, d = arm_mean(per, m, "perm_p")
        for est, a, b in (("tau_any", rand, zs), ("tau_sel", ret, rand), ("tau_marg", perm, rand),
                          ("tau_pair", ret, perm)):
            if a is not None and b is not None:
                rows[f"{m}|{est}"] = {**pair(a, b, idx), "model": m, "estimand": est, "R": r, "D": d,
                                      "registered_R_D": REG_RDF.get(ds, (None, None))[:2]}
        if f"{m}|rand_d1" in per and f"{m}|rand_d2" in per:
            pl = pair(per[f"{m}|rand_d1"], per[f"{m}|rand_d2"], idx)
            rows[f"{m}|placebo_d1_d2"] = {**pl, "model": m, "estimand": "placebo rand d1 - rand d2",
                                         "flag": bool(abs(pl["d"]) >= SESOI and (pl["lo"] > 0 or pl["hi"] < 0))}
    return rows


def apply_labels(rows: dict, ds: str, families: dict[str, list[str]]) -> None:
    """Families: {name: [row keys]}; every other row is its own family of m = 1. Notes: X2 on the known-sum sets."""
    fam_of = {k: f for f, ks in families.items() for k in ks if k in rows}
    det = set()
    for f, ks in families.items():
        det |= detected({k: (rows[k]["d"], rows[k]["p"]) for k in ks if k in rows})
    for k, r in rows.items():
        if k not in fam_of:
            det |= detected({k: (r["d"], r["p"])})
        r["label"], r["family"] = label(r, k in det), fam_of.get(k)
        r["m"] = len([x for x in families.get(fam_of.get(k), [k]) if x in rows]) if k in fam_of else 1
        if r.get("estimand") in ("tau_pair", "tau_marg") and ds in KNOWN_SUM:
            r["note"] = SPLIT
        r["tag"] = A.LABEL


# ------------------------------------------------------------------------------------------------ §7.5 nomination
def nominate(rows_a: dict) -> list[str]:
    """OV-dev-A: H_pair(m) / H_marg(m) when the 95% lower bound of tau_pair / tau_marg is >= +2.0 (c_t1.advance)."""
    out = []
    for m in NOMINATORS:
        for est, h in (("tau_pair", "H_pair"), ("tau_marg", "H_marg")):
            r = rows_a.get(f"{m}|{est}")
            if r is not None and A.advance(r) == "NOMINATE":
                out.append(f"{h}({m})")
    return out


def family_keys(nominated: list[str]) -> list[str]:
    est = {"H_pair": "tau_pair", "H_marg": "tau_marg"}
    return [f"{c.split('(')[1].rstrip(')')}|{est[c.split('(')[0]]}" for c in nominated]


def ovb_perm_scored(ledger_rows: list[dict]) -> bool:
    """CC-338 S4: any new OV-dev-B output (a perm row or any C-ATTR 'at_' run) counts."""
    return any(r.get("dataset") == "ov_dev_b" and (r.get("arm") == "perm" or str(r.get("run_id", "")).startswith("at_"))
               for r in ledger_rows)


def dedup(rows: list[dict]) -> list[dict]:
    """A stored run scored in two calls (its zs is needed by each call) enters the summary once; the copies must agree
    on the ids and the decision columns, else REFUSED."""
    out = {}
    for r in rows:
        k = (r.get("run_id"), r.get("dataset"), r.get("tau"), r.get("variant"))
        if k in out and any(out[k]["per_image"].get(c) != r["per_image"].get(c) for c in ("ids", "cider_s", "cider_ptb")):
            raise SystemExit(f"REFUSED: two ledger rows of {k[0]} on {k[1]} disagree")
        out.setdefault(k, r)
    return list(out.values())


# ------------------------------------------------------------------------------------------------ §7.7 variance
def draw_variance(per: dict, m: str, ret: np.ndarray | None) -> dict | None:
    """§7.7a: mean within-image variance over draws, its share of the image-bootstrap variance of ret - rand mean."""
    keys = draw_keys(per, m, "rand_d")
    if len(keys) < 2 or ret is None:
        return None
    x = np.array([per[k] for k in keys])
    n, r = x.shape[1], x.shape[0]
    s2w = float(x.var(axis=0, ddof=1).mean())
    total = float(np.var(ret - x.mean(0), ddof=1) / n)
    return {"sigma2_w": s2w, "draw_part": s2w / (n * r), "total": total, "share": s2w / (n * r) / total if total else None}


def anova_fix(y: np.ndarray) -> dict:
    """§7.7b, y = s(ret) - s(fix_F), n x R_F, one value per cell. V_b, V_img, omega, the F-based upper bound and the
    five-set development row (t interval, R_F - 1 df)."""
    from scipy import stats

    n, rf = y.shape
    g, gi, gf = y.mean(), y.mean(1), y.mean(0)
    ms_f = n * np.sum((gf - g) ** 2) / (rf - 1)
    ms_i = rf * np.sum((gi - g) ** 2) / (n - 1)
    ms_e = np.sum((y - gi[:, None] - gf[None, :] + g) ** 2) / ((n - 1) * (rf - 1))
    v_b = max(0.0, (ms_f - ms_e) / n)
    v_a = max(0.0, (ms_i - ms_e) / rf)  # image component, printed beside
    v_img = float(np.mean([np.var(y[:, f], ddof=1) / n for f in range(rf)]))
    f05 = float(stats.f.ppf(0.05, rf - 1, (rf - 1) * (n - 1)))
    v_bu = max(0.0, (ms_f / f05 - ms_e) / n)
    omega, omega_u = v_b / v_img, v_bu / v_img
    se = float(np.sqrt(max(ms_f + ms_i - ms_e, 0.0) / (n * rf)))
    t = float(stats.t.ppf(0.975, rf - 1))
    return {"MS_F": float(ms_f), "MS_I": float(ms_i), "MS_E": float(ms_e), "V_b": v_b, "V_a": v_a, "V_img": v_img,
            "F_0.05": f05, "V_b_upper": v_bu, "omega": omega, "omega_upper": omega_u,
            "label": "the fixed-set rows are practically unconditional" if omega_u <= 0.25
            else "conditional on the realised fixed set", "dev_row": {"d": float(g), "se": se, "lo": float(g) - t * se,
                                                                     "hi": float(g) + t * se, "df": rf - 1}}


def components(per: dict) -> tuple[dict, dict]:
    """§7.7a per backbone, and §7.7b where at least two fixed sets exist (y = ret - fix_F)."""
    ms = sorted({k.split("|")[0] for k in per})
    var = {m: draw_variance(per, m, per.get(f"{m}|ret")) for m in ms}
    fx = {}
    for m in ms:
        fk = draw_keys(per, m, "fix_f")
        if len(fk) >= 2 and f"{m}|ret" in per:
            fx[m] = anova_fix(np.array([per[f"{m}|ret"] - per[k] for k in fk]).T)
    return var, fx


# ------------------------------------------------------------------------------------------------ §8 copy bound
def copy_loss(caps: dict, shown: dict, refs: dict, score, n: int, unit: str = UNITS[0]) -> np.ndarray:
    """loss(y; S) = s(y) - s(masked_n(y, S)) per image (ids sorted), the same references and document frequencies;
    the references are never masked. Unit (ii) masks RDRSegmenter words and scores the masked text as segmented."""
    ids = sorted(caps)
    plain = score({i: caps[i] for i in ids}, refs)
    if unit == UNITS[1]:
        sg = score.segment(sorted({caps[i] for i in ids} | {x for i in ids for x in shown[i]}))
        mk = score({i: A.masked(sg[caps[i]], [sg[x] for x in shown[i]], n) or "." for i in ids}, refs, segmented=True)
    else:
        mk = score({i: A.masked(caps[i], shown[i], n) or "." for i in ids}, refs)
    return np.asarray(plain, float) - np.asarray(mk, float)


def kappa(loss_arm: np.ndarray, loss_zs: np.ndarray) -> np.ndarray:
    """κ_q = loss(y_arm; R_q) - loss(y_zs; R_q): the zs caption never saw R_q (the placebo)."""
    return loss_arm - loss_zs


def copy_bound(ds: str, caps: dict, s: dict, r_q: dict, own_rand: dict, refs: dict, score, idx, blind=None) -> dict:
    """caps / s: {'zs','ret','rand'} captions and per-image scores (ids sorted); r_q: the ret run's shown captions;
    own_rand: the rand d0 run's own shown captions; blind: the stored image-blind captions or None. Per unit (i, ii)
    and n = 2, 3, 4 (n = 3 decides): K_ret, L_cp, K_nc with labels; companions K_rand, K_ret - K_nc and the blind
    loss against R_q, descriptive. Tier POST HOC except XM-dev500 (first look)."""
    tier = "first look" if ds == "xm_dev500" else "POST HOC"
    out = {}
    for unit in UNITS:
        res = {}
        for n in (2, 3, 4):
            lz = copy_loss(caps["zs"], r_q, refs, score, n, unit)
            kq = kappa(copy_loss(caps["ret"], r_q, refs, score, n, unit), lz)
            knc = kappa(copy_loss(caps["rand"], r_q, refs, score, n, unit), lz)
            zero = np.zeros_like(kq)
            rows = {"K_ret": pair(kq, zero, idx), "L_cp": pair(np.asarray(s["ret"]) - np.asarray(s["rand"]) - kq, zero, idx),
                    "K_nc": pair(knc, zero, idx)}
            for k, r in rows.items():
                r["label"] = label(r, bool(detected({k: (r["d"], r["p"])})))
            comp = {"K_rand": pair(kappa(copy_loss(caps["rand"], own_rand, refs, score, n, unit),
                                         copy_loss(caps["zs"], own_rand, refs, score, n, unit)), zero, idx),
                    "K_ret_minus_K_nc": pair(kq - knc, zero, idx)}
            if blind is not None:
                comp["blind_loss"] = pair(copy_loss(blind, r_q, refs, score, n, unit), zero, idx)
            for r in comp.values():
                r["label"] = COMPANION
            rows.update(comp)
            for r in rows.values():
                r["tier"], r["tag"] = tier, A.LABEL
            rows["withdrawn"] = rows["K_nc"]["label"] == "REVERSED"
            res[f"n{n}"] = rows
        res["monotonicity check failed"] = res["n4"]["K_ret"]["d"] > res["n2"]["K_ret"]["d"]
        out[unit] = res
    return out


def kit_scorer(kit_b: Path):
    """Stripped CIDEr-D through kit B (score2.kit2: RDRSegmenter, lower-cased), df over the given references.
    score(capt, refs, segmented=True) takes captions already segmented (unit ii); score.segment(texts) -> {text: seg}."""
    import score2 as S2s

    E4, PA, _ptb = S2s.kit2(kit_b)
    seg: dict[str, str] = {}

    def segment(texts) -> dict:
        miss = sorted(set(texts) - seg.keys())
        if miss:
            seg.update(zip(miss, (t.lower() for t in E4.rdr(miss))))
        return seg

    def score(capt: dict, refs: dict, segmented: bool = False) -> np.ndarray:
        ids = sorted(capt)
        sg = segment([x for i in ids for x in refs[i]] + ([] if segmented else [capt[i] for i in ids]))
        cider = E4.Cider({i: [sg[x] for x in refs[i]] for i in ids})
        return np.asarray(cider.per_image({i: " ".join(PA.strip_trailing_punct_tokens(
            (capt[i] if segmented else sg[capt[i]]).split())) for i in ids}), float)
    score.segment = segment
    return score


def blind_run(p: Path, c2_rows: list[dict]) -> dict:
    """§8 companion: a stored image-blind run, admitted only when its sha256 is the run_sha256 that the pinned stage-2
    ledger records for that blind run (STORED_SHA256 holds no blind run and is not changed)."""
    r = json.loads(Path(p).read_text(encoding="utf-8"))
    h = A.sha(p)
    if not any(x.get("arm") == "blind" and x.get("run_id") == r.get("run_id")
               and (x.get("inputs") or {}).get("run_sha256") == h for x in c2_rows):
        raise SystemExit(f"REFUSED: {Path(p).name} is not a blind run of the pinned stage-2 ledger")
    return r


# ------------------------------------------------------------------------------------------------ §7.9 swap (post hoc)
def swap_delta(per: dict, idx: np.ndarray) -> dict:
    """§7.9 post hoc companion on the stored Flickr30K carve cells, per backbone: δ = mean_i {[ret - rand d0] with the
    Flickr30K-train memory - [ret - rand d0] with the full COCO memory}, paired, the two τ_sel beside it."""
    out = {}
    for m in sorted({k.split("|")[0] for k in per}):
        col = {c: per.get(f"{m}|{c}") for c in ("ret", "rand_d0", "ret_f30k", "rand_d0_f30k")}
        if any(v is None for v in col.values()):
            continue
        same, other = col["ret_f30k"] - col["rand_d0_f30k"], col["ret"] - col["rand_d0"]
        zero = np.zeros_like(same)
        rows = {"delta": pair(same, other, idx), "tau_sel_f30k": pair(same, zero, idx), "tau_sel_coco": pair(other, zero, idx)}
        for k, r in rows.items():
            r["label"], r["tier"], r["tag"] = label(r, bool(detected({k: (r["d"], r["p"])}))), SWAP_TIER, A.LABEL
        out[m] = rows
    return out


def length_gaps(runs: list[dict]) -> dict:
    """§7.9 rule L per cell (backbone, memory): |len_ret - len_rand| / len_rand in mean whitespace tokens."""
    ln = {(r["model"], r["spec"]["memory"], r["spec"]["arm"]): float(np.mean([len(c.split()) for c in r["predictions"].values()]))
          for r in runs if r["spec"]["arm"] in ("ret", "rand") and not r["spec"].get("draw")}
    out = {}
    for (m, mem, arm), v in sorted(ln.items()):
        if arm == "ret" and (m, mem, "rand") in ln:
            b = ln[(m, mem, "rand")]
            out[f"{m}|{mem}"] = {"ret": v, "rand": b, "rel_gap": abs(v - b) / b,
                                 "not separated from length": abs(v - b) / b > LENGTH_GAP}
    return out


# ------------------------------------------------------------------------------------------------ §9 sensitivity
def df_resample(cider_cls, rseg: dict, hyps: dict, ids: list[str], rows: np.ndarray) -> dict[str, np.ndarray]:
    """Per arm, the per-position stripped CIDEr-D of one bootstrap resample, document frequencies recomputed over the
    resampled images' references (an image drawn twice counts twice)."""
    u = sorted({ids[j] for j in rows})
    pos = {i: k for k, i in enumerate(u)}
    cid = cider_cls({i: rseg[i] for i in u}, df_refs=[rseg[ids[j]] for j in rows])
    at = [pos[ids[j]] for j in rows]
    return {arm: np.asarray(cid.per_image({i: h[i] for i in u}))[at] for arm, h in hyps.items()}


def primary(sc: dict) -> dict:
    """tau_pair and tau_marg per image or position (draw means as §7.2) from {ret, rand_d<j>, perm_p<j>: scores}."""
    perm = np.mean([sc[k] for k in sorted(sc) if k.startswith("perm_p")], 0)
    rand = np.mean([sc[k] for k in sorted(sc) if k.startswith("rand_d")], 0)
    return {"tau_pair": sc["ret"] - perm, "tau_marg": perm - rand}


def df_sensitivity(cider_cls, rseg: dict, hyps: dict, ids: list[str], idx: np.ndarray) -> tuple[dict, dict]:
    """§9: the primary contrasts with document frequencies recomputed inside the first SENS_B resamples of the set's
    shared index matrix, beside the fixed-df interval over the same resamples. Returns (rows, full-df scores)."""
    full = cider_cls({i: rseg[i] for i in ids})
    sc = {k: np.asarray(full.per_image(h)) for k, h in hyps.items()}
    base, sub = primary(sc), idx[:SENS_B]
    redf = [primary(df_resample(cider_cls, rseg, hyps, ids, rows)) for rows in sub]
    out = {}
    for e, v in base.items():
        rs, fx = np.array([c[e].mean() for c in redf]), v[sub].mean(1)
        (lo, hi), (flo, fhi) = np.percentile(rs, [2.5, 97.5]), np.percentile(fx, [2.5, 97.5])
        out[e] = {"d": float(v.mean()), "lo_df_resampled": float(lo), "hi_df_resampled": float(hi),
                  "lo_df_fixed": float(flo), "hi_df_fixed": float(fhi), "B": SENS_B}
    return out, sc


def arm_key(r: dict) -> str | None:
    sp = r["spec"]
    return {"ret": "ret", "rand": f"rand_d{sp['draw']}", "perm": f"perm_p{sp['draw']}"}.get(sp["arm"])


def dfsens(runs: list[dict], led: list[dict], refs: dict, E4, PA, nominated: list[str]) -> dict:
    """The §9 row on the batch-1 OV-dev-B runs of SENS_MODEL. Its full-df per-image scores must equal the ledger's
    (1e-4), so the row rescores exactly what was scored."""
    by = {arm_key(r): r for r in runs if arm_key(r)}
    if not {"ret", "rand_d0", "rand_d1", "rand_d2", "perm_p1", "perm_p2"} <= set(by):
        return {"status": f"NOT RUN: {SENS_MODEL} batch-1 OV-dev-B arms incomplete ({sorted(by)})"}
    ids = sorted(refs)
    texts = sorted({c for r in by.values() for c in r["predictions"].values()} | {x for i in ids for x in refs[i]})
    seg = dict(zip(texts, (t.lower() for t in E4.rdr(texts))))
    rseg = {i: [seg[x] for x in refs[i]] for i in ids}
    hyps = {k: {i: " ".join(PA.strip_trailing_punct_tokens(seg[r["predictions"][i]].split())) for i in ids}
            for k, r in by.items()}
    rows, sc = df_sensitivity(E4.Cider, rseg, hyps, ids, A.boot_idx(len(ids)))
    for k, r in by.items():
        want = [x for x in led if x.get("run_id") == r["run_id"] and x.get("tau") == "-inf" and x.get("variant") is None]
        if len(want) != 1 or want[0]["per_image"]["ids"] != ids \
                or np.abs(sc[k] - np.array(want[0]["per_image"]["cider_s"])).max() > A.C2_PARITY_TOL:
            raise SystemExit(f"SENSITIVITY PARITY FAIL: {r['run_id']}: the full-df scores differ from the ledger")
    for e, r in rows.items():
        r.update(model=SENS_MODEL, set="ov_dev_b", nominated=f"H_{e[4:]}({SENS_MODEL})" in nominated, batch=B1_NOTE,
                 label="§9 sensitivity row (reference-only document frequencies): reported, no rule", tag=A.LABEL)
    return {"status": "computed", "rows": rows}


# ------------------------------------------------------------------------------------------------ SC5 prompts
def prompt_key(r: dict) -> tuple:
    sp = r["spec"]
    return r["model"], r["dataset"], sp["arm"], 0 if sp["arm"] == "zs" else int(sp["draw"])


def prompt_check(b1: list[Path], refs: list[Path]) -> dict:
    """SC5 (CC-346), v1.2 V2: each '-b1' run's per-image prompt sha256 against every batched block-1 or stored run of
    the same backbone, set, arm and draw (stored runs admitted by their pin). Hashes compared, counts kept."""
    pool: dict[tuple, list[dict]] = {}
    for p in refs:
        r = A.as_run(Path(p))
        pool.setdefault(prompt_key(r), []).append(r)
    out = {"pairs": {}, "no_reference": [], "not_comparable": []}
    for p in b1:
        r = json.loads(Path(p).read_text(encoding="utf-8"))
        mine = r["prompt_sha256"]
        found = pool.get(prompt_key(r), [])
        if not found:
            out["no_reference"].append(r["run_id"])
        for o in found:
            old = o.get("prompt_sha256_per_image") or o.get("prompt_sha256")
            if not isinstance(old, dict):
                out["not_comparable"].append(f"{r['run_id']} | {o['run_id']}")
                continue
            same = sum(old.get(i) == h for i, h in mine.items())
            out["pairs"][f"{r['run_id']} | {o['run_id']}"] = {"compared": len(mine), "equal": same,
                                                               "missing": sum(i not in old for i in mine)}
    out["unequal"] = sorted(k for k, v in out["pairs"].items() if v["equal"] != v["compared"])
    return out


def prompt_gate(pc: dict, n_b1: int) -> None:
    """SC5 stops: a '-b1' prompt that differs from the batched or stored run of its cell (V2), or '-b1' runs with no
    compared pair at all (a check that compared nothing is no check)."""
    if pc["unequal"]:
        raise SystemExit(f"REFUSED: {len(pc['unequal'])} '-b1' runs whose prompts differ from the v1.1 construction (V2)")
    if n_b1 and not pc["pairs"]:
        raise SystemExit("REFUSED: SC5 compared no prompt hash: no '-b1' run has a comparable batched or stored run")


# ------------------------------------------------------------------------------------------------ S1 host stages
def freeze_copy(src: Path, dst: Path) -> None:
    """The host's read-only copy of an output tree (files 0444, folders 0555)."""
    shutil.copytree(src, dst, symlinks=False)
    for p in sorted(dst.rglob("*"), key=lambda q: -len(q.parts)):
        p.chmod(0o555 if p.is_dir() else 0o444)
    dst.chmod(0o555)


def tree_ok(d: Path, sums_sha: str) -> int:
    """S1: the copy's SHA256SUMS is the file the laptop verified (its sha256 from the LOG); every listed file hashes as
    listed except logs/job.log (appended after the sums, CC-346 R7); out/, logs/ and parity/ hold no unlisted file."""
    sums = d / "SHA256SUMS"
    if not sums.is_file() or A.sha(sums) != sums_sha:
        raise SystemExit(f"REFUSED: {sums} is not the SHA256SUMS whose sha256 was logged")
    listed = {n: h for h, n in (ln.split(maxsplit=1) for ln in sums.read_text(encoding="utf-8").splitlines() if ln.strip())}
    have = {str(p.relative_to(d)) for sub in ("out", "logs", "parity") if (d / sub).is_dir()
            for p in (d / sub).rglob("*") if p.is_file() and ".partial" not in p.name}
    if have != set(listed):
        raise SystemExit(f"REFUSED: {d}: {len(have - set(listed))} unlisted and {len(set(listed) - have)} missing files")
    bad = [n for n, h in listed.items() if n != "logs/job.log" and A.sha(d / n) != h]
    if bad:
        raise SystemExit(f"REFUSED: {d}: {len(bad)} files differ from SHA256SUMS, e.g. {bad[:3]}")
    return len(listed)


def stored_files() -> dict[Path, str]:
    """The stored run files pinned in STORED_SHA256 (vectors and lists excluded)."""
    rows = [ln.split(maxsplit=1) for ln in A.RESTORED.read_text().splitlines() if ln.strip()]
    return {Path(p): h for h, p in rows if p.endswith(".preds.json")}


def env_record() -> dict:
    """S1: the scoring environment, written at verify and required unchanged at every later stage: kit B, the pinned
    VnCoreNLP-1.2 jar (score.JAR_SHA256) and its word-segmenter models, Java, Python and its packages."""
    import score as S

    vnc = A.lb.DATA / "vncorenlp"
    jar = vnc / "VnCoreNLP-1.2.jar"
    if not jar.is_file() or A.sha(jar) != S.JAR_SHA256:
        raise SystemExit(f"REFUSED: {jar} is not the pinned VnCoreNLP-1.2 jar ({S.JAR_SHA256[:8]})")
    pkgs = "\n".join(sorted(f"{d.metadata['Name']}=={d.version}" for d in importlib.metadata.distributions()))
    java = subprocess.run(["java", "-version"], capture_output=True, text=True, check=True).stderr.strip()
    return {"python": sys.version.split()[0], "packages_sha256": hashlib.sha256(pkgs.encode()).hexdigest(), "java": java,
            "jar_sha256": S.JAR_SHA256, "kit_b": {p.name: A.sha(p) for p in sorted(KIT.glob("*.py"))},
            "vncorenlp_models": {str(p.relative_to(vnc)): A.sha(p) for p in sorted((vnc / "models").rglob("*")) if p.is_file()}}


def runs_of(tree: Path, m: str, ds: str) -> list[Path]:
    """A verified tree's scoreable runs of one backbone and set (never a re-decode or smoke run)."""
    skip = tuple(f"-{x}.preds.json" for x in ("host50", "rev50", "fwd50", "smoke"))
    return [p for p in sorted((tree / "out").glob(f"at_{m}_{ds}-*.preds.json")) if not p.name.endswith(skip)]


def stored_of(m: str, ds: str) -> list[Path]:
    return sorted(p for p in stored_files() if p.name.split("-")[0].endswith(f"_{m}_{ds}"))


def is_zs(p: Path) -> bool:
    return re.search(r"_(?:ov_dev_[ab]|xm_dev500)-zs[-.]", Path(p).name) is not None


def with_zs(m: str, ds: str, own: list[Path], pool: list[Path]) -> list[Path]:
    """score_set needs one zs per backbone: the call's own zs if it has one, else the first zs of the pool."""
    if any(is_zs(p) for p in own):
        return own
    zs = [p for p in pool if is_zs(p)]
    if not zs:
        raise SystemExit(f"REFUSED: no zs run of {m} on {ds}")
    return own + zs[:1]


def parity_files(w: Path) -> list[Path]:
    return sorted((w / "in/b1/parity").glob("STEP1B0_*.json")) + sorted((w / "in/b/parity").glob("STEP10_*.json"))


def d1_pass(w: Path, models) -> list[str]:
    par = parity(sorted((w / "in/b1/parity").glob("STEP1B0_*.json")))
    return [m for m in models if par.get(m, {}).get("D1") == "PASS"]


def score_call(ds: str, runs: list[Path], ledger: Path, nom: Path | None = None, verdict: Path | None = None) -> None:
    A.cmd_score(argparse.Namespace(set=ds, runs=runs, ledger=ledger, kit_b=KIT, c_lists=CL, refs=None, captions=None,
                                   c2_dir=None, c2_ledger=None, memory=None, nomination=nom, verdict=verdict))


def st_verify(a, w: Path, rec: dict) -> None:
    """Copy the two output trees read-only, check them against the logged sums, the stored pins, the environment,
    SC5 and the §7.1 scoring parity gate (C's six stage-2 OV-dev-B runs against the stage-2 ledger, 1e-4)."""
    for k, src in SRC.items():
        if (src / "RUNNING").exists():
            raise SystemExit(f"REFUSED: {src}/RUNNING exists: never beside a decode job (§6.7)")
        freeze_copy(src, w / "in" / k)
    rec["trees"] = {k: {"sums_sha256": h, "files": tree_ok(w / "in" / k, h)} for k, h in (("b1", a.b1_sums), ("b", a.b_sums))}
    bad = [p.name for p, h in stored_files().items() if not p.is_file() or A.sha(p) != h]
    if bad:
        raise SystemExit(f"REFUSED: {len(bad)} stored runs missing or not as pinned, e.g. {bad[:3]}")
    rec["env"] = env_record()
    b1 = [p for m in OLD3 for ds in A.B1B_N for p in runs_of(w / "in/b1", m, ds)]
    pc = prompt_check(b1, [p for m in OLD3 for ds in A.B1B_N for p in runs_of(w / "in/b", m, ds) + stored_of(m, ds)])
    rec["prompts"] = {"b1_runs": len(b1), "pairs": len(pc["pairs"]), "unequal": pc["unequal"],
                      "no_reference": pc["no_reference"], "not_comparable": pc["not_comparable"]}
    prompt_gate(pc, len(b1))
    parity_7_1(w, rec)


def parity_7_1(w: Path, rec: dict) -> None:
    """§7.1 scoring parity gate: C's six stage-2 OV-dev-B runs re-scored equal the pinned stage-2 ledger (1e-4)."""
    led = w / "led/parity_c2.jsonl"
    score_call("ov_dev_b", [Path(A.C2_DIR) / n for n in A.C2_RUNS], led)
    A.c2_parity(A.read_ledgers([led]), w / "in/stage2_ledger.jsonl")
    rec["parity_7_1"] = {"ledger_sha256": A.sha(led), "stage2_ledger_sha256": A.C2_LEDGER_SHA256, "result": "ok"}


def st_ova(a, w: Path, rec: dict) -> None:
    """V4 (1): batch-1 OV-dev-A of the D1-PASS nominators (with each one's stored zs), then the nomination file."""
    ms = d1_pass(w, NOMINATORS)
    if not ms:
        raise SystemExit("REFUSED: no Tier-A backbone with a D1 PASS: run the stage `close` (V4 release)")
    for m in ms:  # SC4 before any score: an incomplete Tier A is not scored (CC-346 R5)
        have = {arm_key(json.loads(p.read_text(encoding="utf-8"))) for p in runs_of(w / "in/b1", m, "ov_dev_a")}
        if not set(B1_COLS) <= have:
            raise SystemExit(f"REFUSED: {m} lacks the batch-1 OV-dev-A runs {sorted(set(B1_COLS) - have)}; nothing scored")
    led = w / "led/ova.jsonl"
    score_call("ov_dev_a", [p for m in ms for p in with_zs(m, "ov_dev_a", runs_of(w / "in/b1", m, "ov_dev_a"),
                                                          stored_of(m, "ov_dev_a"))], led)
    cmd_nominate(argparse.Namespace(ledger=[led], closed=None, parity=parity_files(w), out=w / "res" / FILES["ova"]))


def st_close(a, w: Path, rec: dict) -> None:
    cmd_nominate(argparse.Namespace(ledger=[], closed=a.reason, parity=[], out=w / "res" / FILES["close"]))


def st_ovb(a, w: Path, rec: dict) -> None:
    """V4 (2): batch-1 OV-dev-B (one look), the verdict (= the summary of both batch-1 sets) and the §9 row."""
    import score2 as S2s

    nf = w / "res" / FILES["ova"]
    if nomination(nf).get("closed"):
        raise SystemExit("REFUSED: 1b was closed (release clause): the next stage is `rest`")
    ms = [m for m in d1_pass(w, OLD3) if runs_of(w / "in/b1", m, "ov_dev_b")]
    led = w / "led/ovb.jsonl"
    score_call("ov_dev_b", [p for m in ms for p in with_zs(m, "ov_dev_b", runs_of(w / "in/b1", m, "ov_dev_b"),
                                                          stored_of(m, "ov_dev_b"))], led, nom=nf)
    cmd_summary(argparse.Namespace(ledger=[w / "led/ova.jsonl", led], nomination=nf, parity=parity_files(w),
                                   out=w / "res" / FILES["ovb"]))
    E4, PA, _ptb = S2s.kit2(KIT)
    q = [json.loads(p.read_text(encoding="utf-8")) for p in runs_of(w / "in/b1", SENS_MODEL, "ov_dev_b")
         if SENS_MODEL in ms]
    sens = dfsens(q, A.read_ledgers([led]), A.score_refs("ov_dev_b", A.C.load_lists(CL)), E4, PA,
                  nomination(nf)["nominated"])
    out = w / "res/DFSENS.json"
    out.write_text(json.dumps({"label": A.LABEL, "registration": REG12, **sens}, indent=1, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    rec["dfsens_sha256"] = A.sha(out)


def st_rest(a, w: Path, rec: dict) -> None:
    """V4 (3), after the logged verdict or the release: XM-dev500 at batch size 1, then every batched block-1 output with
    the stored runs of its set, then the summary of every ledger."""
    nf, vf = w / "res" / FILES["ova"], w / "res" / FILES["ovb"]
    vf = vf if vf.is_file() else None
    b1, b = w / "in/b1", w / "in/b"
    ms = [m for m in d1_pass(w, OLD3) if runs_of(b1, m, "xm_dev500")]
    if ms:
        score_call("xm_dev500", [p for m in ms for p in with_zs(m, "xm_dev500", runs_of(b1, m, "xm_dev500"),
                                                               runs_of(b, m, "xm_dev500") + stored_of(m, "xm_dev500"))],
                   w / "led/xm_b1.jsonl", nf, vf)
    for ds in A.B1B_N:
        own = {m: runs_of(b, m, ds) + stored_of(m, ds) for m in OLD3}
        runs = [p for m in OLD3 if own[m] for p in with_zs(m, ds, own[m], [])]
        if runs:
            score_call(ds, runs, w / f"led/bat_{ds}.jsonl", nf, vf)
    cmd_summary(argparse.Namespace(ledger=sorted(p for p in (w / "led").glob("*.jsonl") if p.name != "parity_c2.jsonl"),
                                   nomination=nf, parity=parity_files(w), out=w / "res" / FILES["rest"]))


def st_posthoc(a, w: Path, rec: dict) -> None:
    """Block-0 rows on stored outputs, POST HOC (except κ on XM-dev500, first look): the copy bound per set and backbone
    (§8, both units, blind companion where a blind run is staged and admitted), and the swap δ (§7.9) where the carve
    ledgers are staged."""
    rec["copy_bound"] = {}
    blinds = sorted((w / "in/blind").glob("*.preds.json"))
    for ds in ("ov_dev_b", "xm_dev500"):
        for m in OLD3:
            arms = {}
            for p in stored_of(m, ds) + runs_of(w / "in/b", m, ds):
                sp = A.as_run(p)["spec"]
                if sp["arm"] in ("zs", "ret") or (sp["arm"] == "rand" and sp["draw"] == 0):
                    arms.setdefault(sp["arm"], p)
            if set(arms) != {"zs", "ret", "rand"}:
                rec["copy_bound"][f"{ds}|{m}"] = f"NOT RUN: arms present {sorted(arms)}"
                continue
            bl = [p for p in blinds if f"_{m}_{ds}-blind" in p.name]  # admitted by the stage-2 ledger in cmd_copybound
            out = w / f"res/COPYBOUND_{ds}_{m}.json"
            cmd_copybound(argparse.Namespace(set=ds, zs=arms["zs"], ret=arms["ret"], rand=arms["rand"], kit_b=KIT,
                                             c_lists=CL, c2_ledger=w / "in/stage2_ledger.jsonl",
                                             c2_run=Path(A.C2_DIR) / "c2_qwen25vl_7b_ov_dev_b-ret-k8-first-T1.preds.json",
                                             blind=bl[0] if bl else None, out=out))
            rec["copy_bound"][f"{ds}|{m}"] = A.sha(out)
    carve = w / "in/carve"
    if not (carve / "carve_coco.jsonl").is_file():
        rec["swap"] = "NOT RUN: carve ledgers not staged"
        return
    coco, f30k = carve / "carve_coco.jsonl", carve / "carve_f30k.jsonl"
    if A.sha(coco) != A.T1_CARVE_LEDGER_SHA256:
        raise SystemExit(f"REFUSED: {coco} is not the tier-1 carve ledger 4ced15b4")
    per, _p, ids = A.set_columns(A.read_ledgers([coco, f30k]), "f30k_carve", "en")
    lruns = sorted((carve / "runs").glob("*.preds.json"))
    rec["swap"] = {"inputs": {p.name: A.sha(p) for p in [coco, f30k, *lruns]},
                   "rows": strip(swap_delta(per, A.boot_idx(len(ids)))),
                   "length": length_gaps([json.loads(p.read_text(encoding="utf-8")) for p in lruns])}


# ------------------------------------------------------------------------------------------------ block 3
def k7_open() -> None:
    """K7 (v1.1 §10.1): at and after 2026-11-16 12:00 VN every unfinished step is NOT RUN (CC-368 ruling 6)."""
    if CLOCK() >= K7_TS:
        raise SystemExit(f"REFUSED: K7 ({K7_UTC} = 2026-11-16 12:00 VN) has passed: every unfinished step is NOT RUN")


def test_named(paths) -> list[str]:
    """Binding 1: paths whose file name names a test set ('test' between separators, or a registered test-set key)."""
    return sorted(str(p) for p in paths if TEST_NAME.search(Path(p).name))


def b3_id(s: dict) -> str:
    """The run id the block3 job writes for one step of c_attr.b3_steps, from the decoder's own id functions."""
    a = argparse.Namespace(set=s["set"], memory="vi", batch1=True, redecode=None, limit=None, variant=s["arm"],
                           model=s["runner"], arm=s["arm"], k=8, order="first" if s["arm"] == "ret_img" else None,
                           tpl="T1", draw=0)
    return A.lmcap_run_id(a) if s["runner"] == "lmcap" else A.run_id_of(a)


def b3_runs(w: Path, runner: str, ds: str, arms=None) -> list[Path]:
    """The verified copy's block-3 runs of one runner and set that exist, in run order (D1 files are never scored)."""
    return [p for s in A.b3_steps((runner,)) if s["set"] == ds and (arms is None or s["arm"] in arms)
            for p in [w / "in/b3/out" / f"{b3_id(s)}.preds.json"] if p.is_file()]


def full_set(ids, ds: str) -> None:
    """Binding 4 and §10.2: rows come from full sets only."""
    if ids is None or len(ids) != A.B3_N[ds]:
        raise SystemExit(f"REFUSED: {ds} rows over {len(ids or [])} images, not the full set of {A.B3_N[ds]}")


def b3_rows(per: dict, ds: str, idx: np.ndarray) -> dict[str, dict]:
    """v1.1 §7.10 rows on one set, each a family of m = 1 (§7.4): LMCap τ_sel, τ_pair, τ_marg and the Qwen2.5-VL
    image-caption-pair τ_sel (ret_img - rand_img d0). Labels of erratum E6 and CC-368 O8, O9, N1; no "split of a known
    τ_sel" (O8). A row whose two arms are not both present is absent (§10.2). Masked3 columns never enter."""
    rows = {}
    for m, est, x, y in B3_EST:
        if x in per and y in per:
            r = {**pair(per[x], per[y], idx), "model": m, "estimand": est, "arms": f"{x} - {y}", "m": 1}
            r["label"] = label(r, bool(detected({est: (r["d"], r["p"])})))
            r.update(tier=B3_XM if ds == "xm_dev500" else B3_TIER[f"{m}|{est}"], wording=E6[m], decodes=B3_DECODES,
                     batch=B3_BATCH, tag=A.LABEL)
            if m != "lmcap":
                r["beside"] = TEXT_SEL[ds]  # §7.10 "beside the text-only τ_sel": a pointer, no difference row
            rows[f"{m}|{est}"] = r
    return rows


def k5_verdict(row: dict | None) -> str:
    """K5 mechanically from the registered m = 1 rule (θ̂ >= +2.0 and p <= 0.025); NOT RUN without a row."""
    if row is None:
        return "NOT RUN"
    return "DETECTED" if detected({"k5": (row["d"], row["p"])}) else "NOT DETECTED"


def b3_pins(w: Path) -> dict[Path, str]:
    """Scoring inputs with their pins: the two dev reference files (CC-362), the v1.2 nomination file (the V4 (1) gate
    of `score` on OV-dev-B) and the two stored Qwen2.5-VL zs runs (score_set needs one zs per backbone and set)."""
    st = stored_files()
    return {**{A.lb.DATA / k: h for k, h in B3_REFS.items()}, w / "in" / B3_NOM: B3_NOM_SHA256,
            **{p: st[p] for ds in A.B3_N for p in stored_of("qwen25vl_7b", ds) if is_zs(p)}}


def d1_b3(w: Path) -> dict:
    return parity(sorted((w / "in/b3/parity").glob("STEP3_*.json")))


def st_b3verify(a, w: Path, rec: dict) -> None:
    """Run doc §8 items 1 and 4: no test-set name, the read-only copy of /root/outputs/c_attr_b3 against the logged
    sums, the pinned inputs, the environment, the D1 verdicts (STEP3) and the §7.1 parity gate. Scores no block-3 run."""
    if (SRC_B3 / "RUNNING").exists():
        raise SystemExit(f"REFUSED: {SRC_B3}/RUNNING exists: the block-3 decode job is still running (§6.7)")
    pins = b3_pins(w)
    tests = test_named([*SRC_B3.rglob("*"), *pins])
    if tests:
        raise SystemExit(f"REFUSED: {len(tests)} test-set names, e.g. {tests[:2]} (binding 1)")
    freeze_copy(SRC_B3, w / "in/b3")
    rec["trees"] = {"b3": {"sums_sha256": a.b3_sums, "files": tree_ok(w / "in/b3", a.b3_sums)}}
    off = [p.name for p, h in pins.items() if not p.is_file() or A.sha(p) != h]
    if off:
        raise SystemExit(f"REFUSED: {len(off)} inputs missing or not as pinned: {off}")
    rec["pins"] = {str(p): h for p, h in pins.items()}
    rec["env"] = env_record()
    rec["d1"] = d1_b3(w)
    parity_7_1(w, rec)


def st_b3k5(a, w: Path, rec: dict) -> None:
    """CC-368 ruling 12: the K5 verdict in its own file, before any other block-3 row is computed. Only the two K5 arms
    are scored (lmcap_ri, lmcap_rand on OV-dev-B). LMCap D1 not PASS: K5 NOT RUN (run doc §2), nothing scored. A K5 arm
    missing beside a D1 PASS (a CAP STOP or JOB STOP before step 2): refused, no row until a judge line (run doc §4)."""
    d1 = d1_b3(w)
    res = {"label": A.LABEL, "registration": REG_B3, "rule": K5_RULE, "d1": d1, "row": None}
    if d1.get("lmcap", {}).get("D1") == "PASS":
        runs = b3_runs(w, "lmcap", "ov_dev_b", ("ri", "rand"))
        if len(runs) != 2:
            raise SystemExit(f"REFUSED: K5 NOT RUN: {len(runs)} of its 2 arms exist; no block-3 row is scored until a "
                             "judge line (run doc §4)")
        led = w / "led/k5.jsonl"
        score_call("ov_dev_b", runs, led, nom=w / "in" / B3_NOM)
        per, _p, ids = A.set_columns(A.read_ledgers([led]), "ov_dev_b", "vi")
        full_set(ids, "ov_dev_b")
        res["row"] = strip(b3_rows(per, "ov_dev_b", A.boot_idx(len(ids))).get("lmcap|tau_sel"))
        res["inputs"] = {**{p.name: A.sha(p) for p in runs}, "k5.jsonl": A.sha(led)}
    else:
        res["reason"] = "LMCap D1 not PASS: its block-3 steps were NOT RUN (run doc §2; v1.2 V3)"
    res["verdict"] = k5_verdict(res["row"])
    res["consequence"] = K5_OUT[res["verdict"]]
    (w / "res" / FILES["b3k5"]).write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    rec["k5"] = res["verdict"]


def st_b3rest(a, w: Path, rec: dict) -> None:
    """After the logged K5 file: the other registered rows (LMCap τ_pair, τ_marg on OV-dev-B, every row on XM-dev500,
    the image-caption-pair τ_sel on both sets), each runner only with its D1 PASS. The OV-dev-B LMCap τ_sel is read
    back from the K5 ledger and must equal the K5 file. K5 not DETECTED or NOT RUN: every row is stamped uninterpreted."""
    kf = w / "res" / FILES["b3k5"]
    k5 = json.loads(kf.read_text(encoding="utf-8"))
    d1 = d1_b3(w)
    ok = [r for r in B3_RUNNERS if d1.get(r, {}).get("D1") == "PASS"]
    stray = [p.name for r in B3_RUNNERS if r not in ok for ds in A.B3_N for p in b3_runs(w, r, ds)]
    if stray:
        raise SystemExit(f"REFUSED: block-3 runs without a D1 PASS: {stray} (v1.2 V3, V8)")
    res = {"label": A.LABEL, "registration": REG_B3, "k5": k5["verdict"], "k5_sha256": A.sha(kf),
           "k5_consequence": k5["consequence"], "d1": d1, "alpha_one_sided": ALPHA, "sesoi": SESOI, "sets": {},
           "not_run": []}
    for ds in A.B3_N:
        lm = b3_runs(w, "lmcap", ds, ("perm",) if ds == "ov_dev_b" else None) if "lmcap" in ok else []
        qw = b3_runs(w, "qwen25vl_7b", ds) if "qwen25vl_7b" in ok else []
        ledgers = [w / "led/k5.jsonl"] if ds == "ov_dev_b" and k5["row"] else []
        if lm or qw:
            led = w / f"led/b3_{ds}.jsonl"
            score_call(ds, lm + (with_zs("qwen25vl_7b", ds, qw, stored_of("qwen25vl_7b", ds)) if qw else []), led,
                       nom=w / "in" / B3_NOM if ds == "ov_dev_b" else None)
            ledgers.append(led)
        rows = {}
        if ledgers:
            per, _p, ids = A.set_columns(A.read_ledgers(ledgers), ds, "vi")
            full_set(ids, ds)
            rows = b3_rows(per, ds, A.boot_idx(len(ids)))
        for r in rows.values():
            if k5["verdict"] != "DETECTED":
                r["interpretation"] = UNINTERPRETED
        res["sets"][ds] = {"n": A.B3_N[ds] if rows else 0, "rows": strip(rows)}
        res["not_run"] += [f"{ds}|{m}|{e}" for m, e, _x, _y in B3_EST if f"{m}|{e}" not in rows]
    mine = res["sets"]["ov_dev_b"]["rows"].get("lmcap|tau_sel") or {}
    if k5["row"] and any(mine.get(c) != k5["row"][c] for c in ("d", "p", "label")):
        raise SystemExit("REFUSED: the OV-dev-B LMCap τ_sel differs from the logged K5 file")
    (w / "res" / FILES["b3rest"]).write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    rec["rows"] = {ds: sorted(s["rows"]) for ds, s in res["sets"].items()}


STAGE = {"verify": st_verify, "ova": st_ova, "close": st_close, "ovb": st_ovb, "rest": st_rest, "posthoc": st_posthoc,
         "b3verify": st_b3verify, "b3k5": st_b3k5, "b3rest": st_b3rest}


def cmd_stage(a) -> None:
    """S1 (CC-338, CC-346): the registered scoring order on the host, one stage per call. Every stage after verify
    needs --prev = the sha256 of the previous stage's file as logged by the operator; each writes one file, prints its
    sha256 and stops. Order: verify -> ova | close -> ovb -> rest -> posthoc; `rest` follows ovb's verdict or, when no
    verdict exists, the empty v1.2 nomination file (the release clause; the score gate then checks it is empty).
    Block 3 (CC-368 ruling 12), in its own work folder: b3verify -> b3k5 -> b3rest, each refused at and after K7."""
    b3 = a.stage in B3_STAGES
    if b3:
        k7_open()  # K7 binds every block-3 scoring stage
    w = Path(a.work or (WORK_B3 if b3 else WORK))
    res = w / "res"
    out = res / FILES[a.stage]
    if out.exists():
        raise SystemExit(f"REFUSED: {out.name} exists; a stage runs once")
    if a.stage not in ("verify", "b3verify"):
        name = PREV[a.stage] if a.stage != "rest" or (res / PREV["rest"]).is_file() else FILES["ova"]
        prev = res / name
        if not prev.is_file() or A.sha(prev) != a.prev:
            raise SystemExit(f"REFUSED: {name} is not the file whose sha256 was logged (--prev): STOP (V4 order)")
        if env_record() != json.loads((res / FILES["verify"]).read_text(encoding="utf-8"))["env"]:
            raise SystemExit("REFUSED: the scoring environment differs from the one recorded at verify")
    (w / "led").mkdir(parents=True, exist_ok=True)
    res.mkdir(exist_ok=True)
    rec = {"label": A.LABEL, "registration": REG_B3 if b3 else REG12, "stage": a.stage, "prev_sha256": a.prev,
           "utc": A.lb.utc()}
    STAGE[a.stage](a, w, rec)
    rf = out if a.stage in ("verify", "b3verify", "posthoc") else res / f"STAGE_{a.stage}.json"
    rf.write_text(json.dumps(rec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"STAGE {a.stage} DONE: {out.name} sha256 {A.sha(out)}; record {rf.name} sha256 {A.sha(rf)}"
          f"{'; DFSENS.json sha256 ' + rec['dfsens_sha256'] if 'dfsens_sha256' in rec else ''}; write them to the LOG, then STOP")


# ------------------------------------------------------------------------------------------------ CLI
def strip(o):
    return {k: strip(v) for k, v in o.items() if k != "_bm"} if isinstance(o, dict) else o


def cmd_score(a) -> None:
    A.cmd_score(a)  # the V4 gates run inside (SC1)


def cmd_nominate(a) -> None:
    if a.closed:  # v1.2 V4 release clause: 1b ends with no verdict; the OPS line "1b closed: <reason>" logs its hash
        rec = {"label": A.LABEL, "registration": REG12, "nominated": [], "closed": a.closed}
        Path(a.out).write_text(json.dumps(rec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"empty v1.2 nomination file; {a.out} sha256 {A.sha(a.out)} (write it to the LOG first)")
        return
    if not a.ledger:
        raise SystemExit("nominate: --ledger or --closed")
    led = A.read_ledgers(a.ledger)
    if ovb_perm_scored(led) or any(Path(a.ledger[0]).parent.glob("*ov_dev_b*perm*")):
        raise SystemExit("REFUSED: an OV-dev-B score of a new run exists; the nomination comes first (§7.5)")
    led = split_b1(led)[0]  # V1: no nomination rule on batched outputs
    per, _p, ids = A.set_columns(led, "ov_dev_a", "vi")
    if not per:
        raise SystemExit("REFUSED: no batch-1 OV-dev-A rows; an empty v1.2 file comes only from --closed")
    par = parity(a.parity)
    d1 = [m for m in NOMINATORS if par.get(m, {}).get("D1") == "PASS"]
    stray = sorted({k.split("|")[0] for k in per} - set(d1))
    if not d1 or stray:
        raise SystemExit(f"REFUSED: batch-1 OV-dev-A rows of {stray} without a D1 PASS, or no D1-PASS nominator (V3)")
    miss = [f"{m}|{c}" for m in d1 for c in B1_COLS if f"{m}|{c}" not in per]
    if miss:  # SC4: an early nomination on one backbone would lock out the other
        raise SystemExit(f"REFUSED: OV-dev-A columns missing {miss}; the nomination waits for every D1-PASS nominator")
    rows = set_rows(per, "ov_dev_a", A.boot_idx(len(ids)))
    apply_labels(rows, "ov_dev_a", {})
    rec = {"label": A.LABEL, "registration": REG12, "batch": B1_NOTE, "parity": par, "nominators_d1_pass": d1,
           "rule": "95% lower bound >= +2.0 on OV-dev-A (c_t1.advance)", "note": SPLIT,
           "nominated": nominate(rows), "rows": strip({k: v for k, v in rows.items() if k.split("|")[0] in NOMINATORS})}
    Path(a.out).write_text(json.dumps(rec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"nominated {rec['nominated'] or 'nothing'}; {a.out} sha256 {A.sha(a.out)} (write it to the LOG first)")


def cmd_summary(a) -> None:
    led, batched = split_b1(dedup(A.read_ledgers(a.ledger)))
    nom = nomination(a.nomination)["nominated"] if a.nomination else []
    par = parity(a.parity)
    res = {"label": A.LABEL, "registration": REG12, "alpha_familywise_one_sided": ALPHA, "sesoi": SESOI,
           "nominated": nom, "nomination_sha256": A.sha(a.nomination) if a.nomination else None, "parity": par,
           "sets": {}, "batched": {}}
    for ds in ("ov_dev_a", "ov_dev_b", "xm_dev500", "f30k_val"):
        per, _p, ids = A.set_columns(batched, ds, A.SETS[ds])
        if per:  # V1 / CC-340 1d: batched and stored rows, no family, labelled; CC-338 S2 reads STEP10
            rows = set_rows(per, ds, A.boot_idx(len(ids)))
            apply_labels(rows, ds, {})
            for r in rows.values():
                if r["model"] in OLD3 and "A1" not in par.get(r["model"], {}):
                    raise SystemExit(f"REFUSED: no STEP10 record for {r['model']} (CC-338 S2)")
                r["batch"] = BATCHED
                if par.get(r["model"], {}).get("host_parity") == "FAIL":
                    r["host"] = HOST_FB
            var, fx = components(per)  # §7.7: the fixed sets f1-f4 exist only batched (V5)
            res["batched"][ds] = {"n": len(ids), "rows": strip(rows), "variance": var, "fixed_set": fx}
        per, _p, ids = A.set_columns(led, ds, A.SETS[ds])
        if not per:
            continue
        no_d1 = sorted({k.split("|")[0] for k in per} - {m for m, v in par.items() if v.get("D1") == "PASS"})
        if no_d1:
            raise SystemExit(f"REFUSED: batch-1 rows of {no_d1} without a D1 PASS (V3)")
        idx = A.boot_idx(len(ids))  # one index matrix per set
        rows = set_rows(per, ds, idx)
        fam = {}
        if ds == "ov_dev_b":
            fam = {"registered (§7.5)": family_keys(nom),
                   "S-BB (§7.6)": [f"{m}|tau_sel" for m in sorted({k.split("|")[0] for k in per}) if m not in OLD3]}
        apply_labels(rows, ds, fam)
        for r in rows.values():  # V6
            r["batch"] = B1_NOTE
            if r.get("estimand") == "tau_sel" and ds in KNOWN_SUM:
                r["note"] = SEL_B1
        if ds == "ov_dev_b" and a.nomination and not nom:  # batch-1 nomination only (CC-340 1c)
            res["no_claim"] = "no claim was nominated on OV-dev-A"
        var, fx = components(per)
        res["sets"][ds] = {"n": len(ids), "rows": strip(rows), "variance": var, "fixed_set": fx}
    Path(a.out).write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({ds: {k: v["label"] for k, v in s["rows"].items()} for ds, s in res["sets"].items()},
                     ensure_ascii=False))


def cmd_copybound(a) -> None:
    """§8 on stored outputs (block 0 step 0.3), both units; the scoring parity gate first (§7.1)."""
    import stage2 as ST2

    clists = A.C.load_lists(a.c_lists)
    refs = ST2.references2(a.set, clists)
    score = kit_scorer(a.kit_b)
    q = A.stored_run(Path(a.c2_run))
    if A.sha(a.c2_ledger) != A.C2_LEDGER_SHA256:
        raise SystemExit("not the stage-2 ledger")
    old = [json.loads(x) for x in Path(a.c2_ledger).read_text(encoding="utf-8").splitlines() if x.strip()]
    ref_b = ST2.references2("ov_dev_b", clists)
    want = next(r for r in old if r.get("run_id") == q["run_id"] and r.get("tau") == "-inf" and r.get("variant") is None)
    got = score(q["predictions"], ref_b)
    if want["per_image"]["ids"] != sorted(q["predictions"]) or np.abs(got - np.array(want["per_image"]["cider_s"])).max() > A.C2_PARITY_TOL:
        raise SystemExit("SCORING PARITY FAIL (§7.1): no copy-bound row")
    runs = {k: A.as_run(Path(p)) for k, p in (("zs", a.zs), ("ret", a.ret), ("rand", a.rand))}
    caps = {k: r["predictions"] for k, r in runs.items()}
    ids = sorted(caps["ret"])
    blind = {i: blind_run(a.blind, old)["predictions"][i] for i in ids} if a.blind else None
    mem = A.C.memory_captions(clists)
    src = A.C.DATASETS[a.set]["src"]
    r_q = {i: [A.C.shown(mem[c], src) for c in runs["ret"]["exemplars"][i]] for i in ids}
    own = {i: [A.C.shown(mem[c], src) for c in runs["rand"]["exemplars"][i]] for i in ids}
    s = {k: score(caps[k], refs) for k in ("ret", "rand")}
    res = {"label": A.LABEL, "set": a.set, "inputs": {k: r["_sha256"] for k, r in runs.items()},
           "blind": A.sha(a.blind) if a.blind else "NOT RUN: no admitted blind run staged",
           "bound": strip(copy_bound(a.set, caps, s, r_q, own, refs, score, A.boot_idx(len(ids)), blind))}
    Path(a.out).write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"copy bound {a.set}: {a.out} sha256 {A.sha(a.out)}")


# ------------------------------------------------------------------------------------------------ self-test
def selftest() -> None:
    ok, rng = [], np.random.default_rng(11)
    n = 600
    base = rng.normal(40, 10, n)
    rand = [base + rng.normal(0, 4, n) for _ in range(3)]
    perm = [r + 0 for r in (rand[0], rand[1])]
    per = {"qwen25vl_7b|zs": base - 5, "qwen25vl_7b|rand_d0": rand[0], "qwen25vl_7b|rand_d1": rand[1],
           "qwen25vl_7b|rand_d2": rand[2], "qwen25vl_7b|perm_p1": perm[0], "qwen25vl_7b|perm_p2": perm[1]}
    per["qwen25vl_7b|ret"] = np.mean(perm, 0) + 3  # registered planted case: ret = perm + 3, perm = rand
    calls = []
    real = A.boot_idx
    A.boot_idx = lambda k: calls.append(k) or real(k)
    try:
        idx = A.boot_idx(n)
        rows = set_rows({**per, "qwen25vl_7b|rand_d2": np.mean(perm, 0) * 3 - rand[0] - rand[1]}, "ov_dev_b", idx)
    finally:
        A.boot_idx = real
    assert len(calls) == 1, "one index matrix per set"
    assert abs(rows["qwen25vl_7b|tau_pair"]["d"] - 3) < 1e-9 and abs(rows["qwen25vl_7b|tau_marg"]["d"]) < 1e-9, \
        "ret = perm + 3 and perm = rand give tau_pair = 3, tau_marg = 0"
    r2 = set_rows(per, "ov_dev_b", idx)
    assert abs(r2["qwen25vl_7b|tau_sel"]["d"] - (per["qwen25vl_7b|ret"] - np.mean(rand, 0)).mean()) < 1e-9, \
        "rand is the mean over the draws"
    bm = {k: r2[f"qwen25vl_7b|{k}"]["_bm"] for k in ("tau_sel", "tau_marg", "tau_pair")}
    assert np.allclose(bm["tau_sel"], bm["tau_marg"] + bm["tau_pair"]), "replicate-wise identity: one shared matrix"
    pp = pair(base, base - 3, idx)
    assert pp["hi"] - pp["lo"] < 1e-9 and abs(pp["d"] - 3) < 1e-9, "paired bootstrap"
    m3 = set_rows({**per, **{f"{k}_m3": v + 50 for k, v in per.items() if k != "qwen25vl_7b|zs"}}, "ov_dev_b", idx)
    assert all(abs(m3[k]["d"] - r2[k]["d"]) < 1e-12 and m3[k].get("R") == r2[k].get("R") for k in r2), \
        "the masked3 ('_m3') columns never enter a draw mean"
    ok.append("estimands (planted ret = perm + 3, perm = rand), draw mean, one index matrix, paired, identity, '_m3' apart")
    a3 = ALPHA / 3
    t = {"a": (2.0, a3), "b": (2.0, ALPHA / 2), "c": (2.0, ALPHA)}
    assert detected(t) == {"a", "b", "c"}, "boundary (θ̂ = 2.0; p = α_j): both inclusive"
    assert detected({**t, "a": (1.999, a3)}) == set(), "a point below +2.0 fails (and ends the step-down)"
    assert detected({"a": (5, 0.004), "b": (5, 0.011), "c": (5, 0.02)}) == {"a", "b", "c"}
    assert detected({"a": (5, 0.009), "b": (5, 0.010), "c": (5, 0.012)}) == set(), "Holm: 0.009 > 0.025 / 3"
    assert detected({"a": (5, 0.005), "b": (5, 0.013), "c": (5, 0.014)}) == {"a"}, "step-down stops at the first failure"
    assert detected({"a": (5, 0.012), "b": (5, 0.02), "c": (5, 0.03)}) == set(), "alpha is 0.025, not 0.05"
    assert detected({"x": (2.0, 0.025)}) == {"x"} and detected({"x": (2.0, 0.02500001)}) == set(), "m = 1"
    ok.append("Holm toy cases at one-sided 0.025, boundary (θ̂ = 2.0; p = α_j)")
    agree, k50 = 0, 0  # m = 1: the p rule equals '95% percentile lower bound > 0' unless exactly 50 of 2,000 means <= 0
    for s in range(300):
        g = np.random.default_rng(100 + s)
        x = g.normal(g.uniform(-0.5, 2.5), 8, 300)
        st = pair(x, np.zeros(300), real(300))
        kneg = int(np.sum(st["_bm"] <= 0))
        if kneg == 50:
            k50 += 1
            continue
        assert (st["p"] <= ALPHA) == (st["lo"] > 0), (s, kneg)
        agree += 1
    edge = summary(1.0, np.array([-1.0] * 49 + [-0.001] + [1.0] * 1950))
    assert edge["lo"] > 0 and edge["p"] > ALPHA, "50 means <= 0: lower bound > 0 but p = 51/2001; the p rule decides"
    assert detected({"x": (5.0, edge["p"])}) == set()
    ok.append(f"m = 1 equals the 95% lower-bound rule off the 50-means edge ({agree} random cases, {k50} at the edge)")
    lab = lambda **kw: label({"d": 0, "lo": -1, "hi": 1, "lo90": -1, "hi90": 1, **kw}, False)  # noqa: E731
    assert lab() == "NEGLIGIBLE" and lab(hi90=2.0) == "UNRESOLVED" and lab(lo90=-2.0) == "UNRESOLVED"
    assert lab(hi=-0.01, hi90=-0.5) == "REVERSED" and lab(hi=0.0) == "NEGLIGIBLE"
    ok.append("labels at their boundaries (REVERSED < 0, NEGLIGIBLE open at ±2.0)")
    rows3 = {**set_rows(per, "ov_dev_b", idx), **{k.replace("qwen25vl_7b", "internvl3_8b"): v for k, v in
                                                 set_rows(per, "ov_dev_b", idx).items()}}
    apply_labels(rows3, "ov_dev_b", {"registered (§7.5)": ["qwen25vl_7b|tau_pair", "internvl3_8b|tau_pair"]})
    assert all(rows3[f"{m}|{e}"]["note"] == SPLIT for m in ("qwen25vl_7b", "internvl3_8b") for e in ("tau_pair", "tau_marg"))
    assert rows3["qwen25vl_7b|tau_pair"]["m"] == 2 and rows3["qwen25vl_7b|tau_sel"]["m"] == 1
    assert rows3["qwen25vl_7b|tau_pair"]["label"] == "DETECTED" and "note" not in rows3["qwen25vl_7b|tau_sel"]
    xr = set_rows(per, "xm_dev500", idx)
    apply_labels(xr, "xm_dev500", {})
    assert "note" not in xr["qwen25vl_7b|tau_pair"], "the X2 words belong to OV-dev-A and OV-dev-B rows"
    ok.append(f"X2 label '{SPLIT}' on OV-dev-A / OV-dev-B τ_pair and τ_marg rows; family sizes")
    ra = set_rows(per, "ov_dev_a", idx)
    assert nominate(ra) == ["H_pair(qwen25vl_7b)"] and family_keys(["H_pair(qwen25vl_7b)"]) == ["qwen25vl_7b|tau_pair"]
    assert ovb_perm_scored([{"dataset": "ov_dev_b", "arm": "perm"}]) and not ovb_perm_scored([{"dataset": "ov_dev_a", "arm": "perm"}])
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        led = Path(tmp) / "ledger_ov_dev_b.jsonl"
        led.write_text(json.dumps({"dataset": "ov_dev_b", "arm": "perm", "model": "qwen25vl_7b"}) + "\n")
        try:
            cmd_nominate(argparse.Namespace(ledger=[led], closed=None, parity=[], out=Path(tmp) / "n.json"))
            raise AssertionError("nomination must be refused")
        except SystemExit as e:
            assert "REFUSED" in str(e)
        try:
            run = Path(tmp) / "run.json"
            run.write_text(json.dumps({"spec": {"arm": "perm"}}))
            v4_gate(argparse.Namespace(set="ov_dev_b", runs=[run], nomination=None, verdict=None))
            raise AssertionError("OV-dev-B perm scoring before the nomination must be refused")
        except SystemExit as e:
            assert "REFUSED" in str(e)
    ok.append("nomination (95% lower bound >= +2.0), refused once an OV-dev-B perm score exists; OV-dev-B perm needs it")
    selftest_v12(per)
    ok.append("v1.2: v11 file refused by name and content, V4 gates (1) and (3) and release, '-b1' batch size, "
              "batch-1 rows apart from batched rows, labels (batch 1, batched, τ_sel, host parity), D1 / STEP10 needed")
    pv = draw_variance(per, "qwen25vl_7b", per["qwen25vl_7b|ret"])
    assert abs(pv["sigma2_w"] - np.mean(np.var(np.array(rand), axis=0, ddof=1))) < 1e-9
    nn, rf, vb = 925, 5, 4.0
    g = np.random.default_rng(5)
    y = g.normal(0, 1, (400, 1)) * 0 + g.normal(2, np.sqrt(vb), (1, rf)) + g.normal(0, 10, (400, rf))
    est = [anova_fix(g.normal(0, 3, (nn, 1)) + g.normal(2, np.sqrt(vb), (1, rf)) + g.normal(0, 10, (nn, rf)))["V_b"]
           for _ in range(400)]
    assert abs(np.mean(est) - vb) < 0.5, f"planted V_b recovered ({np.mean(est):.2f} vs {vb})"
    af = anova_fix(y)
    assert abs(af["omega"] - af["V_b"] / af["V_img"]) < 1e-12 and af["V_img"] > 0
    assert abs(anova_fix(g.normal(0, 1, (925, 5)))["F_0.05"] - 0.178) < 0.002, "F quantile of §7.7b (about 0.178)"
    ok.append("ANOVA: planted V_b recovered, omega = V_b / V_img, F quantile 0.178 at n = 925")
    selftest_copy(ok)
    selftest_score2(ok)
    selftest_b3(ok)
    print("c_attr_score selftest ok: " + "; ".join(ok))


def toy_scorer():
    """Unigram recall against the references; segmentation joins 'con mèo' and 'trên ghế' into words (unit ii)."""
    def segment(texts) -> dict:
        return {t: t.lower().replace("con mèo", "con_mèo").replace("trên ghế", "trên_ghế") for t in texts}

    def score(capt: dict, refs: dict, segmented: bool = False) -> np.ndarray:
        r = {i: [segment([x])[x] for x in refs[i]] for i in capt}
        c = {i: capt[i] if segmented else segment([capt[i]])[capt[i]] for i in capt}
        return np.array([np.mean([len(set(c[i].split()) & set(x.split())) for x in r[i]]) for i in sorted(capt)], float)
    score.segment = segment
    return score


def selftest_copy(ok: list) -> None:
    """§8 (both units, companions, blind admission) and §7.9 (swap δ, rule L) on planted strings."""
    toy = toy_scorer()
    refs = {"a": ["một con mèo nằm trên ghế"], "b": ["hai người đi trên phố"], "c": ["con mèo ngủ say"]}
    shown = {"a": ["con mèo nằm trên ghế sofa"], "b": ["người đi trên phố đông"], "c": ["con mèo đen"]}
    own = {"a": ["chiếc xe đỏ"], "b": ["cây xanh"], "c": ["mèo ngủ say trên ghế"]}
    caps = {"zs": {"a": "một con mèo trên ghế", "b": "hai người đi bộ", "c": "mèo ngủ"},
            "ret": {"a": "con mèo nằm trên ghế", "b": "người đi trên phố", "c": "con mèo ngủ"},
            "rand": {"a": "một con mèo", "b": "hai người trên phố", "c": "mèo"}}
    lz = copy_loss(caps["zs"], shown, refs, toy, 2)
    assert np.all(kappa(lz, lz) == 0), "κ of a zs run against itself is 0"
    lr = copy_loss(caps["ret"], shown, refs, toy, 2)
    assert list(lz) == [2.0, 2.0, 0.0] and list(lr) == [3.0, 4.0, 1.0], "losses with the references unmasked"
    assert list(kappa(lr, lz)) == [1.0, 2.0, 1.0], "κ subtracts the zs placebo"
    assert list(copy_loss({"x": "đen ngủ"}, {"x": ["chó đen to"]}, {"x": ["chó đen to ngủ"]}, toy, 2)) == [0.0], \
        "the references are never masked (a masked reference would lose 'đen')"
    one = {"x": "mèo nằm trên"}
    syl = copy_loss(one, {"x": ["con mèo nằm trên ghế"]}, {"x": ["mèo nằm trên đệm"]}, toy, 3, UNITS[0])
    wrd = copy_loss(one, {"x": ["con mèo nằm trên ghế"]}, {"x": ["mèo nằm trên đệm"]}, toy, 3, UNITS[1])
    assert list(syl) == [3.0] and list(wrd) == [0.0], "unit (ii): word 3-grams of the segmented texts (con_mèo is a word)"
    s = {k: toy(caps[k], refs) for k in ("ret", "rand")}
    blind = {"a": "con mèo nằm", "b": "hai người", "c": "con mèo đen"}
    cb = copy_bound("ov_dev_b", caps, s, shown, own, refs, toy, A.boot_idx(3), blind)
    x = cb[UNITS[0]]["n2"]
    xm = copy_bound("xm_dev500", caps, s, shown, own, refs, toy, A.boot_idx(3))
    assert x["K_ret"]["tier"] == "POST HOC" and xm[UNITS[1]]["n3"]["K_ret"]["tier"] == "first look"
    assert "blind_loss" not in xm[UNITS[0]]["n3"] and "blind_loss" in cb[UNITS[1]]["n3"]
    knc = kappa(copy_loss(caps["rand"], shown, refs, toy, 2), lz)
    assert abs(x["K_ret"]["d"] - np.mean(kappa(lr, lz))) < 1e-12 and abs(x["K_nc"]["d"] - np.mean(knc)) < 1e-12
    assert abs(x["K_ret_minus_K_nc"]["d"] - (x["K_ret"]["d"] - x["K_nc"]["d"])) < 1e-12, "companion K_ret - K_nc"
    assert abs(x["blind_loss"]["d"] - np.mean(copy_loss(blind, shown, refs, toy, 2))) < 1e-12, "blind loss against R_q"
    assert x["K_rand"]["label"] == x["blind_loss"]["label"] == COMPANION and x["K_ret"]["label"] != COMPANION
    assert set(cb) == set(UNITS) and isinstance(cb[UNITS[1]]["monotonicity check failed"], bool)
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        bp = Path(tmp) / "blind.json"
        bp.write_text(json.dumps({"run_id": "c2_qwen25vl_7b_ov_dev_b-blind-k8-first-T1", "predictions": blind}))
        row = {"run_id": "c2_qwen25vl_7b_ov_dev_b-blind-k8-first-T1", "arm": "blind", "inputs": {"run_sha256": A.sha(bp)}}
        assert blind_run(bp, [row])["predictions"] == blind
        try:
            blind_run(bp, [{**row, "inputs": {"run_sha256": "0" * 64}}])
            raise AssertionError("a blind run not pinned by the stage-2 ledger must be refused")
        except SystemExit as e:
            assert "REFUSED" in str(e)
    ok.append("copy bound: κ placebo, references never masked, unit (ii) on RDR words, companions K_rand, K_ret - K_nc "
              "and blind (descriptive, against R_q), blind admitted by the stage-2 ledger only, POST HOC except XM-dev500")
    g = np.random.default_rng(3)
    base = g.normal(30, 5, 400)
    sw = {"qwen25vl_7b|ret": base + 2, "qwen25vl_7b|rand_d0": base, "qwen25vl_7b|ret_f30k": base + 7,
          "qwen25vl_7b|rand_d0_f30k": base + 1}
    sd = swap_delta(sw, A.boot_idx(400))["qwen25vl_7b"]
    assert abs(sd["delta"]["d"] - 4) < 1e-9 and abs(sd["tau_sel_f30k"]["d"] - 6) < 1e-9 and sd["delta"]["tier"] == SWAP_TIER, \
        "swap δ = τ_sel with the Flickr30K-train memory minus τ_sel with the COCO memory"
    lg = length_gaps([{"model": "q", "spec": {"memory": mem, "arm": arm, "draw": 0}, "predictions": {"1": cap}}
                      for mem, arm, cap in (("coco", "ret", "a b c d e f g h i j k l"), ("coco", "rand", "a b c d e f g h i j"),
                                            ("f30k", "ret", "a b c d e f g h i j k"), ("f30k", "rand", "a b c d e f g h i j"))])
    assert lg["q|coco"]["not separated from length"] and not lg["q|f30k"]["not separated from length"], \
        "rule L: a gap above 0.10 (0.2) is flagged, a gap of exactly 0.10 is not"
    ok.append("swap δ = (ret - rand)[Flickr30K memory] - (ret - rand)[COCO memory], POST HOC; rule L above 0.10")


def selftest_v12(per: dict) -> None:
    """Addendum v1.2 (CC-340 W1) and CC-346 SC2-SC4: planted files and ledgers only."""
    import tempfile
    ns = argparse.Namespace

    def refused(f, *args, **kw) -> str:
        try:
            f(*args, **kw)
        except SystemExit as e:
            return str(e)
        raise AssertionError(f"{f.__name__} must refuse")

    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        good = {"registration": REG12, "nominated": ["H_pair(qwen25vl_7b)"]}
        files = {"v11": (V11_NAME, good), "k1": ("other.json", {"registration": "C_ATTR_DEV_PREREG_v1_1.md 44f81329",
                                                                  "claims": [], "reason": "K1 fired"}),
                 "ok": ("c_attr_nomination.json", good), "empty": ("empty.json", {**good, "nominated": []}),
                 "verdict": ("verdict.json", {"registration": REG12, "sets": {"ov_dev_b": {}}, "nomination_sha256": "x"})}
        for k, (name, rec) in files.items():
            (t / k).mkdir()
            files[k] = t / k / name
            files[k].write_text(json.dumps(rec))
        assert "REFUSED" in refused(nomination, files["v11"]), "the v11 file is refused by name"
        assert "REFUSED" in refused(nomination, files["k1"]), "the v11 content is refused under any name"
        assert nomination(files["ok"])["nominated"] == good["nominated"]
        run = lambda rid, bs=1: {"run_id": rid, "spec": {"arm": "ret", "batch_size": bs}}  # noqa: E731
        rp = {}
        for k, r in {"b1": run("at_q_ov_dev_b-ret-k8-first-T1-mvi-b1"), "bad": run("at_q_ov_dev_b-ret-mvi-b1", 4),
                     "bat": run("at_q_ov_dev_b-perm-k8-first-T1-p1-mvi", 8), "batA": run("at_q_ov_dev_a-perm-p1-mvi", 8)}.items():
            rp[k] = t / f"{k}.json"
            rp[k].write_text(json.dumps(r))
        sc = lambda s, k, **kw: v4_gate(ns(**{"set": s, "runs": [rp[k]], "nomination": None, "verdict": None, **kw}))  # noqa: E731
        assert "REFUSED" in refused(sc, "ov_dev_b", "b1"), "V4 (1): batch-1 OV-dev-B before the nomination"
        assert "REFUSED" in refused(sc, "ov_dev_b", "b1", nomination=files["v11"]), "V1: the v11 file is no licence"
        sc("ov_dev_b", "b1", nomination=files["ok"])
        assert "batch size 1" in refused(sc, "ov_dev_a", "bad"), "SC2: a '-b1' run must be a batch-1 decode"
        assert "REFUSED" in refused(sc, "ov_dev_a", "batA", nomination=files["ok"]), "V4 (3): batched before the verdict"
        assert "REFUSED" in refused(sc, "ov_dev_b", "bat", nomination=files["ok"])
        sc("ov_dev_a", "batA", verdict=files["verdict"])
        sc("ov_dev_a", "batA", nomination=files["empty"])  # release clause
        cli = subprocess.run([sys.executable, "-X", "utf8", "-I", "-B", str(A.ATTR / "c_attr.py"), "score", "--set",
                              "ov_dev_b", "--runs", str(rp["b1"]), "--ledger", str(t / "cli.jsonl")],
                             capture_output=True, text=True, timeout=600)
        assert cli.returncode and "(V4)" in cli.stderr and not (t / "cli.jsonl").exists(), \
            f"SC1: `c_attr.py score` itself refuses OV-dev-B before the nomination ({cli.stderr.strip()[-160:]})"
        ids = [str(i) for i in range(len(per["qwen25vl_7b|ret"]))]
        led = t / "ledger.jsonl"
        lines = []
        for ds in ("ov_dev_a", "ov_dev_b"):
            for key, v in per.items():
                m, arm = key.split("|")
                base = {"dataset": ds, "model": m, "arm": arm.split("_")[0], "tau": "-inf",
                        "draw": int(arm[-1]) if "_" in arm else 0, "per_image": {"ids": ids, "cider_s": list(v)}}
                lines.append({**base, "run_id": f"at_{key}-{ds}-b1"})
                if arm.startswith(("ret", "perm")):  # batched ret = perm + 10, so a mixed contrast is seen
                    vv = list(v + 7) if arm == "ret" else list(v)
                    lines.append({**base, "run_id": f"at_{key}-{ds}", "per_image": {"ids": ids, "cider_s": vv}})
        led.write_text("".join(json.dumps(x) + "\n" for x in lines))
        pf = []
        for m, rec in (("qwen25vl_7b", {"A1": "FAIL", "host_parity": "FAIL"}), ("qwen25vl_7b", {"D1": "PASS"}),
                       ("qwen25vl_7b", {"D1": "FAIL"}), ("internvl3_8b", {"D1": "PASS"})):
            pf.append(t / f"p{len(pf)}.json")
            pf[-1].write_text(json.dumps({"model": m, **rec}))
        assert parity([pf[1], pf[2]])["qwen25vl_7b"]["D1"] == parity([pf[2], pf[1]])["qwen25vl_7b"]["D1"] == "FAIL", \
            "SC3: a D1 FAIL on either host stands, in either file order"
        out = t / "s.json"
        assert "D1" in refused(cmd_summary, ns(ledger=[led], nomination=files["ok"], parity=pf[:1], out=out)), "SC2"
        assert "STEP10" in refused(cmd_summary, ns(ledger=[led], nomination=files["ok"], parity=pf[1:2], out=out)), "SC2"
        assert "REFUSED" in refused(cmd_summary, ns(ledger=[led], nomination=files["v11"], parity=pf[:2], out=out))
        cmd_summary(ns(ledger=[led], nomination=files["ok"], parity=pf[:2], out=out))
        s = json.loads(out.read_text())
        r1, rb = s["sets"]["ov_dev_b"]["rows"], s["batched"]["ov_dev_b"]["rows"]
        assert abs(r1["qwen25vl_7b|tau_pair"]["d"] - 3) < 1e-9 and abs(rb["qwen25vl_7b|tau_pair"]["d"] - 10) < 1e-9, \
            "batch-1 contrasts use batch-1 rows only"
        assert all(r["batch"] == B1_NOTE for r in r1.values()) and all(r["batch"] == BATCHED for r in rb.values())
        assert r1["qwen25vl_7b|tau_sel"]["note"] == SEL_B1 and rb["qwen25vl_7b|tau_pair"]["host"] == HOST_FB
        assert r1["qwen25vl_7b|tau_pair"]["family"] and not rb["qwen25vl_7b|tau_pair"]["family"], "no family on batched rows"
        dup = t / "dup.jsonl"
        dup.write_text(json.dumps({**lines[0], "per_image": {"ids": ids, "cider_s": [0.0] * len(ids)}}) + "\n")
        assert "disagree" in refused(cmd_summary, ns(ledger=[led, dup], nomination=files["ok"], parity=pf[:2], out=out))
        only_batched = t / "batched_a.jsonl"
        only_batched.write_text("".join(json.dumps(x) + "\n" for x in lines
                                        if x["dataset"] == "ov_dev_a" and not is_b1(x["run_id"])))
        assert "REFUSED" in refused(cmd_nominate, ns(ledger=[only_batched], closed=None, parity=pf[:2], out=out)), \
            "V1: no nomination rule on batched rows"
        b1a = t / "b1_a.jsonl"
        b1a.write_text("".join(json.dumps(x) + "\n" for x in lines if x["dataset"] == "ov_dev_a" and is_b1(x["run_id"])))
        assert "missing" in refused(cmd_nominate, ns(ledger=[b1a], closed=None, parity=pf[1:2] + pf[3:], out=out)), \
            "SC4: a D1-PASS nominator without its four OV-dev-A columns blocks the nomination"
        assert "D1" in refused(cmd_nominate, ns(ledger=[b1a], closed=None, parity=pf[2:3], out=out)), \
            "V3: no nomination from rows of a backbone without a D1 PASS"
        both = t / "b1_both.jsonl"
        both.write_text(b1a.read_text() + "".join(json.dumps({**x, "model": "internvl3_8b", "run_id": x["run_id"].replace(
            "qwen25vl_7b", "internvl3_8b")}) + "\n" for x in lines if x["dataset"] == "ov_dev_a" and is_b1(x["run_id"])))
        assert "internvl3_8b" in refused(cmd_nominate, ns(ledger=[both], closed=None, parity=pf[1:2], out=out)), \
            "V3: rows of a backbone without a D1 PASS beside a D1-PASS nominator"
        cmd_nominate(ns(ledger=[b1a], closed=None, parity=pf[1:2], out=out))
        assert json.loads(out.read_text())["nominated"] == ["H_pair(qwen25vl_7b)"]
        cmd_nominate(ns(ledger=[], closed="D1 failed for both Tier-A backbones", parity=[], out=t / "rel.json"))
        assert released(ns(verdict=None, nomination=t / "rel.json")), "release clause: the empty v1.2 file"


def selftest_score2(ok: list) -> None:
    """CC-346: SC1 (the gate inside c_attr.cmd_score), SC5, S3, S1 (tree, stages, host placement) and the real
    score -> ledger -> nominate -> summary chain on planted runs (only the data readers and the segmenter replaced)."""
    import tempfile
    import types
    ns = argparse.Namespace
    import score as S

    E4, PA = S.kit(KIT)  # kit B, sha-pinned: the CIDEr-D of every score
    saved = {k: sys.modules.get(k) for k in ("score", "stage2")}
    sys.modules["score"] = types.SimpleNamespace(references=lambda ds, cl: ("stage-1", ds))
    sys.modules["stage2"] = types.SimpleNamespace(references2=lambda ds, cl: ("stage-2", ds))
    try:
        assert A.score_refs("ov_dev_a", {}) == ("stage-1", "ov_dev_a") and A.score_refs("ov_dev_b", {})[0] == "stage-2", \
            "OV-dev-A references come from C's stage-1 reader (stage 2 refuses OV-dev-A)"
    finally:
        for k, v in saved.items():
            if v is None:
                sys.modules.pop(k, None)
            else:
                sys.modules[k] = v
    # §9 sensitivity row: planted references whose n-gram document frequencies change with the resample
    ids = [f"i{j:02d}" for j in range(12)]
    words = ["mèo", "chó", "xe", "cây", "nhà", "hoa"]
    rseg = {i: [f"con {words[j % 6]} nằm trên ghế", f"một {words[(j + 1) % 6]} đứng gần {words[j % 3]}"]
            for j, i in enumerate(ids)}
    hyps = {"ret": {i: rseg[i][0] for i in ids}, "rand_d0": {i: "con mèo" for i in ids},
            "rand_d1": {i: "một chó" for i in ids}, "rand_d2": {i: "xe" for i in ids},
            "perm_p1": {i: rseg[i][1] for i in ids}, "perm_p2": {i: "con nhà nằm" for i in ids}}
    idx = A.boot_idx(len(ids))
    same = df_resample(E4.Cider, rseg, hyps, ids, np.arange(len(ids)))
    full = E4.Cider({i: rseg[i] for i in ids})
    assert all(np.allclose(same[k], full.per_image(h)) for k, h in hyps.items()), "identity resample = the set's own df"
    rows = np.array([0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    dup = df_resample(E4.Cider, rseg, hyps, ids, rows)
    want = E4.Cider({f"{j:02d}": rseg[ids[r]] for j, r in enumerate(rows)})
    assert np.allclose(dup["ret"], want.per_image({f"{j:02d}": hyps["ret"][ids[r]] for j, r in enumerate(rows)})), \
        "df recomputed over the resample, an image drawn twice counted twice"
    sens, sc = df_sensitivity(E4.Cider, rseg, hyps, ids, idx)
    base = primary(sc)
    assert np.isclose(np.percentile(base["tau_pair"][idx[:SENS_B]].mean(1), 2.5), sens["tau_pair"]["lo_df_fixed"]), \
        "the fixed-df interval uses the set's shared index matrix (first 200 rows)"
    assert not np.isclose(sens["tau_pair"]["lo_df_resampled"], sens["tau_pair"]["lo_df_fixed"]), "df actually recomputed"
    e4 = types.SimpleNamespace(Cider=E4.Cider, rdr=lambda ts: list(ts))
    pa = types.SimpleNamespace(strip_trailing_punct_tokens=lambda t: t)
    runs = [{"run_id": f"r_{k}", "spec": {"arm": k.split("_")[0], "draw": int(k[-1]) if "_" in k else 0},
             "predictions": {i: hyps[k][i] for i in ids}} for k in hyps]
    led = [{"run_id": f"r_{k}", "tau": "-inf", "per_image": {"ids": ids, "cider_s": list(np.round(sc[k], 4))}} for k in hyps]
    refs = rseg
    got = dfsens(runs, led, refs, e4, pa, ["H_pair(qwen25vl_7b)"])
    assert got["rows"]["tau_pair"]["nominated"] and not got["rows"]["tau_marg"]["nominated"]
    led[0]["per_image"]["cider_s"][0] += 1
    try:
        dfsens(runs, led, refs, e4, pa, [])
        raise AssertionError("§9 row on scores other than the ledger's must stop")
    except SystemExit as e:
        assert "PARITY" in str(e)
    assert dfsens(runs[:-1], led, refs, e4, pa, [])["status"].startswith("NOT RUN")
    ok.append("§9 row: df recomputed in 200 resamples of the shared matrix (duplicates counted), fixed-df beside, "
              "equal to the ledger at full df; OV-dev-A references from the stage-1 reader")
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        selftest_tree(t / "tree")
        selftest_chain(t / "chain", E4)
        selftest_stage(t / "stage")
    ok.append("S1: 444 copy against the logged sums (job.log alone exempt, no unlisted file), stage order by the logged "
              "sha, once per stage, same environment, host placement allowed by the isolation hook; SC5 prompt hashes; "
              "SC1 gate in c_attr.cmd_score; the real score -> nominate -> summary chain ('_m3', dedup, one zs per call)")
    ok.append("block 3 stages on a planted tree: verify (sums, RUNNING, test-set names, pins, parity), K5 first from "
              "its two arms only, rest with the K5 row read back and checked, LMCap D1 FAIL gives K5 NOT RUN and "
              "uninterpreted Qwen2.5-VL rows, a missing K5 arm and runs without a D1 PASS refused")


def selftest_tree(t: Path) -> None:
    src = t / "src"
    for f, txt in (("out/at_q_ov_dev_a-ret-mvi-b1.preds.json", "{}"), ("logs/job.log", "x\n"), ("parity/D1_q.json", "{}")):
        (src / f).parent.mkdir(parents=True, exist_ok=True)
        (src / f).write_text(txt)
    (src / "SHA256SUMS").write_text("".join(f"{A.sha(src / f)}  {f}\n" for f in
                                            ("logs/job.log", "out/at_q_ov_dev_a-ret-mvi-b1.preds.json", "parity/D1_q.json")))
    (src / "logs/job.log").write_text("x\nJOB DONE\n")  # appended after the sums (R7)
    h = A.sha(src / "SHA256SUMS")
    freeze_copy(src, t / "c1")
    assert tree_ok(t / "c1", h) == 3 and not (t / "c1/out").stat().st_mode & 0o222
    for name, change in (("sums", lambda d: None), ("file", lambda d: (d / "parity/D1_q.json").write_text("{ }")),
                         ("extra", lambda d: (d / "out/x.preds.json").write_text("{}"))):
        d = t / f"c_{name}"
        shutil.copytree(src, d)
        change(d)
        try:
            tree_ok(d, "0" * 64 if name == "sums" else h)
            raise AssertionError(f"tree check must refuse ({name})")
        except SystemExit as e:
            assert "REFUSED" in str(e)
    for p in [t / "c1", *(t / "c1").rglob("*")]:
        p.chmod(0o755)  # writable again, so the temporary folder can be removed
    cfg = A.iso_config(t / "ncs", t / "outputs", [], set())
    assert A.iso_denied(str(WORK).replace("/root", str(t)) + "/in/b1/out/x.preds.json", cfg) is None and \
        A.iso_denied(t / "outputs/c_attr_b1/out/x.preds.json", cfg) is None and \
        A.iso_denied(t / "outputs/c_attr_score/x", cfg), "the work folder lies outside /root/outputs (isolation hook)"


def selftest_stage(t: Path) -> None:
    global env_record
    res = t / "res"
    res.mkdir(parents=True)
    (res / "VERIFY.json").write_text(json.dumps({"env": {"x": 1}}))
    real_env, ran = env_record, []
    env_record = lambda: {"x": 1}  # noqa: E731
    real_ova = STAGE["ova"]
    STAGE["ova"] = lambda a, w, rec: ran.append(a.stage) or (w / "res/c_attr_nomination.json").write_text("{}")
    try:
        for prev in (None, "0" * 64):
            try:
                cmd_stage(argparse.Namespace(stage="ova", work=t, prev=prev))
                raise AssertionError("a stage without the logged sha256 of the previous file must stop")
            except SystemExit as e:
                assert "--prev" in str(e)
        env_record = lambda: {"x": 2}  # noqa: E731
        try:
            cmd_stage(argparse.Namespace(stage="ova", work=t, prev=A.sha(res / "VERIFY.json")))
            raise AssertionError("a changed environment must stop")
        except SystemExit as e:
            assert "environment" in str(e)
        env_record = lambda: {"x": 1}  # noqa: E731
        cmd_stage(argparse.Namespace(stage="ova", work=t, prev=A.sha(res / "VERIFY.json")))
        assert ran == ["ova"]
        try:
            cmd_stage(argparse.Namespace(stage="close", work=t, prev=A.sha(res / "VERIFY.json"), reason="planted"))
            raise AssertionError("a stage runs once (ova and close write the same file)")
        except SystemExit as e:
            assert "once" in str(e)
    finally:
        env_record, STAGE["ova"] = real_env, real_ova
    (res / "c_attr_nomination.json").unlink()
    (res / "VERDICT.json").write_text("{}")
    try:
        cmd_stage(argparse.Namespace(stage="rest", work=t, prev=A.sha(res / "VERIFY.json")))
        raise AssertionError("rest follows the logged verdict when one exists")
    except SystemExit as e:
        assert "VERDICT.json" in str(e), "rest follows the logged verdict when one exists"


def selftest_chain(t: Path, E4) -> None:
    """The stages ova, ovb and rest on a planted work tree: the unstubbed c_attr.cmd_score (kit B CIDEr-D, score_set,
    X2 rows), nominate, the verdict, the §9 row and the summary. Replaced: references, memory captions, the RDR segmenter
    and the list of stored runs only."""
    import score2 as S2s
    ns = argparse.Namespace
    ids = [f"i{j:02d}.jpg" for j in range(24)]
    noun, verb, place = ["con mèo", "con chó", "chiếc xe", "cái cây"], ["nằm", "đứng", "chạy", "ngồi"], ["ghế", "sân", "đường", "cỏ"]
    refs = {i: [f"{noun[j % 4]} đang {verb[(j // 4) % 4]} trên {place[(j // 2) % 4]}",
                f"một {noun[j % 4]} {verb[(j // 4) % 4]} gần {place[(j // 2) % 4]}"] for j, i in enumerate(ids)}
    caps = {f"c{j}": {"openviic": f"một bức ảnh số {j}", "ktvic": f"ảnh {j}"} for j in range(4)}
    real = (A.score_refs, A.C.memory_captions, S2s.kit2)

    def kit2(folder):
        e4, pa, ptb = real[2](folder)
        e4.rdr = lambda ts: [re.sub(r"([.,])", r" \1", x) for x in ts]
        return e4, pa, ptb
    global stored_files, env_record

    def refused(f, *args) -> str:
        try:
            f(*args)
        except SystemExit as e:
            return str(e)
        raise AssertionError(f"{getattr(f, '__name__', f)} must refuse")
    A.score_refs, A.C.memory_captions, S2s.kit2 = (lambda ds, cl: refs), (lambda cl: caps), kit2
    w = t
    for d in ("in/b1/out", "in/b1/parity", "in/b/out", "in/b/parity", "stored", "c2", "led", "res"):  # led, res: cmd_stage
        (w / d).mkdir(parents=True)

    def run(m, ds, arm, draw, cap, where, b1=True, k=8, rid=None):  # stored zs: c1_; C's stage 2: c2_; else at_
        if not rid:
            tag = {"rand": f"-d{draw}", "perm": f"-p{draw}"}.get(arm, "")
            rid = (f"at_{m}_{ds}-zs-b1" if b1 else f"c1_{m}_{ds}-zs") if arm == "zs" else \
                f"at_{m}_{ds}-{arm}-k{k}-first-T1{tag}-mvi" + ("-b1" if b1 else "")
        p = w / where / f"{rid}.preds.json"
        p.write_text(json.dumps({"schema": A.SCHEMA, "run_id": rid, "model": m, "dataset": ds, "lang": "vi",
                                 "spec": {"arm": arm, "img_examples": False, "k": 0 if arm == "zs" else k,
                                          "order": "first" if arm in ("ret", "perm") else None,
                                          "tpl": None if arm == "zs" else "T1", "draw": draw,
                                          "memory": None if arm == "zs" else "vi", "tau": "-inf", "redecode": None,
                                          "batch_size": 1 if b1 else 8},
                                 "exemplars": {i: ["c0", "c1"] for i in ids}, "predictions": {i: cap(i) for i in ids},
                                 "hit_max": {i: False for i in ids}, "n_tokens": {i: 9 for i in ids},
                                 "prompt_sha256": {i: "a" * 64 for i in ids}}, ensure_ascii=False))
        return p
    q = "qwen25vl_7b"
    good, generic = (lambda i: refs[i][0]), (lambda i: "một bức ảnh")
    arms = lambda ds, draws: [run(q, ds, "ret", 0, good, "in/b1/out"),  # noqa: E731
                              *(run(q, ds, "rand", d, generic, "in/b1/out") for d in draws),
                              run(q, ds, "perm", 1, generic, "in/b1/out"), run(q, ds, "perm", 2, generic, "in/b1/out")]
    for m, rec, where in ((q, {"D1": "PASS"}, "in/b1/parity/STEP1B0"), ("internvl3_8b", {"D1": "FAIL"}, "in/b1/parity/STEP1B0"),
                          (q, {"A1": "FAIL", "host_parity": "PASS"}, "in/b/parity/STEP10")):
        (w / f"{where}_{m}.json").write_text(json.dumps({"model": m, **rec}))
    real_stored, real_env, real_c2, real_src = stored_files, env_record, (A.C2_DIR, A.C2_RUNS, A.C2_LEDGER_SHA256), dict(SRC)
    try:
        arms("ov_dev_a", (0,))
        ovb_runs = arms("ov_dev_b", (0, 1, 2))
        za, zb = run(q, "ov_dev_a", "zs", 0, generic, "stored", b1=False), run(q, "ov_dev_b", "zs", 0, generic, "stored", b1=False)
        stored_files = lambda: {p: A.sha(p) for p in (za, zb)}  # noqa: E731
        run(q, "ov_dev_a", "perm", 1, generic, "in/b/out", b1=False)  # a batched block-1 output
        st_ova(ns(), w, {})
        nf = w / "res" / FILES["ova"]
        assert json.loads(nf.read_text())["nominated"] == ["H_pair(qwen25vl_7b)"], "planted: ret far above perm"
        kw = dict(kit_b=KIT, c_lists=CL, refs=None, captions=None, c2_dir=None, c2_ledger=None, memory=None, verdict=None)
        try:
            A.cmd_score(ns(set="ov_dev_b", runs=ovb_runs + [zb], ledger=w / "x.jsonl", nomination=None, **kw))
            raise AssertionError("V4 (1) in c_attr.cmd_score")
        except SystemExit as e:
            assert "(V4)" in str(e) and not (w / "x.jsonl").exists(), "V4 (1) in c_attr.cmd_score"
        try:
            A.cmd_score(ns(set="ov_dev_b", runs=ovb_runs + [zb, run(q, "ov_dev_b", "zs", 0, generic, "stored")],
                           ledger=w / "x.jsonl", nomination=nf, **kw))
            raise AssertionError("two zs runs of one backbone in one score call")
        except SystemExit as e:
            assert "two zs" in str(e), "two zs runs of one backbone in one score call"
        st_ovb(ns(), w, {})
        vf = w / "res" / FILES["ovb"]
        v = json.loads(vf.read_text())["sets"]["ov_dev_b"]["rows"]
        assert v[f"{q}|tau_pair"]["R"] == 3 and v[f"{q}|tau_pair"]["D"] == 2 and v[f"{q}|tau_pair"]["family"], \
            "draw means over the decoded draws only (the X2 '_m3' rows of the ledger stay apart)"
        assert v[f"{q}|tau_pair"]["label"] == "DETECTED" and v[f"{q}|tau_sel"]["note"] == SEL_B1
        sens = json.loads((w / "res/DFSENS.json").read_text())
        assert sens["status"] == "computed" and sens["rows"]["tau_pair"]["nominated"], "§9 row at the ovb stage"
        st_rest(ns(), w, {})
        s = json.loads((w / "res" / FILES["rest"]).read_text())
        assert "ov_dev_a" in s["batched"] and s["sets"]["ov_dev_b"]["rows"] == json.loads(vf.read_text())["sets"]["ov_dev_b"]["rows"], \
            "the stored zs scored in two calls enters once; batched rows apart"
        # S1 verify on the planted trees (SRC, the stored pins, the environment and C's stage-2 runs replaced)
        for k in ("b1", "b"):
            d = w / "in" / k
            (d / "logs").mkdir()
            (d / "logs/job.log").write_text("JOB DONE\n")
            fs = sorted(str(p.relative_to(d)) for sub in ("out", "logs", "parity") for p in (d / sub).rglob("*") if p.is_file())
            (d / "SHA256SUMS").write_text("".join(f"{A.sha(d / f)}  {f}\n" for f in fs))
        sums = {k: A.sha(w / "in" / k / "SHA256SUMS") for k in ("b1", "b")}
        c2 = [run(q, "ov_dev_b", arm, 0, cap, "c2", b1=False, rid=f"c2_{q}_ov_dev_b-{arm}") for arm, cap in (("zs", generic), ("ret", good))]
        score_call("ov_dev_b", c2, w / "c2/stage2_ledger.jsonl")
        A.C2_DIR, A.C2_RUNS, A.C2_LEDGER_SHA256 = str(w / "c2"), {p.name: "planted" for p in c2}, A.sha(w / "c2/stage2_ledger.jsonl")
        SRC.update(b1=w / "in/b1", b=w / "in/b")
        env_record = lambda: {"x": 1}  # noqa: E731

        def verify(name):
            vw = w / name
            (vw / "in").mkdir(parents=True)
            (vw / "led").mkdir()
            shutil.copy(w / "c2/stage2_ledger.jsonl", vw / "in/stage2_ledger.jsonl")
            rec = {}
            st_verify(ns(b1_sums=sums["b1"], b_sums=sums["b"]), vw, rec)
            return rec
        rec = verify("vw_ok")
        assert rec["trees"]["b1"]["files"] == 13 and rec["prompts"]["pairs"] == 1 and rec["parity_7_1"]["result"] == "ok", \
            f"verify on planted trees ({rec['trees']}, {rec['prompts']})"
        (w / "in/b1/RUNNING").write_text("")
        assert "RUNNING" in refused(verify, "vw_running"), "verify never runs beside a decode job"
        (w / "in/b1/RUNNING").unlink()
        good_pins, stored_files = stored_files, (lambda: {za: "0" * 64})
        assert "stored runs" in refused(verify, "vw_pins"), "verify checks every stored pin"
        stored_files, A.C2_LEDGER_SHA256 = good_pins, "0" * 64
        assert "stage-2 ledger" in refused(verify, "vw_parity"), "verify runs the §7.1 parity gate"
        assert "differ" in refused(prompt_gate, {"unequal": ["x"], "pairs": {"x": {}}}, 1), "SC5: unequal prompts stop"
        assert "compared no" in refused(prompt_gate, {"unequal": [], "pairs": {}}, 3), "SC5: a check comparing nothing stops"
        prompt_gate({"unequal": [], "pairs": {}}, 0)
        data = A.lb.DATA
        (w / "ncs/vncorenlp").mkdir(parents=True)
        (w / "ncs/vncorenlp/VnCoreNLP-1.2.jar").write_text("not the jar")
        A.lb.DATA = w / "ncs"
        try:
            assert "jar" in refused(real_env), "the VnCoreNLP-1.2 jar is pinned"
        finally:
            A.lb.DATA = data
        # stage pre-conditions on a second planted work tree
        w5 = w / "w5"
        for d in ("in/b1/out", "in/b1/parity", "in/carve", "led", "res"):
            (w5 / d).mkdir(parents=True)
        (w5 / "in/b1/parity/STEP1B0_qwen25vl_7b.json").write_text(json.dumps({"model": q, "D1": "FAIL"}))
        assert "no Tier-A backbone" in refused(st_ova, ns(), w5, {}) and not (w5 / "led/ova.jsonl").exists(), \
            "no D1-PASS nominator: nothing scored, only the release clause"
        (w5 / "in/b1/parity/STEP1B0_qwen25vl_7b.json").write_text(json.dumps({"model": q, "D1": "PASS"}))
        for p in sorted((w / "in/b1/out").glob(f"at_{q}_ov_dev_a-*-b1.preds.json"))[:3]:  # perm p1, p2, rand d0
            shutil.copy(p, w5 / "in/b1/out" / p.name)
        assert "lacks" in refused(st_ova, ns(), w5, {}) and not (w5 / "led/ova.jsonl").exists(), \
            "SC4 before any score: an incomplete Tier A is not scored"
        cmd_nominate(ns(ledger=[], closed="planted", parity=[], out=w5 / "res" / FILES["close"]))
        (w5 / "led/ova.jsonl").write_text("")  # so that only the closed-file rule can stop ovb here
        assert "closed" in refused(st_ovb, ns(), w5, {}), "a closed 1b has no batch-1 OV-dev-B to score"
        assert "no zs" in refused(with_zs, q, "ov_dev_a", [], []), "score_set needs one zs per backbone"
        for name, mem in (("carve_coco.jsonl", None), ("carve_f30k.jsonl", "f30k")):
            (w5 / "in/carve" / name).write_text("".join(json.dumps(
                {"dataset": "f30k_carve", "model": q, "arm": arm, "draw": 0, "tau": "-inf", "memory": mem,
                 "run_id": f"{arm}-{name}", "per_image": {"ids": ["f1", "f2", "f3"], "cider_ptb": [1.0, 2.0, 3.0]}}) + "\n"
                for arm in ("ret", "rand")))
        stored_files = lambda: {}  # noqa: E731
        assert "4ced15b4" in refused(st_posthoc, ns(), w5, {}), "the carve ledger is pinned"
        stored_files = good_pins
        pc = prompt_check([ovb_runs[0]], [zb, run(q, "ov_dev_b", "ret", 0, good, "stored", b1=False)])
        assert len(pc["pairs"]) == 1 and not pc["unequal"], "SC5: the batched ret of the same backbone, set, arm, draw"
        other = json.loads(ovb_runs[0].read_text())
        other["prompt_sha256"]["i00.jpg"] = "b" * 64
        ovb_runs[0].write_text(json.dumps(other))
        pc = prompt_check([ovb_runs[0]], [run(q, "ov_dev_b", "ret", 0, good, "stored", b1=False)])
        assert pc["unequal"] and list(pc["pairs"].values())[0]["equal"] == 23, "SC5: one prompt hash differs"
        selftest_b3_chain(w, run, good, generic, zb, refused)
    finally:
        A.score_refs, A.C.memory_captions, S2s.kit2 = real
        stored_files, env_record = real_stored, real_env
        A.C2_DIR, A.C2_RUNS, A.C2_LEDGER_SHA256 = real_c2
        SRC.update(real_src)


def selftest_b3(ok: list) -> None:
    """Block-3 scoring (CC-368 ruling 12) on planted columns: run ids, rows and labels, the K5 rule, K7, names, sets."""
    global CLOCK
    import tempfile
    ids = {s["name"]: b3_id(s) for s in A.b3_steps(B3_RUNNERS)}
    assert len(ids) == 10 and ids["B3_lmcap_ov_dev_b_ri"] == "at_lmcap-ri_ov_dev_b-mvi-b1" \
        and ids["B3_lmcap_xm_dev500_perm"] == "at_lmcap-perm_xm_dev500-mvi-b1" \
        and ids["B3_qwen25vl_7b_ov_dev_b_ret_img"] == "at_qwen25vl_7b_ov_dev_b-ret_img-k8-first-T1-mvi-b1" \
        and ids["B3_qwen25vl_7b_xm_dev500_rand_img"] == "at_qwen25vl_7b_xm_dev500-rand_img-k8--T1-d0-mvi-b1", \
        "the scorer finds the run ids of run doc §2"
    n = A.B3_N["ov_dev_b"]
    two, zero = np.full(n, 2.0), np.zeros(n)
    per = {"lmcap_ri|lmcap": two, "lmcap_rand|lmcap": zero, "lmcap_perm|lmcap": two, "lmcap_ri|lmcap_m3": zero + 50,
           "qwen25vl_7b|ret_img": np.full(n, 1.5), "qwen25vl_7b|rand_d0_img": zero, "qwen25vl_7b|ret": two + 7,
           "qwen25vl_7b|zs": zero - 9}
    idx = A.boot_idx(n)
    rows = b3_rows(per, "ov_dev_b", idx)
    assert {k: (r["d"], r["label"]) for k, r in rows.items()} == {
        "lmcap|tau_sel": (2.0, "DETECTED"), "lmcap|tau_pair": (0.0, "NEGLIGIBLE"), "lmcap|tau_marg": (2.0, "DETECTED"),
        "qwen25vl_7b|tau_sel_img": (1.5, "NEGLIGIBLE")}, "ri - rand, ri - perm, perm - rand, ret_img - rand_img d0, m = 1"
    r, q = rows["lmcap|tau_sel"], rows["qwen25vl_7b|tau_sel_img"]
    assert r["m"] == 1 and r["wording"] == E6["lmcap"] and r["decodes"] == B3_DECODES and r["batch"] == B3_BATCH \
        and r["tier"] == B3_TIER["lmcap|tau_sel"] and r["tag"] == A.LABEL and "beside" not in r
    assert q["wording"] == E6["qwen25vl_7b"] and q["beside"] == TEXT_SEL["ov_dev_b"] and q["decodes"] == B3_DECODES
    assert all("note" not in x for x in rows.values()), "CC-368 O8: no 'split of a known τ_sel' on block-3 rows"
    xr = b3_rows(per, "xm_dev500", idx)
    assert all(x["tier"] == B3_XM for x in xr.values()) and xr["qwen25vl_7b|tau_sel_img"]["beside"] == TEXT_SEL["xm_dev500"]
    part = b3_rows({k: v for k, v in per.items() if k != "lmcap_perm|lmcap"}, "ov_dev_b", idx)
    assert set(part) == {"lmcap|tau_sel", "qwen25vl_7b|tau_sel_img"}, "a row without both of its arms is absent"
    assert k5_verdict({"d": 2.0, "p": ALPHA}) == "DETECTED" and k5_verdict({"d": 2.0, "p": 0.02500001}) == "NOT DETECTED" \
        and k5_verdict({"d": 1.999, "p": 1 / 2001}) == "NOT DETECTED" and k5_verdict(None) == "NOT RUN"
    names = ["uit-openviic-annotation-test.json", "test_data.json", "xm_test2500_x.jpg", "f30k_test.csv",
             "nocaps_val.json", "selftest.log", "at_lmcap-ri_ov_dev_b-mvi-b1.preds.json", "STEP3_lmcap.json", "contest.txt"]
    assert test_named(names) == sorted(names[:5]), "test-set file names are refused by name"
    try:
        full_set(["i1"], "xm_dev500")
        raise AssertionError("rows over part of a set must be refused")
    except SystemExit as e:
        assert "full set" in str(e)
    real = CLOCK
    try:
        CLOCK = lambda: K7_TS - 1  # noqa: E731
        k7_open()
        for at in (K7_TS, K7_TS + 3600):
            CLOCK = lambda at=at: at  # noqa: E731
            try:
                k7_open()
                raise AssertionError("K7 must refuse")
            except SystemExit as e:
                assert "K7" in str(e)
        with tempfile.TemporaryDirectory() as tmp:
            try:
                cmd_stage(argparse.Namespace(stage="b3k5", work=Path(tmp), prev=None))
                raise AssertionError("a block-3 stage after K7 must be refused")
            except SystemExit as e:
                assert "K7" in str(e), "cmd_stage checks K7 first for every block-3 stage"
    finally:
        CLOCK = real
    ok.append("block 3: the decoder's run ids, LMCap τ_sel, τ_pair, τ_marg and the image-caption-pair τ_sel at m = 1 "
              "with their labels and wording and no split note, absent rows, the K5 rule at its boundary, K7 at "
              "2026-11-16T05:00Z, test-set names, full sets")


def selftest_b3_chain(w: Path, run, good, generic, zb: Path, refused) -> None:
    """The block-3 stages on a planted tree through the unstubbed c_attr.cmd_score. Called inside selftest_chain, whose
    replaced references, memory captions, segmenter, environment and stage-2 runs it reuses."""
    global stored_files, SRC_B3, B3_NOM_SHA256
    ns, q, src, wb = argparse.Namespace, "qwen25vl_7b", w / "b3src", w / "wb3"
    for d in ("b3src/out", "b3src/parity", "b3src/logs", "wb3/in", "wb3/led", "wb3/res"):
        (w / d).mkdir(parents=True)
    zx = run(q, "xm_dev500", "zs", 0, generic, "stored", b1=False)
    cap_of = {"ri": good, "rand": generic, "perm": generic, "ret_img": good, "rand_img": generic}
    for s in A.b3_steps(B3_RUNNERS):
        lm = s["runner"] == "lmcap"
        p = run(f"lmcap_{s['arm']}" if lm else q, s["set"], "lmcap" if lm else s["arm"][:-4], 0, cap_of[s["arm"]],
                "b3src/out", rid=b3_id(s))
        if not lm:
            r = json.loads(p.read_text(encoding="utf-8"))
            r["spec"]["img_examples"] = True
            p.write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
    for r in B3_RUNNERS:
        (src / f"parity/STEP3_{r}.json").write_text(json.dumps({"model": r, "D1": "PASS", "host": "h1", "block": 3}))
    (src / "logs/job.log").write_text("JOB DONE\n")
    fs = sorted(str(p.relative_to(src)) for d in ("out", "logs", "parity") for p in (src / d).rglob("*") if p.is_file())
    (src / "SHA256SUMS").write_text("".join(f"{A.sha(src / f)}  {f}\n" for f in fs))
    sums = A.sha(src / "SHA256SUMS")
    shutil.copy(w / "c2/stage2_ledger.jsonl", wb / "in/stage2_ledger.jsonl")
    shutil.copy(w / "res" / FILES["ova"], wb / "in" / B3_NOM)
    saved = (stored_files, SRC_B3, B3_NOM_SHA256, dict(B3_REFS), A.lb.DATA, dict(A.B3_N), A.C2_LEDGER_SHA256)
    try:
        stored_files = lambda: {p: A.sha(p) for p in (zb, zx)}  # noqa: E731
        SRC_B3, B3_NOM_SHA256, A.lb.DATA = src, A.sha(wb / "in" / B3_NOM), w / "ncs"
        for k, txt in zip(sorted(B3_REFS), ("[]", "{}")):
            (A.lb.DATA / k).parent.mkdir(parents=True, exist_ok=True)
            (A.lb.DATA / k).write_text(txt)
            B3_REFS[k] = A.sha(A.lb.DATA / k)
        A.B3_N.update(ov_dev_b=24, xm_dev500=24)
        A.C2_LEDGER_SHA256 = A.sha(w / "c2/stage2_ledger.jsonl")
        (src / "RUNNING").write_text("")
        assert "still running" in refused(st_b3verify, ns(b3_sums=sums), w / "wb3_r", {})
        (src / "RUNNING").unlink()
        (src / "out/xm_test2500_q.json").write_text("{}")
        assert "test-set" in refused(st_b3verify, ns(b3_sums=sums), w / "wb3_n", {}), "a test-set name stops verify"
        (src / "out/xm_test2500_q.json").unlink()
        B3_NOM_SHA256 = "0" * 64
        assert "pinned" in refused(st_b3verify, ns(b3_sums=sums), w / "wb3_p", {}), "verify checks every pin"
        B3_NOM_SHA256 = A.sha(wb / "in" / B3_NOM)
        rec = {}
        st_b3verify(ns(b3_sums=sums), wb, rec)
        assert rec["trees"]["b3"]["files"] == 13 and rec["d1"]["lmcap"]["D1"] == "PASS" \
            and rec["parity_7_1"]["result"] == "ok" and len(rec["pins"]) == 5, f"b3verify ({rec['trees']})"
        st_b3k5(ns(), wb, {})
        k5 = json.loads((wb / "res/K5.json").read_text(encoding="utf-8"))
        assert k5["verdict"] == "DETECTED" and k5["row"]["label"] == "DETECTED" and k5["consequence"] == K5_OUT["DETECTED"]
        k5_ids = {b3_id(s) for s in A.b3_steps(("lmcap",)) if s["set"] == "ov_dev_b" and s["arm"] in ("ri", "rand")}
        led = A.read_ledgers([wb / "led/k5.jsonl"])
        assert len(led) == 4 and {x["run_id"] for x in led} == k5_ids, "K5 scores its two arms only (plain, masked3)"
        shutil.copytree(wb, w / "wb3_t")
        kt = json.loads((w / "wb3_t/res/K5.json").read_text(encoding="utf-8"))
        kt["row"]["d"] += 1
        (w / "wb3_t/res/K5.json").write_text(json.dumps(kt, ensure_ascii=False), encoding="utf-8")
        assert "differs" in refused(st_b3rest, ns(), w / "wb3_t", {}), "rest's τ_sel must equal the logged K5 file"
        st_b3rest(ns(), wb, {})
        s = json.loads((wb / "res/B3_SUMMARY.json").read_text(encoding="utf-8"))
        ov, xm = s["sets"]["ov_dev_b"]["rows"], s["sets"]["xm_dev500"]["rows"]
        assert s["not_run"] == [] and set(ov) == set(xm) == {f"{m}|{e}" for m, e, _x, _y in B3_EST}
        assert ov["lmcap|tau_sel"] == k5["row"] and ov["lmcap|tau_marg"]["d"] == 0.0 \
            and ov["lmcap|tau_marg"]["label"] == "NEGLIGIBLE" and ov["qwen25vl_7b|tau_sel_img"]["label"] == "DETECTED"
        assert not any("interpretation" in x for x in [*ov.values(), *xm.values()]), "K5 DETECTED: rows interpreted"
        w2 = w / "wb3_d1"  # LMCap D1 FAIL: K5 NOT RUN, the Qwen2.5-VL rows printed without interpretation
        shutil.copytree(src, w2 / "in/b3")
        for d in ("led", "res"):
            (w2 / d).mkdir()
        shutil.copy(wb / "in" / B3_NOM, w2 / "in" / B3_NOM)
        (w2 / "in/b3/parity/STEP3_lmcap.json").write_text(json.dumps({"model": "lmcap", "D1": "FAIL"}))
        for p in (w2 / "in/b3/out").glob("at_lmcap-*"):
            p.unlink()
        st_b3k5(ns(), w2, {})
        k2 = json.loads((w2 / "res/K5.json").read_text(encoding="utf-8"))
        assert k2["verdict"] == "NOT RUN" and k2["row"] is None and not (w2 / "led/k5.jsonl").exists()
        st_b3rest(ns(), w2, {})
        s2 = json.loads((w2 / "res/B3_SUMMARY.json").read_text(encoding="utf-8"))
        r2 = s2["sets"]["ov_dev_b"]["rows"]
        assert set(r2) == {"qwen25vl_7b|tau_sel_img"} and r2["qwen25vl_7b|tau_sel_img"]["interpretation"] == UNINTERPRETED \
            and len(s2["not_run"]) == 6 and s2["k5_consequence"] == K5_OUT["NOT RUN"]
        stray = sorted(src.glob("out/at_lmcap-*"))[0]
        shutil.copy(stray, w2 / "in/b3/out" / stray.name)
        assert "without a D1 PASS" in refused(st_b3rest, ns(), w2, {}), "runs of a runner without a D1 PASS refused"
        w3 = w / "wb3_cap"  # a CAP STOP or JOB STOP before step 2: K5 refused, no K5 file
        shutil.copytree(src, w3 / "in/b3")
        for d in ("led", "res"):
            (w3 / d).mkdir()
        (w3 / "in/b3/out" / f"{b3_id(A.b3_steps(('lmcap',))[1])}.preds.json").unlink()
        assert "judge line" in refused(st_b3k5, ns(), w3, {}) and not (w3 / "res/K5.json").exists()
    finally:
        stored_files, SRC_B3, B3_NOM_SHA256 = saved[:3]
        B3_REFS.clear()
        B3_REFS.update(saved[3])
        A.lb.DATA = saved[4]
        A.B3_N.clear()
        A.B3_N.update(saved[5])
        A.C2_LEDGER_SHA256 = saved[6]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("score")
    p.add_argument("--set", choices=sorted(A.SETS), required=True)
    p.add_argument("--runs", type=Path, nargs="+", required=True)
    p.add_argument("--ledger", type=Path, required=True)
    for k in ("kit_b", "c_lists", "refs", "captions", "c2_dir", "c2_ledger", "nomination"):
        p.add_argument("--" + k.replace("_", "-"), type=Path)
    p.add_argument("--memory", choices=("vi", "coco", "f30k"), default=None)
    p.add_argument("--verdict", type=Path, help="v1.2 V4 (3): the batch-1 OV-dev-B summary, hashed in the LOG")
    p = sub.add_parser("nominate")
    p.add_argument("--ledger", type=Path, nargs="*", default=[])
    p.add_argument("--closed", help="v1.2 V4 release clause: write the empty v1.2 nomination file with this reason")
    p.add_argument("--parity", type=Path, nargs="*", default=[], help="parity/STEP1B0_<m>.json (D1 verdicts, SC4)")
    p.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("summary")
    p.add_argument("--ledger", type=Path, nargs="+", required=True)
    p.add_argument("--nomination", type=Path)
    p.add_argument("--parity", type=Path, nargs="*", default=[], help="parity/STEP10_<m>.json and STEP1B0_<m>.json")
    p.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("copybound")
    p.add_argument("--set", choices=("ov_dev_b", "xm_dev500"), required=True)
    for k in ("zs", "ret", "rand", "kit_b", "c_lists", "c2_ledger", "c2_run", "out"):
        p.add_argument("--" + k.replace("_", "-"), type=Path, required=True)
    p.add_argument("--blind", type=Path, help="a stored image-blind run, admitted by the stage-2 ledger")
    p = sub.add_parser("stage")
    p.add_argument("stage", choices=sorted(STAGE))
    p.add_argument("--work", type=Path, help="planted self-test trees only; the host default is /root/c_attr_score, "
                                             "or /root/c_attr_score_b3 for the block-3 stages")
    p.add_argument("--prev", help="sha256 of the previous stage's file, as logged")
    p.add_argument("--b1-sums", help="verify: sha256 of the verified block-1b SHA256SUMS, as logged")
    p.add_argument("--b-sums", help="verify: sha256 of the verified block-1 SHA256SUMS, as logged")
    p.add_argument("--reason", help="close: the reason of the OPS line '1b closed: <reason>'")
    p.add_argument("--b3-sums", help="b3verify: sha256 of the verified block-3 SHA256SUMS, as logged")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.cmd == "stage" and A.machine_id() in ("h1", "h2"):  # as c_attr.py's commands on a GPU host: the open() hook
        A.iso_install(A.iso_default())
    {"score": lambda: cmd_score(a), "nominate": lambda: cmd_nominate(a), "summary": lambda: cmd_summary(a),
     "copybound": lambda: cmd_copybound(a), "stage": lambda: cmd_stage(a)}.get(a.cmd, ap.print_help)()


if __name__ == "__main__":
    main()
