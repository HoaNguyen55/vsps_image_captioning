#!/usr/bin/env python3
"""Synthetic self-test and named mutants for a_e6_split.py (REG-1119a). Rented host only (PI-1111j); no label file.

  test_a_e6_split.py selftest --out F   hand values on the a_cert_e3 mini world, keys extended (fixture() docstring)
  test_a_e6_split.py mutants --out F    the unmutated source must pass first; each mutant applies exact replacements
                                        (each target must occur exactly once) to a copy of the source, executed with
                                        __file__ = the original; KILLED = at least one of its named checks is False
                                        (an exception inside a check is recorded as None, never a kill)
"""
import contextlib
import hashlib
import io
import json
import os
import shutil
import sys
import tempfile
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "a_e6_split.py"
sys.path.insert(0, str(HERE.parent / "a_cert"))
import a_cert_e3 as E  # noqa: E402

A, Fault, q_ = E.A, E.Fault, E._q
E_ORIG = E.score_e3_core
REASON = "the investigator watched R2's screen from time to time on 2026-11-18, PI-1118ai/aj"  # REG-1119a
REG_LINE = (f"x | REG-1119a-topup-e6-split | ... with (iii) the count of old_repeat items on listed images and the "
            f"count of same-map pairs; ... the reason ({REASON}) is printed beside them.")
M_ = lambda *mids: json.dumps([sorted(mids), []])  # noqa: E731  (the a_cert syn form: [pos MIDs, neg MIDs])
SYN = {"a": M_("/m/a"), "b": M_("/m/b"), "c": M_("/m/c"), "d": M_("/m/c"), "e": M_("/m/a", "/m/e"),
       "f": M_("/m/c"), "g": M_("/m/a", "/m/e")}
KEEP = ("n", "n_YN_both", "agree", "agreement")


def fixture():
    """a_cert_e3 _mini_labels plus base part-1 targets (i,x) N, (j,y) Y, (j,z) A, (i,f) Y, (j,g) N; top-up old_repeat
    (i,x) Y, (j,y) N, (j,z) Y and ctrl_present (i,a) Y. Old repeats (top-up / base last line):
      i: (i,c) Y/Y agree, (i,x) Y/N disagree;  j: (j,d) U/N, (j,y) N/Y disagree, (j,z) Y/A.
      (i) all: n 5, Y/N both 3, agree 1 (1/3).  Without i: n 3, both 1, agree 0 (0.0).  Without j: n 2, both 2, agree 1.
    Same-map (SYN): d~c~f (/m/c), g == e, e shares /m/a with a. Top-up targets (i,d), (i,e), (j,u); (j,e) is a
    control. CC-480 J-1 count: listed {i,j} or {i} -> 1 ((i,d) with c, f); {j} -> 0 ((j,e) is not a target; (j,u) has
    no map); an added target (i,x), x unmapped and itself a base class on i, adds 0."""
    b0 = [("i", "c", 1, "target"), ("j", "d", 1, "target"), ("i", "a", 1, "ctrl_present"), ("i", "c", 3, "repeat"),
          ("i", "x", 1, "target"), ("j", "y", 1, "target"), ("j", "z", 1, "target"), ("i", "f", 1, "target"),
          ("j", "g", 1, "target")]
    l0 = [("i", "c", 1, "N"), ("i", "c", 1, "Y"), ("j", "d", 1, "N"), ("i", "a", 1, "Y"), ("i", "c", 3, "Y"),
          ("i", "x", 1, "N"), ("j", "y", 1, "Y"), ("j", "z", 1, "A"), ("i", "f", 1, "Y"), ("j", "g", 1, "N")]
    b1 = [("i", "d", 1, "target", "Y"), ("i", "e", 1, "target", "U"), ("j", "e", 1, "ctrl_absent", "N"),
          ("i", "c", 1, "old_repeat", "Y"), ("j", "d", 1, "old_repeat", "U"), ("j", "u", 2, "target", "Y"),
          ("i", "d", 3, "repeat", "Y"), ("i", "x", 1, "old_repeat", "Y"), ("j", "y", 1, "old_repeat", "N"),
          ("j", "z", 1, "old_repeat", "Y"), ("i", "a", 1, "ctrl_present", "Y")]
    k0 = {q_("", p, i, c): {"image": i, "class": c, "part": p, "role": r} for i, c, p, r in b0}
    k1 = {q_("topup1|", p, i, c): {"image": i, "class": c, "part": p, "role": r} for i, c, p, r, _ in b1}
    lab0 = [json.dumps({"qid": q_("", p, i, c), "label": x}) for i, c, p, x in l0]
    lab1 = [json.dumps({"qid": q_("topup1|", p, i, c), "label": x}) for i, c, p, _, x in b1]
    return k0, lab0, k1, lab1


