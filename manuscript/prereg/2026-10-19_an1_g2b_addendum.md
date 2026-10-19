# A-N1 scoring addendum to the G2-B prereg (DRAFT): object measures robust to incomplete gold, a registered secondary analysis

- **Parent registration:** `manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.{md,json}` (0932ba1). The JSON's sha256 is
  given in §7.
- **Status:** DRAFT for the judge's final PD-16 ruling. The analysis is REGISTERED only if this addendum, `measures.py` and
  `score_an1.py` are committed before the A-N1 statistic is first computed on G2-B data, and only if the committed
  `score_an1.py` computes it (PD-16, item 1, D-W13-6).
- **What it does not change:** no G2-B primary or secondary test, verdict rule, kill rule, family or gold; not
  `score_g2b.py`, the G2-B prereg or the confirmation map. All three stay byte-identical. The A-N1 verdict is a
  **registered secondary** result. It appears in the body only, never in the abstract or the conclusions as
  confirmatory (map §6; PD-16, item 1).
- **G2-B outputs read by this addendum:** none. The only file read under `data/results/g2b/` is `selfcheck.json`.

## 1. Question and measures (definitions in DESIGN.md)

Paper A shows that the verbosity reward of object F1 (its slope on ln M) depends on gold completeness. IR calls this
problem incomplete judgments, and handles it with measures that use only judged documents:
- condensed lists (Sakai 2007, doi:10.1145/1277741.1277756);
- bpref (Buckley and Voorhees 2004, doi:10.1145/1008992.1009000);
- infAP (Yilmaz and Aslam 2006, doi:10.1145/1183614.1183633).

The mapping is: image = topic, mention set = retrieved set, gold positives = judged relevant, verified negatives =
judged non-relevant, any other mention = unjudged. The verified negatives N_i are U80 \ inst_i on coco80, and the OIV7
`absent` labels on XM600. They are the same at every gold level. Each level's judged pool is G ∪ (N \ G).

- **cF1:** F1 with the unjudged mentions removed from precision. Recall is unchanged. Under complete coco80 gold it equals
  the registered F1 exactly. At oiv7_verified it is defined as the registered F1, whose precision is already condensed
  (DESIGN.md D3).
- **bpref_set:** bpref in the trec_eval min(R, N) form, on a mention set taken in random order.
- **Degenerate case D1:** with references alone there are no negatives, and both measures reduce to functions of recall.
  They are therefore not applied to any level without verified negatives. The infAP-style estimator, with all mentions
  pooled, is condensed precision (DESIGN.md §2). It is not a separate candidate.

## 2. Stage-1 record (EXPLORATORY)

- **When.** DESIGN.md and STAGE1_PLAN.md (plan time 2026-10-19T01:44:19Z) were written first. Their sha256, with that of
  `measures.py`, were recorded at 2026-10-19T02:05:42Z in `pre_stage1.sha256`. The stage-1 run then went from
  2026-10-19T02:05:46Z to 2026-10-19T02:06:02Z, with `measures.py` sha256 c41fe6d98dcf33719545e1dc3ed1d9999b3b6395f0de11c97e4219137f354ac6 at HEAD
  cbed6dbc88b80ee0dc92f5891d82af0ce7772060.
- **Data.** These are data already scored in Paper A, read through `score_g2b.py`:
  - COCO-2500: 2500 images, the 9 selfcheck systems, coco80;
  - UIT-ViIC test: 231 images, the 10 selfcheck systems, coco80;
  - XM3600: 600 images, the 6 selfcheck systems, objects_in with OIV7.

  All images were used. The levels were refs1_randk, refs_all and the complete gold, with the registered random draws and
  bootstrap.
- **Data-path check.** Every `slope` cell of `data/results/g2b/selfcheck.json` for these families was recomputed through
  the stage-1 path and agreed (`sets.*.data_path_check`).

Table S1 (EXPLORATORY). Verbosity slopes (points of 100·measure per unit ln M), their range over the three gold levels, and ρ. Source: `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` (sha256 d70cb94bc3bebae5908b740fa23e7a3290b0585302bff0a7acfee5bb897872d1), keys `sets.<set>.measures.<measure>.{slope, range, rho}` ([point, [2.5%, 97.5%]]).

