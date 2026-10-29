# Paper B, B-R1 dev pilot: reverse-direction panel swap (RULE; no B-R1 score computed)

This rule is final after CC-161 (W1-W11). Its sha256 is pinned in `scripts/b_r1/b_r1.py` (RULE_SHA256) and logged in
`.session_backup/2026-10-13/decisions/LOG.md` before any training. It uses dev data only: KTVIC dev300 is a split of
KTVIC train. **B-R1 adapters are never decoded or scored on any test split. 41 R3 images (5 of R1, 25 of R2) also have
an OpenViIC-test copy.** Everything below is AI opinion, not expert-validated. It supersedes RULE_DRAFT.md (82f0f73c,
deleted).

## 1. Question

D0 (rule 72345e1c, decide 15dd925f) found that the KTVIC-trained B-1 adapters gain +10.59 CIDEr-D per doubling
against KTVIC references but only +0.72 against OpenViIC references on the same 187 dev300 images. The gap is +9.87
[6.71, 13.35]. One alternative explanation has not been excluded: the OpenViIC panel may not respond to any data
scaling. B-R1 tests this in the reverse direction. It trains the same recipe on OpenViIC captions of KTVIC-train
images, then scores against both panels.

## 2. Training data (pinned; ids and shas only, no caption text in the repo)

| Input | sha256 |
|---|---|
| data/ktvic_openviic_refs.json (`_pairs.train` only) | 4eb02cc43841bae4f844ee74d4c01b58e677dc8d6abafdd998c9f5b5706f725d |
| data/datasets/openviic/uit-openviic-annotation-train.json (the only OpenViIC file opened) | d757520e76b8490df6c7275c2beb8b3ecef0342635a436bea8c3cfd07eb49df0 |
| data/datasets/ktvic/train_data.json | 72ee9b57c350fb5f215e1f04701c515a51e5e415240e51a77c8ce00ce6316a0f |
| data/splits/ktvic_train_minus_dev300.txt (B-1 pool, 3,469) | 006080b455a553ca9cc5d3f514ad76bfbe67f444c9c145a5696de681a4be1a58 |
| data/splits/ktvic_dev300.txt | cee024f8bb76846b1623e36d1861caccc4d13874db87544213a1f18f3de6898c |
| manuscript/prereg/2026-10-29_b_r1/r1_lists.json (built by `b_r1.py lists`) | 571dfedf16bd39dfa4e94f6f0873c89241d7ffb61ef9a86c38ffa4a4e4db289c |

1. **Candidates.** These are the B-1 pool ids that have an OpenViIC copy with split `train` in `_pairs.train`. There
   are 2,272 of 3,469.
2. **Exclusion (dev300 near-twins).** A train id is excluded if (a) it shares an OpenViIC file, of any split, with a
   dev300 image, or (b) min(pHash, dHash) <= 10 against any dev300 image. In (b) the mirrored train image also
   counts. This is `match_openviic.py`'s hash bound without its SSCD clause, so it excludes more, not less. Because
   there is no SSCD check, a crop-type duplicate can still pass. 10 candidates are excluded: 713, 1628, 1826, 2049,
   4469, 4487, 4691, 4887, 5297, 5891. That leaves **2,262 eligible**.
3. **Levels.** The levels are R1/R2/R3 = 216 / 867 / 1734. These are the N of B-1 L1/L3/L4, so x matches B-1. Each is
   a prefix of B-1's own order `train_rl.schedule(pool, 3469, 42)`, filtered to eligible ids. The levels are nested.
   Their ids sha256 are 750a5dec... / 2b78fae9... / 79c154b3... (full values in r1_lists.json). Overlap with the
   B-1 level of the same N: 152/216, 575/867, 1143/1734.
4. **Caption source.** This is the only change from B-1. B-1 trains on one caption per image: `build_gold_sft.py`
   default `--select first`. B-R1 also uses k = 1 on both sides. The caption is the first element of D0 §3's O pool:
   the train copies in `_pairs` order, captions pooled, stripped, exact repeats dropped (`d0.dedup`).
   - `b_r1.py ann` writes a KTVIC-format JSON with KTVIC ids and file names and one OpenViIC caption per image. It is
     built on the laptop, outside the repo: sha256 dfaa19c7d1729e3829031c554c00f3df0e174cc05c4875b3eb5285b3d9e96135,
     1,734 images.
   - On M2 this is the only caption file staged. `build_gold_sft.py --annotations <ann> --images-file r1_<lv>.txt`
     runs unchanged and must reproduce these sft.jsonl sha256: R1 1e4ad956..., R2 846ecc7e..., R3 7229e9c1...
     (full values in b_r1.py SFT_PINS).
   - Disclosure: the OpenViIC targets are longer. On the R3 images the mean is 17.4 words, against 12.0 for the
     KTVIC first caption of the same images.

