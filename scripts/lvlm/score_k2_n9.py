#!/usr/bin/env python3
"""Scorer for the E1 K2 seed placebo and the N9 count-matched leaderboard (the analysis script that the N9 prereg §8
and judge rule CC-018 require before any K2 or N9 output is scored).

Registrations: manuscript/prereg/2026-10-18_n9_count_matched_leaderboard.{md,json} and
manuscript/prereg/2026-10-18_e1_k2_placebo_addendum.md (commit b8b2500). Every threshold, seed, resample count,
comparator and expected count is read from the committed prereg JSON; every label is computed by rule.
The CHAIR matcher, gold, agg(), trunc_curve() and interp_loglog() come from scripts/lvlm/e1_chair_count.py, imported
unchanged. The sentence tie-average, the exact random-subset expectation, the TRF precision residual, the two-sided
bootstrap p and Holm are ported verbatim from .session_backup/2026-10-13/r10_cpu/run_e1_x1pb.py (E1J's generator).

Modes (run in this order; each later mode refuses to start without the earlier mode's passing output):
  e1check  re-scores E1's released outputs and must reproduce E1J pairs_15 point estimates of dP_MCP_prefix,
           dP_MCP_sent_tieavg, dP_MCP_rand_exact and dP_TRF_prefix exactly (3 decimals) for all 15 pairs.
  k2       K2 placebo: k2_seed2 minus k2_seed1; prediction, kill rule, admissibility, C* (addendum §3).
  kf       the K_F fidelity gate on n9_base alone (judge rule: scored first; may run while the methods decode).
  n9       K-protocol checks, then the K_F fidelity gate on the base alone (stops on FAIL, no method scored), then P1
           under C*, P2, the specification curve, CAR, dm, predictions (a)-(c) and the kill rules (prereg §4-§7).
Usage (CPU; python -I in a venv with numpy, or python3 -E -P where numpy sits in user site-packages):
  score_k2_n9.py e1check --coco-zip ZIP --opera DIR --lim DIR --out e1check.json
  score_k2_n9.py k2 --coco-zip ZIP --runs DIR --e1check e1check.json --out k2_scores.json
  score_k2_n9.py kf --coco-zip ZIP --runs DIR --e1check e1check.json [--lim-r1 r1.jsonl] --out kf.json   (base only)
  score_k2_n9.py n9 --coco-zip ZIP --runs DIR --e1check e1check.json --k2 k2_scores.json --lim-r1 r1.jsonl --out n9.json
  score_k2_n9.py selftest
"""
import argparse, hashlib, importlib.util, json, re, sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
PREREG = REPO / 'manuscript/prereg/2026-10-18_n9_count_matched_leaderboard.json'
PREREG_SHA = '2b232bd3a9e6663a35f3a33da6a1a3f2b9e7530dec44a1d84b08521df0cb6381'   # committed in b8b2500
E1J = REPO / '.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json'
MANIFEST = REPO / 'data/coco_probe/chair500_val2014.sha256'
SYN = REPO / 'data/coco_probe/chair_synonyms.txt'
CONTROLS = {'matched_prefix': 'mcp_pref', 'sentence_tie_average': 'mcp_sent', 'uniform_random_subset': 'mcp_rand'}
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
e1 = None


def load_e1(coco_zip, opera='', lim=''):
    """Import the unchanged E1 scorer; it reads SYN ZIP OPERA LIM OUT from sys.argv at import time."""
    global e1
    want = json.loads(PREREG.read_text())['inputs_sha256']['annotations_trainval2014.zip']
    if sha(coco_zip) != want:
        raise SystemExit(f'{coco_zip}: not the registered COCO annotations zip ({want})')
    saved = sys.argv
    sys.argv = ['e1_chair_count.py', str(SYN), str(coco_zip), str(opera), str(lim), '/dev/null']
    spec = importlib.util.spec_from_file_location('e1_chair_count', REPO / 'scripts/lvlm/e1_chair_count.py')
    e1 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(e1)
    sys.argv = saved


