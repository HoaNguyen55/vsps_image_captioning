# Q11 ledger ruling and G-B run document v1.2 (C-PVR-T1, Paper C, ACM TALLIP): DRAFT for the round-2 full 3-judge panel at irreversible 92 (CC-242)

- **Version v1.2.** It answers CC-242 (round 1 NEXT_ROUND, median 88; LOG l.1404) and supersedes v1.1 a262cc75 (LOG
  l.1400) and v1 302e4c96 (l.1392). Both stay unchanged as records. The CC-242 item -> section map is §13.
  - **B1/W1:** a 4th PORTFOLIO edit replaces the HEAD l.193 tail; cite l.191 (was l.188); 4 changed lines; staged-blob
    grep (§1.5).
  - **B2/W2:** this document enters the same gatekeeper commit as the PORTFOLIO patch and the two idcheck files, with
    an n-gram scan, before the pause line (§1.6). CC-242 governs any CC-240 N-text that v1.2 supersedes.
  - **B3/W3:** C8(c) is the pinned `write_new` probe exactly as the coordinator ran it (LOG l.1405, PASS). The 'exact
    drvfs path' claim is struck. A failure at window time means no G-B and PI Q1 (B′) (§3).
  - **C1 (Codex):** a defined end state when gates.py is alive with no curl child past the wall (§8.3).
  - **N1-N16:** all folded in (§13).
  - **Coordinator facts:**
    - C17 is met: MT4 run finished, l.1401; the v18.14 apply line is l.1403.
    - No other background agent is running.
    - A stale ignored `scripts/c_pvr/__pycache__` was removed by the coordinator (13:30 VN); C20 now requires it
      absent.
- **History, v1.1.** v1.1 superseded v1 `Q11_GB_RUN_DRAFT.md` 302e4c96 (LOG l.1392; v1 is kept unchanged as a record).
  The changes come from the drafter's errata and the coordinator's request:
  1. The PORTFOLIO patch is built with `-U1` and applied to the working tree with `-C1`, after `git apply --check` (§1.5).
  2. The HEAD in the pause line is a placeholder, filled at run time with the HEAD after the Q11 and idcheck commits
     (§2.3).
  3. The recovery branch is keyed on the ACCESS_LOG state (sealed file written, `gb_counts.json` missing or untrusted),
     whatever the rc: 48, 49 or 50 (§5).
  4. The pid route is `echo $$ > "$3/sh.pid"` plus `pgrep -P`. No `pgrep -f` or `pkill -f` (§2.1, §8.2).
  5. A LOG writer W-k is added: background agents of any paper, including workflows and their bash loops (§4.1).
  - (a) The main finding is stated up top (next bullet).
  - (b) The window waits until the MT4 novelty-iterate run has finished and logged (C17, W-c).
  - (c) The PI's answers PI-1103u (LOG l.1393) are folded in as decided facts (§10):
    - Q-PI-2 YES; Q-PI-T YES; Q-PI-ID as recommended; Q-PI-RR: run under the pinned 3bced05e;
    - **Q-PI-W NO: no WSL restart.** C7 becomes a /mnt/d health check right before the run (C8, C12), disclosed as a
      higher EIO risk (§8.1).
- **MAIN FINDING: the pinned gates.py (3bced05e) has no re-run path.**
  - Once the start marker and its `gate-b start` ACCESS_LOG row exist, `gb_refuse` refuses every later start
    (l.1039-1040), and ACCESS_LOG is append-only. Any failure after the marker therefore ends G-B for good.
  - A re-download then needs a **new gates.py version** with a ruled re-run path, its own full panel at 92 and its own
    mutant run (§7.1).
  - **Recommendation: run now under the pinned version** (Q-PI-RR). A new version is needed only if a failure
    happens, and building it costs the same then as now. Building it now would spend that cost on every path,
    including the expected path where G-B passes.
- **Status.** This is a draft. It is not a ruling and licenses nothing. Nothing was run, moved or committed while
  drafting.
  - HEAD is now `8511fe6` (a VSPS-J commit after PINS-B `ec9466bd`, LOG l.1388).
  - `git diff ec9466b HEAD -- scripts/c_pvr` is empty, so P2/P7 (LOG l.1389, run under ec9466b) hold for HEAD.
  - After the Q11 commit, the same diff must show only the two idcheck additions (N14).
- **Subject of the panel.**
  - (a) The Q11 ledger answer.
  - (b) The one G-B run: command, pause line, preconditions, LOG quiet rule, failure branches.
  - (c) Registration: this document is committed with the Q11 commit (§1.6, B2).
  - These carry CC-240 N1-N5 (CC-240 Ruling 4 and the CARRIED line), the idcheck item left open by LOG l.1388, and
    CC-242 B1-B3, C1 and N1-N16.
  - Where v1.2 replaces CC-240 N-text (N1's restart clause, N5(b)'s 'no unlink rows'), CC-242 governs (CC-242 Rulings 4,
    6 and 7; CC-240 Ruling 6 precedent).
- **Order (CC-240 l.12, binding).** PINS-B commit (done) -> P2 (done) -> P7 (done) -> **Q11 ledger ruling (this
  panel, 92)** -> tenancy window P8 -> G-B, one run.
- **Reading rule for this document.** Every check that `gates.py` makes **before** the start marker (gates.py l.1108-1130)
  can only refuse, so the one run survives it. From the marker on (l.1129), **any** non-zero exit ends G-B under the
  pinned sha (§7.1). The words in this document go mostly to the second group.
- **Pause tag.** The pause tag is written once, in §2.2, and is called "the §2 tag" everywhere else. No LOG line
  other than the pause line may ever contain it (§2.3).

---

## 1. The Q11 ledger question and the proposed answer

### 1.1 Source (quoted)
- **Prereg §14, row Q11** (`PREREG_DRAFT_v1_2.md` l.805, committed 8282874):
  > "Correct L2-P1 to 36,707 images (41,164 − 4,457; RULE l.19) and release NoCaps val to C as its tier-2 rehearsal, by
  > a ledger ruling >= 92, before any C GPU work?" Recommended: YES. Default: "HOLD: C stops after PINS; no G-B, no C
  > GPU work".
- **Prereg §9.1 step 6** (l.638-639): "**Q11 answered YES** (PI line + ledger ruling >= 92). Under the default HOLD: C
  stops after step 5; G-B never runs (no test-gold exposure for a branch that cannot reach tier 2), and no C GPU work
  runs on any host."
- **Prereg §9.3 preconditions** (l.654-655): "... PINS-A and PINS-B committed; Q11 = YES; `gates.py` sha equals PINS-B."
- **PI line, PI-1102a** (LOG l.1140): "Q11 YES (L2-P1 -> 36,707 and NoCaps val to C, still via a ledger ruling >= 92
  before any C GPU work / G-B)".
- **Origin, CC-214r3** l.212-213: "Q11 (NoCaps val against L2-P1). Recommended: correct the L2-P1 row to 36,707 unused
  images and release NoCaps val to C as its tier-2 rehearsal set, ruled before the C tier-2 prereg. Default: HOLD."
  Also Ruling 6 (l.125-126): "This is the main falsifier on C's path."
- **"Ledger"** = the test-set ledger, PORTFOLIO §2.3 ("each unspent set has exactly one owner";
  `manuscript/directions/PORTFOLIO_3Y_2026-10-29.md`).
  - CC-214r3 W7 (l.154-156) fixes how a ledger entry takes effect: it is "date[d] to the adopting ruling or PI line,
    plus the gatekeeper commit of the PORTFOLIO rows. Those rows take effect only through that commit."
- **Order sources.**
  - CC-236 l.180 and CC-236r2/r3 l.141: "Q11 ledger ruling at 92".
  - CC-239 l.15 and l.35: "PINS-B -> Q11 -> G-B, and Q11 is separate (PI-1102a, CC-232 (f))".
  - CC-232 (f) (l.146): "Nothing irreversible (PINS-B registration, Q11, G-B, GPU) proceeds on the default alone".
- **CC-242 Ruling 1** (round 1, on the merits; nobody contests it): "Q11 on the merits: YES. L2-P1 = 36,707 by the set
  rule; the operational rule is gates.py l.196-203. ... nocaps val becomes C's tier-2 dev-confirm rehearsal set, and C
  decodes none of it before its tier-2 prereg."
- **Name clash (not this question).** PORTFOLIO §5 also has a row "Q11" (l.297: "ViTextCaps stays C-only"). This
  panel does not rule on it. Here "Q11" always means the prereg §14 / CC-214r3 question.

### 1.2 Why the correction is needed
- NoCaps val (4,500 images) is a subset of OIV7 val. It is spent dev: it is in PORTFOLIO §2.3 "Dev-only (spent): ...
  nocaps val", and C-EN read it (`cen_nocaps_val.tsv` 6add90eb).
- The L2-P1 row "OIV7 val − 456 XM ids (41,164)" therefore contains 4,457 spent images (4,500 minus the 43 that are
  already among the 456 XM ids; RULE l.19).
- The correction narrows L2-P1 to the unspent 36,707. The 4,457 NoCaps val images get a role inside C: the tier-2
  dev-confirm rehearsal set for P_obj^VI (prereg §0 l.151-152, §4.4 l.370).

### 1.3 Proposed answer
**YES**, in four parts.
1. **L2-P1 row.** L2-P1 owns OIV7 val − 456 XM3600 ids − the 4,457 NoCaps val ids not in the 456 = **36,707** images.
   - It is defined as a set rule on pinned files: `oiv7_val_ids.txt` 4b7a1813 − `xm3600_in_oiv7_val_ids.txt` 54966ca7
     − ids(`cen_nocaps_val.tsv` 6add90eb).
   - The operational rule is gates.py l.196-203 (`l2p1 = set(val7) - x456`; `l2p1_q11 = l2p1 - (val - x456)`; both
     sizes asserted, 41,164 / 36,707) (N1).
   - No new id file is made now. L2-P1's own prereg writes and pins its list (YAGNI here).
