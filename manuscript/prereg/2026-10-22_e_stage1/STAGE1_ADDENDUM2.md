# Paper E, stage 1: addendum 2, controls and positioning (CC-087)

**Label: EXPLORATORY / DEV.** This addendum is not a registration.

| field | value |
|---|---|
| Authority | CC-087 (2026-10-22): E-a, E-b and E-c, E-d and E-e as disclosures, and the ownership rule. The judge names this note `E_ADDENDUM_1.md`; the coordinator named it `STAGE1_ADDENDUM2.md`. It is the same addendum. |
| Design | `DESIGN.md` sha256 `c793cbe6f9b57aca71a70e5cdcc954d914624e89b93661015a430802a9ae98bd`, unchanged. The split addendum (`SPLIT_ADDENDUM.md`, commit 37e629d) is unchanged. |
| Written | 2026-10-22, before any Paper E output exists. Nothing ran on M3, and no model, judge or embedding ran. |
| Pin | `e_lists.py` pins this note's sha256 (`e_lists.GPU_PINS`), so every mode checks it. `SHA256SUMS` lists the code. |

## 0. Bindings

1. This addendum is committed, after the judge's CC-087b check, **before E's first M3 step**. E's M3 work still waits for binding 5 of the design: C's stage-2 prereg committed, or C stopped.
2. **The approved rules stay as they are:** A1–A3, the pick of DESIGN §7.2, the best-global set `GLOBAL` (`siglip2`, `mclip`, `whole_raw`, `whole_sub`), the JUDGE floor and the 4.0 GPU-h cap.
   - Every row added here is a **named comparison**, reported with the §7.1 bootstrap CI. None of them gates, enters the pick, or can be chosen as a best-global baseline. `score.py`'s self-test checks this.
3. Like every stage-1 number, these rows are dev-A exploration. They go into the ledger (key `named`) and into the "all configurations tried" appendix.

## 1. E-a: subtracted against raw P(yes | image)

**What the subtraction is.**
- p_without = P(yes | no image, question about o) is asked **once per class**, not per image (`guard.fill`).
- So subtracting it shifts each class's score by a constant: a per-class offset, in the sense of contextual calibration (Zhao et al., "Calibrate Before Use", arXiv 2102.09690).
- **Within a class it does not change the order of images.** It changes a caption's score only through which classes the caption mentions, and the paper says so.

**Named comparisons** (`score.named`, for each question language q):

| name | a − b | reported |
|---|---|---|
| `sub_vs_raw:q` | `E:q:sub:0.0` − `E:q:raw:0.0` | bc accuracy and τ-b, each with CI |
| `emp_vs_raw:q` | `Eemp:q` − `E:q:raw:0.0` | bc accuracy and τ-b, each with CI |
| `prior_tercile:q:t` | bc accuracy of `E:q:sub:0.0` and of `E:q:raw:0.0` on the bc pairs whose added absent class falls in tercile t (0, 1, 2) of p_without, pooled over the judges | both accuracies with CI |

- **`Eemp:q`** is the empirical-prior variant. It subtracts the class's mean P(yes | image) over the E-dev-A items of that class, in place of P(yes | no image). It is computed per judge and pooled as in DESIGN §5.
- **Cost.** All of this runs on CPU, on the caches already planned.
- **Stage-2 binding.** E's stage-2 prereg names `sub_vs_raw` as a comparison and fixes the two framing branches before E-dev-B:
  - **subtracted beats raw:** E is presented as a calibrated object-level scorer;
  - **otherwise:** E is presented as an object-level decomposition, with a registered negative result on the subtraction.

## 2. E-b: object-level controls

**Controls** (`score.controls`; all CPU except the phrase embeddings):

