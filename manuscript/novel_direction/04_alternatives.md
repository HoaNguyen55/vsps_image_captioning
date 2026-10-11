# Three alternative directions (independent of XWit)

*Draft, 11/10/2026. Separate from `00_DE_XUAT.md` (cross-lingual witnesses), which this file does not modify.*

Starting point: VSPS object P/R/F1 is 41.5/36.7/39.0 and zero-shot is 31.6/57.1/40.7. Each direction below asks a different question about where that gap comes from. None of them adds a detector, an F1 reward, or a phrase-level loss.

---

## A. Mentionability: the trade-off is partly a salience mismatch, not hallucination

**Thesis.** Most of the precision zero-shot "loses" and most of the recall VSPS loses come from the same thing: neither system knows *which true objects a Vietnamese annotator would bother to mention*. If a captioner learns a mention probability per object, estimated from agreement among the 5 KTVIC annotators, P and R rise together against the references.

**Why it would remove the trade-off.** Reference-based object precision counts every object that is present but not mentioned in the references as a false positive. Reference-based recall only rewards objects the annotators chose to mention. The verifier answers a different question ("is it in the image?"), so it removes true-but-unmentioned objects (good for P) and also low-confidence-but-salient ones (bad for R). Once you condition on *mentionability* instead of *existence*, the two errors stop being linked through one threshold. A salient, mentionable object is kept even when Vintern says UNCERTAIN, because salient objects tend to be large and central and therefore real. A tiny background object is dropped even when it is SUPPORTED, because annotators never mention it. Both moves help both metrics.

**New measurement (the scientific contribution).** On the 300-image object gold (exhaustive human object lists, `data/object_gold`), split each zero-shot false positive into one of two classes:

- (i) **truly absent**: hallucination;
- (ii) **present but unmentioned**: a salience miss.

Do the same for each VSPS false negative: (iii) rejected by the verifier but present and mentioned, versus (iv) never proposed. The paper's headline number is the share of the "trade-off" that is (ii)+(iii) rather than real hallucination. To my knowledge no one has reported this decomposition for LVLM captioning, and certainly not for Vietnamese.

**Hypotheses (falsifiable).**

- **H-A1.** At least 40% of zero-shot object false positives on the gold-300 are class (ii). *Refuted* if under 25%: then the trade-off really is hallucination, and this direction should be dropped.
- **H-A2.** A mentionability score m(o, image) predicts "mentioned by ≥1 of 5 annotators" with AUROC ≥ 0.80 among *present* objects. The score is a small logistic or MLP head on box area, centrality, category prior and the captioner's own first-mention rank. *Refuted* if AUROC < 0.70.
- **H-A3.** Building SFT targets by ranking propositions on P(exists) × m, at a threshold chosen on dev, gives object P ≥ 41.5 and R ≥ 45 on KTVIC test (3 seeds). *Refuted* if any seed has P < 41.5 or R ≤ 36.7 + 3.

**First experiment (about 1 GPU-hour, mostly CPU).**

1. Reuse the existing zero-shot and VSPS outputs on the gold-300.
2. Run the object matcher you already have against both the gold lists and the references, then label classes (i) to (iv).
3. Fit m on the train-split references, using Qwen box proposals plus area, centrality and category frequency. Report the H-A2 AUROC.
4. Re-filter the existing Stage-1 propositions by P×m and score them *offline as captions*. No retraining, so only rendering costs GPU time.

This tests H-A1 and H-A2 directly, and gives an upper-bound preview of H-A3.

**Novelty search.**