2. **NoCaps val.** It stays spent dev. Its role is **C tier-2 dev-confirm rehearsal (P_obj^VI)**.
   - **C decodes none of it before its tier-2 prereg** (CC-242 Ruling 1).
   - Tier 2 needs its own prereg (prereg §0).
3. **Effective date.** The ledger change takes effect at the gatekeeper commit of the PORTFOLIO rows in §1.5
   (CC-214r3 W7), made after the round-2 GO (`CC-242rN`, the id filled at commit). The commit message and LOG line cite
   `CC-242rN` and PI-1102a.
4. **Licences.**
   - Q11 = YES closes precondition P5 (PINS_B_DRAFT_v1_1 §4) for G-B.
   - It also lifts the HOLD on "C GPU work". Every other C GPU precondition still binds: the Q-custody host amendment
     (prereg §8.3), the cap pin, M1 or a named host.
   - Q11 = YES licenses no rental and no decode by itself.

### 1.4 Evidence that the answer changes nothing already computed
- G-A computes and asserts both bases:
  - `ga_counts.json` (f7036396, committed): `x_l2p1_41164` 0, `x_l2p1_36707` 0. NoCaps test overlaps neither base.
  - Amendment v1.3 l.322: "Both counts are asserted".
  - Erratum CC-227 l.33: "gate-a step0 reported l2p1 41,164, l2p1_q11 36,707".
- `ga_remaining_ids.txt` 3feccabc does not depend on Q11. Amendment v1.3 l.349: "Q11 changes only which L2-P1 base
  is printed, and both are printed". So the G-B filter key, P2 and P7 do not change.
- **Other preregs that cite 41,164** (`git grep -n "41,164" manuscript/`):
  - RULE l.19/21/101, MT4 `AMENDMENT_W25K1.md` l.72-87 and `DEV_RULE.md` l.124 use it as the **W25 comparison
    pool**. B `AMENDMENT_R5_DRAFT_v1_2.md` l.122/192/288 and VSPS-J `AMENDMENT_1_DRAFT_v1_2.md` l.301 use it as an
    exclusion set.
  - The 36,707 is a subset and the 4,457 stay excluded as NoCaps val, so no comparison or exclusion count changes.
  - B l.288 already records "PI-1102a Q11 ..., ledger ruling ≥ 92 pending". VSPS-J l.301 already treats NoCaps val as
    C's.
  - No edit to those files is proposed.

### 1.5 PORTFOLIO edit (exact text) and how to stage it
- **§2.3 ledger row** (HEAD l.175):
  - old: `| OIV7 val − 456 XM ids (41,164) | human-verified labels | features only (W25 dedup) | L2-P1 |`
  - new: `| OIV7 val − 456 XM ids − 4,457 NoCaps val ids (36,707) | human-verified labels | features only (W25 dedup); the 4,457 NoCaps val images are spent dev and leave L2-P1 (Q11: PI-1102a, CC-242rN; effective at this commit) | L2-P1 |`
- **§2.3 "Dev-only (spent)" line** (HEAD l.191; v1/v1.1 wrongly cited l.188): `nocaps val` -> `nocaps val (C tier-2
  dev-confirm rehearsal for P_obj^VI; Q11: PI-1102a, CC-242rN)`.
- **§L2 owner sentence** (HEAD l.67): `OIV7 val minus the 456 XM3600 ids (41,164 images)` -> `OIV7 val minus the 456
  XM3600 ids and the 4,457 spent NoCaps val ids (36,707 images; Q11, CC-242rN)`.
- **§2.3 C-roles paragraph, tail of HEAD l.193 (B1; 4th edit).** It uses J2's wording from CC-242 B1. `CC-242rN` is
  filled at commit.
  - old (the tail only; everything before "Note:" is unchanged): `Note: nocaps val (4,457 of its 4,500 images) sits
    inside L2-P1's 41,164 although it is spent (above); ledger ruling pending (C_DIRECTION_v4 §14 Q11; precondition of
    the C tier-2 prereg); until then C holds nocaps val and decodes none of it.`
  - new: `Note: Q11 ruled (PI-1102a, CC-242rN GO; effective at this commit): the 4,457 nocaps val images leave L2-P1
    (= 36,707); nocaps val is C's tier-2 dev-confirm rehearsal set; C decodes none of it before its tier-2 prereg.`
  - Without this edit the commit would leave a ledger line that contradicts the l.175 row (CC-242 What was checked 2).
- **Left stale on purpose (N15), named in the commit message** ("PORTFOLIO l.68 and l.291 still state 41,164-based
  estimates; L2-P1's own prereg restates them"). The L2-P1 cost line l.68 (it becomes about 92 GPU-h
  short / 199 detailed: 36,707 × 6 × 1.5 s and × 3.25 s) and §5 Q5 l.291. These are estimates, not ledger rows;
  L2-P1's own prereg restates them.
- **Staging.** The working PORTFOLIO already has 3 unrelated uncommitted hunks (Objects365 -> Paper B, PI-1101p Q4;
  `git diff --stat` 3+/3−). They must not enter this commit, and `git add -p` is not available. Steps:
  1. `git show HEAD:manuscript/directions/PORTFOLIO_3Y_2026-10-29.md > $S/P_head.md`; copy it to `$S/P_q11.md`; apply
     the **four** edits above to `$S/P_q11.md` only.
  2. `git diff --no-index -U1 $S/P_head.md $S/P_q11.md > $S/q11.patch`; fix the path headers to
     `a/manuscript/directions/...` and `b/...`.
     - Why `-U1`: the L2-P1 row (HEAD l.175) is two lines above the Objects365 row (l.177) that the uncommitted hunk
       changes. A default 3-line context would carry the HEAD text of l.177, and the working-tree apply would reject it.
  3. Checks first, then apply:
     - `git apply --cached --check $S/q11.patch` (the index equals HEAD);
     - `git apply --check -C1 $S/q11.patch` (the working tree);
     - only if both pass: `git apply --cached $S/q11.patch` (index only), then `git apply -C1 $S/q11.patch` (working
       tree, so both edits coexist).
     - If either check fails, nothing is applied and the gatekeeper stops.
  4. Checks, all of them:
     - `git diff --cached --numstat -- manuscript/directions/PORTFOLIO_3Y_2026-10-29.md` = `4	4` (4 changed lines:
       l.67, l.175, l.191, l.193);
     - `git diff --cached` holds no Objects365 text;
     - **staged-blob check (B1):** `git show :manuscript/directions/PORTFOLIO_3Y_2026-10-29.md | grep -c 'ledger ruling pending'`
       prints **0** (HEAD prints 1 at drafting);
     - `git show :manuscript/directions/PORTFOLIO_3Y_2026-10-29.md | grep -c '36,707'` ≥ 3.
  - `$S` is ext4 session scratch. The n-gram scan runs on the staged blob.

### 1.6 The one gatekeeper commit (B2/W2; CC-242 Coordinator order step 5)
- **Contents, staged together, nothing else:**
  1. the PORTFOLIO patch (§1.5, 4 changed lines, the staged-blob check = 0);
  2. `scripts/c_pvr/idcheck.py` 040e78ef and `scripts/c_pvr/idcheck_out.txt` 13d59e15 (CC-242 Ruling 2; PI-1103u
     Q-PI-ID);
  3. **this file, `Q11_GB_RUN_DRAFT_v1_2.md`, byte-equal to the sha that the round-2 GO names.** It registers, before
     any data, F1-F3 (§6), R-A/R-B with the four ACCESS_LOG states (§5), the open-count shape (§5.3), the stall, wall
     and end-state numbers (§8.2-§8.3), the checklist C1-C20 (§3), and the CC-240 N1-N5 pre-registrations.
- **Checks before the commit:**
  - re-hash all three paths;
  - the n-gram scan (`ngram_scan_cen.py` 92607635, 8/6-gram vs the four corpora, positive controls hit) on the staged
    PORTFOLIO blob, the two idcheck files and this file: PASS;
  - `sha256sum -c scripts/c_pvr/SHA256SUMS` = 16 OK. SUMS is not edited; the idcheck files get no SUMS line;
  - `git diff ec9466b --cached -- scripts/c_pvr` shows only the two idcheck additions (N14).
- **Commit message:** `CC-242rN` filled; "effective at this commit"; the N15 stale note. Only the generic tag form
  `OPS-<MMDD>c-gbpause` may appear (N4).
- **After:** push, then one LOG line "Q11 effective at this commit <sha>", written before the pause line. v1 and v1.1
  stay uncommitted records.
- **Then the archive move (N13):** `mkdir -p .session_backup/2026-11-02/c_gd/` first, then `mv` of
  `scripts/c_pvr/idcheck_out_rerun.txt` (13d59e15) there, re-hash, and one LOG line.

---

## 2. G-B command, pause tag and pause LOG line

### 2.1 Command (PINS_B_DRAFT_v1_1 §1.3 l.81, Q-B1; W9: no pipe, rc captured at once)
```
cd /mnt/d/vsps_image_captioning
S=$HOME/gbrun_<MMDD>
[ ! -e "$S" ] && [ ! -e "$S/gb_rc.txt" ] && mkdir -m 700 "$S" || { echo "LAUNCH GUARD: $S exists"; exit 1; }   # fresh, mode 700, ext4
setsid -f /bin/sh -c 'echo $$ >"$3/sh.pid"; /usr/bin/python3 -I -B scripts/c_pvr/gates.py gate-b --gates-sha "$1" --pause-tag "$2" >"$3/gb_stdout.txt" 2>"$3/gb_stderr.txt"; echo "rc=$? $(date -u +%FT%TZ)" >"$3/gb_rc.txt"' sh 3bced05e7f718377b34837cfb3f6d6539fb8aafc28bc5f8818e5d7be4ccdf897 '<the §2 tag>' "$S"
```
- **Launch guard (N11).** `$S` must not exist before the launch: a fresh mode-700 dir on ext4 with no `gb_rc.txt`. If
  the guard fires, nothing is launched and the coordinator stops. A stale `$S` means a former launch, which goes to
  the PI.
