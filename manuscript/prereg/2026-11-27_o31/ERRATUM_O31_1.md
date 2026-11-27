# ERRATUM O31-1 to PREREG_DRAFT_O31_v3.md (5b33480b, commit 3d49435) and COMPUTE_PLAN_O31_v3.md (7557ca3b)

Written by ruling CC-504 (2026-11-27), before any O31 output exists: no P0r, G1, G2, P1 or G3 output, and no tier-2 or tier-3 file has been read.
It is committed before P0r. It changes no registered threshold, margin, seed, set or hypothesis.
It does four things:
- fixes details that the committed text leaves open;
- settles one conflict between two committed texts by the binding ruling CC-501 W3;
- corrects one number in the compute plan;
- adds two disclosures.

## E1. Secondary family verdict (§6.2 vs §6.3)
§6.3 (the CC-501 W3 block) governs the verdicts of H3, H4, H5a and H5b. A member PASSes iff its Holm-adjusted one-sided bootstrap p is below 0.05; for H4, the point condition Δ_RT >= +10.0 must also hold.
The CI conditions written in §6.2 under H4 ("CI lower bound > 0", "CI upper bound of FA(V_O31) − FA(V_FAIR) ≤ +5.0") and under H5a/H5b ("CI lower bound … > 0", "the same D rule as H2") are superseded as pass rules. The unadjusted 95 % CIs are reported beside each member, as W3 requires. For H5b the statistic is D_en = (h_S2 − h_S1) − 0.25 × (h_S0 − h_S1), computed on English counts.

## E2. Three-state combiner when a family score is missing or undefined (§4.2)
A family whose score for a proposition is missing or undefined (NaN, yes+no mass 0) counts as UNSURE for that proposition:
- It never supports.
- It never refutes. REJECTED therefore needs every declared family to have a score <= τ_rej.

With every score present, this equals §4.2's max rule. In K0 a Q+ key that is absent from a used family's table is a FAULT, not UNSURE.

## E3. Affirmative question Q+ (§4.1)
- **Which probe:** Q+ of a stage-1 proposition is the first probe in `evidence.probes` whose `model` is `5CD-AI/Vintern-1B-v3_5`. That is the string recorded in the stage-1 records, and it equals `m0.MODEL["repo"]` and E1b's `VIN`. It is the direct question: `rescap/pipeline/verify.py` records the direct question before the negated one.
- **Join key:** `qkey` (strip, drop a final "?" or ".", collapse spaces, lower-case), as in E1b.
- **Records without Q+:** a proposition with no such probe keeps its recorded status, because the verifier rules only on what it probes. In the stage-1 records (tarball b312de68), 190,591 propositions carry exactly two such probes and 1,625 carry none. All 1,625 are recorded REJECTED, that is, rejected before any probe.
- **Reporting and the FAULT rule:** the number of propositions without Q+ is reported in the K0 output. A proposition whose recorded status is not REJECTED and that has no Q+ is a FAULT.
- **Family tables:** every family table has one row per (image file name, qkey), holding s = p(yes) / (p(yes) + p(no)). The first occurrence is kept. This is the E1b `probes.jsonl` format.

## E4. Order of the verifier, person-noun neutralization and the build (§4.2, §4.4)
For every arm the order is the same:
1. Take the stage-1 records as recorded, before any neutralization.
2. Set every proposition's `verification.status` from the arm's verifier:
   - S1 / OP_strict: the recorded FAIR verdicts, unchanged;
   - S2 and the other grid points: the O31 three-state combiner.
3. Run FAIR `person_uncap` unchanged, with its default types (entity, attribute, action, counting).
4. Run the build (§4.4).

The K0 input is the pre-neutralization record set; the stage-1 tarball b312de68 is of that kind (0 of its 3,700 records carries a `gender_uncap` backoff). A record that already carries a `gender_uncap` backoff is a FAULT.

