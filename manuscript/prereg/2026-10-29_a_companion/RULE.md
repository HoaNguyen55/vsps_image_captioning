# Companion registration to PASCAL-50S: few-reference extrapolation (X1, X2) and the salience excess (X4, X5), Paper A (2026-10-29)

- **prereg_id:** `2026-10-29_a_p50_companion`. Directory `manuscript/prereg/2026-10-29_a_companion/`.
- **Status:** REGISTERED on its joint commit with P50 (`manuscript/prereg/2026-10-28_pascal50s/PREREG.md`, prereg_id `2026-10-28_a_p50_kladder`), with `scripts/pascal50s/p50x.py`, the edited job and SHA256SUMS, before the first output of any P50 run (CC-158 W1). A commit at or after the first output makes it POST_HOC.
- **Rulings:** CC-158 ruling 1, W1, W2, W3, W8; CC-159 rulings 1–6, W2, W5–W8. Source design: `manuscript/pivots/2026-10-29_A_pivots.md` Options 1 and 2.
- **Hold:** P50 does not start before this joint commit. If it has not landed by 11-08 12:00Z, P50 may run only with a judge-read job version without the p50x lines, and X1–X5 are lost on PASCAL-50S (CC-159 ruling 4). P50's cap (8 GPU-h) and cutoff (11-16 12:00Z) do not move.
- **What this file does not change:** every P50 rule, verdict and branch text (P50 §3–§9) stands as registered. P50-A4 and P50-O2 keep "no correction" (CC-144 ruling 6). §5 below adds a family-wise reading next to them; it never re-scores them.

## 0. What the authors saw before writing

- Spent sets only (dev role), decided outputs: A-N2 uv231en and cv295 (16 runs), COCO-5000 (9 runs). Dev check: `scripts/a_x1_devcheck/devcheck.py`, result `.session_backup/2026-10-29/a_x1_devcheck/devcheck_result.json`, drop rule written first: `.session_backup/2026-10-29/a_x1_devcheck/DROP_RULE.md`.
- `pascal50S.json` structure only, through the unchanged `p50.py refcheck` (laptop, scratch dir, sha256 and size checked against the pin, file deleted at once; departure from P50 §6 ("on the m3-role machine only") and §11, disclosed in P50 §0; accepted as a disclosed deviation, CC-159 ruling 6): 1,000 keys, pattern `9999_999999.jpg`, `records_image_id` shape, 1,000/1,000 matched 1:1, **50 references for every image** (`.session_backup/2026-10-29/a_x1_devcheck/p50_refcheck_local.json`). No reference text was printed or stored. Whether the 5 UIUC captions are among the 50 is unknown and not needed.
- No P50 output exists. Nothing on PASCAL-50S was decoded.
- Prior-art sweep (W3): `.session_backup/2026-10-29/a_x1_devcheck/prior_art_W3.md`.

## 1. Data, runs, golds (all inherited from P50, unchanged)

- Images: the 1,000 P50 ids; analysis set = P50 §3.3 (clean in every run of every kept model).
- **Runs (pre-fixed count):** the X family is exactly P50's family ALL: the runs of the models kept by P50 `plan.json` after the smoke and the 8 GPU-h cap (P50 §2, §6), minus any model that leaves by FAULT before `score`. It is fixed by `plan.json` and the ledger before the look and is never chosen afterwards. n_X = its size (at most 16).
- Matcher `score_coco_probe.en_classes`, COCO-80; V20 table of P50 §4.2.
- Reference draw: P50 §3.2 unchanged (`default_rng(1)`, k in (1, 2, 5, 10, 20), r = 20). The k = 5 rung's 20 subsets are the X1/X2 input; refs50 = all 50 references. No new draw is made for X1/X2.
- Bootstrap: P50 §3.3 weights, `default_rng(0).multinomial(N, [1/N]*N, size=1000)` over the analysis set, paired and shared by every statistic here. Image-level.
- Precision P_x(G) = 100 · Σ_i |m_xi ∩ G_i| / Σ_i |m_xi| (the P of `score_g2b.scores`), mean over the subsets.

## 2. Option 1: few-reference extrapolation (X1, X2)

### 2.1 Frozen estimator (chosen on dev only; W2)

