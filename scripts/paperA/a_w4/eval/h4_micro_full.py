#!/usr/bin/env python
"""Sec 4.3 part (d) micro-F1 slopes (h4_check.py analyse(), unchanged, imported) on a chosen manifest and system set.
Inputs are built as h4_check.load_coco() builds them, with manifest, instance gold and systems from argv.
CP-111: also keeps the analyse() keys T3 (k_eff, sec5) and T2_profile / T2_share_draws_r_monotone_n1to5 ((A2),
sec4.3), so r4 has them; additive, the estimator is unchanged.
Run: python h4_micro_full.py MANIFEST INSTANCE_GOLD {all9|five|all9full} OUT_JSON"""
import json
import sys
from pathlib import Path

sys.path.insert(0, "/mnt/d/vsps_image_captioning/.session_backup/2026-10-14/r12/H4/scripts")
import h4_check as h4  # noqa: E402

manifest, gold_file, sysset, out_path = sys.argv[1:5]
sc, ROOT = h4.sc, h4.ROOT
vi, syn = sc.load_vi_terms(), sc.load_synonyms()
cids = sorted(i["cocoid"] for i in json.loads(Path(manifest).read_text("utf-8"))["images"])
cinst = {int(k): set(v["coco"]) for k, v in json.loads(Path(gold_file).read_text()).items()}
kr = h4.karpathy_refs(set(cids))
refs = [[sc.en_classes(s, syn) for s in kr[c][:5]] for c in cids]
ments = {}
for d in {"all9": ("coco5000", "coco_transfer", "coco5000_vcd"), "five": ("coco5000", "coco5000_vcd"),
           "all9full": ("coco5000", "coco_transfer_full5000", "coco5000_vcd")}[sysset]:
    for f in sorted((ROOT / "data/results" / d).glob("*.shard*.jsonl")):
        name = f.name.split(".shard")[0] + ("+vcd" if d == "coco5000_vcd" else "")
        ms = {}
        for line in f.read_text("utf-8").splitlines():
            r = json.loads(line)
            ms[r["cocoid"]] = sc.vi_objects(r["caption"], vi)
        assert set(cids) <= set(ms), name
        ments[name] = [ms.get(c, set()) for c in cids]
assert all(len(r) == 5 for r in refs)
res = h4.analyse(Path(out_path).stem, refs, ments, list(ments), inst=[cinst.get(c, set()) for c in cids], seed=1)
keep = ("n_img", "n_sys", "systems", "median_M", "T2_identity_b_randk", "T2_microF1_randk", "T2_identity_b5_minus_b1",
        "sign_agree_mixed_of_15", "sign_agree_micro_of_15",
        "T3", "T2_profile", "T2_share_draws_r_monotone_n1to5")  # CP-111: sec5 k_eff and sec4.3 (A2) for r4
Path(out_path).write_text(json.dumps({k: res[k] for k in keep}, indent=1, default=str))
