# K2 Gate 0/0b dev pilot rule: the target ceiling of gold-edited self-distillation (CC-119 ruling 4)

**Status: DRAFT, not committed.** Written 2026-10-27. No output of this pilot exists. No GPU was used, and no caption, prediction or test file was opened. Before any output, the judge panel reads this rule and `scripts/grl/k2_gate0.{py,sh}`, and the gatekeeper commits them. `EXPECT_HEAD` in `k2_gate0.sh` is that commit.

**What this measures.** Gate 0 asks whether the K2 target exists on dev: if val gold edits the zero-shot captions, how far does CHAIR_i fall, and how much recall and length survive? Val gold edits val captions, so **the numbers are a ceiling of the target only. They are never reported as a method result** (CC-119 ruling 4). K2 Gate 1 stays HELD until W9–W13 and W19–W23 are committed (ruling 5). The name "G-VSPS" is dropped (W23); the method is K2, gold-edited self-distillation, citing FAIR as prior work.

Sibling: `PILOT_RULE.md` (G-RL). Shared code: `common.py` (guard, isolation, staging, gold, id lists) and `reward.py` (matchers, negation/hedge rules).

## 1. Authority

| Source | What it fixes |
|---|---|
| CC-119 ruling 4, W1–W8, W19–W21 | this pilot: val 924 only, the frozen SESOIs, the STOP conditions, the M3 hygiene and the disclosures |
| CC-119 ruling 8 (PD-GR-3) | on M3: K2 Gate 0/0b first, then K2 Gate 1 when approved, then the G-RL pilot (`gate0.sh` and `gate1.sh` check this) |
| PI-1026r(3), PI-1026s | the first CC-119-approved pilot runs on M3 now; date-only gates do not bind (CC-118 r2/r3 are amended for this pilot) |
| PI-1026aa | Q5 YES: the backbone's own gold-edited captions may be K2 training text (training data, never evidence, no MT COCO); Q6: M4 only after a Gate 1 GO |
| CC-124 r2, W1, W2, W8 | 5 GPU-h ceiling (amends CC-119 r4); cost NOT-RUN is never a negative pilot; tmux + lock + m3_clear controls; operator order |
| PI-1026u | Q1: K1/K2/K6 and G-RL are one MT4 paper; KV-4,224 is its one-look test. Q2: the Gate-1 pool is 2,402. Q4: K1+K6 is the registered primary, and K2 is promoted only on a Gate-1 GO. Q7: G1′ on OIV7 val is the fallback |

## 2. Frozen now (W1, W3, W4, W5, W21)