- For run x and k = 5 subset s: for every class c the output mentions on image i, y_ic = number of the 5 drawn references naming c. Pooled over images: TP_obs = #{y >= 1}, Q1 = #{y = 1}, Q2 = #{y = 2}.
- **Form 1 (frozen): first-order jackknife,** TP_hat = min(TP_obs + Q1 · (T−1)/T, M_x), T = 5. P_hat = 100 · TP_hat / M_x, then the mean over the 20 subsets.
- Why jackknife-1 (chosen on dev, descriptive here): on MAE it beat the better trivial correction in every k = 2 → refs5 cell (uv231en −2.62 pp [−3.35, −1.76]; cv295 −4.43 [−5.26, −2.52]; COCO-5000 −2.71 [−3.26, −2.11]), where Chao2 did not (uv231en +3.91 [+2.42, +5.34]).
- **Dev losses (reported in full):** jackknife-1 LOST to the better trivial correction in every k = 3 → refs5 cell (uv231en +2.40 [+1.07, +3.12]; cv295 +2.72 [+1.40, +3.37]; COCO-5000 +2.78 [+2.48, +3.05]) and at uv231en k = 2 → inst ∪ refs5 (+6.88 [+4.80, +9.50]). At the closest analog of P50's 10× extrapolation (k = 5 → inst ∪ refs5) it is −1.35 [−2.01, +0.73] on uv231en (CI spans 0; p 0.095) and −2.35 [−2.83, −1.58] on cv295. All dev numbers come from spent sets (uv231en is the spent UIT-ViIC test set, used under CC-158 W2) and are post hoc / exploratory; they never support a confirmatory claim (CC-159 ruling 6).
- X1 is NOT_EVALUABLE if any X run has M_x = 0 (there is no fallback form).
- Trivial comparators (both rank-preserving up to the 100% cap): (i) **pooled-uniform**: one factor per subset and bootstrap column, computed with the Chao-2014 incidence extrapolation to K = 50 (not with jackknife-1) on TP, Q1 and Q2 pooled over all runs, then applied to every run's raw precision (`p50x.precisions`); (ii) **Ḡ-ratio**: P_x(refs5) · Ḡ(refs50)/Ḡ(refs5), capped at 100.
- Truth: P_x(refs50), called "50-reference consensus", never "complete gold".

### 2.2 Status after the W2 drop rule (read before §2.3)

The drop rule (written before any statistic) has two legs on uv231en, 16 runs:
- **R1 did not fire:** raw few-reference ranks are not the truth ranks: tau_b(raw k = 5, inst ∪ refs5) = 0.817 (cv295 0.833, COCO-5000 0.722). At k = 2 → refs5 the raw tau_b is 0.950 (cv295 0.983).
- **R2 fired:** no estimator raised tau_b. Jackknife-1 minus raw: +0.033 [−0.033, +0.067] (k = 2 → refs5), −0.006 [−0.136, +0.067] (k = 5 → inst ∪ refs5). Chao2: 0.000 and −0.083. Jackknife-1 beat the trivial corrections on MAE (above; and −1.35 [−2.01, +0.73] at k = 5 → inst ∪ refs5).
- Cause seen on dev: the cap at M_x ties six short runs at 100%, and the truth ranking is mostly short vs detailed, which raw already gets right.

**Ruling: X1 and X2 are DESCRIPTIVE (CC-159 rulings 1–2).** They are reported with CIs and carry no verdict, and neither enters any Holm reading. `p50x.py` fixes `RESTORE_X1 = False`; X2 has no confirmatory path.

### 2.3 Descriptive statistics (no verdict)

| ID | Statement | Statistic |
|---|---|---|
| **X1** | The jackknife-1 extrapolation from k = 5 is closer to the refs50 precision than the better trivial correction | D1 = MAE_jack1 − min(MAE_(i), MAE_(ii)) over the X runs (pp), with CI and one-sided bootstrap p; the `sign_lt_0` outcome is printed as descriptive only |
| **X2** | Ranking runs by the extrapolated k = 5 precision agrees with refs50 more than raw k = 5 does | D2 = tau_b(P_hat, P(refs50)) − tau_b(P(refs5), P(refs50)), with CI, p and the number of runs |

- X2 is numbers only. For reading them: on cost, the 8-of-13 GPU-h projection leaves about 8–10 runs; on dev, raw tau_b at the k = 5 analog was 0.817.
- X1's descriptive outcome is NOT_EVALUABLE if any X run has M_x = 0 or n_X < 6.
- Optional descriptive (no verdict): X3 = X1 with voc20 as truth on V20; per-run P_hat, Q1, Q2.

