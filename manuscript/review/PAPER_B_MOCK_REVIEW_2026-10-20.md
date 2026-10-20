# Paper B: mock LRE review panel (2026-10-20)

Manuscript: `journal_draft_B/` sec1–sec8 (HTML comments stripped), title from `outline_B.md`, `paperB.bib`, `new_vs_FAIR.md`. Title: *What a Vietnamese Captioning Benchmark Measures: A Controlled Fine-Tuned VLM and a Validity Audit of KTVIC*. Line numbers refer to the source files. Comments were stripped with their line breaks kept, so the numbering is unchanged.

Issue counts: AE 2 FATAL / 4 MAJOR / 3 MINOR; R1 1 / 7 / 3; R2 1 / 3 / 2; R3 1 / 3 / 2. **Total 5 FATAL, 17 MAJOR, 10 MINOR.**

---

## 1. Associate editor: desk-reject screen

**Scope.** An LRE submission fits when its core is a released resource or an evaluation methodology. Here the core is an audit of KTVIC plus an evaluation kit, which fits, but the paper does not present the kit as a resource and spends roughly 40% of its text on model-training negatives (§4.3–4.4, §5.2, §6).

**What is released?** Scripts, a scorer and protocol card, three matcher lexicons, split/ID lists and result files (sec3:68–77). No captions, no images; checkpoints "on request" (sec3:79). The kit has no URL, DOI, version, licence or documentation in the text.

**Length and readability.** About 12,600 words in sec1–8 (new_vs_FAIR.md:35 still says 7,669). The paper has no figures, no abstract and no conclusion section.

**Count of internal codes visible to a reader** (approximate grep over comment-stripped text):

| Item | Count |
|---|---|
| "registered"/"Registered" + "REGISTERED" | 89 + 17 |
| POST_HOC / LOCALLY_FROZEN / NOT_RUN labels | 10 / 4 / ≥3 |
| PENDING (incl. 6× `[PENDING-WISE-ADDENDUM]`) | 15 |
| "kill" / "kill rule" | 12 / 4 |
| "gate" | 41 |
| commit hashes (7-hex) | ≈28 |
| HH:MM:SS timestamps | ≈29 |
| PD-, CC-, D18, KB1, LBB-, B-N1/2/3, B-F1, N12-D2, M3/M4, EV-RANK, C3 | 2, 1, 2, 1, 5, 3, 1, 1, ≥4, 2, 1 |
| run IDs (52_a, 35_e, p1ep4_s42-short, …) | ≥9 |
| file:line citations in body text (`…V4.txt:233-236`) | 2 |
| TODO / [VERIFY] / [verified] tags | 3 / 2 / ≈20 |
| "Paper A" | 1 |

### FATAL
- **AE-F1. Incomplete submission.** There is no abstract or conclusion. Three TODOs remain: sec2:7 "TODO: read both in full before 2026-11-01"; sec3:56 "TODO: paired CI for the flip"; sec8:49 "TODO: adapt this subsection to the target venue's policy". About 15 PENDING markers remain, including the final-system test: sec6:113 "B-F1 (registration pending; its result goes in Section 5 once run)". An editor returns this without review.
- **AE-F2. The resource is not available or citable.** sec3:66 says "we release them as an evaluation kit", but no repository, DOI, licence or version is given anywhere. In addition, sec3:79 says "fine-tuned checkpoints are available on request". For LRE the released resource is the contribution; without it there is nothing to review.

