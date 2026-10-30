# MT4 Branch K1+K6, W25-K1 amendment (DRAFT): input glue and the §4 correction

**Status:** v2, binding at the gatekeeper commit (CC-192), 2026-10-30, with the CC-190 fixes W1 to W5 and W7 applied. Written at HEAD c9a9054, before any W25-K1 feature or `w25k1_decide.json` exists. No
W25-K1 step has run. No image of UIT-ViIC test or T2 has been fetched. No caption, gold file, prediction or score was
opened. CC-190 (panel 3/3, 90.7) ruled GO-with-fixes for the reversible steps. This version binds only after the
one-judge diff read (CC-190 W8, request `.session_backup/2026-10-30/w25k1_diffread_request.md`) and the gatekeeper's
commit, with `scripts/mt4_k1k6/w25k1_prep.py` added to `scripts/mt4_k1k6/SHA256SUMS`.

**Sources:**
- DEV_RULE §4 (sha 685e4dd6) and §2 (c);
- CC-175 r5 (reuse of `feats_ut.npz` and `oiv7_parts` for W25-K1 only), J-3 and Q3 (XM3600 by sha only);
- CC-189 W6 (W25-K1 runs after the W1-W5 commit, with the T2 carve frozen at HEAD);
- W25 RULE §1, §3 and §5 (`2026-10-28_w25_neardup/RULE.md`);
- CC-153 r1 and r4;
- CC-190 rulings 1 to 8 and W1 to W8;
- PI-1030f (LOG l.894: dev sets matched by exact sha or id only, for new preregs) and the PI's answer to CC-190 Q2.

**What it changes:** it adds one glue script and corrects one sentence of DEV_RULE §4.

**What it does not change:**
- the rule (W25 RULE §3: C1 ∨ C2 ∨ C3);
- the sets of the §4 table;
- the XM3600 narrowing (J-3);
- the outputs, the O_EXCL writer and the HOLD;
- `k1k6.py`. It stays frozen at c9a9054, sha 4b511444 (`scripts/mt4_k1k6/SHA256SUMS`; 5b73fb81 was the pre-commit
  file and is superseded, CC-190 W1). Every new feature row comes from the glue `feats` (CC-193).

## 1. The gaps (found by the operator at HEAD c9a9054)

1. **Images.** UIT-ViIC test (231) and T2-2000 are not on the laptop. `k1k6.py w25k1 feats` reads only a local
   `--images` folder.
2. **Lists.** No code writes the per-set `id<TAB>path` lists that `feats` reads: the KTVIC and OpenViIC train pool,
   the KTVIC, UIT-ViIC and OpenViIC tests, and T2.
3. **Pool file.** `decide --pool` takes one npz. The reused `feats_ut.npz` (17d3ebf0) has integer ids, while the pool
   keys are `uitviic:<id>`, `ktvic:<id>` and `openviic:<stem>`. The re-keying and the concat were never written. A
   key drift would make every exclusion a silent no-op, because `cmd_pool` filters on exact strings.
4. **OIV7 side.** `decide --sets` names each set by its file stem. The OIV7 val set is 72 W25 parts plus C-EN's
   `feats_nocaps_val.npz`. That raw file still holds the 43 XM3600 NoCaps rows, so passing it unchanged would compare
   XM3600 perceptually and break J-3 and CC-153 r4. W25 drops those rows inside `w25.inputs()`, and nothing in K1+K6
   called it.
5. **§4 text.** DEV_RULE §4 says that "every test-side image is already on the laptop". That is wrong for UIT-ViIC test
   and T2 (§3 below).

## 2. The glue: `scripts/mt4_k1k6/w25k1_prep.py`

- **sha256:** `f465c2a651acdea22aeadb8ce64a502402a245146b9f0e5a35fa8ae8e7cc87b5`.
- **Selftest:** `python3 w25k1_prep.py --selftest` fails under `-I` with system python; it passes under `-I` in a venv that has numpy (CC-192 ran c_stage1_lists).
  It needs no torch and uses synthetic data. It checks:
  - re-keying, the drop of the K2-W25 ids and row alignment;
  - that a key drift FAULTs;
  - that the tmpfs folder is gone after success, after a wrong sha, after a lost image and after a crash inside the
    features step, and that no output is written in the failure cases;
  - that a caption sentinel in the release JSON reaches no returned row;
  - that a T2 body whose sha differs from its C-EN memory row, or is a refused image, FAULTs and writes nothing;
  - that `check` FAULTs on a missing or extra set, a wrong count, a duplicate id or a pool key that is not a
    `pool_rows` key;
  - that `parity` FAULTs when one hash bit differs;
  - that a work folder inside the repository is refused.
