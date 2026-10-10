# 08 — Journal standards for 2025-H2 and 2026: what Q1/Q2 journals published on captioning hallucination and low-resource captioning, and the experimental bar VSPS must meet

Research-wall agent 08, 2026-10-10. This extends `../novelty/10_journal_sweep.md`, which covered 2024 to early 2026 and asked about overlap only. This file adds:
- papers from 2025-H2 and 2026 that 10_journal_sweep did not cover;
- the **experimental protocol** of the papers whose full text I could open;
- a reviewer-expectation checklist, compared against the v10 manuscript.

## Method

- **OpenAlex**: 5 title and abstract queries (caption, captioning, hallucination(s), object hallucination vision-language), limited to 24 journals from 2025-01-01. The journals were TALLIP, Neurocomputing, PRL, ESWA, IPM, IEEE Access, MTAP, NCA, KBS, TMM, TCSVT, CVIU, PR, TOMM, EAAI, Applied Intelligence, Multimedia Systems, JVCIR, IVC, SPIC, Sci. Rep., InfFus, TIP and Neural Networks. The queries returned 367 works. Filtered to 2025-07 onward and to hallucination, low-resource, LVLM or detailed captioning, 54 remained, and I triaged them by hand. I also ran 21 language-specific title queries (Vietnamese, Hindi, Bengali, Arabic, Urdu, Indonesian, Thai, Korean, multilingual, low-resource), with no venue restriction.
- **Crossref**: 4 searches inside TALLIP (ISSN 2375-4699) and 4 general journal-article searches from 2026-04 onward, to cover OpenAlex's indexing lag.
- **Full texts opened** (needed to extract the protocol):
  - Sci. Rep. 2026 (two papers, nature.com HTML and the accepted-manuscript PDF);
  - IEEE Access 2026 Metric-Driven RL (OA PDF from ieeexplore);
  - arXiv versions of MHR (TOMM 2026) and CLVA (PR 2026);
  - arXiv version of Adjudicated Captioning (IEEE Access 2026).
- **Could not open**: ACM DL (TALLIP, TOMM) returned 403, Elsevier pages blocked the request or the abstract was elided, and Firecrawl refused the IP. Anything rated from the abstract alone is marked **[abstract]**, and anything rated from the title alone is marked **[title]**.

**Bottom line**
- **No 2025-H2 or 2026 journal paper overlaps VSPS at HIGH.** None verifies typed propositions offline into SFT targets, and none evaluates hallucination in Vietnamese detailed captioning.
- **The experimental bar is above v10.** Q1/Q2 hallucination papers in 2026 routinely have:
  - 2 to 4 backbones;
  - 3 to 7 inference-time baselines (VCD, OPERA, DoLa, DeCo and similar);
  - POPE and CHAIR, often with AMBER;
  - mean ± sd over 3 runs.
- **The low-resource captioning bar** in Sci. Rep. 2026 and TALLIP 2025 is n-gram metrics plus a 200-image human evaluation with 3 raters and κ.
- **What v10 lacks** (from a grep of `manuscript/FAIR_28.08.26_v10_EN_IEEE.docx`): OPERA, DoLa, POPE, AMBER and a second backbone. It already has VCD, seeds, bootstrap, κ, Wilcoxon, BLEU and CIDEr.

---

## (a) Papers (new relative to novelty/10, or newly read in full)

### a1. Read in full: their protocols set the bar

