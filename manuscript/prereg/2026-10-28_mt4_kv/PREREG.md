# MT4 confirmatory PREREG (conditional, two branches): one scoring event on KV-4,224

**Status:** written 2026-10-28, before any Gate 1 output, any confirmatory training and any KV prediction. No K2 adapter, no K1/K6 adapter and no KV decode exist. Built from Ken's `manuscript/ken/K22_MT4_PREREG_DRAFT.md` (draft, not binding) and CC-148 ruling 1, W6, W8 and W13, under CC-151 r1 and PI-1026bb.

**Commit order (CC-151 r1, PI-1026bb Q1).** This PREREG is committed **before ANY K2 Gate 1 GPU step**, teacher decode and training included. The K2 Gate 1 job HOLDs until it is at HEAD (`k2_gate1.PREREG_REL`). Ken's conditions "commit after a Gate 1 GO" and "W26 at NCA" are struck.

**Label.** CONFIRMATORY, one look. Every hypothesis, threshold, test order, seed rule, pooling rule and freeze rule below is fixed before any KV prediction exists.

**Venue.** Information Processing & Management (IP&M), special issue VSI: MMLowRes; fallback Neurocomputing (PI-1026ay; CC-149: SCIE, not on hold). Quartile standard SJR (Scopus). The journal's MJL status is re-checked on the submission day (CC-149 W1). The science below does not depend on the venue.

**Novelty re-search (CC-119 W23, completed; CC-153 W7).** Ken's K14-1 pass (`manuscript/ken/K14_PRIOR_ART_MT4_2026-10-27.md`, rows 1–18: SENTINEL 2507.12455, KnowAda 2411.09018, SEED 2507.04680, OSCAR 2605.00323, LURE, HalluciDoctor and others) plus this folder's `PRIOR_ART_W23.md` (rows 19–20: STIC 2405.19716 and ReCaption 2312.01701, read at abstract and method level by a non-Ken writer). Neither STIC nor ReCaption does gold-only deterministic editing followed by plain SFT; the 80% pivot rule is not triggered. **Narrowed gap claim (setting novelty, not method novelty):** we know of no prior work that removes clauses from a backbone's own detailed captions by a deterministic rule against human COCO instance gold, trains the same backbone on them by plain SFT, and shows fewer hallucinations than its zero-shot output at matched coverage, with an unedited self-training control, in Vietnamese. The method follows the verified-proposition supervision of Nguyen et al. (FAIR 2026), cited as prior work; the earlier working name for K2 is dropped from CANDIDATES l.26, l.131 and l.202.

**Sources:** CC-148 r1, W5–W8, W11–W13; CC-151 r1, r2, r6, r13; PI-1026u Q1/Q4; PI-1026av Q1/Q2/Q5/Q7/Q8; PI-1026ay; PI-1026bb Q1–Q3; CC-119 W1, W19–W21, W25; K2 Gate 1 RULE (`2026-10-28_k2_gate1/RULE.md`); W25 RULE (`2026-10-28_w25_neardup/RULE.md`); CANDIDATES_2026-10-26 K1 (l.25, l.117–l.128) and K6 (l.183–l.192).

## 0. Which branch binds

| K2 Gate 1 outcome (`gate1_decide.json`) | Binding branch |
|---|---|
| **GO** | **Branch K2** (§4): K2 is the registered primary (PI-1026av Q1) |
| **NO-GO** | **Branch K1+K6** (§5): the headline is K1 + K6 (PI-1026u Q4); K2 gets no KV look |
| INCONCLUSIVE, NOT-RUN (cost), or no `gate1_decide.json` by the freeze date | **Branch K1+K6** by default; the PI may rule before the freeze that K2 enters KV as a descriptive arm with no H. Nothing else changes. A NOT-RUN (fault) is rerunnable (K2 Gate 1 RULE §7) and switches nothing by itself |

- A GO only activates the K2 branch of this already-committed text. Gate 1 numbers are never reported as a finding.
- Measured Gate 1 rates may enter this PREREG only through the cost-only amendment of §8.
- Both branches share §1–§3 and §6–§10.

