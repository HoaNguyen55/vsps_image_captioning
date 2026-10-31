# VSPS H1 pilot, AMENDMENT 1: Phase A re-run all-GPU on m5

Status: DRAFT, 2026-10-31 (written 03:45Z = 10:45 VN). Not committed. Applies to PREREG.md 7411957a (commit 07fd1d5),
scripts/vsps_h1/SHA256SUMS f0df7153. Label on every output stays `TIER 1 / DEV-EXPLORE (VSPS-H1)`.
Tier: REVERSIBLE (dev-explore pilot on train), one judge, bar >= 90.

## A1. Why

The PI chose a separate rented RTX 4090 (ssh alias `m5`) for Phase A, to have the result today (PI message 2026-10-31
~10:30 VN). This uses the PI override that PREREG §8 and CC-198 ruling 7 already allow ("The PI may override with M1"),
with a separate rented GPU instead of M1. Every §8 condition written for M1 applies to m5 unchanged:
- cap **4 GPU-h**, with the 50-image projection rule (A4);
- upload only {image_id, file_name, entity id -> category_vi} and the 3,700 train JPEGs, to a folder outside every other
  dataset tree (m5 holds no other dataset);
- the replay (`vote.py`) and the funnel stay on the laptop;
- the run is all-GPU, never mixed with CPU lines.

The §8 rule "never overlaps C-T2 or A-T3" holds trivially: m5 is a separate host and runs nothing else. The laptop-scoring
preemption rule no longer applies, because nothing runs on the laptop CPU.

## A2. What does not change

- GO/STOP rule (§5), thresholds +5.0 recall points and 2.0 precision points, judge-read triggers (R3, M6), records,
  metrics M1-M6, exclusions (§6), known limits (§7).
- Detector code and pins: `detect_boxes.py` 70a5cbba, `config.json` a56bb77b, `vi_en_map.json` 657d5dac, byte-identical
  on m5. Same repos and revisions, same thresholds. **No code change**: the only difference is `--device cuda`
  (detect_boxes.py already takes `--device`).
- Line pins (W1): each line carries config_sha256, map_sha256 and `device` = `cuda`. `vote.py` refuses a boxes file that
  mixes devices, so a CPU line cannot enter the GPU file.

## A3. The laptop CPU run is abandoned unread

A CPU Phase A run was started on the laptop under PREREG §8 (pid 3176610, `~/vsps_h1_runs/phaseA/boxes.jsonl`, about
1,020 of 3,700 lines at 03:41Z). It has **not** been voted, scored or looked at; no line has been opened.

At GPU launch, in this order:
1. Check that `/proc/3176610/cmdline` is the detect_boxes.py command with `--out .../phaseA/boxes.jsonl --device cpu`,
   then `kill 3176610` by exact PID (never by name) and confirm it has exited.
2. Move `~/vsps_h1_runs/phaseA/` to `~/vsps_h1_runs/phaseA_cpu_abandoned/` unread.
3. Record only `sha256`, byte size and line count of its boxes.jsonl in the ledger line, as a disclosure.

That file is never passed to `vote.py`, never merged and never resumed. The **GPU boxes file is the only Phase-A input to
vote.py.**

## A4. m5 run (cap 4 GPU-h, 50-image projection rule)

