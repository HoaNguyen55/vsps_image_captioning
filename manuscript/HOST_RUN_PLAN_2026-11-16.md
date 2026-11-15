# Host run plan: one CPU-only build session (host alias set in section 2), jobs K1b, K2, K4, K5 and, after the Paper C freeze commits, K3

Written 2026-11-15T11:34Z (`date -u`; 18:34 VN) for the coordinator, at the team lead's request. A plan only: nothing was rented, run or contacted to write it. Binding for this session: no Artifact, document-connector, upload or publishing tool; outputs are local files only. Read first: skill `running-rented-gpu-jobs`, `manuscript/HOST_RUN_PLAN_2026-11-15.md` and the records of its jobs (`.session_backup/2026-11-15/host_prep_build/`, `c_tex_build/`, `taimma_build/`), rulings CC-410, CC-418, CC-420, CC-421, CC-422 and the LOG to line 2719 (OPS-1115ay).

- **Names.** K1 to K5 are the job names of this plan only. They are not the stop rule K1 of Paper C's attribution study, not the K-time of stage H and not the freeze line of Paper C. The machine of 2026-11-15 was hD: it is deleted and its laptop files are cleaned up (PI-1115s); K1 ran on it and is not run again. The machine of the next session takes the alias that section 2 sets in one line (`H=hE`; a re-rental takes the next free name, set in that same line); the alias lives only in `~/.ssh/config`. No ruled script hard-codes an alias: every command takes `$H`. No host string or address goes into any repo file or LOG line.
- **Outcome-free.** This file holds no result and no figure of any paper. The Paper A held zones (Section 6.7 of `sec7_verbosity_sign.md`, Supplementary S11) were not opened; K4 handles them by section 5.2.
- **Every input of this session is prepared and hashed on the laptop before the rental** (section 2), so no host step waits for laptop text work. Builds take seconds to minutes.

---

## 0. Decisions for the coordinator (recommendation, confidence, default)

| # | Decision | Recommendation | Conf. | Default if not decided |
|---|---|---|---|---|
| D1 | **Licence of a rental with no stage-H job.** Every licence of 15 Nov let J1 to J3 ride on the stage-H host (PI-1113g; PI-1113h says "no new rental is licensed by this line"; CC-395 ruling 8). The rule adopted after PI-1112b (LOG l.2231) says "no GPU host is rented for CPU-only work unless a judged GPU job starts on it"; PI-1113c made a one-off exception. For it: PI-1111j (tests and CPU work on rented hosts, not on the laptop); CC-399 Q3 default ("build on the next rented host"); CC-421 Ruling 5 ("Run it on the next rented host session"); CC-420 ruling 7 step 3 (Table 6 and figures by script). | Write one coordinator line under the standing approval PI-1115k: "builds-only rental for K1 to K5 of HOST_RUN_PLAN_2026-11-16.md, cap 3 h, deleted at the end". Not a reserved item of PI-1115k (no test-set look, no data licence, no submission, money far below any cap). | 85 | no rental |
| D2 | **When to rent.** T-a: as soon as K1 and K2 inputs are final (expected this evening VN); K3 (Paper C freeze chain) and the K2 count of record are carried to a second short session after the freeze. T-b: wait and run all five once, after the Paper C freeze chain is committed (not before 2026-11-16T05:00Z, 12:00 VN; realistically later). | **T-a**: PI-1115a puts the conference version first and the K2 measures decide its cut now; the K1 outputs unlock the CC-420 diff read of Paper B; a second session costs about 5,000 to 10,000 VND (money is no constraint, PI 11-10). | 75 | T-a |
| D3 | **A judge read before the run.** The scripts of Annex A and the two derived K2 files differ from the bytes CC-410 read (TARGET `build_lncs.sh` ef21d602, as-run preamble cdfe51a9). | One-judge REVERSIBLE read of Annex A (8 files) and of the K2 diff (section 4.2) before renting. Without it every K2 count stays PROVISIONAL, which it is anyway tonight; the K2 count of record (K2-R) cannot be logged without it (CC-410 J3-1). | 80 | run without the read; K2 PROVISIONAL |
| D4 | **K5 cannot run as the script stands** (section 4.5). | NOT RUN until an adapted Springer build script exists with its own read. | 90 | NOT RUN |
| D5 | **Idle rule.** Measured on 15 Nov: T0 08:12:19Z to tools ready 08:18:38Z (6 min, with four setup attempts). | Delete the host when the expected wait for the next step exceeds 10 min. Nothing in this plan waits, since all inputs exist before T0. | 85 | 10 min |

---

## 1. Preconditions and money

### 1.1 Licences per job

| Job | Licence on the LOG |
|---|---|
| Rental | D1 (coordinator line under PI-1115k), or the PI's yes |
| K1 Paper B Table 6 and figures | CC-420 ruling 7 step 3 (Table 6 by the script of FIGURE_TABLE_SPEC A2 from HUMAN.json and BUILD.json; Fig. 3, Fig. 2, Fig. EF1, Fig. 1; outputs to `paper/rev_2026-11-15/figures/` with a sums file; a one-judge DIFF read before their commit). Custody of the Paper B results was released by CC-418 (from its LOG line) |
| K1b Paper B Fig. EF1 and Fig. 1 | CC-428 ruling 4 (CC sha ab98dc743c8b2c92714bcc9745cf9cb21ea254dfe556f5b9ce9be16b88b2261e): 12-file allow-list (list sha 4559900b36be7a3d372fe36549da3fabccf03b8cab7fae2f133530ab3fea11e8), runner k1b_run.sh 8ed0cb65d480e634dbeba1124c9aca2590562ffffaec77aa63863ab3d0168e40; before the push W1 and W2 closed by sha match and the W3 coordinator line on the LOG. K1 itself is not run again: it ran on 2026-11-15 (venv, selftest and build rc 0; records and pulled outputs in `.session_backup/2026-11-15/host_session_hD/k1/`) |
| K2 TAIMMA page measures | CC-421 Ruling 5 ("both layouts, and once more with the placeholders filled by dummy text"); CC-399 G1, Q3; CC-410 J3-1 to J3-5 and ruling 7 |
| K3 Paper C journal tex/PDF | PI-1113h (the use); CC-410 J2-0 ("the commit of generated files waits for the rebuild after C2 + v2, with its own diff read"); tickets T1 of CC-400 and CC-401 |
| K4 Paper A main and supplement PDFs | CC-422 (fix package v6, step B1 `build_A_supp.sh`); committed 95909d4 (OPS-1115aw) and a7f2b4e (condition W5, OPS-1115ax) |
| K5 Paper B Springer build | CC-420 ruling 7 step 3 (one build for the page count); CC-426 ruling 8 (CC sha 4aaddf05714c937e4205ee9e5f47637bf797af4ad220f830f0ae98bd0adb57d7: `build_B_rev.sh` SAFE and FIT FOR JOB K5, its inputs are the allow-list) and CC-425 addendum A3 (CC sha bf6eaf40c005fa0cadaebce5def7edb6629ca67218386e8ec08d9e54d701b87c: when and how it runs; conditions (1) to (4)) |

### 1.2 State of the inputs at 2026-11-15T11:34Z (re-check every line in section 2)

| Job | Ready? | What exists now (sha256 at my read) | Missing |
|---|---|---|---|
| K1 | partly | `scripts/b_figs/build_all.sh` 87a04678161385d4, `fig2_breaking.py` 3a936e97f045d5b8, `fig3_human.py` 2281dcff8053850a, `table6_human.py` 2c0d40302df036a5. Inputs named by the script constants, each equal to its pin (checked with Annex A `k1_list.py`, rc 0): `RESULT.json` 25614b469cf59dc61f15e839b89a8e78ca0b316905afc4bd2ae52eaa0d32b43a (`.session_backup/2026-11-13/b_stages/host_pull/20261113T174234Z/b_work/`), `HUMAN.json` 990a0df51ba3e35349fbe2dcf37826150ce9d5c3aa88b3e375c697377f745057 (`.../host_pull/H_20261115T083124Z/b_work/`), `BUILD.json` 05a6c5b72aa4c17c6baf1b1bd520700730f90f073997e8c5977f1f8188c3b201 (`manuscript/prereg/2026-11-12_b_fecert/b_pref_pin/`), held `paper.md` cb462dfc4797f3b7030fbe58a7b873aabef8a204cba62b55392cde92c1ed6a0e (`.session_backup/2026-11-14/b_text_held/draft_v3/`) | `build_all_v2.sh` (being written; used if present). Fig. EF1 and Fig. 1 are in no script yet. `table6_human.py` compares with the held draft_v3 `paper.md`, not with the transferred `paper/rev_2026-11-15/paper.md` (aeeaa016, Paper B HEAD 568eaec): which file block T6 is compared with is the script author's call; `k1_list.py` re-run just before the push decides |
| K2 | **yes** | `manuscript/conf_taimma_2027/draft_v3_1/paper.md` b42eecb1c8e574af98ade56902fae0676a440f6cfd579dd8690984be5ee6692d (final for the provisional count, team lead 2026-11-15) and `check_draft.py` c07066475cfb703d1dbd1e4e4e8161aac8666cd7c5a4e580d465a0d8d70c8dc0 (OPS-1115as); `paperC.bib` a415c4da and `tex/strip_num.lua` 5a91751f at Paper C HEAD 55315ca; build files of 15 Nov: `host_prep_build/j3/build_lncs.sh` ef21d602 (CC-410 TARGET, = as run), `j3/lncs.lua` c8d597b4 (= as run), `taimma_build/in_as_run/lncs_preamble.tex` cdfe51a9 (as run, with the host change of HOST_CHANGES.diff 77e3e658) | restore texts r1 to r4 (no exact pairs exist); k0 and k3 (not mechanical, section 4.2) |
| K3 | no | Paper C HEAD 55315cad9e57073a9ccd346597fae34e393db69a; tools package of 15 Nov (section 2, P2) | the freeze chain of the runbook `manuscript/fix_packages/2026-11-15_C/CHAIN_REHEARSAL_2026-11-15.md` (3f19f129e30dc862dc84d0d33a6020ef6cc9f6a46038b7a8d1c4bc7f3ec68ac8), steps 1 to 6: shell C2 (not before 2026-11-16T05:00:00Z), then v2 (CC-408), v4 (CC-413), v5 (CC-423), each with its gatekeeper commit line; K3 is its step 7 |
| K4 | **yes** | Paper A HEAD a7f2b4ece3f6d2229f85494c2cd1e35080224ae2 (v6 in 95909d4, W5 in a7f2b4e); at HEAD: `paper/build/build_A_cas.sh` fa54fa4e2d57c985, `build_A_supp.sh` e3a4cab2a1d4a5d2 (= CC-422), `filter.lua` 89e187af95d4f70b, `prep.py` 9a08ef5a89627ef7, `shims.tex` 0d2622f6101aaedc, `cas.pandoc.tex` f6d20ce7bcd74265; pinned `cas-common.sty` e95a01f4b33531d01ade231669fcc1e42f52193dddcb22ead5b63240eb952f8f at `.session_backup/2026-10-27/builds/A_cas/cas-common.sty` | none |
| K5 | yes, once the A3 (3) line is on the LOG | Paper B HEAD 6356b995e0c9475fb8b12f075407ebedcf876301; `paper/build/build_B_rev.sh` d671b9d2c637d5dec5d4fe85e93e38275b2e92bc167fc3601435f7f88f25ed2a at that HEAD (equal to the sha CC-426 names, l.123; read with `git show 6356b99:paper/build/build_B_rev.sh`); the old `build_B_springer.sh` is not used (CC-426 N5) | the coordinator line of CC-425 addendum A3 (3) extending OPS-1115ba to K5 |

