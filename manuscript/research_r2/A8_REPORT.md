I ran all the pilots on existing outputs (CPU only), but `REPORT.md` was not written: the harness blocks report files from subagents. The summary comes first, then the full report for you to save. Scripts and raw outputs are in `/tmp/claude-1000/-mnt-d-vsps-image-captioning/755eae04-5e4c-4ce1-ab21-d4bc106761ee/scratchpad/research_r2/A8/`.

## A8 summary (≤350 words)

**Pilot verdict.** Gold-free agreement between *different* sources (prompts, adapters, models, a detector, a Dawid-Skene label model) only trades recall for precision; F1 stays flat or falls.
- **COCO-5000, judged by human instance labels:** keeping only the teacher's confirmed mentions gives dP +6.5 [6.1, 7.0], dR −3.8, dF1 +0.3 [−0.0, 0.6].
- **KTVIC test:** confirmation by other adapters gives dF1 −6.1 [−7.9, −4.4].
- **Against human labels:** every machine consensus stays about 5 F1 and 12 P below a target fused from two human captions.
- **The one exception:** voting over temperature samples of one adapter raised both P and R.

**Idea 1: vote-then-fuse self-distillation on a hidden-label pool (UIT-OpenViIC, de-duplicated)**
- **Mechanism:** take 6 fuse2 samples per unseen image and keep only sentences whose objects all appear in ≥3 of 6 samples. A greedy cover of at most 2 such sentences is the pseudo-reference. Continue fuse2 on these rows plus replayed KTVIC rows.
- **Closest prior + delta:** MBR finetuning (2309.10966) selects whole outputs, for translation. ASC, IC3 and Self-Validation merge samples with an LLM at inference only. The delta is an object-level vote over the model's own samples, fused without an LLM, used as training targets.
- **Pilot:**
  - On 1,500 train images, scored against annotators never used in training: one sample → vote-then-fuse gives dP +7.0 [5.9, 8.1], dR +5.2 [3.9, 6.5], dF1 +6.4 [5.4, 7.4].
  - Against the round-1 MBR pick: dF1 +3.3 [2.5, 4.2].
  - Risk: greedy seed committees on unseen images gain only +0.3 [−0.5, 1.2]. E5, which was also trained on its own samples, was null.
- **GPU:** 2.2 h labelling (this step is the gate) + 2.4 h for three arms (vote-fuse, greedy control, human skyline) + 3.9 h evaluation ≈ 8.5.
- **Kill:** on the hidden human captions, vote-fuse beats greedy by less than 1.5 F1, or its precision drops. After training: vote-fuse ≤ greedy arm, or gain over fuse2 within seed spread.
- **Confidence:** high that the gate gives a clean answer; about 20% that it beats fuse2.

**Idea 2: cross-fitted vote-fuse vs gold-selected RFT on the same samples (add-on to the queued cross-fit job)**
- **Mechanism:** compare vote-fuse rows, RFT's gold pick and greedy on half B, using the half-A adapter's samples. Train only if both pass.
- **Prior + delta:** tri-training and cross-fitting exist, but not for captioning; this isolates what gold adds to sample selection.
- **GPU:** 0.5 for the gate, about 10 with a student.
- **Kill:** vote-fuse more than 3 F1 below the RFT pick, or cross-fitted RFT itself null.
- **Confidence:** 10–15%; high value as an ablation.

**Key literature finding:** UIT-OpenViIC already contains 401 of the 558 KTVIC test images (arXiv 2602.22678). Any pool must be de-duplicated; those images also come with a second, independent set of existing human captions.

---

# Full report

## 0. Bottom line

1. **Agreement across different sources cannot produce labels better than the teacher.**
   - On COCO-5000 (human instance gold) and KTVIC test, k-of-n agreement only moves along a fixed P/R frontier.
   - The best F1 gain is +1.4, from fusing several systems' captions.
   - Human-level precision (about 91% on COCO) comes only with about one human's recall.
   - A gold-free Dawid-Skene label model is worse than counting votes.
   - Conclusion: committee or co-training filters are not worth GPU time.
2. **Voting over one adapter's own samples does improve the label.** Vote-then-fuse gains about 6 F1 over one sample, even against annotators never trained on.
   - Memorisation is weak: 3.1% of sampled sentences copy the image's own references (0.00% for another image's references), and samples score far below their training target.
   - The open question is the gain over **greedy** decoding on **unseen** images. Greedy seed committees there show about zero voting gain, and E5 (gold-picked samples on seen images) was null in both modes.
