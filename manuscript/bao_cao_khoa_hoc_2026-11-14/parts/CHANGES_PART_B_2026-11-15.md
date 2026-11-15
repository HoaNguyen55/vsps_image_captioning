# Changes to Part B of the scientific report, 2026-11-15

Working note for the coordinator; not part of the report. Nothing was edited in place, nothing was built into the report folder, nothing was committed.

## Files written (all in `parts/`)

- `B_report.v2_2026-11-15.md`: the new Part B. `B_report.v2_2026-11-15.diff`: `diff -u` against `B_report.md` (413 lines added, 0 removed or changed).
- `E_tinh_trang.v2_2026-11-15.md` and its `.diff`: Part E with only the lines that said the Paper B result was held or pending changed (list below).
- this file.

## Source used

The released draft after the three ruled edits of CC-420 W1: `.session_backup/2026-11-14/b_text_held/draft_v3_1/` (`paper.md` sha256 51821b40..., `number_manifest_B_v2.tsv` 31cc1066..., both equal to the TARGET values of CC-420; `online_resource.md` 19616bac..., unchanged from `draft_v3`). `draft_v3/paper.md` (cb462dfc...) differs from it only in the abstract (short form E1) and in the two prior-use sentences (E2, E3). The report follows `draft_v3_1`, the text that enters the paper repository. The held annexes (P3, P4, named systems) were not opened and are not reported.

## What changed in Part B

The existing Part B described the text of the paper repository (the KTVIC audit paper, `sec1` to `sec8`). The released draft is a rewrite with a new title and question (FE-CERT), so a line-level update was not possible. Sections B.1 to B.13 are kept byte for byte (their numbering is cited from the front matter and Part E), and the rewrite is reported in new sections:

| Place | Change |
|---|---|
| before B.1 | one paragraph "Cập nhật ngày 15/11/2026" explaining the two layers |
| B.1.8 (new) | how the rewrite relates to B.1 to B.13; Table B.29 (old section -> Online Resource 2 section, from S.0); three statements of B.1 to B.13 that no longer hold for the rewrite |
| B.14 | general information on the rewrite: title, drafting state (P3, P4, Section 6.6 absent; "not submitted in this state"), abstract claims, what it adds, what it does not claim, section map (Table B.30) |
| B.15 to B.18 | Sections 1 to 4 (introduction, related work, background, the certificate; equations B.8 to B.10, Table B.31) |
| B.19 | Section 5: registration, pools (Table B.32), stages, predictions and rules (Table B.33, equations B.11 to B.13), design of the human arm with D1 and D2 |
| B.20 | Sections 6.1 to 6.6: Tables B.34 (Table 4), B.35 (Table 5), B.36 (Table 7); P1 INCONCLUSIVE with LOW-SENSITIVITY, P2 NOT SUPPORTED, English control NOT RUN |
| B.21 | Section 6.7 in full: the nine disclosure items (D1 to D4 in English, word for word, each with a Vietnamese rendering; D6, D7; S8), Table B.37 (Table 6, every cell), agreement, rater-alone rows, the branch that fell; ten review remarks |
| B.22 to B.24 | Sections 7, 8, 9 and the Statements and Declarations |
| B.25 | Online Resource 1 (E.1 to E.7, incl. E.6 item 13: custody, items as built, pace with the unexplained time-on-screen medians) and Online Resource 2 (S.0) |
| B.26 to B.28 | claim-evidence table (Table B.38) with manifest keys, review list, glossary additions (Table B.39) |

Wording rules applied: no label word is attached to H-P or H-U anywhere; "no label: low inter-rater agreement" is kept in English; the ruled sentences S1, S3, S6, S7, S8, D1 to D4 are quoted in English and translated beside the quote; no rater-alone row is promoted; no reading of the low agreement is offered; no internal id appears in the report text. New references not yet in `paperB.bib` are named by author and year in prose only (no `[@key]`), so the build needs no new bib entry.

