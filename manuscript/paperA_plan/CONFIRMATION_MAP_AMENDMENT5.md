# CONFIRMATION MAP, Amendment 5

**Status.** Drafted by the N-M3 verifier, 2026-10-21, under PD-30, and revised per the judge's CC-073 (YES 91%). It is
committed by the gatekeeper together with the N-M3 design (`manuscript/prereg/2026-10-21_n_m3_caphit/DESIGN.md`)
and `scripts/n_m3/caphit.py`, before the measurement runs.

**Scope.** Documentation only (PD-30):
- two rows, 33 and 34, one clause each, for §7.6 and §10.5 c3;
- the correction of a false clause (§3);
- no abstract row;
- no verdict, verdict rule, selection logic, precondition or registered outcome changes.

The number is POST_HOC and descriptive, and supports no causal claim about qwen3vl_8b's A-N2 failure.

**Timing.** Written before any share was computed from the G2-B `n_tokens` field (DESIGN.md states the state).

## 1. Rows

| # | Block / outcome | Old clause (current text) | New clause | Fallback (structural gate fails) | Verdict | Strength |
|---|---|---|---|---|---|---|
| 33 | §7.6 design paragraph (sec7_verbosity_sign.md) | "detailed captions capped at 160 new tokens, the same cap as in the eight-LVLM test below; how many of them reached it was not recorded" | "detailed captions capped at 160 new tokens, {p}% of which reached the cap by the recorded token counts, Supplementary S7; the same cap as in the eight-LVLM test below" | "detailed captions capped at 160 new tokens; cap share: Supplementary S7; the same cap as in the eight-LVLM test below" | none (descriptive, POST_HOC) | same; corrects a false clause (§3) |
| 34 | §10.5 conclusion c3 (sec10_discussion.md) | "(Qwen3-VL-8B, detailed captions capped at 160 new tokens; how many reached the cap is unknown)" | "(Qwen3-VL-8B; detailed captions capped at 160 new tokens, {p}% of which reached the cap, Supplementary S7)" | "(Qwen3-VL-8B; detailed captions capped at 160 new tokens; cap share: Supplementary S7)" | none (descriptive, POST_HOC) | same |

- The row 34 fallback adapts CC-073's fallback phrase, "detailed captions capped at 160 new tokens (cap share:
  Supplementary S7)", to avoid a nested parenthesis inside the c3 parenthesis. This is for the judge to check.
- Row 33 sits inside §7.6's existing parenthesis "(three temperatures × a short and a detailed Vietnamese prompt;
  …)", so its new clause and its fallback use semicolons, with no nesting (CC-073b).

## 2. Fill rule
- **{p}:** the pooled share of the 9 G2-B LADDER detailed runs (`g2b_q3_{cv295,uv231,xm600}-detailed-T{0,05,08}`,
  every image) whose decoder-recorded `n_tokens` is ≥ 160, the registered `max_new_tokens`, in percent.
  - It is rounded half up to an integer, exactly from the counts.
  - It is printed by the single verified `caphit.py run` as `p` and `filled_clauses`.
- **Supplementary S7** takes:
  - the per-run and per-set shares;
  - the two `detailed_en` runs;
  - the re-tokenization agreement check per run;
  - the validation facts (A-N2 526/526; B-N1 787/789 recorded hits, agreement 788/789, the miss at n_tokens = 159);
  - the upper-bound caveat (an EOS exactly at token 160 also gives n_tokens = 160).
- **Rule:** {p} is never written into any file without a verified run (design commit, gate, single run, verifier
  re-run; PD-30). Until then the old clauses stay, except that the false §7.6 clause is corrected in every outcome
  (§3).

## 3. Correction of a false clause
- **The clause:** §7.6 (sec7_verbosity_sign.md:63) says the number of detailed captions that reached the cap "was not
  recorded".
- **Why it is false:** every G2-B decode file records a per-image `n_tokens` field, written by
  `scripts/g2b/decode_qwen3vl.py` (sha `8a855ef4`).
- **Reason:** a judge error. The clause entered through the judge's ruling CC-043 ("its truncation share was not
  recorded, because G2-B outputs carry no hit_max"), as CC-073 records.
- **Fix:** the clause is replaced in every outcome, by row 33's new clause or, if the gate fails, by its fallback.
  "Not recorded" is never used.
