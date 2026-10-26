#!/usr/bin/env python3
"""Post hoc MBR-3 row over P1-R's existing KTVIC-test captions (Paper B), for
manuscript/prereg/2026-10-26_b_posthoc/PREREG.md (sha256 08afefd4…, commit 13da5d7): CPU re-scoring only, no decode,
label POST_HOC, no verdict. It reuses scripts/b_f1/score_b_f1.py (look, selector, evaluate_py, f0, statistics,
pin_all, gate_body) with every function body unchanged, adding the registered gates G1-G8.

    posthoc_mbr3.py dry OUT.json    SYNTHETIC ids, references and captions only: exercises K-COV, K-L1 (pass and stop),
                                    the dropped fields, the no-caption rule, the gate and split comparisons and the
                                    once-only refusal; reads no KTVIC file and no member file
    posthoc_mbr3.py run             the one run; only with this file, the PREREG and ADDENDUM_C3.md committed at HEAD;
                                    writes the record named in the addendum, never overwritten

Both need VNCORENLP_DIR, JAVA_HOME (a JDK, for jnius) and java on PATH; run also needs NCS_DATA (KTVIC under
datasets/ktvic). Prints and writes numbers, ids and hashes only, never a caption. score_b_f1.main() is never called.
"""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import os
import re
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
_spec = importlib.util.spec_from_file_location("score_b_f1", HERE.parent / "score_b_f1.py")
S = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(S)  # defines functions only; its main() is never called
ROOT, sha = S.ROOT, S.sha

RUNNER = "scripts/b_f1/posthoc_mbr3.py"
PREREG = ("manuscript/prereg/2026-10-26_b_posthoc/PREREG.md",
          "08afefd4fe87229c2d48415fc3f46f3ef95de11c05b52f937e953a807483f823")
ADDENDUM = "manuscript/prereg/2026-10-26_b_posthoc/ADDENDUM_C3.md"
GATE = ("manuscript/prereg/2026-10-20_b_f1_record/b_f1_gate.json",
        "cf64ee1c4caa2f483141e9d8b202d25af23e93c523e490a74a63d082a79b8dc2")
SEEDS = S.SEEDS
# §A.2 members (test-caption files) and their committed L1 results (K-L1)
MEMBERS = {"s42": ("data/results/p1assist_s42-short.preds.json",
                   "ca5ce25366b04def1ca1099344a0e4a610bf767e357140525e4290913ffe2fef"),
           "s43": ("data/results/p1assist_s43-short.preds.json",
                   "13343482926cade1e3640185e3c5bd7cd504df5f2a2099ffb614d7a9bcb51861"),
           "s44": ("data/results/p1assist_s44-short.preds.json",
                   "9344cb3504f3b925156ee59952735e946a97de29b682583d217de4198060f248")}
L1 = {"s42": ("data/results/p1assist_s42-short.json",
              "ea38b60e7dc5c243356b98b8ac19b91165cb93ecb6f8a6f2badcbeb7053dbfa9", 148.66403869141925),
      "s43": ("data/results/p1assist_s43-short.json",
              "ce8576a440d55888c2954070cef7c916f8030de94f5e171d9e6a02aef79137eb", 148.06296896003204),
      "s44": ("data/results/p1assist_s44-short.json",
              "723d97653f895e98306a4dbbbf85a1dcd1d6df9012422711bfd85f98b2cca2ad", 147.96149059506558)}
L1_TOL = 1e-6
# §A.3/§A.4 code and reference pins (K-PIN)
CODE = {"scripts/seed_consensus.py": "2b72dc417d60c5ec6a0be9cfd3b69692a783e2ba9bd1fc7dcb14c5195296c486",
        "scripts/b_f1/score_b_f1.py": "9c57cc9771d6da84f56534004ebd60c72acd1103ca7c63a741c2f482881304aa",
        "scripts/evaluate.py": "a68d56826d90d8a409493cd6f49007e906c6cb4f5668314edb9b8e7a632e8236",
        "scripts/rl_report.py": "f92faa61965348fc5296f7e97399a82086a125c1b936b9dfb4494cda266997c5",
        "scripts/rl_reward.py": "3b18b7a3620c2511d4d13caea62f204534783e3024cac188da78d957e6a0a74b"}
