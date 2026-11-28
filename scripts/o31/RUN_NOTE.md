# O31 code g12d: the G1 stage-1 fix after CC-521 (2026-11-28)

**Base.** g12c (SHA256SUMS e40128da; cleared for commit by CC-521 (a) but never committed; this package replaces it in the commit, CC-521r2). The change is in `G12C_TO_G12D.diff` (a record), with a hunk map. This is round 3 of 3 for G1 (a diff read).

**Binding text:** PREREG v3 (5b33480b), ERRATUM_O31_1 (91108b81), ERRATUM_O31_2 (817eac8f), ERRATUM_O31_3 (979486bf; committed with this package, byte copy of judge_cc521/expected_fixes), COMPUTE_PLAN v3; rulings CC-504, CC-504r2, CC-519, CC-521.

## CC-521 fixes in g12d
- **W4 / F3 (match by stem).**
  - `record_names` returns record stems. `new_items` maps them back to the train file names (115 names end in .png, .jpeg or .JPG); an unknown stem stays unmatched and is a FAULT, as are two train files sharing a stem. `run()` compares stems.
  - `prepare()` refuses unless the 69 names equal `data/screening/val_manifest.json` (pin 79f3628c, added to REUSED).
  - Tests use mixed extensions and a stand-in screening list.
  - Real-input record (`INPUTS_AND_RELEASE_CHECK.log`, laptop, names only): 3,769 train items, 115 not .jpg, 69 new, equal to the screening manifest, no twin among them.
- **W5 / F1 (first-release generator) and F2 (seed).**
  - `stage1.RELEASE` pins all 26 files of `git archive 1f30d09 rescap scripts/generate_stage1.py` (tar sha 474ff239...; generate_stage1.py e9d911a1).
  - `use_release(tree)` refuses a changed, missing or extra file. It then drops every loaded `rescap*` and `generate_stage1` module, puts the tree first on sys.path, imports generate_stage1 and the seven stage-1 modules, and refuses if any loads from outside the tree.
  - `g12.py stage1 --release TREE` calls it after `check_qwen`, `check_vintern` and `m0.check_model` (HEAD snapshot). `prepare()` and `run()` use the returned module; probes, K0 and the rest stay on HEAD.
  - `run()` seeds random, NumPy and torch with 42 once before `main()`. `g1_stage1.json` records the seed, the release commit, generate_stage1's sha and the loaded generator's `attn_implementation` (a wrapper on `QwenVLAdapter.load` records it).
  - A fresh-process test does the HEAD imports first and uses a stand-in release tree with its own pins. Mutants X08 (HEAD modules kept) and X09 (tree appended) must be killed.
  - The real tree passed `use_release` on the laptop (same log).
- **W6.** A14 (staged copy), A16 (refs/main content) and C02 (g12 Vintern pins) have tests.
- **W7 (binding).** `check_cache` refuses unless the checked folder resolves to `$HF_HOME/hub/models--<org>--<name>/snapshots/<revision>`. `check_qwen` calls it; `check_vintern` is the Vintern form, called by `g12.py stage1` before `m0.check_model`. Tests and own mutants Q01, V01 and V02 cover both.
- **N1.** "once" is dropped. **N3.** run_pass refuses duplicate ids (test).
- **N2 (not done here).** Keep the pool image sha list from `pool.npz` with the G1 and probe records.
- **N5.** The pass's feature venv `PY_FEAT` (ImageHash 4.3.2, numpy 2.5.4, pillow 13.0.0, PyWavelets 1.10.0, scipy 1.18.1, torch 2.5.1+cpu, as `cenfeat_venv_freeze.txt` 1a639a50) is named in R2 of CC-521. Its wheels are staged before the push.

**Superseded below:** the g12c W2 text "FAIR's settings, as recorded for the 3,700" and its "accept as E1a did" decision. CC-521 ruling 3 and ERRATUM_O31_3 replace them.

