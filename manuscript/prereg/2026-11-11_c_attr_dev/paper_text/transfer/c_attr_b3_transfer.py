#!/usr/bin/env python3
"""C-ATTR-DEV block 3 -> Paper C paper repo WORKING TREE (CC-380 ruling 15 (3)).

Parses E1-E19, the fill map (section 5.1) and the 127 manifest rows (section 5) from the committed package itself;
starts every paper file from `git show HEAD:` (re-runs are idempotent); applies the rows in package order (each OLD
exactly once before, each filled NEW exactly once after); fills every {{...}} / [[...]] from the map; appends the
manifest rows with "W1 recompute pending" -> "W1 recompute PASS" (ruling 15 (3)); writes the paper files.
Before any write it checks, fail-closed: the package and CC-380 shas, the result sums (G1), the paper HEAD and the
HEAD blob shas (G2), and every manifest row against its source file (raw value, sha prefix, display), and that the
map displays equal the manifest's number column row by row. Reads no ledger, list, caption or test-set file.
Never runs git add / commit. Usage: python3 -I c_attr_b3_transfer.py
"""
import hashlib
import json
import re
import subprocess
from pathlib import Path

RUN = Path('/mnt/d/vsps_image_captioning')
PAPER = Path('/mnt/d/vsps_papers/vsps-paperC-tallip')
PD = 'paper_v1_analysis'
PKG = RUN / 'manuscript/prereg/2026-11-11_c_attr_dev/paper_text/C_ATTR_B3_PAPER_TEXT_v1.md'
CC380 = RUN / '.session_backup/2026-10-13/decisions/CC-380.txt'
B3 = RUN / 'data/results/c_attr_1113_b3score'
PAPER_HEAD = '44bbdd9979ea03d0d9c30c435a0246984022c561'
PINS = {PKG: 'e3820d3bf93f4246913c6eb651373965303d4afb31fc51fc3db48687ab2904f6',
        CC380: '60b7e074445a7ac0c6dfbef2f37a5bbd90a82972c0fe6043450d245aea9f7634',
        B3 / 'SHA256SUMS': 'd2500b48a906852247255617418620b28a7e862f6f0f81c4c815eb5dbed79dcd'}
HEAD_SHA8 = {'03_method.md': '50b0529c', '05_preregistration_and_analysis.md': '489c4b79', '06_results.md': '61be0e29',
             '07_disclosures.md': '8e58dc6d', '09_limitations.md': '349703a1',
             '11_supplement_registered_rows.md': '1223064f', 'number_manifest_C.tsv': '3eeb2dab',
             'paperC.bib': 'a415c4da', '00_abstract.md': '4c023726', '01_introduction.md': 'b731e637',
             '10_conclusion.md': '83d466df'}
MANIFEST = 'number_manifest_C.tsv'
HOUSE_HEADER = 'number\tfile::key\traw_value\tsha256_prefix\tstatus\tused_in'
FLOOR = 1 / 2001


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git(*a):
    return subprocess.run(['git', '-C', str(PAPER), *a], capture_output=True, check=True).stdout


def head(name):
    return git('show', f'HEAD:{PD}/{name}').decode('utf-8')


# ------------------------------------------------------------------ gates G1/G2 (fail closed)
for p, h in PINS.items():
    assert sha(p.read_bytes()) == h, f'pin {p}'
for ln in (B3 / 'SHA256SUMS').read_text().splitlines():
    h, rel = ln.split()
    assert sha((B3 / rel).read_bytes()) == h, f'G1 {rel}'
assert git('rev-parse', 'HEAD').decode().strip() == PAPER_HEAD, 'G2 paper HEAD'
for n, h8 in HEAD_SHA8.items():
    assert sha(head(n).encode('utf-8')).startswith(h8), f'G2 HEAD blob {n}'

PKGT = PKG.read_text(encoding='utf-8')


def section(start, end):
    a = PKGT.index(start)
    return PKGT[a:PKGT.index(end, a)]