## 3. Recipe (B-1, unchanged)

The recipe is B-1 PREREG ee91c152 as run on M4:

- `train_stage2.py --stage sft --epochs 2 --seed S --loss-mask assistant`, 4-bit with 512 vision tokens,
  `save_steps=200`;
- the same resume hook (05466ef5) and the same .venv freeze (7332d343);
- greedy short-prompt dev300 decode with `evaluate.py --model qwen2.5-vl-7b` (NCS_DATASET=ktvic_dev);
- the same log checks.

`b1.py check --machine --job b_r1_job.sh` enforces B-1's registered job fragments and S5's forbidden flags.

- **Seeds:** 42 and 43.
- **Machine parity, Step 0:** B-1's own Step 0 runs on M2. The n2 p1dev_s42 adapter is decoded and needs at least
  95% identical captions to the registered n2 preds (1e183383). Otherwise it is a JOB STOP.

## 4. Budget (from B-1's measured M4 gpu_seconds.tsv)

- Measured train time: N=216 397 s, N=867 1,509 s, N=1734 2,982 s (mean of 3 seeds). Each decode takes 315 s, and
  Step 0 takes 322 s.
- Design: 2 x (397 + 1,509 + 2,982) + 6 x 315 + 322 = 11,988 s = **3.33 GPU-h**.
- Allowances: about 4.0 GPU-h if the longer targets lengthen the outputs, and about 6 GPU-h with a 1.5x factor for a
  different card.
- **Hard cap: 8 GPU-h.** Accounting follows B-1 (`b1.left`, start lines charged). A timeout is a final CAP STOP.
- With a third seed the design would be about 5.0 GPU-h. It is not proposed: on the decided B-1 K panel, dropping
  seed 44 from {L1, L3, L4} hardly moves the slope CI (11.58 [7.81, 15.80] vs 11.48 [7.72, 15.76]). The image
  bootstrap dominates.

## 5. Evaluation and the pre-fixed rule

- **Images and references.** The 187 D0 image ids (sha ba506945) are used. Panels are as in D0 §3: k_i = min(5,
  |O|, |K|), the same per panel, selected by the hash rule. There is one CIDEr-D df per panel, built from its
  selected references.
- **Scorer.** kit B as in D0: RDRSegmenter, lower-cased, trailing punctuation stripped, CIDEr-D x100, and
  `d0.in_order` (the fixed id order).
- **Bootstrap.** The bootstrap is D0's: one `default_rng(0)` (2000, 187) index matrix, shared by both directions, so
  forward and reverse draws are paired. CIs are 95% percentile intervals.
- **Scorer gate (a decided number, not a look).** The 15 forward B-1 adapters are rescored by this code. Their b_K,
  b_O and g must equal D0's decided point values within 1e-6. Otherwise the run aborts with no output.
  - Laptop smoke tests of the code path met it at 4e-15. They used forward preds standing in for reverse ones, so no
    reverse number exists. Only output keys and the gate were printed, and the forward sigma = inf numbers were never
    read.
  - The forward CIs recomputed here use `d0.in_order`, so they differ numerically from D0's decided CIs. Only the
    points are gated.
- **W6 re-read consistency (CC-161 W7).** The minus-twins forward g must equal the D0 masked re-read's mask (a) g
  within 1e-6. Score also refuses unless that re-read (reread.json 7853ab4a, LOG CC-161 W6) says PROCEED.

Statistics, with x = log2 N over R1-R3 and seed fixed effects (`d0.fe_slope`):

- b_O^R: own panel, because the adapters were trained on OpenViIC captions;
- b_K^R: the other panel;
- g_R = b_O^R - b_K^R;
- g_rel_R: the same on ln(mean CIDEr-D), in % per doubling.

**Manipulation check (CC-161 W3).** The check passes if the mean hypothesis syllables of the six reverse adapters
exceed those of the forward B-1 adapters at matched N (seeds 42/43, L1/L3/L4), pooled over the 187 images. A length
slope is not used, because length can already be learned at N = 216.

**Outcome (exactly one; clauses in this order; only GO_BOTH passes):**

1. **STYLE_NOT_LEARNED** if the manipulation check fails. The reverse adapters did not move toward the OpenViIC
   style, so nothing is read from the slopes.
2. **REVERSE_FLAT_OTHER_UP** if CI_lo(b_O^R) <= 0 and CI_lo(b_K^R) > 0. This supports the D0 alternative: the
   OpenViIC panel is insensitive to scaling.
3. **REVERSE_FLAT_BOTH** if CI_lo(b_O^R) <= 0 otherwise. The OpenViIC captions are a weak training signal, and the
   panel question stays open.
   - In both REVERSE_FLAT cases D0's gap cannot be read as panel-specific learning, and Paper B Option 1 goes back
     to the judge.
