"""O31 self-tests: synthetic fixtures only (no dataset caption, no image). Run: run_tests.sh.

The package is imported from $O31_SRC (default ./src) so mutants.py can point it at a mutated copy.
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import math
import os
import random
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, os.environ.get("O31_SRC", str(HERE / "src")))

import numpy as np  # noqa: E402

from o31 import REPO, REUSED, decode, extract, gate, metrics, no_forbidden, overlap, probe, repo, store, train, verify  # noqa: E402
from o31 import a8, points, t4, vcoco  # noqa: E402  PKG1 (ERRATUM_O31_4, ERRATUM_O31_5)
from o31.verify import REJECTED, SUPPORTED, UNCERTAIN  # noqa: E402

V, I = ("vintern",), ("vintern", "internvl3")
VIN = "5CD-AI/Vintern-1B-v3_5"  # the model string recorded in the stage-1 records (erratum E3)


# ------------------------------------------------------------------ verify
def test_grid_30_points():
    g = verify.grid()
    assert len(g) == 30 and len(set(g)) == 30 and all(r < a for a, r, _ in g)
    assert {f for *_, f in g} == {V, I}


def test_score_and_nan():
    assert abs(verify.score(0.3, 0.1) - 0.75) < 1e-12 and math.isnan(verify.score(0.0, 0.0))


def test_smoke_rule():
    assert verify.smoke_ok([0.5] * 20) and not verify.smoke_ok([0.49] * 20)
    assert not verify.smoke_ok([0.9] * 19)
    assert verify.smoke_ok([0.9] * 10 + [0.1] * 9 + [0.9] + [0.0] * 30)  # only the first 20 count


def test_combine_any_yes_supports():
    assert verify.combine({"vintern": 0.05, "internvl3": 0.95}, I, 0.7, 0.2) == SUPPORTED
    assert verify.combine({"vintern": 0.5, "internvl3": 0.5}, I, 0.7, 0.2) == UNCERTAIN


def test_combine_reject_needs_all_families():
    assert verify.combine({"vintern": 0.05, "internvl3": 0.5}, I, 0.7, 0.2) == UNCERTAIN
    assert verify.combine({"vintern": 0.05, "internvl3": 0.1}, I, 0.7, 0.2) == REJECTED
    assert verify.combine({"vintern": 0.05}, V, 0.7, 0.2) == REJECTED


def test_combine_missing_or_nan_blocks_reject():
    assert verify.combine({"vintern": 0.01}, I, 0.7, 0.2) == UNCERTAIN
    assert verify.combine({"vintern": 0.01, "internvl3": float("nan")}, I, 0.7, 0.2) == UNCERTAIN
    assert verify.combine({}, V, 0.7, 0.2) == UNCERTAIN


def test_combine_thresholds_inclusive():
    assert verify.combine({"vintern": 0.7}, V, 0.7, 0.2) == SUPPORTED
    assert verify.combine({"vintern": 0.2}, V, 0.7, 0.2) == REJECTED


def test_combine_spatial_always_uncertain():
    assert verify.combine({"vintern": 0.99}, V, 0.5, 0.1, "spatial_relation") == UNCERTAIN
    assert verify.combine({"vintern": 0.01}, V, 0.5, 0.1, "spatial_relation") == UNCERTAIN


def test_combine_tau_order_enforced():
    for a, r in ((0.5, 0.5), (0.3, 0.5)):
        try:
            verify.combine({"vintern": 0.4}, V, a, r)
        except ValueError:
            continue
        raise AssertionError("tau_rej >= tau_acc accepted")


def test_combine_equals_max_rule_when_all_present():
    rng = random.Random(1)
    for _ in range(2000):
        s = {"vintern": rng.random(), "internvl3": rng.random()}
        a, r, _f = rng.choice(verify.grid()[15:])
        mx = max(s.values())
        want = SUPPORTED if mx >= a else REJECTED if mx <= r else UNCERTAIN
        assert verify.combine(s, I, a, r) == want


def _rec():
    def p(pid, typ, q, st="SUPPORTED"):
        ev = {"probes": [{"model": VIN, "question_vi": q}, {"model": VIN, "question_vi": q + " không"},
                         {"model": "Qwen/Qwen2.5-VL-7B-Instruct", "question_vi": "khác?"}]} if q else {}
        return {"id": pid, "type": typ, "text_vi": "x", "evidence": ev, "verification": {"status": st}}
    return {"image_id": "1", "propositions": [p("P1", "entity", "Có con chó không?"),
                                              p("P2", "spatial_relation", "Cái ghế ở bên trái?"),
                                              p("P3", "entity", None, "REJECTED"),
                                              p("P4", "entity", None, "SUPPORTED")]}


def test_apply_states_keys_and_copy():
    rec = _rec()
    tab = {"vintern": {verify.qkey("Có con chó không?"): 0.1, verify.qkey("Cái ghế ở bên trái?"): 0.99}}
    out, n = verify.apply_states(rec, tab, V, 0.7, 0.2)
    # E3: no Q+ -> the recorded status stays (P3 REJECTED, P4 SUPPORTED, the latter flagged for a FAULT)
    assert [p["verification"]["status"] for p in out["propositions"]] == [REJECTED, UNCERTAIN, REJECTED, SUPPORTED]
    assert n["no_q"] == 2 and n["no_q_not_rejected"] == 1 and n["miss"] == 0
    assert rec["propositions"][0]["verification"]["status"] == SUPPORTED
    assert verify.affirmative_key(rec["propositions"][0]) == "có con chó không"
    assert verify.affirmative_key({"evidence": {"probes": [{"model": "vintern-1b", "question_vi": "Có chó?"}]}}) is None


def test_fair_model_is_the_e1b_constant():
    import ast
    src = (REPO / "scripts/vsps_j_m0/m0.py").read_text(encoding="utf-8")
    node = next(n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "MODEL" for t in n.targets))
    model = ast.literal_eval(node.value)
    assert verify.FAIR_MODEL == model["repo"] == VIN


# ------------------------------------------------------------------ extract
def test_terms_equal_repo_loader():
    repo()
    import score_coco_probe as sc
    assert extract.load_terms() == sc.load_vi_terms()


def test_mentions_order_and_set():
    cap = "Một con chó nằm cạnh chiếc ô tô, phía sau có một người đứng."
    assert extract.ordered_classes(cap) == ["dog", "car", "person"]
    props = extract.entity_propositions(cap)
    assert [p["order"] for p in props] == [0, 1, 2] and all(p["type"] == "entity" for p in props)


def test_mentions_consumption():
    assert extract.ordered_classes("Chiếc ô tô đỏ.") == ["car"]  # not also bowl (tô)
    assert "chair" not in extract.ordered_classes("Một chiếc ghế dài.")


def test_en_classes_consume_phrases():
    assert extract.en_classes("Robot man juggles one hot dog upward.") == {"person", "hot dog"}
    assert extract.en_classes("Frozen hot dog versus purple dog.") == {"hot dog", "dog"}


def test_mentions_random_equivalence():
    repo()
    import score_coco_probe as sc
    terms = [t for t, _ in extract.load_terms()]
    rng = random.Random(7)
    for _ in range(300):
        cap = " ".join(rng.choice(["Có", "một", "và", "cạnh", ",", "đang", "trên"]) + " " + rng.choice(terms)
                       for _ in range(rng.randint(1, 6)))
        ms = extract.mentions(cap, check=False)
        assert {m["cls"] for m in ms} == sc.vi_objects(cap, extract.load_terms())
        assert [m["start"] for m in ms] == sorted(m["start"] for m in ms)


# ------------------------------------------------------------------ store
def test_budget_clip_ceil():
    assert [store.budget(n) for n in (0, 1, 3, 4, 7, 9, 10, 20)] == [5, 5, 5, 6, 11, 14, 15, 15]


def test_n_supp_entities():
    def p(pid, eid, typ="entity", st="SUPPORTED"):
        return {"id": pid, "type": typ, "subject": {"entity_id": eid}, "verification": {"status": st}}
    rec = {"propositions": [p("a", "e1"), p("b", "e1"), p("c", "e2"), p("d", "e3", st="UNCERTAIN"),
                            p("e", "e4", typ="attribute"), {"id": "f", "type": "entity", "verification": {"status": "SUPPORTED"}}]}
    assert store.n_supp_entities(rec) == 3


def test_variant_b_logic():
    from collections import Counter
    c = Counter()
    sft = {"response": "A", "n_uncertain": 2}
    assert store.variant_b(sft, [{"pair_type": "A>B_x", "rejected": "B"}], c)["response"] == "B"
    assert store.variant_b(sft, [{"pair_type": "B>C_x", "chosen": "B2"}], c)["response"] == "B2"
    assert store.variant_b(sft, [], c) is None
    assert store.variant_b({"response": "A", "n_uncertain": 0}, [], c)["variant_detailed"] == "B_equals_A"


def test_rebuild_passes_budget():
    seen = []

    def fake(rec, b):
        seen.append(b)
        return {"prompt": store.DETAILED_MARK + ".", "response": f"b{b}", "image_id": rec["image_id"], "n_uncertain": 0}, None, []
    sup = {"type": "entity", "verification": {"status": "SUPPORTED"}}
    recs = [{"image_id": str(i), "propositions": [dict(sup, id=f"p{j}", subject={"entity_id": f"e{j}"}) for j in range(n)]}
            for i, n in enumerate((0, 2, 8))]
    rows, rep = store.rebuild(recs, scaled=True, build=fake)
    assert seen == [5, 12] and rep["counts"]["skipped_too_few_supported"] == 1 and len(rows) == 2
    seen.clear()
    store.rebuild(recs, scaled=False, build=fake)
    assert seen == [9, 9]


def _fair_rec(heads):
    def ent(eid, cat):
        return {"id": eid, "category_vi": cat, "number": {"value": 1},
                "gender": {"value": "khong_xac_dinh", "evidence": "not_determinable"}}
    return {"image_id": "7", "file_name": "x.jpg", "entities": [ent(f"e{i}", h) for i, h in enumerate(heads)],
            "propositions": [{"id": f"P{i}", "type": "entity", "subject": {"entity_id": f"e{i}"},
                              "predicate": {"lemma_vi": "có"}, "text_vi": f"một {h}",
                              "verification": {"status": "SUPPORTED"}} for i, h in enumerate(heads)]}


def test_rebuild_real_fair_builder_budget_reaches_selector():
    repo()
    from rescap.chair import objects_in
    rec = _fair_rec(["chó", "xe đạp", "ghế", "ô tô", "cây", "mèo", "bàn", "xe máy", "cái ô", "con ngựa", "quả bóng", "tivi"])
    build = store.fair_builder()
    n = {b: len(set(objects_in(build(rec, b)[0]["response"]))) for b in (5, 15)}
    assert n[5] < n[15], n
    rows, rep = store.rebuild([rec], scaled=True)
    assert rep["budgets"] == {"7": 15} and len(store.detailed_captions(rows)) == 1


def test_rebuild_does_not_mutate_caller():
    def mutating(rec, b):
        rec["propositions"][0]["text_vi"] = "changed"
        return None, None, []
    rec = _fair_rec(["chó"])
    before = json.dumps(rec, sort_keys=True)
    store.rebuild([rec], scaled=True, build=mutating)
    assert json.dumps(rec, sort_keys=True) == before


# ------------------------------------------------------------------ gate
def test_funnel_micro_precision_macro_recall():
    g = {"a", "b"}
    r = gate.funnel([(g, {"a", "x", "y"}), ({"c", "d", "e", "f"}, {"c", "d", "e", "f"}), (set(), {"z"})])
    assert r["n"] == 2 and abs(r["P"] - 100 * 5 / 7) < 1e-9 and abs(r["R"] - 100 * (0.5 + 1) / 2) < 1e-9


def test_funnel_matches_recall_funnel_script():
    repo()
    refs = [["Chó tím cãi nhau với mèo bạc.", "Ba chó lùn."], ["Xe máy hồng bay dọc đường mây tím.", "Người khổng lồ ôm xe máy."],
            ["Bàn đá biết hát."], ["Bầu trời kẻ sọc vuông."]]
    caps = {"0": "Chó tím ngủ cạnh ghế bay.", "1": "Xe máy hồng chở người khổng lồ.", "2": "Bàn đá hát."}
    with tempfile.TemporaryDirectory() as d:
        rd = Path(d) / "rec"
        rd.mkdir()
        recs = []
        for i, rr in enumerate(refs):
            rec = {"image_id": str(i), "reference_captions": rr, "selected_ids": [], "propositions": []}
            recs.append(rec)
            (rd / f"{i}.json").write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
        sft = Path(d) / "sft.jsonl"
        sft.write_text("".join(json.dumps({"image_id": k, "prompt": "Mô tả chi tiết bức ảnh này bằng tiếng Việt.",
                                           "response": v}, ensure_ascii=False) + "\n" for k, v in caps.items()),
                       encoding="utf-8")
        out = subprocess.run([sys.executable, "-I", "-B", str(REPO / "scripts/recall_funnel.py"), "--in", str(rd),
                              "--sft", str(sft)], capture_output=True, text=True, check=True).stdout
    line = next(x for x in out.splitlines() if x.startswith("sft_caption"))
    p, r = map(float, re.findall(r"[PR]=\s*([\d.]+)", line))
    mine = gate.store_funnel(recs, caps)
    assert (round(mine["P"], 1), round(mine["R"], 1)) == (p, r), (mine, line)


def test_choose_opstar_floor_and_tie():
    s1 = {"P": 42.0, "R": 36.0}
    pts = [{"op": 0, "P": 39.9, "R": 60.0}, {"op": 1, "P": 40.0, "R": 48.0}, {"op": 2, "P": 41.0, "R": 48.0},
           {"op": 3, "P": 45.0, "R": 40.0}]
    d = gate.choose(pts, s1)
    assert d["P_floor"] == 40.0 and d["op_star"]["op"] == 2 and d["pass"]


def test_choose_pass_boundary_and_infeasible():
    s1 = {"P": 42.0, "R": 36.0}
    assert gate.choose([{"op": 0, "P": 42.0, "R": 47.1}], s1)["pass"]
    assert not gate.choose([{"op": 0, "P": 42.0, "R": 47.09}], s1)["pass"]
    d = gate.choose([{"op": 0, "P": 30.0, "R": 90.0}], s1)
    assert not d["pass"] and d["op_star"] is None


def test_op_mid_over_all_points():
    s1 = {"P": 42.0, "R": 36.0}
    pts = [{"op": 0, "P": 41, "R": 50.0}, {"op": 1, "P": 43, "R": 42.0}, {"op": 2, "P": 44, "R": 44.5},
           {"op": 3, "P": 45, "R": 43.4}, {"op": 4, "P": 30, "R": 43.0}]
    d = gate.choose(pts, s1)
    assert d["mid_target_R"] == 43.0 and d["op_mid"]["op"] == 4  # infeasible (P 30 < 40) but nearest: E7


def test_load_table_first_occurrence():
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "probes.jsonl"
        f.write_text("".join(json.dumps(r) + "\n" for r in (
            {"image": "a.jpg", "q": "k1", "p_yes": 0.9}, {"image": "a.jpg", "q": "k1", "p_yes": 0.1},
            {"image": "b.jpg", "q": "k1", "p_yes": 0.4})), encoding="utf-8")
        t = gate.load_table(f)
    assert t == {"a.jpg": {"k1": 0.9}, "b.jpg": {"k1": 0.4}}


def _gendered(pid, eid, st):
    """A gendered entity proposition with unanimous K=5 evidence (person_uncap criteria 1-4 when UNCERTAIN)."""
    return {"id": pid, "type": "entity", "subject": {"entity_id": eid, "text_vi": "một người phụ nữ"},
            "predicate": {"lemma_vi": "có"}, "text_vi": "một người phụ nữ", "verification": {"status": st},
            "evidence": {"probes": [{"model": VIN, "question_vi": "Trong ảnh có người phụ nữ không?", "polarity": "affirms",
                                     "samples": ["Có."] * 5},
                                    {"model": VIN, "question_vi": "Trong ảnh không có người phụ nữ phải không?",
                                     "polarity": "refutes", "samples": ["Không."] * 5}],
                         "visual_grounding": {"grounding_score": 0.95}, "external_knowledge": {"inference_type": "none"}}}


def _k0_records():
    heads, gold = ["chó", "mèo", "xe máy", "bàn", "ghế", "ô tô", "con ngựa"], ["chó", "mèo", "xe máy"]
    recs, tab = [], {}
    for i in range(4):
        r = _fair_rec(heads)
        r.update(image_id=str(i), file_name=f"{i}.jpg", reference_captions=[f"Một {g} ở đây." for g in gold])
        for j, p in enumerate(r["propositions"]):
            q = f"Trong ảnh có {heads[j]} không?"
            p["evidence"] = {"probes": [{"model": VIN, "question_vi": q}]}
            p["verification"]["status"] = "SUPPORTED" if j < 2 else "UNCERTAIN"
            tab.setdefault(r["file_name"], {})[verify.qkey(q)] = 0.95 if heads[j] in gold else 0.6
        r["entities"].append({"id": "w", "category_vi": "phụ nữ", "number": {"value": 1},
                              "gender": {"value": "nu", "evidence": "visible"}})
        r["propositions"].append(_gendered("PW", "w", "UNCERTAIN"))
        tab[r["file_name"]][verify.qkey("Trong ảnh có người phụ nữ không?")] = 0.45  # UNCERTAIN at every point
        r["propositions"].append({"id": "PR", "type": "entity", "subject": {"entity_id": "e3"}, "text_vi": "một bàn",
                                  "predicate": {"lemma_vi": "có"}, "verification": {"status": "REJECTED"}})
        recs.append(r)
    return recs, tab


def test_k0_driver_end_to_end():
    recs, tab = _k0_records()
    raw = json.dumps(recs, sort_keys=True)
    res = gate.run_k0(recs, {"vintern": tab})
    assert json.dumps(recs, sort_keys=True) == raw
    assert len(res["points"]) == 15 and len(res["skipped"]) == 15 and not res["complete"] and res["decision"] is None
    d = res["preview_no_verdict"]
    lo = [p for p in res["points"] if p["op"][0] <= 0.6]
    assert all(p["P"] < d["P_floor"] for p in lo), (lo, d)  # every head supported: precision falls below the floor
    assert d["op_star"]["op"][0] >= 0.7 and d["op_star"]["R"] > res["s1"]["R"] and d["pass"], (d, res["s1"])
    # S1 = recorded statuses (chó, mèo of 3 gold) -> uncap -> B 9; the uncapped person adds no lexicon gold
    assert abs(res["s1"]["R"] - 200 / 3) < 1e-9, res["s1"]
    # E4: person_uncap runs in BOTH arms and flips the gendered UNCERTAIN in every record
    assert res["s1"]["uncap"]["uncapped"] == 4 and all(p["uncap"]["uncapped"] == 4 for p in res["points"])
    assert all(p["states"]["no_q"] == 4 and p["states"]["no_q_not_rejected"] == 0 for p in res["points"])
    assert all(len(p["sft_sha256"]) == 64 for p in res["points"] + [res["s1"]])
    assert "Trong" not in json.dumps(res, ensure_ascii=False)  # numbers only, no caption text
    bad = json.loads(raw)
    bad[0]["propositions"][-1]["verification"]["status"] = "SUPPORTED"  # no Q+ and not REJECTED
    for case, b, t in (("missing Q+ score", recs, {k: dict(v) for k, v in tab.items()}), ("no-Q+ not rejected", bad, tab)):
        if case == "missing Q+ score":
            t["0.jpg"].pop(next(iter(t["0.jpg"])))
        try:
            gate.run_k0(b, {"vintern": t})
        except SystemExit as e:
            assert "FAULT" in str(e)
        else:
            raise AssertionError(f"{case} accepted")


def test_k0_launcher_isolated_with_stores_and_exclude():
    recs, tab = _k0_records()
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "rec").mkdir()
        for r in recs:
            (d / "rec" / f"{r['image_id']}.json").write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
        (d / "rec" / "_report_shard0.json").write_text("{}", encoding="utf-8")  # generate_stage1 side file: skipped
        rows = [{"image": im, "q": q, "p_yes": v} for im, t in tab.items() for q, v in t.items()]
        (d / "probes.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows if x["image"] != "2.jpg"),
                                        encoding="utf-8")
        (d / "g1.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows if x["image"] == "2.jpg"),
                                    encoding="utf-8")
        (d / "excl.txt").write_text("3.jpg\n", encoding="utf-8")
        cmd = [sys.executable, "-I", "-B", str(HERE / "k0.py"), "--records", str(d / "rec"), "--table",
               f"vintern={d / 'probes.jsonl'}", "--table", f"vintern={d / 'g1.jsonl'}", "--exclude", str(d / "excl.txt"), "--store-dir", str(d / "stores"),
               "--out", str(d / "k0.json")]
        env = {**os.environ, "O31_SRC": os.environ.get("O31_SRC", str(HERE / "src"))}
        r = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=d)
        assert r.returncode == 0, r.stderr[-2000:]
        res = json.loads((d / "k0.json").read_text(encoding="utf-8"))
        assert res["inputs"]["n_records"] == 3 and res["inputs"]["n_excluded"] == 1
        assert res["inputs"]["tables"]["vintern"] == [hashlib.sha256((d / f).read_bytes()).hexdigest()
                                                      for f in ("probes.jsonl", "g1.jsonl")]
        assert res["decision"] is None and res["preview_no_verdict"] is not None and len(res["points"]) == 15
        for arm in [res["s1"]] + res["points"]:
            f = d / "stores" / arm["store"] / "sft.jsonl"
            assert hashlib.sha256(f.read_bytes()).hexdigest() == arm["sft_sha256"]
        assert "Trong" not in (d / "k0.json").read_text(encoding="utf-8")


def test_uncap_equals_person_uncap_script():
    recs = []
    for i, st in enumerate(("UNCERTAIN", "SUPPORTED", "REJECTED")):
        r = _fair_rec(["chó"])
        r.update(image_id=str(i), file_name=f"{i}.jpg")
        r["entities"].append({"id": "w", "category_vi": "phụ nữ", "number": {"value": 1}, "gender": {"value": "nu"}})
        r["propositions"].append(_gendered("PW", "w", st))
        recs.append(r)
    got, stats = store.uncap(recs)
    assert stats["uncapped"] == 1 and got[0]["propositions"][-1]["verification"]["status"] == SUPPORTED
    with tempfile.TemporaryDirectory() as d:
        src, dst = Path(d) / "in", Path(d) / "out"
        src.mkdir()
        for i, r in enumerate(recs):
            (src / f"{i:07d}.json").write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
        subprocess.run([sys.executable, "-I", "-B", str(REPO / "scripts/person_uncap.py"), "--in", str(src),
                        "--out", str(dst)], capture_output=True, check=True)
        want = [json.loads((dst / f"{i:07d}.json").read_text(encoding="utf-8")) for i in range(len(recs))]
    assert got == want
    try:
        store.uncap(got)
    except SystemExit as e:
        assert "gender_uncap" in str(e)
    else:
        raise AssertionError("already-uncapped input accepted")


# ------------------------------------------------------------------ metrics
def test_counts_aggregate_ratio_of_sums():
    rows = [metrics.counts({"a"}, {"a", "b", "c", "d"}), metrics.counts({"x", "y"}, {"y"})]
    a = metrics.aggregate(rows)
    assert abs(a["R"] - 40.0) < 1e-9 and a["h"] == 0.5 and abs(a["CHAIR_i"] - 100 / 3) < 1e-9 and a["CHAIR_s"] == 50.0
    assert rows[0] == {"m": 1, "tp": 1, "fp": 0, "fn": 3, "g": 4}


def test_statistics_exact():
    S = {"n": 10.0, "tp_S0": 6.0, "g_S0": 10.0, "fp_S0": 4.5, "tp_S1": 4.0, "g_S1": 10.0, "fp_S1": 1.7,
         "tp_S2": 5.5, "g_S2": 10.0, "fp_S2": 2.0, "cmp_x": 7.0, "cmp_y": 6.0, "cmp_k": 10.0,
         "pr_n": 20.0, "pr_o": 17.0, "pr_f": 12.0, "ab_n": 10.0, "ab_o": 3.0, "ab_f": 2.0}
    st = metrics.statistics_of(S)
    want = {"vi.dR21": 15.0, "vi.gap01": 20.0, "vi.rho": 0.75, "vi.D": 0.03 - 0.25 * 0.28, "H3.d": 10.0,
            "H4.dRT": 25.0, "H4.dFA": 10.0}
    assert all(abs(st[k] - v) < 1e-9 for k, v in want.items()), st
    assert np.isnan(metrics.statistics_of({**S, "g_S1": 0.0})["vi.dR21"])


def test_cmp_counts_order():
    g = {"dog", "car"}
    assert metrics.cmp_counts(["cat", "dog", "car", "dog"], ["car"], g) == (0, 1, 1)
    assert metrics.cmp_counts(["dog", "cat", "car"], ["car", "bus"], g) == (1, 1, 2)
    assert metrics.cmp_counts([], ["car"], g) == (0, 0, 0)


def test_cmp_score_k0_counted():
    r = metrics.cmp_score(np.array([1, 0, 2]), np.array([2, 0, 2]))
    assert r == {"CMP": 75.0, "n_used": 2, "n_k0": 1}


def test_index_chunks_equal_one_draw():
    full = np.random.default_rng(5).integers(0, 37, size=(23, 37))
    ch = np.concatenate(list(metrics.index_chunks(37, 23, 5, chunk=4)))
    assert (full == ch).all()


def test_p_null_inclusive_and_nan():
    rep = np.array([-2.0, -1.0, 0.0, np.nan])
    assert metrics.p_null(rep, -2.0, "le") == (1 + 1 + 1) / 5
    assert metrics.p_null(rep, 0.0, "ge") == (1 + 1 + 1) / 5


def test_holm_cummax():
    adj = metrics.holm({"H3": 0.01, "H4": 0.012, "H5a": 0.04, "H5b": 0.045})
    # raw scaled: 0.04, 0.036, 0.08, 0.045 -> step-down cumulative max: 0.04, 0.04, 0.08, 0.08
    assert all(abs(adj[k] - v) < 1e-12 for k, v in {"H3": 0.04, "H4": 0.04, "H5a": 0.08, "H5b": 0.08}.items()), adj


def _cols(n, r0, r1, r2, h0, h1, h2, rng):
    """Synthetic per-image columns: |G| = 4, tp ~ Binomial(4, r), fp ~ Poisson(h)."""
    c = {}
    for k, r, h in (("S0", r0, h0), ("S1", r1, h1), ("S2", r2, h2), ("e0", r0, h0), ("e1", r1, h1), ("e2", r2, h2)):
        c[f"g_{k}"] = np.full(n, 4.0)
        c[f"tp_{k}"] = rng.binomial(4, r, n).astype(float)
        c[f"fp_{k}"] = rng.poisson(h, n).astype(float)
    return c


def test_primary_pass_fail_not_identified():
    rng = np.random.default_rng(0)
    pt, rp = metrics.bootstrap(_cols(800, 0.6, 0.4, 0.55, 0.45, 0.17, 0.10, rng), b=400, seed=1)
    assert metrics.primary(pt, rp)["primary"] == "PASS"
    pt, rp = metrics.bootstrap(_cols(800, 0.6, 0.4, 0.55, 0.45, 0.17, 0.60, rng), b=400, seed=1)
    assert metrics.primary(pt, rp)["H2"] == "FAIL"
    pt, rp = metrics.bootstrap(_cols(800, 0.41, 0.4, 0.55, 0.45, 0.17, 0.10, rng), b=400, seed=1)
    assert metrics.primary(pt, rp)["H1"] == "NOT_IDENTIFIED"


def test_secondary_holm_and_h4_point():
    rng = np.random.default_rng(3)
    n = 600
    c = _cols(n, 0.6, 0.4, 0.55, 0.45, 0.17, 0.10, rng)
    c.update(cmp_x=rng.binomial(3, 0.85, n).astype(float), cmp_y=rng.binomial(3, 0.8, n).astype(float), cmp_k=np.full(n, 3.0),
             pr_n=np.full(n, 3.0), pr_o=rng.binomial(3, 0.85, n).astype(float), pr_f=rng.binomial(3, 0.6, n).astype(float),
             ab_n=np.full(n, 1.0), ab_o=rng.binomial(1, 0.25, n).astype(float), ab_f=rng.binomial(1, 0.28, n).astype(float))
    pt, rp = metrics.bootstrap(c, b=400, seed=2)
    s = metrics.secondary(pt, rp)
    assert all(s[k]["verdict"] == "PASS" for k in ("H3", "H4", "H5a", "H5b")), s
    c["pr_o"] = rng.binomial(3, 0.66, n).astype(float)  # dRT ~ +6 < 10: p small, point condition fails
    pt, rp = metrics.bootstrap(c, b=400, seed=2)
    s = metrics.secondary(pt, rp)
    assert s["H4"]["p_holm"] < 0.05 and s["H4"]["verdict"] == "FAIL"


def test_rehearsal_small():
    rng = np.random.default_rng(4)
    strong = _cols(500, 0.6, 0.3, 0.6, 0.45, 0.17, 0.05, rng)
    assert metrics.rehearsal(strong, b_out=20, b_in=100, n_sub=400, seed=9)["P_PASS"] == 1.0
    weak = _cols(500, 0.6, 0.4, 0.5, 0.45, 0.17, 0.17, rng)
    r = metrics.rehearsal(weak, b_out=20, b_in=100, n_sub=400, seed=9)
    assert r["P_PASS"] < 0.98 and not r["gate"] and "secondary_pass_share_not_gating" not in r


def test_rehearsal_reports_secondary_not_gating():
    rng = np.random.default_rng(6)
    n = 300
    c = _cols(n, 0.6, 0.3, 0.6, 0.45, 0.17, 0.05, rng)
    c.update(cmp_x=rng.binomial(3, 0.9, n).astype(float), cmp_y=rng.binomial(3, 0.8, n).astype(float), cmp_k=np.full(n, 3.0),
             pr_n=np.full(n, 3.0), pr_o=rng.binomial(3, 0.9, n).astype(float), pr_f=rng.binomial(3, 0.5, n).astype(float),
             ab_n=np.full(n, 1.0), ab_o=rng.binomial(1, 0.2, n).astype(float), ab_f=rng.binomial(1, 0.3, n).astype(float))
    r = metrics.rehearsal(c, b_out=4, b_in=60, n_sub=250, seed=3)
    assert set(r["secondary_pass_share_not_gating"]) == {"H3", "H4", "H5a", "H5b"} and r["P_PASS"] == 1.0


def test_seed_mean():
    assert metrics.seed_mean([np.array([1.0, 2]), np.array([3.0, 2]), np.array([2.0, 5])]).tolist() == [2.0, 3.0]


def test_registered_constants():
    assert (metrics.ALPHA, metrics.MARGIN_H2, metrics.RHO_MIN, metrics.GAP_MIN) == (0.05, 0.25, 0.50, 2.0)
    assert (metrics.B_MAIN, metrics.SEED_MAIN) == (10_000, 20261127)
    assert (metrics.B_OUT, metrics.B_IN, metrics.N_SUB, metrics.SEED_REH) == (1_000, 1_000, 4_224, 20261128)
    assert (metrics.H3_NULL, metrics.H4_POINT, metrics.H4_FA) == (-2.0, 10.0, 5.0)
    assert (gate.R_GOAL, gate.FLOOR_DROP) == (47.1, 2.0)
    assert (store.K_SCALE, store.B_MIN, store.B_MAX, store.B_FAIR) == (1.5, 5, 15, 9)
    import inspect
    sig = inspect.signature(metrics.bootstrap).parameters
    assert sig["b"].default == 10_000 and sig["seed"].default == 20261127
    sig = inspect.signature(metrics.rehearsal).parameters
    assert [sig[k].default for k in ("b_out", "b_in", "n_sub", "seed")] == [1_000, 1_000, 4_224, 20261128]


def test_ci_index_hand_computed():
    assert metrics.ci(np.arange(100.0)) == (2.0, 96.0, 0)  # int(0.025*100) = 2, int(0.975*100) - 1 = 96
    assert metrics.ci(np.r_[np.arange(40.0), [np.nan] * 3]) == (1.0, 38.0, 3)


def _pr(dr, d, gap=20.0, rho=0.75):
    point = {"vi.gap01": gap, "vi.rho": rho, "vi.D": float(np.mean(d))}
    return metrics.primary(point, {"vi.dR21": np.asarray(dr, float), "vi.D": np.asarray(d, float)})


def test_h1_h2_boundaries():
    ok_dr, ok_d = np.full(200, 1.0), np.full(200, -0.01)
    assert _pr(ok_dr, ok_d)["primary"] == "PASS"
    assert _pr(np.zeros(200), ok_d)["H1"] == "FAIL"          # CI lower bound must be > 0 (strict)
    assert _pr(ok_dr, np.zeros(200))["H2"] == "FAIL"         # CI upper bound must be < 0 (strict)
    assert _pr(ok_dr, ok_d, rho=0.50)["H1"] == "PASS"         # rho >= 0.50 (inclusive)
    assert _pr(ok_dr, ok_d, rho=0.4999)["H1"] == "FAIL"
    assert _pr(ok_dr, ok_d, gap=2.0)["H1"] == "PASS"          # gap >= 2.0 identified
    assert _pr(ok_dr, ok_d, gap=1.999)["H1"] == "NOT_IDENTIFIED"


def _sec_reps(b=1000, frac=None):
    """Replicates where each member's one-sided p is about `frac` (None: tiny)."""
    def arr(good, bad):
        x = np.full(b, good)
        if frac:
            x[: int(frac * b)] = bad
        return x
    return {"H3.d": arr(5.0, -3.0), "H4.dRT": arr(20.0, -1.0), "H4.dFA": arr(0.0, 6.0),
            "en.dR21": arr(5.0, -1.0), "en.D": arr(-0.1, 0.1)}


