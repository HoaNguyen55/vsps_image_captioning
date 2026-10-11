# 04 — How to measure and report "no trade-off" (Pareto) between faithfulness and coverage

Agent 04, 2026-10-11. This extends `../research_wall/02_caption_evaluation_metrics.md`, which already holds the exact definitions of AMBER, DCScore, CAPTURE, CompreCap, CAPEval, CAPability and PoSh, plus the D1–D6 evaluation fixes. Those are not repeated. What is new here: (1) how 2024–2026 papers that *claim* a precision/coverage win actually report it, with their numbers; (2) papers that show the trade-off and how reviewers catch it; (3) the statistics for a dominance claim; (4) Vietnamese and multilingual sets with object-level gold; (5) the metric set and plots for the next VSPS paper.

"Opened" means I opened the arXiv abstract or HTML page on 2026-10-11. Numbers are copied from the table named. "Search-only" means I saw the number only in a search snippet. Those are marked UNVERIFIED.

## 1. Bottom line

The papers whose claims hold up report precision and coverage for the same captions, plus length, at more than one operating point (REVERSE NeurIPS 2025; OPERA CVPR 2024; CapMAS ICML 2025). Reviewers catch fake wins through length and recall. "Precision not down" has to be a non-inferiority test with a margin fixed in advance. Reference-derived gold makes P a lower bound, and that bias hurts the higher-recall system.

## 2. Metrics: what each measures, and whether it carries over to Vietnamese

| Metric (venue, link) | Precision side | Coverage side | Open vocab? | Vietnamese / 3090 cost |
|---|---|---|---|---|
| **CHAIR** (Rohrbach et al., EMNLP 2018) | CHAIR_i, CHAIR_s | none on its own. Papers add object recall against COCO segmentation labels | No (80 COCO classes + synonyms) | Already in VSPS (`rescap/chair.py`, 113-entry vi lexicon). 0 GPU |
| **AMBER** (Wang et al., arXiv 2311.07397, opened; still **no venue** in arXiv comments, v2 Feb 2024; code on GitHub) | CHAIR, Hal (share of captions with ≥1 hallucination), Cog (hallucinated objects drawn from a list of likely-but-absent objects) | **Cover** = mentioned ∩ annotated / annotated, against **all visible objects** annotated by humans | Closed (AMBER list) | The VSPS exhaustive gold is an AMBER-style annotated set. Report under AMBER's names. 0 GPU |
| **POPE** (Li et al., EMNLP 2023, arXiv 2305.10355, opened) | yes/no polling: accuracy, precision, recall, F1, yes-ratio under random/popular/adversarial negatives | none: it is discriminative, not a caption metric | Closed | Measures the *verifier* (Vintern), not the captioner. See §4 |
| **FaithScore** (Jing et al., Findings EMNLP 2024, arXiv 2311.01477, opened) | share of atomic facts verified against the image | **none**: the abstract defines faithfulness only | Open | Needs an LLM fact extractor and a VLM verifier. A Vietnamese port is the VSPS proposer + verifier itself, which makes it circular. Use only on a human-checked subset |
| **ALOHa** (Petryk et al., NAACL 2024, arXiv 2404.02904, opened) | LLM-extracted objects matched (Hungarian) to references + detections. Finds 13.6% more hallucinated objects than CHAIR on HAT and 30.8% more on nocaps | none | Open | English LLM parser. Its value for VSPS is as an **open-vocabulary audit** of the closed-lexicon CHAIR-vi (§5) |
| **CLAIR** (Chan et al., EMNLP 2023, arXiv 2310.12971, opened) | one LLM judge score (+39.6% relative correlation over SPICE on Flickr8K-Expert) | mixed into one score | Open | One scalar, so it **cannot show** a Pareto claim. Cite only as an overall-quality check |
| **Polos** (Wada et al., CVPR 2024, arXiv 2402.18091, opened) | learned metric from 131K human judgments (Polaris), SOTA incl. FOIL | mixed into one score | n/a | English-trained. Same objection as CLAIR |
| **CAPTURE** (Dong et al., arXiv 2405.19092, no venue) | precision over parsed objects, attributes and relations | recall over the same, combined as F1 | Semi | English scene-graph parser. Not portable without a vi parser |
| **DCScore / DeCapBench** (Ye et al., ICLR 2025, arXiv 2503.07906) | s_p over primitive units verified by GPT-4o | **s_r with correct extra units added to numerator and denominator** (fixes incomplete references) | Open | Copy its *recall correction* into the lexicon metric (02/D2). 0 GPU |
| **CompreCap** (Lu et al., CVPR 2025, arXiv 2412.08614) | attribute and relation accuracy | object coverage over manually segmented regions | Closed vocab | Template for "coverage over a human region list" |
| **CapMAS factuality/coverage** (Lee et al., **ICML 2025**, arXiv 2412.15484, opened; code github.com/adobe-research/CapMAS) | P = share of atomic propositions verified true | **R = share of curated VQA items on IIW-400 answerable from the caption alone**; F1 = harmonic mean | Open | The closest published pair to "VSPS precision + coverage". The QA-coverage idea ports to Vietnamese if ~5–10 questions per image are written by hand on the 300-image gold set |

