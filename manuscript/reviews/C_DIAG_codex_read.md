# Codex read-only review: Paper C C-DIAG prereg draft v1 (2026-11-08)

**Subject:** manuscript/prereg/2026-11-08_c_diag/C_DIAG_PREREG_DRAFT_v1.md (d6aae3f9), against scripts/c_pvr/c_pvr.py, scripts/c_stage1/decode_icl.py and CC-298.

Codex ran read-only through the codex plugin and edited no files. Its report follows verbatim, with the absolute link targets kept as written.

## Defects

- **High — XM600 reference access conflicts with the stated exclusion.** The prereg says XM600 receives no reference reads and limits the run to XM-dev500 ∪ XM-test2500. It also proposes parsing the XM3600 `full_data.json` and filtering to scored IDs ([draft lines 105–107, 113–120, 127–129](/mnt/d/vsps_image_captioning/manuscript/prereg/2026-11-08_c_diag/C_DIAG_PREREG_DRAFT_v1.md:105)). Reading that full file can read XM600 references before the filter applies. The producer needs a source that does not read the excluded references.

- **High — The stated bootstrap p-value is not a null-calibrated test.** The formula counts signs of the uncentered bootstrap contrasts. Their distribution is centered near the observed contrast. The `+1` correction prevents zero p-values but does not make those counts a valid null distribution ([draft lines 298–300](/mnt/d/vsps_image_captioning/manuscript/prereg/2026-11-08_c_diag/C_DIAG_PREREG_DRAFT_v1.md:298)). Use a defined null-centered procedure, or base decisions on the registered intervals.

- **Medium — Holm adjustment does not cover several decision labels.** The prereg defines a family of up to 14 contrasts. L1 requires Holm significance only for `P_obj^VI filt − ret`. The `filt − ctl` label, the CIDEr labels and the per-set `filt − rand` label use unadjusted CI rules ([draft lines 308–335](/mnt/d/vsps_image_captioning/manuscript/prereg/2026-11-08_c_diag/C_DIAG_PREREG_DRAFT_v1.md:308)). Those labels can therefore be triggered without the familywise adjustment the prereg describes.

- **Medium — The κ confidence interval has no rule for undefined bootstrap replicates.** The gate excludes UNCERTAIN labels before computing κ. A resample can leave too few eligible observations or a constant marginal, which makes κ undefined. The gate requires the CI lower bound for V1 but gives no handling rule for such replicates ([draft lines 227–240](/mnt/d/vsps_image_captioning/manuscript/prereg/2026-11-08_c_diag/C_DIAG_PREREG_DRAFT_v1.md:227)).

## Checks passed

- The draft hash matches the supplied prefix. The cited CC-298 decision file and both code files match their cited hashes.
- `c_pvr.verify` uses the first 32 propositions in flattened rank order, and the remaining propositions become UNCERTAIN. `parse_label` and the draft's REJECTED-only removal rule match the described behavior ([c_pvr.py lines 269–293](/mnt/d/vsps_image_captioning/scripts/c_pvr/c_pvr.py:269), [lines 343–362](/mnt/d/vsps_image_captioning/scripts/c_pvr/c_pvr.py:343)).
- `a7_masks` matches the removal counts per demonstration and uses the pinned A7 seed ([c_pvr.py lines 143, 343–350](/mnt/d/vsps_image_captioning/scripts/c_pvr/c_pvr.py:143)).
- The cited decoder supports the T1/T2 prompts, first/last retrieval ordering, greedy decoding and a 60-token short-caption cap ([decode_icl.py lines 48–58, 181–196, 255–260](/mnt/d/vsps_image_captioning/scripts/c_stage1/decode_icl.py:48)).
- The listed call, decode and GPU-hour estimates are arithmetically consistent with the stated rates.
## Round 2 (2026-11-09): v1.1 C_DIAG_PREREG_DRAFT_v1_1.md (c472fb82)

Codex ran read-only through the codex plugin and edited no files. Its report follows verbatim.

All four round-1 findings are closed in v1.1. Codex found no High defects. It raised two new Medium issues and one Low. The file is `/mnt/d/vsps_image_captioning/manuscript/prereg/2026-11-08_c_diag/C_DIAG_PREREG_DRAFT_v1_1.md`; the SHA-256 matches and it is 1,015 lines.

## Round-1 findings

- **High, XM600 references via `full_data.json`: closed.** The XM CIDEr producer reads the prefiltered XM-test2500 file, and `full_data.json` is expressly excluded. The label-subset step loads XM600 label rows but discards them without scoring or printing, so that is not a read of XM600 references (lines 193–210).
- **High, bootstrap p not null-calibrated: closed as written.** The bootstrap now gives percentile CIs only. The Holm family uses the separately defined arm-swap permutation p (lines 457–475).
- **Medium, Holm omitted some decision labels: closed within the stated scope.** Holm covers every completed XM P_obj contrast. CIDEr and the other listed outcomes are classed as descriptive, not tested claims (lines 482–500).
- **Medium, undefined κ bootstrap replicates: closed.** Undefined replicates are dropped and counted, and more than 1% makes that verifier a fault. An undefined point κ fails V1. An undefined blind κ is set to zero for V5 (lines 322–342).

## New findings

- **Medium, lines 465–475 and 504–512: the arm-swap p is not shown to be an exact test for the pooled-ratio null.**
  - Exactness needs within-image exchangeability or an arm randomization scheme. Here the arms are fixed pipeline outputs, and equal pooled precision does not imply exchangeability.
  - The prereg calls the distribution "exact" under a "sharp null" without defining that null as an exchangeability assumption.
  - The two-sided p has no sign, and the bootstrapped CI tests a different null. So p and CI can disagree on whether zero is excluded.
  - The label rules partly allow that disagreement: UPs is a Holm-rejected, positive estimate that fails UP's extra CI condition.
