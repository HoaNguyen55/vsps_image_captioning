# G-RL Gate-0 / Gate-1 dev pilot rule (CC-114, CC-118 W3, CC-119, PI-1026l, PI-1026r, PI-1026s, PI-1026u)

**Status: DRAFT, not committed.** Written 2026-10-27. No pilot output exists. No GPU was used, and no model output, caption, prediction or test file was opened. Before Gate 0, the judge panel reads this rule and `scripts/grl/`, and the gatekeeper commits both. `EXPECT_HEAD` in both runners is that commit.

**Sibling rule.** The K2 Gate 0/0b dev pilot (CC-119 ruling 4) is `K2_GATE0_RULE.md` in this folder. It shares the guard, gold and id lists, and on M3 it runs first (CC-119 PD-GR-3, ruling 8). Under PI-1026u Q1, K1/K2/K6 and G-RL are one MT4 paper; KV-4,224 is its one-look test.

**Label.** PILOT / DEV. This rule registers no confirmatory hypothesis. The pilot runs are not confirmatory seeds (CC-118 r5). Confirmatory claims belong to the later G-RL prereg (CC-118 W5), on KV-4,224 with KV-4,740 and KV-5,000 reported beside it.

## 0. Authority, and what changed since ALT_PLAN

| Source | What it fixes here |
|---|---|
| CC-114 W1–W13 | matched-count F1 is co-primary; one gold for reward and score; Gate 1 is gated against SFT-ref; SESOI 2.0 and margin −1.0 each get a source; Gate 0 is a measured-rate guard; MOCHa DOI (W11) |
| CC-118 r5, W2–W5; PI-1026u Q2 | Gate 1 runs on the full Gate-1 pool **UT-2,402** (2,532 minus the 130 Karpathy-val ids, a pre-fixed, disclosed leakage exclusion; 2,532 reported beside it) and the full val 924. The cap comes from Gate 0's rate (planning figure ~25–40 GPU-h). One look and a stop rule. The ID script comes first |
| PI-1026l | the KV and UT pools belong to G-RL; this overrules CC-106 l.105 and PI-1026d's pool plan |
| PI-1026r (2) | the pilot runs on **M3**, not M4, which amends CC-114 r8 and CC-118 W2. M3 holds no test images. The pilot is interleaved with C-EN and never runs during a test decode |
| CC-114 Q3 / CC-118 r11 | dev = the official UIT-ViIC val 924 |
| CC-119 r4, r8, r10; CC-120; CC-121 | M3 isolation from C-EN (§7); K2 Gate 0/0b runs before this pilot |
| PI-1026aa | Q3: form (a) is the confirmatory H1 form, co-primary with raw F1; G2's matched-count F1 is a reported secondary. Q5: YES (K2 training text). Q6: M4 only after a K2 or G-RL Gate 1 GO. Memory fallback: no `PI_OK=3B` pre-authorisation; a STOP asks the PI when it happens |
| CC-124 W1–W8 | tmux + lock + m3_clear as the isolation controls; training-side C-EN sha refusal; list-style reward gate; 3 GPU-h Gate-0 wall and remaining-cap timeouts; ladder 35 / 25 / 40 with memory STOP → TO-PI; H_matched pilot form (a); operator order |
| PI-1026s | gates that only protect a calendar do not bind work start. CC-118 r2's "after A's IP&M manuscript number" and "after the C-EN test window" are lifted for this pilot (CC-119 ruling 4); their real content is kept as the §7 isolation conditions |

**Struck from ALT_PLAN_AGENT_2026-10-26.md** (CC-118 W3). The plan file itself is not edited here.
- l.87: "≤ 8 GPU-h", "400 images", "dev-500 (restval)", "M4 after Ken's pilot, from 12-01", and the ΔRecall ≥ −1.0 gate against base.
- l.154: "from 12-01".
- l.52: "not used by A/B/C" is false. A touched 516 KV images (CC-106 l.48).

## 1. Populations (ID-only; `scripts/grl/id_counts.py`)

`id_counts.py` asserts every value below and writes `id_counts.json` with the sha256 of each input and each list. It reads ids only.