- Object importance as "probability that an observer mentions it" goes back to [Berg et al., CVPR 2012](https://core.ac.uk/works/2253098) and person-centric follow-ups ([Chen & Grauman, arXiv 1604.04842](https://arxiv.org/pdf/1604.04842)). Those works predict what gets mentioned. They were not used to supervise LVLM captioners, and not to explain a P/R trade-off.
- Consensus weighting of *whole captions* exists ([Wang et al., IJCAI 2020](https://ijcai.org/proceedings/2020/92); [IC3, EMNLP 2023](https://aclanthology.org/2023.emnlp-main.556)). Neither works at the object level, and neither touches hallucination.
- CHAIR ([Rohrbach et al., EMNLP 2018](https://arxiv.org/pdf/1809.02156)) and [ALOHa (NAACL 2024)](https://arxiv.org/pdf/2404.02904) score against references or annotations. Neither separates "unmentioned" from "absent".
- [SPARC (arXiv 2502.01419)](https://arxiv.org/pdf/2502.01419) documents the precision-for-recall trade-off but fixes it with attention recalibration.

**Overlap verdict.** Low-to-moderate. The pieces exist: importance prediction from 2012, consensus captions from 2020/23. But two things appear new: the *decomposition of the hallucination/omission trade-off into salience error versus existence error*, and *mentionability-conditioned target construction for LVLM SFT*.

**Main risk.** A reviewer may say "you are just optimising for the reference distribution", i.e. metric gaming. Mitigation: also report P/R against the *exhaustive gold* and a human preference study. If the gold-P stays flat while reference-P/R rise, that is itself the finding: the old metric conflated two things. A second risk: if H-A1 fails, the direction ends in week 1. That failure is cheap and informative.

---

## B. The knowledge-verbalization gap: say exactly what you internally believe

**Thesis.** The 7B captioner's hidden states already encode object presence better than its captions express it. VSPS loses recall because it replaces that internal belief with the opinion of a *weaker external* judge (Vintern-1B). Building targets from the captioner's own linearly-probed belief closes the gap in both directions: it says what it knows, and drops what it does not.

**Why it would remove the trade-off.** Two separable failure modes exist:

- **omission**: the probe says present, but the model does not say it;
- **confabulation**: the probe says absent, but the model says it.

Zero-shot suffers mostly from confabulation. VSPS adds an independent verifier whose errors are not aligned with the captioner's knowledge, so it creates *new* omissions (correct beliefs vetoed by a 1B model). If targets are aligned to the captioner's own probe, the information used for the decision is the model's best available evidence, not a lossy proxy. The SFT objective then asks only for *verbalization consistency*, which costs no perception capacity and needs no new evidence source. Both error types can shrink toward the probe's error rate, with no new evidence source (unlike XWit).

**New learning signal.** "Belief-consistency targets". For each image:

- train a linear probe on mid-layer states, on the gold-300 dev split plus KTVIC references, to predict presence of each candidate object;
- the SFT target mentions an object iff the probe's calibrated p ≥ τ, whether or not the model said it;
- iterate: retrain the probe on the new model, rebuild the targets, and repeat once.

As far as I can find, no captioning work uses a probe's output as the *supervision target*.

**Hypotheses.**

- **H-B1.** On the gold-300, a linear probe on Qwen2.5-VL-7B mid-layer states has higher object-presence AUROC than Vintern-1B verification (K=5 or logit mode, κ≈0.79 vs K=5 per commit 0bd5a1c). *Refuted* if the probe's AUROC is less than or equal to Vintern's.
- **H-B2.** At least 30% of zero-shot false negatives (present in gold, not in caption) have probe p ≥ 0.7. This is a measurable "knows but doesn't say" rate. *Refuted* if under 15%.
- **H-B3.** SFT on belief-consistency targets gives P ≥ 41.5 and R > 50 (3 seeds), and the probe-verbalization disagreement rate falls by ≥ 50%. *Refuted* on either count.

**First experiment (about 2 GPU-hours on the 3090, 4-bit or bf16 with cached features).**

1. Run one forward pass of Qwen2.5-VL-7B on the gold-300 plus 500 train images.
2. Cache mean-pooled vision-token states at 4 layers, together with the hidden state at the position of the object query word in a templated prompt.
3. Train logistic probes per layer, then compute AUROC against the gold and compare with the Vintern logit verifier.
4. Count the H-B2 omissions.

No captioner training is needed to accept or kill the direction.

**Novelty search.**

- [Training-bias analysis (arXiv 2508.04567)](https://arxiv.org/pdf/2508.04567) shows linear probes reach above 95% on object presence while generation reaches about 81%, and blames the LM head. This is strong *support* for the premise. They mitigate by editing the head, not by building captioning targets.
- [The First to Know (ECCV 2024)](https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/6429_ECCV_2024_paper.php) probes first-token logits for abstention.
- [HALP (EACL 2026)](https://preview.aclanthology.org/credits/2026.eacl-long.287) and [VIB-Probe (arXiv 2601.05547)](https://www.alphaxiv.org/abs/2601.05547.md) use probes for detection or inference-time suppression.
- None measures *omission* (knows-present, not said), and none uses the probe as the target for caption SFT.

**Overlap verdict.** Moderate. The "LVLMs know more than they say" premise is published (2508.04567 is the closest). The new parts are: the omission side of the gap, measured on captions; and closing it by self-belief target construction, which makes the method recall-raising by design. It must cite 2508.04567 prominently and position against it.

**Main risk.** The probe may simply learn reference co-occurrence priors, i.e. language prior leakage. If so, belief-consistency targets *reintroduce* hallucination. Control: probe on vision-token states only (no text tokens), and test on counterfactual images (object masked out) as 2508.04567 does. A second risk is that H-B1 fails because Vintern is surprisingly strong. H-B2 stays publishable anyway.

---

## C. Calibrated epistemic captions: a third channel between "say" and "omit"

**Thesis.** The trade-off exists because a caption has only two actions per proposition, assert or omit, so every UNCERTAIN proposition is forced into one of them. Giving the captioner a calibrated third action, Vietnamese epistemic hedges ("có vẻ", "hình như", "có thể là"), turns captioning into calibrated belief reporting. Assertive precision then rises while total recall rises.

**Why it would remove the trade-off.** VSPS currently drops the UNCERTAIN bucket. That is where much of its recall loss lives, and it can be measured directly from the Stage-1 records. With a hedge channel, a proposition is (a) asserted if p ≥ τ_hi, (b) hedged if τ_lo ≤ p < τ_hi, (c) omitted otherwise. Precision of *asserted* content is set by τ_hi alone, recall of *mentioned* content by τ_lo alone. Two thresholds decouple what one threshold couples. The scientific question is whether a 7B captioner can learn *calibrated* Vietnamese epistemic markers, so that the empirical precision of hedged claims matches the stated level.

**Hypotheses.**

- **H-C1.** In the Stage-1 records, at least 25% of gold-present objects that VSPS drops fall in the UNCERTAIN bucket. *Refuted* if under 10%: then the hedge channel has nothing to recover.
- **H-C2.** After SFT with three-way targets, the empirical gold-precision of the asserted, hedged and omitted-but-probed tiers is monotone and within ±10 pts of the target levels (e.g. ≥0.8, 0.4–0.7). *Refuted* if hedged precision ≥ asserted precision, or if ECE > 0.15.
- **H-C3.** Asserted-only P ≥ 41.5, and mention-level R (asserted + hedged) ≥ 50. A Vietnamese human study also shows hedged captions are not rated less useful than VSPS captions. *Refuted* on any count.

**First experiment (about 1 GPU-hour).**

1. Compute H-C1 offline from the existing Stage-1 records and the gold-300.
2. Render three-way targets for 300 train images using a fixed hedge lexicon.
3. Run a short LoRA SFT (about 40 minutes on the 3090) and score tier-wise precision on the gold-300.

This is a pilot of H-C2 at small scale.

**Novelty search.**

- [Calibrating Expressions of Certainty (ICLR 2025)](https://arxiv.org/pdf/2410.04315) models certainty phrases as distributions for text LMs.
- [Verbalized calibration in VLMs (arXiv 2505.20236)](https://arxiv.org/pdf/2505.20236) finds VLMs overconfident in stated confidence, but for QA rather than captions.
- A [Utrecht MSc thesis (2025)](https://studenttheses.uu.nl/handle/20.500.12932/49908) fine-tuned BLIP-2 with hedges via SFT+PPO. It failed to align hedges with human expectations, and found metrics penalise hedging.

**Overlap verdict.** Moderate. Hedged captioning has been attempted (the thesis), but not with verifier-derived calibration targets, not as a fix for the P/R trade-off, and not in Vietnamese.

**Main risk.** Standard object P/R treats a hedge as a mention, so under the *conventional* metric the precision gain is not visible. Reviewers may call tier-split P/R "moving the goalposts". Pareto improvement *on the existing metric* is unlikely.

---

## Ranking (novelty × feasibility × chance of Pareto improvement, each scored 1–5)

| Rank | Direction | N | F | P | Product | Why |
|---|---|---|---|---|---|---|
| 1 | **A. Mentionability** | 4 | 5 | 4 | 80 | Week-1 test is almost all CPU on existing outputs. The mechanism acts *on the metric's own variable*, so P and R can rise together under the standard reference metric. |
| 2 | **B. Knowledge-verbalization gap** | 4 | 4 | 3 | 48 | The premise is supported by 2508.04567, so it is plausible but less novel. The probe can be built in 2 GPU-hours. The Pareto chance depends on the probe not leaking priors. |
| 3 | **XWit (00_DE_XUAT)** | 3.5 | 4 | 3 | 42 | Clean Neyman-Pearson story, but it needs a 3-language object normalisation pipeline. Its premise (low cross-lingual error correlation) is unproven, and it can fail at H1. |
| 4 | **C. Calibrated hedging** | 4 | 4 | 2 | 32 | Novel for Vietnamese and cheap, but it shows no gain under the conventional metric. Prior hedging work hit alignment problems. |

**Recommendation.** Run the week-1 tests of A (H-A1/H-A2) and B (H-B1/H-B2) in parallel: both reuse existing outputs and the gold-300. They are also complementary. A changes *what* is said and B changes *how the decision is made*, so if both pass, a combined paper ("the trade-off is a salience-and-verbalization artefact") is a single coherent thesis, not a lego.
