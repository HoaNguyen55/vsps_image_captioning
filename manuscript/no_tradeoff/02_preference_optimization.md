# 02: Preference optimization and RL for hallucination with no recall loss

Scope: DPO/RL-style methods that report a precision-side metric and a recall/coverage-side metric together.
This extends `research_wall/01`, `07` and `novelty/08`, which already describe RLAIF-V, HSA-DPO, OPA-DPO, SENTINEL, CCCaption, ClaimDiff-RL, CapRL and REVERSE. Here I add only the precision-and-coverage numbers for those papers and new entries.
Numbers come from the arXiv HTML tables, opened on 2026-10-11. "Retest" means the numbers come from another paper's table. UNVERIFIED marks anything I could not confirm.

## 1. The pattern across the literature

Most preference methods lower AMBER CHAIR but also lower **AMBER Cover**. The papers attribute the Cover drop to the model "omitting ambiguous objects", which is the same failure VSPS has. Only a few methods hold or raise Cover. They share one mechanism: **the training signal penalizes only the hallucinated span, or it explicitly rewards correct additions.** A whole-response "less-hallucinated is better" preference does neither.

| Mechanism | Coverage outcome | Examples |
|---|---|---|
| Whole-response DPO, chosen = cleaner/shorter | Cover drops 2–4 pts | OPA-DPO, CHiP, HSA-DPO, RLHF-V, CSR-7B, FGAIF (length 216→60) |
| Phrase/token-local loss, rest of the response anchored | Cover held or up | HALVA, mDPO (LLaVA), HA-DPO-13B (retest) |
| Reward has an explicit recall/correct-addition term next to the hallucination penalty | Recall up, precision held vs SFT | SC-Captioner, BalCapRL, MOCHa |
| Coverage-only signal | Cover up, hallucination up | Self-Consistency paper, Table V ablation |

## 2. Methods with both sides measured

### 2.1 HALVA / DPA: data-augmented phrase-level alignment. **Pareto on all three models**
- P. Sarkar, S. Ebrahimi, A. Etemad, A. Beirami, S. Arik, T. Pfister. **ICLR 2025**. https://arxiv.org/abs/2405.18654, proceedings https://proceedings.iclr.cc/paper_files/paper/2025/hash/b73228d026ef49bfa49f95b7e330513e-Abstract-Conference.html, code https://github.com/pritamqu/HALVA (LoRA weights on HF `pritamqu/halva13b-lora`).
- How it works: a correct response is perturbed at the phrase level into a hallucinated one. The loss pushes down only the hallucinated phrase tokens relative to the correct ones. A token-wise divergence to the frozen reference keeps the rest of the generation distribution in place.
- Numbers, AMBER generative (Table 3), base → HALVA, CHAIR / Cover / Hal:
  - LLaVA-1.5-7B: 7.8/51.0/36.4 → **6.6/53.0/32.2**
  - LLaVA-1.5-13B: 6.6/51.9/30.5 → 6.4/52.6/30.4
  - VILA-1.5-13B: 9.9/63.3/56.1 → 9.1/63.9/54.2
- CHAIR (Table 1), C_i / C_s / Len: 7B 15.4/50.0/100.6 → 11.7/41.4/92.2.
- MMHal (Table 4), score / hallucination rate: 7B 2.11/0.54 → 2.25/0.54.
- Cost: LoRA on the LLM only, 4×A100-80GB, about 1.5–3 h, one epoch of 342 steps. A 7B LoRA with a reference forward fits a 3090 in 4-bit. In bf16 it is tight; the reference can be computed with the adapter disabled.
- **Trade-off check:** caption length falls by 8 words (100.6 → 92.2), but AMBER Cover rises, so the shorter captions still cover more objects. The gains on 13B are small.
- VSPS mapping: **training**. The verifier already labels each proposition SUPPORTED or REJECTED. Turn REJECTED propositions into phrase-level negatives inside otherwise-correct captions, so the "be less wordy" pressure never appears.

