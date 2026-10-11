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
    python3 scripts/evaluate.py --model qwen2.5-vl-7b --adapter $NCS_DATA/runs/v2raw_s42 --split test_data.json --prompt detailed --name v2raw_s42-detailed
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

## v3 target proxy (CPU, 2026-10-11, not trained)

Target captions vs KTVIC train references (`scripts/recall_funnel.py`, sft_caption row; v2 raw reproduces 40.6 / 41.2 exactly from the stored records):

| build | P | R |
|---|---|---|
| v2 raw (budget 9) | 40.6 | 41.2 |
| v2 raw, budget 12 / 15 | 40.2 / 40.0 | 41.8 / 41.9 |
| + clean_props repairs (stutter collapse, clause → subject existence) | 40.7 | 41.2 |
| + `scripts/unanimous_uncap.py` after person_uncap | 40.5 | 43.2 |
| + target repairs below (v3) | 40.2 | 41.8 |

v3 vs v2 raw on the same 3,589 train images, strict and lenient (gendered gold and caption words → `người`, as in the table above):

| store | strict P / R / F1 | lenient P / R / F1 |
|---|---|---|
| v2 raw | 40.6 / 42.4 / 41.5 | 48.2 / 54.2 / 51.0 |
| v3 | 40.2 / 43.0 / 41.6 | 47.6 / 56.6 / 51.7 |

Defect rates in detailed targets (`scripts/target_lint.py`, % of captions with at least one hit):

| pattern | shipped | v2 raw | v3 |
|---|---|---|---|
| unverified gendered noun | 9.9 | 12.2 | 0.3 |
| `một số X` read as a noun `số X` (count 1) | 8.6 | 14.2 | 0.4 |
| pronoun remnant (`anh ta`, `cô ấy`) | 2.0 | 2.8 | 0.0 |
| person NP echoed (`một người, một người`) | 5.1 | 6.4 | 4.3 |
| colour on a person (`người màu đỏ`) | 3.1* | 3.1 | 3.2 |
| duplicated word | 1.3 | 1.4 | 1.5 |

*same pattern as the other columns. v3 repairs: `một số` added to `NUMBER_MARKERS` (root cause: `một số rau` parsed as one `số rau`, count 1, in 1,597 of 28,912 entities; stored records re-parsed at build time); gendered nouns inside predicates/attribute values neutralised (the verifier never asked about them), with the subject echo stripped again afterwards; `anh ta`/`cô ta` added to the pronoun-remnant rule; attribute values that restate the subject or name another referent repaired or dropped. Gender neutrality costs about 1.2 strict recall points, which were credited for gender the verifier never checked.

Proposition level (SUPPORTED set): person_uncap R 48.0 / P 39.8 → + unanimous_uncap R 50.7 / P 39.3. Budget is not the bottleneck. The renderer loses about 7 recall points between the SUPPORTED set and the caption, and the captions it writes carry errors the model then learns: a colour moved onto the wrong noun (`một người mặc áo kẻ có màu đỏ và trắng` → `Một người có màu đỏ và trắng`), gendered text leaking from clause-swallowing propositions, and ungrammatical sequences (`Cái mũ này đang đạp xe`). Fixing the renderer comes before the next training run.

Relation gate (`relation_predicate` in `rescap/pipeline/generate.py`, applies to new Stage-1 runs): of 21,406 stored relation propositions it keeps 5,704. In a 40-item sample, all of the 468 SUPPORTED ones it drops are malformed (`một tòa nhà | thang | một cầu thang`). Only 511 relations reach the v2 targets (2.5% of selected propositions), so the gate matters for precision, not recall.

Strict-metric ceiling for a gender-neutral captioner: 83.7 recall (47.6% of train images have gendered gold), so neutrality is not what caps recall.
