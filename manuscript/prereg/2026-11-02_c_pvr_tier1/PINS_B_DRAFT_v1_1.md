# PINS-B DRAFT v1.1 (C-PVR-T1, Paper C, ACM TALLIP): the `gates.py` (B) pin for G-B, the one test-gold read

DRAFT, not registered. Written 2026-11-03T06:26:41Z (`date -u`) at HEAD 9cecf677994c97928fec371a5d44d0867b8af96e.
No commit, no LOG line, no G-B run, no parity run, no network request. No test gold was opened: no Open Images label
CSV was fetched or read, no XM3600 A12 label CSV was opened or hashed, and no NoCaps-test caption file or
`nocaps_val_4500_captions.json` was opened. The touches are listed in §10.

This text supersedes `PINS_B_DRAFT.md` f4bec5698f38da0c9458830622b0f45c0227eb047f312c96d8a562e6f125dccb (v1) for the
92 panel. It carries the rulings of **CC-239** (`.session_backup/2026-10-13/decisions/CC-239.txt`,
c080bee9050adbe4a97a484910b0869053a0da37a9abfc42b72a245c628fdd43; design GO 92, one judge, reversible 90; LOG
OPS-1103c-pinsB-code-start) and describes the (B) bytes that now exist.

Bases (unchanged from v1): prereg `PREREG_DRAFT_v1_2.md` 0a2f0773 (8282874); amendment `AMENDMENT_CC222_DRAFT_v1_3.md`
c565e67a (db97b93); erratum `ERRATUM_CC227_GA_SCHEMA.md` a116fa85 (5e4045c); `PINS_A_DRAFT_v1_4.md` 624b0804 (3fb6725).

Tier: **irreversible, full panel at 92** (prereg §9.1 step 5; PI-1102a Q-PINS YES, LOG l.1140; CC-239 decision). The
panel must refuse GO while any of CC-239 W1-W6 is open; §3.3 maps each to its code, selftest case and mutants.

---

## 0. What changed since v1

- **`gates.py` (B) now exists** as an uncommitted working copy:
  - `scripts/c_pvr/gates.py` **3bced05e7f718377b34837cfb3f6d6539fb8aafc28bc5f8818e5d7be4ccdf897** (2,279 lines);
  - diff from bf4d5f64: **insert-only** (`git diff --numstat HEAD -- scripts/c_pvr/gates.py` = 1091 added, 0 deleted; every hunk
    is an add; no line of bf4d5f64 is changed or removed). Diff sha256 3903bd617909c12b32c5c5291e46c8ad78045c2f16bda030c8893ce597185941, from
    `git diff --no-color HEAD -- scripts/c_pvr/gates.py | sha256sum`.
  - So `BARRED`, `refuse()`, `sha_file()`, `write_once()`, `access_log()`, all G-A code, all G-C2 code and
    `OI_TEST_URL` are byte-equal (Q-B0, Q-B8, Q-B13).
- **`gates_mutants.py` (B)** 34003b9368b306733b668b871124169c270d975c0b963ae992ba02ae6360d176: the 68 + 2 rows of f9c1ff3c are unchanged (targets and replacements
  byte-equal; each target still occurs once in (B)); 80 rows added for G1-G24, Q-B7 and the remaining-count check;
  every copy now runs in the W3 sandbox (§1.3).
- **Rulings Q-B0..Q-B13 are decided** by CC-239 (§8 records them; they are no longer questions).
- **G17-G24 added** (CC-239 Ruling 3, W1-W6 plus two NB rows).
- **Fixes of v1 text:** the map has `_note` **and** `_skipped` (W10 (b)); the §7 override table gains prereg §8.2 l.590
  and the Q-B7 §5.6 term (W7); the run commands carry no pipe and print `rc=$?` (W9).

## 1. Pinned object and closure

### 1.1 What exists at HEAD 9cecf67 (unchanged from v1 §1.1)
Base code `gates.py` bf4d5f64; harness f9c1ff3c; `SHA256SUMS` c87ebaf5 (16 lines); PINS of G-A (`xm_src` 1bd00f46,
`xm_attr` 288de413, `oiv7_val` 4b7a1813, `xm456` 54966ca7, `noc_val` 6add90eb, `gc1` 1f65b2ae, `prov` e242623f); G-A
outputs `ga_counts.json` f7036396, `ga_remaining_ids.txt` 3feccabc (10,496 ids, the G-B filter key),
`xm3600_all_ids.txt` 1bd00f46; G-C2 record 767998f8 (made under bf4d5f64).

### 1.2 What (B) adds to the closure (constants in the (B) bytes; G-B and parity FAULT on any mismatch)

