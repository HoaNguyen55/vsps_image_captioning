# CIDER_VI_PIN v1.1: the CIDEr-VI scoring form for the C-PVR-T1 guard (DRAFT, not approved)

Status: DRAFT v1.1 for round 2/3 of CC-294, a one-judge FULL read at **IRREVERSIBLE 85**. Round 1 (CC-294,
2026-11-08T06:18:15Z) gave NEXT_ROUND 80, with one BLOCKING item, W1 (JDK). Round 2 can grant GO. It is an
implementation pin of a registered gate, not an amendment: no registered line changes. It binds only after a GO and a
gatekeeper commit, and only if that commit lands before S16 opens any tier-1 output.

v1 = `CIDER_VI_PIN_v1.md` (0ff30613, 311 l.) is left untouched. §15 lists every change v1 → v1.1 with its source.

**Written before any tier-1 output was read.**
- v1 was written 2026-11-08, about 04:40Z-05:50Z (UTC), at repo HEAD f5cc716. v1.1 was written about
  06:25Z-07:10Z, at HEAD f5cc716 and then at 7e24eb6 (the scorer commit, CC-293r3 GO 87), which landed in that window.
- Both were written on branch paper-v10 while S15 was running on HC-1 (end by about 2026-11-08T19:45Z).
- No tier-1 output, pulled file, watch file, a1_decomp file or host file was opened.
- §13 lists every touch near a barred path. CC-294 Ruling 3 upheld the blind status of v1.
- AI opinion throughout.

Sources:
- the rulings: CC-293 (2026-11-08T03:20:47Z) Ruling 4 (G-1); CC-293r2 (06:00:08Z) W4 and N-H; CC-294 (06:18:15Z);
  CC-293r3 (06:32:30Z) Rulings 3 and 4 (binding readings on `--cider` / `--no-cider`);
- PI-1108d (2026-11-08T06:07:26Z, per CC-294 Ruling 7);
- prereg v1.2 `PREREG_DRAFT_v1_2.md` 0a2f0773 (8282874);
- T1-GUARD v3 `AMENDMENT_T1_GUARD_DRAFT_v3.md` 9e03811c (f5c6741);
- T1-REP v4 `AMENDMENT_T1_REPORTING_DRAFT_v4.md` 0e9793f3 (4124ef3);
- PINS-A v1.4 `PINS_A_DRAFT_v1_4.md` 624b0804 (3fb6725);
- T1-ANALYSIS v1.1 59b6eae5 (f5cc716);
- `C_DIRECTION_v4_1_2026-11-02.md` (the δ_C table).

## Tóm tắt cho PI (tiếng Việt)

- Bản v1.1 sửa lỗi chặn W1 của CC-294. Script giờ dừng (FAULT) nếu `java -version` không phải 21.0.12.1, và ghi lại
  dòng phiên bản, đường dẫn java cùng sha của VnCoreNLP vào bản ghi.
- Không khoá gói Java được, vì `apt-mark hold` cần sudo mà dự án cấm sudo. FAULT của W1 là lớp bảo vệ. Nên chạy S16
  ngay sau khi kéo kết quả S15 về.
- Đã thêm 8 ca kiểm tra toàn vẹn, ca chú thích rỗng, đếm số chuỗi bị NFC đổi, và kiểm tra khoảng [0, 1000] tính cả
  hai đầu.
- Mutant: 28/28 của script bị bắt. Trong 16 mutant tay của giám khảo, 15 bị bắt; mutant còn lại là tương đương (CC-294
  Phán quyết 1 (b)).
- Cách tính không đổi so với v1, và đã được PI duyệt (PI-1108d).
- Script chấm điểm đã được commit (7e24eb6). Bản này đã kiểm lại định dạng file với bản đã commit đó.

## 1. Where CIDEr-VI is consumed (registered spots)

| spot | what it needs from CIDEr-VI |
|---|---|
| prereg §6.3 (iii), l.469-470, with T1-GUARD G-3 | the variant passes δ_C (CIDEr-VI) vs A1 |
| prereg §6.3 l.472-475 as replaced by T1-GUARD G-1 | the CI lower bound of the pooled-G1 ΔCIDEr-VI(variant − A1) > −2.0: per-image scores within each source set, DF per G-7, image weighting, bootstrap stratified by set |
| prereg §6.3 l.476-477 (unchanged STOP) | STOP before tier 2 if neither variant passes δ_C and δ_R |
| prereg §12 (iii)-(iv), l.767-768 | (iv) reads the variant chosen in (iii), so the go rule rests on δ_C |
| T1-GUARD G-4, §2.1 descriptives | XM3600-vi ΔCIDEr-VI(variant − A1) with its CI, in-sample; the per-set Δ with CIs |
| T1-GUARD G-6 | the operating characteristics of §3 rest on the SD basis of §1 (per-image CIDEr-D ×100, `data/results/metrics_v2/*.cider.json`, d8ee09e) |
| T1-GUARD G-7 | the DF corpus: per source set, the references of that set's guard-half images that remain after §7.4 / W25; never pooled |
| T1-REP v4 §4 (l.190-192) | A1 − A0 CIDEr-VI on XM3600-vi, the ICL-mechanism check (none gates) |
| C_DIRECTION v4.1 δ_C table | δ_C = 2.0 on the CIDEr ×100 scale, labelled lenient |
| PINS-A v1.4 §4.2 (l.221-226) | the house segmenter pins and call: VnCoreNLP 62bbc58f, jar / rdr / vi-vocab shas, the CLI call with a marker line, the JDK by `java -version` (l.225) |
| T1-ANALYSIS v1.1 C-M2 (via the scorer) | C-M2's PVR is the §6.3 variant, so it is NOT_RUN until a pinned CIDEr-VI input exists (CC-293 Ruling 4 (e)) |

