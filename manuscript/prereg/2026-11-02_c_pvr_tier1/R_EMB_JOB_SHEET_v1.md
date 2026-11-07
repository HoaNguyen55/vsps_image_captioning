# Paper C (C-PVR-T1): R-EMB job sheet v1 — the pre-S11 E-G instance (embed + venv freezes + INFRA PROBE)

Status: DRAFT inside the R-P5b bundle (CC-280 WORK LIST 2b, AM5 as restated by AD2). Not judge-read, not committed.
Nothing here has been rented, pushed or run. Licence: PI-1106j (one pre-S11 RTX 3090, money inside C's block S).
Label of every host check: INFRA PROBE (PI-1106f form): no hostcheck output of this instance is a record for S12.
Placeholders: `ALIAS` = the ~/.ssh/config alias of the instance (no host, IP or port is written anywhere); `HEAD` = the
R-P5b commit; `B` = the laptop build dir `~/c_pvr_build_<MMDD>` (ext4); `PY` / `PYE` = the host main / EN venv python
(`~/venvs/c_pvr_gpu_966eb327/bin/python`, `~/venvs/c_pvr_llava_d2f0f262/bin/python`).

## 1. Preconditions (laptop; each a STOP if missing)

1. R-P5b GO and its gatekeeper commit = HEAD; `sha256sum -c` of scripts/c_pvr_gpu/SHA256SUMS, scripts/c_pvr/SHA256SUMS
   and scripts/c_en/SHA256SUMS all OK.
2. `queries ids` run at HEAD (`c_pvr_manifest.py queries ids --src <repo> --kept <c_datastores> --stage
   ~/c_pvr_dev_stage_1105 --out B/q`), its OPS-qtsv pin line logged (10 list shas + QTSV.sha256).
3. `queries images --q B/q --src <repo> --stage ~/c_pvr_dev_stage_1105 --to B/emb_push` (the 8 E-G lists: xm3600_vi
   3,600, ktvic_explore 286, openviic_explore 1,020, vitextvqa_dev 1,676, t_a 1,070, d_vi_kt 1,878, d_vi_ov 7,220,
   d_tc 20,842 = 37,592 files). **EMB_PUSH = sha256 of B/emb_push/MANIFEST.sha256**, pinned in an OPS line
   (`OPS-<MMDD>c-emb-push`: sha, 37,592 files, bytes, HEAD) BEFORE any push.
4. Money, L-before (host v3 §3): balance ≥ this instance's worst case (3.75 h × r, i.e. the 3.5 h hard stop + the
   0.25 h teardown overrun) + Σ R_j of every live rental (B included). Rental line with the offer values against
   GPU_RENTAL_SPEC (1× RTX 3090 / 3090 Ti 24 GB, CPU ≥ 5900X, RAM ≥ 32 GB, disk 200 GB ≥ 1000 MB/s, net ≥ 400 Mbps,
   CUDA ≥ 12.4, uptime > 99 %). The rental line's UTC stamp is **T0**; the hard stop is **T0 + 3.5 h**.
5. The 30-min backup loop for this instance has no /dev/shm path in it.

## 2. What may be on E-G (AM5)

