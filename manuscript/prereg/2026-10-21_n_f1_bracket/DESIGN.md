# N-F1 bracket for Paper A: design

Status: **POST_HOC, exploratory.** Authority: PD-28 item (1) (`.session_backup/2026-10-13/decisions/PD-28.txt`,
sha256 `fde27b7e…`). It answers mock review N-F1 (`manuscript/review/PAPER_A_MOCK_REVIEW_R2_2026-10-21.md`).

There is no verdict. The bracket never changes a registered verdict. Its realized outcome sentence enters §7.5,
§10 and the abstract's XM3600 clause as a qualifier (PD-28).

This text was written before any P_lower or P_upper statistic was computed on real data. `bracket.py run` refuses
to start unless this file and `scripts/n_f1/bracket.py` equal their HEAD blobs, and it refuses if
`data/results/n_f1/bracket_result.json` already exists.

## Question
On XM3600, the top gold rung (OIV7 human-verified labels) is scored with verified precision:
P = verified-present / (verified-present + verified-absent).
- Mapped mentions that OIV7 does not verify drop out of the denominator.
- Verbose captions have a lower verifiable share.

Does the registered positive F1 slope on ln M survive when those mentions are counted as errors?

## Sets
1. **§7.5 six systems.** `{zeroshot, p1_s43, fuse2_s42} x {short, detailed}`, in the order of
   `systems_queued_in_58_z` in `manuscript/prereg/2026-10-14_xm3600_predictions.json`.
   - Data: all 600 images.
   - Matcher: `rescap.chair.objects_in(raw_tone=False)`, the v2 tone-normalised matcher behind the registered
     numbers.
   - Registered statistic: N1-XM-3, `slope(oiv7_verified) > 0`. Its value is
     `xm3600_full_verdict.json:matcher_v2_tone_normalised.n1_f1_vs_logM_slopes.oiv7_verified`.
2. **G2-B xm600 ladder.** The six LADDER decodes `g2b_q3_xm600-{short,detailed}-T{0,05,08}`.
   - Data: the registered clean subset, `Dataset.clean_index(LADDER, clean=True)`, which is 537 images.
   - Lexicon: objects_in.
   - Registered statistic: G2B-E2, `slope[complete](LADDER)` with complete = `oiv7_verified`
     (G2-B prereg md:130). Its value is `g2b_score.json:datasets.xm600.predictions.G2B-E2.parts.0`.

## Estimands
Each system is scored over the images in its set. "Mapped" means the 69 lexicon classes with an OIV7 mapping (see R1)
(`resolve_map(oidv7-class-descriptions.csv)`). With sums taken over images (bootstrap-weighted in the draws):
- pm: mapped mentions whose class OIV7 verifies as present.
- am: mapped mentions whose class OIV7 verifies as absent.
- u: mapped mentions with no OIV7 verification. u = mapped − pm − am.
- pos: the verified-present classes.

| | Precision | Recall | F1 |
|---|---|---|---|
| registered | pm / (pm + am) | pm / pos | 2PR/(P+R) |
| lower | **pm / (pm + am + u)** (unverified count as errors) | unchanged | 2PR/(P+R) |
| upper | **(pm + u) / (pm + am + u)** (unverified count as correct) | unchanged | 2PR/(P+R) |

- Recall is the registered micro recall over verified-present classes. In §7.5, R comes from caption_rows
  columns 6/5; in G2-B, from pm/pos. It is identical in all three modes.
- The x-axis is unchanged: ln M, where M is all `objects_in` mentions per caption.
- Statistic: the OLS slope of 100·F1 on ln M across the six systems, computed by the registered code.
- Per system and per draw, P_lower ≤ P_registered ≤ P_upper, and F1 follows the same order. The **slopes** need
  not follow that order. No bracketing of the registered slope is claimed.

## Implementation (registered code by import)
The bracket alters only the precision inputs. Every function that computes F1, the slope or the CI is imported
unchanged.

**§7.5.**
- Functions are imported from `.session_backup/2026-10-14/r12_verify/evaluate_xm3600_predictions_v3.py`, loaded
  with importlib: `load_caption_json`, `load_preds_file`, `xo.caption_rows`, `image_counts`,
  `prf_draws_extended` (for M), `oi_draws_extended` (for F1_pos), `ols_slope`, `ci_bounds` and the constants.
