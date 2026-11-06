# Paper C (TALLIP, C-PVR-T1): R-H6 — KT-C pixel fetch plan v1

Status: DRAFT for R-H6 (one judge, REVERSIBLE 85). Not judge-read, not committed. Nothing was fetched, and no network
was used. AI opinion throughout; [est.] marks an estimate.

- Written 2026-11-07 (UTC) on base HEAD 00ed260.
- Basis:
  - CC-280 Ruling 3 (a)-(h), AM3, AM5, WORK LIST steps 2c and 4;
  - PI-1106k (LOG l.1730): "Cho tải, sau khi qua giám khảo". This is a stated departure from the "never fetch test
    images" rule, for this set only;
  - PRE_S11_PLAN_v1.md §4.3 (H6). Where §4.3 and CC-280 differ, CC-280 wins.
- Sources read:
  - cen_fetch.py e51918e9: COCO_URL l.50, `url_ok` l.218-230, `get` l.236-254, REC_LINE / `read_rec` l.257-266,
    RECORD_PINS l.348-351;
  - CC-278 (A3 row timing, A6 absence guard, A7 stop form).

## 1. What and why

- `seal` needs all 6 sets, and kt_c (3,907 COCO Karpathy-test images, SPEED_SET en) has no pixels on the laptop
  (PRE_S11 §4.3).
- K1 (laptop fetch, record-checked) is the route PI-1106k licenses. K2 (fetch on the host) and K3 (drop kt_c) stay
  rejected.
- This plan fixes the source, the list, the checks, custody, logging, retention and the stop rules. It does not fetch.

## 2. Order and gates (CC-280 AM3, WORK LIST 4)

1. The R-P5b commit (it contains the builder `queries` subcommand).
2. The `queries` **ids pass**, which writes the kt_c TSV (`id<TAB>image`, 3,907 rows; the names come from the C-EN
   record). An OPS-<MMDD>c-qtsv line pins its sha.
3. R-H6 GO on this plan, plus a GO on the fetch code (§10). PI-1106k is already given.
4. **H6 fetch** (this plan). Then the OPS-<MMDD>c-ktc pin line.
5. The kt_c **images pass** of `queries`, which reads the H6 dir as its source.

H6 does not wait for H1 or E-G, and E-G never receives KT-C (AM5).

## 3. Pinned inputs (all checked before the ACCESS_LOG row and before any network call)

| input | where | pin |
|---|---|---|
| kt_c TSV (the fetch list) | the path in the OPS-<MMDD>c-qtsv line (ids-pass output, laptop ext4) | its sha in that line |
| C-EN record `coco_test.sha256.tsv` | `.session_backup/machines/M1/root/outputs/c_en/fetch/coco_test.sha256.tsv` (the M3 copy has the same sha) | 614afa1b7cf63bde693fc9692b1699d47ba527d396b7a1216d031b1d50018fdf = cen_fetch RECORD_PINS["coco_test"] |
| fetch helper | `scripts/c_en/cen_fetch.py` (tracked) | e51918e958ad86e832dd34fbf5ed86d2f7fc13cf41b602dfe537afa43af4c673 |

- Record format (REC_LINE): `id<TAB>file<TAB>sha256<TAB>bytes`, 5,000 rows, parsed by `cen_fetch.read_rec`.
- A names-only check, done for this plan: all 5,000 files are named `COCO_val2014_<id:012d>.jpg`, and the record
  bytes total 820,306,454 B for the 5,000. The total for the 3,907 is computed at preflight from the record rows of
  the TSV ids and goes into the OPS line.
- cen_fetch is imported from its sha-checked bytes (module built from the same bytes; the c_pvr_a12.py form). It is
  never re-opened by path.

## 4. The fetch list (CC-280 3(b))

- Exactly the 3,907 `image` names of the pinned kt_c TSV.
- Preflight, before the row, with no network. Any failure = STOP:
  - 3,907 rows, unique ids, unique names;
  - every (id, image) pair equals (id, file) of one row of the 614afa1b record;
  - every name is `COCO_val2014_<id:012d>.jpg`, the `url_ok` rule.
