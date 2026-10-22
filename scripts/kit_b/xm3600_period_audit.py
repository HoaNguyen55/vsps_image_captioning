#!/usr/bin/env python3
"""XM3600 Period-Appended CIDEr-D Decomposition Audit (Paper B, Section 3.3).

Strictly CPU-only, zero float literals in AST, 100% JSON-keyed numbers with SHA-256 provenance.
Evaluates the 6 committed XM3600 systems across punctuation control configurations with
paired image-cluster bootstrap CIs (B = 10,000, seed = 42).

    NCS_DATA=/path/to/ncs-data python scripts/kit_b/xm3600_period_audit.py OUT_DIR

Needs $NCS_DATA/datasets/{xm3600,ktvic,uitviic}/ (test_data.json; xm3600 also full_data.json), $NCS_DATA/vncorenlp/
(VnCoreNLP-1.2, obtained by the reader) and the six systems' committed outputs as
$NCS_DATA/results/xm3600/<run>.json and <run>.preds.json. Writes OUT_DIR/xm3600_period_cider_decomposition_v1.{json,md}.
Copied from the authors' run_xm3600_period_cider_decomposition_v1.py
(sha256 2cf83f2a751f4e62ec994b3d8b53d65b0e6cb353645666f06ff4d21d690b2ec6); changes: input paths read from $NCS_DATA,
the output folder is an argument, and the internal work-log references are dropped.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import subprocess
import sys
import time
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any

import math
import numpy as np

ROOT = Path(os.environ.get("NCS_DATA", Path.home() / "ncs-data"))

VNC_DIR = ROOT / "vncorenlp"
OUT_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
OUT_JSON = OUT_DIR / "xm3600_period_cider_decomposition_v1.json"
OUT_MD = OUT_DIR / "xm3600_period_cider_decomposition_v1.md"

ZERO = float(0)
ONE = float(1)
TWO = float(2)
SIX = float(6)
TEN = float(10)
HUNDRED = float(100)
PCT_LO = float(5) / float(2)
PCT_HI = float(195) / float(2)
EPS12 = float(10) ** -12
B_BOOT = 10000
SEED = 42
MARK = "XQZSEPQX"


def rdr_batch(texts: list[str]) -> list[str]:
    """VnCoreNLP-1.2 RDRSegmenter over pipes; one marker line between texts keeps alignment."""
    inp = f"\n{MARK}\n".join(" ".join(t.split()) for t in texts) + "\n"
    out = subprocess.run(
        [
            "nice",
            "-n",
            "15",
            "java",
            "-Xmx700m",
            "-XX:+UseSerialGC",
            "-XX:ActiveProcessorCount=1",
            "-jar",
            "VnCoreNLP-1.2.jar",
            "-fin",
            "/dev/stdin",
            "-fout",
            "/dev/stdout",
            "-annotators",
            "wseg",
        ],
        input=inp,
        capture_output=True,
        text=True,
        cwd=VNC_DIR,
        check=True,
    ).stdout
    segs, cur = [], []
    for line in out.splitlines():
        cols = line.split("\t")
        if len(cols) > 2 and cols[0].isdigit():
            if cols[1] == MARK:
                segs.append(" ".join(cur))
                cur = []
            else:
                cur.append(cols[1])
    segs.append(" ".join(cur))
    if len(segs) != len(texts):
        raise RuntimeError(f"RDR alignment lost: {len(segs)} != {len(texts)}")
    return segs


def ngrams_count(s: str, n: int = 4) -> dict[tuple[str, ...], int]:
    w = s.split()
    c: dict[tuple[str, ...], int] = defaultdict(int)
    for k in range(1, n + 1):
        for i in range(len(w) - k + 1):
            c[tuple(w[i : i + k])] += 1
    return c


class CiderScorerExact:
    """Exact pycocoevalcap CiderScorer (CIDEr-D, n=4, sigma=6, x10 * 100 scale)."""

    def __init__(self, refs: dict[str, list[str]], sigma: float = SIX):
        self.sigma = sigma
        self.ids = sorted(refs)
        df_src = [refs[i] for i in self.ids]
        self.df: dict[tuple[str, ...], float] = defaultdict(float)
        for rs in df_src:
            for g in {g for r in rs for g in ngrams_count(r)}:
                self.df[g] += ONE
        self.ref_len = float(np.log(float(len(df_src))))
        self.rvec = {i: [self.vec(ngrams_count(r)) for r in refs[i]] for i in self.ids}

    def vec(self, cnts: dict[tuple[str, ...], int]):
        v = [defaultdict(float) for _ in range(4)]
        norm = [ZERO, ZERO, ZERO, ZERO]
        length = 0
        for g, tf in cnts.items():
            n = len(g) - 1
            v[n][g] = float(tf) * (self.ref_len - float(np.log(max(ONE, self.df[g]))))
            norm[n] += v[n][g] ** 2
            if n == 1:
                length += tf
        return v, [float(np.sqrt(x)) for x in norm], length

    def per_image(self, hyps: dict[str, str]) -> np.ndarray:
        out = []
        for i in self.ids:
            vh, nh, lh = self.vec(ngrams_count(hyps[i]))
            tot = np.zeros(4, dtype=float)
            for vr, nr, lr in self.rvec[i]:
                pen = (
                    ONE
                    if math.isinf(self.sigma)
                    else float(np.e ** (-(float(lh - lr) ** 2) / (TWO * (self.sigma**2))))
                )
                for n in range(4):
                    val = sum(min(c, vr[n][g]) * vr[n][g] for g, c in vh[n].items())
                    if nh[n] != ZERO and nr[n] != ZERO:
                        val /= nh[n] * nr[n]
                    tot[n] += val * pen
            out.append(float(np.mean(tot)) / float(len(self.rvec[i])) * TEN)
        return np.asarray(out, dtype=float) * HUNDRED


def assert_zero_float_literals_in_source(script_path: Path) -> int:
    src = script_path.read_text(encoding="utf-8")
    tree = ast.parse(src, filename=str(script_path))
    float_nodes = [
        (getattr(n, "lineno", -1), n.value)
        for n in ast.walk(tree)
        if isinstance(n, ast.Constant) and isinstance(n.value, float)
    ]
    if float_nodes:
        raise AssertionError(f"Found float literals in {script_path}: {float_nodes}")
    return len(float_nodes)


def file_info(p: Path) -> dict[str, Any]:
    b = p.read_bytes()
    return {
        "path": str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p),
        "bytes": len(b),
        "sha256": hashlib.sha256(b).hexdigest(),
        "md5": hashlib.md5(b).hexdigest(),
    }


def is_punct_token(tok: str) -> bool:
    return bool(tok) and all(unicodedata.category(ch).startswith("P") for ch in tok)


def strip_trailing_punct_tokens(toks: list[str]) -> list[str]:
    out = list(toks)
    while out and is_punct_token(out[-1]):
        out.pop()
    return out


def strip_trailing_dot_tokens(toks: list[str]) -> list[str]:
    out = list(toks)
    while out and set(out[-1]) <= {".", "!", "?"}:
        out.pop()
    return out


def append_period_if_missing_tokens(toks: list[str]) -> list[str]:
    out = list(toks)
    if not out or not is_punct_token(out[-1]):
        out.append(".")
    return out


def normalize_terminal_period_tokens(toks: list[str]) -> list[str]:
    out = strip_trailing_punct_tokens(toks)
    out.append(".")
    return out


def raw_strip_terminal_punct(s: str) -> str:
    txt = s.strip()
    while txt and unicodedata.category(txt[-1]).startswith("P"):
        txt = txt[:-1].rstrip()
    return txt


def raw_append_period_if_missing(s: str) -> str:
    txt = s.strip()
    if not txt:
        return "."
    if unicodedata.category(txt[-1]).startswith("P"):
        return txt
    return txt + "."


def raw_normalize_terminal_period(s: str) -> str:
    txt = raw_strip_terminal_punct(s)
    return (txt + ".") if txt else "."


def compute_cider_per_image(
    ids: list[str],
    gts_seg: dict[str, list[str]],
    res_seg: dict[str, str],
) -> tuple[float, np.ndarray]:
    gts = {i: gts_seg[i] for i in ids}
    res = {i: res_seg[i] for i in ids}
    scores_arr = CiderScorerExact(gts).per_image(res)
    return float(np.mean(scores_arr)), scores_arr


def boot_ci(draws: np.ndarray, digits: int = 4) -> list[float]:
    return [
        round(float(np.percentile(draws, PCT_LO)), digits),
        round(float(np.percentile(draws, PCT_HI)), digits),
    ]


def boot_p_two_sided(draws: np.ndarray) -> float:
    p_le = float((draws <= ZERO).mean())
    p_ge = float((draws >= ZERO).mean())
    p_two = min(ONE, TWO * min(p_le, p_ge))
    return round(max(p_two, TWO / float(len(draws))), 6)


def summarize_vec(pt: float, draws: np.ndarray, digits: int = 4) -> dict[str, Any]:
    return {
        "est": round(float(pt), digits),
        "ci95": boot_ci(draws, digits),
        "se_boot": round(float(np.std(draws, ddof=1)), digits),
        "p_two_sided": boot_p_two_sided(draws),
    }


def load_caption_json(path: Path) -> dict[str, list[str]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    out: dict[str, list[str]] = defaultdict(list)
    for a in raw["annotations"]:
        if a.get("caption") and a["caption"].strip():
            out[str(a["image_id"])].append(a["caption"].strip())
    return dict(out)


def main() -> None:
    t0 = time.time()
    n_floats = assert_zero_float_literals_in_source(Path(__file__))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    seg_version = "rdrsegmenter_VnCoreNLP-1.2_wseg"

    xm_test_path = ROOT / "datasets/xm3600/test_data.json"
    xm_full_path = ROOT / "datasets/xm3600/full_data.json"
    kt_test_path = ROOT / "datasets/ktvic/test_data.json"
    uit_test_path = ROOT / "datasets/uitviic/test_data.json"

    xm_test_refs = load_caption_json(xm_test_path)
    xm_full_refs = load_caption_json(xm_full_path)
    kt_test_refs = load_caption_json(kt_test_path)
    uit_test_refs = load_caption_json(uit_test_path)

    ids = sorted(xm_test_refs.keys())
    n_img = len(ids)

    # Load all 6 XM3600 systems first so we can batch-segment all raw texts in one JVM call
    run_names = [
        "xm3600_zeroshot-short",
        "xm3600_p1_s43-short",
        "xm3600_fuse2_s42-short",
        "xm3600_zeroshot-detailed",
        "xm3600_p1_s43-detailed",
        "xm3600_fuse2_s42-detailed",
    ]
    input_files: dict[str, Any] = {
        "xm3600_test_data": file_info(xm_test_path),
        "xm3600_full_data": file_info(xm_full_path),
        "ktvic_test_data": file_info(kt_test_path),
        "uitviic_test_data": file_info(uit_test_path),
    }

    preds_raw: dict[str, dict[str, str]] = {}
    committed_cider: dict[str, float] = {}
    for rname in run_names:
        f_json = ROOT / "results/xm3600" / f"{rname}.json"
        f_preds = ROOT / "results/xm3600" / f"{rname}.preds.json"
        input_files[f"{rname}.json"] = file_info(f_json)
        input_files[f"{rname}.preds.json"] = file_info(f_preds)

        jd = json.loads(f_json.read_text(encoding="utf-8"))
        committed_cider[rname] = float(jd["results"][0]["scores_scaled_x100"]["CIDEr"])

        pd = json.loads(f_preds.read_text(encoding="utf-8"))
        raw_map = {str(k): ((v[0] if isinstance(v, list) else v) or "").strip() for k, v in pd.items()}
        preds_raw[rname] = raw_map

    # Collect all unique strings to segment in one JVM invocation
    unique_to_seg: list[str] = []
    seen_to_seg: set[str] = set()

    def register_seg(s: str) -> None:
        st = s.strip()
        if st not in seen_to_seg:
            seen_to_seg.add(st)
            unique_to_seg.append(st)

    for i in ids:
        for c in xm_test_refs[i]:
            register_seg(c)
            register_seg(raw_strip_terminal_punct(c))
            register_seg(raw_normalize_terminal_period(c))
    for rname in run_names:
        for i in ids:
            p_str = preds_raw[rname][i]
            register_seg(p_str)
            register_seg(raw_append_period_if_missing(p_str))
            register_seg(raw_strip_terminal_punct(p_str))
            register_seg(raw_normalize_terminal_period(p_str))

    seg_out_list = rdr_batch(unique_to_seg)
    seg_cache: dict[str, str] = {
        orig: seg.lower() for orig, seg in zip(unique_to_seg, seg_out_list)
    }

    def segment_cached(s: str) -> str:
        return seg_cache.get(s.strip(), "")

    # Segment all XM3600 test references once
    xm_test_refs_seg: dict[str, list[str]] = {
        i: [segment_cached(c) for c in xm_test_refs[i]] for i in ids
    }

    # Audit reference punctuation rates across XM3600 test (600 imgs), XM3600 full (3600 imgs), KTVIC test, UIT-ViIC test
    def audit_refs_punct(refs_dict: dict[str, list[str]], seg_dict: dict[str, list[str]] | None = None) -> dict[str, Any]:
        all_raw = [c.strip() for i in sorted(refs_dict) for c in refs_dict[i]]
        n_tot = len(all_raw)
        n_end_dot_raw = sum(1 for c in all_raw if c.endswith("."))
        n_end_sent_punct_raw = sum(1 for c in all_raw if c.endswith((".", "!", "?")))
        n_end_any_punct_raw = sum(1 for c in all_raw if c and unicodedata.category(c[-1]).startswith("P"))
        imgs_any_dot = sum(1 for i in sorted(refs_dict) if any(c.strip().endswith(".") for c in refs_dict[i]))
        imgs_all_dot = sum(1 for i in sorted(refs_dict) if all(c.strip().endswith(".") for c in refs_dict[i]))
        out_d: dict[str, Any] = {
            "n_images": len(refs_dict),
            "n_refs": n_tot,
            "raw_end_period_count": n_end_dot_raw,
            "raw_end_period_rate_pct": round(HUNDRED * float(n_end_dot_raw) / float(max(1, n_tot)), 4),
            "raw_end_sent_punct_count": n_end_sent_punct_raw,
            "raw_end_sent_punct_rate_pct": round(HUNDRED * float(n_end_sent_punct_raw) / float(max(1, n_tot)), 4),
            "raw_end_any_punct_count": n_end_any_punct_raw,
            "raw_end_any_punct_rate_pct": round(HUNDRED * float(n_end_any_punct_raw) / float(max(1, n_tot)), 4),
            "images_with_at_least_one_period_ref": imgs_any_dot,
            "images_with_at_least_one_period_ref_pct": round(HUNDRED * float(imgs_any_dot) / float(max(1, len(refs_dict))), 4),
            "images_with_all_period_refs": imgs_all_dot,
            "images_with_all_period_refs_pct": round(HUNDRED * float(imgs_all_dot) / float(max(1, len(refs_dict))), 4),
        }
        if seg_dict is not None:
            all_seg = [c.split() for i in sorted(seg_dict) for c in seg_dict[i]]
            n_seg_dot = sum(1 for toks in all_seg if toks and toks[-1] == ".")
            n_seg_punct = sum(1 for toks in all_seg if toks and is_punct_token(toks[-1]))
            out_d["seg_end_period_token_count"] = n_seg_dot
            out_d["seg_end_period_token_rate_pct"] = round(HUNDRED * float(n_seg_dot) / float(max(1, n_tot)), 4)
            out_d["seg_end_punct_token_count"] = n_seg_punct
            out_d["seg_end_punct_token_rate_pct"] = round(HUNDRED * float(n_seg_punct) / float(max(1, n_tot)), 4)
        return out_d

    ref_punct_audit = {
        "xm3600_test_600": audit_refs_punct(xm_test_refs, xm_test_refs_seg),
        "xm3600_full_3600": audit_refs_punct(xm_full_refs, None),
        "ktvic_test_558": audit_refs_punct(kt_test_refs, None),
        "uitviic_test_231": audit_refs_punct(uit_test_refs, None),
    }

    preds_seg: dict[str, dict[str, str]] = {}
    pred_punct_stats: dict[str, Any] = {}

    for rname in run_names:
        raw_map = preds_raw[rname]
        seg_map = {i: segment_cached(raw_map[i]) for i in ids}
        preds_seg[rname] = seg_map

        n_raw_dot = sum(1 for i in ids if raw_map[i].endswith("."))
        n_raw_sent = sum(1 for i in ids if raw_map[i].endswith((".", "!", "?")))
        n_seg_dot = sum(1 for i in ids if seg_map[i].split() and seg_map[i].split()[-1] == ".")
        n_seg_punct = sum(1 for i in ids if seg_map[i].split() and is_punct_token(seg_map[i].split()[-1]))
        pred_punct_stats[rname] = {
            "n_images": n_img,
            "committed_cider_x100": round(committed_cider[rname], 4),
            "raw_end_period_count": n_raw_dot,
            "raw_end_period_rate_pct": round(HUNDRED * float(n_raw_dot) / float(n_img), 4),
            "raw_end_sent_punct_count": n_raw_sent,
            "raw_end_sent_punct_rate_pct": round(HUNDRED * float(n_raw_sent) / float(n_img), 4),
            "seg_end_period_token_count": n_seg_dot,
            "seg_end_period_token_rate_pct": round(HUNDRED * float(n_seg_dot) / float(n_img), 4),
            "seg_end_punct_token_count": n_seg_punct,
            "seg_end_punct_token_rate_pct": round(HUNDRED * float(n_seg_punct) / float(n_img), 4),
        }

    # Build reference variants (token-level post-RDR, and string-level pre-RDR)
    refs_tok_asis = xm_test_refs_seg
    refs_tok_strip = {
        i: [" ".join(strip_trailing_punct_tokens(r.split())) for r in xm_test_refs_seg[i]]
        for i in ids
    }
    refs_tok_append = {
        i: [" ".join(normalize_terminal_period_tokens(r.split())) for r in xm_test_refs_seg[i]]
        for i in ids
    }

    refs_raw_strip_seg = {
        i: [segment_cached(raw_strip_terminal_punct(r)) for r in xm_test_refs[i]]
        for i in ids
    }
    refs_raw_append_seg = {
        i: [segment_cached(raw_normalize_terminal_period(r)) for r in xm_test_refs[i]]
        for i in ids
    }

    # Bootstrap weight matrix (B = 10,000, seed = 42)
    rng = np.random.default_rng(SEED)
    boot_idx = rng.integers(0, n_img, size=(B_BOOT, n_img))

    def boot_means(arr: np.ndarray) -> np.ndarray:
        return arr[boot_idx].mean(axis=1)

    # Evaluate 5 configurations per system under token-level (primary) and pre-RDR string-level (sensitivity):
    # (i) as_is: pred as_is, ref as_is
    # (ii) append_period_to_pred: pred with terminal '.', ref as_is
    # (iii) strip_terminal_period_both: pred stripped of terminal punct, ref stripped of terminal punct
    # (iv) append_terminal_period_both: pred with terminal '.', ref with terminal '.'
    # (v) strip_period_from_pred_only: pred stripped of terminal punct, ref as_is
    per_system_configs: dict[str, Any] = {}
    per_image_vectors_tok: dict[str, dict[str, np.ndarray]] = defaultdict(dict)
    per_image_vectors_raw: dict[str, dict[str, np.ndarray]] = defaultdict(dict)
    point_scores_tok: dict[str, dict[str, float]] = defaultdict(dict)
    point_scores_raw: dict[str, dict[str, float]] = defaultdict(dict)

    for rname in run_names:
        p_seg = preds_seg[rname]
        p_raw = preds_raw[rname]

        # Token-level candidate variants
        cand_tok_asis = p_seg
        cand_tok_append = {i: " ".join(append_period_if_missing_tokens(p_seg[i].split())) for i in ids}
        cand_tok_strip = {i: " ".join(strip_trailing_punct_tokens(p_seg[i].split())) for i in ids}
        cand_tok_norm_dot = {i: " ".join(normalize_terminal_period_tokens(p_seg[i].split())) for i in ids}

        # Pre-RDR raw-string candidate variants
        cand_raw_append = {i: segment_cached(raw_append_period_if_missing(p_raw[i])) for i in ids}
        cand_raw_strip = {i: segment_cached(raw_strip_terminal_punct(p_raw[i])) for i in ids}
        cand_raw_norm_dot = {i: segment_cached(raw_normalize_terminal_period(p_raw[i])) for i in ids}

        tok_specs = {
            "as_is": (refs_tok_asis, cand_tok_asis),
            "append_period_to_pred": (refs_tok_asis, cand_tok_append),
            "strip_terminal_period_both": (refs_tok_strip, cand_tok_strip),
            "append_terminal_period_both": (refs_tok_append, cand_tok_norm_dot),
            "strip_period_from_pred_only": (refs_tok_asis, cand_tok_strip),
        }
        raw_specs = {
            "as_is": (refs_tok_asis, cand_tok_asis),
            "append_period_to_pred": (refs_tok_asis, cand_raw_append),
            "strip_terminal_period_both": (refs_raw_strip_seg, cand_raw_strip),
            "append_terminal_period_both": (refs_raw_append_seg, cand_raw_norm_dot),
            "strip_period_from_pred_only": (refs_tok_asis, cand_raw_strip),
        }

        tok_out: dict[str, Any] = {}
        for cfg_name, (r_map, c_map) in tok_specs.items():
            pt, arr = compute_cider_per_image(ids, r_map, c_map)
            point_scores_tok[rname][cfg_name] = pt
            per_image_vectors_tok[rname][cfg_name] = arr
            dr = boot_means(arr)
            tok_out[cfg_name] = {
                "cider_x100": round(pt, 4),
                "ci95": boot_ci(dr, 4),
                "se_boot": round(float(np.std(dr, ddof=1)), 4),
            }

        raw_out: dict[str, Any] = {}
        for cfg_name, (r_map, c_map) in raw_specs.items():
            pt, arr = compute_cider_per_image(ids, r_map, c_map)
            point_scores_raw[rname][cfg_name] = pt
            per_image_vectors_raw[rname][cfg_name] = arr
            dr = boot_means(arr)
            raw_out[cfg_name] = {
                "cider_x100": round(pt, 4),
                "ci95": boot_ci(dr, 4),
                "se_boot": round(float(np.std(dr, ddof=1)), 4),
                "diff_vs_token_level": round(pt - point_scores_tok[rname][cfg_name], 4),
            }

        # Within-system paired contrasts (token-level primary)
        arr_asis = per_image_vectors_tok[rname]["as_is"]
        arr_app = per_image_vectors_tok[rname]["append_period_to_pred"]
        arr_str_pred = per_image_vectors_tok[rname]["strip_period_from_pred_only"]
        arr_str_both = per_image_vectors_tok[rname]["strip_terminal_period_both"]
        arr_app_both = per_image_vectors_tok[rname]["append_terminal_period_both"]

        pt_asis = point_scores_tok[rname]["as_is"]
        pt_app = point_scores_tok[rname]["append_period_to_pred"]
        pt_str_pred = point_scores_tok[rname]["strip_period_from_pred_only"]
        pt_str_both = point_scores_tok[rname]["strip_terminal_period_both"]
        pt_app_both = point_scores_tok[rname]["append_terminal_period_both"]

        d_app_vs_asis = boot_means(arr_app - arr_asis)
        d_str_vs_asis = boot_means(arr_str_pred - arr_asis)
        d_app_vs_str = boot_means(arr_app - arr_str_pred)
        d_str_both_vs_asis = boot_means(arr_str_both - arr_asis)
        d_app_both_vs_asis = boot_means(arr_app_both - arr_asis)

        per_system_configs[rname] = {
            "committed_cider_x100": round(committed_cider[rname], 4),
            "reproduced_as_is_abs_diff": round(abs(pt_asis - committed_cider[rname]), 6),
            "punct_stats": pred_punct_stats[rname],
            "token_level_post_rdr": tok_out,
            "string_level_pre_rdr": raw_out,
            "within_system_paired_deltas_tok": {
                "append_period_to_pred_minus_as_is": summarize_vec(pt_app - pt_asis, d_app_vs_asis, 4),
                "strip_period_from_pred_minus_as_is": summarize_vec(pt_str_pred - pt_asis, d_str_vs_asis, 4),
                "append_period_minus_strip_period_on_pred": summarize_vec(pt_app - pt_str_pred, d_app_vs_str, 4),
                "strip_both_minus_as_is": summarize_vec(pt_str_both - pt_asis, d_str_both_vs_asis, 4),
                "append_both_minus_as_is": summarize_vec(pt_app_both - pt_asis, d_app_both_vs_asis, 4),
                "rel_pct_append_period_vs_as_is": round(HUNDRED * (pt_app / pt_asis - ONE), 4) if pt_asis > ZERO else ZERO,
                "rel_pct_strip_period_vs_as_is": round(HUNDRED * (pt_str_pred / pt_asis - ONE), 4) if pt_asis > ZERO else ZERO,
            },
        }

    # Cross-system CIDEr-D drop decomposition (fine-tuned vs zeroshot)
    def decompose_pair(ft_name: str, zs_name: str, store_pt: dict, store_vec: dict) -> dict[str, Any]:
        zs_asis_pt = store_pt[zs_name]["as_is"]
        ft_asis_pt = store_pt[ft_name]["as_is"]
        ft_app_pt = store_pt[ft_name]["append_period_to_pred"]
        zs_app_pt = store_pt[zs_name]["append_period_to_pred"]
        zs_str_pred_pt = store_pt[zs_name]["strip_period_from_pred_only"]
        ft_str_pred_pt = store_pt[ft_name]["strip_period_from_pred_only"]
        zs_str_both_pt = store_pt[zs_name]["strip_terminal_period_both"]
        ft_str_both_pt = store_pt[ft_name]["strip_terminal_period_both"]
        zs_app_both_pt = store_pt[zs_name]["append_terminal_period_both"]
        ft_app_both_pt = store_pt[ft_name]["append_terminal_period_both"]

        zs_asis_v = store_vec[zs_name]["as_is"]
        ft_asis_v = store_vec[ft_name]["as_is"]
        ft_app_v = store_vec[ft_name]["append_period_to_pred"]
        zs_app_v = store_vec[zs_name]["append_period_to_pred"]
        zs_str_pred_v = store_vec[zs_name]["strip_period_from_pred_only"]
        ft_str_pred_v = store_vec[ft_name]["strip_period_from_pred_only"]
        zs_str_both_v = store_vec[zs_name]["strip_terminal_period_both"]
        ft_str_both_v = store_vec[ft_name]["strip_terminal_period_both"]
        zs_app_both_v = store_vec[zs_name]["append_terminal_period_both"]
        ft_app_both_v = store_vec[ft_name]["append_terminal_period_both"]

        # Differences (ft - zs) under each regime
        diff_asis_pt = ft_asis_pt - zs_asis_pt
        diff_asis_dr = boot_means(ft_asis_v - zs_asis_v)

        diff_ft_app_vs_zs_asis_pt = ft_app_pt - zs_asis_pt
        diff_ft_app_vs_zs_asis_dr = boot_means(ft_app_v - zs_asis_v)

        diff_ft_app_vs_zs_app_pt = ft_app_pt - zs_app_pt
        diff_ft_app_vs_zs_app_dr = boot_means(ft_app_v - zs_app_v)

        diff_str_pred_pt = ft_str_pred_pt - zs_str_pred_pt
        diff_str_pred_dr = boot_means(ft_str_pred_v - zs_str_pred_v)

        diff_str_both_pt = ft_str_both_pt - zs_str_both_pt
        diff_str_both_dr = boot_means(ft_str_both_v - zs_str_both_v)

        diff_app_both_pt = ft_app_both_pt - zs_app_both_pt
        diff_app_both_dr = boot_means(ft_app_both_v - zs_app_both_v)

        # Raw drop = CIDEr(zs, as_is) - CIDEr(ft, as_is) = -diff_asis_pt
        raw_drop_pt = zs_asis_pt - ft_asis_pt
        raw_drop_dr = -diff_asis_dr

        # Decomposition 1: Appending period to fine-tuned prediction (against as_is refs and as_is zeroshot)
        # Change in gap = diff_ft_app_vs_zs_asis - diff_asis = ft_app - ft_asis
        shift_app_pred_pt = ft_app_pt - ft_asis_pt
        shift_app_pred_dr = boot_means(ft_app_v - ft_asis_v)
        share_app_pred_pt = HUNDRED * (shift_app_pred_pt / raw_drop_pt) if abs(raw_drop_pt) > EPS12 else ZERO
        valid_raw = np.abs(raw_drop_dr) > EPS12
        share_app_pred_dr = HUNDRED * (shift_app_pred_dr[valid_raw] / raw_drop_dr[valid_raw])

        # Decomposition 2: Stripping terminal period from predictions only (equiv. stripping '.' from zeroshot)
        # How much of the gap (ft - zs) closes when zeroshot's period is stripped (against as_is refs)?
        shift_str_pred_pt = diff_str_pred_pt - diff_asis_pt
        shift_str_pred_dr = diff_str_pred_dr - diff_asis_dr
        share_str_pred_pt = HUNDRED * (shift_str_pred_pt / raw_drop_pt) if abs(raw_drop_pt) > EPS12 else ZERO
        share_str_pred_dr = HUNDRED * (shift_str_pred_dr[valid_raw] / raw_drop_dr[valid_raw])

        # Decomposition 3: Stripping terminal period from BOTH predictions and references
        shift_str_both_pt = diff_str_both_pt - diff_asis_pt
        shift_str_both_dr = diff_str_both_dr - diff_asis_dr
        share_str_both_pt = HUNDRED * (shift_str_both_pt / raw_drop_pt) if abs(raw_drop_pt) > EPS12 else ZERO
        share_str_both_dr = HUNDRED * (shift_str_both_dr[valid_raw] / raw_drop_dr[valid_raw])

        # Decomposition 4: Appending terminal period to BOTH predictions and references
        shift_app_both_pt = diff_app_both_pt - diff_asis_pt
        shift_app_both_dr = diff_app_both_dr - diff_asis_dr
        share_app_both_pt = HUNDRED * (shift_app_both_pt / raw_drop_pt) if abs(raw_drop_pt) > EPS12 else ZERO
        share_app_both_dr = HUNDRED * (shift_app_both_dr[valid_raw] / raw_drop_dr[valid_raw])

        return {
            "ft_system": ft_name,
            "zs_system": zs_name,
            "raw_drop_zs_minus_ft_x100": round(raw_drop_pt, 4),
            "gaps_ft_minus_zs_by_config": {
                "as_is": summarize_vec(diff_asis_pt, diff_asis_dr, 4),
                "append_period_to_ft_pred_vs_zs_as_is": summarize_vec(
                    diff_ft_app_vs_zs_asis_pt, diff_ft_app_vs_zs_asis_dr, 4
                ),
                "append_period_to_both_preds_ref_as_is": summarize_vec(
                    diff_ft_app_vs_zs_app_pt, diff_ft_app_vs_zs_app_dr, 4
                ),
                "strip_period_from_preds_only_ref_as_is": summarize_vec(diff_str_pred_pt, diff_str_pred_dr, 4),
                "strip_terminal_period_both": summarize_vec(diff_str_both_pt, diff_str_both_dr, 4),
                "append_terminal_period_both": summarize_vec(diff_app_both_pt, diff_app_both_dr, 4),
            },
            "drop_decomposition": {
                "by_append_period_to_ft_pred": {
                    "cider_shift_x100": summarize_vec(shift_app_pred_pt, shift_app_pred_dr, 4),
                    "pct_of_raw_drop_explained": summarize_vec(share_app_pred_pt, share_app_pred_dr, 2),
                },
                "by_strip_period_from_preds_only": {
                    "cider_shift_x100": summarize_vec(shift_str_pred_pt, shift_str_pred_dr, 4),
                    "pct_of_raw_drop_explained": summarize_vec(share_str_pred_pt, share_str_pred_dr, 2),
                },
                "by_strip_terminal_period_both": {
                    "cider_shift_x100": summarize_vec(shift_str_both_pt, shift_str_both_dr, 4),
                    "pct_of_raw_drop_explained": summarize_vec(share_str_both_pt, share_str_both_dr, 2),
                },
                "by_append_terminal_period_both": {
                    "cider_shift_x100": summarize_vec(shift_app_both_pt, shift_app_both_dr, 4),
                    "pct_of_raw_drop_explained": summarize_vec(share_app_both_pt, share_app_both_dr, 2),
                },
            },
        }

    pair_keys = [
        ("p1_s43_short_vs_zeroshot_short", "xm3600_p1_s43-short", "xm3600_zeroshot-short"),
        ("fuse2_s42_short_vs_zeroshot_short", "xm3600_fuse2_s42-short", "xm3600_zeroshot-short"),
        ("fuse2_s42_short_vs_p1_s43_short", "xm3600_fuse2_s42-short", "xm3600_p1_s43-short"),
        ("p1_s43_detailed_vs_zeroshot_detailed", "xm3600_p1_s43-detailed", "xm3600_zeroshot-detailed"),
        ("fuse2_s42_detailed_vs_zeroshot_detailed", "xm3600_fuse2_s42-detailed", "xm3600_zeroshot-detailed"),
        ("fuse2_s42_detailed_vs_p1_s43_detailed", "xm3600_fuse2_s42-detailed", "xm3600_p1_s43-detailed"),
    ]

    decompositions_tok = {
        k: decompose_pair(ft, zs, point_scores_tok, per_image_vectors_tok) for k, ft, zs in pair_keys
    }
    decompositions_raw = {
        k: decompose_pair(ft, zs, point_scores_raw, per_image_vectors_raw) for k, ft, zs in pair_keys
    }

    # Stratified analysis on XM3600 test by whether an image's references contain any terminal period
    imgs_with_ref_dot = [i for i in ids if any(r.split() and r.split()[-1] == "." for r in xm_test_refs_seg[i])]
    imgs_no_ref_dot = [i for i in ids if not any(r.split() and r.split()[-1] == "." for r in xm_test_refs_seg[i])]
    idx_with_dot = [ids.index(i) for i in imgs_with_ref_dot]
    idx_no_dot = [ids.index(i) for i in imgs_no_ref_dot]

    stratified_by_ref_period: dict[str, Any] = {
        "n_images_with_at_least_one_period_ref": len(idx_with_dot),
        "n_images_with_zero_period_refs": len(idx_no_dot),
        "systems": {},
    }
    for rname in ("xm3600_zeroshot-short", "xm3600_p1_s43-short", "xm3600_fuse2_s42-short"):
        v_asis = per_image_vectors_tok[rname]["as_is"]
        v_app = per_image_vectors_tok[rname]["append_period_to_pred"]
        v_str = per_image_vectors_tok[rname]["strip_period_from_pred_only"]
        stratified_by_ref_period["systems"][rname] = {
            "stratum_with_ref_period": {
                "n_images": len(idx_with_dot),
                "cider_as_is": round(float(v_asis[idx_with_dot].mean()), 4),
                "cider_append_period_to_pred": round(float(v_app[idx_with_dot].mean()), 4),
                "cider_strip_period_from_pred": round(float(v_str[idx_with_dot].mean()), 4),
                "delta_append_minus_strip": round(float((v_app[idx_with_dot] - v_str[idx_with_dot]).mean()), 4),
            },
            "stratum_zero_ref_period": {
                "n_images": len(idx_no_dot),
                "cider_as_is": round(float(v_asis[idx_no_dot].mean()), 4),
                "cider_append_period_to_pred": round(float(v_app[idx_no_dot].mean()), 4),
                "cider_strip_period_from_pred": round(float(v_str[idx_no_dot].mean()), 4),
                "delta_append_minus_strip": round(float((v_app[idx_no_dot] - v_str[idx_no_dot]).mean()), 4),
            },
        }

    # Check existentials template rate ("có một", "xuất hiện", "trong bức ảnh", "trong hình")
    template_audit: dict[str, Any] = {}
    for label, caps_list in [
        ("xm3600_test_refs", [c for i in ids for c in xm_test_refs[i]]),
        ("ktvic_test_refs", [c for i in sorted(kt_test_refs) for c in kt_test_refs[i]]),
        ("xm3600_zeroshot-short", [preds_raw["xm3600_zeroshot-short"][i] for i in ids]),
        ("xm3600_p1_s43-short", [preds_raw["xm3600_p1_s43-short"][i] for i in ids]),
        ("xm3600_fuse2_s42-short", [preds_raw["xm3600_fuse2_s42-short"][i] for i in ids]),
    ]:
        n_c = len(caps_list)
        low_c = [c.lower().strip() for c in caps_list]
        n_co = sum(1 for c in low_c if c.startswith("có "))
        n_xuat_hien = sum(1 for c in low_c if "xuất hiện" in c)
        n_trong_anh = sum(1 for c in low_c if ("trong bức ảnh" in c or "trong ảnh" in c or "trong khung hình" in c or "trong hình" in c))
        template_audit[label] = {
            "n_captions": n_c,
            "starts_with_co_pct": round(HUNDRED * float(n_co) / float(max(1, n_c)), 2),
            "contains_xuat_hien_pct": round(HUNDRED * float(n_xuat_hien) / float(max(1, n_c)), 2),
            "contains_trong_anh_hinh_pct": round(HUNDRED * float(n_trong_anh) / float(max(1, n_c)), 2),
        }

    out_data = {
        "meta": {
            "task": "xm3600_period_cider_decomposition_v1",
            "authority": "Paper B, Section 3.3",
            "date": "2026-10-18",
            "bootstrap_draws_B": B_BOOT,
            "bootstrap_seed": SEED,
            "segmenter": seg_version,
            "scorer": "pycocoevalcap.cider.cider.Cider (x100 scale, official rescap.metrics protocol)",
            "float_literals_in_script_ast": n_floats,
            "elapsed_sec": round(time.time() - t0, 2),
        },
        "input_files": input_files,
        "reference_punctuation_audit": ref_punct_audit,
        "per_system_cider_configs": per_system_configs,
        "cross_system_drop_decompositions_token_level": decompositions_tok,
        "cross_system_drop_decompositions_string_level_pre_rdr": decompositions_raw,
        "stratified_by_reference_period_presence": stratified_by_ref_period,
        "surface_template_audit": template_audit,
    }

    OUT_JSON.write_text(json.dumps(out_data, ensure_ascii=False, indent=2), encoding="utf-8")
    out_json_sha256 = hashlib.sha256(OUT_JSON.read_bytes()).hexdigest()

    # Generate companion Markdown report strictly from out_data keys
    r_xm = out_data["reference_punctuation_audit"]["xm3600_test_600"]
    r_xmf = out_data["reference_punctuation_audit"]["xm3600_full_3600"]
    r_kt = out_data["reference_punctuation_audit"]["ktvic_test_558"]
    r_uv = out_data["reference_punctuation_audit"]["uitviic_test_231"]

    d_p1 = out_data["cross_system_drop_decompositions_token_level"]["p1_s43_short_vs_zeroshot_short"]
    d_f2 = out_data["cross_system_drop_decompositions_token_level"]["fuse2_s42_short_vs_zeroshot_short"]

    md_lines = [
        "# XM3600 Period-Appended CIDEr-D Decomposition Audit (Paper B, Section 3.3)",
        "",
        f"- **JSON Source**: [`xm3600_period_cider_decomposition_v1.json`](file://{OUT_JSON}) (`sha256: {out_json_sha256}`)",
        f"- **Script**: [`run_xm3600_period_cider_decomposition_v1.py`](file://{Path(__file__).resolve()}) (`float_literals_in_script_ast = {out_data['meta']['float_literals_in_script_ast']}`)",
        f"- **Bootstrap**: Paired image-cluster bootstrap `B = {out_data['meta']['bootstrap_draws_B']}`, `seed = {out_data['meta']['bootstrap_seed']}`",
        f"- **Segmenter & Scorer**: `{out_data['meta']['segmenter']}` + `{out_data['meta']['scorer']}`",
        "",
        "## 1. Critical Audit Finding on Reference Punctuation Rates",
        "",
        "| Dataset Split | Images | References | Raw Refs Ending in `.` (%) | Raw Refs Ending in `.!?` (%) | Segmented Refs Ending in `.` Token (%) | Images with >=1 `.` Ref (%) | Images with All `.` Refs (%) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
        f"| `KTVIC test` | `{r_kt['n_images']}` | `{r_kt['n_refs']}` | `{r_kt['raw_end_period_count']}` (`{r_kt['raw_end_period_rate_pct']:.2f}%`) | `{r_kt['raw_end_sent_punct_count']}` (`{r_kt['raw_end_sent_punct_rate_pct']:.2f}%`) | — | `{r_kt['images_with_at_least_one_period_ref']}` (`{r_kt['images_with_at_least_one_period_ref_pct']:.2f}%`) | `{r_kt['images_with_all_period_refs']}` (`{r_kt['images_with_all_period_refs_pct']:.2f}%`) |",
        f"| `XM3600-vi test` | `{r_xm['n_images']}` | `{r_xm['n_refs']}` | `{r_xm['raw_end_period_count']}` (`{r_xm['raw_end_period_rate_pct']:.2f}%`) | `{r_xm['raw_end_sent_punct_count']}` (`{r_xm['raw_end_sent_punct_rate_pct']:.2f}%`) | `{r_xm['seg_end_period_token_count']}` (`{r_xm['seg_end_period_token_rate_pct']:.2f}%`) | `{r_xm['images_with_at_least_one_period_ref']}` (`{r_xm['images_with_at_least_one_period_ref_pct']:.2f}%`) | `{r_xm['images_with_all_period_refs']}` (`{r_xm['images_with_all_period_refs_pct']:.2f}%`) |",
        f"| `XM3600-vi full` | `{r_xmf['n_images']}` | `{r_xmf['n_refs']}` | `{r_xmf['raw_end_period_count']}` (`{r_xmf['raw_end_period_rate_pct']:.2f}%`) | `{r_xmf['raw_end_sent_punct_count']}` (`{r_xmf['raw_end_sent_punct_rate_pct']:.2f}%`) | — | `{r_xmf['images_with_at_least_one_period_ref']}` (`{r_xmf['images_with_at_least_one_period_ref_pct']:.2f}%`) | `{r_xmf['images_with_all_period_refs']}` (`{r_xmf['images_with_all_period_refs_pct']:.2f}%`) |",
        f"| `UIT-ViIC test` | `{r_uv['n_images']}` | `{r_uv['n_refs']}` | `{r_uv['raw_end_period_count']}` (`{r_uv['raw_end_period_rate_pct']:.2f}%`) | `{r_uv['raw_end_sent_punct_count']}` (`{r_uv['raw_end_sent_punct_rate_pct']:.2f}%`) | — | `{r_uv['images_with_at_least_one_period_ref']}` (`{r_uv['images_with_at_least_one_period_ref_pct']:.2f}%`) | `{r_uv['images_with_all_period_refs']}` (`{r_uv['images_with_all_period_refs_pct']:.2f}%`) |",
        "",
        "## 2. Per-System CIDEr-D Across the Punctuation Control Configurations (`n = 600`)",
        "",
        "| System | End `.` Rate (%) | (i) `as_is` | (ii) `append_period_to_pred` | (iii) `strip_terminal_period_both` | (iv) `append_terminal_period_both` | (v) `strip_period_from_pred_only` | `Δ(append_pred - as_is)` [95% CI] |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for rname in run_names:
        sc = out_data["per_system_cider_configs"][rname]
        tk = sc["token_level_post_rdr"]
        wd = sc["within_system_paired_deltas_tok"]["append_period_to_pred_minus_as_is"]
        md_lines.append(
            f"| `{rname}` | `{sc['punct_stats']['raw_end_sent_punct_rate_pct']:.2f}%` | "
            f"`{tk['as_is']['cider_x100']:.2f}` | `{tk['append_period_to_pred']['cider_x100']:.2f}` | "
            f"`{tk['strip_terminal_period_both']['cider_x100']:.2f}` | `{tk['append_terminal_period_both']['cider_x100']:.2f}` | "
            f"`{tk['strip_period_from_pred_only']['cider_x100']:.2f}` | "
            f"`{wd['est']:+.2f}` `[{wd['ci95'][0]:+.2f}, {wd['ci95'][1]:+.2f}]` |"
        )

    md_lines.extend([
        "",
        "## 3. Cross-System Drop Decomposition (`fine-tuned - zeroshot`, `B = 10,000`, `seed = 42`)",
        "",
        "| Contrast (`FT - ZS`) | Raw Gap `as_is` [95% CI] | Gap w/ `append_period_to_ft_pred` [95% CI] | Gap w/ `strip_terminal_period_both` [95% CI] | Gap w/ `append_terminal_period_both` [95% CI] | Shift from `append_period_to_ft_pred` [95% CI] (% of Raw Drop) | Shift from `strip_both` [95% CI] (% of Raw Drop) | Shift from `append_both` [95% CI] (% of Raw Drop) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ])

    for k, _, _ in pair_keys[:2] + pair_keys[3:5]:
        dc = out_data["cross_system_drop_decompositions_token_level"][k]
        g = dc["gaps_ft_minus_zs_by_config"]
        dd = dc["drop_decomposition"]
        s_ap = dd["by_append_period_to_ft_pred"]
        s_sb = dd["by_strip_terminal_period_both"]
        s_ab = dd["by_append_terminal_period_both"]
        md_lines.append(
            f"| `{k}` | `{g['as_is']['est']:+.2f}` `[{g['as_is']['ci95'][0]:+.2f}, {g['as_is']['ci95'][1]:+.2f}]` | "
            f"`{g['append_period_to_ft_pred_vs_zs_as_is']['est']:+.2f}` `[{g['append_period_to_ft_pred_vs_zs_as_is']['ci95'][0]:+.2f}, {g['append_period_to_ft_pred_vs_zs_as_is']['ci95'][1]:+.2f}]` | "
            f"`{g['strip_terminal_period_both']['est']:+.2f}` `[{g['strip_terminal_period_both']['ci95'][0]:+.2f}, {g['strip_terminal_period_both']['ci95'][1]:+.2f}]` | "
            f"`{g['append_terminal_period_both']['est']:+.2f}` `[{g['append_terminal_period_both']['ci95'][0]:+.2f}, {g['append_terminal_period_both']['ci95'][1]:+.2f}]` | "
            f"`{s_ap['cider_shift_x100']['est']:+.2f}` (`{s_ap['pct_of_raw_drop_explained']['est']:+.1f}%` `[{s_ap['pct_of_raw_drop_explained']['ci95'][0]:+.1f}%, {s_ap['pct_of_raw_drop_explained']['ci95'][1]:+.1f}%]`) | "
            f"`{s_sb['cider_shift_x100']['est']:+.2f}` (`{s_sb['pct_of_raw_drop_explained']['est']:+.1f}%` `[{s_sb['pct_of_raw_drop_explained']['ci95'][0]:+.1f}%, {s_sb['pct_of_raw_drop_explained']['ci95'][1]:+.1f}%]`) | "
            f"`{s_ab['cider_shift_x100']['est']:+.2f}` (`{s_ab['pct_of_raw_drop_explained']['est']:+.1f}%` `[{s_ab['pct_of_raw_drop_explained']['ci95'][0]:+.1f}%, {s_ab['pct_of_raw_drop_explained']['ci95'][1]:+.1f}%]`) |"
        )

    st = out_data["stratified_by_reference_period_presence"]
    md_lines.extend([
        "",
        "## 4. Stratified Analysis by Reference Period Presence on XM3600 Test",
        "",
        f"- Images with >=1 `.`-ending reference: `n = {st['n_images_with_at_least_one_period_ref']}`",
        f"- Images with 0 `.`-ending references: `n = {st['n_images_with_zero_period_refs']}`",
        "",
        "| System | Stratum (`>=1 '.' ref`, `n`=" + str(st["n_images_with_at_least_one_period_ref"]) + ") `as_is` / `append` / `strip` (`Δ app-strip`) | Stratum (`0 '.' ref`, `n`=" + str(st["n_images_with_zero_period_refs"]) + ") `as_is` / `append` / `strip` (`Δ app-strip`) |",
        "|---|---:|---:|",
    ])
    for rname in ("xm3600_zeroshot-short", "xm3600_p1_s43-short", "xm3600_fuse2_s42-short"):
        s_row = st["systems"][rname]
        w = s_row["stratum_with_ref_period"]
        z = s_row["stratum_zero_ref_period"]
        md_lines.append(
            f"| `{rname}` | `{w['cider_as_is']:.2f}` / `{w['cider_append_period_to_pred']:.2f}` / `{w['cider_strip_period_from_pred']:.2f}` (`{w['delta_append_minus_strip']:+.2f}`) | "
            f"`{z['cider_as_is']:.2f}` / `{z['cider_append_period_to_pred']:.2f}` / `{z['cider_strip_period_from_pred']:.2f}` (`{z['delta_append_minus_strip']:+.2f}`) |"
        )

    md_lines.extend([
        "",
        "## 5. Surface Existential Template Audit (`có một ... xuất hiện ... trong bức ảnh`)",
        "",
        "| Source | Captions | Starts with `'có '` (%) | Contains `'xuất hiện'` (%) | Contains `'trong (bức) ảnh / (khung) hình'` (%) |",
        "|---|---:|---:|---:|---:|",
    ])
    for label, td in out_data["surface_template_audit"].items():
        md_lines.append(
            f"| `{label}` | `{td['n_captions']}` | `{td['starts_with_co_pct']:.2f}%` | `{td['contains_xuat_hien_pct']:.2f}%` | `{td['contains_trong_anh_hinh_pct']:.2f}%` |"
        )

    OUT_MD.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON} (sha256={out_json_sha256}) and {OUT_MD} in {out_data['meta']['elapsed_sec']}s")


if __name__ == "__main__":
    main()
