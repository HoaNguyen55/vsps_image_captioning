# Pre-registration v2: B-N2, the KTVIC leaked/clean placebo and descriptive gaps (Paper B), per judge PD-19

- **Status (D-W13-6).** REGISTERED, valid only if this file is committed before the first subset statistic is computed. The absence check (Section 3) found no earlier computation. JSON key: `status_D_W13_6`.
- **Label.** Registered re-analysis of existing outputs.
- **Disclosure.**
  - The per-image KTVIC test outputs of every system named here existed before this registration; their sha256 values are pinned in the JSON under `systems.*.preds`.
  - The only new thing is the statistic on the leaked/clean split, and it has not been computed.
  - The committed full-558 CIDEr-D values were read in order to specify the F0 gate.
- **Files.**
  - Companion JSON: `2026-10-19_b_n2_leakage_did_prereg_v2.json`, built in code by `b_n2_prereg_v2.py` from `b_n2_inventory.json` and `b_n2_absence_check.json`.
  - Decision: `.session_backup/2026-10-13/decisions/PD-19.txt` (JSON `decision.sha256`).
  - This file supersedes the 2026-10-19 DRAFT (JSON `supersedes`).

## 1. Headline leakage DiD: NOT EVALUABLE, deferred

- **Why.** The treated arm is empty: no run of ours was trained with UIT-OpenViIC data (JSON `headline_DiD`).
  - Inventory keys: `arms.treated` = [], `treated_arm_empty` = true, `build_sources_by_kind.openviic` = 0.
  - fuse2 and multiref were built from KTVIC `train_data.json` only. Their build reports and their step/epoch fingerprints show this.
- **Revival.** The DiD revives only when all four of these exist:
  1. a licence check showing that UIT-OpenViIC allows training use;
  2. a new prereg for the OpenViIC-trained run, committed before training;
  3. a GPU plan entry;
  4. a sha-pinned data manifest of its training data.
- **Allowed now.** A feasibility check of availability and licence, which trains nothing.

## 2. What this registers (all short mode)

- **Placebo DiD, fuse2 − P1.** Both arms are KTVIC-only and use the legacy loss mask, with seeds 42, 43 and 44 (JSON `systems.K_P1_legacy_short`, `systems.Kp_fuse2_legacy_short`):
  - K = `p1-gold` (seed 42; commit 92be680, JSON `systems.p1_seed42_link`), `p1_s43`, `p1_s44`;
  - K′ = `fuse2_s42`, `fuse2_s43`, `fuse2_s44`.
  - Seed-matched pairs are given in `systems.seed_matched_pairs`.
- **D1, descriptive leaked − clean gap for every KTVIC-only system** (`systems.D1_all_KTVIC_only_short`): the six systems above plus `p1assist_s42`, `p1assist_s43`, `p1assist_s44` and `mr5assist_s42`.
- **multiref_s42 is excluded from D1 and disclosed.** The three PD-19 (d) checks, with evidence in `systems.multiref_s42_entry`:
  1. Its outputs are in the O-2308423 sha list: true.
  2. The listed shas equal the mirror copies: true.
  3. Its own build report shows KTVIC train only: FALSE, because no build report or sha of the training directory on O-2308423 was mirrored.
  - The row count in the machine log (18,845) matches the KTVIC-only `gold_multiref` builds on n2 and n3. Byte identity is not recorded, so that match is not a pass.
  - Re-entry needs that build report or the `sft.jsonl` sha.
- **zeroshot is not in D1.** We did not train it, and the exposure of its base model is unknown. B-N1 reports the clean-157 sensitivity for zero-shot models.

## 3. Absence check (mandatory; evidence in `b_n2_absence_check.json`)

- **Question.** Has any leaked/clean (401/157) subset metric been computed before for these systems?
- **Scope.** `data/`, `.session_backup/` (task folders, machine mirrors, `gpu_jobs/M1_EVENTS.log`, `M2_EVENTS.log`), `manuscript/` (`WORKFLOW_LOG.md`, preregs, drafts) and `scripts/`.
  - File types searched: text files (json, jsonl, md, txt, log, tsv, csv, py, sh, yaml).
  - Excluded: model checkpoint directories and virtual environments (`excluded.dirs`), and this task's own folder.
- **Stage 1.** `grep -rIl -i -E 'leak|openviic_train_(leaked|clean)|in_openviic_train|not_in_openviic|clean[_ -]?157|157[_ -]?clean|401[_ -]?leaked|leaked[_ -]?401'`. The exact command is in `commands.stage1`; the file list is in `b_n2_absence_check_stage1.json`.
- **Stage 2.** Three tests, on every stage-1 file:
  - (a) the same line names a metric (CIDEr, F1, CHAIR, BLEU, METEOR, ROUGE, precision or recall);
  - (b) a JSON key naming the split holds a metric;
  - (c) a metric appears within 3 lines of a split-specific term.
- **Classification.** Ordered rules, and then an item-by-item review of the hits the rules did not cover. The reviewed items are listed with reasons in `REVIEW` in `b_n2_absence_check.py`.
- **Result.** `n_files_by_category` in the JSON gives the counts; `n_unclassified` = 0. Every hit falls into one of four kinds:
  - another meaning of "leak": CJK or token leakage, leak-free annotator scoring, the prior-leak kill, the paraphrase chain, UIT-ViIC/COCO overlap, or the OpenViIC 8-gram release scan;
  - registration, plan or decision text;
  - the allowed overlap count (401/558) and ID lists;
  - text data such as tokenizer vocabularies, dataset files and literature caches, which are listed and not scanned.
  - **No earlier leaked/clean subset metric exists for any system** (`prior_split_metric_found` = false).
