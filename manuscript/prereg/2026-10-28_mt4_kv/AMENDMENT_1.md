# MT4 confirmatory PREREG, AMENDMENT 1 (DRAFT): fixed NOT_AFTER, a mechanical Branch K2 freeze, and the m3 role

**Label: PREREG AMENDMENT.** This is not the §8 cost-only amendment. §8 l.145 forbids that route from changing the freeze rule or the binding branch (CC-162 ruling 2, rejected 3/3).

**Status:** DRAFT v5 (final hardening round), 2026-10-29, adds the threat model (A0), the fixed `KV_PRED_SUMS` path, and the re-run of the decision in `check`; applies the Codex round-4 (91) fixes (kept set pinned; duplicate halts; GitHub receipt time in code) and CC-162a F2–F5, the Codex re-read (93) items (a)–(c), CC-162b G1–G2, and the Codex round-3 (95) blockers (an external time anchor for the decision; the KV freeze tool `scripts/mt4_kv/kv_freeze.py`). Written **blind**:
- no K2 Gate 1 val decode and no `gate1_decide.json` exist;
- no confirmatory training has run;
- no KV image has been staged and no KV prediction exists.

The Gate 1 outputs that do exist (teacher, detect, timing, two adapters) are training-side and were read by sha only (CC-135).

**Tier: IRREVERSIBLE (CC-162 Part B, 88% < 98%).** It binds only after all of these:
- the PI's explicit answer to CC-162 Q1 and Q2;
- an independent Codex read;
- a one-judge diff read;
- the gatekeeper's commit, together with K2 Gate 1 Amendment 2 (`2026-10-28_k2_gate1/AMENDMENT_2_DRAFT.md`), before any K2 file is restored to M1 and before any Gate 1 output.

`PREREG.md` stays byte-identical (dd0fe943…). This file's sha joins `2026-10-28_mt4_kv/SHA256SUMS` and both K2 `SHA256SUMS` copies at the commit.

**If the PI does not answer:**
- this file is not committed;
- K2 stays HELD after P50;
- the current text binds: Branch K2 freezes about 11-18, and a late or missing Gate 1 means Branch K1+K6.

**Sources:** CC-162 rulings 2, 3 and 8, W1 and W8; CC-162 Codex review; PI-1029h (CC-160 Q1, Q2); PREREG §0, §2, §8, §9 and §5; K2 Gate 1 RULE §5–§7.

## A0. Threat model (round 6; the bypass hunt stops here)

**In scope: enforced by code, and selftested.**
- An honest operator or agent choosing a branch, a freeze date or a kept set after seeing results:
  - `NOT_AFTER` is checked at the write;
  - the decision is anchored, and its push is received by GitHub before `NOT_AFTER`;
  - `check` re-runs the decision on its recorded inputs and requires the identical result;
  - the A4 deadline test is mechanical;
  - the kept set is read only from the pinned, committed `kv_kept.json`;
  - the freeze instant comes from the log and D.
- An accidental resume from partial outputs: every attempt starts from zero (`fresh`).
- A host lost mid-step: the open start is charged its full logged timeout before any retry (exit 6), and the ledger line is fsynced.
- A late or partial freeze: no freeze before its instant, and no partial freeze before D.
- Duplicate lines, and lines outside the kept set:
  - another sha for a kept system and seed is a FAULT that halts the freeze;
  - a same-sha repeat is descriptive;
  - lines outside the kept set are descriptive;
  - out-of-order lines halt the freeze.

**Out of scope for code: enforced by the audit trail.** The trail is WORKFLOW_LOG and the decision LOG, the git history, GitHub's push receipts, and disclosure in the paper. Deliberate tampering is not something the code can prevent:
- setting a host's system clock back or forward, including clock skew in the UTC column of `KV_PRED_SUMS`. Those times come from the decoding host's clock, and the code checks only their order and that they follow the GO's push;
- running `freeze` at a false "now";
- hand-writing or hand-editing JSON or `KV_PRED_SUMS` lines outside the tools;
- force-pushing q2 `main` to remove or replace an anchor;
- editing the tools themselves; their shas are pinned and the gatekeeper checks the committed bytes.

**Requested from the PI:** GitHub branch protection on q2 `main` (no force-push, no deletion), so that an anchor cannot be removed after the verdict is seen.

**Where `check` runs:** only on the laptop. It needs `gh` credentials for the GitHub API, and M1 never receives them. M1 writes the decision; the laptop anchors it, pushes it, and checks it.

