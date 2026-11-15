#!/usr/bin/env python3
"""C-ATTR-DEV shell C1 (T-CUT, the block-2 cut-off) -> Paper C paper repo WORKING TREE.

Source of every sentence: section 4 of the committed package C_ATTR_B3_PAPER_TEXT_v1.md (CC-378 ruling 7).
Applies C1-a (new subsection 6.10.9), C1-c, C1-d and C1-e, plus the 6.10.1 heading fix noted at the tex
rebuild (OPS-1114k). C1-b is NOT applied: the package lets it enter only together with shell C2.

Fail-closed gates before any write: the package pin; the paper HEAD and the four files equal to HEAD; exactly
one cut-off LOG line, stamped at or after 2026-11-14T11:00:00Z, equal as a string to the CC-378 template with
only <utc> and <id> filled; the Aya-Vision-8B label DETECTED in the result file and in the manifest row whose
status says "shell C1 only". Each OLD occurs exactly once before and each NEW exactly once after.
Reads no ledger, list, caption or test-set file. Never runs git add / commit.
Usage: python3 -I c_attr_c1_transfer.py
"""
import hashlib
import json
import subprocess
from pathlib import Path

RUN = Path('/mnt/d/vsps_image_captioning')
PAPER = Path('/mnt/d/vsps_papers/vsps-paperC-tallip')
PD = PAPER / 'paper_v1_analysis'
PKG = RUN / 'manuscript/prereg/2026-11-11_c_attr_dev/paper_text/C_ATTR_B3_PAPER_TEXT_v1.md'
DEC = RUN / '.session_backup/2026-10-13/decisions'
VERDICT = RUN / 'data/results/c_attr_1112_score/res/VERDICT.json'
PKG_SHA = 'e3820d3bf93f4246913c6eb651373965303d4afb31fc51fc3db48687ab2904f6'
PAPER_HEAD = 'd558df0'
CUTOFF_NOT_BEFORE = '2026-11-14T11:00:00Z'
FILES = ['06_results.md', '05_preregistration_and_analysis.md', '07_disclosures.md', 'number_manifest_C.tsv']
AYA_KEY = 'data/results/c_attr_1112_score/res/VERDICT.json::sets.ov_dev_b.rows.aya_vision_8b|tau_sel.label'
PLACEHOLDER = '{{VER1B::sets.ov_dev_b.rows.aya_vision_8b~tau_sel.label}}'


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git(*a: str) -> str:
    return subprocess.run(['git', '-C', str(PAPER), *a], capture_output=True, check=True).stdout.decode()


def cutoff_line() -> str:
    """The one LOG line of the cut-off, checked against the template of CC-378 ruling 7."""
    cc = (DEC / 'CC-378.txt').read_text(encoding='utf-8').splitlines()
    i = next(k for k, ln in enumerate(cc) if ln.strip().startswith('"<utc> OPS-<id>-c-b2-cutoff:'))
    j = next(k for k in range(i + 1, len(cc)) if cc[k].rstrip().endswith('"'))
    template = ' '.join(ln.strip() for ln in cc[i:j + 1])[1:-1]
    lines = [ln for ln in (DEC / 'LOG.md').read_text(encoding='utf-8').splitlines() if '-c-b2-cutoff:' in ln]
    assert len(lines) == 1, 'exactly one cut-off line'
    utc, ident = lines[0].split(' ')[0], lines[0].split(' ')[1].removeprefix('OPS-').removesuffix('-c-b2-cutoff:')
    assert utc >= CUTOFF_NOT_BEFORE, 'cut-off line stamped too early'
    assert lines[0] == template.replace('<utc>', utc).replace('<id>', ident), 'cut-off line differs from the template'
    return lines[0]


def c1a_text(pkg: str) -> str:
    """The quoted block under 'C1-a' of the package, with its one placeholder filled."""
    lines = pkg.splitlines()
    i = next(k for k, ln in enumerate(lines) if ln.startswith('C1-a, 06, new subsection'))
    start = next(k for k in range(i, len(lines)) if lines[k].startswith('>'))
    block = []
    for ln in lines[start:]:
        if not ln.startswith('>'):
            break
        block.append(ln[1:].removeprefix(' '))
    text = '\n'.join(block)
    assert text.count(PLACEHOLDER) == 1 and text.startswith('#### 6.10.9 What did not run')
    return text.replace(PLACEHOLDER, 'DETECTED')


def swap(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, f'OLD not exactly once: {old[:50]!r}'
    out = text.replace(old, new)
    assert out.count(new) == 1, f'NEW not exactly once: {new[:50]!r}'
    return out


def main() -> None:
    pkg_bytes = PKG.read_bytes()
    assert sha(pkg_bytes) == PKG_SHA, 'package pin'
    pkg = pkg_bytes.decode('utf-8')
    assert git('rev-parse', '--short', 'HEAD').strip() == PAPER_HEAD, 'paper HEAD'
    assert git('status', '--porcelain', '--', *[f'paper_v1_analysis/{f}' for f in FILES]) == '', 'files differ from HEAD'
    line = cutoff_line()
    label = json.loads(VERDICT.read_text(encoding='utf-8'))['sets']['ov_dev_b']['rows']['aya_vision_8b|tau_sel']['label']
    assert label == 'DETECTED', 'Aya-Vision-8B label'
    manifest = (PD / FILES[3]).read_text(encoding='utf-8')
    c1_rows = [r for r in manifest.splitlines() if 'shell C1 only' in r]
    assert len(c1_rows) == 1 and c1_rows[0].split('\t')[:2] == ['DETECTED', AYA_KEY], 'manifest row of the Aya label'

    c1c_old, c1c_new = '(S-BB)', '(S-BB; Section 6.10.9)'
    c1d = ' Block 2 was not run by its registered cut-off (Section 6.10.9).'
    c1d_old = 'the positive control first (Sections 3.8 and 5.7).'
    for s in (f'`{c1c_old}` → `{c1c_new}`', f'append `{c1d}`'):
        assert s in pkg, f'not the package wording: {s}'

    t06 = (PD / FILES[0]).read_text(encoding='utf-8')
    t06 = swap(t06, '### 6.11 Compute', c1a_text(pkg) + '\n\n### 6.11 Compute')
    t06 = swap(t06, '**6.10.1 What ran.** ', '#### 6.10.1 What ran\n\n')
    t05 = swap((PD / FILES[1]).read_text(encoding='utf-8'), c1c_old, c1c_new)
    t07 = swap((PD / FILES[2]).read_text(encoding='utf-8'), c1d_old, c1d_old + c1d)
    utc, ident = line.split(' ')[0], line.split(' ')[1].rstrip(':')
    row = '\t'.join(['one', f'decisions LOG::{ident}', "'non-Qwen backbones with tau_sel DETECTED on OV-dev-B: 1'",
                     sha(line.encode('utf-8'))[:12],
                     f'FACT_RECORDED (LOG line {ident}, {utc}); the count is derived from the Aya-Vision-8B label '
                     'row and this line (CC-378 ruling 7; shell C1)', '06_results.md'])
    assert manifest.endswith('\n') and row not in manifest
    for name, text in zip(FILES, (t06, t05, t07, manifest + row + '\n')):
        (PD / name).write_text(text, encoding='utf-8')
        print(sha(text.encode('utf-8'))[:16], name)
    print('applied: C1-a, C1-c, C1-d, C1-e, heading 6.10.1; not applied: C1-b (waits for shell C2)')


if __name__ == '__main__':
    main()
