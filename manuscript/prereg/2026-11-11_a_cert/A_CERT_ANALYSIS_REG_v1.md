# A-CERT analysis registration v1: certification of a conclusion under incomplete gold, tested on the human-completed object gold of XM3600-600 (Paper A)

Written 2026-11-11T04:25Z (`date -u`). vsps HEAD `da37725`, branch `paper-v10`. Paper A at `vsps-paperA-spic` `e8aa602`.

**Status.** Draft for a judge read. Nothing was run on labels. No code exists. AI opinion throughout. "unverified" marks a statement the writer did not check.

**What binds this file.**
- Labelling plan v1.1 (`manuscript/prereg/2026-11-11_xm600_gold_completion/XM600_GOLD_COMPLETION_PLAN_v1_1.md`, sha256 `8ad28f67…`), §4 and §5. This file may not change them (CC-327 L6).
- CC-329 N1: "the paper's post hoc bound" in plan §5 is Paper A Supplementary Table S7.2. CC-329 N2: nobody but the annotator opens a label value before this registration is committed.
- CC-327 Ruling 3: this registration is drafted by an agent that has read no label value, is judge-read and committed before any value is opened, and states that the PI saw values while labelling.

**Disclosures.**
- The annotator is the PI, an author who knows the study. He saw every value while labelling. He could not see which caption set or reference named a pair.
- The writer of this file did not open, list or stat `~/vsps_labels`, `key.json`, any label file, any caption file or any per-image prediction file. Read: the plan, CC-327, CC-329, `BUILD.json`, code, and stored aggregate result files (§10).
- As of LOG l.2157 the PI's typed yes and the label-start OPS line of CC-329 Ruling 9 were not in the LOG. Whether labelling has started is unverified.
- Images and captions were analysed before. Only the labels are new. Every result below that uses them is "new labels on previously analysed captions". Every result that does not use them is development or post hoc and is labelled so.

---

## 1. Units

| Item | Value | Source |
|---|---|---|
| Images I600 | the 600 XM3600-600 images | `data/datasets/xm3600/test_data.json` (0a613214) |
| Images I537 | the registered clean subset of the second backbone | `score_g2b.Dataset.clean_index(LADDER, True)`; 537 in `g2b_score.json` G2B-E2 `n_images` |
| Family Q25 (first backbone) | `xm3600_{zeroshot,p1_s43,fuse2_s42}-{short,detailed}` (Section 6.2) | `BUILD.json` |
| Family Q3 (second backbone) | `g2b_q3_xm600-{short,detailed}-T{0,05,08}` (second backbone) | `BUILD.json` |
| Classes V_m | the 69 lexicon classes with an Open Images mapping (part 1) | `data/xm3600/vi_oiv7_map.json` (27f2b1ca) |
| Matcher | `rescap.chair.objects_in`, called as `build_assignment.py` l.74 and l.78 call it | builder 497e5747 |
| References | 1,227 Vietnamese references; 573 images have two, 27 have three (counted today, counts only) | `test_data.json` |

Q25 statistics use I600. Q3 statistics use I537, as registered. Twelve-system statistics use I600; the same on I537 is a sensitivity row.

## 2. Definitions carried over

**From plan v1.1 §5 (verbatim).**
- "**Completed status.** A named pair is present if Open Images verifies it present or the human answer is Y; absent if Open Images verifies it absent or the answer is N; U and A stay unsettled and are counted. An Open Images label is never overridden by a human answer; the control questions measure the disagreement."
- "**Precision (primary).** Per system, completed precision on mapped classes = present / (present + absent) over its named mapped classes. This is the registered verified-precision formula with fewer unsettled mentions. The same quantity over mapped and unmapped classes together is secondary (part 2)."
- "**Recall, F1, verified-negative hallucination and the share of captions naming an absent class** are reported under the two golds, never mixed. […] The two golds: (i) the gold for recall unchanged (Open Images verified-present classes, as registered); (ii) Open Images plus human Y, labelled "pooled gold; favours systems that name more". No verdict attaches to (ii)."
- "**Repeats.** The part-1 answer is the label; the part-3 answer is used only for within-annotator agreement."
- "**No propagation.** Each (image, class) pair keeps its own answer. A Y on one class settles no other class […]. Disagreements between same-map synonyms on one image are counted and reported as a consistency figure."
- "**Pairs whose class is unknown although one pos subclass is verified absent** (33 targets) are settled by the human answer."
- "**Unsettled remainder.** U, A and unanswered pairs keep the lower and upper bound of the paper's post hoc bound, computed as registered."
- "**Aggregation as registered:** distinct mapped classes per caption, summed over images, image bootstrap as registered."

