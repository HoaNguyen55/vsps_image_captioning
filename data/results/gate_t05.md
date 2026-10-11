# Gate T0.5 — single-pass logit verifier vs K=5 self-consistency (RTX 3090, 2026-10-11)

`python scripts/gate_t05.py --in <stage1> --n 600 --out data/results/gate_t05.json` (600 random stored probes, Vintern-1B-v3_5).

| prompt | agreement with K=5 majority | κ vs K=5 | s / probe |
|---|---|---|---|
| Stage-1 prompt (with "Chỉ trả lời 'có' hoặc 'không'") | 90.7% | 0.794 | 0.41 |
| bare question (`--raw-prompt`) | 78.2% | 0.531 | 0.43 |

The stored `answer` is the K=5 majority (`VLM.probe`, T=0.7), not a greedy answer, so G1 ("≥98% vs greedy") cannot be measured from saved records; κ is the meaningful gate and passes (≥0.7). Agreement by K=5 vote margin (Stage-1 prompt):

| K=5 vote | n | agreement |
|---|---|---|
| 5/5 | 445 | 97.8% |
| 4/5 | 89 | 84.3% |
| 3/5 | 66 | 51.5% |

The logit pass agrees where self-consistency is confident; disagreement is concentrated where the K=5 majority itself is close to a coin flip. One pass instead of five samples per probe.
