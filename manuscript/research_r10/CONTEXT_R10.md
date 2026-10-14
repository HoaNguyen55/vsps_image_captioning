# CONTEXT_R10: shared brief for the 20 R10 research agents (2026-10-14)

Repo: /mnt/d/vsps_image_captioning (branch paper-v10, HEAD 9193a3d). The project is Vietnamese image captioning on KTVIC with Qwen2.5-VL-7B and QLoRA. Read this whole file first.

## 1. What the paper is now (decision PD-2, 2026-10-14)

- **Paper type:** a hybrid. Evaluation and methodology are the main contribution. Strong KTVIC results serve as the controlled baseline.
- **Venue target:** Q2 journal, with Q1 as a stretch.
- **Primary endpoint for every object-level claim:** comparison at matched object count.
  - Selection or decoding methods: paired ΔF1 against a same-count control (top-k_i by raw sample vote share).
  - Training methods: residual against the pre-registered count frontier.
- **Main open problem:** no METHOD survives count control yet.
- **R10 goal:** find research directions that are MORE NOVEL than the current state. That means one of:
  - a method that genuinely beats the count frontier at matched count;
  - an evaluation/methodology contribution of clear, general value;
  - a resource or analysis that reviewers would call new.

## 2. Verified facts (taken from primary files; cite the file when you use one)

- **Response-only P1 baseline, 3 seeds, KTVIC test short** (`data/results/p1assist_s4{2,3,4}-short.json`):
  - per-seed CIDEr 148.66 / 148.06 / 147.96;
  - means (SD): B-4 45.74 (0.13), METEOR 39.16 (0.19), ROUGE-L 64.60 (0.19), CIDEr 148.23 (0.38), CHAIR_i 17.59 (0.65).
- **Word-level CIDEr-D protocol:** VnCoreNLP RDRSegmenter, n=4, σ=6. GRIT 136.0 uses the same protocol, but selected its checkpoint on test and built its vocabulary on train+test (Gemini audit: `.session_backup/2026-10-13/r9_synthesis/KTVIC_PROTOCOL_COMPARATORS.md`). Gemini reports syllable-level CIDEr of 164.25 for the same model. Treat that as Gemini's figure: VERIFY before using.
- **Count frontier** (pre-registered, `manuscript/prereg/2026-10-12_ladder_predictions.json`; tool `scripts/prereg_ladder_check.py`, function `at`):
  - TP per image = 1.3996 · (M/1.7826)^0.7468, where M = object mentions per image.
  - Frontier invariance (the frontier stays fixed across systems) has held on every landed run so far.
- **UPE-MBR** (MBR selection over samples, KTVIC test, 3 seeds; `data/results/upe/test/upe_mbr_ktvic_test.json`):
  - vs greedy: panel F1 +1.91 [+1.45, +2.35] and P −1.05 [−1.74, −0.39];
  - vs the same-count COUNT control: ΔF1 +0.07 / +0.03 / +0.17, so kill 2 fired. UPE is a pure count shift.
- **PLAN-F1** (calibrated object-set planning; dev300 CPU audit, `data/results/planf1/`):
  - plan F1 58.95 at m = 2.63 classes/img, vs greedy 54.53 at m = 1.76;
  - official frontier residual −2.49 [−5.52, +0.09];
  - equal to a raw-vote count-matched control (ΔF1 +0.08 [−0.74, +0.91]) and to plain top-3 (Δ −0.01);
  - within an image, the decision rule ranks exactly like q, so it only sets the count k_i.
- **Human levels.**
  - KTVIC, one annotator vs the other four: P 85.33 / R 46.90 / F1 60.50. Two vs three: F1 70.93 (`data/results/human_parity.json`).
  - Independent second panel (OpenViIC annotators, other guideline) vs the 5 KTVIC refs: F1 44.96 / 53.18 / 55.38 / 55.78 / 56.08 for k = 1..5. Gemini artifact: `.session_backup/2026-10-13/r9_synthesis/PD2_BLOCKER8_CEILING_COCO2500.json`.
  - COCO-2500, human captions vs COCO-80 instance labels: k=1 70.28, k=5 79.46.