| Set | Measure | slope one_ref | slope all_refs | slope complete | Range (95% CI) | ρ = Range/Range_F1 (95% CI) |
|---|---|---|---|---|---|---|
| COCO-2500 | F1 | -4.14 | 11.08 | 22.41 | 26.55 (25.34, 27.72) | — |
| COCO-2500 | cF1 | 8.63 | 18.16 | 22.41 | 13.78 (12.89, 14.62) | 0.52 (0.50, 0.54) |
| COCO-2500 | bpref | 17.96 | 25.05 | 27.68 | 9.72 (8.69, 10.75) | 0.37 (0.34, 0.39) |
| UIT-ViIC test | F1 | -15.79 | 4.80 | 37.52 | 53.31 (48.91, 56.95) | — |
| UIT-ViIC test | cF1 | 9.40 | 20.09 | 37.52 | 28.12 (25.15, 30.39) | 0.53 (0.50, 0.55) |
| UIT-ViIC test | bpref | 19.60 | 31.98 | 40.65 | 21.05 (16.25, 25.02) | 0.39 (0.32, 0.45) |
| XM3600 | F1 | -9.30 | -2.43 | 19.32 | 28.62 (26.21, 31.02) | — |
| XM3600 | cF1 | 14.94 | 18.05 | 19.32 | 4.38 (2.89, 6.54) | 0.15 (0.11, 0.21) |
| XM3600 | bpref | 19.73 | 21.76 | 19.96 | 2.03 (1.38, 4.42) | 0.07 (0.05, 0.16) |

- **Choice rule result (STAGE1_PLAN.md §3, applied in code).** The rule selected **bpref_set**: its minimum shrink was
  0.605, against 0.472 for cF1. Its θ was
  0.5. The kill did not fire.
- **Diagnostic, run after the choice was seen** (`stage1_diag.py`, disclosed here). bpref_set is almost entirely recall.
  The median of bpref_set / R over systems and levels was:
  - COCO-2500: 0.977 (minimum 0.885);
  - UIT-ViIC test: 0.994 (minimum 0.916);
  - XM3600: 0.994 (minimum 0.976).

  Its larger shrink therefore comes mostly from dropping precision, which carries most of the gold-level dependence. This
  is a near form of degenerate case D1 that the plan's rule did not screen for.
- **Deviation (proposed; the judge rules, §8).** cF1 is frozen as the primary measure, with θ from the plan's θ rule
  applied to cF1. The reasons are:
  - cF1 keeps a precision term;
  - it equals the registered F1 under complete gold;
  - its stage-1 ρ is larger, so the deviation makes the registered test harder, not easier.

  bpref_set becomes descriptive. If the judge keeps the rule's choice, `primary` takes the values in
  `alternative_if_rule_kept` of the JSON. No code changes, because the scripts read the measure and θ from the JSON.

  PD-16 final (a): bpref_set's Q is now reported per set, descriptively and without a verdict (§3, "Descriptive: bpref_set Q").
- **Other stage-1 facts:**
  - Under both measures the one-reference slope is positive on all three sets (table). The negative one-reference F1
    slope therefore depends on scoring unjudged mentions as errors.
  - On XM3600, 231 of 600 images carry no
    verified negative (D2).
  - On COCO-2500, 761 of
    5191 reference positives at all_refs are classes that the
    instance gold marks absent (D6, positive wins).

## 3. The registered test (frozen here)

- **Primary measure:** cF1. **Statistic:** Q = θ · Range_F1 − Range_cF1, with θ = 0.6.
  - Range_μ is the max minus the min, over the three gold levels `golds.<set>.{one_ref, all_refs, complete}`, of
    slope_μ, where slope_μ is the OLS slope of 100·μ_x on ln M_x over the LADDER family (`score_g2b.stat_slope`).
  - F1 is the registered mixed F1, computed by `score_g2b.scores`.
