#!/usr/bin/env python
"""CC-108 W3 summary: reproduction gates, then every COCO-2500-based Paper A quantity on four cells
(r0 9 sys/2,500 = the paper; r1 5 sys/2,500; r2 5 sys/full 5,000; r3 5 sys/rest 2,500). Aggregates only.
CP-111: OUT is the W3 output folder (absolute, so the copy under scripts/paperA/a_w4 runs); once
r4_full5000_all9.json and h4_r4_full5000_all9.json exist there, r4 (9 sys/full 5,000) is added and the summary is
written to w4_summary.json instead of w3_summary.json."""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, "/mnt/d/vsps_image_captioning/scripts/paperA")
import a1_system_robustness as a1  # noqa: E402

BK = Path("/mnt/d/vsps_image_captioning/.session_backup")
OUT = BK / "2026-10-26/a_full5000/out"
CELLS = ("r0_2500_all9", "r1_2500_five", "r2_full5000_five", "r3_rest2500_five")
R4 = (OUT / "r4_full5000_all9.json").exists() and (OUT / "h4_r4_full5000_all9.json").exists()
CELLS += ("r4_full5000_all9",) * R4
GOLDS = ["refs1_randk", "refs2_randk", "refs3_randk", "refs4_randk", "refs5_randk", "inst"]

# gates: the patched copies reproduce the frozen outputs on the paper's cell
ref = json.loads((BK / "2026-10-14/r11_litmaps/L1/check_coco.json").read_text())
r0 = json.loads((OUT / "r0_2500_all9.json").read_text())
assert r0["gold"] == ref["gold"] and r0["systems"] == ref["systems"] and r0["n_img"] == ref["n_img"], "check_coco gate"
h4ref = json.loads((BK / "2026-10-14/r12/H4/out/h4_check.json").read_text())["coco2500"]
h4r0 = json.loads((OUT / "h4_r0_2500_all9.json").read_text())
assert json.loads(json.dumps(h4r0["T2_microF1_randk"])) == json.loads(json.dumps(h4ref["T2_microF1_randk"])), "h4 gate"
assert h4r0["T2_identity_b_randk"] == json.loads(json.dumps(h4ref["T2_identity_b_randk"])), "h4 identity-b gate"

logit = lambda p: math.log(p / (1 - p))


def cell(name):
    c = json.loads((OUT / f"{name}.json").read_text())
    h = json.loads((OUT / f"h4_{name}.json").read_text())
    g = c["gold"]
    sl = [g[k]["slope"] for k in GOLDS]
    r = {"n_img": c["n_img"], "n_sys": len(c["systems"]), "systems": c["systems"],
         "slope_ci": {k: [g[k]["slope"], g[k]["slope_ci"]] for k in GOLDS},
         "b": {k: g[k]["b"] for k in GOLDS}, "M_range": g["inst"]["M_range"], "median_M": g["inst"]["median_M"],
         "P1_rises_every_step_and_to_inst": all(a < b for a, b in zip(sl, sl[1:])),
         "P2_inst_ci_above_0": g["inst"]["slope_ci"][0] > 0,
         "P3_refs1": {"Mstar_micro": g["refs1_randk"]["Mstar_micro"], "M_max": g["refs1_randk"]["M_range"][1],
                      "holds": g["refs1_randk"]["Mstar_micro"] <= g["refs1_randk"]["M_range"][1]
                      and (g["refs1_randk"]["slope"] <= 0 or g["refs1_randk"]["slope_ci"][0] <= 0 <= g["refs1_randk"]["slope_ci"][1]),
                      "slope_negative_ci_below_0": g["refs1_randk"]["slope_ci"][1] < 0},
         "P4_sign_agree_mixed": f'{sum((v["slope"] > 0) == (v["Mstar_mixed"] > v["median_M"]) for v in g.values())}/{len(g)}',
         # CP-111a W3: "held" keys as registered in check_coco_PREDICTIONS.txt (c7cad2b2); P1_rises_every_step_and_to_inst
         # above is the separate every-step report. P3_refs1.M_max is this cell's own upper M (r0: 2.14).
         "P1_holds": g["refs1_randk"]["slope"] < g["refs5_randk"]["slope"] < g["inst"]["slope"],
         "P4_holds": all((v["slope"] > 0) == (v["Mstar_mixed"] > v["median_M"]) for v in g.values()),
         "kill_fires": not g["inst"]["slope_ci"][0] > 0 or not g["refs1_randk"]["slope"] < g["inst"]["slope"],
         "microF1_randk": {k: [v["slope"], v["slope_ci"]] for k, v in h["T2_microF1_randk"].items()},
         "channel_share": {}}
    for lab, (lo, hi) in {"refs1_to_refs5": ("refs1_randk", "refs5_randk"), "refs1_to_inst": ("refs1_randk", "inst")}.items():
        db = logit(g[hi]["b"]) - logit(g[lo]["b"]); dg = math.log(c["U"][hi] / c["U"][lo])
        r["channel_share"][lab] = round(db / (db + dg), 3)
    r["system_robustness"] = {}
    for col, gk in zip(a1.COLS, ("refs1_randk", "refs5_randk", "inst")):
        pts = {s: (v[3], v[2]) for s, v in c["tables"][gk].items()}
        a = a1.analyse(pts)
        r["system_robustness"][col] = {k: a[k] for k in ("slope_full", "loo_min", "loo_max", "jackknife_t95",
                                                         "jackknife_t95_excludes_0", "loo_sign_flips", "system_r")}
        r["system_robustness"][col]["subsets"] = a1.subsets(pts, a1.suffix_prompt, a1.is_zeroshot)
    return r


res = {"label": "CC-108 W3, planned rows (exploratory / post hoc); COCO-2500 keeps the registered XM prior",
       "gates": {"check_coco_r0_equals_frozen_check_coco.json": True, "h4_r0_equals_frozen_h4_check.json": True},
       "cells": {n: cell(n) for n in CELLS}}
# the paper's Table 7.2 COCO row and channel split must come out of r0
t72 = res["cells"]["r0_2500_all9"]["system_robustness"]
assert [round(t72[c]["slope_full"], 2) for c in a1.COLS] == [-4.28, 11.08, 22.41]
assert [round(t72["1 ref"]["loo_min"], 2), round(t72["1 ref"]["loo_max"], 2)] == [-11.62, -1.68], t72["1 ref"]
assert res["cells"]["r0_2500_all9"]["channel_share"] == {"refs1_to_refs5": 0.613, "refs1_to_inst": 0.709}, \
    res["cells"]["r0_2500_all9"]["channel_share"]
res["gates"]["a1_table_7_2_and_channel_share_reproduced_on_r0"] = True
(OUT / ("w4_summary.json" if R4 else "w3_summary.json")).write_text(json.dumps(res, indent=1, default=str) + "\n")
for n, r in res["cells"].items():
    print(n, r["n_img"], r["n_sys"], {k: v[0] for k, v in r["slope_ci"].items()}, "P1-4", r["P1_rises_every_step_and_to_inst"],
          r["P2_inst_ci_above_0"], r["P3_refs1"], r["P4_sign_agree_mixed"])
