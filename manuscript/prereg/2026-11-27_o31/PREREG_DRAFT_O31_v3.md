# PREREG DRAFT O31 v3: retention-first verified-proposition fine-tuning (Objective 3.1, RQ8)

Status: DRAFT v2, not committed. Nothing in it has run. v1 (86905b51) written 2026-11-27 by the o31-plan agent; v2 folds in CC-501 (CONDITIONAL GO 87): W1-W4 verbatim and N1, N2, N4, N6, N7, N8, N11. Hunk map: `PREREG_V1_TO_V2.diff` and `PREREG_V1_TO_V2_MAP.md`.
Companion files: `DIRECTION_NOTE_O31_v2.md` (observations O1–O10, design D1), `COMPUTE_PLAN_O31_v3.md` (GPU caps for K4), `OPEN_QUESTIONS_O31.md`.
**Tier of this document:** IRREVERSIBLE (bar 85, PI-1103ad): the commit reserves a one-look set and binds the claim form (ruling CC-501). The tier-3 look needs its own IRREVERSIBLE panel (>= 85, with Codex).
**Dependencies:** Q4 is ruled (CC-501 ruling 4). Q1 is a PI item due before the first tier-1 student output (G3); §3.4 fixes the branch rule now.

---

## 1. Research question and claim form

**RQ8 (proposal §4):** does fine-tuning on verified propositions reduce hallucination while keeping coverage, with no verifier at inference?

**Registered claim form (set-independent).** On the tier-3 images, against near-complete instance gold, the O31 student (S2) does both of the following, with no verifier at inference:
- it recovers at least half of the object-recall gap between the zero-shot base (S0) and the precision-first VSPS recipe (S1);
- it keeps hallucinated objects per caption non-inferior to S1, within a margin tied to the S0 → S1 reduction.

The proposal's KTVIC numbers (1.57 and 47.1) are **development design goals read on KTVIC test in a dev role**, because that test is spent (FAIR). They are never registered thresholds.

## 2. Systems (proposal §8.2 configurations)

| Code | System | Proposal config | Inference |
|---|---|---|---|
| S0 | Qwen2.5-VL-7B-Instruct zero-shot, the FAIR detailed prompt | (1) | 1 greedy pass |
| S1 | FAIR VSPS recipe **retrained** on the O31 training pool with the FAIR verifier's recorded verdicts (Vintern-1B, K = 5 dual queries, unanimity), B = 9, the template renderer only (no constrained-LM rows, unlike FAIR's shipped store), same step count as S2 | (2) | 1 greedy pass |
| S2 | D1: retention-first verifier → coverage-scaled rebuild → same SFT recipe and step count | (3) | 1 greedy pass |
| S3 | S0 plus the O31 verifier applied at inference (stage-1 + selection + render per image) | (5) | pipeline; **dev sets only** (cost, Q6) |
| A-x | ablations, dev only (§8) | – | – |

Configuration (4), repairing REJECTED propositions, is **out of scope**: it is Table 2's FAIR 2028 row. DPO is out of scope too (Table 2, FAIR 2029).

**Training recipe, fixed for S1, S2 and every ablation:**
- FAIR §III-C: 4-bit NF4 QLoRA with double quantisation and bf16 compute; LoRA r = 16, α = 32; learning rate 1e-4; batch 1 with gradient accumulation 8; 512 visual tokens; transformers 4.51.3.
- Optimiser steps: **N_steps = the number of optimiser steps of two epochs over S1's store**. Every arm runs exactly N_steps; a larger store sees fewer epochs. This is proposal §8.2 "cùng số bước huấn luyện".
- The store size of each arm is reported.
- Seeds: 42 at dev. For S1 and S2 at tiers 2 and 3: 42, 43, 44. The registered tests use the seed-mean caption-level scores (see §6.3).

## 3. Data (full official splits; existing labels only)

### 3.1 Training pool
- **Pool:** all KTVIC train images (3,769) minus the 2 byte twins of KTVIC test images (train 3589 = test 1335, train 7511 = test 507; LOG OPS-1031e1blaunch). That leaves **3,767**.
- **Why the twins go:** KTVIC test is an evaluation set here, so this is a principled exclusion. It is fixed now and reported beside the full-pool count.
- **Stage-1 records:** 3,698 come from the existing records (tarball pin b312de68). The other 69 images need a new stage-1 run under the same generator settings.
- **Gold:** no gold caption enters any training target (FAIR rule).