## 2. Implementation (pinned; unchanged from v1)

- **Scorer:** `scripts/kit_b/protocol_pilot.py` **6aee428207a2d1a045cd72d054e26a2e2ac8d9c2e414cb0c161e3b95dffd92bf**,
  class `Cider`.
  - It is tracked at HEAD (7fa7b83) and byte-equal to the archived kit (`.session_backup/2026-10-21/zenodo_build/
    code/scripts/kit_b/`).
  - It re-implements pycocoevalcap's CiderScorer (CIDEr-D): n = 4, σ = 6, clipping, and the Gaussian length penalty
    on bigram counts. Each per-image score is × 10 inside, and `per_image` multiplies by 100 on top.
  - The output scale is CIDEr ×100, the δ_C scale.
- **Call:** one `Cider(refs)` per source set, with **no `sigma` and no `df_refs` argument**, then `per_image(hyps)`
  for each arm. The returned array runs in `Cider.ids` order (sorted ids) and is mapped back by `zip(Cider.ids, …)`.
- **Helper:** `scripts/kit_b/punctuation_audit.py`
  **a7e8024030f56cbff07124278cd631964b7b1197607426d7212fd665b6c2f9b1**, `strip_trailing_punct_tokens` (stripped
  column only, §4).
- **Loader:** the `scripts/c_stage1/score.py` `kit()` pattern (258daa84, l.38-60).
  - Each kit file is sha-checked, then loaded by `spec_from_file_location` and registered in `sys.modules`.
  - `protocol_pilot` is loaded first, so the kit's own `import protocol_pilot` resolves to the checked module.
  - `sys.path` is restored afterwards.
  - The kit imports `rescap.chair.norm_tone`, so `CP.rescap_mods` first checks `rescap/chair.py` e47d249a and
    `rescap/vi/lexicon.py` fbc945f2 (the c_pvr REPO_PINS). `norm_tone` is never called on this route.
- **c_pvr code:** `scripts/c_pvr_gpu/c_pvr_gpu.py` 9a9c6eb5 behind its sha. Its `load()` then checks
  `scripts/c_pvr/c_pvr.py` a503644a and `scripts/c_pvr/c_pvr_run.py` 0c80ee68. Nothing in them changes.
- **Equality with the G-6 scorer:** the selftest checks `Cider(refs).per_image` against pycocoevalcap 1.2
  `CiderScorer(n=4, sigma=6.0)` × 100, at rtol 1e-12.
  - It does this on 61 synthetic images, including an empty caption and an exact copy. One image has a single
    unique reference and a copy of it, and scores exactly 1000.
  - It does it again on every arm of a three-set synthetic world, after the full text route (§10).

## 3. Text route and JDK (pinned)

The same route is used for references and for captions:

1. `CP.clean` (c_pvr.py l.213-215): Unicode **NFC**, then whitespace runs (newlines included) become one space,
   trimmed. A text that contains the batch marker `XQZSEPQX` (CP.MARK) is a FAULT.
2. `CP.rdr` (c_pvr.py l.537-560): the VnCoreNLP-1.2 RDRSegmenter `wseg` CLI over pipes, with one marker line between
   texts.
   - The call is `java -Xmx700m -XX:+UseSerialGC -XX:ActiveProcessorCount=1 -jar VnCoreNLP-1.2.jar -fin /dev/stdin
     -fout /dev/stdout -annotators wseg` (PINS-A l.226).
   - On every call the jar, `wordsegmenter.rdr` and `vi-vocab` are re-hashed against VNC_PINS: 9e2811cd…7793,
     9e62f96b…7fa06 and 0a47c5b5…eaa5 (PINS-A §4.2, l.221-223; VnCoreNLP github 62bbc58f).
   - The files sit in `~/c_pvr_tools/vncorenlp/` (or `$VNCORENLP_DIR`). Alignment loss is a FAULT.
3. The segmenter words, with `_` joining syllables (`đàn_ông`), are joined by one space.
4. **`str.lower()`**, after segmentation. This is the house order, as in the G-6 basis `segment(…).lower()`
   (rescap/metrics.py l.400-402) and stage 1 `s.lower()` (c_stage1/score.py l.158). It is not `casefold`.

**JDK (CC-294 W1).** `jdk()` runs at the head of `score`, before any other input is read and before the segmenter.
- It resolves `java` with `shutil.which("java")`. This is the same PATH lookup as the bare `java` of CP.JAVA (c_pvr.py
  l.69).
