# Paper A CONFIRMATION MAP (PD-10 binding 4)

**Written by** A-writer on 2026-10-18 at about 20:05Z; amended at about 20:25Z with the A4.1 XM3600 verdicts and the judge's CC-029 fixes 2–10. It is to be committed through the gatekeeper and the judge BEFORE anyone reads a scored K2, N9 or G2-B output.
- **No output exists yet.** When this map was written, no K2, N9 or G2-B output had been scored or read. Claude main stopped the local scorer, and the A4.2 v3 ledger (rows 41–45, 65, 66) gives `NO_RESULT_ON_DISK` for all three.
- **Fixed in advance.** The map fixes which registered verdicts carry each abstract-level claim, and which sentence the abstract uses for each outcome.
- **Not a new prediction.** It adds no prediction and changes no registered rule; every verdict rule below is quoted from its committed prereg.
- **Machine-readable copy:** `CONFIRMATION_MAP.json`.
- Amendment 1 (2026-10-18, PD-12): wording-only; abstract sentences shortened; no verdict rule, selection logic, precondition, qualifier or placeholder changed.
**Fixed frame (Amendment 1).** "Object-hallucination metrics such as CHAIR and object F1 score captions against gold; registered tests examine whether gold completeness and object count change them." The abstract opens with this text in every outcome; it carries no result claim.
**Brace fill format (Amendment 1).** "Each brace is filled mechanically, with no other words: {S}, {R}, {R'} and {k} take the integer the evaluator prints; {C*} takes the control name the evaluator prints (matched_prefix, sentence_tie_average or uniform_random_subset); {passed | failed | not run}, {selected {C*} | no control passed | not run} and {; a run was invalid under the registered protocol check, with no valid re-run | ; its runs were not scored by the freeze} take exactly one listed alternative, verbatim; {G2B-O1 and G2B-E2 verdict per set} takes 'O1/E2: CV295 v/v, XM600 v/v, UV231 v/v'; {G2B-E1 verdict per set} takes 'E1: CV295 v, XM600 v, UV231 v'; {failing verdicts} takes 'c: CV295 v, XM600 v, UV231 v', where c lists each of O1, E2 and P1, in that order, that is FAIL on at least one set, joined by '/', and each v gives those claims' verdicts in the same order, joined by '/'; {; if K1 fired: its exponent is dataset-specific} takes '; its exponent is dataset-specific' if K1 fired and nothing otherwise; every v is the evaluator's verdict token (PASS, FAIL, INCONCLUSIVE or NOT_EVALUABLE)."

**Sources.**
- PD-10 (`.session_backup/2026-10-13/decisions/PD-10.txt`): bindings 1–5 and the GitHub push times.
- A4.2 v3 ledger (`.session_backup/2026-10-18/paperA_tasks/A4.2/prereg_ledger_v3.tsv`).
- A4.4 `tests_status.tsv` (VERIFIED). The prereg texts are read at their registration commits; every one equals HEAD (sha256 in the JSON).

Times are UTC. "Push" is the GitHub server-side log (PD-10); the local reflog differs by 1–2 s. The experiment freeze for Paper A is 2026-11-10 (DEBATE D7).

## 1. Stage-2 tests (REGISTERED only, PD-10 binding 2)