**What the strongest papers actually report: separate P and R for the same captions, plus length.** Single-scalar metrics (CLAIR, Polos, CIDEr) can hide a trade-off and should only be secondary.

## 3. How papers that claim "both improve" report it (numbers copied)

### 3.1 REVERSE: Generate, but Verify (Wu, …, Darrell, Chan). NeurIPS 2025. arXiv 2504.13169 (opened HTML v2). Project page reverse-vlm.github.io

Table 1 reports CHAIR-MSCOCO and AMBER-G side by side.

| Backbone | Method | CHAIR_i ↓ | CHAIR_s ↓ | AMBER CHAIR ↓ | AMBER Cover ↑ |
|---|---|---|---|---|---|
| LLaVA-v1.5 7B | baseline | 15.4 | 50.0 | 7.8 | 51.0 |
| LLaVA-v1.5 7B | REVERSE τ=0.003 | 10.3 | 37.0 | 6.0 | **52.2** |
| LLaVA-v1.5 7B | REVERSE τ=0.0003 | 6.1 | 13.6 | 4.0 | **26.9** |
| LLaVA-MORE 8B | baseline | 14.4 | 52.0 | 7.8 | 53.1 |
| LLaVA-MORE 8B | REVERSE τ=0.003 | 12.2 | 42.4 | 6.5 | 54.8 |
| Qwen2.5-VL FT 3B | baseline | 12.2 | 45.8 | 7.7 | 51.7 |
| Qwen2.5-VL FT 3B | REVERSE τ=0.01 | 10.5 | 39.4 | 7.5 | 51.5 |

- **How it reports.** Figure 5 sweeps the verification threshold τ and plots CHAIR (↓) against Coverage (↑). τ=0.003 is chosen as "the peak of the performance frontier". Appendix Table A.2 gives **bootstrapped 95% CIs**: CHAIR_i 10.3 (8.94–11.68), Cover 52.2 (51.1–53.5).
- **Trade-off check.** The paper shows it itself: the stricter τ halves Cover (51.0 → 26.9). On Qwen2.5-VL 3B, Cover is −0.2 (51.7 → 51.5). The Pareto claim holds only at one operating point. **This is the reporting template VSPS should copy**: the knob is the verifier threshold, as in VSPS.

### 3.2 CapMAS (Lee et al., ICML 2025) and ReflectCAP (arXiv 2604.12357, opened HTML v1, 2026, no venue)

ReflectCAP Table 1 uses the CapMAS factuality (P) / coverage (R) metrics on IIW-400. Selected rows:

| Model | Zero-shot P / R / F1 | ReflectCAP P / R / F1 |
|---|---|---|
| Qwen2.5-7B | 68.3 / 57.9 / 62.7 | 68.8 / 62.3 / 65.4 |
| GPT-4.1-nano | 78.9 / 62.6 / 69.8 | **78.0** / 67.2 / 72.2 |
| Qwen2.5-32B | 71.9 / 64.0 / 67.7 | **69.9** / 66.4 / 68.1 |
| InternVL-38B | 72.5 / 57.8 / 64.3 | 73.7 / 64.2 / 68.6 |

- **Lesson.** The paper says it "sets a new Pareto frontier", yet P falls on 2 of the 8 backbones (−0.9 and −2.0) and it reports no CI. A careful reviewer would reject "no trade-off" from this table. With a non-inferiority margin of 1 pt, the GPT-4.1-nano row passes and the Qwen2.5-32B row fails. Its Figure 3 plots F1 against inference TFLOPs, which is a useful second Pareto axis (cost) for VSPS's single-pass captioner compared with multi-agent pipelines.

