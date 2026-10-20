# Paper A: mock IP&M review panel (2026-10-20)

Scope: the panel read only what a reviewer receives: the abstract (outline.md:40), sec1–sec11, declarations.md, supplementary.md, appB_matcher_sensitivity.md and paperA.bib, all with HTML comments removed. The line numbers below are the original files' numbers; removing the comments did not shift any line. Quotes are verbatim and at most 25 words.

Measured facts used below:
- Prose words, sec1–sec11 + declarations, comments removed (tables included): **12,556**. Supplementary + App. B: 7,938.
- Abstract: 246 words; "registered" appears 12 times.
- Visible text has **49 distinct internal codes**, "frozen locally" ×29, "kill rule" ×8 and 5 commit hashes.
- Supplementary has 48 visible `[sX.YY, from secN.md…; old §…]` markers and 10 TODO/PENDING lines.
- The paper has no figures.

Totals: **FATAL 4 · MAJOR 23 · MINOR 17.**

---

## 1. Associate editor: desk-reject screen

**Recommendation: desk reject (return without review).** The manuscript is visibly unfinished: it has placeholders and contradicts itself on which results exist. Its abstract is a test ledger written in internal codes.

### FATAL
- **AE-F1. Unfinished, and it contradicts itself on what has been done.**
  - The second-backbone test is reported as passed in the abstract and §7.6 but as pending in six places:
    - sec1_introduction.md:7 "a registered second-backbone test is scheduled (Section 7.6)"
    - sec1_introduction.md:29 "a second-backbone test is pending"
    - sec7_verbosity_sign.md:3 "G2-B and B3 are registered and pending"
    - sec10_discussion.md:7 "A second-backbone test is pending"
    - sec10_discussion.md:47
    - sec11_limitations_ethics.md:23
  - The K2 placebo is unrun in one place and has a result in another: sec3_measurement_setup.md:38 "(TODO: E1 K2 placebo not yet run; D17 §1(c))" against sec6:39 "The prediction held". supplementary.md:137 says "Registered seed placebo (K2): pending." while supplementary.md:135 says "[Resolved in the cut pass…]".
  - Open placeholders:
    - sec10_discussion.md:49–51, a section titled "Open items before submission" containing "[PENDING items…]"
    - sec7_verbosity_sign.md:94 "[PENDING: B3 large-$k$…]"
    - sec1_introduction.md:15 "(Paper B, under review; TODO citation)"
    - sec1_introduction.md:30 "(TODO: N9; Section 6.4)"
    - declarations.md:7 "[TODO authors: confirm product names and versions]"
- **AE-F2. A reader cannot decode the abstract or the main text.**
  - outline.md:40 (abstract): "registered seed placebo: selected matched_prefix; its runs were not scored by the freeze"; "XM600 is the informative set"; "the registered demotion rule did not fire".
  - Twelve uses of "registered" in 246 words, and no plain sentence stating what the paper finds.
  - Codes in the main text include:
    - sec4_theory.md:58 "Under CC-007"
    - sec7_verbosity_sign.md:82 "The kill rules K1, K2 (restricted form), K3, KN1, KL and KD apply"
    - sec7_verbosity_sign.md:88 "By kill rule KA2"
    - sec3_measurement_setup.md:27 "(primary; PD-2 Q1)"
    - sec5_exchangeability.md:44 "(H4 §1a)"
    - sec6_rescoring_published_methods.md:49 "(L6 §3 D1; registered in b8b2500)"
  - The Source column of Table 7.1 shows internal JSON keys: sec7_verbosity_sign.md:11 "C1J `check_coco_gold.*`".
  - The supplementary shows 48 source-map markers, e.g. supplementary.md:9 "[s3.20, from sec3_measurement_setup.md:46–48; CAR decomposition, old §3.5]", and internal paths, e.g. supplementary.md:135 ".session_backup/2026-10-13/decisions/PD-15.txt".

