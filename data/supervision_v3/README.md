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

## Result: v3 seed 42 (RTX 3090, 2026-10-11)

KTVIC test (558 images), detailed prompt, `scripts/object_prf.py --ci`:

| model | P | R | F1 [95% CI] | P_h | R_vague (F1) | CHAIR_s | CHAIR_i | halluc/cap |
|---|---|---|---|---|---|---|---|---|
| v2 raw s42 | 38.1 | 42.2 | 40.1 | – | – | 86.6 | 54.4 | 2.14 |
| v3 s42 | 37.0 | 43.3 | 39.9 | 42.2 | 53.7 (47.3) | 89.8 | 55.7 | 2.33 |
| P1 gold-caption SFT | 78.3 | 42.7 | 55.3 [53.0, 57.5] | 80.3 | 46.1 (58.6) | | | |

The surface repairs (gender 12.2→0.3%, "số X" 14.2→0.4%) do not move object P/R: v3 sits on the same point as v2 raw (within one seed). Template targets are the ceiling, not their typos; see manuscript/novel_direction/06 §6 for the direction that replaces them.
