# A5: existing cross-lingual and instance-labelled data for precise, complete Vietnamese captions

Round-2 novelty research, direction A5. All numbers come from CPU pilots on existing data. The code, JSON outputs and
logs are in this directory (section 8). Bootstrap B = 2000 over images unless stated. Brackets are 95% percentile CIs.

## 0. Verdict

**Main finding.** None of the existing instance-labelled or cross-lingual resources can materially raise KTVIC
precision through training. The bound is quantitative:

- **COCO-80 coverage.** COCO-80 instance supervision reaches only 14.5% of fuse2-short's precision gap to a human
  (0.045 of 0.310 excess false mentions per caption).
- **Best-case gain.** If every such mention vanished, P would rise from 72.9 to 74.5 under the human-parity protocol,
  or from 75.7 to 78.4 against all 5 references.
- **Realistic gain.** Only about 55% of reference-false COCO-80 mentions are true hallucinations (measured on COCO),
  so the realistic ceiling is roughly half of that: about +0.9, or about +1.4 against 5 references.

**What does survive.** These resources are decisive as **human-only evidence about what reference precision
measures**. On UIT-ViIC, fused SFT targets lose 5.7 points of precision against held-out Vietnamese annotators but
**0.0** against exhaustive COCO instance labels. English COCO captions lose 14-17 points against Vietnamese
annotators, also at equal true precision. Reference precision ranks targets by *typicality*, not *truth*.

**Ideas surviving the pilots:**

| Idea | What it is | Status |
|---|---|---|
| 1 | Two-gold target audit (analysis and protocol). Needs no new GPU beyond queued jobs. | High confidence at target level |
| 2 | Instance-gated cross-lingual reference fusion | Conditional, only for COCO-domain coverage; low-moderate confidence |

**Killed (numbers in section 6):**
- instance-anchored target selection or fusion;
- COCO-instance three-state rewards aimed at KTVIC precision;
- translate-train of English COCO references to raise KTVIC precision;
- KTVIC + UIT-ViIC mixing aimed at KTVIC precision;
- XM3600-vi x Open Images verified labels and COCO-Stuff as gold for the non-COCO part of the gap.

**Hygiene facts the running jobs need:**
- **Overlap 1 (UIT-ViIC train in COCO test).** 133 UIT-ViIC *train* images are in the COCO Karpathy *test*
  5,000-image probe. A UIT-ViIC-trained model (jobs 59a/59b) scored on that probe must drop them.
- **Overlap 2 (UIT-ViIC val/test in COCO train).** All 924 UIT-ViIC val images and all 231 test images are in
  Karpathy *train*. Any translate-train or COCO-train mix therefore leaks into the UIT-ViIC evaluation.

## 1. Data facts established here

**KTVIC object space vs COCO-80.** Gold classes are the union of the 5 references, extracted with the 113-noun lexicon.
I mapped the lexicon to COCO-80 by hand (`pilot_ktvic_coverage.COCO`).

| Split | Person family | Other COCO-80 | Non-COCO |
|---|---|---|---|
| Test | 32.5% | 11.3% | 56.2% |
| Train | 32.7% | 15.3% | 52.0% |

- The non-COCO 56.2% (test) includes cây, nhà, đường, áo, nón, cửa, quầy hàng, quả, hoa and similar nouns.
- Any COCO-80 transfer therefore touches at most 44-48% of KTVIC gold. Inside that share, 33 points are `người` and
  its subtypes, which COCO cannot tell apart.
