# Paper A: mock IP&M review panel, round 2 (2026-10-21)

## What the panel read and how
- **Read in full:**
  - the abstract, highlights and keywords (outline.md:28–40);
  - sec1–sec11, declarations.md and appB_matcher_sensitivity.md;
  - supplementary.md, cover_letter_A.md and title_page_A.md;
  - paperA.bib and number_manifest.tsv.
- **Read as reviewers see it.** HTML comments were stripped with their newlines kept, so every file:line below matches the source file. Comments were used only to trace numbers.
- **Checked against source files.** Where a point depends on how a test was scored, the panel read the preregistration or evaluator directly:
  - `manuscript/prereg/2026-10-14_xm3600_predictions.md`;
  - `manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.md`;
  - `manuscript/prereg/2026-10-19_an1_g2b_addendum.md`;
  - `.session_backup/2026-10-14/r12_verify/evaluate_xm3600_predictions_v3.py` and `xm3600_full_verdict.json`;
  - `data/results/g2b/g2b_score.json`.

  A journal reviewer would not see these files. A reviewer who asks for the code would.

**Measured facts**
- **Prose words.** sec1–sec11 plus declarations: **11,611**. This counts visible words with comments removed, tables included and headings excluded. Because `wc -w` also counts table pipes and LaTeX tokens, this is an upper bound. Round 1 counted 12,556 by a different method.
- **Abstract:** 241 words. "Registered" appears 3 times (12 in round 1).
- **Highlights:** 82, 76, 81, 84 and 83 characters (all ≤ 85).
- **Clean-up since round 1:**
  - **Gone from the visible text:** TODO/PENDING markers, `[sX.YY]` source markers, commit hashes, "frozen locally" and "kill rule".
  - **Placeholders still visible:** 3.
- **Figures:** none.

**Totals for new issues: FATAL 1 · MAJOR 9 · MINOR 17.**
**Round-1 FATAL + MAJOR (27 items):** RESOLVED 5 · PARTLY 16 · OPEN 5 · NO LONGER APPLIES 1.

---

## 1. The three reviewers in brief

### R1: measurement and statistics
**Recommendation: major revision. Reject if the XM3600 scoring issue (N-F1) stands.**

The authors took round 1 seriously:
- The theory is now a "descriptive decomposition" (sec4_theory.md:1–3).
- The nested-gold caveat appears in the body (sec1_introduction.md:7, sec4_theory.md:42, sec7_verbosity_sign.md:68, sec11_limitations_ethics.md:23).
- A random-deletion null was added (sec7:68).
- Count control is exploratory everywhere.

What remains is the one confirmatory claim. The ordering half of that claim is admitted to be automatic. The weight therefore falls on "positive under complete gold". On the only image-out-of-sample sets, that endpoint is scored with a different precision rule from the lower rungs (N-F1). It also rests on a 160-token cap whose effect on the second backbone was never measured (N-M3).

### R2: vision–language hallucination evaluation
**Recommendation: major revision.**

**Strengths**
- The rescoring of released outputs is honest.
- The eight-LVLM rank reversal is the most useful practical result (sec7:72).

**Problems**
- "Complete gold" is never defined, and it means three different things (N-M1).
- Both backbones are Qwen models, and the cross-family per-model test failed (N-M9).
- Related work still lacks the obvious 2024–2026 validity and dense-caption benchmarks: HQM, CompreCap, DeCapBench, FaithScore, HalDec-Bench and DetailVerifyBench. Each was verified by the panel; see §4.

### R3: IP&M handling editor
**Recommendation: send to review, provided the visible placeholders are cleared. Expected outcome: major revision.**

**What improved**
- The desk-reject triggers of round 1 are mostly gone: no TODO markers, no internal codes in the main text, full declarations, and length under 12k.

**What remains**
- **Readability.** The abstract still reads as a test ledger (N-M6).
- **Placeholders.** Three remain visible:
  - sec11_limitations_ethics.md:43 "[AUTHOR TO CONFIRM: …]";
  - cover_letter_A.md:18 and declarations.md:15 "[AUTHOR TO PROVIDE]";
  - supplementary.md:1 "(draft)".