### MAJOR
- **AE-M1. Over the length limit.** The main text has 12,556 words against IP&M's ~12,000, before any decoding of the jargon, which will add words. A further 7.9k words sit in the supplementary.
- **AE-M2. The contribution is diffuse and hedged.** The paper has 5 RQs, 5 contributions and 3 threats, plus human-validity and preference audits. Each contribution is qualified:
  - sec1_introduction.md:29 "two of five predictions failed; COCO-2500 agrees (exploratory); a second-backbone test is pending"
  - sec1_introduction.md:30 "Applied post hoc, under a protocol written after a pilot"
  
  There is no single headline claim.
- **AE-M3. The IP&M fit is asserted, not made.** The link to IR evaluation under incomplete judgments, which would justify the venue, is one clause: sec2_related_work.md:9 "incomplete relevance judgments bias evaluation measures (Buckley and Voorhees, 2004)". As written, the paper reads like a CV/ACL paper.
- **AE-M4. No figures in a paper about slopes and a frontier.** sec4_theory.md:58 cites "(Fig. 4)", but no figure exists. Fixable by plotting existing outputs on CPU.

### MINOR
- outline.md:21–26: four title options remain and none is chosen.
- Two numbering schemes for tables: sec6_rescoring_published_methods.md:17 "**Table 6.1** (paper Tab. 2)"; sec8:27 "(Tab. 5)"; sec11:5 "**Tab. 7**".
- sec7_verbosity_sign.md:80 "exposure possible)..": double full stop.
- sec7_verbosity_sign.md:84 "after all 23 decodes": this does not square with "6 systems per set" × 3 sets (sec7:17).
- Commit hashes in the running text: sec7_verbosity_sign.md:58 "committed in 4ccbee3"; also 0932ba1, 7254a39 and ca644df.
- sec8_human_validity.md:78: the heading "8.4b" is not a numbering a journal accepts.

---

## 2. R1: methods and statistics

**Recommendation: reject.** The registered tests of the theory confirm predictions that would hold without it, and the risky predictions failed. The count control was never validated: the registered count tests failed or were not scored. The second-backbone family is confounded by a token cap and by harness drift.

### FATAL
- **R1-F1. The theory's confirmed predictions do not discriminate, and its risky predictions failed.**
  - The golds are nested, and the paper says the Ḡ-channel "exists under any missingness" (sec4_theory.md:42). The ordering in k and a positive endpoint at large gold are therefore expected even under SCAR (random) missingness, so their "registered confirmation" does not test the propensity model.
  - The predictions that could have failed did fail:
    - the multi-reference sign: sec4_theory.md:62 "predictions of a positive all-references slope failed on two English LVLM families … and on XM3600"
    - sign agreement: sec7_verbosity_sign.md:69 "N1-XM-5: FAIL"
    - transfer of the optimum: sec7_verbosity_sign.md:72 "the crossing lies at a more complete gold, which the transferred exponent missed"
  - The closed form gives the wrong sign at k=1: sec4_theory.md:56 "in 88% of bootstrap replicates $\Lambda_U(1) > 0$ while the slope is negative".
  - The XM3600 one-reference pass came about through a different route than predicted: sec7_verbosity_sign.md:72 "did not come about through the mechanism the prereg gave".
  - The paper's practical headline is that one reference gives a negative slope, so a pair can be "ranked in opposite orders" (sec1_introduction.md:5). That observation is outside the theory: outline.md:40 "an empirical observation the theory does not predict".
  - The only model-specific evidence, the b-channel share, is post hoc and on COCO-2500 only (sec4_theory.md:60). As confirmatory theory, the 1,075 words of §4 plus S1 do not earn their place.
