# A-CERT analysis registration v1.3 (H2d): the break-down floor as a ranking of comparisons (Paper A)

Written 2026-11-11T08:18:55Z (`date -u`). vsps HEAD `0519b82`, branch `paper-v10`. Addendum to `A_CERT_ANALYSIS_REG_v1_1.md` (sha256 `e564b7b1…`, committed in `0519b82`; frozen, not edited), under CC-335 Ruling 9 (sha256 `399096fd…`). `data/results/a_cert/freeze/` did not exist at 08:18:55Z: the v1.1 freeze had not run.

**Revised under CC-336** (sha256 `e9733b64…`), 2026-11-11T09:11:05Z (`date -u`), vsps HEAD `bd7ef1c`. Revision of `A_CERT_ANALYSIS_REG_v1_2_H2D.md` (sha256 `ce586f56…`, kept unchanged). `data/results/a_cert/` did not exist at 2026-11-11T09:11:05Z: the v1.1 freeze had not run.

**Changes from v1.2.**
- Version: title v1.2 → v1.3; this header.
- H-B1: the printed label (between the first pair of quotation marks under Label) replaced.
- H-B2: §3 Bootstrap bullet names the exact stream; §6 Q3 recommended answer replaced; one line added after the §6 table (CC-336 binds).
- H-B3: §3 PASS and FAIL readings: "30 dependent pairs" → "n1 + n0 dependent pairs" (three places).
- H-B4: §4 Size bullet replaced; the external d-to-AUC citation removed.
- N-H1: Status: the "changes no other rule" sentence now names the prediction count (§5).
- N-H2: §5 second bullet: the void case (count stays six) appended.
- N-H3: FAIL reading: "the [margin / length] rule" → "the rule with the larger AUC (margin or length)".
- N-H4: this header and block.

**Label (printed with every H2d number).** "registered on 2026-11-11 after the aggregate look on COCO-5000, before anyone but the annotator opened a human label value; the human answers are unseen by the analysts, the Open Images statuses that enter the outcome are partly seen (v1.1 §9)". If this file is committed after the v1.1 `freeze` has run, "changed after the freeze, before labels" (v1.1 §8) is added. H2d is valid only if this file is committed and pinned by a LOG line before the v1.1 `score` runs (CC-335 Rulings 3 and 9); otherwise H2d is void and its AUCs are exploratory.

**Status.** Draft for a one-judge read (REVERSIBLE, 85). Nothing was run; no label value was opened. AI opinion. H2d is a registered verdict on a quantity v1.1 already prints (`w*` beside confirmed status, v1.1 H2 secondary row). Apart from the count of registered predictions (§5), it changes no rule of v1.1: w0 = 0.20 stays primary; H1, H2a, H2b and H3 are unchanged. **Whether H2d also becomes a clause of the 11-16 entry gate is the PI's decision (CC-335 P-2) and is not decided here.**

**Disclosures.**
- The writer did not open, list or stat `~/vsps_labels`, `~/.vsps_sealed`, `~/bpa1pull_1108` or any reserved directory, and opened no label, caption or per-image file. Read: CC-335, v1.1, addendum VP v1.
- The Open Images statuses are partly seen (v1.1 §9: under them alone the Q25 reference-gold order agrees in sign with verified precision for 9 of 15 pairs, including the five against the most verbose system). Confirmed status uses those statuses and the human answers, so the outcome is partly foreseeable. The human answers are unseen by the analysts; the annotator (the PI) saw every value while labelling (v1.1 Disclosures).
- Nothing from Part P or Part V of the VP addendum feeds H2d: no constant, threshold, seed or the SESOI comes from COCO-5000, Part P or any XM3600 outcome. OC1 stays an optional second leg behind its own gate.

