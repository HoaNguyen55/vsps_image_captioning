# C-PVR-T1 pixel W25 run document v1.4 (Paper C, ACM TALLIP; prereg §8, §9.1 step 8): DRAFT for its one-judge diff read (R2, round 2/3)

**Status:** draft for the R2 diff read v1.3 → v1.4: one judge, round 3/3 of the CC-250 topic (the last before
ESCALATE_TO_PI), REVERSIBLE 85 (PI-1029o as amended by PI-1103ad/ae; CC-250r2 NEXT STEP).
It licenses nothing until a GO. Nothing in it has run.
v1.1 written 2026-11-03 about 18:15-18:46Z (`date -u`; the v1.1 LOG stamp is 18:46:15Z). v1.2 written 2026-11-03 about
19:05-19:40Z. v1.3 written 2026-11-04 about 01:15-01:50Z. v1.4 written 2026-11-04 about 01:50-02:20Z (`date -u`),
HEAD ab1dd77.
- It supersedes `W25_RUN_DOC_v1_3.md` a7700d33, `W25_RUN_DOC_v1_2.md` 9093a0e1 (never read), `W25_RUN_DOC_v1_1.md`
  d123786d and `W25_RUN_DOC_v1.md` a2dece2a (all unchanged, kept in their snapshots) for the window. v0 `W25_PIXEL_RUN_DRAFT.md` 82610ad4 §1 (purpose, query sets), §3 (host, time, cost) and
  §7 (n_e_power, timeline) still hold by reference, except where this text differs. So v0 is registered with this file
  (W-R5, N45).
- **Label:** TIER 1 / DEV-EXPLORE (C-PVR-T1).
- **N28 (CC-248, BLOCKING for the R2 GO per CC-249 Ruling 6) is answered in §6A and PQ5; it closes with N40 (CC-250
  Ruling 2).**
- **Scope of v1.2:** CC-250 N38-N46 only (table §A0). Nothing else changed from v1.1.
- **Scope of v1.3:** v1.2 (D1-D9 unchanged) plus CC-251 N47-N56, PQ5 = C done, PQ5b, PQ7 answered (table §A1).
  Nothing else changed from v1.2.
- **Scope of v1.4:** v1.3 plus CC-250r2 N57 (BLOCKING), N58, and the optional N59, N60, N62, N64 (table §A2). Nothing
  else changed from v1.3.
- **Line references** are at `c_pvr_run.py` 290a75dc (re-derived by grep), except inside the record tables §A and §A0,
  which keep their 4af623d0 references.

**Sources read:**
- CC-251 (sha a029773f) and CC-250 (sha 75a83a20) in full; CC-245r3, CC-247, CC-248, CC-249 in full; CC-242r2 Rulings 7-9 and G0-G14;
- W25_RUN_DOC_v1 a2dece2a and v1.1 d123786d in full; TEXTCAPS_PIN_DRAFT b3daefb5 in full;
- LOG l.1453-1469 and l.1473 (PI-1104c), l.1481 (OPS-1104c-run-code-r5), l.1484 (CC-251), l.1485
  (OPS-1104c-run-commit-r5);
- `c_pvr_run.py` 290a75dc (code only, by grep): `CODE` l.51-62, `FAULT_ERR` l.74, `write_new` l.140, `integrity`
  l.147-157, `owners_load` l.743, `owner_feats` l.766, `no_sockets` l.802, `owner_feats_cmd` l.823-863 (features call
  l.844), `stage_nocaps` l.886-902, `featurize` l.911 (features call l.914), `write_part` l.942, `read_part` l.949-954,
  `run_set` (part print l.1003), `ovqa_zip` l.1023 (curl l.1029), `deadline` l.1045, `sig_handler` l.1105 (worker
  branch l.1107), `w25_pre` l.1120, `w25` l.1134-1194 (flock l.1143), `real_env` l.1201 (workers line l.1208),
  selftest `workers=1` l.1541/1570/1653, start-method assert l.2044, `main` l.2069 (`set_start_method("spawn")`
  l.2072); `gates.write_new` l.943-965; `build_memory.features` l.150-200.

---

## A2. Changes from v1.3 (CC-250r2 sha 73fd99e8, LOG l.1493-1494; each cites its source)

| # | item | v1.3 text | source | exact fix in v1.4 |
|---|---|---|---|---|
| G1 | provenance of the 13 staged caches; the 19-file account; PQ5b | "The 13 staged caches were made earlier on other hosts"; "Recomputing them would touch test-set pixels (KTVIC, OpenViIC and UIT-ViIC test, Karpathy test)"; PQ5b "The other 13 were made earlier on rented machines"; 4 files unaccounted | CC-250r2 N57 (BLOCKING), Rulings 5-6; LOG l.911, l.938, l.1494 | §6A(i) states: 8 copied from rented-machine backups; 5 in `~/vsps_w25k1`, 4 of them (ktvic_test, openviic_test, uitviic_test, t2) computed there under fork; oiv7_val's origin not claimed; all 13 read by sha. "At least 4 of them are test-set files" (feats_coco_test, ktvic_test, openviic_test, uitviic_test). All 19 files accounted for. PQ5b = the CC-250r2 Ruling 5 text, verbatim. §A1 F5 left as the v1.3 record; this row supersedes it |
| G2 | pause-line file name | "§4 of W25_RUN_DOC_v1_3 <sha8>" | CC-250r2 N57, Ruling 7 | "§4 of W25_RUN_DOC_v1_4 <sha8>". W-R5 registers v1.4 + v0; v1.2 and v1.3 also stay untracked |
| G3 | worker-handler mechanism | "If a worker still blocks … in a C-level call, it never runs its Python handler" (the fork case) | CC-250r2 N58, Ruling 3 | Under spawn the workers have SIG_DFL for SIGTERM, so `terminate()` ends a worker in an interruptible wait. The teardown hang stays possible by three routes: a worker in D-state; the pool lock held by a killed worker; the parent blocked in a C call (SSCD/torch). In the third, step 1 does not help; step 2 applies after 10 min. No command changes |
| G4 | EXP check (optional) | none | CC-250r2 N59 | §3.5, outside the watcher block: EXP recorded as an integer 0..24; the first `watch.txt` line must read `parts=0/<EXP> armed=1` (or `armed=0` when EXP = 0); else the coordinator restarts the watcher only. Watcher text unchanged |
| G5 | P21 ppid check (optional) | none | CC-250r2 N60 | P21 signals a spawn worker or tracker only if its ppid = 1 or a P4 selftest PID recorded in pre.txt |
| G6 | 4af623d0 wording (optional) | "appears below only as the sha that wrote `c_pvr_lists.json`" | CC-250r2 N62 | "appears below only as lists provenance or in history rows" |
| G7 | optional ViTextVQA dev check rule | none | CC-250r2 N64, Ruling 8 (3) | the pre-written rule is copied into §6A(i); binding only if the PI picks it |
| — | N61 (end-line drift), N63 (STATE) | — | CC-250r2 N61, N63 | not changed: N61 is a record only; N63 is the coordinator's |

## A1. Changes from v1.2 (CC-251, PI-1104c; each cites its source)

| # | item | v1.2 text | source | exact fix in v1.3 |
|---|---|---|---|---|
| F1 | kill line vs resource_tracker; argv-tag sentence | kill if ppid = `$PY` and comm python*; "the workers carry the tag in argv" (§3.4, §6A H4) | CC-251 N47, Ruling 4 | The kill line adds `grep -qaF spawn_main /proc/$p/cmdline` (quiet, fixed string, child only), so the tracker (comm python, no `spawn_main`) is never killed. `hang.txt` labels each child `worker`, `tracker` or `other`. The argv sentence now says: under spawn the tag is not in a worker's /proc cmdline (only in its memory); `$PY`'s own cmdline has it; no evidence file prints a cmdline |
| F2 | `sem.mp-*` in /dev/shm | not mentioned | CC-251 N48 | P12a/P12b, `hang.txt` and §3.6 record `ls /dev/shm \| grep -c '^sem\.mp-'` (count only). Nothing is removed by hand. §6A states they exist while a Pool is open and go at a normal exit |
| F3 | run sha and line drift | RUN' = 4af623d0 in §0, §1, §2, P1, P4, W-R3, §3.4, pause line; P5 18/9; line refs at 4af623d0 | CC-251 N49, Ruling 6; LOG l.1485 | RUN' = 290a75dc (commit ab1dd77) only where it is the w25 run sha. 4af623d0 stays as lists provenance (N31 triple, §3.1, W-R3b); fb35ec94 stays for owners and owner-feats. P5 = 3 files, 25 insertions / 10 deletions vs 155b6c01; §1 lists the 3c1ee0e → ab1dd77 hunks. P4 notes a solo selftest of about 31 s. The pause line names CC-251. Line refs re-derived at 290a75dc |
| F4 | §6A(i), PQ5, §1 "held back" | C offered as a choice; "any hang mitigation, unless PQ5 = C" | CC-251 N50, Ruling 2; PI-1104c | §6A(i) states C is DONE (spawn in `main` l.2072): it removes the fork-after-threads path by construction, but is not shown to remove the hang; the stress test (0/18 old vs 0/18 new) does not discriminate; the rate stays unmeasured; A then B stay the backstop. The 24 `Pool(4)` count is kept. spawn, not forkserver, with the reason. §1 records C as the one allowed pre-launch change, now done |
| F5 | equality scope | none | CC-251 N51; PI-1104c | §6A(i) states the scope: 64 dev images, 2 of the 6 laptop caches (2 of the 19 files), bit-identical; the 13 staged caches are read by sha and never recomputed (test-set pixels); optional 32 vitextvqa_dev ids before P1. New **PQ5b**; P16 must carry its answer |
| F6 | P11/P21 patterns | c_pvr names only | CC-251 N52 | add `multiprocessing.spawn` and `multiprocessing.resource_tracker`; the P21 by-PID rule covers them, before the pause line only |
| F7 | post-run code re-hash | none | CC-251 N53 | §3.6 re-hashes `c_pvr_run.py` and the 10 `CODE` files against the launch pins; the result line records it; a mismatch → one-judge read before any output is used |
| F8 | watcher `kids=` and `cpu` | not stated | CC-251 N54 | §3.5 states that `kids=` and `cpu` include the tracker, so `kids=1` between batches is the tracker. The watcher text is unchanged (P18 unchanged) |
| F9 | records | none | CC-251 N55, N56 | §6A(i): `no_sockets()` does not reach spawned workers; `sig_handler`'s worker branch is dead code, held with N29; the W25 flock is not inherited by workers. feq.py and the stress harness stay in the r5 snapshot, not committed |
| F10 | PQ5, PQ7, PQ1-PQ4 status | open questions | PI-1104c (LOG l.1473) | PQ5 answered C, DONE; A then B backstop. PQ7 answered YES. PQ1-PQ4 not yet approved; kept as asked. P16 now needs PQ1-PQ4 and PQ5b; P17 cites PQ7 = YES |

## A0. Changes from v1.1 (CC-250; each cites its source)