### 1.3 Money

| Item | Value | Source |
|---|---|---|
| Last balance | **362,570 VND** (L-after of hD, two equal panel reads) | OPS-1115bh-hD-deleted |
| Rate | **9,224 VND/h + 30 VND set-up fee; 9,254 VND/h used in the check** | OPS-1115bc-hD-rent (offer 85425) |
| Cap of this session | **3 h** (expected use 0.5 to 1 h; 15 Nov: 3,107 VND for about 20 min and 1,321 VND for about 8 min 30 s) | this plan; CC-431 ruling 5 |
| L-before | balance >= cap x rate + 3 x rate + other live rentals (none) = 6 x 9,254 = **55,524 VND** | skill l.19 |

- 362,570 >= 55,524: PASS. The check holds for any rate up to 60,428 VND/h; use the real rate of the chosen offer.
- Expected spend 4,627 to 9,254 VND; at the full cap 27,762 VND, leaving 334,808 VND.
- Warn the PI to top up at **50,000 VND** (PI-1108h); during a live rental warn at least 12 h before the balance runs out, that is at 111,048 VND at this rate (skill l.20). Neither level is reached by this session or by a second one of the same size.
- Fresh panel read just before renting; L-after with the panel's per-instance figure after the deletion (skill l.22).

---

## 2. Laptop preparation (no cost; all before T0)

Common lines for every block of this plan (the address filter and helpers of `J2_RUN.md`):

```bash
H=hE   # the alias of this session; the only line that sets it
REPO=/mnt/d/vsps_image_captioning
PLAN=$REPO/manuscript/HOST_RUN_PLAN_2026-11-16.md
HP=$REPO/.session_backup/$(date -u +%F)/host_prep_$H        # prep folder; name it in the prep OPS line
PA=/mnt/d/vsps_papers/vsps-paperA-spic; PB=/mnt/d/vsps_papers/vsps-paperB-lre; PC=/mnt/d/vsps_papers/vsps-paperC-tallip
F() { grep -v -E '([0-9]{1,3}\.){3}[0-9]{1,3}'; }
S() { ssh -o BatchMode=yes "$H" "$@" 2>&1 | F; return "${PIPESTATUS[0]}"; }
sha() { sha256sum "$1" | cut -c1-64; }
```

**P0. Annex scripts.** Extract the eight files of Annex A byte for byte and check them:

```bash
mkdir -p "$HP/scripts"
x() { awk -v b="-----BEGIN $1-----" -v e="-----END $1-----" '$0 == e {f = 0} f {print} $0 == b {f = 1}' "$PLAN" > "$HP/scripts/$1"; }
for n in run_setup.sh k1_list.py k1_run.sh k2_cuts.py k2_prep.py k2_run.sh k4_run.sh k_counts.sh; do x "$n"; done
(cd "$HP/scripts" && sha256sum -c --quiet -) << 'EOF' && echo "annex OK: 8 files"
c4998685f2e026feba0522010c046648ce1d02bd99ff04e64605b23e5b29291b  run_setup.sh
dcf6decc36348074fec48b23ef99981963308fc747dd502a298fa8a9bda042d9  k1_list.py
ca60daf87cef569e57eade457e6dc7ee4bda25ce24eefe4667e49f3c7ed13982  k1_run.sh
8ff6d2dc487a3c0fc5be451cda6c68e9390b87346acec413adafc37ed6e0e7df  k2_cuts.py
bef12da9987254eb842427e41f98358e0c5fb1d8f1b54fde1118e40503454d45  k2_prep.py
a06f6e47bd0843fce23366d3b601ee674ba3b9206f42b966059fd37be46e4152  k2_run.sh
a21571b3fdd6acdcd50a80c62f78acbc9351843ab4ee8cab3279aeb8f5b50dd7  k4_run.sh
685183a20bff56f11bc1f8c5c658fa31d8ebc41ecafc4d3800a1058b573fa442  k_counts.sh
EOF
for f in "$HP"/scripts/*.sh; do bash -n "$f" || echo "STOP: syntax $f"; done
```

STOP on any mismatch: nothing of this plan is used until it is read.

**P1. Tools package** (the J2 package of 15 Nov with the **as-run** setup script, which worked on this template; the package bytes 7ad7ded3 failed on missing cairo/pango, record `c_tex_build/HOST_CHANGES.diff` 9da4cb3e):

```bash
P=$REPO/.session_backup/2026-11-15/host_prep_build/j2
(cd "$P" && sha256sum --quiet -c J2_PUSH.sha256) && echo "J2 list OK: 10 files"
mkdir -p "$HP/tools"; (cd "$P" && tar -cf - $(cut -c67- J2_PUSH.sha256)) | tar -xf - -C "$HP/tools"
cp $REPO/.session_backup/2026-11-15/c_tex_build/host_tex_setup.as_run_final.sh "$HP/tools/host_tex_setup.sh"
cp "$HP/scripts/run_setup.sh" "$HP/tools/"
(cd "$HP/tools" && find . -type f -printf '%P\n' | sort | xargs sha256sum) > "$HP/tools.sha256"
grep -c . "$HP/tools.sha256"                                          # 11
grep -E ' host_tex_setup.sh$| j2_host_build.sh$| check_610.py$' "$HP/tools.sha256" | cut -c1-16
#   -> bf5294df081a0aef (as run), 654b187a670d2707, 8b5374092c33f511
```

**P2. K1 inputs** (run again right before the K1 push of section 4.1; a MISMATCH line or rc 1 is a STOP for K1 only):

```bash
K1S="build_all.sh fig2_breaking.py fig3_human.py table6_human.py"   # the four files read by CC-425; no other file of scripts/b_figs goes to the host
python3 -I "$HP/scripts/k1_list.py" "$REPO" $(for s in $K1S; do case $s in *.py) echo "$REPO/scripts/b_figs/$s";; esac; done) | sort -u > "$HP/k1_inputs.sha256"; echo "k1_list rc ${PIPESTATUS[0]}"
(cd "$REPO" && sha256sum $(for s in $K1S; do echo "scripts/b_figs/$s"; done)) > "$HP/k1_scripts.sha256"
cat "$HP/k1_inputs.sha256" "$HP/k1_scripts.sha256" > "$HP/k1.sha256"; grep -c . "$HP/k1.sha256"
```

Block T6 of the `paper.md` that `table6_human.py` compares with must equal block T6 of the transferred draft, or a PASS would be against a text that is not going forward (CC-420 ruling 7 step 3):

```bash
git -C "$PB" show HEAD:paper/rev_2026-11-15/paper.md > "$HP/k1_rev_paper.md"
python3 -I - "$REPO/$(grep -o -E '[^ ]+/paper\.md$' "$HP/k1_inputs.sha256")" "$HP/k1_rev_paper.md" << 'PY'
import sys
def t6(path):
    ls = open(path, encoding="utf-8").read().splitlines()
    s = [i for i, l in enumerate(ls) if "id=T6" in l and l.startswith("<!-- @P")]
    assert len(s) == 1, path
    out = []
    for l in ls[s[0] + 1:]:
        if l.startswith("<!-- @P"):
            break
        if l.startswith("|"):
            out.append(l)
    return out
a, b = t6(sys.argv[1]), t6(sys.argv[2])
print(f"T6 rows {len(a)} and {len(b)}:", "EQUAL" if a == b else "DIFFERENT")
sys.exit(0 if a == b else 1)
PY
```

Today: 29 and 29 rows, EQUAL (held draft_v3 cb462dfc against rev_2026-11-15 aeeaa016). DIFFERENT: STOP for K1; the script goes back to its author. The list holds 4 inputs and 4 scripts (8 lines). `k1_list.py` sees only inputs named by `*_REL`/`*_SHA` constants; `figEF1.py` names its inputs otherwise, so `build_all_v2.sh`, `fig1_schematic.py` and `figEF1.py` go to the host only under an addendum to CC-425.

**P3. K2 inputs** (after the draft agent has finished: copy only when its writer is done, hash twice equal (P3 and P7), keep a 444 copy; CC-410 ruling 7(b)):

```bash
D=$REPO/manuscript/conf_taimma_2027/draft_v3_1; K=$HP/k2; mkdir -p "$K/src"
sha "$D/paper.md" | tee "$HP/k2_draft_first.sha"                     # first hash; the second is taken at P7
git -C "$PC" show HEAD:paper_v1_analysis/paperC.bib > "$K/src/paperC.bib"
git -C "$PC" show HEAD:paper_v1_analysis/tex/strip_num.lua > "$K/src/strip_num.lua"
sha "$K/src/paperC.bib"; sha "$K/src/strip_num.lua"                 # a415c4da..., 5a91751f... today; another value is recorded, not a stop
J=$REPO/.session_backup/2026-11-15
for v in base k1 k1k2; do cp -r "$D" "$K/d_$v"; chmod -R u+w "$K/d_$v"; done
python3 -I "$HP/scripts/k2_cuts.py" "$K/d_k1" k1
python3 -I "$HP/scripts/k2_cuts.py" "$K/d_k1k2" k1 && python3 -I "$HP/scripts/k2_cuts.py" "$K/d_k1k2" k2
for v in base k1 k1k2; do (cd "$K/d_$v" && python3 -I -B check_draft.py --sync-first-words \
  && python3 -I -B check_draft.py --build-manifest "$REPO/manuscript/conf_taimma_2027/WRITING_PLAN_C_TAIMMA_v1.md" > "../check_$v.bm.txt" \
  && python3 -I -B check_draft.py > "../CHECKS_$v.md"; echo "checker $v rc $?"); done   # all rc 0, 12 PASS and 1 INFO
for v in base k1 k1k2; do python3 -I "$HP/scripts/k2_prep.py" "$J/host_prep_build/j3/build_lncs.sh" "$J/host_prep_build/j3/lncs.lua" \
  "$J/taimma_build/in_as_run/lncs_preamble.tex" "$K/d_$v/paper.md" "$K/src/paperC.bib" "$K/src/strip_num.lua" "$K/push" "$v" \
  $( [ $v = base ] && echo vi ); done
cat "$K"/push/in_*.sha256 > "$HP/k2.sha256"; grep -c . "$HP/k2.sha256"        # 7 folders x 6 files = 42
chmod -R a-w "$K"
```

- The writing plan read by `--build-manifest` is the one of REVISION_NOTES_V3_1 §3: `sha WRITING_PLAN_C_TAIMMA_v1.md` must begin 0d4cb1079110655f; another value: STOP and ask its writer.
- The checker run on the k1 and k1k2 copies (tested on 15 Nov: rc 0, 12 PASS, 1 INFO, 72 units, 344 numeric tokens) is the "checker in its three modes" that CC-421 asks for every k step. Any rc other than 0: that variant is not pushed.
- Expected shas today (from b42eecb1): `in_base/paper.md` b42eecb1, `in_k1/paper.md` 170e4e8a..., derived `build_lncs.sh` 8e29e0d43d906489a3b330877a263592c1d3877f3c5afa29c35c1c60aefa1ff5, base preamble b2f6806a3d67d6e6ed257f82a22fa04f0e697ff9b79dc4be59d31374a25552e2, dummy preamble 3aea17b1091ddaefbe04e253e3dae46c07435720ecc99875eb01486c5cb4ed02. A changed draft changes the paper.md shas only.
- The dummy text exists only in `$HP/k2/push/in_*_dummy`, `in_base_vi` and the pulled records. **It never enters a draft folder** (CC-421 Ruling 5); `k2_cuts.py` refuses to write inside `conf_taimma_2027/`.