- **Detached (`setsid -f`).** gate-b must not run under a tool timeout or in the coordinator's process group. A Bash
  tool timeout (max 10 min) or the end of the session would signal it: rc 49, or SIGKILL residue (§2.5(d) of PINS-B).
  Either one consumes the run.
- **`/usr/bin/python3` by absolute path.** This is the pinned interpreter (LOG l.1388: `sys.executable` /usr/bin/python3
  -> python3.12, e50d468e), not `~/.venvs/c_pvr`. The (B) code is stdlib only.
- **The real `HOME`.** `SEALED` and the `gpu_backup.sh` path are built from `Path.home()` (gates.py l.56, l.1236).
- **cwd = repo root.** `ROOT` comes from `__file__` (l.53). The cwd only fixes where the relative command resolves.
- **Output.** stdout gets `gb_counts.json` (indent 1) on success and **nothing** on any post-marker exit (Q-B11).
  stderr gets only pre-marker FAULT text. `gb_rc.txt` gets the rc and the stamp. All three are on ext4 and hold no
  gold.
- **Pid route (no `pgrep -f`, no `pkill -f`).** `pgrep -f` would also match the coordinator's own wrapper command.
  - `SH=$(cat "$S/sh.pid")` is the pid of the detached `sh`. It is written first, by the `sh` itself (`$$`).
  - `GP=$(pgrep -P "$SH" -x python3)` is the gates.py pid: the only `python3` child of that `sh`.
  - `CP=$(pgrep -P "$GP" -x curl)` is the live curl pid, if any. gates.py runs at most one curl at a time (HEAD, then
    the body).
  - Each pid is re-read on every watch step, because the curl pid changes between HEAD and body.
- **Monitoring.** The coordinator watches only `gb_rc.txt`, `/proc/$GP` and `/proc/$CP/io` (§8.2). It writes no LOG
  line until `gb_rc.txt` exists.

### 2.2 The pause tag
- **The §2 tag = `OPS-<MMDD>c-gbpause`**, where `<MMDD>` is the `date -u` month-day of the pause line. It matches
  `OPS-[0-9A-Za-z][0-9A-Za-z-]*` (gates.py l.980).
- Before the pause line: `grep -c -- '<the §2 tag>' .session_backup/2026-10-13/decisions/LOG.md` must print **0**. At
  drafting, `grep -c gbpause` printed 0.

### 2.3 Pause LOG line (text; one line, appended with a single `>>`; the stamp is `$(date -u +%FT%TZ)` once, which already ends in `Z`)
```
$(date -u +%FT%TZ) <the §2 tag>: G-B pause window opens per CC-242rN GO <median> (Q11 ledger ruling, full panel, irreversible 92) and PI-1103u (Q-PI-2 YES; no WSL restart, /mnt/d health check C8 PASS at <utc>) and <PI-id of the C18 confirmations line>: from this line until gates.py gate-b exits, every LOG.md writer and every other paper's laptop job is paused (§4 list of Q11_GB_RUN_DRAFT_v1_2 <sha8>, committed <Q11 commit sha8>); HEAD <HEAD after the Q11 and idcheck commits, git rev-parse HEAD at run time>, gates.py 3bced05e7f718377b34837cfb3f6d6539fb8aafc28bc5f8818e5d7be4ccdf897; preconditions §3 all PASS (<scratch file> <sha8>); no other LOG line until the exit.
```
- **The predicate it must meet** (gates.py `pause_ok`, l.977-991):
  - the tag is a whole token in **exactly one** LOG line;
  - that line starts with a `date -u` stamp earlier than the gates.py import time `T0`;
  - it contains `G-B` and a word starting `pause`.
- **Order.** Write the line. Wait at least 2 s, so the stamp is strictly earlier than `T0`. Record the quiet-probe values
  (§4.2). Then launch §2.1.
- **Tag hygiene (binding).** No other LOG line, before or after, may contain the §2 tag as a token. Only the generic
  form `OPS-<MMDD>c-gbpause` (with the literal `<MMDD>`) may appear in a CC file, a LOG line or a commit message (N4).
  This covers:
  - this draft's own LOG line;
  - the Q11 ruling line that `judge-panel.js` writes (l.163; free subject text), so the chair must not quote the tag;
  - the gatekeeper lines;
  - the post-run lines, which use `OPS-<MMDD>c-gb-result` and `OPS-<MMDD>c-gb-resume`.
- **A second hit:**
  - before the marker, it is a FAULT with text, and the run survives;
  - after the marker, it is rc 40 and the run is consumed.

### 2.4 Pre-marker FAULT branch (N11)
- **The state.** `gb_rc.txt` shows rc 1 (a `fault()` SystemExit or any pre-marker exception) or rc 2 (argparse). The
  ACCESS_LOG holds **no** `gate-b` row, and `~/.vsps_sealed/c_pvr/gb_start` is absent. No byte was requested, and the
  run is **not** consumed.
- **Steps:**
  - the coordinator copies `gb_stderr.txt` (FAULT text only, no gold) and writes the `OPS-<MMDD>c-gb-result` line
    (pre-marker FAULT, rc, stderr sha and text), then the resume line;
  - the cause is fixed only if it is outside gates.py (e.g. a LOG line, a tenancy input, a typo in the command). Any
    change to gates.py is B′ (§7.1);
  - **a one-judge read** (reversible 90) checks the cause and the fix;
  - a new window then opens under the new tag `OPS-<MMDD>c-gbpause2`, with C1-C20 re-run. The first tag already sits on
    one LOG line, so it cannot be reused.

---

## 3. Precondition checklist (all PASS, checked in one coordinator pass right before the pause line)

Run them in this order. Save the outputs to `$S_pre/pre.txt` (an ext4 dir separate from the launch `$S`, which must
stay absent until launch) and record its sha in the pause line. A FAIL means no pause line is written and no run
happens. **C18 and C19 come first** (before C8), and C8 runs within 5 min before the pause line.

