# CONFIRMATION MAP, Amendment 5b

**Status.** Drafted by the N-M3 fill writer, 2026-10-21, under the judge's CC-076 (YES 93%,
`.session_backup/2026-10-13/decisions/CC-076.txt`) and CC-077 (93%). It is committed by the gatekeeper together with
the result file `data/results/n_m3/caphit_result.json` (sha256
`72404c620e83a46d932c13e42a8ac6d8240e756c6ab702e5b59d6e3aca56459f`) and the fill.

**Scope.** A wording correction made after the run:
- the new-clause text of amendment 5 rows 33 and 34 is replaced by the text in §2;
- one row is added, row 35 (CC-077): the §7.6 eight-LVLM clause that the fill makes false;
- no number, fill rule, rounding rule, verdict, verdict rule, selection logic, precondition or registered outcome
  changes;
- the row 33-34 fallbacks are unchanged (and unused: the structural gate passed);
- it supersedes `amendment_5.status` ("measurement NOT RUN") in `CONFIRMATION_MAP.json`, which is left as written.

The number stays POST_HOC and descriptive, and supports no causal claim about qwen3vl_8b's A-N2 failure.

**Timing.** Written after the single run (2026-10-21T15:50:31Z) and after the independent verifier re-run passed
(326 of 326 fields).

## 1. Why the registered fill is not used verbatim
- **{p} = 100 under the registered rule.** The pooled share is 3,367 of 3,378 = 0.99674
  (`pooled_9_ladder_detailed.counts.{hits_recorded,n}`). Rounded half up to an integer, as amendment 5 §2 fixes, it
  is 100. The run printed `p` = 100 and `filled_clauses` with "100% of which reached the cap".
- **Read literally, "100%" is false.** 11 of the 3,378 captions did not reach the cap: uv231 683 of 693 (runs 228,
  228 and 227 of 231) and xm600 1,799 of 1,800 (`per_set_pooled.*.counts`). Amendment 5 §3 exists to remove a false
  clause; filling {p} verbatim would put a new one in the same place.
- **The correction.** The text gives the count and one decimal (99.7%) instead of the integer that rounds up to
  "all". Why this is allowed after the run (CC-076):
  - it changes no number and no rule: it is the same registered quantity, the pooled recorded-hit share, stated more
    precisely;
  - it is weaker than the pre-fixed text (99.7% against 100%), so it favours no claim.
- 99.7 is 100 × 0.99674 to one decimal; it is not a rounding tie, so the rounding mode does not matter.
- **The result file is committed unchanged**, with its `filled_clauses` as computed. The text differs from
  `filled_clauses` only as §2 states.

## 2. Rows

| # | Block / outcome | Old clause | Amendment 5 new clause, filled ({p} = 100) | Amendment 5b clause (in the text) | Verdict | Strength |
|---|---|---|---|---|---|---|
| 33 | §7.6 design paragraph (sec7_verbosity_sign.md) | as amendment 5 | "detailed captions capped at 160 new tokens, 100% of which reached the cap by the recorded token counts, Supplementary S7; the same cap as in the eight-LVLM test below" | "detailed captions capped at 160 new tokens, 3,367 of 3,378 [99.7%] of which reached the cap by the recorded token counts, Supplementary S7; the same cap as in the eight-LVLM test below" | none (descriptive, POST_HOC) | weaker than the pre-fixed fill; still corrects the false clause (amendment 5 §3) |
| 34 | §10.5 conclusion c3 (sec10_discussion.md) | as amendment 5 | "(Qwen3-VL-8B; detailed captions capped at 160 new tokens, 100% of which reached the cap, Supplementary S7)" | "(Qwen3-VL-8B; detailed captions capped at 160 new tokens, 99.7% of which reached the cap, Supplementary S7)" | none (descriptive, POST_HOC) | weaker than the pre-fixed fill |
| 35 | §7.6 eight-LVLM paragraph (sec7_verbosity_sign.md) | "; in the second-backbone runs the share is unknown" (amendment 4, CP-064) | none (not in amendment 5) | "; in the second-backbone runs, 3,367 of 3,378 Vietnamese detailed captions (99.7%) reached it (Supplementary S7)" | none (descriptive, POST_HOC) | same quantity as row 33; replaces a clause the fill makes false |

- **Row 33 tail.** It keeps "; the same cap as in the eight-LVLM test below". `filled_clauses.sec7_6` lacks the
  tail; DESIGN.md says the clause is "followed by" it (verifier note 1).
- **Row 33 brackets (CC-077).** The share is written "[99.7%]", in square brackets, because the clause sits inside
  §7.6's existing parenthesis "(three temperatures × a short and a detailed Vietnamese prompt; …)". This keeps
  CC-073b's no-nesting rule. The change from CC-076's "(99.7%)" is typographic only: no word or number changes.
- **Row 34** gives the share only, with no count (CC-076).
- **Row 35 (CC-077).** After the fill, the old clause is false: the share is known. It is replaced, not deleted,
  because deleting it would break the symmetric cap fact PD-28 requires: the eight-LVLM paragraph states the cap
  share of both harnesses.

## 3. Supplementary S7
Filled per amendment 5 §2, in one paragraph and Table S7.4 (supplementary.md):
- per-run, per-set and pooled counts of captions, recorded hits and re-tokenization agreement (the per-run and
  per-set shares are given as counts out of n);
- the two `detailed_en` runs, not pooled;
- the validation facts: A-N2 526 of 526, agreement 526 of 526; B-N1 787 of 789, agreement 788 of 789, the miss at
  159 recorded tokens. CC-077 accepts the B-N1 counts as validation facts. The S7 source comment cites
  `data/results/b_n1/b_n1_run.json` (sha256 `adad454d`) ::
  `LBB-D2.lbB_qwen3vl_8b_{ktvic_test,uitviic_test}-detailed.hit_max_share` and the matching `inputs_sha256` entries;
- the upper-bound caveat (an EOS exactly at token 160 also gives n_tokens = 160).

Every printed number has a `number_manifest.tsv` row keyed to `caphit_result.json` (`keyed (POST_HOC, 72404c62)`),
except 159, keyed to DESIGN.md line 73.

## 4. Verification record
- The independent verifier re-run passed: 326 of 326 fields match the result file.
- Its record is copied byte-identical from the git-excluded `.session_backup/2026-10-21/n_m3_verify/` to
  `manuscript/prereg/2026-10-21_n_m3_caphit/`, so the record's "in this folder" holds there (CC-077):
  - `VERIFY.md`, sha256 `705d656729564a3b09e86fcd58f6e2b2f93d464628803e7a45a23b180070dc8c`;
  - `verify_caphit.py`, sha256 `9de08f06740324627ef23d5dfb4792c059e53caf968d219d35f95f416fda80e2`;
  - `verify_out.json`, sha256 `a74c528d7bebc8d907e652b591177b624666745fb2cf7eeda9638ec7227c9151`.
- A scan found no session paths and no usernames in the three files. The only absolute path is the repo root in the
  usage line of `verify_caphit.py`.
- The "fill blocker" at the top of the record is the issue this amendment resolves.

## 5. Coverage
- Every clause in the text that states the second backbone's cap share is now covered: rows 33 and 35 in §7.6, row 34
  in §10.5 c3. No clause saying the share is "not recorded" or "unknown" remains.