def quiet(fn):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = fn()
    return rc, buf.getvalue()


def setup() -> dict:
    """Mini world with SYN; FREEZE_E3 written and read back; the registered result written by a_cert_e3.e3_score."""
    tmp = Path(tempfile.mkdtemp(prefix="a_e6_split_test_"))
    m12, mp = E._mini(A.test_mods(), tmp)
    W = {**E.e_world(m12, mp, E._oi_fake), "syn": SYN}
    fzp = tmp / "fz" / "FREEZE_E3.json"
    A.write_atomic(fzp, E.freeze_e3_core(W))
    k0, lab0, k1, lab1 = fixture()
    ldir = tmp / "vsps_labels"
    files = {"labels": ldir / "xm600_gold" / "labels_PI.copy.jsonl", "key": ldir / "xm600_gold" / "key.json",
             "topup_labels": ldir / "xm600_gold_topup1" / "labels_PI.copy.jsonl",
             "topup_key": ldir / "xm600_gold_topup1" / "key.json"}
    data = {"labels": "\n".join(lab0) + "\n", "key": json.dumps(k0), "topup_labels": "\n".join(lab1) + "\n",
            "topup_key": json.dumps(k1)}
    A._LABEL_OK.update(str(p) for p in files.values())
    for k, p in files.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(data[k], encoding="utf-8")
    A._LABEL_OK.clear()
    hs = {k: hashlib.sha256(x.encode("utf-8")).hexdigest() for k, x in data.items()}
    r1p = tmp / "A_CERT_RESULT.json"
    r1p.write_text(json.dumps({"provenance": {"labels_sha256": hs["labels"], "key_sha256": hs["key"]}}), encoding="utf-8")
    log = [f"x FREEZE_E3.json sha256 {A.sha(fzp)}", f"x A_CERT_RESULT.json sha256 {A.sha(r1p)}",
           f"x topup1 key.json {hs['topup_key']}", f"x topup1 session-end labels {hs['topup_labels']}"]
    logp = tmp / "LOG.md"
    logp.write_text("\n".join(log) + "\n", encoding="utf-8")
    P = {"freeze": str(fzp), "part1": str(r1p), "log": str(logp), "result": str(tmp / "score" / "RESULT.json"),
         "part1_n": sum(k["part"] == 1 for k in k0.values())}
    arg = {**{k: str(p) for k, p in files.items()}, "labels_sha": hs["labels"], "topup_labels_sha": hs["topup_labels"]}
    rc, _ = quiet(lambda: E.e3_score(arg, P, lambda: W))
    if rc != 0:
        raise SystemExit("setup: the registered e3-score on the fixture failed")
    log.append(f"x OPS-e3-score-end | wrote A_CERT_E3_RESULT.json sha256 {A.sha(P['result'])}")
    ovl = {}
    for name, txt in (("i", "i\n"), ("j", "j\n"), ("zz", "zz\n")):
        ovl[name] = tmp / f"overlap_{name}.txt"
        ovl[name].write_text(txt, encoding="utf-8")
    P.update(overlap=str(ovl["i"]), overlap_sha=A.sha(ovl["i"]), overlap_n=1)
    R3 = json.loads(Path(P["result"]).read_text(encoding="utf-8"))
    bad = json.loads(json.dumps(R3))
    bad["E6"]["old_repeat"]["agree"] += 1
    badp = tmp / "RESULT_tampered.json"
    badp.write_text(json.dumps(bad), encoding="utf-8")
    return {"tmp": tmp, "ldir": ldir, "W": W, "FZ": json.loads(fzp.read_text(encoding="utf-8")), "k0": k0, "k1": k1,
            "a0": A.answers(lab0), "a1": A.answers(lab1), "R3": R3, "bad": bad, "badp": badp, "P": P, "arg": arg,
            "log": log + [REG_LINE], "logp": logp, "ovl": ovl, "n": 0, "qids": list(k0) + list(k1)}