**From the paper (`e8aa602`).**
- Verbosity slope: "the ordinary least squares slope of $F_1$ (in points) on $\ln M$ across the systems of a family, with an image-bootstrap interval; it is conditional on the systems" (`paper/sec3_measurement_setup.md` l.56). M is all `objects_in` mentions per caption.
- Verified precision: mapped mentions that Open Images verifies present, over those it verifies present or absent (`sec3` l.13; `scripts/xm3600_oiv7.py` l.26, l.190–211).
- Label-gold F1: verified precision with the registered recall over verified-present classes (`F1_pos`; `scripts/n_f1/` DESIGN.md "Estimands").
- Bootstrap as registered. Q25: the first 500 rows of `default_rng(0).integers(0, 600, (2000, 600))` (`evaluate_xm3600_predictions_v3.py` l.68–73, l.425–426; `sec3` l.52). Q3: `default_rng(0).multinomial(n, 1/n, size=1000)` over the clean index (G2-B registration `design_constants`; `sec3` l.52). Intervals are 95% percentile intervals.
- The post hoc bound: Table S7.2 (`paper/supplementary_SPIC.md` l.598–605): Q25 +5.83 (unverifiable = error) and +20.13 (unverifiable = correct); Q3 +1.97 and +14.78. Source values: `data/results/n_f1/bracket_result.json` (4796ed12).
- The coverage bound: Lemma 1 and Proposition 2 (`supplementary_SPIC.md` l.104–122), estimator `p50x.f0_hat` (3f562e87).

## 3. Label-derived quantities

**Label of a question.** In the pinned read-only copy of `labels_PI.jsonl`, the last line of a `qid` is its answer (`label` in Y, N, U, A). `key.json` (a2cef894) gives image, class, part, role and bucket. Part-3 lines and control roles never enter a status.

**Completed status** `st_c(i, c)` for a class in V_m: the Open Images status if it is present or absent; else present for Y and absent for N on the part-1 target; else *remainder* (U, A, unanswered).

Per system s on an image set, over distinct mapped classes per caption, summed over images: `pm`, `am` (Open Images present, absent), `hy`, `hn` (human Y, N), `rem`.
- Completed precision: `P_c = (pm + hy) / (pm + am + hy + hn)`.
- Remainder ends (plan §5, N1): `P_c_lo = (pm + hy) / (pm + am + hy + hn + rem)`; `P_c_hi = (pm + hy + rem) / (same denominator)`.
- F1 under gold (i): `F_c = 2 P_c R / (P_c + R)` with R the registered recall, computed from the Open Images statuses only. `F_c_lo`, `F_c_hi` likewise.
- Slopes: `b_F` = OLS slope of 100·F_c on ln M; `b_P` = OLS slope of 100·P_c on ln M. Each has `_lo` and `_hi` values with every system's remainder set the same way, as in Table S7.2.

Implementation rule: precision columns come from `st_c`; recall columns come from the Open Images statuses. Every slope, F1 and interval function is the registered one, imported unchanged (as `scripts/n_f1/bracket.py` does).

## 4. The certification procedure (uses no new label)

### 4.1 One rule for an incomplete gold
An incomplete gold gives each mention one of three states: known present, known absent, unknown. For two systems A and B on one image set, with distinct mapped classes per caption:
- `n_s` = mentions of s; `t_s` = known-present mentions of s.
- Cells of unknown pairs: `B-only` (named by B, not A), `A-only`, `S` (named by both). `U(cell)` = number of unknown pairs in the cell.
- A completion sets `x(cell)` of them present, `0 ≤ x(cell) ≤ X(cell)`, where `X(cell)` is the cap of §4.2 or §4.3.
- Completed precision of the completion: `P(A) = (t_A + x_A + x_S)/n_A`, `P(B) = (t_B + x_B + x_S)/n_B`.

**Orientation.** A is the system with the higher observed precision `t/n`. An exact tie is ABSTAIN. A system with `n_s = 0` makes the pair NOT DEFINED (counted, excluded).

