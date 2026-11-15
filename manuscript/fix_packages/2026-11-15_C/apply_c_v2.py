#!/usr/bin/env python3
"""Apply C_FIX_PACKAGE_v2.md to the Paper C paper repo WORKING TREE. PREPARED 2026-11-15, NOT RUN.

It applies only to "HEAD after shell C2" (the freeze transfer c_attr_c2_transfer.py, committed on or after
2026-11-16T05:00:00Z). Gates before any write: the package pin; commit 9b8e6ae is an ancestor of HEAD; the
section files and the manifest are clean against HEAD; every file this package changes has the sha256 it must
have after shell C2 (PRE); the manifest is the 9b8e6ae manifest plus exactly the two rows shell C2 appends.
Then, in memory: the 12 OLD/NEW blocks (each OLD once at its turn, each NEW once after), the renumbering of
Tables 10-18 with exact counts, and the two manifest rows of CC-405 Annex B. Checks: the abstract (150-200
words, no first person, no citation), the prompt template byte for byte against the two pinned code files
(read by syntax tree, nothing executed), Table 12 (old 17) rows, caption order, untouched files. The section
files are written only if they equal TARGET. Reads no ledger, caption, label or test-set file. Never runs
git add / commit. If a judge changes a NEW text, PKG_SHA and TARGET are void and must be recomputed.
Usage: python3 -I apply_c_v2.py
"""
import ast
import collections
import hashlib
import json
import re
import subprocess
from pathlib import Path