## 3. Option 2: the salience excess (X4, X5)

**Label: within-mention mechanism.** It tests which objects people mention, not how many. It is worded as **excess versus the size-matched null**. It is not a replication of Table S7.1 (that used a label gold; X5 is its analog).

### 3.1 Null (SCAR_DESIGN reused, gold swapped)

- Complete gold C_i and level golds G_L,i as below. k_i^(s) = |G_L,i^(s) ∩ C_i| per registered subset s (from the P50 draw, no fresh draw).
- Each replicate: one uniform permutation per image of sorted(C_i); subset s keeps the first k_i^(s) classes. Shared by every run.
- R = 1000, one `numpy.random.default_rng(0)` stream, consumed in the order prediction (X4, X5) → level → replicate → image (P50 id order, all 1,000 images; the analysis set is applied when scoring).
- Statistic: `score_g2b.stat_slope` (OLS slope of 100·F1 on ln M over the X runs), imported unchanged; F is the subset mean.
- Observed: the same statistic on G_L ∩ C. Excess = observed − null mean.

### 3.2 Predictions

| ID | Complete gold C | Levels | Rule |
|---|---|---|---|
| **X4** (co-primary) | refs50, COCO-80 | refs1_randk and refs5_randk (here refs_k ⊆ refs50, so G_L ∩ C = G_L) | each level: PASS if observed < null 2.5th percentile; FAIL if observed >= null median; else INCONCLUSIVE. `compound` over the two levels |
| **X5** (co-primary where evaluable) | voc20, V20 vocabulary (P50 §4) | refs1_randk on V20 | same rule |

- **X5 NOT_EVALUABLE** (pre-written): the label rung was dropped under P50 §4.4; or P50's `not_evaluable` fires on the V20 family; or Σ_i |voc20_i| over the analysis set < 2 · Σ_i k_i, where Σ_i k_i is the mean over the 20 registered subsets of Σ_i k_i^(s) (fewer than one deletable class per kept class, so the null cannot move); or the null's 2.5 and 97.5 percentiles are equal.
- **X4 NOT_EVALUABLE** at a level if the null's 2.5 and 97.5 percentiles are equal (k_i = |refs50_i| almost everywhere), or by P50's `not_evaluable`.
- Sign fixed in advance by the 8/8 exploratory direction of Table S7.1 (`data/results/scar/scar_null_result.json`).
- Optional descriptive (no verdict): sign of the b-channel share by run (sec4 Λ split).

## 4. p-values (for Holm only; verdicts stay as in §2–§3)

