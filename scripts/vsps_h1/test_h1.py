#!/usr/bin/env python
"""Synthetic selftest for VSPS H1 (no model, no image, no dataset text).

    python scripts/vsps_h1/test_h1.py
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
sys.path.insert(0, str(HERE))

from build_map import TABLE, coco_terms, key_of, map_noun  # noqa: E402
from detect_boxes import gdino_label_to_prompt, parse_line, read_lines, xyxy_to_xywh  # noqa: E402
from vote import decision, promote_uncertain_votes, vote, votes_and_boxes  # noqa: E402

from rescap.chair import norm_tone  # noqa: E402
from rescap.pipeline.verify import (SignalCalibration, Verdict, VerificationConfig, as_box,  # noqa: E402
                                    detector_vote, evidence_signals, verify)
from rescap.vlm.replay import ReplayVLM  # noqa: E402


class Size:
    size = (100, 100)


def ent(eid: str, bbox=None) -> dict:
    e = {"id": eid, "category_vi": "chó", "gender": {"value": "khong_xac_dinh", "evidence": "not_determinable"}}
    if bbox:
        e["bbox"] = bbox
    return e


def existence(pid: str, eid: str) -> dict:
    return {"id": pid, "type": "entity", "subject": {"entity_id": eid, "text_vi": "con chó", "head_noun_vi": "chó"},
            "text_vi": "Có một con chó", "epistemic": "OBSERVATION"}


def spatial(pid: str, rel: str) -> dict:
    return {"id": pid, "type": "spatial_relation",
            "subject": {"entity_id": "a", "text_vi": "con chó", "head_noun_vi": "chó"},
            "object": {"entity_id": "b", "text_vi": "con chó", "head_noun_vi": "chó"},
            "predicate": {"lemma_vi": "ở"}, "spatial_relation": {"relation_vi": rel, "frame_of_reference": "image_relative"},
            "text_vi": f"con chó {rel} con chó", "epistemic": "OBSERVATION"}


def run(entities, props, votes=None, config=None):
    for p in props:
        p["verification"] = {"status": None}
    verify(ReplayVLM([]), Size(), entities, props, config=config or VerificationConfig(), entity_votes=votes)
    return {p["id"]: p["verification"]["status"] for p in props}


def test_map() -> None:
    table = {norm_tone(k): v for k, v in TABLE.items()}
    coco = coco_terms()
    assert key_of("Một số  Xe Máy") == "xe máy"
    assert map_noun("hai người đàn ông", table, coco) == ("man", "table_canonical")
    assert map_noun("xanh", table, coco) == (None, "unmapped")
    assert map_noun("biển quảng", table, coco)[0] == "billboard"
    assert map_noun("hươu cao cổ", table, coco) == ("giraffe", "coco80")


def test_detector_plumbing() -> None:
    assert xyxy_to_xywh([10, 20, 40, 60]) == [10.0, 20.0, 30.0, 40.0]
    assert as_box(xyxy_to_xywh([10, 20, 40, 60])).cx == 25.0
    assert gdino_label_to_prompt("Traffic  Light", ["traffic light", "man"]) == "traffic light"
    assert gdino_label_to_prompt("man woman", ["man", "dog"]) == "man"
    assert gdino_label_to_prompt("cat", ["man", "dog"]) is None


def test_vote() -> None:
    box = [[0, 0, 10, 10, 0.9]]
    assert vote(box, box, True) == "SUPPORTED"
    assert vote([], [], True) == "REFUTED"
    assert vote(box, [], True) == "UNCERTAIN"
    assert vote(box, box, False) == "UNCERTAIN"
    det = {"entities": {"a": "dog", "b": "dog", "c": "dog", "d": None},
           "prompts": {"dog": {"gdino": [[0, 0, 5, 5, 0.4], [50, 0, 5, 5, 0.8]], "owlv2": box}}}
    votes, boxes = votes_and_boxes(det)
    assert votes == {"a": "SUPPORTED", "b": "SUPPORTED", "c": "SUPPORTED", "d": "UNCERTAIN"}
    assert boxes == {"a": [50, 0, 5, 5], "b": [0, 0, 5, 5]}  # distinct instances, best first; c has none left
    fun = {"R0": {"supported": {"R": 36.5, "P": 41.1}}, "R2": {"supported": {"R": 41.5, "P": 39.1}},
           "R3": {"supported": {"R": 43.0, "P": 36.0}}}
    assert decision(fun, subset_gain=5.2) == {
        "recall_gain_pts": 5.0, "precision_drop_pts": 2.0, "r2_minus_r3_precision_pts": 3.1,
        "exact_replay_recall_gain_pts": 5.2, "verdict": "GO", "judge_read_required": []}
    fun["R3"]["supported"]["P"] = 38.0
    assert decision(fun, subset_gain=4.0)["judge_read_required"] == [
        "R2-R3 supported precision < +2.0", "recall gain on exact-replay images < +5.0"]
    fun["R2"]["supported"]["P"] = 39.0
    assert decision(fun)["verdict"] == "STOP"
    assert decision(fun, complete=False) == {"verdict": "INCOMPLETE"}
    assert parse_line('{"image_id": "1"') is None and parse_line('{"image_id": "1"}') == {"image_id": "1"}


def test_line_pins() -> None:
    line = {"image_id": "1", "config_sha256": "c", "map_sha256": "m", "device": "cpu"}
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "boxes.jsonl"
        assert read_lines(path, "c", "m", "cpu") == {}
        path.write_text(json.dumps(line) + "\n" + '{"image_id": "2", "trunc')
        assert list(read_lines(path, "c", "m", "cpu")) == ["1"]  # matching line: resume skips it
        for args in (("c2", "m", "cpu"), ("c", "m2", "cpu"), ("c", "m", "cuda")):
            try:
                read_lines(path, *args)
            except SystemExit:
                continue
            raise AssertionError(f"line accepted under {args}")
        path.write_text(json.dumps(line) + "\n" + json.dumps(dict(line, image_id="2", device="cuda")) + "\n")
        try:
            read_lines(path, "c", "m")
        except SystemExit:
            return
        raise AssertionError("mixed devices accepted")


def test_r3_falsifier() -> None:
    def status(pid, eid, st):
        return dict(existence(pid, eid), verification={"status": st})
    r1 = {"propositions": [status("P1", "a", "UNCERTAIN"), status("P2", "b", "REJECTED"),
                           status("P3", "c", "SUPPORTED"), dict(spatial("P4", "trên"), verification={"status": "UNCERTAIN"})]}
    votes = promote_uncertain_votes(r1)
    assert votes == {"a": "SUPPORTED"}
    out = run([ent("a"), ent("b")], [existence("P1", "a"), existence("P2", "b")], votes)
    assert out == {"P1": "SUPPORTED", "P2": "UNCERTAIN"}  # b has no vote: verifier verdict kept


def test_verify_hooks() -> None:
    assert detector_vote(Verdict.UNCERTAIN, "gate", "UNCERTAIN") == (Verdict.UNCERTAIN, "gate")
    assert detector_vote(Verdict.REJECTED, "no_support", "SUPPORTED") == (Verdict.UNCERTAIN, "detector_dispute")
    assert detector_vote(Verdict.UNCERTAIN, "gate", "REFUTED") == (Verdict.UNCERTAIN, "gate")
    # no probe answers: the existence claim cannot be settled ...
    assert run([ent("a")], [existence("P1", "a")]) == {"P1": "UNCERTAIN"}
    # ... unless both detectors see it
    assert run([ent("a")], [existence("P1", "a")], votes={"a": "SUPPORTED"}) == {"P1": "SUPPORTED"}
    # geometry decides left/right from boxes once both entities exist; it never decides depth
    ents = [ent("a", [0, 0, 30, 30]), ent("b", [60, 0, 30, 30])]
    h1 = VerificationConfig(absent_bbox_is_evidence=False)
    both = {"a": "SUPPORTED", "b": "SUPPORTED"}
    out = run(ents, [existence("P1", "a"), existence("P2", "b"), spatial("P3", "bên phải")], both, h1)
    assert out["P3"] == "REJECTED", out
    props = [existence("P1", "a"), existence("P2", "b"), spatial("P3", "phía sau")]
    run(ents, props, both, h1)
    assert props[2]["spatial_relation"]["geometric_check"]["consistent"] is None
    # absent box: 0.0 under v1 when other entities have one, ⊥ under H1
    ents = [ent("a", [0, 0, 10, 10]), ent("b")]
    for absent_is_evidence, expect in ((True, 0.0), (False, None)):
        signals = evidence_signals(existence("P2", "b"), ents[1], Size(), ents, probe=None, probe_failed=False,
                                   calibration=SignalCalibration(), absent_bbox_is_evidence=absent_is_evidence)
        assert next(s.value for s in signals if s.name == "bbox") == expect
    assert "H1-bbox" in h1.resolved_decision_rule_version()


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"ok {name}")
