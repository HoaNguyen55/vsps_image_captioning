#!/usr/bin/env python3
"""Paper A: the registered E6 split (LOG REG-1119a-topup-e6-split; CC-457 ruling (2) T2: J1 B4, J2 B5, J3 W7).

  split --labels L --labels-sha H --key K --topup-labels T --topup-labels-sha H2 --topup-key K2
      Once, after the e3-score END line, with the same six arguments as that call. It runs a_cert_e3.e3_score
      unchanged (every refusal, the custody guard, the fault rule, one atomic write that refuses an existing file) on
      its own output path, with the scoring core wrapped: the wrapper runs a_cert_e3.score_e3_core twice, once on the
      full top-up key (its E6 must equal the stored A_CERT_E3_RESULT.json) and once without the old_repeat items whose
      image is listed in overlap_images.txt. It writes (i) and (ii) E6 old_repeat counts and agreement values and
      (iii) counts. No line of a_cert_e3.py or a_cert.py is copied or changed.
Outputs hold counts, the two E6 values, labels and sha256 only; FAULT <type> on any error, nothing written.
Tests: test_a_e6_split.py (synthetic; rented host only). The run licence is owed (RUN_NOTE_A_E6_SPLIT.md).
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "a_cert"))
import a_cert_e3 as E  # noqa: E402

A, Fault, ROOT = E.A, E.Fault, E.ROOT
SELF = "scripts/a_e3_e6split/a_e6_split.py"
REG_ID = "REG-1119a-topup-e6-split"
REASON = "the investigator watched R2's screen from time to time on 2026-11-18, PI-1118ai/aj"  # REG-1119a verbatim
OVERLAP = "manuscript/prereg/2026-11-11_xm600_gold_completion/overlap_images.txt"
SHA = {"overlap": "4f9719667c8a9294dc8cadc9565a048b9b7008ee0c1ecb924317550ba5278273",  # REG-1119a, build_overlap
       "a_cert_e3": "aec32aa0935d7fbba245e3c84826d055a7711ea3195eaaea2ba12477a4025362",  # CC-371 T2
       "freeze": "59308edb470f806ab6cae4b947095018868ded67d6f9f579451f8f87a3d2afeb",  # CC-371 T3
       "part1": "7492a16c692d3fd5ed28c4b8eaeab91766544ec5bd4ebe307a48537469d80957",  # CC-371 T4
       "labels": "ba362466ebd9c50918076dcf5865fbac9c5cd6482288f4251fa1f76e0f2718b4"}  # CC-371 T7
P_REAL = {**E.P_REAL, "split": f"{E.OUT}/split/A_CERT_E3_E6_SPLIT.json", "overlap": OVERLAP,
          "overlap_sha": SHA["overlap"], "overlap_n": 150}
LABEL = {"i": "E6 over all old_repeat items, as registered (primary, unchanged)",
         "ii": "sensitivity row: E6 over the old_repeat items whose image is NOT listed in overlap_images.txt (sha256 "
               "4f971966); fixed before the top-up start line by REG-1119a-topup-e6-split (CC-457 ruling (2) T2); "
               "neither row is a gate"}
SAME_MAP_DEF = ("CC-480 J-1, fixed before the run (CC-457 J2 B5(b)): top-up target questions (role target) on a listed "
                "image for which a base question on the same image (R2 was shown every base question of the listed "
                "images) names another class with the same Open Images map (identical pos and neg MIDs, the "
                "same-map grouping of a_cert.human)")
KEEP = ("n", "n_YN_both", "agree", "agreement")
ORIG = E.score_e3_core


def canon(x) -> str:
    """One serial form for in-memory rows and rows read back from JSON (NaN-safe, key order free)."""
    return json.dumps(json.loads(json.dumps(x, default=float)), sort_keys=True)


def same_map(key0: dict, key1: dict, syn: dict, listed: set) -> int:
    """(iii) label-free: the count of SAME_MAP_DEF (CC-480 J-1)."""
    base = defaultdict(set)
    for k in key0.values():
        base[k["image"]].add(k["class"])
    tgt = {(k["image"], k["class"]) for k in key1.values() if k["role"] == "target" and k["image"] in listed}
    return sum(any(b != c and syn.get(b, b) == syn.get(c, c) for b in base[i]) for i, c in tgt)


def split_rows(w: dict, fz: dict, key0: dict, ans0: dict, key1: dict, ans1: dict, listed: set, res3: dict) -> dict:
    """REG-1119a (i)-(iii) through the registered core; every other row must come out unchanged."""
    if not listed <= set(w["ids"]):
        raise Fault("an overlap image is not an I600 id")
    full = ORIG(w, fz, key0, ans0, key1, ans1)
    if canon(full["E6"]) != canon(res3["E6"]):  # E6 only: integer counts and ratios (E1-E5 floats not compared)
        raise Fault("recomputed E6 differs from A_CERT_E3_RESULT.json")
    drop = {q for q, k in key1.items() if k["role"] == "old_repeat" and k["image"] in listed}
    sub = ORIG(w, fz, key0, ans0, {q: k for q, k in key1.items() if q not in drop}, ans1)
    f6, s6 = full["E6"], sub["E6"]
    moved = ("old_repeat", "old_repeat_also_base_part3")
    if any(canon(full[r]) != canon(sub[r]) for r in full if r != "E6") or \
            any(canon(f6[x]) != canon(s6[x]) for x in f6 if x not in moved) or \
            f6["old_repeat"]["n"] - s6["old_repeat"]["n"] != len(drop):
        raise Fault("the split changed more than E6 old_repeat")
    pick = lambda b: {x: b[x] for x in KEEP}  # noqa: E731
    return {"schema": "vsps.a_cert_e3.e6_split.v1", "registration": REG_ID, "reason": REASON, "verdict": None,
            "note": "neither row is a gate; no other registered row changes (REG-1119a)", "row_label": E.ROW_LABEL,
            "E6_i": {"label": LABEL["i"], **pick(f6["old_repeat"])},
            "E6_ii": {"label": LABEL["ii"], **pick(s6["old_repeat"])},
            "counts_iii": {"old_repeat_on_listed_images": len(drop),
                           "same_map_pairs": same_map(key0, key1, w["syn"], listed),
                           "same_map_definition": SAME_MAP_DEF}}


def real_pins(a: dict) -> None:
    """The P_REAL-only gates of e3_score (HEAD blobs, base key) re-asserted, plus the CC-371 shas and this file."""
    if not all(A.committed(x) for x in (SELF, E.SELF, E.ADD, A.SELF, OVERLAP)):
        raise Fault("code, addendum or overlap list differs from its HEAD blob")
    got = (A.sha(ROOT / E.SELF), A.sha(ROOT / A.SELF), A.sha(ROOT / E.ADD), A.sha(ROOT / P_REAL["freeze"]),
           A.sha(ROOT / P_REAL["part1"]), a["labels_sha"])
    if got != (SHA["a_cert_e3"], E.SHA_ACERT, E.SHA_ADD, SHA["freeze"], SHA["part1"], SHA["labels"]):
        raise Fault("an input differs from its CC-371 pin")
    r1 = json.loads((ROOT / P_REAL["part1"]).read_text(encoding="utf-8"))
    if r1["provenance"]["key_sha256"] != A.KEY_SHA:
        raise Fault("the part-1 result did not read the pinned base key")


def split(a: dict, P: dict = P_REAL, wfn=None) -> int:
    """Label-free checks first; then e3_score on P['split'] with the wrapped core; FAULT <type> only."""
    try:
        res3, r3sha = E.pinned(P, "result", "A_CERT_E3_RESULT")
        if not any(REG_ID in ln and REASON in ln for ln in E.log_lines(P)):
            raise Fault("no REG-1119a line")
        ob = (ROOT / P["overlap"]).read_bytes()  # hash and parse the same bytes
        listed = ob.decode("utf-8").split()
        if hashlib.sha256(ob).hexdigest() != P["overlap_sha"]:
            raise Fault("overlap_images.txt differs from its pin")
        if len(listed) != P["overlap_n"] or len(set(listed)) != len(listed):
            raise Fault("the overlap list is not the registered list of unique ids")
        if P is P_REAL:
            real_pins(a)
    except BaseException as e:  # noqa: BLE001  (fault rule: exception type only)
        print(f"FAULT {type(e).__name__}")
        return 2

    def core(w, fz, key0, ans0, key1, ans1):
        out = split_rows(w, fz, key0, ans0, key1, ans1, set(listed), res3)
        out["split_provenance"] = {"split_script_sha256": A.sha(__file__), "overlap_sha256": P["overlap_sha"],
                                   "a_cert_e3_result_sha256": r3sha}
        return out

    E.score_e3_core = core
    try:
        return E.e3_score(a, {**P, "result": P["split"]}, wfn)
    finally:
        E.score_e3_core = ORIG


def main(argv: list) -> int:
    if E._audit not in getattr(main, "hooks", ()):
        sys.addaudithook(E._audit)
        main.hooks = (E._audit,)
    if len(argv) == 13 and argv[0] == "split" and tuple(argv[1::2]) == E.SCORE_ARGS:
        return split(dict(zip((x[2:].replace("-", "_") for x in E.SCORE_ARGS), argv[2::2])))
    raise SystemExit("usage: a_e6_split.py split " + " ".join(f"{x} X" for x in E.SCORE_ARGS))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