def registration():
    if sha(PREREG) != PREREG_SHA:
        raise SystemExit(f'{PREREG} is not the committed registration')
    r = json.loads(PREREG.read_text())
    num = lambda pat, s: [float(x) for x in re.fullmatch(pat, s).groups()]
    alpha, sesoi = num(r'Holm p < ([\d.]+) AND dP_Cstar >= \+([\d.]+)', r['primary_endpoints']['P1_object_choice']['survives'])
    alpha2, sesoi2 = num(r'Holm p < ([\d.]+) AND dP_TRF >= \+([\d.]+)', r['primary_endpoints']['P2_frontier_PD2_training_time']['off_frontier'])
    b_min, = num(r'D_b >= \+([\d.]+) AND 95% lower bound > 0', r['frozen_predictions']['b']['held'])
    b_kill, = num(r'D_b < ([\d.]+): drop \(b\).*', r['frozen_predictions']['b']['kill'])
    head_min, head_of = num(r'>= (\d+) of (\d+) methods SURVIVE on P1 .*', r['kill_rules']['K_headline'])
    return r, {'alpha': alpha, 'sesoi': sesoi, 'alpha_p2': alpha2, 'sesoi_p2': sesoi2, 'b_min': b_min, 'b_kill': b_kill,
               'headline_min': int(head_min), 'headline_of': int(head_of)}


# ------------------------------------------------ ported verbatim from run_e1_x1pb.py (E1J's generator)
def per_image_ext(cap, g):
    base = e1.per_image(cap, g)
    sents = [s.strip() for s in re.split(r"[.!?]+", cap) if s.strip()]
    seen, sent_groups = set(), []
    for s in sents:
        grp = []
        for n in e1.nodes(s):
            if n not in seen:
                seen.add(n)
                grp.append(n in g)
        if grp:
            sent_groups.append(grp)
    if len([x for grp in sent_groups for x in grp]) != len(base['tp']):
        sent_groups = [base['tp']]
    base['sent_groups'] = sent_groups
    return base


def sent_tie_avg_tp(sent_groups, k):
    rem, tp_exp = int(k), 0.0
    for grp in sent_groups:
        if rem <= 0:
            break
        if len(grp) <= rem:
            tp_exp += float(sum(grp))
            rem -= len(grp)
        else:
            tp_exp += float(rem) * (float(sum(grp)) / float(len(grp)))
            rem = 0
            break
    return tp_exp


def two_sided_boot_p(draws):
    valid = draws[~np.isnan(draws)]
    if len(valid) == 0:
        return 1.0
    p_pos = (np.sum(valid <= 0.0) + 1.0) / (len(valid) + 1.0)
    p_neg = (np.sum(valid >= 0.0) + 1.0) / (len(valid) + 1.0)
    return float(min(1.0, 2.0 * min(p_pos, p_neg)))


def holm_adjust(pvals):
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m, adj, running_max = len(items), {}, 0.0
    for idx, (k, p) in enumerate(items):
        running_max = max(running_max, min(1.0, (m - idx) * p))
        adj[k] = round(running_max, 6)
    return adj


# ------------------------------------------------ per-pair arrays and statistics (formulas of evaluate_pair_full)
def pair_arrays(B, X, ids):
    ids = np.array(ids)
    a = {'mX': np.array([len(X[i]['u']) for i in ids], float), 'tX': np.array([sum(X[i]['tp']) for i in ids], float),
         'mB': np.array([len(B[i]['u']) for i in ids], float), 'tB': np.array([sum(B[i]['tp']) for i in ids], float),
         'g': np.array([X[i]['g'] for i in ids], float)}
    k = np.minimum(a['mX'], a['mB'])
    a['k'] = k
    a['tx_pref'] = np.array([sum(X[i]['tp'][:int(q)]) for i, q in zip(ids, k)], float)
    a['tb_pref'] = np.array([sum(B[i]['tp'][:int(q)]) for i, q in zip(ids, k)], float)
    a['tx_sent'] = np.array([sent_tie_avg_tp(X[i]['sent_groups'], int(q)) for i, q in zip(ids, k)], float)
    a['tb_sent'] = np.array([sent_tie_avg_tp(B[i]['sent_groups'], int(q)) for i, q in zip(ids, k)], float)
    a['tx_rand'] = np.where(a['mX'] > 0, k * (a['tX'] / np.maximum(a['mX'], 1.0)), 0.0)
    a['tb_rand'] = np.where(a['mB'] > 0, k * (a['tB'] / np.maximum(a['mB'], 1.0)), 0.0)
    rows = [B[i] for i in ids]
    a['ks_mat'] = np.array([[min(q, len(r['u'])) for q in range(1, 13)] for r in rows], float)   # E1 trunc_curve, K=12
    a['tps_mat'] = np.array([[sum(r['tp'][:q]) for q in range(1, 13)] for r in rows], float)
    return a