- **No figures.**
- **IP&M fit.** It rests on one IR sentence plus one clause in related work.
- **Provenance claim.** The cover letter's claim that every number is listed does not fully hold for the manifest (N-M8).

---

## 2. Status of every round-1 FATAL and MAJOR item

| ID | Status | Evidence (current text) |
|---|---|---|
| **AE-F1** unfinished / contradictory | **PARTLY** | "Pending/scheduled" wording is gone, and §7.6 is reported as done (sec7_verbosity_sign.md:59–72). The §10.6 "Open items" section is deleted. B3 is "registered, not run" (sec7:74–76). Still visible: sec11_limitations_ethics.md:43 "[AUTHOR TO CONFIRM: Polaris BSD; DOCCI-Critique CC BY 4.0]"; cover_letter_A.md:18 and declarations.md:15 "[AUTHOR TO PROVIDE]"; supplementary.md:1 "Supplementary Material (draft)". No longer fatal. |
| **AE-F2** undecodable jargon | **PARTLY** | The main text is decoded; the internal codes and the JSON keys in Table 7.1 are gone. Remaining: "NOT_SUPPORTED" (sec8_human_validity.md:76, sec10_discussion.md:6); raw model IDs "qwen3vl_8b", "idefics3_8b", "llava_ov_7b" (sec7:72, sec10:34); "cv295/uv231/xm600" used in Table 7.1 (sec7:15) before they are defined (sec7:62–64); "Q =" (sec7:70); "CHAIR-500" (sec6:45); recipe "P1" (sec7:43). The abstract is still a ledger (N-M6). |
| **R1-F1** theory non-discriminating | **PARTLY** (now MAJOR) | §4 is demoted to description (sec4:3). The caveat is stated: "the ordering is expected even if objects are missing from references at random" (sec4:42). A random-deletion null was added, labelled post hoc (sec7:68). Residual: the confirmatory claim's non-trivial half is the complete-gold endpoint, and see N-F1/N-M1 on that endpoint. The b-channel share is still from COCO-2500 only (sec4:56). |
| **R1-F2** count control unvalidated | **PARTLY** (now MAJOR) | Count is exploratory everywhere: sec1:9, sec6:3, highlight 3 (outline.md:30), abstract. Still open: the two-column standard and checklist item 3 are recommended practice on post hoc evidence (sec3:58–66, sec10:14, sec10:22). The stopping-method versus decoding split was not reported, yet one of the two survivors is the end-of-sequence method (supplementary.md:93). |
| **AE-M1** length | **RESOLVED** | 11,611 visible words (see method above). The live IP&M limit was not verified (outline.md:6). |
| **AE-M2** diffuse contribution | **PARTLY** | sec1:7 now states "Our one confirmatory claim". But 5 RQs (sec1:19–23) and 5 contributions (sec1:27–31) remain, and the abstract spends more words on secondary tests than on the claim. |
| **AE-M3** IP&M fit asserted | **PARTLY** | There is still one IR sentence (sec1:3) and one clause plus Lu et al. 2016 (sec2:9). The cover letter's fit sentence is generic (cover_letter_A.md:13). The condensed-F1 test borrows Sakai's (2007) condensed lists without citing it (sec7:70). Fix: §4 of this file. |
| **AE-M4** no figures | **OPEN** | No figure in sec1–11. outline.md:100 says Fig. 4 already exists (`paperA_tasks/A3.3/fig4_v3.{pdf,png}`). |
| **R1-M1** family confounds | **OPEN** | No leave-one-system-out or within-prompt slopes anywhere. Mild help: in the G2-B temperature test (G2B-P3b), the exponent-equivalence parts PASS or are INCONCLUSIVE; only the intercept part FAILS (g2b_score.json). sec7:68 does not report this split. |
| **R1-M2** token cap / harness | **PARTLY** | The cap is disclosed, but "how many of them reached it was not recorded" (sec7:61). Harness agreement of 6.4% is disclosed (sec7:72). The placebo run in the failed harness is disclosed (sec6:37). The cap-hit share is still unknown (N-M3). |
| **R1-M3** image reuse / clean subsets | **RESOLVED** | cv295 is described as all discovery images (sec7:62), and xm600 = the §7.5 images, "outcome … known" (sec7:64). The clean subset is defined (sec7:66). |
| **R1-M4** cross-lingual matcher | **OPEN** | There is no Vietnamese-lexicon perturbation; App. B perturbs only the English side (appB_matcher_sensitivity.md:5). The lexicon is "documented in the companion paper" (supplementary.md:74), which is unavailable. The UIT-ViIC sign still flips with the matcher (sec7:12–13, sec7:35). |
| **R1-M5** lenient rules / post hoc emphasis | **PARTLY** | The demotion rule is reported as registered (sec7:53). The abstract still says "the same 600 images as Section 7.5 are the informative set" (outline.md:40). The asymmetric "FAIL … whose interval includes 0" wording remains (sec7:72, sec8:76), now explained as the registered rule. |
| **R1-M6** thin margins / self-certified | **PARTLY** | Margins are stated (sec7:25, sec8:7). Third-party timestamps: Zenodo DOI not yet given (declarations.md:15). This cannot be fixed retroactively (c). |
| **R1-M7** human tests see 1–2 objects; multiplicity | **PARTLY** | The limitation is stated (sec8:13, sec8:72, sec8:82, sec11:27). There is still no multiplicity accounting across the paper, and sec3:52 contradicts the G2-B registration (N-M5). |
| **R2-M1** HQM missing | **OPEN** | Not in paperA.bib or the text. Verified: arXiv 2406.17115, "Measuring the Measurers: Quality Evaluation of Hallucination Benchmarks for Large Vision-Language Models" (2024-06-24). |
| **R2-M2** LeHaCE delta | **PARTLY** | It is positioned: "the closest prior work in method … Our controls instead match the number of mentioned objects per image exactly" (sec2:7). No head-to-head on the 15 comparisons. |
| **R2-M3** theory delta small | **NO LONGER APPLIES** | The theory is no longer claimed as a contribution beyond description (sec1:7 "it is not what the tests confirm"; sec1:27). |
| **R2-M4** detailed-caption benchmarks | **OPEN** | CompreCap, DeCapBench, FaithScore, HalDec-Bench and DetailVerifyBench are absent. There is no transfer argument for open-vocabulary or atomic-fact scoring. sec11:31 still limits "complete" to COCO-80. |
| **R2-M5** exchangeability positive in companion | **PARTLY** | The TODO is gone. Flickr30k is admitted as "(we did not trace the cause)" (sec5:35). The single-writer case is still only in the companion: "reported in a companion manuscript in preparation" (sec5:38, sec1:11). |
| **R3-M1** declarations missing | **RESOLVED** | Present: ethics, data/code, related manuscript, competing interests, funding, CRediT (declarations.md:9–31). The DOI placeholder is counted under AE-F1. |
| **R3-M2** registration verifiability | **PARTLY** | A Zenodo archive with commit times is promised (declarations.md:15); the DOI is not filled. |
| **R3-M3** number manifest | **PARTLY** | The manifest is referenced (sec3:54, cover_letter_A.md:17, supplementary.md:246) and has 655 rows. Rows are stale or unsourced (N-M8). |
| **R3-M4** licences | **PARTLY** | THumB/Composite: "we report aggregates only" (sec11:43). The placeholder remains (sec11:43), while sec8:66 states "CC BY 4.0" as fact. CapArena is dropped for having no licence (sec8:11) while the equally unlicensed THumB/Composite are used, and the difference is not explained. COCO, Flickr30k, XM3600/Open Images, UIT-ViIC and six preference sets carry no stated licence (sec9:11–17 names only VaPR). |
| **R3-M5** decode reproducibility | **PARTLY** | N9 settings are given (sec6:45). G2-B temperatures, top-p, seeds and software versions appear nowhere in the visible text. sec7:61 says only "three temperatures"; the values are in the prereg (§3). |
| **R3-M6** companion disclosure | **RESOLVED** | declarations.md:17–19; cover_letter_A.md:23. |
| **R3-M7** AI declaration | **RESOLVED** | Tools, purpose and oversight are named (declarations.md:7). sec3:54 states the provenance rules. Optional: add model versions. |

