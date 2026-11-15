#!/usr/bin/env python3
"""Apply the Paper A text fixes ruled in CC-403 (GO 88) to the paper repo WORKING TREE.

The body below is the judge's own check script (cc403_check/final.py, sha256 cda460da...) unchanged, which
builds the 13 final files in memory from HEAD 3ff70f2, the package blocks (blocks.json 7e8a5378) and the
judge-written blocks of Annex A (judge_blocks.json 10d85b40), and asserts that the custody zones (S11 in both
supplements, Section 6.7, the abstract body, the highlights) are byte-unchanged. Added here: gates before
it (pins of the three inputs, paper HEAD, clean paper/ tree) and, after it, a comparison of all 13 results
with the sha256 targets of CC-403 Ruling 9; files are written only if all 13 match. It imports scrub() and does
not run scrub_supp.py (CC-403 W2). Never runs git add / commit.
Usage: python3 -I apply_cc403.py     (python3 -I: the script adds the scrub folder to sys.path itself)
"""
import hashlib as _h, pathlib as _p, subprocess as _s
_C = _p.Path('/mnt/d/vsps_image_captioning/.session_backup/2026-11-15/cc403_check')
_PINS = {'final.py': 'cda460da', 'blocks.json': '7e8a5378', 'judge_blocks.json': '10d85b40'}
for _n, _pin in _PINS.items():
    assert _h.sha256((_C / _n).read_bytes()).hexdigest().startswith(_pin), f'pin {_n}'
_R = '/mnt/d/vsps_papers/vsps-paperA-spic'
assert _s.run(['git', '-C', _R, 'rev-parse', '--short', 'HEAD'], capture_output=True, check=True).stdout.decode().strip() == '3ff70f2', 'paper HEAD'
assert _s.run(['git', '-C', _R, 'status', '--porcelain', '--', 'paper'], capture_output=True, check=True).stdout == b'', 'paper/ tree not clean'
# ---- judge's check script, unchanged ----
import json,subprocess,re,sys,hashlib,glob,os
sys.path.insert(0,'/mnt/d/vsps_papers/vsps-paperA-spic/paper/build')
from scrub_supp import scrub, LEAK
R='/mnt/d/vsps_papers/vsps-paperA-spic'
B=json.load(open('/mnt/d/vsps_image_captioning/.session_backup/2026-11-15/cc403_check/blocks.json')); J=json.load(open('/mnt/d/vsps_image_captioning/.session_backup/2026-11-15/cc403_check/judge_blocks.json'))
for k in ('N-12r-a','N-12r-b','N-15r'): J.pop(k)
J['N-10r'][2]=J['N-10r'][2].replace("by that convention the","by that convention (post hoc) the")
def head(f): return subprocess.run(['git','-C',R,'show','3ff70f2:paper/'+f],capture_output=True,check=True).stdout.decode()
order=[]
for bid in sorted(B,key=lambda x:(int(re.search(r'\d+',x).group()),x)):
    if bid in ('A-F10','A-F21','A-F24'): continue
    d=B[bid]; order.append((bid,d['file'],d['OLD'],d['NEW']))
for k,(f,o,n) in J.items(): order.append((k,f,o,n))
files={}
for bid,f,o,n in order:
    s=files.setdefault(f,head(f)); assert s.count(o)==1,(bid,s.count(o)); files[f]=s.replace(o,n)
for bid,f,o,n in order:
    if n: assert files[f].count(n)==1,bid
# blank lines in SPIC
sp=files['supplementary_SPIC.md']; print('3+ newline runs in SPIC:',len(re.findall(r"\n{3,}",sp))); files['supplementary_SPIC.md']=re.sub(r"\n{3,}","\n\n",sp)
o,rows=scrub(files['supplementary.md']); assert o==files['supplementary_SPIC.md']; print('BYTE-EQUAL scrub(src)==SPIC')
print('leaks',sorted(set(LEAK.findall(o))))
files['supplementary_provenance_internal.tsv']="comment_no\tsrc_line\theading\tvisible_text_before\tcomment\n"+"".join("\t".join(r)+"\n" for r in rows)
files['number_manifest.tsv']=head('number_manifest.tsv')+"1,000 (A-N3 bootstrap draws, span-label test, Section 7.2)\tA\tdata/results/a_n3/a_n3_run.json\tconfig.n_boot\t7a5a614d2068\tkeyed (CC-403 N-14; registration manuscript/prereg/2026-10-19_a_n3_criterion_mhaldetect.md l.47)\n"
def words(t): return len(re.sub(r"<!--.*?-->","",t,flags=re.S).split())
cnt={}
for p in sorted(glob.glob(R+'/paper/sec*.md'))+[R+'/paper/declarations.md']:
    fn=os.path.basename(p); cnt[fn]=words(files.get(fn,head(fn)))
