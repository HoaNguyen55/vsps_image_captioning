# Paper A, A-T1: tier-1 dev-explore for a registered gold-completeness test with a MEASURED completeness premise (FINAL, v3.1 after CC-170b GO 92%)

Status: FINAL, 2026-10-30, after CC-170 (GO-with-fixes 91%; W1–W13), CC-170a (GO-with-fixes 90%; W2′, W5′, N1–N6, W8)
and CC-170b (GO 92%; W5″, V1–V3), see §11. Before this commit, on M1 (role m3), CPU only: G2 downloads and pins (§1),
`split`, `select` (`a_t1_lists.json`) and `gold --set D1` (resolved V in §3; the D1 premise is logged in LOG.md).
Nothing decoded or scored under this file. Everything below is AI opinion. Binding: PI-1029n (three tiers), PI-1029q (public
datasets usable), PI-1029r (fit the storyline; no new section), full official splits, one look per test set, no new
human labels (AI labels are not evidence), no personal e-mail in any request, no host/IP/port in repo files.

## 0. Why this experiment (storyline fit first)

Paper A's storyline (revision 1 title): *Gold Completeness and the Verbosity Slope of Object Hallucination Metrics:
A Registered Audit*. The meta-review (A_META_REVIEW items 4–5) says the low-risk part (reference rungs ordered) is
near-mechanical, and the risky part, label gold > every reference gold, has one PASS (XM3600, verified precision),
one weak PASS (second backbone, bracket lower bound +1.97 [−0.44, +4.01]) and one FAIL (PASCAL-50S label step,
−2.29 [−5.15, +0.61]). Item 5(b): the FAIL may mean the VOC-label rung was not more complete than 50 references; that
premise "was assumed, not measured". The only informative registered PASS is X4 (salient few-reference gold gives a
lower slope than size-matched random deletions); its label-gold twin X5 was NOT_EVALUABLE because the label rung was
too small (Σ|voc20| 1,782 < 2 Σk 2,079.2).

A-T1 tests both on a gold whose completeness is exhaustive by construction and **measured before any decode**:
ADE20K pixel labels (every pixel labelled) vs one Localized Narrative per image.

**Where it lands (no new section; CC-170 W7):** one paragraph in §6.4 (after the PASCAL-50S result), one sentence in
§6.6 (X4/X5), two rows in Table 1, details in the supplement. AD-2 leads the paragraph. Wording is fixed now (§7.1).
The PASCAL FAIL may be called "consistent with" an incomplete label rung, never "explained by" it.

### 0.1 Candidates (ranked by fit, then P(PASS), then reviewer gain)

| # | Candidate | Fit | Tier-3 set | Owner / spent? | P(PASS) prior | Reviewer gain | Tier-1 GPU-h |
|---|---|---|---|---|---|---|---|
| **A-1 (chosen; CC-170 91%)** | ADE20K exhaustive labels vs Localized Narratives: label step (AD-1) + label-gold salience null (AD-2, the X5 form) | exact (items 4, 5(b)) | full ADE20K SceneParsing validation split, 2,000 images | unused, unowned (no ledger line, no prereg; ledger line requested, §9) | AD-1 ≈ 0.8, AD-2 ≈ 0.85, joint ≈ 0.7 before tier 1 | correctness +0.25–0.5, contribution +0.25 | ≈ 6.2, cap 10 |
| A-2 (CC-170 40%) | COCO val2017 + LVIS v1 vs 5 COCO references | exact | COCO val2017 | same val2014 pool as the spent Karpathy test and A's own COCO sets; LVIS not exhaustive per image | ≈ 0.8 | similar, re-used COCO images | ≈ 8 |
| A-3 (CC-170 20%) | Visual Genome paragraph test + VG object labels | partial (labels not exhaustive) | VG paragraph test | about half COCO images | ≈ 0.6 | lower | ≈ 6 |

Rejected outright: OpenImages V7 test + LN (125k images; full-split rule makes it > 100 GPU-h; OIV7 val belongs to
L2-P1); AMBER (no human references; L2-P2 fallback); nocaps val, COCO Karpathy test, XM3600, PASCAL-50S (spent);
Flickr30K test (C).

## 1. Data and custody (CC-170 W3)

- ADE20K SceneParsing release `ADEChallengeData2016.zip` (MIT CSAIL): images/{training 20,210, validation 2,000},
  annotations/ (PNG, pixel value = class index 1–150, 0 = unlabelled), objectInfo150.txt.
- Localized Narratives (Pont-Tuset et al., ECCV 2020; CC BY 4.0, verified on the project page 2026-10-30):
  `ade20k_train_captions.jsonl` (20,476 narratives) for tiers 1–2; `ade20k_validation_captions.jsonl` (2,053) for
  tier 3 only, fetched on M1 only. Narrative text never enters the repo.
