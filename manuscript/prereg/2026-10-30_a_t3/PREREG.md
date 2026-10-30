# Paper A, A-T3: tier-1 dev-explore on COCO, with the tier-2/3 design frozen (FINAL, after CC-184)

Status: FINAL, 2026-10-30. Written under CC-183 (GO-with-fixes 91%, reversible tier; W1–W13). The W11 one-judge
reads are CC-184 (GO-with-fixes 91%; F1–F6 applied here, F7–F12 before their named steps). This file's sha256 is
pinned in `a_t3.py PREREG_SHA256`; the gatekeeper commits it. Gemma-3 is out (CC-184 r2). Done on the laptop before this draft, CPU only, no image and no model output opened: the A registry
(`a_t3_registry.json`), the dev lists (`a_t3_lists.json`), the W3 gate on the dev pool (`a_t3_w3_gate.json`) and the
D1 premise (§3). Nothing has been decoded or scored under this file. **No test look. No test reservation: the
val2017 list is not reserved and is not committed as reserved (CC-183 r9).** Everything below is AI opinion.
Binding: PI-1029n/o (three tiers), full official splits with principled, pre-fixed exclusions reported beside the
full count, one look per test set, no new human labels, no personal e-mail in any request, no host/IP in repo files.

## 0. What A-T3 tests and where it lands

A replication of A's gold-completeness tests on COCO with four pinned LVLMs: InternVL3, LLaVA-OV, Idefics3 and
Aya-Vision. They span three LLM families (Qwen2.5/Qwen2, Llama-3.1, Command R7B; two of the four LLMs are
Qwen-family) and three vision encoders. None was used in A's XM3600 label-gold tests (to verify against A's XM3600
X4/X5 headline before any public sentence, CC-184 F3); three also appear in A's eight-LVLM ladder. The point is
system dependence (meta-review item 6) and a premise that is measured before any decode (item 5(b)). It is not a
new-domain claim.

- **Joint primary (CC-183 r4, W4).**
  - **AD-1′** = slope[L | COCO-80] − slope[R1 | COCO-80] > 0. It compares the label gold L with ONE reference R1,
    drawn by the frozen `p50.draw()` (rng 1, 20 replicates). AD-1′ is a **NEW variant**, chosen by A-T1's
    output-free premise rule on gold sizes (§3). It was never "copied from A-T1", because A-T1 §3 used a union over
    references.
  - **AD-2 = X5:** the R1∩L gold gives a lower slope than size-matched random deletions from L.
  - Claim = AD-1′ PASS **and** X5 PASS, each at one-sided 0.025 (intersection–union). A single-test claim uses Holm
    over the family, so the passing test needs p ≤ 0.0125 with two members.
  - Sign rules only, no SESOI. The scout's +2.0 is rejected.
- **L vs R5 (W5).** This is the faithful A-T1 §3 transplant. It is registered, computed and **always reported with
  its CI as PREMISE_NOT_MET**, because the dev-pool L/R5 is 1.385 < 2.
  - The paper never says "A4 replicates" or "label > every reference gold".
  - It says "label > one reference" and discloses the ≈ 2× size advantage of L over R1.
- **X4 (r5, W6).** R1 gives a lower slope than size-matched random deletions from the union of all references. X4
  joins the Holm family only if tier 1 gives X4 PASS **and** a predicted P(PASS) ≥ 0.98. Otherwise it is
  descriptive.
- **O2 (secondary).** The slope rises at each rung R1 → R2 → R5. It is labelled near-mechanical, since the gold grows
  ≈ 1.5× and L is ≈ 2.1× R1.
- **Placement (W12).** No new section:
  - one paragraph in §6.4, after the PASCAL-50S result;
  - one sentence in §6.6 (X4/X5);
  - two rows in Table 1;
  - details in the supplement.

  The sentences are fixed in §7. Every FAIL is reported briefly. A-T3 adds ≤ 400 words within the 9,000-word cap.

## 1. Data, exclusions and custody

- **Images.**
  - Tiers 1–2: COCO **train2017** files, fetched one by one from images.cocodataset.org/train2017/ by `stage`. They
    carry no request headers and no e-mail. train2017 holds no val2017 image.
  - Tier 3: COCO val2017, on M1 (role m3) only.
