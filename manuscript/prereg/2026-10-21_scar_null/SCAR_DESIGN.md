# SCAR random-deletion null for Paper A: design

Status: **POST_HOC, exploratory** (D-W13-6). Authority: PD-23 (d) and PD-23b item 1
(`.session_backup/2026-10-13/decisions/PD-23.txt`, `PD-23b.txt`). It answers mock review R1-F1:
under nested golds, could the ordering of F1's verbosity slope by gold level come from random
missingness alone?

The analysis has no verdict. It never enters the abstract and never changes a registered verdict.
It belongs in sec4/§7 or the supplement, and either result has a reading:
- observed slope close to the null: random incompleteness reproduces the pattern;
- otherwise: which objects annotators name adds to it.

This text was written before any null statistic or intersection-gold slope was computed on real
data. It must be committed before `scar_null.py run` executes. `run` refuses to start unless this
file and `scar_null.py` equal their HEAD blobs.

## Sets and systems
- The G2-B sets cv295, uv231 and xm600 (xm600 holds the same 600 images as Section 7.5). Each is
  scored on its registered LADDER family (6 Qwen3-VL decodes: {short, detailed} x T in {0, 0.5, 0.8}).
  The decodes are the frozen files in `.session_backup/2026-10-20/g2b_score/outputs/`, sha-checked
  against `data/results/g2b/g2b_score_record/precheck.json`. Images are the registered clean subset,
  `Dataset.clean_index(LADDER, clean=True)`, as in the registered descriptive slope. The primary
  lexicon is used: coco80 for cv295 and uv231, objects_in for xm600.
- The Section 7.5 XM3600 six systems (`data/results/xm3600/xm3600_{zeroshot,p1_s43,fuse2_s42}-{short,detailed}.preds.json`,
  pinned by `xm3600_full_verdict.json`, which the committed `data/results/g2b/selfcheck.json` pins in
  turn). They use the selfcheck path (`xm3600_context`, `mentions`, all 600 images). Including them
  needs no new scoring code: only the gold is swapped. See reading R5.

## Unit, levels and comparator
- G_complete,i is the set of unique object classes in image i's complete gold:
  - cv295 and uv231: `inst`, the COCO-2014 instance classes;
  - xm600 and §7.5: `oiv7_verified`, the classes with OIV7 status "present" (see R4).
- The levels are L in {refs1_randk, refs_all}, built with the registered gold construction
  (`score_g2b.gold_variants`). refs1_randk holds S = 20 registered subsets, and F is the mean over
  the subsets inside `score_g2b.scores`.
- The intersection gold is G_L,i ∩ G_complete,i, taken per subset s for refs1_randk.
- Comparator: the observed slope on that intersection gold. It is reported next to the registered
  slope on G_L, which is read from `data/results/g2b/g2b_score.json` (or from
  `xm3600_full_verdict.json` for §7.5), not recomputed.

## Null
- k_i = |G_L,i ∩ G_complete,i|, or k_i^(s) per registered subset s for refs1_randk. The value comes
  from the registered randk reference choice, not from a fresh draw.
- In each replicate, each image keeps a uniform random subset of size k_i of its sorted complete
  classes, drawn without replacement, and the rest is deleted.
- Each replicate makes ONE deletion draw per (image, level): a uniform permutation of the image's
  sorted complete classes. The kept set is the first k_i classes of that permutation. For
  refs1_randk, subset s keeps the first k_i^(s) (see R1). Every prefix of a uniform permutation is a
  uniform subset of its size.
- The draw is shared by every system and temperature on the set's ladder, so every ladder point
  faces the same gold.
- Statistic: the registered `score_g2b.stat_slope`, the OLS slope of 100*F1 on ln M over the
  ladder. It is reused by import with `rows` and `scores`, never reimplemented.
