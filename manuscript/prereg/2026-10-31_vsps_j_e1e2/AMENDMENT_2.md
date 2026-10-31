# VSPS-J E1+E2 AMENDMENT_2: keep the two KTVIC train/test byte twins in E1b

Status: DRAFT for a one-judge diff read (REVERSIBLE, bar >= 90), 2026-10-31. Not committed.
Parent: AMENDMENT_1 as committed in edec78b (CC-209a GO-with-fixes 92). Trigger: OPS-1031e1bhold.
PI decision: **PI-1031l** (LOG): "Không cần quá sạch, dữ liệu của bài báo khác đã công bố thì dùng lại thôi, đừng quan tâm."

## B1. What changes
- Two of the 3,700 KTVIC-train images in E1b are byte-identical to KTVIC test images. These are the twin pairs known
  since CC-130 / PI-1026af:
  - train `00000003589.jpg` (sha256 bd5ea1bc…906261) = test `00000001335.jpg`
  - train `00000007511.jpg` (sha256 dc1cd698…90f9d) = test `00000000507.jpg`
- `cmd_e1b` exempts exactly these two shas from the `exclusion.json` `ktvic_test` byte check, through the constant
  `KTVIC_TWINS`. Any other image whose bytes match a KTVIC test image still stops the run with a FAULT, as before.
- The two images may sit on the E1b rental. KTVIC is a published dataset and E1b reads no KTVIC test label, so the PI
  ruled that custody here need not be stricter (PI-1031l).

## B2. What does not change
- The plan (`e1e2_plan.json` 0aafd392) and the E1b order sha are unchanged: both records stay in E1b.
- Rules, thresholds, grids, seeds, caps, statistics, scoring and the staged-scoring order are unchanged.
- E1a, its smoke-image check (`cmd_smokelist`, still refusing every KTVIC test byte) and the M1-only rule for UIT-ViIC
  test images are unchanged.
- No KTVIC test caption or label is read by E1b.

## B3. Disclosure
- The two records are reported in E1b like every other record. A note in the result says their images are byte-equal to
  KTVIC test images.
- No KTVIC-test claim may use E1b output.

## B4. Code
- `scripts/vsps_j_e1e2/e1e2.py`: the new constant `KTVIC_TWINS` (2 shas). In `cmd_e1b`, the refused set becomes
  `ktvic_test - KTVIC_TWINS`. No other line changes.
- `scripts/vsps_j_e1e2/test_e1e2.py`: the new `test_twin_exemption` checks that only a named twin passes and that any
  other test-identical image still faults.
- The diff is in `CC209b_A2.diff`, outside the SUMS.
