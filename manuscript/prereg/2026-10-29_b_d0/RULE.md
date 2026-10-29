# Paper B, D0 dev gate: same-image panel swap, own-panel vs other-panel slope (CC-158 W4)

Logged before any D0 score is computed. Dev data only (KTVIC dev300, a split of KTVIC train). No test set, no GPU.
One look: `scripts/b_d0/d0.py run` refuses to start if its output exists, if this file's sha256 differs from the
pin in the script, or if that sha256 is not in `.session_backup/2026-10-13/decisions/LOG.md`.
Everything below is AI opinion, not expert-validated.

## 1. Inputs (pinned by sha256)

| Input | sha256 |
|---|---|
| data/splits/ktvic_dev300.txt | cee024f8bb76846b1623e36d1861caccc4d13874db87544213a1f18f3de6898c |
| data/ktvic_openviic_refs.json (`_pairs.train` only; its merged caption lists are NOT used) | 4eb02cc43841bae4f844ee74d4c01b58e677dc8d6abafdd998c9f5b5706f725d |
| data/datasets/openviic/uit-openviic-annotation-train.json (the only OpenViIC file opened) | d757520e76b8490df6c7275c2beb8b3ecef0342635a436bea8c3cfd07eb49df0 |
| data/datasets/ktvic/train_data.json (KTVIC references of dev300) | 72ee9b57c350fb5f215e1f04701c515a51e5e415240e51a77c8ce00ce6316a0f |
| M4 mirror `.session_backup/machines/M4/root/outputs/b1_scaling/SHA256SUMS` | 7855927583f38b557857da632db904aad10ffc88fa51044bbdd338fae2ab58a1 |
| same folder, ledger.json (decided B-1 ledger) | 4afa3f44fa2da731f6fa6b8e02182b40328340f455443e334db36a4f1faab394 |
| same folder, decide.json (decided B-1 verdict, PASS b = +9.61) | b44a76fe6456e6c037fc5578b701f949e73515973b5f68263236e65d65addaf9 |

Models: the 15 decided B-1 adapters only, seeds 42/43/44 x levels L1-L5 (N = 216, 433, 867, 1734, 3469). Their
`b1_s{seed}_{L}-dev300-short.json` and `.preds.json` files are checked against the M4 SHA256SUMS. Zero-shot, step 0
and S5 rows are not used.

Scorer: Paper B kit B exactly as B-1 `score_rows` uses it (protocol_pilot 6aee4282..., punctuation_audit a7e80240...,
VnCoreNLP-1.2.jar RDRSegmenter, lower-cased, trailing punctuation tokens stripped from the hypothesis, CIDEr-D x100).
The jar is read from `$NCS_DATA/vncorenlp`. The script records `NCS_DATA` and the jar sha256 in its output.

## 2. Image set I (recomputed by the script, asserted)

I = dev300 ids whose KTVIC-train image has at least one matched copy with OpenViIC split `train` in
`_pairs.train`. |I| = 187. The sorted id list (one per line, trailing newline) has sha256
ba5069452fc8cf8cf644b057ba36775f6d2d001054a510adf7d1c23074e3bbb3.

Ids: 32, 77, 89, 98, 99, 182, 224, 236, 317, 320, 542, 584, 784, 805, 823, 826, 827, 859, 875, 890, 938, 979, 999,
1318, 1403, 1437, 1449, 1466, 1472, 1477, 1535, 1594, 1642, 1643, 1821, 1835, 1836, 1846, 2004, 2043, 2071, 2083,
2091, 2151, 2152, 2234, 2240, 2241, 2401, 2448, 2502, 2526, 2533, 2650, 2653, 2675, 2817, 2823, 2861, 2917, 2925,
2974, 2993, 2999, 3016, 3074, 3144, 3204, 3207, 3309, 3323, 3455, 3456, 3494, 3617, 3676, 3813, 3823, 3850, 3854,
4004, 4007, 4018, 4045, 4065, 4130, 4222, 4248, 4257, 4304, 4308, 4309, 4328, 4395, 4403, 4457, 4462, 4541, 4546,
4564, 4587, 4645, 4647, 4662, 4695, 4801, 4804, 4812, 4830, 4879, 4889, 4943, 4954, 4958, 4983, 4993, 4996, 5198,
5207, 5228, 5232, 5279, 5287, 5291, 5343, 5360, 5522, 5552, 5560, 5600, 5604, 5637, 5650, 5701, 5707, 5722, 5751,
5767, 5799, 5908, 5965, 5976, 5984, 6150, 6164, 6245, 6273, 6278, 6293, 6418, 7202, 7213, 7218, 7397, 9981, 10414,
10422, 10448, 10489, 10664, 10700, 10701, 10704, 10753, 10760, 10773, 10787, 10788, 10838, 10839, 10858, 10910,
10920, 10921, 10923, 10933, 10941, 10964, 10973, 10977, 11423, 11425, 11427, 11466, 11616, 11642, 11674

## 3. Reference panels and the k rule

- O pool of image i: captions of its OpenViIC-train copies only (8 images have two train copies; their captions are
  pooled), stripped, empty and exact repeats dropped. OpenViIC dev/test captions are never read, so the 6 images
  that also have a dev or test copy get train-copy captions only.
