# 6 Discussion

<!-- Draft 2026-10-15 (was sec7_discussion.md); renumbered and revised 2026-10-20 under PD-24. Numbers repeated from earlier sections carry the same src keys. -->

## 6.1 What a KTVIC CIDEr score measures

Taken together, Sections 3–5 identify four sources of variation in a KTVIC CIDEr score. They are not additive parts: each is measured on a different comparison.

1. **Task adaptation and template match.** A system fine-tuned on KTVIC learns the task format (one short Vietnamese sentence) and one writer's short, unpunctuated sentence pattern; we did not separate the two. Under our committed protocol, fine-tuning moves the score from 28.98 (zero-shot) to the 140s, and stripping the zero-shot outputs' final periods alone raises it to 33.30 (Section 3.3).
2. **Punctuation, where the pipeline keeps it.** In a pipeline that replaces the PTB tokenizer and drops its punctuation removal, one period per caption costs a system that never punctuates 35.17 points; with PTB-style removal it costs nothing (Section 3.3)<!-- src: .session_backup/2026-10-14/r11_verify/c8_l5_d1_d3a_cpu_audit.json :: l5_d1_punct_idf_law|ktvic_test_k1_to_k5_curves|p1assist_s42-short|first_k|k=5|d_abs -->.
3. **Tokenisation.** Word segmentation against syllable tokenisation moves the same outputs by 15.64 points; a second word segmenter moves them by less than one point (Section 3.4).<!-- R2 N-M8 -->
4. **Image content.** What the caption says about the image is what the score is meant to measure.

The first three are properties of the protocol and the reference writer, not of the image. Under our committed protocol each is larger than the gap between our system and the reported GRIT score. A KTVIC CIDEr difference is interpretable only between systems that share segmenter, punctuation policy and reference style, and even then it rewards matching one writer.

## 6.2 Object scores need count control and a second panel

Object-level metrics avoid the template problem but meet two others.

- **Count.** In Table 5.1, fuse2's higher object F1 comes with naming more objects, and every lever in the supplement that raised raw object F1 did so by naming more objects (S2, S6).<!-- CC-145 J6: condensed. -->
- **Incomplete, single-writer gold.** More than half of the objects KTVIC scores as unsupported for fuse2 are named by a separately written caption panel of the same images (Section 5.3). The two panels disagree about what is in the image. KTVIC's five references are one person's account, and treating them as five independent accounts overstates their coverage.

## 6.3 What a training-data gain on KTVIC measures

On development data with one backbone, adding KTVIC training images raised CIDEr-D against KTVIC references by +10.59 per doubling but against the OpenViIC panel of the same images by only +0.72 (Section 5.4). In a two-seed reverse pilot trained on OpenViIC captions, adapters gained +2.98 per doubling against the OpenViIC panel, so that panel does register training gains. Their gain against KTVIC references was not distinguishable from zero, nor from their own-panel slope; whether it reaches KTVIC references is not established (Section 5.5). Both are development results and panel-specific score associations; writer, annotators and protocol cannot be separated in them, and no held-out confirmation exists yet. For Vietnamese captioning this suggests that a training-set-size gain on KTVIC is first of all a gain in agreement with KTVIC's own references. A claim about better descriptions needs a second panel, and here also human judgments, which this paper does not collect.<!-- BD items 1, 2, 4, 14 (R5 m3): own subsection (was under 6.2 'Object scores need count control'); 'D0 GO' code removed; 'no new human judgments' made visible next to 'better descriptions' --><!-- src: .session_backup/2026-10-29/b_r1/decide.json (a6627047) :: primary.b_O_own ; primary.b_K_ci95 ; outcome (ASYMMETRIC, O5b per LOG CC-163 W9) --><!-- MERGE-SCOPED (PI-1029n approved B+D; was CONDITIONAL CC-163 W10; submission gated at 98, CC-166): remove with Sections 5.4-5.5 if the PI answers NO to B+D; revert text: delete Section 6.3 (heading and paragraph) and renumber 6.4-6.6 back to 6.3-6.5 (BD revision 2026-10-29 moved the D0/B-R1 sentences into 6.3) --><!-- src: manuscript/prereg/2026-10-29_b_d0/d0_decide.json (15dd925f) :: primary.b_K ; primary.b_O ; verdict -->

## 6.4 Recommendations for Vietnamese captioning evaluation

1. **Report a protocol card** with every score: segmenter and version, CIDEr variant, scale, punctuation policy, number of references and decoding (Section 4.2).
2. **Restore the PTB tokenizer's punctuation removal, or report CIDEr with and without it,** when a Vietnamese pipeline replaces that tokenizer with a word segmenter; state which pipeline produced every compared score.
3. **Publish the object matcher with object scores.** State whether its rules were checked by a human. Do not draw conclusions that depend on unattested rules (Section 3.5).
4. **Compare object metrics at matched count** (for example with the companion paper's count-matched controls) before claiming a precision gain.
5. **Use a second gold where one exists:** COCO instance labels for UIT-ViIC, a separately written caption panel (aggregates only) for KTVIC images.
6. **Check image overlap across datasets** before training on one and testing on another (Section 3.6). Do not use a model whose training images overlap KTVIC test (for example ViCLIP-OT, trained on UIT-OpenViIC) as an evaluator on KTVIC test.
7. **Do not call within-writer agreement a human ceiling** on KTVIC.

## 6.5 The evaluation kit puts the recommendations into practice

Most recommendations above have a component in the evaluation kit (Section 3.7), so a reader can apply them to a new system without our predictions or our models. Supplementary Table S14.1 maps each recommendation to its component; recommendation 4 relies on the companion paper's controls.

<!-- CC-145 J6 (2026-10-28, B pass 3): Table 6.1 moved whole to Supplementary S14 (Table S14.1). -->

<!-- CC-145 J6 (2026-10-28): two sentences cut as duplicates of Section 3.7 ("The kit carries no dataset captions (Section 3.7 reports the text scan of the archive). The numbers manifest that maps each number to its source is archived with the kit.") --><!-- R2 N-M1: manifest status made consistent with sec7.4 and the cover letter. --> The scripts that need KTVIC captions, OpenViIC or COCO read them from the reader's own copy, and nothing derived per image from OpenViIC leaves the reader's machine. Applied to three third-party systems on their own test splits, the kit reported recommendations 1 and 2 for each: the protocol card's columns, and CIDEr-D with and without punctuation removal (Section 3.7; Supplementary S9).<!-- CC-145 J6: "All GPU steps of that run used 620 GPU-seconds on one 24 GB GPU." cut (stated in Section 3.7). --><!-- src: scores.json e1a6e0d8 :: rows.* ; gpu_seconds.tsv 4bc43820 (sum 620) -->

## 6.6 What the controlled system contributes

P1-R is a simple, stable baseline: three seeds within 0.7 CIDEr-D of each other, with committed scores that a second machine reproduces byte for byte. Its value here is less its score than its role as an instrument. Because backbone, recipe and decoding are fixed, the differences we attribute to references, punctuation, matchers and gold cannot be differences between architectures. Every result in the main text comes from one model (Section 7.1).<!-- CC-145 J6: condensed; Section 7.1 "One model family" carries the second-backbone guard and the 3B fallback (S3). -->