def checks(m, env: dict) -> tuple[dict, dict]:
    ck, err = {}, {}
    W, FZ, k0, k1, a0, a1, R3 = (env[x] for x in ("W", "FZ", "k0", "k1", "a0", "a1", "R3"))
    core = lambda listed, res3=R3: m.split_rows(W, FZ, k0, a0, k1, a1, listed, res3)  # noqa: E731
    keep = lambda d: {x: d[x] for x in KEEP}  # noqa: E731
    i_ = {"n": 5, "n_YN_both": 3, "agree": 1, "agreement": 1 / 3}

    def faults(fn):  # True for a Fault, False for no exception; any other exception propagates (recorded, no kill)
        try:
            fn()
            return False
        except Fault:
            return True

    def e2e(lines=None, **over):
        env["n"] += 1
        P = {**env["P"], "split": str(env["tmp"] / f"split_{env['n']}" / "SPLIT.json"), **over}
        env["logp"].write_text("\n".join(env["log"] if lines is None else lines) + "\n", encoding="utf-8")
        rc, so = quiet(lambda: m.split(env["arg"], P, lambda: W))
        out = Path(P["split"])
        return rc, so, out.exists(), P

    nf = (2, "FAULT Fault\n", False)

    def valid():
        rc, so, ex, P = e2e()
        if not (rc == 0 and ex):
            return False
        txt = Path(P["split"]).read_text(encoding="utf-8")
        out = json.loads(txt)
        return set(json.loads(so)) == {"wrote", "sha256"} and json.loads(so)["sha256"] == A.sha(P["split"]) and \
            set(out) == {"schema", "registration", "reason", "verdict", "note", "row_label", "E6_i", "E6_ii",
                         "counts_iii", "provenance", "split_provenance"} and \
            out["E6_i"] == {"label": m.LABEL["i"], **i_} and \
            out["E6_ii"] == {"label": m.LABEL["ii"], "n": 3, "n_YN_both": 1, "agree": 0, "agreement": 0.0} and \
            "4f971966" in out["E6_ii"]["label"] and out["reason"] == REASON and out["verdict"] is None and \
            out["counts_iii"]["old_repeat_on_listed_images"] == 2 and out["counts_iii"]["same_map_pairs"] == 1 and \
            out["split_provenance"]["a_cert_e3_result_sha256"] == A.sha(env["P"]["result"]) and \
            not any(q in txt for q in env["qids"])

    def twice():
        rc, so, ex, P = e2e()
        before = Path(P["split"]).read_text(encoding="utf-8") if ex else None
        rc2, so2 = quiet(lambda: m.split(env["arg"], P, lambda: W))
        return rc == 0 and (rc2, so2) == (2, "FAULT Fault\n") and Path(P["split"]).read_text(encoding="utf-8") == before

    ovl = env["ovl"]
    tests = {
        # (ii) and (iii) by hand through split_rows
        "ii_by_hand_without_image_i": lambda: (r := core({"i"})) and keep(r["E6_i"]) == i_ and keep(r["E6_ii"]) == {
            "n": 3, "n_YN_both": 1, "agree": 0, "agreement": 0.0} and r["counts_iii"]["old_repeat_on_listed_images"] == 2,
        "ii_by_hand_without_image_j": lambda: (r := core({"j"})) and keep(r["E6_ii"]) == {
            "n": 2, "n_YN_both": 2, "agree": 1, "agreement": 0.5} and r["counts_iii"]["old_repeat_on_listed_images"] == 3,
        "ii_equals_i_on_an_empty_list": lambda: (r := core(set())) and keep(r["E6_ii"]) == i_ and
            r["counts_iii"]["old_repeat_on_listed_images"] == 0,
        "split_rows_no_fault_on_valid_input": lambda: faults(lambda: core({"i"})) is False,
        "fault_if_recompute_differs_from_registered_result": lambda: faults(lambda: core({"i"}, env["bad"])),
        "fault_if_a_listed_image_is_not_in_the_world": lambda: faults(lambda: core({"zz"})),
        "same_map_by_hand_listed_ij": lambda: m.same_map(k0, k1, SYN, {"i", "j"}) == 1,
        "same_map_by_hand_listed_i": lambda: m.same_map(k0, k1, SYN, {"i"}) == 1,
        "same_map_by_hand_listed_j": lambda: m.same_map(k0, k1, SYN, {"j"}) == 0,
        "same_map_skips_the_identical_class": lambda: m.same_map(k0, {**k1, "qx": {
            "image": "i", "class": "x", "part": 1, "role": "target"}}, SYN, {"i"}) == 1,
        # split mode end to end: one write, refusals, fault rule
        "e2e_valid_run_writes_counts_only": valid,
        "e2e_refuses_if_output_exists": twice,
        "e2e_refuses_without_REG_line": lambda: e2e(env["log"][:-1])[:3] == nf,
        "e2e_refuses_REG_line_without_the_reason": lambda: e2e(env["log"][:-1] + [REG_LINE.replace(REASON, "")])[:3]
        == nf,
        "e2e_refuses_without_E3_result_pin_line": lambda: e2e(env["log"][:4] + env["log"][5:])[:3] == nf,
        "e2e_refuses_wrong_overlap_sha": lambda: e2e(overlap_sha="0" * 64)[:3] == nf,
        "e2e_refuses_overlap_count_not_registered": lambda: e2e(overlap_n=2)[:3] == nf,
        "e2e_refuses_overlap_id_not_in_world": lambda: e2e(overlap=str(ovl["zz"]), overlap_sha=A.sha(ovl["zz"]))[:3]
        == nf,
        "e2e_refuses_tampered_registered_result": lambda: e2e(env["log"] + [
            f"x A_CERT_E3_RESULT.json sha256 {A.sha(env['badp'])}"], result=str(env["badp"]))[:3] == nf,
        "e2e_fault_rule_exception_writes_nothing": lambda: (lambda r: (r[0], r[1], r[2]) == (
            2, "FAULT ZeroDivisionError\n", False))(quiet_split(m, env, lambda: 1 / 0)),
        "score_core_restored_after_split": lambda: E.score_e3_core is E_ORIG,
    }
    for name, fn in tests.items():
        try:
            ck[name] = bool(fn())
        except Exception as e:  # noqa: BLE001  (recorded; never a kill)
            ck[name], err[name] = None, f"{type(e).__name__}: {str(e)[:80]}"
    return ck, err


