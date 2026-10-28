# W22-SFT memory probe: QLoRA NF4 SFT of Qwen3-VL-8B at 512-token targets on one 24 GB GPU

**Status:** rule written 2026-10-28, before any W22-SFT output. Binding once the gatekeeper commits it, after the judge read of this rule and `scripts/w22_sft/`.

**Sources:**
- CC-148 W2 (this amendment), W3 (arm configuration), W7 (decode identity), W11 (caps) and W12 (machines).
- PI-1026av: the 7B fallback is pre-authorised (CC-148 Q3). PI-1026ax (LOG, 2026-10-28, PI verbatim "M3 vẫn đang giữ, đẩy nhanh tiến độ"; corrects OPS-1028r) keeps M3 rented while M4 runs B-1, so this train-images-only probe runs on M3 (placement on M3: CC-150a, under PI-1026ax).

**Supersedes:** Ken's K19 draft (`manuscript/ken/K19_W22_PROBE_DRAFT.md`) for the SFT case only. K19's on-policy G-RL probe (k = 8, 384 tokens) stays a separate, unratified document.

**Label:** PROBE / DEV. It is an engineering measurement only:
- no hypothesis, no caption, no score and no paper number;
- no adapter is saved.

## 1. Question

Does QLoRA NF4 SFT of Qwen3-VL-8B-Instruct @ `0c351dd01ed87e9c1b53cbc748cba10e6187ff3b`, in the Gate 1 configuration with 512-token targets and micro-batch 1, meet both of these on one RTX 3090?
- peak `torch.cuda.max_memory_reserved()` ≤ **23,500,000,000 B** (GB pinned to 1e9, compared as integers);
- K2 Gate 1 dev projected at ≤ **20 GPU-h** (§4).

## 2. Configuration (pinned in `w22_sft.py`; the Gate 1 trainer reuses `load()` verbatim)

| Item | Value |
|---|---|
| Model | the M3 snapshot `/root/ncs-data/models/Qwen3-VL-8B-Instruct-0c351dd`, with all 14 files checked against the B-N1 pins (sha 9ff02dc2) before any GPU step |
| Quantisation | 4-bit NF4, double quant, bf16 compute, sdpa attention. `prepare_model_for_kbit_training` is **not** called, because it turns checkpointing on by default and upcasts the untied embed and lm_head to fp32. `pixel_values` are cast to bf16 |
| LoRA | seed 0, r 16, α 32, dropout 0, language tower only (`^(?!.*visual)` over q, k, v, o, gate, up and down). Asserted at 43,646,976 trainable parameters (36 × 1,212,416) |
| Optimiser | torch AdamW, lr 1e-4, weight decay 0. 8 micro-batches of 1 per optimiser step (`sft_examples_per_step`) |
| Loss | `labels=` path of the model's forward, with −100 over the prompt, `use_cache=False` |
| Processor | B-N1 `processor_kwargs` (min_pixels 262,144, max_pixels 1,048,576): the teacher path of the K2 targets |
| Prompt | `scripts/evaluate.py` PROMPTS["detailed"], read from the file and asserted at sha 0addb5dd |
| Allocator | `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` |
| C1 | no gradient checkpointing |
| C2 (fallback, one retry) | C1 plus `gradient_checkpointing_enable(use_reentrant=False)` and `enable_input_require_grads()`. Runs only after a C1 memory failure |

**Targets.**
- The targets are synthetic token ids: n − 1 ordinary ids from fixed arithmetic (`1000 + 7919·k mod 140000`, all below the special range starting at 151,643), followed by `<|im_end|>`.
- Long targets have n = 512 label positions, `<|im_end|>` included.
- Memory depends on length, not content. No caption text from any dataset copy is read or built, and targets are never decoded or printed.

**KV-cache API.** K19 §5 found that `rl_policy.py` relies on a cache attribute that transformers 4.56+ removed. That code path is on-policy only: it clones the prompt cache for k samples. SFT runs one teacher-forced forward with `use_cache=False` and builds no cache object, so the removal cannot reach this probe. The selftest asserts that `w22_sft.py` names neither that API nor `rl_policy` / `train_stage2`.

