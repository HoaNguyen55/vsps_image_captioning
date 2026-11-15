#!/usr/bin/env python3
"""Apply the Paper C text fixes ruled in CC-405 (GO 88) to the paper repo WORKING TREE.

The body below is the judge's own check script (cc405_check/final.py, sha256 e8dc6c5c...) unchanged: it builds
the 8 final files in memory from commit 6a5d36a, the fix package and the judge-written blocks of Annex A
(judge_blocks.json bf08a174), checks every manifest row against its source, asserts that the abstract, the
introduction and the conclusion are unchanged, and simulates the prepared shell C2 transfer on the result.
Added here: gates before it (pins, paper HEAD, clean files) and, after it, a comparison of the 8 results with
the sha256 targets of CC-405 Ruling 6; files are written only if all 8 match. Never runs git add / commit.
Usage: python3 -I apply_cc405.py
"""
import hashlib as _h, pathlib as _p, subprocess as _s
_C = _p.Path('/mnt/d/vsps_image_captioning/.session_backup/2026-11-15/cc405_check')
for _n, _pin in {'final.py': 'e8dc6c5c', 'judge_blocks.json': 'bf08a174'}.items():
    assert _h.sha256((_C / _n).read_bytes()).hexdigest().startswith(_pin), f'pin {_n}'
_R = '/mnt/d/vsps_papers/vsps-paperC-tallip'
assert _s.run(['git', '-C', _R, 'rev-parse', '--short', 'HEAD'], capture_output=True, check=True).stdout.decode().strip() == '6a5d36a', 'paper HEAD'
assert _s.run(['git', '-C', _R, 'status', '--porcelain', '--', 'paper_v1_analysis/*.md', 'paper_v1_analysis/number_manifest_C.tsv'], capture_output=True, check=True).stdout == b'', 'paper md files or manifest not clean'
# ---- judge's check script, unchanged ----
"""CC-405 check: build the ruled Paper C files in memory from `git show 6a5d36a:` and print target sha256s.
Reads the package and the paper repo; writes only judge_blocks.json beside this file. Usage: python3 -I final.py"""
import collections, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN = Path('/mnt/d/vsps_image_captioning')
R = '/mnt/d/vsps_papers/vsps-paperC-tallip'
PKG = RUN / 'manuscript/fix_packages/2026-11-15_C/C_FIX_PACKAGE_v1.md'
PKG_SHA = '3d4bfc7327948529461cb76981b2ef6f18a668a4ecff4c23ccacb99df2c7381a'
C2 = RUN / 'manuscript/prereg/2026-11-11_c_attr_dev/paper_text/transfer/c_attr_c2_transfer.py'
sha = lambda b: hashlib.sha256(b).hexdigest()
head = lambda f: subprocess.run(['git', '-C', R, 'show', '6a5d36a:paper_v1_analysis/' + f], capture_output=True, check=True).stdout.decode()

t = PKG.read_bytes(); assert sha(t) == PKG_SHA, 'package pin'
m = re.split(r'^<<<(C-F\d+[a-e]?) (?:(\S+) )?(OLD|NEW|EVIDENCE|END)>>>\n', t.decode(), flags=re.M)
B = {}
for i in range(1, len(m), 4):
    bid, f, kind, body = m[i:i + 4]
    if kind in ('OLD', 'NEW'):
        B.setdefault(bid, {})[kind] = body[:-1] if body.endswith('\n') else body
        B[bid]['file'] = f or B[bid].get('file')
assert len(B) == 27