## Check result (scratch only)

Command (from the run repository root; the two prereg files are the default `B_EXTRA`):

```
D=.session_backup/2026-11-14/b_text_held/draft_v3_1; B=/mnt/d/vsps_papers/vsps-paperB-lre/paper
python3 -I manuscript/bao_cao_khoa_hoc_2026-11-14/checks/check_part.py manuscript/bao_cao_khoa_hoc_2026-11-14/parts/B_report.v2_2026-11-15.md --src $B/*.md $B/number_manifest_B.tsv $B/../prereg/2026-10-28_b1_scaling/PREREG.md $B/../prereg/2026-10-28_d_extrap/PREREG.md $D/paper.md $D/online_resource.md $D/number_manifest_B_v2.tsv --bib $B/paperB.bib --allow manuscript/bao_cao_khoa_hoc_2026-11-14/parts/B_report.allow.tsv
```

Result: words 60965; numbers checked 1355; matched 1355; allowed by list 0; UNMATCHED 0; citation keys used 64; MISSING from bib 0; review lists (address, tunnel, internal ruling id) all 0. Part E v2 with its own source list: 7 numbers, UNMATCHED 0. `00_mo_dau.md` against the new B and E: 17 numbers, UNMATCHED 0. A pandoc run of the new Part B alone with `paperB.bib` (Markdown and DOCX, in the scratchpad) ended without error. Also checked by script: all 45 manifest keys of Table B.38 exist in `number_manifest_B_v2.tsv`; every English quotation of 25 characters or more in the new sections occurs in `paper.md` or `online_resource.md` (whitespace-normalised).

For `run_all.sh` the coordinator sets `B_EXTRA` to the two prereg files plus the three draft files (after the transfer: the same files under `paper/rev_2026-11-15/`), and renames the v2 file or points the script and `build.sh` at it.

## Part E: lines changed (old line numbers of `E_tinh_trang.md`)

- l.10 (E.1, bullet "Bài B"): results no longer held; pointer to B.14 to B.28.
- l.12 (E.1): "hai nghiên cứu này" -> the Paper A study only.
- l.30 (E.3, "Nghiên cứu đang chạy"): labelling closed, analysis ran, labels stated without numbers.
- l.32 (E.3, "Phần so sánh cặp"): was a pending-state paragraph (deadline, remote rater, about 338 screens, single-rater fallback); now states what happened and points to B.19.5 and B.21. This is the one edit that goes beyond a bare status word; revert it if only status words may change.
- l.34 (E.3, "Văn bản bài sẽ thay đổi ở đâu"): rewrite finished and read, waits for the transfer; Part B now has two layers.
- l.64 and l.67 (E.7 items 1 and 4): rating done; what remains for the investigator.
- l.79 (Table E.2, row B): open work and blocked items updated.

Not changed, for the coordinator to decide: Part E l.3 ("tính đến rạng sáng ngày 15/11/2026"), l.20 and l.58 (Paper A items scheduled "after Paper B closes"). Front matter `00_mo_dau.md`: no line says the Paper B result is held, so nothing was changed; these lines describe Paper B by its earlier text only and may need a sentence: l.14 (sources "as of 14/11/2026"), l.32 (one-line description of Paper B), l.39 (Table 0.1, row B), l.54 (new human labels: "phần so sánh cặp của bài B (xem Phần E)"), l.56 (English comparison: still true, the registered English control is NOT RUN).

## Open points

1. Order of Part B: the rewrite is reported after the earlier text (B.14 to B.28) to keep every existing cross-reference valid. Moving it to the front would renumber B.2 to B.13 and the references to them in the front matter and Part E.
2. The paper repository has no `paper/rev_2026-11-15/` yet; the report cites the files by name only.
3. The four figures of the rewrite are not built, so the report inserts none.

## Source of the new numbers (file::key)

