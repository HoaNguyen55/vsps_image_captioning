# ERRATUM O31-3 to PREREG_DRAFT_O31_v3.md (5b33480b), ERRATUM_O31_1.md (91108b81), ERRATUM_O31_2.md (817eac8f) and COMPUTE_PLAN_O31_v3.md (7557ca3b)

Written by ruling CC-521 (2026-11-27), before any O31 output exists: no P0r, overlap-pass, G1, G2, P1 or G3 output, and no tier-2 or tier-3 file has been read. It is committed before the first O31 push to the PI's PC.
It changes no hypothesis, threshold, margin, set, estimand, statistic or stop rule.
It fixes what §3.1's "the same generator settings" means for the stage-1 run of the 69 KTVIC-train images without records.

**Why.** The stage-1 records (tarball b312de68, 3,700 records) were committed with the first release (commit 1f30d09, 2026-08-30). `rescap/pipeline/generate.py` changed after that (commits 93070e1 and 41896b7: whole-word gendered-noun match, a relation-predicate gate, the subject-echo cut), and these changes alter the records that `scripts/generate_stage1.py` writes. Ruling CC-521 checked all 3,700 records, counting only:
- `classify_epistemic` at the release gives the recorded `epistemic` label for 192,216 of 192,216 propositions; the current version differs on 4,494.
- The current relation gate would drop 15,702 and change 3,352 of the 21,406 recorded relation predicates.
- 3,686 records carry the release's Vietnamese diagnostic strings; none carries the English strings of the later translation commit.
This checks one function and the diagnostic strings, not every line of the generator.
Running the current code for the 69 would mix two generators in one training pool.

## F1. Stage-1 code for the 69 images (§3.1; COMPUTE_PLAN G1)

- The 69 records are written by `rescap/` and `scripts/generate_stage1.py` at commit 1f30d09 (the first release). They arrive as the tar `git archive 1f30d09 rescap scripts/generate_stage1.py`. Its sha256 is printed on the laptop before the push and matched on the PC (ERRATUM_O31_2 E1 O-H3). Each file that stage-1 imports from it is pinned by sha256 in the O31 code; `scripts/generate_stage1.py` is e9d911a1c32d4e3aa258cc26c33a4023e3ffb93207cbc41ecf65d23a1654cf57. `main()` runs unchanged.
- Flags: `--generator qwen2.5-vl-7b --verifier vintern-1b --max-entities 8 --max-pairs 8 --verifier-tiles 4`, colour cross-check on, K = 5 sampled verifier answers. These are the argparse defaults of that file and the values of `configs/main.env`.
- The FAIR stage-1 run did not record the following details. They are fixed here as E1a fixed them:
  - transformers 4.51.3;
  - Qwen2.5-VL-7B-Instruct @ cc594898 and Vintern-1B-v3_5 @ b98f263e, each loaded by hub id, offline, from the Hugging Face cache inside the job folder, with refs/main = the pin and every file pin checked on the snapshot that is loaded;
  - `QWEN_MAX_PIXELS` unset;
  - attention sdpa (flash-attn not installed), as recorded from the loaded generator.
  The paper states that these details may differ from the FAIR run.
- All other O31 code (probes, K0, the overlap pass, training and decoding) uses the gatekeeper commit of `scripts/o31` and the repository snapshot of that commit.

## F2. Seed of the stage-1 run

FAIR's stage-1 sets no seed. The G1 run seeds Python `random`, NumPy and torch (CPU and CUDA) with 42 (`configs/main.env` SEED) once, before `main()`. No deterministic-algorithm switch is set. Sampled verifier answers are not claimed to be bit-reproducible.

## F3. Which 69 images

The 69 are the KTVIC train images (train_data.json 72ee9b57: 3,769) whose file stem has no record in the tarball. They are matched by file stem: 115 KTVIC-train file names end in .png, .jpeg or .JPG, and the tarball names its records by stem. The two byte twins of §3.1 have records and are not among the 69. The 69 file names equal those of `data/screening/val_manifest.json` (79f3628c, n 69). The run record checks this and stops on any difference.

## F4. Text left as it was

Everything else in the prereg, ERRATUM_O31_1, ERRATUM_O31_2 and COMPUTE_PLAN v3 is unchanged.