# Annex A of CC-405: APPLY WITH CHANGE (package OLD kept, NEW replaced)
J = {
 'C-F09': B['C-F09']['OLD'] + '\n- **Copy and token-limit diagnostics (Section 3.5; Tables S1–S4, S6, S10, S11 and S14).** The *4-gram copy rate against the memory* is the share of a run\'s caption 4-grams (syllables; each caption\'s distinct 4-grams, summed over the run\'s captions) that occur in a caption of any memory cluster, counting every caption that a cluster can show; the zero-shot arm is its baseline. The *near-verbatim copy share* is the share of captions whose copy statistic m against the examples shown with them is at least 0.90; m is the maximum, over those examples, of the larger of 1 − (edit distance / length of the longer of the two captions) and the single-reference BLEU-4, both computed on syllables. The *hit-max rate* is the share of captions whose generation reached the limit of 60 new tokens without an end-of-sequence token.',
 'C-F12': 'Configurations were frozen on development data and each test set was looked at once. Each backbone\'s configuration was picked from its `ret` runs alone (Section 3.5), and `rand` and `fix` run at the picked k, tail and τ, so `ret` − `rand` is measured at a configuration selected on the `ret` score; the stage-A `rand` and `fix` runs are listed in Table S10.',
 'C-F15b': 'they do not include the variation from drawing other random examples, or run-to-run variation. Development estimates of the share of the image-bootstrap variance of the draw-averaged `ret` − `rand` (τ_sel) that the random draw accounts for, and a `rand` d1 − d2 placebo that was flagged for one backbone on one set, are in Section 6.10.5; no test interval is widened, recomputed or relabelled with them.',
 'C-F16': '**Reading the labels of Table 17.** REVERSED on L_cp means that the 95% upper bound of L_cp is below 0 (Section 5.7). L_cp is a lower bound on the part of the retrieval contrast that does not travel through copied n-grams, so on these rows the registered reading applies: the bound does not exclude that the whole retrieval-specific effect is carried by copied n-grams; it does not show that this part is negative. K_nc is the direction check of assumption A_cp (Section 3.8): the `rand` caption never saw R_q, so K_nc measures overlap that needs no copying, and its registered expected sign is ≥ 0. No K_nc row is REVERSED, so the bound is in force on every row (column "bound").\n\nThe English copy bound on the Flickr30K carve and Flickr30K val, registered as a post hoc row, was not coded and was not run.',
 'C-F17': 'Everything else is secondary, reported with unadjusted CIs, with no family-wise claim. Multiplicity is handled within each registration as listed; no error rate is claimed across registrations or over the five one-look test sets taken together.',
 'C-F19': '+40.28 [38.50, 42.08] on XM-test2500; each backbone\'s own rows also have 95% CIs above zero (Table S5).',
}
NOT_APPLIED = {'C-F05'}
json.dump(J, open(HERE / 'judge_blocks.json', 'w'), ensure_ascii=False, indent=0)

key = lambda x: (int(re.search(r'\d+', x).group()), x)
order = [(b, B[b]['file'], B[b]['OLD'], J.get(b, B[b]['NEW'])) for b in sorted(B, key=key) if b not in NOT_APPLIED]
files = {}
for bid, f, o, n in order:
    s = files.setdefault(f, head(f)); assert s.count(o) == 1, (bid, s.count(o)); files[f] = s.replace(o, n)
for bid, f, o, n in order:
    assert files[f].count(n) == 1, bid
for f in ('00_abstract.md', '01_introduction.md', '10_conclusion.md', '02_related_work.md', '04_data_and_splits.md'):
    assert f not in files, f
print('applied', len(order), 'blocks:', ' '.join(b for b, *_ in order))

# manifest: six appended rows, each value checked against its source; three used_in edits in place
def src(p): return (RUN / p).read_bytes()
st2, des = src('manuscript/prereg/2026-10-22_c_stage2/PREREG.md'), src('manuscript/prereg/2026-10-22_c_stage1/DESIGN.md')
df = json.loads(src('.session_backup/2026-10-22/c_stage2/final/decide_final.json'))
reg = json.loads(src('manuscript/prereg/2026-10-30_c_t1/c_t1_registry.json'))
L = lambda b, n: b.decode().splitlines()[n - 1]
assert 'point estimate **≥ −1.0**' in L(st2, 332) and 'CIDEr-D (stripped) cost' in L(st2, 332)
assert df['ov_dev_b']['H_G']['per_model']['qwen25vl_7b']['tau_G'] == '0.00'
assert 'm ≥ 0.90' in L(des, 257) and 'Near-verbatim' in L(des, 257)
assert L(des, 181).startswith('| `qwen25vl_7b` |') and L(des, 181).rstrip().endswith('| 4 |')
assert L(des, 182).startswith('| `internvl3_8b` |') and L(des, 182).rstrip().endswith('| 2 |')
assert reg['models']['aya_vision_8b']['batch_size'] == 2
for p in ('manuscript/prereg/2026-10-22_c_stage2/PREREG.md', 'manuscript/prereg/2026-10-22_c_stage1/DESIGN.md',
          'manuscript/prereg/2026-10-30_c_t1/c_t1_registry.json'):
    assert src(p) == Path(R, 'prereg', p.split('prereg/')[1]).read_bytes(), 'run-repo and paper-repo copies differ: ' + p
