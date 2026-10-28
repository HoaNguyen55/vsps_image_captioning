# Paper D, D-alpha: pre-registration of the L1–L4 → L5 extrapolation test on B-1's dev curve

**Label: DEV CURVE (dev300). Development split only; never a test result.** Ruled by CC-147 ruling 1 (GO-with-fixes, specs 1–10, W1–W3). This is a separate registration for Paper D (PI-1026ah: B-1 results go to D). It is **not** a B-1 amendment: it changes no B-1 rule, verdict, list, cap or code, and it does not touch `scripts/b1_scaling/`. CC-147 names this file `ADDENDUM.md`; the writer's brief names it `PREREG.md`; the content is the CC-147 addendum.

| field | value |
|---|---|
| Paper | D. One question: does a scaling form fitted on the four smaller B-1 training sizes predict the full-data point? It makes no method claim and changes nothing in B |
| Input | B-1's `ledger.json` (kit-B stripped CIDEr-D per image, `rows[name]["cider_s"]`), read from the laptop mirror only after B-1's `decide.json` exists; its sha256 and decide.json's sha256 are recorded in the output |
| Upstream | B-1 prereg `manuscript/prereg/2026-10-28_b1_scaling/PREREG.md` (sha256 `ee91c152…`), code `scripts/b1_scaling/b1.py` (`e747205e…`, checked at run time against `scripts/b1_scaling/SHA256SUMS`) |
| Code | `scripts/d_extrap/d_extrap.py` (§10), `SHA256SUMS` there |
| Machine | laptop CPU only; numpy and scipy only; 0 GPU-h |
| Written | 2026-10-28, 04:21–04:52Z, on the laptop. No B-1 output other than `logs/job.log` and `gpu_seconds.tsv` was opened (§2) |

## 0. Timing statement (honest)

1. **Committed while B-1 is training, before any B-1 score is read.** B-1's 17 decodes are the 15 points, Step 0 and the zero-shot decode. evaluate.py writes CIDEr-D into each decode's result file, so every finished decode holds a score on disk, unread.
2. **At writing (2026-10-28T04:37Z, recounted at 04:47Z and 04:50Z, unchanged), 6 of 17 decodes were on disk, unread**, counted from `job.log` `OK dec_` lines only (distinct step names): `dec_b1_step0_p1dev_s42`, `dec_b1_zeroshot`, `dec_b1_s42_L1`, `dec_b1_s42_L2`, `dec_b1_s42_L3`, `dec_b1_s42_L4`. The last job.log line was `03:55:04Z START train_b1_s42_L5`. No seed-43 or seed-44 point existed. (CC-147 estimated "about 7"; the job.log count is 6.)
3. **At commit**, the gatekeeper's GATE_LOG row records the commit UTC, the last job.log line at that moment, and N decodes on disk from `OK dec_` lines (CC-147 W1). If seed-43 decodes exist by then, they are on disk and unread, as all others; that row states which.
4. **W3.** If the commit lands after B-1's `score` step has started (a `score` line in job.log, projected about 13:00Z on 10-28), this file is not a registration: the whole D-alpha analysis is labelled **post hoc** in every use, and no further writer time is spent on it.
5. **W2 read rule.** Until `decide.json` exists in the M4 mirror (`.session_backup/machines/M4/root/outputs/b1_scaling/`), nobody — writer, judge, gatekeeper or any agent — opens anything there except `logs/job.log` and `gpu_seconds.tsv` (B-1 §1.2 item 6). `d_extrap.py run` refuses to start unless `decide.json` sits beside the ledger, and refuses a ledger whose sha256 differs from decide.json's `ledger_sha256`.

## 1. What is already known (not blind)

D-alpha is **not blind** at L5. Cited from B-1 §11:
- **B-1 §11 item 1.** The authors know S5's seed-42 CIDEr-D at L3 / L4 / L5 = 125.52 / 128.71 / 144.33 (S5's word-level scorer, not kit-B stripped). So the seed-42 L4→L5 step is known to be about +15.6, against about +3.2 for L3→L4. B-1 seed 42 L3–L5 repeats S5's design on a new host.
- **B-1 §11 item 2.** The authors know the B-F1 KTVIC-**test** scores of the L5 recipe at seeds 42 / 43 / 44: 144.18 / 144.86 / 147.60. The L5 level of every seed is therefore partly foreseeable (different split, different scorer).
- **Genuinely unseen:** L1 and L2 at every seed; L1–L4 at seeds 43 and 44; every kit-B stripped dev300 value.

Consequences, fixed here:
- **The primary test uses seeds 43 and 44 only**, described as "new draws whose L5 level is partly foreseeable from B-F1 test and S5".
- **Seed 42 is a labelled replication row** (same fits, same rule, reported as "replication; S5's L3–L5 known").
- "All complete seeds" is a descriptive row.
- This weakens the novelty case; the item runs because it costs no GPU and the registration window closes at `score` (CC-147 ruling 1).

## 2. What the writer opened