REFS = {"data/datasets/ktvic/test_data.json": "cc22ec6a8883773cb23c87ad5b64925f5a53c21982117274b53621f454e7ebbf",
        "data/datasets/ktvic/train_data.json": "72ee9b57c350fb5f215e1f04701c515a51e5e415240e51a77c8ce00ce6316a0f"}
SPLIT = ("data/splits/ktvic_train_minus_dev300.txt",
         "006080b455a553ca9cc5d3f514ad76bfbe67f444c9c145a5696de681a4be1a58", 3469)
CLEAN = ("data/lb/splits/ktvic_test_openviic_train_clean.txt",
         "4832c16b4499a70b5b6d5c3967a22f551283b45b3a885ba011301b6a4e90015e")
N_TEST = 558
# G5: every verdict, kill or claim label statistics() writes (score_b_f1.py l.405-439; CP-112 W3(e), CP-112a ruling 1)
DROP = (("primary", "verdict"), ("K2", "fires"), ("K2", "reported_as"), ("K3", "fires"), ("K3", "reported_as"),
        ("prediction_check", None), ("objects", "claims_allowed"), ("objects", "status"))
PRECOMMIT = ("G8: whatever the value, no abstract or conclusion sentence of Paper B changes; sec5.1 gets at most one "
             "claim-free post hoc sentence (PREREG §A.6)")


class Stop(SystemExit):
    """A registered stop: the record is not written, nothing is re-run, the work returns to the judge."""


# ------------------------------------------------------------------------------------------- gates
def refuse_existing(out: Path) -> None:
    """G7: once only."""
    if out.exists():
        raise Stop(f"REFUSED (G7): {out} exists; the row runs once and is never overwritten")


def gate_equal(body: dict, G: dict, scorer_sha: str, prereg_sha: str) -> list[str]:
    """G1: what run() requires of the committed B-F1 gate record and of a fresh gate_body (score_b_f1.py l.477-486)."""
    bad = [k for k, want in (("mode", "gate"), ("all_pass", True), ("script_sha256", scorer_sha)) if G.get(k) != want]
    bad += ["prereg"] if G.get("prereg", {}).get("sha256") != prereg_sha else []
    bad += ["body.all_pass"] if not body.get("all_pass") else []
    return bad + [k for k in ("pins", "instrument", "self_check") if body.get(k) != G.get(k)]


def split_equal(rest: list[str], pinned_ids: list[str], n: int) -> bool:
    """G2: sc.split_ids rest equals the pinned train-minus-dev300 list, as a set and in count."""
    return len(rest) == len(set(rest)) == n and set(rest) == set(pinned_ids) and len(pinned_ids) == n


def coverage(caps: dict, ids: list[str]) -> None:
    """G3 / K-COV, before selection: each member's keys are exactly the test ids."""
    bad = [s for s in SEEDS if sorted(caps[s]) != ids]
    if bad:
        raise Stop(f"STOP (K-COV): member(s) {bad} do not cover exactly the {len(ids)} test ids; no selection ran")


def strip(rec: dict) -> dict:
    """G5: drop every verdict, kill and claim label before anything is written or printed."""
    for key, sub in DROP:
        if sub is None:
            rec.pop(key, None)
        elif isinstance(rec.get(key), dict):
            rec[key].pop(sub, None)
    left = [f"{k}.{s}" for k, s in DROP if (s is None and k in rec) or (s and s in rec.get(k, {}))]
    if left:
        raise AssertionError(f"G5: fields left {left}")
    return rec


