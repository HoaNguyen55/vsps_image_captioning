# R14 synthesis: metric-improving methods (main, 2026-10-15)

Sources: the four reports `R14_1/REPORT.md` (detector grounding), `R14_2/REPORT.md` (preference/RL), `R14_3/REPORT.md` (multi-sample + independent verifier), `R14_4/REPORT.md` (data/scale).

## Diagnosis that all four reports support

- The model is not capacity-limited, and more KTVIC caption text does not help:
  - 4 epochs instead of 2 gives CIDEr −6.7;
  - training on all 5 refs gives −1.1.
- Self-evidence (re-thresholding the model's own score, self-votes, self-fusion) cannot win (L1). Every past negative is of this kind.
- About 54% of KTVIC "hallucinations" are objects that the independent OpenViIC panel names. This caps any detector/removal method:
  - F1 ceiling +0.6 (OIV7) to +1.7 (open vocabulary);
  - the real Grounding DINO veto gives F1 −3.7.
- The ceiling for reranking at a fixed object count is:
  - +4.2 F1 on held-out refs, but only +0.6 F1 on the panel;
  - CHAIR_i 23.3 → 15–17.
- CIDEr headroom without fitting the references is small. Seed consensus is the most reliable CIDEr lever: the test-pool proxy gives +3.05 [+1.03, +5.11] (exploratory; selection would be done on dev).

## Candidate combined plan (for the judge, PD-9)

### Stage 1: cheap probes, about 13 GPU-h, all selected on dev300 only

| id | method | GPU-h | expected | gate |
|---|---|---|---|---|
| S1 | Seed consensus: delta-space soup / cross-seed MBR (R14-4 A). Needs p1dev_s43/s44. | 4.3 | CIDEr +1..+3 | dev ≥ +1.0 CIDEr |
| S2 | XV-EF1: independent-VLM verifier (InternVL3-8B, scorer only) replaces self-votes in the UPE rule (R14-3 P1). The verifier cache is reused by S4. | 1.5 | F1 vs COUNT +0.5..+1.0; CHAIR_i −1.5..−3 | G0: within-cell AUROC ≥ 0.58; no-image AUROC ≤ 0.60 |
| S3 | M3 count-matched DPO stage 1 + CM-RFT on the same sample pool (R14-2 P-1, P-2) | 5.0 | F1 +0.5..+2 at fixed count | M3 stage-1 gate (R14-2 recommends replacing the EV-RANK AUROC gate with M3's own gate) |
| S5 | Data-scaling probe at 25% / 50% of the training data (R14-4 C) | 1.8 | diagnostic | decides whether any external-data spend is justified |

### Stage 2: run only if the stage-1 gate it depends on passes

| id | method | runs if |
|---|---|---|
| S4 | Verifier-checked count-matched DPO: R14-1 P-B, using the S2 verifier labels instead of the detector | S2 G0 passes, and S3 shows DPO is learnable |
| S6 | LS-BoN selector (R14-3 P2), about 0.3 GPU-h | S2 passes |
| S7 | P/R-reward count-stratified RLOO on held-out UIT-ViIC images (R14-2 P-3) | the judge reopens D14, and S3 or S4 passes |
| S8 | UIT-ViIC translate-train + joint tagged model (R14-4 B), about 8 GPU-h | S5 shows data scaling helps (slope b LB > 1) |

### Final stacked system for the papers

soup(seeds) + DPO adapter (S3/S4) + XV-EF1 selection (S2), evaluated once on test under a single committed prereg.

### Dropped

- detector veto (R14-1 P-A as a method; it stays as an analysis row);
- tag-conditioned SFT;
- CIDEr-only RL;
- VCD / ICD / OPERA / M3ID / AGLA;
- a bigger backbone, as a primary lever;
- synthetic captions for KTVIC.
