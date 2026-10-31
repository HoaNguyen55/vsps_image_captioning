# VSPS-J E1+E2 PREREG: fresh logit records (E1b KTVIC train, E1a UIT-ViIC test) and a type-routed single-probe verifier (E2), dev-explore

**Amended by `AMENDMENT_1.md` (CC-209 W1/W2, path ii): E1b on one rented 4090, E1a on M1 with its own smoke, one OUT
folder per host, exact accelerate / qwen-vl-utils pins, staged scoring. Where they differ, AMENDMENT_1 governs.**

Status: DRAFT for a one-judge read (tier REVERSIBLE, dev-explore, bar >= 90), 2026-10-31. Not committed.
Licence for drafting: CC-207 rulings 3-4 (each later VSPS-J prereg goes to a one-judge read). Nothing here licenses a
GPU rental or any test-set use. The rental needs this read's GO, a gatekeeper commit and PI block funding (PI-1031i:
year 1 = method research; renting is free once a judge GO exists).
Label on every output: `TIER 1 / DEV-EXPLORE (VSPS-J E1+E2)`. Every estimate is AI opinion. Every number marked
[measured] was computed on the laptop on 2026-10-31 with the command beside it or by `e1e2.py plan` (`e1e2_plan.json`).

Code: `scripts/vsps_j_e1e2/` = `e1e2.py` (plan, e1b, e1a, detect, score), `ret.py` (CC-207 W9), `test_e1e2.py` (CPU
selftest, no weights), `e1e2_job.sh` (GPU block); SUMS in that folder. It imports `scripts/vsps_j_m0/m0.py` (commit
dba7685, unchanged) for the pinned probe and every guard. Plan file here: `e1e2_plan.json`. The E1a fetch list
is built on the host from the pinned UIT-ViIC `test_data.json` (`e1e2.py fetchlist`, sha in the plan) and is not
committed.

## 1. What M0 changed (result anchored in f77eea1, `M0_RESULT.sha256` 0779d20d)

| M0 outcome (selection set, 663 images) | consequence here |
|---|---|
| 2-shot dR -28.6 [-34.3, -21.5] -> few-shot **DROP** | no 2-shot arm anywhere: program E1 (iv) and E2 "2-shot probes" are removed |
| zero-shot AUROC 0.844 [0.833, 0.854] -> detector **CONTINUE** | the zero-shot single yes/no-logit probe is the E2 base; the cross-family pivot is not triggered |
| arm-A recall by type: count 75.3, attribute 66.0, relation 66.6, object 70.7 | the per-type spread motivates type-routed operating points |

M0 probed English spans; E1/E2 probe the Vietnamese stage-1 questions. M0 is therefore motivation, not a prior on any
number below.

## 2. Construct

**Probe (all of E1).** `m0.probe(ad, pv, q)` with no demos: the pinned Vintern-1B-v3_5 (revision b98f263e, 4 file
shas, `max_tiles` 4), the `yes_no_logit` prompt `<image>\n<q>? Chỉ trả lời 'có' hoặc 'không'.`, one greedy step,
P(yes) = yes-mass / (yes + no mass), raw mass logged. The selftest checks that this is byte-for-byte the prompt the K=5
path (`VLM.probe_yes_no`) asks. Same probe, same pins, same token rule as M0 (its GPU smoke passed: mass 0.998, text
100 %, equivalence 0.0).

**E1b, verifier-only logit pass on KTVIC train.** Every unique Vintern question of each of the 3,700 stage-1 records
(`data/stage1_records/stage1_records.tar.gz`, b312de68, read in place) is asked once on its image. Key = the replay key
(`ReplayVLM._key`), first occurrence per image. **345,768 probes** [measured]. The Qwen colour cross-check answers (K=5,
21,252 probes) are not re-asked; they replay from the records.

