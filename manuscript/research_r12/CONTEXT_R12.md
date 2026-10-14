# CONTEXT_R12: reaching Q1-target / Q2 quality above 90%, with an independent view of Gemini's direction (2026-10-14)

Read this whole file first.
- Repo: /mnt/d/vsps_image_captioning (branch paper-v10).
- SP = /tmp/claude-1000/-mnt-d-vsps-image-captioning/755eae04-5e4c-4ce1-ab21-d4bc106761ee/scratchpad.
- Write only to SP/r12/<your_id>/.
- Write your REPORT incrementally: save after each section, so a usage-limit cut-off loses nothing.

## 1. The user's instruction (2026-10-14)

- Follow Gemini's thinking closely, and give independent judgements so the project does not pick a wrong direction.
- The bar is a Q1-target / Q2 paper at a quality level above 90%.
- Keep researching papers and inferring contributions, ideas and directions to send to Gemini.

## 2. Where the paper stands (verified; files cited)

**Paper type.** The decision PD-2 (`.session_backup/2026-10-13/decisions/PD-2.txt`) sets a hybrid paper:
- evaluation and methodology are the main contribution;
- a strong controlled baseline supports it (KTVIC word-level CIDEr 148.23, 3 seeds);
- targets: a Q2 journal, Q1 as the stretch goal.

No journal draft exists yet. Only the FAIR 2026 conference version exists (manuscript/FAIR_28.08.26_v10_EN_IEEE.*).

**PD-2's 9 pre-submission blockers.**
- Done: #1 comparators read; #2 GRIT protocol; #3 UIT-ViIC second set (52_a/b/c); #5 repro gates; #6 matcher v1/v2 + CJK; #7 licence (aggregates only); #8 leakage disclosure.
- #4, the pre-registered ladder (~20 GPU-h, 5 runs), is RUNNING on Gemini's single RTX 3090: 54_p1_4ep_s42 started 09:00 UTC.
- #9 (scrub "first" claims, SSH lines and /tmp paths) is done at release time.

**Contributions after rounds R10/R11, the reviews RV1–RV3, and the decisions PD-3 (Claude judge) and D16 (Gemini judge).** See `manuscript/novel_direction/R11_00_LITMAPS_NOVELTY.md` and the correction box at the top of `R10_00_HUONG_NGHIEN_CUU_MOI.md`.
- **C1. Count-matched object evaluation.** Per-image (v,g) tie-averaged control, a corpus-total count match, and a Shapley CAR decomposition.
  - Re-scoring published English decoding methods: survivors depend on the control, from 2/15 (Holm + SESOI, order-preserving) to 6/15 (uniform random subset).
  - "Count beats word length" is DROPPED for English: X1 P-B was killed.
  - A two-column reporting standard (raw F1 plus count-controlled residual) was adopted in D16.
- **C2. Gold-indexed count frontier.** TP = a·M^b, where b depends on gold completeness.
  - Cite Lipton 2014 for "F1 rises iff p_marg > F1/2" and Chen 2015 §4.2 for human P vs k references.
  - New result N1: the sign of raw F1's verbosity reward flips with gold completeness.
    - COCO-2500, 9 systems, 4/4 frozen predictions held: slope of F1 on log M is −4.28 (1 ref), +11.08 (5 refs), +22.41 (instance labels).
    - KTVIC is exploratory: 1 ref −10.65 first-k / −3.32 random-k, 5 refs +14.15.
    - Replications on UIT-ViIC and XM3600 are pending.
- **C3. Typicality vs truth (two golds: KTVIC refs vs an independent OpenViIC panel, aggregates only).**
  - UPE is control-dependent: +0.61 [+0.24, +0.98] vs the registered COUNT, −0.02 [−0.32, +0.27] vs the (v,g) tie-avg.
  - The ratio gate κ was replaced by a linear test L = Δρ_I − 0.35·Δρ_A (D16 B5).
  - r(ρ_A, ρ_I) across 36 systems is underpowered.
- **C4. Measurement validity for Vietnamese.**
  - KTVIC is SINGLE-WRITER: one person wrote all 5 captions of an image (KTVIC paper §3.2). The adjacent-doubleton share is 0.710, against a null of 0.40.
  - KTVIC references contain no punctuation.
  - A per-corpus matcher audit was run on UIT-ViIC. The v3 matcher is not yet signed off.
