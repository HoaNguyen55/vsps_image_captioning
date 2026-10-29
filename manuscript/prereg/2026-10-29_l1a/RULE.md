# L1-a dev pilot: diacritic-only reading errors of open LVLMs on Vietnamese scene text (RULE; no output exists)

Final after CC-165 (GO-with-fixes 91%; W1, W2, W4, W5 and W6 applied). It was written before any L1-a decode
existed. Its sha256 is pinned in `scripts/l1a/l1a.py` (RULE_SHA256). It is logged in
`.session_backup/2026-10-13/decisions/LOG.md` after the one-judge diff read, then committed by the gatekeeper. Only
then may the job run (CC-165 W3). **It uses ViTextVQA dev only. No ViTextVQA test
file has been fetched, and no test image is ever extracted or staged.** Everything below is AI opinion, not
expert-validated.

## 1. Question and scope

Do open LVLMs that read Vietnamese text in images make diacritic-only errors often enough to support the L1 line? In
which mark classes do these errors fall? A diacritic-only error has a correct base-letter skeleton but wrong or missing
tone or vowel marks.

- This pilot tests only **kill clause (a)** of PORTFOLIO_3Y L1 and CC-160 W7: the diacritic-only share of wrong
  answers.
- The re-rank clause (b) (re-rank gain ≥ +1.0 EM) is not tested here. Neither are the RAISE parts that need a fix
  (re-rank ≥ +2 on 3 backbones; ITERATE rank 1 "lattice adds ≥ 8 points"). Both need the later L1-b pilot.
- A pass therefore means **"not killed"**, never RAISE. PROCEED_STRONG (§6) says only that the share part of RAISE
  holds.

## 2. Data (pinned; ids, shas and counts only, no question or answer text in the repo)

| Input | sha256 |
|---|---|
| data/datasets/vitextvqa_raw/ViTextVQA_train.json (35,159 QA; used only for the gold noise counts in §2.4) | 915f569fc9848b424c75cb16133b82730aa0ec47947a46d5a311675484e638b5 |
| data/datasets/vitextvqa_raw/ViTextVQA_dev.json (5,155 QA, 1,676 images) | c6ab6a7babceb5928e393ec4cc7461c68b35f4fb19ec1a39e9366318be876b81 |
| data/datasets/vitextvqa_raw/ViTextVQA_images.zip (all splits; never extracted in full, never copied to M2) | 39420475263f38892c5abceed5b4886beec707526f9e05a12e2ecd39a0d0e0b3 |
| manuscript/prereg/2026-10-29_l1a/neardup.json (W1 pass, `l1a.py neardup`) | fa676be1274fac78ba9624f0432b34b91766b60ad5ec247c54b77ff1e5ac843d |
| manuscript/prereg/2026-10-29_l1a/l1a_lists.json (rebuilt by `l1a.py build` after W1) | ac5ed047dc013cb642a325b491994d516ff8ee187c26f30fa47c0b62057e0087 |

The fetch is recorded in LOG OPS-1029l. The licence is CC BY-NC 3.0 (HF card). The official terms are still open
under G3.

1. **Build (CPU, laptop, done once on 2026-10-29).** `python3 -P scripts/l1a/l1a.py build --stage
   data/datasets/l1a_vitextvqa_dev`. This directory is gitignored.
   - The step reads the zip members `st_images/<file>` one by one. It takes only the dev filenames that the W1 pass did not flag and refuses
     any name that is not `<digits>.jpg`. There is no extractall.
   - It writes:
     - `images/` (1,520 jpgs, 523 MB);
     - `grey.png` (512 x 512, RGB 128, sha c6bf3833...);
     - `questions.jsonl` (qa id, image id, file, image sha, question; **no answers**; sha 2e486b96...).
   - No train image was extracted.
   - l1a_lists.json holds:
     - the 4,585 kept QA ids in dev order;
     - the 1,520 kept image shas;
     - the 570 excluded QA ids and the 156 excluded image files;
     - the stratum ids;
     - the train/dev disjointness check: image ids and filenames are disjoint;
     - the counts in §2.4.