def stats(a, s):
    ks = a['k'][s].sum()
    out = {c: 100.0 * (a['tx' + c[3:]][s].sum() - a['tb' + c[3:]][s].sum()) / ks for c in ('mcp_pref', 'mcp_sent', 'mcp_rand')}
    mx = a['mX'][s].mean()
    tp_hat = e1.interp_loglog(a['ks_mat'][s].mean(0), a['tps_mat'][s].mean(0), mx)
    out['trf'] = 100.0 * (a['tX'][s].mean() - tp_hat) / mx if not np.isnan(tp_hat) else np.nan
    out['raw'] = 100.0 * (a['tX'][s].sum() / a['mX'][s].sum() - a['tB'][s].sum() / a['mB'][s].sum())
    out['dR'] = 100.0 * (a['tX'][s].sum() - a['tB'][s].sum()) / a['g'][s].sum()
    out['dm'] = mx - a['mB'][s].mean()
    out['M_X'], out['M_B'], out['k_mean'] = mx, a['mB'][s].mean(), a['k'][s].mean()
    return out


def summarize(full, draws, key):
    v = np.array([d[key] for d in draws], float)
    lo, hi = (np.nanpercentile(v, [2.5, 97.5]) if np.any(~np.isnan(v)) else (np.nan, np.nan))
    f = lambda x: None if x is None or np.isnan(x) else round(float(x), 3)
    return {'est': f(full[key]), 'ci95': [f(lo), f(hi)], 'p_boot': round(two_sided_boot_p(v), 5),
            'n_valid_draws': int(np.sum(~np.isnan(v)))}


# ------------------------------------------------ mode e1check
def mode_e1check(args):
    load_e1(args.coco_zip, args.opera, args.lim)
    e1j = json.loads(E1J.read_text())
    sysd = e1.load_systems()
    gt, found = e1.load_gt(set().union(*[set(v) for v in sysd.values()]))
    P = {s: {i: per_image_ext(c[i], gt[i]) for i in c if i in found} for s, c in sysd.items()}
    rows, ok = {}, True
    for key, ref in e1j['pairs_15'].items():
        x, b = key.split(' vs ')
        common = sorted(set(P[b]) & set(P[x]))
        full = stats(pair_arrays(P[b], P[x], common), np.arange(len(common)))
        got = {'dP_MCP_prefix': full['mcp_pref'], 'dP_MCP_sent_tieavg': full['mcp_sent'], 'dP_MCP_rand_exact': full['mcp_rand'],
               'dP_TRF_prefix': full['trf']}
        cmp = {}
        for m, v in got.items():
            mine = None if np.isnan(v) else round(float(v), 3)
            cmp[m] = {'repro': mine, 'e1j': ref[m]['est'], 'match': mine == ref[m]['est']}
            ok &= cmp[m]['match']
        cmp['n_img'] = {'repro': len(common), 'e1j': ref['n_img'], 'match': len(common) == ref['n_img']}
        ok &= cmp['n_img']['match']
        rows[key] = cmp
    out = {'mode': 'e1check', 'script_sha256': sha(__file__), 'e1_scorer_sha256': sha(REPO / 'scripts/lvlm/e1_chair_count.py'),
           'e1j': {'path': str(E1J.relative_to(REPO)), 'sha256': sha(E1J)}, 'coco_zip_sha256': sha(args.coco_zip),
           'inputs_sha256': {f'{d.name}/{f.name}': sha(f) for d in (Path(args.opera), Path(args.lim)) for f in sorted(d.glob('*.jsonl'))},
           'n_pairs': len(rows), 'all_match': bool(ok), 'pairs': rows}
    Path(args.out).write_text(json.dumps(out, indent=1) + '\n')
    print(f'e1check: {len(rows)} pairs, all_match={ok}')
    return 0 if ok else 1