3. **Recommendation:** run the gate first (D1, 2.2 GPU-h). D2 is a cheap add-on to the queued cross-fitted RFT.

## 1. Data and protocol

**COCO-5000 (Karpathy test).** Five existing Vietnamese caption sources:
- zero-shot, short prompt
- zero-shot, detailed prompt
- zero-shot, detailed prompt with VCD decoding
- old VSPS adapter, short prompt
- old VSPS adapter, detailed prompt

Scoring:
- Objects are the 80 COCO classes, matched with `vi_classes` and `coco80_vi`.
- Main gold is instance labels only.
- Calibration: English human captions matched with Rohrbach's synonym list.
- P, R and F1 follow `object_prf.py`.
- 95% CIs come from a bootstrap over images (B = 2000) with a shared index matrix, so paired deltas use the same draws.

**KTVIC test (558 images, never trained on).** Objects come from the KTVIC lexicon. The 1v4 protocol of `human_parity.py` scores against 4 of the 5 captions, averaged over folds. It reproduces one human at P 85.3 / R 46.9 exactly.

**Within-model samples.** `/root/ncs-data/e5_round1/samples.jsonl`: fuse2 s42, detailed prompt, T 0.8, 6 samples on 1,500 train images (seen). No multi-sample file exists for unseen images.

## 2. Pilots

### 2.1 COCO-5000, gold = human instance labels (`pilot_coco.py`, `pilot_ds.py`, `calib_coco_fused_humans.py`)

| Source | P [CI] | R [CI] | F1 |
|---|---|---|---|
| Zero-shot detailed (teacher-like) | 78.6 [77.9, 79.3] | 67.5 [66.6, 68.3] | 72.6 |
| One English human caption | 92.5 [91.8, 93.1] | 56.5 [55.6, 57.5] | 70.2 |
| Two human captions fused (fuse2 rule) | 86.0 [85.4, 86.7] | 73.2 [72.3, 74.0] | 79.1 |
| Named by ≥2 of 5 sources | 83.9 [83.3, 84.7] | 66.5 [65.7, 67.4] | 74.2 |
| Named by ≥3 of 5 sources | 90.9 [90.2, 91.6] | 53.8 [52.9, 54.7] | 67.6 |
| Teacher, kept if ≥1 other source agrees | 85.1 | 63.7 | 72.9 |
| Object-consensus MBR pick of the 5 captions | 80.7 | 68.2 | 73.9 |
| Greedy fusion of 2 of the 5 captions | 73.6 | 74.5 | 74.0 |

**Paired deltas against the teacher:**
- Kept if confirmed: dP +6.5 [6.1, 7.0], dR −3.8 [−4.1, −3.4], dF1 +0.3 [−0.0, 0.6].
  - The 1,637 of 11,084 unconfirmed mentions are 40.9% correct [38.4, 43.3].
  - Requiring 2 confirmers: F1 −5.6.
  - Confirmers from the same model only: F1 −0.6.
  - Only the other model as confirmer: F1 −10.3.
- MBR pick: dF1 +1.3 [1.0, 1.6].
- Fusion of 2: dF1 +1.4 [1.0, 1.8].

**Dawid-Skene label model.**
- It misestimates source reliabilities: it puts P(mention | present) at 0.98, against true values of 0.39–0.87.
- It ranks items worse than the raw vote count (AUROC 0.779 vs 0.798).

**Errors voting cannot remove (`audit_classes.py`).**
- 25.7% of the teacher's false positives (610 of 2,376) survive ≥3-of-5 agreement.
- They are led by dining table (198) and chair (103), which are systematic errors.

### 2.2 KTVIC test, 1v4 protocol (`pilot_ktvic.py`, `pilot_seeds.py`)

| Source | P [CI] | R [CI] | F1 |
|---|---|---|---|
| One human caption | 85.3 [84.1, 86.6] | 46.9 [45.2, 48.7] | 60.5 |
| fuse2 detailed (teacher) | 64.7 [62.5, 67.0] | 62.3 [60.0, 64.6] | 63.5 |
| Short: all 3 adapters agree (P1 s42, P1 s43, fuse2) | 84.6 | 34.8 | 49.3 |
| Teacher, kept if a P1 adapter agrees | 77.2 | 45.7 | 57.4 |
| Teacher, kept if Grounding-DINO (COCO-80) agrees | 70.9 | 17.8 | 28.5 |
| Fusion of 2 of the 6 adapter captions | 62.4 | 66.6 | 64.4 |

