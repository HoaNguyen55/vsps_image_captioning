# R14-2: Preference optimisation and RL that move CIDEr, object F1 and CHAIR_i together

2026-10-15. Desk research plus repository reading; no GPU, no commits. Base system: P1 LoRA SFT on Qwen2.5-VL-7B
(KTVIC test CIDEr 148.2, 3-seed mean; CHAIR_i 0.183; 1.82 mentions/caption). P1_dev on dev300: CIDEr-D 144.33,
CHAIR_i 0.2325, m 1.763, F1 54.57 (P 74.29 / R 43.13) (rl/g1_cn_v3_s42/gate.json; M3 REPORT sec. 3e).

## 0. Bottom line
- Most published hallucination-DPO methods buy precision with coverage (sec. 2, table). Only a few report BOTH a coverage
  gain and a hallucination drop. HALVA, the strongest of these, uses count-preserving substitution pairs plus a token KL.
- At a fixed object count m, a TP gain raises P and R in the same proportion, so F1 rises and CHAIR_i falls together.
  The count-matched designs (M3, CM-RFT) therefore aim at "both", not "precision only".
- Ranking: (1) M3 CM-DPO, with one HALVA-KL fallback arm; (2) CM-RFT, count-matched rejection-sampling SFT on M3's pool;
  (3) a P/R-reward count-stratified RLOO on held-out UIT-ViIC train images, run only if (1) or (2) passes.
- Dropped: a CIDEr-only RL rerun (35_e); a detector reward on KTVIC (R9 C2/C4: tags vs union P 34.3, R 22.0;
  CIDEr -13); training on public English preference sets (count channel, sec. 1); any OpenViIC training (eval-only).

## 1. Constraints from our own runs
- 35_e (N11; CN-RLOO, CIDEr-D-only reward, k = 8, T 1.0, lr 2e-5, KL beta 0.03, 1,000 KTVIC train images, all of
  them P1 SFT targets): dev CIDEr-D +1.57 [-6.26, +9.55] < gate 3.0. Exact-copy rate 0.67% -> 2.25% (limit 1.33%).
  In-run dev CIDEr dipped to 138.3 at step 250. m 1.763 -> 1.793. CHAIR_i 0.233 -> 0.216. Count-matched endpoint
  +2.07 [-0.19, +4.24], post hoc. Reading: on memorised images, the CIDEr reward has little headroom and pays for copying.
- E5 group-relative RFT (CIDEr + precision): residual -0.15 [-2.55, +2.06]. E5 offline DPO: -1.97 [-4.33, +0.18],
  CIDEr -26.7, CJK 4.1%. Only 24.4% of E5's pairs were count-matched. MR5 (SFT on all 5 refs): +0.25 [-2.10, +2.54].
- Public preference data (Paper A Tab. 9.1): the chosen response names fewer objects in 0.70-0.90 of count-unmatched
  pairs for HA-DPO, HSA-DPO, SENTINEL and RLHF-V. The share is about 0.50 for RLAIF-V and mDPO, and 0.444 for POVID.
  Whole-response ranking (RLAIF-V) is roughly count-neutral; edit or rewrite pairs are not.
- Dev300 power: the paired CIDEr CI half-width is about ±8, so CIDEr can only be a non-inferiority guard, not a
  selection target. The object-F1 residual CI is ±1.3-2.0.
- M3 gate: M3 runs only if EV-RANK within-cell AUROC >= 0.58. The kNN prior gave 0.5806 (KTVIC gold) and 0.5395
  (panel) on test, and it was killed.

