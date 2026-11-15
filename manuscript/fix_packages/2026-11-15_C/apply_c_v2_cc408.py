#!/usr/bin/env python3
"""Paper C fix package v2 AS RULED IN CC-408, REVISED version (CONDITIONAL GO 88): check, or write to the paper repo
WORKING TREE. The ruling file is pinned at its revised text (ae06c9f5...); its first version (f871f1ee...) is void.

Default mode (no argument) writes nothing: it builds the after-C2 tree in memory (every file from `git show
9b8e6ae:`, the freeze transfer's own swap calls, its two manifest rows with a dummy stamp and id), runs the same
gate and the same build as the write mode, and prints per file whether the result equals the target of CC-408
Ruling 9. `--write --ruling CC-408` does the same on the real tree and writes only if every file equals its
target and the manifest meets the byte rule of Ruling 9. Never runs git add / commit.

What is built: the 12 blocks of C_FIX_PACKAGE_v2.md in package order, with the texts of CC-408 Annex A for
C-V04 (NEW; W1), C-V05a (one sentence of NEW; N1) and C-V08 (OLD and NEW; N2), read byte for byte from the
ruling file; then C-R01 and C-M01. The build function, the gate on the ten section files and every content
check are those of apply_c_v2.py, imported as a module (its main() is not run; its own PKG_SHA and TARGET are
void under CC-408 and are not used). Added here: file 07 must be the C2 commit's (Ruling 6 iv); the row for 40
must be the C2 row (Ruling 6 v); manifest lines 71 and 73 must be the strings of Ruling 9; the manifest lines
before the two C2 rows must have the sha256 of Ruling 9.
Usage: python3 -I apply_c_v2_cc408.py            (check, in memory)
       python3 -I apply_c_v2_cc408.py --write --ruling CC-408
"""
import hashlib
import importlib.util
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
RUN = Path('/mnt/d/vsps_image_captioning')
R = Path('/mnt/d/vsps_papers/vsps-paperC-tallip')
PD = R / 'paper_v1_analysis'
HERE = RUN / 'manuscript/fix_packages/2026-11-15_C'
PKG = HERE / 'C_FIX_PACKAGE_v2.md'
MODULE = HERE / 'apply_c_v2.py'
RULING = RUN / '.session_backup/2026-10-13/decisions/CC-408.txt'
C2 = RUN / 'manuscript/prereg/2026-11-11_c_attr_dev/paper_text/transfer/c_attr_c2_transfer.py'
PINS = {
    PKG: '2653ec721b4442b450b973d813c085f23b2b116f47cfba9cc3b4e3e80dcea171',
    MODULE: '382c1735ec818cd2e6561da7b920fbb9e34ea50e882f6ce4da18b3d98afebc79',
    RULING: 'ae06c9f57edfb51fa561d190dd75562dee72dba3f7006bcf1e81d358879de3b5',  # revised 2026-11-15T00:51:58Z; the first version is void
    C2: '030c369d97f8668c7f82c8a05a046811e9d95da77272a63055f85f511e9da56c',
}
BASE = '9b8e6ae'
MANIFEST = 'number_manifest_C.tsv'
TARGET = {  # CC-408 (revised) Ruling 9, l.196-205
    '00_abstract.md': 'a4725e99fbd8883be97c991639020870a8bcdfa21f34483ddf5f5f18610cc51f',
    '01_introduction.md': 'ffc90b60351e639fbc05162807e44d8f4237a3935c33b3b2aefa6610cf35b952',
    '03_method.md': '5db109ab3b011cf658da599d5ef67636c7b282f378829abb3a35f176521da057',
    '04_data_and_splits.md': '58529b1dc3444b9a89830661a0a724e4ee3fc5ed8bb8acb9383639a70320c540',
    '05_preregistration_and_analysis.md': 'ea9094d34f05bd15dc69e5b5c9788355775cc2107f285a8a0f7c28c370a62b97',
    '06_results.md': '01d41de0ba50542b5a991353e7ff56f762f5ce36b33e8b732fa3d352530e60f6',
    '08_english_comparison.md': '69706e5f18ef88a5c9d9bdbcb8ad30607b565cd58043d50275a84f6e93a121f8',
    '09_limitations.md': 'c52b962c41460296aefd324c7f9a53b4b6f1c149026c17d08051d279c458745c',
    '11_supplement_registered_rows.md': '5a71a8a08085cdaabe385539208f008275aed18fabbd6c962cf0d0c5c44f0ff9',
    'V2_PROGRESS_C.md': 'eee308faacbd2f5f0902d65db79c34ad4ad3cfeb2954acbfaea1fe26b2c16689',
}
FILE07_AFTER_C2 = 'c91bcf318ff086c7eacadf9cebe7ae096d644a7cfeedb9585ef3a71adb300693'  # Ruling 6 (iv): c91bcf31
ROW40_SHA = '6b0d2217'  # Ruling 6 (v): sha256 of the row-40 line, without its line break
MAN_HEAD_SHA = 'bae5743928a30483d090f8abb6ee45aae78934d27c40a1122db688efe2c0f95f'  # Ruling 9, l.209-210
LINE71 = '\t'.join(['1997', '.session_backup/2026-10-26/c_test/CHAIN.log::c_ov_test     staged / distinct sha (\\d+) #0',
                    '1997.0', 'fc543266fcc6', 'keyed (restored under PI-1110n; CC-405)', '04_data_and_splits.md'])
