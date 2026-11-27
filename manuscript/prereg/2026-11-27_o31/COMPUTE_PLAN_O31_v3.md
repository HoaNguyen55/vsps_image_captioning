# COMPUTE PLAN O31 (one 24 GB RTX 3090)

Status: v3 after CC-501r2 (R2-B2: rented host per PI-1127h; no O31 work on the PI's PC). v2 = 941c0bcf, v1 = 1fcbbf7d. Nothing is rented and nothing has run.
**Hardware:** a rented host with one RTX 3090, 4090 or 5090 (PI-1126b), rented when the live balance allows (PI-1127h; warn at 50,000 VND, PI-1126f) and after the C-CONF host is paid for. Not the PI's PC. All GPU-h and caps below are 3090 planning values; on a faster card they stay as written.
**Custody:** under PI-1111j, CPU replays and scoring run on the GPU host (host), not on the laptop. Tier-3 gold stays where the tier-3 ruling names. On host, work only under `~/vsps_host/o31/`.

**Speed anchors.** All are measured on a 4090 and scaled ×1.4 to a 3090. The factor 1.4 is an assumption; the first smoke test of each job replaces it.

| Item | 4090 measured | Source | 3090 planning value |
|---|---|---|---|
| Stage-1 (generator + Vintern K = 5), per image | 80 s median | FAIR v10 §IV-B | 112 s |
| Vintern-1B single probe | 0.05 s | LOG OPS-1031e1bcaprisk | 0.07 s |
| InternVL3-8B single probe (FA, 1,845 tokens median, no image-prefix reuse) | 0.338 s mean, 0.263 median | `.session_backup/2026-11-02/e2b_rate/rate.json` | 0.47 s |
| Qwen3-VL-8B single probe | 0.081 s | same file | 0.11 s |
| QLoRA SFT, 7.2k rows × 2 epochs | – | 3.6 h on a 3090 (VSPS-J program, Q1_GAP) | 3.6 h (S1); about 4.3 h for S2's longer targets at equal steps |
| Detailed decode, batch 1, greedy | – | 0.5 h per 558 images on a 3090 | 3.2 s per image |

**Probe count.** The E1b log holds 345,768 (image, question) pairs over 3,700 images, both query polarities. The affirmative half is about 173k. With the 69 new images, the planning figure is about **176k probes**.

## 1. Steps, in order

| Step | What | Where | GPU-h (3090) | Cap | Gate before it |
|---|---|---|---|---|---|
| **P0** | Write the O31 code: replay, supervision build with scaled budget, K0 scorer, self-tests and mutants on synthetic data | host CPU | 0 | – | none (code only) |
| **P0r** | K0 replay, Vintern-only grid (10 points), reusing the recorded E1b logits | host CPU, ~2 h | 0 | 3 h CPU | prereg commit + code read |
| **G1** | Stage-1 for the 69 KTVIC-train images without records (FAIR generator settings) + Vintern single-probe logits for them | host | 2.2 | 3.5 | prereg commit + code read |
| **G2** | InternVL3-8B single-probe pass on 3,767 images (~176k probes) | host | 23 (17 if the 0.263 s median holds) | 30 | same |
| **P1** | K0 on the full 30-point grid with both families; choose OP\*, OP_mid | host CPU | 0 | 3 h CPU | G1, G2 done |
| **G3** | **Dev pilot:** SFT S1 (retrain, seed 42), S2 at OP\*, S2 at OP_mid; decode S0, S1, S2 ×2 on KTVIC test 558 + UIT-ViIC 231 | host | 12 + 2.8 ≈ 15 | 20 | K0 PASS (else stop) |
| G4 | Ablations A-2, A-3, A-4 (SFT + dev decodes) | host | 3 × 4.3 + 2 ≈ 15 | 20 | G3 read (K1 not fired) |
| G5 | A-5: S3, verifier at inference, on 789 dev images (stage-1 + O31 probes) | host | 25 | 32 | G3 read |
| G6 | A-6: D2 arm (optional, Q5) | host | 5 | 7 | PI line |
| G7 | Seeds 43, 44 for S1 and S2 | host | 4 × 4 ≈ 16 | 20 | tier-1 freeze commit |
| **T2** | Tier 2 on Karpathy test 5,000: decode S0 + S1 ×3 + S2 ×3, in Vietnamese and in English (7 × 2 × 4.5 h); V-COCO probes on S0 mentions (~25k probes, 2 families) | host | 63 + 4 ≈ 67 | 80 | tier-2 prereg amendment read; W25 overlap pass |
| T2v / T3v | V_FAIR comparator for H4: FAIR's rule is Vintern-1B with K = 5 **sampled dual** queries (Q⁺ and Q⁻), i.e. about 10 generations per proposition instead of 1 probe; ~25k / ~21k propositions × 10 × ~0.1 s (sampled short answers, 3090) | host | ~7 + ~6 | 10 / 8 | with T2 / T3 |
| **T3** | Tier 3 on KV-4,224: the same decodes (7 × 2 × 3.8 h) + V-COCO | host or the host the ruling names | 53 + 3 ≈ 56 | 65 | P(PASS) ≥ 0.98; IRREVERSIBLE panel; PI reassignment (Q1) |

**Totals at batch 1:**
- without the optional arms: about **G1 2 + G2 23 + G3 15 + G4 15 + G7 16 + T2 67 + T3 56 + V_FAIR 13 ≈ 210 GPU-h**;
- with A-5 and A-6: about 240 GPU-h.

That is roughly 8–10 days of continuous running on one 3090.

**Batched greedy decoding** (batch 8, left padding, fixed in the run doc) would cut the decode-heavy T2 and T3 rows by about 2.5×. That brings the total to about 135–145 GPU-h. Use it only if a parity check passes on 50 dev images (bit-equal or token-equal captions at batch 1 vs batch 8). Otherwise stay at batch 1.

**Daily rhythm (PI-1126e):** GPU jobs G1, G2, G3 and so on run at night on host. CPU reads and judge reads happen in the morning.

## 2. Models, memory, settings
- **Student and generator:** Qwen2.5-VL-7B-Instruct.
  - QLoRA, as in FAIR: NF4 with double quantisation and bf16 compute; LoRA r = 16, α = 32, dropout as in FAIR's config; learning rate 1e-4; batch 1 with gradient accumulation 8; 512 visual tokens; transformers 4.51.3; equal optimiser steps (prereg §2).
  - Peak VRAM about 14–18 GB on 24 GB. Gradient checkpointing is on, as in FAIR's config.
- **Verifiers in inference only, bf16, one model resident at a time:**
  - InternVL3-8B: peak 16.0 GB measured (E2b);
  - Vintern-1B: under 4 GB;
  - Qwen3-VL-8B (optional): 16.6 GB.
- **Why not plain LoRA in bf16:** a 7B model in bf16 needs about 15 GB for weights plus activations. That does not leave safe room at 512 visual tokens on 24 GB. QLoRA stays.

## 3. Disk (host, under ~/vsps_host/o31/)

| Item | Size |
|---|---|
| Qwen2.5-VL-7B-Instruct | about 16.6 GB |
| InternVL3-8B | about 16 GB |
| Vintern-1B-v3_5 | about 2 GB |
| (optional) Qwen3-VL-8B | about 17 GB |
| Python venvs (training + probe; pinned freezes) | about 15 GB |
| KTVIC images (train + test) | about 1.5 GB |
| COCO images: UIT-ViIC 231 + Karpathy test 5,000 + KV-4,224 | about 1.6 GB |
| Stage-1 records tarball (b312de68) + new 69 | about 1 GB |
| E1b Vintern probe log + G2 probe log | about 1 GB |
| Adapters, about 0.2 GB each × about 15 | about 3 GB |
| Decodes + scores (ids and counts only leave the host) | under 1 GB |
| **Total** | **about 75–80 GB** |

## 4. What can start first (small development pilot)
1. **Now, with no gate:** P0, the code and its self-tests on synthetic data.
2. **After the prereg commit (and a code read; CC-501 ruling 6):**
   - P0r (CPU, 0 GPU-h). The E1b sweep's Vintern-only maximum (R 44.7) is at the pre-neutralization `supported` stage, so it does not predict K0 at its post-neutralization `sft_caption` stage; P0r's outcome is unmeasured (N6). G2 stays on the critical path regardless, because the two-family grid needs it.
   - G1 + G2 the same night on host: about 25 GPU-h, cap 33.5. They touch only training images.
3. **Then:** P1 (CPU), and, if K0 PASSes, G3, the dev pilot of about 15 GPU-h. G3 answers the RQ8 dev question on KTVIC test and UIT-ViIC 231 within about 2 nights of the prereg commit.

## 5. Host checks carried from earlier lines
- **Bundles and pins:** the system-package bundle (PI-1115r) and pinned freezes; every model is loaded offline by revision and per-file sha.
- **Probes:** a CPU load probe of every model before the first GPU call, and the smoke rule on yes/no mass ≥ 0.5.
- **JVM:** VnCoreNLP runs in a CUDA-free process. A whitespace fallback is a FAULT.
- **Running jobs:** one OUT folder per job and per block; STOP markers are never resumed without a ruling; caps are counted from the launch.json t0.
- **After a job:** the rented host is handled under the clean-host rule (PI-1115s).
