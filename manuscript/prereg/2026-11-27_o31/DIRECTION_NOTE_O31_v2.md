# Direction note O31 v1: a high-recall proposition verifier and verified-proposition fine-tuning (Objective 3.1, RQ8)

Stamp: 2026-11-27 (date -u at write time, see the file mtime). Author: o31-plan agent. Status: v2 after CC-501 (CONDITIONAL GO 87): folds in N5 (NEW claim restated, §5–§6), N6 (O4, §4 Main risk) and N7 (O10). v1 = cb501c07. Nothing here was run. No GPU, no rental, no commit.
Mandate: PI-1127g (brief `~/vsps_out/o31/BRIEF.md`); proposal v18.65 Objective 3.1, RQ8, Table 2 rows "FAIR 2027" and "JVCIR (conditional)", §8.2.
Every estimate and expected effect below is AI opinion, not evidence. Every number tagged with a `file::key` was read today from that file.

---

## 1. The problem

The FAIR 2026 system (VSPS, proposal ref. [8]) fine-tunes Qwen2.5-VL-7B with QLoRA on captions rebuilt from propositions that a verifier accepted. On KTVIC it cut hallucinated objects per detailed caption from 4.26 to 1.57, but object recall fell from 57.1 % to 37.1 % (COCO: 63.3 % to 45.9 %). Captions shrank from 117 to 34 words. RQ8 asks whether verified-proposition fine-tuning can keep the hallucination gain while recovering coverage, with no verifier at inference. The proposal sets two design targets:

- (T-a) verifier: keep at least 80 % of true propositions ("proposition recall" = retention, proposal §8.2), with its false-accept rate reported beside it;
- (T-b) captioner: hallucinated objects per caption near 1.57, and object recall ≥ 47.1 % (half of the 57.1 → 37.1 drop recovered).

**Two facts constrain how (T-b) can be tested.**
1. KTVIC test is spent (the FAIR look). So 1.57 and 47.1 can only be **development design goals** read on KTVIC test in a dev role. They can never be registered thresholds. The registered claim must be set-independent (§6 and the prereg).
2. 47.1 sits at the KTVIC human leave-one-out recall (46.9 / P 85.5, `.paper_work/KE_HOACH_Q2.md` §0). KTVIC gold is caption-derived and incomplete. On it, higher recall partly rewards naming more, and a true but unreferenced object counts as "hallucinated". Confirmation therefore belongs on near-complete instance gold (COCO-80 instances), with the comparison made at a matched number of mentioned objects (Objective 3.2).

## 2. Our own observations (idea provenance)

