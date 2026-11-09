#!/usr/bin/env python3
"""Guard mutants for the C-DIAG code (CC-299r3 code read; scripts/b_pa1/b_pa1_gpu_mutants.py form). Each mutant breaks
one gate or FAULT path in a scratch copy and must make its selftest fail, offline (unshare -rn), -X utf8 -I -B: test_c_diag.py
for the Python files, c_diag_job_selftest.sh for c_diag_job.sh. The scratch tree mirrors the repo by symlinks, so only
the mutated file differs. Run (scratch under $TMPDIR):
    ~/.venvs/c_pvr_cider/bin/python -X utf8 -I -B scripts/c_diag/c_diag_mutants.py [--jobs 3]
"""
import argparse
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(os.path.abspath(__file__)).parent
REPO = HERE.parents[1]
D, G, S, T, J = "c_diag.py", "c_diag_gpu.py", "c_diag_score.py", "c_diag_t1table.py", "c_diag_job.sh"
MUT = [  # (id, file, old, new): each old must occur exactly once
    ("D1 sealed component", D, 'if ".vsps_sealed" in parts:', "if False:"),
    ("D2 test_data.json", D, 'DENY = ("test_data.json", ', "DENY = ("),
    ("D3 t2pool_*", D, '"t2pool_*", ', ""),
    ("D4 allow-list sha", D, 'return None if self.sha_ok(q, h) else "sha256 differs from its allow-list entry"',
     "return None"),
    ("D5 write to an input", D, 'if write:\n            return "write to an allow-listed input"',
     'if False:\n            return "write to an allow-listed input"'),
    ("D34 out dir write-only", D, "if (write and under(p, self.outs)) or", "if under(p, self.outs) or"),
    ("D35 denied out dir", D, 'if (d := deny(os.path.abspath(o) + "/x")) is not None:', "if False:"),
    ("D36 --rate required", D, "    if not a.rate:  # CC-307 N5", "    if False:  # CC-307 N5"),
    ("D37 LABEL in records", D, 'write_new(w / "floor.json", {"label": LABEL, **f}, sums)', 'write_new(w / "floor.json", f, sums)'),
    ("D6 unlisted open", D, 'return "not on the allow-list (Appendix B)"', "return None"),
    ("D7 swallowed refusal", D, "if self.faults:\n            fault(", "if False:\n            fault("),
    ("D8 sealed listing", D, 'self.stop(f"listing refused: deny backstop ({d})")', "pass"),
    ("D9 N18 out dir", D, "if under(os.path.abspath(o), [str(ROOT)]) or under(os.path.realpath(o), "
                          "[os.path.realpath(ROOT)]):", "if False:"),
    ("D10 NB-2 row 8", D, '"decomp": ("lists", "frozen",', '"decomp": ("lists", "oiv7", "frozen",'),
    ("D11 floor 0.10", D, "FLOOR = 0.10", "FLOOR = 0.05"),
    ("D12 floor >=", D, "return c_b is not None and c_b >= FLOOR", "return c_b is not None and c_b > FLOOR"),
    ("D13 gate-only = both", D, 'return all(not f[b]["passes_floor"] for b in BACKBONES)',
     'return any(not f[b]["passes_floor"] for b in BACKBONES)'),
    ("D14 bare rule", D, "if norm(u[a:b].lower()) not in ok:", "if False:"),
    ("D15 one class", D, 'len(p["classes"]) == 1 and', 'len(p["classes"]) >= 1 and'),
    ("D16 unknown out", D, 'st.get(p["classes"][0]) in ("present", "absent")', "True"),
    ("D17 per-query cap", D, 'per[(u["qid"], u["status"])] < cap:', 'per[(u["qid"], u["status"])] <= cap:'),
    ("D18 supply FAULT", D, "if any(len(v) < CELL_MIN for v in take[\"c\"].values()):", "if False:"),
    ("D19 cell 150", D, "CELL, CELL_MIN = 150, 100", "CELL, CELL_MIN = 140, 100"),
    ("D20 no status on host", D, 'for k in ("qid", "file", "image_sha256", "rank", "prop_index", "text")}',
     'for k in ("qid", "file", "image_sha256", "rank", "prop_index", "text", "status")}'),
    ("D21 VI share empty", D, "for c in caps) / max(1, len(caps))", "for c in caps) / max(1, sum(map(bool, caps)))"),
    ("D22 VI block ret and rand", D, 'for a in ("ret", "rand"))', 'for a in ("ret",))'),
    ("D23 byte-equal order", D, '"byte_equal_computable": order_ok and man_ok and bs_ok',
     '"byte_equal_computable": man_ok and bs_ok'),
    ("D24 CC-212 prompt sha", D, "if got != {q: want.get(q) for q, _f, _h in items}:", "if False:"),
    ("D25 never-cut XM", D, 'never = next((k for k in ORDER if k in keep and k[1] == "xm_test2500"), None)',
     "never = None"),
    ("D26 money binds the cap", D, "return min(CAP_GATE_H if gate_only else CAP_MAIN_H, (M_D - SETUP_VND) / rate)",
     "return CAP_GATE_H if gate_only else CAP_MAIN_H"),
    ("D27 O_B", D, "o_b = 0 if (a.b_resume_used or a.b_ended) else 7 * a.r_b + 30",
     "o_b = 0 if (a.b_resume_used or a.b_ended) else 7 * a.r_b"),
    ("D28 3 r_D", D, "rhs = m + 3 * a.r_d + a.sigma_live", "rhs = m + 2 * a.r_d + a.sigma_live"),
    ("D29 h_B = T1 + T1'", D, "h_b = a.h_b_t1 + a.h_b_t1p", "h_b = a.h_b_t1"),
    ("D30 NB-3 subset keys", D, "if bad := set(lab) - set(self.ids3000()):", "if bad := set():"),
    ("D31 unit = carried AND found", D, '{c for p in dc["props"] if p["kind"] == "obj" for c in p["classes"]} & '
                                        'mention(dc["text"])', '{c for p in dc["props"] if p["kind"] == "obj" for c in '
                                                               'p["classes"]}'),
    ("D32 written once", D, 'if p.exists():\n        fault(f"{p.name} exists', 'if False:\n        fault(f"{p.name} exists'),
    ("G1 text never asked", G, 'flat = [(n, j) for n, dc in enumerate(dcs) for j, p in enumerate(dc["props"]) if p["kind"] == "obj"]',
     'flat = [(n, j) for n, dc in enumerate(dcs) for j, p in enumerate(dc["props"])]'),
    ("G2 CAP label", G, 'out[n][j] = "CAP" if x >= D.CP.CAP else lab', "out[n][j] = lab"),
    ("G3 REJECTED only", G, 'return [[lab == "REJECTED" for lab in d] for d in labels]',
     'return [[lab in ("REJECTED", "UNCERTAIN") for lab in d] for d in labels]'),
    ("G4 ctl obj-only", G, "a7 = D.CP.a7_masks(qid, [[m[j] for j in o] for m, o in zip(fm, obj)])",
     "a7 = D.CP.a7_masks(qid, [[m[j] for j in range(len(m))] for m, o in zip(fm, obj)])"),
    ("G5 order last", G, 'return xs[::-1] if w["order"] == "last" else list(xs)', "return list(xs)"),
    ("G6 zero-shot fallback", G, '(D.C.prompt(w["tpl"], kept) if kept else zs)', 'D.C.prompt(w["tpl"], kept)'),
    ("G7 0.5 h pull", G, 'return int(c["cap_h"] * 3600 - D.PULL_H * 3600 -', 'return int(c["cap_h"] * 3600 - 0 -'),
    ("G8 never-cut in projection", G, "if k in blocks and k != never and not started(k)), None)",
     "if k in blocks and not started(k)), None)"),
    ("G9 started not cut", G, "if k in blocks and k != never and not started(k)), None)",
     "if k in blocks and k != never), None)"),
    ("G10 gate-only no S2", G, 'if c["branch"] == "gate-only":\n        fault(', 'if False:\n        fault('),
    ("G11 cut never starts", G, 'if w and "|".join(k) not in cuts(o) and', "if w and"),
    ("G12 torn line", G, 'p.write_text("".join(y + "\\n" for y in lines[:n]), "utf-8")', "pass"),
    ("G13 repeated row", G, "if r[key] in self.done:\n                    fault", "if False:\n                    fault"),
    ("G14 CAP.json once", G, 'if p.exists():\n        fault("CAP.json exists', 'if False:\n        fault("CAP.json exists'),
    ("G15 gate-only 3.0 h", G, 'gate_only = a.branch == "gate-only"', "gate_only = False"),
    ("G16 host prompt = CC-212", G, 'if {q: D.C.sha(t) for q, (t, _i) in texts[arm].items()} != w["prompt_sha256"][arm]:',
     "if False:"),
    ("G17 zero-shot pin", G, 'if D.C.sha(zs) != w["zs_sha256"] or D.C.sha(zs) != D.C.ZS_PROMPT_SHA256:', "if False:"),
    ("G18 FAULT rc 9", G, "FAULT_RC = 9", "FAULT_RC = 1"),
    ("G19 gate blind pass", G, 'blab, bbad = D.CP.parse_label(blind([D.CP.ver_prompt(P, u["text"])])[0])',
     'blab, bbad = lab, bad'),
    ("S1 degenerate κ", S, "empty = (a + b == 0) | (c + d == 0) | (a + c == 0) | (b + d == 0) | (pe >= 1)",
     "empty = pe >= 1"),
    ("S2 κ CI FAULT", S, 'out["fault"] = bool((~ok).sum() > 0.01 * B_REPS)', 'out["fault"] = False'),
    ("S3 V1 CI bound", S, 'and ci["ci"] is not None and ci["ci"][0] >= V["k_lo"]', ""),
    ("S4 V5 blind = 0", S, '(t["kappa_blind"] if t["kappa_blind"] is not None else 0.0)', '(t["kappa_blind"] or 1.0)'),
    ("S5 V2 inclusive", S, 't["no_rate_present"] <= V["no_p"]', 't["no_rate_present"] < V["no_p"]'),
    ("S6 V4 inclusive", S, 't["uncertain_share"] <= V["unc"]', 't["uncertain_share"] < V["unc"]'),
    ("S7 UPs needs lo > 0", S, "if reject and point > 0 and lo > 0:", "if reject and point > 0:"),
    ("S8 DOWN needs hi < 0", S, "if reject and point < 0 and hi < 0:", "if reject and point < 0:"),
    ("S9 S1 needs ctl UP", S, 'if fc in ("UP", "UPs"):', 'if fc in ("UP", "UPs", "NS"):'),
    ("S10 C state δ", S, 'return prefix + ("1" if hi < 0 and lo <= -delta else', 'return prefix + ("1" if hi < 0 and lo < 0 else'),
    ("S11 GB both", S, 'return "GB" if fa and fb else', 'return "GF" if fa and fb else'),
    ("S12 Holm step-down", S, "stopped = stopped or ps[k] > ALPHA / (m - j)", "stopped = stopped or ps[k] > ALPHA / m"),
    ("S13 p floor", S, "return float((1 + int((np.abs(d) >= abs(d0) - 1e-9).sum())) / (len(swaps) + 1))",
     "return float(int((np.abs(d) >= abs(d0) - 1e-9).sum()) / len(swaps))"),
    ("S14 > 1 % FAULT", S, "if strict and (~ok).sum() > 0.01 * len(reps):", "if False:"),
    ("S15 delete before verdict", S, "if not a.deleted_utc or not end or", "if False and"),
    ("S16 R3 whole branch", S, 'if gate_only and any(v["status"] == "incomplete" for v in rec["verifiers"].values()):',
     "if False:"),
    ("S17 stop = incomplete", S, "if stop or rows is None or", "if rows is None or"),
    ("S18 gate sha", S, "if D.sha(D.dump(units)) != a.gate_sha:", "if False:"),
    ("S19 partial never opened", S, "complete[(b, ds)] = complete_block(sums, b, ds)", "complete[(b, ds)] = True"),
    ("S20 XM release", S, 'if xm.get("release_sha256") != XM_VI_FULL or', "if"),
    ("S21 OV 1,836 keys", S, 'if set(ov) != {r[0] for r in s.lists["sets"]["ov_dev_a"]} | ob:', "if False:"),
    ("S23 family members", S, 'for x in ("ret", "ctl", "rand"):  # the Holm family', 'for x in ("ret", "ctl"):  #'),
    ("S24 ΔP_cm k = min", S, "k = min(len(of), len(orr))", "k = max(len(of), len(orr))"),
    ("S25 OV byte-equal ret + rand (W2)", S, '''            for arm in ("ret", "rand"):  # §5.3 item 1: one share per (backbone, set, arm) (CC-307 W2)
                blk.setdefault("byte_equal_share", {})[arm]''', '''            for arm in ("ret", "rand"):  # §5.3 item 1: one share per (backbone, set, arm) (CC-307 W2)
                pass
            blk.setdefault("byte_equal_share", {})[arm]'''),
    ("S26 cider complete blocks only (W3)", S, "            if not complete_block(sums, b, ds):\n                continue",
     "            if False:\n                continue"),
    ("S27 absolute SUMS path (N2)", S, 'in rel.split("/") or \\\n                rel.startswith("/"):',
     'in rel.split("/") or \\\n                False:'),
    ("T1 TMAN", T, "if D.sha(man) != TMAN:", "if False:"),
    ("T2 T5 prefix", T, "if len(want) != 1 or not want[0].startswith(T5_PREFIX):", "if len(want) != 1:"),
    ("T3 > 1 % FAULT", T, "if bad := faults(tbl):", "if bad := []:"),
    ("T4 3,000 ids only", T, "    for i in ids:\n        si = st.get(i, {})", "    for i in sorted(Q):\n        si = st.get(i, {})"),
    ("T5 T2 = SUMS line", T, "if sums.get(rel) != T[k][1]:", "if False:"),
    ("T6 own nine inputs", T, 'D.allow("t1table", entries, [a.res], helpers=False)', 'D.allow("t1table", entries, [a.res])'),
    ("J1 SUMS after EXIT", J, '  say "EXIT $MODE rc=$rc"\n  [ -z "$MANIFEST" ] || sums > $O/$MANIFEST',
     '  [ -z "$MANIFEST" ] || sums > $O/$MANIFEST\n  say "EXIT $MODE rc=$rc"'),
    ("J2 gate-only push", J, "    || stop \"gate-only push holds more than the gate images and the gate unit file\"", "    || true"),
    ("J3 no data/", J, '[ ! -e data ] || stop', "[ ! -e data ] || true"),
    ("J4 TMAN", J, '= "$TMAN" ] || stop "tmpfs MANIFEST.sha256 differs from TMAN (NB-C3)"', '= "$TMAN" ] || true'),
    ("J5 freeze", J, '[ "$C_DIAG_FREEZE" = "$FZ" ] || stop', '[ "$C_DIAG_FREEZE" = "$FZ" ] || true'),
    ("J6 3 attempts", J, "for n in 1 2 3; do", "for n in 1; do"),
    ("J7 FAULT stops", J, '      9) stop "$name FAULT', '      19) stop "$name FAULT'),
    ("J8 cap stop final", J, '124) final cap_stop "during $name"', '124) stop "during $name"'),
    ("J9 verdict wait", J, "-lt $WAIT_S ] || final idle_stop", "-lt 999999999 ] || final idle_stop"),
    ("J10 money stop", J, 'for m in $FINAL; do [ ! -e $O/$m ] || { MANIFEST=SHA256SUMS_${MODE}_stop; say "${m%.json} (final) '
                          'before $name"; exit 0; }; done', ":"),
    ("J11 trap wipe", J, "  if [ -d $HD ]; then $PY -X utf8 -I -B $X wipe", "  if false; then $PY -X utf8 -I -B $X wipe"),
    ("J15 -X utf8 (W1)", J, "  if [ -d $HD ]; then $PY -X utf8 -I -B $X wipe", "  if [ -d $HD ]; then $PY -I -B $X wipe"),
    ("J16 cap stop in the verdict wait", J, '|| final cap_stop "cap reached during the verdict wait"',
     '|| true "cap reached during the verdict wait"'),
    ("J12 gate SUMS w/o log", J, "! -name job.log ! -name steps.log", "! -name steps.log"),
    ("J13 HEAD", J, '[ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop', '[ "$(git rev-parse HEAD)" = "$EXPECT" ] || true'),
    ("J14 branch vs mode", J, '[ "$BR" = gate-only ] || stop', '[ "$BR" = gate-only ] || true'),
]
PY = os.path.expanduser("~/.venvs/c_pvr_cider/bin/python")