- **Medium, lines 478–480, 509–512 and 532–533: the UPs summary can print a false sentence.**
  - UPs includes any positive estimate that is not UP, and UP also requires the CI lower bound to be above zero.
  - A UPs case can therefore have an estimate at or above the 2-point SESOI (smallest effect size of interest) when its CI lower bound is nonpositive.
  - The summary text (S4/S4c) still says "precision rose by less than SESOI_P".
- **Low, lines 613–626: the one-verifier billed-hour total looks mis-rounded.** The listed InternVL3 components sum to about 12.83 h: 0.22 gate, 6.04 verify, 4.57 decode, 0.6 loads/wait and 1.4 overhead. That rounds to 12.8 h, not the stated ≈12.7 h.

## Checks that passed

- The SHA-256 and the 1,015-line count match.
- The allow-list names only the XM-test2500 reference file for XM and the dev references file for OV.
  - Test and confirm-half annotation files are not listed, and the prereg describes them as refused.
  - The separate §4.5 coordinator step sits outside the guard. Its inputs are tier-1 records, a manifest and the restricted label subset, with no XM600 references (lines 935–956).
- The 7×7×2×2 label table partitions its stated input states. Appendix D's row counts sum to 196, so the state enumeration is complete (lines 502–546, 996–1015). The UPs sentence above is the only false-print case Codex found.
- The planned `verify` behaviour fits `CAP = 32`.
  - It asks the first 32 propositions in input order and marks later ones UNCERTAIN.
  - The plan passes obj-only propositions in rank order and removes REJECTED only.
  - `a7_masks` samples the same number per demonstration (draft lines 235–249 and 416–422; `/mnt/d/vsps_image_captioning/scripts/c_pvr/c_pvr.py` lines 277–293 and 343–350).
- `/mnt/d/vsps_image_captioning/scripts/c_stage1/score.py` applies the existing output guard in its scoring variants. The `−inf` path uses no verifier scores, which matches the prereg's unguarded scoring plan (score.py lines 116–134; draft lines 428–432).
- The cap, cut and solvency worked example arithmetic is consistent, as are the main stage subtotals and cuts (lines 619–650).

The review was read-only. I did not edit or create any files.
## Round 3 (2026-11-09): v1.2 C_DIAG_PREREG_DRAFT_v1_2.md (afbb61fb)

Codex ran read-only through the codex plugin and edited no files. Its report follows verbatim.

## Round-2 findings

- **Arm-swap p: partly closed.** v1.2 now defines an exchangeability null. It says the null is stronger than equal pooled precision. It also requires the CI to agree in sign before a directional label is assigned, and a Holm rejection with a CI crossing zero maps to NS (prereg l.536–550, l.583–587). That closes the pooled-precision mismatch and the p/CI label disagreement. Exactness is still not established for the independent swaps (see new defects).
- **UPs/S4 summary: closed.** UPs now requires a positive point estimate, a positive CI lower bound, and "not UP". That makes its point estimate less than SESOI_P. D.1 confirms the condition, and the S4/S4c sentence is consistent with it (prereg l.585, l.607–610, l.1203–1210).
- **12.7 h rounding: closed.** The components total 12.83 h, correctly reported as about 12.8 h (prereg l.702–703).

## New defects

- **Medium, prereg l.537–549:** The stated exchangeability null does not establish exactness for the full permutation scheme. The procedure swaps arms independently across images. The null says only that the two arm-count pairs are exchangeable within each image. Exactness for independent swaps needs joint invariance of all image pairs under the product of those swaps, or an explicit independence assumption.
- **Medium, prereg l.727–729 against B run doc l.851–852:** The solvency reserve can understate B's resume cost. C-DIAG prices O_B's seven non-cap hours at `r_B` plus 30 VND. B's §12.3 resume check prices them at the resume offer's `RH′` and adds `FEE′`. If those differ from `r_B` and 30 VND, the reserve may not cover B's worst case.

## Checks that passed

- The prereg hash matches the supplied prefix, and the file is 1,231 lines.
- D.1's 56 consistent primitive cases partition into one state each. D.2's 196 combinations partition into one summary label each. Counts and S4/S4c branching are internally consistent (l.1195–1230).
- The gate-only branch specifies the both-below-floor trigger, the 3.0-hour cap, gate images only, and host deletion after the pull and before the verdict computation. It has its own solvency substitution, and the worked arithmetic checks out (l.163–167, l.710–737, l.781, l.1146, l.1182–1185).
- §4.5 names nine inputs, a narrow manifest check, the sorted 3,000-id restriction, and a seeded 10,000-by-3,000 bootstrap draw. The procedure is mechanically specified (l.426–465).
- The reused code matches the prereg in the functions inspected:
  - `verify` asks the first 32 propositions.
  - `a7_masks` matches removal counts per demonstration.
  - `demos_after` drops emptied demonstrations.
  - `decode_icl.py` supplies the described prompt and retrieval ordering.
  - The scorer's `−inf` path is unguarded.
  - Citations: `scripts/c_pvr/c_pvr.py` l.277–293 and l.343–362; `scripts/c_stage1/decode_icl.py` l.181–196; `scripts/c_stage1/score.py` l.116–134.

No files were changed. No tests, network requests or GPU jobs were run.