| # | item | v1.1 text | source | exact fix in v1.2 |
|---|---|---|---|---|
| D1 | bytecode before P1; P3 that can pass | P3 `find scripts/c_pvr scripts/w25 scripts/c_stage1 …` must be empty, but `scripts/w25/__pycache__` and `scripts/c_stage1/__pycache__` exist, and other CODE-closure dirs hold bytecode. `-B` stops writing bytecode, not reading it | CC-250 N38 (BLOCKING); Q11 C20 precedent | New coordinator step **B0** before P1 (§3.3): list, then remove, the git-ignored `__pycache__` dirs and `*.pyc` of the 8 CODE-closure dirs (`CODE` l.50-61); the list goes into pre.txt; one LOG line `OPS-<MMDD>c-w25-bytecode` before the pause line. **P3** covers the same 8 dirs and must print nothing; it is run again right before P14. v1.2 only plans this; nothing was removed while drafting |
| D2 | phase-aware stall | the E1/H1 60-min stall applies until `w25_rc.txt` exists, so it can fire during `decide` (nothing is printed there) | CC-250 N39 (BLOCKING) | The stall is **armed only while part lines are pending in this window**. The watcher takes a 4th argument `EXP` = the part lines expected in this window (24 on a first window; on a resume, 24 minus the part lines of all earlier windows, from their result lines). Once `parts ≥ EXP`, or from the start if `EXP = 0`, the stall is off; the wall stays on. The same for `AUTO=0`. Each result line records its part-line count. Decide estimate and ovqa_zip margin stated (§3.5, §6, §6A) |
| D3 | §6A(i) evidence, option C, PQ5 | "owner-feats ran the same `Pool(4)` path … no hang"; C = "`workers=1`, or a non-fork pool start method in a pinned module" | CC-250 N40 (BLOCKING), Ruling 5, Ruling 7 | §6A(i) states: a window opens 24 `Pool(4)` (21 NoCaps + 3 OpenViVQA batches), owner-feats opened 6; the observed hangs ran with `Pool(1)` (selftest `workers = 1`); the rate is unmeasured. C's `workers=1` form is removed; C = a non-fork start method set in `c_pvr_run.py` `main` (new sha). PQ5 gains: "A freeze is possible; we have not shown it is rare in this long run." Recommendation A and the default unchanged |
| D4 | curl and H3 "frozen" | §3.4 "the curl fetchers are children of `$PY`"; H3 frozen = CPU flat **and** `curl=0` | CC-250 N41, Ruling 3 | NoCaps fetches are urllib threads inside `$PY` (`stage_nocaps` l.885-901, `cen_fetch.get` l.236-251); curl is a child only during `ovqa_zip` (l.1029). H3 "frozen" rests on CPU ticks only, with the disclosure that in the NoCaps fetch phase it cannot tell a network wait from a freeze. P15 notes that it probes with curl while the window fetches with urllib |
| D5 | prepared kill line | `kill -KILL <pids>` | CC-250 N42 | One shell line per PID; it kills only if, at that moment, the PID's ppid = `$PY` and its comm starts `python` (§6A H4) |
| D6 | torn ACCESS_LOG row | P12b has no end-of-file check | CC-250 N43; CC-242r2 G3 torn-row clause | P12b adds `tail -c 1` of ACCESS_LOG.tsv = LF (one byte of the declared file). A torn last row goes to the one-judge read of the cause. The §6A G-table cites G3's torn-row clause |
| D7 | line drift; H3 window; header time | owner_feats_cmd l.830-858, read_part l.941-956, w25 l.1133-1192, real_env l.1207, C1 cite l.1158-1161; H3 "last 3 lines (15 min)"; header "18:15-19:00Z" | CC-250 N44 | owner_feats_cmd l.822-862 (features l.843); read_part l.948-953; w25 l.1133-1193; real_env l.1200 (workers l.1207); C1 cite l.1160-1161; H3 uses the last **4** `watch.txt` lines (15 min); header time corrected |
| D8 | registration paths; v1 §12 | "the rest of v1 §12 stands"; W-R5 names this file only | CC-250 N45, Ruling 8 | v1.2 keeps the v0 reference, so W-R5 registers v1.2 **and** v0 82610ad4 (exactly 2 paths). §12 quotes the one v1 §12 sentence relied on |
| D9 | STATE | — | CC-250 N46 | Noted only: the coordinator updates the next STATE file's C row (§12) |

## A. Changes from v1 to v1.1 (record, as in v1.1; each cites its source)

