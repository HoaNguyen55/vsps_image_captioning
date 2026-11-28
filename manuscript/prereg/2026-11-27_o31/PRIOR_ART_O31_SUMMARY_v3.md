# Prior-art summary for O31, v3 (2026-11-28; replaces v2 05419ded)

## What changed in how the table was made
- **Full texts.** The seven closest works were read in full in the dissections (`dissect_<arxiv id>.txt`; sources and shas in `fetch_log.tsv`): 2609.35294, 2605.20278, 2503.07906, 2402.09801, 2507.12455, 2311.13614 and 2503.02846. Every cell used in the corrected novelty statement was checked again against the saved text, and the check corrected one of the dissections: HalluciDoctor App. B.2 Table 5 has five thresholds, not three.
- **Missing works.** The nine works that the adversarial review found missing were added with venue and year only where `PRIOR_WORK_CHECK.tsv` marks them verified. Their full texts have not been read; each row says "not read". The arXiv preprint of MHR is verified, but its later venue is not.
- **Other venues.** Venues that no record in this session verifies are now marked "unverified".
- **Settings not read verbatim.** Settings of VCD, DeCo, EFUF's code and the SENTINEL release were read on the projects' public pages, partly not verbatim, and are marked so. SENTINEL's detector thresholds could not be read (HTTP 503).
- **No new searches** were run for v3.

## Verdicts per idea (v3)

| Idea | Status | Closest work and the decisive cell |
|---|---|---|
| Cut hallucination without "saying less" in detailed captions | **TAKEN for coverage under RL; OPEN in absolute counts** | Beyond Saying Less Tab. 2: Cover 64.3 → 73.7, but hallucinated objects per gold object flat (0.1144 → 0.1140, derived); ClaimDiff-RL; MOCHa (trade-off framing); FeedQuill; BalCapRL |
| Fine-tune on verified or filtered model-written captions | **PARTLY TAKEN** | HalluciDoctor (SFT after deletion; RTX 3090); SENTINEL (DPO on detector-verified own sentences, also on Qwen2.5-VL-7B, App. E Tab. 19); Less is More (data filtering); FAIR 2026 (ours) |
| Verifier operating point → student behaviour | **TAKEN as a general claim** | HalluciDoctor App. B.2 Tab. 5 (five thresholds → SFT students, CHAIR and MME); SENTINEL Tab. 8–9 (detector choice, uncertain handling; DPO); ClaimDiff-RL Tab. 3 (three severity weights; RL) |
| Supervision density → student coverage | **TAKEN at two points under RL** | Beyond Saying Less Tab. 2 (COCO labels vs DOPA labels) |
| Three-state verdict with an unused uncertain band | **PARTLY TAKEN; a design detail** | EFUF (the 23–32 CLIP band); SENTINEL (detector disagreement ignored, Tab. 9) |
| Cross-family open-VLM verifier | **PARTLY TAKEN; a design detail** | FeedQuill (open-VLM ensemble; rule and versions not reported) |
| Per-span roles: mask the uncertain, unlearn the refuted (D2) | **PARTLY TAKEN** | EFUF; Mask-DPO; SCAPO subsentence credit |
| Count-matched preference pairs (D3) | **PARTLY TAKEN in its parts** | HSA-DPO; Mask-DPO; SENTINEL; deferred (Table 2) |
| A registered pre-SFT gate on supervision coverage | **Not a contribution** (research process; F04 (c)) | kept in the method section only |
| Mitigation with no inference cost | **PARTLY TAKEN** | Nullu (weight editing); HALVA (phrase-level alignment); EFUF |
| Non-English training-time hallucination mitigation | **PARTLY TAKEN** | MHR (13 languages; arXiv 2408.00550, venue unverified) |
| Vietnamese captioning with hallucination-aware fine-tuning | **NEW apart from our own FAIR 2026 and MT4** | no third-party work found |
| **What remains new:** measured training-data verifier retention and false accept against human instance gold, beside published rules on identical propositions; student object recall at five operating points chosen by a fixed rule before training, each beside its pre-training supervision recall, with a registered monotone-ordering test; a count-matched comparison with the base model's own and length-controlled captions — for SFT on verified propositions, object existence only | **NEW as far as the seven full texts and the review's 28-method check show** | the full corrected paragraph is E-A.3 of `ERRATUM_O31_5.md` |

## The corrected novelty statement (one sentence for the abstract)
For supervised fine-tuning on verified propositions, and for object existence only, we measure the training-data verifier's retention against human instance gold beside published verifier rules, and the student's object recall at five verifier operating points fixed before training, each beside its pre-training supervision recall. We then test the ordering on a 5,000-image rehearsal set and compare the student at a matched object count with the base model's own captions cut to the same length. All of this is done in Vietnamese, without new labels, preference or reinforcement learning, or a verifier at inference.

## Implications
- **Wording rules for the draft.**
  - Never write that no SFT work reports student behaviour across verifier operating points (HalluciDoctor does).
  - Never present the three-state verdict, the cross-family rule or the pre-SFT gate as contributions.
  - Never write "first non-English" (MHR).
  - "Same base model as Beyond Saying Less" is not distinctive, because SENTINEL also runs on Qwen2.5-VL-7B.
- **Comparators.** These follow from the table: VCD and DeCo (decoding-time), the released SENTINEL adapter (training-time, run as released) and, optionally, EFUF-style unlearning. HALVA, Nullu, OPERA, PAI, LURE and Woodpecker are cited, not run (ERRATUM_O31_5 E-D.2).
- **To read before the draft.** Less is More, MOCHa, VFC, LURE, HALVA, Nullu and MHR in full, plus 2610.23610 (against Paper A's boundary).

## V2_TO_V3 change list
1. 2609.35294: "TAKEN (goal)" narrowed to "TAKEN for coverage under RL; open for absolute hallucination reduction". Added: per-caption counts derived from Tab. 2, the two-point supervision-density result, the short prompt and the Qwen3-VL backbone.
2. 2605.20278: "160-image human-labelled diagnostic" corrected; only the reference caption is human, and the counts are made by Gemini. Added: the SFT stage on 2M Gemini captions (VQA average 66.90 → 58.23), the three severity-weight settings with one run each, and that captions halve during RL.
3. 2503.07906: the "InternVL-2" verifier is not confirmed. Verdicts reach the policy through two learned reward models, and the richness reward counts units whether they are correct or not.
4. 2402.09801: added the implicit three-state band (23–32), projector-only training, thresholds taken from 200 human-annotated captions, and the code's CLIP ViT-B/32 and window settings.
5. 2503.02846: added that its own out-of-domain correct facts drop 28 % (Tab. 1).
6. 2507.12455: added the three-state detector verdict, the run on Qwen2.5-VL-7B-Instruct (App. E Tab. 19), the released LoRA adapters (Apache-2.0) and that Cover is never reported.
7. 2311.13614: added the five-threshold sweep with SFT students (App. B.2 Tab. 5) and the RTX 3090 training. Its venue is now marked unverified.
8. The novelty row was rewritten. Items (i) (the registered gate) and (ii) (transfer slopes) of v2 are withdrawn as worded, and E-A.3 replaces them.
9. Nine works were added: Less is More, MOCHa, VFC, LURE, OPA-DPO, RLAIF-V, HALVA, Nullu and MHR. Two comparator rows were added: VCD and DeCo.
10. A `venue_verified` column was added to the table. Unverified venues are labelled.
