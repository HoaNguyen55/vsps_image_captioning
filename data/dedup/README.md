# KTVIC train ↔ test near-duplicates

`python scripts/near_dup.py --a train_data.json --b test_data.json --thr 0.95 --out data/dedup/ktvic_dup_train_test.json`
(CLIP ViT-B/32 image embeddings, cosine; RTX 3090, 2026-10-10).

| cos ≥ | 0.90 | 0.93 | 0.95 | 0.97 | 0.99 |
|---|---|---|---|---|---|
| test images | 46 | 15 | 11 | 8 | 5 |

Visual check of the top 48 pairs: all 12 pairs with cos ≥ 0.949 are the same photo; between 0.90 and 0.95 only
about 3–4 more are the same photo (crop/resize), the rest are similar scenes (markets, supermarkets, lantern streets).
So about 15 of 558 test images (≈3%) also appear in KTVIC train. Use cos ≥ 0.93 as the cut: removing those 15
gives a 543-image deduplicated test split. Overlap of KTVIC with UIT-OpenViIC (401/558 test, per ViCLIP-OT,
arXiv 2602.22678) is a separate question and is not measured here.

Object P/R/F1 on the 543-image deduplicated split (same lexicon/gold):

| model | P | R | F1 | (full 558: F1) |
|---|---|---|---|---|
| VSPS main s42 / s43 / s44 | 40.6 / 41.7 / 40.8 | 37.0 / 37.8 / 37.5 | 38.7 / 39.6 / 39.1 | 39.0 / 39.7 / 39.3 |
| v2 raw s42 | 37.3 | 42.5 | 39.7 | 40.1 |
| v2 clean s42 | 36.7 | 41.2 | 38.8 | 39.2 |
| zero-shot Qwen2.5-VL-7B | 30.8 | 57.4 | 40.1 | 40.7 |

Every score moves by ≤1 point and the ranking is unchanged, so the train↔test duplicates do not explain the paper's results.
