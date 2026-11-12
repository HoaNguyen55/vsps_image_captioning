#!/usr/bin/env python3
"""Overlap-only assignment for the second annotator (plan v1.1 section 4; CC-327 L1).

Subset of the committed base assignment by overlap_images.txt: same screens, same order, same qids, nothing added.
Reads only the public base copies (never key.json, never a label file). Prints counts and sha256 only.

    python3 -B tools/obj_rater/build_overlap.py --out ~/vsps_labels/xm600_gold_r2
    python3 -B tools/obj_rater/server.py --dir ~/vsps_labels/xm600_gold_r2 --annotator R2 --port 8793
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[2] / "manuscript" / "prereg" / "2026-11-11_xm600_gold_completion"
PINS = {"assignment.json": "55e07337218acc820aafc27659e499ade4ae622cc6eaf41be2f7bb3df510cb2d",
        "practice.json": "e0ed805b31fc623df52f40d7e517cd22f8474fb043d00cb0a167d07ac4fcbbf7",
        "overlap_images.txt": "4f9719667c8a9294dc8cadc9565a048b9b7008ee0c1ecb924317550ba5278273"}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def build(out: Path) -> dict:
    out = out.expanduser().resolve()
    if str(out).startswith("/mnt") or out.exists():
        raise SystemExit(f"REFUSED: {out} is under /mnt or already exists")
    for name, pin in PINS.items():
        if sha(BASE / name) != pin:
            raise SystemExit(f"STOP: base {name} differs from its pin")
    base = json.loads((BASE / "assignment.json").read_text(encoding="utf-8"))
    overlap = set((BASE / "overlap_images.txt").read_text(encoding="utf-8").split())
    screens = [s for s in base["screens"] if Path(s["image"]).stem in overlap]
    assert {Path(s["image"]).stem for s in screens} == overlap and len(overlap) == 150
    base_qids = {q["qid"] for s in base["screens"] for q in s["q"]}
    qids = [q["qid"] for s in screens for q in s["q"]]
    assert len(qids) == len(set(qids)) and set(qids) <= base_qids
    n_base_overlap = sum(len(s["q"]) for s in base["screens"] if s["sid"].split("-", 1)[1] in overlap)
    assert len(qids) == n_base_overlap  # every question of the overlap images, nothing else
    meta = {**base["meta"], "name": "xm600_gold_overlap_r2", "n_screens": len(screens), "n_questions": len(qids)}
    out.mkdir(parents=True)
    (out / "assignment.json").write_text(
        json.dumps({"meta": meta, "screens": screens}, ensure_ascii=False, sort_keys=True, indent=1), encoding="utf-8")
    (out / "practice.json").write_bytes((BASE / "practice.json").read_bytes())
    rec = {"counts": {"overlap_images": len(overlap), "images_with_screens": len({s["image"] for s in screens}),
                      "screens": len(screens), "questions": len(qids),
                      "screens_by_part": dict(sorted(Counter(str(s["part"]) for s in screens).items())),
                      "questions_by_part": dict(sorted(Counter(str(s["part"]) for s in screens for _ in s["q"]).items()))},
           "inputs_sha256": {**PINS, "tools/obj_rater/build_overlap.py": sha(Path(__file__))},
           "outputs_sha256": {n: sha(out / n) for n in ("assignment.json", "practice.json")}}
    (out / "BUILD_OVERLAP.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    return rec


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    print(json.dumps(build(Path(ap.parse_args().out)), ensure_ascii=False, indent=1))