LINE73 = '\t'.join(['1937', 'manuscript/prereg/2026-10-25_c_test/PREREG.md::§3.1 primary distinct images', '1937',
                    'acecd6527217', 'keyed (restored under PI-1110n; CC-405)', '04_data_and_splits.md'])


def sha(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ruled_package(A) -> str:
    """The text of package v2 with the three blocks of CC-408 Annex A put in, each string from the ruling file."""
    pkg = PKG.read_text(encoding='utf-8')
    line = RULING.read_text(encoding='utf-8').split('\n')  # line[n - 1] = line n of the ruling
    for n, head in ((266, 'C-V04 05_preregistration_and_analysis.md NEW ('), (269, ''), (272, 'C-V05a 04_data_and_splits.md NEW ='),
                    (276, 'C-V08 01_introduction.md (OLD and NEW'), (277, 'OLD:'), (279, 'NEW:')):
        assert line[n - 1].startswith(head) and (head or line[n - 1] == ''), f'ruling l.{n}'
    table = dict(ln.split()[::-1] for ln in line[195:205])  # sha -> path, Ruling 9
    assert {f'paper_v1_analysis/{f}': h for f, h in TARGET.items()} == {v: k for k, v in table.items()}, 'TARGET is not the table of Ruling 9'
    blk = {bid: (f, old, new) for bid, f, old, new in A.blocks(pkg)}
    old_s, new_s = line[272].removeprefix('OLD sentence: '), line[273].removeprefix('NEW sentence: ')
    assert blk['C-V05a'][2].count(old_s) == 1 and old_s != line[272] and new_s != line[273]
    ruled = {'C-V04': (blk['C-V04'][1], line[267] + '\n\n' + line[269]),  # l.268, an empty line, l.270
             'C-V05a': (blk['C-V05a'][1], blk['C-V05a'][2].replace(old_s, new_s)),  # l.273 -> l.274
             'C-V08': (line[277], line[279])}  # l.278, l.280
    for bid, (old, new) in ruled.items():
        f, old0, new0 = blk[bid]
        was = f'<<<{bid} {f} OLD>>>\n{old0}\n<<<{bid} {f} NEW>>>\n{new0}\n<<<{bid} EVIDENCE>>>'
        assert pkg.count(was) == 1, bid
        pkg = pkg.replace(was, f'<<<{bid} {f} OLD>>>\n{old}\n<<<{bid} {f} NEW>>>\n{new}\n<<<{bid} EVIDENCE>>>')
    return pkg


def gate(A, src: dict[str, str]) -> None:
    """The tree is the committed after-C2 state: the gate of apply_c_v2.py plus Ruling 6 (iv) and (v)."""
    A.check_pre(src)
    assert sha(src['07_disclosures.md']) == FILE07_AFTER_C2, '07_disclosures.md is not the C2 text'
    assert sha(src[MANIFEST].split('\n')[-2]).startswith(ROW40_SHA), 'the last manifest row is not the C2 row for 40'


def build(A, src: dict[str, str]) -> dict[str, str]:
    out = A.build(src, ruled_package(A))
    assert set(out) == set(TARGET) | {MANIFEST}, sorted(set(out) ^ (set(TARGET) | {MANIFEST}))
    before, after = src[MANIFEST].split('\n'), out[MANIFEST].split('\n')
    assert len(before) == len(after) and after[-1] == '' and after[-3:] == before[-3:], 'manifest: line count, final newline or the two C2 rows'
    assert [i + 1 for i, (x, y) in enumerate(zip(before, after)) if x != y] == [71, 73], 'manifest: lines other than 71 and 73 differ'
    assert after[70] == LINE71 and after[72] == LINE73, 'manifest lines 71 and 73 are not the strings of Ruling 9'
    assert sha('\n'.join(after[:-3]) + '\n') == MAN_HEAD_SHA, 'manifest: sha256 of the lines before the two C2 rows'
    return out


def after_c2_in_memory() -> dict[str, str]:
    """The after-C2 tree, built from 9b8e6ae with the freeze transfer's own functions; nothing is written."""
    c2 = load(C2)
    cpkg = c2.PKG.read_bytes()
    assert hashlib.sha256(cpkg).hexdigest() == c2.PKG_SHA, 'text package of the freeze transfer'
    cpkg = cpkg.decode('utf-8')
    def show(f: str) -> str:
        return subprocess.run(['git', '-C', str(R), 'show', f'{BASE}:paper_v1_analysis/{f}'], capture_output=True, check=True).stdout.decode('utf-8')
    names = subprocess.run(['git', '-C', str(R), 'ls-tree', '--name-only', f'{BASE}:paper_v1_analysis'], capture_output=True, check=True).stdout.decode().split()
    src = {f: show(f) for f in names if f.endswith('.md')} | {MANIFEST: show(MANIFEST)}
    t06 = c2.swap(src['06_results.md'], c2.B2_OLD, c2.B2_NEW)
    src['06_results.md'] = c2.swap(t06, c2.C2A_ANCHOR, c2.C2A_ANCHOR + '\n\n' + c2.c2a_text(cpkg))
    src['05_preregistration_and_analysis.md'] = c2.swap(src['05_preregistration_and_analysis.md'], c2.C2B_OLD, c2.C2B_NEW)
    src['07_disclosures.md'] = c2.swap(src['07_disclosures.md'], c2.C2C_ANCHOR, c2.C2C_ANCHOR + c2.C2C_ADD)
    src['03_method.md'] = c2.swap(src['03_method.md'], c2.C1B_ANCHOR, c2.C1B_ANCHOR + c2.C1B_ADD)
    stamp = '2026-11-16T05:00:01Z'  # dummy: the real freeze line does not exist yet
    line = c2.k7_template().replace('<utc>', stamp).replace('<id>', '1116zz')
    ident = line.split(' ')[1].rstrip(':')
    row = '\t'.join(['NOT RUN', f'decisions LOG::{ident}', f"'{c2.K7_FACT}'", c2.sha(line.encode('utf-8'))[:12],
                     f'FACT_RECORDED (LOG line {ident}, {stamp}; CC-378 ruling 7; shell C2)', '06_results.md'])
    row40 = '\t'.join(['40', f'manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_DEV_PREREG_v1_1.md::§5 No Vietnamese '
                       f'memory swap ({c2.FORTY_QUOTE})', f"'{c2.FORTY_QUOTE}'", c2.PREREG_SHA12, 'registered text (v1.1)', '06_results.md'])
    src[MANIFEST] += row + '\n' + row40 + '\n'
    return src


def main() -> int:
    write = sys.argv[1:] == ['--write', '--ruling', 'CC-408']
    assert write or not sys.argv[1:], 'usage: no argument (check in memory), or --write --ruling CC-408'
    for path, pin in PINS.items():
        assert hashlib.sha256(path.read_bytes()).hexdigest() == pin, f'pin {path.name}'
    A = load(MODULE)
    if write:
        def git(*a: str) -> str:
            return subprocess.run(['git', '-C', str(R), *a], capture_output=True, check=True).stdout.decode()
        git('merge-base', '--is-ancestor', BASE, 'HEAD')
        assert git('status', '--porcelain', '--', 'paper_v1_analysis/*.md', f'paper_v1_analysis/{MANIFEST}') == '', 'section files or manifest not clean'
        src = {p.name: p.read_text(encoding='utf-8') for p in sorted(PD.glob('*.md'))} | {MANIFEST: (PD / MANIFEST).read_text(encoding='utf-8')}
    else:
        src = after_c2_in_memory()
    gate(A, src)
    out = build(A, src)
    equal = {f: sha(out[f]) == want for f, want in TARGET.items()}
    print('mode:', 'WRITE on the working tree' if write else 'CHECK on an in-memory after-C2 tree (nothing is written)')
    for f, want in TARGET.items():
        print(f"{'EQUAL  ' if equal[f] else 'DIFFERS'} {f:38s} result {sha(out[f])}" + ('' if equal[f] else f'  target {want}'))
    print(f'{MANIFEST}: byte rule of Ruling 9 met (only lines 71 and 73 change; sha256 of the lines before the two C2 rows {MAN_HEAD_SHA[:8]})')
    if not all(equal.values()):
        print('NOT WRITTEN: a result differs from its target in CC-408 Ruling 9; the targets are not adjusted here')
        return 1
    if write:
        for f, text in sorted(out.items()):
            (PD / f).write_bytes(text.encode('utf-8'))
        print(f'WRITTEN: {len(out)} files under CC-408; paper HEAD', git('rev-parse', '--short', 'HEAD').strip())
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