def require_e1check(path):
    """The e1check output must come from this script version, pass on all pairs and refer to the registered E1J sha
    (so it can be used where E1J itself is absent, e.g. on the GPU machine)."""
    d = json.loads(Path(path).read_text())
    e1j_sha = json.loads(PREREG.read_text())['inputs_sha256'][str(E1J.relative_to(REPO))]
    ok = (d.get('mode') == 'e1check' and d.get('all_match') is True and d.get('script_sha256') == sha(__file__)
          and d.get('e1j', {}).get('sha256') == e1j_sha and d.get('n_pairs') == len(d.get('pairs', {})) > 0
          and all(v['match'] for r in d['pairs'].values() for v in r.values()))
    if not ok:
        raise SystemExit('refusing to score: no passing e1check from this script version (prereg §8 step 4)')
    return {'path': str(path), 'sha256': sha(path)}


# ------------------------------------------------ decode outputs and K-protocol
def load_run(runs, label):
    p = Path(runs) / f'{label}.json'
    return json.loads(p.read_text()), {'path': str(p), 'sha256': sha(p)}


def protocol(reg, outs, spec_by_label, k2=None):
    """K-protocol (prereg §7). Returns the list of failures; scoring stops if it is not empty."""
    fail = []
    manifest = dict(reversed(l.split()) for l in MANIFEST.read_text().splitlines() if l.strip())
    decode_sha = reg['committed_files_sha256']['scripts/lvlm/decode_llava.py']
    ref = None
    for label, d in outs.items():
        need = lambda cond, what: cond or fail.append(f'{label}: {what}')
        need(d.get('schema') == 'vsps.decode_llava.v1' and d.get('label') == label, 'schema/label')
        need(d['script']['sha256'] == decode_sha, 'decode_llava.py sha differs from the committed harness')
        im = d['images']
        need(im['id_list_sha256'] == reg['images']['sha256'] and im['n_ids'] == reg['images']['n_ids']
             and im['n_decoded'] == im['n_ids'] and im.get('limit') is None, 'image list / count / --limit')
        need(all(manifest.get(p['image_file']) == p['image_sha256'] for p in d['preds']), 'image bytes differ from the manifest')
        dec = d['decoding']
        need(dec['max_new_tokens'] == reg['decoding']['max_new_tokens'] and dec['num_beams'] == reg['decoding']['num_beams']
             and dec['dtype'] == reg['decoding']['dtype'] and dec['question'] == reg['decoding']['question'], 'decoding settings')
        spec = spec_by_label[label]
        pin = lambda x: f"{x['repo']}@{x['revision']}"
        need(pin(d['model']['base']) == spec['base'] and pin(d['model']['vision']) == spec['vision']
             and [pin(x) for x in d['model']['loras']] == spec['loras']
             and d['model']['drop_vision_lora'] == spec['drop_vision_lora'], 'model pins')
        if spec.get('expected_lora_merges') is not None:
            exp = spec['expected_lora_merges']
            got = [{k: m[k] for k in ('lora', 'modules_by_component', 'skipped_by_component')} for m in d['model']['lora_merged']]
            need(got == [{k: e[k] for k in ('lora', 'modules_by_component', 'skipped_by_component')} for e in exp],
                 'merged LoRA module counts differ from prereg §1')
            has_file = [e['non_lora_tensors'] for e in exp
                        if 'non_lora_trainables.bin' in reg['pins'][e['lora'].split('@')[0]]['files']]
            need([n['n_tensors'] for n in d['model']['non_lora_loaded']] == has_file, 'non_lora tensor counts')
        if k2 is not None:
            need(dec['do_sample'] is True and dec['temperature'] == k2['temperature'] and dec['top_p'] == k2['top_p']
                 and dec['top_k'] == k2['top_k'] and dec['seed'] in k2['seeds'], 'K2 sampling settings')
        else:
            need(dec['do_sample'] is False, 'N9 runs must be greedy')
        key = (dec['batch_size'], dec['prompt_template_ids_sha256'], im['id_list_sha256'],
               tuple((p['image_id'], p['image_sha256']) for p in d['preds']))
        ref = ref or key
        need(key == ref, 'batch size, prompt ids or image bytes differ between runs')
    return fail


