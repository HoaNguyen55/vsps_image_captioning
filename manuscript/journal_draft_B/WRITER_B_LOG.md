# B-writer log (Paper B, journal_draft_B)

Sessions 2026-10-18 and 2026-10-19 (resume after the 21:57Z stop). Nothing was committed: commits go only through the gatekeeper. Every new number in the text has a src comment and a manifest row whose value is read by key and display-checked (`update_manifest.py`).

## 1. Ladder wording (W8 Amendment 1, A4.4)
- sec4.3 states the only registered joint criterion (2026-10-12, 1b5d16b; MET). It corrects the addendum margins to ±1.0 per run and ±0.8 pooled (the addendum, l.34). The draft had "±1.0 and ±2.0", but ±2.0 is in neither file and is descriptive. The ladder TOST is labelled POST_HOC.
- Timing (main, A4.2/A4.4): the earliest registered ladder output is fuse2_s44-detailed at 2026-10-12T12:27:19Z (re-checked by file mtime). The addendum reached disk at 2026-10-14T15:54:52Z and was committed in 4ccbee3 at 16:38:04Z. The earlier "p1ep4 13:39Z" is replaced.
- sec5.2: 4/6 runs inside all intervals (cons_s42-short P OUT; fuse2_s43-detailed M OUT, 3.2545 vs [3.054, 3.254]), counted in code. The registered criterion is MET. The ±0.8 TOST FAILS (90% CI −0.9877 < −0.8). The pooled ±1.0/±2.0 results are EXPLORATORY. Runs 56–58 stay PENDING until verified and scored by prereg_ladder_check, and no new GPU output was used.
- Overclaims fixed: sec1:17 ("equivalent within ±1.0"); sec5 "what the ladder says"; sec7.2; sec8.1. I also checked that no landed run has ci95[0] > 0.

## 2. Gemini prose errors
None of the four is present in sec1–sec8. Residual forms were fixed (see 1). Matcher v3 is labelled unattested throughout, and the "v3 sign-off" PENDING row is DROPPED (no new annotation). No "typicality vs truth" wording.

## 3. XM3600 period effect
- sec3.3: appending a period gives +2.71 [2.23, 3.21] (P1 s43) and +2.75 [2.32, 3.20] (fuse2 s42), from `xm3600_period_cider_decomposition_v1.json` (sha 410097af) :: cross_system_drop_decompositions_token_level.*.drop_decomposition.by_append_period_to_ft_pred.cider_shift_x100. No percentage of the drop explained is used.
- Independent recompute (this is a Gemini-produced file): scratchpad `writerB/recompute_xm3600_period_shift.py` (sha cd36b9a0…) uses the GPU-M2 monitor's own CIDEr-D (score_vi.py) with RDRSegmenter. The as-written CIDEr-D equals the committed values, and the point and paired-bootstrap CI (B = 10000, seed 42) equal the key's to 4 dp. Output `xm3600_period_shift_recompute.json` sha 41794e68…, all_pass = true.
- Also fixed: "XM3600 references, which are punctuated". Only 217 of 1,227 (17.69%) end with a period (recounted). With the period appended, both systems still score below zero-shot, and the rest of the drop is not decomposed. sec8 XM3600 limitation updated.

## 4. Resource framing
- sec3.7 is now the release kit and data availability, with Table 3.1: scorer/protocol card, matchers v1–v3 and lexicons (v3 unattested), split and ID lists, two-gold protocol, audit scripts, results and manifest. "Not released": images, captions, OpenViIC-derived files. Checkpoints are on request until licences are confirmed (D2).
- sec7.4 (new) maps recommendations 1–7 to kit components. Old 7.4 → 7.5. A sec3 intro line was added. The sec1 kit bullet and framing sentence were rejected by the user at the pause and NOT re-applied.
- Wording checked against the repo: result files record segmenter, tokenisation and scale, but not the CIDEr variant or punctuation policy. The KTVIC–OpenViIC overlap list is not released (only the matcher).

