# Judge read request: VSPS H1 AMENDMENT 1 (Phase A all-GPU on m5)

One judge. Tier REVERSIBLE (dev-explore pilot on train), bar >= 90. Draft, not committed.

Subject: `AMENDMENT_1_GPU_M5.md` (this folder) against PREREG.md 7411957a (commit 07fd1d5), CC-198 ruling 7, CC-201.
PI direction: Phase A on a separate rented RTX 4090 (`m5`) today (PI message 2026-10-31 ~10:30 VN).

Please rule on:
1. Does the m5 run meet the PREREG §8 PI-override conditions (all-GPU, cap 4 GPU-h, 50-image projection, upload list,
   replay and funnel on the laptop)? Is anything in §5 or the detector pins changed?
2. A3: is killing the laptop CPU run (pid 3176610) by exact PID and archiving its partial file unread, with only
   sha/size/lines disclosed, enough? Is the GPU file as the only vote.py input clean?
3. A5: is the measured GPU-vs-CPU difference (0 count/presence flips on 5 images, at most 0.64 px and 0.0071 score, 1 top-box
   order swap) adequately disclosed, with no correction?
4. A6: accept the filename-only stubs, including the 558 KTVIC test filenames (no captions, no images), as staging outside
   the literal §8 upload list? Recommended: yes. Alternative: an empty test stub (weaker guard).

Checks the judge can re-run on the laptop: `sha256sum -c` in scripts/vsps_h1; the two smoke files named in A5 (laptop copy of the
GPU smoke: `~/vsps_h1_runs/smoke_gpu/boxes.jsonl`; m5 manifest copy beside it); `ps -p 3176610`. On m5: `sha256sum -c /root/vsps_h1_MANIFEST.sha256`
from `/root/vsps_h1`.

Default if no ruling: the run does not start.
