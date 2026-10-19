"""B-N2 absence check (judge PD-19 (b)): has any leaked/clean (401/157) subset metric been computed before for the KTVIC
systems? Every command, file, line and classification is recorded; matched lines are stored cut to 200 characters.
  stage 1  text files that mention the split or a leak (grep, listed);
  stage 2  (a) a stage-1 line that also names a metric; (b) in JSON, a key naming the split whose value holds a metric key;
           (c) a metric within 3 lines of a split-specific term (pretty-printed JSON, tables).
Each hit is classified by ordered rules; a hit no rule explains is UNCLASSIFIED and blocks the REGISTERED status.
Hits that no rule covers were read by the agent and are classified in REVIEW, one by one, with the reason.
Usage: python3 -E -P -B b_n2_absence_check.py REPO OUT_JSON [EARLIER_OUT_JSON: reuse its stage-1 file list]
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT, OUT = Path(sys.argv[1]), Path(sys.argv[2])
REUSE = Path(sys.argv[3]) if len(sys.argv) > 3 else None
SCOPE = ['data', '.session_backup', 'manuscript', 'scripts']        # logs: manuscript/WORKFLOW_LOG.md, gpu_jobs/M1|M2_EVENTS.log
INCL = [f'--include={g}' for g in ('*.json', '*.jsonl', '*.md', '*.txt', '*.log', '*.tsv', '*.csv', '*.py', '*.sh', '*.yaml')]
EXCL = [f'--exclude-dir={d}' for d in ('checkpoint-*', '.venv', 'venv', '__pycache__')]   # model checkpoints and environments
OWN = '.session_backup/2026-10-19/HV_LK/'                             # this task's own drafts (no statistic computed)
LEAK = r'leak|openviic_train_(leaked|clean)|in_openviic_train|not_in_openviic|clean[_ -]?157|157[_ -]?clean|401[_ -]?leaked|leaked[_ -]?401'
SPLIT = re.compile(r'openviic_train_(leaked|clean)|in_openviic_train|not_in_openviic|clean[_ -]?157|157[_ -]?clean|401[_ -]?leaked|'
                   r'leaked[_ -]?401|"leaked"|"clean"|leaked[ _-]*(minus|−|-)[ _-]*clean|leaked/clean|\bleaked\b', re.I)
METRIC = re.compile(r'cider|\bf1\b|f1_|chair|bleu|meteor|rouge|precision|recall', re.I)
RULES = [   # (category, applies to path, applies to context)
    ('text data: tokenizer vocabularies, datasets, literature caches', re.compile(
        r'(vocab|tokenizer)\.json$|merges\.txt$|dataset_coco\.json$|refs_en\.json$|/r11_litmaps|/dl/\d{4}\.\d+/|/longcap_arena'), None),
    ('another meaning of leak (CJK or token leakage, leak-free annotator scoring, prior-leak kill, paraphrase chain, '
     'UIT-ViIC/COCO overlap, OpenViIC 8-gram release scan)', None, re.compile(
        r'cjk|non-vietnamese|leak-?free|leakage-free|prior[- _]leak|paraphrase-chain|leak_a23|leak_aheld|uitviic.{0,60}coco|'
        r'coco.{0,60}leak|openviic_leak_scan|leak_ceiling|leaking|leakage (control|guard)|overlap_133', re.I)),
    ('registration, plan or decision text: no number computed', re.compile(
        r'GAP_ANALYSIS|b_n1_vi_leaderboard|build_lb|/decisions/|LB_leaderboards/MANIFEST'), None),
    ('overlap count or id list (allowed: not a system metric)', None, re.compile(
        r'in_openviic_train(_pct)?"?: *\d|matched_openviic_train_copy|viclip|A_32_leakage_disclosure', re.I)),
]
RULES = [RULES[0], RULES[2], RULES[3], RULES[1]]   # path rules first, then the overlap count, then other meanings of leak
PLAN = 'registration, plan or decision text: no number computed'
OTHER = RULES[3][0]
REVIEW = {   # (path suffix, line) -> (category, reason), read by the agent
    ('research_r10/V3/REPORT.txt', 177): (OTHER, 'train/dev norm separation ("so there is no leakage")'),
    ('research_r6/verify/B1-P1.txt', 37): (OTHER, 'literature remark: GRPO resurfaces leaked data'),
    ('scripts/xv_ef1.py', 428): (OTHER, 'prior-leak kill flag of XV-EF1'),
    ('journal_draft_B/sec1_intro.md', 12): (RULES[2][0], '401 of 558 overlap count; panel aggregates, no subset metric'),
    ('kg_plan/R3_03_feasibility_v2.md', 169): (PLAN, 'proposal to bootstrap on a clean-157 set; no number'),
    ('manuscript/WORKFLOW_LOG.md', 978): (PLAN, 'main proposes the B-N2 placebo to the judge'),
    ('manuscript/WORKFLOW_LOG.md', 990): (PLAN, 'PD-19 (b) recorded'),
    ('journal_draft_B/number_manifest_B.tsv', 418): (PLAN, 'PENDING row for B-N2; no number'),
}


def classify(path, line, ctx):
    for (suf, ln), (cat, why) in REVIEW.items():
        if path.endswith(suf) and line == ln:
            return cat, why
    for name, prx, crx in RULES:
        if (prx and prx.search(path)) or (crx and crx.search(ctx)):
            return name, 'rule'
    return 'UNCLASSIFIED', None


def json_hits(obj, trail=''):
    """keys naming the split whose subtree carries a metric key"""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            t = f'{trail}.{k}'
            if SPLIT.search(f'"{k}"') and METRIC.search(json.dumps(v)[:100000] if isinstance(v, (dict, list)) else ''):
                out.append(t)
            out += json_hits(v, t)
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:5000]):
            out += json_hits(v, f'{trail}[{i}]')
    return out


cmd1 = ['grep', '-rIl', '-i', '-E', LEAK, *INCL, *EXCL, *SCOPE]
if REUSE:
    files = json.loads(REUSE.read_text(encoding='utf-8'))['stage1_files']
else:
    files = sorted(f for f in subprocess.run(cmd1, cwd=ROOT, capture_output=True, text=True).stdout.split('\n') if f and not f.startswith(OWN))
hits, skipped = [], []
for f in files:
    p = ROOT / f
    if RULES[0][1].search(f):            # text data cannot hold a computed system metric: listed, not scanned
        skipped.append(f)
        continue
    lines = p.read_text(encoding='utf-8', errors='ignore').splitlines()
    for n, line in enumerate(lines, 1):
        if re.search(LEAK, line, re.I) and METRIC.search(line):
            hits.append({'file': f, 'line': n, 'kind': 'same_line', 'text': line.strip()[:200], 'ctx': line})
        elif SPLIT.search(line) and any(METRIC.search(x) for x in lines[max(0, n - 4):n + 3]):
            ctx = '\n'.join(lines[max(0, n - 4):n + 3])
            hits.append({'file': f, 'line': n, 'kind': 'window_3', 'text': line.strip()[:200], 'ctx': ctx})
    if f.endswith('.json') and p.stat().st_size < 50_000_000:
        try:
            for t in json_hits(json.loads(p.read_text(encoding='utf-8', errors='ignore'))):
                hits.append({'file': f, 'line': None, 'kind': 'json_key', 'text': t[:200], 'ctx': t})
        except ValueError:
            pass
for h in hits:
    h['category'], h['how'] = classify(h['file'], h['line'], h.pop('ctx'))
uses = json.loads(REUSE.read_text(encoding='utf-8'))['files_naming_the_split_lists'] if REUSE else sorted(f for f in subprocess.run(['grep', '-rIl', 'ktvic_test_openviic_train', *INCL, *EXCL, *SCOPE], cwd=ROOT,
                                        capture_output=True, text=True).stdout.split('\n') if f and not f.startswith(OWN))
by_cat = {}
for h in hits:
    by_cat.setdefault(h['category'], set()).add(h['file'])
unclassified = [h for h in hits if h['category'] == 'UNCLASSIFIED']
out = {'stage1_reused_from': {'path': str(REUSE), 'sha256': __import__('hashlib').sha256(REUSE.read_bytes()).hexdigest()} if REUSE else None,
       'commands': {'stage1': ' '.join(cmd1[:4]) + f" '{LEAK}' " + ' '.join(INCL + EXCL + SCOPE),
                    'stage2': {'same_line': f'stage-1 pattern and /{METRIC.pattern}/i on one line',
                               'window_3': f'/{SPLIT.pattern}/i with a metric within 3 lines',
                               'json_key': 'a JSON key matching the split pattern whose value holds a metric key'},
                    'split_list_users': 'grep -rIl ktvic_test_openviic_train ' + ' '.join(INCL + EXCL + SCOPE)},
       'excluded': {'own_folder': OWN, 'dirs': [e.split('=')[1] for e in EXCL]},
       'n_stage1_files': len(files), 'stage1_files': files, 'not_scanned_text_data_files': skipped, 'n_hits': len(hits), 'n_hit_files': len({h['file'] for h in hits}),
       'files_by_category': {k: sorted(v) for k, v in by_cat.items()}, 'hits': hits,
       'files_naming_the_split_lists': uses, 'n_unclassified': len(unclassified)}
OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
print(json.dumps({'n_stage1_files': len(files), 'n_hits': len(hits), 'by_category': {k: len(v) for k, v in by_cat.items()},
                  'unclassified': [(h['file'], h['line'], h['text'][:120]) for h in unclassified][:40]}, ensure_ascii=False, indent=1))