# ------------------------------------------------------------------ parse E-rows (section 3 only)
S3 = section('\n## 3. Edit rows E1–E19 (c)\n', '\n## 4. Conditional shells (d)\n')
blocks = re.findall(r'<<<E(\d+) (\S+) (OLD|NEW)>>>\n(.*?)\n<<<END>>>', S3, re.S)
assert len(blocks) == 38, len(blocks)
ROWS = []
for i in range(0, 38, 2):
    (n1, f1, k1, old), (n2, f2, k2, new) = blocks[i], blocks[i + 1]
    assert (n1, f1, k1, k2) == (n2, f2, 'OLD', 'NEW') and int(n1) == i // 2 + 1, blocks[i][:3]
    ROWS.append((f'E{n1}', f1, old, new))

# ------------------------------------------------------------------ parse the fill map (section 5.1)
S51 = section('\n### 5.1 Placeholder → display (the fill map)\n', '\n## 6. Transfer gates (f)\n')
MAP_ROWS = re.findall(r'^\| `(.+)` \| (.+) \|$', S51, re.M)
assert len(MAP_ROWS) == 128, len(MAP_ROWS)
MAP, NONTOKEN = {}, []
for key, disp in MAP_ROWS:
    m = re.fullmatch(r'\{\{(.+)\}\}( \((table|sentence)\))?', key)
    if m:
        tok = m.group(1) + ('|s' if m.group(3) == 'sentence' else '')
    elif re.fullmatch(r'[A-Z0-9]+\.(d|lo|hi)', key):
        tok = key
    else:
        NONTOKEN.append((key, disp))
        continue
    assert tok not in MAP, tok
    MAP[tok] = disp

# ------------------------------------------------------------------ parse the manifest rows (section 5)
S5 = section('\n## 5. Manifest rows (e)\n', '\n### 5.1 ')
tsv = re.search(r'```tsv\n(.*?)\n```', S5, re.S).group(1).split('\n')
assert tsv[0] == HOUSE_HEADER, 'manifest header'
MROWS = [r.split('\t') for r in tsv[1:]]
assert len(MROWS) == 127 and all(len(r) == 6 for r in MROWS)
assert head(MANIFEST).split('\n', 1)[0] == HOUSE_HEADER, 'house columns'

# ------------------------------------------------------------------ verify every manifest row against its source


def fd(x):
    s = f'{x:.2f}'.replace('-', '−')
    return s if s.startswith('−') else '+' + s


def fb(x):
    s = f'{x:.2f}'
    return '0.00' if s == '-0.00' else s.replace('-', '−')


def pdisp(v):
    return f'{v:#.3g}'


def walk(o, key):
    for part in re.findall(r'[^.\[\]]+|\[\d+\]', key):
        o = o[int(part[1:-1])] if part.startswith('[') else o[part]
    return o


def tsv_rows(p):
    return [ln.split(' ') for ln in p.read_text().splitlines()]


def ssum(p):
    return sum(int(r[1]) for r in tsv_rows(p) if r[1] != 'start')


def status_lines(p, pat):
    return [ln for ln in p.read_text(encoding='utf-8').splitlines() if re.search(pat, ln)]


# registered literal rows: manifest key -> (string that must occur in the registered text, display, raw value)
REG_LIT = {'§6.5 heading (hard cap 5 GPU-h)': ('hard cap 5 GPU-h', '5', '5'),
           'V8 (block 3 cap)': ('min(12, 1.5 P3)', 'min(12, 1.5 P3)', 'min(12, 1.5 P3)'),
           '§7.13 OV-dev-B Qwen2.5-VL chance of DETECTED at a true +2.0':
               ('Chance of DETECTED: about 0.49 at a true +2.0', 'about 0.49', 'about 0.49'),
           '§7.13 OV-dev-B Qwen2.5-VL standard error':
               ('OV-dev-B, Qwen2.5-VL: standard error about 1.03', 'about 1.03', 'about 1.03'),
           '§7.13 NEGLIGIBLE needs |θ̂| below about 0.3': ('NEGLIGIBLE needs |θ̂| below about 0.3', 'about ±0.3', 'about 0.3'),
           '§2 D1 (first 50 OV-dev-B items per runner)': ('first 50 OV-dev-B items', '50', 50),
           '§2 lmcap_rand / lmcap_perm (K = 4)': ('K = 4', '4', 4),
           '§2 lmcap_rand (N = 3 shots)': ('N = 3 shot', '3', 3)}


