# ERRATUM O31-4 to PREREG_DRAFT_O31_v3.md (5b33480b), ERRATUM_O31_1.md (91108b81), ERRATUM_O31_2.md (817eac8f), ERRATUM_O31_3.md (979486bf) and COMPUTE_PLAN_O31_v3.md (7557ca3b)

Written by ruling CC-525b (2026-11-28) as the first part of a split amendment. The second part, ERRATUM_O31_5, follows before the first G3 output.
It is committed before the first output of P0r exists. When it is committed, no output of P0r, P1, G1 or G2 exists; of the §3.5 overlap pass only the laptop step `kv` has run (KV-4,224 ids and descriptors only, no overlap result).
It changes no hypothesis, threshold, margin, seed, set, grid, gate, estimand, statistic or stop rule.
It does three things:
- it fixes the rule that picks two extra operating points from P1's `k0.json`;
- it fixes one reporting row on the position of OP\* in the grid;
- it fixes the form of any later test across the five points and its place in a family (E4-7).

**Why now.** `gate.run_k0` writes the S1 store's numbers (`s1`) and, for every grid point it computes, R_sup, P_sup and the store's sha256 (`points`) into every `k0.json`, the incomplete P0r preview included. P0r's preview covers the 15 Vintern-only points on 3,698 records; P1 covers all 30 points on the training pool after the §3.5 part (a) removals, which holds nearly the same images. A rule that picks points by R_sup is therefore fixed before any `k0.json` exists, so that no value of one can shape it.

**What reads what.** The rules of E4-2 to E4-5 read P1's `k0.json` only. That file is computed from the outputs of G1, G2 and the §3.5 pass. E4-7 reads `ops5.json` and tier-2 outputs only. No rule here was chosen after any output of P0r, P1, G1 or G2 existed, or after any output of the §3.5 pass other than the laptop step `kv`'s KV-4,224 ids and descriptors (which hold no grid-point value), and no rule here reads P0r's preview.