**E1a, stage-1 v1 unchanged on UIT-ViIC test.** `scripts/generate_stage1.py` `main()` runs byte-identical: generator
`qwen2.5-vl-7b`, verifier `vintern-1b`, K=5 (auto), max-entities 8, max-pairs 8, verifier tiles 4, colour
cross-check on. Pins and settings:
- Qwen2.5-VL-7B-Instruct at `cc594898137f460bfe9f0759e9844b3ce807cfb5`, every file checked against the B-N1 registry
  (`manuscript/prereg/2026-10-19_b_n1_vi_leaderboard.json`, 9ff02dc2; LFS by sha256, others by git blob sha1).
- `QWEN_MAX_PIXELS` unset, so the adapter default 1280·28·28. flash-attn is not installed, so attention is sdpa.
- Disclosed: the revision and attention kernel of the FAIR stage-1 run were not recorded. E1a records are compared only
  with each other, never with the 3,700.

The only addition is a side-log. A wrapper around `VinternAdapter.probe_yes_no` returns the K=5 answer unchanged, then
asks the same question once with the probe above on the same image tiles and appends one row (image, key, P(yes), mass,
token, seconds). Retries with the stricter prefix are logged under their own key. Records and side-log stay outside the
repo (they carry UIT-ViIC captions as `reference_captions`).

**E1a detectors (laptop CPU, after the pull, 0 GPU-h).** The H1 `Detectors` class unchanged, H1 config and map pins
(`scripts/vsps_h1/SHA256SUMS`), prompts from `vi_en_map.json`. The map was built on KTVIC vocabulary, so UIT-ViIC sports
nouns may be unmapped; they get the vote UNCERTAIN. The share of E1a entities with a mapped prompt is reported.

**E2 verifier (CPU replay, `e1e2.replay`).** `verify()` (HEAD; the H1 additions are default-off) is replayed per record
with `LogitVLM`:
- every Vintern probe answers from the logit table: AFFIRMS iff P(yes) >= 0.5, confidence = max(p, 1-p) (raw, not the
  3-level `vintern.calibrated()`), one sample, text `Có.` / `Không.`;
- so V = 0.5 + 0.5·p on a yes (0.75-1.0) and 0.5 - 0.5·(1-p) = p/2 on a no (0-0.25). V jumps from 0.25 to 0.75 at
  p = 0.5. **Range limit:** S = (0.6 V + 0.2 M + 0.2 G) over the live channels, so a claim with P(yes) < 0.5 has
  S <= 0.55 and can become SUPPORTED only at S_hi <= 0.55 with M and G both live and high; with V alone, grid values
  below 0.75 add nothing. The knob mainly tightens above p = 0.5. This bounds the recall lever;
- a missing question answers INCONCLUSIVE and counts as a miss; any miss in E2 is a FAULT;
- the Qwen colour answers replay from the record (`ReplayVLM`, model filter).

The only knob is `VerificationConfig.per_type_thresholds[type].S_hi` for the six stage-1 types (entity, counting,
attribute, action, relation, spatial_relation). All other thresholds, weights, ceilings, hard constraints and the
acquiescence invariant stay at v1. The image passed to replay is None in every condition, so the comparisons are like
for like. Live vs replay on recorded K=5 answers agrees on 97.9 % of propositions [measured, 100 records,
`ReplayVLM` + `VerificationConfig()`]; H1 measured 98.32 %.

Routing uses the stage-1 `type` field, not M0's English keyword rule. Detector fusion (`e2_chosen_det`) uses the H1
`detector_vote` rule unchanged, with zero free parameters:
- **H1 votes only, no boxes:** the H1 STOP showed that boxes cost recall;
- **`absent_bbox_is_evidence` stays at v1 (True) in every E2 condition**, so the detector arm differs from `e2_chosen`
  only by the vote. The program's "E2 keeps False" was about attached boxes; E2 attaches none, so the flag has nothing to
  act on except through the vote, and holding it constant removes that confound;
