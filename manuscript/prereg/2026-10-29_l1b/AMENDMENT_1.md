# L1-b AMENDMENT 1: rerank crash (Qwen2.5-VL M-RoPE) and idefics3 parity failure (bf16), before any score

Amends PREREG.md (sha b6034c4a, unchanged) under its §4.4 "code-fix re-run" clause. Written 2026-10-30, before
`score` has run. Tier 1 (DEV-EXPLORE, ViTextVQA dev half E only). AI opinion, not expert-validated. Judge: CC-173
(single judge, reversible tier ≥ 90): GO-with-fixes 91%. W1–W4 and W7 are applied in this text.

## 1. What happened (job at 58160ccf on M2, machine id m4)

| UTC (2026-10-29) | Step | Result |
|---|---|---|
| 16:57:17 | JOB START, gemma3_4b skipped (P2b) | |
| 16:57:18–17:39:55 | dec_idefics3_8b (2,557 s) | OK, 2,210 answers, sidecar written |
| 17:39:56–17:40:52 | rr_idefics3_8b (56 s) | PARITY FAIL (rc 3), max \|cached − full\| per item 0.172 / 0.313 / 0.746 / 0.375 nats, tol 0.25 |
| 17:40:53–17:41:29 | rr_qwen25vl_7b (36 s) | JOB STOP rc 1: RuntimeError in qwen2_5_vl `position_ids + delta` (6 vs 16 at dim 2), first batch of item 0 |

internvl3_8b and qwen3vl_8b never started. No `score` has run (`.session_backup/2026-10-29/l1b/decide.json` does not
exist), and no rerank output was pulled to the laptop.

## 2. Root causes (debug on M2, first 4–24 E items, scores only)

**A. Qwen2.5-VL crash: a code bug (ours, triggered by transformers 4.57.6).** M-RoPE keeps per-sequence prefix
state outside the KV cache: `rope_deltas` (shape (1, 1) after the batch-1 prefill). `score_cached` repeated the KV
cache to the candidate batch B but not `rope_deltas`. In transformers 4.57.6, `Qwen2_5_VLModel.forward` then does
`delta.repeat_interleave(B // 1, dim=1)` on the (1, 1) delta, which gives (1, B), and that cannot be broadcast against
the (3, B, L) position ids. qwen3_vl's copy of the code repeats on dim 0 and does not crash, but it relies on the same
unexpanded state. A tiny random Qwen2.5-VL (rope delta −2) reproduces the crash with the 58160ccf code under 4.57.6.
The selftest's tiny LLaVA has no M-RoPE, so the CPU selftest could not catch it.

**B. idefics3 parity failure: bf16 numerics, not a cache bug; the 0.25-nat tolerance was miscalibrated.**
- With the unchanged 58160ccf `score_cached`, idefics3_8b in **float32** (GPU + CPU offload) gives
  max \|cached − full\| = 0.00012 and 0.00020 nats on items 0 and 2 (item 2 is the worst bf16 item, 0.746).
- In bf16 the gap is the same size with batch 1 as with batch 8 (item 2: 0.69 vs 0.75), so batching is not the cause.
- The full forward is reproducible (adding 5 padding tokens changes it by 0.0000). The gap comes from the two bf16
  kernel paths (prefill + cached step vs one long causal pass), and part of it is bf16 logit rounding (per-token
  steps of 1/16 and 1/8 nat). An fp32 LM head removes only 10–50% of it.
- The gap varies from run to run (non-deterministic bf16 kernels). It grows with answer length (≤ 0.25 nat for
  3–6-token answers, 0.4–0.97 nat for 11–13 tokens).
- All four backbones show it at bf16, at the registry batch sizes, with the fixed code (§3), as max over the 4 parity
  items: qwen25vl_7b 0.150–0.208, qwen3vl_8b 0.415, internvl3_8b 0.240–0.296, idefics3_8b 0.746 (0.971 in one
  bf16-logit re-run).
- **A real position bug is 1–2 orders of magnitude larger.** Forcing the Qwen2.5-VL rope delta to 0 (a deliberate
  M-RoPE bug) gives 16.0 / 24.9 / 25.8 / 31.0 nats on the same 4 items.

**C. A latent crash in `candidates()` (found while re-estimating the budget).** `variants()` returned no variants
only for syllables with no vowel letter. A bare "qu" syllable has a vowel letter (u), but `tone_pos()` treats it as
the consonant glide, finds no tone-bearing vowel, and returns None, so `w[None]` raised TypeError. It occurs in exactly
1 of the 2,210 idefics3 first-pass answers and in 0 of the 3 × 2,210 Qwen-family answers. The idefics3 rerank would
have stopped there.

