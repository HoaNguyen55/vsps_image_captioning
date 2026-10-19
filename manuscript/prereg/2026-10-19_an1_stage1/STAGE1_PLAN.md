# A-N1 stage-1 plan (written before stage 1 runs)

- **Written:** 2026-10-19T01:44:19Z (UTC), before any A-N1 measure was computed on any data. The sha256 of this file and
  of `measures.py` are recorded in `MANIFEST.json` before the stage-1 run. The run writes its own start and end times
  into `stage1_results.json`.
- **Authority:** judge PD-16 (preliminary), item 3(a): the measure, statistic, prediction and verdict rule are frozen after
  stage 1, before any G2-B data are touched. This plan names the candidates and the rule for choosing among them.
- **Status of everything stage 1 produces:** EXPLORATORY. XM3600's registered C2 verdicts do not cover these statistics
  (PD-16, item 2).

## 1. Candidates (definitions in DESIGN.md §2)

1. **cF1**, condensed F1 over the judged pool J = G ∪ (N \ G).
2. **bpref_set**, bpref in the trec_eval form, on an unordered mention set taken in random order.

F1 (registered mixed F1) is the baseline. The infAP-style estimator is not a candidate (DESIGN.md §2, D1 and D8).

## 2. Data (already scored in Paper A; read through `score_g2b.py`, imported unchanged)

| Set | Systems | Images | Lexicon | Levels (one_ref, all_refs, complete) | N_i |
|---|---|---|---|---|---|
| COCO-2500 | the 9 systems of the selfcheck (coco5000, coco_transfer, coco5000_vcd shards) | 2,500 (`data/coco_probe/manifest.json`) | coco80 | refs1_randk, refs_all, inst | U80 \ inst_i |
| UIT-ViIC test | the 10 systems of the selfcheck (`all_10`) | test ids of `uitviic_context()` | coco80 (primary) | refs1_randk, refs_all, inst | U80 \ inst_i |
| XM3600 | the 6 systems of the selfcheck | the 600 of `xm3600_context()` | objects_in | refs1_randk, refs_all, oiv7_verified | OIV7 `absent` |

- Random reference draws: `score_g2b.random_subsets` with the registered `n_random_subsets` and `subset_seed`, over each
  set's own image list (k = 1 only).
- Bootstrap: the registered image bootstrap, `default_rng(bootstrap_seed).multinomial(n, 1/n, size=n_boot)`, with
  percentiles `ci_lo_percentile` and `ci_hi_percentile`. All values are read from the prereg JSON.
- All images are used, as in the three reference files. Stage 1 applies no clean-subset filter.
- **Data-path check:** before any new number is used, the raw F1 slope of every `slope` cell of
  `data/results/g2b/selfcheck.json` is recomputed through the stage-1 data path and must agree with the cell's
  `reproduced` value to within 0.005.

## 3. Choice rule (applied in code by `measures.py stage1`; the constants are in `measures.py`)

For candidate μ and set d, ρ_μ,d = Range_μ / Range_F1 (point estimate), and the shrink is s_μ,d = 1 − ρ_μ,d.

1. **Admissible:** Range_μ has a finite point estimate on all three sets.
2. **Score:** S_μ = min over the three sets of s_μ,d.
3. **Primary measure:** the admissible μ with the larger S_μ. If |S_cF1 − S_bpref| < 0.05, cF1 is chosen: it is the
   simpler measure and equals F1 under complete gold.
4. **Early stop (kill):** if s_μ*,d ≤ 0 on 2 or more of the 3 sets, no addendum is drafted, and the result is reported to
   main as a negative.
5. **Threshold θ:** the largest, over the three sets, of the 97.5th bootstrap percentile of ρ_μ*,d. It is rounded up
   to the next multiple of 0.05 and capped at 1.0. If a percentile is undefined, θ = 1.0.
6. **Primary statistic for G2-B:** Q = θ · Range_F1 − Range_μ* on the LADDER family. The verdict is the prereg rule
   `sign_gt_0` with the prereg bootstrap. The other candidate is reported as descriptive only, with no verdict.

## 4. Outputs

`stage1_results.json`: per set, the slopes at each level, Range, ρ and Q at θ = 1 with CIs, for F1, cF1 and bpref_set.
It also gives the diagnostics: the share of mentions that are unjudged per level, the conflicts at all_refs (D6), the
number of images without verified negatives (D2), and the result of the data-path check. The output ends with a `choice`
block computed by the rule above.