- CC-147 in full; B-1's PREREG.md in full; `scripts/b1_scaling/b1.py` (`plan`, `run_name`, `score_rows`, `decide`, `sensitivity`, `fake_ledger`, `selftest`); the `ledger`/`decide` lines of `b1_job.sh`; C's test prereg §7.1 (l.146–148); `scripts/scaling_probe.py` constants (`B`, `BOOT_SEED`, `DEV_N`).
- From the M4 mirror and M4 itself: `logs/job.log` lines (step names, times, counts) and the file sizes of `job.log` and `gpu_seconds.tsv`. Nothing else under `outputs/b1_scaling/`.
- **Not opened:** any ledger, decide file, result JSON, `dec_*.log`, preds file, caption or reference.

## 3. Input and points (spec 1)

- y_{s,L} = mean of `rows[name]["cider_s"]` over the 300 dev images (kit B, final punctuation stripped, ×100; B-1 §5).
- N_L = 216, 433, 867, 1,734, 3,469 for L1–L5, taken with the row names from `b1.plan()` entries of kind `point` (fields `seed`, `level`, `N`), imported, never hardcoded. The script asserts that `plan()` lists 15 points.
- A seed is complete iff all five of its point rows exist in the ledger (B-1 §7.4). An incomplete seed leaves every row.
- The zero-shot point and the S5 rows are not used.

## 4. Fit set and rows (spec 2)

| row | seeds | role |
|---|---|---|
| **primary** | the complete seeds among {43, 44} | verdict per form |
| replication | 42, if complete | same fit and rule, labelled replication |
| all complete seeds | every complete seed | descriptive |
| mask 2004 | primary seeds, dev300 minus image 2004 | descriptive (§8) |

- Two primary seeds complete: pooled fit. One complete: that seed alone, labelled "one seed". None: **NO VERDICT** for every form.
- **Every fit uses L1–L4 only.** L5 enters neither a fit nor a start value; it enters only e (selftest: a jump at L5 moves e by exactly the jump).

## 5. Forms (spec 3) — exactly these three; no form may be added later

- **F1, log-linear (the P-B1 form):** y_{s,L} = a_s + b·log2 N_L, seed intercepts, common b, OLS (b = `b1.fe_slope` on the balanced L1–L4 grid; a_s = mean_L y_s − b·mean_L x). ŷ_{s,L5} = a_s + b·log2 3469.
- **F2, log–log power:** ln y_{s,L} = c_s + β·ln N_L, seed intercepts, common β, OLS in log space; ŷ_{s,L5} = exp(c_s + β·ln 3469). If any point mean (or any bootstrap replicate mean) is ≤ 0, F2 is NO VERDICT.
- **F3, saturating power:** y_{s,L} = E_s − A·N_L^(−α), common A and α, one E_s per seed.
  - Optimizer: `scipy.optimize.least_squares(method="trf")`, residuals y-hat − y over the S × 4 points, scipy defaults otherwise (version recorded in the output).
  - Bounds: α ∈ [0.05, 2], A ∈ [0, 1e5], E_s ∈ [0, 400].
  - Starts, recomputed for every fit (the point fit and **each bootstrap replicate from that replicate's own L1–L4 means**, no warm start): α0 = 0.5; E_s0 = max over L1–L4 of y_s + 1; A0 = mean_s (E_s0 − y_{s,L1})·216^0.5; the start vector is clipped into the bounds.
  - **F3 fails** if `status ≤ 0` (not converged) or α-hat is at a bound, defined as scipy's own `active_mask` for α ≠ 0.
  - **F3 is NO VERDICT** when (a) it would rest on one seed (3 parameters on 4 points; this covers the one-seed fallback and always the seed-42 row), (b) the point fit fails, or (c) more than 5% of the bootstrap refits fail. With ≤ 5% failed refits the CI is the percentile over the successful refits, and the failed count is reported.
- **Not fitted: Lin et al.'s rectified scaling law** (arXiv 2402.02314), L(D) = B/(D_l + D^β) + E. It has 4 free parameters per curve and B-1 gives 4 x-values per seed in the fit set, so it has zero residual degrees of freedom and is not identifiable here. It is named and not fitted.

## 6. Estimand, bootstrap and rule (specs 4–6)

- **e = mean over the row's seeds of (y_{s,L5} − ŷ_{s,L5})**, in stripped CIDEr-D points. e > 0 means the form under-predicted L5.
- **CI:** 95% percentile (2.5, 97.5) over B-1's own index matrix, `numpy.random.default_rng(0).integers(0, 300, (2000, 300))`, built exactly as `b1.decide` builds it. Each replicate recomputes every point mean from its per-image values, refits every form on L1–L4, and recomputes e. **The CI covers image sampling only**; seed variance is not in it.
- **T = 2.0 stripped CIDEr-D**, C's registered SESOI (`manuscript/prereg/2026-10-25_c_test/PREREG.md` l.148, "+2.0 stripped CIDEr-D points", PR2 §7.1), on the same stripped ×100 convention as B-1's decision column. Fixed now and never changed.
- **Rule, per form, three-way (TOST-style):**
  - **EXTRAPOLATES** if −T ≤ CI_lo and CI_hi ≤ +T (the boundary counts as inside);
  - **FAILS** if CI_hi < −T or CI_lo > +T (no overlap with [−T, +T]);
  - **INCONCLUSIVE** otherwise.
- No "best form" claim beyond these labels. Forms are not ranked, combined or selected.

## 7. Author's prior (a prior, not a rule; spec 8)

S5's seed-42 steps (+3.2 for L3→L4, +15.6 for L4→L5, S5's scorer, not kit-B stripped) suggest that every form fitted on L1–L4 will under-predict L5 (e > 0), and F3 most, since a saturating curve bends down where S5 bent up. If B-1's L5 points behave like S5's, FAILS is the expected F3 label. This prior shapes no rule.