### 3.3 OPERA (Huang et al., CVPR 2024, arXiv 2311.17911, opened HTML): report at two lengths

LLaVA-1.5, CHAIR_S / CHAIR_I: greedy 45.0 / 14.7 vs OPERA 44.6 / 12.8 at 512 new tokens (Table 1), and 20.6 / 6.2 vs 14.2 / 5.2 at 64 tokens (Table 2). The gain depends strongly on length. Reporting both lengths is now the de-facto standard in decoding papers, and VSPS should report at least a short and a long setting for the zero-shot baseline.

### 3.4 Papers that expose the trade-off (what reviewers will look for)

- **Targeting the Attention Heads Behind Object Hallucination in LLaVA** (Sandhu et al., Actionable Interpretability Workshop @ COLM 2026, arXiv 2608.24966, opened). CHAIR_s 0.370 → 0.230 and CHAIR_i 0.156 → 0.096 (p < 0.001), but **object recall 0.78 → 0.70**, and the outputs are "shorter and more conservative". This is exactly the profile of VSPS v1 (P up, R down), and the paper calls it a trade-off.
- **The Devil is in the EOS** (Mohamed & Kementchedjhieva, COLM 2025, arXiv 2507.20077, opened abstract). Reducing the EOS bias gives longer, more detailed captions "along with an expected rise in hallucinations". The EOS bias is a clean **detail knob** that can be applied equally to every system (§6).
- **FADE** (arXiv 2606.29431) reports VISTA cutting recall from 80.6 to 62.6 on LLaVA-1.5. **SPARC** (arXiv 2502.01419) reports F1 83.67 / R 79.98 with CHAIR_s 51.52 against PAI's 34.92 at R 72.44. Both are search-only and **UNVERIFIED**. They are useful only as evidence that 2025–2026 papers routinely add recall and F1 next to CHAIR.

## 4. POPE versus generative metrics

- POPE is a yes/no probe, so it scores the **verifier role**, not caption quality. CapMAS (ICML 2025, abstract) reports that VQA-style performance "may not correlate" with detailed-caption ability. Earlier POPE work (see `06_verifier_precision.md`) shows answers are yes-biased and memorised.
- **For VSPS:** report POPE (random / popular / adversarial, with **yes-ratio**) for Vintern-1B and Qwen2.5-VL-7B in the verifier section only. Do *not* use it as evidence about the captioner. A Vietnamese POPE can be built directly from the 300-image exhaustive gold: positives are gold classes, adversarial negatives are high co-occurrence classes absent from the gold (the 02/D5 Cog list).
- No verified Vietnamese POPE exists. The "ViHallu" found in search is either a Chinese/English visual-variation method (Dai et al., ACM MM 2025, arXiv 2507.22003, not Vietnamese) or the DSC2025 *text-only* Vietnamese task (arXiv 2601.04711). A Vietnamese POPE derived from the gold would be a small new contribution.

## 5. The gold problem: why reference-derived precision is a lower bound

1. **Reference incompleteness → P is a lower bound, R is salient recall.** A correct object that is absent from the 5 KTVIC references counts as a hallucination. In the repo, human ref #1 scored against the other four reaches only R 46.9 / P 85.5 (`../OBJECT_GOLD_PROTOCOL.md`). Penquitt et al. (arXiv 2609.21822, cited in 02) find up to **+40% objects** on COCO after re-annotation, mostly small, occluded or dense. Rankings stayed mostly stable.
2. **The bias favours the conservative system.** Expected false "hallucinations" grow with the number of correct non-reference mentions, so a higher-recall system loses more precision to the gold artefact. The direction is safe: if VSPS-v3 mentions more objects **and** its reference-gold precision is not lower, its true precision is very likely not lower either. Say this in the paper and show it numerically: report P on reference-gold and on exhaustive gold for the same 300 images, and the gap per system.
3. **The closed lexicon hides out-of-vocabulary hallucinations, so bias 2 cannot be signed.** An object not in the 113-entry lexicon is never counted, correct or wrong. Fix this with an **ALOHa-style open-vocabulary audit** on a sample: extract every noun phrase from 100 captions per system and have one human label each as present or absent. Report the open-vocabulary hallucination rate next to CHAIR-vi. Without it, a reviewer can say the gain is a lexicon artefact.
4. **The DCScore correction** (02/D2) is the published way to credit correct extras. Use the gold-only version on the 300 images, so no verifier is involved and there is no circularity with Vintern.
5. **Lenient hypernym matching** inflates recall for vague captions. Fix the one-vague-mention-covers-all bug from 02 *before* any Pareto claim, and always show `exact` beside `lenient`.