| Quantity | Value |
|---|---|
| Karpathy val (KV) | 5,000 → 4,870 (minus 130 refused: CHAIR-500 61, POPE-500 70) → 4,740 (minus 130 UT images) → **4,224** (minus 516 A-touched) |
| UIT-ViIC train | 2,695 − 163 refused (Karpathy test 133, COCO-2500 59, CHAIR-500 14, POPE-500 21; the sources overlap) = **UT-2,532**. The 2,695 is reported beside it |
| train ∩ KV | 132 raw; 130 after the refusals. These 130 are outside KV-4,740, so UT ∩ KV-4,740 = UT ∩ KV-4,224 = 0 |
| **Gate-1 pool** (PI-1026u Q2) | **UT-2,402** = UT-2,532 minus the 130 Karpathy-val ids, so that no model output ever exists on Karpathy val (C-EN PREREG l.67/l.159; CC-119 W19). UT-2,402 ∩ KV = 0. The 130 ids are never staged on M3 |
| C-EN lists (CC-119 W19) | train-2,695 ∩ `cen_coco_kval` = 132, ∩ `cen_coco_test` = 133; UT-2,402 and val-924 ∩ either list = 0. On M3, every staged image (train and val) is also refused if its sha256 is in C-EN's three test-side records, which cover Karpathy test, Karpathy val and NoCaps val, so a byte copy of a test image under a train id (the CC-122 class) never reaches the machine (CC-124 W3) |
| UIT-ViIC val | **924**. 0 exclusion hits, 0 KV overlap, 0 A-touched (a_n3 ∪ gt_cache); all 924 are Karpathy train |
| References | UT-2,402 has 12,012 (UT-2,532: 12,667); val-924 has 4,620 |
| Restval reconciliation (CC-114 W2) | 30,504; 29,770 after removing exclusion.json ids; 28,913 after also removing UIT-ViIC train (885). Both CC-114 figures are right under their own definitions. CHAIR ∪ POPE inside restval is 734 ids; the 739 figure is their sum (5 ids are in both) |
| Disclosure | UT-2,402 holds 88 A-touched ids and 857 restval ids (also in C-EN's memory); UT-2,532 holds 101 and 885. These are training-side facts, not test exposure |

`exclusion.json`'s image_sha256 rule needs the image bytes. The M3 runner applies it (§7).

Training: Gate 1 uses UT-2,402 (PI-1026u Q2). Every result table reports the 2,532 and 2,695 counts beside it; no model is trained or decoded on the 163 refused or the 130 Karpathy-val ids.

## 2. Base model and framework

**Base: Qwen/Qwen2.5-VL-7B-Instruct @ cc594898 (Apache-2.0), 4-bit NF4 QLoRA. Fallback: Qwen2.5-VL-3B-Instruct @ 66285546 (qwen-research licence, disclosed).**

Models cached on M3 (m3_rebuild_2026-10-26.log §4): Qwen2.5-VL-7B, Qwen3-VL-8B, InternVL3-8B (-hf) and SigLIP2. No 3B or 4B model is cached.

| Candidate | For | Against |
|---|---|---|
| **Qwen2.5-VL-7B** (chosen) | It is the only model with a measured QLoRA on-policy RL run on a 3090 here: CN-RLOO v3 peaked at 20.23 GB reserved at 9.80 s/img (k = 8, ≤ 40 tokens; `.session_backup/2026-10-13/rl_35e/g1_cn_v3_s42/summary.json`). The policy code `rl_policy.py` (sha 7644e567, the rl_gate_v2 pin) is CPU-tested on it (`test_train_rl.py`). Its venv is pinned (`.venv` 7332d343: transformers 4.51.3, peft 0.21.2, bitsandbytes 0.50.2). All four of the group's training negatives used this backbone (FAIR 4-bit DPO, B's DPO and RFT, CN-RLOO), so an on-policy result is not confounded by a backbone change. That matters for the mechanism framing (CC-114 W10d) | It is older than Qwen3-VL. The novelty table draft and ALT_PLAN name Qwen3-VL-8B |
| Qwen3-VL-8B @ 0c351dd | newer; named in ALT_PLAN and the novelty draft | **No M3 venv can QLoRA-train it.** `.venv` has transformers 4.51.3, which predates Qwen3-VL. `venv-lb` has 4.57.6 but no peft or bitsandbytes. The group has never trained it (B1 aborted at Step 1). `rl_policy.py`'s cache replication (`DynamicCache.key_cache`) is untested under 4.57. B1's zero-shot guard **FAILED** on KTVIC dev300 (`step1_dev300_guard.json`: short CJK 3% > 2%; detailed 5.1 mentions, outside the [0.8, 3.5] band). The band is a KTVIC-frontier guard, not a G-RL criterion, but the CJK rate bears on the language gate. No 4B fallback is pinned anywhere |
| InternVL3-8B | cached | The repo has no RL or QLoRA path for it |

Whether G-RL moves to Qwen3-VL-8B, the merged paper's K2 backbone, is open question 4. It needs a new pinned venv and a port of `rl_policy.py`.