- **entity existence only.** Counts are not fused (Paper A owns counts, CC-207 W10).

## 3. Data and custody

| set | role | size | custody [measured] |
|---|---|---|---|
| KTVIC train stage-1 records | E1b probes; E2 selection (T-KT, **in-sample dev**, CC-207 W6) | 3,700 images, 192,216 propositions | all train-only KTVIC (train_data 72ee9b57, test_data cc22ec6a); image bytes must not match exclusion.json `ktvic_test` (FAULT) |
| KTVIC train without records | not probed | 69 images | excluded by construction: FAIR's pipeline-screening set (`data/screening/val_manifest.json`, n 69, "all 69 train images outside stage-1"); they have no stage-1 records, so not a survivorship gap |
| UIT-ViIC test | E1a stage-1 + logits; T-COCO read | 231 images (full split) | spent (exclusion.json `uitviic_test`, c52a96d1), dev role only; 231/231 fetched bytes equal exclusion.json's `uitviic_test` sha list (laptop fetch to scratch today; `e1a` refuses otherwise); overlap 0 with A-T3 3,232, KV-4,224, UT-2,532, Karpathy test, M-HalDetect dev-touched 3,454; 231/231 in `instances_train2014.json` (777ef504) |

- **Gold, all existing human labels:**
  - T-KT uses the KTVIC train references (caption-derived, so in-sample dev only);
  - T-COCO uses COCO instance annotations.
- No new labels. No AI label is used as evidence: detector votes are a method component, never gold.
- **Domain limit (CC-207 W7):** UIT-ViIC test is sports-only. The top instance classes are person 1,233, sports ball
  373, chair 270, tennis racket 223 and bench 87.
- **No test set is touched.**
- **Ledger:** UIT-ViIC test is already spent, so no new owner is displaced. One ledger line, exact text and placement
  in `JUDGE_READ_REQUEST.md` (gatekeeper commit set).

## 4. Outcomes, rules and stop rules (scored once, `e1e2.py score`)

### 4.1 E1b fidelity (gate before any E2 selection)
- **Coverage:** every unique recorded Vintern question of every record has a logit row. Otherwise the score is
  REFUSED (INCOMPLETE).
- **Agreement with K=5 (gate T0.5 G2 bar):** kappa(P(yes) >= 0.5, recorded K=5 majority) >= **0.70**. If it is below,
  E2-KT = STOP: the logits are not a faithful verifier signal, and E2 is not selected.
  - Anchor: `data/results/gate_t05.json`, 600 probes, 3090, 6 tiles, 4 tokens: agreement 90.7 %, kappa 0.794. By K=5
    margin: 97.8 % (5/5), 84.3 % (4/5), 51.5 % (3/5).
  - This replaces the program's "< 97 % of propositions agree" rule. That rule compared a replay of identical answers
    (98.32 %) with a change of answer source that gate T0.5 already measured at 90.7 % per probe, so it would stop a
    working run by construction.
- **Descriptive:** overall agreement and agreement by K=5 margin.

### 4.2 E2 selection on KTVIC train (T-KT, in-sample dev; never registered, never tier 2/3, never a headline)
- **Metrics** (`kt_metrics`, equal to `recall_funnel.py` supported stage and `ret.py`; checked in the selftest):
  - supported-stage P and R;
  - retention = P(SUPPORTED | object in refs);
  - mirror rate (reported, never a claim).
- **Baselines [measured on recorded verdicts]:** retention 52.9 (4,474/8,453), mirror 69.6, supported R 36.5, P 41.1.
  Command: `python3 -I scripts/vsps_j_e1e2/ret.py <records>`. The score also reports `replay_v1_k5` (recorded
  answers, image None) and `logit_base` (all S_hi 0.70).
