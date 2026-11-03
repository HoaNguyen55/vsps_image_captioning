#!/usr/bin/env python3
"""Author mutant harness for scripts/c_pvr/c_pvr_run.py (Q-SPLIT (iii); gates_mutants.py pattern).
Usage: ~/.venvs/c_stage1_lists/bin/python -I -B c_pvr_run_mutants.py <c_pvr_run.py> <repo root> <scratch dir>.
Each mutant replaces one exact string (it must occur once) and runs `selftest --root <repo root>` on a sandboxed copy:
`env -i`, `unshare -rnm` (loopback-only network, private tmpfs on /dev/shm), HOME and TMPDIR on the ext4 scratch dir,
which must not lie under /mnt or contain a BARRED word. The unmutated copy runs first and must print 'selftest ok'.
KILLED = the selftest fails; TIMEOUT counts as killed. EQUIV lists mutants argued equivalent or untestable in writing;
they are run and expected to survive."""
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

M = {
    # Q-SPLIT (ii) pins and the import closure
    "code_pin_c_pvr": ('"scripts/c_pvr/c_pvr.py": "8f10bd6097', '"scripts/c_pvr/c_pvr.py": "8f10bd6098'),
    "no_code_check": ("    if bad := code_bad(root):\n", "    if (bad := code_bad(root)) and False:\n"),
    "code_bad_no_file_check": ("if not (root / rel).is_file() or hashlib", "if hashlib"),
    "no_closure_check": ("    if stray:\n", "    if False:\n"),
    "closure_skips_all": ("and Path(f).resolve().is_relative_to(root.resolve())", "and False"),
    # refusals
    "no_gates_refuse": ("    CP.refuse(p)\n    G.refuse(p)\n", "    CP.refuse(p)\n"),
    "no_own_barred": ("    if OWN_BARRED.search(str(p)):\n", "    if False:\n"),
    "own_barred_no_info": (r"|nocaps_\w*image_info", ""),
    # integrity (SUMS line, run sha)
    "no_run_sha_check": ("    if CP.sha_file(Path(__file__)) != run_sha:\n", "    if False:\n"),
    "sums_malformed_ok": ('    if not all(re.fullmatch(r"[0-9a-f]{64}  \\S+", x) for x in lines):\n', "    if False:\n"),
    "sums_own_any": ("if [x.split()[0] for x in lines if x.split()[1] == SELF_REL] != [run_sha]:",
                     "if run_sha not in [x.split()[0] for x in lines if x.split()[1] == SELF_REL]:"),
    "sums_no_verify": ("    if bad := [x.split()[1] for x in lines if sha(root / x.split()[1]) != x.split()[0]]:\n",
                       "    if bad := []:\n"),
    # owners (R6)
    "ledger_no_gone": ("if sorted(rows) != sorted(ldg) or", "if not set(rows) <= set(ldg) or"),
    "ledger_header_kept": ('if r.startswith("| ")][1:]', 'if r.startswith("| ")]'),
    "ledger_whole_doc": ('sec = text.split("\\n### 2.3 ", 1)[1].split("\\n### ", 1)[0]',
                         'sec = text.split("\\n### 2.3 ", 1)[1]'),
    "lists_no_gone": ("    if have != sorted(lists):\n", "    if not set(have) <= set(lists):\n"),
    "spent_unchecked": ("    if miss := [p for p in spent if p not in sec]:\n", "    if miss := []:\n"),
    "spent_whole_text": ("[p for p in spent if p not in sec]", '[p for p in spent if p not in port.decode("utf-8")]'),
    "no_orphans": ("orphans = sorted(set(owners) - refs)", "orphans = []"),
    "owner_short_sha": ('re.fullmatch(r"[0-9a-f]{64}", h) for h in o["caches"].values()) or o["n"] < 1:',
                        're.fullmatch(r"[0-9a-f]{63,64}", h) for h in o["caches"].values()) or o["n"] < 1:'),
    "owner_n_zero": ('for h in o["caches"].values()) or o["n"] < 1:', 'for h in o["caches"].values()) or o["n"] < 0:'),
    "owner_no_caches": ("    if not o[\"caches\"] or not all(", "    if not all("),
    # lists
    "lists_missing_unchecked": ("    if miss := sorted(k for k, v in pins.items() if v is None):\n", "    if False:\n"),
    "lists_sha_unchecked": ("        if sha(root / rel) != want:\n            fault(f\"{rel} differs from its pin {want[:8]}\")\n"
                            "        return", "        if False:\n            fault(f\"{rel} differs from its pin {want[:8]}\")\n"
                            "        return"),
    "half_odd": ('encode("utf-8")).hexdigest()[-1], 16) % 2 == 0\n', 'encode("utf-8")).hexdigest()[-1], 16) % 2 == 1\n'),
    "half_salt": ('return int(hashlib.sha256((i + "c_pvr").encode', 'return int(hashlib.sha256((i + "c_pvrx").encode'),
    "split_no_dup_check": ("    if len(ids) != n or len(set(ids)) != n:\n", "    if len(ids) != n:\n"),
    "t_a_salt": ('key=lambda i: (hashlib.sha256((i + "c_pvr_TA")', 'key=lambda i: (hashlib.sha256((i + "c_pvr_OB")'),
    "t_a_n": ("T_A_N = 1070", "T_A_N = 1071"),
    "t_a_short_ok": ("    if len(set(tc)) != len(tc) or len(t_a) != T_A_N:\n", "    if len(set(tc)) != len(tc):\n"),
    # CC-245 round 2: B1 (one id space, exactly one row per selected id, n), B2 (inventory), B3 (D-VI), rulings (a)-(d)
    "no_dangling": ("dangling = sorted(v for v in refs if v not in owners and not OWN_RX.match(v))", "dangling = []"),
    "owner_any_status": ("    if st not in STATUSES:\n", "    if False:\n"),
    "owner_no_reason": ('    if st == "deferred" and not o.get("reason"):\n', "    if False:\n"),
    "owner_source_n_off": ('    if st in ("compute", "id_join") and len(set(pinned_ids(disk, o["source"]))) != o["n"]:\n',
                           "    if False:\n"),
    "owner_space_mix_ok": ('    if len({CACHE_SPACE.get(c) for c in o["caches"]}) != 1 or None in', "    if False and None in"),
    "owner_space_unknown_ok": (' or None in {CACHE_SPACE.get(c) for c in o["caches"]}:\n        fault(f"owner {k}: its caches',
                               ':\n        fault(f"owner {k}: its caches'),
    "owner_select_n_off": ('    if o["select"] and len(set(pinned_ids(disk, o["select"]))) != o["n"]:\n', "    if False:\n"),
    "pinned_ids_sha_off": ("    if G.sha_bytes(b) != want:\n        fault(f\"{rel} differs from its pin", "    if False:\n        fault(f\"{rel} differs from its pin"),
    "ids_of_plus_first_only": ('    for path in jpath.split("+"):\n', '    for path in jpath.split("+")[:1]:\n'),
    "ids_of_list_whole": ("str(x[0] if isinstance(x, list) else x)", "str(x)"),
    "b_rules_unchecked": ("    if G.sha_bytes(b) != brules[1] or sorted(json.loads(b)[\"owners\"]) != sorted(bmap):\n", "    if False:\n"),
    "b_rules_sha_only": ("    if G.sha_bytes(b) != brules[1] or sorted(json.loads(b)[\"owners\"]) != sorted(bmap):\n",
                         "    if G.sha_bytes(b) != brules[1]:\n"),
    "bmap_not_referenced": ("            *extra, *bmap.values()}\n    dangling", "            *extra}\n    dangling"),
    "list_values_first_only": ("*(x for v in lists.values() for x in mapped(v))", "*(mapped(v)[0] for v in lists.values())"),
    "skip_lists_hashed": ('**({} if all(OWN_RX.match(x) for x in mapped(v)) else {"sha256": G.sha_bytes(read(p))})',
                          '**{"sha256": G.sha_bytes(read(p))}'),
    "list_rx_no_json": (r'LIST_RX = re.compile(r"^manuscript/prereg/.+\.(?:txt|tsv|json)$")',
                        r'LIST_RX = re.compile(r"^manuscript/prereg/.+\.(?:txt|tsv)$")'),
    "records_first_block": ('    for block in re.split(r"\\n(?=[^ \\n]*:)", text):\n', '    for block in re.split(r"\\n(?=[^ \\n]*:)", text)[:1]:\n'),
    "select_space_unchecked": ('    if o["select"] and (len({CACHE_SPACE.get(c) for c in o["caches"]}) != 1 or not set(o["caches"]) <= set(CACHE_SPACE)):\n',
                               "    if False:\n"),
    "select_space_unknown_ok": (' != 1 or not set(o["caches"]) <= set(CACHE_SPACE)):\n', " != 1):\n"),
    "select_dup_rows_ok": ("        if set(cnt) != sel or any(v != 1 for v in cnt.values()):\n", "        if set(cnt) != sel:\n"),
    "select_missing_ok": ("        if set(cnt) != sel or any(v != 1 for v in cnt.values()):\n", "        if any(v != 1 for v in cnt.values()):\n"),
    "select_n_unchecked": ('        if len(idx) != o["n"]:\n', "        if False:\n"),
    "frozen_sha_unchecked": ("    if sha(p) != want:\n        fault(f\"{p.name} differs from --{key}-sha\")\n", ""),
    "frozen_log_unchecked": ('    if want not in refuse(env["log"]).read_text(encoding="utf-8"):\n', "    if False:\n"),
    "frozen_schema_unchecked": ('    if doc.get("schema") != schema:\n', "    if False:\n"),
    "owners_status_unchecked2": ('    if bad := sorted(k for k, o in ow.items() if o.get("status") not in STATUSES):\n        fault(f"owners {bad} have no R6 status")',
                                 '    if bad := []:\n        fault(f"owners {bad} have no R6 status")'),
    "manifest_owner_mismatch_ok": ('        if man["owners_sha256"] != env["owners_sha"]:\n', "        if False:\n"),
    "manifest_row_unchecked": ('            if not m or m["n"] != o["n"] or m["source_sha256"] != o["source"][1]:\n', "            if not m:\n"),
    "manifest_row_source_ok": (' or m["source_sha256"] != o["source"][1]:\n                fault(f"owner {k} is',
                               ':\n                fault(f"owner {k} is'),
    "compute_rows_dropped": ("            cmp[k] = cached(o[\"n\"], {m[\"cache\"]: m[\"sha256\"]})\n", "            pass\n"),
    "join_rows_dropped": ('    return (cmp, {k: o for k, o in ow.items() if o["status"] == "id_join"},', '    return (cmp, {},'),
    "join_n_unchecked": ('    if not all(x.isdigit() for x in photos) or len(photos) != o["n"]:\n', '    if not all(x.isdigit() for x in photos):\n'),
    "join_digit_unchecked": ('    if not all(x.isdigit() for x in photos) or len(photos) != o["n"]:\n', '    if len(photos) != o["n"]:\n'),
    "join_hits_not_in_files": ('out["ovqa_dev"][2], hits)))', 'out["ovqa_dev"][2], set())))'),
    "join_into_n_e_power": ('rec["n_e_power_inputs"] = {"w25_flagged": rec["nocaps_test"]["flagged"], "lost": rec["nocaps_test"]["lost"]}',
                            'rec["n_e_power_inputs"] = {"w25_flagged": rec["nocaps_test"]["flagged"] + 1, "lost": rec["nocaps_test"]["lost"]}'),
    "outputs_precheck_off": ('    if any(os.path.lexists(env["out"] / x) for x in OUTS) or decided(env["sealed"]):\n',
                             '    if decided(env["sealed"]):\n'),
    "decided_off": ('    if any(os.path.lexists(env["out"] / x) for x in OUTS) or decided(env["sealed"]):\n',
                    '    if any(os.path.lexists(env["out"] / x) for x in OUTS):\n'),
    "owner_feats_late": ('    ys = {k: owner_feats(env, o) for k, o in sorted(cmp.items())}\n    q = query_ids(env)',
                         '    ys = {}\n    q = query_ids(env)'),
    "xm_loaded_late": ('"sscd": env["sscd_ok"](refuse(env["sscd"])), "xm": env["xm"]()}', '"sscd": env["sscd_ok"](refuse(env["sscd"])), "xm": set()}'),
    "retry_truncated_on": ('    f = env["features"]([p for _, p in pairs], st["sscd"], workers=env["workers"], retry_truncated=False)',
                           '    f = env["features"]([p for _, p in pairs], st["sscd"], workers=env["workers"], retry_truncated=True)'),
    # owner-feats (Ruling 8)
    "of_only_unchecked": ("    if only is not None and only not in rows:\n", "    if False:\n"),
    "of_mnt_ok": ('    if str(env["in"].resolve()).startswith("/mnt/"):\n        fault("the owner caches', '    if False:\n        fault("the owner caches'),
    "of_n_unchecked": ('        if len(ids) != o["n"] or len(set(ids)) != o["n"]:\n', "        if False:\n"),
    "of_missing_ok": ("        if miss := [x for x in paths if not x.is_file()]:\n", "        if miss := []:\n"),
    "of_unreadable_ok": ('        if f["unreadable"]:\n            fault(f"{k}:', '        if False:\n            fault(f"{k}:'),
    "of_retry_on": ('[refuse(x) for x in paths], sscd, workers=env["workers"], retry_truncated=False)',
                    '[refuse(x) for x in paths], sscd, workers=env["workers"], retry_truncated=True)'),
    "of_mode_0644": ("write_new(p, buf.getvalue(), 0o400, check_mode=True)", "write_new(p, buf.getvalue(), 0o644, check_mode=True)"),
    "of_manifest_early": ("    if all(p.exists() for p in done.values()) and not os.path.lexists(env[\"feats\"]):\n",
                          "    if not os.path.lexists(env[\"feats\"]):\n"),
    "of_manifest_rewrite": ("    if all(p.exists() for p in done.values()) and not os.path.lexists(env[\"feats\"]):\n",
                            "    if all(p.exists() for p in done.values()):\n"),
    "of_no_log_row": ('        alog(env["sealed"], "owner-feats write", p.name,', '        (lambda *a: a)(env["sealed"], "owner-feats write", p.name,'),
    "fname_ktvic_any": ("        if len(hit) != 1:\n", "        if not hit:\n"),
    "fname_jpg_unchecked": ('    if rule == "jpg" and NAME_RX.fullmatch(i):\n', '    if rule == "jpg":\n'),
    "kt_id_rx_loose": (r'KT_ID, OV_KEY = re.compile(r"[1-9]\d*")', r'KT_ID, OV_KEY = re.compile(r"\d+")'),
    # lists (B3, Ruling 10-11)
    "dvi_no_dev299": ('DVI_KT = ("h_bdt1_739", "ktvic_dev299", "refused_ktvic_dup")', 'DVI_KT = ("h_bdt1_739", "refused_ktvic_dup")'),
    "dvi_no_ov_owner": ('DVI_OV = ("openviic_dev_c1",)', "DVI_OV = ()"),
    # CC-245r2 B3a (the real 5-field copy map) and B3b (closure over both sides)
    "copy_len_off": ("                if len(e) != 5 or not isinstance(e[0], str)", "                if not isinstance(e[0], str)"),
    "copy_type_off": ("if len(e) != 5 or not isinstance(e[0], str) or not OV_KEY", "if len(e) != 5 or not OV_KEY"),
    "copy_file_off": (" or not OV_KEY.fullmatch(e[0]) or e[1] not in SPLITS:", " or e[1] not in SPLITS:"),
    "copy_split_off": (" or not OV_KEY.fullmatch(e[0]) or e[1] not in SPLITS:", " or not OV_KEY.fullmatch(e[0]):"),
    "copy_test_keys_off": ('    if set(pairs["test"]) != kt_test or not set(pairs["train"]) <= kt_train:\n',
                           '    if not set(pairs["train"]) <= kt_train:\n'),
    "copy_train_keys_off": ('    if set(pairs["test"]) != kt_test or not set(pairs["train"]) <= kt_train:\n',
                            '    if set(pairs["test"]) != kt_test:\n'),
    "dvi_no_test_side": ('    for split in ("train", "test"):\n        for k, es in pairs[split].items():',
                         '    for split in ("train",):\n        for k, es in pairs[split].items():'),
    "dvi_no_closure": ("    while frontier:\n", "    for _ in (1,):\n"),
    "dvi_no_test_seeds": ('"ktvic_test_side": {("k", i) for i in kt_test},', '"ktvic_test_side": set(),'),
    "dvi_no_ov_test_seed": ('"openviic_owners": {("o", f) for f in ov_own | ov_test}}', '"openviic_owners": {("o", f) for f in ov_own}}'),
    "dvi_owner_subset_unchecked": ("    if bad := sorted(k for k, v in kt_own.items() if not v <= kr_ids):\n", "    if bad := []:\n"),
    "dvi_hop_only_off": ('"removed_hop_only": side(gone - one_hop)', '"removed_hop_only": side(gone - seeds)'),
    "dvi_kept_ov_off": ('kept_ov = kr_ids - {i for t, i in gone if t == "k"}, ovr - {f for t, f in gone if t == "o"}',
                        'kept_ov = kr_ids - {i for t, i in gone if t == "k"}, ovr'),
    "ov_key_jpg_only": (r're.compile(r"\d{11}\.(?:jpg|jpeg|png|JPG|PNG)")', r're.compile(r"\d{11}\.jpg")'),
    "kt_captions_all": ('sum(str(a["image_id"]) in keep_kt for a in kr["annotations"])', 'len(kr["annotations"])'),
    "ov_captions_all": ('sum(len(ov_train[f]["captions"]) for f in keep_ov)', 'sum(len(v["captions"]) for v in ov_train.values())'),
    "kt_int_unchecked": ('    if not all(type(r["id"]) is int for r in images):\n', "    if False:\n"),
    "ov_key_unchecked": ("    if not all(OV_KEY.fullmatch(k) for k in d):\n", "    if False:\n"),
    "d_tc_keeps_ta": ('"d_tc_images_before_w25": len(set(tc) - set(t_a))', '"d_tc_images_before_w25": len(set(tc))'),
    # tenancy (prereg §8.2)
    "tag_any_token": ('    if not re.fullmatch(r"OPS-[0-9A-Za-z][0-9A-Za-z-]*", tag):\n', "    if False:\n"),
    "tag_prefix": ('    rx = re.compile(r"(?<![\\w-])" + re.escape(tag) + r"(?![\\w-])")\n    hits = [x for x in refuse(',
                   "    rx = re.compile(re.escape(tag))\n    hits = [x for x in refuse("),
    "tag_one_or_more": ("    if len(hits) != 1:\n        return f\"the pause tag", "    if not hits:\n        return f\"the pause tag"),
    "stamp_no_time": ('    if not m or datetime.fromisoformat(m.group(1) + "+00:00").timestamp() >= t0:\n',
                      "    if not m:\n"),
    "no_w25_name": ("    if not W25_RX.search(hits[0]) or not", "    if not"),
    "w25_substring": ('W25_RX = re.compile(r"(?<![\\w-])W25(?![\\w-])")', 'W25_RX = re.compile(r"W25")'),
    "no_pause_word": (' or not re.search(r"(?i)\\bpause", hits[0]):\n        return "the pause line does not name W25',
                      ':\n        return "the pause line does not name W25'),
    "no_foreign_jobs": ('    if G.foreign_jobs(env["proc"], os.getpid()):\n', "    if False:\n"),
    "backup_shm_ok": ('    if not env["backup"].is_file() or b"/dev/shm" in env["backup"].read_bytes():\n',
                      '    if not env["backup"].is_file():\n'),
    "lock_replaced_ok": ('        if (a.st_dev, a.st_ino) != (b.st_dev, b.st_ino):\n', "        if False:\n"),
    "shm_mode_ok": ("or s.st_mode & 0o777 != 0o700 or", "or"),
    "tag_used_action_only": ('x.split("\\t")[2:4] == ["w25 start", h]', 'x.split("\\t")[2] == "w25 start"'),
    "no_tag_used": ('    if tag_used(env["sealed"], tag):\n', "    if False:\n"),
    "tag_written_plain": ('alog(env["sealed"], "w25 start", hashlib.sha256(tag.encode()).hexdigest(), run_sha)',
                          'alog(env["sealed"], "w25 start", tag, run_sha)'),
    "no_pre_tenancy": ("    if why := tenancy(env, tag):\n", "    if False:\n"),
    "no_lock": ("        fcntl.flock(lockfd, fcntl.LOCK_EX | fcntl.LOCK_NB)\n        if os.path", "        if os.path"),
    "no_residue_check": ('        if os.path.lexists(env["shm"]):\n            fault(', "        if False:\n            fault("),
    "shm_mode_0755": ('        env["shm"].mkdir(mode=0o700)\n        os.chmod(env["shm"], 0o700)',
                      '        env["shm"].mkdir(mode=0o755)\n        os.chmod(env["shm"], 0o755)'),
    # inputs
    "n_remain_unchecked": ('    if len(rem) != env["n_remain"] or len(set(rem)) != len(rem):\n', "    if False:\n"),
    "oi_list_unchecked": ("    if bad := [i for i in rem if i not in oi]:\n", "    if bad := []:\n"),
    "owners_status_unchecked": ('    if bad := sorted(k for k, o in ow.items() if o.get("status") not in STATUSES):\n',
                                "    if bad := []:\n"),
    "staged_cache_unchecked": ('            if not (env["in"] / name).is_file() or sha(env["in"] / name) != want:\n',
                               "            if False:\n"),
    "owner_rows_unchecked": ('    if len(ids) != o["n"]:\n', "    if False:\n"),
    "out_on_mnt_ok": ('    if str(env["in"].resolve()).startswith("/mnt/") or', "    if"),
    # fetch, classes (prereg §8.1)
    "fetched_any_err": ('    if b is not None and err == "":\n', "    if b is not None:\n"),
    "redirect_lost": ('FAULT_ERR = re.compile(r"status \\d+|redirected|not a JPEG body")',
                      'FAULT_ERR = re.compile(r"status \\d+|not a JPEG body")'),
    "lost_any_string": ('LOST_ERR = re.compile(r"[A-Za-z_]\\w*")', 'LOST_ERR = re.compile(r".+")'),
    "fault_class_ignored": ('            if cls == "fault":\n', "            if False:\n"),
    "url_validation_dir": ('CP.OI_TEST_URL.format(file=f"{x}.jpg")', 'W.F.OI_URL.format(file=f"{x}.jpg")'),
    "xm_backstop_off": ("    if G.sha_bytes(b) in xm:\n", "    if False:\n"),
    # features (R1d)
    "decode_class_lost": ('lost[pairs[i][0]] = "decode " + msg.split(":")[0]', 'lost[pairs[i][0]] = "decode"'),
    "trunc_not_counted": ('        trunc += [pairs[i][0]] if "truncated" in msg else []\n', ""),
    "drop_not_logged": ('        fh.write(f"{CP.utc()}\\tdeleted\\t{folder}\\t{n} files\\t{what}\\n")\n', "        pass\n"),
    "drop_count_zero": ("    n = sum(len(fs) for _, _, fs in os.walk(folder))\n", "    n = 0\n"),
    # parts and resume
    "part_mode_0644": ("write_new(part, buf.getvalue(), 0o400, check_mode=True)",
                       "write_new(part, buf.getvalue(), 0o644, check_mode=True)"),
    "read_part_no_set": ('    if meta["set"] != kind or meta', "    if meta"),
    "read_part_no_batch": ('meta["batch_sha256"] != ids_sha(ids) or ', ""),
    "read_part_no_run": (' or meta["run_sha256"] != run_sha:', ":"),
    "resume_refetch": ("        if part.exists():\n            lost.update", "        if False:\n            lost.update"),
    "no_guard": ("        guard(env, st)\n", ""),
    "cap_ge": ("        if len(lost) > LOST_CAP[kind]:\n", "        if len(lost) >= LOST_CAP[kind]:\n"),
    "cap_nocaps_11": ('LOST_CAP = {"nocaps_test": 10,', 'LOST_CAP = {"nocaps_test": 11,'),
    "cap_nocaps_9": ('LOST_CAP = {"nocaps_test": 10,', 'LOST_CAP = {"nocaps_test": 9,'),
    "cap_ovqa_2": ('"ovqa_dev": 1}  # prereg §8.1', '"ovqa_dev": 2}  # prereg §8.1'),
    "cap_ovqa_0": ('"ovqa_dev": 1}  # prereg §8.1', '"ovqa_dev": 0}  # prereg §8.1'),
    "cap_per_batch": ("        lost |= gone | dec\n", "        lost = gone | dec\n"),
    "decode_lost_dropped": ("        lost |= gone | dec\n", "        lost |= gone\n"),
    # 24 h stop (prereg §8.3)
    "project_every_batch": ('    if st["projected"]:\n        return\n', ""),
    "project_never_stops": ('    if end > st["deadline"]:\n', "    if False:\n"),
    "deadline_rewritten": ("    if not p.exists():\n        write_new(p,", "    if True:\n        write_new(p,"),
    "wall_23h": ("WALL = 24 * 3600", "WALL = 23 * 3600"),
    "deadline_never": ('    if env["clock"]() >= st["deadline"]:\n', "    if False:\n"),
    # OpenViVQA (R1e, CC-237 (vi))
    "ovqa_rule_sha_unchecked": ('    if sha(rule_p) != env["rule"][1]:\n', "    if False:\n"),
    "ovqa_names_count_off": ('    if len(set(names)) != CP.OVQA_COUNTS[CP.OVQA_DEV][0] or not', "    if not"),
    "ovqa_name_rx_off": (" or not all(NAME_RX.fullmatch(x) for x in names):\n", ":\n"),
    "zip_pin_unchecked": ("    if rc or (n, s256) != CP.OVQA_DEV_ZIP:\n", "    if rc:\n"),
    "zip_rc_unchecked": ("    if rc or (n, s256) != CP.OVQA_DEV_ZIP:\n", "    if (n, s256) != CP.OVQA_DEV_ZIP:\n"),
    "no_ovqa_count": ('    got = CP.ovqa_count(env["ovqa"], env["sealed"], refuse(env["root"] / env["rule"][0]), env["rule"][1], z)',
                      '    got = {"dev_names_in_zip": len(CP.ovqa_load(env["ovqa"], env["sealed"], CP.OVQA_DEV)["images"])}'),
    "dup_member_ok": ("            if Path(m).name in members:\n", "            if False:\n"),
    "zip_not_in_tmpfs": ('    d = st["shm"] / "ovqa"\n', '    d = env["work"] / "ovqa"\n'),
    "zip_not_dropped": ('            drop(env, st["shm"] / "ovqa", "after ovqa_dev (dev-images.zip and batches)")\n', ""),
    "ident_rewritten": ("            if not ident_p.exists():\n                write_new(ident_p",
                        "            if True:\n                write_new(ident_p"),
    "ident_unchecked": ("        if not ident_p.exists():\n            fault(", "        if False:\n            fault("),
    "zip_always": ("        if not all((env[\"work\"] / \"parts\" / f\"ovqa_dev_{n:04d}.npz\").exists()",
                   "        if True or not all((env[\"work\"] / \"parts\" / f\"ovqa_dev_{n:04d}.npz\").exists()"),
    # window exit (trap, signals, ACCESS_LOG)
    "no_trap": ('            drop(env, env["shm"], "trap: window exit")\n', "            pass\n"),
    "no_signals": ("            signal.signal(s, on_sig)\n", "            pass\n"),
    "signals_not_restored": ("                signal.signal(s, old[s])\n", "                pass\n"),
    "child_handler_raises": ("            os._exit(128 + signum)\n", "            pass\n"),
    "abort_reason_dropped": ('        why = str(e).split(":")[0][:16] if isinstance(e, SystemExit) else type(e).__name__\n',
                             '        why = "-"\n'),
    "flag_c12_only": ('        hit |= {q["ids"][i] for i in r["excluded"].nonzero()[0]}',
                      '        hit |= {q["ids"][i] for i in r["C1_C2_registered"].nonzero()[0]}'),
    "abort_row_is_end": ('    done, why = "w25 abort", "-"\n', '    done, why = "w25 end", "-"\n'),
    # decide (one look)
    "ovqa_out_lost_only": ('out["ovqa_dev"][2]', 'out["ovqa_dev"][1]'),
    "flagged_includes_lost": ('files = dict(zip(OUTS, (out["nocaps_test"][0],', 'files = dict(zip(OUTS, (out["nocaps_test"][2],'),
    "flickr_off": ("len(gone & set(G.FLICKR_W3))", "0"),
    "owner_union_last_only": ('        hit |= {q["ids"][i]', '        hit = {q["ids"][i]'),
    "decide_missing_part_ok": ('        if not p.exists():\n            fault(f"{p.name} is missing', '        if False:\n            fault(f"{p.name} is missing'),
    # real environment and CLI
    "real_strict_false": ('"strict": True, "pins_b": G.PINS_B', '"strict": False, "pins_b": G.PINS_B'),
    "real_shm": ('SHM, LOCK = Path("/dev/shm/c_pvr_w25")', 'SHM, LOCK = Path("/dev/shm/c_pvr_w26")'),
    "real_batch_1024": ('"batch": W.BATCH, "in"', '"batch": 1024, "in"'),
    "host_any": ('w.add_argument("--host", choices=("laptop",), required=True)', 'w.add_argument("--host", required=True)'),
    "cli_no_integrity": ("    integrity(root, x.run_sha)\n", ""),
    "curl_env_dropped": ("stdin=subprocess.DEVNULL, env=G.CURL_ENV)", "stdin=subprocess.DEVNULL)"),
}
EQUIV = {
    # CP.BARRED (oidv7-*-annotations, /dev/shm/c_pvr_gb, nocaps_val_4500_captions.json) is a subset of gates.BARRED
    # (annotations, /dev/shm/c_pvr_gb) plus OWN_BARRED (nocaps_*captions): dropping CP.refuse refuses nothing less.
    "no_cp_refuse": ("    CP.refuse(p)\n    G.refuse(p)\n", "    G.refuse(p)\n"),
    # 'status N' and 'not a JPEG body' are not identifiers, so LOST_ERR never matches them: classify FAULTs them with
    # or without the FAULT_ERR alternative ('redirected' IS an identifier and is killed above as redirect_lost).
    "status_falls_to_fault": ('FAULT_ERR = re.compile(r"status \\d+|redirected|not a JPEG body")',
                              'FAULT_ERR = re.compile(r"redirected|not a JPEG body")'),
    # Untestable here: the sandbox runs as namespace root with one mapped uid, so no other uid can own the tmpfs dir.
    "shm_uid_ok": (" or s.st_uid != os.getuid():\n", ":\n"),
    # Untestable here: rmtree failure needs a read-only parent, which namespace root bypasses.
    "drop_no_verify": ("    if os.path.lexists(folder):\n        fault(f\"{folder} could not be deleted\")\n", ""),
}
TIMEOUT, JOBS = 600, 3
src = Path(sys.argv[1]).read_text()
root = str(Path(sys.argv[2]).resolve())
S = Path(sys.argv[3]).resolve()
if str(S).startswith("/mnt/") or re.search(r"(?i)annotations|labels|captions|gb_intermediate|image_info", str(S)):
    sys.exit(f"{S}: the scratch dir must be on ext4 and free of BARRED words")