**Framework: a minimal custom loop, not TRL GRPOTrainer.** `.venv` pins trl 0.19.1. I have not verified that 0.19.1's GRPOTrainer supports image inputs, and an upgrade would mean a new, unpinned stack. The loop is `train_rl.update` with three changes:
- the reference is the base model (adapter disabled);
- the reference pass is chunked like the policy pass;
- the reward is the one in §4.

It calls the `rl_policy.py` primitives unchanged.

**Fallback prerequisite (only on a SWITCH-3B verdict):** download Qwen2.5-VL-3B-Instruct at revision 66285546 into M3's HF cache and set `refs/main` to it, as `dl_models.py` does for the 7B. `train.py` refuses any other revision.

## 3. Arms (identical except for the training signal)

Every arm:
- starts from the same base with the same fresh LoRA: seed 0, r 16, α 32, language tower only, dropout 0;
- uses the same detailed prompt (`evaluate.py` PROMPTS["detailed"]) for sampling, training and decoding;
- has the base model as its KL anchor.

| Arm | Signal |
|---|---|
| base | none: zero-shot, scored as a reference row |
| **SFT-ref** | token NLL on all 12,012 UT-2,402 references, 2 epochs, lr 1e-4, 8 examples/step |
| **RFT** | the same SFT on the best-of-8 base sample per UT image under the §4 reward (ties go to the lowest index; images whose best reward is 0 are dropped), 2 epochs |
| **G-RL** | on-policy RLOO (Dr. GRPO baseline, no std normalisation; `rl_reward.rloo`). k = 8 at T = 1.0 (top_p 1, top_k 0), ≤ 160 new tokens, 5 images/step, one pass over UT-2,402 (481 steps), lr 2e-5, β = 0.03 k3 KL to base, ratio clip 0.2 (inert at one inner epoch), grad clip 1.0 |

RFT and G-RL draw the same number of samples from the same base: 2,402 × 8.

**Why every arm starts from base** (open question 3). ALT_PLAN asks about detailed captions. The UIT-ViIC references are one sentence each, so an RL arm started from SFT-ref would be stuck in the short regime, where precision is already near its ceiling. Starting all arms from base makes the comparison three training signals applied to one model and one set of images. The cost: SFT-ref will be short, so raw ΔF1(G-RL − SFT-ref) partly measures mention count. That is why matched-count F1 is co-primary (W1) and precision is non-inferiority-gated.

## 4. Reward and gold (W8)

**One gold.** COCO-2014 instance classes: the 80 categories with ≥ 1 instance, crowd included. Neither the reward nor the dev score uses reference-derived classes.
- Built ID-restricted, for UT-2,402 and val-924 only, from `instances_{train,val}2014.json` (pinned shas) by `reward.py gold` → `gold_instances.json` (3,326 ids, 0 empty, 3.52 classes per image). The K2 Gate 0/0b editor and scorer use the same file (CC-119 W21).
- It deliberately differs from `score_coco_probe.py`'s union with reference classes, because the reward never reads references.
- The later KV test uses the same definition on `instances_val2014`.

**Matchers.** v1 = the coco80_vi.json lexicon: longest phrase first, each matched span consumed. v2 = LEX_V2's 6 rewrites, then v1.
- The reward uses v1. The score uses v2, with v1 beside it.
- v1's rules are a subset of v2's. The detected class sets are **not nested**:
  - LEX_V2 removes v1 hits (*ghi bàn / bàn thắng / bóng bàn* is not a dining table);
  - LEX_V2 adds hits v1 misses (*cầu thủ / vận động viên / thủ môn / trọng tài / khán giả / người chơi* are person).
- UIT-ViIC is all ball sports, so the two diverge exactly here. `reward.py --selftest` pins both directions.
- The dev score reports, per system, the share of captions where v1 = v2.

**English (not in this pilot).** In the later English arm, the reward and the confirmatory score both use Rohrbach's synonym list (`data/coco_probe/chair_synonyms.txt`, `en_classes`) only.

**Reward per sample** (`scripts/grl/reward.py`): r ∈ [0, 1].
- **Gates (r = 0):**
  - unfinished at 160 tokens;
  - not Vietnamese-only: no Vietnamese diacritic, or any CJK character, or any out-of-script character (`clean_supervision` regexes);
  - a word 5-gram occurring ≥ 3 times;
  - list style (`reward.list_style`, CC-124 W4): a bare noun list, i.e. ≥ 4 segments of ≤ 3 syllables each when split at `, ; .` or a newline (comma, period and newline lists), or any bullet or numbered line. Ordinary multi-sentence captions have long segments and pass;
  - syllables outside the length window.
