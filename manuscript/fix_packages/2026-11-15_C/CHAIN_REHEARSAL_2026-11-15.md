# Paper C freeze chain: rehearsal and runbook (read-only check, 2026-11-15)

Made 2026-11-15, 11:12:28Z to 11:41:35Z (both stamps from date -u). Read-only: nothing was written to the LOG or to the paper repo, nothing
was staged, and no script ran in a write mode. Paper repo /mnt/d/vsps_papers/vsps-paperC-tallip: HEAD 55315ca, the
same 12 dirty paths before and after (11 modified files under paper_v1_analysis/tex/, untracked
docs/CC309_PARAGRAPH_DRAFT.md), nothing staged.

Chain: (1) freeze line, (2) shell C2, (3) read and commit C2, (4) package v2 (CC-408), (5) package v4 plus Annex B
(CC-413), (6) package v5 (CC-423), (7) tex rebuild. Nothing may happen before 2026-11-16T05:00:00Z.

CC-423 was written at 11:15:45Z, during this check (CONDITIONAL GO 88, CC sha 734009b0...). It is no longer
pending. Step 6 below follows it.

---------------------------------------------------------------------------------------------------------------------

## 1. Pins (sha256 on disk, 2026-11-15)

| file | expected (who pins it) | on disk |
|---|---|---|
| manuscript/prereg/2026-11-11_c_attr_dev/paper_text/transfer/c_attr_c2_transfer.py | 030c369d... (apply_c_v2_cc408.py PINS; CC-408) | 030c369d97f8668c7f82c8a05a046811e9d95da77272a63055f85f511e9da56c OK |
| manuscript/prereg/2026-11-11_c_attr_dev/paper_text/C_ATTR_B3_PAPER_TEXT_v1.md | e3820d3b... (c2 PKG_SHA) | e3820d3bf93f4246913c6eb651373965303d4afb31fc51fc3db48687ab2904f6 OK |
| manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_DEV_PREREG_v1_1.md | 44f81329d418 (c2 PREREG_SHA12) | 44f81329d418efef823d466a4dca5fc9943817322cb3eef0afec7318c9d7681a OK |
| .session_backup/2026-10-13/decisions/CC-408.txt | ae06c9f5... (task; v2_cc408 PINS) | ae06c9f57edfb51fa561d190dd75562dee72dba3f7006bcf1e81d358879de3b5 OK |
| manuscript/fix_packages/2026-11-15_C/C_FIX_PACKAGE_v2.md | 2653ec72... | 2653ec721b4442b450b973d813c085f23b2b116f47cfba9cc3b4e3e80dcea171 OK |
| manuscript/fix_packages/2026-11-15_C/apply_c_v2.py | 382c1735... | 382c1735ec818cd2e6561da7b920fbb9e34ea50e882f6ce4da18b3d98afebc79 OK |
| manuscript/fix_packages/2026-11-15_C/apply_c_v2_cc408.py | 69e45cc1... (CC-411 l.151; LOG) | 69e45cc1cf6d0a90214fec294920ff4e8d5cc5008058782defadb898353dc6ac OK |
| manuscript/fix_packages/2026-11-15_C/C_FIX_PACKAGE_v4_search.md | 61ace3ab... | 61ace3ab74fa7003265d2418e120fe5777577a6aaf15cb7e9529c476f55a4908 OK |
| manuscript/fix_packages/2026-11-15_C/apply_c_v4_search.py | 2660d082... (v5 V4_SHA256) | 2660d082128cecc5020550c2cff51a760a2bde7b0ef41b4e0e9195dc21c04a9f OK |
| .session_backup/2026-10-13/decisions/CC-413.txt | b9c9ec64... (task; v5 CC413_SHA256) | b9c9ec64c7120b8f10622559ce43caae5078349a2e7a796e02fba26c508bc2be OK |
| Annex B of CC-413 (bytes strictly between the markers) | 3fb2a675... | 3fb2a675a822a1742c70c283426ca2a89b25180abe3267d118611b8359fc0b00 OK |
| manuscript/fix_packages/2026-11-15_C/C_FIX_PACKAGE_v5_audit.md | 29cd9b78... (v5 PKG_SHA256; CC-423) | 29cd9b7882182067e06b51114784c126b1b9738ef7248e41724ee14205f371f8 OK |
| manuscript/fix_packages/2026-11-15_C/apply_c_v5_audit.py | object read by CC-423: 24615559...; to run: f80bb672... (CC-423 W2) | 24615559c0f3724d48a355b5bcedfc2646e8d48374d18a641382c6df91de0c45 (the read object; the f80bb672 variant does NOT exist on disk, see step 6.1) |
| .session_backup/2026-10-13/decisions/CC-423.txt | 734009b0... (LOG line CC-423) | 734009b0a5a29bd06b7b08d06cd41c84254cb68bf01c3ab1c44f1475b4d46820 OK |
| scripts/c_attr/block0/MUTANTS_LOG.txt | a7eef59372d5 (v5 C-M02 row 22) | a7eef59372d5f25dac1d285fdbefccf0c6fa4b73f4dd66b61f432f5072726bbf OK |