## W1: the judge's CC-519 mutants (`jmut_cc519.py` f35858bb, run unchanged; record `jmut_cc519_run_on_g12c.txt`)

| mutant | new test |
|---|---|
| K03 cap clock reset on resume | `test_probe_cap_clock_survives_resume`: launch.json t0 two hours old, cap 1 h, so the job must stop with 4 |
| K09 finalize keeps non-finite | `test_finalize_refuses_non_finite_after_resume`: the NaN row is written before the halt; after a resume the pair is skipped; finalize must refuse |
| K12 smoke not fetched, K13 not touched | `test_probe_explored_fetched_and_touched`: `explored(..., m0_dir=)` with a stand-in M0 folder (the real touched list, so its sha pin holds; an invented fetch list holding one untouched id) |
| L03 g12 smoke custody off | `test_g12_smoke_custody_and_exit_code`: custody refuses before any model load |
| L04 g12 refused image allowed | `test_g12_image_loader_refuses_listed_bytes` |
| L05 g12 smoke verdict ignored | `test_g12_smoke_custody_and_exit_code`: a failed smoke exits 2 |
| L01, L02, D08 (W5) | `test_decode_e5_e6_prompt_and_g12_refusals` |

`explored` gains one argument, `m0_dir`, used only by tests (default: the pinned M0 folder). It was needed for K13: in the pinned lists every fetched image is touched (821 fetched, 0 fetched and not touched), so no real name can reach that clause.

**K08 (yes/no overlap allowed) cannot be killed. My argument that it is equivalent; the judge decides:** `token_ok` also requires every yes id to decode to a non-empty prefix of "có" and every no id to a non-empty prefix of "không". An id in both sets would have to decode to a non-empty string that is a prefix of both words, and none exists ("c..." vs "k..."). So the disjointness term never decides. Expected survivors: K08, the four the judge accepted (K10, K14, K15, K21) and D06 (W5, decoder read before G3).

## W2 as written for g12c (the stage-1 wrapper; code version, matching and binding superseded above)
- **Which images.** KTVIC `train_data.json` (pin 72ee9b57: 3,769) minus the names of the stage-1 tarball records (pin b312de68: 3,700, member names only, no record opened). Both byte twins must be among the records, and exactly 69 images must remain (prereg §3.1).
- **Settings.** `generate_stage1.py` (pin ad965ceb) `main()` runs unchanged with FAIR's values from `configs/main.env` (pin 2ea67f5f; a test parses it): `--generator qwen2.5-vl-7b --verifier vintern-1b --max-entities 8 --max-pairs 8 --verifier-tiles 4`. There is no `--logit-verifier`, so Vintern answers with K = 5 sampled dual queries, as recorded for the 3,700. The colour cross-check is on. QWEN_MAX_PIXELS must be unset (adapter default, as stage 1 and E1a), HF_HUB_OFFLINE=1, transformers 4.51.3 (E8).
- **Models.** Qwen2.5-VL-7B-Instruct @ cc594898 and Vintern-1B-v3_5 @ b98f263e are loaded by hub id from the HF cache inside the job folder. Qwen: snapshot dir = the revision, refs/main = the revision, every B-N1 file pin holds (`decode_hf_vlm.check_snapshot`). Vintern: `m0.check_model`.
- **Input custody.** `train_data.json` must be the staged copy in `NCS_DATA/datasets/ktvic`. Each of the 69 images must be present and none may have bytes listed in exclusion.json.
- **Records.** The records carry the `train_data.json` reference captions through FAIR's own `load_manifest` (the manifest `o31_g1_manifest.json` holds the 69 items) and land in `G1/records` in the stage-1 format.
- **Cap.** G1's cap is 3.5 GPU-h (stage-1 plus the Vintern probes), counted from `G1/launch.json` t0 as wall time (E7). A timer sets generate_stage1's own stop flag, so the run ends after the image in flight and writes STOP.json. The Vintern probe of the 69 then runs as `g12.py probe --family vintern --records G1/records --out G1`, so both parts share one t0.
- **Result.** It returns 0 only if `G1/records` holds exactly the 69 names. `g1_stage1.json` holds counts and the names' sha.
- Planned at 112 s per image, the 69 images take about 2.15 GPU-h (COMPUTE_PLAN G1: 2.2, cap 3.5).