## 6. The "detail knob": plots that make dominance visible

A single operating point invites "you just picked a different length". The literature uses a sweep (REVERSE Fig. 5, OPERA's two lengths, HallE-Control's controllable detail; Zhai et al., arXiv 2310.01779, opened, no venue, code released, abstract claims "maintains object coverage" with no number in the abstract). For VSPS:

- **Knobs, applied equally to every system:**
  - (a) `max_new_tokens` ∈ {32, 64, 128, 256};
  - (b) an EOS logit bias as in *The Devil is in the EOS*, which needs no retraining and is fair to zero-shot and SFT;
  - (c) for the teacher pipeline only: verifier threshold τ and entity budget k (8 → 12 → 16), which shows where recall is lost (proposal vs verification vs rendering).
- **Plot 1 (main figure): object P vs R on the exhaustive gold**, one curve per system over the knob, with iso-F1 contours and 95% bootstrap ellipses or crosses at each point. Dominance means the VSPS curve sits up and to the right of zero-shot and VSPS-v1 at every matched recall.
- **Plot 2: CHAIR_i (or 1−P) vs #gold objects mentioned per caption.** This is the length-controlled view and defuses the "shorter captions" objection. Report a **matched-length** comparison: P and R of each system at the knob setting whose mean #mentions is closest to zero-shot's.
- **Plot 3 (optional): F1 vs inference cost** (s/image or TFLOPs), following ReflectCAP Fig. 3. VSPS is single-pass, so this is where it beats verify-at-inference methods such as REVERSE and CapMAS.
- Table: at the default setting, P, R, F1, Cover, CHAIR_i, CHAIR_s, Hal, #mentions and words, for both reference-gold (558) and exhaustive-gold (300).

## 7. Statistics for a dominance claim

Opened today: Dror, Shlomov & Reichart, *Deep Dominance*, ACL 2019 (aclanthology.org/P19-1266; `deepsig` on PyPI). Standard references not re-opened today: Koehn, EMNLP 2004 (paired bootstrap for MT); Berger, *Technometrics* 1982 and Berger & Hsu, *Statistical Science* 1996 (intersection-union tests); Agarwal et al., NeurIPS 2021, arXiv 2108.13264 (stratified bootstrap CIs over seeds).

1. **Unit: the image.** Use a paired bootstrap over test images, 10,000 resamples, and **the same resample indices for ΔP, ΔR and ΔF1**, recomputing the micro ratios (sum of hits / sum of mentions) on each resample. This preserves the P–R correlation. `scripts/score_ci.py` already does paired bootstrap, so extend it to the joint version.
2. **Hypotheses, fixed before testing:**
   - H_R: ΔR > 0 (superiority).
   - H_P: ΔP > −δ, with δ = 1.0 pt fixed in advance (non-inferiority).
   - Claim "recall up, precision not down" iff the 95% one-sided lower bounds of ΔR > 0 **and** ΔP > −δ. By Berger's intersection-union principle the conjunction is valid at α without a Holm correction. Report "precision up" only if ΔP's lower bound > 0.
   - Run this against **both** VSPS-v1 and zero-shot. Against zero-shot (P 31.6), precision superiority is likely and recall non-inferiority (δ on R) is the hard side, so state which side is superiority and which is non-inferiority for each comparison.
3. **Seeds.** Train 3 (better 5) seeds. Report mean ± sd and a **two-level bootstrap** (resample seeds, then images) so the CI includes training variance. As a robustness check, run ASO (`deepsig`) on the per-seed F1 distributions and report ε_min < 0.5. Deterministic baselines (zero-shot greedy) have sd 0, and the paper should say so.
4. **Per-image win rate.** Report the share of images where R rises and P does not fall, with a sign test. It is easy to read and hard to argue with.
5. **Human anchor.** Use the exhaustive gold with 2 annotators + adjudication and report κ (the protocol already requires κ ≥ 0.6 on calibration). For any LLM/VLM-judge metric, add human κ on a subset (Fu & Liu, Findings EMNLP 2025, cited in 02).