- **Custody.** The full zip is fetched and opened **on M1 (role m3) only**. `a_t1.py split` (CPU, refuses unless
  machine id = m3) writes (a) a training-only archive (training images, training PNGs, objectInfo150.txt) and (b) the
  pHash/dHash numbers of the 2,000 validation images. Only (a) and (b) leave M1. The laptop and M2 never hold a
  validation image, label or narrative.
- **G2 gate (before `split`):** `PIN` holds sha256 of the full zip, the training-only archive (recorded in M1's
  EVENTS by `split`), objectInfo150.txt and the train narratives; ADE20K terms of use quoted in the run record
  (PI-1029q covers use). Downloads use no e-mail and no personal header.
- **G2 pins (2026-10-30, official sources):** `ADEChallengeData2016.zip` from data.csail.mit.edu/places/ADEchallenge
  (sceneparsing.csail.mit.edu; its page states "License: BSD 3-Clause License") 7ff1be44…; objectInfo150.txt (member
  of that zip) c368be0c…; training-only archive (`split`) 2f2042c4…; `ade20k_train_captions.jsonl` (20,476 lines) from
  storage.googleapis.com/localized-narratives/annotations 78a0a878…. Full values in `a_t1.py PIN`. Zip members:
  training 20,210 images + 20,210 PNGs, validation 2,000 + 2,000.

## 2. Sets (fixed by `a_t1.py select` on the laptop, ids only, before any decode)

- Candidates: ADE20K **training** images with an annotation PNG and ≥ 1 narrative; minus every candidate within
  min(pHash, dHash) ≤ 10 (candidate mirror included; B-R1 rule) of any validation image, from (b). Ordered by
  sha256(image id). `select` refuses if the archive holds any validation member.
- D1 = first 1,000 (tier 1), D2 = next 1,000 (tier 2; never decoded or scored in tier 1), smoke = next 20 (listed,
  not staged or decoded). Sizes asserted (W6). Tier 3 = all 2,000 validation images (full official split).

## 3. Vocabulary, gold rungs and the premise (frozen now)

- **Resolved map (W2′ applied by `gold --set D1` to the pinned objectInfo150.txt, 2026-10-30; V1):** |V| = 24, V =
  {airplane, bed, bench, bicycle, boat, book, bottle, bus, car, chair, clock, couch, dining table, microwave, oven,
  person, refrigerator, sink, sports ball, toilet, traffic light, truck, tv, vase} (person kept; none removed).
  Resolution log: added 32 seat → chair, 57 pool table → dining table, 88 streetlight → traffic light, 103 van → car,
  111 stool → chair, 117 minibike → bicycle. Resolved map (36 indices): the 30 below plus these 6.
- **Class map, forward direction (W2, fixed before data):** an ADE20K-150 class is kept iff the frozen English
  matcher maps its listed ADE name to exactly {that COCO-80 class}. Start map: 30 ADE indices → V = 24 COCO names before the W2′ resolution
  (`a_t1.py ADE2COCO`); dropped: armchair (no match), minibike (→ bicycle), crt screen (no match). Departure from
  CC-170's wording, stated: the rule tests the listed name only, not every WordNet synonym, because rare synonyms
  (e.g. "passenger vehicle" → person) would empty V. Pre-declared descriptive sensitivity (no verdict): AD-1 and AD-2 recomputed with the classes added
  by the W2′ resolution excluded from L, N and the model mentions; computed by the tier-2 prereg's code on the D1
  outputs and reported beside the primary.
- **Reverse direction (W2′, CC-170a):** `gold` first reads only the pinned objectInfo150.txt and lists every UNMAPPED
  class any of whose names or synonyms the matcher sends into V (e.g. stool → chair, minibike → bicycle). Resolution
  rule, fixed now and repeated to a fixed point: if the class's first-listed name gives exactly one V class, the class
  is added to the map for that class; otherwise each V class it hits leaves V (with its map entries). `gold` refuses
  if any conflict remains. The resolved map, V and the resolution log are written into the D1 gold file and copied
  into the final PREREG.md before any score; narratives are read only after this gate. V1 (CC-170b): after
  `gold --set D1`, |V|, V, the resolution log and the D1 premise are logged in LOG.md before `stage`.
- `gold` refuses unless objectInfo150.txt is present, matches its pin, and each ADE name is among its index's
  comma-separated synonyms (W1; tested on the real tab/comma format).
