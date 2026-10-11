#!/usr/bin/env python
"""Lift UNCERTAIN to SUPPORTED where the SAVED dual-probe evidence is unanimous.

    python scripts/unanimous_uncap.py --in <stage1_person> --out <stage1_unanimous>
    python scripts/unanimous_uncap.py --self-check

Run after person_uncap.py. Finding (2026-10-11, 3,701 train records): after the
gender ceiling is lifted, the remaining UNCERTAIN entity/action/attribute
propositions whose evidence is unanimous match the KTVIC references about as well
as SUPPORTED ones (object precision 38-39 vs 40-42), and they carry 5-11 recall
points. Their verdict is UNCERTAIN because of the untuned decision rule
(`v1.0-doc07-UNTUNED`), not because any sample disagreed.

CRITERIA (pre-registered, no explanation-text parsing, no model calls):
 1. status == UNCERTAIN, type in {entity, action, attribute};
 2. external_knowledge.inference_type in {none, None};
 3. person_uncap.evidence_unanimous: every affirming sample yes, every negating
    sample no, grounding_score >= 0.9;
 4. for action/attribute: the subject entity's existence is SUPPORTED (before or
    after this pass), so no unverified referent is asserted through it.
Relations and counts are never lifted (relations: 18% reference precision even
when unanimous; counts need an exact number nobody re-checked). Lifted
propositions carry `backoff{kind: "unanimous_uncap"}`. The input is not modified.
"""
from __future__ import annotations

import argparse
import copy
import json
from collections import Counter
from pathlib import Path

from person_uncap import evidence_unanimous

TYPES = ("entity", "action", "attribute")


def _liftable(p: dict) -> bool:
    ek = (p.get("evidence") or {}).get("external_knowledge") or {}
    return ((p.get("verification") or {}).get("status") == "UNCERTAIN" and p.get("type") in TYPES
            and ek.get("inference_type") in (None, "none") and evidence_unanimous(p)[0])


def uncap(record: dict, stats: Counter) -> dict:
    out = copy.deepcopy(record)
    props = out.get("propositions") or []
    lift = [p for p in props if _liftable(p)]
    exists = {(p.get("subject") or {}).get("entity_id") for p in props
              if p.get("type") == "entity" and (p in lift or p["verification"]["status"] == "SUPPORTED")}
    for p in lift:
        if p["type"] != "entity" and (p.get("subject") or {}).get("entity_id") not in exists:
            stats["skip:subject_unconfirmed"] += 1
            continue
        p["verification"]["status"] = "SUPPORTED"
        p["backoff"] = {"kind": "unanimous_uncap"}
        stats[f"lifted:{p['type']}"] += 1
    return out


def self_check() -> None:
    def prop(pid, ptype, eid, status="UNCERTAIN", yes=("Có.",) * 5):
        return {"id": pid, "type": ptype, "subject": {"entity_id": eid},
                "verification": {"status": status},
                "evidence": {"external_knowledge": {"inference_type": "none"},
                             "visual_grounding": {"grounding_score": 0.95},
                             "probes": [{"polarity": "affirms", "samples": list(yes)},
                                        {"polarity": "refutes", "samples": ["Không."] * 5}]}}
    rec = {"propositions": [prop("P1", "entity", "e1"), prop("P2", "action", "e1"),
                            prop("P3", "action", "e2"), prop("P4", "entity", "e3", yes=("Có.",) * 4 + ("Không.",)),
                            prop("P5", "relation", "e1")]}
    st = Counter()
    got = {p["id"]: p["verification"]["status"] for p in uncap(rec, st)["propositions"]}
    assert got == {"P1": "SUPPORTED", "P2": "SUPPORTED", "P3": "UNCERTAIN", "P4": "UNCERTAIN",
                   "P5": "UNCERTAIN"}, got
    assert rec["propositions"][0]["verification"]["status"] == "UNCERTAIN"
    print("self-check OK")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="src", required=True)
    ap.add_argument("--out", dest="dst", required=True)
    args = ap.parse_args()
    src, dst = Path(args.src).expanduser(), Path(args.dst).expanduser()
    dst.mkdir(parents=True, exist_ok=True)
    stats = Counter()
    for f in sorted(src.glob("*.json")):
        rec = uncap(json.loads(f.read_text(encoding="utf-8")), stats)
        (dst / f.name).write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
        stats["records"] += 1
    print(json.dumps(dict(stats), indent=1))
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(self_check() if "--self-check" in sys.argv else main())