S.mkdir(parents=True, exist_ok=True)
for d in ("home", "tmp"):
    (S / d).mkdir(exist_ok=True)
SANDBOX = ["env", "-i", "PATH=/usr/bin:/bin", f"HOME={S / 'home'}", f"TMPDIR={S / 'tmp'}", "OMP_NUM_THREADS=1",
           "MKL_NUM_THREADS=1", "unshare", "-rnm",  # one BLAS thread, as W25-K1 run2.sh: features fork a worker pool
           "sh", "-c", 'mount -t tmpfs tmpfs /dev/shm && exec "$@"', "sh"]


def run(name: str, a: str, b: str) -> str:
    if src.count(a) != 1:
        return f"PATTERN({src.count(a)})"
    p = S / f"{name}.py"
    p.write_text(src.replace(a, b))
    try:
        r = subprocess.run(SANDBOX + [sys.executable, "-I", "-B", str(p), "selftest", "--root", root],
                           capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    (S / f"{name}.err").write_text(r.stderr[-4000:])
    return "SURVIVED" if r.returncode == 0 and "selftest ok" in r.stdout else "KILLED"


base = run("_original", "#!/usr/bin/env python3\n", "#!/usr/bin/env python3\n")
if base != "SURVIVED":
    (S / f"_original.{base.lower()}").write_text(base + "\n")  # N8: a TIMEOUT leaves its own marker
    sys.exit(f"the unmutated copy {'TIMED OUT (' + str(TIMEOUT) + ' s)' if base == 'TIMEOUT' else 'FAILED (see _original.err)'}"
             " in the sandbox; no mutant is counted")
with ThreadPoolExecutor(JOBS) as ex:
    res = dict(zip(M, ex.map(lambda kv: run(kv[0], *kv[1]), M.items())))
    eq = dict(zip(EQUIV, ex.map(lambda kv: run(kv[0], *kv[1]), EQUIV.items())))
dead = ("KILLED", "TIMEOUT")
for n, v in {**res, **eq}.items():
    print(f"{n:28s} {v}")
print(f"mutants {len(M)}: killed {sum(v in dead for v in res.values())} (timeout "
      f"{sum(v == 'TIMEOUT' for v in res.values())}), other {[n for n, v in res.items() if v not in dead]}; "
      f"equivalent {len(EQUIV)}: {eq}")
