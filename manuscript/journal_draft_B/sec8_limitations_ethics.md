# 8 Limitations and ethics

<!-- Draft 2026-10-15. -->

## 8.1 Limitations

**One model family.** All results come from Qwen2.5-VL with one QLoRA recipe. The registered second backbone (Qwen3-VL-8B-Instruct) failed its Step 1 guard and was aborted per the registration (Section 4.4). The 3B fallback adds scale, not diversity, and is **PENDING**. We claim two model scales of one family (7B, 3B), not two backbones.

**Incomplete ladder.** Three of the five registered ladder steps (56 multiref, 57 rnd2, 58 unf2) are **PENDING** after a machine failure. The pooled equivalence result rests on two ladder steps and four seed replications of an anchor recipe. Its ±1.0 TOST sits at the edge of significance and was specified after runs 54 and 55 had landed (Section 4.3).

**Single seeds for some runs.** Each ladder step, cons included, has one seed. A miss of one to three precision points cannot be separated from seed noise.

**No human judgments.** We collected no new human annotation. The OpenViIC panel is a second set of captions, not ground truth. The within-writer leave-one-out figures are not a human ceiling. Model-generated signals (sample votes, kNN priors, model-drafted matcher rules) serve only inside methods and never as evidence.

**Matcher v3 is unattested.** Its rules were drafted by an AI model and have no human sign-off. No conclusion in this paper depends on it.

**Exploratory analyses.** The UIT-ViIC slope differences, the P-M6b look, the 35_e count-matched endpoint and all TOST results are exploratory or post-registration, and are labelled so where they appear.

**Comparators.** No published Vietnamese system has been rescored under our protocol. HDUCap and ViG could not be read in full (Section 2). We therefore make no ranking claim.

**XM3600 link.** The XM3600 CIDEr drop of the fine-tuned systems coincides with a change in end-period rate from 99.5% to 0.0%. We have not yet decomposed the drop by appending periods; the link is correlational until that run exists.

## 8.2 Data, licences and release

We use KTVIC as publicly released by its authors (Pham et al., 2024) and the other datasets under their published terms. We redistribute no images or reference captions; we release code, matchers, split/image IDs and aggregate scores, and readers obtain the data from the original sources.

**UIT-OpenViIC** is used only through aggregate statistics. No OpenViIC caption, n-gram or per-image derived file appears in this paper or its release. Every released file is scanned for 8-gram overlap with OpenViIC captions before publication, and the scan must find none.

**Leakage rules.** 401 of the 558 KTVIC test images are in OpenViIC's training split. No model here is trained on OpenViIC, and an OpenViIC-trained model must not be evaluated on KTVIC test. Any UIT-ViIC-trained adapter is scored on POPE-500 with all 21 UIT-ViIC training images excluded, and on the COCO probe without its 59 (Section 3.6). ViCLIP-OT is trained on KTVIC and is never used as an evaluator on KTVIC test.

**People in images.** Captions describe everyday scenes with people. No identity recognition is performed. Matcher rules for role and gender nouns are documented so that their effect on scores can be inspected.

## 8.3 Relation to the conference version and the companion paper

A conference version of part of this work appeared at FAIR 2026 ("A Method for Reducing Hallucinations in Detailed Vietnamese Image Captioning Using Supervision from Verified Propositions"). That paper's contribution, VSPS supervision from verified propositions, is not a contribution of this paper. What we reuse from it is the KTVIC/COCO setup, the QLoRA recipe and the P1 control. P1's seed-42 score (149.8 there, 149.79 here under the same scorer) serves only as a reference point. `new_vs_FAIR.md` itemises the overlap. A companion paper on object-count confounding in hallucination metrics is under review. It uses KTVIC only as a motivating example, and no number is a primary result in both papers.

## 8.4 Analysis provenance and the use of AI agents

Much of the analysis code and many intermediate reports were produced by AI coding agents (two different assistants) under human direction, with one agent reviewing the other's results. Reviews found that the agents' JSON outputs reproduced from raw data, but that their prose and logs sometimes contained numbers that existed in no output file, or that disagreed with the JSON. This draft follows the rules of the companion paper:

1. Every number is read from a JSON key and listed with its file hash in `number_manifest_B.tsv`.
2. A number with no computing source is not used. For example, a zero-shot CIDEr of 34.33 that came from a re-implemented scorer is replaced by the committed scorer's 28.98.
3. Predictions are frozen and committed before the outputs they predict are scored. Additions made after a look are labelled post-registration.
4. Model-generated signals are never gold or human evidence. No new human annotation was collected.
5. Every cited identifier is checked on a primary page, and unread papers are cited without their numbers.

The authors take responsibility for all analyses and text. TODO: adapt this subsection to the target venue's policy on AI assistance.
