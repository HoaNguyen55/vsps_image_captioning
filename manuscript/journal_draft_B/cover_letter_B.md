# Cover letter, Paper B (Language Resources and Evaluation), draft 2026-10-29

<!-- Venue LRE (PD-25 Q7). Signed by the corresponding author, Trần Văn Lăng (PD-25b). Every claim below comes from the abstract, Section 1 or the declarations; nothing here is new. Fill the placeholders at submission. -->

Dear Editors,

We submit the manuscript "What Training-Data Gains Measure on a Vietnamese Captioning Benchmark: A Development Study with Two Reference Panels, a Validity Audit of KTVIC and an Open Evaluation Kit" for consideration in *Language Resources and Evaluation*.

Vietnamese captioning systems are compared mainly by CIDEr on KTVIC. This manuscript audits what a KTVIC score measures and releases the audit as an open evaluation kit. Four properties of the dataset change what its scores mean:
- the five references of each image come from one writer;
- no reference ends with a period, and the scoring pipeline decides what that costs: Vietnamese pipelines that replace pycocoevalcap's PTB tokenizer with a word segmenter drop its punctuation removal, and under them one appended period lowers a fine-tuned system's CIDEr-D by 35.17 points, while with PTB-style removal it costs nothing;
- scores depend on word segmentation (15.64 CIDEr-D points against syllable tokenisation) and on matcher rules;<!-- CC-147 W5: unsourced frequency claim removed. -->
- 555 of the 558 test images have captioned copies in UIT-OpenViIC, 401 of them in its training split (the 401 was reported by Tran et al., 2026, for a retrieval model).
On development data with one backbone, the manuscript also asks what a training-data gain measures. Each doubling of KTVIC training images raises CIDEr-D by +9.61 [7.18, 12.36]. On 187 development images, the gain is +10.59 [7.43, 13.81] against KTVIC references and +0.72 [−0.83, 2.36] against a second, separately written caption panel of the same images: gains from more KTVIC training captions register mainly on KTVIC's own references. In a two-seed reverse pilot trained on the second panel's captions, the gain against KTVIC references, +1.29 [−1.23, 3.75], is not distinguishable from zero; whether such gains reach KTVIC references is not established. KTVIC test is closed under our one-look rule, so these results stay at the development tier.<!-- BD revision 2026-10-29 items 1, 2, 5e, 7: 'no measurable gain' replaced; src d0_decide.json 15dd925f primary.b_K ; b_K_ci95 ; b_O ; b_O_ci95 ; b_r1 decide a6627047 primary.b_K_other ; b_K_ci95 -->
We propose a protocol card that states these choices with every score, and release an open evaluation kit that scores any system's outputs under a declared card. Under a description-only pre-registration, we ran the kit on 3 external systems from 3 sources (three released third-party checkpoints, each decoded by us and scored once on the test split it reports on; descriptive scores, no ranking). No outside group has yet run the kit.<!-- CC-145 W2: authors' run stated; 'validated' removed. --><!-- CC-126 W3 headline; PREREG 2026-10-28_b2_external §7.3 templates; scores.json e1a6e0d8 :: external_systems, distinct_sources, w13_validated_sentence_allowed --> The pre-registered training and decoding tests are reported in a supplement with their verdicts unchanged.

**Prior and related work.**
- A conference version appeared at FAIR 2026 (IEEE; cited). Its contribution, VSPS supervision, is not used here. The overlap is the KTVIC/COCO setup, the P1 training recipe and one baseline score, used as a reference point. Section 1 states this.
- A companion manuscript by the same authors, "Gold Completeness and the Verbosity Slope of Object Hallucination Metrics: A Registered Audit", is in preparation (working title; a copy is available to the editor on request).<!-- 2026-10-27: A moved from IP&M to SPIC, single-anonymized, not yet submitted (PI-1026ad, PI-1026ae). If A is submitted before B, write "under review at Signal Processing: Image Communication (submitted <date>)" here and in sec1/sec2/sec7/bib. --> Its XM3600 and UIT-ViIC slope results appear only there, and this manuscript cites them. The exchangeability statistic of Section 3.2 is defined there (Supplementary Table S13.1). In the manuscript the companion is cited without its title, as work in preparation.<!-- CC-088 (A-2); title restoration in the manuscript CLOSED by CC-145 J3 (2026-10-28): title in this cover letter only; "in preparation" kept in the manuscript; B (LRE 12/2026) precedes A (SPIC 12-21..12-30, PI-1026ap) -->

<!-- LRE Special Focus (less-resourced languages): flag here or not; PI decision owed (V2_PROGRESS_B.md). -->

**Transparency.**
- Every number is traced to an output file, a stated derivation or a cited source in a numbers manifest.
- The kit, the pre-registration files, the score-only result files and the manifest are archived on Zenodo (reserved DOI: [AUTHOR TO PROVIDE: Zenodo reserved DOI]), in a deposit that holds this paper's components only; until the record is public, the editor and reviewers receive an access link;<!-- CC-074 (b): the Zenodo record stays unpublished until the decision on Paper A (venue now SPIC, PI-1026ad; CC-074(c) kept by PI-1026ae) --> manifest rows that cite sources that could not be released are marked as withheld.<!-- deposit v4: 42 of 604; recount at the rebuild (V2_PROGRESS_B pass 2) -->
- The kit contains our matcher word lists (author-built, v1 and v2) but no counts derived from KTVIC and no dataset captions; the model-drafted v3 rules are not included.
- The authors of KTVIC and UIT-OpenViIC confirmed in writing (2026-10-28) the use of their datasets; the confirmations are on file with the corresponding author.<!-- PI-1026az; CC-126 W17 -->
- In the paper and its kit, UIT-ViIC appears only as aggregates and pointers; no UIT-ViIC caption or per-image panel is shown or released, and no permission from its authors is claimed.<!-- PI-1029p (5) -->
- The use of generative AI is declared in Section 7.5.

**Authors.**<!-- CC-074 (LRE cover-letter rule, per the guide as read by Ken 2026-10-21): an ORCID iD or a university homepage/online CV for each author; never invent or look up IDs without the authors' confirmation. -->
- Nguyễn Lê Minh Hòa: [AUTHOR TO PROVIDE: ORCID iD or university homepage/online CV]
- Nguyễn Văn Thịnh: [AUTHOR TO PROVIDE: ORCID iD or university homepage/online CV]
- Trần Văn Lăng: [AUTHOR TO PROVIDE: ORCID iD or university homepage/online CV]

The training-set-size and two-panel studies are part of this manuscript only; we do not submit them as a separate paper. The manuscript has not been published and is not under consideration elsewhere. All authors have approved the submission and declare no competing interests.

Yours sincerely,

Trần Văn Lăng (corresponding author), on behalf of Nguyễn Lê Minh Hòa, Nguyễn Văn Thịnh and Trần Văn Lăng
Journal Editorial Department, Ho Chi Minh City University of Foreign Languages – Information Technology (HUFLIT), Ho Chi Minh City, Vietnam; langtv@huflit.edu.vn
