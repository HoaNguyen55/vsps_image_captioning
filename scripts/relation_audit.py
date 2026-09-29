#!/usr/bin/env python
"""How many relation propositions actually reach the SFT supervision (Section III-B-3).

    python scripts/relation_audit.py --in $NCS_DATA/stage1_final \
        --sft data/supervision/sft.jsonl --out data/results/relation_audit.json

Replays the main system's detailed-mode selection (variant B: SUPPORTED only,
budget 9, junk-proposition filter) through the same functions build_dpo_data.py
uses, restricted to the images that have a detailed example in the shipped store.
CPU only; no model is called.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_dpo_data as b  # noqa: E402

RELATION_TYPES = ("relation", "spatial_relation")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--in", dest="src", required=True, help="stage-1 records after person_uncap.py")
    ap.add_argument("--sft", default="data/supervision/sft.jsonl")
    ap.add_argument("--out", default="data/results/relation_audit.json")
    args = ap.parse_args()

    b.SELECT_BUDGET[0] = 9
    b.CLEAN_PROPS[0] = True
    detailed = {
        str(r["image_id"]) for r in map(json.loads, Path(args.sft).read_text(encoding="utf-8").splitlines())
        if r.get("variant") != "short"
    }

    verdicts: Counter = Counter()
    selected: Counter = Counter()
    images_with_relation = 0
    n_images = 0
    stats: Counter = Counter()
    for f in sorted(Path(args.src).expanduser().glob("*.json")):
        rec = json.loads(f.read_text(encoding="utf-8"))
        for p in rec.get("propositions") or []:
            verdicts[(p.get("type"), b.verdict_of(p))] += 1
        if str(rec.get("image_id")) not in detailed:
            continue
        n_images += 1
        props = b.clean_props(list(rec.get("propositions") or []), stats)
        supported = [p for p in props if b.verdict_of(p) == "SUPPORTED"]
        chosen = b._select(supported, rec.get("entities") or [], stats, "B")
        types = Counter(str(p.get("type")) for p in chosen)
        selected.update(types)
        images_with_relation += any(types[t] for t in RELATION_TYPES)

    total = sum(selected.values())
    rel = sum(selected[t] for t in RELATION_TYPES)
    report = {
        "n_detailed_images": n_images,
        "selected_by_type": dict(selected),
        "selected_total": total,
        "relation_share_of_selected": round(rel / total, 4) if total else None,
        "images_with_any_relation": images_with_relation,
        "images_with_any_relation_share": round(images_with_relation / n_images, 4) if n_images else None,
        "verdicts_by_type": {f"{t}|{v}": n for (t, v), n in sorted(verdicts.items(), key=str)},
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "verdicts_by_type"}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