## A1. `NOT_AFTER` (replaces "the freeze date" as the Gate 1 deadline)

- **`NOT_AFTER` = 2026-11-10T12:00:00Z** (epoch 1794312000). It is the constant `k2_gate1.NOT_AFTER` at the amendment commit; the code and this text name the same instant.
- **Machine-checked, at the write (CC-162a F5; Codex (a)):**
  - a GPU step whose timeout would end after `NOT_AFTER` − 2.0 h is HELD (`left` exit 4);
  - the job refuses to start the decide step at or after `NOT_AFTER` (`k2_gate1.py deadline`, exit 4);
  - `gate1_decide.py` is the single writer of `gate1_decide.json`, for both the decision and NOT-RUN (cost). It holds an exclusive lock (`flock` on `.gate1_decide.lock`) and refuses when the clock is at or past `NOT_AFTER`. It records `written_epoch` in the file, writes a fsynced temporary file, checks the clock again, and only then renames. A late or direct call, or a call that crosses the instant between the two checks, leaves no `gate1_decide.json`.
- If the second clock check fails at the rename, the verdict markdown (`STOP.md` or `GATE1_VERDICT.md`) that was just written is deleted, so no verdict outlives a refused decision (CC-162b G1).
- **What counts as a decision (external time anchor; Codex round 3):** only a `gate1_decide.json` that `gate1_decide.py check` accepts. Two conditions:
  1. it records a `written_epoch` before `NOT_AFTER`;
  2. its sha256 is the content of `manuscript/prereg/2026-10-28_k2_gate1/gate1_decide.sha256` in a commit on q2 `main` (local `paper-v10` is pushed to q2 `main`; checked on the fetched `refs/remotes/q2/main`). The **first** commit that ever wrote that file must name exactly this sha (one look: a second decision anchored later never counts);
  3. **GitHub's own receipt time** of a push to q2 `main` carrying that commit is before `NOT_AFTER`. A carrying push is one whose head is the anchor commit or a descendant of it in the fetched history. `check` reads it from the GitHub REST activity API (`repos/HoaNguyen55/vsps_image_captioning_q2/activity?ref=refs/heads/main&activity_type=push`), with the events API as the fallback, taking only the head sha and the server timestamp. Local commit times are ignored, because they can be backdated (Codex round 4).
- **If the GitHub API is unreachable:** `check` exits 4 (HELD) and decides nothing; it is rerun. This is fail-closed: no step that needs the decision (the cost-only amendment, `kv_freeze.py`, the scorer) can go on while it is HELD. The branch is fixed only by a reachable API answer. Branch K1+K6 binds when that answer shows no carrying push received before `NOT_AFTER`; an outage alone never binds a branch. The operator still logs the push output line, as a record only.
- **Re-run (round 6):** `gate1_decide.json` records the sha of every input (`decode_sha256`, the five val decodes plus the bf16 row). `check` re-reads those inputs, requires the same shas, re-runs the decision, and requires identical verdict, failed gates, gate results, deltas and rates. A hand-edited verdict is refused, and so are inputs that cannot be re-read (selftested). A NOT-RUN (cost) record has no inputs and is not re-run.
- A file with a plausible but forged `written_epoch` and no such anchored and pushed commit is no decision. The branch rule (A2), `kv_freeze.py` and the MT4 scorer read the decision only through `check`.
- Without an anchored commit whose push GitHub received before `NOT_AFTER`, there is no decision: the NOT-RUN (cost) path of A2, Branch K1+K6.
- So no decision can exist at or after `NOT_AFTER`. A Gate 1 run still in progress at that instant ends with no decision.
- **Feasibility (Codex review; CC-162 W2):** P50 keeps 7 models (14 full runs); 10 of 14 full runs were done at 10-29 03:25Z, 2.26 GPU-h used including 0.27 h of smoke, and its worst-case decode end is about 07:30Z on 10-29 (CC-162a ruling 5). Gate 1 needs about 19.1 GPU-h of projected work after the reused steps. Even if P50 used its full cap, about 11 days remain.

## A2. §0, replacement of row 3

Old row 3 (l.21):

> | INCONCLUSIVE, NOT-RUN (cost), or no `gate1_decide.json` by the freeze date | **Branch K1+K6** by default; the PI may rule before the freeze that K2 enters KV as a descriptive arm with no H. Nothing else changes. A NOT-RUN (fault) is rerunnable (K2 Gate 1 RULE §7) and switches nothing by itself |