### MAJOR
- **AE-M1. Internal lab notation throughout** (see the table above). Examples: sec5:16 "by kill rule KB1 we report its score shifts only"; sec3:62 "(judge rule CC-005)"; sec6:80 "Under the addendum's decision rule N12-D2 (ca644df)". A reader cannot resolve "judge rule".
- **AE-M2. The bibliography is unusable.** paperB.bib has 5 entries, but the text cites about 25 works (CIDEr, CHAIR, XM3600, GRIT, Qwen2.5-VL, QLoRA, VnCoreNLP, OpenViIC, HDUCap, ViG, SacreEOS, Berger et al., …). Reviewer-visible tags remain: sec2:5 "[VERIFY]" and sec2:11 "[VERIFY: technical report identifier]".
- **AE-M3. The contribution is unfocused.** sec1:16 "*A released evaluation kit*" is the first of six contributions (sec1:16–21), and the ladder, B1, WiSE-FT and §6.7b each need their own registration history. The title promises an audit; half the paper is a training-lever diary.
- **AE-M4. Process prose instead of science.** Examples: sec6:50 "pushed at 07:01:59Z, 44 s before look 1 began at 07:02:24Z"; sec4:55 "The addendum reached disk at 15:54Z". This belongs in a supplement.

### MINOR
- AE-m1. Stale overlap statistic: new_vs_FAIR.md:35 "7,669 in total across sec1–sec8".
- AE-m2. Section numbering "6.7b" (sec6:107).
- AE-m3. Internal names leak: sec5:78 "companion paper (Paper A)"; sec1:12/sec5:86 "(C3)".

**AE decision: return to authors without review (desk reject in this form). Reason: incomplete manuscript (no abstract, TODOs, pending final test), and the claimed resource has no access route or licence.**

---

## 2. R1: methods and statistics

### FATAL
- **R1-F1. The central empirical claims are either unresolved or pending, so the method half of the paper reports no verdict.**
  - The ladder H0 is not met: sec5:64 "the registered frontier-invariance H0 is not met".
  - B1 was aborted: sec4:67 "The 3B runs are **PENDING**".
  - The leakage test cannot be evaluated (sec3:60).
  - The punctuation fix does not re-rank the four models (sec5:16).
  - The final test is pending (sec6:113).
  - S3/M3 is contradictory (R1-M5).

  The negative-results framing (sec6:5) would be acceptable if the negatives were conclusive. Instead most are KILLs with CIs that include the effect of interest. Example: sec6:42 "+1.57 [−6.26, 9.55], below the registered pass threshold of +3.0". That is underpowered, not negative.

### MAJOR
- **R1-M1. The registered per-run clause cannot discriminate.** In Table 5.2 the per-run CI half-widths are about 1.8 (sec5:36 "−1.5946 [−3.4578, 0.2019]"), so SE ≈ 0.75–0.93. Under true invariance, P(|residual| > 1.0) ≈ 0.18–0.28 per run, so 2–3 of 10 runs are expected outside ±1.0. P(all 10 inside) ≈ 0.04–0.13: the registered conjunction fails 85–96% of the time even if H0 is true. "8 of 10 runs within ±1.0" (sec5:49) is what invariance predicts, so "NOT MET" is close to uninformative. The authors half-say this (sec5:59 "single-run claims cannot be resolved") but still headline the verdict. They should report the expected exceedance count, or reframe H0 as uninformative by design.
- **R1-M2. The single-writer test is confounded.** The 0.40 null (sec3:19) assumes exchangeable slots. But sec4:23 says "Slot 0 is the first caption typed and names fewer objects than later slots". A monotone slot-position trend alone raises adjacency above 0.40 and raises lag-1 Jaccard, with no paraphrase chaining involved. Two things are needed: (i) a permutation null that preserves per-slot inclusion rates; (ii) the same statistic on an independent-writer corpus (UIT-ViIC, XM3600) as a negative control. Without them, "each written with the previous one in view" (sec3:21) is unsupported.
- **R1-M3. The punctuation headline is a synthetic perturbation.**
  - The paper headlines "lowers CIDEr-D by 35.17 points" (sec1:10, sec7:10) on a model trained never to emit a period. The realistic effect on a punctuating system is +4.32: sec3:34 "28.98 as written and 33.30 with their final periods stripped".
  - On XM3600 the period accounts for +2.71 of a 7–10-point drop (sec3:38).
  - The −35 figure is a property of CIDEr's IDF on a degenerate vocabulary item, not a measured system difference. Lead with the stripped/unstripped deltas instead.