- **Direction and rule:** Q > 0, under the prereg verdict rule `sign_gt_0`: PASS if ci95_lo > 0; FAIL if the point
  estimate is ≤ 0; otherwise INCONCLUSIVE. NOT_EVALUABLE follows the prereg rule; for example, a LADDER run missing or
  excluded by KD, an empty clean subset, or an undefined slope.
- **Sets:** cv295, xm600 and uv231, each with its primary lexicon (`score_g2b.score`): coco80, objects_in with OIV7, and
  coco80. The uv231 secondary lexicon is not analysed (D7).
- **Images:** the clean subset of LADDER (KL), as for G2B-E1, E2 and O1. The full set is a sensitivity analysis without
  verdict.
- **Bootstrap:** the prereg `analysis_plan.bootstrap`: `default_rng(0)`,
  1000 multinomial image draws over the clean LADDER subset in id order. These are the same
  draws as the G2-B primary analyses on that subset. Percentiles are
  2.5 and 97.5. The random reference
  draws are those of `score_g2b.Dataset` (subset seed 1).
- **Descriptive, without verdict:**
  - the slopes per level, Range and ρ for F1, cF1 and bpref_set;
  - bpref_set's Q at the same θ;
  - the unjudged shares, D2 counts and D6 counts.
- **Descriptive: bpref_set Q (PD-16 final (a)).** Q_bpref = θ · Range_F1 − Range_bpref_set per set, with the
  primary's θ, bootstrap draws, clean LADDER subset, levels and lexicon. Output keys
  `sets.<set>.primary_analysis.descriptive_Q_at_theta.bpref` and `sets.<set>.sensitivity_full_set.descriptive_Q_at_theta.bpref`.
  It has no verdict and enters no verdict, outcome or kill rule.

## 4. Scope (PD-16, item 4; binding 3)

- **All three G2-B sets overlap the stage-1 images and golds.** CV295 is part of COCO-2500, XM600 is the XM3600 set of 600 images, and
  UV231 is UIT-ViIC test. This test is therefore a NEW-BACKBONE test (Qwen3-VL-8B, the G2-B LADDER) on development images.
  It is NOT an image-out-of-sample test, and Paper A says so wherever it reports the result.
- **UV231** follows the prereg `exposure.uv231_handling`:
  - its images are COCO train2017 images;
  - a FAIL there counts;
  - a PASS there is never counted as support.
- **Given verified negatives (PD-16 final (b)).** The claim holds given verified negatives.
  - On CV295 and UV231 the negatives are U80 \ inst_i, the exhaustive complement of the complete gold. cF1 therefore
    carries the complete gold's negatives at every ladder level, and part of the shrinkage on these sets is by
    construction.
  - XM600's OIV7 `absent` labels are not exhaustive: 231 of the
    600 stage-1 XM3600 images carry none (D2). XM600 is therefore the informative set.
  - Conflict rates at all_refs, stage 1: reference positives that the complete gold marks absent, where the positive
    wins (D6). COCO-2500 761 of
    5191; UIT-ViIC test
    2 of
    429; XM3600
    44 of 1409
    (keys `sets.<set>.diagnostics.conflict_pairs_all_refs` and `positive_pairs_all_refs`). The scorer reports the same
    counts for each registered set under `sets.<set>.primary_analysis.diagnostics_all_images`.

## 5. Outcome rule and consequences (applied in code, `score_an1.outcome`)

The outcome is the first of these that applies:
- **NOT_TESTABLE:** no set has a PASS, FAIL or INCONCLUSIVE verdict.
- **NOT_SUPPORTED:** 2 or more sets are FAIL (uv231 counts).
- **SUPPORTED:** cv295 and xm600 are both PASS, and no set is FAIL.
- **MIXED:** otherwise.

INCONCLUSIVE is never support (prereg `verdict_rules.counting`). The consequences are:
- **SUPPORTED.** The §7 body may say: "In a registered secondary test on a second backbone, on development images, the
  gold-level range of the verbosity slope under condensed F1 was below θ times that of F1 on CV295 and XM600." It also
  gives the per-set verdicts and the D1 scope: the measure needs verified negatives. Paper A may then offer cF1 as the
  adoptable measure (A-G1), with that scope.