Paper repo files at HEAD 55315ca (start values of the chain): 00 4c023726, 01 b731e637, 02 8dbc299b, 03 2da4f2e5,
04 f7d1d0e7, 05 8e635ee2, 06 5443fe5e, 07 72adbcb0, 08 72f3cd8b, 09 4111d095, 10 83d466df, 11 025d744a,
STUDY_BRIEF_C 61f54eb9, V2_PROGRESS_C c208ed1b, number_manifest_C.tsv 83414dc3, paperC.bib a415c4da,
paperC_bib_audit.tsv a1af3339, docs/TABLE1B_W5_EVIDENCE.md 11a291b3, scripts/paperC/c_pass2_check.py a257bd14;
paper_v1_analysis/tex/readme.txt does not exist.

## 2. Check modes today (python3 -I -B, no argument, against HEAD 55315ca)

| script | result | rc |
|---|---|---|
| c_attr_c2_transfer.py | NOT RUN. It has no check mode: its only mode writes. Read in full instead (section 3). Run today it would stop at the freeze-line gate (0 freeze lines in the LOG) before any write, but the task forbids running it. | — |
| apply_c_v2_cc408.py | CHECK on an in-memory after-C2 tree (built from 9b8e6ae with c2's own swap calls and a dummy stamp): 10 of 10 files EQUAL the Ruling 9 targets; manifest byte rule met (bae57439) | 0 |
| apply_c_v4_search.py | order gate "package v2 is NOT committed yet", which is the expected reason. File 11 built in memory at 5a71a8a0; 15 blocks; content checks pass; 5 of 5 OK; ALL RESULTS EQUAL TARGETS | 0 |
| apply_c_v5_audit.py (24615559, SKIP = ()) | order gate "the CC-413 commit does NOT exist yet", which is the expected reason. 13 blocks; 7 of 7 OK; manifest without freeze row fa91f428 OK; C-M03 counts (271, 258, 29, 20) | 0 |
| apply_c_v5_audit.py variant f80bb672 (SKIP = ("C-A13",)), scratch copy | same order gate; 12 blocks; 6 of 6 OK; manifest fa91f428 OK; ALL RESULTS EQUAL TARGETS | 0 |
| annex_b.py (extracted to scratch, no --write, default DIR = paper repo) | stops with "02_related_work.md is not at its package v4 target", which is the expected reason (v4 has not run) | 1 |

## 3. c_attr_c2_transfer.py: what it requires (read in full, 141 lines)

Hard-coded paths: run repo, paper repo, LOG. There is no option for another path and no check mode. It never runs
git add or git commit.

Gates, in order. The script asserts each one and stops before any write if one fails:
1. Package C_ATTR_B3_PAPER_TEXT_v1.md has sha256 e3820d3b...; four wording literals are present in it.
2. `git status --porcelain` is empty for the five files: paper_v1_analysis/06_results.md, 05_preregistration_and_analysis.md,
   07_disclosures.md, 03_method.md, number_manifest_C.tsv. The dirty tex/ files do not block it.
3. 6a5d36a (shell C1) is an ancestor of HEAD.
4. 06_results.md holds the heading "#### 6.10.9 What did not run" exactly once.
5. The freeze-line gate. It reads the LOG:
   - It counts every LOG line that contains the freeze-line id suffix followed by a colon. There must be exactly one
     such line in the whole LOG, and it must match `<stamp> OPS-<id>` + suffix + `: ` at the line start, with
     `<id>` in `[0-9a-z]+`. So the line takes NO " | " separators (the usual LOG form fails) and no hyphen inside `<id>`.
   - Stamp: `YYYY-MM-DDTHH:MM:SSZ` (regex `\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ`), at or after 2026-11-16T05:00:00Z, and not
     later than the script's own clock (time.gmtime) when it runs.
   - The block-4 NOT RUN phrase is in the line.
   - The line equals, as a string, the template line of the docstring (l.12) with only `<utc>` and `<id>` replaced.
     A trailing space, a wrapped line or any edited character makes it refuse.
6. Each OLD occurs exactly once before its swap and each NEW exactly once after. Registration v1.1 has prefix
   44f81329d418 and holds the quote "40 hold only KTVIC images". The manifest ends with a line break and does not
   already hold either new row.

What it writes: the five files. 06 gets the full B2 sentence and the block-4 paragraph after "Block 3 ran (Section
6.10.8)."; 05 changes "ends" to "ended"; 07 gets " Block 4 was not run before the freeze (Section 6.10.9)."; 03 gets
" Section 6.10.9 states whether they ran.". The manifest gets two rows at the end: the freeze row, whose hash cell is
the first 12 hex digits of the sha256 of the LOG line, and the row for 40. It prints `paper HEAD`, then sha256[:16]
of each file in the order 06, 05, 07, 03, manifest.