- **R1-M4. §7.1 is not a decomposition.** sec7:7 says "decompose a KTVIC CIDEr score into four parts". The parts are not additive. They are measured on different systems and directions (template: zero-shot→P1; punctuation: an appended period on P1; segmentation: a re-tokenisation of P1). In addition, sec7:14 "larger than most published differences between Vietnamese systems" is unsupported: the paper reports no published differences.
- **R1-M5. One experiment is reported both ways.**
  - sec4:79 says "count-matched DPO design (M3) is registered separately (commit a68fb66) and has not run", and sec6:34 says "It is **PENDING**".
  - But sec6:110 says "S3, count-matched DPO and rejection-sampling fine-tuning: FAIL. Every arm (A, R, A-KL) met a kill rule", with the same commit a68fb66 and the same arms.
- **R1-M6. The leaderboard is degenerate and its tense is inconsistent.** sec5:16 "will score public VLMs" is followed in the same paragraph by "Four models were scored". With 4 systems, "tau_b 1.0 [1.0, 1.0]" and "tau_b 0.667 [0.333, 0.667]" are bootstrap artefacts of n = 4 and support no rank statement. Rescoring published Vietnamese systems (GRIT, HDUCap, ViG) under the protocol card is what readers need, and sec8:21 says "No published Vietnamese system has been rescored".
- **R1-M7. It is unclear which system the paper is about.**
  - Table 5.1 (sec5:13–14) gives P1 145.8 vs P1-R 148.23 as the main system.
  - sec5:24 says "P1's seed 42 scored 149.79", which is higher than every P1-R seed.
  - sec6:113 then says MBR-3 "is the only lever carried into the single registered test evaluation of the final system".
  - Which system is the paper's? If MBR-3 becomes final, Table 5.1 changes.
  - "Residual" is defined on precision (sec4:47) but used on F1 (sec5:9, sec6:91).

### MINOR
- R1-m1. sec4:75 "reproduced the committed result file byte for byte" shows only that rescoring fixed predictions is deterministic, not that the training or decoding reproduces.
- R1-m2. The deviation table is incomplete. sec4:83 "Every disclosed deviation" omits two items: the S5 registered outcome that was not acted on (sec6:112 "The registered rule returned FUND_EXTERNAL_IMAGE_DATA. External data was not added"), and the S3 amendment 59901cc (sec6:109).
- R1-m3. The B-N3 stop rule reads backwards. sec8:15 says the ratings "exceeded our pre-set agreement gate (identical scores on 71–87% … threshold of 50%)", so high agreement caused a stop. Explain the rule, or drop the paragraph.

**R1 recommendation: reject (resubmission encouraged). Reason: the audit claims are interesting but the key test (single-writer) is confounded, and the method results are underpowered or unresolved and presented as verdicts.**

---

## 3. R2: prior work, novelty and overlap

### FATAL
- **R2-F1. Salami risk with the companion paper is real and under-disclosed.**
  - The text twice says the companion works on English and uses KTVIC "only as a motivating example": sec1:23 "develops the general theory of object-count confounding … on English benchmarks", and sec8:37.
  - Yet the same Vietnamese results are split between the two papers:
    - sec3:15 "The XM3600 evaluation and its pre-registration belong to the companion paper";
    - sec3:38 "the XM3600 scores are primary in the companion paper";
    - sec5:78 "The gold-completeness ordering of the verbosity slope on UIT-ViIC is reported in the companion paper (Paper A)", directly after printing those slopes (sec5:74–76);
    - sec5:80 "(companion paper, Section 11.1)".
  - Both papers share the count-matched frontier machinery (sec2:15).
  - new_vs_FAIR.md has an overlap table for FAIR only, none for the companion.
  - An editor will require the companion manuscript and a two-way overlap table. As written, a reviewer would suspect one study split across three venues (FAIR, companion, this paper).

