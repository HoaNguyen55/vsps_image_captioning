# Host run plan, evening of 15 Nov 2026 (Vietnam time)

Written 2026-11-15 05:15 VN (2026-11-14T22:15:58Z, `date -u`) for the coordinator, under PI-1114l item 5. A plan only: nothing was run, rented or contacted to write it. Sources are named in each step. Where a document does not give a command, a sha or a rule, the step says "not found in <document>" and the item is in section 6.

**Outcome-free for Paper B.** This file holds no figure and no result of any Paper B stage. Pins are given as sha256 only.

**Machine name.** The new host is called **hC** here and in the LOG. The two ruled laptop-side Paper B scripts and the two helpers hard-code the ssh alias `hB` (`b_stage_push.sh` l.15, `B_STAGE_H.sh` l.30, `~/.cache/vsps_b/bh.sh`, and `bpin.sh` through the push script it calls). A byte change would need a one-judge diff read, so the plan keeps the bytes: `~/.ssh/config` carries one `Host hB hC` entry for the new machine (the old hB entry removed first). No host string, address or port is written in any repo file or LOG line (skill l.26, l.64).

**Hard times (registered).**

| Event | UTC | Vietnam |
|---|---|---|
| Paper B closing line, latest (labelling plan v1.1 l.150; prereg v1.1 l.415) | 2026-11-15T11:00:00Z | 18:00, 15 Nov |
| K-time: stage H must have FINISHED (prereg v1.1 §10 l.369, §13 l.418; `b_fecert.py` l.81) | 2026-11-16T05:00:00Z | 12:00, 16 Nov |

The closing line comes earlier if both raters finish earlier (plan l.150). Every time below then moves earlier by the same amount.

---

## 1. Preconditions and the money check

### 1.1 Licences on the LOG

| Job | Licence |
|---|---|
| J5 stage H on a re-rented host | PI-1113g (yes to CC-388 Q1: one RTX 3090 host, "kept (or re-rented) for stage H after your Paper B closing line, then deleted"); CC-388 ruling 5(c); CC-389 X16 |
| J1 Paper A code test | CC-395 ruling 8: "a host rented later for another licensed job, with its idle CPU used niced"; default of its PI question: "run it on the next host you approve for any paper" |
| J2 Paper C tex/PDF rebuild | PI-1113h (as read by CC-395: the use, on a licensed host); OPS-1114f ("wait for the next host"); tickets T1 of CC-400 and CC-401; plan `KE_HOACH_SAU_GAN_NHAN_2026-11-14.md` §5 item 3 |
| J3 TAIMMA page build | CC-399 G1 and Q3 (default: "build on the next rented host") |
| J4 Paper B figures | **not found** on the LOG: no line licenses a figure run on this host (section 6, item 12) |
| This plan, evening rental | PI-1114l item 5. The same line leaves "renting the host earlier in the afternoon" unanswered, **default: evening** |

No rental for Paper A or C alone is licensed (OPS-1114f; CC-395 ruling 8). J1 to J4 ride on the stage-H host.

### 1.2 Before renting (laptop, no cost)

1. The closing pin-form line is in the laptop LOG (section 4, C1). No host is rented before it in variant (a).
2. A fresh balance read on the provider panel (the last logged figure is two days old).
3. The newest STATE file still says "Live rental: none" (`.claude/agents/STATE_2026-11-13.md` l.8). The L-before formula points at the newest STATE for other live rentals: there are none (OPS-1114f). A STATE update at the rental is owed (section 6, item 15).
4. Offer search by the skill (l.14-16): 1x RTX 3090 / 3090 Ti 24 GB; CPU at least Ryzen 7 5800XT class; RAM >= 32 GB; disk >= 200 GB at >= 1000 MB/s; network >= 400 Mbps; CUDA >= 12.4; uptime > 99 %; max rental time >= the block's hours plus margin (here >= 24 h). Take the cheapest offer that passes every field. Any other choice needs its own DEVIATION line (as OPS-1113ch did).
5. Every push list of section 3 is prepared and hashed on the laptop (J1 file list, J2 archive, J3 inputs, J5 work-file source).
6. The periodic host backup loop (`~/.config/vsps/gpu_backup.sh`) is **not** started for hC (section 4, C9).

### 1.3 Money

| Item | Value | Source |
|---|---|---|
| Last logged balance | **366,998 VND** (L-after, 2026-11-13T17:46:18Z) | OPS-1114f-hB-deleted; no later balance line in the LOG |
| Rate of the previous rental | **9,205 VND/h** (9,175 + 30), offer 77334 | OPS-1113ch-hB-rent |
| Previous block | about 3.1 h, 28,800 VND, against a cap of 312,970 VND | OPS-1114f |
| L-before formula | balance >= cap (hours x rate) + 3 x rate + sum of the remaining capped VND of other live rentals (none) | skill `running-rented-gpu-jobs` l.19 |

At 9,205 VND/h (use the real rate of the chosen offer; the check is `balance >= (cap hours + 3) x rate`):

| Cap | Cap in VND | + 3 x rate | Needed | Balance 366,998 passes? | Balance left if the whole cap is used |
|---|---|---|---|---|---|
| 8 h (top of the 5-8 h estimate) | 73,640 | 27,615 | 101,255 | yes | 293,358 |
| **10 h** (8 h + 25 % margin, the margin of `B_STAGE_TIMING.md`) | 92,050 | 27,615 | **119,665** | yes | 274,948 |
| **18 h** (variant (a) ceiling: rental kept to K-time) | 165,690 | 27,615 | **193,305** | yes | 201,308 |
| 20 h (variant (b) ceiling, rent at 16:00 VN) | 184,100 | 27,615 | 211,715 | yes | 182,898 |

- Expected spend for 5 to 8 h: 46,025 to 73,640 VND.
- **Recommended cap in the rental line: 18 h** (the host must be usable until K-time for one infrastructure re-run of H); expected use 5 to 8 h. With this cap the check holds for any rate up to 17,476 VND/h; with the 10 h cap up to 28,230 VND/h.
- If L-before fails: nothing is rented and the PI is asked at once (skill l.19; PI-1108h).
- **Warning levels.** (i) The PI is told to top up when the balance falls to **50,000 VND** (PI-1108h; kept by PI-1110r). (ii) During a live rental the PI is warned at least 12 h before the balance runs out (skill l.20): at 9,205 VND/h that is a balance of **110,460 VND**. Neither level is reached by this session (lowest projected balance 201,308 VND at the 18 h ceiling).
- During the run: read the panel about every 6 h and log balance, this instance's figure and hours left (skill l.20). After deletion: L-after, the panel's per-instance figure into the block ledger (skill l.22).

---

## 2. Timeline, two variants

Measured on host hB (13 Nov): rental T0 14:37:09Z, facts 14:38:40Z, tree pushed 14:43:05Z, venv 14:44:40Z, G0 at 14:47:33Z, so **10 min 24 s from rental to G0**; deleted about 17:45:20Z (OPS-1113ch, -ci, -cj, -ck; OPS-1114f). The skill's figure for the idle rule is "about 1 h on a fresh host" (l.56). The plan uses 1 h as the threshold and notes that the measured value is lower.

