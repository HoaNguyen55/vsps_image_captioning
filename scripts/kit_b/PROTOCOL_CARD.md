# Protocol card (fill in one per reported score table)

Paper B, Section 4.2. Report this card with every Vietnamese caption score. The right-hand column of the example gives the settings used for KTVIC in Paper B.

| Item | Your setting | Paper B (KTVIC) |
|---|---|---|
| Test set (name, split, number of images, references per image) | | KTVIC official test, 558 images, 5 references each |
| Segmenter (name, version, SHA-256 of the jar or package) | | RDRSegmenter, VnCoreNLP 1.2, jar SHA-256 `9e2811cdbc2ddfc71d04be5dc36e185c88dcd1ad4d5d69e4ff2e1369dccf7793`, applied to candidates and references |
| n-gram metrics (implementation, scale) | | pycocoevalcap BLEU-4, ROUGE-L, CIDEr-D, all ×100 |
| Punctuation (as written / final period stripped / period appended) | | as written; the stripped variant reported separately (`punctuation_audit.py`) |
| Decoding (greedy or sampling, captions per image, prompt) | | greedy, one caption per image per prompt |
| Object matcher (version) | | v2 (tone-normalised); v1 and v3 as sensitivity (the v3 rules are not in the kit) |
| Object P / R / F1 definition | | precision micro-averaged over mentions; recall macro-averaged over images with non-empty gold; F1 their harmonic mean; gold = union of the image's references |
| Uncertainty (method, draws, seed) | | paired bootstrap over images; image-clustered when seeds are pooled |
| Seeds | | 42, 43, 44 |
| Scorer process | | scoring runs as a separate process from generation |
| Result files (SHA-256 of each scored output) | | listed in the numbers manifest |