| # | item | v1 text | source | exact fix in v1.1 |
|---|---|---|---|---|
| C1 | P12 resume form | P12 asks for no `'w25 '` row and an absent `~/.vsps_sealed/c_pvr/w25`, so it fails every resume, although §7 says "P1-P20 re-run". It also uses `ls -d` and `stat` on the sealed dir by hand | coordinator erratum; `w25` l.1160-1161 (parts dir `exist_ok`, deadline kept); CC-248 Ruling 7 ("No agent lists or reads ~/.vsps_sealed by hand") | P12 is split into **P12a** (first window) and **P12b** (resume window). Both use the ACCESS_LOG action field (`cut -f3`) only. The `ls -d` and `stat` of the sealed dir are dropped (§5) |
| C2 | RUN' scope wording | §1 l.44: "the fb35ec94 → RUN' diff touches only LISTS_IN, _st_lists and the mutant harness (TEXTCAPS_PIN_DRAFT §3)". That cites a draft section that holds the rejected item 3, mixes file shas with commits, and leaves out SHA256SUMS | CC-247 Ruling 5 (item 3 rejected); CC-248 Ruling 1; CC-249 N33; LOG l.1463, l.1465 | §1 now says: `git diff --stat 155b6c01 3c1ee0e -- scripts/c_pvr` = 3 files, 18 insertions / 9 deletions: `c_pvr_run.py` (2 hunks: the LISTS_IN `textcaps_train` line; the `_st_lists` assert l.1492 `== []`), `c_pvr_run_mutants.py` (N20, N23), `SHA256SUMS` (2 lines replaced). P5 expects exactly this |
| C3 | `$TH` | §2 l.66 `TH='OMP_NUM_THREADS=1 MKL_NUM_THREADS=1'`; P4 "with `$TH`" | coordinator erratum; CC-245r3 N22 | `TH` is deleted. Quoted, `env "$TH" cmd` passes ONE word, so `env` sets `OMP_NUM_THREADS` to `1 MKL_NUM_THREADS=1` and leaves MKL unset. Every line now writes `env OMP_NUM_THREADS=1 MKL_NUM_THREADS=1` (after `env -i …` where `-i` is used). The watcher records the live env of `$PY` (§3.5) |
| C4 | F2 HEAD `-L` | v1 has no F2 text. The CC-247 lesson (`-I` without `-L`: a 3xx passes `--fail`, and its headers are the redirect's) applies to P15 | CC-247 Ruling 2; LOG l.1460 | F2 is recorded as DONE (final-hop HEAD `-L`, LOG l.1460, §0). **P15 does NOT take `-L`**: the W25 Open Images fetch FAULTs on a redirect (`FAULT_ERR` l.73), so P15 must see the first answer. P15 PASS is read from `-w '%{http_code} %{content_type} %{num_redirects}'` = `200 image/jpeg 0`, never from rc alone. A 3xx is a P15 FAIL |
| C5 | Who performs F0 | v1 §0 lists "TextCaps pin" with no performer (the CC-247 drafter erratum 2 pattern) | CC-247 Ruling 1; LOG l.1460 | §0 records F0 as DONE by the coordinator (playwright-cli headless, hrefs only, PASS). Every remaining step in §0 and every E-step in §6 now names who acts |
| C6 | §12 "not listed" | v1 §12 says `~/.vsps_sealed` was "not listed" | LOG l.1454-1455 (hand row 26); l.1448 (row 19); l.1459 (row 29) | False. v1's drafting ran `ls ~/.vsps_sealed/c_pvr/ \| head -0` (names not printed): ACCESS_LOG hand row 26. The other hand rows on record are row 19 (CC-245 N9) and row 29 (CC-247 N24; ACCESS_LOG sha after it a4196013). Corrected in §12; v1.1's own touches are in §13 |
| C7 | N25 precondition | none | CC-247 N25; LOG l.1459 | New **P21**: no orphaned c_pvr or mutant python, checked after P4. P4 selftests run one at a time under `timeout -k 10 120` (§5) |
| C8 | N6, N7, N11, N12, N17, N22 | §9 | CC-245r3 carried; CC-247; CC-249 Ruling 6 | Kept in §9. N17: `lists` printed 1,676 (CC-249). N22: the env literal (C3); owner-feats and `lists` ran with it (LOG l.1461, l.1466); CC-245r3 Ruling 5 is qualified by CC-248 Ruling 4 (→ N28) |
| C9 | N27 | none | CC-248 N27 | The r4 mutant record is added to §9 |
| C10 | N29 | none | CC-248 N29 | Held by the same-sha rule until after `w25_counts.json` (§1) |
| C11 | N31 | none | CC-249 N31 | The triple lists edb07fbb / run 4af623d0 / owners 0cf330d3 is stated in §0 and in the result line (§8). The optional lists-record hardening is held by §1 |
| C12 | N32 (P7) | P7 "`lists` done (§3.1)" | CC-249 N32 | P7 made concrete: sha checks, LOG lines, ACCESS_LOG action counts, the owner-feats rc file. No file-mode check of the json (DrvFs) |
| C13 | N33 | placeholders `<F>`, `RUN'`, `<pin commit>`; W-R3b, W-R6 open; §0 order | CC-249 N33 | Filled: RUN2 = 4af623d0…e9b4; pin commit 3c1ee0e; F = 8f707edd…50f9; OWN = 0cf330d3…3b086; lists = edb07fbb…8e18. §3.1 `lists` marked DONE. W-R3b MOOT; W-R6 NOT TRIGGERED. §0 order updated |
| C14 | N34, N36 | §8 item 3 | CC-249 N34, N36 | The result commit names the three frozen jsons; the n-gram scan covers every staged blob, and its output is kept next to the snapshot |
| C15 | N28 hang plan | E2 "ask the PI for a WSL restart" only | CC-248 Ruling 4 and N28; CC-249 Ruling 6 | New §6A: risk, detection (no sealed listing), who acts, what is logged, parts, resume vs new run, G0-G14 consistency. PI question PQ5 rewritten with three options, a recommendation and a default |
| C16 | Watcher reads the sealed parts dir | §3.5 `ls ~/.vsps_sealed/c_pvr/w25/parts \| wc -l` every 5 min | CC-248 Ruling 7; C6 | Progress now comes from the flushed `"<set> part NNNN"` stdout line of `run_set` in `$S/w25_stdout.txt` (ext4). The watcher never touches `~/.vsps_sealed`. It also records CPU ticks and curl children (§3.5). This makes the W-R4 "row" question moot |
| C17 | PQ count | PQ1-PQ7 | task; N28 | Seven questions kept. PQ5 (the hang question) is expanded into the N28 question; the others are unchanged except dates |

## 0. Summary

| item | value |
|---|---|
| Host | laptop CPU only (prereg §8), 0 VND |
| Time | about 1.5-5.5 h [est., v0 §3]; registered stop 24 h from the first start (in code, `deadline` l.1045) |
| Code | `c_pvr_run.py` 290a75dc (RUN', spawn start method) at commit ab1dd77; c_pvr.py 8f10bd60, gates.py 3bced05e, w25.py d6d12780 unchanged |
| Frozen inputs | owners 0cf330d3 (LOG l.1449); owner-feats manifest 8f707edd (LOG l.1461); lists edb07fbb (LOG l.1466, CC-249 GO 93) |
| Provenance triple (N31) | lists edb07fbb was written by run 4af623d0 on owners 0cf330d3 (CC-249 integrity chain; the json carries no run sha) |
| Gold | none: pixels, ids, keys and container lengths only |
| Result | `w25_counts.json` → n_e_power = 10,182 − flagged − lost − 4 (`gates.n_e_power`) |

**Order and performers:**

| # | step | who | state |
|---|---|---|---|
| 1 | owner-feats (fb35ec94, OMP/MKL 1) | coordinator | DONE, rc 0, 46.5 min, manifest 8f707edd (LOG l.1461) |
| 2 | TextCaps pin F0-F5 | coordinator (F0: playwright-cli headless, hrefs only; F2: HEAD `-L`, final hop) | DONE, F0 PASS, two-source pin (LOG l.1460, CC-247 GO 90) |
| 3 | 4af623d0 diff (TextCaps pin), read, gatekeeper commit | writer agent; CC-248 judge; gatekeeper | DONE, commit 3c1ee0e (LOG l.1463-1465) |
| 4 | `lists` + T6 check | coordinator; CC-249 judge | DONE, edb07fbb, 0 FAULT (LOG l.1466-1467) |
| 5 | N35 copy of the lists json | coordinator | DONE (LOG l.1468) |
| 5b | PQ5 = C: spawn start method (r5), read, gatekeeper commit | writer agent; CC-251 judge; gatekeeper | DONE, commit ab1dd77 (LOG l.1481, l.1484-1485) |
| 6 | R2 diff read v1.1 → v1.3 (round 2/3) | one judge | next |
| 7 | W-R5 registration commit of this file | gatekeeper | after the R2 GO |
| 8 | PI window line (PQ1-PQ4, PQ5b; PQ5 and PQ7 answered in PI-1104c) | PI in chat; the coordinator writes the PI-<id> line | before P9 |
| 9 | staging (§3.2) | coordinator | before P9 |
| 10 | B0 bytecode removal and its LOG line (§3.3), then P1-P21 (§5) | coordinator | right before the pause line |
| 11 | pause line (§4.1) | coordinator | one `>>` |
| 12 | launch + watcher (§3.4, §3.5) | coordinator | detached |
| 13 | watch, E-ladder (§6, §6A) | watcher (files only); coordinator; PI at E2 (PQ5) | in the window |
| 14 | §3.6, result line, resume line | coordinator | after the exit |
| 15 | R4 result read | one judge (full panel at 85 on any fault) | after the resume line |
| 16 | result commit (W-R7) | gatekeeper | after the R4 GO |
| 17 | n_e_power line | coordinator | after the commit |

## 1. Which sha runs, and the same-sha rule

- **`w25` runs at RUN' = 290a75dc** (the r5 spawn sha), committed at ab1dd77 (CC-251 GO 90). SUMS holds only this
  `c_pvr_run.py` line, and `integrity()` refuses any other `--run-sha` (l.147-157). The earlier sha 4af623d0 (commit
  3c1ee0e) appears below only as lists provenance (N31) or in history rows (N62).
- owners (built at fb35ec94), owner-feats (run at fb35ec94), the 6 `of_*.npz` and the 13 staged caches stay valid at
  RUN' (CC-251 Ruling 3):
  - `owners_load` (l.743-762) and `owner_feats` (l.766-786) check the owners sha, the manifest sha, `owners_sha256`, n
    and `source_sha256`, never a run sha. The only run-sha check is `read_part` (l.949-954, W25 parts only), and no
    W25 part exists.
  - owner-feats ended rc 0 at 17:18:23Z, before the 4af623d0 edit at 17:37:07Z (CC-248).
  - **Scope (C2):** `git diff --stat 155b6c01 3c1ee0e -- scripts/c_pvr` = 3 files, 18 insertions / 9 deletions:
    `c_pvr_run.py` (2 hunks: LISTS_IN `textcaps_train`; `_st_lists` l.1492 `== []`), `c_pvr_run_mutants.py` (N20,
    N23), `SHA256SUMS` (2 lines replaced). CC-247 Ruling 5, CC-248 Ruling 1. The R2 judge re-runs it (W-R3).
  - **Scope (N49):** `git diff --stat 3c1ee0e ab1dd77 -- scripts/c_pvr` = 3 files, 9 insertions / 3 deletions:
    `c_pvr_run.py` (`import multiprocessing` l.30; the selftest assert `get_start_method(allow_none=True) == "spawn"`
    l.2044; `main()` first statement `multiprocessing.set_start_method("spawn")` with a two-line comment, l.2070-2072),
    `c_pvr_run_mutants.py` (mutant `start_fork` l.265; one comment word l.290), `SHA256SUMS` (2 lines replaced). No
    `CODE` pin and no pinned module changed (CC-251).
  - **Combined:** `git diff --stat 155b6c01 ab1dd77 -- scripts/c_pvr` = 3 files, 25 insertions / 10 deletions (numstat
    SHA256SUMS 2/2, c_pvr_run.py 8/2, c_pvr_run_mutants.py 15/6). P5 expects exactly this.
  - The W-R5 registration commit touches `manuscript/` only, so this diff is unchanged at the launch HEAD.
- **Same-sha rule (N11, binding).** No byte of `c_pvr_run.py` (and no SUMS line) changes between the first `w25`
  launch and the existence of `w25_counts.json` with its 'w25 decide' row.
  - Why: every part records `run_sha256`, and `read_part` refuses a part from another sha. A sha change forces a
    re-fetch of every NoCaps-test pixel.
  - Held back until after the result: `score` (N11); N29 (killpg `try/except`); the N31 option (run and owners shas
    in the lists record); the dead worker branch of `sig_handler` (N55); any other hardening. The one allowed
    pre-launch change, PQ5 = C, is DONE (ab1dd77, before any launch; CC-251 Ruling 7). No further hang mitigation
    is planned before the result.

## 2. Notation

```
R=/mnt/d/vsps_image_captioning
L=.session_backup/2026-10-13/decisions/LOG.md                          # relative to $R
FT=$HOME/.venvs/c_stage1_lists/bin/python                              # R1a
CV=$HOME/.venvs/c_pvr/bin/python
SSCD=$HOME/backups/vsps_image_captioning/.session_backup/2026-10-22/c_stage1/sscd_disc_mixup.torchscript.pt
IN=$HOME/c_pvr_w25_in                                                  # owner-feats --in dir (ext4); 6 of_*.npz
OWN=0cf330d39ae4a24b1e95841fbb16f617d405a9d4ffca9747498ef33657f3b086   # LOG l.1449
F=8f707edd3c30180d05a597bd7867a278605e3c9f3cdfc93ebc8544b98d7b50f9     # owner-feats manifest, LOG l.1461
RUN2=290a75dc414df655d4bdb5f2f18947b3885305673f647bc6d4c6556d0087a352  # RUN' (r5, spawn), commit ab1dd77
LISTS=edb07fbbea45b69b246ec1e82e23103784b7c777c4e0ef6737e49151d1dc8e18 # c_pvr_lists.json, LOG l.1466
PRE=$HOME/w25pre_<MMDD>                                                # checklist dir, ext4, separate from $S
S=$HOME/w25run_<MMDD>                                                  # launch dir, absent until launch
```
There is no `TH` variable (C3). The thread env is written out in full on every line.

## 3. Exact command sequence

### 3.1 `lists`: DONE (LOG l.1466, CC-249 GO 93)
- Run once at HEAD 3c1ee0e, `--run-sha` 4af623d0, `env OMP_NUM_THREADS=1 MKL_NUM_THREADS=1`, rc 0 at 17:57:20Z,
  stderr 0 B. `c_pvr_lists.json` = edb07fbb (untracked, write-once). One 'lists write' row.
- T6: every TEXTCAPS_PIN_DRAFT §5 field matched, 0 FAULT. Snapshot `.session_backup/2026-11-04/c_lists/` (N35).
- It is never run again (write-once). It does not gate the window: `w25` never reads it. W-R6 was not triggered.
- The removal counts in it never go into a paper, cover letter or talk (PI-1101o; CC-249 Ruling 4).

### 3.2 Staging the 13 cached caches (coordinator; before P9; never in the window)
There is no `stage-inputs` subcommand. Staging is a hand copy into `$IN`, beside the six `of_*.npz` files. The staged
name must equal the OWNERS cache key; `owners_load` re-hashes every one before the window.
```
mkdir -m 700 "$PRE"          # then write $PRE/stage.sha256 from the text below; its sha goes in pre.txt
M=$R/.session_backup/machines
cp -n $M/M1/root/outputs/c_en/{feats_nocaps_val,feats_coco_test,feats_coco_kval,feats_memory}.npz "$IN"/
cp -n $M/M1/root/b_w25slot/out/{c7_coco_gap_val2014,c7_a_t3_val2017,c7_pascal50s_a}.npz "$IN"/
cp -n $M/M1/root/outputs/w25/feats_ut.npz "$IN"/
cp -n $HOME/vsps_w25k1/{oiv7_val,ktvic_test,openviic_test,uitviic_test,t2}.npz "$IN"/
chmod 400 "$IN"/*.npz; ( cd "$IN" && sha256sum -c "$PRE/stage.sha256" )          # 13 OK
```
- If an M1 copy does not verify, use the M3 copy of the same name (`M3/root/outputs/...`), never a different file.
- `stage.sha256`:
```
b69dac29b4dd07e759d1ff2fc38cb5d716cbe31ddb34c4233ff8f8667b8acba6  feats_nocaps_val.npz
2bc3b83ea4116603a041559d35e156f11005c44a910f29100439658593d45934  feats_coco_test.npz
9783f7a669aa1b0a6df8e8a78aa3586fb7009f376d8151442ac3acc7da580a7e  feats_coco_kval.npz
caf4a62199fccfe903e3a553a3717673d62a32ae07a2e289c2a706d70132e437  feats_memory.npz
72b1de15618c4e53ad099666257d5810f263e159e32256df2f5599297bef7a3d  c7_coco_gap_val2014.npz
95144514c601007b512528e7478140f3df9a91885ef40027dd4f6e3136a2ce80  c7_a_t3_val2017.npz
00ef39757bb11fa2ac0333ba7b5304a855f41fc91dca39ee8349c4b6337b0c94  c7_pascal50s_a.npz
17d3ebf07ebf95bcd0c8bf123ff65fb8f2df65c52cd4e17ac492e05976b98c1d  feats_ut.npz
2ca7e2f56bc3695dc4be13f10d4511881e4460d6d0815c27a6ab1220d8e7c5bb  oiv7_val.npz
cd985050fd2042b87049410334a05a6406b4363d69c05a45e6ed28ccae86702d  ktvic_test.npz
f4c79b825a1b62256dfac15b6ce59bce1054b83386ab4d5d932ac3c4e73d360e  openviic_test.npz
4f4784903fb0164309a3b1b6b3ba4fbaa9c09da6c4be5294a6c43f75581ff95f  uitviic_test.npz
98f61bae0c8e03c389db3563a5e6fbec7aa1a6f531a38d027f7c5ed54aba4268  t2.npz
```
- Staging is heavy /mnt/d reading. It must finish before P9 and never run inside the window.

### 3.3 Bytecode removal, preconditions, then the pause line (coordinator)
- **B0 (N38), before P1.** The 8 CODE-closure dirs are the dirs of the 10 paths in `c_pvr_run.py` `CODE` l.51-62
  (scripts/c_pvr among them). Remove their git-ignored bytecode, listing it first:
```
cd $R
DIRS="scripts scripts/c_pvr scripts/w25 scripts/c_stage1 scripts/c_en scripts/lb scripts/g2b scripts/grl"
for d in $DIRS; do ls -l "$d"/__pycache__ "$d"/*.pyc 2>/dev/null; done > "$PRE/bytecode_removed.txt"
for d in $DIRS; do
  if [ -d "$d/__pycache__" ]; then git check-ignore -q "$d/__pycache__" && rm -r "$d/__pycache__" || echo "NOT IGNORED: $d/__pycache__"; fi
  for f in "$d"/*.pyc; do [ -e "$f" ] && { git check-ignore -q "$f" && rm "$f" || echo "NOT IGNORED: $f"; }; done
done
```
  - Any "NOT IGNORED" line is a stop: nothing tracked is removed, and the coordinator asks for a read.
  - `bytecode_removed.txt` and its sha go into pre.txt. One LOG line `OPS-<MMDD>c-w25-bytecode` (dirs, file count,
    the list sha) is written before P1, so it lies before the pause line (Q11 C20 precedent).
  - Every later python line in this document keeps `-B`, so no bytecode is written again. P3 checks this.
- Run §5 P1-P21 in the stated order. Save the outputs to `$PRE/pre.txt` and record its sha.
- Then append the pause line (§4.1) with one `>>`. Wait at least 2 s. Write `wc -l` and `sha256sum` of `$L` into
  `$PRE/quiet_pre.txt` and check that the last line is the pause line.

### 3.4 Launch (coordinator; detached; launch guard first; pid route without `pgrep -f`)
```
cd $R
[ ! -e "$S" ] && mkdir -m 700 "$S" || { echo "LAUNCH GUARD: $S exists"; exit 1; }      # checked BEFORE mkdir (CC-243 N3, G4)
setsid -f /bin/sh -c 'echo $$ >"$1/sh.pid"; OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 "$2" -I -B scripts/c_pvr/c_pvr_run.py w25 --host laptop --run-sha "$3" --pause-tag "$4" --owners-sha "$5" --feats-sha "$6" --sscd "$7" --in "$8" >"$1/w25_stdout.txt" 2>"$1/w25_stderr.txt"; echo "rc=$? $(date -u +%FT%TZ)" >"$1/w25_rc.txt"' \
  sh "$S" "$FT" "$RUN2" '<the W25 tag>' "$OWN" "$F" "$SSCD" "$IN"
```
- **Detached** (`setsid -f`): no tool timeout or session end can signal it.
- **Pid route:** `SH=$(cat "$S/sh.pid")`; `PY=$(pgrep -P "$SH")` must give exactly one pid, the w25 python (no `-x`
  filter: comm may be `python` or `python3.12`). The `build_memory` pool workers (started by spawn) and one
  `multiprocessing` resource_tracker are children of `$PY`, never of `$SH`; all have comm python (CC-251
  worker_tree.txt). NoCaps fetches are urllib threads inside `$PY` (`stage_nocaps` l.886-902, `cen_fetch.get`
  l.236-251), not processes. curl is a child of `$PY` only during `ovqa_zip` (l.1029). Never `pgrep -f` or `pkill -f`: the coordinator's own wrapper would match.
- The concrete tag appears only on this command line (argv) and in its pause line. The 'w25 start' ACCESS_LOG row
  holds only sha256(tag). `$PY`'s own /proc cmdline carries the tag. Under spawn a worker's /proc cmdline is
  `<python> -B -I -c from multiprocessing.spawn import spawn_main; … --multiprocessing-fork`, so the tag is not in it
  (it is only in the worker's in-memory `sys.argv`; CC-251 probe). The policy stays: no evidence file prints a
  cmdline (N47).

### 3.5 Watch (ext4 and /proc only; never `~/.vsps_sealed`; no LOG line until the exit)
`$PRE/w25_watch.sh` (its sha goes in pre.txt), started right after the launch:
`setsid -f /bin/sh "$PRE/w25_watch.sh" "$S" "$(stat -c %Y "$S/sh.pid")" <AUTO> <EXP>`. On a resume, the second
argument is the **first** window's `sh.pid` mtime.
- **`EXP` (N39)** = the part lines expected in this window. First window: 24 (NoCaps test 10,496 ids = 21 batches of
  512; OpenViVQA dev 1,070 names = 3 batches; the last line is `ovqa_dev part 0002`). Resume: 24 minus the sum of the
  part-line counts in all earlier result lines (§8 step 1). It is written into pre.txt.
- **EXP check (N59).** An empty or non-numeric `EXP` makes `[ "$n" -lt "$EXP" ]` false, so the stall disarms
  silently (safe for `decide`; the wall stays). So the coordinator records in pre.txt that `EXP` is an integer 0..24,
  and checks that the first poll line of `watch.txt` reads `parts=0/<EXP> armed=1` (first window), or `armed=0` when
  `EXP = 0`. If not, the coordinator stops and restarts the watcher only, never touching `$PY`.
```sh
#!/bin/sh
# w25_watch.sh S T_FIRST AUTO EXP: writes $S/watch.txt and $S/ALERT only; never LOG.md; never ~/.vsps_sealed; never SIGKILL.
# The stall is armed only while part lines are pending (parts < EXP); decide prints nothing and is never stalled.
S=$1; T1=$2; AUTO=$3; EXP=$4
sleep 10; SH=$(cat "$S/sh.pid"); PY=$(pgrep -P "$SH")
[ "$(echo $PY | wc -w)" = 1 ] || { echo "$(date -u +%FT%TZ) pid route gave '$PY'" >> "$S/ALERT"; exit 1; }
echo "$(date -u +%FT%TZ) py=$PY env_threads1=$(tr '\0' '\n' < /proc/$PY/environ | grep -cE '^(OMP|MKL)_NUM_THREADS=1$')" >> "$S/watch.txt"
cpu() { t=0; for p in $PY $(pgrep -P "$PY"); do
  t=$((t + $(sed 's/^.*) //' "/proc/$p/stat" 2>/dev/null | awk '{s = $12 + $13} END {print s + 0}'))); done; echo "$t"; }
n0=-1; last=$(date +%s); sent=0; e2=0
while [ ! -e "$S/w25_rc.txt" ]; do
  now=$(date +%s); n=$(grep -c ' part ' "$S/w25_stdout.txt" 2>/dev/null); n=${n:-0}
  [ "$n" -ne "$n0" ] && { n0=$n; last=$now; }
  st=$(sed 's/^.*) //' "/proc/$PY/stat" 2>/dev/null | cut -d' ' -f1)
  armed=0; [ "$n" -lt "$EXP" ] && armed=1
  echo "$(date -u +%FT%TZ) parts=$n/$EXP armed=$armed py=${st:-gone} cpu=$(cpu) curl=$(pgrep -c -P "$PY" curl) kids=$(pgrep -c -P "$PY") shm=$(ls /dev/shm/c_pvr_w25 2>/dev/null | wc -l)" >> "$S/watch.txt"
  why=""
  [ "$armed" = 1 ] && [ $((now - last)) -ge 3600 ] && why="E1 stall: no new part line for 60 min"
  [ "$now" -ge $((T1 + 86400 + 5400)) ] && why="E1 wall: 24 h + 90 min after the first launch"
  if [ -n "$why" ] && [ -n "$st" ] && [ "$st" != Z ]; then
    if [ "$sent" = 0 ]; then
      sent=$now; echo "$(date -u +%FT%TZ) $why" >> "$S/ALERT"
      if [ "$AUTO" = 1 ]; then kill -TERM "$PY" && echo "$(date -u +%FT%TZ) SIGTERM to $PY" >> "$S/ALERT"; fi
    elif [ "$AUTO" = 1 ] && [ "$e2" = 0 ] && [ $((now - sent)) -ge 600 ]; then
      e2=1; echo "$(date -u +%FT%TZ) E2: alive 10 min after SIGTERM; no further signal (§6A)" >> "$S/ALERT"
    fi
  fi
  sleep 300
done
```
- **What it reads:**
  - the count of `"<set> part NNNN"` lines in `$S/w25_stdout.txt`. `run_set` prints one per finished part with
    `flush=True` (c_pvr_run.py l.1003). Finished parts skipped on a resume print nothing, so the count is per window;
  - `/proc/$PY/stat` (state; fields 14-15 utime+stime, summed with its direct children; CLK_TCK = 100);
  - `/proc/$PY/environ`, once, for the N22 run record (count only; expected 2);
  - the number of curl children (non-zero only during `ovqa_zip`; NoCaps fetches are urllib threads, N41) and of all
    children of `$PY`; the entry count of `/dev/shm/c_pvr_w25` (no file read).
  - **Tracker (N54):** `kids=` counts the resource_tracker plus the live pool workers, and `cpu()` sums the tracker
    too (negligible). So `kids=1` between batches is the tracker, not a stuck worker. The watcher text is unchanged.
- **Phase rule (N39).** The stall is armed only while `parts < EXP`. After the last part line of this window, the
  process runs `decide` (the one look) and prints nothing until it exits, so no stall SIGTERM can reach it there. If
  `EXP = 0` (a resume with every part done), the stall is off from the start. The wall stays armed in every phase.
  The same rule binds the coordinator under `AUTO=0`: no stall SIGTERM once `parts ≥ EXP`.
  - Decide estimate: W25-K1 decide took 57 s CPU on about 7.8e8 query-owner pairs (LOG l.939). Here (10,496 + 1,070
    queries × 118,957 owner rows, CC-250) about 1.4e9 pairs: a few minutes. The wall (24 h + 90 min) leaves at least
    about 1 h after the code's own 24 h `Stop`, which is checked before every batch.
  - ovqa_zip margin: between `nocaps_test part 0020` and `ovqa_dev part 0000` the process downloads dev-images.zip
    (165,039,269 B) and runs `ovqa_count`, with no part line. This must fit inside the armed 60 min; at the
    P15-checked network it takes minutes. If it does not, E1 fires as for any stall.
- The stall and wall clocks come from the watcher's own time and the `sh.pid` mtime, never from an ACCESS_LOG stamp
  field (G5) and never from the sealed `deadline` file.
- `AUTO=1`: the watcher sends the single E1 SIGTERM itself. `AUTO=0`: it only writes `ALERT`, and the coordinator
  sends the SIGTERM by hand and appends its time to `ALERT`. Ruling W-R4. **Default: `AUTO=0`.**
- The watcher's argv ends in `w25_watch.sh`, not `_job.sh`, so `foreign_jobs` does not count it. It is disclosed as a
  non-job process beside `d_watch`.

### 3.6 After the exit (coordinator; `w25_rc.txt` exists, or §6A step 2 ended the process)
```
cd $R
ls /dev/shm/c_pvr_w25 2>/dev/null && echo RESIDUE                         # must print nothing
{ wc -l $L; sha256sum $L; } > "$S/quiet_post.txt"                          # = quiet_pre (§4.3)
cut -f3 $HOME/.vsps_sealed/c_pvr/ACCESS_LOG.tsv | grep -n '^w25 '          # action field only (§9.3 of Q11 v1.2)
cut -f3 $HOME/.vsps_sealed/c_pvr/ACCESS_LOG.tsv | grep -c '^ovqa-pin'      # identity (c) row(s)
tail -n 3 $HOME/.vsps_sealed/c_pvr/w25_deletions.log                        # trap line last (absent after a WSL restart, §6A)
sha256sum manuscript/prereg/2026-11-02_c_pvr_tier1/{w25_counts.json,w25_flagged_ids.txt,w25_lost_ids.txt,w25_ovqa_out_ids.txt,w25_f30k_join_ids.txt}
sha256sum $FT "$(readlink -f /usr/bin/python3)" /usr/bin/curl            # = P10 values
sha256sum "$S"/{watch.txt,ALERT,hang.txt,pi_e2.txt} 2>/dev/null           # the files that exist
ls /dev/shm | grep -c '^sem\.mp-'                                           # count only; nothing removed (N48)
/usr/bin/python3 -I -B -c 'import ast,hashlib; t=open("scripts/c_pvr/c_pvr_run.py","rb").read(); assert hashlib.sha256(t).hexdigest()=="290a75dc414df655d4bdb5f2f18947b3885305673f647bc6d4c6556d0087a352"; c=next(ast.literal_eval(n.value) for n in ast.parse(t).body if isinstance(n,ast.Assign) and getattr(n.targets[0],"id","")=="CODE"); print("CODE re-hash", len(c), "bad", [p for p,h in c.items() if hashlib.sha256(open(p,"rb").read()).hexdigest()!=h])'   # N53: prints "CODE re-hash 10 bad []"
```
- **Code re-hash (N53).** Spawned children re-read `c_pvr_run.py` (as `__mp_main__`) and `match_openviic.py` from disk
  at each of the 24 Pool openings, after the parent's single `CODE` check. So after the exit the coordinator re-hashes
  `c_pvr_run.py` (= 290a75dc) and the 10 `CODE` files (parsed from the file, never imported), and the result line
  records that they equal the launch pins. Any mismatch (or a failed assert) sends the run to a one-judge read before
  any output is used.
Then the result line, then the resume line (§4.2), then §7 or §8. These declared reads (one known ACCESS_LOG file by
`cut`, the deletions-log tail) are the only sealed touches in this document (W-R4).

## 4. Pause tag, pause line and the LOG quiet rule

### 4.1 Tag and line
- **The W25 tag = `OPS-<MMDD>c-w25pause`** (`<MMDD>` = the `date -u` month-day of the pause line). It must fullmatch
  `OPS-[0-9A-Za-z][0-9A-Za-z-]*`. A retry or resume uses `OPS-<MMDD>c-w25pause2` (then `…3`) and a fresh
  `S=$HOME/w25run_<MMDD>_2` (G4).
- **`pause_w25` predicate (c_pvr_run.py, checked before the window and before every batch):**
  - the tag is a whole token in **exactly one** LOG line;
  - that line starts with a `date -u` stamp earlier than the process start `T0`;
  - the line holds a standalone uppercase `W25`: `(?<![\w-])W25(?![\w-])`. `W25-K1` does not count, and neither does
    the lowercase `w25` inside the tag;
  - the line holds a separate word starting `pause`: `(?i)\bpause`. The tag does not satisfy it, because `pause`
    follows `5` inside `w25pause`.
- **Pause line** (one line, one `>>`, stamp from `$(date -u +%FT%TZ)` once):
```
$(date -u +%FT%TZ) <the W25 tag>: C pixel W25 pause window opens per <CC id of the R2 GO>, CC-251 and <PI id of the window line>: from this line until c_pvr_run.py w25 exits, every LOG.md writer and every other paper's laptop job is paused (§4 of W25_RUN_DOC_v1_4 <sha8>); HEAD <git rev-parse HEAD>, c_pvr_run.py 290a75dc (spawn), owners 0cf330d3, owner-feats manifest 8f707edd, lists edb07fbb; preconditions §5 all PASS (<pre.txt sha8>); hang plan §6A (PQ5 = C done; A then B backstop; PQ5b <answer>); no other LOG line until the exit.
```
- P14 tests this exact string against the three regexes before it is appended.
- **Tag hygiene (binding):** only the generic form `OPS-<MMDD>c-w25pause`, with the literal `<MMDD>`, may appear in a
  CC file, a LOG line other than the pause line, an evidence file or a commit message. The post-run lines use
  `OPS-<MMDD>c-w25-result` and `OPS-<MMDD>c-w25-resume` (different tokens).
- A second whole-token hit, a LOG read error (9p EIO) or a torn UTF-8 append aborts the window at the next batch
  (`guard` → FAULT; the trap deletes tmpfs; the parts are kept).

### 4.2 The LOG quiet rule: the G-B rule, by default (CC-245 Ruling 3, N7)
- **Rule.** From the pause line until the result line, **nobody appends to LOG.md**. The first line after the pause
  line is `OPS-<MMDD>c-w25-result`, then at once `OPS-<MMDD>c-w25-resume`, which ends the pause.
- **Why.** `w25` re-reads LOG.md (strict UTF-8) before every batch (CC-245 Ruling 3). A torn append, an EIO or a
  second tag line ends the window.
- **Writers** are W-a..W-k of Q11 v1.2 §4.1, unchanged:
  - W-a coordinator: the pause line, then nothing until the exit;
  - W-b judges and panels: none run;
  - W-c workflows: none run;
  - W-d per-tick writers: no `/loop` tick;
  - W-e Gemini and W-f the other tool: closed by the PI (PQ3);
  - W-g other papers' jobs: none;
  - W-h `gpu_backup` loops: not started until the resume line, **also not after a WSL restart** (§6A);
  - W-i `d_watch`: keep running (disclosed); after a WSL restart it is restarted (it writes only its own log);
  - W-j hooks and MCP: no Edit/Write in the window;
  - W-k background agents: none live; each finishes and logs before P9.
  - Added: the §3.5 watcher writes only `$S`; the PI's E2 answer goes to `$S/pi_e2.txt`, not LOG.md (§6A).
- The relaxed form of v0 §5.3 is **not proposed** (CC-245 N7).
- **Worst case:** the window ends by itself at the 24 h stop, so LOG.md can stay quiet for about 24 h. On a hang it
  stays quiet until the PI acts (G10; §6A).

### 4.3 Proof the rule held
`$PRE/quiet_pre.txt` (right after the pause line) and `$S/quiet_post.txt` (right after the exit, before any new line)
must hold equal `wc -l` and sha256 values. The result line cites both.

## 5. Preconditions (coordinator; one pass right before the pause line; G-B C1-C20 style; any FAIL = no pause line)

Order: P16 (PI line) and P17 (usage) first; P4 then P21; P9 within 5 min before the pause line; P14 last.

| # | precondition | how | PASS | G-B source |
|---|---|---|---|---|
| P1 | code pins | `sha256sum scripts/c_pvr/{c_pvr.py,gates.py,c_pvr_run.py}` and `git show HEAD:<path> \| sha256sum` | 8f10bd60…, 3bced05e…, 290a75dc…, equal on disk and at HEAD | C1 |
| P2 | SUMS | `timeout 120 sha256sum -c scripts/c_pvr/SHA256SUMS` from the repo root | 18 OK, rc 0 | C4 |
| P3 | clean tree, no bytecode | `git status --porcelain --ignored scripts/c_pvr data/splits/textcaps_train_ids.txt`; `for d in $DIRS; do find "$d" -maxdepth 1 \( -name __pycache__ -o -name '*.pyc' \); done` over the 8 CODE-closure dirs of B0 (§3.3). Run after B0, and again right before P14 | both empty, both times | C2, C20, N38 |
| P4 | selftests, **one at a time, never in parallel** | in the CC-245r3 sandbox form (harness l.288-290: `env -i …` then `unshare -rnm`, tmpfs on /dev/shm and over `~/.vsps_sealed`, cwd and TMPDIR on ext4 scratch). Each line is `timeout -k 10 120 env -i … OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 … <python> -I -B <script> selftest` (the two assignments come **after** `-i`): `$CV … $R/scripts/c_pvr/c_pvr.py selftest` once; `$FT … $R/scripts/c_pvr/c_pvr_run.py selftest` twice | "selftest ok … 8f10bd60"; "selftest ok … 290a75dc" twice; each < 120 s (N8). A solo `c_pvr_run.py` selftest takes about 31 s under spawn (was 9-17 s; LOG l.1481), still under the 120 s timeout. A timeout is a FAIL and N28 evidence: the PI is told before any window (§6A) | v0 P3/P4 |
| P5 | the sha diff that lets W25 run at RUN' | `git diff --stat 155b6c01 HEAD -- scripts/c_pvr` | exactly `c_pvr_run.py`, `c_pvr_run_mutants.py`, `SHA256SUMS`; 3 files, 25 insertions / 10 deletions (= `155b6c01 ab1dd77`, §1, N49) | C5 |
| P6 | GOs and commits in force | the R2 GO (CC id) of this file, not revoked; CC-248 GO 91 and commit 3c1ee0e; CC-249 GO 93; CC-251 GO 90 and commit ab1dd77; this file committed byte-equal to the GO'd sha (W-R5) | all | C6 |
| P7 | frozen inputs (N32) | `sha256sum manuscript/prereg/2026-11-02_c_pvr_tier1/{c_pvr_owners.json,c_pvr_owner_feats.json,c_pvr_lists.json}` = `$OWN`, `$F`, `$LISTS`; `grep -c` in `$L` finds the lines OPS-1103c-owners (l.1449), OPS-1103c-owner-feats, OPS-1104c-lists and the CC-249 GO line (each ≥ 1); `head -c 4 ~/c_pvr_of_run/rc.txt` = `rc=0`; `cut -f3 ~/.vsps_sealed/c_pvr/ACCESS_LOG.tsv` then `grep -c '^owner-feats write'` = 6, `grep -c '^owner-feats manifest'` = 1, `grep -c 'lists write'` = 1 (cut only; no ls of the sealed dir). No file-mode check of the jsons (DrvFs shows r-xr-xr-x; the sha is the check) | all | — |
| P8 | staged caches | `( cd $IN && sha256sum -c $PRE/stage.sha256 )` 13 OK; `ls $IN/of_*.npz \| wc -l` = 6; `stat -c '%a' $IN` = 700; `df -T $IN` = ext4 | all | v0 P5 |
| P9 | /mnt/d health (C8) | (a) `mount \| grep ' /mnt/d '` = 9p; (b) `~/.local/state/vsps/d_watch.log` absent, or no FAIL after the last RECOVERED, and `d_watch.sh` live; (c) the pinned `write_new` probe of LOG l.1405 in a fresh `.session_backup/w25_probe` absent beforehand (G6), probe text and sha in pre.txt; (d) = P2 | all, within 5 min before the pause line; any FAIL → no window, PI asked | C7, C8 |
| P10 | toolchain | `sha256sum $FT` (resolved), `/usr/bin/curl` = 1ccbd3da…, `readlink -f /usr/bin/python3` = e50d468e…; `$FT -m pip freeze \| sha256sum` = 1a639a50…; `$FT -m pip check` OK; SSCD sha = 9f26bd4c…; `systemctl list-timers 'apt-daily*' --all` (live reading governs, G8): neither due within 6 h + 90 min; `systemctl is-active apt-daily.service apt-daily-upgrade.service` = inactive for both | equal; not due; inactive | C3, G8 |
| P11 | no heavy I/O, no other job | `ps -eo pid,etime,args`: no rsync, mutants, LaTeX/pandoc, `git gc`, B/MT4/VSPS-J job, background agent, workflow or agent bash loop (other than `d_watch`); no `multiprocessing.spawn` worker or `multiprocessing.resource_tracker` process (N52); no `gpu_backup` loop; `/proc/*/cmdline` has no argument ending `_job.sh` | none | C9, C11, C16, C17 |
| P12a | no W25 residue, **first window** | `/dev/shm/c_pvr_w25` absent; `/dev/shm/c_pvr_w25.lock` absent, or `flock -n /dev/shm/c_pvr_w25.lock true` rc 0; the 5 outputs absent under `manuscript/prereg/2026-11-02_c_pvr_tier1/`; `cut -f3 ~/.vsps_sealed/c_pvr/ACCESS_LOG.tsv \| grep -c '^w25 '` = 0; `ls /dev/shm \| grep -c '^sem\.mp-'` recorded in pre.txt (record only, not residue, nothing removed; N48) | as stated | C10 |
| P12b | no W25 residue, **resume window** (C1) | `/dev/shm/c_pvr_w25` absent (or removed by hand under §7 with its two records); lock as P12a; the 5 outputs absent; on `cut -f3 … ACCESS_LOG.tsv`: `grep -c '^w25 decide'` = 0, `grep -c '^w25 end'` = 0, `grep -c '^w25 start'` = the number of earlier windows named in earlier result lines; `grep '^w25 ' \| tail -n 1` equals the last action the previous result line names; `tail -c 1 ~/.vsps_sealed/c_pvr/ACCESS_LOG.tsv \| od -An -c` = `\n` (one byte of the declared file; N43). A torn last row (no final LF) is not repaired by hand: it goes to the one-judge read of the cause (CC-242r2 G3 torn-row clause); the one-judge read GO on the cause is cited; `ls /dev/shm \| grep -c '^sem\.mp-'` recorded in pre.txt (record only, nothing removed; N48) | as stated | C10, G3, G4 |
| P13 | tenancy inputs | `grep -c /dev/shm ~/.config/vsps/gpu_backup.sh` = 0 and the file exists | as stated | C11 |
| P14 | LOG and tag | LOG.md decodes strict UTF-8 and ends with `\n`; the concrete tag has 0 whole-token hits (`pause_w25` regex); the drafted pause line passes the three §4.1 regexes (tested in memory, not in LOG) | as stated | C12, C13 |
| P15 | network reachable without content (C4) | `ID=$(LC_ALL=C sort manuscript/prereg/2026-11-02_c_pvr_tier1/ga_remaining_ids.txt \| head -n 1)`; `U=$(/usr/bin/python3 -I -B -c 'import sys; sys.path.insert(0, "scripts/c_pvr"); import c_pvr; print(c_pvr.OI_TEST_URL.format(file=sys.argv[1] + ".jpg"))' "$ID")`; `env -i PATH=/usr/bin:/bin /usr/bin/curl -q -sS -I --fail --proto =https -o /dev/null -w '%{http_code} %{content_type} %{num_redirects}\n' "$U"`. **No `-L`**: the W25 fetch FAULTs on a redirect (`FAULT_ERR` l.74). P15 probes with curl; the window fetches NoCaps with urllib (`cen_fetch.get` l.236-251, which returns "redirected" when the final URL differs). The PASS rule (200, no redirect) matches that FAULT (N41) | prints `200 image/jpeg 0`. rc 0 alone is not a PASS; a 3xx is a FAIL | v0 P13 |
| P16 | PI window line | a PI-<id> LOG line from the PI's chat answers PQ1-PQ4 and PQ5b (PQ5 = C and PQ7 = YES are on record in PI-1104c; PQ6 if asked), written before P9 | present; cited in the pause line | C15, C18 |
| P17 | usage (G7, fails closed) | `~/.config/vsps/usage_check.sh` twice, 10 min apart, each with data age ≤ 120 s and numeric fields: 5-hour ≥ 15% and 7-day ≥ 10% remaining, ≥ 90 min headroom at the measured rate, no 5-hour reset inside the launch phase. If five_hour reads None: PQ7 = YES (PI-1104c), so it passes on 7-day ≥ 10% plus the P16 PI line. The usage guard writes nothing to LOG.md in the window | as stated | C19, G7 |
| P18 | staging and watcher text | `$PRE/stage.sha256` and `$PRE/w25_watch.sh` byte-equal to §3.2 / §3.5; their shas in pre.txt | equal | — |
| P19 | `$S` absent | `[ ! -e "$S" ]` | absent | Q11 v1.2 §2.1 |
| P20 | the RESUME note | `$PRE/RESUME.txt` names: the window state, `$S`, the E-step reached, the PQ5 option, "the pause stays open until the result line" (G10), and "after a WSL restart: no `gpu_backup` loop, no LOG writer, no `/loop` tick until the resume line" | written | G10 |
| P21 | no orphaned c_pvr or mutant process (C7, CC-247 N25) | after P4: `pgrep -a python` and `ps -eo pid,ppid,etime,args` show no `c_pvr_run.py`, `c_pvr.py`, `c_pvr_run_mutants.py`, `c_run_mut_scratch`, `multiprocessing.spawn` or `multiprocessing.resource_tracker` process (N52: a stale spawn worker or tracker from a timed-out P4 selftest carries no c_pvr name, and the sandbox has no pid namespace; the coordinator's own grep excluded) | none. If any: record PID, `/proc/<pid>/wchan`, elapsed in pre.txt; SIGTERM by PID; SIGKILL by PID after 10 s for a survivor. This is allowed only for stale selftest, mutant, spawn-worker or tracker PIDs and only **before** the pause line (CC-247 N25, CC-251 N52). Before signalling a spawn worker or tracker, record its ppid; signal it only if ppid = 1 (orphaned) or ppid = a P4 selftest PID recorded in pre.txt. An unrelated multiprocessing process is never signalled (N60). Then re-run P11 and P21 | CC-247 N25 |

## 6. Stall, wall and end-state ladder (no SIGKILL by any agent; clocks from `sh.pid` mtime and watcher time, G5)

| step | when | who | action | then |
|---|---|---|---|---|
| E1 stall | no new part line for **60 min** (a 512-image batch takes about 4-15 min), **armed only while `parts < EXP`** (§3.5 phase rule, N39); never during `decide` | watcher (`AUTO=1`) or coordinator (`AUTO=0`) | **one SIGTERM to `$PY`** | `sig_handler` → `SystemExit` in the main process; `Pool.__exit__` terminates the workers; the `finally` deletes `/dev/shm/c_pvr_w25` (logged) and writes 'w25 abort'; parts kept → §7 |
| E1 wall | `$PY` alive at first-launch `sh.pid` mtime + 24 h + 90 min | as E1 stall | the same single SIGTERM | the code's own 24 h `Stop` fires at the next batch boundary, so reaching this means a hang |
| E2 | `$PY` alive (state not Z) at the first poll ≥ 10 min after the SIGTERM | coordinator | §6A steps H1-H4: `hang.txt`, P9(a)/(c) under `timeout 20`, the PQ5 request to the PI in chat. **No further signal by any agent** | the pause stays open until the PI acts (G10) |
| E3 | the PI acts per the PQ5 answer | PI | §6A step 1 and/or step 2 | → E4 |
| E4 | `$PY` has exited | coordinator | §3.6, then the result line, then the resume line | §7 or §8 |

- **Pre-start window.** Before the 'w25 start' row the handlers are not installed. A SIGTERM there kills with the
  default action. `w25_pre` has no `Pool` (it loads caches), so the fork hang of §6A cannot occur there. In the
  microseconds between `mkdir /dev/shm/c_pvr_w25` and the handler install, it would leave an **empty** dir, removed by
  hand under §7. This differs from G2 on purpose: G2 guards a half-written `gb_start` marker that would consume the
  run; `w25` has no such marker (its 'w25 start' row is written after the handlers are installed).
- **Disclosed:** E1 can end a batch that is still making progress (G5).

## 6A. N28 freeze plan (CC-248 N28 (i)-(iii); BLOCKING for the R2 GO)

**(i) The risk, stated (N50).** The intermittent hang seen under 3 parallel selftests recurs with OMP/MKL = 1 (CC-248
Ruling 4). Its cause is open ("consistent with fork-after-threads", CC-247). `build_memory.features` opens `Pool(4)`
after `torch.jit.load` (l.168-176).
- **PQ5 = C is DONE** (PI-1104c; CC-251 GO 90; commit ab1dd77). `main()` sets `multiprocessing.set_start_method("spawn")`
  as its first statement (l.2072), before `load()` and before every subcommand. The only process pool in the code
  closure is `build_memory.features`, so every Pool on the owner-feats and w25 paths starts its workers by fork+exec.
  No Python code runs in a forked copy of the threaded parent. **This removes the suspected fork-after-threads path by
  construction.**
- **It is not shown to remove the hang.** The stress test (6 rounds × 3 parallel sandbox selftests) gave 0/18 hangs
  at the old sha 4af623d0 and 0/18 at 290a75dc. It never failed at the old sha either, so it does not discriminate. A hang
  in the window stays possible, and its rate stays unmeasured. **A, then B, stay the backstop at E2** (PI-1104c).
- **How a hang can still happen under spawn (N58).** Spawn workers have no Python SIGTERM handler: `SIGTERM` is
  `SIG_DFL` in them (CC-250r2 probe). So on the single SIGTERM the main process raises `SystemExit`, and
  `Pool.__exit__` → `terminate()` sends SIGTERM to the workers, which ends a worker in an interruptible wait. The
  teardown can still hang by three routes:
  - a worker in D-state (uninterruptible I/O);
  - the pool lock: `_help_stuff_finish` takes `inqueue._rlock`, which a killed worker may hold;
  - the main thread itself blocked in a C call (SSCD/torch runs in the parent, build_memory l.168-192), where its
    Python SIGTERM handler never runs.
  Then the `finally` never runs and no 'w25 abort' row is written. That lands in the §7 row "'w25 start' and no end or
  abort row", not the ABORT row. In the third route, A's step 1 (killing workers) does not help, and step 2 (B, WSL
  restart) applies after 10 min. No command changes.
- **Evidence, stated plainly (N40, CC-250 Ruling 5).**
  - `featurize` (l.914) calls `build_memory.features` once per batch, and each call opens one `Pool(4)`. A first
    window opens **24** `Pool(4)` (21 NoCaps-test + 3 OpenViVQA-dev batches; 96 worker starts, now by spawn).
    owner-feats opened **6** (one per compute owner; 24 workers, under fork) and had no hang (LOG l.1461). That covers
    about a quarter of the openings.
  - The hangs seen so far ran with **`Pool(1)`**: the selftest fixtures use `workers = 1` (l.1541, l.1570, l.1653),
    and the hangs appeared only with 3 selftests in parallel (r3, r4), all under fork.
  - **The hang rate for 24 solo `Pool(4)` openings is unmeasured.** It is plausibly small, but no number is claimed.
    A freeze is possible; we have not shown it is rare in this long run.
  - The window runs alone (P11, P21).
- **Why spawn, not forkserver** (CC-251 Option 3): with forkserver the workers are children of the server process,
  not of `$PY`. That would break the ppid = `$PY` test of the H4 kill line and the `pgrep -P $PY` counts. Spawn keeps
  the workers and the resource_tracker as direct children of `$PY` (CC-251 worker_tree.txt: same pgid and sid, comm
  python).
- **Feature equality, and its scope (N51).** 64 dev images (the first 32 ids of `ktvic_dev299` and of
  `openviic_dev_c1`) went through `build_memory.features` with `workers = 4` under spawn and OMP/MKL = 1. sha, pHash,
  dHash, both mirrored hashes and SSCD were bit-identical to the laptop caches be2b121b and cfbf24f9 (LOG l.1481). That
  covers **2 of the 19** cached feature files (2 of the 6 owner-feats caches made on this laptop).
  - **All 19 files (N57):**
    - 2 checked: `ktvic_dev299` be2b121b, `openviic_dev_c1` cfbf24f9;
    - `vitextvqa_dev` fe258106: optional check (dev), below;
    - `xm3600_all` 10de1a60: never re-run (XM3600 holds the one-look XM-test2500);
    - `h_bdt1_739` 10a49f17 and `refused_ktvic_dup` be9aebfb: not rechecked (KTVIC images);
    - the 13 staged caches: 8 are copied from rented-machine backups (§3.2 M1 paths); 5 sit in the laptop W25-K1
      folder `~/vsps_w25k1`, and 4 of them (ktvic_test, openviic_test, uitviic_test, t2) were computed there, under
      fork (LOG l.911, l.938); oiv7_val's origin is not established and is not claimed. All 13 are only read, by sha
      (§3.2, P8). A start-method change in this process cannot alter them. Their comparability rests on the earlier
      rulings (CC-242r2, CC-245r3).
  - At least 4 of the 13 are test-set files: feats_coco_test (Karpathy test), ktvic_test, openviic_test,
    uitviic_test. They are not recomputed. (This narrows CC-251's wording, as CC-250r2 Ruling 6 rules.)
  - **Optional ViTextVQA dev check (N64; binding only if the PI picks it in PQ5b).**
    - Scope: 32 ids from `vitextvqa_dev` (the first 32 in owner order, the feq.py form of CC-251), on this laptop.
      Dev only; never `xm3600_all` or any test-set owner.
    - Setup: `workers = 4`, spawn, OMP/MKL = 1, `cache = None`; compared with `of_vitextvqa_dev.npz` fe258106
      loaded at its manifest sha.
    - PASS = sha, pHash, dHash, both mirrored hashes and SSCD bit-identical for all 32. Any difference or error = no
      window, and a one-judge read.
    - Timing: before P1 and before P11/P21, never in the window. Cap: CPU only, 15 min wall; a time-out is a FAIL.
    - Records: the output and its sha go into pre.txt, with one LOG line before the pause line.
  - The PI rules on this scope in **PQ5b**.
- **Records (N55, N56).** `no_sockets()` (l.802) does not reach spawned workers; they hash local files only. The worker
  branch of `sig_handler` (l.1107) is now dead code for workers; it stays as it is, held with N29 (same-sha rule). The
  W25 flock (l.1143) is no longer inherited by workers, so an orphaned worker cannot hold the lock. feq.py and the
  st_one.py/stress.sh harness stay in `.session_backup/2026-11-04/c_run/r5/` only; they are not committed or pinned.
  Lesson: a hang-fix test must be able to fail at the old sha before it counts as evidence.

**(ii) Detection (watcher clock; ext4 and /proc only).**
- **H1 stall:** no new `"<set> part NNNN"` line in `$S/w25_stdout.txt` for 60 min (12 polls at 300 s). This is the E1
  trigger, armed only while `parts < EXP` (§3.5 phase rule, N39), so never during `decide`. One SIGTERM, then wait.
- **H2 ignored SIGTERM:** `/proc/$PY/stat` still readable with state not Z at the first poll ≥ 10 min after the
  SIGTERM. This is E2. **A hang = H1 + H2.**
- **H3 classification** (recorded, not a trigger), from the last 4 `watch.txt` lines (15 min at 300 s polls; N44):
  - *frozen*: `cpu` rose by < 100 ticks (< 1 CPU-s at CLK_TCK 100). It rests on CPU ticks only (N41). A
    featurizing batch burns well over that per 15 min. **Disclosure:** in the NoCaps fetch phase the fetchers are urllib
    threads inside `$PY`, so a long network wait also shows flat CPU; there H3 cannot tell a network wait from a
    freeze. H3 is a record only and never triggers anything;
  - *D-state*: any thread of `$PY` or its children in state D (`hang.txt`);
  - *busy*: otherwise (slow, not frozen).

**(iii) Who acts and what is logged.**
- **H4, coordinator, at E2:**
  1. writes `$S/hang.txt`:
     `{ date -u +%FT%TZ; for p in $PY $(pgrep -P $PY); do l=main; [ "$p" = "$PY" ] || { l=other; case "$(cat /proc/$p/comm)" in python*) l=tracker; grep -qaF spawn_main /proc/$p/cmdline && l=worker;; esac; }; echo "== $p $(cat /proc/$p/comm) $l"; for t in /proc/$p/task/*; do echo "$t $(sed 's/^.*) //' $t/stat | cut -d' ' -f1,12,13) $(cat $t/wchan)"; done; done; tail -n 4 $S/watch.txt; free -m; echo "sem.mp $(ls /dev/shm | grep -c '^sem\.mp-')"; } > $S/hang.txt 2>&1`
     (comm and a label only; no cmdline is printed. The `grep -qaF` is quiet and runs on children only, never on
     `$PY`'s own cmdline, which carries the tag. Label: `worker` = comm python with `spawn_main` in its cmdline;
     `tracker` = comm python without it, the one resource_tracker; `other` = e.g. curl during `ovqa_zip`; N47);
  2. runs P9(a) and P9(c) under `timeout 20`, output appended to `hang.txt`;
  3. writes into `hang.txt` the backstop action lines for the PI: for step 1, one shell line per `worker` PID; never
     `$PY`, never the resource_tracker, never curl. Each line re-checks, at the moment the PI runs it (hours may
     pass, N42), all of: ppid = `$PY`; comm python*; `spawn_main` in the child's own cmdline (a quiet fixed-string
     test, not a process pattern match; it excludes the tracker, N47). No `pkill`, no `-f`:
     `p=<pid>; [ "$(ps -o ppid= -p $p | tr -d ' ')" = "<PY>" ] && case "$(cat /proc/$p/comm)" in python*) grep -qaF spawn_main /proc/$p/cmdline && kill -KILL $p;; esac`
     Sparing the tracker keeps the normal clean-up of the `sem.mp-*` names when `$PY` then exits.
  4. asks the PI in chat, in plain words, with the H3 class and the prepared lines;
  5. writes the PI's answer verbatim, with its time, to `$S/pi_e2.txt`. **Nothing goes to LOG.md.**
- **The PI** performs the backstop action: A step 1, then B if needed (below). No agent sends SIGKILL and no agent runs
  `wsl --shutdown`.
- **After the exit** the result line records: the E-step reached, H3 class, the end route (ended by itself after the
  SIGTERM / PI step 1 kill of PIDs … / PI step 2 WSL restart), the shas of `watch.txt`, `ALERT`, `hang.txt` and
  `pi_e2.txt`, the ACCESS_LOG action mirror, the deletions-log tail (or "no trap line: WSL restart"), quiet_pre/post,
  the `sem.mp-*` count and the N53 code re-hash.

**Partial parts.**
- A finished part is whole: `gates.write_new` writes a tmp, fsyncs, then `os.link`s. A part is complete or absent.
- A kill or a WSL restart during a write can leave one `.<part>.<pid>.tmp` in the sealed parts dir. It is never read as
  a part (`run_set` looks only for `<set>_NNNN.npz`). Nobody lists the dir to look for it. It stays, and the result
  line discloses "a stray tmp is possible".
- The batch in flight is lost from tmpfs and is fetched again on the resume: at most 512 NoCaps-test images are fetched
  twice. No pixel of a finished part is fetched again.
- After a WSL restart, `/dev/shm/c_pvr_w25` and its lock are gone with the VM, so no tmpfs residue needs removal.
- **`sem.mp-*` (N48).** While a Pool is open, multiprocessing keeps `sem.mp-*` names in /dev/shm (6 per open Pool in
  the CC-251 probe). A normal exit removes them. A SIGKILL of `$PY`, a killed tracker or a WSL restart can leave them
  (a WSL restart clears /dev/shm). They are not W25 residue: `w25_pre` and `tenancy` ignore them. The coordinator
  records the count only (`ls /dev/shm | grep -c '^sem\.mp-'`) in pre.txt, `hang.txt` and the result line. Nothing is
  removed by hand.

**Resume, or a new run.**
- **A resume is the same run:** the same RUN', `$OWN`, `$F`, `$IN`, parts and deadline; a fresh tag and fresh `$S`;
  P1-P21 with **P12b**; after a one-judge read (85) of `watch.txt`, `ALERT`, `hang.txt` and `pi_e2.txt`.
- **The 24 h deadline keeps running** during the hang and the wait (fixed at the first start, l.1045, never reset).
  Example: launch 22:00 VN; last part 03:00; H1 at 04:00; E2 by 04:15; PI acts about 07:00; read and P1-P21 by about
  09:00; 13 h left against 1.5-5.5 h of total work. It fits. If the PI acts after the deadline, the resume `Stop`s at
  its first guard → PQ6.
- **A second hang of the same class** goes to the PI. C is already in place; any further code change is a new run
  (below).
- **A new run** is any change of `c_pvr_run.py` (or a module it pins) after the first launch. `read_part` refuses every
  old part (run sha), so every pixel is fetched again, and the sealed `w25` dir (parts, `deadline`) needs its own
  ruling before anything reuses or sets it aside (precedent: CC-242r2 G3(b), marker removal by its own ruling). It
  needs a full panel at 85 and a new run-document version. Nothing of it is planned now.

**PQ5 status and the backstop (PI-1104c).**

| route | what happens | for | against |
|---|---|---|---|
| **C: DONE before any launch** | spawn start method in `main` (l.2072), commit ab1dd77, CC-251 GO 90 | removes the fork-after-threads path by construction; features bit-identical on 64 dev images | not shown to remove the hang (the stress test does not discriminate); equality covers 2 of 19 files (PQ5b) |
| **A: backstop, first** (at E2) | step 1: the PI runs the prepared per-PID lines in his own WSL terminal (workers only; never `$PY`, never the tracker). If `$PY` exits within 10 min, the main process runs its `finally` (tmpfs deleted and logged, 'w25 abort' row) → the ABORT branch. Step 2, if `$PY` is still alive 10 min after step 1, or H3 says D-state: the PI runs `wsl --shutdown` in Windows and reopens WSL; the coordinator restarts from `$PRE/RESUME.txt` | no new sha; the common case keeps the clean abort row; works for D-state through step 2 | needs the PI at the keyboard; the pause stays open until then (G10); a worker kill may not free the main if it waits on a pool lock (then step 2) |
| **B: backstop, then** | A's step 2: the PI runs `wsl --shutdown` (the v1 E2 route) | always ends every process | no abort row and no trap line; also ends the coordinator session and `d_watch` |

- PQ5 is answered (C) and done. At a freeze, A then B apply as written; no agent sends SIGKILL or runs
  `wsl --shutdown`. The rate is unmeasured, but a hang is recoverable: parts are kept and the resume path is
  registered.
- **PQ5b** (the equality scope) must be answered in the P16 PI line. **Default (no PQ5b answer): the window does not
  open.**

**Consistency with CC-242r2 G0-G14.**

| G | here |
|---|---|
| G2 (no signal pre-marker) | §6 pre-start note: `w25` has no marker; the default-action kill consumes nothing |
| G3 (exit branch keyed on observed state; torn-row clause) | §7 is keyed on the ACCESS_LOG action field and file presence; E2 maps to the no-row branch. A torn last ACCESS_LOG row (no final LF, e.g. after a WSL restart) goes to the one-judge read of the cause, as G3's torn-row clause sends a torn row to its ruling (P12b, N43) |
| G4 (fresh tag and `$S` per retry, after a read) | §4.1, §7; read at 85 (PI-1103ae replaces 90) |
| G5 (E-clock from a file mtime; no ACCESS_LOG stamp read; E1 may end live work) | §3.5, §6 |
| G6 (probe dir absent beforehand) | P9(c) |
| G7 (usage fails closed; backup routine after the resume line) | P17. If usage reaches the PI-1101j stop point during a hang, the coordinator updates `$PRE/RESUME.txt` only (ext4) and tells the PI in chat; no LOG line |
| G8 (live timer reading) | P10 |
| G10 (pause open until the PI answers; RESUME says so) | §4.2, §6 E2, P20 |
| G13 (coordinator order) | §0 order table |

## 7. Exit branches and resume (keyed on the ACCESS_LOG action field and file presence; no sealed byte read)

| state | meaning | branch |
|---|---|---|
| no 'w25 start' row; rc 1 or 2 | pre-window FAULT (owner cache sha, tenancy input, pause line, argparse). Nothing consumed | fix outside the code; one-judge read (85); new tag and fresh `$S` |
| 'w25 start' + 'w25 decide' + 'w25 end', rc 0, 5 outputs present | the window finished | §8 |
| 'w25 start' + 'w25 abort', reason `STOP` (24 h stop or first-batch projection) | features kept (prereg §8.3) | PQ6 to the PI; no resume without a ruling |
| 'w25 start' + 'w25 abort', `FAULT` from tenancy (tag count, LOG read, foreign job, lock, tmpfs mode) | the window was disturbed; parts intact | **resume** after a one-judge read of the cause |
| 'w25 start' + 'w25 abort', `FAULT` lost > cap (NoCaps test 10, OpenViVQA dev 1), a fetch FAULT (status, redirect, not a JPEG), an XM3600 sha hit, or an `ovqa_count` FAULT (N6) | a registered stop | full panel at 85 (PI-1103ad); NoCaps parts kept; the PI is told |
| 'w25 start' + 'w25 abort', reason `ABORT` (signal: E1, or §6A step 1) | stall or wall | one-judge read of `watch.txt`/`ALERT`/`hang.txt`/`pi_e2.txt`, then resume (P12b) or PI |
| 'w25 start' and no end or abort row | SIGKILL of `$PY`, power loss, §6A step 2 WSL restart, or the teardown hang of §6A | residue: if `/dev/shm/c_pvr_w25` exists, remove it by hand with one line in `w25_deletions.log` (utc, `hand`, folder, file count) and one ACCESS_LOG hand row "hand row: tmpfs residue removal (CC-<id>)" (no tab in a field, no token `w25` in the action field); a stale lock is left; then the one-judge read and a resume (P12b) |
| some of the 5 outputs present but no 'w25 decide' row | `decide` failed part-way (e.g. a /mnt/d EIO in `write_new`) | **no rerun**: `w25_pre` refuses. The files are hashed and kept; full panel at 85 (decide is the one look) |

**Resume rules (binding):**
- the same RUN' (§1), `$OWN`, `$F` and `$IN`;
- a new pause line with a fresh tag (`tag_used` refuses a used tag) and a fresh `$S`; P1-P21 with P12b;
- `/dev/shm/c_pvr_w25` absent (the code refuses residue; it is "left for a human");
- finished parts are verified (batch-id sha, set, run sha) and skipped;
- **the 24 h deadline is fixed at the first start** and never reset. The watcher's wall uses the first launch's
  `sh.pid` mtime;
- a second abort or hang of the same class goes to the PI.

## 8. Outputs and their rulings

| output | where | goes to |
|---|---|---|
| `w25_counts.json` (`write_new` 0o444; label, rule, run/code/owners/feats/ga/SSCD shas, per set queried/featured/lost by class/truncated/flagged per owner and criterion/flagged-or-lost/FLICKR_W3 overlap; `n_e_power_inputs`; `id_join_beside_n_e_power`; `ovqa_identity_c`; deferred owners) | `manuscript/prereg/2026-11-02_c_pvr_tier1/` | R4 read, commit |
| `w25_flagged_ids.txt`, `w25_lost_ids.txt`, `w25_ovqa_out_ids.txt`, `w25_f30k_join_ids.txt` (sorted ids; no owner or reason column, PI-1101o) | same | R4, R5 |
| parts `nocaps_test_NNNN.npz` (21) and `ovqa_dev_NNNN.npz` (3); `deadline`; `ovqa_identity_c.json` | `~/.vsps_sealed/c_pvr/w25/` (ext4, 0400) | never committed or copied; reused by the §7.4 self-retrieval |
| `w25_deletions.log`; ACCESS_LOG rows 'w25 start', 'w25 projection', 'ovqa-pin …', 'w25 decide', 'w25 end' / 'w25 abort' | `~/.vsps_sealed/c_pvr/` | the result line mirrors the action field and shas only |
| `$S` and `$PRE` files | ext4 | evidence copies to `.session_backup/<date>/c_w25/` with SHA256SUMS |

**Steps after rc 0:**
1. `OPS-<MMDD>c-w25-result` (coordinator): rc and stamps; the part-line count of this window and its `EXP` (N39; a
   resume's `EXP` is taken from these counts); the 5 output shas; the `n_e_power_inputs` (F, L); the
   id-join count (beside n_e_power, not in it); lost by class; truncated; the ACCESS_LOG action mirror; the
   deletions-log tail; quiet_pre/post; the P10 re-hash; the N53 code re-hash ("CODE re-hash 10 bad []", `c_pvr_run.py`
   = 290a75dc); the `sem.mp-*` count (N48); `env_threads1=2` from `watch.txt` (N22); the triple lists
   edb07fbb / run 4af623d0 / owners 0cf330d3 and owner-feats 8f707edd (N31), and the w25 run sha 290a75dc. Then `OPS-<MMDD>c-w25-resume`.
2. **R4 result read:** one judge, reversible 85. It checks the shas inside `w25_counts.json` = §2; every part present;
   the deletions log complete with the trap line last; lost ≤ caps; `ovqa_identity_c` passed; no residue. Any FAULT,
   abort, hang, `Stop`, lost > cap or departure from RULE §3 goes to a **full panel at 85** instead (PI-1103ad).
3. **Gatekeeper result commit** after the GO (W-R7, N34, N36):
   - `w25_counts.json` and the 4 id files (R5; public image ids, no gold, no reason column; precedent
     `ga_remaining_ids.txt`);
   - the frozen jsons the counts cite by sha: `c_pvr_lists.json` edb07fbb, `c_pvr_owners.json` 0cf330d3,
     `c_pvr_owner_feats.json` 8f707edd, each re-hashed against its staged blob;
   - n-gram scan (`ngram_scan_cen.py`) on **every** staged blob, the jsons included, printing each scanned sha; the
     scan output is kept under `.session_backup/<date>/c_w25/` beside the snapshot (N36);
   - commit prose names removal counts only as "counts per CC-249" (PI-1101o); no AI-attribution line; no host, IP,
     port or PI address.
4. **n_e_power line `OPS-<MMDD>c-ne-power`** (coordinator) after the commit, from the pinned function, never retyped:
```
sha256sum scripts/c_pvr/gates.py    # = 3bced05e… before the import
/usr/bin/python3 -I -B -c 'import json,sys; sys.path.insert(0,"scripts/c_pvr"); import gates; P="manuscript/prereg/2026-11-02_c_pvr_tier1/"; g=json.load(open(P+"gb_counts.json")); d=json.load(open(P+"w25_counts.json"))["n_e_power_inputs"]; print(gates.n_e_power(g["n_e_gb"], d["w25_flagged"], d["lost"]))'
```
   - n_e_power = 10,182 − F − L − 4. Upper bound 10,178. No threshold on it (CC-243 Ruling 3).
   - The id-join hits are reported beside it (CC-245 Ruling 9), never subtracted here.

## 9. Carried items

| item | how it is handled |
|---|---|
| **N6** OpenViVQA missing-name departure (CC-245 Ruling 12) | `ovqa_names` and the pinned `c_pvr.ovqa_count` FAULT on any missing or extra name (cap 0). Stricter than prereg §8.1 (lost, cap 1); **stated as a conservative departure**. If it fires: the NoCaps-test parts are kept, the window ends, and the case goes to the PI and a full panel at 85 (§7). No re-implementation of check (c) and no re-pin of `c_pvr.py` |
| **N7** run document | no `w25-decide` line (decide is inside `w25`); `--owners-sha`, `--feats-sha`, `--in` on the launch line (§3.4); the G-B quiet rule is the default (§4.2); P9(b) passes on "file absent" |
| **N11** `score` and CC-236r3 N2 | `score` only after `w25_counts.json` and its 'w25 decide' row (§1). CC-236r3 N2 (decomp_fail counting; all-fail = FAULT) goes to that later read |
| **N12** aislop file-length finding | a known false positive (one pinned sha = one audit unit, CC-245 Ruling 13). The rule is not disabled; no window action |
| **N17** ViTextVQA dev 1,676 vs 1,520 | `lists` printed 1,676 (CC-249). C's proxy tier-1 dev uses only the 1,520 L1-spent images (the W25 owner `vitextvqa_dev`). The 156 L1a near-duplicate exclusions are not used in tier 1 |
| **N22** thread env | `env OMP_NUM_THREADS=1 MKL_NUM_THREADS=1` written out on the launch line and the P4 selftests (C3); owner-feats and `lists` ran with it (LOG l.1461, l.1466); the watcher records it from `/proc/$PY/environ` and the result line cites it. CC-248 Ruling 4 qualifies CC-245r3 Ruling 5: the env does not remove the hang path (→ N28, §6A). If one thread makes the projection exceed 24 h, that is a `Stop` (§7) |
| **N27** r4 mutant record | 186/186 killed with one TIMEOUT kill (`select_dup_rows_ok`), confirmed as an assertion kill solo by the agent (14.8 s) and by CC-248 (12 s; FAULT text "select None: 2 rows, not n = 1"). N23 reaped the TIMEOUT child; no orphan. 4 registered equivalents survive. No re-run required |
| **N28** hang plan | §6A and PQ5: C done (ab1dd77), A then B backstop |
| **N47** kill line excludes the tracker; argv sentence | §3.4, §6A H4 steps 1 and 3 |
| **N48** `sem.mp-*` count only | P12a, P12b, §3.6, §6A partial parts, §8 step 1 |
| **N49** run sha 290a75dc, P5 25/10, P4 31 s, line drift | §0, §1, §2, §4.1, P1, P4, P5, P6, W-R3; header line refs |
| **N50** C done, efficacy not shown | §6A(i), PQ5, §1 |
| **N51** equality scope | §6A(i), PQ5b, P16 |
| **N52** spawn and tracker patterns | P11, P21 |
| **N53** post-exit code re-hash | §3.6, §8 step 1 |
| **N54** watcher `kids=`/`cpu` include the tracker | §3.5 |
| **N55**, **N56** records | §6A(i) |
| **N29** killpg race | `try/except ProcessLookupError` around `os.killpg` in the harness: held until after `w25_counts.json` (§1) |
| **N31** lists provenance | §0 triple; result line (§8 step 1); optional record hardening held (§1) |
| **N32** P7 | §5 P7 |
| **N33** placeholders, W-R3b, W-R6, order | §0, §1, §2, §10 |
| **N34**, **N36** result commit | §8 step 3 |

## 10. Rulings needed (R2, one judge, reversible 85)

| # | ruling | recommended | default |
|---|---|---|---|
| W-R1 | this document as the run document (commands §3, checklist §5, ladder §6, freeze plan §6A, branches §7, outputs §8) | GO | the window does not open |
| W-R2 | LOG quiet = the G-B rule (§4.2); relaxed form not used | YES | same |
| W-R3 | `w25` runs at RUN' 290a75dc (ab1dd77); owners and owner-feats from fb35ec94, the 6 `of_*.npz` and the 13 staged caches stay valid (CC-251 Ruling 3); P5 = 3 files, 25/10 vs 155b6c01 (N49) | YES | the window does not open |
| W-R3b | run `w25` at fb35ec94 before the TextCaps pin | **MOOT**: `lists` already ran at 4af623d0 (CC-249) | — |
| W-R4 | the watcher: `AUTO=1` (one unattended SIGTERM) vs `AUTO=0` (alert only). The watcher no longer reads the sealed dir (C16), so the v1 "row" question is moot. Conditional on the §3.5 phase rule (N39): no stall SIGTERM once `parts ≥ EXP`, under `AUTO=1` or `AUTO=0`. The declared sealed reads (`cut -f3` of ACCESS_LOG in P7/P12/§3.6; the deletions-log tail in §3.6) need no hand row; any other touch does | `AUTO=1` | `AUTO=0`, the coordinator watches live |
| W-R5 | register by one gatekeeper commit before the pause line exactly 2 paths (CC-250 Ruling 8, N45; CC-250r2 Ruling 7): this file (v1.4) (byte-equal to the GO'd sha) and `W25_PIXEL_RUN_DRAFT.md` 82610ad4907b3394fa84b2b977eba70a5f0faf00859c867f6714dd4bd2973c3d (kept in force by reference for §1, §3, §7); staged-blob shas re-hashed; NGRAM scan PASS on both staged blobs with shas printed, output kept beside the snapshot; `git diff --cached --name-only` = these 2 paths (manuscript/ only, so P5 is unchanged); no AI-attribution line; no host, IP, port or PI address; no concrete pause tag. v1, v1.1, v1.2 and v1.3 stay untracked in their snapshots; the message cites the round-3 GO, CC-250r2 and CC-251 | YES | same |
| W-R6 | a `lists` reference mismatch does not hold the window | **NOT TRIGGERED**: 0 mismatch (CC-249 Ruling 3) | — |
| W-R7 | R5: commit the ids-only outputs plus the frozen lists edb07fbb, owners 0cf330d3 and owner-feats 8f707edd jsons in the result commit (§8 step 3) | YES | commit the 5 W25 outputs only; the jsons stay untracked, pinned by sha |
| W-R8 | apt timers: the live reading governs (G8); a timer due inside the window means waiting | YES | same |
| W-R9 | the N28 freeze plan §6A as written and as amended by N39-N43 (phase-aware H1, CPU-only H3 with its disclosure, the re-checking kill line, the torn-row check) and N47-N55 (C done; A then B backstop; tracker-safe kill line; `sem.mp-*` count only; code re-hash); detection H1-H3, H4 duties, parts, resume vs new run; no further code change before the result | YES | the window does not open |

## 11. PI window questions (times in Vietnam time; each with a recommendation and a default)

| # | question | recommended | default |
|---|---|---|---|
| PQ1 | May the laptop run C's W25 window overnight, starting about 22:00 VN on an evening after the R2 GO and the W-R5 commit? Expected about 1.5-5.5 h (ending about 23:30-03:30 VN). The worst case is the registered 24 h stop, until about 22:00 VN the next day. **During the window no paper writes to LOG.md and no other laptop job runs.** Status: not yet approved (PI-1104c); asked again later. | YES | the window does not open |
| PQ2 | For the window: laptop on mains power, sleep off, lid open? Status: not yet (PI-1104c). | YES (confirm on the day in the PI line) | the window does not open |
| PQ3 | Gemini and the other tool (INC-1027a) closed for the whole window? Status: not yet (PI-1104c). | YES | the window does not open |
| PQ4 | Windows Update restart deferred until the window + 1 h (active hours or pause updates)? Status: not yet (PI-1104c). | YES | the window does not open |
| PQ5 | **(N28) ANSWERED: C (PI-1104c). DONE:** commit ab1dd77, CC-251 GO 90. The code now starts its helper processes in a fresh way (spawn), which removes the suspected cause of a freeze by construction. We could not show that the freeze is gone: our stress test never froze, with the old code or the new. A freeze is possible; we have not shown it is rare in this long run. If it happens, your route is the backstop: **A** first (you kill only the stuck helper processes we list for you, one prepared line each), then **B** (you restart WSL) if the run is still alive 10 min later. The LOG pause stays open until you act, and the 24 h limit keeps running. | answered C; A then B as backstop | — |
| PQ5b | **(N51, corrected by CC-250r2 N57)** You asked for an equality check against the 19 cached feature files. It covered 2 of them, bit-identical on 64 dev images: the KTVIC-dev and OpenViIC-dev files made on this laptop. The other 4 laptop files are not rechecked: one more dev set (ViTextVQA dev) can be checked the same way before the window; the XM3600 file is never re-run, because XM3600 holds a one-look test set; the two KTVIC-image files are not rechecked. The 13 older files (8 copied from rented-machine backups; 5 kept in the laptop folder of the 30-31 Oct step, 4 of which were computed there) are only read by their fingerprint, so this change cannot alter them; at least 4 of them are test-set files that must not be recomputed. The check that matters, whether the new start method computes the same features on this laptop, is what the 64 images test. Do you accept this scope? | YES (optionally add ViTextVQA dev before the window, about 15 min of laptop CPU; rule in §6A(i), N64) | the window does not open |
| PQ6 | If the first-batch projection or the 24 h stop fires: is moving the rest of W25 to a rented 4090 a fallback (host amendment and its own read, about 70k VND [est.])? | YES, as a fallback only | stop, keep the features, ask again |
| PQ7 | If the 5-hour usage field reads None at P17, may the window open on 7-day ≥ 10% plus your line? **ANSWERED: YES (PI-1104c).** | YES | wait for a numeric reading |

## 12. v1 drafting touches, corrected (C6)
- v1 §12 said `~/.vsps_sealed` was "not listed". That was false. The v1 drafting session ran
  `ls ~/.vsps_sealed/c_pvr/ | head -0` (names not printed; no sealed byte read). It is covered by ACCESS_LOG hand row
  26 (LOG l.1454, with the row-number erratum at l.1455).
- The other hand rows on record: row 19 (CC-245 N9: the writer's and the CC-245 judge's listings; LOG l.1448) and
  row 29 (CC-247 N24: the judge's discarded `tail`; ACCESS_LOG sha a4196013 after it; LOG l.1459).
- The one v1 §12 sentence this document relies on (N45), with its false last item struck: "**Not opened:** any Open
  Images label body; `gb_intermediate.json`; any NoCaps data or caption file; `nocaps_val_4500_captions.json`; any
  OpenViVQA json; any TextCaps caption; ACCESS_LOG" (struck: "; `~/.vsps_sealed` (not listed)"). Nothing else in v1
  §12 is relied on.
- STATE (N46): the coordinator updates the next STATE file's C row (W25 run doc v1.2, R2 diff read). Not part of
  this document.

## 13. Touches during v1.1 drafting (`date -u` 2026-11-03 about 18:15-19:00Z)
- **Read:** the sources at the top; LOG l.1453-1468 and `grep` hits in LOG for "row 19"; the CC files named above.
- **Code read** (code text only): the `c_pvr_run.py`, `gates.py` and `build_memory.py` functions listed at the top.
- **Listed (names and sizes only):** `manuscript/prereg/2026-11-02_c_pvr_tier1/`; `~/c_pvr_of_run/` and
  `~/c_lists_1104/` (rc, stdout and stderr file names; no content read); `.session_backup/2026-11-04/`.
- **Not touched:** `~/.vsps_sealed` and everything under it (not opened, listed or statted); ACCESS_LOG; any NoCaps
  data or caption file; any TextCaps caption text; any Open Images label body; `gb_intermediate.json`; any OpenViVQA
  json; the lists, owners and owner-feats json bodies.
- Nothing was run, downloaded or committed. No c_pvr command was run.

## 14. Touches during v1.2 drafting (`date -u` 2026-11-03 about 19:05-19:40Z)
- **Read:** CC-250.txt in full (sha 75a83a20); v1.1 and v1 §12; `c_pvr_run.py` `CODE` l.48-62 and `ovqa_zip`
  l.1022-1032 (code text only); `w25.py` `BATCH` (grep); the v0 and v1.1 shas.
- **Not touched:** `~/.vsps_sealed` and everything under it; ACCESS_LOG; any NoCaps, TextCaps or OpenViVQA data;
  any caption text; any Open Images label body; `gb_intermediate.json`; no bytecode dir was listed or removed (B0
  is planned only).
- Nothing was run, downloaded or committed. No c_pvr command was run.

## 15. Touches during v1.3 drafting (`date -u` 2026-11-04 about 01:15-01:50Z)
- **Read:** CC-251.txt in full (sha a029773f); LOG l.1473, l.1481, l.1484-1485; v1.2 in full.
- **Code read** (code text only): `grep -n` of `c_pvr_run.py` at 290a75dc for the line references above;
  `git diff --numstat 155b6c01 ab1dd77 -- scripts/c_pvr`.
- **Not read:** the r5 evidence files (cited through CC-251 and LOG l.1481 only).
- **Not touched:** `~/.vsps_sealed` and everything under it; ACCESS_LOG; /dev/shm; any NoCaps, TextCaps or OpenViVQA
  data; any caption text; any Open Images label body; `gb_intermediate.json`; no bytecode dir was listed or removed.
- Nothing was run, downloaded or committed. No c_pvr command was run.

## 16. Touches during v1.4 drafting (`date -u` 2026-11-04 about 01:50-02:20Z)
- **Read:** CC-250r2.txt in full (sha 73fd99e8); LOG l.1494 (erratum); v1.3 target passages.
- **Not touched:** `~/.vsps_sealed` and everything under it; ACCESS_LOG; /dev/shm; `~/vsps_w25k1`; any NoCaps, TextCaps
  or OpenViVQA data; any caption text; any Open Images label body; `gb_intermediate.json`.
- Nothing was run, downloaded or committed. No c_pvr command was run.