Durations of J1 to J4 are estimates: J1 "minutes to tens of minutes" (CC-395, For the PI); J2 took 8 min on hB including tool setup (build record §1); J3 has no record (new script, debugging); J4 unknown. **No timing exists for stage H** (`B_STAGE_TIMING.md` l.33-36 does not count it).

### Variant (a): rent after the closing line (default, licensed as is)

| Step | UTC | Vietnam |
|---|---|---|
| Laptop preparation of section 1.2 complete | by 10:30Z | by 17:30 |
| Rating sessions stopped; closing pin-form line; 444 copies (section 4) | <= 11:00:00Z | <= 18:00 |
| L-before on the panel; rent; rental line = T0 | about 11:15Z | about 18:15 |
| Access, facts, host packages (section 3.0) | T0 + 0:10 | 18:25 |
| In parallel: J1 push and run; Paper B tree, jar, runner, `setup_venv`; private build tools for J2/J3 | T0 + 0:10 to 0:25 | 18:25 to 18:40 |
| G0 (new), G0 LOG line, `push_new_host`, X16 check | T0 + 0:25 to 0:40 | 18:40 to 18:55 |
| J2 build and pull; J3 script debugging and build; J4 if ready; J1 pull and removal | T0 + 0:40 to 2:30 | 18:55 to 20:45 |
| **Gate L (latest T0 + 2:30 = 13:45Z)**: agents off the host; LOG copy; `push_labels`; `check`; H starts in tmux | <= 13:45Z | <= 20:45 |
| H ends (no measured time; planning reserve 0.5 to 3 h); pulls; wipe; pin; removal line; host deleted; L-after | about 14:15Z to 16:45Z | about 21:15 to 23:45 |

- **Idle time: 0 h by construction.** The host is rented only when H's own inputs exist, and J1 to J4 fill the time until Gate L. If J1 to J4 end early, Gate L moves earlier.
- Idle rule (skill l.56; CC-388 5(c)): no wait exceeds the setup time, so the host is kept until the removal line and deleted as the next host step.
- Session length about 3 to 5.5 h, at or below the low end of the 5 to 8 h estimate; the caps of section 1.3 cover 8 h and more.

### Variant (b): rent earlier, run J1 to J4 while waiting for the closing line

Needs the PI's yes first (PI-1114l leaves the earlier rental unanswered, default evening).

| Rent at | J1-J4 done about | Wait for the closing line (if at 18:00 VN) plus label preparation | Idle rule |
|---|---|---|---|
| 09:00Z (16:00 VN) | 11:00Z (18:00 VN) | 0 to 0.5 h | below the setup time: keep the host; H starts about 11:15Z (18:15 VN) |
| 07:00Z (14:00 VN) or earlier | 09:30Z (16:30 VN) | 1.5 h or more | **exceeds the setup time: pull, delete after J1-J4, re-rent at the closing line.** That is two rentals; the first is a rental for Papers A and C alone, which no PI line licenses (OPS-1114f) |

- (b) saves nothing on the hard deadline: in (a) H starts at about 20:45 VN at the latest, more than 15 h before K-time.
- (b) depends on inputs that are not ready in the afternoon: `draft_v2/` of the TAIMMA paper was still being revised at 05:15 VN (no `REVISION_NOTES.md` yet) and has no diff read; the J4 scripts do not exist.
- (b) has one real advantage: all agent work ends before any label reaches the host. Variant (a) reaches the same separation with Gate L.

**Recommended: (a).**

---

## 3. The jobs

Order on the host: 3.0 host session, then J1 (first, alone with the code-only trees), G0 for J5, then J2, J3, J4 up to Gate L, then J5. The reasons for this order are in section 5.

### 3.0 Host session steps (skill l.24-30; `B_STAGE_HOST_SETUP.md` §1)