4. **GO_BOTH** if all of these hold:
   - CI_lo(g_R) > 0;
   - g_R >= 1.0 (Q3);
   - CI_lo(g_rel_R) > 0 (Q3);
   - with sigma = inf (no length penalty, co-primary, Q6): CI_lo(g_R) > 0 for the reverse direction **and**
     CI_lo(g) > 0 for the forward direction.

   Each panel then rewards its own training captions more than the other's, in both directions. Option 1 stays
   eligible, and the full study still needs its own re-rule.
   - If the sigma = 6 conditions hold but a sigma = inf condition fails, the outcome is **GAP_INCONCLUSIVE**
     (`length_penalty_dependent`), never a pass.
   - If a D0 clause (g_R >= 1.0 or g_rel) fails, evaluation falls through to clause 5.
5. **ASYMMETRIC** if CI_hi(g_R) < P1 SESOI = 4.934 CIDEr-D per doubling. P1 SESOI was fixed by D0 §6 as max(1, g/2)
   and is asserted against D0's decide.json. This is an equivalence reading: the OpenViIC-trained adapters gain on
   KTVIC references about as much as on OpenViIC references. The reason says whether CI_lo(b_K^R) > 0, meaning the
   gains transfer. This is reported as is; the judge rules on the claim's scope.
6. **GAP_INCONCLUSIVE** otherwise. The g_R CI spans both 0 and P1 SESOI. This result is never read as ASYMMETRIC.

**Power, stated before the run (CC-161 W8).** The values are computed on CPU from D0's forward data at this design
(seeds 42/43 x L1/L3/L4), in the W6 re-read:

| Statistic | 95% CI half-width | MDE at 80% power |
|---|---|---|
| own-panel-type slope (b_O) | 2.20 | 3.15 |
| other-panel slope (b_K) | 4.04 | 5.77 |
| gap g | 4.19 | 5.98 |

All values are in CIDEr-D per doubling.
- GO_BOTH therefore needs g_R of roughly 4 or more.
- ASYMMETRIC needs g_R of roughly 0.7 or less.
- GAP_INCONCLUSIVE is a likely g_R outcome. The pilot's main purpose is the b_O^R question: does the OpenViIC panel
  respond to OpenViIC-caption training?

## 6. P2 re-rule (object content)

This is a logged amendment to D0 §6 under its "except by a logged ruling" clause (CC-161 ruling 5). It is
**dev-informed: the matcher was chosen after D0's numbers were seen.** D0 showed that matcher v2 cannot see data
scaling even on the own panel. The v2 union F1 stays around 76, with K slope
-0.19 [-1.00, 0.67]. B-1's exact matcher (`rescap.chair.objects_in`) does see it: K +1.35 [0.57, 2.18], union +0.71
[0.20, 1.24]. The rules:

- P2 primary matcher = `rescap.chair.objects_in`. v2 is secondary and reported.
- **Sensitivity precondition.** P2 is assessable only if the primary matcher's own-panel F1 slope has CI_lo > 0 in
  each direction it is used: forward = gold K, reverse = gold O. Otherwise P2 is NOT_ASSESSABLE, and no equivalence
  claim is made. B-R1 records this as `p2_matcher_sensitive`.
- The margin formula is unchanged, applied to the primary matcher on the D0 numbers: max(2.0, |0.71|, 2 x 0.47) =
  **2.0 F1 points**, the same value as before.
- Disclosed caveats:
  - (i) The KTVIC lexicon behind `objects_in` may favour gold K over gold O, which would bias the reverse
    precondition against passing.
  - (ii) The choice is dev-informed. It is conservative: equivalence under a matcher that cannot see scaling would
    pass trivially.
- Object F1 never gates the B-R1 outcome.

## 7. Descriptive rows (pre-declared, no verdict)

1. **Minus dev near-twins, both directions.** The scan in §2 found 11 B-1 train ids, over the whole 3,469 pool, that
   are near-twins of 10 dev300 images. 8 of those dev images are in the 187: 1594, 2004, 4645, 4954, 5198, 9981,
   10448, 10489. D0 knew only 2004.
   - The forward adapters trained on these twins with KTVIC captions: 1 at L3, 3 at L4, 11 at L5. This could inflate
     b_K, which is the direction of D0's gap.
   - Forward and reverse slopes are therefore recomputed on the 179 images without them, using masked draws of the
     same matrix.
   - The D0 masked re-read (CC-161 W6) was logged before computing and run once. It is POST HOC, DESCRIPTIVE and
     DEV, and D0's verdict is unchanged. Masks and results, g [95% CI]:

     | Mask | Images | g |
     |---|---|---|
     | (a) minus the 8 twins | 179 | +10.43 [7.09, 13.96] |
     | (b) minus 2004 | 186 | +9.87 [6.60, 13.43] |
     | (c) minus 16 exact-caption ids | 171 | +8.49 [5.24, 12.01] |
     | (d) union of (a) and (c) | 165 | +8.92 [5.59, 12.40] |

     For (d), g_rel = +7.47% [3.70, 11.36]. The hold rule was not met, so B-R1 proceeds.
