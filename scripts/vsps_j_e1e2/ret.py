#!/usr/bin/env python
"""T-KT retention and mirror rate on stage-1 records (CC-207 W9; the source of 52.9 / 69.6 in the VSPS-J program).

    python3 -I scripts/vsps_j_e1e2/ret.py <dir of stage-1 *.json records>

Unit: (image, lexicon object) pairs over all propositions of the image (rescap.chair.objects_in); images whose
reference captions name no lexicon object are skipped. "Kept" = some SUPPORTED proposition names the object.
retention = kept / pairs in gold; mirror rate = not kept / pairs outside gold; all-REJECTED = every proposition
naming the object is REJECTED. Gold is caption-derived (KTVIC train refs): in-sample dev only (CC-207 W6).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def counts(records) -> dict:
    from rescap.chair import objects_in

    c = dict.fromkeys(("keep_pos", "all_pos", "drop_neg", "rej_neg", "all_neg"), 0)
    for r in records:
        gold = set().union(*[set(objects_in(x)) for x in r["reference_captions"]])
        if not gold:
            continue
        by: dict[str, set] = {}
        for p in r["propositions"]:
            for o in set(objects_in(p["text_vi"])):
                by.setdefault(o, set()).add(p["verification"]["status"])
        for o, st in by.items():
            sup = "SUPPORTED" in st
            if o in gold:
                c["all_pos"] += 1
                c["keep_pos"] += sup
            else:
                c["all_neg"] += 1
                c["drop_neg"] += not sup
                c["rej_neg"] += st == {"REJECTED"}
    return c


def rates(c: dict) -> dict:
    return {"retention": 100 * c["keep_pos"] / max(c["all_pos"], 1),
            "mirror": 100 * c["drop_neg"] / max(c["all_neg"], 1),
            "all_rejected": 100 * c["rej_neg"] / max(c["all_neg"], 1)}


def main() -> int:
    recs = (json.loads(f.read_text(encoding="utf-8")) for f in sorted(Path(sys.argv[1]).glob("*.json")))
    c = counts(recs)
    r = rates(c)
    print(f"retention P(SUPPORTED|obj in refs) = {r['retention']:.1f} ({c['keep_pos']}/{c['all_pos']})")
    print(f"mirror not-SUPPORTED | obj not in refs = {r['mirror']:.1f}; all-REJECTED = {r['all_rejected']:.1f}"
          f" (n {c['all_neg']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
