# ERRATUM B-ALT-1 to PREREG_DRAFT_B_ALT_v2.md (ed05acdb, commit 2d3c39f): host rule of §5

Written by ruling CC-510e2 (2026-11-27), before use. No FE-LOCUS code has been read, no S0 has run, and no FE-LOCUS quantity exists: no CENSUS_ALT.json, PER_IMAGE_ALT.npz or RESULT_ALT.json.
It changes no hypothesis, threshold, floor, seed, split, estimand, data set or stage order. It replaces only the **Host** paragraph of §5 (l.187).

**Why.** The registered rule names "the D1 rented host" and excludes the PI's PC. It rested on PI-1127h, under which the project rented when money allowed and the PI's PC was neither the default nor switched on (CC-505 ruling 9; CC-510 ruling 6). The PI has since replaced that rule (PI-1127m, LOG 2026-11-27T13:54:47Z): no new rentals; his PC is used and kept on when needed.

## E1. Replacement text for the §5 Host paragraph

**Host (CC-510 ruling 6 as amended by CC-510e2).** One of two hosts, in this order. The laptop writes files only.
- **(a) The D1 rented host**, only if it is still running under its existing payment when the S0 judge code read has passed and D1's `RESULT_D1.json` is pinned on the LOG. The rental is not extended and no new rental is started for this study (PI-1127m).
- **(b) Otherwise, the PI's PC**, under the record checks H1–H7 below.

In either case this study has its own S0 judge code read, its own `env_check`, and **its own hard stop at 8 CPU-h**, separate from D1's 8 CPU-h. S0, S1 and S2 all run on the same host. A move between hosts after S0 has started needs a new judge line.

**Record checks for host (b), each written to the session record before the step it guards.**
- **H1 Own folder.** Every FE-LOCUS file lives in one new folder in the agent's own work area on that machine. Nothing is read or written outside it, except the pinned segmenter environment installed into the same folder. Nothing of Paper A and no other study's folder is touched (PI-1127a).
- **H2 Push by tar, no repository.** Code, the 75 output files, the 2,790 reference strings, `DEV.json`, `FAMILY.json` and `SYSTEMS.tsv` arrive as one tar file whose sha256 is printed on the laptop before the push and matched on the host after it. The tar holds no `.git` directory, and `find <folder> -name .git` returns nothing before S0.
- **H3 Environment.** `env_check` passes in the folder: VnCoreNLP 1.2 jar with its full sha256 pinned at the S0 code read, pyvi 0.1.1, and the CIDEr-D code at its registered sha. S0 self-tests and mutants run on this host.
- **H4 CPU stop.** Every stage runs under one wrapper that adds the user and system CPU time of the whole process tree, logs it, and stops the run at 8 CPU-h. As a backstop, `ulimit -t 28800` is set for each process. A stop writes a judge line, and nothing runs again without one.
- **H5 No overlap with C-CONF.** No FE-LOCUS process runs on that machine from 2026-11-28T09:00Z until the LOG carries the C-CONF test session's end line, or the C-CONF chair's line that C-CONF will not use this machine. Before every stage and at the window's start, `pgrep -af` for the FE-LOCUS wrapper is run and its output recorded. If any FE-LOCUS stage could still be running at 09:00Z, it is not started.
- **H6 Pull and pin.** `RESULT_ALT.json` and `PER_IMAGE_ALT.npz` are pulled to the laptop's home file system, not to `/mnt/d`, and checked against the shas printed on the host. They are pinned on the LOG and set to mode 444.
- **H7 Wipe.** After H6, the whole folder is deleted on the host: tar, references, outputs, the per-image matrix and the environment. `ls` on the folder path, showing it absent, goes to the session record. Logs that hold no caption text may be kept in the pulled copy.

## E2. Text left as it was
The rest of §5, and §§0–4, 6–9, are unchanged. Where §5 says "on the host", it now means the host chosen under E1.