def resolve(rel, key):
    """(value, expected display) for one manifest row; reads only the named key / status line / literal."""
    p = RUN / rel
    k = re.sub(r' \(.*\)$', '', key)          # drop the descriptive suffix "(...)"
    if rel.endswith('.json'):
        o = json.loads(p.read_text(encoding='utf-8'))
        if key.endswith(' / sesoi (2.0)'):
            v = walk(o, key.split(' / ')[0]) / 2.0
            return v, f'{v:.1f}'
        if k == 'steps':
            v = len(o['steps'])
            assert v == 10
            return v, 'ten'
        v = walk(o, k)
        if k.startswith('steps['):               # the named run id must be that step's
            assert key.split('(')[1].rstrip(')') in json.dumps(walk(o, k.rsplit('.', 1)[0])), key
        if k == 'not_run':
            assert v == []
            return v, 'no step NOT RUN'
        if k == 'env.packages_sha256':
            return v, v[:8] + '…'
        if isinstance(v, str):
            return v, v
        if k.endswith('.d'):
            return v, fd(v)
        if re.search(r'\.(lo|hi|lo90|hi90)$', k):
            return v, fb(v)
        if k.endswith('.p'):
            return v, (('at its floor (1/2,001)', '1/2,001, its floor') if abs(v - FLOOR) < 1e-12 else pdisp(v))
        if k in ('cap_h', 'P_h'):
            return v, f'{v:.2f}'
        if k.startswith('rates_L_r'):
            return v, f'{v:.2f}' if k.endswith('[1]') else f'{v:.1f}'
        if isinstance(v, int):
            return v, f'{v:,}'
        raise ValueError(f'no display rule for {rel}::{key}')
    if rel.endswith('gpu_seconds.tsv'):
        t1 = ssum(B3 / 'decode/gpu_seconds_try1.tsv')
        if key.startswith('line '):
            n = int(key.split()[1])
            name, v = tsv_rows(p)[n - 1]
            assert key.endswith(f'({name})')
            return int(v), f'{int(v):,}'
        if key == 'sum of non-start rows':
            return ssum(p), f'{ssum(p):,}'
        if key == 'sum of non-start rows + gpu_seconds_try1.tsv sum':
            return ssum(p) + t1, f'{ssum(p) + t1:,}'
        if key == '(sum of non-start rows + gpu_seconds_try1.tsv sum) / 3600':
            v = (ssum(p) + t1) / 3600
            return v, f'{v:.2f}'
    if rel.endswith('gpu_seconds_try1.tsv'):
        if key == 'sum of non-start rows':
            return ssum(p), f'{ssum(p):,}'
        if key == 'sum of non-start rows / 3600':
            return ssum(p) / 3600, f'{ssum(p) / 3600:.2f}'
    if rel.endswith('job.log'):
        if key == 'line "JOB DONE gpu_h"':
            (ln,) = status_lines(p, r' JOB DONE gpu_h ')
            v = ln.rsplit(' ', 1)[1]
            return v, v
        if key == 'lines " OK B3_" (count)':
            v = len(status_lines(p, r' OK B3_'))
            return v, str(v)
        if key == 'lines "CAP STOP" or "JOB STOP" (count)':
            v = len(status_lines(p, r'CAP STOP|JOB STOP'))
            return v, ('no cap stop, no job stop' if v == 0 else str(v))
    if rel.endswith('mutants.log'):
        a, b = p.read_text(encoding='utf-8').splitlines()[-2:]
        assert b == 'rc 0' and key == f'line "{a}"'
        m = re.fullmatch(r'(\d+)/(\d+) killed; survived: none', a)
        return a, f'{m.group(1)} of {m.group(2)}'
    if rel.endswith('.md'):                    # registered literal: must occur in the registered text
        txt = p.read_text(encoding='utf-8')
        if key == '§9 item 4 model.safetensors sha256':
            v = re.search(r'\b([0-9a-f]{64})\b', txt[txt.index('model.safetensors'):]).group(1)
            return v, v[:8] + '…'
        lit, disp, raw = REG_LIT[key]
        assert lit in txt, lit
        return raw, disp
    raise ValueError(f'no resolver for {rel}::{key}')


