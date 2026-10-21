# Cover letter, Paper B (Language Resources and Evaluation), draft 2026-10-21

<!-- Venue LRE (PD-25 Q7). Signed by the corresponding author, Trần Văn Lăng (PD-25b). Every claim below comes from the abstract, Section 1 or the declarations; nothing here is new. Fill the placeholders at submission. -->

Dear Editors,

We submit the manuscript "What a Vietnamese Captioning Benchmark Measures: A Validity Audit of KTVIC and an Open Evaluation Kit" for consideration in *Language Resources and Evaluation*.

Vietnamese captioning systems are compared mainly by CIDEr on KTVIC. This manuscript audits what a KTVIC score measures and releases the audit as an open evaluation kit. Four properties of the dataset change what its scores mean:
- the five references of each image come from one writer;
- no reference ends with a period: stripping the final period raises the zero-shot backbone's CIDEr-D from 28.98 to 33.30, and appending one to every output of a fine-tuned system that never punctuates lowers it by 35.17 points;
- scores depend on word segmentation (15.64 CIDEr-D points against syllable tokenisation) and on matcher rules that are rarely published;
- 555 of the 558 test images also appear in UIT-OpenViIC, 401 of them in its training split.
We propose a protocol card that states these choices with every score. The pre-registered training and decoding tests are reported in a supplement with their verdicts unchanged.

**Prior and related work.**
- A conference version appeared at FAIR 2026 (IEEE; cited). Its contribution, VSPS supervision, is not used here. The overlap is the KTVIC/COCO setup, the P1 training recipe and one baseline score, used as a reference point. Section 1 states this.
- A companion manuscript by the same authors, "Object Metrics Under Incomplete Gold: A Measurement-Validity Analysis of Caption Hallucination Scores", is [STATUS AT SUBMISSION: under review at Information Processing & Management]. Its XM3600 and UIT-ViIC slope results appear only there, and this manuscript cites them. The exchangeability statistic of Section 3.2 is defined there, and the two papers share one Zenodo archive (Section 3.7, Table 7.1). We will gladly provide a copy.

**Transparency.**
- Every number is traced to an output file, a stated derivation or a cited source in a numbers manifest.
- The kit, the pre-registration files, the score-only result files and the manifest are archived on Zenodo (DOI: [AUTHOR TO PROVIDE]), in one deposit shared with the companion manuscript; 41 of the manifest's 504 rows cite sources that could not be released and are marked.
- The kit contains our matcher word lists (author-built, v1 and v2) but no counts derived from KTVIC and no dataset captions; the model-drafted v3 rules are not included.
- The use of generative AI is declared in Section 7.5.

The manuscript has not been published and is not under consideration elsewhere. All authors have approved the submission and declare no competing interests.

Yours sincerely,

Trần Văn Lăng (corresponding author), on behalf of Nguyễn Lê Minh Hòa, Nguyễn Văn Thịnh and Trần Văn Lăng
Journal Editorial Department, Ho Chi Minh City University of Foreign Languages – Information Technology (HUFLIT), Ho Chi Minh City, Vietnam; langtv@huflit.edu.vn