- K pool of image i: its KTVIC references from train_data.json, stripped, exact repeats dropped.
- **Deviation from "exactly k = 5" (pivot file l.70), fixed before scoring.** Counted before this rule (counts only,
  no score): 84 of the 187 images have fewer than 5 OpenViIC-train captions (66 have 4, 13 have 3, 5 have 2).
  Primary: k_i = min(5, |O pool_i|, |K pool_i|), the SAME k_i for both panels, so reference counts match per image.
- Hash rule, both panels: rank the pool by sha256 of the UTF-8 string `"{id}|{caption}"`, ascending, keep the first
  k_i.
- CIDEr-D document frequencies: one Cider object per panel, built from that panel's selected references on the 187
  images. No df from dev300's other 113 images.

## 4. Statistics

x = log2 N over L1-L5. For each panel P in {K, O} and adapter (s, L): per-image CIDEr-D against P, mean over I.

- **b_K** (own panel: the adapters were trained on KTVIC references) and **b_O** (other panel): pooled common slope
  with seed fixed effects (`b1.fe_slope`), CIDEr-D per doubling.
- **g = b_K - b_O**, the own-minus-other slope gap.
- **Scale-free companion g_rel = r_K - r_O**, where r_P is the same fixed-effects slope fitted to ln(mean CIDEr-D
  against P), times 100: per-cent gain per doubling. This guards against a gap that comes only from the O panel's
  lower CIDEr-D level.
- Also reported: ratio b_O / b_K, per-seed slopes and gaps, mean CIDEr-D at L1 and L5 per panel.
- Bootstrap: images resampled with replacement within I, B = 2000, `numpy default_rng(0)`, one (2000, 187) index
  matrix shared by every statistic and both panels (paired). Percentile 95% CIs. The gap CI comes from the paired
  draws of g, not from two separate CIs.

Object content (matcher v2 = `score_coco_probe.vi_objects(..., "v2")`, the COCO-80 Vietnamese lexicon of pivot P2):
per image, the mention set of the hypothesis vs the gold class set from (a) the selected K refs, (b) the selected
O refs, (c) their union; corpus F1 via `object_prf.image_counts` (exact classes) and `object_prf.scores`. Report F1
at each point, its fixed-effects slope with CI for (a), (b), (c), and the gap slope(a) - slope(b). Secondary, same
statistics with B-1's matcher (`rescap.chair.objects_in`). Object F1 never gates GO.

## 5. SESOI and the GO rule (pre-fixed)

- SESOI_D0 = 1.0 CIDEr-D per doubling. This is the B-1 LIMIT, the smallest slope B-1 treats as meaningful.
- **GO** if and only if all three hold: g >= SESOI_D0, CI_lo(g) > 0, and CI_lo(g_rel) > 0.
- **NO_GO** otherwise. The output labels the reason as one of:
  - `gap_below_sesoi`: g < 1.0;
  - `gap_ci_includes_0`;
  - `scale_only`: the absolute gap passes but the relative one does not.

What each outcome does (CC-158 Q1/W5):
- GO: B Option 1 stays eligible. Recommend YES on Q1 (B+D) only if W5 also finds no prior same-image cross-panel
  training study. All GPU items still need a re-rule at >= 90%.
- NO_GO: B Option 1 is dropped. B falls back to Option 2 / no pivot. Q1 is answered NO (D goes to VJCS).

## 6. What D0 fixes for the full study (formulas fixed now, values filled in by the script)

- P1 SESOI (own-minus-other slope gap in the T/T2 study) = max(1.0, 0.5 * g) CIDEr-D per doubling. Half the dev
  estimate allows for winner's-curse shrinkage. Computed only on GO.
- P2 equivalence margin (|object F1 of K-trained minus O-trained|, matcher v2, union gold) = max(2.0 F1 points,
  |slope (c)|, 2 * SD over seeds of F1 (c) at L5). The first term floors the margin; the second is one doubling of
  data's object gain; the third is seed noise.
- Neither value can be changed after this run except by a logged ruling.

## 7. Descriptive rows (pre-declared, no verdict)

1. Minus image 2004: dev300 image 2004 is a byte twin of L5 training image 4487 (CC-130). The same statistics are
   computed on I minus 2004, using masked draws of the same index matrix.
2. Exact k = 5: the images with at least 5 captions in both pools, at k = 5.
3. Panel description: mean k_i, mean reference length in syllables per panel, the share of selected O references
   that exactly equal a selected K reference after segmentation, and the mean best-match 4-gram Jaccard of each O
   reference to the K references. This is the independence caveat.
4. Reproduction gate: before any D0 number, KTVIC rescoring on all 300 images with 5 refs must reproduce the ledger
   `cider_s` mean of each of the 15 adapters within 1e-3. If any fails, the run aborts with no output. This re-reads
   a decided number and is not a look.

## 8. Output

`.session_backup/2026-10-29/b_d0/decide.json` holds ids, counts and numbers only. No caption text, from any
dataset, is written to any file or printed.