## 1. Units, outcome, exclusions
- Units: the 30 within-family pairs of v1.1 H2 (15 Q25 on I600, 15 Q3 on I537), pooled into one ranking. The 36 cross-family pairs are not used.
- Exclusions (v1.1 H2 "Ties and undefined pairs"): ABSTAIN and NOT DEFINED pairs are excluded before anything else, and their number is printed. They are fixed at the freeze (no label input).
- Outcome `y` = 1 if the pair is *confirmed* under v1.1 H2 "Truth" (`P_c(A) − P_c(B) > 0` at the registered value and at both remainder ends; a tie is not confirmed), else 0. A is the system with the higher observed reference-gold precision (v1.1 §4.1), so the certified and the observed direction coincide. `n1`, `n0` = confirmed and unconfirmed pairs after exclusion.

## 2. The three rankings (all fixed before labels, read from FREEZE.json)
- **w\***: the break-down floor of v1.1 §4.2 (C-ref, V-B budget, the seeded two-reference gold, 30 bisection steps), ranked ascending: score = −w\*. NI pairs take the lowest score and are tied with each other. (`w* = 0` cannot occur, addendum VP v1.1 §V.4a; it would be a code fault.)
- **Two-reference margin**: `Δ_ref = t_A/n_A − t_B/n_B` under the v1.1 §4.2 gold, the |Δ| by which the v1.1 H2a margin null rule ranks; computed from the per-pair counts FREEZE.json holds. Larger = ranked higher.
- **Length rule**: the v1.1 H2a length null rule as a binary score: 1 if `n_A > n_B` (the observed-better system names more), 0 otherwise, including `n_A = n_B` (v1.1: equal `n` is not certified).
- **Ties**: equal stored values are ties and get half credit in every ranking. No tie-break is used: neither v1.1's pair-index tie-break of the margin rule nor the |Δ| tie-break that addendum §V.6 uses for COCO K2 (which would lend the margin to w\*).

## 3. Statistic and verdict
- `AUC(s)` = [Σ over confirmed i and unconfirmed j of 1[s_i > s_j] + ½·1[s_i = s_j]] / (n1·n0). `D = AUC(w*) − max(AUC(margin), AUC(length))`.
- Bootstrap: B = 2,000, seed 20261111, image multiplicities = rows 1 to 2,000 of `a_m1.boot_weights(600, numpy.random.default_rng(20261111), 2000)` (row 0 is the point), as v1.1 H3, fixed here whatever stream H2a's interval uses, one vector over I600 per replicate; Q3 pairs use its entries on I537. Scores and exclusions are held fixed (as H2a holds the certified set fixed); `y` is recomputed from the reweighted counts at all three remainder levels; the three AUCs and the max are recomputed inside each replicate, giving `D*`. A replicate with `n1* = 0` or `n0* = 0` gets `D* = −1` (least favourable) and their number is printed. Percentiles as v1.1's registered percentile intervals.
- **NOT EVALUABLE** iff `n1 < 5` or `n0 < 5`. This needs labels, so it is known only at `score`, unlike H2a.
- **PASS** iff `D ≥ 0.10` (SESOI, §4) and the 2.5th percentile of `D*` is above 0.
- **FAIL** otherwise.
- Printed whatever the verdict: `n1`, `n0`, excluded count, NI count, the three AUCs, `D` with its 95% interval, the same per family (descriptive, no verdict), and the 0.36th percentile of `D*` (Bonferroni over seven predictions, §5; no verdict).

Fixed readings (each with the label above and "single annotator"; the v1.1 §6 kappa rule applies unchanged):
- PASS (CC-335 Ruling 4 (iv)): "the break-down floor w\* ranked the robustness of comparisons better than the observed margin and the length rule on a new benchmark's human-completed gold (single annotator, n1 + n0 dependent pairs)". It is not a validation of the floor guarantee (that is H2a and H2b) and changes no H2a verdict.
- FAIL: "On the human-completed gold of XM3600-600 (single annotator, n1 + n0 dependent pairs), the break-down floor w\* did not rank the comparisons better than the observed two-reference margin and the length rule by the registered amount (D = …, 95% interval …; SESOI 0.10). With n1 + n0 dependent pairs the test has low power; this result alone does not show that w\* ranks worse." Only if the 97.5th percentile of `D*` is below 0 the paper adds: "the rule with the larger AUC (margin or length) ranked them better than w\* here".
- NOT EVALUABLE: "H2d could not be evaluated: n1 confirmed and n0 unconfirmed pairs, at least 5 of each needed." The AUCs are printed as descriptive figures with no reading.

