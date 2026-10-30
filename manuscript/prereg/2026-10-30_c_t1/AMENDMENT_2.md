# C-T1 AMENDMENT 2: B3_lmcap_ri_ovb stopped at the XGLM load; load the same weights from safetensors and rerun B3

Amends PREREG.md (sha f1d06278, unchanged) and AMENDMENT_1.md (sha 84665ee1, unchanged). Written 2026-10-30 after the
job stopped. Tier 1 (DEV-EXPLORE) only. AI opinion, not expert-validated. Judge: CC-185 GO-with-fixes 93% (single judge,
reversible tier ≥ 90, PI-1029o); its W1-W4 are applied in this text. No pred, caption text or score was opened for this amendment. Code (c_t1.py 022af90e,
c_t1_job.sh 86351ee1), the registry (c_t1_registry.json 09e6f90a), venv-t1 (T1_FREEZE 1766dc23) and every decision rule
are unchanged.

## 1. What happened

| UTC (2026-10-30) | Event |
|---|---|
| 02:57:19 | START B3_lmcap_ri_ovb (left 1036 min) |
| 02:58:04 | JOB STOP B3_lmcap_ri_ovb rc=1 |

`logs/B3_lmcap_ri_ovb.log`: c_t1.py:469 `XGLMForCausalLM.from_pretrained(a.xglm, torch_dtype=torch.float16)` →
transformers `load_state_dict` → `check_torch_load_is_safe()` → ValueError (CVE-2025-32434: transformers 4.57.6 refuses
`torch.load` of a `.bin` checkpoint unless torch ≥ 2.6, even with `weights_only=True`).

**Root cause.** venv-t1 (= venv-lb freeze + open_clip_torch 2.32.0 + ftfy 6.3.1 + wcwidth) has torch 2.5.1+cu121 and
transformers 4.57.6 (read on M1). The registry pins XGLM-2.9B at revision 33c659ae, whose only weight file is
`pytorch_model.bin` (sha256 9aa29d66). With this torch, transformers can never load it. The smoke step S_lmcap that
should have caught this failed earlier at c_t1.py:435 on the caption-store wrapper (CC-179). That error masked this
one: S_lmcap never reached line 469.

**Scope: only XGLM, so only the four B3 steps.** Weight files of every model a remaining step loads (M1, read only):

| Step(s) | Model | Weights | Loader | Affected |
|---|---|---|---|---|
| B3 ri/se × ovb/carve | XGLM-2.9B | `pytorch_model.bin` | transformers | **yes** |
| B3 (all) | M-CLIP H-14 | `open_clip_pytorch_model.bin` | open_clip's own `torch.load` (no transformers check) | no: it built on GPU in this step (c_t1.py:438-467 ran before 469), and t1check passed |
| B3 (all) | xlm-roberta-large | config and tokenizer only; text weights come from the M-CLIP checkpoint | open_clip | no |
| B4, B5, B6, B7 | qwen25vl_7b, internvl3_8b, aya_vision_8b | `model-*.safetensors` | transformers | no |
| B7 embed | SigLIP2 | `model.safetensors` | transformers | no |

## 2. The fix (staging only)

The same XGLM weights in safetensors format go into the pinned snapshot directory. HF repo `facebook/xglm-2.9B`
has `refs/pr/2` (commit e16cf0213968ba3cb613ec070a3cff7c1e5ffd8d, 2023-06-12, "Adding `safetensors` variant of this
model", SFconvertbot, open and unmerged). It is one commit on top of the pinned 33c659ae. Its tree (HF tree API,
unauthenticated) carries every pinned file with the same hash, including `pytorch_model.bin` 9aa29d66, and adds
`model.safetensors`, sha256 **9e2926577049a20960ead82d1ebe5ce04d498f450ca53e5c1fb0993c4fc7d8de** (5,883,096,008 B).
The PR is not from Meta. It is accepted only because of the tensor-equality proof below.

**Proof (M1, CPU only, scratch dir outside every C-T1 readable root; no token).** `verify_xglm_st.py` (sha 5d09e549),
result `verify.json` (sha bc51943a); both are kept in `.session_backup/2026-10-30/c_t1_amend2/`.
- Both file shas equal their pins (bin 9aa29d66, safetensors 9e292657).
- `torch.load(bin, weights_only=True)`, called directly in the verification script only (never in the job), gives 772
  tensors, all float16. The safetensors file holds 771: every common tensor has the same dtype and shape and is
  `torch.equal`. The only key not in it is `lm_head.weight`, which is tied to `model.embed_tokens.weight`.