| Test | Carries | Prereg (commit) | Commit / push | First output | Status |
|---|---|---|---|---|---|
| XM3600 N1 | C2 | `manuscript/prereg/2026-10-14_xm3600_predictions.{md,json}` (4ccbee3) | 2026-10-14 16:38:04 / 16:38:08 | 17:00:36 (+22m32s) | N1-XM-1, N1-XM-3 and N1-XM-4 PASS; N1-XM-2 and N1-XM-5 FAIL; kill rules not fired (1 of the 3 out-of-sample sign predictions failed; N1-XM-1 passed). Predictions mixed, not a clean pass (§2). |
| G2-B, primary claims only | C2 | `manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.{md,json}` (0932ba1); content from G2 REPORT §4 (6c647a6, 2026-10-14 07:01:40 / 07:01:58) | 2026-10-18 18:31:57 / 18:32:03 | none (ledger rows 41, 42, 66) | scheduled |
| K2 seed placebo (selects C*) | C1 | E1 REPORT §1 H4 and §4 K2 (6c647a6); addendum `manuscript/prereg/2026-10-18_e1_k2_placebo_addendum.md` (b8b2500) | 6c647a6 07:01:40 / 07:01:58; b8b2500 2026-10-18 17:42:08 / 17:42:28 | none (ledger row 45) | scheduled |
| N9 leaderboard, with the K-F gate | C1 | `manuscript/prereg/2026-10-18_n9_count_matched_leaderboard.{md,json}` (b8b2500); predictions L6 REPORT §3 D1 and §6 (4812563, 2026-10-14 10:39:32 / 10:42:03 local) | 2026-10-18 17:42:08 / 17:42:28 | none (ledger rows 43, 44, 65) | scheduled |
| LongCap-Arena (Q2) | human validity | `manuscript/prereg/2026-10-15_q2_longcap_arena.{md,json}` (7254a39) | 2026-10-15 02:50:04 / 02:50:10 | 05:59:16 (+3h09m; the crashed first run's time is not preserved) | MIXED (computed) |
| VaPR count control (Q4) | human validity, as PD-10 groups it; preference data, not human judgments | `manuscript/prereg/2026-10-15_q4_vapr_count_control.{md,json}` (7254a39) | 2026-10-15 02:50:04 / 02:50:10 | 02:50:28 (+24 s) | PASS (computed) |

## 2. C2: gold completeness and the frontier (leads the abstract)

**Registered verdict rules, quoted.**
- **XM3600** (prereg md lines 57–65):
  - N1-XM-1: slope(refs1_randk) < 0; N1-XM-2: slope(refs_all) > 0; N1-XM-3: slope(oiv7_verified) > 0; N1-XM-4: slope(refs1_randk) < slope(refs_all) < slope(oiv7_verified); N1-XM-5: for each gold variant g in {refs1_firstk, refs1_randk, refs_all, oiv7_verified}, sign(slope_g) = sign(M*_mixed(g) − median M).
  - Kill: "If ≥ 2 of the 3 out-of-sample sign predictions (N1-XM-1, N1-XM-2, N1-XM-3) fail, N1 is demoted from a core result to an explanatory lemma / diagnostic."
  - Kill: "If slope(refs1_randk) ≥ 0 (N1-XM-1 fails), N1's 1-reference prediction fails in a third setting and the sign-flip claim is dropped".
- **XM3600 computed verdicts** (`.session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json :: prereg_comparisons[16..20]`): N1-XM-1 PASS, N1-XM-2 FAIL, N1-XM-3 PASS, N1-XM-4 PASS, N1-XM-5 FAIL. N1-XM-5 agrees for 3 of 4 gold variants; it fails only for refs_all, where M*_mixed = 1.7631 is above the median M = 1.3833 but the slope is −2.4278 (prereg_comparisons[20].observed_value.per_gold.refs_all). Both failures therefore concern the gold of all 2–3 references. **Registered verdict:** neither kill fired. The demotion rule needs 2 of the 3 out-of-sample sign predictions to fail, and only N1-XM-2 did; the sign-flip kill needs N1-XM-1 to fail, and it passed. The predictions are mixed; XM3600 is not a clean pass. Cross-check: `.session_backup/2026-10-18/paperA_tasks/A4.1/MANIFEST.json` (sha256 06824b7bddfd, pending A-verifier) :: verdicts[9..13] give the same five labels, and verdicts[14] ("XM3600 kill rule (H6 P2)") is NOT_FIRED with 1 failure among N1-XM-1..3; `.session_backup/2026-10-18/paperA_tasks/A4.1/tab4.tex` (sha256 dfd8fe8474c1) row tab4.p0.r16 labels XM3600 N1 "Predictions mixed", registered.
- **G2-B** (prereg §8–§11):
  - "`sign_gt_0`: PASS if ci95_lo > 0; FAIL if point <= 0; else INCONCLUSIVE"; "`sign_lt_0`: PASS if ci95_hi < 0; FAIL if point >= 0; else INCONCLUSIVE"; "`compound`: FAIL if any part is FAIL; else NOT_EVALUABLE if any part is NOT_EVALUABLE; else PASS if every part is PASS; else INCONCLUSIVE".
  - Primary claims: G2B-E1 one-reference endpoint, `slope[refs1_randk]` sign_lt_0; G2B-E2 complete-gold endpoint, `slope[complete]` sign_gt_0; G2B-O1 ordering, compound of two sign_gt_0 differences; G2B-P1 exponent ordering. Sets: cv295, uv231, xm600. G2B-NS: the multi-reference sign is "NOT predicted".
  - Kill K1: "G2B-P1 is FAIL on 2 or more of the 3 datasets" → "drops the completeness account for this backbone and reports only that the exponent is dataset-specific".
  - Kill KN1: "G2B-E1 is FAIL … on any dataset" → "the sign-flip claim (N1) is dropped from Paper A; only the ordering result can remain".
  - Reporting: "'Replicates on a second backbone' may be written only for CV295 and XM600, and only where G2B-E1, G2B-E2 and G2B-O1 all PASS."

**Map rule** (fixed now, before any G2-B output). Over the six verdicts G2B-E2 and G2B-O1 on cv295, uv231 and xm600:
- **PASS:** all six PASS and K1 does not fire.
- **FAIL:** K1 fires, or G2B-E2 or G2B-O1 is FAIL on 2 or more of the 3 sets (a set counts when either verdict is FAIL there).
- **MIXED:** neither PASS nor FAIL.
- **NOT-TESTABLE:** no evaluable G2-B verdict by 2026-11-10 (no run, or all primary verdicts NOT_EVALUABLE, or all runs excluded by KD or KL).

**Abstract sentence.** Braces are filled from the evaluator's output, as computed.
- **PASS:** "In registered confirmation tests, F1's slope on log object count is ordered by gold completeness and positive under complete gold on XM3600 and, with a second backbone (Qwen3-VL-8B), on 600 discovery-disjoint XM3600 images and 295 discovery images; a UIT-ViIC test pass, on COCO train2017 images the backbone may have seen, is not counted as support. On XM3600, two of five registered predictions failed on a negative slope with all 2–3 references; the registered demotion rule did not fire."
- **MIXED:** "In registered confirmation tests, F1's slope on log object count is ordered by gold completeness and positive under complete gold on XM3600; with a second backbone (Qwen3-VL-8B) the result is mixed ({G2B-O1 and G2B-E2 verdict per set}; a UIT-ViIC test pass, on COCO train2017 images the backbone may have seen, is not counted as support). On XM3600, two of five registered predictions failed on a negative slope with all 2–3 references; the registered demotion rule did not fire."
- **FAIL:** "In registered confirmation tests, F1's slope on log object count is ordered by gold completeness and positive under complete gold on XM3600, but not with a second backbone (Qwen3-VL-8B: {failing verdicts}{; if K1 fired: its exponent is dataset-specific}). On XM3600, two of five registered predictions failed on a negative slope with all 2–3 references; the registered demotion rule did not fire."
- **NOT-TESTABLE:** "In a registered confirmation test on XM3600, F1's slope on log object count is ordered by gold completeness and positive under complete gold, but two of its five registered predictions failed on a negative slope with all 2–3 references (the registered demotion rule did not fire); the registered second-backbone test was not evaluable."
- **"Replicate(s)"** may be written only for CV295 and XM600, and only on a set where G2B-E1, G2B-E2 and G2B-O1 all PASS (the G2-B reporting rule quoted above). It is never written for UV231.

**One-reference clause,** appended to the C2 sentence. It is an empirical sign, not a prediction of the theory (CC-007; G2B-E1 is "the empirical half of N1").
- G2B-E1 PASS on all three sets: "The one-reference slope is negative in every registered test, an empirical observation the theory does not predict."
- KN1 fires: "The one-reference sign is not confirmed (registered kill KN1); only the ordering is claimed."
- Otherwise: "The one-reference slope is negative on XM3600 and {G2B-E1 verdict per set} with the second backbone."

**Scope (binding 3).** On CV295, G2-B is a NEW-BACKBONE replication on 295 discovery images, with the same references and instance gold. CV295 ⊂ COCO-2500: all 295 cocoids are in `data/coco_probe/manifest.json`. It is NOT an image-out-of-sample test. Image-disjoint confirmation comes from UV231, XM600 and XM3600 N1 (binding 3). Under CC-024, a FAIL on UV231 counts against the claim, but a PASS there is not counted as support: its images are COCO train2017 images, which the backbone may have seen (G2-B prereg §4).

**Completed tests.** Any registered C2 test that completes, B3 included, enters §7.7 and §10.1 with its verdict as computed, failures included (judge, CC-029; §6).

## 3. C1: count control (second in the abstract)

**Registered verdict rules, quoted.**
- **K2** (addendum §3): prediction "|dP_MCP| < 0.5".
  - Kill: "|dP_MCP| > 1.0, or a 95% interval that excludes 0, means the matched-prefix control is miscalibrated: stop, and draw no matched-prefix conclusion from E1 or N9 (E1 §4 K2)".
  - "a control is *admissible* iff |dP| ≤ 0.5 and its 95% interval covers 0. N9's primary control C* is the first admissible control in the order matched prefix, sentence tie-average, uniform random subset."
- **K-F** (N9 §7): "If |ΔCHAIR_i| > 1.0 or |ΔCHAIR_s| > 1.5, the protocol is fixed before any method look. The failed run is kept and disclosed."
- **N9 P1** (§5): "A method **SURVIVES** iff its Holm-adjusted p < 0.05 AND dP_C* ≥ +1.0".
- **K-headline:** "If at least half of the methods (≥ 3 of 6) SURVIVE on P1, the headline becomes 'training changes object choice'."
- **K-rank:** "If no pair is significantly reversed, Paper A reports N9 as 'consistent with the raw ranking' and rests no claim on it."
- **K-placebo:** "If no control is admissible on K2, P1 has no primary control. N9 reports the three per-image controls as a specification curve and makes no 'survives count control' claim, and Paper A's C1 wording becomes 'count control changes the ranking'."
- **Prediction (b), "the primary frozen prediction":** "HELD iff D_b ≥ +0.3 and its 95% lower bound > 0". K-b: "If D_b < 0.1, prediction (b) is dropped and N9 'shows no Δk → Δm link'".

**Map rule.**
- **NOT-TESTABLE:** K-F fails with no protocol fix before any method look, or K-protocol leaves the base or a method run invalid with no valid re-run, or the runs are not scored by 2026-11-10.
- **MIXED:** K-F passes and K-placebo fires (no admissible control).
- **PASS:** K-F passes, C* exists, and K-rank finds at least one significantly reversed pair.
- **FAIL:** K-F passes, C* exists, and K-rank finds none.

**Abstract sentence.** {S} = SURVIVES count out of 6, and {R} = reversed pairs, as computed. Every C1 sentence names both preconditions: the K-F fidelity check and the K2 seed-placebo selection.
- **PASS:** "In a registered count-matched leaderboard of six public LLaVA-1.5-7B anti-hallucination checkpoints, scored after a registered fidelity check and under the per-image control a registered seed placebo selected, count control significantly reverses {R} pairwise rankings of raw precision gains, and {S} of 6 gains survive it."
- **FAIL:** "In a registered count-matched leaderboard of six public LLaVA-1.5-7B anti-hallucination checkpoints, scored after a registered fidelity check and under the per-image control a registered seed placebo selected, the ranking is consistent with the raw ranking (no significantly reversed pair), so no claim rests on it; {S} of 6 gains survive the control."
- **MIXED (K-placebo).** Choose by K-rank's test, run under each of the three per-image controls:
  - (a) at least one significantly reversed pair under at least one control: "After a registered fidelity check, the registered leaderboard of six public LLaVA-1.5-7B anti-hallucination checkpoints is reported as a specification curve over three per-image controls (none passed the registered seed placebo), so no gain is claimed to survive count control; count control changes the ranking ({R'} significantly reversed pairs under {k} of 3 controls)."
  - (b) none: "After a registered fidelity check, the registered leaderboard of six public LLaVA-1.5-7B anti-hallucination checkpoints is reported as a specification curve over three per-image controls (none passed the registered seed placebo), so no gain is claimed to survive count control; the ranking is consistent with the raw ranking under all three controls, and no claim rests on it."
  - The registered wording "count control changes the ranking" is used only in (a), and never with a claim that a gain survives count control.
- **NOT-TESTABLE:** "A registered count-matched leaderboard of six public LLaVA-1.5-7B anti-hallucination checkpoints could not be scored (registered fidelity check: {passed | failed | not run}; registered seed placebo: {selected {C*} | no control passed | not run}{; a run was invalid under the registered protocol check, with no valid re-run | ; its runs were not scored by the freeze}), so no confirmatory count-control claim is made; the post-hoc re-scoring of 15 published comparisons is exploratory."

**Modifiers.**
- If S ≥ 3 (K-headline), append "; training changes object choice" (PASS and FAIL only; under K-placebo, P1 has no primary control).
- If the K2 kill fires for the matched prefix, append: "The matched prefix failed the registered seed placebo, so neither analysis draws a matched-prefix conclusion."
- Prediction (b) is reported in §6.4 and is not abstract-level. If K-b fires, both halves of the §9 conjunctive kill have fired (the first half, the failed L6 D2 prediction, already did; ledger row 64). Then "length control leaves a count channel" is withdrawn wherever it is carried: contribution 5 ("length matching does not remove this"), §9's "Length matching does not remove the channel" and its "What the audit implies" paragraph, and every §10 sentence that carries the claim; Table 9.1 becomes description only. If N9 is NOT-TESTABLE, the paper states that the second half of the kill could not be evaluated.

**Stage 1 for C1.** The E1 re-scoring of 15 published comparisons is POST_HOC (binding 1). No E1 number appears in the abstract or conclusions as a confirmed finding (binding 5).

## 4. Human validity

Both verdicts were computed before this map, under registrations committed before their first output. The abstract therefore uses the realized sentence only; the other outcome sentences do not apply.
- **LongCap-Arena.**
  - Rule: "(i) … OLS slope β_M < 0 and 95% CI upper bound < 0; (ii) … Δτ_b ≥ +0.10 and CI lower bound > 0; (iii) … acc_ceq − acc_cdiff > 0 and CI lower bound > 0. Overall verdict: PASS if all three tests pass, FAIL if none passes, otherwise MIXED."
  - Computed: (i) PASS, (ii) FAIL (kill fired), (iii) FAIL (kill fired). Verdict **MIXED** (`.session_backup/2026-10-15/r13_human/q2_longcap_arena.json :: verdict`).
- **VaPR.**
  - Rule: "PASS if the pass rule holds [the Wilson 95% lower bound of VaPR's count-matched share exceeds each comparator's share]. PARTIAL_POINT_ONLY if only the point estimate exceeds all three. FAIL otherwise."
  - Computed: **PASS** (`.session_backup/2026-10-15/r13_human/q4_vapr_count_control.json :: verdict`).
- **Abstract sentence (realized):** "On public human judgments the registered evidence is mixed: on LongCap-Arena, human Relevance falls with object count, but count-matched precision tracks Relevance worse than raw precision (Δτ_b = −0.028 [−0.036, −0.019]; registered verdict MIXED: 1 of 3 tests passed). A length- and style-matched preference set, VaPR, is mostly but not fully count-matched (registered positive control, PASS)."
- The registered kill on test (ii) withdraws only "better"; "worse" is allowed because the interval excludes 0 (`.session_backup/2026-10-15/r13_human/q2_longcap_arena.json :: test_ii_delta_tau.delta_tau` = −0.02763, `delta_tau_ci_95` = [−0.03611, −0.01864]; tests (i) PASS, (ii) and (iii) FAIL).
- Polaris, DOCCI-Critique, THumB and Composite are stage 1 (below). None of their verdicts appears in the abstract or conclusions as confirmatory.

## 5. Stage-1 labels (PD-10 binding 1; times from A4.4 `tests_status.tsv`)

| Test | Label | Evidence |
|---|---|---|
| Polaris (G2) | LOCALLY_FROZEN | prereg on disk 2026-10-14 15:37:51 < first output 16:25:48 < commit 7f22d13 16:47:58 (push 16:48:02) |
| DOCCI-Critique (G3) | LOCALLY_FROZEN | same file and times as Polaris |
| X1 P-B | LOCALLY_FROZEN | file 2026-10-14 04:12:41 < first output 05:57:56 < commit 6c647a6 07:01:40 (push 07:01:58) |
| L1 COCO-2500 | LOCALLY_FROZEN, never committed | `check_coco_PREDICTIONS.txt` mtime 07:22:14, sha256 c7cad2b2…3fb09; first output 07:25:31 |
| H3 N1 (English LVLM families) | LOCALLY_FROZEN, never committed | `N1_PREDICTIONS.txt` mtime 12:43:39, sha256 ba1f6bc7…fa58fa1a; first output 12:47:47 |
| H1 THumB/Composite | LOCALLY_FROZEN, never committed | `PREDICTIONS_FROZEN.txt` mtime 12:52:33, sha256 c09ed9a3…22538; first output 15:12:36 |
| E1 Holm survivors (15 published comparisons) | POST_HOC | first output 01:48:40 < protocol written 01:54:58 < commit 6c647a6 07:01:40. It is NOT "specified in timestamped files before analysis". |
| XM3600 N2 (adjacency) | POST_HOC | result quoted in its own prereg; first output 15:54:48 < commit 4ccbee3 16:38:04 |

- **X1 P-B** has no stage-2 test and stays exploratory everywhere.
- **Pins, PD-10 ruling (a)(i).** The full sha256 and mtime of the three never-committed files are in the JSON (`stage1.pins`); committing this map pins them. Under ruling (a)(iii), a copy with different content, or an mtime at or after the first output, makes that test POST_HOC.

## 6. Not mapped

- **B3** (registered ca644df, 2026-10-14 17:16:22 / 17:16:27; large-k reference sets, nocaps and PASCAL-50S; no output yet) carries no abstract-level claim here, on two conditions (judge, CC-029):
  - No B3 job is queued before a map amendment that sets B3's abstract and conclusion sentences is committed.
  - Any registered C2 test that completes, B3 included, enters §7.7 and §10.1 with its verdict as computed, failures included.
- **L6 D2** (registered 4812563, 2026-10-14 10:39:32, before its first output at 11:26:14; prediction FAILED, §9; A4.4 row L6_D2) carries no abstract-level claim of its own, but it is NOT independent of the conclusions. Its failure is the first half of §9's registered conjunctive kill; the second half is N9's K-b. Contribution 5 ("length matching does not remove this"), §9's "What the audit implies" and any §10 sentence carrying that claim depend on that kill: if K-b fires, they are withdrawn and Table 9.1 becomes description only (§3 modifiers); if N9 is NOT-TESTABLE, the paper says that the kill's second half could not be evaluated.
- Any verdict not named in §2–§4 does not enter the abstract or conclusions as confirmatory.