| # | Observation | Source (file::key) | What it implies |
|---|---|---|---|
| O1 | VSPS: halluc/cap 4.26 → 1.57, KT recall 57.1 → 37.1, P 31.6 → 41.9; COCO recall 63.3 → 45.9, halluc 0.45 → 0.17 | `FAIR_28.08.26_v10_EN_IEEE.pdf`::Tab II, III, IV | the baseline and the size of the recall debt |
| O2 | **Recall funnel**, 3,700 KTVIC-train records against train-ref gold, stages of `scripts/recall_funnel.py`, measured **after neutralization**: all_props R 68.9 (P 29.1) → not_rejected 66.0 → supported 48.0 (P 39.8; verifier −18.0) → sft_caption 36.6 (P 42.6) → **student 37.1** (test). Correction 10-10: at B = 9 the selector costs ~1; clean-props ~−4.6 and rendering ~−4.7. The **pre-neutralization** records in the tarball b312de68 (what E1b replays) give all_props 66.0 and supported R 36.9 / P 41.2. The gap is the neutralization step | `.paper_work/KE_HOACH_Q2.md`::§0 table + correction D1; `VSPS_J_PROGRAM_2026-10-31.md`::§1.1–1.2 | **the student's recall copies the supervision's recall**; the verifier is the largest single loss |
| O3 | **MT4 (GESD)**: gold-edited own captions reach target CHAIR_i 1.79 at recall 65.28 (zero-shot 9.38 / 65.65), but the student only reaches 6.65 vs base 9.22 (about one third of the target-level reduction transfers); student recall 67.02 (+4.65). Detector editing loses 13.92 recall points at target level | `manuscript/journal_draft_MT4/05_results.md`::§5.1, §5.3, §5.4 Tab 3 | **editing own captions keeps recall but transfers hallucination reduction poorly**; a weak verifier costs recall |
| O4 | Verifier retention on KTVIC train (caption gold): recorded 5/5-unanimity rule 52.9 (supervision P 41.1, R 36.5); single-probe logit rule 64.5 (P 38.5, R 44.3); best of the 120-point threshold sweep R 44.7 at P 38.2, retention 65.2. **All E1b values are at the pre-neutralization `supported` stage**, not at K0's post-neutralization `sft_caption` stage (N6) | `~/vsps_j_e1e2_runs/score_root/e1b_result.json` (97d2553b)::`e1b_e2_kt.{recorded_v1,logit_base,sweep}`; LOG OPS-1031e1bscore | the answer source (logit vs K = 5 dual queries), not the threshold, moves retention; on the pre-neutralization `supported` stage the threshold knob on Vintern-1B is flat. Whether that carries to K0's stage is **not measured** (N6) |
| O5 | T-COCO on 231 UIT-ViIC test images (COCO-80 entity existence, descriptive, n_absent 48): retention 36.6 (recorded), 42.6 (logit); detection recall 66.7 → 60.4 | LOG OPS-1101e1ascore (e1a_result a01eafc6) | retention of true entity propositions is the weakest number we have |
| O6 | Vintern-1B single probe on M-HalDetect val (EN human labels): Inaccurate-span recall 70.9, P 59.6, AUROC 0.844; 2-shot worse | LOG OPS-1031m0score (m0_result 0779d20d) | a 1B verifier is a usable detector; the problem is retention, not detection |
| O7 | InternVL3-8B (FA) vs Vintern-1B, Vietnamese-form probes on M-HalDetect: Δprecision +7.77, Δretention +15.22, Δdetection-recall −2.79; EN: retention 65.0 vs 47.0, recall 83.4 vs 87.1 | LOG OPS-1102e2b-score (res 9b9c3f6e), OPS-1102e2b-score-en (f1fea816) | **a stronger cross-family verifier moves precision and retention together**, which a threshold cannot |
| O8 | Box detectors as a gate cost recall (H1 R1 −4.4) | `manuscript/directions/VSPS_J_PROGRAM_2026-10-31.md`::§2 E0 | no detector gate |
| O9 | Neutralization was FAIR's biggest recall lever (VSPS-Base → Neutral R 23.3 → 37.7 at P 39.1 → 39.9); hedging UNCERTAIN instead of excluding adds 0.90 objects at +0.45 halluc; spatial relations never SUPPORTED (0 / 26,795); 27.4 % of query groups split | FAIR v10::Tab IV, V, §III-B | coverage comes back through what is done with UNCERTAIN, not only through SUPPORTED |
| O10 | Paper C: a prior-debiased yes-score (p(yes│image) − p(yes│question)) separates neighbour-only classes weakly, AUROC 0.55–0.63 (these are Paper C TEST rows that no rule registered; motivation only, and no O31 choice uses them, N7) | `manuscript/journal_draft_C/11_supplement_registered_rows.md`::Tab S12 | prior-debiasing alone is not the verifier fix; used here as motivation only |

**The design axis.** O2 and O3 point in opposite directions. Rebuilding from verified propositions (VSPS) transfers the hallucination gain fully but caps recall at the verifier's retention. Editing the model's own caption (MT4) keeps recall but transfers only about a third of the hallucination gain. O4 to O7 show where the retention is lost and that only a better verifier, not a looser threshold, moves retention and precision together.

## 3. Relation to earlier lines (boundaries)

- **VSPS-J (parked, commit 551eae2, CC-244r2).** Its registered claim was a *verifier-level* one: E2b H1–H4 for `internvl3_8b|FA` (and `|1c`), closed under O2-(i). O31 does **not** re-open H1–H4 and makes no tier claim from E2b. E2b, E1a, E1b and M0 numbers are cited only as dev motivation (O4–O7). What O31 adds is the part VSPS-J never reached: the verifier is used to build fine-tuning data, a pre-SFT supervision gate is registered, and the claim is about the **student**, confirmed at matched object count. The un-parking needs a judge line (OPEN_QUESTIONS Q4).
- **MT4 / L3-P1 (Gate 1 NO-GO, fallback T2_FAIL).** MT4 edits its own captions using COCO *gold* (or a detector), on UIT-ViIC/COCO images. O31's primary design rebuilds from propositions verified by a ≤ 9B VLM verifier with no gold in the loop, trained on KTVIC. Design D2 (§4) is close to MT4's GESD-det and is kept as a secondary dev arm only. KV-4,224 is still MT4's committed unspent set; using it needs a PI reassignment line (Q1).
- **Paper A.** O31 uses the count-matched comparison of Objective 3.2 as an evaluation instrument only, cited as A's method. No A analysis is repeated (salami check at every read).
- **Paper C.** C's verifier is a neighbour-class filter at inference; O31's verifier is offline and only builds data. No shared claim.
- **Table 2 scope (PI-1127d).** FAIR 2027 = the high-recall verifier + fine-tuning with its data (proposal §8.2 configurations 1, 2, 3, 5). Configuration 4 (repairing REJECTED propositions) is Table 2's FAIR 2028 row and is out. DPO is the FAIR 2029 row (and FAIR 2026's DPO after SFT failed) and is out.