Freeze-line gate rehearsed on scratch LOG copies, with the gate's asserts copied and the clock set to
2026-11-16T05:10:00Z:

| line | result |
|---|---|
| template, stamp 2026-11-16T05:00:01Z, id 1116zz | PASS |
| same with " \| " before OPS (usual LOG form) | REFUSED (0 well-formed, 1 mention) |
| id with a hyphen (1116-zz) | REFUSED (0 well-formed, 1 mention) |
| stamp 04:59:59Z | REFUSED (before the freeze) |
| stamp 12:00:00Z (VN time written with Z) | REFUSED (in the future until 12:00Z) |
| trailing space | REFUSED (differs from the template) |
| line present twice (a later line quotes it) | REFUSED (2 mentions) |

Today the LOG holds 0 lines that contain the freeze-line id suffix. The LOG ends with a line break.

## 4. Whole-chain simulation (scratch clone)

The scripts take no other path, so none was run against the scratch copy. Instead,
/tmp/claude-1000/-mnt-d-vsps-image-captioning/cbc155a0-619c-4f6d-b27a-ab9635fb7056/scratchpad/sim_chain.py
(sha256 f5a5e3856e98161d04a6b258fa91ad731b8a4a3e35fde2835512d781561ec7ee) did the following:
- It cloned the paper repo at 55315ca and copied the 12 dirty paths into the clone.
- It used a scratch LOG copy with one dummy freeze line (stamp 2026-11-16T05:00:01Z, id 1116zz).
- It called only the scripts' pure functions: c2 swap/c2a_text/k7_template, v2 gate/build, v4 check_content,
  v5 check_content/manifest_step. No main() was called.
- It re-ran each write mode's git gates itself on the clone.
- It ran annex_b.py with DIR = the clone. This is the one script that takes a path.
- It made each commit with the exact add list, checked that the staged list equals that list, and checked that the
  tree is left dirty with exactly the 12 tex/docs paths.

| step | result on the clone |
|---|---|
| C2 | gates pass; 03 45888a88, 05 0137bb6b, 06 68f77eb9, 07 c91bcf31 (= the PRE of apply_c_v2.py and Ruling 6 (iv)); row 40 6b0d2217; path-scoped diff 5 file sections, 13,231 bytes; commit 5 paths |
| v2 | write-mode path on the REAL after-C2 tree, with 02 at its 55315ca text 8dbc299b (the check mode uses the 9b8e6ae text of 02): gate passes, 10 of 10 targets equal, manifest byte rule met, 02 unchanged; commit 11 paths |
| v4 + Annex B | order gate "v2 committed" (11 at 5a71a8a0); 15 blocks; content checks pass; 5 of 5 targets; annex_b.py OK x3 (02 b9f0c1f8, evidence ed7608d0, 11 c4a24cd4); commit 5 paths |
| v5 (f80bb672) | order gate "CC-413 state at HEAD"; 12 blocks; 6 of 6 targets; step-2 gates pass after step 1 (readme absent, HEAD still at the CC-413 state, nothing staged, manifest clean, step 1 on disk); manifest without freeze row fa91f428; commit 7 paths |

The simulation also showed the l.260 stop: with SKIP = () (24615559), step 1 writes tex/readme.txt and step 2 then
stops at l.260 ("tex/readme.txt exists already"). No order of the two write modes avoids it, because step 2 also
re-reads every step-1 file, the readme included. This is CC-423 W2, closed by the f80bb672 variant.

## 5. Runbook

Shell variables used below:

```
RUN=/mnt/d/vsps_image_captioning
P=/mnt/d/vsps_papers/vsps-paperC-tallip
FIX=$RUN/manuscript/fix_packages/2026-11-15_C
T=$RUN/manuscript/prereg/2026-11-11_c_attr_dev/paper_text/transfer
C2=$T/c_attr_c2_transfer.py
D=$RUN/.session_backup/2026-10-13/decisions
LOG=$D/LOG.md
```