RUN = Path('/mnt/d/vsps_image_captioning')
R = Path('/mnt/d/vsps_papers/vsps-paperC-tallip')
PD = R / 'paper_v1_analysis'
PKG = RUN / 'manuscript/fix_packages/2026-11-15_C/C_FIX_PACKAGE_v2.md'
PKG_SHA = '2653ec721b4442b450b973d813c085f23b2b116f47cfba9cc3b4e3e80dcea171'
BASE = '9b8e6ae'
MANIFEST = 'number_manifest_C.tsv'
MAN_BASE_SHA = '83414dc3d863bbe62c67b64c4dd0cb9b3f9796fc7247575b08a9bf7f296d1f81'  # manifest at 9b8e6ae
RESTORED = 'keyed (restored under PI-1110n; CC-405)'
# sha256 of each section file as it must stand after shell C2, before this package (03, 05, 06 are changed by C2)
PRE = {
    '00_abstract.md': '4c023726251dc023be30542f3d95d778af8f7b0c483fa84e1379f026a7a6d630',
    '01_introduction.md': 'b731e6371c425657f647732faf5ddf0203001fed3dc15f5e694f410dc575ec00',
    '03_method.md': '45888a88eddaad7fff2aafea9d30f92f82a355b1d9f7f72e9e48c13ae2ff12f5',
    '04_data_and_splits.md': 'f7d1d0e7fa48390fa78e7cccfed971c59a66401a1405f9c6dd78430e06177b99',
    '05_preregistration_and_analysis.md': '0137bb6bfe2245d7f3c2788aaa64105fa780daebc33984b3575ba7df69444a83',
    '06_results.md': '68f77eb9a59e8d07a293aa7cb316f407b4d2b9f38717c5ee7b73fb97ee9995fa',
    '08_english_comparison.md': '72f3cd8b5f916669c54490f993447f8fa5af6ba5ce240647f5a842bf6ae10b14',
    '09_limitations.md': '4111d0957ae1555922defef6096a396a3b76b300c57435c0778e8f8ebfe01df2',
    '11_supplement_registered_rows.md': '025d744a9413ef509558496ef55694188dd7249baace8a946aa98c81c791f165',
    'V2_PROGRESS_C.md': 'c208ed1b3cb6537dfee718bb057522913921aed4c3b8ba731d5d48e5e1f45d7d',
}
# sha256 of each section file after this package
TARGET = {
    '00_abstract.md': 'a4725e99fbd8883be97c991639020870a8bcdfa21f34483ddf5f5f18610cc51f',
    '01_introduction.md': 'ad60b37f045ad34d2994d6a44e2459fbb13e044f367a5e1a159ea95273cbbe0c',
    '03_method.md': '5db109ab3b011cf658da599d5ef67636c7b282f378829abb3a35f176521da057',
    '04_data_and_splits.md': 'b7f333a8571685cdd84c1fc1b7556ebecba3e2e98fd8e6597a30e7d82be7575c',
    '05_preregistration_and_analysis.md': 'd46bbc40a2ed9343ea7a1d3d02b4947b7fac3d4bf3cfad397cfbbdd5cfdeae68',
    '06_results.md': '01d41de0ba50542b5a991353e7ff56f762f5ce36b33e8b732fa3d352530e60f6',
    '08_english_comparison.md': '69706e5f18ef88a5c9d9bdbcb8ad30607b565cd58043d50275a84f6e93a121f8',
    '09_limitations.md': 'c52b962c41460296aefd324c7f9a53b4b6f1c149026c17d08051d279c458745c',
    '11_supplement_registered_rows.md': '5a71a8a08085cdaabe385539208f008275aed18fabbd6c962cf0d0c5c44f0ff9',
    'V2_PROGRESS_C.md': 'eee308faacbd2f5f0902d65db79c34ad4ad3cfeb2954acbfaea1fe26b2c16689',
}
UNTOUCHED = ('02_related_work.md', '07_disclosures.md', '10_conclusion.md', 'STUDY_BRIEF_C.md')
CODE = {  # pinned code that holds the prompt templates: path -> (sha256, name of the pin constant)
    'scripts/c_stage1/decode_icl.py': ('fa5a251160d4fd4fb0cd130af33614283863a84e6ed7905f3da81bb6255010db', 'TEMPLATE_SHA256'),
    'scripts/c_en/cen_decode.py': ('777a5af03e9f1f61d5de638747c8e18cd5b4e528de0bdba745a621f2903a3885', 'EN_TEMPLATE_SHA256'),
}
TABLE_MAP = {'15': '10', '16': '11', '17': '12', '18': '13', '10': '14', '11': '15', '12': '16', '13': '17', '14': '18'}
TABLE_COUNTS = {  # labels changed per file, by old number, on "HEAD after shell C2"
    '05_preregistration_and_analysis.md': {'10': 1},
    '06_results.md': {'13': 1, '14': 1, '15': 3, '16': 12, '17': 3, '18': 2},
    '08_english_comparison.md': {'10': 1, '11': 2, '12': 2, '13': 3, '14': 2},
    '09_limitations.md': {'15': 1, '16': 1, '18': 1},
    '11_supplement_registered_rows.md': {'14': 3, '15': 1, '18': 1},
}
LABEL = r'S?\d+[a-z]?(?:\s*\([a-z]\))?'
TABLE_REF = re.compile(rf'\bTables?\s+{LABEL}(?:(?:,\s*|\s+and\s+|–){LABEL})*')
TABLE_LAB = re.compile(r'(?<![\dS.])(1[0-8])(?![\da-z])')


