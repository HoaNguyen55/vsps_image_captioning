#!/usr/bin/env python3
"""Mutant harness for scripts/c_pvr_gpu/c_pvr_gpu.py (pattern of scripts/c_pvr/c_pvr_mutants.py).
Usage: <venv python> -I -B c_pvr_gpu_mutants.py <repo root> <empty scratch dir outside /mnt>.
The scratch dir gets scripts/c_pvr/{c_pvr.py,c_pvr_run.py,prompts/} and one mutated scripts/c_pvr_gpu/c_pvr_gpu.py per mutant
(set M), then one mutated scripts/c_pvr_gpu/c_pvr_manifest.py per mutant beside the unmutated c_pvr_gpu.py (set MB, P5).
Each mutant replaces one exact string (it must occur once) and runs `selftest` on the copy. The unmutated copy runs
first and must print 'selftest ok'. KILLED = the selftest fails.
Then c_pvr_job.sh (CC-270 N9): the unmutated script must pass every dry-run case of job_dry() under <scratch>/job, and
each J mutant must fail at least one case (KILLED). The two tallies are printed separately."""
import shutil
import subprocess
import sys
from pathlib import Path

M = {
    # money (T1-REP §9, host v3 §3)
    "cut_order_swapped": ('CUT_ORDER = ("A10", "A5",', 'CUT_ORDER = ("A5", "A10",'),
    "t_down_omitted": ("return (m - s - T_DOWN_H * r) // r", "return (m - s) // r"),
    "fit_strict_lt": ("return ceil125(sum(left.values()) + fixed_sec) <= h_m(m, s, r)",
                      "return ceil125(sum(left.values()) + fixed_sec) < h_m(m, s, r)"),
    "a8_wait_not_projected": ("return ceil125(sum(left.values()) + fixed_sec) <= h_m(m, s, r)",
                              "return ceil125(sum(left.values())) <= h_m(m, s, r)"),
    "r_host_rounded_down": ("r = math.ceil(Fraction(line))", "r = math.floor(Fraction(line))"),
    "speed_incomplete_silent": ('    if miss := sorted({a for _, _, arms in SETS.values() for a in arms} - set(rate)):',
                                '    if miss := []:'),
    "ceil_is_floor": ("return -(-5 * sec // 14400)", "return 5 * sec // 14400"),
    "pqc2_restores_cuts": ("        m = M_PQC2\n", "        m = M_PQC2\n        left, cuts = dict(arm_sec), []\n"),
    "pqc2_no_solvency": ("        if not pqc2_solvent:\n", "        if False:\n"),
    "timer_not_wall_clock": ('return int(cap["p1_epoch"] + cap["cap_h"] * 3600 - now)',
                             'return int(cap["cap_h"] * 3600)'),
    # loader, generation, echo (PINS-A §12 Q-LLAVA, Ruling 2)
    "weights_only_false_passes": ('        if k.get("weights_only", True) is not True:\n', "        if False:\n"),
    "genconfig_none_only": ("if k not in d or d[k] != v)", "if v is None and d.get(k) is not None)"),
    "echo_check_off": ("        if body in CP.clean(text) or CP.clean(text).startswith(body[:24]):\n",
                       "        if False:\n"),
    # ids only, datastores (meta item 17, OPS-1106c-datastores, CC-261 N6)
    "log_accepts_text": ("            if isinstance(x, str) and not ID_RX.fullmatch(x):\n", "            if False:\n"),
    "log_any_key": ("        if k not in keys:\n", "        if False:\n"),
    "kept_rehash_skipped": ("    if hashlib.sha256(b).hexdigest() != sha:\n", "    if False:\n"),
    "str_norm_removed": ("ids = [str(x) for x in (a.tolist() if hasattr(a, \"tolist\") else a)]",
                         "ids = list(a.tolist() if hasattr(a, \"tolist\") else a)"),
    "t2pool_allowed": ('BARRED = re.compile(r"\\.vsps_sealed|t2pool_", re.I)', 'BARRED = re.compile(r"\\.vsps_sealed", re.I)'),
    # decode and block rules (NB-SPEED, T1-REP R-1, host v3 §4.4)
    "speed_writes_captions": ('out = None if x.speed else open(outp, "a")', 'out = open(outp, "a")'),
    "never_cut_skipped": ("    for a in sorted(NEVER_CUT):\n        need(a)\n", ""),
    "a7_before_pvr_drop": ('PHASES = (("A1", "S3", "PVR-drop", "PVR-keep", "A12", "A0", "A6", "A7",',
                           'PHASES = (("A1", "S3", "A7", "PVR-drop", "PVR-keep", "A12", "A0", "A6",'),
    # CC-270 B1: the v1 set-major order, cuttable phase first, A10 not last, A8/S2 after the cuttable arms
    "set_major_order": ("for a in sum(PHASES, ()) for s, (_, lang, arms) in SETS.items()",
                        "for s, (_, lang, arms) in SETS.items() for a in sum(PHASES, ())"),
    "cuttable_first": ("for a in sum(PHASES, ()) for s", "for a in sum(PHASES[::-1], ()) for s"),
    "cut_tail_not_a10": ("          tuple(reversed(CUT_ORDER)))", "          CUT_ORDER)"),
    "a8_after_cuttable": ("for a in sum(PHASES, ()) for s", "for a in sum((PHASES[0], PHASES[2], PHASES[1]), ()) for s"),
    # CC-270 B2: the A8 wait bound, the decomposition arrival check, the wipe count of the mid-run push
    "a8_wait_unbounded": ("        if clock() - t0 > A8_WAIT_SEC:\n", "        if False:\n"),
    "a1_decomp_sha_unchecked": ("    if want.get(f.name) != hashlib.sha256(b).hexdigest():\n", "    if False:\n"),
    "a1_decomp_ids_unchecked": ("    if set(dec) != ids:\n", "    if False:\n"),
    "wipe_skips_a1_decomp": ('(d / "MANIFEST.sha256", d / "a1_decomp" / "MANIFEST.sha256")', '(d / "MANIFEST.sha256",)'),
    # CC-270 N9: DEMOCAP pins (W5) must refuse d_tc / d_en
    "democap_need_removed": ('    if ds != "d_vi":\n        need(f"DEMOCAP_{ds}")\n', ""),
    "speed_log_full": ("        keep = SPEED_LOG if x.speed else LOG_KEYS", "        keep = LOG_KEYS"),
    "hostcheck_sha_unchecked": ("    if {k: rep.get(k) for k in now} != now:\n", "    if False:\n"),
    "wipe_ignores_count": ("    return 0 if files == expect else 5", "    return 0"),
    # N8 demonstration caption (CC-269r2 Ruling 4, W2-W3) and S9 helper pins (S9 §8.1)
    "democap_last_caption": ('        first.setdefault(str(a["image_id"]), a["caption"])',
                             '        first[str(a["image_id"])] = a["caption"]'),
    "democap_int_key": ('        first.setdefault(str(a["image_id"]), a["caption"])',
                        '        first.setdefault(a["image_id"], a["caption"])'),
    "democap_src_unhashed": ("    return json.loads(pinned_bytes(src / fname, sha))", "    return json.loads((src / fname).read_bytes())"),
    "democap_manifest_unchecked": ('    if bad := [i for i, d in M["demos"].items() if d["text"] != want[i]]:',
                                   '    if bad := []:'),
    "helper_blob_as_sha256": ('        if (s256 if kind == "lfs" else s1) != want:', '        if s256 != want:'),
    # CC-270r2 N1': the r_host string form and its range
    "r_host_no_fullmatch": ('    if not re.fullmatch(r"[0-9]+(\\.[0-9]+)?", line):\n', "    if False:\n"),
    "r_host_unicode_digits": ('re.fullmatch(r"[0-9]+(\\.[0-9]+)?", line)', 're.fullmatch(r"\\d+(\\.\\d+)?", line)'),
    "r_host_no_range": ("    if not R_HOST[0] <= r <= R_HOST[1]:\n", "    if r <= 0:\n"),
    # CC-270 P2: S9 passes (A4 / A9 M-CLIP, A5 XGLM, A10 two calls), D-VI only, outputs-only answers and scores
    "t_a_keeps_s9": ('tuple(a for a in VI_ARMS if a not in ("A12", *S9_ARMS))),', 'tuple(a for a in VI_ARMS if a != "A12")),'),
    "sets_ok_off": ("    if bad := [(s, a) for s, (ds, _, arms) in SETS.items() for a in arms if a in S9_ARMS and ds != \"d_vi\"]:",
                    "    if bad := []:"),
    "a5_loads_mblip": ('else "xglm" if x.arm == "A5" else "mblip")', 'else "mblip")'),
    "mclip_not_closed": ("        pass_sec = clock() - s0\n        close()\n", "        pass_sec = clock() - s0\n"),
    "mclip_after_generator": ('    gen, _ = load("llava" if x.arm in EN_ARMS else "xglm" if x.arm == "A5" else "mblip")\n'
                              '    t0, n = clock() - pass_sec, 0\n',
                              "    t0, n = clock() - pass_sec, 0\n"),
    "a9_no_mclip_pass": ('    if x.arm in ("A4", "A9"):\n        score, close', '    if x.arm == "A4":\n        score, close'),
    "a4_prop_text_scored": ('        rows = CP.a4_texts([M["demos"][i] for i in ranked[:CP.K]])\n',
                            '        rows = [[p["text"] if p["kind"] == "obj" else None for p in M["demos"][i]["props"]]'
                            ' for i in ranked[:CP.K]]\n'),
    "a9_rank_order": ("        ids = CP.a9_pick(ranked[:CP.A9_POOL], sc)\n", "        ids = ranked[:CP.K]\n"),
    "mclip_fp16": ("model.encode_text(tok(texts).to(dev)).float()", "model.encode_text(tok(texts).to(dev)).float().half()"),
    "mclip_trunc_ge": ("> tok.context_length for x in texts)", ">= tok.context_length for x in texts)"),
    "a5_shots_unchecked": ("    if sorted(got) != sorted(want):\n", "    if False:\n"),
    "a5_shot_self_kept": ("caps = [i for i in norm_ids(got[s], kept) if i != s][:CP.K]",
                          "caps = [i for i in norm_ids(got[s], kept)][:CP.K]"),
    "a10_answers_dropped": ('                st["answers"] = answers\n', ""),
    "answers_in_log": ('LOG_KEYS = {"utc", "set",', 'LOG_KEYS = {"answers", "scores", "utc", "set",'),
    "a4_scores_not_written": ('        st = {"scores": prior[q["id"]], "masks": masks}\n', '        st = {"masks": masks}\n'),
    # P3: EN arms (Q-LLAVA), S2 on S3 (CC-270r2 N5'), DEMOCAP by datastore (CC-270 Ruling 6), preflight per (set, arm)
    "preflight_no_democap": ('        if SETS[s][0] != "d_vi":\n            need(f"DEMOCAP_{SETS[s][0]}")\n', ""),
    "s2_reads_a1": ('A8_SRC = {"A8": "A1", "S2": "S3"}', 'A8_SRC = {"A8": "A1", "S2": "A1"}'),
    "s2_through_demos_for": ('    if base == "A8":\n        if not x.a1_decomp:', '    if x.arm == "A8":\n        if not x.a1_decomp:'),
    "en_loads_mblip": ('load("llava" if x.arm in EN_ARMS else "xglm" if x.arm == "A5" else "mblip")',
                       'load("xglm" if x.arm == "A5" else "mblip")'),
    "en_rec_arm_overwritten": ('if k in OUT_KEYS and k != "arm"}', "if k in OUT_KEYS}"),
    "en_need_skipped": ("    if x.arm in NEEDS:\n        need(NEEDS[x.arm])\n", ""),
    # CC-272 N4 (pools before any load), N6 (cap inside the M-CLIP pass), N7 (hostcheck records), N1 (refs/main)
    "pool_check_off": ("    pool_check(base, todo, M, kept)\n", ""),
    "pool_a9_k": ('CP.A9_POOL if arm == "A9"', 'CP.K if arm == "A9"'),
    "a5_shot_short": ("        if len(caps) != CP.K:\n", "        if False:\n"),
    "mclip_pass_no_cap": ("            if cap and left_sec(cap, clock()) <= 0:  # CC-272 N6", "            if False:  # CC-272 N6"),
    "xglm_check_off": ('    if not text.strip() or CP.clean(P["lmcap_block_vi.txt"])[:19] in CP.clean(text):\n', "    if False:\n"),
    "genconfig_spy_noop": ("    GenerationConfig.validate = validate\n", ""),
    "raw_sha_dropped": ('        if kind == "blob":\n            raw[f] = s256\n', ""),
    "ref_not_written": ("    ref.write_text(rev)\n", ""),
    "by_name_unchecked": ('    by_name_ok("clip336", tower)\n', ""),
    # P4: W5 per CC-270 Ruling 6 (D-EN / D-TC rules, routed by datastore); CC-273 N5 (genconfig per kind), N6
    "en_int_key": ('first.setdefault(str(i["cocoid"]), i["sentences"][0]["raw"])',
                   'first.setdefault(i["cocoid"], i["sentences"][0]["raw"])'),
    "en_second_sentence": ('i["sentences"][0]["raw"])', 'i["sentences"][1]["raw"])'),
    "en_any_split": ('        if i["split"] in ("train", "restval"):\n', "        if True:\n"),
    "en_train_only": ('        if i["split"] in ("train", "restval"):\n', '        if i["split"] == "train":\n'),
    "en_last_wins": ('first.setdefault(str(i["cocoid"]), i["sentences"][0]["raw"])',
                     'first[str(i["cocoid"])] = i["sentences"][0]["raw"]'),
    "tc_last_wins": ('first.setdefault(str(a["image_id"]), a.get("caption_str"))',
                     'first[str(a["image_id"])] = a.get("caption_str")'),
    "tc_skips_uncaptioned": ('first.setdefault(str(a["image_id"]), a.get("caption_str"))',
                             'a.get("caption_str") and first.setdefault(str(a["image_id"]), a["caption_str"])'),
    "first_caps_unclean": ("    return {i: CP.clean(first[i]) for i in ids}", "    return {i: first[i] for i in ids}"),
    "first_caps_no_fault": ("    if miss := [i for i in ids if not isinstance(first.get(i), str) or not CP.clean(first[i])]:",
                            "    if miss := []:"),
    "democap_tc_as_en": ('"d_tc": democap_tc,', '"d_tc": democap_en,'),
    "democap_en_as_vi": ('"d_en": democap_en}', '"d_en": demo_captions}'),
    "en_pin_wrong_file": ('src_json(src, *DEMO_PIN["karpathy"])', 'src_json(src, *DEMO_PIN["textcaps_train"])'),
    "genconfig_seen0": ('            out[kind]["genconfig"] = seen[-1]', '            out[kind]["genconfig"] = seen[0]'),
    "genconfig_stale_ok": ("            if len(seen) == n0:\n", "            if False:\n"),
    "en_hostcheck_unchecked": ("        hostcheck_fresh(hc_en)\n", "        pass\n"),
    "llava_code_unchecked": ('    for s, n in ((snap, "llava"), (tower, "clip336"), (code, "llava_code")):',
                             '    for s, n in ((snap, "llava"), (tower, "clip336")):'),
    # P5: CC-276 W1 (no source json on the host; derived file by datastore, pinned), W3, W5, W7; CC-270 Q4 (A12)
    "host_reads_src": ('    want = read_democap(x.democap, ds, M["democap_sha256"], kept)  # W1: no source json on the host',
                       '    want = DEMOCAP_RULE[ds](sorted(M["demos"]), x.src)'),
    "democap_file_not_by_ds": ('    doc = json.loads(pinned_bytes(d / f"{ds}.json", sha))',
                               '    doc = json.loads(pinned_bytes(d / "d_vi.json", sha))'),
    "democap_file_unpinned": ('    doc = json.loads(pinned_bytes(d / f"{ds}.json", sha))',
                              '    doc = json.loads((d / f"{ds}.json").read_bytes())'),
    "democap_ids_unchecked": ("CP.LABEL, ds) or set(t) != kept or any(", "CP.LABEL, ds) or any("),
    "labels_on_host_ok": ('    if any("absent" in q for q in qs):', "    if False:"),
    "a12_masks_unchecked": ('        if [len(m) for m in masks] != [len(dc["props"]) for dc in dcs] or any(', "        if False and any("),
    "a12_laptop_masks_ignored": ('        masks = q["a12_masks"]\n', '        masks = [[False] * len(dc["props"]) for dc in dcs]\n'),
    "w3_vi_empty_ok": ("        if not isinstance(cap, str) or not CP.clean(cap):  # CC-276 W3", "        if not cap:  # CC-276 W3"),
    "w3_first_caps_empty_ok": ("    if miss := [i for i in ids if not isinstance(first.get(i), str) or not CP.clean(first[i])]:",
                               "    if miss := [i for i in ids if not first.get(i)]:"),
    "democap_pin_tc_pending": ('    "DEMOCAP_d_tc": "CC-270 Ruling 6 + CC-276 Ruling 1 (P5) + W2 OPS-1106c-w2-dtc",', '    "DEMOCAP_d_tc": PENDING,'),
    "democap_pin_en_pending": ('    "DEMOCAP_d_en": "CC-270 Ruling 6 + CC-276 Ruling 1 (P5)",', '    "DEMOCAP_d_en": PENDING,'),
    "kept_glob": ("    b = pinned_bytes(kdir / fname, sha)\n",
                  '    b = pinned_bytes(next(p for p in sorted(kdir.glob("*_kept_ids.txt")) if p.name == fname), sha)\n'),
    "host_audit_off": ('    if HOST and event in ("open",', '    if False and event in ("open",'),
    "echo_en_noun_vi": ('    noun = "một con chó" if lang == "vi" else "a dog"', '    noun = "một con chó"'),
}
# P5 builder (c_pvr_manifest.py): ranking, demos coverage, the derived file, A12 masks, seal, atomic write
MB = {
    "rank_tie_desc": ("np.lexsort((cand, -r[cand]))", "np.lexsort((-cand, -r[cand]))"),
    "rank_ascending": ("np.lexsort((cand, -r[cand]))", "np.lexsort((cand, r[cand]))"),
    "rank_cut_short": ("np.partition(r, -n)[-n]", "np.partition(r, -n)[-n + 1]"),
    "n_rank_k": ("N_RANK = 7  #", "N_RANK = 4  #"),
    "emb_not_normalised": ("    return v / np.linalg.norm(v, axis=1, keepdims=True), sha(b)", "    return v, sha(b)"),
    "emb_missing_ok": ("    if miss := [i for i in ids if i not in row]:", "    if miss := []:"),
    "a2_not_in_demos": ('        need |= {i for q, r in zip(qids, ranked) for i in G.CP.pick("A2", q, r, kept)}', "        pass"),
    "shots_not_in_demos": ('        need |= set(want) | {i for r in M["a5_shots"].values() for i in r}', "        pass"),
    "democap_rule_by_id_form": ("    texts = G.DEMOCAP_RULE[ds](kept, src)", "    texts = G.demo_captions(kept, src)"),
    "dry_writes": ("    if not dry:\n        put(", "    if True:\n        put("),
    "decomp_text_unchecked": ('    if [d["text"] for d in dcs] != [texts[i] for i in order]:', "    if False:"),
    "a12_labels_shipped": ('        rec = {"id": q, "image": img,', '        rec = {"absent": [], "id": q, "image": img,'),
    "a12_absent_ignored": ('            absent = set(lab.get(q, {}).get("absent", []))', "            absent = set()"),
    "image_sha_of_name": ('"image_sha256": sha(G.guard(images / img).read_bytes())', '"image_sha256": sha(img.encode())'),
    "sizes_unchecked": ("    if len(rows) != SIZES[s] or (s in EXPLORE", "    if (s in EXPLORE"),
    "explore_unchecked": ("(s in EXPLORE and not all(map(G.CR.half, qids)))", "False"),
    "shots_draw_unchecked": ("        if sorted(i for i, _ in srows) != sorted(want):", "        if False:"),
    "seal_shot_check_off": ("    if hit := set(shots[0].values()) & ", "    if hit := set() & "),
    "seal_twice": ("    if man.exists():\n", "    if False:\n"),
    "put_overwrites_tmp": ('with open(tmp, "xb") as f:', 'with open(tmp, "wb") as f:'),
}