General stop rule for every step: if any assert fires, any line prints DIFF/DIFFERS/NOT WRITTEN, or any sha differs
from this list, stop. Do not edit a target, a pin or a script; the change goes to a diff read. Before each step:
`git -C $P status --short` must show only the 12 paths listed in the header, `git -C $P diff --cached --name-only`
must be empty, and HEAD must be the previous step's commit.

### Step 0 (before 05:00Z on 11-16, read-only)
- `sha256sum` of every file in section 1. Each must be unchanged.
- `git -C $P rev-parse --short HEAD` must print 55315ca. No commit may touch 00-11, V2_PROGRESS_C.md or the manifest
  before the v2 commit (CC-408 Ruling 6 (iii)). Tell every agent that writes to the paper repo (conference version,
  build) to hold until step 6 is committed.
- Freeze-line mention count must be 0. The command spells the suffix in pieces so that the literal is not written:
  `python3 -I -c "import sys; print(sum(('-c-'+'k7:') in l for l in open(sys.argv[1], encoding='utf-8')))" $LOG` → 0
- Check the clock: compare `date -u` with an outside time source. A WSL clock that runs fast would stamp a line
  "at 05:00Z" before real 05:00Z.

### Step 1: freeze line (coordinator, at or after 2026-11-16T05:00:00Z)
Build the line from the docstring template so that nothing is retyped. `ID` is the next free OPS id of 11-16, only
`[0-9a-z]`, for example 1116a. Check first that the id is unused.
```
U=$(date -u +%Y-%m-%dT%H:%M:%SZ); ID=1116a
[[ "$U" > "2026-11-16T04:59:59Z" ]] || { echo "before the freeze: stop"; exit 1; }
python3 -I -B - "$C2" "$U" "$ID" >> "$LOG" <<'EOF'
import hashlib, importlib.util, sys
assert hashlib.sha256(open(sys.argv[1], 'rb').read()).hexdigest() == '030c369d97f8668c7f82c8a05a046811e9d95da77272a63055f85f511e9da56c', 'c2 script changed: stop'
assert __import__('re').fullmatch(r'[0-9a-z]+', sys.argv[3]), 'id form'
s = importlib.util.spec_from_file_location('c2', sys.argv[1]); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
print(m.k7_template().replace('<utc>', sys.argv[2]).replace('<id>', sys.argv[3]))
EOF
```
- Expected: the mention count of step 0 is now 1, the line is the last line of the LOG, and it starts
  `<U> OPS-<ID>` with no " | ".
- Stop if: the count is not 1, or the line was wrapped, edited or written in the " | " form. Do not append a second
  line, because two lines block C2 for good. Go to a judge.
- From now on, never: no later LOG line, CC ruling or judge line may contain the freeze-line id with its colon. Name
  it "the freeze line" or by OPS id without the suffix. The freeze line is the single sanctioned exception to the
  rule against that literal in the LOG (a coordinator decision). A re-run of C2 after a failed read needs the count
  to still be 1.

### Step 2: shell C2 (directly after step 1, so the stamp is not in the future and not stale)
```
python3 -I -B $C2
```
- Expected output: `paper HEAD 55315ca`, then the sha256[:16] values
  - 06 68f77eb9a59e8d07
  - 05 0137bb6bfe2245d7
  - 07 c91bcf318ff086c7
  - 03 45888a88eddaad7f
  - the manifest (no fixed value: it depends on the stamp and the id)
- The output ends with `applied: C2-a (with the full B2 sentence), C2-b, C2-c, C1-b, manifest rows for the K7 line
  and for 40`.
- Manifest checks:
  - `head -n -2 $P/paper_v1_analysis/number_manifest_C.tsv | sha256sum` → 83414dc3... (the HEAD manifest).
  - `tail -n 1 ... | tr -d '\n' | sha256sum` → 6b0d2217... (row 40).
  - The freeze row's hash cell equals the first 12 hex digits of `sha256` of the LOG line, without its line break.
- Save the diff, scoped to the five paths. A bare `git diff` takes in the tex diffs.
```
git -C $P diff -- paper_v1_analysis/06_results.md paper_v1_analysis/05_preregistration_and_analysis.md \
  paper_v1_analysis/07_disclosures.md paper_v1_analysis/03_method.md paper_v1_analysis/number_manifest_C.tsv \
  > $T/C_C2_TRANSFER.diff
```
  Expected: 5 `diff --git` sections, about 13.2 kB (13,231 bytes in the rehearsal with a 6-character id; the size
  moves with the id length).
