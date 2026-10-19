# MODELS v2: open VLMs for the LB leaderboards (A-N2, B-N1), revised per PD-17

Built 2026-10-19T03:12:44Z by `build_lb_v2.py` from the Hugging Face Hub metadata in `hf_api/` (model info, file tree at the revision, chat template; generic User-Agent, no token, >= 3.5 s between requests; no weights downloaded). Revision = the main-branch commit on the fetch date, except Qwen3-VL-8B, pinned to the G2-B revision (its LFS hashes equal G2-B's SHA256SUMS entries; checked).

VRAM: weights at the load dtype (parameters x 2 bytes); activations for the registered batch come on top and are not measured here (no GPU used); 'fits' = weights <= 20 GB of the 24 GB RTX 3090. Vietnamese: a template that inserts the user text unfiltered (checked in code on each fetched template) accepts a Vietnamese prompt; whether the language model is documented for Vietnamese is the B-N1 rule.

| Key | Repo | Revision | Open-weights licence | Params | VRAM weights GB (dtype) | Gated | Remote code | Chat template | Vietnamese documented | Used in |
|---|---|---|---|---|---|---|---|---|---|---|
| llava15_7b | `llava-hf/llava-1.5-7b-hf` | `b234b804b114d9e37bb655e11cbbb5f5e971b7a9` | llama2 | 7,063,427,072 | 14.13 (float16); fits: True | False | no | inserts the user text unfiltered | no: card languages ['en'] | A |
| llava_ov_7b | `llava-hf/llava-onevision-qwen2-7b-ov-hf` | `0d50680527681998e456c7b78950205bedd8a068` | apache-2.0 | 8,030,807,584 | 16.06 (float16); fits: True | False | no | inserts the user text unfiltered | no: 'Vietnamese' not in hf_api/readme_Qwen__Qwen2-7B-Instruct.md | A |
| qwen25vl_3b | `Qwen/Qwen2.5-VL-3B-Instruct` | `66285546d2b821cf421d4f5eb2576359d3770cd3` | qwen-research | 3,754,622,976 | 7.51 (bfloat16); fits: True | False | no | inserts the user text unfiltered; adds 'You are a helpful assistant.' | yes: hf_api/readme_Qwen__Qwen2.5-7B-Instruct.md ('Vietnamese') | A B |
| qwen25vl_7b | `Qwen/Qwen2.5-VL-7B-Instruct` | `cc594898137f460bfe9f0759e9844b3ce807cfb5` | apache-2.0 | 8,292,166,656 | 16.58 (bfloat16); fits: True | False | no | inserts the user text unfiltered; adds 'You are a helpful assistant.' | yes: hf_api/readme_Qwen__Qwen2.5-7B-Instruct.md ('Vietnamese') | A B |
| qwen3vl_8b | `Qwen/Qwen3-VL-8B-Instruct` | `0c351dd01ed87e9c1b53cbc748cba10e6187ff3b` | apache-2.0 | 8,767,123,696 | 17.53 (bfloat16); fits: True | False | no | inserts the user text unfiltered | yes: hf_api/readme_Qwen__Qwen3-8B.md ('100+ languages') | A B |
| internvl3_8b | `OpenGVLab/InternVL3-8B-hf` | `259a3b64a14623c0ec91a045cb43f7c5af5fa6af` | qwen | 7,944,373,760 | 15.89 (bfloat16); fits: True | False | no | inserts the user text unfiltered | yes: hf_api/readme_Qwen__Qwen2.5-7B-Instruct.md ('Vietnamese') | A B |
| idefics3_8b | `HuggingFaceM4/Idefics3-8B-Llama3` | `fddb4ff79181e55a994674777e06cd5456ce3dc3` | apache-2.0 | 8,462,086,384 | 16.92 (bfloat16); fits: True | False | no | inserts the user text unfiltered | no: card languages ['en'] | A |
| smolvlm2_2b | `HuggingFaceTB/SmolVLM2-2.2B-Instruct` | `482adb537c021c86670beed01cd58990d01e72e4` | apache-2.0 | 2,246,784,880 | 4.49 (bfloat16); fits: True | False | no | inserts the user text unfiltered | no: card languages ['en'] | A |

Excluded (licence, gating and remote code from `hf_api/<repo>.info.json`):

| Repo | Revision | Licence | Params | Gated | Remote code | Why |
|---|---|---|---|---|---|---|
| `google/gemma-3-4b-it` | `093f9f388b31de276ce2de164bdc2081324b9767` | gemma | 4,300,079,472 | manual | no | gated (manual): no tokens or credentials on rented machines (PD-17 J5) |
| `5CD-AI/Vintern-1B-v3_5` | `b98f263eab246eb5269ade64edbdca8a887dc44d` | mit | 938,193,024 | False | yes | scope: its remote code (config auto_map -> InternVLChatModel) lies outside the one audited HF-native decoder, decode_hf_vlm.py, that every model runs through (PD-17 J4). Safety is not the reason: S2 already runs pinned remote code (CC-030) |
| `Vi-VLM/Vistral-V-7B` | `6c8313eb59048d33799a651a8d9437ee376f92b9` | apache-2.0 | 7,406,768,384 | auto | no | not loadable by transformers alone (LlavaVistralForCausalLM is neither a transformers class nor in the repo); gated (auto) |
| `llava-hf/llava-1.5-13b-hf` | `5dda2880bda009266dda7c4baff660b95ca64540` | llama2 | 13,351,494,656 | False | no | VRAM: its parameters x 2 bytes (fp16) exceed one 24 GB RTX 3090 |
| `openbmb/MiniCPM-V-2_6` | `6c04d9e3022bcff6e6738dfb1fc19a5cfd2a855f` | not in card metadata | 8,099,175,152 | auto | yes | remote code (auto_map -> MiniCPMV); gated (auto) |

B-N1 replacement rule for Gemma-3 (PD-17 J5): applied at drafting time to the fixed candidate list; no candidate qualifies (table in the B-N1 prereg, Section 4), so B-N1 has 4 models.

Notes: every model used is open weights, ungated, under the licence its card states (column 4); Qwen2.5-VL-3B carries the Qwen research licence and InternVL3-8B-hf the Qwen licence of its language model. SmolVLM2's processor needs num2words, the only package added to the G2-B venv. No token or credential is needed on the machines.