New row 3:

> | INCONCLUSIVE, NOT-RUN (cost), or no `gate1_decide.json` written before `NOT_AFTER` = 2026-11-10T12:00:00Z | **Branch K1+K6** by default; the PI may rule before the Branch K1+K6 freeze that K2 enters KV as a descriptive arm with no H. Nothing else changes. A NOT-RUN (fault) is rerunnable only before `NOT_AFTER` and switches nothing by itself. A host lost or a job killed inside a GPU step (an open ledger start) is a NOT-RUN (fault) **only after** that step has been charged its full logged timeout, min(stage cap, Gate 1 total left) (K2 Gate 1 RULE §6 as amended); if that charge leaves no Gate 1 total, the result is NOT-RUN (cost). Whether a run is still in progress at `NOT_AFTER` does not matter: no decision means Branch K1+K6 |

The table's rows are mutually exclusive and exhaustive:
- a GO that `check` accepts (written before `NOT_AFTER`) gives Branch K2;
- a NO-GO that `check` accepts gives Branch K1+K6;
- INCONCLUSIVE, NOT-RUN (cost), or no decision before `NOT_AFTER` gives Branch K1+K6.

A NOT-RUN (fault) is not a decision. If it is not followed by a decision before `NOT_AFTER`, it falls into the last case.

## A3. §2, replacement of the freeze bullets (l.39–40) for Branch K2

Old: "**Freeze, about 11-18 (VN).** … The gatekeeper's commit of `KV_PRED_SUMS` with the shas of the KV gold, `kv4224.txt` and the scoring code is the freeze." and "**A system not in `KV_PRED_SUMS` at the freeze loses confirmatory status** …".

New, for Branch K2:

> **Freeze (Branch K2).**
> - Each KV prediction file is sha256-hashed when its decoder finishes. Its line `SHA  FILE  UTC` is appended to `KV_PRED_SUMS` (fsync). UTC is the append time, written by the decode job, never by hand. No one opens a KV prediction (unchanged).
> - The **kept set** is the list of systems and seeds that the committed cost-only amendment keeps (§8 and A4). It lives in **`manuscript/prereg/2026-10-28_mt4_kv/kv_kept.json`**, committed with that amendment and pinned in `mt4_kv/SHA256SUMS`. `kv_freeze.py` reads it only from HEAD and only if its sha matches the pin committed at HEAD. It refuses any other kept set, and any set that drops an H system or seed (base_s; K seeds 1–3; U seeds 1–3; never cut, §8). No caller-supplied set is accepted (Codex round 4).
> - The **freeze instant** is fixed by the log, not by a commit (CC-162a F2): **min(UTC of the first `KV_PRED_SUMS` line that completes the kept set + 24 h, D)**, with **D = 2026-11-30T12:00:00Z**. The gatekeeper's commit of `KV_PRED_SUMS` (with the shas of the KV gold, `kv4224.txt` and the scoring code) only records the frozen set; its time decides nothing.
> - **No early or partial freeze (Codex (b)):** the gatekeeper may not commit `KV_PRED_SUMS` before D unless every kept system and seed has its line. A commit with an incomplete kept set before D is void; the freeze is then at D. The check is mechanical: the commit script compares the lines with the kept set and refuses a short list before D.
> - The **frozen set** is every `KV_PRED_SUMS` line whose UTC is at or before the freeze instant. At D, exactly the lines up to D are committed. A line appended after the instant is post-freeze and descriptive.
> - **Duplicate lines (CC-162a F2; Codex round 4):** the first line per system and seed counts. A later line for the same system and seed with the **same** sha is descriptive. A later line with **another** sha (a re-decode) halts the freeze: FAULT → PI, nonzero exit, no frozen output.
> - Neither the gatekeeper nor anyone else can widen or shrink the frozen set by choosing when to commit. The set is fixed by the logged UTC, by the kept set, and by D, which is fixed now.
> - **Lines outside the kept set** (any system or seed the cost-only amendment did not keep) are descriptive, even when appended before the instant (CC-162b G2).
> - **Tool (CC-160 W9; Codex round 3):** `scripts/mt4_kv/kv_freeze.py` is the only writer (`append`, fsynced, the UTC set by the code) and the only validator (`freeze`) of `KV_PRED_SUMS`. The file sits at the one constant path `manuscript/prereg/2026-10-28_mt4_kv/KV_PRED_SUMS`; there is no path option (round 6). Every command first runs `gate1_decide.py check` and refuses unless the decision is an anchored GO. `freeze` applies, in code:
    - the first-line rule. A duplicate line with another sha for a kept system and seed **halts the freeze** (FAULT → PI, nonzero exit, no output; Codex round 4). Lines whose UTC is out of order, or earlier than the decision's push receipt, also halt it;