### 3.2 Verifier yardsticks (existing human gold only)
- **V-COCO (primary for the verifier):** entity propositions formed from the COCO-80 mentions of S0's captions, using the frozen `data/coco_probe/coco80_vi.json`. Gold = COCO-2014 instance annotations.
  - Retention RT = P(SUPPORTED │ class present).
  - False-accept FA = P(SUPPORTED │ class absent).
  - Detection recall DR = 1 − FA under the non-strict reading, and P(REJECTED │ absent) under the strict reading.
  - Dev: UIT-ViIC test 231 (spent). Tier 3: the tier-3 set.
- **V-EN (English arm, dev only):** M-HalDetect val, already pinned (2cbc7942; CC BY-NC 4.0) and already used by VSPS-J as dev. Retention of Accurate spans and recall of Inaccurate spans, all claim types.
- **V-VI (Vietnamese proposition labels):** none exist today. ViHal (PI-1110i; TRUE / FALSE / CANNOT-TELL per proposition, KTVIC-train images) is planned and HELD. It is used only if the PI un-holds it (Q3), and it would then get its own amendment. **Without it, the 80 % design target is measurable for COCO-80 entity propositions and in English only. The paper says so.**

### 3.3 Development sets (tier 1; spent; dev role)

| Set | n | Gold | Role |
|---|---|---|---|
| KTVIC test | 558 | caption-derived (5 refs, 113-noun CHAIR-vi lexicon) | design goals 1.57 / 47.1; FAIR comparability; dose-response |
| UIT-ViIC test | 231 | COCO instances ∪ Vietnamese refs | instance-gold dev for the student and for V-COCO |
| KTVIC train (in-sample) | 3,767 | train refs (caption-derived) | pre-SFT supervision gate K0 only |

### 3.4 Confirmation sets
- **Tier 2, dev-confirm rehearsal:** the COCO-2014 Karpathy test, 5,000 images. FAIR spent it, so it is in a dev role. FAIR's COCO numbers (R 63.3 → 45.9, halluc 0.45 → 0.17) are its reference point.
  - Before any decode, a W25 id and near-duplicate pass is run against every ledger owner (§3.5).
