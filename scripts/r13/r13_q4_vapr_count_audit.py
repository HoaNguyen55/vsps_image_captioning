#!/usr/bin/env python3
"""R13 Q4: VaPR (COLM 2025, VaPR-UCLA/vapr-30k, Apache-2.0) as a positive control for the sec. 9 count audit.

Prereg: manuscript/prereg/2026-10-15_q4_vapr_count_control.md + .json. Count channel only (the length channel is prior work).
Same procedure as sec. 9 (Table 9.1): distinct COCO-80 classes per response with the E1 CHAIR matcher, pairs where neither
response names a class are dropped, count-matched share = share of pairs with dk = 0. Comparator values are read from the
committed sec. 9 audit JSON, not typed in.
Run (cwd outside the data dir): nice -n 19 env OMP_NUM_THREADS=2 python3 -E -P /mnt/d/vsps_image_captioning/scripts/r13/r13_q4_vapr_count_audit.py
"""
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

ROOT = Path("/mnt/d/vsps_image_captioning")
DATA = ROOT / ".session_backup/2026-10-15/r13_data/vapr_30k/vapr-30k.json"
PREREG = ROOT / "manuscript/prereg/2026-10-15_q4_vapr_count_control.json"
SEC9 = ROOT / ".session_backup/2026-10-14/r11_verify/c6_n3_rlaifv_rlhfv_audit.json"
OUT = ROOT / ".session_backup/2026-10-15/r13_human/q4_vapr_count_control.json"
SYN = ROOT / "data/coco_probe/chair_synonyms.txt"
E1_PATH = ROOT / ".session_backup/2026-10-14/research_r10/E1/e1_chair_count.py"
COMPARATORS = {"HA-DPO": "hadpo_llava15", "HSA-DPO": "hsadpo", "SENTINEL": "sentinel_llava15_7b"}

sys.argv = ["e1_chair_count.py", str(SYN), "", "", "", ""]
_spec = importlib.util.spec_from_file_location("e1_chair_count", str(E1_PATH))
e1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(e1)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def cls(text):
    return set(e1.nodes(text or ""))


def gpt(conv):
    return " ".join(t["value"] for t in conv if t.get("from") == "gpt")


def wilson(k, n, z=1.959963984540054):
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return [c - h, c + h]


def audit(pairs):
    dk, dw, obj = [], [], 0
    for c, r in pairs:
        cc, cr = cls(c), cls(r)
        if cc | cr:
            obj += 1
            dk.append(len(cc) - len(cr))
            dw.append(len(c.split()) - len(r.split()))
    unm = [d for d in dk if d]
    k_eq = sum(d == 0 for d in dk)
    lw = [(d, w) for d, w in zip(dk, dw) if abs(w) <= 2]
    lw_unm = [d for d, _ in lw if d]
    return {"pairs": len(pairs), "pairs_with_objects": obj, "count_matched_n": k_eq,
            "count_matched_share": k_eq / obj, "count_matched_share_wilson_ci95": wilson(k_eq, obj),
            "chosen_fewer_among_unmatched": sum(d < 0 for d in unm) / max(len(unm), 1),
            "chosen_fewer_among_unmatched_wilson_ci95": wilson(sum(d < 0 for d in unm), len(unm)) if unm else None,
            "mean_dk": sum(dk) / obj, "mean_dwords": sum(dw) / obj,
            "abs_dwords_le_2_pairs": len(lw), "abs_dwords_le_2_count_matched_share": sum(d == 0 for d, _ in lw) / max(len(lw), 1),
            "abs_dwords_le_2_chosen_fewer_among_unmatched": sum(d < 0 for d in lw_unm) / max(len(lw_unm), 1)}


def _selftest():
    a = audit([("a dog", "a dog and a cat"), ("a cat", "a dog"), ("nothing", "here")])
    assert a["pairs_with_objects"] == 2 and a["count_matched_n"] == 1 and a["chosen_fewer_among_unmatched"] == 1.0, a
    lo, hi = wilson(50, 100)
    assert abs(lo - 0.4038) < 1e-3 and abs(hi - 0.5962) < 1e-3


def main():
    _selftest()
    pre = json.loads(PREREG.read_text())
    inputs = {str(p.relative_to(ROOT)): sha(p) for p in (DATA, SEC9, SYN, E1_PATH)}
    mismatch = {k: v for k, v in inputs.items() if pre["input_sha256"].get(k) != v}
    res = {"test": "R13_Q4_VaPR_count_positive_control", "prereg_json": str(PREREG.relative_to(ROOT)), "prereg_json_sha256": sha(PREREG),
           "script_sha256": sha(__file__), "input_sha256": inputs, "input_sha_mismatch_vs_prereg": mismatch, "claim_scope": "count channel only"}
    res["script_sha_matches_prereg"] = res["script_sha256"] == pre["script_sha256"]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if mismatch or not res["script_sha_matches_prereg"]:
        res["verdict"] = "ABORTED_SHA_MISMATCH"
        OUT.write_text(json.dumps(res, indent=1))
        raise SystemExit("sha mismatch vs prereg; aborted")

    rows = json.loads(DATA.read_text(encoding="utf-8"))
    vapr = audit([(gpt(r["conversations"]), gpt(r["rejected_conversations"])) for r in rows])
    sec9 = json.loads(SEC9.read_text())["summary_table_7_datasets"]
    comp = {name: sec9[key]["count_matched_share"] for name, key in COMPARATORS.items()}
    lo = vapr["count_matched_share_wilson_ci95"][0]
    res["vapr"] = vapr
    res["comparator_count_matched_share_from_sec9_json"] = comp
    res["point_gt_each"] = {k: vapr["count_matched_share"] > v for k, v in comp.items()}
    res["ci_lo_gt_each"] = {k: lo > v for k, v in comp.items()}
    res["pass"] = all(res["ci_lo_gt_each"].values())
    res["verdict"] = "PASS" if res["pass"] else ("PARTIAL_POINT_ONLY" if all(res["point_gt_each"].values()) else "FAIL")
    res["vapr_count_matched_exactly"] = vapr["count_matched_share"] == 1.0
    OUT.write_text(json.dumps(res, indent=1))
    print(res["verdict"])


if __name__ == "__main__":
    main()