**Decision for the judge: stage-1 details the registration does not name.** Prereg §3.1 says "the same generator settings", and E3/E8 name transformers only for Vintern probes, training and decoding. The wrapper follows the E1a registration (`manuscript/prereg/2026-10-31_vsps_j_e1e2/PREREG.md`, stage-1 v1 unchanged):
- transformers 4.51.3 (the `PY` environment);
- Qwen2.5-VL-7B-Instruct @ cc594898 (B-N1 pin);
- QWEN_MAX_PIXELS unset (adapter default 1280·28·28);
- attention sdpa (no flash-attn installed).
E1a disclosed that the revision and the attention kernel of the FAIR stage-1 run were not recorded. The same disclosure holds here: the 69 new records may differ from the 3,700 in those two unrecorded details. Recommendation: accept as E1a did, and disclose it in the paper.

## W3: the §3.5 launcher (`s35.py`, `src/o31/overlap.py`): needs its own read, and the pass must run before the first of G1 and G2
- **`feats` (PI's PC; 4 runs)** computes the descriptors of pool, ktvic_test, uit_test and karpathy_test with `build_memory.features` unchanged and the SSCD weights at the W25 pin (9f26bd4c).
  - The id lists are sha-pinned. Pool = `train_data.json` minus the 2 twins (3,767, ids = file names). ktvic_test = `data/lb/sets/ktvic_test.tsv` (558). uit_test = `data/lb/sets/uitviic_test.tsv` (231). karpathy_test = `cen_coco_test.tsv` (5,000).
  - Every image must be readable, and byte-equal to the sha in its list where the list has one. The output is in W25 npz form.
- **`kv` (laptop)** takes the KV-4,224 rows of C-EN's `feats_coco_kval.npz` (pin 9783f7a6, the CC-153 W25 memory; KV-5,000 ⊇ KV-4,224). The ids are rebuilt by `m0.kv4224()`, which is `id_counts.counts()` on its pinned inputs with ids pin 86d93863 (E2). No KV image is read.
- **`pass` (laptop)** needs all five sets at their registered counts. It calls `overlap.w4_pass` (the committed rule, direction as E13) and writes two files:
  - `w4_pass.json`: removed ids, counts and input shas;
  - `exclude_p1.txt` = the 2 twins plus every part (a) hit, which is P1's `--exclude` (E2).
- **`kv` needs the full laptop tree as VSPS_REPO.** `m0.kv4224()` reads untracked pinned inputs (UIT-ViIC and Karpathy json, gt_cache, a_n3 gold), which a `git archive` snapshot does not hold. Its laptop tests ran only with an injected id function; the real rebuild has not been run.
- **Decision for the judge: where `kv` and `pass` run.** ERRATUM_O31_2 E1 O-H8 says nothing derived from the tier-3 set is placed on the PC before its registered step, and E2 says the KV descriptors come from the existing W25 memory. That memory is on the laptop, and the KV id rebuild reads laptop-only pinned files (UIT-ViIC and Karpathy json, gt_cache). So I put `kv` and `pass` on the laptop: CPU work of seconds, ids and descriptors only. The four other feature files come to the laptop by the O-H7 copy, sha-checked. If the judge prefers the PC, O-H8 needs a ruling line first.

## ERRATUM_O31_2 E3-E6 in the code (word for word)
- **E3.** Family 2 is `OpenGVLab/InternVL3-8B-hf` @ 259a3b64 in its own environment with transformers 4.57.6 (`probe.FAMILIES`; `check_env`; host `PY_LB`). Vintern probes, stage-1, training and the decoder use transformers 4.51.3 (`PY`).
- **E4.** Vintern runs at batch 1. InternVL3 runs at batch 8 only if, over the first 50 images of the job, every probe's s at batch 8 is within 1e-3 of batch 1 and the top token is equal (left padding); otherwise batch 1. The decision is written once in `smoke.json`. New: `probe.g2_inputs` makes `g12.py probe --family internvl3` refuse unless the record folders hold all 3,769 records (the 3,700 plus G1's 69) and the exclude file holds both twins, so G2 is one job after G1.
- **E5.** The base loads in bf16 for every arm. The 4-bit option is removed from `load_student` and from `g12.py`, and `run.json` records `"base_dtype": "bfloat16"`.
- **E6.** `decode.PROMPTS["en"] = "Describe this image in detail in English."` (sha 525a4e1b; a test checks it equals `evaluate.py` `PROMPTS["detailed_en"]`). `g12.py decode --lang en` refuses without `--en-prompt` and refuses any other string.
- **E7.** Every cap is wall time from `launch.json` t0, and a STOP is never resumed without a ruling. This is unchanged in the code, and stage-1 follows the same rule.