## 8. Vietnamese and multilingual sets with object-level gold

| Dataset | Source / size (opened) | Object-level gold? | What it reports | Use for VSPS |
|---|---|---|---|---|
| **KTVIC** (Pham et al., arXiv 2401.08100; no venue on arXiv page) | 4,327 life-domain images, 21,635 captions | **No.** Captions only | BLEU, METEOR, CIDEr, ROUGE | Main set. Object gold only from the VSPS 300-image exhaustive annotation |
| **UIT-ViIC** (Lam et al., ICCCI 2020, arXiv 2002.00175) | 3,850 **MS-COCO** ball-sports images (2017 edition per a survey), 19,250 captions | **Indirectly, yes**: COCO instance labels exist for these images, so a COCO-80 → Vietnamese class map gives a CHAIR-style gold for free. ID manifest not found online; distributed from the UIT lab site (UNVERIFIED) | n-gram metrics | Cheap second test set with **non-reference object gold**. The domain is narrow (sports) |
| **UIT-OpenViIC** (Bui et al., arXiv 2305.04166, "submitted to Elsevier") | Vietnamese complex scenes; size not in the abstract | Not stated (captions only per abstract) | Transformer baselines; CAMO | OOD check only |
| **ViTextCaps** (Nguyen et al., arXiv 2604.27712, 2026; from 04 file) | 15,729 images, 74,970 captions, scene text | No | Captioning metrics | Out of scope (OCR-centred) |
| **Crossmodal-3600** (Thapliyal et al., EMNLP 2022, arXiv 2205.12522) | 3,600 geographically diverse **Open Images** photos, 36 languages; **vi: 7,350 captions** (3,450 images with 2 captions, 150 with ≥3), mean 18.0 words (search summary of the paper table) | **Indirectly**: Open Images has human-verified image-level labels and boxes. The join by image ID is not tested (UNVERIFIED) | Used to rank multilingual captioners against human judgments | Strongest **multilingual** second benchmark: same images in vi and en, so cross-lingual P/R are directly comparable |

No Vietnamese benchmark reports object hallucination or coverage at all, and SHROOM-Visions 2026 skips Vietnamese (02/A6). That gap is itself a contribution statement.

## 9. Recommended metric set and plots

The five picks below are the recommendation. Concretely:
- **Primary table (exhaustive gold, 300 images, κ reported):** object P, R (= AMBER Cover) and F1 with `exact` matching (`lenient` in the appendix, after the vague-mention fix); Hal; CHAIR_i; Cog; #gold objects mentioned; words per caption.
- **Secondary table (reference gold, 558 images):** CHAIR_i/s, P/R/F1, DCScore-corrected R, CIDEr/BLEU-4. Put reference-gold P and exhaustive-gold P side by side on the same 300 images.
- **Audits:** open-vocabulary human audit (100 captions per system); POPE-vi for the verifier only; optionally CapMAS-style QA coverage on 100 images.
- **Plots and statistics:** as in §6 and §7.

## Top picks for VSPS

1. Headline = object P / R(AMBER Cover) / F1 + Hal + #mentions on the 300-image exhaustive gold; reference-gold CHAIR/P/R on all 558 images as secondary, with the lower-bound gap shown.
2. Main figure = P–R curves over a shared detail knob (max_new_tokens or EOS bias) with iso-F1 lines and CIs, copying REVERSE NeurIPS 2025 Fig. 5 / Table A.2.
3. Claim test = joint paired bootstrap: ΔR > 0 (superiority) AND ΔP > −1 pt (non-inferiority), as an IUT against both v1 and zero-shot; 3–5 seeds with a two-level bootstrap.
4. Close the loopholes: matched-length comparison, open-vocab human audit (ALOHa-style), the vague-mention lenient fix, and POPE-vi used for the verifier only.
5. Add one second set with non-reference object gold: UIT-ViIC + COCO labels, or XM3600-vi + Open Images labels.

Sources (opened 2026-10-11): arxiv.org/abs/2311.07397, /2311.01477, /2404.02904, /2310.12971, /2402.18091, /2305.10355, /2310.01779, /2401.08100, /2002.00175, /2305.04166, /2205.12522, /2412.15484, /2504.13169 (+html v2), /2604.12357 (+html v1), /2507.20077, /2608.24966, /html/2311.17911; aclanthology.org/P19-1266; github.com/adobe-research/CapMAS.