- Never the 5,000. The other 1,093 record rows are the KT_C_OUT owners (uitviic_train_pool ∪ m0_dev_touched_3454 ∪
  a_t3_val2017; a_t3_val2017 = A's tier-3 images). Their names are never requested.
- Never the 54 Karpathy-test files under `.session_backup/machines/O-2308428/.../cv295_dl` (another job's download;
  not read, not copied).

## 5. Source and request (CC-280 3(a), 3(d))

- URL = `COCO_URL.format(filepath="val2014", file=name)`, i.e. `http://images.cocodataset.org/val2014/<name>`. It is
  rebuilt from the row, never read from a file.
- One `cen_fetch.get(url)` per name (`png=False`):
  - urlopen with a 60 s timeout, at most 3 tries;
  - refused if redirected, if the status ≠ 200, or if the body does not start with the JPEG SOI.
- No retry beyond `get`'s own tries, and no second pass in the same run. Sequential, one connection.
- Plain http is acceptable only because every byte string is sha-checked against the record (§7).
- Pixels only:
  - no caption, annotation or instances json, no COCO API / pycocotools call;
  - no HEAD request, and no URL other than the 3,907 above.

## 6. Custody (CC-280 3(e))

- The dir is `K=~/c_pvr_ktc_<MMDD>`: NEW, 0700, on the laptop's ext4, never on /mnt/d.
  - Absence guard first: `[ ! -e "$K" ]`. The script re-checks it (`os.mkdir`, which fails if the dir exists),
    checks that the fs type is ext4, and refuses BARRED paths (`.vsps_sealed|t2pool_`).
  - Files are 0600. K holds the 3,907 images and nothing else. The one exception is a `.tmp_<name>` left by a crash
    during a write: it is never kept, and it falls under O1.
  - The manifest file sits beside K: `~/c_pvr_ktc_<MMDD>.sha256`.
- **ACCESS_LOG hand row**, written by the **coordinator** between the two script runs (§10): after `preflight` passes
  and BEFORE `fetch` (the first GET). It has 5
  tab-separated fields (CC-278 A3 form; no tab inside a field; no token `w25`):
  - utc;
  - `coordinator`;
  - `hand row: KT-C pixel fetch 3,907 (CC-280 R3, PI-1106k)`;
  - the expanded absolute path of K;
  - the full kt_c TSV sha.
  - Row number + log sha after the append go into the OPS line. No agent lists or reads sealed custody.
- Laptop only. The pixels reach HC-1 only inside the sealed arrival manifest (host v3 §4.2: kt_c images pass → seal →
  TMAN → push to tmpfs).
  - Never pushed to E-G (AM5).
  - Never on /dev/shm of the laptop.
  - Never in a backup loop.

## 7. Per-image check before keeping (CC-280 3(c))

1. The check runs **in memory, before any write**: sha256(b) = the record sha AND len(b) = the record bytes for that
   id.
2. On a pass: write `K/.tmp_<name>` (O_EXCL, 0600), fsync, `os.replace` to `K/<name>`, then re-hash the kept file from
   disk.
3. In-memory mismatch: nothing is written; log it (id, utc, "sha" or "bytes"); STOP.
4. On-disk re-hash mismatch: one `rm` of that file (`os.unlink` of that one name); log it; STOP.
5. At the end:
   - file count = 3,907;
   - Σ bytes = the preflight total;
   - the manifest lists every TSV name exactly once.

## 8. Stop rules

| event | action |
|---|---|
| a preflight check fails (§3, §4), or K exists | STOP before the row and before any network call; report the count only |
| `get` returns no bytes (404, other status, redirect, 3 network errors, not a JPEG body) | **STOP and PI** (3(h)). No substitute image; K3 stays rejected |
| sha or byte mismatch (§7) | that file is never kept (or gets one `rm`), log, **STOP** (3(c)) |
| any other exception | STOP; report the class name, no traceback with paths beyond K |

After a STOP:
- The verified files stay in K (0600, laptop).
- No resume, rerun or deletion happens without a new read (and a PI line for 3(h)).
- A resume, if ruled, first re-hashes every file in K against the record (the cen_fetch `run_fetch` resume form) and
  fetches only the rest. **[open point O1]**

## 9. Logging (CC-280 3(f))

- Stdout:
  - progress counts every 500 images (fetched / 3,907, failed 0);
  - the final summary: count, bytes, manifest sha, start/end utc.
- No URL list and no caption are printed. Ids appear only in a STOP line, for the one failing id.
- Manifest `~/c_pvr_ktc_<MMDD>.sha256`: one `<sha256>  <name>` line per file (sha256sum format), sorted by name
  (`LC_ALL=C`). The coordinator re-checks it with `cd "$K" && sha256sum -c ../c_pvr_ktc_<MMDD>.sha256`.
- OPS line `OPS-<MMDD>c-ktc` (`date -u`; one O_APPEND write; the CC-280 6(a) side-file rule applies if LOG.md is
  unwritable). It carries:
  - count 3,907;
  - total bytes;
  - the manifest sha;
  - HEAD;
  - cen_fetch e51918e9, record 614afa1b, the kt_c TSV sha;
  - the fetch script sha;
  - the ACCESS_LOG row number and the log sha after the append;
  - start/end utc;
  - failed 0;
  - the R-H6 CC id and PI-1106k.

## 10. Code (needed; not written in this step)

- A short stdlib script, `scripts/c_pvr_ktc/c_pvr_ktc_fetch.py`, with its own SHA256SUMS (the AM9 logic: never in
  scripts/c_pvr_gpu/SHA256SUMS; it never goes to a host).
- What it does: §3-§9, in two subcommands, so that the coordinator's row (§6) sits between them:
  - `preflight --tsv F --tsv-sha H --out K`: no network, and nothing is written. It checks the §3 pins, the §4 list
    against the record, the absence of K and its ext4 parent, and it prints the 3,907 byte total;
  - `fetch` with the same arguments: it re-runs every preflight check, then creates K and makes the first GET.
- Coordinator order: `preflight` → ACCESS_LOG row → `fetch`.
- It imports `cen_fetch` from its sha-checked bytes and calls `read_rec`, `get`, `sha_bytes`, and the `url_ok` rule.
  No new fetch logic.
- `selftest`: a fake `OPEN` (cen_fetch's own test hook) and synthetic record/TSV fixtures. No network.
- Mutants, each to be killed:
  - mismatch kept;
  - bytes unchecked;
  - a name outside the TSV fetched;
  - the 5,000 used instead of the TSV;
  - redirect accepted;
  - absence guard off;
  - file mode 0644;
  - a write before the check;
  - a retry loop added.
- **[open point O2]** Where it is read: recommended together with this plan in R-H6 (one read). The alternative is
  the R-P5b bundle.

## 11. Retention (CC-280 3(g))

- K is kept until the **tier-1 final pull**. Then one logged deletion, driven by the manifest:

  ```bash
  cd "$K" && cut -c67- ../c_pvr_ktc_<MMDD>.sha256 | xargs -d '\n' rm -- && cd .. && rmdir -- "$K"
  ```

  - `rmdir` fails, and so flags, if anything unlisted is left.
  - It is never a recursive delete.
  - One LOG line records the utc, the path and the count.
- Tier 2 never uses KT-C.
- The same rule covers every other laptop copy of these pixels: the kt_c images-pass dir, if it copies rather than
  reads K **[open point O3]**.
- Host copies are wiped by host v3 §4 (logged tmpfs wipe).

## 12. Time and cost [est.]

- 3,907 × about 164 KB ≈ 0.64 GB.
- Sequential: about 10-30 min.
- 0 VND (laptop).

## 13. Open points for the reader

- O1: the resume rule after a STOP, or a crash that leaves a `.tmp_<name>` in K. Recommended: none without a new
  read; a ruled resume re-hashes K first and removes a stray `.tmp_<name>` with one logged `rm` (the run_fetch form).
- O2: read the fetch script in R-H6 (recommended) or in R-P5b.
- O3: the kt_c images pass reads K directly as `--images` (one copy of the pixels; recommended) or copies it into
  `~/c_pvr_build_<MMDD>/images/kt_c/` like the other sets (two copies, both under §11).
- O4: the record source path is under `.session_backup/machines/M1/` on /mnt/d. The script reads it once, sha-checked,
  and only at preflight. A /mnt/d EIO there is a STOP before any network call.