def quiet_split(m, env, wfn):
    env["n"] += 1
    P = {**env["P"], "split": str(env["tmp"] / f"split_{env['n']}" / "SPLIT.json")}
    env["logp"].write_text("\n".join(env["log"]) + "\n", encoding="utf-8")
    rc, so = quiet(lambda: m.split(env["arg"], P, wfn))
    return rc, so, Path(P["split"]).exists()


def load(text: str):
    ns = {"__name__": "a_e6_split_under_test", "__file__": str(SRC)}
    exec(compile(text, str(SRC), "exec"), ns)  # noqa: S102  (the module under test or one named mutant of it)
    return types.SimpleNamespace(**ns)


# name: ([(old, new), ...], [named checks of which at least one must be False])
MUTANTS = {
    "M01_membership_inverted": ([('k["role"] == "old_repeat" and k["image"] in listed}',
                                  'k["role"] == "old_repeat" and k["image"] not in listed}')],
                                ["ii_by_hand_without_image_i", "ii_equals_i_on_an_empty_list"]),
    "M02_no_restriction": ([('if k["role"] == "old_repeat" and k["image"] in listed}', "if False}")],
                           ["ii_by_hand_without_image_i", "ii_by_hand_without_image_j"]),
    "M03_listed_targets_dropped_too": ([('if k["role"] == "old_repeat" and k["image"] in listed}',
                                         'if k["image"] in listed}')], ["split_rows_no_fault_on_valid_input"]),
    "M04_overlap_pin_dropped": ([('        if hashlib.sha256(ob).hexdigest() != P["overlap_sha"]:\n'
                                  '            raise Fault("overlap_images.txt differs from its pin")\n', "")],
                                ["e2e_refuses_wrong_overlap_sha"]),
    "M05_overlap_count_guard_dropped": ([('len(listed) != P["overlap_n"] or ', "")],
                                        ["e2e_refuses_overlap_count_not_registered"]),
    "M06_world_id_guard_dropped": ([('    if not listed <= set(w["ids"]):\n'
                                     '        raise Fault("an overlap image is not an I600 id")\n', "")],
                                   ["fault_if_a_listed_image_is_not_in_the_world", "e2e_refuses_overlap_id_not_in_world"]),
    "M07_registered_result_not_compared": ([('    if canon(full["E6"]) != canon(res3["E6"]):', "    if False:")],
                                           ["fault_if_recompute_differs_from_registered_result",
                                            "e2e_refuses_tampered_registered_result"]),
    "M08_same_map_by_class_name": ([("b != c and syn.get(b, b) == syn.get(c, c)", "b != c and b == c")],
                                   ["same_map_by_hand_listed_ij"]),
    "M09_same_map_counts_the_identical_class": ([("any(b != c and syn.get(b, b)", "any(syn.get(b, b)")],
                                                ["same_map_skips_the_identical_class"]),
    "M10_same_map_counts_non_target_roles": ([('if k["role"] == "target" and k["image"] in listed}',
                                               'if k["role"] != "old_repeat" and k["image"] in listed}')],
                                             ["same_map_by_hand_listed_j"]),
    "M11_output_leaks_full_E6_block": ([("pick = lambda b: {x: b[x] for x in KEEP}", "pick = lambda b: dict(b)")],
                                       ["e2e_valid_run_writes_counts_only"]),
    "M12_REG_line_not_required": ([("        if not any(REG_ID in ln and REASON in ln for ln in E.log_lines(P)):\n"
                                    '            raise Fault("no REG-1119a line")\n', "")],
                                  ["e2e_refuses_without_REG_line", "e2e_refuses_REG_line_without_the_reason"]),
    "M13_E3_result_pin_not_required": ([('res3, r3sha = E.pinned(P, "result", "A_CERT_E3_RESULT")',
                                         'res3 = json.loads((ROOT / P["result"]).read_text(encoding="utf-8")); '
                                         'r3sha = A.sha(ROOT / P["result"])')],
                                       ["e2e_refuses_without_E3_result_pin_line"]),
    "M14_core_not_restored": ([("    finally:\n        E.score_e3_core = ORIG\n", "    finally:\n        pass\n")],
                              ["score_core_restored_after_split"]),
}


