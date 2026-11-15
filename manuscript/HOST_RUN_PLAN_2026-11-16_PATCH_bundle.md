# Proposed patch: install bundle, job K1b and host clean-up in the host run doc and the rented-host skill (for a judge; NOT applied)

- **Pairs.** P1 to P5: install bundle (PI-1115r). P6 to P8, P11: job K1b of CC-428 and the order of the next session (K1b, K2, K4, K5; K3 after the Paper C freeze commits; K1 not run again). P9, P10, P12: apt row and laptop clean-up after deletion (PI-1115s). P13 to P15: K5 with `build_B_rev.sh` (CC-426, CC-425 addendum A3).

- **Why (PI-1115r).** Every rented machine is a fresh image. On 2026-11-15 the hD image lacked libfontconfig1,
  libfreetype6, libglib2.0-0t64, libharfbuzz0b, libpng16-16t64, libjpeg-turbo8, libxml2 (and liblcms2-2, libnss3,
  libnspr4). The tool setup stopped with rc 9 at its `ldd` check, and the stop rule of section 6.4 dropped K2 to K5
  (`.session_backup/2026-11-15/host_session_hD/setup/rec/missing_libs.txt`, `setup_out.txt`).
- **Targets.** `manuscript/HOST_RUN_PLAN_2026-11-16.md` (sha256 77c3768f59194383bfa4362eef431e5c0968064f52603ae81b62ad8f96057c0e)
  and `.claude/skills/running-rented-gpu-jobs/SKILL.md` (sha256 5053a11d230f5b1130a3359db4e9253d6a9c79d9f7675ae0e1272337edbe387d).
  Each OLD text below occurs once in its file. Nothing else changes; `host_tex_setup.sh`, `run_setup.sh` and the
  annex shas are untouched.
- **Bundle files at the time of writing** (not committed; any edit changes them, so the judge reads the shas at
  ruling time): `scripts/host_bundle/SYSTEM_PACKAGES.txt` 2c93837400a81701b9c4a31ce60232b59453e432e26fc515e6e327c556f64423,
  `scripts/host_bundle/install_system.sh` be66d6a0adb9bd1cf3e6fdf343479ad6680f8f80e0fa49286ba9f20f1f8f8809,
  `scripts/host_bundle/cleanup_host.sh` 3a0f387695fea5d65e83f32766a3190efd50c11a5f0c086cc57e8256c698ee6a.
  Selftest of install_system.sh on the laptop: 117 of 117 checks pass, installs nothing. Not run on any host.
  cleanup_host.sh: `--dry-run` only (see the last section).
