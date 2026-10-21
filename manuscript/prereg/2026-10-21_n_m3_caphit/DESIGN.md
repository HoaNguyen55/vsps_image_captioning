# N-M3 cap-hit share for Paper A: design

Status: **POST_HOC, descriptive, no verdict.** Authority: PD-30 (`.session_backup/2026-10-13/decisions/PD-30.txt`,
sha256 `4e535c31…`), as revised by the judge's CC-073 (`.session_backup/2026-10-13/decisions/CC-073.txt`). It
settles PD-28 work item 6 (mock review N-M3).
- The number makes no causal claim about the A-N2 failure of qwen3vl_8b.
- It enters the text only through amendment 5 (`manuscript/paperA_plan/CONFIRMATION_MAP_AMENDMENT5.md`).

**State before this design is committed:** nobody has computed any share from the G2-B `n_tokens` field.
- This verifier searched the repo and `.session_backup/` and found no file that does. The G2-B scorer
  (`scripts/g2b/score_g2b.py`), `g2b_score.json`, the precheck and the verification records do not read the field.
  The only `hit_max_share` computations are the A-N2 and B-N1 scorers, on their own decodes.
- The judge listed the field's keys without reading its values (CC-073).
- The structural gate below reads the values only to check presence, type and range. It outputs booleans and
  image counts, no share.

`caphit.py run` refuses to start unless:
- this file and `scripts/n_m3/caphit.py` equal their HEAD blobs;
- the structural gate holds;
- `data/results/n_m3/caphit_result.json` does not already exist.

## Question
How many G2-B Qwen3-VL-8B detailed captions reached the 160-new-token cap?

## Source of {p}: the recorded token counts (CC-073 ruling 1)
- Every G2-B `*.preds.json` records a per-image `n_tokens`. The decoder that writes it is
  `scripts/g2b/decode_qwen3vl.py` (sha `8a855ef4…`, the precheck `decoder_sha256`).
  - It counts the non-pad generated tokens with batch size 1, where pad is id 151643.
  - An `<|im_end|>` EOS (151645) counts when generated.
- **hit := n_tokens ≥ 160**, the registered `max_new_tokens` of the detailed prompt (G2-B prereg
  `decode.max_new_tokens.detailed`).
  - This is a direct reading of a registered output field, not an estimate.
  - Caveat: n_tokens = 160 also holds when EOS was exactly the 160th token. So the share is an upper bound by at most
    those cases. n_tokens < 160 means the cap was not reached.
- Each file is sha-checked against `data/results/g2b/g2b_score_record/precheck.json` (`runs.<run_id>.sha256`).
- The denominator is every image in each file (295 cv295, 231 uv231, 600 xm600), not the clean subset, because the
  cap is a property of the decode.

## Structural gate (CC-073 ruling 2)
For each of the 9 Vietnamese LADDER detailed runs `g2b_q3_{cv295,uv231,xm600}-detailed-T{0,05,08}`:
- `n_tokens` is present for every image in `predictions`;
- every value is an integer (Python `int`, not bool or float);
- every value lies in [0, 160];
- the record's `max_new_tokens` is 160.

The gate passes only if all four hold for all 9 runs. `gate.json` holds booleans and image counts only, with no
share. If the gate fails, STOP: the clauses take the fallback (amendment 5).

## Agreement check: re-tokenization (reported, not gating)
- **Tokenizer:**
  - Snapshot: `Qwen/Qwen3-VL-8B-Instruct` at revision `0c351dd01ed87e9c1b53cbc748cba10e6187ff3b`, the G2-B prereg
    `model.revision`.
  - Files: `tokenizer.json`, `tokenizer_config.json`, `vocab.json`, `merges.txt` and `config.json`. They were copied
    from the M3 snapshot into the git-excluded mirror `.session_backup/2026-10-21/n_m3_tokenizer/`, and each equals
    its entry in `.session_backup/2026-10-13/research_r9/C8_backbone/SHA256SUMS` (sha `dc7bd4a4…`, the G2-B prereg
    `model.checksum_manifest.sha256`).
  - Loader: `transformers.AutoTokenizer.from_pretrained(mirror, local_files_only=True)`, offline. The class must be
    `Qwen2TokenizerFast`.
  - The script refuses unless transformers is 4.57.6 and tokenizers is 0.22.2, the registered decode freeze
    `FREEZE.txt` (sha `bf152944…`).
