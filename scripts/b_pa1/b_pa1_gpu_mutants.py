#!/usr/bin/env python3
"""Guard mutants for b_pa1_gpu.py, b_pa1_mid.py, b_pa1_job.sh and b_pa1_d8i_validate.py (DRAFT; the job's runner is b_pa1_job_selftest.sh). The committed mutants.py is only imported (its tree()),
never edited. Each mutant breaks one guard or rule in a scratch copy and must make its file's selftest fail, offline
(unshare -rn), -I -B. Run:  python3 -I -B scripts/b_pa1/b_pa1_gpu_mutants.py
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from mutants import tree  # noqa: E402  scratch scripts/ of symlinks, so common.ROOT stays the repo
from b_pa1_gpu import scratch  # noqa: E402  removes its tree by name and rmdir (no recursive delete)

G, D, J, V = "b_pa1_gpu.py", "b_pa1_mid.py", "b_pa1_job.sh", "b_pa1_d8i_validate.py"
PY = {G: sys.executable, D: "/usr/bin/python3", V: "/usr/bin/python3"}
MUT = [  # (id, file, old, new): each old must occur exactly once
    ("G1 gate >= 0.95", G, 'return share >= Fraction(reg["gate"]["pass_share"])', 'return share > Fraction(reg["gate"]["pass_share"])'),
    ("G2 gate denominator 231", G, "return Fraction(sum(map(is_vn, caps)), n)", "return Fraction(sum(map(is_vn, caps)), max(1, sum(map(bool, caps))))"),
    ("G3 gate lower case", G, 't = unicodedata.normalize("NFD", text.lower())', 't = unicodedata.normalize("NFD", text)'),
    ("G4 gate NFD", G, 't = unicodedata.normalize("NFD", text.lower())', 't = unicodedata.normalize("NFC", text.lower())'),
    ("G5 dot below mark", G, 'VN_MARKS = frozenset("\\u0306\\u0302\\u031b\\u0300\\u0301\\u0309\\u0303\\u0323")', 'VN_MARKS = frozenset("\\u0306\\u0302\\u031b\\u0300\\u0301\\u0309\\u0303")'),
    ("G6 undetermined clashes", G, 'return not (determined(a) and determined(b)) or a["lineage"]["V"]', 'return a["lineage"]["V"]'),
    ("G7 clash on V", G, 'a["lineage"]["V"] == b["lineage"]["V"] or \\\n', ''),
    ("G8 clash on L", G, ' or \\\n        a["lineage"]["L"] == b["lineage"]["L"]', ''),
    ("G9 Rule S <= 8.0e9", G, 'm["safetensors_total"] > reg["rule_s_max_params"]', 'm["safetensors_total"] >= reg["rule_s_max_params"]'),
    ("G10 Rule S needs a total", G, 'if m["safetensors_total"] is None or m["safetensors_total"]', 'if m["safetensors_total"]'),
    ("G11 pin skip", G, 'if not m["files"] or not m["revision"]:', 'if False:'),
    ("G12 stop at 4", G, 'if len(acc) >= reg["gate"]["n_accept"]:\n        rec.update', 'if len(acc) > reg["gate"]["n_accept"]:\n        rec.update'),
    ("G13 gate in walk order", G, 'if reg["walk"].index(key) != len(seen):', 'if False:'),
    ("G14 walk record order", G, 'if order != reg["walk"][:len(order)]:', 'if False:'),
    ("G15 shared ids removed", G, 'y, n = y - (y & n), n - (y & n)', 'y, n = y, n'),
    ("G16 empty Y/N refused", G, 'if not y or not n:', 'if False:'),
    ("G17 abstain = neither set", G, '"abstain": top not in y and top not in n', '"abstain": top not in y'),
    ("G18 p_yes ratio", G, '"p_yes": py / (py + pn) if', '"p_yes": py if'),
    ("G19 digit one token", G, 'if any(len(x) != 1 for x in ids) or len(', 'if len('),
    ("G20 digit distinct", G, 'or len({x[0] for x in ids}) != len(digits):', ':'),
    ("G21 EV renormalised", G, '"ev": sum(d * x for d, x in enumerate(p)) / s if', '"ev": sum(d * x for d, x in enumerate(p)) if'),
    ("G22 proposition types", G, 'for x in items if isinstance(x, dict) and x.get("type") in types and', 'for x in items if isinstance(x, dict) and'),
    ("G23 parse ok", G, 'return props, ("ok" if whole and not bad else', 'return props, ("ok" if whole else'),
    ("G24 trim x1.25", G, 'return Fraction(5, 4) * Fraction(', 'return Fraction(1) * Fraction('),
    ("G25 trim order", G, 'TRIM_ORDER = ("a4", "h", "a3")', 'TRIM_ORDER = ("h", "a4", "a3")'),
    ("G26 trim <= cap left", G, 'if need(kept) <= left:', 'if need(kept) < left:'),
    ("G27 core never trimmed", G, '"core_fits": need([]) <= left', '"core_fits": True'),
    ("G28 A3 projection", G, '"a3": cap4 * (r["e_d2"] + r["v_d2v1"] + r["v_d1v2"])', '"a3": cap4 * (r["e_d2"] + r["v_d2v1"])'),
    ("G29 output key whitelist", G, 'if k not in OUT_KEYS:', 'if False:'),
    ("G30 ids-only values", G, 'if isinstance(x, str) and not ID_RX.fullmatch(x):', 'if False:'),
    ("G31 duplicate row", G, 'if k in self.done:\n            fault', 'if False:\n            fault'),
    ("G32 torn tail kept", G, 'B.write_new(p.with_name(f"{p.name}.torn.{utc()}"), b[cut:])', 'pass'),
    ("G33 torn file refused", G, 'if b and not b.endswith(b"\\n"):\n        fault', 'if False:\n        fault'),
    ("G34 wipe count", G, 'return 0 if len(files) == n_man + 1 else 1', 'return 0'),
    ("G35 wipe log line", G, 'f.write(f"{utc()}\\t{d}\\t{len(files)}\\t{n_man}\\n")', 'pass'),
    ("G36 frame sha", G, 'if sha_bytes(b) != FRAME_SHA:', 'if False:'),
    ("G37 slice-A count", G, 'if len(rows) != N_SLICE or len(want) != N_SLICE or len(names) != N_SLICE:', 'if False:'),
    ("G38 slice order = frame", G, 'rows = [r for r in frame if r[1] in want]', 'rows = [r for f in names for r in frame if r[1] == f]'),
    ("G39 W blocks aligned", G, 'if i < 0 or i % block or', 'if i < 0 or'),
    ("G40 W cap 1.0 GPU-h", G, 'return min(left, W_CAP_SEC - c["used_w_before_sec"] - used_sec(rows, True)) if w else left', 'return left'),
    ("G41 open step refused", G, 'if st and not in_step:', 'if False:'),
    ("G42 ledger one open step", G, 'if st:\n            fault(f"ledger step', 'if False:\n            fault(f"ledger step'),
    ("G43 money stop marker", G, 'FINAL = ("CAP_STOP.json", "MONEY_STOP.json", "PA3.json", "CORE_STOP.json")', 'FINAL = ("CAP_STOP.json", "PA3.json", "CORE_STOP.json")'),
    ("G44 cap 22 or 28", G, 'if a.cap_h not in (22, 28) or', 'if a.cap_h <= 0 or'),
    ("G45 CAP.json once", G, 'B.write_new(O() / "CAP.json", (json.dumps(d, sort_keys=True) + "\\n").encode())', '(O() / "CAP.json").write_bytes((json.dumps(d, sort_keys=True) + "\\n").encode())'),
    ("G46 MAPF hex", G, 'if mode in ("a1score", "rest") and not HEX64.fullmatch(mapf):', 'if False:'),
    ("G47 MAPF fixed for A1-score", G, 'if mp.exists() and mp.read_text().strip() != mapf:', 'if False:'),
    ("G48 rest MAPF = A1-score's", G, 'if (o / "out/a1score/MAPF.txt").read_text().strip() != mapf:', 'if False:'),
    ("G49 H input sha", G, 'if not HEX64.fullmatch(hin) or sha_bytes(hp.read_bytes()) != hin:', 'if False:'),
    ("G50 A4 model only", G, 'if k not in a4_models(reg, acc):', 'if False:'),
    ("G51 PA3 marker", G, 'B.write_new(o / "PA3.json"', 'Path("/dev/null").open'),
    ("G52 PA3 rc", G, '                return PA3_RC\n', '                return 0\n'),
    ("G53 A4 smoke in memory", G, '                mem = Mem()\n', '                mem = Mem()\n                Out(sd / f"a4smoke_{m}.jsonl")\n'),
    ("G54 one resume", G, 'B.write_new(O() / "RESUME.json"', '(lambda p, b: p.write_bytes(b))(O() / "RESUME.json"'),
    ("G55 resume closes open step", G, 'if st and a.close_sec is None:', 'if False:'),
    ("G56 money stop threshold", G, 'if a.balance > a.threshold:', 'if False:'),
    ("G57 A4 = first two of pool", G, 'if k not in accepted][:2]', 'if k not in accepted][:1]'),
    ("G58 ACCEPT holds 4", G, 'if len(a) != reg["gate"]["n_accept"]:\n        fault("ACCEPT.json', 'if False:\n        fault("ACCEPT.json'),
    ("G59 prompt sha", G, 'or sha_bytes(pr["text"].encode()) != pr["sha256"]:', ':'),
    ("G60 decomposer L = verifier L", G, 'if ms[r["decomposer"]]["lineage"]["L"] != ms[r["verifier"]]["lineage"]["L"]:', 'if False:'),
    ("G61 prompt slots", G, '    if slots != set(kw):\n', '    if False:\n'),
    ("G62 verify all types", G, 'if p["type"] in M.reg["verify_types"]:\n                res.append', 'if p["type"] == "object":\n                res.append'),
    ("G63 CLIPScore max(cos, 0)", G, '"score": w * max(cos, 0.0)', '"score": w * cos'),
    ("G64 gate venv per model", G, 'return [(f"s.gate.{k}", ms[k]["venv"]) for k in reg["walk"]]', 'return [(f"s.gate.{k}", "main") for k in reg["walk"]]'),
    ("G65 rest A3 before H", G, 'out += [(f"rest.{s}", "main") for s in ("decomp_d2", "verify_d2v1", "verify_d1v2")] if "a3" in t["kept"] else []',
     'out += [(f"rest.{s}", "main") for s in ("decomp_d2", "verify_d2v1", "verify_d1v2")] if "a3" in t["kept"] and False else []'),
    ("G66 snapshot pin", G, 'if (s256 if kind == "lfs" else s1) != want:', 'if False:'),
    ("G67 no unpinned pickle", G, 'if any(q.suffix in (".bin", ".pt", ".pth", ".ckpt") and q.name not in m["files"] for q in p.iterdir()):', 'if False:'),
    ("G68 git blob form", G, 'hashlib.sha1(b"blob %d\\0" % n)', 'hashlib.sha1()'),
    ("G69 trim uses cap left in step", G, 'trim(project(rates, a4_models(reg, acc)), left_sec(in_step=True))', 'trim(project(rates, a4_models(reg, acc)), 10 ** 9)'),
    ("D1 df distinct per caption", D, 'df.update({t for t in map(norm, toks)', 'df.update([t for t in map(norm, toks)'),
    ("D2 df >= 10", D, 'if n >= MIN_DF)', 'if n > MIN_DF)'),
    ("D3 map terms cover", D, 'if LETTER.search(t) and t not in terms and t not in stop}', 'if LETTER.search(t) and t not in stop}'),
    ("D4 stop list covers", D, 'if LETTER.search(t) and t not in terms and t not in stop}', 'if LETTER.search(t) and t not in terms}'),
    ("D5 letters only", D, 'if LETTER.search(t) and t not in terms', 'if t not in terms'),
    ("D6 (ii) unmapped classes", D, 'if i not in mapped)', ')'),
    ("D7 ACCEPT sha", D, 'if s_sums.get("out/s/ACCEPT.json") != sha(acc_b):', 'if False:'),
    ("D8 only the 4 caption files", D, 'if set(d_sums) != want:', 'if False:'),
    ("D9 caption file sha", D, 'if sha(b) != d_sums[rel]:', 'if False:'),
    ("D10 one row per id", D, 'if any(r.get("cap") != k for r in caps[k]) or len({r["id"] for r in caps[k]}) != len(caps[k]):', 'if False:'),
    ("D11 map freeze pin", D, 'not B.pin_line(log, sha(mb), MV.MAP_NAME, MV.XW_NAME, sha(xb)):', 'False:'),
    ("D12 class list pin", D, 'if c.name != MV.CAT_NAME or sha(b) != mp["categories_sha256"] or not B.pin_line(log, sha(b), MV.CAT_NAME):', 'if False:'),
    ("D13 R7 shas", D, 'if B.K.sha_file(root / rel) != s:', 'if False:'),
    ("D14 out of tree", D, 'if root.resolve() in d.parents and (root / ".session_backup").resolve() not in d.parents:', 'if False:'),
    ("D15 entry provenance", D, 'if not isinstance(who, dict) or not all(', 'if False and not all('),
    ("D16 entry tag", D, 'if e.get("tag") not in ("dictionary", "instrument") or', 'if'),
    ("D17 class in list", D, 'if e.get("o365") not in ids:', 'if False:'),
    ("D18 (i) listed token", D, 'if e["src"] == "i" and v not in tok_i:', 'if False:'),
    ("D19 (ii) listed class", D, 'if e["src"] == "ii" and cid not in cls_ii:', 'if False:'),
    ("D20 add-only term", D, 'if v in terms or v in seen:', 'if v in seen:'),
    ("D21 one per entries file", D, 'if v in terms or v in seen:', 'if v in terms:'),
    ("D22 log terms count", D, 'terms = {norm(t["vi"]) for t in mp["terms"]} | {norm(r["vi"]) for r in logged}', 'terms = {norm(t["vi"]) for t in mp["terms"]}'),
    ("D23 log lines strict", D, 'if not m:\n            raise SystemExit("REFUSED: a line of the amendments', 'if False:\n            raise SystemExit("REFUSED: a line of the amendments'),
    ("D24 coverage of this map", D, 'if cov.get("map_sha256") != sha(mb):', 'if False:'),
    ("D25 terms appended", D, 'terms = mp["terms"] + [', 'terms = [] + mp["terms"][:0] + mp["terms"][::-1] + ['),
    ("D26 crosswalk copied", D, 'B.write_new(out / MV.XW_NAME, xb)', 'B.write_new(out / MV.XW_NAME, xb + b" ")'),
    ("D27 parity1 done first", D, 'if not MV.at(lines, MV.DONE_RE, mp["map_v1_sha256"]):', 'if False:'),
    ("D28 final freeze pin", D, 'if not pins:\n        raise SystemExit("REFUSED: no final-map', 'if False:\n        raise SystemExit("REFUSED: no final-map'),
    ("D29 one start after pin", D, 'if len(starts) != 1 or starts[0] < min(pins):', 'if not starts:'),
    ("D30 parity2 done refused", D, 'if MV.at(lines, DONE2, msha):', 'if False:'),
    ("D31 matcher files", D, 'if MV.r3(log, root) != mp["sources"]:', 'if False:'),
    ("D32 final schema", D, 'if a.map.name != FINAL_NAME or mp.get("schema") != "vsps.b_pa1.map.final" or', 'if'),
    ("D33 parity2 once", D, 'os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)', 'os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)'),
    ("D34 run label", D, '{**MV.record(p), "run": "parity2"}', '{**MV.record(p)}'),
    ("D35 gate 231", D, 'GATE_N = "b_pa1_map_final.json", "coverage.json", 10, 231', 'GATE_N = "b_pa1_map_final.json", "coverage.json", 10, 230'),
    ("D36 H salt", D, 'salt: str = "b-pa1-h2|"', 'salt: str = "b-pa1-h2"'),
    ("D37 lists of this frame", D, 'or lists.get("frame_sha256") != B.K.sha_file(a.frame):', ':'),
    ("D38 punct toggle", D, 'return s.rstrip(".!?…").rstrip() if s and s[-1] in ".!?…" else s + "."', 'return s + "."'),
    ("D39 NFC/NFD toggle", D, 'return unicodedata.normalize("NFD", t) if unicodedata.normalize("NFC", t) == t else unicodedata.normalize("NFC", t)', 'return unicodedata.normalize("NFD", t)'),
    ("D40 tone open cluster only", D, 'r"(?![^\\W\\d_])")', '"")'),
    ("D41 tone keeps quý", D, '(r"(?<![qQ])" if frm[-1] in "yỳýỷỹỵ" else "")', '""'),
    ("D42 seg alignment", D, 'if norm(text[c:c + len(syl)]) != norm(syl):', 'if False:'),
    ("J1 MAN check", J, '[ "$(sha256sum < $HB/$SET/MANIFEST.sha256 | cut -c1-64)" = "$MAN" ] || stop', 'true || stop'),
    ("J2 tmpfs file set", J, '|| stop "tmpfs file set differs from MANIFEST.sha256"', '|| true'),
    ("J3 timeout = CAP STOP", J, '    124) final cap_stop "during $ST" CAP_STOP.json "CAP STOP";;', '    124) stop "x";;'),
    ("J4 resume needs RESUME.json", J, '[ -e $O/RESUME.json ] || stop "previous $RK run', 'true || stop "previous $RK run'),
    ("J5 one resume", J, '( set -C; echo "$RK $(ts)" > $O/RESUME_USED ) 2>/dev/null || stop', 'true || stop'),
    ("J6 trap closes the ledger step", J, 'if [ -n "$STEP" ]; then $PYM -I -B $X ledger end', 'if false; then $PYM -I -B $X ledger end'),
    ("J7 HEAD = H_B", J, '[ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop', 'true || stop'),
    ("J8 final markers", J, 'for m in $FINAL; do [ ! -e $O/$m ] || stop "$m exists: final"; done', 'true'),
    ("J9 hostcheck on this GPU", J, ' or d["gpu_uuid"] != sys.argv[4])', ')'),
    ("J10 E-12 status line", J, '[ "$MODE" != s ] || say "E1 E2 NOT RUN (pre-fixed, R5 E-12)"', 'true'),
    ("J11 finished run refused", J, '[ ! -e $O/RUN.$RK.done ] || stop "run $RK is already done"', 'true'),
    ("J12 H sha when H kept", J, 'then stop "TRIM keeps H: EXTRA = h_input.jsonl sha"; fi', 'then true; fi'),
    ("J13 trap wipe", J, 'if [ -d $HB/$SET ]; then $PYM -I -B $X wipe', 'if false; then $PYM -I -B $X wipe'),
    ("J14 SUMS checks", J, '(cd $B && sha256sum --quiet -c SHA256SUMS && sha256sum --quiet -c SHA256SUMS_GPU) || stop', 'true || stop'),
    ("J15 clean tree", J, 'git diff --quiet HEAD -- || stop', 'true || stop'),
    ("J16 MAPF hex", J, 'a1score|rest) [[ $MAPF =~ ^[0-9a-f]{64}$ ]] || stop', 'a1score|rest) true || stop'),
    ("J17 W1 forward TERM to the step", J, 'kill -TERM -- -$SPID 2>/dev/null || kill -TERM $SPID 2>/dev/null || true; ', ''),
    ("J18 W2 early 137 not final", J, '[ $EL -lt $LEFT ] || final cap_stop', 'false || final cap_stop'),
    ("J19 W2 late 137 final", J, '[ $EL -lt $LEFT ] || final cap_stop', 'true || final cap_stop'),
    ("J20 W3 rc 13 stops (HM9)", J, '    13) [ -e $O/CORE_STOP.json ] ||', '    13) continue; [ -e $O/CORE_STOP.json ] ||'),
    ("J21 W3 job writes CORE_STOP", J, '"$ST" "$(ts)" > $O/CORE_STOP.json', '"$ST" "$(ts)" > /dev/null'),
    ("J22 W3 CORE_STOP in the job list", J, 'FINAL="CAP_STOP.json MONEY_STOP.json PA3.json CORE_STOP.json"', 'FINAL="CAP_STOP.json MONEY_STOP.json PA3.json"'),
    ("J23 W3 registered mode order", J, '[ -z "$PREV" ] || [ -e $O/RUN.$PREV.done ] || stop', 'true || stop'),
    ("J24 HM8 LEFT > 0", J, '[ "$LEFT" -gt 0 ] || final cap_stop "cap reached before $ST"', 'true || final cap_stop "cap reached before $ST"'),
    ("J25 HM10 W uses left --w", J, 'if [ "$V" = w ]; then LEFT=$($PYM -I -B $X left --w); else', 'if [ "$V" = w ]; then LEFT=$($PYM -I -B $X left); else'),
    ("J26 N3 markers in the loop", J, '[ ! -e $O/$m ] || { n=${m%.json}; MANIFEST=', 'true || { n=${m%.json}; MANIFEST='),
    ("J27 N4 final stop manifest", J, '"$(ts)" > $O/$3; MANIFEST=SHA256SUMS_${RK}_stop; say', '"$(ts)" > $O/$3; say'),
    ("J28 N5 host_w25.sums required", J, '[ -s host_w25.sums ] && sha256sum --quiet -c host_w25.sums', '[ ! -e host_w25.sums ] || sha256sum --quiet -c host_w25.sums'),
    ("J29 N2 stdin /dev/null", J, '--hin $EXTRA < /dev/null >> $LOG/steps.log 2>&1 &;;\n    legacy)', '--hin $EXTRA >> $LOG/steps.log 2>&1 &;;\n    legacy)'),
    ("G70 W3 CORE_STOP in markers", G, 'FINAL = ("CAP_STOP.json", "MONEY_STOP.json", "PA3.json", "CORE_STOP.json")', 'FINAL = ("CAP_STOP.json", "MONEY_STOP.json", "PA3.json")'),
    ("G71 W3 trim writes CORE_STOP", G, 'B.write_new(o / "CORE_STOP.json"', 'Path("/dev/null").open'),
    ("G72 W3 later blocks need core_fits", G, 'if t.get("core_fits") is not True:', 'if False:'),
    ("G73 N8 complete inputs", G, '        if len(rows) != n:\n', '        if False:\n'),
    ("G74 N13 hourly near the threshold", G, 'return 1 if balance - threshold <= 6 * burn else 6', 'return 6'),
    ("G75 HM5 money stop at the threshold", G, 'if a.balance > a.threshold:', 'if a.balance >= a.threshold:'),
    ("G76 HM1 ledger seconds", G, '"sec": max(1, int(time.monotonic() - st["m"]) + 1),', '"sec": 1,'),
    ("G77 HM2 used_before counts", G, 'left = c["cap_sec"] - c["used_before_sec"] - used_sec(rows)', 'left = c["cap_sec"] - used_sec(rows)'),
    ("G78 HM3 in-step elapsed counts", G, '- (int(time.monotonic() - st["m"]) + 1 if st else 0)', '- 0'),
    ("J30 W2 elapsed on the monotonic clock", J, '  EL=$(( $(mono) - T0S ))', '  EL=0'),
    ("J31 N-b the trap waits for the step", J, '|| true; wait $SPID 2>/dev/null || true; fi', '|| true; fi'),
    ("J32 N-a money marker then TERM is final", J, 'if [ $rc = 143 ] && [ -e $O/MONEY_STOP.json ]; then', 'if false; then'),
    ("J33 manifest after the EXIT line", J, '  say "EXIT $MODE rc=$rc"\n  [ -z "$MANIFEST" ] || sums > $O/$MANIFEST', '  [ -z "$MANIFEST" ] || sums > $O/$MANIFEST\n  say "EXIT $MODE rc=$rc"'),
    ("J34 done mode writes its manifest", J, 'MANIFEST=SHA256SUMS_$MODE   #', 'true   #'),
    ("J35 W9 (a) teardown ignores signals", J, "local rc=$?; trap '' TERM HUP INT PIPE", 'local rc=$?'),
    ("J36 W9 (b) say survives a dead console", J, 'say() { local l; l="$(ts) $*"; echo "$l" >> $LOG/job.log; echo "$l" 2>/dev/null || true; }', 'say() { echo "$(ts) $*" | tee -a $LOG/job.log; }'),
    ("J37 N-f HM28 money line needs the marker", J, 'if [ $rc = 143 ] && [ -e $O/MONEY_STOP.json ]; then', 'if [ $rc = 143 ]; then'),
    ("J38 N-f HM32 PA3 stop manifest", J, '    3) MANIFEST=SHA256SUMS_${RK}_stop; say "PA3 STOP', '    3) say "PA3 STOP'),
    ("G79 HM4 cap-init --used-sec", G, '"used_before_sec": a.used_sec,', '"used_before_sec": 0,'),
    ("D44 W5 instrument needs the amendment", D, 'if e["tag"] == "instrument" and not inst_ok:', 'if False:'),
    ("D45 W5 amendment LOG pin", D, 'bool(B.pin_line(log, str(am.get("sha256", "")), str(am.get("name", ""))))', 'True'),
    ("D46 W5 registry mode", D, 'return reg["instrument_llm"].get("mode") == INSTRUMENT_MODE and isinstance(am, dict)', 'return isinstance(am, dict)'),
    ("D47 W5 drafter id", D, 'not DRAFTER_RE.fullmatch(str(e.get("drafter", "")))', 'False'),
    ("D48 W5 drafter logged", D, "drafter={e['drafter']} vi=", "drafter=- vi="),
    ("D49 W7 entries file LOG pin", D, 'if not B.pin_line(log, sha(ent_b), a.entries.name):', 'if False:'),
    ("D50 N-c coverage checks its own root", D, 'out = outside_tree(a.out_dir, root)\n    mp, mb, _, _', 'out = outside_tree(a.out_dir)\n    mp, mb, _, _'),
    ("J39 F-1 a1decode manifest names the 4 caption files", J, '(cd $O && sha256sum $NARROW) > $O/SHA256SUMS_a1decode', 'sums > $O/SHA256SUMS_a1decode'),
    ("J40 F-1 no glob over out/a1decode", J, """NARROW=$(echo "$STEPS" | sed -n 's|^a1decode\\.decode\\.\\([^ ]*\\) .*$|out/a1decode/captions_\\1.jsonl|p')""", 'NARROW=$(cd $O && find out/a1decode -type f | LC_ALL=C sort)'),
    ("J41 F-1 a1decode full manifest _all", J, '  MANIFEST=SHA256SUMS_a1decode_all   #', '  MANIFEST=   #'),
    ("J42 F-4 UTF-8 mode in the job interpreters", J, 'PYM="$HOME/venvs/b_pa1_main_$LKM/bin/python -X utf8"; PYL="$HOME/venvs/b_pa1_legacy_$LKL/bin/python -X utf8"; PYW="$HOME/venvs/b_pa1_w/bin/python -X utf8"',
     'PYM=$HOME/venvs/b_pa1_main_$LKM/bin/python; PYL=$HOME/venvs/b_pa1_legacy_$LKL/bin/python; PYW=$HOME/venvs/b_pa1_w/bin/python'),
    ("G80 F-3 cap-init stores --used-w-sec", G, '"used_w_before_sec": a.used_w_sec,', '"used_w_before_sec": 0,'),
    ("G81 F-3 left --w subtracts HB-T1's W seconds", G, 'W_CAP_SEC - c["used_w_before_sec"] - used_sec(rows, True)', 'W_CAP_SEC - used_sec(rows, True)'),
    ("G82 F-3 0 <= used_w_sec <= used_sec", G, 'not 0 <= a.used_w_sec <= a.used_sec:', 'a.used_sec < 0:'),
    ("V1 F-2 the (i) amend runs", V, 'r1 = run(M.cmd_amend, ns(ei), d / "LOG.md")', 'r1 = ("ok", json.dumps({"added": n1}))'),
    ("V2 F-2 (ii) before (i)", V, 'r2 = run(M.cmd_amend, ns(eii), d / "LOG.md")\n        r1 = run(M.cmd_amend, ns(ei), d / "LOG.md")', 'r1 = run(M.cmd_amend, ns(ei), d / "LOG.md")\n        r2 = run(M.cmd_amend, ns(eii), d / "LOG.md")'),
    ("V3 F-2 the (i) pin line on the scratch LOG", V, 'log.read_text(encoding="utf-8") + line + "\\n"', 'log.read_text(encoding="utf-8")'),
    ("V4 F-2 computed RESULT", V, "RESULT {'PASS' if not bad else 'FAIL ' + ','.join(bad)}", "RESULT PASS"),
    ("V5 F-2 file name", V, '"name": ei.name == EN_I,', '"name": True,'),
    ("V6 F-2 provenance = md v1.3", V, '"provenance": (doc_i.get("provenance") or {}).get("amendment") ==', '"provenance": True or (doc_i.get("provenance") or {}).get("amendment") =='),
    ("V7 F-2 src i only", V, '"src_i": n1 > 0 and all(e.get("src") == "i" for e in doc_i["entries"]),', '"src_i": n1 > 0,'),
    ("V8 F-2 pulled coverage", V, '"pulled_coverage": cv.get("classes_only") is False}', '"pulled_coverage": True}'),
    ("V9 F-2 (A)+(B) on the LOG", V, '"ab_on_log": B.pin_line(log, ms, MD) and', '"ab_on_log": True or'),
    ("V10 F-2 final count", V, 'ok["final"] = fm["n_added"] == n1 + n2 and', 'ok["final"] = True or'),
    ("D43 case toggle", D, 'return t.lower() if t != t.lower() else t[:1].upper() + t[1:]', 'return t.lower()'),
]


def run(d: Path, f: str) -> tuple[bool, str]:
    cmd = ["bash", "b_pa1_job_selftest.sh", str(d / J)] if f == J else ["unshare", "-rn", PY[f], "-I", "-B", f, "selftest"]
    r = subprocess.run(cmd, cwd=d, capture_output=True, text=True, timeout=900)
    if r.returncode:
        tail = [x for x in (r.stderr or r.stdout).splitlines() if x.strip()]
        return False, tail[-1][:110] if tail else str(r.returncode)
    return True, ""


def main() -> int:
    with scratch("b_pa1_gpu_mut_") as root:
        d = tree(root)
        for f in (G, D, J, V):
            ok, why = run(d, f)
            assert ok, f"control fails: {f} {why}"
        print("control: the four selftests pass on the unmutated files", flush=True)
        survived = []
        for mid, f, old, new in MUT:
            src = (HERE / f).read_text(encoding="utf-8")
            if src.count(old) != 1:
                print(f"{mid}: PATTERN NOT FOUND ONCE ({src.count(old)})")
                survived.append(mid)
                continue
            (d / f).unlink()
            (d / f).write_text(src.replace(old, new), encoding="utf-8")
            ok, why = run(d, f)
            print(f"{mid}: {'SURVIVED' if ok else 'KILLED'} {why}", flush=True)
            survived += [mid] if ok else []
            (d / f).unlink()
            (d / f).symlink_to(HERE / f)
        print(f"{len(MUT) - len(survived)}/{len(MUT)} killed; survived: {survived or 'none'}")
        return 1 if survived else 0


if __name__ == "__main__":
    sys.exit(main())