- **MIXED.** The per-set verdicts are reported verbatim. No general claim is made, and cF1 stays exploratory.
- **NOT_SUPPORTED.** The result is reported as a registered negative, and cF1 is not proposed (A-N1 kill). The IR framing
  stays in the discussion.
- **NOT_TESTABLE.** The paper says that the test was not run or not evaluable.

## 6. Preconditions and procedure

The A-N1 analysis waits for the G2-B preconditions (PD-16, item 1):
- all 23 decodes;
- the CC-027 (b) provenance check (KD, through `score_g2b.load_runs`);
- the clean subsets (KL);
- main's go for scoring (CC-027 (c)).

`python3 scripts/g2b/an1/score_an1.py score --addendum <committed JSON> --outputs-dir <G2-B outputs> --out <new file>` refuses to run in
any of these cases:
- a pin differs: score_g2b.py, the prereg, its frozen files, measures.py or score_an1.py;
- score_an1.py, measures.py or the addendum JSON is not committed and unchanged at HEAD;
- any of the 23 registered outputs or sidecars is missing;
- `--out` exists (no overwrite).

The `dryrun` mode ran the same code path with stage-1 captions standing in for the LADDER runs. It is a code test, not a
result (`dryrun_stage1_standins.json`).

## 7. Instrument items

- **Shas and code at HEAD:** `ADDENDUM_DRAFT.json`, under `code` and `code_at_head`.
- **No overwrite:** every script refuses an existing `--out`. Delivered files are never overwritten (new versions get
  `_v2`).
- **8-gram scan:** `openviic_leak_scan.py` was run on this folder; the result is in `MANIFEST.json`.
- **No Paper-B numbers:** every number here comes from the stage-1 files of this folder, the G2-B prereg or
  `selfcheck.json`. No Paper-B manifest is read.
- **Open models only:** Qwen3-VL-8B-Instruct, licence Apache-2.0.

## 8. For the judge

- **(a)** Keep the plan's choice (bpref_set, θ 0.5) or accept the proposed deviation (cF1, θ
  0.6).
- **(b)** Accept the verified-negative levels as the only levels where the measures apply (D1), and the constructed
  "references + N" levels on coco80 (D6, positive wins).
- **(c)** Accept the outcome rule and its body-only placement.
- **(d)** Accept the proposed commit paths in the JSON.

## Number sources

Every number above that is not in Table S1 comes from this table (sha256 prefix; full values in MANIFEST.json).