- **R1-F2. RQ2 has no confirmatory support, and the count control is not validated.**
  - Every registered or frozen test of count control failed or was not scored:
    - N9: sec6_rescoring_published_methods.md:47 "N9 was not scored"
    - X1: sec6:43 "killed the claim"
    - LongCap-Arena: sec8_human_validity.md:20 "Count-matched precision tracks Relevance better than raw precision: FAIL"
    - THumB/Composite P1b: sec8:32 "failed ×2"
  - The construct-validity defence is asserted (sec3_measurement_setup.md:67 "its justification is construct validity, not agreement with human judges"), but no evidence supports it.
  - The matched prefix treats a legitimate shift of operating point (stopping before uncertain mentions) as "not choosing objects better" (sec1_introduction.md:9). For the 4 stopping-method comparisons (sec6:7), the baseline's prefix nearly equals the method's output by construction, so part of the "count effect" is tautological.
  - The headline overstates this: sec6_rescoring_published_methods.md:29 "**Most of the raw gain is a count effect.**" The spread across controls is 2/15 to 6/15, and K4 triggers under the random subset (sec6:35).
  - The paper's main practical recommendation, the two-column standard, therefore rests on a post hoc analysis only.

### MAJOR
- **R1-M1. The frontier "families" mix count with other changes.**
  - G2-B's six systems are one model at "three temperatures, two prompts" (sec7_verbosity_sign.md:80). Temperature changes hallucination rate (s_m), not only M, so it strains (A3). The detailed prompt changes style as well as count.
  - The slope is OLS over 6–11 points, and its interval "is conditional on the systems" (sec3_measurement_setup.md:56). The image bootstrap ignores system-level variance.
  - Required: leave-one-system-out and within-prompt slopes.
- **R1-M2. Token cap and harness drift.**
  - sec7_verbosity_sign.md:88 "All of qwen3vl_8b's and idefics3_8b's detailed captions reached the registered 160-token cap". Truncation censors M and removes the late, low-propensity mentions, which is exactly the tail that (A2) and the slope depend on.
  - The share of G2-B decodes that hit the cap is not reported.
  - The same model gives opposite results under two harnesses: sec7_verbosity_sign.md:88 "agree on only 6.4% (cv295)". In A-N2, qwen3vl_8b "fails the complete-gold part" while it passes in G2-B.
  - The K2 placebo that admits the matched prefix ran "inside the N9 harness" (supplementary.md:138), whose fidelity check failed (sec6_rescoring_published_methods.md:47 "|ΔCHAIR_i| = 1.49 > 1.0").
- **R1-M3. Images reused across tests, and exclusions not defined.**
  - The abstract (outline.md:40) says the second backbone was tested "on … 295 discovery images", but the body describes them only as "COCO val2017 (295 images outside train2017)" (sec7_verbosity_sign.md:80). The overlap with COCO-2500 is not disclosed.
  - xm600 appears to be the same 600 XM3600 images as §7.5 (sec7:58), and those results were seen before the G2-B prereg.
  - "Clean subsets (263 of 295, 209 of 231 and 537 of 600 images)" (sec7:84) are never defined.
- **R1-M4. Matching across languages.**
  - COCO-2500 consists of "Vietnamese captions mapped to COCO-80 and scored against the English references" (sec4_theory.md:46). Lexicon errors scale with the number of mentions, so they load onto the slope.
  - On UIT-ViIC the five-reference sign flips with the matcher (sec7_verbosity_sign.md:50, Table 7.1 rows 14–15: +4.80 vs −6.28).
  - The sensitivity analysis swaps only the English reference-side extractor (appB_matcher_sensitivity.md:5) and does not perturb the Vietnamese lexicon.
- **R1-M5. Lenient kill rules and post hoc emphasis.**
  - The XM3600 demotion fires only "if 2 or more of N1-XM-1 to N1-XM-3 fail" (sec7_verbosity_sign.md:62).
  - "XM600 is the informative set" (outline.md:40) singles out the favourable set after a MIXED outcome.
  - Verdict labels are applied asymmetrically: "a FAIL under the registered 'point ≤ 0' rule whose interval includes 0" (sec7:88, sec8:80).
- **R1-M6. Registration margins are thin, and registration is self-certified.**
  - Margins: sec7_verbosity_sign.md:26 "three minutes before the first output, never committed"; sec8_human_validity.md:7 "committed after the first results file (by 22 minutes)".
  - The registration rests on hashes in the authors' own repository; there is no third-party registry.