- `k1k6.py --selftest` still passes.
- **Work folder:** WORK must be outside the repository (REFUSED otherwise). Feature files are never committed (§4).
- **Reads:** ids, file names, image sha256s and features only. It never reads `kv4224.txt` or any `*_gold.json`, and
  it never calls `cmd_gold` or `cmd_stage`. Release JSONs are parsed by the loader. Caption text is never printed or
  written, and `pool_rows` tests caption presence only (to count references). Annotations of `instances_val2014.json`
  are never accessed.

| Subcommand | Does | Checks |
|---|---|---|
| `lists` | `pool_new.tsv`: the KTVIC train and OpenViIC train rows of the frozen `k1k6.pool_rows(data, w25_ut, ∅)` (12,857 = 3,769 + 9,088; keys never re-implemented); `ktvic_test.tsv` (558); `openviic_test.tsv` (2,001) | KTVIC test: every file sha = `data/lb/sets/ktvic_test.tsv` (pin 456243c0, the exclusion.json source). OpenViIC test: every file sha = `2026-10-25_c_test/ov_test_files.tsv` (pin 99d4fc49, C test PREREG l.15). `w25_excluded_ids.txt` pin f6151d28 |
| `fetch --set uitviic_test` | each image's release `coco_url` (`uitviic/test_data.json`, pin 54abc0fb) goes to `/dev/shm/k1k6_w25k1/uitviic_test`; glue `feats` (CC-193); unlink and a `deletions.log` line, also on failure | every body's sha256 must be in exclusion.json `image_sha256.uitviic_test` (exclusion.json c52a96d1), else FAULT and not written; 231 images; a lost image is a FAULT |
| `fetch --set t2` | the same, with the `coco_url` of the 2,000 `t2_ids.txt` ids (via `k1k6.set_ids("t2")`, pin 298ae5e1) from the pinned `instances_val2014.json` `images[]` (e1b4d1bc), as `cmd_stage` does; no host is written in the code | **positive pin:** every body's sha256 must equal its row of C-EN `fetch/memory.sha256.tsv` (pin 553fb604; 2,000 of 2,000 T2 ids present), else FAULT and not written. **Also** no body may be a refused image: any exclusion.json `image_sha256` list, or the C-EN test-side records (`coco_test`, `coco_kval`, `nocaps_val` sha tsv; a missing record is REFUSED). A lost image is a FAULT |
| `pool` | `pool.npz` = `feats_ut.npz` (pin 17d3ebf0) re-keyed to `uitviic:<id>`, minus the 10 K2-W25 ids, then the new `pool_new.npz` | key set = the frozen `pool_rows` keys exactly, no duplicate, no unreadable; n = 15,249 (§2 (c)) |
| `against` | `kv5000.npz` and `oiv7_val.npz` from W25's own `w25.inputs()` (C-EN features at their pins, KV ids = kv5000, the 43 XM3600 NoCaps rows dropped by id) plus the 72 parts | every part sha = the W25 `SHA256SUMS` line; OIV7 rows = 41,164 exactly (W25's lost count was 0) |
| `parity` (CC-190 W7) | the first 50 sorted UT-2,402 ids, fetched by their release `coco_url` (`uitviic/train_data.json`, pin 441d22d2) to tmpfs, featured by the glue `feats` (CC-193) in the laptop venv, unlinked; the parity file is deleted after the comparison | every body's sha = its `feats_ut.npz` row; pHash, dHash and both mirrored hashes exactly equal and SSCD cosine ≥ 0.999 on all 50 rows, else FAULT and back to the judge. Reported as a reproducibility check |
| `check` (CC-190 W4) | run immediately before `decide`; prints the input shas and the exact `decide` command | WORK holds exactly `pool.npz` + the six stems (`pool_new.npz` may stay): kv5000 5,000, oiv7_val 41,164, ktvic_test 558, uitviic_test 231, openviic_test 2,001, t2 2,000; `pool.npz` n = 15,249 with keys = the `pool_rows` keys; no duplicate id and 0 unreadable in any file |

**T2 sha (CC-190 W3).** The first, positive pin of the T2 bytes is C-EN's `fetch/memory.sha256.tsv` (sha 553fb604,
112,320 lines; the M1 and M3 mirrors are byte-identical). It holds a row for each of the 2,000 T2 ids. Every fetched T2
body must equal its row. The refused-image check stays as a second check. MT4 PREREG AMENDMENT_2 must require the tier-2
stage manifest to equal this record, else FAULT.