- **Rule, fixed now:**
  - start from S_hi = 0.70 (v1) for every type;
  - two passes over the types in the order entity, counting, attribute, action, relation, spatial_relation;
  - for each type, S_hi is tried on the grid {0.50, 0.55, ..., 0.95}, with every other type at its current value
    (2 × 6 × 10 = 120 replays);
  - keep the value with the highest retention subject to supported-stage **P >= 39.2** (the H1 floor, P0 - 2.0);
  - ties go to the larger S_hi; if no value is feasible, the type keeps its current value.
  - Two passes, not one: a CPU dry run on synthetic P(yes) (the yes-share of the recorded K=5 samples, no model output,
    deleted) put the all-0.70 base below the P floor, so a single pass depended on the type order.
  - The full trace is reported.
- **Stop (program E2):** if retention < **65.0** or P < 39.2 at the chosen vector, E2 = STOP. The curve is then reported
  as an ablation, and T-COCO reads only the baselines.
- **Disclosure (CC-207 W6, H1 section 5 literal reading):** non-detector verifier settings are selected on the 3,700 H1
  records. Detector fusion is never selected or read on them.

### 4.3 T-COCO read on E1a (at the chosen vector only; CC-207 ruling 4, W7)
- **Unit:** an entity proposition whose `text_vi` names exactly one COCO-80 class under the FAIR matcher
  (`score_coco_probe.vi_objects`, lexicon v2, `coco80_vi.json` 926e0857). Propositions naming more than one class are
  left out.
- **Absent / present:** the class is absent from, or present in, the image's COCO instances.
- **Metrics:**
  - DR = P(not SUPPORTED | absent);
  - DR_strict = P(REJECTED | absent);
  - RT = P(SUPPORTED | present);
  - absent and present counts.
- **Conditions:**
  - `recorded_v1` (live K=5);
  - `replay_v1_k5`, the **baseline**;
  - `logit_base`;
  - `e2_chosen`;
  - `e2_chosen_det` (descriptive).
- **CI:** an image-clustered percentile bootstrap, B 2,000, seed 20261031. It gives 95 % CIs for each condition's DR
  and RT, and for the paired difference from the baseline (same resampled images).
- **Stop (program l.257):** if DR(`e2_chosen`) < DR(baseline) - **5.0**, E2 = STOP. This is decisive only if
  n_absent >= **200**; with fewer it is reported and descriptive (W7).
