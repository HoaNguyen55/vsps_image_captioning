# Paper B: mock LRE review panel, round 2 (2026-10-21)

**Manuscript.** `manuscript/journal_draft_B/`: the abstract in `outline_B.md:8`, sec1–sec8, `supplementary_B.md`, `cover_letter_B.md`, `title_page_B.md`, `paperB.bib`, `number_manifest_B.tsv` and `new_vs_FAIR.md`.

**Title.** *What a Vietnamese Captioning Benchmark Measures: A Validity Audit of KTVIC and an Open Evaluation Kit.*

**Line numbers.** They refer to the source files. HTML comments were stripped with their line breaks kept, so the numbers match the source.

**Other material checked:**
- the FAIR 2026 stamped PDF, read with `pdftotext -layout`;
- the companion manuscript (`manuscript/journal_draft/`);
- the staged archive at `.session_backup/2026-10-21/zenodo_build/` (README, code tree, FINAL_SCAN.json, BUILD_RECORD.json and the archived manifests).

**Data rule.** No dataset caption text was opened or is quoted here.

**Totals for new issues: 1 FATAL, 12 MAJOR, 14 MINOR.**

**Round-1 status (22 FATAL/MAJOR items):**

| Status | Count |
|---|---|
| RESOLVED | 10 |
| PARTLY | 10 |
| OPEN | 1 |
| NO LONGER APPLIES | 1 |

**Overall.** The text has improved a great deal. The main text is now a focused audit-and-kit paper with an abstract, a conclusion and three contributions, and almost no lab codes remain in it.

The main remaining risk is the resource itself. The archive staged for Zenodo is not the kit that Table 3.1 describes. An LRE reviewer who downloads the DOI cannot run most of Table 3.1. That single fact moves the paper from "major revision" towards "desk reject".

---

## 1. Reviewer reports (summary)

### R1: language resources and dataset-audit methodology

**Strengths.**
- The single-writer finding is stated with its confound: sec3:21 now concedes that a slot-position trend could produce the same statistics.
- The punctuation mechanism is clear (sec3:32).
- The overlap audit is useful (sec3:60–62).
- The main text no longer reports method-side verdicts as findings.

**Concerns.**
- The central test still lacks its control: the slot-rate-preserving null is "not run" (sec3:21).
- The companion's own data show above-null adjacency in an independent-worker corpus (N-M5).
- The image-matching method behind 401/555 is not described (N-M9).
- The independence of the second panel is asserted, not checked (N-M10).
- "Pre-registered" rests on git commit times that a reviewer cannot inspect (N-M11).

**Recommendation: major revision.**

### R2: Vietnamese NLP and captioning

**Strengths.**
- Matcher versions with tone normalisation and the *cây* classifier problem (sec3:50–56) are the most Vietnamese-specific and most useful part.
- The protocol card (sec4:22–36) is sensible, and its debt to sacreBLEU and SacreEOS is now acknowledged (sec2:13).
- The Vietnamese dataset list is complete enough (sec2:5).

**Concerns.**
- "Segmenter sensitivity" compares RDRSegmenter with whitespace syllables, not two segmenters (N-M8).
- "P1 (seed 42)" names two different systems (N-M6).
- Several headline sentences say more than the data show (N-M7).
- HDUCap and ViG, the two closest recent systems, are still unread (sec2:7).
- The −35.17 headline still leads the abstract and the cover letter.

**Recommendation: major revision.**

### R3: handling editor (fit, overlap, availability, length, desk-reject screen)

**Fit.** Good, if the kit ships. An audit of a Vietnamese benchmark plus a released evaluation kit is squarely in scope for LRE.

**Overlap with FAIR.** Handled honestly (sec1:22, sec7:35, new_vs_FAIR.md). FAIR already noted two points: KTVIC CHAIR is an upper bound, and P1 matches the short reference phrasing (FAIR §IV-C/§IV-E1). The paper should say so (N-m8).