**Worst case** (closed form; A2 plan §3.6, restated for precision):
`Δ_min = t_A/n_A − (t_B + X(B-only))/n_B + min(0, 1/n_A − 1/n_B) · X(S)`.

**Verdict.** CERTIFIED iff `Δ_min > 0`. Otherwise NOT CERTIFIED. ABSTAIN counts as NOT CERTIFIED.

**A slope.** For a family, each system gets the interval `[t_s/n_s, (t_s + X(N_s))/n_s]`, with `N_s` the cell of all its unknown mentions. The slope interval is the minimum and maximum of the OLS slope over the corners: a system above the mean ln M takes its low end for the minimum and its high end for the maximum, and the reverse below the mean. The sign is CERTIFIED iff the interval excludes 0. This ignores that two systems can share a pair; it is an outer interval, so it can only fail to certify. C-ref certifies the precision slope only, because a completion also changes reference-gold recall. C-label gives the precision slope and the F1 slope with the registered recall held fixed (gold (i)). For a slope over m systems the cell level is α_S = α/m.

### 4.2 Reference-only certificate (C-ref)
- **Gold.** Two references per image. For the 27 three-reference images, two are drawn once: `default_rng(20261111)`, images in ascending id, `choice(3, 2, replace=False)`. Known present = named by at least one of the two. No pair is known absent. Unknown = named by neither.
- **`f1(cell)`** = pairs of the cell's systems named by exactly one of the two references (for B-only: classes B names and A does not; likewise S and N_s).
- **Cap, no assumption (w = 0):** `X = U`.
- **Cap, floor w > 0:** `X = min(U, ⌊β⌋)`, with `c = (1 − w)/(2w)`, `L = ln(2/α_S)`, `f1⁺ = f1 + L + √(L² + 2L·f1)`, and
  `β = c·f1 + (1 + c)L/3 + √( ((1 + c)L/3)² + 2c(1 + c)·f1⁺·L )` (A2 plan §3.4–3.5, V-B).
- **Constants.** α = 0.05 per verdict; α_S = 0.025 for every cell; grid w ∈ {0, 0.10, 0.20, 0.30, 0.50}; **primary w0 = 0.20**.
- **Break-down floor** `w*` of a pair: the smallest w at which it is CERTIFIED, by 30 bisection steps on [0.001, 1]; `w* = 0` if certified at w = 0; `NI` if not certified at w = 1.
- **Weakest evaluable floor** `w_ev`: the smallest grid value at which at least 10 of the 30 within-family pairs are CERTIFIED; "none" if no grid value reaches 10.