| # | Paper | Venue / year / DOI | Method (1–2 sentences) | Relevance to VSPS | Action |
|---|---|---|---|---|---|
| 1 | **Benchmarking large vision language models for multilingual image caption generation in low resource settings.** M. Hussain, I. Khan, J. Rashid, T. Althobaiti, M. S. Saleem, A. Alameri | *Scientific Reports* 2026-09 (Springer Nature, Scopus Q1). DOI 10.1038/s41598-026-70568-5 | Builds ZARWA-v1, a bilingual Urdu/Arabic caption corpus translated from English with human verification (test split reviewed exhaustively). It benchmarks 9 VLMs (Qwen2.5-VL, Pangea, PALO, mBLIP, PaliGemma2, LLaVA-OV, plus Florence-2, InstructBLIP and BLIP-2) under zero-shot, LoRA and QLoRA; **QLoRA Qwen2.5-VL is best**. Its error analysis finds **object hallucination is the largest error class (21.9% Urdu, 20.3% Arabic)**, and BLEU and BERTScore barely separate the flagged captions (BLEU-4 44.1 vs 49.8). | Overlap **low–medium**: same backbone and recipe as VSPS, also low-resource, but no mitigation. **Metric/benchmark** and must-cite motivation: "QLoRA LVLM captioners in low-resource languages hallucinate and n-gram metrics miss it." | Cite in the Introduction as independent 2026 evidence. Copy its protocol: 3 seeds, a 200-image human evaluation with 3 raters, κ, and an error taxonomy. |
| 2 | **Mitigating multimodal hallucinations through visual attention tracing and origin-point regeneration (HB).** B. J. Li, H. Yu, Y. Han, J. Ren, M. Dai, S. Bao | *Sci. Rep.* 2026-06. DOI 10.1038/s41598-026-52390-1 | A training-free decoder that tracks a visual attention score, detects the token where attention drifts to text, backtracks there and regenerates. Reports POPE F1 91.4 and CHAIR_S 40.2 on LLaVA-1.5. | Overlap **none–low** (decoding). **Baseline protocol reference.** | Use it as the template for the baseline table (see a3). |
| 3 | **Mitigating hallucination in MLLMs via cross-layer visual anchors (CLVA).** C. Yang, S. Cai, J. Yuan, C. Hu | *Pattern Recognition* 2026-07 (Elsevier, Q1). DOI 10.1016/j.patcog.2026.114380; arXiv 2603.25088 (read) | Training-free; strengthens mid-layer visual anchors and suppresses the deep-layer attention that regresses to early visual noise. | Overlap **none**. Protocol reference: 3 backbones and time/VRAM overhead reported. | Report VSPS overhead the same way (VSPS has zero inference overhead, which is a selling point). |
| 4 | **Mitigating Multilingual Hallucination in LVLMs (MHR).** X. Qu, M. Song, W. Wei, D. Liu, J. Dong, Y. Cheng | *ACM TOMM* 2026 (ACM, Q1). DOI 10.1145/3797025; arXiv 2408.00550 (read) | Two stages: multilingual SFT, then cross-lingual DPO on hallucination-aware pairs. **Languages, now verified**: en, ru, de, zh, ja, fr, es, pt, uk, bg, tr, ar, ko. **Vietnamese is not included.** Benchmarks are POPE-MUL, MME-MUL and AMBER-MUL; backbones are LLaVA-1.5 and CogVLM. | Overlap **medium** for C5. This resolves the "unverified" item in novelty/10: VSPS may claim "first for Vietnamese detailed captioning". | Must cite and contrast. Optionally run its POPE-style Vietnamese probe (see d4). |
| 5 | **Metric-Driven RL for Object Hallucination Reduction in LVLM-Based Image Captioning.** T. Nguyen, H. S. Yoon, T. M. Luu, E. Yoon, C. D. Yoo | *IEEE Access* 2026 (IEEE, Q1/Q2). DOI 10.1109/ACCESS.2026.3723028 (OA PDF read) | PPO adapters on frozen InstructBLIP, with an Object Consistency Score reward (correctness + coverage) and KL. Up to −41% CHAIR_S on COCO and −29% CCEval on VG. | Overlap **low–medium** (same task and metric, RL instead of verified SFT). **Baseline-to-compare** in Related Work. **Low bar**: it copies baseline numbers from the LURE paper and reports no seeds, no human evaluation and no significance tests. | Cite it. Note that it reports **Coverage** (object recall) next to CHAIR, as VSPS does with object R. Use it to justify P/R/F1. |
| 6 | **Adjudicated Captioning: Multi-Agent Alignment Scoring and Consensus-Distilled Beam Arbitration for Strict Zero-Shot Image Captioning.** T. T. Duy, T.-P. Doan, L. Nguyen-Vu, N. T. V. Khanh | *IEEE Access* 2026. DOI 10.1109/ACCESS.2026.3719341; arXiv 2607.28986 (read) | Inference-time frozen verifier re-ranking plus a Borda-consensus beam reranker on top of IFCap. CIDEr 117.6 on Karpathy COCO; reference-proxy CHAIR_S drops from 13.28% to 7.84%. Vietnamese author group, English data. | Overlap **low**: "verifier consensus" happens at inference and is not used to build training targets. | Optional cite as a contrast for verifier consensus at inference time. |