Every number of B.14 to B.28 is printed in `paper.md` or `online_resource.md` of `draft_v3_1` and has a row in `number_manifest_B_v2.tsv` (733 lines). The rows of the human arm and the head rows of P1 and P2 are listed here; the numbers of Sections 3 (POST HOC background) keep the keys of the earlier manifest `number_manifest_B.tsv`.

| Number | file::key [tag] | Status label |
|---|---|---|
| 6 | `owed/N9_OUTPUT.txt::breaks (N9_annexA.py 194c3c44 on DEV.json 88ff39aa) [h9_b]` | POST HOC |
| 54 | `owed/N9_OUTPUT.txt::near-margin Cert_NC (N9_annexA.py 194c3c44 on DEV.json 88ff39aa) [h9_n]` | POST HOC |
| 918 | `V.json::cert_dev [n003]` | DEVELOPMENT + FIRST SCORING OF RELEASED OUTPUTS |
| 68 | `V.json::derived: ids of V starting with D: [n007]` | DEVELOPMENT |
| 4 | `V.json::derived: ids of V starting with FL: [n008]` | FIRST SCORING OF RELEASED OUTPUTS |
| 72 | `RESULT.json::P1.N [n010]` | DEVELOPMENT + FIRST SCORING OF RELEASED OUTPUTS |
| 2 | `RESULT.json::P1.breaks [n011]` | HELD-OUT FRONT END |
| 0.0278 | `RESULT.json::P1.r [n012]` | HELD-OUT FRONT END |
| 0.0849 | `RESULT.json::P1.cp_upper_95 [n013]` | HELD-OUT FRONT END |
| 0.0050 | `RESULT.json::P1.cp_lower_95 [n014]` | HELD-OUT FRONT END |
| 54 | `DEV.json::derived: count of Cert_NC with z_min^NC <= 4 [n016]` | DEVELOPMENT |
| 915 | `NC.json::V_NC [n017]` | DEVELOPMENT |
| 6 | `NC.json::breaks [n018]` | DEVELOPMENT |
| 0.0066 | `NC.json::r_NC [n019]` | DEVELOPMENT |
| 22 | `GATE2.json::formed [n032]` | DESCRIPTIVE |
| 10 | `RESULT.json::P2.n_FL [n033]` | FIRST SCORING OF RELEASED OUTPUTS |
| 2 | `RESULT.json::P2.k_FL [n034]` | FIRST SCORING OF RELEASED OUTPUTS, HELD-OUT FRONT END |
| 20 | `GATE2.json::derived: formed comparisons with repo loc110504 [n044]` | DESCRIPTIVE |
| 1101 | `RESULT.json::counts.D_over_F_dev_DEVELOPMENT.comparisons [n046]` | DEVELOPMENT |
| 909 | `RESULT.json::counts.D_over_F_dev_DEVELOPMENT.CERTIFIED [n047]` | DEVELOPMENT |
| 0.0288 | `RESULT.json::counts.D_over_F_dev_DEVELOPMENT.CHANGED_share [n053]` | DEVELOPMENT |
| 22 | `RESULT.json::counts.FL_over_F.comparisons [n073]` | FIRST SCORING OF RELEASED OUTPUTS; F includes the HELD-OUT FRONT END members |
| 8 | `RESULT.json::counts.FL_over_F.CERTIFIED [n074]` | FIRST SCORING OF RELEASED OUTPUTS; F includes the HELD-OUT FRONT END members |
| 1123 | `RESULT.json::derived: len(comparisons) [n090]` | DESCRIPTIVE |
| 0.8012 | `RESULT.json::secondary.FE_PRED_AUC [n336]` | DESCRIPTIVE (D ∪ FL) |
| 0.9546 | `RESULT.json::secondary.FE_PRED_AUC_f0_significant_EXTRA [n339]` | DESCRIPTIVE (code row; no registered label of its own) |
| 10.0 | `B_PREF_LABELLING_PLAN_v1_1.md::l.43 [h_eps]` | REGISTERED CONSTANT (human arm design; not a result) |
| 0.60 | `B_PREF_LABELLING_PLAN_v1_1.md::l.105 [h_eq_hi]` | REGISTERED CONSTANT (human arm design; not a result) |
| 0.40 | `B_PREF_LABELLING_PLAN_v1_1.md::l.105 [h_eq_lo]` | REGISTERED CONSTANT (human arm design; not a result) |
| 40 | `B_PREF_LABELLING_PLAN_v1_1.md::l.158 [h_gateP]` | REGISTERED CONSTANT (human arm design; not a result) |
| 100 | `B_PREF_LABELLING_PLAN_v1_1.md::l.157 [h_gateU]` | REGISTERED CONSTANT (human arm design; not a result) |
| 0.5 | `B_PREF_LABELLING_PLAN_v1_1.md::l.104, l.105 [h_half]` | REGISTERED CONSTANT (human arm design; not a result) |
| 47 | `B_PREF_LABELLING_PLAN_v1_1.md::l.104 [h_ndec]` | REGISTERED CONSTANT (human arm design; not a result) |
| 40 | `B_PREF_LABELLING_PLAN_v1_1.md::l.57 [h_qC]` | REGISTERED CONSTANT (human arm design; not a result) |
| 100 | `B_PREF_LABELLING_PLAN_v1_1.md::l.57 [h_qP]` | REGISTERED CONSTANT (human arm design; not a result) |
| 160 | `B_PREF_LABELLING_PLAN_v1_1.md::l.57 [h_qU]` | REGISTERED CONSTANT (human arm design; not a result) |
| 30 | `B_PREF_LABELLING_PLAN_v1_1.md::l.62 [h_rep]` | REGISTERED CONSTANT (human arm design; not a result) |
| 40 | `BUILD.json::counts.drawn.C [hb_dC]` | DESCRIPTIVE (build record of the human arm; not a result) |
| 100 | `BUILD.json::counts.drawn.P [hb_dP]` | DESCRIPTIVE (build record of the human arm; not a result) |
| 160 | `BUILD.json::counts.drawn.U [hb_dU]` | DESCRIPTIVE (build record of the human arm; not a result) |
| 558 | `BUILD.json::counts.eligible_images.C [hb_eC]` | DESCRIPTIVE (build record of the human arm; not a result) |
| 165 | `BUILD.json::counts.eligible_images.P [hb_eP]` | DESCRIPTIVE (build record of the human arm; not a result) |
| 266 | `BUILD.json::counts.eligible_images.U [hb_eU]` | DESCRIPTIVE (build record of the human arm; not a result) |
| 300 | `BUILD.json::counts.main_pairs [hb_main]` | DESCRIPTIVE (build record of the human arm; not a result) |
| 298 | `BUILD.json::counts.pool_after_earlier_draws.C [hb_pC]` | DESCRIPTIVE (build record of the human arm; not a result) |
| 215 | `BUILD.json::counts.pool_after_earlier_draws.U [hb_pU]` | DESCRIPTIVE (build record of the human arm; not a result) |
| 8 | `BUILD.json::counts.practice_screens [hb_prac]` | DESCRIPTIVE (build record of the human arm; not a result) |
| 30 | `BUILD.json::counts.repeats [hb_rep]` | DESCRIPTIVE (build record of the human arm; not a result) |
| 330 | `BUILD.json::counts.screens [hb_scr]` | DESCRIPTIVE (build record of the human arm; not a result) |
| 0.603 | `HUMAN.json::derived: rater_alone.PI.P.k_word / rater_alone.PI.P.n [hd_aAPq]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 0.504 | `HUMAN.json::derived: rater_alone.PI.U.k_word / rater_alone.PI.U.n [hd_aAUq]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 0.522 | `HUMAN.json::derived: rater_alone.R2.P.k_word / rater_alone.R2.P.n [hd_aNPq]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 0.518 | `HUMAN.json::derived: rater_alone.R2.U.k_word / rater_alone.R2.U.n [hd_aNUq]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 170 | `HUMAN.json::derived: inter_rater.raw x inter_rater.n [hd_agree]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 172 | `HUMAN.json::derived: sum of strata.<s>.n_dec + not_decisive.split (pairs both raters decided) [hd_both]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 129 | `HUMAN.json::derived: sum of strata.<s>.n_dec over P, U, C [hd_dec]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 171 | `HUMAN.json::derived: not_decisive.tie + not_decisive.split [hd_notdec]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 0.507 | `HUMAN.json::derived: 1 - strata.U.q (the syllable share) [hd_syl]` | NEW HUMAN JUDGEMENTS; REGISTERED QUANTITY (no label: low inter-rater agreement) |
| 60 | `HUMAN.json::derived: tie_cannot_rates.PI.tie x inter_rater.n [hd_tieA]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 109 | `HUMAN.json::derived: tie_cannot_rates.R2.tie x inter_rater.n [hd_tieN]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 0.910 | `HUMAN.json::strata.C.ci95.1 [hh_Chi]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 20 | `HUMAN.json::strata.C.k_word [hh_Ck]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 0.564 | `HUMAN.json::strata.C.ci95.0 [hh_Clo]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 26 | `HUMAN.json::strata.C.n_dec [hh_Cn]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 0.769 | `HUMAN.json::strata.C.q [hh_Cq]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 0.755 | `HUMAN.json::strata.P.ci95.1 [hh_Phi]` | NEW HUMAN JUDGEMENTS; REGISTERED QUANTITY (no label: low inter-rater agreement) |
| 16 | `HUMAN.json::strata.P.k_word [hh_Pk]` | NEW HUMAN JUDGEMENTS; REGISTERED QUANTITY (no label: low inter-rater agreement) |
| 0.372 | `HUMAN.json::strata.P.ci95.0 [hh_Plo]` | NEW HUMAN JUDGEMENTS; REGISTERED QUANTITY (no label: low inter-rater agreement) |
| 28 | `HUMAN.json::strata.P.n_dec [hh_Pn]` | NEW HUMAN JUDGEMENTS; REGISTERED QUANTITY (no label: low inter-rater agreement) |
| 0.286 | `HUMAN.json::p.H-P [hh_Pp]` | NEW HUMAN JUDGEMENTS; REGISTERED QUANTITY (no label: low inter-rater agreement) |
| 0.571 | `HUMAN.json::strata.P.q [hh_Pq]` | NEW HUMAN JUDGEMENTS; REGISTERED QUANTITY (no label: low inter-rater agreement) |
| 0.611 | `HUMAN.json::strata.U.ci95.1 [hh_Uhi]` | NEW HUMAN JUDGEMENTS; REGISTERED QUANTITY (no label: low inter-rater agreement) |
| 37 | `HUMAN.json::strata.U.k_word [hh_Uk]` | NEW HUMAN JUDGEMENTS; REGISTERED QUANTITY (no label: low inter-rater agreement) |
| 0.376 | `HUMAN.json::strata.U.ci95.0 [hh_Ulo]` | NEW HUMAN JUDGEMENTS; REGISTERED QUANTITY (no label: low inter-rater agreement) |
| 75 | `HUMAN.json::strata.U.n_dec [hh_Un]` | NEW HUMAN JUDGEMENTS; REGISTERED QUANTITY (no label: low inter-rater agreement) |
| 1.000 | `HUMAN.json::p.H-U [hh_Up]` | NEW HUMAN JUDGEMENTS; REGISTERED QUANTITY (no label: low inter-rater agreement) |
| 0.493 | `HUMAN.json::strata.U.q [hh_Uq]` | NEW HUMAN JUDGEMENTS; REGISTERED QUANTITY (no label: low inter-rater agreement) |
| 38 | `HUMAN.json::rater_alone.PI.P.k_word [hh_aAPk]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 63 | `HUMAN.json::rater_alone.PI.P.n [hh_aAPn]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 0.065 | `HUMAN.json::rater_alone.PI.P.p [hh_aAPp]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 70 | `HUMAN.json::rater_alone.PI.U.k_word [hh_aAUk]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 139 | `HUMAN.json::rater_alone.PI.U.n [hh_aAUn]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 1.000 | `HUMAN.json::rater_alone.PI.U.p [hh_aAUp]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 24 | `HUMAN.json::rater_alone.R2.P.k_word [hh_aNPk]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 46 | `HUMAN.json::rater_alone.R2.P.n [hh_aNPn]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 0.441 | `HUMAN.json::rater_alone.R2.P.p [hh_aNPp]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 59 | `HUMAN.json::rater_alone.R2.U.k_word [hh_aNUk]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 114 | `HUMAN.json::rater_alone.R2.U.n [hh_aNUn]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 0.779 | `HUMAN.json::rater_alone.R2.U.p [hh_aNUp]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 0.355 | `HUMAN.json::inter_rater.ac1 [hh_ac]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 0.516 | `HUMAN.json::inter_rater.kappa_per_stratum.C [hh_kC]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 0.345 | `HUMAN.json::inter_rater.kappa_per_stratum.P [hh_kP]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 0.260 | `HUMAN.json::inter_rater.kappa_per_stratum.U [hh_kU]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 0.351 | `HUMAN.json::inter_rater.kappa [hh_kap]` | NEW HUMAN JUDGEMENTS; REGISTERED QUANTITY (no label: low inter-rater agreement) |
| 0.433 | `HUMAN.json::inter_rater.kappa_ci95.1 [hh_kaphi]` | NEW HUMAN JUDGEMENTS; REGISTERED QUANTITY (no label: low inter-rater agreement) |
| 0.270 | `HUMAN.json::inter_rater.kappa_ci95.0 [hh_kaplo]` | NEW HUMAN JUDGEMENTS; REGISTERED QUANTITY (no label: low inter-rater agreement) |
| 0.470 | `HUMAN.json::inter_rater.kappa_two_category [hh_ktwo]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 9 | `HUMAN.json::margin_bins.C.above_median.0 [hh_mChk]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 13 | `HUMAN.json::margin_bins.C.above_median.1 [hh_mChn]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 11 | `HUMAN.json::margin_bins.C.below_or_at_median.0 [hh_mClk]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 13 | `HUMAN.json::margin_bins.C.below_or_at_median.1 [hh_mCln]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 8 | `HUMAN.json::margin_bins.P.above_median.0 [hh_mPhk]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 14 | `HUMAN.json::margin_bins.P.above_median.1 [hh_mPhn]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 8 | `HUMAN.json::margin_bins.P.below_or_at_median.0 [hh_mPlk]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 14 | `HUMAN.json::margin_bins.P.below_or_at_median.1 [hh_mPln]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 17 | `HUMAN.json::margin_bins.U.above_median.0 [hh_mUhk]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 37 | `HUMAN.json::margin_bins.U.above_median.1 [hh_mUhn]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 20 | `HUMAN.json::margin_bins.U.below_or_at_median.0 [hh_mUlk]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 38 | `HUMAN.json::margin_bins.U.below_or_at_median.1 [hh_mUln]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 300 | `HUMAN.json::inter_rater.n [hh_n]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 0.567 | `HUMAN.json::inter_rater.raw [hh_raw]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 43 | `HUMAN.json::not_decisive.split [hh_split]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 128 | `HUMAN.json::not_decisive.tie [hh_tie]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 0.200 | `HUMAN.json::tie_cannot_rates.PI.tie [hh_tieA]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 0.363 | `HUMAN.json::tie_cannot_rates.R2.tie [hh_tieN]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 0.891 | `HUMAN.json::within_rater.PI.kappa [hh_wAk]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 0.933 | `HUMAN.json::within_rater.PI.raw [hh_wAraw]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 0.363 | `HUMAN.json::within_rater.R2.kappa [hh_wNk]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 0.567 | `HUMAN.json::within_rater.R2.raw [hh_wNraw]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 30 | `HUMAN.json::within_rater.PI.n [hh_wn]` | NEW HUMAN JUDGEMENTS; DESCRIPTIVE (registered row; no verdict) |
| 27 | `LOG.md (first 2697 lines)::INC-1115a-ungated-tunnel [hl_exp]` | LOG FACT (run record; not a result) |
| 363 | `LOG.md (first 2697 lines)::OPS-1115y-b-close-record [hl_linA]` | LOG FACT (run record; not a result) |
| 439 | `LOG.md (first 2697 lines)::OPS-1115y-b-close-record [hl_linN]` | LOG FACT (run record; not a result) |
| 67 | `LOG.md (first 2697 lines)::derived: minutes from first_t_server 2026-11-14T22:21:32Z to last_t_server 2026-11-14T23:28:10Z (OPS-1115y-b-close-record) [hl_minA]` | LOG FACT (run record; not a result) |
| 68 | `LOG.md (first 2697 lines)::derived: minutes from first_t_server 2026-11-15T06:53:35Z to last_t_server 2026-11-15T08:01:45Z (OPS-1115y-b-close-record) [hl_minN]` | LOG FACT (run record; not a result) |
| 614 | `LOG.md (first 2697 lines)::OPS-1115y-b-close-record [hl_msA]` | LOG FACT (run record; not a result) |
| 336 | `LOG.md (first 2697 lines)::OPS-1115y-b-close-record [hl_msN]` | LOG FACT (run record; not a result) |
| 330 | `LOG.md (first 2697 lines)::OPS-1115y-b-close-record [hl_qid]` | LOG FACT (run record; not a result) |
| 215 | `B_PREF_LABELLING_PLAN_v1_1.md::l.119 (decisive pairs for EQUIVALENT at a true 0.50) [hp_eq]` | REGISTERED CONSTANT (human arm design; not a result) |
| 0.05 | `B_PREF_LABELLING_PLAN_v1_1.md::l.108 (family-wise level of Holm's correction) [hp_holm]` | REGISTERED CONSTANT (human arm design; not a result) |
| 80% | `B_PREF_LABELLING_PLAN_v1_1.md::l.104 (power behind the 47 decisive pairs) [hp_pow]` | REGISTERED CONSTANT (human arm design; not a result) |
| 20 | `B_PREF_LABELLING_PLAN_v1_1.md::l.65 (expected seconds per screen) [hp_sec]` | REGISTERED CONSTANT (human arm design; not a result) |
| 0.70 | `B_PREF_LABELLING_PLAN_v1_1.md::l.104 (true share behind the 47 decisive pairs) [hp_true]` | REGISTERED CONSTANT (human arm design; not a result) |
| 0 | `H.rc::the return code of stage H [hr_rc]` | LOG FACT (run record; not a result) |
| 0.10 | `B_PREF_LABELLING_PLAN_v1_1.md::l.105 [h_eq10]` | REGISTERED CONSTANT (human arm design; not a result) |
| 0.20 | `B_PREF_LABELLING_PLAN_v1_1.md::l.128, l.129 [h_k20]` | REGISTERED CONSTANT (human arm design; not a result) |
| 0.40 | `B_PREF_LABELLING_PLAN_v1_1.md::l.127 [h_k40]` | REGISTERED CONSTANT (human arm design; not a result) |
| 90% | `B_PREF_LABELLING_PLAN_v1_1.md::l.105 [h_cp90]` | REGISTERED CONSTANT (human arm design; not a result) |
| 95% | `B_PREF_LABELLING_PLAN_v1_1.md::l.109, l.123 (level of the intervals) [hp_ci95]` | REGISTERED CONSTANT (human arm design; not a result) |