- **R1-M7. The human-validity tests see almost nothing.**
  - sec8_human_validity.md:13 "finds 1.23 classes per caption on average (median 1)"; DOCCI has 1.50 (sec8:76).
  - On long captions, the count tests therefore run on one or two objects.
  - LongCap (iii) pairs captions of different images (sec8:21).
  - Across the paper there are dozens of tests with no overall accounting of multiplicity.

### MINOR
- sec3_measurement_setup.md:11: recall is macro-averaged while precision is micro-averaged ("mixed F1"), and the theory is exact only for micro-F1. Headline numbers use mixed F1.
- Bootstrap B varies without stated reason: sec3:52 "$B = 5000$", sec4:58 "$B$ = 2,000", sec8:5 "2,000-draw".
- sec7_verbosity_sign.md:84: the secondary G2-B predictions are buried: "P3b is INCONCLUSIVE on cv295 and FAILS on uv231 and xm600".
- sec11_limitations_ethics.md:45 "This matters more for absolute truthfulness than for the measurement properties": this is asserted. Exposure could change which mentions come late, and so the salience order.

---

## 3. R2: prior work and novelty

**Recommendation: major revision.** The genuinely new pieces are:
- a per-image exact count match applied to released outputs;
- the gold-indexed sign of F1's verbosity reward;
- a cheap test of exchangeability.

Each is narrower than claimed. The paper frames itself as a measurement-validity study but omits the main hallucination-benchmark validity work.

### MAJOR
- **R2-M1. HQM is missing.** "Measuring the Measurers: Quality Evaluation of Hallucination Benchmarks for LVLMs" (Yan et al., 2024; arXiv 2406.17115, doi 10.48550/arxiv.2406.17115) assesses the reliability and validity of hallucination benchmarks, including alignment with humans. It is absent from paperA.bib, yet the paper is framed as a validity study: sec1_introduction.md:3 "Like any measurement, these scores can respond to properties of the instrument". A reviewer will require positioning against it.
- **R2-M2. The count/length confound is established, and the delta over it is undemonstrated.**
  - Prior work: LeHaCE (Wei et al., NeurIPS 2024, doi 10.52202/079017-3538), CCEval, Fazli et al. 2026 (arXiv 2609.01888), Long et al. 2026 (arXiv 2609.35294) and Sandhu et al. 2026.
  - The paper's claim is sec1_introduction.md:9 "That measurement is our contribution", but no head-to-head is reported.
  - Demand: run a LeHaCE-style length-curve control on the same 15 comparisons, and show that the conclusions differ from the per-image match.
- **R2-M3. The theory adds little to its cited sources.**
  - sec1_introduction.md:7 "we add the monotonicity in $k$, the single crossing and the two-channel split", on top of Lipton et al. (2014) and Chen et al. (2015, §4.2).
  - Given R1-F1, a reviewer will rate this a modest extension.
  - Gold incompleteness is also well trodden: Buckley & Voorhees 2004; ImageNet ReaL; RePOPE; COCO-ReM; Long et al. 2026.
- **R2-M4. No test on modern detailed-caption benchmarks that score with denser gold.**
  - Candidates: CompreCap (CVPR 2025, doi 10.1109/cvpr52734.2025.01827), DCScore/DeCapBench (arXiv 2503.07906), DetailVerifyBench (arXiv 2604.05623), HalDec-Bench (arXiv 2511.20515), FaithScore (doi 10.18653/v1/2024.findings-emnlp.290).
  - None is cited. sec11_limitations_ethics.md:31 limits "complete" gold to COCO-80.
  - Demand at least an argument for why the sign result transfers to open-vocabulary or atomic-fact scoring (ALOHa and OpenCHAIR are cited but not analysed).