p12 = lambda p: sha(src(p))[:12]
ROWS = [
 ['-1.0', 'manuscript/prereg/2026-10-22_c_stage2/PREREG.md::§7.5 H_G pass rule, CIDEr-D cost floor (l.332)', '-1.0', p12('manuscript/prereg/2026-10-22_c_stage2/PREREG.md'), 'design', '06_results.md'],
 ['0.00', '.session_backup/2026-10-22/c_stage2/final/decide_final.json::ov_dev_b.H_G.per_model.qwen25vl_7b.tau_G', "'0.00'", p12('.session_backup/2026-10-22/c_stage2/final/decide_final.json'), 'reader-reference', '06_results.md'],
 ['0.90', 'manuscript/prereg/2026-10-22_c_stage1/DESIGN.md::§6.2 near-verbatim copy share, copy_stat m >= (l.257)', '0.90', p12('manuscript/prereg/2026-10-22_c_stage1/DESIGN.md'), 'design', '11_supplement_registered_rows.md'],
 ['4', 'manuscript/prereg/2026-10-22_c_stage1/DESIGN.md::§4.2 batch, qwen25vl_7b (l.181)', '4', p12('manuscript/prereg/2026-10-22_c_stage1/DESIGN.md'), 'design', '03_method.md'],
 ['2', 'manuscript/prereg/2026-10-22_c_stage1/DESIGN.md::§4.2 batch, internvl3_8b (l.182)', '2', p12('manuscript/prereg/2026-10-22_c_stage1/DESIGN.md'), 'design', '03_method.md'],
 ['2', 'manuscript/prereg/2026-10-30_c_t1/c_t1_registry.json::models.aya_vision_8b.batch_size', '2', p12('manuscript/prereg/2026-10-30_c_t1/c_t1_registry.json'), 'prereg-quoted', '03_method.md'],
]
assert [r[3] for r in ROWS] == ['6d039398c88a', '92a1f0e992cb', 'eacc9a9c737c', 'eacc9a9c737c', 'eacc9a9c737c', '09e6f90a0973']
man = head('number_manifest_C.tsv'); assert man.endswith('\n')
ml = man.split('\n')  # ml[n-1] = line n
def edit(n, num, old_used, new_used):
    c = ml[n - 1].split('\t'); assert c[0] == num and c[5] == old_used, (n, c); c[5] = new_used; ml[n - 1] = '\t'.join(c)
edit(43, '60', '03_method.md,08_english_comparison.md', '03_method.md,08_english_comparison.md,11_supplement_registered_rows.md')
tok_re = re.compile(r'(?<![\w.])[+−-]?\d[\d,]*(?:\.\d+)?')
def toks(s): return [x.group(0).replace('−', '-').replace('+', '').replace(',', '') for x in tok_re.finditer(re.sub(r'`[^`]*`', ' ', s))]
t08 = toks(files['08_english_comparison.md'])
assert '0.95' not in t08 and '0.70' not in t08, 'the 0.95 / 0.70 forms are still used in 08'
edit(3907, '0.95', '08_english_comparison.md', '')
edit(3908, '0.70', '08_english_comparison.md', '')
files['number_manifest_C.tsv'] = '\n'.join(ml) + ''.join('\t'.join(r) + '\n' for r in ROWS)
assert files['number_manifest_C.tsv'].count('\n') == man.count('\n') + 6

# numbers: every token new in a file needs a manifest row with that number whose used_in names the file
rows = [l.split('\t') for l in files['number_manifest_C.tsv'].splitlines()[1:]]
def norm(x): x = x.replace('−', '-').replace('+', '').replace(',', '').strip("'"); return x
have = collections.defaultdict(set)
for r in rows:
    if len(r) >= 6:
        for u in r[5].split(','):
            have[u].add(norm(r[0]))