---

## 3. New issues

### FATAL

**N-F1 (R1, R2). On XM3600, the "complete gold" endpoint is scored with condensed precision, its gold is smaller than the reference gold, and neither fact is disclosed.** This stays FATAL until the bound below is reported.
- **Where:**
  - sec7_verbosity_sign.md:43–49 and :14–15;
  - sec1:7, sec4:42 ("Because the golds are nested");
  - outline.md:28 (highlight 1) and outline.md:40;
  - cover_letter_A.md:10.
- **The problem**
  - **The score changes at the top rung.** The XM3600 evaluator computes OIV7 precision as verified-present / (verified-present + verified-absent) (`evaluate_xm3600_predictions_v3.py`, `vp = div(t[:,1], t[:,1]+t[:,2])`). Mentions with no OIV7 verification are dropped from the denominator. The G2-B preregistration (line 130: "P = verified precision over verified mapped mentions") and the condensed-F1 addendum (line 27: "whose precision is already condensed") confirm this for xm600. So the top rung of the "ordering by completeness" changes the scoring rule as well as the gold.
  - **Detailed captions often lose more mentions.** The share of verifiable mentions ranges from 43% to 70% across the six systems (xm3600_full_verdict.json, `verifiable_share`). Detailed minus short:

    | Prompt pair | Detailed − short verifiable share |
    |---|---|
    | zero-shot | −20.65 [−23.85, −17.52] |
    | fuse2 | −5.11 [−7.31, −2.77] |
    | p1_s43 | +1.10 [−1.13, +3.47] (no drop) |

    Dropping unjudged mentions can bias the slope upward if they are less often correct than judged mentions. That is plausible, because hallucinated objects are rarely OIV7 verification candidates, but it is not measured. The lower bound below tests it.
  - **The OIV7 gold is not more complete in size.** Mean gold size is 2.04 classes per image for OIV7 against 2.35 for the union of the references (xm3600_predictions.md:41–43). The two golds are not nested.
  - **This cuts both ways.** Because the golds are not nested, the top rung's ordering is not automatic under random missingness, so it is more informative than the reference rungs. The damage is different: completeness is not the factor that changes at that rung, and the scoring rule is.
  - **What follows.** The only image-out-of-sample support for the confirmatory claim (XM3600 on both backbones) is therefore not a test of "more complete gold". cv295 uses COCO instance labels and is unaffected, but it is a replication on discovery images (sec7:62).