def test_secondary_uses_holm_adjusted_p():
    reps = _sec_reps(frac=0.03)
    point = {k: float(np.median(v)) for k, v in reps.items()}
    s = metrics.secondary(point, reps)
    assert all(s[k]["p"] < 0.05 and s[k]["p_holm"] >= 0.05 and s[k]["verdict"] == "FAIL" for k in s if k.startswith("H")), s
    s = metrics.secondary(point, _sec_reps())
    assert all(s[k]["verdict"] == "PASS" for k in ("H3", "H4", "H5a", "H5b")), s


def test_secondary_h4_is_max_of_parts_and_h3_null():
    reps = _sec_reps()
    reps["H4.dFA"] = np.full(1000, 7.0)  # FA part fails (null dFA >= 5 holds everywhere)
    point = {k: float(np.median(v)) for k, v in reps.items()}
    s = metrics.secondary(point, reps)
    assert s["H4"]["p"] == 1.0 and s["H4"]["verdict"] == "FAIL" and s["H3"]["verdict"] == "PASS"
    reps = _sec_reps()
    reps["H3.d"] = np.full(1000, -1.0)  # above the -2.0 null: PASS; a 0.0 null would FAIL it
    s = metrics.secondary({k: float(np.median(v)) for k, v in reps.items()}, reps)
    assert s["H3"]["verdict"] == "PASS"


