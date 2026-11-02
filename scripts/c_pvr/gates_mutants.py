#!/usr/bin/env python3
"""CC-222 round-3 / CC-227 mutant harness for scripts/c_pvr/gates.py. Usage: python3 -I this.py <gates.py> <scratch dir>.
Each mutant replaces one exact string (it must occur once) and runs `selftest` on the copy. A mutant is KILLED when
the selftest fails before its final real-pin check (copies outside the repo always fail that check, so a failure that
is only that check counts as SURVIVED). EQUIV lists mutants proven equivalent; they are run and expected to survive."""
import subprocess, sys
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
}
EQUIV = {
 "eq_val_term": (' | (t & s["val"])\n', "\n"),
 "eq_no_36707_assert": ('len(l2p1_q11) != N["l2p1_q11"]', "False"),
}
src = Path(sys.argv[1]).read_text(); S = Path(sys.argv[2]); S.mkdir(parents=True, exist_ok=True)
def run(name, a, b):
    if src.count(a) != 1:
        return "PATTERN"
    p = S / f"{name}.py"; p.write_text(src.replace(a, b))
    r = subprocess.run(["python3", "-I", str(p), "selftest"], capture_output=True, text=True)
    last = (r.stderr.strip().splitlines() or [""])[-1]
    return "KILLED" if r.returncode and "selftest ok" not in r.stdout and "pinned real file" not in last else "SURVIVED"
res = {n: run(n, *ab) for n, ab in M.items()}
eq = {n: run(n, *ab) for n, ab in EQUIV.items()}
for n, v in {**res, **eq}.items():
    print(f"{n:24s} {v}")
print(f"mutants {len(M)}: killed {sum(v == 'KILLED' for v in res.values())}, survived "
      f"{[n for n, v in res.items() if v != 'KILLED']}; equivalent {len(EQUIV)}: {eq}")