### 2.2 SC-Captioner: RL with a correctness bonus and a mistake punishment. **Recall up, precision held vs SFT**
- L. Zhang et al. **ICCV 2025**. https://arxiv.org/abs/2508.06125, poster https://iccv.thecvf.com/virtual/2025/poster/2454, code https://github.com/zl2048/SC-Captioner.
- Reward: scene-graph parse into object, attribute and relation sets. The model drafts a caption and then self-corrects it. Elements the correction adds or removes are checked against the reference. Correct changes earn a **bonus**, which makes this a recall term. Wrong ones are **punished**, which is the precision term. Precision and recall are both rewarded, F1-like, but as separate terms.
- Numbers, Qwen2-VL-7B on DOCCI500 (Table 1), object P / R / F1:
  - zero-shot: 83.69 / 56.79 / 66.47
  - SFT: 79.99 / 62.68 / 69.50
  - SFT+DPO: 79.86 / 64.85 / 70.77
  - **SFT+SC-Captioner (corrected): 80.20 / 66.00 / 71.63**
  - Attribute P/R/F1 69.54/50.34/57.67 vs SFT 68.85/47.57/55.50. CAPTURE 63.34 vs 62.05.
- COCO-LN500 (Table 2), object P/R/F1: zero-shot 81.12/61.82/69.47 → 78.72/75.01/76.37.
- Cost: LoRA through LLaMA-Factory on 8×A800. A 7B LoRA with 4-bit base on a 3090 is plausible, but rollouts are slow (estimate, not measured).
- **Trade-off check:** against **zero-shot**, object precision falls 3.5 pts (DOCCI) and 2.4 pts (COCO-LN), so it is not Pareto there. Against **SFT**, both object P and R rise. The paper says removing the mistake punishment makes precision "drop significantly" (Table 3, but the row mapping did not survive extraction).
- VSPS mapping: **training, after SFT**. This is the closest analogue to VSPS's situation: an SFT model that is more precise but recalls less. The bonus/punishment can be scored by the Vintern verifier instead of a reference parse; the 3-state logit verifier is already in the repo. This is the cleanest "F1 rather than precision" reward precedent.

### 2.3 mDPO: conditional preference plus anchored reward. **Pareto on LLaVA-7B only**
- F. Wang et al. **EMNLP 2024**. https://arxiv.org/abs/2406.11839, project page https://feiwang96.github.io/mDPO. A code link is not in the paper (UNVERIFIED whether the repo is public).
- How it works: on top of DPO, it adds an image-conditional preference (corrupted image = rejected) and an anchor that keeps the chosen reward positive, so the chosen likelihood is not driven down.
- Numbers (Table 1), AMBER CHAIR / Cover / Hal / Cog:
  - LLaVA-1.5-7B: 7.4/51.8/34.7/4.1 → **4.4/52.4/24.5/2.4**. Plain DPO gives 6.5/55.1/34.5/2.3.
  - Object HalBench CHAIR_s/CHAIR_i: 54.7/15.9 → 35.7/9.8. MMHal score 2.19 → 2.39.
- Cost: LoRA r=64; GPU not stated.
- **Trade-off check:** Bunny-3B Cover falls **75.6 → 67.4**, and even on 7B, Cover is lower than plain DPO's 55.1. The authors call the decrease "minor". The result is not robust across base models.
- VSPS mapping: **training**. Its anchor term addresses the DPO failure VSPS saw in v9 §IV-9, where chosen likelihood collapsed and hedges saturated.

### 2.4 BPO: bootstrapped preference optimization. **Cover up strongly, hallucination down slightly (retest)**
- R. Pi et al. **ECCV 2024**, doi:10.1007/978-3-031-73414-4_22, https://arxiv.org/abs/2403.08730. I did not open the paper's own tables.
- How it works: rejected responses are the model's own outputs, bootstrapped by distorting the image and by LLM-injected errors. Chosen responses are the annotations.
- Numbers, from the **HDPO retest** (arXiv 2411.10436, Table 1), LLaVA-1.5-7B base → BPO:
  - AMBER CHAIR 7.6 → 5.0, **Cover 51.8 → 58.8**, Hal 35.1 → 33.5, Cog 4.3 → 2.0
  - COCO CHAIR_s/CHAIR_i 51.2/14.2 → 42.2/10.1
  - POPE F1 86.1 → **83.1**