def tree(root: Path) -> Path:
    """root mirrors the repo by symlinks: every top-level entry, scripts/<entry> and scripts/c_diag/<file>."""
    (root / "scripts" / "c_diag").mkdir(parents=True)
    for e in REPO.iterdir():
        if e.name not in ("scripts", ".git"):
            (root / e.name).symlink_to(e)
    for e in (REPO / "scripts").iterdir():
        if e.name != "c_diag":
            (root / "scripts" / e.name).symlink_to(e)
    for f in HERE.iterdir():
        if f.is_file():
            (root / "scripts" / "c_diag" / f.name).symlink_to(f)
    return root / "scripts" / "c_diag"


def scrub(root: Path) -> None:
    """Remove a scratch tree by name: unlink each link and file, rmdir each real dir (no recursive delete)."""
    for top, dirs, files in os.walk(root, topdown=False):
        for f in files:
            os.unlink(os.path.join(top, f))
        for x in dirs:
            q = os.path.join(top, x)
            os.unlink(q) if os.path.islink(q) else os.rmdir(q)
    root.rmdir()


def run(d: Path, f: str) -> tuple[bool, str]:
    if f == J:
        cmd = ["bash", str(d / "c_diag_job_selftest.sh"), str(d / J)]
    else:
        cmd = ["unshare", "-rn", PY, "-X", "utf8", "-I", "-B", str(d / "test_c_diag.py")]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=1500)
    if r.returncode:
        tail = [x for x in (r.stderr + r.stdout).splitlines() if x.strip() and not x.startswith("{")]
        fails = [x for x in tail if x.startswith("FAIL ")]
        return False, (fails[0] if fails else tail[-1] if tail else str(r.returncode))[:110]
    return True, ""


