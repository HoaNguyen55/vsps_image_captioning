# W4 top-up note (Paper A, CC-108 W4; PI-1026c Q3 = YES; revised under CP-111 W3 and PI-1026f)

**Scope.** The job decodes the two adapter systems `fuse2_s42` and `p1_s43`, each with the short and the detailed prompt (4 runs), on `data/coco_probe/manifest_rest2500.json`. These are the 2,500 Karpathy-test images that are not in the seed-42 `manifest.json`. The merge then turns COCO-2500 into the full Karpathy test of 5,000 images for all 9 systems (r4). What r4 changes in the paper is fixed in advance by `FILL_RULE.md`, beside this note.

**Constraints.**
- **Order on M3.** The job runs on M3 only: after C's XM block has finished and C's cleanup has been verified (CP-111 ruling 5). Nothing starts before that. CP-111's slot "before B's p1-gold decode" is released: there is no p1-gold decode (CP-112, l.140).
- **Caps.** Planned path: 5 GPU-h in total, counting the parity slice, the rate check and the top-up. Parity-fail path: 7 GPU-h in total, parity slice included (PI-1026f Q1).
- **Ledger.** The job keeps its own GPU ledger, `/root/outputs/a_w4/gpu_ledger.tsv` (one line per run: name, start UTC, end UTC, wall s). Nothing is written under C's directories.
- **Parity-fail path (PI Q1).** PI-1026f (LOG l.460): if gate (b) fails, M3 re-decodes all 5,000 images for the 4 adapter runs in one environment. There is no merge across environments, and the mismatch count is disclosed. The cap for that re-decode is 7 GPU-h (about 5.6 expected). See "Parity-fail path" below.
- **Date fallback (PI Q2).** PI-1026f (LOG l.460): if W4 has not landed by 11-03, M3 is extended and A's experiment freeze slips by up to one week; the 12-20 submission date is unchanged. Neither r0 nor a 5-system row becomes A's headline COCO number.
- **Before any M3 output.** This note, `FILL_RULE.md` and the package (`w4/`, `eval/`, `SHA256SUMS`, `INPUTS.sha256`) are committed through the gatekeeper (CP-111 commit 2). Then the job may start.

**Measured cost.** The n2 queue logs (`.session_backup/machines/n2/queue/36_coco_{a,b}_*.log`) give the final per-image rates on 2,500 images:

| Run | s/image |
|---|---|
| p1_s43 short | 0.84 |
| p1_s43 detailed | 0.87 |
| fuse2_s42 short | 0.82 |
| fuse2_s42 detailed | 1.41 |

That gives 2,500 × 3.94 s = 2.74 h, plus the model loads and the parity slice (about 0.1 h), so ≈ 2.8 GPU-h in total. The n2 GPU type was not recorded.

## Gate (a): adapter sha256 (checked locally 2026-10-26)

| Adapter | sha256 of `adapter_model.safetensors` |
|---|---|
| fuse2_s42 | `4dd674ab85ca2bb957594460cde28916ce6c643bf3e08a8e6d7489ccd643d857` |
| p1_s43 | `c2715ef34f2c95ced88d71e10323469df4d794aca341c3843c979fbedb9140e4` |

- **Local backup:** both files exist in the mirror at `.session_backup/machines/O-2308423/root/outputs/runs/{fuse2_s42,p1_s43}/adapter_model.safetensors` (154.1 MB each, with `adapter_config.json`).
- **Match:** both shas equal the lines `runs/fuse2_s42` and `runs/p1_s43` of `.session_backup/machines/n2/adapters.remote.sha256`.
  - That file is a listing of the n2 `runs/` directory, dated 2026-10-13, the day after the 36_coco jobs ran.
  - The job scripts load `$NCS_DATA/runs/{p1_s43,fuse2_s42}` from that directory, but the job logs record no sha.