def test_rehearsal_draws_with_replacement():
    rng = np.random.default_rng(8)
    c = _cols(300, 0.6, 0.3, 0.6, 0.45, 0.17, 0.05, rng)
    r = metrics.rehearsal(c, b_out=3, b_in=20, n_sub=300, seed=1)
    assert 0.55 < r["outer_unique_share"] < 0.72, r  # without replacement it would be exactly 1.0


def test_rehearsal_gate_threshold():
    rng = np.random.default_rng(10)
    c = _cols(400, 0.6, 0.4, 0.515, 0.45, 0.17, 0.10, rng)
    r = metrics.rehearsal(c, b_out=40, b_in=200, n_sub=400, seed=3)
    assert r["P_PASS"] == 0.975 and not r["gate"], r  # 39/40 passes is still below the 0.98 gate


# ------------------------------------------------------------------ overlap
def _feats(ids, shas, ph, dh, sscd, ph_m=None, dh_m=None):
    return {"ids": ids, "sha": shas, "phash": np.array(ph, np.uint64), "dhash": np.array(dh, np.uint64),
            "phash_m": np.array(ph_m if ph_m is not None else ph, np.uint64),
            "dhash_m": np.array(dh_m if dh_m is not None else dh, np.uint64), "sscd": np.array(sscd, np.float32)}


def _unit(*v):
    v = np.array(v, np.float32)
    return v / np.linalg.norm(v)


def test_w4_rules_and_direction():
    far, far2, mid, alt = 0xFFFFFFFFFFFFFFFF, 0xF0F0F0F0F0F0F0F0, 0x00FF00FF00FF00FF, 0xFFFF0000FFFF0000
    pool = _feats(["p0", "p1", "p2", "p3"], ["s0", "s1", "s2", "s3"], [1, 0, 0, far], [1, 0, 0, far],
                  [_unit(1, 0, 0, 0), _unit(0.8, 0.6, 0, 0), _unit(0.45, 0.893, 0, 0), _unit(0, 0, 0, 1)])
    kt = _feats(["k0"], ["s0"], [far2], [far2], [_unit(0, 0, 1, 0)])  # p0 is its byte twin
    uit = _feats(["u0"], ["su"], [0], [0], [_unit(1, 0, 0, 0)])
    # c1 matches u0 only through ITS OWN mirrored hashes (x side) and SSCD 0.6 >= 0.5
    kar = _feats(["c0", "c1"], ["sc0", "sc1"], [mid, alt], [mid, alt], [_unit(0, 0, 1, 0), _unit(0.6, 0, 0.8, 0)],
                 ph_m=[mid, 3], dh_m=[mid, 3])
    out = overlap.w4_pass({"pool": pool, "ktvic_test": kt, "uit_test": uit, "karpathy_test": kar})
    # p0 byte twin; p1 SSCD 0.8 > 0.75 vs u0; p2 hash 0 but SSCD 0.45 < 0.5: kept; p3 far: kept
    assert out["removed"]["pool"] == ["p0", "p1"], out
    assert out["removed"]["karpathy_test"] == ["c1"] and "uit_test" not in out["removed"], out
    assert "pool_vs_tier3" in out["skipped"] and "tier3_vs_uit_test" in out["skipped"]


# ------------------------------------------------------------------ train / decode / custody
def test_n_steps_floor():
    assert train.n_steps(7203) == 2 * 900 and train.n_steps(8) == 2
    try:
        train.n_steps(7)
    except ValueError:
        return
    raise AssertionError("tiny store accepted")


def _tcfg(**k):
    return {"arm": "S2", "seed": 42, "data": "d", "out": "o", "rows_s1": 7203, "steps": 1800, **k}


def test_train_check_refuses():
    train.check(_tcfg())
    for bad in (_tcfg(seed=7), _tcfg(steps=1801), _tcfg(lr=2e-4), _tcfg(lora_r=8), _tcfg(arm="S3"),
                _tcfg(base_model="Qwen/Qwen2.5-VL-3B-Instruct"), _tcfg(vision_tokens=1024)):
        try:
            train.check(bad)
        except ValueError:
            continue
        raise AssertionError(f"accepted {bad}")


def test_train_argv():
    a = train.argv(_tcfg(seed=43))
    for flag, v in (("--lr", "0.0001"), ("--grad-accum", "8"), ("--lora-r", "16"), ("--lora-alpha", "32"),
                    ("--vision-tokens", "512"), ("--seed", "43"), ("--stage", "sft")):
        assert a[a.index(flag) + 1] == v
    assert "--force-4bit" in a


def test_parity_rule():
    b1 = {s: {str(i): [1, 2, i] for i in range(50)} for s in decode.SYSTEMS}
    assert decode.parity(b1, json.loads(json.dumps(b1)))["batch"] == 8
    b8 = json.loads(json.dumps(b1))
    b8["S1"]["3"] = [1, 2, 4]
    r = decode.parity(b1, b8)
    assert r["batch"] == 1 and r["mismatches"] == {"S1": ["3"]}
    short = {s: dict(list(v.items())[:49]) for s, v in b1.items()}
    assert decode.parity(short, short)["batch"] == 1


def test_decode_check():
    decode.check({"system": "S0", "batch": 1, "lang": "vi"})
    for bad in ({"system": "S0", "batch": 8, "lang": "vi"}, {"system": "S0", "batch": 4, "lang": "vi"},
                {"system": "S0", "batch": 1, "lang": "vi", "do_sample": True}):
        try:
            decode.check(bad)
        except ValueError:
            continue
        raise AssertionError(f"accepted {bad}")


def test_no_torch_and_no_forbidden_imports():
    assert "torch" not in sys.modules and "transformers" not in sys.modules
    no_forbidden()
    src = Path(verify.__file__).parent
    for f in src.glob("*.py"):
        assert not re.search(r"\be2b_1c", f.read_text(encoding="utf-8")) or f.name == "__init__.py", f


def test_repo_sha_refuses_changed_file():
    with tempfile.TemporaryDirectory() as d:
        code = ("import sys; sys.path.insert(0, %r); import o31\n"
                "try:\n    o31.repo()\nexcept SystemExit as e:\n    print('REFUSED' if 'FAULT' in str(e) else 'OTHER')\n"
                "else:\n    print('ACCEPTED')") % str(Path(verify.__file__).parent.parent)
        env = {**os.environ, "VSPS_REPO": d}
        out = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True, env=env).stdout.strip()
    assert out == "REFUSED", out
    assert len(REUSED) >= 15


# ------------------------------------------------------------------ G1/G2 probe runner and student decoder (CC-504 follow-up)
_TINY: dict = {}


def _tiny():
    """A tiny random Qwen2.5-VL (real transformers classes, CPU, nothing downloaded) and its processor."""
    if _TINY:
        return _TINY["proc"], _TINY["net"]
    import torch
    import transformers as tf
    from tokenizers import Tokenizer, models, pre_tokenizers

    torch.manual_seed(0)
    sp = ["<|im_start|>", "<|im_end|>", "<|vision_start|>", "<|vision_end|>", "<|image_pad|>", "<|video_pad|>"]
    words = ["<unk>", "<pad>"] + sp + ["user", "assistant", "có", "không", "Có", "Không", "Trong", "ảnh", "người",
                                       "xe", "chó", "bàn", "Chỉ", "trả", "lời", "'có'", "hoặc", "'không'.", "?",
                                       "Mô", "tả", "chi", "tiết", "bức", "này", "bằng", "tiếng", "Việt."]
    words += [f"w{i}" for i in range(30)]
    tk = Tokenizer(models.WordLevel({w: i for i, w in enumerate(words)}, unk_token="<unk>"))
    tk.pre_tokenizer = pre_tokenizers.WhitespaceSplit()
    tok = tf.Qwen2TokenizerFast(tokenizer_object=tk, unk_token="<unk>", pad_token="<pad>", eos_token="<|im_end|>",
                                additional_special_tokens=sp)
    tpl = ("{% for m in messages %}<|im_start|> {{ m['role'] }} {% for c in m['content'] %}{% if c['type'] == 'image' %}"
           "<|vision_start|> <|image_pad|> <|vision_end|> {% else %}{{ c['text'] }} {% endif %}{% endfor %}<|im_end|> "
           "{% endfor %}{% if add_generation_prompt %}<|im_start|> assistant {% endif %}")
    ip = tf.Qwen2VLImageProcessor(min_pixels=4 * 28 * 28, max_pixels=8 * 28 * 28, patch_size=14, merge_size=2,
                                  temporal_patch_size=2)
    proc = tf.Qwen2_5_VLProcessor(image_processor=ip, tokenizer=tok, chat_template=tpl)
    cfg = tf.Qwen2_5_VLConfig(
        vocab_size=len(words), hidden_size=32, intermediate_size=64, num_hidden_layers=2, num_attention_heads=4,
        num_key_value_heads=2, max_position_embeddings=512, rope_scaling={"type": "mrope", "mrope_section": [1, 1, 2]},
        image_token_id=words.index("<|image_pad|>"), video_token_id=words.index("<|video_pad|>"),
        vision_start_token_id=words.index("<|vision_start|>"), vision_end_token_id=words.index("<|vision_end|>"),
        bos_token_id=2, eos_token_id=3, pad_token_id=1,
        vision_config=dict(depth=2, hidden_size=16, out_hidden_size=32, intermediate_size=32, num_heads=2, patch_size=14,
                           spatial_merge_size=2, temporal_patch_size=2, window_size=56, fullatt_block_indexes=[1]))
    net = tf.Qwen2_5_VLForConditionalGeneration(cfg).eval()
    net.generation_config.pad_token_id, net.generation_config.eos_token_id = 1, 3
    _TINY.update(proc=proc, net=net)
    return proc, net


def _imgs(n):
    from PIL import Image
    return [Image.new("RGB", (40 + 7 * (i % 9), 30 + 11 * (i % 7)), (37 * i % 255, 120, (200 - 13 * i) % 255)) for i in range(n)]


def _probe_records():
    recs = []
    for i in range(3):
        props = []
        for j, h in enumerate(("người", "xe", "chó")):
            q = f"Trong ảnh có {h} không?"
            props.append({"id": f"P{j}", "type": "entity", "verification": {"status": "UNCERTAIN"},
                          "evidence": {"probes": [{"model": VIN, "question_vi": q},
                                                  {"model": VIN, "question_vi": f"Trong ảnh không có {h} phải không?"},
                                                  {"model": "Qwen/Qwen2.5-VL-7B-Instruct", "question_vi": "khác?"}]}})
        props.append({"id": "PR", "type": "entity", "verification": {"status": "REJECTED"}})
        recs.append({"image_id": str(i), "file_name": f"{2 - i}.jpg", "propositions": props})
    return recs


def test_probe_work_modes():
    recs = _probe_records()
    v, i = probe.work(recs, "vintern"), probe.work(recs, "internvl3")
    assert [n for n, _ in v] == ["0.jpg", "1.jpg", "2.jpg"] == [n for n, _ in i]
    assert len(v[0][1]) == 6 and len(i[0][1]) == 3  # E1b: every unique Vintern question; G2: Q+ only (E3)
    assert [k for k, _q in i[0][1]] == [verify.qkey(f"Trong ảnh có {h} không?") for h in ("người", "xe", "chó")]
    assert all(q.endswith("không?") for _k, q in i[0][1])


def test_probe_instruct_equals_m0_and_pins():
    repo()
    import m0
    for q in ("Trong ảnh có chó không?", "Có xe", "x?"):
        assert probe.instruct(q) == m0.instruct(q)
    fam = probe.FAMILIES
    assert fam["vintern"]["repo"] == m0.MODEL["repo"] and fam["vintern"]["revision"] == m0.MODEL["revision"]
    reg = json.loads((REPO / probe.REGISTRY).read_text(encoding="utf-8"))["models"]
    assert reg["internvl3_8b"]["hub_id"] == fam["internvl3"]["repo"] and reg["internvl3_8b"]["revision"] == fam["internvl3"]["revision"]
    assert reg["qwen25vl_7b"]["revision"] == decode.SETTINGS["revision"] and reg["qwen25vl_7b"]["hub_id"] == decode.SETTINGS["base"]
    assert fam["vintern"]["batch"] == (1,) and fam["internvl3"]["batch"] == (1, 8)
    assert (fam["vintern"]["transformers"], fam["internvl3"]["transformers"]) == ("4.51.3", "4.57.6")
    assert (fam["vintern"]["cap_h"], fam["internvl3"]["cap_h"]) == (3.5, 30.0)  # COMPUTE_PLAN v3 G1, G2 caps
    assert (probe.PROBE_TOL, probe.PARITY_IMAGES, probe.SMOKE_N, probe.MASS_FLOOR) == (1e-3, 50, 20, 0.5)
    assert probe.PROBE_TOL == m0.EQUIV_TOL


def test_yes_no_ids_and_token_ok():
    proc, _net = _tiny()
    tok = proc.tokenizer
    yes, no = probe.yes_no_ids(tok)
    assert {tok.convert_tokens_to_ids(w) for w in ("Có", "có")} <= set(yes) and \
        {tok.convert_tokens_to_ids(w) for w in ("Không", "không")} <= set(no)
    assert probe.token_ok(tok, yes, no) and not probe.token_ok(tok, yes, yes) and not probe.token_ok(tok, no, yes)


def _direct_s(proc, net, im, q):
    import torch
    msgs = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": probe.instruct(q)}]}]
    enc = proc(text=[proc.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)], images=[im],
               return_tensors="pt")
    with torch.no_grad():
        pr = torch.softmax(net(**enc).logits[0, -1].float(), dim=-1)
    yes, no = probe.yes_no_ids(proc.tokenizer)
    a, b = pr[yes].sum().item(), pr[no].sum().item()
    return a / (a + b), a + b