## E4-1. Terms
- **S1 store:** the store K0 builds for S1 (OP_strict: FAIR's recorded verdicts, B = 9). Its numbers are `s1` in `k0.json`.
- **Grid point:** one of the 30 points of §4.3. Its numbers are one entry of `points` in `k0.json`: R_sup, P_sup and `sft_sha256`.
- **R_sup and P_sup:** K0's supervision recall (a per-image mean) and precision (a ratio of sums) at the `sft_caption` stage (§4.5; the header of `scripts/o31/src/o31/gate.py`). Both are percentages on the 0 to 100 scale that `gate.funnel` writes (R = 100 × the mean of the per-image recalls), so "1.0 point" in E4-3 is 1.0 percentage point. In `k0.json` they are the keys `R` and `P` of `s1`, of each entry of `points` and of `decision.op_star` and `decision.op_mid`; the store sha256 is the key `sft_sha256` of each.
- **OP\* and OP_mid:** as §4.5 and ERRATUM_O31_1 E7, from the decision in P1's `k0.json`.
- P1's `k0.json` is the K0 output that carries the K0 verdict (`"complete": true` and a `decision` that is not null; ERRATUM_O31_1 E7); `ops5.json` is computed from that file only. Every value is read from it as the IEEE-754 double that `json.loads` returns, and every target, difference and comparison below is computed in that arithmetic in the order written (t25 = a + 0.25 × (b − a)); an exact tie in that arithmetic goes to the tie rules of E4-2.

## E4-2. The rule that picks OP_25 and OP_75 (a pure function of P1's `k0.json`)
1. If K0 FAILs, no point is picked and the result is NOT RUN.
2. Let a = R_sup of the S1 store and b = R_sup(OP\*). The targets are t25 = a + 0.25 (b − a) and t75 = a + 0.75 (b − a).
3. The eligible points are all 30 grid points, whether or not they meet P_floor, except any point whose `sft_sha256` equals that of the S1 store, of OP\* or of OP_mid (byte-identical stores may occur in the grid).
4. OP_25 is the eligible point with the smallest |R_sup − t25|. Ties go to the higher P_sup, then to the earlier grid point in the order of ERRATUM_O31_1 E7.
5. A point whose `sft_sha256` equals that of OP_25 is then also not eligible, and OP_75 is picked in the same way for t75.
6. If no point is eligible at step 4 or at step 5, the result is NOT_IDENTIFIED.

## E4-3. The five points, and when they are identified
- The five points are OP_strict (= S1), OP_25, OP_mid, OP_75 and OP\*. They are put in ascending order of their R_sup values, equal values in the label order just given. This order, not the labels, defines the four adjacent pairs; both orders are reported.
- If two adjacent R_sup values in that order differ by less than 1.0 point, the result is NOT_IDENTIFIED. The constant 1.0 is fixed here, before any `k0.json` exists.
- Otherwise the result is IDENTIFIED.
- The result, the two picked points and the five R_sup and P_sup values with their store sha256 are written once to `ops5.json`, from P1's `k0.json` and nothing else, by code that has its own code read. Its sha256 is recorded before any training of a student at OP_25 or OP_75. `k0.py` and `gate.run_k0` are not changed.

## E4-4. What the result allows
- **IDENTIFIED:** a later erratum, committed before the first G3 output, may train and evaluate students at OP_25 and OP_75 and may register the test of E4-7 across the five points. Without such an erratum, the five points are a reported row only.
- **NOT RUN or NOT_IDENTIFIED:** under no later erratum is a student trained at OP_25 or OP_75, a test run across the five points, or a table of student results across the five points offered. The content of `ops5.json` is reported in every case.
- A-1 stays as registered in every case.

## E4-5. Reporting row: is OP\* at the edge of the grid?
- OP\* is at the edge iff τ_acc(OP\*) ∈ {0.50, 0.90} or τ_rej(OP\*) ∈ {0.10, 0.30}. The position is reported from P1's `k0.json`, whatever it is.
- The paper states an edge OP\* as a limitation: the best point may lie outside the grid.
- The row is descriptive, with no rule, and changes no registered element.

## E4-6. Text left as it was
- These stay as registered: §4.3 (the grid); §4.5 (K0, P_floor, OP\*, OP_mid, the 47.1 bar and the dose-response points); ERRATUM_O31_1 E7 (the tie rules, and OP_mid chosen over all 30 points); A-1; H1 to H5; the families; the tiers; and the stop rules K0 to K6.
- No rule here reads P0r's preview, and P0r stays a preview with no verdict (ERRATUM_O31_1 E7).
- Everything else in the prereg, ERRATUM_O31_1, ERRATUM_O31_2, ERRATUM_O31_3 and COMPUTE_PLAN v3 is unchanged.

## E4-7. The form of any later test across the five points, and its place in a family
- A test across the five points that a later erratum registers is T-4 in exactly this form, at tier 2, on the seed-42 students at the five points. Predicted direction: R increases with R_sup, where R is the §5 object recall at tier 2 on the gold of ERRATUM_O31_1 E11.
  - For each adjacent pair k = 1 … 4 in R_sup order (E4-3): Δ_k = R(point k+1) − R(point k).
  - V_k is the variance of Δ_k over the B = 10,000 shared replicates (the paired image bootstrap of §6.3 and ERRATUM_O31_1 E9).
  - σ²_seed is the pooled between-seed variance of R, the mean of the sample variances (with n − 1 in the denominator) of S1's three and S2's three tier-2 per-seed R values on the full tier-2 image list.
  - z_k = Δ_k / sqrt(V_k + 2 σ²_seed), and p_k = 1 − Φ(z_k).
  - p_T4 = max_k p_k (intersection-union). A zero denominator makes T-4 NOT_IDENTIFIED.
- If a later erratum places T-4 in a test family, T-4's membership does not depend on `ops5.json` or on any `k0.json` value: if the result of E4-3 is NOT RUN or NOT_IDENTIFIED, or T-4 itself is NOT RUN or NOT_IDENTIFIED, T-4 stays a member and enters that family's correction with p = 1. No member of that family is added, removed or re-weighted because of `ops5.json` or of any `k0.json` value.
