#!/usr/bin/env python3
"""CPU selftest for VSPS-J M0, no weights and no data (numpy + torch + torchvision):
    python3 -I scripts/vsps_j_m0/test_m0.py      (also run by `m0.py selftest` and `m0_job.sh`)"""
from __future__ import annotations

import math
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from m0 import (ELIGIBLE, SEED, chat_args, claim_type, custody_sets, demo_pixels, pick_demos, pick_smoke,  # noqa: E402
                probe, projection_h, question, segments, sha_refused, smoke_verdict, text_ok)
from m0_stats import SEED as STATS_SEED, auroc, bootstrap, decide, prec_at_recall, stats, tau_matched  # noqa: E402


def main() -> None:
    import types

    import numpy as np
    import torch

    assert SEED == STATS_SEED == 20261031
    # rules
    assert claim_type("There are two dogs") == "count" and claim_type("a red bus") == "attribute"
    assert claim_type("a man holding an umbrella") == "relation" and claim_type("A kite") == "object"
    assert claim_type("in front of the house") == "relation" and claim_type("only") == "object"
    assert question("  The dog is  brown. ") == 'Có đúng là "The dog is brown" không'
    recs = [{"image": "COCO_val2014_000000000042.jpg", "annotations": [
        {"label": "ACCURATE", "text": "A dog."}, {"label": "INACCURATE", "text": "two cats"},
        {"label": "ANALYSIS", "text": "x"}, {"label": "UNSURE", "text": "y"}, {"label": "ACCURATE", "text": " ."}]},
        {"image": "COCO_val2014_000000000043.jpg", "annotations": []}]
    segs, ex = segments(recs)
    assert [(s["seg"], s["y"], s["image"]) for s in segs] == [(0, 0, 42), (1, 1, 42)], segs
    assert ex == Counter({"ANALYSIS": 1, "UNSURE": 1, "no_word_character_ACCURATE": 1, "record_without_spans": 1}), ex

    # chat arguments: 0 demos == yes_no_logit's string; 2 demos -> 3 placeholders in order
    h, q, npl = chat_args("Có đúng là \"x\" không", [], [], 3)
    assert h is None and npl is None and q == "<image>\n" + "Có đúng là \"x\" không? Chỉ trả lời 'có' hoặc 'không'."
    h, q, npl = chat_args("Q", [("D1", "Có."), ("D2", "Không.")], [1, 2], 3)
    assert npl == [1, 2, 3] and [a for _, a in h] == ["Có.", "Không."]
    assert sum(t.count("<image>") for t, _ in h) + q.count("<image>") == len(npl) and h[0][0].startswith("<image>\nD1")

    # probe() against a fake model that applies the pinned chat() placeholder logic
    class LM:
        def generate(self, **k):
            assert k["output_scores"] and k["return_dict_in_generate"] and k["max_new_tokens"] == 1
            logits = torch.full((1, 10), -30.0)
            logits[0, 1], logits[0, 2], logits[0, 9] = math.log(3), math.log(1), 0.0  # yes 3 : no 1 : other 1
            return types.SimpleNamespace(scores=(logits,), sequences=torch.tensor([[1]]))

    class Model:
        language_model = LM()

        def chat(self, tok, pv, question, cfg, history=None, num_patches_list=None):
            turns = [t for qa in (history or []) for t in qa] + [question]
            npl = num_patches_list or [pv.shape[0]]
            assert sum(t.count("<image>") for t in turns) == len(npl) and len(pv) == sum(npl)
            self.seen = pv[:, 0, 0, 0].tolist()
            self.language_model.generate(max_new_tokens=cfg["max_new_tokens"])
            return "Có"

    ad = types.SimpleNamespace(_model=Model(), _tokenizer=None, _yes_no_ids=lambda: ([1], [2]))
    orig = ad._model.language_model.generate
    pv = lambda v, n: torch.full((n, 3, 2, 2), float(v))  # noqa: E731
    demos = ((pv(1, 1), "D1", "Có."), (pv(2, 2), "D2", "Không."))
    text, p, m = probe(ad, pv(3, 3), "Q", demos)
    assert ad._model.seen == [1, 2, 2, 3, 3, 3] and text == "Có"
    assert abs(p - 0.75) < 1e-6 and abs(m - 0.8) < 1e-4, (p, m)
    assert ad._model.language_model.generate == orig
    assert abs(probe(ad, pv(3, 3), "Q")[1] - 0.75) < 1e-6 and ad._model.seen == [3, 3, 3]

    # first-token text rule and one-tile demos
    assert text_ok("C") and text_ok("Kh") and text_ok("Không.") and not text_ok("Yes") and not text_ok("")
    from PIL import Image

    assert demo_pixels(Image.new("RGB", (640, 427)), "float32", "cpu").shape == (1, 3, 448, 448)

    # smoke verdict
    good = [{"arm": a, "p_yes": 0.3, "mass": 0.9, "text": "Không."} for a in "AB" for _ in range(10)]
    v = smoke_verdict(good, [0.0])
    assert v["A"]["ok"] and v["B"]["ok"] and v["equiv_ok"]
    bad_b = good[:10] + [{"arm": "B", "p_yes": 0.5, "mass": 0.1, "text": "Yes"}] * 10
    v = smoke_verdict(bad_b, [0.0])
    assert v["A"]["ok"] and not v["B"]["ok"]
    assert smoke_verdict(good, [1e-3])["A"]["ok"] and not smoke_verdict(good, [2e-3])["A"]["ok"]
    assert not smoke_verdict([dict(good[0], p_yes=float("nan"))] + good[1:], [0.0])["A"]["ok"]
    assert abs(projection_h(1.0, {"A": 3600, "B": 3600}, {"A": 0.5, "B": 1.0}) - 2.5) < 1e-9

    # custody
    C = custody_sets({1, 2, 3, 4, 8}, {4, 5, 6, 7, 9}, owned={2, 6}, refused={3, 8, 9},
                     ksplit={3: "test", 7: "test", 1: "restval"})
    assert C["drop"] == {2, 6} and C["probe"] == {1, 3, 4, 8} and C["ktest"] == {3} and C["held"] == {3, 8}
    assert C["op"] == {1, 4} and C["demo_pool"] == {5}
    assert sha_refused({1: "aa", 3: "bb", 4: "cc"}, {"bb", "cc"}, held={3}) == [4]

    # demos / smoke picks are deterministic and respect the pool
    ts = [{"rec": r, "seg": 0, "image": 100 + r, "label": "ACCURATE" if r % 2 else "INACCURATE",
           "text": "w " * (6 + r % 3)} for r in range(40)]
    d1 = pick_demos(ts, {100 + r for r in range(40)})
    assert d1 == pick_demos(ts, {100 + r for r in range(40)}) and {d["label"] for d in d1} == set(ELIGIBLE)
    assert d1[0]["image"] != d1[1]["image"]
    sm = pick_smoke(ts, {100 + r for r in range(10)}, 5)
    assert len(sm) == 5 and all(100 <= s["image"] < 110 for s in sm)

    # statistics
    y = np.array([1, 1, 0, 0, 1, 0])
    assert auroc(np.array([0.1, 0.2, 0.8, 0.9, 0.3, 0.7]), y) == 1.0
    assert auroc(np.full(6, 0.5), y) == 0.5
    assert abs(auroc(np.array([0.1, 0.8, 0.2, 0.9, 0.5, 0.5]), y) - 5.5 / 9) < 1e-12
    pB = np.array([0.1, 0.2, 0.3, 0.4, 0.4, 0.9])  # labels 1,1,0,0,1,0
    assert tau_matched(pB, y, 1.0) == 0.2 and tau_matched(pB, y, 0.6) == 0.4 and tau_matched(pB, y, 0.61) == 0.2
    assert tau_matched(np.array([0.1]), np.array([0]), 0.5) is None
    s = stats(np.array([0.1, 0.6, 0.4, 0.9, 0.3, 0.7]), pB, y)
    assert abs(s["R_A"] - 2 / 3) < 1e-12 and abs(s["P_A"] - 2 / 3) < 1e-12 and s["tau_B"] == 0.2  # 0.3 also reaches 2/3 but adds a false flag
    assert abs(s["R_B"] - 2 / 3) < 1e-12 and abs(s["dR_pts"]) < 1e-9 and s["P_B"] == 1.0
    assert prec_at_recall(pB, y) == 0.6
    rng = np.random.default_rng(0)
    yy = rng.integers(0, 2, 400)
    pa, pb = rng.random(400), np.clip(rng.random(400) - 0.3 * yy, 0, 1)
    gi = np.repeat(np.arange(100), 4)
    c1, c2 = bootstrap(pa, pb, yy, gi, B=50), bootstrap(pa, pb, yy, gi, B=50)
    assert c1 == c2 and c1["dR_pts"][0] <= c1["dR_pts"][1]
    assert decide({"dR_pts": 3.0, "AUROC_A": 0.6, "AUROC_B": 0.7}, {"dR_pts": [0.1, 6]}) == \
        {"few_shot": "KEEP", "detector": "CONTINUE"}
    assert decide({"dR_pts": 2.9, "AUROC_A": 0.6, "AUROC_B": 0.64}, {"dR_pts": [0.1, 6]}) == \
        {"few_shot": "DROP", "detector": "STOP_PIVOT"}
    assert decide({"dR_pts": 5.0, "AUROC_A": 0.7, "AUROC_B": 0.7}, {"dR_pts": [-0.1, 9]})["few_shot"] == "DROP"
    assert decide({"AUROC_A": 0.6}, {})["few_shot"] == "N/A_ARM_B_DROPPED"
    stop_cases()
    print("selftest ok")