- **Fix (CPU, existing outputs; label it post hoc):**
  - Report the verifiable share per system.
  - Re-score the OIV7 rung twice: unverified mapped mentions counted as false positives (lower bound), and as dropped (current).
  - Report mean gold size per rung.
  - If the lower-bound slope stays above 0, the claim survives with a stated bound. If not, the confirmatory claim on XM3600 must be restated as "positive under verified-label scoring".
  - Either way, call the rung "verified-label gold (unjudged mentions dropped)" in §7.5, Table 7.1, the abstract and highlight 1, and remove "nested" for that rung.

### MAJOR

**N-M1 (R2). "Complete gold" is undefined and means different things on different sets.**
- **Where:** sec3_measurement_setup.md:5–9 (three gold families, none called "complete"); sec7:3, sec7:66; sec1:7; outline.md:28.
- **Problem.** In G2-B, "complete" means:
  - COCO instance classes only, not instance + references, on cv295 and uv231;
  - OIV7 verified labels on xm600 (G2-B prereg §5).

  Instance gold is not a superset of the reference gold, so sec4:42's "the golds are nested" holds only for the k-reference rungs. sec11:31 admits the COCO-80 limit but not the non-nesting.
- **Fix:** Define "complete gold" per set in §3.1. State that only the k-reference rungs are nested. Have the random-deletion null cover the reference rungs, as it now does ("on the references' own complete-gold objects", sec7:68).

**N-M2 (R3). The headline omits the caveat that the body repeats.**
- **Where:** outline.md:28 (highlight 1); outline.md:40 (abstract); cover_letter_A.md:10.
- **Problem.** Each says the slope "is ordered by gold completeness" as a confirmed result. None says that the ordering would also appear under random missingness. The body says so five times: sec1:7, sec4:42, sec7:68, sec10:5, sec11:23. A reviewer reading only the front matter gets a stronger claim than the evidence.
- **Fix:** Add one clause to the abstract and cover letter: "(an ordering expected under nested golds; the registered content is the positive complete-gold endpoint)". Reword highlight 1 so that it leads with the endpoint.