tot=sum(cnt.values()); top=sorted(cnt.items(),key=lambda x:-x[1])[:3]; print('main',tot,top)
ab=head('abstract_A.md')
reps=[("counted 2026-11-13 UTC at the Phase B commit).","counted 2026-11-13 UTC at the Phase B commit; recounted 2026-11-14 UTC after the CC-403 text fixes)."),
 ("Main text now: 18,505 words",f"Main text now: {tot:,} words"),("Over the limit by 10,005 words.",f"Over the limit by {tot-8500:,} words."),
 ("Longest files: sec7_verbosity_sign.md 7,461; sec2_related_work.md 2,184; sec11_limitations_ethics.md 2,001.","Longest files: "+"; ".join(f"{a} {b:,}" for a,b in top)+".")]
for a,b in reps: assert ab.count(a)==1,a; ab=ab.replace(a,b)
files['abstract_A.md']=ab
# custody assertions
def after(s,mark): i=s.index(mark); return s[i:]
for f in ('supplementary.md','supplementary_SPIC.md'):
    assert after(files[f],'\n## S11 ')==after(head(f),'\n## S11 '),f
s7=files['sec7_verbosity_sign.md']; assert after(s7,'\n## 6.7')==after(head('sec7_verbosity_sign.md'),'\n## 6.7')
a0=head('abstract_A.md'); i=a0.index('## Abstract'); assert ab[ab.index('## Abstract'):]==a0[i:]
assert 'highlights_A.md' not in files
print('custody zones unchanged: S11 x2, 6.7, abstract body, highlights')
print('order:',[b for b,*_ in order])
for f,s in sorted(files.items()):
    print(f, hashlib.sha256(head(f).encode()).hexdigest()[:12],'->',hashlib.sha256(s.encode()).hexdigest())

# ---- compare with the targets of CC-403 Ruling 9, then write ----
_T = {'abstract_A.md': '61fa852921d406e991a04c7af69c5d13c8343fe92ada69aec1f1f5fe23f0cda2',
      'number_manifest.tsv': '14f12d297b63ab234a1504c0e9dc6a56dc7edc45c8fcf170d5ce36f0b2fbdf84',
      'outline.md': '85953e6a3011379993c0b6bb4b3e47f5a109a0f2f91c77a896f125344beb625d',
      'sec10_discussion.md': '0b7137efc9a323f362f0961a41343639fe6e00e050354b0a608a3a869837a4b6',
      'sec11_limitations_ethics.md': '912620f1a520b4fe97d38735267cdedcd02af0c58c2b5eb60022eb375c8872f3',
      'sec1_introduction.md': '46b7534e1936ce4841d8c23b5baf09a6e4457e651917c5055ef872de2475c914',
      'sec3_measurement_setup.md': 'e24a48620d6ea2644170525d419f2567caef7309d10c89758c81f25bfc598077',
      'sec5_exchangeability.md': '280b0e87e80d387df432515d392d50400a39c798581ad8b2e25c5ce52883a8fd',
      'sec7_verbosity_sign.md': 'b6f46b8aaf33ef133b54e5e4d91f2c1f037e061d48f495e1b23eed5b0aaf4817',
      'sec8_human_validity.md': '4572367c38fbb12dda6cf4786f41ce64e692f583c95e233fecd13499b3dc182d',
      'supplementary.md': '497bf520564c025ec2ddb192d05fb17344dccd00a492c6c17c928bdd9c62a00b',
      'supplementary_SPIC.md': '711a98e45815c85834dda04a5950feb47c501fb09be043f464df4341e9a6387a',
      'supplementary_provenance_internal.tsv': 'b50eee90834a95e39ca251544180e32c81879cd2c301b0dacb30146188adee21'}
assert set(files) == set(_T), sorted(set(files) ^ set(_T))
for _f, _want in _T.items():
    assert hashlib.sha256(files[_f].encode()).hexdigest() == _want, f'sha differs from CC-403 Ruling 9: {_f}'
for _f, _text in files.items():
    (_p.Path(R) / 'paper' / _f).write_bytes(_text.encode())
print('WRITTEN: 13 files equal to the CC-403 Ruling 9 targets')