- **Registration overlap (disclosed).**
  - The B-N1 prereg (`manuscript/prereg/2026-10-19_b_n1_vi_leaderboard.md`, commit 327191c) registers LBB-D1, the leaked − clean gap for its reference rows. Those rows include `p1_s43-short` and `fuse2_s42-short`.
  - LBB-D1 is registered but not computed: no B-N1 output exists.
  - Each prereg reports its own method, and neither reuses the other's numbers.
- **Status rule.** REGISTERED holds only if this file is committed before the first computation of any subset statistic. If the check had found an earlier computation, the status would have been POST_HOC.

## 4. Sets

- **Leaked L (401) and clean C (157).** Committed at `data/lb/splits/ktvic_test_openviic_train_{leaked,clean}.txt` (commit 327191c), byte-identical to agent LB's lists. JSON keys: `sets.leaked`, `sets.clean`.
- **Rule.** An image is leaked if it is a KTVIC test image with a matched copy in the OpenViIC TRAIN split. Only IDs are read; no caption is.
- **Checks.** All true (`sets.checks`):
  - the list equals the split-field rule;
  - its count equals the panel summary count;
  - L and C are disjoint;
  - L ∪ C equals the 558 test IDs.

## 5. Methods

- **CIDEr-D, word level, under the protocol card.**
  - **Scorer.** `scripts/evaluate.py` → `rescap.metrics.CaptionMetrics(language="vi", segmenter="rdrsegmenter", tokenize=True)`, pycocoevalcap `Cider`, reported ×100. The file shas are in `methods.cider_d.scorer_files_sha256`.
  - **Per subset.** Make one `Cider().compute_score` call per system over all 558 images, on the tokens from `CaptionMetrics._align` + `_tokenize`, and keep the per-image vector c(i). Then `C_S = 100 · mean_{i∈S} c(i)`. The document frequencies come from all 558 images.
  - **S1 (sensitivity, point estimates only).** Subset-df variant.
  - **S2 (sensitivity, CI, no verdict).** The punctuation fix as defined in B-N1.
- **Object F1 (secondary; CI; no verdict).** `scripts/object_prf.py`: `scores(rows of S)["F1"]`, with `image_counts` against the KTVIC reference gold.
- **Scorer self-check and F0 gate** (`methods.self_check`), for every system:
  1. `CaptionMetrics` over all 558 images, on the `evaluate.py` path, gives a ×100 CIDEr that equals the committed `results[segmenter=rdrsegmenter].scores_scaled_x100.CIDEr` exactly (float equality), with `scorer.segmenter == "rdrsegmenter"`.
  2. F0: `100 · mean_{558} c(i)` equals the same value within 1e-9.
  3. Order of work: this prereg is committed first. The scorer and its self-check output then go through the gatekeeper. Only after both does anyone compute a subset statistic.
  4. Any failure triggers K-F0.
- **Bootstrap** (`methods.bootstrap`).
  - **Draws.** B = 5000 with `numpy.random.default_rng(0)`, stratified: each draw resamples |L| IDs from L and |C| from C, with replacement.
  - **Pairing.** The same draws serve every system and metric.
  - **df.** Fixed at its 558-image value.
  - **CI.** Percentile 2.5 / 97.5.

## 6. Estimands and verdict

- **Gap.** `gap(s) = C_L(s) − C_C(s)`.
- **Placebo.** `DiD_PL = mean_{s∈K′} gap(s) − mean_{s∈K} gap(s)`, with the seed-matched values reported beside it.
- **D1.** `gap(s)` for every D1 system, with its CI.
- **δ = 3.0 CIDEr-D points (×100)** (JSON `delta`). It is quoted from `manuscript/prereg/2026-10-13_upe_mbr.md` line 143 ("…whose KTVIC CIDEr-D change is >= -3.0"); the file's sha256 is in `delta.source.sha256`.
- **Placebo verdict.**

| Verdict | Condition |
|---|---|
| PASS | the 95% CI lies inside (−δ, +δ): ci_lo > −δ and ci_hi < +δ |
| FAIL | the CI lies entirely outside: ci_lo ≥ +δ or ci_hi ≤ −δ |
| INCONCLUSIVE | anything else |

- **Role of the placebo.** It is the control that any later leakage claim on this split needs.

## 7. Kill rules

- **K-F0.** If the self-check or F0 fails for a system, stop; nothing is computed on subsets.
- **K-COV.** A system without predictions for all 558 IDs is dropped and named.
- **K-PL.** If the placebo FAILs, the split interacts with the training recipe even without exposure. No later DiD on this split may then be called leakage inflation unless it has a recipe-matched control.

## 8. Paper B note (PD-19, PD-11 (c))

- **Applies to none of ours.** The PD-11 (c) caveat ("apply the leakage caveat … to every KTVIC test number of a model that saw OpenViIC") applies to none of our models.
- **Still needed elsewhere.** It stays for comparators trained on OpenViIC or of unknown exposure, including zero-shot external models (B-N1 reports the clean-157 sensitivity).
- **For the B-writer.** Correct any text implying that our models were exposed.