## 4. SESOI = 0.10 AUC (writer's choice; CC-335 gives no number; Q1)
Rationale (uses no XM3600, COCO-5000 or Part P outcome):
- Resolution. Moving one confirmed pair across a ranking changes its AUC by at most 1/n1 (one unconfirmed pair: 1/n0). With 30 pairs and balanced classes (15/15) one pair is worth at most 0.067, so at 0.10 no single pair's placement reaches the SESOI alone. With unbalanced classes (n0 = 5) one pair is worth 0.20; there the bootstrap condition carries the weight.
- Size. No external benchmark is used. Published d-to-AUC conversions grade one AUC against 0.5, not a difference between two AUCs on the same pairs, so the SESOI rests on the resolution argument above: at balance a gain of 0.10 is more than one pair's placement. A score that needs a floor model and a budget is worth using over a free margin only with a gain of that order.
- Not 0.05: the A2 plan's 0.05 is a coverage share (Δ_cov), a different scale, and below 0.067 one pair can decide at balance.

## 5. Order, multiplicity, custody
- `score` computes H2d right after H2a (v1.1 §7 order, step 4), in the same single pass, under the v1.1 §12 fault rule. The scores come only from FREEZE.json; no score-side quantity is recomputed after labels. If FREEZE.json exists when this file is committed, nothing is re-frozen.
- H2d is a seventh registered prediction: the v1.1 §7 count prints seven, H2d marked by its label; "all pass" needs all seven. The Bonferroni intervals of H1a and H3 are unchanged. If H2d is void (not committed and pinned before `score`), the count stays six.
- Code (to the one-judge code read; none exists yet): selftest: AUC with ties equals brute-force enumeration on random small cases; NI handling; the empty-class rule; every verdict at its boundary (`D = 0.10`; `n1 = 5` against `n1 = 4`). Mutants: NI ranked first; ties scored 0 or 1; max replaced by min or by the margin alone; scores recomputed after labels; a tie in `P_c` counted as confirmed; excluded pairs kept; the |Δ| tie-break imported for w\*.

## 6. Open questions for the judge
| # | Question | Recommended answer |
|---|---|---|
| Q1 | SESOI: 0.10 AUC (writer's choice, §4)? | Accept 0.10. Default if not ruled: 0.10 |
| Q2 | Length rule: binary as v1.1 defines it, or a graded `ln(n_A/n_B)`? | Binary. A graded score is a new choice made after the look |
| Q3 | Replicate stream: the same `a_m1.boot_weights` vector as H2a's interval and H3 (I537 entries for Q3)? | Yes: rows 1 to 2,000 of `a_m1.boot_weights(600, numpy.random.default_rng(20261111), 2000)`, one vector over I600 per replicate, I537 entries for Q3 pairs (CC-336). No fallback to another stream. |
| Q4 | Empty-class replicates: `D* = −1`, counted and printed? | Yes (least favourable) |
| Q5 | Count H2d as a seventh prediction in v1.1 §7? | Yes |
| Q6 | If most of the 30 pairs are NI at the freeze, the w\* ranking is nearly constant. Add a freeze-time rule? | No. Keep Ruling 9's evaluability rule; the freeze prints the NI count, and a FAIL is then reported as such |
| Q7 | Pooled AUC over both families, or per family? | Pooled (Ruling 9: "the 30 within-family pairs"); per-family AUCs descriptive only |

CC-336 answers Q1-Q7. Where a recommended answer above differs from it, CC-336 binds.
