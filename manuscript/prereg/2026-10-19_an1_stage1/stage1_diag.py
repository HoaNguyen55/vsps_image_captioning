#!/usr/bin/env python3
"""A-N1 stage-1 diagnostic, written AFTER the stage-1 choice was seen (EXPLORATORY, disclosed in ADDENDUM_DRAFT.md).

How much of each candidate is recall? Point estimates per set, level and system, all images, primary lexicon:
recall R, bpref_set, the ratio bpref_set / R, raw precision P and condensed precision P^c.

  OMP_NUM_THREADS=2 nice -n 15 python3 stage1_diag.py --out stage1_diagnostic.json
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np

import measures as me

g = me.g


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    out = ap.parse_args().out
    if out.exists():
        raise SystemExit(f"{out} exists; never overwritten")
    reg = g.jload(g.PREREG)
    res = {"schema": "vsps.an1_stage1_diag.v1", "status": "EXPLORATORY, computed after the stage-1 choice was seen",
           "note": "R is the macro recall that bpref_set and cF1 use; P is raw precision against the level positives (at oiv7_verified it is not the registered OIV7 precision)",
           "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "measures_py_sha256": g.sha256_file(me.HERE), "this_sha256": g.sha256_file(Path(__file__)), "sets": {}}
    for name, _, ids, lexicons, files, complete in me.stage1_inputs():
        caps = {s: g.read_captions(f) for s, f in files.items()}
        ds = me.dev_dataset(reg, ids, lexicons, caps, complete)
        lx, n = next(iter(lexicons)), len(ids)
        idx, one = np.arange(n), np.ones((1, n))
        neg = me.negatives(ds.lex[lx], lx)
        cells = []
        for lv in ("refs1_randk", "refs_all", complete):
            gold = me.positives(ds, lx, lv)
            for s in caps:
                ment = ds.ment(s, lx)
                c = me.condensed(me.judged_rows(ment, gold, neg), idx, one)
                b = float(me.bpref(me.bpref_rows(ment, gold, neg), idx, one)["F"][0])
                cells.append({"level": lv, "system": s, "M": float(c["M"][0]), "R": float(c["R"][0]), "bpref": b,
                              "bpref_over_R": b / float(c["R"][0]),
                              "P": float(g.scores(g.rows(ment, gold), idx, one)["P"][0]), "P_condensed": float(c["P"][0])})
        ratio = [c["bpref_over_R"] for c in cells]
        res["sets"][name] = {"cells": cells, "bpref_over_R_min": min(ratio), "bpref_over_R_median": float(np.median(ratio)),
                             "P_condensed_min": min(c["P_condensed"] for c in cells if c["level"] != complete)}
        print(name, {k: v for k, v in res["sets"][name].items() if k != "cells"}, flush=True)
    out.write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    Path(str(out) + ".sha256").write_text(f"{g.sha256_file(out)}  {out.name}\n", encoding="utf-8")


if __name__ == "__main__":
    main()