**Overlap with the companion.**
- Disclosed, and Table 7.1 is a real improvement.
- The two papers point at each other for key controls (N-M4).
- They share one undisclosed archive whose README names the companion's title (N-M3).

**Availability.**
- The licences and terms of the three datasets are now stated (sec3:79). There are no licences, only research-use or citation requests.
- The DOI is still a placeholder, and the staged archive does not match the text (N-F1, N-M1, N-M2).

**Length.**
- The main text is about 8,400 words (sec1–8 summed after stripping comments) and the supplement 5,730.
- The abstract is 253 words. Check LRE's limit; Springer journals often cap the abstract at 250 words.
- There are no figures.

**Desk-reject screen.** A desk reject is likely if the editor or a reviewer opens the archive as staged. It is unlikely once the kit is rebuilt.

**Recommendation: major revision if the kit is fixed; return without review if it is submitted as staged.**

---

## 2. Status of every round-1 FATAL and MAJOR item

| ID | Round-1 issue | Status | Evidence (current file:line) |
|---|---|---|---|
| AE-F1 | Incomplete: no abstract or conclusion, TODOs, PENDING, B-F1 | **RESOLVED** | Abstract at outline_B.md:8; conclusion at sec8:1–9. No TODO or PENDING in the visible main text. B-F1 is stated as not run (sec1:20, S7:224). Author placeholders remain; see N-M12. |
| AE-F2 | Resource not available or citable | **PARTLY** | MIT licence and Zenodo are stated (sec3:77, sec7:25), but the DOI is "[AUTHOR TO PROVIDE]". The staged archive does not contain most Table 3.1 components (N-F1). |
| R1-F1 | Method half has no verdict | **NO LONGER APPLIES** | Reframed: the method results moved to the supplement with their verdicts unchanged (sec1:20, supplementary_B.md:5). |
| R2-F1 | Salami risk with the companion | **PARTLY** | Table 7.1 (sec7:39–51) has been added, and the XM3600 scores and UIT-ViIC slopes were removed (sec3:38, sec5:33). Still open: circular controls (sec3:21 ↔ companion sec5_exchangeability.md:38); the KTVIC row of Table 7.1 (sec7:45); the joint archive (N-M3, N-M4). |
| R3-F1 | Data rights not established | **PARTLY** | Terms now reported (sec3:79, sec7:25): no licence for KTVIC, UIT-ViIC or OpenViIC. Weights and outputs are withheld (sec3:81). There is no written permission, and score-only files derived from these datasets are released "keeping source terms" that do not exist (archive README, "Data terms"). |
| AE-M1 | Internal lab notation | **PARTLY** | The main text is clean except "Paper A's Section 7.5" (sec7:44). The visible supplement still holds 24 seven-hex commit hashes, 33 clock times, 18 "REGISTERED", 7 "KILL", 7 "POST_HOC", 3 "LOCALLY_FROZEN", 4 machine verdict strings (FUND_EXTERNAL_IMAGE_DATA, SECONDARY_POSITIVE_OR_INCONCLUSIVE, NOT_EVALUABLE), run numbers 54–62, and "NCS_DATASET", "evaluate.py" and "hit_max" (e.g. supplementary_B.md:113–118, 239, 99). |
| AE-M2 | Bibliography unusable | **RESOLVED** | paperB.bib has 39 entries checked by DOI/arXiv, and the [VERIFY] tags are gone. Two gaps remain: FAIR pages/DOI are pending (paperB.bib:404), and the companion entry has no title (paperB.bib, `companion2026underreview`). |
| AE-M3 | Unfocused contribution | **RESOLVED** | Three contributions (sec1:16–18). |
| AE-M4 | Process prose | **RESOLVED** (main text) | No timestamps in sec1–8. Timestamps remain in the supplement (e.g. supplementary_B.md:130, 157, 161), which is acceptable but heavy. |
| R1-M1 | Per-run clause cannot discriminate | **PARTLY** | Argued in words (supplementary_B.md:68: "little power to discriminate"). The expected number of runs outside ±1.0 under H0 is not computed. |
| R1-M2 | Single-writer test confounded | **PARTLY** | The confound is acknowledged (sec3:21), but the slot-rate-preserving permutation null is "not run". It is CPU-only on existing data. The companion's controls are misdescribed (N-M5). |
| R1-M3 | Synthetic −35 headline | **PARTLY** | sec1:10 now gives 28.98→33.30 first. The abstract (outline_B.md:8), cover letter :11, sec6:10 and sec8:5 still lead with −35.17, and sec1:10 adds an overclaim (N-M7). |
| R1-M4 | Not a decomposition | **PARTLY** | sec6:7 now says "not additive", and "most published differences" is gone. sec2:7 still says "each of these choices moves CIDEr by more than the reported gaps", but only segmentation was measured. |
| R1-M5 | M3/S3 reported both ways | **RESOLVED** | Reported once as FAIL (S7:221, S8:229). |
| R1-M6 | Degenerate 4-model leaderboard | **RESOLVED** | Moved to S4 and called "an illustration of the protocol, not a ranking result" (supplementary_B.md:99). |
| R1-M7 | Which system is the paper's | **RESOLVED** | P1-R is named the main system (sec4:13, sec5:23, S7:224). The residual is defined on both precision and F1 (supplementary_B.md:27). The label ambiguity is logged separately (N-M6). |
| R2-M1 | Missing annotator and metric-fragility work | **RESOLVED** | Geva 2019, Caglayan 2020, Kasai 2022, CLIPScore and van Miltenburg 2024 are cited (sec2:5, 9, 13, 17). |
| R2-M2 | Vietnamese prior work incomplete | **PARTLY** | VieCap4H, the scene-text dataset and the OpenViIC arXiv version have been added (sec2:5). HDUCap and ViG are still not read (sec2:7). |
| R2-M3 | Novelty inflated | **RESOLVED** | Three contributions; protocol card credited to sacreBLEU/SacreEOS (sec2:13). |
| R3-M1 | Generation reproducibility | **OPEN** | Still no hardware, library versions, decoding seeds or GPU-h in the paper; sec4:42 only states the limit. The archive README already has the pins (transformers 4.51.3, trl 0.19.1) and a hardware table, so this is a copy-over. Runs 56–58 were rerun without any comparison with the lost originals (supplementary_B.md:37). |
| R3-M2 | OpenViIC 8-gram scan unverifiable | **PARTLY** (stale) | sec3:83 says the scan "has not yet been run". The staged archive shows it was run (FINAL_SCAN.json; README "Short matches in pinned code"), but the result and method are not in the paper (N-M2). |
| R3-M3 | AI-use disclosure | **RESOLVED** | Claude and Gemini are named, including text drafting (sec7:68). AI drafting of v3 is stated in the methods (sec3:52). The manifest is supplementary material (sec6:47). Model versions are not given (N-m14). |