def test_hf_probe_score_and_batch_parity():
    proc, net = _tiny()
    fn = probe.make_hf_probe(proc, net)
    ims = _imgs(50)
    qs = ["Trong ảnh có người không?", "Trong ảnh có chó không? w1 w2 w3"]
    s, mass, top, n_tok = fn([ims[0]], [qs[0]])[0]
    ds, dm = _direct_s(proc, net, ims[0], qs[0])
    assert abs(s - ds) < 1e-6 and abs(mass - dm) < 1e-6 and 0 < mass <= 1 and n_tok > 0
    items = [(f"{k}.png", [(verify.qkey(q), q) for q in qs]) for k in range(50)]
    load = {f"{k}.png": ims[k] for k in range(50)}.get
    r1, r2 = probe.probe_rows(fn, items, 1, load), probe.probe_rows(fn, items, 2, load)
    assert probe.batch_parity(r1, r2, 50)["ok"], probe.batch_parity(r1, r2, 50)


def test_batch_parity_rule():
    b1 = [{"image": f"{k}", "q": "a", "p_yes": 0.5, "top": "có"} for k in range(50)]
    near = [dict(r, p_yes=0.5 + 2 ** -10) for r in b1]
    assert probe.batch_parity(b1, near, 50)["ok"]                      # |d| = 0.00098 < 1e-3
    assert not probe.batch_parity(b1, [dict(r, p_yes=0.5011) for r in b1], 50)["ok"]
    assert not probe.batch_parity(b1, [dict(r, top="không") if r["image"] == "3" else r for r in b1], 50)["ok"]
    assert not probe.batch_parity(b1, b1, 49)["ok"] and not probe.batch_parity(b1, b1[:-1], 50)["ok"]


def test_probe_smoke_rule():
    rows = [{"p_yes": 0.4, "mass": 0.5} for _ in range(20)]
    assert probe.smoke(rows)["ok"] and not probe.smoke(rows[:19])["ok"]
    assert not probe.smoke([dict(r, mass=0.49) for r in rows])["ok"]
    assert not probe.smoke([dict(rows[0], p_yes=float("nan"))] + rows[1:])["ok"]


def _fake_probe(calls=None, fail_after=None, batch_bias=0.0):
    def fn(images, questions):
        out = []
        for q in questions:
            if calls is not None:
                calls.append(q)
                if fail_after is not None and len(calls) > fail_after:
                    raise KeyboardInterrupt
            h = int(hashlib.sha256(q.encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
            out.append((min(1.0, h + batch_bias * (len(questions) > 1)), 0.9, "có", 7))
        return out
    return fn


def _items(n_img, n_q=3):
    return [(f"{k:03d}.jpg", [(f"q{k}_{j}", f"Câu {k} {j}?") for j in range(n_q)]) for k in range(n_img)]


def test_run_pass_resume_shards_finalize():
    items = _items(5)
    with tempfile.TemporaryDirectory() as d:
        out = Path(d)
        calls = []
        try:
            probe.run_pass(_fake_probe(calls, fail_after=8), items, out, 1, lambda n: n, 1.0, shard_images=2)
        except KeyboardInterrupt:
            pass
        assert (out / "shard_00000.jsonl").exists() and (out / "shard_00001.jsonl.partial").exists()
        calls2 = []
        assert probe.run_pass(_fake_probe(calls2), items, out, 1, lambda n: n, 1.0, shard_images=2) == 0
        assert len(calls2) == 15 - 8  # only the pairs not yet written
        f = probe.finalize(items, out, shard_images=2)
        assert f["rows"] == 15
        tab = gate.load_table(out / "probes.jsonl")
        assert set(tab) == {n for n, _ in items} and all(len(v) == 3 for v in tab.values())
        assert (out / "probes.jsonl.sha256").read_text().split()[0] == f["sha256"]
        more = items[:4] + [(items[4][0], items[4][1] + [("extra", "Câu thêm?")])]
        try:
            probe.finalize(more, out, shard_images=2)
        except SystemExit as e:
            assert "work pairs" in str(e)
        else:
            raise AssertionError("rows that are not the work pairs accepted")
        (out / "shard_00000.jsonl").write_text("tampered\n")
        try:
            probe.finalize(items, out, shard_images=2)
        except SystemExit as e:
            assert "FAULT" in str(e)
        else:
            raise AssertionError("tampered shard accepted")


def test_run_pass_stops():
    items = _items(3)
    with tempfile.TemporaryDirectory() as d:
        out = Path(d)
        bad = lambda ims, qs: [(float("nan"), 0.0, "x", 1) for _ in qs]  # noqa: E731
        assert probe.run_pass(bad, items, out, 1, lambda n: n, 1.0) == 2 and (out / probe.STOP).exists()
        try:
            probe.run_pass(_fake_probe(), items, out, 1, lambda n: n, 1.0)
        except SystemExit as e:
            assert "REFUSED" in str(e)
        else:
            raise AssertionError("resumed after a STOP")
    with tempfile.TemporaryDirectory() as d:
        assert probe.run_pass(_fake_probe(), items, Path(d), 1, lambda n: n, 0.5, t0=time.time() - 3600) == 4


def test_probe_job_parity_decides_batch():
    items = _items(55, n_q=2)
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "a"
        assert probe.probe_job(_fake_probe(), items, out, "internvl3", lambda n: n) == 0
        assert json.loads((out / "smoke.json").read_text())["batch"] == 8
        assert {json.loads(x)["batch"] for x in (out / "probes.jsonl").read_text().splitlines()} == {8}
        out = Path(d) / "b"  # batch-dependent scores (> 1e-3): parity fails -> batch 1
        assert probe.probe_job(_fake_probe(batch_bias=0.01), items, out, "internvl3", lambda n: n) == 0
        assert json.loads((out / "smoke.json").read_text())["batch"] == 1
        out = Path(d) / "c"  # Vintern: batch 1 always (E1b)
        assert probe.probe_job(_fake_probe(), items, out, "vintern", lambda n: n) == 0
        assert json.loads((out / "smoke.json").read_text())["batch"] == 1
        out = Path(d) / "e"
        low = lambda ims, qs: [(0.5, 0.3, "x", 1) for _ in qs]  # noqa: E731
        assert probe.probe_job(low, items, out, "vintern", lambda n: n) == 2 and (out / probe.STOP).exists()


def test_probe_job_logs_no_question_text():
    import contextlib
    import io
    items = _items(10)
    buf = io.StringIO()
    with tempfile.TemporaryDirectory() as d, contextlib.redirect_stdout(buf):
        probe.probe_job(_fake_probe(), items, Path(d), "vintern", lambda n: n)
    assert "Câu" not in buf.getvalue() and "DONE" in buf.getvalue()


def test_probe_inputs_custody():
    from PIL import Image
    m0d = REPO / probe.M0_DIR
    touched = {int(x) for x in (m0d / "dev_touched_ids.txt").read_text().split()}
    kar = {int(x) for x in (m0d / "karpathy_test_val_ids.txt").read_text().split()}
    fetched = [n for n in (m0d / "fetch_images.txt").read_text().split()
               if int(n[-16:-4]) in touched and int(n[-16:-4]) not in kar]
    kar_name = next(n for n in (m0d / "fetch_images.txt").read_text().split() if int(n[-16:-4]) in kar)
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        for k, n in enumerate(fetched[:5] + [kar_name, "COCO_val2014_000000000001.jpg", "00000001335.jpg"]):
            Image.new("RGB", (8, 8), (k * 20, 0, 0)).save(d / n)  # synthetic stand-in bytes
        five = fetched[:5]
        probe.explored(five, d, refused=set())
        refused_one = {hashlib.sha256((d / five[2]).read_bytes()).hexdigest()}
        for names, ref in ((five[:4] + [kar_name], set()), (five[:4] + ["COCO_val2014_000000000001.jpg"], set()),
                           (five[:4] + ["00000001335.jpg"], set()), (five[:4], set()), (five[:4] + [five[0]], set()),
                           (five, refused_one)):
            try:
                probe.explored(names, d, refused=ref)
            except SystemExit as e:
                assert "REFUSED" in str(e)
            else:
                raise AssertionError(f"accepted {names}")
    assert len(probe.refused_shas()) >= 558 + 231
    with tempfile.TemporaryDirectory() as d:
        for sub in ("a", "b"):
            (Path(d) / sub).mkdir()
            (Path(d) / sub / "x.json").write_text(json.dumps({"file_name": "1.jpg", "propositions": []}))
        try:
            probe.records([Path(d) / "a", Path(d) / "b"], None)
        except SystemExit as e:
            assert "duplicate" in str(e)
        else:
            raise AssertionError("duplicate record accepted")
        (Path(d) / "ex.txt").write_text("1.jpg\n")
        assert probe.records([Path(d) / "a"], Path(d) / "ex.txt") == []


def test_merge_tables_two_inputs():
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "a.jsonl").write_text(json.dumps({"image": "1.jpg", "q": "k", "p_yes": 0.2}) + "\n")
        (d / "b.jsonl").write_text(json.dumps({"image": "2.jpg", "q": "k", "p_yes": 0.7}) + "\n")
        assert gate.merge_tables([d / "a.jsonl", d / "b.jsonl"]) == {"1.jpg": {"k": 0.2}, "2.jpg": {"k": 0.7}}
        (d / "c.jsonl").write_text(json.dumps({"image": "1.jpg", "q": "k", "p_yes": 0.9}) + "\n")
        try:
            gate.merge_tables([d / "a.jsonl", d / "c.jsonl"])
        except SystemExit as e:
            assert "FAULT" in str(e)
        else:
            raise AssertionError("overlapping tables accepted")


def test_decode_settings_equal_evaluate():
    import ast
    src = (REPO / "scripts/evaluate.py").read_text(encoding="utf-8")
    assert re.search(r'"--max-new-tokens", type=int, default=160\)', src) and decode.SETTINGS["max_new_tokens"] == 160
    assert re.search(r'"--max-vision-tokens", type=int, default=512\)', src) and decode.SETTINGS["max_pixels"] == 512 * 784
    assert "min_pixels=256 * P" in src and decode.SETTINGS["min_pixels"] == 256 * 784
    assert 'attn_implementation="sdpa"' in src and decode.SETTINGS["attn"] == "sdpa"
    node = next(n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "PROMPTS" for t in n.targets))
    assert ast.literal_eval(node.value)["detailed"] == decode.PROMPTS["vi"]


def test_decode_tiny_batch_parity_and_eos():
    proc, net = _tiny()
    gen = decode.make_generate(proc and net, proc, decode.PROMPTS["vi"], max_new_tokens=8) if False else \
        decode.make_generate(net, proc, decode.PROMPTS["vi"], max_new_tokens=8)
    ims = _imgs(5)
    solo = [gen([im])[0] for im in ims]
    batched = gen(ims[:3]) + gen(ims[3:])
    assert [r[0] for r in solo] == [r[0] for r in batched] and [r[2] for r in solo] == [r[2] for r in batched]
    assert decode.until_eos([5, 6, 3, 1, 1], {3, 1}) == ([5, 6, 3], False)
    assert decode.until_eos([5, 6, 7], {3}) == ([5, 6, 7], True)


def test_decode_run_resume_sha_and_custody():
    from PIL import Image
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        items = []
        for k in range(5):
            Image.new("RGB", (30, 30), (k * 40, 0, 0)).save(d / f"{k}.png")
            items.append((str(k), f"{k}.png", hashlib.sha256((d / f"{k}.png").read_bytes()).hexdigest()))
        n_calls = []

        def gen(ims):
            n_calls.append(len(ims))
            if sum(n_calls) > 4 and len(n_calls) == 3:
                raise KeyboardInterrupt
            return [([7, 3], "w1", False) for _ in ims]
        try:
            decode.run(gen, items, d, d / "o", 2)
        except KeyboardInterrupt:
            pass
        n_calls.clear()
        seen = []
        r = decode.run(lambda ims: seen.extend(ims) or [([7, 3], "w1", False) for _ in ims], items, d, d / "o", 2)
        assert len(seen) == 1  # four images were already in the partial file
        assert r["n"] == 5 and json.loads((d / "o.preds.json").read_text()) == {str(k): "w1" for k in range(5)}
        assert (d / "o.preds.json.sha256").read_text().split()[0] == r["sha256"]
        for bad, why in ((lambda: decode.run(gen, items, d, d / "o", 1), "REFUSED"),
                         (lambda: decode.run(gen, [("9", "0.png", "0" * 64)], d, d / "p", 1), "FAULT")):
            try:
                bad()
            except SystemExit as e:
                assert why in str(e), e
            else:
                raise AssertionError(why)


def test_decode_check_and_parity_record():
    decode.check({"system": "S0", "batch": 1, "lang": "vi", "adapter": None})
    decode.check({"system": "S2", "batch": 8, "lang": "vi", "adapter": "a", "parity_passed": True})
    for bad in ({"system": "S0", "batch": 1, "lang": "vi", "adapter": "a"},
                {"system": "S1", "batch": 1, "lang": "vi", "adapter": None},
                {"system": "S1", "batch": 1, "lang": "vi", "adapter": "a", "max_new_tokens": 161}):
        try:
            decode.check(bad)
        except ValueError:
            continue
        raise AssertionError(f"accepted {bad}")
    assert decode.parity_passed({"batch": 8, "mismatches": {}})
    assert not decode.parity_passed({"batch": 8, "mismatches": {"S1": ["3"]}}) and not decode.parity_passed({})


def test_decode_adapter_check_and_effect():
    import copy
    import transformers as tf
    from peft import LoraConfig, PeftModel, get_peft_model
    proc, net = _tiny()
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        net.save_pretrained(d / "base")
        pm = get_peft_model(copy.deepcopy(net), LoraConfig(r=4, lora_alpha=8, target_modules=["q_proj", "v_proj"],
                                                           init_lora_weights=False))
        pm.save_pretrained(d / "ad")
        cfg = json.loads((d / "ad/adapter_config.json").read_text())
        (d / "ad/adapter_config.json").write_text(json.dumps({**cfg, "base_model_name_or_path": decode.SETTINGS["base"]}))
        assert len(decode.check_adapter(d / "ad")) == 64
        (d / "ad/adapter_config.json").write_text(json.dumps({**cfg, "base_model_name_or_path": "Qwen/other"}))
        try:
            decode.check_adapter(d / "ad")
        except SystemExit:
            pass
        else:
            raise AssertionError("adapter of another base accepted")
        m2 = PeftModel.from_pretrained(tf.Qwen2_5_VLForConditionalGeneration.from_pretrained(d / "base").eval(),
                                       str(d / "ad")).eval()
        m2.generation_config.pad_token_id, m2.generation_config.eos_token_id = 1, 3
        im = _imgs(1)
        a = decode.make_generate(net, proc, decode.PROMPTS["vi"], 8)(im)[0][0]
        b = decode.make_generate(m2, proc, decode.PROMPTS["vi"], 8)(im)[0][0]
        assert a != b


def test_g12_launcher_parity_decide():
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        for sname in decode.SYSTEMS:
            t = {str(k): [1, 2, k] for k in range(50)}
            b8 = dict(t, **({"7": [9]} if sname == "S2" else {}))
            (d / f"{sname}.tokens.json").write_text(json.dumps({"b1": t, "b8": b8}))
        env = {**os.environ, "O31_SRC": os.environ.get("O31_SRC", str(HERE / "src"))}
        r = subprocess.run([sys.executable, "-I", "-B", str(HERE / "g12.py"), "parity-decide", "--out", str(d)],
                           capture_output=True, text=True, env=env)
        assert r.returncode == 0, r.stderr[-1500:]
        res = json.loads((d / "parity.json").read_text())
        assert res == {"batch": 1, "mismatches": {"S2": ["7"]}}
        r = subprocess.run([sys.executable, "-I", "-B", str(HERE / "g12.py"), "--help"], capture_output=True, text=True,
                           env=env)
        assert r.returncode == 0 and "smoke" in r.stdout


# ------------------------------------------------------------------ g12c (CC-519 W1-W3, N1, E3-E6)
def _raises(fn, needle):
    try:
        fn()
    except SystemExit as e:
        assert needle in str(e), (needle, str(e))
    else:
        raise AssertionError(f"no SystemExit ({needle})")