def run_checks(text: str, env: dict) -> tuple[dict, dict]:
    try:
        return checks(load(text), env)
    finally:
        E.score_e3_core = E_ORIG  # a mutant may leave the wrapper installed; the next run starts clean


def main(argv: list) -> int:
    if len(argv) != 3 or argv[0] not in ("selftest", "mutants") or argv[1] != "--out":
        raise SystemExit("usage: test_a_e6_split.py selftest|mutants --out F")
    sys.addaudithook(E._audit)  # the custody guard of a_cert_e3 is live for the whole test
    env = setup()
    src = SRC.read_text(encoding="utf-8")
    try:
        ck, err = run_checks(src, env)
        rec = {"schema": "vsps.a_e6_split.selftest.v1", "split_sha256": A.sha(SRC), "a_cert_e3_sha256": A.sha(E.__file__),
               "checks": ck, "errors": err, "n": len(ck), "pass": all(x is True for x in ck.values())}
        print("\n".join(f"{'ok  ' if x is True else 'FAIL'} {k}" for k, x in ck.items()))
        print("selftest ok" if rec["pass"] else "selftest FAILED")
        if argv[0] == "mutants":
            res = {}
            for name, (reps, named) in MUTANTS.items():
                text = src
                for old, new in reps:
                    if text.count(old) != 1:
                        raise SystemExit(f"mutant {name}: target occurs {text.count(old)} times")
                    text = text.replace(old, new)
                mk, me = run_checks(text, env)
                killed = any(mk.get(x) is False for x in named)
                res[name] = {"killed": killed, "named_false": [x for x in named if mk.get(x) is False], "errors": me}
                print(f"{'KILLED  ' if killed else 'SURVIVED'} {name}")
            nk = sum(r["killed"] for r in res.values())
            print(f"{nk}/{len(res)} killed")
            rec = {**rec, "schema": "vsps.a_e6_split.mutants.v1", "mutants": res, "killed": nk,
                   "pass": rec["pass"] and nk == len(res)}
        Path(argv[2]).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
        return 0 if rec["pass"] else 1
    finally:
        os.rename(env["ldir"], env["tmp"] / "lbl_done")  # the guard lets rmtree walk the renamed dir
        shutil.rmtree(env["tmp"])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