**Round-1 MINOR items (brief):**
- AE-m1: PARTLY. new_vs_FAIR.md:35 is still stale.
- AE-m2: RESOLVED.
- AE-m3: PARTLY (sec7:44).
- R1-m1: RESOLVED (sec4:42).
- R1-m2: RESOLVED (S8:240–241).
- R1-m3: OPEN. sec7:13 still reads as if high agreement caused the stop.
- R2-m1: unchanged. The DOI prefix is `j.image.2025` and the year is given as 2026; confirm the year of vol. 140.
- R2-m2: RESOLVED (sec1:12, sec3:60).
- R3-m1: RESOLVED (sec7:31).
- R3-m2: PARTLY. COCO/Open Images exposure caveats still appear 5 times (sec2:5 twice, sec3:11, sec3:15, sec5:29).

---

## 3. New issues

### FATAL

**N-F1. The staged archive is not the evaluation kit the paper describes.**

*Where:* outline_B.md:8, sec1:18, sec3:66–75 (Table 3.1), sec6:37–45 and cover letter :22, set against `.session_backup/2026-10-21/zenodo_build/`.

*Problem.* The text says that the n-gram scorer with punctuation variants, the punctuation and XM3600 period audits, the segmentation audit, the exchangeability test, the *cây* audit, the matchers v1–v3 and a protocol-card template "run as shipped". The staged archive was checked against those claims:

- **Missing scripts.** No script in `code/` or `tools/` contains `doubleton`, `adjacent_share`, `add_period`/`strip_period`/`cider_strip`, `cay_audit` or `protocol_pilot`. The only hits are in pre-registration text files.
- **Headline scripts left behind.** The scripts that produced the headline numbers live only in `.session_backup`:
  - `r11_verify/c3_n2_exchangeability_all_datasets.py` (0.7102);
  - `r11_verify/c8_l5_d1_d3a_cpu_audit.py` (−35.17, 28.98→33.30);
  - `research_r10/E4/protocol_pilot.py` (15.64, τ = 0.969).

  The package plan excludes `.session_backup` ("Never release: … .session_backup", ZENODO_PACKAGE_PLAN_DRAFT.md). STATUS.md:30 already records that the v3 rules, the c8 punctuation audit, the XM3600 period audit, the overlap lists and the 8-gram scanner "still live only in git-excluded session folders".
- **Wrong exchangeability statistic.** The shipped `scripts/caption_exchangeability.py` computes adjacent-versus-non-adjacent object overlap, not the doubleton adjacent share behind 0.7102 or the lag-1 minus lag-2–4 Jaccard excess.
- **Wrong README.** `code/README.md` is the FAIR VSPS README. It describes VSPS, a `Makefile` for the VSPS pipeline, and shipped `data/stage1_records/`, `data/supervision/`, human-audit annotations and test-split predictions. None of these is in the archive, and the last two contradict sec3:81 and sec7:25.
- **Hard-coded paths.** Nine files hard-code the author's repository root (FINAL_SCAN.json `userpaths`).
- **External dependency.** `match_openviic.py` needs an external SSCD copy-detection model (`--sscd`), which the paper never mentions.
- **No protocol card.** No protocol-card template file exists.

*Fix (CPU only, no GPU).* Build a Paper-B kit:
- an include list with the c3_n2, c8, E4, XM3600-period and *cây* scripts, ported to read the reader's dataset copies;
- the v3 rule file, labelled unattested;
- a `PROTOCOL_CARD.md` template;
- a B-specific README with one `selftest` command and the root path made configurable.

Then rerun every Table 3.1 row from the archive on a clean machine, re-scan it, reserve the DOI, and make every sentence about the kit match the archive's file list. Until a reviewer can run each row of Table 3.1 from the DOI, the resource contribution is not reviewable.

### MAJOR

**N-M1. The text contradicts itself on what the kit contains.**

*Lexicons:*
- **Shipped**, per the abstract (outline_B.md:8: "the kit holds our hand-built matcher word lists"), sec1:18, sec3:66, sec3:81, sec7:25 and the archive README;
- **"we release three versions"**, per sec3:48;
- **not included**, per sec6:41 ("lexicons not included") and new_vs_FAIR.md:23 ("no lexicons", "the v1 lexicon, which the kit does not ship").

*Manifest:*
- **not part of the kit**, per sec6:47;
- **archived with the kit**, per sec7:58, cover letter :22 and new_vs_FAIR.md:23.

*Score files:* Table 3.1 and sec3:81 never mention the score-only result files and pre-registration files that the archive and the cover letter (:22) do ship.

*"Hand-built":* the abstract's "hand-built" conflicts with v3 being "drafted by an AI model … from training-split counts" (sec3:52).

*Fix.* Write one inventory of the archive, put it in Table 3.1, and make the abstract, sec1, sec3.7, sec6.4, sec7.2, new_vs_FAIR.md and the cover letter quote it. Call the word lists "author-built (v1, v2) and model-drafted, unattested (v3)".

**N-M2. The 8-gram scan text is stale, and the "no text from any dataset" claim needs a caveat.**

