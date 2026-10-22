# Cover letter, Paper A (IP&M), draft 2026-10-21

<!-- PD-25/25b: signed by the corresponding author, Trần Văn Lăng; Hòa submits. The email and affiliation come from the authors only. Every claim below is a sentence of the abstract or the declarations; nothing here is new. -->

Dear Editor-in-Chief,

We submit the manuscript "Object Metrics Under Incomplete Gold: A Measurement-Validity Analysis of Caption Hallucination Scores" for consideration as a full-length research article in *Information Processing & Management*.

Object-hallucination metrics such as CHAIR and object F1 are widely used to rank captioning and vision–language systems. The manuscript asks when their scores measure what they claim, and tests this with pre-registered analyses.
- **Main result.** In confirmation tests, F1's slope on log object count is ordered by gold completeness (expected for nested reference golds) and positive under label gold, on XM3600 and, with a second Qwen backbone (Qwen3-VL-8B), on the same 600 XM3600 images, with a replication on 295 discovery images. On XM3600, whose label gold is human-verified labels, scored with verified precision (mentions OIV7 cannot verify are excluded), it is positive only when unverifiable mentions are excluded; counting them as errors removes the positive slope (post hoc)<!-- src: data/results/n_f1/bracket_result.json (sha256 4796ed12) :: outcome_paper = ii, sentence_paper; per set: sets.s75.outcome_from_lower = i, sets.xm600.outcome_from_lower = ii (paper-level AND, DESIGN.md R3, CC-063); design c8bd21c; run record manuscript/prereg/2026-10-21_n_f1_bracket/run_record.json (062ab6a5); VERIFIED manuscript/verification/paperA/N_F1_bracket_run.json (60e58bfe; byte-identical re-run); CONFIRMATION_MAP Amendment 4 row 27 -->. There, two of five registered predictions failed with all references.<!-- CONFIRMATION_MAP Amendment 4 (draft): wording of abstract rows 2-new, q1 and 3-new; bracket slot filled with row 27, sentence (ii), from the verified run (PD-28 (1)) --> Post hoc, dropping any system never changes the label-gold sign, but XM3600's one-reference slope turns positive without one verbose system; inference concerns these Qwen-VL systems.<!-- CC-088 A-1 / CP-091: abstract wording (Amendment 6 row 36), no new number -->
- **Other findings.** Public human judgments give mixed evidence: relevance falls with object count, but count-matched precision tracks it worse than raw precision. A registered count-matched leaderboard failed its fidelity check and was not scored, so no count-control claim is confirmatory; the re-scoring of 15 published comparisons is exploratory.

We believe the paper fits the journal's tradition of evaluation and measurement methodology in information processing.

**Transparency**
- Every registered prediction was committed to version control before the outputs it predicts. Analyses written later are labelled post hoc.
- Every reported result in the main text and the supplement is read by script from an output file and listed with the file's SHA-256 in a numbers manifest.<!-- N-M8: softened per the review; manifest rows edited in place (Amendment 4 pass), row count unchanged -->
- The code (MIT licence), the pre-registration files, score-only copies of the result files behind the numbers and the manifest are archived on Zenodo (DOI: [AUTHOR TO PROVIDE]). Of the manifest's 804 rows, 29 cite sources that could not be released, and they are marked.
- The use of generative AI is declared before the references, as the journal's policy requires.

**Our prior work.** One of the evaluated systems is a fine-tuned adapter trained with the recipe introduced in our conference paper (Nguyen et al., FAIR 2026, cited); no result of that paper is repeated here.

**Related manuscript.** A companion manuscript by the same authors on the validity of the Vietnamese captioning benchmark KTVIC is in preparation. It uses the same fine-tuned instrument. This paper's XM3600 results and its object-F1 slope results on UIT-ViIC appear only in this paper. We will gladly provide a copy.

The manuscript has not been published, is not under consideration elsewhere, and has not been posted as a preprint.<!-- CP-054: keep the preprint clause only if still true at submission. --> All authors have approved the submission and declare no competing interests.

Yours sincerely,

Trần Văn Lăng (corresponding author), on behalf of Nguyễn Lê Minh Hòa, Nguyễn Văn Thịnh and Trần Văn Lăng
Journal Editorial Department, Ho Chi Minh City University of Foreign Languages – Information Technology (HUFLIT), Ho Chi Minh City, Vietnam; langtv@huflit.edu.vn<!-- from the IEEE-stamped FAIR 2026 camera-ready, as the first author instructed on 2026-10-21 -->