- **Gold.**
  - Labels: COCO 2017 instance annotations, from `annotations_trainval2017.zip` (sha256 113a836d…, the scout's pin).
    Tiers 1–2 read only the member `annotations/instances_train2017.json`, which holds no val2017 image by
    construction. The val2017 member is read by `gold --set test` on m3 only, after r9 (the code refuses it
    elsewhere).
  - References: Karpathy `dataset_coco.json` (2fd99922…). It is read by id, and val2017 rows are refused off m3.
  - COCO-80 instance gold is **annotated, not exhaustive** (W12). RePOPE-type label errors exist and are cited in
    the text.
- **Dev pool (r7, W9).** Karpathy restval (30,504) minus the 3,799 val2017 ids, minus every exclusion.json coco
  list (CHAIR-500: 319 more ids, POPE-500: 314; the other lists have 0 in restval) = **26,077**. The pool is ordered
  by sha256(str(cocoid)).
  - **D1** = first 1,000 (tier 1), **D2** = next 1,000 (tier 2), smoke = next 20 (listed, not decoded).
  - **Deviation from CC-183 r7, accepted by CC-184 r1 (r7 amended by name).** Dev↔test near-duplicates are
    dropped **from the test side**; the reference set for that pass is fixed as D1 ∪ D2 ∪ smoke (2,020 ids),
    whether or not tier 2 runs. D1/D2 do not move. The cost (a few test ids) is counted beside 5,000.
  - **Dev-side W2 (CC-184 F8).** Before `score --tier 1`, m3 runs `neardup` for D1 ∪ D2 against Karpathy test, KV,
    CHAIR-500, POPE-500, cv295, PASCAL-50S, NoCaps val and F30K test (XM3600 only if the PI answers CC-183 Q5 = b).
    Hits leave the tier-1/2 analysis set through `score --exclude` (sha and count recorded); the lists do not change.
  - Sources:
    - val2017 ids: `val2017_ids.txt` in this directory (5,000 ids, ea37cee0…), the guard input and not a
      reservation. It was made from `.session_backup/…/val2017_names.txt` (612097d2…), which is not in git. W1
      re-checks the ids against `instances_val2017.json` on m3.
    - exclusion.json (c52a96d1…).
- **Exposure mismatch (W9).** D1/D2 are inside train2017, which most LVLM training mixes include. val2017 is the
  usual held-out split. The tier-2 P(PASS) is therefore labelled **possibly optimistic**.
- **Test list (W1; built later, by id only, not reserved here).** val2017 (5,000) ∩ restval = 3,799, then:
  - minus CHAIR-500/POPE-500 = 3,693;
  - minus C's 8 near-dup drops = 3,685;
  - minus Flickr-id hits (F30K, NoCaps val, OIV7 val);
  - minus any id decoded by any study, smokes included;
  - minus the W2 drops.

  `a_t3.py testlist` prints every count beside 5,000. It refuses to write an unreserved list into the repo.
- **Memory (r1).** All 3,693 candidates are in C's retrieval memory: their captions were used as exemplars, and the
  images were never decoded or scored by C. For A they are "unused by A, not pristine, disclosed" (CC-171 pattern).
- **Exclusions (r3).** Karpathy test 593, KV 608, CHAIR-500 73, POPE-500 74, C's 8, the Flickr hits and the W2 drops
  are all pre-fixed and disclosed by id, with counts printed beside 5,000. There is no full-5,000 result, because
  scoring those images would be a second look.
- **XM3600 (r6, Q5).** Default (a): the Flickr-id map plus byte-sha only, with the 1,745 unchecked ids disclosed. If
  the PI says (b), the W2 pass adds the cached XM features on m3. No XM3600 image is staged anywhere for A.
- **Custody disclosure (W8, r8).** These are deviations from A-T1 §1. None is an outcome look.
  - (i) The scout read val2017 instances and captions on the laptop and printed aggregates only (premise 2.162 /
    1.173 / 1.404; scout §6).
  - (ii) The other tool's scratch on the laptop still holds an extracted `instances_val2017.json` and the full
    2017 zip.
  - (iii) `dataset_coco.json` on the laptop holds the Karpathy captions of the val2017 images (it has for months;
    A-T3 code refuses those rows off m3).
  - (iv) The W3 numbers below were computed after the val2017 ratio (2.162) had been seen.
  - (v) The A-T3 author and the CC-184 judge read only the train2017 member of that zip on the laptop (no caption
    text printed). Per CC-184 r5/F11 and PI-1030d: D1/D2 gold was built and its shas logged, then the extracted
    `instances_val2017.json` and the 2017 zip were deleted from the laptop (OPS line in LOG.md); m3 re-downloads the
    zip at pin 113a836d for `gold --set test`.
  - From now on, val2017 gold and images live only on m3. M2's guard refuses val2017 ids and names everywhere under
    `$NCS_DATA/datasets`, and val2017 image shas in the A-T3 staging dir. It fails closed without the m3-made sha
    list.

## 2. W3 gate on the dev pool and the W1b erratum (logged in LOG.md, CC-184 F12)

| Set | n | Σ\|L\| | Σ\|R1\| | L/R1 | L/(2·R1∩L) | L/R5 | gate R1 | A-T1 form (L vs R5) |
|---|---|---|---|---|---|---|---|---|
| dev pool (restval − val2017 − exclusions) | 26,077 | 74,566 | 35,472.4 | **2.102** | **1.138** | 1.385 | holds | fails |
| D1 | 1,000 | 2,855 | 1,360.5 | **2.098** | **1.133** | 1.385 | holds | fails |
| D2 (CC-184 recount) | 1,000 | 2,829 | — | **2.094** | **1.129** | 1.399 | holds | fails |

- Computed by `a_t3.py gold --set pool` (`a_t3_w3_gate.json`, counts only) and `gold --set D1` (laptop, CPU,
  2026-10-30).
  - L = categories with any instance, crowd included.
  - R_k = union of the matcher classes of k references drawn by `p50.draw()` (rng 1, 20 replicates, mean over
    replicates).
  - Matcher: score_g2b `MATCH["coco80"]["en"]`, unchanged. The 80 category names are asserted to map to themselves.
- These numbers alone justify R1: they still select R1 and still reject the R5 form.
- Disclosed: the val2017 ratio (2.162) was seen first (scout), and the earlier restval figures (2.09 / 1.13 / 1.39)
  included the 3,799 val2017 ids (J2, r8).
- The margins are small (D1 2.098, D2 2.094 vs 2); the gate is a premise, not the effect (CC-184 r3). The tier-3 gate
  is computed on m3 (W7).
- LOG lines (appended 2026-10-30):
  - "A-T3 W3: dev pool 26,077 L/R1 2.102, L/(2·R1∩L) 1.138, L/R5 1.385; D1 2.098/1.133/1.385; R1 kept; val2017
    2.162 seen first (disclosed)."
  - W1b erratum: "Scout l.104 'never scored' is false for 53 POPE-500 ids in restval; C memory holds 3,693/3,693
    candidates, not ~3,640."

## 3. Gold rungs and the premise (frozen now)

- L_i = COCO-80 categories with ≥ 1 instance (crowd included). R1, R2, R5 = `p50.draw()` k = 1, 2, 5. An image with
  6–7 references draws 5 of them for R5. R_all = the union of all references, used as X4's complete set.
- **Premise (output-free, before every decode).** Σ|L| / Σ|R1| ≥ 2 and Σ|L| ≥ 2·Σ|R1∩L|. `stage` refuses if it
  fails on its set. D1 holds (§2). Tier 2 repeats the gate on D2 before its decode.
- **Tier 3.**
  - The premise is computed on m3 by `gold --set test` before the first decode.
  - It is logged as **known-to-pass and non-informative**, because 2.162 was seen.
  - If it fails, there is no decode and this sentence is used: "On the reserved COCO val2017 images, the label rung
    was measured before decoding and was not twice as large as one reference, so the label-step and salience tests
    were not run (PREMISE_NOT_MET)."

## 4. Systems (W10) and decode

- **Decode.** Decoder `scripts/lb/decode_hf_vlm.py` (e2de1881), unchanged. The A-N2 schema, decode, decoder and venv
  blocks (d5714e2b…) are copied by `register`. short_en/detailed_en, greedy, 60/160 new tokens.
- **A registry (`a_t3_registry.json`).** Each model block is copied unchanged from its pinned source; `registry
  --check` re-verifies this in every job.

| Model | Pin | LLM family | Vision encoder (verify at pin) | Source | Host |
|---|---|---|---|---|---|
| InternVL3-8B-hf | 259a3b64 | Qwen2.5 | InternViT-300M | A-N2 | M2 |
| LLaVA-OV-7B | 0d506805 | Qwen2 | SigLIP-so400m | A-N2 | M2 |
| Idefics3-8B | fddb4ff7 | Llama-3.1 | SigLIP-so400m | A-N2 | M2 |
| Gemma-3-4B-it | 093f9f38 | Gemma 3 | SigLIP-400M | L1-b | OUT (CC-184 r2) |
| Aya-Vision-8B | d7601ac8 | Command R7B | SigLIP2-so400m | C-T1 | M1 |

- **Wording (CC-184 F3).** Models are named and described by vision encoder and LLM family. Never "non-Qwen" and
  never "outside our main Qwen-VL set". The operator records each vision tower from the snapshot's config.json at
  the pin in the run log (names only).
- **Gemma: OUT for all three tiers (CC-184 r2).** Its four LFS hashes were null at finalisation, so there is no late
  fill (CC-168b W16); `SOURCES` pins the L1-b registry sha, so a later fill fails `registry --check`. In-set: 4 models
  / 8 runs.
- **Aya drop/move rule (Q7 default).**
  - Aya's D1 cells run on M1 only, after C-T1 has ended and been mirrored, staged outside C-T1's guard roots. The
    snapshot is checked at its pins and never fetched by the job.
  - The tier-1 score waits for both Aya cells until the earlier of 72 h after M2's tier-1 BLOCK DONE and
    **2026-11-03T00:00Z** (`AYA_DEADLINE`; CC-184 F9 default, as the M1 rental end is not the binding limit).
  - If both cells are not present by then (or Aya stops on KD, a pin, OOM or the cap), Aya is out of A-T3 for all
    tiers and is never added back. The drop is recorded by setting `AYA_OUT` = its LOG id; until then `score --tier
    1` refuses to score without Aya (model-set lock, F9).
  - A move to M2 (PI token per command) is allowed only before any tier-1 score.
- **Model set.** The set scored at tier 1 is the set for tiers 2–3 (read from the tier-1 result; `score` refuses any
  other), with ≥ 3 models (`p50.MIN_MODELS`).

## 5. Statistics (laptop CPU; tier 3 on m3)

- **Slopes.** Per run, mixed F1 against a gold rung, with replicate golds averaged by score_g2b `rows`. Slope = OLS
  of 100·F on ln M across the runs (models × 2 prompts), with images and systems held fixed. The analysis set is
  images with a clean, non-empty caption from every run.
- **Bootstrap.** Multinomial image weights, 1,000 draws, seed 0, 95% percentile CI.
- **AD-1′, L vs R5, O2 steps.** Slope differences, rule `sign_gt_0`. One-sided p = (1 + #draws ≤ 0)/(B + 1).
- **Premise at score time (CC-184 F6, r3; A-T1/CC-170b precedent).** Recomputed on the clean-caption analysis set
  from the same replicate draws as the slopes. If it fails there while the pre-decode gate held, the verdict is
  PREMISE_NOT_MET, reported with `n_dropped_unclean`; no re-scoring and no re-cleaning.
- **X5 then X4.** One `default_rng(0)` stream, `p50x.salience` unchanged, 1,000 null replicates.
  - X5: gold R1∩L, complete L. It is NOT_EVALUABLE if Σ|L| < 2·Σ|R1∩L|.
  - X4: gold R1, complete R_all.
  - PASS iff observed < null 2.5th percentile. p = (1 + #null ≤ obs)/(R + 1).
- **Tier-1 predictors (planning only).** `a_t1.predict` / `predict_null` scaled to **N_TEST_PLAN = 3,500**, a fixed
  lower bound that is never replaced by the W1 count.
- **Tier-2 rehearsal (W7).** AD-1′ by the bootstrap predictor. X5 by an image bootstrap of the salience z (200
  resamples × 200 null replicates, seed 0) scaled to 3,500. Both must be ≥ 0.98.

## 6. Outcomes

**Tier 1 (D1; clauses in this order; `outcome1`):**

0. **PREMISE_NOT_MET** (D1 gate; it holds) → no decode.
1. **NOT_REPRODUCED** if AD-1′ or X5 is not PASS → no tier 2; one dev-ablation sentence in the supplement.
2. **PASS_LOW_POWER** if min P(AD-1′, X5) < 0.98 → stop.
3. **X4_NOT_EVALUABLE** → tiers 2–3 only if the PI accepts an AD-1′/X5-only replication.
4. **PROCEED_TO_TIER2** otherwise. The X4 promotion (r5) is recorded and binds tiers 2–3.

For clauses 2 and 3 the Q8 default is to stop and submit A with text + G0 + one dev-ablation sentence.

**Tier 2 (D2, exact tier-3 code, run once).** REHEARSAL_PASS iff AD-1′ and X5 PASS and both P ≥ 0.98. Otherwise
REHEARSAL_FAIL, and the test is never touched.

- **Tier-1 binding (CC-184 F1).** Tiers 2–3 run only from a tier-1 result with PROCEED_TO_TIER2, or with
  X4_NOT_EVALUABLE when the constant `PI_X4_ACCEPT` holds the PI's LOG id. PASS_LOW_POWER never proceeds. The X4
  promotion and the model set are read from that file (`score --tier1`, sha recorded), never set by hand.
- **Score output (F9).** `score` writes only `data/results/a_t3/tier{n}.json` and refuses if it exists.

**Tier 3 (one look).** Only after the r9 re-read reserves the W1 list (`TEST_RESERVED`).

- **Frozen at this commit:** the tier-3 analysis, scoring, outcome and premise code (`gold --set test` and
  `score --tier 3`, both on m3).
- **Deviation from CC-183 W7 ("tier-3 code frozen at commit"; CC-184 F5):** test staging and the tier-3 decode job
  are not frozen here. They are limited to the unchanged decoder, the same registration blocks and prompts, and
  run ids `at3t3_*`, and they land in the r9 commit, covered by the r9 re-read.

## 7. Paper-facing text (fixed now; ≤ 400 words; W12)

**§6.4 paragraph.**

- **Joint PASS:** "On COCO val2017 images unused by A (n = N after pre-fixed exclusions of 5,000, listed in the
  supplement), with four LVLMs not used in our XM3600 label-gold tests (InternVL3, LLaVA-OV, Idefics3, Aya-Vision;
  three LLM families, two Qwen-family), the label gold measured before decoding
  was about twice the size of one reference (r = …). The label gold gave a larger verbosity slope than one reference
  (+x [lo, hi]). One reference gave a lower slope than size-matched random deletions from the label gold (p = …).
  This was registered, one look, conditional on the systems scored. Against the union of five references the label
  gold was not twice as complete, so that comparison is reported as premise not met (+y [lo, hi]); we do not claim
  that label gold exceeds every reference gold."
- **One test PASS (Holm):** "… the label step passed (…); the salience test did not (p = …)", or the reverse. A claim
  stands only at p ≤ 0.0125; otherwise "nominal, not claimed".
- **Neither:** "On COCO val2017 the label-step and salience tests did not pass (…); the label-gold claim stays scoped
  to XM3600."

**Other placements.**

- **Three models (Aya dropped):** the same sentences with "three LVLMs (InternVL3, LLaVA-OV, Idefics3; two of
  the three with Qwen-family LLMs)".
- **Stopped at tier 1 or 2, by power, budget or date:** "A dev-set replication on COCO with four [three] other LVLMs
  stopped before the test under its pre-registered rules, so no test look was made (supplement)."
- **§6.6:** "X4 on COCO: … (descriptive unless promoted by its pre-written power rule)."
- **Table 1:** two rows, AD-1′ and X5, with L vs R5 marked PREMISE_NOT_MET.
- **Supplement:** O2 (near-mechanical), the exposure mismatch, custody, memory, and the exclusions beside 5,000.

## 8. Machines and budget (cap `CAP_GPU_H` = 40 GPU-h, PI-1030d answering CC-184 P1)

- **Timing basis.** From P50's ledger (same decoder, 1,000 images, RTX 3090): InternVL3 4,854 s and LLaVA-OV
  4,039 s. Idefics3 ≈ 4,900 s and Aya ≈ 4,900 s are estimated from Idefics3's smoke ratio and assumed for Aya.
  Gemma ≈ 2,500 s if it is in.
- **Tier 1.** M2: 3 models ≈ **3.8 GPU-h**, 4.5 with Gemma; cap 6. M1: Aya ≈ 1.4; cap 2.
- **Tier 2.** ≈ 5.2. On M2 if before ~11-02, else M1.
- **Tier 3.** ≈ 19 on M1 (m3), for ≤ 3,685 images.
- **Total.** ≈ 29.6 against the 40 GPU-h cap (PI-1030d), leaving room for loads and one host-loss rerun.
- **Cap constant.** `a_t3.py CAP_GPU_H` = 40 is the single A-T3 cap (all tiers, all machines), set by PI-1030d before
  any decode; it is never changed after a decode starts.
- **Stop rule (r10, CC-184 F2).** After tier 1: projected = GPU-s spent on all machines + Σ over the in-set runs of
  (that run's measured seconds per image) × (1,000 + 3,685). If projected > `CAP_GPU_H`, tiers 2–3 do not start.
- **Date stops (F2).** No tier-2 decode starts after 2026-11-05T00:00Z and no tier-3 decode after 2026-11-07T00:00Z
  (`DATE_STOP`; `register` and the job's `datecheck` refuse). If missed, A-T3 stops and the §7 "stopped" sentence is
  used. This protects the 11-10 freeze.
- **Host loss (F4; CC-177/CC-180 pattern).** Before any restart the operator closes the open run with one ledger row:
  the run label, wall = (the last partial-file or log mtime) − the START timestamp in EVENTS, rc 137. The cap
  arithmetic then counts it. A resumed run keeps its run key (decode_hf_vlm resumes by slice).
- **Start conditions.** Tier 1 on M2 starts only after this commit, setup_gpu.sh steps 6–8, the selftests and the
  end of L1-b. It never pre-empts (CC-181 r7).

## 9. Steps before tier 1 (in order)

1. W11 judge reads.
2. Gemma decision.
3. On m3: `valsha` gives the 5,000 val2017 image shas (numbers only; ids checked, F7), under CC-182 conditions
   while C-T1 runs. Pin the sha in `VALSHA_SHA256` (a pins-only commit) and copy the file to M2.
4. Gatekeeper commit of this file.
5. M2: `stage --set D1`, `register`, `a_t3_job.sh <HEAD>`.
6. M1, after C-T1: the same steps for Aya.
7. On m3: the dev-side W2 pass (F8). Laptop: `score --tier 1 --exclude <drop ids>`.

The test-side W2 and W1 passes (F10 named drop files) and the r9 re-read are needed before tier 3 only.

## 10. Files

- `scripts/a_t3/a_t3.py`, `scripts/a_t3/a_t3_job.sh`, `scripts/a_t3/SHA256SUMS`.
- Reused unchanged: p50.py, p50x.py, a_t1.py, score_g2b.py, decode_hf_vlm.py, c_stage1/build_memory.py (W2) and
  grl/common.py (guard).
- Selftest: `python3 scripts/a_t3/a_t3.py --selftest` (synthetic only).
- This directory: PREREG.md, a_t3_registry.json, a_t3_lists.json, a_t3_w3_gate.json, val2017_ids.txt,
  JUDGE_READ_REQUEST.md, SHA256SUMS.

## 11. CC-183 W-items

| Item | Status in this draft |
|---|---|
| W1 | Code (`testlist`); not run into the repo, not reserved |
| W1b | Proposed LOG line (§2) |
| W2 | Code (`neardup`, m3 only); test-side drops (stated deviation, §1) |
| W3 | Done (§2) |
| W4 | §0 / §5 |
| W5 | §0 / §7 |
| W6 | §6 |
| W7 | §3 / §5 / §6 (staging/decode deviation, CC-184 F5) |
| W8 | §1, guard |
| W9 | §1 |
| W10 | §4, registry |
| W11 | JUDGE_READ_REQUEST.md |
| W12 | §1 / §7 |
| W13 | Not now (after r9) |
