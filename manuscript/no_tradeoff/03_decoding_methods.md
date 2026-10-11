# 03: Training-free decoding and inference-time methods: does recall survive?

Agent 03, written 2026-10-11. This report extends `research_wall/01_hallucination_mitigation_sota.md`, which already covers method descriptions, venues and Qwen2.5-VL code status. It adds the one thing 01 lacked: **for each method, whether the precision-side metric and the coverage-side metric move together**, i.e. AMBER CHAIR together with AMBER Cover, or CHAIR together with recall and length.

The numbers were pulled from arXiv HTML tables on 2026-10-11. They are not comparable across papers, because max tokens (64 vs 512), prompts and CHAIR implementations differ. Only compare rows within one table. "Derived" means I back-solved object recall from a table's CHAIR_i and CHAIR-F1 using R = F·P/(2P−F) with P = 1−CHAIR_i, which is the definition the source paper gives in its App. A.3.1.

## 0. Bottom line for VSPS

1. **No decoding method recovers recall at the scale VSPS lost it.** The VSPS gap is object recall 36.7 against 57.1 for zero-shot, about 20 points. The best Pareto-clean decoding results on Qwen2.5-VL-7B move AMBER Cover by +0.2 to +0.6 points (SIRA, MaskCD) or move CHAIR recall by +0.5 (ReWEIGH). Every method with a large Cover gain (VCD, OPERA, ReVisiT on Qwen2.5-VL) pays for it elsewhere: CHAIR worsens, or CHAIR recall falls. Decoding re-ranks tokens the model already finds plausible. It cannot restore the object mentions that SFT trained out of the distribution, such as the entity cap of 8 and the template brevity. Treat decoding as a **precision add-on on top of a recall fix made in the data or proposal stage**, not as the recall fix itself.
2. **Methods measured as Pareto on Qwen2.5-VL-7B itself**, where both sides are reported: SIRA (AMBER 5.3/47.2 → 4.6/47.8), MaskCD (→ 4.8/47.4) and ReWEIGH (CHAIR_s 31.6 → 25.4, derived recall 58.2 → 58.7, but AMBER Cover −1.2). ReVisiT is Pareto in its own paper (CHAIR_s 35.2 → 29.8, CHAIR-F1 79.85 → 81.16) but not in ReWEIGH's re-run.
3. **Methods that clearly lose coverage**: PAI, DeCo, LISA, DoLa (on Qwen2.5-VL), OPERA (CHAIR recall), HALC (only evaluated at 64 tokens), EOS-style methods, VGD at strict operating points, ICT and SID on Qwen2.5-VL (small losses).
4. **Already known in the repo**: our VCD barely moves KTVIC (v10 Table III: 31.9/55.9/40.6 vs 31.6/57.1/40.7). This matches every third-party Qwen2.5-VL table below, where VCD is inconsistent: Cover goes up in one table and down in another.

## 1. Qwen2.5-VL-7B tables with both sides measured (the most relevant evidence)

**T1. ReWEIGH Table 1** (arXiv:2608.19075; 500 COCO, "describe in detail", 512 tokens). The recall column is derived.

| Method | CHAIR_s | CHAIR_i | CHAIR-F1 | recall (derived) | AMBER CHAIR | Cover | Hal | Latency |
|---|---|---|---|---|---|---|---|---|
| Base | 31.60 | 9.58 | 70.80 | 58.2 | 4.52 | 55.80 | 20.32 | 1.00× |
| VCD | 33.80 | 9.65 | 70.27 | 57.5 | 5.43 | 63.30 | 26.99 | 2.03× |
| OPERA | 20.20 | 7.01 | 63.79 | **48.5** | 3.51 | 63.33 | 20.92 | 8.03× |
| DoLa | 23.60 | 16.76 | 60.32 | **47.3** | 4.47 | 51.71 | 18.92 | 1.25× |
| PAI | 26.20 | 9.61 | 66.98 | 53.2 | 4.25 | **49.47** | 18.03 | 2.04× |
| ReVisiT | 24.00 | 6.75 | 66.99 | 52.3 | 4.27 | 62.30 | 24.90 | 1.05× |
| ReWEIGH | 25.40 | 7.54 | **71.83** | **58.7** | 3.80 | 54.65 | 18.82 | 1.01× |