- Matcher: score_g2b `MATCH["coco80"]["en"]` unchanged; model and narrative mentions both restricted to V.
- Label rung L_i: mapped classes covering > 0.1% of the pixels (primary). 0 (any pixel) and 0.5%: descriptive only.
- Narrative rung N_i: matcher classes in V over all narratives of image i (1, rarely 2).
- **Premise (output-free; W4: computed by `gold` on D1 and logged BEFORE `stage`; tier 2 repeats the gate on D2
  before its decode, `stage --set D2`, N3):** Σ|L| / Σ|N| ≥ 2 and
  Σ|L| ≥ 2 Σ|N ∩ L| (X5's evaluability condition). `stage` refuses unless both hold, so a failed premise costs no GPU.

## 4. Systems and decode (A-N2, unchanged)

A-N2 registration (d5714e2b…) models, decode, decoder (decode_hf_vlm.py e2de1881) and venv blocks copied unchanged
by `a_t1.py register` (p50.register pattern; D1 only). Seven models in P50's kept order (qwen3vl_8b, qwen25vl_7b,
qwen25vl_3b, smolvlm2_2b, llava15_7b, internvl3_8b, llava_ov_7b); short_en and detailed_en; greedy. 14 runs.
Model outputs stay off the repo; their sha256 sidecars are kept (W12).

## 5. Statistics (laptop CPU, once; P50/X5 code reused)

- Per run: mixed F1 against a gold rung (score_g2b `rows`/`scores`), mean mentions M; slope = OLS of 100·F on ln M
  across the 14 runs (`stat_slope`); images and systems held fixed (results are conditional on the systems scored,
  W13). Bootstrap: multinomial image weights, 1,000 draws, seed 0, 95% percentile CI. Analysis set = images with a
  clean non-empty caption from every run.
- **AD-1 (label step):** slope[L | V] − slope[N | V]; rule `sign_gt_0` (PASS iff CI_lo > 0; FAIL iff point ≤ 0).
  One-sided p = (1 + #draws ≤ 0) / (B + 1).
- **AD-2 (salience, X5 form):** p50x.salience with gold = N ∩ L and complete set = L, 1,000 size-matched random
  deletions (rng 0). PASS iff observed < null 2.5th percentile; one-sided p = (1 + #null ≤ observed) / (R + 1);
  NOT_EVALUABLE if Σ|L| < 2 Σ|N ∩ L|.
- **Multiplicity (W5):** the tier-1 GO and the joint confirmatory claim need BOTH AD-1 and AD-2 to PASS
  (intersection–union), so no adjustment applies to them; each test is at one-sided 0.025. A single-test claim at
  tier 3 uses Holm over the pair: the passing test needs one-sided p ≤ 0.0125, otherwise "nominal, not claimed"
  (§7.1). Both p-values are always reported.
- **Predicted P(PASS on validation 2,000):** AD-1 = mean over draws d of Φ(d / SE_3 − 1.96), SE_3 =
  SD(draws)·sqrt(n_D1 / 2,000); AD-2 = Φ(z·sqrt(2,000 / n_D1) − 1.96), z = (null mean − observed) / null SD. The AD-2
  predictor ignores the sampling variance of the observed slope (W10), so it is a tier-1 planning number only; the
  tier-2 prereg replaces it by an image-bootstrap of the observed-minus-null excess.

## 6. Tier-1 outcome (clauses in this order)

0. **PREMISE_NOT_MET** (before any GPU, from `gold` on D1): → no decode; supplement sentence "the label rung was
   measured and was not twice as complete as one narrative on ADE20K training images".
1. **NOT_REPRODUCED** if AD-1 or AD-2 is not PASS. → No tier 2; one supplement sentence (dev ablation).
2. **PASS_LOW_POWER** if min(predicted P) < 0.98. → Stop, unless the PI grants an exception (PI-1029n gives no
   lower-P route to a test look).
3. **PROCEED_TO_TIER2** otherwise. → Tier-2 prereg on D2 (exact tier-3 analysis, run once, M2).

Tier-1 freedom is limited to the descriptive items above (share thresholds 0 and 0.5%, per-model slopes).

## 7. Draft tier-3 rule (copied verbatim into the tier-3 prereg)

On the 2,000 validation images (M1, role m3), same models, prompts, V, SHARE_MIN, matcher and statistics. The
premise is computed from validation labels and narratives on M1 and logged before the first decode. Registered
claim = AD-1 PASS and AD-2 PASS. Reported in full whatever the outcome.

### 7.1 Paper sentence per tier-3 outcome (fixed now)

- Both PASS: "On ADE20K, where the label rung was measured to be at least twice as complete as one narrative
  (ratio r), one narrative gave a lower verbosity slope than size-matched random deletions from the label gold
  (p = …), and the label gold gave a larger slope than the narrative (+x [lo, hi]); registered, one look,
  conditional on the seven systems scored. This is consistent with the PASCAL-50S failure reflecting a label rung that
  was not more complete."
- Exactly one test PASS (W5′): Holm over the pair at tier 3. The passing test's claim stands only if its one-sided
  p ≤ 0.0125; otherwise the cell reads "nominal, not claimed".
  - AD-2 PASS with p ≤ 0.0125, AD-1 not PASS: "… salience-driven missingness was again detected (p = …), but the
    label step did not pass (…)"; the label-gold claim is narrowed to XM3600.
  - AD-1 PASS with p ≤ 0.0125, AD-2 not PASS: "… the label step passed (…); the salience test did not (p = …)."
- Neither, or premise not met: one sentence in §6.4 with the numbers; the label-gold claim stays scoped to XM3600.

## 8. Machines and budget

| Tier | Data | Machine | GPU-h |
|---|---|---|---|
| 0 (CPU) | split of the zip | M1 (role m3), CPU only | 0 |
| 1 | D1, 1,000 training images | M2 (role m4, dev-only); the guard refuses any ADE_val/validation file, any `ADEChallengeData` path, any `.zip`, and any staged pascal50s/xm3600/nocaps set under `$NCS_DATA/datasets` | P50 measured 4.73 GPU-h for the same 7 models × 1,000 images; × 1.3 for larger scene images ≈ 6.2; **cap 10** |
| 2 | D2, 1,000 training images | M2 | ≈ 6.2, cap 10 |
| 3 | validation, 2,000 | M1 (role m3) | ≈ 12.4, cap 18 |

Seven models up to 8B in bf16 fit one RTX 3090 24 GB (P50 ran the same set on a 24 GB card).

## 9. Gates and disclosures

- **G-own / W8:** the ledger line "ADE20K SceneParsing val (2,000) + LN-ADE val | pixel labels + narratives | unused
  | A" was added to `manuscript/directions/PORTFOLIO_3Y_2026-10-29.md` §2.3 on 2026-10-30 (lands with the
  finalisation commit). Before tier 3 run the W25 near-duplicate filter of the validation
  images against every other owner's set (overlaps dropped from A's set under a pre-fixed rule, disclosed).