| # | precondition | how it is checked | PASS | note |
|---|---|---|---|---|
| C1 | HEAD gates.py = `--gates-sha` | `git show HEAD:scripts/c_pvr/gates.py \| sha256sum` and `sha256sum scripts/c_pvr/gates.py` | both = 3bced05e7f718377b34837cfb3f6d6539fb8aafc28bc5f8818e5d7be4ccdf897 | CC-240 N3. Also in code (`gb_integrity`, pre-marker) |
| C2 | `git status --porcelain scripts/c_pvr` is empty | that command | empty | **FAILS today**: `?? idcheck.py`, `?? idcheck_out.txt`, `?? idcheck_out_rerun.txt`. Disposition in §3.1 |
| C3 | toolchain = pin line l.1388 | `curl --version \| head -1`; `stat -c %F /usr/bin/curl`; `sha256sum /usr/bin/curl`; `/usr/bin/python3 -I -c 'import sys;print(sys.executable,sys.version.split()[0])'`; `sha256sum "$(readlink -f /usr/bin/python3)"` | `curl 8.5.0 (x86_64-pc-linux-gnu) libcurl/8.5.0 OpenSSL/3.0.13 ...` (full string as l.1388); regular file; 1ccbd3dae948374ba8eef1ebda26c64b783ede50b463196e53666e0880bdac60; `/usr/bin/python3 3.12.3`; e50d468e8b0adfb05733f5b87b3cff34829c4a8c1aea50c865aa8bdfe4bb150f | `unattended-upgrade-shutdown` is live on the laptop. Re-hash both right before the pause line and again after the exit. Also `systemctl list-timers 'apt-daily*' --all`: neither `apt-daily` nor `apt-daily-upgrade` may be due within the window plus 90 min, otherwise wait (agents cannot stop them without sudo; N6). At drafting (07:4xZ) all five matched; at v1.2 drafting the timers were due 18:57 VN (apt-daily) and 06:03 VN next day (apt-daily-upgrade) |
| C4 | SUMS 16 OK | `sha256sum -c scripts/c_pvr/SHA256SUMS; echo rc=$?` from the repo root | 16 `OK`, rc 0, 16 lines; file sha 0999c775 | in code too (pre-marker). At drafting: 16/16 |
| C5 | P2 and P7 done, and still valid for the current HEAD | `git diff --stat ec9466b HEAD -- scripts/c_pvr` lists only `idcheck.py` and `idcheck_out.txt` as additions after the Q11 commit (empty before it; empty at v1.2 drafting, HEAD 8511fe6) (N14); LOG l.1389; `.session_backup/2026-11-03/c_pinsb/p2p7/p2.txt` sha 2999f0ed, `p7.txt` sha ca936961 | both rc 0; P2 = CC-239 Ruling 4 values; P7 = 3feccabc | gate-b re-runs both in code before the marker (N11, W11) |
| C6 | Q11 GO at 92 and the Q11 commit made | **`CC-242rN` GO (≥ 92), not revoked** by any later CC line (N5): `grep -n 'CC-242' LOG.md`; `git log -1 --format=%H -- manuscript/directions/PORTFOLIO_3Y_2026-10-29.md` = the §1.6 commit, which also holds `Q11_GB_RUN_DRAFT_v1_2.md` with the GO'd sha; the "effective at this commit" LOG line exists | all three | prereg §9.3 "Q11 = YES"; B2 |
| C7 | **no WSL restart (PI-1103u, Q-PI-W NO)**; replaced by a /mnt/d health check right before the run | C8, run as the last step before the pause line (C8 within the 5 min before the pause line), and C12 | C8 and C12 pass | **Disclosed: higher EIO risk than CC-240 N1 asked for; CC-242 Ruling 6 states the overrule explicitly.** N1 wanted G-B "only right after a WSL restart". Without one, the 9p channel has been up since the last outage (LOG l.1295: the channel fails under heavy concurrent I/O and stays failed until a restart). An EIO after the marker is rc 48 or 50 and ends G-B (§5, §7). Mitigation: C8, C9 and the quiet window keep /mnt/d I/O near zero for the few minutes of the run |
| C8 | /mnt/d health, right before the run (within 5 min of the pause line) | (a) `mount \| grep ' /mnt/d '` = 9p (aname=drvfs); (b) `~/.local/state/vsps/d_watch.log`: no `FAIL` line after the last `RECOVERED` (or the file is absent: no failure since d_watch started, LOG l.1323), and `d_watch.sh` is live; **(c) the pinned `write_new` probe, exactly as run once by the coordinator on 2026-11-03 (LOG l.1405, OPS-1103c-q11-probe, PASS):** `timeout 20 /usr/bin/python3 -I -B` with `sys.path` = `scripts/c_pvr`; assert sha256 of `scripts/c_pvr/gates.py` = 3bced05e…; `gates.write_new(Path('.session_backup/q11_probe/p.json'), b'x\n', 0o444)` returns 73cb3858… (sha of `b'x\n'`); re-read = `b'x\n'`; unlink the 0444 file; assert no `.tmp` is left (dir empty); rmdir; assert no `__pycache__` created. drvfs reports mode 0o555 for the file (9p metadata off), which `write_new` ignores on /mnt/d (`check_mode` False, as at l.1186); (d) `timeout 120 sha256sum -c scripts/c_pvr/SHA256SUMS` (also C4) | all pass, each within its timeout | rc 48 and rc 50 come from /mnt/d EIO (LOG l.1295). (c) runs the same pinned function with the same mode on the same mount as l.1186, so chmod 0444 → link → dir fsync → unlink tmp → re-read are exercised there (B3); it does not prove the channel stays up during the run. **Any C8 failure: no pause line, no G-B under 3bced05e; the PI is asked (restart, or B′ by CC-242 PI Q1)** |
| C9 | no heavy /mnt/d I/O | `ps -eo pid,etime,args`: no rsync, no `gates_mutants.py`/`c_pvr_mutants.py`, no novelty-iterate/expert-review/judge-panel agent or its bash loop, no background agent of any paper (W-k), no pandoc/LaTeX build, no `git gc`; no `gpu_backup.sh` loop | none | CC-240 N1. gpu_backup is not started until the resume line (§4) |
| C10 | sealed dir ready, no G-B residue | `stat -c '%a %U' ~/.vsps_sealed/c_pvr` = `700 hoanguyen`; `ls ~/.vsps_sealed/c_pvr/gb_start ~/.vsps_sealed/c_pvr/gb_intermediate.json manuscript/prereg/2026-11-02_c_pvr_tier1/gb_counts.json /dev/shm/c_pvr_gb` all absent; `grep -c 'gate-b' ~/.vsps_sealed/c_pvr/ACCESS_LOG.tsv` = 0 | as stated | in code too (pre-marker). At drafting: 700, all absent, 0 gate-b rows, ACCESS_LOG 13 rows sha f6ef9ede |
| C11 | tenancy inputs | `grep -c /dev/shm ~/.config/vsps/gpu_backup.sh` = 0 and the file exists; scan `/proc/*/cmdline` for an argument ending `_job.sh` = none; `/dev/shm/c_pvr_gb.lock` absent or unlocked | as stated | §8.2 steps 1-4, in code. **During the window the coordinator types no command with an argument ending `_job.sh`, not even `grep ... c_pvr_job.sh`**: `foreign_jobs` counts any such argv (l.994-1006) and that would be rc 40 |
| C12 | LOG.md decodes as strict UTF-8 and ends with a newline | `/usr/bin/python3 -I -c 'import pathlib;pathlib.Path(".session_backup/2026-10-13/decisions/LOG.md").read_text(encoding="utf-8")'`; `tail -c1 LOG.md \| od -c` = `\n` | no error; `\n` | `pause_ok` reads the whole file strict UTF-8 4-5 times after the marker. A decode error there is rc 50. At drafting: decodes, 1,390 lines |
| C13 | §2 tag absent | §2.2 | 0 | |
| C14 | bucket objects unchanged | the l.1380 HEAD-only check repeated: `env -i PATH=/usr/bin:/bin /usr/bin/curl -q -sS -I --fail --proto =https <OI_LABEL_URL s=val\|test>` (headers to `$S`) | one `HTTP/2 200` each; exactly one Content-Length, 28392297 / 93606939; no Content-Encoding; `x-goog-hash` md5 = 8720e72fb87b89ac4bad277e076bd1ec / 8a711a152098b98d1d9e7687646325a1 | a bucket change after the marker is rc 42 and consumes the run. Checked before, it only stops the window |
| C15 | PI answers in force | PI-1103u (LOG l.1393): Q-PI-2 YES, Q-PI-T YES, Q-PI-ID, Q-PI-RR, Q-PI-W NO (§10) | present; the PI has closed Gemini and the other tool for the window | §10 |
| C16 | idle laptop | no other paper's laptop job running or queued (B, MT4, VSPS-J); no GPU job waits on a laptop step in the window | none | PINS-B §8.1 |
| C17 | MT4 novelty-iterate run (PI-1103s, LOG l.1385) finished and logged; no live W-k writer | completion line present (**met**: LOG l.1401, OPS-1103mt4-iterate2-done, 10:08:09Z; the v18.14 apply line l.1403 also logged); re-checked live right before C8: `ps -eo pid,etime,args` shows no agent, workflow or agent bash loop (`q.sh`, `sleep` loops other than `d_watch`) (N9) | both | PI-1103u: "MT4 novelty-iterate finished first" |
| C18 | PI confirmations on a PI LOG line before C8 (N6; CC-242 PI Q3) | a PI-<id> line, logged from the PI's chat answer, states: Gemini and the other tool (INC-1027a) are closed; the laptop is on mains power, sleep off, lid open; the Windows Update restart is deferred | present before C8; cited in the pause line | PI-1103u already gives Q-PI-T YES; this line confirms it live on the day. Without it the window does not open |
| C19 | usage headroom ≥ about 90 min (N12) | `~/.config/vsps/usage_check.sh` run twice, 10 min apart, before C8: for both the 5-hour and 7-day limits, remaining % ÷ (% used per minute between the two reads) ≥ 90 min (or no change), and the 5-hour reset is not due inside the window | both limits | The usage-guard routine writes **nothing** to LOG.md in the window; a low reading is acted on after the resume line |
| C20 | no stale bytecode or ignored file under `scripts/c_pvr` | `git status --porcelain --ignored scripts/c_pvr` is empty after the Q11 commit and the archive move (this also covers C2); `find scripts/c_pvr -name __pycache__ -o -name '*.pyc'` prints nothing | empty | the coordinator removed a stale ignored `scripts/c_pvr/__pycache__` at 13:30 VN on 2026-11-03 (from an earlier agent run). gate-b runs with `-B`, and the C8(c) probe asserts no `__pycache__` is created |

### 3.1 The three untracked idcheck files (C2)
- **What they are.** G-D artifacts, LOG l.1153 (OPS-1102c-gd, 2026-11-02T01:12:15Z):
  - "Copied byte-equal to scripts/c_pvr/: idcheck.py 040e78ef, idcheck_out.txt 13d59e15";
  - the rerun output `idcheck_out_rerun.txt` is "13d59e15 = BYTE-EQUAL to the pinned output";
  - "The three files stay uncommitted (CC-214r3 W8 carry)".
- **Re-hashed now.**
  - `idcheck.py` 040e78effe93fbb99a118ad2f8a78d2a2046ee3a9a8660984db3f159fd53ebc3 and both outputs
    13d59e152d604cd96dfe55b8998af5105efdf8c5d83703c67f311b04a8031baf.
  - The originals in `.session_backup/2026-11-01/c_direction_v3_idcheck/` have the same two shas.
- **Open carries that cover them.**
  - CC-214r3 W8 (l.157): "Commit idcheck.py and idcheck_out.txt (040e78ef / 13d59e15) into scripts/ with the tier-1
    prereg, and re-run them there."
  - CC-221r3 W2 (l.68): "8282874 staged only PREREG_DRAFT_v1_2.md ... a later gatekeeper licence closes W8."
  - CC-221r3 W7 (l.73): "the rerun output ... stays uncommitted unless a gatekeeper licence covers it."
  - Prereg §9.2 G-D row (l.648) names these exact paths.
- **Disposition, decided by the PI (PI-1103u, Q-PI-ID) and sound on the merits (CC-242 Ruling 2); the round-2 GO licenses the gatekeeper commit (§1.6).**
  1. The gatekeeper commits `scripts/c_pvr/idcheck.py` 040e78ef and `scripts/c_pvr/idcheck_out.txt` 13d59e15. Steps:
     re-hash = the two shas above; n-gram scan of the two blobs PASS; no SUMS line added; SUMS stays 16 lines. This
     closes CC-214r3 W8.
  2. The coordinator first runs `mkdir -p .session_backup/2026-11-02/c_gd/` (absent at v1.2 drafting; N13), then moves
     `idcheck_out_rerun.txt` (13d59e15) there (gitignored), re-hashes it, and writes
     one LOG line giving the old path, the new path and the sha. The file is byte-equal to the committed output, so
     nothing is lost.
  - Both steps happen **before** the pause line, and in the same commit as §1.5 if the gatekeeper wants one commit.
    C2 then passes.
- **Fallback (only if the panel withholds the commit licence).** Move all three to `.session_backup/2026-11-02/c_gd/`
  with one LOG line and the three shas. W8 stays open as a carry; the PI is told.
- **Rejected:** a `.gitignore` entry (it hides the files and leaves W8 silent). Leaving them in place fails C2.
- **Why the commit is safe for G-B.**
  - `gb_integrity` checks the SUMS lines only (l.1043-1060), and HEAD gates.py does not change.
  - `idcheck.py` reads ids only (CC-221r3 Ruling 4: "not a label read").

---

## 4. LOG quiet rule (PINS-B §2.3 step 7, ratified by CC-240 Ruling 3; N2: name every LOG.md writer)

**Rule.** From the pause line until gate-b exits, nobody appends to `.session_backup/2026-10-13/decisions/LOG.md`.
- Why: `tenancy` re-reads it before and after each stream and before the read.
  - A second tagged line gives rc 40.
  - A torn UTF-8 append or an EIO gives rc 50.
  - Either ends G-B.
