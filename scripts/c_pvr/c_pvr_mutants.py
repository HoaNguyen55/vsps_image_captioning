#!/usr/bin/env python3
"""Mutant harness for scripts/c_pvr/c_pvr.py (pattern of gates_mutants.py; PINS-A §4.5 list plus CC-234 item 15).
Usage: <venv python> -I -B c_pvr_mutants.py <c_pvr.py> <repo root> <scratch dir outside /mnt>.
Each mutant replaces one exact string (it must occur once) and runs `selftest --root <repo root>` on the copy. The
unmutated copy runs first and must print 'selftest ok', so a mutant cannot be "killed" by a path or import error.
KILLED = the selftest fails. EQUIV lists mutants proven equivalent in writing; they are run and expected to survive."""
import subprocess
import sys
from pathlib import Path

M = {
    # verifier labels and parser (§2.3, CC-234 item 14)
    "maybe_to_supported": ('"maybe": "UNCERTAIN"', '"maybe": "SUPPORTED"'),
    "parsefail_to_supported": ('else ("UNCERTAIN", True)', 'else ("SUPPORTED", True)'),
    "parse_last_run": ('m = FIRST_RUN.search(unicodedata.normalize("NFC", ans).casefold())',
                       'm = ([*FIRST_RUN.finditer(unicodedata.normalize("NFC", ans).casefold())] or [None])[-1]'),
    "parse_skips_leading_word": ("lab = LABELS.get(m.group(0)) if m else None",
                                 "lab = next((LABELS[w] for w in FIRST_RUN.findall(unicodedata.normalize('NFC', ans)"
                                 ".casefold()) if w in LABELS), None)"),
    "quote_rule_removed": ("return clean(text).replace('\"', \"'\")", "return clean(text)"),
    # rendering and demonstrations (§2.1, prereg §6.4)
    "order_reversed": ("    return list(ranked[:K])\n", "    return list(ranked[:K])[::-1]\n"),
    "backfill": ("return [t for t in kept if t is not None], sum(t is None for t in kept)",
                 "return [t if t is not None else dc['text'] for t, dc in zip(kept, dcs)], "
                 "sum(t is None for t in kept)"),
    "n0_keeps_kshot": ('    if not demos:\n        return P[f"cap_{lang}_0.txt"]\n', ""),
    "k_5": ("K = 4  #", "K = 5  #"),
    "no_prompt_sha": ("        if hashlib.sha256(b).hexdigest() != sha:\n", "        if False:\n"),
    "clean_no_nfc": ('return " ".join(unicodedata.normalize("NFC", s).split())', 'return " ".join(s.split())'),
    "no_sentence_drop": ("        if cut and not alive:\n", "        if False:\n"),
    "no_emptied": ("    if emptied and props and all(drop):\n", "    if False:\n"),
    "tidy_space_before_punct": ('    (re.compile(r"\\s+([.,;:!?])"), r"\\1"),\n', ""),
    # cap and arms (J-C, CC-234 items 4-6)
    "cap_33": ("CAP = 32  #", "CAP = 33  #"),
    "overflow_order_reversed": ("    for j, p in enumerate(props):\n", "    for j, p in enumerate(props[::-1]):\n"),
    "cap_split_per_arm": ("        if j >= CAP:\n", '        if j >= CAP + (arm == "A8"):\n'),
    "a8_uses_a0": ('A8_INPUT = "A1"', 'A8_INPUT = "A0"'),
    "a8_switch_coupled": ('A8_DELETE = "rejected"', 'A8_DELETE = "coupled"'),
    "a8_coupled_is_rejected": ('"coupled": {"REJECTED", "UNCERTAIN"}}[rule]', '"coupled": {"REJECTED"}}[rule]'),
    "pvr_drop_is_keep": ('{"drop": {"REJECTED", "UNCERTAIN"}, "keep"', '{"drop": {"REJECTED"}, "keep"'),
    "seed_a2": ('"A2": 20262002', '"A2": 20262012'),
    "seed_a3": ('"A3": 20262003', '"A3": 20262013'),
    "seed_a7": ('"A7": 20262007', '"A7": 20262017'),
    "seed_in_boot_range": ('"A7": 20262007', '"A7": 20261200'),
    "a3_top_8": ("A3_TOP = 7", "A3_TOP = 8"),
    # generation and loading (J-T, W10, CC-234 item 2)
    "repetition_penalty_1_5": ('"repetition_penalty": 1.0,', '"repetition_penalty": 1.5,'),
    "num_beams_5": ('"num_beams": 1,', '"num_beams": 5,'),
    "sampling_on": ('GEN_BASE = {"do_sample": False,', 'GEN_BASE = {"do_sample": True,'),
    "max_new_caption_25": ('MAX_NEW = {"caption": 64,', 'MAX_NEW = {"caption": 25,'),
    "safetensors_off": ("use_safetensors=True,", "use_safetensors=False,"),
    "not_local_only": ("from_pretrained(snap, local_files_only=True, use_safetensors",
                       "from_pretrained(snap, local_files_only=False, use_safetensors"),
    "repo_genconfig_kept": ("    model.generation_config = GenerationConfig(**gc)\n", ""),
    "no_prompt_strip": ("new = out[len(ids):] if out[:len(ids)] == ids else out", "new = out[len(ids):]"),
    "no_weight_sha": ("        if sha_file(snap / f) != sha:\n", "        if False:\n"),
    "dtype_fp16": ('DTYPE = "bfloat16"', 'DTYPE = "float16"'),
    # M1 (m9 probe, OPS-1106c-m9-probe-meta): tied lm_head / word_embeddings left on meta
    "mblip_meta_guard_off": ("    if meta := [n for n, t in [*model.named_parameters(), *model.named_buffers()] if t.is_meta]:\n",
                             "    if meta := []:\n"),
    "mblip_tie_skipped": ("    tie_mblip(model, snap, files, torch)\n", ""),
    "mblip_tie_unchecked": ("    if w is not lm.get_input_embeddings().weight or not torch.equal(w, head):\n", "    if False:\n"),
    # proxy (v3 §7)
    "diacritics_stripped": ("def norm(s: str, strip_marks: bool = False)", "def norm(s: str, strip_marks: bool = True)"),
    "norm_no_nfc": ('    s = unicodedata.normalize("NFC", s).casefold()\n    if strip_marks',
                    "    s = s.casefold()\n    if strip_marks"),
    "ge3_to_ge2": ("min(len(s), len(a)) >= 3", "min(len(s), len(a)) >= 2"),
    "near_0_4": ("NEAR = 0.5", "NEAR = 0.4"),
    "near_no_token_rule": ("if any(st & {w for w in a.split() if len(w) >= 2} or Levenshtein",
                           "if any(Levenshtein"),
    "w_default_0": ("def p_text(c: dict, w: int = 1)", "def p_text(c: dict, w: int = 0)"),
    "question_no_boundary": ('re.compile(r"(?<!\\w)(?:" + x + r")(?!\\w)")', 're.compile(x)'),
    "caps_one_letter": ("len(letters) >= 2 and", "len(letters) >= 1 and"),
    "apostrophe_quotes": ("(?<![^\\W_])\\'([^\\']+)\\'(?![^\\W_])", "\\'([^\\']+)\\'"),
    # decomposers (CC-234 item 7)
    "no_relation_gap": ("        while a > floor and chunk[a - 1] == chunk[i0]:\n", "        while False:\n"),
    "vi_no_attr": ("            if toks[i][2] in attr:\n", "            if False:\n"),
    # CC-236 B1, B2, W1, W2, W3
    "align_no_fold": ("toks = align(u, words, lambda x: chair.norm_tone(x.lower()))", "toks = align(u, words)"),
    "align_raw_compare": ("if len(fold(syl)) != len(syl) or fold(text[c:c + len(syl)]) != fold(syl):",
                          "if text[c:c + len(syl)] != syl:"),
    "no_underscore_map": ('seen = [t.replace("_", " ") for t in texts]', "seen = list(texts)"),
    "no_merge": ("units = merge_units([([noun]", "units = ([([noun]"),
    "merge_drops_class": ("out[-1] = (c + cls, m + ms, j0, max(j1, i1))", "out[-1] = (c, m + ms, j0, max(j1, i1))"),
    "check_contain_off": ('        if p["kind"] == "obj" and not all(', "        if False and not all("),
    "check_disjoint_off": ('    if any(p["end"] > q["start"] or', '    if False and any(p["end"] > q["start"] or'),
    "decomp_fail_aborts": ('            if "differs from its pin" in str(e):\n                raise\n', "            raise\n"),
    "decomp_fail_drops_caption": ('"sents": [[0, len(t)]] if t else [], "nouns": [], "props": [], "decomp_fail"',
                                  '"sents": [], "nouns": [], "props": [], "decomp_fail"'),
    "no_colour_phrase": ("            elif i in phrase_end:\n", "            elif False:\n"),
    "plural_no_human": ('"human": "humans", ', ""),
    "plural_only_rule_off": ('if w in IRREGULAR.values() or (w.endswith("s") and not w.endswith(("ss", "us"))):',
                             "if False:"),
    "plural_last_word": ('h = words.index("of") - 1 if "of" in words[1:] else len(words) - 1', "h = len(words) - 1"),
    "vi_va_not_delim": ('VI_DELIM = {"và", ', "VI_DELIM = {"),
    "en_cc_not_delim": ('or doc[i].dep_ == "cc" or', "or"),
    "no_text_props": ("props += [{", "props += [] and [{"),
    "decomposer_digit_tokens": ("    return extract(text, tokens=False)\n", "    return extract(text)\n"),
    "raw_tone_unchecked": ('    if os.environ.get("RESCAP_RAW_TONE") is not None:', "    if False:"),
    "no_vnc_sha": ("        if sha_file(vnc / rel) != sha:\n", "        if False:\n"),
    # EN map (§4.3)
    "en_map_pos_altered": ('"pos": vi[k]["pos"], "neg"', '"pos": vi[k]["pos"][1:], "neg"'),
    "en_tie_no_own": ('(f not in names(vi[k]["neg"]), len(vi[k]["pos"]), keys.index(k))',
                      '(len(vi[k]["pos"]), keys.index(k))'),
    "en_no_plural": ('cls[k]["en"] = sorted(set(cls[k]["en"]) | {f for f in more if f not in claims})',
                     'cls[k]["en"] = sorted(set(cls[k]["en"]))'),
    # custody, ovqa-pin, URL, refusals
    "oi_url_changed": ('OI_TEST_URL = "https://open-images-dataset.s3.amazonaws.com/test/{file}"',
                       'OI_TEST_URL = "https://open-images-dataset.s3.amazonaws.com/tests/{file}"'),
    "sha1_no_blob_header": ('hashlib.sha1(b"blob %d\\0" % n)', "hashlib.sha1()"),
    "ovqa_main_revision": ("OVQA_URL.format(rev=OVQA_REV, name=name)", 'OVQA_URL.format(rev="main", name=name)'),
    "ovqa_no_unlink": ("            part.unlink(missing_ok=True)\n", ""),
    "ovqa_no_sha1_check": ("if rc or n != size or s1 != sha1:", "if rc or n != size:"),
    "ovqa_dev_qa_3546": ('"vlsp2023_dev_data.json": (1070, 3545)', '"vlsp2023_dev_data.json": (1070, 3546)'),
    "ovqa_dev_images_1071": ('"vlsp2023_dev_data.json": (1070, 3545)', '"vlsp2023_dev_data.json": (1071, 3545)'),
    "ovqa_test_count_off": ('"vlsp2023_test_data.json": (1000, 14035)', '"vlsp2023_test_data.json": (1000, 14034)'),
    "ovqa_rule_sha_unchecked": ("    if sha_file(rule_path) != rule_sha:\n", "    if False:\n"),
    "ovqa_dev_images_optional": ('        elif name == OVQA_DEV:\n            fault(', "        elif False:\n            fault("),
    "ovqa_zip_sha_unchecked": ("        if (n, s256) != OVQA_DEV_ZIP:\n", "        if False:\n"),
    "skeleton_leaks_values": ('    out = {"type": type(v).__name__}\n', '    out = {"type": type(v).__name__, "v": str(v)[:80]}\n'),
    "custody_mnt_allowed": ('    if str(dest.resolve()).startswith("/mnt/"):\n', "    if False:\n"),
    "refusal_removed": ('|/dev/shm/c_pvr_gb|nocaps_val_4500_captions\\.json", re.I)', '|/dev/shm/c_pvr_gb", re.I)'),
}
EQUIV = {
    # Proof: merge_units leaves units with i0(next) >= i1(this), so nxt >= i1; right() only increments, so
    # right(i1) >= i1. Hence max(min(r, nxt), i1) = min(r, nxt) = min(max(r, i1), nxt). The rewritten form only
    # matters if merging were removed, which no_merge covers (check_props then fires).
    "b_old_form": ("b = max(min(right(i1), nxt), i1)", "b = min(max(right(i1), i1), nxt)"),
}
src_path, root, S = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
if str(S.resolve()).startswith("/mnt/"):
    raise SystemExit("scratch dir must not be under /mnt (EIO mitigation)")
src = src_path.read_text()
S.mkdir(parents=True, exist_ok=True)


def run(name, a, b):
    if src.count(a) != 1:
        return f"PATTERN({src.count(a)})"
    p = S / f"{name}.py"
    p.write_text(src.replace(a, b))
    r = subprocess.run([sys.executable, "-I", "-B", str(p), "selftest", "--root", root], capture_output=True, text=True)
    return "SURVIVED" if r.returncode == 0 and "selftest ok" in r.stdout else "KILLED"


if run("_original", "#!/usr/bin/env python3\n", "#!/usr/bin/env python3\n") != "SURVIVED":
    raise SystemExit("the unmutated copy does not pass its selftest; no mutant is counted")
res, eq = {}, {}
for table, out in ((M, res), (EQUIV, eq)):
    for n, ab in table.items():
        out[n] = run(n, *ab)
        print(f"{n:28s} {out[n]}", flush=True)
print(f"mutants {len(M)}: killed {sum(v == 'KILLED' for v in res.values())}, other "
      f"{[n for n, v in res.items() if v != 'KILLED']}; equivalent {len(EQUIV)}: {eq}")