- Stop if: the script refuses. Nothing is written in that case. Do not retry with an edited line; go to a judge.

### Step 3: one-judge full read with byte match, then commit
- The judge reads C_C2_TRANSFER.diff and the five files. The byte match is the four fixed shas above plus the three
  manifest rules.
- NGRAM/caption scan PASS on the five files; no host, IP or port; no AI lines.
- Commit:
```
git -C $P add -- paper_v1_analysis/06_results.md paper_v1_analysis/05_preregistration_and_analysis.md \
  paper_v1_analysis/07_disclosures.md paper_v1_analysis/03_method.md paper_v1_analysis/number_manifest_C.tsv
git -C $P diff --cached --name-only    # exactly these 5 lines
```
- Check the staged blob shas (`git -C $P show :paper_v1_analysis/<f> | sha256sum`) against the disk values. Commit
  without attribution lines. Push as for 6a5d36a. Write the OPS line, which names the freeze line by OPS id without
  the suffix-colon literal.
- Stop if: the read is not GO or a staged blob differs. Then `git -C $P reset -q -- <the 5 paths>` and
  `git -C $P checkout -- <the 5 paths>` (back to 55315ca). Write no second freeze line and do not edit the script;
  go to a judge. C2 may be re-run only while the freeze-line mention count is still 1.
- Run-repo record: $T/C_C2_TRANSFER.diff (and c_attr_c2_transfer.py, untracked today) go to a separate run-repo
  commit if the coordinator commits them. They are not part of the paper repo.

### Step 4: package v2 under CC-408
```
sha256sum $D/CC-408.txt                   # ae06c9f57edfb51fa561d190dd75562dee72dba3f7006bcf1e81d358879de3b5
python3 -I -B $FIX/apply_c_v2_cc408.py    # check mode first (it still builds from 9b8e6ae; rc 0 expected)
python3 -I -B $FIX/apply_c_v2_cc408.py --write --ruling CC-408
```
- Expected:
  - `mode: WRITE on the working tree`
  - 10 EQUAL lines:
    - 00 a4725e99
    - 01 ffc90b60
    - 03 5db109ab
    - 04 58529b1d
    - 05 ea9094d3
    - 06 01d41de0
    - 08 69706e5f
    - 09 c52b962c
    - 11 5a71a8a0
    - V2_PROGRESS_C eee308fa
  - the manifest byte-rule line (bae57439)
  - `WRITTEN: 11 files under CC-408; paper HEAD <C2 commit>`
- Byte-unchanged after the write (W3): 02 8dbc299b (the task's "file 02 must become 8dbc299b": it stays at that
  value), 07 c91bcf31, 10 83d466df, STUDY_BRIEF_C 61f54eb9, paperC.bib a415c4da.
- Manifest checks:
  - Only lines 71 and 73 differ from the C2 commit (`git -C $P diff -U0 -- paper_v1_analysis/number_manifest_C.tsv`).
  - The last two rows are byte-unchanged.
- Stop if: any DIFFERS or `NOT WRITTEN`, or any of the unchanged files moved.
- Commit, 11 paths:
```
git -C $P add -- paper_v1_analysis/00_abstract.md paper_v1_analysis/01_introduction.md paper_v1_analysis/03_method.md \
  paper_v1_analysis/04_data_and_splits.md paper_v1_analysis/05_preregistration_and_analysis.md \
  paper_v1_analysis/06_results.md paper_v1_analysis/08_english_comparison.md paper_v1_analysis/09_limitations.md \
  paper_v1_analysis/11_supplement_registered_rows.md paper_v1_analysis/V2_PROGRESS_C.md \
  paper_v1_analysis/number_manifest_C.tsv
```
- Before the commit: NGRAM/caption scan PASS (the Vietnamese template is new text); the message names CC-408
  CONDITIONAL GO 88 and the CC sha; one OPS line.

### Step 5: package v4 under CC-413, then Annex B, one commit
```
sha256sum $D/CC-413.txt     # b9c9ec64c7120b8f10622559ce43caae5078349a2e7a796e02fba26c508bc2be
python3 -I -B $FIX/apply_c_v4_search.py     # check: "package v2 is committed (file 11 at the CC-408 target)"
python3 -I -B $FIX/apply_c_v4_search.py --write --ruling CC-413
```
- Expected:
  - 15 blocks; content checks passed
  - OK lines:
    - docs/TABLE1B_W5_EVIDENCE.md 03c79960
    - 02 4288f1fb
    - 11 fc7608a3
    - paperC.bib 550b88d1
    - paperC_bib_audit.tsv 55ece507
  - `ALL RESULTS EQUAL TARGETS`, then `WRITTEN: 5 files ...`