**T2. SIRA Table 2** (arXiv:2605.14621). The CHAIR columns are CHAIR_s and CHAIR_i at 512 tokens. Latency is from Table 4 at 128 tokens.

| Method | CS512 | CI512 | AMBER CHAIR | Cover | Hal | Cog |
|---|---|---|---|---|---|---|
| Base | 35.5 | 24.5 | 5.3 | 47.2 | 23.6 | 1.9 |
| DoLa | 35.9 | 24.6 | 5.5 | 46.8 | 25.1 | 2.2 |
| OPERA (5.9×) | 32.9 | 22.8 | 5.1 | **46.2** | 21.6 | 1.7 |
| VCD (2.1×) | 33.9 | 23.3 | 4.7 | **45.9** | 20.5 | 1.6 |
| ICT | 31.9 | 22.1 | 4.9 | **45.1** | 21.8 | 1.2 |
| MaskCD | 31.8 | 22.0 | 4.8 | 47.4 | 22.0 | 1.5 |
| SID | 33.0 | 22.8 | 4.9 | 46.3 | 21.5 | 1.4 |
| **SIRA (1.5×)** | 31.2 | 21.7 | **4.6** | **47.8** | 20.2 | 0.9 |

The same method changes sign across these two tables. VCD's Cover rises by 7.5 in T1 and falls by 1.3 in T2. OPERA's Cover rises by 7.5 in T1 and falls by 1.0 in T2. Any claim built on VCD or OPERA "preserving recall" on Qwen2.5-VL is therefore setup-dependent. SID, ICT, OPERA and VCD all lose 0.9 to 2.1 points of Cover in T2. Only SIRA and MaskCD hold Cover there.

## 2. Per-method cards

Venues follow 01, which verified them from the arXiv comment field or the proceedings. Venues I could not confirm are marked UNVERIFIED.

### Pareto evidence (both sides measured and both improve or hold)

**SIRA: Shared-Prefix Internal Reconstruction of Attribution.** T. Qin et al., arXiv 2026 (no venue, **no code found**). https://arxiv.org/abs/2605.14621
- Method: a counterfactual branch shares the early layers, then masks image attention in the late layers, and its logits are subtracted from the full branch. There is no second full forward pass.
- Evidence: Qwen2.5-VL-7B in T2. AMBER CHAIR 5.3 → 4.6, Cover 47.2 → 47.8, CS512 35.5 → 31.2.
- Cost: 1.4–1.5× (Table 4). Feasible on a 3090, since it needs only an attention-mask hook.
- VSPS stage: decoding of the SFT captioner.
- Trade-off check: none visible on AMBER. The paper reports no length numbers.

**ReWEIGH: Calibrating Token-Level Ordinal Visual Evidence.** arXiv 2026 (Aug), **no code in the text, so UNVERIFIED**. https://arxiv.org/abs/2608.19075
- Method: pools vocabulary ranks from visual-token readouts, then down-weights tokens whose image evidence falls below a per-token reference computed from unlabeled images.
- Evidence: Qwen2.5-VL-7B in T1. CHAIR_s 31.6 → 25.4, CHAIR-F1 70.80 → 71.83, derived recall 58.2 → 58.7, AMBER CHAIR 4.52 → 3.80.
- Cost: 1.01× (+1.3% with cached evidence, +2.4% online).
- VSPS stage: decoding.
- Trade-off check: **AMBER Cover 55.80 → 54.65 (−1.2)**, so it is not strictly Pareto on AMBER.

**ReVisiT: Revisit What You See.** B. Cho, J. Kim, ACL 2026 (long). https://arxiv.org/abs/2506.09522 , code at https://github.com/bscho333/ReVisiT (the paper evaluates Qwen2.5-VL-7B).
- Method: picks the vision token whose projected logits have minimum JSD to the current output distribution over a constrained vocabulary, then uses it to refine the logits.
- Own Table 3, Qwen2.5-VL-7B: CHAIR_s 35.2 → 29.8, CHAIR_i 8.43 → 7.04, CHAIR-F1 79.85 → 81.16 (VCD: 35.0/9.07/80.10).
- Cost: +0.6% latency on Qwen2.5-VL.
- Trade-off check: in the ReWEIGH re-run (T1), AMBER Cover rises to 62.3 and AMBER CHAIR falls to 4.27, but Hal rises to 24.9 and derived CHAIR recall falls to 52.3. The outcome is mixed and setup-dependent.

