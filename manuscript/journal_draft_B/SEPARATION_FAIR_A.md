# Separation note: merged Paper B+D vs FAIR 2026 and Paper A (for a second reviewer)

Date: 2026-10-29. Writer B; AI-prepared, not expert-validated. Required by Codex CC-166 ("a second independent reviewer confirms FAIR/A separation and source-number reconciliation") before the merged paper is submitted.
Scope: `manuscript/journal_draft_B/` (main text sec1–sec8, outline abstract, supplement). Paper D is merged into B (PI-1029n). **D is not submitted standalone.**

## 1. The three papers

| | FAIR 2026 (published, IEEE) | Paper A (in preparation, SPIC) | Merged Paper B+D (this folder, LRE) |
|---|---|---|---|
| Question | Can verified-proposition supervision (VSPS) reduce hallucination in detailed Vietnamese captions? | When does an object-level hallucination score support a comparison between systems? | What does a KTVIC score, and a gain in it, measure? |
| Primary evidence | VSPS method; P1 gold-SFT baseline (seed 42, CIDEr 149.8); human rating | count/gold-completeness slope (XM3600), exchangeability statistic, English data (COCO, Flickr30k), LVLM rankings | KTVIC audit (single writer, punctuation, segmentation, matchers, overlaps); P1-R instrument; B-1 training-set size (dev); D0 and B-R1 two-panel studies (dev) |
| Data | KTVIC, COCO | XM3600, UIT-ViIC, COCO, Flickr30k, UIT-OpenViIC (aggregates); no primary KTVIC number | KTVIC (primary), UIT-OpenViIC panel of KTVIC images (aggregates), UIT-ViIC, XM3600 (punctuation only); no English data |

## 2. What is new against FAIR 2026

`new_vs_FAIR.md` carries the item-by-item table. The merge adds these rows, none of which is in FAIR:
- B-1 training-set-size study on dev300: three seeds × five sizes, registered rule, PASS, +9.61 [7.18, 12.36].
- D-α extrapolation test: INCONCLUSIVE.
- D0 two-panel gate: GO, +10.59 against +0.72.
- B-R1 reverse direction: ASYMMETRIC/O5b.
- Matched-design and masked rows (post hoc, descriptive).

**Reused from FAIR, and disclosed:**
- the KTVIC/COCO setup;
- the QLoRA recipe on Qwen2.5-VL-7B (B-1 and B-R1 use the P1 recipe);
- the P1 seed-42 score, as a reference point;
- the v1 lexicon, as matcher v1;
- related-work citations.

The VSPS method, its verifier and FAIR's human ratings are not used.

**Text check (writer, 2026-10-29).** Method: lower-cased word tokens of the sec1–sec8 text with HTML comments removed, compared against `pdftotext` of `manuscript/FAIR_28.08.26_v10_EN_IEEE.pdf`.
- 8-word sequences: 3 shared out of 13,681. All three come from one sentence that names FAIR's method in sec1: "builds supervision for detailed Vietnamese captioning from verified propositions".
- 12-word sequences: 0 shared.

## 3. What is new against Paper A

Supplementary Table S13.1 states each paper's claims and data. No number is a primary result in both papers. Specific points:
- **KTVIC.** A reports no primary KTVIC number. B owns all KTVIC results, including B-1, D0 and B-R1.
- **UIT-OpenViIC.** A uses its captions of KTVIC test images for the exchangeability statistic (aggregates). B uses the same panel on KTVIC *test* images for §5.3 (aggregates). B also uses it on 187 *dev300* (KTVIC-train) images for D0/B-R1, a set A does not use.
- **System outputs.** A scores B's KTVIC-trained P1 and fuse2 outputs on XM3600 and UIT-ViIC for its own claims. B reports those outputs only for its punctuation and transfer audits. This sharing is disclosed in both papers (S13).
- **Text check (writer, 2026-10-29).** Same method, B (sec1–sec8 + outline) against A (`manuscript/journal_draft/sec*.md`).
  - 8-word sequences: 13 shared out of 15,578. 12-word sequences: 2 shared:
    - the AI-assistance provenance sentence ("…analysis code was written with AI assistance under the authors' direction");
    - one phrase about XM3600's null ("…COCO and UIT-ViIC sit at the null").
  - Both should be reworded in one of the two papers before submission. The provenance sentence may stay identical if the venues allow boilerplate; reviewer to decide.
- **Figures.** B has no figure files. A's figures (`journal_draft/figs/fig2_slope_by_gold`, `fig4_lambda_channels`) are not used in B.

## 4. Shared kit (disclosed, not a shared contribution)

These tools are shared:
- the scorer (kit B: VnCoreNLP RDRSegmenter, CIDEr-D ×100, trailing-punctuation stripping);
- the matchers v1/v2 and the count-matched controls;
- the exchangeability statistic.

Their ownership:
- The count-matched controls and the exchangeability statistic are **defined and validated in A**. B uses them as tools, cites A, and claims nothing for them (S13.1 rows "Count-matched controls", "Exchangeability statistic").
- The protocol card and the evaluation kit are **B's contribution**. B's Zenodo deposit holds only B's components (Table S14.2), and A has its own archive.
- Neither paper may present a common-kit component as an independent contribution of both.

## 5. Source-number reconciliation (for the second reviewer)

Every number in B's main text and abstract has a row in `number_manifest_B.tsv` with a file, a key and a sha256 prefix. The merge rows are tagged `MERGE-SCOPED PI-1029n`. Decided files and their pins:

| Result | File | sha256 |
|---|---|---|
| B-1 (PASS) | `.session_backup/machines/M4/root/outputs/b1_scaling/decide.json` | b44a76fe… (pinned in D0 RULE §1) |
| D-α (INCONCLUSIVE) | `.session_backup/2026-10-28/d_extrap` | f0eb2b9e… |
| D0 (GO) | `manuscript/prereg/2026-10-29_b_d0/d0_decide.json` | 15dd925f… |
| D0 masked re-read (post hoc) | `manuscript/prereg/2026-10-29_b_r1/d0_reread.json` | 7853ab4a… |
| B-R1 (ASYMMETRIC; O5b per LOG CC-163 W9) | `manuscript/prereg/2026-10-29_b_r1/b_r1_decide.json` | a6627047… |
| Matched design (post hoc) | `manuscript/prereg/2026-10-29_b_r1/b_r1_matched.json` | fa58ab8c… |

Two known discrepancies, both disclosed in §5.5:
- **Forward CI.** D0's decided CI is [6.71, 13.35]. B-R1's recomputed CI is [6.63, 13.43], with the same point estimate. The text quotes D0's.
- **Minus-2004 row.** D0's minus-2004 descriptive row (g 9.99) predates the id-order fix. The text uses the re-read's masks instead.

## 6. Reviewer checklist

- [ ] No primary number appears in both A and B (S13.1; compare `number_manifest.tsv` with `number_manifest_B.tsv`).
- [x] The two shared 12-grams with A were reworded in B on 2026-10-29 (sec3 null sentence, sec7 AI-provenance sentence); the shared 12-gram count is now 0.
- [ ] The FAIR overlap is limited to the disclosed reuse rows of `new_vs_FAIR.md`.
- [ ] D0/B-R1 wording: dev-only, O5b, no transfer claim, no "first"; ViCLIP-OT credited for the overlap count; Bromonschenkel 2026 positioned.
- [ ] The cover letter states that the training-set-size and two-panel studies are not submitted separately.
