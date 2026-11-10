#!/usr/bin/env python3
"""Controls behind the count 0 for XM-test2500 (PIN-C2). Ids-free: counts and similarities only.

1. The XM features come from a later extraction run (owner-feats) than pool.npz. The same 299 KTVIC images are in
   both runs, so their features must agree: equal sha256, equal hashes, SSCD cosine 1.
2. The whole 15,249-image pool against the 2,500 XM test images: registered rule (build_memory.near, unchanged) and
   the SSCD > 0.75 clause. If no pool image matches, no shown example can.

    python -I -B xm_control.py > xm_control_stdout.txt"""
import json
import sys
from pathlib import Path

import numpy as np

R = Path("/mnt/d/vsps_image_captioning")
sys.path[:0] = [str(R / "scripts/c_stage1"), str(R / "scripts/w25"), str(R / "scripts")]
import build_memory as BM  # noqa: E402

F = ("phash", "dhash", "phash_m", "dhash_m", "sscd")
p = np.load(Path.home() / "vsps_w25k1/pool.npz")
a = np.load(Path.home() / "c_pvr_w25_in/of_ktvic_dev299.npz")
x = np.load(Path.home() / "c_pvr_w25_in/of_xm3600_all.npz")
pid = p["ids"].tolist()
at = {k: i for i, k in enumerate(pid)}
i = np.array([at[f"ktvic:{int(k)}"] for k in a["ids"].tolist()])
cos = (a["sscd"] * p["sscd"][i]).sum(1)
out = {"same_images_in_both_runs": {"n": len(i), "sha_equal": int((a["sha"] == p["sha"][i]).sum()),
                                    "phash_equal": int((a["phash"] == p["phash"][i]).sum()),
                                    "dhash_equal": int((a["dhash"] == p["dhash"][i]).sum()),
                                    "sscd_cos_min": round(float(cos.min()), 6)}}
lists = json.loads((R / "manuscript/prereg/2026-10-22_c_stage1/lists.json").read_text(encoding="utf-8"))
xat = {str(k): n for n, k in enumerate(x["ids"].tolist())}
sel = np.array([xat[r[0]] for r in lists["sets"]["xm_test2500"]])
xsha = x["sha"].tolist()
fx = {"sha": p["sha"].tolist(), **{k: p[k] for k in F}}
fy = {"sha": [xsha[n] for n in sel], **{k: x[k][sel] for k in F}}
sim = np.nan_to_num(p["sscd"]) @ np.nan_to_num(x["sscd"][sel]).T
out["pool_15249_vs_xm_test2500"] = {"pool_images_registered_rule": int(BM.near(fx, fy).sum()),
                                    "pool_images_sscd_gt_0.75": int((sim > 0.75).any(1).sum()),
                                    "max_sscd": round(float(sim.max()), 4)}
print(json.dumps(out, indent=1))