**N-M3 (R1). The token cap is used to excuse a failure but not examined for the pass.**
- **Where:** sec10_discussion.md:34; sec7:72 versus sec7:61.
- **Problem.** The conclusion explains qwen3vl_8b's failed ladder with "every detailed caption of that model reached the 160-token cap". The same model, with the same cap, is the second backbone of the confirmatory test, yet "how many of them reached it was not recorded" (sec7:61). The two harnesses agree on only 6.4% of detailed captions (sec7:72). A capped M on the detailed half of a 6-system family shapes the slope.
- **Fix (CPU):** Re-tokenize the saved G2-B detailed captions with the pinned processor and report the cap-hit share per run. Re-fit the slopes on short-prompt systems only, and with leave-one-system-out. Label all of this post hoc. Alternatively, drop the cap remark from sec10:34.

**N-M4 (R1). The supplementary gives a different set of registered predictions for the second-backbone test from §7.6.**
- **Where:** supplementary.md:169–174 versus sec7:66–68.
- **Problem**
  - **Supplementary S4** lists "Registered predictions of the second-backbone test, in the wording of its original protocol": a b-difference primary endpoint (P1–P4), a K2 rule counting "2 or more of 3 backbones", and P2 across three backbones.
  - **§7.6** lists four different primary claims (one-reference sign, complete-gold sign, slope ordering, exponent ordering). These are the claims registered in G2-B (prereg §9: G2B-E1, E2, O1, P1).
  - **The gap.** The paper never says that G2-B superseded the earlier protocol or what changed, although the prereg lists the departures (§12). A reader will see possible outcome switching.
- **Fix:** Replace supplementary.md:169–174 with the G2-B wording and verdict rules (prereg §8–§10). Add the departures list (§12) and the "what the author saw before registering" list (§13).

**N-M5 (R1). The multiplicity statement contradicts the registrations.**
- **Where:** sec3_measurement_setup.md:52.
- **Problem**
  - sec3:52 says "Families of tests are Holm-corrected". The G2-B registration says "multiplicity: No correction; every prediction is reported separately" (prereg §8).
  - §7.5 and §7.6 report uncorrected intervals without saying so.
  - Across the paper there are dozens of verdicts, with no count of the tests run.
- **Fix:**
  - Say in §3.6 which families are Holm-corrected; only §6 is.
  - State that the registered tests in §7 and §8 are uncorrected, as registered.
  - Add the count of registered verdicts to Table 11.1 (PASS / FAIL / INCONCLUSIVE). This is wording only. Most primary intervals in §7.6 are far from 0, so the conclusions would not change.

**N-M6 (R3). The abstract is still a ledger, and three of its phrases are wrong or unclear.**
- **Where:** outline.md:40.
- **Problems**
  - **(a)** "second backbone, development images": the body calls them "discovery images" (sec7:62) and runs the condensed-F1 test on all three sets (sec7:70).
  - **(b)** "the same 600 images as Section 7.5 are the informative set": §7.6 does not say this. Registered support required cv295 as well (sec7:70: "support required a pass on cv295 as well"), so singling out the passing set is post hoc emphasis.
  - **(c)** "(fidelity check: failed; seed placebo: selected the matched prefix; its runs were not scored by the analysis cut-off)": the reader cannot tell whose runs were not scored. sec6:37 reports a placebo result.
  - **(d)** It cites "Section 7.5" twice; an abstract should stand alone.
  - **(e)** It omits the eight-LVLM rank reversal (sec7:72), which the conclusion features (sec10:34) and which is the clearest practical result.
- **Fix:** Rewrite the abstract in five plain sentences:
  1. the problem;
  2. the confirmed endpoint, with its caveat;
  3. the rank reversal across eight LVLMs, with the per-model failure;
  4. count matching as exploratory, with the 12 → 2–6 curve;
  5. the human evidence.

  Keep every number the confirmation map fixes. This needs the map amendment noted in REVIEW_TRIAGE_PLAN_2026-10-20.md:31.

**N-M7 (R1, R3). The negative one-reference slope is called both a prediction and an observation.**
- **Where:**
  - "an observation, not a prediction": sec1:7, sec7:3, sec4:54, sec11:23;
  - outline.md:40: "an empirical observation the theory does not predict";
  - highlight 2 (outline.md:29) leads with it.