# CC-270 N9: c_pvr_job.sh dry run with stubbed PY (decode/selftest/pip faked; steps/left/wipe real), git, nvidia-smi.
# The copy's HC points into the scratch dir (the real /dev/shm path is never created); FREEZE_SHA = the fake freeze.
J = {
    "trap_before_lock": ("exec 9> $O/.job.lock\n",
                         'teardown() { $PY -I -B $X wipe --dir $HC --log $O/c_pvr_hc_deletions.log; say "EXIT $MODE"; }\n'
                         "trap teardown EXIT\nexec 9> $O/.job.lock\n"),
    "cap_mark_ignored": ('[ -e $MARK ] && stop "CAP_STOP.json exists: a cap stop is final"', "true"),
    "rc4_not_cap_stop": ("if [ $rc = 124 ] || [ $rc = 4 ]; then", "if [ $rc = 124 ]; then"),
    "speed_end_per_run": ("END=$(( $(cat $O/speed_start.epoch) + 5400 ))", "END=$(( $(date +%s) + 5400 ))"),
    "a8_no_decomp_arg": ("    case $ARM in A8|S2) ARGS+=(--a1-decomp $HC/a1_decomp/$SET.json);; esac\n", ""),
    "en_main_venv": ("  case $ARM in S[1-5]) PYS=$PYE;; *) PYS=$PY;; esac", "  PYS=$PY"),
    "en_freeze_unchecked": ('[ "$C_PVR_FREEZE_EN" = "$FREEZE_SHA_EN" ] || stop', "true || stop"),
    "src_arg_restored": ("--images $HC/images/$SET --democap $HC/democap)", "--images $HC/images/$SET --src $HC/src)"),
}
FAKE_PY = r"""#!/bin/bash
echo "$0 $*" >> "$DRY_CALLS"
[ "$1 $2 $3" = "-m pip freeze" ] && { case "$0:${DRY_EN_BAD:-}" in *c_pvr_llava_*:1) echo other;; *) echo "torch==2.6.0+cu124";; esac; exit 0; }
case "$4" in
  selftest|hostcheck) exit 0;;
  preflight) exit ${DRY_PREFLIGHT_RC:-0};;
  decode) a=("$@"); for i in "${!a[@]}"; do case "${a[$i]}" in --set) S=${a[$((i+1))]};; --arm) A=${a[$((i+1))]};; esac; done
          [ "$S $A" = "${DRY_RC4:-}" ] && exit 4; [ "$S $A" = "${DRY_RC1:-}" ] && exit 1; exit 0;;
  *) exec "$DRY_REALPY" "$@";;
esac
"""


