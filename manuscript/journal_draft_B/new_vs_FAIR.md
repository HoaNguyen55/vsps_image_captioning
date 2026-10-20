# What is new in Paper B compared with FAIR 2026

FAIR 2026 = "A Method for Reducing Hallucinations in Detailed Vietnamese Image Captioning Using Supervision from Verified Propositions" (VSPS), `manuscript/FAIR_28.08.26_v10_EN_IEEE.pdf`.

## Overlap table

| Item in Paper B | In FAIR? | Status in Paper B |
|---|---|---|
| KTVIC / COCO dataset description; 558-image test split | yes (§IV-A) | reused setup, rewritten |
| QLoRA recipe on Qwen2.5-VL-7B (§4.1) | yes (§IV-B) | reused, cited |
| Zero-shot and P1 (gold SFT) systems; P1 seed 42 CIDEr 149.8 | yes (Table I) | reference point only, not a claim |
| 113-entry Vietnamese object lexicon (= matcher v1) | yes (§IV-C) | reused as v1 |
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
| Evaluation kit (own code only: scorer and protocol card, matcher code, split and overlap scripts, audit scripts, number manifest; no lexicons, predictions or weights) | no (FAIR used the v1 lexicon, which the kit does not ship) | new |
| Segmentation sensitivity (149.79 vs 165.43) | no | new |
| Matchers v2 / v3, *cây* audit, UIT-ViIC role/child flip | no | new |
| Dataset overlap audit (KTVIC–OpenViIC 401/558; UIT-ViIC–COCO/POPE; CC-005 rule) | no | new |
| UIT-ViIC transfer, in-domain replication | no | new |
| Two caption panels (OpenViIC aggregates), EV-RANK concordance; UPE two-estimator reconciliation (supplement S6.2) | no | new |
| Pre-registered and controlled negatives (kNN, UPE-MBR, 35_e, P-M6b, PLAN-F1, WiSE-FT, self-fuse, E5, MR5, tags), leaderboard, leakage test, Tier-3 dev gates | no | new (supplement S4–S7) |
| Recommendations for Vietnamese captioning evaluation | no | new |
| AI-agent provenance rules and number manifest | no | new |

## Estimated share of new material

Method: words of the draft text (src comments removed), 7,669 in total across sec1–sec8 (2026-10-15). After the PD-24 rebuild (2026-10-20) the main text is 8,115 words (sec1–sec8, abstract excluded) and the supplement 5,720; the share below was not recomputed. Paragraphs that restate FAIR content were counted generously as overlap. These are §4.1's recipe and the zero-shot/P1 rows; §3.1's KTVIC description; the reused citations in §2; the P1 149.8 reference in §3.4 and §5.1; §8.3. That gives about 700–900 words, or 9–12%.

**Estimated new material: about 88% (range 85–91%).** This is well above the ≥ 30% target (LRE, IP&M) and TALLIP's ≥ 25%. No primary result of Paper B appears in FAIR. Re-estimate on the final manuscript with a text-overlap tool, and disclose FAIR in the cover letter.

The two-way overlap with the companion paper (under review) is Table 7.1 of the main text (`sec7_limitations_ethics.md` §7.3).
