#!/usr/bin/env python3
"""Paper A, XM3600-600 object gold: agreement of the second annotator (R2) with the first (PI). Stdlib only.
Spec: plan manuscript/prereg/2026-11-11_xm600_gold_completion/XM600_GOLD_COMPLETION_PLAN_v1_1.md (8ad28f67) §4 l.37
(statistic) and l.38 (0.60 rule); CC-367 (f37090f5) 7(c), 1(b); CC-372 (d8eb3d84) rulings 1-6 and fixes B1-B6, N1-N5.
Label rows are server.py's (e3beb936) l.82-86: qid, label in Y/N/U/A, annotator, t_server, ms_on_screen; append-only,
the last line of a qid wins (l.4-6; plan §3 l.30).

  selftest --out F    synthetic fixtures in a temp dir only; prints every check and 'N checks; selftest ok' / FAILED
  score --labels-pi1 L1 --labels-pi1-sha H1 --labels-pi2 L2 --labels-pi2-sha H2 --labels-r2 L3 --labels-r2-sha H3
        --key K --assignment B --assignment-r2 R --out D
      L1 = the PI's scored 444 copy (sha = PI1_SHA, CC-372 2(a)): the PI's part-1 answers come from L1 only.
      L2 = the PI's 444 copy of the L-e line; it must start with the L1 bytes; part-2 answers = last line over all L2;
           part-1 lines after the L1 prefix are ignored and counted (2(b)-(d)).
      L3 = R2's 444 copy of the L-g line (2(e)). K = ~/vsps_labels/xm600_gold/key.json, sha = KEY_SHA (CC-372 ruling 1):
           the script reads it once, before any label byte, and keeps only (part, role) of the R2 qids.
      Order (2(g)): out / argument / pin checks -> assignments -> key -> strata -> label bytes -> completeness (ruling 4)
      -> statistics in memory -> one write of D/KAPPA_RESULT.json via a sibling temp dir (N1). On any fault it prints
      `FAULT <type> <label-free|after-labels>` only (N4) and leaves no D.
Nothing per question is printed or written: no qid, image, class, bucket, named_by or role (CC-372 1(e)).
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import re
import shutil
import sys
import tempfile
from fractions import Fraction as Fr
from pathlib import Path

PLAN = "manuscript/prereg/2026-11-11_xm600_gold_completion/XM600_GOLD_COMPLETION_PLAN_v1_1.md"
P_REAL = {"assign_sha": "55e07337218acc820aafc27659e499ade4ae622cc6eaf41be2f7bb3df510cb2d",
          "r2_sha": "fc8aafe9600bf9b1977629432b60c4ffc3a22c9677454b6ea665c421574d21ff",
          "key_sha": "a2cef89475675b66867577d399d7050ccf2925abc7a0b04f9572718a85a1c73a",  # KEY_SHA: plan §8, a_cert.py l.48
          "pi1_sha": "ba362466ebd9c50918076dcf5865fbac9c5cd6482288f4251fa1f76e0f2718b4",  # PI1_SHA: OPS-1113q, CC-372 2(a)
          # plan l.37 (457 part-1 targets); BUILD_OVERLAP.json 10588e86: part 1 557, part 2 511, part 3 42 questions
          "n": {"p1_target": 457, "p1_control": 100, "p2_target": 511, "p3_repeat": 42}}
ROLES = {1: {"target", "ctrl_absent", "ctrl_present", "foil_absent"}, 2: {"target"}, 3: {"repeat"}}  # build_assignment l.121-124
ANNOT = ("PI", "R2")
LABELS = {"Y", "N", "U", "A"}
YN = ("Y", "N")
THRESHOLD = Fr(3, 5)  # plan §4 l.38: "Kappa at or above 0.60"
STAT_STRATA = ("p1_target", "p1_control", "p2_target")  # plan l.37; part 3 enters no statistic (CC-367 1(b))
GATED = ("p1_target", "p2_target")  # plan l.38: the part-1 target kappa; part 2 "gated the same way by the part-2 target kappa"
REGISTERED = {
    "statistic": "plan §4 l.37: Cohen's kappa on Y against N over the part-1 target questions of the overlap images "
                 "(457) that both answered Y or N; raw agreement and PABAK beside it; part-1 controls and part 2 "
                 "reported separately; the U and A rates of each annotator are reported beside it",
    "rule": "plan §4 l.38: Kappa at or above 0.60: the first annotator's labels are used as the completed gold and "
            "kappa is reported. Kappa below 0.60: label-based results are reported as a sensitivity analysis only, "
            "with the disagreement table. The 0.60 rule applies to the part-1 target kappa; part-2 results are gated "
            "the same way by the part-2 target kappa.",
    "scope": "CC-372 ruling 6: the agreement figures of plan §4 l.37 for parts 1 and 2; no part-2 P_c, H2 or H3",
    "part3": "CC-367 1(b): R2's part-3 answers enter no registered statistic; only the question count is given",
    "threshold": THRESHOLD}
RULE = {"GOLD": "kappa at or above 0.60: the first annotator's labels are used as the completed gold; kappa reported",
        "SENSITIVITY_ONLY": "kappa below 0.60: label-based results are a sensitivity analysis only, with the "
                            "disagreement table"}
RULE_UNDEFINED = ("kappa undefined (no Y/N pair, or p_e = 1): the 'below 0.60' consequence, sensitivity analysis only, "
                  "never gold (CC-372 ruling 3; default pending PI Q1)")
SCORE_ARGS = ("--labels-pi1", "--labels-pi1-sha", "--labels-pi2", "--labels-pi2-sha", "--labels-r2", "--labels-r2-sha",
              "--key", "--assignment", "--assignment-r2", "--out")
DENY = ("/vsps_labels", "/.vsps_sealed", "/bpa1pull_1108", "/data/results/a_cert_e3", "/data/results/a_e3",
        "gt_cache.json", "/.session_backup/machines/hbt1", "/a1_precheck/raw")
_OK: set[str] = set()


class Fault(Exception):
    pass


# ------------------------------------------------------------------------------------------------ custody
def refused(path) -> bool:
    """key.json, any labels_*/practice_*.jsonl and the sealed paths, except the files `score` is reading right now."""
    p = os.path.abspath(os.fsdecode(path))
    if p in _OK:
        return False
    b, low = os.path.basename(p), p.replace(os.sep, "/").lower()
    return b == "key.json" or bool(re.fullmatch(r"(labels|practice)_.*\.jsonl", b)) or any(d in low for d in DENY)


def _audit(event: str, args) -> None:
    if event in ("open", "os.listdir", "os.scandir") and args and \
            isinstance(args[0], (str, bytes, os.PathLike)) and refused(args[0]):
        raise Fault(f"custody: {event} refused")


def hx(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ------------------------------------------------------------------------------------------------ statistics
def answers(lines, who: str) -> dict:
    """qid -> answer; the last line of a qid wins (server.py l.4-6)."""
    out = {}
    for ln in lines:
        if ln.strip():
            r = json.loads(ln)
            if r.get("annotator") != who or r.get("label") not in LABELS:
                raise Fault("label row: wrong annotator or label")
            out[r["qid"]] = r["label"]
    return out


def stats(yy: int, yn: int, ny: int, nn: int) -> dict:
    """2x2 on the questions both answered Y or N (first letter PI, second R2). Kappa is None when p_e = 1 or n = 0."""
    n = yy + yn + ny + nn
    if n == 0:
        return {"n_both_YN": 0, "raw_agreement": None, "kappa": None, "pabak": None}
    po = Fr(yy + nn, n)
    pe = Fr((yy + yn) * (yy + ny) + (ny + nn) * (yn + nn), n * n)
    kappa = None if pe == 1 else (po - pe) / (1 - pe)
    return {"n_both_YN": n, "raw_agreement": po, "kappa": kappa, "pabak": 2 * po - 1}


def agree(pairs: list) -> dict:
    yn = [a + b for a, b in pairs if a in YN and b in YN]
    t = {k: yn.count(k) for k in ("YY", "YN", "NY", "NN")}
    return {"table": t, **stats(t["YY"], t["YN"], t["NY"], t["NN"])}


def rater(ans: list) -> dict:
    """Counts of one annotator on one stratum; every question is answered (ruling 4), so rates are over all questions."""
    n = len(ans)
    c = {k: sum(a == k for a in ans) for k in ("Y", "N", "U", "A")}
    return {**c, "U_rate": Fr(c["U"], n) if n else None, "A_rate": Fr(c["A"], n) if n else None}


def gate(kappa) -> str:
    if kappa is None:
        return "SENSITIVITY_ONLY"  # CC-372 ruling 3 (default pending PI Q1)
    return "GOLD" if kappa >= THRESHOLD else "SENSITIVITY_ONLY"


def stratum_row(pairs: list, gated: bool) -> dict:
    row = agree(pairs)
    row["kappa_undefined"] = row["kappa"] is None
    row["per_rater"] = {ANNOT[i]: rater([p[i] for p in pairs]) for i in (0, 1)}
    if gated:
        row["gate"] = gate(row["kappa"])
        row["gate_rule"] = RULE_UNDEFINED if row["kappa_undefined"] else RULE[row["gate"]]
    return row


# ------------------------------------------------------------------------------------------------ strata and score
def strata(bpart: dict, r2a: dict, kmap: dict, P: dict) -> dict:
    """qid -> stratum for the R2 qids: public screen part, checked against the key's (part, role) (CC-372 1(d))."""
    out = {}
    for s in r2a["screens"]:
        for q in s["q"]:
            qid = q["qid"]
            if bpart.get(qid) != s["part"]:
                raise Fault("R2 question not in the base assignment with the same part")
            if qid not in kmap:
                raise Fault("R2 question not in the key")
            part, role = kmap[qid]
            if part != s["part"]:
                raise Fault("key part differs from the screen part")
            if role not in ROLES[part]:
                raise Fault("key role outside its part's set")
            out[qid] = {1: "p1_target" if role == "target" else "p1_control", 2: "p2_target", 3: "p3_repeat"}[part]
    n = {k: sum(v == k for v in out.values()) for k in P["n"]}
    if n != P["n"]:
        raise Fault("stratum sizes differ from the registered counts")
    return out