## 1. Test set, gold and matcher

- **Test: KV-4,224** = Karpathy val 5,000 − 130 refused (CHAIR-500 61, POPE-500 70) − 130 UT-2,532 ids − 516 A-touched (PILOT_RULE §1; `id_counts.py` `kv_pool_a_excluded`). **Pinned now (CC-153 W10):** the id list's sha256 is `86d9386324e8cb34c4c7216e494b21da0cbcfe458702952b9ce261a9f608f8f9` (`2026-10-27_grl_pilot/id_counts.json` l.75, `id_lists_sha256.kv_pool_a_excluded`), i.e. the sha256 of the integer COCO ids in ascending numeric order, one per line, each ending in `\n`, UTF-8, no header (`id_counts.sha_ids`). `kv4224.txt` is written in exactly that format, its file sha must equal this pin, and it is added to this folder and committed before any KV image is staged. `scripts/grl/id_counts.py` asserts `kv_pool_a_excluded == 4224` (`EXPECT` l.39, `check(got, EXPECT)` l.122) before it writes any list; that run, with rc 0, precedes any KV staging. The format is the one of `kv5000.txt`, whose file sha equals its `id_lists_sha256.kv` entry (b7a7a89d). No code writes `kv4224.txt` yet: its writer is one entry added to `id_counts.py`'s `lists` (l.127), a code change committed and judged separately before staging. A mismatch of count or sha is a FAULT before staging. KV-4,740 and KV-5,000 are reported beside it, descriptive (PILOT_RULE header).
- **Gold (CC-119 W21):** COCO-2014 instance classes of `instances_val2014` (80 categories, crowd included), the definition of `gold_instances.json`. The KV gold file is built by id, sha-pinned before the freeze, and read only by the scoring code.
- **Matcher (CC-119 W20):** v2 scores; v1 is reported beside it. Negated or hedged mentions count as hallucinations, never as TPs.
- **Rates:** CHAIR_i = Σhal / Σmen × 100 (pooled); R = Σtp / Σ|gold| × 100. Every decode passes through `untruncate` before scoring.
- **No Vietnamese references exist on KV**: no test CIDEr. Every metric is gold-instance based, COCO-80 only.
- **Training side:** every training pool is UT-2,402 minus the W25 exclusions (K2 branch), or goes through the same W25 pass before any training (K1 pools; CC-119 W25).

## 2. One pinned decode path, one scoring event (CC-148 W7, W8)

- **Student path:** venv-q3 (freeze 2bb7397e), the 4-bit NF4 base + the arm's LoRA adapter, not merged, greedy, 512 new tokens, batch 4, `min_pixels` 262,144, `max_pixels` 1,048,576, `PROMPTS["detailed"]` (sha 0addb5dd). The base is re-decoded on the same path (**base_s**, fresh zero LoRA). No venv-lb Gate 0 decode is reused on KV.
- **Freeze, about 11-18 (VN).** Each KV prediction file is sha256-hashed when its decoder finishes and appended to `KV_PRED_SUMS` (fsync). **No one opens a KV prediction**: not the operator, CC, Ken or a judge; only the scoring code reads it, once. The gatekeeper's commit of `KV_PRED_SUMS` with the shas of the KV gold, `kv4224.txt` and the scoring code is the freeze.
- **A system not in `KV_PRED_SUMS` at the freeze loses confirmatory status** (PI-1026av Q2). If any registered seed of a system an H uses is missing, that H is NOT-RUN and the sequence stops there; an H is never tested with fewer seeds than registered. A system added after the freeze is "post-freeze, descriptive".
- **Scoring:** one run of the MT4 scorer after the freeze writes `mt4_decide.json`. That write is the look: no rescoring, no matcher or gold change.
- **Fault before scoring** (sha mismatch, broken file): NOT-RUN (fault) → TO-PI; no re-decode after the freeze without a new ruling.
- **Machine:** KV images are staged and decoded on M3 only, after C-EN has finished, under a guard amendment written with the decode code, and deleted at cleanup (CC-148 W12). M4 runs no KV step.
- **Confirmatory training machine (CC-153 W12):** every confirmatory training run of either branch (K, U, Kd, SFT-ref; K1, K6) runs on M3, the test-capable machine. Paper A's N9 and PASCAL-50S jobs on M3 and B-1 on M4 keep priority over it; the freeze date (§2) does not wait for them, and a system not trained by the freeze loses confirmatory status as written.

