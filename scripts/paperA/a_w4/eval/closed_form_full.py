#!/usr/bin/env python
"""CP-111 W4: Supplementary closed form (h4_check.py closed_form(), unchanged, imported) on a W3/W4 cell, as
h4_check.main() builds its COCO inputs: b(k) = h4 T2_identity_b_randk points, b_inf = check_coco gold inst+refs5 b.
Run: python closed_form_full.py H4_JSON CHECK_COCO_JSON OUT_JSON
Gate: on r0 (h4_r0_2500_all9.json, r0_2500_all9.json) the output equals frozen h4_check.json T5_closed_form coco keys."""
import json
import sys
from pathlib import Path

sys.path.insert(0, "/mnt/d/vsps_image_captioning/.session_backup/2026-10-14/r12/H4/scripts")
import h4_check as h4  # noqa: E402

h4_json, cc_json, out_path = sys.argv[1:4]
bk = {int(k): v["point"] for k, v in json.loads(Path(h4_json).read_text())["T2_identity_b_randk"].items()}
b_inf = json.loads(Path(cc_json).read_text())["gold"]["inst+refs5"]["b"]
res = {"coco_free_D": h4.closed_form(bk), "coco_D_from_inst+refs": h4.closed_form(bk, b_inf=b_inf)}
Path(out_path).write_text(json.dumps(res, indent=1, default=str))
print(json.dumps(res, default=str))