1. **Rent.** Checkout, Ubuntu 24.04 template, random password in a 0600 file. The `date -u` stamp of the rental line is T0.
2. **Access.** Alias in `~/.ssh/config` only (`Host hB hC`); `ssh-copy-id` through an askpass script; BatchMode login, plain and under the run env.
3. **Facts.** nvidia-smi, lscpu, free, df for `/dev/shm` and home, a 4 GB `dd` with direct I/O, OS version, clock skew < 60 s. A fact that contradicts the offer is a FAULT: delete the host; the money still counts.
4. **Packages, all before G0** (so that G0 certifies the final system; CC-389 point 4 and F7; CC-390 ruling 4):
   - `apt-get install -y git tmux rsync util-linux python3.12 python3.12-venv` (skill l.28; HOST_SETUP step 4). This also covers J1's step 0 (`python3.12-venv`, package l.185); record the package version for J1's line.
   - `python3` and `python3-venv` if `/usr/bin/python3` is missing (lesson of OPS-1113cj; accepted by CC-390 ruling 4). `setup_venv`, G0 and J1's runner all call `python3`.
   - `time` for `/usr/bin/time` (CC-388 #7).
   - Java (CC-388 #6): `apt-cache policy openjdk-21-jre-headless` and, after the install, `java -version`, both recorded with dots written as underscores. G0 needs the version string `21_0_13_0_3`. On hB the apt candidate was `21_0_13_0_3+1-1~24_04_1` and was installed by `=<version>` (OPS-1113ch). If the default candidate is newer, take the matching string from `apt-cache madison`. If it is no longer in the archive: STOP; a pin change goes to a diff read; never edit the pin.
   - Confirm `tmux` and `procps` (`pgrep`) are present and record them in the rental line (CC-389 N5).
   - No package is installed after G0. If one turns out to be needed, the conditions of CC-390 ruling 4 and its addendum apply (simulate first, no stage running, re-check Java, freeze and jar, one LOG line); anything outside them is a one-judge read.
5. Nothing of J2/J3 is installed in the system: their tools are unpacked privately (3.2).

OPS lines: the rental line (T0, offer id, L-before with its numbers, spec facts, apt Java candidate, tmux and procps present, licence lines; no host string); a DEVIATION line if the offer is not the cheapest passing one.

### J1. Paper A: the one host test of the per-annotator code

| | |
|---|---|
| Licence | CC-395 (CONDITIONAL GO 89 "to the ONE host test", closed by byte match OPS-1114t); registered row: `A_CERT_ANALYSIS_REG_v1_1.md` §10 l.243 |
| Run doc | `scripts/a_cert/PERANN_READ_PACKAGE.md` §7 (sha256 ba58e66f53860c96d21e234469320127222454aded79c2df0e817deb50947ad5) |
| Sums | `scripts/a_cert/SHA256SUMS_PERANN` (sha256 334a96806460a6b51d30b7a870ff7854a6f1dc68fa89085238afae7a3cf6739c); `sha256sum -c` from `scripts/a_cert/` gives 4 OK (checked while writing this plan); as-read copies in `scripts/a_cert/perann_r2_asread/` |
| Code shas | `a_cert_perann.py` 70efc01d, `a_cert_perann_mutants.py` 08c05517, `a_cert.py` 2e872588, `a_cert_kappa.py` 1a0be694 (CC-395 ruling 8) |

**Commands (all from the package).**
1. Step 0: the host-environment line (package l.185). On this host the package is installed in 3.0 step 4; the J1 line records its version.
2. Step 1 (laptop): re-hash every file of the allow-list (package l.173-179: 25 `rescap` files, 10 scripts, the v3 evaluator, 2 lexicon files, 5 `a_cert` files) against its laptop sha; a mismatch stops the work. Then the one guarded push of package l.190, unchanged, with the host alias filled in. It refuses if `/root/a_perann`, `/root/a_perann_mut` or `/root/a_perann_records` exists.
3. Step 2 (host): the runner of package l.198-217, saved byte for byte as `/root/run_perann.sh` (extracted by script, its sha recorded), started **once**, from outside the tree, in tmux: `bash /root/run_perann.sh`. The command that puts the runner file on the host is **not found in the package**; use the form CC-389 ruling 6 uses for another script (`ssh ... 'cat > /root/run_perann.sh' < file`, then a sha check on the host).
4. Pull the eight records to `scripts/a_cert/host_checks_perann/` (the folder does not exist yet): `status.log`, `selftest_perann.log`, `selftest_perann.json`, `mutants_perann.log`, `mutants_result_perann.json`, `venv_freeze.txt`, `run_perann.sh`, `SHA256SUMS`. Before and after the pull, grep every file for dotted addresses and host names; none may remain (package l.221).
5. Plan step, **not in the package**: after the pull and `sha256sum -c` of the records on the laptop, remove `/root/a_perann`, `/root/a_perann_venv`, `/root/a_perann_mut`, `/root/a_perann_records` and `/root/run_perann.sh` on the host, check each with `test ! -e`, and write one OPS line. Reason: the package forbids `LOG.md`, any label and any `key.json` "on the host" (l.181; CC-395 ruling 8), and stage H later brings all three. With this step J1's tree and those files are never on the host together (section 6, item 4).

**Goes to the host:** only the allow-list files and the runner. **Never:** anything under `data/results/`, `data/datasets/`, `data/xm3600/`; any assignment, overlap list, `BUILD*.json`, `FREEZE*`, `LOG.md` or CC text; `~/vsps_labels*`; any `key.json` or label copy; any token (package l.181). No real label is used: the fixtures are made up in code (package §6).

**Import failure:** stop. Push only the named code file, with a logged line; never a data, label, key or result file (package l.183).

**Acceptance (stated before the run; package l.223; CC-395 ruling 8):** `59 checks; selftest ok`; `61/61 killed`, each KILLED with a non-empty `named_failed` and no `no_exception` entry; `selftest rc 0` and `mutants rc 0` in `status.log`; the `status.log` digest lines of the four `a_cert` files equal the shas above; `script_sha256` = `source_sha256` = 70efc01d. If the host Python is not 3_12_3, record it; this is not a fault (CC-395 N3).

**Fail rule:** a failed acceptance means no rerun and no fix without a judge line; the failed records are kept as such.

**Judge read after:** one judge, records read = round 3 of the CC-391 topic (CC-395 ruling 9); it only confirms the acceptance and the shas. Then the gatekeeper commit of the list in CC-395 ruling 9 (NGRAM scan, staged-blob shas, the records-read CC sha and the CC-395 sha in the message).

**OPS lines (topics):** host reuse with its licence line; step 0 (package version); step 1 push (list sha, rc); runner start and end with both return codes; records pulled with the `SHA256SUMS` sha; removal of the J1 paths; later the commit.

### J2. Paper C: rebuild of the journal tex and PDFs

| | |
|---|---|
| Licence | PI-1113h; OPS-1114f; ticket T1 of CC-400 and of CC-401 ("the tex/PDF rebuild is made from the post-C1 commit; then check that 6.10.1 to 6.10.9 print as typed") |
| Source | repo `/mnt/d/vsps_papers/vsps-paperC-tallip`, commit **6a5d36aeee4c22597b4188bb1d84413f04cabddf** (HEAD when this plan was written; OPS-1114au), folder `paper_v1_analysis/` (42 tracked files) |
| Script | `paper_v1_analysis/tex/build.sh`, sha256 33eb75db8cfcad28c0b39e4c4643055894b1d824d81e1d0c51b5c432e45995f2 at that commit |
| Other inputs at that commit | `tex/preamble.tex` 0c9c2819..., `tex/strip_num.lua` 5a91751f..., `tex/fig1_forest.py` c7d168ca..., `paperC.bib` a415c4da..., `fig1_ret_minus_rand.svg` b2de16dc... (computed with `git show <commit>:<path> \| sha256sum`) |
| Method of record | `.session_backup/2026-11-13/c_tex_build/C_TEX_BUILD_RECORD.md` (sha256 98140a9c8988e472b0526d7343605cfc093c4f78ef3901d8defec39d12caddc3), §1 and §6 |
| Helper files of that build | `~/.cache/vsps_c/scripts/env.sh` c3dd1d86..., `fonts.conf` bbfcba95... (the corrected one), `tl_pkgs_nodot.txt` d06aba5d... (uncommitted; re-hash before use) |

**Steps (the method of the record, §1; done by one build agent under `/root/paperC_build/` only).**
1. Laptop: `git archive` of commit 6a5d36a, folder `paper_v1_analysis`, to a tar; record its sha256. The working tree of the paper repo is **not** the source: it still holds 11 stale generated files of the 13 Nov build (CC-400 N3).
2. Push the tar, check the sha on both sides, unpack under `/root/paperC_build/src/`.
3. Tools, private, **before G0** (3.0 step 5): pandoc 3.5 static binary; the TinyTeX bundle unpacked by hand, then `tlmgr install` of the packages of the laptop list; `rsvg-convert` and `pdfinfo` by `apt-get download` into a private folder and `dpkg -x` (record §6 points 1-4 and C). All commands source `env.sh`. The literal command lines of this setup are **not found in the record** (it describes them in words); this time the agent saves them as one script in the record folder (section 6, item 6).
4. Use the corrected `fonts.conf` **from the first command**. On 13 Nov the first font lookup wrote 15 cache files into the system font-cache folder (record §6 A; OPS-1114k). After the tool setup, repeat the count-only check of record §6 A2 (entries newer than a marker file in the system font-cache, apt, dpkg and temp folders and at the top of `/root`): it must show no new entry before G0 starts.
5. Build: `nice -n 19 bash build.sh /root/paperC_build/src/paper_v1_analysis`, run in `/root/paperC_build/src/paper_v1_analysis/tex` (record §1). At most 4 processes (OPS-1113dc).
6. Host: sha256 list of the tex folder before and after; `grep -c` counts in the two final-pass logs and the two latexmk outputs (undefined, Overfull, Underfull, Missing character, Warning, Error); page counts.
7. Pull the built tex folder and the small records as tars; sha on both sides.
8. Laptop checks (no build on the laptop): page counts and words (`pdfinfo`, `pdftotext | wc -w`), "??" count, and the **6.10 check**: the nine headings of `06_results.md` l.128-254 at that commit, typed `6.10.1 What ran` to `6.10.9 What did not run`, each print in the main PDF with its typed number, and no bold run-in "6.10.1" remains.
9. Copy the changed generated files into the paper-repo working tree, unstaged, each checked byte for byte against the build output (record §7). They replace the stale files of 13 Nov.
10. Check that no process of the build is left on the host. The agent closes its session before Gate L.

**Goes to the host:** the source tar (paper text, bibliography, figure source, build script) and the three helper files. **Never:** any file outside `paper_v1_analysis/`, any data set, label, key, result file, LOG or ruling text.

**Records to pull back:** a new folder `.session_backup/2026-11-15/c_tex_build/` in the form of the 13 Nov one: build record, `VERSIONS.txt` (dots as underscores), the two sha lists, four log files, the setup script.

**Pass rule:** build exit code 0; 0 undefined references and citations in both final-pass logs; 0 "??" in both PDFs; the four inputs (`build.sh`, `preamble.tex`, `strip_num.lua`, `fig1_forest.py`) have the same sha before and after; the 6.10 check holds. A numbering or source finding is reported and **not patched** by the agent (as on 13 Nov); then there is no commit and the finding goes to the next paper-repo diff read.

**Judge read after:** a diff read of the generated files, then the gatekeeper commit in the paper repo (OPS-1113dc: "a diff read and the gatekeeper commit follow"; OPS-1114k: "one more build on the next host and the tex/PDF commit").

**OPS lines (topics):** build launched (commit, tar sha, licence, host use at that moment); build result (exit code, pages, counts, 6.10 check, record sha, every deviation); later the paper-repo commit.

**Known follow-up:** shell C2 of Paper C comes after the K7 line (not before 2026-11-16T05:00:00Z) and changes the text again, so one more rebuild is owed after it (section 6, item 7).

### J3. TAIMMA conference draft: LNCS page count (gate G1 of CC-399)

| | |
|---|---|
| Licence | CC-399 G1: "Compile with llncs and splncs04 and record a page count of 12 to 15 before the READY notice"; Q3 default: next rented host |
| Draft | `manuscript/conf_taimma_2027/draft_v2/paper.md`. At about 05:10 VN 15 Nov its sha256 was 7f329adeb57d6b3ff7a5fe1d0c881755bdb60cf156ead4377ee269674d8f3110 and the folder had no `REVISION_NOTES.md`: **the draft was still being revised** |
| Bibliography | `paper_v1_analysis/paperC.bib` of the Paper C repo at 6a5d36a (a415c4da...) |
| Figure | `paper_v1_analysis/fig1_ret_minus_rand.svg` at 6a5d36a (b2de16dc...), the file the draft links (draft l.220; `DRAFT_NOTES.md` item 8) |
| Build script | **does not exist. To be written and debugged on the host** (specification below) |

**Precondition on the draft.** The G1 count of record is taken only on the `paper.md` bytes that the round-2 diff read of CC-399 (items B1 to B6) has closed, named by sha256, with `check_draft.py` re-run on them. If that read is not closed at run time:
- either wait (J3 simply moves to the end of the J-block and drops out at Gate L),
- or run the build as a **debug build** on the current bytes to finish the script. Its count is labelled PROVISIONAL in the record and is not logged as G1.

A second count is owed in any case after the K7 re-join (CC-399 G2; units C26 and C44 change after 2026-11-16T05:00:00Z).

**What the build script must do** (model: Paper C `tex/build.sh`; proposed path `manuscript/conf_taimma_2027/build/build_lncs.sh` with a `preamble_lncs.tex`; both new files).

1. *Inputs, hashed first.* `paper.md`, `paperC.bib`, the SVG, `preamble_lncs.tex`, the script itself, `strip_num.lua` (reused from Paper C, 5a91751f...), and the class files `llncs.cls` and `splncs04.bst`. The source of the two class files (a TeX Live package installed with `tlmgr` into the private TinyTeX, or the publisher's author kit) is **to be confirmed on the host**; their sha256 and the class version line go into the record.
2. *Pre-processing (layout only; no word changes).* Strip the header comment block (draft l.1-9), every `<!-- p:ID -->` marker and the closing comment under "References" (CC-399 N11). Take the title from the `#` line, the abstract from under `## Abstract`, the keywords from under `## Keywords`, and the author placeholder line; they go into `\title`, `\author`/`\institute` (placeholders), `abstract` and `\keywords` of the class. The body runs from `## 1 Introduction` to the line before `## References`.
3. *pandoc.* The reader and writer options of `build.sh` l.8 (`-f markdown-implicit_figures+implicit_figures+lists_without_preceding_blankline`, `--shift-heading-level-by=-1`, `--lua-filter=strip_num.lua`, `-t latex --columns=100`). The headings carry typed numbers ("1 Introduction", "5.1 ..."): the filter removes them and the class numbers the sections. The four end sections (ethics and data, availability, acknowledgments, interests) are unnumbered; how they are set (the class's credits block or starred sections) is recorded.
4. *Citations.* The result must be numeric LNCS references made by BibTeX with `splncs04` (the words of G1). The draft's closing comment says "pandoc citeproc"; the ruling wins. Whether pandoc's `--natbib` output is kept (with a numeric natbib set-up) or mapped to plain `\cite` is settled while debugging and recorded.
5. *Tables (7 pipe tables, T1 to T7).* pandoc writes them as `longtable` with booktabs rules; the preamble loads what that output needs. The table titles are typed as bold paragraphs ("**Table 1.** ..."), not pandoc captions: for the page count they stay as typed paragraphs above each table. Wide tables (for example T1 with five text columns) must fit the 122 mm text block: any font-size, column-width or `\tabcolsep` setting is a layout choice that moves the page count, so each is listed in the record. `DRAFT_NOTES.md` item 10 (short author names before the bare "[n]" keys in T1) is a text change and is **not** made by the script.
6. *The one figure.* Convert the SVG to PDF with `rsvg-convert -f pdf` (`build.sh` l.5) and point the include at the PDF; set it at text width. Remove the typed "**Fig. 1.**" from the caption so the class numbers it once. Define the macro pandoc 3.5 wraps images in (`\pandocbounded`, seen in `build.sh` l.15). The rebuild of the figure from manifest values as a script-made vector file (writing plan C.4 l.211; CC-399 N5) is a separate owed item (section 6, item 10); it does not change the figure's area, so the page count does not wait for it.
7. *LaTeX.* `latexmk -g -<engine> -interaction=nonstopmode -halt-on-error`, output to a file, last 30 lines shown on a failure (`build.sh` l.38). The engine is recorded. The text holds Unicode signs (minus sign, Greek letters, the infinity sign), so the engine and font choice must print all of them: "Missing character" = 0 is part of the pass rule.
8. *Record (one file plus logs, in a new folder `.session_backup/2026-11-15/taimma_build/`).*
   - sha256 of every input **before and after** (unchanged) and of every output;
   - the exact command lines, UTC start and end, exit code;
   - **page count** (from the LaTeX log and from `pdfinfo`), page size, and the page on which the reference list starts (whether references count toward the limit is a "re-fetch" item of the writing plan §F);
   - **Overfull** and Underfull counts in the final-pass log, with the size and source line of each overfull box;
   - undefined references and citations (must be 0), "??" in the PDF text (must be 0), "Missing character" (must be 0);
   - words by `pdftotext | wc -w`;
   - versions: pandoc, the TeX engine, latexmk, bibtex, tlmgr revision, the class version line, rsvg-convert (dots as underscores).

**Goes to the host:** `paper.md`, the bib file, the SVG, the script, the preamble, `strip_num.lua`. **Never:** the number manifest's sources, any data, label, key, result file, LOG or ruling text. The tools are those of J2 under `/root/paperC_build/` plus the class files; TeX packages found missing during debugging are installed only into the private TinyTeX and listed in the record.

**Pass rule for G1:** the record shows a build with exit code 0 and the three zero counts, on the diff-read bytes, and **12 <= pages <= 15**. Over 15: cut in the plan's §B order (writing plan l.159), never a row of plan A.5. Under 12: restore text from Paper C §5.2 and §7 (CC-399 G1). Both are text changes on the laptop with their own diff read; the host job only measures.

**Judge read after:** none is ruled for the script (not found). The G1 OPS line with the record sha is an anchor of CC-399: GO there needs G1 to G3 logged and the diff read closed (CC-399 Closure).

**OPS lines (topics):** build script written (sha, where it ran); G1 count (draft sha, pages, counts, record sha) or the PROVISIONAL note.

### J4. Paper B: three figures of the held rewrite draft (placeholder)

The scripts do not exist. The held folders were not opened to write this step. The only fact used is the outcome-free line OPS-1114at ("figures 1, 2, EF1 not built").

**The step may run only if all of these hold before Gate L:**
1. The three scripts were written by an agent that is neither a rater nor the PI-facing channel (CC-394 ruling 7(i)).
2. A read of the scripts by one judge is on the LOG. It names the host as the place of the run (no such licence is on the LOG today), the inputs, and confirms that no input holds a label, a key or caption text.
3. Each input is a pinned result file, named by path and sha256 from an existing pin line or sums file, without the coordinator opening it.
4. No figure needs the output of stage H. A figure that does waits for the human result read.
5. The run starts after the new G0 LOG line (before that line the host holds the code tree, the venv, the jar, the runner and no study file: CC-388 ruling 4) and after J1's paths are removed.
6. The scripts work in their own folder (for example `/root/b_figs`). They never create `/root/b_work`, `/root/b_records`, `/root/b_pins`, `/root/ncs-data/datasets` or `/root/ncs-data/results`: `push_new_host` refuses if `/root/b_work` exists, and G0 refuses if any data path exists.

**After the run:** the agent pulls the figures and a sha list into the held folder (444); the coordinator sees exit codes and shas only; figures are vector or at least 600 dpi (project rule). They enter the paper only through the one-judge read of the held package after the closing line (CC-394 ruling 7(vi)).

**If any condition is missing at Gate L:** J4 is NOT RUN in this session and goes to the next host. It never delays J5.

### J5. Paper B stage H

| | |
|---|---|
| Registered | `manuscript/prereg/2026-11-12_b_fecert/B_FECERT_PREREG_v1_1.md` (736b7e6a...) §9 row H l.347, §10 K-time l.369, §13 l.417-418; `B_PREF_LABELLING_PLAN_v1_1.md` (59ae449b...) §6 l.145-151; sums `SHA256SUMS_B_FECERT` (b5cdc6a3...) |
| Rulings | CC-384 ruling 10 (order, stops); CC-388 rulings 4 and 5(c), L19; CC-389 rulings 3 (points 13-17), 4, X16, X17, addendum A2-A3; CC-390 N8 |
| Run doc | `.session_backup/2026-11-13/b_stages_stubs/B_STAGE_H.md` (0e1d8e20...) and `B_STAGE_H.sh` (**4e6839ec3513446edee351fab1f5938063726682ba209aea9644a5d38fd702fd**, the CC-389 TARGET); sums `SHA256SUMS_B_STUBS` (71a4e15c..., 5 OK); 444 snapshot `.session_backup/2026-11-13/b_stages_stubs_snapshot_cc389/` |
| Stage package | `.session_backup/2026-11-13/b_stages/`: `B_STAGE_RUNNER.sh` 7b2be4d6..., `b_stage_push.sh` 0b4eb57d... (CC-390 TARGET), sums `SHA256SUMS_B_STAGES` 0c4abe59... |
| Code | commit 9e6578a0095de817a827911e8db7852306d7f390 (stage 0b); no code edit is allowed (CC-384 ruling 10) |
| Pinned work files | source folder `.session_backup/2026-11-13/b_stages/host_pull/20261113T174234Z/b_work/` (444): `FAMILY.json` 431d92a4a2eaf0516446c9f9aef453ee52d311b6e329d97cd1abb4c4e8017f77 (OPS-1113cr-pin), `PAIR_CANDIDATES.json` 2274d989fe92c329ed5fed9dce52f6e1c17151c10d8059a79f52bc6d53c0eb3e (OPS-1113cx-pin), `FEID.json` 1f56a5ce8c5fd434b19409322d275478ec999d41d34447cfca719a35b040b1f7 (OPS-1114d-pin) |

All shas in this table were re-computed or read from the LOG while writing the plan; the three work files themselves were not opened. Re-run `sha256sum -c` on both sums files before the first host step.

**Steps.** Every call by absolute path (CC-390 N8). "Laptop" steps are the coordinator's own; no agent runs them.

1. **Laptop, pushes before G0** (`B_STAGE_HOST_SETUP.md` steps 7-9; no LOG copy yet because of J1):
   `bash .../b_stages/b_stage_push.sh tree`, then `... vnc`, then `... runner`.
   Expected: 34 files of `git archive 9e6578a`; 8 VnCoreNLP files with `sha256sum -c` OK; the runner sha on the host = 7b2be4d6.
2. **Host, in tmux** (helper `~/.cache/vsps_b/bh.sh <tag> setup_venv`, then `bh.sh <tag> g0`): `B_STAGE_RUNNER.sh setup_venv`, then `B_STAGE_RUNNER.sh g0`. `setup_browser` is **not** needed (CC-389 point 16). G0 runs only after every step of 3.0 and the private tool setup of J2/J3 is finished. Expected values are in the runner (freeze 31e1f303, wheel list equal, Java string, jar 9e2811cd, runs 1 to 5). No study data is on the host at G0; G0 refuses if a data path exists.
   - ENV mismatch: fix the environment, never a pin; retry with `g0 --rerun-infra <LOG id>`, each retry with its own LOG id (this retry needs the LOG copy on the host, so J1's paths must be gone first); old records stay in `G0_attempt_<UTC>/`.
   - CODE mismatch: back to a judge. **No data and no label is pushed after any G0 miss** (CC-384 l.225-226; CC-388 #13).
3. **New G0 LOG line** (pipe form `<UTC>Z | <id> | ...`, with the token `G0`; content as L6 of CC-388 ruling 7 and W2: shas of `G0_TREE_SHA256.txt`, `G0_freeze.txt`, `runs.log`; the five run results; the statement that the 34 code lines equal the laptop listing of the same archive). The id is what `--g0-log` takes.
4. **Laptop:** `bash .../b_stages_stubs/B_STAGE_H.sh push_new_host --work-src .../host_pull/20261113T174234Z/b_work --g0-log <G0 id>`. It pushes the three pinned work files, each checked against its pin line, and KTVIC `test_data.json`.
5. **X16 check (CC-389 X16, W12), before `run`:** the sha256 of the pushed `/root/ncs-data/datasets/ktvic/test_data.json` equals the entry for that file in the L8 data-push manifest (manifest sha256 32b22ae93e56a1fd0592554fd68f404bbb0fe115f90f70b6f99609167cf4c0a0, OPS-1113cq; pulled copy `.../host_pull/20261113T174234Z/b_records/DATA_MANIFEST.sha256`). The command is **not found in the rulings**; it is a read-only `sha256sum` through the filtered ssh, compared with the manifest line, and it goes into an OPS line.
6. **Gate L** (section 5): J1 pulled and removed; J2, J3, J4 pulled or stopped; no agent session open on the host.
7. **Laptop:** `b_stage_push.sh log` (prints `--log-sha`).
8. **Laptop:** `B_STAGE_H.sh push_labels --closing-log <closing id> --key ~/vsps_labels_b/b_pref/key.json --pi <444 copy of PI> [--r2 <444 copy of R2>]` (section 4). Then `b_stage_push.sh log` again; use the sha it prints.
9. **Host:** `bash /root/B_STAGE_H.sh check --closing-log <closing id> --log-sha <sha>`.
10. **Host, inside tmux (binding, CC-389 F5 and W12):** `bash /root/B_STAGE_H.sh run --prev 1f56a5ce8c5fd434b19409322d275478ec999d41d34447cfca719a35b040b1f7 --pin-log OPS-1114d --closing-log <closing id> --log-sha <sha>`. The stage call inside is `b_fecert.py H --work W --log L --prev <FEID.json> --labels DIR` with `CUDA_VISIBLE_DEVICES=`, `nice -n 19`, `python -I -B` (`b_fecert.py` l.20; CC-384 l.169). `bh.sh` wraps only `B_STAGE_RUNNER.sh`; a tmux wrapper for `B_STAGE_H.sh` is missing (section 6, item 2). While H runs, nothing else runs on the host and nobody calls `wipe`.
11. **Laptop:** `B_STAGE_H.sh pull`: records `H.*`, `H_*` and `HUMAN.json` go to `.session_backup/2026-11-13/b_stages/host_pull/H_<UTC>/` (444, sha on both sides); the host then runs `wipe`.
12. **Laptop:** `b_stage_push.sh pull` once more, for the remaining records of this host (G0 records, `setup/`, `WIPED_H`): CC-389 addendum A2(b) requires the work files and records pulled with sha on both sides before deletion. A pull is not a new job.
13. **LOG lines, then deletion** (CC-388 L19; CC-389 addendum A2(c)): pin-form line for `HUMAN.json` (sha from `H.outputs.sha256`; sha only); the removal line; delete the instance on the panel as the **next host step, with no new job on the host**; L-after.

**Return codes of `run`** (CC-384 l.185-187; CC-388 #18; CC-389 F2, F5):

| rc | Meaning | Next |
|---|---|---|
| 0 | ended | pull, wipe, pin line, removal line, delete |
| 3 | FAULT (the script writes `CHAIN_STOP`) | final: pull, wipe, removal line, delete; no re-run |
| 4 | infrastructure | labels stay; ONE re-run with `--rerun-infra <LOG id>` after a LOG line names the shown cause (re-push the LOG copy, new `--log-sha`); only before K-time |
| 1, 2 | refused / argument error | no automatic re-run; labels stay; a one-judge read decides (before any input was read: records moved aside by a logged step and a plain first run; otherwise NOT RUN) |
| start record without rc (ssh drop, reboot) | unknown | `run` refuses; a one-judge read decides |

**Never on the host:** `~/vsps_labels/` (Paper A), `~/.vsps_sealed`, `assignment.json`, `practice.json`, `BUILD.json`, KTVIC images, `scripts/kit_b/pilot_results.json`, the data files of the 13 Nov stages other than `test_data.json` (H reads none of them), any file not listed in step 4 or 8 (CC-388 ruling 4; `B_STAGE_HOST_SETUP.md` §5).

**Pass/fail rule of the host step (not of the study):** the step is done when a final H return code exists, the records and `HUMAN.json` are pulled with equal shas, the wipe is complete and the removal line is written. The study's labels are not computed, read or written by the coordinator; they belong to the result read.

**Judge read after:** one judge, the human result read of prereg §13 l.417; the tier is stated by that ruling (the result read of the earlier stages, CC-394, was read at the IRREVERSIBLE tier). Then the result commit, which is allowed only after the closing line (CC-394 ruling 6), and the human-arm text of the held draft only after that read (CC-396).

**OPS lines (topics):** tree and jar pushed; environment steps; **new G0 line**; work files and `test_data.json` pushed with the X16 check; Gate L; labels pushed (shas equal on both sides, time); `check` result; H start and end with rc (status only); pull (list sha); `HUMAN.json` pin line; records pull; **removal line**; host deleted with L-after; hand-off line.

---

## 4. Custody for J5

```
+--------------------------------------------------------------------------------------------------+
| CUSTODY BOX: Paper B label material                                                              |
|                                                                                                  |
| C1  CLOSING LINE FIRST. Both rating sessions are stopped (each with its session-end line) before |
|     the closing line, so no answer can be written after it (CC-389 point 15). The coordinator    |
|     appends ONE pin-form line (CC-388 5(c)(i)):                                                  |
|       <date -u>Z OPS-<id>-pin: key.json <sha> labels_PI.jsonl <sha> labels_R2.jsonl <sha>        |
|       (closing, plan §6)                                                                         |
|     Latest 2026-11-15T11:00:00Z (18:00 VN). If R2 has no file, the R2 pair is left out. If R2's  |
|     file exists, it is carried and pushed, finished or not; the code decides (CC-389 point 14).  |
| C2  WHICH FILES. Exactly two or three, named by path only, never listed or opened:               |
|       ~/vsps_labels_b/b_pref/key.json                                                            |
|       ~/vsps_labels_b/b_pref/labels_PI.<closing UTC>.jsonl   (444 copy)                          |
|       ~/vsps_labels_b/b_pref/labels_R2.<closing UTC>.jsonl   (444 copy, only if R2 has a file)   |
|     One 444 copy of each live label file is made at the closing line, or the last session's copy |
|     is used if its sha equals the live file's (CC-389 point 15). The closing line carries the    |
|     shas of these copies.                                                                        |
| C3  BY WHOM, WHEN. The coordinator only, with `B_STAGE_H.sh push_labels`, passing the paths. No  |
|     agent. Only after the closing line is in the laptop LOG, before K-time, and only when the    |
|     host has passed G0 and holds FEID.json and test_data.json (the script refuses otherwise:     |
|     CC-389 F1). One push only: the script refuses if /root/b_labels_H exists.                    |
| C4  ARRIVAL CHECK. push_labels checks that the copies are 444, that the closing line carries     |
|     their shas, and that the host files have the same shas. Then on the host `check`: the folder |
|     holds exactly key.json, labels_PI.jsonl[, labels_R2.jsonl], mode 444, equal to the closing   |
|     line in the LOG copy whose sha is --log-sha.                                                 |
| C5  WHILE THE LABEL FOLDER EXISTS. No agent session on the host; no other job; no listing of the |
|     folder; no backup loop (C9). Plan rule, stricter than the 13 Nov practice.                   |
| C6  WIPE. `B_STAGE_H.sh pull` calls `wipe` on the host: label folder first, then the data paths, |
|     each path tested gone, marker WIPED_H (CC-389 F2, F4). It runs only after a FINAL H (rc 0 or |
|     3, or the re-run's rc) was pulled, or after K-time; never while H runs. After rc 4 or rc 1/2 |
|     the labels stay for the re-run or the one-judge read. The runner's own `wipe` is not used    |
|     (CC-389 X17). Then the removal LOG line; deleting the instance is the removal of everything  |
|     else. If H is NOT RUN before K-time after the labels were pushed, the host is deleted at     |
|     once with a removal line (CC-389 point 17).                                                  |
| C7  NO RESULT OF STAGE H ON THE INVESTIGATOR CHANNEL. The terminal shows only STAGE, FAULT,      |
|     ERROR and REFUSED lines and the rc (B_STAGE_H.md, Records). The coordinator does not open    |
|     HUMAN.json, H.stdout or H.stderr, on the host or after the pull, and writes no figure, count |
|     or label word from them into the LOG, the dashboard, a report or a message. The PI is told   |
|     stage status only: ran or not run, rc, sha. The results are read first by a judge (prereg    |
|     §13 l.417; research-cycle gate 6); the PI sees them after that read.                         |
| C8  COMMITS. key.json, label files and result files are committed only after the closing line,   |
|     by the gatekeeper, under the result read (plan l.146; CC-394 ruling 6). The pulled H files   |
|     are never committed without a ruling (CC-389 addendum A3).                                   |
| C9  BACKUP LOOP OFF. The 30-minute host backup helper copies the host's home folder. With labels |
|     and the key there it would copy them into backup folders. It is not started for hC. The      |
|     sha-checked pulls of section 3 are the only copies.                                          |
| C10 OTHER HOLDS UNCHANGED. ~/vsps_labels/ (Paper A) and ~/.vsps_sealed are never touched;        |
|     BUILD.json is not opened in the repo or on the remote before the closing line (CC-393).      |
+--------------------------------------------------------------------------------------------------+
```

---

## 5. Order, parallel work, stop rules

### 5.1 Order and why

1. **Host session (3.0).** Every system package before G0.
2. **J1 first**, as soon as `python3` and the venv package are there. Its package forbids `LOG.md`, labels and keys on the host, so it must be finished, pulled and removed before the LOG copy arrives (step J5.7).
3. **Paper B pushes and `setup_venv`** in parallel with J1 (separate paths, no LOG copy).
4. **Private build tools** for J2/J3 in parallel, finished and checked before G0.
5. **G0**, the G0 line, `push_new_host`, the X16 check. From here J5 is ready except for the labels.
6. **J2, then J3, then J4** (if its conditions hold), all before Gate L.
7. **Gate L**, then **J5** steps 7 to 13, then deletion.

J1 to J4 come before the labels for two reasons taken from the rulings. (i) After the removal line the next host step is the deletion, "with no new job on the host" (CC-389 addendum A2(c)), so nothing can follow H. (ii) No agent should work on a host that holds the labels and the key (C5). H does not lose its deadline by this: Gate L is at 20:45 VN at the latest, more than 15 h before K-time. A judge reading that would allow H first is listed in section 6, item 13.

### 5.2 What may run in parallel

| At the same time | Allowed? |
|---|---|
| J1 runner (2 threads, `nice -n 19`, `ionice -c3`) + Paper B tree/jar/runner pushes + `setup_venv` + private tool setup | yes: separate folders, CPU only, no shared file |
| G0 (mutants with `--jobs 4`) + J1 runner still going | yes on a host of at least 8 cores / 16 threads; neither reads the other's paths |
| J2 build or J3 build (at most 4 processes, `nice -n 19`) + J1 | yes (precedent OPS-1113dc: the build ran beside a Paper B stage, own folder only, no system change) |
| J2 and J3 builds | one after the other: same tool folder, same agent |
| J4 + J2/J3 | yes, own folder, after the G0 line |
| **Anything + stage H, or anything while `/root/b_labels_H` exists** | **no** (C5) |
| Any `apt-get install` after G0 | no, except under CC-390 ruling 4 and its addendum |

### 5.3 Stop rules

| Event | Rule |
|---|---|
| A host fact contradicts the offer | FAULT: delete the host; the money counts; a new rental needs its own L-before (skill l.27) |
| L-before fails | nothing is rented; the PI is asked at once |
| Any sums or sha check fails (tree against both SUMS, jar files, runner, J1 allow-list re-hash, J2 tar on both sides, work files against their pin lines, label copies on both sides, any pulled list) | that job STOPS; nothing of it proceeds. For J5: no label push after any miss. The same file failing a second time: STOP and read (skill l.39) |
| G0 miss | ENV: fix and retry with its own LOG id; CODE: judge. No data, no label |
| J1 acceptance fails | no rerun, no fix without a judge line; records kept; J1's paths are still removed before the LOG copy |
| J2 or J3 build fails or finds a source defect | reported, not patched on the host; no commit; the job ends; it never delays Gate L |
| **Gate L time box: T0 + 2 h 30 min** | whatever of J2, J3, J4 is unfinished is stopped by its own pid file (skill l.44-47), pulled as incomplete and carried to the next host or, for J3, to the PI's answer on CC-399 Q3. J1 is the exception: it is never signalled (it runs once); if it is still running at Gate L, the LOG copy waits for it |
| A pushed stream stalls (under 50 KB/s for 10 min while a fresh probe is 10 times faster) | stop it by pid, top up from a stdout-only failing list, DEVIATION line (skill l.35-39) |
| H rc 3 | FAULT: final; pull, wipe, removal line, delete |
| H rc 4 | one infrastructure re-run with a LOG id, before K-time |
| H rc 1 or 2, or a start record without rc | STOP; labels stay; one-judge read |
| Host lost before the label push | re-rent: the skill asks for the PI's licence and a one-judge read of a short machine-loss addendum (l.55); see section 6, item 14. New G0, new G0 line |
| Host lost after the label push | STOP; delete the instance on the panel if it is still listed; one-judge read (an H start without rc is never restarted by the coordinator: CC-389 F5); a removal line states what was on the host |
| Planning line (this plan's own, not registered): first H start later than **2026-11-15T21:30Z (04:30 VN, 16 Nov)** | report to the team lead at once: the reserve of 3 h for a run, 3 h for one re-run and 1.5 h for a re-rental is used up |
| **K-time 2026-11-16T05:00:00Z (12:00 VN, 16 Nov)** | **If H has not finished by this instant, it is NOT RUN** (prereg §10 l.369, §13 l.418). `B_STAGE_H.sh run` and the code refuse to start at or after it, and the code makes a later finish a FAULT (`b_fecert.py` l.1407-1408, l.1432-1433). At 05:00:00Z, with no final H return code: the coordinator writes the NOT RUN line (status only), runs `wipe` (allowed after K-time), writes the removal line and deletes the host at once (CC-389 point 17). K-time cannot be moved now: it sits in the committed code and no code edit is allowed (CC-389 point 13) |
| Balance | warn the PI at 50,000 VND, or 12 h before it runs out during a live rental (section 1.3) |
| After any FAULT | only the job script's run is a record; a direct call is an INFRA PROBE (skill l.65) |

Whether a stage H process that is still running at K-time may be stopped by a signal is **not found in the rulings** (section 6, item 16).

---

## 6. Missing before the session

| # | Missing item | Who can produce it |
|---|---|---|
| 1 | **A closing-line helper.** `~/.cache/vsps_b/sessions.sh` has `b-start` and `b-end` but no closing command. `bpin.sh` writes a pin-form line but then pushes the LOG copy to the host alias; that is harmless before the rental and wrong while J1's tree is on the host. The closing line is written before renting | coordinator |
| 2 | **A tmux wrapper for `B_STAGE_H.sh run`.** `bh.sh` calls only `B_STAGE_RUNNER.sh`. Coordinator helper, not study code, same form as `bh.sh`, with the same withholding of FAULT and ERROR text | coordinator |
| 3 | **The ssh alias.** The ruled scripts need the alias `hB`; one `Host hB hC` entry for the new machine, the old entry removed | coordinator |
| 4 | **J1 on a shared host.** (a) The laptop sha list of the allow-list files (the package gives shas for the `a_cert` files only; the others are "at its laptop sha"). (b) `run_perann.sh` extracted byte for byte from package l.198-217, with its sha. (c) The command that puts the runner on the host is not in the package. (d) The removal step of J1's paths and the reading that the package's "forbidden on the host" list is met by removing J1 before the LOG copy and the labels arrive are this plan's, not a ruling's. (e) Step 0 says "nothing else installed or upgraded", while this host also gets the Paper B packages before it | coordinator for (a)-(c); one judge line for (d) and (e) if the coordinator wants them ruled before the run (recommended: yes, a short reversible line) |
| 5 | **J1 round-3 records read** (owed after the run) and its commit | one judge; gatekeeper |
| 6 | **J2 setup script.** The 13 Nov record describes the private tool setup in words; the literal commands are not on file | the build agent, saved into the new record folder |
| 7 | **J2 follow-ups.** The diff read and paper-repo commit of the rebuilt files; one more rebuild after shell C2 (after the K7 line, not before 2026-11-16T05:00:00Z), for which no host is planned | one judge; gatekeeper; coordinator plans the later build |
| 8 | **J3 build script and preamble** (`build_lncs.sh`, `preamble_lncs.tex`): to be written and debugged on the host. The source of `llncs.cls` and `splncs04.bst` is to be confirmed there | a build agent (the J2 agent) |
| 9 | **J3 draft readiness.** `draft_v2/` complete (`REVISION_NOTES.md`, `CHECKS.md` re-run on the final sha) and the round-2 diff read of CC-399 B1-B6 closed; otherwise only a PROVISIONAL count | the revising agent; one judge |
| 10 | **J3 owed after this session.** Figure 1 rebuilt from manifest values by a script, with a hand check of the plotted values (writing plan C.4; CC-399 N5); the second page count after the K7 re-join (CC-399 G2); the PI's answer to CC-399 Q3 (laptop or host for page builds; default host) | a figure agent; coordinator; PI |
| 11 | **J4 scripts** for figures 1, 2 and EF1 of the held draft, their input list by sha, and the rule for where the outputs are kept | a non-rater agent; the coordinator names inputs by sha without opening them |
| 12 | **J4 read and licence.** No LOG line licenses the figure run on this host or reads the scripts | one judge |
| 13 | **Optional reading to let H go first.** May J2 to J4 continue after H's wipe and before the deletion, given that no label or data file is left? Today CC-389 addendum A2(c) says no new job. Default in this plan: J1 to J4 first, with the Gate L time box | one judge |
| 14 | **Re-rental after a lost host.** The skill asks for the PI's licence and a one-judge machine-loss addendum; the PI may be asleep during the session. Question to the PI before the evening, recommended answer: yes, one re-rental for stage H is licensed in advance (precedent PI-1108i). Default: wait for the PI's line | PI; one judge for the addendum |
| 15 | **STATE update.** The newest STATE says no live rental and predates the closing line; a new STATE block for the rental (T0, offer, L-before, cap, alias) | coordinator |
| 16 | **H still running at K-time.** No ruling says whether the process may be stopped by a signal. Default until ruled: do not signal it; let the code write its own end; the 18 h cap bounds the cost | one judge |
| 17 | **X16 command.** The comparison of the pushed `test_data.json` sha with the L8 manifest entry has no command in a ruling; a read-only sha comparison is used and logged | coordinator |
| 18 | **Stage H timing.** No measured or registered time exists; the reserves of section 5.3 are this plan's assumptions | measured in the run and logged (report only) |
| 19 | **The request for the human result read**, written outcome-free, with the file list by sha | coordinator; then one judge |
| 20 | **Fresh balance and offer.** The balance of section 1.3 is the last logged one (13 Nov); the rate is that of the previous offer | coordinator, on the panel, just before renting |
| 21 | **Variant (b) only:** the PI's yes to an earlier rental | PI |

### Not found in the documents read

- A licence line for J4 on a rented host (item 12).
- The literal tool-setup commands of the 13 Nov Paper C build (item 6).
- A command for the X16 check (item 17) and for placing J1's runner on the host (item 4c).
- Any timing of stage H (item 18).
- A rule for a stage H process still running at K-time (item 16).
- A ruled read for the J3 build script.
- A closing-line command in the session helper (item 1).