- `evaluate_suite` and `main` are never called.
- The bracket edits the caption_rows array before calling `oi_draws_extended`:
  - lower: column 2 (absent) := column 0 − column 1 (mapped − present). Then vp = pm / mapped.
  - upper: column 1 (present) := column 0 − column 2 (mapped − absent). Then vp = (pm + u) / mapped.
  - Recall reads columns 5 and 6 only, so it is untouched.
- The slope loop is copied from `evaluate_suite`, because it is inline code and not a function:
  - point: `ols_slope(ln M_pt, F1_pos_pt)`;
  - draws: B = `B_MSTAR` = 500, the first 500 rows of `default_rng(SEED_MAIN=0).integers(0, 600, (B_PAIRED=2000, 600))`;
  - each draw: `ols_slope(ln max(M_b, EPS9), F1_pos_b)`.

**G2-B.**
- Functions are imported from `scripts/g2b/score_g2b.py`: `load_runs`, `Dataset`, `oiv7_rows` via `Dataset.rows`,
  `scores`, `stat_slope`, `ci`.
- The bootstrap weights W are `default_rng(bootstrap_seed=0).multinomial(n, 1/n, size=n_boot=1000)` over the clean
  index, as in `evaluate_prediction`.
- lower: `scores` on oiv7_rows with am := mapped − pm. `scores` keeps R = pm/pos.
- upper: `scores` cannot do this in one call, because pm feeds both P and R. So:
  - P comes from `scores` on rows with pm := mapped − am;
  - R comes from `scores` on the registered rows;
  - F = `div(2PR, P+R, 0)`, the expression `scores` itself uses.
  - The selftest checks that with u = 0 all three modes give F bitwise equal to `scores`.
- Per-image mapped counts are `len(m ∩ mapped)`, from the same mention sets.

**Gate.**
- One function per set takes the precision mode. `gate` calls it only with `registered`; `run` calls all three
  modes. The gate therefore tests the exact code path of the run, including the CI.
- The run's assembly (`assemble`: all modes, the outcome, verifiable shares, gold sizes, serialisation) is
  exercised end to end by the selftest on synthetic contexts of both set shapes, never on real data.

## Seeds and B
No new randomness.
- §7.5: `SEED_MAIN` = 0, B_PAIRED = 2000, B_MSTAR = 500 (v3 constants). The refs1_randk gold, used only for gold
  size, is v3's `rng_rk = default_rng(0)` with 20 subsets.
- G2-B: bootstrap_seed = 0, n_boot = 1000 and subset_seed = 1 (`design_constants` of the G2-B prereg). The CI
  percentiles are 2.5 and 97.5.

## Also reported (run)
- Per set and mode:
  - the slope point and its 95% CI. §7.5 gives the CI both rounded to 2 dp, as registered, and raw;
  - per-system P, R, F1 and M.
- The registered-mode slopes are the gate values ("the slopes under the registered P").
- The verifiable share per system, 100·(pm + am)/mapped:
  - §7.5: v3's `verifiable_share`, with its CI over all B_PAIRED draws, as the registered per-system CIs;
  - G2-B: the same quantity under W.
- The mean gold size per rung: the mean |G_i| over the scored images, for refs1_randk (mean over its registered
  subsets), refs_all and oiv7_verified (verified-present classes).
  - The §7.5 refs1_randk value is the mean over the 20 drawn subsets, so it will not equal the committed
    `Gbar_all_600` = 1.6, which is the expectation over each image's references.
  - The gate checks the §7.5 refs_all and oiv7_verified sizes against the committed 2.3483 and 2.0417.

## Decision rule
Per set, the outcome is (i) if the **lower-bound slope's 95% CI lower limit > 0**; otherwise it is (ii).
- The limit is the unrounded 2.5 percentile: `np.nanpercentile` for §7.5, `score_g2b.ci` for G2-B.
- A non-finite or missing CI gives (ii).

For the paper's claim, the outcome is (i) only if **both** sets give (i); otherwise it is (ii) (ruled in CC-063; see R3).

Fixed outcome sentences (PD-28, verbatim):
- (i) lower-bound slope CI lower > 0: "it stays positive when unverifiable mentions count as errors (post hoc)";
- (ii) otherwise: "it is positive only when unverifiable mentions are excluded; counting them as errors removes the
  positive slope (post hoc)".

If (ii) is realized, highlight 1 also drops its out-of-sample implication (PD-28).