@contextlib.contextmanager
def l1_guard(want: dict[str, float], member_names: dict[str, str], mbr_name: str, tmp: Path, calls: dict):
    """G4 / K-L1 inside look's member loop: wraps the module-level evaluate_py and f0 (their bodies unchanged). After
    the three members are scored, each corpus CIDEr-D must equal its committed L1 value within 1e-6, before the MBR
    file is scored and before statistics() runs; each member is scored once. On a mismatch the MBR preds in tmp are
    deleted (only their sha256 is kept) and Stop is raised, so no record is written."""
    ev0, f00, st0 = S.evaluate_py, S.f0, S.statistics
    seed_of = {n: s for s, n in member_names.items()}
    got: dict[str, float] = {}

    def evaluate_py(preds, name, tmp_, ncs):
        if name == mbr_name and len(got) < len(SEEDS):
            raise AssertionError("K-L1 guard: the MBR file reached scoring before the member check")
        if name not in seed_of and name != mbr_name or name in calls["evaluate"]:
            raise AssertionError(f"K-L1 guard: {name} unknown or scored twice")
        calls["evaluate"].append(name)
        return ev0(preds, name, tmp_, ncs)

    def f0(M, result, reward, ids, tol):
        out, per = f00(M, result, reward, ids, tol)
        name = result.name.removesuffix(".json")
        if name in seed_of:
            got[seed_of[name]] = out["corpus_CIDEr_x100"]
            if len(got) == len(SEEDS):
                bad = [s for s in SEEDS if not abs(got[s] - want[s]) < L1_TOL]
                calls["l1"] = {s: {"rescored": got[s], "committed": want[s]} for s in SEEDS}
                if bad:
                    mbr = tmp / f"{mbr_name}.preds.json"
                    calls["mbr_tmp_sha256"] = sha(mbr.read_bytes()) if mbr.is_file() else None
                    mbr.unlink(missing_ok=True)
                    raise Stop(f"STOP (K-L1): member(s) {bad} differ from their committed L1 CIDEr-D by >= {L1_TOL}; "
                               f"no record written, nothing re-run; tmp MBR preds sha256 "
                               f"{calls['mbr_tmp_sha256']} deleted")
        return out, per

    def statistics(*a, **k):
        calls["statistics"] += 1
        return st0(*a, **k)

    S.evaluate_py, S.f0, S.statistics = evaluate_py, f0, statistics
    try:
        yield
    finally:
        S.evaluate_py, S.f0, S.statistics = ev0, f00, st0


def guarded_look(P, cfg, M, seg, caps, files, train_refs, rest, test_refs, clean, ncs, tmp, want, calls) -> dict:
    ids = sorted(test_refs)
    coverage(caps, ids)
    names = {s: Path(files[s]).name.removesuffix(".preds.json") for s in SEEDS}
    with l1_guard(want, names, cfg["names"]["mbr"], tmp, calls):
        res = S.look(P, cfg, M, seg, caps, files, train_refs, rest, test_refs, clean, ncs, tmp)
    if calls["statistics"] > 1 or sorted(calls["evaluate"]) != sorted([*names.values(), cfg["names"]["mbr"]]):
        raise AssertionError(f"K-L1 guard: scoring calls {calls}")
    return strip(res)


# ------------------------------------------------------------------------------------------- run
def addendum() -> dict:
    """The committed addendum's JSON block (mapping, names, paths), checked against this file."""
    text = S.pinned(ADDENDUM).decode("utf-8")
    block = json.loads(re.search(r"```json\n(.*?)\n```", text, re.S)[1])
    want = {s: list(MEMBERS[s]) for s in SEEDS}
    if block.get("runner") != {"path": RUNNER, "sha256": sha(HERE.read_bytes())} or block.get("members") != want \
            or block.get("prereg") != {"path": PREREG[0], "sha256": PREREG[1]}:
        raise Stop("REFUSED (K-PIN): ADDENDUM_C3.md does not name this runner, the §A.2 members or the PREREG")
    return block