- **Problem.** It was a registered prediction that passed: N1-XM-1 (sec7:46) and G2B-E1, a primary claim on all three sets (sec7:66–68). Readers will not know whether it is confirmed.
- **Fix:** Use one phrase everywhere: "registered and confirmed as an empirical regularity; not derived from the decomposition".

**N-M8 (R3). The cover letter's "every number" claim does not match the manifest.**
- **Where:** cover_letter_A.md:17 ("Every number in the paper is read by script … and listed"); sec3:54 rule (i).
- **Problem.** number_manifest.tsv contains:
  - **Stale rows.** 4 Paper-A rows are still `pending` with "prereg … to be committed": N9, K2, G2-B, B3.
  - **Unsourced rows.** 4 rows, among them "200 (abstract word target)".
  - **Rounding mismatches.** Values are rounded differently from the text: τ_b "−0.29" against the text's −0.286 (sec7:72); slope "−1.12" against −1.124.
  - **Mixed papers.** Paper B rows (`B`) are in the same file.
- **Fix:**
  - Regenerate the manifest for Paper A only.
  - Mark the 4 pending rows resolved, with their sources.
  - Match the precision used in the text.
  - Soften the cover letter to "every number in the main text and the supplement".

**N-M9 (R2). The generality of the claim is untested beyond one model family.**
- **Where:** sec7:43 and sec7:61; sec7:72; sec11:29.
- **Problem**
  - **One family.** Both backbones are Qwen (Qwen2.5-VL-7B, Qwen3-VL-8B). sec1:7 and sec10:34 say "a second backbone" without noting this.
  - **The cross-family test failed.** The eight-LVLM test failed its per-model prediction (sec7:72).
  - **The ranking test is lenient.** Its PASS rule, "upper bound below 0.9", passes on cv295 with τ_b −0.286 [−0.571, 0.000], so it is weak evidence; state the rule's leniency.
  - **The English families failed.** The English LVLM families, with seven backbones, failed their positive-slope predictions (sec7:29).
- **Fix:** Scope the claim as "for the Qwen-VL family; the eight-LVLM test supports the rank reversal but not the per-model pattern". Name the family in the abstract.
- **Optional, GPU:** a non-Qwen backbone on xm600. Costly; flag only.

### MINOR

Reviewer tags: R1 for items 2–4 and 9; R2 for 5 and 14; R3 for all others.

1. **sec11_limitations_ethics.md:25 contradicts the main human result.** It says "judges were near count-neutral (Section 8.2)". sec8:17 and sec8:80 say humans penalize count on long captions, and highlight 4 says the same. Fix: "on short COCO captions".
2. **sec9_preference_audit.md:27: "the statement stands".** The registered prediction failed, and the second half of the withdrawal rule could not be evaluated. Fix: "unresolved; Table 9.1 is descriptive. The VaPR control (registered, PASS) is the only registered support".
3. **sec6:37 and sec3:38: the placebo logic is not explained.** The placebo ran in a harness that failed its fidelity check, yet it is said to "calibrate" the control. Explain why a within-harness seed difference can calibrate a paired control even when absolute CHAIR is off by 1.49.
4. **sec7:68: the random-deletion null is hard to follow.**
   - "−14.40" sits next to the primary slope of −11.46 without a definition.
   - "all eight set-by-level cells" includes a fourth set (the §7.5 first-backbone outputs) that is never named.

   Fix: define the statistic, list the eight cells, and add a small table to S7.
