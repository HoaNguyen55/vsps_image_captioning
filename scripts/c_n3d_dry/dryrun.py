"""DRY-N3D driver (CC-511e6 ruling 4 (c), (d)). SYNTHETIC BUNDLE ONLY.

Imports the committed c_n3d and c_n3d_host UNCHANGED (every CODE.sha256 line checked) and patches only H.PUSH (the
bundle push list), the values of H.DATA_PINS (keys and the jar pin unchanged), N.PARITY_TOL = inf and
VSPS_MACHINE_ID. Then H.run(root, data, out) with B = 2000 under the stdlib trace module (lines of c_n3d_host.py and
c_n3d.py only), and the PASS checks of ruling 4 (d).

  python -I -B dryrun.py --code C --bundle B --real-push C/PUSH_LIST.sha256 --out DIR
Refuses unless B holds the SYNTHETIC marker and every rewritten file's sha differs from its real pin (a wrong --root
can never spend the registered look).
"""
from __future__ import annotations

import argparse
import ast
import json
import math
import os
import resource
import sys
import time
import trace
from pathlib import Path

WANT = {"c_n3d.py": "f61df892bbc848bccab8a65445f8554e746c3e92bb6785c3fd1a85596de3baaa",
        "c_n3d_host.py": "05b3b82761b643c4ab18a13b711e07b5df171158bc66add6ba6fde0460a94569"}
HOST_FUNCS = ("run", "vi_cells", "stage2_cells", "en_cells", "flag_arrays", "make_statuses", "status_fn", "cell_of",
              "t8_length", "family_rows", "custody", "data_pins", "module_pin_check")
N_FUNCS = ("english_public",)
SENS = ("SR1_rand_mean_d0_d2", "SR2_M5", "SR2_M15", "SR4_LN_0.10", "SR4_LN_0.40", "SR5_T8_length",
        "SR6_reversed_precedence")
DECISION = "N3D_DECISION_SYNTHETIC_DRY.json"


def code_check(code: Path, sha) -> None:
    for ln in (code / "CODE.sha256").read_text().splitlines():
        h, p = ln.split(None, 1)
        if sha(code / p.strip()) != h:
            raise SystemExit(f"REFUSED: {p} is not as in CODE.sha256")
    if any(sha(code / f) != h for f, h in WANT.items()):
        raise SystemExit("REFUSED: c_n3d.py / c_n3d_host.py are not f61df892 / 05b3b827")


def interlock(bundle: Path, real_push: dict, real_pins: dict, push: dict, pins: dict) -> None:
    """The bundle is synthetic: marker present, same path sets, every decode and caption file differs from its pin."""
    if not (bundle / "SYNTHETIC").is_file() or set(push) != set(real_push) or set(pins) != set(real_pins):
        raise SystemExit("REFUSED: not a DRY-N3D synthetic bundle")
    same = [p for p in push if p.endswith(".preds.json") and push[p] == real_push[p]]
    same += [p for p in pins if not p.endswith(".jar") and pins[p] == real_pins[p]]
    if same or pins["vncorenlp/VnCoreNLP-1.2.jar"] != real_pins["vncorenlp/VnCoreNLP-1.2.jar"]:
        raise SystemExit(f"REFUSED: real files in the bundle: {same[:3]}")


def statements(path: Path, funcs: tuple) -> dict[str, list[int]]:
    """Statement lines of each named top-level function (nested ones included), less docstrings and the
    statements that are only `raise SystemExit(...)` (ruling 4 (d))."""
    out = {}
    for node in ast.parse(path.read_text(encoding="utf-8")).body:
        if not isinstance(node, ast.FunctionDef) or node.name not in funcs:
            continue
        docs = {id(n.body[0]) for n in ast.walk(node) if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and
                isinstance(n.body[0], ast.Expr) and isinstance(n.body[0].value, ast.Constant)}
        out[node.name] = sorted({st.lineno for st in ast.walk(node) if isinstance(st, ast.stmt) and st is not node
                                 and id(st) not in docs and not (isinstance(st, ast.Raise) and
                                 isinstance(st.exc, ast.Call) and getattr(st.exc.func, "id", "") == "SystemExit")})
    return out


def coverage(path: Path, counts: dict, funcs: tuple) -> dict:
    src = path.read_text(encoding="utf-8").splitlines()
    done = {ln for (f, ln), c in counts.items() if c and Path(f).resolve() == path.resolve()}
    return {fn: {"statements": len(ls), "executed": sum(ln in done for ln in ls),
                 "not_executed": [f"{ln}: {src[ln - 1].strip()}" for ln in ls if ln not in done]}
            for fn, ls in statements(path, funcs).items()}