def run() -> int:
    if os.environ.get("B_F1_STAGE"):
        raise Stop("REFUSED: B_F1_STAGE is set")
    S.pinned(RUNNER)  # this file equals its blob at HEAD
    S.pinned(*PREREG)
    A = addendum()
    out = ROOT / A["paths"]["record"]
    refuse_existing(out)  # G7
    P, cfg = S.load()
    cfg = cfg | {"names": cfg["names"] | {"mbr": A["names"]["mbr"]}}
    M = S.modules()
    from rl_reward import Segmenter
    seg = Segmenter()
    # G1 / K-SC: pins, then gate_body (self_check) equal to the committed B-F1 gate; reads S1 dev outputs only
    G = json.loads(S.pinned(*GATE))
    body = S.gate_body(P, cfg, M, seg)
    bad = gate_equal(body, G, CODE["scripts/b_f1/score_b_f1.py"], S.PREREG[1])
    if bad:
        raise Stop(f"STOP (K-SC, G1): gate or self-check differs from the committed B-F1 gate: {bad}")
    # G2 / K-SC: pinned split
    ev, sc = M[0], M[4]
    _, rest = sc.split_ids(sc.load_prereg())
    if not split_equal(rest, S.pinned(SPLIT[0], SPLIT[1]).decode("utf-8").split(), SPLIT[2]):
        raise Stop("STOP (K-SC, G2): sc.split_ids rest differs from the pinned train-minus-dev300 list")
    # K-PIN: code, references, clean list, L1 results
    for rel, want in CODE.items():
        S.pinned(rel, want)
    for rel, want in REFS.items():
        if S.sha_file(S.ncs_file(rel)) != want:
            raise Stop(f"STOP (K-PIN): {rel} under NCS_DATA differs from its pin")
    clean = sorted(S.pinned(*CLEAN).decode("utf-8").split())
    want = {}
    for s, (rel, h, value) in L1.items():
        row = next(r for r in json.loads(S.pinned(rel, h))["results"] if r["tokenization"] == "word-level")
        if row["scores_scaled_x100"]["CIDEr"] != value:
            raise Stop(f"STOP (K-PIN): {rel} does not hold the registered L1 value")
        want[s] = value
    test_refs = ev.references("test_data.json")
    ids = sorted(test_refs)
    if len(ids) != N_TEST or len(clean) != cfg["n_clean"] or not set(clean) <= set(ids):
        raise Stop("STOP (K-PIN): the test ids or the clean list differ from the registration")
    caps = {s: json.loads(S.pinned(*MEMBERS[s])) for s in SEEDS}  # the members are read only here, after G1-G2
    calls = {"evaluate": [], "statistics": 0}
    with tempfile.TemporaryDirectory() as t:  # outside the repository: the MBR preds and evaluate.py outputs
        tmp = Path(t)
        if tmp.resolve().is_relative_to(ROOT):
            raise Stop("REFUSED (G6): the temporary directory is inside the repository")
        files = {s: ROOT / MEMBERS[s][0] for s in SEEDS}
        res = guarded_look(P, cfg, M, seg, caps, files, ev.references("train_data.json"), rest, test_refs, clean,
                           Path(os.environ["NCS_DATA"]), tmp, want, calls)
    rec = {"id": "b_posthoc_mbr3", "label": "POST_HOC", "verdict": None,
           "authority": "PI-1026e Q2 (2026-10-26), lifting the B-F1 §9 closure for this one row; B-F1 verdict FAIL "
                        "unchanged; §9 closure restored after this row",
           "prereg": dict(zip(("path", "sha256"), PREREG)), "addendum": {"path": ADDENDUM, "sha256": S.SEEN[ADDENDUM]},
           "runner_sha256": sha(HERE.read_bytes()), "b_f1_prereg": dict(zip(("path", "sha256"), S.PREREG)),
           "config": cfg, "env": S.env(), "G1_gate_equal": True, "G2_split_equal": True,
           "members": {s: dict(zip(("path", "sha256"), MEMBERS[s])) for s in SEEDS}, "K_L1": calls["l1"],
           "precommitment": PRECOMMIT, **res, "inputs_sha256": dict(sorted(S.SEEN.items()))}
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "x", encoding="utf-8") as f:  # G7 again at write time
        json.dump(rec, f, ensure_ascii=False, indent=1, default=lambda o: o.item())
    print(json.dumps({"mode": "run", "label": "POST_HOC", "record": A["paths"]["record"],
                      "sha256": sha(out.read_bytes()), "K_F0_fired": res.get("K_F0_fired")}))
    return 1 if res.get("K_F0_fired") else 0