- **G2:** data pins and terms (§1).
- **Exposure (N6):** LN may be in some LVLMs' training data. Tier 1 makes no exposure claim; the tier-3 prereg adds
  an 8-gram hit count of each decode against the validation narratives (p50.ngram pattern), descriptive only.
- Scope: one matcher, 24 classes before the W2′ resolution, English only; ADE images are scenes, not COCO-style object photos; one narrative is
  a single reference, so the claim is "label vs one narrative", not "label vs every reference".

## 10. Files

- `scripts/a_t1/a_t1.py` (split, select, gold, stage, register, guard, left, score, selftest),
  `scripts/a_t1/a_t1_job.sh`, `scripts/a_t1/SHA256SUMS`.
- Reused unchanged: `scripts/pascal50s/p50.py`, `scripts/pascal50s/p50x.py`, `scripts/g2b/score_g2b.py`,
  `scripts/lb/decode_hf_vlm.py`, `scripts/b_r1/b_r1.py` (pHash/dHash).
- Selftest: `python3 scripts/a_t1/a_t1.py --selftest` (synthetic only: class-map rule, objectInfo150 format, pixel
  shares, near-val rule, set split, premise, AD-1/AD-2 on synthetic captions, predictors, outcome order, guard, cap).
- Finalisation: G2 pins; `split` on M1; `select` (lists committed); `gold` on D1 and the premise logged; rename to
  PREREG.md, pin its sha256 in `a_t1.py PREREG_SHA256` and LOG.md; regenerate SHA256SUMS; gatekeeper commit by path.

## 11. CC-170 W-items

CC-170b: W5″ multiplicity text (§5) · V1 V counts "before the W2′ resolution" + LOG step · V2 synonym promise replaced
by a pre-declared sensitivity excluding added classes · V3 docstring. Tier-2 prereg notes: `register --set`, W10
bootstrap predictor.

CC-170a: W2′ reverse-direction gate and resolution rule (§3, code + selftest) · W5′ Holm for single-PASS cells
(§7.1) · N1 missing-file and ";" tests · N2 `select` refuses annotations/validation · N3 D2 premise gate, `stage
--set` · N4 ≥ 18,000 candidates · N5 docstring · N6 strict sidecars, 8-gram moved to tier 3 · W8 ledger line added.

CC-170: W1 objectInfo150 parsing (comma synonyms, hard fail, pin, real-format test) · W2 class-map rule (30 indices, V = 24) ·
W3 custody (`split` on M1 only) · W4 premise before GPU (`stage` gate) · W5 multiplicity (intersection–union; p-values
defined; paper sentences §7.1) · W6 set-size asserts · W7 sections 6.4/6.6 · W8 ledger line (coordinator, §9) · W9
wider guard · W10 AD-2 predictor caveat · W11 job header · W12 outputs off the repo · W13 scope sentence.