def score(a: dict, P: dict = P_REAL, seen: dict | None = None) -> dict:
    seen = {} if seen is None else seen
    if Path(a["out"]).exists():
        raise Fault("--out exists")
    shas = [a["labels_pi1_sha"], a["labels_pi2_sha"], a["labels_r2_sha"]]
    if not all(re.fullmatch(r"[0-9a-f]{64}", h) for h in shas):
        raise Fault("label sha argument is not 64 hex")
    if len(set(shas)) != 3:
        raise Fault("the three label sha arguments are not distinct")
    if a["labels_pi1_sha"] != P["pi1_sha"]:
        raise Fault("--labels-pi1-sha is not PI1_SHA")
    ab, rb = Path(a["assignment"]).read_bytes(), Path(a["assignment_r2"]).read_bytes()
    if (hx(ab), hx(rb)) != (P["assign_sha"], P["r2_sha"]):
        raise Fault("assignment differs from its pin")
    base, r2a = json.loads(ab.decode("utf-8")), json.loads(rb.decode("utf-8"))
    bpart = {q["qid"]: s["part"] for s in base["screens"] for q in s["q"]}
    r2q = {q["qid"] for s in r2a["screens"] for q in s["q"]}
    files = [os.path.abspath(a[k]) for k in ("key", "labels_pi1", "labels_pi2", "labels_r2")]
    try:
        _OK.add(files[0])
        kb = Path(files[0]).read_bytes()  # read once; the same bytes are hashed and parsed
        ksha = hx(kb)
        if ksha != P["key_sha"]:
            raise Fault("key.json sha is not KEY_SHA")
        kmap = {q: (k["part"], k["role"]) for q, k in json.loads(kb.decode("utf-8")).items() if q in r2q}  # part, role only
        st = strata(bpart, r2a, kmap, P)
        _OK.update(files[1:])
        seen["labels"] = True
        l1, l2, l3 = (Path(f).read_bytes() for f in files[1:])
    finally:
        _OK.clear()
    if (hx(l1), hx(l2), hx(l3)) != tuple(shas):
        raise Fault("label file sha differs from its argument")
    if not l2.startswith(l1):
        raise Fault("--labels-pi2 does not extend --labels-pi1")
    pi1, pi2 = answers(l1.decode("utf-8").splitlines(), ANNOT[0]), answers(l2.decode("utf-8").splitlines(), ANNOT[0])
    r2 = answers(l3.decode("utf-8").splitlines(), ANNOT[1])
    if not set(pi2) <= bpart.keys():  # L2 holds every L1 line, so this covers L1 too
        raise Fault("PI qid not in the base assignment")
    if not set(r2) <= r2q:
        raise Fault("R2 qid not in the R2 assignment")
    p1q = {q for q, v in st.items() if v.startswith("p1_")}
    p2q = {q for q, v in st.items() if v == "p2_target"}
    if not p1q <= pi1.keys():
        raise Fault("PI part 1 not complete")
    if not p2q <= pi2.keys():
        raise Fault("PI part 2 not complete")
    if not (p1q | p2q) <= r2.keys():
        raise Fault("R2 not complete")
    tail = [json.loads(ln)["qid"] for ln in l2[len(l1):].decode("utf-8").splitlines() if ln.strip()]
    late = [q for q in tail if bpart[q] == 1]  # part from the public base assignment, never from the key (2(c))
    res = {"schema": "vsps.a_cert_kappa.result.v2", "registered": REGISTERED, "strata": {},
           "pi_part1_lines_after_index": {"all_part1": len(late), "overlap_part1": sum(q in st for q in late)},
           "pi_part2_overlap_final_after_index": len({q for q in tail if st.get(q) == "p2_target"})}
    for s in P["n"]:
        qs = sorted(q for q, v in st.items() if v == s)
        row = {"n_questions": len(qs)}
        if s in STAT_STRATA:
            src = pi1 if s.startswith("p1_") else pi2  # PI part 1 from L1 only (2(a)); part 2 from all of L2 (2(b))
            row.update(stratum_row([(src[q], r2[q]) for q in qs], s in GATED))
        res["strata"][s] = row
    res["provenance"] = {"labels_pi1_sha256": hx(l1), "labels_pi2_sha256": hx(l2), "labels_r2_sha256": hx(l3),
                         "key_sha256": ksha, "assignment_sha256": hx(ab), "assignment_r2_sha256": hx(rb),
                         "code_sha256": hx(Path(__file__).read_bytes()), "plan": PLAN, "ruling": "CC-372"}
    return res


