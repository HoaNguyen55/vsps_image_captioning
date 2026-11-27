# ERRATUM O31-2 to PREREG_DRAFT_O31_v3.md (5b33480b, commit 3d49435), ERRATUM_O31_1.md (91108b81, commit 3319dd7) and COMPUTE_PLAN_O31_v3.md (7557ca3b)

Written by ruling CC-519 (2026-11-27), before any O31 output exists: no P0r, G1, G2, P1 or G3 output, and no tier-2 or tier-3 file has been read.
It is committed before P0r. It changes no hypothesis, threshold, margin, seed, set, estimand, statistic or stop rule.
It does five things:
- moves every O31 step from a rented host to the PI's own PC, with record checks;
- settles one conflict between §3.5 (overlap pass before G1, tier-3 set included) and §3.4 (the tier-3 set is fixed only before the first G3 output), keeping the timing of §3.5;
- fixes three run details that the committed text leaves open and that can move a registered outcome (probe environment and batch, decode precision, the English prompt);
- states how the GPU caps are counted;
- names the two ruling conditions it replaces.

**Why.** COMPUTE_PLAN v3 names "a rented host ... Not the PI's PC". That rested on PI-1127h. The PI has replaced it (PI-1127m, LOG 2026-11-27T13:54:47Z): no new rentals; his PC is used and kept on when needed. He also allows data and results to stay on that PC, with one backup copy on the laptop (PI-1127r, LOG 2026-11-27T15:49:33Z).

## E1. Host (replaces the COMPUTE_PLAN v3 "Hardware" paragraph and the §5 bullet "After a job")

**Hardware:** the PI's own PC with one RTX 3090 24 GB (PI-1127m). No host is rented for O31. All GPU-h and caps of COMPUTE_PLAN stay as written. Every O31 step (P0r, G1, G2, P1, G3 and later) runs there, under the record checks O-H1 to O-H8, each written to the session record before the step it guards.

- **O-H1 Own folder.** Every O31 file lives under `~/vsps_host/o31` on that PC: code, repository snapshot, data, models, the Hugging Face cache (`HF_HOME`), the pip cache, `TMPDIR`, the virtual environments and all outputs. Nothing is read or written outside that folder, and no other study's folder is touched.
- **O-H2 Interpreter.** CPython 3.12.3 is unpacked inside the folder, and every virtual environment is made from it. The interpreters are passed to every script by variable: `PY` (transformers 4.51.3: Vintern probes, training, the student decoder) and `PY_LB` (transformers 4.57.6: the InternVL3 probe only, E3). The system Python is never used or changed, and nothing is installed with administrator rights. Before H1 the record shows `readlink -f` of each interpreter (inside the folder) and its version (3.12.3).
- **O-H3 Push by tar, no repository.** The code tree (`scripts/o31/` at the gatekeeper commit) and the repository snapshot (`git archive` of the same commit) arrive as tar files. Each tar's sha256 is printed on the laptop before the push and matched on the PC after it. `find ~/vsps_host/o31 -name .git` returns nothing before each step.
- **O-H4 Environment and models.** The pip-freeze sha256 of each environment is recorded at H1 and re-checked before each GPU job. Every model is loaded offline (`HF_HUB_OFFLINE=1`) by revision, with its per-file pins checked by the committed code.
- **O-H5 GPU use.** Before and after each GPU job the record holds one `nvidia-smi` compute-process query. A job starts only if no process of another study and no other O31 job is listed. Any process of the PI's own desktop session that is listed is named in the record. One O31 GPU job runs at a time.
- **O-H6 Reserved windows.** No O31 process runs on the PC, and nothing is pushed to it for O31, from the C-CONF set-up line (LOG OPS-1128ab, 2026-11-27T16:18:56Z) until the LOG carries that session's end line. The same holds for any later window the LOG reserves the PC for. Before the first O31 step after a window, the record cites the LOG id of its end line.
- **O-H7 Data stay; laptop backup (PI-1127r).** Data, models, environments and outputs may stay in the folder; the clean-host rule (PI-1115s) does not apply to this PC. Every output file (records, probe tables and their shard lists, stores, `k0.json`, adapters, decodes, scores) is copied to the laptop's home file system (not `/mnt/d`), checked against the sha256 printed on the PC and set to mode 444, within one day of being written. Files that hold caption text are never committed.
- **O-H8 Test custody.** No image, gold file or output of the tier-3 set, and nothing derived from it, is placed on the PC before its registered step (§3.5: tier-3 images reach the GPU host only after the tier-3 ruling). No folder of another study's test session is opened.

