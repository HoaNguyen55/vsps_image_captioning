#!/usr/bin/env python3
"""C-ATTR-DEV -> Paper C paper repo: build the transferred text by script (CC-358 R5 / TG1-TG11, CC-363 R7 / W1-W7).

Reads: the package (e1be6f93), CC-363 (904ecf43, for the Ruling 3 sentence only), the committed result files
data/results/c_attr_1112_score/res/ (checked against SHA256SUMS cb0af612), and the paper files at paper-repo HEAD.
Writes: the paper repo WORKING TREE only (never git add / commit) and, in argv[1], parts.md + fills.json for the note.
Numbers come only from res/. Keys whose files are not in res/ (S10A, S10B, STEP10, D1, STEP1B0, CAP, GS1, GS1B, K0,
SUM::n_b1_runs) keep the package token and are listed as TG2 OPEN.
Usage: python3 -I c_attr_transfer.py <out_dir>
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

RUN = Path('/mnt/d/vsps_image_captioning')
PAPER = Path('/mnt/d/vsps_papers/vsps-paperC-tallip')
PD = 'paper_v1_analysis'
PKG = RUN / 'manuscript/prereg/2026-11-11_c_attr_dev/paper_text/C_ATTR_PAPER_TEXT_v1.md'
CC363 = RUN / '.session_backup/2026-10-13/decisions/CC-363.txt'
RESD = RUN / 'data/results/c_attr_1112_score'
RES = RESD / 'res'
RESREL = 'data/results/c_attr_1112_score/res/'
OUT = Path(sys.argv[1])

PKG_SHA = 'e1be6f939ab4961347b0d6d6f211150b06d171bb3459a3e3f6454c56b76817c1'
CC363_SHA = '904ecf4368654017dd9988592a2801d7b71beb9b71fa9f2a391d59bf38916c81'
SUMS_SHA = 'cb0af612fcc5a8f7789e600ccbce6f8bb347bef566ae44cef4dfe8203ef741e5'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ---------------------------------------------------------------- integrity gates (fail closed)
assert sha(PKG) == PKG_SHA, 'package sha'
assert sha(CC363) == CC363_SHA, 'CC-363 sha'
assert sha(RESD / 'SHA256SUMS') == SUMS_SHA, 'SHA256SUMS sha'
SUMS = {ln.split()[1]: ln.split()[0] for ln in (RESD / 'SHA256SUMS').read_text().splitlines() if ln.strip()}
for rel, h in SUMS.items():
    assert sha(RESD / rel) == h, rel
assert subprocess.run(['git', '-C', str(PAPER), 'rev-parse', 'HEAD'], capture_output=True, text=True,
                      check=True).stdout.strip().startswith('f6aa449'), 'paper HEAD'

L = PKG.read_text(encoding='utf-8').split('\n')


def pl(n):
    return L[n - 1]


def segs(n):
    return re.findall(r'"([^"]*)"', pl(n))


def unquote(a, b):
    out = []
    for ln in L[a - 1:b]:
        if ln.startswith('> > '):
            out.append('> ' + ln[4:])
        elif ln.startswith('> '):
            out.append(ln[2:])
        elif ln == '>':
            out.append('')
        else:
            raise ValueError(f'unquoted line {ln[:40]!r}')
    return out


def head(path):
    return subprocess.run(['git', '-C', str(PAPER), 'show', f'HEAD:{PD}/{path}'], capture_output=True, check=True
                          ).stdout.decode('utf-8')


# ---------------------------------------------------------------- results (res/ only)
M = ['qwen25vl_7b', 'internvl3_8b', 'aya_vision_8b']
DISP = {'qwen25vl_7b': 'Qwen2.5-VL-7B', 'internvl3_8b': 'InternVL3-8B', 'aya_vision_8b': 'Aya-Vision-8B'}
TDISP = dict(DISP, internvl3_8b='InternVL3-8B (τ = −∞)')
SETD = {'ov_dev_a': 'OV-dev-A', 'ov_dev_b': 'OV-dev-B', 'xm_dev500': 'XM-dev500'}
UNITD = {'i_syllables': '(i) syllables', 'ii_words': '(ii) words'}
EST = {'tau_any': 'τ_any', 'tau_sel': 'τ_sel', 'tau_marg': 'τ_marg', 'tau_pair': 'τ_pair'}
FILES = {'NOM': 'c_attr_nomination.json', 'VER': 'VERDICT.json', 'SUM': 'SUMMARY.json', 'DFS': 'DFSENS.json',
         'PH': 'POSTHOC.json', 'VFY': 'VERIFY.json'}
for s in ('ov_dev_b', 'xm_dev500'):
    for m in M:
        FILES[f'CB_{s}_{m}'] = f'COPYBOUND_{s}_{m}.json'
J = {a: json.loads((RES / f).read_text(encoding='utf-8')) for a, f in FILES.items()}
FMETA = {a: (RESREL + f, SUMS['res/' + f]) for a, f in FILES.items()}

# ---- Phase-A sources (coordinator rule, 2026-11-12): (a) committed file pinned by a ruling/LOG line, or (b) a
# count/record file of a read-only pull whose sha matches that pull's SHA256SUMS, whose own sha is LOG-pinned.
PULL = '.session_backup/machines/ATTR_H1/root/outputs/'
BSUMS_SHA = 'a2b63fef7532c70422817ba75539db91c529f2beadf2c4821b1c3344c7593ff7'    # block 1 (OPS-1112c; VERIFY tree b)
B1SUMS_SHA = '0754128c7bab2cfac4a001b534cce6bb68bb8de8e143d29c5af6233ffb6d5113'   # block 1b (OPS-1112af)
PINNED = {PULL + 'c_attr_b1/CAP_1B.json': '6d42608e205a495215b2d1df30b70ea18d4fa65cc6c5edee437d1fe449a5c3a7',
          PULL + 'c_attr_b1/STEPS_1B.tsv': 'bd9139b03dd1d5734ea189fff7c532de18387abc4208a07f8b9a7c2d6d711ea4',
          'scripts/c_attr/block0/K0_REPORT.json': '15108f2b1260770e4aa92fb44ae6301df45106b52a334d4b33068a4cf1028019'}
SRCLOG = []   # (file, sha, how verified)


def pullsums(sub, want):
    sp = RUN / PULL / sub / 'SHA256SUMS'
    assert sha(sp) == want, sub
    return {ln.split()[1]: ln.split()[0] for ln in sp.read_text().splitlines() if ln.strip()}


PS = {'c_attr': pullsums('c_attr', BSUMS_SHA), 'c_attr_b1': pullsums('c_attr_b1', B1SUMS_SHA)}


def ext(alias, rel):
    h = sha(RUN / rel)
    if rel in PINNED:
        assert h == PINNED[rel], rel
        how = 'LOG/ruling pin' + ('; HEAD blob equal' if not rel.startswith(PULL) else '')
        if not rel.startswith(PULL):
            assert hashlib.sha256(subprocess.run(['git', '-C', str(RUN), 'show', f'HEAD:{rel}'], capture_output=True,
                                                 check=True).stdout).hexdigest() == h, rel
    else:
        sub, inner = rel[len(PULL):].split('/', 1)
        assert PS[sub][inner] == h, rel
        how = f'pull SHA256SUMS of {sub} ({(BSUMS_SHA if sub == "c_attr" else B1SUMS_SHA)[:8]})'
    J[alias] = json.loads((RUN / rel).read_text(encoding='utf-8')) if rel.endswith('.json') else None
    FMETA[alias] = (rel, h)
    SRCLOG.append((rel, h, how))


for m in M:
    for s in (('ov_dev_b', 'ov_dev_a') if m != 'aya_vision_8b' else ('ov_dev_b',)):
        ext(f'S10A_{m}_{s}', PULL + f'c_attr/parity/S10a_{m}_{s}.json')
    ext(f'S10B_{m}', PULL + f'c_attr/parity/S10b_{m}.json')
    ext(f'STEP10_{m}', PULL + f'c_attr/parity/STEP10_{m}.json')
    ext(f'D1_{m}', PULL + f'c_attr_b1/parity/D1_{m}.json')
    ext(f'STEP1B0_{m}', PULL + f'c_attr_b1/parity/STEP1B0_{m}.json')
ext('CAP', PULL + 'c_attr_b1/CAP_1B.json')
ext('K0', 'scripts/c_attr/block0/K0_REPORT.json')
ext('STEPS1B', PULL + 'c_attr_b1/STEPS_1B.tsv')
LOGMD = (RUN / '.session_backup/2026-10-13/decisions/LOG.md').read_text(encoding='utf-8').split('\n')


def opsline(tag):
    hits = [x for x in LOGMD if tag in x[:120]]
    assert len(hits) >= 1, tag
    return hits[0]


def joblog(sub, ops_tag):
    """job.log is outside the sums by design: use only lines whose content the OPS line also states."""
    rel = PULL + sub + '/logs/job.log'
    lines = (RUN / rel).read_text(encoding='utf-8').split('\n')
    done = [x for x in lines if ' JOB DONE gpu_h ' in x]
    assert len(done) == 1 and not any(('CAP STOP' in x or 'JOB STOP' in x) for x in lines)
    gh = done[0].rsplit(' ', 1)[1]
    ops = opsline(ops_tag)
    assert f'gpu_h {gh}' in ops and 'no CAP STOP' in ops, ops_tag
    J['GS1' if sub == 'c_attr' else 'GS1B'] = {'gpu_h': gh}
    FMETA['GS1' if sub == 'c_attr' else 'GS1B'] = (rel + ' (line "JOB DONE gpu_h", also stated in ' + ops_tag + ')',
                                                   sha(RUN / rel))
    SRCLOG.append((rel, sha(RUN / rel), f'outside the pull sums by design; only the JOB DONE line (and, for block 1b, '
                                        f'the OK lines) used, each stated by {ops_tag}'))
    return lines


joblog('c_attr', 'OPS-1112c-c-attr-block1-done')
JL1B = joblog('c_attr_b1', 'OPS-1112af-c-attr-1b-done-pull')
steps = [x.split()[0] for x in (RUN / PULL / 'c_attr_b1/STEPS_1B.tsv').read_text().splitlines() if x.strip()]
okl = [x for x in JL1B if ' OK' in x]                    # the OPS line's "55 OK lines" (D1, preflight and others included)
assert len(okl) == 55 and '55 OK lines' in opsline('OPS-1112af-c-attr-1b-done-pull')
done_steps = [s_ for s_ in steps if any(x.rstrip().endswith(' OK ' + s_) for x in okl)]
assert len(done_steps) == len(steps) == 50
J['SUMR'] = {'n_b1_runs': len(done_steps)}
FMETA['SUMR'] = (PULL + 'c_attr_b1/STEPS_1B.tsv (steps) + logs/job.log (OK lines, count stated by OPS-1112af)',
                 PINNED[PULL + 'c_attr_b1/STEPS_1B.tsv'])
B1 = 'batch size 1; registered in v1.2 after K1 fired, on string-identity counts only'
BAT = 'A1 not met; batched decode; descriptive'
SPLIT, REDEC = 'split of a known τ_sel', 'batch-1 re-decode of a known τ_sel'
FLOOR = 1 / 2001

FILLS = []
CUR = ['']


def g(alias, *keys):
    o = J[alias]
    for k in keys:
        o = o[k]
    return o


def keystr(keys):
    return '.'.join(str(k) for k in keys)


def rec(alias, keys, raw, printed, kind='number'):
    rel, h = FMETA[alias]
    FILLS.append({'alias': alias, 'file': rel, 'key': keystr(keys), 'raw': raw,
                  'printed': printed, 'kind': kind, 'used_in': CUR[0], 'sha12': h[:12]})
    return printed


def fb(x):  # bound: two decimals, U+2212 for negatives, never "-0.00"
    s = f'{x:.2f}'
    if s in ('-0.00', '0.00'):
        return '0.00'
    return s.replace('-', '−')


def fd(x):  # point: signed, two decimals
    s = fb(x)
    return s if s.startswith('−') or s == '0.00' else '+' + s


def num(alias, keys, dec=2, signed=False):
    v = g(alias, *keys)
    p = (fd(v) if signed else fb(v)) if dec == 2 else f'{v:.{dec}f}'
    return rec(alias, keys, v, p)


def iv(alias, keys, ninety=False):
    d = rec(alias, keys + ['d'], g(alias, *keys, 'd'), fd(g(alias, *keys, 'd')))
    lo = rec(alias, keys + ['lo'], g(alias, *keys, 'lo'), fb(g(alias, *keys, 'lo')))
    hi = rec(alias, keys + ['hi'], g(alias, *keys, 'hi'), fb(g(alias, *keys, 'hi')))
    s = f'{d} [{lo}, {hi}]'
    if ninety:
        lo9 = rec(alias, keys + ['lo90'], g(alias, *keys, 'lo90'), fb(g(alias, *keys, 'lo90')))
        hi9 = rec(alias, keys + ['hi90'], g(alias, *keys, 'hi90'), fb(g(alias, *keys, 'hi90')))
        s += f' (90% interval [{lo9}, {hi9}])'
    return s


def pval(alias, keys, table=True):
    v = g(alias, *keys, 'p')
    if abs(v - FLOOR) < 1e-12:
        p = 'at its floor (1/2,001)' if table else '1/2,001, its floor'
    else:
        p = f'{v:.3g}'
    return rec(alias, keys + ['p'], v, p)


def lab(alias, keys):
    return rec(alias, keys + ['label'], g(alias, *keys, 'label'), g(alias, *keys, 'label'), 'label')


def fill_simple(text):
    """Fill {{ALIAS::key}} tokens whose alias is in res/; leave the TG2-OPEN tokens as written."""
    def sub(mo):
        alias, key = mo.group(1), mo.group(2)
        if alias not in FILES or (alias, key) == ('SUM', 'n_b1_runs'):   # res/ only; Phase-A tokens: fill_phase_a
            return mo.group(0)
        if key.endswith('|count'):
            k = key[:-6].split('.')
            return rec(alias, k, g(alias, *k), str(len(g(alias, *k))), 'count')
        k = key.split('.')
        v = g(alias, *k)
        return rec(alias, k, v, str(v), 'number' if isinstance(v, (int, float)) else 'text')
    return re.sub(r'\{\{([A-Za-z0-9_]+)::([^}]+)\}\}', sub, text)


def qhalf(v, places):  # half-up on the stored decimal string (avoids binary ties such as 0.00925 -> 0.0092)
    from decimal import Decimal, ROUND_HALF_UP
    return str(Decimal(repr(v)).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))


def fmt_a(alias, key, v):
    leaf = key.split('.')[-1]
    if alias == 'CAP':
        return f'{v:.2f}'
    if alias == 'K0':
        if leaf == 'refill_share_8':
            return f'{v:.6f}'
        if leaf.startswith('overlap'):
            return qhalf(v, 4)
        if leaf.startswith('mean_cos'):
            return qhalf(v, 3)
    if alias.startswith('STEP10_') and leaf == 'A1':
        return v + (' (K1 fired)' if v == 'FAIL' else '')
    return str(v)


def fill_phase_a(text, where):
    """Second pass: fill the Phase-A tokens from the verified sources; anything else stays and is listed."""
    CUR[0] = where

    def sub(mo):
        alias, key = mo.group(1), mo.group(2)
        if (alias, key) == ('SUM', 'n_b1_runs'):
            alias, key = 'SUMR', 'n_b1_runs'
        if alias not in FMETA or alias in FILES:
            return mo.group(0)
        if key.endswith('|count'):
            k = key[:-6].split('.')
            return rec(alias, k, len(g(alias, *k)), str(len(g(alias, *k))), 'count')
        k = key.split('.')
        v = g(alias, *k)
        return rec(alias, k, v, fmt_a(alias, key, v), 'number' if isinstance(v, (int, float)) else 'label')
    return re.sub(r'\{\{([A-Za-z0-9_]+)::([^}]+)\}\}', sub, text)


OPEN_RE = re.compile(r'\{\{(S10A_\w+|S10B_\w+|STEP10_\w+|D1_\w+|STEP1B0_\w+|CAP|GS1|GS1B|K0)::[^}]+\}\}'
                     r'|\{\{SUM::n_b1_runs\}\}')


def check_closed(text, where):
    rest = OPEN_RE.sub('', text)
    for bad in ('{{', '}}', '[[', ']]', '<m>', '<set>', '<est>', '<backbone>', '<Backbone>', '<estimand>',
                '<u>', '<stage>', '…p}', '…label'):
        assert bad not in rest, f'{where}: unresolved {bad!r}'
    return text


def row(cells):
    return '| ' + ' | '.join(cells) + ' |'


# ---------------------------------------------------------------- paper files at HEAD
F = {n: head(n) for n in ('03_method.md', '05_preregistration_and_analysis.md', '06_results.md',
                         '07_disclosures.md', '09_limitations.md', '11_supplement_registered_rows.md',
                         'paperC.bib', 'paperC_bib_audit.tsv', 'number_manifest_C.tsv')}
BLOCKS = []  # (id, phase, package lines, file, inserted text)


def once(text, old, where):
    assert text.count(old) == 1, f'{where}: anchor count {text.count(old)}'


def ins_after(fn, anchor, new, bid, phase, plines):
    once(F[fn], anchor, bid)
    F[fn] = F[fn].replace(anchor, anchor + new)
    BLOCKS.append((bid, phase, plines, fn, new.strip('\n')))


def repl(fn, old, new, bid, phase, plines):
    once(F[fn], old, bid)
    F[fn] = F[fn].replace(old, new)
    BLOCKS.append((bid, phase, plines, fn, new.strip('\n')))


def para(lines):
    """Package paragraphs -> paper markdown: whole-line bold headings become headings."""
    out = []
    for ln in lines:
        mo = re.fullmatch(r'\*\*(\d+\.\d+(?:\.\d+)?) (.+)\*\*', ln)
        if mo:
            ln = ('#### ' if mo.group(1).count('.') == 2 else '### ') + mo.group(1) + ' ' + mo.group(2)
        out.append(ln)
    return '\n'.join(out)


# ================================================================= Phase A + B text
# ---- Section 3: opening clause (P1) and 3.8 (package l.64-90)
CUR[0] = '03_method.md §3.8'
clause = segs(46)[1]
assert clause.startswith('… and Section 3.8 ')
repl('03_method.md',
     'Section 3.6 describes the scorer, and Section 3.7 the two arms added for the Flickr30K registration.',
     'Section 3.6 describes the scorer, Section 3.7 the two arms added for the Flickr30K registration, '
     + clause[2:], 'P1-open', 'A', '46')
s38 = para(unquote(64, 90))
TG8_CUTS = []
once(s38, ' Section 6.10.8 states which of them ran.', 'TG8 3.8')
s38 = s38.replace(' Section 6.10.8 states which of them ran.', '')
TG8_CUTS.append(('03_method.md §3.8 "Not used." (package l.90)', 'cut " Section 6.10.8 states which of them ran."'))
s38 = check_closed(fill_simple(s38), '3.8')
assert F['03_method.md'].endswith('not the published system.\n')
F['03_method.md'] += '\n' + s38 + '\n'
BLOCKS.append(('P1', 'A', '64-90', '03_method.md', s38))

# ---- Box 1 rows (l.96-102)
CUR[0] = '05 Box 1'
box1 = '\n'.join(L[95:102])
assert all(r.startswith('| ') for r in L[95:102])
detected = [ln for ln in F['05_preregistration_and_analysis.md'].split('\n') if ln.startswith('| detected |')]
assert len(detected) == 1
ins_after('05_preregistration_and_analysis.md', detected[0] + '\n', box1 + '\n', 'P2', 'A', '96-102')

# ---- 5.5 cross-reference (TG8), 5.6 closing sentence (l.108), 5.7 (l.112-162)
repl('05_preregistration_and_analysis.md', 'The cap was not reached (Section 6.10).',
     'The cap was not reached (Section 6.11).', 'TG8-5.5', 'A', '-')
s56 = unquote(108, 108)[0]
ins_after('05_preregistration_and_analysis.md', 'and Section 6.9 reports their outcome.', ' ' + s56,
          'P3-5.6', 'A', '108')
s57 = para(unquote(112, 162))
HOLD_P3 = ('Each image\'s random draws are seeded by its own id and are independent across images, so the variance '
           'of the draw-averaged difference d̄_i is [Var(m_I) + E σ²_I / R] / n, with m_i the image\'s expected '
           'difference and σ²_i its between-draw variance (law of total variance). The image bootstrap of d̄_i '
           'estimates exactly this quantity, so the interval includes the variance of the random draw at any R ≥ 1 '
           '(Proposition 3a of the registration); the same holds for `perm` over D. A shared `fix` set is different '
           '(Section 6.10.5). ')
once(s57, HOLD_P3, 'P-3 hold')
s57 = s57.replace(HOLD_P3, '')                       # CC-358 R5 Phase A (ii): held until the P-3 read
assert s57.count('[@Holm1979]') == 1              # TG6: Holm verified on OpenAlex (W2121044470) -> kept
once(s57, '(S-BB; Section 6.10.8)', 'TG8 5.7')
s57 = s57.replace('(S-BB; Section 6.10.8)', '(S-BB)')
TG8_CUTS.append(('05 §5.7 "Multiplicity." (package l.140)', '"(S-BB; Section 6.10.8)" -> "(S-BB)"'))
s57 = check_closed(fill_simple(s57), '5.7')
F['05_preregistration_and_analysis.md'] = F['05_preregistration_and_analysis.md'].rstrip('\n') + '\n\n' + s57 + '\n'
BLOCKS.append(('P3-5.7', 'A+B (Order of looks = B)', '112-162 minus P-3 sentences of l.122', '05_preregistration_and_analysis.md', s57))

# ================================================================= Section 6.10 (P4, P5)
CUR[0] = '06_results.md §6.10'
box_610 = '\n'.join(unquote(199, 201)).replace('**6.10 Attribution of the retrieval gain on development data**',
                                               '### 6.10 Attribution of the retrieval gain on development data')
s6101 = check_closed(fill_simple(unquote(203, 203)[0]), '6.10.1')
s6102 = check_closed(para(unquote(170, 182)), '6.10.2')

# ---- 6.10.3: Table 15 (NOM rows)
CUR[0] = '06_results.md §6.10.3 Table 15'
nominated = g('NOM', 'nominated')
rec('NOM', ['nominated'], nominated, ', '.join(nominated), 'text')
t15 = [pl(209), '', pl(211), pl(212)]
for m in ('qwen25vl_7b', 'internvl3_8b'):
    for e in ('tau_pair', 'tau_marg', 'tau_sel'):
        k = ['rows', f'{m}|{e}']
        note = REDEC if e == 'tau_sel' else SPLIT
        if e != 'tau_sel':
            assert g('NOM', *k, 'note') == SPLIT
        nom = 'not a candidate' if e == 'tau_sel' else (
            'yes' if f'H_{e[4:]}({m})' in nominated else 'no')
        t15.append(row([TDISP[m], EST[e], iv('NOM', k), note, nom]))
T15 = '\n'.join(t15)

# ---- N+ opening (l.243), Holm order, Table 16
CUR[0] = '06_results.md §6.10.3'
assert 'closed' not in J['NOM'] and nominated, 'case N+ only'
cname = {c: re.sub(r'\((\w+)\)', lambda mo: '(' + DISP[mo.group(1)] + ')', c) for c in nominated}
open_n = segs(243)[0]
open_n = open_n.replace('{{NOM::nominated|count}}', str(len(nominated))).replace(
    '{{NOM::nominated|names}}', ' and '.join(cname[c] for c in nominated))
mfam = len(nominated)
VB = ['sets', 'ov_dev_b', 'rows']
ordr = sorted(nominated, key=lambda c: (g('VER', *VB, f"{re.search(r'[(](\w+)[)]', c).group(1)}|tau_{c[2:6]}", 'p'), c))
alpha = {}
for j, c in enumerate(ordr, 1):
    alpha[c] = 0.025 / (mfam - j + 1)
assert alpha == {'H_pair(internvl3_8b)': 0.0125, 'H_pair(qwen25vl_7b)': 0.025}, alpha
assert g('VER', 'alpha_familywise_one_sided') == 0.025

CUR[0] = '06_results.md §6.10.3 Table 16'
AYA_FLAG = 'placebo flagged (Section 6.10.5)'       # W2 (writer-composed marker)
t16 = [pl(222), '', pl(224), pl(225)]
order16 = [('qwen25vl_7b', 'tau_pair'), ('qwen25vl_7b', 'tau_marg'), ('qwen25vl_7b', 'tau_sel'),
           ('internvl3_8b', 'tau_pair'), ('internvl3_8b', 'tau_marg'), ('internvl3_8b', 'tau_sel'),
           ('aya_vision_8b', 'tau_pair'), ('aya_vision_8b', 'tau_marg'), ('aya_vision_8b', 'tau_sel'),
           ('qwen25vl_7b', 'tau_any'), ('internvl3_8b', 'tau_any'), ('aya_vision_8b', 'tau_any')]
for m, e in order16:
    k = VB + [f'{m}|{e}']
    r = g('VER', *k)
    assert r['batch'] == B1
    claim = f'H_{e[4:]}({m})' in nominated
    fam = 'nominated claims' if claim else 'none'
    assert (r['family'] == 'registered (§7.5)') == claim and r['m'] == (mfam if claim else 1)
    note = {'tau_sel': REDEC, 'tau_any': '–'}.get(e, SPLIT)
    if e in ('tau_pair', 'tau_marg'):
        assert r['note'] == SPLIT
    if e == 'tau_sel':
        assert r['note'] == REDEC
    if m == 'aya_vision_8b' and e in ('tau_pair', 'tau_marg'):
        note += '; first look, no registered claim'
    if m == 'aya_vision_8b' and e != 'tau_pair':
        note = (note + '; ' if note != '–' else '') + AYA_FLAG
    t16.append(row([TDISP[m] if e != 'tau_any' else TDISP[m], EST[e], iv('VER', k), pval('VER', k),
                    f"{fam}, {rec('VER', k + ['m'], r['m'], str(r['m']))}", lab('VER', k), note]))
T16 = '\n'.join(t16)

# ---- PASS sentences (l.244), Qwen first (registration §7.5 item 4)
pass_t = segs(244)[0]
sent = []
for c in sorted(nominated, key=lambda c: 0 if 'qwen' in c else 1):
    m = re.search(r'\((\w+)\)', c).group(1)
    e = 'tau_' + c[2:6]
    k = VB + [f'{m}|{e}']
    r = g('VER', *k)
    assert r['label'] == 'DETECTED' and r['d'] >= 2.0 and r['p'] <= alpha[c]
    s = (pass_t.replace('<Claim c>', cname[c]).replace("<backbone>'s", DISP[m] + "'s").replace('<estimand>', EST[e])
         .replace('[[VER::sets.ov_dev_b.rows.<m>~<est>]]', iv('VER', k)).replace('{{…p}}', pval('VER', k, False))
         .replace('{{α_j}}', f'{alpha[c]:g}').replace('{{…m}}', str(r['m'])))
    rec('VER', k + ['label'], r['label'], 'PASS (label DETECTED)', 'label')
    sent.append(check_closed(s, 'PASS'))
PASS_P = ' '.join(sent)

# ---- non-nominated rows (l.249-253)
DET_T, NEG_T, AYA_T = segs(249)[0], segs(251)[0], segs(253)[0]
assert DET_T.endswith('{{; split of a known τ_sel | ; batch-1 re-decode of a known τ_sel}}.')


def row_sentence(m, e):
    k = VB + [f'{m}|{e}']
    r = g('VER', *k)
    assert r['m'] == 1 and r['family'] is None
    note = '; ' + r['note'] if r.get('note') else ''
    if m == 'aya_vision_8b' and e != 'tau_pair':
        note += '; placebo flagged on this set (Section 6.10.5)'   # W2 (writer-composed)
    head_ = f"{DISP[m]}'s {EST[e]}"
    if r['label'] == 'DETECTED':
        s = DET_T.replace("<Backbone>'s <estimand>", head_).replace('[[…]]', iv('VER', k)).replace(
            '{{…p}}', pval('VER', k, False)).replace(
            '{{; split of a known τ_sel | ; batch-1 re-decode of a known τ_sel}}', note)
    elif r['label'] == 'NEGLIGIBLE':
        s = NEG_T.replace("<Backbone>'s <estimand>", head_).replace('[[…|90]]', iv('VER', k, ninety=True))
        n1 = ''
        if r['lo'] > 0 or r['hi'] < 0:                          # CC-363 N1 (filled from the file)
            n1 = (f" (its 95% interval, [{fb(r['lo'])}, {fb(r['hi'])}], excludes zero; NEGLIGIBLE means inside "
                  f"±2.0, not zero)")
        s = s.replace('a descriptive row{{note}}.', 'a descriptive row' + note + n1 + '.')
    else:
        raise AssertionError(f'unexpected label {r["label"]} at {m} {e}')
    rec('VER', k + ['label'], r['label'], r['label'], 'label')
    return check_closed(s, f'row {m} {e}')


nonnom = []
for m in ('qwen25vl_7b', 'internvl3_8b'):
    for e in ('tau_pair', 'tau_marg', 'tau_sel', 'tau_any'):
        if f'H_{e[4:]}({m})' not in nominated:
            nonnom.append(row_sentence(m, e))
aya = [AYA_T] + [row_sentence('aya_vision_8b', e) for e in ('tau_pair', 'tau_marg', 'tau_sel', 'tau_any')]

# ---- DF sensitivity (l.336)
CUR[0] = '06_results.md §6.10.3 (last paragraph); Table S25a'
assert g('DFS', 'status') == 'computed'
rec('DFS', ['status'], 'computed', 'computed', 'text')
DF_S = segs(336)[1]
assert DF_S.startswith('Recomputing document frequencies')

s6103 = '\n\n'.join(['#### 6.10.3 The registered claim (nomination, then one look)', T15, open_n, T16, PASS_P,
                     ' '.join(nonnom), ' '.join(aya), DF_S])

# ---- 6.10.4 (l.265)
CUR[0] = '06_results.md §6.10.4'
s6104 = '#### 6.10.4 XM-dev500 at batch size 1 (no rule)\n\n' + segs(265)[0]

# ---- 6.10.5 (l.286-290, CC-363 Ruling 3, Ruling A)
CUR[0] = '06_results.md §6.10.5'
cc = CC363.read_text(encoding='utf-8').split('\n')
R3 = ' '.join(x.strip() for x in cc[268:272])
assert R3.startswith('"A recorded review found') and R3.endswith('printed with this flag."')
R3 = R3[1:-1]
flagged = []
for s in ('ov_dev_b', 'xm_dev500'):
    for m in M:
        k = ['sets', s, 'rows', f'{m}|placebo_d1_d2']
        if g('SUM', *k, 'flag'):
            flagged.append((s, m))
assert flagged == [('ov_dev_b', 'aya_vision_8b')], flagged
assert g('VER', *VB, 'aya_vision_8b|placebo_d1_d2', 'flag') is True
pf = segs(287)[0]
k = VB + ['aya_vision_8b|placebo_d1_d2']
pf = pf.replace('<backbone>', DISP['aya_vision_8b']).replace('<set>', 'OV-dev-B').replace('[[…]]', iv('VER', k))
rec('VER', k + ['flag'], True, 'flagged', 'label')
once(pf, '{{review id and its consequence}}.', 'W2')
pf = pf.replace('{{review id and its consequence}}.', R3)       # W2: Ruling 3 sentence verbatim
share_t = segs(288)[0]
once(share_t, '; the intervals of Tables 16 and S21 include this part (Section 5.7).', 'TG8 share')
share_t = share_t.replace('; the intervals of Tables 16 and S21 include this part (Section 5.7).', '.')
TG8_CUTS.append(('06 §6.10.5 draw-share sentences x6 (package l.288)',
                 'cut "; the intervals of Tables 16 and S21 include this part (Section 5.7)" (its support, the 5.7 '
                 'draw-variance sentences, is held for the P-3 read)'))
shares = []
for s in ('ov_dev_b', 'xm_dev500'):
    for m in M:
        shares.append(share_t.replace('{{…share}}', num('SUM', ['sets', s, 'variance', m, 'share'], 3)).replace(
            "<backbone>'s", DISP[m] + "'s").replace('<set>', SETD[s]))
fix_t = segs(290)[0]
fixs = []
for s in ('ov_dev_b', 'xm_dev500'):
    k = ['batched', s, 'fixed_set', 'qwen25vl_7b']
    assert g('SUM', *k, 'omega_upper') > 0.25 and g('SUM', *k, 'label') == 'conditional on the realised fixed set'
    rec('SUM', k + ['label'], g('SUM', *k, 'label'), g('SUM', *k, 'label'), 'label')
    fixs.append(fix_t.replace('<set>', SETD[s]).replace('{{omega}}', num('SUM', k + ['omega'])).replace(
        '{{omega_upper}}', num('SUM', k + ['omega_upper'])))
RULING_A_NOTE = 'Conditional on the realised fixed set (development estimate, batched decodes, Section 6.10.5).'
ra = ('By the same registered rule, every `fix` row of the paper carries the table note "' + RULING_A_NOTE[:-1]
      + '"; the note is words only, and no number of this section enters a test table.')   # Ruling A (writer-composed)
s6105 = '\n\n'.join(['#### 6.10.5 Placebo, variance components and the fixed set', pf + ' ' + ' '.join(shares),
                     ' '.join(fixs) + ' ' + ra])

# ---- 6.10.6 Table 17 and sentences (l.295-314), swap (l.342-350)
CUR[0] = '06_results.md §6.10.6 Table 17'
t17 = [pl(295), '', pl(297), pl(298)]
cb_sent = {}
for s in ('ov_dev_b', 'xm_dev500'):
    for m in M:
        a = f'CB_{s}_{m}'
        wd = any(g(a, 'bound', u, 'n3', 'withdrawn') for u in UNITD)
        assert not wd, 'withdrawal case not built'
        for u in UNITD:
            rec(a, ['bound', u, 'n3', 'withdrawn'], False, 'in force', 'label')
            mono = g(a, 'bound', u, 'monotonicity check failed')
            assert mono is False
            rec(a, ['bound', u, 'monotonicity check failed'], False, '–', 'label')
            flags = '–'
            if s == 'ov_dev_b' and m == 'aya_vision_8b':
                flags = 'L_cp and K_nc contain `rand`: ' + AYA_FLAG
            if s == 'xm_dev500' and m == 'aya_vision_8b':
                flags = BAT                                    # W1 (source: scoring run doc v1.1 §1 step 5)
            cells = [SETD[s], DISP[m] if m != 'internvl3_8b' else TDISP[m], UNITD[u]]
            for q in ('K_ret', 'L_cp', 'K_nc'):
                kk = ['bound', u, 'n3', q]
                cells.append(iv(a, kk) + ', ' + lab(a, kk))
            t17.append(row(cells + ['in force', flags]))
T17 = '\n'.join(t17)

CUR[0] = '06_results.md §6.10.6'
LE0 = segs(308)[0]
cbs = []
for s in ('ov_dev_b', 'xm_dev500'):
    for m in M:
        a = f'CB_{s}_{m}'
        for u in UNITD:
            kk = ['bound', u, 'n3', 'L_cp']
            r = g(a, *kk)
            assert r['label'] != 'DETECTED' and r['d'] <= 0, 'only the L_cp <= 0 sentence is built'
            cbs.append(check_closed(LE0.replace('On <set>, unit <u>,', f'On {SETD[s]}, {DISP[m]}, unit {UNITD[u]},')
                                    .replace('[[…L_cp]]', iv(a, kk)), 'copy'))
tier_ovb, tier_xm = segs(311)[0], segs(311)[1]
assert tier_ovb.startswith('These rows are post hoc') and tier_xm.startswith('These rows are a first look')
for m in M:
    assert g(f'CB_ov_dev_b_{m}', 'bound', 'i_syllables', 'n3', 'K_ret', 'tier') == 'POST HOC'
    assert g(f'CB_xm_dev500_{m}', 'bound', 'i_syllables', 'n3', 'K_ret', 'tier') == 'first look'
eng, kap = segs(313)[0], segs(314)[1]
assert eng.startswith('The English copy bound') and kap.startswith('κ of a `zs` caption')

CUR[0] = '06_results.md §6.10.6 (last paragraph); Table S25b'
assert g('PH', 'swap', 'length') == {}
rec('PH', ['swap', 'length'], {}, 'NOT RUN (rule L)', 'text')
sw = segs(349)[0]
swm = [m for m in M if m in g('PH', 'swap', 'rows')]
assert swm == ['qwen25vl_7b', 'aya_vision_8b']
part = ' and '.join(f"{iv('PH', ['swap', 'rows', m, 'delta'])} for {DISP[m]} ({lab('PH', ['swap', 'rows', m, 'delta'])})"
                    for m in swm)
once(sw, 'δ = [[PH::swap.rows.<m>.delta]] for <backbone> ({{label}})', 'swap')
sw = sw.replace('[[PH::swap.rows.<m>.delta]] for <backbone> ({{label}})', part)
rl = segs(350)[0]
rls = [rl.replace('<backbone>', DISP[m]).replace('<memory>', mem) for m in swm
       for mem in ('Flickr30K-train memory', 'COCO memory')]
s6106 = '\n\n'.join(['#### 6.10.6 The copy bound (post hoc on OV-dev-B; first look at κ on XM-dev500)', T17,
                     ' '.join(cbs[:6]) + ' ' + tier_ovb, ' '.join(cbs[6:]) + ' ' + tier_xm, eng + ' ' + kap,
                     sw + ' ' + ' '.join(rls)])

# ---- 6.10.7 (l.324)
CUR[0] = '06_results.md §6.10.7'
for s in ('ov_dev_a', 'ov_dev_b', 'xm_dev500'):
    for kk, r in g('SUM', 'batched', s, 'rows').items():
        assert 'host' not in r and r['batch'] == BAT
s6107 = '#### 6.10.7 Batched rows (descriptive sensitivity row)\n\n' + segs(324)[0] + ' ' + segs(324)[1]

S610 = '\n\n'.join([box_610, s6101, s6102, s6103, s6104, s6105, s6106, s6107])
S610 = check_closed(S610, '6.10')

# ---- 6.11 Compute (l.374)
CUR[0] = '06_results.md §6.11'
s611 = unquote(374, 374)[0]
old611 = ('### 6.10 Compute\n\nThe test used 9.59 GPU-hours of the 20 GPU-hour cap on one 24 GB GPU (OpenViIC block 4.61, '
          'XM3600 block 4.90, pre-test decode-parity checks 0.08). Verified precision and all decision steps ran on CPU. '
          'The development stages used 6.84 and 4.91 GPU-hours under a separate cap.')
repl('06_results.md', old611, S610 + '\n\n' + old611.replace('### 6.10 Compute', '### 6.11 Compute') + ' ' + s611,
     'P4+P5+6.11', 'A+B', '170-182, 199-203, 209-374')

# ================================================================= Section 7 (P7, P9, W7)
CUR[0] = '07_disclosures.md'
c452 = pl(452).split(' | ')
old_b2, new_b2 = c452[1].strip('"'), c452[2].rstrip(' |').strip('"')
repl('07_disclosures.md', old_b2, new_b2, 'P9-Box2', 'A', '452')
box2 = '\n'.join(L[418:422])
assert all(r.startswith('| ') for r in L[418:422])
last_b2 = [ln for ln in F['07_disclosures.md'].split('\n') if ln.startswith('| test sets re-used after their look')]
assert len(last_b2) == 1
ins_after('07_disclosures.md', last_b2[0] + '\n', box2 + '\n', 'P7-Box2rows', 'A', '419-422')
s75 = unquote(402, 413)
HOLD_W3 = ' Blocks 2–4 {{status sentence of §4.9, items B2–B4}}.'
once(s75[4], HOLD_W3, 'W3 hold')
s75[4] = s75[4].replace(HOLD_W3, '')                         # CC-363 W3: blocks 2-4 sentence held
W7 = ('- **Deviations at scoring time.** The scoring stages ran on the rented machine on CPU only, at the lowest '
      'priority, while another study of the group decoded on its GPU. The two reference files were staged again from '
      'the copies of record at their pinned hashes. The segmenter model files were restored before the verification '
      'stage and recorded only afterwards; their hashes are in the verification file, and the scoring parity gate '
      '(Section 5.7) is the check that binds them. The scoring code\'s mutant record ran without network isolation '
      '(see "Mutant check on the rented machine" above). These are stated as facts; no check beyond those named here '
      'was made of their effect.')                           # CC-363 W7 (writer-composed from Ruling 1g)
idx = [i for i, x in enumerate(s75) if x.startswith('- **Scorer fixes before any score.**')]
assert len(idx) == 1
s75.insert(idx[0] + 1, W7)
s75 = para(s75)
F['07_disclosures.md'] = F['07_disclosures.md'].rstrip('\n') + '\n\n' + s75 + '\n'
BLOCKS.append(('P7-7.5', 'A+B (scoring sentence = B; W7 bullet = B)', '402-413 minus the blocks 2-4 sentence; + W7',
               '07_disclosures.md', s75))

# ================================================================= Section 9 (P8, P9)
CUR[0] = '09_limitations.md'
c451 = pl(451).split(' | ')
old91, new91 = c451[1].strip('"'), c451[2].rstrip(' |').strip('"')
repl('09_limitations.md', old91, new91, 'P9-9.1', 'A', '451')
b91 = '\n'.join(unquote(428, 429))
ins_after('09_limitations.md', new91 + '\n', b91 + '\n', 'P8-9.1', 'A', '428-429')
s92i = unquote(433, 433)[0]
ins_after('09_limitations.md', 'the registered τ = −∞ secondary is printed beside every τ = 0.10 row for this reason.',
          ' ' + s92i, 'P8-9.2int', 'A', '433')
s92c = unquote(437, 437)[0]
ins_after('09_limitations.md', 'and the object-precision results stand as registered.', ' ' + s92c,
          'P8-9.2con', 'A', '437')
s93 = unquote(441, 441)[0]
ins_after('09_limitations.md', 'and check each run against those hashes.', ' ' + s93, 'P8-9.3', 'A', '441')

# ================================================================= Supplement (P6, P9)
SU = '11_supplement_registered_rows.md'
CUR[0] = SU
app453 = pl(453).split(' | ')[2].rstrip(' |')
assert app453.startswith('append: "')
app453 = app453[len('append: "'):-1]
ins_after(SU, 'Each code fix was a new commit with its own review, and both test blocks ran at the last of these commits.',
          ' ' + app453, 'P9-supp-closing', 'A', '453')
repl(SU, 'Decode parity on 52 OV-dev-B images: 52/52 identical for both backbones.',
     'Decode parity on 52 OV-dev-B images: 52/52 identical for both backbones (same items, same batch slices: '
     'run-to-run parity).', 'P9-supp-l711', 'A', '454')
assert '(same items, same batch slices: run-to-run parity)' in pl(454)

sup = [unquote(445, 445)[0].replace('**Attribution study (C-ATTR-DEV): every row.** ', '')]
sup_head = '### Attribution study (C-ATTR-DEV): every row'
# N4: OV-dev-A m = 1 labels of the nomination file (J12)
CUR[0] = SU + ' (nomination-file labels)'
labs = '; '.join(f"{DISP[m]} " + ', '.join(f"{EST[e]} {lab('NOM', ['rows', f'{m}|{e}'])}"
                                         for e in ('tau_pair', 'tau_marg', 'tau_sel'))
                 for m in ('qwen25vl_7b', 'internvl3_8b'))
sup.append('*Nomination-file labels (OV-dev-A, batch size 1, m = 1).* The nomination file also holds the labels the '
           'scorer applied with m = 1; they are not a rule on OV-dev-A, where the nomination rule of Section 5.7 decides, '
           'and Table 15 does not print them: ' + labs + '.')                      # CC-363 N4 (writer-composed)

# S20 (l.378-384): tokens expanded here, filled from the step-1.0 / D1 records by fill_phase_a
CUR[0] = SU + ' Table S20'
s20 = [pl(378), '', pl(380), pl(381)]
for ln, m in zip(L[381:384], M):
    ln = ln.replace(' → fired if FAIL', '')               # shell instruction; fmt_a prints "FAIL (K1 fired)"
    ln = re.sub(r'\{\{(\w+)::identical\}\}/\{\{…n\}\}', r'{{\1::identical}}/{{\1::n}}', ln)
    s20.append(ln)
assert all(g('NOM', 'parity', m, 'A1') == 'FAIL' and g('NOM', 'parity', m, 'D1') == 'PASS' for m in M)
for m in M:                                               # the record files agree with the nomination file
    assert g(f'STEP10_{m}', 'A1') == g('NOM', 'parity', m, 'A1') and g(f'STEP1B0_{m}', 'D1') == 'PASS'

# S21
CUR[0] = SU + ' Table S21'
s21 = [pl(257), '', pl(259), pl(260)]
for m in M:
    cells = [TDISP[m]]
    for e in ('tau_any', 'tau_sel', 'tau_marg', 'tau_pair'):
        k = ['sets', 'xm_dev500', 'rows', f'{m}|{e}']
        assert g('SUM', *k, 'batch') == B1
        cells.append(iv('SUM', k) + ' ' + lab('SUM', k))
    k = ['sets', 'xm_dev500', 'rows', f'{m}|placebo_d1_d2']
    fl = rec('SUM', k + ['flag'], g('SUM', *k, 'flag'), 'flagged' if g('SUM', *k, 'flag') else 'not flagged', 'label')
    cells.append(f'{iv("SUM", k)} ({fl})')
    s21.append(row(cells))

# S22
CUR[0] = SU + ' Table S22'
s22 = [pl(318), '', pl(320), pl(321)]
for s in ('ov_dev_a', 'ov_dev_b', 'xm_dev500'):
    for m in M:
        rows_ = g('SUM', 'batched', s, 'rows')
        if f'{m}|tau_sel' not in rows_:
            continue
        cells = [SETD[s], TDISP[m]]
        for e in ('tau_sel', 'tau_marg', 'tau_pair', 'tau_any'):
            k = ['batched', s, 'rows', f'{m}|{e}']
            cells.append(iv('SUM', k) + ' ' + lab('SUM', k))
        R = rec('SUM', ['batched', s, 'rows', f'{m}|tau_sel', 'R'], rows_[f'{m}|tau_sel']['R'],
                str(rows_[f'{m}|tau_sel']['R']))
        D = rec('SUM', ['batched', s, 'rows', f'{m}|tau_pair', 'D'], rows_[f'{m}|tau_pair']['D'],
                str(rows_[f'{m}|tau_pair']['D']))
        s22.append(row(cells + [f'{R}, {D}', '–']))

# S23
CUR[0] = SU + ' Table S23'
s23 = [pl(269), '', pl(271), '', pl(273), pl(274)]
for s, tier in (('ov_dev_b', 'post hoc (registration §7.7a)'), ('xm_dev500', 'descriptive')):
    for m in M:
        vk = ['sets', s, 'variance', m]
        pk = ['sets', s, 'rows', f'{m}|placebo_d1_d2']
        fl = rec('SUM', pk + ['flag'], g('SUM', *pk, 'flag'), 'flagged' if g('SUM', *pk, 'flag') else 'not flagged',
                 'label')
        s23.append(row([SETD[s], DISP[m], num('SUM', vk + ['sigma2_w']), num('SUM', vk + ['draw_part'], 3),
                        num('SUM', vk + ['total'], 3), num('SUM', vk + ['share'], 3), iv('SUM', pk), fl, tier]))
s23 += ['', pl(278), '', pl(280), pl(281)]
for s in ('ov_dev_b', 'xm_dev500'):
    k = ['batched', s, 'fixed_set', 'qwen25vl_7b']
    s23.append(row([SETD[s]] + [num('SUM', k + [x]) for x in ('MS_F', 'MS_I', 'MS_E', 'V_b', 'V_img', 'omega',
                                                             'omega_upper')]
                   + [g('SUM', *k, 'label'),
                      f"{num('SUM', k + ['dev_row', 'd'], signed=True)} [{num('SUM', k + ['dev_row', 'lo'])}, "
                      f"{num('SUM', k + ['dev_row', 'hi'])}]"]))

# Table S24 (every n, both units, companions)
CUR[0] = SU + ' Table S24'
s24 = ['**Table S24. Copy bound at every n (2, 3, 4), both units, with the companions K_rand, K_ret − K_nc and the '
       'loss of the image-blind caption. DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY. Stripped CIDEr-D points, paired 95% '
       'bootstrap CIs, B = 2,000. K_rand, K_ret − K_nc and the blind loss are labelled "descriptive; never called a '
       'bound". Tier as the scorer wrote it. Aya-Vision-8B on XM-dev500: "A1 not met; batched decode; descriptive".**',
       '', row(['set', 'backbone', 'unit', 'n', 'K_ret [95% CI], label', 'L_cp [95% CI], label',
                'K_nc [95% CI], label', 'K_rand', 'K_ret − K_nc', 'blind loss', 'tier']),
       row(['---'] * 11)]
for s in ('ov_dev_b', 'xm_dev500'):
    for m in M:
        a = f'CB_{s}_{m}'
        blind = g(a, 'blind')
        for u in UNITD:
            for n in ('n2', 'n3', 'n4'):
                b = ['bound', u, n]
                cells = [SETD[s], TDISP[m], UNITD[u], n[1]]
                for q in ('K_ret', 'L_cp', 'K_nc'):
                    cells.append(iv(a, b + [q]) + ', ' + lab(a, b + [q]))
                for q in ('K_rand', 'K_ret_minus_K_nc'):
                    assert g(a, *b, q, 'label') == 'descriptive; never called a bound'
                    cells.append(iv(a, b + [q]))
                if isinstance(blind, str) and blind.startswith('NOT RUN'):
                    assert 'blind_loss' not in g(a, *b)
                    cells.append(rec(a, ['blind'], blind, blind, 'text'))
                else:
                    assert g(a, *b, 'blind_loss', 'label') == 'descriptive; never called a bound'
                    cells.append(iv(a, b + ['blind_loss']))
                tier = rec(a, b + ['K_ret', 'tier'], g(a, *b, 'K_ret', 'tier'), g(a, *b, 'K_ret', 'tier'), 'label')
                if s == 'ov_dev_b' and m == 'aya_vision_8b':
                    tier += '; L_cp and K_nc contain `rand`: ' + AYA_FLAG
                if s == 'xm_dev500' and m == 'aya_vision_8b':
                    tier += '; ' + BAT
                s24.append(row(cells + [tier]))

# S25
CUR[0] = SU + ' Table S25'
s25 = [pl(328), '', pl(330), pl(331)]
for e in ('tau_pair', 'tau_marg'):
    k = ['rows', e]
    nom = rec('DFS', k + ['nominated'], g('DFS', *k, 'nominated'), 'yes' if g('DFS', *k, 'nominated') else 'no',
              'label')
    s25.append(row([EST[e], nom, num('DFS', k + ['d'], signed=True),
                    f"[{num('DFS', k + ['lo_df_resampled'])}, {num('DFS', k + ['hi_df_resampled'])}]",
                    f"[{num('DFS', k + ['lo_df_fixed'])}, {num('DFS', k + ['hi_df_fixed'])}]"]))
s25 += ['', pl(342), '', pl(344), pl(345)]
for m in swm:
    k = ['swap', 'rows', m]
    s25.append(row([DISP[m], iv('PH', k + ['tau_sel_f30k']), iv('PH', k + ['tau_sel_coco']),
                    iv('PH', k + ['delta']) + ', ' + lab('PH', k + ['delta']),
                    'NOT RUN (no carve run with a hash of record)', 'NOT RUN (no carve run with a hash of record)']))
s25.append('')
s25.append('InternVL3-8B has no stored Flickr30K-train carve cell, so it has no row.')   # CC-363 N3 (writer-composed)

# S26 (K0, TG2-OPEN)
CUR[0] = SU + ' Table S26'
s26 = [pl(388), '', pl(390), pl(391)]
for s in ('ov_dev_a', 'ov_dev_b', 'xm_dev500'):
    for p in ('1', '2'):
        b = f'{{{{K0::diagnostics.{s}.p{p}.'
        s26.append(row([SETD[s], f'p{p}', b + 'refill_share_8}}', b + 'refill_gate}}',
                        b + 'overlap_with_ret_4}}; ' + b + 'overlap_with_ret_8}}',
                        b + 'mean_cos_ret_8}}, ' + b + 'mean_cos_perm_8}}, ' + b + 'mean_cos_rand_d0_8}}']))
s26.append('')
s26.append('Images with π_1(q) = π_2(q): ' + '; '.join(
    f'{SETD[s]} {{{{K0::diagnostics.{s}.same_donor_p1_p2}}}}' for s in ('ov_dev_a', 'ov_dev_b', 'xm_dev500')) + '.')
s26.append('')
s26.append(segs(394)[0])

SUP = '\n\n'.join([sup_head] + sup + ['\n'.join(s20), '\n'.join(s21), '\n'.join(s22), '\n'.join(s23), '\n'.join(s24),
                                      '\n'.join(s25), '\n'.join(s26)])
SUP = check_closed(SUP, 'supplement')
F[SU] = F[SU].rstrip('\n') + '\n\n' + SUP + '\n'
BLOCKS.append(('P6', 'A (S20, S26) + B (S21-S25)', '257-260, 269-283, 303, 318-321, 328-345, 378-394, 445', SU, SUP))

# ================================================================= Phase-A pass (coordinator rule of 2026-11-12)
for fn in [k for k in F if k.endswith('.md')]:
    F[fn] = fill_phase_a(F[fn], fn)
k0 = J['K0']['diagnostics']
assert all(k0[s][p]['refill_gate'] == 'pass' and k0[s][p]['refill_share_8'] <= 0.10
           for s in ('ov_dev_a', 'ov_dev_b', 'xm_dev500') for p in ('p1', 'p2'))      # S26 sentence checked at keys
assert all(len(g(f'S10B_{m}', 'failing_ids')) == g(f'S10B_{m}', 'n') - g(f'S10B_{m}', 'identical') for m in M)

# ================================================================= Ruling A: note on every `fix` row (grep of HEAD)
DAG = '†'
FIXNOTE = DAG + ' ' + RULING_A_NOTE
FIXROWS = []


def is_fix_cell(c):
    c = c.strip()
    return c in ('`fix`', '`ret` − `fix`') or bool(re.fullmatch(r'`?[\w.]+-fix-[\w-]+`?', c))


for fn in ('06_results.md', SU):
    lines = F[fn].split('\n')
    out, i = [], 0
    attr_start = next(j for j, x in enumerate(lines) if x.startswith('### Attribution study (C-ATTR-DEV)')) \
        if fn == SU else len(lines)
    attr_610 = next(j for j, x in enumerate(lines) if x.startswith('### 6.10 Attribution')) if fn == '06_results.md' \
        else len(lines)
    stop = min(attr_start, attr_610)
    caption = ''
    while i < len(lines):
        if lines[i].startswith('**Table'):
            caption = re.match(r'\*\*(Table [^.]*)', lines[i]).group(1)
        if i < stop and lines[i].startswith('|'):
            j = i
            block, hit = [], False
            while j < len(lines) and lines[j].startswith('|'):
                cells = lines[j].split('|')
                new = [c.rstrip() + ' ' + DAG + ' ' if is_fix_cell(c) else c for c in cells]
                if new != cells:
                    hit = True
                    FIXROWS.append((fn, caption, lines[j].split('|')[1].strip()[:60]))
                block.append('|'.join(new).replace(' ' + DAG + '  |', ' ' + DAG + ' |'))
                j += 1
            out += block
            if hit:
                out += ['', FIXNOTE]
            i = j
        else:
            out.append(lines[i])
            i += 1
    F[fn] = '\n'.join(out)
assert len(FIXROWS) > 0
# fail-closed sweep (Ruling A4): every table line of the paper sections that names a `fix` arm is marked or excluded
FIX_EXCL = ('| `fix` | one set of k clusters', '| `ret`, `rand`, `fix`, `zs` |')   # definitions (3.2 table, Box 1)
for fn in sorted(p.name for p in (PAPER / PD).glob('*.md') if re.match(r'(0\d|10|11)_', p.name)):
    text = F.get(fn) or head(fn)
    for mk in ('### Attribution study (C-ATTR-DEV)', '### 6.10 Attribution', '### 3.8 Arms', '### 5.7 The attr',
               '### 7.5 The attr'):
        text = text.split(mk)[0]
    for ln in text.split('\n'):
        if ln.startswith('|') and ('`fix`' in ln or '-fix-' in ln) and not ln.startswith(FIX_EXCL):
            assert DAG in ln, f'unmarked fix row in {fn}: {ln[:80]}'
NFIXNOTES = sum(F[fn].count('\n' + FIXNOTE + '\n') for fn in ('06_results.md', SU))

# ================================================================= bib (TG6) and audit
BIB_ADD = '''
@article{Holm1979,
  author    = {Holm, Sture},
  title     = {A Simple Sequentially Rejective Multiple Test Procedure},
  journal   = {Scandinavian Journal of Statistics},
  year      = {1979},
  volume    = {6},
  pages     = {65--70},
  doi       = {10.2307/4615733}
}
@article{Sattolo1986,
  author    = {Sattolo, Sandra},
  title     = {An algorithm to generate a random cyclic permutation},
  journal   = {Information Processing Letters},
  year      = {1986},
  volume    = {22},
  number    = {6},
  pages     = {315--317},
  doi       = {10.1016/0020-0190(86)90073-6}
}

@article{Schuirmann1987,
  author    = {Schuirmann, Donald J.},
  title     = {A comparison of the Two One-Sided Tests Procedure and the Power Approach for assessing the equivalence of average bioavailability},
  journal   = {Journal of Pharmacokinetics and Biopharmaceutics},
  year      = {1987},
  volume    = {15},
  number    = {6},
  pages     = {657--680},
  doi       = {10.1007/BF01068419}
}
'''
assert '@article{Sattolo1986' not in F['paperC.bib'] and '@article{Schuirmann1987' not in F['paperC.bib']
assert '@article{Holm1979' not in F['paperC.bib']
for key in ('Li2025UnveilingICL', 'Ramos2023LMCap', 'Bazi2025RAGCap'):
    assert '{' + key + ',' in F['paperC.bib'], key
F['paperC.bib'] = F['paperC.bib'].rstrip('\n') + '\n' + BIB_ADD
AUDIT = [
    'Sattolo1986\tdoi:10.1016/0020-0190(86)90073-6\thttps://api.crossref.org/works/10.1016/0020-0190(86)90073-6\t200\t'
    'OK (2026-11-12; C-ATTR transfer, TG6; IPL 22(6) 315-317, Sandra Sattolo)',
    'Schuirmann1987\tdoi:10.1007/BF01068419\thttps://api.crossref.org/works/10.1007/BF01068419\t200\t'
    'OK (2026-11-12; C-ATTR transfer, TG6; J Pharmacokinet Biopharm 15(6) 657-680)',
    'Li2025UnveilingICL\tdoi:10.1109/TPAMI.2026.3719106\thttps://api.crossref.org/works/10.1109/TPAMI.2026.3719106 ; '
    'https://arxiv.org/html/2507.08021\t200\tOK (2026-11-12; TPAMI 48(11) 14759-14776 on Crossref; "short-cut" copying '
    'finding seen in the arXiv text: Finding 5 "Similarity-Based Retrieval Induces Shortcut-Driven CIDEr Inflation")',
    'Holm1979\tdoi:10.2307/4615733\thttps://api.openalex.org/works?filter=title.search:simple%20sequentially%20rejective'
    '%20multiple%20test%20procedure\t200\tOK (2026-11-12; OpenAlex W2121044470: Sture Holm, Scandinavian Journal of '
    'Statistics 6, 65-70, 1979, doi 10.2307/4615733; issue not in the record, so no number field; JSTOR stable page did '
    'not load and Crossref api/works/10.2307/4615733 returned 404)',
]
F['paperC_bib_audit.tsv'] = F['paperC_bib_audit.tsv'].rstrip('\n') + '\n' + '\n'.join(AUDIT) + '\n'

# ================================================================= manifest rows (append only)
MAN = []
for f in FILLS:
    if f['kind'] in ('number', 'count'):
        MAN.append('\t'.join([f['printed'], f"{f['file']}::{f['key']}", repr(f['raw']), f['sha12'],
                              'keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-363)', f['used_in'].split()[0]]))
    else:
        MAN.append('\t'.join([f['printed'], f"{f['file']}::{f['key']}", repr(f['raw']), f['sha12'],
                              'label (DEVELOPMENT / C-ATTR-DEV; CC-363)', f['used_in'].split()[0]]))
MAN.append('\t'.join([BAT, 'manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_SCORING_RUN_DOC_v1_1.md::§1 step 5', repr(BAT),
                      sha(RUN / 'manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_SCORING_RUN_DOC_v1_1.md')[:12],
                      'label source (CC-363 W1; not in COPYBOUND_xm_dev500_aya_vision_8b.json)',
                      '06_results.md,11_supplement_registered_rows.md']))
F['number_manifest_C.tsv'] = F['number_manifest_C.tsv'].rstrip('\n') + '\n' + '\n'.join(MAN) + '\n'

# ================================================================= self-checks on the paper text
PAPER_MD = [k for k in F if k.endswith('.md')]
ALL = '\n'.join(F[k] for k in PAPER_MD)
NEWTXT = '\n'.join(b[4] for b in BLOCKS)
for s in (SPLIT, REDEC, B1, BAT):
    assert s in NEWTXT, s
assert pl(174).split('"')[1] in NEWTXT                                          # V1 K1 sentence
for s in ('re-implementation of the LMCap recipe by this study; not the authors\' code (no licence); not a statement '
          'about the published numbers', 'image-caption-pair prompt format, as used by RAGCap; not RAGCap'):
    assert s in NEWTXT, s
assert NEWTXT.count(': PASS.') == 2 and 'FAIL: the claim nominated' not in S610   # TG3 (5.7 holds the rule text)
assert NEWTXT.count('"FAIL: the claim nominated on OV-dev-A did not hold on OV-dev-B"') == 1
assert NEWTXT.count('values are for m = 1') == 3
for bad in ('OPS-', 'CC-3', 'RAGCap-style', 'no effect', 'HC2', 'ckey', 'ATTR_H1', 'C-DIAG'):
    assert bad not in NEWTXT, bad
assert not re.search(r'([0-9]{1,3}\.){3}[0-9]{1,3}', NEWTXT)
assert not re.search(r'\battribution (test|tests)\b|\btest of the (attribution|method)\b', NEWTXT)
assert F['06_results.md'].count('### 6.11 Compute') == 1 and '### 6.10 Compute' not in F['06_results.md']
for k in ('00_abstract.md', '01_introduction.md', '10_conclusion.md'):
    assert head(k) == (PAPER / PD / k).read_text(encoding='utf-8'), k   # TG7: untouched

# ================================================================= write working tree + note parts
for k, v in F.items():
    (PAPER / PD / k).write_text(v, encoding='utf-8')

OUT.mkdir(parents=True, exist_ok=True)
parts = ['## Block map (package lines -> paper file:lines)', '',
         '| block | phase | package lines | paper file:lines |', '|---|---|---|---|']
for bid, ph, pls, fn, txt in BLOCKS:
    t = F[fn]
    pos = t.find(txt.split('\n')[0])
    first = t[:pos].count('\n') + 1
    last = first + txt.count('\n')
    parts.append(f'| {bid} | {ph} | {pls} | {PD}/{fn}:{first}-{last} |')
SUBMAP = [  # finer map for the phase gates: (id, phase, package lines, file, start marker, end marker or None)
    ('6.10 box + 6.10.1 (first part)', 'A', '199-203', '06_results.md', '### 6.10 Attribution', '**6.10.1 What ran.**'),
    ('6.10.1 incl. last sentence (Scoring followed ... parity gate passed)', 'A; last sentence B', '203',
     '06_results.md', '**6.10.1 What ran.**', '#### 6.10.2'),
    ('6.10.2', 'A', '170-182', '06_results.md', '#### 6.10.2', '#### 6.10.3'),
    ('6.10.3 Table 15, N+ opening, Table 16, PASS, row sentences, DF', 'B', '209-253, 336', '06_results.md',
     '#### 6.10.3', '#### 6.10.4'),
    ('6.10.4', 'B', '265', '06_results.md', '#### 6.10.4', '#### 6.10.5'),
    ('6.10.5 (+ CC-363 Ruling 3, Ruling A sentence)', 'B', '286-290', '06_results.md', '#### 6.10.5', '#### 6.10.6'),
    ('6.10.6 Table 17, copy sentences, swap', 'B', '295-314, 349-350', '06_results.md', '#### 6.10.6', '#### 6.10.7'),
    ('6.10.7', 'B', '324', '06_results.md', '#### 6.10.7', '### 6.11 Compute'),
    ('6.11 Compute (+ sentence)', 'A', '374', '06_results.md', '### 6.11 Compute', None),
    ('5.7 Order of looks paragraph', 'B', '160', '05_preregistration_and_analysis.md', '**Order of looks.**',
     '**Budget.**'),
    ('Supplement header + N4 labels', 'A (N4 = B)', '445', SU, '### Attribution study (C-ATTR-DEV)', '**Table S20.'),
    ('Table S20', 'A (verdict cells from NOM)', '378-384', SU, '**Table S20.', '**Table S21.'),
    ('Table S21', 'B', '257-261', SU, '**Table S21.', '**Table S22.'),
    ('Table S22', 'B', '318-322', SU, '**Table S22.', '**Table S23.'),
    ('Table S23 (a, b)', 'B', '269-283', SU, '**Table S23.', '**Table S24.'),
    ('Table S24', 'B', '303', SU, '**Table S24.', '**Table S25 (a).'),
    ('Table S25 (a, b) + N3 note', 'B', '328-345', SU, '**Table S25 (a).', '**Table S26.'),
    ('Table S26 + sentence', 'A', '388-394', SU, '**Table S26.', None),
]
parts += ['', '## Finer block map (phase gate per subsection / table)', '',
          '| block | phase | package lines | paper file:lines |', '|---|---|---|---|']
for bid, ph, pls, fn, a, b in SUBMAP:
    lines = F[fn].split('\n')
    s = next(i for i, x in enumerate(lines) if x.startswith(a))
    e = next(i for i in range(s + 1, len(lines)) if lines[i].startswith(b)) - 1 if b else len(lines) - 1
    while not lines[e].strip():
        e -= 1
    parts.append(f'| {bid} | {ph} | {pls} | {PD}/{fn}:{s + 1}-{e + 1} |')
from collections import Counter
cnt = Counter((fn, cap or '(no caption)') for fn, cap, _ in FIXROWS)
parts += ['', f'## Ruling A: {len(FIXROWS)} table rows or headers marked {DAG}; {NFIXNOTES} note lines', '',
          '| file | table | marked rows |', '|---|---|---|']
parts += [f'| {fn} | {cap} | {n} |' for (fn, cap), n in cnt.items()]
parts += ['', 'Excluded as definitions (not result rows): 03_method.md arm table row `fix`; Box 1 row `ret`, `rand`, '
          '`fix`, `zs`. The script asserts that no other table line with `fix` / `-fix-` in 0*/10/11 files is unmarked.']
OPEN = sorted(set(OPEN_RE.findall(ALL)) | set(re.findall(r'\{\{[^}]+\}\}', ALL)))
assert '6.10.8' not in ALL, 'TG8: dangling 6.10.8'
parts += ['', '## Phase-A sources opened (each verified before use)', '', '| file | sha256 | verified by |',
          '|---|---|---|'] + [f'| `{r}` | {h} | {how} |' for r, h, how in SRCLOG]
parts += ['', '## TG8 cuts (deviations from TG1 for the judge; no claim added)', ''] + \
         [f'- {w}: {what}' for w, what in TG8_CUTS]
left = sorted(set(re.findall(r'\{\{[^}]+\}\}', ALL)))
parts += ['', f'## Tokens left unfilled: {len(left)}', ''] + [f'- `{o}`' for o in left]
(OUT / 'parts.md').write_text('\n'.join(parts) + '\n', encoding='utf-8')
(OUT / 'fills.json').write_text(json.dumps(FILLS, ensure_ascii=False, indent=0), encoding='utf-8')
print('blocks', len(BLOCKS), 'fills', len(FILLS), 'numeric', sum(f['kind'] in ('number', 'count') for f in FILLS),
      'fixrows', len(FIXROWS), 'open', len(set(re.findall(r'\{\{[^}]+\}\}', ALL))))