def dump(res: dict) -> str:
    return json.dumps(res, indent=1, ensure_ascii=False, default=lambda f: {"exact": str(f), "value": float(f)}) + "\n"


def write_result(out: Path, body: str) -> None:
    """Write into a sibling temp dir, then rename it to `out`; on any fault the temp dir is removed (N1)."""
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(dir=out.parent, prefix=".tmp_kappa_"))
    try:
        (tmp / "KAPPA_RESULT.json").write_text(body, encoding="utf-8")
        os.rename(tmp, out)
    except BaseException:
        shutil.rmtree(tmp, ignore_errors=True)
        raise


def run_score(a: dict, P: dict = P_REAL) -> int:
    seen = {"labels": False}
    try:
        body = dump(score(a, P, seen))  # serialised before anything is created
        write_result(Path(a["out"]), body)
    except BaseException as e:  # noqa: BLE001  (fault rule: exception type and stage only)
        print(f"FAULT {type(e).__name__} {'after-labels' if seen['labels'] else 'label-free'}")
        return 2
    print(json.dumps({"wrote": str(Path(a["out"]) / "KAPPA_RESULT.json"), "sha256": hx(body.encode("utf-8"))}))
    return 0


# ------------------------------------------------------------------------------------------------ selftest
def selftest(out: Path) -> int:
    ck = {}
    try:
        _checks(ck)
    except BaseException as e:  # noqa: BLE001  (recorded; the mutant harness never counts it as a kill)
        ck[f"no_exception ({type(e).__name__}: {str(e)[:80]})"] = False
    ck = {k: bool(x) for k, x in ck.items()}
    rec = {"schema": "vsps.a_cert_kappa.selftest.v2", "script_sha256": hx(Path(__file__).read_bytes()),
           "checks": ck, "n": len(ck), "pass": all(ck.values())}
    Path(out).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print("\n".join(f"{'ok  ' if x else 'FAIL'} {k}" for k, x in ck.items()))
    print(f"{len(ck)} checks; " + ("selftest ok" if rec["pass"] else "selftest FAILED"))
    return 0 if rec["pass"] else 1