2. **Same-N crossover.** For seeds 42/43 and N = 216/867/1734:
   mean of [O(R) - O(F)] + [K(F) - K(R)], against B-1 L1/L3/L4.
   The image sets differ (see the overlaps in §2.3). A same-image KTVIC arm was refused for B-R1 (CC-161 ruling 3).
3. **Hypothesis length.** Mean syllables per adapter, and the fixed-effects length slope (syllables per doubling)
   in each direction. CIDEr-D's length penalty could confound slopes, because the OpenViIC targets are longer.
   - As each model's outputs move toward its own panel's length, the length penalty (sigma = 6) lowers the other
     panel's slope in both directions. That alone could produce GO_BOTH.
   - So the sigma = inf (no length penalty) slopes are a co-primary condition for GO_BOTH (§5). This is the form of
     kit B's `P8_rdr_sigma_inf(no_LP)`.
4. **Both directions together:** g + g_R. Also g - g_R with its paired CI, which is the asymmetry: one index matrix
   gives the paired draws.
5. **Exact-caption overlap (counts only, computed now, no score).**
   - B-R1 targets: 0/216, 0/867 and 0/1734 equal any selected O or K reference of the 187 images, after stripping.
   - B-1's KTVIC first captions equal a selected K reference in 1 of L1, 4 of L3, 11 of L4 and 21 of L5, and 0
     selected O references.
   - This is a second forward-only advantage, alongside the twins in row 1.

## 8. Run and one look

- **On M2.** `bash scripts/b_r1/b_r1_job.sh <HEAD>` runs inside tmux. The job refuses unless
  `/root/.vsps_machine_id` is `m4`. It also refuses unless the HEAD equals the given one, the tree is clean,
  scripts/b_r1 and scripts/b1_scaling SHA256SUMS verify, and the venv, hook and ann pins match.
- **Guards.** `b_r1.py guard` runs before every GPU step. It requires `grl common.host_ok` and the m4 role. It
  refuses if any OpenViIC path is staged, any KTVIC test file or test-sha image is present, any C-EN set or process
  exists, or another lock exists.
- **What runs.** The lock is B-1's O_EXCL lock at /root/outputs/b_r1/RUNNING. M2 does no scoring.
- **Crashes (CC-152a).** A finished step is skipped on re-run. A training run with no metrics.jsonl is never
  resumed, because checkpoint resume fails under the pinned venv. The job stops instead. The operator deletes the
  run folder unread and renames its log unread. The run is retrained from scratch once, and a second failure is a
  JOB STOP for the judge.
- **Staging (CC-161 W10).** Staging is done by hand under one LOG checklist line written at staging time. The
  line lists, with no host string:
  - $NCS_DATA/datasets/ktvic: train images plus train_data.json 72ee9b57;
  - $NCS_DATA/datasets/ktvic_dev, verified by ktvic_dev_split.py --verify;
  - the base snapshot, S5 shard shas checked by `b1.py check --machine`;
  - $NCS_DATA/runs/p1dev_s42, adapter 227a3312;
  - /root/outputs/b_r1/s5_preds/p1dev_s42_redecode-dev300-short.preds.json 1e183383;
  - the hook 05466ef5;
  - $NCS_DATA/datasets/ktvic_r1/ann_ov.json dfaa19c7.

  No OpenViIC file is staged. The line ends with one `b_r1.py guard --head <HEAD>` run with rc 0. The ann JSON holds
  caption text. It lives only on M2 and in the scratchpad, never in the repo, and is deleted from M2 at cleanup.
- **Scoring.** The outputs and their SHA256SUMS are pulled to `.session_backup/machines/M2/root/outputs/b_r1`. Then
  `b_r1.py score` runs once on the laptop CPU. It refuses if its output exists, if RULE.md is not pinned and logged,
  if D0's decide.json (15dd925f), the W6 re-read (7853ab4a) or D0's input pins differ, or if the re-read did not
  say PROCEED.
- **Output.** `.session_backup/2026-10-29/b_r1/decide.json` holds ids, counts and numbers only.

## 9. Code

- B-R1 code: scripts/b_r1/{b_r1.py, d0_reread.py, b_r1_job.sh}.
- It imports scripts/b_d0/d0.py 0d87a953 (the in_order-fixed version, LOG l.701), which is pinned in
  scripts/b_r1/SHA256SUMS and committed with it (CC-161 W1).
- The Q1-Q7 answers are in CC-161: Q1/Q7 W6 re-read done, Q2 no, Q3 yes, Q4 yes (dev-informed amendment), Q5 by
  hand, Q6 yes.