- The first line after the exit is the coordinator's `OPS-<MMDD>c-gb-result` line (§9).

### 4.1 Writers, and how each is stopped or shown idle

| # | writer | how it writes LOG.md | stop / verify |
|---|---|---|---|
| W-a | coordinator (main session) and gatekeeper | OPS, PI and commit lines by `>>` | Rule: the coordinator is the window's operator. It writes the pause line, then nothing until `gb_rc.txt` exists. A PI chat message in the window is answered in chat and logged **after** the exit. No commit runs in the window |
| W-b | chair via `judge-panel.js` (l.163 appends one line) and judge agents (`.claude/agents/judge.md` writes a CC line) | CC lines | No panel or judge runs in the window. Verify: no workflow listed as running in the coordinator's task list, and no judge agent in `ps` |
| W-c | `novelty-iterate.js`, `expert-review.js` | no direct LOG.md write in the scripts (grep: only `judge-panel.js` names LOG.md), but their agents and their completion step trigger OPS lines (e.g. l.1369, l.1377) | None running. **The MT4 novelty-iterate run (PI-1103s) has finished and logged (LOG l.1401, OPS-1103mt4-iterate2-done); C17 is met.** Re-checked live right before C8 (C17). Not killed for G-B |
| W-d | per-tick paper writers (A→B→C each tick; memory "paper-writing-every-tick") | OPS lines per tick | No `/loop` or scheduled tick runs from the pause line until the resume line. The coordinator stops any loop before C8 and starts none before §9 |
| W-e | Gemini | per memory it writes `SUBAGENT_WORK_LOG.md` and its dashboard, not LOG.md; it acts on the PI's direct orders | At drafting: no Gemini process (`ps`), no crontab, only the `launchpadlib-cache-clean` systemd timer. It can run outside WSL; **the PI closes it for the window** (PI-1103u, Q-PI-T YES) |
| W-f | the other tool (INC-1027a) | unknown tool; it rewrote repo files on 10-27 (memory "other-tool-writes-repo") | Cannot be verified from WSL. **The PI closes it for the window** (PI-1103u, Q-PI-T YES) |
| W-g | B / MT4 / VSPS-J jobs | laptop `*_job.sh` (checked in code); remote jobs write nothing to LOG.md themselves, but their completions lead to coordinator lines | No rental exists (M1 deleted, LOG l.1375). No laptop job (C11, C16). Any remote completion is logged after the exit. **The VSPS-J O1 screen (CC-241r2) starts only after the resume line** (N8) |
| W-h | `gpu_backup.sh` loops | write `.session_backup/machines/backup.log`, not LOG.md, but rsync is heavy /mnt/d I/O | None running at drafting (`ps`). **Not started until the resume line** (no machine to pull; this overrides the memory routine "restart gpu_backup loops each session" for this window). gates.py only checks that the script exists and has no `/dev/shm` (0 hits at drafting) |
| W-i | `d_watch.sh` (pid 106041 at drafting) | never: the full script writes `~/.local/state/vsps/d_watch.log` (ext4) and a one-line probe `.session_backup/.d_watch_probe` on /mnt/d every 60 s | **Keep running** (recommended, panel question P-4); it also feeds C8 (b). It is light I/O and not a `*_job.sh`, and it is the EIO evidence if rc 48 or rc 50 happens. Disclosed as a non-job concurrent process beside prereg §8.2 step 4 |
| W-j | claude-mem worker, aislop PostToolUse hook, codex app-server, MCP servers | none writes LOG.md (aislop scans files touched by Edit/Write; the coordinator makes no Edit/Write in the window) | No action. Disclosed |
| W-k | background agents of any paper (drafters, code writers, readers), incl. workflows and their bash loops (e.g. the arXiv `q.sh` loop) | each such agent may append its own OPS line on completion. Example: LOG l.1391 (`OPS-1103vj-1c-code`, 07:54:37Z) was appended by a VSPS-J code agent while v1 was being drafted | None running. Verify: the coordinator's task list shows no live background agent or workflow, and `ps -eo pid,etime,args` shows no `claude` subprocess other than the coordinator's own session processes and no agent bash loop (`q.sh`, `sleep` loops other than `d_watch`). With no WSL restart (PI-1103u) nothing ends them for us: each must finish and log before C8, and none is started until the resume line |

### 4.2 Proof the rule held (objective, no trust in the list)
- **Right after the pause line,** record `wc -l` and `sha256sum` of LOG.md into `$S/quiet_pre.txt`. Check that the last
  line is the pause line.
- **After gate-b exits and before any new line,** take the same two values again into `$S/quiet_post.txt`. They must be
  equal.
- The result line (§9) cites both. If they differ, the result ruling records which line came in, and the rc tells
  whether it mattered.

---

## 5. Recovery branch: sealed file written, `gb_counts.json` missing (CC-240 N1; keyed on state, not on rc)

### 5.1 Which states lead here, and how the branch is decided
The branch is keyed on the **ACCESS_LOG state**, whatever the rc. After the `gate-b write` row (l.1176) several
failures leave the same state: the sealed file is certified, and `gb_counts.json` is missing or untrusted.
- **rc 48:** `write_new` of `gb_counts.json` fails on /mnt/d drvfs (l.1186): `OSError`, an existing target, or a
  re-read mismatch (l.943-966).
- **rc 50:**
  - `gb_counts_ok` raises (l.1184); or
  - the in-try `_gb_cleanup` meets an `OSError` (l.1185); or
  - any other exception after l.1176.
- **rc 49:** SIGTERM, SIGINT or SIGHUP arrives after l.1176.
- The rc does **not** tell this state apart from others. rc 48 can also come from the sealed write (l.1175), and rc
  49/50 from anywhere after the marker.

The branch is decided **from ACCESS_LOG rows and file presence only** (actions and shas; no sealed byte read):

| state after `gate-b start` | meaning | branch |
|---|---|---|
| `gate-b write` row present (sealed sha S), `gate-b abort <rc>` with rc 48, 49 or 50, and `gb_counts.json` absent (or present but untrusted, below) | sealed written and verified (sha + mode 0400 re-read inside `write_new` before the row); the failure came after it | **R-A** (this section) |
| no `gate-b write` row, `gate-b abort <rc>` (any rc) | no sealed bytes are certified (a partial `gb_intermediate.json` may exist, or a `.gb_intermediate.json.<pid>.tmp`) | **R-B** = the prereg §9.4 loss branch (NOT COMPUTED) and a re-download ruling (§7) |
| `gate-b write` row and no abort row (SIGKILL or power loss after l.1176) | the same as R-A for the sealed file; tmpfs residue is handled as in §7.3 | **R-A** plus the SIGKILL-residue step |
| `gate-b start` row, **no** `gate-b write` row and **no** abort row (SIGKILL or power loss after the marker and before l.1176; N2) | no sealed bytes are certified; tmpfs residue and a partial sealed or `.tmp` file are possible | **R-B** plus the SIGKILL-residue step |

- In R-A, check the `gate-b unlink` rows (0-2). If the cleanup did not finish, tmpfs residue is removed by hand with an
  `unlink (hand)` row (PINS-B §2.5(d)).
- Also check `manuscript/prereg/2026-11-02_c_pvr_tier1/` for `gb_counts.json` and `.gb_counts.json.<pid>.tmp`.
  - `os.link` can succeed and the re-read then fail, so a `gb_counts.json` may exist after rc 48.
  - Under R-A such a file is **not trusted**. It is kept, hashed and compared field by field with §5.3. Equal = it is
    adopted by the ruling. Different = it is discarded with its sha in the LOG.
  - A leftover `.tmp` is hashed, then removed with a LOG line.

### 5.2 What is and is not recoverable under R-A

| `gb_counts.json` key | recovered from | exact? |
|---|---|---|
| `n_e_gb`, `present_pairs`, `absent_pairs` | sealed bytes, §5.3 | yes: `sealed_bytes` (l.1062-1066) maps every `statuses` entry to one key with sorted present/absent lists, and gate_b computes the same three numbers from the same `st` (l.1178-1181) |
| `coverage_share`, `remaining` | `n_e_gb / 10496`, 10496 | yes (`GB_REMAINING`; `len(rem)` checked = 10,496 before the marker) |
| `sealed_sha256` | the `gate-b write` row | yes |
| `streams.*.md5`, `bucket_md5`, `record_md5` | = record md5 8720e72f... / 8a711a15... | yes: the run passed `r["md5"] == bmd5 == rec_md5[s]` for both streams |
| `streams.*.bytes` | = Content-Length 28,392,297 / 93,606,939 (C14) | yes: the run passed `r["bytes"] == clen` |
| `streams.*.filtered_sha256` | the two `gate-b unlink` rows | yes (`written[fp]` is the sha written to the row) |
| `streams.*.sha256` (full-stream sha256) | **not recoverable** | no: held only in memory. **In `gb_counts_recovered.json` both values are `"NOT RECORDED (gb_counts.json not written)"` and are labelled unverified** (N7). Any prereg §9.4 reconciliation (CC-220 Ruling 4) would then rest on md5 + byte count only, and **needs its own ruling at 92** |
| `utc` | the `gate-b write` row stamp (labelled as such) | approximate |
| `inputs` | the pins (8 PINS_B + 3 A12) + `/usr/bin/curl` sha re-hashed at the exit (C3) | yes for the pins; curl = the post-exit hash (disclosed) |
| `label`, `gates_sha256`, `ga_remaining_sha256` | constants | yes |

### 5.3 The counts-only open (stated override of prereg §9.4 "one open")
- **The conflict.** Prereg §9.4 allows exactly two entries for the sealed file: `write` (G-B) and **one** `open` at the
  tier-3 freeze. Deriving the counts is a further read.
- **R-A therefore needs a ruling at 92 that adds one entry: `open-count`.** It is counts only, and it does **not**
  use up the tier-3 open. The ruling is written before any read. It is not licensed by this panel. This panel only
  registers its shape.