def _g12():
    import importlib.util
    spec = importlib.util.spec_from_file_location("g12_under_test", HERE / "g12.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _png(path, k):
    from PIL import Image
    Image.new("RGB", (8, 8), (k % 256, (7 * k) % 256, 3)).save(path, format="PNG")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_probe_cap_clock_survives_resume():
    """K03: a resumed job keeps launch.json t0 (ERRATUM_O31_2 E7), so an old t0 stops it at the cap."""
    with tempfile.TemporaryDirectory() as d:
        out = Path(d)
        (out / "launch.json").write_text(json.dumps({"t0": time.time() - 7200}) + "\n")
        assert probe.probe_job(_fake_probe(), _items(10), out, "vintern", lambda n: n, cap_h=1.0) == 4
        assert json.loads((out / "launch.json").read_text())["t0"] < time.time() - 7000


def test_finalize_refuses_non_finite_after_resume():
    """K09: run_pass writes the non-finite row before its halt; after a resume that pair is skipped, so finalize's
    check is the only guard."""
    items = _items(2)
    with tempfile.TemporaryDirectory() as d:
        out = Path(d)
        bad_q = items[0][1][0][1]
        nan_one = lambda ims, qs: [(float("nan") if q == bad_q else 0.5, 0.9, "có", 7) for q in qs]  # noqa: E731
        assert probe.run_pass(nan_one, items, out, 1, lambda n: n, 1.0) == 2
        (out / probe.STOP).unlink()  # a ruling-permitted resume
        assert probe.run_pass(_fake_probe(), items, out, 1, lambda n: n, 1.0) == 0
        _raises(lambda: probe.finalize(items, out), "non-finite")


def test_probe_explored_fetched_and_touched():
    """K12, K13: a smoke image must be both fetched and touched (lists of a stand-in M0 folder)."""
    m0d = REPO / probe.M0_DIR
    touched = sorted(int(x) for x in (m0d / "dev_touched_ids.txt").read_text().split())
    untouched = next(i for i in range(1, 10**6) if i not in set(touched))
    name = lambda i: f"COCO_val2014_{i:012d}.jpg"  # noqa: E731
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        md = d / "m0"
        md.mkdir()
        (md / "dev_touched_ids.txt").write_bytes((m0d / "dev_touched_ids.txt").read_bytes())
        fetched = [name(i) for i in touched[:5]] + [name(untouched)]
        (md / "fetch_images.txt").write_text("\n".join(fetched) + "\n")
        (md / "karpathy_test_val_ids.txt").write_text("")
        for k, n in enumerate(fetched + [name(touched[5])]):
            _png(d / n, k)
        probe.explored(fetched[:5], d, refused=set(), m0_dir=md)
        _raises(lambda: probe.explored(fetched[:4] + [name(untouched)], d, refused=set(), m0_dir=md), "REFUSED")
        _raises(lambda: probe.explored(fetched[:4] + [name(touched[5])], d, refused=set(), m0_dir=md), "REFUSED")
        (md / "dev_touched_ids.txt").write_text("1\n")
        _raises(lambda: probe.explored(fetched[:5], d, refused=set(), m0_dir=md), "FAULT")


def test_g12_image_loader_refuses_listed_bytes():
    """L04."""
    g = _g12()
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        h = _png(d / "a.png", 1)
        _raises(lambda: g.image_loader(d, {h})("a.png"), "refused image")
        assert g.image_loader(d, {"0" * 64})("a.png").size == (8, 8)


def test_g12_smoke_custody_and_exit_code():
    """L03: custody is checked before any model load; L05: a failed smoke exits 2 (host_selftest relies on it)."""
    import argparse
    g = _g12()
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        names = [f"x{k}.png" for k in range(5)]
        for k, n in enumerate(names):
            _png(d / n, k)
        ns = argparse.Namespace(family="vintern", snapshot=d, images=d, names=names, out=d / "o")
        _raises(lambda: g.cmd_smoke(ns), "REFUSED smoke images")
        saved = probe.explored, probe.load
        try:
            probe.explored = lambda *a, **k: None
            probe.load = lambda fam, snap: ((lambda ims, qs: [(0.5, 0.3, "x", 1) for _ in qs]), {"revision": "r"})
            assert g.cmd_smoke(ns) == 2
            probe.load = lambda fam, snap: ((lambda ims, qs: [(0.5, 0.9, "có", 1) for _ in qs]), {"revision": "r"})
            assert g.cmd_smoke(ns) == 0
        finally:
            probe.explored, probe.load = saved


def test_g12_probe_inputs_record_and_default_refused():
    """N1: the refused list defaults to exclusion.json; OUT/inputs.json holds the input shas and counts."""
    import argparse
    g = _g12()
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "r").mkdir()
        for n in ("1.jpg", "2.jpg"):
            (d / "r" / f"{n[:-4]}.json").write_text(json.dumps({"file_name": n, "propositions": []}))
        (d / "ex.txt").write_text("2.jpg\n")
        seen = {}
        saved = probe.load, probe.probe_job
        try:
            probe.load = lambda fam, snap: (None, {"revision": "rev1"})
            probe.probe_job = lambda fn, items, out, fam, loader: seen.update(items=items, loader=loader) or 0
            ns = argparse.Namespace(family="vintern", records=[d / "r"], exclude=d / "ex.txt", images=d,
                                    snapshot=d, refused_sha=None, out=d / "o")
            assert g.cmd_probe(ns) == 0
            ns.family = "internvl3"
            _raises(lambda: g.cmd_probe(ns), "REFUSED G2")
        finally:
            probe.load, probe.probe_job = saved
        rec = json.loads((d / "o/inputs.json").read_text())
        assert rec["n_records"] == 1 and rec["n_refused"] == len(probe.refused_shas()) and rec["snapshot_revision"] == "rev1"
        assert rec["file_names_sha256"] == probe.sha_lines(["1.jpg"])
        assert rec["exclude_sha256"] == hashlib.sha256(b"2.jpg\n").hexdigest()


def test_g2_one_job_after_g1():
    """ERRATUM_O31_2 E4: G2 runs once over all 3,769 records (3,700 + G1's 69) with both twins excluded."""
    from o31 import stage1
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        a, b = d / "a", d / "b"
        a.mkdir(), b.mkdir()
        for k in range(3700):
            (a / f"{k:011d}.json").write_text("{}")
        (d / "ex.txt").write_text("\n".join(stage1.TWINS) + "\n")
        _raises(lambda: probe.g2_inputs([a], d / "ex.txt"), "REFUSED G2")
        for k in range(69):
            (b / f"n{k}.json").write_text("{}")
        (d / "ex1.txt").write_text(stage1.TWINS[0] + "\n")
        _raises(lambda: probe.g2_inputs([a, b], d / "ex1.txt"), "REFUSED G2")
        probe.g2_inputs([a, b], d / "ex.txt")


def test_decode_e5_e6_prompt_and_g12_refusals():
    """E6: the English prompt is exactly the erratum string (= evaluate.py detailed_en); g12 decode refuses any other
    (L01) and parity-decode refuses 49 images (L02); manifest ids must be unique (D08)."""
    import ast
    e6 = "Describe this image in detail in English."
    assert decode.PROMPTS["en"] == e6 and hashlib.sha256(e6.encode()).hexdigest().startswith("525a4e1b")
    src = (REPO / "scripts/evaluate.py").read_text(encoding="utf-8")
    node = next(n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "PROMPTS" for t in n.targets))
    assert ast.literal_eval(node.value)["detailed_en"] == e6
    assert "four" not in (HERE / "g12.py").read_text() and "four_bit" not in (Path(decode.__file__)).read_text()
    g = _g12()
    with tempfile.TemporaryDirectory() as d:
        base = ["decode", "--system", "S0", "--snapshot", d, "--items", d, "--images", d, "--out", f"{d}/o",
                "--lang", "en", "--batch", "1"]
        _raises(lambda: g.main(base), "needs --en-prompt")
        _raises(lambda: g.main(base + ["--en-prompt", "Describe this image."]), "differs from the ERRATUM_O31_2 E6")
        tsv = Path(d) / "i.tsv"
        tsv.write_text("".join(f"{k}\t{k}.png\t{'0' * 64}\n" for k in range(49)))
        _raises(lambda: g.main(["parity-decode", "--system", "S0", "--snapshot", d, "--items", str(tsv), "--images", d,
                                "--out", f"{d}/p"]), "exactly 50")
        tsv.write_text("1\ta.png\th\n1\tb.png\th\n")
        _raises(lambda: decode.read_items(tsv), "not distinct")


# ------------------------------------------------------------------ G1 stage-1 wrapper (W2)
def test_stage1_settings_are_fair():
    """FAIR_ARGS = configs/main.env's stage-1 values (generate_stage1 run unchanged); K = 5 sampled verifier (no
    --logit-verifier), colour cross-check on; counts and pins as registered."""
    from o31 import stage1
    env = dict(re.findall(r"^(\w+)\s*\?=\s*(\S+)", (REPO / "configs/main.env").read_text(), re.M))
    a = list(stage1.FAIR_ARGS)
    flag = lambda f: a[a.index(f) + 1]  # noqa: E731
    assert (flag("--generator"), flag("--verifier"), flag("--max-entities"), flag("--max-pairs"),
            flag("--verifier-tiles")) == (env["GENERATOR"], env["VERIFIER"], env["MAX_ENTITIES"], env["MAX_PAIRS"],
                                          env["VERIFIER_TILES"]) == ("qwen2.5-vl-7b", "vintern-1b", "8", "8", "4")
    assert len(a) == 10 and "--logit-verifier" not in a and "--no-colour-cross-check" not in a
    assert (stage1.N_TRAIN, stage1.N_RECORDS, stage1.N_NEW, stage1.CAP_H) == (3769, 3700, 69, 3.5)
    assert stage1.CAP_H == probe.FAMILIES["vintern"]["cap_h"] and stage1.TRANSFORMERS == "4.51.3"
    assert stage1.TWINS == ("00000003589.jpg", "00000007511.jpg")
    assert stage1.RECORDS_TAR_SHA.startswith("b312de68") and stage1.KTVIC_TRAIN_SHA.startswith("72ee9b57")
    assert stage1.QWEN["revision"] == decode.SETTINGS["revision"] == probe.registry_entry("qwen25vl_7b")["revision"]
    import rescap.pipeline.generate, rescap.pipeline.realize, rescap.pipeline.select, rescap.pipeline.verify  # noqa: E401,F401
    import rescap.vlm.qwen_vl, rescap.vlm.registry, rescap.vlm.vintern  # noqa: E401,F401  (closure: main()'s imports)


def _train_items(n=3769):
    """Invented KTVIC-train items with mixed extensions (F3: .jpg, .png, .jpeg, .JPG)."""
    ext = (".jpg", ".png", ".jpeg", ".JPG")
    return [{"image_id": str(k), "file_name": f"t{k:06d}{ext[k % 4]}", "captions": []} for k in range(1, n + 1)]


def test_stage1_new_items():
    from o31 import stage1
    items = _train_items()
    items[0]["file_name"], items[1]["file_name"] = stage1.TWINS  # the twins hold records
    names = [i["file_name"] for i in items]
    stems = {Path(n).stem for n in names[:3700]}  # the tarball names records by stem (F3)
    new = stage1.new_items(items, stems)
    assert [i["file_name"] for i in new] == names[3700:] and len(new) == 69
    assert {Path(i["file_name"]).suffix for i in new} == {".jpg", ".png", ".jpeg", ".JPG"}
    _raises(lambda: stage1.new_items(items[:-1], stems), "FAULT")
    _raises(lambda: stage1.new_items(items, stems - {Path(stage1.TWINS[0]).stem}), "FAULT")
    _raises(lambda: stage1.new_items(items, stems | {Path(names[-1]).stem}), "FAULT")
    _raises(lambda: stage1.new_items(items, stems | {"zz"}), "FAULT")
    dup = [dict(i) for i in items]
    dup[5]["file_name"] = Path(dup[6]["file_name"]).stem + ".png" if not dup[6]["file_name"].endswith(".png") else \
        Path(dup[6]["file_name"]).stem + ".jpg"
    _raises(lambda: stage1.new_items(dup, stems), "share a stem")


def _stage(d, n_new_images=69):
    """A staged NCS_DATA folder: train_data.json (invented, 3,769 images with mixed extensions incl. the twins), the
    69 new images, and a records tarball of 3,700 empty records named by stem (twins included)."""
    import tarfile
    from o31 import stage1
    kt = d / "datasets" / "ktvic"
    (kt / "images").mkdir(parents=True)
    items = _train_items()
    items[3588]["file_name"], items[100]["file_name"] = stage1.TWINS
    imgs = [{"id": int(i["image_id"]), "filename": i["file_name"]} for i in items]
    anns = [{"image_id": int(i["image_id"]), "caption": f"zqx {i['image_id']} vwk"} for i in items]
    (kt / "train_data.json").write_text(json.dumps({"images": imgs, "annotations": anns}), encoding="utf-8")
    have = [i["file_name"] for i in items[:3700]]  # twins (items 100, 3588) included
    new = [i["file_name"] for i in items if i["file_name"] not in set(have)]
    shas = [_png(kt / "images" / n, k) for k, n in enumerate(new[:n_new_images])]
    tar = d / "records.tar.gz"
    with tarfile.open(tar, "w:gz") as tf:
        for n in have:
            p = d / f"{Path(n).stem}.json"
            p.write_text("{}")
            tf.add(p, arcname=f"stage1/{p.name}")
            p.unlink()
    return kt.parent.parent, kt / "train_data.json", tar, shas, new


def _pins(train, tar):
    from o31 import stage1
    saved = stage1.KTVIC_TRAIN_SHA, stage1.RECORDS_TAR_SHA
    stage1.KTVIC_TRAIN_SHA = hashlib.sha256(train.read_bytes()).hexdigest()
    stage1.RECORDS_TAR_SHA = hashlib.sha256(tar.read_bytes()).hexdigest()
    return saved


def test_stage1_prepare_manifest_and_custody():
    import shutil
    import generate_stage1 as gs
    from o31 import stage1
    with tempfile.TemporaryDirectory() as d:
        stage, train, tar, shas, new = _stage(Path(d))
        _raises(lambda: stage1.prepare(stage, train, tar, gs, refused=set(), screen=new), "72ee9b57")
        saved = _pins(train, tar)
        try:
            got = stage1.prepare(stage, train, tar, gs, refused=set(), screen=new[::-1])
            assert [i["file_name"] for i in got] == new and len(got) == 69
            m = json.loads((stage / "datasets/ktvic" / stage1.MANIFEST).read_text(encoding="utf-8"))["images"]
            assert m == got and m[0]["captions"] == [f"zqx {m[0]['image_id']} vwk"]  # train_data.json captions
            _raises(lambda: stage1.prepare(stage, train, tar, gs, refused=set(), screen=new[:-1] + ["x.jpg"]),
                    "val_manifest")
            other = Path(d) / "elsewhere" / train.name  # same bytes, not the staged copy (A14)
            other.parent.mkdir()
            shutil.copy(train, other)
            _raises(lambda: stage1.prepare(stage, other, tar, gs, refused=set(), screen=new), "staged copy")
            _raises(lambda: stage1.prepare(stage, train, tar, gs, refused={shas[3]}, screen=new), "missing or refused")
            (stage / "datasets/ktvic/images" / new[5]).unlink()
            _raises(lambda: stage1.prepare(stage, train, tar, gs, refused=set(), screen=new), "missing or refused")
            stage1.RECORDS_TAR_SHA = "0" * 64
            _raises(lambda: stage1.prepare(stage, train, tar, gs, refused=set(), screen=new), "b312de68")
        finally:
            stage1.KTVIC_TRAIN_SHA, stage1.RECORDS_TAR_SHA = saved
    names = stage1.screen_names()
    assert len(names) == 69 == len(set(names)) and all(n.endswith(".jpg") for n in names)