## 4. Candidate designs

### D1 (recommended). Retention-first verifier → coverage-scaled rebuild, gated before SFT, with a dose-response

1. **Verifier (Objective 3.1).**
   - Single affirmative yes/no probe per proposition, read as the normalised p(yes) at the answer position. This drops FAIR's K = 5 dual-query unanimity, which O4 shows is the retention loss.
   - Two families: Vintern-1B (logits already recorded for 3,700 images, O4) and InternVL3-8B (O7). Optional third: Qwen3-VL-8B.
   - Three states from two thresholds on the family scores: SUPPORTED if max-family p ≥ τ_acc; REJECTED only if every family gives p(yes) ≤ τ_rej; UNCERTAIN otherwise. The OR on acceptance is the retention lever. The AND on rejection keeps rejection conservative.
   - Spatial relations: no boxes, so they stay UNCERTAIN (O8, O9). Relation → entity backoff kept (+1.2, memory note).
2. **Supervision.** FAIR's rebuild path (selector, renderer with the D8 fixes, neutralization), with one change: the detailed budget scales with the number of SUPPORTED entities of the image instead of B = 9.
3. **Operating point chosen before SFT, on supervision, by a registered rule.**
   - On KTVIC train (in-sample, caption gold, a dev quantity), build the full store on CPU for each candidate (τ_acc, τ_rej): neutralization, selector, **template renderer only**, filters. S1's store is rebuilt the same way.
   - Read R and P at one stage, `sft_caption`.
   - Pick the point with the highest R subject to P ≥ P(S1 store) − 2.0.
   - **Pre-SFT gate:** if no point reaches R ≥ 47.1, no SFT GPU-hour is spent on D1 (kill K0). By O2, the student's recall cannot exceed the supervision's.
   - **Why template only:** the constrained-LM path needs a GPU and cost ~1.1 recall (D8 note). It is dropped from both S1 and S2, so the gate measures exactly the store that gets trained.
4. **Dose-response.** Three operating points (FAIR-strict, middle, retention-first) give three supervision sets and three students (one seed each, dev). They estimate the supervision → student transfer slopes for recall and for hallucination. This is the mechanism claim and a practitioner's dial.
5. **Student.** Qwen2.5-VL-7B, the FAIR QLoRA recipe, the same number of optimiser steps for every configuration, no verifier at inference.

- **Expected (opinion).** With InternVL3-8B in the OR, supervision recall about 46–52 at supervision P 39–42. Student KT recall about 44–50. Halluc/cap on KTVIC about 1.6–2.1, because more true but unreferenced objects count against caption gold. On COCO instance gold: recall about 52–57 at halluc about 0.17–0.25.
- **Main risk.** The supervision gate may fail with Vintern alone. O4's sweep tops out at R 44.7, but on the pre-neutralization `supported` stage, so it does not measure K0 (post-neutralization `sft_caption`); the expectation is unmeasured (N6). InternVL3 probes (about 23 GPU-h on a 3090) are planned on the critical path regardless.

### D2 (secondary dev arm). Edit-in-place with verdict roles: learn / mask / unlearn

- Target = the base model's own detailed caption.
- Token loss role by verdict:
  - SUPPORTED spans are learned (standard NLL);
  - UNCERTAIN spans are masked out of the loss (neither taught nor penalised);
  - REJECTED spans with high confidence get an unlikelihood term (weight λ).
- It targets MT4's transfer gap (O3) while keeping MT4's recall.
- **Status:** PARTLY TAKEN (EFUF 2402.09801 unlearning, Mask-DPO 2503.02846 masking, SCAPO in 2609.35294 subsentence credit).
- **Deviation:** it adds a loss term beyond proposal §8.2 ("verification signal becomes supervised data"). It is also close to MT4 GESD-det.
- **Use:** a dev arm only if D1 passes K0 and budget allows. It is not registered for FAIR 2027.