- **F1** over the v1 classes against the gold.
- **Matcher-gaming guard.** A class named only inside a negated or hedged clause counts as a false positive and earns no true positive. Clauses are split at punctuation and *nhưng*. Negation = *không có/thấy/phải/hề*, *chẳng*, *chưa có/thấy*. Hedges = `clean_supervision.HEDGE_RE`. Naming a class without asserting it never pays.
- A caption with no class, on an image with no gold class, scores 1. There are no such images here.

**Length window.** [0.75, 1.25] × the median syllable count of the base model's finished step-0 samples on **all 2,402 UT images** (Gate 1 stage 1). It is train-side and fixed before any training step or any dev decode. Gate 0 uses a provisional window from its own 40-image sample, for timing only.

## 5. Gate 0: measured rate and memory (`scripts/grl/gate0.sh`)

All stages use UT train images only. No val or test image is read.
1. Selftests, venv freeze check, guard (§7), staging, guard again.
2. Base sample of the first 40 schedule images (k = 8) → s_sample.
3. **30 G-RL steps** (150 images), preceded by a dry-run check:
   - generation-time log-probs of 2 samples equal the training forward's (mean gap < 0.02 nat/token);
   - sampler gap 0;
   - the loss mask covers generated tokens only (`guard_mask`);
   - every trainable tensor gets a gradient, with a finite, non-zero norm.
   This gives s_grl per image.
4. **30 SFT steps** (240 reference examples) → s_sft.
5. `evaluate.py` greedy decode (bf16, detailed, 160 tokens) of 40 train images → s_greedy, from its printed [40/40] rate.
6. `decide.py gate0`: peak = the maximum `max_memory_reserved` over stages 2–4; finished share = the share of the 320 stage-2 samples that end with EOS within 160 tokens. The projection to Gate 1 at the full data is
   GPU-h = [2,402·s_sample + 2,402·s_grl + 2·2,402·s_sft (RFT, upper bound) + 2·12,012·s_sft + 4·924·s_greedy] / 3600 + 1.2 h (loads and scans).

**Ladder.** The first matching rule decides. The Gate-0 adapters are discarded.