- The ball class `bóng` (UIT-ViIC's main non-person class) is 0.34% (train) / 0.58% (test) of KTVIC gold classes.

**UIT-ViIC.** 3,850 images carry COCO-2014 instance labels averaging 3.5 classes per image. Train has 2,687 images with
exactly 5 captions; one caption names 0.97 COCO-80 classes on average.

**Leakage.** 133 UIT-ViIC train images fall in Karpathy test (the COCO probe). All 924 val and 231 test images fall in
Karpathy train.

**XM3600 x Open Images V7.**
- 1,855 of 3,600 XM3600 images have human-verified image-level labels (456 val + 1,399 test). Each carries 9.9 positive
  and 5.5 negative labels; 1,817 images have at least one negative.
- Only 21 labelled images come from the Vietnam locale.
- There are 7,350 Vietnamese captions, about 2 per image.

## 2. Pilots

### P-A. Target policies scored against held-out annotators vs COCO instances (UIT-ViIC train)
`pilot_uitviic.py`, COCO-80 Vietnamese matcher (score_coco_probe.vi_classes).

**Do single-annotator mentions exist?** I asked how often a class named by k of 5 annotators is instance-present:

| k | (image, class) pairs | Instance-present |
|---|---|---|
| 1 (singletons) | 1,323 | 98.11% [97.31, 98.83] |
| 2 | 1,288 | 99.30% |
| 3 | 978 | 99.39% |
| 4 | 527 | 98.67% |
| 5 | 810 | 99.01% |

**Actual training targets (built from all 5 captions) vs instances:**

| Policy | P | R |
|---|---|---|
| p1 | 98.98 | 29.93 |
| cons | 99.17 | 44.87 |
| fuse2 | 98.92 | 55.07 |
| fuse3 / fuse5 | 98.88 | 56.30 |

**Common leave-2-annotators-out protocol (10 folds):**

| Comparison | Gold | ΔP | ΔR |
|---|---|---|---|
| fuse2 - p1 | 2 held-out Vietnamese captions | -5.74 [-6.41, -5.03] | +26.84 [25.87, 27.89] |
| fuse2 - p1 | Instances | **+0.01 [-0.16, +0.19]** | +18.36 [17.83, 18.93] |

**Do the two golds rank policies the same way?** Kendall τ_b over the 6 build_gold_sft policies:
- **F1:** 1.00 (p = 0.003). Order fuse2 > rnd2 > unf2 > cons > multiref > p1 under both golds.
- **R:** 1.00 (p = 0.003).
- **P:** 0.14 (p = 0.70). Every policy is about 99% precise against instances; reference precision only tracks how
  many captions were merged.

**Instance anchoring** (icons, ifuse2, ifuse3 drop captions that name an instance-absent class):
- It changes the target on 0.86% (cons) and 1.53% (fuse2) of images.
- Effect on targets:

| Comparison | Gold | ΔP | Other deltas |
|---|---|---|---|
| ifuse2 - fuse2 | Instances | +0.87 [0.62, 1.14] | ΔR 0.00 |
| ifuse2 - fuse2 | Held-out annotators | +0.16 [0.05, 0.27] | ΔR -0.35 [-0.53, -0.19], ΔF1 -0.07 (p = 0.25) |

- **Caveats.** Much of the instance-absent 1% is matcher noise (bàn / dining table, gậy bóng chày when the bat has no
  box). `cầu thủ` and `vận động viên` are not person terms in coco80_vi, so person recall is understated equally for
  every policy.

### P-B. Cross-lingual pools: English COCO vs Vietnamese UIT-ViIC references on the same images
`pilot_crossling.py`. English captions are scored by the classes they name, so translation is assumed to be perfect.
That makes this an upper bound for translate-train.

**Descriptive comparison:**

| Measure | Vietnamese | English |
|---|---|---|
| Classes per caption | 0.97 | 1.49 |
| Precision vs instances | 99.0 | 99.1 |
| Union-5 recall vs instances | 51.7 | 65.6 |

- The union of all 10 captions reaches 70.1.
- English-only classes: 0.69 per image, 93.9% instance-present.
- Caveat: the UIT-ViIC annotation tool let writers view the English COCO captions on request (Lam et al. 2020), and
  the Vietnamese pool still names 35% fewer classes.

**Common folds**, every policy scored against the 2 held-out Vietnamese captions and against instances:

| Comparison | Gold | ΔP | ΔR | ΔF1 |
|---|---|---|---|---|
| en_p1 - vi_p1 | Held-out Vietnamese | -14.12 [-15.29, -12.97] | +16.0 | +2.95 |
| en_p1 - vi_p1 | Instances | +0.08 [-0.33, 0.47] | +14.3 | |
| en_fuse2 - vi_fuse2 | Held-out Vietnamese | -16.91 [-17.76, -16.11] | +12.5 | -7.0 |
| en_fuse2 - vi_fuse2 | Instances | -0.82 [-1.21, -0.45] | +20.7 [19.9, 21.6] | |
| xl_fuse2i - vi_fuse2 | Held-out Vietnamese | -14.96 [-15.75, -14.22] | +15.1 | |
| xl_fuse2i - vi_fuse2 | Instances | +0.54 [0.40, 0.71] | +21.76 [21.08, 22.47] | |

- xl_fuse2i is the Vietnamese consensus plus the English caption adding the most instance-verified classes.
- The instance gate itself is xl_fuse2i - xl_fuse2: true ΔP +1.29 [1.02, 1.58].

### P-C. KTVIC: how much of the false-positive mass is reachable by COCO-80 labels
`pilot_ktvic_coverage.py`.

Every reference-false mention (exact match, as object_prf P) is typed as one of:
- vaguer (an ancestor of a gold class);
- person-naming;
- coco-same;
- person-new;
- coco-new;
- non-coco.

Only person-new and coco-new are COCO-addressable.

| System | Addressable share | P ceiling if all addressable mentions vanish (5 refs) |
|---|---|---|
| P1-short | 10.9% [7.0, 15.1] | 77.9 -> 79.9 |
| fuse2-short | 13.8% [10.0, 18.1] | 75.7 -> 78.4 [75.9, 80.9] |
| tags_fuse2-short | 13.7% | 77.9 -> 80.3 |
| fuse2-detailed | 17.2% [14.1, 20.5] | 68.0 -> 71.9 [69.7, 74.3] |

- Non-COCO mentions are 49-55% of reference-false mentions for every trained system.
- Person-naming disagreements are 20-24%.

### P-D. Where the 12-point precision gap to one human lives (KTVIC test, 1v4 parity protocol)
`pilot_gap_decomp.py`.

| | P |
|---|---|
| Human | 85.3 |
| fuse2-short | 72.9 |
| P1-short | 75.2 |

**fuse2-short excess false mentions per caption over the human, same gold: +0.310 in total.**

| Type | Excess per caption | Share of the excess |
|---|---|---|
| non-COCO | +0.152 [0.105, 0.196] | 49% |
| person-naming | +0.079 [0.051, 0.110] | 25% |
| coco-new | +0.045 [0.024, 0.067] | 15% |
| vaguer | +0.028 | 9% |
| person-new | 0.000 | — |

- The largest single classes are đường (`trên đường`, "on the street"), phụ nữ / đàn ông naming, cửa (mostly
  `cửa hàng`, "shop"), quầy hàng vs sạp hàng, áo (`mặc áo ...`, "wearing a ... shirt"), quả and thuyền.
- P1's total excess is +0.188, with the same split.

**Side check.** Counting fusion novelty with person nouns merged (COCO-style) changes the fuse2 targets by
ΔP +0.28 [0.13, 0.43], ΔR -1.74, ΔF1 -0.59 [-0.78, -0.42] on KTVIC train. So fusion's extra person nouns are mostly
confirmed by held-out annotators, and this is not a fix.

### P-E. On COCO images, are reference-false COCO-80 mentions hallucinations?
`pilot_coco_reffalse.py`. Existing Vietnamese captions on the 5,000-image probe, instance labels.

| System | Instance-absent share of reference-false mentions |
|---|---|
| Zero-shot short | 55.7% [51.6, 59.5] |
| Zero-shot detailed | 49.8% [48.0, 51.5] |
| VSPS short | 60.6% [56.0, 65.5] |
| VSPS detailed | 54.8% [52.0, 57.7] |

At the *model* level, about half of reference-false COCO-80 mentions are real hallucinations. At the *target* level the
share is about 1-2% (P-A). This is why the realistic gain of any COCO-80 reward is about half of the P-C ceiling:
roughly +1.4 P (fuse2-short) and +2.1 P (fuse2-detailed) against 5 references, with perfect transfer.

### P-F. XM3600-vi x Open Images V7 verified labels
`pilot_xm3600_oi.py`. The KTVIC lexicon is mapped by hand to Open Images display names.

**Human Vietnamese mentions:**

| Status | Share |
|---|---|
| Present | 51.0% |
| Verified absent | 4.4% |
| Unverifiable | 42.0% |
| Unmapped | 2.6% |

- **Noise floor:** absent among verified mentions is 7.89% [6.73, 9.14]. This comes from matcher ambiguity
  (`cây`/`quả`/`nhà` as classifiers or compound heads) and from label errors.
- For mentions one annotator makes and the other does not, the figure is 11.5% [9.4, 13.5].
- **Testability** (share of labelled images where the class is verified at all):

| Class | Testable |
|---|---|
| cây | 48.1% |
| người | 34.5% |
| xe | 21.8% |
| áo | 20.5% |
| nhà | 18.1% |
| hoa | 12.0% |
| đường | 5.1% |
| cửa | 2.2% |
| quầy hàng | 0.4% |

- **Verdict:** usable as an out-of-distribution check for person, vehicle, tree and building classes. It cannot test the
  classes that carry KTVIC's excess (đường, cửa, quầy hàng).

### P-G. COCO-Stuff things + 91 stuff classes as gold for non-COCO nouns
`pilot_cocostuff.py`, with `--norm` for compound handling.

- **Human floor** (UIT-ViIC captions, compound-normalised):

| Family | Verified absent |
|---|---|
| Person | 0.1% |
| COCO-80 | 11.1% |
| Stuff-type nouns | 48.9% |

  The stuff figure comes from `nhà` in `sân nhà` and other compound or sense errors.
- **Models** (COCO probe, normalised): stuff-type verified-absent 21.8% (zero-shot short) to 37.4% (zero-shot detailed).
  This cannot be told apart from the human floor.
- Worn clothing is painted as `person` in COCO-Stuff, so `áo` is unverifiable.
- **Verdict:** inconclusive; do not use.

### P-H. Compound artefacts of `objects_in` on KTVIC
`vi_norm.py`, `pilot_norm_effect.json`.

- These compounds are split into lexicon nouns:
  - cửa hàng / cửa sổ (shop / window) read as door;
  - cầu thủ / cầu thang (player / stairs) read as bridge;
  - quả bóng (ball) read as fruit;
  - bàn phím / bàn chải (keyboard / brush) read as table;
  - hoa văn (pattern) read as flower;
  - cây vợt (racket) read as tree;
  - đường kẻ / đường ray (line / rail) read as road.
- Normalising them on both sides moves P by at most +1.1 and changes no ranking:

| System | P before | P after |
|---|---|---|
| P1-short | 77.9 | 78.5 |
| fuse2-short | 75.7 | 76.0 |
| fuse2-detailed | 68.0 | 67.9 |
| zero-shot short | 52.3 | 53.4 |

  This agrees with the round-1 critique.

## 3. Literature

Full texts were read by me or by two literature sub-agents that returned extracts; arXiv ids are given. The shared
web-search budget ran out twice. I completed 11 targeted scoop searches, the second agent 1, and the first agent 0.
The first agent instead fetched its candidates directly by id.

### Captioning with instance-labelled data and object-level rewards
- **CHAIR (Rohrbach et al., EMNLP 2018, 1809.02156).** Builds gold from COCO segmentations plus references and notes
  that the annotation source matters. Nobody uses this to audit *training targets*.
- **Feng et al. (2406.12663, 2024).** Manual check of CHAIR on 500 COCO images with LLaVA-1.5: over 55% of flagged
  hallucinations are unjustified, caused by extraction errors and lossy references (subassemblies, small items,
  background). This is model outputs only, in English, with no per-cause split. It is the closest prior to Idea 1.
- **Misra et al. (CVPR 2016, 1512.06974).** Models visual presence separately from human relevance, i.e. reporting bias.
- **COCO-Stuff (Caesar et al., CVPR 2018, 1612.03716).** Stuff is 69.1% of pixels but 38.2% of caption nouns.
- **Kamath et al. (2602.23351, TACL 2026).** Reporting bias leaves spatial, temporal, negation and counting skills
  under-supervised; scaling data, models or languages does not fix it.
- **Biten et al. (WACV 2022, 2110.01705).** Ground-truth labels are model *input* plus caption augmentation that swaps
  objects. CHAIRi 6.9 -> 3.8, CHAIRs 10.1 -> 5.9.
- **Rewards (literature sub-agent extracts).** None uses exhaustive human instance labels as an RL reward or for
  preference-pair selection.

  | Paper | Evidence source |
  |---|---|
  | CLIP-reward (2205.13115) | CLIP |
  | MOCHa (2312.03631) | NLI against references |
  | CCCaption (2602.21655, CVPR 2026) | MLLM-judge completeness / correctness |
  | BalCapRL (2605.07394) | GPT judge |
  | SC-Captioner (2508.06125, ICCV 2025) | Reference sets; concedes it penalises present-but-unmentioned |
  | CapRL (2509.22647) | QA |
  | ViGoR (2402.06118) | Grounding DINO plus a reward model |
  | FGAIF (2404.05046) | LLaVA labels |

  - **CHAIR-DPO (2508.20181).** Uses a DETR detector over COCO-80 to pick winner/loser pairs: AMBER CHAIR 7.6 -> 3.0,
    Cover -5.1.
  - **HallE-Control (2310.01779).** Uses COCO ground-truth objects plus the RAM tagger to *construct* data:
    CHAIRi 25.3 -> 14.0, coverage +4.0.
  - Three-state ("federated") rewards and transfer to a label-free or other-language set were not found.
- **Detector-verified captions.**
  - FuseCap (2305.17718): detector + LLM enrichment, no verification. Hirota et al. (2406.13912) fine-tuned BLIP on
    FuseCap COCO captions: recall 45.7 -> 56.9 but CHAIRi 3.1 -> 6.3, the same recall-up, precision-down pattern as
    fuse2.
  - HalluciDoctor (2311.13614), Woodpecker (2310.16045), VFC (2404.19752) and DenseFusion (2407.08303) all filter or
    enrich *model* captions. None audits human references.

### Multilingual and translate-train
- **XM3600 (2205.12522, EMNLP 2022).**
  - Annotators first rated English model captions, then wrote native captions.
  - Vietnamese: 7,350 captions, 18.0 words on average.
  - CIDEr-human correlation: Pearson 0.88 with XM3600 references vs 0.68 with machine-translated COCO references. On
    the 28 extra languages, the MT-COCO references correlate -0.44.
  - Vietnamese CIDEr of translate-train models: 0.18-0.34 on XM3600 vs 0.94-1.15 on MT-COCO-dev.
- **Translated instruction data is the norm, and nobody measures object precision:**
  - mBLIP (2307.06930): NLLB into 95 languages. Matching tasks lift POPE 63.7 -> 76.1 while CHAIR barely moves.
  - Pangea (2410.16153): 40:60 English:multilingual is the optimum; Vietnamese is 315.5K items.
  - Aya Vision (2505.08751): NLLB plus LLM post-editing; Vietnamese COMET 0.758 -> 0.837; 35% multilingual is best.
  - PALO (2402.14818) and Maya (2412.07112): no Vietnamese.
  - Vietnamese models (Vintern 2408.12480; LaVy 2404.07922; Vista; dinhanhx/coco-2017-vi): translated or
    Gemini-generated data, no captioning evaluation. coco-2017-vi's "plus" file merges all UIT-ViIC splits into train,
    a leakage trap.
- **Native vs translated.**
  - COCO-CN (1805.08661, TMM 2019): native beats MT and is combined by sequential training.
  - STAIR (1705.00823).
  - Buettner & Kovashka (2410.02027, EMNLP 2024): English captions name about 50% more object nouns than German ones;
    German retrieval mean recall 33.4 (MT) vs 38.4 (native).
  - Ye et al. (2310.14356, CVPR 2025): multilingual caption sets have +46% objects. GIT fine-tuned per language is best
    in-language, and the equal mix is second-best. No precision metric.
  - Multi-PixMo (2604.18347).
- **Multilingual hallucination.** CLAIM (ACL 2025) finds non-English queries hallucinate more and fixes it at inference
  time; MHR (2408.00550). No Vietnamese POPE or CHAIR was found.
- **Vietnamese datasets.**
  - KTVIC (2401.08100): 3 annotators plus 2 revisers; images are EVJVQA's.
  - UIT-ViIC (2002.00175): 5 writers; the annotation tool showed COCO category icons and, on request, the English
    captions.
  - UIT-OpenViIC (2305.04166).

### Scoop searches I ran

| # | Query topic | Result |
|---|---|---|
| 1 | COCO-Stuff hallucination / stuff mentions | Only COCO-Stuff's own caption analysis |
| 2 | Three-state reward, present-but-unmentioned neutral | ClaimDiff-RL, CCCaption, MOCHa, ViCrit; none of them three-state |
| 3 | Cross-lingual captions equally accurate against instances | Ye 2025, Misra 2016, XM3600; no instance-based comparison |
| 4 | CHAIR overestimation / incomplete references | Feng 2406.12663; Rohrbach 2018 |
| 5 | MT plus native caption combination | 2504.14359, COCO-CN, STAIR, German SLSP 2021 |
| 6 | Training targets vs held-out annotators / instances | None |
| 7 | CHAIR or GT-label reward with GRPO | MOCHa, SAVOR (2609.16601); none with GT labels |
| 8 | Vietnamese captioning hallucination | None |
| 9 | Single-annotator objects vs presence | CHAIR, HAT, ALOHa; none |
| 10 | Open Images verified negatives for captions | NoCaps CHAIR (2210.07688), not using negatives |
| 11 | Cross-lingual hallucination transfer | CLAIM (ACL 2025) |

**Unscooped as far as these searches reach:**
- auditing SFT *target policies* and *annotator pools or languages* against exhaustive human instance gold;
- instance-gated cross-lingual reference fusion.

## 4. Idea 1 (survives): two-gold target audit, "reference precision measures typicality, not truth"

**Mechanism.**
1. For any multi-reference captioning set whose images carry exhaustive human instance labels (UIT-ViIC, COCO), score
   every SFT-target policy and every trained model twice: against held-out annotators (the leave-k-out protocol of
   human_parity.py) and against instance labels.
2. Split each reference-false mention into instance-present (atypical but true) or instance-absent (hallucinated).
3. Use the agreement between the two golds in three ways:
   - to validate the KTVIC offline target-ranking protocol: F1 and R rankings agree, τ = 1.0;
   - to show that reference *precision* is not a truth signal for targets: τ_P = 0.14;
   - to state falsifiable predictions for the trained models.

**Closest prior and delta.**
- **Feng et al. 2406.12663.** Manual audit of CHAIR on English model captions.
- **Rohrbach et al. 2018.** CHAIR gold built from references plus segmentations.
- **Misra et al. 2016 and Buettner & Kovashka 2024.** Reporting bias, and English mentioning more objects.
- **Delta.** Ours is the first audit of *training-target policies*, and of *annotator pools across languages*, against
  exhaustive human instance labels. It uses no AI labels and no new annotation. It turns the paper's AI-silver claim
  ("fusion's precision loss is mostly reporting gap") into a human-label result at target level:
  ΔP_ref -5.74 vs ΔP_inst +0.01 [-0.16, +0.19], with singletons 98.1% present.
- It also validates the paper's leakage-free offline protocol on a second dataset with an external gold. The ordering
  fuse2 > rnd2 > unf2 > cons > multiref ≈ p1 is the same as on KTVIC train.

**Pre-registered predictions for queued jobs 59a/59b** (UIT-ViIC test + val, 1,155 images, COCO-80, paired bootstrap
vs P1):
- **fuse2-short vs P1-short:** ΔP_inst in [-1.5, +1.5], ΔR_inst >= +3.
- **fuse2-detailed vs P1-short:** ΔR_inst >= +10 and ΔP_inst >= -2, while ΔP against the 5 Vietnamese references
  <= -3.
- **COCO probe:** the same comparison after removing the 133 overlap images, gold = instances only.

**GPU cost.** 0 new hours if 59a/59b already caption val; otherwise about 0.5 GPU-h for val inference.

**Code** (about 30 lines, port from pilot_uitviic.py):
- `scripts/object_prf.py instance_block`: add an "instances only" table and the instance-present/absent split of
  reference-false mentions. Today it scores only instances ∪ references; coco_block already does both.
- `scripts/human_parity.py offline`: add `--instance-gold`, with `NCS_DATASET=uitviic` and the coco80 extractor.

**Kill criterion.** On UIT-ViIC test + val, if the 95% CI upper bound of ΔP_inst(fuse2-detailed - P1) is below -2, the
target-level identity does not carry to the model. The paper must then call the precision loss real hallucination.

**Confidence.** High that the target-level result holds (measured). Moderate (about 0.6) that the model-level
prediction holds. P-E shows models do hallucinate COCO-80 classes; the question is only whether fusion adds to that.

## 5. Idea 2 (conditional): instance-gated cross-lingual reference fusion (xl-fuse) for COCO-domain coverage

**Mechanism.**
1. On COCO-image training sets (UIT-ViIC train), build the detailed target from the Vietnamese consensus caption plus
   the machine-translated English COCO caption that adds the most *instance-verified* COCO classes.
2. A caption naming any instance-absent class is never imported.
3. Partial references from two annotator pools, which differ in typicality but not truth (P-B), are fused into one
   Vietnamese target that is faithful by construction.

**Closest prior and delta.**
- **COCO-CN (TMM 2019).** MT data plus native data, combined by sequential training.
- **Ye et al. (CVPR 2025).** Multilingual caption mixes as separate rows; no truth gold.
- **Buettner et al. (2025).** Native-guided recaptioning.
- **Round-1 VN2.** Cross-team Vietnamese pooling.
- **Delta.** One fused target from native plus translated partial references, with imports gated by exhaustive human
  labels, evaluated with two golds. Novelty is incremental. The gate itself adds only +1.29 true P.

**Pilot (target level, common folds), xl_fuse2i vs vi_fuse2:**
- true R +21.76 [21.08, 22.47] at true ΔP +0.54 [0.40, 0.71];
- against held-out Vietnamese annotators: ΔP -14.96 [-15.75, -14.22], ΔR +15.1.

**Expected model-level effect (honest proxy).**
- On KTVIC, target-level R gains carried to the trained model at a ratio of about 0.94: offline fuse2 - p1 R +21.0 vs
  trained fuse2-detailed - P1-short R +19.8. That comparison is confounded by prompt mode.
- Using a ratio of 0.4-0.9: on UIT-ViIC test + val in detailed mode, vs job 59b fuse2, true R +9 to +20, true P within
  ±2, and reference P -6 to -14.

**Job spec (one RTX 3090, about 5 GPU-h):**
1. **Targets (CPU).** `build_gold_sft.py --annotations $NCS_DATA/datasets/uitviic/train_data.json --objects coco80
   --select consensus --fuse 2 --xl-en $NCS_DATA/datasets/karpathy/dataset_coco.json --instance-gold
   data/uitviic/instance_gold.json`.
   - `--xl-en` and `--instance-gold` are new options of about 40 lines.
   - Short row = Vietnamese consensus.
   - Detailed row = consensus + translated e*, where e* = argmax over the image's English captions of
     |en_classes(e) ∩ inst - classes(consensus)|, subject to en_classes(e) ⊆ inst.
   - Fallback when no English caption adds a verified class: the fuse2 target.
2. **Translate (0.3 GPU-h).** About 2.3k selected English captions with Qwen2.5-VL-7B-Instruct text-only, greedy, max 64
   new tokens. Prompt: "Dịch câu sau sang tiếng Việt tự nhiên, ngắn gọn như chú thích ảnh, giữ đúng các sự vật: {en}".
   Post-check: vi_classes(translation) ⊇ imported classes, otherwise drop the import.
3. **Train (about 2.6 GPU-h).** `NCS_DATASET=uitviic python scripts/train_stage2.py --stage sft --data
   ~/ncs-data/gold_xlfuse_uitviic --epochs 2 --seed 42`, with the hyperparameters of job 59b.
4. **Evaluate (about 0.8 GPU-h).** `NCS_DATASET=uitviic python scripts/evaluate.py --model qwen2.5-vl-7b --adapter <run>
   --prompt short|detailed` on test (231) and val (924).
5. **Cross-dataset (about 1.2 GPU-h).** `scripts/coco_probe.py --name xlfuse` on the 2,500-image manifest minus the 133
   UIT-ViIC-train images, short and detailed.
6. **Score (CPU).** `object_prf.py` two-gold tables (instances only; instances + references), paired against 59b
   (fuse2) and 59a (P1). Also report CIDEr and language fidelity (share of captions with untranslated English words).

**Kill criterion.** In detailed mode with instances-only gold, vs 59b: ΔR_inst < +3, or the CI upper bound of
ΔP_inst < -2, or more than 1% of captions keep English words.

**Confidence.** About 0.35 that it is worth a paper slot.

**When to run it.** Only after Idea 1 is in the paper and its 59a/59b prediction has held. Without two-gold reporting,
its -15 reference-precision cost reads as a regression.

## 6. Killed or bounded directions

**(a) Instance-anchored target selection or fusion (UIT-ViIC).**
- Changes 0.9-1.5% of targets.
- Target ΔP_inst +0.87, ΔP_ref +0.16, ΔF1_ref -0.07 (n.s.).
- Human captions are already 99% instance-precise, so there is nothing to select away.

**(b) COCO-instance rewards, negatives or three-state RL aimed at KTVIC precision.**
- Novel per the literature: no reward uses exhaustive ground-truth labels.
- Bounded: only 14.5% of the excess false mentions are COCO-addressable. The ceiling is +1.6 P at the human-parity level
  and about +0.9 realistic. Against 5 references: +2.7 short / +3.9 detailed, or about +1.4 / +2.1 realistic. This is
  within seed noise of the short-mode effects already reported.
- It still makes sense for COCO-domain true precision, but that is not this paper's bottleneck.

**(c) Translate-train of English COCO references for KTVIC precision.**
- At target level with perfect translation: ΔP against Vietnamese annotators -14 to -17. English pools are equally
  truthful but name 1.5x more classes.
- Translate-train therefore *lowers* reference precision. It also needs leakage control for the UIT-ViIC val/test images
  that sit in COCO train.

**(d) Multi-dataset Vietnamese mix (KTVIC + UIT-ViIC) for KTVIC precision.**
- No honest proxy predicts a gain. UIT-ViIC's main non-person class (`bóng`) is 0.3-0.6% of KTVIC gold classes.
- The UIT-ViIC policy ranking simply replicates KTVIC's.
- Not proposed.

**(e) XM3600 x Open Images and COCO-Stuff as gold for the non-COCO 49%.**
- Human noise floors are 7.9% and 48.9% respectively.
- Testability of đường, cửa and quầy hàng is 0.4-5%.
- Insufficient for the claim. XM3600 is usable only as an extra out-of-distribution check for person and vehicle classes.

**(f) Person-merged fusion novelty.** ΔF1 -0.59 [-0.78, -0.42]; dropped.

## 7. Most important literature finding

No published work uses exhaustive human instance labels either to audit how SFT targets built from human references
behave, or as a training reward. The nearest prior evidence:
- **Metrics side:** Feng et al. 2406.12663 found that more than 55% of CHAIR-flagged hallucinations in LLaVA captions are
  unjustified.
- **Training side:** CHAIR-DPO 2508.20181 selects preference pairs with a detector.

The open slot is therefore evaluative, which Idea 1 fills. The KTVIC bound in P-C/P-D shows why the reward slot would
not pay off for this paper.

## 8. Files (this directory)

**Pilot scripts and outputs:**

| Script | Outputs |
|---|---|
| `pilot_uitviic.py` | `.json`, `.log` (P-A) |
| `pilot_crossling.py` | `.json`, `.log` (P-B) |
| `pilot_ktvic_coverage.py` | `.json` (P-C) |
| `pilot_gap_decomp.py` | `.json` (P-D and the side check) |
| `pilot_coco_reffalse.py` | `.json` (P-E) |
| `pilot_xm3600_oi.py` | `.json` (P-F) |
| `pilot_cocostuff.py` | `.json`, `_norm.json` (P-G) |
| `vi_norm.py` | `pilot_norm_effect.json` (P-H) |

**Downloaded data (parsed only):**
- `dl/xm3600` (captions.jsonl, image_attributions.csv);
- `dl/oi` (oidv7 class descriptions and val/test human image labels);
- `dl/cocostuff` (stuffthingmaps_trainval2017.zip, 659 MB; labels.md).

**Paper text:** `papers/cocostuff_1612.03716.txt`.

**How to run:**
- Repo pilots: `cd /mnt/d/vsps_image_captioning && NCS_DATA=data nice -n 15 python <script>`.
- The XM3600 and COCO-Stuff pilots: `cd /tmp && NCS_DATA=/mnt/d/vsps_image_captioning/data python3 -P <script> --dl
  <A5>/dl`.

The scripts ran against repo commit ee7cad1 (coco80_vi without bare `kéo`). P-A and P-B were re-run after that commit.