**MaskCD: Image-Head Masked Contrastive Decoding.** J. Deng et al., Findings EMNLP 2025. https://arxiv.org/abs/2510.02790 , code at https://github.com/Deng-Jingyuan/MaskCD
- Evidence on Qwen2.5-VL (SIRA re-run, T2): AMBER 5.3/47.2 → 4.8/47.4, which is Pareto.
- Own Table 6, LLaVA-1.5: CHAIR 9.2 → 8.7, Cover 41.3 → 48.6, but **Hal 29.2 → 34.5 (worse)**.
- Cost: 2 passes, about 2×, plus offline head discovery.
- VSPS stage: a drop-in replacement for the amateur branch in our existing VCD loop (`scripts/baselines.py`).

**MemVR: Memory-Space Visual Retracing.** X. Zou et al., ICML 2025. https://arxiv.org/abs/2410.03577 , code at https://github.com/1zhou-Wang/MemVR
- Table 3, LLaVA-1.5: CHAIR_s 50.0 → 46.6, CHAIR_i 15.4 → 13.0, **Recall 77.1 → 80.8**, Len 100.6 → 99.6. VCD scores 48.6/14.9/77.3 and OPERA scores 47.8/14.6/76.8.
- Cost: Table 1, 1.04× ms/token and 1.01× memory. VCD is 2.20× and OPERA 3.66×.
- Trade-off check: in App. Table A5, recall falls for **Qwen-VL (53.4 → 52.3)** and **GLM-4V-9B (72.7 → 70.7)**, and length shrinks for all three models. So the recall gain shows up only on LLaVA. The released code covers Qwen-VL v1, not Qwen2.5-VL.

**SID: Self-Introspective Decoding.** F. Huo et al., ICLR 2025. https://arxiv.org/abs/2408.02032 , code at https://github.com/huofushuo/SID
- In VGD's re-run (arXiv:2607.27823 Table 1, LLaVA-1.5): AMBER CHAIR 7.8 → 5.4, **Cover 51.0 → 52.6**, CHAIR_s 50.0 → 48.2, Len 101.2 → 95.8. That is Pareto on AMBER.
- Own Table 3 reports only CHAIR_s and CHAIR_i, for example LLaVA greedy 49.6/14.4 → 44.2/12.2.
- Cost: own Table 6 (POPE) gives 704 s against 494 s for the plain pass (about 1.4×), with VCD at 904 s.
- Trade-off check: **on Qwen2.5-VL (T2), Cover 47.2 → 46.3**. Length is down about 5% on LLaVA.

