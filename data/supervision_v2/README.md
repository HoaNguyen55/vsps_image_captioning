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