*Problem.*
- sec3:83 says the scan "has not yet been run". The archive's FINAL_SCAN.json and README show that a scan was run.
- The README says five pinned code files contain author-written example phrases that share 8–9 consecutive words with some dataset captions, and that no match of 12 or more words exists.
- sec3:81 and sec7:25 state flatly that the kit contains "no text from any dataset". The paper never defines the scan (which corpora, n, tokenisation, exclusions).

*Fix.* Report the scan in sec3.7:
- the corpora scanned and n = 8;
- that 0 files contain a match of 12 or more words;
- the number of documented 8–9-word matches in pinned code, and why those files cannot be edited (they are pinned by pre-registration hashes).

Soften "no text" to "no dataset captions; N short incidental matches in author-written code examples, listed in BUILD_RECORD.json".

**N-M3. The archive is shared with the companion paper, and the paper does not say so.**

*Problem.* The staged README introduces the deposit as accompanying two manuscripts and gives the companion's full title. One DOI would then be the "resource" contribution of two papers. sec3:77, sec7:25, Table 7.1 (sec7:39–51) and the cover letter never mention this. The companion bib entry has no title, while the archive gives it.

*Fix.*
- Either build a separate Paper-B deposit (preferred for LRE), or state in sec3.7 and Table 7.1 that one archive serves both papers and say which components belong to each.
- Give the companion's title in paperB.bib and in cover letter :18.

**N-M4. The overlap with the companion is honest but circular, and Table 7.1 misstates one row.**

*Problem.*
- **Circular controls.** B's main audit statistic (sec3:19–21) is the companion's diagnostic: the companion calls it "Our diagnostic" (journal_draft/sec1_introduction.md:11) and develops it in its sec5. B defers its negative controls to the companion ("The companion paper reports the same statistics at the null…", sec3:21), and the companion defers its KTVIC case back to B (journal_draft/sec5_exchangeability.md:38). Neither paper alone shows the contrast.
- **Unchecked XM3600 claim.** sec3:38 says that with the period appended "both systems still score below the zero-shot backbone", which rests on XM3600 scores that B declines to print. A reviewer of B cannot check it.
- **Table 7.1 KTVIC row.** sec7:45 says the companion uses KTVIC as a "motivating example only". In fact the companion computes OpenViIC-panel statistics on KTVIC test images (journal_draft/sec11_limitations_ethics.md:39; journal_draft/supplementary.md:262).

*Fix.*
- Print the independent-corpus control values in sec3.2 with attribution to the companion (e.g. COCO 0.402, UIT-ViIC 0.384), and say the diagnostic is defined there.
- Either print the three XM3600 CIDEr-D values with attribution or delete "still score below".
- In Table 7.1, change "KTVIC: motivating example only" to say the companion also uses OpenViIC captions of KTVIC test images.

**N-M5. The single-writer inference ignores evidence that file order alone can raise the statistic.**

*Problem.* sec3:21 says the companion shows the statistic "at the null on corpora written by independent annotators". The companion's own table (journal_draft/sec5_exchangeability.md, Table 5.1) reports two corpora above the null:
- Flickr30k, written by independent workers, at 0.483 with a lag-1 excess of +0.055, which the companion attributes to "a non-random file order";
- OpenViIC full test at 0.477.

So adjacency above 0.40 is not specific to a single writer. KTVIC's 0.71 is far higher, and the interface description (Pham et al., §3.2) supports a single writer, but the text overstates what the control shows. Together with the unrun slot-preserving null, the step from "0.71" to "each written with the previous one in view" (sec3:21) is still an interpretation.

*Fix.*
- Run the slot-rate-preserving permutation null; it is CPU-only on existing files.
- Report Flickr30k and OpenViIC as above-null cases caused by ordering.
- Phrase the conclusion as "consistent with the single-writer interface and not explained by slot inclusion rates" only if the null supports it.

**N-M6. "P1 (seed 42)" names two different systems.**