VER = []
for num, fk, raw, pre, status, used in MROWS:
    rel, key = fk.split('::', 1)
    assert sha((RUN / rel).read_bytes()).startswith(pre) and len(pre) == 12, f'sha prefix {fk}'
    v, disp = resolve(rel, key)
    assert raw == repr(v), f'raw {fk}: {raw!r} vs {v!r}'
    assert num in (disp if isinstance(disp, tuple) else (disp,)), f'display {fk}: {num!r} vs {disp!r}'
    VER.append(fk)
assert len(VER) == 127

# map display column == manifest number column, row by row (the map's extra "ten (05 E5, S27)" entry dropped)
mdisp = [d for k, d in MAP_ROWS if k != 'ten (05 E5, S27)']
assert mdisp == [r[0] for r in MROWS], 'map vs manifest order/value'

# ------------------------------------------------------------------ apply E1-E19 with filled NEW strings
USED = {}


def fill(text):
    text = re.sub(r'\[\[([A-Z0-9]+)\|90\]\]',
                  r'{{\1.d}} [{{\1.lo}}, {{\1.hi}}] (90% interval [{{\1.lo90}}, {{\1.hi90}}])', text)
    text = re.sub(r'\[\[([A-Z0-9]+)\]\]', r'{{\1.d}} [{{\1.lo}}, {{\1.hi}}]', text)

    def sub(mo):
        tok = mo.group(1)
        assert tok in MAP, f'unfilled placeholder {tok}'
        USED[tok] = USED.get(tok, 0) + 1
        return MAP[tok]
    text = re.sub(r'\{\{(.+?)\}\}', sub, text)
    assert '{{' not in text and '}}' not in text and '[[' not in text and ']]' not in text
    return text


files = {}
applied = []
for rid, fname, old, new in ROWS:
    t = files.setdefault(fname, head(fname))
    assert t.count(old) == 1, f'{rid}: OLD count {t.count(old)}'
    nf = fill(new)
    t = t.replace(old, nf)
    assert t.count(nf) == 1, f'{rid}: NEW count {t.count(nf)}'
    files[fname] = t
    applied.append((rid, fname))

man = head(MANIFEST)
assert man.endswith('\n')
pend = sum(r[4].count('W1 recompute pending') for r in MROWS)
add = ['\t'.join(r[:4] + [r[4].replace('W1 recompute pending', 'W1 recompute PASS')] + r[5:]) for r in MROWS]
assert sum(a.count('W1 recompute PASS') for a in add) == pend and not any('pending' in a for a in add)
files[MANIFEST] = man + '\n'.join(add) + '\n'

# ------------------------------------------------------------------ write the working tree and report
for fname, t in files.items():
    (PAPER / PD / fname).write_bytes(t.encode('utf-8'))
    print(f'{fname}\tbefore {sha(head(fname).encode())}\tafter {sha(t.encode())}')
print('rows applied:', ' '.join(f'{r}:{f}' for r, f in applied))
print(f'placeholders filled: {sum(USED.values())} occurrences, {len(USED)} distinct tokens; '
      f'map entries {len(MAP_ROWS)} ({len(MAP)} tokens, {len(NONTOKEN)} non-token)')
print('map tokens not used by E1-E19:', sorted(set(MAP) - set(USED)))
print('non-token map entries:', [k for k, _ in NONTOKEN])
print(f'manifest rows appended: {len(add)}; verified against source: {len(VER)}; '
      f'"W1 recompute pending" -> "W1 recompute PASS": {pend}')
