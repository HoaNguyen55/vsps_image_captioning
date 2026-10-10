#!/usr/bin/env python
"""Object recall funnel: precision / recall at each step from proposals to supervision.

    python scripts/recall_funnel.py --in $NCS_DATA/stage1_final --sft data/supervision/sft.jsonl

Gold is the set of lexicon objects (the 113-entry CHAIR-vi lexicon) in each record's
KTVIC train references. For every step -- all proposals, not REJECTED, SUPPORTED,
SUPPORTED and selected, the rendered detailed SFT caption -- the script counts the object
classes that survive and reports P = sum|M & G| / sum|M|, R = mean |M & G| / |G| over
images with non-empty gold, and objects per image. It shows where recall is lost.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

STAGES = ("all_props", "not_rejected", "supported", "supported_selected", "sft_caption")


def stage_texts(rec: dict, caption: str) -> dict[str, list[str]]:
    props = rec["propositions"]
    sel = set(rec.get("selected_ids") or [])

    def status(p: dict) -> str:
        return p["verification"]["status"]

    return {
        "all_props": [p["text_vi"] for p in props],
        "not_rejected": [p["text_vi"] for p in props if status(p) != "REJECTED"],
        "supported": [p["text_vi"] for p in props if status(p) == "SUPPORTED"],
        "supported_selected": [p["text_vi"] for p in props
                               if status(p) == "SUPPORTED" and p["id"] in sel],
        "sft_caption": [caption],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="src", required=True, help="directory of Phase-1a records (*.json)")
    ap.add_argument("--sft", default=str(ROOT / "data" / "supervision" / "sft.jsonl"))
    args = ap.parse_args()

    from rescap.chair import objects_in

    captions = {}
    for line in Path(args.sft).read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if "Mô tả chi tiết" in r["prompt"]:
            captions[r["image_id"]] = r["response"]

    tp = dict.fromkeys(STAGES, 0)
    mentioned = dict.fromkeys(STAGES, 0)
    recalls: dict[str, list[float]] = {k: [] for k in STAGES}
    for f in sorted(Path(args.src).expanduser().glob("*.json")):
        rec = json.loads(f.read_text(encoding="utf-8"))
        gold = set().union(*[set(objects_in(c)) for c in rec["reference_captions"]])
        if not gold:
            continue
        for k, texts in stage_texts(rec, captions.get(rec["image_id"], "")).items():
            m = set().union(*[set(objects_in(t)) for t in texts])
            tp[k] += len(m & gold)
            mentioned[k] += len(m)
            recalls[k].append(len(m & gold) / len(gold))

    if not recalls["all_props"]:
        raise SystemExit(f"no records with gold objects under {args.src}")
    for k in STAGES:
        n = len(recalls[k])
        print(f"{k:20s} P={100 * tp[k] / max(mentioned[k], 1):5.1f}  "
              f"R={100 * statistics.mean(recalls[k]):5.1f}  obj/img={mentioned[k] / n:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