## 3. The fix (scripts/l1b/l1b.py 58160ccf d312c128 → 391f1e88)

1. **`score_cached`:** after the prefill, the model's `rope_deltas` (on `net.model` in 4.57.6, on `net` in 4.51.3;
   None for 1-D RoPE models) is saved. Before each candidate batch it is set to `rd.repeat_interleave(B, 0)`, so it is
   expanded with the cache. This is per-model prefix-state expansion, no cache-free fallback. idefics3 and InternVL
   (1-D RoPE) are unaffected.
2. **`PARITY_TOL` 0.25 → 2.0 nats** (summed log-likelihood, same 4 items × 8 candidates, img arm). 2.0 is about 2× the
   largest bf16 gap seen (0.97) and one eighth of the smallest deliberate-bug gap (16.0). The gate keeps its purpose
   (catch a wrong position, mask or cache) and stops failing on bf16 path noise. **Disclosure:** the value was chosen
   after seeing the parity gaps of these 4 items. The gaps are gold-free, and no outcome was seen (§4).
   **Sensitivity floor (CC-173 W3):** at 2.0 the gate catches gross (≥ about 2 nats) position, mask or cache errors,
   not subtle ones. The deliberate-bug probe covers Qwen2.5-VL M-RoPE only, and the fp32 control covers idefics3 only.
   InternVL3 and Qwen3-VL have neither.
   **Limitation (CC-173 W4):** bf16 path noise of up to about 1 nat on the summed log-likelihood of long answers is the
   same size as τ ∈ {0, 0.5, 1}. Its effect on selection was not measured. It mostly adds random flips, which the harm
   guard counts and which push toward KILL. It is reported as a limitation of the rerank.
3. **`variants()`:** a syllable whose unmarked base letters have no tone-bearing vowel (`tone_pos` is None, i.e. a
   bare qu-) gets no variants, like a vowel-less syllable (PREREG §4.2 "no vowel"). On the 3 Qwen-family E answer
   files, old and new `candidates()` give identical candidate lists on 2,210 / 2,210 answers each (cand_sha). On the
   idefics3 file: 2,209 identical, 1 that crashed before.
4. **`check_prov` / `score`:** `REUSE_DEC` pins the reused idefics3 decode (§5). A non-Qwen decode is accepted only
   if its file sha equals the pin, and then its header's `l1b_sha256` must equal the pinned writer (d312c128). Any
   other decode written by an earlier l1b.py is refused.
5. **Selftests (48 ok on M2 under .venv 4.51.3 and venv-lb 4.57.6; 46 on the laptop, which has no torch):**
   - tiny Qwen2.5-VL with a non-zero rope delta: cached batches (3 + 1) = full forward < 1e-4 nats (it crashes with
     the old code under 4.57.6);
   - bare qu- gets no variants;
   - score accepts the pinned reused decode and refuses an unpinned one.

**Unchanged:**
- PREREG.md, registry, split, prompt and batch sizes;
- `cmd_decode` (the diff does not touch it), `choose`, `outcome` and `score`'s analysis;
- l1b_job.sh (3c260686), so the reused decode's `job_sha256` header still matches;
- the selection grid and every decision rule.

## 4. No outcome seen

- `score` has not run. It runs on the laptop only, once, after the job has finished.
- No gold is on M2. The debug scripts printed only parity gaps, candidate counts, token lengths and timings.
- No first-pass answer text and no rerank score file was opened by a person or an agent. The idefics3 decode file
  was read by code only (to build candidates), and no answer string was printed.
- The 4 rows written by the failed idefics3 rerank and the header of the qwen25 rerank are superseded unread (§6).

## 5. Reuse of dec_idefics3_8b

`out/l1b_idefics3_8b_img.preds.json`:
- sha256 **ec3f8478e1f28b02460318e8435bf53160bd09b81cce252669da00370b3b4426**, which equals its sidecar;
- header: `l1b_sha256` d312c128, `job_sha256` 3c260686, split b749f720, prereg b6034c4a, git_head 58160ccf,
  n 2,210, revision fddb4ff7.

It is reused as is:
- the job skips the decode when the sidecar exists;
- `rerank` checks the sidecar;
- `score` checks the pin (§3.4).

The decode depends only on `cmd_decode`, the l1a prompt, the pinned items and the decode harness. None of these
changed. Re-decoding would cost 0.71 GPU-h, and it could even differ, because bf16 kernels are non-deterministic.