# ------------------------------------------------------------------------------------------- dry run
def dry(out: Path) -> int:
    """SYNTHETIC only: no KTVIC file, no member file and no S1 output is read."""
    refuse_existing(out)
    P, cfg = S.load()  # B-F1's registered constants (B, seed, level, tol, k2), read from the committed JSON
    cfg = cfg | {"names": cfg["names"] | {"mbr": "synthetic_mbr3-test-short"}}
    rng = np.random.default_rng(11)
    objs = ["người", "chó", "mèo", "bàn", "xe máy", "ghế"]
    filler = ["một", "đang", "đứng", "ngồi", "cạnh", "trên", "trong", "sân", "nhà", "đường"]
    rec = {"SYNTHETIC": "made-up ids, references and captions; no KTVIC file, member file or S1 output is read",
           "runner_sha256": sha(HERE.read_bytes()), "prereg": dict(zip(("path", "sha256"), PREREG))}
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        ncs = tmp / "ncs"
        (ncs / "datasets" / "ktvic").mkdir(parents=True)
        test_ids, train_ids = sorted(str(100 + 3 * k) for k in range(60)), [str(900 + k) for k in range(40)]
        obj = {i: [objs[int(j)] for j in rng.choice(len(objs), 2, replace=False)] for i in test_ids + train_ids}
        refs = {i: [f"{obj[i][0]} {S._syn(rng, filler, 3)} {obj[i][1]} {S._syn(rng, filler, 2)}" for _ in range(5)]
                for i in test_ids + train_ids}
        for split, ids in (("test_data.json", test_ids), ("train_data.json", train_ids)):
            (ncs / "datasets" / "ktvic" / split).write_text(json.dumps({
                "images": [{"id": int(i), "filename": f"{i}.jpg"} for i in ids],
                "annotations": [{"image_id": int(i), "caption": c} for i in ids for c in refs[i]]},
                ensure_ascii=False), encoding="utf-8")
        keep = os.environ.get("NCS_DATA")
        os.environ["NCS_DATA"] = str(ncs)
        try:
            M = S.modules()
            from evaluate import references
            from rl_reward import Segmenter
            seg = Segmenter()
            caps = {"s42": {i: refs[i][0] for i in test_ids}, "s43": {i: refs[i][int(i) % 2] for i in test_ids},
                    "s44": {i: f"{objs[int(i) % len(objs)]} {S._syn(rng, filler, 4)}" for i in test_ids}}
            files = {}
            for s in SEEDS:
                files[s] = tmp / f"synthetic_{s}-test-short.preds.json"
                files[s].write_text(json.dumps(caps[s], ensure_ascii=False, indent=1), encoding="utf-8")
            test_refs = references(str(ncs / "datasets" / "ktvic" / "test_data.json"))
            train_refs = references(str(ncs / "datasets" / "ktvic" / "train_data.json"))
            clean = test_ids[::3]
            texts = {c for s in SEEDS for c in caps[s].values()} | {c for r in refs.values() for c in r}
            seen = io.StringIO()

            # synthetic L1: each member scored once by the unchanged evaluate_py/f0, as the committed results were
            reward = M[3].Reward(test_refs, seg)
            want = {}
            with tempfile.TemporaryDirectory() as t1:
                for s in SEEDS:
                    r = S.evaluate_py(files[s], files[s].name.removesuffix(".preds.json"), Path(t1), ncs)
                    want[s] = S.f0(M, r, reward, test_ids, cfg["tol"])[0]["corpus_CIDEr_x100"]

            # G3 / K-COV: one id missing from s44
            short = {"s42": caps["s42"], "s43": caps["s43"], "s44": dict(list(caps["s44"].items())[1:])}
            calls = {"evaluate": [], "statistics": 0}
            try:
                guarded_look(P, cfg, M, seg, short, files, train_refs, train_ids, test_refs, clean, ncs, tmp, want,
                             calls)
                kcov = "not fired"
            except Stop as e:
                kcov = str(e)
            assert kcov.startswith("STOP (K-COV)") and calls == {"evaluate": [], "statistics": 0}, (kcov, calls)
            rec["K_COV"] = {"message": kcov, "scoring_calls": calls["evaluate"], "statistics_calls": calls["statistics"]}

            # K-L1 pass: the whole row, fields dropped, each system scored once, statistics once
            calls = {"evaluate": [], "statistics": 0}
            with tempfile.TemporaryDirectory() as t2, contextlib.redirect_stdout(seen), contextlib.redirect_stderr(seen):
                res = guarded_look(P, cfg, M, seg, caps, files, train_refs, train_ids, test_refs, clean, ncs, Path(t2),
                                   want, calls)
            assert not res["K_F0_fired"] and calls["statistics"] == 1 and len(calls["evaluate"]) == 4, calls
            assert "prediction_check" not in res and "verdict" not in res["primary"], sorted(res)
            assert not {"fires", "reported_as"} & (set(res["K2"]) | set(res["K3"])), (res["K2"], res["K3"])
            assert not {"claims_allowed", "status"} & set(res["objects"]), res["objects"]
            dump = json.dumps(res, ensure_ascii=False)
            assert not any(c in dump for c in texts), "G6: a caption reached the record"
            rec["K_L1_pass"] = {"scoring_calls": calls["evaluate"], "statistics_calls": calls["statistics"],
                                "K_L1": calls["l1"], "kept_keys": sorted(res),
                                "primary_keys": sorted(res["primary"]), "K2_keys": sorted(res["K2"]),
                                "K3_keys": sorted(res["K3"]), "objects_keys": sorted(res["objects"]),
                                "D_MBR_x100_mean_lo_hi": res["primary"]["D_MBR_x100_mean_lo_hi"],
                                "mbr_preds_sha256": res["selection"]["mbr_preds_sha256"]}

            # K-L1 stop: s43's committed value off by 0.01; MBR never scored, statistics never called, tmp preds gone
            calls = {"evaluate": [], "statistics": 0}
            with tempfile.TemporaryDirectory() as t3, contextlib.redirect_stdout(seen), contextlib.redirect_stderr(seen):
                try:
                    guarded_look(P, cfg, M, seg, caps, files, train_refs, train_ids, test_refs, clean, ncs, Path(t3),
                                 want | {"s43": want["s43"] + 0.01}, calls)
                    kl1 = "not fired"
                except Stop as e:
                    kl1 = str(e)
                mbr_left = (Path(t3) / f"{cfg['names']['mbr']}.preds.json").exists()
            assert kl1.startswith("STOP (K-L1)") and "s43" in kl1, kl1
            assert cfg["names"]["mbr"] not in calls["evaluate"] and calls["statistics"] == 0 and not mbr_left, calls
            assert sorted(calls["evaluate"]) == sorted(f.name.removesuffix(".preds.json") for f in files.values())
            rec["K_L1_stop"] = {"message": kl1, "scoring_calls": calls["evaluate"],
                                "statistics_calls": calls["statistics"], "mbr_tmp_deleted": not mbr_left,
                                "mbr_tmp_sha256": calls["mbr_tmp_sha256"]}
            printed = seen.getvalue()
            assert not any(c in printed for c in texts), "G6: a caption was printed"
            rec["G6_no_caption"] = {"captured_output_chars": len(printed), "caption_in_output": False,
                                    "caption_in_record": False}
        finally:
            if keep is None:
                os.environ.pop("NCS_DATA", None)
            else:
                os.environ["NCS_DATA"] = keep

    # G1 and G2 comparison logic on synthetic records (the real gate runs only in `run`)
    G = {"mode": "gate", "all_pass": True, "script_sha256": "a" * 64, "prereg": {"sha256": "b" * 64},
         "pins": {"x": "1"}, "instrument": {"y": True}, "self_check": [{"check": "z", "ok": True}]}
    body = {"all_pass": True, "pins": {"x": "1"}, "instrument": {"y": True}, "self_check": [{"check": "z", "ok": True}]}
    g1 = {"equal": gate_equal(body, G, "a" * 64, "b" * 64),
          "self_check differs": gate_equal(body | {"self_check": [{"check": "z", "ok": False}]}, G, "a" * 64, "b" * 64),
          "pins differ": gate_equal(body | {"pins": {"x": "2"}}, G, "a" * 64, "b" * 64),
          "scorer differs": gate_equal(body, G, "c" * 64, "b" * 64)}
    assert g1["equal"] == [] and all(g1[k] for k in g1 if k != "equal"), g1
    ids = [str(k) for k in range(10)]
    g2 = {"equal": split_equal(sorted(ids), ids, 10), "one id differs": split_equal(ids[:9] + ["x"], ids, 10),
          "count differs": split_equal(ids[:9], ids[:9], 10)}
    assert g2 == {"equal": True, "one id differs": False, "count differs": False}, g2
    rec["G1_comparison"], rec["G2_comparison"] = g1, g2
    probe = Path(tempfile.mkdtemp()) / "exists.json"
    probe.write_text("{}", encoding="utf-8")
    try:
        refuse_existing(probe)
        g7 = "not refused"
    except Stop as e:
        g7 = str(e).split(":")[0]
    probe.unlink()
    probe.parent.rmdir()
    assert g7 == "REFUSED (G7)", g7
    rec["G7_refusal"] = g7
    rec["main_called"] = False
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "x", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=1, default=lambda o: o.item())
    print(json.dumps({"mode": "dry", "all_pass": True, "record": str(out), "sha256": sha(out.read_bytes())}))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=("dry", "run"))
    ap.add_argument("out", nargs="?", help="dry: the output JSON (never overwritten)")
    a = ap.parse_args()
    if a.mode == "dry":
        if not a.out:
            raise SystemExit("dry needs OUT")
        return dry(Path(a.out))
    if a.out:
        raise SystemExit("run takes no OUT: the record path is the addendum's")
    return run()


if __name__ == "__main__":
    sys.exit(main())