def per_image_maps(outs, gt, found):
    return {label: {p['image_id']: per_image_ext(p['caption'], gt[p['image_id']]) for p in d['preds'] if p['image_id'] in found}
            for label, d in outs.items()}


def boot_draws(n, n_boot, seed):
    rng = np.random.default_rng(seed)
    return [rng.integers(0, n, n) for _ in range(n_boot)]


# ------------------------------------------------ mode k2
def mode_k2(args):
    reg, th = registration()
    e1c = require_e1check(args.e1check)
    k2 = reg['k2_addendum']
    load_e1(args.coco_zip)
    labels = [f'k2_seed{s}' for s in k2['seeds']]
    loaded = {l: load_run(args.runs, l) for l in labels}
    outs = {l: v[0] for l, v in loaded.items()}
    spec = {l: {'base': k2['model'], 'vision': k2['vision'], 'loras': [], 'drop_vision_lora': False, 'expected_lora_merges': None}
            for l in labels}
    fail = protocol(reg, outs, spec, k2=k2)
    if fail:
        raise SystemExit('K-protocol failed:\n' + '\n'.join(fail))
    gt, found = e1.load_gt({p['image_id'] for d in outs.values() for p in d['preds']})
    P = per_image_maps(outs, gt, found)
    B, X = P[labels[0]], P[labels[1]]                       # X = seed 2, B = seed 1 (addendum §2)
    ids = sorted(set(B) & set(X))
    a = pair_arrays(B, X, ids)
    full = stats(a, np.arange(len(ids)))
    draws = [stats(a, s) for s in boot_draws(len(ids), k2['n_boot'], k2['boot_seed'])]
    res = {}
    for name in k2['control_order']:
        s = summarize(full, draws, CONTROLS[name])
        lo, hi = s['ci95']
        s['kill'] = 'FIRED' if abs(s['est']) > k2['kill_abs_dP_gt'] or not (lo <= 0.0 <= hi) else 'NOT_FIRED'
        s['admissible'] = bool(abs(s['est']) <= k2['admissible_abs_dP_le'] and lo <= 0.0 <= hi)
        res[name] = s
    c_star = next((n for n in k2['control_order'] if res[n]['admissible']), 'NONE')
    pref = res[k2['control_order'][0]]
    out = {'mode': 'k2', 'script_sha256': sha(__file__), 'prereg': {'path': str(PREREG.relative_to(REPO)), 'sha256': PREREG_SHA},
           'e1check': e1c, 'runs': {l: v[1] for l, v in loaded.items()}, 'n_img': len(ids), 'X_minus_B': k2['X_minus_B'],
           'controls': res, 'K2_PREDICTION': 'HELD' if abs(pref['est']) < k2['prediction_abs_dP_lt'] else 'NOT_HELD',
           'C_STAR': c_star, 'thresholds_from_prereg': {k: k2[k] for k in ('prediction_abs_dP_lt', 'kill_abs_dP_gt',
                                                                          'admissible_abs_dP_le', 'n_boot', 'boot_seed')}}
    Path(args.out).write_text(json.dumps(out, indent=1) + '\n')
    print(f"k2: prediction {out['K2_PREDICTION']}, C* = {c_star}")
    return 0


# ------------------------------------------------ K_F fidelity gate (base only) and mode kf
def k_f(reg, base_out, gt, found, lim_r1=None):
    base_P = per_image_maps({'base': base_out}, gt, found)['base']
    base_agg = e1.agg(list(base_P.values()))
    kf = reg['kill_rules']['K_F_fidelity']
    pub, lim = kf['published']['value'], kf['max_abs_diff']
    diffs = {m: round(float(base_agg[m] - pub[m]), 3) for m in lim}
    res = {'base_agg': base_agg, 'n_img': len(base_P), 'published': pub, 'diff': diffs, 'max_abs_diff': lim,
           'verdict': 'PASS' if all(abs(diffs[m]) <= lim[m] for m in lim) else 'FAIL'}
    if lim_r1:
        r1 = {int(re.sub(r'\D', '', r['image_id'].split('.')[0])): r['text'] for r in map(json.loads, open(lim_r1))}
        same = [p['caption'] == r1.get(p['image_id']) for p in base_out['preds']]
        res['descriptive_exact_caption_match_vs_lim_r1'] = {'share': round(float(np.mean(same)), 4), 'n': len(same),
                                                            'lim_r1_sha256': sha(lim_r1)}
    return res