**Departure (CC-173 W2):** this narrows PREREG l.395 ("a code fix ... re-runs **all** backbones") and CC-168b W17
option (a). It takes W17 option (b), a pin on one file's sha and its writer's sha, and applies it to the idefics3
decode only. Every rerank, of all four backbones, is re-run.

## 6. Superseded files (moved before the relaunch, scores only, never read)

They move from `/root/outputs/l1b` to `/root/outputs/l1b/superseded_58160ccf/`, outside `out/` and `logs/`, so they
are not in the new SHA256SUMS and do not block the new run key:

| File | sha256 |
|---|---|
| out/l1b_idefics3_8b_PARITY_FAIL.json | 1acd933e428690ab2e1a621148b544266d031ccb29a37757f2264cb6e9418b89 |
| out/l1b_idefics3_8b_rerank.jsonl (header + 3 rows) | faf7cbc17660670fe89383a6f246342d98eb08391ced7e5e38759828b5eeefb1 |
| out/l1b_qwen25vl_7b_rerank.jsonl (header only) | 3697e9e5f4d78a5131324121c447b5adcf66b342ae2337e84f67d0c76371e1eb |
| code_at_start.sha256 (58160ccf run; copied, then overwritten by the relaunch) | acf23ae359c23c0e766cf30fd6565a01e84181f6ce70e7af8f2bbbc7db368e57 |
| logs/job.log at the stop (copied; the relaunch appends) | f1e83cb7eaff42937c5c52e3a08ea3913862d1ee764c985767564f66b21a00b4 |

The decode `.partial.jsonl` (22f20b24) stays in `out/`. finish() leaves it out of the sums.

## 7. GPU-h

**Already charged** (`gpu_seconds.tsv`, kept): dec 2,557 s + rr_idefics3 56 s + rr_qwen25 36 s = 2,649 s = **0.74 h**.

**Debug** (2026-10-29 17:54:32–18:26:50 UTC, wall span): 1,938 s = **0.54 h**. It is charged to the same cap by one
line `debug_amend1 1938` appended to `gpu_seconds.tsv` before the relaunch. Charged total: **1.27 h**, left 6.73 h.

**Re-estimate** (fixed code, measured at registry batch sizes on E items 4–23, both arms, scaled by the all-E mean
candidate count):

| Backbone | s/item | Estimate |
|---|---|---|
| qwen25vl_7b | 1.65 | 0.88 GPU-h |
| qwen3vl_8b | 2.05 | 0.95 GPU-h |
| internvl3_8b | 2.36 | 1.09 GPU-h |
| idefics3_8b | 3.29 | 2.20 GPU-h |

With 4 loads and parity (≈ 0.1 h) the remaining work is ≈ **5.3 GPU-h**. Total ≈ 6.6 of 8. **The hard cap stays
8 GPU-h** (CAP_S unchanged). A timeout stays a final CAP STOP: the reranks done by then are scored, and the
unfinished one is NOT_ASSESSABLE (CC-168 W4a).

## 8. Relaunch (same run, same output dir)

1. Gatekeeper commit of l1b.py, scripts SUMS, this file and prereg SUMS. Push.
2. Move M2 to the new HEAD by git bundle (ff-only, clean tree, all three SUMS OK).
3. Move the §6 files, then append the debug line to `gpu_seconds.tsv`.
4. Run `bash scripts/l1b/l1b_job.sh <new HEAD>` in tmux `l1b`. Order:
   - gemma skipped (P2b);
   - idefics3 decode skipped (sidecar);
   - reranks: idefics3_8b → qwen25vl_7b → internvl3_8b → qwen3vl_8b.

Every backbone's rerank is re-run (PREREG §4.4/W17). The one departure is the reused idefics3 decode (§5, W17 option
(b) for that file only).
- A parity failure at tol 2.0 is final NOT_ASSESSABLE. This run gets no AMENDMENT_2 for parity.
- Any rc other than 0, 3 or 124 is a JOB STOP back to the judge (CC-173 W7).

## 9. Pins

- `scripts/l1b/l1b.py` 391f1e88599fc70872ef62b8619f79ee7313e01186b87509489c80819f4c861a; scripts/l1b/SHA256SUMS
  regenerated (8 entries).
- This file is added to the prereg SHA256SUMS (4 entries). The job preflight verifies both.
- PREREG.md, l1b_registry.json, l1b_split.json and l1b_job.sh are unchanged.