miss = {}
for f, s in files.items():
    if f.endswith('.md'):
        new = collections.Counter(toks(s)) - collections.Counter(toks(head(f)))
        miss[f] = sorted(k for k in new if k not in have[f] and k.lstrip('-') not in have[f])
print('new number tokens without a row naming the file:', {k: v for k, v in miss.items() if v})

# the five anchors of shell C2 and a full in-memory C2 transfer on the ruled files
spec = importlib.util.spec_from_file_location('c2', C2); c2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
pkg = c2.PKG.read_bytes(); assert sha(pkg) == c2.PKG_SHA; pkg = pkg.decode()
fin = {f: files.get(f, head(f)) for f in c2.FILES}
anchors = [(c2.B2_OLD, '06_results.md'), (c2.C2A_ANCHOR, '06_results.md'), (c2.C2B_OLD, '05_preregistration_and_analysis.md'),
           (c2.C2C_ANCHOR, '07_disclosures.md'), (c2.C1B_ANCHOR, '03_method.md')]
for a, f in anchors:
    assert head(f).count(a) == 1 and fin[f].count(a) == 1, a
    for bid, _, o, n in order:
        assert a not in o and a not in n, (bid, a)
assert fin['06_results.md'].count('#### 6.10.9 What did not run') == 1
t06 = c2.swap(fin['06_results.md'], c2.B2_OLD, c2.B2_NEW)
t06 = c2.swap(t06, c2.C2A_ANCHOR, c2.C2A_ANCHOR + '\n\n' + c2.c2a_text(pkg))
c2.swap(fin['05_preregistration_and_analysis.md'], c2.C2B_OLD, c2.C2B_NEW)
c2.swap(fin['07_disclosures.md'], c2.C2C_ANCHOR, c2.C2C_ANCHOR + c2.C2C_ADD)
c2.swap(fin['03_method.md'], c2.C1B_ANCHOR, c2.C1B_ANCHOR + c2.C1B_ADD)
mf = fin['number_manifest_C.tsv']; assert mf.endswith('\n') and c2.FORTY_QUOTE not in mf
assert not any('-c-k7:' in s for s in files.values())
print('shell C2: five anchors once before and after; simulated C2 swaps pass on the ruled files')

for f in sorted(files):
    print(f'{f:40s} {sha(head(f).encode())[:12]} -> {sha(files[f].encode())}')

# ---- compare with the targets of CC-405 Ruling 6, then write ----
_T = {'03_method.md': '2da4f2e55af5fb2990d8ce0e17b3f833b8fd96df909df6d8c0e9e083d50714a5',
      '05_preregistration_and_analysis.md': '8e635ee27de07725125ffcbbbce258885afd08b9980f6cd54902b27edde8e303',
      '06_results.md': '5443fe5ed2265d2d21451f1e42f422fc3bd2350e0276ab0676f69bb84dbff951',
      '07_disclosures.md': '72adbcb08352881cfcfe16ea661450770958d0965468c6265c3ee856d2c3c1cc',
      '08_english_comparison.md': '72f3cd8b5f916669c54490f993447f8fa5af6ba5ce240647f5a842bf6ae10b14',
      '09_limitations.md': '4111d0957ae1555922defef6096a396a3b76b300c57435c0778e8f8ebfe01df2',
      '11_supplement_registered_rows.md': '025d744a9413ef509558496ef55694188dd7249baace8a946aa98c81c791f165',
      'number_manifest_C.tsv': '83414dc3d863bbe62c67b64c4dd0cb9b3f9796fc7247575b08a9bf7f296d1f81'}
assert set(files) == set(_T), sorted(set(files) ^ set(_T))
for _f, _want in _T.items():
    assert _h.sha256(files[_f].encode()).hexdigest() == _want, f'sha differs from CC-405 Ruling 6: {_f}'
for _f, _text in files.items():
    (_p.Path(_R) / 'paper_v1_analysis' / _f).write_bytes(_text.encode())
print('WRITTEN: 8 files equal to the CC-405 Ruling 6 targets')