### MAJOR
- **R2-M1. Novelty claims overlook close prior work on annotator effects and metric fragility:**
  - Geva et al. 2019, *Are we modeling the task or the annotator?* (EMNLP; doi 10.18653/v1/D19-1107). This is the canonical single-annotator-artefact paper, and it is not cited for §3.2.
  - Caglayan et al. 2020, *Curious case of language generation evaluation metrics: a cautionary tale* (COLING; doi 10.18653/v1/2020.coling-main.210). It covers metric sensitivity to trivial surface edits, which is directly relevant to §3.3.
  - Kasai et al. 2022, *Transparent Human Evaluation for Image Captioning* (NAACL; doi 10.18653/v1/2022.naacl-main.254). It documents reference-quality issues.
  - Hessel et al. 2021, CLIPScore (EMNLP; doi 10.18653/v1/2021.emnlp-main.595). It is the reference-free alternative, yet sec2:9 discusses only ViCLIP-OT.
  - van Miltenburg (2024), *Image captioning in different languages* (arXiv 2407.09495). It is the multilingual captioning-evaluation context.
- **R2-M2. The Vietnamese prior-work list is incomplete.**
  - Missing: the VLSP 2021 VieCap4H challenge (doi 10.25073/2588-1086/vnucsce.341) and its systems, an earlier shared benchmark that contradicts sec1:5 "three public benchmarks".
  - Missing: the 2026 Vietnamese scene-text captioning dataset (arXiv 2604.27712).
  - Missing: the OpenViIC arXiv version (2305.04166).
  - HDUCap (doi 10.1016/j.jvcir.2026.104963) and ViG (doi 10.1109/mapr72750.2026.11685699) are cited but unread. sec2:7 says "We could not read the full text of either paper". A reviewer will not accept unread closest work.
- **R2-M3. What is genuinely new is narrower than claimed.** sec2:13 "Our protocol card (Section 4.2) applies the same idea to Vietnamese": the idea is sacreBLEU/SacreEOS. Count-controlled object metrics are the companion's. CIDEr's IDF penalty for unseen n-grams is a known property. The new parts are: (i) the KTVIC single-writer finding, if it survives R1-M2; (ii) KTVIC's punctuation convention and the cross-corpus effect; (iii) the KTVIC–OpenViIC 401/558 overlap; (iv) the *cây*/tone matcher audit. That is a solid short resource paper, not the six-contribution paper of sec1:16–21.

### MINOR
- R2-m1. Check the OpenViIC volume year. sec1:5/sec2:5 say "Signal Processing: Image Communication 140:117430, 2026"; OpenAlex gives an online date of 2025-10-31 for vol. 140. Cite whichever year the volume carries.
- R2-m2. The overlap figures are inconsistent. sec1:12 says "About two thirds … (401 of 558 …)", but 401/558 = 71.86% (sec3:60). sec3:13 and sec5:88 say "555 of the 558", so the "157 images without an OpenViIC copy" (sec3:60) lack only a *training-split* copy. State both numbers once, with split names.

**R2 recommendation: major revision, conditional on the editor accepting the companion-paper overlap. Reason: a real, useful audit core, but the novelty is inflated, the closest annotator-artefact and metric-fragility work is missing, and the three-way split must be justified.**

---

## 4. R3: reproducibility, data licences, ethics, AI-use

