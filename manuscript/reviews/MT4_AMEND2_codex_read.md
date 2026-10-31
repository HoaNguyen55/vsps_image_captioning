# CC-205 W2 — AMENDMENT_2 external read

**Readiness: 55/100 — not ready to commit.** No KV gold or prediction read occurs before the proposed `closure_check`; `kv_ready` first reads only the anchored T2 decision record (`manuscript/prereg/2026-10-30_mt4_k1k6/AMENDMENT_2_k1k6.diff`:229–235; `scripts/mt4_k1k6/k1k6.py`:910–927).

1. **BLOCKING —** The amendment says that when the ladder cuts K1 seed 2 (after the K6 cut), no confirmatory training occurs and the branch becomes NOT-RUN (cost) (`manuscript/prereg/2026-10-30_mt4_k1k6/AMENDMENT_2_DRAFT.md`:107–110, 274). But the tier-2 job attempts K1 seed 1 and K6 training; `step` skips individually cut stages, so K1 seed 1 can train in this case (`scripts/mt4_k1k6/k1k6_job.sh`:75–85, 137–142). Add a pre-training branch stop when `caps.json` cuts K1 seed 2.

2. **BLOCKING —** The one-look rule is not enforced across failed or incomplete scorer attempts. `kv_ready` refuses only if `mt4_k1k6_decide.json` already exists (`scripts/mt4_k1k6/k1k6.py`:925–927); `cmd_kvscore` reads sums, gold and predictions before its final O_EXCL write (`manuscript/prereg/2026-10-30_mt4_k1k6/AMENDMENT_2_k1k6.diff`:229–254). An interruption or exception after a read but before that write leaves no marker, so a second invocation can read/score again. Record an irreversible attempt before any KV read, or make every post-read failure terminal and unrerunnable.

3. **NON-BLOCKING —** The closure comparison is before the KV sums, gold and prediction reads, and its listed matcher/data dependencies appear to cover the scorer’s imported repo modules (`manuscript/prereg/2026-10-30_mt4_k1k6/AMENDMENT_2_k1k6.diff`:7–14, 229–235; `manuscript/prereg/2026-10-30_mt4_k1k6/AMENDMENT_2_DRAFT.md`:179–196). Actual missing closure files raise raw `FileNotFoundError` in `closure()` rather than the specified FAULT path (`manuscript/prereg/2026-10-30_mt4_k1k6/AMENDMENT_2_k1k6.diff`:200–208); it fails closed, but align the error handling with the text.

4. **NON-BLOCKING —** Seed-count handling is consistent with the majority ruling: a cut K1 seed 2 makes H-B1 descriptive and prevents a confirmatory KV look (`manuscript/prereg/2026-10-30_mt4_k1k6/AMENDMENT_2_DRAFT.md`:107–112, 274), matching PREREG’s “never tested with fewer seeds” and ban on changing an H system’s seed count (`manuscript/prereg/2026-10-28_mt4_kv/PREREG.md`:40, 144–145) and CC-205 ruling 3 (`.session_backup/2026-10-13/decisions/CC-205.txt`:39–40). Finding 1’s operational stop is still needed to make this rule executable.

## Re-read after fixes

**Readiness: 92/100 — targeted blockers resolved; ready for the requested judge read.** Verified revised file hashes match the v3 request (`manuscript/prereg/2026-10-30_mt4_k1k6/JUDGE_READ_REQUEST_AMEND2.md`:20–23).

1. **RESOLVED —** `cmd_left` returns 0 if `ladder_applied` cuts K1 seed 2, triggering the frozen job’s cost stop before training; the seed-2-only selftest checks this (`AMENDMENT_2_k1k6.diff`:126–139, 389–402; `scripts/mt4_k1k6/k1k6_job.sh`:81–89).
2. **RESOLVED —** `kvscore_attempt.json` is O_EXCL/fsynced and `kv_ready` refuses it on subsequent decode/scoring calls; it precedes KV gold and prediction reads (`AMENDMENT_2_k1k6.diff`:241–259, 269–279). Reading `KV_PRED_SUMS` first is acceptable: it contains hash/name/system/time metadata only, closure is checked first, and pre-freeze exits HELD without creating the marker (`AMENDMENT_2_DRAFT.md`:161–172; diff:269–277). The selftest covers terminal refusal after a simulated crash (diff:365–376).
3. **RESOLVED —** A missing closure file now raises `SystemExit` with a FAULT before `KV_PRED_SUMS`, gold or prediction reads; the selftest covers it (`AMENDMENT_2_k1k6.diff`:214–224, 383–388). No new blocking issue found in the requested scope.