**AGLA: Assembly of Global and Local Attention.** W. An et al., CVPR 2025. https://arxiv.org/abs/2406.12718 , code at https://github.com/Lackel/AGLA
- Table 3: LLaVA-1.5 CS/CI/Recall 51.0/15.2/75.2 → 43.0/14.1/**78.9**, and InstructBLIP 54.0/18.1/71.1 → 49.0/12.1/72.5.
- Cost: Table A9, 0.69 s/sample against 0.56 s for VCD and 1.64 s for OPERA. The authors ran 7B on **one RTX 3090**. It needs BLIP-ITM for the local view.
- Trade-off check: no length or AMBER reported. No Qwen path exists. The local view is built from prompt-relevant regions, which for a captioning prompt is weakly defined.

**M3ID** (CVPR 2024, arXiv:2403.14003), as re-run in CAAC (arXiv:2505.21472 Table 2, AMBER, LLaVA-1.5):
- Average over 64 and 512 tokens: CHAIR 9.6 → 6.6, **Cover 47.5 → 53.1**, Hal 39.5 → 33.7. That is Pareto, and it is the largest Cover gain at a lower CHAIR anywhere in this survey.
- InstructBLIP: CHAIR 11.2 → 8.7, Cover 49.6 → 49.5 (flat).
- LLaVA-NeXT: CHAIR **worsens** (7.9 → 10.0).
- Cost: 2×. It is trivial to add to our step loop as a text-only amateur.

**VTI: Visual-Textual Intervention.** S. Liu, H. Ye, J. Zou, ICLR 2025. https://arxiv.org/abs/2410.15778 , code at https://github.com/shengliu66/VTI
- Table 2, LLaVA-1.5: CS/CI 51.0/15.2 → 35.8/11.1, **Recall 75.2 → 76.8**, but **Len 102.2 → 93.8**.
- Table 2, InstructBLIP: **Recall 71.1 → 70.1**, Len 115.3 → 105.8.
- Cost: about 1.0×, using fixed steering vectors in forward hooks.
- Trade-off check: shorter outputs. A follow-up (EMNLP 2025, found in search, UNVERIFIED) reports that VTI significantly reduces Cover on LLaVA-1.5.

**CAAC: Confidence-Aware Attention Calibration.** arXiv 2025, code at https://github.com/mehrdadfazli/CAAC
- Table 2, AMBER average: LLaVA-1.5 CHAIR 9.6 → 5.5 with Cover 47.5 → 47.6 (flat). InstructBLIP 11.2 → 6.1 with Cover 49.6 → 50.1.
- Cost: the second pass fires on 14% of tokens.
- No Qwen results.

**SAGE: Sink-Aware Grounded Decoding.** arXiv 2026, no code found.
- Table 2, AMBER CHAIR_i/Cover for Qwen2-VL-7B: 6.1/61.5, against OPERA 8.8/52.4 and HALC 7.8/54.7.
- No vanilla row is given, so the Pareto claim relative to the base model is **unverifiable**. The relative-gain labels in the paper do not match its own numbers. Overhead is +10.8%.

### Coverage losers (flag)

| Method (venue) | Evidence of the coverage loss |
|---|---|
| **PAI** (ECCV 2024) | Qwen2.5-VL Cover 55.8 → 49.5, derived recall 58.2 → 53.2 (T1). LLaVA Cover 50.47 → 43.11 (ReWEIGH Table 1). Own paper has no recall; GPT-4V detail stays flat (LLaVA 5.24 → 5.36) |
| **DeCo** (ICLR 2025, https://github.com/zjunlp/DeCo) | Own Table 7, AMBER LLaVA-1.5 greedy: CHAIR 8.2 → 6.6, **Cover 48.9 → 47.5**. Beam: 50.7 → 46.8. Latency 1.2× |
| **LISA** (arXiv 2025) | Table 3, AMBER LLaVA beam: Cover 50.7 → 45.6 (−5.1) |
| **DoLa** (ICLR 2024) | Qwen2.5-VL: CHAIR_i 9.58 → 16.76, derived recall → 47.3 (T1). Cover 47.2 → 46.8 (T2) |
| **OPERA** (CVPR 2024) | Qwen2.5-VL derived CHAIR recall 58.2 → 48.5 (T1), Cover −1.0 (T2). Latency 5.9–8×. Excluded on cost alone |
| **HALC** (ICML 2024) | Own Table 1 uses only 64 tokens and reports BLEU, no recall. ONLY Table 5 gives latency 6.52× |
| **VGD** (arXiv 2026) | Qwen2-VL-7B: AMBER CHAIR 7.4 → 1.9 but **Cover 68.4 → 55.6** at @rec90, even though length is unchanged (86) |
| **EOS / REVERSE strict / OWL** | VGD Table 1, LLaVA: OWL Cover 51.0 → 34.9 with Len 69.4. REVERSE τ=0.0003 Cover → 26.9 |
| **ICT** (CVPR 2025, UNVERIFIED) | Qwen2.5-VL Cover 47.2 → 45.1 (T2) |
| **VCD** (CVPR 2024) | Qwen2.5-VL: Cover +7.5 but CHAIR worse in T1, Cover −1.3 in T2. Our own KTVIC run shows recall 57.1 → 55.9 |

### Not verifiable on the recall side

- **ICD** (Findings ACL 2024): InstructBLIP CHAIR_s 21.4 → 14.4, with no recall or length reported.
- **IBD** (arXiv 2402.18476, venue UNVERIFIED): needs a trained prompt of 68–74K parameters, so it is not training-free. CHAIR LLaVA 20.6/6.2 → 12.7/4.5; GPT-4V detail rises from 5.2 to 5.5 against beam search. No recall reported.
- **CODE** (arXiv 2406.01920; NeurIPS 2024 is UNVERIFIED): only MMHal is reported. Latency 272.9 ms/token against 178 for VCD on a 7B model.
- **Nullu** (CVPR 2025): 64-token CHAIR plus BLEU only. LLaVA-Bench detail 5.02 → 5.59. It is a weight edit with 1.0× cost.
- **ClearSight/VAF** (arXiv 2503.13107): POPE, MME and NoCaps only, at 1.0× latency.
- **VISTA** (ICML 2025): CHAIR only (LLaVA greedy 46.4 → 20.4). The large CHAIR_s drop and 1.27× latency suggest shortening, but that is **unverified**.
- **ONLY** (ICCV 2025): CHAIR only, at 1.07×.

## 3. Applicability on top of the LoRA-finetuned Qwen2.5-VL-7B

The LoRA adapter merges into the base weights, so every hook-based method applies unchanged. The weight-edit methods (Nullu, QK steering) would have to be recomputed on the merged weights. Memory is not the constraint: everything except OPERA and HALC stays within about 1.05× of the bf16 7B footprint (about 16 GB), which fits a 3090.

| Method | Qwen2.5-VL code? | Effort in our loop | Latency | Expected effect on the SFT model |
|---|---|---|---|---|
| ReVisiT | Yes (paper evaluates Qwen2.5-VL-7B) | Low (clone) | 1.006× | CHAIR down. Recall direction unclear (+F1 in own paper, −recall in T1) |
| SIRA | No code | Medium (attention mask on late layers + logit subtraction) | 1.5× | Small Pareto: −0.7 AMBER CHAIR, +0.6 Cover |
| MaskCD | Code exists, no Qwen2.5 path | Low (swap the VCD amateur) | about 2× | Small Pareto on Qwen2.5-VL (T2) |
| M3ID | Trivial | Very low (text-only amateur in the existing loop) | 2× | Largest Cover gain, but only on LLaVA. Untested on Qwen2.5 |
| MemVR | Qwen-VL v1 only | Medium (FFN re-injection hook) | 1.04× | Recall ±1. Recall fell on non-LLaVA models |
| ReWEIGH | No code | Medium-high (needs an unlabeled-image calibration set, which KTVIC train provides) | 1.01× | Best CHAIR-F1 on Qwen2.5-VL, Cover −1.2 |

One structural caveat matters more than any single number. All of these methods redistribute probability among tokens at each step. They do not change when the model emits EOS or how many objects it decides to list. The VSPS model's recall loss comes from SFT targets that were capped at 8 entities and rendered tersely, and the model has learned that brevity. So expect at most a ±1–2 point recall change from decoding. The recall fix has to come from the targets (see 03_grounding_for_recall and the proposal and verification threshold notes). Once recall is restored there, a cheap Pareto-safe decoder (ReVisiT at about 1.0× or SIRA at 1.5×) can be stacked on top to pull precision back. Run every decoder with greedy as the reference: the Rethinking-CD finding in 01 (A20) is that greedy already beats most contrastive decoding methods on Qwen2.5-VL.

## Top picks for VSPS

1. **ReVisiT** (ACL 2026, code, Qwen2.5-VL-7B native, 1.006× latency): CHAIR_s 35.2 → 29.8 and CHAIR-F1 79.85 → 81.16 on Qwen2.5-VL-7B (own Table 3). AMBER re-run Cover 55.8 → 62.3 at AMBER CHAIR 4.52 → 4.27.
2. **SIRA** (arXiv 2026, no code, 1.5×): the only fully Pareto row on Qwen2.5-VL-7B AMBER, 5.3/47.2 → 4.6/47.8 (CHAIR/Cover, Table 2).
3. **ReWEIGH** (arXiv 2026, no code, 1.01×): Qwen2.5-VL-7B CHAIR_s 31.6 → 25.4 with CHAIR-F1 70.8 → 71.8 (derived recall 58.2 → 58.7). AMBER Cover falls 1.2.
4. **MaskCD / M3ID in the existing VCD loop** (about 2×, near-zero effort): MaskCD 5.3/47.2 → 4.8/47.4 on Qwen2.5-VL (SIRA Table 2). M3ID AMBER 9.6/47.5 → 6.6/53.1 on LLaVA (CAAC Table 2).
5. **MemVR** (ICML 2025, code, 1.04×): LLaVA CHAIR_s 50.0 → 46.6 with Recall 77.1 → 80.8 (Table 3), but recall falls on Qwen-VL and GLM-4V (Table A5). Use only as a low-cost ablation.