**What is proved, and under what.** If (A0) every pair a reference names is present, (A1) the references of an image are independent draws from one law (the paper's (A1)), (A1+) naming events of different pairs are independent given the image, and (F_w) every present pair in the cell is named by one reference with probability at least w, then `P(x(cell) > β) ≤ α_S`, so a CERTIFIED verdict is wrong with probability at most α for fixed outputs on these images. Proof sketch: for a present pair named by N of two references, `P(N=0)/P(N=1) = (1−p)/(2p) ≤ c`; sum over pairs and apply Bernstein's inequality twice. **This derivation is an AI derivation. The A2 plan was never judge-read (no CC ruling names it) and never run.** The writer re-derived the two inequalities by hand; that is not a review.

**What it does not guarantee.** Anything when (F_w) fails: present objects that writers rarely name are exactly the unknown mass. Nothing about a re-run of a system, another image set, recall, mixed F1 or CHAIR_s. Proposition 2 cannot certify: it bounds the missing share from below, and a certificate needs a bound from above (A2 plan §3.3). At w = 0 nothing but (A0) is assumed.

### 4.3 Label-side certificate (C-label)
The same rule with the Open Images statuses as the gold: known present = verified present, known absent = verified absent, unknown = no status; cap `X = U`. No assumption is made. Because a human answer never overrides an Open Images label, the completed gold is one of the completions, so a C-label verdict cannot be contradicted by it except through the remainder. C-label carries no hypothesis; it states which conclusions were already fixed before labelling.

### 4.4 Precision interval per system
Reported for each of the twelve systems on I600: low end `(t_s + L̂_s)/n_s`, high end `(t_s + X(N_s; w))/n_s` for each grid w. `L̂_s = φ1²/(4φ2)` with φ1, φ2 the pairs of `N_s ∪ {known-present mentions of s}` named by exactly one and by both references (Proposition 2 with k = 2, applied to the pairs system s names; `φ1(φ1 − 1)/4` if φ2 = 0). The low end is asymptotic and holds under (A0) and (A1). It is never used to certify.

## 5. Facts fixed before unsealing (not predictions)

Derived today from `bracket_result.json` per-system values with the registered OLS formula; the derivation reproduces the stored corner slopes exactly (5.826, 20.134, 1.968, 14.777). Point values; no interval; not checked by registered code.

| Family | Range of the label-gold F1 slope over all completions (C-label, outer corner range of §4.1) | Table S7.2 | All-references slope |
|---|---|---|---|
| Q25 (I600) | [+2.31, +23.65] | [+5.83, +20.13] | −2.43 |
| Q3 (I537) | [−4.68, +21.42] | [+1.97, +14.78] | −6.39 |

Consequences:
- Table S7.2 sets every system's unverifiable mentions the same way. It is not a bound on the slope (the design note says so: "No bracketing of the registered slope is claimed"). The completed slope can fall outside it.
- Q25: `b_F > 0` and `b_F >` the all-references slope hold for every completion, at point level. They are not hypotheses. A computed `b_F` outside [+2.31, +23.65] is a code fault: STOP.
- Q3: `b_F >` −6.39 holds for every completion at point level. The sign of `b_F` is open.
- The precision slope `b_P` has the range [−45.67, +26.43] (Q25) and [−59.01, +38.81] (Q3); its registered values are −2.52 and −5.37. Its sign is open in both families.

The freeze (§8) recomputes these with the registered code and bootstrap, and pins them.

## 6. Hypotheses on the new labels

Every verdict below carries the words **"single annotator"** until the second annotator has labelled the overlap images. Then plan §4 applies: part-1 target kappa at or above 0.60 keeps the verdict, with kappa reported; below 0.60 every verdict is reworded "sensitivity analysis only" with the disagreement table. Nothing is recomputed and no threshold moves. Control agreement (443 questions) and repeat agreement (150) are reported whatever their value; they gate nothing.

**Remainder rule.** A point rule must hold at the registered value and at both remainder ends (`_lo`, `_hi`; every system's remainder set the same way, as Table S7.2 is computed). If it holds at the registered value but not at both ends, the verdict is INCONCLUSIVE (remainder).

### H1. The completed label-gold slope
Statistic: `b_F` (compared with Table S7.2, an F1 slope; N1). `b_P` is reported beside it with its interval and carries no verdict.

| Id | Prediction | PASS | FAIL | Otherwise |
|---|---|---|---|---|
| H1a | Q3: `b_F > 0` | point > 0 and the 95% interval excludes 0 | point ≤ 0 | INCONCLUSIVE |
| H1b | Q25: `b_F` inside [+5.83, +20.13] | point inside | point outside | – |
| H1c | Q3: `b_F` inside [+1.97, +14.78] | point inside | point outside | – |

Reported with H1b and H1c: the paired-bootstrap interval of `b_F` minus each end of Table S7.2.

Outcomes that contradict the paper's reading, and the fixed sentence for each:
- H1a FAIL: "With the unverifiable mentions settled by a human, the label-gold slope of the second backbone is not positive; the registered PASS depended on excluding them." This contradicts Section 6.3's support for a positive label-gold slope on a second backbone.
- H1b or H1c FAIL below the lower end: "Counting unverifiable mentions as errors did not bound the slope from below." Section 6.2's sentence that +5.83 "still" lies above both reference slopes must then be replaced by the certified range of §5.
- H1b or H1c FAIL above the upper end: the same for the upper end.
- All three PASS: the paper's reading stands, and the post hoc bound is replaced by a measurement.

### H2. Validity of the reference-only certificate
Units: the 30 within-family pairs (15 in Q25 on I600, 15 in Q3 on I537). The 36 cross-family pairs on I537 are a secondary row.

**Truth.** A pair is *confirmed* if `P_c(A) − P_c(B) > 0` in the certified direction (for a non-certified pair: in the observed reference-gold direction) at the registered value and at both remainder ends. A tie is not confirmed. Only precision is used, so no verdict rests on gold (ii).

**H2a (primary, at w0 = 0.20).** `V_c` = share confirmed among CERTIFIED pairs; `V_n` = share confirmed among the others.
- NOT EVALUABLE if fewer than 10 pairs are CERTIFIED or fewer than 10 are not. This is known at the freeze and is declared there, before unsealing.
- PASS: at most ⌊0.05 · n_cert⌋ certified pairs are not confirmed (so `V_c ≥ 0.95`), and `V_c > V_n`.
- VALID, NOT DISCRIMINATING: the first condition holds and `V_c ≤ V_n`. Fixed sentence: "the certificate made no error, and the uncertified reference-gold orderings held as often".
- FAIL: more than ⌊0.05 · n_cert⌋ certified pairs are not confirmed. Fixed sentence: "the floor w0 is refuted on a two-reference Vietnamese gold; only the no-assumption certificate may be used there".
- Reported whatever the verdict: `V_c`, `V_n`, the image-bootstrap 95% interval of `V_c − V_n` (B = 2,000, seed 20261111, certified set held fixed), the exact one-sided 95% lower limit `0.05^(1/n)` when no certified pair fails (pairs share images and systems, so it is descriptive), and the null rules: constant (certify all), margin (the n_cert pairs with the largest |Δ| under reference gold), length (certify iff the observed-better system names more). If the margin rule makes fewer errors than C-ref at the same count, the paper may not say the certificate beats a margin threshold.

**H2b (budget coverage, always evaluable).** For each of the twelve systems on I600, `x_s` = completed-present pairs in `N_s`; `x_s_hi` adds the remainder in `N_s`. Covered iff `x_s_hi ≤ ⌊β(N_s; w0)⌋`.
- PASS: at least 11 of 12 covered. FAIL: 10 or fewer. If the Open Images statuses alone already put two systems above the budget, FAIL is determined at the freeze and is declared there.
- If `⌊β⌋ ≥ U(N_s)` for all twelve systems, the budget never binds and the label is "PASS (vacuous)"; it supports nothing. The number of systems with `⌊β⌋ < U(N_s)` is printed at the freeze.
- Reported per system and for every grid w: `x_s`, `U(N_s)`, `β`, and the measured effective floor `ŵ_s = f1 / (f1 + 2·x_s)`.

**Registered secondary row (no PASS for the method).** H2a's counts at every grid w and at `w_ev`, with the label VALID AT w or REFUTED AT w by H2a's error rule. The break-down floor `w*` of every pair beside its confirmed status.

### H3. The coverage bound against the completed gold
- Universe `N_u`: pairs (i, c) in I600, c in V_m, named by at least one of the twelve caption sets, with no Open Images status. It is fixed by the images and the stored outputs. Inside it the completed gold is a full inventory up to the remainder.
- Gold: the two references of §4.2. `φ1`, `φ2` = pairs of `N_u` named by exactly one and by both. `f̂0 = φ1²/(4φ2)` (`p50x.f0_hat` with T = 2).
- `X` = pairs of `N_u` named by neither reference with human Y; `X_hi` adds the remainder among them.
- `D = X − f̂0` and `D_hi = X_hi − f̂0`, with the image bootstrap (B = 2,000, seed 20261111; multiplicities as `a_m1.boot_weights`).

| Label | Rule |
|---|---|
| RESPECTED (PASS) | the 2.5th percentile of D* is above 0 |
| VIOLATED (FAIL) | the 97.5th percentile of D_hi* is below 0 |
| INCONCLUSIVE | neither |
| NOT EVALUABLE | φ2 = 0 or φ1 + φ2 < 50 |

VIOLATED means that more unnamed pairs are predicted than exist among the pairs the systems name: (A1) fails on these references, or references name classes that are absent. The count of reference-named pairs of V_m whose completed status is absent is reported beside it.

Secondary (no verdict): the same on all system-named pairs of V_m (its RESPECTED outcome is largely foreseeable from stored Open Images aggregates); the ratio `X / f̂0`; the low ends of §4.4 against `P_c` for the twelve systems; the A-M1 form `D_L` over all completed-present pairs, where only "consistent" can be read because the labels are not a complete inventory.

## 7. Evaluability, multiplicity, order

**How many comparisons exist.** Twelve caption sets give 66 system pairs: 15 + 15 within families, 36 across. Q3's six runs are two prompts at three temperatures, so about 9 of its 15 pairs are short-versus-detailed and 6 are near-copies. Effective independent information is far below 30. Per-image pairs are not used: the guarantee is for pooled counts. The image bootstrap gives intervals for the truth side only. H1 has two families, so two units. H3 has one pooled unit; H2b has twelve.

**Multiplicity.** Six registered predictions: H1a, H1b, H1c, H2a, H2b, H3. Rules are point or count rules, except the intervals of H1a and H3, which are 95% and uncorrected, as in the paper's registrations (`sec3` l.52). The Bonferroni interval (99.17%) is printed beside each of those two. The paper prints the number registered, passed, failed, inconclusive and not evaluable. "All pass" is written only if all six pass.

**Order.** (1) quality figures of plan §4; (2) H3; (3) H2b; (4) H2a and its secondary row; (5) H1; (6) secondary rows. One pass; the script refuses to run if its result file exists.

## 8. Freeze before unsealing

`a_cert.py freeze` reads no label file (path guard). It writes `data/results/a_cert/freeze/FREEZE.json` with: pins of every input and code file; all constants of §4 and §6; for all 66 pairs the counts, `Δ_min` at each grid w, the verdicts and `w*`; `w_ev`; the null rules' selections; the §4.4 intervals; the C-label verdicts for pairs and slopes; the §5 ranges with registered bootstraps; `φ1`, `φ2`, `f̂0` of H3; the evaluability declaration of H2a; any H2b outcome already determined. The file is hashed, copied read-only, committed through the gatekeeper and pinned by one LOG line. Unsealing without that line is a fault.

## 9. Expectations stated now (unverified; rough arithmetic from stored aggregates)

- Stored verified precision of Q25 lies between 91.6 and 95.9, while object precision against the references lies between 36.7 and 72.3 (`xm3600_oiv7.json`). Between 30% and 57% of mapped mentions have no Open Images status. A valid cap is therefore close to "all unknown mentions present". The writer expects **few or no CERTIFIED pairs at w = 0 and at w0**, so H2a is likely NOT EVALUABLE, and expects that a floor strong enough to certify ten pairs is refuted.
- Under the stored Open Images statuses alone, the reference-gold order of Q25 agrees in sign with verified precision for 9 of 15 pairs, including all five pairs against the most verbose system. A margin rule may therefore be right where the certificate abstains.
- H3's universe was chosen so that its outcome is not readable from stored aggregates.

## 10. Secondary and post hoc rows (each labelled where printed)

| Row | Label | Note |
|---|---|---|
| Part 2 (classes without a mapping): `P_c` over mapped and unmapped classes; H2 and H3 repeated | secondary; separate later unsealing; partial part-2 labels are not used; gated by the part-2 kappa | plan §5, §6 |
| Recall, F1, verified-negative hallucination, captions naming an absent class under gold (ii) | "pooled gold; favours systems that name more"; no verdict | plan §5 |
| Same-map synonym disagreements; U and A rates per class | descriptive | plan §5 |
| H1 to H3 on the 150 overlap images with each annotator's labels | descriptive; after the second annotator | plan §4 |
| COCO-5000, nine systems, 36 pairs, instance gold as the top level (A2 plan K0–K3) | development; needs its own judge read | A2 plan |
| OPERA and "Less is More" released outputs: C-ref at one to five references against the CHAIR gold, for the 15 published comparisons | post hoc descriptive, never evidence for H2: the paper already scored these 15 gains under the full gold | METHOD_DELTA_A §4 |
| Other-family arm (PI-1105k, PI-1107c): a third family on I600 | development; C-ref and C-label at once; completed-gold rows only after a top-up labelling session and a separate unsealing; CC-327 L2 applies | plan §6 |

## 11. Code to write

| File | Content | Checks |
|---|---|---|
| `scripts/a_cert/a_cert.py` | modes `selftest`, `gate`, `freeze`, `score`. Pins and a path guard: `freeze` and `gate` refuse any path under `vsps_labels`; `score` refuses without the FREEZE pin line, without part 1 complete (2,233 part-1 questions answered), or if a result exists | selftest: (i) toys T1 and T2 of A2 plan §3.10, restated for precision, in exact fractions; (ii) the closed form of §4.1 equals exhaustive enumeration on at least 300 random small instances; (iii) the corner slope range equals enumeration over all corners; (iv) `Δ_min` is monotone in w; (v) size simulation of β (2,000 replicates; point mass at w and two Beta laws above w; a code check, not evidence); (vi) status logic on a synthetic label file: last line wins, part 3 ignored, Open Images never overridden, U and A to the remainder, no propagation between synonyms; (vii) every verdict label at its boundary |
| `scripts/a_cert/a_cert_mutants.py` | each mutant must be caught | separate intervals instead of the coupled form; shared-cell sign flipped; c = (1−w)/w; cap without `min(U, ·)`; a tie counted as confirmed; a human N overriding Open Images present; the part-3 answer used as the label; a Y propagated to a synonym; recall recomputed from the completed gold; remainder dropped from `_lo`/`_hi`; the certified set recomputed after labels; H3 on the wrong percentile; `freeze` allowed to open the label path |
| `scripts/a_cert/SHA256SUMS` | pins | – |

`gate` reproduces, through the same functions `score` uses and without labels: the registered slopes 19.3247 and 13.7085; the four Table S7.2 ends; the `BUILD.json` counts (4,910 named pairs; 1,790 part-1 targets). Any mismatch stops the work.

Reused unchanged, by import: `scripts/xm3600_oiv7.py` (`resolve_map`, `statuses`, `caption_rows`); `rescap.chair.objects_in`; `scripts/pascal50s/p50x.py` (`f0_hat`); `scripts/n_f1/bracket.py` and through it `evaluate_xm3600_predictions_v3.py` and `scripts/g2b/score_g2b.py` (slopes, F1, bootstraps, clean subset); `scripts/a_m1/a_m1.py` (`boot_weights`; imported, never run, because its guard refuses XM3600 paths); `tools/obj_rater/build_assignment.py` (`load_systems`).

## 12. Custody of the unsealing

1. Judge GO on this file; gatekeeper commit; LOG line with its sha256. Until then N2 holds.
2. Code written; selftest and mutants pass; one-judge code read; commit.
3. `gate`, then `freeze`; FREEZE pin line in the LOG.
4. Part 1 complete. The session-end LOG line of plan §3 gives `wc -l`, the sha256 and the read-only copy `labels_PI.<UTC>.jsonl`.
5. The operator runs `a_cert.py score` once on that copy, with its sha256 as an argument. Only the script reads the file and `key.json`. The operator does not display the outputs. Logged: UTC start and end, command, exit status, sha256 of the label copy, of `key.json`, of FREEZE.json and of the result.
6. One-judge result read; then the coordinator and the PI see the result. The PI does not open `key.json`.
7. Part 2, the second annotator and the top-up session are separate, later unsealings with their own LOG lines. They never change a part-1 verdict except through the kappa rule.

## 13. Open questions for the judge

| # | Question | Recommended answer |
|---|---|---|
| Q1 | Proposition 2 bounds the missing share from below and cannot certify. The certificate here uses the cap and a floor w (A2 plan Lemma B). Is that the method the PI's decision means? | Yes. Say it in the paper in these words. Proposition 2 keeps the roles of §4.4 and H3. |
| Q2 | Lemma B and the Bernstein budget were never judge-read. | Check §4.2 in this read; Codex is unavailable until 11-27. If not accepted, keep only w = 0 and report the grid as a sensitivity analysis. |
| Q3 | Primary operating point: fixed w0 = 0.20, or `w_ev`? | Keep 0.20 primary, `w_ev` secondary. 0.20 has no principled basis beyond the A2 plan; `w_ev` is chosen by the data, though without labels. |
| Q4 | N_min = 10 of 30 and the 0.95 share. | Accept; with 30 dependent pairs no stronger claim is honest. |
| Q5 | Two references for the 27 three-reference images: seeded draw or first two? | Seeded draw (the paper's rule for k-reference golds); first two as a sensitivity row. |
| Q6 | H2b's pass count (11 of 12) and α_S = 0.025 for every cell. | Accept. |
| Q7 | May `freeze` run before the PI's yes and the label-start line are in the LOG? | Yes; it reads no label. |
| Q8 | The released logs under `.session_backup/2026-10-27/a1_precheck/raw/` are reserved for A2-OC1. With A2 folded into Paper A, is OC1 dropped, kept, or moved? | Keep the reservation untouched until a ruling; use only the OPERA and "Less is More" re-download for the post hoc row. |
| Q9 | Three-tier rule: no rehearsal can use the new labels. Is the freeze, with H2a's evaluability declared before unsealing, enough? | Yes. A rehearsal on stored Open Images statuses is in §9 and predicts a weak outcome; it is disclosed, not hidden. |