## 8. Dev twin (spec 7)

The primary uses the full dev300, as B-1 does. A **mask-2004 row** (dev300 image 2004 is byte-identical to train image 4487, in L5 only; B-1 §1.1(b)) repeats the primary seeds' fits with each point mean over the other 299 images and each replicate the registered index-matrix row with the draws of image 2004 dropped (B-1 §6's formula). It is descriptive: its three-way labels are output as `label_descriptive` (never `verdict`), each sentence ends "Descriptive row (dev300 minus image 2004, byte twin of L5 train image 4487); no verdict.", and it gives no verdict. The "all complete seeds" row is output the same way ("Descriptive row (all complete seeds); no verdict.").

## 9. Pre-written sentences (spec 9)

Every number reads "dev curve (dev300)". The script fills these templates (`d_extrap.SENT`); `{seeds}` is "seeds 43, 44" or "seeds 43 (one seed)" etc.; `{dir}` is "under" if e > 0, else "over".
- **EXTRAPOLATES:** "On the KTVIC development split (dev300), {form} fitted to the four smaller training sizes (216–1,734 images) predicted the full-data point (3,469 images) within ±2.0 stripped CIDEr-D: e = {e} [{lo}, {hi}] ({seeds}; image-bootstrap 95% CI, image sampling only)."
- **FAILS:** "On the KTVIC development split (dev300), {form} fitted to the four smaller training sizes (216–1,734 images) {dir}-predicted the full-data point (3,469 images) by more than 2.0 stripped CIDEr-D: e = {e} [{lo}, {hi}] ({seeds}; image-bootstrap 95% CI, image sampling only)."
- **INCONCLUSIVE:** "On the KTVIC development split (dev300), {form} fitted to the four smaller training sizes gave e = {e} [{lo}, {hi}] at the full-data point ({seeds}); the interval overlaps ±2.0 stripped CIDEr-D without lying inside it, so neither extrapolation nor failure is shown."
- **NO VERDICT:** "{form} gave no verdict on dev300 ({why})."
- **Every primary sentence ends:** "Seeds 43 and 44 are new draws whose L5 level is partly foreseeable from the B-F1 test scores and S5; the CI covers image sampling only." Every seed-42 sentence ends "Replication (S5's L3-L5 known)." (`d_extrap.NOTE`). If W3 applies, every sentence adds "post hoc (registered after B-1's scoring began)".
- Nothing here changes B-1's P-B1 verdict or any text of Paper B. Scorecard credit for D is scored after the result (PI-1026ao(3) pattern), never pre-committed.

## 10. Code (`scripts/d_extrap/d_extrap.py`)

- `d_extrap.py run --ledger <mirror>/ledger.json --out <file>`: laptop CPU, write-once output. It refuses unless `decide.json` is beside the ledger, the ledger sha256 equals decide.json's `ledger_sha256`, and the imported `b1.py` equals its pin in `scripts/b1_scaling/SHA256SUMS`. It records the sha256 of the ledger, decide.json, b1.py and itself, and the numpy and scipy versions. It sets `sys.dont_write_bytecode` before importing b1, so it writes nothing under `scripts/b1_scaling/`.
- The run path was exercised once in the scratchpad on a synthetic ledger: it wrote its output and refused a missing `decide.json`, a ledger sha mismatch and an existing output. The F3 "> 5% of refits failed" branch has no synthetic test.
- `d_extrap.py --selftest`: synthetic ledgers only (no file read except B-1's code). It covers: row names from `plan()` and B-1's index matrix (B = 2000); exact log-linear data → F1 e = 0, EXTRAPOLATES; a +15 jump at L5 → F1 FAILS ("under-predicted"); wide per-image noise around a small miss → INCONCLUSIVE; exact power data → F2 e = 0; exact saturating data → F3 e ≈ 0, EXTRAPOLATES, no failed refits; a jump at L5 moves e by exactly the jump (L5 never fitted); F3 with α-hat at its upper bound → NO VERDICT; a non-converged status → failure; seed 42 → F3 NO VERDICT; an incomplete seed dropped, one primary seed labelled "(one seed)" with F3 NO VERDICT; no primary seed → NO VERDICT; the mask-2004 row drops exactly image 2004; the descriptive rows carry `label_descriptive`, not `verdict`, and every row's sentence ends with its note; inclusive boundaries; F2 refuses a non-positive point.

## 11. D-beta

The optional frozen D-beta rule of CC-147 was not added (deadline). A later D-beta prereg must therefore be labelled "QLoRA side seen".

## 12. Amendments

None.