- It runs `java -version` and **FAULTs unless the first stderr line contains `"21.0.12.1"`**. A FAULT writes nothing.
- On this laptop the check gives `openjdk version "21.0.12.1" 2026-08-18`, `/usr/bin/java` →
  `/usr/lib/jvm/java-21-openjdk-amd64/bin/java`, build 21.0.12.1+1-1-24.04.4-Ubuntu (PINS-A A6 value).
- The record keeps the resolved path, its realpath, every `-version` line, the VnCoreNLP dir and the three VNC_PINS
  shas (§8).
- **No package hold.** `apt-mark hold` needs sudo, and the project forbids sudo, so no hold is set (CC-294 N8 / PI
  Q1). Unattended upgrades stay on, so the W1 FAULT is the guard.
  - If Java changes before S16, the producer stops, writes nothing, and the case returns to a judge before S16
    continues.
  - S16 should run soon after the S15 pull, to keep that window short.

Other route facts:
- One RDR pass covers the distinct cleaned texts of a run. The output keeps RDRSegmenter's own rewrites, such as
  old-style tone placement (PINS-A B1), on both sides alike.
- A literal `_` in a caption is not replaced. RDRSegmenter splits it into its own token, as in both precedents, which
  feed raw text. Its count is printed (§7).
- Segment-then-lower is load-bearing. On a made-up sentence with a capitalised name, RDR segments the cased text
  differently from the lower-cased text: `trần_minh_khoa` vs `trần minh khoa`. The selftest asserts the pinned order
  (CC-294 N6).
- `lower` vs `casefold` is shown on `ß`.
- A batch of 40,000 distinct synthetic texts fits under `-Xmx700m` (13.8 s, 262 MB; CC-294 check 6).

## 4. Punctuation rule (pinned; unchanged from v1)

- **As written (the GATING column):** every punctuation token the segmenter emits is kept, in references and captions.
  - This is the form of the G-6 SD basis, so the registered operating characteristics (T1-GUARD §1, §3) stay the
    guard's own.
  - It is the file passed to `c_pvr_score.py --cider`.
- **Stripped (DESCRIPTIVE only, never gating):** `punctuation_audit.strip_trailing_punct_tokens` runs on the
  caption's segmented, lower-cased tokens, removing trailing tokens whose characters are all Unicode category P.
  - References, the DF corpus and the Cider object are unchanged.
  - This is the stage-1 form, `c_stage1/score.py` l.164-165.
- **Disclosed difference from Paper C stage 1** (DESIGN.md §6.1, 133bd16, a different study): stage 1 decided on the
  stripped column. Here the gating column is as written, so that it follows the registered guard power (CC-293
  Ruling 4 (d), (e)). PI-1108d approves this.

## 5. The stripped column's report (pinned; unchanged from v1)

The producer writes `cider_vi_stripped.json` (the §8 format). Its record carries a block `stripped_descriptive` with
**point estimates only** (D2, accepted by CC-294 Ruling 1 (c)):
- per set and v ∈ {PVR-drop, PVR-keep}: the mean of s_i(v) − s_i(A1);
- the pooled G1 value: the image-weighted mean over the two guard sets;
- XM3600-vi: A1 − A0.

The block is labelled "descriptive, never gating" and sits beside the scorer's as-written `guard_G1` block. It has no
CI, no pass/fail and no decision. The selftest computes every expected value of the block from the stripped file
itself (CC-294 N2).

## 6. Reference files and the DF corpus (pinned; unchanged from v1)

| set (scorer name) | reference file | sha256 | field read | registered as C's reference set |
|---|---|---|---|---|
| `ktvic_explore` | `data/datasets/ktvic/test_data.json` | cc22ec6a8883773cb23c87ad5b64925f5a53c21982117274b53621f454e7ebbf | `annotations[].image_id` (int; id = `str(int)`, c_pvr_run.kt_ids) and `.caption` (not `segment_caption`) | prereg §4.1 l.335 "CIDEr-VI guard dev"; c_pvr_run LISTS_IN; c_pvr_lists.json edb07fbb `inputs` (cc90c96) |
| `openviic_explore` | `data/datasets/openviic/uit-openviic-annotation-test.json` | 66af01bac79af9e197f934ba3628477d5324506092d9a13dfd35330596310b16 | top-level key as-is (c_pvr_run.ov_keys) and `[key].captions` | prereg §4.1 l.336 "CIDEr-VI guard dev"; c_pvr_run LISTS_IN; c_pvr_lists.json `inputs` |
| `xm3600_vi` | `data/datasets/xm3600/full_data.json` | 101d24ad98e9dec43625ee425fa1b49aa1bde98f9609945bf5dd4424fef1dacc | `annotations[].image_id` (16-hex id) and `.caption` | prereg §4.1 l.331 "CIDEr-VI dev (in-sample)"; sha in prereg §2.4 l.267, W25 `RULE.md` l.21 (8f99bc8), b_pa1 `xm3600_all` |

- Field names come from house code, not from opening the files: c_stage1/score.py `references`, protocol_pilot
  `main`, eprime_pilot `score_pilot.py` l.163-166 and c_pvr_manifest `queries_ids`.
