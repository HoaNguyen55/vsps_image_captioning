# Supervision v2 (built 2026-10-10, not yet trained)

Built from the shipped Stage-1 records (after person_uncap) with the fixed renderer (`rescap/pipeline/realize.py`: entities beyond the topic-shift cap are listed, length drops keep unique objects) and the clean-props rehoming fix (`scripts/build_dpo_data.py`):

    python3 scripts/build_dpo_data.py --in <stage1_neutral> --out data/supervision_v2/raw \
        --seed 42 --min-supported 1 --budget 9 --detailed-variant B --style-variation --clean-props
    python3 scripts/clean_supervision.py --in data/supervision_v2/raw/sft.jsonl --out data/supervision_v2/clean --suffix ''

Template rendering only: the 630 constrained-LM rows of the shipped store are not included.

Detailed captions vs KTVIC train references (3,560 images; precision is a lower bound because references are short):

| store | P | R | R (gendered → người) |
|---|---|---|---|
| shipped data/supervision/sft.jsonl | 42.3 | 38.0 | 49.4 |
| v2 raw (7,206 rows: 3,617 short + 3,589 detailed) | 40.4 | 42.4 | 54.8 |
| v2 clean (in-place repair) | 40.4 | 39.6 | 53.3 |

Next step (GPU, one per variant and seed 42/43/44):

    python3 scripts/train_stage2.py --stage sft --data data/supervision_v2/raw --out $NCS_DATA/runs/v2raw_s42 --epochs 2 --seed 42
    python3 scripts/evaluate.py --adapter $NCS_DATA/runs/v2raw_s42 --split test_data.json --prompt detailed --name v2raw_s42-detailed
    python3 scripts/object_prf.py

## Result: v2 raw, seed 42 (RTX 3090, 2026-10-10)

KTVIC test (558 images), detailed prompt, same lexicon/gold as Table IV:

| model | P | R | F1 | true obj/cap | CHAIR_s | CHAIR_i | halluc/cap | words |
|---|---|---|---|---|---|---|---|---|
| shipped VSPS main_s42 | 41.5 | 36.7 | 39.0 | 1.30 | 79.2 | 50.1 | 1.57 | 34 |
| v2 raw s42 | 38.1 | 42.2 | 40.1 | 1.50 | 86.6 | 54.4 | 2.14 | 44 |
| v2 clean s42 | 37.6 | 41.0 | 39.2 | 1.45 | 86.7 | 54.8 | 2.12 | 40 |
| zero-shot Qwen2.5-VL-7B | 31.6 | 57.1 | 40.7 | 2.07 | 98.0 | 65.1 | 4.26 | 117 |

Recall +5.5 and F1 +1.1 over shipped s42, but precision −3.4 and hallucinated mentions per caption +36%: the richer targets move the model along the same precision/recall curve toward zero-shot rather than above it. F1 still trails zero-shot. Single seed. v2 clean (in-place repetition repair) is below v2 raw on every column, so the repair costs recall without buying precision; v2 raw is the better store.
