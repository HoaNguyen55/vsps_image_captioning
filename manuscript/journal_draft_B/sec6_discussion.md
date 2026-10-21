# 6 Discussion

<!-- Draft 2026-10-15 (was sec7_discussion.md); renumbered and revised 2026-10-20 under PD-24. Numbers repeated from earlier sections carry the same src keys. -->

## 6.1 What a KTVIC CIDEr score measures

Taken together, Sections 3–5 identify four sources of variation in a KTVIC CIDEr score. They are not additive parts: each is measured on a different comparison.

1. **Template match.** A system fine-tuned on KTVIC learns one writer's short, unpunctuated sentence pattern. Fine-tuning moves the score from 28.98 (zero-shot) to the 140s, and stripping the zero-shot outputs' final periods alone raises it to 33.30 (Section 3.3).
2. **Punctuation.** One period per caption costs a system that never punctuates 35.17 points<!-- src: .session_backup/2026-10-14/r11_verify/c8_l5_d1_d3a_cpu_audit.json :: l5_d1_punct_idf_law|ktvic_test_k1_to_k5_curves|p1assist_s42-short|first_k|k=5|d_abs -->.
3. **Tokenisation.** Word segmentation against syllable tokenisation moves the same outputs by 15.64 points; a second word segmenter moves them by less than one point (Section 3.4).<!-- R2 N-M8 -->
4. **Image content.** What the caption says about the image is what the score is meant to measure.

The first three are properties of the protocol and the reference writer, not of the image. Each is larger than the gap between our system and the reported GRIT score. A KTVIC CIDEr difference is interpretable only between systems that share segmenter, punctuation policy and reference style, and even then it rewards matching one writer.

## 6.2 Object scores need count control and a second panel

Object-level metrics avoid the template problem but meet two others.

- **Count.** In Table 5.1, fuse2's higher object F1 comes with naming more objects. In the supplement, every training or decoding lever that raised raw object F1 did so by naming more objects (S6), and in the supervision ladder target curation mainly changed how many objects the fine-tuned model names (S2).
- **Incomplete, single-writer gold.** More than half of the objects KTVIC scores as unsupported for fuse2 are named by a separately written caption panel of the same images (Section 5.3). The two panels disagree about what is in the image. KTVIC's five references are one person's account, and treating them as five independent accounts overstates their coverage.

## 6.3 Recommendations for Vietnamese captioning evaluation

1. **Report a protocol card** with every score: segmenter and version, CIDEr variant, scale, punctuation policy, number of references and decoding (Section 4.2).
2. **Report CIDEr with and without final punctuation** when systems or references differ in punctuation convention.
3. **Publish the object matcher with object scores.** State whether its rules were checked by a human. Do not draw conclusions that depend on unattested rules (Section 3.5).
4. **Compare object metrics at matched count** (for example with the companion paper's count-matched controls) before claiming a precision gain.
5. **Use a second gold where one exists:** COCO instance labels for UIT-ViIC, a separately written caption panel (aggregates only) for KTVIC images.
6. **Check image overlap across datasets** before training on one and testing on another (Section 3.6). Do not use a model whose training images overlap KTVIC test (for example ViCLIP-OT, trained on UIT-OpenViIC) as an evaluator on KTVIC test.
7. **Do not call within-writer agreement a human ceiling** on KTVIC.

## 6.4 The evaluation kit puts the recommendations into practice

Most recommendations above have a component in the evaluation kit (Section 3.7, Table 3.1), so a reader can apply them to a new system without our predictions or our models.

| Recommendation | Kit component |
|---|---|
| 1. Protocol card | the scorer and the protocol card template (Section 4.2); every result file the scorer writes records its segmenter, tokenisation and scale |
| 2. CIDEr with and without final punctuation | the punctuation and XM3600 period audits (Section 3.3) |
| 3. Publish the matcher | the matcher code and the author-built word lists of v1 and v2; the model-drafted v3 rules are not included (Section 3.7) |
| 4. Count-matched comparison | none in this kit; the controls are the companion paper's |
| 5. A second gold | the two-gold protocol (COCO instance labels for UIT-ViIC; a second caption panel for KTVIC images, aggregates only) |
| 6. Image-overlap check | the image-overlap matcher, which regenerates the KTVIC–OpenViIC and UIT-ViIC / COCO / POPE-500 ID lists (Section 3.6) |
| 7. No within-writer "human ceiling" | the exchangeability test and the leave-one-out script (Section 3.2) |

The kit carries no dataset captions (Section 3.7 reports the text scan of the archive). The numbers manifest that maps each number to its source is archived with the kit.<!-- R2 N-M1: manifest status made consistent with sec7.4 and the cover letter. --> The scripts that need KTVIC captions, OpenViIC or COCO read them from the reader's own copy, and nothing derived per image from OpenViIC leaves the reader's machine.

## 6.5 What the controlled system contributes

P1-R is a simple, stable baseline: three seeds within 0.7 CIDEr-D of each other, with committed scores that a second machine reproduces byte for byte. Its value here is less its score than its role as an instrument. Because backbone, recipe and decoding are fixed, the differences we attribute to references, punctuation, matchers and gold cannot be differences between architectures. A registered second backbone stopped at its zero-shot guard, and the 3B fallback is not reported in this version (Supplementary S3), so every result in the main text comes from one model.
