# A-T3 r9: test list, deviations and disclosures (CC-197 W2-W5, W7)

Written 2026-10-30T18:30Z, before `score --tier 2`. No tier-2 outcome exists. PREREG.md is not edited; this file
records the deviations from it. The ledger line is OPS-1031at3res in LOG.md (CC-197 W1).

**Status.** The list below is fixed by this commit. `TEST_RESERVED` is not set and no tier-3 job exists. Both
come in one later commit, only after tier2.json shows REHEARSAL_PASS, the clause in section 2 (iii) holds, and a
one-judge read is done (CC-197 W6). On REHEARSAL_FAIL these ids stay reserved and are never touched.

## 1. The list

- File: `a_t3_testlist_r9_drop_all.json` (sha256 5aaa479f). N **3,232** of 5,000.
- ids_sha256 b0aefdb4a61c8099369d7f42a5625ab5aa83ec310a9f28f04bc2f00102727215.
- Builder: `scripts/a_t3/a_t3.py` 4bfeaef9 (commit 03e7c28, CC-194), laptop, ids only. Pins: Karpathy 2fd99922,
  val2017_ids ea37cee0, exclusion c52a96d1.
- Exact invocation (ONE `--drop` flag; `--drop` is `nargs="*"`, so a repeated flag keeps only the last list):

      python3 scripts/a_t3/a_t3.py testlist --karpathy data/datasets/karpathy/dataset_coco.json \
        --val2017-ids manuscript/prereg/2026-10-30_a_t3/val2017_ids.txt \
        --drop flickr_ids=flickr_ids.txt decoded_any=decoded_any_full.txt w2_test=w2_test.txt dev_test=dev_test.txt \
        --out <scratch>

  Re-run at HEAD 16c62e4 on 2026-10-30T18:25Z: the output is byte-identical (5aaa479f).
- Drop files: flickr_ids 96f9f845 (6), decoded_any_full 879a7f04 (449), w2_test e3b0c442 (empty), dev_test
  53ef1ba0 (1). decoded_any_full = decoded_any_an3 69465995 (296) union decoded_any_a1precheck 470d9f63 (169).
- counts_beside_5000: val2017 5,000; cap_restval 3,799; minus_chair500 3,746; minus_coco2500 3,746;
  minus_coco_karpathy_test 3,746; minus_cv295 3,746; minus_pope500 3,693; minus_uitviic_test 3,693;
  minus_c_near_dup_8 3,685; **minus_flickr_ids 3,679; minus_decoded_any 3,233; minus_w2_test 3,233;
  minus_dev_test 3,232**. No drop-file id is in the list.
- The list file's `status` field reads "NOT RESERVED (CC-183 r9)" because it was built before the reservation.
  The reservation is the ledger line and this commit; the file is kept byte-identical at its sha.

## 2. N below N_TEST_PLAN (CC-197 ruling 3, W3)

