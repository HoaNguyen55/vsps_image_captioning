# 7 Discussion

<!-- Draft 2026-10-15. Numbers repeated from earlier sections carry the same src keys. -->

## 7.1 What a KTVIC CIDEr score measures

Taken together, Sections 3–6 decompose a KTVIC CIDEr score into four parts.

1. **Template match.** A system fine-tuned on KTVIC learns one writer's short, unpunctuated sentence pattern. That alone moves the score from 28.98 (zero-shot) to the 140s.
2. **Punctuation.** One period per caption costs 35.17 points<!-- src: .session_backup/2026-10-14/r11_verify/c8_l5_d1_d3a_cpu_audit.json :: l5_d1_punct_idf_law|ktvic_test_k1_to_k5_curves|p1assist_s42-short|first_k|k=5|d_abs -->.
3. **Tokenisation.** The choice of segmenter moves the same outputs by 15.64 points (Section 3.4).
4. **Image content.** Only the remainder reflects what the caption says about the image.

The first three parts are properties of the protocol and the reference writer, not of the image. They are also larger than most published differences between Vietnamese systems. A KTVIC CIDEr difference is interpretable only between systems that share segmenter, punctuation policy and reference style, and even then it rewards matching one writer.

## 7.2 Object scores need count control and a second panel

Object-level metrics avoid the template problem but meet two others.

- **Count.** Every lever in Section 6 that raised raw object F1 did so by naming more objects. The ladder (Section 5.2) shows that target curation moves the fine-tuned model along one precision–count frontier: more objects at the precision the frontier predicts.
- **Incomplete, single-writer gold.** More than half of the objects KTVIC scores as unsupported for fuse2 are named by an independent caption panel of the same images (Section 5.4). The two panels disagree about what is in the image. KTVIC's five references are one person's account, and treating them as five independent accounts overstates their coverage.

## 7.3 Recommendations for Vietnamese captioning evaluation

1. **Report a protocol card** with every score: segmenter and version, CIDEr variant, scale, punctuation policy, number of references and decoding (Section 4.2).
2. **Report CIDEr with and without final punctuation** when systems or references differ in punctuation convention.
3. **Publish the object matcher with object scores.** State whether its rules were checked by a human. Do not draw conclusions that depend on unattested rules (Section 3.5).
4. **Compare object metrics at matched count**, or report the frontier residual, before claiming a precision gain.
5. **Use a second gold where one exists:** COCO instance labels for UIT-ViIC, an independent caption panel (aggregates only) for KTVIC images.
6. **Check image overlap across datasets** before training on one and testing on another (Section 3.6). Do not use a model trained on KTVIC (for example ViCLIP-OT) as an evaluator on KTVIC test.
7. **Do not call within-writer agreement a human ceiling** on KTVIC.

## 7.4 What the controlled system contributes

P1-R is a simple, stable baseline: three seeds within 0.7 CIDEr-D of each other, reproduced byte for byte on a second machine. Its value here is less its score than its role as an instrument. Because backbone, recipe and decoding are fixed, the differences we attribute to references, punctuation, matchers and gold cannot be differences between architectures. The registered second backbone was aborted at its guard (Section 4.4); the pending 3B run tests scale within one family, not a different family.