- The two guard-set pins are taken from `c_pvr_run.LISTS_IN` at run time, not typed a second time. Only the XM3600
  pin is new.
- **Scored images = the manifest query ids** of each set, from the sealed build checked against TMAN as in
  `c_pvr_score.manifests`.
  - Every manifest id must have at least one reference, or the run FAULTs.
  - Every guard-set id must satisfy `c_pvr_run.half` (prereg §4.2, explore half), or the run FAULTs.
  - References of any other image (the confirm half, the rest of the file) are dropped while the file is parsed.
- **DF corpus = the kit default = the references of the scored images of that set**, one Cider per set, never pooled.
  - For the guard sets this is exactly G-7, by construction (CC-294 Ruling 1 (d)).
    - The manifest query set is the set "that remains after §7.4 / W25", whatever was removed. dev-w25 removes items
      from the datastores, and query sets are not trimmed (W25_DEV_RUN_DOC_v1_2 l.81; prereg l.505).
    - `c_pvr_manifest.build_set` (l.146-147) FAULTs unless n equals SIZES 286 / 1,020, which are the
      `c_pvr_lists.json` halves (edb07fbb, cc90c96), and unless every id is explore half.
    - The producer prints n per set (§8 record).
  - For XM3600-vi (descriptive, outside G-7) the DF corpus is the references of its 3,600 manifest images.
  - The difference from the G-6 SD basis (DF over all 558 KTVIC references) is already disclosed in T1-GUARD §2.1.
- Licence to read: these are C's registered tier-1 dev / guard-dev sets (prereg §4.1).
  - The producer reads them only at S16, after this pin's GO and commit.
  - For this draft they were **hashed only**, which CC-294 Ruling 4 rules is not a look (§13).

## 7. Arms, completeness, range and FAULTs (pinned)

- **Arms written:** `xm3600_vi`: A0, A1, PVR-drop, PVR-keep. `ktvic_explore` and `openviic_explore`: A1, PVR-drop,
  PVR-keep (CC-293 Ruling 4 (d)).
  - This is exactly the scorer's `cider_in` need list (§8).
  - There is no A8 at tier 1: δ_C vs A8 is the tier-2 G-2 contrast.
- **Captions:** `out/<set>.<arm>.jsonl` under `--out`. Each one is checked:
  - against its line in the pulled SUMS file (`SHA256SUMS_tier1`), which may hold no malformed or repeated line;
  - for an LF last line;
  - for keys within `c_pvr_gpu.OUT_KEYS`, and for a set / arm match;
  - for unique ids and a string caption.
  - These are the `c_pvr_score.records` checks. Each has its own FAULT case and mutant (CC-294 N1).
- **Manifests:** MANIFEST.sha256 = `--tman`, each `manifest/<set>.json` against it, and label = CP.LABEL with the set
  equal to the file's set.
- **Completeness:** every one of the 10 (set, arm) files must cover exactly its manifest ids. A partial, absent or
  foreign-id arm is a FAULT, and **no CIDEr-VI file is written** (D1).
- **Empty captions** are kept and score 0 in both columns. The selftest world holds two: one `""` and one
  whitespace-only (CC-294 N2).
- **Range:** every score of both columns must lie in **[0, 1000] inclusive**, or it is a FAULT and nothing is written.
  NaN fails. 1000 is the attainable maximum, a caption equal to every reference (CC-294 N5). This equals the scorer's
  N-H check (§8).
- **Order:** the JDK check comes first. Then every integrity check runs before the segmenter: TMAN, SUMS, explore
  half, reference shas, references per id, captions. A FAULT writes nothing. Output files are opened with `xb` and are
  never overwritten.
- **Counts printed** (numbers only):
  - per (set, arm): captions empty after `clean`; captions containing `_`; captions **changed by NFC** (CC-294 N3);
    captions whose trailing punctuation the stripped column removes;
  - per set: references containing `_`, and references **changed by NFC**.
  - The NFC counts measure disclosure §11 (a) at S16.

## 8. Output format and record (pinned; consumed by `c_pvr_score.py score --cider F --cider-sha H`)

Checked against the **committed** scorer `scripts/c_pvr/c_pvr_score.py`
**7fe4a0806ad8c73ba42093422ed59004e1530c329a48bd819017e243c90204c4**. That is commit 7e24eb6, CC-293r3 GO 87, Form B.
`git show HEAD:` re-hashes to 7fe4a080, and the working copy equals HEAD. While this pin was drafted the scorer moved
ab6b9ede → 7f3ddfa5 → 1e15ce7a → 7fe4a080.
- `cider_in` is at l.812-826. It now also FAULTs on a non-finite value or one outside [0, 1000], inclusive (CC-293r2
  N-H; CC-294 N5).
- Its consumers: `xm_columns` l.338-339 (`cider[XM][a][i]`), `dCIDEr_xm_A1` l.597, `guard_g1` l.802
  (`cider[s][v][i] − cider[s]["A1"][i]`), and the A1 − A0 block (l.924).
- `--cider` / `--cider-sha` and `--no-cider REASON` are exclusive. `--no-cider` FAULTs under `SHA256SUMS_tier1`
  (l.834-837; CC-293r2 W4).