## E5. n_SUPP_entities and the build (§4.4)
- **n_SUPP_entities(i):** the number of distinct subject entity ids among the image's SUPPORTED propositions of type `entity`, counted after step 3 of E4. A proposition with no entity id counts by its own proposition id.
- **"FAIR's filters":** `build_dpo_data.build_for_image` with `--style-variation --clean-props --detailed-variant B --min-supported 1`, the detailed budget of §4.4 and the short budget unchanged. This is the build of FAIR's training store; FAIR's SFT trained on `data/supervision` (README.md l.99).
- **`scripts/clean_supervision.py`:** it is NOT applied to any arm. Disclosure: before this pin, the ruling judge saw the S1-type store recall with and without that script in `data/supervision_v2/README.md`. The pin follows FAIR's recorded training input, not those numbers.
- **Store identity:** the SFT of each arm trains on the byte-identical `sft.jsonl` whose R_sup and P_sup K0 reports. Its sha256 is recorded in the K0 output and in the training record.

## E6. Selector scores (disclosure, §4.4)
FAIR's selector is unchanged. It weights each proposition by the recorded FAIR support and contradiction scores. Only `verification.status` changes between arms. S2's selection order therefore still uses FAIR's recorded scores. The paper states this.

## E7. K0 runs (§4.5; COMPUTE_PLAN §1)
- **P0r:** the Vintern-only half of the §4.3 grid, which is 15 points. COMPUTE_PLAN_O31_v3.md row P0r says "10 points"; that is an error, and §4.3 governs. P0r is a preview: its output carries no K0 verdict.
- **The K0 verdict:** it is the P1 output alone. P1 uses all 30 points and both families, on the training pool after the §3.5 (a) removals.
- **OP\*:** ties go to the higher P_sup, then to the earlier grid point. The grid order is family set (Vintern only, then Vintern ∪ InternVL3), then τ_acc ascending, then τ_rej ascending. If no point meets P_floor, K0 FAILs.
- **OP_mid:** chosen over all 30 grid points, whether or not they meet P_floor. Ties go to the higher P_sup, then to the earlier grid point.

## E8. Optimiser steps (§2)
- **N_steps:** N_steps = 2 × floor(rows_S1 / 8), where rows_S1 counts every row of S1's `sft.jsonl` (detailed and short). Every arm runs exactly N_steps through `max_steps`.
- **Loss mask:** `--loss-mask legacy`, as in the FAIR runs.
- **Check:** the training record shows global_step = N_steps.

## E9. Bootstrap details (§6.3)
- **Index draws:** numpy PCG64, `default_rng(seed)`. One (B × n) index matrix is drawn in row chunks and shared by every statistic.
- **Percentile 95 % CI:** with the defined replicates sorted (count b), the bounds are element int(0.025 b) and element int(0.975 b) − 1.
- **Undefined replicates:** a replicate with a zero denominator is undefined. It is counted and reported, it is left out of the CI, and it counts on the null side of every one-sided p-value.

## E10. Tier-2 rehearsal (§7)
- **Random stream:** one PCG64 stream with seed 20261128. Each outer draw is 4,224 image indices drawn from the 5,000 with replacement, followed by its B_in = 1,000 inner index rows.
- **H3–H5b:** they are evaluated in each outer draw and reported as pass shares. They do not gate.

## E11. Gold for tier 2 (§3.4)
The tier-2 registered-form rows (H1, H2 and the rehearsal) use the tier-3 gold form: COCO-2014 instance annotations for the 80 classes only. A row with gold = instances ∪ references, comparable to FAIR's COCO block, may be reported. It is labelled descriptive.

## E12. Seeds in the count-matched precision (§5, §6.3)
For H3, S2 seed j is paired with S1 seed j (j = 42, 43, 44). Per image, TP_S2(k), TP_S1(k) and k are computed for each pair and then averaged over the three pairs, before resampling.

## E13. Overlap direction (§3.5)
- **Part (a):** x = the training pool, compared against each named set. A hit leaves the pool.
- **Part (b):** x = Karpathy test 5,000 and x = the tier-3 set, each compared against UIT-ViIC test 231. A hit leaves x.

In both parts, only x's mirrored hashes count, as in the committed W25 rule.