- Do NOT commit yet: Annex B reads the working tree at these v4 values.
- Extract Annex B outside the paper repo (path of the coordinator's choice; the scratchpad or $FIX), then check, then
  write:
```
A=<outside the paper repo>/annex_b.py
python3 -I -c "import hashlib,sys; b=open(sys.argv[1],'rb').read(); a=b.split(b'----- BEGIN ANNEX B (annex_b.py) -----\n')[1].split(b'----- END ANNEX B -----')[0]; assert hashlib.sha256(a).hexdigest()=='3fb2a675a822a1742c70c283426ca2a89b25180abe3267d118611b8359fc0b00'; open(sys.argv[2],'wb').write(a)" $D/CC-413.txt $A
python3 -I -B $A            # DIR defaults to the paper repo; 3 OK lines
python3 -I -B $A --write    # WRITTEN (not staged)
```
- Expected after Annex B: 02 b9f0c1f8, docs/TABLE1B_W5_EVIDENCE.md ed7608d0, 11 c4a24cd4; bib 550b88d1 and audit
  55ece507 unchanged.
- Stop if: any DIFF.
- Commit, 5 paths. This is `paper_v1_analysis/paperC.bib`, NOT `paper_v1_analysis/tex/paperC.bib`, which is dirty:
```
git -C $P add -- paper_v1_analysis/02_related_work.md docs/TABLE1B_W5_EVIDENCE.md paper_v1_analysis/paperC.bib \
  paper_v1_analysis/paperC_bib_audit.tsv paper_v1_analysis/11_supplement_registered_rows.md
```

### Step 6: package v5 under CC-423 (CONDITIONAL GO 88, CC sha 734009b0...; SKIP = ("C-A13",))
Ruling file: `sha256sum $D/CC-423.txt` → 734009b0a5a29bd06b7b08d06cd41c84254cb68bf01c3ab1c44f1475b4d46820.
Combination (CC-423 l.16-17): SKIP = ("C-A13",), MAN_OPS = ("C-M02", "C-M03"). That means blocks C-A01 to C-A12,
then C-M02 and C-M03. tex/readme.txt is not created.

6.1 The one-line change (the coordinator makes it; this agent did not edit the script). In
    $FIX/apply_c_v5_audit.py, now 24615559c0f3724d48a355b5bcedfc2646e8d48374d18a641382c6df91de0c45:
    - line 65 before:
      `SKIP = ()  # () or ("C-A13",): the readme may be left for the packaging step; no other target depends on it`
    - line 65 after:
      `SKIP = ("C-A13",)  # () or ("C-A13",): the readme may be left for the packaging step; no other target depends on it`

    Only `()` after `SKIP = ` becomes `("C-A13",)`. The two spaces and the comment stay byte-identical. No other line
    changes, and the file keeps its final line break.

    Expected sha256 after the change: f80bb6721a26cb74d05f7a45f851a208141e507807c8d592ad4199edadd91221 (CC-423 l.100).
    A scratch copy with exactly this change gave that value. Dropping the comment gives 53630b88..., which is wrong.

    A one-command form that refuses unless the result is f80bb672:
```
python3 -I -c "import sys,hashlib; p=sys.argv[1]; s=open(p,encoding='utf-8').read().split('\n'); assert hashlib.sha256('\n'.join(s).encode()).hexdigest().startswith('24615559') and s[64].startswith('SKIP = ()  #'); s[64]=s[64].replace('SKIP = ()','SKIP = (\"C-A13\",)',1); t='\n'.join(s).encode(); assert hashlib.sha256(t).hexdigest()=='f80bb6721a26cb74d05f7a45f851a208141e507807c8d592ad4199edadd91221'; open(p,'wb').write(t)" $FIX/apply_c_v5_audit.py
sha256sum $FIX/apply_c_v5_audit.py    # f80bb672...
V5=$FIX/apply_c_v5_audit.py
```
    The writer may not change anything else (W2). When the six file targets and the manifest target are met, no
    second read is needed (W2).

6.2 Run the check, then `--write`, then `--write-manifest`, back to back. Nothing is staged in between, and step 1 is
    not committed before step 2.
```
python3 -I -B $V5                                   # "the CC-413 commit is in place"; 12 blocks; 6 OK + manifest OK
python3 -I -B $V5 --write --ruling CC-423           # WRITTEN (step 1): 6 files
python3 -I -B $V5 --write-manifest --ruling CC-423  # WRITTEN (step 2): the manifest
```
- Expected results:
  - 02 397ce797
  - 03 3a36a06f
  - 04 0334d0aa
  - paperC.bib 21de95ea
  - paperC_bib_audit.tsv 8730a73e
  - scripts/paperC/c_pass2_check.py 254b4c2e
  - manifest without the freeze row fa91f428
  - C-M03 counts (271, 258, 29, 20)
  - tex/readme.txt NOT created
- Stop if:
  - the check mode does not print "the CC-413 commit is in place". The write gate needs, at HEAD:
    - all seven PRE files at the CC-408 / CC-413 values;
    - the manifest head at bae57439;
    - the two freeze rows as the last two rows.
  - any line prints DIFF.
  - step 2 refuses. Then step 1 is in the tree; do not commit it alone, because after a step-1 commit step 2 can
    never run.
  - a readme appears.
- Refusal and re-read rule (CC-423 item 11). If an earlier step ended at different bytes, the gate refuses. Then
  re-read, before any new pin:
  - the PRE value of the file concerned;
  - the C-A04/C-A05 anchors if the bibliography or its audit table differs (they sit on the last v4 entry and the
    last audit row, Zong2025VLICLBench);
  - the readme list if file 11 differs;
  - M03_COUNTS and MAN_TARGETS if any section file or the manifest head differs;
  - the counts 581 / 40 / 36.

  Each of these is a new read, not a new pin by the writer.
- Manifest checks (W3):
  - Its last-but-six and last-but-five rows (the freeze row and row 40) equal HEAD.
  - The LOG line of the commit records the full-file sha of the manifest and that fact.
- Commit (W3): one gatekeeper commit after both steps, staged by path. That is the six files plus the manifest, 7
  paths. The tex/ build files and docs/CC309_PARAGRAPH_DRAFT.md are not staged:
```
git -C $P add -- paper_v1_analysis/02_related_work.md paper_v1_analysis/03_method.md paper_v1_analysis/04_data_and_splits.md \
  paper_v1_analysis/paperC.bib paper_v1_analysis/paperC_bib_audit.tsv scripts/paperC/c_pass2_check.py \
  paper_v1_analysis/number_manifest_C.tsv
```
- The readme (Annex A of CC-423, a0dda92e) waits for packaging.

### Step 7: tex rebuild on a rented host
- Build from the paper-repo HEAD after step 6, as in the J2 precedent (OPS-1115ah: git archive of paper_v1_analysis,
  CC-410 ruling 2).
- The outputs (tex/*.tex, *.bbl, PDFs) are NOT committed and NOT staged.
- Read from the build log:
  - CC-408 N4: fonts for the Vietnamese template cells; {i}/{caption} braces survive pandoc.
  - CC-423 N5: the Table 1 box in italic code font.
- No host details in files.

### Never stage, in any commit
- paper_v1_analysis/tex/ (all 11 modified files, including tex/paperC.bib) and docs/CC309_PARAGRAPH_DRAFT.md.
- Never use `git add -A`, `git add .`, `git add paper_v1_analysis/`, `git commit -a` or a bare `git diff` for a record.

## 6. Overlap of targets (v2, v4, v5): no conflict

Each script's PRE equals the previous step's target. This was checked in memory by the check modes and on the
scratch clone with real commits.

| file | 55315ca | C2 | v2 (CC-408) | v4 | Annex B | v5 (CC-423) |
|---|---|---|---|---|---|---|
| 02_related_work.md | 8dbc299b | — | — (checked) | 4288f1fb | b9f0c1f8 | 397ce797 |
| 03_method.md | 2da4f2e5 | 45888a88 | 5db109ab | — | — | 3a36a06f |
| 04_data_and_splits.md | f7d1d0e7 | — | 58529b1d | — | — | 0334d0aa |
| 05_preregistration_and_analysis.md | 8e635ee2 | 0137bb6b | ea9094d3 | — | — | — |
| 06_results.md | 5443fe5e | 68f77eb9 | 01d41de0 | — | — | — |
| 07_disclosures.md | 72adbcb0 | c91bcf31 | — (checked) | — | — | — |
| 11_supplement_registered_rows.md | 025d744a | — | 5a71a8a0 | fc7608a3 | c4a24cd4 | — (read) |
| 00, 01, 08, 09, V2_PROGRESS_C | HEAD | — | targets above | — | — | — |
| paperC.bib | a415c4da | — | — (checked) | 550b88d1 | — | 21de95ea |
| paperC_bib_audit.tsv | a1af3339 | — | — | 55ece507 | — | 8730a73e |
| docs/TABLE1B_W5_EVIDENCE.md | 11a291b3 | — | — | 03c79960 | ed7608d0 | — |
| scripts/paperC/c_pass2_check.py | a257bd14 | — | — | — | — | 254b4c2e |
| number_manifest_C.tsv | 83414dc3 | +2 rows (stamp) | lines 71, 73 | — | — | +5 rows, used_in; fa91f428 without the freeze row |

v2's check mode builds from 9b8e6ae. Between 9b8e6ae and 55315ca only 02_related_work.md and
docs/TABLE1B_W5_EVIDENCE.md changed. CC-411 Ruling 5 sanctions that commit and sets the v2 check of 02 at 8dbc299b.
The write-mode path was rehearsed with the 55315ca 02 and passes: no table label 10-18, caption order holds, 02 not
in the output.

## 7. Risks found

1. **v5 l.260 stops step 2 when SKIP = ().** BLOCKING with the script as it is on disk (24615559). It is closed only
   by the f80bb672 variant ruled in CC-423 W2, and that variant does not exist yet. Make it byte-exact (step 6.1)
   and check its sha before use.
2. **Freeze-line form.** No " | " separators, which differs from every other LOG line. The id is `[0-9a-z]+` with
   no hyphen. One unwrapped line, no trailing space. The stamp comes from `date -u` and must not be earlier than
   05:00:00Z. Every wrong form was shown to be refused; a refusal is fail-closed, but it costs the morning.
3. **Uniqueness in the LOG, permanently.** Two lines that contain the id suffix with its colon block C2 for good:
   it can never find exactly one, and the LOG is append-only. That includes a re-run after a failed step-3 read.
   No OPS, CC or judge line may ever quote the freeze line. Today the count is 0.
4. **Clock.** A fast WSL clock could stamp the line before real 05:00Z. That would break the registered freeze time
   without any script noticing. Check against an outside time source; a margin of a minute or two is cheap.
5. **Diff scope.** A bare `git diff` for C_C2_TRANSFER.diff takes in the eleven dirty tex files. Scope it to the
   five paths.
6. **Two paperC.bib files.** paper_v1_analysis/tex/paperC.bib is dirty. Only paper_v1_analysis/paperC.bib belongs
   to steps 5 and 6.
7. **v2's write gate.** It uses the pathspec `paper_v1_analysis/*.md`, and git's `*` crosses `/`. Any new or
   changed .md anywhere under paper_v1_analysis/ (tex/, rev_analysis_2026-10-31/) makes v2 refuse. This is
   fail-closed, but keep the tree clean of .md drafts.
8. **Other writers.** Any commit to 00-11, V2 or the manifest between C2 and v2 voids CC-408 (Ruling 6 (iii)).
   Commits from the conference-version or build agents must wait until step 6 is committed.
9. **Commit timing.**
   - v4 must not be committed before Annex B runs: Annex B checks the working tree at the v4 values.
   - v5 step 1 must not be committed before step 2.
   - Each is one commit.
10. **v5 C-M02 reads the LOG.** The LOG lines OPS-1112j-c-attr-1b-g0 and OPS-1112bb-c-score-selftest must each
    stay the only line that begins with that id. Today each has exactly 1 hit.
11. **Manifest after C2 has no fixed sha.** Check it by rule: the head equals 83414dc3, row 40 is 6b0d2217, and the
    freeze-row hash cell equals sha256(line)[:12]. After v5 the target is fa91f428 without the freeze row.
12. **Annex B and v5 defaults.**
    - annex_b.py writes to the real paper repo when no DIR is given. Keep the file itself outside the paper repo so
      that it is never staged.
    - tex/readme.txt is NOT written in this chain (CC-423); it goes at packaging with Annex A a0dda92e.
13. **/mnt/d I/O.** WSL 9p I/O errors under heavy concurrent I/O have happened before. Avoid parallel heavy jobs
    while the chain runs, and re-hash after each write.
14. **c2 has no check mode.** Its first real run is the write run of step 2. The rehearsal covers its logic through
    its own functions but not its main(). Read its printed sha lines against step 2 before anything else.

Scratch records, outside the repo, to be deleted at will: sim_chain.py; sim/ (clone, LOG copies, annex_b.py,
C_C2_TRANSFER.sim.diff); v5skip/apply_c_v5_audit.py (f80bb672). All are under
/tmp/claude-1000/-mnt-d-vsps-image-captioning/cbc155a0-619c-4f6d-b27a-ab9635fb7056/scratchpad/.