### a2. Abstract- or title-level (2025-H2 / 2026, not in novelty/10)

| # | Paper | Venue / DOI | Summary | Overlap / role | Action |
|---|---|---|---|---|---|
| 7 | Continual Learning for Image Captioning in Hindi. S. K. Mishra, S. Saha, P. Bhattacharyya | **ACM TALLIP** 2025. 10.1145/3749641 [abstract] | Continual-learning LSTM/GRU Hindi captioning on translated MS-COCO. | None. **Shows what TALLIP publishes in captioning**: translated-COCO, n-gram metrics, no LVLM, no hallucination. | Positions VSPS as the first LVLM-hallucination captioning paper in TALLIP. Say so in the cover letter. |
| 8 | Hi-MetaCap: Object Relational Transformer in Meta-Learning for Hindi Captioning. S. K. Mishra, S. Chakraborty, S. Saha, P. Bhattacharyya | **TALLIP** 2025. 10.1145/3749642 [abstract] | Few-shot meta-learning ensemble with pseudo-captions; works with 1% of the paired data. | None. Pseudo-label confidence weighting is loosely related to the verifier gate. | Optional cite. |
| 9 | ChitraVivran: Real-Time Attention-Based Hindi Image Captioning. H. Sharma, D. Padha, Y. P. Singh | **TALLIP** 2025-12. 10.1145/3779214 [abstract] | Ensemble-feature Hindi captioner; builds PASCAL-1K-Hindi by translation; BLEU-3/4 on Flickr8K-Hindi. | None. | Optional cite. |
| 10 | Exploring Semantic Attributes for Image Caption Synthesis in Low-Resource Assamese. P. Choudhury, P. Guha, S. Nandi | **TALLIP** 2025. 10.1145/3717612 [abstract] | Visual-semantic self-attention with XE+RL; BLEU-n and CIDEr on COCO-Assamese. | None. | Cite (TALLIP low-resource captioning lineage). |
| 11 | Image captioning in low resource Assamese with semantic information prior and spatially encoded transformer. P. Choudhury, S. Nair, P. Guha, S. Nandi | *ESWA* 2025-09. 10.1016/j.eswa.2025.129479 [title] | Same group; transformer captioner. | None. | Optional. |
| 12 | CaptionPS: Benchmarking Worker-Centric Detailed Image Captioning in Power Scenarios. Z. Wang et al. | *IEEE Access* 2026. 10.1109/ACCESS.2026.3685213 [abstract] | Domain detailed-caption dataset; SFT of several VLMs, best InternVL3.5-8B. | None. Shows that "SFT a suite of VLMs" counts as a journal contribution in 2026. | Optional. |
| 13 | VQA-LLM Fusion Caption Generator (VLFuseCap). F. A. Galatolo et al. | *JVCIR* 2026-10. 10.1016/j.jvcir.2026.104983 [abstract] | VQA answers fused by an LLM into detailed captions; GPT-4-generated training data. | **Low**: VQA→caption composition, but no verification, uncertainty or neutralization. | Should cite as contrast ("VQA answers composed without a verification gate"). |
| 14 | Attention-supervised transformer for grounded image captioning. X. Zhang, L. Chai, J. Huang | *Multimedia Systems* 2026-09. 10.1007/s00530-026-02684-1 [title] | Grounded captioning. | Low (C4 traceability context). | Optional. |
| 15 | KRCapVLM: Beam-guided knowledge replay for knowledge-rich captioning using VLM. R. Aljunaid et al. | *Pattern Recognition* 2026-11. 10.1016/j.patcog.2026.113568 [title] | VLM captioning with knowledge replay. | Low. | Watch. |
| 16 | TriFusion-RL: task verifiers, self-feedback and perceptual tools for VLMs. X. Wang | *CVIU* 2026. 10.1016/j.cviu.2026.104764 [title] | RL with verifiers and tools. | Low–medium (verifiers as reward, not as SFT gate); unverified details. | Fetch the abstract before submission. |
| 17 | Rewarding fine-grained image captioning with keyword group contrastive. K. Ye, Z. Lu, L. Shen, T. Cui | *ESWA* 2026. 10.1016/j.eswa.2026.131405 [title] | Fine-grained caption reward. | Low. | Watch. |
| 18 | Premise blindness in LVLMs: understanding and mitigating false-premise hallucination. B. Xu et al. | *Information Sciences* 2026/27. 10.1016/j.ins.2026.124045 [title] | False-premise hallucination. | Low (relevant to the negated-query probe in VSPS's dual polarity). | Read if the negated-query design is challenged. |
| 19 | Mitigating hallucinations in vision-language models through object-centric prompting (STAR). J. B. Ma, H. G. Han | *PRL* 2026-08. 10.1016/j.patrec.2026.08.013 [abstract] | Detector priors (labels, boxes, confidences) in the prompt, plus high-res crop verification for low-confidence regions. MME, POPE and CHAIR on Gemma-3 and Qwen-3.5-VL. | Low (inference time). **Technique-to-borrow**: crop-verify low-confidence regions (see d3). | Already listed in novelty/10. |
| 20 | Benchmarking Vietnamese image captioning: spatially-aware transformer and the HDUCap dataset. A. C. Hoang et al. | *JVCIR* 2026-09. 10.1016/j.jvcir.2026.104963 [title] | Newest Vietnamese captioning journal paper. | None on hallucination. | Must cite (newest Vietnamese captioning work). Already flagged in novelty/10. |
| 21 | A multimodal transformer-based architecture for Vietnamese image captioning focusing traffic scenes | *J. Sci. & Tech. HaUI* 2025-11. 10.57001/huih5804.2025.414 [title] | Vietnamese domain captioning. | None. Not Scopus Q1/Q2. | Optional. |

### a3. Experimental standard extracted from the full texts

| Paper (venue) | Backbones | Baselines | Benchmarks / metrics | Human eval | Seeds / variance | Significance test | Compute reported |
|---|---|---|---|---|---|---|---|
| HB (Sci. Rep. 2026) | 4 (LLaVA-1.5, InstructBLIP, MiniGPT-4, Shikra) | 7 (greedy, nucleus, beam-5, DoLa, VCD, DeCo, OPERA), run with the authors' recommended hyperparameters | POPE, CHAIR_S/I, AMBER | 200 COCO images, expert token-level annotation (for localisation) | **mean of 3 trials, sd ≤0.3 (POPE) / ≤0.5 (CHAIR)** | none found | partial |
| CLVA (PR 2026) | 3 (LLaVA-1.5, InstructBLIP, Qwen-VL) | 5 (greedy, beam, MemVR, ClearSight, IMCCD) | POPE, CHAIR_S/I + **Recall** | none found | none found | none found | **time + GPU memory overhead** |
| MHR (TOMM 2026) | 2 (LLaVA-1.5, CogVLM) | per-language base vs. MHR, plus ablations | POPE/MME/AMBER extended to 13 languages | none found | none found | none found | — |
| Metric-RL (IEEE Access 2026) | 1 main + 1 generalisation (InstructBLIP; mPLUG-Owl), 4 zero-shot LVLMs listed | mitigation baselines **copied** from the LURE paper | CHAIR + **Coverage** (COCO), CCEval (VG), BLEU/METEOR/SPICE/BERTScore | none | none | none | 8×A6000, ~1 day |
| Low-resource ML (Sci. Rep. 2026) | 9 VLMs × {zero-shot, LoRA, QLoRA} | the 9 models themselves | BLEU-1..4, ROUGE-L, METEOR, chrF, BERTScore, LASER, LaBSE | **200 test images × 3 raters, 5 criteria (Likert), κ**; dataset validation with Fleiss κ 0.76/0.79 | **3 seeds (42, 1337, 2024), mean + variance plot** | none found | 4×A100; peak memory 61 GB (LoRA) and 24 GB (QLoRA) |
| TALLIP captioning 2025 (#7–#10) [abstract] | 1 architecture family | earlier encoder-decoder captioners | BLEU-n, CIDEr, on 1–2 (often translated) datasets | qualitative examples | not stated | not stated | — |

**Bar for a 2026 Q1/Q2 hallucination-captioning paper** (median of the table above):
- **at least 2 backbones**;
- **at least 4 baselines**, including VCD and OPERA or DoLa, run by the authors rather than copied;
- **CHAIR + POPE**, and AMBER for "detailed" claims;
- recall or coverage next to CHAIR;
- **mean ± sd over 3 runs**;
- a **200-image human evaluation with 3 raters and κ** (expected for low-resource generation papers);
- **inference overhead** (time and VRAM).

Significance tests are rare in these journals. VSPS's paired bootstrap and Wilcoxon already **exceed** the norm.

---

## (b) Overlap risks (max 5)

1. **MHR (ACM TOMM 2026)**: medium, C5. It claims to be the first attempt at multilingual LVLM hallucination. Verified: its 13 languages exclude Vietnamese, and it evaluates QA-style benchmarks, not detailed captioning. Wording for VSPS: "first hallucination study of *Vietnamese detailed captioning*", contrasted with "multilingual POPE/AMBER-style QA (MHR)".
2. **Low-resource ML benchmark (Sci. Rep. 2026)**: low–medium. Same recipe (QLoRA Qwen2.5-VL-7B, low-resource captions), and it reports object hallucination as the main error. A reviewer may ask what VSPS adds over "just QLoRA". Answer: VSPS changes the *targets* (verified propositions) and measures hallucination with CHAIR instead of BLEU. Show that P2 (gold-caption SFT) is the "plain QLoRA" baseline and that it hallucinates more.
3. **Metric-Driven RL (IEEE Access 2026)**: low–medium, C1 contrast. Same task and metric (CHAIR + coverage), using a reward instead of verified SFT data. Cite it and keep the "no reward model, no RL loop" contrast.
4. **VLFuseCap (JVCIR 2026)**: low. It composes captions from VQA answers. Contrast: VSPS verifies typed propositions with dual-polarity voting and a third UNCERTAIN state before composing.
5. **Adjudicated Captioning (IEEE Access 2026, Vietnamese authors)**: low. A consensus verifier is used at inference. Contrast: in VSPS, verification is offline and the deployed model makes a single pass.

## (c) Must-compare baselines / must-cite (max 5)

1. **OPERA and DoLa**, alongside the VCD already run, as inference-time baselines on zero-shot Qwen2.5-VL-7B. Every 2026 decoding-side journal paper read here uses at least 3 of {VCD, OPERA, DoLa, DeCo}. Without them, "VSPS vs. decoding methods" rests on VCD alone.
2. **A second backbone.** Every hallucination paper above uses at least 2 (the median is 3). InternVL2.5-8B or Qwen2-VL-2B, SFT'd on the same `sft.jsonl`, would answer "is this specific to Qwen2.5-VL?". This is already plan item KE_HOACH_Q2 §105. These papers make it **required, not optional**.
3. **Cite the low-resource ML benchmark (Sci. Rep. 2026, 10.1038/s41598-026-70568-5)** for motivation, and **MHR (TOMM 2026)** for C5. Both are 2026 journal papers that a TALLIP reviewer is likely to know.
4. **Cite the TALLIP captioning lineage** (#7, #10, and optionally #8/#9) to show fit with the journal's scope. TALLIP has published no LVLM-hallucination captioning paper. Say this in the cover letter as the gap VSPS fills for TALLIP.
5. **Cite Metric-Driven RL (IEEE Access 2026)** as the closest 2026 journal paper on the same task, with CHAIR + coverage.

## (d) Actionable improvements, ranked by expected gain/cost

| Rank | Change | Where in the repo | Expected effect | GPU cost (1× RTX 3090) | Risk |
|---|---|---|---|---|---|
| 1 | **DoLa baseline.** `transformers` `generate()` takes `dola_layers="high"` natively for decoder LMs. Add a `--mode dola` branch beside `vcd_caption`. | `scripts/baselines.py` (beside `gen_greedy`/`vcd_caption`) | Closes the "only one decoding baseline" gap. DoLa usually changes CHAIR by about 1 point, so VSPS's margin should hold. No effect on VSPS itself. | ~1 GPU-h on KTVIC test, ~3 GPU-h on COCO-5000 | Low. Check that Qwen2.5-VL's text decoder accepts `dola_layers` in the installed transformers version. If not, implement the premature/mature layer contrast as in `vcd_caption`. |
| 2 | **Second backbone (InternVL2.5-8B or Qwen2-VL-2B), 3 seeds**, trained on the same `sft.jsonl`, with zero-shot and P2 (gold SFT) for the same backbone. | the stage-2 training entry point and `configs/main.env` (backbone id); `scripts/evaluate.py` unchanged | Meets the backbone norm. If VSPS lowers CHAIR on both backbones, the method claim generalises. Recall is bounded by the supervision (see memory: funnel), so expect a similar R/P profile. | ~3.6 h × 3 seeds ≈ 11 h for 7–8B (QLoRA); ~4 h total for 2B | Medium. InternVL chat-template and QLoRA target modules differ, and VRAM is tight at 8B. Qwen2-VL-2B is the safe fallback. |
| 3 | **OPERA baseline** (beam 5 with an over-trust penalty), using the official code adapted to Qwen2.5-VL, or reporting it only on the English COCO probe with LLaVA-1.5 if porting fails. | new mode in `scripts/baselines.py` | Expected by reviewers (the OPERA comparison appears in HB, CLVA and STAR). | ~4–6 GPU-h on KTVIC test at beam 5 (OPERA is ~5× slower than greedy) | Medium–high: the port to Qwen2.5-VL is non-trivial. The fallback is DeCo or ClearSight, which are lighter. |
| 4 | **Standard English benchmarks: CHAIR on COCO with an English prompt, the AMBER generative split (1,004 images) and POPE (3×3,000 questions)** for zero-shot vs. VSPS. Plan item B5. | `scripts/coco_probe.py`/`score_coco_probe.py`; add an AMBER scorer (official json and script) | Makes VSPS comparable with every number in the table above. A POPE gain is uncertain because VSPS trains captioning, not yes/no QA; report it honestly. | ~2–3 GPU-h | Low–medium (the POPE result may be flat). |
| 5 | **Error taxonomy in the human evaluation** (object / attribute / count / relation / gender / fluency error per caption) with Fleiss κ over 3 raters on 200 images, mirroring Sci. Rep. 2026 (#1). | `scripts/human_eval_sample.py`, `human_eval_score.py`, `agreement.py` (exist) | Turns the human evaluation into evidence of *where* hallucinations drop. This is also the strongest answer to "BLEU/CIDEr do not show it". | 0 GPU; ~3 rater-days | Low. Needs a third rater if only two exist. |
| 6 | **Mean ± sd for every row**, including the baselines (note that deterministic decoders have sd 0), plus the existing paired bootstrap (`score_ci.py`) with a Holm correction across CHAIR_i, CHAIR_s, P, R and F1. | `scripts/score_ci.py` (add `--holm`), table builder in `build_v10.py` | Matches HB and Sci. Rep. and exceeds the norm. Removes the "single run" objection. | 0 | None. |
| 7 | **Compute table**: Stage-1 GPU-h (~88 GPU-h; see the memory correction), SFT h, peak VRAM, per-image latency vs. VCD, DoLa and OPERA. | `scripts/measure_vram.py`, `scripts/measure_latency.py` (exist) | CLVA and Sci. Rep. report overhead. VSPS's zero inference overhead against decoding baselines becomes a visible win. | <1 GPU-h | None. |
| 8 | **Crop-verify (borrowed from STAR, PRL 2026)**: for UNCERTAIN entity propositions whose grounding box is small, re-query Vintern-1B on a 2× crop before final verdict. | `rescap/pipeline/verify.py` (UNCERTAIN path) | Turns some UNCERTAIN into SUPPORTED, so +recall at near-SUPPORTED precision on small objects. Expect +1–2 R, an estimate not yet measured. | Offline re-verification of UNCERTAIN entity props only, ~10–15 GPU-h for the train set | Medium: verifier precision may fall on crops, so audit 100 samples with `audit_three_state_sample.py` first. |

## (e) Watch queries (re-run monthly)

1. **OpenAlex** with these filters: `primary_location.source.id:S4306421405|S19610489|S137030581|S115173108|S414566|S13144211|S2485537415|S196734849,from_publication_date:<last-run>,title.search:hallucination`. These IDs cover TALLIP, TOMM, TMM, TCSVT, PR, ESWA, IEEE Access and Sci. Rep.
2. OpenAlex `title.search:image captioning` restricted to TALLIP (`S4306421405`) and to `title_and_abstract.search:Vietnamese caption`. This catches any Vietnamese or TALLIP competitor.
3. Crossref `https://api.crossref.org/works?query.bibliographic=object+hallucination+image+captioning&filter=type:journal-article,from-pub-date:<last-run>`. It indexes faster than OpenAlex.
4. arXiv listing for cs.CV + cs.CL with abstract terms `hallucination AND (caption OR captioning) AND (verified OR verification OR proposition OR claim) AND (SFT OR fine-tuning OR data)`. Journal versions usually appear there first.
5. Google Scholar alert: `"low-resource" "image captioning" "vision-language" hallucination 2026`.
6. Semantic Scholar: `multilingual hallucination vision-language captioning`, with `publicationTypes=JournalArticle` and `year=2026-`.

## Unverified

- Full texts of TALLIP #7–#10 (ACM 403). Their protocols are inferred from the abstracts only, so human evaluation and seeds are "not stated", not "absent".
- Abstracts elided by Elsevier for #11, #15, #16, #17, #18, and for the PR version of CLVA (its arXiv version was read). GLINT, CoSE and Pan et al. (ESWA 2026) remain title-only, as in novelty/10.
- CaptionPS: the IEEE PDF fetch returned only a 3-page fragment, so its protocol was not extracted.
- Whether `transformers` `dola_layers` works with Qwen2.5-VL's multimodal `generate()`; check this before relying on rank 1.
- No journal extension of HalluciDoctor, RLAIF-V or SENTINEL was found up to 2026-10-10 (OpenAlex and Crossref), the same result as novelty/10.