## Install and build (added after the coordinator's decisions, 2026-11-15)

Decisions taken: source `draft_v3_1` accepted (now committed in the paper repository as `paper/rev_2026-11-15/`, commit 568eaec); the rewrite stays after the earlier text; the Part E l.32 edit is accepted. This section supersedes the earlier statements of this file that nothing was installed or built, that the front matter was unchanged, and the diff counts and check counts given above for Part B (now: 413 lines added, 0 removed; 61,007 words).

**Part B, first lines.** The update paragraph was moved to directly under the part title and reworded as "Cách đọc Phần B": B.14 to B.28 describe the paper as it now stands (`paper/rev_2026-11-15/`), B.1 to B.13 the earlier text.

**Front matter, `00_mo_dau.v2_2026-11-15.md` and `.diff` (5 lines changed, old line numbers).**
- l.14: Part B also uses the rewritten draft stored on 15/11/2026 (B.14 to B.28); the text of 14/11/2026 is the earlier text (B.1 to B.13).
- l.32: one-line description of Paper B is now the front-end question; the KTVIC audit is an online resource.
- l.39 (Table 0.1, row B): question, main results (P1 "INCONCLUSIVE" with "LOW-SENSITIVITY", P2 "NOT SUPPORTED", human arm "no label: low inter-rater agreement", kappa 0.351) and evidence base; every number is printed in Part B and keyed in `number_manifest_B_v2.tsv`.
- l.54: the pairwise arm of Paper B is done and reported in B.21.
- l.56: English comparison: the registered control is "CONTROL: NOT RUN" (B.20.5); the earlier "none" row kept as the earlier text.

