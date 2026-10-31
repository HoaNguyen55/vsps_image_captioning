# Judge read request v3: MT4 PREREG AMENDMENT_2 after CC-205 and the Codex read (one-judge read, W2)

**Status.** CC-205 (3/3, GO-with-fixes, 92) ruled on the content. This v2 applies W3, W4, W5, W5b, W6, W7, W8, W9 and
W12 to the draft and the diff.
- Not done here, by instruction: W10 (another agent fetches the 4B snapshot).
- W1 (PI YES) is met by **PI-1031e** (LOG l.986), which answers CC-205 Q1–Q5. The draft cites it in its Status block,
  next to the CC-188 l.83 / W4 overrule (CC-205 r6, PI-1031b).
- W11 is written as binding text (A6), as ruling 9 requires.
- v3 applies the Codex read (`manuscript/reviews/MT4_AMEND2_codex_read.md`, 55): blocking items 1 and 2 and
  non-blocking item 3. Item 4 needed no change.
- Nothing committed. M1 untouched.

**Asked of:** one judge (CC-205 W2; the Codex read is done; a Codex re-read of items 1–3 is optional). The question is whether the revised text and the full
diff meet W3–W12, so that the gatekeeper may commit. The PI's YES is already logged as PI-1031e (W1).

## Old → new shas

| File | v1 (CC-205) | v2 (Codex read) | v3 (this read) |
|---|---|---|---|
| `AMENDMENT_2_DRAFT.md` | 81b1060a… | 85a9acdc… | 161288f3ce68a18eecdc0453624185e5ea1ddb73a634d3f34edb703176d9c64d |
| `AMENDMENT_2_k1k6.diff` | 35771a25… | 6e53bdc9… | 937fddeb86ffd4cb4ee94cf088f28f2edb473f3a050f49792dd774fea2abf8a2 |
| `k1k6.py` after the diff (base f2273b90) | ec959982… | 5c5766ca… | 7dbca3c4d4bbe39f0e07bbb9b7f0d7de738f4d4d6875bb6dc0933e17e8569534 |
| `scripts/mt4_k1k6/SHA256SUMS` after the commit (simulated) | — | 7ed15bdb… | 64abce8cffee6af4549fe3973c652643e1c2b713a1d0b571c3c4cb06809569ba (k1k6.py → 7dbca3c4; job 27d2b431, w25k1_prep f465c2a6 unchanged) |
| `k1k6_job.sh` | 27d2b431 | 27d2b431 | 27d2b431 (unchanged) |

## Codex item → fix (v3)

| Codex item | Fix | Where |
|---|---|---|
| 1 BLOCKING: a cut of K1 seed 2 must stop the branch before tier-2 training | `cmd_left` prints 0 for every stage when `caps.json` `ladder_applied` holds "cut K1 seed 2". The frozen job's `[ "$t" -gt 0 ] \|\| cost` then writes `K1K6_COST.txt` before `train_k1_s1`, and l.49 closes the branch for later tiers. Selftest: with seed 2 cut → 0; with only K6 cut → a positive timeout. A mutation that disables the stop fails the selftest | A1 "K1 seed count"; Part B row; code |
| 2 BLOCKING: one look across failed scorer attempts | `kv_attempt` writes `kvscore_attempt.json` (O_EXCL, fsync: time, closure sha, frozen set) **before any KV gold or prediction read**. `kv_ready` refuses whenever it exists, for scoring and for decoding, so any later failure is terminal. Selftest: a simulated crash after the marker, then `kv_ready` and a second marker are both refused. A mutation that removes the refusal fails | A2 "One attempt"; Part B tier-3 row; code |
| 3: `closure()` raises FileNotFoundError on a missing file | SystemExit FAULT listing the missing files; selftest | A3; code |
| 4: seed-count text consistent | no change | — |

**One deviation for the judge.** The marker comes after `freeze_set` reads `KV_PRED_SUMS`, not before it as the
coordinator's literal wording asked. That file holds only shas, file names, system names and times; it holds no
prediction or gold content. Reading it first means a premature call (before the freeze instant) exits HELD and writes
no marker. If the marker came first, an operator who ran `SCORE=1` early would burn the one look on a HELD exit. The
marker still precedes every gold and prediction read. Alternative: marker first, so that HELD is terminal too. The
drafter rates that worse; the judge rules.

The two prereg-folder SUMS (`2026-10-30_mt4_k1k6`, `2026-10-28_mt4_kv`) gain their lines at the commit. They are not
pre-written here, because the final file names and shas are fixed only then (W4).