- **Adapter confirmation vs teacher:** dP +12.5 [10.4, 14.6], dR −16.6, dF1 −6.1 [−7.9, −4.4].
- **Committee fusion vs teacher:** dF1 +0.9 [0.1, 1.8].
- **Greedy seed committee** (three seeds of the old VSPS recipe, ≥2 of 3, unseen images): dF1 +0.3 [−0.5, 1.2].

### 2.3 Temperature samples of one adapter, 1,500 seen train images (`pilot_samples.py`, `vote_fuse.py`, `pilot_vtf_1v4.py`, `pilot_heldout.py`)

| Construct (gold = all 5 refs) | P [CI] | R [CI] | F1 [CI] | Words |
|---|---|---|---|---|
| One sample | 63.9 [62.5, 65.3] | 62.1 [60.7, 63.6] | 63.0 | 22.8 |
| Objects in ≥3 of 6 samples (set only) | 71.3 | 68.5 | 69.9 | – |
| MBR pick | 60.9 | 72.6 | 66.2 | 24.6 |
| **Vote-then-fuse, k=3, ≤2 sentences** | **72.2 [70.9, 73.6]** | **67.1 [65.5, 68.5]** | **69.6 [68.3, 70.7]** | 17.6 |

- **Vote-then-fuse vs MBR pick:** dF1 +3.3 [2.5, 4.2].
- **Under 1v4:** vote-then-fuse 69.1 / 68.6 / 68.8, against one human 85.1 / 49.3 / 62.4. It wins on F1 through recall; precision stays 16 points below a human.
- **Against only the 3.32 captions per image never used in a training target:**
  - one sample: 52.0 / 68.4 / 59.1
  - vote-then-fuse: 59.0 / 73.6 / 65.5, i.e. dP +7.0 [5.9, 8.1], dR +5.2 [3.9, 6.5], dF1 +6.4 [5.4, 7.4]
- **Memorisation checks:**
  - The training target scores 77.5 F1 on the same held-out annotators (this number is optimistic), so samples are not copies of it.
  - Sentence copying is 3.1% (vote-then-fuse output: 4.6%).
  - Sample diversity: mean pairwise Jaccard 0.509; all 6 samples share one object set on only 1.9% of images.
- **E5 vs fuse2** (gold-selected samples on seen images): short dF1 −0.8 [−2.4, 0.7]; detailed +0.2 [−1.2, 1.6]. Null in both modes.

**Why the two regimes differ.**
- Temperature samples make independent errors, so a vote removes them.
- Different systems differ systematically in how many objects they name, so their intersection inherits the tersest source's recall.
- Greedy seed replicas are near-identical, so there is nothing to vote away.

## 3. Literature (full texts; arXiv IDs)

**Self-training: selection beats imitation, and gains are small.**
- **MBR finetuning (2309.10966):** self-training on beam output hurts (COMET 57.79 → 57.08). Self-MBR over 256 samples on 200k unlabelled sentences helps (+2.15) and partly matches MBR decoding.
- **BLIP CapFilt (2201.12086):** +1.9 CIDEr. Nucleus sampling beats beam. A filter sharing the captioner's parameters flags only 8% instead of 25% (confirmation bias).
- **UCM (2201.02010):** +1.6 CIDEr from 280k images; a second round adds nothing.
- **Self-Distillation few-shot captioning (WACV 2021):** a committee of 3 captioners on re-randomised splits gives +2.5 CIDEr at 1% labels. Not cross-fitted.
- **Noisy Student (1911.04252):** a warm-started student stalls (86.4 vs 86.9 from scratch). ReST-EM also restarts from the base model.
- **Self-labelling for captions (2305.02297):** helps on in-distribution images, −0.5 on out-of-distribution images; likelihood filtering hurts.

