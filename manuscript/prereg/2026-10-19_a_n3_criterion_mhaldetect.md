# A-N3 v2: criterion validity of object metrics against existing human hallucination labels (M-HalDetect)

Status: FINAL DRAFT for commit. Registered only if committed before any agreement statistic is computed. The scorer passes the gate before any statistic, with a self-check and a provenance check of its inputs; it reads the git-excluded M-HalDetect copy by sha pin only (PD-21, SCORERS).
Tier: registered secondary; Paper A body only; not in the abstract unless the confirmation map is amended before scoring (PD-21 (b)). Judge: PD-21 (sha `2e87e4322f06e8964d97d1dc36ef3cb3040dfabf7a531fab4566694cf8069d5b`). Supersedes the v1 draft (sha `f90603f2bb4f588b662348448adba984af9b8ea7def2e74528c9c5e42e7979cd`).
Machine-readable twin: `2026-10-19_a_n3_criterion_mhaldetect_v2.json`. All numbers are read in code by `code/build_a_n3_v2.py` from the files named.

## 1. Question
Do object-metric judgments agree better with human hallucination labels as the gold becomes more complete, and does
cF1 agree better than F1 where the gold is incomplete?

## 2. Data, licence and attribution
- Source pin: `github.com/hendryx-scale/mhal-detect` at `6ef75f547c81a65dbb4883624a4bc34321c43b9c`; blob and
  sha256 pins of LICENSE.md, README.md, train_raw.json and val_raw.json are in the JSON (`licence_handling.source_pin`).
- M-HalDetect: Gunjal, Yin and Bas, 'Detecting and Preventing Hallucinations in Large Vision Language Models', AAAI 2024 (arXiv 2308.06394). Annotations (c) 2023 Scale AI, CC BY-NC 4.0; images under the Flickr terms via COCO. Used for non-commercial research only; not redistributed; cited and attributed in Paper A.
- The download stays git-excluded. Only aggregates, COCO image-ID lists and the source pin are committed (PD-21 (b)).
- Release counts (`a_n3_mhaldetect_counts.json`): 14143 records, 14141
  after dedup; labels ACCURATE, INACCURATE, ANALYSIS, UNSURE on segments of InstructBLIP responses. The labels are
  human annotations.
- HAT: dropped. Disclosure: "no licence found (aloha@7da6b90e)" (PD-21 (c)).

## 3. Overlap disclosure
The captions are M-HalDetect's own InstructBLIP outputs, so this is new evidence on partly familiar images (PD-21 (b)). M-HalDetect images in Paper A sets (`a_n3_overlap.json` :: mhaldetect.all.overlap):
CV295 26, COCO-2500 217, CHAIR-500 40
(COCO-5000 Karpathy test 419). Labels on these images are used.

## 4. Analysis set (fixed now)
- Images: the 3419 M-HalDetect images with at least one COCO-2014 instance annotation (ID list pinned below); the 35 images without instances are excluded because their complete gold is empty. ID lists: `a_n3_image_ids_v2.txt` (3419 ids), `a_n3_excluded_no_instances_v2.txt` (35 ids).
- Records: every record of train_raw.json and val_raw.json (pinned) on those images, after dedup on (image, response) keeping the first in file order (train, then val): 13997 records (`a_n3_analysis_set_v2.json`).
- Several responses per image: each record is its own unit; the records of an image share its gold and its refs1_randk draws; no averaging or selection over responses; the bootstrap resamples images, so an image's records move together (the train/val shared images are one cluster).
- ANALYSIS and UNSURE spans: ANALYSIS and UNSURE spans stay in the response, so their classes count in the metric's mentions M_r; they never label a class: a class named only in ANALYSIS or UNSURE spans (or outside every span) is unlabelled and does not enter HP_r.
- Evaluable set E: records of the analysis set with |S_r| + |H_r| >= 1, non-empty gold at one_ref (every draw) and all_refs, and j_r > 0 at one_ref (every draw) and all_refs. E0 (sensitivity only): records with |S_r| + |H_r| >= 1, committed conventions as they are (sensitivity only).