5. **The OPERA-on-Shikra result appears twice with two intervals.** sec6:29 gives −1.23 [−2.42, −0.08] against beam search; supplementary.md:97 gives −1.23 [−2.62, +0.08] against greedy. Name the baseline in both places. Also soften sec6:29, "the whole raw gain, and more, comes from naming fewer objects", which is a causal reading of a post hoc analysis.
6. **Undefined labels.** "NOT_SUPPORTED" (sec8:76, sec10:6) → "not supported". "Q =" (sec7:70) → define it. Model IDs (sec7:72, sec10:34) → product names. "Confirmation map" (sec7:68) → define it or delete it. "CHAIR-500" (sec6:45) → "the 500 CHAIR images of Section 6.1". The "gold-SFT recipe P1" (sec7:43, supplementary.md:274) clashes with predictions P1–P4.
7. **Set codes are used before they are defined.** Table 7.1 uses cv295/uv231/xm600 (sec7:15); they are defined at sec7:62–64. Also, "the same 600 images as Section 7.5" appears 11 times. Define "XM600" once.
8. **Table 7.1's second-backbone row merges three sets and leaves out values.** It omits the all-references slopes ("Section 7.6", which gives only differences). The G2-B registration (§11) asks for one row per set with the all-references cell. §7.6 also lists "the ordering of the exponent" as a primary claim but reports no b values (sec7:66–68).
9. **The bootstrap B is not stated where it differs.** sec3:52 says "B = 5000 unless stated", but G2-B used 1,000 draws (prereg §7) and XM3600 used 500 (xm3600_predictions.md:53). Neither §7.5 nor §7.6 states its B.
10. **Broken cross-references.** "Section 4.5" at supplementary.md:97 and :199; §4 ends at 4.3.
11. **Supplementary structure.**
    - The title says "(draft)" (supplementary.md:1).
    - Paragraphs are filed under the wrong sections. S6 "Numbers manifest" holds the DOCCI limits, the VaPR control and the licences (supplementary.md:250–266). S4 holds proposition text and the XM3600 design (supplementary.md:123, :151).
    - Run-on sentence: supplementary.md:274, "…COCO instance labels COCO-2500 is the discovery set".
    - An unverified statement is printed: supplementary.md:310, "*Post hoc note (… not verified by us)*". Either verify it or delete it.
12. **declarations.md:19 has the wrong referent.** "Its XM3600 results" reads as the companion manuscript's results. Use "This paper's", as cover_letter_A.md:23 does.
13. **Highlight 5 (outline.md:32) overclaims.** "checks whether caption references come from separate writers" does not fit this paper's evidence: Flickr30k has independent workers yet sits above the null (sec5:35), and the single-writer case is in the companion. Fix: "flags non-exchangeable reference order".
14. **Condensed F1 has no source citation (sec7:70).** It is Sakai's condensed-list idea; cite Sakai (2007), verified in §4. This also helps AE-M3.
15. **sec3:38 points to the wrong section.** "assumption A2; Section 4.3": A2 is defined in §4.1.
16. **sec8:66 versus sec11:43: licence stated as fact before it is confirmed.** sec8:66 states DOCCI-Critique "CC BY 4.0" as fact before the authors have confirmed it (sec11:43). Make the two agree after confirming.
17. **Decode settings missing from the paper.** The G2-B temperatures (0, 0.5, 0.8; prereg §6), top-p 0.95, seed 42 and bf16 (prereg §3) appear only in the prereg. Add them to S2 (this is R3-M5).

---

## 4. Related work: verified gaps and IR framing

The panel checked each item on its primary record (arXiv abs page or Crossref) on 2026-10-21.

| Work | Identifier | Why it matters |
|---|---|---|
| Yan et al., "Measuring the Measurers: Quality Evaluation of Hallucination Benchmarks for LVLMs" (HQM) | arXiv 2406.17115 | The direct validity-of-benchmarks precedent. Required. |
| CompreCap, "Benchmarking LVLMs via Directed Scene Graph for Comprehensive Image Captioning" (CVPR 2025) | doi 10.1109/cvpr52734.2025.01827 | Denser gold for detailed captions. |
| DeCapBench / DCScore, "Painting with Words" | arXiv 2503.07906 | Unit-level precision and recall on detailed captions. |
| FaithScore (Findings of EMNLP 2024) | doi 10.18653/v1/2024.findings-emnlp.290 | Atomic-fact hallucination scoring. |
| HalDec-Bench | arXiv 2511.20515 | Hallucination detectors in captioning. |
| DetailVerifyBench | arXiv 2604.05623 | Dense hallucination localization in long captions. |
| Sakai, "Alternatives to Bpref" (SIGIR 2007) | doi 10.1145/1277741.1277756 | The source of the condensed-list idea used in sec7:70. IR fit. |
| Yilmaz & Aslam, "Estimating average precision with incomplete and imperfect judgments" (CIKM 2006) | doi 10.1145/1183614.1183633 | IR evaluation under incomplete judgments. IR fit. |
| Zobel, "How reliable are the results of large-scale IR experiments?" (SIGIR 1998) | doi 10.1145/290941.291014 | Pool bias. IR fit. |