**Consistency signals.**
- **CapMAS (2412.15484):** "object appears in m of 40 samples" detects hallucinations at AUROC 73.5, vs 81.4 for a yes/no probe and 61.5 for a detector.
- **HEDGE (2511.12693):** sample-consistency detection saturates at about 10–15 samples.
- **FactTune-MC (2311.08401):** consistency-based DPO gains precision but loses coverage (Llama-2 correct facts 19.03 → 11.31).
- **Self-Validation (2601.22451):** N=3 samples plus LLM rewrite cuts CHAIR_I 9.9 → 3.1 but F1 falls 74.4 → 70.6. Inference only.
- **ASC (2405.13131) and IC3 (2302.01328):** merge samples with an LLM at inference only.
- **Majority-vote RL:**
  - TTRL (2504.16084) and MM-UPT (2505.22453) work for discrete answers, but MM-UPT fails when the base model is weak (49.47 → 44.11).
  - TTRV (2510.06783): binary majority votes hurt on 4 of 5 benchmarks.
  - SRT (2505.21444): vote-based RL collapses after about 1,000 steps.
- **Self-judging bias (HalDec-Bench, 2511.20515):** a model judging its own captions drops to AUROC 54 vs 80 on others' captions.

**Partial scoops.**
- SENTINEL (2507.12455): own samples labelled by two-detector agreement, used for DPO; Qwen2.5-VL hallucination 15.0 → 4.7.
- CAPTURE self-loop (2405.19092): OWLv2 filter plus LLM merge for SFT; the filter adds only 56.68 vs 56.43.
- HalluciDoctor (2311.13614), Embodied captioning (2504.08531), Visual Fact Checker (2404.19752).
- RubiCap (2603.09160): majority over 5 external teacher models, used as an RL rubric.

**Still open:**
- Object-level vote over one adapter's own samples as an SFT pseudo-label filter.
- Extractive, LLM-free fusion of agreed sentences.
- Vietnamese self-training judged by instance labels.

**Real data must stay in the mix:** accumulate rather than replace (2404.01413), and run one round only.

**Resources a reviewer will raise.**
- **COCO-35L Vietnamese:** public machine translations of all COCO train captions (`coco_mt_train.jsonl.bz2`). A COCO pool would need this as a baseline; machine translation trails native Vietnamese captions by about 11 BLEU (2402.05512).
- **XM3600:** 7,350 human Vietnamese captions (CC BY 4.0). 1,855 of its images have dense, human-verified positive and negative Open Images labels, usable as an instance-like judge.
- **UIT-OpenViIC (2305.04166):** 13.1k Vietnam images, 61k captions. **It overlaps KTVIC: 401 of 558 test and 2,464 of 3,769 train images are near-duplicates (2602.22678).**
- **OpenViVQA:** MIT licence, from the same crawl, so the same de-duplication applies.

## 4. Designs

The rule is pre-registered before any unseen-image data is seen (`vote_fuse.py`):
- 6 samples per image (T 0.8, top-p 0.95).
- A sentence is admissible only if all its KTVIC-lexicon objects appear in ≥3 of 6 samples.
- Greedy cover of at most 2 admissible sentences for the detailed target, at most 1 for the short target.

### D1. Vote-then-fuse self-distillation on UIT-OpenViIC with captions hidden

**Pool.** 800 OpenViIC-train images, after strict near-duplicate removal against KTVIC train and test. Use `scripts/near_dup.py` with CLIP cosine ≥ 0.90, deliberately stricter than its default.

**Step 0: labelling, which is also the gate (2.2 GPU-h).**
- fuse2_s42 produces 6 samples (about 6 s), a greedy detailed caption (3 s) and a greedy short caption (1 s) per image.
- On CPU, score vote-then-fuse, greedy, MBR pick and one held-out human against the hidden OpenViIC captions: 1v4 protocol, paired bootstrap, plus CIDEr-D.
- **Kill if** vote-then-fuse − greedy < +1.5 F1, or its CI includes 0, or its precision is below greedy's.

**Step 1: three arms (2.4 GPU-h).** Each continues fuse2_s42 for 1 epoch on 1,600 pseudo rows + 1,600 replayed KTVIC rows (400 steps × 7.3 s each). The arms differ only in the pseudo labels:
- **V:** vote-then-fuse.
- **G:** greedy captions. This controls for confirmation bias; the MBR-finetuning result predicts it does not help.
- **H:** OpenViIC's human captions, through the fuse2 recipe. This is the skyline; report the fraction of H's gain that V recovers.