| Value | File | sha256 | Key |
|---|---|---|---|
| 2026-10-19T01:44:19Z | `.session_backup/2026-10-19/A-N1_ir_measures/ADDENDUM_DRAFT.json` | fd3804b6542bd2e2 | `stage1_record.plan.written_utc` |
| 2026-10-19T02:05:42Z | `.session_backup/2026-10-19/A-N1_ir_measures/ADDENDUM_DRAFT.json` | fd3804b6542bd2e2 | `stage1_record.pre_stage1_hashes.recorded_utc` |
| 2026-10-19T02:05:46Z | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` | d70cb94bc3bebae5 | `started_utc` |
| 2026-10-19T02:06:02Z | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` | d70cb94bc3bebae5 | `finished_utc` |
| c41fe6d98dcf33719545e1dc3ed1d9999b3b6395f0de11c97e4219137f354ac6 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` | d70cb94bc3bebae5 | `measures_py_sha256` |
| cbed6dbc88b80ee0dc92f5891d82af0ce7772060 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` | d70cb94bc3bebae5 | `code_at_head` |
| 2500 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` | d70cb94bc3bebae5 | `sets.COCO-2500.n_images` |
| 9 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` | d70cb94bc3bebae5 | `sets.COCO-2500.systems|len` |
| 231 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` | d70cb94bc3bebae5 | `sets.UIT-ViIC test.n_images` |
| 10 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` | d70cb94bc3bebae5 | `sets.UIT-ViIC test.systems|len` |
| 600 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` | d70cb94bc3bebae5 | `sets.XM3600.n_images` |
| 6 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` | d70cb94bc3bebae5 | `sets.XM3600.systems|len` |
| 0.605 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` | d70cb94bc3bebae5 | `choice.score_min_shrink.bpref` |
| 0.472 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` | d70cb94bc3bebae5 | `choice.score_min_shrink.cF1` |
| 0.5 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` | d70cb94bc3bebae5 | `choice.theta` |
| 0.977 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_diagnostic.json` | ab3f55c78439af33 | `sets.COCO-2500.bpref_over_R_median` |
| 0.885 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_diagnostic.json` | ab3f55c78439af33 | `sets.COCO-2500.bpref_over_R_min` |
| 0.994 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_diagnostic.json` | ab3f55c78439af33 | `sets.UIT-ViIC test.bpref_over_R_median` |
| 0.916 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_diagnostic.json` | ab3f55c78439af33 | `sets.UIT-ViIC test.bpref_over_R_min` |
| 0.994 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_diagnostic.json` | ab3f55c78439af33 | `sets.XM3600.bpref_over_R_median` |
| 0.976 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_diagnostic.json` | ab3f55c78439af33 | `sets.XM3600.bpref_over_R_min` |
| 231 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` | d70cb94bc3bebae5 | `sets.XM3600.diagnostics.images_without_negatives` |
| 761 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` | d70cb94bc3bebae5 | `sets.COCO-2500.diagnostics.conflict_pairs_all_refs` |
| 5191 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` | d70cb94bc3bebae5 | `sets.COCO-2500.diagnostics.positive_pairs_all_refs` |
| cF1 | `.session_backup/2026-10-19/A-N1_ir_measures/ADDENDUM_DRAFT.json` | fd3804b6542bd2e2 | `primary.measure` |
| 0.6 | `.session_backup/2026-10-19/A-N1_ir_measures/ADDENDUM_DRAFT.json` | fd3804b6542bd2e2 | `primary.theta.value` |
| 0 | `manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.json` | c506bc777b483f50 | `design_constants.set_by_this_registration.bootstrap_seed` |
| 1000 | `manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.json` | c506bc777b483f50 | `design_constants.n_boot.value` |
| 2.5 | `manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.json` | c506bc777b483f50 | `design_constants.ci_lo_percentile.value` |
| 97.5 | `manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.json` | c506bc777b483f50 | `design_constants.ci_hi_percentile.value` |
| 1 | `manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.json` | c506bc777b483f50 | `design_constants.set_by_this_registration.subset_seed` |
| 2 | `.session_backup/2026-10-19/A-N1_ir_measures/ADDENDUM_DRAFT.json` | fd3804b6542bd2e2 | `outcome_rule.not_supported_min_fail_sets` |
| 23 | `manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.json` | c506bc777b483f50 | `runs|len` |
| Apache-2.0 | `manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.json` | c506bc777b483f50 | `model.licence` |
| 231 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` | d70cb94bc3bebae5 | `sets.XM3600.diagnostics.images_without_negatives` |
| 600 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` | d70cb94bc3bebae5 | `sets.XM3600.n_images` |
| 761 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` | d70cb94bc3bebae5 | `sets.COCO-2500.diagnostics.conflict_pairs_all_refs` |
| 5191 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` | d70cb94bc3bebae5 | `sets.COCO-2500.diagnostics.positive_pairs_all_refs` |
| 2 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` | d70cb94bc3bebae5 | `sets.UIT-ViIC test.diagnostics.conflict_pairs_all_refs` |
| 429 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` | d70cb94bc3bebae5 | `sets.UIT-ViIC test.diagnostics.positive_pairs_all_refs` |
| 44 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` | d70cb94bc3bebae5 | `sets.XM3600.diagnostics.conflict_pairs_all_refs` |
| 1409 | `.session_backup/2026-10-19/A-N1_ir_measures/stage1_results.json` | d70cb94bc3bebae5 | `sets.XM3600.diagnostics.positive_pairs_all_refs` |