- **Encoding:** `tok.encode(caption, add_special_tokens=False)`. The caption is the saved `predictions[image_id]`
  string: the decoder's `batch_decode(..., skip_special_tokens=True)` output, stripped.
- **Reported per run:**
  - re-tokenized length ≥ 155, ≥ 158 and ≥ 160;
  - the agreement of (length ≥ 158) with the recorded hit;
  - the share with no sentence-final punctuation. A caption has none when, after trailing whitespace and closing
    quotes or brackets (`" ' ” ’ » ) ]`) are removed, it is empty or its last character is not one of `. ! ? …`.
- **Validation facts.** These were computed under the earlier PD-30 design, on decodes that recorded `hit_max`. They
  are reported again by `run` and gate nothing:
  - A-N2 qwen3vl_8b `detailed_en`, cv295 + uv231en: 526/526 agree at ≥ 158. All 526 are recorded hits, with drift
    (re-tokenized − recorded) in [−1, 0].
  - B-N1 qwen3vl_8b Vietnamese `detailed`, KTVIC test + UIT-ViIC test: 787/789 recorded hits. Agreement is 788/789;
    the one miss is a caption with n_tokens = 159 whose re-tokenized length is ≥ 158. Drift is in [−2, 0].

## Outputs (run)
- **Per run** (set × temperature):
  - n;
  - the recorded hits and their share;
  - the re-tokenization counts and agreement;
  - the no-final-punctuation share;
  - the structural facts.
- **Runs:**
  - the 9 LADDER detailed runs;
  - the 2 `detailed_en` runs `g2b_q3_{cv295,uv231}-detailed_en-T0`, for S7 only, not pooled.
- **Per set, pooled** over its 3 LADDER detailed runs, caption-weighted.
- **{p}:** the pooled recorded-hit share over the 9 LADDER detailed runs (3,378 captions), in percent (CC-073
  ruling 3). It is rounded half up to an integer, exactly from the integer counts; Python's `round()`, which rounds
  halves to even, is not used.

## Fill (CC-073 ruling 4; amendment 5 rows 33-34)
- **§7.6:** "detailed captions capped at 160 new tokens, {p}% of which reached the cap by the recorded token counts,
  Supplementary S7", followed by "; the same cap as in the eight-LVLM test below" (CC-073b: semicolons inside §7.6's
  parenthesis, no nesting).
- **§10.5 c3:** "(Qwen3-VL-8B; detailed captions capped at 160 new tokens, {p}% of which reached the cap,
  Supplementary S7)".
- **Fallback** (the structural gate fails): "detailed captions capped at 160 new tokens (cap share: Supplementary
  S7)". It never says "not recorded".
- The per-run and per-set shares, the English runs and the agreement checks go to Supplementary S7.

## Run
`python3 -B scripts/n_m3/caphit.py run`, under an interpreter with transformers 4.57.6 and tokenizers 0.22.2. The
gate needs no tokenizer.

Process (PD-30): commit this design, the script and amendment 5 first. Then the gate, a single run, a verifier
re-run and the fill CP.

