# CONTEXT_R14: methods that IMPROVE the metrics (user priority, 2026-10-15)

## Goal

The user puts research ahead of writing. The aim is a method whose output improves the paper's key metrics enough for a Q1/Q2 venue:
- KTVIC test: CIDEr, BLEU-4, object Precision/Recall/F1, CHAIR_i;
- UIT-ViIC test;
- COCO object F1;
- XM3600.

## Current best (KTVIC test, 558 images, word-level rdrsegmenter, ×100)

| System | CIDEr | B-4 | CHAIR_i | mentions/caption |
|---|---|---|---|---|
| zero-shot Qwen2.5-VL-7B | 28.98 | 5.48 | 0.429 | – |
| p1assist_s42 (P1 LoRA SFT) | 148.66 | 45.88 | 0.183 | 1.82 |
| fuse2_s42 | 143.90 | – | 0.219 | – |

- The 3-seed P1 mean is 148.23 (SD 0.38).
- Object P/R/F1 per system: see `data/results/*.json` keys `chair` and `results`, and the object PRF files in `.session_backup/2026-10-14/r11_verify/`.

## What already FAILED (pre-registered negatives; do NOT propose these again unless the change is substantive)

- UPE-MBR; self-fuse k=1 (it hurts relations); CIDEr-RL 35_e (N11); M6 P-M6b; text-kNN prior (KILL on test, 2026-10-14); constrained-LM pilots; VCD on the COCO probe (see `coco5000_scores_vcd.json`).
- Decision theory (L1): any rule that only re-thresholds the model's own score has ranking term A = 0, so it cannot beat the count frontier. Only methods that ADD EVIDENCE can win: external detectors or grounding, multi-sample agreement with a verifier, extra training signal, or more or better data.
- Already approved but not yet run: M3 (count-matched DPO, 4.2 GPU-h; runs only if the within-cell probe AUROC is ≥ 0.58), EV-RANK (prereg ca644df), N9, WiSE-FT (59).
- Ladder (multiref SFT 56–58): the pre-registered prediction is NO frontier change (joint residual −0.54 [−1.55, +0.54]).

## Resources

- 2× RTX 3090 24 GB, rented: O-2293424 and O-2293440.
- Base model: Qwen2.5-VL-7B. Qwen2.5-VL-3B is available as a fallback. Qwen3-VL failed its guard (3% CJK).
- Experiments freeze 2026-11-15, so about 30 days and about 1,400 GPU-h in total. GPU work is run by Gemini; Claude designs, pre-registers and reviews.
- Local machine: 4 cores, 8 GB RAM, CPU only.

## Hard rules

- Existing datasets and labels only; no new human annotation. AI labels are never EVALUATION evidence. They may be used as training signal, but must be disclosed.
- No test-set tuning: select on dev300 only. Pre-register before any confirmatory look.
- No "first" claims. Verify every paper ID on its primary page.

## Repo pointers

- Earlier method research: `manuscript/novel_direction/R6_00_PHUONG_PHAP_DOT_PHA.md`, `R9_00_MUC_TIEU_90_PHAN_TICH.md`, `R10_00_HUONG_NGHIEN_CUU_MOI.md`, `R11_00_LITMAPS_NOVELTY.md`.
- Paper drafts: `manuscript/journal_draft/`.
- Literature: `manuscript/research_r13/R13_LIT_UPDATE.md`.
