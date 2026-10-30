# C-T2 launch read request (irreversible tier, bar ≥ 92, band 92-98, PI-1029o)

What is asked: may the C-T2 tier-2 rehearsal run on Flickr30K val (1,014 images, its single look) on M1, under
`PREREG.md` and the code below? Running it is irreversible because it spends val's one look. Give several ranked
options (PI-1029o). Panel per the decision-judge protocol (3 judges + Codex); the gatekeeper commits only after a GO.
Nothing has run. Nothing is committed. No preds file and no caption text was opened to write this.

## Files (sha256 at writing; re-check before reading, another tool writes this repo)

| file | sha256 |
|---|---|
| `manuscript/prereg/2026-10-30_c_t2/PREREG.md` | `4e831b23c8314cdb9eb94b0fc5380cf82c43f01f430b145311ddec9bec6b587b` |
| `scripts/c_t2/c_t2.py` | `6113844a378e98fb1ed485f2e064d4708cd4e48612cca4c61efe9e9d49a8c83e` |
| `scripts/c_t2/c_t2_job.sh` | `17ad52273ed37cfa906ce321546481449e2a8ddfbf34af798698d8088170c70f` |
| base: `scripts/c_t1/c_t1.py` (unchanged) | `022af90e143e91161ed594d67248aaddf80209430762b060185b14b59d501dfa` |
| base: `scripts/c_t1/c_t1_job.sh` (unchanged) | `86351ee131254ccfbae5e96416384cae02e749b176c7cfc2c6e4c0a25b20d731` |
| `T1_SUMMARY.json` (decision anchor, 0bf52da) | `7d5b291856d2d499b914dba5054864e02ee350dc98b4459e97b1ece52b9dfda6` |
| carve ledger `carve_coco.jsonl` (pooled; pinned in c_t2.py) | `4ced15b41c3efabfd6d69722a8c2008c8287597f69fc3a5ce18a4d4ab01b5615` |
| ruling `CC-191.txt` | `.session_backup/2026-10-30/rulings/CC-191.txt` |

## How to read the code change (W1)

```
diff scripts/c_t1/c_t1.py scripts/c_t2/c_t2.py
python3 scripts/c_t2/c_t2.py --selftest      # CPU; also rerun python3 scripts/c_t1/c_t1.py --selftest (unchanged)
bash -n scripts/c_t2/c_t2_job.sh
```
`c_t2.py` is a copy of `c_t1.py`. The tier-1 files are not edited, so the tier-1 record and its SUMS stay valid.
The diff has 82 removed and 312 added lines. Of the added lines, about 230 are new code (the `t2` and `dupcheck`
commands and `selftest_t2`); the rest are edits to existing lines.
- **Admission of val, refusal of test:** a new `f30k_names(part)` admits carve, memory and val and refuses
  everything else (test). `items_of`, `img_folder`, `cmd_embed` (its `set|` key prefix, now set for f30k_val too),
  `store` (new `val_refs`, reads only `split == val` rows) and `extract` (new `extract_want`: the 1,014 val members
  only, into `c_t2_f30k_val/images/`) all go through it. `SETS` and `F30K` gain `f30k_val` and never a test entry.
- **Isolation (AMENDMENT_1 logic, unchanged in form):** `refused_names()` is now the 1,000 test names, not the
  2,014 val + test names. `ISO_DATASETS` gains `c_t2_f30k_val`, `out_ok` moves to `/root/outputs/c_t2` (tier-1
  outputs are now denied), and `dupcheck` is added to the hooked commands.
- **Labels and cost:** `LABEL` is `TIER 2 / DEV-CONFIRM (C-T2)`. Run ids take the prefix `t2_`. `CAP_S` is 3.0 GPU-h
  and `BLOCKS` holds the tier-2 estimate. The schema string is kept, so the scorer reads the files unchanged.