**P4. K3 source** only when section 4.3's precondition holds (otherwise skip P4):

```bash
C=$(git -C "$PC" rev-parse HEAD); T3=$HP/k3_src_$(echo $C | cut -c1-7).tar
git -C "$PC" archive --format=tar -o "$T3" "$C" -- paper_v1_analysis
[ "$(git get-tar-commit-id < "$T3")" = "$C" ] && echo "tar is of $C"; tar -tf "$T3" | grep -vc '/$'; sha "$T3"
for f in tex/build.sh tex/preamble.tex tex/strip_num.lua tex/fig1_forest.py; do echo "$(tar -xOf "$T3" paper_v1_analysis/$f | sha256sum | cut -c1-16)  $f"; done
#   -> 33eb75db8cfcad28 0c9c2819657638a9 5a91751fc1daf5a0 c7d168caa9e56e8e; any other value: STOP for K3 (j2_host_build.sh pins them;
#      a new pin is a byte change of that script with its own read)
```

**P5. K4 source** (allow-list: exactly what the two scripts read; no manifest, provenance table, plan, brief or fix package):

```bash
CA=$(git -C "$PA" rev-parse HEAD); T4=$HP/k4_src_$(echo $CA | cut -c1-7).tar
git -C "$PA" cat-file -e "$CA:paper/build/build_A_supp.sh" || echo "STOP: no build_A_supp.sh at HEAD (K4 skipped)"
git -C "$PA" archive --format=tar -o "$T4" "$CA" -- paper/build paper/figs 'paper/sec*.md' paper/abstract_A.md paper/title_page_A.md \
  paper/declarations.md paper/paperA.bib paper/intext_trace_A.tsv paper/supplementary_SPIC.md paper/highlights_A.md
[ "$(git get-tar-commit-id < "$T4")" = "$CA" ] && echo "tar is of $CA"; tar -tf "$T4" | grep -vc '/$'; sha "$T4"
for f in build/build_A_cas.sh build/build_A_supp.sh; do echo "$(tar -xOf "$T4" paper/$f | sha256sum | cut -c1-16)  $f"; done   # fa54fa4e2d57c985, e3a4cab2a1d4a5d2 today
mkdir -p "$HP/k4/pin"; cp $REPO/.session_backup/2026-10-27/builds/A_cas/cas-common.sty "$HP/k4/pin/"
cp "$HP/scripts/k4_run.sh" "$HP/scripts/k_counts.sh" "$HP/k4/"
(cd "$HP/k4" && sha256sum pin/cas-common.sty k4_run.sh k_counts.sh) > "$HP/k4.sha256"; head -1 "$HP/k4.sha256" | cut -c1-16   # e95a01f4b33531d0
```

The pinned `cas-common.sty` in `$OUT` makes `build_A_cas.sh` skip its fetch from `mirrors.ctan.org` (l.22-23 of the script), an address that CC-410 ruling 5 does not list. HEAD a7f2b4e is the source today; a later HEAD is named in the K4 line.

**P6. K5**: nothing, unless section 4.5's precondition holds.

**P7. Before renting.** `sha "$REPO/manuscript/conf_taimma_2027/draft_v3_1/paper.md"` equals `$HP/k2_draft_first.sha` and `$HP/k2/push/in_base/paper.md` (otherwise redo P3); `k1_list.py` of P2 run again with the same output; the D1 line is on the LOG; a fresh panel read; the newest STATE file shows no live rental; this plan's prep OPS line (section 7, line 1) is written. The 30-minute host backup loop is not started for this host (nothing on it needs it; the pulls of section 4 are the copies).

---

## 3. Host session start

1. **Offer and rent** (skill l.13-25; GPU_RENTAL_SPEC): 1x RTX 3090 / 3090 Ti 24 GB; CPU at least Ryzen 7 5800XT class; RAM >= 32 GB; disk >= 200 GB at >= 1000 MB/s; network >= 400 Mbps; CUDA >= 12.4; uptime > 99 %; max rental time >= 3 h plus margin. Cheapest offer that passes every field (15 Nov: 84966 and 89528 with a 5950X at 9,185 VND/h; 76866 has a 3950X; 106263 is the FAULT machine of CC-302, excluded). Ubuntu 24.04 template; random password in a 0600 file; L-before (section 1.3); the `date -u` stamp of the click is **T0**.
2. **Access.** `Host hE` (the alias of section 2) in `~/.ssh/config` only; `ssh-copy-id` through an askpass script; BatchMode login works.
3. **Facts** (skill l.27): nvidia-smi, lscpu, free, df of `/dev/shm` and home, 4 GB `dd` with direct I/O, OS version, clock skew < 60 s. A fact against the offer is a FAULT: delete; the money counts.
4. **System packages, all before step 6** (CC-410 N3; PI-1115r: the host is a fresh image, so missing system libraries are expected): the install bundle `scripts/host_bundle/`, profile `pdf` (K2 to K5; it includes `base`, which covers K1b and every package of the 15 Nov list), no Java. Push its two files, check their shas, install, and read the verification table:

```bash
tar -C "$REPO/scripts" -cf - host_bundle/SYSTEM_PACKAGES.txt host_bundle/install_system.sh | ssh -o BatchMode=yes "$H" 'tar -xf - --no-same-owner -C /root'; echo "tar ${PIPESTATUS[0]} ssh ${PIPESTATUS[1]}"
(cd "$REPO/scripts" && sha256sum host_bundle/SYSTEM_PACKAGES.txt host_bundle/install_system.sh) | ssh -o BatchMode=yes "$H" 'cd /root && sha256sum --quiet -c - && echo "bundle OK"' 2>&1 | F
S 'bash /root/host_bundle/install_system.sh pdf > /root/bundle_install.txt 2>&1; echo "bundle rc $?"; sed -n "/^CHECK /,\$p" /root/bundle_install.txt | tr . _'
```

   - rc 0 (`VERIFY CLEAN`): go on to step 5. The private-tool rows say `skip` here (the setup has not run yet); that is expected.
   - rc 1: install the packages that the `MISSING` lines name (`apt-get install -y --no-install-recommends <package>`), then `S 'bash /root/host_bundle/install_system.sh --verify pdf'` once. Still not clean: K2 to K5 drop out; K1b continues if every `base` row is clean; pull and delete.
   - The table (dots as underscores) goes into the facts-and-packages OPS line; its `apt idle` row replaces the `pgrep` check. Every package added by hand is named in that line and goes into `SYSTEM_PACKAGES.txt` after the session (`scripts/host_bundle/README.md`).
   - No apt call of any kind after step 6 starts (the private `apt-get download` of the setup script included, which runs inside step 6), except the one recovery install of section 6.4.
5. **Push the tools** (form of `J2_RUN.md` §2):

```bash
S 'test ! -e /root/paperC_build && mkdir -p /root/paperC_build && echo "build folder made"' || echo "STOP: /root/paperC_build exists"
tar -C "$HP/tools" -cf - $(cut -c67- "$HP/tools.sha256") | ssh -o BatchMode=yes "$H" 'tar -xf - --no-same-owner -C /root/paperC_build'; echo "tar ${PIPESTATUS[0]} ssh ${PIPESTATUS[1]}"
ssh -o BatchMode=yes "$H" 'cd /root/paperC_build && sha256sum --quiet -c - && echo "tools OK: $(find . -type f | wc -l) files"' < "$HP/tools.sha256" 2>&1 | F    # 11
```

6. **Tool setup in tmux** (CC-410 N2), with `aliascnt` added because 15 Nov's first LNCS build stopped on it (`taimma_build/RECORD.md`):

```bash
S 'tmux new-session -d -s tools "bash /root/paperC_build/run_setup.sh" && echo started'
# wait with a background until-loop (skill l.50): until ! S 'tmux has-session -t tools 2>/dev/null'; do sleep 15; done
S 'echo "setup rc $(cat /root/paperC_build/rec/setup.rc)"; tail -n 25 /root/paperC_build/rec/setup_out.txt'
```

   - rc 0: tools present for K2 to K5 ("SETUP OK (J2 and J3)"). rc 3: LNCS class missing: K2 only takes the fallback of CC-410 J3-4. rc 9: STOP line at the end of the output; if it names a missing library or package, section 6.4 allows one recovery install and one re-run of the unchanged setup.
   - Read every `DRIFT` line: the TinyTeX bundle is a daily release; drift is reported, never forced back (CC-410 J2-1). Addresses as CC-410 ruling 5: pandoc 3.5 (pinned a46b448a), installer READ only (sha da22ffb5 on 13 and 15 Nov), bundle at the address the installer names. Anything else: STOP; K2 to K5 drop out.
   - `bash /root/paperC_build/host_tex_setup.sh outside` must show 0 for `/var/cache/fontconfig`.
7. **K1b runs beside step 6** (section 4.1b): separate folder, CPU light. K1 (section 4.1) ran on 2026-11-15 and is not run again.

OPS lines: rental (T0, offer, L-before numbers, spec facts, D1 line id; no host string); facts and packages; tools (setup rc, bundle sha and DRIFT lines, outside counts).

---

## 4. The jobs

Order on the host: K1b (beside the tool setup), **K2** (first after the setup: PI-1115a), K4, K5, and K3 only when the precondition of section 4.3 holds. Each job ends with its pull before the next starts. Pull form for every job (sha on both sides, then an address and host-name count before anything is unpacked on the laptop; CC-410 N4 for hits in binary files):

```bash
pull() {  # pull <host dir> <tar name> <laptop dir> <paths inside the host dir...>
  local d=$1 t=$2 l=$3; shift 3; mkdir -p "$l"
  S "cd $d && n=\$(grep -r -l -a -E '([0-9]{1,3}\.){3}[0-9]{1,3}' $* 2>/dev/null | wc -l); h=\$(grep -r -l -a -i -F -e \"\$(hostname)\" $* 2>/dev/null | wc -l); echo \"address-like files \$n, host-name files \$h\"; tar -cf $t $* && sha256sum $t | cut -c1-64"
  ssh -o BatchMode=yes "$H" "cat $d/$t" > "$l/$t"; sha "$l/$t"            # equal to the line above
}
```

A non-zero address count: for each hit file, `for a in $(hostname -I); do grep -a -c -F "$a" FILE; done` on the host; all 0 means a version string or a DOI, not the host: say so in the record (CC-410 N4). A non-zero host-name count: STOP, read the hit on the host by counts, no pull until 0. The tar is unpacked on the laptop with `tar -xf ... --no-same-owner`, then `chmod -R a-w`.

The laptop record folder of the session: `SB=$REPO/.session_backup/<UTC date of T0>/host_session_$H/` with one sub-folder per job.

### 4.1 K1: Paper B Table 6 and figures

| | |
|---|---|
| Inputs | `$HP/k1.sha256` (P2): the scripts of `scripts/b_figs/` and every file their constants name, each equal to its pin |
| Requirement | one pinned line, `matplotlib==3.10.9` (the only version on record: `.session_backup/2026-10-21/gpu_m3/pip_freeze.txt`). No hashed lock exists; this run writes `wheels.sha256` and `freeze.txt`, which become the lock of later runs (section 8) |
| BUILD.json on a host | It was on the never-on-host list of the stage-H host (CC-388 ruling 4; plan of 15 Nov C10) while the labels were held. It holds counts and sha256 values only (keys `counts`, `inputs_sha256`, `outputs_sha256`; read as key names only for this plan), it is committed (5eee5e3), the closing line is past and CC-418 released Paper B custody; CC-420 ruling 7 step 3 names it as an input of Table 6 |
| Time | 3 to 6 min (venv and wheel download 1 to 3 min; builds seconds) |

