#!/usr/bin/env python3
"""KTVIC punctuation audit: CIDEr-D with the final period stripped vs appended, k = 1..5 references (Paper B, 3.3).

For each system, every output is segmented with RDRSegmenter, its trailing punctuation tokens are stripped
("cider_strip") or replaced by one "." ("cider_add_period"), and CIDEr-D x100 is computed against the first k
references (first_k) and averaged over the five cyclic choices of k references (cyclic_balanced_k).

    NCS_DATA=/path/to/ncs-data python scripts/kit_b/punctuation_audit.py --out punct.json [--systems A B ...]

Needs $NCS_DATA/datasets/ktvic/test_data.json, $NCS_DATA/vncorenlp/ (VnCoreNLP-1.2, obtained by the reader) and
system outputs $NCS_DATA/results/<system>.preds.json ({image_id: caption}). Scorer and segmenter come from
scripts/kit_b/protocol_pilot.py. The functions below are copied from the KTVIC part of the authors' audit script
c8_l5_d1_d3a_cpu_audit.py (sha256 6ddf523d699f794196169e9b797b600d63cdb1fa9e1492b334f77ed52bdfaa82); its UIT-ViIC
part (withdrawn in Paper B) and its XM3600 classifier audit are not included.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import unicodedata
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import protocol_pilot as E4  # noqa: E402

DATA = Path(os.environ.get("NCS_DATA", Path.home() / "ncs-data"))
SYSTEMS = ["p1assist_s42-short", "p1ep4_s42-short", "fuse2_s42-short", "zeroshot-short"]


def is_punct_tok(tok: str) -> bool:
    return bool(tok) and all(unicodedata.category(ch).startswith("P") for ch in tok)


def strip_trailing_punct_tokens(toks: list[str]) -> list[str]:
    out = list(toks)
    while out and is_punct_tok(out[-1]):
        out.pop()
    return out


def cider_mean(refs: dict[str, list[str]], hyps: dict[str, str]) -> float:
    return float(E4.Cider(refs).per_image(hyps).mean())



def run_l5_d1_punct_idf_law(ktvic_models: list[str]) -> dict:
    # 1. KTVIC test (n=558): segmented references and predictions via E4.rdr (official RDRSegmenter)
    ktvic_test_raw = json.loads((DATA / "datasets/ktvic/test_data.json").read_text(encoding="utf-8"))
    refs_raw: dict[str, list[str]] = {}
    for a in ktvic_test_raw["annotations"]:
        refs_raw.setdefault(str(a["image_id"]), []).append(a["caption"])
    ids_ktvic = sorted(refs_raw.keys())

    raw_hyps = {}
    for m_name in ktvic_models:
        p_f = DATA / "results" / f"{m_name}.preds.json"
        if p_f.exists():
            d = json.loads(p_f.read_text(encoding="utf-8"))
            raw_hyps[m_name] = {str(k): (v[0] if isinstance(v, list) else v) or "" for k, v in d.items()}

    # Batch RDR segmentation over all KTVIC refs and model predictions
    flat_texts = []
    for i in ids_ktvic:
        flat_texts.extend(refs_raw[i])
    for m_name in raw_hyps:
        for i in ids_ktvic:
            flat_texts.append(raw_hyps[m_name][i])

    seg_flat = [s.lower() for s in E4.rdr(flat_texts)]
    it = iter(seg_flat)
    ktvic_refs_seg = {i: [next(it) for _ in refs_raw[i]] for i in ids_ktvic}
    ktvic_preds_seg = {m_name: {i: next(it) for i in ids_ktvic} for m_name in raw_hyps}

    ktvic_k_curves = {}
    for m_name, hyp_orig in ktvic_preds_seg.items():
        hyp_strip = {}
        hyp_add = {}
        for i in ids_ktvic:
            toks = strip_trailing_punct_tokens(hyp_orig[i].split())
            hyp_strip[i] = " ".join(toks)
            hyp_add[i] = " ".join(toks + ["."])

        first_k_rows = {}
        cyclic_k_rows = {}
        for k in range(1, 6):
            refs_fk = {i: ktvic_refs_seg[i][:k] for i in ids_ktvic}
            c_s = cider_mean(refs_fk, hyp_strip)
            c_a = cider_mean(refs_fk, hyp_add)
            d_abs = c_a - c_s
            d_rel_pct = 100.0 * (c_a / c_s - 1.0) if c_s > 0 else 0.0
            first_k_rows[f"k={k}"] = {
                "k": k,
                "cider_strip": round(c_s, 4),
                "cider_add_period": round(c_a, 4),
                "d_abs": round(d_abs, 4),
                "d_rel_pct": round(d_rel_pct, 4),
            }

            c_s_shifts = []
            c_a_shifts = []
            for shift in range(5):
                refs_sh = {
                    i: [ktvic_refs_seg[i][(shift + j) % len(ktvic_refs_seg[i])] for j in range(k)]
                    for i in ids_ktvic
                }
                c_s_shifts.append(cider_mean(refs_sh, hyp_strip))
                c_a_shifts.append(cider_mean(refs_sh, hyp_add))
            cs_m = float(np.mean(c_s_shifts))
            ca_m = float(np.mean(c_a_shifts))
            cyclic_k_rows[f"k={k}"] = {
                "k": k,
                "cider_strip": round(cs_m, 4),
                "cider_add_period": round(ca_m, 4),
                "d_abs": round(ca_m - cs_m, 4),
                "d_rel_pct": round(100.0 * (ca_m / cs_m - 1.0), 4),
            }

        rels_fk = [first_k_rows[f"k={k}"]["d_rel_pct"] for k in range(1, 6)]
        rels_cy = [cyclic_k_rows[f"k={k}"]["d_rel_pct"] for k in range(1, 6)]
        monotone_fk = all(rels_fk[j] > rels_fk[j + 1] for j in range(4))
        monotone_cy = all(rels_cy[j] > rels_cy[j + 1] for j in range(4))
        reaches_le_minus20_k5 = bool(rels_fk[-1] <= -20.0)
        kill_gt_minus15_k5 = bool(rels_fk[-1] > -15.0)

        ktvic_k_curves[m_name] = {
            "first_k": first_k_rows,
            "cyclic_balanced_k": cyclic_k_rows,
            "monotone_more_negative_first_k": monotone_fk,
            "monotone_more_negative_cyclic_k": monotone_cy,
            "k5_d_rel_pct_first_k": round(rels_fk[-1], 4),
            "k5_d_rel_pct_cyclic_k": round(rels_cy[-1], 4),
            "passes_le_minus20_pct_at_k5": reaches_le_minus20_k5,
            "triggers_kill_rule_gt_minus15_or_nonmonotone": bool(kill_gt_minus15_k5 or not monotone_fk),
        }

    return {"ktvic_test_k1_to_k5_curves": ktvic_k_curves}


def selftest() -> None:
    assert is_punct_tok(".") and not is_punct_tok("a.") and strip_trailing_punct_tokens(["a", "b", ".", "!"]) == ["a", "b"]
    refs = {"1": ["x y z w", "x y z v"], "2": ["p q r s", "p q r t"]}
    plain = cider_mean(refs, {"1": "x y z w", "2": "p q r s"})
    dotted = cider_mean(refs, {"1": "x y z w .", "2": "p q r s ."})
    assert dotted < plain, (plain, dotted)  # a period the references never use lowers CIDEr-D
    print("selftest ok")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path)
    ap.add_argument("--systems", nargs="+", default=SYSTEMS)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    out = {"l5_d1_punct_idf_law": run_l5_d1_punct_idf_law(a.systems)}
    if a.out:
        a.out.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for m, c in out["l5_d1_punct_idf_law"]["ktvic_test_k1_to_k5_curves"].items():
        r = c["first_k"]["k=5"]
        print(f"{m:24s} k=5 strip {r['cider_strip']:.2f} add-period {r['cider_add_period']:.2f} d_abs {r['d_abs']:+.2f}")


if __name__ == "__main__":
    main()
