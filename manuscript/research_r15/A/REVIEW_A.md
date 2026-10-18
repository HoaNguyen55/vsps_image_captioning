# R15-A: Literature review for Paper A (measurement validity of object-hallucination metrics)

Date: 2026-10-18. Window: 2017 to Oct 2026, weighted to 2024-2026. 70 papers, listed with metadata in `papers_A.json`.

## Method

- Every entry was resolved on its arXiv abs page (https://arxiv.org/abs/ID), with requests spaced 3.5 s apart. Title, authors, first-version date, comment and journal-ref were taken from the page. The export.arxiv.org API returned 429/503 and was not used.
- Venue: from the arXiv comment or journal-ref. Where neither gives one, the entry says "arXiv preprint". Venues were **not** re-checked on the venue page. One venue (Sun et al., 2309.14525) is from memory and is marked UNVERIFIED in the JSON.
- `year` is the year of the first arXiv version. The venue year can be later (for example MARINE 2402.08680 appeared at ICML 2025).
- Overlap with existing notes: 22 entries are already cited in `journal_draft/sec2_related_work.md` or `research_r13/R13_LIT_UPDATE.md`. They are kept so that each theme reads on its own, and are marked (S2) or (R13) below. The other 48 are new to the manuscript.
- Non-arXiv precedents already in sec2 are not repeated here: Sun et al. 2019 (W19-2303), LeHaCE (NeurIPS 2024), Lipton et al. 2014, Buckley and Voorhees 2004, and Saunders and Freitas 2022.
- Claims about paper content come from the abstract on the abs page and from earlier R11-R13 reading. No PDFs were downloaded. Check each claim against the PDF before citing it.

## T1. Object-hallucination metrics and benchmarks (21)

**Caption-level, gold-referenced metrics.**
- CHAIR (Rohrbach et al., EMNLP 2018; 1809.02156) is the origin of the field. It matches mentions to the COCO-80 synonym lists and scores them against instance labels plus reference captions.
- Every later caption metric keeps this precision-type core:
  - AMBER (2311.07397, S2) adds a coverage term.
  - THRONE (CVPR 2024; 2405.05256, S2) moves to class-wise P/R/F0.5 with LM-based judging of free-form text.
  - ALOHa (NAACL 2024; 2404.02904, S2) and OpenCHAIR (Ben-Kish et al.; 2312.03631) extend the vocabulary beyond COCO-80, using LLM extraction and open-vocabulary matching.
- In all of these, the gold set fixes what can count as a hallucination, so gold incompleteness enters the score directly.

**Probing (discriminative) benchmarks.**
- POPE (EMNLP 2023; 2305.10355, S2) replaced free-form scoring with yes/no existence questions. The authors motivated the change partly by CHAIR's dependence on instruction and caption length.
- Descendants vary the probe:
  - CIEM (2309.02301)
  - NOPE, with negative-presence questions (ALVR @ ACL 2024; 2310.05338)
  - BEAF, with before/after image edits (ECCV 2024; 2407.13442)
  - AutoHallusion, with synthetic edits (2406.10900)
  - HallusionBench, on entangled language-prior and visual illusions (CVPR 2024; 2310.14566)
- Probing removes the verbosity channel by construction. It also stops measuring what a model chooses to say, which is the quantity that caption metrics and preference data act on.

**LLM- or judge-scored benchmarks.**
- Benchmarks that use a judge or a learned evaluator:
  - HaELM (2308.15126)
  - Hal-Eval (ACM MM 2024; 2402.15721)
  - FaithScore (Findings of EMNLP 2024; 2311.01477), which decomposes answers into atomic facts
  - MMHal-Bench from LLaVA-RLHF (2309.14525)
  - GAVIE from LRV-Instruction (ICLR 2024; 2306.14565)
  - M-HalDetect (AAAI 2024; 2308.06394)
  - UniHD (ACL 2024; 2402.03190)
- These move the gold into a judge model. That makes completeness implicit rather than absent.

**Surveys.** Liu et al. (2402.00253) and Bai et al. (2404.18930) catalogue these metrics. Neither treats the number of mentioned objects as a confound to be controlled.

## T2. Length, count and conservative generation as confounds (14)

**Early analyses.**
- Biten et al. (WACV 2022; 2110.01705) and Dai et al. (EACL 2023; 2210.07688) tied object hallucination to co-occurrence priors and training objectives.
- LURE (ICLR 2024; 2310.00754) showed that hallucinations concentrate late in the caption. This makes position, and so length, a mechanism and not only a nuisance.
- M3ID (CVPR 2024; 2403.14003) reports that reliance on the visual signal decays as generation proceeds.
- Petryk et al. (2305.07021) use token confidence to trade correctness against content.

**Mitigation methods whose gains interact with length.**
- Decoding-time methods report CHAIR at a fixed max-token budget, not at a fixed object count:
  - VCD (2311.16922)
  - OPERA (CVPR 2024; 2311.17911)
  - MARINE (ICML 2025; 2402.08680)
- Woodpecker (2310.16045) is a post-hoc corrector and can delete content.
- Some methods say outright that they work by shortening:
  - "Less is More" (ACL 2024; 2402.14545, S2) encourages EOS and accepts the recall loss.
  - SumGD (Findings of NAACL 2025; 2410.13321, S2) notes that shorter captions lower CHAIR.

**2026 re-evaluations: the closest framing threat.**
- Fazli et al. (2609.01888, R13) re-evaluate 6 mitigation methods on 3 LVLMs and 4 benchmarks. They find that lower hallucination usually comes with lower recall or detail.
- Sandhu et al. (2608.24966, R13) study attention heads behind object hallucination in LLaVA and evaluate their own intervention under fixed token budgets (a token-budget control, not an object-count control).
- Long et al. (2609.35294, R13) name the "saying less" shortcut in RL alignment and counter it with dense presence/absence annotation.
- All three control length in tokens or report recall next to precision. None matches the number of mentioned objects per image, gives a sign condition indexed by gold completeness, or decomposes the effect.

## T3. Gold and reference completeness (5)

**In detection.**
- LVIS (CVPR 2019; 1908.03195) built incompleteness into the protocol: federated, non-exhaustive labels with explicit "not exhaustively annotated" flags. This is the clearest precedent for scoring under declared incompleteness.
- COCO-ReM (Singh et al.; 2403.18819) and Penquitt et al. (2609.21822, R13) re-annotate COCO and find many missing objects. COCO-ReM reports that model rankings change under the corrected labels; Penquitt et al. report largely stable rankings.

**In LVLM probing.** RePOPE (2504.15707, S2) shows that annotation errors in POPE's COCO-derived labels change model rankings.

**Theory.** The positive-unlabeled survey (Bekker and Davis, Machine Learning 2020; 1811.04820) formalises when metrics are estimable under missing positives (SCAR and related assumptions). This is the lens behind Paper A's argument that a verbosity effect SCAR cannot produce must come from somewhere else.

**Gap.** Detection-side work studies boxes. LVLM-side work studies yes/no labels. Neither studies how a caption metric's verdict on verbosity changes as the gold used to score free-form object mentions becomes more complete.

## T4. Meta-evaluation of caption metrics against human judgments (19)

**Classic short-caption judgments.**
- THumB 1.0 (NAACL 2022; 2111.08940, S2) gives expert precision and recall ratings.
- Polos/Polaris (CVPR 2024; 2402.18091, S2) gives 131K judgments.
- Reference-free and learned metrics are validated mainly by correlation with such sets:
  - CLIPScore (EMNLP 2021; 2104.08718)
  - PAC-S (CVPR 2023; 2303.12112)
  - InfoMetIC (ACL 2023; 2305.06002)
  - CLAIR (EMNLP 2023; 2310.12971)
  - FLEUR (ACL 2024; 2406.06004)
- Berger et al. (TACL 2025; 2408.04909, S2) survey these metrics and how they are validated.

**Detailed and long captions (2024-2026).**
- Datasets:
  - DOCCI (2404.19753)
  - ImageInWords (2405.02793)
  - DOCCI-Critique (2506.07631, S2)
- Metrics and benchmarks that separate a precision-like axis from a coverage-like axis:
  - CAPTURE (Dong et al.; 2405.19092)
  - DCScore/DeCapBench (ICLR 2025; 2503.07906)
  - CapMAS (ICML 2025; 2412.15484, S2)
  - CAPability (NeurIPS 2025 D&B; 2502.14914, S2)
- Human preference arenas:
  - CapArena (Findings of ACL 2025; 2503.12329, S2/R13) finds that output length alone agrees with humans at the caption level but not at the model level.
  - VELA/LongCap-Arena (EMNLP 2025; 2509.25818, S2/R13) gives 32K judgments of descriptiveness and relevance.

**Judges as evaluators.** MLLM-as-a-Judge (ICML 2024; 2402.04788) and LLaVA-Critic (CVPR 2025; 2410.02712) document how well multimodal judges agree with humans and how they are biased.

**Gap.** These sets validate whole metrics against humans. They do not ask whether the agreement survives once object count is matched, and so they cannot tell whether humans reward correct selection or simply reward more or fewer objects. Paper A §8 (LongCap-Arena MIXED; humans penalise count, but count-matched precision does not track humans better) sits exactly here. It should be framed as a conditional analysis on these released sets, not as a new benchmark.

## T5. Length and count bias in preference data and judges (11)

**Text-LLM precedent.**
- Singhal et al. (COLM 2024; 2310.03716) show that much of RLHF's measured gain is explained by length.
- Length-controlled AlpacaEval (COLM 2024; 2404.04475) regresses length out of judge win rates.
- Park et al. (2403.19159) add a length penalty to DPO.
- Together these establish length as a channel. Their remedies condition on token length.

**LVLM preference data and hallucination-aware DPO.**
- Datasets and methods:
  - RLHF-V (CVPR 2024; 2312.00849)
  - RLAIF-V (2405.17220)
  - POVID (2402.11411)
  - HA-DPO (2311.16839)
  - BPO (2403.08730)
  - mDPO (EMNLP 2024; 2406.11839)
  - HDPO (2411.10436, R13)
  - VaPR (COLM 2025; 2510.01700, R13)
- They build chosen/rejected pairs in which the rejected side is often a hallucinated rewrite or an over-long response.
- HDPO and VaPR explicitly match length or style. None reports the difference in the number of mentioned objects between chosen and rejected responses as a separate channel.

**Gap.** Paper A §9 audits a count channel in released preference sets, with VaPR as the positive control (PASS). The literature has the length channel; the per-pair count difference is not reported in any audited set we found.

## Gaps Paper A addresses (no priority claims)

1. **A per-image count control.** Prior controls fix tokens (Sandhu et al.; decoding papers), fit a length curve (LeHaCE), or report recall next to precision (Fazli et al.; AMBER; THRONE). Paper A compares systems at an exactly matched number of mentioned objects per image, with paired, image-clustered intervals and a decomposition.
2. **Sign of the verbosity effect as a function of gold completeness.** Detection re-annotation (COCO-ReM; Penquitt et al.) and RePOPE show that score levels and rankings move as the gold changes. Paper A states and tests when the sign of the verbosity effect on object P/R/F1 flips as the gold grows, building on Lipton et al.'s F1-threshold result and the PU/SCAR framework (Bekker and Davis).
3. **Human agreement conditional on count.** CapArena, LongCap-Arena, THumB and Polaris validate metrics unconditionally. Paper A asks whether agreement holds within count-matched pairs, and reports a MIXED result honestly.
4. **A count channel in preference data.** The length channel is known (Singhal et al.; Park et al.; HDPO; VaPR). Paper A measures the object-count difference within pairs in released LVLM preference sets.
5. **A reporting standard.** The field reports CHAIR and POPE without the matching unit or the gold level. Paper A's two-column standard follows sacreBLEU and SacreEOS: it fixes what is reported and leaves the metrics unchanged.

## Framing risks

- Fazli et al. (2609.01888) and Sandhu et al. (2608.24966) already argue that mitigation gains are partly conservative generation. Cite them in §1 as the source of the concern. Paper A's contribution is the count-matched quantification and the gold-indexed theory.
- The length channel in preference data is established (T5). Claim only the count channel, and the finding that matching on length does not remove it, if the data support that.
- Penquitt et al. find rankings "largely stable" under more complete detection gold. Contrast this explicitly with any ranking change Paper A reports for captions.

## Open items

- Venues for CIEM, HaELM, OpenCHAIR, AutoHallusion, CAPTURE, DOCCI, ImageInWords, COCO-ReM, RLAIF-V, POVID, HA-DPO, BPO, Park et al., HDPO, Fazli et al., Long et al., Penquitt et al.: none was found on the abs page, so they are listed as "arXiv preprint". Check the venue pages before camera-ready.
- Sun et al. (2309.14525) is listed with a venue from memory, marked UNVERIFIED.
- Content claims above are taken from abstracts. Confirm each one in the PDF before citing it.
