# C-PVR-T1 dev-set W25 run document v1.5 ADDENDUM r2: the D-EN decide supplement (Paper C, plan S7'; DRAFT)

**Status (r2):** draft for the one-judge diff read r1 → r2, REVERSIBLE 85, per CC-267 (NEXT_ROUND 78; B1-B4).
It supersedes `W25_DEV_RUN_DOC_v1_5_ADDENDUM.md` 1bb4555e (unchanged). Written 2026-11-05 about 19:50-20:10Z
(`date -u`). Table §A lists the changes.

**Status (r1, history):** draft addendum for its one-judge read, REVERSIBLE 85 (PI-1103ae), per CC-261 (S7 panel, NEXT_ROUND 88)
K2-K7 and PI-1105n. It **amends** `W25_DEV_RUN_DOC_v1_4.md` 4d5f707c (registered at 186af09) for one run of the new
subcommand `dev-w25-den`; every rule of v1.4 not changed here stays in force (window rules §4, freeze plan §6, exit
table §7). It licenses nothing until its GO and its registration commit. Nothing in it has run. Written
2026-11-05 about 19:25-19:35Z (`date -u`; r1 said 2026-11-06 in error, CC-267 N1); code committed at 817adb3 (CC-265 GO 90).
- **Label:** TIER 1 / DEV-EXPLORE (C-PVR-T1). Dev data only: no test look, no gold, 0 GPU-h, 0 VND.
- **Sources read:** CC-261 in full; LOG l.1570, l.1595, l.1605-1608, l.1616 (PI-1105n), l.1630 (OPS-1106c-den-code);
  `c_pvr_run.py` 3d3eeed0 (working tree, code text only): `tag_used` l.722, `window` l.1175, `DEN_ROWS` l.1260,
  `dev_inputs` l.1313, `DEN_OUTS`/`DEV_V1`/`DEN_WALL` l.1415-1420, `dev_den` l.1438-1465, the `dev-w25-den` branch of `main` l.2657-2659 (CC-267 N4);
  `~/w25devpre_1105/pre.txt` (P15 block of the v1.4 window); `~/w25dev_env_2.sh` (RUN, DOC, D0, S lines).

## A. Changes from r1 1bb4555e (CC-267; each cites its source)