- `XGLMForCausalLM.from_pretrained(<safetensors dir>, torch_dtype=float16, use_safetensors=True)`: all 772 bin tensors
  are in the model's `state_dict` and bit-identical, `lm_head.weight` included. The model has no extra keys. PASS.
- With both `pytorch_model.bin` and `model.safetensors` in one directory, the job's unchanged call (no
  `use_safetensors`) loads in venv-t1. transformers prefers safetensors, and the `.bin` path would have raised. A CPU
  generate (beam 3, 3 returned sequences, synthetic text prompt, no data) ran with the pinned tokenizer files
  (XGLMTokenizerFast).

**Why no code or registry change.** `check_snapshot` checks that the 7 pinned files are present with their hashes.
They stay present (the `.bin` included), so `pinsok` and the B3 `check_snapshot` pass unchanged, and the load picks the
added safetensors file. Editing `c_t1_registry.json` would break A-T3: `a_t3.py` pins it at 09e6f90a (SOURCES, and
its selftest compares the Aya block). Editing c_t1.py would change the `c_t1_sha256` that the B0-B2 preds record.
The new pin is therefore enforced by the operator sha checks in §4 (S3, S8), not by the job's code. This ceiling is
disclosed (§6).

**Ranked alternatives, not taken.**
- (b) Local `.bin` → safetensors conversion: same proof needed, and the file is not one anyone else can fetch.
- (c) torch ≥ 2.6 in venv-t1: changes T1_FREEZE and the torch under M-CLIP and the CUDA stack mid-run.
- (d) The transformers safety bypass: refused while (a) exists.

## 3. Ledger and lock

- `gpu()` closed the step itself: `gpu_seconds.tsv` holds `B3_lmcap_ri_ovb start 1793329039` and
  `B3_lmcap_ri_ovb 45` (34 lines, sha 57c16f82, last byte LF). The 45 s are charged as logged. They were GPU time:
  M-CLIP was loaded and the memory and shots were encoded. No line is added or edited, unlike CC-177 and CC-180.
- The job left through `stop`, so the EXIT trap removed `RUNNING`; it is absent. CAP_STOP.json is absent. No tmux
  session or c_t1 process is live, and the GPU is idle.
- `cmd_lmcap` writes its preds only at the end and keeps no partial. `out/` and `smoke/` hold no `lmcap` file, so
  there is nothing to resume. B3_lmcap_ri_ovb has no `.done`.

## 4. Relaunch (same output dir, same host m3 = M1)

C-T1 runs on M1 (machine id m3) under CC-176. PREREG l.160 allows no retry of a failed step except resuming its own
partial. This amendment authorises exactly one outcome-blind rerun from scratch of B3_lmcap_ri_ovb under the fix, and
first runs of the B3 se/carve steps on the same file (CC-185 r1). It sets no precedent for rerunning a step that wrote
output or whose output was seen. The steps that follow are new runs. Steps with `.done` (B0, the
smoke steps, B1, B2) are skipped. As on every launch, `draws`, `vicheck`, `score` and `select` rerun (CPU).
1. The gatekeeper commits this file and the regenerated `manuscript/prereg/2026-10-30_c_t1/SHA256SUMS` (6 entries).
   That commit is the new EXPECT HEAD. It is shipped to M1 as a bundle (as `c_t1_a03d3d2.bundle`) and checked out;
   `git diff --quiet HEAD` must hold.
2. Before launch, check that no tmux `c_t1` session, c_t1 process, GPU compute process, `RUNNING` or `CAP_STOP.json`
   exists. Record the shas: `out/x1_ov_dev_b.json` 3b633827, `out/x1_ktvic_dev299.json` 2ebac15c,
   `out/x1_f30k_carve_coco.json` 4a80ee50, `t_config.json` 948165b8, `gpu_seconds.tsv` 57c16f82, and require
   `$NCS_DATA/datasets/c_t1_mem/coco_captions.json` = 9c830e22 (the CC-179 flat store; CC-185 W1). Before step 2:
   `git diff --name-only a03d3d2..<new HEAD>` touches no C-T1 code, imported module or this prereg dir other than this
   file and SHA256SUMS (CC-185 W2). Before step 3: the guard dry run and the N5 inventory confirm that
   `/root/a_t3_m3` (A-T3 images) is under no guard root, no c_t1 command-line path and not under $NCS_DATA
   (CC-185 W3); otherwise stop.