- Bootstrap statistics (the P50-A4/A4r and P50-O2 parts; X1 and X2 are printed with the same rule, descriptive only): one-sided p = (1 + #{b : stat_b <= 0}) / (B + 1) for a `sign_gt_0` statistic (for X1, #{D1_b >= 0}), B = 1000, the shared weights.
- Null statistics (X4, X5): p = (1 + #{r : null_r <= observed}) / (R + 1), R = 1000.
- A compound's p is the largest p of its parts.

## 5. Family and multiplicity

- **Companion confirmatory family:** {X4, X5} (CC-159 ruling 2). NOT_EVALUABLE members leave the family before the correction.
- **Holm** at one-sided α = 0.025 over that family. A member PASSes only if its §2–§3 verdict is PASS **and** it survives Holm; otherwise its verdict stands and "not significant after Holm" is written next to it.
- **Family-wise reading (CC-158 W1), descriptive:** Holm over {P50-A4 or P50-A4r, P50-O2, X4, X5} only (CC-159 W8; X1 and X2 never enter) is reported in one table next to the registered P50 verdicts, which are not changed.
- Kill rule: none. Counting as G2B `counting` (INCONCLUSIVE is never support).

## 6. Where it runs (this edits P50's commit set; disclosed)

- P50 §6 deletes `pascal50S.json`, the images and the raw decodes on the m3-role machine right after `score`. X1–X5 need per-reference incidence and refs50, so they **cannot** be computed later from the copied predictions.
- Therefore: a new evaluator `scripts/pascal50s/p50x.py` (selftest on synthetic data; numbers only) runs inside `scripts/pascal50s/p50_job.sh` **after `p50.py score` and before the delete step**, reading the same `score` inputs and the same draw. Its read of the outputs is part of P50's one look (§7 of P50); it refuses if its own decide file exists.
- The job edit, `p50x.py`, its sha in `SHA256SUMS`, and this file go in the same gatekeeper commit as the P50 PREREG. The 8-gram check (P50 §6 W4) covers `p50x_decide.json` before it leaves the m3-role machine.
- **Fault rule (CC-159 W2, fixed before the look):** P50's decide file is 8-gram-checked and copied out before p50x runs; once it exists the cutoff never fires. p50x gets at most 2 attempts, counted in EVENTS; after the second failure, or on an 8-gram hit in its decide file (that file stays on the machine and is deleted with the data), the companion is recorded as `{"status": "FAULT (code): companion not run"}` and the deletion proceeds. An empty analysis set gives a NOT_EVALUABLE record. The stub test `scripts/pascal50s/test_p50_job_paths.sh` exercises these paths.
- No extra GPU-h. CPU cost: about 0.57 s per null replicate at full scale (CC-159 timing), so about 10 min for R = 1000.

## 7. Branch texts (written before any output)

- **X4 PASS (± X5 PASS):** "On 1,000 PASCAL-50S images with 50 references each, the slope of object F1 on ln M under [1 / 5] reference(s) lay below the 95% range of a size-matched random-deletion null drawn from the 50-reference consensus (excess [value]; registered; Holm-adjusted across [family]). This is consistent with reference gold penalising verbose captions through which objects people mention, not only how many; it is a within-mention mechanism test, not proof of cause."
- **X4 FAIL:** "The registered salience excess did not appear on PASCAL-50S: the observed slope was at or above the null median ([value]). The 8/8 exploratory pattern of Table S7.1 does not replicate on a reference-derived complete gold."
- **Not testable:** "[X4/X5] could not be evaluated: [reason]. It carries no result."
- **X1/X2 descriptive (default):** "As a descriptive check, a jackknife extrapolation from 5 references moved precision closer to the 50-reference value by [D1] pp on average; it [did / did not] change the run ranking (tau_b [raw] → [extrapolated]). This was not a registered test."

## 8. Nearest work (W3; full list in prior_art_W3.md)

- Incomplete relevance judgments in IR: Buckley & Voorhees 2004 (bpref, tolerates missing judgments, does not estimate); Yilmaz & Aslam 2006 (infAP) and Aslam et al. 2006 (statAP), which need a designed sample of new judgments; Zobel 1998.
- **Closest IR precedent: Zobel 1998** (doi:10.1145/290941.291014), a parametric extrapolation of the count of unfound relevant items over pool depth and system count, with no corrected per-system metric.
- Trushkowsky et al. 2013 apply species estimators (Chao92 / jackknife) to crowd answer lists to estimate set size, not a metric (per the arXiv preprint 1202.2335; the ICDE full text was not read).
- Rohrbach et al. 2018 (with Feng et al. 2024, arXiv 2406.12663, and POPE 2023) already report that caption-only gold inflates hallucination scores. X4's addition is the size-matched random-deletion null, and nothing more. HaloProbe (arXiv 2604.06165): no unseen-gold estimate.
- Vedantam et al. 2015 and Misra et al. 2016 are described from prior knowledge, not re-read; both are re-read before any sentence about them enters paper text. Berg et al. 2012 and Llerena & Jung 2025 as listed in `prior_art_W3.md`.
- **No "first" claim** anywhere, in this file or in the paper (CC-159 ruling 5). Positioning sentence: *Unlike pool-depth extrapolation in IR (Zobel, 1998), which estimates how many relevant items exist, and unlike sampling-based estimators (infAP, statAP), which need new judgments, we correct each system's object precision from the incidence of its own mentions across the references already collected, and check it against a 50-reference consensus never used to fit it.*

## 9. Dev evidence for X4 (closed item)

- X4 dev analog (complete gold = refs5, A-N2, 16 runs, R = 1000; `.session_backup/2026-10-29/a_x1_devcheck/x4_dev_analog.json`; post hoc, spent sets): observed below the null 2.5th percentile in all 4 cells, p = 0.001 each: uv231en refs1 −15.6 vs [−1.8, +4.3], refs2 −4.8 vs [+3.8, +8.1]; cv295 refs1 −25.1 vs [−18.3, −14.3], refs2 −19.0 vs [−14.4, −11.3]. The k = 5-of-50 level has no direct dev analog.