2. **Near-duplicate pass (CC-165 W1, CC-160 W1; fixed before it ran).**
   - When: on the laptop CPU, before staging.
   - What is compared: the 1,676 dev images against every zip member that is neither a train nor a dev file (the
     other 3,353, presumably test).
   - How the other images are handled: they are read in memory only and never written. test.json is never fetched.
   - Features: those of `match_openviic` on the bytes (pHash, dHash, mirrored hashes, SSCD disc_mixup 9f26bd4c).
   - Rule: the W25 RULE §3 union. A dev image is **flagged** if any one holds:
     - C1: equal sha256;
     - C2: min(pHash, dHash) ≤ 10 (the dev mirrored hashes count) and SSCD ≥ 0.5;
     - C3: SSCD > 0.75.
   - More than 3 unreadable other members is a FAULT.
   - **Every QA of a flagged dev image is excluded** from staging, numerators and denominators. The excluded QA are
     reported beside the result.
   - Output: `neardup.json`, holding dev filenames and counts only.
   - **Result (2026-10-29, run once, 32 min CPU):** 3,353 other members compared, 0 unreadable.
     - **156 of 1,676 dev images flagged:** C1 0, C2 145, C3 154. Most are re-encoded copies (SSCD ≥ 0.99, hash
       distance 0).
     - **Their 570 QA are excluded.** 1,520 images and 4,585 QA remain.
     - This means ViTextVQA dev and the other split share near-identical images. That fact matters for any later L1
       test look (W25-style exclusion on the test side).
3. **Full split.** All 4,585 kept dev QA are decoded (the full dev split minus the pre-fixed W1 exclusion). There is one gold answer per question. No dev item has an empty gold
   after tokenisation, so nothing is excluded.
4. **Mark-bearing stratum (primary population; gold only, prediction-free, fixed now).** A QA is in the stratum if its
   gold answer has at least one syllable with a tone or vowel mark under §5.1. This gives **2,878 of 4,585** (62.8%).
   - The other 1,707 are numbers, codes and unmarked words. On those a diacritic-only error is possible only by
     adding marks.
   - This replaces scout 1's "transcription-type" rule (see §6.2).
   - By gold length in syllables: 1 syllable 108, 2 syllables 791, 3 or more 1,979 (counted now; used by row (f)).
5. **Gold mark-noise floor (critic blocker; counts from the gold, no model output).**

   | Count | train | dev |
   |---|---|---|
   | answers | 35,159 | 5,155 |
   | syllables | 130,556 | 19,098 |
   | old-style tone placement on open oa/oe/uy (hòa type) | 1,046 | 153 |
   | new-style placement on open oa/oe/uy (hoà type) | 147 | 25 |
   | syllables with more than one tone mark (malformed gold) | 49 | 8 |
   | other combining marks | 0 | 0 |
   | answers with no mark at all | 12,664 | 1,929 |

   - The gold mixes both placement styles, mostly the old style. §5.1 makes placement irrelevant, so this mix creates
     no error.
   - The 8 malformed dev syllables cannot be matched exactly by any well-formed prediction. They are left in, since
     the full split is used. They can add at most 8 items to the denominators.

## 3. Backbones (pinned; reused unchanged)

The four models come from the B-N1 registry `manuscript/prereg/2026-10-19_b_n1_vi_leaderboard.json` (sha 9ff02dc2...).
Each is pinned to a 40-hex revision with per-file hashes, trust_remote_code False, bf16 and sdpa.