**Step 2: evaluation (about 3.9 GPU-h).**
- KTVIC test, both prompts.
- OpenViIC test, 300 de-duplicated images, both prompts.
- COCO-500 and UIT-ViIC test, short prompt, against instance labels. Here the judge uses a different lexicon than the vote.
- Free extra on CPU: score KTVIC test outputs against KTVIC captions plus OpenViIC's captions on the roughly 400 overlapping images.

**Total:** about 8.5 GPU-h.

**Success requires all of:**
- V − fuse2 on KTVIC F1 larger than the seed spread (fuse2 s42 vs s43), with p < 0.05.
- V > G.
- No precision loss against instance labels.

**Confirmation-bias controls.**
- Only images the teacher never saw, which fixes E5's failure mode.
- Selection over samples, not imitation of greedy output; arm G measures plain self-training.
- Human rows replayed in every arm; one round only.
- External judges: hidden human captions, instance labels, CIDEr.
- A per-class audit of the systematic false positives that voting cannot remove.
- Extractive fusion only, so no new text is invented.

**Extension if V > G:** a student trained from scratch on fuse2 rows + V rows (3.8 GPU-h), as Noisy Student does.

### D2. Cross-fitted vote-then-fuse vs gold-selected RFT on the same samples

- **Gate:** use the half-A adapter's queued samples on half B, plus greedy decoding of 600 half-B images (about 0.5 GPU-h). Compare vote-then-fuse, RFT's gold pick, one sample and greedy against half B's own captions.
- **Train only if** the gate passes **and** the cross-fitted RFT itself beats fuse2.
  - Training needs the half-B adapter's samples on half A (+3.1 h) and a student (about 5.7 h); total about 10 GPU-h.
- **Kill:** vote-then-fuse rows more than 3 F1 below the RFT pick, or below greedy.

### Rejected by the pilots

| Idea | Reason |
|---|---|
| Cross-adapter / co-training filters | dF1 −6.1 on KTVIC; +0.3 n.s. on COCO |
| Detector agreement on KTVIC | Recall falls to 17.8 |
| Dawid-Skene weighting | Worse than counting votes |
| Vote-then-fuse on seen train images | E5 null in both modes |
| COCO pool without a machine-translation baseline | COCO-35L Vietnamese already exists |
| Object-majority RL | Collapse risk (SRT, TTRV); revisit only after D1 |

## 5. Caveats and side findings

- **Matcher artifact affecting the paper's own COCO numbers (`audit_keo.py`).** `coco80_vi.json` maps bare "kéo" (the verb "pull", or "ngăn kéo" = drawer) to scissors.
  - All 253 of zero-shot-detailed's scissors mentions are bare "kéo"; 217 are false.
  - This inflates its COCO CHAIR_i by about 2.0 points; VSPS-detailed by 0.6.
  - Fix: keep only "cái kéo" / "cây kéo".
- The KTVIC lexicon both drives the vote and scores KTVIC/OpenViIC results; CIDEr and the COCO-80 instance judge are the independent checks.
- Vote-then-fuse captions are about 25% shorter than fuse2-detailed (17.6 vs 24 words), which matters for the length penalty in CIDEr-D.
- OpenViIC is licensed for non-commercial research only.
- The COCO human calibration uses an English matcher, so part of the human-vs-machine gap may be matcher differences.

## 6. Files

All in `/tmp/claude-1000/-mnt-d-vsps-image-captioning/755eae04-5e4c-4ce1-ab21-d4bc106761ee/scratchpad/research_r2/A8/`:
- **Scripts:** `coco_gold_cache.py`, `pilot_coco.py`, `pilot_ds.py`, `calib_coco_fused_humans.py`, `pilot_ktvic.py`, `pilot_seeds.py`, `pilot_samples.py`, `vote_fuse.py` (includes a self-check), `pilot_vtf_1v4.py`, `pilot_heldout.py`, `memo_check.py`, `audit_classes.py`, `audit_keo.py`.
- **Outputs:** one `*.txt` per script.
- **Copied read-only from n3:** `coco5000_gold.json`, `e5_samples_train.jsonl`.

To run any script:
```
NCS_DATA=/mnt/d/vsps_image_captioning/data nice -n 15 python3 <script> [coco5000_gold.json | e5_samples_train.jsonl]
```