| # | item | r1 text | source | fix in r2 |
|---|---|---|---|---|
| R1 | P6 PI line count | `grep -c 'PI-1105n:'` = 2 today (the CC-265 line also holds it) | CC-267 B1 | `grep -cE '^[0-9T:-]+Z PI-1105n:'`; tested = 1; expected 1 |
| R2 | P3 vs bytecode | no B0, so P3 fails on the git-ignored `scripts/__pycache__` | CC-267 B2 | inline B0 to `bytecode_removed_den.txt`, its LOG line `OPS-<MMDD>c-w25den-bytecode`, then P3 again before close |
| R3 | v1 evidence | P9/P14/P15/B0 "verbatim" from v1.4 would append to `pre.txt` 831604ef, truncate `p14.txt` 616901e1 and `bytecode_removed.txt` | CC-267 B3 | every block inlined with `_den` paths (`pre_den.txt`, `p2_den.txt`, `p14_den.txt`, `bytecode_removed_den.txt`, new probe paths); §7 re-hashes `pre.txt` and `p14.txt` |
| R4 | P10 | dropped | CC-267 B4; CC-265 W1 | P10 added: FT realpath sha, pip freeze sha, pip check, SSCD sha = v1's |
| R5 | run order | implicit | CC-267 run order | §3 head states it |
| R6 | non-blocking | status date; P11b by reference; no P21/RESUME; `main` cite | CC-267 N1-N4 | UTC date fixed; P11b and the ckey line inlined; stale-python pattern in P11; `RESUME_den.txt`; cite l.2657-2659. N5 (W3/W4) carried; N6 noted (ADDCC = the GO'd round) |
| R7 | version pointers | `DOC=` and the pause line name the r1 file | follows R1-R6 | `DOC=` (env `_3` sed) and the pause line name `W25_DEV_RUN_DOC_v1_5_ADDENDUM_r2` |

## 1. The defect and the fix (a)
- **Defect (CC-261 R3).** The v1.4 run (`dev-w25` at 84b0d587, rc 0, LOG l.1606) loaded `feats_memory.npz` caf4a621
  with `W.load`, whose ids come back as int64 Python ints (`w25.py` l.125 `.tolist()`), while the D-EN ids from
  `cen_memory_allowed.tsv` are strings. `rows(…, missing_ok=True)` found no match, so all 80,083 D-EN ids left as
  "no feature row" (`d_en_no_feature_row` 80,083 against N88's 2; d_en out 80,083, kept 0). No D-EN near-duplicate
  decision was computed or seen (every D-EN `flagged_by_set` entry is 0). **D-EN is VOID; D-VI, D-TC and the three
  t2pool blocks are valid** (CC-261 R1).
- **Fix (CC-261 K3, code read CC-265; PI-1105n second freeze exception).** In `c_pvr_run.py` `3d3eeed09c7ebb13e00f84ddf347754c1d8cb78464f8acccfc4f4eb7d721ec1d`:
  - (i) the `feats_memory` ids are str-normalised **at load** in `dev_inputs`, not inside `rows()`;
  - (ii) a pre-window FAULT unless D-EN matched / missing = `DEN_ROWS` = (80,081, {388662, 397819}), pinned by value;
  - (iii) the selftest fixture goes through `np.savez` with int64 ids and `W.load`;
  - (iv) 9 new killed mutants (240/240 killed, the same 5 EQUIV survive; LOG l.1630);
  - (v) RULE, LOST_CAP, `build_lists`, LISTS_SHA, STAGE, K_TRUNC and the d_vi/d_tc/t2pool code are unchanged
    (`dev_decide` = `dev_sets` + the same writes).
- **The supplement (CC-261 O1 + N2, K4).** The new subcommand `dev-w25-den`:
  - refuses if either D-EN output or a `dev-w25-den start` row exists (one run);
  - sha-checks the v1 outputs `dev_w25_out_ids.json` ffdcb6ba and `dev_w25_counts.json` b91b1336 before and after,
    and never writes them;
  - reads the dev parts under the v1 run sha 84b0d587 (from `dev_w25_counts.json`) and the W25 parts under 290a75dc;
    opens no image;
  - recomputes every block in memory and FAULTs (nothing written) unless all of them equal the v1 files outside D-EN
    (N2);
  - writes `dev_w25_den_out_ids.json` and `dev_w25_den_counts.json` (0o444) with D-EN only;
  - has its own stop, `DEN_WALL` = 4 h from its start, **checked once, after the in-memory compute** (l.1452; not a
    running wall; v1 decide took about 50 s; CC-265 W2); the v1 `dev_w25/deadline` file (about 2026-11-06T13:40Z) is
    never read, so it cannot stop this run (CC-261 K4).
  - **This is D-EN's first evaluation, a repair and not a second look** (CC-261 R3). v1.4's "decide is one look, no
    rerun" (§7, §8) is departed from for D-EN only, by this addendum and PI-1105n.

## 2. Code, commit and the env file (c)
- **Code:** `c_pvr_run.py` `3d3eeed09c7ebb13e00f84ddf347754c1d8cb78464f8acccfc4f4eb7d721ec1d` at commit `817adb3` (gatekeeper, after CC-265 GO 90; PI-1105n). Mutants
  f6fa0a54, SHA256SUMS 5dbc1425 (18 OK); `git diff --stat 6472b78 817adb3 -- scripts/c_pvr` = 3 files, +157/−16
  (checked on disk while drafting).
- **Carried hardening, not done (freeze; CC-265 W3, W4):** `tag_used` (l.722) does not list `dev-w25-den start`, so a
  tag reused from such a row is not caught by it (harmless here: the start row itself blocks a second supplement; the
  tag below is fresh anyway); `st.get("deadline") or deadline(env)` would fall back to the dev-w25 file only for a
  deadline of 0, which `time.time` cannot give. Both wait for a later code change.
- **Freeze:** `817adb3` is the **second** exception (PI-1105n; the first was 6472b78, PI-1105j). The v1.4 §1
  freeze resumes at `817adb3` and holds until the S7' result commit.
- **Env file `$HOME/w25dev_env_3.sh`** = `w25dev_env_2.sh` with `RUN=` and `DOC=` changed, plus one appended line
  `SD=` (the new launch dir; v1.4's `$S` = `~/w25devrun_1105` exists and holds the v1 evidence). Same `D0`, so the
  same `$PRE`, `$STG`, `$IN`. Every block below sources `_3`.
```sh
[ -e "$HOME/w25dev_env_2.sh" ] && [ ! -e "$HOME/w25dev_env_3.sh" ] || { echo "GUARD: env files"; exit 1; }
{ sed -e 's/^RUN=.*/RUN=3d3eeed09c7ebb13e00f84ddf347754c1d8cb78464f8acccfc4f4eb7d721ec1d/' -e 's#^DOC=.*#DOC=manuscript/prereg/2026-11-02_c_pvr_tier1/W25_DEV_RUN_DOC_v1_5_ADDENDUM_r2.md#' "$HOME/w25dev_env_2.sh"; echo 'SD=$HOME/w25devden_$D0'; } > "$HOME/w25dev_env_3.sh"; chmod 400 "$HOME/w25dev_env_3.sh"
diff "$HOME/w25dev_env_2.sh" "$HOME/w25dev_env_3.sh"; sha256sum "$HOME/w25dev_env_3.sh"     # RUN= and DOC= differ; SD= added
```

## 3. Run order and checklist (any FAIL = no pause line; every block writes ONLY to `_den` files; stderr kept)
**Run order (CC-267):** `_3` (§2) → B0 → P1, P2, P3, P5, P6 → P10 → P11, P11b, P12, P15, P17 → P3 again → P9 (within
5 min of the pause line) → close `pre_den.txt` → one shell call (P14, pause line, launch; §4) → §7 checks → result and
resume lines → S7' panel.
**v1 evidence is never written (CC-267 B3).** `$PRE` is v1's dir (same `D0`). No block here opens `pre.txt` 831604ef,
`p14.txt` 616901e1 or `bytecode_removed.txt` for writing; §7 re-hashes the first two. The new files are
`pre_den.txt`, `p2_den.txt`, `p14_den.txt`, `bytecode_removed_den.txt`, `RESUME_den.txt`.

**B0 (CC-267 B2; before P1).** v1.4 §3.5 B0 with the same 8 `$DIRS` and the same check-ignore rule, list to a NEW file.
```sh
. "$HOME/w25dev_env_3.sh"; cd "$R"
[ ! -e "$PRE/bytecode_removed_den.txt" ] || { echo "GUARD: bytecode_removed_den.txt exists"; exit 1; }
for d in $DIRS; do ls -l "$d"/__pycache__ "$d"/*.pyc 2>/dev/null; done > "$PRE/bytecode_removed_den.txt"
for d in $DIRS; do
  if [ -d "$d/__pycache__" ]; then git check-ignore -q "$d/__pycache__" && rm -r "$d/__pycache__" || echo "NOT IGNORED: $d/__pycache__"; fi
  for f in "$d"/*.pyc; do [ -e "$f" ] && { git check-ignore -q "$f" && rm "$f" || echo "NOT IGNORED: $f"; }; done
done
sha256sum "$PRE/bytecode_removed_den.txt"; wc -l < "$PRE/bytecode_removed_den.txt"
```
Any `NOT IGNORED` line is a stop. Then one LOG line `OPS-<MMDD>c-w25den-bytecode` (dirs, file count, list sha). Today
the list holds `scripts/__pycache__` (git-ignored; another laptop job's `.pyc`), which made P3 fail (CC-267).

**P1, P2, P3, P5, P6.**
```sh
. "$HOME/w25dev_env_3.sh"; cd "$R"
{ echo "== P1 $(date -u +%FT%TZ)"; for p in c_pvr.py gates.py c_pvr_run.py; do echo "$(sha256sum < scripts/c_pvr/$p | cut -c1-64) disk $p"; echo "$(git show HEAD:scripts/c_pvr/$p | sha256sum | cut -c1-64) HEAD $p"; done; } >> "$PRE/pre_den.txt" 2>&1
{ echo "== P2 $(date -u +%FT%TZ)"; timeout 120 sha256sum -c scripts/c_pvr/SHA256SUMS > "$PRE/p2_den.txt" 2>&1; echo "rc=$? OK=$(grep -c ': OK$' "$PRE/p2_den.txt")"; } >> "$PRE/pre_den.txt" 2>&1
{ echo "== P3 $(date -u +%FT%TZ)"; git status --porcelain --ignored scripts/c_pvr "$DOC"; for d in $DIRS; do find "$d" -maxdepth 1 \( -name __pycache__ -o -name '*.pyc' \); done; echo "(end P3)"; } >> "$PRE/pre_den.txt" 2>&1
{ echo "== P5 $(date -u +%FT%TZ)"; git diff --stat 6472b78 817adb3 -- scripts/c_pvr | tail -n 1; git diff --quiet 817adb3 HEAD -- scripts/c_pvr && echo "817adb3..HEAD scripts/c_pvr: none"; } >> "$PRE/pre_den.txt" 2>&1
ADDCC='<CC id of the addendum GO>'; case "$ADDCC" in ''|*'<'*) echo "fill ADDCC"; exit 1;; esac
{ echo "== P6 $(date -u +%FT%TZ)"; git cat-file -t 817adb3; echo "doc HEAD $(git show HEAD:"$DOC" | sha256sum | cut -c1-64)"; echo "doc disk $(sha256sum < "$DOC" | cut -c1-64)"; for c in CC-265 "$ADDCC"; do echo "$c GO lines: $(awk -F' \\| ' -v id="$c" '$2==id && $4 ~ /^GO([ :(]|$)/ && $4 !~ /NEXT_ROUND|ESCALATE/ && $5 ~ /^(median )?[0-9]+%$/ {v=$5; gsub(/[^0-9]/,"",v); if (v+0>=85) print}' "$L" | wc -l)"; done; echo "PI-1105n $(grep -cE '^[0-9T:-]+Z PI-1105n:' "$L")"; } >> "$PRE/pre_den.txt" 2>&1
```
B1 test (CC-267): `grep -cE '^[0-9T:-]+Z PI-1105n:'` on LOG.md gave **1** (2026-11-05T19:51Z); the unanchored form gave 2,
because the CC-265 line l.1631 also contains the token.

**P10 (CC-267 B4): the interpreter and libraries equal v1's** (an N2 FAULT from library drift would spend the one run).
```sh
. "$HOME/w25dev_env_3.sh"; cd "$R"
{ echo "== P10 $(date -u +%FT%TZ)"; echo "FT $(readlink -f "$FT") $(sha256sum < "$(readlink -f "$FT")" | cut -c1-16)"; "$FT" -m pip freeze | sha256sum | cut -c1-16; "$FT" -m pip check; sha256sum < "$SSCD" | cut -c1-16; systemctl list-timers 'apt-daily*' --all --no-pager; systemctl is-active apt-daily.service apt-daily-upgrade.service; } >> "$PRE/pre_den.txt" 2>&1
```
PASS = the v1 P10 lines in `~/w25devpre_1105/pre.txt` (13:27:59Z): `FT /usr/bin/python3.12 e50d468e8b0adfb0`;
`1a639a50adf550c5`; `No broken requirements found.`; `9f26bd4c848cc19b`; no apt timer due within 1 h; both
`inactive`. Any difference = no pause line.

**P11, P11b, P12, P15, P17.**
```sh
. "$HOME/w25dev_env_3.sh"; cd "$R"
{ echo "== P11 $(date -u +%FT%TZ)"; ps -eo pid,etime,args | grep -E 'rsync|c_pvr_run_mutants|pdflatex|xelatex|pandoc|git gc|_job\.sh|gpu_backup|curl|multiprocessing\.(spawn|resource_tracker)|c_pvr_run\.py|c_pvr\.py' | grep -v grep | cut -c1-120; echo "(end P11)"; } >> "$PRE/pre_den.txt" 2>&1
{ echo "== P11b $(date -u +%FT%TZ)"; grep -nE 'OPS-[0-9]{4}[a-z0-9]*-?(rent|rented|rental|deleted|lost)\b' "$L" | cut -c1-110 | tail -n 12; echo "(end P11b)"; } >> "$PRE/pre_den.txt" 2>&1
# echo "ckey.vn live instances: <n> ($(date -u +%FT%TZ))" >> "$PRE/pre_den.txt"      # read from the provider panel; must be 0
{ echo "== P12 $(date -u +%FT%TZ)"; ls -d /dev/shm/c_pvr_w25 2>&1; [ -e /dev/shm/c_pvr_w25.lock ] && { flock -n /dev/shm/c_pvr_w25.lock true; echo "lock free rc=$?"; } || echo "lock absent"; ls manuscript/prereg/2026-11-02_c_pvr_tier1/dev_w25_den_out_ids.json manuscript/prereg/2026-11-02_c_pvr_tier1/dev_w25_den_counts.json 2>&1; echo "dev-w25-den rows $(cut -f3 "$HOME/.vsps_sealed/c_pvr/ACCESS_LOG.tsv" | grep -c '^dev-w25-den ')"; echo "v1 $(sha256sum manuscript/prereg/2026-11-02_c_pvr_tier1/dev_w25_out_ids.json manuscript/prereg/2026-11-02_c_pvr_tier1/dev_w25_counts.json | cut -c1-8 | tr '\n' ' ')"; [ ! -e "$SD" ] && echo "SD absent"; } >> "$PRE/pre_den.txt" 2>&1
NP=/dev/shm/c_pvr_nsprobe_den_$D0; PD=.session_backup/w25den_nsprobe_$D0
{ echo "== P15 $(date -u +%FT%TZ)"; [ ! -e "$NP" ] && [ ! -e "$NP.lock" ] && [ ! -e "$PD" ] || echo "P15 GUARD: probe path exists"
unshare -rn sleep 120 & NSPID=$!; sleep 1
echo "environ readable from outside: $(tr '\0' '\n' < /proc/$NSPID/environ | grep -c '^PATH=')"
unshare -rn "$FT" -I -B -c '
import fcntl, hashlib, os, sys
from pathlib import Path
np, log, pd, real = sys.argv[1], sys.argv[2], sys.argv[3], "/dev/shm/c_pvr_w25.lock"
print("uid inside", os.getuid())
nets = [x.split(":")[0].strip() for x in Path("/proc/self/net/dev").read_text().splitlines()[2:]]
print("interfaces lo only:", nets == ["lo"])
if os.path.exists(real):
    fd2 = os.open(real, os.O_RDWR)
    fcntl.flock(fd2, fcntl.LOCK_EX | fcntl.LOCK_NB)
    fcntl.flock(fd2, fcntl.LOCK_UN)
    os.close(fd2)
    print("real W25 lock: flock OK")
else:
    print("real W25 lock absent: dev-w25-den creates it inside the namespace")
fd = os.open(np + ".lock", os.O_RDWR | os.O_CREAT | os.O_EXCL, 0o600)
fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
os.mkdir(np, 0o700)
s = os.lstat(np)
print("tmpfs dir mode", oct(s.st_mode & 0o777), "uid match", s.st_uid == os.getuid())
open(log, "rb").read().decode("utf-8")
print("LOG strict UTF-8 read OK")
os.rmdir(np); os.close(fd); os.unlink(np + ".lock")
assert hashlib.sha256(open("scripts/c_pvr/gates.py", "rb").read()).hexdigest().startswith("3bced05e")
sys.path.insert(0, "scripts/c_pvr")
import gates as G
d = Path(pd); d.mkdir(); p = d / "p.json"
h = G.write_new(p, b"x\n", 0o444); ok = p.read_bytes() == b"x\n"; p.unlink()
left = sorted(x.name for x in d.iterdir()); d.rmdir()
print("netns write_new", h[:16], "left", left, "PASS" if ok and not left else "FAIL")
' "$NP" "$R/$L" "$PD"
kill -TERM $NSPID; wait $NSPID; echo "TERM to a namespaced pid: rc=$?"; } >> "$PRE/pre_den.txt" 2>&1
{ echo "== P17 $(date -u +%FT%TZ)"; "$HOME/.config/vsps/usage_check.sh"; } >> "$PRE/pre_den.txt" 2>&1
```
**P3 again, P9, RESUME note, close (P9 within 5 min of the pause line).**
```sh
. "$HOME/w25dev_env_3.sh"; cd "$R"
{ echo "== P3b $(date -u +%FT%TZ)"; git status --porcelain --ignored scripts/c_pvr "$DOC"; for d in $DIRS; do find "$d" -maxdepth 1 \( -name __pycache__ -o -name '*.pyc' \); done; echo "(end P3b)"; } >> "$PRE/pre_den.txt" 2>&1
{ echo "== P9 $(date -u +%FT%TZ)"; mount | grep ' /mnt/d ' | cut -c1-60; echo "d_watch live: $(ps -eo pid,args | awk '($2 ~ /bash$/ && $3 ~ /d_watch\.sh$/) || $2 ~ /d_watch\.sh$/' | wc -l)"; [ -e "$HOME/.local/state/vsps/d_watch.log" ] && awk '/ FAIL$| RECOVERED$/{l=$0} END{print "last event:", l}' "$HOME/.local/state/vsps/d_watch.log" || echo "d_watch.log absent"; PB=.session_backup/w25den_probe_$D0; [ ! -e "$PB" ] && mkdir "$PB" && timeout 20 /usr/bin/python3 -I -B -c 'import hashlib, sys; from pathlib import Path; assert hashlib.sha256(open("scripts/c_pvr/gates.py", "rb").read()).hexdigest().startswith("3bced05e"); sys.path.insert(0, "scripts/c_pvr"); import gates as G; d = Path(sys.argv[1]); p = d / "p.json"; h = G.write_new(p, b"x\n", 0o444); assert p.read_bytes() == b"x\n"; p.unlink(); left = sorted(x.name for x in d.iterdir()); d.rmdir(); print("write_new", h[:16], "left", left, "PROBE PASS")' "$PB" || echo "P9c FAIL (or the probe dir existed)"; echo "P9d OK=$(timeout 120 sha256sum -c scripts/c_pvr/SHA256SUMS 2>&1 | grep -c ': OK$')"; } >> "$PRE/pre_den.txt" 2>&1
printf '%s\n' "Paper C dev W25 D-EN supplement RESUME note (W25_DEV_RUN_DOC_v1_5_ADDENDUM_r2), $(date -u +%FT%TZ): window OPENING; SD=$SD; next LOG lines after the exit: OPS-<MMDD>c-w25den-result, then OPS-<MMDD>c-w25den-resume; after a WSL restart: no gpu_backup loop, no LOG writer until the resume line; restart d_watch only; the run is not retried (§6)." > "$PRE/RESUME_den.txt"
sha256sum "$PRE/RESUME_den.txt" "$PRE/pre_den.txt"                  # pre_den.txt is closed here
```

| # | PASS |
|---|---|
| B0 | no `NOT IGNORED` line; list sha and count recorded; LOG line written |
| P1 | 8f10bd60…, 3bced05e…, 3d3eeed09c7ebb13e00f84ddf347754c1d8cb78464f8acccfc4f4eb7d721ec1d, each disk = HEAD |
| P2 | `rc=0 OK=18` |
| P3, P3b | only `(end P3)` / `(end P3b)` |
| P5 | `3 files changed, 157 insertions(+), 16 deletions(-)`; `817adb3..HEAD scripts/c_pvr: none` |
| P6 | `commit`; doc HEAD = doc disk = the GO'd sha; `CC-265 GO lines: 1`; `<ADDCC> GO lines: 1` (ADDCC = the GO'd round's CC id); `PI-1105n 1` |
| P10 | equal to v1, as listed above |
| P11 | only `(end P11)` (no stale c_pvr python either: CC-267 N3's P21 is folded in here) |
| P11b | every rental token listed has a later deleted/lost token, and the recorded `ckey.vn live instances: 0` |
| P12 | the dir absent; `lock free rc=0` or `lock absent`; both D-EN outputs absent; `dev-w25-den rows 0`; `v1 ffdcb6ba b91b1336`; `SD absent` |
| P15 | `environ readable from outside: 1`; `uid inside 0`; `interfaces lo only: True`; `real W25 lock: flock OK` (or absent); `tmpfs dir mode 0o700 uid match True`; `LOG strict UTF-8 read OK`; `netns write_new 73cb3858a687a849 left [] PASS`; `rc=143`. Else `NS=''`, reason recorded |
| P17 | data age ≤ 120 s; 7-day ≥ 10% remaining; five_hour None passes on the PI-1105n line (as PQ-D7) |
| P9 | 9p; `d_watch live: ≥ 1`, no FAIL as last event; `write_new 73cb3858a687a849 left [] PROBE PASS`; `P9d OK=18` |
| P14 | inside §4, on the final string: `p14_den.txt` all True |

## 4. Pause line, run, result and resume (c); one shell call
**Same run conditions as v1 (CC-265 W1, binding).** N2 is a strict equality on RULE §3 decisions, so the supplement
uses exactly the v1 `dev-w25` conditions (pause line LOG l.1605): `--owners-sha $OWN`, `--feats-sha $F`, `--sscd
$SSCD`, `--in $IN`, `--stage $STG` from `w25dev_env_3.sh` (identical to `_2`, whose values ran v1); `--run-sha
3d3eeed09c7ebb13e00f84ddf347754c1d8cb78464f8acccfc4f4eb7d721ec1d`; `OMP_NUM_THREADS=1 MKL_NUM_THREADS=1`; `NS='unshare -rn'` as in v1; and a **new** pause tag. A BLAS-order
flip near a threshold would FAULT the N2 check (fail-closed) and spend the one run, so no setting differs from v1.
Same window rules as v1.4 §4 (G-B quiet rule; no LOG writer, judge, workflow or other laptop job; no rented machine
live; d_watch live). Tag `OPS-<MMDD>c-w25denpause` (fresh; only the generic form appears outside its LOG line). The
P14 test is v1.4 §3.6's, unchanged.
```sh
. "$HOME/w25dev_env_3.sh"; cd "$R"
NS='unshare -rn'                                   # or NS='' if P15 failed (state the reason)
TAG="OPS-$(date -u +%m%d)c-w25denpause"
PL="$(date -u +%FT%TZ) $TAG: C dev W25 D-EN supplement pause window opens per <CC id of this addendum's GO>, CC-261 and PI-1105n: from this line until c_pvr_run.py dev-w25-den exits, every LOG.md writer and every other paper's laptop job is paused (§4 of W25_DEV_RUN_DOC_v1_5_ADDENDUM_r2 <sha8 of this file>, amending W25_DEV_RUN_DOC_v1_4 186af09); HEAD $(git rev-parse --short HEAD), c_pvr_run.py 3d3eeed0, v1 outputs ffdcb6ba/b91b1336; preconditions §3 all PASS ($(sha256sum < "$PRE/pre_den.txt" | cut -c1-8)); netns ${NS:-off}; no other LOG line until the exit."
printf '%s\n' "$PL" | /usr/bin/python3 -I -B -c '
import re, sys
sys.path.insert(0, "scripts/c_pvr")
import gates as G
tag, log = sys.argv[1], sys.argv[2]
pl, b = sys.stdin.read(), open(log, "rb").read()
t = b.decode("utf-8")
rx = re.compile(r"(?<![\w-])" + re.escape(tag) + r"(?![\w-])")
ok = [b.endswith(b"\n"), bool(re.fullmatch(r"OPS-[0-9A-Za-z][0-9A-Za-z-]*", tag)),
      sum(bool(rx.search(x)) for x in t.splitlines()) == 0, pl.count("\n") == 1 and pl.endswith("\n"),
      bool(G.STAMP.match(pl)), len(rx.findall(pl)) == 1, bool(re.search(r"(?<![\w-])W25(?![\w-])", pl)),
      bool(re.search(r"(?i)\bpause", pl)), "\t" not in pl, "<" not in pl and ">" not in pl]
print("P14", "LOG-utf8-LF tagform tag0-in-LOG oneline stamp tag1-in-line W25 pause notab filled", ok)
sys.exit(0 if all(ok) else 1)
' "$TAG" "$L" > "$PRE/p14_den.txt" 2>&1 || { cat "$PRE/p14_den.txt"; echo "P14 FAIL: no pause line"; exit 1; }
[ ! -e "$SD" ] && mkdir -m 700 "$SD" || { echo "LAUNCH GUARD: $SD exists; no pause line"; exit 1; }
printf '%s\n' "$PL" >> "$L"; sleep 2
{ wc -l "$L"; sha256sum "$L"; } > "$SD/quiet_pre.txt"; [ "$(tail -n 1 "$L")" = "$PL" ] && echo "pause line is last"
setsid -f /bin/sh -c 'echo $$ >"$1/sh.pid"; OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 $2 "$3" -I -B scripts/c_pvr/c_pvr_run.py dev-w25-den --host laptop --run-sha "$4" --pause-tag "$5" --owners-sha "$6" --feats-sha "$7" --sscd "$8" --in "$9" --stage "${10}" >"$1/den_stdout.txt" 2>"$1/den_stderr.txt"; echo "rc=$? $(date -u +%FT%TZ)" >"$1/den_rc.txt"' \
  sh "$SD" "$NS" "$FT" "$RUN" "$TAG" "$OWN" "$F" "$SSCD" "$IN" "$STG"
```
- **Waiting (no watcher).** No Pool is opened (no image is read), so the v1.4 freeze path does not arise. The
  coordinator checks `$SD/den_rc.txt` every few minutes. Expected: about 10-20 min [est.: `dev_inputs` as `dev_pre`,
  about 5-10 min; the in-memory recompute incl. 80,081 D-EN rows, a few minutes]. If `$PY` (pid route of v1.4 §3.4)
  is alive at `sh.pid` mtime + 4 h 30 min, one SIGTERM; then v1.4 §6 E2 and §6A (A then B) apply by reference.
- **After the exit:** §7 checks, then `OPS-<MMDD>c-w25den-result`, then at once `OPS-<MMDD>c-w25den-resume`.

## 5. PASS rule, written before the run (d)
PASS **iff** all of (CC-265 W5: the code's pre-window guard `DEN_ROWS` (80,081 matched; missing exactly {388662,
397819}) and its in-run N2 equality are the in-code halves of the items below; §7 checks the outputs):
- `den_rc.txt` reads `rc=0`;
- `dev_w25_den_counts.json`: `d_en.n` = **80,083**; `d_en_no_feature_row` = **2**; the 2 ids are **388662 and
  397819** (the pre-window guard FAULTs otherwise, and both appear in `dev_w25_den_out_ids.json` `datastore.d_en`);
  `queries` and `featured` equal those of the v1 `dev_w25_counts.json` b91b1336; `n2_equal_outside_d_en` = true;
  `run_sha256` = `3d3eeed09c7ebb13e00f84ddf347754c1d8cb78464f8acccfc4f4eb7d721ec1d`; `dev_run_sha256` = 84b0d587…; `w25_run_sha256` = 290a75dc…;
- the v1 files are byte-unchanged: `dev_w25_out_ids.json` ffdcb6ba…, `dev_w25_counts.json` b91b1336…;
- stderr holds no line outside the PIL palette allow-list (CC-261 N1; §7).
D-EN's `flagged`, `out` and `kept` are recorded, with no threshold on them. They stay internal (PI-1101o; CC-261 N7).

## 6. Stop rule (e)
- **Any FAULT, abort, `Stop`, a failed PASS item, or a departure from §5 goes to a full panel at 85 and to the PI.
  No retry and no second supplement without a PI line** (CC-261 K5). The code itself refuses a second run (a
  `dev-w25-den start` row or either output present).
- A pre-window FAULT (no `dev-w25-den start` row, e.g. the `DEN_ROWS` guard) consumes nothing, but it is still a
  departure: panel and PI, no retry on the agent's own call.

## 7. After the exit (f)
```sh
. "$HOME/w25dev_env_3.sh"; cd "$R"
echo "v1 evidence $(sha256sum < "$PRE/pre.txt" | cut -c1-8) $(sha256sum < "$PRE/p14.txt" | cut -c1-8)"      # 831604ef 616901e1 (CC-267 B3)
cat "$SD/den_rc.txt"; grep -v -e 'UserWarning: Palette images with Transparency expressed in bytes should be converted to RGBA images' -e '^  warnings.warn($' "$SD/den_stderr.txt" | wc -l    # rc=0; 0 lines outside the allow-list
ls /dev/shm/c_pvr_w25 2>/dev/null && echo RESIDUE
{ wc -l "$L"; sha256sum "$L"; } > "$SD/quiet_post.txt"; cmp "$SD/quiet_pre.txt" "$SD/quiet_post.txt" && echo "quiet held"
cut -f3 "$HOME/.vsps_sealed/c_pvr/ACCESS_LOG.tsv" | grep -n '^dev-w25-den \|^ovqa-pin' | tail -n 4     # start, ovqa-pin read, decide, end
tail -n 2 "$HOME/.vsps_sealed/c_pvr/w25_deletions.log"                                               # trap line last
sha256sum manuscript/prereg/2026-11-02_c_pvr_tier1/{dev_w25_out_ids.json,dev_w25_counts.json,dev_w25_den_out_ids.json,dev_w25_den_counts.json}
/usr/bin/python3 -I -B -c '
import hashlib, json, sys
P = "manuscript/prereg/2026-11-02_c_pvr_tier1/"
h = lambda f: hashlib.sha256(open(P + f, "rb").read()).hexdigest()
v1, d, o = (json.load(open(P + f)) for f in ("dev_w25_counts.json", "dev_w25_den_counts.json", "dev_w25_den_out_ids.json"))
ok = {"v1 ids ffdcb6ba": h("dev_w25_out_ids.json").startswith("ffdcb6ba"), "v1 counts b91b1336": h("dev_w25_counts.json").startswith("b91b1336"),
      "d_en n 80083": d["d_en"]["n"] == 80083, "no_feature_row 2": d["d_en_no_feature_row"] == 2,
      "388662 397819 out": {"388662", "397819"} <= set(o["datastore"]["d_en"]), "queries = v1": d["queries"] == v1["queries"],
      "featured = v1": d["featured"] == v1["featured"], "n2": d["n2_equal_outside_d_en"] is True,
      "run": d["run_sha256"] == sys.argv[1], "dev run 84b0d587": d["dev_run_sha256"].startswith("84b0d587"),
      "w25 run 290a75dc": d["w25_run_sha256"].startswith("290a75dc")}
print(ok, "d_en", {k: d["d_en"][k] for k in ("n", "flagged", "out", "kept")}); sys.exit(0 if all(ok.values()) else 1)' "$RUN"
/usr/bin/python3 -I -B -c 'import ast,hashlib; t=open("scripts/c_pvr/c_pvr_run.py","rb").read(); assert hashlib.sha256(t).hexdigest()=="3d3eeed09c7ebb13e00f84ddf347754c1d8cb78464f8acccfc4f4eb7d721ec1d"; c=next(ast.literal_eval(n.value) for n in ast.parse(t).body if isinstance(n,ast.Assign) and getattr(n.targets[0],"id","")=="CODE"); print("CODE re-hash", len(c), "bad", [p for p,h in c.items() if hashlib.sha256(open(p,"rb").read()).hexdigest()!=h])'
```
Expected: `v1 evidence 831604ef 616901e1`; `rc=0 …`; `0`; no RESIDUE; `quiet held`; the 4 ACCESS_LOG actions in order; the trap line last; v1 shas
ffdcb6ba / b91b1336; the dict all True (exit 0); `CODE re-hash 10 bad []`. The D-EN counts printed go to the result
line and the S7' record only (internal).

## 8. The S7' record (g; CC-261 K6, K7, N1, N3)
The S7' full-panel read (85, round 2/3 of the CC-261 topic) gets, in its record and the result line:
- both sealed hand rows: `OPS-1105c-sealed-handrow` (LOG l.1570) and `OPS-1105c-sealed-handrow2` (LOG l.1595);
- the E3 wording: "textvqa_textcaps_val: images inside the pinned TextVQA archive, no val id list held"; no TextCaps
  val member was extracted, decoded or featurized;
- the K_TRUNC disclosure (CC-259 W5): "One OpenViIC training image whose file is truncated (1 byte) was removed from
  D-VI (8,377 registered, 8,376 used), as in C's stage-1 memory." (dvi_openviic `dropped_truncated` 1);
- **deviation D-EN:** the int64/str id defect voided D-EN in the v1 run (cause, CC-261 R3); remedy = this addendum's
  one D-EN-only supplement under PI-1105n (code `817adb3`), D-EN's first evaluation;
- **deviation stderr (N8 erratum, CC-261 R2/N1):** v1.4 expected "stderr 0 bytes"; the run wrote 2,233 B of PIL
  "Palette images with Transparency" UserWarnings (0 images lost; the same lines as decode_out 083c9f42). The expectation
  was a drafting error; this addendum uses an allow-list instead;
- every t2pool block, including **openviic_test_confirm** (n 981, out 95, kept 886), which the result line l.1606
  omitted (N3), with the ACCESS_LOG line number of every action of both runs;
- all of this stays internal (LOG, CC, addendum, deviation record): no D-EN counts and no repair text in the paper
  (CC-261 N7, PI-1101o; PQ-DISC is the PI's).
On the S7' GO, one gatekeeper commit holds the two v1 files, the two D-EN files and one datastore pin line (CC-261 R4).

## 9. Rulings asked of the one-judge read
| # | ruling | recommended | default |
|---|---|---|---|
| X1 | this addendum amends v1.4 for one `dev-w25-den` run; v1.4 rules not changed here stay in force | GO | no run |
| X2 | the PASS rule §5 and the stop rule §6, as written before the run | YES | no run |
| X3 | `w25dev_env_3.sh` = `_2` with RUN/DOC changed and `SD=` added; same dirs | YES | same |
| X4 | no watcher; one SIGTERM at 4 h 30 min; v1.4 §6/§6A by reference | YES | same |
| X5 | stderr judged by the PIL palette allow-list (N1) | YES | same |

## 10. Touches during drafting
- Read the sources above (code text only; LOG by line; `pre.txt` P15 block; the env file's RUN/DOC/D0/S lines).
- Not touched: `~/.vsps_sealed` (no `find`, `du` or `ls -R` over `/` or `$HOME`); ACCESS_LOG; any output file body;
  any caption or label. Nothing run, downloaded or committed.