| Key | Hub id @ revision | Batch | processor_kwargs |
|---|---|---|---|
| qwen25vl_7b | Qwen/Qwen2.5-VL-7B-Instruct @ cc594898 | 4 | min_pixels 262,144, max_pixels 1,048,576 |
| qwen3vl_8b | Qwen/Qwen3-VL-8B-Instruct @ 0c351dd0 | 4 | same |
| internvl3_8b | OpenGVLab/InternVL3-8B-hf @ 259a3b64 | 2 | none |
| qwen25vl_3b | Qwen/Qwen2.5-VL-3B-Instruct @ 66285546 | 8 | same as Qwen |

- The pixel limits are fixed now and are never tuned on this pilot. Resolution is a suspected cause of mark loss, so
  it belongs to a later manipulation, not to this measurement.
- The venv is venv-lb (setup_gpu.sh H_LB 685ffe2a; torch 2.5.1+cu121, transformers 4.57.6, accelerate 1.15.0). The
  decode refuses if the packages differ from the registry.
- **Scope (CC-165 W4).** All four backbones have **Qwen-family LMs**: InternVL3-8B-hf at 259a3b64 has
  text_config.model_type qwen2.
  - Every verdict is scoped to "open LVLMs with Qwen-family LMs". decide.json carries this label in `scope`, and so
    does every L1 wording.
  - A non-Qwen-LM backbone is **required** before L1-b or any RAISE.
- **Resolution asymmetry (disclosed).** InternVL3-8B-hf reads each image as **one 448 x 448 tile**
  (crop_to_patches false). The Qwen models get 0.26-1.05 MP. InternVL's base-letter errors are therefore inflated,
  which pushes its share toward KILL. The registry processor config is not changed.

## 4. Decode

- **Prompt** (one prompt for every model, Vietnamese, sha256 24e65010...):
  `Dựa vào chữ xuất hiện trong ảnh, hãy trả lời câu hỏi sau. Chỉ ghi câu trả lời ngắn gọn, không giải thích.\nCâu
  hỏi: {q}`. This is the user turn, after the image, through the model's own chat template.
- **Generation:** greedy (do_sample False, num_beams 1) with max_new_tokens 48. Other settings come from each
  snapshot's generation_config, which is recorded.
- **Harness:** `scripts/lb/decode_hf_vlm.py` (sha e2de1881), reused through its `load`, `make_generate` (per-item
  texts), `check_snapshot` and `decode_slices`. It has fixed slices and fsynced resume. The run key includes the
  questions sha.
- **Arms:**
  - **img:** the real dev image.
  - **grey:** every QA is decoded with the same grey 512 x 512 image instead of its own. This is the image-removed
    probe (§7). It uses the same code path, so no text-only message format is introduced.
- **Order:** the img arms first (7B, Qwen3-8B, InternVL3-8B, 3B), then the grey arms in the same order. If the cap
  stops the job, the verdict arms are done first.

## 5. Metric (deterministic, against human gold; no AI label)

### 5.1 Syllables and signatures

- Text is NFC-normalised and lowercased. It is split into runs of letters and digits; stray combining marks stay
  inside their syllable. Punctuation and whitespace are dropped.
- Each syllable becomes a signature under NFD: (skeleton, vowel marks, tone).
  - Marks are classified by code point, never by position:
    - tone: U+0300 huyền, U+0301 sắc, U+0303 ngã, U+0309 hỏi, U+0323 nặng;
    - vowel mark: U+0302 circumflex, U+0306 breve, U+031B horn.
  - A vowel mark is stored with the index of its base letter.
  - The tone is stored without a position, so old and new placement (hòa / hoà) give the same signature.
- **đ does not decompose under NFD.** It stays a base letter, so đ ↔ d is a base-letter error. This is conservative:
  it pushes toward KILL.

### 5.2 Answer-level classes

- **contained view (primary).** The gold has n syllables. Every window of n consecutive prediction syllables is
  compared with it:
  - **correct** if any window equals the gold signatures;
  - otherwise **diac** if any window has the gold skeleton. Among those windows, the one with the fewest differing
    syllables is used, the first on ties.
  - otherwise **base**. An empty prediction is base.

  This view does not count a polite sentence around a right answer as a reading error.