**UIT-ViIC test sha.** `data/lb/sets/uitviic_test.tsv` col 3 equals exclusion.json `image_sha256.uitviic_test`, 231 of
231 (CC-190).

**Dry check (laptop, 2026-10-30, outside the repository):**
- `lists` gives pool_new 12,857 (ktvic 3,769, openviic 9,088), ktvic_test 558 and openviic_test 2,001, and every sha
  matches.
- `against` gives kv5000 5,000 and oiv7_val 41,164.
- `fetch_rows` alone (no fetch): UIT-ViIC test 231 and T2 2,000 URLs, all on one COCO image host. The T2 memory record
  loads at its pin with 2,000 of 2,000 ids. The C-EN test-side records load (14,500 shas, 14,081 beyond
  exclusion.json). The parity rows are 50 UT ids (368 to 8297).
- `pool` end to end on the real `feats_ut.npz` (17d3ebf0) with a zero-feature stand-in for `pool_new.npz` gives
  n = 15,249. The stand-in output was deleted.
- No `fetch`, `feats`, `parity`, `check` or `decide` was run.
- **Shas re-verified with sha256sum (2026-10-30):** k1k6.py 4b511444, DEV_RULE.md 685e4dd6, t2_ids.txt 298ae5e1,
  exclusion.json c52a96d1, instances_val2014.json e1b4d1bc, ktvic_test.tsv 456243c0, ov_test_files.tsv 99d4fc49,
  uitviic test_data.json 54abc0fb, uitviic train_data.json 441d22d2, w25_excluded_ids.txt f6151d28, feats_ut.npz
  17d3ebf0, feats_coco_kval.npz 9783f7a6, memory.sha256.tsv 553fb604.

**Order (laptop, CPU, venv-cenfeat clone per O-3; M1 is refused, CC-190 ruling 7).** All steps but the last are
rerunnable.
0. Environment gates (CC-190 W6): `sha256sum -c scripts/mt4_k1k6/SHA256SUMS` OK; pip freeze sha = 1a639a50;
   `pip check` passes; SSCD weights = 9f26bd4c. All of them go in the run LOG line, otherwise FAULT before any `feats`.
1. `lists`
2. `parity` (W7). On a FAULT, stop and go back to the judge.
3. glue `feats` (CC-193) for pool_new, ktvic_test and openviic_test (images = `data/datasets`)
4. `fetch` for uitviic_test and t2
5. `pool`
6. `against`
7. `check` (W4)
8. the one `decide`, only after the CC-190 re-score at ≥ 92:

   `k1k6.py w25k1 decide --pool W/pool.npz --sets W/{kv5000,oiv7_val,ktvic_test,uitviic_test,openviic_test,t2}.npz`

The file stems are the set names in `w25k1_decide.json`. The venv-cenfeat clone does not exist on the laptop yet;
system python has no torch.

**Crash between the two writes (CC-190 N1).** `decide` writes `w25k1_excluded_keys.txt` before the O_EXCL json. If it
crashes with no json, the keys file is deleted, the event is logged, and the run is never repeated silently: it goes
back to the judge.

## 3. Correction of DEV_RULE §4 ("Where")

**Replaces** "Every test-side image is already on the laptop and never goes to M1" with:

> KTVIC test and OpenViIC test are already on the laptop and are read in place. UIT-ViIC test and T2-2000 are fetched
> from their COCO `coco_url` into laptop tmpfs (`/dev/shm/k1k6_w25k1`) as in W25 RULE §5. They are sha-checked in
> memory (§2), featured, then unlinked, and every deletion is logged. KV-5,000 and OIV7 val are reused features only,
> and no byte of them is fetched. No test-side byte ever goes to M1.

The rest of §4 is unchanged, including the 5.4 h wall cap charged to the test line and the 0 GPU-h.

**Scope of the T2 hold (CC-190 W5, ruling 4).** CC-175's "any T2 byte" and DEV_RULE l.16 ("any T2 image" before the
first tier-2 step) cover two things:
- T2 staging, decoding or training for a K1, K6 or base8_s system;
- any T2 byte on M1.

Exclusion-only perceptual features in laptop tmpfs fall outside that hold (CC-175 l.35, CC-189 W6, DEV_RULE §4
l.128). The bytes exist only in tmpfs and are deleted after the features. No system sees them. The T2 gold is not read.
T2 is frozen at HEAD.