## 3. Statistics (both branches)

- **Seed pooling.** For a multi-seed system, the per-image counts (hal, men, tp, |gold|) are summed over its seeds; the system's CHAIR_i and R are the pooled ratios. Every seed has equal weight (same images). Per-seed estimates and min/max are reported beside it. An H that holds pooled while a single seed points the other way still holds, and this is stated.
- **Paired image bootstrap:** B = 2,000, `numpy.random.default_rng(0)`. One index draw per replicate, shared by every system and seed; seeds are fixed, not resampled. CIs are percentile 2.5 / 97.5.
- **What the CIs cover (CC-153 W9).** The bootstrap CIs resample images only. They are conditional on the registered seeds and exclude seed-to-seed (training) variance; per-seed estimates with min/max are shown beside every pooled number. Training and decoding are also not bit-reproducible beyond seed control (bf16 / NF4 kernels and cuDNN nondeterminism), so a rerun with the same seed may differ; no rerun is made after the freeze (§2).
- **Fixed sequence.** Each branch's H's are tested in the written order at α = 0.05 (two-sided 95% CIs). A later H is tested only if every earlier one holds; this keeps the family-wise error at 0.05 without correction. An H after the stop is reported as "not tested (sequence stopped at Hk)", with descriptive numbers.
- **SESOI:** CHAIR_i −3.0, recall margin −2.0 (CC-119 W1; frozen; no new SESOI after the dev values were seen).

## 4. Branch K2 (binds on a K2 Gate 1 GO)

**Systems and seeds (CC-148 r1):**

| System | Seeds on KV | Role |
|---|---|---|
| base_s | 1 decode (deterministic) | comparator of H1, H2 |
| **K** (K2 gold-edited) | **3** | the primary system |
| **U** (SFT-unedited) | **3** | comparator of H3 |
| Kd (K2 detector-edited, GD-T 0.30) | 2 | H-P2r secondary only |
| SFT-ref (UT-2,402 references; not K1) | 2 | F1 form (a) reference row |
| base_bf16 (bf16 on the student path) | 1 | diagnostic; first item of the §8 cost ladder |

- **Confirmatory seeds are new training runs.** Default: seeds **1, 2, 3** (K, U) and **1, 2** (Kd, SFT-ref); seed 0 is excluded because it would recreate the Gate 1 dev adapter, and Gate 1 adapters are never test systems (PILOT_RULE §6). The seed sets the LoRA initialisation and the example order (`train.schedule(keys, 2n, seed)`). The trainer change that exposes the seed is a code commit, judged, before any confirmatory training.
- **Reused training data:** the Gate 1 teacher decode, D(img) and targets (their shas asserted); they are training data, not systems.
- **Training config:** K2 Gate 1 RULE §2 verbatim (W22-SFT C1, r 16, α 32, lr 1e-4, exactly 2 epochs, last checkpoint, no grid, 1:0 mix). An OOM is NOT-RUN (fault) → TO-PI, never a C2 switch (CC-151 r13).

**Hypotheses (fixed sequence H1 → H2 → H3; CC-148 r1):**

