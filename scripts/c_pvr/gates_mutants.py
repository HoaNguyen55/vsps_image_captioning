#!/usr/bin/env python3
"""CC-222 round-3 / CC-227 mutant harness for scripts/c_pvr/gates.py. Usage: python3 -I this.py <gates.py> <scratch dir>.
Each mutant replaces one exact string (it must occur once) and runs `selftest` on the copy. A mutant is KILLED when
the selftest fails before its final real-pin check (copies outside the repo always fail that check, so a failure that
is only that check counts as SURVIVED). EQUIV lists mutants proven equivalent; they are run and expected to survive.
PINS-B (B) (CC-239 W3, Q-B9, Q-B13): rows g1_..g24_ (PINS-B G-row in the name), qb7_ and gb_ follow the 68 rows of
CC-227; those 68 and their targets are unchanged. Every copy runs in the W3 sandbox: `unshare -rnm` (loopback-only
network, private tmpfs on /dev/shm), env -i with HOME and TMPDIR on the ext4 scratch dir, which must not lie under
/mnt or contain a BARRED word (a REFUSED copy path would be a false kill). A copy that exceeds TIMEOUT s is
TIMEOUT and counts as killed (a mutant that drops LOCK_NB deadlocks on the lock-held case). JOBS copies run at once."""
import re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
M = {
 "no_context_byte": ("        keep = cut - 1  # one byte of look-behind context", "        keep = cut"),
 "hex_no_lookbehind": ('HEX_RX = re.compile(rb"(?<![0-9a-fA-F])[0-9a-fA-F]{16}(?![0-9a-fA-F])")', 'HEX_RX = re.compile(rb"[0-9a-fA-F]{16}(?![0-9a-fA-F])")'),
 "hex_lowercase_only": ('HEX_RX = re.compile(rb"(?<![0-9a-fA-F])[0-9a-fA-F]{16}(?![0-9a-fA-F])")', 'HEX_RX = re.compile(rb"(?<![0-9a-f])[0-9a-f]{16}(?![0-9a-f])")'),
 "tail_4096": ("TAIL = 1 << 20", "TAIL = 4096"),
 "cut_no_check": ("                if m.start() >= cut:\n                    break\n", ""),
 "no_other_fault": ("    if other:\n", "    if False:\n"),
 "no_oi_oiv7_fault": ('    if oi_test & s["oiv7"]:\n', "    if False:\n"),
 "no_mixed_rule": ("        if 0 < nh < n:", "        if False:"),
 "no_annotations_guard": ("not extra <= INFO_TOP_STR", "False"),
 "cc227_any_type_value": ("or any(not isinstance(d[k], str) or len(d[k]) > 64 for k in extra)", "or False"),
 "cc227_no_len_cap": ("not isinstance(d[k], str) or len(d[k]) > 64", "not isinstance(d[k], str)"),
 "cc227_no_str_check": ("not isinstance(d[k], str) or len(d[k]) > 64", "len(d[k]) > 64"),
 "cc227_type_in_top": ('INFO_TOP = {"images", "licenses", "info"}', 'INFO_TOP = {"images", "licenses", "info", "type", "foo"}'),
 "cc227_schema_no_sha": ("    if sha_bytes(b) != info_sha:\n", "    if False:\n"),
 "cc227_len_ge_64": ("len(d[k]) > 64", "len(d[k]) >= 64"),
 "cc227_schema_values": ('return {"type": type(v).__name__, ', 'return {"v": v, "type": type(v).__name__, '),
 "no_xm_removal": ("    removed = xm_hit | ", "    removed = "),
 "no_vi_rule": ('sets[vs] = "UNCHECKABLE" if vi.get(tok, 0) else "CLEAN"', 'sets[vs] = "CLEAN"'),
 "vi_no_variants": ('VI_RX = re.compile(rb"(?i)open[_-]?vivqa|vi[_-]?textcaps|viet?cap")', 'VI_RX = re.compile(rb"(?i)openvivqa|vitextcaps|viecap")'),
 "no_sha_check_scan": ('    if n[0] != spec["size"] or h.hexdigest() != spec["sha256"]:', "    if False:"),
 "no_refuse": ("    if BARRED.search(str(p)):", "    if False:"),
 "no_verify_cmp": ('    if sha_bytes(rem) != rec["ga_remaining_sha256"] or sha_file(out / "ga_remaining_ids.txt") != sha_bytes(rem):', "    if False:"),
 "no_undetermined": ('origin in ("OI", "undetermined")', 'origin in ("OI",)'),
 "flickr_server_required": ('rb"(?:\\d+" + SEP + rb"){0,2}(\\d+)[_.]"', 'rb"(?:\\d+" + SEP + rb"){1,2}(\\d+)[_.]"'),
 "flickr_one_segment": ('rb"(?:\\d+" + SEP + rb"){0,2}(\\d+)[_.]"', 'rb"(?:\\d+" + SEP + rb"){0,1}(\\d+)[_.]"'),
 "flickr_no_escape": ('SEP = rb"(?:\\\\?/|%2[Ff])"', 'SEP = rb"(?:/|%2[Ff])"'),
 "flickr_no_pct": ('SEP = rb"(?:\\\\?/|%2[Ff])"', 'SEP = rb"(?:\\\\?/)"'),
 "flickr_host_eq_parse": ('        elif rec["n_flickr_static"] < FLICKR_FLOOR * rec["n_flickr_host"]:', '        elif rec["n_flickr_static"] != rec["n_flickr_host"]:'),
 "no_flickr_floor": ('        elif rec["n_flickr_static"] < FLICKR_FLOOR * rec["n_flickr_host"]:', "        elif False:"),
 "no_flickr_min": ('        if rec["n_flickr_static"] < spec["flickr_min"]:', "        if False:"),
 "no_nkey0": ('    if rec["n_key"] == 0:', "    if False:"),
 "no_int_value": ("|-?\\d+|null)'),", "|null)'),"),
 "list_cap_16": ("){0,128}\\]|'", "){0,16}\\]|'"),
 "census_depth3": ('key = re.sub(r"[0-9]", "#", d) if d', 'key = re.sub(r"[0-9]", "#", "/".join(d.split("/")[:3])) if d'),
 "census_digit_segment": ('key = re.sub(r"[0-9]", "#", d) if d', 'key = "/".join("#" if x.isdigit() else x for x in d.split("/")) if d'),
 "no_bare_key": ('else "~" + re.sub(r"[0-9]", "#", stem)', 'else ""'),
 "w8_no_dotslash": ('    if d and key.startswith("~"):', "    if False:"),
 "shortest_prefix": ("prefixes[max(hit, key=len)]", "prefixes[min(hit, key=len)]"),
 "w1_ids_first": ('    write_once(out / "ga_counts.json", jdump(counts))\n    write_once(out / "ga_remaining_ids.txt", rem)', '    write_once(out / "ga_remaining_ids.txt", rem)\n    write_once(out / "ga_counts.json", jdump(counts))'),
 "w1_no_counts_refuse": ('    for name in ("ga_remaining_ids.txt", "ga_counts.json"):\n        if (out / name).exists():', '    for name in ("ga_remaining_ids.txt",):\n        if (out / name).exists():'),
 "w1_verify_no_partial": ('    if not (out / "ga_counts.json").exists() or not (out / "ga_remaining_ids.txt").exists():', "    if False:"),
 "w9_no_verify": ("    rem_sha = gate_a_verify(root, ga, pins, strict)", '    rem_sha = sha_file(out / "ga_remaining_ids.txt")'),
 "hit_not_final": ('noc = "HIT" if hits else "UNCHECKABLE" if reasons else "CLEAN"', 'noc = "UNCHECKABLE" if reasons else "HIT" if hits else "CLEAN"'),
 "no_unpinned_key": ('                reasons += [f"{f}: unpinned image-like key', '                reasons += [] and [f"{f}: unpinned image-like key'),
 "no_record_count": ('                if want is not None and s["n_records"] != want:', "                if False:"),
 "no_retry_cap": ('sum(a["kind"] == "transport" for a in att) >= MAX_TRANSPORT', "False"),
 "content_not_final": ('closed = any(a["kind"] == "content" for a in att) or', "closed = False or"),
 "no_doc_decided_scan": ("    if doc_decided(prov, key):", "    if False:"),
 "no_origin_check": ('            if comp.get("origin") not in ORIGINS:', "            if False:"),
 "no_cite_check": ('            if not comp.get("cites") or any(ci.split()[0] not in src for ci in comp["cites"]):', "            if False:"),
 "no_crawl_check": ('            if comp["origin"] == "web" and not comp.get("crawl"):', "            if False:"),
 "no_remap_check": ('            if set(mp) & set(t["prefixes"]):', "            if False:"),
 "no_map_barred": ("            if any(MAP_BARRED.search(k) for k in mp):", "            if False:"),
 "no_prov_pin": ('    prov = json.loads(pinned(root, "prov", pins).read_text())', '    prov = json.loads((root / pins["prov"][0]).read_text())'),
 "landing_single": ("out.setdefault((m.group(1) or m.group(2)).decode(), set()).add(r[0])", "out[(m.group(1) or m.group(2)).decode()] = {r[0]}"),
 "pin_no_firstbyte": ('    if first != b"{" or (strict and ip.stat().st_size != INFO["size"]):', '    if strict and ip.stat().st_size != INFO["size"]:'),
 "w2_no_validation": ("            scans[f] = valid_scan(p, f, sft[f])", "            scans[f] = json.loads(p.read_text())"),
 "w2_no_mode": ("    if p.stat().st_mode & 0o222:", "    if False:"),
 "w2_no_label": ('want = {"label": LABEL, "file": key,', 'want = {"file": key,'),
 "w2_no_file": ('"label": LABEL, "file": key, "sha256"', '"label": LABEL, "sha256"'),
 "w2_no_sha": ('"file": key, "sha256": spec["sha256"], "size"', '"file": key, "size"'),
 "w2_no_size": ('"size": spec["size"], "url": spec["url"],', '"url": spec["url"],'),
 "w2_no_url": ('"url": spec["url"],\n            "gates_sha256"', '\n            "gates_sha256"'),
 "w2_no_gates_sha": ('            "gates_sha256": sha_file(Path(__file__))}\n    bad', '            }\n    bad'),
 "w3_narrow_keys": ("""KEY_RX = re.compile(rb'"((?:[^"\\\\]|\\\\.){0,256})"\\s*:')""", """KEY_RX = re.compile(rb'"([A-Za-z0-9_]{0,256})"\\s*:')"""),
 "w3_no_decode": ("""                        kname = json.loads(b'"' + m.group(1) + b'"')""", "                        kname = m.group(1).decode()"),
 "w7_no_mirror": ('    access_log(gc2.parent, f"gate-c2 FAULT {kind}", key, f"attempt {len(att)}")\n', ""),
 "w7_no_reset_check": ('    if logged["content"] > sum(a["kind"] == "content" for a in att) or \\\n', '    if False and \\\n'),
 'g1_no_verify': ('    if gate_a_verify(root, env["ga"], pins, strict=strict) != pins_b["ga_rem"][1]:', '    if False:'),
 'g2_no_counts_check': ('    for p in (env["out"] / "gb_counts.json", sealed / "gb_intermediate.json", sealed / "gb_start", env["shm"]):', '    for p in (sealed / "gb_intermediate.json", sealed / "gb_start", env["shm"]):'),
 'g2_no_sealed_check': ('    for p in (env["out"] / "gb_counts.json", sealed / "gb_intermediate.json", sealed / "gb_start", env["shm"]):', '    for p in (env["out"] / "gb_counts.json", sealed / "gb_start", env["shm"]):'),
 'g2_no_shm_check': ('    for p in (env["out"] / "gb_counts.json", sealed / "gb_intermediate.json", sealed / "gb_start", env["shm"]):', '    for p in (env["out"] / "gb_counts.json", sealed / "gb_intermediate.json", sealed / "gb_start"):'),
 'g3_no_gates_sha': ('    if sha_file(Path(__file__)) != gates_sha:', '    if False:'),
 'g3_sums_line_any': ('    if own != [gates_sha]:', '    if False:'),
 'g3_no_sums_verify': ('        fault(f"SHA256SUMS: {len(bad)} line(s) do not verify")', '        pass'),
 'g3_no_pins_b': ('    for k in pins_b:\n        pinned(root, k, pins_b)', '    for k in pins_b:\n        pass'),
 'g4_no_head_cmp': ('            if bmd5 != rec_md5[s]:', '            if False:'),
 'g4_no_stream_cmp': ('            if r["md5"] != bmd5 or r["md5"] != rec_md5[s]:', '            if False:'),
 'g4_sha_unfed': ('        h.update(b)\n        m.update(b)', '        m.update(b)'),
 'g4_md5_unfed': ('        h.update(b)\n        m.update(b)', '        h.update(b)'),
 'g4_no_length': ('            if r["bytes"] != clen:', '            if False:'),
 'g5_keep_all': ('        elif rec.split(b",", 1)[0] in keep:', '        elif True:'),
 'g5_key_third': ('        elif rec.split(b",", 1)[0] in keep:', '        elif rec.split(b",")[2] in keep:'),
 'g6_no_val_assert': ('            if s == "val" and r["kept"]:', '            if False:'),
 'g7_mixed_pos': ('        labels[img] = {"pos": sorted(m for m, v in seen[img].items() if v == {1}),', '        labels[img] = {"pos": sorted(m for m, v in seen[img].items() if 1 in v),'),
 'g7_mixed_neg': ('                       "neg": sorted(m for m, v in seen[img].items() if v == {0})}', '                       "neg": sorted(m for m, v in seen[img].items() if 0 in v)}'),
 'g7_absent_first': ('    if c_map["pos"] & pos:\n        return "present"\n    return "absent" if c_map["neg"] & neg else "unknown"', '    if c_map["neg"] & neg:\n        return "absent"\n    return "present" if c_map["pos"] & pos else "unknown"'),
 'g7_no_conflict_count': ('        conflicts += sum(len(v) > 1 for v in seen[img].values())', '        conflicts += 0'),
 'g8_no_once_check': ('        bad = [n for n in v["pos"] + v["neg"] if len(mids.get(n, [])) != 1]', '        bad = [n for n in v["pos"] + v["neg"] if not mids.get(n)]'),
 'g8_no_skip_note': ('        if c.startswith("_"):\n            continue\n        bad = [n for n in v["pos"]', '        if False:\n            continue\n        bad = [n for n in v["pos"]'),
 'g9_no_manifest_cmp': ('    bad = sorted(k for k in want if cov[k] != want[k] or cov[k] != man.get(k))', '    bad = sorted(k for k in want if cov[k] != want[k])'),
 'g9_no_const_cmp': ('    bad = sorted(k for k in want if cov[k] != want[k] or cov[k] != man.get(k))', '    bad = sorted(k for k in want if cov[k] != man.get(k))'),
 'g9_no_ppc_cmp': ('    if bad or ppc != man.get("pairs_per_class"):', '    if bad:'),
 'g9_no_parity_in_gb': ('    parity(root, pins, pins_b, a12, want)  # P2 in code (W11)', '    pass'),
 'g10_ppc_emitted': ('               "sealed_sha256": sealed_sha}', '               "sealed_sha256": sealed_sha, "pairs_per_class": {}}'),
 'g10_no_key_check': ('    if set(rec) != GB_KEYS or', '    if False and set(rec) != GB_KEYS or'),
 'g11_indent': ('    return (json.dumps(d, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\\n").encode()', '    return (json.dumps(d, sort_keys=True, indent=1, ensure_ascii=True) + "\\n").encode()'),
 'g11_mode_444': ('        sealed_sha = write_new(sealed_p, sealed_bytes(st), 0o400, check_mode=True)', '        sealed_sha = write_new(sealed_p, sealed_bytes(st), 0o444, check_mode=True)'),
 'g11_link_replace': ('            os.link(tmp, p)', '            os.replace(tmp, p)'),
 'g12_no_pause': ('    if why:\n        return why\n', ''),
 'g12_no_foreign': ('    if foreign_jobs(env["proc"], os.getpid()):', '    if False:'),
 'g12_no_backup': ('    if not env["backup"].is_file() or b"/dev/shm" in env["backup"].read_bytes():', '    if False:'),
 'g12_lock_ignored': ('        fault("tenancy: the G-B lock is held; G-B does not start")', '        pass'),
 'g12_no_shm_mode': ('        if not stat.S_ISDIR(s.st_mode) or s.st_mode & 0o777 != 0o700 or s.st_uid != os.getuid():', '        if False:'),
 'g12_no_initial': ('    if why:\n        fault(f"tenancy: {why}; G-B does not start")', '    if False:\n        pass'),
 'g13_no_cleanup': ('        try:\n            _gb_cleanup(env, procs, written, sealed)\n        except', '        try:\n            pass\n        except'),
 'g13_no_unlink_row': ('            access_log_sync(sealed, "gate-b unlink", f, sha)', '            pass'),
 'g13_no_kill': ('        if p.poll() is None:', '        if False:'),
 'g13_no_abort_row': ('                access_log_sync(sealed, f"gate-b abort {code}", "-", gates_sha)', '                pass'),
 'g14_allow_any': ('    if rp not in allowed:', '    if False:'),
 'g14_no_allow_sha': ('    if sha_bytes(b) != allowed[rp]:', '    if False:'),
 'g15_output_file': ('               "--max-redirs", "3", "-A", "vsps-research")', '               "--max-redirs", "3", "-A", "vsps-research", "-o", "/tmp/x")'),
 'g15_no_proto': ('CURL_STREAM = ("/usr/bin/curl", "-q", "-sS", "--fail", "-L", "--proto", "=https", "--proto-redir", "=https",', 'CURL_STREAM = ("/usr/bin/curl", "-q", "-sS", "--fail", "-L", "--proto-redir", "=https",'),
 'g15_head_insecure': ('CURL_HEAD = ("/usr/bin/curl", "-q", "-sS", "-I", "--fail", "--proto", "=https")', 'CURL_HEAD = ("/usr/bin/curl", "-q", "-sS", "-I", "-k", "--fail", "--proto", "=https")'),
 'g15_no_q_first': ('CURL_STREAM = ("/usr/bin/curl", "-q", "-sS",', 'CURL_STREAM = ("/usr/bin/curl", "-sS", "-q",'),
 'g15_stderr_open': ('stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,\n', 'stdout=subprocess.PIPE, stderr=None,\n'),
 'g15_env_inherit': ('                            env=CURL_ENV)', '                            env=None)'),
 'g16_test_url': ('OI_TEST_URL = "https://open-images-dataset.s3.amazonaws.com/test/{file}"', 'OI_TEST_URL = "https://open-images-dataset.s3.amazonaws.com/validation/{file}"'),
 'g17_no_marker_check': ('    for p in (env["out"] / "gb_counts.json", sealed / "gb_intermediate.json", sealed / "gb_start", env["shm"]):', '    for p in (env["out"] / "gb_counts.json", sealed / "gb_intermediate.json", env["shm"]):'),
 'g17_no_row_check': ('    if log.exists() and any(x.split("\\t")[2:3] == ["gate-b start"] for x in log.read_text().splitlines()):', '    if False:'),
 'g17_no_marker': ('    write_new(marker, f"{utc()}\\t{gates_sha}\\n".encode(), 0o400, check_mode=True)  # W1, before the first byte', '    pass'),
 'g17_no_start_row': ('    access_log_sync(sealed, "gate-b start", marker, gates_sha)', '    pass'),
 'g18_print_error': ('        code = GB_RC[e.code] if isinstance(e, GBAbort) else GB_RC["internal"]', '        code = GB_RC[e.code] if isinstance(e, GBAbort) else GB_RC["internal"]\n        print(repr(e), file=sys.stderr)'),
 'g18_catch_exception_only': ('    except BaseException as e:  # noqa: B036 - W2: every failure after the marker is silent', '    except Exception as e:'),
 'g18_reraise_field': ('        except (csv.Error, ValueError, TypeError, KeyError):\n            raise GBAbort("label_row") from None', '        except (csv.Error, ValueError, TypeError, KeyError):\n            raise'),
 'g18_no_header_check': ('            if rd.fieldnames != LABEL_HEADER:', '            if False:'),
 'g18_no_foreign_id': ('                if img not in ids:', '                if False:'),
 'g19_real_shm': ('"shm": d / "shm/c_pvr_gb",', '"shm": SHM_GB,'),
 'g19_no_spawn_stub': ('    subprocess.Popen = _no_spawn  # type: ignore[assignment,misc]', '    pass'),
 'g20_no_file_fsync': ('            f.flush()\n            os.fsync(f.fileno())\n        os.chmod(tmp, mode)', '            f.flush()\n        os.chmod(tmp, mode)'),
 'g20_no_dir_fsync': ('                os.fsync(dfd)', '                pass'),
 'g20_no_log_fsync': ('        f.flush()\n        os.fsync(f.fileno())\n\n\ndef pause_ok', '        f.flush()\n\n\ndef pause_ok'),
 'g20_no_reread': ('        if sha_bytes(p.read_bytes()) != sha_bytes(data) or (check_mode and p.stat().st_mode & 0o777 != mode):', '        if check_mode and p.stat().st_mode & 0o777 != mode:'),
 'g20_no_mode_stat': ('        if sha_bytes(p.read_bytes()) != sha_bytes(data) or (check_mode and p.stat().st_mode & 0o777 != mode):', '        if sha_bytes(p.read_bytes()) != sha_bytes(data):'),
 'g21_no_last_record': ('    if buf:\n        emit(buf)', '    if False:\n        emit(buf)'),
 'g21_no_carry': ('        *recs, buf = (buf + b).split(b"\\n")', '        *recs, buf = b.split(b"\\n")'),
 'g21_crlf_header': ('            if rec.rstrip(b"\\r").decode("latin-1") != ",".join(LABEL_HEADER):', '            if rec.decode("latin-1") != ",".join(LABEL_HEADER):'),
 'g22_own_pid': ('        if not d.name.isdigit() or int(d.name) == me:', '        if not d.name.isdigit():'),
 'g22_tag_prefix': ('    rx = re.compile(r"(?<![\\w-])" + re.escape(tag) + r"(?![\\w-])")', '    rx = re.compile(re.escape(tag))'),
 'g22_one_or_more': ('    if len(hits) != 1:', '    if not hits:'),
 'g22_no_stamp_time': ('    if not m or datetime.fromisoformat(m.group(1) + "+00:00").timestamp() >= t0:', '    if not m:'),
 'g22_no_gb_name': ('    if "G-B" not in hits[0] or not re.search(r"(?i)\\bpause", hits[0]):', '    if False:'),
 'g22_seconds_only': ('STAMP = re.compile(r"^(\\d{4}-\\d\\d-\\d\\dT\\d\\d:\\d\\d(?::\\d\\d)?)Z")', 'STAMP = re.compile(r"^(\\d{4}-\\d\\d-\\d\\dT\\d\\d:\\d\\d:\\d\\d)Z")'),
 'g23_no_hup': ('GB_SIGS = (signal.SIGTERM, signal.SIGINT, signal.SIGHUP)', 'GB_SIGS = (signal.SIGTERM, signal.SIGINT)'),
 'g24_no_base64': ('        raw = base64.b64decode(md5s[0], validate=True)', '        raw = md5s[0].encode()[:16]'),
 'g24_composite_ok': ('    if len(md5s) != 1 or len(lens) != 1 or not lens[0].isdigit():', '    if len(md5s) > 1 or len(lens) != 1 or not lens[0].isdigit():'),
 'qb7_no_flickr_term': ('    return n_e_gb - w25_flagged - lost - len(FLICKR_W3)', '    return n_e_gb - w25_flagged - lost'),
 'gb_no_remaining_n': ('    if len(rem) != remaining_n or len(set(rem)) != remaining_n:', '    if False:'),
}
EQUIV = {
 "eq_val_term": (' | (t & s["val"])\n', "\n"),
 "eq_no_36707_assert": ('len(l2p1_q11) != N["l2p1_q11"]', "False"),
}
TIMEOUT, JOBS = 300, 3
src = Path(sys.argv[1]).read_text(); S = Path(sys.argv[2]).resolve(); S.mkdir(parents=True, exist_ok=True)
if str(S).startswith("/mnt/") or re.search(r"(?i)annotations|labels|captions", str(S)):
    sys.exit(f"{S}: the scratch dir must be on ext4 and free of BARRED words (W3)")