- **What gate (a) rests on.** Gate (a) rests on the 10-13 n2 listing plus gate (b). It shows that the backups are the adapters n2 held, not that they are the bytes the jobs read; gate (b) is the real equivalence test.
- **On M3:** upload both run folders to `/root/ncs-data/runs/{fuse2_s42,p1_s43}/`. Then run `sha256sum /root/ncs-data/runs/{fuse2_s42,p1_s43}/adapter_model.safetensors`, which must print exactly the two values above. If either differs, stop and do not decode.

## Code and environment

- **Code:** the decoder is `scripts/coco_probe.py`, the same code that wrote the existing 2,500-image decodes (n2 jobs 36_coco_a/b).
- **Change since the n2 run:**
  - n2 ran it at the 2026-10-12 version (commit 2521435). Commit 4592d69 (10-14) later added a `--model` switch.
  - The default backbone keeps the exact earlier load: hub id `Qwen/Qwen2.5-VL-7B-Instruct`, class `Qwen2_5_VLForConditionalGeneration` and 28×28-pixel tokens, which `_check()` asserts at start-up.
  - The `short` and `detailed` strings of `scripts/evaluate.py` `PROMPTS` hash the same at 2521435 and HEAD (sha256 prefixes `8870589c4a32` and `0addb5dd720e`).
  - `MAX_NEW` is 60/160 in both versions. Decoding is greedy, bf16, with a merged adapter.
  - The parity slice, gate (b), covers the `coco_probe.py` change.
- **Pinning:**
  - Use the repo at the paper-v10 commit current at run time, with `coco_probe.py` sha256 `930a3899e229e22a1b9326951210e49da3be2904cecd1a4214f02ac8b261ebb8` and `evaluate.py` sha256 `a68d56826d90d8a409493cd6f49007e906c6cb4f5668314edb9b8e7a632e8236`, as of 2026-10-26 (both also in `INPUTS.sha256`).
  - Pass `--model qwen2.5-vl-7b` explicitly.
- **env.txt (CP-111 W3 (d)), before the parity slice:**
  ```bash
  mkdir -p /root/outputs/a_w4   # first M3 command of the job
  cd /root/vsps && . .venv/bin/activate && export NCS_DATA=/root/ncs-data
  bash scripts/paperA/a_w4/w4/w4_env.sh /root/outputs/a_w4
  ```
  **Stop rule (before parity).** If `env.txt` shows any `ABSENT`, a non-zero `uncommitted paths`, or a HEAD that does not contain the CP-111 commit 2 (`git merge-base --is-ancestor <commit 2> HEAD` fails), stop: no decode.
  It writes `/root/outputs/a_w4/env.txt`: repo HEAD, the `coco_probe.py`/`evaluate.py` and adapter shas, the base-model snapshot hash in the M3 HF cache (`refs/main` and `snapshots/`), `nvidia-smi -L` with the GPU UUID redacted, and the GPU name/driver/memory, `python --version` and `pip freeze`. It records no host name, address or port. `env.txt` is mirrored and goes into commit 3.
- **Untested risk:** the n2 package versions are not in the mirror. The parity slice, gate (b), is the only test of environment equivalence.

## Images

Stage the val2014 files of `manifest_rest2500.json` on M3. Also stage the 50 files of the parity slice, which are seed-42 images.

```bash
cd /root/vsps && . .venv/bin/activate && export NCS_DATA=/root/ncs-data
python scripts/download_coco_images.py --manifest data/coco_probe/manifest_rest2500.json --out $NCS_DATA/datasets/coco_probe/val2014
python scripts/download_coco_images.py --manifest scripts/paperA/a_w4/w4/parity50_manifest.json --out $NCS_DATA/datasets/coco_probe/val2014
```

- Check the sha256 of `scripts/paperA/a_w4/w4/parity50_manifest.json` on M3 against `SHA256SUMS` before the downloads.
- Both downloads must report `errors: 0`. Count 2,550 distinct manifest files present.
- Write `sha256sum` of every staged file to `/root/outputs/a_w4/images_sha256.txt`, which is mirrored. There is no earlier sha list for these files.
- **Karpathy images stay on M3 only.** They are mirrored as sha lists, never as files, and they are deleted from M3 after the merge mirror has been verified (CP-111 ruling 5).