## 3. Data and steps

Images: **UIT-ViIC train only.**
- Ids 1–40 are the first 40 lines of the pinned, ascending `manuscript/prereg/2026-10-27_grl_pilot/ut2402.txt` (sha 3969bfd4). The first five are 368, 419, 431, 488 and 531.
- Image 41 is the worst case: the UT-2402 image with the largest w × h from its PIL header, ties broken by the lowest id.
- Every id is asserted to lie in UT-2402 and outside val-924. Every image is sha-checked against the staged `images.sha256`.
- No release json, no val image and no test image is opened. The `common.py guard` test-image scan still hashes staged files for its refusal check, as in every G-RL job.
- If the images are not staged, the job stops with a FAULT. It never calls `common.stage`, which would also stage val-924.

Steps, in one process per config:
1. Load and attach LoRA.
2. Ids 1–40 with 512-token targets: 5 optimiser steps of 8.
3. Id 41 with a 512-token target: 1 optimiser step of 1.
4. Ids 1–16 with **64-token** targets: 2 optimiser steps of 8, which give the SFT-ref rate (§4).

What is measured, all in integer bytes:
- `max_memory_reserved`, reset before load and before each forward, backward and optimiser step, kept as the per-phase maximum.
- **Peak** is the maximum over all phases, load included.
- `mem_get_info` at the end, reported beside the peak (it includes the CUDA context).

Time:
- **s_ex_512** = mean synchronised wall seconds per example over examples 9–40 (optimiser steps 2–5, optimiser time included). It is also reported × 8 as seconds per optimiser step.
- **s_ex_64** = the same over the 16 short examples.

Also recorded per example: `image_grid_thw`, sequence length and a finite-loss flag.

## 4. Projection (Gate 1 dev GPU-h, CC-148 W3/W4/W11)

dev_h = [(2,402 + 5 × 924) × 3.24 + 2,402 × 0.209 + 3 × 2 × 2,402 × s_ex_512 + 2 × 12,012 × s_ex_64] / 3600 + 11 × 0.1

| Term | Count | Source |
|---|---|---|
| Teacher decode | UT-2,402 zero-shot, one decode that feeds all three edited/unedited target sets | CC-148 l.29 anchor of 3.24 s/img at 512 tokens |
| Detector pass | GD-T presence sets on the 2,402 training images, for the detector-edited targets (P2 ran on val 924 only) | P2 measured 0.209 s/img (OPS-1028i-op, WORKFLOW_LOG l.1811) |
| Val decodes | 5 × 924: the base in student precision (W7), SFT-unedited, K2 gold-edited, K2 detector-edited and SFT-ref | W3, W7; same anchor |
| Edited-target arms | 3 arms (SFT-unedited, K2 gold-edited, K2 detector-edited) × 2 epochs × 2,402 at the 512-token rate, an upper bound since real targets are ≤ 512 | W3, W4 |
| SFT-ref | 2 epochs × 12,012 one-sentence references at the 64-token rate | PILOT_RULE l.40, l.81 |
| Loads | 11 × 0.1 h (1 teacher, 1 detector, 4 training, 5 decode) | K2 Gate 0 `load_hours` |

The training-only hours are reported beside dev_h but do not gate.

**Assumptions and judge items.**
- **W4 default.** The projection assumes 2 epochs, the last checkpoint and no grid. If the Gate 1 rule adopts J1's grid instead, the extra per-epoch val decodes need a re-projection.
- **What is gated.** The whole Gate 1 dev stage is gated, decodes included. That is the plain reading of W2 ("Gate 1 dev projected"), and W11 has no other line for the decodes. With about 7.6 h fixed, the PASS line falls at about 2.1–2.8 s per 512-token example (s_ex_64 from 0.6 down to 0.2 s), depending on s_ex_64. **Judge item:** confirm this reading before the commit.
- **W11 stage caps.** Stage caps are ceil(1.2 × projection), so a dev_h above about 16.7 gives a stage cap above the 20 GPU-h interim line. That case goes TO-PI and does not change the W22 verdict.