- **Poppler libraries (lead's item 1).** The hD `ldd` lines liblcms2.so.2, libnss3.so / libsmime3.so, libnspr4.so /
  libplc4.so resolve on Ubuntu 24.04 to the packages liblcms2-2, libnss3 and libnspr4 (laptop `dpkg -S` of the same
  files; libnssutil3.so and libplds4.so come from the same two packages). All three are in SYSTEM_PACKAGES.txt.

## P1. Run doc, section 3 step 4 (system packages)

OLD:

```text
4. **System packages, all before step 6** (CC-410 N3), the list that worked on 15 Nov minus Java: `apt-get install -y git tmux rsync util-linux python3.12 python3.12-venv python3 python3-venv time procps`; record the versions (dots as underscores). Then `pgrep -x apt-get; pgrep -x dpkg` print nothing. No apt call of any kind after step 6 starts (the private `apt-get download` of the setup script included, which runs inside step 6).
```

NEW:

````text
4. **System packages, all before step 6** (CC-410 N3; PI-1115r: the host is a fresh image, so missing system libraries are expected): the install bundle `scripts/host_bundle/`, profile `pdf` (K2 to K5; it includes `base`, which covers K1b and every package of the 15 Nov list), no Java. Push its two files, check their shas, install, and read the verification table:

```bash
tar -C "$REPO/scripts" -cf - host_bundle/SYSTEM_PACKAGES.txt host_bundle/install_system.sh | ssh -o BatchMode=yes "$H" 'tar -xf - --no-same-owner -C /root'; echo "tar ${PIPESTATUS[0]} ssh ${PIPESTATUS[1]}"
(cd "$REPO/scripts" && sha256sum host_bundle/SYSTEM_PACKAGES.txt host_bundle/install_system.sh) | ssh -o BatchMode=yes "$H" 'cd /root && sha256sum --quiet -c - && echo "bundle OK"' 2>&1 | F
S 'bash /root/host_bundle/install_system.sh pdf > /root/bundle_install.txt 2>&1; echo "bundle rc $?"; sed -n "/^CHECK /,\$p" /root/bundle_install.txt | tr . _'
```

   - rc 0 (`VERIFY CLEAN`): go on to step 5. The private-tool rows say `skip` here (the setup has not run yet); that is expected.
   - rc 1: install the packages that the `MISSING` lines name (`apt-get install -y --no-install-recommends <package>`), then `S 'bash /root/host_bundle/install_system.sh --verify pdf'` once. Still not clean: K2 to K5 drop out; K1 continues if every `base` row is clean; pull and delete.
   - The table (dots as underscores) goes into the facts-and-packages OPS line; its `apt idle` row replaces the `pgrep` check. Every package added by hand is named in that line and goes into `SYSTEM_PACKAGES.txt` after the session (`scripts/host_bundle/README.md`).
   - No apt call of any kind after step 6 starts (the private `apt-get download` of the setup script included, which runs inside step 6), except the one recovery install of section 6.4.
````

## P2. Run doc, section 3 step 6, the rc bullet

OLD:

```text
   - rc 0: tools present for K2 to K5 ("SETUP OK (J2 and J3)"). rc 3: LNCS class missing: K2 only takes the fallback of CC-410 J3-4. rc 9: STOP line at the end of the output.
```

NEW:

```text
   - rc 0: tools present for K2 to K5 ("SETUP OK (J2 and J3)"). rc 3: LNCS class missing: K2 only takes the fallback of CC-410 J3-4. rc 9: STOP line at the end of the output; if it names a missing library or package, section 6.4 allows one recovery install and one re-run of the unchanged setup.
```

## P3. Run doc, section 6.4, the setup stop rule

OLD:

```text
| Setup rc 9, or an address outside CC-410 ruling 5 | K2 to K5 drop out; K1 continues; pull and delete |
```

NEW:

```text
| Setup rc 9 whose STOP line names a missing library or package ("a library is missing", `not found`) | once per session, with a DEVIATION line for each step: (1) wait until `tmux has-session -t tools` fails; (2) keep the first attempt's records: `S 'cd /root/paperC_build/rec && mv setup_out.txt setup_out_attempt1.txt && mv setup.rc setup_attempt1.rc && bash /root/paperC_build/host_tex_setup.sh outside > outside_attempt1.txt'`; (3) install: `S 'bash /root/host_bundle/install_system.sh pdf'`, plus `apt-get install -y --no-install-recommends` of each package the STOP output names that the list lacks (find it with `apt-cache search` or the library name; record each); (4) `S 'find /var/cache/fontconfig -newer /root/paperC_build/marker_setup \| wc -l'`: if it is not 0 (a font package ran fc-cache), record the count and `mv /root/paperC_build/marker_setup /root/paperC_build/marker_setup_attempt1`, so the re-run's own font-cache check measures the re-run only; (5) re-run the unchanged setup once with the step 6 commands; (6) `S 'bash /root/host_bundle/install_system.sh --verify pdf'`: the private-tool `ldd` rows must now be `ok`. Setup rc 0 or 3: go on as section 3 step 6. Setup rc 9 again: K2 to K5 drop out; K1 continues; pull and delete |
| Setup rc 9 for any other reason, or an address outside CC-410 ruling 5 | K2 to K5 drop out; K1 continues; pull and delete |
```

Note for the judge on P3 (4): the marker move is the only part of the recovery that touches a setup record. Without
it, an fc-cache run by the recovery install would make the unchanged setup's check (`/var/cache/fontconfig` newer
than the marker must be 0) fail for a reason that is not the build's own font use. On the primary path (P1) the
bundle runs before the marker exists, so the question does not arise. Recommendation: accept (4) as written,
confidence 75 %. Default if it is refused: drop step (4) and accept that a recovery which installed a font package
ends in rc 9.

## P4. Skill, Host session step 4 (Prep)

OLD:

```text
4. **Prep.** `apt-get install -y git tmux rsync util-linux python3.12 python3.12-venv` if missing. Add `default-jre-headless`, and fetch the VnCoreNLP jar and models by sha, only if a host step segments Vietnamese; in VSPS the decomposers run on the laptop. This is host prep, not a code change.
```

NEW:

```text
4. **Prep (PI-1115r: every rented host is a fresh image; never assume a library is present).** Push `scripts/host_bundle/` (sha-checked) and run, as root, `bash scripts/host_bundle/install_system.sh <profiles>` (base | figures | pdf | gpu | all) before any tool setup or job. Add the `java` profile, and fetch the VnCoreNLP jar and models by sha, only if a host step segments Vietnamese; in VSPS the decomposers run on the laptop. No job starts before its table says `VERIFY CLEAN`; the table goes into the facts-and-packages OPS line. After the session, add whatever was found missing to `SYSTEM_PACKAGES.txt` with date and evidence (`scripts/host_bundle/README.md`). This is host prep, not a code change.
```

## P5. Skill, Common mistakes (one row added after the last row)

OLD:

```text
| Running hostcheck directly after a FAULT | Only the job script's run is a record; a direct call is an INFRA PROBE |
```

NEW:

```text
| Running hostcheck directly after a FAULT | Only the job script's run is a record; a direct call is an INFRA PROBE |
| Assuming a library an earlier image had | Every host is a fresh image: run the bundle first and read its table |
```

## P6. Run doc, section 1.1, licences: K1 done, K1b added

OLD:

```text
| K1 Paper B Table 6 and figures | CC-420 ruling 7 step 3 (Table 6 by the script of FIGURE_TABLE_SPEC A2 from HUMAN.json and BUILD.json; Fig. 3, Fig. 2, Fig. EF1, Fig. 1; outputs to `paper/rev_2026-11-15/figures/` with a sums file; a one-judge DIFF read before their commit). Custody of the Paper B results was released by CC-418 (from its LOG line) |
```

NEW:

```text
| K1 Paper B Table 6 and figures | CC-420 ruling 7 step 3 (Table 6 by the script of FIGURE_TABLE_SPEC A2 from HUMAN.json and BUILD.json; Fig. 3, Fig. 2, Fig. EF1, Fig. 1; outputs to `paper/rev_2026-11-15/figures/` with a sums file; a one-judge DIFF read before their commit). Custody of the Paper B results was released by CC-418 (from its LOG line) |
| K1b Paper B Fig. EF1 and Fig. 1 | CC-428 ruling 4 (CC sha ab98dc743c8b2c92714bcc9745cf9cb21ea254dfe556f5b9ce9be16b88b2261e): 12-file allow-list (list sha 4559900b36be7a3d372fe36549da3fabccf03b8cab7fae2f133530ab3fea11e8), runner k1b_run.sh 8ed0cb65d480e634dbeba1124c9aca2590562ffffaec77aa63863ab3d0168e40; before the push W1 and W2 closed by sha match and the W3 coordinator line on the LOG. K1 itself is not run again: it ran on 2026-11-15 (venv, selftest and build rc 0; records and pulled outputs in `.session_backup/2026-11-15/host_session_hD/k1/`) |
```

## P7. Run doc, new section 4.1b K1b, placed before section 4.2

OLD:

```text
### 4.2 K2: TAIMMA page measures (PROVISIONAL)
```

NEW:

````text
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
````

## P8. Run doc, section 6.1, order of the next session

OLD:

```text
1. Laptop: P0 to P7 (section 2).
2. Rent, access, facts, system packages (section 3 steps 1-4).
3. Tools push and setup in tmux; **K1 beside it**.
4. **K2**, then K3 (if eligible), K4, K5 (if eligible), one after the other, each pulled before the next.
5. Leaving checks; delete; L-after (6.3).
```

NEW:

```text
1. Laptop: P0 to P7 (section 2), the K1b laptop lines of section 4.1b, and the push of the install bundle (section 3 step 4).
2. Rent, access, facts, system packages (section 3 steps 1-4).
3. Tools push and setup in tmux; **K1b beside it** (K1 ran on 2026-11-15 and is not run again).
4. **K2**, then K4, then K5 (section 4.5: `paper/build/build_B_rev.sh` at Paper B HEAD 6356b99, CC-426 ruling 8 and CC-425 addendum A3), one after the other, each pulled before the next; K3 only once the Paper C freeze commits exist (runbook steps 1 to 6), else it moves to a later session.
   The session's job list is therefore K1b, K2, K4, K5, then K3 only after the Paper C freeze commits.
5. Leaving checks; delete; L-after; host clean-up (6.3).
```