## Gate (b) parity slice and gate (c) rate, in one run before the top-up

**Slice.** `w4/parity50_manifest.json` (sha256 `e169d4da…`) holds 50 ids of the existing decodes. It was drawn with `random.Random(20261026).sample(sorted cocoids of manifest.json, 50)` and fixed 2026-10-26, before any M3 output.

**Expected values.** The expected caption hashes are in `w4/parity50_expected_caption_sha256.json` (`01ccc958…`). It holds hashes only, no caption text.

```bash
cd /root/vsps && . .venv/bin/activate && export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1
O=/root/outputs/a_w4
for s in fuse2_s42 p1_s43; do
  python scripts/coco_probe.py --manifest scripts/paperA/a_w4/w4/parity50_manifest.json --images-dir $NCS_DATA/datasets/coco_probe/val2014 \
    --out-dir $O/parity --adapter $NCS_DATA/runs/$s --name $s --model qwen2.5-vl-7b 2>&1 | tee $O/parity_$s.log
done
```

**Gate (b).**
- Mirror `$O/parity/` locally, then run `python scripts/paperA/a_w4/w4/w4_merge.py parity <mirror>/parity`.
- It must print 50/50 byte-identical for all 4 runs and exit 0. The selftest (`w4_merge.py selftest`) passes it on rows cut from the existing decodes and catches one changed caption.
- Gate (b) stays 50/50 byte-identical across all 4 runs. It is never loosened: a different decoder environment is a different system.
- Any mismatch stops the top-up. Nothing is merged, and the mismatch count is disclosed. The parity-fail path below applies.

**Gate (c).**
- The parity logs print s/image at 50/50 for each run. The projection is 2,500 × (sum of the four parity rates) + 4 × the model-load time seen in the logs.
  - Projection ≤ 5 h: continue.
  - Projection > 5 h: stop and ask the PI (CC-108 ruling 4: up to 8 h is the PI's call, not the job's).
- During the top-up, the decoder prints its rate every 50 images. After 200 images of each run, re-project with the measured rate and apply the same rule.
- A hard timeout wraps the whole top-up. It is set to 5 h minus the measured parity wall time, so the total stays within the cap.

## Top-up decode (after gates a–c pass)

```bash
cd /root/vsps && . .venv/bin/activate && export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1
O=/root/outputs/a_w4
T=$(( 5*3600 - ${PARITY_SECONDS:?set to the measured wall time of the parity runs} ))
timeout ${T}s bash -c '
for s in p1_s43 fuse2_s42; do
  python scripts/coco_probe.py --manifest data/coco_probe/manifest_rest2500.json \
    --images-dir $NCS_DATA/datasets/coco_probe/val2014 --out-dir '$O'/rest2500 \
    --adapter $NCS_DATA/runs/$s --name $s --model qwen2.5-vl-7b 2>&1 | tee '$O'/rest2500_$s.log
done'
sha256sum $O/rest2500/*.jsonl > $O/rest2500.sha256
```

- **Output directory:** the out-dir is `/root/outputs/a_w4/rest2500`. It must never be `coco_transfer`, because the decoder appends to existing jsonl files.
- **Resume:** the decoder can resume (one line per image, never rewritten). After a stop, the same command continues where it left off.
- **What may be read:** no caption is read or printed before the merge, apart from the hashes in gate (b).

## Parity-fail path (PI-1026f Q1)