def test_stage1_run_argv_records_seed_and_cap():
    import random
    import generate_stage1 as gs
    from o31 import stage1
    ext = (".jpg", ".png", ".jpeg", ".JPG")
    new = [{"image_id": str(k), "file_name": f"n{k:03d}{ext[k % 4]}", "captions": []} for k in range(69)]
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        stage = d / "stage"
        draws = []

        def fake(write=69):
            def main():
                assert sys.argv[1:] == ["--source", stage1.MANIFEST, "--out", str(d / "o" / "records"),
                                        *stage1.FAIR_ARGS], sys.argv
                assert gs.KTVIC == stage / "datasets" / "ktvic"
                draws.append(random.random())
                rd = Path(sys.argv[4])
                rd.mkdir(parents=True, exist_ok=True)
                for i in new[:write]:
                    (rd / f"{Path(i['file_name']).stem}.json").write_text("{}")
                (rd / "_report_shard0of1.json").write_text("{}")
                return 0
            return main
        assert stage1.run(d / "o", stage, new, gs, main=fake(68)) == 5
        assert stage1.run(d / "o", stage, new, gs, main=fake()) == 0
        assert draws == [random.Random(42).random()] * 2  # F2: seeded once before main(), each run
        rec = json.loads((d / "o/g1_stage1.json").read_text())
        assert rec["records"] == 69 and rec["seed"] == 42 and rec["release_commit"] == "1f30d09"
        assert rec["names_sha256"] == probe.sha_lines(sorted(Path(i["file_name"]).stem for i in new))
        t0 = json.loads((d / "o/launch.json").read_text())["t0"]
        (d / "o2").mkdir()
        (d / "o2/launch.json").write_text(json.dumps({"t0": time.time() - 4 * 3600}) + "\n")
        assert stage1.run(d / "o2", stage, new, gs, main=fake()) == 4 and (d / "o2" / probe.STOP).exists()
        _raises(lambda: stage1.run(d / "o2", stage, new, gs, main=fake()), "REFUSED")

        def slow():
            t = time.time()
            while not gs._stop and time.time() - t < 20:
                time.sleep(0.02)
            return 0
        (d / "o3").mkdir()
        (d / "o3/launch.json").write_text(json.dumps({"t0": time.time() - 3.5 * 3600 + 1.0}) + "\n")
        assert stage1.run(d / "o3", stage, new, gs, main=slow) == 4 and (d / "o3" / probe.STOP).exists()
        assert json.loads((d / "o/launch.json").read_text())["t0"] == t0


_RELEASE_STUB = {
    "rescap/__init__.py": "",
    "rescap/pipeline/__init__.py": "",
    "rescap/pipeline/generate.py": "", "rescap/pipeline/verify.py": "", "rescap/pipeline/select.py": "",
    "rescap/pipeline/realize.py": "", "rescap/vlm/__init__.py": "", "rescap/vlm/registry.py": "",
    "rescap/vlm/vintern.py": "",
    "rescap/vlm/qwen_vl.py": "class QwenVLAdapter:\n    attn_implementation = None\n\n    def load(self):\n"
                             "        self.attn_implementation = 'sdpa'\n        return self\n",
    "scripts/generate_stage1.py": (
        "import json, sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).resolve().parents[1]))\n"
        "KTVIC = None\n_stop = False\n\n\ndef load_manifest(source):\n"
        "    return json.loads((KTVIC / source).read_text())['images']\n\n\ndef main():\n"
        "    from rescap.vlm.qwen_vl import QwenVLAdapter\n    QwenVLAdapter().load()\n"
        "    out = Path(sys.argv[sys.argv.index('--out') + 1])\n    out.mkdir(parents=True, exist_ok=True)\n"
        "    for i in load_manifest(sys.argv[sys.argv.index('--source') + 1]):\n"
        "        (out / (Path(i['file_name']).stem + '.json')).write_text('{}')\n    return 0\n"),
}


def test_stage1_release_tree_fresh_process():
    """F1 (CC-521 W5): after the HEAD imports of cmd_stage1's order, use_release loads generate_stage1 and rescap from
    the pinned release tree (a stand-in tree here, with its own pins), records the generator's attention
    implementation and the seed; a changed or extra file is refused."""
    from o31 import stage1
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        tree = d / "release"
        for rel, text in _RELEASE_STUB.items():
            (tree / rel).parent.mkdir(parents=True, exist_ok=True)
            (tree / rel).write_text(text)
        pins = {rel: hashlib.sha256((tree / rel).read_bytes()).hexdigest() for rel in _RELEASE_STUB}
        (d / "pins.json").write_text(json.dumps(pins))
        kt = d / "stage/datasets/ktvic"
        kt.mkdir(parents=True)
        new = [{"image_id": "1", "file_name": "a.png", "captions": []}, {"image_id": "2", "file_name": "b.JPG",
                                                                         "captions": []}]
        (kt / stage1.MANIFEST).write_text(json.dumps({"images": new}))
        script = d / "job.py"
        script.write_text(
            "import json, sys\nfrom pathlib import Path\nsys.path.insert(0, sys.argv[1])\n"
            "from o31 import repo, stage1\nrepo()\nimport m0, rescap.pipeline.generate, rescap.vlm.qwen_vl  # HEAD first\n"
            "d = Path(sys.argv[2])\ng = stage1.use_release(d / 'release', json.loads((d / 'pins.json').read_text()))\n"
            "import rescap.pipeline.generate as G, rescap.vlm.qwen_vl as Q\n"
            "rc = stage1.run(d / 'o', d / 'stage', json.loads(sys.argv[3]), g, cap_h=1.0)\n"
            "print(json.dumps({'rc': rc, 'files': [G.__file__, Q.__file__, g.__file__],\n"
            "                  'rec': json.loads((d / 'o/g1_stage1.json').read_text())}))\n")
        r = subprocess.run([sys.executable, "-I", "-B", str(script), str(Path(stage1.__file__).parents[1]), str(d),
                            json.dumps(new)], capture_output=True, text=True, env=os.environ)
        assert r.returncode == 0, r.stderr[-1500:]
        out = json.loads(r.stdout.strip().splitlines()[-1])
        assert out["rc"] == 0 and all(Path(f).resolve().is_relative_to(tree.resolve()) for f in out["files"]), out
        assert out["rec"]["attn_implementation"] == "sdpa" and out["rec"]["seed"] == 42 and out["rec"]["records"] == 2
        assert out["rec"]["generate_stage1_sha256"] == pins["scripts/generate_stage1.py"]
        (tree / "rescap/vlm/registry.py").write_text("# changed\n")
        _raises(lambda: stage1.use_release(tree, pins), "1 changed")
        (tree / "rescap/vlm/registry.py").write_text("")
        (tree / "rescap/extra.py").write_text("")
        _raises(lambda: stage1.use_release(tree, pins), "1 extra or missing")
    assert stage1.RELEASE["scripts/generate_stage1.py"].startswith("e9d911a1c32d4e3a") and len(stage1.RELEASE) == 26
    assert set(stage1.RELEASE_MODULES) <= {k[:-3].replace("/", ".") for k in stage1.RELEASE}


def test_launchers_fresh_process():
    """g12.py stage1 checks the environment first and s35.py pass refuses missing inputs, each in a fresh process
    (no module preloaded by the suite)."""
    env = {**os.environ, "O31_SRC": os.environ.get("O31_SRC", str(HERE / "src")), "QWEN_MAX_PIXELS": "1"}
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run([sys.executable, "-I", "-B", str(HERE / "g12.py"), "stage1", *sum(
            ([f"--{k}", d] for k in ("stage", "train", "records-tar", "release", "qwen", "vintern", "out")), [])],
            capture_output=True, text=True, env=env, cwd=d)
        assert r.returncode != 0 and "QWEN_MAX_PIXELS" in r.stderr and "Traceback" not in r.stderr, r.stderr[-800:]
        r = subprocess.run([sys.executable, "-I", "-B", str(HERE / "s35.py"), "pass", "--feats", d, "--out", f"{d}/o"],
                           capture_output=True, text=True, env=env, cwd=d)
        assert r.returncode != 0 and "REFUSED a feature file is missing" in r.stderr and "Traceback" not in r.stderr, \
            r.stderr[-800:]


def test_stage1_env_and_model_bindings():
    import argparse
    import m0
    from o31 import stage1
    saved = {k: os.environ.get(k) for k in ("QWEN_MAX_PIXELS", "HF_HUB_OFFLINE", "HF_HOME")}
    try:
        os.environ.pop("QWEN_MAX_PIXELS", None)
        os.environ["HF_HUB_OFFLINE"] = "1"
        stage1.check_env()
        os.environ["QWEN_MAX_PIXELS"] = str(512 * 784)
        _raises(stage1.check_env, "QWEN_MAX_PIXELS")
        os.environ.pop("QWEN_MAX_PIXELS")
        os.environ.pop("HF_HUB_OFFLINE")
        _raises(stage1.check_env, "HF_HUB_OFFLINE")
        os.environ["HF_HUB_OFFLINE"] = "1"
        pin, stage1.TRANSFORMERS = stage1.TRANSFORMERS, "9.9.9"
        try:
            _raises(stage1.check_env, "needs transformers 9.9.9")
        finally:
            stage1.TRANSFORMERS = pin
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            os.environ["HF_HOME"] = str(d / "hf")
            snap = d / "hf/hub/models--Qwen--Qwen2.5-VL-7B-Instruct/snapshots" / stage1.QWEN["revision"]
            snap.mkdir(parents=True)
            _raises(lambda: stage1.check_qwen(snap), "HF cache")  # no refs/main
            (snap.parent.parent / "refs").mkdir()
            (snap.parent.parent / "refs/main").write_text("0" * 40)
            _raises(lambda: stage1.check_qwen(snap), "HF cache")  # refs/main is not the pin (A16)
            (snap.parent.parent / "refs/main").write_text(stage1.QWEN["revision"])
            _raises(lambda: stage1.check_qwen(snap), "pinned file")
            away = d / "copy/hub/models--Qwen--Qwen2.5-VL-7B-Instruct/snapshots" / stage1.QWEN["revision"]
            away.mkdir(parents=True)
            _raises(lambda: stage1.check_qwen(away), "not the HF_HOME cache")  # W7: checked != loaded
            vin = d / "hf/hub/models--5CD-AI--Vintern-1B-v3_5/snapshots" / stage1.VINTERN["revision"]
            vin.mkdir(parents=True)
            stage1.check_vintern(vin)
            _raises(lambda: stage1.check_vintern(d / "copy" / vin.name), "not the HF_HOME cache")
            g = _g12()
            ns = argparse.Namespace(stage=d, train=d, records_tar=d, release=d / "rel", qwen=snap, vintern=d / vin.name,
                                    out=d / "o")
            keep = stage1.check_env, stage1.check_qwen, m0.check_model
            try:
                stage1.check_env = stage1.check_qwen = lambda *a: None

                def sentinel(_snap):
                    raise SystemExit("SENTINEL m0.check_model")
                m0.check_model = sentinel
                _raises(lambda: g.cmd_stage1(ns), "not the HF_HOME cache")  # g12 binds Vintern before its pins
                ns.vintern = vin
                _raises(lambda: g.cmd_stage1(ns), "SENTINEL")  # C02: the Vintern pins are checked
                m0.check_model = lambda *a: None
                seen = []

                def rel(tree):
                    seen.append(tree)
                    raise SystemExit("SENTINEL use_release")
                keep_rel, stage1.use_release = stage1.use_release, rel
                try:
                    _raises(lambda: g.cmd_stage1(ns), "SENTINEL use_release")  # F1 (CC-521r2): g12 loads the 1f30d09 tree
                finally:
                    stage1.use_release = keep_rel
                assert seen == [ns.release]
            finally:
                stage1.check_env, stage1.check_qwen, m0.check_model = keep
    finally:
        for k, v in saved.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)