### FATAL
- **R3-F1. Rights to the evaluated data and to derivatives are not established.**
  - sec3:79 says "KTVIC ships no licence file". Without a licence, default copyright applies, and the paper still proposes releasing derivatives: the lexicons built from KTVIC training counts (sec3:52), "committed predictions" (sec3:66) from a model trained to reproduce KTVIC text (sec6:42 reports 2.25% exact copies for RL), and on-request checkpoints.
  - UIT-ViIC and UIT-OpenViIC are, to this reviewer's knowledge, distributed by the UIT group on request under research-use agreements. The authors must state the terms they obtained the data under and whether those terms allow the derived artefacts and the aggregate scores. The reviewer could not confirm the terms.
  - The fallback backbone Qwen2.5-VL-3B is under the *Qwen Research* licence (Hugging Face model card: `license_name: qwen-research`), not the Apache-2.0 of the 7B, and this affects any release of 3B adapters.
  - The authors need written permission from the KTVIC authors or a statement of terms. Without it, the kit cannot be published as described.

### MAJOR
- **R3-M1. Reproducibility of generation is not shown.** Only rescoring is reproduced (sec4:75–77). The paper gives no hardware, library versions, decoding seeds, training time or GPU budget per run (only B1 gets one: sec4:65 "7.0–8.0 GPU-h"). It also mentions a machine failure (sec4:57 "Runs 56–58 were lost to a machine failure and rerun") without showing that the reruns match their originals.
- **R3-M2. The OpenViIC handling cannot be checked.** sec3:81 says "Every released file is scanned for 8-gram overlap with OpenViIC captions … the scan must find none". Neither the scan's result nor its script is reported, and the exclusion of 8-grams that also occur in KTVIC or common Vietnamese is not defined. Aggregate scores against a dataset whose terms are not stated (R3-F1) remain a use of that dataset.
- **R3-M3. The AI-use disclosure is incomplete and self-damaging.**
  - sec8:41 says "Much of the analysis code and many intermediate reports were produced by AI coding agents (two different assistants)". The assistants are not named, and the section does not say whether the manuscript text was AI-drafted, which Springer's policy requires.
  - The same paragraph says agent prose "contained numbers that existed in no output file". This invites the question of how many numbers in *this* text were checked by a human. The manifest (sec8:43) is not part of the submission package as described.
  - The v3 matcher rules were drafted by an AI model (sec3:52), so they need the same disclosure in the methods section, not only in limitations.

### MINOR
- R3-m1. Ethics, people in images. sec8:33 says "No identity recognition is performed". The paper does not discuss gender nouns in references and outputs, although matcher rules for "role and gender nouns" exist and FAIR's gender neutralisation is excluded (new_vs_FAIR.md:15).
- R3-m2. COCO-exposure caveats are repeated five times (sec2:5, sec3:11, sec3:15, sec5:68, sec6:66). State the caveat once, with a quantitative contamination check where possible.

**R3 recommendation: major revision. Reason: the release cannot go ahead until the data rights are settled; reproducibility covers scoring only; the AI-use statement is unfinished.**

---

## 5. Triage of FATAL and MAJOR issues

(a) = rewriting; (b) = CPU analysis on existing data; (c) = not fixable, so it becomes a limitation or a reframing.