def mode_kf(args):
    reg, _ = registration()
    e1c = require_e1check(args.e1check)
    load_e1(args.coco_zip)
    base = next(r for r in reg['runs'] if r['role'] == 'comparator')
    d, rec = load_run(args.runs, base['label'])
    fail = protocol(reg, {base['label']: d}, {base['label']: base})
    if fail:
        raise SystemExit('K-protocol failed:\n' + '\n'.join(fail))
    gt, found = e1.load_gt({p['image_id'] for p in d['preds']})
    out = {'mode': 'kf', 'script_sha256': sha(__file__), 'prereg': {'path': str(PREREG.relative_to(REPO)), 'sha256': PREREG_SHA},
           'e1check': e1c, 'run': rec, 'K_F': k_f(reg, d, gt, found, args.lim_r1)}
    Path(args.out).write_text(json.dumps(out, indent=1) + '\n')
    print(f"kf: K_F {out['K_F']['verdict']} diff {out['K_F']['diff']}")
    return 0 if out['K_F']['verdict'] == 'PASS' else 2


# ------------------------------------------------ mode n9
def mode_n9(args):
    reg, th = registration()
    e1c = require_e1check(args.e1check)
    k2res = json.loads(Path(args.k2).read_text())
    if k2res.get('mode') != 'k2' or k2res.get('script_sha256') != sha(__file__):
        raise SystemExit('refusing to score N9: the K2 result is missing or from another script version')
    load_e1(args.coco_zip)
    runs = reg['runs']
    spec = {r['label']: r for r in runs}
    loaded = {r['label']: load_run(args.runs, r['label']) for r in runs}
    outs = {l: v[0] for l, v in loaded.items()}
    fail = protocol(reg, outs, spec)
    if fail:
        raise SystemExit('K-protocol failed:\n' + '\n'.join(fail))
    gt, found = e1.load_gt({p['image_id'] for d in outs.values() for p in d['preds']})
    base_label = next(r['label'] for r in runs if r['role'] == 'comparator')
    out = {'mode': 'n9', 'script_sha256': sha(__file__), 'prereg': {'path': str(PREREG.relative_to(REPO)), 'sha256': PREREG_SHA},
           'e1check': e1c, 'k2': {'path': args.k2, 'sha256': sha(args.k2), 'C_STAR': k2res['C_STAR']},
           'runs': {l: v[1] for l, v in loaded.items()}, 'thresholds_from_prereg': th}

    # K_F first, on the base alone (judge rule 2); no method statistic is computed before it passes
    out['K_F'] = k_f(reg, outs[base_label], gt, found, args.lim_r1)
    if out['K_F']['verdict'] != 'PASS':
        Path(args.out).write_text(json.dumps(out, indent=1) + '\n')
        print('K_F FAIL: protocol must be fixed before any method is scored')
        return 2

    P = per_image_maps(outs, gt, found)
    methods = [r['label'] for r in runs if r['role'] == 'method']
    extra = [r['label'] for r in runs if r['role'] == 'sensitivity']
    ids = sorted(set.intersection(*[set(P[l]) for l in P]))
    arrays = {l: pair_arrays(P[base_label], P[l], ids) for l in methods + extra}
    full = {l: stats(a, np.arange(len(ids))) for l, a in arrays.items()}
    samples = boot_draws(len(ids), reg['scoring']['n_boot'], reg['scoring']['boot_seed'])   # same draws for every run
    draws = {l: [stats(a, s) for s in samples] for l, a in arrays.items()}
    keys = ('mcp_pref', 'mcp_sent', 'mcp_rand', 'trf', 'raw', 'dR', 'dm')
    table = {l: {k: summarize(full[l], draws[l], k) for k in keys} | {'agg': e1.agg([P[l][i] for i in ids])} for l in arrays}
    out['n_img'] = len(ids)
    out['base_agg'] = e1.agg([P[base_label][i] for i in ids])
    out['hit_max_new_tokens'] = {l: sum(p['hit_max_new_tokens'] for p in d['preds']) for l, d in outs.items()}
    c_star = k2res['C_STAR']
    cs = CONTROLS.get(c_star)

    def holm_family(key, alpha, sesoi):
        pv = {l: (table[l][key]['p_boot'] if table[l][key]['est'] is not None else 1.0) for l in methods}
        adj = holm_adjust(pv)
        return {l: {'p_holm': adj[l], 'label': ('NOT_COMPUTABLE' if table[l][key]['est'] is None else
                                               'PASS' if adj[l] < alpha and table[l][key]['est'] >= sesoi else 'NO')} for l in methods}
    p1 = holm_family(cs, th['alpha'], th['sesoi']) if cs else None
    p2 = holm_family('trf', th['alpha_p2'], th['sesoi_p2'])
    for l in methods:
        table[l]['P1'] = {'control': c_star, **(table[l][cs] | p1[l])} if cs else {'control': 'NONE (K-placebo)'}
        table[l]['P2'] = table[l]['trf'] | p2[l]
        if table[l]['P1'].get('label') == 'PASS':
            table[l]['P1']['label'] = 'SURVIVES'
        if table[l]['P2']['label'] == 'PASS':
            table[l]['P2']['label'] = 'OFF_FRONTIER'
    for l in arrays:  # CAR, single-caption form (prereg §4): C = raw - TRF, B = TRF - C*, A = C*
        f = full[l]
        if cs:
            table[l]['CAR'] = {'C_count': None if np.isnan(f['trf']) else round(f['raw'] - f['trf'], 3),
                               'B_allocation': None if np.isnan(f['trf']) else round(f['trf'] - f[cs], 3),
                               'A_choice': round(f[cs], 3), 'D_base_rerank': 0.0, 'total_dP_raw': round(f['raw'], 3),
                               'vertex_mean_counts': {'M_base': round(f['M_B'], 3), 'M_method': round(f['M_X'], 3),
                                                      'mean_k_star': round(f['k_mean'], 3)}}
    out['table'] = table

    fp = reg['frozen_predictions']
    name_to_label = {r['method']: r['label'] for r in runs}
    # (a) median over the methods of dP_C* vs E1's 15-pair mean under the same control
    if cs:
        comp = fp['a']['comparator_E1_15pair_mean_same_control'][c_star]['value']
        med = float(np.median([full[l][cs] for l in methods]))
        med_draws = np.array([np.median([draws[l][b][cs] for l in methods]) for b in range(len(samples))])
        lb = float(np.nanpercentile(med_draws, 2.5))
        a_lab = 'HELD' if med > comp and lb > comp else 'POINT_ONLY' if med > comp else 'NOT_HELD'
        out['prediction_a'] = {'median': round(med, 3), 'ci95_lower': round(lb, 3), 'comparator': comp, 'control': c_star, 'verdict': a_lab}
    else:
        out['prediction_a'] = {'verdict': 'NOT_EVALUATED (no primary control; K-placebo)'}

    # (b) D_b = dm(near-balanced) - dm(chosen-fewer), classes per caption
    def d_b(nb, cf):
        f = lambda src: float(np.mean([src[l]['dm'] for l in nb]) - np.mean([src[l]['dm'] for l in cf]))
        dd = np.array([f({l: draws[l][i] for l in nb + cf}) for i in range(len(samples))])
        lo, hi = np.nanpercentile(dd, [2.5, 97.5])
        return {'near_balanced': nb, 'chosen_fewer': cf, 'est': round(f(full), 3), 'ci95': [round(float(lo), 3), round(float(hi), 3)]}
    nb = [name_to_label[x] for x in fp['b']['near_balanced']]
    cf = [name_to_label[x] for x in fp['b']['chosen_fewer']]
    b = d_b(nb, cf)
    b['verdict'] = ('HELD' if b['est'] >= th['b_min'] and b['ci95'][0] > 0 else
                    'KILLED (prediction dropped; N9 shows no dk -> dm link)' if b['est'] < th['b_kill'] else 'NOT_SHOWN')
    full_merge = [r['label'] for r in runs if r['role'] == 'sensitivity' and r['loras'] == spec[name_to_label['POVID']]['loras']]
    out['prediction_b'] = {'primary': b, 'sensitivity_not_verdict': {
        'plus_RLAIF-V': d_b(nb + [name_to_label['RLAIF-V']], cf),
        'povid_fullmerge': d_b([full_merge[0] if l == name_to_label['POVID'] else l for l in nb], cf)}}
    out['prediction_c'] = {'verdict': fp['c']['status']}

    # kill rules
    n_surv = sum(table[l]['P1'].get('label') == 'SURVIVES' for l in methods)
    out['K_headline'] = {'n_survive': n_surv, 'threshold': th['headline_min'],
                         'verdict': 'TRIGGERED' if n_surv >= th['headline_min'] else 'NOT_TRIGGERED'}
    if cs:
        systems = methods + [base_label]
        def val(l, k, i=None):  # base sits at 0 on both rankings
            return 0.0 if l == base_label else (full[l][k] if i is None else draws[l][i][k])
        rev = []
        for x in range(len(systems)):
            for y in range(x + 1, len(systems)):
                si, sj = systems[x], systems[y]
                raw_d, cm_d = val(si, 'raw') - val(sj, 'raw'), val(si, cs) - val(sj, cs)
                dd = np.array([val(si, cs, i) - val(sj, cs, i) for i in range(len(samples))])
                lo, hi = np.nanpercentile(dd, [2.5, 97.5])
                if np.sign(raw_d) != np.sign(cm_d) and not (lo <= 0.0 <= hi):
                    rev.append({'pair': [si, sj], 'raw_diff': round(raw_d, 3), 'cm_diff': round(cm_d, 3),
                                'cm_ci95': [round(float(lo), 3), round(float(hi), 3)]})
        out['K_rank'] = {'significant_reversals': rev, 'verdict': 'RANKING_CHANGED' if rev else 'RANKING_UNCHANGED (report as consistent; no claim rests on N9)'}
        out['K_placebo'] = 'NOT_TRIGGERED'
    else:
        out['K_rank'] = {'verdict': 'NOT_EVALUATED (no primary control)'}
        out['K_placebo'] = 'TRIGGERED: specification curve only; no "survives count control" claim'
    Path(args.out).write_text(json.dumps(out, indent=1) + '\n')
    print(f"n9: K_F {out['K_F']['verdict']}, C* {c_star}, (a) {out['prediction_a']['verdict']}, (b) {b['verdict']}, "
          f"headline {out['K_headline']['verdict']}, rank {out['K_rank']['verdict']}")
    return 0