def one(m) -> tuple[str, bool, str]:
    mid, f, old, new = m
    src = (HERE / f).read_text(encoding="utf-8")
    if src.count(old) != 1:
        return mid, True, f"PATTERN NOT FOUND ONCE ({src.count(old)})"
    root = Path(tempfile.mkdtemp(prefix="c_diag_mut_"))
    try:
        d = tree(root)
        (d / f).unlink()
        (d / f).write_text(src.replace(old, new), encoding="utf-8")
        ok, why = run(d, f)
        return mid, ok, why
    finally:
        scrub(root)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    root = Path(tempfile.mkdtemp(prefix="c_diag_mut_"))
    try:
        d = tree(root)
        for f in ("test_c_diag.py", J):
            ok, why = run(d, f)
            assert ok, f"control fails: {f} {why}"
    finally:
        scrub(root)
    print("control: test_c_diag.py and c_diag_job_selftest.sh pass on the unmutated files", flush=True)
    todo = [m for m in MUT if not a.only or m[0].split()[0] in a.only]
    survived = []
    py = [m for m in todo if m[1] != J]
    with ThreadPoolExecutor(a.jobs) as ex:  # the job mutants share /dev/shm/c_diag_hd: one at a time, after
        results = list(ex.map(one, py)) + [one(m) for m in todo if m[1] == J]
    for mid, ok, why in results:
        print(f"{mid}: {'SURVIVED' if ok else 'KILLED'} {why}", flush=True)
        survived += [mid] if ok else []
    print(f"{len(todo) - len(survived)}/{len(todo)} killed; survived: {survived or 'none'}")
    return 1 if survived else 0


if __name__ == "__main__":
    sys.exit(main())