## 5. WiSE-FT
- 10-18: marked NOT_RUN. 10-19: the gate is VERIFIED (data/results/wise_ft_gate.json sha 93eb8e67; byte-identical A-verifier re-run, PD11_rerun_record.json).
- New sec6.6 with Table 6.2. Guard not binding (no α passes 140.7), so α* = 0.75 is chosen on UIT-ViIC val F1 alone. ΔF1 is −1.49 [−2.58, −0.47] at α 0.75 and −4.25 [−5.59, −2.98] at α 0.5. Not futile; the follow-up SFT has not run. No KTVIC test number is presented as a held-out estimate.
- PD-14 N12-D2 sentence pasted VERBATIM. The four addendum reporting items (l.64–67) are marked [PENDING-WISE-ADDENDUM] in text, table and manifest.
- PD-11 sentence pasted VERBATIM into the new sec4.6 deviations table (Table 4.1); status REGISTERED. PD-11 condition 5: the KTVIC-test guard is flagged in sec8.1.

## Coordinator corrections applied
- D-W13-6 / A4.4 labels (verbatim, with times):
  - kNN: LOCALLY_FROZEN, exploratory. Its rule outcome, recomputed from the keys, is SECONDARY_POSITIVE_OR_INCONCLUSIVE, so "KILL" is dropped everywhere, including the outline.
  - EV-RANK: POST_HOC. Its "gate for M3" was removed; M3 = Tier-3 S3 (a68fb66, not run).
  - PLAN-F1: NOT_RUN, no verdict; its CPU critique is POST_HOC.
  - M4 C2: LOCALLY_FROZEN.
  - Ladder TOST: POST_HOC; pooled ±1.0/±2.0 EXPLORATORY.
  - UPE and the RL gate: REGISTERED, with push-after-output disclosed.
  - All 9 A4.4 B rows are fixed, including the 3 rows in journal_draft/paperB_outline.md (:19, :24, :84) plus :90 (main's instruction).
- PD-10 (b): P-M6b is REGISTERED for look 1 only.
  - Registered row: pool7_T05 / KTVIC gold / M6 / concat, +0.65 [+0.02, +1.27], p = 0.044. KILL by the "< +0.8" clause (M6/REPORT.txt:200).
  - Clustered CI: POST_HOC robustness check.
  - Row counts: 12 registered and 12 post hoc, none pass (counted in code).
  - Disclosures: no prereg file; 44 s; 5 h on disk; the 07:06Z prose bug; the pools were already scored for UPE (2026-10-13T02:28:54Z, ba351f8).
- B2 findings (text only; no B2 number used):
  - c8 UIT-ViIC 94.29% and +1.29 [0.85, 1.77] withdrawn. Replaced by the raw count 1,133 of 1,155 (98.10%), recounted. The effect is PENDING.
  - "148.3" is not present in B.
  - UPE kill 2 is restated as the registered panel-precision rule on 2 of 3 seeds, with P values from the primary JSON. The RL rule is cited from rl_gate_v2.md:147–152; the guard alone decided it.
  - G1: the "0.0 on every seed" claim was false (seed 44 CIDEr diff 2.8e-14). Text now gives exact diffs and PASS.
  - Fig. 2: B-only variant, as a placeholder comment only.
- CC-024: UIT-ViIC test = COCO train2017 and XM3600 = Open Images, both "exposure possible" (sec2, sec3.1, sec5.3, Table 6.2). No B text relied on unseen images.
- No-OpenViIC correction: no B text applied the 401/558 caveat to our models. sec3.6 now cites b_n2_inventory.json and ERRATA, and keeps the overlap for OpenViIC-trained, published/zero-shot and two-panel uses.
- New registered items, placeholders only, no numbers: B-N1 (327191c) in sec5.1; B-N2 (not evaluable; placebo and descriptive gaps PENDING the judge) in sec3.6.
- T3-S3 disclosure (arm A token-mean CE vs A-KL per-sequence token-sum KL) is in sec4.5. Its source note `2026-10-18_tier3_S3_operations.md` is untracked.
- Also fixed: sec8 ViCLIP-OT "trained on KTVIC" → UIT-OpenViIC (CC-014 had missed sec8). Run-ID clash resolved (3B = 61/62).

## Not done / flagged to main
- sec1 kit bullet (user-rejected edit), so main decides. The new_vs_FAIR % has not been recomputed. The release-kit components still only in .session_backup are listed in STATUS.md. B2 numbers and figures await VERIFIED.

## File sha256 after edits (first 16 hex)
sec1 8c085c539767a363 · sec2 cd13c96dc3b802c3 · sec3 736b33a622b204ab · sec4 f0b99101cb0ca4be · sec5 e8fc9cb2390191e3 · sec6 af57a0a5112e8506 · sec7 14d615bea1ac0e95 · sec8 116b170776b56d34 · outline_B 50e379b998b8b7dc · new_vs_FAIR 80ef89d2f80cdd02 · STATUS 886bb793c840f8a4 · number_manifest_B.tsv 5daca9eb7bf717c0 · journal_draft/paperB_outline.md 07c65128ea6af197.
Scratchpad (`/tmp/claude-1000/-mnt-d-vsps-image-captioning/755eae04-5e4c-4ce1-ab21-d4bc106761ee/scratchpad/writerB/`): apply_text_edits.py 2773dd9498ca8ff9 · apply_outline_edits.py 3ebc02963be719ba · update_manifest.py 9c20065952c0be7f · recompute_xm3600_period_shift.py cd36b9a0ed016156 · xm3600_period_shift_recompute.json 41794e6826f470de.

## Ladder result (2026-10-19; VERIFIED registered check) and judge PD-20
- Source: the registered check's `.session_backup/2026-10-18/ladder_check/final/stdout.txt` (sha 0477f26f), cited by line. Verification: `manuscript/verification/paperA/LADDER_CHECK_final.json` (be043f40, VERIFIED, byte-identical re-run). Values are parsed from stdout in code (`apply_ladder_result.py`), not typed.
- Table 5.2: rows 56–58 filled at the check's printed precision.
  - multiref_s42-short: all IN, +0.04 [−1.85, +2.01] (stdout:2).
  - unf2_s42-short: M OUT below (2.056 < 2.096), P and R IN, +0.46 [−1.18, +2.20] (stdout:4).
  - rnd2_s42-detailed: all IN, +0.71 [−1.02, +2.30] (stdout:5).
  - rnd2_s42-short: M OUT below (2.004 < 2.031), P and R IN, −0.02 [−1.95, +1.86] (stdout:6).
- Run count, counted in code: 6 of 10 landed runs are inside all intervals; it was 4 of 6. The joint 95% CI over 10 runs is [−0.90, +0.92] (stdout:11).
- The point −0.007 is labelled "computed from the printed per-run points (verification record LADDER_CHECK_final.json)". It is cited to rows[0].items.C2.evidence, and the check itself prints no point.
- Judge PD-20 (replaces the [PENDING-JUDGE] marker): the registered H0 (V4.txt:233-236; per-run clause l.235, pooled clause l.236; 1b5d16b) is a conjunction and is NOT met. The pooled part is met. The per-run part is not: 8 of 10 runs are within ±1.0 (counted in code), with p1ep4 −1.59 (stdout:1) and cons +1.44 (stdout:3).
- The judge's sentence is pasted VERBATIM under Table 5.2 and in the §5.2 text. Every earlier "criterion MET" or "invariance holds" claim is corrected in sec1, sec4.3 (H0 restated as the conjunction; the "only joint test" sentence removed), sec5 (pooled-frontier heading, interim six-run statement, "what the ladder says", Table 5.1 bullet), sec7.2, sec8 (ladder limits; AI-provenance item 3), outline_B, STATUS and the manifest. The resolution note (V4.txt:241-242) is quoted; it changes no verdict.
- The ±0.8 TOST stays POST_HOC and FAILS. It is labelled as computed on the six runs landed before the reruns and not recomputed. The per-run M/P/R interval verdicts are reported as their own registered set.
- Manifest: +34 rows (stdout values, interval bounds, CI, counts, the −0.007 point) and +6 rows (8 of 10, −1.59, +1.44, the H0 bounds 1.0 and 0.8, the resolution ±2). The three ladder PENDING rows are now RESULT. The judge row records "not met" (PD-20). Total 462 rows.
- sha256 after edits (first 16 hex): sec1_intro.md d660340c18d9ab8e · sec4_system.md e731ab73e5e3ad75 · sec5_results.md 36ab017c1bd2e806 · sec7_discussion.md ae71aaf9de6026bd · sec8_limitations_ethics.md 8253325ed9bc973e · outline_B.md 46d1ac05723e3046 · STATUS.md 7c872aa32f0dd9ba · number_manifest_B.tsv 2528dd9a01bc7cfd · apply_ladder_result.py a693301f7fa4b180 · apply_pd20.py 445780c20923c2c4 

## Main edit 2026-10-19T05:00:02Z (judge PD-20 erratum)
- sec5_results.md: the verbatim PD-20 sentence's citation was changed from `2026-10-12_frontier_invariance_V4.txt:233-235` to `:233-236` at 2 sites, per the judge's erratum. No other change. sec5_results.md sha256 prefix after the edit: 0b5f48c139473486.

## Judge PD-21b (2026-10-19): B-N3 NOT_RUN; FAIR-2026 ratings support no claim
- No B-N3 placeholder existed, so one was added in sec8.1 after "No human judgments". It holds the judge's sentence VERBATIM, and no other statement about the raters or the FAIR paper.
- Source: `.session_backup/2026-10-19/HL_human_labels/b_n3_quality_gate.json` (sha 341bd115). Checked in code: n_items 150; 2 rater files; identical_share 0.713 / 0.867 / 0.813, so 71–87%; rule "exceeds 0.5"; STOP true.
- Search of sec1–sec8, outline_B, STATUS, new_vs_FAIR and number_manifest_B for human_eval, rater, rating, Likert and kappa:
  - No number or claim is drawn from the FAIR-2026 ratings, so nothing needed removing.
  - The κ hits are the UIT-ViIC transfer slope, and sec2's "rater-equivalence" is an unrelated citation.
  - new_vs_FAIR lists "human rating" only as a FAIR component that Paper B does not use. I left it unchanged; main may drop it.
- Manifest: +6 rows (2, 150, 71, 87, 50, B-N3 NOT_RUN). Outline and STATUS updated.
- sha256 after edits (first 16 hex): sec8_limitations_ethics.md 9debe5ba7d7682dd · outline_B.md 3291c43a91f31af0 · STATUS.md e9072fee96895e68 · number_manifest_B.tsv 008b68b94bbd9dc3 

## PD-24 rebuild (2026-10-20, B-writer)
- Main text = audit + protocol card + kit. Moved to `supplementary_B.md` (verdicts and src comments unchanged): ladder (old sec4.3, sec5.2, Table 5.1 residual column), second backbone and 3B (old sec4.4), B-N1 (old sec5:26), B-N2 detail (old sec3:60), UPE two estimators (old sec5.4), all of old sec6, old sec4:79 and sec4.6. sec1 lists every moved registered result in one line (codes in a comment).
- Renamed sec7_discussion.md → sec6_discussion.md and sec8_limitations_ethics.md → sec7_limitations_ethics.md (working tree only; index unstaged, nothing committed); sec6_negatives.md removed; sec8_conclusion.md new; abstract (249 words) at the top of outline_B.md.
- PD-24 (c): XM3600 CIDEr-D 48.39 / 41.17 / 38.61 and the UIT-ViIC slopes removed (manifest rows 46–48 REMOVED); sec1 / sec2 / sec7.3 now describe the companion paper correctly; Table 7.1 = A↔B overlap.
- PD-24 (b): kit = own code only, [AUTHOR TO CHOOSE LICENCE], Zenodo [AUTHOR TO PROVIDE]; "available on request" deleted; lexicons, predictions and weights not promised. Licences read on the Hugging Face model cards 2026-10-20: Qwen2.5-VL-3B-Instruct = Qwen Research License Agreement (non-commercial only); Qwen2.5-VL-7B-Instruct = Apache-2.0.
- S3 corrected to FAIL at every site (old sec4:79, sec6:34, outline, manifest row 318). Verbatim judge sentences (PD-20, PD-14) keep their wording; file:line, commit and run-ID locators moved into comments.
- Bib: paperB.bib rebuilt (39 entries), each matched by DOI/arXiv ID and checked via Crossref / arXiv APIs (RDRSegmenter via ACL Anthology L18-1410); citation_map_B.tsv regenerated (74 rows, all resolved). VES-RFT dropped (no DOI or arXiv record). FAIR 2026 and the companion paper cannot be checked externally.
- Checks: number conservation old→new (no visible number lost except bibliographic identifiers and section numbers); visible-text grep of sec1–sec8 for TODO, PENDING, PD-, CC-, KB1, LBB-, B-N, B-F1, D18, "kill rule", "Paper A", [VERIFY]: none.
- Word counts (comments stripped): main sec1–sec8 8,115; abstract 249; supplement 5,720.
- Advisor pass: Table 7.1 and sec1 now state that Paper A scores this paper's KTVIC-trained P1/fuse2 on XM3600 and its ten UIT-ViIC systems; kit scope narrowed (object-level audits need a lexicon not shipped); number manifest = reviewer supplementary material, not kit; "zero-shot guard"; B-N1 prediction wording checked against the 327191c prereg; citation audit 2 applied (R13_HaUI_traffic authors/issue, R13_2610_14976 IEEE Access DOI in r13_new_refs.bib; neither is cited by Paper B).