| role | (B) constant | path | sha256 | re-hashed for v1.1 |
|---|---|---|---|---|
| mapped classes (69 keys + `_note` + `_skipped`) | `PINS_B["map"]` | `data/xm3600/vi_oiv7_map.json` | 27f2b1ca3f2bf47d43c8f00e8409472c8d571eb720d47b8107a1c77bd208d16a | yes, equal |
| class names to MIDs | `PINS_B["desc"]` | `data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv` | 84a4373a0efb7fd6d93fe19b0e7ceb6c1b855c233d13b9b78a9a33655c9fdce3 | yes, equal |
| full-file md5 record, val | `PINS_B["md5_val"]` | `data/datasets/xm3600/oiv7/full-val.md5` | 5770ed7c94cb6ae9ebd5e8746a95382d6475d0887c87ad4c05afa664ec840d8a | yes, equal |
| full-file md5 record, test | `PINS_B["md5_test"]` | `.../full-test.md5` | 2eebd937f99edec5267abd697f1b839d9846fc4ba4fd070d833b048bbc9ace54 | yes, equal |
| md5 record, train (provenance) | `PINS_B["md5_train"]` | `.../full-train.md5` | e1af682181bcbbdfea6c76fb083e90481aa834efa1138efde869c1cc21e40de0 | yes, equal |
| producer (sha only, not run) | `PINS_B["fetch"]` | `.../fetch.sh` | 75c22a0814037cee2bf328101aefdb3852a499c3e65fcdb1707e8fa2992f6c07 | yes, equal |
| parity target | `PINS_B["manifest"]` | `data/xm3600/manifest.json` | 263015f9dc46ebe2cea80055e04ed39baf80a356f4e027cd3756464279135bef | yes, equal |
| G-B filter key | `PINS_B["ga_rem"]` | `manuscript/prereg/2026-11-02_c_pvr_tier1/ga_remaining_ids.txt` | 3feccabc6da972396482faf0d2ae81296277e665ce094368019a3913c2fcbd24 | yes, equal |
| parity input (A's spent dev gold) | `A12["train"]` | `data/datasets/xm3600/oiv7/xm3600-train-annotations-human-imagelabels.csv` | 779afb19a4c3c25f100f871e92bbe8e937d6fa7f20ea75c4d0f7a23953056e76 | **no** (not opened; prereg §2.3 value) |
| parity input | `A12["val"]` | `.../xm3600-val-annotations-human-imagelabels.csv` | b7967190d6b05d6c97d38fe238046091905aabfe5bd268df4efe1c2a9a3db9d0 | **no** |
| parity input | `A12["test"]` | `.../xm3600-test-annotations-human-imagelabels.csv` | 06567dd986bf571db62d69af5abec0973a37f2552b1e00c50147cf490f72c19a | **no** |
| code closure (W8) | `CURL_STREAM[0]` | `/usr/bin/curl` (curl 8.5.0 at drafting) | hashed by `gate-b` at run time into `gb_counts.json` `inputs` | – |
| Q-B7 term | `FLICKR_W3` | the 4 ids of `G_C2_record.json` 767998f8 `flickr_image_exclusions` | checked against the record by the selftest's real section | – |
| tenancy inputs (read, not pinned) | `GB_LOG`, HOME `/.config/vsps/gpu_backup.sh`, `/proc` | `.session_backup/2026-10-13/decisions/LOG.md` | – | – |

- The three A12 shas are the prereg §2.3 values (pinned by reference in pin 1, LOG l.1347). They are first hashed by
  `parity` itself, through `allow_read`, before any row is parsed. A mismatch is a FAULT and parity does not run.
- `WANT_B` holds the manifest `coverage` targets (CC-239 Ruling 4 (c)-(d)): mapped_classes 69;
  mapped_classes_with_a_verified_label_on_xm3600 68; images_with_any_verified_label 2,584;
  images_with_a_verified_label_on_a_mapped_class 2,119; image_class_pairs present 4,453 / absent 8,276;
  verified_labels positive 19,052 / negative 10,700 / conflicting 0; rows_per_oi_split train 1,222 / val 6,623 / test
  21,907. `GB_REMAINING` = 10,496 (`ga_counts.json` `remaining`).

### 1.3 Command lines of (B) (quoted from the (B) docstring and CLI; W9: no pipe, `rc` printed at once)

```
S=<ext4 scratch dir, not under /mnt, no BARRED word in its path>; mkdir -p "$S/home" "$S/tmp"
env -i PATH=/usr/bin:/bin HOME="$S/home" TMPDIR="$S/tmp" unshare -rnm sh -c 'mount -t tmpfs tmpfs /dev/shm && exec "$@"' sh python3 -I -B scripts/c_pvr/gates.py selftest ; echo rc=$?
python3 -I scripts/c_pvr/gates_mutants.py scripts/c_pvr/gates.py "$S/mut" ; echo rc=$?        # sandboxes each copy itself
python3 -I -B scripts/c_pvr/gates.py gate-a verify ; echo rc=$?                                 # P7, rerun rule
python3 -I -B scripts/c_pvr/gates.py parity --gates-sha <(B) sha> ; echo rc=$?                  # P2, laptop CPU
python3 -I -B scripts/c_pvr/gates.py gate-b --gates-sha <(B) sha> --pause-tag <OPS tag> ; echo rc=$?   # once
```

- **W3 in code:** `selftest` FAULTs unless `/proc/self/net/dev` lists only `lo`, `~/.vsps_sealed/c_pvr` does not
  exist under the current HOME, and HOME is not under `/mnt`. So the selftest cannot run against the real sealed dir,
  and it cannot reach the network.
- `selftest` also replaces `subprocess.Popen` with a recorder that raises, so no process can start.
- The G-B fixtures pass their own sealed, tmpfs, lock, LOG, `gpu_backup` and `/proc` paths, and assert that they are not
  the real ones. The private tmpfs on `/dev/shm` means that even a mutant that wrote to `/dev/shm/c_pvr_gb` could not
  leave residue that blocks the real G-B (G19).
- `gate-a verify`, `parity` and `gate-b` run outside the sandbox: they need the real sealed dir (verify, gate-b) and the
  network (gate-b).
- If `tee` is used, log `${PIPESTATUS[0]}` (CC-229 W5 carried; W9).

## 2. Specification as built (prereg §3.1, §3.3, §5.6, §8.2, §9.3-§9.6, §11; amendment §2.3 N11, §6; erratum E6; CC-239)

### 2.1 Loader (`load_labels`, `resolve_map`, `status`, `statuses`, `coverage_b`): stdlib port of `xm3600_oiv7.py` 9a79403f
- `resolve_map` = l.60-75: `csv.reader` over 84a4373a, opened exactly as the reference (`encoding="utf-8"`); `_`-prefixed
  keys skipped; a name not present exactly once FAULTs (message names the class and map names, never a label row).
- `status` = l.78-81 (present if `pos & P`, else absent if `neg & N`, else unknown); `statuses` = l.84-93.
- `load_labels(ids, csv_paths, allowed)` = the `cmd_build` loop l.106-119:
  - `Confidence` parsed as `int(float(x))`;
  - pos = MIDs seen only with 1, neg = only with 0, mixed = neither and counted as conflicting;
  - rows counted per file.
- **W2 exception to "port exactly":** the reference `assert r["ImageID"] in vi, r` (l.112) prints the row. In (B), the
  header check (`ImageID,Source,LabelName,Confidence`), a foreign id, and any `csv.Error`, `ValueError`, `TypeError` or
  `KeyError` raise `GBAbort` with a fixed code only (`header`, `label_row`). The original exception is dropped
  (`from None`).
- `allow_read` is the **Q-B8 scoped allow**: the resolved path must be a key of the given map (the 3 A12 constants for
  parity; the 2 tmpfs files gate-b itself wrote), and the bytes read must hash to its value. The parse runs on those
  same bytes, so there is no gap between the check and the use.
- The selftest checks the AST: `allow_read` is called only by `load_labels`, and `load_labels` only by `parity` and
  `gate_b`. Every other subcommand still goes through `refuse()` / `sha_file()`, which still refuse the A12 paths and
  `/dev/shm/c_pvr_gb/` (G14).

### 2.2 `parity --gates-sha H` (prereg §3.3; CC-239 Q-B2, Q-B10, Ruling 4)
- Steps:
  - Refuses unless `--gates-sha` equals sha256 of the running file (Q-B5).
  - Verifies the map, class-description and manifest pins.
  - Reads the 3,600 XM3600 ids (`PINS["xm_src"]` 1bd00f46) and loads the 3 A12 files through `allow_read`.
  - Computes the manifest `coverage` and compares it with **both** `WANT_B` and the sha-pinned manifest. It also
    compares `pairs_per_class` in memory with the manifest (never printed). Any difference FAULTs, naming only the key.
- It does **not** check SHA256SUMS. A dry run on candidate bytes (Q-B10) precedes the SUMS update. The binding P2 run
  repeats under the committed sha.
- Prints exactly (Ruling 4 (a)-(e)), aggregates only, all already committed in 263015f9:
  ```
  parity ok  TIER 1 / DEV-EXPLORE (C-PVR-T1)  gates.py <H>
  re-hash ok: xm3600-train 779afb19 / xm3600-val b7967190 / xm3600-test 06567dd9; class descriptions 84a4373a; map 27f2b1ca; manifest 263015f9
  registered targets = constants = manifest: mapped_classes 69; images_with_a_verified_label_on_a_mapped_class 2119; present 4453 / absent 8276; mapped_classes_with_a_verified_label_on_xm3600 68
  reader checks = constants = manifest: images_with_any_verified_label 2584; verified_labels positive 19052 / negative 10700 / conflicting 0; rows_per_oi_split train 1222 / val 6623 / test 21907
  pairs_per_class 68/68 equal
  ```
  (the numbers are printed from the computed values; this shows the pass case).
- **W11:** the parity *record* file is **not** adopted, because a write-once record from the dry run would block the
  binding P2 run under the same sha. Instead, **`gate-b` re-runs `parity` in-process** before its start marker (§2.3
  step 4). This turns P2 into a code check without a file.

### 2.3 `gate-b --gates-sha H --pause-tag T`, one process (Q-B4 (a)), fail-closed in this order
Before the start marker (no gold requested yet), a failure is a FAULT with text (Q-B11 allows it):
1. **One-run rule** (`gb_refuse`). Refuses if:
   - `~/.vsps_sealed/c_pvr` resolves under `/mnt`, or is not a mode-0700 dir;
   - or any of these exists: `gb_counts.json` in the prereg folder, `gb_intermediate.json`, the start marker
     `~/.vsps_sealed/c_pvr/gb_start`, or `/dev/shm/c_pvr_gb`;
   - or `ACCESS_LOG.tsv` holds a `gate-b start` row (W1).
2. **Integrity** (`gb_integrity`, Q-B5):
   - `--gates-sha` = sha256(`__file__`);
   - SHA256SUMS has exactly one `scripts/c_pvr/gates.py` line, equal to `--gates-sha`;
   - every SUMS line verifies;
   - every `PINS_B` pin verifies.
3. **N11:** `gate_a_verify` must return the pinned `ga_rem` sha 3feccabc **before any label byte** (G1; the selftest
   proves the order with a spy).
4. **P2 in code:** `parity` (as §2.2). Then `resolve_map` (69 classes, also checked by parity).
5. `ga_remaining_ids.txt` = 10,496 unique ids.
6. The `full-{val,test}.md5` records parse as one `<md5>  -` line. Then sha256 of `/usr/bin/curl` (W8).
7. **Tenancy** (`tenancy`, §8.2 steps 1-4, W6):
   - `pause_ok`: the `--pause-tag` (form `OPS-...`) occurs as a whole token in **exactly one** LOG line; that line
     starts with a `date -u` stamp (`YYYY-MM-DDTHH:MM[:SS]Z`) earlier than the process start (`T0`, module import);
     and that line contains `G-B` and a word beginning `pause` (any case).
   - **LOG quiet rule (registered here):** every re-check after the marker re-reads `LOG.md`. A second line carrying the
     tag, or a read that meets a half-written UTF-8 append, would abort with rc 40 or 50 and consume the run. So **no
     agent writes the LOG between the pause line and gate-b's exit**. The G-B result line is written after the exit.
   - No `/proc/<pid>/cmdline` other than gates.py's own pid has an argument ending in `_job.sh`.
   - `gpu_backup.sh` exists and contains no `/dev/shm`.
8. **Lock:** open `/dev/shm/c_pvr_gb.lock` and take `flock(LOCK_EX | LOCK_NB)`; held = FAULT.
9. **Start marker (W1):** `~/.vsps_sealed/c_pvr/gb_start` (written by `write_new`, mode 0400, stat-checked), then an
   fsynced ACCESS_LOG row `gate-b start <H>`.
   - CC-239 W1 requires the marker before the first HEAD or stream byte. (B) writes it after the offline checks and
     the lock and before that byte, so a typo in `--gates-sha` or `--pause-tag`, or a missing pause line, FAULTs
     without consuming the one run.

From the marker on, **nothing is printed on any non-success exit** (Q-B11, W2):
- A `try` catches `BaseException` (including a `SystemExit` from any `fault()`).
- The `finally`:
  - sets SIGTERM/SIGINT/SIGHUP to ignored;
  - kills and waits for a live curl;
  - unlinks every tmpfs file, each with an fsynced `gate-b unlink` row and its sha (the sha of a partial file is taken
    from its bytes);
  - removes the dir;
  - writes an fsynced `gate-b abort <rc>` row;
  - restores the handlers and closes the lock.
- Then `os._exit(rc)`.

| class | rc | raised when |
|---|---|---|
| tenancy | 40 | a re-check fails (pause line, foreign `*_job.sh`, `gpu_backup`, lock inode replaced, tmpfs dir not a 0700 dir of this uid) |
| head | 41 | HEAD curl rc != 0; no or several `x-goog-hash` md5; no or several Content-Length; base64 not 16 bytes (composite object) |
| md5 | 42 | bucket md5 != record md5 (checked **before** the body request, Q-B12 in code); full-stream md5 != bucket or record |
| curl | 43 | body curl rc != 0 |
| header | 44 | first record of a stream (CR stripped) != `ImageID,Source,LabelName,Confidence`, or empty stream; or the filtered-file header at the read |
| val_row | 45 | the val stream kept a data row (Q-B6; G-A `in_oiv7_val` 0) |
| label_row | 46 | the single read meets a foreign id or a bad field |
| integrity | 47 | streamed bytes != Content-Length; an `allow_read` path or sha mismatch |
| write | 48 | `write_new` fails (exists, I/O, re-read sha, mode) |
| signal | 49 | SIGTERM, SIGINT or SIGHUP (W10 (e)) |
| internal | 50 | anything else, incl. a `SystemExit` from `fault()` and a `gb_counts.json` key-set violation |

10. mkdir `/dev/shm/c_pvr_gb` mode 0700 (chmod again against the umask).
11. For s in (val, test):
    - re-check tenancy (with the lock-inode and dir-mode checks);
    - HEAD `CURL_HEAD + (url,)` → `bucket_md5` (G24: `x-goog-hash` md5 as one header or comma-joined, base64 → hex;
      Content-Length);
    - bucket md5 must equal the record md5, or abort 42 with **no body request**;
    - body `CURL_STREAM + (url,)` → `gb_filter` (W5, one pass; below) writing `filtered-$s.csv` (O_EXCL, 0600);
    - curl rc 0; full-stream md5 = bucket = record; byte count = Content-Length;
    - re-check tenancy;
    - for val, kept data rows must be 0.
12. Re-check tenancy. Then **the single read**: `load_labels(remaining, [filtered-val, filtered-test], {resolved path:
    filtered sha})`, then `statuses`.
13. **Sealed writer (W4):** `write_new(gb_intermediate.json, mode 0400, check_mode)`, in this order: tmp → write → fsync
    → chmod → `os.link(tmp, final)` (fails if final exists) → fsync(dir) → unlink tmp → re-read sha and stat mode 0400.
    The bytes are `json.dumps({id: {"absent": [...], "present": [...]}}, sort_keys=True, separators=(",", ":"),
    ensure_ascii=True) + "\n"`, holding only ids with at least one known class. Then an fsynced `gate-b write` row.
14. The four numbers. `gb_counts_ok` (exact key set). Unlink both tmpfs files (rows) and the dir. Then
    `gb_counts.json` by `write_new` (0444 requested; `/mnt/d` drvfs ignores the mode, so no mode check there, but
    it has the link no-overwrite, fsync and re-read) **last**, as the commit marker.
15. The CLI prints `gb_counts.json` (indent 1, sorted), the same bytes that go to the repo.

**`gb_filter` (W5):**
- sha256 and md5 run over the raw bytes as received.
- Records split on `\n` across any read boundary.
- Record 1 is the header. A data record is kept iff its bytes before the first comma are in the remaining set (fetch.sh
  `awk -F, '$1'`).
- Each kept record is written with `\n` appended (awk ORS). So a last record without a newline gains one, and a CR
  stays inside the record (the csv reader then handles CRLF).
- The full stream is held only one 64 KiB read at a time.

### 2.4 Outputs
- `gb_counts.json`, exact key set (`GB_KEYS`):
  - `label`, `utc`, `gates_sha256`, `ga_remaining_sha256`;
  - `n_e_gb`, `present_pairs`, `absent_pairs`, `coverage_share` (= n_e_gb / remaining), `remaining`;
  - `streams.{val,test}.{sha256, md5, bucket_md5, record_md5, filtered_sha256, bytes}`;
  - `inputs` (the 8 `PINS_B` and 3 A12 shas, plus `/usr/bin/curl`);
  - `sealed_sha256`.
- **Changes vs v1 §2.3:** `bytes` added per stream (the public Content-Length, checked); `inputs` gains the A12 shas and
  the curl sha (W8). There is no per-class, per-image or kept-row count. Any other key, including `pairs_per_class`,
  `labels` and `rows_per_oi_split`, makes `gb_counts_ok` raise (internal, 50) before anything is written (G10).
- Sealed intermediate as in §2.3 step 13. The gatekeeper commits its sha as `GB_SEALED.sha256` (prereg §9.4).
- ACCESS_LOG rows from code: `gate-b start`, `gate-b write`, `gate-b unlink` ×2, or on abort `gate-b unlink` (0-2) and
  `gate-b abort <rc>`. Each is fsynced. ACCESS_LOG stays 0644 in a 0700 dir (CC-238 N3; not chmodded).

### 2.5 Disclosures (CC-239 W10)
- **(a) Parity cannot prove the conflict rule.**
  - XM3600 has conflicting = 0, and positive + negative = all 29,752 rows. So the real parity run never exercises the
    mixed branch or duplicate (image, MID) rows.
  - Prereg N3 (l.128) says parity covers "conflict rule cmd_build l.115-118". It does not. The rule rests on the G7
    fixtures (2 conflicts and a duplicate row in the hand-counted set) and the 4 G7 mutants alone.
  - NoCaps test may contain conflicts. If it does, G7 is the only evidence that they are handled.
- **(b)** The map has `_note` **and** `_skipped`. v1 §1.2 said "+ `_note`". Both are skipped, as in the reference.
- **(c) "Never touches disk" is procedural.** The full stream is held only one 64 KiB read at a time, and the filtered
  rows live in tmpfs. But tmpfs pages may go to WSL swap, so the rule rests on the procedure (as prereg §8.2 step 5),
  not on an OS boundary.
- **(d) SIGKILL residue.** A SIGKILL (or a power loss) skips the `finally`. It leaves the tmpfs dir, possibly a
  filtered file and the start marker. The next start refuses (G2, G17).
  - The coordinator removes **only the tmpfs residue**, by hand, with an ACCESS_LOG row `unlink (hand)` with its sha
    and a LOG line.
  - Removing the start marker is a re-download and needs its own ruling at 92 (prereg §9.6).
- **(e)** SIGHUP is handled with SIGTERM and SIGINT (`GB_SIGS`; G23).

### 2.6 Q-B7 (tier-2 term, registered before G-B)
- `n_e_power(n_e_gb, w25_flagged, lost)` = n_e_gb − w25_flagged − lost − 4, where 4 = `len(FLICKR_W3)`, the 4 ids of
  `G_C2_record.json` 767998f8. The selftest's real section checks them against that record (pinned by sha).
- `gate-b` never calls it and prints no fifth number. The tier-2 power code (§5.6) must use this formula. The exact
  0-4 drop is computed only at the single tier-3 open (report-only).

## 3. Test evidence (offline; laptop CPU; W3 sandbox; no gold)

### 3.1 Runs
- **Evidence copies** (session scratch is not kept). Byte copies are in `.session_backup/2026-11-03/c_pinsb/`
  (gitignored), re-hashed there:
  - `gates_B_3bced05e.py` 3bced05e (= `scripts/c_pvr/gates.py`);
  - `gates_mutants_B_34003b93.py` 34003b93 (= `scripts/c_pvr/gates_mutants.py`);
  - `selftest_B_out.txt` 6f614df1;
  - `mutants_B_out.txt` 9ea5f2f7;
  - `ngram_code_out.txt` 47cdff3d;
  - `aislop_B.json` 3602d9e0;
  - `ngram_doc_out.txt` (this file's scan; sha in the coordinator's LOG line).
- **Selftest of (B) from the repo:**
  - Run in the W3 sandbox (§1.3 line 2), rc 0, 16.2 s wall. Output:
    ```
    FAULT f: scan FAULT after 3 attempt(s): 55 B sha 9d373235, pinned 55 B 00000000; no record written -> its models UNCHECKABLE on nocaps_test; join continues
    real pins (sha only): xm_src=OK xm_attr=OK oiv7_val=OK xm456=OK noc_val=OK gc1=OK prov=OK
    registered provenance: schema ok; 24 undetermined image-bearing Pangea components -> pangeains decided by documentation, not scanned
    real (B) pins (sha only): map=OK desc=OK md5_val=OK md5_test=OK md5_train=OK fetch=OK manifest=OK ga_rem=OK flickr_w3=OK
    selftest ok  TIER 1 / DEV-EXPLORE (C-PVR-T1)  gates.py 3bced05e7f718377b34837cfb3f6d6539fb8aafc28bc5f8818e5d7be4ccdf897
    (the first line is the existing G-C2 join note on stderr, from the fixture file `f`; unchanged code)
    ```
  - Run outside the sandbox, rc 1, with `FAULT: selftest runs only in the W3 sandbox: unshare -rnm, private /dev/shm,
    HOME on ext4 scratch`.
- **Harness (B):**
  - `gates_mutants.py` (B) 34003b9368b306733b668b871124169c270d975c0b963ae992ba02ae6360d176, run on a byte copy of (B) in ext4 scratch
    `/tmp/claude-1000/-mnt-d-vsps-image-captioning/078aa393-7328-44fb-9c0d-f6e088395441/scratchpad/pinsb/`, rc 0,
    370 s (3 jobs) wall.
  - Result: **148 mutants run, 148 killed (0 by timeout), none survived**. Output file sha256 9ea5f2f7f0720d84082525a29d6c62922ec5bd08255cd6a9d6355bd3ec2c5cda.
  - The harness ran on the scratch copy, byte-equal to `gates_B_3bced05e.py`.
  - The 68 CC-227 rows: 68/68 killed (rows byte-equal to f9c1ff3c; no PATTERN). The 80 (B) rows: 80/80 killed. An earlier run of the same rows left `g21_no_last_record` alive, because the shuffled fixture rarely ended on a kept row; the G21 fixture now ends on a kept record, and the final run kills it. The 2 registered equivalents (`eq_val_term`,
    `eq_no_36707_assert`): SURVIVED, as required. They also serve as the baseline: an unmutated-equivalent copy reaches
    only the real-pin check, so no kill is an artefact of the sandbox or the copy path.
- **c_pvr.py `_st` AST check (G16):** the c_pvr.py l.1325-1328 snippet, run on (B): `OI_TEST_URL` equals
  `https://open-images-dataset.s3.amazonaws.com/test/{file}`, result `True`. The full `c_pvr.py selftest` under (B)
  needs its model/spacy stack and is left to the coordinator (§11).
- **aislop** (user rule): all findings are warnings with `fixable: false`. Against HEAD, two are new:
  - `hardcoded-url` on the selftest probe `https://example.invalid/x` (test-only, invalid by design);
  - `python-broad-except` on the `except BaseException: pass` around the abort-row write in `gate_b`'s `finally`
    (W2: after the marker nothing may print; the rc still carries the code).
  - `function-too-long` now also covers `gate_b` and the selftest helpers. `file-too-large` was already present at
    HEAD.
  - None was refactored, because a refactor would change the pinned bytes. The panel can rule otherwise.
- **NGRAM SCAN PASS** on `gates.py` (B) and `gates_mutants.py` (B) (8/6-gram vs KTVIC, OpenViIC, UIT-ViIC, COCO-Karpathy;
  positive controls hit), and on this file (§10).

### 3.2 What the selftest feeds G-B
A synthetic world in a temp dir:
- a 5-class map (+ `_note`, `_skipped`) over 8 class names (one name twice);
- A12 parity rows for 7 XM3600 fixture ids, hand-counted: 5 mapped / 4 with a label; 7 images with any label; 5 with a
  mapped label; 3 present / 5 absent; 4 positive / 5 negative / 2 conflicting; rows 7 / 3 / 4;
- the 10,501 fixture remaining ids;
- a val stream (header + 50 foreign rows) and a test stream (100 known images, 100 present / 20 absent, one mixed id,
  50 unknown, 200 foreign rows);
- HEAD replies built from the bodies;
- a LOG with a pause line and a longer look-alike tag;
- a `/proc` tree whose **own-pid** entry carries `c_pvr_job.sh` (every run proves the own-pid exclusion).

`curl` is a stand-in fed from these bytes (`_FakeCurl`). It records the argv, and a hook can fire during a read: a
signal, a foreign job appearing, a mode change, or a `SystemExit`.

### 3.3 Coverage table G1-G24 (each: selftest case, killed mutants; the panel checks row by row)

| # | behaviour | selftest case (function) | killed mutants (gates_mutants.py rows) |
|---|---|---|---|
| G1 | `gate_a_verify` before the first label byte (N11) | spy order `verify` < first HEAD; a changed G-A input FAULTs with no curl call (`_st_b_runs`) | g1_no_verify |
| G2 | one run: refuse on gb_counts / sealed file / tmpfs dir | each artifact alone in a fresh env → REFUSED, no curl call; second run after success → REFUSED | g2_no_counts_check, g2_no_sealed_check, g2_no_shm_check |
| G3 | `--gates-sha` = sha(`__file__`); SUMS gates.py line; SUMS and pins verify | wrong sha; SUMS gates line changed; other SUMS line changed; a PINS_B pin changed | g3_no_gates_sha, g3_sums_line_any, g3_no_sums_verify, g3_no_pins_b |
| G4 | md5 bucket = record (before body) and = stream; sha256 over all bytes; Content-Length | head≠record (no body request); flipped body byte; length +1; success compares stream sha/md5 with the fixture bytes | g4_no_head_cmp, g4_no_stream_cmp, g4_sha_unfed, g4_md5_unfed, g4_no_length |
| G5 | keep header + `$1` ∈ remaining only; full stream never written | `gb_filter` vs reference; success filtered sha = reference | g5_keep_all, g5_key_third |
| G6 | val keeps 0 data rows | val stream with one remaining id (record re-pinned) → 45 | g6_no_val_assert |
| G7 | conflict rule; present before absent | hand-counted parity fixture (2 conflicts; an image with pos Dog and neg Cat); `status` cases | g7_mixed_pos, g7_mixed_neg, g7_absent_first, g7_no_conflict_count |
| G8 | 69 classes; a name not exactly once FAULTs; `_` keys skipped | map naming `Twin` (twice) and `Nope` (absent) → FAULT; `_note`/`_skipped` present in every run | g8_no_once_check, g8_no_skip_note |
| G9 | parity exact vs constants AND manifest; pairs_per_class | parity = hand counts; constant +1; manifest absent +1; manifest per-class +1; gate-b with conflicting −1 FAULTs before the marker | g9_no_manifest_cmp, g9_no_const_cmp, g9_no_ppc_cmp, g9_no_parity_in_gb |
| G10 | only the §2.4 keys | success key set; `pairs_per_class`, `labels`, `rows_per_oi_split`, `kept_rows`, a stream key, a non-sha input → raise | g10_ppc_emitted, g10_no_key_check |
| G11 | sealed bytes deterministic, write-once, 0400, ext4 | two runs byte-equal and equal to the expected literal; stat 0400; second write refused, original kept | g11_indent, g11_mode_444, g11_link_replace |
| G12 | tenancy → no start, or abort; nothing printed | pre-marker: no pause line, `/dev/shm` in gpu_backup, lock held, foreign job → FAULT, no marker; mid-run: foreign job → 40; tmpfs chmod 0755 → 40 | g12_no_pause, g12_no_foreign, g12_no_backup, g12_lock_ignored, g12_no_shm_mode, g12_no_initial |
| G13 | tmpfs unlinked on success, FAULT, signal; unlink rows; curl killed | rows on success (shas = filtered shas) and in every abort case; curl stand-in killed on signal | g13_no_cleanup, g13_no_unlink_row, g13_no_kill, g13_no_abort_row |
| G14 | other subcommands refuse A12 / `/dev/shm/c_pvr_gb/`; allow exact + sha | `allow_read` refuses a non-allowed path and a sha mismatch; `sha_file` refuses the 3 A12 paths and a tmpfs path; AST caller check | g14_allow_any, g14_no_allow_sha |
| G15 | pinned argv (https only, `-q` first, no `-o`/`-k`/proxy); spawn args | literal compare of both tuples; forbidden-flag set; `curl_run` spawn recorded with stdin/stderr DEVNULL and env {PATH}; each run's argv = constant + URL | g15_output_file, g15_no_proto, g15_head_insecure, g15_no_q_first, g15_stderr_open, g15_env_inherit |
| G16 | `OI_TEST_URL` byte-equal | AST read of the own file (as c_pvr.py l.1325) | g16_test_url |
| G17 | persistent start marker; refusal survives an abort | marker file alone → REFUSED; `gate-b start` row alone → REFUSED; every abort leaves marker 0400 + start row; a second run after an abort → REFUSED, no curl call | g17_no_marker_check, g17_no_row_check, g17_no_marker, g17_no_start_row |
| G18 | no field value in any message after the first byte | 13 abort cases with fds 1/2 captured: empty; a `SystemExit` with text mid-stream → 50, silent; loader: foreign id, bad Confidence, short row, bad header → code only (`str(e) == code`) | g18_print_error, g18_catch_exception_only, g18_reraise_field, g18_no_header_check, g18_no_foreign_id |
| G19 | no network, no real sealed/tmpfs/lock path | selftest FAULTs outside the sandbox; fixture paths ≠ real; `subprocess.Popen` stubbed; exactly one recorded spawn (the probe) | g19_real_shm, g19_no_spawn_stub |
| G20 | fsync + post-write verify (sealed, gb_counts, ACCESS_LOG) | `os.fsync` recorder: marker tmp, sealed tmp, sealed dir, gb_counts tmp, out dir, ACCESS_LOG; chmod suppressed → write; torn link → write | g20_no_file_fsync, g20_no_dir_fsync, g20_no_log_fsync, g20_no_reread, g20_no_mode_stat |
| G21 | chunk-boundary correctness | LF, LF without the final newline, CRLF, CRLF without it × chunks 1, 7, 64 KiB, whole = reference filter; byte-equal output and hashes | g21_no_last_record, g21_no_carry, g21_crlf_header |
| G22 | tenancy line exact; own pid excluded | 0 / 2 lines; longer tag; `pre-` prefix; no stamp; stamp = t0; minute stamp passes; no `G-B`; no pause; bad tag form; own pid with `_job.sh` → 0 | g22_own_pid, g22_tag_prefix, g22_one_or_more, g22_no_stamp_time, g22_no_gb_name, g22_seconds_only |
| G23 | SIGHUP with SIGTERM/SIGINT | each of the three signals mid-stream → 49, tmpfs gone, curl killed, handlers restored; `GB_SIGS` set checked | g23_no_hup |
| G24 | x-goog-hash base64 → hex | the OIL vector `2DL+t3Wzy3gHe/iuNQrc5Q==` → d832feb7…; joined and split headers equal; composite, no length, short digest, two md5 → head | g24_no_base64, g24_composite_ok |
| Q-B7 | n_e_power − 4 | `n_e_power(100, 3, 1) == 92`; real section: `FLICKR_W3` = G_C2_record 767998f8 exclusions | qb7_no_flickr_term |
| – | remaining = 10,496 unique | remaining_n + 1 → FAULT before the marker | gb_no_remaining_n |

**Not tested offline (checked at run time and logged):** the real bucket md5 and Content-Length, the real header, the
real parity numbers, and the real curl network path.

**Equivalences not registered as mutants (disclosed):**
- The four tenancy re-checks are partly redundant against the fixtures: before the test stream ⊇ after the val
  stream; before the read ⊇ after the test stream. So a mutant that drops one of them alone is caught by the next one.
- In the second md5 compare, each half alone is equivalent, because the earlier bucket = record check already forces
  equality.
- Setting the signals to SIG_IGN during cleanup has no offline test.

## 4. Preconditions of prereg §9.3, with status

| # | precondition | status | evidence / step still needed |
|---|---|---|---|
| P1 | prereg committed | **MET** | 8282874 (LOG l.1136) |
| P2 | parity passed (§3.3) | **OPEN** | code exists (§2.2); dry run on 3bced05e allowed by CC-239 Q-B10 (coordinator step, own LOG line, not run here); binding run after the commit; also re-run inside gate-b |
| P3 | PINS-A committed | **MET** | 3fb6725 + 9419103 + 9cecf67 (CC-238 Ruling 5) |
| P4 | PINS-B committed | **OPEN** | this text + (B) bytes → HEAD pre-check (Q-B12) → 92 panel → gatekeeper commit |
| P5 | Q11 = YES | **HALF** | PI-1102a given; ledger ruling ≥ 92 open, separate, after PINS-B |
| P6 | `gates.py` sha = PINS-B | **OPEN** | enforced in code: `--gates-sha` + the single SUMS gates.py line (Q-B5) |
| P7 | rerun rule | **OPEN** | `gates.py gate-a verify` under (B) must print 3feccabc (coordinator, after the commit); also in-code N11 |
| P8 | §8.2 tenancy window | **OPEN (at run)** | pause LOG line matching the §2.3 step 7 predicate; Q-PI-2 window |

## 5. Carry items (unchanged from v1 §5 unless stated)
- CC-237 N3: the curl argv in PINS_A_DRAFT_v1_1 §5 step 1 and v1_4 §5 is superseded by 9419103.
- CC-238 (c)-at-W25: OPEN until §8 W25; gates the A8 OpenViVQA proxy only, not G-B.
- CC-238 N3 (custody): ACCESS_LOG 0644 in a 0700 dir, accepted; (B) does not chmod it. `gb_intermediate.json` is 0400.
- CC-229 W2 (internal only, never in the paper): unchanged; G-B changes neither sentence.
- CC-229 W3 → **Q-B7 ruled YES** (§2.6; §7 row).
- CC-229 W5 → W9 form (§1.3): no pipe, `echo rc=$?` at once; `${PIPESTATUS[0]}` if tee is used.
- CC-232 C8, (f): nothing irreversible proceeds on a default; the spend chain is PINS-A → PINS-B (92) → Q11 ledger
  (≥ 92) → G-B → laptop W25 → tier 1.
- v1.4 §16 (6)-(8): PINS-B, then Q11, then G-B once.

## 6. G-C2 and the rerun rule under (B)
- `G_C2_record.json` 767998f8 stands. No `gate-c2` command runs under (B). The `gate-c2` code is byte-equal
  (insert-only diff).
- `gate-a verify` under (B) must reproduce 3feccabc (P7), and `gate-b` calls it in code (N11).
- Erratum E6: (B) is the PINS-B change.

## 7. Overrides stated (not silent)

| registered text | registered | PINS-B reading | ruling |
|---|---|---|---|
| prereg §11 l.753 | `c_pvr.py gate-b --stream --pause-tag` | `gates.py gate-b --gates-sha H --pause-tag T` | Q-B1 |
| **prereg §8.2 l.590 (W7, added)** | "the G-B window (`c_pvr.py gate-b`, ...)" | `gates.py gate-b`; the window, tmpfs and lock paths are unchanged | Q-B1 |
| prereg §11 l.752; amendment §1 l.110 | `c_pvr.py parity --xm3600-csv-dir ...`; "`c_pvr.py` keeps ... parity" | `gates.py parity --gates-sha H` (the A12 paths are constants) | Q-B2 |
| prereg §9.6 | `curl \| tee >(sha256sum) >(md5sum) \| awk` | the same three legs in one Python pass (`gb_filter`) under the PINS-B sha; HEAD in code first | Q-B4, Q-B12 |
| `gates.py` docstring l.3-4; amendment §1 reason 3 | "no network code ... local files and stdin only" | `gate-b` starts `/usr/bin/curl` with `CURL_HEAD`/`CURL_STREAM`; closure = (B) + curl binary (W8). l.3-4 stay byte-equal; an added docstring paragraph states the override | Q-B4 |
| `gates.py` BARRED l.73 | refuses `annotations\|labels\|captions\|/dev/shm/c_pvr_gb` | unchanged; a separate exact-path `allow_read` for the 3 A12 constants (parity) and the 2 tmpfs files gate-b wrote | Q-B8 |
| **prereg §5.6 (W7, added)** | n_e_power = n_e(G-B) − W25-flagged count (+ lost) | n_e_power = n_e(G-B) − W25-flagged − lost − **4** (`FLICKR_W3`); fixed before G-B | Q-B7 |
| `cmd_build` l.112 "port exactly" | `assert r["ImageID"] in vi, r` | `GBAbort("label_row")`, code only (no row in any message) | Q-B3 / W2 |

## 8. Rulings recorded (CC-239; no longer questions)

| # | ruling | conf. |
|---|---|---|
| Q-B0 | YES: (B) = bf4d5f64 + G-B + loader + parity, insert-only | 95 |
| Q-B1 | `gates.py gate-b` (overrides §11 l.753, §8.2 l.590) | 93 |
| Q-B2 | `gates.py parity` (overrides amendment l.110, §11 l.752) | 92 |
| Q-B3 | stdlib port proved by parity; W2 exception only | 95 |
| Q-B4 | (a) one process, curl subprocess, argv `[/usr/bin/curl, -q, -sS, --fail, -L, --proto, =https, --proto-redir, =https, --max-redirs, 3, -A, vsps-research, URL]`, stderr DEVNULL, env {PATH} | 91 |
| Q-B5 | `--gates-sha` = sha256(`__file__`) and = the SUMS gates.py line | 95 |
| Q-B6 | keep the val stream; 0 kept data rows | 92 |
| Q-B7 | subtract all 4 Flickr ids from n_e_power at tier 2; no fifth G-B number | 91 |
| Q-B8 | scoped exact-path allow; additive diff | 92 |
| Q-B9 | every G-row ≥ 1 killed mutant; old 68 still killed; harness and selftest under W3 | 95 |
| Q-B10 | dry parity on the candidate bytes allowed and recommended before the panel (own LOG line); binding P2 after the commit; order commit → P2 → P7 → Q11 → G-B | 91 |
| Q-B11 | rc only from the first byte on; pinned code table (§2.3); `gate-b abort <rc>` row | 92 |
| Q-B12 | headers-only pre-check before the panel (coordinator, LOG line) and in code before each stream | 93 |
| Q-B13 | the 70 harness targets stay unique (checked: each occurs once in (B)) | 94 |

### 8.1 For the PI
- FYI (decided by CC-239): writing (B) (Q-PI-1); the Q11 ledger as its own 92 panel after PINS-B (Q-PI-3).
- **Q-PI-2** (default applies): one laptop window for G-B.
  - Pauses: B, MT4 and VSPS-J laptop jobs, by a LOG line matching §2.3 step 7. No GPU job is affected.
  - Length: about 30-60 min [est.]; the Q-B12 Content-Length replaces the estimate (W12).
  - Recommended: YES, in the first idle laptop window after the Q11 ledger GO. Default: the same.

## 9. The pin LOG line the gatekeeper would write (template; filled where known; `<>` = still open)

**Working tree until that edit:** `sha256sum -c scripts/c_pvr/SHA256SUMS` fails on exactly two lines, `gates.py` and
`gates_mutants.py`. This is by design (no SUMS edit before the panel), not tampering. `gate-b` refuses to start in this
state (Q-B5), so G-B cannot run before the commit.

SUMS after the gatekeeper's edit:
- `SHA256SUMS` keeps its 16 lines. Two are replaced:
  ```
  3bced05e7f718377b34837cfb3f6d6539fb8aafc28bc5f8818e5d7be4ccdf897  scripts/c_pvr/gates.py
  34003b9368b306733b668b871124169c270d975c0b963ae992ba02ae6360d176  scripts/c_pvr/gates_mutants.py
  ```
- The resulting file would have sha256 0999c7753dd1066a541933f6ad145b859e390b4a9b83b7a96eac168ca20cd43c. This was computed in memory; the working `SHA256SUMS` is
  unchanged.
- Every other line verifies as at pin 2.

```
<date -u>Z OPS-<MMDD>c-pinsB: PINS-B (gates.py G-B, loader, parity) committed <commit sha> and pushed q2 paper-v10:main, per CC-<nnn> GO <median> (full panel J1 <> J2 <> J3 <>, round <r>/3, irreversible 92; Codex no new BLOCKING; CC-239 W1-W6 closed row by row), after PINS-A pin 1 3fb6725 (l.1347) + A11 amendment 9419103 (l.1353) + pin 2 9cecf67 (l.1362). Committed files, sha256 re-hashed from HEAD: scripts/c_pvr/gates.py 3bced05e7f718377b34837cfb3f6d6539fb8aafc28bc5f8818e5d7be4ccdf897 (bf4d5f64 -> (B), insert-only diff 1091 added, 0 deleted, diff 3903bd617909c12b32c5c5291e46c8ad78045c2f16bda030c8893ce597185941; G-A, G-C2, BARRED, refuse, sha_file byte-equal); scripts/c_pvr/gates_mutants.py 34003b9368b306733b668b871124169c270d975c0b963ae992ba02ae6360d176 (148 mutants: 148 killed incl. G1-G24, Q-B7 rows; equivalents eq_val_term, eq_no_36707_assert (CC-227 proofs)); scripts/c_pvr/SHA256SUMS 0999c7753dd1066a541933f6ad145b859e390b4a9b83b7a96eac168ca20cd43c (16 OK from repo root); manuscript/prereg/2026-11-02_c_pvr_tier1/PINS_B_DRAFT_v1_1.md <sha256>. Selftest from HEAD in the W3 sandbox: 'selftest ok  TIER 1 / DEV-EXPLORE (C-PVR-T1)  gates.py 3bced05e7f718377b34837cfb3f6d6539fb8aafc28bc5f8818e5d7be4ccdf897' rc <rc>. Dry parity (Q-B10) on 3bced05e: <LOG line> rc <rc>. HEAD pre-check (Q-B12): val md5 <> = full-val.md5, Content-Length <>; test md5 <> = full-test.md5, Content-Length <> (<LOG line>). c_pvr.py 8f10bd60 selftest re-run under (B) ok (A11 OI_TEST_URL AST equality). curl: `curl --version` <>, /usr/bin/curl sha256 <> (W8). Closure pins: vi_oiv7_map 27f2b1ca, class-descriptions 84a4373a, full-val.md5 5770ed7c, full-test.md5 2eebd937, full-train.md5 e1af6821, fetch.sh 75c22a08, A12 779afb19/b7967190/06567dd9, manifest 263015f9, ga_remaining 3feccabc. G-C2 record 767998f8 stands (made under bf4d5f64; no gate-c2 runs under (B)). NGRAM SCAN PASS <scan output sha256>. The curl argv quoted in PINS_A_DRAFT_v1_1.md §5 step 1 and PINS_A_DRAFT_v1_4.md §5 is superseded by 9419103 (CC-237 N3). Check (c) OPEN until §8 W25, gates the A8 OpenViVQA proxy only, not G-B (CC-238). Preconditions left for G-B: parity P2 under the committed sha, gate-a verify P7, Q11 ledger ruling >= 92 (P5), tenancy window (P8). Next: gates.py parity, gate-a verify, then the Q11 ledger panel.
```

## 10. Touches during drafting (`date -u` 2026-11-03, about 05:50-06:26Z)
- **Read:**
  - CC-239 in full; `PINS_B_DRAFT.md` v1;
  - prereg v1.2 §3.3, §5.6, §8.2, §9, §11, N3 row l.128; amendment v1.3 §1, §2.3, §5.6, §6; erratum §0, E6;
  - `gates.py` bf4d5f64 and `gates_mutants.py` f9c1ff3c in full; `xm3600_oiv7.py` l.1-180 (code);
  - `c_pvr.py` l.800-825 and l.1318-1332; `fetch.sh`; `SHA256SUMS`.
- **Read, aggregates and ids only:**
  - `data/xm3600/manifest.json` coverage (committed aggregates; the `pairs_per_class` entry was counted, not printed);
  - `vi_oiv7_map.json` key shape;
  - `G_C2_record.json` `flickr_image_exclusions` (4 ids);
  - `full-val.md5` (format only);
  - the LOG tail (3 lines) and the format of its pause lines.
- **Hashed:** the 8 non-gold `PINS_B` files (all equal), `G_C2_record.json`, CC-239, v1. The A12 label CSVs were **not**
  opened or hashed.
- **Ran:**
  - the (B) selftest in the W3 sandbox (fixtures; real section: sha of the 7 PINS + 8 PINS_B files, the G_C2 record ids,
    the provenance schema);
  - the harness in ext4 scratch;
  - the n-gram scan;
  - two probes in a scratch dir under `.git/` on `/mnt/d` (`os.link` no-overwrite and dir fsync on drvfs; removed at
    once);
  - an `unshare -rnm` capability probe;
  - one call of the (B) `write_new` on a scratch dir under `/mnt/d/.../.git/`: the drvfs sequence chmod 0444 → link
    → dir fsync → unlink tmp works, an overwrite is refused (`write`), and no tmp is left (dir removed);
  - `aislop scan` on copies of the HEAD and (B) files in ext4 scratch.
- **No network request. No label CSV, caption file, NoCaps-test info value or sealed file was opened.**
- Nothing was committed. The working `SHA256SUMS` is unchanged.
- Files changed or added: `scripts/c_pvr/gates.py` (modified in place, insert-only), `scripts/c_pvr/gates_mutants.py`
  (modified), this file, and the evidence copies in `.session_backup/2026-11-03/c_pinsb/` (gitignored).

## 11. Left for the coordinator (in order; CC-239 NEXT STEPS)
1. **HEAD pre-check (Q-B12, W12):**
   - Run `curl -q -sS -I --fail --proto =https <URL>` for val and test. No body.
   - Log a LOG line with the `x-goog-hash` md5 decoded to hex (as `bucket_md5`), Content-Length and utc. It must equal
     `full-{val,test}.md5`; a mismatch or a missing md5 goes to a ruling before the panel.
   - Also check: exactly one Content-Length, and **no `Content-Encoding`**. (B) checks streamed bytes = Content-Length
     only after the full stream, i.e. after the marker. A gzip-encoded object would abort G-B (header, rc 44) and
     consume the run.
   - Content-Length goes into Q-PI-2.
2. **Dry parity (Q-B10)** on 3bced05e7f718377b34837cfb3f6d6539fb8aafc28bc5f8818e5d7be4ccdf897: `python3 -I -B scripts/c_pvr/gates.py parity --gates-sha 3bced05e7f718377b34837cfb3f6d6539fb8aafc28bc5f8818e5d7be4ccdf897 ;
   echo rc=$?`, laptop CPU, outside the sandbox (it reads the repo files only), plus its own LOG line. Not run by the
   drafter: CC-239 places it as its own logged step, and the drafter writes no LOG line.
3. Re-run the selftest and harness from the repo (§1.3) and the full `c_pvr.py selftest` under (B) (G16).
   - **LOG quiet rule:** from the pause line to gate-b's exit, no agent writes the LOG (§2.3 step 7).
4. The PINS-B full panel at 92 (J1/J2/J3 + Codex read-only; W1-W6 row by row against §3.3).
5. The gatekeeper commit (gates.py, gates_mutants.py, the SUMS lines of §9, this file) and the pin LOG line (§9 + W8).
6. P2 under the committed sha, then P7 `gate-a verify`, then the Q11 ledger panel at 92, then G-B once.