def refused(fn) -> bool:
    try:
        fn()
    except SystemExit as e:
        return str(e).startswith("REFUSED")
    return False


def stop_cases() -> None:
    """CC-208 W1: a stopped run is never resumed or scored; a crash with no marker resumes."""
    import hashlib
    import json
    import tempfile
    import time

    import m0

    ids = lambda n: {int(x) for x in (m0.PDIR / n).read_text().split()}  # noqa: E731
    order = m0.image_order(ids("val_ids.txt") - ids("dropped_ids.txt"))
    val = [{"image": f"COCO_val2014_{i:012d}.jpg", "annotations": [{"label": "INACCURATE", "text": "two dogs"}]}
           for i in order]
    ad, img = types_ns(_pixel_values=lambda im: None), (lambda i: None)
    calls = []
    m0.probe = lambda *a, **k: calls.append(1) or ("có", 0.7, 0.99)  # fake model, no weights

    def fresh(t0_shift: float = 0.0) -> Path:
        out = Path(tempfile.mkdtemp())
        (out / "launch.json").write_text(json.dumps({"t0": time.time() - t0_shift}))
        return out

    slow, fast = {"arm_b_dropped": False, "sec_median": {"A": 1e6, "B": 1e6}}, \
        {"arm_b_dropped": False, "sec_median": {"A": 0.0, "B": 0.0}}
    # the CC-208 simulation: pre-val PROJECTION_STOP, then the same call again -> refused, nothing decoded
    out = fresh()
    assert m0.run_val(ad, val, img, (), slow, out) == 3 and (out / m0.STOP).exists() and not calls
    assert refused(lambda: m0.run_val(ad, val, img, (), fast, out)) and not calls
    # a stop record without a marker also refuses
    (out / m0.STOP).unlink()
    assert refused(lambda: m0.run_val(ad, val, img, (), fast, out)) and not calls
    # cap checked before an image (a resumed run past the pre-val check): rc 4, no decode
    s0 = m0.segments(val)[0][0]
    row0 = json.dumps({"rec": s0["rec"], "seg": s0["seg"], "image": s0["image"], "arm": "A", "n_img": 1,
                       "p_yes": 0.7, "mass": 0.99, "text": "có", "sec": 0.1}) + "\n"
    out = fresh(t0_shift=6 * 3600)
    (out / "probes.jsonl").write_text(row0)
    assert m0.run_val(ad, val, img, (), fast, out) == 4 and not calls
    assert json.loads((out / m0.STOP).read_text())["n_img"] == 1
    # smoke fault record refuses
    out = fresh()
    (out / "smoke.json").write_text(json.dumps({"fault": True}))
    assert refused(lambda: m0.refuse_if_stopped(out))
    # crash with no marker: resume allowed, completes
    out = fresh()
    (out / "probes.jsonl").write_text(row0)
    assert m0.run_val(ad, val, img, (), fast, out) == 0 and len(calls) == 2 * len(order) - 1
    pf = out / "probes.jsonl"
    seal = lambda: (out / "probes.jsonl.sha256").write_text(  # noqa: E731
        hashlib.sha256(pf.read_bytes()).hexdigest() + "  probes.jsonl\n")
    seal()
    assert len(m0.check_scorable(out)) == 2 * len(order)
    # score refusals: sha mismatch, NaN row, marker
    pf.write_text(pf.read_text() + json.dumps({"rec": 0, "seg": 9, "arm": "A", "p_yes": float("nan")}) + "\n")
    assert refused(lambda: m0.check_scorable(out))
    seal()
    assert refused(lambda: m0.check_scorable(out))
    pf.write_text("".join(pf.read_text().splitlines(keepends=True)[:-1]))
    seal()
    m0.check_scorable(out)
    m0.halt(out, 4, "CAP_STOP test", 7)
    assert refused(lambda: m0.check_scorable(out))
    m0.probe = probe


def types_ns(**k):
    import types

    return types.SimpleNamespace(**k)


if __name__ == "__main__":
    main()