| Item | Value |
|---|---|
| SESOIs (W1) | **CHAIR_i −3.0**, **recall margin −2.0**. PROPOSAL l.101's `min(3.0, 0.5 × gain)` is struck. No SESOI moves after Gate 0 |
| Model | Qwen/Qwen3-VL-8B-Instruct @ 0c351dd, the 14 snapshot files pinned by the B-N1 registration (sha 9ff02dc2), at `/root/ncs-data/models/Qwen3-VL-8B-Instruct-0c351dd`; bf16, sdpa, batch 4, `min_pixels` 262,144, `max_pixels` 1,048,576 |
| Decoder | `scripts/lb/decode_hf_vlm.py` unchanged (sha e2de1881, B-N1's pin), `/root/venv-lb` (freeze 685ffe2a: torch 2.5.1+cu121, transformers 4.57.6). Greedy (`do_sample=False`, `num_beams=1`) |
| Prompt | `evaluate.py` PROMPTS["detailed"] (sha 0addb5dd), Vietnamese |
| `max_new_tokens` (W3) | frozen by the probe (§4): the smallest of 256 / 384 / 512 / 768 / 1024 that cuts < 10% of probe captions (J3's < 10% cap-hit target). The same value binds the zero-shot comparator, the teacher and the student in every later K2 stage. 160 is excluded: it cuts 99.7% (CC-119 W3) |
| Truncated final clause (W3) | on a cap-hit caption, the last unit is dropped unless it ends in . ! ? (`untruncate`), before both editing and scoring, for every row |
| Editor (W5) | units = maximal runs ending at . , ; : ! ? or a newline. A unit is deleted if it names a COCO-80 class (matcher v1: `score_coco_probe.py` d11db7e1 with `coco80_vi.json` 926e0857) absent from the image's gold, or if it fails the language check (CJK or out-of-script characters, `clean_supervision` 01f17200). A trailing , ; : becomes "." |
| Gold (W21) | one definition: COCO-2014 instance classes, i.e. `gold_instances.json` (sha 42c100f5), the G-RL reward's gold. It is used for the editor, the scorer, G1 and later KV. CHAIR_i under instances ∪ reference classes (val references, matcher v2, as B's object_prf) is reported as a diagnostic only |
| Scorer (W20) | matcher v2. A class named only in a negated or hedged unit (`reward.NEG_RE`, `clean_supervision.HEDGE_RE`) is a hallucination and never a true positive, as in `grl/reward.py`. CHAIR_i = Σ hallucinated / Σ mentioned classes (pooled, ×100); R = Σ tp / Σ |gold| (×100). Paired image bootstrap B = 2,000, `default_rng(0)` |
| Length rule (W4) | one rule everywhere: mean words ≥ 90% of zero-shot (replaces 75% and ±25%) |

## 3. Data and isolation (W6, W19)

- **Scored set:** the full UIT-ViIC val 924 (`uitviic_val.tsv`, sha 338252e1).
- **Probe set:** the first 40 UT-2,402 train ids of the seed-0 schedule, decoded at 1024 tokens for length and rate only. No val image is decoded before the freeze, and the probe captions are never scored.
- **ID and hash asserts (W19), before the val decode** (`k2_gate0.val_ids_ok`): the manifest is exactly val-924 and has
  - 0 ids in Karpathy val or test, or in any exclusion.json source;
  - 0 ids in `cen_coco_kval` / `cen_coco_test`;
  - 0 image sha256 in C-EN's three test-side records (`coco_test`, `coco_kval`, `nocaps_val`.sha256.tsv), which covers NoCaps val.

  `id_counts.py` pins the id half: val ∩ cen lists = 0, UT-2,402 ∩ cen lists = 0, and train-2,695 ∩ `cen_coco_kval` = 132 and ∩ `cen_coco_test` = 133, as the judges found.
- **PROPOSAL l.104 corrected:** "No KV image is decoded" holds for KV-4,224 only in the proposal's wording. In this design **no Karpathy-val image is decoded at all**. The 130 UT ∩ KV ids are outside the Gate-1 pool (PI-1026u Q2) and are never staged.
- **M3 isolation (W6; CC-120, CC-121; C-EN has priority).** `common.guard` runs before every GPU stage. It refuses to proceed unless all of the following hold:
  - C-EN's three test-side hash records are complete (the hash-only pass writes no bytes);
  - no protected set is staged (`$NCS_DATA/datasets/cen_{coco_test,coco_kval,nocaps_val}/` absent, i.e. C-EN's cleanup has deleted it);
  - no C-EN process is running;
  - the GPU is idle;
  - HEAD equals the commit and the tracked tree is clean;
  - no image under `/root/{outputs,queue,ncs-data,vsps}` is a test image or unidentifiable.
- **Lock and controls (CC-124 W1, ruling 3).** `k2_gate0.sh` (and the G-RL runners) refuse to start outside a tmux session (`$TMUX`), hold `/root/outputs/grl_pilot/RUNNING` for the whole run and refuse to start if it exists. The three real controls:
  - C-EN → pilot: `cen_chain.sh:42` tmux exclusivity (C-EN PREREG l.129, committed at 30514a7) refuses to start any chain-driven C-EN step (feats, stage_coco, stage_nocaps) while any tmux session exists. It binds at code level because the runners require `$TMUX`.
  - pilot → C-EN: `common.m3_clear` before every GPU stage, plus the RUNNING lock for the whole run.
  - operator: no cen_chain step and no direct `cen_fetch.py --stage` is started while RUNNING exists.

  `cen_job.sh`, `cen_chain.sh` and `cen_fetch.py` are not edited before this commit (C-EN PREREG §13). A lock check at `cen_fetch.py` `if a.stage:` (l.406, the single writer of `cen_<set>/images`) is required at the next C-EN code amendment, and in any case before any G-RL Gate 1 run while C-EN is unfinished, because Gate 1's G-RL stage lasts about 20 h and the guard runs only at stage starts.
- **Operator checklist and order (CC-124 W8, ruling 10).** Order on M3: (1) the pilot commit, M3 at `EXPECT_HEAD`; (2) a C-EN step whenever one is ready (C-EN precedence); (3) K2 Gate 0/0b (probe + val decode, one tmux run, one lock, 5 GPU-h ceiling) in the first window in which no C-EN step is running or ready to start; (4) G-RL Gate 0 at 7B after K2 is decided; (5) the W22 probe per CC-124 ruling 9; Gate 1 HELD. Before starting: M3 at `EXPECT_HEAD` with a clean tree; `memory.done.json` at 30514a7 present (recorded 112,320, refused 2); no `cen*` tmux session; `m3_clear` passes; the runner is started inside tmux; the window and the reason are logged in WORKFLOW_LOG. The C-EN test-side hash pass stored no bytes (`done.json` `stored = false`), so CC-119 r4's "test bytes deleted" is met by the records; the operative condition is `m3_clear` + the tmux rule.

## 4. Steps (`scripts/grl/k2_gate0.sh`)

1. Selftests: `common`, `reward`, `k2_gate0` and the LB decoder's own `--selftest`. Then the venv-lb freeze check, guard, staging (shared with G-RL) and guard again.
2. **Probe** (GPU): 40 UT train images at 1024 new tokens. Decoder lines are time-stamped; GPU memory is polled every second.
3. **Freeze** (CPU, `k2_gate0.py freeze`):
   - `max_new_tokens` as in §2;
   - s/img = the probe's slice-to-slice rate (model loading and the batch-1 parity pass excluded), scaled by decode steps per batch slice at the frozen value;
   - projected Gate 0 GPU-h = 924 × s/img / 3600 + 0.1 h;
   - **cap = ⌈1.2 × projected⌉ to 0.1 GPU-h**.
   - **NOT RUN (cost) → TO-PI** if no ladder value cuts < 10%, or if the cap exceeds the **5 GPU-h ceiling**. CC-124 ruling 2 amends CC-119 r4's 2 GPU-h: that figure was computed at 160 tokens (1.36 GPU-h), which CC-119 W3 forbids, and CC-119 l.55 itself says the cap comes from the probe. At 5 GPU-h the freeze admits 256 and 384 at the all-hit bound, 512 depending on the measured slice lengths, and refuses 768 and above; expected spend is about 2.5–4.5 GPU-h.
4. **Gate 0** (GPU): val 924 at the frozen value, under `timeout` = cap. A cap timeout (124) is NOT RUN (cost) → TO-PI; any other non-zero exit is NOT RUN (fault) → TO-PI; neither is a negative pilot; no rerun (CC-125 X3).
5. **Score and decide** (CPU, `k2_gate0.py score`): untruncate, edit, score both rows, apply the STOP rules.

## 5. STOP conditions (any one fires a STOP)

| | Condition (edit − zero-shot on val 924) |
|---|---|
| (a) | the edit lowers R by > 1.0 |
| (b) | the edit lowers CHAIR_i by < 5.0. PROPOSAL l.100's reason ("matcher error") is struck under W2: v1 ⊂ v2 in rules, so the gate cannot detect matcher error. The v1 = v2 agreement share is reported instead |
| (c) Gate 0b | edited mean words < 90% of zero-shot (W4) |
| (d) | **STOP-only (W1):** the ceiling (CHAIR_i drop) < 2 × SESOI = 6.0, or the bootstrap 95% half-width of ΔCHAIR_i ≥ 3.0, or that of ΔR ≥ 2.0. It can only stop; it never loosens a SESOI |
| (e) W20 | more than half of the CHAIR_i drop comes from negated or hedged mentions: 1 − (drop with unasserted mentions excluded) / (drop) > 0.5 |
| freeze (**NOT RUN, cost → TO-PI**) | no `max_new_tokens` ≤ 1024 cuts < 10%, or the cap exceeds 5 GPU-h |
| cap (**NOT RUN, cost → TO-PI**) | the val decode does not finish inside the cap (exit 124) |

**Two STOP classes (CC-124 W2).** A freeze or cap outcome is a cost artefact: `STOP.md` and `gate0_decide.json` carry `verdict: NOT-RUN`, `class: cost -> TO-PI`; it goes to the PI, is never a negative K2 pilot and never triggers the K1 + K6 fallback below. Only (a)–(e), reached on scored output, are negative pilots.

(d) binds more tightly than (b) whenever (b) alone would pass. Both stay as written.

**On a negative-pilot STOP, (a)–(e) (W8):** `STOP.md` with the measured values. No rerun, no tuned retry, no second look. G1's headline falls back to K1 + K6 (PI-1026u Q4), and the K2 rows become a disclosed negative pilot. **On NOT RUN (cost):** `STOP.md` labelled as such, the PI decides (rent time or stop); nothing is reported as a pilot result. **On GO:** the ceiling exists. That licenses only the drafting of the K2 Gate 1 rule (W9–W13, W19–W23), not a run.

## 6. Reported in `gate0_decide.json` (numbers only)

- Zero-shot and edited CHAIR_i and R.
- The diagnostics: unasserted mentions excluded, negation-blind, and union gold.
- The deltas and their bootstrap half-widths.
- The share of the drop from unasserted mentions, the number of deleted units, and the share of them that are negated or hedged (W20).
- `p1_truncation_frontier` (§6b): verdict, Gap_ceiling with CI, the frontier points, check T, matched-count F1, cap-hit share.
- CC-124 W9 diagnostic: the count of deleted units whose only gold-absent v1 class is a LEX_V2-rewritten dining-table hit (*ghi bàn / bàn thắng / bóng bàn*). The editor stays v1 (CC-119 r4).
- Mean words, Vietnamese-only share, v1 = v2 share (W2), `max_new_tokens`, cap-hit share (W3), wall s/img, peak GPU memory (W8), the freeze record, the decode sha, and the frozen SESOIs.

The label "TARGET CEILING ONLY" is written into the file.

## 6b. Registered secondary analysis P1: the truncation frontier (Ken K14 P1)

**Status.** Registered here, before any output, as a secondary analysis with its own verdict. It runs on CPU over the same val-924 zero-shot decodes and edited targets that Gate 0 produces (data labelled "shared with Gate 0 (W7)"). It changes nothing in Gate 0: not (a)–(e), not the SESOIs, not the cap or the ceiling. Source: `manuscript/ken/K14_PROPOSALS_2026-10-27.md` §P1 (l.65–123). Ken's three motivating sources are cited as he names them: *Less is More*, Fig. 5 (a truncation baseline); the attention-heads paper (recall 0.78 → 0.70); LURE (hallucinations sit late in the caption). **K14 gives no identifier for any of the three**; they go through the non-Ken identifier and claim check (CC-114 W10 pattern) before any paper cites them, and no claim here rests on them.

**Why.** G1 compares K2 with the *uncut* zero-shot at a recall margin of −2.0. A zero-shot caption cut short also loses CHAIR_i as it loses recall. If cutting alone reaches "−3.0 CHAIR_i at −2.0 recall", G1 as written can be met by a trivial baseline. P1 tests this before any K2 GPU time.

**Frontier (fixed now).**
- Each zero-shot caption (post-W3 decode, after `untruncate`) is cut to its first k clauses, k = 1, 2, …, k_max, with exactly the pinned editor's clause splitter (`units`, W5). A caption with fewer than k clauses stays whole, so k = k_max is the uncut set.
- For each k: corpus recall R_k and CHAIR_i,k under the W21 gold and the W20 scorer.
- The frontier is the piecewise-linear curve through (R_k, CHAIR_i,k). Its value at a target recall R* is the linear interpolation between the two k that bracket R*; equal recalls take the first k that reaches R*; outside [R_1, R_max] the end point is used and `frontier_clamped` is set.
- Word-percentage truncation may be reported as a secondary curve. It is never used for the verdict.

**Measures.**
- **Gap_ceiling** = CHAIR_i(frontier at R_edited) − CHAIR_i(edited), where "edited" is the K2 target set, the student's ceiling. Paired image bootstrap (B = 2,000, `default_rng(0)`, the Gate 0 resample), frontier and edited on the same draw; the 95% half-width is reported.
- **Check T:** does any k < k_max satisfy ΔR ≥ −2.0 and ΔCHAIR_i ≤ −3.0 against the uncut zero-shot (point estimates)? That is, does truncation alone meet G1 as written.
- Beside them: R_edited, both CHAIR_i values, the frontier points by k, matched-count F1 of edited and zero-shot (Paper A's matched prefix on the asserted v2 classes, cited as a tool), mean words and the cap-hit share (W3).

**Verdict (pre-fixed; `k2_gate0.p1_frontier`).**
| | |
|---|---|
| **P1-GO** | Gap_ceiling ≥ 6.0 (2 × SESOI, the W1 logic) and half-width < 3.0 |
| **P1-NO-GO** | Gap_ceiling < 6.0. `P1_VERDICT.md` carries: "K2 headline under G1 not safe: ceiling does not clear the truncation frontier by 2×SESOI". Gate 0 itself is not stopped |
| P1-INCONCLUSIVE | Gap_ceiling ≥ 6.0 but half-width ≥ 3.0 (not resolvable on val 924), or the frontier was clamped (R_edited outside [R_1, R_max]: not a same-recall comparison; CC-125) |
| P1-ERROR | P1 raised (CC-125 X1): Gate 0's record is written first and stands; `P1_VERDICT.md` says "P1-ERROR (not run)" |
| **Flag** | if T is true: "G1 comparator must become the frontier", for the judge, whatever the gap |

The verdict and the flag are written to `P1_VERDICT.md` and into `gate0_decide.json` under `p1_truncation_frontier`. One look; no rerun. A P1-NO-GO or a T flag goes to the judge panel together with Gate 0's result; it feeds the K2 Gate 1 rule and the MT4 fixed sequence (Ken proposes H-P1 after H2), and nothing here is a method result.

## 7. Disclosures (W7)

- Val 924 was used before:
  - as B's WiSE-FT gate set;
  - for B's adapter decodes (`data/results/uitviic_ind_val/`);
  - as the G-RL pilot's dev set (`PILOT_RULE.md`).

  All 924 images are COCO train2014, so exposure during pretraining is possible.
- **Shared decodes:** none. G-RL's zero-shot val decode uses Qwen2.5-VL-7B at 160 tokens through `evaluate.py`. This pilot's uses Qwen3-VL-8B at the frozen value through the LB decoder. The settings differ, so neither decode serves the other (CC-119 ruling 8), and each is labelled with its model and settings.
- The editor (v1) and the scorer (v2) share the lexicon. The edit therefore removes exactly the mentions that v1 flags. This is why (b) is a size check, not a validity check (W2).
- Training text policy (PD-GR-2, PI-1026aa Q5 YES): the backbone's own gold-edited captions may be K2 training text, disclosed as training data, never evidence, no MT COCO; no training happens in Gate 0. Nothing here is AI-labelled evidence.

## 8. Planning cost

- Measured anchor: 5.29 s/img at 160 tokens (`step1_dev300_guard.json`, KTVIC dev300 detailed, Qwen3-VL-8B), which gives about 1.36 GPU-h for 924 images at 160.
- At a larger frozen value the probe sets the figure. If the cap would exceed 5 GPU-h, Gate 0 is NOT RUN (cost) at the freeze and goes to the PI. At the all-hit bound: 256 → 2.8, 384 → 4.1, 512 → 5.4, 768 → 8.0 GPU-h (CC-124 l.33); with real slice lengths 256–384 projects to about 2.3–4.1.
- Probe: about 0.1–0.2 GPU-h.

## Amendment (2026-10-28, CC-136 / CC-136P): §6c P2 pilot, gold editor vs detector editor

**Status.** Added on 2026-10-28, after Gate 0's output (18:45Z on 2026-10-27) and before any P2 output. §1–§6b, §7 and §8 above are unchanged: this text is appended, and nothing above it moves. Source: Ken's draft `manuscript/ken/K18_P2_ADDENDUM_DRAFT.md` (sha 5af47b76), which stays non-binding, as revised by the CC-136 single-judge read and by the five-judge panel CC-136P. CC-136P supersedes CC-136 wherever they differ. Code: `scripts/grl/k2_p2_detect.py` (detector, GPU), `scripts/grl/k2_p2.py` (reproduction, editing, scoring, decision, CPU) and `scripts/grl/k2_p2.sh` (the M3 job). The judge code read covers one frozen snapshot of the three files; any later change needs a new read (CC-136P W15).

**What this measures.** Does replacing COCO instance gold with an open-vocabulary detector, in the same pinned editor (§2) on the same Gate 0 decodes, cost enough at the target level to justify testing gold at the student level? It is a dev screen, not a contribution. E_gold is edited with the same gold that scores it, so every number here is a **TARGET CEILING ONLY** and is never a method result (K14 l.150–152).

**Authority.** CC-126 W9 / ruling 4 / Q6 (the screen, its GO rule and the 0.5 GPU-h cap), PI-1026ac Q6 (dev only), UPGRADE_PLAN §6 last row (a missed Ken pilot is dropped, not run in full), CC-132b (M3 order), CC-136 and CC-136P W1–W18.

**Condition (CC-136P W7): met.** Gate 0 GO, fired [], P1-GO (OPS-1028c; `gate0_decide.json` sha 0b6da7e0). P1 check T is false. Gate 0 STOP or NOT RUN would have meant no P2.

### 6c.1 Detector and pins (CC-136P W8)

| Item | Value |
|---|---|
| Model | Grounding DINO-T (Swin-T, "OGC" checkpoint), README Checkpoints row 1: data `O365,GoldG,Cap4M`, COCO box AP "48.4 (zero-shot) / 57.2 (fine-tune)" |
| Paper | Liu et al., *Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection*, ECCV 2024 (LNCS), DOI 10.1007/978-3-031-72970-6_3, arXiv:2303.05499 |
| Code | `IDEA-Research/GroundingDINO` commit `856dde20aee659246248e20734ef9ba5214f5e44` (2024-08-12), Apache-2.0. Cloned at `/root/GroundingDINO`, outside `common.SCAN_ROOTS` (the repo's own asset images would fail the scan). The job asserts a clean checkout of this commit |
| Config | `groundingdino/config/GroundingDINO_SwinT_OGC.py` at that commit (`num_queries` 900, `max_text_len` 256), with `text_encoder_type` set at run time to the local BERT directory below |
| Weights | `groundingdino_swint_ogc.pth`, 693,997,677 bytes, sha256 `3b3ca2563c77c69f651d7bd133e97139c186df06231157a64c507099c52bc799`, from `https://huggingface.co/ShilongLiu/GroundingDINO/resolve/a94c9b567a2a374598f05c584e96798a170c56fb/groundingdino_swint_ogc.pth`. That is the HF LFS oid; the GitHub release asset publishes no digest. Stored at `$NCS_DATA/models/groundingdino-swint-ogc/` |
| Text encoder | `google-bert/bert-base-uncased` @ `86b5e0934494bd15c9632b12f734a8a67f723594`, Apache-2.0. A local copy at `$NCS_DATA/models/bert-base-uncased-86b5e09/` holds exactly five files, each sha-asserted: `model.safetensors` 68d45e23…69d3, `config.json` 7160e155…7d20, `tokenizer.json` ce64fce7…9a98, `tokenizer_config.json` a025160e…bf10, `vocab.txt` 07eced37…38a3 (full values in `k2_p2_detect.FILES`). With no other weight file present, the load is the pinned safetensors. The Hub name is never resolved at run time |
| venv-gd | `/root/venv-gd`, python3.10; torch **2.5.1+cu121** and torchvision **0.20.1+cu121** (download.pytorch.org/whl/cu121, the build already proven on M3), CUDA **12.1**, transformers **4.44.2** (the writer's choice, contemporary with the commit; untested with it, so the smoke run is the test). The rest of GD's `requirements.txt` is resolved by pip. GroundingDINO is installed with `pip install --no-build-isolation -e /root/GroundingDINO`. The MultiScaleDeformableAttention op needs nvcc 12.1 at build time. M3's rebuild record lists build-essential but no CUDA toolkit, so the build installs one. `run()` asserts torch, CUDA and transformers |
| Freeze | the `pip freeze` sha256 of venv-gd is recorded in an OPS line after the build. `k2_p2.sh` requires it as `GD_FREEZE` and asserts it as `k2_gate0.sh` does for venv-lb, and the detector refuses a missing value (None = fault) |
| Offline | `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`. The only network step is `k2_p2_detect.py fetch` (the pinned URLs, sha-asserted in memory, then tmp + os.replace) |
| Run-recorded | venv-gd freeze, s/img, peak GPU memory, prompt token count, load time, MSDA CUDA call count, unexpected checkpoint keys |

### 6c.2 COCO exposure (disclosed; CC-136P W11)

- **COCO instance labels: none, per the authors.** README row 1 gives T's data as `O365,GoldG,Cap4M` and its COCO AP as zero-shot. The paper's ‡ note on non-zero-shot COCO numbers applies to model L, not to T. Appendix B's "We use COCO, O365, and OpenImage(OI) for our model pretrain" describes the model family and is not quoted alone.
- **HF model-card conflict.** The `ShilongLiu/GroundingDINO` card metadata lists `detection-datasets/coco`. That repo also holds checkpoint B, which is trained on COCO (README row 2). Both sources are disclosed, and the conflict is not resolved here.
- **COCO images: possible.** GoldG contains Flickr30k Entities and Visual Genome images (GD appendix B; MDETR, Kamath et al., ICCV 2021, arXiv:2104.12763). VG's images come from the intersection of YFCC100M and MS-COCO (Krishna et al., IJCV 2017, DOI 10.1007/s11263-016-0981-7). All val-924 images are COCO train2014 (§7). GLIP releases a GoldG "without COCO images" (arXiv:2112.03857; `final_mixed_train_no_coco.json`), but the GD paper does not say which GoldG version T used. Cap4M's and O365's image sources were not checked.
- **Direction.** Exposure would favour the detector arm and shrink the gold − detector gap, so it biases toward NO-GO.
- **Struck (CC-136P W11):** the optional count of val-924 ids in VG's `coco_id` metadata. No pinned metadata file exists, and the count would decide nothing.

### 6c.3 Editor, class source and the detection rule (CC-136P W1, W9, W10, W16)

**Editor.** Exactly §2's pinned editor (W5): the `units` splitter, matcher v1 (`score_coco_probe.py` d11db7e1, `coco80_vi.json` 926e0857), the language check (`clean_supervision` 01f17200), the trailing-punctuation rule and `untruncate` (W3). It is imported from `k2_gate0.py` and not copied. **One change only:** the image's presence set is the detector's D(img) ⊆ COCO-80 instead of the gold G(img). A unit is deleted if it names a v1 class outside D(img) or fails the language check.

**Class source (W10).** The 80 names are the pinned `COCO80` tuple in `k2_p2_detect.py`: COCO-2014's instance categories in category-id order, the `category_dict` order of `demo/test_ap_on_coco.py`. They are **not** taken from `gold_instances.json`, which names only 65 distinct classes on these 3,326 ids (Ken's draft l.76 is corrected here). Asserts: gold ⊆ COCO80, and COCO80 equals the class keys of `coco80_vi.json` minus `_note`. Equality with gold is never asserted. The mapping is identity by name, with no class outside COCO-80 and no many-to-one map.

**Prompt.** `" . ".join(COCO80) + " ."`, which equals `test_ap_on_coco.py` l.174 and `build_captions_and_token_span(COCO80, True)[0]`; the job asserts the equality. No name contains "/", so the upstream `random.choice` branch never runs and the prompt is deterministic (asserted). **Token count: 195** of the 256 limit (CPU tokenisation on 2026-10-28 with the pinned `tokenizer.json`, CLS and SEP included). The run asserts ≤ 256 and that all 80 spans have tokens in the positive map; upstream silently drops a span whose `char_to_token` is None.

**Preprocessing.** `demo/inference_on_a_image.py` `load_image` (l.58–70): `RandomResize([800], max_size=1333)`, `ToTensor`, ImageNet `Normalize`. The call is `util/inference.load_image`, which applies the same transform. Batch 1, fp32, `model.eval()`, `torch.no_grad`.

**Rule (W1).** The source is `demo/inference_on_a_image.py` at 856dde2, l.117–133, given-phrase mode:
- `create_positive_map_from_span` gives span-normalised rows (80 × 256);
- `positive_maps @ sigmoid(pred_logits).T` gives an 80 × 900 class × query score;
- class c ∈ D(img) iff some query scores **> 0.30**, the `box_threshold` argparse default at l.162.

The rule caption is the model caption. The demo's tokenisation of its global `text_prompt` is not reproduced. Not used:
- `PostProcessCocoGrounding` (top-300, no threshold, an AP tool);
- `util/inference.predict()`'s max-over-all-tokens rule (0.35 in `predict_with_caption`);
- `get_phrases_from_posmap` and `text_threshold`.

D(img) at 0.35 is written beside it and reported descriptively only, as presence precision and recall; no E_det is built at 0.35.

**Bias, disclosed both ways.** The span mean lowers multi-token classes (*traffic light*, *dining table*, *cell phone*). That adds misses, and a miss deletes the whole unit with its correct mentions, which biases toward a GO through recall. Possible VG image exposure (6c.2) biases toward NO-GO.

**Fault asserts (W9), each NOT RUN (fault):**
- the GD op `_C` imports, and the `MultiScaleDeformableAttnFunction` CUDA path is called (call count > 0 after the first image; a silent pytorch fallback is a fault);
- `load_state_dict` reports `missing_keys == []`, and `unexpected_keys` lie within the pinned named set {`label_enc.weight`, `bert.embeddings.position_ids`}, which the smoke run confirms;
- torch, CUDA, transformers, the weights, the five BERT files, the GD commit and the venv-gd freeze match their pins;
- `k2_gate0.val_ids_ok` passes, and all 924 staged val images match `uitviic_val.tsv`, checked before the GPU pass and again per image.

**Output.** `p2_detect.json`: D at 0.30 and at 0.35 for the 924 ids, the 80 per-class max scores per image (disclosure only, never tuning), and the pins and run figures. It is hashed into `p2_detect.sha256` before E_det is built (W13).

### 6c.4 Data and the reproduction control (CC-136P W3)

- **Scored set:** UIT-ViIC val 924 (`uitviic_val.tsv` 338252e1), under the same guard, `m3_clear`, tmux + RUNNING lock and `EXPECT_HEAD` as §3.
- **Decodes:** Gate 0's own zero-shot val decode (Qwen3-VL-8B @ 0c351dd, `max_new_tokens` 512), shared with Gate 0 (W7). There is no new decode; the only GPU work is the detector.
- **Reproduction control (W3).** E_gold is **recomputed**, not retrieved. The runner first asserts:
  - `gate0_decide.json` sha256 = 0b6da7e083af…17a5;
  - the decode sha256 = 8bb0192c76c1…0c51, as named in that record.

  It then recomputes E_gold with the imported `k2_gate0.untruncate / edit / row / rates`. The recomputed zero-shot and edited rates must equal the record at its 4 decimals, `deleted_units` must equal it, and the record must hold edited CHAIR_i 1.795, R 65.28 and 277 deleted units (OPS-1028c). Any mismatch is NOT RUN (fault), never a look, and the detector record is not opened. Only after this does it build E_det = edit(c, D(img)).
- **Scoring:** gold W21 (`gold_instances.json` 42c100f5), scorer W20 (matcher v2; negated or hedged mentions are hallucinations), pooled CHAIR_i and R as §2.

### 6c.5 Decision rule (fixed by CC-126 W9 before Gate 0; unchanged) and the arm licence (CC-136P W4)

| | Condition (point estimates on val 924) |
|---|---|
| **P2-GO** | CHAIR_i(E_det) − CHAIR_i(E_gold) ≥ **6.0**, **or** R(E_gold) − R(E_det) ≥ **4.0** (2 × SESOI, W1) |
| **P2-NO-GO** | neither. `P2_STOP.md` with the measured values; no rerun, no threshold change, no detector change |
| P2 NOT RUN (cost → TO-PI) | the detector step exceeds its 1,800 s timeout (exit 124). `P2_STOP.md` + `p2_decide.json`, `verdict: NOT-RUN`, `class: cost -> TO-PI`. It is not a negative pilot (CC-124 W2), and it closes the pilot |
| P2 NOT RUN (fault → TO-PI) | a venv/op build or smoke failure, a pin or sha mismatch, a W3 or W9 assert, or any other non-zero exit. `P2_FAULT_<utc>.md` only. It is not a look, and no other detector or HF port is used without a new ruling |

**Arm licence (W4), fixed after Gate 0 and before any P2 output.** `fired_arm` ∈ {chair, recall, both, none}.
- (a) CHAIR arm fired (chair or both): it licenses drafting H-P2 (K14 l.130: gold-student CHAIR_i lower by ≥ 3.0, recall margin −2.0) **only if** Σhal(E_det) > Σhal(E_gold) (`driver: hallucination`). Otherwise the fire is `recall-driven` and licenses H-P2r as a secondary only.
- (b) R arm only: it licenses H-P2r (gold-student R higher by ≥ 2.0, CHAIR_i non-inferior at margin +1.0) as a secondary only.
- (c) Both arms with a hallucination driver: H-P2 is primary and H-P2r secondary.
- **No GO by itself licenses the full P2 run (~39 GPU-h).** That still needs a K2 Gate 1 GO, the MT4 prereg and a fresh cost ruling. The judge decides H-P2's place in the fixed sequence.
- A GO never claims "gold is better". A NO-GO never claims a detector can replace gold; it means only "no licence for a full P2".

**Reachability note (W6; noted after Gate 0, before P2 output; rule unchanged).** CHAIR_i is pooled, Σhal / Σmen (`k2_gate0.py` l.100–110), and `edit` deletes whole units. A detector miss deletes units with correct mentions and shrinks Σmen, while a false positive keeps hallucinated units. CHAIR_i(E_det) is therefore not bounded by the zero-shot 9.375, and the CHAIR arm can fire through recall loss; the driver test above separates the two. R has the fixed denominator Σ|gold| and falls monotonically under deletion. The thresholds were set at CC-126 W9 (2026-10-27T04:59Z), before Gate 0's output (18:45Z). CC-136's "CHAIR arm nearly unreachable / ≤ 9.4" is struck.

**Records (W2, W13)** go to `/root/outputs/grl_pilot/k2/p2/` only: `p2_detect.json` (+ `.sha256`), `smoke_<utc>.json`, `p2_decide.json`, and `P2_VERDICT.md` (GO), `P2_STOP.md` (NO-GO or cost) or `P2_FAULT_<utc>.md`, plus `runs.log`. **`gate0_decide.json` is never written.** The writer refuses that name, and the job asserts its sha before and after.

`p2_decide.json` carries:
- `verdict`, `fired_arm`, `driver`, `licence`;
- E_gold and E_det rates;
- Σhal, Σmen, Σtp and Σ|gold| for both arms, and `correct_mentions_lost` = Σtp(E_gold) − Σtp(E_det);
- both deltas with bootstrap 95% half-widths (B = 2,000, `default_rng(0)`, one draw shared by both arms). They are reported only. If the fired arm's half-width ≥ its SESOI (3.0 / 2.0), the licence text says so;
- deleted units and their negated-or-hedged share per arm, mean words, matched-count F1;
- D presence precision and recall against gold at 0.30 and, descriptively, at 0.35;
- the shas and the detector's run figures;
- the label "TARGET CEILING ONLY".

**One look (W13).** The look is the moment `p2_decide.json` is written. A fault rerun is allowed only before that file exists, and every attempt is logged in `runs.log` and the WORKFLOW_LOG. A `p2_detect.json` that matches its hash from a faulted attempt is reused, with no second GPU pass.

### 6c.6 Cost and run order (CC-136P W5, W12, W18)

- **Speed source:** YOLO-World (Cheng et al., CVPR 2024, DOI 10.1109/CVPR52733.2024.01599, arXiv:2401.17270), Tab. 2: GD-T at 1.5 FPS on one V100 without TensorRT, on LVIS minival. 924 / 1.5 ≈ 616 s ≈ 0.17 GPU-h, plus about 0.05 h for loading and checks, so about **0.22 GPU-h**. The conversion to an RTX 3090 and to an 80-class prompt has no source.
- **Cap:** `timeout 1800` (0.5 GPU-h) on the detector step only (model load + 924 images). Exit 124 is NOT RUN (cost); any other non-zero exit is NOT RUN (fault). Editing, scoring and the bootstrap run on CPU.
- **Order on M3 (W12; replaces the draft's C-EN-priority sentence, W18):**
  1. B-2 CLEANUP DONE;
  2. the W5 commit window;
  3. the gatekeeper commit of §6c, the three scripts and SHA256SUMS;
  4. the M3 HEAD move;
  5. the venv-gd build: one attempt of at most ~1 h, outside the timeout, with the GD clone on M3 only after B-2 cleanup (CC-132 W8) and the freeze then recorded in an OPS line;
  6. `k2_p2.sh` in tmux under `grl_pilot/RUNNING` (noclobber), running selftests, guard + `m3_clear`, `fetch`, the W3 reproduction, the **smoke** on the first 2 staged UT-2402 train images (never val-924; MSDA call count, shas, keys, s/img and peak memory; D not kept; not a look), then guard again, the detector under the cap, and the decision.

  G-RL Gate 0 may run before or after P2, never concurrently with it.
- **Refusals.** `k2_p2.sh` refuses to start if any other `/root/outputs/*/RUNNING` exists, if any other tmux session exists, if `/root/ncs-data/b2_stage` exists, or if a B-2 process is running. Locks are checked on M3 itself, never on the local mirror, and the mirror is never copied back. A build or smoke failure is P2 NOT RUN (fault) → PI.
- **Commit timing (W5).** The commit lands only after `b2_chain` prints CLEANUP DONE and no C-2 or B-1 step pinned to 1ae7339d is pending (`b2_chain.sh` l.27/l.54, `c2_chain.sh` l.43, `b1_chain.sh` l.53). Re-pinning those steps instead is the PI's choice, after a judge diff check. The HEAD checks are never edited, and no machine's HEAD moves while one of its jobs runs.

### 6c.7 Risks and pre-written MT4 sentences (CC-136P W16)

**Risks.**
1. Same-image exposure through VG/GQA (6c.2): it can be disclosed, not fixed, and it biases toward NO-GO.
2. The model-card conflict: answered by README row 1, together with the fact that the HF repo also holds checkpoint B.
3. The threshold choice: the authors use 0.30 (argparse) and 0.35 (README / `predict_with_caption`). 0.30 was fixed before the data; 0.35 is descriptive.
4. The CUDA-op build (R3): a failure is NOT RUN (fault), with no HF port swap.
5. Circularity: E_gold is near-clean by construction, so a target GO says nothing about a student.
6. The finding holds for COCO-80 only.
7. Tokeniser overflow: the measured count is 195 tokens against the 256 limit, and the run asserts it.
8. Val 924 is used again (§7: B's WiSE-FT gate, B's adapter decodes, G-RL dev, Gate 0); this is disclosed (CC-136 R2).

**Sentences.** X, Y, Z, W and V are filled from `p2_decide.json`.
- **GO, CHAIR arm (hallucination-driven):** "On UIT-ViIC val (924 images), editing the same zero-shot Qwen3-VL-8B captions with the same rule, but with Grounding DINO-T detections (box threshold 0.30, the authors' default) in place of COCO instance gold, left CHAIR_i X points higher than gold editing (≥ 6.0, twice the SESOI), with more hallucinated mentions kept. This is a target-level ceiling, not a student result."
- **GO, R arm or recall-driven CHAIR arm:** "… the detector-edited targets lost Y points of object recall (Z correct mentions) relative to gold-edited targets, because detector misses deleted whole clauses. Target-level ceiling only."
- **NO-GO:** "Under the same editor and the same decodes, detector editing differed from gold editing by W CHAIR_i points and V recall points at the target level, below the pre-registered 6.0 / 4.0. It removed a share S = (9.375 − CHAIR_i(E_det)) / (9.375 − 1.795) of the gold-removable CHAIR_i (descriptive). By the pre-registered rule this gives no licence for a student-level gold-versus-detector test, and none was run."
- **NOT RUN (cost):** "The detector pass did not finish within its pre-registered 0.5 GPU-h cap. Per the rule this is a cost outcome, not a negative result, and no comparison is reported."
- **NOT RUN (fault):** "The pinned detector could not be run as registered (reason: …). No substitute detector was tried, and no comparison is reported."
- **Disclosure with every outcome:** "Grounding DINO-T's released training data (O365, GoldG, Cap4M) contains no COCO instance annotations according to its authors, but GoldG includes Visual Genome images, a subset of which are COCO images. We could not rule out that the detector saw our validation images with non-COCO labels; any such exposure favours the detector arm."

### 6c.8 Related work and the novelty claim (CC-136P W17, ruling 1)

- **Cited:** Woodpecker (Yin et al., *Sci. China Inf. Sci.* 2024, DOI 10.1007/s11432-024-4251-x, arXiv:2310.16045; verified in K14_PRIOR_ART l.68). It corrects hallucinations with expert models, Grounding DINO among them, not with gold.
- **Identifiers verified on 2026-10-28 (arXiv titles) by a non-Ken check; claims not yet verified:**
  - SENTINEL, arXiv:2507.12455. Its abstract confirms an object cross-check "with two open-vocabulary detectors"; the detector names are not checked.
  - CHAIR-DPO, arXiv:2508.20181 ("Object-aware Preference Optimization"). The DETR-as-truth claim is not checked.
  - MARINE, arXiv:2402.08680. The "MARINE-Truth" oracle claim is not checked.
  - ViGoR, arXiv:2402.06118.
  - POPE, arXiv:2305.10355.

  None of these five is cited for a detector-versus-gold claim until that claim is checked against the paper text.
- **Narrowed novelty.** Prior work already uses detector truth in place of gold. P2 claims no novelty for that. What it may claim is a controlled comparison: the same decodes, the same deterministic editor, gold versus detector as the only change, toward a student-level effect, in Vietnamese. The value is application, answering "why human gold when a detector is free?". Ken's K14 l.131 sentence is not used.

### 6c.9 Questions in the draft, resolved

1. Does P1-ERROR block P2? Moot: the condition is met (P1-GO; W7).
2. Threshold 0.30 or 0.35? 0.30 (argparse default, l.162); 0.35 is descriptive only.
3. Is there a half-width conjunct on GO? No. Gate 0's output has been seen, so any change now would be post hoc; the half-widths are reported only (W4).
4. Is the VG `coco_id` count run? No, it is struck (W11).
