# N-M3 cap-hit: independent verifier re-run (2026-10-21)

> **Fill blocker, judge ruling needed:** the pre-fixed fill gives "100% of which reached the cap", but 11 of 3378 captions did not reach it (3367/3378 = 99.67%). Per set, uv231 is 683/693 = 98.6%, with per-run hits of 228, 228 and 227 of 231. Rounding half up is applied correctly, but the sentence read literally is false, and amendment 5 §3 exists to remove a false clause. This does not affect the verification PASS. It blocks the fill CP as written until the judge rules.

**Verdict: PASS.** 326 of 326 fields match `data/results/n_m3/caphit_result.json` (sha256 `72404c620e83a46d932c13e42a8ac6d8240e756c6ab702e5b59d6e3aca56459f`). No mismatches.

## Method
- Script: `verify_caphit.py` (copy in this folder), sha256 `9de08f06740324627ef23d5dfb4792c059e53caf968d219d35f95f416fda80e2`. It is written independently and does not import `scripts/n_m3/caphit.py`. Output: `verify_out.json` (sha256 `a74c528d7bebc8d907e652b591177b624666745fb2cf7eeda9638ec7227c9151`), counts only.
- Interpreter: scratchpad `venv_lb` (transformers 4.57.6, tokenizers 0.22.2, asserted), run with `-I -B`, `HF_HUB_OFFLINE=1`.
- Tokenizer: `.session_backup/2026-10-21/n_m3_tokenizer/`, `local_files_only=True`. Class `Qwen2TokenizerFast`. All 5 files equal C8_backbone `SHA256SUMS`.
- Inputs: each of the 11 G2-B preds files was sha-checked against `precheck.json` `runs.<run_id>.sha256` (`file` and `run_id` also checked). The 4 A-N2/B-N1 validation files were checked against `a_n2_run.json`/`b_n1_run.json` `inputs_sha256`. All pass.
- The result's `script_sha256` (`d01e6a67…`) and `design_sha256` (`05210c63…`) equal the HEAD blobs and the working-tree files.

- **First run:** script sha `ecfdcd448484b0554290453ff9ba78c39ba9bba1153fd85868c8f6c2c3733da8` returned FAIL with 4 mismatches. All 4 were `validation[i].file`, a path key my dict did not emit; every number matched. Fix: emit `file` and also compare the per-run shares. The second run (sha above) gave 326/326. The first `verify_out.json` was overwritten.
- **Extra checks:** `gate.pass` is true. The single B-N1 miss is in uitviic_test, with n_tokens = 159 and re-tokenized length ≥ 158, as DESIGN.md states.

## What was compared
- Gate: structure for each of the 9 runs.
- Per run (9 LADDER + 2 `detailed_en`): structure, counts and shares.
- Per set: pooled counts and shares.
- Pooled over the 9 runs: counts and shares.
- `p` and `filled_clauses`.
- `validation_facts` [0..3].

## Key numbers (recomputed)
| Scope | n | hits (n_tokens ≥ 160) | retok ≥155 / ≥158 / ≥160 | ≥158 agrees with hit | no final punct |
|---|---|---|---|---|---|
| cv295 (3 runs) | 885 | 885 | 885 / 885 / 877 | 885 | 856 |
| uv231 (3 runs) | 693 | 683 | 687 / 686 / 677 | 690 | 659 |
| xm600 (3 runs) | 1800 | 1799 | 1799 / 1799 / 1784 | 1800 | 1760 |
| **Pooled 9** | **3378** | **3367** (99.674%) | 3371 / 3370 / 3338 | 3375 (99.91%) | 3275 (96.95%) |
| cv295 detailed_en T0 (S7) | 295 | 295 | 295 / 295 / 293 | 295 | 284 |
| uv231 detailed_en T0 (S7) | 231 | 231 | 231 / 231 / 227 | 231 | 224 |

- Per-run hits:
  - cv295 T0/T05/T08: 295/295/295 of 295.
  - uv231: 228/228/227 of 231.
  - xm600: 599/600/600 of 600.
- **p = 100.** 3367/3378 = 99.674% rounds half up to 100. Integer check: (200·3367 + 3378) // 6756 = 100.
- Validation facts reproduced:
  - A-N2: 295 + 231 = 526 recorded hits; agreement at ≥158 is 526/526; drift in [−1, 0].
  - B-N1: 558 + 229 = 787/789 hits; agreement at ≥158 is 788/789; drift in [−2, 0].
  - `hit_max == (n_tokens ≥ 160)` holds in all 4 files.

## Clause selected
Amendment 5 pre-fixed these new clauses verbatim:
- Row 33: "detailed captions capped at 160 new tokens, {p}% of which reached the cap by the recorded token counts, Supplementary S7; the same cap as in the eight-LVLM test below"
- Row 34: "(Qwen3-VL-8B; detailed captions capped at 160 new tokens, {p}% of which reached the cap, Supplementary S7)"

The gate passed (9/9 runs, all 4 checks), so amendment 5 takes the **new clauses**, not the fallbacks. With {p} = 100:
- Row 33 (§7.6, `manuscript/journal_draft/sec7_verbosity_sign.md`): "detailed captions capped at 160 new tokens, 100% of which reached the cap by the recorded token counts, Supplementary S7; the same cap as in the eight-LVLM test below"
- Row 34 (§10.5 c3, `manuscript/journal_draft/sec10_discussion.md`): "(Qwen3-VL-8B; detailed captions capped at 160 new tokens, 100% of which reached the cap, Supplementary S7)"

The old clauses are still present in both files, one occurrence each.

## Notes for the judge (not discrepancies)
1. `filled_clauses.sec7_6` in the result does not contain the "; the same cap as in the eight-LVLM test below" tail. That matches DESIGN.md, which says the clause is "followed by" that tail. The fill CP must append it to match row 33's new clause verbatim.
2. "100%": see the fill blocker at the top.
3. Upper bound (R1): the recorded hit and re-tokenized ≥158 disagree on 3 of 3378 captions, all in uv231 (T05: 2, T08: 1).