**Backups and install.** `B_report.md.pre_2026-11-15` (sha256 9ca314a60b7570ca...), `E_tinh_trang.md.pre_2026-11-15` (06b4a7ce389a9c99...), `00_mo_dau.md.pre_2026-11-15` (d4909dff2b9f253c...) are the files as they were. The v2 contents are now under the original names: `B_report.md` 69f1bd90a56ad64d..., `E_tinh_trang.md` 97b3f8c4bd15bc9d..., `00_mo_dau.md` 5b8af8c8363a00b2... (each byte-equal to its `.v2_2026-11-15.md`). Parts A, C and D were not touched. Nothing was committed.

**Check.** `checks/run_all.sh` with `B_EXTRA` = the two prereg files plus `paper.md`, `online_resource.md` and `number_manifest_B_v2.tsv` of `paper/rev_2026-11-15/`, and with the `A_EXTRA` of the caveat below: `ALL PARTS rc=0`. Matched numbers: A 712 of 712, B 1355 of 1355, C 1271 of 1271, D 368 of 368, E 7 of 7, 00 19 of 19; missing citation keys 0 in every part.

**Caveat on Part A (Part A to be refreshed when the Paper A text settles).** Without `A_EXTRA` the run ends rc=1 on Part A with four unmatched tokens. They are word counts of the length-warning block that Paper A commit dafba17 (2026-11-15) removed from `paper/abstract_A.md`:
- `A_report.md` line 7: 18,505; 10,005; 7,461
- `A_report.md` line 671: 18,505

The passing run used `A_EXTRA` = a scratch copy of `paper/abstract_A.md` at `dafba17^` (taken with `git show`, kept outside the repositories). Part A therefore still states the earlier word counts on those two lines; Part A was not changed.

**Build.** `build.sh` ran once after the checks. PDF: 234 pages. sha256 (equal to `build/SHA256SUMS`):
- `BAO_CAO_KHOA_HOC_VSPS_2026-11-14.md` 997e7b407e40e646f816be69165169254776f017d1d5a387220564365cab0b67
- `BAO_CAO_KHOA_HOC_VSPS_2026-11-14.docx` 825ac45aa9eb9a27d2f2a252624b47cd5587bba105352624943e6ac0c4b7cc68
- `BAO_CAO_KHOA_HOC_VSPS_2026-11-14.pdf` 6d35723f53e4e587df194402ab96e4336069609285d82444578d27d28522fa90