3. `mv /root/scratch/amd2_xglm/st/model.safetensors $NCS_DATA/models/c_t1_xglm_2_9b/` (same filesystem, a rename),
   then `chmod 444` it, then `sha256sum` it: it must be 9e292657 (§2). The 7 pinned files are not touched, and
   `pytorch_model.bin` stays. `HF_HUB_OFFLINE=1 /root/venv-t1/bin/python -I -c` with
   `decode_hf_vlm.check_snapshot(registry xglm_2_9b, $XG)` must pass. Then delete `/root/scratch/amd2_xglm/both/`
   (symlinks only).
4. Launch in tmux `c_t1`: `T1_FREEZE=1766dc23a71509ba4fb6b8adb34b1999a3a2bf78ebe1e227730fd6647bea3599 bash
   scripts/c_t1/c_t1_job.sh <new HEAD>`. The preflight re-checks HEAD, both SUMS, RESTORED_SHA256, both freezes,
   both selftests, the guard, memcheck, pinsok and t1check.
5. Expect, in order: `JOB START head <new HEAD>`; `THIRD BACKBONE aya_vision_8b k=4 order=last tpl=T1 tau=-inf`;
   `START B3_lmcap_ri_ovb (left 1035 min)` (±1). After the rerun's `draws`/`select`, the 4 shas of S2 (x1 files,
   t_config) are unchanged.
6. **Stop and ask the judge (blocking):** if any S2 sha differs, the THIRD BACKBONE line differs, a B2 step or any
   finished step starts again, or `B3_lmcap_ri_ovb.log` shows the CVE ValueError or a load of `pytorch_model.bin`.
   Any further B3 failure is a JOB STOP under PREREG l.160 and comes back to the judge; it is not retried here.
7. One OPS LOG line with S2-S5 values (step names and shas only).
8. When the job ends (DONE, CAP STOP or STOP), check `model.safetensors` again (sha 9e292657) and log it.

## 5. What does not change

Every threshold, rule and SESOI stays as written: SESOI +2.0 PTB CIDEr-D; the NOMINATE/WATCH/DROP labels; the kill
gate; the tier-2/tier-3 rules; the third-backbone order; the 0.95 Vietnamese check; C's stage-A selection rule; the
arms, templates, blocks and priority; the LMCap specification (PREREG §4: K = 4, N = 3, XGLM-2.9B fp16, beam 3,
M-CLIP re-rank, 40 new tokens); the 20 GPU-h hard cap with stop order B7 → B6 → B5; the scoring commands and the
honesty notes. The XGLM weights are bit-identical to the pinned ones (§2). Only their file format changes.

## 6. Disclosure (tier-1 write-up and run record)

- B3_lmcap_ri_ovb failed once at the XGLM load (45 s charged), with no output. It was rerun from scratch under this
  amendment.
- XGLM-2.9B was loaded from `model.safetensors` (refs/pr/2 e16cf021, sha 9e292657), which holds weights bit-identical
  to the pinned `pytorch_model.bin` 9aa29d66 at revision 33c659ae (§2 proof). The registry still names 33c659ae and
  the `.bin`. The safetensors pin is enforced by operator sha checks before and after the run, not by `check_snapshot`.
- S_lmcap never measured LMCap's rate (CC-179 r3). The CC-179 r4 LMCap rate substitute is the rerun's own closing
  ledger line for B3_lmcap_ri_ovb (the last such line), never the 45 s line and never their sum (CC-185 r6). The cap
  counts both closed lines.
- The run spans two HEADs: B0-B2, the smoke steps and the 45 s attempt ran at a03d3d2; the rest runs at the HEAD that
  commits this file. c_t1.py, the job and every imported module are byte-identical across both (CC-185 r5).
- Residual risk: the LMCap code after c_t1.py:469 (fp16 CUDA generate and M-CLIP re-rank) runs for the first time in
  this rerun. The CPU check covered only the load and an fp32 generate.
- M-CLIP's `open_clip_pytorch_model.bin` is still unpickled by open_clip under torch 2.5.1. Mitigation: its sha256 pin
  (ee81ce53), checked before every load.
- Host-rebuild note (with CC-178 N1): a rebuilt m3 needs `fetch` for XGLM plus `model.safetensors` from e16cf021 and
  the sha check of S3. A registry pin is not pre-approved (CC-185 r3): any later pin goes in a sidecar or
  addendum file that leaves the registry (09e6f90a) and a_t3.py untouched, and needs its own ruling. After C-T1, add
  the missing smoke coverage (an S_lmcap that reaches the generator).
