# Pre-Registration & Licence Verification (`B3` / `PD-4 Q6` / `PD-5 Q1`): `nocaps` (10 Refs) & `PASCAL-50S` (50 Refs)

- **Verification Date**: `2026-10-14`
- **Generator Script**: `.session_backup/2026-10-14/r12_verify/build_pd4_q6_preregs.py`
- **Companion JSON**: `.session_backup/2026-10-14/r12_verify/b3_licence_verification.json`
- **`B3` Execution Gate Status**: **`UNBLOCKED (True)`** (aggregate metrics only in git; `0` raw captions or images committed)

---

## 1. Summary Table: `nocaps` & `PASCAL-50S` Licence and Provenance Audit

| Property | `nocaps` (Validation) | `PASCAL-50S` |
|---|---|---|
| **Primary Citation** | Harsh Agrawal, Karan Desai, Yufei Wang, Xinlei Chen, Rishabh Jain, Mark Johnson, Dhruv Batra, Devi Parikh, Stefan Lee, Peter Anderson (ICCV 2019, pp. 8948-8957, arXiv:1812.08658) | Ramakrishna Vedantam, C. Lawrence Zitnick, Devi Parikh (CVPR 2015, pp. 4566-4575, arXiv:1411.5726, 'CIDEr: Consensus-based Image Description Evaluation') |
| **Eval Split Size** | `4500` images $\times$ `10` refs (`45000` captions) | `1000` images $\times$ `50` refs (`50000` captions) + `4000` human triplets |
| **Annotation Licence** | `Creative Commons Attribution 2.0 Generic (CC-BY 2.0) — released by the nocaps authors (allenai/nocaps, Georgia Tech / Allen Institute for AI) following the Open Images V4 annotation licence.` | `Academic research evaluation release by Vedantam, Zitnick & Parikh (CVPR 2015, Virginia Tech / Microsoft Research) on top of the 1,000 UIUC PASCAL Sentences / PASCAL VOC 2008 benchmark images (Flickr Terms of Use, academic research benchmark distribution). Standard benchmark evaluation and publication of aggregate correlation/slope statistics is permitted; raw images and raw 50-reference corpora are not redistributed in git.` |
| **Image Licence** | `Creative Commons Attribution 2.0 Generic (CC-BY 2.0) — all 4,500 validation images are from the Open Images V4 validation split (Flickr CC-BY 2.0 photos with individual photographer attribution in Open Images metadata).` | `Cyrus Rashtchian, Peter Young, Micah Hodosh, Julia Hockenmaier (NAACL HLT 2010 Workshop on Creating Speech and Language Data with Amazon's Mechanical Turk, 'Collecting Image Annotations Using Amazon's Mechanical Turk' — UIUC PASCAL Sentences, 1,000 PASCAL VOC 2008 images)` |
| **Academic Eval & Aggregate Reporting** | `True` | `True` |
| **Raw Images / Captions in Git** | `0` / `0` | `0` / `0` |

---

## 2. Detailed Provenance, Redistribution Rules, and Pre-Registered `H4` Role

### 2.1 `nocaps` (`R = 10` Independent Human References + Open Images V4 Object Labels)
- **Citation**: Harsh Agrawal, Karan Desai, Yufei Wang, Xinlei Chen, Rishabh Jain, Mark Johnson, Dhruv Batra, Devi Parikh, Stefan Lee, Peter Anderson (ICCV 2019, pp. 8948-8957, arXiv:1812.08658).
- **Official Source**: `https://nocaps.org/` (`https://nocaps.s3.amazonaws.com/nocaps_val_4500_captions.json`).
- **Licence Terms**: Creative Commons Attribution 2.0 Generic (CC-BY 2.0) — released by the nocaps authors (allenai/nocaps, Georgia Tech / Allen Institute for AI) following the Open Images V4 annotation licence. Creative Commons Attribution 2.0 Generic (CC-BY 2.0) — all 4,500 validation images are from the Open Images V4 validation split (Flickr CC-BY 2.0 photos with individual photographer attribution in Open Images metadata).
- **Ground-Truth Object Labels**: Open Images V4 human-verified bounding-box / image-level object classes (600 classes; ~51-80 overlapping with COCO-80).
- **Pre-registered Role in Testing `H4` Proposition**: Tests H4's proposition at R = 10 independent human references per image (subsampling k in {1, 2, 5, 10} references vs Open Images human-verified object labels): verifies that power-law exponent b(k) and the verbosity reward slope increase monotonically with k from k=1 to k=10 and instance labels.
- **Data-Availability Statement**: nocaps validation annotations and Open Images V4 images are publicly available from https://nocaps.org/ and https://storage.googleapis.com/openimages/web/index.html under CC-BY 2.0.

### 2.2 `PASCAL-50S` (`R = 50` Independent Human References + `4,000` Human Consensus Triplets)
- **Citation**: Ramakrishna Vedantam, C. Lawrence Zitnick, Devi Parikh (CVPR 2015, pp. 4566-4575, arXiv:1411.5726, 'CIDEr: Consensus-based Image Description Evaluation').
- **Underlying Image Corpus**: Cyrus Rashtchian, Peter Young, Micah Hodosh, Julia Hockenmaier (NAACL HLT 2010 Workshop on Creating Speech and Language Data with Amazon's Mechanical Turk, 'Collecting Image Annotations Using Amazon's Mechanical Turk' — UIUC PASCAL Sentences, 1,000 PASCAL VOC 2008 images).
- **Official Source**: `https://ramakrishnavedantam.com/cider/`.
- **Licence Terms**: Academic research evaluation release by Vedantam, Zitnick & Parikh (CVPR 2015, Virginia Tech / Microsoft Research) on top of the 1,000 UIUC PASCAL Sentences / PASCAL VOC 2008 benchmark images (Flickr Terms of Use, academic research benchmark distribution). Standard benchmark evaluation and publication of aggregate correlation/slope statistics is permitted; raw images and raw 50-reference corpora are not redistributed in git.
- **Triplet Breakdown**: `HC (Human-Human Correct, 1000), HI (Human-Human Incorrect, 1000), HM (Human-Machine, 1000), MM (Machine-Machine, 1000)`.
- **Pre-registered Role in Testing `H4` Proposition**: Tests H4's proposition across the full k in {1, 2, 5, 10, 20, 50} independent-annotator reference completeness curve on 1,000 images (50 independent AMT workers per image), plus human triplet preference concordance across HC/HI/HM/MM pairs.
- **Data-Availability Statement**: PASCAL-50S 50-reference annotations and 4,000 human-consensus triplets are available from the CIDEr project release (Vedantam et al., CVPR 2015) for research evaluation.

---

## 3. Repository Hygiene & Compliance Enforcement (`PD-4 Q7` & `PD-5 Q1`)

1. **Zero Raw Text or Image Redistribution**: Raw dataset archives (`nocaps` JSONs and `PASCAL-50S` mat/JSON files) reside only in unversioned `data/datasets/` storage and are excluded by `.gitignore`. Only aggregate JSON summaries (subsampled $k$-reference slopes, power-law exponents $\hat{b}(k)$, N2 exchangeability statistics, and triplet concordance accuracies) may be committed to git.
2. **Automated Pre-Commit Gate**: Every generated artifact is scanned by `licence_check.py --rev -`, `.session_backup/2026-10-14/r11_litmaps/openviic_leak_scan.py`, and `scan.py data/ktvic_openviic_refs.json` (`0` blocked blobs, `0` leaked 8-grams).
