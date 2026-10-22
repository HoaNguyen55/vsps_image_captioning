# Paper E' pilot note: English-anchored Vietnamese captioning (H1), training-free

**EXPLORATORY / DEV-PILOT (CC-098). Not confirmatory.** It makes no claim. A GO only authorises writing the E' pre-registration; a NO-GO sends the work to H2's precheck. Committed before any decode. Times are UTC.

## Arms
All zero-shot, greedy (`do_sample=False`, `num_beams=1`), 60 new tokens per generation step, one caption per image, no exemplars. Models and snapshots are B-N1's: Qwen2.5-VL-7B, InternVL3-8B. Loading, batching and the greedy call are the committed LB/C code, imported unchanged.

| arm | step 1 | step 2 |
|---|---|---|
| **D** direct | image + B-N1 short Vietnamese prompt (`evaluate.PROMPTS["short"]`, sha256 8870589c) | none |
| **T** translate | the English step below | text only, **no image**, prompt T |
| **A** anchor | the English step below | image + prompt A |

English step (shared by T and A, decoded once; Paper A's `short_en`): `Describe this image in ONE short English sentence, like a caption. Do not list items or explain.`

Prompt T (`{en}` = the English caption):
```
Dịch chú thích ảnh tiếng Anh sau sang tiếng Việt. Chỉ viết MỘT câu tiếng Việt ngắn gọn, giống chú thích ảnh. Không giải thích.
Chú thích tiếng Anh: {en}
```
Prompt A (anchor line, a newline, then the D prompt unchanged):
```
Chú thích tiếng Anh của bức ảnh này (chỉ để tham khảo, có thể thiếu hoặc sai): {en}
Mô tả bức ảnh này bằng MỘT câu tiếng Việt ngắn gọn, giống chú thích ảnh. Không liệt kê, không giải thích.
```
Only the final Vietnamese caption is scored. Stop rule: a text-only arm with more than 20% empty captions stops the job (that path has not run on a GPU).

## Sets (spent by this pilot; not E' confirmation sets)
- **KTVIC dev299**: C's committed dev pool `manuscript/prereg/2026-10-21_dev_pools/ktvic_dev299.tsv`, all 299 rows (the pool has no 300th), sha256 `a4ac7fdbd904f2205845705f5235b9748225a83a07854b58e59a755b85e4186e`.
- **XM-dev300**: the first 300 of C's XM-dev500 (`lists.json` `sets.xm_dev500`) in sorted id order, no seed. `xm_dev300.tsv`, sha256 `b633153409eb1992c5d1857f8f8928471a01e5ac6103d2b9ab5ce6459726a443`. `lists.json` sha256 `5c479f03e8be544f4cd12b5d997b5dc92b6c622df061760cd02f6ba82f6b4371`.
- **Disjointness (checked in code, counts 0):** no image is in OV-test, XM-test2500, A's XM600, or any A, B or C test set (C's stage-2 refusal with its carve-out, plus an explicit sha check against XM-test2500 and the still-refused shas).

## Metrics (local, CPU; Paper A's matcher v2, `rescap.chair.objects_in`, on the final caption)
- **Object F1 = 2PR/(P+R).** KTVIC: gold = union of the image's references; P micro, R mean per-image recall over images with gold (`object_prf` definition). XM: gold = OIV7 human labels via `xm3600_oiv7`; P = present/(present+absent) mapped mentions, R = mentioned/present pairs, micro; unlabelled images add nothing.
- **Object count** = distinct classes per caption. **CIDEr-D** = Paper B's protocol card (RDRSegmenter 1.2, lower-cased, final punctuation stripped, x100).
- **Matched count (CC-098: A's matched-prefix control):** per image, the first k = min(count_A, count_D) distinct classes of each caption, in order of mention; F1 recomputed on those prefixes.
- **Pooling:** every contrast is the mean over the 4 cells (2 models x 2 sets); "each model" = the mean over that model's 2 sets. Paired image bootstrap, 2,000 draws, seed 0, one resample per set shared by models and arms; 95% percentile CI.

## Decision rule (CC-098), `score_pilot.decide`
- **GO** iff all hold: (A-D) F1 >= +2.0 points; its CI lower bound > 0; each model's (A-D) F1 > 0; the matched-prefix (A-D) F1 has CI lower bound > 0 (my reading of "the gain holds at matched count"); (A-D) CIDEr-D >= -1.0; (A-T) F1 >= 0.
- **NO-GO** if (A-D) F1 <= 0 or the matched-prefix (A-D) F1 <= 0. Then H2's precheck and pilot.
- Any other outcome is **INCONCLUSIVE**: no spend; the judge rules.

## Budget and data handling
- **GPU:** <= 2 GPU-h wall for the whole job (hard `timeout`), one RTX 3090 (M3), run in an M3 gap after C's stage-2 XM block is scored, never displacing C's January test. Estimate in the REPORT: about 1.7 h (high 1.9 h).
- Captions stay in output files on M3 and in local scratch; they are never committed or printed. The committed record holds numbers, ids and sha256 only.
- OIV7 labels never reach the GPU host; scoring refuses when `VSPS_MACHINE_ID` is set.
- Existing gold only (OIV7 labels, references); no new annotation; AI-silver is not evidence.
- Ownership: A owns the count-confound result (used here as a control), B the protocol, C retrieval ICL (no exemplars here).
- Files: `scripts/eprime_pilot/{decode_pilot.py,score_pilot.py,job.sh}`, pinned in `SHA256SUMS`.