>   - the outside-kept rule;
>   - completion, the instant min(completion + 24 h, D), and the refusal before the instant (no early or partial freeze);
>   - the H NOT-RUN status for a missing seed.
>
>   The gatekeeper commits `KV_PRED_SUMS` with `freeze.json`, never a hand-made set. `kv_freeze.py --selftest` covers each rule; its sha is pinned in `mt4_kv/SHA256SUMS`. A one-judge code read is required before any KV staging (CC-162b G3).
> - A system not in the frozen set loses confirmatory status (PI-1026av Q2).
> - If any registered seed of a system an H uses is missing from the frozen set, that H is NOT-RUN and the fixed sequence stops there. An H is never scored with fewer seeds than registered (unchanged).
> - Scoring, the one look, and the fault rule are unchanged (§2 l.41–42).

Branch K1+K6 keeps its own freeze rule (§5 l.96, §8 l.145): set by the cost-only amendment, before any K1 training, never after any KV prediction. This amendment does not change it.

## A4. §8, a mechanical cost test for Branch K2 against D

Added after the cost ladder and its H-systems sentence (l.144). It is applied by the cost-only amendment, which is committed before the first confirmatory training step as today.

> **Branch K2 deadline test.**
> - Let t₀ = the `written_epoch` of the GO in `gate1_decide.json` + 24 h. It is fixed by the file, not by when the amendment is written.
> - **Exact inputs (CC-162a F3)**, all written before the cost-only amendment, none of them a KV output:
>   - decode rate r_dec = **the maximum `s_per_image_decode` over the five val-924 provenance records** (`k2g1_{base_s,unedited,gold,det,ref}.preds.json`);
>   - training rate r_tr = **the maximum over the four Gate 1 training stages (train_unedited, train_gold, train_det, train_ref) of the ledger seconds of the attempt that wrote the stage's `.done`, divided by that stage's examples** (2 × `examples_per_epoch` from `targets.json.counts.json`). For train_det, that is the M1 rerun, not the 6,120 s charge of the lost attempt.
>   - projections, as in §8: a training seed = 2 × 2,392 (its arm's examples per epoch) × r_tr / 3600 + 0.1 GPU-h; a KV decode = 4,224 × r_dec / 3600 + 0.1 GPU-h; cap = ceil(1.2 × projection) to 0.1 GPU-h.
> - Let C_H = the sum of those caps over the H systems only:
>   - training: K × 3 and U × 3, the confirmatory seeds;
>   - KV decodes: base_s, K × 3 and U × 3;
>   - plus 2.0 h of KV staging and cleanup.
> - Everything runs on the one m3-role GPU.
> - If t₀ + C_H > D, **Branch K2 is NOT-RUN (cost) and Branch K1+K6 binds**, with its own freeze set by the cost-only amendment under §5. Otherwise Branch K2 proceeds and the ladder is applied to the other systems as today.
> - The test uses no KV output and no operator or PI choice. Its inputs are the GO's `written_epoch`, the two maxima above, and the fixed caps formula. `kv_freeze.py costtest` computes it (after `check`), and its output file is committed with the cost-only amendment.

This decides the branch. It may therefore not be changed by the cost-only amendment (l.145, unchanged).

## A5. §2 and §9: "M3" means the m3 role

- In §2 l.43 ("KV images are staged and decoded on M3 only") and l.44 ("runs on M3, the test-capable machine"), and in §9 l.149 ("K2 Gate 1 (M3, before 11-06 12:00Z)"), "M3" reads as **the m3 role**: the machine whose `/root/.vsps_machine_id` is `m3`, now M1 (PI-1029d, CC-155 W1). M4 and the m4 role (M2) still run no KV step.
- §9 calendar, replaced, with every other date unchanged:
  1. K2 Gate 1 (m3 role) before `NOT_AFTER` 2026-11-10T12:00Z;
  2. the cost-only amendment;
  3. confirmatory training;
  4. the Branch K2 freeze at min(the UTC of the line that completes the kept set + 24 h, D 2026-11-30T12:00Z) (Branch K1+K6: the date set in the cost-only amendment);
  5. scoring;
  6. MT4 writing after B freezes (11-30) and A freezes (12-18, SPIC; CC-142 ruling 5);
  7. IP&M 01–02/2027.

## A6. K2 Gate 1 RULE §6–§7, the ledger rule this amendment relies on (text in Amendment 2 §2)

- Every GPU step logs `NAME start EPOCH TIMEOUT`, with TIMEOUT = min(stage cap, Gate 1 total left). The line is written, flushed and fsynced (file and directory) before the step starts (`k2_gate1.py ledger`; Codex (c)).
- **Every attempt starts from zero (CC-162a F1):** before a GPU step without a matching `.done`, the job deletes that step's decode partial (`k2_gate1.py fresh`) and logs it. A step that needs more than its cap therefore ends in exit 124, which is NOT-RUN (cost), however often it is killed or its host is lost. Training already has no resume.
- **Charges (CC-162a ruling 4):**
  - an open start (no end line: host lost, job killed) is charged its full TIMEOUT, whatever the clock;
  - a step whose child exits with a code (a crash, a kill of the child) is charged its measured seconds, as RULE §7 already says. With every retry starting from zero, a full charge would add no protection.
- `left` appends the charge for an open start and exits 6 (NOT-RUN (fault), rerunnable) before any retry.
- A retry gets only the total that remains. If the total is spent, `left` returns 0 and the job writes NOT-RUN (cost).
- A legacy open start without a logged timeout is closed only by a committed amendment; the single M3 line is closed at its determined timeout of 6,120 s (Amendment 2 §2).

**Selftest asserts:**
- `k2_gate1.py` `ledger_selftest`:
  - a start line is fsynced twice (file and directory);
  - a killed child's measured seconds (42 s) are charged as written;
  - an open start's charge is the same at any clock (1,600 s at now = 5,001 and at now = 10⁹);
  - two losses in one step cost 1,000 + 2 × 600 s, and each rerun is allowed only after the charge;
  - a charge that spends the 36 h total gives `left` = 0, the cost stop;
  - a legacy open start is refused with no ledger write.
- `k2_gate1.py` `kill_rerun_selftest`, with the real `decode_hf_vlm.decode_slices`: a step needing 5 slices under a cap of 3 is killed after 2. Without `fresh` the retry finishes it, which is the loophole the test proves exists. With `fresh` the retry hits its cap.
- `gate1_decide.py` `deadline_selftest` and `anchor_selftest`:
  - a late direct `decide` or cost `notrun` call writes nothing;
  - a clock that crosses `NOT_AFTER` between the lock check and the rename leaves no file;
  - a second writer is locked out;
  - `check` refuses a record with a late or missing `written_epoch`;
  - the race test also asserts that the verdict markdown is removed (G1);
  - in a temporary repository with a local bare remote:
    - a decision committed and pushed before `NOT_AFTER` is accepted;
    - a forged earlier-timestamped decision with no anchored commit is refused;
    - an anchor committed after `NOT_AFTER` is refused;
    - an unpushed anchor is refused.
- `kv_freeze.py --selftest`:
  - the first line per system and seed counts;
  - a same-sha repeat is descriptive and a different-sha repeat is a fault;
  - lines outside the kept set are descriptive;
  - the instant is completion + 24 h, or D when that comes later;
  - no freeze before the instant, and no partial freeze before D;
  - at D with a seed missing, the H is NOT-RUN;
  - the cost test falls on both sides of D;
  - `rates()` uses the det rerun, not the lost attempt;
  - an unanchored decision is refused before anything else.
- The job selftest fails if any of the three decode steps lacks its `fresh` partial.

A retry therefore cannot reduce the charged cost, and cannot finish a step that its cap would have stopped.

## A7. What this amendment does not change

It leaves these unchanged:
- every H, threshold, SESOI, matcher, gold and test set;
- the fixed sequence, the seed counts, pooling and the bootstrap;
- the one look;
- the K1+K6 freeze rule;
- the English arm;
- the budget lines (dev 40, test 100, English 30);
- the cost ladder order.

## A8. For the reader (Codex and the one judge)

- Confirm the A2 rows are exhaustive and that A2–A4 leave no discretionary step after a GO is known. The freeze instant comes from the log and D, and the A4 inputs are two named maxima and fixed formulas.
- Confirm that D (11-30T12:00Z) does not move any H and only fixes when the existing missing-seed rule applies.
- Confirm the commit order: this file, then Amendment 2 (and 2a if needed), then setup `WITH_K2=1`, then the restore. All of it comes before any Gate 1 val decode.