- **strict view (secondary).** The same comparison on the whole prediction.
- **Diac subclasses:** tone-only, vowel-mark-only, or both. There is also an "all marks dropped" flag: the gold has
  marks and the window has none.

### 5.3 Character level (descriptive)

- Characters are units of (base, marks), taken after `rescap.chair.norm_tone` (pinned e47d249a).
- Levenshtein distance is computed on the prediction window of n syllables with the fewest edits.
- A substitution with the same base and different marks is a **mark substitution**. Every other edit is a base edit.
  On ties, base edits are preferred.
- Reported: base edits, mark substitutions and their share, pooled over wrong stratum items.

### 5.4 Mark classes (descriptive; the "which classes" answer)

Over diac errors in the stratum, the pilot reports:
- the subclass counts;
- the tone confusion counts (gold tone > predicted tone, "none" included);
- the vowel-mark confusion counts per base letter (circ / breve / horn / none);
- the all-marks-dropped count;
- the đ ↔ d count (CC-165 W5): wrong answers that are base errors only because of đ ↔ d. These are answers that
  would be diac if đ were folded to d. The count is given per backbone, for all items and for the stratum.

**Validation on CPU (gold corruptions, not model output; p300 Pattern 8):**
- gold against itself gives 4,585 correct;
- stripping all marks gives diac on 2,878/2,878 stratum items and correct on 1,707/1,707 others;
- swapping the first tone gives diac-tone on 2,737 items, and correct on the 141 stratum items that carry vowel marks
  but no tone.

## 6. Pre-fixed rule

### 6.1 Primary statistic (per backbone, img arm)

share = (diac answers in the stratum) / (wrong answers in the stratum), under the contained view.

**Decision statistic (CC-165 W2): the chance-corrected share c = share − null.**
- null is the same backbone's mismatched-gold null share, row (g) in §6.2.
- The 95% CI of c is a percentile cluster bootstrap over images (B = 2,000, `default_rng(0)`). One index matrix is
  shared by all backbones and by both terms, so the share and its null are drawn together.
- **The point estimate of c decides.** The CI is reported, and a CI that crosses 10% is flagged for the judge.
- The raw contained share (upper bracket) and the strict share (lower bracket) are reported beside c. So is the
  uncorrected outcome, which is descriptive only.

**Assessable.** A backbone is assessable if its img arm exists with n = the staged QA count (§2), empty answers ≤ 20% and hit_max
≤ 5%. Otherwise it is NOT_ASSESSABLE and leaves the rule.

**Outcome (exactly one; clauses in this order):**

1. **NO_VERDICT** if fewer than 3 backbones are assessable. Back to the judge.
2. **KILL** if c < 10% on every assessable backbone. L1-P1/P2 are killed or demoted to a conference paper
   (PORTFOLIO L1, CC-160). If any CI_hi ≥ 10%, the reason names those backbones for the judge's read.
3. **PROCEED_STRONG** if c ≥ 20% and CI_lo(c) ≥ 10% on every assessable backbone. The share part of RAISE holds;
   the fix part is untested.
4. **PROCEED** otherwise: c ≥ 10% on at least one assessable backbone.

### 6.2 Secondary rows (pre-declared, descriptive, never gating)

- (a) **All items** as the population. This is scout 2's "all wrong answers"; it dilutes with number and code
  questions.
- (b) **Near-miss denominator** (scout 1 clause b). The denominator is diac plus wrong answers whose skeleton window
  is within 2 base edits of the gold. **This depends on the prediction and inflates the share by construction.** It is
  shown only so that the scout figure can be compared.
- (c) **Strict view** on the stratum.
- (d) **Ranking.** The backbone order by contained EM and by mark-blind EM (diac counted correct). The pilot reports
  whether the order changes. This is the PORTFOLIO "changes the ranking" part, descriptive at n = 4.