# ------------------------------------------------------------------ §3.5 launcher (W3)
def _s35():
    import importlib.util
    spec = importlib.util.spec_from_file_location("s35_under_test", HERE / "s35.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_s35_sets_and_pins():
    from o31 import stage1
    assert overlap.EXPECT_N == {"pool": 3767, "ktvic_test": 558, "uit_test": 231, "karpathy_test": 5000, "tier3": 4224}
    for k in ("ktvic_test", "uit_test", "karpathy_test"):
        rows = overlap.set_rows(k)
        assert len(rows) == overlap.EXPECT_N[k] and all((r[2] is None) == (k == "karpathy_test") for r in rows)
    assert overlap.set_rows("karpathy_test")[0][1].startswith("COCO_val2014_")
    saved = dict(overlap.LISTS)
    try:
        overlap.LISTS["uit_test"] = (saved["uit_test"][0], "0" * 64, 2)
        _raises(lambda: overlap.set_rows("uit_test"), "differs from its pin")
    finally:
        overlap.LISTS.update(saved)
    items = _train_items()
    items[0]["file_name"], items[1]["file_name"] = stage1.TWINS
    pool = overlap.set_rows("pool", items)
    assert len(pool) == 3767 and not set(stage1.TWINS) & {r[0] for r in pool} and pool == sorted(pool)
    _raises(lambda: overlap.set_rows("pool", _train_items()), "FAULT")
    assert overlap.KV_FEATS_SHA.startswith("9783f7a6")
    import w25
    assert w25.CEN_FEATS["coco_kval"] == overlap.KV_FEATS_SHA


def test_s35_feats_checks():
    import w25
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        sscd = d / "sscd.pt"
        sscd.write_bytes(b"stand-in weights")
        shas = [_png(d / f"{k}.png", k) for k in range(3)]

        def feat(paths, sscd_path, workers=4, unreadable=()):
            n = len(paths)
            return {"sha": [hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in paths],
                    **{k: np.arange(n, dtype=np.uint64) for k in ("phash", "dhash", "phash_m", "dhash_m")},
                    "sscd": np.eye(n, 512, dtype=np.float32), "unreadable": list(unreadable)}
        rows = [(str(k), f"{k}.png", shas[k] if k else None) for k in range(3)]
        _raises(lambda: overlap.feats("x", rows, d, sscd, d / "a.npz", features=feat), "9f26bd4c")
        saved = w25.SSCD_SHA
        w25.SSCD_SHA = hashlib.sha256(sscd.read_bytes()).hexdigest()
        try:
            assert overlap.feats("x", rows, d, sscd, d / "a.npz", features=feat) == {"set": "x", "n": 3}
            f = w25.load(d / "a.npz")
            assert f["ids"] == ["0", "1", "2"] and f["sha"] == shas and not f["unreadable"]
            _raises(lambda: overlap.feats("x", rows, d, sscd, d / "a.npz", features=feat), "REFUSED")
            bad = [rows[0], (rows[1][0], rows[1][1], "0" * 64), rows[2]]
            _raises(lambda: overlap.feats("x", bad, d, sscd, d / "b.npz", features=feat), "differs from the sha")
            un = lambda *a, **k: feat(*a, unreadable=(1,), **k)  # noqa: E731
            _raises(lambda: overlap.feats("x", rows, d, sscd, d / "c.npz", features=un), "cannot be hashed")
        finally:
            w25.SSCD_SHA = saved
        s = _s35()
        (d / "t.json").write_text("{}")
        _raises(lambda: s.main(["feats", "--set", "pool", "--images", str(d), "--sscd", str(sscd), "--train",
                                str(d / "t.json"), "--out", str(d / "p.npz")]), "72ee9b57")


def _save_feats(path, f):
    repo()
    import w25
    w25.save(path, f["ids"], {**f, "unreadable": []}, set=path.stem)


def test_s35_kv_rows():
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        n = 4230
        f = _feats(list(range(n)), [f"s{k}" for k in range(n)], range(n), range(n), np.eye(n, 4, dtype=np.float32))
        _save_feats(d / "kval.npz", f)
        _raises(lambda: overlap.kv_feats(d / "kval.npz", d / "kv.npz", kv_ids=lambda: set(range(4224))), "9783f7a6")
        saved = overlap.KV_FEATS_SHA
        overlap.KV_FEATS_SHA = hashlib.sha256((d / "kval.npz").read_bytes()).hexdigest()
        try:
            want = set(range(3, 4227))
            assert overlap.kv_feats(d / "kval.npz", d / "kv.npz", kv_ids=lambda: want)["n"] == 4224
            import w25
            got = w25.load(d / "kv.npz")
            assert set(got["ids"]) == {str(i) for i in want} and got["sha"][0] == "s3" and int(got["phash"][0]) == 3
            _raises(lambda: overlap.kv_feats(d / "kval.npz", d / "kv2.npz", kv_ids=lambda: set(range(4226, 4230 + 4220))),
                    "FAULT KV-4,224")
            _raises(lambda: overlap.kv_feats(d / "kval.npz", d / "kv3.npz", kv_ids=lambda: set(range(4000))),
                    "FAULT KV-4,224")
        finally:
            overlap.KV_FEATS_SHA = saved


def test_s35_pass_exclude_file():
    from o31 import stage1
    far = 0xFFFFFFFFFFFFFFFF
    sets = {"pool": _feats(["a.jpg", "b.jpg", "c.jpg"], ["s0", "s1", "s2"], [1, 2, 3], [1, 2, 3],
                           [_unit(1, 0, 0, 0), _unit(0, 1, 0, 0), _unit(0, 0, 1, 0)]),
            "ktvic_test": _feats(["k0"], ["s1"], [far], [far], [_unit(0, 0, 0, 1)]),  # b.jpg: byte twin
            "uit_test": _feats(["u0"], ["su"], [0x0F0F0F0F0F0F0F0F], [0x0F0F0F0F0F0F0F0F], [_unit(0, 1, 1, 0)]),
            "karpathy_test": _feats(["c0"], ["sc"], [far], [far], [_unit(0, 0, 0, 1)]),
            "tier3": _feats(["9"], ["s2"], [far], [far], [_unit(0, 0, 0, 1)])}  # c.jpg: byte twin of a KV image
    expect = {k: len(v["ids"]) for k, v in sets.items()}
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        for k, f in sets.items():
            _save_feats(d / f"{k}.npz", f)
        files = {k: d / f"{k}.npz" for k in sets}
        rec = overlap.run_pass(files, d / "out", expect=expect)
        assert rec["removed"]["pool"] == ["b.jpg", "c.jpg"] and rec["removed"]["tier3"] == []
        assert (d / "out/exclude_p1.txt").read_text().split() == sorted(["b.jpg", "c.jpg", *stage1.TWINS])
        assert rec["n_exclude_p1"] == 4 and set(rec["inputs_sha256"]) == set(sets)
        _raises(lambda: overlap.run_pass({k: v for k, v in files.items() if k != "tier3"}, d / "o2", expect=expect),
                "REFUSED")
        _raises(lambda: overlap.run_pass(files, d / "o3", expect={**expect, "pool": 4}), "FAULT pool")
        _raises(lambda: overlap.run_pass(files, d / "o4"), "FAULT")  # the registered counts
        dup = dict(sets["karpathy_test"], ids=["c0", "c0"], sha=["sc", "sd"])
        dup = {k: (np.concatenate([v, v]) if isinstance(v, np.ndarray) else v) for k, v in dup.items()}
        _save_feats(d / "dup.npz", dup)
        _raises(lambda: overlap.run_pass({**files, "karpathy_test": d / "dup.npz"}, d / "o5",
                                         expect={**expect, "karpathy_test": 2}), "distinct")  # N3 (B09)



# ------------------------------------------------------------------ PKG1 (ERRATUM_O31_4, ERRATUM_O31_5): C06, C23, C24, C22, C13
_GRID_FAMS = {"V": ["vintern"], "V+I": ["vintern", "internvl3"]}


def _k0f(R, P=None, sh=None, s1=(36.6, 42.6, "S1"), complete=True):
    """A P1-form k0.json (30 points in E7 order, real op form) with the decision of the committed gate.choose."""
    pts = [{"op": [a, r, list(f)], "R": R[i], "P": P[i] if P else 41.0, "sft_sha256": sh[i] if sh else f"h{i}",
            "store": f"p{i:02d}"} for i, (a, r, f) in enumerate(verify.grid())]
    s = {"R": s1[0], "P": s1[1], "sft_sha256": s1[2], "store": "S1"}
    c = gate.choose(pts, s)
    k = {"s1": s, "points": pts, "complete": complete, "decision": c if complete else None,
         "preview_no_verdict": None if complete else c}
    return json.loads(json.dumps(k))  # as json.loads returns it (E4-1)


def _base_R():
    return [44 - 10 * (a - .5) + r if f == ("vintern",) else 50 - 10 * (a - .5) + r for a, r, f in verify.grid()]


def _ruling1_cases():
    """The fixtures of CC-525r2a ruling 1 (parta_adv.py), in the real k0.json form; expected results from the text."""
    C = {}
    C["distinct stores"] = (_k0f(_base_R()), "IDENTIFIED")
    C["OP* = OP_mid"] = (_k0f([30.0] * 15 + [48.0] * 15), "NOT_IDENTIFIED")
    C["all 30 one store"] = (_k0f([48.0] * 30, sh=["X"] * 30), "NOT_IDENTIFIED")
    C["three grid stores"] = (_k0f([37.5] * 10 + [42.3] * 10 + [48.0] * 10, sh=["A"] * 10 + ["B"] * 10 + ["C"] * 10),
                              "NOT_IDENTIFIED")
    C["label order != R order"] = (_k0f([38.0] * 8 + [40.0] * 7 + [44.0] * 8 + [48.0] * 7,
                                        sh=["A"] * 8 + ["B"] * 7 + ["C"] * 8 + ["D"] * 7), "IDENTIFIED")
    R = [30.0] * 30
    R[29], R[5], R[12], R[20] = 48.0, 44.0, 41.0, 46.5
    C["OP_25 beyond OP_mid"] = (_k0f(R), "IDENTIFIED")
    R = [36.0] * 30
    R[3], R[20], R[29], R[10], R[25] = 39.0, 39.9, 48.0, 42.3, 45.15
    P = [41.0] * 30
    P[3], P[20] = 40.0, 41.5
    C["decimal tie, P differs"] = (_k0f(R, P), "IDENTIFIED")
    C["decimal tie, P equal"] = (_k0f(R), "IDENTIFIED")
    C["b == a"] = (_k0f([47.5] + [30.0] * 29, s1=(47.5, 42.6, "S1")), "NOT_IDENTIFIED")
    R = [47.2] + [60.0] * 14 + [30.0] * 15
    P = [41.0] + [10.0] * 14 + [41.0] * 15
    C["b < a"] = (_k0f(R, P, s1=(55.0, 42.6, "S1")), "NOT_IDENTIFIED")
    C["K0 FAIL (no feasible)"] = (_k0f(_base_R(), P=[30.0] * 30), "NOT RUN")
    C["K0 FAIL (R < 47.1)"] = (_k0f([x - 10 for x in _base_R()], P=[38.0 if i % 2 else 41.0 for i in range(30)]), "NOT RUN")
    R, P, sh = [30.0] * 30, [41.0] * 30, [f"h{i}" for i in range(30)]
    R[4], P[4], sh[4] = 36.6, 42.6, "S1"
    R[29], P[29] = 48.0, 40.8
    R[25] = R[26] = 55.0
    P[25] = P[26] = 30.0
    C["OP_mid byte twin of S1"] = (_k0f(R, P, sh), "NOT_IDENTIFIED")
    return C


def _dyadic(Pa, Pb, ia, ib, same_r=None):
    R = [30.0] * 30
    R[29], R[14], R[27] = 48.5, 42.5, 45.5
    if same_r:
        R[same_r[0]] = R[same_r[1]] = 39.5
    else:
        R[ia], R[ib] = 39.25, 39.75
    P = [41.0] * 30
    if not same_r:
        P[ia], P[ib] = Pa, Pb
    return _k0f(R, P, s1=(36.5, 42.6, "S1"))


def test_points_ruling1_fixtures():
    for name, (k, want) in _ruling1_cases().items():
        got = points.extra_points(k)
        assert got["result"] == want, (name, got["result"], got["reason"])
    by_r = points.extra_points(_ruling1_cases()["label order != R order"][0])
    assert by_r["order_by_R"] != by_r["order_by_label"] and by_r["order_by_R"][0] == "OP_strict"
    beyond = points.extra_points(_ruling1_cases()["OP_25 beyond OP_mid"][0])
    assert beyond["order_by_R"].index("OP_25") > beyond["order_by_R"].index("OP_mid"), beyond["order_by_R"]
    same = points.extra_points(_ruling1_cases()["OP* = OP_mid"][0])
    assert 0.0 in same["gaps"] and same["reason"].startswith("adjacent")
    one = points.extra_points(_ruling1_cases()["all 30 one store"][0])
    assert "step 4" in one["reason"] and one["op_25"] is None
    three = points.extra_points(_ruling1_cases()["three grid stores"][0])
    assert "step 5" in three["reason"] and three["op_25"] is not None


def test_points_ieee_double_tie_and_tie_levels():
    eq = points.extra_points(_ruling1_cases()["decimal tie, P equal"][0])
    assert eq["op_25"]["grid_index"] == 20 and eq["t25"] == 36.6 + 0.25 * (48.0 - 36.6)  # doubles: 39.9 is nearer
    pd = points.extra_points(_ruling1_cases()["decimal tie, P differs"][0])
    assert pd["op_25"]["grid_index"] == 20
    assert points.extra_points(_dyadic(40.9, 41.3, 3, 20))["op_25"]["grid_index"] == 20  # level 1: higher P
    assert points.extra_points(_dyadic(41.3, 40.9, 3, 20))["op_25"]["grid_index"] == 3
    assert points.extra_points(_dyadic(41.0, 41.0, 20, 3))["op_25"]["grid_index"] == 3  # level 2: earlier grid point
    assert points.extra_points(_dyadic(0, 0, 0, 0, same_r=(7, 22)))["op_25"]["grid_index"] == 7


def test_points_floor_not_applied_and_shas_excluded():
    R = [30.0] * 30
    R[29], R[14], R[27], R[3] = 48.5, 42.5, 45.5, 39.5
    P = [41.0] * 30
    P[3] = 20.0  # far below P_floor; still eligible (E4-2 step 3)
    k = _k0f(R, P, s1=(36.5, 42.6, "S1"))
    got = points.extra_points(k)
    assert got["op_25"]["grid_index"] == 3 and got["result"] == "IDENTIFIED"
    sh = [f"h{i}" for i in range(30)]
    sh[2] = k["decision"]["op_mid"]["sft_sha256"]  # a byte twin of OP_mid lies on t25: never eligible
    R2 = list(R)
    R2[2], R2[3] = 39.5, 39.0
    P2 = list(P)
    P2[3] = 41.0
    got = points.extra_points(_k0f(R2, P2, sh, s1=(36.5, 42.6, "S1")))
    assert got["op_25"]["grid_index"] == 3, got["op_25"]


def test_points_equal_r_in_label_order():
    """OP_mid (grid index 5) and OP_25 (grid index 9) share R 42.5: the R order keeps the label order (E4-3)."""
    R = [30.0] * 30
    R[29], R[27], R[5], R[9] = 48.5, 45.5, 42.5, 42.5
    got = points.extra_points(_k0f(R, s1=(36.5, 42.6, "S1")))
    assert got["five"]["OP_mid"]["grid_index"] == 5 and got["five"]["OP_25"]["grid_index"] == 9
    assert got["order_by_R"] == ["OP_strict", "OP_25", "OP_mid", "OP_75", "OP*"] and got["result"] == "NOT_IDENTIFIED"
    assert [e["label"] for e in got["five_in_R_order"]] == got["order_by_R"]
    assert [e["label"] for e in got["five_in_label_order"]] == list(points.LABELS)
    lab = points.extra_points(_ruling1_cases()["label order != R order"][0])
    assert [e["R"] for e in lab["five_in_R_order"]] == sorted(e["R"] for e in lab["five_in_label_order"])


def test_points_refuses_preview_and_bad_order():
    k = _k0f(_base_R(), complete=False)
    _raises(lambda: points.extra_points(k), "REFUSED not P1")
    k = _k0f(_base_R())
    k["decision"] = None
    _raises(lambda: points.extra_points(k), "REFUSED not P1")
    k = _k0f(_base_R())
    k["points"] = k["points"][::-1]
    _raises(lambda: points.extra_points(k), "E7 order")


def test_points_edge_row():
    k = _k0f(_base_R())
    e = points.edge_row(k)
    assert k["decision"]["op_star"]["op"] == [0.5, 0.3, ["vintern", "internvl3"]] and e["edge"] is True
    for a_, r_, want in ((0.7, 0.2, False), (0.9, 0.2, True), (0.5, 0.2, True), (0.7, 0.1, True), (0.7, 0.3, True),
                         (0.6, 0.2, False)):
        R = [30.0] * 30
        R[[i for i, (a, r, f) in enumerate(verify.grid()) if (a, r, f) == (a_, r_, ("vintern", "internvl3"))][0]] = 48.0
        assert points.edge_row(_k0f(R))["edge"] is want, (a_, r_)
    assert points.edge_row(_k0f(_base_R(), P=[30.0] * 30))["edge"] is None


def _ops5_dir(d, k0, name="k0.json"):
    p = Path(d) / name
    p.write_text(json.dumps(k0))
    return p


def _run_ops5(*args):
    env = {**os.environ, "O31_SRC": os.environ.get("O31_SRC", str(HERE / "src"))}
    return subprocess.run([sys.executable, "-I", "-B", str(HERE / "ops5.py"), *map(str, args)], capture_output=True,
                          text=True, env=env)


def test_ops5_writer_once_from_one_p1_file():
    with tempfile.TemporaryDirectory() as d:
        k0 = _k0f(_base_R())
        kp = _ops5_dir(d, k0)
        r = _run_ops5("--k0", kp, "--out", f"{d}/o")
        assert r.returncode == 0, r.stderr[-800:]
        body = json.loads(Path(f"{d}/o/ops5.json").read_text())
        assert {k: body[k] for k in points.extra_points(k0)} == json.loads(json.dumps(points.extra_points(k0)))
        assert body["k0_sha256"] == hashlib.sha256(kp.read_bytes()).hexdigest() and body["result"] == "IDENTIFIED"
        sha = hashlib.sha256(Path(f"{d}/o/ops5.json").read_bytes()).hexdigest()
        assert Path(f"{d}/o/ops5.json.sha256").read_text().split()[0] == sha and sha in r.stdout
        assert body["edge_row_E4_5"]["edge"] is True
        before = Path(f"{d}/o/ops5.json").read_bytes()
        r = _run_ops5("--k0", kp, "--out", f"{d}/o")
        assert r.returncode != 0 and Path(f"{d}/o/ops5.json").read_bytes() == before  # written once
        r = _run_ops5("--k0", kp, "--k0", _ops5_dir(d, k0, "k0b.json"), "--out", f"{d}/two")
        assert r.returncode != 0 and "one k0.json" in r.stderr and not Path(f"{d}/two/ops5.json").exists()
        r = _run_ops5("--k0", _ops5_dir(d, _k0f(_base_R(), complete=False), "prev.json"), "--out", f"{d}/prev")
        assert r.returncode != 0 and "REFUSED not P1" in r.stderr and not Path(f"{d}/prev/ops5.json").exists()
        bad = _k0f(_base_R())
        bad["points"] = bad["points"][:29]
        r = _run_ops5("--k0", _ops5_dir(d, bad, "bad.json"), "--out", f"{d}/bad")
        assert r.returncode != 0 and not Path(f"{d}/bad/ops5.json").exists()  # nothing written before C06 returns


def _all18():
    """The 18 fixture cases of CC-525r2a ruling 1 with their results under the committed text (a preview is refused)."""
    c = dict(_ruling1_cases())
    c["dyadic level 1 (a)"] = (_dyadic(40.9, 41.3, 3, 20), "IDENTIFIED")
    c["dyadic level 1 (b)"] = (_dyadic(41.3, 40.9, 3, 20), "IDENTIFIED")
    c["dyadic level 2"] = (_dyadic(41.0, 41.0, 20, 3), "IDENTIFIED")
    c["identical R, distinct shas"] = (_dyadic(0, 0, 0, 0, same_r=(7, 22)), "IDENTIFIED")
    c["P1 file incomplete"] = (_k0f(_base_R(), complete=False), "REFUSED")
    return c


def test_ops5_equals_c06_on_the_18_fixtures():
    import importlib.util
    spec = importlib.util.spec_from_file_location("ops5_under_test", HERE / "ops5.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    cases = _all18()
    assert len(cases) == 18
    with tempfile.TemporaryDirectory() as d:
        for n, (name, (k0, want)) in enumerate(cases.items()):
            kp, out = _ops5_dir(d, k0, f"k{n}.json"), Path(d) / f"o{n}"
            if want == "REFUSED":
                _raises(lambda: m.main(["--k0", str(kp), "--out", str(out)]), "REFUSED not P1")
                assert not (out / "ops5.json").exists()
                continue
            with contextlib.redirect_stdout(io.StringIO()):
                assert m.main(["--k0", str(kp), "--out", str(out)]) == 0
            body = json.loads((out / "ops5.json").read_text())
            ref = json.loads(json.dumps(points.extra_points(k0)))
            assert body["result"] == want and {k: body[k] for k in ref} == ref, name
            assert (out / "ops5.json.sha256").read_text().split()[0] == hashlib.sha256((out / "ops5.json").read_bytes()).hexdigest()


def _ops5_file(d, k0=None):
    k0 = k0 or _k0f(_base_R())
    _run_ops5("--k0", _ops5_dir(d, k0), "--out", d)
    return Path(d) / "ops5.json"


def test_require_identified_guard():
    with tempfile.TemporaryDirectory() as d:
        o = _ops5_file(d)
        rec = json.loads(o.read_text())
        st = Path(d) / "sft.jsonl"
        st.write_text("invented store row\n")
        _raises(lambda: points.require_identified(o, "OP_25", st), "not the OP_25 store")
        rec_sha = hashlib.sha256(st.read_bytes()).hexdigest()
        rec["five"]["OP_25"]["sft_sha256"] = rec_sha
        o2 = Path(d) / "o2"
        o2.mkdir()
        (o2 / "ops5.json").write_text(json.dumps(rec))
        _raises(lambda: points.require_identified(o2 / "ops5.json", "OP_25", st), "sha256")  # no sha line
        (o2 / "ops5.json.sha256").write_text(hashlib.sha256((o2 / "ops5.json").read_bytes()).hexdigest() + "  ops5.json\n")
        assert points.require_identified(o2 / "ops5.json", "OP_25", st)["sft_sha256"] == rec_sha
        _raises(lambda: points.require_identified(o2 / "ops5.json", "OP_mid", st), "not an E-B3 extra point")
        rec["result"] = "NOT_IDENTIFIED"
        (o2 / "ops5.json").write_text(json.dumps(rec))
        (o2 / "ops5.json.sha256").write_text(hashlib.sha256((o2 / "ops5.json").read_bytes()).hexdigest() + "  ops5.json\n")
        _raises(lambda: points.require_identified(o2 / "ops5.json", "OP_25", st), "not IDENTIFIED")


def _t4_ops5(order):
    return {"schema": points.SCHEMA, "result": "IDENTIFIED", "order_by_R": order,
            "order_by_label": list(points.LABELS)}


def _t4_cols(n=40, seed=3):
    rng = np.random.default_rng(seed)
    g = rng.integers(1, 5, n).astype(float)
    tp = {}
    for j, s in enumerate(("S1", "OP_25", "A-1", "OP_75", "S2")):
        tp[s] = np.minimum(g, rng.binomial(g.astype(int), 0.3 + 0.1 * j)).astype(float)
    return {"g": g, "tp": tp}


def test_t4_statistic_by_hand():
    cols = _t4_cols()
    order = ["OP_strict", "OP_25", "OP_mid", "OP_75", "OP*"]
    res = t4.t4(_t4_ops5(order), lambda: cols, [40.0, 41.0, 43.0], [50.0, 52.0, 51.0], vk_ddof=1, b=300, seed=7)
    g = cols["g"]
    stu = [t4.STUDENT[x] for x in order]
    reps = [[] for _ in range(4)]
    for idx in metrics.index_chunks(len(g), 300, 7):
        r = [100 * cols["tp"][s][idx].sum(1) / g[idx].sum(1) for s in stu]
        for k in range(4):
            reps[k].append(r[k + 1] - r[k])
    v = [float(np.var(np.concatenate(x), ddof=1)) for x in reps]
    s2 = (np.var([40.0, 41.0, 43.0], ddof=1) + np.var([50.0, 52.0, 51.0], ddof=1)) / 2
    pr = [100 * cols["tp"][s].sum() / g.sum() for s in stu]
    z = [(pr[k + 1] - pr[k]) / math.sqrt(v[k] + 2 * s2) for k in range(4)]
    assert res["label"] == "COMPUTED" and abs(res["sigma2_seed"] - s2) < 1e-12
    assert t4.STUDENT == {"OP_strict": "S1", "OP_25": "OP_25", "OP_mid": "A-1", "OP_75": "OP_75", "OP*": "S2"}  # E-B3
    assert all(abs(a - b) < 1e-9 for a, b in zip(res["V"], v)) and all(abs(a - b) < 1e-9 for a, b in zip(res["z"], z))
    assert abs(res["p"] - max(1 - 0.5 * (1 + math.erf(x / math.sqrt(2))) for x in z)) < 1e-12
    assert abs(t4.sigma2_seed([1.0, 2.0, 3.0], [2.0, 4.0, 6.0]) - 2.5) < 1e-12
    assert abs(t4.phi(0.0) - 0.5) < 1e-15 and abs(t4.phi(1.96) - 0.9750021048517795) < 1e-12


def test_t4_order_from_ops5_and_refusals():
    cols = _t4_cols()
    order = ["OP_25", "OP_strict", "OP_mid", "OP*", "OP_75"]  # R order differs from the label order
    res = t4.t4(_t4_ops5(order), lambda: cols, [40.0, 41.0, 43.0], [50.0, 52.0, 51.0], vk_ddof=1, b=50, seed=1)
    g = cols["g"]
    pr = [100 * cols["tp"][t4.STUDENT[x]].sum() / g.sum() for x in order]
    assert res["Delta"] == [pr[k + 1] - pr[k] for k in range(4)] and res["order_by_R"] == order

    def boom():
        raise AssertionError("decodes read although ops5.json is not IDENTIFIED")
    for lab in ("NOT_IDENTIFIED", "NOT RUN"):
        r = t4.t4({"schema": points.SCHEMA, "result": lab}, boom, [], [], vk_ddof=None)
        assert r["label"] == lab and r["p"] == 1.0
    _raises(lambda: t4.t4(_t4_ops5(order), lambda: cols, [1.0, 2.0, 3.0], [1.0, 2.0, 3.0]), "ddof of V_k")


def test_t4_zero_denominator_at_any_k():
    cols = _t4_cols()
    cols["tp"]["A-1"] = cols["tp"]["OP_25"].copy()  # k = 2 has Delta = 0 in every replicate: V_2 = 0
    order = ["OP_strict", "OP_25", "OP_mid", "OP_75", "OP*"]
    res = t4.t4(_t4_ops5(order), lambda: cols, [40.0, 40.0, 40.0], [50.0, 50.0, 50.0], vk_ddof=1, b=50, seed=1)
    assert res["label"] == "NOT_IDENTIFIED" and res["p"] == 1.0 and res["V"][1] == 0.0 and res["V"][0] > 0


def test_t4_reads_ops5_only():
    with tempfile.TemporaryDirectory() as d:
        o = _ops5_file(d)
        assert t4.load_ops5(o)["result"] == "IDENTIFIED"
        k = Path(d) / "k0.json"
        _raises(lambda: t4.load_ops5(k), "never a k0.json")
        (Path(d) / "ops5.json.sha256").write_text("0" * 64 + "  ops5.json\n")
        _raises(lambda: t4.load_ops5(o), "sha256")


def _a8_records():
    heads = ["chó", "mèo", "xe máy", "bàn", "ghế", "ô tô", "con ngựa", "cây", "quả bóng", "tivi", "cái ô", "xe đạp"]
    recs = []
    for i in range(3):
        r = _fair_rec(heads)
        r.update(image_id=str(i), file_name=f"{i}.jpg", reference_captions=[f"Mây tím có {h} lơ lửng." for h in heads[:4]])
        for j, p in enumerate(r["propositions"]):
            p["evidence"] = {"probes": [{"model": VIN, "question_vi": f"Trong ảnh có {heads[j]} không?"}]}
        recs.append(r)
    return recs


def test_a8_is_s1_arm_with_the_scaled_budget():
    recs, tab = _k0_records()
    s1 = gate.run_k0(recs, {"vintern": tab})["s1"]
    mine = a8.arm_store(recs, False, "S1", None)
    keys = ("R", "P", "rows", "sft_sha256", "uncap", "mean_budget", "store", "n")
    assert {k: mine[k] for k in keys} == {k: s1[k] for k in keys}
    recs = _a8_records()
    unc, _ = store.uncap(recs)
    rows, rep = store.rebuild(unc, scaled=True)
    rows9, _ = store.rebuild(unc, scaled=False)
    with tempfile.TemporaryDirectory() as d:
        got = a8.a8_store(recs, d)
        assert got["sft_sha256"] == store.store_sha(rows) != store.store_sha(rows9) and got["store"] == "A8"
        assert got["mean_budget"] == 15 and (Path(d) / "A8" / "sft.jsonl").exists()
        assert hashlib.sha256((Path(d) / "A8" / "sft.jsonl").read_bytes()).hexdigest() == got["sft_sha256"]
    assert [p["verification"]["status"] for p in recs[0]["propositions"]] == ["SUPPORTED"] * 12  # caller unchanged


def test_a8_launcher_refuses_overwrite():
    env = {**os.environ, "O31_SRC": os.environ.get("O31_SRC", str(HERE / "src"))}
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "rec").mkdir()
        for r in _a8_records():
            (Path(d) / "rec" / f"{r['image_id']}.json").write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
        (Path(d) / "ex.txt").write_text("2.jpg\n")
        cmd = [sys.executable, "-I", "-B", str(HERE / "a8store.py"), "--records", f"{d}/rec", "--exclude", f"{d}/ex.txt",
               "--store-dir", f"{d}/st", "--out", f"{d}/a8.json"]
        r = subprocess.run(cmd, capture_output=True, text=True, env=env)
        assert r.returncode == 0, r.stderr[-800:]
        res = json.loads(Path(f"{d}/a8.json").read_text())
        assert res["inputs"]["n_records"] == 2 and res["inputs"]["n_excluded"] == 1 and "Mây" not in json.dumps(res)
        r = subprocess.run(cmd, capture_output=True, text=True, env=env)
        assert r.returncode != 0 and "exists" in r.stderr


_PA_CAPS = ["Chó tím ngủ cạnh ghế bay, rồi một chiếc ô tô nhỏ ghé qua.", "Mèo bạc ôm tivi trên bàn đá.",
            "Xe đạp hồng chở chó lùn qua cây cầu mây."]


def _pa_inputs(d, n=10):
    from PIL import Image
    d = Path(d)
    (d / "img").mkdir(exist_ok=True)
    items, preds = [], {}
    for k in range(n):
        f = f"im{k:03d}.png"
        Image.new("RGB", (8, 8), (k * 20 % 255, 9, 9)).save(d / "img" / f)
        items.append((f"id{k}", f, hashlib.sha256((d / "img" / f).read_bytes()).hexdigest()))
        preds[f"id{k}"] = _PA_CAPS[k % 3]
    pp = d / "s0.preds.json"
    pp.write_text(json.dumps(preds, ensure_ascii=False), encoding="utf-8")
    (d / "s0.preds.json.sha256").write_text(hashlib.sha256(pp.read_bytes()).hexdigest() + "  s0.preds.json\n")
    return items, pp


def test_g3v_pa_builder_q_plus_on_matched_phrase():
    with tempfile.TemporaryDirectory() as d:
        items, pp = _pa_inputs(d)
        preds = vcoco.read_decode(pp, items)
        work, units = vcoco.pa_work(preds, items)
        assert [f for f, _ in work] == sorted(f for _i, f, _h in items)
        props = extract.entity_propositions(_PA_CAPS[0])
        assert units[0]["classes"] == [p["cls"] for p in props] == extract.ordered_classes(_PA_CAPS[0])
        assert [q for _k, q in work[0][1]] == [f"Trong ảnh có {p['text_vi']} không" for p in props]
        repo()
        from rescap.pipeline.verify import build_questions
        assert work[0][1][0][1] == build_questions({"type": "entity", "subject": {"text_vi": props[0]["text_vi"]}})[0]
        assert all(k == verify.qkey(q) for _f, qs in work for k, q in qs)
        pp.write_text(pp.read_text(encoding="utf-8") + " ", encoding="utf-8")
        _raises(lambda: vcoco.read_decode(pp, items), "sidecar")
        _raises(lambda: vcoco.check_images(items, Path(d) / "img", set()), "not the registered")
        assert vcoco.check_images(items, Path(d) / "img", {h for _i, _f, h in items}) is None


def _g3v_run(d, items, pp, fam_done=("vintern", "internvl3")):
    preds = vcoco.read_decode(pp, items)
    work, _units = vcoco.pa_work(preds, items)
    rc = {}
    for f in fam_done:
        rc[f] = vcoco.run_family(_fake_probe(), work, Path(d) / "g3v", f, lambda n: n)
    return rc


def test_g3v_job_clock_cap_and_k1():
    with tempfile.TemporaryDirectory() as d:
        items, pp = _pa_inputs(d)
        (Path(d) / "K1_fired.json").write_text('{"fired": true}')  # G3v runs whatever K1 shows (G-5)
        assert _g3v_run(d, items, pp) == {"vintern": 0, "internvl3": 0}
        st = vcoco.status(Path(d) / "g3v")
        assert st == {"vintern": "DONE", "internvl3": "DONE", "row": "DONE"}
        t0 = json.loads((Path(d) / "g3v" / "launch.json").read_text())["t0"]
        assert all(json.loads((Path(d) / "g3v" / f / "launch.json").read_text())["t0"] == t0 for f in vcoco.FAMILIES)
    with tempfile.TemporaryDirectory() as d:
        items, pp = _pa_inputs(d)
        root = Path(d) / "g3v"
        root.mkdir()
        (root / "launch.json").write_text(json.dumps({"t0": time.time() - 2 * 3600, "job": "G3v", "cap_h": 1.0}))
        assert _g3v_run(d, items, pp, ("vintern",)) == {"vintern": 4}
        assert vcoco.status(root)["row"] == "NOT RUN"
    with tempfile.TemporaryDirectory() as d:
        items, pp = _pa_inputs(d)
        root = Path(d) / "g3v"
        root.mkdir()
        (root / "launch.json").write_text(json.dumps({"t0": time.time(), "job": "G3"}))
        _raises(lambda: _g3v_run(d, items, pp, ("vintern",)), "clock of job")
        (root / "launch.json").write_text(json.dumps({"t0": time.time(), "job": "G3v"}))
        (root / "vintern").mkdir()
        (root / "vintern" / "launch.json").write_text(json.dumps({"t0": 1.0, "family": "vintern"}))
        _raises(lambda: _g3v_run(d, items, pp, ("vintern",)), "second launch clock")


def test_g3v_launcher_status_and_size():
    env = {**os.environ, "O31_SRC": os.environ.get("O31_SRC", str(HERE / "src"))}
    with tempfile.TemporaryDirectory() as d:
        items, pp = _pa_inputs(d, n=10)  # >= 20 probes for the smoke rule; not the 231 of G-1
        tsv = Path(d) / "items.tsv"
        tsv.write_text("".join("\t".join(it) + "\n" for it in items))
        r = subprocess.run([sys.executable, "-I", "-B", str(HERE / "g3v.py"), "run", "--family", "vintern", "--preds",
                            str(pp), "--items", str(tsv), "--images", f"{d}/img", "--snapshot", d, "--out", f"{d}/g"],
                           capture_output=True, text=True, env=env)
        assert r.returncode != 0 and "231 UIT-ViIC test images" in r.stderr and not Path(f"{d}/g").exists()
        _g3v_run(d, items, pp, ("vintern",))
        r = subprocess.run([sys.executable, "-I", "-B", str(HERE / "g3v.py"), "status", "--out", f"{d}/g3v"],
                           capture_output=True, text=True, env=env)
        assert json.loads(r.stdout) == {"vintern": "DONE", "internvl3": "INCOMPLETE", "row": "INCOMPLETE"}


def test_host_selftest_calls_scripts_through_bash():
    """A committed script may lose its mode bit (git archive gives 644): every .sh is called through bash."""
    lines = (HERE / "host_selftest.sh").read_text(encoding="utf-8").splitlines()
    calls = [ln for ln in lines if re.search(r'"\$HERE/[^"]+\.sh"', ln) and not ln.lstrip().startswith("#")]
    assert calls and all(re.search(r'\bbash "\$HERE/[^"]+\.sh"', ln) for ln in calls), calls
    rt = (HERE / "run_tests.sh").read_text(encoding="utf-8")
    assert "sha256sum -c PROTECTED_071c8dc.sha256" in rt


def test_zz_import_closure_pinned():
    """W2: runs last; every repo file loaded by the suite (incl. run_k0 through the real builder and person_uncap)
    is in REUSED, so repo() sha-checks it."""
    assert {"build_dpo_data", "person_uncap", "w25", "rescap.pipeline.select"} <= set(sys.modules)
    root = REPO.resolve()
    loaded = {str(Path(m.__file__).resolve().relative_to(root)) for m in list(sys.modules.values())
              if getattr(m, "__file__", None) and Path(m.__file__).resolve().is_relative_to(root)}
    assert loaded and loaded <= set(REUSED), sorted(loaded - set(REUSED))


def main() -> int:
    tests = [(k, v) for k, v in globals().items() if k.startswith("test_") and callable(v)]
    bad = 0
    for name, fn in tests:
        try:
            fn()
            print(f"ok   {name}")
        except Exception as e:  # noqa: BLE001 - report every failing test, exit non-zero
            bad += 1
            print(f"FAIL {name}: {type(e).__name__}: {e}")
            if os.environ.get("O31_FAILFAST") == "1":  # mutant runs: a kill needs one failing test
                break
    print(f"{len(tests) - bad}/{len(tests)} passed")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