| Condition | Verdict |
|---|---|
| any dry-run check fails | **STOP** (a code fault; fix it, then a new judge read) |
| peak > 23.5 GB | **STOP → TO-PI** (CC-118 W3; the C3 failure was 24.9 GB). No automatic 3B fallback (CC-124 r7): a 3B Gate 0 runs only on a logged PI line `PI_OK=3B` in WORKFLOW_LOG, which `gate0.sh` accepts beside a SWITCH-3B verdict. Any 3B snapshot download (rev 66285546) is logged before the run and the qwen-research licence disclosed |
| finished share < 0.90 | **TO-PI**. The 160-token cap would truncate base detailed output, so the length window would come from a short tail, RFT would lose images, and most early G-RL rewards would be 0. The judges or PI set a higher pinned cap for sampling *and* decoding before Gate 1 |
| 7B and projected G-RL arm > 35 GPU-h | **SWITCH-3B**: Gate 0 once more at 3B (CC-124 W6; ALT_PLAN l.87's 25 amended) |
| 3B and projected G-RL arm > 25 GPU-h | **STOP** (CC-124 W6; ALT_PLAN's 15 amended) |
| projected total > 40 GPU-h | **TO-PI** (the top of CC-118's planning figure). Gate 1 runs only with a logged PI approval (`PI_OK`) |
| otherwise | **GO**. Cap = ⌈1.2 × projected total⌉ |

**Memory plan (24 GB).**
- 4-bit NF4 double-quant base. LoRA on the 7 language-tower projections only.
- 512 vision tokens (build_model's 24 GB budget).
- No gradient checkpointing, because the shared prompt KV cache needs `use_cache`. The prompt graph is kept across chunks.
- micro = 1: each backward covers ≤ 160 response tokens, the same as CN-RLOO v3's micro 4 × 40 tokens, which peaked at 20.23 GB (19.30 GB in its dry run, `c3.json`).
- `lm_head` runs on the last position only in generate and in the prompt pass. Its absence caused the 24.9 GB peak: a 2.7 GB fp32 logits block (`rl_policy.py` docstring).
- The reference pass is chunked by micro. train_rl's unchunked k-wide pass would need ~0.8 GB of fp32 logits, plus its logsumexp, at 160 tokens.
- The log-prob check uses 2 samples, not 8. At 8 × 160 tokens, `out.logits` would add ~1.5 GB.
- `expandable_segments`.
- Added over CN-RLOO: about 0.35 GB of sampling KV cache (8 × ~760 tokens × 57 KB).
- **Projected peak ≈ 20.5–21.5 GB at 7B**, against the 23.5 GB stop.
- The dev decodes use bf16 `evaluate.py`, the group's standard decode, already run on 3090s (B-N1, B-F1).

**Planning GPU-h (unmeasured; Gate 0 replaces these figures).**
- Scaled from the measured 9.8 s/img, G-RL at 7B is ~25–45 s/img: rollouts up to 160 tokens instead of 40, and 8 policy and 8 reference chunks per image.
- Gate 0 itself: ~1.5–2.5 GPU-h at 7B.
- Gate 1 at 7B:

| Stage | GPU-h |
|---|---|
| base samples | ~9 |
| G-RL | ~18–32 |
| SFT-ref + RFT | ~3 |
| 4 dev decodes | ~4–6 |
| loads | ~1 |
| **total** | **~35–51** |

- At 7B, SWITCH-3B or TO-PI is therefore a likely outcome. At 3B the total is roughly ~20–30 GPU-h.

## 6. Gate 1: full data, one look (`scripts/grl/gate1.sh`)

**Order.** Each stage is preceded by the guard (§7) and the cap check:
1. base samples on all UT-2,402;
2. the length window;
3. RFT picks;
4. G-RL, then RFT, then SFT-ref;
5. dev decodes of base, SFT-ref, RFT and G-RL on all val-924 (`evaluate.py`, bf16, greedy, detailed, 160 tokens);
6. `score_dev.py` (CPU);
7. `decide.py gate1`.

The cap is wall-clock GPU-h since Gate 1 started. If it is exceeded, the verdict is **STOP (cap)** with no result. The RFT pick count and the anchors' finished share are saved (`picks.jsonl.summary.json`, `anchors.json`) and copied into the decide file.

**Scoring** (`score_dev.py`, numbers only, refuses to overwrite).
- v2 primary, gold as in §4.
- Micro P = Σtp / Σmentions and R = Σtp / Σ|gold| (×100); F1 = 2PR / (P + R).
- **Matched count**: Paper A's matched prefix, cited as a tool (definition: `journal_draft/sec3_measurement_setup.md:36`, "the first k_i distinct classes in order of mention" at k_i = min(M_i^S, M_i^B)), computed on the COCO-80 v2 instrument (`score_coco_probe.py` v2); `c_stage1/score.py cm` is the same rule on the KTVIC instrument. Per image, both captions keep their first k = min(count_x, count_y) classes in order of first mention.
- Paired image bootstrap: B = 2,000, `default_rng(0)`, one resample shared by every contrast. The CI is the 95% percentile interval.

**GO iff all hold** (G-RL − SFT-ref unless stated):

| | Criterion |
|---|---|
| H_raw | ΔF1 ≥ 2.0 and its CI lower bound > 0 |
| H_matched_base (pilot form (a); CC-114 W1 amended for this pilot by CC-124 r6; PI-1026aa Q3: form (a) is also the confirmatory H1 form at the G-RL prereg, co-primary with raw F1, literal (b) reported beside; for G2 matched-count F1 is a reported secondary) | matched-count ΔF1(G-RL − **base**) CI lower bound > 0: the gain does not vanish at matched count against the model it started from |
| H_matched_sftref (pilot form (a), same amendment) | matched-count ΔF1(G-RL − SFT-ref) CI lower bound > −1.0 (non-inferiority). The literal CC-114 W1 contrast (matched ΔF1 vs SFT-ref, point and CI) is logged beside it as `logged_matched_dF1_v2_vs_sftref` |
| NI_precision | ΔP CI lower bound > −1.0 |
| G1 | Vietnamese-only share(G-RL) ≥ base − 0.5 pp |
| G2 | mean syllables(G-RL) inside the train-side window of `anchors.json` (not base greedy, which the cap may truncate) |
| G3 (matcher gaming) | NOT [classes per caption(G-RL) > 1.5 × base AND matched ΔF1(G-RL − base) CI lower bound ≤ 0] |
| G4 (matcher gaming) | captions with a negated or hedged class mention(G-RL) ≤ base + 2 pp |
| G5 (vocabulary hacking) | non-COCO object nouns per caption(G-RL) ≥ 0.9 × base. Nouns are counted by `rescap.chair.objects_in` on the text left after the v2 class spans are blanked |
| G6 (list style, CC-114 r6) | list-style captions(G-RL) ≤ base + 2 pp: a bare noun list, or bullet or numbered lines |

Otherwise the verdict is **STOP**. A STOP is labelled **under-moved** when G-RL's mean KL per caption over its last 50 steps is < 0.2 nat (the CN-RLOO under-moved threshold). The label explains the STOP. It does not change the verdict or allow a rerun.

**Why H_matched deviates from the literal W1 (blocking for the judge read).** W1 makes matched-count F1 co-primary with raw F1 and requires both to pass. Applied literally against SFT-ref (matched ΔF1 ≥ 2.0 and CI lower bound > 0), this criterion is very likely unpassable on this population, whatever G-RL does:
- In `gold_instances.json` (labels only), **97.0% of the val-924 images have both *person* and *sports ball* in gold**. The mean is 3.54 classes per image, and 0.1% of images have a single class.
- SFT-ref learns one-sentence references, so it will name about 1–2 classes. The matched prefix keeps k = min(count_G-RL, count_SFT-ref), which is about 1–2. Those first classes are almost always *person* or *ball*, so they are almost always gold.
- Both sides then reach the same matched tp for nearly every image, and matched ΔF1 ≈ 0 by construction. The gate would STOP after ~35–50 GPU-h without having tested anything.

The pilot form tests the two things matched count is meant to rule out:
- that G-RL's gain over its own start is only "say more" (against base, at similar counts);
- that G-RL is worse than SFT-ref at equal count (non-inferiority).

The same arithmetic will bind the confirmatory H1 on KV, so the panel should rule on it at the prereg. The options are:
- (a) this pilot form;
- (b) the literal W1;
- (c) start every arm from SFT-ref (open question 3).

`decide.py` implements (a).

**Logged, not gating:** G-RL − RFT (the on-policy question, H1-mech later), G-RL − base, RFT − SFT-ref, all of them under v1 as well, and v1 = v2 agreement.

**Stop rule.** One look. `score_dev` and `decide` refuse to overwrite.
- After a STOP, the negative is reported (CC-118 W5). There is no rerun, retune, new seed, new window or second look. Any further pilot needs a new judge ruling.
- A crash is not a verdict. Only the crashed stage is rerun, from scratch, and the rerun is logged.
- A GO is followed by the G-RL prereg (CC-118 W5): power from the paired variance in `scores.json`, seeds ≥ 2, and fresh confirmatory runs. The pilot adapters are never test systems.

## 7. Machine and data guard (`scripts/grl/common.py`)

The guard runs before every GPU stage. It refuses to proceed unless all of the following hold:
- `/root/.vsps_machine_id` ∈ {m3, m4}.
- `nvidia-smi` lists no compute process. The pilot never runs concurrently with another job, such as a C-EN test decode.
- **C-EN isolation (CC-119 W6/r10, CC-120, CC-121; C-EN has priority on M3)** (`common.m3_clear`):
  - C-EN's three test-side hash records are complete (`/root/outputs/c_en/fetch/{coco_test,coco_kval,nocaps_val}.done.json`). That pass is hash-only and writes no test bytes;
  - no protected set is staged: none of `$NCS_DATA/datasets/cen_{coco_test,coco_kval,nocaps_val}/` exists. C-EN's `--stage` writes a test set only there and its cleanup deletes it, so the pilot runs only after that deletion;
  - no C-EN process is running (`pgrep -f scripts/c_en/`).
- **Lock and controls (CC-124 W1, ruling 3).** `gate0.sh`, `gate1.sh` and `k2_gate0.sh` refuse to start outside a tmux session (`$TMUX`), hold `/root/outputs/grl_pilot/RUNNING` for the whole run and refuse to start if it exists. The three real controls:
  - C-EN → pilot: `cen_chain.sh:42` tmux exclusivity (C-EN PREREG l.129, committed at 30514a7) refuses to start any chain-driven C-EN step (feats, stage_coco, stage_nocaps) while any tmux session exists. It binds at code level because the runners require `$TMUX`.
  - pilot → C-EN: `common.m3_clear` before every GPU stage, plus the RUNNING lock for the whole run.
  - operator: no cen_chain step and no direct `cen_fetch.py --stage` is started while RUNNING exists.

  `cen_job.sh`, `cen_chain.sh` and `cen_fetch.py` are not edited before this commit (C-EN PREREG §13). A lock check at `cen_fetch.py` `if a.stage:` (l.406, the single writer of `cen_<set>/images`) is required at the next C-EN code amendment, and in any case before any G-RL Gate 1 run while C-EN is unfinished, because Gate 1's G-RL stage lasts about 20 h and the guard runs only at stage starts.
- HEAD equals `EXPECT_HEAD` and the tracked tree is clean.
- There is no `test*` file under `$NCS_DATA/datasets/uitviic`.
- Every image file under `/root/{outputs,queue,ncs-data,vsps}` (minus `.venv`, the roots `setup_gpu.sh` checks) passes the scan:
  - an image without a COCO-id file name is **refused**, because it cannot be shown not to be a test image (KTVIC, XM3600, NoCaps);
  - an image with a refused COCO id is refused. The refused ids are exclusion.json's 6,095 ids plus all of KV-5,000 (the 130 UT ∩ KV ids are out of the Gate-1 pool and never staged);
  - every image is hashed against exclusion.json's image_sha256 **and** against the sha256 column of C-EN's `coco_test`, `coco_kval` and `nocaps_val` records (`common.cen_test_shas`; CC-124 W3). On a GPU host a missing record is REFUSED.

C-EN's memory images (COCO train or restval minus the refused ids) pass.

**Staging** (`common.py stage`):
- inputs: the two release files, uploaded to `$NCS_DATA/datasets/uitviic/src/` and checked against pinned shas;
- the train file is cut to UT-2,402, so the 163 refused and the 130 Karpathy-val ids never reach the machine;
- val is unchanged;
- each image comes from its own `coco_url` and is hashed in memory;
- an image is refused if its hash is a test image's, or, for val, differs from `uitviic_val.tsv`;
- images are written by tmp + `os.replace`;
- `src/` is deleted after staging.

The pilot reads only UIT-ViIC train and val and the derived gold. No file of a test split is opened.

## 8. SESOI and margin, sourced before any data (CC-114 W6, CC-118 W3)

Every number below comes from an existing file. None is a G-RL output. C-EN's CIDEr-D +2.0 is not reused.

**SESOI: F1 2.0 points.**
- *Above instrument noise.* On the same captions, matcher v1 and v2 differ by 0.48 F1 points (short) and 0.72 (detailed). Source: `data/results/b1_qwen3vl/step1_dev300_guard.json`, KTVIC dev300 (Qwen3-VL zero-shot). 2.0 is about 2.8× the larger gap, so a pass cannot come from the choice of matcher version.
- *Resolvable at n = 924 in one look.* Existing val-924 decodes of B's adapters (`data/results/uitviic_ind_val/object_prf-detailed.txt`, fuse2_s42 − p1_s42) give paired ΔF1 CIs of [+4.5, +6.5] (instance + reference gold, v2) and [+6.6, +9.8] (exact match). That is SE ≈ 0.5–0.8. With a true effect of 2.0, P(CI lower bound > 0) ≈ Φ(2.0/SE − 1.96) ≈ 0.68–0.98.
- CC-098 also used +2.0, but that is precedent only, not a source.

**Margin: −1.0 point, on precision.**
- It is ½ × SESOI, and more than 2× the v1/v2 precision gap on the same captions (0.23 pp short, 0.46 pp detailed; same json).
- **Why precision, not recall** (ALT_PLAN l.87 used recall against base):
  - the known failure of an F1 reward is spraying mentions. Under instance gold, F1 rises with ln M (Paper A, `journal_draft/sec7_verbosity_sign.md` l.3, cited as a tool), and spraying shows up as a precision loss;
  - a recall loss already costs raw F1, which must gain ≥ 2.0;
  - H1 (ALT_PLAN l.79) puts the margin on precision.

## 9. Disclosures

- **Val 924 is not fresh.**
  - It is B's WiSE-FT gate set (α* was chosen on it; PD-31 DESIGN §4; CC-108 W9.4).
  - B's adapters were decoded on it earlier (`data/results/uitviic_ind_val/`). The author of this rule read only the two summary files' numbers, for §8.
  - All 924 images are COCO train2014, so exposure during pretraining is possible.
  - A's reference-statistic use of it (J3, CC-118 l.157) is not confirmed. The ID script finds 0 A-touched ids under the a_n3 ∪ gt_cache definition, but that does not settle it.
- **Reward vs score.**
  - The matchers differ (v1 vs v2), and their outputs are not nested (§4).
  - Under a v1 reward, sport-role nouns earn nothing, so the policy may drift toward *người*. The v1 rows beside v2 and the G5 guard watch for this.
- **Backbone.** This rule deviates from ALT_PLAN and the novelty draft (Qwen3-VL-8B with a 4B fallback). See §2.
- **Fallback licence.** The 3B fallback carries the qwen-research licence.
- **Pool.** Gate 1 trains on UT-2,402; the 130 Karpathy-val ids are excluded before any output (PI-1026u Q2), with 2,532 and 2,695 reported beside it.

## 10. Before Gate 0 (CC-118 W4, in order)

There is no date gate (PI-1026s). Every item below is a real prerequisite: it protects the one-look test sets, the instruments or the order on M3.

0. K2 Gate 0/0b is decided (`k2/gate0_decide.json` or `k2/STOP.md`; CC-119 PD-GR-3). Gate 1 also waits for K2 Gate 1 if that is approved, unless K2 stopped or a logged waiver (`K2_ORDER_WAIVER`) is given.
1. C-EN's CC-107 W3 shas are recorded, and the §7 isolation conditions hold.
2. `id_counts.py` is committed.
3. W8 (this §4) and W6 (this §8) are judge-read.
4. The W11 MOCHa DOI fix is made at all 5 live lines.
5. The judge panel reads the code in `scripts/grl/`.
6. The gatekeeper commits the rule and the code.
7. On M3, the operator:
   - writes `/root/.vsps_machine_id` (m3);
   - uploads `data/datasets/uitviic/{train,val}_data.json` to `$NCS_DATA/datasets/uitviic/src/`;
   - follows the CC-124 ruling-10 order: the pilot commit and M3 at `EXPECT_HEAD`; any ready C-EN step first (C-EN precedence); K2 Gate 0/0b in the first window with no C-EN step running or ready; then G-RL Gate 0 at 7B after K2 is decided; the W22 probe per CC-124 ruling 9; Gate 1 HELD;
   - checks before starting: M3 at `EXPECT_HEAD` with a clean tree; `memory.done.json` at 30514a7 present (recorded 112,320, refused 2); no `cen*` tmux session; `m3_clear` passes; the runner is started inside tmux; the window and the reason are logged in WORKFLOW_LOG. The C-EN test-side hash pass stored no bytes (`done.json` `stored = false`), so CC-119 r4's "test bytes deleted" is met by the records and the operative condition is `m3_clear` + the tmux rule.

## 11. Files

`SHA256SUMS` in this folder lists every file of the rule and of `scripts/grl/` (`sha256sum -c` from the repo root). The gatekeeper regenerates it at commit. `common.py` PINS holds the shas of every input, id list and reused script.

The selftests' Vietnamese strings are **synthetic matcher fixtures** built from lexicon terms and LEX_V2 patterns. They are not captions from any dataset or model.

## 12. Open questions for the judge panel (each with the recommended answer)

1. **Matched-count F1: settled by CC-124 r6 + PI-1026aa Q3.** The literal W1 test against SFT-ref cannot pass on this population (§6: 97.0% of val images have person and sports ball in gold). **Recommended:** the pilot form in `decide.py` (matched ΔF1 vs base CI lo > 0, and vs SFT-ref non-inferiority at −1.0), with the confirmatory H1 form ruled at the prereg together with PI Q3.
2. **Cost ladder: settled by CC-124 r7 / W6.** Switch at 7B above 35 GPU-h, STOP at 3B above 25, TO-PI above 40 in total. A 7B memory peak above 23.5 GB stays STOP → TO-PI with no automatic 3B (2/3, J1 dissents). PI-1026aa: no pre-authorisation; a 3B Gate 0 runs only on a PI line logged after the STOP.
3. **Start policy.** All arms start from base (§3). **Recommended:** keep base for the pilot, because it tests detailed captions, the merged paper's G1 regime. In the confirmatory paper, initialise the RL arm from K2 if K2 passes its Gate 1 (CANDIDATES K3 row), with base-start reported beside it.
4. **Backbone.** Qwen2.5-VL-7B here, while K2 uses Qwen3-VL-8B in the same merged paper (PI-1026u Q1). **Recommended:** G-RL Gate 1 waits for K2's W22 QLoRA probe, which it must wait for anyway under PD-GR-3. If the probe passes (Qwen3-VL-8B QLoRA ≤ 23.5 GB in a pinned venv), port `rl_policy.py` and run the G-RL pilot on Qwen3-VL-8B, re-reading the code first. If it fails, run this 7B rule as written and report the backbone difference. Update the novelty table row either way. **CC-124 r9:** G-RL Gate 0 runs at Qwen2.5-VL-7B as written after K2 is decided; a Qwen3-VL-8B port is a new rule version with a code read and a fresh Gate 0, and any 7B Gate 0 already run is kept as a disclosed timing record. If the W22 probe rule is committed before the G-RL Gate 0 slot, W22 (≤ 0.5 GPU-h) runs first.