| allowed | NOT allowed |
|---|---|
| the repo at HEAD (code only; git checkout or bundle) | any caption text; democap/*.json; manifest/*.json |
| weights: SigLIP2 `google/siglip2-so400m-patch14-384` @ e8e48729 (per-file sha = c_pvr_embed.py SNAP), mBLIP, S9 helpers, LLaVA files as setup_host.sh | KT-C or any COCO pixels (`push_rows` refuses a kt_c list) |
| /dev/shm/c_pvr_emb (0700): exactly B/emb_push (its MANIFEST.sha256 = EMB_PUSH and the 37,592 images) | the 981 OpenViIC / 272 KTVIC confirm-half images (NB-T2POOL, AM2); any t2pool_* file |
| /dev/shm/c_pvr_hc/kept: the 3 kept-id files + their MANIFEST.sha256, ONLY for the INFRA PROBE hostcheck (`--kept`) | NoCaps / OI-test material; old embeddings (emb_xm_*, emb_ov_test, c_stage1/emb.npz, emb_memory, emb_coco_test); the Q TSVs |

All images sit in /dev/shm only, sha-checked on arrival; logs hold ids and counts only; every tmpfs dir ends with a
logged wipe (`c_pvr_gpu.py wipe`, file count = manifest lines + 1, rc 0).

## 3. Order on E-G (AD2; times are billed time from T0)

| step | command (host unless marked) | output / check |
|---|---|---|
| 1 | checkout HEAD; `sha256sum -c` of the three SUMS | all OK, else STOP |
| 2 | `bash scripts/c_pvr_gpu/setup_host.sh main` | main venv from requirements_c_pvr_gpu.host.lock 966eb327 (--require-hashes --no-deps + cu124 index); installed closure = the file; freeze written to ~/c_pvr_out/gpu_lock_966eb327/freeze.sha256 and **must equal 9a074530** (setup STOPs otherwise: then pull the setup log, freeze and host.lock files, wipe, delete; the R-P6 reader rules, AM1) |
| 3a | `bash scripts/c_pvr_gpu/setup_host.sh siglip` | SigLIP2 snapshot at e8e48729, every file sha = SNAP, path in ~/c_pvr_out/siglip2_snapshot.path |
| 3b (parallel to 3a) | laptop: `ssh ALIAS 'mkdir -m 700 /dev/shm/c_pvr_emb'`; `tar -C B/emb_push -cf - MANIFEST.sha256 images \| ssh ALIAS 'tar -C /dev/shm/c_pvr_emb -xf -'`; then `ssh ALIAS 'cd /dev/shm/c_pvr_emb && sha256sum --quiet -c MANIFEST.sha256 && sha256sum MANIFEST.sha256'` | arrival: every file OK and the manifest sha = EMB_PUSH |
| 4 | in tmux: `HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 HF_HOME=~/c_pvr_models/hf $PY -I -B scripts/c_pvr_gpu/c_pvr_embed.py embed --push /dev/shm/c_pvr_emb --tman <EMB_PUSH> --snapshot "$(cat ~/c_pvr_out/siglip2_snapshot.path)" --out ~/c_pvr_out/emb > ~/c_pvr_out/logs/embed.log 2>&1` | 8 npz `emb_<list>.files.npz` (keys = file names) + .sha256; the arrival check is repeated in code (manifest sha, 0700, file set = manifest, E-G lists only, sha before open); an unreadable image = STOP |
| 5 | laptop: `scp 'ALIAS:c_pvr_out/emb/*' B/emb_eg/`; `cd B/emb_eg && cat *.sha256 \| sha256sum -c` | 8 npz pulled and verified |
| 6 | `$PY -I -B scripts/c_pvr_gpu/c_pvr_gpu.py wipe --dir /dev/shm/c_pvr_emb --log ~/c_pvr_out/c_pvr_emb_deletions.log` | rc 0 (37,593 files); the images leave the host right after the pull |
| 7 | `bash scripts/c_pvr_gpu/setup_host.sh rest` | EN venv (d2f0f262) freeze; mBLIP, S9 helpers, Q-LLAVA files by pin |
| 8 | laptop: push the 3 kept files + a `<sha256>  kept/<name>` MANIFEST.sha256 to /dev/shm/c_pvr_hc (0700); host: `mkdir -p ~/c_pvr_out/probe && cp ~/c_pvr_out/*_snapshot.path ~/c_pvr_out/probe/` (R-P6 erratum: hostcheck / hostcheck-en read `<name>_snapshot.path` from their --out; done this way on E-G, OPS-1107c-eg-done; c_pvr_job.sh already passes --out ~/c_pvr_out), then `$PY -I -B scripts/c_pvr_gpu/c_pvr_gpu.py hostcheck --mblip "$(cat ~/c_pvr_out/mblip_snapshot.path)" --kept /dev/shm/c_pvr_hc/kept --out ~/c_pvr_out/probe`; `$PYE -I -B scripts/c_pvr_gpu/c_pvr_gpu.py hostcheck-en --out ~/c_pvr_out/probe` | INFRA PROBE only (no S12 record) |
| 9 | `$PY -I -B scripts/c_pvr_gpu/c_pvr_gpu.py wipe --dir /dev/shm/c_pvr_hc --log ~/c_pvr_out/c_pvr_hc_deletions.log` | rc 0 |
| 10 | laptop: pull ~/c_pvr_out/{gpu_lock_966eb327/{freeze.sha256,requirements_c_pvr_gpu.host.lock,pip_report.json}, gpu_lock_llava_d2f0f262/freeze.sha256, logs/setup.log, logs/embed.log, probe/, *deletions.log} | the AM5 pull list |
| 11 | delete the instance; L-after; spent (panel per-instance figure or r × billed h) enters S | – |

**Hard stop T0 + 3.5 h** (PI-1106j upper estimate; AM5): whatever step runs, stop it, pull what exists (npz with their
.sha256 first, then the freeze / lock / log files), wipe every /dev/shm dir that exists, delete. Only this teardown may
run past T0 + 3.5 h, by at most 0.25 h. The order puts the embed and its pull (steps 2-6) first, so the stop can cut
only steps 7-9 (AD2).

## 4. Laptop after the pull (no host)

1. Rekey (file names → ids through the pinned Q TSVs), into B/emb (ext4):
   `c_pvr_embed.py rekey --name <set> --pair B/emb_eg/emb_<set>.files.npz B/q/<set>.tsv --out B/emb/emb_<set>.npz` for
   xm3600_vi, ktvic_explore, openviic_explore, vitextvqa_dev, t_a and d_tc; D-VI as one npz:
   `--name d_vi --pair B/emb_eg/emb_d_vi_kt.files.npz B/q/d_vi_kt.tsv --pair B/emb_eg/emb_d_vi_ov.files.npz
   B/q/d_vi_ov.tsv --out B/emb/emb_d_vi.npz`.
2. Parity anchor (CC-280 Ruling 2(d), AM2, AD4; PARITY_MIN = 0.995 in committed code):
   `c_pvr_parity.py check --new-xm B/emb/emb_xm3600_vi.npz --new-ov B/emb/emb_openviic_explore.npz --old-xm
   <M1>/c_stage2/emb_xm_dev500.npz <M1>/c_test/emb_xm_test2500.npz --old-ov <M1>/c_test/emb_ov_test.npz`
   (`<M1>` = .session_backup/machines/M1/root/outputs). rc 0 = PASS; rc 1 = STOP: the new npz files are not used, read.
3. OPS-emb pin line: the 7 new npz shas + def163d3 (D-EN) + 6e8bdba2 (KT-C) with n and meta (torch, transformers,
   dtype, snapshot map), the parity result line, both freeze shas and the host.lock sha with their source instance
   (AM8). The builder's `set --pins` file takes these shas.