def sha(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def blocks(pkg: str) -> list[tuple[str, str, str, str]]:
    """(id, file, OLD, NEW) in the order of the package."""
    m = re.split(r'^<<<(C-V\d+[a-z]?) (?:(\S+) )?(OLD|NEW|EVIDENCE|END)>>>\n', pkg, flags=re.M)
    b: dict[str, dict] = {}
    for i in range(1, len(m), 4):
        bid, f, kind, body = m[i:i + 4]
        if kind in ('OLD', 'NEW'):
            b.setdefault(bid, {'file': f})[kind] = body.removesuffix('\n')
    assert len(b) == 12, len(b)
    return [(bid, v['file'], v['OLD'], v['NEW']) for bid, v in b.items()]


def renumber(name: str, text: str) -> str:
    seen: collections.Counter = collections.Counter()

    def lab(m: re.Match) -> str:
        seen[m.group(1)] += 1
        return TABLE_MAP[m.group(1)]

    out = TABLE_REF.sub(lambda m: TABLE_LAB.sub(lab, m.group(0)), text)
    assert dict(seen) == TABLE_COUNTS.get(name, {}), (name, dict(seen))
    return out


def templates() -> dict[str, dict]:
    out = {}
    for rel, (pin, const) in CODE.items():
        src = (RUN / rel).read_bytes()
        assert hashlib.sha256(src).hexdigest() == pin, f'code pin {rel}'
        c = {n.targets[0].id: ast.literal_eval(n.value) for n in ast.parse(src.decode()).body
             if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') in ('HEADER', 'LINE', 'TAILS', const)}
        form = json.dumps({'header': c['HEADER'], 'line': c['LINE'], 'tails': c['TAILS']}, ensure_ascii=False, sort_keys=True)
        assert sha(form) == c[const], f'template sha {rel}'
        out[rel] = {**c, 'sha': c[const]}
    return out


def manifest(text: str) -> str:
    lines = text.split('\n')  # lines[n - 1] = line n
    def edit(n: int, num: str, used: str, source: str, needle: str) -> None:
        c = lines[n - 1].split('\t')
        assert c[0] == num and c[4] == 'removed-PI-1101o' and c[5] == used, (n, c)
        raw = (RUN / source).read_bytes()
        assert hashlib.sha256(raw).hexdigest()[:12] == c[3] and needle in raw.decode('utf-8'), (n, source)
        c[4], c[5] = RESTORED, '04_data_and_splits.md'
        lines[n - 1] = '\t'.join(c)
    edit(71, '1997', '04_data_and_splits.md,07_disclosures.md', '.session_backup/2026-10-26/c_test/CHAIN.log',
         'c_ov_test     staged: 2001 files, sha OK 2001/2001, distinct sha 1997')
    edit(73, '1937', '04_data_and_splits.md', 'manuscript/prereg/2026-10-25_c_test/PREREG.md',
         '**1,941 entries / 1,937 distinct images**')
    return '\n'.join(lines)


def check_pre(src: dict[str, str]) -> None:
    """The tree is exactly "HEAD after shell C2"."""
    for f, want in PRE.items():
        assert sha(src[f]) == want, f'{f} is not the after-C2 text'
    lines = src[MANIFEST].split('\n')
    n = len(lines) - 3  # two rows appended by shell C2, then the final newline
    assert lines[-1] == '' and sha('\n'.join(lines[:n]) + '\n') == MAN_BASE_SHA, 'manifest is not 9b8e6ae plus two rows'
    assert re.match(r'NOT RUN\tdecisions LOG::OPS-[0-9a-z]+-c-k7\t', lines[n]) and lines[n].endswith('\t06_results.md'), 'K7 row'
    assert lines[n + 1].startswith('40\tmanuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_DEV_PREREG_v1_1.md::§5 No Vietnamese memory swap'), 'row for 40'


def tokens(text: str) -> list[str]:
    tok = re.compile(r'(?<![\w.])[+−-]?\d[\d,]*(?:\.\d+)?')
    return [x.group(0).replace('−', '-').replace('+', '').replace(',', '') for x in tok.finditer(re.sub(r'`[^`]*`', ' ', text))]


def number_report(src: dict[str, str], out: dict[str, str]) -> dict[str, list[str]]:
    """Number tokens whose count grows in a file and that no manifest row names for that file (report, not a gate)."""
    have = collections.defaultdict(set)
    for row in out[MANIFEST].splitlines()[1:]:
        c = row.split('\t')
        for used in (c[5].split('|')[0].split(',') if len(c) >= 6 else []):
            have[used].add(c[0].replace('−', '-').replace('+', '').replace(',', '').strip("'"))
    miss = {}
    for f, text in out.items():
        if f.endswith('.md'):
            new = collections.Counter(tokens(text)) - collections.Counter(tokens(src[f]))
            miss[f] = sorted(k for k in new if k not in have[f] and k.lstrip('-') not in have[f])
    return {f: v for f, v in miss.items() if v}


def build(src: dict[str, str], pkg: str) -> dict[str, str]:
    """All changed files, built in memory from the after-C2 texts. Raises on any failed check."""
    out: dict[str, str] = {}
    todo = blocks(pkg)
    for bid, f, old, new in todo:
        assert not TABLE_LAB.search(''.join(TABLE_REF.findall(old + '\n' + new))), f'{bid} holds a table label 10-18'
        text = out.get(f, src[f])
        assert text.count(old) == 1, (bid, text.count(old))
        out[f] = text.replace(old, new)
    for bid, f, _, new in todo:
        assert out[f].count(new) == 1, bid
    for f in sorted(set(src) - {MANIFEST}):
        text = renumber(f, out.get(f, src[f])) if f != 'V2_PROGRESS_C.md' else out.get(f, src[f])
        if text != src[f]:
            out[f] = text
    out[MANIFEST] = manifest(src[MANIFEST])
    assert not set(out) & set(UNTOUCHED), sorted(set(out) & set(UNTOUCHED))

    # abstract: TALLIP 150-200 words, no first person, no citation
    body = out['00_abstract.md'].split('## Abstract\n\n')[1].strip()
    assert '\n' not in body and 150 <= len(body.split()) <= 200, len(body.split())
    assert not re.search(r"\b(we|our|ours|us|i)\b", body, flags=re.I) and '[@' not in body

    # prompt template: the table rows are the strings of the pinned code, byte for byte
    (vi, en) = templates().values()
    rows = [f"| header | {vi['HEADER']} | {en['HEADER']} |", f"| example line | {vi['LINE']} | {en['LINE']} |",
            f"| tail T1 | {vi['TAILS']['T1']} | {en['TAILS']['T1']} |", f"| tail T2 | {vi['TAILS']['T2']} | {en['TAILS']['T2']} |",
            f"| sha256 of the template | `{vi['sha']}` | `{en['sha']}` |"]
    assert '\n'.join(rows) + '\n\n### Context from published systems (Section 8.7)' in out['11_supplement_registered_rows.md']
    assert vi['sha'].startswith('7478361a') and out['03_method.md'].count('prefix `7478361a`') == 1

    # captions in order of appearance; Table 12 (old 17): twelve rows, K_nc DETECTED and the bound in force on each
    caps = [m for f in sorted(src) if f[:2] in ('02', '03', '04', '05', '06', '08')
            for m in re.findall(r'^\*\*Table (\d+[a-z]?)\b', out.get(f, src[f]), flags=re.M)]
    assert caps == ['1', '1b'] + [str(i) for i in range(2, 19)], caps
    t12 = out['06_results.md'].split('**Table 12. Copy bound at n = 3')[1].split('\n\n')[1].split('\n')[2:]
    assert len(t12) == 12 and all(r.split('|')[6].strip().endswith('DETECTED') and r.split('|')[7].strip() == 'in force' for r in t12)
    return out


def main() -> None:
    def git(*a: str) -> str:
        return subprocess.run(['git', '-C', str(R), *a], capture_output=True, check=True).stdout.decode()
    pkg = PKG.read_bytes()
    assert hashlib.sha256(pkg).hexdigest() == PKG_SHA, 'package pin'
    git('merge-base', '--is-ancestor', BASE, 'HEAD')
    assert git('status', '--porcelain', '--', 'paper_v1_analysis/*.md', f'paper_v1_analysis/{MANIFEST}') == '', 'section files or manifest not clean'
    src = {p.name: p.read_text(encoding='utf-8') for p in sorted(PD.glob('*.md'))} | {MANIFEST: (PD / MANIFEST).read_text(encoding='utf-8')}
    check_pre(src)
    out = build(src, pkg.decode('utf-8'))
    assert set(out) == set(TARGET) | {MANIFEST}, sorted(set(out) ^ (set(TARGET) | {MANIFEST}))
    for f, want in TARGET.items():
        assert sha(out[f]) == want, f'{f} differs from its target'
    print('new number tokens without a row naming the file:', number_report(src, out))
    for f, text in sorted(out.items()):
        (PD / f).write_bytes(text.encode('utf-8'))
        print(sha(text)[:16], f)
    print(f'WRITTEN: {len(out)} files; paper HEAD', git('rev-parse', '--short', 'HEAD').strip())


if __name__ == '__main__':
    main()
