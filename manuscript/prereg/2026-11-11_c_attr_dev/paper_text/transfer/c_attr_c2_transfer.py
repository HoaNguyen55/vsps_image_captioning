#!/usr/bin/env python3
"""C-ATTR-DEV shell C2 (T-K7, the freeze) -> Paper C paper repo WORKING TREE. PREPARED BEFORE K7; it refuses
to write until the K7 line exists.

Source of every sentence: section 4 of the committed package C_ATTR_B3_PAPER_TEXT_v1.md (CC-378 ruling 7).
Applies C2-a (block-4 paragraph appended to 6.10.9, and the B2 sentence in its full form with "or before the
freeze"), C2-b (05 Budget: "ends" -> "ended"), C2-c (07 Block order), C1-b (03 "Other registered arms": it
enters only with shell C2) and one manifest row for the K7 LOG line (same form as the C1 row).

K7 LINE (written by the coordinator at or after 2026-11-16T05:00:00Z, stamp from date -u; the text below with
only <utc> and <id> filled; a line that differs gives no sentence and goes to a judge):
<utc> OPS-<id>-c-k7: DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY. K7 freeze (v1.1 §10.1, 2026-11-16 12:00 VN = 2026-11-16T05:00:00Z; CC-378 ruling 7): every unfinished step is NOT RUN. Block 4 (English, Flickr30K val): steps 4.1, 4.2, 4.3, 4.4 and 4.5, including the memory swap of §7.9, NOT RUN (no block-4 host, package, read or decode exists); K6 has no cell to build: swap NOT RUN. Block 2 NOT RUN since its cut-off (OPS-1114ap-c-b2-cutoff). The NOT RUN items of CC-363 ruling 2 (rule L on the four swap cells, the English copy bound, the blind companion for Aya-Vision-8B) stay NOT RUN. Blocks 1, 1b and 3 ended (CC-363, CC-378).

Fail-closed gates before any write (CC-402 W1-W4, N2-N4): the package pin; the shell C1 commit 6a5d36a is an
ancestor of HEAD, 6.10.9 exists and the five files equal HEAD; exactly one K7 LOG line, with a well-formed
stamp at or after 2026-11-16T05:00:00Z and not in the future, equal as a string to the template above; every
literal below is the package's wording. Each OLD occurs exactly once before and each NEW exactly once after.
Two manifest rows are added: one for the K7 line, and one for the number 40 of the block-4 paragraph, keyed
to the registered text v1.1 (8,190 already has a row that names 06_results.md). Reads no ledger, list,
caption or test-set file. Never runs git add / commit.
Usage: python3 -I c_attr_c2_transfer.py
"""
import hashlib
import re
import subprocess
import time
from pathlib import Path

RUN = Path('/mnt/d/vsps_image_captioning')
PAPER = Path('/mnt/d/vsps_papers/vsps-paperC-tallip')
PD = PAPER / 'paper_v1_analysis'
PKG = RUN / 'manuscript/prereg/2026-11-11_c_attr_dev/paper_text/C_ATTR_B3_PAPER_TEXT_v1.md'
LOG = RUN / '.session_backup/2026-10-13/decisions/LOG.md'
PKG_SHA = 'e3820d3bf93f4246913c6eb651373965303d4afb31fc51fc3db48687ab2904f6'
K7_NOT_BEFORE = '2026-11-16T05:00:00Z'
C1_COMMIT = '6a5d36a'
PREREG = RUN / 'manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_DEV_PREREG_v1_1.md'
PREREG_SHA12 = '44f81329d418'
K7_FACT = 'steps 4.1, 4.2, 4.3, 4.4 and 4.5, including the memory swap of §7.9, NOT RUN'
FORTY_QUOTE = '40 hold only KTVIC images'
FILES = ['06_results.md', '05_preregistration_and_analysis.md', '07_disclosures.md', '03_method.md',
         'number_manifest_C.tsv']

B2_OLD = 'was not run by its registered cut-off (2026-11-14 18:00, UTC+7); the secondary family S-BB is empty.'
B2_NEW = ('was not run by its registered cut-off (2026-11-14 18:00, UTC+7) or before the freeze; '
          'the secondary family S-BB is empty.')
C2A_ANCHOR = 'Block 3 ran (Section 6.10.8).'
C2B_OLD = 'A freeze at 2026-11-16 12:00 (UTC+7) ends every step not finished by then.'
C2B_NEW = 'A freeze at 2026-11-16 12:00 (UTC+7) ended every step not finished by then.'
C2C_ANCHOR = 'Block 2 was not run by its registered cut-off (Section 6.10.9).'
C2C_ADD = ' Block 4 was not run before the freeze (Section 6.10.9).'
C1B_ANCHOR = ('**Other registered arms.** The registration also names a memory swap on fixed English images and '
              'further backbones outside the Qwen language-model line.')
C1B_ADD = ' Section 6.10.9 states whether they ran.'


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git(*a: str) -> str:
    return subprocess.run(['git', '-C', str(PAPER), *a], capture_output=True, check=True).stdout.decode()


