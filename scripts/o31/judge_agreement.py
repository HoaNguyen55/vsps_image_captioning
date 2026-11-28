"""Agreement of points.extra_points (C06) with the three judges' fixture scripts of the point rule.

    $PY -I -B judge_agreement.py <rulings dir> <committed gate.py>

Each script runs unchanged (runpy, its own prints captured); its fixture k0 dicts are translated to the real k0.json
form (op = [tau_acc, tau_rej, [families]], "V" -> vintern, "V+I" -> vintern + internvl3) and passed to
extra_points. One line per case: the script's verdict, then ours. The committed text governs where they differ.
"""
import contextlib
import io
import json
import os
import runpy
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, os.environ.get("O31_SRC", str(Path(__file__).resolve().parent / "src")))

from o31 import points  # noqa: E402

FAMS = {"V": ["vintern"], "V+I": ["vintern", "internvl3"]}


def real_form(k: dict, complete_default=None) -> dict:
    k = json.loads(json.dumps(k))

    def fix(p):
        if isinstance(p, dict) and isinstance(p.get("op"), list) and len(p["op"]) == 3 and p["op"][2] in FAMS:
            p["op"] = [p["op"][0], p["op"][1], FAMS[p["op"][2]]]
    for p in k.get("points", []):
        fix(p)
    for key in ("op_star", "op_mid"):
        fix((k.get("decision") or {}).get(key))
    if "complete" not in k and complete_default is not None:
        k["complete"] = complete_default
    return k


def ours(k: dict) -> tuple:
    """(result, picks 'pXX pYY' or None, R-order labels or None)."""
    try:
        r = points.extra_points(k)
    except SystemExit as e:
        return (f"REFUSED ({str(e)[:40]})", None, None)
    picks = None if not r["op_75"] else f"p{r['op_25']['grid_index']:02d} p{r['op_75']['grid_index']:02d}"
    return (r["result"], picks, r["order_by_R"])


def verdict(script_out, mine) -> str:
    """AGREE / DIFFER on the result, and on the picks and the R order where the script reports them."""
    if isinstance(script_out, dict):
        script_out = (script_out["result"],)
    res = str(script_out[0]).replace("T-4 ", "")
    same = res.split(" (")[0] == mine[0] or (res.startswith("IDENTIFIED") and mine[0] == "IDENTIFIED")
    if len(script_out) == 4 and mine[1]:
        picks = script_out[3].replace("OP_25=", "").replace("OP_75=", "")
        lab = [x.replace("S1", "OP_strict") for x in script_out[1]]
        same = same and picks == mine[1] and lab == mine[2]
    return "AGREE" if same else "DIFFER (text governs; see RUN_NOTE)"


def run(script: Path, gate_py: Path):
    out = io.StringIO()
    argv = sys.argv
    sys.argv = [str(script), str(gate_py)]
    try:
        with contextlib.redirect_stdout(out):
            ns = runpy.run_path(str(script), run_name="judge_fixture")
    finally:
        sys.argv = argv
    return ns, out.getvalue()


def main() -> int:
    rulings, gate_py = Path(sys.argv[1]), Path(sys.argv[2])
    lines = []
    ns, txt = run(rulings / "parta_adv.py", gate_py)
    lines.append("== parta_adv.py (CC-525r2a): script verdict | ours")
    for name, k in ns["C"].items():
        sc, mine = ns["parta"](k), ours(real_form(k))
        lines.append(f"{name[:44]:44s} | {str(sc[0])[:48]:48s} | {mine[0]:15s} {mine[1] or '':8s} | {verdict(sc, mine)}")
    for name, args in (("dyadic level 1: p03 P 40.9, p20 P 41.3", (40.9, 41.3, 3, 20)),
                       ("dyadic level 1: p03 P 41.3, p20 P 40.9", (41.3, 40.9, 3, 20)),
                       ("dyadic level 2: equal P, p20 vs p03", (41.0, 41.0, 20, 3))):
        k = ns["tie"](*args)
        sc, mine = ns["parta"](k), ours(real_form(k))
        lines.append(f"{name[:44]:44s} | {str(sc[0])[:48]:48s} | {mine[0]:15s} {mine[1] or '':8s} | {verdict(sc, mine)}")
    R = [30.0] * 30
    R[29], R[14], R[27], R[7], R[22] = 48.5, 42.5, 45.5, 39.5, 39.5
    k = ns["k0"](R, s1=(36.5, 42.6, "S1"))
    sc, mine = ns["parta"](k), ours(real_form(k))
    lines.append(f"{'identical R, distinct shas: p07 vs p22':44s} | {str(sc[0])[:48]:48s} | {mine[0]:15s} {mine[1] or '':8s} | "
                 f"{verdict(sc, mine)}")
    ns, txt = run(rulings / "chooser_adv.py", gate_py)
    lines.append("== chooser_adv.py (CC-525r2, before the split): script verdict | ours")
    for name, k in ns["cases"].items():
        sc, mine = ns["amended"](k), ours(real_form(k))
        lines.append(f"{name[:44]:44s} | {str(sc[0])[:48]:48s} | {mine[0]:15s} {mine[1] or '':8s} | {verdict(sc, mine)}")
    ns, txt = run(rulings / "parta_check.py", gate_py)
    lines.append("== parta_check.py (CC-525b; its fixtures carry no 'complete' key, set to true here): script | ours")
    for name, k in ns["cases"].items():
        sc, mine = ns["ops5"](k), ours(real_form(k, complete_default=True))
        lines.append(f"{name[:44]:44s} | {sc['result'][:48]:48s} | {mine[0]:15s} {mine[1] or '':8s} | {verdict(sc, mine)}")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