- Under Form B the scorer committed first. So this pin's round-2 read is the second read, and it checks this §8
  against the committed 7fe4a080 (CC-294 Ruling 6; CC-293r3 item 9).
- **Binding readings, CC-293r3:**
  - Ruling 4: `--cider` = the producer's `cider_vi.json`. `--cider-sha` = the sha recorded under
    `"as_written (gating; --cider)"` in `cider_vi_record.json`. `cider_vi_stripped.json` is never passed to
    `--cider`. A run on it is FAULT, and its numbers are POST_HOC.
  - Ruling 3: `--no-cider` is valid only after `c_pvr_cider_vi.py` has been run on that same pull and has FAULTed.
    The REASON and the S16 OPS line quote that FAULT text verbatim and name the pulled SUMS file and its sha. If the
    producer succeeds, `--cider` is mandatory. Any other `--no-cider` run is FAULT, and its numbers are POST_HOC.
- **Which producer FAULT licenses `--no-cider`.** This is this pin's reading, fixed pre-data, for the round-2 judge to
  rule.
  - It is licensed only by the D1 completeness FAULTs of `captions()`, the two messages that end
    "no CIDEr-VI file is written": an arm absent or not in the SUMS file, and an arm that does not cover exactly its
    manifest ids.
  - Every other producer FAULT does **not** license it, and stops S16 for a judge. These are the JDK, TMAN, manifest,
    SUMS and record custody checks, the explore half, a reference sha or a missing reference, the range check and
    the batch marker. Their messages end differently ("nothing is written", or no suffix).
  - So an environment or custody failure can never turn a possible δ_C STOP into NOT_DECIDED. No code change is
    needed, because the message texts already differ.

The format:
- **File** `cider_vi.json`: one JSON object `{set: {arm: {image id: score}}}`.
  - Sets: exactly `xm3600_vi`, `ktvic_explore`, `openviic_explore`. A top-level key that is not a manifest set FAULTs in
    `cider_in`, so the file holds **no metadata key**.
  - Arms: as in §7. `cider_in` requires `xm3600_vi.A0` and A1 / PVR-drop / PVR-keep on all three sets. Every arm
    present must cover exactly its set's manifest ids.
  - Image ids: the manifest `queries[].id` strings (XM3600 16-hex, KTVIC `str(int)`, OpenViIC file key).
  - Score: a JSON number, per-image CIDEr-VI on the ×100 scale, in [0, 1000], at full float64 precision (Python
    `repr`, no rounding, `allow_nan=False`).
  - Serialisation: `json.dumps(d, sort_keys=True)` plus a final LF, UTF-8.
- **`--cider-sha`** = the sha256 of those exact bytes. It is printed in the record as
  `files."as_written (gating; --cider)".sha256`.
- **Beside it, never passed to the scorer:** `cider_vi_stripped.json`, in the same format, and
  `cider_vi_record.json`, the printed record. The record holds no text. Its fields:
  - `jdk` = {`java`, `realpath`, `version` (every `java -version` line), `vnc_dir`, `vnc_pins`} (CC-294 W1);
  - `python`, `numpy`;
  - `tman`, and `sums_sha256` (the sha of the pulled SUMS file);
  - `code_sha256` (c_pvr_gpu.py, the two kit files and this producer);
  - `refs` (path and sha per set), and `n` per set;
  - `files` (both shas);
  - `counts` and the reference counts of §7;
  - the §5 block `stripped_descriptive`.