## P9. Run doc, section 6.2, two rows (each its own pair; the row between them is unchanged)

OLD:

```text
| Tool setup + K1 venv and builds | yes: separate folders (`/root/paperC_build`, `/root/k1`), CPU only, no shared file |
```

NEW:

```text
| Tool setup + K1b venv and builds | yes: separate folders (`/root/paperC_build`, `/root/k1b`), CPU only, no shared file |
```

OLD:

```text
| Any apt-get after step 6 started | no; only private `tlmgr install` into the private TinyTeX, each with a record line (CC-410 J3-5) |
```

NEW:

```text
| Any apt-get after step 6 started | no, except the one recovery install of section 6.4; only private `tlmgr install` into the private TinyTeX, each with a record line (CC-410 J3-5) |
```

## P10. Run doc, section 6.3, leaving, deletion and clean-up

OLD:

```text
Expected: 0 processes of the build folder, no tmux session. Every job's tar is on the laptop with equal shas. Then delete the instance on the panel as the next step, with no new job; check twice that the panel lists no instance and the host does not answer; L-after with the per-instance figure; remove the `Host hD` entry. No label, key or data file was ever on hD.
```

NEW:

```text
Expected: 0 processes of the build folder, no tmux session. Every job's tar is on the laptop with equal shas. Then delete the instance on the panel as the next step, with no new job; check twice that the panel lists no instance and the host does not answer; L-after with the per-instance figure; then the laptop clean-up (PI-1115s): `bash "$REPO/scripts/host_bundle/cleanup_host.sh" "$H" --dry-run`, read the list, then the same command without `--dry-run`. It removes the alias's block in `~/.ssh/config`, its host keys (`ssh-keygen -R`) and any per-host known_hosts file, its control socket, and the askpass, password and pid files named after the alias; its last line is the text of the clean-up OPS line (names only, never an address). Kept: LOG lines and the session record folder (logs, sums, pulled results). No label, key or data file was ever on the host.
```

## P11. Run doc, section 7, OPS lines

OLD:

```text
5. **K1** (section 4.1).
6. **K2 PROVISIONAL** (section 4.2).
7. **K3** or **K3 NOT RUN** (which precondition failed).
8. **K4** (numbers only).
9. **K5 NOT RUN** (the script) or K5.
10. **leaving and deletion**, with L-after, block spend and the 50,000 VND check.
```

NEW:

```text
5. **K1b** (section 4.1b; K1 ran on 2026-11-15).
6. **K2 PROVISIONAL** (section 4.2).
7. **K3** or **K3 NOT RUN** (which precondition failed).
8. **K4** (numbers only).
9. **K5 NOT RUN** (the script) or K5.
10. **leaving and deletion**, with L-after, block spend and the 50,000 VND check; then the host clean-up line (section 6.3, PI-1115s).
```

## P12. Skill, End and loss

OLD:

```text
- **End:** pull the registered file set, verify SUMS, wipe tmpfs (logged), delete the instance, do L-after, write the hand-off OPS line, then the result read.
```

NEW:

```text
- **End:** pull the registered file set, verify SUMS, wipe tmpfs (logged), delete the instance, do L-after, write the hand-off OPS line, then the result read.
- **Clean-up (PI-1115s), the last step after the delete and L-after, also after a lost host:** `bash scripts/host_bundle/cleanup_host.sh <alias> --dry-run`, then without `--dry-run`. It removes every laptop file about the machine except logs: the ssh config block, host keys and any per-host known_hosts file, control sockets, the askpass script, the password file and pid files of that host. One OPS line names what was removed (names only, never an address). Kept: LOG lines and the session record folder.
```

## P13. Run doc, section 1.2, state of the K5 inputs (CC-426 N5)

OLD:

```text
| K5 | no | Paper B HEAD 568eaec29f29a4eb7e9a2401c2e1709f9e72d503 (transfer; `paper/rev_2026-11-15/SNAPSHOT.sha256` c68d9beb, `paper.md` aeeaa016); `paper/build/build_B_springer.sh` 59e86b264cba0f5b | an adapted build script (section 4.5) and its read |
```

NEW:

```text
| K5 | yes, once the A3 (3) line is on the LOG | Paper B HEAD 6356b995e0c9475fb8b12f075407ebedcf876301; `paper/build/build_B_rev.sh` d671b9d2c637d5dec5d4fe85e93e38275b2e92bc167fc3601435f7f88f25ed2a at that HEAD (equal to the sha CC-426 names, l.123; read with `git show 6356b99:paper/build/build_B_rev.sh`); the old `build_B_springer.sh` is not used (CC-426 N5) | the coordinator line of CC-425 addendum A3 (3) extending OPS-1115ba to K5 |
```

## P14. Run doc, section 1.1, licence of K5

OLD:

```text
| K5 Paper B Springer build | CC-420 ruling 7 step 3 ("the build-script path fix; one build for the page count"); needs the adapted script (section 4.5) |
```

NEW:

```text
| K5 Paper B Springer build | CC-420 ruling 7 step 3 (one build for the page count); CC-426 ruling 8 (CC sha 4aaddf05714c937e4205ee9e5f47637bf797af4ad220f830f0ae98bd0adb57d7: `build_B_rev.sh` SAFE and FIT FOR JOB K5, its inputs are the allow-list) and CC-425 addendum A3 (CC sha bf6eaf40c005fa0cadaebce5def7edb6629ca67218386e8ec08d9e54d701b87c: when and how it runs; conditions (1) to (4)) |
```

## P15. Run doc, section 4.5, K5 with the ruled script

OLD:

```text
### 4.5 K5: Paper B Springer build (NOT RUN with the present script)

`paper/build/build_B_springer.sh` (59e86b26) reads `manuscript/journal_draft_B/` of the run-repo layout (l.7), and from it `sec*.md`, `outline_B.md`, `title_page_B.md`, `citation_map_B.tsv` and `paperB.bib`. The transferred draft in `paper/rev_2026-11-15/` is one `paper.md` with `title_page.md`, `online_resource.md` and an unmerged `paperB_additions_PROPOSED.bib` (CC-420 ruling 6: not merged until each mark is read). CC-420 calls the change "the build-script path fix", but the layout differs, so a new script (or mode) is needed: single `paper.md`, its citation mapping, its bibliography rule.

**Run only if:** that script exists in the Paper B repo or in a prep folder, with its sha and a one-judge read that names its inputs. Then: allow-list = the inputs the script names (from its header); push by `git archive` of HEAD with those pathspecs, as P5; run in tmux with all output to files; counts by `k_counts.sh` for `paperB_LRE` (the supplement is built by pandoc directly and keeps no log: its page count by `pdfinfo` only); pull to `$SB/k5`. Custody released (CC-418): the PDF may be viewed. Time 3 to 8 min. Otherwise one NOT RUN line.
```

NEW:

````text
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
````

## Not settled by this patch

- The bundle files (`SYSTEM_PACKAGES.txt`, `install_system.sh`, `cleanup_host.sh`) must be committed, or their shas
  pinned in the run doc, before the next rental, with the shas read at that time.
- The next session needs its own alias and prep folder. The run doc's `H=hD` line (section 2), `Host hD` in section 3
  step 2, `HP=.../host_prep_hD`, the record folder `SB=.../host_session_hD/` (section 4) and the title line name the host of 2026-11-15, which is deleted and whose laptop
  files were removed on 2026-11-15; a new alias is chosen when the next host is rented. No OLD/NEW is proposed here
  for those lines: the alias belongs to that session's revision of the run doc.
- P6 to P11 assume the run doc's sha 77c3768f is no longer pinned by a running session (CC-428 ruling 4 (a) kept the
  run doc unedited for that reason).
- Untested on a real fresh host: the full install on a minimal image, apt's resolution order there, the time it
  takes, and the font row on a host image. `cleanup_host.sh` was run only with `--dry-run` (a made-up alias on the
  real ssh config: nothing found; a made-up alias in a scratch fixture tree: every item listed, the fixture unchanged,
  no address in the output); its removal path has not been run.