def job_dry(root: Path, base: Path, text: str) -> list[str]:
    """Run the job-script cases on `text`; return the names of the cases that fail (empty = all hold)."""
    import hashlib
    import json
    import os
    import time
    fails = []
    if base.exists():
        shutil.rmtree(base)  # only ever a dir this harness created inside its own scratch
    repo, home, fb = base / "repo", base / "home", base / "bin"
    shutil.copytree(root / "scripts/c_pvr/prompts", repo / "scripts/c_pvr/prompts")
    for f in ("c_pvr.py", "c_pvr_run.py"):
        shutil.copy2(root / "scripts/c_pvr" / f, repo / "scripts/c_pvr" / f)
    g = repo / "scripts/c_pvr_gpu"
    g.mkdir()
    for f in ("c_pvr_gpu.py", "requirements_c_pvr_gpu.lock", "requirements_c_pvr_llava.lock"):
        shutil.copy2(root / "scripts/c_pvr_gpu" / f, g / f)
    hc = base / "hc"
    freeze = hashlib.sha256(b"torch==2.6.0+cu124\n").hexdigest()
    for a, b in (("HC=/dev/shm/c_pvr_hc;", f"HC={hc};"), ("FREEZE_SHA=PENDING ", f"FREEZE_SHA={freeze} "),
                 ("FREEZE_SHA_EN=PENDING ", f"FREEZE_SHA_EN={freeze} ")):
        if text.count(a) != 1:
            raise SystemExit(f"job.sh pattern {a!r} occurs {text.count(a)} times")
        text = text.replace(a, b)
    (g / "c_pvr_job.sh").write_text(text)
    sums = lambda d, names: "".join(  # noqa: E731
        f"{hashlib.sha256((repo / d / n).read_bytes()).hexdigest()}  {d}/{n}\n" for n in names)
    (g / "SHA256SUMS").write_text(sums("scripts/c_pvr_gpu", ("c_pvr_gpu.py", "c_pvr_job.sh",
                                                            "requirements_c_pvr_gpu.lock",
                                                            "requirements_c_pvr_llava.lock")))
    (repo / "scripts/c_pvr/SHA256SUMS").write_text(sums("scripts/c_pvr", ("c_pvr.py", "c_pvr_run.py")))
    lk = hashlib.sha256((g / "requirements_c_pvr_gpu.lock").read_bytes()).hexdigest()[:8]
    lke = hashlib.sha256((g / "requirements_c_pvr_llava.lock").read_bytes()).hexdigest()[:8]
    py, pye = home / f"venvs/c_pvr_gpu_{lk}/bin/python", home / f"venvs/c_pvr_llava_{lke}/bin/python"
    fb.mkdir(parents=True)
    py.parent.mkdir(parents=True)
    pye.parent.mkdir(parents=True)
    for p, body in ((py, FAKE_PY), (pye, FAKE_PY), (fb / "git", '#!/bin/bash\n[ "$1" = rev-parse ] && echo "$DRY_HEAD"; exit 0\n'),
                    (fb / "nvidia-smi", "#!/bin/bash\necho 'NVIDIA GeForce RTX 3090'\n")):
        p.write_text(body)
        p.chmod(0o755)
    o = home / "c_pvr_out"
    head = "a" * 40

    def case(mode, cap=None, env=(), pre=None, run_head=head):
        if o.exists():
            shutil.rmtree(o)
        (o / "logs").mkdir(parents=True)
        (o / "mblip_snapshot.path").write_text("/nonexistent\n")
        (o / "HOSTCHECK_OK.json").write_text("{}\n")
        (o / "HOSTCHECK_EN_OK.json").write_text("{}\n")
        if cap:
            (o / "CAP.json").write_text(json.dumps({"decision": "RUN", "cap_h": 1, "p1_epoch": int(time.time())} | cap))
        if hc.exists():
            shutil.rmtree(hc)
        hc.mkdir(mode=0o700)
        (hc / "a.bin").write_bytes(b"x")
        (hc / "MANIFEST.sha256").write_text(f"{hashlib.sha256(b'x').hexdigest()}  a.bin\n")
        tman = hashlib.sha256((hc / "MANIFEST.sha256").read_bytes()).hexdigest()
        if pre:
            pre()
        calls = base / "calls.txt"
        calls.write_text("")
        e = {"PATH": f"{fb}:/usr/bin:/bin", "HOME": str(home), "DRY_CALLS": str(calls), "DRY_HEAD": head,
             "DRY_REALPY": sys.executable, **dict(env)}
        cmd = ["bash", str(g / "c_pvr_job.sh"), mode, run_head, tman]
        if "lock" in dict(env):
            cmd = ["flock", str(o / ".job.lock")] + cmd
        r = subprocess.run(cmd, capture_output=True, text=True, env=e, timeout=600)
        log = (o / "logs/job.log").read_text() if (o / "logs/job.log").exists() else ""
        dec = [ln.split() for ln in calls.read_text().splitlines() if " decode " in f" {ln} "]
        return r, log, dec, hc.exists()

    def check(name, ok):
        if not ok:
            fails.append(name)

    r, log, dec, alive = case("tier1", {"arms": ["A1"]}, env={"lock": "1"})
    check("lock_held_refused_hc_kept", r.returncode == 1 and "REFUSED" in r.stdout and alive and "EXIT" not in log)
    r, log, dec, alive = case("tier1", {"arms": ["A1"]}, pre=lambda: (o / "CAP_STOP.json").write_text("{}"))
    check("cap_mark_final", r.returncode == 1 and "CAP_STOP.json exists" in log and not dec and not alive
          and "EXIT tier1 rc=1" in log)
    r, log, dec, alive = case("tier1", {"arms": ["A1"]}, run_head="b" * 40)
    check("head_mismatch", r.returncode == 1 and "HEAD is not" in log and not dec and not alive)
    r, log, dec, alive = case("tier1", {"arms": ["A1"]}, env={"DRY_PREFLIGHT_RC": "1"})
    check("preflight_refusal", r.returncode == 1 and "pins PENDING" in log and not dec and not alive)
    r, log, dec, alive = case("tier1", {"arms": ["A1"], "p1_epoch": 0})
    check("cap_before_step", r.returncode == 0 and "CAP STOP cap reached before" in log and not dec
          and (o / "CAP_STOP.json").exists())
    r, log, dec, alive = case("tier1", {"arms": ["A1", "A8", "A11"]}, env={"DRY_RC4": "xm3600_vi A11"})
    arms = [d[d.index("--arm") + 1] for d in dec]
    a8 = [d for d in dec if d[d.index("--arm") + 1] == "A8"]
    dl = (o / "c_pvr_hc_deletions.log").read_text().split("\t") if (o / "c_pvr_hc_deletions.log").exists() else []
    check("rc4_cap_stop_then_wipe", r.returncode == 0 and (o / "CAP_STOP.json").exists() and not alive
          and log.index("CAP STOP during xm3600_vi A11") < log.index("EXIT tier1 rc=0") and dl[2:] == ["2", "2\n"]
          and "WIPE COUNT MISMATCH" not in log)
    check("democap_arg_no_src", dec and all("--src" not in d and d[d.index("--democap") + 1] == f"{hc}/democap"
                                            for d in dec if "--democap" in d) and all("--democap" in d for d in dec))
    check("phased_order_in_job", arms == ["A1"] * 5 + ["A8"] * 5 + ["A11"] and len(a8) == 5 and all(
        d[d.index("--a1-decomp") + 1] == f"{hc}/a1_decomp/{d[d.index('--set') + 1]}.json" for d in a8
        if "--a1-decomp" in d) and all("--a1-decomp" in d for d in a8))
    r, log, dec, alive = case("tier1", {"arms": ["A1", "S3", "S2"]})  # P3: EN venv per arm, S2 bound to kt_c's push
    arms = [d[d.index("--arm") + 1] for d in dec]
    s2 = [d for d in dec if d[d.index("--arm") + 1] == "S2"]
    check("en_venv_s2_decomp", r.returncode == 0 and arms == ["A1"] * 5 + ["S3", "S2"] and all(
        ("/c_pvr_llava_" in d[0]) == (d[d.index("--arm") + 1] in ("S3", "S2")) for d in dec)
        and len(s2) == 1 and "--a1-decomp" in s2[0] and s2[0][s2[0].index("--a1-decomp") + 1] == f"{hc}/a1_decomp/kt_c.json"
        and all("--a1-decomp" not in d for d in dec if "S3" in d))
    r, log, dec, alive = case("tier1", {"arms": ["A1"]}, env={"DRY_EN_BAD": "1"})
    check("en_freeze_mismatch", r.returncode == 1 and "EN venv freeze differs" in log and not dec and not alive)
    r, log, dec, alive = case("speed", env={"DRY_RC1": "xm3600_vi A1"})
    stamp = o / "speed_start.epoch"
    check("speed_stamp_written", r.returncode == 1 and stamp.exists() and len(dec) == 1)
    r, log, dec, alive = case("speed", pre=lambda: (o / "speed_start.epoch").write_text(f"{int(time.time()) - 6000}\n"))
    check("speed_total_1h30", r.returncode == 1 and "speed test over 1.5 h before" in log and not dec)
    return fails