*Problem.* The label "P1" covers both the legacy-mask P1 and the response-only P1-R:
- sec3:34: "P1 (seed 42) … from 148.66" is P1-R (source key `p1assist_s42`; 148.66 = P1-R seed 42, sec5:7).
- sec3:44: "P1 (seed 42) scores 149.79" is legacy P1 (`p1-gold-short`).
- sec3:54: P1-R again (`p1assist_s42`).
- Legacy P1 is used for the UIT-ViIC flip (sec3:56, `transfer_p1_s43`), for XM3600 (sec3:38, `p1_s43`), for UIT-ViIC transfer (sec5:29) and for the second panel (sec5:43, `p1-gold-short`).

A reader cannot tell which numbers belong to the declared main system.

*Fix.* Use "P1-R" and "P1 (legacy mask)" everywhere, give the seed each time, and add a one-line note in sec4.1 on which analyses use which.

**N-M7. Several claims are stronger than the evidence.**

| Where | Claim | What the evidence shows |
|---|---|---|
| sec1:10 | "Any system that writes ordinary Vietnamese sentences pays this cost." | The measured cost for a punctuating system is +4.32 (28.98→33.30); 35.17 applies only to a system that never punctuates. |
| sec2:7 | Protocol choices each move CIDEr "by more than the reported gaps between systems". | Only segmentation was measured (Section 3.4). CIDEr variant and scale were not. |
| outline_B.md:8 | On the second panel "some differences between systems shrink or vanish". | One contrast at one seed: the precision cost goes from −2.21 to −0.25, while the F1 gain grows from +3.99 to +4.51 (sec5:43). |
| outline_B.md:8, sec8:5 | The convention follows KTVIC-trained systems "to other corpora". | One corpus (XM3600); UIT-ViIC was not measured (sec3:36). |
| sec5:22 | CIDEr "rewards matching the short, unpunctuated reference template, not describing more of the image". | The detailed-mode collapse (22.4) also reflects CIDEr-D's length penalty and fuse2's period-closed detailed targets (sec4:14). |

*Fix.* Reword each to its measured scope. Lead the abstract with the strip/append deltas on punctuating systems and keep −35.17 as the never-punctuating extreme.

**N-M8. The "segmenter" claim compares a segmenter with no segmentation.**

*Problem.* sec3:44 compares RDRSegmenter with whitespace syllables, yet the abstract says "CIDEr-D moves by 15.64 points with the word segmenter alone", and sec6:11 says "the choice of segmenter". In addition:
- τ = 0.969 is "over all scored systems" with no n;
- "RDRSegmenter … reproduces KTVIC's own segmentation" has no number, although `scripts/identify_segmenter.py` exists.

*Fix.* Say "word segmentation versus syllable tokenisation". Give n for τ and the agreement rate with KTVIC's segmentation. Optionally, as a CPU-only check, add a second real segmenter so that "choice of segmenter" is earned.

**N-M9. The image-matching method behind 401/555 is not described.**

*Problem.* sec3:13 and sec3:60 say only that test images "match an image" in OpenViIC. The shipped `match_openviic.py` shows a perceptual-hash proposal step (Hamming distance ≤ 10), confirmation by SSCD cosine ≥ 0.5, and a visual check. None of this, nor any false-match or missed-match rate, is in the paper.

*Fix.* Add a short method paragraph covering:
- the hash type and threshold;
- the copy-detection model and threshold;
- how many pairs were inspected by eye, and the result;
- the external model as a kit dependency.

**N-M10. The independence of the OpenViIC panel is asserted, not checked.**

*Problem.* sec1:12, sec2:17, sec3:13 and sec5:41 call the OpenViIC captions "independent". The companion reports that OpenViIC's caption-entry protocol "is not documented" and finds its full-test adjacency above the null (journal_draft/sec5_exchangeability.md, Table 5.1). The claim that 55.12% of fuse2's "hallucinated" objects appear in the other panel (sec5:43) depends on this independence.

*Fix.* Report aggregate cross-panel n-gram overlap on the 555 images (KTVIC references against OpenViIC captions) beside the within-panel overlap, as aggregates only and CPU-only. Say "written separately" unless the check supports "independent".

**N-M11. Registration times cannot be verified by a reviewer.**