for d in ("home", "tmp"):
    (S / d).mkdir(exist_ok=True)
SANDBOX = ["env", "-i", "PATH=/usr/bin:/bin", f"HOME={S / 'home'}", f"TMPDIR={S / 'tmp'}", "unshare", "-rnm",
           "sh", "-c", 'mount -t tmpfs tmpfs /dev/shm && exec "$@"', "sh"]
def run(name, a, b):
    if src.count(a) != 1:
        return "PATTERN"
    p = S / f"{name}.py"; p.write_text(src.replace(a, b))
    try:
        r = subprocess.run(SANDBOX + ["python3", "-I", str(p), "selftest"], capture_output=True, text=True,
                           timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    last = (r.stderr.strip().splitlines() or [""])[-1]
    return "KILLED" if r.returncode and "selftest ok" not in r.stdout and "pinned real file" not in last else "SURVIVED"
with ThreadPoolExecutor(JOBS) as ex:
    res = dict(zip(M, ex.map(lambda kv: run(kv[0], *kv[1]), M.items())))
    eq = dict(zip(EQUIV, ex.map(lambda kv: run(kv[0], *kv[1]), EQUIV.items())))
dead = ("KILLED", "TIMEOUT")
for n, v in {**res, **eq}.items():
    print(f"{n:24s} {v}")
print(f"mutants {len(M)}: killed {sum(v in dead for v in res.values())} (timeout {sum(v == 'TIMEOUT' for v in res.values())}), survived "
      f"{[n for n, v in res.items() if v not in dead]}; equivalent {len(EQUIV)}: {eq}")
