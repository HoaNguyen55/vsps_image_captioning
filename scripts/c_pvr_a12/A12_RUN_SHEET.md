# Paper C — A12 absent-label extraction: coordinator run sheet (R-H1)

Basis: CC-277 Ruling 1 + AD1 (H1); CC-280 Ruling 1 (a)-(g), AM9, WORK LIST step 5; LOG OPS-1106c-a12-source.
Plan: PRE_S11_PLAN_v1.md §2.5 (CC-280 wins on conflict).

- Who runs it: the **coordinator only**, on the laptop. No agent runs it, and no agent reads or lists sealed custody.
- When: after the R-H1 GO and the gatekeeper commit of `scripts/c_pvr_a12/`. It may run in parallel with H6 and E-G.
- It never goes to a host. Its SUMS file is `scripts/c_pvr_a12/SHA256SUMS`, never `scripts/c_pvr_gpu/SHA256SUMS`
  (AM9).
- The script writes nothing to /mnt/d and never writes ACCESS_LOG. The label file is never copied.

## 1. Preconditions (stop at the first failure)

```bash
cd /mnt/d/vsps_image_captioning
git rev-parse HEAD                                   # = the R-H1 GO commit
sha256sum -c scripts/c_pvr_a12/SHA256SUMS            # all OK; c_pvr_a12.py = the R-H1 read sha
env -i PATH=/usr/bin:/bin nice -n 19 ~/.venvs/c_pvr/bin/python -I -B scripts/c_pvr_a12/c_pvr_a12.py selftest
                                                     # prints 'selftest ok', rc 0 (synthetic fixtures only)
O="$HOME/c_pvr_a12_$(date -u +%m%d)"
[ ! -e "$O" ] && echo absent-ok                     # absence guard (CC-278 A6 form); the script re-checks it
```

- The venv must be `~/.venvs/c_pvr`, because the pinned `xm3600_oiv7.py` imports numpy at module level. The script
  itself is stdlib only.
- No other heavy /mnt/d writer may be running (EIO lesson).

## 2. ACCESS_LOG hand row: FIRST, before anything reads the label file (CC-277 1(c), CC-280 1(c))

The coordinator appends one row to the ACCESS_LOG.tsv that holds hand row 52 (OPS-1106c-w2-dtc). It has 5
tab-separated fields: utc, tool, action, path, sha. There is no tab inside a field and no token `w25`
(CC-245 Ruling 7).

```bash
A=<the ACCESS_LOG.tsv of hand row 52>               # set by the coordinator; never listed by an agent
U=$(date -u +%Y-%m-%dT%H:%M:%SZ)
printf '%s\t%s\t%s\t%s\t%s\n' "$U" coordinator \
  'hand row: A12 absent-label extraction (CC-277 H1, CC-280 R1)' \
  /mnt/d/vsps_image_captioning/data/xm3600/oiv7_labels.json \
  bac3953a511a9793c22e928a29b68ae05dbf9654502abcbe7b64fd9f6d74c8b2 >> "$A"
wc -l < "$A"; sha256sum "$A"                         # row number + log sha after the append -> OPS line
```

After the row, and only after it, run the tracked-input check (git may read the label file to compare it):

```bash
git diff --quiet HEAD -- data/xm3600 scripts/xm3600_oiv7.py scripts/c_pvr_a12 \
  manuscript/prereg/2026-11-02_c_pvr_tier1/xm3600_all_ids.txt \
  manuscript/prereg/2026-11-02_c_pvr_tier1/ga_remaining_ids.txt; echo rc=$?     # rc=0
```

## 3. The command (exactly this; one run)

```bash
env -i PATH=/usr/bin:/bin nice -n 19 ~/.venvs/c_pvr/bin/python -I -B \
  scripts/c_pvr_a12/c_pvr_a12.py run --out "$O"; echo rc=$?
stat -c '%a %n' "$O" "$O/a12_absent.json"; ls -A "$O"; sha256sum "$O/a12_absent.json"
```

- The script first checks six input shas against its pins, before any parse:
  - `xm3600_oiv7.py` 9a79403f;
  - `vi_oiv7_map.json` 27f2b1ca;
  - `oidv7-class-descriptions.csv` 84a4373a;
  - `oiv7_labels.json` bac3953a;
  - `xm3600_all_ids.txt` 1bd00f46;
  - `ga_remaining_ids.txt` 3feccabc.
- It then calls the pinned `resolve_map` + `statuses`. It prints one json line with counts, shas and the output path,
  and no ids.

## 4. PASS rule (every item; anything else = FAULT)

- rc 0, and the printed line shows:
  - `label_keys` 2584, `with_status` 2119, `present` 4453, `absent` 8276. These are the four registered numbers
    (LOG l.1381; CC-280 1(d)). The script FAULTs on any difference;
  - `label_keys_outside_qids` 0 and `label_keys_x_ga_remaining` 0 (CC-277 AD1 form: label keys ∩ ga_remaining_ids);
  - `absent_total` 8276;
  - `queries_with_absent` ≤ 2119;
  - `classes_used` ≤ 69;
  - `mapped_classes` 69 (LOG l.1381; a coordinator check, the script only reports it).
- `stat` shows `700` for `$O` and `600` for `$O/a12_absent.json`.
- `ls -A "$O"` shows `a12_absent.json` only.
- `sha256sum` equals the printed `out_sha256`.

**FAULT / STOP:** report only the FAULT line and the counts. No script edit, no rerun and no other input without a
new read. The ACCESS_LOG row stays. If `$O` exists after a FAULT (possible only after a crash during the write), it
is inspected, not deleted, until the read rules.

## 5. OPS line (written with `date -u`; one O_APPEND write to LOG.md)

```
<utc> OPS-<MMDD>c-a12: CC-277 H1 / CC-280 Ruling 1 A12 extraction. A12 source is a tracked repo file:
data/xm3600/oiv7_labels.json bac3953a (commit e564ed6, blob 101a6ae2), not sealed custody (CC-280 R1(b),
OPS-1106c-a12-source); label file not copied. HEAD <sha>; c_pvr_a12.py <sha> (scripts/c_pvr_a12/SHA256SUMS <sha>);
pins xm3600_oiv7.py 9a79403f, map 27f2b1ca, desc 84a4373a, xm3600_all_ids 1bd00f46, ga_remaining 3feccabc.
ACCESS_LOG hand row <n> at <utc> (tool coordinator), log sha after append <sha>. rc 0: label_keys 2,584 /
with_status 2,119 / present 4,453 / absent 8,276 (= LOG l.1381); outside qids 0; label keys ∩ ga_remaining 0;
queries_with_absent <n>; absent_total 8,276; classes_used <n> of 69. Output ~/c_pvr_a12_<MMDD>/a12_absent.json
(0600, dir 0700, ext4) <bytes> B sha256 <full> = the a12 pin; the builder's manifest inputs.a12 must equal it
(CC-277 N3). Deletion after the xm3600_vi seal (CC-277 1(f)).
```

## 6. Deletion (after the xm3600_vi manifest is sealed, CC-277 1(f))

```bash
rm -- "$O/a12_absent.json" && rmdir -- "$O"          # one file, then the empty dir; never a recursive delete
```

- One LOG line records it: utc, path, and the sha it had.
- The source stays in git.