## 5. Criterion
`score_coco_probe.en_classes(text, score_coco_probe.load_synonyms())`. A class c named in the response is supported if an ACCURATE span names it,
hallucinated if an INACCURATE span names it and no ACCURATE span does, and otherwise unlabelled.
HP_r = |S_r| / (|S_r| + |H_r|). Known bias: INACCURATE spans also carry attribute and relation errors. That works
against AN3-P1.

## 6. Golds and measures
one_ref = refs1_randk: score_g2b.random_subsets([5]*N, kmax=1, n_rep=20, seed=1) over the images in id order; score_g2b.gold_variants; all_refs = refs_all; complete = inst (from `a_n3_instance_gold.json`, derived
from the official COCO-2014 instances; data-path check {'overlap_images': 217, 'mismatches': 0});
union = inst+refs_all (descriptive). Verified negatives for cF1: U80 minus the instance classes. Per record, with
W = identity: F1, P, R from score_g2b.rows/scores; cF1 from measures.condensed(measures.judged_rows(...)). All
imported unchanged (sha pins in the JSON). cF1 = F1 at complete gold by construction (no unjudged mention when G = inst; measures.py D3 assert), so AN3-P2 is tested at one_ref and all_refs only (PD-21 (d)).

## 7. Statistic
tau_b(measure, HP) over E. 1000 image-cluster draws: numpy.random.default_rng(0).multinomial(N_img, [1/N_img]*N_img, size=n_boot) over images in id order; each record takes its image's multiplicity; all statistics share the draws (paired); CI = percentiles 2.5 and 97.5.

## 8. Registered predictions (from the theory; written before any agreement number)
- **AN3-P1 (primary):** tau_b(P@all_refs, HP) - tau_b(P@one_ref, HP) > 0 and tau_b(P@complete, HP) - tau_b(P@all_refs, HP) > 0 (compound of sign_gt_0).
  A mention outside the gold is scored as a hallucination whether or not the object is present. Added gold consists
  of present objects, so it removes false hallucinations and leaves the true ones. The instance gold is exhaustive
  over U80 by design.
- **AN3-P2 (secondary):** tau_b(cF1@one_ref, HP) - tau_b(F1@one_ref, HP) > 0 and tau_b(cF1@all_refs, HP) - tau_b(F1@all_refs, HP) > 0 (compound of sign_gt_0),
  at one_ref and all_refs only. cF1 drops the mentions that the reference gold cannot judge but the instance gold
  shows present. Recall is shared.
- Verdict rules: PASS if ci95_lo > 0; FAIL if point <= 0; else INCONCLUSIVE; compound: FAIL if any part FAIL; else PASS if every part PASS; else INCONCLUSIVE.
- Outcome: NOT_TESTABLE if |E| < 1000 records or < 500 images, or the data-path check fails; NOT_SUPPORTED if AN3-P1 FAIL; SUPPORTED if both
  PASS; MIXED otherwise.
- Kill: If AN3-P1 FAILs, Paper A does not state that agreement with human hallucination labels rises with gold completeness; the failed registered prediction is reported in the body.
- Descriptive only: union level; mention level hit rate, false-alarm rate and Youden J per level; tau_b of R and F1 per level; per split (train, val); the CV295 and COCO-2500 overlap images as a subset (not a confirmation on Paper A sets); E0 sensitivity; counts of supported, hallucinated and unlabelled mentions. Not registered: count-matched agreement (not registered: C1 is NOT-TESTABLE (PD-15) and M-HalDetect has one generator, so there is no between-system verbosity to match).

## 9. Scorer
scripts/an3/score_an3.py is written after registration and passes the gate before any statistic. It runs a
self-check on toy cases, checks the sha of every input against the pins (the M-HalDetect copy is read by sha only),
imports the committed modules unchanged and refuses an existing output.