**Flag (does not gate).** W7 decodes run on 4-bit + PEFT and are probably slower than the bf16 anchor. The Gate 1 rule re-prices them from its own measured rate.

## 5. Verdict (first match wins; `w22_sft.py verdict`, selftested)

| Condition | Result |
|---|---|
| install, freeze, pip check, snapshot, guard, import check or plan fails, or any crash that is not OOM | **FAULT** (§6) |
| C1: OOM, or peak > 23,500,000,000 B | run **C2** |
| C2: OOM, or peak > 23,500,000,000 B | **FAIL (memory)**: the 7B self-distillation route |
| the config that met memory projects dev_h > 20 | **FAIL (speed)**: the 7B self-distillation route; C2 is not tried after a speed failure, since checkpointing only slows it |
| the cap ends a config that has not failed memory | **NOT-RUN (cost) → TO-PI**. Not evidence about feasibility |
| otherwise | **PASS (C1 or C2)**. The Gate 1 trainer uses that config verbatim |

**7B route** (PI Q3, pre-authorised by PI-1026av): Qwen2.5-VL-7B self-distillation with a fresh 7B Gate 0 and P1 under a rule v2. **A 7B student on 8B targets is never allowed.**

A PASS does not authorise Gate 1. Gate 1 stays HELD until K2_GATE1_RULE and the MT4 PREREG are committed (CC-148 ruling 1).

## 6. Cap, faults, one look

- **Cap.** 0.75 GPU-h = 2,700 s over every GPU process, faulted ones included.
  - The ledger is `/root/outputs/w22_sft/gpu_seconds.tsv`.
  - Each config runs under `timeout` set to 2,700 s minus the ledger total; exit 124 = NOT-RUN (cost).
  - The venv build, the snapshot hash and the selftest are CPU work and fall outside the cap.
- **FAULT.** The job writes `W22_FAULT_<utc>.md` and a `runs.log` line. A rerun is allowed after the fix. It counts against the same cap and may not change §2–§4. A code fix gets a judge re-read before the rerun. A config record that finished cleanly and matches its `.sha256` is reused on a rerun without another GPU step.
- **One look.** The job refuses to start if `w22_decide.json` exists.

## 7. Machine and guards (`scripts/w22_sft/w22_sft_job.sh`)

The probe runs on M3 (CC-150a under PI-1026ax; M4 is busy with B-1), using the cached 0c351dd snapshot. A's N9 keeps priority, and the probe never runs concurrently with N9 or any other job. The job refuses to start:
- outside tmux;
- if more than one tmux session exists;
- if any `/root/outputs/*/RUNNING` lock exists;
- while `/root/ncs-data/b2_stage` exists.

The job then:
- holds `/root/outputs/w22_sft/RUNNING` (noclobber, removed on exit);
- runs `common.py guard <EXPECT_HEAD>` (host, idle GPU, committed clean HEAD, C-EN clear, test-image scan) before the import check and before each config.