- **Summary:** the per-set column builder is moved, without change, out of `cmd_summary` into `set_columns`, so `t2`
  reuses it. `cmd_summary` now also skips `f30k_val`, which means the tier-1 NOMINATE/DROP labels never apply to val.
- **New `t2`:** applies the five claims (`T2_CLAIMS`), val PASS, pooled P (C3) at m = the number of val passes, once
  (C1), and family = val PASS AND P ≥ 0.98 (C2). A claim with a missing arm is NOT RUN. It adds the W2 descriptive
  rows `zs − lmcap_ri` and `ret − zs`. It pins the carve ledger sha, requires all 1,014 val ids, and prints the
  `--exclude` dedup row beside the full result, never in its place.
- **New `dupcheck`:** PI-1030f exact sha256 matches of val against the COCO memory example images, the carve, and
  other val images.
- **Selftest additions:** these cases are refused: test via `f30k_names`, a val list that holds a test name via
  `extract_want`, a staged manifest with a test file via `items_of`, a test file name via the guard, real test names
  via the live hook (in any dir), and tier-1 outputs. A real val name passes the hook and the guard. `cmd_summary`
  skips val. For the decision rule the selftest checks:
  - only the 5 claims exist, and InternVL3 `ret − rand` is never one, even when its rows exist (W4);
  - VAL FAIL, VAL PASS with no margin, and NOT RUN each come out as expected;
  - m comes from val passes, in one pass;
  - the dedup row and the carve-ledger pin work end to end.
- **Job (`c_t2_job.sh`, new, derived from `c_t1_job.sh`):**
  - runs on m3 only and refuses a busy GPU;
  - preflight in this order: HEAD and SUMS, the COCO memory lines of C-T1 `RESTORED_SHA256`, venv freezes, the
    selftest in both venvs, the guard, memcheck (coco), pinsok (Aya, XGLM, M-CLIP), t1check, then dupcheck;
  - then V0 embed and draws, then the V1 claim arms (LMCap ri, Aya ret and rand, Qwen ret and rand, InternVL3 ret),
    then the V2 zs arms (Qwen, InternVL3, Aya);
  - one 3.0 GPU-h cap; any failure stops; nothing is scored on M1.

## Questions with recommended defaults

- **Q-a (C2):** should tier-3 entry require val PASS (CI lower bound > 0) in addition to §8's "PASS with margin"?
  Recommended: YES (PI-1029n: a direction that fails tier 2 never touches test; it adds a single condition). Default:
  YES.
- **Q-b (C1):** m in the pooled P = the number of claims passing val, computed once (conservative, CC-191 r5)
  vs the permissive largest-s reading. Recommended: the conservative reading. Default: conservative.
- **Q-c (C6, PI Q1 of CC-191):** InternVL3 τ = 0.10 declined at tier 2. Recommended: decline. Default: decline.
- **Q-d (W2 cost):** zs of all three backbones at tier 2 (≈0.84 GPU-h, inside the cap) and again at tier 3.
  Recommended: keep. Fallback: decomposition on the carve only, labelled.

## Known ceilings (disclosed)

- aislop on `scripts/c_t2/`: 3 errors (`except SystemExit: pass` in selftest expected-raise checks at copied tier-1 lines 1140, 1168, 1287) and 5 warnings (long functions, file size, `rices_generate` params), all on lines copied byte-identical from c_t1.py; the new lines are clean. Left as is (W1: copied lines unchanged).

- The open() hook sees Python-level opens only (C-T1 AMENDMENT_1 ceiling). Test images never exist as files on M1
  because `extract` reads val members only.
- `dupcheck` compares against COCO members[0] (the shown-example image) only, not every cluster member, and it uses
  exact sha256, not pixels. Near-duplicate search against test is a tier-3 item.
- Rates are tier-1 carve seconds × 1.014. Aya is the largest single item (≈ 2,750 s for ret and rand).
- The M1 rental end date (2027-03-04) comes from the coordinator's brief. The drafter saw no LOG id for it.