- (e) **Minus grey-correct items** (§7).
- (f) **By gold length.** The primary share for 1-, 2- and ≥3-syllable golds, and the primary share without the
  108 one-syllable golds.
- (g) **Mismatched-gold null.** Each img-arm prediction in the stratum is scored against the gold of another stratum
  item: a seeded derangement (`default_rng(1)`; shuffle, then pair each item with the next, cyclic; same-image pairs
  skipped). The diac share of those wrong pairs is the chance rate at which the contained view finds a same-skeleton
  window in an unrelated answer.

**Known bias of the contained view (disclosed before any output).**
- A short gold is classed diac if any window of a long wrong answer has its skeleton with other marks. Skeleton
  collisions are common in Vietnamese: scout 2 found 74% of syllable types ambiguous once stripped. So the contained
  view can push the share up, away from KILL. The selftest shows the case: a 1-syllable gold inside an unrelated
  sentence is diac (contained) and base (strict).
- Strict (row c) is therefore the **lower bracket** and contained the **upper bracket**.
- **Judge flags** in decide.json; they never change the outcome:
  - the null share (g) is ≥ 5 points on any backbone;
  - dropping the 1-syllable golds (f) would change the outcome;
  - prior_flag on any backbone (§7);
  - row (e) moves any backbone across 10%.

**Why not scout 1's denominator (AI opinion).** Clause (a), "gold appears in the question's target text region",
cannot be computed: ViTextVQA has no OCR boxes, and an OCR system's output is not gold. Clause (b) conditions on the
prediction, so the 10% kill could hardly fire. The stratum is gold-only, fixed before any output, and counted now.

## 7. Contamination and language-prior probe (grey arm)

- Reported per backbone:
  - contained EM with the grey image, on all items and on the stratum;
  - **prior_flag** if grey EM is ≥ 10% on all items;
  - row (e): the primary share recomputed without the items that the same backbone answers correctly with the grey
    image.
- The probe is descriptive. It never changes the §6.1 outcome.
- prior_flag on any backbone, or row (e) moving any backbone across 10%, is written to decide.json `judge_flags`
  (§6.2). The judge reads them before L1-b.
- The probe cannot prove that a backbone never saw ViTextVQA in training. It shows only how much of the dev gold can
  be produced without the image. The real training data of these models is unknown.
- If the cap stops the job before a grey arm runs, that backbone's probe is "not run". The verdict still stands on
  the img arms.

## 8. Run, budget, one look

**Machine.**
- The run is on M2 (machine id m4, dev only, RTX 3090): `bash scripts/l1a/l1a_job.sh <HEAD>` inside tmux. It uses
  `set -euo pipefail`.
- The job refuses unless `/root/.vsps_machine_id` is m4, HEAD is the given one, the tree is clean, both SHA256SUMS
  verify, the venv-lb freeze matches and `l1a.py --selftest` passes.

**Guard (before every GPU step).**
- grl `host_ok`: m4, an idle GPU, HEAD and a clean tree.
- The staged directory must hold exactly the 1,520 pinned dev jpgs, grey.png and questions.jsonl at their shas, and
  nothing else.
- No ViTextVQA zip, test file or `st_images` directory may be anywhere under NCS_DATA.
- No other experiment lock.
- The lock is B-1's O_EXCL lock at /root/outputs/l1a/RUNNING.

**Staging (by hand, one LOG checklist line, no host string).**
- The laptop's `data/datasets/l1a_vitextvqa_dev` is copied to `$NCS_DATA/datasets/l1a_vitextvqa_dev`. The line ends
  with one `l1a.py guard` rc 0.
- questions.jsonl holds question text. It lives only on M2 and in the gitignored laptop directory. Gold answers
  never leave the laptop.
- **Cleanup (CC-165 W6).** After the pull, questions.jsonl and the staged images are deleted from M2, and the
  deletion is logged in one LOG line with no host string.

