# C-T1 AMENDMENT 1: run the tier-1 job on M1 (machine id m3) with read isolation

Amends PREREG.md (sha256 f1d06278, unchanged). Written 2026-10-30 before any C-T1 GPU step. Nothing has been decoded or
scored, and no output exists. Tier 1 (DEV-EXPLORE) only. This is AI opinion, not expert-validated. Judge: CC-176
(single judge, reversible tier ≥ 90): GO-with-fixes 91%, on M1; W1-W4 are applied in this text
(W1 filled at the venv-t1 rebuild on the new m3 host, 2026-10-30).

## 1. Why

M1's GPU has been idle since 2026-10-29T19:48:56Z, and the standing rule is to keep the GPU queue full. M2 (m4) runs
L1-b until about 00:30Z and then BD-T1 for about 10 GPU-h. The PREREG ties the job to m4 in three places: §2 custody
("only that .tar goes to M2"), §5 ("one machine (dev role, machine id m4)", "Queue and staging on M2") and §10 ("dev
role only"). M1 is the test-capable role (m3). By design it also holds files that tier 1 must never read: the
Flickr30K zip with the val and test images, ADE20K validation (A-T1), C's spent test-side records and others. The
m4-only rule was a custody device. It made test files unreachable because they were absent. This amendment swaps
absence for an enforced read boundary that is just as strong for Python-level opens under $NCS_DATA and
/root/outputs; paths outside both roots are not fenced, and native or child-process opens are not seen (§4).

## 2. What changes (only these)

1. **Machine.** `c_t1_job.sh` accepts machine id m3 or m4 and exports the actual id. Everything else in the preflight
   is unchanged and runs in the same order: HEAD and SUMS, venv freezes, selftest in venv-lb and venv-c1score,
   custody guard, memcheck, pinsok, t1check.
2. **Read isolation (new, `c_t1.py` `iso_*`).** On a GPU host (m3 or m4), every data command (`draws embed decode
   lmcap score select vicheck memcheck t1check pinsok cfg`) runs under a Python `open()` audit hook. The hook covers
   builtins, io and `os.open`, and resolves symlinks first. It raises PermissionError for (name rules on the basename as requested AND as resolved,
CC-176 W2):
   - any file whose name is one of the 2,014 Flickr30K val/test names in `c_t1_f30k_lists.json`;
   - any `*.zip`, `*.tar`, `*.tar.*`, `*.tgz` or `*.7z` (N6);
   - any path under `$NCS_DATA` outside `datasets/{ktvic, openviic, c_t1_f30k_carve, c_t1_f30k_memory, cen_memory,
     c_t1_mem}`, `models/` and `vncorenlp/`. This denies, for example, `f30k_raw/` (the zip) and `ade20k_raw/`;
   - any path under `/root/outputs` outside `/root/outputs/c_t1` and the 6 files of `RESTORED_SHA256`. This denies,
     for example, `c_en/emb_coco_test.npz`, `c_en/ex_coco_test.json`, `c_test/` and `k2_gate1/`.
   `extract` (the only command that opens the zip), `lists`, `store`, `memfiles` and `fetch` are not hooked; none is a
   data command of the job.
3. **Guard scope.** `guard` scans the job's readable roots under $NCS_DATA and /root/outputs, plus the HF hub cache: `$NCS_DATA/datasets`, `$NCS_DATA/models`,
   `$NCS_DATA/vncorenlp`, `/root/outputs/c_t1` and the HF hub cache. It no longer scans the whole of
   `$NCS_DATA` and `/root/outputs`, where M1's quarantined zips would always fail it by design. It also refuses:
   - any entry of `$NCS_DATA/datasets` other than the six C-T1 dirs (`--images $DS` makes `datasets/` readable);
   - any symlink inside those roots that resolves to a denied path.
   The PREREG's archive, `flickr30k-images*` and val/test-name checks are unchanged.
4. **Flickr30K val/test images stay unreadable.** The images never exist as files. `extract` reads only the
   1,000 carve and 28,000 memory members, by list, and the val/test members stay inside the zip. The zip lives in
   `/root/ncs-data/f30k_raw` (quarantine, outside every readable root). The hook denies that dir, the zip's name
   (`*.zip`) and every val/test file name. The guard refuses all three inside the readable roots.
5. **Selftest (new block, must pass in both venvs).** It builds a synthetic `$NCS_DATA` and `/root/outputs` with a
   carve image, a model file, a restored file, an own output, a zip in `f30k_raw`, an ADE20K file, a test-side `c_en`
   file, a `c_test` file, a val/test file name, an archive, a symlink from the carve dir into `f30k_raw`, and two
   symlinks with a refused name (`v1.jpg`, `flickr30k-images.zip`) that point to an allowed file (W2). It
   asserts:
   - `iso_denied` allows exactly the first four, plus a path outside both roots, and denies the rest, including all
     three symlinks and the `.tar.*` / `.7z` forms;
   - the guard flags the symlink and an extra `datasets/` dir;
   - in a child process with the hook installed, `open()` and `os.open()` succeed on exactly the allowed files and
     raise PermissionError on every denied one;
   - the live config (from `RESTORED_SHA256` and the lists) has 6 restored files and 2,014 refused names, denies
     M1's real quarantine, ADE20K, `c_test`, `c_en` test-side and `c_stage2/runs` paths, and allows the staged ones.
6. **Queue text (§5 W5) on M1.** C-T1 runs on M1 (CC-174 r5 and OPS-1030d queue it there; CC-176 r1). CC-172 W5
   bullet 1 ("only after BD-T1 tier 1 has finished") is overruled for a run on M1 only (CC-176 r3, separate hosts);
   it binds again if C-T1 moves back to M2. The rest of W5 and the CC-171 r1 disclosure sentence bind. K1/K6 tier 1
   (CC-175) does not pre-empt C-T1 and starts after C-T1 is done and cleaned up (CC-176 r4). The pre-emption rule is unchanged. If an A or B job is ready
   for M1, C-T1 stops between steps and resumes from its `.done`/partial files. BD-T1 stays on M2, and the two jobs
   never share a machine, so BD-T1's `*openviic*` refusal is not affected. After C-T1, `ktvic/` and `openviic/` are
   deleted from M1's `datasets/` (logged).

## 3. What does not change

Every threshold, rule and SESOI stays as written in the PREREG: SESOI +2.0 PTB CIDEr-D, the NOMINATE/WATCH/DROP
labels, the kill gate, the tier-2/tier-3 rules (val PASS, the Fréchet P(PASS), Holm at α = 0.05), the third-backbone
order and the 0.95 Vietnamese check, C's stage-A selection rule, the arms, templates, blocks and priority, the 20 GPU-h
hard cap with stop order B7 → B6 → B5, the scoring commands and the honesty notes. Flickr30K val and test remain
refused in tier 1. No spent test set is decoded, scored or staged.

## 4. Known ceiling (disclosed)

The hook sees Python-level opens only. Native-code opens (safetensors and tokenizers in Rust) and child processes
(the VnCoreNLP segmenter) are not seen. They receive only the registry's model paths and the staged reference files,
and the guard scans those dirs. The real guarantee for the Flickr30K val/test images is that they are never written
as files.

## 5. Staging on M1 (LOG OPS-1030g, before this amendment; ratified as a logged departure, CC-176 r8)

M1 was lost on 2026-10-30 at about 04:30 VN (OPS-1030h/i). Only the shas below survive, and the staging is redone
on the new m3 host. `extract` is deterministic by list, so it must reproduce manifests 79c41b1d / c0d0084f.

- zip fetched at the pinned rev (sha 2ce2420c) into the quarantine dir;
- `extract` → train-only tar 93282dd4 → carve and memory images (sha = manifests), then the tar was deleted;
- caption stores and memfiles built on the laptop (`store`, `cen_memory.py store`, `memfiles`);
- the Vietnamese images were staged by list: 9,414 files = dev299, OV-dev-B and the 8,190 memory representatives,
  each with a sha check. Under C's stage-2 host rule, 0 are refused: the 925 OV-dev-B images are C's carve-out,
  and 57 KTVIC names only coincide with OpenViIC test names. They were staged with KTVIC `train_data.json`, OpenViIC
  train and the 1,836-key OV-dev subset 550cfe06. No test annotation file was staged;
- the 111,927 COCO memory images were staged per file, each with a sha check against `memfiles_coco.json`;
- models: `fetch` for xlm-roberta-large, M-CLIP and XGLM. idefics3_8b was hard-linked from the L1-b snapshot and
  `check_snapshot` passed. The C backbones and SigLIP2 are reached through logged symlinks;
- venv-t1 was built as the venv-lb freeze plus open_clip_torch 2.32.0 and ftfy 6.3.1 (`--no-deps`). Its freeze sha
  is in the LOG as `T1_FREEZE` (W-b). venv-t1 also pins wcwidth==0.2.13, ftfy 6.3.1's declared dependency, which it needs
  at import; environment-only, no rule change (PREREG §11 W-b). CC-176 W1: the freeze = the 45 lines of 2cb23ab9
  plus that one line, and nothing else; T1_FREEZE = 1766dc23a71509ba4fb6b8adb34b1999a3a2bf78ebe1e227730fd6647bea3599;
  `python -I -c "import ftfy, open_clip"` offline OK.
- Aya-Vision-8B: the PI accepted its HF gate (PI-1030a). It stays first in §6.1. Its 5 null sha256 pins are filled
  from the authenticated tree API in a separate gate commit (PREREG W-a; HF token per command, never stored), and that
  commit must be inside the launch HEAD; with the pins still null, `pinsok` skips it (never a STOP). Gemma-3-4B
  (4 null pins) is skipped. idefics3_8b remains fallback 2. If no backbone passes §6.2, the third backbone is reported
  NOT RUN and the other blocks run (N8).