Staging on m5 (done 2026-10-31, before this amendment's read; nothing beyond the 5-image smoke has run):
- `/root/vsps_h1/scripts/vsps_h1/`: detect_boxes.py, config.json, vi_en_map.json (byte-identical to the SUMS pins).
- `/root/vsps_h1/records/`: the 3,700 stage-1 records stripped to `image_id`, `file_name`,
  `entities[].{id, category_vi}`; same basenames, so the sorted order is the same as on the laptop.
- `/root/vsps_h1/images/`: the 3,700 train JPEGs.
- `/root/vsps_h1/ktvic/`: **filename-only stubs** for the custody check `train_only_ids` (see A6).
- Manifest: 7,405 files, `sha256sum -c` all OK on m5; manifest sha256 8ab56a3b. Caption 8-gram scan of every staged text
  file against KTVIC train+test (97,496 8-grams): 0.

Environment on m5: python 3.12.3 (laptop 3.12.3), torch 2.15.0+cu132 (laptop 2.15.0+cpu), torchvision 0.29.2+cu132
(laptop +cpu), transformers 5.22.1, pillow 13.0.0, numpy 2.5.4; every other package equals the laptop `pip freeze`.
The CUDA build adds only cuda/nvidia/triton wheels. Weights were fetched at the pinned revisions; all 15 files used match the
laptop cache by sha256 (GroundingDINO model.safetensors 5548f844c928c4b6f411fa8cbcc2bfa8dbbba437cb1d513975519f93c2a9ed21,
OWLv2 model.safetensors e1e130b9e404cf91a75ad45644c1da9d7fa5284085eecc864266a6923efb99e7). The unused pytorch_model.bin
copies were deleted, and the run is offline (`HF_HUB_OFFLINE=1`).

Run command (m5; `--out` sits outside `/root/vsps_h1`, the script's ROOT, as the custody guard requires):
```
mkdir -p /root/vsps_h1_runs/phaseA && test ! -e /root/vsps_h1_runs/phaseA/boxes.jsonl
cd /root/vsps_h1 && HF_HUB_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1 /root/venvs/vsps_h1/bin/python \
    scripts/vsps_h1/detect_boxes.py --records records --images images --ktvic ktvic \
    --out /root/vsps_h1_runs/phaseA/boxes.jsonl --device cuda > /root/vsps_h1_runs/phaseA/detect.log 2>&1
```
A resume after a kill uses the same command with `>>` and the same device.

**50-image projection rule.** PREREG §8 and CC-198 name this rule but do not define it, and no earlier prereg or ruling
does; this is its first written definition. When 50 lines exist: projected GPU-h = (elapsed wall time since launch) + 3,650 x (median
`seconds` of lines 2-50). If it is above 4.0 GPU-h, stop the run and report; do not change anything to make it fit.
GPU-h is counted as wall-clock time from launch to exit, since the rental bills by the hour. The smoke projects about
0.2 GPU-h (A5).

**Return to the laptop.** `sha256sum` on m5, `scp` to a **new** laptop path `~/vsps_h1_runs/phaseA_gpu/boxes.jsonl`
(never into `phaseA/`), and the sha is checked again on the laptop. Then, on the laptop, as in CC-201 W3(e):
```
cd /mnt/d/vsps_image_captioning && (cd scripts/vsps_h1 && sha256sum -c SHA256SUMS)
~/.venvs/vsps_h1/bin/python scripts/vsps_h1/vote.py --records ~/vsps_h1_runs/stage1 \
    --boxes ~/vsps_h1_runs/phaseA_gpu/boxes.jsonl --out ~/vsps_h1_runs/phaseA_gpu/replay
```
`vote.py` gets the full laptop records; m5 never sees references, propositions or verdicts. INCOMPLETE means resume on m5,
pull again, vote again; never decide on fewer than 3,700.
If m5 is lost mid-run: resume on m5 with `>>` if the host survives; otherwise start a **fresh** file on a new all-GPU host
(or a fresh all-CPU file). The abandoned CPU file (A3) is never resumed or merged. After the pull, `/root/vsps_h1` and `/root/vsps_h1_runs` on m5 are
deleted and the deletion is logged.

## A5. GPU vs CPU numerics (measured, disclosed)

The 5-image smoke on m5 (`--limit 5`, ids 2-6, scratch file `/root/vsps_h1_runs/smoke_gpu/boxes.jsonl`, sha 97ca9961)
was compared with the CPU smoke `~/vsps_h1_runs/smoke/boxes.jsonl` (sha 9e6579b2, same config and map shas, same ids):
- same key set, sizes, pins and entity -> prompt map in every line; `device` cuda vs cpu;
- 48 prompt x detector cells: 0 count differences and 0 presence differences, so no vote changes on these 5 images;
- matched boxes differ by at most 0.64 px and scores by at most 0.0071;
- 1 GroundingDINO cell swaps the order of two near-equal top boxes. The consensus box is the GroundingDINO box in score
  order (§3.2), so such a swap can change which box an entity gets, and therefore the geometric channel.

GPU kernels are not bit-identical to CPU and not guaranteed deterministic run to run. A detection whose score sits within
about 0.01 of a threshold (GroundingDINO 0.35 or 0.25, OWLv2 0.10) can flip between devices. This is disclosed beside the
result. It is not tuned and not corrected, and the run is never mixed across devices. The smoke file is not reused: the run
writes a fresh file.

Smoke speed: 1.20 s for the first image (CUDA warm-up), then 0.16-0.20 s per image (median 0.18 s). 3,700 x 0.18 s is about
11 min, plus model load: about 0.2 GPU-h, far under the 4 GPU-h cap. The CPU took 30-44 s per image.

## A6. Staging items outside the §8 upload list (for the judge)

`detect_boxes.py` reads `--ktvic/{train,test}_data.json` to check that every image is train-only. The real files hold
captions, so they are **not** uploaded. Filename-only stubs are uploaded instead:
- `train_data.json`: `{"images": [{"filename": ...}]}` for exactly the 3,700 file_names (all checked on the laptop to be in
  the real train split and absent from test);
- `test_data.json`: the 558 KTVIC **test filenames only**, with no captions and no images, so the on-host guard stays a real
  check.

The test filename list and the three code/config files are outside the literal §8 list ({image_id, file_name,
entity id -> category_vi} + JPEGs). They carry no caption text and no test image. An empty test stub would also run, but it
would weaken the guard. Recommended: accept the test filename stub. The stub is already on m5 (uploaded before this read). If the judge picks the
empty stub instead: overwrite `test_data.json` with `{"images": []}`, regenerate the manifest and re-run `sha256sum -c`
before launch.

## A7. Records

Ledger line OPS-<id> at launch: this amendment's sha, commit 07fd1d5, device cuda on m5 (alias only, never host, IP or
port), the m5 manifest sha 8ab56a3b, the abandoned CPU file's sha/size/lines (A3), and the 1-decimal rounding note
(CC-201 ruling 6). summary.json is anchored as in CC-201 W3(f).