def main() -> int:
    root, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    if str(scratch).startswith("/mnt/") or any(scratch.iterdir()):
        raise SystemExit("scratch must be an empty dir outside /mnt")
    shutil.copytree(root / "scripts/c_pvr/prompts", scratch / "scripts/c_pvr/prompts")
    for f in ("c_pvr.py", "c_pvr_run.py"):
        shutil.copy2(root / "scripts/c_pvr" / f, scratch / "scripts/c_pvr" / f)
    (scratch / "scripts/c_pvr_gpu").mkdir()
    survived = []
    for fname, muts in (("c_pvr_gpu.py", M), ("c_pvr_manifest.py", MB)):
        src = (root / "scripts/c_pvr_gpu" / fname).read_text("utf-8")
        dst = scratch / "scripts/c_pvr_gpu" / fname

        def run(text: str) -> bool:
            dst.write_text(text, "utf-8")
            r = subprocess.run([sys.executable, "-I", "-B", str(dst), "selftest"], capture_output=True, text=True,
                               env={"PATH": "/usr/bin:/bin", "HF_HUB_OFFLINE": "1"})
            return r.returncode == 0 and "selftest ok" in r.stdout

        if bad := [n for n, (a, _) in muts.items() if src.count(a) != 1]:
            raise SystemExit(f"{fname}: patterns not occurring once: {bad}")
        if not run(src):
            raise SystemExit(f"the unmutated {fname} fails its selftest")
        gone = []
        for name, (a, b) in muts.items():
            killed = not run(src.replace(a, b))
            print(f"{'KILLED' if killed else 'SURVIVED'}  {fname}:{name}")
            if not killed:
                gone.append(name)
        dst.write_text(src, "utf-8")  # the builder imports the unmutated c_pvr_gpu.py
        print(f"{fname} {len(muts) - len(gone)}/{len(muts)} killed")
        survived += gone
    job = (root / "scripts/c_pvr_gpu/c_pvr_job.sh").read_text("utf-8")
    if bad := job_dry(root, scratch / "job", job):
        raise SystemExit(f"the unmutated c_pvr_job.sh fails its dry run: {bad}")
    print("job dry run ok (unmutated)")
    js = []
    for name, (a, b) in J.items():
        if job.count(a) != 1:
            raise SystemExit(f"{name}: pattern occurs {job.count(a)} times")
        failed = job_dry(root, scratch / "job", job.replace(a, b))
        print(f"{'KILLED' if failed else 'SURVIVED'}  job:{name}  {failed}")
        if not failed:
            js.append(name)
    print(f"job.sh {len(J) - len(js)}/{len(J)} killed")
    return 1 if survived or js else 0


if __name__ == "__main__":
    sys.exit(main())