- **Trade-off check:** POPE F1 drops 3 pts, and Hal barely moves. The precision gain is modest relative to the recall gain.
- VSPS mapping: **training**. Use the model's own over-confident captions as negatives. The retest numbers need confirming against the BPO paper.

### 2.5 CSR: calibrated self-rewarding. **Length held on 13B, not 7B**
- Y. Zhou et al. **NeurIPS 2024**. https://arxiv.org/abs/2405.14622, code https://github.com/YiyangZhou/CSR.
- Reward: sentence-level beam scoring that mixes the model's own likelihood with a CLIP image–sentence relevance score, applied iteratively as DPO.
- Numbers (Table 7), CHAIR_s / CHAIR_i / average length:
  - 13B: 48.3/14.1/89.7 → iter-5 28.0/7.3/**102.4**
  - 7B: 48.8/14.9/89.0 → 18.3/5.4/82.1
- **Trade-off check:** in the HDPO retest, CSR-7B AMBER Cover falls **51.8 → 45.0**. Length is only a weak proxy for recall.
- **One A100-80GB, LoRA, 3.5 h for 7B**, which makes it the cheapest published setup. In 4-bit it should fit a 3090 (estimate).

### 2.6 Coverage-losing methods (cite as the trade-off the field accepts)

| Method (venue) | Link | Base → method, AMBER CHAIR / Cover (table) | Note |
|---|---|---|---|
| OPA-DPO (CVPR 2025) | arXiv 2501.09695, github.com/zhyang2226/OPA-DPO | 7B 7.7/51.6 → 2.2/**47.9**; 13B 6.8/51.9 → 2.4/48.3 (T2) | Paper says "slight compromise in Cover". LoRA r=256 |
| RLAIF-V (CVPR 2025, per brief) | arXiv 2405.17220, github.com/RLHF-V/RLAIF-V | 3.0/**50.4** vs base 7.7/51.6 (OPA-DPO T2 retest); ObjHal Resp 54.5 → 10.5 (own T1) | 8×A100; full FT. Own paper reports no coverage metric |
| CHiP (ICLR 2025) | arXiv 2501.16629, github.com/LVUGAI/CHiP | LLaVA-1.6-7B 8.3/61.0 → 3.7/**57.8**; Muffin 8.0/48.3 → 4.4/45.3 (T1) | Length unchanged (T6), so the Cover drop is omission. 4×H100 |
| HSA-DPO (AAAI 2025) | arXiv 2404.14233, github.com/Mr-Loevan/HSA-DPO | LLaVA-1.5 7.8/51.0 → 2.1/**47.3**; Qwen-VL 6.6/53.2 → 3.7/52.4 (T3) | Plain DPO on Qwen-VL kept Cover at 53.2. LoRA |
| SENTINEL (ICCV 2025) | arXiv 2507.12455, github.com/pspdada/SENTINEL | ObjHal Resp 52.7 → 4.3, AMBER CHAIR 8.4 → 2.9, Hal 35.5 → 14.6 (T1) | **Cover not reported**. MM-Vet 31.0 → 32.6 (T13). LoRA |
| RLHF-V (CVPR 2024) | arXiv 2312.00849, github.com/RLHF-V/RLHF-V | Cover **46.1** vs LLaVA-1.5 51.0 (HSA-DPO T3 retest). Own T1: MMHal informativeness 33.4 → 40.0, but LLaVA-Bench Detail 79.7 → 75.3 | Full FT, 8×A100 |
| HA-DPO (arXiv 2023) | arXiv 2311.16839 | SHR 36.7 → 34.0 (own T3). Retests disagree: 7B 7.7/51.6 → 7.8/52.1 (OPA-DPO T2); 13B 6.6/52.0 → 6.0/52.3 (HDPO T2) | Near-Pareto but tiny effect. MME-Cog 355.7 → 313.9 |
| POVID (arXiv 2024) | arXiv 2402.11411, github.com/YiyangZhou/POVID | CHAIR_s 66.8 → 31.8; LLaVA-Bench captioning 53.4 → 60.1 (T1/T4). Retest Cover 51.6 → 51.3 (OPA-DPO T2) | Roughly Cover-neutral, but its own CHAIR baseline (66.8) is unusually high. LoRA, 1×A100 |
| HDPO (arXiv 2024) | arXiv 2411.10436 | 7B 7.6/51.8 → 3.3/**50.2**; 13B 6.6/52.0 → 3.8/51.0 (T1/T2) | Smallest Cover loss among the strong reducers. LoRA |
| V-DPO (EMNLP 2024 Findings; venue UNVERIFIED this session) | arXiv 2411.02712, github.com/YuxiXie/V-DPO | 7.8/51.0 → 5.6/**49.7** (T3) | Full FT, 4×A100-40GB |
| FGAIF (OpenReview-reviewed, venue UNVERIFIED) | arXiv 2404.05046, github.com/LiqiangJing/FGAIF | CHAIR_s 22.0 → 6.2, **length 216 → 60.2** (T3); LLaVA-Bench Detail 75.4 → 93.6 | Sub-sentence object/attribute/relation rewards with PPO. The length collapse shows a precision-only reward |
| Self-Consistency/self-reflection (arXiv 2509.23236) | arXiv 2509.23236 | 7.8/51.0 → 2.0/50.2. Ablation (T5) ranking pairs by coverage: Cover **57.8** but Hal 25.9 vs 10.3 | Shows that a coverage-only preference brings hallucination back |
| P²-DPO (arXiv 2026, ICLR-26 style) | arXiv 2606.03376, github.com/ZrpChuang/P2-DPO | **Qwen2.5-VL-7B**: AMBER CHAIR_i 5.4 → 3.9, Hal 29.0 → 24.9 (T2) | Cover not reported, so no recall evidence |
| Re-Align (arXiv 2025) | arXiv 2502.13146 | POPE/HallusionBench only | No generative coverage metric |
| AMP (NeurIPS 2024, venue from memory) | arXiv 2405.11165, github.com/takomc/amp | MMHal 2.01 → 3.17; LLaVA-Bench Detail 75.9 → 89.1 (T1) | No CHAIR/Cover. The detail gain is GPT-judged |
| FDPO / M-HalDetect (AAAI 2024) | arXiv 2308.06394 | −41% hallucination (human eval) on InstructBLIP | No coverage metric |
| TPO/TPR (arXiv 2411.17265) | arXiv 2411.17265, tpr-dpo.github.io | ObjHal CH_s 53.6 → 4.0 (T1) | AMBER columns were garbled in extraction (UNVERIFIED). 8×A100, full FT |

### 2.7 "Less is more": counter-example of recall loss
- Z. Yue, L. Zhang, Q. Jin. "Less is More: Mitigating Multimodal Hallucination from an EOS Decision Perspective." **ACL 2024** (venue from memory; the arXiv page does not state it). https://arxiv.org/abs/2402.14545.
- Numbers (Table 1), Len / CHAIR_s / CHAIR_i / Recall:
  - LLaVA-1.5-7B: 100.6/50.0/15.4/77.1 → 76.2/36.8/11.3/**74.3**
  - LLaVA-7B: 57.8/35.4/13.8/64.8 → 39.9/27.0/13.2/**57.1**
  - The one non-loss: MiniGPT-v2 recall 66.3 → 66.6.
- The paper calls the recall loss "a beneficial compromise". It is the textbook statement of the trade-off that VSPS must not reproduce. VSPS's entity cap of 8 plus "drop UNCERTAIN" behaves like an early EOS.

## 3. RL rewards that score F1/coverage, not just hallucination

| Method | Reward terms | Evidence that the recall term matters |
|---|---|---|
| SC-Captioner (ICCV 2025) | correctness bonus (recall) + mistake punishment (precision) | Obj R 62.68 → 66.00 and P 79.99 → 80.20 vs SFT (T1) |
| BalCapRL (arXiv 2605.07394, no code found) | separate precision, recall and linguistic rewards, each GDPO-normalized | Without the recall reward, arena length falls 203 → 152 (T3). Qwen2.5-VL-3B: DCScore 43.3 → 50.8, CaptionQA 70.0 → 75.0 (T1). **No hallucination metric reported**. 8×B200, 46 h for 7B |
| MOCHa (arXiv 2312.03631, code github.com/assafbk/mocha_code) | NLI fidelity + BERTScore adequacy + KL, PPO | BLIP-L CIDEr 138.4 → 139.6 with CHAIR_i 2.3 → 2.1 (T6). Fidelity-only ablation: CIDEr 132.9, BERTScore 0.66 (T7). Small captioners only |
| Re³Cap (arXiv 2608.21305, code not released) | retrieval-guided keep/add/remove self-review | Qwen2-VL-7B object F1 69.47 → 78.18 vs GRPO 75.80 (T1). No P/R split, ~216 A100-h |
| ClaimDiff-RL, CuRe, CCCaption | hallucination and omission scored separately | Already in `novelty/08` and `research_wall/07`; not repeated |

Rule of thumb from these papers: **the precision term stops hallucination, and the recall term stops length/omission collapse. Either one alone fails** (FGAIF and EOS for precision only; Self-Consistency T5 for coverage only).

## 4. 1×RTX 3090 feasibility
- LoRA and one GPU are reported only by **CSR** (1×A100-80GB, 3.5 h) and **POVID** (1×A100-80GB). HALVA, mDPO, HSA-DPO, SENTINEL, OPA-DPO, HDPO, Re-Align and SC-Captioner use LoRA on 4–8 GPUs. CHiP, RLAIF-V, RLHF-V, V-DPO and TPR use full fine-tuning on multiple GPUs.
- For Qwen2.5-VL-7B on 24 GB: a 4-bit base plus LoRA, with the reference logits taken via `disable_adapter()`, is the only realistic option. That is the same QLoRA DPO setup that already failed in v9 §IV-9. A **phrase-local loss (HALVA)** or **anchored DPO (mDPO)** directly targets that failure, because neither pushes down the whole chosen sequence. GRPO with G=4 rollouts is overnight-scale; see `research_wall/07` for the estimate.

## 5. Mapping to VSPS
- **Training (post-SFT)**: SC-Captioner-style reward computed by Vintern. +1 for each new SUPPORTED entity the model adds beyond the SFT caption, −1 for each REJECTED one, 0 for UNCERTAIN. This targets recall loss (a) and (b) directly.
- **Training (SFT replacement or add-on)**: HALVA phrase-level negatives built from REJECTED propositions, with the KL/divergence keeping the rest. No length pressure.
- **Rendering/data**: the CHiP/OPA-DPO results show that "cleaner chosen = shorter chosen" causes the Cover drop. Keep the chosen captions at least as entity-rich as the zero-shot ones.

## Top picks for VSPS
1. **HALVA (ICLR 2025)**: AMBER CHAIR 7.8 → 6.6 **and** Cover 51.0 → 53.0 on LLaVA-1.5-7B, Pareto on all three models (Table 3). LoRA, phrase-local loss.
2. **SC-Captioner (ICCV 2025)**: correctness bonus plus mistake punishment. On Qwen2-VL-7B, object P 79.99 → 80.20 and R 62.68 → 66.00 vs SFT (Table 1). This is the F1-style reward that fits VSPS's SFT model, though it is −3.5 P vs zero-shot.
3. **mDPO (EMNLP 2024)**: AMBER CHAIR 7.4 → 4.4 with Cover 51.8 → 52.4 on LLaVA-7B (Table 1). Its anchor stops chosen-likelihood collapse, but Bunny-3B loses 8 Cover points.
4. **BPO (ECCV 2024)**: Cover 51.8 → 58.8 with AMBER CHAIR 7.6 → 5.0 (HDPO Table 1 retest; own table not checked). POPE F1 falls 86.1 → 83.1.
5. **Two-term reward design (BalCapRL / MOCHa)**: dropping the recall reward cuts length 203 → 152 (BalCapRL Table 3), and fidelity-only cuts CIDEr 139.6 → 132.9 (MOCHa Table 7). Use these as the ablation argument for an F1 reward over a precision-only one.