## Inputs (sha256; `caphit.py` refuses on any mismatch, before transformers is imported)
| File | sha256 (prefix) | Source of the expected value |
|---|---|---|
| `.session_backup/2026-10-13/decisions/PD-30.txt` | `4e535c31` | recorded here |
| `manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.json` | `c506bc77` | `g2b_score.json:prereg_sha256` |
| `.session_backup/2026-10-13/research_r9/C8_backbone/SHA256SUMS` | `dc7bd4a4` | G2-B prereg `model.checksum_manifest.sha256` |
| `.session_backup/2026-10-13/research_r9/C8_backbone/FREEZE.txt` | `bf152944` | G2-B prereg `model.venv.freeze_sha256` |
| `.session_backup/2026-10-21/n_m3_tokenizer/tokenizer.json` | `a5d85b6d` | SHA256SUMS |
| `.session_backup/2026-10-21/n_m3_tokenizer/tokenizer_config.json` | `c2da7718` | SHA256SUMS |
| `.session_backup/2026-10-21/n_m3_tokenizer/vocab.json` | `ca10d7e9` | SHA256SUMS |
| `.session_backup/2026-10-21/n_m3_tokenizer/merges.txt` | `599bab54` | SHA256SUMS |
| `.session_backup/2026-10-21/n_m3_tokenizer/config.json` | `5cd45286` | SHA256SUMS |
| `data/results/a_n2/a_n2_run.json` | `1f6ce422` | HEAD blob (CP-041) |
| `.session_backup/2026-10-20/a_n2_run/outputs/lbA_qwen3vl_8b_cv295-detailed_en.preds.json` | `7935912a` | `a_n2_run.json:inputs_sha256` |
| `.session_backup/2026-10-20/a_n2_run/outputs/lbA_qwen3vl_8b_uv231en-detailed_en.preds.json` | `91f9a726` | `a_n2_run.json:inputs_sha256` |
| `data/results/b_n1/b_n1_run.json` | `adad454d` | HEAD blob |
| `.session_backup/2026-10-20/b_n1_run/outputs/lbB_qwen3vl_8b_ktvic_test-detailed.preds.json` | `51df6c6f` | `b_n1_run.json:inputs_sha256` |
| `.session_backup/2026-10-20/b_n1_run/outputs/lbB_qwen3vl_8b_uitviic_test-detailed.preds.json` | `e89477e3` | `b_n1_run.json:inputs_sha256` |
| `data/results/g2b/g2b_score_record/precheck.json` | `02bdca27` | HEAD blob |
| `.session_backup/2026-10-20/g2b_score/outputs/g2b_q3_cv295-detailed-T0.preds.json` | `9ec53788` | `precheck.json:runs.*.sha256` |
| `.session_backup/2026-10-20/g2b_score/outputs/g2b_q3_cv295-detailed-T05.preds.json` | `1d9934b9` | `precheck.json:runs.*.sha256` |
| `.session_backup/2026-10-20/g2b_score/outputs/g2b_q3_cv295-detailed-T08.preds.json` | `59f2e553` | `precheck.json:runs.*.sha256` |
| `.session_backup/2026-10-20/g2b_score/outputs/g2b_q3_uv231-detailed-T0.preds.json` | `2a92344b` | `precheck.json:runs.*.sha256` |
| `.session_backup/2026-10-20/g2b_score/outputs/g2b_q3_uv231-detailed-T05.preds.json` | `3bef57a2` | `precheck.json:runs.*.sha256` |
| `.session_backup/2026-10-20/g2b_score/outputs/g2b_q3_uv231-detailed-T08.preds.json` | `d994c696` | `precheck.json:runs.*.sha256` |
| `.session_backup/2026-10-20/g2b_score/outputs/g2b_q3_xm600-detailed-T0.preds.json` | `a66647d1` | `precheck.json:runs.*.sha256` |
| `.session_backup/2026-10-20/g2b_score/outputs/g2b_q3_xm600-detailed-T05.preds.json` | `3e6189d6` | `precheck.json:runs.*.sha256` |
| `.session_backup/2026-10-20/g2b_score/outputs/g2b_q3_xm600-detailed-T08.preds.json` | `944668eb` | `precheck.json:runs.*.sha256` |
| `.session_backup/2026-10-20/g2b_score/outputs/g2b_q3_cv295-detailed_en-T0.preds.json` | `736a3d32` | `precheck.json:runs.*.sha256` |
| `.session_backup/2026-10-20/g2b_score/outputs/g2b_q3_uv231-detailed_en-T0.preds.json` | `85066857` | `precheck.json:runs.*.sha256` |

## Readings for the judge
- **R1. Upper bound.** n_tokens = 160 cannot tell a cap hit from an EOS generated exactly as the 160th token. The
  re-tokenization agreement per run shows how often the two disagree.
- **R2. No nesting (CC-073b).** The §7.6 clause sits inside an existing parenthesis, "(three temperatures × a short
  and a detailed Vietnamese prompt; …)". So the §7.6 fill and both fallbacks use semicolons and commas, not
  parentheses. The per-location fallbacks are amendment 5 rows 33-34.