| name | score of caption c |
|---|---|
| `objemb_siglip2_<l>_raw`, `objemb_mclip_<l>_raw` | mean over M(c) of cos(image, phrase(o)) |
| `objemb_siglip2_<l>_sub`, `objemb_mclip_<l>_sub` | the same, minus each class's mean cosine over the E-dev-A pair images (the embedding analogue of the prior) |
| `prior_only:q` | −mean over M(c) of P(yes \| no image) (the judges' content-free prior), pooled |
| `count_only` | −\|M(c)\| |

- **Phrase texts.** These are written for this addendum, with no authorship claim: en `a photo of {np}`, where {np} is S2's English noun phrase (for example "a photo of a dog"), and vi `một bức ảnh có {np}`, where {np} is the lexicon class word (`judge.OBJ_PHRASE`, self-tested).
- **Models.** The SigLIP2 and M-CLIP models are those of DESIGN §6, with the same snapshot, revision and TO VERIFY items.
- **Scope.** `judge.py embed` scores all 112 lexicon classes for every pair image in both phrase languages, reusing the image embeddings it already computes. It writes `obj_embed.json` (ids, class names and cosines; never committed).
- **Named comparisons:** `pick_vs_<control>`, which is the picked E minus each control, on bc accuracy and τ-b, each with CI.
- **Claim rule.** These controls are not added to the A1/A2 best-global set, because A1–A3 stay as CC-081 approved them.
  - The paper may claim that the VLM yes/no adds anything beyond object decomposition **only if E beats the object-level SigLIP2 and M-CLIP controls**, and beats `prior_only` and `count_only`.
  - E's stage-2 prereg names this test.
- **Optional, not done here.** Switching `whole_*` to VQAScore's published template happens only once the exact text has been checked against VQAScore's paper or repository; it would then be called "VQAScore-style".

## 3. Budget

- **Object-phrase embeddings.** There are 2 phrase languages × 112 classes = 224 texts per model, and 121 image embeddings that are already computed. Both models are already loaded in the `embed` step.
- **Cost.** Under 0.01 GPU-h, inside the existing embed row of DESIGN §8 (0.03 point, 0.05 high).
- **Totals.** The required total stays about 2.6 GPU-h (point) and 3.7 (high). The hard cap stays 4.0.

## 4. E-c: positioning

- **DEPICT is the closest work, and the paper lists it first among the differences.** DEPICT ("DEPICT: Scoring Text-to-Image Alignment by Answer Agreement", arXiv 2610.03617, October 2026), as its abstract describes it (read on the arXiv API by the coordinator): DEPICT is a training-free metric that replaces fixed reference answers on decomposed verification questions with the expected agreement between image-based and caption-only answers, weighting questions by how decisively the caption determines them, and merges this with a holistic score; it is evaluated mainly for text-to-image alignment (five benchmarks, eleven backbones).
  - E differs, stated only as differences: E subtracts the model's no-image P(yes) per object mention, a content-free prior, on lexicon-extracted objects, adds a count term, and is evaluated on Vietnamese and English captions. DEPICT instead contrasts image-based answers with answers implied by the caption text.
  - DEPICT is read in full before the paper describes its method.
- **Added to Related Work:**
  - Calibrate Before Use (Zhao et al., arXiv 2102.09690), for the content-free prior;
  - VQAScore (Lin et al., ECCV 2024; identifier to be checked before citing), for yes/no scoring of image–text alignment.
- DESIGN binding 7 still holds: no "first", no "novel", and no claim of the subtraction.

## 5. E-d: power (disclosure; no change to stage 1)

- **The split addendum's counts.** There are 77 Vietnamese bc pairs from 43 images. The image-level SE of a pairwise accuracy near 0.5 is about √(0.25 / 43) ≈ 0.076, so a 95% interval is about ±0.15.
- **The E-dev-B gate is decided in E's stage-2 prereg, before E-dev-B.** It chooses either of:
  - pooling all Vietnamese pairs that have a correct winner;
  - a consistency check in place of 2 × SESOI.
- Either choice is a named deviation from QQ34 §2.4 and needs PI approval.

## 6. E-e: human-judgment sets (later)

- These enter only in a later prereg, with their licences checked first.
- No image may overlap a refused set (the `exclusion.json` COCO sets, CHAIR-500, CV295).
- Only human labels count. NAME-Bench is used only if its labels are confirmed human, and FOIL is never used.
- There is no machine translation into Vietnamese.

## 7. Ownership between the papers (CC-087 salami rule)

- **E owns the per-object statistic as a metric** and validates it: pairs, τ, and later the human-judgment sets.
- **C reports only the guard's effect on captions** (H_G). It cites B for the S2 verifier, and E only as related work. C's claims never depend on E's results.
- **What each paper does not report:**
  - C reports no pair or τ tables, and does not use E as a named secondary metric;
  - E reports no CIDEr and no in-context-learning effect.
- **B's numbers stay B's.** Neither E nor C re-reports B's 0.634 or 0.485 as its own result.
- **Before submission.** The cover letters name the sister papers and the boundaries, and a cross 8-gram check across A, B, C and E runs.

## 8. Code changes

| file | change |
|---|---|
| `scripts/e_stage1/judge.py` | `OBJ_PHRASE` and `obj_texts`; `embed` also writes `obj_embed.json` (image × class cosines for SigLIP2 and M-CLIP, en and vi phrases) |
| `scripts/e_stage1/score.py` | `distinct`, `class_mean`, `controls` (`Eemp`, `prior_only`, `count_only`, `objemb_*`), `named` (the comparisons of §1–§2); the ledger row gains `named`; `obj_embed.json` is read when present and hashed into `inputs_sha256` |
| `scripts/e_stage1/e_lists.py` | `GPU_PINS` also pins this note |

The self-tests cover the new parts:
- the empirical prior, prior-only, count-only and both object-embedding variants, on known numbers;
- that a control that ranks every pair right still never becomes the pick or the best global baseline;
- that the named comparisons and terciles compute;
- the phrase texts.
