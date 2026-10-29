# Cover letter, Paper A (Signal Processing: Image Communication), draft v2 2026-10-27

<!-- v2 (SPIC): retargeted per plan §7 (11-06 item, done early: no PI input needed) and PI-1026ae: journal name; fit sentence for SPIC's "multimedia quality assessment and measures" scope; private reviewer link; Paper B "in preparation, copy to the editor"; subscription route needs no statement here. Signed by the corresponding author, Trần Văn Lăng (PD-25/25b). Every claim below is a sentence of the abstract or the declarations; nothing here is new. -->

Dear Editor,

We submit the manuscript "Gold Completeness and the Verbosity Slope of Object Hallucination Metrics: A Registered Audit" for consideration as an original research article in *Signal Processing: Image Communication*.

Object-hallucination metrics such as CHAIR and object F1 are widely used to rank captioning and vision–language systems. The manuscript asks when these quality measures measure what they claim, and tests this with pre-registered analyses.
- **Main result.** In registered tests on Vietnamese Crossmodal-3600 images (intervals conditional on the systems scored), and with a second Qwen backbone on 537 of the same 600 images, the slope of object F1 on log object count is ordered by gold completeness. Its positive sign under human-verified labels depends on excluding mentions the labels cannot verify, and the reference-gold signs rest on one verbose system (both post hoc). Two of five registered Crossmodal-3600 predictions failed. The registered primary replication on PASCAL-50S (50 references per image, seven public LVLMs) failed at its label-gold step (50 references against VOC labels: −2.29 [−5.15, +0.61]); the slope still rose at every registered reference level (secondary), and a registered companion test placed reference gold below a size-matched random-deletion null. The ordering claim is therefore scoped to Crossmodal-3600 and its second backbone (Section 6.4, Table 1). All registered verdicts, failures included, are listed in one table.
- **Other findings.** In public human judgments, relevance falls with object count, but count-matched precision tracks it worse than raw precision. A registered count-matched leaderboard failed its fidelity check and was not scored, so no count-control result is confirmatory; the re-scoring of 15 published comparisons is post hoc.

The paper fits the journal's scope on multimedia quality assessment and measures: it shows that the validity of an object-level caption score depends on its reference set, and it continues the journal's discussion of whether image-captioning metrics measure what they should.

**Transparency**
- Every registered prediction was committed to version control before the outputs it predicts. Analyses written later are labelled post hoc.
- Every reported number is read by script from an output file and listed with the file's SHA-256 in a numbers manifest.
- The code (MIT licence), the pre-registration files, score-only copies of the result files behind the numbers and the manifest are deposited on Zenodo as a restricted record; reviewers receive a private access link [PI: link to be inserted at submission].
- The use of generative AI is declared before the references, as the journal's policy requires.

**Our prior work.** One of the evaluated systems is a fine-tuned adapter trained with the recipe introduced in our conference paper (Nguyen et al., FAIR 2026, cited); no result of that paper is repeated here.

**Related manuscript.** A companion manuscript by the same authors on the validity of the Vietnamese captioning benchmark KTVIC is in preparation; a copy is available to the editor. This paper's XM3600 results and its object-F1 slope results on UIT-ViIC appear only in this paper.

The manuscript has not been published, is not under consideration elsewhere, and has not been posted as a preprint.<!-- CP-054: keep the preprint clause only if still true at submission. --> All authors have approved the submission and declare no competing interests.

Yours sincerely,

Trần Văn Lăng (corresponding author), on behalf of Nguyễn Lê Minh Hòa, Nguyễn Văn Thịnh and Trần Văn Lăng
Journal Editorial Department, Ho Chi Minh City University of Foreign Languages – Information Technology (HUFLIT), [ADDRESS: PI to supply by 11-04], Ho Chi Minh City, Vietnam; langtv@huflit.edu.vn