- **R2-M5. The exchangeability contribution's positive finding is in an unavailable companion paper.**
  - sec1_introduction.md:13 "a single-writer corpus does not (companion paper)".
  - Within this paper, every independent corpus sits at the null except Flickr30k, which is unexplained: sec5_exchangeability.md:31 "file order by length? [TODO: trace length-by-position numbers]".

### MINOR
- M-HalDetect (Gunjal et al., AAAI 2024, doi 10.1609/aaai.v38i16.29771) is used in sec8_human_validity.md:80 "M-HalDetect human span labels" but is not in paperA.bib.
- NOPE (doi 10.18653/v1/2024.alvr-1.4) and HallusionBench (doi 10.1109/cvpr52733.2024.01363) are not positioned. They are less central, but expected in a related-work section.
- sec2_related_work.md:7 "Closest in aim, Fazli et al. (2026)": the "closest" prior works are 2026 arXiv preprints, so the novelty claims depend on unrefereed readings. Quote their claims cautiously.
- sec9_preference_audit.md:29 "the length channel in preference data is prior work": the preference audit is descriptive and limited to COCO-80. As a contribution it is thin.

---

## 4. R3: reproducibility, licences, ethics, AI use

**Recommendation: major revision.**
- Required declarations are missing, and several licences are still TODO.
- Registration cannot be verified by a third party.
- Decoding is not reproducible across the authors' own harnesses.
- The paper admits that AI agents produced unsupported numbers, while the manifest that would answer this is still a TODO.

### MAJOR
- **R3-M1. Required declarations are missing.** declarations.md:1–12 contains only the AI declaration. There is no data-availability statement, code-availability statement, competing-interests statement, funding statement or CRediT statement.
- **R3-M2. Registration cannot be verified.**
  - sec3_measurement_setup.md:54 "A prediction counts as registered only if it was committed to version control before the first output". The commits are in a private repository and no URL is given.
  - Git history can be rewritten. No OSF/AsPredicted or Zenodo timestamp is given.
- **R3-M3. Number provenance.**
  - sec3_measurement_setup.md:54 "their prose and logs repeatedly contained numbers that existed in no output file". The safeguard is still a TODO: "(TODO: `manuscript/number_manifest.tsv`, H6 P1)".
  - Reviewers will demand the manifest, the code and the JSON outputs at submission.
- **R3-M4. Licences.**
  - sec11_limitations_ethics.md:43 "TODO: confirm the Polaris (BSD) and DOCCI-Critique (CC BY 4.0) licences."
  - THumB/Composite "ship without a licence file" (sec11:43) yet are used, while CapArena "was dropped because no licence statement … could be found" (sec8_human_validity.md:11). The standard is applied inconsistently.
  - sec11:37 "TODO: written confirmation from the authors (PD-2 Q4)."
  - Licences are not stated for XM3600/Open Images, COCO, Flickr30k, UIT-ViIC, KTVIC, or the seven preference sets (sec9_preference_audit.md:11–17).
- **R3-M5. Decoding is not reproducible.**
  - sec6_rescoring_published_methods.md:47 "3.6% of the 500 base captions match those exactly".
  - sec7_verbosity_sign.md:88 "agree on only 6.4% (cv295)".
  - Missing from the main text: G2-B temperatures, seeds, max tokens and software versions.
- **R3-M6. Companion submission.** sec1_introduction.md:15 "(Paper B, under review; TODO citation)". Elsevier requires related manuscripts under consideration to be disclosed and supplied to the editor. Shared data (KTVIC, the adapters) raises a question of overlap.
- **R3-M7. The AI declaration is incomplete.**
  - declarations.md:7 "[TODO authors: confirm product names and versions]".
  - declarations.md:8 "to draft and edit the manuscript text". Elsevier's current policy allows this, but asks for the tool name, its purpose and the level of human oversight.
  - Given R3-M3, the editor will expect an explicit statement of how every number in the text was verified.

