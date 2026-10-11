# Supervision v3 (built 2026-10-11, not yet trained)

Rebuilt from the stored Stage-1 records (`data/stage1_records/stage1_records.tar.gz`):

    tar -xzf data/stage1_records/stage1_records.tar.gz -C /tmp/s1
    python3 scripts/person_uncap.py --in /tmp/s1/stage1 --out /tmp/s1_person
    (cd scripts && python3 unanimous_uncap.py --in /tmp/s1_person --out /tmp/s1_unan)
    python3 scripts/build_dpo_data.py --in /tmp/s1_unan --out data/supervision_v3 \
        --seed 42 --min-supported 1 --budget 9 --detailed-variant B --style-variation --clean-props

`dpo.jsonl` is not committed (10 MB, rebuildable). Target quality vs v2 raw is in `data/supervision_v2/README.md` ("v3 target proxy").

Next step (GPU), same recipe as v2:

    python3 scripts/train_stage2.py --stage sft --data data/supervision_v3 --out $NCS_DATA/runs/v3_s42 --epochs 2 --seed 42
    python3 scripts/evaluate.py --model qwen2.5-vl-7b --adapter $NCS_DATA/runs/v3_s42 --split test_data.json --prompt detailed --name v3_s42-detailed
    python3 scripts/object_prf.py