- **E1a kappa:** reported, descriptive (E1b's kappa is the gate; same model and prompt).
- **Labels:**
  - the 80 % values (T-COCO DR and RT) are design goals (PI-1031g), never thresholds;
  - T-COCO is confirmed only at tier 2 (full Karpathy test, spent), never here (W8);
  - there is no captioner and no CHAIR in this block.

## 5. Cost (4090 wall-clock GPU-h; measured anchors)

| sub-job | work | anchor | estimate | cap |
|---|---|---|---|---|
| E1b | 345,768 probes on 3,700 images (median 94 per image) | M0 arm A on a 4090, same probe: median 0.032 s, mean 0.040 s per probe (`probes.jsonl`, 16,027 rows) | **3.1 h** (median) to **3.8 h** (mean), + load and smoke about 0.05 h | **5.0** |
| E1a | 231 images, full stage-1 + side-log | stage-1 records: 85.7 s mean / 79.7 s median per image on a 3090 (`stats.seconds`, 3,700 records; 88.1 GPU-h in total); side-log 94 × 0.032-0.040 s per image | **5.3-5.7 h** (the 4090 is not assumed faster for Qwen generation; no measurement) | **7.5** |
| E1a detectors | 231 images, laptop CPU | H1 CPU run: 27.1 s per image (1,069 lines) | about 1.7 h CPU, **0 GPU-h** | none |
| E2 score | 123 replays × 3,700 records + T-COCO | dry run: 63 replays in 27 min on the laptop [measured, synthetic P(yes)] | about 1 h CPU, **0 GPU-h** | none |

- **Block:** about **8.4-9.6 GPU-h** of probing, plus about 1 h of setup:
  - venv;
  - Vintern about 2 GB;
  - Qwen about 16.6 GB;
  - scp of the 3,700 KTVIC images, about 0.53 GB;
  - 231 COCO images.
- **Rental:** about 9.5-10.6 h, at the m6 rate of 15.2k VND/h (11,818 VND for 46.7 min) up to 17.5k VND/h, so about
  **145-185k VND**.
- **Worst case at both caps:** 12.5 + 1 h, about 235k VND.
- **This replaces the program's E1 figures:**
  - E1a: the program says 1.5 h (its anchor was the multi-stream 24.2 h wall over a fleet, not one GPU);
  - E1b: the program says 12 h (it assumed half of stage-1; the logit pass needs one 1-token step per unique question).

**Projection and cap rules (M0 binding form, CC-206):**
- **E1b pre-pass:** after the smoke, if elapsed + 345,768 × smoke median s/probe > 5.0, PROJECTION_STOP before any
  image of the pass.
- **E1b at image 200** (fixed seeded order, `order_sha256` e2a3bcaa): if elapsed + remaining probes × median s/probe
  over images 2-200 > 5.0, PROJECTION_STOP.
- **E1a at image 20** (the file order of `test_data.json`, `order_sha256` b3dee1a8): if elapsed + remaining images ×
  median s/image over images 2-20 > 7.5, PROJECTION_STOP.
  - This replaces the program's "50 images > 3 h", which would fire on the expected cost.
- **Hard caps:** checked before each image is decoded (E1b in the loop; E1a when the image is opened). A cap hit is
  CAP_STOP.
- **Never:** a subset, another model, or a cap raise without a new ruling.

## 6. Smoke and FAULT rules
- **E1b smoke** (the first 20 images of the seeded order, 5 questions each, 100 probes; M0 section 7.1 rules, arm A
  only):
  - tokens resolve;
  - P(yes) finite;
  - median mass >= 0.5;
  - >= 90 % có/không first tokens;
  - equivalence with `VinternAdapter.yes_no_logit` on 5 probes, |dP| <= 1e-3.

  Any failure is a FAULT, and nothing more is decoded in E1b.
- **E1a** refuses to start unless the E1b smoke passed (same model, same block).
  - FAULT if the first E1a image produces no record (load or pipeline error), or if any logged P(yes) is non-finite.
  - Images that fail later (exception caught by `main()`) leave exit 5 with no marker; the same command may resume
    once (OPS line). Images still failing after that one resume are listed in the result and contribute 0 T-COCO
    units; the score proceeds if at most 11 (5 %) fail, else INCOMPLETE. The 3,700 had no failures (3,700 + the 69
    screening images = 3,769), so this is not expected.
  - A STOP or INCOMPLETE in one sub-job is recorded in the result and never blocks scoring the other (`isolated`).
- **Stop markers:** each sub-job folder (`OUT/e1b`, `OUT/e1a`) has its own STOP marker, written on every FAULT,
  PROJECTION_STOP and CAP_STOP (`m0.halt`).
  - A stopped sub-job is never resumed or scored (`m0.refuse_if_stopped`, `m0.check_scorable`). A crash with no marker
    may resume.
  - An E1a stop does not block E1b's score, and the reverse holds too, except the smoke dependency above.

## 7. Run, return, scoring
- **Slot:** dates are non-binding (CC-207 r8 / W11). The block uses its own rented 4090; M1 is not used. The host is
  deleted after the pull (PI-1031c).
- **Staging on the host:**
  - the repo at the gatekeeper commit;
  - `data/datasets/uitviic/test_data.json`, which is untracked and sha-checked by `e1a`;
  - the 3,700 KTVIC train images by scp.

  No host, IP or port is written in the repo.
- **Environment:** the M0 pins (torch 2.15.0, torchvision 0.29.2, transformers 4.51.3, numpy 2.5.4, pillow 13.0.0, timm
  1.0.30, einops 0.8.2), plus `accelerate` and `qwen_vl_utils` for the generator. Their versions are recorded in
  `pip_freeze.txt`, not pinned (judge question 5).
- **Commands:**
  - `PY=<venv>/bin/python bash scripts/vsps_j_e1e2/e1e2_job.sh --selftest`;
  - then `PY=... KT_IMAGES=... UIT_IMAGES=... STAGE=... OUT=<the ONE OUT folder> bash scripts/vsps_j_e1e2/e1e2_job.sh`.
  - The job checks four SUMS (e1e2, m0, vsps_h1, this folder) and the environment, runs the selftest, fetches both pinned
    snapshots, writes `refs/main`, builds the fetch list, fetches and hashes the 231 images, stages UIT-ViIC as `NCS_DATA`, then runs E1b and
    then E1a and writes each `probes.jsonl.sha256`.
- **One OUT folder (CC-208a G2).** The launch OPS line records it. A second OUT folder, or a relaunch after a STOP, is a
  protocol breach.
- **Return:**
  - sha256 manifest of every OUT file on the host; scp; re-check on the laptop;
  - delete the host;
  - OPS lines at launch, at each projection, at each stop or done, and at the pull.
- **Laptop, after the pull:**
  - `PY_H1 -I e1e2.py detect` (H1 env, CPU);
  - then `<m0 venv> -I e1e2.py score --out <OUT> --res <OUT>/e1e2_result.json`, **once**.
  - The result json holds numbers only and enters the repo through the gatekeeper with its sha.

## 8. What this can and cannot claim
- **Can (dev-explore):**
  - whether one zero-shot logit probe can replace K=5 self-consistency in VSPS verification (kappa, T-KT curve);
  - which per-type S_hi vector the fixed rule picks;
  - the T-COCO detection recall and retention of v1, the logit base and that vector on 231 sports images.
- **Cannot:**
  - any test or tier-3 claim;
  - any T-KT number as a result (in-sample);
  - any >= 80 % claim;
  - any captioner, CHAIR or supervision-quality claim (that is E3);
  - any cross-family claim (deferred, section 9).

## 9. Program items deferred or changed (each a judge question)
- **Cross-family self-consistency on attribute and relation (program E2):** deferred to an E2b amendment.
  - M0 did not trigger the pivot (AUROC 0.844).
  - No yes/no-logit path exists in the repo for a second family: C-T3 decodes captions only.
  - The default candidate for E2b is Aya-Vision-8B (Command R7B LM, Vietnamese listed; C-T1 pin d7601ac8).
- **UNCERTAIN as the recall knob:** not tuned. S_lo, C and E stay at v1.
- **T-EN routing on M-HalDetect:** not in this prereg. M0 already reports per-type recall; mapping the KTVIC S_hi vector
  onto English spans would need its own rule.

## 10. CC-207 fix map

| Fix | Where closed |
|---|---|
| W6 T-KT in-sample dev, out of every freeze target; non-detector settings on the 3,700 disclosed; detector fusion only on new records (E1a) | sections 2, 4.2, 4.3 |
| W7 E1a absent/present counts, image-clustered CI, < 200 absent = descriptive, sports-only limit | sections 3, 4.3 |
| W9 `ret.py` committed in `scripts/vsps_j_e1e2/`, reproduces 52.9 (4,474/8,453) and 69.6 (n 21,049) [measured] | section 4.2 |
| Ruling 4 (E1a reads; H1 section 5 scope) | sections 4.2-4.3 |
| W8 T-COCO confirmed only at tier 2 | section 4.3 |
| W10 no count fusion | section 2 |
| W11 dates non-binding, VSPS-J queues behind A/B/C gates | section 7 |
| W2 (carried) logit path reused from M0 (`m0.probe`), smoke rules reused | sections 2, 6 |