## 2. Literature: what moves coverage AND precision (IDs checked against Semantic Scholar records)
Coverage = AMBER Cover or object recall. "Both" means coverage rises AND CHAIR/hallucination falls vs base or SFT.
| Method | arXiv ID, venue | Signal / pairs | Coverage | Hallucination | Both? |
|---|---|---|---|---|---|
| HALVA (DPA) | 2405.18654 (ICLR 2025 per M3 report; v3 page shows no venue) | GT-concept swaps, phrase loss + token KL | Cover 51.0->53.0 (7B), 51.9->52.6 (13B) | CHAIR 7.8->6.6; 6.6->6.4 | YES (small) |
| SC-Captioner | 2508.06125, ICCV 2025 | reference-matched add/remove reward, policy gradient | vs SFT: obj R 62.68->66.00 | obj P 79.99->80.20 (DPO: 78.78) | YES vs SFT (P below zero-shot 83.69) |
| CCCaption | 2602.21655 (CVPR 2026 poster page) | GRPO, completeness + correctness judges (Qwen3-VL-2B) | Prism 50.05->52.80 | Halluc. avg 70.19->70.57 | YES (tiny); CapRL-3B correctness -0.86 |
| plain DPO (mDPO's table) | 2406.11839, EMNLP 2024 | VLFeedback pairs | LLaVA Cover 51.8->55.1 | CHAIR 7.4->6.5 | YES on LLaVA; NO on Bunny (75.6->74.1) |
| mDPO | same | image-conditional + reward anchor | LLaVA 51.8->52.4; Bunny 75.6->67.4 | 7.4->4.4; 9.8->4.9 | mixed |
| FeedQuill | 2503.07906, ICLR 2025 | PPO, r = precision + 0.5 x #units | DCScore F 24.5->34.5 (no separate R) | CHAIR_i 25.3->2.6 | unclear; count-only reward 10.03 (< base) |
| BalCapRL | 2605.07394 (arXiv) | c-GDPO, prec + rec + linguistic | DCScore 43.3->52.0 (no separate P/R) | n/a | unclear; w/o length mask -> length 81 |
| OPA-DPO | 2501.09695, CVPR 2025 (S2) | on-policy + GPT-4V minimal edits | Cover 51.6->47.9 | CHAIR 7.7->2.2 | NO |
| RLAIF-V | 2405.17220, CVPR (S2) | self-sampled, claim-level open labeler, iterative | Cover 51.6->50.4 (OPA-DPO Tab.) | 7.7->3.0 | NO (small loss) |
| HSA-DPO | 2404.14233 (arXiv) | fine-grained AI-feedback edits | 13B Cover 47.3 (base 51.9) | 2.1 | NO |
| CHiP | 2501.16629, ICLR 2025 (S2) | visual + hierarchical DPO | Muffin 48.3->45.3; LLaVA-1.6 61.0->57.8 | 8.0->4.4; 8.3->3.7 | NO |
| V-DPO | 2411.02712, EMNLP 2024 (S2) | vision-guided (CFG-like) DPO | 51.0->49.1 / 49.7 | improved | NO |
| HA-DPO | 2311.16839 (arXiv) | GPT-rewritten pairs | 51.6->52.1 | 7.7->7.8 | no effect (OPA-DPO Tab.) |
| TPO / TPR | 2411.17265 (NeurIPS 2025 poster; renamed) | topic-level self-resampling + rewrite | not reported | ObjHal CHAIR_i 25.2->2.2 | unknown |
| SENTINEL | 2507.12455, ICCV 2025 (S2) | in-domain sentence pairs, GDINO+YOLO-World cross-check, C-DPO | not reported; GPT "detailedness" 8.21->8.32 | ObjHal Ment. 28.0->2.6 | unknown |
| RLHF-V | 2312.00849, CVPR 2024 | dense human corrections | not verified | improved | unknown |
| DOPA/SCAPO | 2609.35294 (arXiv, 2026-09) | dense presence/absence reward, subsentence credit | claims "beyond saying less"; abstract only | | unverified numbers |
| OCS-PPO | 2610.14976, IEEE Access 2026 | correctness + coverage object reward, InstructBLIP | numbers not on abs page | -41% COCO | unverified split |
| CapRL | 2509.22647 (arXiv) | QA-accuracy reward (vision-free LLM) | Prism +8.4% avg | correctness -0.86 (CCCaption Tab.) | NO evidence |
| Visual-RFT | 2503.01785, ICCV 2025 | IoU / class verifiable rewards | detection and classification, not captions | | n/a |
| GRPO / SCST | 2402.03300; 1612.00563 (CVPR 2017); 2503.01333 (arXiv); 2302.08242 (ICML 2023) | CIDEr reward | CIDEr gains on small or non-LVLM captioners (2503.01333: +2.4% over SCST) | | CIDEr only |
Displacement risk: Razin et al. 2410.08847 (ICLR 2025): DPO on near-identical pairs lowers the chosen likelihood.
Readings:
(a) Methods that edit away hallucinations (OPA, HSA, CHiP, V-DPO) lose coverage; Tab. 9.1 shows why.
(b) The "both" cases are count-preserving (HALVA swaps), reference-matched on both sides (SC-Captioner), or rewarded
    on both sides with a length/linguistic guard (CCCaption, BalCapRL). Effects are +0.4 to +3.3 points, not large.
(c) A count or length-only recall reward is hacked (FeedQuill cr-only 10.03; BalCapRL length 81 / 375; R9 C4
    inventory argmax on 30-34% of images under an F1-only reward).

## 3. Pair and reward sources for Vietnamese without new annotation
- KTVIC: 5 references per train image. Union = gold for labels. LOO / split references (choose with 0-1, score with
  3-4; R10 item 9) for any held-out check. Labels are human; candidates come from the model, flagged [MH].
- UIT-ViIC train: 2,562 images (133 Karpathy-test and 59 manifest overlaps removed; M3 out/uitviic_train_keep_ids.json)
  with COCO instance labels. These are existing human labels; P1 never trained on these captions, so there is no copy
  channel.
- The model's own samples: the pool of 12 samples (T 0.5 / 0.8) already specified for M3.
- Detector tags: KTVIC-harmful (sec. 0). Not a reward on KTVIC. Allowed only as a disclosed [MH] feature on COCO
  images, and not proposed here.
- OpenViIC panel: evaluation only (secondary truth-side check). Never in pairs, rewards, selection or stopping.

## 4. Proposals
### P-1 (rank 1): M3 CM-DPO as designed (research_r10/M3/REPORT.txt sec. 4), plus one fallback arm
- What: DPO on the policy's own same-k, |dsyl| <= 2 sample pairs; winner has more union-gold classes; SFT anchor
  alpha 1.0; beta 0.1; lr 5e-6; 1 epoch; about 2,000 pairs on the 1,000 RL images.
- Fallback arm A-KL (pre-registered, runs ONLY after a guard kill on G2/G3): replace the anchor with HALVA's token-wise
  forward KL to pi_SFT on the chosen response (alpha 0.4, as in HALVA 7B), lr 2.5e-6.
- GPU-h (1x RTX 3090, QLoRA): stage 1 4.2 (sampling 2.1, DPO 1.8, dev eval 0.3); A-KL +2.1;
  stages 2-3 per M3 (~29); total <= 35.
- Why both metrics move: at fixed m, dTP > 0 gives dP = dTP/M and dR = dTP/G, both > 0; CHAIR_i falls by about dP/100.
  Literature support: HALVA (Cover +2.0, CHAIR -1.2) is the closest published effect of count-preserving pairs. The
  in-house ceiling at fixed count is +6.64 [+4.72, +8.66] in-sample and +4.64 split-annotator; vote share only +0.24.
- Expected (dev300 vs P1_dev): d-res +0.5 to +2.0 F1; dCHAIR_i -0.005 to -0.020; |dm| <= 0.10; dCIDEr in [-3, +2].
- Gate note (for the judge): the AUROC >= 0.58 gate tests EV-RANK's probe, not M3's signal. M3's split-annotator
  +4.64 is direct held-out evidence. Recommend replacing the gate with M3's own stage-1 gate. Judge decision required;
  not decided here.
- 35_e risk and avoidance: no CIDEr reward, so there is no gradient toward copying references; the copy mask drops
  pairs at m >= 0.90; add guard G6 copy rate <= 2x P1_dev (R10 item 3); the anchor is on the first human caption,
  not on model text.

### P-2 (rank 2): CM-RFT, count-matched rejection-sampling SFT (expert iteration) on M3's pool
- What: for each of the 1,000 images, take from the 12-sample pool the sample with the SAME k as P1_dev's greedy that
  has the most union-gold classes (ties broken by LOO CIDEr-D). Keep it only if its TP > the greedy's TP. LoRA-SFT 1
  epoch, lr 1e-5, response-only CE, mixed 1:1 with the image's first human caption (count-neutral).
- No NLL on count-biased winners (the RPO concern in M3 sec. 2): k is pinned to the greedy's k.
- GPU-h: 0 sampling (reuses M3's pool), SFT about 0.4, dev eval 0.3, so 0.7. At 3 seeds for test: +2.5.
- Evidence: the fixed-count oracle above; SC-Captioner/ReST-style supervised self-training realises part of best-of-n
  headroom without DPO displacement. M3's own estimate is that the policy realises 10-30% of the headroom.
- Expected: d-res +0.3 to +1.5; dCHAIR_i -0.003 to -0.015; dCIDEr in [-2, +1]. Lower ceiling than P-1, lower risk.
- 35_e risk: no RL and no CIDEr reward; the targets are model text at P1's own count. Copy guard as P-1 (drop targets
  with m >= 0.90).
- Role: also the cheap attribution control for P-1 (is the preference contrast needed, or does SFT on winners suffice?).

### P-3 (rank 3; conditional): count-stratified RLOO with a precision-and-recall reward on held-out images
- What: CN-RLOO engine (train_rl.py, k = 8), reward r = CIDEr-D_LOO + w x (TP - lam x FP), using COCO instance labels
  on 1,000 UIT-ViIC kept images, plus union gold with LOO refs on 1,000 KTVIC images. Count-stratified baseline
  (M4 CS) so there is no gradient on count. lam set so the break-even precision equals P1's dev precision (0.74).
- SC-Captioner and CCCaption are the published two-sided rewards; R9 C4 estimated F1 +1.6 to +2.7 over CIDEr-only RL
  at CIDEr -1 to -5.
- Preconditions: the judge reopens RL (D14); P-1 or P-2 passes stage 1 (the signal must be learnable off-line first).
- GPU-h: first look about 4.0 (as M4) + UIT-ViIC val eval 0.5 + KTVIC dev 0.3, so about 5; full about 22.
- Expected: dev d-res +0.5 to +2.0; UIT-ViIC val instance F1 +2 to +5 at |dm_coco| <= 0.15; dCIDEr in [-5, +1].
- 35_e risk: half the images were never SFT targets (copy channel absent); the KTVIC CIDEr term uses LOO refs; the
  object term breaks the "CIDEr only" plateau; an inventory/list guard (R9 C4: >= 2 commas or > max-ref classes + 1);
  copy guard <= 2x step 0. Biggest remaining risk: UIT-ViIC sports-domain style drift lowering KTVIC CIDEr (guard).

## 5. Dev300 selection plan (all proposals)
- One frozen config per proposal plus at most the one fallback named above. No hyperparameter search on dev300; the
  checkpoint is the last step (no best-of-checkpoints; the gate v2 lesson).
- Paired image bootstrap B = 2000 (numpy default_rng(0)) vs P1_dev greedy; frozen frontier at(); matcher v2 pinned,
  v3 side by side.
- Primary: d-res (frontier residual F1). Co-reported: dP, dR, dCHAIR_i, dm, CIDEr-D, B-4.
- Guards: |dm| <= 0.20 (P-3: 0.15); dev CIDEr-D >= 141.33 (P0 punctuation protocol, declared); CJK <= 1/300;
  syllables in [10.69, 13.06]; fragments <= 15; copy rate <= 2x P1_dev.
- Truth-side (secondary, never selects): OpenViIC panel count-matched rho_I on 296/300 dev images; dev
  kappa = d_rho_I / d_rho_A reported.
- Order: P-2 and P-1 stage 1 share one pool (2.1 GPU-h) and run back to back (about 5 GPU-h total). P-3 only after one
  of them passes.

## 6. Prereg sketch (frozen predictions, kill rules)
| ID | Prediction (dev300 unless noted) | PASS | KILL |
|---|---|---|---|
| P-1 H1 | |dm| <= 0.10 | - | |dm| > 0.20 (G1) |
| P-1 H2 | d-res in [+0.5, +2.5], point +1.2 | d-res >= +1.5 and LB > 0, all guards | d-res < +0.5 or any guard |
| P-1 H5 (new) | dP > 0 AND dR > 0 (both LB reported); dCHAIR_i <= -0.005 | both point estimates > 0 | dR < 0 with LB > 0 (precision-only drift) |
| P-1 test | 3-seed pooled residual > 0, CI excl. 0 (T1); vs C2 LB > 0 (T2) | T1 and T2 | T1 fails, or CIDEr loss > 3, or CJK > 0.5% |
| P-2 | d-res in [+0.3, +1.5]; |dm| <= 0.05 by construction | d-res >= +1.0, LB > 0 | d-res < +0.3 or guard |
| P-2 vs P-1 | P-1 - P-2 >= +0.5 (contrast adds signal) | reported | no kill; attribution only |
| P-3 | d-res in [+0.5, +2.0]; UIT-ViIC val dP_inst > 0 at |dm| <= 0.15 | d-res >= +1.0, LB > 0, dCIDEr >= -3 | otherwise; no rerun |
| All | test CIDEr within 148.23 - 3 (non-inferiority) | | below that: report as negative |
A null result on all three is reported as a pre-registered negative and supports "count explains the object metric".

## 7. Risks
- Power: true effects of +1 to +1.5 F1 have about 40-50% PASS probability on dev300. GREY continues to stage 2 only
  under M3's rule.
- Likelihood displacement (P-1; 97.6% one-object swaps): anchor or KL plus guards; P-2 has none.
- Typicality, not truth: union gold rewards naming habits (>= 12% of pairs are naming variants). Panel rho_I and COCO
  instance labels are the truth checks.
- CIDEr is unlikely to rise meaningfully for any proposal. Expected CIDEr movement is within ±2; no published method
  shows a CIDEr gain on top of a 148-CIDEr SFT LVLM, and 35_e is our in-domain counter-evidence.

## 8. Ranking
1. P-1 M3 CM-DPO (+A-KL fallback): best evidence for both P and R (count-preserving pairs, HALVA analogue), 4.2 GPU-h,
   code ready; P(stage-1 PASS) about 0.3.
2. P-2 CM-RFT: 0.7 GPU-h on the same pool, lowest risk, smaller ceiling; P(PASS) about 0.2-0.25; serves as control.
3. P-3 P/R-reward CS-RLOO on held-out images: most published support for two-sided rewards (SC-Captioner, CCCaption),
   but blocked by D14 and conditional on 1 or 2; P(PASS | 1 or 2 passed) about 0.35.
Not recommended: RLAIF-V / OPA-DPO / CHiP / V-DPO / HSA-DPO replications (coverage loss on AMBER), CapRL-style QA
reward (correctness drop, needs an LLM judge in Vietnamese), detector reward on KTVIC, CIDEr-only GRPO.