### D3 (not now). Count-matched verified preference pairs (DPO)

- Pairs = a verified caption vs a variant with the same number of objects, one of them refuted.
- This would stop preference learning from rewarding "saying less" (Wei et al. [7]).
- Out of scope: Table 2 places DPO at FAIR 2029, and FAIR 2026's DPO after SFT degraded every setting. Listed for completeness.

## 5. What is new, against prior art (detail in PRIOR_ART_O31.tsv)

- **TAKEN (English):** "less hallucination without saying less" as a goal.
  - Beyond Saying Less (2609.35294, on-policy RL with dense presence/absence annotation, DOPA);
  - ClaimDiff-RL (2605.20278, claim-difference rewards);
  - BalCapRL (2605.07394);
  - FeedQuill (2503.07906, unit-level precision and recall preferences);
  - KnowAda (2411.09018, adapt captions to what the model knows).
- **PARTLY TAKEN:**
  - verified or filtered self-captions as training data (HalluciDoctor 2311.13614, SENTINEL 2507.12455 with detector cross-checks, our FAIR 2026);
  - loss-level masking or unlearning (EFUF, Mask-DPO).
- **NEW, as far as 25 searches show; the narrow combination we can defend:**
  (i) the verifier operating point is fixed by a registered pre-SFT gate on supervision coverage, before any SFT; (ii) the supervision → student transfer slopes are measured across operating points under data-level SFT only; (iii) the setting is Vietnamese, no RL, no new labels, one 24 GB GPU, with confirmation on instance gold (CC-501 ruling 1(b)). The single-probe cross-family OR-accept / AND-reject rule is a design detail, not a claim (FeedQuill already ensembles open VLMs).

  None of the works read registers a pre-SFT coverage gate or reports supervision → student transfer slopes across verifier operating points under SFT only. Beyond Saying Less uses RL on the same Qwen2.5-VL-7B base with model-made DOPA labels and human spot checks; ClaimDiff-RL already offers tunable operating points through rewards; FeedQuill already verifies with an open-VLM ensemble (N5).
- **Novelty level, honestly:** method novelty is about 2.5–3 of 5 (CC-501). The mechanism result (transfer slopes) and the low-resource, no-new-label setting carry the paper. That fits FAIR 2027. JVCIR needs the tier-3 PASS plus the English arm.

## 6. Expected application value

- **Assistive description in Vietnamese:** fewer wrong objects than zero-shot while naming about half again as many true objects as VSPS. The PI's stated use (blind and low-vision users) needs both.
- **A practical dial (PARTLY TAKEN, ClaimDiff-RL tunes operating points through RL rewards; ours is a data-level dial):** the operating point → recall/hallucination curve tells a deployer how to set the verifier for a wanted coverage, at zero inference cost.
- **Reusable component:** the verifier is the shared part of Objective 3.1. It feeds the agentic verifier of Model 3 (IVC paper) and FAIR 2028's repair data.

## 7. Kill criteria (fixed now; the prereg repeats them)

| Code | Trigger | Action |
|---|---|---|
| K0 | Pre-SFT gate (stage `sft_caption`, same build as the trained store): no registered operating point gives KTVIC-train supervision recall ≥ 47.1 at P ≥ P(S1 store) − 2.0 | D1 spends no SFT GPU-h; report the curve as an ablation; go to Q5 (D2 or pivot) |
| K1 | Dev students (KTVIC test 558 and UIT-ViIC test 231, both spent, dev role): recall recovery < 0.30 of the zero-shot → VSPS gap on both, **or** halluc/cap above VSPS + δ_h on both | stop after one seed |
| K2 | Tier-2 rehearsal P(PASS) < 0.98 | the tier-3 set is never touched; dev result reported briefly |
| K3 | Language-check failures (CJK or out-of-script) > 2 % of student captions (MT4 G6) | stop that arm |
| K4 | Judges' novelty doubt ≥ 80 % (pivot rule) | pivot |
| K5 | A salami conflict with A, B, C or MT4 | the item leaves O31 |

## 8. Next gate

One-judge FULL read of `PREREG_DRAFT_O31_v1.md` together with this note (reversible, bar 85). A judge or PI line is also needed on the main direction and on the un-parking of the VSPS-J verifier line (Q4). Nothing runs before the prereg commit, not even P0 (the CPU replay of the recorded Vintern logits). The K0 gate governs P0's output, so its rule must be committed before that output exists. Otherwise the gate would be post hoc. Only the code and its self-tests on synthetic data may be written before the commit.