def checks(rec: dict, N) -> dict:
    vi = [f"{s}|{m}" for s in ("ov_dev_b", "xm_dev500") for m in N.MODELS]
    fam = [f"{s}|{m}" for s in ("ov_dev_b", "xm_dev500") for m in N.FAMILY_MODELS]
    sens = rec["sensitivity"]
    c = {"family_6_rows": len(rec["family"]) == 6,
         "rows_6_vi_cells": sorted(rec["rows"]) == sorted(vi),
         "sensitivity_SR1_SR2_SR4_SR5_SR6_per_cell": all(set(SENS) <= set(sens[k]) for k in vi),
         "SR3_for_4_family_cells_computed": all(isinstance(sens[k].get("SR3_stored_batched"), dict) for k in fam)
         and not any("SR3_stored_batched" in sens[k] for k in vi if k not in fam),
         "english_3_models_with_NOT_RUN": sorted(rec["english"]) == sorted(N.MODELS) and all(
             any(v == N.EN_NOT_RUN for v in e["rows"].values()) for e in rec["english"].values()),
         "modules_checked_gt_0": rec["modules_checked"] > 0,
         # the synthetic bundle exercised every branch (advisor 7): all VI cells decidable, every flag fires
         "all_6_vi_cells_decidable": all(rec["rows"][k]["decidable"] for k in vi),
         "h_rows_no_rule_in_non_family_cells": all("h_rows_no_rule" in rec["rows"][k] for k in vi if k not in fam),
         "every_flag_fires_in_every_vi_cell": all(rec["rows"][k]["rows"][f"base_{f}_ret"]["point"] > 0
                                                  for k in vi for f in N.FLAGS),
         "verified_status_branch_used_xm": rec["gold_decided_class_level"]["xm_dev500"]["verified"] > 0}
    return c


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for k in ("code", "bundle", "out"):
        ap.add_argument(f"--{k}", type=Path, required=True)
    a = ap.parse_args()
    code, bundle, outdir = a.code.resolve(), a.bundle.resolve(), a.out.resolve()
    sys.path.insert(0, str(code))
    os.environ.setdefault("PYTHONHASHSEED", "0")           # as c_n3d.main
    import c_n3d as N
    code_check(code, N.sha)
    import c_n3d_host as H
    assert H.N is N
    real_push, real_pins = N.push_list(H.PUSH), dict(H.DATA_PINS)
    push, pins = N.push_list(bundle / "PUSH_LIST.sha256"), json.loads((bundle / "DATA_PINS.json").read_text())
    interlock(bundle, real_push, real_pins, push, pins)
    # the four patches of ruling 4 (c)
    H.PUSH = bundle / "PUSH_LIST.sha256"
    H.DATA_PINS.update(pins)
    N.PARITY_TOL = math.inf
    os.environ["VSPS_MACHINE_ID"] = "DRY-N3D-LAPTOP-SYNTHETIC"
    outdir.mkdir(parents=True, exist_ok=False)
    (outdir / "SYNTHETIC_README.txt").write_text(
        f"{DECISION} is the decision file of DRY-N3D, the shape-faithful dry run of CC-511e6 ruling 4 on a SYNTHETIC "
        "bundle. Every number in it is synthetic and means nothing about Paper C or N3D.\n", encoding="utf-8")
    t0, rc = time.time(), 0
    tr = trace.Trace(count=1, trace=0, ignoredirs=[sys.prefix, sys.base_prefix, str(bundle)])
    try:
        tr.runfunc(H.run, bundle / "root", bundle / "ncs-data", outdir / DECISION)
    except BaseException as e:                       # a fault is the finding: recorded, never patched
        import traceback
        rc = 1
        (outdir / "FAULT_TRACEBACK.txt").write_text(traceback.format_exc(), encoding="utf-8")
        print(f"DRY-N3D FAULT: {type(e).__name__}; traceback in FAULT_TRACEBACK.txt")
    wall = time.time() - t0
    ru_s, ru_c = resource.getrusage(resource.RUSAGE_SELF), resource.getrusage(resource.RUSAGE_CHILDREN)
    counts = tr.results().counts
    cov = {"c_n3d_host.py": coverage(code / "c_n3d_host.py", counts, HOST_FUNCS),
           "c_n3d.py": coverage(code / "c_n3d.py", counts, N_FUNCS)}
    dec = outdir / DECISION
    res = {"rc": rc, "decision_file": dec.is_file(), "partial_left": (outdir / (DECISION + ".partial")).exists(),
           "wall_s": round(wall, 1), "cpu_s_self": round(ru_s.ru_utime + ru_s.ru_stime, 1),
           "cpu_s_children": round(ru_c.ru_utime + ru_c.ru_stime, 1), "coverage": cov,
           "patches": ["H.PUSH", "H.DATA_PINS values", "N.PARITY_TOL=inf", "VSPS_MACHINE_ID"],
           "note_module_pin_check": "its default push= binds the real PUSH_LIST at definition; the closure files are "
                                    "byte-equal in both lists, so it checks the same pins (not patched)"}
    if dec.is_file():
        rec = json.loads(dec.read_text(encoding="utf-8"))
        res["decision_sha256"] = N.sha(dec)
        res["checks"] = checks(rec, N)
        res["wall_h_in_record"] = rec["wall_h"]
    uncovered = {f: {fn: v["not_executed"] for fn, v in c.items() if v["not_executed"]} for f, c in cov.items()}
    res["pass_core"] = rc == 0 and res["decision_file"] and all(res.get("checks", {"x": False}).values())
    (outdir / "DRY_RESULT.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: res[k] for k in res if k != "coverage"}, indent=1))
    print("not executed:", json.dumps(uncovered, indent=1, ensure_ascii=False))
    sys.exit(rc)


if __name__ == "__main__":
    main()