*Problem.* The verdict labels in sec7:60 and supplementary_B.md:9 are "computed from commit, push, file and output times". The archive ships the pre-registration files but not the git history, and the paper gives no public repository URL. A reviewer therefore cannot check any commit hash or time cited in the supplement, and "pre-registered" in the abstract rests on records the reviewer cannot see.

*Fix.* Do one of the following:
- give the public repository URL and state that the cited commits are on it;
- include a `git bundle` or a signed list of commit time stamps in the archive;
- say "registered in version control" and call it self-attested.

**N-M12. Submission blockers remain in the visible text.**

*Problem.*
- DOI placeholders: sec3:77, sec7:25 and cover letter :22.
- "[STATUS AT SUBMISSION…]": cover letter :18.
- FAIR pages and DOI are pending (paperB.bib:404).
- The companion bib entry has no title.
- S7:224 is written in a conditional future tense ("If it has not been run by the freeze date of 2026-11-15, it is reported here as registered and not run").
- sec3:83 has a stale "has not yet been run".

*Fix.* Fill or remove every placeholder and write S7:224 in its final state. B-F1 is optional and not blocking: the main system is P1-R whatever its outcome (S7:224). Consider dropping "the single final test evaluation has not been run" from the abstract and sec8:9 and keeping it only in S7.

### MINOR

1. **N-m1.** Visible "Paper A's Section 7.5" in Table 7.1 (sec7:44). Write "the companion's".
2. **N-m2.** sec3:51 says "30 of 73 scored systems", while sec5:45 says "all 79 scored KTVIC systems". Explain the difference (date or set).
3. **N-m3.** P1's three-seed M is 1.7825 in Table 5.1 (sec5:13) and 1.7826 in S2.1 (supplementary_B.md:27). Use one rounding.
4. **N-m4.** new_vs_FAIR.md:35 is stale:
   - it gives 7,669 and 8,115 words, but the main text is now about 8,400;
   - the share of new material is "not recomputed";
   - it cites "§8.3", which no longer exists.
   Recompute it with a text-overlap tool.
5. **N-m5.** sec7:13 (round-1 R1-m3) still reads as if high agreement caused the stop. Explain that the gate stops the criterion analysis when rating variance is too low, or drop the paragraph.
6. **N-m6.** sec7:58 says "Every number is read from a JSON key". The manifest also has derived, literature, stdout-line and TSV rows (number_manifest_B.tsv status column). Say "from an output file or a stated derivation".
7. **N-m7.** The abstract is 253 words (outline_B.md:8). Check LRE's limit.
8. **N-m8.** FAIR already noted that KTVIC CHAIR is an upper bound because gold comes from references, and that P1 matches the short reference phrasing (FAIR §IV-C, §IV-E1). Acknowledge this in sec1:22 and new_vs_FAIR.md, so the "incomplete gold" and "template" points are presented as quantified here, not as first raised here.
9. **N-m9.** There are no figures. The adjacency figure slot (sec3:21 comment) and a k = 1…5 punctuation curve (sec3:34) would help readability.
10. **N-m10.** sec1:12 is headed "Two caption panels disagree", but its content is the image overlap. Split it or retitle it.
11. **N-m11.** The archived manifest gives "human-judgment source" as the reason for withholding rows that cite pre-registration files (V4.txt, the WiSE-FT addendum, the M6 REPORT). Most of those files ship in `code/manuscript/prereg/`. Fix the reasons.
12. **N-m12.** Table S2 reports reruns 56–58, which number_manifest_B.tsv:312–314 marks "outputs not yet verified". Verify them or flag them in the table.
13. **N-m13.** S5's numbers (0.20 [−13.97, +14.67]; bounds −38.05 to +13.02; supplementary_B.md:103) have no manifest rows.
14. **N-m14.** The AI tools in sec7:68 are named without versions or dates of use.

---

## 4. Related work: gaps

**Verified by the panel** (arXiv API or Crossref, 2026-10-21). These are relevant to an LRE audit paper and are not cited:

- **Benchmark validity**
  - Bowman and Dahl (2021), *What Will it Take to Fix Benchmarking in Natural Language Understanding?* NAACL. doi 10.18653/v1/2021.naacl-main.385.
  - Raji et al. (2021), *AI and the Everything in the Whole Wide World Benchmark.* arXiv 2111.15366.
- **Dataset documentation.** The protocol card is a cousin of these:
  - Bender and Friedman (2018), *Data Statements for Natural Language Processing.* TACL. doi 10.1162/tacl_a_00041.
  - Gebru et al., *Datasheets for Datasets.* arXiv 1803.09010.
- **Train–test overlap auditing.** The direct analogue of §3.6: Lewis et al., *Question and Answer Test-Train Overlap in Open-Domain Question Answering Datasets.* arXiv 2008.02637.
- **Caption-metric validity**
  - Kilickaya et al., *Re-evaluating Automatic Metrics for Image Captioning.* arXiv 1612.07600.
- **Vietnamese VLMs and benchmarks**
  - *LaVy: Vietnamese Multimodal Large Language Model.* arXiv 2404.07922.
  - *OpenViVQA* (UIT, the same group as UIT-OpenViIC). arXiv 2305.04183.

**Possible gaps, not verified:**
- Vietnamese captioning systems from 2025–2026 that report KTVIC scores, beyond GRIT, HDUCap and ViG.
- Recent Vietnamese multimodal-LLM evaluation suites.
- Whether KTVIC has a peer-reviewed version beyond arXiv 2401.08100 (paperB.bib cites only the preprint).

---

## 5. Recommendation distribution

**As staged (archive as built on 2026-10-21, placeholders unfilled):**

| Outcome | Probability |
|---|---|
| Desk reject / return without review | 25% |
| Reject | 15% |
| Major revision | 45% |
| Minor revision | 12% |
| Accept | 3% |

**After N-F1, N-M1–N-M3 and N-M12 are fixed (a CPU-only rebuild of the kit and the text):**

| Outcome | Probability |
|---|---|
| Desk reject | 7% |
| Reject | 13% |
| Major revision | 55% |
| Minor revision | 22% |
| Accept | 3% |

The difference between the two rows is mostly one test: can a reviewer who downloads the DOI run every row of Table 3.1?

## 6. The five highest-value fixes before submission

1. **Build the Paper-B kit and make the text match it** (N-F1, N-M1, N-M2).
   - Ship the scripts that produced 0.7102, −35.17/+4.32, 15.64, the XM3600 period shift and the *cây* audit.
   - Add the v3 rules (labelled unattested), a protocol-card template and a B-specific README with one self-test.
   - Remove the hard-coded root path.
   - Rerun each Table 3.1 row from the archive.
   - Report the 8-gram scan result.
   - Reserve the DOI.

   CPU only.
2. **Close the single-writer control** (R1-M2, N-M5). Run the slot-rate-preserving null, and print the companion's independent-corpus values with attribution, including the above-null Flickr30k/OpenViIC cases. CPU only.
3. **Fix the companion handling** (R2-F1, N-M3, N-M4).
   - Disclose the shared archive and the companion's title.
   - Correct the KTVIC row of Table 7.1.
   - Either print with attribution or drop the XM3600 "still below zero-shot" sentence.
4. **Bring claims to their evidence** (R1-M3, N-M6–N-M10).
   - Lead with the strip/append deltas.
   - Separate P1 from P1-R everywhere.
   - Reword sec1:10, sec2:7, the "shrink or vanish" claim and "segmenter".
   - Document the image-matching method.
   - Check the independence of the panel with aggregates.
5. **Make the package submission-ready** (N-M12, R3-M1, AE-M1, N-M11).
   - Fill the placeholders and resolve S7:224.
   - Add a reproducibility paragraph (hardware, the pinned library versions from the archive README, GPU-h per run).
   - Move commit hashes and clock times from the supplement into one provenance table.
   - Give the public repository URL so that registration times can be checked.

   B-F1 is optional and not blocking. If it is run, report it in S7 only.