def _raises(fn, word: str) -> bool:
    """True only for a Fault whose message holds `word`; any other exception or none is False."""
    try:
        fn()
    except Fault as e:
        return word in str(e)
    except Exception:  # noqa: BLE001
        return False
    return False


def _try(fn):
    try:
        return fn()
    except Exception:  # noqa: BLE001
        return None


def _out(fn) -> tuple:
    """(return value or None, stdout) of fn."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = _try(fn)
    return rc, buf.getvalue()


T = [f"t{i:02d}" for i in range(1, 14)]  # part-1 targets of the overlap images
C = {"c1": "ctrl_present", "c2": "ctrl_absent", "c3": "foil_absent"}  # part-1 controls, one of each control role
S = [f"s{i:02d}" for i in range(1, 11)]  # part-2 targets
# (qid, answer[, annotator]) in file order; a second entry for a qid is a re-answer (the last one wins).
PI1 = [*((q, "Y") for q in T[:8]), ("t09", "Y"), ("t09", "N"), ("t10", "N"), ("t11", "U"), ("t12", "N"), ("t13", "Y"),
       *((q, "Y") for q in C), ("z1", "Y"), ("s01", "N"), ("s02", "N"), ("s09", "N"), ("s10", "N"), ("z2", "A")]
TAIL = [("t01", "N"), ("c1", "N"), ("z1", "N"), ("s01", "N"), ("s01", "Y"), ("s02", "Y"), ("s03", "Y"), ("s04", "Y"),
        ("s05", "Y"), ("s06", "N"), ("s07", "N"), ("s08", "N"), ("r1", "Y"), ("r2", "N")]  # L2 = L1 + TAIL
R2 = [*((q, "Y") for q in T[:6]), ("t07", "Y"), ("t07", "N"), ("t08", "N"), ("t09", "N"), ("t10", "N"), ("t11", "Y"),
      ("t12", "A"), ("t13", "Y"), *((q, "Y") for q in C), *((q, "Y") for q in S[:4]), ("s05", "N"), ("s06", "Y"),
      *((q, "N") for q in S[6:]), ("r1", "N"), ("r2", "Y")]
SENT = "SENTINEL"  # every image/class/bucket/named_by of the fixture key holds it; it must never be printed or written


def _row(q: str, lab: str, who: str) -> str:
    return json.dumps({"qid": q, "label": lab, "annotator": who, "t_server": "2026-11-13T00:00:00Z", "ms_on_screen": 900})


def _lines(rows: list, who: str) -> str:
    return "".join(_row(r[0], r[1], r[2] if len(r) > 2 else who) + "\n" for r in rows)


def _base(extra_r2: bool = False) -> tuple[dict, dict]:
    def scr(part, img, qs):
        return {"sid": f"p{part}-{img}", "part": part, "image": f"images/{img}.jpg",
                "q": [{"qid": q, "label": "c", "hint": ""} for q in qs]}
    base = [scr(1, "o1", T[:7] + list(C)), scr(1, "o2", T[7:]), scr(1, "x1", ["z1"]), scr(2, "o1", S[:5]),
            scr(2, "o2", S[5:]), scr(2, "x1", ["z2"]), scr(3, "o1", ["r1"]), scr(3, "o2", ["r2"])]
    r2 = [s for s in base if s["image"] != "images/x1.jpg"] + ([scr(1, "o9", ["q_extra"])] if extra_r2 else [])
    return {"meta": {}, "screens": base}, {"meta": {}, "screens": r2}


def _key() -> dict:
    roles = {**{q: (1, "target") for q in T + ["z1"]}, **{q: (1, r) for q, r in C.items()},
             **{q: (2, "target") for q in S + ["z2"]}, "r1": (3, "repeat"), "r2": (3, "repeat")}
    return {q: {"image": f"{SENT}_img", "class": f"{SENT}_cls", "part": p, "role": r, "bucket": f"{SENT}_bkt",
                "named_by": [f"{SENT}_nb"]} for q, (p, r) in roles.items()}


def _world(d: Path, tag: str, pi1=PI1, tail=TAIL, r2=R2, key_fn=None, extra_r2=False, l2_head=None, **over):
    """Fixture files in d/tag (labels not named labels_*: the hook refuses those); returns (score args, P)."""
    w = d / tag
    w.mkdir()
    base, r2a = _base(extra_r2)
    key = _key()
    if key_fn:
        key_fn(key)
    l1 = _lines(pi1, "PI")
    files = {"base.json": json.dumps(base), "r2a.json": json.dumps(r2a), "key.json": json.dumps(key),
             "pi1.jsonl": l1, "pi2.jsonl": (l1 if l2_head is None else l2_head) + _lines(tail, "PI"),
             "r2.jsonl": _lines(r2, "R2")}
    for name, body in files.items():
        _OK.add(str(w / name))  # the fixture key is named key.json, so its writer is let through once
        (w / name).write_text(body, encoding="utf-8")
        _OK.discard(str(w / name))
    sh = {k: hx(v.encode("utf-8")) for k, v in files.items()}
    P = {"assign_sha": sh["base.json"], "r2_sha": sh["r2a.json"], "key_sha": sh["key.json"], "pi1_sha": sh["pi1.jsonl"],
         "n": {"p1_target": 13 + extra_r2, "p1_control": 3, "p2_target": 10, "p3_repeat": 2}}
    a = {"labels_pi1": str(w / "pi1.jsonl"), "labels_pi1_sha": sh["pi1.jsonl"], "labels_pi2": str(w / "pi2.jsonl"),
         "labels_pi2_sha": sh["pi2.jsonl"], "labels_r2": str(w / "r2.jsonl"), "labels_r2_sha": sh["r2.jsonl"],
         "key": str(w / "key.json"), "assignment": str(w / "base.json"), "assignment_r2": str(w / "r2a.json"),
         "out": str(w / "out")}
    for k, v in over.items():
        (P if k in P else a)[k] = v
    return a, P


def _checks(ck: dict) -> None:
    # --- the formulas, by hand (KAPPA_READ_PACKAGE.md §5)
    s = stats(4, 1, 1, 4)  # p_o 8/10, p_e (5*5 + 5*5)/100 = 1/2, kappa (4/5 - 1/2)/(1/2) = 3/5
    ck["kappa_4_1_1_4_is_exactly_3_5"] = (s["kappa"], s["raw_agreement"], s["pabak"]) == (Fr(3, 5), Fr(4, 5), Fr(3, 5))
    s = stats(6, 2, 0, 2)  # p_o 4/5, p_e (8*6 + 2*4)/100 = 14/25, kappa (6/25)/(11/25) = 6/11; PABAK 3/5
    ck["kappa_6_2_0_2_unequal_marginals_6_11_pabak_3_5"] = \
        (s["n_both_YN"], s["kappa"], s["raw_agreement"], s["pabak"]) == (10, Fr(6, 11), Fr(4, 5), Fr(3, 5))
    s = stats(3, 2, 0, 0)  # PI all Y, R2 mixed: p_o = p_e = 3/5, kappa 0 (defined)
    ck["kappa_one_rater_constant_is_0_defined"] = s["kappa"] == 0 and s["kappa"] is not None
    s = stats(5, 0, 0, 0)  # both all Y: p_e = 1
    ck["kappa_both_constant_same_answer_undefined"] = s["kappa"] is None and (s["raw_agreement"], s["pabak"]) == (1, 1)
    s = stats(0, 3, 0, 0)  # PI all Y, R2 all N: p_o 0, p_e 0
    ck["kappa_opposite_constants_0_pabak_minus_1"] = (s["kappa"], s["raw_agreement"], s["pabak"]) == (0, 0, -1)
    ck["kappa_no_YN_pair_all_undefined"] = stats(0, 0, 0, 0) == \
        {"n_both_YN": 0, "raw_agreement": None, "kappa": None, "pabak": None}
    ck["gate_at_or_above_3_5_below_and_undefined_sensitivity"] = \
        [gate(x) for x in (Fr(3, 5), Fr(7, 10), Fr(6, 11), None)] == ["GOLD", "GOLD", "SENSITIVITY_ONLY", "SENSITIVITY_ONLY"]
    u = stratum_row([("Y", "Y")] * 3, True)
    ck["undefined_row_sensitivity_kappa_null_flag_rule"] = (u["gate"], u["kappa"], u["kappa_undefined"], u["gate_rule"],
                                                             u["raw_agreement"]) == ("SENSITIVITY_ONLY", None, True,
                                                                                     RULE_UNDEFINED, 1)
    ck["answers_last_line_wins"] = answers([_row("q", "Y", "PI"), _row("q", "N", "PI"), "", _row("r", "U", "PI")],
                                           "PI") == {"q": "N", "r": "U"}
    ck["answers_wrong_annotator_is_fault"] = _raises(lambda: answers([_row("q", "Y", "R2")], "PI"), "annotator")
    ck["answers_label_outside_YNUA_is_fault"] = _raises(lambda: answers([_row("q", "X", "PI")], "PI"), "label")
    ck["rater_counts_and_rates"] = rater(["Y", "N", "U", "A"]) == \
        {"Y": 1, "N": 1, "U": 1, "A": 1, "U_rate": Fr(1, 4), "A_rate": Fr(1, 4)}

    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        a, P = _world(d, "w")
        res = _try(lambda: score(a, P))
        ck["ok_list_cleared_and_key_refused_after_score"] = not _OK and refused(a["key"])
        St = (res or {}).get("strata", {})
        t1, c1, p2 = St.get("p1_target", {}), St.get("p1_control", {}), St.get("p2_target", {})
        ck["world_p1_target_table_last_line_wins"] = t1.get("table") == {"YY": 7, "YN": 2, "NY": 0, "NN": 2}
        ck["world_p1_target_n_13_both_YN_11"] = (t1.get("n_questions"), t1.get("n_both_YN")) == (13, 11)
        ck["world_p1_target_kappa_14_25_raw_9_11_pabak_7_11"] = \
            (t1.get("kappa"), t1.get("raw_agreement"), t1.get("pabak")) == (Fr(14, 25), Fr(9, 11), Fr(7, 11))
        ck["world_p1_target_gate_on_kappa_not_pabak"] = (t1.get("gate"), t1.get("kappa_undefined")) == \
            ("SENSITIVITY_ONLY", False)
        ck["world_p1_target_UA_rates_per_rater"] = t1.get("per_rater") == {
            "PI": {"Y": 9, "N": 3, "U": 1, "A": 0, "U_rate": Fr(1, 13), "A_rate": Fr(0)},
            "R2": {"Y": 8, "N": 4, "U": 0, "A": 1, "U_rate": Fr(0), "A_rate": Fr(1, 13)}}
        ck["world_p1_control_three_roles_pooled_undefined_flag_no_gate"] = \
            (c1.get("n_questions"), c1.get("table"), c1.get("kappa"), c1.get("kappa_undefined"), c1.get("raw_agreement"),
             c1.get("pabak"), "gate" in c1) == (3, {"YY": 3, "YN": 0, "NY": 0, "NN": 0}, None, True, 1, 1, False)
        ck["world_p2_target_from_L2_kappa_3_5_gate_GOLD"] = \
            (p2.get("n_questions"), p2.get("table"), p2.get("kappa"), p2.get("gate")) == \
            (10, {"YY": 4, "YN": 1, "NY": 1, "NN": 4}, Fr(3, 5), "GOLD")
        ck["world_p3_repeat_count_only"] = St.get("p3_repeat") == {"n_questions": 2}
        ck["world_late_part1_lines_ignored_and_counted"] = \
            (res or {}).get("pi_part1_lines_after_index") == {"all_part1": 3, "overlap_part1": 2}
        ck["world_W1_part2_final_after_index_8"] = (res or {}).get("pi_part2_overlap_final_after_index") == 8
        ck["world_provenance"] = (res or {}).get("provenance", {}) == {
            "labels_pi1_sha256": a["labels_pi1_sha"], "labels_pi2_sha256": a["labels_pi2_sha"],
            "labels_r2_sha256": a["labels_r2_sha"], "key_sha256": P["key_sha"], "assignment_sha256": P["assign_sha"],
            "assignment_r2_sha256": P["r2_sha"], "code_sha256": hx(Path(__file__).read_bytes()), "plan": PLAN,
            "ruling": "CC-372"}
        rc, so = _out(lambda: run_score(a, P))
        f = Path(a["out"]) / "KAPPA_RESULT.json"
        body = f.read_text(encoding="utf-8") if f.is_file() else "{}"
        ck["run_score_writes_one_result_with_exact_values"] = rc == 0 and sorted(x.name for x in f.parent.iterdir()) == \
            ["KAPPA_RESULT.json"] and json.loads(body)["strata"]["p1_target"]["kappa"]["exact"] == "14/25" and \
            not [x for x in f.parent.parent.iterdir() if x.name.startswith(".tmp_kappa_")]
        ck["result_and_stdout_hold_no_qid_or_key_field"] = rc == 0 and not any(x in body or x in so for x in (
            SENT, "ctrl_", "foil_", '"qid')) and not any(x in body for x in ("t01", "t13", "s01", "z1"))  # stdout has a tmp path
        rc, so = _out(lambda: run_score(a, P))
        ck["second_run_refused_FAULT_type_label_free"] = rc == 2 and so == "FAULT Fault label-free\n"
        a2, P2 = _world(d, "f1")
        rc, so = _out(lambda: run_score({**a2, "labels_r2_sha": "0" * 64}, P2))
        ck["after_labels_fault_prints_stage_and_writes_nothing"] = rc == 2 and so == "FAULT Fault after-labels\n" and \
            not Path(a2["out"]).exists() and not [x for x in (d / "f1").iterdir() if x.name.startswith(".tmp_kappa_")]
        full = d / "f2"
        (full / "out").mkdir(parents=True)
        (full / "out" / "x").write_text("x", encoding="utf-8")
        ck["write_fault_leaves_no_temp_dir"] = _try(lambda: write_result(full / "out", "{}\n")) is None and \
            sorted(x.name for x in full.iterdir()) == ["out"]
        a2, _ = _world(d, "f3")
        argv = ["score"] + [x for k in SCORE_ARGS for x in (k, {**a2, "labels_pi1_sha": P_REAL["pi1_sha"],
                                                               "labels_pi2_sha": "1" * 64, "labels_r2_sha": "2" * 64}
                                                           [k[2:].replace("-", "_")])]
        rc, so = _out(lambda: main(argv))
        ck["main_maps_score_argv_to_a_label_free_pin_fault"] = rc == 2 and so == "FAULT Fault label-free\n"

        # --- refusals; the label-free ones get label paths that do not exist (so they must come before any read)
        gone = {"labels_pi1": str(d / "n1.jsonl"), "labels_pi2": str(d / "n2.jsonl"), "labels_r2": str(d / "n3.jsonl")}

        def refuses(tag, word, labels_gone=True, a_over=None, **kw):
            a2, P2 = _world(d, tag, **kw)
            return _raises(lambda: score({**a2, **(gone if labels_gone else {}), **(a_over or {})}, P2), word)

        ck["refuses_out_exists_before_labels"] = refuses("x01", "--out exists", a_over={"out": td})
        ck["refuses_sha_argument_not_64_hex"] = refuses("x02", "64 hex", labels_r2_sha="abc")
        ck["refuses_sha_arguments_not_distinct"] = refuses("x03", "not distinct", a_over={"labels_r2_sha": "1" * 64,
                                                                                         "labels_pi2_sha": "1" * 64})
        ck["refuses_pi1_sha_not_PI1_SHA_before_labels"] = refuses("x04", "PI1_SHA", labels_pi1_sha="3" * 64)
        ck["refuses_base_assignment_pin_before_labels"] = refuses("x05", "pin", assign_sha="0" * 64)
        ck["refuses_r2_assignment_pin_before_labels"] = refuses("x06", "pin", r2_sha="0" * 64)
        ck["refuses_key_sha_before_labels"] = refuses("x07", "KEY_SHA", key_sha="0" * 64)
        ck["refuses_r2_qid_not_in_key"] = refuses("x08", "not in the key", key_fn=lambda k: k.pop("t13"))
        ck["refuses_key_part_differs_from_screen_part"] = refuses("x09", "key part",
                                                                  key_fn=lambda k: k["t01"].update(part=2))
        ck["refuses_part1_role_outside_set"] = refuses("x10", "role outside", key_fn=lambda k: k["c1"].update(role="repeat"))
        ck["refuses_part2_role_not_target"] = refuses("x11", "role outside",
                                                      key_fn=lambda k: k["s01"].update(role="ctrl_absent"))
        ck["refuses_stratum_sizes_not_registered"] = refuses("x12", "registered counts", n={"p1_target": 457, "p1_control": 3,
                                                                                            "p2_target": 10, "p3_repeat": 2})
        ck["refuses_r2_question_not_in_base"] = refuses("x13", "same part", extra_r2=True)
        ck["refuses_label_sha_mismatch"] = refuses("x14", "label file sha", False, labels_r2_sha="0" * 64)
        ck["refuses_L2_not_extending_L1"] = refuses("x15", "does not extend", False,
                                                    l2_head=_lines([("t01", "N")] + PI1[1:], "PI"))
        ck["refuses_PI_qid_not_in_base"] = refuses("x16", "PI qid not in the base", False, tail=TAIL + [("zz", "Y")])
        ck["refuses_R2_qid_outside_R2_assignment"] = refuses("x17", "R2 qid not in", False, r2=R2 + [("z1", "Y")])
        ck["refuses_row_of_other_annotator_in_file"] = refuses("x18", "annotator", False, r2=R2 + [("t13", "Y", "PI")])
        ck["refuses_PI_part1_incomplete"] = refuses("x19", "PI part 1 not complete", False,
                                                    pi1=[r for r in PI1 if r[0] != "t13"])
        ck["refuses_PI_part2_incomplete"] = refuses("x20", "PI part 2 not complete", False,
                                                    tail=[r for r in TAIL if r[0] != "s05"])
        ck["refuses_R2_incomplete"] = refuses("x21", "R2 not complete", False, r2=[r for r in R2 if r[0] != "t13"])

        # --- custody hook (installed by main)
        ck["custody_refuses_key_label_and_sealed_paths"] = all(refused(x) for x in (
            d / "key.json", d / "labels_R2.jsonl", d / "labels_PI.20261112T181546Z.jsonl", d / "practice_R2.jsonl",
            "/home/u/vsps_labels/xm600_gold_r2/a.txt", "/home/u/vsps_labels_b/a.txt")) and not refused(d / "w" / "r2.jsonl")
        ck["custody_hook_blocks_open_of_key_json"] = _raises(lambda: open(d / "key.json", "w"), "custody")


def main(argv: list) -> int:
    if _audit not in getattr(main, "hooks", ()):
        sys.addaudithook(_audit)
        main.hooks = (_audit,)
    mode = argv[0] if argv else ""
    if mode == "selftest" and len(argv) == 3 and argv[1] == "--out":
        return selftest(Path(argv[2]))
    if mode == "score" and len(argv) == 1 + 2 * len(SCORE_ARGS) and tuple(argv[1::2]) == SCORE_ARGS:
        return run_score(dict(zip((x[2:].replace("-", "_") for x in SCORE_ARGS), argv[2::2])))
    raise SystemExit("usage: a_cert_kappa.py selftest --out F | score " + " ".join(f"{x} X" for x in SCORE_ARGS))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