## Fix → where

| Fix | Draft | Code |
|---|---|---|
| W3 pointer `2026-10-28_mt4_kv/AMENDMENT_2_K1K6.md`; `AMENDMENT_COST_K1K6.md` byte-unchanged | Status item 5 | — |
| W4 all three SUMS in the commit set | Status item 5; Part C item 1 | — |
| W5 scorer closure | A1 anchor; A3 "Scorer closure"; Part B tier-3 table | `SCORER_CLOSURE`, `closure`, `closure_check`. `t2decide` writes `scorer_closure`. `kvscore` checks it right after `kv_ready`, before `KV_PRED_SUMS`, gold or any prediction is read. Selftest: equal / changed / missing / absent; a fresh-process probe asserts completeness (mutation test fails as expected) |
| W5b one-seed H-B1 is descriptive only → NOT-RUN (cost) | A1 "K1 seed count"; Part B row | — |
| W6 Part B rows (i)–(v), incl. whether KV is spent | Part B, three tables | — |
| W7 money and rental gate; PI-1031c exception | A6 row; A6 exception paragraph; Part C Money | — |
| W8 Q7 = (a); the exclusion/coco_test/nocaps check at the `kv4224.txt` commit; FAULT, not KeyError | A4 | `cmd_guard`: SystemExit FAULT on a missing record row |
| W9 v1 label, fixed after the dev numbers, never blocks v2 | A5 | `V1_LABEL`; `v1_safe` (records the exception type only) |
| W11 no AMEND2 on M1 before "tier 1 done" + `t1_select` + `caps.json` | A6 row; Part C item 0 | — |
| W12 `decoder_sha256` differs between tier 1 and tiers 2/3; `k1k6_lists.json` 5b73fb81 stays | A7 "Disclosures" | — |

## Checks run (laptop CPU, scratch copy; ids, shas and existing dev counts only)

- v3: `git apply --check` of the diff against HEAD: clean.
- `python3 k1k6.py --selftest`: ok.
- In a scratch tree with `SHA256SUMS` updated to 7dbca3c4, `bash k1k6_job.sh --selftest`: ok.
- Function bodies (AST) unchanged from f2273b90:
  - training and decoding: `cmd_train`, `cmd_decode`, `load`;
  - planning: `plan`, `t1_rule`;
  - pool: `pool_rows`, `drop_trunc`, `example_plan`;
  - gold and scoring: `cmd_gold`, `prf`, `chair`, `pool_seeds`;
  - rules and freeze: `hyp`, `p_pass`, `t2_rule`, `freeze_set`, `cmd_kvsums`.
- Changed: `cmd_stage`, `scan_k1`, `cmd_guard`, `short_counts`, `detailed_counts`, `load_set`, `cmd_t2decide`,
  `cmd_kvscore`, `cmd_left` and `kv_ready` (both new in v3), `selftest`. Added in v3: `kv_attempt`.
- On the two val-924 planning prediction files (47f3e0ba, 6120c566), the old and new v2 counts and `hyp()` are
  identical.
- The C-EN mirror records hold T2 2,000 of 2,000 rows (553fb604) and Karpathy val 5,000 of 5,000 rows (8c93f306).
- 8-gram/6-gram scan: 0 on all three files. No host, e-mail or token.

## Points for the readers

1. **Closure scope.** The closure covers repo files only. Python and numpy are not pinned in code: A3 asks for a
   logged `pip freeze` sha of M1's `/root/vsps/.venv` at `t2decide` and at `kvscore`. Is that enough, or should the
   interpreter freeze be part of `scorer_closure`?
2. **Shared modules.** The closure includes the shared `grl/` and `rescap/` modules. An edit by another study between
   the A3 commit and the look forces a FAULT and a new ruling. A3 says so. Confirm this is acceptable.
3. **Spent rule.** KV counts as **spent** from the first `kvsums` line. A fault before that line leaves KV unspent,
   but a re-stage needs a one-judge ruling (Part B, W6 v). Confirm that boundary.
4. **T1_FAIL logging.** The frozen job logs "tier 1 done" even on T1_FAIL, because `plan` exits 1, not 2. The draft
   does not change the job; the record of truth is the `t1_select.json` verdict and the missing `caps.json`, plus the
   operator's OPS line (W6 i).

## PI answers (CC-205 Q1–Q5)

All five are YES in PI-1031e ("Đồng ý cả 5"); the draft cites it at Status item 1, A1, A6 and Part C. The A6
money/rental gate is still checked by the gatekeeper against the logged balance and rental end before each launch.
