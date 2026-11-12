# C-ATTR-DEV block 3: build note (host commands for the coordinator's LOG lines)

Label: `DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY`. Written by the block-3 coder, 2026-11-12 (UTC from `date -u`). Not committed. No decode and no score of anything. No test set touched. The host is named only by its ssh alias role (`hc2` = the live host of tonight, role H1 of block 1/1b); no host name, IP or port is written here.

Host rules followed for every command: `ssh -o BatchMode=yes hc2`, output piped through `grep -v -E '([0-9]{1,3}\.){3}[0-9]{1,3}'`; CPU only (`CUDA_VISIBLE_DEVICES=` empty), `nice -n 19 ionice -c3`; a NEW tree `/root/c_b3_tree/` (code only, `git archive` of HEAD plus the changed files; no data); logs under `/root/outputs_c_b3_checks/`. Not touched: the GPU, tmux `a_e3_7b`, `/root/a_e3`, `/dev/shm/a_e3`, `/root/outputs`, `/root/vsps` (its `.venv` and `/root/venv-lb` interpreters are only executed, never written), `/root/c_attr_score`, `/root/ncs-data`, `/root/a_e3code_tree`, `/root/b_fecert_tree`.

Laptop-side deviations, disclosed (none tested anything; no result is used as a check of the package):
- Three read-only `python3 -I -c` calls on the laptop: one printed the top-level and per-set keys of the committed `scripts/c_attr/c_attr_lists.json` (ids only, no caption) to confirm the `donor` lists for OV-dev-B and XM-dev500; two printed the model keys, hub ids, revisions, null-hash counts and the `venv` entry of the committed `manuscript/prereg/2026-10-30_c_t1/c_t1_registry.json`.
- One `sed -i` on `scripts/c_attr/c_attr.py` whose pattern (with a literal `\n`) matched nothing; it rewrote the file with unchanged content (later edits were made with the editor; the final bytes are those of `SHA256SUMS`).
- One LOG grep printed line 825 (CC-176) to 400 characters instead of 300; the OPS lines 818 and 831 were read through `cut -c1-1500` as allowed.
- An empty `python3 - <<EOF` no-op call ran once (no code).

## Commands (UTC, in order)

| UTC | where | command | result |
|---|---|---|---|
| 2026-11-12T12:00:01Z | hc2 | `test -e /root/c_b3_tree; test -e /root/outputs_c_b3_checks; ls -d /root/vsps/.venv/bin/python /root/venv-lb/bin/python /root/venv-t1/bin/python; nproc; free -g` | both paths free; `.venv` and `venv-lb` present; **no `/root/venv-t1`** on hc2; 32 CPU, 62 GB RAM |
| 2026-11-12T12:00:10Z | laptop → hc2 | `mkdir -p /root/c_b3_tree /root/outputs_c_b3_checks`; `scp` of the code-only archive `git archive --format=tar.gz HEAD scripts manuscript/prereg rescap configs data/coco_probe/chair_synonyms.txt` (HEAD `d10874e9a84e1072c6eeb4b2e6c51f760b8b6555`; `scripts/c_attr/` byte-equal to eb4286a / 42276d5; archive sha256 `0e5a812df6a4dda536bf4afc9c356ac126ab51868fd735510f25564c5d9949c6`) | copy ended 12:08:11Z |
| 2026-11-12T12:08:11Z | hc2 | `cd /root/c_b3_tree && sha256sum tree.tgz && nice -n 19 ionice -c3 tar -xzf tree.tgz && rm -f tree.tgz && (cd scripts/c_attr && sha256sum -c SHA256SUMS)` | archive sha equal; 8/8 OK (committed code, unchanged) |
| 2026-11-12T12:13:36Z | hc2 | control, committed code: `CUDA_VISIBLE_DEVICES= HF_HUB_OFFLINE=1`; `for f in c_attr c_attr_lists c_attr_score; do nice -n 19 ionice -c3 /root/vsps/.venv/bin/python -I -B scripts/c_attr/$f.py --selftest; done > /root/outputs_c_b3_checks/control_selftest.log 2>&1`; then the same `c_attr.py --selftest` with `/root/venv-lb/bin/python` appended | ended 12:13:47Z; rc 0; 4 "selftest ok" lines. Backed up by the coordinator read-only to `.session_backup/machines/ATTR_H1_misc/outputs_c_b3_checks/control_selftest.log`, sha256 `6bec52e44370c5ca3e677c75820effa7e794d91e5104e8a2e590c4d3dcaca80b` (planted self-test data only) |

No further host command was run. The session paused on the usage limit after 12:14Z; the coordinator's two messages (inventory request with a 15:45Z deadline; host deleted 15:47Z) were read at 15:49:54Z, after the deletion. Therefore:

- **The reference inventory of hc2 (model snapshot dirs, dataset folders with counts, venv freeze sha256, segmenter path) was NOT recorded.** The run document's §3 lists what a fresh host needs from committed pins and LOG lines of record instead.
- **OWED on the next host, before any block-3 decode (STOP gates b3.g1, b3.g2, b3.g4 of the run document):** the self-tests of the changed code (four "selftest ok" lines, plus `c_attr.py --selftest` under venv-t1) and the mutant run (control passes, then `83/83 killed; survived: none`: the 73 of record plus B1–B10), and the first dry run of the `block3` job mode. No record of the changed code exists from any host.

## Laptop-side steps (only `py_compile`, `bash -n`, `git diff`, `sha256sum`)

| UTC | command | result |
|---|---|---|
| 2026-11-12T15:50Z–16:30Z (not stamped one by one) | `python3 -m py_compile scripts/c_attr/c_attr.py scripts/c_attr/c_attr_mutants.py; bash -n scripts/c_attr/c_attr_job.sh` | OK (the untracked `scripts/c_attr/__pycache__/c_attr.cpython-*.pyc` that py_compile wrote was removed) |
| 2026-11-12T15:50Z–16:30Z (not stamped one by one) | `sha256sum $(awk '{print $2}' SHA256SUMS) > SHA256SUMS` in `scripts/c_attr/` (same 8 files, same order) | new `SHA256SUMS` below |
| 2026-11-12T15:50Z–16:30Z (not stamped one by one) | `git diff HEAD -- scripts/c_attr > scripts/c_attr/C_ATTR_B3.diff` | 4 files, +240 / −24 |

`grep -c -F` was used to count each single-line mutant pattern (each 1, except the "decoded once" line, whose mutant B6 carries the following `# no weights` line and is unique that way).