## Inputs (sha256; `bracket.py` refuses on any mismatch, before importing any project module)
| File | sha256 (prefix) | Source of the expected value |
|---|---|---|
| `.session_backup/2026-10-13/decisions/PD-28.txt` | `fde27b7e` | recorded here |
| `scripts/g2b/score_g2b.py` | `66c665c7` | `g2b_score.json:scorer_sha256` |
| `manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.json` | `c506bc77` | `g2b_score.json:prereg_sha256` |
| `data/results/g2b/g2b_score.json` | `68be2b7a` | `g2b_score.json.sha256` |
| `data/results/g2b/g2b_score_record/precheck.json` | `02bdca27` | HEAD blob |
| `.session_backup/2026-10-20/g2b_score/outputs/g2b_q3_xm600-short-T0.preds.json` | `82b6ef5f` | `precheck.json:runs.*.sha256`; sidecar rechecked by `load_runs` |
| `.session_backup/2026-10-20/g2b_score/outputs/g2b_q3_xm600-detailed-T0.preds.json` | `a66647d1` | `precheck.json:runs.*.sha256`; sidecar rechecked by `load_runs` |
| `.session_backup/2026-10-20/g2b_score/outputs/g2b_q3_xm600-short-T05.preds.json` | `522819df` | `precheck.json:runs.*.sha256`; sidecar rechecked by `load_runs` |
| `.session_backup/2026-10-20/g2b_score/outputs/g2b_q3_xm600-detailed-T05.preds.json` | `3e6189d6` | `precheck.json:runs.*.sha256`; sidecar rechecked by `load_runs` |
| `.session_backup/2026-10-20/g2b_score/outputs/g2b_q3_xm600-short-T08.preds.json` | `71b168e7` | `precheck.json:runs.*.sha256`; sidecar rechecked by `load_runs` |
| `.session_backup/2026-10-20/g2b_score/outputs/g2b_q3_xm600-detailed-T08.preds.json` | `944668eb` | `precheck.json:runs.*.sha256`; sidecar rechecked by `load_runs` |
| `.session_backup/2026-10-14/r12_verify/evaluate_xm3600_predictions_v3.py` | `24356632` | G2-B prereg md:287 |
| `manuscript/prereg/2026-10-14_xm3600_predictions.json` | `5d0134bf` | HEAD blob |
| `.session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json` | `0b2b3aa5` | `selfcheck.json:references_sha256`; sec7 cites `0b2b3aa5e1a3` |
| `.session_backup/2026-10-14/r12_verify/xm3600_full_verdict_v2.json` | `c88d503f` | recorded here (v3's own output) |
| `data/results/g2b/selfcheck.json` | `e29f0a4f` | HEAD blob |
| `data/results/xm3600/xm3600_zeroshot-short.preds.json` | `1f357332` | `xm3600_full_verdict.json:landed_result_files` |
| `data/results/xm3600/xm3600_zeroshot-detailed.preds.json` | `47db3b9d` | `xm3600_full_verdict.json:landed_result_files` |
| `data/results/xm3600/xm3600_p1_s43-short.preds.json` | `1150a046` | `xm3600_full_verdict.json:landed_result_files` |
| `data/results/xm3600/xm3600_p1_s43-detailed.preds.json` | `296a26bf` | `xm3600_full_verdict.json:landed_result_files` |
| `data/results/xm3600/xm3600_fuse2_s42-short.preds.json` | `426c2d81` | `xm3600_full_verdict.json:landed_result_files` |
| `data/results/xm3600/xm3600_fuse2_s42-detailed.preds.json` | `b941181c` | `xm3600_full_verdict.json:landed_result_files` |
| `scripts/object_prf.py` | `6b711280` | HEAD blob (v3 imports it; not in G2-B frozen_files) |
| `rescap/chair.py` | `e47d249a` | G2-B prereg frozen_files |
| `rescap/svp/matching.py` | `a9253060` | HEAD blob (matcher dependency of chair.py) |
| `rescap/vi/lexicon.py` | `fbc945f2` | HEAD blob (matcher dependency of chair.py) |
| `rescap/vi/color.py` | `242fc46f` | HEAD blob (matcher dependency of chair.py) |
| `scripts/xm3600_oiv7.py` | `9a79403f` | G2-B prereg frozen_files |
| `scripts/score_coco_probe.py` | `d11db7e1` | G2-B prereg frozen_files |
| `scripts/clean_supervision.py` | `01f17200` | G2-B prereg frozen_files |
| `rescap/vlm/mock.py` | `33793de0` | G2-B prereg frozen_files |
| `data/datasets/xm3600/test_data.json` | `0a613214` | xm3600 prereg `frozen_inputs_sha256` / G2-B frozen_files |
| `data/xm3600/oiv7_labels.json` | `bac3953a` | xm3600 prereg `frozen_inputs_sha256` / G2-B frozen_files |
| `data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv` | `84a4373a` | xm3600 prereg `frozen_inputs_sha256` / G2-B frozen_files |

In addition, `score_g2b.check_pins` re-verifies every G2-B frozen file after the import.

## Run
`OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2 nice -n 15 python3 -B scripts/n_f1/bracket.py run`

- Precondition (PD-28 order): map amendment 4 (work-list item 2) is committed before `run`.
- It makes one pass and writes `data/results/n_f1/bracket_result.json`.
- It re-runs the gate cells first and refuses if any fails.
- An independent verifier re-run follows, as for SCAR (PD-28 process).

## Readings for the judge (defaults are implemented)
- **R1. Denominator.** "All mapped mentions" means the mentions of the OIV7-mapped classes, which is v3's
  caption_rows column 0, also the denominator of the registered `verifiable_share`.
  - Counts, from the pinned files: 69 lexicon classes have an OIV7 mapping (`data/xm3600/vi_oiv7_map.json`, 69
    entries, all resolved by `resolve_map`). That is the "OIV7 status on 69 mapped classes" of the §7.5 verdict
    log (`xm3600_oiv7_cli_stdout[0]`) and the committed `vmap_resolved_classes_in_xm3600_oiv7` = 69.
  - 67 of the 69 have an OIV7 status on at least one of these 600 images.
  - The "82 mapped classes" in `manuscript/prereg/2026-10-14_xm3600_predictions.md` (lines 27, 36, 43) does not
    match the pinned map (sha `27f2b1ca`, the sha that prereg itself pins). The count does not enter any
    computation.
  - Unmapped `objects_in` mentions stay out of both bounds' precision.
  - M on the x-axis still counts them, as in the registered rung.
  - This follows PD-28's text. It is not a choice.
- **R2. Unrounded limit.** The decision uses the unrounded 2.5 percentile. §7.5 also reports v3's 2-dp
  `ci_bounds`. If the two disagree in sign, that happens only when |limit| < 0.005, and it is reported as such.
- **R3. Combining the sets.** PD-28 does not say how two sets combine for the paper's claim.
  - **Ruled (CC-063):** the paper-level outcome is (i) only if BOTH sets give (i), because they are the same
    images under two backbones; otherwise it is (ii).
  - Each set's own sentence is reported in §7.5.
- **R4. Already derivable.** §7.5's per-system P_lower point is already derivable from committed numbers, since
  P_lower = P_pos × verifiable_share / 100 (`xm3600_full_verdict.json` systems block, 4 dp).
  - R_pos and M are also committed, so a 4-dp approximation of the lower-bound point slope was derivable before
    this design. Its bootstrap CI, which decides the outcome, was not.
  - This verifier did not compute either. The gate writes no per-system verifiable share and no mapped count.
  - Disclosure (CC-063, verbatim): "the lower-bound point slope was approximately derivable from committed numbers
    before this design, and neither the design author nor the verifier computed it; the outcome-deciding CI was
    not derivable."
- **R5. Evaluator version.** sec7 cites `xm3600_full_verdict.json`, which the v1 (`dc00c456`) or v2 (`010986c6`)
  evaluator wrote; both write that path.
  The design imports v3 (`24356632`), which writes `_v2.json`.
  - The v1→v3 diffs touch only output paths, the landed-file list, n-gram None handling and the kappa verdict text.
  - None of them touches the imported functions.
  - Evidence: the gate reproduces the oiv7 slope and its CI against **both** verdict files.
- **R6. Analysis set and contrasts.** G2-B uses the clean subset only (537 images), the registered E2 analysis set.
  - The full-set sensitivity (600 images) is not computed.
  - The O1 contrast (complete − refs_all) is not computed under the bounds, since PD-28's statistic is the slope
    only.
- **R7. Inline glue.** The §7.5 slope loop and idx_boot construction are inline in `evaluate_suite`, so they are
  copied (six lines). The G2-B P_upper recombination copies `scores`' F expression.
  - Both are covered by the gate (point and CI of the registered mode) and by the selftest (u = 0 identity).
- **R8. Run settings.** nice 15 with 2 threads, as SCAR used (CC-048 R8).
