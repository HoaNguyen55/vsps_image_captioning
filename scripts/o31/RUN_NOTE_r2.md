# O31 code, round 2 (ruling CC-504): run note, 2026-11-27

**Binding text:**
- `manuscript/prereg/2026-11-27_o31/PREREG_DRAFT_O31_v3.md` (5b33480b, commit 3d49435);
- `ERRATUM_O31_1.md` (91108b81, commit 3319dd7).

The code implements the erratum's items E1–E13 as written. No choice in the code is open any more (N3).

**Round 1 is untouched:** `~/vsps_out/o31_code` (SHA256SUMS cd78a489). The change from round 1 to round 2 is in `R1_TO_R2.diff`, which opens with a hunk → W map.

Nothing here read a dataset caption or image, and nothing ran on a GPU. Nothing was written to /mnt/d.

## W items

**W5: Vintern model string and records without Q+ (E3)**
- `verify.FAIR_MODEL = "5CD-AI/Vintern-1B-v3_5"`. A test parses `scripts/vsps_j_m0/m0.py` (pinned, 5d3c02f4) and asserts the constant equals `MODEL["repo"]` and the literal string.
- A proposition with no Q+ keeps its recorded status.
- `run_k0` reports per point: the counts by state, `no_q`, `no_q_not_rejected` and `miss`.
- `run_k0` raises a FAULT if a proposition without Q+ is not recorded REJECTED, or if a Q+ score is missing.
- The fixtures use the real model string. One fixture has a REJECTED proposition with no probe.

**W3: order (E4)**
- `run_k0` takes the RAW records. Each arm runs statuses → `store.uncap` → build:
  - S1 uses the recorded statuses;
  - each grid point uses `apply_states`.
- `store.uncap` calls `person_uncap.main()` unchanged, with its default types, on temp dirs. A test shows its output is byte-equal to running `scripts/person_uncap.py` itself on synthetic UNCERTAIN, SUPPORTED and REJECTED gendered records.
- A record that already carries `gender_uncap` is a FAULT.
- Each arm's store is written to `--store-dir/<arm>/sft.jsonl` on the host. The sha256 reported in the K0 output is the sha of that written file (E5). The output also carries the person_uncap stats and the per-point elapsed time, and a projection is printed after each point against the 3 h P0r CPU cap.
- A partial run (P0r, the 15 Vintern points) carries `preview_no_verdict`. Only a complete 30-point run carries `decision` (E7).
- `--exclude` takes the §3.5 (a) removals.
- **P0r/P1 command:** `VSPS_REPO=<snapshot> $PY -I -B k0.py --records <raw stage-1 dir> --table vintern=<E1b probes.jsonl> [--table internvl3=<G2 table>] [--exclude <ids>] --store-dir <host dir> --out k0.json`.
  - `k0.py` is a top-level launcher. `-I` drops the cwd from sys.path, so `-m o31.gate` would not find the package.
  - A test runs `k0.py` as an isolated subprocess on synthetic records with an exclude file, and re-hashes every written store against the report.

**W2: import closure**
- REUSED now has 36 files, all clean in git at 3319dd7:
  - the 18 from round 1;
  - 17 more modules that the full suite loads, including `run_k0` through the real builder and `person_uncap`: `rescap/{__init__,metrics,repro,vocab}`, `rescap/svp/{__init__,entailment,matching}`, `rescap/vi/{__init__,classifier,color}`, `rescap/vlm/{__init__,base,mock,registry}`, `scripts/c_stage1/decode_icl`, `scripts/g2b/decode_qwen3vl`, `scripts/lb/decode_hf_vlm`;
  - `m0.py`.
- `test_zz_import_closure_pinned` runs last. It fails if any loaded repo file is not in REUSED.
- `rescap/pipeline/generate.py` stays pinned. It loads lazily when a build neutralizes a gendered noun.

**W1: decision lines guarded**
- New tests cover:
  - the registered constants and function defaults;
  - the CI index on a hand-computed vector;
  - the strict and inclusive boundaries of H1 and H2;
  - the Holm-adjusted verdict;
  - H4 = max of its two parts, and the H3 null;
  - the rehearsal drawing with replacement, via the new `outer_unique_share` (about 0.63 at n_sub = n; it would be 1.0 without replacement);
  - the 0.98 gate, through a fixture where P(PASS) = 0.975 must not pass;
  - OP_mid over all points, through a nearest point that is infeasible;
  - `load_table` keeping the first occurrence.
- `mutants.py` holds the 27 own mutants (M26 `--exclude` ignored, M27 reported sha differs from the written store are new), 6 W3/W5 mutants and the judge's 35. J34 is re-pointed, because W3 moved its line: it now targets `s1 = arm(*store.uncap(records), scaled=False, name="S1")`, with the same mutation (S1 from O31 states).
- Re-pointed sites: J34 only.

**W4:** ERRATUM_O31_1.md is committed (3319dd7), and its sha is checked as 91108b81.

**N2:** `train.argv` passes `--loss-mask legacy` (E8).

## Results (laptop, python 3.12.3, numpy 2.5.4, `-I -B`, VSPS_REPO = the repo at 3319dd7)

| Run | Result |
|---|---|
| `test_o31.py` | 60/60 passed |
| `mutants.py` (own 27 + W3/W5 6 + judge 35 = 68) | 68/68 killed, 0 survived, 0 bad sites (log: `run_tests_r2.log`) |
| `jmut_cc504.py` run unchanged on r2 (record: `jmut_cc504_run_on_r2.txt`) | 34 killed, `survived 0 []`; J34 prints SITE (re-pointed above, killed in `mutants.py`) |
| `host_selftest.sh` dry run on the laptop (`git archive 3319dd7` snapshot, tar 7a666891) | H1–H3 PASS (59/59 before the k0.py test was added; judge script 34 killed + 1 re-pointed); H4 stopped at the sha check, as expected, because synthetic stand-ins were passed. The H4 block was also checked on a synthetic tarball |

## Host self-test (`host_selftest.sh`, before P0r)

| Item | What it does |
|---|---|
| H1 | Writes a pip freeze and its sha. With GPU=1, it also requires transformers 4.51.3 and trl 0.19.1 (repo `requirements.txt`), and records torch, peft, bitsandbytes and accelerate |
| H2 | Unpacks `git archive <COMMIT> rescap scripts data/coco_probe` read-only and records the tar sha. `o31.repo()` must accept every pin |
| H3 | Runs `run_tests.sh`: SHA256SUMS, the tests, all 68 mutants. It records the log sha, and with JMUT set it runs the judge's script unchanged |
| H4 | Checks the records tarball is b312de68 and probes.jsonl is ffd27917 (OPS-1031e1bdone). It requires 3,700 records, 0 gender_uncap traces, and every no-Q+ proposition REJECTED (expected 1,625), and prints counts only |

H5 (global_step = N_steps under 4.51.3) is for before G3, not P0r. It is not part of this script.

## Not covered (unchanged from CC-504)

The probe runner, the G1 stage-1 run and the decoder are still stubs. They need their own code read before G1 and G2.
