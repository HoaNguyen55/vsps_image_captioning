"""Mutation check: each mutant edits a COPY of the package (never the package itself); the copy's test_o31.py must
fail on every one. Own mutants M01-M27, W3/W5, G01-G30 (g12b), S/G31-G37/O (g12c), X/Q/V (g12d),
P/C/T/G41-G49/A/H (PKG1: C06, C23, C24, C22, C13, N9, the host_selftest call), SM (pkgS: CC-529 W3, the student
smoke), and the 35 judge mutants of CC-504.

    $PY -I -B mutants.py        exit 0 iff every mutant is killed and every mutation site exists exactly once
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent

MUTANTS = [
    ("M01 reject on any NO", "verify.py", 'if states and all(s == "NO" for s in states):', 'if "NO" in states:'),
    ("M02 missing family ignored", "verify.py", "states = [family_state(scores.get(f), tau_acc, tau_rej) for f in families]",
     "states = [family_state(scores.get(f), tau_acc, tau_rej) for f in families if f in scores]"),
    ("M03 accept strict >", "verify.py", 'return "YES" if s >= tau_acc', 'return "YES" if s > tau_acc'),
    ("M04 spatial not forced", "verify.py", "if ptype in ALWAYS_UNCERTAIN:", "if False:"),
    ("M05 recall micro in K0", "gate.py", '"R": 100 * sum(recalls) / len(recalls)', '"R": 100 * tp / sum(len(g) for g, _ in pairs if g)'),
    ("M06 floor -3.0", "gate.py", "R_GOAL, FLOOR_DROP = 47.1, 2.0", "R_GOAL, FLOOR_DROP = 47.1, 3.0"),
    ("M07 OP* tie -> lower P", "gate.py", 'key=lambda ip: (ip[1]["R"], ip[1]["P"], -ip[0])', 'key=lambda ip: (ip[1]["R"], -ip[1]["P"], -ip[0])'),
    ("M08 K0 strict >", "gate.py", '"pass": star["R"] >= R_GOAL', '"pass": star["R"] > R_GOAL'),
    ("M09 budget floor 4", "store.py", "K_SCALE, B_MIN, B_MAX, B_FAIR = 1.5, 5, 15, 9", "K_SCALE, B_MIN, B_MAX, B_FAIR = 1.5, 4, 15, 9"),
    ("M10 budget floor() not ceil", "store.py", "math.ceil(K_SCALE * n)", "math.floor(K_SCALE * n)"),
    ("M11 S1 budget scaled too", "store.py", "b = budget(n_supp_entities(rec)) if scaled else B_FAIR", "b = budget(n_supp_entities(rec))"),
    ("M12 CMP k = max", "metrics.py", "k = min(len(ux), len(uy))", "k = max(len(ux), len(uy))"),
    ("M13 CMP ignores order", "metrics.py", "ux, uy = list(dict.fromkeys(order_x)), list(dict.fromkeys(order_y))",
     "ux, uy = sorted(set(order_x)), sorted(set(order_y))"),
    ("M14 null side exclusive", "metrics.py", 'on = (rep <= null) if side == "le" else (rep >= null)',
     'on = (rep < null) if side == "le" else (rep > null)'),
    ("M15 Holm without cummax", "metrics.py", "run = max(run, min(1.0, (m - i) * p[k]))", "run = min(1.0, (m - i) * p[k])"),
    ("M16 R per caption not per gold", "metrics.py", 'R = {k: 100 * _ratio(S[f"tp_{k}"], S[f"g_{k}"]) for k in (a, b, c)}',
     'R = {k: 100 * _ratio(S[f"tp_{k}"], S["n"]) for k in (a, b, c)}'),
    ("M17 H4 point condition dropped", "metrics.py", '"H4": point["H4.dRT"] >= H4_POINT', '"H4": True'),
    ("M18 H2 margin 0.5", "metrics.py", "ALPHA, MARGIN_H2, RHO_MIN, GAP_MIN = 0.05, 0.25, 0.50, 2.0",
     "ALPHA, MARGIN_H2, RHO_MIN, GAP_MIN = 0.05, 0.50, 0.50, 2.0"),
    ("M19 W4 (b) direction", "overlap.py", 'r = rule(feats[x], feats["uit_test"])', 'r = rule(feats["uit_test"], feats[x])'),
    ("M20 parity ignores image set", "decode.py", "if len(a) != PARITY_N or a.keys() != b.keys():", "if a.keys() != b.keys():"),
    ("M21 N_steps ceil", "train.py", "return epochs * (rows_s1 // grad_accum)", "return epochs * -(-rows_s1 // grad_accum)"),
    ("M22 mentions sorted by class", "extract.py", "key=lambda kv: (kv[1][0], kv[0])", "key=lambda kv: kv[0]"),
    ("M23 K0 keeps empty-gold images", "gate.py", "        if not gold:\n            continue\n        tp += len(m & gold)",
     "        tp += len(m & gold)"),
    ("M24 builder gets the caller's record", "store.py", "build(copy.deepcopy(rec), b)", "build(rec, b)"),
    ("M25 K0 driver accepts missing Q+", "gate.py", 'if n["miss"]:', "if False:"),
    ("M26 --exclude ignored", "gate.py", 'recs = [r for r in recs if r["file_name"] not in drop]', "recs = recs"),
    ("M27 reported sha not the written store", "gate.py", "sha = store.write_store(rows, Path(store_dir) / name) if store_dir",
     "sha = store.write_store(rows[::-1], Path(store_dir) / name) and store.store_sha(rows) if store_dir"),
    # G1/G2 probe runner and student decoder
    ("G01 vintern asks Q+ only", "probe.py", '            if mode == "all":', "            if False:"),
    ("G02 lower-case yes word dropped", "probe.py", 'YES_WORDS = ("Có", "có", " Có", " có")', 'YES_WORDS = ("Có", " Có")'),
    ("G03 probe right padding", "probe.py", '    tok.padding_side = "left"', '    tok.padding_side = "right"'),
    ("G04 probe first position", "probe.py", "net(**enc).logits[:, -1]", "net(**enc).logits[:, 0]"),
    ("G05 s = p(yes) unnormalised", "probe.py", "[(a / (a + b) if a + b > 0", "[(a if a + b > 0"),
    ("G06 parity tolerance 1e-2", "probe.py", "PROBE_TOL, PARITY_IMAGES, BATCHES = 1e-3, 50, (1, 8)",
     "PROBE_TOL, PARITY_IMAGES, BATCHES = 1e-2, 50, (1, 8)"),
    ("G07 parity image floor dropped", "probe.py", "ok = n_images >= PARITY_IMAGES and", "ok ="),
    ("G08 parity ignores top token", "probe.py", ' or k1[k]["top"] != kb[k]["top"]]', "]"),
    ("G09 resume re-asks done pairs", "probe.py", "todo = [(key, q) for key, q in qs if (name, key) not in have]",
     "todo = list(qs)"),
    ("G10 non-finite s kept", "probe.py", "                        if not math.isfinite(s):\n", "                        if False:\n"),
    ("G11 shard sha not re-checked", "probe.py", "        if _sha(out / name) != sha:", "        if False:"),
    ("G12 batch 8 without parity", "probe.py", 'rec["batch"] = 8 if rec["parity"]["ok"] else 1', 'rec["batch"] = 8'),
    ("G13 smoke mass floor dropped", "probe.py", "statistics.median(masses) >= MASS_FLOOR", "True"),
    ("G14 finalize pair check dropped", "probe.py", "if sorted(got) != sorted(want) or len(set(got)) != len(got):",
     "if False:"),
    ("G15 explored check dropped", "probe.py", "    if bad or len(names) != 5 or len(set(names)) != 5:", "    if False:"),
    ("G16 vintern batch 8", "probe.py", '"questions": "all", "batch": (1,)', '"questions": "all", "batch": (1, 8)'),
    ("G17 decode right padding", "decode.py", '    processor.tokenizer.padding_side = "left"', '    processor.tokenizer.padding_side = "right"'),
    ("G18 until_eos drops the stop token", "decode.py", "return ids[:k + 1], False", "return ids[:k], False"),
    ("G19 S0/adapter rule dropped", "decode.py", 'if (cfg.get("system") == "S0") != (cfg.get("adapter") is None):', "if False:"),
    ("G20 decode re-decodes done images", "decode.py", "todo = [it for it in items if it[0] not in have]", "todo = list(items)"),
    ("G21 decode image sha unchecked", "decode.py", "if hashlib.sha256(b).hexdigest() != h:", "if False:"),
    ("G22 parity record ignores mismatches", "decode.py", 'return record.get("batch") == 8 and record.get("mismatches") == {}',
     'return record.get("batch") == 8'),
    ("G23 mixed-batch resume allowed", "decode.py", 'if any(r["batch"] != batch for r in have.values()):', "if False:"),
    ("G24 adapter base unchecked", "decode.py", 'if cfg.get("base_model_name_or_path") != SETTINGS["base"]:', "if False:"),
    ("G25 max_new_tokens 200", "decode.py", '"max_new_tokens": 160,', '"max_new_tokens": 200,'),
    ("G26 Q13 decision ignores a system", "decode.py", "    for s in SYSTEMS:\n        a, b = tok_b1.get(s, {}), tok_b8.get(s, {})",
     "    for s in SYSTEMS[:2]:\n        a, b = tok_b1.get(s, {}), tok_b8.get(s, {})"),
    ("G27 smoke allows Karpathy test images", "probe.py", "or int(m.group(1)) in kar \\", "\\"),
    ("G28 smoke ignores refused bytes", "probe.py", "                or _sha(folder / n) in refused:", "                or False:"),
    ("G29 merged tables overwrite", "gate.py", "            if dup:\n                raise", "            if False:\n                raise"),
    ("G30 second table of a family dropped", "gate.py", "        spec.setdefault(f, []).append(p)", "        spec[f] = [p]"),
    # W5 (CC-504)
    ("W5a old model string", "verify.py", 'FAIR_MODEL = "5CD-AI/Vintern-1B-v3_5"', 'FAIR_MODEL = "vintern-1b"'),
    ("W5b no-Q+ sent to UNCERTAIN", "verify.py", "        if k is None:\n", "        if False:\n"),
    ("W5c no-Q+ guard skipped", "gate.py", 'if n["no_q_not_rejected"]:', "if False:"),
    # W3 (CC-504)
    ("W3a S2 path without uncap", "gate.py", "**arm(*store.uncap(recs), scaled=True, name=name)", "**arm(recs, {}, scaled=True, name=name)"),
    ("W3b S1 path without uncap", "gate.py", 's1 = arm(*store.uncap(records), scaled=False, name="S1")', 's1 = arm(records, {}, scaled=False, name="S1")'),
    ("W3c gender_uncap guard skipped", "store.py",
     'if any((p.get("backoff") or {}).get("kind") == "gender_uncap"', 'if False and any((p.get("backoff") or {}).get("kind") == "gender_uncap"'),
]


def _judge() -> list:
    """The 35 mutants of CC-504 (~/vsps_out/judge_cc504/expected_fixes/jmut_cc504.py), J34 re-pointed (W3 moved it)."""
    return [
        ("J01 rho 0.40", "metrics.py", "0.05, 0.25, 0.50, 2.0", "0.05, 0.25, 0.40, 2.0"),
        ("J02 gap 1.0", "metrics.py", "0.05, 0.25, 0.50, 2.0", "0.05, 0.25, 0.50, 1.0"),
        ("J03 H1 lo>=0", "metrics.py", "rho >= RHO_MIN and lo > 0", "rho >= RHO_MIN and lo >= 0"),
        ("J04 H2 hi<=0", "metrics.py", 'h2 = "PASS" if hi < 0 else "FAIL"', 'h2 = "PASS" if hi <= 0 else "FAIL"'),
        ("J05 CI lo idx +1", "metrics.py", "float(ok[int(0.025 * nb)])", "float(ok[int(0.025 * nb) + 1])"),
        ("J06 CI hi idx", "metrics.py", "float(ok[int(0.975 * nb) - 1])", "float(ok[int(0.975 * nb)])"),
        ("J07 rehearsal no replacement", "metrics.py", "sub = rng.integers(0, n, size=n_sub)", "sub = rng.choice(n, size=n_sub, replace=False)"),
        ("J08 gate 0.95", "metrics.py", '"gate": wins / b_out >= 0.98', '"gate": wins / b_out >= 0.95'),
        ("J09 H4 min", "metrics.py", '"H4": max(p_null(', '"H4": min(p_null('),
        ("J10 H4b null 0", "metrics.py", 'p_null(reps["H4.dFA"], H4_FA, "ge")', 'p_null(reps["H4.dFA"], 0.0, "ge")'),
        ("J11 H5b side le", "metrics.py", '"H5b": p_null(reps["en.D"], 0.0, "ge")', '"H5b": p_null(reps["en.D"], 0.0, "le")'),
        ("J12 seed main", "metrics.py", "B_MAIN, SEED_MAIN = 10_000, 20261127", "B_MAIN, SEED_MAIN = 10_000, 20261128"),
        ("J13 B main 1000", "metrics.py", "B_MAIN, SEED_MAIN = 10_000, 20261127", "B_MAIN, SEED_MAIN = 1_000, 20261127"),
        ("J14 reh seed", "metrics.py", "B_OUT, B_IN, N_SUB, SEED_REH = 1_000, 1_000, 4_224, 20261128",
         "B_OUT, B_IN, N_SUB, SEED_REH = 1_000, 1_000, 4_224, 20261127"),
        ("J15 nan not null", "metrics.py", "(1 + int(on.sum()) + int(np.isnan(rep).sum()))", "(1 + int(on.sum()))"),
        ("J16 verdict unadjusted p", "metrics.py", '"verdict": "PASS" if adj[k] < ALPHA', '"verdict": "PASS" if p[k] < ALPHA'),
        ("J17 H3 null 0", "metrics.py", "H3_NULL, H4_POINT, H4_FA = -2.0, 10.0, 5.0", "H3_NULL, H4_POINT, H4_FA = 0.0, 10.0, 5.0"),
        ("J18 H4 point 5", "metrics.py", "H3_NULL, H4_POINT, H4_FA = -2.0, 10.0, 5.0", "H3_NULL, H4_POINT, H4_FA = -2.0, 5.0, 5.0"),
        ("J19 Q+ last probe", "verify.py", "            return qkey(q[\"question_vi\"])\n    return None",
         "            k = qkey(q[\"question_vi\"])\n    return locals().get('k')"),
        ("J20 budget max 20", "store.py", "K_SCALE, B_MIN, B_MAX, B_FAIR = 1.5, 5, 15, 9", "K_SCALE, B_MIN, B_MAX, B_FAIR = 1.5, 5, 20, 9"),
        ("J21 scale 2.0", "store.py", "K_SCALE, B_MIN, B_MAX, B_FAIR = 1.5, 5, 15, 9", "K_SCALE, B_MIN, B_MAX, B_FAIR = 2.0, 5, 15, 9"),
        ("J22 S1 B 5", "store.py", "K_SCALE, B_MIN, B_MAX, B_FAIR = 1.5, 5, 15, 9", "K_SCALE, B_MIN, B_MAX, B_FAIR = 1.5, 5, 15, 5"),
        ("J23 nsupp any type", "store.py", 'if p.get("type") == "entity" and', 'if'),
        ("J24 K0 goal 45", "gate.py", "R_GOAL, FLOOR_DROP = 47.1, 2.0", "R_GOAL, FLOOR_DROP = 45.0, 2.0"),
        ("J25 OPmid feasible only", "gate.py", "_, mid = min(enumerate(points),", "_, mid = min(feas,"),
        ("J26 load_table last", "gate.py", 't.setdefault(r["image"], {}).setdefault(r["q"], r["p_yes"])',
         't.setdefault(r["image"], {})[r["q"]] = r["p_yes"]'),
        ("J27 W4 pool last set only", "overlap.py", 'hit |= r["excluded"]', 'hit = r["excluded"]'),
        ("J28 seed_mean axis1", "metrics.py", "np.mean(np.stack(per_seed), axis=0)", "np.mean(np.stack(per_seed), axis=1)"),
        ("J29 parity batch 8 always", "decode.py", '"batch": 1 if mism else 8', '"batch": 8'),
        ("J30 min_supported 0", "store.py", "min_supported: int = 1", "min_supported: int = 0"),
        ("J31 tau order not enforced", "verify.py", "if not tau_rej < tau_acc:", "if False:"),
        ("J32 grid tau_acc missing 0.9", "verify.py", "TAU_ACC = (0.50, 0.60, 0.70, 0.80, 0.90)", "TAU_ACC = (0.50, 0.60, 0.70, 0.80)"),
        ("J33 reject strict <", "verify.py", 'else "NO" if s <= tau_rej', 'else "NO" if s < tau_rej'),
        ("J34 S1 from O31 states (re-pointed)", "gate.py", 's1 = arm(*store.uncap(records), scaled=False, name="S1")',
         's1 = arm(*store.uncap([verify.apply_states(r, {}, ("vintern",), 0.5, 0.1)[0] for r in records]), scaled=False, name="S1")'),
        ("J35 reh inner from full set", "metrics.py", "idx = rng.integers(0, n_sub, size=(c, n_sub))",
         "idx = rng.integers(0, n_sub, size=(c, n_sub)) * 0"),
    ]


MUTANTS += _judge()
LAUNCHERS = ("g12.py", "s35.py")
MUTANTS += [  # g12c: CC-519 W2 (G1 stage-1 wrapper), W3 (§3.5 launcher), N1, E4-E6
    ("S01 max-entities 10", "stage1.py", '"--max-entities", "8"', '"--max-entities", "10"'),
    ("S02 logit verifier", "stage1.py", '"--verifier-tiles", "4")', '"--verifier-tiles", "4", "--logit-verifier")'),
    ("S03 70 new images", "stage1.py", "N_TRAIN, N_RECORDS, N_NEW = 3769, 3700, 69", "N_TRAIN, N_RECORDS, N_NEW = 3769, 3700, 70"),
    ("S05 records outside train", "stage1.py", "if not set(TWINS) <= have or not have <= set(names):",
     "if not set(TWINS) <= have:"),
    ("S06 new count unchecked", "stage1.py", 'if len(new) != N_NEW or set(TWINS) & {i["file_name"] for i in new}:', "if False:"),
    ("S07 train json unpinned", "stage1.py", "if _sha(train_json) != KTVIC_TRAIN_SHA:", "if False:"),
    ("S08 tarball unpinned", "stage1.py", "if _sha(tar) != RECORDS_TAR_SHA:", "if False:"),
    ("S09 refused image allowed", "stage1.py", '\n           or _sha(kt / "images" / i["file_name"]) in refused]', "]"),
    ("S10 QWEN_MAX_PIXELS allowed", "stage1.py", 'if os.environ.get("QWEN_MAX_PIXELS"):', "if False:"),
    ("S11 online hub allowed", "stage1.py", 'if os.environ.get("HF_HUB_OFFLINE") != "1":', "if False:"),
    ("S12 transformers unchecked", "stage1.py", "if transformers.__version__ != TRANSFORMERS:", "if False:"),
    ("S13 cap timer off", "stage1.py", "    timer.start()\n", ""),
    ("S14 cap spent before start", "stage1.py", "    if left <= 0:", "    if False:"),
    ("S15 STOP ignored", "stage1.py",
     '    if (out / STOP).exists():\n        raise SystemExit(f"REFUSED: {out / STOP} exists; no resume without a ruling")\n    lf',
     "    lf"),
    ("S16 done without all 69", "stage1.py", "return 0 if rc == 0 and got == want else 5", "return 0 if rc == 0 else 5"),
    ("S17 cap stop unreported", "stage1.py", "    if g._stop:\n", "    if False:\n"),
    ("S18 Qwen refs/main unchecked", "stage1.py",
     'snap.name != QWEN["revision"] or not ref.is_file() \\\n            or ref.read_text().strip() != QWEN["revision"]:',
     'snap.name != QWEN["revision"]:'),
    ("S19 Qwen file pins unchecked", "stage1.py", "    LB.check_snapshot(m, snap)\n", ""),
    ("S20 FAIR flags not passed", "stage1.py", '"--out", str(rec_dir), *FAIR_ARGS]', '"--out", str(rec_dir)]'),
    ("G31 G2 partial records", "probe.py", "if n != N_TRAIN or not set(TWINS) <= drop:", "if not set(TWINS) <= drop:"),
    ("G32 G2 twins kept", "probe.py", "if n != N_TRAIN or not set(TWINS) <= drop:", "if n != N_TRAIN:"),
    ("G33 g12 G2 check skipped", "g12.py", '    if a.family == "internvl3":\n        probe.g2_inputs(a.records, a.exclude)\n', ""),
    ("G34 refused default empty", "g12.py", "else probe.refused_shas()", "else set()"),
    ("G35 other English prompt", "g12.py", "    if prompt != decode.PROMPTS[a.lang]:\n", "    if False:\n"),
    ("G36 E6 string", "decode.py", 'PROMPTS["en"] = "Describe this image in detail in English."',
     'PROMPTS["en"] = "Describe this image in English."'),
    ("G37 g12 stage1 env unchecked", "g12.py", "    stage1.check_env()\n", ""),
    ("O01 pool 3769", "overlap.py", 'EXPECT_N = {"pool": 3767,', 'EXPECT_N = {"pool": 3769,'),
    ("O02 tier3 4000", "overlap.py", '"karpathy_test": 5000, "tier3": 4224}', '"karpathy_test": 5000, "tier3": 4000}'),
    ("O03 id list unpinned", "overlap.py", "if hashlib.sha256((root / rel).read_bytes()).hexdigest() != want:", "if False:"),
    ("O04 twins in pool", "overlap.py", "for n in sorted(set(names) - set(TWINS))]", "for n in sorted(set(names))]"),
    ("O05 unreadable kept", "overlap.py", '    if f["unreadable"]:\n        raise SystemExit(f"FAULT {name}',
     '    if False:\n        raise SystemExit(f"FAULT {name}'),
    ("O06 image sha unchecked", "overlap.py", "if any(s is not None and s != got", "if False and any(s is not None and s != got"),
    ("O07 SSCD weights unpinned", "overlap.py", "w25.ok_sscd(sscd)", "str(sscd)"),
    ("O08 KV features unpinned", "overlap.py", "kv = w25.load(kval, KV_FEATS_SHA)", "kv = w25.load(kval)"),
    ("O09 KV count unchecked", "overlap.py",
     'if len(want) != EXPECT_N["tier3"] or len(keep) != len(want) or kv["unreadable"]:', 'if kv["unreadable"]:'),
    ("O10 pass without every set", "overlap.py", "if set(feat_files) != set(EXPECT_N):", "if False:"),
    ("O11 pass count unchecked", "overlap.py", 'if len(f["ids"]) != expect[k] or', 'if False and len(f["ids"]) != expect[k] or'),
    ("O12 twins not excluded", "overlap.py", 'excl = sorted(set(TWINS) | set(res["removed"]["pool"]))',
     'excl = sorted(set(res["removed"]["pool"]))'),
    ("O13 s35 pool train unpinned", "s35.py",
     "if a.train is None or hashlib.sha256(a.train.read_bytes()).hexdigest() != stage1.KTVIC_TRAIN_SHA:",
     "if a.train is None:"),
]
MUTANTS += [  # g12d: CC-521 W4 (stems, F3), W5 (release tree F1, seed F2), W7 (snapshot binding)
    ("X01 record names as .jpg", "stage1.py", 'names = {Path(m.name).stem for m in tf if', 'names = {Path(m.name).stem + ".jpg" for m in tf if'),
    ("X02 stems not mapped", "stage1.py", "have = {by_stem.get(s, s) for s in stems}", "have = set(stems)"),
    ("X03 shared stem allowed", "stage1.py", "    if len(by_stem) != N_TRAIN:\n", "    if False:\n"),
    ("X04 screening list unchecked", "stage1.py", 'if sorted(i["file_name"] for i in new) != sorted(screen):', "if False:"),
    ("X06 seed not set", "stage1.py", "    seed_all()\n", ""),
    ("X07 attention not recorded", "stage1.py",
     'rec.setdefault("attn_implementation", getattr(self, "attn_implementation", None))', "pass"),
    ("X08 HEAD rescap kept", "stage1.py", "        del sys.modules[k]\n", "        pass\n"),
    ("X09 release tree appended", "stage1.py", 'sys.path[:0] = [str(tree), str(tree / "scripts")]',
     'sys.path += [str(tree), str(tree / "scripts")]'),
    ("X10 release pins unchecked", "stage1.py", "if bad or files != set(pins):", "if files != set(pins):"),
    ("X11 extra release files", "stage1.py", "if bad or files != set(pins):", "if bad:"),
    ("X12 records matched by name", "stage1.py", 'want = sorted(Path(i["file_name"]).stem for i in new)',
     'want = sorted(i["file_name"] for i in new)'),
    ("Q01 Qwen snapshot not bound", "stage1.py", "    check_cache(snap, QWEN)\n", ""),
    ("V01 Vintern snapshot not bound", "stage1.py", "    check_cache(snap, VINTERN)\n", ""),
    ("V02 g12 Vintern binding skipped", "g12.py", "    stage1.check_vintern(a.vintern)\n", ""),
]

LAUNCHERS += ("ops5.py", "a8store.py", "g3v.py", "host_selftest.sh")  # PKG1 launchers and the host self-test
MUTANTS += [  # PKG1: CODE_NEEDS C06, C23, C24, C22, C13; CC-526 N9; the host_selftest call
    ("P01 M-C06a P_floor applied", "points.py", 'if p["sft_sha256"] not in excl]',
     'if p["sft_sha256"] not in excl and p["P"] >= d["P_floor"]]'),
    ("P02 M-C06b OP_mid sha not excluded", "points.py",
     'excl = {s1["sft_sha256"], d["op_star"]["sft_sha256"], d["op_mid"]["sft_sha256"]}',
     'excl = {s1["sft_sha256"], d["op_star"]["sft_sha256"]}'),
    ("P03 M-C06c tie to lower P", "points.py", '(abs(ip[1]["R"] - t), -ip[1]["P"], ip[0])',
     '(abs(ip[1]["R"] - t), ip[1]["P"], ip[0])'),
    ("P04 M-C06d identified with gap < 1.0", "points.py", "small = [g for g in gaps if g < GAP]",
     "small = [g for g in gaps if g < 0.0]"),
    ("P05 M-C06e no eligible point returns a point", "points.py", "        if not el:\n            step = 4",
     "        if False:\n            step = 4"),
    ("P06 M-C06f decimal arithmetic", "points.py", '(abs(ip[1]["R"] - t), -ip[1]["P"], ip[0])',
     '(abs(__import__("decimal").Decimal(repr(ip[1]["R"])) - __import__("decimal").Decimal(repr(t))), -ip[1]["P"], ip[0])'),
    ("P07 M-C06g equal R in grid order", "points.py", 'by_r = sorted(five, key=lambda lp: lp[1]["R"])',
     'by_r = sorted(five, key=lambda lp: (lp[1]["R"], -1 if lp[1]["grid_index"] is None else lp[1]["grid_index"]))'),
    ("P08 K0 FAIL not NOT RUN", "points.py", '    if not d["pass"]:\n        return {**out, "result": "NOT RUN"',
     '    if d["op_star"] is None:\n        return {**out, "result": "NOT RUN"'),
    ("P09 t25 at the midpoint", "points.py", "    t25 = a + 0.25 * (b - a)\n", "    t25 = a + 0.5 * (b - a)\n"),
    ("P10 OP_25 sha not excluded for OP_75", "points.py", '        excl.add(p["sft_sha256"])\n', ""),
    ("P11 preview accepted", "points.py", 'if k0.get("complete") is not True or k0.get("decision") is None:',
     'if k0.get("decision") is None and k0.get("preview_no_verdict") is None:'),
    ("P12 grid order unchecked", "points.py",
     '    if [p.get("op") for p in k0.get("points", [])] != [[a, r, list(f)] for a, r, f in verify.grid()]:',
     "    if False:"),
    ("P13 edge misses tau_rej 0.30", "points.py", "EDGE_TAU_ACC, EDGE_TAU_REJ = (0.50, 0.90), (0.10, 0.30)",
     "EDGE_TAU_ACC, EDGE_TAU_REJ = (0.50, 0.90), (0.10,)"),
    ("P14 guard ignores the result", "points.py", 'if rec.get("schema") != SCHEMA or rec.get("result") != "IDENTIFIED":',
     'if rec.get("schema") != SCHEMA:'),
    ("P15 guard ignores the store sha", "points.py",
     '    if hashlib.sha256(Path(store_sft).read_bytes()).hexdigest() != rec["five"][label]["sft_sha256"]:',
     "    if False:"),
    ("P16 guard ignores the sha line", "points.py", "    if not line or line[0] != sha:", "    if False:"),
    ("C01 M-C23a ops5 accepts a preview", "ops5.py", '    k0 = json.loads(raw.decode("utf-8"))\n',
     '    k0 = json.loads(raw.decode("utf-8"))\n    k0 = {**k0, "complete": True, "decision": k0["decision"] or k0["preview_no_verdict"]}\n'),
    ("C02 M-C23b ops5 overwrites", "ops5.py",
     '    if target.exists():\n        raise SystemExit(f"REFUSED {target} exists: ops5.json is written once")\n'
     '    fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)',
     "    fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)"),
    ("C03 M-C23c ops5 merges a second k0.json", "ops5.py", "    if len(a.k0) != 1:", "    if not a.k0:"),
    ("C04 M-C23d ops5 writes before C06 returns", "ops5.py", "    res = points.extra_points(k0)\n",
     '    a.out.mkdir(parents=True, exist_ok=True)\n    (a.out / "ops5.json").write_text("{}")\n'
     "    res = points.extra_points(k0)\n    (a.out / \"ops5.json\").unlink()\n"),
    ("T01 M-C24a sigma2 ddof 0", "t4.py", "np.mean([np.var(r_s1, ddof=1), np.var(r_s2, ddof=1)])",
     "np.mean([np.var(r_s1, ddof=0), np.var(r_s2, ddof=0)])"),
    ("T02 M-C24b one sigma2_seed", "t4.py", "den = [vk + 2 * s2 for vk in v]", "den = [vk + s2 for vk in v]"),
    ("T03 M-C24c min instead of max", "t4.py", '"p": max(pk)', '"p": min(pk)'),
    ("T04 M-C24d pairs by label", "t4.py", '    order = ops5["order_by_R"]', '    order = ops5["order_by_label"]'),
    ("T05 M-C24e reads a k0.json", "t4.py", 'if rec.get("schema") != points.SCHEMA or "points" in rec or "decision" in rec:',
     "if False:"),
    ("T06 zero denominator only when all k", "t4.py", "if any(x == 0 for x in den):", "if all(x == 0 for x in den):"),
    ("T07 decodes read before the ops5 result", "t4.py",
     '    if ops5.get("result") != "IDENTIFIED":\n        return',
     '    load_columns()\n    if ops5.get("result") != "IDENTIFIED":\n        return'),
    ("T08 p_k = Phi(z)", "t4.py", "pk = [1.0 - phi(zk) for zk in z]", "pk = [phi(zk) for zk in z]"),
    ("T09 V_k ddof defaulted", "t4.py", "    if vk_ddof is None:\n        raise", "    if vk_ddof is None:\n        vk_ddof = 0\n    if False:\n        raise"),
    ("T10 OP_mid student not A-1", "t4.py", '"OP_mid": "A-1"', '"OP_mid": "OP_mid"'),
    ("P17 R-order record in label order", "points.py", '"five_in_R_order": [{"label": lab, **e} for lab, e in by_r]',
     '"five_in_R_order": [{"label": lab, **e} for lab, e in five]'),
    ("G41 M-C22a question from the class name", "vcoco.py", 'q_plus(p["text_vi"]) for p in props', 'q_plus(p["cls"]) for p in props'),
    ("G42 M-C22b cap not applied", "vcoco.py", "G3V_CAP_H = 1.0", "G3V_CAP_H = 30.0"),
    ("G43 M-C22c K1 gate applied to G3v", "vcoco.py", "    t0 = clock(root)\n",
     '    t0 = clock(root)\n    if any(p.name.startswith("K1") for p in Path(root).parent.iterdir()):\n        return 0\n'),
    ("G44 second launch clock accepted", "vcoco.py",
     '            if json.loads(fl.read_text()).get("t0") != rec["t0"]:', "            if False:"),
    ("G45 another job's clock accepted", "vcoco.py", '        if rec.get("job") != JOB:', "        if False:"),
    ("G46 decode sidecar unchecked", "vcoco.py", "    if not line or line[0] != hashlib.sha256(preds_path.read_bytes()).hexdigest():",
     "    if False:"),
    ("G47 image custody unchecked", "vcoco.py", "        if got != h or got not in allowed:", "        if False:"),
    ("G48 K4 stop not reported NOT RUN", "vcoco.py", '    st["row"] = "NOT RUN" if "NOT RUN" in vals else',
     '    st["row"] = "INCOMPLETE" if "NOT RUN" in vals else'),
    ("G49 G3v size not 231", "g3v.py", "    if len(items) != vcoco.UIT_TEST_N:", "    if False:"),
    ("A01 M-C13a scaled=False", "a8.py", 'return arm_store(records, True, "A8", store_dir, build)',
     'return arm_store(records, False, "A8", store_dir, build)'),
    ("A02 M-C13b O31 verdicts applied", "a8.py", 'return arm_store(records, True, "A8", store_dir, build)',
     'from . import verify\n    return arm_store([verify.apply_states(r, {}, ("vintern",), 0.5, 0.1)[0] for r in records], True, '
     '"A8", store_dir, build)'),
    ("A03 A-8 without person_uncap", "a8.py", "    unc, ust = store.uncap(records)\n", "    unc, ust = records, {}\n"),
    ("A04 a8store.py ignores the exclusions", "a8store.py", '    recs = [r for r in recs if r["file_name"] not in drop]\n', ""),
    ("H01 host_selftest calls run_tests.sh by path", "host_selftest.sh", 'bash "$HERE/run_tests.sh"', '"$HERE/run_tests.sh"'),
]
MUTANTS += [  # CC-534 (ERRATUM_O31_G2): InternVL3 probes at batch 1; G2 cap 48 h from launch.json t0
    ("G50 InternVL3 batch 8 again", "probe.py", '"questions": "q_plus", "batch": (1,),', '"questions": "q_plus", "batch": BATCHES,'),
    ("G51 G2 cap back to 30 h", "probe.py", '"cap_h": 48.0},', '"cap_h": 30.0},'),
    ("G52 G2 cap 49 h", "probe.py", '"cap_h": 48.0},', '"cap_h": 49.0},'),
]
MUTANTS += [  # pkgS: CC-529 W3, the student smoke of g12.py
    ("SM01 smoke verdict on batch-5 equality", "g12.py", 'rec.get("ok_student", True)', 'rec.get("token_equal_b5", True)'),
    ("SM02 repeat equality not required", "g12.py", '"ok_student": b1 == b1r and all(', '"ok_student": all('),
    ("SM03 empty caption accepted", "g12.py", '"ok_student": b1 == b1r and all(t[1] for t in r1)}', '"ok_student": b1 == b1r}'),
    ("SM04 first_diff ignores a length difference", "g12.py", "if x != y), min(len(a), len(b)))", "if x != y), None)"),
    ("SM05 first_diff counts from 1", "g12.py", "enumerate(zip(a, b))", "enumerate(zip(a, b), 1)"),
    ("SM06 repeat pass reuses the first pass", "g12.py", "        b1r = [gen([im])[0][0] for im in ims]\n",
     "        b1r = b1\n"),
    ("SM07 same-image batch not of copies", "g12.py", "gen([ims[0]] * 5)", "gen(ims)"),
    ("SM08 stop id from the first token", "g12.py", "None if t[2] else t[0][-1]", "None if t[2] else t[0][0]"),
]


def main() -> int:
    py = sys.executable
    survived, bad_site = [], []
    with tempfile.TemporaryDirectory(prefix="o31_mut_") as tmp:
        for name, f, old, new in MUTANTS:
            dst = Path(tmp) / name.split()[0]
            shutil.copytree(HERE, dst, ignore=shutil.ignore_patterns("__pycache__", "*.log", "*.diff", "*.txt"))
            path = dst / f if f in LAUNCHERS else dst / "src" / "o31" / f  # launchers: the copy's own g12.py / s35.py
            text = path.read_text(encoding="utf-8")
            if text.count(old) != 1:
                bad_site.append(name)
                print(f"SITE {name}: pattern found {text.count(old)} times")
                continue
            path.chmod(0o644)
            path.write_text(text.replace(old, new), encoding="utf-8")
            r = subprocess.run([py, "-I", "-B", str(dst / "test_o31.py")], capture_output=True, text=True,
                               env={**os.environ, "O31_SRC": str(dst / "src"), "O31_FAILFAST": "1"})
            killed = r.returncode != 0
            fails = [ln.split(":")[0][5:] for ln in r.stdout.splitlines() if ln.startswith("FAIL")]
            print(f"{'killed  ' if killed else 'SURVIVED'} {name}  {fails[:3]}")
            if not killed:
                survived.append(name)
    print(f"{len(MUTANTS) - len(survived) - len(bad_site)}/{len(MUTANTS)} killed; survived {survived}; bad sites {bad_site}")
    return 1 if survived or bad_site else 0


if __name__ == "__main__":
    sys.exit(main())