- **Reference style matters.** fuse2's precision drop on KTVIC refs (67.21 vs 79.30, detailed) vanishes against COCO-80 instance labels (88.94 vs 89.84). The C3 panel confirms that 56.5% of P1's "false positives" are real objects.
- **Model sees more than it says.**
  - POPE seen-rate for small/medium/large objects is 67/88/96%, but short captions name 7/24/56% (R9 C7).
  - 81.6% of P1's misses are named by ≥2 of 70 other outputs (R9 C8).
- **COCO transfer** (`data/results/coco_transfer/`): instance F1, short / detailed:
  - zero-shot 63.3 / 73.4;
  - fuse2 59.4 / 65.8;
  - P1 59.3 / 59.4.

  Fine-tuning on KTVIC forgets COCO vocabulary.
- **POPE-vi** (`data/results/pope_vi/`): P1 s43 F1 88.2 random (POPE labels), 92.4 under RePOPE labels.
- **Measurement fixes.**
  - Tone-mark normalisation (matcher v2) moves only the zero-shot and legacy rows, by +0.2 to +0.5 F1 (`data/results/tone_norm/SUMMARY.json`).
  - CJK leakage: zero-shot detailed 5.2%; legacy systems 15–42%.
  - The 'cây' classifier is matched as "tree" (e.g. in "cây cầu").
- **KTVIC paper, Table 3:** baseline predictions were segmented, but the references were syllable-level. The original 21.79 / 36.77 reproduce; rescored, they become 48.85 / 72.87 (Gemini audit).
- **Earlier negatives or limits (R6–R9 reports in `manuscript/research_r9/*/REPORT.txt` and `manuscript/research_r8/`):**
  - knowledge-graph methods: not suitable;
  - CN-RLOO realistic gain +2 to +6 CIDEr; the first RL look, 35_e, is running now;
  - resolution is not the bottleneck;
  - a stronger backbone gives about 0 on KTVIC;
  - ≥90% on object metrics is unreachable for honest captions.

## 3. Hard constraints

- **Data:** existing datasets and labels only. No new annotation. AI-made labels are never evidence; flag any model-generated signal used inside a method.
- **OpenViIC:** used only as an evaluation panel. Never train on it. Never write its caption text into any file. Publishing aggregate scores is allowed (user decision U-002).
- **Tuning:** only on dev300 (`data/splits/ktvic_dev300.txt`). Nothing on test. Pre-register before any confirmatory look.
- **No "first" claims.** Claim novelty only against verified prior work. Verify arXiv IDs and DOIs with web search and mark anything unverified.
- **Compute:**
  - GPU: one RTX 3090 (24 GB), run by the Gemini agent system. You have NO GPU and NO ssh.
  - Local CPU: 4 cores and 8 GB shared by 20 agents plus Gemini. Any CPU pilot must run with `nice -n 19 env OMP_NUM_THREADS=1 MKL_NUM_THREADS=1`, use < 1.5 GB RAM, and take < 10 min. Run one pilot at a time.
- **Writing:** write ONLY inside your own folder `research_r10/<your_id>/`. The repo is read-only for you. No commits, pushes or edits of shared files.

## 4. Deliverable: `research_r10/<your_id>/REPORT.txt` (English, ≤ 250 lines)

0. **BOTTOM LINE** (5–8 lines): the idea, why it is new, and the expected value.
1. **Problem and hypothesis:** testable, with falsifiable predictions.
2. **Closest prior work:** ≥ 5 verified references (id + one line each), what is new relative to each, and a novelty rating (high / moderate / low).
3. **Evidence so far:** quick CPU checks on existing files, if any, with numbers and file paths, plus the literature.
4. **Pilot design for Gemini to RUN:**
   - data, steps, exact commands or scripts needed, GPU-h on one 3090, CPU-h;
   - pre-registration points, primary endpoint (count-matched where relevant), kill rules.
5. **Claims Gemini must VERIFY:** a numbered list of facts or citations to check independently.
6. **Risks**, and **fit with the PD-2 paper** (which pillar it strengthens).
7. **Scores, 1–5 each:** novelty, feasibility on 1×3090, expected impact, risk. One line of justification each.
