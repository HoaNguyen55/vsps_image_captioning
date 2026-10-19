"""Writes the B-N2 prereg v2 JSON (judge PD-19). Reads b_n2_inventory.json, b_n2_absence_check.json and the mirror of
O-2308423 (multiref_s42 entry checks); delta is quoted from manuscript/prereg/2026-10-13_upe_mbr.md line 143 with its sha.
Usage: python3 -E -P -B b_n2_prereg_v2.py REPO INVENTORY_JSON ABSENCE_JSON OUT_JSON
"""
import glob, hashlib, json, re, sys
from pathlib import Path

ROOT, INV, ABS, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
rel = lambda p: str(Path(p).resolve().relative_to(ROOT))
inv, ab = json.loads(INV.read_text(encoding='utf-8')), json.loads(ABS.read_text(encoding='utf-8'))
runs = inv['runs']

UPE = ROOT / 'manuscript/prereg/2026-10-13_upe_mbr.md'
line143 = UPE.read_text(encoding='utf-8').splitlines()[142]
delta = float(re.search(r'KTVIC CIDEr-D change is >= -(\d+\.\d+)', line143).group(1))

# multiref_s42: the three PD-19 (d) conditions, short mode (the D1 mode)
M = ROOT / '.session_backup/machines/O-2308423/root'
listed = dict(reversed(l.split()) for l in (M / 'outputs/sha256/56_multiref_s42.sha256').read_text().splitlines() if l.strip())
need = {f'/root/ncs-data/results/multiref_s42-short{x}': M / f'outputs/results/multiref_s42-short{x}' for x in ('.preds.json', '.json')}
own_reports = sorted(glob.glob(str(M / '**/gold_multiref/_build_report.json'), recursive=True))
mr = {'machine': 'O-2308423', 'sha_list': rel(M / 'outputs/sha256/56_multiref_s42.sha256'),
      'c1_outputs_in_machine_sha_list': all(k in listed for k in need),
      'c2_listed_sha_equals_mirror_copy': all(k in listed and listed[k] == sha(v) for k, v in need.items()),
      'c3_own_build_report_shows_ktvic_train_only': bool(own_reports) and all(
          json.loads(Path(f).read_text())['source'].endswith('/ktvic/train_data.json') for f in own_reports),
      'own_build_reports_found': [rel(f) for f in own_reports],
      'context_not_a_pass': {
          'job_line': 'queue/done/56_multiref_s42.sh: train_stage2.py --data /root/ncs-data/gold_multiref',
          'machine_log_rows': re.search(r'read (\d+) rows from /root/ncs-data/gold_multiref', (M / 'queue/56_multiref_s42.log').read_text()).group(1),
          'other_machine_builds_same_dir': {k: v['source'] for k, v in inv['sft_builds_on_mirrors'].items() if '/gold_multiref/' in k},
          'metrics_fingerprint_rows': runs['multiref_s42']['metrics_fingerprint']['rows_implied']}}
mr['enters_D1'] = mr['c1_outputs_in_machine_sha_list'] and mr['c2_listed_sha_equals_mirror_copy'] and mr['c3_own_build_report_shows_ktvic_train_only']
mr['disclosure'] = None if mr['enters_D1'] else ('excluded from D1: ' + '; '.join(
    k for k in ('c1_outputs_in_machine_sha_list', 'c2_listed_sha_equals_mirror_copy', 'c3_own_build_report_shows_ktvic_train_only') if not mr[k])
    + ' failed. The training data directory on O-2308423 has no build report or sha in the mirror; the row count matches the '
      'KTVIC-only gold_multiref builds on n2/n3, but byte identity is not recorded. Re-entry needs that build report or the sft.jsonl sha.')

K, Kp = ['p1-gold', 'p1_s43', 'p1_s44'], ['fuse2_s42', 'fuse2_s43', 'fuse2_s44']
d1 = [r for r, v in runs.items() if v['arm'] == 'control' and (r != 'multiref_s42' or mr['enters_D1'])]
assert all(runs[r]['arm'] == 'control' for r in K + Kp) and set(K + Kp) <= set(d1)
pin = lambda r: {k: v for k, v in (runs[r]['outputs']['short']['cider_full_558'] or {}).items()} | \
    {'preds': [{k: p[k] for k in ('path', 'sha256', 'git_tracked', 'modified_vs_HEAD')} for p in runs[r]['outputs']['short']['preds']]}