### MINOR
- No ethics statement saying that no human subjects were involved and no IRB approval was needed. sec8_human_validity.md:3 "We collected no new annotation" implies it but does not say it.
- sec8_human_validity.md:80 "CC BY-NC 4.0, research use; the download is pinned by sha256": good practice. Apply the same pinning to every dataset.
- appB_matcher_sensitivity.md:7 "the copied code reproduces the cited values exactly": "copied code" is unexplained. Name the release and its version.

---

## Triage (FATAL and MAJOR)

(a) = fixable by rewriting only · (b) = fixable by CPU analysis on existing data · (c) = not fixable; reframe as a limitation.

| Issue | Fix | Note |
|---|---|---|
| AE-F1 unfinished / contradictory | (a) | Sync every "pending" with §7.6; delete §10.6, TODO and PENDING. B3 is either dropped or kept as a limitation. |
| AE-F2 jargon / internal codes | (a) | Decode all 49 codes; strip the S-markers, JSON keys and hashes; rewrite the abstract in plain claims. |
| AE-M1 length | (a) | Decoding will push it longer; the cut has to come from §6.4, §8.4b, §9 and §7.6 secondaries. |
| AE-M2 diffuse contribution | (a) | |
| AE-M3 IP&M fit | (a) | |
| AE-M4 no figures | (b) | |
| R1-F1 theory non-discriminating / failed | (b) + (a) | SCAR random-deletion null on the existing outputs; b-channel share on the XM3600 and G2-B outputs; demote §4 to a descriptive decomposition. The failed predictions stay (c). |
| R1-F2 count control unvalidated | (a) + (c) | Present RQ2 as exploratory. Split the stopping-method comparisons from the decoding ones (b). No confirmatory count claim is possible (N9 is dead). |
| R1-M1 family confounds | (b) | Leave-one-system-out and within-prompt slopes; system-level resampling. |
| R1-M2 token cap / harness | (b) + (c) | Report the cap-hit share for G2-B. Re-fit after excluding truncated captions, or after truncating all captions to a common token budget. Harness drift and K2-in-N9 stay (c). |
| R1-M3 image reuse / undefined subsets | (a) + (b) | Disclose the overlaps, define "clean", and report G2-B on images disjoint from COCO-2500 and from §7.5. |
| R1-M4 cross-lingual matcher | (b) | Vietnamese-lexicon perturbation; English-caption-only family as the primary. |
| R1-M5 lenient kill rules / emphasis | (a) | |
| R1-M6 thin margins / self-certified registration | (c) | |
| R1-M7 human tests see 1–2 objects | (c) | |
| R2-M1 HQM | (a) | |
| R2-M2 LeHaCE head-to-head | (b) | |
| R2-M3 theory delta | (a) | |
| R2-M4 detailed-caption benchmarks | (a) | Argue transfer; an applied test would need new scoring, which is out of scope. |
| R2-M5 exchangeability positive in companion paper | (a) + (c) | Trace Flickr30k length by position (b). |
| R3-M1 declarations | (a) | |
| R3-M2 registration verifiability | (a) + (c) | Deposit the repository snapshot with a DOI now; timestamps from before submission cannot be proven. |
| R3-M3 numbers manifest | (a) | The file exists. Reference it and release it. |
| R3-M4 licences | (a) | Drop THumB/Composite if consistency with CapArena is required. |
| R3-M5 decode reproducibility | (a) + (c) | |
| R3-M6 companion disclosure | (a) | |
| R3-M7 AI declaration | (a) | |

## The single change most likely to move the outcome to "major revision"

**Re-scope Paper A around one confirmatory claim, cleaned of internal codes:** "the sign of object F1's verbosity reward depends on gold completeness".
- Support it with the registered XM3600 test and G2-B, with the image reuse disclosed, the 160-token cap handled, and a SCAR random-deletion null showing the ordering is not automatic. The null and the cap re-fit are CPU work on existing outputs.
- Demote the theory to a descriptive decomposition.
- Present count matching and the human and preference audits as exploratory.

Rewritten this way, the desk-reject risk (AE-F1/F2) is gone, and R1's reject reason becomes a revisable scope dispute.