(i) **Deviation.** N = 3,232 < N_TEST_PLAN = 3,500. PREREG l.82 ("minus any id decoded by any study, smokes
included") and section 7 (test images "unused by A") drop the 449 ids that Paper A already scored against COCO
instance gold on third-party captions (A-N3 M-HalDetect 296, A-1 precheck CHAIR recompute 169, 16 shared; 446
remain after the Flickr drops). The constant N_TEST_PLAN = 3,500 is unchanged (PREREG l.194-195 "never replaced";
the CC-194 scoring closure a5c8e501 stays byte-identical).

(ii) **Planning-only recompute at 3,232** from the tier-1 effects (tier1.json 6d121592, n 990). Approximate closed
form; the tier-1 `_draws` were not saved, so this is not a rerun of the predictors: AD-1' z ~ 58, X5 z ~ 38,
X4 z ~ 26, P ~ 1.00 for each. No outcome was looked at.

(iii) **Stricter-only clause.** After `score --tier 2`, compute P at 3,232 directly (`a_t1.predict_null` on the
tier2 X5/X4 fields with n -> 3232; AD-1' se = (ci_hi - ci_lo)/3.92 * sqrt(n/3232)), or equivalently require
every tier2 P at 3,500 >= 0.987. If any P < 0.98 at 3,232 (or < 0.987 at 3,500), the result is treated as
REHEARSAL_FAIL even if tier2.json says PASS; the case goes to the PI and the test is not touched. The clause never
turns a FAIL into a PASS.

## 3. Disclosures (W4)

1. **m3 metadata read.** Before r9, `w2t_prep.py` l.44 (a6c0adc3) parsed `instances_val2017.json` on m3, reading
   `images[]` only (id, flickr_url), outside a_t3.py's TEST_MEMBER guard. The annotations were not read. Only the
   6 Flickr drop ids left M1. No outcome was seen.
2. **Laptop val2014 gold.** `data/datasets/coco_probe/annotations/instances_val2014.json` (160,682,675 bytes,
   gitignored, kept for A-N3 reproducibility) holds public COCO instance gold for all 3,232 reserved ids (3,199
   annotated), since val2017 is a subset of val2014. **Erratum to PREREG l.105** ("val2017 gold and images live
   only on m3"): the gold also exists on the laptop in the 2014 file. a_t3.py BAD_NAME (l.91) refuses
   `instances_val`; other scripts are not guarded. No outcome on these ids was looked at (the 449 that were are
   dropped). Tier-3 gold comes only from the m3 2017 member at zip pin 113a836d; the tier-3 scorer records the
   gold file sha and refuses any other.
3. **XM3600.** 1,745 XM3600 ids have no Flickr mapping and are unchecked (CC-183 Q5 default (a)). The 1,855
   mapped ids give 0 Flickr hits; the byte-sha check gives 0 hits.
4. **235057** dropped on the test side: a near-dup of the dev set (D1/D2/smoke), CC-184 r1 (`dev_test.txt`).
5. **Near-dups.** Test side 0 hits vs about 9 expected at the dev-side F8 rate (`a_t3_w2_test_drops.json`
   6160f3c0). The positive control re-found 5 of 5 dev-side F8 drops with the same per-set pattern
   (`a_t3_w2_posctl.json` 16d9238c).
6. **decoded_any reading.** Two sources, both Paper A's own evaluations against COCO instance gold: A-N3
   (M-HalDetect, InstructBLIP descriptions) 296 ids, and the A-1 precheck CHAIR recompute on public third-party
   CHAIR outputs 169 ids. Our own decodes contain none of the 449. The drop is about A's evaluation history, not
   leakage (CC-197 ruling 2).
7. **Code pin.** a_t3.py 4bfeaef9 (CC-194) supersedes the 0e063d9f cited in the r9 request; the testlist path is
   unchanged and the re-run above reproduces the list byte for byte.

`prep_report.json` (67aa07ce) holds the Flickr-map counts and hits and the 20 smoke image shas.

## 4. Tier-3 premise sentences (W5, CC-183 W7)

Each sentence is used verbatim for its case. N, N' and d are filled with the numbers from tier-3 output.

**Pre-decode gate fails** (`gold --set test` on m3, before any decode), by failed arm:

- L/R1 < 2 only: "On the 3,232 reserved COCO val2017 images, the label gold, measured before decoding, was not at
  least twice the size of one reference, so no image was decoded and the label-step test (AD-1') and the salience
  tests (X5, X4) were not run (PREMISE_NOT_MET)."
- sum|L| < 2 sum|R1 ∩ L| only: "On the 3,232 reserved COCO val2017 images, the label gold, measured before
  decoding, was not at least twice its overlap with one reference, so no image was decoded and the label-step test
  (AD-1') and the salience tests (X5, X4) were not run (PREMISE_NOT_MET)."
- Both: "On the 3,232 reserved COCO val2017 images, the label gold, measured before decoding, was neither at least
  twice the size of one reference nor at least twice its overlap with it, so no image was decoded and the
  label-step test (AD-1') and the salience tests (X5, X4) were not run (PREMISE_NOT_MET)."

**Score-time gate fails** (CC-184 F6): "On the N = 3,232 reserved COCO val2017 images the premise held before
decoding but not on the N' = <N'> images with a clean caption from every run (n_dropped_unclean = <d>), so the
label-step test (AD-1') and the salience tests X5 and X4 (x4_in_family true) are reported as PREMISE_NOT_MET,
without re-scoring or re-cleaning."

**Reading rule.** The tier-3 outcome is always 'SCORED' (a_t3.py l.591). If tier3.json `premise.gate_R1` is
false, AD-1', X5 and X4 are reported as PREMISE_NOT_MET whatever their p-values.

Log label unchanged: "known-to-pass and non-informative".

## 5. Files (SHA256SUMS in this folder)

The list, the six drop files, the two near-dup jsons, prep_report.json and this file. Ids, counts and shas only:
no caption text, no gold annotation, no image.
