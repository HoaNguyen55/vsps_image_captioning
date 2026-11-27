# COMPUTE plan B-D1/A3 v2 (draft; v1 2026-11-27T09:22Z; v2 after CC-505)

## Where it runs

- **All of S0, S1 and S2 run on a rented host only** (CC-505 ruling 9; PI-1111, PI-1031, PI-1127h). The PI's own PC is not used. Nothing runs on the laptop, H3 included.
- **Money order (PI-1127h, CC-505 ruling 9).** The C-CONF staging floor (430,000 VND by 2026-11-28T09:30Z) is met first. The D1 rental starts only after that host is paid, or after a top-up that keeps the floor. So no D1 result exists before 2026-11-28 at the earliest. While renting, the 50,000 VND warning rule applies (PI-1126f).
- **The host is a fresh machine.** It gets the full install bundle (PI-1115r) before any push. No host alias, IP or port appears in any registered file (CC-501e1 E1).
- **The laptop only writes files and pushes inputs.**
- No GPU is used. CPU only (`CUDA_VISIBLE_DEVICES=`), `nice -n 19`, as in FE-CERT.
- **Precondition before S1: the pinned environment.** The rented host is not the FE-CERT host. It needs Java 21.0.13.0.3, the VnCoreNLP jar `9e2811cd…`, pyvi 0.1.1 and the underthesea 9.5.0 wheel `81400f41…`, with the same numpy and scipy as the FE-CERT venv. `b_fecert.env_check` must pass on the host, and G0 then confirms the numbers. If the environment cannot be matched, it is a stop and a judge line, not a substitution.

## CPU estimate (from the FE-CERT run records, `results/b_records/*.time`)

| step | basis | CPU-h |
|---|---|---|
| S1 re-score: 54 F_dev members, D, 75 files | stage 1: 9,487 user-s, 28 min wall at 562% CPU | 2.6 |
| S1 re-score: 18 `uts` members, D | stage 2b: 8,055 user-s for `uts` + `chr` (36 members) on D and the first-look pool, so about half | 1.1 |
| G0 check (class stats from matrix vs DEV.json) | same work as `add_class`, already inside the S1 figure | ~0.2 |
| S2 H1–H3, AER bootstraps (3 folds × 1,101 × one 10,000×558 product) | ~2×10¹⁰ flops | <0.1 |
| S2 A3 (1,000 nulls × 54 members, plus 72 for the F row) | ~5×10¹¹ flops | ~0.3 |
| S0 self-tests and mutants on stub data | FE-CERT G0 took ~2.5 min wall | ~0.2 |
| **total** | | **≈ 4.5 CPU-h; hard stop at 8 CPU-h**; about 1.5 h wall on 6–8 cores |

**Hard stop at 8 CPU-h (CC-505 B6).**
- Each stage runs under `/usr/bin/time -v` and under `prlimit --cpu=<remaining CPU-seconds>`. The remaining figure is 28,800 s minus the user+sys seconds of the stages before it.
- Before each stage, the coordinator adds the user+sys seconds of every `.time` record so far.
- If the sum reaches 28,800 s, or a stage is killed by the limit: stop, write no result, and write a judge line. A re-run needs that ruling.
- The limit is per process. The Java segmenter is a child process, so the cumulative check on the `.time` records is the binding one.

- RAM: about 1.6 GB peak (stage 1: 1.53 GB max RSS).
- Disk: under 100 MB. The `PER_IMAGE_D1.npz` matrix is 75 × 72 × 558 float64, about 24 MB.

## Inputs by sha256 (all present on the laptop, checked 2026-11-27 by hash only)

| input | sha256 |
|---|---|
| 73 own files `data/results/<name>.preds.json` | each equal to its row in `SYSTEMS.tsv` (`30ac9555cd6cdc8fd50f47e637e734fac564c692605f590ba213a60a3be6e1a0`); 73/73 checked |
| baseline `result_resnetlstm.json` (`.session_backup/2026-10-22/b2/thesis_code_1a8d105/`) | `85a7dcdb195450bea1d67137ad11ab41a65b76dab5f796d59dae2776f38ae5f2` |
| baseline `result_vittrans.json` (same folder) | `b12747b55e61019c060469190f560f8a7a5f8f4d190aa83a63cf9ba551fb8de3` |
| KTVIC test references `data/datasets/ktvic/test_data.json` | `cc22ec6a8883773cb23c87ad5b64925f5a53c21982117274b53621f454e7ebbf` |
| `DEV.json` (G0 target; H3 input) | `88ff39aa9552b671a0e439aec961d0fefe02df1f52a2a5df9765a9d8226f7e8d` |
| `RESULT.json` (G0 `uts` verdict target) | `25614b469cf59dc61f15e839b89a8e78ca0b316905afc4bd2ae52eaa0d32b43a` |
| `FAMILY.json`, `CENSUS.json` | `431d92a4a2eaf0516446c9f9aef453ee52d311b6e329d97cd1abb4c4e8017f77`, `2252167b435890c5dbf70a97e0fc918bc6989c48acda636427d4dd2889599afa` |
| code reused unchanged: `b_fecert.py`, `family.py`, `protocol_pilot.py`, `ptb_protocol.py`, `b2.py`, `b2_controls.py`, `b_pa1.py`, `build_pairs.py` | `67e43dea…`, `7cb2c69b…`, `6aee4282…`, `ea5fbe6e…`, `52b8c145…`, `6f2a7258…`, `c481fcf4…`, `49692235…` (full values in `DEV.json::code_sha256`) |
| segmenters | VnCoreNLP 1.2 jar sha256 prefix `9e2811cd`; pyvi 0.1.1; underthesea 9.5.0 wheel `81400f41b75ceff6f80c52b4ad043806c80f5899ec555d8e6374d468a59bce56`; Java 21.0.13.0.3 |
| new code (to be written after the registration commit) | `scripts/b_d1/b_d1.py` and its test file, read by a judge before S1 |

## Not needed

- No decoding, no model weights, no images. Only text output files and references are pushed.
- The first-look pool is not used at all (CC-505 B5): no fetch, and no `V.json`.

## Custody

- `PER_IMAGE_D1.npz` and `RESULT_D1.json` are mode 444 and pinned by sha256 on the LOG before the next step reads them.
- The per-image matrix is never committed (per-image container precedent). `RESULT_D1.json` holds aggregates only and is committed after the result read.
- After the run, the host files are backed up and the host is deleted. Its ssh alias, host keys, password and askpass files are then cleaned (PI-1115s).