| | Hypothesis | Holds when |
|---|---|---|
| **H1** | K vs base_s: fewer hallucinations at near-equal recall | point ΔCHAIR_i ≤ −3.0 **and** its CI upper bound < 0, **and** point ΔR ≥ −2.0 |
| **H2** | K vs base_s's clause-truncation frontier at R(K) | gap = CHAIR_i(frontier at R(K)) − CHAIR_i(K): point ≥ 3.0 **and** CI lower bound > 0. Frontier as K2 Gate 0 §6b on base_s's KV captions, recomputed in each bootstrap draw. **Low clamp** (R(K) below the one-clause recall): H2 not supported, sequence stops. **High clamp** (R(K) above the uncut base recall): read at the endpoint and flagged (K2 Gate 1 RULE §7, CC-151 r4) |
| **H3** | K vs U: the edits, not self-training, carry the effect | point ΔCHAIR_i ≤ −3.0 **and** its CI upper bound < 0. ΔR(K − U) is reported |

- **Recall form (CC-153 W8, ruling 8).** H1's recall check is the CC-148 r1 point form (point ΔR ≥ −2.0), accepted in PI-1026av; it is not a non-inferiority test and no non-inferiority claim is made. The CI lower bound of ΔR is reported against −2.0 as descriptive only. The CHAIR_i forms are unchanged. PI Q1 of CC-153 (switch to the CI form, lower bound > −2.0) is open; the default is the point form, and a "CI form" answer is applied before this PREREG is committed, never after.

