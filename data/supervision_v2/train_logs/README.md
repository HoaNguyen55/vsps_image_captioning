# Training logs (seed 42, RTX 3090 24 GB)

QLoRA SFT of Qwen2.5-VL-7B, `make`-equivalent command in ../README.md. Wall time from the tqdm bar of run_v2.log:

| run | steps | wall time |
|---|---|---|
| v2raw_s42 | 1,800 | 3 h 36 m |
| v2clean_s42 | 1,778 | 3 h 33 m |

`*.metrics.jsonl`: loss / grad-norm / LR every 10 steps (TRL log).