def k7_template() -> str:
    """The K7 line of this file's docstring (the one line that starts with '<utc> OPS-<id>-c-k7:')."""
    return next(ln for ln in __doc__.splitlines() if ln.startswith('<utc> OPS-<id>-c-k7:'))


def k7_line() -> str:
    quoted = [ln for ln in LOG.read_text(encoding='utf-8').splitlines() if '-c-k7:' in ln]
    lines = [ln for ln in quoted if re.match(r'\S+ OPS-[0-9a-z]+-c-k7: ', ln)]
    assert len(lines) == 1 and len(quoted) == 1, f'exactly one K7 line is needed, found {len(lines)} ({len(quoted)} mentions): nothing written'
    utc, ident = lines[0].split(' ')[0], lines[0].split(' ')[1].removeprefix('OPS-').removesuffix('-c-k7:')
    assert re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ', utc), 'K7 stamp malformed'
    assert K7_NOT_BEFORE <= utc <= time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'K7 stamp before the freeze or in the future'
    assert K7_FACT in lines[0], 'K7 line does not list the block-4 steps as NOT RUN'
    assert lines[0] == k7_template().replace('<utc>', utc).replace('<id>', ident), 'K7 line differs from the template'
    return lines[0]


def c2a_text(pkg: str) -> str:
    """The quoted paragraph under 'C2-a' of the package."""
    lines = pkg.splitlines()
    i = next(k for k, ln in enumerate(lines) if ln.startswith('C2-a, 06 §6.10.9, appended'))
    start = next(k for k in range(i, len(lines)) if lines[k].startswith('>'))
    block = []
    for ln in lines[start:]:
        if not ln.startswith('>'):
            break
        block.append(ln[1:].removeprefix(' '))
    text = '\n'.join(block)
    assert text.startswith('Block 4 was not run before the freeze:') and '{{' not in text
    return text


def swap(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, f'OLD not exactly once: {old[:50]!r}'
    out = text.replace(old, new)
    assert out.count(new) == 1, f'NEW not exactly once: {new[:50]!r}'
    return out


def main() -> None:
    pkg_bytes = PKG.read_bytes()
    assert sha(pkg_bytes) == PKG_SHA, 'package pin'
    pkg = pkg_bytes.decode('utf-8')
    for s in ('or before the freeze; the secondary family S-BB is empty.', f'`{C2B_OLD}` → `{C2B_NEW}`',
              f'append `{C2C_ADD}`', f'append `{C1B_ADD}`'):
        assert s in pkg, f'not the package wording: {s}'
    assert git('status', '--porcelain', '--', *[f'paper_v1_analysis/{f}' for f in FILES]) == '', 'files differ from HEAD'
    git('merge-base', '--is-ancestor', C1_COMMIT, 'HEAD')  # raises unless the shell C1 commit is in the history
    read = {f: (PD / f).read_text(encoding='utf-8') for f in FILES}
    assert read[FILES[0]].count('#### 6.10.9 What did not run') == 1, 'shell C1 is not in the paper'
    line = k7_line()

    t06 = swap(read[FILES[0]], B2_OLD, B2_NEW)
    t06 = swap(t06, C2A_ANCHOR, C2A_ANCHOR + '\n\n' + c2a_text(pkg))
    t05 = swap(read[FILES[1]], C2B_OLD, C2B_NEW)
    t07 = swap(read[FILES[2]], C2C_ANCHOR, C2C_ANCHOR + C2C_ADD)
    t03 = swap(read[FILES[3]], C1B_ANCHOR, C1B_ANCHOR + C1B_ADD)
    utc, ident = line.split(' ')[0], line.split(' ')[1].rstrip(':')
    row = '\t'.join(['NOT RUN', f'decisions LOG::{ident}', f"'{K7_FACT}'", sha(line.encode('utf-8'))[:12],
                     f'FACT_RECORDED (LOG line {ident}, {utc}; CC-378 ruling 7; shell C2)', '06_results.md'])
    prereg = PREREG.read_bytes()
    assert sha(prereg).startswith(PREREG_SHA12) and FORTY_QUOTE in prereg.decode('utf-8'), 'registration v1.1 pin or quote'
    row40 = '\t'.join(['40', f'manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_DEV_PREREG_v1_1.md::§5 No Vietnamese '
                        f'memory swap ({FORTY_QUOTE})', f"'{FORTY_QUOTE}'", PREREG_SHA12, 'registered text (v1.1)',
                        '06_results.md'])
    manifest = read[FILES[4]]
    assert manifest.endswith('\n') and row not in manifest and row40 not in manifest
    print('paper HEAD', git('rev-parse', '--short', 'HEAD').strip())
    for name, text in zip(FILES, (t06, t05, t07, t03, manifest + row + '\n' + row40 + '\n')):
        (PD / name).write_text(text, encoding='utf-8')
        print(sha(text.encode('utf-8'))[:16], name)
    print('applied: C2-a (with the full B2 sentence), C2-b, C2-c, C1-b, manifest rows for the K7 line and for 40')


if __name__ == '__main__':
    main()
