"""O31 self-tests: synthetic fixtures only (no dataset caption, no image). Run: run_tests.sh.

The package is imported from $O31_SRC (default ./src) so mutants.py can point it at a mutated copy.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import random
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, os.environ.get("O31_SRC", str(HERE / "src")))

import numpy as np  # noqa: E402

from o31 import REPO, REUSED, decode, extract, gate, metrics, no_forbidden, overlap, repo, store, train, verify  # noqa: E402
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
        (d / "probes.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows), encoding="utf-8")
        (d / "excl.txt").write_text("3.jpg\n", encoding="utf-8")
        cmd = [sys.executable, "-I", "-B", str(HERE / "k0.py"), "--records", str(d / "rec"), "--table",
               f"vintern={d / 'probes.jsonl'}", "--exclude", str(d / "excl.txt"), "--store-dir", str(d / "stores"),
               "--out", str(d / "k0.json")]
        env = {**os.environ, "O31_SRC": os.environ.get("O31_SRC", str(HERE / "src"))}
        r = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=d)
        assert r.returncode == 0, r.stderr[-2000:]
        res = json.loads((d / "k0.json").read_text(encoding="utf-8"))
        assert res["inputs"]["n_records"] == 3 and res["inputs"]["n_excluded"] == 1
        assert res["inputs"]["tables"]["vintern"] == hashlib.sha256((d / "probes.jsonl").read_bytes()).hexdigest()
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
    print(f"{len(tests) - bad}/{len(tests)} passed")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