- **Procedure.**
  - (i) Append an ACCESS_LOG row `<utc>\tcoordinator\topen-count (hand)\t<path>\t<S>`, plus a LOG mirror line.
  - (ii) Run the pinned script below (its sha goes into that ruling) on ext4, output to `$S`.
  - (iii) Write `gb_counts_recovered.json` (not `gb_counts.json`) with the §5.2 values. `streams.*.sha256` =
    `"NOT RECORDED (gb_counts.json not written)"`.
  - (iv) A one-judge read checks it before the gatekeeper commit.
- **Script text (fixed now; prints the five numbers and nothing else; no id, class or list leaves the process):**
```python
import hashlib, json, sys
from pathlib import Path
p = Path.home() / ".vsps_sealed/c_pvr/gb_intermediate.json"
b = p.read_bytes()
if hashlib.sha256(b).hexdigest() != sys.argv[1]:          # S from the 'gate-b write' row
    raise SystemExit("FAULT: sealed sha differs; loss branch (prereg §9.4)")
d = json.loads(b)
if (json.dumps(d, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode() != b:
    raise SystemExit("FAULT: sealed bytes are not in gates.py sealed_bytes form")
n = len(d)
print(json.dumps({"n_e_gb": n, "present_pairs": sum(len(v["present"]) for v in d.values()),
                  "absent_pairs": sum(len(v["absent"]) for v in d.values()),
                  "coverage_share": n / 10496, "remaining": 10496}, sort_keys=True))
```
- **Not allowed:** a re-download to rebuild the full-stream sha256s; any other read of the sealed file; printing any
  per-id or per-class value.
- **Next sha (CC-240 N1).** It writes an ext4 copy of `gb_counts.json` before the /mnt/d write. That change is not made
  here.

---

## 6. Pre-written rule: n_e_gb = 0, or 0 kept test rows, is an instrument FAULT (CC-240 N5 (a))

- **Rule.** Each case below is an **instrument FAULT**, not a result. It goes to a ruling at 92. No power check and no
  tier-2 use follow. No vocabulary or map change is allowed as a "fix" (prereg §9.3 W3); a fix is a new instrument
  under a ruling.
  - (F1) `n_e_gb` = 0.
  - (F2) `streams.test.filtered_sha256` equals the sha of a header-only file. That means 0 kept test rows:
    - LF header `ImageID,Source,LabelName,Confidence\n` = 69c66382838062dbeaa0f58e554856bdfdecc322ec5d3787cf9f85a0d97f2c95;
    - CRLF variant = 8c20466cff6ba1b6dfb34b13d04f0dcda3e55aede4c8a3993ca801a1fa1358c4. (`gb_filter` keeps a CR inside
      the record and appends `\n`, PINS-B §2.3.)
  - (F3) `streams.val.filtered_sha256` is **not** one of those two values. This cannot happen after rc 0 (rc 45), so
    seeing it is an internal inconsistency.
- **Each case is checked without opening anything.** It uses only the `gb_counts.json` fields and ACCESS_LOG shas. For
  F1 a third check is possible: `sealed_sha256` = sha256 of `{}\n` =
  ca3d163bab055381827226140568f3bef7eaac187cebd76878e0b63e9e442356.
- **Likely causes the ruling looks at, in this order (no gold read):**
  - the id format of `ga_remaining_ids.txt` against the stream key (16-hex OI ImageIDs; amendment v1.3 l.350-352);
  - the map/description resolution (69 classes; parity passed);
  - the CSV header form.
- **Not a FAULT.** `n_e_gb` > 0 with low `coverage_share` is a result. It goes to the registered power check at tier 2
  (§5.6, n_e_power, Q-B7). No threshold is added now.

---

## 7. Re-download ruling shape for transport aborts rc 41 / 42 / 43 / 47 (CC-240 N5 (b))

### 7.1 Finding: under 3bced05e a second run cannot start at all
- `gb_refuse` (l.1029-1041) refuses for ever once ACCESS_LOG holds any `gate-b start` row (l.1039-1040). The selftest
  makes this a registered behaviour: G17 "`gate-b start` row alone → REFUSED" (PINS-B §3.3 l.346).
- ACCESS_LOG is append-only (prereg §9.4).
- So removing `gb_start` (PINS-B §2.5(d): "Removing the start marker is a re-download and needs its own ruling at 92")
  is **not sufficient**. Every post-marker abort (rc 40-50) ends G-B under the pinned sha.
- A re-download therefore needs **a successor gates.py (B′)** with its own full panel at 92 and its own mutant run. Its
  only new behaviour would be a ruled re-run path, e.g. it starts only if:
  - ACCESS_LOG holds exactly one `gate-b start`, followed by exactly one `gate-b abort <rc>` with rc in the licensed set;
  - no `gate-b write` row exists;
  - a hand row `gate-b relicense CC-<nnn>` follows.
  - The CC-240 hardening items fit the same sha: curl stall timeout, `pthread_sigmask`, the ext4 copy of
    `gb_counts.json`, the `OverflowError` catch, `-A` on `CURL_HEAD`, the N8 mutant rows.
- **Not allowed:** editing ACCESS_LOG; running with a different `HOME` to dodge the refusal (the sealed path is fixed
  by prereg §9.4).

### 7.2 Evidence the re-download ruling must cite
- **ACCESS_LOG rows:**
  - `gate-b start <3bced05e>`, then 0-2 `gate-b unlink` rows (each with its sha), then `gate-b abort <rc>`;
  - **no** `gate-b write` row; `gb_intermediate.json` and `gb_counts.json` absent; `/dev/shm/c_pvr_gb` absent.
- **Files:** `gb_stdout.txt` and `gb_stderr.txt` empty (post-marker silence); `gb_rc.txt`; `$S/quiet_*.txt` (§4.2);
  the coordinator's `/proc/<curl>/io` trace (§8.2); the `d_watch.log` window; a post-exit HEAD-only check as C14.
- **Stated correction of CC-240 N5(b) (CC-242 Ruling 7; N3).** N5(b) named "no unlink rows" as evidence. The code
  writes 0-2 `gate-b unlink` rows on a transport abort, depending on the stage (`_gb_cleanup`, l.1082-1092), so the
  table below replaces that wording. CC-242 governs.
- **Expected `gate-b unlink` rows by stage.** The unlink count tells the stage and so the class:

| rc | stage | unlink rows | class |
|---|---|---|---|
| 41 | HEAD of val / of test | 0 / 1 (filtered-val) | transport **if** the post-exit HEAD-only check (C14 form) shows the object unchanged (same md5, length, no Content-Encoding); otherwise content (STOP, PI). The post-exit HEAD check decides (CC-242 Ruling 7) |
| 42 | bucket md5 ≠ record, before the body of val / test | 0 / 1 | **content: the object changed**; a re-download cannot give the pinned bytes, so STOP, and P_obj^VI goes to the PI (no re-download) |
| 42 | full-stream md5 ≠ bucket/record, after the body of val / test | 1 / 2 | transport (corrupt transfer) |
| 43 | body curl rc ≠ 0, val / test (file opened `O_EXCL` before curl) | 1 / 2 | transport |
| 47 | streamed bytes ≠ Content-Length, val / test | 1 / 2 | transport |

- (A 47 from an `allow_read` mismatch at the single read gives 2 rows. It is an instrument fault, not transport, and
  goes to its own ruling.)

### 7.3 What the re-download ruling must establish
1. No gold reached any agent or any file outside tmpfs.
   - Nothing was printed (Q-B11).
   - The unlink rows match the stage table.
   - The single read (l.1172) comes only after both streams pass, so in a transport abort gates.py parsed no label row.
2. The class is transport by the table above. Content (pre-body 42) = STOP.
3. The (B′) instrument: §7.1, own 92 panel, its own mutant run.
4. The rerun must give full-stream md5 = record md5 (in code) and, at the tier-3 reconciliation, the conditions of
   prereg §9.4 / CC-220 Ruling 4.
5. **One** licensed re-run. A second transport abort goes to the PI.
6. The same tenancy steps and a new pause line with a new tag.

- **Other post-marker aborts.** rc 40, 44, 45, 46, 49 and 50 also end G-B. Each goes to its own 92 ruling with the
  same evidence list. The cause analysis differs: tenancy; content/format; instrument; signal; internal.
- **SIGKILL residue** (PINS-B §2.5(d)): the coordinator removes only the tmpfs residue, by hand, with an `unlink (hand)`
  row and a LOG line. Everything else follows §7.1.

---

## 8. Disclosures carried from CC-240 and how the window handles them

### 8.1 Disclosures (verbatim sense of the pin LOG line l.1388)
- **No WSL restart before G-B (PI-1103u; departs from CC-240 N1).** N1 asked for G-B "only right after a WSL restart
  and a /mnt/d health check". The PI chose no restart. The run therefore uses a 9p channel that has been up since the
  last outage, and the EIO risk is higher than N1 intended. Mitigations:
  - the C8 health check (d_watch clean since the last outage, the pinned `write_new` 0o444 probe on /mnt/d (C8(c), as LOG l.1405), SUMS over
    9p) within 5 min before the pause line;
  - C12 (strict UTF-8 read of LOG.md);
  - near-zero concurrent /mnt/d I/O (C9, §4).
  - Consequences of an EIO: one after the sealed write goes to the §5 branch; one before it goes to §7 and ends G-B.
- **N3.** `CURL_HEAD`/`CURL_STREAM` (gates.py l.738-740) have no `--max-time`/`--speed-time`, so a curl stall has no
  timeout. The coordinator watches (§8.2). The next (B) sha adds a stall timeout.
- **N4.** There are signal windows:
  - between the marker and `gate-b start` row (l.1129-1130) and the handler install (l.1135);
  - in except/finally (SIG_IGN before cleanup).
  - A default SIGINT there can skip the abort row or the cleanup. No gold is printed.
  - The next sha uses `pthread_sigmask`.
- **N6.** `int(float('inf'))` raises `OverflowError`, outside the `ValueError`/`TypeError` catch (l.792-798). It maps
  to rc 50, not 46. It is silent and leaks nothing, and a malformed gold row aborts either way.