| Issue | Fix | Note |
|---|---|---|
| AE-F1 incomplete (abstract, TODOs, PENDING, B-F1) | (a) + (c) | Write the abstract and conclusion; delete TODOs. Drop pending items or move them to "future work". B-F1 is a GPU run: submit only after it lands, or cut MBR-3 from the paper. |
| AE-F2 no access route or licence for the kit | (a) | Archive on Zenodo with a DOI and a code licence (e.g. MIT/Apache); add a data-availability statement. Checkpoints: (c) until R3-F1 is settled. |
| AE-M1 internal codes | (a) | Replace with plain prose; move registration times and commits to a supplementary table. |
| AE-M2 bibliography | (a) | Merge the full bib; resolve the [VERIFY] tags. |
| AE-M3 unfocused | (a)/(c) | Reframe (see §6). |
| AE-M4 process prose | (a) | Move to the supplement. |
| R1-F1 method results unresolved | (c) | Cannot be made positive. Reframe: the ladder, B1, the leaderboard and §6 become a supplementary "what failed and why" record, not contributions. |
| R1-M1 per-run clause uninformative | (b) | Compute the expected exceedance count from the reported SEs; state that H0 was miscalibrated by design. |
| R1-M2 exchangeability confound | (b) | Slot-rate-preserving permutation null on KTVIC, plus the same statistic on UIT-ViIC and XM3600 references. CPU only, existing data. |
| R1-M3 synthetic −35 headline | (a) + (b) | Lead with strip/append deltas on punctuating systems (zero-shot, 4 leaderboard VLMs); measure the UIT-ViIC period effect, which is still PENDING (sec3:36). |
| R1-M4 non-additive "decomposition" | (a) | Call it "four sources of variation", drop "most published differences", or (b) tabulate published KTVIC gaps from the literature. |
| R1-M5 M3/S3 contradiction | (a) | Report it once, correctly. |
| R1-M6 4-model leaderboard | (c) | Moving beyond 4 models needs GPU decodes. Report it as a 4-model illustration with no τ CIs, or cut it. |
| R1-M7 which system | (a) | Name one system; fix the residual definition. If B-F1 changes the system, Table 5.1 waits for it. |
| R2-F1 companion overlap | (a) + (c) | Add a two-way overlap table (FAIR and companion); fix "English benchmarks only"; send the companion to the editor. If the XM3600 and UIT-ViIC slope results must stay in the companion, delete them here instead of pointing to them. |
| R2-M1 missing prior work | (a) | Cite and position against Geva 2019, Caglayan 2020, Kasai 2022, CLIPScore, van Miltenburg 2024. |
| R2-M2 Vietnamese prior work | (a) | Add VieCap4H and the scene-text dataset; read HDUCap and ViG, or drop them. |
| R2-M3 inflated novelty | (a) | Trim the contributions to the four new audit findings plus the kit. |
| R3-F1 data rights | (a)/(c) | Ask the KTVIC, UIT-ViIC and OpenViIC authors for written terms (an email, not an experiment); report them. If refused, release scripts only and list the restriction as a limitation. |
| R3-M1 generation reproducibility | (a) | Add hardware, software versions and per-run GPU-h from logs; say rerun ≠ original. |
| R3-M2 OpenViIC scan | (b) | Run the 8-gram scan on the kit now and report its result. |
| R3-M3 AI-use disclosure | (a) | Name the tools, state AI drafting of text and matcher rules, ship the manifest as supplementary material. |

---

## 6. The single change most likely to move the outcome to "major revision"

**Rebuild the paper as a resource paper around a public, licensed, DOI-archived KTVIC evaluation kit and the audit findings that survive R1-M2's control** (single writer with a slot-preserving null, punctuation convention, segmentation, matcher, overlap). Move the ladder, B1, WiSE-FT, the leaderboard and all of §6 into a supplementary negative-results record, with the registration labels kept there. This one change does five things:
- it removes most of the jargon;
- it removes the dependence on the pending GPU runs (B-F1, 3B);
- it removes the unresolved H0 from the headline;
- it shrinks the companion-overlap surface;
- it gives LRE the reviewable resource it requires.

---

## 7. Venue judgement

**LRE is the right venue only for the reframed paper of §6.** Its readers value a dataset audit, protocol documentation and a released kit, and Vietnamese is under-resourced. In its current form the paper is a model-training study that reports mostly null or unresolved results, and LRE reviewers will read the method half as out of scope.

If the authors want to keep the system/negatives half as the main contribution, the alternatives on the authors' own list (outline_B.md:17–18) fit better:
- **ACM TALLIP**: an Asian-language scope that accepts system-plus-evaluation papers. It states an explicit ≥ 25%-new rule, which handles the FAIR overlap cleanly.
- **The IP&M low-resource multimodal special issue**: low-resource VLM evaluation is its call topic, and a later deadline (2027-08-31) leaves time for B-F1 and the 3B runs.

The panel does not rank these venues by quartile. The choice should follow the framing: the audit-and-kit framing goes to LRE; the system-and-negatives framing goes to TALLIP or IP&M.