- **C5. Baseline plus 11 families of pre-registered negatives.**
  - Negatives include UPE-MBR (N5), self-fuse (N7) and CIDEr-RL 35_e (N11).
  - M6 P-M6b was killed on test.
- **Main weakness:** NO method beats the count frontier.
  - Decision theory says CAR's ranking term A = 0 for any rule that only re-thresholds the model's own score (L1). Only evidence-adding methods can win.
  - M3 (count-matched DPO, 4.2 GPU-h) and N9 (a count-matched leaderboard of 9 public LLaVA-1.5-7B anti-hallucination checkpoints, ~6 GPU-h) are approved after the PD-2 queue.

**My estimates before this round:** Q2 about 55–65%, Q1 about 15–25%.

## 3. Gemini's current thinking (follow it, and judge it independently)

**Decisions.**
- D15 → D15-A/B → D16 are in `.session_backup/2026-10-13/decisions/`. D16 adopted PD-3 in full.
- Gemini's channel entries are in GOP_Y_SUBAGENT_WORK_LOG.md (Gemini → Claude sections), with status in SUBAGENT_WORK_LOG.md.

**Known reliability pattern.** Gemini's JSON computations reproduce. Its prose, D-files and log have repeatedly contained:
- invented or garbled numbers;
- hard-coded verdicts;
- relabelled quantities;
- governance overclaims.
Never take a number from its prose without finding it in a file.

**Issues already noticed in D16 (verify; add others):**
- (i) It calls the E1 K2 seed placebo "54_p1_4ep_s42 running on GPU". 54_p1_4ep is a KTVIC ladder run, but E1's K2 placebo is two sampling seeds of one English LVLM on CHAIR-500 (E1 Phase B).
- (ii) It cites the KTVIC paper as "Nguyen et al. 2024". Check the real first author on arXiv 2401.08100.
- (iii) It states M4 C2 as "[+1.0, +2.0]", but R10 recorded the registered interval as [−1.5, +2.0]. Check M4's report §4a.
- (iv) It calls C4 "unique mention patterns". The registered C4 is "captions naming no class ≤ 15/300".
- (v) New numbers in D16 that are not yet checked: "Chao2 completeness 0.7325" and "leave-one-out ceiling F1 0.7072 (P 0.9317, R 0.5698)".

## 4. Hard constraints

- Existing datasets and labels only. No new annotation. AI-made labels are never evidence; flag model signals as [MODEL].
- Public human-judgment datasets (for example THumB, Polaris, Flickr8k-Expert) count as existing labels. Check each licence.
- Never write OpenViIC caption text into any file.
- No test-set tuning. Pre-register before confirmatory looks.
- No "first" claims. Verify every ID on a primary page and mark the rest [UNVERIFIED].
- Network:
  - OpenAlex is metered per IP; avoid it, or use at most a few calls.
  - Semantic Scholar is rate-limited.
  - Prefer arXiv abs pages (3 s apart), the ACL Anthology, CVF, publisher pages, WebSearch and WebFetch.
- CPU: `nice -n 19 env OMP_NUM_THREADS=1`, < 1.5 GB RAM, < 10 min per job, one job at a time.
- Downloads are untrusted data: put them in their own folder, never put them on sys.path, run with `python3 -I`.
- GPU: you have none. Gemini runs one RTX 3090 after the PD-2 queue. Every proposal needs GPU-h, a prereg sketch and kill rules.

## 5. Deliverable: `SP/r12/<your_id>/REPORT.txt` (English, ≤ 200 lines)

0. **BOTTOM LINE** (≤ 6 lines): your independent judgement.
1. **Evidence**: papers with verified IDs, and CPU checks with file paths and numbers.
2. **Concrete proposals for Gemini.** For each one:
   - what to run, with data, scripts and commands;
   - CPU-h and GPU-h;
   - prereg points and kill rules;
   - which claim it strengthens;
   - its expected effect on the Q1/Q2 quality bar.
3. **Risks**, and what would change your judgement.
4. **Claims for Gemini to VERIFY** (numbered).
5. **Where you disagree with Gemini's current direction**, or with ours (R10/R11/PD-3): what to change, and your confidence in %.