```bash
S 'test ! -e /root/k1 && mkdir -p /root/k1/repo && echo "k1 folder made"' || echo "STOP: /root/k1 exists"
(cd "$REPO" && tar -cf - $(cut -c67- "$HP/k1.sha256")) | ssh -o BatchMode=yes "$H" 'tar -xf - --no-same-owner -C /root/k1/repo'; echo "tar ${PIPESTATUS[0]} ssh ${PIPESTATUS[1]}"
ssh -o BatchMode=yes "$H" 'cd /root/k1/repo && sha256sum --quiet -c - && echo "k1 inputs OK: $(find . -type f | wc -l) files"' < "$HP/k1.sha256" 2>&1 | F
ssh -o BatchMode=yes "$H" 'cat > /root/k1/k1_run.sh' < "$HP/scripts/k1_run.sh"; S "[ \"\$(sha256sum /root/k1/k1_run.sh | cut -c1-64)\" = $(sha "$HP/scripts/k1_run.sh") ] && echo 'runner OK'"
S 'tmux new-session -d -s k1 "bash /root/k1/k1_run.sh" && echo started'
# wait (background until-loop) for: ! tmux has-session -t k1
S 'cd /root/k1/rec && for f in venv selftest build; do echo "$f rc $(cat $f.rc 2>/dev/null || echo none)"; done; cat build_script.txt python.txt; grep -E "^(input|output) " build.txt'
pull /root/k1 k1.tar "$SB/k1" rec repo/scripts/b_figs/out
```

