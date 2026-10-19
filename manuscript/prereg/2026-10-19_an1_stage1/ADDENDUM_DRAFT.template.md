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

- **When.** DESIGN.md and STAGE1_PLAN.md (plan time {{ad:stage1_record.plan.written_utc}}) were written first. Their sha256, with that of
  `measures.py`, were recorded at {{ad:stage1_record.pre_stage1_hashes.recorded_utc}} in `pre_stage1.sha256`. The stage-1 run then went from
  {{s1:started_utc}} to {{s1:finished_utc}}, with `measures.py` sha256 {{s1:measures_py_sha256}} at HEAD
  {{s1:code_at_head}}.
- **Data.** These are data already scored in Paper A, read through `score_g2b.py`:
  - COCO-2500: {{s1:sets.COCO-2500.n_images}} images, the {{s1:sets.COCO-2500.systems|len}} selfcheck systems, coco80;
  - UIT-ViIC test: {{s1:sets.UIT-ViIC test.n_images}} images, the {{s1:sets.UIT-ViIC test.systems|len}} selfcheck systems, coco80;
  - XM3600: {{s1:sets.XM3600.n_images}} images, the {{s1:sets.XM3600.systems|len}} selfcheck systems, objects_in with OIV7.

  All images were used. The levels were refs1_randk, refs_all and the complete gold, with the registered random draws and
  bootstrap.
- **Data-path check.** Every `slope` cell of `data/results/g2b/selfcheck.json` for these families was recomputed through
  the stage-1 path and agreed (`sets.*.data_path_check`).

{{TABLE}}

- **Choice rule result (STAGE1_PLAN.md §3, applied in code).** The rule selected **bpref_set**: its minimum shrink was
  {{s1:choice.score_min_shrink.bpref|.3f}}, against {{s1:choice.score_min_shrink.cF1|.3f}} for cF1. Its θ was
  {{s1:choice.theta}}. The kill did not fire.
- **Diagnostic, run after the choice was seen** (`stage1_diag.py`, disclosed here). bpref_set is almost entirely recall.
  The median of bpref_set / R over systems and levels was:
  - COCO-2500: {{dg:sets.COCO-2500.bpref_over_R_median|.3f}} (minimum {{dg:sets.COCO-2500.bpref_over_R_min|.3f}});
  - UIT-ViIC test: {{dg:sets.UIT-ViIC test.bpref_over_R_median|.3f}} (minimum {{dg:sets.UIT-ViIC test.bpref_over_R_min|.3f}});
  - XM3600: {{dg:sets.XM3600.bpref_over_R_median|.3f}} (minimum {{dg:sets.XM3600.bpref_over_R_min|.3f}}).

  Its larger shrink therefore comes mostly from dropping precision, which carries most of the gold-level dependence. This
  is a near form of degenerate case D1 that the plan's rule did not screen for.
- **Deviation (proposed; the judge rules, §8).** cF1 is frozen as the primary measure, with θ from the plan's θ rule
  applied to cF1. The reasons are:
  - cF1 keeps a precision term;
  - it equals the registered F1 under complete gold;
  - its stage-1 ρ is larger, so the deviation makes the registered test harder, not easier.

  bpref_set becomes descriptive. If the judge keeps the rule's choice, `primary` takes the values in
  `alternative_if_rule_kept` of the JSON. No code changes, because the scripts read the measure and θ from the JSON.
- **Other stage-1 facts:**
  - Under both measures the one-reference slope is positive on all three sets (table). The negative one-reference F1
    slope therefore depends on scoring unjudged mentions as errors.
  - On XM3600, {{s1:sets.XM3600.diagnostics.images_without_negatives}} of {{s1:sets.XM3600.n_images}} images carry no
    verified negative (D2).
  - On COCO-2500, {{s1:sets.COCO-2500.diagnostics.conflict_pairs_all_refs}} of
    {{s1:sets.COCO-2500.diagnostics.positive_pairs_all_refs}} reference positives at all_refs are classes that the
    instance gold marks absent (D6, positive wins).

## 3. The registered test (frozen here)

- **Primary measure:** {{ad:primary.measure}}. **Statistic:** Q = θ · Range_F1 − Range_cF1, with θ = {{ad:primary.theta.value}}.
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
- **Bootstrap:** the prereg `analysis_plan.bootstrap`: `default_rng({{pr:design_constants.set_by_this_registration.bootstrap_seed}})`,
  {{pr:design_constants.n_boot.value}} multinomial image draws over the clean LADDER subset in id order. These are the same
  draws as the G2-B primary analyses on that subset. Percentiles are
  {{pr:design_constants.ci_lo_percentile.value}} and {{pr:design_constants.ci_hi_percentile.value}}. The random reference
  draws are those of `score_g2b.Dataset` (subset seed {{pr:design_constants.set_by_this_registration.subset_seed}}).
- **Descriptive, without verdict:**
  - the slopes per level, Range and ρ for F1, cF1 and bpref_set;
  - bpref_set's Q at the same θ;
  - the unjudged shares, D2 counts and D6 counts.

## 4. Scope (PD-16, item 4; binding 3)

- **All three G2-B sets overlap the stage-1 images and golds.** CV295 is part of COCO-2500, XM600 is the XM3600 set of {{s1:sets.XM3600.n_images}} images, and
  UV231 is UIT-ViIC test. This test is therefore a NEW-BACKBONE test (Qwen3-VL-8B, the G2-B LADDER) on development images.
  It is NOT an image-out-of-sample test, and Paper A says so wherever it reports the result.
- **UV231** follows the prereg `exposure.uv231_handling`:
  - its images are COCO train2017 images;
  - a FAIL there counts;
  - a PASS there is never counted as support.

## 5. Outcome rule and consequences (applied in code, `score_an1.outcome`)

The outcome is the first of these that applies:
- **NOT_TESTABLE:** no set has a PASS, FAIL or INCONCLUSIVE verdict.
- **NOT_SUPPORTED:** {{ad:outcome_rule.not_supported_min_fail_sets}} or more sets are FAIL (uv231 counts).
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
- all {{pr:runs|len}} decodes;
- the CC-027 (b) provenance check (KD, through `score_g2b.load_runs`);
- the clean subsets (KL);
- main's go for scoring (CC-027 (c)).

`python3 score_an1.py score --addendum <committed JSON> --outputs-dir <G2-B outputs> --out <new file>` refuses to run in
any of these cases:
- a pin differs: score_g2b.py, the prereg, its frozen files, measures.py or score_an1.py;
- score_an1.py, measures.py or the addendum JSON is not committed and unchanged at HEAD;
- any of the {{pr:runs|len}} registered outputs or sidecars is missing;
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
- **Open models only:** Qwen3-VL-8B-Instruct, licence {{pr:model.licence}}.

## 8. For the judge

- **(a)** Keep the plan's choice (bpref_set, θ {{s1:choice.theta}}) or accept the proposed deviation (cF1, θ
  {{ad:primary.theta.value}}).
- **(b)** Accept the verified-negative levels as the only levels where the measures apply (D1), and the constructed
  "references + N" levels on coco80 (D6, positive wins).
- **(c)** Accept the outcome rule and its body-only placement.
- **(d)** Accept the proposed commit paths in the JSON.
