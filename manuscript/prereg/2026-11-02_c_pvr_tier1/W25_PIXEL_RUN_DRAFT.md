# C-PVR-T1 pixel W25 run document: DRAFT v0 (Paper C, ACM TALLIP; prereg §9.1 step 8)

**Status:** planning draft. Nothing in it has run. No image was downloaded, no code was written, nothing was committed.
Written 2026-11-03 (`date -u` about 11:50-12:20Z), HEAD 2caa802.
- **Label:** TIER 1 / DEV-EXPLORE (C-PVR-T1).
- **What it plans:**
  - the pixel W25 step on C's NoCaps-test and OpenViVQA-dev images (prereg §8, §8.1-§8.3, §9.1 step 8);
  - the count that feeds `n_e_power` = n_e_gb − w25_flagged − lost − 4 (prereg §5.6; PINS-B §2.6, Q-B7; Q11 v1.2
    §9.2 step 5).

**Sources read for this draft:**
- PREREG_DRAFT_v1_2 §0, §4.4, §5.3-§5.6, §7, §8-§11, §14-§15;
- AMENDMENT_CC222 v1.3 (W25 lines);
- PINS_A_DRAFT_v1_4 §4.1, §5, §8, §11-§12, §16;
- PINS_B_DRAFT_v1_1 §2.6, §4-§5;
- Q11_GB_RUN_DRAFT_v1_2 §2-§4, §9;
- CC-220 (B3, B4, NB-W25STOP, NB-LOST, NB-T2POOL, Q-custody), CC-236r3, CC-237 (vi), CC-243;
- STATE_2026-11-03;
- RULE.md of 2026-10-28_w25_neardup;
- `scripts/w25/w25.py` (header, l.1-120, `fetch` workers);
- `scripts/c_pvr/c_pvr.py` 8f10bd60 (header, l.1-110, l.800-920, `main`);
- `scripts/c_pvr/gates.py` 3bced05e (l.55-90, l.750-770, l.970-1010);
- `cen_fetch.get` l.236-252.

---

## 0. Summary

| item | finding |
|---|---|
| Can W25 run now? | **No.** The `w25` subcommand does not exist. CC-236 Q-SPLIT (GO 92) moved `owners`, `lists`, `w25` and `score` from `c_pvr.py` to a second file, `c_pvr_run.py`. That file is not written (PINS-A v1.4 §11, OPEN row). |
| Host | **Laptop CPU only** (prereg §8: the named custody host). No GPU and no rental. **0 VND.** |
| Runtime | about **2.5-6 h** for the whole window [est.], against the registered 24 h wall-clock stop (§8.3) |
| Bytes | NoCaps test: 10,496 OI-test JPEGs, about 3 GB in total [est.], at most 512 at a time in tmpfs. OpenViVQA dev: `dev-images.zip`, 165,039,269 bytes. |
| Gold | **None.** Pixels and ids only. No Open Images label body, no `gb_intermediate.json`, no NoCaps caption, no OpenViVQA question or answer string. |
| Output to n_e_power | w25_flagged (NoCaps test vs earlier owners, RULE §3 C1 ∨ C2 ∨ C3) and lost (§8.1, cap 10). n_e_power = 10,182 − flagged − lost − 4, computed by the pinned `gates.n_e_power`. |
| Blocking gaps | (1) `c_pvr_run.py`; (2) an interpreter ruling, because the `c_pvr` venv has no torch, PIL or imagehash; (3) `owners` frozen; (4) feature caches for XM3600 and ViTextVQA dev; (5) a fetch path for `dev-images.zip`; (6) this run document's read |

---

## 1. What W25 does and what it reads

### 1.1 Purpose
- **Prereg §7.2 rule 3.** A NoCaps-test image that is a pixel near-duplicate of an image of an **earlier ledger owner**,
  or is lost in the W25 fetch, leaves P_obj^VI, R_obj^VI and the local proxy at every tier. It is counted only.
- The same holds for OpenViVQA-dev images and the proxy.
- The W25-flagged count plus the lost count enter n_e_power (§5.6).
- The step produces **features only**: pHash, dHash, mirrored hashes, the SSCD descriptor and sha256. It produces no
  caption, prediction, label or score (prereg §0; CC-153 r1).

### 1.2 Query sets (the images fetched)

| set | ids | source | bytes moved | where the bytes live |
|---|---|---|---|---|
| NoCaps test, G-A remaining | **10,496** = `ga_remaining_ids.txt` (3feccabc, committed). Every id must also be in the official OI test list (`test-images-with-rotation.csv` de55c6b8, sealed under `~/.vsps_sealed/c_pvr/ga/`, ids column only). G-A: `in_oi_test` 10,600, `other` 0, removed 104 (XM3600). | `OI_TEST_URL` = `https://open-images-dataset.s3.amazonaws.com/test/{file}`, imported from `c_pvr.py` (A11; byte-equal to gates.py l.81) and passed to the unchanged `cen_fetch.get`. No substitute source. | about 3.0 GB [est.: OI test is about 36 GB for 125,436 images, so about 0.29 MB per image]. At most 512 per batch, about 150 MB. | `/dev/shm/c_pvr_w25/b<NNNN>/` (tmpfs, mode 0700). Each batch is unlinked once its features exist, and the deletion is logged. |
| OpenViVQA dev | 1,070 image names from `vlsp2023_dev_data.json` (sealed, sha 456c9836). These names are the one string field allowed (CC-237 (vi)). | `dev-images.zip` at HF revision cc85c24c, LFS sha256 ff6a0e87, 165,039,269 bytes (`OVQA_DEV_ZIP`, c_pvr.py l.109) | 165 MB once | `/dev/shm/c_pvr_w25/ovqa/` (tmpfs). Members are extracted at most 512 at a time. The zip is unlinked after the last batch. |