**Registered secondaries (never gating, no claim; CC-148 W6):**
1. Matched-count F1, form (a) (PI-1026aa; Paper A's estimator, cited as a tool): K vs base_s (CI lower bound > 0) and K vs SFT-ref (non-inferior at margin −1.0). MT4 makes no count-control claim.
2. H-P2r (P2 licence, K2_GATE0_RULE l.237): R(K) − R(Kd) ≥ 2.0 with CHAIR_i non-inferior at margin +1.0; K 3 seeds, Kd 2, pooled as §3.
3. Lexicon-evasion share, v2 only: (i) share of captions with 0 v2 mentions; (ii) v2 mentions per 100 words; (iii) per 100 words, the frequency of the generic-noun list L_h. Flag: (ii) down **and** (iii) up for K vs base_s, both CIs excluding 0. **L_h is written and committed by a human (the PI) before the freeze**, not by Ken or CC; if it is not committed by then, (iii) and the flag are not reported and (i)–(ii) are.
4. The English arm (§6).
5. Descriptive: mean words, out-of-script share, cap-hit share, v1 vs v2, check T on KV, base_bf16 vs base_s.

## 5. Branch K1+K6 (binds on a NO-GO, and by default on INCONCLUSIVE or NOT-RUN)

**Systems (CANDIDATES_2026-10-26 l.25, l.117–l.128, l.183–l.192):**
- **K1 (Strong-SFT):** all-gold multi-reference SFT on Qwen3-VL-8B over KTVIC + UIT-ViIC + OpenViIC training data (fuse multi-reference targets), short mode. Seeds: **2** (default; §8 ladder).
- **K6:** the K1 recipe on Qwen3-VL-4B. **K6 needs a pinned 4B model before the freeze, or it is dropped** (CC-148 W8); then H-B2 is "not tested (K6 not frozen)".
- **base8_s:** Qwen3-VL-8B zero-shot on the K1 decode path, short and detailed (1 decode each).
- **Metric of H-B1/H-B2 (short mode).** Prompt `PROMPTS["short"]` of `scripts/evaluate.py`. P, R and F1 are `object_prf.prf` over `object_prf.image_counts`, the scorer of the CANDIDATES §1.1 short rows (`object_prf-short.txt`), with gold = the W21 instance classes only (KV has no Vietnamese references, so the reference-class union of `instance_block` is empty). Detailed-mode CHAIR_i is §1's.
- **Entry conditions of Branch K1+K6, before any K1/K6 training:** its own dev rule, which must fix (a) the short-mode `max_new_tokens` (`evaluate.py`'s default is 160; the Gate 0 short runs' value is not verified here), (b) the K1 decode path used for K1, K6 and base8_s (venv, precision, merge or not), (c) the training mix and epochs, (d) the language gate on short-mode CJK leakage; and the W25 pass of every K1 pool. Until that rule is committed, Branch K1+K6 cannot run. This PREREG fixes the test side only.
- **Money, freeze and exclusions of Branch K1+K6 (CC-153 W11; PI Q2, recommended YES).** The unspent K2 test line (§8; K2 gets no confirmatory training on this branch) funds the K1 dev rule, the W25 pass of the K1 pools, K1 × 2, K6 and base8_s, all within the 170 GPU-h total (PI-1026bb). The branch's freeze date is set in the cost-only amendment (§8), before any K1 training and never after any KV prediction exists; if the projected costs do not fit or no such date can be set, H-B1 is NOT-RUN (cost) → TO-PI. The ~11-18 freeze (§9) is probably not met on this branch. Every K1/K6 training pool passes `exclusion.json` plus the W25 near-duplicate pass against every group test set: KTVIC test, UIT-ViIC test (by id list, as UT-2,402), OV-test, XM, KV and OIV7 (CANDIDATES l.120: 401 KTVIC-test images sit in OpenViIC train).

**Hypotheses (fixed sequence H-B1 → H-B2):**

| | Hypothesis | Holds when |
|---|---|---|
| **H-B1** | K1 vs base8_s, short mode, instance F1 on KV (gold instances, matcher v2) | point ΔF1 ≥ +2.0 **and** CI lower bound > 0, **and** instance precision non-inferior (CI lower bound of ΔP > −1.0) |
| **H-B2** | K6-4B vs base8_s: deployable at no loss | CI lower bound of ΔF1 (short) > 0 **and** detailed CHAIR_i(K6) − CHAIR_i(base8_s) with CI upper bound < 0 |

- Secondaries: matched-count F1 form (a) for K1 vs base8_s; the English arm (§6, run with K1 in place of K); detailed-mode CHAIR_i and R of K1, descriptive (CANDIDATES expects a trade-off there).
- Pre-written framing: K1 is the strong baseline and data/backbone axis, not a method claim (CANDIDATES l.126).

## 6. English arm (both branches; ≤ 30 GPU-h; descriptive, no H; PI-1026av Q5)

- The binding branch's procedure moved to English unchanged, with no tuning: prompt `PROMPTS["detailed_en"]` of `scripts/evaluate.py` ("Describe this image in detail in English."), the same `units`, the same W21 gold; matcher = Rohrbach et al.'s CHAIR synonym list (EMNLP 2018, DOI 10.18653/v1/D18-1437) in place of v1/v2.
- Branch K2: teacher decode of the UT pool in English, then K-EN and U-EN, 1 seed each; KV decodes of base_s-EN, K-EN and U-EN. Branch K1+K6: K1-EN (English COCO references) and base8_s-EN.
- Reported: CHAIR_i and R with §3 bootstrap CIs, within English only. No cross-language difference is tested (as C-EN).
- Cap: ceil(1.2 × projection) ≤ 30, else the English arm is NOT-RUN (cost) → TO-PI. It never delays the H's.

## 7. Disclosures (CC-148 W13)

- Paper A's matched-count estimator is cited as a measurement tool; MT4 makes no count-control claim.
- Val 924 reuse (B's WiSE-FT gate, B decodes, G-RL dev, K2 Gate 0, P1, P2, Gate 1); all 924 are COCO train2014 and may be in pretraining data.
- UT-2,402 holds 88 A-touched and 857 restval ids (also in C-EN's memory): training-side facts, not test exposure.
- COCO-80 only; no Vietnamese references on KV, no test CIDEr.
- GD-T (det arm) may have seen Visual Genome images, which include COCO images.
- KV-4,224 excludes the 516 A-touched and 130 CHAIR/POPE-500 images. C-EN hashed and feature-extracted Karpathy val on M3 (no caption, prediction or score of any evaluated system, C-EN PREREG §3.3; CC-153 ruling 1); W25 reused those features. W25's `feats_ut.npz` and `oiv7_parts` are never committed and are read only by its decide step; only `w25_excluded_ids.txt` and `w25_decide.json` leave M3, through the gatekeeper (CC-153 W5).
- The training pool excludes the W25 near-duplicates of KV-5,000 and OIV7 val; the count is reported.
- CIs are conditional on the registered seeds (per-seed min/max shown) and do not include seed-to-seed variance; bf16 / NF4 and cuDNN nondeterminism remains beyond seed control (§3, CC-153 W9).
- The comparator is the NF4 base on the student path; the bf16 row is beside it where it was run.
- K2 training text is the backbone's own captions, edited against gold: training data, not evidence (no MT COCO, no AI-silver labels).

## 8. Budget (PI-1026bb Q3) and the cost-only amendment

| Line | GPU-h | Holds |
|---|---|---|
| dev | 40 | K2 Gate 1 36 + W22-SFT 0.75 + W25 3.25 |
| **test** | **100** | the confirmatory seed training (Branch K2: about 30 GPU-h for 3/3/2/2) **and** every KV decode |
| English | 30 | §6 |
| **total** | **170** | |

- Stage caps = ceil(1.2 × projection) to 0.1 GPU-h (CC-148 W11). A cap hit is NOT-RUN (cost) → TO-PI, never a negative result (CC-124 r2).
- **Planning projection, Branch K2 (unmeasured student rate):** 11 student-path KV decodes (base_s, K × 3, U × 3, Kd × 2, SFT-ref × 2) + base_bf16 = 12 × 4,224 images. At 3.25 s/img that is about 46 GPU-h; at the 6.5 s/img planning factor about 92 GPU-h. With about 30 GPU-h of training, the test line projects 76–122 GPU-h. It may not fit at 100.
- **Pre-written cost ladder (applied in this order, only by the cost-only amendment, until the caps fit test 100):**
  1. drop the base_bf16 KV decode (diagnostic);
  2. drop SFT-ref seed 2 (F1 form (a) K vs ref then on one seed, descriptive);
  3. drop Kd seed 2 (H-P2r then descriptive);
  4. drop SFT-ref entirely (F1 form (a) K vs ref not reported).
  The H systems (base_s, K × 3, U × 3) are never cut. If they alone do not fit, the result is NOT-RUN (cost) → TO-PI before any confirmatory training. Branch K1+K6 uses the same rule: K6 is cut before K1's second seed, and base8_s is never cut. On Branch K1+K6 the test line also carries the K1 dev rule and the W25 pass of the K1 pools (§5, CC-153 W11).
- **Cost-only amendment (allowed explicitly).** After the K2 Gate 1 timing probe and training rates exist (or the K1 dev rule's measured rates), one amendment may: replace planning rates by measured ones; recompute every projection and cap; apply the ladder above. On Branch K1+K6 it also sets that branch's freeze date under §5's rule (before any K1 training, never after any KV prediction); this applies the freeze rule and does not change it. It may **not** change any H, threshold, SESOI, matcher, gold, test set, freeze rule, the binding branch, or the seed count of an H system. It is committed before the first confirmatory training step, after a one-judge diff read. It is the only route by which Gate 1 numbers enter this PREREG (CC-151 r1).

## 9. Calendar (VN; CC-148 W14, CC-151 run order)

W25 on M3 → byte deletion logged → this PREREG committed → K2 Gate 1 (M3, before 11-06 12:00Z) → cost-only amendment → confirmatory training → freeze about **11-18** → scoring about 11-18..20 on M3 after N9 → MT4 writing after B freezes (11-30) and A freezes (12-18) → IP&M 01–02/2027. Gate 1 late means every later date slips; the freeze date does not wait for unfrozen systems (§2), nor for A's N9 / PASCAL-50S on M3 or B-1 on M4 (§2, W12). On Branch K1+K6 the freeze date is the one set in the cost-only amendment (§5, W11).

## 10. Pre-written report sentences (filled from `mt4_decide.json`)

**Branch K2**
- **H1–H3 hold:** "On Karpathy val (4,224 images after pre-registered exclusions), the gold-edited self-distilled Qwen3-VL-8B student (3 seeds) lowered CHAIR_i by X [CI] points relative to the same-precision base, with point Δrecall ≥ −2.0 (Δ Y [CI]); it was W [CI] points below the base model's clause-truncation frontier at equal recall, and Z [CI] points below a student trained on the same model's unedited captions (3 seeds). All three pre-registered hypotheses held in the fixed order."
- **Stop at H1:** "The pre-registered primary hypothesis was not supported: relative to the same-precision base, ΔCHAIR_i was X [CI] and Δrecall Y [CI]. H2 and H3 were not tested."
- **Stop at H2:** "The student reduced hallucination relative to the base (H1 held), but not by more than truncating base captions to the same recall: the gap to the truncation frontier was W [CI] (pre-registered ≥ 3.0 / frontier clamped). H3 was not tested. The reduction is therefore not distinguishable from producing shorter captions."
- **Stop at H3:** "Gold editing reduced hallucination beyond the base and beyond the truncation frontier, but its advantage over fine-tuning on the model's own unedited captions (Z [CI]) did not meet the pre-registered −3.0; part of the effect may come from self-training rather than from the edits."

**Branch K1+K6**
- **H-B1 holds:** "Fine-tuning Qwen3-VL-8B on all available Vietnamese gold captions raised short-mode instance F1 on Karpathy val by X [CI] points over its zero-shot output, with precision within the −1.0 margin. This is a strong supervised baseline, not a new method."
- **H-B1 fails:** "Fine-tuning on all available Vietnamese gold captions did not raise short-mode instance F1 by the pre-registered +2.0 (ΔF1 X [CI]); H-B2 was not tested."
- **H-B2:** "A 4B model trained with the same recipe matched or exceeded the 8B zero-shot model (ΔF1 X [CI]; detailed ΔCHAIR_i Y [CI])." / "… did not (…)." / "K6 was not frozen and was not tested."

**Both branches**
- **NOT-RUN:** "Hk could not be tested as registered (reason: …); no substitute analysis is reported as confirmatory."
- **H-P2r (secondary):** "As a secondary, gold-edited students had Y [CI] points higher recall than detector-edited students (CHAIR_i difference X [CI], non-inferiority margin +1.0)."
- **English arm:** "An English arm repeating the procedure with English prompts and the CHAIR synonym list is reported within English only, without cross-language tests."
- **Every outcome:** "Scoring covers the 80 COCO classes, with COCO-2014 instance annotations as gold; Karpathy val has no Vietnamese references. Training images that were near-duplicates of any Karpathy val or Open Images V7 validation image were removed before training."

## 11. Judge items (defaults written; the panel rules)

Ruled by CC-153 (II): M1 kept with W11, M2 point form kept with W8, M3–M6 accepted (W9, W11), M7 pinned (W10). M8: addressed by W7 (`PRIOR_ART_W23.md`), for the diff read.

- **M1.** §0: INCONCLUSIVE and NOT-RUN default to Branch K1+K6.
- **M2.** §4 H1: ΔR ≥ −2.0 on the point estimate (CC-148 r1 literal, default) or on the CI lower bound (Ken's non-inferiority form)? H1/H3: "point ≤ −3.0 and CI upper < 0" (default) or "CI upper ≤ −3.0"?
- **M3.** §4: confirmatory seeds 1–3 / 1–2, excluding seed 0 (default), and the seed = LoRA init + example order.
- **M4.** §5: K1 seeds 2, the H-B1/H-B2 forms (taken from CANDIDATES' prior and falsifier lines), and base8_s on the K1 decode path.
- **M5.** §4 secondary 3: L_h written by the PI before the freeze; whether L_h needs an AI-silver ruling (it is a measurement word list, not an image label).
- **M6.** §8: the cost ladder order, and whether the H systems' 7 decodes plus training must fit before any training starts.
- **M7.** §1: `kv4224.txt` written by the `id_counts.py` rule and pinned before staging.
- **M8.** CC-119 W23: is K14-1 plus its review enough to commit this PREREG? If not, W23 holds this PREREG and therefore every Gate 1 GPU step.

## Amendments

(none)