**Budget (from the measured B-N1 short-prompt rates on an RTX 3090).**
- Measured KTVIC rates in s/item: 3B 0.47, 7B 0.70, Qwen3-8B 0.69, InternVL3-8B 1.27.
- ViTextVQA dev images are larger: a median of 0.49 MP against about 0.3 MP. A x1.4 factor is applied.
- img arms: 4,585 x (0.66 + 0.98 + 0.97 + 1.78) s ≈ **5.6 GPU-h**.
- grey arms: 512² input, about 0.4 x the KTVIC rate ≈ **1.6 GPU-h**.
- Loads: about 0.3 GPU-h.
- **Design ≈ 7.5 GPU-h. Hard cap 12 GPU-h.** Accounting follows B-1 (`b1.left`; start lines charged). A timeout is a
  final CAP STOP.
- The Qwen2.5-VL-3B snapshot is fetched on M2 at the pinned revision (CPU, not charged). The other three are already
  on M2 from setup_gpu.sh.

**Crashes.**
- An interrupted decode resumes from its finished slices (same run key only). Any other failure, including CUDA OOM,
  is a JOB STOP back to the judge.
- Batch sizes are never changed silently. An OOM fix is a logged amendment before any score.

**Scoring.**
- The preds and SHA256SUMS are pulled to `.session_backup/machines/M2/root/outputs/l1a`. `l1a.py score` then runs
  once on the laptop CPU.
- It refuses:
  - if decide.json exists;
  - if RULE.md, l1a_lists.json or rescap/chair.py differ from their pins;
  - if any preds file's sidecar or provenance differs: lists, prompt, registry, questions sha, n.
- Output: `.session_backup/2026-10-29/l1a/decide.json`. It holds ids, counts and numbers only, never a prediction
  string.

## 9. Code

| File | Role |
|---|---|
| scripts/l1a/l1a.py | build, guard, lock, left, snap, fetch, decode, score, neardup, --selftest (56 checks, synthetic) |
| scripts/l1a/l1a_job.sh | the M2 job |
| scripts/l1a/SHA256SUMS | the two files above plus the reused pins: decode_hf_vlm.py, the B-N1 registry, rescap/chair.py, b1.py, grl/common.py |
| manuscript/prereg/2026-10-29_l1a/SHA256SUMS | RULE.md, l1a_lists.json, neardup.json |

**Finalisation (CC-165 W3, done in this order).**
1. RULE_DRAFT.md was renamed RULE.md.
2. RULE_SHA256 was set in l1a.py.
3. Both SHA256SUMS were regenerated.
4. The selftest was run.

Any later edit to RULE.md repeats steps 2-4. Otherwise the job stops at preflight.

The selftest, guard, lock and cap steps run in `/root/vsps/.venv`, because they import b1.py, as in B-R1. Decode,
snap and fetch run in venv-lb.

**Dry run (laptop, CPU, no model output).** `score` ran end to end on synthetic predictions made from corrupted gold
(stripped marks, prefixes, junk), with the RULE pin pointed at the draft. The output went to the scratchpad and was
deleted. This checked only the code path: provenance checks, all rows, flags and the ranking.

## 10. Rulings applied (CC-165, GO-with-fixes 91%)

The panel answered the six questions as follows.

- **Q1.** The stratum is the primary population.
- **Q2.** đ ↔ d is a base-letter error, and its count is reported (W5).
- **Q3.** The near-duplicate pass applies. It is §2.2 (W1).
- **Q4.** CC-160 W7 is amended for L1-a only. No L1-b GPU step and no L1 test look until G1 (the sweep) and G3
  (the written terms) close.
- **Q5.** No model is added. The scope label applies (§3, W4). A non-Qwen-LM backbone is required before L1-b or any
  RAISE.
- **Q6.** Run now on idle M2. Any committed B or C M2 job queues ahead of L1-a's next step, at a step boundary,
  without killing a running decode.