- R = 1000 replicates (read from PD-23.txt) from a single `numpy.random.default_rng(0)` stream. Draws are consumed in the
  order set -> level -> replicate -> image (R2):
  - sets: cv295, uv231, xm600, s75;
  - levels: refs1_randk, refs_all;
  - images: registered id order (R3).
- Draws are taken over all of a set's ids. The clean index is applied afterwards when scoring, so
  the draws do not depend on the clean filter.
- An image with an empty complete gold, or with k_i = 0, gets an empty gold. It still consumes its
  `permutation` call, which consumes nothing when the size is 0.

## Report
For each set and level:
- the registered slope on G_L, with its source key;
- the observed slope on the intersection gold;
- the null mean and its 2.5 and 97.5 percentiles (`numpy.percentile`, linear; the values are read from
  the prereg `design_constants.ci_lo_percentile`/`ci_hi_percentile`);
- the share of null replicates whose sign equals the observed slope's sign;
- the number of scored images, and the sums of k_i (mean over subsets) and of |G_complete,i| over
  the scored images;
- all R null slopes.

`run` makes one pass. It refuses if `data/results/scar/scar_null_result.json` already exists.

No verdict is computed.

## Run
`OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2 nice -n 15 python3 -B scripts/scar/scar_null.py run`

This uses PD-23 (d)'s nice 15 with 2 threads. AGENT_RULES §5 says nice 19 with 1 thread; see R8.

## Readings for the judge (defaults are implemented)
- R1. refs1_randk has 20 registered subsets, so each image has 20 values of k_i^(s).
  - Default: one permutation per (image, level), with nested prefixes per subset. This keeps "one
    draw per image and level".
  - Alternatives: (a) use subset 0 only; (b) make 20 independent draws, which breaks "one draw".
- R2. Where the replicate index sits in the draw order. A fresh `default_rng(0)` per replicate
  would make every replicate identical.
  - Default: one stream, in the order set -> level -> replicate -> image. This mirrors the order of
    the registered `random_subsets` (k -> r -> image).
- R3. Image order follows the registered `Dataset.ids`:
  - cv295 and uv231 are integer-sorted;
  - xm600 and §7.5 are string-sorted (`sorted(refs)`).
  - Both are "sorted image id".
- R4. The registered xm600 complete-gold slope uses `oiv7_rows` (F1_pos, which ignores unverified
  mentions). The intersection gold and the null golds are set golds, so they are scored with
  `rows`/`scores`, the reference-gold path.
  - Their slopes are comparable with each other, not with the registered oiv7_verified slope.
  - G_complete,i is the OIV7 "present" set, as `oiv7_rows` defines it.
  - Disclosure: xm600's intersection slope and its null are compared with each other; the registered
    oiv7_verified slope is context only.
- R5. §7.5 has its own registered refs1_randk choice: `evaluate_xm3600_predictions.py`, seed 0,
  20 subsets, one reference per image via `rng.integers(len(refs))`, image order `sorted(ids)`.
  - Default: rebuild that choice in four lines of gold construction (not scoring code). The gate
    requires it to reproduce the committed §7.5 refs1_randk slope.
  - Alternative: borrow G2-B xm600's seed-1 subsets.
  - The §7.5 draws are independent of xm600's, coming later in the same stream. Alternative: share
    xm600's draws.
  - Disclosure: the source of the §7.5 refs1_randk rebuild is a git-excluded, sha-pinned file
    (`.session_backup/2026-10-14/r12_verify/evaluate_xm3600_predictions.py`); the rebuild reproduces the
    committed -8.9867 cell.
- R6. uv231 uses only its primary lexicon (coco80). The secondary objects_in lexicon is not run.
  - Disclosure: objects_in on uv231 was not run.
- R7. Percentiles use numpy's default linear interpolation. The share counts the replicates with
  `sign(null) == sign(observed)`.
- R8. Run settings: PD-23 (d) (nice 15, 2 threads) is followed over AGENT_RULES §5 (nice 19,
  1 thread).