- **W25 runs on all 10,496 ids, not on the 10,182 n_e_gb ids.** Which ids make up n_e_gb is known only inside the
  sealed `gb_intermediate.json`. That file is opened once, at the tier-3 freeze (prereg §9.4), and is never consulted
  here.
- Subtracting the full flagged and lost counts from n_e_gb is therefore **conservative by construction** (prereg
  §5.6): some flagged or lost images carry no mapped label.
- A flagged or lost id may also be one of the 4 `FLICKR_W3` ids. It is then subtracted twice. This is also
  conservative and is disclosed.
- The exact drop is computed only at the single tier-3 open (report-only; PINS-B §2.6).

### 1.3 Comparison side: earlier-owner feature caches (no new pixels of other owners in the window)
- `owners` (prereg §7.1) builds `c_pvr_owners.json` from PORTFOLIO §2.3 at HEAD and from every one-look or spent list
  under `manuscript/prereg/`. Its sha is frozen **before any feature pass**.
- The table below is the inventory known at drafting. `owners` decides the final list. Rule §7.2 (2): T_A and O_B
  (C's non-spent splits) yield to C's test sets, so they are not compared here.

| owner set | cache | sha256 (first 8) | where | status |
|---|---|---|---|---|
| NoCaps val 4,500 (spent dev, C tier-2) | C-EN `feats_nocaps_val.npz` | b69dac29 (C-EN SHA256SUMS_feats) | `.session_backup/machines/M1|M3/root/outputs/c_en/` | present |
| COCO Karpathy test 5,000 (KT-C) | C-EN `feats_coco_test.npz` | 2bc3b83e | same | present |
| KV-5,000 (covers KV-4,224) | C-EN `feats_coco_kval.npz`; also `~/vsps_w25k1/kv5000.npz` | 9783f7a6 / 4e3eac3e (W25-K1 inputs) | same; `~/vsps_w25k1/` | present |
| OIV7 val 41,164 (L2-P1 36,707 + NoCaps val 4,457) | `~/vsps_w25k1/oiv7_val.npz`; M3 `w25/oiv7_parts/` (72 parts) | 2ca7e2f5 (W25-K1 inputs); parts per M3 `w25/SHA256SUMS` | laptop ext4; `.session_backup/machines/M3/` | present |
| UT-2,402 | `feats_ut.npz` | per M3 `w25/SHA256SUMS` | `.session_backup/machines/M1|M3/root/outputs/w25/` | present |
| KTVIC test, OpenViIC test, UIT-ViIC test, T2-2000 | `~/vsps_w25k1/{ktvic_test,openviic_test,uitviic_test,t2}.npz` | cd985050 / f4c79b82 / 4f478490 / 98f61bae (W25-K1 inputs) | laptop ext4 | present |
| COCO gap val2014 734, PASCAL-50S A 1,000, A-T3 val2017 5,000 | B's C7 caches | 72b1de15 / 00ef3975 / 95144514 (LOG l.1317-1319) | `.session_backup/machines/M1/root/b_w25slot/out/` | present |
| **XM3600 (all 3,600; spent dev)** | none found: `emb_xm_*.npz` are CLIP retrieval embeddings, not W25 features | — | images local: `data/datasets/xm3600/images/` (3,600 files) | **missing**: compute on the laptop before the window. Read ids and image files only, never `full_data.json` captions. About 25 min at 0.38 s/img. |
| **ViTextVQA dev (proxy earlier owner, §7.1)** | none found | — | `data/datasets/vitextvqa_raw/` or `l1a_vitextvqa_dev/` (to pin) | **missing**: compute on the laptop before the window. About 10-15 min [est.]. |
| Other PORTFOLIO §2.3 owners (PASCAL-50S full, ADE20K val, AMBER, restval/B4, M0 dev-touched, Objects365 val, ViTextVQA test, MTVQA, VinText, …) | to be listed by `owners` | — | — | **open**: each one is either "cache present at sha" or "computed on its holding host" (§7.4 hosts), or the `owners` ruling records why it is out of scope (for example disjoint by source, with no shared image pool) |

- **Staging.** Before the window, every cache is copied to an ext4 input dir (`~/c_pvr_w25_in/`, mode 0700) and
  checked against a pinned manifest (`sha256sum -c`). The window then does almost no /mnt/d I/O (9p EIO history,
  LOG l.1295).
- **Two counts kept apart (prereg §7.3).**
  - (b) W25-flagged against earlier owners, plus lost: these enter n_e_power.
  - (c) §7.4 self-retrieval against D-VI, D-EN and D-TC: datastore side only, never in n_e_power.
  - The window computes the NoCaps-test features once. (b) is decided by `w25-decide`; (c) is computed later by
    `lists` or the §7.4 step from the same feature file.

### 1.4 What is never touched
- No Open Images label body (`oidv7-*-annotations*`): `refuse()`/`BARRED` is imported from `c_pvr.py` and selftested.
- No byte of `gb_intermediate.json`. It is not even hashed.
- No `/dev/shm/c_pvr_gb`.
- No NoCaps caption file. No `nocaps_val_4500_captions.json`. No `nocaps_test_image_info.json` beyond what G-A
  already pinned.
- No OpenViVQA question or answer string.
- Nobody looks at any image pair (RULE §3, "No visual check").

---

## 2. Is the code pinned and complete?

### 2.1 What is pinned
- `c_pvr.py` 8f10bd6097eb60a56e7f4e4bef9cd5d716fbebaa94ee15e4a7cca139caece120 (SHA256SUMS l.4, A11 commit 9419103).
- Its selftest last passed:
  - in the CC-237 judge re-run (LOG l.1352: selftest ok; mutants 83 killed + 1 equivalent);
  - under the (B) gates.py, OPS-1103c-pinsB-G16 (LOG l.1379, rc 0).
- **Not re-run for this draft** (instruction: run nothing yet). Before the window it re-runs as precondition P3.
- What `c_pvr.py` holds for W25:
  - `OI_TEST_URL` (l.41) and the AST equality check against `gates.py` (l.1327-1328);
  - the OpenViVQA constants (`OVQA_REV`, `OVQA_URL`, `OVQA_DEV_ZIP` l.101-109);
  - `ovqa_count(..., dev_zip)` (l.884-920), which performs identity check (c);
  - `refuse`/`BARRED`, `SEALED`, `LABEL`.
- The W25 functions, unchanged and pinned:
  - `scripts/w25/w25.py` d6d12780 (commit 8f99bc8);
  - `build_memory.features` / `near` (`scripts/c_stage1/build_memory.py` e771b92d at HEAD);
  - `cen_fetch.get` (`scripts/c_en/cen_fetch.py` e51918e9 at HEAD);
  - RULE.md 289c0a59;
  - SSCD `sscd_disc_mixup.torchscript.pt` 9f26bd4c (laptop copy:
    `~/backups/vsps_image_captioning/.session_backup/2026-10-22/c_stage1/`, as in W25-K1 run 2).

### 2.2 What is missing (each item blocks the window)
1. **`c_pvr_run.py`** (`owners`, `lists`, `w25`, `w25-decide`) under Q-SPLIT conditions (i)-(iv) (PINS-A §12):
   - (i) every shared constant is imported from `c_pvr.py`, and the selftest asserts `c_pvr_run.OI_TEST_URL is
     c_pvr.OI_TEST_URL` (amendment v1.3 l.133);
   - (ii) it refuses to run unless sha256(`c_pvr.py`) = 8f10bd60;
   - (iii) its own selftest (synthetic images, a dummy SSCD net, sockets raise, as `w25.py --selftest`) and its own
     mutants;
   - (iv) the renamed command lines.

   It must also carry:
   - the §8 id assert (every id in `ga_remaining_ids.txt` ∩ the OI test list, else FAULT before any request);
   - the §8.1 outcome classes, using `get`'s strings exactly as in the prereg table;
   - the XM3600 sha-refuse backstop (`w25.xm_shas()`, `exclusion.json` c52a96d1);
   - lost caps: more than 10 for NoCaps test is a FAULT, more than 1 for OpenViVQA dev is a FAULT;
   - §8.2 tenancy: pause predicate, flock `/dev/shm/c_pvr_w25.lock` re-checked at every batch, foreign `*_job.sh`
     abort, tmpfs mode 0700, gpu_backup `/dev/shm` check;
   - the §8.3 first-batch projection and the 24 h stop;
   - a trap that deletes **the parent** `/dev/shm/c_pvr_w25`, not only batch folders. This is the lesson from the
     W25 FAULT OPS-1028af: `drop()` left the empty parent behind;
   - each deletion logged in `~/.vsps_sealed/c_pvr/w25_deletions.log`.
2. **Interpreter.** The registered command (PINS-A §12 W6) is `~/.venvs/c_pvr/bin/python ... c_pvr_run.py w25`. That
   venv has **no torch, PIL or imagehash** (checked by `find_spec` at drafting), and `build_memory.features` needs all
   three.
   - `~/.venvs/c_stage1_lists` (pip freeze 1a639a50, the cenfeat freeze of RULE §2 and W25-K1 run 2) has them, but
     has no spaCy and no rapidfuzz.
   - `c_pvr.py` imports only the stdlib at module level (l.19-35). spaCy and rapidfuzz are imported lazily (l.556,
     l.725, l.1141, l.1332), so importing its constants under `c_stage1_lists -I` should work. The `c_pvr_run.py`
     selftest asserts this.
   - Ruling R1a (§8).
3. **`owners` frozen** (`c_pvr_owners.json` sha in a LOG line) and the **cache manifest** of §1.3, including the two
   missing caches.
4. **`dev-images.zip` fetch.** The pinned `ovqa_fetch` (l.828) checks `(size, git-blob SHA-1)` for the three jsons
   and refuses if `ovqa_pin.json` exists. It cannot fetch an LFS zip.
   - `c_pvr_run.py` needs a short fetch built from the imported `OVQA_URL`/`OVQA_REV`, with the `curl_argv` flags
     (-L, --proto-redir =https, --max-redirs 3). It checks `(size, sha256) == OVQA_DEV_ZIP` before any member is
     listed.
   - It then calls the pinned `c_pvr.ovqa_count(dest, SEALED, rule, "c7136a5f…", dev_zip)` in-process for (c). The
     A8 proxy stays barred until (c) passes (CC-237 (vi), CC-238).
5. **`score`.** It is not needed for W25. It needs spaCy and rapidfuzz, so it runs in the `c_pvr` venv. Ruling R1b
   decides where it lives.
6. **The read.** A one-judge read of `c_pvr_run.py` (PINS-A §11 row: own selftest + mutants + read, before `owners`
   runs), then a gatekeeper commit with its SHA256SUMS line.

---

## 3. Host, time and cost

- **CPU only.** The SSCD descriptor runs on CPU torch (RULE §2: "No GPU is used"), as do the hashes. The prereg names
  **the laptop** as custody host for NoCaps-test and OpenViVQA-dev pixels (§8). A rental would need the Q-custody host
  amendment (§8.3; one-judge read, rental id recorded before any pixel moves). It is **not needed**.
- **Runtime anchors.** All measured on this laptop (4 vCPU / 20 GB, tmpfs 11 GB), W25-K1 run 2, `~/vsps_w25k1/run2.log`,
  nice 19:
  - local files, features only: ktvic_test 558 in 224 s, openviic_test 2,001 in 746 s, pool_new 12,857 in 4,905 s.
    That is **about 0.38 s/img**.
  - fetched (COCO host) plus features: uitviic_test 231 in 424 s, t2 2,000 in 3,509 s. That is **about 1.75 s/img**.
  - M3 anchor for the OI bucket: 36,707 OIV7 val fetched and featured in about 1.25 h with `w25.fetch`'s 16 fetch
    threads (LOG l.673).
- **Estimate [est.]:**

  | part | images | rate | time |
  |---|---|---|---|
  | NoCaps test, fetch + features | 10,496 | 0.45-1.75 s/img (OI S3 with threaded fetch, down to the W25-K1 serial-fetch rate) | 1.3-5.1 h |
  | OpenViVQA dev zip + features | 1,070 | 0.4 s/img | about 8 min |
  | Pre-window caches (XM3600, ViTextVQA dev) | about 3,600 + about 1,500 | 0.38 s/img | about 35 min, **before** the window |
  | Window total | | | **about 1.5-5.5 h, plan 6 h** |

  - OI test originals may be larger than COCO images. The first-batch projection (§8.3) logs the real figure, and
    the 24 h stop bounds it.
- **Cost: 0 VND.** The balance stays 798,488 VND. The ≤ 350k VND RTX 4090 cap (PI Q-P1 / A13) is for the **tier-1 GPU
  block** (§10), not for W25. If the PI chose the rental fallback (§8 PQ2): a 4090 at 17,499 VND/h for about 3 h of
  run plus about 1 h of setup ≈ 70k VND [est.], under the cap. It is not recommended: it adds a custody host for zero
  speed need.

---

## 4. Exact commands (to run only after every precondition of §5 and the rulings of §8)

Notation:
- `R=/mnt/d/vsps_image_captioning`
- `FT=$HOME/.venvs/c_stage1_lists/bin/python` (if R1a = (a))
- `CV=$HOME/.venvs/c_pvr/bin/python`
- `SSCD=$HOME/backups/vsps_image_captioning/.session_backup/2026-10-22/c_stage1/sscd_disc_mixup.torchscript.pt`
- `RUN=<sha256 of c_pvr_run.py at its commit>`

Subcommand names marked [proposal] are fixed by the R1 read.

**Before the window (no tenancy needed; no C one-look pixel moves):**
```
cd $R
$CV -I -B scripts/c_pvr/c_pvr.py selftest                                   # P3: "selftest ok ... 8f10bd60"
$FT -I -B scripts/c_pvr/c_pvr_run.py selftest                               # P4: own selftest (dummy SSCD, sockets raise)
$FT -I -B scripts/c_pvr/c_pvr_run_mutants.py                                # P4: all killed or registered equivalents
$FT -I -B scripts/c_pvr/c_pvr_run.py owners                                 # writes c_pvr_owners.json; sha -> LOG
$FT -I -B scripts/c_pvr/c_pvr_run.py owner-feats --owner xm3600 --sscd "$SSCD"         # [proposal] laptop, local files
$FT -I -B scripts/c_pvr/c_pvr_run.py owner-feats --owner vitextvqa_dev --sscd "$SSCD"  # [proposal]
$FT -I -B scripts/c_pvr/c_pvr_run.py stage-inputs --out ~/c_pvr_w25_in      # [proposal] copy caches, write manifest
( cd ~/c_pvr_w25_in && sha256sum -c MANIFEST.sha256 )                       # all OK
```
`lists` (D-VI, D-TC counts; prereg §11 `owners && lists`) can run here too. It does not gate pixel W25.

**Window launch (§5 tenancy; generic tag `OPS-<MMDD>c-w25pause`, concrete tag never written outside its one line):**
```
cd $R
S=$HOME/w25run_<MMDD>
[ ! -e "$S" ] || { echo "LAUNCH GUARD: $S exists"; exit 1; }    # guard checked BEFORE mkdir (CC-243 N3)
mkdir -m 700 "$S"
# pause line appended here (§5.2), then wait >= 2 s, then:
wc -l .session_backup/2026-10-13/decisions/LOG.md > "$S/log_pre.txt"; sha256sum .session_backup/2026-10-13/decisions/LOG.md >> "$S/log_pre.txt"
setsid -f /bin/sh -c 'echo $$ >"$3/sh.pid"; "$4" -I -B scripts/c_pvr/c_pvr_run.py w25 --host laptop --pause-tag "$2" --run-sha "$1" --sscd "$5" --in "$6" >"$3/w25_stdout.txt" 2>"$3/w25_stderr.txt"; echo "rc=$? $(date -u +%FT%TZ)" >"$3/w25_rc.txt"' \
  sh "$RUN" '<the concrete tag>' "$S" "$FT" "$SSCD" "$HOME/c_pvr_w25_in"
```
- **Pid route** (no `pgrep -f`, no `pkill -f`):
  - `SH=$(cat "$S/sh.pid")`;
  - `PY=$(pgrep -P "$SH")`: the only child. No `-x` name filter, because the venv interpreter's comm may be `python`
    or `python3.12`;
  - the fetch threads are threads, not children.
- **Watch** (every 5 min, into `$S/watch.txt`):
  - `w25_rc.txt` exists?
  - `/proc/$PY/stat` state;
  - the count of finished feature parts in `~/.vsps_sealed/c_pvr/w25/parts/` (ids and features, no pixels);
  - `ls /dev/shm/c_pvr_w25 | wc -l` (batch count only, never a file read).
- **Stall rule [proposal]:** no new part for 60 min → `kill -TERM "$PY"` only. The trap deletes `/dev/shm/c_pvr_w25`,
  the abort is logged, and the parts made so far are kept.
- **Resume:** `w25` skips finished parts. The 24 h deadline is written at first start and kept (RULE §4 pattern). A
  resume needs a new pause line (§8.3) and a one-judge read of the cause.

**After the exit (window closed, no pixels left):**
```
ls /dev/shm/c_pvr_w25 2>/dev/null && echo "RESIDUE"                         # must print nothing
$FT -I -B scripts/c_pvr/c_pvr_run.py w25-decide --in ~/c_pvr_w25_in --out manuscript/prereg/2026-11-02_c_pvr_tier1   # one look, CPU
/usr/bin/python3 -I -B -c 'import sys; sys.path.insert(0, "scripts/c_pvr"); import gates; print(gates.n_e_power(10182, F, L))'   # F, L from w25_counts.json
```
- The last line uses the pinned formula. It is **not** retyped. Importing `gates` performs no gate action.

---

## 5. Preconditions and window discipline

### 5.1 Registered by the prereg (§8.2 steps 1-5, §8.3); `c_pvr_run.py` enforces them in code
1. Coordinator pause line: the tag occurs as a whole token in exactly one LOG line, that line's `date -u` stamp is
   earlier than process start, and it names `W25` and a word starting `pause`. No foreign `*_job.sh` is live.
2. Exclusive flock `/dev/shm/c_pvr_w25.lock`, re-checked **at every batch**. A foreign `*_job.sh` → abort, trap-delete,
   logged.
3. `/dev/shm/c_pvr_w25` is mode 0700.
4. gpu_backup scripts contain no `/dev/shm` path, checked once. No rental exists, so no loop runs.
5. One uid. The isolation is procedural. This is recorded.
6. 24 h wall-clock stop. The first-batch projection is logged. Projection or elapsed > 24 h → stop; features are kept;
   Q-custody goes to the PI.

### 5.2 Reused from the G-B window (Q11 v1.2 §2-§4, CC-243); coordinator checklist, saved to `$HOME/w25pre_<MMDD>/pre.txt` (ext4, separate from `$S`), sha in the pause line

| # | check | PASS |
|---|---|---|
| P1 | HEAD clean for `scripts/c_pvr`; `sha256sum -c scripts/c_pvr/SHA256SUMS` from repo root | all OK, including the new `c_pvr_run.py` line |
| P2 | `c_pvr.py` = 8f10bd60, `gates.py` = 3bced05e, `c_pvr_run.py` = `$RUN` | equal |
| P3 | `c_pvr.py selftest` (venv `c_pvr`) | "selftest ok … 8f10bd60" |
| P4 | `c_pvr_run.py selftest` + mutants (venv per R1a) | ok; mutants all killed or registered equivalents |
| P5 | `c_pvr_owners.json` sha = the owners LOG line; `~/c_pvr_w25_in/MANIFEST.sha256` all OK; SSCD = 9f26bd4c; `pip freeze \| sha256sum` of the R1a venv = 1a639a50; `pip check` OK | all |
| P6 | /mnt/d health (C8 of Q11 v1.2): (a) 9p mount; (b) `d_watch.log` shows no FAIL after the last RECOVERED and `d_watch.sh` is live; (c) the pinned `write_new` probe as at LOG l.1405; (d) SUMS under `timeout 120` | all, **within 5 min before the pause line** |
| P7 | C3-style toolchain: re-hash the R1a interpreter and `/usr/bin/curl` within the P6 slot (CC-243 N5); `systemctl list-timers 'apt-daily*'` not due within the window + 90 min | equal; not due |
| P8 | no heavy /mnt/d I/O and no other laptop job: `ps -eo pid,etime,args` shows no rsync, mutants, LaTeX, `git gc`, B/MT4/VSPS-J job, or background agent or workflow (W-k); `/proc/*/cmdline` has no `*_job.sh` argument; the coordinator types no argument ending `_job.sh` in the window | none |
| P9 | residue: `/dev/shm/c_pvr_w25` and `~/.vsps_sealed/c_pvr/w25/` absent (first run); `grep -c 'w25' ~/.vsps_sealed/c_pvr/ACCESS_LOG.tsv` = 0, reading the action field only (`cut -f3`) | as stated |
| P10 | LOG.md strict UTF-8 and ends with `\n`; the concrete tag occurs 0 times before the pause line | as stated |
| P11 | **PI line before P6** (C18 pattern): mains power, sleep off, lid open; Gemini and the other tool (INC-1027a) closed; Windows Update restart deferred for window + 1 h | present (§8 PQ1) |
| P12 | usage: `~/.config/vsps/usage_check.sh` twice, 10 min apart. The coordinator needs headroom only for launch (about 10 min) and for the result lines after the exit, because the run is detached. | 7-day ≥ 10% and 5-hour ≥ 15% at launch [proposal] |
| P13 | OI bucket reachable without reading content: one `curl -sS -I --fail --proto =https` HEAD on the first sorted id's `OI_TEST_URL` | `HTTP/2 200`, `Content-Type: image/jpeg` |

### 5.3 The LOG quiet rule: not carried over as is (ruling R3)
- In G-B, the quiet rule existed because `gates.py` re-read LOG.md before and after each stream. A second tag hit or a
  torn append ended the run (rc 40 / 50).
- `c_pvr_run.py w25` reads LOG.md **once, at start** (prereg §8.2 step 1 asks no more). A full LOG freeze for about
  6 h would stop every paper's logging.
- **Proposed:**
  - (a) other papers' **laptop jobs** stay paused for the whole window (prereg §8.2 step 1);
  - (b) LOG lines from non-job writers (judges, drafters, PI lines) **may** be appended;
  - (c) the concrete tag must stay in exactly one line;
  - (d) append-only proof: `head -n <wc at log_pre> LOG.md | sha256sum` after the exit equals the `log_pre` sha;
  - (e) the first line naming the result is `OPS-<MMDD>c-w25-result`, followed by `OPS-<MMDD>c-w25-resume`.
- Default if R3 is not ruled: the G-B quiet rule as written (Q11 v1.2 §4). The window then runs overnight VN, when no
  writer is active.

---

## 6. Outputs and where each goes

| output | where | holds | goes to |
|---|---|---|---|
| `w25_stdout.txt`, `w25_stderr.txt`, `w25_rc.txt`, `log_pre.txt`, `watch.txt`, `pre.txt` | `$S`, `$HOME/w25pre_<MMDD>` (ext4) | rc, stamps, projection, aggregates | result line; evidence copies to `.session_backup/<date>/c_w25/` with shas |
| NoCaps-test features (`parts/part_NNNN.npz`, then `feats_nocaps_test.npz`) | `~/.vsps_sealed/c_pvr/w25/` (ext4, 0700; files 0400) | ids, sha256, hashes, SSCD vectors. No pixel, no label. | `w25-decide`; later the §7.4 self-retrieval (NoCaps test × D-VI, × D-EN); the tier-3 exact difference. **Never committed, never copied to /mnt/d or a backup path; sha in LOG.** Keeping it means **no second pixel fetch**. A second fetch needs its own ruling. |
| OpenViVQA-dev features (`feats_ovqa_dev.npz`) | same | same | `w25-decide` (proxy side); §7.4 |
| (c) identity result | stdout + ACCESS_LOG row `ovqa-pin read keys/lengths` (written by the pinned `ovqa_count`) | count only: 1,070 distinct names, all in the zip, or a FAULT | closes CC-238 "(c) OPEN until §8 W25"; unblocks the A8 proxy |
| `w25_deletions.log` | `~/.vsps_sealed/c_pvr/` | utc, folder, file count per batch, plus the trap line | mirrored in the result line (count and last line) |
| ACCESS_LOG rows `w25 start` / `w25 end` / `w25 abort <rc>` | `~/.vsps_sealed/c_pvr/ACCESS_LOG.tsv` | action, sha | result line; result read (action and sha fields only) |
| **`w25_counts.json`** (written once by `w25-decide`, `write_new` 0o444) | `manuscript/prereg/2026-11-02_c_pvr_tier1/` | label; code and input shas; `c_pvr_owners.json` sha; n fetched / lost / FAULT per set; lost by class (exception names); truncated count; flagged per owner per criterion (C1, C2, C3) and the union; flagged + lost total; report-only SSCD ≥ 0.5 per owner; OpenViVQA dev the same; (c) result | **result read (R4)** → gatekeeper commit |
| `w25_flagged_ids.txt`, `w25_lost_ids.txt` (NoCaps test); `w25_ovqa_out_ids.txt` | same dir | sorted ids only; **no owner or reason column** (PI-1101o) | R5 (commit vs seal). The tier-3 code needs them to drop images from local metrics, and they are the input of the exact difference at the one sealed open |
| n_e_power | LOG line `OPS-<MMDD>c-ne-power` | 10,182 − F − L − 4 from `gates.n_e_power` | tier-2 prereg §5.6 power (§7) |

---

## 7. n_e_power and what follows

### 7.1 The number
- **n_e_power = n_e_gb − w25_flagged − lost − 4 = 10,182 − F − L − 4**, with F and L from `w25_counts.json`.
- L ≤ 10, otherwise FAULT → PI.
- Upper bound: 10,178 (F = L = 0).
- F is unknown. G-A already removed the 104 XM3600 OI-test ids by id. Remaining pixel duplicates against COCO, Flickr,
  OIV7 val or Vietnamese sets are expected to be few [est., no basis to number them].
- No threshold is set on n_e_power itself (CC-243 Ruling 3; Q11 v1.2 §9.2 step 5). It is the n of the tier-2 power
  draw.
- Report-only: the exact drop of the flagged and lost ids among the n_e_gb ids is computed only at the tier-3 open of
  `gb_intermediate.json` (prereg §9.4).

### 7.2 Tier-2 prereg contents (own prereg; skeleton now, filled after tier 1)

Tier 1 has not run, so SESOI_P, the UNCERTAIN variant and the headroom stop do not exist yet.
- **Frozen tier-1 config:**
  - captioner, verifier, k = 4, prompts, greedy (PINS-A);
  - the §6.3-selected UNCERTAIN variant;
  - SESOI_P (never scaled with n, W5);
  - the A7 rule (Q-A7 (b)).
- **Pools (NB-T2POOL):**
  - NoCaps val 4,500 − 43 XM3600 = 4,457. Every tier-1 dev image is removed by id and by W25. For NoCaps val this
    uses the existing `feats_nocaps_val.npz`, so no new fetch.
  - O_B;
  - the KTVIC and OpenViIC confirm halves.
  - The resulting sizes are stated.
- **Power (prereg §5.6, B1):**
  - P(PASS) = the share of B_out = 500 outer replicates, each drawing **n_e_power** images with replacement from the
    NoCaps-val images with a verified mapped label;
  - inner B_in = 1,000 CIs;
  - seeds 20261103 (outer) and 20261104 + r (inner);
  - a replicate passes iff §5.4 (1)-(3) and the VI-script guard ≥ 0.95 hold for PVR and A8;
  - Monte Carlo SE reported.
- **Gate:** P(PASS) ≥ 0.98 → the tier-3 prereg may be written. Below that, NoCaps test is never touched (§9.3,
  three-tier rule).
- **Also:**
  - the tier-2 PASS of §5.3 (1)-(5);
  - the tier-2 GPU host, cost and cap (not yet budgeted: balance 798,488 − ≤ 350,000 tier 1 ≈ 448k VND left);
  - the ViTextCaps cutoff at this freeze (Q7);
  - the salami guard (A's NoCaps val numbers are never re-reported, Q11 v1.2 §9.2 step 7).

### 7.3 Timeline toward the TALLIP look 01/2027 [est.; every step waits for its GO]

| when (VN) | step |
|---|---|
| 11-04 → 11-05 | write `c_pvr_run.py` (owners, lists, w25, w25-decide) + selftest + mutants; R1 one-judge read; gatekeeper commit |
| 11-05 | `owners` frozen; XM3600 and ViTextVQA-dev caches; staging; this document → v1 + R2 read |
| night 11-05/06 | W25 window (about 1.5-5.5 h, overnight VN); `w25-decide`; result read (R4); commit; n_e_power line |
| 11-06 → 11-10 | Q-custody host amendment (4090, `r_host` 17,499 VND/h → cap ⌊350,000 / 17,499⌋ = 20 GPU-h); GPU lock; host selftest; `c_pvr_job.sh`; LLaVA and CLIP pins; cut-first addendum; speed test; P1 line |
| 11-10 → 11-14 | tier-1 block (≤ 350k VND); `score --tier 1`; SESOI_P, UNCERTAIN variant, headroom, go/stop |
| 11-15 → 11-25 | tier-2 prereg (panel); **top-up needed** before the tier-2 GPU run |
| 11-25 → 12-05 | tier-2 run on NoCaps val + O_B + confirm halves; P(PASS) at n_e_power |
| 12-05 → 12-20 | if P(PASS) ≥ 0.98: tier-3 prereg (irreversible ≥ 92); EvalAI account (Q6) |
| 12-20 → 01/2027 | tier-3 decode; one EvalAI look (≤ 5 named submissions) and the one sealed open; write-up for the 03/2027 submission |

---

## 8. Rulings needed and PI questions

### 8.1 Rulings (each with a recommended answer and a default)

| # | ruling | tier / threshold | recommended | default |
|---|---|---|---|---|
| R1 | `c_pvr_run.py` code read (Q-SPLIT (i)-(iv); §2.2 items 1, 4) | one judge, reversible 90 (PINS-A §11 row) | GO after selftest + mutants + read | no `owners`, no W25 |
| R1a | interpreter for `owners` / `lists` / `w25` / `w25-decide` | inside R1 (stated override of PINS-A §12 W6) | **(a)** `~/.venvs/c_stage1_lists` (freeze 1a639a50 = the RULE §2 cenfeat freeze; `c_pvr.py` constants import stdlib-only; asserted in the selftest). (b) Installing torch, imagehash and Pillow into `c_pvr` changes the pinned lock fd2f0f12 and needs a PINS-A re-pin. | (a) |
| R1b | where `score` lives | inside R1 | **write it later in `c_pvr_run.py` by an insert-only diff with its own read.** Each W25 output records the `c_pvr_run.py` sha it ran under, so a later sha change cannot alter a W25 record. `score` needs spaCy and rapidfuzz, so it runs under `c_pvr`. | same |
| R1c | tenancy code | inside R1 | import `foreign_jobs`, `STAMP` and `write_new` from the pinned `gates.py` 3bced05e. The W25 pause predicate is `pause_ok` with `W25` in place of `G-B`. That literal is hard-coded at gates.py l.989, so a small second predicate is needed; mutants cover it. | same |
| R1d | `retry_truncated` for NoCaps-test and OpenViVQA-dev decodes | inside R1 | **False**: the literal "unchanged W25 feature code" of §8.1 (= RULE / `w25.py`). A truncated body counts as lost, which is conservative and under the cap. The truncated count is reported. (CC-193 used True for W25-K1 training pools, a different role.) | False |
| R1e | `dev-images.zip` custody | inside R1 | tmpfs only (`/dev/shm/c_pvr_w25/ovqa/`), unlinked after the last batch ("same tmpfs rule", §8). Tier 3 re-fetches it under the LFS sha. | same |
| R2 | this run document v1 (commands, P1-P13, stall rule, R3 form) | one judge, reversible 90: no gold is touched; the rule, thresholds, caps and host were fixed at registration (≥ 92). Escalate to a **full panel at 92** on any FAULT, abort, lost > cap, 24 h stop, or any departure from RULE §3. | GO | the window does not open |
| R3 | LOG quiet form (§5.3) | inside R2 | relaxed form (a)-(e) | G-B quiet rule as written |
| R4 | result read of `w25_counts.json` + id lists + deletions + ACCESS_LOG rows; gatekeeper commit; n_e_power line | one judge, reversible 90 (CC-243 pattern) | GO if no FAULT and the deletions and trap line are complete | full panel at 92 on any FAULT or abort |
| R5 | custody of the id lists | inside R4 | **commit** the ids-only lists (precedent: `ga_remaining_ids.txt` committed; public image ids, no gold, no reason column) | sealed on ext4 with the sha in LOG |
| R6 | earlier-owner scope | inside R1 (the `owners` output) | every PORTFOLIO §2.3 owner and every spent list: cache present at sha, or computed (XM3600, ViTextVQA dev), or recorded as out of scope with its reason | no window until every owner row is closed |

### 8.2 PI questions (each with a recommended answer and a default)

| # | question | recommended | default |
|---|---|---|---|
| PQ1 | May the laptop run C's W25 window for about 6 h (overnight VN), with other papers' laptop jobs paused, on mains power, sleep off, lid open, Gemini and the other tool closed, and the Windows Update restart deferred? (It becomes P11.) | YES; start about 22:00 VN after the R2 GO | the window does not open until the PI line exists |
| PQ2 | If the first-batch projection exceeds 24 h, or the 24 h stop fires: does PI-1102a's Q-custody YES cover moving the rest of W25 to a dedicated rented 4090 (host amendment, one-judge read, about 70k VND [est.])? | YES, as a fallback only | stop, keep the features, ask the PI (§8.3) |
| PQ3 (FYI, not blocking W25) | C beyond tier 1 needs a top-up (C total about 2.7-3.4M VND [est.], prereg §10.2; balance 798,488) before the tier-2 GPU run (about 11-25) | plan a top-up after the tier-1 GO | no C spend beyond the tier-1 cap |

---

## 9. Touches during drafting (`date -u` 2026-11-03 about 11:45-12:20Z)
- **Read (text):**
  - the sources listed at the top;
  - LOG.md by grep (W25, selftest lines);
  - PORTFOLIO §2.3;
  - `ga_counts.json` and `gb_counts.json` (committed counts; keys and five scalar fields);
  - `ovqa_pin.json` and `ovqa_count_rule.json` (names, sizes, hashes, key names);
  - `~/vsps_w25k1/{check.json, run2.log, deletions.log}` and file mtimes (no gold).
- **Ran (read-only):**
  - `sha256sum` of `c_pvr.py`, `gates.py`, `w25.py`, `build_memory.py`, `cen_fetch.py`;
  - `find_spec` probes of the two venvs;
  - `nproc`, `free`, `df /dev/shm`;
  - `find` limited to `.session_backup/machines/{M1,M3}`, `~/vsps_*`, `~/backups`;
  - `ls` of dataset dirs (names and counts only).
- **Not run:** `c_pvr.py` (no selftest, no subcommand), `gates.py`, `w25.py`.
- **Not opened:** any Open Images label body; `gb_intermediate.json` (not hashed, not stat'ed); any NoCaps data or
  caption file; `nocaps_val_4500_captions.json`; any OpenViVQA json; `ACCESS_LOG.tsv`; XM3600 `full_data.json`.
- No image was downloaded. Nothing was committed.