# ------------------------------------------------ selftest (rules only; statistics are checked by e1check)
def selftest():
    assert two_sided_boot_p(np.array([1.0, 2.0, 3.0])) == min(1.0, 2.0 * (0 + 1.0) / 4.0)
    assert two_sided_boot_p(np.array([np.nan])) == 1.0
    assert holm_adjust({'a': 0.01, 'b': 0.04, 'c': 0.03}) == {'a': 0.03, 'c': 0.06, 'b': 0.06}
    assert sent_tie_avg_tp([[True, False], [True, True, False]], 3) == 1.0 + 1.0 * (2.0 / 3.0)
    assert sent_tie_avg_tp([[True]], 0) == 0.0
    reg, th = registration()
    assert th['sesoi'] > 0 and 0 < th['alpha'] < 1 and th['b_kill'] < th['b_min'] and th['headline_of'] == sum(
        r['role'] == 'method' for r in reg['runs'])
    print('selftest PASS', json.dumps(th))
    return 0


def main(argv):
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = p.add_subparsers(dest='mode', required=True)
    for m in ('e1check', 'k2', 'kf', 'n9'):
        s = sub.add_parser(m)
        s.add_argument('--coco-zip', required=True)
        s.add_argument('--out', required=True)
        if m == 'e1check':
            s.add_argument('--opera', required=True)
            s.add_argument('--lim', required=True)
        else:
            s.add_argument('--runs', required=True)
            s.add_argument('--e1check', required=True)
        if m == 'n9':
            s.add_argument('--k2', required=True)
        if m in ('kf', 'n9'):
            s.add_argument('--lim-r1')
    sub.add_parser('selftest')
    a = p.parse_args(argv)
    return {'e1check': mode_e1check, 'k2': mode_k2, 'kf': mode_kf, 'n9': mode_n9}.get(a.mode, lambda _: selftest())(a)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