**Possible gaps, not re-verified this round:** NOPE and HallusionBench (round 1 gave DOIs; the panel did not re-check them).

**Suggested framing.** A short paragraph in sec2 ("Thresholds, F-measures and incomplete gold") would place gold completeness explicitly as the captioning analogue of incomplete relevance judgments. Using Buckley & Voorhees (already cited), Sakai, Yilmaz & Aslam and Zobel, it would turn the IP&M fit into an argument. About 120 words.

---

## 5. Can a reader follow the main claim?

**Mostly yes in §1, but not from the front matter.**
- **§1 works.** sec1:7 states one confirmatory claim with its caveats, and §11.1 repeats it consistently.
- **The front matter does not.**
  - The abstract buries the claim under four secondary results (N-M6).
  - The highlights state the ordering without its caveat (N-M2).
  - "Complete gold" is never defined (N-M1).
- **The numbers agree.** The panel spot-checked slopes, CIs and counts across the abstract, sec1, sec7, sec10, sec11 and the cover letter. They agree, apart from the rounding issues in N-M8 and the two Shikra baselines (minor 5).

---

## 6. Panel recommendation

| Outcome | Probability |
|---|---|
| Desk reject | 0.15 |
| Reject after review | 0.30 |
| Major revision | 0.48 |
| Minor revision | 0.06 |
| Accept | 0.01 |

**Reasoning**
- **Desk-reject risk.** It fell sharply since round 1, whose editor recommended desk reject. What remains comes from the visible placeholders, the ledger-style abstract and the absence of figures.
- **Reject risk.** It is driven by N-F1: an R2 or R1 who asks for the evaluator will find that the XM3600 top rung changes the precision rule.
- **If N-F1 is fixed.** If the post hoc bound shows the slope stays positive, and the claim is worded as in N-M1/N-M2, major revision becomes the clear modal outcome (about 0.6).

## 7. Five highest-value fixes before submission

1. **XM3600 verified-label rescoring (CPU, existing outputs; N-F1, N-M1).**
   - Report the verifiable share and gold size per rung.
   - Re-score OIV7 with unverified mentions as false positives (lower bound).
   - Define "complete gold" per set, and limit "nested" to the reference rungs.
   - Reword highlight 1, the abstract and §7.5 to match the result.
2. **Second-backbone robustness (CPU, label post hoc; N-M3, R1-M1, R1-M2).**
   - Recover the 160-token cap-hit share by re-tokenizing the saved detailed captions.
   - Add short-only, leave-one-system-out and within-prompt slopes.
   - Remove the asymmetric use of the cap in sec10:34.
3. **Rewrite the abstract, highlights and cover letter (N-M2, N-M6, N-M7, N-M9).**
   - Five plain sentences, with the random-missingness caveat.
   - "Discovery", not "development".
   - Drop "informative set".
   - Fix the placebo parenthetical.
   - Add the eight-LVLM rank reversal.
   - One label for the one-reference sign.
   - Name the Qwen family.
4. **Make the registration record consistent (N-M4, N-M5, N-M8, AE-F1).**
   - Replace supplementary.md:169–174 with the G2-B wording and its departures list.
   - Correct the Holm statement in sec3:52.
   - Regenerate a Paper-A-only manifest with no pending rows.
   - Clear the three visible placeholders, "(draft)" and the "Section 4.5" references.
5. **Related work, IP&M fit and figures (R2-M1, R2-M4, AE-M3, AE-M4; CPU or writing only).**
   - Add HQM, CompreCap, DeCapBench, FaithScore, HalDec-Bench and DetailVerifyBench, with a transfer paragraph.
   - Add the Sakai / Yilmaz & Aslam / Zobel IR framing.
   - Add Fig. 2 (slope by gold, all families) and the existing Fig. 4.

**Optional and costly (GPU):** a non-Qwen backbone on xm600 (N-M9). This is not on the critical path.