- **S16 OPS line (CC-294 N7).** The gatekeeper or operator OPS line of S16 states:
  - (i) `java -version` verbatim, run before the producer;
  - (ii) that the producer record's `tman` and `sums_sha256` equal the scorer's `--tman` and the sha of the pulled
    SUMS file the scorer reads (the scorer's `inputs.sums_sha256`);
  - (iii) the `--cider-sha` value passed, equal to the record's as-written sha (CC-293r3 Ruling 4);
  - (iv) only on the `--no-cider` path: the producer's FAULT line verbatim, the pulled SUMS file name and its sha
    (CC-293r3 Ruling 3).

## 9. Environment (pinned; unchanged from v1)

- **venv** `~/.venvs/c_pvr_cider`, CPython 3.12.3, installed with `--no-deps --require-hashes` from
  `scripts/c_pvr/requirements_c_pvr_cider.lock` **1bb358ae14c1b267ffc0430bfac62f0d4b39c21c0bb5a1967493313b65337b7d**
  (unchanged):
  - numpy 2.5.4, fbde6962… (the same wheel line as `requirements_c_pvr.lock`);
  - scipy 1.18.1, f55fa87b…: `protocol_pilot.py` imports `scipy.stats.kendalltau` at module level, and the c_pvr lock
    has no scipy;
  - pycocoevalcap 1.2, 083ed791…, `--no-deps` (no pycocotools). Only `pycocoevalcap.cider.cider_scorer` is imported,
    by the selftest; its imports are stdlib plus numpy.
- The install was tested offline (`unshare -rn`, `--no-index` against the wheels in `~/c_pvr_cider_wheels/`) in a fresh
  venv. `pip freeze` gives exactly the three lines (CC-294 check 3).
- Non-pip: openjdk 21.0.12.1, asserted (§3), and the VnCoreNLP files of §3, as in `requirements_c_pvr.lock`.
- The c_pvr scorer keeps its own venv `~/.venvs/c_pvr` (numpy 2.5.4). The two meet only through the §8 file and its
  sha.

## 10. Producer (`scripts/c_pvr/c_pvr_cider_vi.py`)

- sha256 **3401b46cef094b175919f87ab7dd1948c8841cd95503bd0fe150e9abde0d67a7**, 579 lines (v1 read: ae1bd10e, 446
  lines). It is untracked and not in `SHA256SUMS`; the commit form is CC-294 Ruling 6 (D5).
- Run:
  - `PY=~/.venvs/c_pvr_cider/bin/python`
  - `$PY -I -B scripts/c_pvr/c_pvr_cider_vi.py score --out $PULL/final/c_pvr_out --sums SHA256SUMS_tier1 --build $O
    --tman $TMAN --res DIR`
  - Then `c_pvr_score.py score … --cider DIR/cider_vi.json --cider-sha <files."as_written (gating; --cider)".sha256>`.
- `selftest`, run here: "selftest ok (kit = pycocoevalcap; text route; 3-set world; 14 FAULT cases; range)", about 9 s.
  It uses synthetic text only, with the real pinned RDR on made-up sentences (PINS-A precedent).
  - Kit = pycocoevalcap, and 1000 is attainable. The range check passes 0 and 1000 and FAULTs on 1000 + 1e-9, −1e-12
    and NaN.
  - The text route: NFD and multi-space input give NFC tokens, output is lower case, segmentation happens before
    lower case, `lower` not `casefold`, and stripping is trailing-only.
  - A world in which:
    - the manifest order differs from sorted order;
    - the reference files hold confirm-half and unrelated extra images;
    - xm PVR-drop has two empty captions;
    - xm A0 has one NFD caption, and one XM reference is NFD.
  - In that world:
    - every arm's as-written and stripped values equal pycocoevalcap with DF over the scored references only;
    - the arm set equals `cider_in`'s need list;
    - the empty captions score 0 and are counted;
    - the NFC counts are exact;
    - the §5 block is recomputed from the stripped file;
    - the `jdk` record holds 21.0.12.1, the real `java` path and the VNC_PINS;
    - an existing output is not overwritten.
  - **14 FAULT cases:** confirm-half id, partial arm, reference sha, TMAN, manifest id without a reference, a stand-in
    `java` reporting 21.0.13 first on PATH (W1), and the 8 custody cases of N1. The N1 cases are SUMS mismatch, torn
    last line, manifest sha, manifest label, extra key, wrong arm, repeated id and repeated SUMS line.
- `mutants`, run here: **28 of 28 killed**. These are the 13 of v1, plus:
  - no_jdk_check and jdk_skipped (W1);
  - range_exclusive (N5);
  - the 8 custody forms of N1;
  - empty_dropped and strip_desc_as_written (N2);
  - lower_first and casefold (N6).
  - Four mutants die by a KeyError, not by an assertion message. They differ in what a real run would do:
    - partial_ok and refs_unfiltered die in `per_image`, before any write. They fail safe and write no file.
    - no_A0 dies in `descriptive()`, after `cider_vi.json` and `cider_vi_stripped.json` are written (the `files`
      entry of the record is evaluated first). Only the record is missing. Downstream it is still refused, because
      the committed `cider_in` FAULTs on a file without `xm3600_vi.A0`. (v1 §10 said "write no file" for no_A0; that
      was wrong and is corrected here.)
    - jdk_skipped would complete in a real run and write all three files without the JDK check. The KeyError is the
      selftest's own `rec["jdk"]` assertion, so this is a test kill, not a fail-safe.
- **The judge's 16 hand mutants** (`~/cc294_hand/run.py`, run unchanged against this file): **15 KILLED**, including
  all 10 non-equivalent survivors of round 1 and lower_first and casefold. `no_clean_ws` survives; it is equivalent,
  because the tokens are unchanged (CC-294 Ruling 1 (b)).

## 11. CC-293's recommendation, checked against the files (CC-294 Ruling 1: CONSISTENT)

| claim | result |
|---|---|
| kit_b `protocol_pilot.Cider` 6aee4282, sha-checked loader in c_stage1/score.py | **holds**: KIT_B l.39-40, `kit()` l.47-60; file tracked at HEAD and byte-equal to the zenodo copy |
| it is the pycocoevalcap CIDEr-D, σ = 6, ×100 | **holds**: read line by line against the pycocoevalcap 1.2 wheel source, and equal to 1e-12 in the selftest |
| segmentation CP.rdr = the PINS-A VnCoreNLP 62bbc58f jar / rdr / vi-vocab | **holds**: VNC_PINS = PINS-A l.221-223, re-hashed on every call; the JDK is now asserted too (§3) |
| lower case | **holds** (house `str.lower()` after segmentation; both are asserted) |
| default DF = G-7 | **holds by construction** (§6; CC-294 Ruling 1 (d)) |
| G-6 SD basis = `score_ci.per_image_cider` → `rescap.metrics._tokenize_vietnamese`, RDR `segment(strip).lower()`, punctuation kept, pycocoevalcap σ = 6, ×100, IDF over the scored set | **holds**: metrics_v2.py l.59-66 (SCALE = 100, score_ci l.39), score_ci l.72-84, metrics.py l.400-402 |
| gate on as written; stage 1 decided on stripped | **holds**: c_stage1/score.py l.10-11, l.164-165, l.265 |
| producer in its own venv with scipy, lock recorded | **done** (§9) |
| arms | **holds**, equal to the scorer's `cider_in` need list, xm A0 included (CC-293 N5) |

Disclosed differences (all ACCEPTED by CC-294 Ruling 1 (b)):

- **(a) NFC is added.** Neither precedent normalises. RDRSegmenter keeps NFD input as NFD, so NFC changes the scores
  only for non-NFC text. The size of the change is measured at S16 by the `changed_by_nfc` counts (§7).
- **(b) The jar route differs from the G-6 basis.** The G-6 numbers came through `py_vncorenlp`. This route is the CLI
  over pipes (PINS-A l.226). It uses the same VnCoreNLP-1.2 RDRSegmenter, here sha-pinned. No equality run was made,
  because py_vncorenlp is absent, so this stays a disclosed caveat beside the SD basis.
- **(c) `CP.clean` is added.** Its whitespace collapse does not change the tokens. `CP.rdr` reads the words from the
  column output, and the marker parse does not depend on newlines (hand mutant no_clean_ws is equivalent). Its stated
  roles are NFC, and one cleaned text per input, which is the key of the single de-duplicated RDR pass. (Reworded per
  CC-294 N4. v1's claim that it stops a newline from shifting the marker alignment is withdrawn.)
- **(d) The scorer changed under this draft** (§8). The §8 contract holds at 7fe4a080.

## 12. Decisions (status after CC-294)

- **D1. A partial or absent CIDEr arm: RESOLVED by CC-293r2 W4** (CC-294 Ruling 1 (f)).
  - The producer keeps FAULT-and-write-nothing on any partial or absent arm.
  - The scorer has the explicit `--no-cider "<reason>"` path, valid only when the pulled SUMS is not
    `SHA256SUMS_tier1`.
  - On that path the §6.3 variant, the §12 (iv) go rule and the decision are NOT_DECIDED; a headroom STOP still takes
    precedence; and C-M1/C-M2 are NOT_RUN.
  - CC-293r3 Ruling 3 binds the path to a producer FAULT on the same pull (§8). If the producer succeeds, `--cider` is
    mandatory.
  - Only the completeness FAULTs ("… no CIDEr-VI file is written") license it. Every other producer FAULT goes to a
    judge (§8, this pin's reading).
  - No producer change is needed.
- **D2. The stripped column is reported as points only: ACCEPTED** (CC-294 Ruling 1 (c)).
- **D3. A literal `_` is left to RDRSegmenter, and its count is printed: ACCEPTED** (CC-294 Ruling 1 (c)).
- **D4. CC-293 PI Q1: CLOSED** by PI-1108d, answered YES (CC-294 Ruling 7).
- **D5. Commit form: RULED** by CC-294 Ruling 6, and it is **Form B**: the scorer committed first (7e24eb6).
  - HEAD `scripts/c_pvr/SHA256SUMS` is 7422ea9f (25 lines; the working copy equals it). It names no cider file.
  - This pin's commit appends exactly two lines to it, `<sha>  scripts/c_pvr/c_pvr_cider_vi.py` and
    `<sha>  scripts/c_pvr/requirements_c_pvr_cider.lock`, at the GO shas.
  - The coordinator stages the append at commit time. This draft adds nothing to SHA256SUMS.
- **D6. JDK hold: none** (CC-294 N8 / PI Q1; sudo is forbidden).
  - The W1 FAULT is the guard, and S16 runs soon after the S15 pull (§3).
  - If the FAULT fires, nothing is written and the case goes to a judge before S16 continues.

## 13. Drafting-touch disclosure (barred paths and data)

**v1 window (about 04:40Z-05:50Z), kept as written in v1 (CC-294 Ruling 3 (i)):**

- **Home-wide `find`.** Three runs of `find / -xdev -name cider_scorer.py` (before 05:10Z), made to locate a local pycocoevalcap,
  walked `$HOME` on the same filesystem.
  - So `find` read the directory entries of `~/c_pvr_out`, `~/s11pull_*` and `~/c_pvr_watch_*` (names only, as a tree
    walk).
  - It opened no file in them and printed no match from them. Its one match was a foreign tool's scratch copy
    (`~/.gemini/…/pyciderevalcap/cider/cider_scorer.py`, vrama91's pyciderevalcap). That copy was not opened or used.
  - After this, only explicit paths were used.
- **Listing and numeric reads.**
  - `ls ~/.venvs/`, `ls`/`find` of `~/.cache/pip`, `ls ~/c_pvr_tools/vncorenlp/`.
  - Reference files of §6: `sha256sum` only. Their `git check-ignore` status was printed.
  - Directory listings of `data/xm3600/`, `data/datasets/xm3600/` and `data/datasets/xm3600/raw/` (spent dev data,
    not barred) printed file names and sizes, e.g. `captions.zip`, `images.tgz`, `image_attributions.csv`,
    `full_data.json`, `test_data.json`. No file in them was opened beyond the `full_data.json` sha.
  - `data/results/metrics_v2/main_s42-short.cider.json` (committed, numbers only): its keys, metadata fields and the
    mean of `per_image["CIDEr-D"]` (17.317, the T1-GUARD §2.3 figure) were printed.
  - `c_pvr_lists.json` l.40-60 (committed): half counts and input shas were printed, plus three TextCaps train ids
    (`t_a_ids`, ids only).
- **Runs.** RDRSegmenter was run on made-up sentences only. A made-up test sentence that matched UIT-ViIC 6-grams was
  replaced before the final NGRAM scan.
- **Network.** `pip download` of three wheels from PyPI into `~/c_pvr_cider_wheels/` (ext4). The pycocoevalcap source
  was read from that wheel.
- Not touched: `~/.vsps_sealed`, `t2pool_*`, COCO annotation files, the host, the a1_decomp files and the a1decomp LOG
  lines. No LOG line was written and nothing was committed.

**v1.1 window (about 06:25Z-07:00Z), explicit paths only (CC-294 Ruling 3 (iv)):**

- Read in full: `.session_backup/2026-10-13/decisions/CC-294.txt` and `~/cc294_hand/run.py`.
- `ls -la ~/cc294_hand/` listed the judge's scratch dir: `run.py`, `scale.py`, `sums_cider_first`. Only `run.py` was
  opened.
- `grep` of the single file `CC-293r2.txt` for W4 / N-H / no-cider lines.
- `grep` of the single file `scripts/c_pvr/c_pvr_score.py` for its CIDEr lines and `cider_in`.
- `CC-293r3.txt`: a `grep` of that one file, then its l.1-2, l.137-152 and l.176-192.
- `git log -3`, plus the sha256 of `git show HEAD:` for the scorer and SUMS (hash and line count only).
- `java -version`, `which java` and `readlink -f` of it.
- RDRSegmenter on made-up sentences only (the N6 and casefold probes).
- The selftest, runner and hand mutants (temp dirs under `/tmp`, synthetic text only); sha256 of this pin's files.
- No `find`, `grep -r`, glob or `du` over `$HOME` or `/`. No LOG line was read or written. Nothing was committed.
  SHA256SUMS was not edited.

## 14. Order before S16

1. Round 2 of CC-294: a one-judge FULL read of this file, the producer and the lock (IRREVERSIBLE 85). Codex is
   optional on the diff.
2. Gatekeeper commit, Form B (D5): the pin v1.1, the producer, the lock, and SUMS = HEAD 7422ea9f plus the two lines.
   Each file is byte-equal to the GO shas. The commit's LOG line carries
   CC-294 Ruling 3 (iii) verbatim: "pin §13 home-wide find disclosed: directory entries only, no file opened, no name
   printed; blind status upheld (CC-294 Ruling 3)". It also states the §8 re-check for whichever commit comes second.
3. At S16: the OPS line of §8 (N7), then the producer, then `c_pvr_score.py score --cider …`. Any later change to the
   form is POST_HOC.

## 15. Changes v1 → v1.1

| change | where | source |
|---|---|---|
| JDK asserted (`"21.0.12.1"` in the first `java -version` line, FAULT otherwise) and recorded with the path and VNC_PINS | §3, §7, §8, §10 | CC-294 W1 |
| 8 custody FAULT cases and mutants | §7, §10 | CC-294 N1 |
| empty pulled captions in the world; §5 expected values from S | §5, §7, §10 | CC-294 N2 |
| `changed_by_nfc` counts (captions per arm, references per set) | §7, §11 (a) | CC-294 N3 |
| §11 (c) reworded; D1 cites CC-293r2 W4 | §11, §12 | CC-294 N4 |
| producer range check [0, 1000] inclusive; equals the scorer's N-H | §7, §8 | CC-294 N5 |
| lower-first and casefold kill cases | §3, §10 | CC-294 N6 |
| S16 OPS line content | §8 | CC-294 N7 |
| no JDK hold; W1 FAULT is the guard | §3, §12 D6 | CC-294 N8, PI Q1 (sudo forbidden) |
| D4 closed; D5 replaced by the ruled commit forms | §12 | CC-294 Rulings 6, 7 |
| §10 KeyError mutants described exactly (no_A0 writes the two cider files; jdk_skipped is a test kill); `--no-cider` licensed only by completeness FAULTs | §8, §10, §12 D1 | v1 §10 error; CC-293r3 Ruling 3 scope |
| §8 re-checked against the committed scorer 7fe4a080 (7e24eb6, Form B); CC-293r3 binding readings on `--cider` and `--no-cider`; D5 = Form B on HEAD SUMS 7422ea9f | §8, §12 D1 and D5, §14 | CC-294 Ruling 6; CC-293r3 Rulings 3, 4 |
| producer sha ae1bd10e → 3401b46c (446 → 579 l.); lock unchanged | §10 | – |