- **Tier 3, one look (branch rule fixed now; the PI answer is due before the first G3 output):**
  1. If the PI reassigns KV-4,224 (COCO Karpathy val minus MT4's three exclusion groups; committed unspent under 70c898a; PI-1103h) to O31, tier 3 = KV-4,224. Gold: COCO-2014 instances for the 80 classes; Vietnamese mentions mapped by the frozen `coco80_vi.json`.
  2. Else, if the PI approves AMBER generative (all 1,004 images), tier 3 = AMBER-1,004, only after an amendment that fixes its Vietnamese-to-AMBER object mapping and its own W25 pass, both before any G3 output.
  3. Else there is no tier 3: O31 ends at tier 2 and reports development and rehearsal results only.
  No branch is chosen or changed after any G3 output exists.
- **English one-look set for the verifier:** none is registered. Every English verifier number is dev (Q10).

### 3.5 Custody
- **What is never printed or committed:** caption text, from any dataset or from any model. Counts, ids and shas only. The n-gram scan runs at every commit.
- **Tier-3 images:** they reach the GPU host only after the tier-3 ruling.
- **Tier-3 gold:** it stays on the scoring machine named in that ruling.
- **Overlap rule (fixed before any O31 output).** Before G1, an exact-sha pass and the committed W25 near-duplicate rule (CC-153) run on ids and descriptors only, for: (a) the training pool (3,767) against KTVIC test 558, UIT-ViIC test 231, Karpathy test 5,000 and the tier-3 set; (b) UIT-ViIC test 231 against Karpathy test 5,000 and the tier-3 set. A hit in (a) leaves the training pool; a hit in (b) leaves the tier-2 or tier-3 scoring set (an image explored at development never confirms). Tier-3 images enter this pass as W25 descriptors only and are never decoded. Removed ids and counts are reported beside the full-set result (PI-1110n). The rule is not changed after the pass.

## 4. The verifier (Objective 3.1) and the supervision gate

### 4.1 Probes
- **Probe form:** one affirmative Vietnamese yes/no question per proposition, built from the FAIR template Q⁺.
- **Score:** s = p(yes) / (p(yes) + p(no)) at the answer position. The token sets are fixed as in M0 (yes: c/có; no: kh/không) and checked by the smoke rule "median mass ≥ 0.5 over the first 20 probes", which was carried from Paper C.
- **Families:**
  - Vintern-1B-v3_5: the recorded E1b logits are reused, sha `probes.jsonl` per OPS-1031e1bdone;
  - InternVL3-8B: a new pass on 3,767 images;
  - Qwen3-VL-8B: optional third family, only through an amendment.
- **Boundary with the parked VSPS-J record (CC-244r2 Ruling 3; CC-501 ruling 4):** O31 code never imports or runs `e2b_1c.py`, `test_e2b_1c.py` or `e2b_1c_mutants.py`. V-EN comes from the published E2b aggregates (descriptive), or from a fresh M-HalDetect dev pass that never confirms. E2b H1–H4 stay closed.

### 4.2 States
- **SUPPORTED** if max_f s_f ≥ τ_acc.
- **REJECTED** if max_f s_f ≤ τ_rej.
- **UNCERTAIN** otherwise.
- **Rule constraints:** τ_rej < τ_acc. Spatial relations are always UNCERTAIN, because there are no boxes. FAIR's neutralization rule and the relation → entity backoff are unchanged.

### 4.3 Candidate operating points (fixed now)
- **Grid:** τ_acc ∈ {0.50, 0.60, 0.70, 0.80, 0.90} × τ_rej ∈ {0.10, 0.20, 0.30}, with families ∈ {Vintern only, Vintern ∪ InternVL3}. That is 30 points.
- **Disclosure (N6):** this grid was written after the E1b sweep had been seen. That sweep is on the pre-neutralization `supported` stage, not K0's post-neutralization `sft_caption` stage, so K0 itself has not been measured at its own stage. K0 is a design gate, not a claim.

### 4.4 Supervision build
- **Pipeline:** person-noun neutralization (FAIR `person_uncap`), then FAIR's selector and the **template renderer only** (D8 fixes) and FAIR's filters. The constrained-LM path is dropped for every arm (S1 included), so the store is built on CPU exactly as K0 measures it. One change: the detailed budget is B_i = clip(⌈1.5 × n_SUPP_entities(i)⌉, 5, 15) instead of 9. The short mode is unchanged (B = 2).
- **Budget constants:** 1.5, 5 and 15 are fixed now, before any replay output exists. That makes them design choices, not tuned values.

### 4.5 Gate K0 (pre-SFT, CPU, in-sample KTVIC train, caption gold)
- **Computation:** for each grid point, build the full store (§4.4) and compute supervision object recall R_sup and precision P_sup over the 3,767 images with `scripts/recall_funnel.py`, **stage `sft_caption`** (the rendered detailed target), on post-neutralization records.
- **Precision floor:** P_floor = P_sup(S1 store, same build, same replay) − 2.0. For reference only, FAIR's shipped sft.jsonl gave P 42.6 / R 36.6 at this stage.
- **Choosing the operating point:** **OP\*** = the point with the highest R_sup subject to P_sup ≥ P_floor. Ties go to the higher P_sup.
- **Rule:** **K0 PASS iff R_sup(OP\*) ≥ 47.1.** On FAIL, no SFT GPU-hour goes to S2. The R_sup–P_sup curve is reported as an ablation and the line goes back to the PI (D2 or pivot, Q5).
- **Dose-response points:**
  - OP_strict = the FAIR rule (S1's data);
  - OP_mid = the grid point whose R_sup is nearest the midpoint of R_sup(S1) and R_sup(OP\*);
  - OP\*.
- **Status of the gate:** it is a design gate, not a claim. Its numbers are in-sample on caption gold, and they are never a headline.

## 5. Metrics (per `evaluating-image-captions`)

- **Object level (primary):**
  - the four counts per caption of Objective 3.2: mentioned; mentioned and in gold; mentioned and not in gold; in gold and not mentioned;
  - computed from them: **object recall R = 100 × ΣTP / Σ│G│** (a ratio of sums) and **hallucinated objects per caption h = Σ(mentioned ∧ not in gold) / N**;
  - also CHAIR_i, CHAIR_s, object precision and F1;
  - the count-matched object precision (proposal Objective 3.2), defined here: for systems X and Y on image i, k_i = min(m_X,i, m_Y,i), where m is the number of distinct COCO-80 classes mentioned; each system keeps its first k_i distinct classes in order of first mention; CMP_X = 100 × Σ_i TP_X,i(k_i) / Σ_i k_i. Images with k_i = 0 are left out of both sums and counted. It is an instrument only; O31 makes no claim about the measure itself and reports no raw-versus-matched contrast as a finding.
- **Reference-based:**
  - BLEU-4, METEOR, ROUGE-L and CIDEr-D;
  - Vietnamese: NFC, then the VnCoreNLP RDRSegmenter (pins of OPS-1102b-r7-pin). The scorer's segmenter string is reported, and a `!whitespace-fallback` name counts as a FAULT. The syllable table goes to the appendix;
  - English: PTB tokeniser;
  - SPICE in English only.
- **Descriptive:** words per caption, objects per caption, and the language-check failure share (CJK or other characters outside Vietnamese Latin script).
- **Verifier:** RT, FA, DR (strict and non-strict) and AUROC of max_f s_f, per proposition type where the gold allows it.
- **POPE:** not registered. It runs only if a later amendment names an unspent, overlap-checked POPE split.
- **KTVIC and COCO are never pooled.** Their class universes and gold sources differ (FAIR §IV-B5).

## 6. Hypotheses and registered thresholds (tier 3 unless stated)

### 6.1 Primary family (intersection–union: both must PASS; no multiplicity correction)
- **H1, recall recovery:**
  - ρ = (R_S2 − R_S1) / (R_S0 − R_S1).
  - PASS iff ρ (point) ≥ 0.50 **and** the 95 % CI lower bound of (R_S2 − R_S1) > 0.
  - If R_S0 − R_S1 < 2.0 points, H1 is NOT_IDENTIFIED (the gap is too small to recover).
- **H2, hallucination non-inferiority:**
  - Per replicate, D = (h_S2 − h_S1) − 0.25 × (h_S0 − h_S1).
  - PASS iff the 95 % CI upper bound of D < 0.
  - The margin is a quarter of S1's own gain over S0, on the same images. This is how "ở mức tương đương [8]" is made set-independent.
- **Risk note:** H2 is expected to be the binding hypothesis. On COCO-style instance gold its margin is about 0.07 hallucinated objects per caption (0.25 × (0.45 − 0.17), FAIR values), while the D1 expectation is h about 0.17–0.25. The margin is not loosened for this reason.
- **Headline:** H1 ∧ H2 PASS → "recovers at least half of the recall lost by precision-first verified SFT at non-inferior hallucination, without a verifier at inference".

### 6.2 Secondary family (Holm within the family, α = 0.05)
- **H3, matched count:** Δ = CMP_S2 - CMP_S1 (X = S2, Y = S1, §5). PASS iff the Holm-adjusted one-sided p for the null Δ <= -2.0 is < 0.05 (§6.3).
- **H4, verifier retention (V-COCO on tier 3):** RT(V_O31 at OP\*) − RT(V_FAIR) ≥ +10.0 points with CI lower bound > 0, **and** the CI upper bound of FA(V_O31) − FA(V_FAIR) ≤ +5.0 points.
- **H5, English arm:** the same adapters decoded with a fixed English detailed prompt on the tier-3 images, scored with English CHAIR under the CHAIR synonym map.
  - H5a: CI lower bound of R_S2 − R_S1 > 0.
  - H5b: the same D rule as H2.
- **Design target T-a (80 % retention):** reported as "reached" iff RT(V_O31) point ≥ 80.0 and FA(V_O31) ≤ FA(V_FAIR) + 5.0, on V-COCO tier 3 and on V-EN dev. It is descriptive and never a PASS/FAIL headline.

### 6.3 Statistics
- **Bootstrap:** paired over images, B = 10,000, seed 20261127, with percentile 95 % CIs.
- **Secondary family (Holm, α = 0.05, four members: H3, H4, H5a, H5b).** For each condition, the one-sided bootstrap p-value is p = (1 + #{b : Δ*_b on the null side}) / (1 + B), taken from the same paired replicates as the CIs (B = 10,000, seed 20261127). Null sides: H3 Δ <= -2.0; H4a Δ_RT <= 0; H4b Δ_FA >= +5.0; H5a Δ_R <= 0; H5b D_en >= 0. H4 is one member: p_H4 = max(p_H4a, p_H4b), and its point condition Δ_RT >= +10.0 must also hold. A member PASSes iff its Holm-adjusted p < 0.05 (and, for H4, the point condition holds). Unadjusted 95 % CIs are reported beside every member.
- **Seeds:** with 3 seeds, each image's caption-level counts are averaged over seeds before resampling. Per-seed values are reported.
- **Ratios:** ratio-of-sums metrics are recomputed inside each replicate. A replicate with a zero denominator is counted as undefined and reported, never dropped silently.
- **Labels:** labels are fixed: PASS, FAIL, UNDERPOWERED, NOT_IDENTIFIED. "Not detected" never means "no effect".

### 6.4 Development goals (tier 1, KTVIC test, dev role; never registered)
- **Goals:** h_S2 ≤ 1.57 + 0.25 × (4.26 − 1.57) ≈ 2.24, aiming at about 1.57; R_S2 ≥ 47.1.
- **Reading:** both are read and reported as dev results labelled "FAIR-continuation, development".
- **S3 (verifier at inference):** reported here, and on UIT-ViIC 231, as descriptive rows.

## 7. Three-tier path
1. **Tier 1, dev-explore:**
   - K0 on CPU;
   - S1, S2 and the dose-response students (seed 42) on KTVIC test 558 and UIT-ViIC 231;
   - V-COCO on UIT-ViIC 231;
   - V-EN on M-HalDetect val;
   - the D2 arm, only if run (dev, not registered).
2. **Tier 2, dev-confirm rehearsal** on Karpathy test 5,000 with S0, S1 (3 seeds) and S2 (3 seeds), frozen after tier 1:
   - **P(PASS)** = the share of B_out = 1,000 outer replicates (n = 4,224, drawn from the 5,000 **with replacement**; seed 20261128) in which H1 ∧ H2 both PASS with B_in = 1,000 inner CIs. **It must be ≥ 0.98.**
   - **Why with replacement (N4; CC-501 recommended without):** each outer replicate stands for a fresh tier-3 set of 4,224 images from the same population. Without replacement, every draw shares about 84 % of its images (4,224 / 5,000) with every other draw, so the outer replicates barely vary. P(PASS) would then sit near 0 or 1 and overstate certainty, which makes the 0.98 gate more lenient than intended. Drawing with replacement keeps the between-set sampling variance, which is the quantity the rehearsal must predict.
   - H3–H5 are rehearsed and reported, but they do not gate.
   - If the rehearsal fails, **tier 3 is never touched**, and the result is reported briefly as a dev result.
3. **Tier 3, one look:** after a frozen-config commit and an IRREVERSIBLE panel. Any read of a tier-3 output counts as the look, including a crashed one.

## 8. Ablations (dev only, tier 1; reported beside the registered rows, never a verdict)

| Code | Change against S2 |
|---|---|
| A-1 | dose-response: OP_strict, OP_mid, OP\*. Slope of student R on R_sup and of student h on supervision h (prediction: R slope in [0.7, 1.3], h slope < 1; descriptive) |
| A-2 | Vintern only (no InternVL3) |
| A-3 | B = 9 fixed instead of scaled |
| A-4 | no relation → entity backoff |
| A-5 | S3, verifier at inference |
| A-6 | D2 (learn / mask / unlearn on own captions), only if Q5 allows and budget remains; its λ is fixed before its first output |

## 9. Stop rules

| Code | Trigger | Action |
|---|---|---|
| K0 | §4.5 gate FAIL | no SFT for S2; curve reported as an ablation; PI (Q5) |
| K1 | Seed-42 dev: ρ < 0.30 on both KTVIC test and UIT-ViIC 231, **or** D's point estimate > 0 on both | stop after seed 42; brief dev report |
| K2 | Tier-2 P(PASS) < 0.98 | no tier 3 |
| K3 | Language-check failures > 2.0 % of any student's captions on any dev set | that arm stops |
| K4 | A GPU job exceeds its cap in COMPUTE_PLAN | STOP marker; no resume without a ruling |
| K5 | Novelty doubt ≥ 80 % at any judge read | pivot route |
| K6 | Any text hides a FAIL, K0's curve, or calls a dev result confirmed | BLOCKING at that text's read |

## 10. Models and licences (status "not yet checked"; every row is checked at pin time, N8)

| Model | Role | Licence (as remembered, to verify) | Pin |
|---|---|---|---|
| Qwen2.5-VL-7B-Instruct | generator G, renderer, student | Apache-2.0 | revision + per-file sha at pin; licence checked at pin time |
| Vintern-1B-v3_5 | verifier family 1 (FAIR) | MIT | the FAIR pin; licence checked at pin time |
| InternVL3-8B | verifier family 2 | MIT (LLM part Qwen2.5, Apache-2.0) | the E2b hub snapshot pin; licence checked at pin time |
| Qwen3-VL-8B-Instruct | optional family 3 (amendment only) | Apache-2.0 | – ; licence checked at pin time |

**Data licences:**

| Data | Licence |
|---|---|
| KTVIC | research release; terms checked at pin time (not yet checked) |
| COCO annotations | CC BY 4.0; checked at pin time |
| COCO images | Flickr terms, not redistributed |
| UIT-ViIC | research use (PI-1026bc); checked at pin time |
| M-HalDetect | CC BY-NC 4.0; checked at pin time |

## 11. Deviations from the proposal (named)
1. The RQ8 headline is set-independent (H1, H2), and the KTVIC 1.57 / 47.1 targets are dev goals, because KTVIC test is spent.
2. "Proposition recall on human labels" is measured on existing gold: COCO-80 entity propositions and English M-HalDetect. Vietnamese all-type proposition labels need ViHal (Q3).
3. Configuration (4) moves to FAIR 2028 and DPO to FAIR 2029 (Table 2), not here.
4. The verifier changes from FAIR's K = 5 dual-query unanimity to single-probe cross-family scores (O4, O7). The proposal names BLIP-2 as an example verifier. That remains possible as a family through an amendment.
5. H1 and H2 are read on raw counts, not at a matched number of mentioned objects (§8.2); H3 is the matched-count check (N1a).
6. Configuration (5), S3, runs on dev sets only, for time (about 280 GPU-h at tiers 2 and 3), not because of the 24 GB rule (N1b; CC-501 Q6).
7. The FAIR 2027 headline is the student (H1 ∧ H2) plus the verifier (H4, T-a); Table 2's FAIR 2027 row names the verifier only (N1c; PI-Q-T2, default YES).
8. The exclusion of the 2 byte twins is a new pre-fixed rule for this study; E1b kept them under PI-1031l, which concerned custody (N1d; CC-501 Q8).

## 12. What the author saw before writing this
- FAIR v10 PDF;
- E1b result json (keys `recorded_v1`, `replay_v1_k5`, `logit_base`, `chosen`, `sweep`);
- the LOG lines for M0, E1a, E1b and E2b scores;
- MT4 draft §5;
- Paper C supplement Table S12 rows (Paper C TEST rows that no rule registered; motivation only, no O31 choice uses them; N7);
- the O2 amendment §0–§4;
- the ViHal plan header;
- `.session_backup/2026-11-02/e2b_rate/rate.json` (probe speeds; N11);
- `.paper_work/KE_HOACH_Q2.md` §0 and the stage list of `scripts/recall_funnel.py`;
- the proposal v18.65.

No test file, no tier-3 file and no caption text was opened. KTVIC-train supervision numbers beyond the E1b keys have not been computed.

## 13. PI answers (placeholders; filled from the PI's own words only)
- **PI-Q-H2 (freezes at commit):** keep H2's margin at 0.25 × (h_S0 − h_S1) on raw counts? Recommendation KEEP (CC-501). Default if no answer: KEEP. PI answer: none by the commit. The coordinator applied the default KEEP (LOG PI-1127h, 2026-11-27T09:00:34Z; delegation rule PI-1109d / PI-1115k). The margin is frozen at this commit.
- **Q1 (tier-3 set; due before the first G3 output, branch rule §3.4):** reassign KV-4,224 to O31? Recommendation YES (CC-501). Default if no answer: no tier 3 (branch 3). PI answer: `[PENDING — recorded by the lead]`.
