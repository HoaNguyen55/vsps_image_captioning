# What is new in Paper B compared with FAIR 2026

FAIR 2026 = "A Method for Reducing Hallucinations in Detailed Vietnamese Image Captioning Using Supervision from Verified Propositions" (VSPS), `manuscript/FAIR_28.08.26_v10_EN_IEEE.pdf`.

## Overlap table

| Item in Paper B | In FAIR? | Status in Paper B |
|---|---|---|
| KTVIC / COCO dataset description; 558-image test split | yes (§IV-A) | reused setup, rewritten |
| QLoRA recipe on Qwen2.5-VL-7B (§4.1) | yes (§IV-B) | reused, cited |
| Zero-shot and P1 (gold SFT) systems; P1 seed 42 CIDEr 149.8 | yes (Table I) | reference point only, not a claim |
| 113-entry Vietnamese object lexicon (= matcher v1) | yes (§IV-C) | reused as v1 |
| KTVIC CHAIR is an upper bound because the gold comes from the references | yes (§IV-C) | acknowledged (sec1:22); quantified here by the second panel (Section 5.3) |
| P1's precision comes with short, reference-style captions | yes (§IV-E) | acknowledged (sec1:22); quantified here by the template and punctuation audits (Sections 3.3, 5.1) |
| Related-work citations (CHAIR, Qwen2.5-VL, QLoRA/LoRA, VnCoreNLP, GRIT 136.0) | yes | reused citations, new text |
| 4-bit DPO negative | yes (§IV-E9) | cited only, not repeated |
| VSPS method, verifier, human rating, gender neutralisation | yes | **not used** |
| Response-only P1-R, 3 seeds, 148.23 (SD 0.38), reproducibility gates | no | new |
| Protocol card (segmenter, CIDEr-D, ×100, punctuation) | no | new |
| Fusion, cons, multiref, unf2, rnd2 systems | no | new |
| Registered supervision ladder (frozen predictions, per-run verdicts, pooled invariance) | no | new (supplement S2) |
| Registered second backbone and its guard abort; 3B fallback (outputs unverified, not reported) | no | new (supplement S3) |
| KTVIC single-writer audit (adjacency 0.7102 vs 0.40) | no | new |
| Punctuation audit (−35.17 CIDEr-D; reference conventions of KTVIC, UIT-ViIC and XM3600; XM3600 period shift) | no | new |
| Evaluation kit (scorer and protocol-card template, matcher code with the author-built v1 and v2 word lists, split and overlap scripts, audit scripts, pre-registration files, score-only result files, numbers manifest; no counts derived from KTVIC, no dataset captions, no v3 rules, predictions or weights; one Zenodo deposit shared with the companion paper) | no (FAIR used the v1 lexicon; the kit ships it as matcher v1) | new |
| Segmentation sensitivity (149.79 vs 165.43) | no | new |
| Matchers v2 / v3, *cây* audit, UIT-ViIC role/child flip | no | new |
| Dataset overlap audit (KTVIC–OpenViIC 401/558; UIT-ViIC–COCO/POPE; CC-005 rule) | no | new |
| UIT-ViIC transfer, in-domain replication | no | new |
| Two caption panels (OpenViIC aggregates), EV-RANK concordance; UPE two-estimator reconciliation (supplement S6.2) | no | new |
| Pre-registered and controlled negatives (kNN, UPE-MBR, 35_e, P-M6b, PLAN-F1, WiSE-FT, self-fuse, E5, MR5, tags), leaderboard, leakage test, Tier-3 dev gates | no | new (supplement S4–S7) |
| Recommendations for Vietnamese captioning evaluation | no | new |
| AI-agent provenance rules and number manifest | no | new |

## Estimated share of new material

Recomputed 2026-10-21 after the round-2 revision (R2 N-m4). The main text (sec1–sec8, HTML comments removed, abstract excluded, tables included) has 9,946 whitespace-separated words, and the supplement 5,768. As a text-overlap check, we lower-cased both this main text and the IEEE-stamped FAIR 2026 paper (`pdftotext`, all pages), split them into word tokens and counted the tokens of this paper that lie inside a run of n consecutive tokens that also occurs in FAIR: 0.69% for n = 5 and 0.09% for n = 8. Verbatim reuse is therefore negligible. The check does not detect paraphrase. Content overlap is the overlap table above: the KTVIC/COCO setup, the QLoRA recipe, the P1 control and its seed-42 score, matcher v1, and two points FAIR already made (KTVIC CHAIR as an upper bound; P1's reference-style captions), which this paper quantifies.

**Estimated new material:** no primary result of Paper B appears in FAIR, and the reused content is confined to the rows marked "reused" above. The earlier word-share estimate (about 88%) was made on an older draft and is not repeated. Disclose FAIR in the cover letter (done).

The two-way overlap with the companion paper (under review) is Table 7.1 of the main text (`sec7_limitations_ethics.md` §7.3).