- **N10.** `/dev/shm/c_pvr_gb.lock` persists after the run, and `CURL_HEAD` lacks `-A vsps-research`. Both are known.
- **PINS-B §2.5 (c).** "Never touches disk" is procedural: tmpfs pages may go to WSL swap.

### 8.2 Window handling (binding once ruled; the numbers are [proposal])
- **No signal to gates.py except the single end-state SIGTERM of §8.3 step E2.**
  - Launched detached (§2.1).
  - No Ctrl-C; no `kill` aimed at the gates.py pid before E2; an agent never sends SIGKILL.
  - The N4 window is the first seconds after the marker (one write + one fsynced append). No action is taken then.
- **Progress watch without gold.** Every 60 s the coordinator reads `/proc/<curl pid>/io` (`wchar`, the bytes curl has
  written to the pipe) and `/proc/<gates pid>/stat`, into `$S/watch.txt`.
  - `wchar` measures the public transfer only (≤ 121,999,236 B in total).
  - The filtered tmpfs files are **not** watched: their size is a function of test-gold rows, and val keeps 0 rows by
    design.
- **Expected time [est.].**
  - Pre-marker checks: about 1-3 min (SUMS, gate-a verify and parity over 9p).
  - Streams: 116.3 MiB, under 2 min at 1 MB/s or more.
  - Read and writes: seconds.
  - gate-b about 3-10 min. Whole window, C8 to resume line: about 20-30 min.
- **Stall rule.** If one curl pid's `wchar` stays the same for **15 min**, the coordinator sends **SIGTERM to that curl
  pid only** (`kill -TERM "$CP"`, with `CP` from the §2.1 pid route: `sh.pid` -> `pgrep -P "$SH" -x python3` ->
  `pgrep -P "$GP" -x curl`; never `pgrep -f` or `pkill -f`).
  - gates.py then sees curl rc ≠ 0. That is rc 41 (HEAD), rc 43 (body), or rc 44 (empty stream). gates.py then runs its
    own cleanup and abort row. This is cleaner than signalling gates.py (no N4 window). It consumes the run (§7).
- **Max wall time.** It is **60 min** from the `gate-b start` row (its ACCESS_LOG stamp). At 60 min the coordinator
  applies the stall action to any live curl, then follows §8.3.
- **Laptop power.** The laptop stays on mains power, sleep off, lid open, Windows Update restart deferred (C18). Sleep
  or a power loss is SIGKILL residue (§5.1 rows 3-4, §7.3).

### 8.3 End state when gates.py outlives the wall (CC-242 Ruling 8; Codex C1, BLOCKING)
All times are counted from the `gate-b start` row. `GP` comes from the §2.1 pid route. Every observation goes to
`$S/hang.txt` on ext4, and no LOG line is written until step E4.

| step | when | condition | named action | ACCESS_LOG state -> branch |
|---|---|---|---|---|
| E1 | 60 min | a curl child is live | SIGTERM to that curl pid only (§8.2) | gates.py then aborts on its own path (rc 41/43/44): start + 0-2 unlink + abort -> R-B (§7) |
| E2 | 70 min | gates.py alive and **no** curl child | record `/proc/$GP/stat` (state field), `/proc/$GP/wchan` and the ACCESS_LOG actions (no sealed byte read); then **one SIGTERM to `$GP`** | the handler gives rc 49 and the `finally` cleans up and writes `gate-b abort 49`. With a `gate-b write` row -> **R-A** (§5); without -> **R-B** (§7). The N4 windows (marker + start row, and the `finally`) are long past or already ignoring signals, so the SIGTERM lands in the `try` |
| E3 | 80 min | gates.py still alive (typically state `D`: blocked in a 9p syscall that never returns) | run C8(a) and C8(c) under `timeout 20`. **/mnt/d dead** (probe times out or EIO): the coordinator asks the PI in chat for a WSL restart, the only way to end a process stuck in uninterruptible 9p I/O. **/mnt/d alive:** the PI is told and asked for the same restart. Agents never send SIGKILL | the restart SIGKILLs gates.py. Write row present, no abort row -> **R-A** + residue (§5.1 row 3); start row only -> **R-B** + residue (§5.1 row 4) |
| E4 | when gates.py has exited (E1, E2, or after the E3 restart) | – | **the coordinator writes the `OPS-<MMDD>c-gb-result` line** as the first LOG line after the pause line: rc (or "killed by WSL restart"), the E-step reached, `hang.txt` sha, the ACCESS_LOG state and branch, quiet_pre/post; then **immediately the `OPS-<MMDD>c-gb-resume` line**, which ends the pause | the branch named in the result line goes to its ruling (§5, §7: full panel at 92) |

- **Why E2 sends a signal now when v1.1 sent none.** After 70 min with no curl child, gates.py has no network work
  left. It is either blocked (9p) or failing. Waiting longer recovers nothing, and leaves the LOG pause open-ended,
  which CC-242 Ruling 8 forbids.
  - SIGTERM goes through the pinned handler (`_gb_signal` -> `GBAbort("signal")`), so the cleanup, the unlink rows and
    the abort row are written by gates.py itself.
  - The sealed file, if certified, survives (R-A).
- **The window always ends at E4.** If /mnt/d is dead, E4 is written after the restart, from the recovered session. A
  RESUME note on ext4 (`$S/RESUME.txt`, written at E3) says which step was reached.

---

## 9. After G-B: which output goes to which ruling; test gold stays closed

### 9.1 Outputs on rc 0

| output | where | holds | goes to |
|---|---|---|---|
| `gb_counts.json` | `manuscript/prereg/2026-11-02_c_pvr_tier1/` (/mnt/d) | the registered keys only (`GB_KEYS`) | result line, result read, gatekeeper commit |
| `gb_intermediate.json` | `~/.vsps_sealed/c_pvr/` (ext4, 0400) | per-id present/absent sets | **never read**; sha only, from the `gate-b write` row and `gb_counts.sealed_sha256` |
| ACCESS_LOG rows | `~/.vsps_sealed/c_pvr/ACCESS_LOG.tsv` | start, unlink ×2, write | mirrored in the result line (prereg §9.4: a LOG line mirrors each entry; written only after the exit) |
| `gb_stdout.txt`, `gb_stderr.txt`, `gb_rc.txt`, `quiet_*.txt`, `watch.txt`, `pre.txt` | `$S` (ext4) | aggregates, rc, stamps | evidence copies to `.session_backup/<date>/c_gb/` with shas |

### 9.2 Steps
1. **`OPS-<MMDD>c-gb-result` line** (first line after the pause line). It holds:
   - rc and stamps; `gb_counts.json` sha; the four numbers; the stream md5/bytes/filtered shas; the `sealed_sha256`;
   - the ACCESS_LOG mirror rows; the quiet proof (§4.2);
   - the curl and python re-hash after the exit, compared with C3. The code records `inputs["/usr/bin/curl"]` but never
     compares it, so this line does.
2. **`OPS-<MMDD>c-gb-resume` line.** It ends the pause, and agents may log again. gpu_backup and the tick loop may
   restart.
3. **Result read** (proposed: one judge, reversible 90, because the numbers cannot be changed and no choice is made).
   It checks:
   - §6 F1-F3;
   - `gates_sha256` = 3bced05e; `ga_remaining_sha256` = 3feccabc; `remaining` 10,496;
   - stream md5 = 8720e72f / 8a711a15; bytes = 28,392,297 / 93,606,939;
   - `inputs` = the pins; curl = 1ccbd3da;
   - `coverage_share` = `n_e_gb` / 10,496.
   - Any F1-F3 hit (§6) or any abort (§5, §7, §8.3) goes to a **full panel at 92** instead (N10).
4. **Gatekeeper commit** (prereg §9.4 "gatekeeper commit right after G-B"): `gb_counts.json`, plus
   `GB_SEALED.sha256` (one line: `<sealed_sha256>  gb_intermediate.json`), plus the LOG line. The n-gram scan runs on
   both. The sealed file itself is never committed, copied or backed up.
5. **Use of the numbers.**
   - `n_e_gb` feeds `n_e_power` = n_e_gb − w25_flagged − lost − 4 at tier 2 (PINS-B §2.6, Q-B7; prereg §5.6). That
     happens after the pixel W25 (prereg §9.1 step 8, its own pause window), not now.
   - No vocabulary or map change after G-B (prereg §9.3, W3).
6. **Next laptop job.** The VSPS-J O1 screen (CC-241r2) starts only after the resume line (N8).
7. **Salami guard (CC-242 Ruling 10; N16).** C never re-reports A's NoCaps val numbers (A number_manifest l.120) as C's
   own claims. C's tier-2 use of NoCaps val produces new numbers under its own prereg. Any A number shown in C is cited
   to A.

### 9.3 Test gold stays closed
- Beyond gates.py's single read (l.1172), nobody opens test gold:
  - the filtered tmpfs files are unlinked by gates.py;
  - the sealed file is opened only at the tier-3 freeze (prereg §9.4), or by the §5.3 count script under its own 92
    ruling;
  - every later subcommand refuses `oidv7-*-annotations*` and `/dev/shm/c_pvr_gb/` (prereg §9.6).
- No agent reads ACCESS_LOG beyond its action and sha fields. No Open Images test label body, NoCaps data or
  `nocaps_val_4500_captions.json` is opened by any step here.

---

## 10. PI answers (PI-1103u, LOG l.1393, 2026-11-03T08:03:25Z): decided facts, no longer questions