**PI-1030f.** PI-1030f (dev sets: exact sha or id match only, for new preregs) came after DEV_RULE had been drafted
and before its commit. T2 is a dev set. CC-190 Q2 asks the PI whether T2 keeps the committed full near-dup screen;
the default is YES, and the committed §4 stands. The PI's answer is written here before `decide`:
PI answer to CC-190 Q2: none received by 2026-10-30T14:41Z; the default YES applies (CC-192). CC-190 Q3: the default accept
applies. If the answer is NO, T2 is matched by C1 sha against the memory
record only, no T2 byte is fetched, and §4 needs a further amendment.

## 4. What W25-K1 fixes, and why one run is enough

- **What it fixes:** the composition of the K1 training pool. `w25k1_excluded_keys.txt` is the list of pool keys that
  `cmd_pool` drops before every tier. Exclusion counts are reported per set (§12).
- **What it is not:** it is not a test look. No system is decoded or scored. No caption, gold or prediction is read. No
  pair is ever shown to anyone. Descriptors are not model outputs (CC-153 r1). The rule is fixed (W25 RULE §3) and can
  only shrink the pool (CC-175 r5). There is no threshold to choose after seeing outputs.
- **Why one run is fine:** the rule, the sets and the code are all fixed before the run, so a second run would give the
  same keys. The run makes no choice that depends on a result.
- **Tier.** `decide` is one-shot by O_EXCL, and its output gates every tier. A reversal after tier 1 voids every later
  tier (CC-175 Q3: rerun fresh, disclosed). The draft therefore asks for the **irreversible band (≥ 92)** for the
  `decide` step and the §4 correction. The glue script and the rerunnable `lists`/`feats`/`fetch`/`pool`/`against`
  steps are reversible (≥ 90). CC-190 confirmed this split (ruling 6). The panel's 90.7 does not reach 92, so `decide`
  waits for the re-score after the diff read, the W6 environment gates, W7 parity on 50 of 50 rows, the W3 pin on 2,000
  of 2,000, the W4 check, and the PI's Q2 answer or its default.

## 6. Truncated files (CC-193)

- **The files.** Four OpenViIC files fail a strict PIL decode with "image file is truncated":

  | Set | Id | Bytes not processed | File sha256 |
  |---|---|---|---|
  | openviic_test | 00000000768 | 18 | 404866ae511c2bfaa52339a40814316b916fb9d031c60d78f0da6d94d2ce733d |
  | openviic_test | 00000001010 | 155 | 96f9a3ab12df1c9be676dfd82b015559cf10073d49448db7c0cd073f00c264e7 |
  | openviic_test | 00000005095 | 76 | 7f00285e59dc0bac1278060d02a9d39d5d9113b1fc73dc5525b49f3d822d6569 |
  | pool_new | openviic:00000007169 | 1 | 4859dd1fc17d928fed15035b69c9964401cf327b33d4ca04b161b3d252fb9d20 |

  The frozen `k1k6.py w25k1 feats` cannot decode them and FAULTed on the first run (OPS-1030w25k1c).
- **The decode.** The glue `feats` calls `build_memory.features(..., retry_truncated=True)`. This is the CC-082 retry:
  a strict decode first; only on a "truncated (N bytes not processed)" failure, a decode with PIL
  `LOAD_TRUNCATED_IMAGES`, set and reset around that one call. Readable images take the frozen path unchanged. The 3
  test files get the same decode as C's lists, C test PREREG l.77/366 and B-2 Amendment 2.
- **7169 is screened, not dropped.** C's memory dropped it (CC-082 T1). Here it is decoded for the screen only, because
  that is the conservative direction: with finite features it can match a test image and be excluded, and with NaN
  features it would stay in the pool unscreened. The pool stays at 15,249. Its training-time handling is a separate
  rule before the first tier-1 training step (CC-193 W5).
- **FAULT rule.** The glue pins the table above (`TRUNC`). Any of these FAULTs and goes back to the judge, never to a
  retry: an image still unreadable after the retry; a pinned set (openviic_test, pool_new, ktvic_test = none) whose
  truncated record differs from the table; more than 3 truncated files in an unpinned set (uitviic_test, t2, parity);
  a non-finite SSCD row. Each set's `truncated_decoded` record is written into its npz and the run LOG (CC-193 gate g).
- **Determinism (CC-193).** With `LOAD_TRUNCATED_IMAGES`, the RGB pixel sha256 of each file is the same on repeat and
  across PIL 12.3.0 and 13.0.0: 768 15277c96ecd6, 1010 16479f6c87bc, 5095 455cfd604acd, 7169 73c900395281.