Where COMPUTE_PLAN, ERRATUM_O31_1 or the code's comments say "rented host" or "host", they now mean this PC under E1.

## E2. The tier-3 set in the §3.5 overlap pass (§3.5 vs §3.4)

§3.5 runs the overlap pass, tier-3 set included, before G1; §3.4 fixes the tier-3 set only before the first G3 output. The two are settled as follows; the timing of §3.5 is kept:
- **When.** The pass runs before the first of G1 and G2. P1's `--exclude` file is the 2 byte twins of §3.1 plus every part (a) hit.
- **The tier-3 set in the pass.** The pass uses KV-4,224 (the branch-1 set of §3.4) as the tier-3 set, on W25 descriptors only, whatever Q1's answer. Its ids are rebuilt as in the M0 registration (`scripts/grl/id_counts.py counts()` on its pinned inputs, count 4,224, ids pin 86d93863). Its images are never decoded and never placed on the PC for this pass (E1 O-H8); its descriptors come from the existing W25 memory of CC-153 where it holds them, otherwise from a machine and step that a ruling names.
- **Effect.** A part (a) hit against KV-4,224 leaves the training pool in every branch; if §3.4 ends in branch 2 or 3, these removals are reported as such. A part (b) hit of KV-4,224 against UIT-ViIC test applies only in branch 1. Branch 2 (AMBER) keeps its own W25 pass under its amendment (§3.4).
- The rule of §3.5 itself (exact sha plus the committed W25 rule, direction as ERRATUM_O31_1 E13) is unchanged.

## E3. Environment of the InternVL3 probe (§4.1, §10)

Family 2 is the registered E2b hub snapshot pin `OpenGVLab/InternVL3-8B-hf` @ 259a3b64 (B-N1 registry 9ff02dc2). transformers 4.51.3 has no InternVL image-text-to-text class, so it cannot load that snapshot. It runs in its own environment with transformers 4.57.6, the version of the environment E2b ran it in (LOG OPS-1101e2b-importgate and OPS-1102e2b-launch; the freeze of E2b's rate run records transformers 4.57.6). Vintern-1B probes, training and the student decoder stay on transformers 4.51.3 (§2). COMPUTE_PLAN §3 already plans separate training and probe environments. The model, revision, score, token sets and question form are unchanged.

## E4. Probe batch size (§4.1)

- Vintern-1B probes run at batch 1, as E1b.
- InternVL3 probes run at batch 8 only if, over the first 50 images of the job, every probe's s at batch 8 is within 1e-3 of its value at batch 1 and the top token is equal (left padding); otherwise at batch 1. The decision is written once, in the job's `smoke.json`, and holds for the whole job.
- G2 is one job over every pool image with records, after G1's records for the 69 images exist. It is not split into parts without a new ruling.

## E5. Load precision at decoding (§2)

Every arm (S0, S1, S2 and every ablation, at every tier) decodes with the base model loaded in bf16 plus the arm's LoRA adapter (S0 has none). The 4-bit load option is never used for a reported row. This is the default of `scripts/evaluate.py` (a68d5682), and FAIR v10 reports its inference latency with the "bf16 base model with the adapter".

## E6. The English detailed prompt of H5 (§6.2)

The fixed English detailed prompt of H5 is exactly:

`Describe this image in detail in English.`

(UTF-8 sha256 525a4e1bf5849e2c38e44cadceed724f66167ac95e621764c384865574913c4a; the string `PROMPTS["detailed_en"]` of `scripts/evaluate.py` at a68d5682, the repository's existing English detailed prompt.) It is fixed here before any O31 English output exists and is not tuned. No other English prompt is used for an H5 row.

## E7. How caps are counted (COMPUTE_PLAN §1, §5; stop rule K4)

A cap is wall time from the job's `launch.json` t0, pauses and restarts included. A GPU job therefore runs as one continuous session. A K4 stop is never resumed without a ruling.

## E8. Ruling conditions replaced

- CC-504r2 condition C1 ("on the rented host") now reads "on the PI's PC under E1 of this erratum".
- CC-504 host item H1 ("for G2/G3 ... transformers 4.51.3") now reads "4.51.3 for training, Vintern probes and decoding; 4.57.6 for the InternVL3 probe environment (E3)".

## E9. Text left as it was

Everything else in the prereg, ERRATUM_O31_1 and COMPUTE_PLAN v3 is unchanged.