Only if gate (b) fails. Stage the 2,500 seed-42 images of `manifest.json` as well (same download command, sha list appended to `images_sha256.txt`). Decode `data/coco_probe/manifest_full5000.json` for the 4 runs into `/root/outputs/a_w4/full5000`, with the top-up commands (manifest and out-dir changed). Rate rule on this path, replacing gate (c):
- projection = 5,000 × (sum of the four parity rates) + 4 × the model-load time seen in the parity logs;
- threshold = 7 h minus the GPU time already spent on the parity slice (the strict reading of the PI's cap 7 GPU-h, CP-111a ruling 4); projection above it: stop and ask the PI;
- the same re-projection after 200 images of each run, and a hard timeout equal to the threshold: `T=$(( 7*3600 - ${PARITY_SECONDS:?set to the measured wall time of the parity runs} ))`.

Then, locally:

```bash
python scripts/paperA/a_w4/w4/w4_merge.py full <mirror>/full5000 data/results/coco_transfer_full5000
```

It asserts that each run covers `manifest_full5000.json` exactly, writes the rows unchanged in content, and prints, per run, how many seed-42 captions differ from `coco_transfer`; that count is disclosed. The post-merge gates below do not apply on this path (nothing is merged). The n2 2,500 decodes stay as the discovery record.

## Merge rule into 5,000

```bash
python scripts/paperA/a_w4/w4/w4_merge.py merge <mirror>/rest2500 data/results/coco_transfer_full5000
```

**Merge.** For each of the 4 runs, `w4_merge.py merge` takes the union by cocoid of `data/results/coco_transfer/{run}.shard0of1.jsonl` (2,500 seed-42 ids) and the M3 half. Before it writes anything, it asserts that:
- each id appears in one row only;
- the old half equals `manifest.json` and the new half equals `manifest_rest2500.json`;
- the two halves are disjoint;
- their union equals `manifest_full5000.json`.

It writes the merged files in cocoid order and prints their sha256. The pinned `coco_transfer/` files stay untouched.

**Post-merge gate (CP-111 W3 (b)), run by `merge` on the files as written; any failure exits non-zero:**
1. The merged files are re-read from disk. They hold exactly the `manifest_full5000.json` ids in cocoid order, every seed-42 caption equals `data/results/coco_transfer` byte for byte, and every other caption equals the M3 half byte for byte.
2. `eval/check_coco_full.py data/coco_probe/manifest.json data/coco_probe/instance_gold.json all9full <tmp> <merged dir>` is run and must equal the frozen `.session_backup/2026-10-14/r11_litmaps/L1/check_coco.json` on `n_img`, `systems` and every `gold` cell. Completeness is asserted inside `check_coco_full.py` and by the merge asserts above.

The selftest runs both gates on a stand-in merge (zero-shot rows in place of the M3 half) and reproduces the frozen `check_coco.json`; it also shows that gate 1 catches a single changed seed-42 caption.

## Re-score (r4)

Outputs go to `.session_backup/2026-10-26/a_full5000/out/` beside r0–r3 (commit 3 force-adds them):

```bash
O=.session_backup/2026-10-26/a_full5000/out; G=.session_backup/2026-10-26/a_full5000/instance_gold_full5000.json; E=scripts/paperA/a_w4/eval
python $E/check_coco_full.py data/coco_probe/manifest_full5000.json $G all9full $O/r4_full5000_all9.json
python $E/h4_micro_full.py data/coco_probe/manifest_full5000.json $G all9full $O/h4_r4_full5000_all9.json
python $E/check_coco_U_boot_full.py data/coco_probe/manifest_full5000.json $G all9full $O/a33_r4_full5000_all9.json
python $E/closed_form_full.py $O/h4_r4_full5000_all9.json $O/r4_full5000_all9.json $O/cf_r4_full5000_all9.json
python $E/summarize.py    # re-checks the r0 gates, adds r4, writes $O/w4_summary.json
```

`instance_gold_full5000.json` is pinned by sha only (`INPUTS.sha256`; rebuilt by `eval/build_instance_gold_full5000.py`). Each script was checked on r0 (9 systems, 2,500) against its frozen output before any M3 output (`check_coco.json`, `h4_check.json` coco2500 incl. T3/T2_profile, `check_coco_U_boot.json`, `h4_check.json` T5_closed_form; record in `.session_backup/2026-10-26/a_cp111/`).

r4 becomes A's reported COCO row whatever it shows, labelled exploratory (post hoc full-split extension, PI-1026c). The text changes follow `FILL_RULE.md` mechanically; no branch is chosen after reading. COCO-2500's in-sample b (0.549 at two references) stays the registered XM3600 prior (4ccbee3) whatever the 5,000 result is.