## N1 and host rules (E1)
- `g12.py probe` defaults its refused list to exclusion.json (pinned) and writes `OUT/inputs.json`: n_records, the sha of the sorted file names, and the shas of the exclude file and of the refused list, plus the snapshot revision.
- `host_selftest.sh` now requires `O31_BASE` and records O-H1 to O-H3 before H1:
  - `PY` and `PY_LB` resolve inside it and are CPython 3.12.3;
  - TMPDIR, HF_HOME, PIP_CACHE_DIR and OUT are inside it;
  - there is no `.git`.
- In H-G, Qwen now goes into the HF cache (as Vintern), so stage-1 can load it by hub id, and `stage1.check_qwen` checks it. Its header says "the PI's PC", not a rented host (N2).
- No file names the system interpreter or the administrator home folder; every Python call goes through `$PY` or `$PY_LB`.

## Order on the PI's PC (after each reserved window's end line, E1 O-H6)
1. H1-H4 + H-G (`host_selftest.sh`, HG=1).
2. `s35.py feats` ×4 on the PC, then the copy back, then `s35.py kv` and `s35.py pass` on the laptop.
3. G1: `g12.py stage1`, then `g12.py probe --family vintern --out G1`.
4. G2: `g12.py probe --family internvl3` over the 3,700 + 69 records with `--exclude exclude_p1.txt`, as one job.
5. P1.

## Pins
REUSED has 51 files, all clean in git at 72d1a91: g12c's 50 plus `data/screening/val_manifest.json` (F3). `stage1.RELEASE` separately pins the 26 files of the 1f30d09 tree. The H2 tar must hold every REUSED path; the release tar travels as its own file (O-H3).

## Tests and mutants (g12d, final bytes; records beside the package)
- Laptop venv: Python 3.12.3, torch 2.15.0+cpu, transformers 4.51.3, numpy 2.5.4, peft 0.15.2.
- VSPS_REPO = `git archive 72d1a91` of rescap, scripts, data/coco_probe and the other REUSED paths.
- `run_tests_g12d.log`: the suite and the package's own `mutants.py` in full (W8).
- `jmut_cc519_run_on_g12d.txt` and `jmut_cc521_run_on_g12d.txt`: both judge files, run unchanged.
- Expected survivors: K08, K10, K15, K21 and D06 (CC-519 set), and A02, B07 and B09 (CC-521 ruling 4).

## Files (repository location)
- `scripts/o31/` holds `g12.py`, `s35.py`, `k0.py`, `test_o31.py`, `mutants.py`, `run_tests.sh`, `host_selftest.sh`, this note and `SHA256SUMS`.
- The package goes to `scripts/o31/src/o31/` and adds `probe.py` and `stage1.py`.
- `RUN_NOTE_r2.md` stays as committed.