| # | question (v1) | PI answer (binding) | where it is applied |
|---|---|---|---|
| Q-PI-2 | run G-B once in the first idle laptop window after the Q11 GO, every LOG writer paused | **YES**, with the MT4 novelty-iterate run finished first | §2, §4, C16, C17 |
| Q-PI-W | WSL restart (`wsl --shutdown`) at the window's start | **NO restart.** Replaced by a /mnt/d health check right before the run (d_watch clean + probe write/read/fsync on /mnt/d + strict UTF-8 read of LOG.md), **disclosed as a higher EIO risk** | C7, C8, C12, §8.1 |
| Q-PI-T | Gemini and the other tool (INC-1027a) closed for the window | **YES**: the PI closes both | W-e, W-f, C15 |
| Q-PI-ID | idcheck disposition | **Commit** `idcheck.py` + `idcheck_out.txt` (closes CC-214r3 W8); **archive** `idcheck_out_rerun.txt` | §3.1, C2 |
| Q-PI-RR | run under the pinned version, or build a re-runnable version first | **Run under the pinned gates.py 3bced05e** (no re-run path; a new version only if a failure happens) | header, §7.1 |
| FYI | Q11 itself | YES since PI-1102a (L2-P1 -> 36,707, NoCaps val to C); this panel makes the ledger edit and the G-B run text binding | §1 |

- **Why "run now under the pinned version" holds.** A new version is needed only if a failure happens after the
  marker. Building it then costs the same as building it now (one new sha, a full 92 panel, a mutant run). Building it
  first would spend that cost on the expected path too, where G-B passes.
- No PI question from v1/v1.1 is open.

### 10.1 CC-242 "For the PI" items and their status in v1.2

| # | item | status / default |
|---|---|---|
| Q1 | if the pinned `write_new` fails on /mnt/d, build B′ (ext4 copy of `gb_counts.json` first) before G-B? | **Not triggered**: the anchor probe PASSED (LOG l.1405). It stays the registered branch if C8(c) fails at window time. Recommended YES; default HOLD G-B until B′ is pinned |
| Q2 | split the Q11 ledger and idcheck commit from the run plan? | v1.2 keeps **one commit** (§1.6), as CC-242 recommends (NO split). Default: one commit after the round-2 GO |
| Q3 | confirm in chat, before the window: Gemini and the other tool closed; mains, sleep off, lid open; Windows Update restart deferred | becomes **C18** (a PI LOG line before C8). Default: the window does not open without it |
| FYI | no-WSL-restart answer kept as an explicit overrule of CC-240 N1 (CC-242 Ruling 6) | C7, §8.1 |

## 11. Questions for the round-2 panel (rulings requested; each with a recommendation)

| # | ruling requested | recommended |
|---|---|---|
| P-1 | Q11 = YES as §1.3 (CC-242 Ruling 1); PORTFOLIO text, the 4 edits incl. the l.193 tail, and staging as §1.5; effective at the §1.6 commit | YES |
| P-2 | One gatekeeper commit (§1.6): PORTFOLIO patch + idcheck.py + idcheck_out.txt + this file, n-gram scan, before the pause line (B2) | YES |
| P-3 | Command, launch guard, detached launch, pid route, §2 tag form, pause line text, tag hygiene, pre-marker FAULT branch with `gbpause2` (§2) | YES |
| P-4 | Checklist C1-C20 as §3, incl. C8(c) = the pinned `write_new` probe of LOG l.1405 (B3), C7 (no WSL restart; CC-242 Ruling 6), C18 (PI line), C19 (usage), C20 (no bytecode); idcheck disposition §3.1 | YES |
| P-5 | LOG quiet rule writers W-a..W-k as §4.1, keeping `d_watch` as a disclosed non-job process; the quiet proof §4.2 | YES (keep d_watch) |
| P-6 | Recovery branch §5: four ACCESS_LOG states -> R-A / R-B (+ residue), whatever the rc; `open-count` as a stated override needing its own 92 ruling; the script text fixed now; N7 labels | YES |
| P-7 | §6 FAULT rule F1-F3, header-only shas fixed now | YES |
| P-8 | §7: no re-run path under 3bced05e; the stage/class table as the stated correction of CC-240 N5(b); rc 41 class decided by the post-exit HEAD check | YES |
| P-9 | §8.2-§8.3: stall 15 min (curl-only SIGTERM), wall 60 min, end-state ladder E1-E4 with one SIGTERM to gates.py at 70 min (Codex C1) | YES [proposal values] |
| P-10 | §9: result read = one judge at 90 unless F1-F3 or an abort (then a full panel at 92); O1 after resume; salami guard | YES |

## 12. Touches during drafting (`date -u` 2026-11-03, v1 about 07:22-07:55Z; v1.1 about 08:00-08:20Z; v1.2 about 10:35-11:05Z)
- **Read.**
  - CC-240 in full; CC-239, CC-236, CC-236r2, CC-236r3, CC-214r3, CC-221, CC-221r3 and CC-232 (grep-targeted lines);
  - LOG l.1140, l.1153, l.1295, l.1323, l.1340-1390 (l.1380, l.1388, l.1389 in full);
  - prereg v1.2 §7-§15; PINS_B_DRAFT_v1_1 §1-§2.6 and §4-§11; amendment v1.3 l.200-212, l.318-351 (grep);
  - gates.py l.725-760, l.832-845, l.943-968, l.970-1250;
  - `ga_counts.json` (committed aggregates); PORTFOLIO §2.3 at HEAD and `git diff` of it;
  - `~/.config/vsps/d_watch.sh` in full, `gpu_backup.sh` head and grep; `.claude/workflows/*.js` (grep LOG.md);
  - memory notes on Gemini, INC-1027a, EIO and per-tick writers;
  - v1.1: LOG l.1391 (VSPS-J code agent line, W-k), l.1393 (PI-1103u); gates.py l.1182-1188 re-read for §5;
  - v1.2: CC-242.txt in full; LOG l.1401, l.1404, l.1405; HEAD PORTFOLIO l.191 and l.193; gates.py l.194-204 and
    l.1082; `systemctl list-timers 'apt-daily*'`; `git diff --stat ec9466b HEAD -- scripts/c_pvr` (empty);
    `git status --porcelain --ignored scripts/c_pvr` (only the three idcheck files); `usage_check.sh` (script text).
- **Hashed or counted, no content read:**
  - the 3 idcheck files and their `.session_backup` originals;
  - ACCESS_LOG (sha, rows, `gate-b` count 0);
  - /usr/bin/curl, /usr/bin/python3.12; SUMS 16 OK; the LOG UTF-8 decode;
  - two header byte strings; `{}\n`.
- **Process scan:** `ps`, `/proc/*/cmdline` for `_job.sh` (none), crontab (none), user timers.
- **Not run:** gate-b, parity, gate-a, selftest, the write_new probe (the coordinator ran it, l.1405), any network
  request. Nothing moved or committed. v1 (302e4c96) and v1.1 (a262cc75) are unchanged; v1.2 is a copy of v1.1 edited
  in place.
- **Not opened:** no Open Images label body, no NoCaps data, no `nocaps_val_4500_captions.json`, no sealed file.

## 13. CC-242 item -> v1.2 section

| CC-242 item | what v1.2 does | section |
|---|---|---|
| B1 / W1 (J1 B1 = J2 W1 = J3 W1) | 4th PORTFOLIO edit replaces the l.193 tail (J2 wording, `CC-242rN`); cite l.191; 4 changed lines; staged-blob grep = 0 | §1.5 |
| B2 / W2 | this file enters the same commit as PORTFOLIO + idcheck, n-gram scan, before the pause line; CC-242 governs superseded CC-240 N-text | §1.6, header |
| B3 / W3 | C8(c) = the pinned `write_new` probe as run at LOG l.1405; 'exact drvfs path' claim struck; fail -> no G-B, B′ + PI Q1 | §3 C8, §10.1 |
| C1 (Codex) / Ruling 8 | end-state ladder E1-E4: named actions, ACCESS_LOG state -> branch, result line writer, resume line | §8.3 |
| Ruling 1 | Q11 YES; C decodes none of nocaps val before its tier-2 prereg | §1.1, §1.3 |
| Ruling 2 | idcheck commit and archive | §1.6, §3.1 |
| Ruling 6 | PI-1103u overrules CC-240 N1's restart clause, disclosed | header, C7, §8.1 |
| Ruling 7 / N3 | §7.2 states the correction of CC-240 N5(b); rc 41 class by the post-exit HEAD check | §7.2 |
| Ruling 9 | round 2 = full panel on v1.2 + the probe anchor | §11 |
| Ruling 10 / N16 (W11) | salami guard: no A NoCaps val numbers re-reported as C's | §9.2 step 7 |
| N1 | gates.py l.196-203 cited as the operational set rule | §1.3 |
| N2 | 4th ACCESS_LOG state (start, no write, no abort) -> R-B + residue | §5.1 |
| N4 | pause-line stamp `$(date -u +%FT%TZ)` once; generic tag only in CC/LOG/commit | §2.3, §1.6 |
| N5 | C6 names `CC-242rN` GO, not revoked | §3 C6 |
| N6 | PI confirmations LOG line before C8, cited in the pause line; apt-daily timers checked | §3 C18, C3, §2.3 |
| N7 | R-A streams sha256 labelled NOT RECORDED / unverified; reconciliation needs its own 92 ruling | §5.2 |
| N8 | VSPS-J O1 screen only after the resume line | §4.1 W-g, §9.2 step 6 |
| N9 | C17 met (l.1401, l.1403); live W-k re-check right before C8 | §3 C17, C9 |
| N10 | result read one judge at 90; F1-F3 or any abort -> full panel at 92 | §9.2 step 3 |
| N11 | launch guard (no `$S`, no `gb_rc.txt`, fresh mode 700); pre-marker FAULT branch + `gbpause2` after a one-judge read | §2.1, §2.4 |
| N12 | usage headroom ≥ about 90 min; the usage guard writes nothing in the window | §3 C19 |
| N13 | `mkdir -p .session_backup/2026-11-02/c_gd/` before the archive move | §1.6, §3.1 |
| N14 | status line: HEAD 8511fe6; `git diff ec9466b HEAD -- scripts/c_pvr` empty before, idcheck-only after | header, §3 C5, §1.6 |
| N15 | l.68 / l.291 named stale in the commit message | §1.5 |
| Coordinator: `__pycache__` | C20: no `__pycache__` / `.pyc` and `--ignored` porcelain empty under `scripts/c_pvr` | §3 C20 |
| Coordinator: C17 met | recorded with line numbers | §3 C17 |