**Import check first.** Before any training step, `w22_sft.py imports` runs inside venv-q3 and checks:
- it imports torch, transformers (AutoConfig, AutoProcessor, AutoModelForImageTextToText, BitsAndBytesConfig, Qwen3VLForConditionalGeneration), peft (LoraConfig, get_peft_model), bitsandbytes, accelerate, numpy and PIL;
- the versions of the five pinned packages match;
- an NF4 round trip of a 64 × 64 tensor on the GPU passes (proving bnb's CUDA library is loaded, not the CPU stub);
- the snapshot config and processor load offline, and `model_type` is `qwen3_vl`.

Exit 3 means a clean FAULT, with no training step run.

## 8. venv-q3 (`scripts/w22_sft/venv_q3_freeze.txt`, sha 2bb7397e)

venv-q3 is venv-lb's freeze (685ffe2a; torch 2.5.1+cu121, transformers 4.57.6, accelerate 1.15.0) plus two lines: `bitsandbytes==0.50.2` and `peft==0.21.2`. The two pins add no package that venv-lb lacks. The same pair already runs on torch 2.5.1+cu121 in M3's `.venv` (7332d343).

Build steps:
1. Build once with `python3.10 -m venv /root/venv-q3`.
2. Run `pip install --no-deps -r venv_q3_freeze.txt`, with the cu121 index first and PyPI as the extra index.
3. Write the `.built` marker.

On every run the job checks that the `pip freeze` sha equals the file's sha and that `pip check` is clean.

| Package | Pin | Index entry |
|---|---|---|
| torch | 2.5.1+cu121, cp310 wheel sha256 92af92c569de5da937dd1afb45ecfdd598ec1254cf2e49e3d698cb24d71aae14 | https://download.pytorch.org/whl/cu121/torch/ |
| torchvision | 0.20.1+cu121, cp310 wheel sha256 304937b82c933d5155bd04d771f4b187273f67a76050bb4276b521f7e9b4c4e7 | https://download.pytorch.org/whl/cu121/torchvision/ |
| transformers | 4.57.6 (2026-01-16), wheel sha256 4c9e9de11333ddfe5114bc872c9f370509198acf0b87a832a0ab9458e2bd0550 | https://pypi.org/project/transformers/4.57.6/ |
| peft | 0.21.2 (2026-10-01), requires_python ≥ 3.10, wheel sha256 106ab6077ff72c54d21577f9af5970e34bac7582cb14209f7b2b511e322a4eae | https://pypi.org/project/peft/0.21.2/ |
| bitsandbytes | 0.50.2 (2026-08-27), torch < 3, ≥ 2.4; manylinux_2_24_x86_64 wheel sha256 55348a9a4a21bfd99cf8c7b32fe67b4030ae5c2a05738e03c1747f65fa6ec283 | https://pypi.org/project/bitsandbytes/0.50.2/ |
| accelerate | 1.15.0 (2026-09-09), as in venv-lb | https://pypi.org/project/accelerate/1.15.0/ |

## 9. Report sentences (written in advance)

- **PASS:** "A pre-registered probe found that 4-bit QLoRA SFT of Qwen3-VL-8B-Instruct at 512-token targets (micro-batch 1, [without / with] gradient checkpointing) peaks at X × 10⁹ B reserved on one 24 GB GPU (limit 23.5 × 10⁹), at Y s per example, which projects Z GPU-h for the Gate 1 development stage (limit 20). Decode hours are anchored at 3.24 s/img (bf16), not measured."
- **FAIL (memory):** "A pre-registered probe found that 4-bit QLoRA SFT of Qwen3-VL-8B at 512-token targets exceeds 23.5 × 10⁹ B on one 24 GB GPU even with gradient checkpointing, so K2 uses Qwen2.5-VL-7B self-distillation with its own Gate 0; no 7B student was trained on 8B outputs."
- **FAIL (speed):** "A pre-registered probe found that 4-bit QLoRA SFT of Qwen3-VL-8B fits in memory (peak X × 10⁹ B) but projects Z GPU-h for the Gate 1 development stage, above the 20 GPU-h limit, so K2 uses Qwen2.5-VL-7B self-distillation with its own Gate 0; no 7B student was trained on 8B outputs. Decode hours are anchored at 3.24 s/img (bf16), not measured."
- **NOT-RUN (cost):** "The probe did not finish within its 0.75 GPU-h cap; this is a cost outcome, not evidence about feasibility, and the backbone choice went to the PI."
- **Every outcome:** "The probe used 41 UIT-ViIC training images and synthetic token-id targets; it read no caption, scored nothing and kept no adapter. Seconds per example exclude CPU preprocessing."
