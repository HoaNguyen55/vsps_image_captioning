# Cover letter, Paper A (IP&M), draft 2026-10-21

<!-- PD-25/25b: signed by the corresponding author, Trần Văn Lăng; Hòa submits. The email and affiliation come from the authors only. Every claim below is a sentence of the abstract or the declarations; nothing here is new. -->

Dear Editor-in-Chief,

We submit the manuscript "Object Metrics Under Incomplete Gold: A Measurement-Validity Analysis of Caption Hallucination Scores" for consideration as a full-length research article in *Information Processing & Management*.

Object-hallucination metrics such as CHAIR and object F1 are widely used to rank captioning and vision–language systems. The manuscript asks when their scores measure what they claim, and tests this with pre-registered analyses.
- **Main result.** In confirmation tests, F1's slope on log object count is ordered by gold completeness and is positive under complete gold. This holds on XM3600 and, with a second backbone (Qwen3-VL-8B), on the same 600 XM3600 images, with a replication on 295 discovery images. On XM3600, two of five registered predictions failed with all references.
- **Other findings.** Public human judgments give mixed evidence: relevance falls with object count, but count-matched precision tracks it worse than raw precision. A registered count-matched leaderboard could not be scored, so no count-control claim is confirmatory; the re-scoring of 15 published comparisons is exploratory.

We believe the paper fits the journal's tradition of evaluation and measurement methodology in information processing.

**Transparency**
- Every registered prediction was committed to version control before the outputs it predicts. Analyses written later are labelled post hoc.
- Every number in the paper is read by script from an output file and listed with the file's SHA-256 in a numbers manifest.
- The code (MIT licence), the pre-registration files, score-only copies of the result files behind the numbers and the manifest are archived on Zenodo (DOI: [AUTHOR TO PROVIDE]). Of the manifest's 655 rows, 38 cite sources that could not be released, and they are marked.
- The use of generative AI is declared before the references, as the journal's policy requires.

**Our prior work.** One of the evaluated systems is a fine-tuned adapter trained with the recipe introduced in our conference paper (Nguyen et al., FAIR 2026, cited); no result of that paper is repeated here.

**Related manuscript.** A companion manuscript by the same authors on the validity of the Vietnamese captioning benchmark KTVIC is in preparation. It uses the same fine-tuned instrument. This paper's XM3600 results and its object-F1 slope results on UIT-ViIC appear only in this paper. We will gladly provide a copy.

The manuscript has not been published, is not under consideration elsewhere, and has not been posted as a preprint.<!-- CP-054: keep the preprint clause only if still true at submission. --> All authors have approved the submission and declare no competing interests.

Yours sincerely,

Trần Văn Lăng (corresponding author), on behalf of Nguyễn Lê Minh Hòa, Nguyễn Văn Thịnh and Trần Văn Lăng
Journal Editorial Department, Ho Chi Minh City University of Foreign Languages – Information Technology (HUFLIT), Ho Chi Minh City, Vietnam; langtv@huflit.edu.vn<!-- from the IEEE-stamped FAIR 2026 camera-ready, as the first author instructed on 2026-10-21 -->