if ab['n_unclassified']:
    raise SystemExit(f"absence check has {ab['n_unclassified']} unclassified hits: review them before writing the prereg")
prior_cat = [c for c in ab['files_by_category'] if c.startswith('PRIOR')]
status = ('POST_HOC (an earlier leaked/clean subset metric exists)' if prior_cat else
          'REGISTERED, valid only if this file is committed before the first subset statistic is computed')
splits = {k: {'path': f'data/lb/splits/ktvic_test_openviic_train_{k}.txt', 'sha256': sha(ROOT / f'data/lb/splits/ktvic_test_openviic_train_{k}.txt'),
              'n': inv['split'][k]['n'], 'equals_LB_draft_sha': sha(ROOT / f'data/lb/splits/ktvic_test_openviic_train_{k}.txt') == inv['split'][k]['sha256']}
          for k in ('leaked', 'clean')}
assert all(v['equals_LB_draft_sha'] for v in splits.values())
out = {
    'id': 'B-N2', 'version': 'v2', 'paper': 'B', 'decision': {'path': '.session_backup/2026-10-13/decisions/PD-19.txt',
                                                             'sha256': sha(ROOT / '.session_backup/2026-10-13/decisions/PD-19.txt')},
    'supersedes': {'path': '.session_backup/2026-10-19/HV_LK/b_n2/2026-10-19_b_n2_leakage_did_prereg_DRAFT.json',
                   'sha256': sha(ROOT / '.session_backup/2026-10-19/HV_LK/b_n2/2026-10-19_b_n2_leakage_did_prereg_DRAFT.json')},
    'label': 'registered re-analysis of existing outputs', 'status_D_W13_6': status,
    'disclosure': 'The per-image outputs of every system named here existed before this registration (sha256 pinned). Only the '
                  'leaked/clean subset statistic is new; it has not been computed (absence check below).',
    'headline_DiD': {'verdict': 'NOT_EVALUABLE (deferred)', 'reason': 'treated arm empty: no run of ours was trained with OpenViIC data',
                     'evidence': {'inventory': {'path': rel(INV), 'sha256': sha(INV), 'keys': ['arms.treated', 'treated_arm_empty',
                                                                                                   'build_sources_by_kind']}},
                     'revival_requires_all': ['licence check that UIT-OpenViIC allows training use',
                                              'a new prereg for the OpenViIC-trained run, committed before training',
                                              'a GPU plan entry', 'a sha-pinned data manifest of its training data'],
                     'allowed_now': 'a feasibility check of availability and licence; it trains nothing'},
    'absence_check': {'path': rel(ABS), 'sha256': sha(ABS), 'commands': ab['commands'], 'excluded': ab['excluded'],
                      'n_stage1_files': ab['n_stage1_files'], 'n_not_scanned_text_data_files': len(ab['not_scanned_text_data_files']),
                      'n_hits': ab['n_hits'], 'n_hit_files': ab['n_hit_files'],
                      'n_files_by_category': {k: len(v) for k, v in ab['files_by_category'].items()},
                      'n_unclassified': ab['n_unclassified'], 'prior_split_metric_found': bool(prior_cat),
                      'files_naming_the_split_lists': ab['files_naming_the_split_lists'],
                      'registration_overlap': ('B-N1 prereg (manuscript/prereg/2026-10-19_b_n1_vi_leaderboard.md, commit 327191c) registers LBB-D1, '
                                               'the leaked-minus-clean gap for its reference rows, which include p1_s43-short and fuse2_s42-short. '
                                               'It is registered, not computed (no B-N1 output exists). Each prereg reports its own method; neither reuses the other.'),
                      'allowed_non_metrics': 'the panel-overlap count (401/558) and the ViCLIP-OT id work'},
    'sets': {**splits, 'committed_in': '327191c (byte-identical to agent LB lists)', 'overlap_file': inv['split']['overlap_file'],
             'checks': inv['split']['checks']},
    'systems': {'K_P1_legacy_short': {r: pin(r) for r in K}, 'Kp_fuse2_legacy_short': {r: pin(r) for r in Kp},
                'D1_all_KTVIC_only_short': {r: pin(r) for r in d1}, 'seed_matched_pairs': [['fuse2_s42', 'p1-gold'], ['fuse2_s43', 'p1_s43'], ['fuse2_s44', 'p1_s44']],
                'p1_seed42_link': inv['p1_seed42_link'], 'multiref_s42_entry': mr,
                'not_in_D1': {'zeroshot': 'not trained by us; exposure of the base model unknown (B-N1 reports the clean-157 sensitivity for zero-shot models)'}},
    'methods': {
        'cider_d': {'scorer_files_sha256': {f: sha(ROOT / f) for f in ('scripts/evaluate.py', 'rescap/metrics.py')},
                    'config': "rescap.metrics.CaptionMetrics(language='vi', segmenter='rdrsegmenter', tokenize=True); pycocoevalcap Cider (CIDEr-D); x100",
                    'per_subset': 'one Cider().compute_score per system over all 558 images on CaptionMetrics._align + _tokenize output; '
                                  'per-image vector c(i); C_S = 100 * mean over i in S of c(i); document frequencies from all 558',
                    'S1': 'subset-df variant (CaptionMetrics.compute on each subset alone): point estimates only',
                    'S2': 'punctuation fix (B-N1 draft definition): CI, no verdict'},
        'object_f1': {'scorer_sha256': {'scripts/object_prf.py': sha(ROOT / 'scripts/object_prf.py')},
                      'per_subset': "object_prf.scores(rows of S)['F1'] with rows = image_counts(set(objects_in(caption)), KTVIC reference gold, _ancestors)",
                      'role': 'secondary; CI; no verdict'},
        'self_check': ['for every system: CaptionMetrics over all 558 (the evaluate.py path) returns a CIDEr whose x100 value equals the '
                       "committed results[segmenter=rdrsegmenter].scores_scaled_x100.CIDEr exactly (float equality), and scorer.segmenter == 'rdrsegmenter'",
                       'F0 gate: 100 * mean over 558 of c(i) equals the same committed value within 1e-9',
                       'the scorer and its self-check output are committed through the gatekeeper after this prereg and before any subset statistic',
                       'any failure: K-F0, nothing on subsets is computed'],
        'bootstrap': {'B': 5000, 'rng': 'numpy.random.default_rng(0)', 'scheme': 'stratified: each draw resamples |L| ids from L and |C| from C with replacement',
                      'paired': 'same draws for every system and metric', 'df': 'fixed at the 558-image value', 'ci': 'percentile 2.5 / 97.5'}},
    'estimands': {'gap': 'gap(s) = C_L(s) - C_C(s)', 'placebo': "DiD_PL = mean_{s in K'} gap(s) - mean_{s in K} gap(s); seed-matched values beside it",
                  'D1': 'gap(s) for every D1 system, with CI'},
    'delta': {'value': delta, 'quoted_line': line143.strip(), 'source': {'path': rel(UPE), 'line': 143, 'sha256': sha(UPE)}},
    'placebo_verdict': {'PASS': 'ci_lo > -delta AND ci_hi < +delta', 'FAIL': 'ci_lo >= +delta OR ci_hi <= -delta',
                        'INCONCLUSIVE': 'otherwise', 'role': 'the control any later leakage claim on this split needs'},
    'kill_rules': {'K-F0': 'self-check or F0 fails for a system -> stop; nothing on subsets',
                   'K-COV': 'a system without predictions for all 558 ids is dropped and named',
                   'K-PL': "placebo FAIL -> the split interacts with the training recipe without exposure; no later DiD on this split is called leakage inflation without a recipe-matched control"},
    'paper_B_note': 'The PD-11 (c) caveat applies to none of our models (none saw OpenViIC). It stays for comparators trained on OpenViIC '
                    'or of unknown exposure, including zero-shot external models.',
}
OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
print(json.dumps({'status': status, 'delta': delta, 'multiref_enters_D1': mr['enters_D1'], 'D1': d1,
                  'c': [mr[k] for k in ('c1_outputs_in_machine_sha_list', 'c2_listed_sha_equals_mirror_copy', 'c3_own_build_report_shows_ktvic_train_only')]}))
