#!/usr/bin/env python3
"""C-DIAG §4.5 [Q6, R2-W5; CC-299r3 R6, NB-C1, NB-C2, NB-C5]: the tier-1 mBLIP verifier table recomputed post hoc on
the 3,000 XM-dev500 ∪ XM-test2500 images (CPU; coordinator-run, never a subagent: T5 holds train caption text).

    PY=~/.venvs/c_pvr/bin/python
    $PY -X utf8 -I -B scripts/c_diag/c_diag_t1table.py --labels W/label_subset.json --labels-sha H --res R
R6: runs UNCONDITIONALLY once Stage 0 completes, in every branch (main, gate-only, no rental, gate FAIL). Before it
opens T2-T5 the coordinator writes the OPS line (this command line in full, the nine shas; R2-W5 (e)).
Its own nine-entry (path, sha256) list under the same `allow` guard (§2.3 backstop included); no manifests() call
(R2-W5 (b)): sha(T4) = TMAN, then only T4's manifest/xm3600_vi.json line, which T5 must match and begin f81323d1.
Cells = c_pvr_score.py l.393-403 unchanged, restricted to the 3,000 sorted ids (NB-C2); s1_table's arithmetic and its
FALLBACK rule; own draw default_rng(20261111), idx = rng.integers(0, 3000, size=(10000, 3000)) (R2-W5 (d)); the > 1 %
undefined-replicate FAULT applied here to every s1_table estimate (s1_table hard-codes strict=False, NB-C1).
XM600 rows of T2, T3 and T5 are loaded and discarded, never scored or printed. Nothing but numbers is printed.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

HERE = Path(os.path.abspath(__file__)).parent  # unresolved: the mutant suite runs scratch copies
sys.path.insert(0, str(HERE))
import c_diag as D  # noqa: E402

TMAN = "4849a08f1fc384f1901fd294950f9ea20a5622879838c4a5ecac73cec62c3efe"  # T4 (LOG l.1763 / S11 docs)
T5_PREFIX = "f81323d1"
T = {  # §4.5 table: T1-T4, T7-T9 by sha; T5 by T4's line; T6 by --labels-sha
    "T1": ("~/s11pull_1107/final/c_pvr_out/SHA256SUMS_tier1",
           "7cf129106dd0ef2c382f4a9a4fd480295e5fc36e3e81b6522439370d500850e8"),
    "T2": ("~/s11pull_1107/final/c_pvr_out/out/xm3600_vi.PVR-drop.jsonl",
           "8bdc38ec2b89078040c677abbbaec29258cb446b1d916cab1bbd606c6bfaab31"),
    "T3": ("~/s11pull_1107/final/c_pvr_out/out/xm3600_vi.PVR-keep.jsonl",
           "ca7a9a208ab8f3c35c12c633a67cb065a13207343b60c71afd3c570fb62b6450"),
    "T4": ("~/c_pvr_h4_1107/MANIFEST.sha256", TMAN),
    "T7": (D.B["lists"][0], D.B["lists"][1]),
    "T8": (D.B["vi_map"][0], D.B["vi_map"][1]),
    "T9": (D.B["desc"][0], D.B["desc"][1]),
}
BUILD = "~/c_pvr_h4_1107"
SEED, B_REPS = 20261111, 10_000
LABEL = ("post hoc (PI-1109a Q6), descriptive; tier-1 verifier mBLIP-BLOOMZ-7B on tier-1 demonstrations (D-VI memory, "
         "not CC-212's), in situ, all units; restricted to the XM-dev500 ∪ XM-test2500 images")
PS = None


def p(key: str) -> Path:
    q = Path(T[key][0]).expanduser()
    return q if q.is_absolute() else D.ROOT / q


def t5_sha(man: bytes) -> str:
    """R2-W5 (b): only the manifest/xm3600_vi.json line of T4 is read."""
    want = [h for h, rel in (x.split("  ", 1) for x in man.decode().splitlines()) if rel == "manifest/xm3600_vi.json"]
    if len(want) != 1 or not want[0].startswith(T5_PREFIX):
        D.fault(f"MANIFEST.sha256 has no single manifest/xm3600_vi.json line beginning {T5_PREFIX}")
    return want[0]


def cells(M: dict, R: dict, st: dict, ids: list[str], mention) -> tuple[dict, Counter]:
    """c_pvr_score.py l.393-403 (and the T|, UN|, KR|, DS| column appends of l.407-415), unchanged except the loop
    runs over the 3,000 sorted ids (NB-C2). rec = PVR-drop / PVR-keep records of the image."""
    Q = {q["id"]: q for q in M["queries"]}
    cols, side = defaultdict(list), Counter()
    for i in ids:
        si = st.get(i, {})
        stat = lambda c, si=si: si.get(c, "unknown")  # noqa: E731
        rec = {a: R[a][i] for a in ("PVR-drop", "PVR-keep")}
        dids = [str(x) for x in Q[i]["ranked"][:PS.CP.K]]
        if any(rec[a]["demo_ids"] != dids for a in rec):
            D.fault(f"demo_ids differ from the manifest ranked[:{PS.CP.K}]")
        dcs = [M["demos"][d] for d in dids]
        labs, ok = PS.verifier_labels(dcs, rec["PVR-drop"], rec["PVR-keep"])
        side["label_mismatch_images"] += not ok
        cell = Counter()
        for dc, lab, md, mk, did in zip(dcs, labs, rec["PVR-drop"]["masks"], rec["PVR-keep"]["masks"], dids):
            for c in {c for p in dc["props"] if p["kind"] == "obj" for c in p["classes"]} & mention(dc["text"]):
                cell[f"T|{PS.unit_label(dc, lab, c)}|{stat(c)}"] += 1
                carry = [j for j, p in enumerate(dc["props"]) if p["kind"] == "obj" and c in p["classes"]]
                side["unit_label_conflicts"] += len({lab[j] for j in carry}) > 1  # CC-293 N9
                cell[f"UN|{stat(c)}"] += 1  # N2: each run read alone (no cross-run reconstruction)
                cell[f"KR|{stat(c)}"] += mk[carry[0]]
                cell[f"DS|{stat(c)}"] += not md[carry[0]]
        for lab in ("REJECTED", "UNCERTAIN", "SUPPORTED"):
            for s0 in ("absent", "present", "unknown"):
                cols[f"T|{lab}|{s0}"].append(cell[f"T|{lab}|{s0}"])
        for k in ("UN|absent", "UN|present", "KR|absent", "KR|present", "DS|present"):
            cols[k].append(cell[k])
    return dict(cols), side


def boot(n: int):
    """R2-W5 (d): own draw, counts-matrix form (W @ R = the replicate sums of idx)."""
    rng = np.random.default_rng(SEED)
    idx = rng.integers(0, n, size=(B_REPS, n))
    W = np.zeros((B_REPS, n), np.int32)
    for r in range(B_REPS):
        W[r] = np.bincount(idx[r], minlength=n)
    return lambda R: W @ R


def faults(tbl: dict) -> list[str]:
    """NB-C1 [J1 N-2]: every estimate s1_table returns (dicts with 'dropped') must drop <= 1 % of B."""
    return [k for k, v in tbl.items() if isinstance(v, dict) and "dropped" in v and v["dropped"] > 0.01 * B_REPS]


def run(a) -> dict:
    global PS
    PS = D.score_mod()
    PS.load(D.ROOT)  # c_pvr_gpu (OUT_KEYS), c_pvr, xm3600_oiv7, c_pvr_cay, c_pvr_cm, gates behind their pins
    mention = PS.mention_fns(D.ROOT)[""]
    entries = {str(p(k)): h for k, (_x, h) in T.items()}
    if not re.fullmatch(r"[0-9a-f]{64}", a.labels_sha or ""):
        D.fault("--labels-sha must be the full Stage-0 sha of the label subset (T6)")
    entries[a.labels] = a.labels_sha
    D.SUBCMD["t1table"] = ()
    D.allow("t1table", entries, [a.res], helpers=False)
    man = p("T4").read_bytes()
    if D.sha(man) != TMAN:
        D.fault("MANIFEST.sha256 differs from TMAN 4849a08f")
    h5 = t5_sha(man)
    t5 = Path(BUILD).expanduser() / "manifest" / "xm3600_vi.json"
    D.GUARD.add(t5, h5)
    D.GUARD.install()
    sums = PS.sums_of(p("T1"))
    for k, rel in (("T2", "out/xm3600_vi.PVR-drop.jsonl"), ("T3", "out/xm3600_vi.PVR-keep.jsonl")):
        if sums.get(rel) != T[k][1]:
            D.fault(f"{rel}: SHA256SUMS_tier1 line differs from {k}")
    M = json.loads(t5.read_bytes())
    if (M.get("label"), M.get("set")) != (PS.CP.LABEL, PS.XM):
        D.fault("manifest/xm3600_vi.json label/set mismatch")
    qids = {q["id"] for q in M["queries"]}
    R = {arm: PS.records(p("T1").parent, sums, PS.XM, arm, qids) for arm in ("PVR-drop", "PVR-keep")}
    lists = json.loads(p("T7").read_text("utf-8"))
    ids = sorted({r[0] for ds in ("xm_dev500", "xm_test2500") for r in lists["sets"][ds]})
    if len(ids) != D.N_LABEL_IDS or not set(ids) <= qids or any(R[x] is None or not set(ids) <= set(R[x]) for x in R):
        D.fault("the 3,000 ids are not all tier-1 XM3600 query ids with PVR-drop and PVR-keep records")
    st = PS.gold(D.ROOT, Path(a.labels), p("T9"), pins=False)
    cols, side = cells(M, R, st, ids, mention)
    del M, R
    tbl = PS.s1_table(PS.Boot(cols, boot(D.N_LABEL_IDS)), side)
    if bad := faults(tbl):
        D.fault(f"> 1 % undefined bootstrap replicates in {bad} (§4.5 R2-W5 (d); final, §8.4)")
    rec = {"label": D.LABEL, "what": LABEL, "n_images": D.N_LABEL_IDS, "seed": SEED, "B": B_REPS,
           "inputs": {**{k: v[1] for k, v in T.items()}, "T5": h5, "T6": a.labels_sha}, "table": tbl}
    h = D.write_new(Path(a.res) / "t1table.json", rec)
    D.say({"step": "t1table", "t1table_sha256": h, "status": tbl.get("status"), "T5": h5})
    return rec


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--labels", required=True)
    ap.add_argument("--labels-sha", required=True)
    ap.add_argument("--res", required=True)
    a = ap.parse_args()
    D.load()
    run(a)
    D.GUARD.done()


if __name__ == "__main__":
    main()