- **Pass:** venv rc 0, selftest rc 0, build rc 0; every `input <name> sha256 ... ok` line names a pinned input; every figure has a vector file and a 600 dpi PNG (the scripts' `save()`); `table6_human.py` exits 0 (any cell that differs from block T6 is a FAIL by design).
- **Fail:** selftest rc 8 or build rc not 0: reported with the record, not patched on the host; the scripts go back to their author.
- **After the pull (laptop):** copy the files of `out/` into `paper/rev_2026-11-15/figures/` of the Paper B repo with a sums file, unstaged (CC-420 ruling 7 step 3: the transfer commit 568eaec exists, so rule 7 of the specification no longer applies). Then the one-judge DIFF read; the gatekeeper commit only after it.
- **Custody:** released (CC-418); the coordinator may view the outputs. No label, key, assignment, practice file, `PAIR_CANDIDATES.json` or caption text goes to the host (section 5.1).
- OPS line: inputs list sha, script used, freeze and wheel-list sha, Python version, three rc values, output sha list, pull tar sha, where the copies went.

### 4.1b K1b: Paper B Fig. EF1 and Fig. 1 (CC-428 ruling 4)

| | |
|---|---|
| Ruling | CC-428 (CC sha ab98dc743c8b2c92714bcc9745cf9cb21ea254dfe556f5b9ce9be16b88b2261e), ruling 4 (a) to (f); W1, W2 and W3 close before the push |
| Inputs | `$HP/k1b.sha256`: exactly the 12 files of ruling 4 (b), list sha 4559900b36be7a3d372fe36549da3fabccf03b8cab7fae2f133530ab3fea11e8; no other file of `b_work/`, no label, key or assignment file |
| Runner | `k1b_run.sh` = `k1_run.sh` with the folder `/root/k1b`, sha 8ed0cb65d480e634dbeba1124c9aca2590562ffffaec77aa63863ab3d0168e40 |
| K1 | not run again; its 2026-11-15 outputs (Fig. 2, Fig. 3, Table 6) are in `.session_backup/2026-11-15/host_session_hD/k1/` and stay the bytes of record for those three (ruling 4 (e)) |

The commands of CC-428 ruling 4 (c), as ruled (copied from the ruling, unchanged):

```bash
K1S="build_all_v2.sh fig1_schematic.py fig2_breaking.py fig3_human.py figEF1.py table6_human.py"
python3 -I "$HP/scripts/k1_list.py" "$REPO" $(for s in $K1S; do case $s in *.py) echo "$REPO/scripts/b_figs/$s";; esac; done) | sort -u > "$HP/k1b_inputs.sha256"; echo "k1_list rc ${PIPESTATUS[0]}"
(cd "$REPO" && sha256sum $(for s in $K1S; do echo "scripts/b_figs/$s"; done)) > "$HP/k1b_scripts.sha256"
cat "$HP/k1b_inputs.sha256" "$HP/k1b_scripts.sha256" > "$HP/k1b.sha256"; grep -c . "$HP/k1b.sha256"; sha "$HP/k1b.sha256"   # 12 and 4559900b..., else STOP
sed 's#^K=/root/k1; #K=/root/k1b; #' "$HP/scripts/k1_run.sh" > "$HP/scripts/k1b_run.sh"; sha "$HP/scripts/k1b_run.sh"      # 8ed0cb65d480e634dbeba1124c9aca2590562ffffaec77aa63863ab3d0168e40 (one line differs: the folder)
# the T6 check of P2 again, against Paper B HEAD (6356b99, paper.md bfce87e9): 29 and 29 rows, EQUAL, else STOP
S 'test ! -e /root/k1b && mkdir -p /root/k1b/repo && echo "k1b folder made"' || echo "STOP: /root/k1b exists"
(cd "$REPO" && tar -cf - $(cut -c67- "$HP/k1b.sha256")) | ssh -o BatchMode=yes "$H" 'tar -xf - --no-same-owner -C /root/k1b/repo'; echo "tar ${PIPESTATUS[0]} ssh ${PIPESTATUS[1]}"
ssh -o BatchMode=yes "$H" 'cd /root/k1b/repo && sha256sum --quiet -c - && echo "k1b inputs OK: $(find . -type f | wc -l) files"' < "$HP/k1b.sha256" 2>&1 | F
ssh -o BatchMode=yes "$H" 'cat > /root/k1b/k1b_run.sh' < "$HP/scripts/k1b_run.sh"; S "[ \"\$(sha256sum /root/k1b/k1b_run.sh | cut -c1-64)\" = $(sha "$HP/scripts/k1b_run.sh") ] && echo 'runner OK'"
S 'tmux new-session -d -s k1b "bash /root/k1b/k1b_run.sh" && echo started'
# wait for: ! tmux has-session -t k1b
S 'cd /root/k1b/rec && for f in venv selftest build; do echo "$f rc $(cat $f.rc 2>/dev/null || echo none)"; done; cat build_script.txt python.txt; grep -E "^(input|output|ruled|check|text) " build.txt; grep -c "^plotted " build.txt; grep -c "^plotted .* changed_F=True " build.txt'
pull /root/k1b k1b.tar "$SB/k1b" rec repo/scripts/b_figs/out
```

- **Pass:** CC-428 ruling 4 (d), every point.
- **Fail:** any FAIL line or rc not 0: reported with the record, not patched on the host.
- **After the pull:** CC-428 ruling 4 (e) and (f): the four new files into `paper/rev_2026-11-15/figures/` of the Paper B repo with the sums file, unstaged; the one-judge diff read before any commit; `build.txt` stays in the session record and is never committed to the paper repo.
- OPS line: as section 4.1, plus the CC-428 sha, the W1 and W2 sha match, the list and runner shas, and whether the Fig. 2 and Fig. 3 bytes equal those of K1 (information, not a failure).

### 4.2 K2: TAIMMA page measures (PROVISIONAL)

**What the count is.** Every K2 build of this session is **PROVISIONAL** (CC-421 Ruling 5: "The next build of v3 is PROVISIONAL like the last one"). It becomes the count of record (K2-R) only in a later session, when all of CC-410 ruling 7 (a) to (f) hold on the bytes after the re-join (CC-421 Ruling 7 S4 and S5): a closing CC names the paper.md sha, that sha is passed as the third argument of `build_lncs.sh`, and one judge has read the as-run build files (CC-410 J3-1; D3).

**Changes to the build files of 15 Nov (made by `k2_prep.py`, listed here for the record and for D3):**

| File | Change | Why |
|---|---|---|
| `build_lncs.sh` (ef21d602 -> 8e29e0d4) | input list without the SVG; no `rsvg-convert`; the figure check expects 0 figures; output sha list and the "does not cover" note without the figure; one new record line `last page fill` | CC-421 Option B removed the only figure: the 15 Nov script would stop with "not exactly one figure"; CC-421 Ruling 5 decides restores by the fill of the last page |
| `lncs_preamble.tex` (cdfe51a9 -> b2f6806a) | one line before `\begin{document}`: `\AtEndDocument{\par\penalty0\typeout{LASTPAGE-FILL ...}}` | measure only: writes the height used on the last page to the log; adds no box, glue or break (tested on the laptop in a scratch folder: same PDF text and page count with and without the line) |
| dummy preamble (-> 3aea17b1) | the placeholder `\institute{...}` line replaced by two dummy institutes with full addresses and three `example.org` e-mails | CC-421 Ruling 5 dummy measure |
| dummy `paper.md` | four placeholders replaced: three dummy authors with `\inst`; one dummy licence entry for each of the six data sets of DECL-02; a three-line acknowledgment; a two-line interests statement | same; the two other bracketed notes of the end sections are left as they are |
| `_vi` variant | the same, with Vietnamese letters in the three dummy names | probe of CC-410 N5 (pdflatex with T1 cannot set them; the real author block has them) |

**Variants built (7 folders x 2 layouts = 14 builds):** `base` (the draft as it is), `k1` (base with cut k1), `k1k2` (with k1 and k2), each plain and `_dummy`, plus `base_vi`; each in the default layout and with `END_SECTIONS=starred`.

```bash
S 'test -d /root/paperC_build && test ! -e /root/paperC_build/taimma && mkdir /root/paperC_build/taimma && echo "folder made"' || echo "STOP"
tar -C "$HP/k2/push" -cf - $(cut -c67- "$HP/k2.sha256") | ssh -o BatchMode=yes "$H" 'tar -xf - --no-same-owner -C /root/paperC_build/taimma'; echo "tar ${PIPESTATUS[0]} ssh ${PIPESTATUS[1]}"
ssh -o BatchMode=yes "$H" 'cd /root/paperC_build/taimma && sha256sum --quiet -c - && echo "k2 inputs OK: $(find . -type f | wc -l) files"' < "$HP/k2.sha256" 2>&1 | F    # 42
ssh -o BatchMode=yes "$H" 'cat > /root/paperC_build/k2_run.sh' < "$HP/scripts/k2_run.sh"; S "[ \"\$(sha256sum /root/paperC_build/k2_run.sh | cut -c1-64)\" = $(sha "$HP/scripts/k2_run.sh") ] && echo 'runner OK'"
S 'bash /root/paperC_build/k2_run.sh; cat /root/paperC_build/taimma/K2_RC.txt /root/paperC_build/taimma/K2_SUMMARY.txt'
pull /root/paperC_build/taimma k2.tar "$SB/k2" K2_RC.txt K2_SUMMARY.txt 'in_*' 'out_*'   # quoted: the globs expand on the host
```

`build_lncs.sh` returns 0 (built, three zero counts), 1 (built, a count not 0) or 9 (STOP, with the last 30 log lines in `out_*.console`). Expected: rc 0 for the six non-vi folders; `base_vi` will probably stop with "Unicode character ... not set up" (a finding, section 8 item 5). Time: about 1 to 3 min (15 Nov: about 1 s per build) plus push and pull.

**Reading the summary: my reading of CC-421 Rulings 5 and 6(e), stated as mine.** The count that decides is the **larger of the two dummy-filled builds** (default and starred) of a variant: the dummy text stands for the investigator's own text, and Ruling 6(e) wants both layouts at 15 or fewer until one is chosen. The plain builds are recorded beside it and decide nothing. Then, in the ruled order:

| Deciding count of `base_dummy` | Next step (none is taken on the host; the host only measures) |
|---|---|
| <= 15 | No cut. Restore check: the ruled restores r1 to r4 need "15 pages with the last page at most 0.6 full after the restore". This session has no restore text (no exact pairs exist), so it records the fill of the last page of `base_dummy`, both as `LASTPAGE-FILL` (pt of `\textheight`) and as the ratio of non-empty lines on the last and the previous page; the two must agree within about 0.1 before either is used. The restore texts r1, r2, r3, r4 (in that order) go to the writer and are measured in the next session |
| > 15 | **k0 comes first and is not mechanical** (fix the overfull boxes, no heading alone at a page foot; class as released, Ruling 6(d)): STOP and report; a layout agent works from the pulled PDFs on the laptop, and k0 is measured in the next session. The `k1` and `k1k2` builds of this session are **information for that decision**, not steps taken: once k0 is done, the first of k1, k1+k2 whose deciding count is <= 15 is the step to apply on the laptop (the measured counts without k0 are an upper bound only if k0 does not lengthen the text; that is checked by measuring again) |
| `k1k2_dummy` still > 15 | k3 (the per-arm table, renumbering, constants, the dagger note re-worded at the re-check) is not mechanical: STOP and report. After k3, still over 15: ESCALATE to the investigator (Ruling 5). No plan A.5 row, registered negative, label, sensitivity, post hoc row, Section 7 bullet, compute line or declaration is cut for length, by anyone |

Each k or r step that is later applied to the draft goes through the checker in its three modes and into the build's log line (Ruling 5), as P3 does for the copies.

- OPS line (the PROVISIONAL note; never "G1"): draft sha (hashed twice), the six other input shas, the two derived file shas and their diff against the 15 Nov bytes, one row per build (pages, reference start page, fill, line ratio, the three zero counts, overfull count over 5 pt), the deciding count of each variant by the rule above, the `base_vi` result, the record sha.

### 4.3 K3: Paper C journal tex/PDF (step 7 of the chain runbook)

**Run only if all hold, else skip with one NOT RUN line:** (1) `date -u` is at or after 2026-11-16T05:00:00Z; (2) the LOG holds the gatekeeper commit lines of the freeze shell C2 and, after it, of the fix packages v2 (CC-408), v4 (CC-413) and v5 (CC-423, "fourth step after the freeze shell, CC-408 and CC-413"); (3) Paper C HEAD equals the commit of the last of those lines. These are steps 1 to 6 of the runbook `manuscript/fix_packages/2026-11-15_C/CHAIN_REHEARSAL_2026-11-15.md` (3f19f129e30dc862dc84d0d33a6020ef6cc9f6a46038b7a8d1c4bc7f3ec68ac8); K3 is its step 7 ("Build from the paper-repo HEAD after step 6, as in the J2 precedent"). If (2) holds only for part of the chain, the build is a toolchain run as on 15 Nov: built and pulled, not copied. While the chain is under way (C2 to step 6), no build agent touches the paper repo (runbook risk 8: "Commits from the conference-version or build agents must wait until step 6 is committed").

Inputs: the tar of P4 (42 files today; the four pinned tex inputs checked there). Tools: those of step 6 (already on the host).

```bash
ssh -o BatchMode=yes "$H" 'cat > /root/paperC_build/src.tar' < "$T3"
S "[ \"\$(sha256sum /root/paperC_build/src.tar | cut -c1-64)\" = $(sha "$T3") ] && test ! -e /root/paperC_build/src && mkdir /root/paperC_build/src && tar -xf /root/paperC_build/src.tar --no-same-owner -C /root/paperC_build/src && echo 'source OK'"
S 'tmux new-session -d -s k3 "bash /root/paperC_build/j2_host_build.sh > /root/paperC_build/rec/k3_console.txt 2>&1; echo \$? > /root/paperC_build/rec/k3.rc" && echo started'
# wait for: ! tmux has-session -t k3
S 'echo "host script rc $(cat /root/paperC_build/rec/k3.rc)"; tail -n 5 /root/paperC_build/rec/k3_console.txt'     # last line: J2 HOST CHECKS: PASS or FAIL
```

Then `J2_RUN.md` §5 (pull of `tex_out.tar` and `rec_out.tar`, equal on both sides; "laptop copy = host list"), §6 (laptop checks with `check_610.py` on the commit's own `06_results.md`) and §7 (working-tree copy, only when HEAD = C at that moment; unstaged), with `C` and `D=$SB/k3`.

- **Pass (plan of 15 Nov l.186):** `build.rc` 0; 0 undefined references and citations in both final-pass logs; 0 "??" in both PDFs; the four inputs unchanged; the 6.10 check PASS. The freeze chain may change the 6.10 headings: a FAIL there is a finding, reported and not patched, and nothing is copied (CC-410 J2-5).
- **Read from the build log** (runbook step 7): CC-408 N4, the fonts of the Vietnamese template cells and the `{i}`/`{caption}` braces surviving pandoc; CC-423 N5, the Table 1 box in italic code font. Paper C holds nothing back, so the logs and PDFs may be read directly.
- **Not committed and not staged** (runbook step 7 and "Never stage": `paper_v1_analysis/tex/` and `docs/CC309_PARAGRAPH_DRAFT.md`; never `git add -A`, `git add .`, `git commit -a` or a bare `git diff` for a record). The working-tree copy of J2_RUN §7 is allowed. This follows the runbook, which is newer than CC-410 J2-0 ("the commit of generated files waits for the rebuild after C2 + v2, with its own diff read"); whether the generated files are ever committed is for a judge, not for this session. Drift of TeX package revisions goes with that later read (VERSIONS_COMPARE.txt; CC-410 J2-1).
- Time: about 3 min (15 Nov: build 30 s).
- OPS line: commit, tar sha, chain lines it follows, rc, pages and words of main and supplement, the counts, 6.10 result, the two log reads (CC-408 N4, CC-423 N5), pull tar shas, working-tree copy yes or no, nothing staged.

### 4.4 K4: Paper A main and supplement PDFs (counts only; outputs held)

Precondition: `build_A_supp.sh` at Paper A HEAD (true at a7f2b4e). The source holds the held zones, so **nothing of this job's output is shown**, only `K4_COUNTS_<n>.txt` (section 5.2).

```bash
S 'test ! -e /root/k4 && mkdir -p /root/k4/src && echo "k4 folder made"' || echo "STOP: /root/k4 exists"
ssh -o BatchMode=yes "$H" 'cat > /root/k4/src.tar' < "$T4"
S "[ \"\$(sha256sum /root/k4/src.tar | cut -c1-64)\" = $(sha "$T4") ] && tar -xf /root/k4/src.tar --no-same-owner -C /root/k4/src && echo 'source OK'"
tar -C "$HP/k4" -cf - pin/cas-common.sty k4_run.sh k_counts.sh | ssh -o BatchMode=yes "$H" 'tar -xf - --no-same-owner -C /root/k4'
ssh -o BatchMode=yes "$H" 'cd /root/k4 && sha256sum --quiet -c - && echo "k4 helpers OK"' < "$HP/k4.sha256" 2>&1 | F
S 'tmux new-session -d -s k4 "bash /root/k4/k4_run.sh 1" && echo started'
# wait for: ! tmux has-session -t k4
S 'cat /root/k4/rec_1/K4_COUNTS_1.txt'      # the ONLY output of K4 that is displayed
KH=$HOME/k4_held_$(date -u +%F); pull /root/k4 k4_1.tar "$KH" rec_1 out_main_1 out_supp_1; chmod 700 "$KH"; chmod 400 "$KH/k4_1.tar"   # home side, where modes hold; the tar is NOT unpacked; only the counts shown above and the tar sha go into $SB/k4
```

- `K4_COUNTS_<n>.txt` gives, per PDF: pages; undefined references or citations; Missing character; overfull hbox count, those over 10 pt, overfull vbox, underfull; lines with "??"; then each overfull box as its size and source line numbers only (`k_counts.sh` cuts every line after the line numbers); the dataset-tag count; whether `highlights_A.docx` exists; the heading numbers of both `.tex` files with their line numbers (no title text), so that a box or an error can be placed in or out of the held zones by its line number alone. Reference values of CC-422 N6 (laptop builds by the package agent): main 38 and 39 pages, supplement 151 and 158 pages, 17 and 72 overfull boxes.
- **Pass:** both rc 0 and both PDFs present; undefined 0, Missing character 0, "??" 0 in both; dataset tags present; docx present. Overfull boxes and pages are recorded, not judged here.
- **Fail:** rc not 0 or no PDF: the reason is in the held console files; a non-PI-facing agent reads them and reports as section 5.2 says (counts, line numbers, error classes and package names only). Missing TeX package: private `tlmgr install <name>` with a record line, then one rebuild as attempt 2 (`k4_run.sh 2`, new folders; the script refuses existing ones); no system package.
- TeX packages: the laptop's 186 installed packages, with which the package agent built both PDFs (CC-422 N6), are all in the 189 of the 15 Nov host (`c_tex_build/tl_pkgs_installed_rev.txt`; only the platform entry of texlive.infra differs), so no package is expected to be missing.
- Time: 5 to 20 min (xelatex, about 200 pages in all, three to five passes each; no record of a host build exists).
- OPS line: commit, tar sha (file count), helper shas, rc values, the counts of `K4_COUNTS_<n>.txt` (numbers only), the held folder and the pull tar sha. No text fragment of any log.

### 4.5 K5: Paper B Springer build (`build_B_rev.sh`, CC-426 ruling 8 and CC-425 addendum A3)

| | |
|---|---|
| Script | `paper/build/build_B_rev.sh` d671b9d2c637d5dec5d4fe85e93e38275b2e92bc167fc3601435f7f88f25ed2a at Paper B HEAD 6356b99 (equal to the sha CC-426 names) |
| Runs only if | the four conditions of CC-425 addendum A3 hold at the push: (1) CC-426 on the LOG with GO or CONDITIONAL GO naming the script by sha, its blocking items on the script closed; (2) the script at HEAD has that sha; (3) the coordinator line extending OPS-1115ba to K5; (4) the host is inside its cap and K4 has been pulled. Otherwise one NOT RUN line |
| Allow-list | the eight pathspecs of the `git archive` line below (CC-425 A3; the inputs CC-426 ruling 8 names) |
| Needs | pandoc, latexmk with xelatex, pdfinfo, python3, the DejaVu Serif font (CC-426 ruling 8): the private tool tree of section 3 step 6 (TeX package `dejavu` is in its list) |
| Return code | 0 also when a PDF fails: K5 reads `report.txt` (page lines, "NOT BUILT") |

The commands of CC-425 addendum A3, as ruled (copied from the ruling, unchanged):

```bash
CB=$(git -C "$PB" rev-parse HEAD); T5=$HP/k5_src_$(echo $CB | cut -c1-7).tar
git -C "$PB" archive --format=tar -o "$T5" "$CB" -- paper/build paper/paperB.bib paper/citation_map_B.tsv paper/supplementary_B.md paper/rev_2026-11-15/paper.md paper/rev_2026-11-15/online_resource.md paper/rev_2026-11-15/title_page.md paper/rev_2026-11-15/cover_letter.md
[ "$(git get-tar-commit-id < "$T5")" = "$CB" ] && tar -xOf "$T5" paper/build/build_B_rev.sh | sha256sum | cut -c1-64     # must equal the sha named by CC-426, else K5 NOT RUN
S 'test ! -e /root/k5 && mkdir -p /root/k5/src /root/k5/rec && echo "k5 folder made"' || echo "STOP: /root/k5 exists"
ssh -o BatchMode=yes "$H" 'cat > /root/k5/src.tar' < "$T5"
S "[ \"\$(sha256sum /root/k5/src.tar | cut -c1-64)\" = $(sha "$T5") ] && tar -xf /root/k5/src.tar --no-same-owner -C /root/k5/src && echo 'source OK'"
S 'tmux new-session -d -s k5 ". /root/paperC_build/env.sh; OUT=/root/k5/out_1 nice -n 19 bash /root/k5/src/paper/build/build_B_rev.sh > /root/k5/rec/console.txt 2>&1; echo \$? > /root/k5/rec/k5.rc" && echo started'
# wait for: ! tmux has-session -t k5
S '. /root/paperC_build/env.sh; echo "k5 rc $(cat /root/k5/rec/k5.rc)"; bash /root/k4/k_counts.sh /root/k5/out_1 paperB_LRE; cd /root/k5/out_1 && for n in 1 2; do echo "ESM_$n: $(pdfinfo ESM_$n.pdf 2>/dev/null | grep ^Pages || echo NOT BUILT)"; done; tail -n 12 report.txt'
pull /root/k5 k5.tar "$SB/k5" rec out_1
```

- A failure is reported with the record and not patched on the host, except one private TeX package with a record line and one rebuild into `out_2`.
- The output is a working build for the page count: nothing of it is committed; the count goes to the diff read of CC-420 ruling 7 step 3 with the K1 and K1b bytes. Custody released (CC-418): `report.txt` and the PDFs may be read.

---

## 5. Custody

### 5.1 Never pushed to the host

- `~/vsps_labels*`, `~/vsps_labels_b`, `~/.vsps_sealed`, any `key.json`, `assignment.json`, `practice.json`, any `*.jsonl` label file, any `gt_cache.json`, `PAIR_CANDIDATES.json`, `FAMILY.json`, `FEID.json`, `ITEMS_MANIFEST.tsv`;
- `LOG.md`, any `CC-*.txt`, STATE files, `RESPONSE_FROM_CORESSPONDING_AUTHOR*`;
- anything under `data/` (results, datasets, XM3600, KTVIC), any image, caption, reference or prediction file;
- held text: `A_FIX_PACKAGE_v1.md`, `A_CUT_PLAN_v1.md`, `ANNEX_FEID_held.md`, `ANNEX_NAMED_held.md`, any other file of `b_text_held/` than the one `paper.md` a K1 script pins, `b_result_snapshot`;
- the Paper A manifest, provenance table, plans and briefs (K4 pushes only its allow-list);
- any token or key (HF, OpenAlex, S2), any password.

Each push is a tar of a listed set checked by `sha256sum -c` on arrival; nothing is copied by folder.

### 5.2 Paper A held zones in K4

The K4 source contains Section 6.7 and S11. On the host and on the way back, the following are **held**: `rec_<n>/console_*.txt`, `out_*/report*.txt`, `out_*/A_cites_report.txt`, `*.log`, `*.tex`, `*.bbl`, `latexmk*.txt`, the PDFs and the docx. The build scripts' own terminal output (`tee report.txt`, which prints LaTeX warning excerpts and the source line after each overfull box over 10 pt) goes only to files on the host; no K4 command prints anything but rc values, file counts, sha values and `K4_COUNTS_<n>.txt`.

After the pull, the tar stays packed in `$KH` on the home side (folder 700, tar 400; under /mnt/d a chmod has no effect and every file reads 777), is never opened by the coordinator, and is never shown, linked or quoted to the investigator while the hold stands. Its LOG line carries numbers only. A reader of the build (for an overfull box or a failure) is a non-PI-facing agent who unpacks the tar in a 700 folder on the home side and reports only counts, `.tex` line numbers, LaTeX error classes and package names, with no word of the document from any section: the hold is wider than the two zones (CC-422 ruling 8). The PDFs are not copied into the paper repo (the build scripts write only to `$OUT`).

### 5.3 The other jobs

K1 and K5: Paper B custody released by CC-418. K2 and K3: Paper C and its conference version, nothing held. The K2 dummy text never enters a draft folder.

---

## 6. Order, parallel work, stop rules, end

### 6.1 Order

1. Laptop: P0 to P7 (section 2), the K1b laptop lines of section 4.1b, and the bundle check: `bash "$REPO/scripts/host_bundle/install_system.sh" --selftest` passes every check, and the sha256 of `SYSTEM_PACKAGES.txt` and `install_system.sh` equal those named in the licence line of the session.
2. Rent, access, facts, system packages (section 3 steps 1-4).
3. Tools push and setup in tmux; **K1b beside it** (K1 ran on 2026-11-15 and is not run again).
4. **K2**, then K4, then K5 (section 4.5: `paper/build/build_B_rev.sh` at Paper B HEAD 6356b99, CC-426 ruling 8 and CC-425 addendum A3), one after the other, each pulled before the next; K3 only once the Paper C freeze commits exist (runbook steps 1 to 6), else it moves to a later session.
   The session's job list is therefore K1b, K2, K4, K5, then K3 only after the Paper C freeze commits.
5. Leaving checks; delete; L-after; host clean-up (6.3).

### 6.2 Parallel

| At the same time | Allowed? |
|---|---|
| Tool setup + K1b venv and builds | yes: separate folders (`/root/paperC_build`, `/root/k1b`), CPU only, no shared file |
| Two TeX jobs (K2 to K5) | no: same tool tree and font cache; the time saved is minutes |
| Any apt-get after step 6 started | no, except the one recovery install of section 6.4; only private `tlmgr install` into the private TinyTeX, each with a record line (CC-410 J3-5) |

### 6.3 Leaving and deletion

```bash
S 'bash /root/paperC_build/host_tex_setup.sh procs; bash /root/paperC_build/host_tex_setup.sh outside; tmux ls 2>&1 | head -3'
```

Expected: 0 processes of the build folder, no tmux session. Every job's tar is on the laptop with equal shas. Then delete the instance on the panel as the next step, with no new job; check twice that the panel lists no instance and the host does not answer; L-after with the per-instance figure; then the laptop clean-up (PI-1115s): `bash "$REPO/scripts/host_bundle/cleanup_host.sh" "$H" --dry-run`, read the list, then the same command without `--dry-run`. It removes the alias's block in `~/.ssh/config`, its host keys (`ssh-keygen -R`) and any per-host known_hosts file, its control socket, and the askpass, password and pid files named after the alias; its last line is the text of the clean-up OPS line (names only, never an address). Kept: LOG lines and the session record folder (logs, sums, pulled results). No label, key or data file was ever on the host.

### 6.4 Stop rules

| Event | Rule |
|---|---|
| L-before fails | nothing is rented; the PI is asked at once |
| A host fact contradicts the offer | FAULT: delete; the money counts; a new rental needs its own L-before |
| Annex or input sha mismatch on the laptop (P0 to P5) | that job (P0: the whole plan) stops before the rental |
| Arrival check fails on the host | that job stops; the same file failing twice: STOP and read (skill l.39) |
| Setup rc 9 whose STOP line names a missing library or package ("a library is missing", `not found`) | one recovery install and one re-run of the unchanged setup, once per session (CC-431 ruling 3 is the judge line that CC-410 J3-5 asks for; never on a host that carries a stage-H job after its gate G0), with a DEVIATION line for each step: (1) wait until `tmux has-session -t tools` fails and `pgrep -x apt-get; pgrep -x dpkg` print nothing; (2) keep the first attempt's records: `S 'cd /root/paperC_build/rec && mv setup_out.txt setup_out_attempt1.txt && mv setup.rc setup_attempt1.rc && cp tl_pkgs_to_install.txt tl_pkgs_to_install_attempt1.txt && bash /root/paperC_build/host_tex_setup.sh outside > outside_attempt1.txt; cat outside_attempt1.txt'`; its line for `/var/cache/fontconfig` must say 0, else the first attempt itself wrote to the system font cache: no recovery, K2 to K5 drop out; (3) install: first `apt-get install -y --no-install-recommends` of each package the STOP output names that the list lacks (find the package on the laptop with `dpkg -S <library file>`; record each), then the install command of section 3 step 4 again with `/root/bundle_recovery.txt` as its output file; its table must say `VERIFY CLEAN` with every `private` and `TinyTeX` row `ok` (they are no longer `skip`: the first attempt unpacked the tools), else K2 to K5 drop out; (4) `S 'bash /root/paperC_build/host_tex_setup.sh outside > /root/paperC_build/rec/outside_after_install.txt; cat /root/paperC_build/rec/outside_after_install.txt; mv /root/paperC_build/marker_setup /root/paperC_build/marker_setup_attempt1'`: the counts since the first marker are on record and the re-run makes a new marker, so its font-cache check measures the re-run only; (5) re-run the unchanged setup once with the step 6 commands (`run_setup.sh` c4998685 and `host_tex_setup.sh` bf5294df, byte-equal); no `install_system.sh` call and no other system font lookup after this point. Setup rc 0 or 3: go on as section 3 step 6. Setup rc 9 again: K2 to K5 drop out; K1b continues; pull and delete |
| Setup rc 9 for any other reason, or an address outside CC-410 ruling 5 | K2 to K5 drop out; K1b continues; pull and delete |
| A job's rc is not 0 | report with the record; no patch on the host except a private TeX package; at most one rebuild in new folders; never a text change |
| A push stream stalls (under 50 KB/s for 10 min while a fresh probe runs 10 times faster) | stop it by pid, top up from a stdout-only list, DEVIATION line (skill l.35-39) |
| Expected wait for the next step > 10 min (D5) | pull what exists, delete |
| Host lost | the pulled tars are the record; skipped jobs go to the next session; a re-rental needs its own L-before and line (the stage-H advance licence PI-1114o does not cover this session) |
| Any K4 file would be shown | it is not; only `K4_COUNTS_<n>.txt` |
| Cap of 3 h reached | pull, delete; unfinished jobs go to the next session |

---

## 7. OPS lines (stamps from `date -u`, pipe form, no host string)

1. **prep**: `$HP` path; annex check (8 OK); tools list sha (11 files, setup script bf5294df); K1 list sha (n inputs, n scripts); K2 list sha (42 files), draft sha hashed twice, checker rc of base, k1, k1k2; K4 tar sha and commit; which jobs are skipped and why.
2. **rental**: T0, offer, rate, L-before with numbers, spec facts, D1 line id.
3. **facts and packages**.
4. **tools**: setup rc, bundle sha, DRIFT lines, outside counts.
5. **K1b** (section 4.1b; K1 ran on 2026-11-15).
6. **K2 PROVISIONAL** (section 4.2).
7. **K3** or **K3 NOT RUN** (which precondition failed).
8. **K4** (numbers only).
9. **K5 NOT RUN** (the script) or K5.
10. **leaving and deletion**, with L-after, block spend and the 50,000 VND check; then the host clean-up line (section 6.3, PI-1115s).
11. A STATE block for this rental (also still owed for hC: OPS-1115aq).

Never write, in any line, the literal string that the binding rules forbid in the LOG.

---

## 8. Owed and not found

| # | Item | Who |
|---|---|---|
| 1 | The D1 licence line (or the PI's yes) | coordinator |
| 2 | The one-judge read of D3 (Annex A and the K2 diff), recommended before renting; required before any K2-R line | one judge |
| 3 | `build_all_v2.sh` and the scripts for Fig. EF1 and Fig. 1 (FIGURE_TABLE_SPEC A3); which `paper.md` Table 6 is compared with after the transfer | the figure agent |
| 4 | A hashed lock for K1, written from this run's `freeze.txt` and `wheels.sha256` | the figure agent, after the run |
| 5 | The Vietnamese letters of the real author block under pdflatex T1 (CC-410 N5): if `base_vi` stops, a LAYOUT change (private `vntex` is in the TeX package list; a T5 font set-up) prepared on the laptop and measured in the next session, recorded as LAYOUT; never a change of the names | a build agent |
| 6 | Restore texts r1 to r4 as exact pairs (CC-421 Ruling 5) and the k0 layout lines, if the measures call for them | the conference-version writer; a layout agent |
| 7 | K2-R, the count of record on the post-re-join bytes (CC-421 S5), with the conditions of CC-410 ruling 7 | next session |
| 8 | K3 after the freeze chain (runbook step 7); whether its generated files are ever committed (the runbook says not staged; CC-410 J2-0 expected a commit after a diff read) | next session (T-a); one judge |
| 9 | The adapted Paper B Springer build script and its read (section 4.5) | a build agent; one judge |
| 10 | The STATE block for hC (OPS-1115aq) and for hD | coordinator |
| 11 | Running title and authors of the LNCS build (CC-421 N2): not applied; it does not move the page count | the build agent, with item 5 |

Not found in the documents read: a licence line for a rental with no stage-H job (D1); a host timing for any Paper A or Paper B build; a hashed matplotlib lock; exact restore texts r1 to r4; a mechanical form of k0 or k3.

---

## Annex A: helper scripts (extract with P0; each file is the lines between its two marker lines)

| File | sha256 | Where it runs | What it does |
|---|---|---|---|
| `run_setup.sh` | c4998685f2e026feba0522010c046648ce1d02bd99ff04e64605b23e5b29291b | host, tmux `tools` | the as-run setup of 15 Nov with `EXTRA_TL_PKGS="llncs aliascnt"` |
| `k1_list.py` | dcf6decc36348074fec48b23ef99981963308fc747dd502a298fa8a9bda042d9 | laptop | K1 push list from the scripts' `*_REL`/`*_SHA` constants, each file checked |
| `k1_run.sh` | ca60daf87cef569e57eade457e6dc7ee4bda25ce24eefe4667e49f3c7ed13982 | host, tmux `k1` | venv, selftest, build; records only |
| `k2_cuts.py` | 8ff6d2dc487a3c0fc5be451cda6c68e9390b87346acec413adafc37ed6e0e7df | laptop | cuts k1 and k2 of CC-421 Ruling 5 on a copy of the draft folder |
| `k2_prep.py` | bef12da9987254eb842427e41f98358e0c5fb1d8f1b54fde1118e40503454d45 | laptop | derived build files and the plain, dummy and vi input folders |
| `k2_run.sh` | a06f6e47bd0843fce23366d3b601ee674ba3b9206f42b966059fd37be46e4152 | host | every variant in both layouts; summary |
| `k4_run.sh` | a21571b3fdd6acdcd50a80c62f78acbc9351843ab4ee8cab3279aeb8f5b50dd7 | host, tmux `k4` | both Paper A builds per attempt number, output to files only, counts and heading map |
| `k_counts.sh` | 685183a20bff56f11bc1f8c5c658fa31d8ebc41ecafc4d3800a1058b573fa442 | host | counts of one LaTeX build, no text fragment |

Tested on the laptop while writing (scratch folders only; no host, no study data): `k1_list.py` on today's scripts (rc 0, 4 inputs equal to their pins); `k2_cuts.py` and the checker in three modes on a copy with k1 and k2 (rc 0, 12 PASS, 1 INFO); `k2_prep.py` on b42eecb1 (the shas of P3); the pre-LaTeX half of the derived `build_lncs.sh` (pre-processing, the five pandoc calls, the preamble fill; laptop pandoc 3.5, the host's pinned version) on `base`, `base_dummy`, `base_vi`, `k1k2`, `k1k2_dummy`: rc 0, 0 figures, "end sections without a number: 4", the author block kept as raw LaTeX (this test found that pandoc escapes a bare `\and`; `k2_prep.py` now writes it as a raw LaTeX span); the `LASTPAGE-FILL` line in a scratch LaTeX file (fill agrees with the line count; text and page count unchanged); `k_counts.sh` on the 15 Nov Paper C main log (3 overfull boxes, as its record); `bash -n` on the five shell scripts. Not tested: anything that needs the host tool tree.

### run_setup.sh

```text
-----BEGIN run_setup.sh-----
#!/bin/bash
# Tools of K2-K5 on the host: the as-run setup of 15 Nov (bf5294df), with aliascnt added to the private TeX packages.
B=/root/paperC_build; mkdir -p $B/rec
{ EXTRA_TL_PKGS="llncs aliascnt" bash $B/host_tex_setup.sh setup; echo $? > $B/rec/setup.rc; } 2>&1 | tr . _ > $B/rec/setup_out.txt
-----END run_setup.sh-----
```

### k1_list.py

```text
-----BEGIN k1_list.py-----
"""K1 push list: every <NAME>_REL path of the figure scripts with its <NAME>_SHA, checked on the laptop."""
import ast, hashlib, sys
from pathlib import Path

root, scripts = Path(sys.argv[1]), sys.argv[2:]
bad = 0
for s in scripts:
    env = {}
    for n in ast.parse(Path(s).read_text(encoding="utf-8")).body:
        if not (isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)):
            continue
        v, k = n.value, n.targets[0].id
        if isinstance(v, ast.Constant) and isinstance(v.value, str):
            env[k] = v.value
        elif isinstance(v, ast.JoinedStr):
            env[k] = "".join(p.value if isinstance(p, ast.Constant) else env[p.value.id] for p in v.values)
    for k, rel in env.items():
        if k.endswith("_REL"):
            pin = env[k[:-4] + "_SHA"]
            got = hashlib.sha256((root / rel).read_bytes()).hexdigest()
            bad += got != pin
            print(f"{pin}  {rel}" if got == pin else f"MISMATCH {rel}: {got} != {pin}", file=sys.stdout if got == pin else sys.stderr)
sys.exit(1 if bad else 0)
-----END k1_list.py-----
```

### k1_run.sh

```text
-----BEGIN k1_run.sh-----
#!/bin/bash
# K1 on the host: a venv from one pinned requirement, the scripts' selftest, then the build. Records in /root/k1/rec.
set -u
K=/root/k1; R=$K/rec; mkdir -p "$R"
export MPLCONFIGDIR=$K/mpl PIP_DISABLE_PIP_VERSION_CHECK=1
echo "matplotlib==3.10.9" > "$R/requirement.txt"
{ python3 -m venv "$K/venv" && "$K/venv/bin/pip" download -q -d "$K/wheels" -r "$R/requirement.txt" \
  && "$K/venv/bin/pip" install -q --no-index --find-links "$K/wheels" -r "$R/requirement.txt"; } > "$R/venv.txt" 2>&1
echo $? > "$R/venv.rc"
(cd "$K/wheels" && sha256sum -- *) > "$R/wheels.sha256" 2>/dev/null
"$K/venv/bin/pip" freeze > "$R/freeze.txt" 2>/dev/null; "$K/venv/bin/python" --version > "$R/python.txt" 2>&1
[ "$(cat "$R/venv.rc")" = 0 ] || exit 9
S=$K/repo/scripts/b_figs; B=$S/build_all_v2.sh; [ -f "$B" ] || B=$S/build_all.sh; echo "$B" > "$R/build_script.txt"
PATH=$K/venv/bin:$PATH bash "$B" --selftest > "$R/selftest.txt" 2>&1; echo $? > "$R/selftest.rc"
[ "$(cat "$R/selftest.rc")" = 0 ] || exit 8
PATH=$K/venv/bin:$PATH bash "$B" > "$R/build.txt" 2>&1; echo $? > "$R/build.rc"
-----END k1_run.sh-----
```

### k2_cuts.py

```text
-----BEGIN k2_cuts.py-----
"""CC-421 Ruling 5 cuts k1 and k2, applied to paper.md of a COPY of the draft folder (never the draft folder itself).
usage: python3 -I k2_cuts.py <copy folder> k1|k2"""
import re, sys
from pathlib import Path

folder, step = Path(sys.argv[1]).resolve(), sys.argv[2]
assert "conf_taimma_2027" not in folder.parts, "a draft folder: work on a copy"
p = folder / "paper.md"
t = p.read_text(encoding="utf-8")
if step == "k1":  # S3-07, the sentence quoted in the ruling
    old = " The equal number of mentions keeps a longer caption from being penalised for naming more objects."
    assert t.count(old) == 1, "k1 sentence not found exactly once"
    t = t.replace(old, "")
elif step == "k2":  # S1-03, the sentence that lists the four prompts
    hits = re.findall(r" Two open MLLMs caption each image under four prompts:.*?and zero-shot \(`zs`\)\.", t)
    assert len(hits) == 1, "k2 sentence not found exactly once"
    unit = next(l for l in t.splitlines() if l.startswith("<!-- p:S1-03 -->"))
    assert hits[0] in unit, "k2 sentence is not in unit S1-03"
    t = t.replace(hits[0], "")
else:
    sys.exit("step must be k1 or k2")
p.write_text(t, encoding="utf-8")
print(step, "applied:", p)
-----END k2_cuts.py-----
```

### k2_prep.py

```text
-----BEGIN k2_prep.py-----
"""K2 inputs: build_lncs.sh for a draft without a figure (CC-421 Option B), a measure-only last-page line, and the
dummy-filled copies of CC-421 Ruling 5. Writes only into <out>; the draft folder is read, never written.
usage: python3 -I k2_prep.py <build_lncs.sh ef21d602> <lncs.lua c8d597b4> <lncs_preamble.tex cdfe51a9> <paper.md> <paperC.bib> <strip_num.lua> <out root> <label> [vi]
Writes <out root>/in_<label> (the draft as it is), in_<label>_dummy (placeholders filled with dummy text) and, with vi,
in_<label>_vi (dummy text with Vietnamese letters in the author names), each with a sha256 list beside it."""
import hashlib, re, shutil, sys
from pathlib import Path

PIN = {0: "ef21d6023c95a09d9665241304a15e1d86fe6d92a57780aed29f2b1d0a79b25c",
       1: "c8d597b466fa226ddc7fa57f056f6f41693945e27140ad6aa83487e2cf62a3c4",
       2: "cdfe51a90031c86cd67a023369d37559c34e5f15834d8ede608b720e145a8fc5"}
src = [Path(a) for a in sys.argv[1:7]]
out, label, vi = Path(sys.argv[7]), sys.argv[8], sys.argv[9:] == ["vi"]
for i, pin in PIN.items():
    got = hashlib.sha256(src[i].read_bytes()).hexdigest()
    assert got == pin, (src[i], got)
names = [f"in_{label}", f"in_{label}_dummy"] + ([f"in_{label}_vi"] if vi else [])
for n in names:
    assert not (out / n).exists(), out / n


def edit(text, pairs):
    for old, new in pairs:
        assert text.count(old) == 1, old[:70]
        text = text.replace(old, new)
    return text


BUILD = [  # no figure in the draft (CC-421 Option B); the last-page fill goes into PAGE_COUNT.txt
    ('INPUTS="paper.md paperC.bib fig1_ret_minus_rand.svg strip_num.lua lncs.lua lncs_preamble.tex build_lncs.sh"',
     'INPUTS="paper.md paperC.bib strip_num.lua lncs.lua lncs_preamble.tex build_lncs.sh"'),
    ('nice -n 19 rsvg-convert -f pdf -o fig1_ret_minus_rand.pdf "$IN/fig1_ret_minus_rand.svg" || die "rsvg-convert"\n', ''),
    ('''[ "$(grep -c -F '\\includegraphics' body.tex)" = 1 ] || die "not exactly one figure in body.tex"''',
     '''[ "$(grep -c -F '\\includegraphics' body.tex)" = 0 ] || die "a figure in body.tex (CC-421 Option B has none)"'''),
    ('sha256sum paper_lncs.pdf paper_lncs.tex body.tex paper_lncs.bbl fig1_ret_minus_rand.pdf',
     'sha256sum paper_lncs.pdf paper_lncs.tex body.tex paper_lncs.bbl'),
    ('echo "- Fig. 1 is the journal figure; its rebuild from manifest values is owed (CC-399 N5) and keeps its area;"',
     'echo "- no figure (CC-421 Option B);"'),
    ('  echo "words (pdftotext | wc -w): $(pdftotext paper_lncs.pdf - | wc -w)"\n',
     '  echo "words (pdftotext | wc -w): $(pdftotext paper_lncs.pdf - | wc -w)"\n'
     '  echo "last page fill (measure line of the preamble): $(grep -a -o -E \'LASTPAGE-FILL [0-9.]+pt of [0-9.]+pt\' "$L" | tail -1)"\n'),
]
PRE = [  # measure only: no box, no glue, no page break is added
    ('\\begin{document}\n',
     '\\AtEndDocument{\\par\\penalty0\\typeout{LASTPAGE-FILL \\the\\pagetotal\\space of \\the\\textheight}}   % MEASURE: height used on the last page, written to the log only\n'
     '\\begin{document}\n'),
]
INST_OLD = '\\institute{[Affiliation and full address: to be set by the PI]\\\\ \\email{[e-mail: to be set by the PI]}}'
INST_NEW = ('\\institute{Faculty of Information Technology, Example University of Science and Technology, 123 Example Street, '
            'Ward 1, District 1, Ho Chi Minh City 700000, Vietnam\\\\ \\email{first.author@example.org, second.author@example.org} '
            '\\and Department of Computer Science, Example University of Education, 456 Example Road, Ward 2, District 5, '
            'Ho Chi Minh City 700000, Vietnam\\\\ \\email{third.author@example.org}}')
AND = " `\\and`{=latex} "  # pandoc escapes a bare \\and; a raw LaTeX span passes it through (checked with pandoc 3.5)
NAMES = {"dummy": AND.join(("First Middle Author\\inst{1}", "Second Middle Author\\inst{1}", "Third Middle Author\\inst{2}")),
         "vi": AND.join(("Trần Văn A\\inst{1}", "Lê Thị B\\inst{1}", "Phạm Văn C\\inst{2}"))}
LICENCE_OLD = '[PI: one entry per set, as documented by its authors; where nothing is documented, write "not reported by the dataset authors"]'
LICENCE_NEW = "; ".join(f"{s}: Dummy Licence Name Attribution 4.0 International" for s in
                        ("KTVIC", "UIT-OpenViIC", "XM3600", "COCO", "NoCaps", "Open Images")) + "."
ACK_OLD = "[PI: acknowledgments and funding sentence.]"
ACK_NEW = ("This dummy acknowledgment stands in for the real one and has its usual length: the work was supported by "
           "the Dummy Research Fund under grant number DUMMY-0000-00-00, and the authors thank the dummy colleagues "
           "of the dummy laboratory for their comments on an earlier version of this paper and the dummy computing "
           "centre for the machines it provided.")
COI_OLD = "[PI: statement of the authors' competing interests.]"
COI_NEW = ("This dummy statement stands in for the real one: the authors state here, in about two lines of text, "
           "whether they have competing interests that are relevant to the content of this article.")

build = edit(src[0].read_text(encoding="utf-8"), BUILD)
pre = edit(src[2].read_text(encoding="utf-8"), PRE)
paper = src[3].read_text(encoding="utf-8")
for name in names:
    d = out / name
    d.mkdir(parents=True)
    (d / "build_lncs.sh").write_text(build, encoding="utf-8")
    shutil.copyfile(src[1], d / "lncs.lua")
    shutil.copyfile(src[4], d / "paperC.bib")
    shutil.copyfile(src[5], d / "strip_num.lua")
    if name == f"in_{label}":
        (d / "lncs_preamble.tex").write_text(pre, encoding="utf-8")
        shutil.copyfile(src[3], d / "paper.md")
        continue
    (d / "lncs_preamble.tex").write_text(edit(pre, [(INST_OLD, INST_NEW)]), encoding="utf-8")
    fill = [("[AUTHORS: to be set by the PI]", NAMES[name.rsplit("_", 1)[1]]), (LICENCE_OLD, LICENCE_NEW), (ACK_OLD, ACK_NEW), (COI_OLD, COI_NEW)]
    (d / "paper.md").write_text(edit(paper, fill), encoding="utf-8")
for name in names:
    d = out / name
    lines = [f"{hashlib.sha256((d / f).read_bytes()).hexdigest()}  {name}/{f}" for f in sorted(p.name for p in d.iterdir())]
    (out / f"{name}.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"== {name}"); print("\n".join(lines))
-----END k2_prep.py-----
```

### k2_run.sh

```text
-----BEGIN k2_run.sh-----
#!/bin/bash
# K2 on the host: every pushed variant folder in_* built in both layouts, one out folder per build, then a summary.
# Optional argument: the sha256 named by the closing diff read (K2-R only); empty = PROVISIONAL.
set -u
T=/root/paperC_build/taimma; cd "$T" || exit 9; . /root/paperC_build/env.sh; RS=${1:-}
for v in in_*; do
  [ -d "$v" ] || continue
  for lay in default starred; do
    o=out_${v#in_}_$lay
    if [ "$lay" = starred ]; then END_SECTIONS=starred bash "$T/$v/build_lncs.sh" "$T/$v" "$T/$o" $RS > "$T/$o.console" 2>&1
    else bash "$T/$v/build_lncs.sh" "$T/$v" "$T/$o" $RS > "$T/$o.console" 2>&1; fi
    echo "$o rc $?" >> "$T/K2_RC.txt"
  done
done
for o in out_*; do
  [ -d "$o" ] || continue
  f=$o/PAGE_COUNT.txt; P=$(pdfinfo "$o/paper_lncs.pdf" 2> /dev/null | awk '/^Pages:/ {print $2}'); a=-; b=-
  if [ -n "$P" ]; then
    a=$(pdftotext -f "$P" -l "$P" -layout "$o/paper_lncs.pdf" - | grep -c .)
    b=$(pdftotext -f $((P - 1)) -l $((P - 1)) -layout "$o/paper_lncs.pdf" - | grep -c .)
  fi
  echo "$o | pages ${P:-none} | references from page $(sed -n 's/^reference list starts on page: \([0-9a-z ]*\) .*/\1/p' "$f" 2> /dev/null)" \
    "| $(grep -a -o -E 'LASTPAGE-FILL [0-9.]+pt of [0-9.]+pt' "$o/paper_lncs.log" 2> /dev/null | tail -1)" \
    "| lines on the last and the previous page $a / $b" \
    "| $(grep -E '^(undefined references|lines with \?\?|Missing character|overfull hboxes over)' "$f" 2> /dev/null | sed 's/ (must be 0)//' | tr '\n' ';')"
done > "$T/K2_SUMMARY.txt"
-----END k2_run.sh-----
```

### k4_run.sh

```text
-----BEGIN k4_run.sh-----
#!/bin/bash
# K4 on the host: both Paper A builds. Every output goes to files (the source holds the held zones); only the
# counts file K4_COUNTS_<n>.txt is ever shown. Argument: attempt number n (default 1); its folders must not exist.
set -u
K=/root/k4; N=${1:-1}; R=$K/rec_$N; M=$K/out_main_$N; P=$K/out_supp_$N
for d in "$R" "$M" "$P"; do [ ! -e "$d" ] || { echo "STOP: $d exists (one folder set per attempt)"; exit 9; }; done
mkdir -p "$R" "$M" "$P"; . /root/paperC_build/env.sh
cp "$K/pin/cas-common.sty" "$M/"
OUT=$M nice -n 19 bash "$K/src/paper/build/build_A_cas.sh" > "$R/console_main.txt" 2>&1; echo $? > "$R/main.rc"
OUT=$P nice -n 19 bash "$K/src/paper/build/build_A_supp.sh" > "$R/console_supp.txt" 2>&1; echo $? > "$R/supp.rc"
{ echo "attempt $N: main rc $(cat "$R/main.rc"); supplement rc $(cat "$R/supp.rc")"
  bash "$K/k_counts.sh" "$M" paperA_SPIC
  bash "$K/k_counts.sh" "$P" paperA_SPIC_supplementary
  grep -h -E '^dataset tags: [0-9]+$' "$M/tags.txt"
  echo "highlights_A.docx: $(test -s "$P/highlights_A.docx" && echo present || echo MISSING)"
  # heading numbers only (no title text) with their .tex line, so that a box or an error can be placed in or out
  # of the held zones (Section 6.7, S11) by its line number alone
  for t in "$M/paperA_SPIC.tex" "$P/paperA_SPIC_supplementary.tex"; do
    echo "headings of $(basename "$t") (line:number): $(grep -n -o -E '^\\(sub)*section\*?\{S?[0-9]+(\.[0-9]+)*' "$t" | sed -E 's/\\(sub)*section\*?\{//' | tr '\n' ' ')"
  done; } > "$R/K4_COUNTS_$N.txt" 2>&1
-----END k4_run.sh-----
```

### k_counts.sh

```text
-----BEGIN k_counts.sh-----
#!/bin/bash
# Counts only, never a text fragment of the document: k_counts.sh <build dir> <job name>
d=$1; j=$2; L=$d/$j.log
[ -f "$L" ] || { echo "$j: NO LOG"; exit 9; }
if [ -f "$d/$j.pdf" ]; then p=$(pdfinfo "$d/$j.pdf" | awk '/^Pages:/ {print $2}'); q=$(pdftotext "$d/$j.pdf" - | grep -c -F '??'); else p=NO-PDF; q=-; fi
echo "$j: pages $p; undefined $(grep -a -c -E 'Warning: (Reference|Citation) `|There were undefined' "$L");" \
  "missing character $(grep -a -c -F 'Missing character' "$L"); overfull hbox $(grep -a -c -E '^Overfull \\hbox' "$L");" \
  "over 10 pt $(grep -a -o -E '^Overfull \\hbox \([0-9.]+pt' "$L" | grep -o -E '[0-9.]+' | awk '$1 > 10 {n++} END {print n + 0}');" \
  "overfull vbox $(grep -a -c -E '^Overfull \\vbox' "$L"); underfull $(grep -a -c -E '^Underfull' "$L"); lines with ?? $q"
grep -a -o -E '^Overfull \\[hv]box \([0-9.]+pt too [a-z]+\)( [a-z]+)+ at lines? [0-9]+(--[0-9]+)?' "$L"
-----END k_counts.sh-----
```
