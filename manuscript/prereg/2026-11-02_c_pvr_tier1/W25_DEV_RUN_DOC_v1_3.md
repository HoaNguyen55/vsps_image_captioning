# C-PVR-T1 dev-set W25 run document v1.2 (Paper C, ACM TALLIP; plan S5; prereg §7.4, §4.4): DRAFT for its one-judge diff read

**Status:** draft for the one-judge diff read v1.1 → v1.2, round 3/3 (the last before ESCALATE_TO_PI), REVERSIBLE 85
(PI-1029o as amended by PI-1103ad/ae), per CC-257r2 (panel, round 2/3, NEXT_ROUND median 82). It licenses nothing
until a GO. Nothing in it has run, been downloaded or been committed. v1 written 2026-11-05 about 05:00-05:50Z; v1.1
about 09:25-09:34Z (file mtime 09:34:21Z, LOG line 09:34:54Z); v1.2 about 10:40-10:55Z (`date -u`), HEAD 5d6f5ca.
- It supersedes `W25_DEV_RUN_DOC_v1_1.md` 2d3ecc2c and `W25_DEV_RUN_DOC_v1.md` afde0323 (both unchanged, kept in
  `.session_backup/2026-11-05/c_w25dev/`).
- **Scope of v1.2:** CC-257r2 W1/BV-G (BLOCKING) and NB1-NB8 only (table §A1). Nothing else changed from v1.1.
- Status of related registrations: T1-REP v4 is committed at 4124ef3 and T1-GUARD v3 at f5c6741. This file cites
  neither as pending.
- **Scope of v1.1:** CC-257 W1-W4 (BLOCKING B1-B4) and the NON-BLOCKING N1-N15 plus PQ-AUTO (table §A). Nothing else
  changed from v1.
- **Label:** TIER 1 / DEV-EXPLORE (C-PVR-T1).
- **Template:** `W25_RUN_DOC_v1_4.md` 8197f5f5 (registered at 2325750; CC-250r3 GO 90). Its §6A freeze plan, §6 ladder
  and §7 exit table are reused **by reference** where this text says so; everything else is restated here.
- **Closes (CC-254 Item 1 NEXT STEP):** N77, N78, N79, N80 (BLOCKING for this GO), N82, N83, N85, N87, N88; CC-252
  N68-N72. N81 binds the S7 read and is written out in §8.2. Table §11.
- **Supersedes in C_NEXT_STEPS_2026-11-04:** the S6 estimate "about 13-14 h" (it assumed D-EN, NoCaps val, KT-C and
  the KTVIC/OpenViIC tests would be featurized; all five come from sha-pinned caches, §3.1) and §3 item 5 "O_B ...
  This is computed in S6" (O_B is out of this run, CC-254 Ruling 1.4; §9).

## A1. Changes from v1.1 (CC-257r2, stamp 2026-11-05T10:20:00Z; each cites its source)

| # | item | v1.1 text | source | exact fix in v1.2 |
|---|---|---|---|---|
| G1 | step-6 GO gate (§3.3 staging command) | `grep -cE "Z \| $PINCC \|.* GO [0-9]{2}"`: fails closed on every real GO line (`\| GO \| 91% \|`) and passes on ESCALATE lines whose subject quotes "GO 88" | CC-257r2 W1/BV-G (BLOCKING), Rulings 4-5 | J1's awk field gate (form (a)): field 2 = the CC id, field 4 starts `GO` and holds no NEXT_ROUND/ESCALATE, field 5 ≥ 85. Test cases and their results are written beside it (§3.3) |
| G2 | pin-line grep | `grep -c "c-tvqa-pin.*$TVSHA"` | CC-257r2 NB1 | anchored: `grep -cE "Z OPS-[0-9]{4}c-tvqa-pin:.*$TVSHA"`, so a CC line quoting the token and the sha cannot satisfy it |
| G3 | P0 gate | only the last `d_watch live:` count | CC-257r2 NB2 | also refuses when the last d_watch.log event is `FAIL` (the P0 PASS row) |
| G4 | provenance | "v1.1 written … about 09:25-10:10Z" | CC-257r2 NB3 | the status line gives v1.1 as 09:25-09:34Z (mtime 09:34:21Z, LOG 09:34:54Z); §15 header corrected |
| G5 | N87 scope; hand row | "over `$HOME`"; "the hand row is left to the coordinator" | CC-257r2 NB4, Ruling 6 | "over `/` or `$HOME`"; §15 and §8.2 cite `OPS-1105c-sealed-handrow` (LOG l.1570) |
| G6 | central directory; decode-check reference | §3.2 (i) silent on the in-memory central directory; §3.4 "l.179-180" | CC-257r2 NB5 | §3.2 (i): the central directory is parsed into memory but never enumerated, printed or written. §3.4 names `scripts/c_stage1/build_memory.py` l.179-180 and notes the check is stricter than `retry_truncated` |
| G7 | P11b regex | misses `OPS-1031m6rent`, `OPS-1031m7rent` | CC-257r2 NB6 | `-?` before the suffix; tested on LOG.md: m6rent, m7rent, m8-rent, m8-deleted, m1-deleted all hit. The ckey.vn live count of 0 stays the operative check |
| G8 | RESUME heredoc; numbering | "W25_DEV_RUN_DOC_v1 §5 P20"; §14 → §16 | CC-257r2 NB7 | "W25_DEV_RUN_DOC_v1_2 §5 P20"; §16 renumbered §15; this round's touches in §16 |
| G9 | T0b repos; freeze scope | candidates unlabelled; "the `CODE` closure" | CC-257r2 NB8 | "unverified candidates"; §1 lists the 8 CODE-closure dirs |
| H1 (v1.3; CC-257r3 ESCALATE_TO_PI 80 → PI-1105i: v1.3 = v1.2 + W1 + W2 only) | GO gate; version pointers | gate `$5+0>=85` rejects `median NN%` GO lines; `DOC=` …v1_1, pause line "§4 of W25_DEV_RUN_DOC_v1_1", RESUME "…v1_2" | CC-257r3 W1, W2; PI-1105i | W1: the CC-257r3 tested gate (field 5 `^(median )?[0-9]+%$`, digits ≥ 85), 17-row test table re-run (§3.3). W2: `DOC=`, the pause line and the RESUME heredoc name W25_DEV_RUN_DOC_v1_3. Nothing else changed; the script docstrings (inside the sha-pinned stage_dev.py 5b2258ed and decode_check.py 24175315) keep "v1_1", by design |
| — | NB9 (STATE refresh; C_NEXT_STEPS freeze note) | — | CC-257r2 NB9 | not in this file: the coordinator's |

## A. Changes from v1 (CC-257, stamp 2026-11-05T07:12:00Z; each cites its source)

| # | item | v1 text | source | exact fix in v1.1 |
|---|---|---|---|---|
| E1 | step order | §0 step 4 runs P0 into `$PRE/pre.txt`, but `$PRE` is first made at step 7 behind `[ ! -e "$PRE" ]` (v1 l.222), so the order cannot run | CC-257 W1/B1 (BLOCKING), Ruling 2 | `$PRE` and `$PRE/h` are made at step 4 (§2, new block) and P0 runs there; the step-7 extraction guard is now "`$PRE` exists and holds no script yet". The staging command checks, before any read: the last `d_watch live:` line of pre.txt ≥ 1, d_watch live now, the pin line, and the step-6 record-check GO (N5). **v1.2 (G1-G3):** the GO gate is the tested awk field gate; the pin grep is anchored; P0 also requires the last d_watch.log event ≠ FAIL |
| E2 | CC-254 departures not named | §3.4 pins the manifests in LOG lines; §3.2 runs pin line, then the record check; §11 claims plain closure | CC-257 W2/B2 (BLOCKING), Ruling 3 | §3.2 and §3.4 state each departure with its reason; §11 N77/N79/N69 rows rewritten |
| E3 | TextVQA val images in the archive | "Never read: any val member" only | CC-257 W3/B3 (BLOCKING), Ruling 4; CC-245 R9; CC-252 (iv) | §3.2 "Val images inside the archive" rules (i)-(iv): no val id list, no namelist, no val member extracted/decoded/featurized; bytes inside the pinned archive are not "arrival"; the corrected reason travels in the pin line and the S7 record (owners json 0cf330d3 not edited); PQ-D5 says so; new D-R12 |
| E4 | IP:port literal | P15 `socket.create_connection((<TEST-NET literal>, 9), …)` | CC-257 W4/B4 (BLOCKING), Ruling 5 | the gates.py l.2192 form inside `unshare -rn`: the `/proc/self/net/dev` interface list == `["lo"]`; P15 PASS row updated. `socket` is no longer imported in the probe |
| E5 | code freeze | none | CC-257 N1, Ruling 6 | §1: from registration to the S7 result commit no commit touches scripts/c_pvr or the CODE closure; S9/S10 drafted only. The C_NEXT_STEPS note is the coordinator's |
| E6 | build_lists disclosure | §3.3 "never opens a caption, question or answer field" | CC-257 N2 | corrected: json.loads parses the pinned KTVIC/OpenViIC train/test jsons and the ViTextVQA dev json in memory; only ids, keys and lengths are accessed (CC-245r2/CC-249 form); also in the stage_dev.py docstring and the staged LOG line |
| E7 | TOFU anchor | "sought at T0 time … for example a dataset loader" | CC-257 N3; CC-247 Ruling 2 | T0b names the anchor before T2: an HF LFS pointer of an unmodified mirror of the same file (candidates named), with repo, commit, sha256 and size recorded; the expected outcome "TOFU only" is pre-stated |
| E8 | size | "about 6.6 GB" | CC-257 N4 | about 7.07 GB (about 6.6 GiB) in §3.2, §10, PQ-D5 |
| E9 | stg.mkdir order | `stg.mkdir` before the RUN pin and the id checks | CC-257 N6 | moved after them: an early FAULT no longer uses up `$STG`. stage_dev.py 5b2258ed (was a8dd6d31) |
| E10 | `$S` made after the append | §3.6 | CC-257 N7 | `mkdir $S` runs after P14 and before the pause-line append |
| E11 | rc not printed | §3.8 | CC-257 N8 | §3.8 prints `w25_rc.txt` and the stderr byte count |
| E12 | decode parity | `load_image` only | CC-257 N9 | decode_check.py 24175315 (was 9507fbe7) runs `_features` and `_mirror_hashes`, the exact per-image calls of `build_memory.features`, and fails on an error string or any exception |
| E13 | netns write probe; no live rental | none | CC-257 N10, N11 | P15 adds a `/mnt/d` `write_new` probe inside `unshare -rn`; new P11b (rental/delete LOG tokens + the ckey.vn instance list) |
| E14 | P17 headroom | "≥ 90 min headroom" copied from a 75-min window | CC-257 N12 | the headroom covers the coordinator's own watch work; the run uses no Claude usage; the 24 h code stop and E2 bound the rest |
| E15 | small fixes | P16 placeholder; §2 "(P7, P12, §3.8)"; §7 decide-phase FAULT; never-executed scripts | CC-257 N13 | P16 filled-guard; §2 "(P7, §3.8)"; §7 row added; §3.3 states both scripts have never run and fail closed |
| E16 | wording | PQ-D1 names MT4; T0 "hrefs only" vs the licence | CC-257 N14 | MT4 dropped (paused, PI-1104b); T0 records the licence from the page's licence link label only |
| E17 | `$TVD` deletion | none | CC-257 N15 | §3.2: deleted after the tier-1 T_A pull and the HC-n deletion record, with one LOG line |
| E18 | PQ-AUTO | none | CC-257 FOR THE PI | PQ-D8 (keep `AUTO=0`) |
| — | N16 STATE refresh | — | CC-257 N16, Ruling 7 | not in this file: the coordinator's next STATE update |

**Sources read for v1.1:** CC-257 in full; the panel journal (wf_2ef57176-1db, grep for the anchor, the size and the
probe form); gates.py l.2186-2194; c_pvr_run.py l.167, l.255-258; CC-245 l.146; CC-247 l.39, l.78.

**Sources read (v1):** CC-254 in full (Item 1 and Item 2); CC-252 N68-N76 and Rulings 2-3; W25_RUN_DOC_v1_4 in full;
`.session_backup/2026-11-04/c_w25/` pre.txt, post.txt, RESUME.txt, watch.txt (head/tail), vitextvqa_check.txt,
`.session_backup/2026-11-04/c_run/r6/selftest_cmd.txt`; C_NEXT_STEPS_2026-11-04 S5-S8, §3, §6; PREREG_DRAFT_v1_2
§4.1-§4.4, §7.4, §8.3; L1a RULE.md l.20-70; TEXTCAPS_PIN_DRAFT l.20-100; LOG l.1405, l.1452, l.1460, l.1496 and the
tail; AMENDMENT_HOST_3090_DRAFT_v3 (grep TextCaps/T_A). Code at 4c0f36b8 (code text only): module docstring,
`CODE` l.57-68, `real_env` l.1224, `dev-w25` block l.1236-1395, `window` l.1146-1191, `run_set` l.994-1018,
`collect` l.1064, `deadline` l.1056, `tenancy` l.701, `tag_used` l.721, `fname` l.820, `build_lists` l.638,
`no_sockets` l.813, `main` l.2484-2527; `match_openviic.load_image`, `build_memory.features` l.150-197,
`w25.rule`/`sscd_any`; harness `SANDBOX` l.351-353; `gates.STAMP` l.744.

---

## 0. Summary

| item | value |
|---|---|
| What runs | `c_pvr_run.py dev-w25` once (one look): featurize the staged D-VI, TextCaps-train and ViTextVQA-dev images, re-open the sealed W25 parts, remove every held C query image and its RULE §3 near-duplicates from D-VI, D-EN and D-TC (prereg §7.4), and count the tier-2 pools (§4.4 NB-T2POOL). Ids and counts only |
| Host | laptop CPU only, 0 VND, no GPU. No network is needed (§3.6, N83) |
| Code | `c_pvr_run.py` 4c0f36b8 at commit c15c183 (CC-254 Item 1 GO 90); c_pvr.py 8f10bd60, gates.py 3bced05e and the other 8 `CODE` pins unchanged |
| Frozen inputs | owners 0cf330d3; owner-feats manifest 8f707edd; lists edb07fbb; W25 result `w25_counts.json` 72ae5ad3 (commit cc90c96, CC-252 GO 91) |
| Staged images (new) | 34,198 = D-VI KTVIC 2,192 + D-VI OpenViIC 8,377 + ViTextVQA dev 1,676 + TextCaps train 21,953 (D-TC 20,883 + T_A 1,070) |
| Cached, not staged | 19 files already in `$IN` (§3.1): the query sets XM3600, NoCaps val, KT-C, KTVIC test, OpenViIC test, and D-EN (`feats_memory.npz` caf4a621) |
| Time | about **4 h** in the window [est.]: 34,198 / 2.58 img/s = 3.7 h, plus about 10 min before the first batch and about 3 min of decide (§10). Registered stop 24 h from the first start |
| Gold | none: pixels, ids, keys and container lengths only |
| New download | one: the TextCaps train pixels, as the official TextVQA train/val image archive (§3.2, N77; PQ-D5) |

**Order and performers.** Each shell block starts with `. "$HOME/w25dev_env.sh"` (§2), because shell state does not
persist between calls.

| # | step | who | gate |
|---|---|---|---|
| 1 | one-judge read of this file | one judge | GO 85 |
| 2 | registration commit of this file only (D-R8) | gatekeeper | after 1 |
| 3 | PI window line (PQ-D1 to PQ-D8) | PI in chat; coordinator writes the PI-<id> line | before step 5 |
| 4 | env file, `mkdir $PRE $PRE/h`, P0 d_watch live (§2, §5) | coordinator | before any /mnt/d bulk read |
| 5 | TextVQA archive pin T0, T0b, T1-T3 (§3.2), LOG line `OPS-<MMDD>c-tvqa-pin` | coordinator | PQ-D5 = YES |
| 6 | one-judge record check of the pin line against §3.2 PASS rules | one judge | before step 8 |
| 7 | scripts out of this file into the existing `$PRE`, sha check (§3.3) | coordinator | — |
| 8 | staging (gated on P0 PASS incl. no FAIL as last d_watch event, d_watch live, the anchored pin line and the step-6 GO by the tested awk gate, §3.3), decode check, LOG line `OPS-<MMDD>c-w25dev-staged` (§3.3, §3.4) | coordinator | outside any window |
| 9 | B0 bytecode removal and its LOG line, then P1-P22 → `pre.txt` (§3.5, §5) | coordinator | right before step 10 |
| 10 | P14, pause line, launch, watcher: **one shell call** (§3.6, §4) | coordinator | all P PASS |
| 11 | watch; E-ladder (§6) | watcher; coordinator; PI at E2 | in the window |
| 12 | §3.8 after-exit, result line, resume line | coordinator | after the exit |
| 13 | S7 result read (§8.2, N81), result commit, datastore pin line | one judge (full panel at 85 on any departure); gatekeeper | after 12 |

## 1. Which sha runs, and the same-sha rule

- **`dev-w25` runs at RUN = 4c0f36b8**, commit c15c183. SUMS holds that line; `integrity()` refuses any other
  `--run-sha`.
- `git diff --stat cc90c96 c15c183 -- scripts/c_pvr` = 3 files, 533 insertions / 52 deletions (CC-254 G3).
  `git diff --stat c15c183 HEAD -- scripts/c_pvr` is empty at HEAD 5d6f5ca (both checked while drafting). The
  registration commit (D-R8) touches `manuscript/` only, so P5 expects exactly these two results.
- The W25 parts were written at 290a75dc. `dev_decide` reads them through `collect(w25w, …, pre["w25_run"])`, with the
  run sha taken from `w25_counts.json` (mutant `dev_w25_parts_own_sha` killed). The run-sha change is therefore safe.
- **Same-sha rule (binding, as v1.4 §1 N11).** No byte of `c_pvr_run.py` or SUMS changes between the first `dev-w25`
  launch and the existence of `dev_w25_counts.json` with its 'dev-w25 decide' row. Every dev part records
  `run_sha256`, and `read_part` refuses a part from another sha. Held back until after the result: N29, N55, N86 (no
  code change), and any hardening.
- **Code freeze (CC-257 Ruling 6, N1; binding).** From the registration commit of this file until the S7 result
  commit, no commit touches `scripts/c_pvr/` (SHA256SUMS included) or any file of the `CODE` closure (the 8 dirs
  scripts, scripts/c_pvr, scripts/w25, scripts/c_stage1, scripts/c_en, scripts/lb, scripts/g2b, scripts/grl). Otherwise P1, P2,
  P3 and P5 fail closed and every pin needs a re-pin. The S9/S10 code may be drafted but not committed in that span.

## 2. Notation (the env file; written once, on the day S5 starts)

```sh
[ ! -e "$HOME/w25dev_env.sh" ] || { echo "GUARD: w25dev_env.sh exists"; exit 1; }
{ echo "D0=$(date -u +%m%d)"; cat <<'EOF'
R=/mnt/d/vsps_image_captioning
L=.session_backup/2026-10-13/decisions/LOG.md
FT=$HOME/.venvs/c_stage1_lists/bin/python
CV=$HOME/.venvs/c_pvr/bin/python
SSCD=$HOME/backups/vsps_image_captioning/.session_backup/2026-10-22/c_stage1/sscd_disc_mixup.torchscript.pt
IN=$HOME/c_pvr_w25_in
OWN=0cf330d39ae4a24b1e95841fbb16f617d405a9d4ffca9747498ef33657f3b086
F=8f707edd3c30180d05a597bd7867a278605e3c9f3cdfc93ebc8544b98d7b50f9
RUN=4c0f36b8521543ff7fe22793455a1903bd54c72e6e22e7cf608618a47756d970
LISTS=edb07fbbea45b69b246ec1e82e23103784b7c777c4e0ef6737e49151d1dc8e18
DOC=manuscript/prereg/2026-11-02_c_pvr_tier1/W25_DEV_RUN_DOC_v1_3.md
PRE=$HOME/w25devpre_$D0
STG=$HOME/c_pvr_dev_stage_$D0
TVD=$HOME/c_pvr_tvqa_dl_$D0
S=$HOME/w25devrun_$D0
P4S=$HOME/w25dev_p4_$D0
DIRS="scripts scripts/c_pvr scripts/w25 scripts/c_stage1 scripts/c_en scripts/lb scripts/g2b scripts/grl"
EOF
} > "$HOME/w25dev_env.sh"; chmod 400 "$HOME/w25dev_env.sh"; sha256sum "$HOME/w25dev_env.sh"
```
**Step 4, right after the env file (E1, CC-257 W1):** make the checklist dir, then run P0 (§5) into it at once.
```sh
. "$HOME/w25dev_env.sh"
[ ! -e "$PRE" ] && mkdir -m 700 "$PRE" "$PRE/h" || { echo "GUARD: $PRE exists"; exit 1; }
```
- `$PRE` (checklist, scripts, manifests), `$STG` (staged images), `$TVD` (the downloaded archive only), `$S` (launch)
  and `$P4S` (selftest scratch) are five separate **new** ext4 dirs. Downloaded data and the scripts never share a dir.
- **New dirs, never `rm -rf` (W25 lesson).** A failed attempt keeps its dirs as they are. After a one-judge read of
  the cause, the retry writes `$HOME/w25dev_env_2.sh`, identical except that `_2` is appended to the five dir names,
  and every later block sources that file instead.
- **N87 (binding for this run and every agent brief):** no `find`, `du` or `ls -R` over `/` or `$HOME` without
  `-path "$HOME/.vsps_sealed" -prune` (`-not -path` does not prune). No command in this file traverses `/` or `$HOME`. The only sealed touches are the
  declared ones (P7, §3.8): `cut -f3` of ACCESS_LOG.tsv and `tail -n 3` of `w25_deletions.log`.
- The concrete pause tag is never written to a file (N71). It lives only in the shell variable `TAG` inside the one
  call of §3.6, on the launch argv and in its LOG line.

## 3. Inputs, staging and the exact command sequence

### 3.1 What is already in `$IN` (no pixel moves; checked by sha)
`dev_pre` reads its query sets and D-EN from the owner caches and `feats_memory.npz` in `$IN` (`owners_load`,
`owner_feats`, `W.load` with each sha). These 19 files are the ones the W25 window used (13 staged per v1.4 §3.2 +
6 owner-feats `of_*.npz` per manifest 8f707edd). `in.sha256` (sha 8633f55d…, 19 lines):

<!-- file: in.sha256 -->
```text
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
10a49f179a9e86b638964a2b94d7f87d7d84fc65504b56ac71a236257fd93775  of_h_bdt1_739.npz
be2b121bf795b1b1aac9ef0d948a21754aad45f1e72b24d6f55c1a1ede9c5604  of_ktvic_dev299.npz
cfbf24f9d88adcd61c3c9fd62afb12d567beac1b602bd8fe51246a741f489bf4  of_openviic_dev_c1.npz
be9aebfbb99a29bf8f74ca6aa392e98710eaa37f38f10fbe97871ffab90502d9  of_refused_ktvic_dup.npz
fe258106652bd1cfe439ad95071aec7ba744e7fdedbda97bc194dfcb63507580  of_vitextvqa_dev.npz
10de1a60700574812f188b89ffdeb800092cd8f068cd508cd496f961d619e01f  of_xm3600_all.npz
```

| role in dev-w25 | set | cache (owner key) |
|---|---|---|
| query | XM3600 (3,600) | `of_xm3600_all.npz` (xm3600_all) |
| query; tier-2 pool | NoCaps val (4,500) | `feats_nocaps_val.npz` (nocaps_val_4500), rows renamed to the tsv ids |
| query | KT-C (3,907) | rows of `feats_coco_test.npz` (karpathy_test_5000), asserted 3,907 |
| query; explore/confirm halves | KTVIC test (558), OpenViIC test (2,001) | `ktvic_test.npz`, `openviic_test.npz` |
| query | NoCaps test (10,496), OpenViVQA dev (1,070) | the sealed W25 parts, under 290a75dc (never copied) |
| datastore | D-EN (80,083) | `feats_memory.npz` caf4a621 (C-EN FEATS cache; CC-254 Ruling 1.1) |
| owner check only | the other 13 | `owners_load` re-hashes all 19 before the window |

At drafting time `$IN` held exactly these 19 files, mode 0400, and the 6 `of_*` shas were re-hashed equal to the
manifest. The 13 others are checked by P8.

### 3.2 TextCaps train pixels: the pinned source (N77, N96)

**The constraint that decides the source.** The same bytes must (i) build and clean D-TC now and (ii) serve T_A for
its tier-1 decode on HC-n later (host amendment v3 l.168, C-8). TextCaps images are TextVQA images (TEXTCAPS_PIN_DRAFT
§1). So the source is **one pinned archive**, not per-image fetches.

**Proposal: the official TextVQA train/val image archive** on the same Meta host that served the pinned TextCaps json
(`dl.fbaipublicfiles.com/textvqa/...`, LOG l.1460).
- The expected link is `https://dl.fbaipublicfiles.com/textvqa/images/train_val_images.zip`, about **7.07 GB (about
  6.6 GiB)**, the size HF mirrors list (CC-257 N4). **Neither is verified here: T0 and the HEAD govern.** The archive
  holds TextVQA train and val images; TextVQA train = 21,953 images = the pinned TextCaps train id count (LOG l.1460),
  which is why it fits.
- Expected member rule: `train_images/<image_id>.jpg` (`TC_MEMBER` in `stage_dev.py`). It is verified for all 21,953
  pinned ids **before any byte is extracted**; one missing member stops staging with nothing written to `textcaps/`.
- Never read: any val member, any test archive, any json. `zipfile` parses the central directory into memory; the code
  never enumerates, prints or writes a name it was not given (one `getinfo` per pinned id, no `namelist()`, no
  `extractall`).

**Val images inside the archive (CC-257 W3/B3; fixed here, before any byte is downloaded).** The HF loader puts train
**and** val images under the same `train_images/<id>.jpg` folder, so the archive brings every TextVQA/TextCaps val
image onto the laptop. TextVQA/TextCaps val is the frozen deferred owner `textvqa_textcaps_val`, whose reason in
`c_pvr_run.py` l.167/l.257 is NOWHERE ("held nowhere: no image or feature cache on any C host … covered on arrival").
- **(i)** No val id list is held or derived. No `namelist()` is taken. No val member is extracted, decoded or
  featurized. The only names the code asks the archive for are the 21,953 pinned train ids (`getinfo`, then `read`).
  `zipfile` parses the central directory into memory; it is never enumerated, printed or written.
- **(ii)** Bytes that sit inside the pinned archive are **not "arrival"** under CC-252 (iv). Arrival = extraction or
  decode of a val member under a later licence (the tier-2 prereg), compared then, count only.
- **(iii)** From the pin line on, the owner's reason reads **"images inside the pinned TextVQA archive, no val id list
  held"** (the CC-245 R9 form used for `vitextvqa_test`). The pin line and the S7 record (§8.2) carry this corrected
  reason. The owners json 0cf330d3 is **not** edited (it is frozen; the same-sha rule and the code freeze hold).
- **(iv)** PQ-D5 tells the PI that the archive also holds the val images and that they are never opened.

**T-steps (coordinator; after PQ-D5 = YES and the registration commit; never inside a window).**
- **T0 (F0 form, no byte of the archive moves).** `playwright-cli` headless render of
  `https://textvqa.org/textcaps/dataset/`, hrefs only, as LOG l.1460. The licence is recorded from the page's licence
  link (its href and link label), not from body text (CC-257 N14). PASS = the page links exactly one image archive
  for the training images on `https://dl.fbaipublicfiles.com/textvqa/`. If that page links none, the same check on
  `https://textvqa.org/dataset/`. The href found is `U`. If neither page links one: stop, fallback below.
- **T0b (anchor named before T2; CC-247 Ruling 2 form, CC-257 N3).** From text only (the HF file pages; no byte of
  any archive), record one independent anchor: the LFS pointer of an unmodified HF mirror of `train_val_images.zip`
  (unverified candidates named by the panel: `leonardPKU/llava1.5_data`, `redactable-llm/TextVQA`; neither was opened while drafting), with repo, commit, LFS sha256
  and size. The HF `facebook/textvqa` loader carries no checksum, so **"TOFU only" is the expected T3 outcome** if no
  mirror shows an unmodified copy; that is pre-stated here and disclosed in the pin line.
- **T1 (fresh dir).**
```sh
. "$HOME/w25dev_env.sh"
[ ! -e "$TVD" ] && mkdir -m 700 "$TVD" || { echo "GUARD: $TVD exists"; exit 1; }
df --output=avail -B1G "$HOME" | tail -n 1          # >= 60 (GB): archive + staged copy + margin
```
- **T2 (HEAD at the final hop, then the body; https only, no proxy env, no HOME; no PI address in any header).**
```sh
. "$HOME/w25dev_env.sh"; U='<the T0 href>'
env -i PATH=/usr/bin:/bin /usr/bin/curl -q -sS --fail -I -L --proto =https --proto-redir =https --max-redirs 3 -A vsps-research "$U" > "$TVD/head.txt"
env -i PATH=/usr/bin:/bin /usr/bin/curl -q -sS --fail -L --proto =https --proto-redir =https --max-redirs 3 -A vsps-research -D "$TVD/get_headers.txt" -o "$TVD/tvqa_images.zip" "$U"; echo "rc=$?" > "$TVD/rc.txt"
sha256sum "$TVD/tvqa_images.zip" > "$TVD/zip.sha256"; stat -c %s "$TVD/tvqa_images.zip" >> "$TVD/zip.sha256"; chmod 400 "$TVD/tvqa_images.zip"
```
  PASS: rc 0; final hop 200; byte size = the final-hop `Content-Length`. Record `Content-Length`, `ETag` and
  `Last-Modified` from both header files.
- **T3 (sha).** The pin is **trust-on-first-download** (the CC-245 Ruling 10 form used for the TextCaps json): the
  sha256 in `zip.sha256`, compared with the T0b anchor. Equal sha and size = "anchored"; different = stop and a
  one-judge read; no anchor found at T0b = "TOFU only", disclosed in the pin line. Any later re-download must give the
  same sha, or it is a new pin with its own read.
- **Pin line** `OPS-<MMDD>c-tvqa-pin` (one `>>`): T0 href, page and licence label; the T0b anchor (or "TOFU only");
  HEAD/GET headers (Content-Length, ETag, Last-Modified); rc; sha256 and size; anchor result; and the corrected owner
  reason "textvqa_textcaps_val: images inside the pinned TextVQA archive, no val id list held" (E3). Then the
  **one-judge record check** of that line against these PASS rules (step 6 of §0; the CC-249 `lists` precedent).
  Staging waits for its GO (the staging command greps it, N5).
- **Departure from CC-254 N77, stated (CC-257 W2/B2).** N77 orders "one one-judge read of the pin, then a LOG pin
  line". This file runs the pin line first, then a one-judge record check of its values, before any staging. Reason:
  the pin's values (sha, size, headers) cannot exist before the download, so a read before the line could rule only the
  procedure, which this file's own read already rules. The record check is the CC-249 form (the judge checks recorded
  values against pre-written PASS rules). No staged byte moves before that GO.
- **Custody of the archive.** Public (the licence as recorded at T0 from the licence link). It stays in `$TVD` on the
  WSL ext4 home: never `/mnt/d`, the repo or a backup path; never committed. It is kept until the tier-1 block's T_A
  pull is done, so T_A on HC-n comes from `$STG/textcaps` (the same bytes, N96).
- **Deletion of `$TVD` (CC-257 N15).** After the tier-1 block has pulled T_A's results and the HC-n deletion record is
  written, the coordinator deletes `$TVD/tvqa_images.zip` (the header, rc and sha files stay) and writes one LOG line
  `OPS-<MMDD>c-tvqa-delete` (file, sha, size). The val images leave the laptop with it, never opened.

**Honest fallback (if T0 finds no official archive, the PI answers PQ-D5 NO, or T2/T3 fail).**
- No other source is used. Per-image Open Images or Flickr URLs would give bytes that differ from the archive, and
  the Flickr originals are partly gone, so D-TC built from them would not match a later T_A decode.
- `dev-w25` cannot then run as committed: `dev_pre` FAULTs on any missing `textcaps/` file (l.1328-1331), and decide
  is one look, so D-TC cannot be cleaned in a later second run.
- Two options, both slower:
  - **F-a (recommended fallback): wait.** S6 does not run, so no tier-1 output can be used (§7.4: "any tier-1 output
    made before it is discarded"). Tier 1 waits for a source.
  - **F-b: strike T_A and D-TC from tier 1.** A code change (STAGE without `textcaps`; new sha, mutants, one-judge
    read) and a prereg amendment with its own read, because T_A is a registered tier-1 dev set (§4.1). The English
    scene-text dev arm and every D-TC retrieval arm are reported NOT RUN. T_B is already empty.
  - Consequence for D-TC under either option: it is never built from unverified bytes.

### 3.3 Staging the 34,198 images (N78, N79; coordinator; outside any window)

**Scripts out of this file.** The three files below are taken from this document by marker, byte for byte, and
checked by sha (P18). `$PRE` already exists from step 4 (E1):
```sh
. "$HOME/w25dev_env.sh"; cd "$R"
[ -d "$PRE" ] && [ ! -e "$PRE/stage_dev.py" ] || { echo "GUARD: $PRE missing, or the scripts are already there"; exit 1; }
/usr/bin/python3 -I -B -c 'import re,sys; t=open(sys.argv[1], encoding="utf-8").read(); [open(sys.argv[2]+"/"+n, "x", encoding="utf-8").write(b) for n, b in re.findall(r"<!-- file: (\S+) -->\n```[a-z]*\n(.*?)```\n", t, re.S)]' "$DOC" "$PRE"
cp -n .session_backup/2026-11-04/c_w25/w25_watch.sh "$PRE/"
( cd "$PRE" && sha256sum in.sha256 stage_dev.py decode_check.py w25_watch.sh )
```
Expected: in.sha256 8633f55d7f6db8f05b24d48d783313227ba06c6f42feff1a48588ad0e4954acb; stage_dev.py
5b2258eddcf8dcaf96cf1026f7b91d47b93b104096cfffbf7ef27706db0d8008; decode_check.py
241753159520b5e8fd2c6fa0f4cfb8bacc3ec787491cfbd584c8e840b08b0039; w25_watch.sh
23daaa6df249765745b9dd4a411a3e65e188bd31feb2bcaf96c4d518a8000852 (the W25 watcher, unchanged).

**What `stage_dev.py` does.**
- **Id lists by the run's own function.** It asserts `c_pvr_run.py` = RUN 4c0f36b8, imports it (CODE-checked by
  `load`) and calls
  `build_lists(root, LISTS_IN, OWNERS, sets)`, the function `dev_pre` calls (l.1306). So the staged ids are the ids
  `dev_pre` will ask for, by construction. It asserts 2,192 / 8,377 / 1,676 / 21,953, T_A = the frozen `t_a_ids`, and
  the frozen lists counts (lists json re-hashed to edb07fbb). It writes `ids_<sub>.txt` (ids only) to `$PRE`.
- **Only the kept images move.** `ktvic/images` (4,327 files) and `openviic/images` (13,300) also hold test and dev
  images; only the D-VI ids are copied. Custody test pixels never move.
- **File names follow `fname` (l.820):** KTVIC keeps its own extension, exactly one `<11-digit id>.*` per id (one
  `scandir` of the source dir, then a lookup); OpenViIC uses the key; ViTextVQA and TextCaps use `<id>.jpg`. Sub-dirs
  are `ktvic/ openviic/ vitextvqa_dev/ textcaps/` (`STAGE` l.1251).
- **ViTextVQA dev 1,676 (N78).**
  - 1,520 from `data/datasets/l1a_vitextvqa_dev/images/`, each re-hashed against `l1a_lists.json` (ac5ed047)
    `dev/image_sha256`. One mismatch = FAULT.
  - 156 = the `flagged_dev_files` keys of `neardup.json` (fa676be1). The script asserts that l1a 1,520 + flagged 156 =
    exactly the 1,676 dev files, disjoint (checked while drafting: equal; and every dev `filename` = `<id>.jpg`).
  - They come from `ViTextVQA_images.zip`, re-hashed in full to 39420475 first (5.58 GB, one sequential read over
    9p), then member `st_images/<name>` only. No other member is read.
  - **The 156 are trust-on-extract under the zip pin.** neardup.json stores criteria per file (C1, C2, C3, max_sscd,
    min_hash), not a sha. zipfile's CRC32 check guards the read.
- **Each file:** read once from its source, written with exclusive create (`open(…, "xb")`), fsynced, chmod 0400,
  re-read and re-hashed on ext4. One manifest per sub-dir, `$PRE/stage_<sub>.sha256`, in `sha256sum -c` form.
- **`$STG` is made only after** the RUN pin, the imports and the id checks (CC-257 N6), so an early FAULT leaves
  `$STG` absent and the same command can run again after the cause is fixed.
- **Chunked /mnt/d reads:** single-threaded, one-second pause every 256 files, with `d_watch` live (P0; checked by the
  command below).
- **What is parsed (CC-257 N2, corrected from v1).** `build_lists` json-parses the pinned KTVIC train/test, OpenViIC
  train/test and ViTextVQA dev jsons in memory, and `stage_dev.py` parses `l1a_lists.json` and `neardup.json`. Caption,
  question and answer strings are therefore in memory, but only ids, keys and container lengths are accessed; nothing
  else is printed or written (the CC-245r2/CC-249 form). It never lists a zip and runs with `HOME=$PRE/h`, so
  `Path.home()/.vsps_sealed` resolves to scratch even by mistake.
- **Never executed (CC-257 N13).** `stage_dev.py` and `decode_check.py` have not been run. Both fail closed (FAULT,
  nothing removed); a failure costs a one-judge read of the cause and, at worst, a `_2` retry.

**Command** (gated on P0 PASS, d_watch live now, the pin line, and the step-6 record-check GO; E1, N5):
```sh
. "$HOME/w25dev_env.sh"; cd "$PRE"
PINCC='<CC id of the step-6 record check>'; case "$PINCC" in ''|*'<'*) echo "fill PINCC"; exit 1;; esac
[ "$(awk -F' \\| ' -v id="$PINCC" '$2==id && $4 ~ /^GO([ :(]|$)/ && $4 !~ /NEXT_ROUND|ESCALATE/ && $5 ~ /^(median )?[0-9]+%$/ {v=$5; gsub(/[^0-9]/,"",v); if (v+0>=85) print}' "$R/$L" | wc -l)" -ge 1 ] || { echo "no GO line for $PINCC"; exit 1; }
[ "$(grep '^d_watch live:' "$PRE/pre.txt" | tail -n 1 | awk '{print $3}')" -ge 1 ] 2>/dev/null || { echo "P0 not PASS in pre.txt"; exit 1; }
[ -e "$HOME/.local/state/vsps/d_watch.log" ] && [ "$(awk '/ FAIL$| RECOVERED$/{l=$NF} END{print l}' "$HOME/.local/state/vsps/d_watch.log")" = FAIL ] && { echo "d_watch.log: last event FAIL"; exit 1; }
[ "$(ps -eo pid,args | awk '($2 ~ /bash$/ && $3 ~ /d_watch\.sh$/) || $2 ~ /d_watch\.sh$/' | wc -l)" -ge 1 ] || { echo "d_watch not live now"; exit 1; }
TVSHA=$(head -c 64 "$TVD/zip.sha256"); [ "$(grep -cE "Z OPS-[0-9]{4}c-tvqa-pin:.*$TVSHA" "$R/$L")" -ge 1 ] || { echo "no pin line for the archive sha"; exit 1; }
[ ! -e "$STG" ] || { echo "GUARD: $STG exists"; exit 1; }
env -i PATH=/usr/bin:/bin HOME="$PRE/h" OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 "$FT" -I -B "$PRE/stage_dev.py" "$R" "$STG" "$PRE" "$TVD/tvqa_images.zip" "$TVSHA" > "$PRE/stage_out.txt" 2> "$PRE/stage_err.txt"; echo "rc=$?" >> "$PRE/stage_out.txt"
tail -n 6 "$PRE/stage_out.txt"; wc -c < "$PRE/stage_err.txt"
```
**GO-gate test (CC-257r3 W1; run by the drafter on 2026-11-05 about 12:00Z, against LOG.md as it stood, with the
gate line above and `PINCC` set to each id; field 5 may read `NN%` or `median NN%`):**

| PINCC | LOG verdict (field 5) | gate count | required |
|---|---|---|---|
| CC-240 | GO (median 93%) | 1 | accept |
| CC-242r2 | GO (median 92%) | 1 | accept |
| CC-213r3 | GO (median form) | 1 | accept |
| CC-244r2 | GO (median 93%; LOG l.1425, the newest real median-form GO line) | 1 | accept |
| CC-249 | GO | 1 | accept |
| CC-252 | GO | 1 | accept |
| CC-254r3 | GO | 1 | accept |
| CC-245r3 | GO | 1 | accept |
| CC-999 | synthetic current one-judge form `\| GO (one judge record check) \| median 90% \|`, appended to a /tmp copy of LOG.md only | 1 | accept |
| CC-255r3 | ESCALATE_TO_PI | 0 | reject |
| CC-255r4 | ESCALATE_TO_PI (median n/a%) | 0 | reject |
| CC-257 | NEXT_ROUND | 0 | reject |
| CC-257r2 | NEXT_ROUND | 0 | reject |
| CC-257r3 | ESCALATE_TO_PI (median 80%) | 0 | reject |
| CC-254 | mixed items (Item 1 GO, Item 2 NEXT_ROUND) | 0 | reject |
| CC-229 | field 5 "Q1 94% / Q2 93%" | 0 | reject |
| CC-247 | field 5 "GO" (no percentage) | 0 | reject |

All seventeen as required (CC-999 gives 0 on the real LOG.md). A mixed-item CC fails closed, so `PINCC` must name a dedicated record-check CC.

PASS: rc 0; last lines `ktvic 2192 manifest …`, `openviic 8377 …`, `vitextvqa_dev 1676 …`, `textcaps 21953 …`,
`STAGE PASS`; stderr empty. Any FAULT: nothing is removed; the dirs stay; one-judge read; a retry uses `_2` dirs (§2).

<!-- file: stage_dev.py -->
```python
#!/usr/bin/env python3
"""W25_DEV_RUN_DOC_v1_1 §3.3: stage exactly the images dev-w25's dev_pre asks for, by name only, into a new ext4 dir.
Args: ROOT STG PRE TVQA_ZIP TVQA_SHA. Ids come from c_pvr_run.build_lists (pinned inputs: ids, keys, lengths only).
json.loads parses the pinned train/test/dev jsons in memory; only ids, keys and lengths are accessed (CC-245r2/CC-249
form). No zip is listed or extracted in full; no val member is touched; ~/.vsps_sealed is never used."""
import hashlib
import json
import os
import sys
import time
import zipfile
from pathlib import Path

root, stg, pre, tz, tz_sha = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]), sys.argv[5]
D = root / "data/datasets"
VZ = (D / "vitextvqa_raw/ViTextVQA_images.zip", "39420475263f38892c5abceed5b4886beec707526f9e05a12e2ecd39a0d0e0b3")
L1A = (root / "manuscript/prereg/2026-10-29_l1a/l1a_lists.json",
       "ac5ed047dc013cb642a325b491994d516ff8ee187c26f30fa47c0b62057e0087")
ND = (root / "manuscript/prereg/2026-10-29_l1a/neardup.json",
      "fa676be1274fac78ba9624f0432b34b91766b60ad5ec247c54b77ff1e5ac843d")
TC_MEMBER = "train_images/{}.jpg"  # TextVQA train/val zip member rule [expected; the pre-check below confirms all ids]
WANT = {"ktvic": 2192, "openviic": 8377, "vitextvqa_dev": 1676, "textcaps": 21953}


def fault(msg):
    sys.exit(f"FAULT: {msg}")


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def pinned(p, want):
    if sha_file(p) != want:
        fault(f"{p.name} differs from its pin {want[:8]}")
    return p


def put(sub, name, b, man, n):
    p = stg / sub / name
    with open(p, "xb") as f:  # exclusive create: nothing is ever overwritten
        f.write(b)
        f.flush()
        os.fsync(f.fileno())
    os.chmod(p, 0o400)
    h = hashlib.sha256(b).hexdigest()
    if sha_file(p) != h:
        fault(f"{sub}/{name} differs after the write")
    man.append(f"{h}  {name}\n")
    if n % 256 == 255:
        print(f"{sub} {n + 1}", flush=True)
        time.sleep(1)  # chunked /mnt/d reads (EIO history, CC-254 N79)


def done(sub, man):
    if len(man) != WANT[sub]:
        fault(f"{sub}: {len(man)} files, not {WANT[sub]}")
    with open(pre / f"stage_{sub}.sha256", "x") as f:
        f.write("".join(man))
    print(sub, len(man), "manifest", sha_file(pre / f"stage_{sub}.sha256"), flush=True)


pinned(root / "scripts/c_pvr/c_pvr_run.py", "4c0f36b8521543ff7fe22793455a1903bd54c72e6e22e7cf608618a47756d970")  # RUN
sys.path.insert(0, str(root / "scripts/c_pvr"))
import c_pvr_run as R  # noqa: E402

R.load(root)
s = {}
R.build_lists(root, R.LISTS_IN, R.OWNERS, s)
ids = {"ktvic": sorted(s["kept_kt"], key=int), "openviic": sorted(s["kept_ov"]), "vitextvqa_dev": s["vt"],
       "textcaps": sorted(s["tc"])}
lj = json.loads(pinned(root / R.LISTS_FILE, R.LISTS_SHA).read_text())
if ({k: len(v) for k, v in ids.items()} != WANT or s["t_a"] != lj["t_a_ids"]
        or (lj["d_vi"]["ktvic_train_images"], lj["d_vi"]["openviic_train_images"], lj["vitextvqa_dev_images"])
        != (2192, 8377, 1676) or len(set(s["tc"]) - set(s["t_a"])) != lj["d_tc_images_before_w25"]):
    fault("the rebuilt id sets differ from the frozen c_pvr_lists.json")
for sub, v in ids.items():
    with open(pre / f"ids_{sub}.txt", "x") as f:
        f.write("".join(f"{i}\n" for i in v))

stg.mkdir(mode=0o700)  # only after the RUN pin and the id checks; FileExistsError if it exists: never rm -rf
for sub in WANT:
    (stg / sub).mkdir(mode=0o700)
man = []
by = {}
for e in os.scandir(D / "ktvic/images"):
    by.setdefault(e.name.split(".", 1)[0], []).append(e.name)
for n, i in enumerate(ids["ktvic"]):
    hit = by.get(f"{int(i):011d}", [])
    if len(hit) != 1:
        fault(f"KTVIC id {i}: {len(hit)} files, not exactly one")
    put("ktvic", hit[0], (D / "ktvic/images" / hit[0]).read_bytes(), man, n)
done("ktvic", man)

man = []
for n, k in enumerate(ids["openviic"]):
    put("openviic", k, (D / "openviic/images" / k).read_bytes(), man, n)
done("openviic", man)

man = []
l1a = json.loads(pinned(*L1A).read_text())["dev"]["image_sha256"]
fl = sorted(json.loads(pinned(*ND).read_text())["flagged_dev_files"], key=lambda f: int(f[:-4]))
names = {f"{i}.jpg" for i in ids["vitextvqa_dev"]}
if len(l1a) != 1520 or len(fl) != 156 or set(l1a) & set(fl) or set(l1a) | set(fl) != names:
    fault("ViTextVQA dev: l1a 1,520 + flagged 156 are not exactly the 1,676 dev files")
for n, f in enumerate(sorted(l1a, key=lambda f: int(f[:-4]))):
    b = (D / "l1a_vitextvqa_dev/images" / f).read_bytes()
    if hashlib.sha256(b).hexdigest() != l1a[f]:
        fault(f"ViTextVQA dev {f} differs from l1a_lists dev/image_sha256 (N78)")
    put("vitextvqa_dev", f, b, man, n)
with zipfile.ZipFile(pinned(*VZ)) as z:  # the central directory is parsed; only st_images/<flagged name> is read
    for n, f in enumerate(fl):
        put("vitextvqa_dev", f, z.read(z.getinfo(f"st_images/{f}")), man, 1520 + n)
done("vitextvqa_dev", man)

man = []
with zipfile.ZipFile(pinned(tz, tz_sha)) as z:  # names are never enumerated; one getinfo per pinned id
    miss = 0
    for i in ids["textcaps"]:
        try:
            z.getinfo(TC_MEMBER.format(i))
        except KeyError:
            miss += 1
    if miss:
        fault(f"TextCaps: {miss} pinned ids have no {TC_MEMBER} member; nothing extracted")
    for n, i in enumerate(ids["textcaps"]):
        put("textcaps", f"{i}.jpg", z.read(TC_MEMBER.format(i)), man, n)
done("textcaps", man)
print("STAGE PASS", flush=True)
```

### 3.4 Decode check of every staged file (N79; before P1)
`LOST_CAP` is 0 for the four staged sets (l.1253), so one unreadable or truncated file FAULTs the one-look run hours
in. The check runs the run's own per-image calls, `match_openviic._features` and `_mirror_hashes` (what
`build_memory.features` maps over every path, `scripts/c_stage1/build_memory.py` l.179-180), with truncated loading
off, over the names in the four manifests (no listing). It fails on the `(path, error)` return that `features` counts
as lost and on any exception after a good load (CC-257 N9). It fails closed and is stricter than the run: the run's
`retry_truncated` is False for these sets too, so any file the check passes, the run reads the same way. One process; about 20-35 min [est.].
```sh
. "$HOME/w25dev_env.sh"; cd "$PRE"
env -i PATH=/usr/bin:/bin HOME="$PRE/h" OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 "$FT" -I -B "$PRE/decode_check.py" "$R" "$STG" "$PRE" > "$PRE/decode_out.txt" 2>&1; echo "rc=$?" >> "$PRE/decode_out.txt"
cat "$PRE/decode_out.txt"
```
PASS: rc 0; `unreadable 0` on all four lines; `DECODE PASS`. Any failure: no window; the failing names (ids only)
go to a one-judge read. A failure is a source problem, not a run choice: nothing is dropped by hand.

Then one LOG line `OPS-<MMDD>c-w25dev-staged` (before the pause line): the 4 counts, the 4 manifest shas, the
`stage_out.txt` and `decode_out.txt` shas, the archive sha, the stage_dev.py and decode_check.py shas, the 1,520
l1a re-hash result, "156 trust-on-extract under zip 39420475", and "build_lists json-parsed the pinned jsons in
memory; ids, keys and lengths only accessed" (N2).

**Departure from CC-254 N79, stated (CC-257 W2/B2).** N79 asks for each manifest to be "pinned in the run doc". This
file pins the **procedure, the counts and the three script shas**; the **four manifest shas** are pinned in the
`OPS-<MMDD>c-w25dev-staged` LOG line and repeated in the pause line, and P8 re-checks every staged file against them
with `sha256sum -c` right before the window. Reason: the TextCaps manifest cannot exist before the archive is
downloaded, and the D-VI manifests are trust-on-copy from /mnt/d (no earlier per-file pin exists), so no manifest sha
can be written into this file before registration. The 1,520 ViTextVQA shas are the exception: they are pre-pinned by
`l1a_lists.json` ac5ed047 and re-checked by `stage_dev.py`.

<!-- file: decode_check.py -->
```python
#!/usr/bin/env python3
"""W25_DEV_RUN_DOC_v1_1 §3.4 (CC-254 N79; CC-257 N9): run the run's own per-image calls, match_openviic._features
and _mirror_hashes (what build_memory.features maps over every path), on every staged image, truncated loading off. LOST_CAP is 0 for the
four staged sets, so one failure here means the window must not open. Args: ROOT STG PRE. Names come from the
manifests, never from a listing."""
import hashlib
import sys
from pathlib import Path

root, stg, pre = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
mo = root / "scripts/match_openviic.py"
if hashlib.sha256(mo.read_bytes()).hexdigest() != "c0d9dd30e3222ab6542a7e1acfbb9bd3899e4b6db5c896b0adc4d805c1005a8b":
    sys.exit("FAULT: match_openviic.py differs from its CODE pin")
sys.path.insert(0, str(root / "scripts"))
from PIL import ImageFile  # noqa: E402

from match_openviic import _features, _mirror_hashes  # noqa: E402

assert ImageFile.LOAD_TRUNCATED_IMAGES is False
bad = 0
for sub in ("ktvic", "openviic", "vitextvqa_dev", "textcaps"):
    names = [x.split("  ", 1)[1] for x in (pre / f"stage_{sub}.sha256").read_text().splitlines()]
    fail = []
    for f in names:
        try:
            r = _features(str(stg / sub / f))
            _mirror_hashes(str(stg / sub / f))
            if isinstance(r[1], str):  # (path, error): the case features() counts as lost
                fail.append(f"{f} {r[1].split(':', 1)[0]}")
        except Exception as e:  # an error after a good load (imagehash, sscd input) would stop the run itself
            fail.append(f"{f} {type(e).__name__}")
    bad += len(fail)
    print(sub, "files", len(names), "unreadable", len(fail), *fail[:20], flush=True)
print("DECODE PASS" if bad == 0 else f"DECODE FAIL {bad}")
sys.exit(1 if bad else 0)
```

### 3.5 Bytecode removal, preconditions, then §3.6
- **B0, before P1** (v1.4 §3.3 B0, same 8 dirs): list, then remove, the git-ignored bytecode of the CODE closure.
```sh
. "$HOME/w25dev_env.sh"; cd "$R"
for d in $DIRS; do ls -l "$d"/__pycache__ "$d"/*.pyc 2>/dev/null; done > "$PRE/bytecode_removed.txt"
for d in $DIRS; do
  if [ -d "$d/__pycache__" ]; then git check-ignore -q "$d/__pycache__" && rm -r "$d/__pycache__" || echo "NOT IGNORED: $d/__pycache__"; fi
  for f in "$d"/*.pyc; do [ -e "$f" ] && { git check-ignore -q "$f" && rm "$f" || echo "NOT IGNORED: $f"; }; done
done
sha256sum "$PRE/bytecode_removed.txt"; wc -l < "$PRE/bytecode_removed.txt"
```
  Any `NOT IGNORED` line is a stop (nothing tracked is removed; one-judge read). One LOG line
  `OPS-<MMDD>c-w25dev-bytecode` (dirs, file count, list sha). Every python line here keeps `-B`.
- Then §5 P0-P22 in the stated order, outputs appended to `$PRE/pre.txt` with stderr (N68). Then
  `sha256sum "$PRE/pre.txt"` **before** the pause line is built; `pre.txt` is never written again (N70).

### 3.6 P14, pause line, launch and watcher: one shell call (N70, N71, N83)
The tag exists only in this call. The line tested is the line appended (no two-field exception). `NS` is
`unshare -rn` if P15 passed, else empty with the reason in the result line.
```sh
. "$HOME/w25dev_env.sh"; cd "$R"
NS='unshare -rn'                                   # or NS='' if P15 failed (state the reason)
TAG="OPS-$(date -u +%m%d)c-w25devpause"
PL="$(date -u +%FT%TZ) $TAG: C dev W25 pause window opens per <CC id of this file's GO>, CC-254 and <PI id of the window line>: from this line until c_pvr_run.py dev-w25 exits, every LOG.md writer and every other paper's laptop job is paused (§4 of W25_DEV_RUN_DOC_v1_3 <sha8 of this file>); HEAD $(git rev-parse --short HEAD), c_pvr_run.py 4c0f36b8, owners 0cf330d3, owner-feats 8f707edd, lists edb07fbb, w25_counts 72ae5ad3, TextVQA archive <sha8>, staging manifests <4 x sha8>; preconditions §5 all PASS ($(sha256sum < "$PRE/pre.txt" | cut -c1-8)); netns ${NS:-off}; hang plan §6 (= W25_RUN_DOC_v1_4 §6A, A then B); no other LOG line until the exit."
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
' "$TAG" "$L" > "$PRE/p14.txt" 2>&1 || { cat "$PRE/p14.txt"; echo "P14 FAIL: no pause line"; exit 1; }
[ ! -e "$S" ] && mkdir -m 700 "$S" || { echo "LAUNCH GUARD: $S exists; no pause line"; exit 1; }      # before the append (N7)
printf '%s\n' "$PL" >> "$L"; sleep 2
{ wc -l "$L"; sha256sum "$L"; } > "$PRE/quiet_pre.txt"; [ "$(tail -n 1 "$L")" = "$PL" ] && echo "pause line is last"
setsid -f /bin/sh -c 'echo $$ >"$1/sh.pid"; OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 $2 "$3" -I -B scripts/c_pvr/c_pvr_run.py dev-w25 --host laptop --run-sha "$4" --pause-tag "$5" --owners-sha "$6" --feats-sha "$7" --sscd "$8" --in "$9" --stage "${10}" >"$1/w25_stdout.txt" 2>"$1/w25_stderr.txt"; echo "rc=$? $(date -u +%FT%TZ)" >"$1/w25_rc.txt"' \
  sh "$S" "$NS" "$FT" "$RUN" "$TAG" "$OWN" "$F" "$SSCD" "$IN" "$STG"
sleep 3; setsid -f /bin/sh "$PRE/w25_watch.sh" "$S" "$(stat -c %Y "$S/sh.pid")" 0 69
sleep 15; head -n 2 "$S/watch.txt"                 # line 2 must read parts=0/69 armed=1 (N59, N72)
```
- `$2` (NS) is unquoted on purpose so that `unshare -rn` splits into two words and an empty NS vanishes. `unshare`
  without `--fork` execs, so the python keeps the pid that `pgrep -P "$SH"` finds (pid route of v1.4 §3.4, unchanged).
- The stdout, stderr and rc file names stay `w25_*` because the reused watcher (23daaa6d) reads exactly those.
- `p14.txt` holds booleans only, never the tag. Its sha goes in the result line. The `filled` check refuses a line that
  still holds a `<…>` placeholder, so an unfilled template can never reach LOG.md.
- P14 runs **after** `pre.txt` is closed, so the pause line cites the final pre.txt sha and P14 tests the final string.
- **Detached** (`setsid -f`); never `pgrep -f` or `pkill -f`.

### 3.7 Watch (ext4 and /proc only; never `~/.vsps_sealed`; no LOG line until the exit)
- The watcher is v1.4 §3.5 byte for byte (23daaa6d), started with `AUTO=0` (D-R7) and **`EXP = 69`**:
  `dvi_ktvic` 5 parts (2,192 / 512), `dvi_openviic` 17 (8,377), `vitextvqa_dev` 4 (1,676), `textcaps` 43 (21,953).
  The last part line is `textcaps part 0042`. The part lines are `"<set> part NNNN: …"` from `run_set` (l.1014,
  `flush=True`). The projection line has no `' part '` token.
- **EXP check (N72).** P22 records `EXP=69` with its integer check in pre.txt, and §3.6 prints watch.txt line 2, which
  must read `parts=0/69 armed=1`. If not, the coordinator stops and restarts the watcher only.
- In this run `curl=` stays 0 and there is no fetch phase: every image is read from `$STG` in place (`stage_local`,
  l.1287), nothing is copied to tmpfs, and each batch's `drop` logs 0 files.
- **Phase rule (N39) unchanged:** stall armed only while `parts < 69`; `dev_decide` prints nothing and is never
  stalled; the wall (24 h + 90 min) stays armed.

### 3.8 After the exit (coordinator; `w25_rc.txt` exists, or §6 step 2 ended the process)
```sh
. "$HOME/w25dev_env.sh"; cd "$R"
cat "$S/w25_rc.txt"; echo "stderr bytes $(wc -c < "$S/w25_stderr.txt")"                    # rc=0 and 0 bytes (N8)
ls /dev/shm/c_pvr_w25 2>/dev/null && echo RESIDUE                                         # must print nothing
{ wc -l "$L"; sha256sum "$L"; } > "$S/quiet_post.txt"; cmp "$PRE/quiet_pre.txt" "$S/quiet_post.txt" && echo "quiet held"
cut -f3 "$HOME/.vsps_sealed/c_pvr/ACCESS_LOG.tsv" | grep -n '^dev-w25 \|^w25 projection'    # action field only
cut -f3 "$HOME/.vsps_sealed/c_pvr/ACCESS_LOG.tsv" | grep -c '^ovqa-pin'
tail -n 3 "$HOME/.vsps_sealed/c_pvr/w25_deletions.log"                                    # dev trap line last (N82)
sha256sum manuscript/prereg/2026-11-02_c_pvr_tier1/{dev_w25_out_ids.json,dev_w25_counts.json}
sha256sum "$FT" "$(readlink -f /usr/bin/python3)"                                         # = P10 values
sha256sum "$S"/{watch.txt,ALERT,hang.txt,pi_e2.txt} "$PRE/p14.txt" 2>/dev/null
ls /dev/shm | grep -c '^sem\.mp-'                                                         # count only (N48)
for s in ktvic openviic vitextvqa_dev textcaps; do ( cd "$STG/$s" && sha256sum -c --quiet "$PRE/stage_$s.sha256" ) && echo "$s unchanged"; done
/usr/bin/python3 -I -B -c 'import ast,hashlib; t=open("scripts/c_pvr/c_pvr_run.py","rb").read(); assert hashlib.sha256(t).hexdigest()=="4c0f36b8521543ff7fe22793455a1903bd54c72e6e22e7cf608618a47756d970"; c=next(ast.literal_eval(n.value) for n in ast.parse(t).body if isinstance(n,ast.Assign) and getattr(n.targets[0],"id","")=="CODE"); print("CODE re-hash", len(c), "bad", [p for p,h in c.items() if hashlib.sha256(open(p,"rb").read()).hexdigest()!=h])'
```
- Expected ACCESS_LOG actions from this run, in order: `dev-w25 start`, `w25 projection` (dev-w25 writes its
  projection row under that name, N82), the `ovqa-pin` read row(s) of `ovqa_names`, `dev-w25 decide`, `dev-w25 end`.
- The 69 per-batch lines "after <set>_NNNN" log 0 files; the trap line ("trap: window exit") is the new last line of
  `w25_deletions.log`. CC-252's "trap line 15:52:26Z is last" no longer holds, as expected (N82).
- The code re-hash prints `CODE re-hash 10 bad []` (v1.4 N53 form). A mismatch sends the run to a one-judge read
  before any output is used.
- Then `OPS-<MMDD>c-w25dev-result`, then at once `OPS-<MMDD>c-w25dev-resume` (§4.2), then §7 or §8.

## 4. Pause tag, pause line and the window rules

### 4.1 Tag
- **Tag = `OPS-<MMDD>c-w25devpause`** (`<MMDD>` = `date -u` month-day of the pause line). It fullmatches
  `OPS-[0-9A-Za-z][0-9A-Za-z-]*`; the lowercase `w25` inside it does not satisfy the `W25` regex, and `pause` follows
  `v`, so `\bpause` does not match inside it. A retry or resume uses `…w25devpause2` (then `…3`) and fresh `_2` dirs.
- `pause_w25` and `tag_used` are shared with `w25` (l.721-726): a tag that opened a `w25` or `dev-w25` window is
  refused.
- **Tag hygiene (N71, binding):** only the generic form with the literal `<MMDD>` appears in a CC file, an evidence
  file, a commit message or any LOG line other than the pause line. No draft file holds the concrete tag (there is no
  `.pl_tmp`; §3.6 keeps it in `TAG`/`PL`). Post-run tokens: `OPS-<MMDD>c-w25dev-result`, `OPS-<MMDD>c-w25dev-resume`.

### 4.2 Window rules (the G-B quiet rule by default; v1.4 §4.2 with these changes)
- **From the pause line until the result line nobody appends to LOG.md.** `dev-w25` re-reads LOG.md (strict UTF-8)
  before every one of its 69 batches; a torn append, an EIO or a second tag line ends the window (FAULT, parts kept).
- Writers W-a..W-k as v1.4 §4.2, with:
  - W-b/W-c judges, panels, workflows: none run (B's and MT4's LOG writers wait too; PQ-D1);
  - W-e Gemini and W-f the other tool: closed by the PI (PQ-D3);
  - W-g other papers' laptop jobs: none (P11);
  - **W-h `gpu_backup` loops: none, and the window opens only when no rented machine is live** (the loop rsyncs to
    `/mnt/d`; PQ-D6);
  - **W-i `d_watch`: live from P0 (before staging) to after the resume line (N69);** after a WSL restart it is
    restarted (it writes only its own log and probe file);
  - W-k background agents: none live; each finishes and logs before P9.
- The watcher writes only `$S`; a PI E2 answer goes to `$S/pi_e2.txt`.
- **Proof:** `quiet_pre.txt` = `quiet_post.txt` (`cmp`, §3.8).
- **Worst case:** the window ends by itself at the 24 h stop; LOG.md stays quiet that long. On a hang it stays quiet
  until the PI acts (G10).

## 5. Preconditions (coordinator; any FAIL = no pause line)

Order: **P0 first, before staging** (and again inside P9); P16, P17 next; P4 then P21; P9 within 5 min before §3.6;
P22 last; then `pre.txt` is closed (§3.5); P14 runs inside §3.6. Every block below appends its own output and stderr
to `$PRE/pre.txt` (N68) and is run exactly as written; each starts with `. "$HOME/w25dev_env.sh"; cd "$R"`.

```sh
. "$HOME/w25dev_env.sh"; cd "$R"
# P0 (N69) d_watch live: run before staging and again inside P9; if the count is 0, start it with the commented line, wait 65 s, re-run the block
{ echo "== P0 $(date -u +%FT%TZ)"; echo "d_watch live: $(ps -eo pid,args | awk '($2 ~ /bash$/ && $3 ~ /d_watch\.sh$/) || $2 ~ /d_watch\.sh$/' | wc -l)"; [ -e "$HOME/.local/state/vsps/d_watch.log" ] && awk '/ FAIL$| RECOVERED$/{l=$0} END{print "last event:", l}' "$HOME/.local/state/vsps/d_watch.log" || echo "d_watch.log absent"; } >> "$PRE/pre.txt" 2>&1
# setsid -f /bin/bash "$HOME/.config/vsps/d_watch.sh" >/dev/null 2>&1; echo "d_watch started $(date -u +%FT%TZ)" >> "$PRE/pre.txt"
{ echo "== P1 $(date -u +%FT%TZ)"; for p in c_pvr.py gates.py c_pvr_run.py; do echo "$(sha256sum < scripts/c_pvr/$p | cut -c1-64) disk $p"; echo "$(git show HEAD:scripts/c_pvr/$p | sha256sum | cut -c1-64) HEAD $p"; done; } >> "$PRE/pre.txt" 2>&1
{ echo "== P2 $(date -u +%FT%TZ)"; timeout 120 sha256sum -c scripts/c_pvr/SHA256SUMS > "$PRE/p2.txt" 2>&1; echo "rc=$? OK=$(grep -c ': OK$' "$PRE/p2.txt")"; } >> "$PRE/pre.txt" 2>&1
# P3 after B0, and again right before P22
{ echo "== P3 $(date -u +%FT%TZ)"; git status --porcelain --ignored scripts/c_pvr data/splits/textcaps_train_ids.txt "$DOC"; for d in $DIRS; do find "$d" -maxdepth 1 \( -name __pycache__ -o -name '*.pyc' \); done; echo "(end P3)"; } >> "$PRE/pre.txt" 2>&1
# P4 one at a time (N68 exact env line; N85 timeout 300 s); HOME is scratch, so the sealed path resolves to scratch and nothing is mounted over it
[ ! -e "$P4S" ] && mkdir -m 700 "$P4S" "$P4S/home" "$P4S/tmp" || echo "P4 GUARD: $P4S exists" >> "$PRE/pre.txt"
{ echo "== P4 $(date -u +%FT%TZ)"; cd "$P4S/tmp"; for c in "$CV $R/scripts/c_pvr/c_pvr.py" "$FT $R/scripts/c_pvr/c_pvr_run.py" "$FT $R/scripts/c_pvr/c_pvr_run.py"; do set -- $c; echo "-- ${2##*/}"; t0=$(date +%s); timeout -k 10 300 env -i PATH=/usr/bin:/bin HOME="$P4S/home" TMPDIR="$P4S/tmp" VNCORENLP_DIR="$HOME/c_pvr_tools/vncorenlp" OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 unshare -rnm sh -c 'mount -t tmpfs tmpfs /dev/shm && exec "$@"' sh "$1" -I -B "$2" selftest; rc=$?; echo "rc=$rc $(( $(date +%s) - t0 )) s"; done; cd "$R"; } >> "$PRE/pre.txt" 2>&1
{ echo "== P5 $(date -u +%FT%TZ)"; git diff --stat cc90c96 HEAD -- scripts/c_pvr | tail -n 1; git diff --quiet c15c183 HEAD -- scripts/c_pvr && echo "c15c183..HEAD scripts/c_pvr: none"; } >> "$PRE/pre.txt" 2>&1
{ echo "== P6 $(date -u +%FT%TZ)"; git cat-file -t c15c183; echo "doc HEAD $(git show HEAD:"$DOC" | sha256sum | cut -c1-64)"; echo "doc disk $(sha256sum < "$DOC" | cut -c1-64)"; for t in 'CC-254 ' 'c-tvqa-pin' 'c-w25dev-staged' 'c-w25dev-bytecode'; do echo "$t $(grep -c -- "$t" "$L")"; done; } >> "$PRE/pre.txt" 2>&1
{ echo "== P7 $(date -u +%FT%TZ)"; sha256sum manuscript/prereg/2026-11-02_c_pvr_tier1/{c_pvr_owners.json,c_pvr_owner_feats.json,c_pvr_lists.json,w25_counts.json,ovqa_count_rule.json} manuscript/prereg/2026-10-27_c_en/{cen_memory_allowed,cen_coco_test,cen_nocaps_val}.tsv .session_backup/2026-11-02/b_pa1/b_pa1_owners.json data/splits/textcaps_train_ids.txt manuscript/prereg/2026-10-29_l1a/{l1a_lists.json,neardup.json} | cut -c1-8,65-; for a in '^w25 decide' '^w25 end' '^dev-w25 '; do echo "$a $(cut -f3 "$HOME/.vsps_sealed/c_pvr/ACCESS_LOG.tsv" | grep -c "$a")"; done; } >> "$PRE/pre.txt" 2>&1
{ echo "== P8 $(date -u +%FT%TZ)"; ( cd "$IN" && sha256sum -c --quiet "$PRE/in.sha256" ) && echo "IN 19 OK"; ls "$IN" | wc -l; stat -c '%a' "$IN"; df -T "$IN" | awk 'NR==2{print $2}'; for s in ktvic openviic vitextvqa_dev textcaps; do ( cd "$STG/$s" && sha256sum -c --quiet "$PRE/stage_$s.sha256" ) && echo "$s OK $(wc -l < "$PRE/stage_$s.sha256") files=$(ls "$STG/$s" | wc -l)"; done; stat -c '%a' "$STG"; df -T "$STG" | awk 'NR==2{print $2}'; tail -n 1 "$PRE/decode_out.txt"; sha256sum "$PRE"/stage_*.sha256 | cut -c1-8,65-; } >> "$PRE/pre.txt" 2>&1
{ echo "== P10 $(date -u +%FT%TZ)"; echo "FT $(readlink -f "$FT") $(sha256sum < "$(readlink -f "$FT")" | cut -c1-16)"; "$FT" -m pip freeze | sha256sum | cut -c1-16; "$FT" -m pip check; sha256sum < "$SSCD" | cut -c1-16; systemctl list-timers 'apt-daily*' --all --no-pager; systemctl is-active apt-daily.service apt-daily-upgrade.service; } >> "$PRE/pre.txt" 2>&1
{ echo "== P11 $(date -u +%FT%TZ)"; ps -eo pid,etime,args | grep -E 'rsync|c_pvr_run_mutants|pdflatex|xelatex|pandoc|git gc|_job\.sh|gpu_backup|stage_dev|decode_check|curl|multiprocessing\.(spawn|resource_tracker)' | grep -v grep | cut -c1-120; echo "(end P11)"; } >> "$PRE/pre.txt" 2>&1
# P11b (N11) no live rental: each machine token below has a later deleted/lost token; then record the ckey.vn instance list as text
{ echo "== P11b $(date -u +%FT%TZ)"; grep -nE 'OPS-[0-9]{4}[a-z0-9]*-?(rent|rented|rental|deleted|lost)\b' "$L" | cut -c1-110 | tail -n 12; echo "(end P11b)"; } >> "$PRE/pre.txt" 2>&1
# echo "ckey.vn live instances: <n> ($(date -u +%FT%TZ))" >> "$PRE/pre.txt"      # read from the provider panel; must be 0
{ echo "== P12 $(date -u +%FT%TZ)"; ls -d /dev/shm/c_pvr_w25 2>&1; [ -e /dev/shm/c_pvr_w25.lock ] && { flock -n /dev/shm/c_pvr_w25.lock true; echo "lock free rc=$?"; } || echo "lock absent"; ls manuscript/prereg/2026-11-02_c_pvr_tier1/dev_w25_out_ids.json manuscript/prereg/2026-11-02_c_pvr_tier1/dev_w25_counts.json 2>&1; echo "sem.mp $(ls /dev/shm | grep -c '^sem\.mp-')"; } >> "$PRE/pre.txt" 2>&1
{ echo "== P13 $(date -u +%FT%TZ)"; [ -f "$HOME/.config/vsps/gpu_backup.sh" ] && echo "gpu_backup.sh /dev/shm hits: $(grep -c /dev/shm "$HOME/.config/vsps/gpu_backup.sh")"; } >> "$PRE/pre.txt" 2>&1
```

**P15 (N83), once, after P12, outside any window:**
```sh
. "$HOME/w25dev_env.sh"; cd "$R"; NP=/dev/shm/c_pvr_nsprobe_$D0
PD=.session_backup/w25dev_nsprobe_$D0
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
    print("real W25 lock absent: dev-w25 creates it inside the namespace")
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
kill -TERM $NSPID; wait $NSPID; echo "TERM to a namespaced pid: rc=$?"; } >> "$PRE/pre.txt" 2>&1
```

**P16-P22 and P9 (P9 within 5 min before §3.6; P22 last):**
```sh
. "$HOME/w25dev_env.sh"; cd "$R"
PIID='<PI id of the window line>'
{ echo "== P16 $(date -u +%FT%TZ)"; case "$PIID" in ''|*'<'*) echo "P16 FAIL: PIID not filled";; *) echo "PI line: $(grep -cE "^[0-9T:-]+Z $PIID:" "$L")";; esac; } >> "$PRE/pre.txt" 2>&1
{ echo "== P17a $(date -u +%FT%TZ)"; "$HOME/.config/vsps/usage_check.sh"; } >> "$PRE/pre.txt" 2>&1
# ... 10 minutes later:
{ echo "== P17b $(date -u +%FT%TZ)"; "$HOME/.config/vsps/usage_check.sh"; } >> "$PRE/pre.txt" 2>&1
{ echo "== P18 $(date -u +%FT%TZ)"; ( cd "$PRE" && sha256sum in.sha256 stage_dev.py decode_check.py w25_watch.sh ); } >> "$PRE/pre.txt" 2>&1
{ echo "== P19 $(date -u +%FT%TZ)"; [ ! -e "$S" ] && echo "S absent"; } >> "$PRE/pre.txt" 2>&1
cat > "$PRE/RESUME.txt" <<EOF
Paper C dev W25 RESUME note (W25_DEV_RUN_DOC_v1_3 §5 P20), written $(date -u +%FT%TZ) right before the pause line
- Window state: OPENING. Pause line OPS-<MMDD>c-w25devpause next (§3.6); launch and watcher in the same call (AUTO=0, EXP=69).
- \$S: $S. Staged images: $STG. Checklist: $PRE.
- E-step reached: none at writing; watch \$S/watch.txt and \$S/ALERT.
- Freeze backstop: A (PI kills listed stuck workers), then B (PI runs wsl --shutdown) (W25_RUN_DOC_v1_4 §6A).
- The pause stays open until the result line (G10). Next LOG lines after the exit: OPS-<MMDD>c-w25dev-result, then OPS-<MMDD>c-w25dev-resume.
- After a WSL restart: no gpu_backup loop, no LOG writer, no /loop tick, no workflow until the resume line. Restart d_watch only.
EOF
{ echo "== P20 $(date -u +%FT%TZ)"; sha256sum "$PRE/RESUME.txt" | cut -c1-16; } >> "$PRE/pre.txt" 2>&1
# P21 (after P4): list only python processes of these kinds (pid ppid etime comm; no cmdline is printed)
{ echo "== P21 $(date -u +%FT%TZ)"; ps -eo pid=,ppid=,etime=,comm=,args= | awk '$4 ~ /^python/ && /c_pvr_run\.py|c_pvr\.py|c_pvr_run_mutants\.py|c_run_mut_scratch|multiprocessing\.(spawn|resource_tracker)/ {print $1, $2, $3, $4}'; echo "(end P21)"; } >> "$PRE/pre.txt" 2>&1
# only for a PID listed by P21, only before the pause line, and for a spawn worker or tracker only if its ppid is 1 (N60; P4 records no PID):
# p=<pid>; { echo "P21 signal $p $(date -u +%FT%TZ) wchan $(cat /proc/$p/wchan)"; kill -TERM "$p"; sleep 10; [ -e "/proc/$p" ] && kill -KILL "$p" && echo "KILL $p"; } >> "$PRE/pre.txt" 2>&1   # then re-run P11 and P21
# P9 (within 5 min before §3.6): (a) 9p; (b) = P0; (c) the LOG l.1405 write_new probe in a fresh dir; (d) = P2
{ echo "== P9 $(date -u +%FT%TZ)"; mount | grep ' /mnt/d ' | cut -c1-60; echo "d_watch live: $(ps -eo pid,args | awk '($2 ~ /bash$/ && $3 ~ /d_watch\.sh$/) || $2 ~ /d_watch\.sh$/' | wc -l)"; [ -e "$HOME/.local/state/vsps/d_watch.log" ] && awk '/ FAIL$| RECOVERED$/{l=$0} END{print "last event:", l}' "$HOME/.local/state/vsps/d_watch.log" || echo "d_watch.log absent"; PD=.session_backup/w25dev_probe_$D0; [ ! -e "$PD" ] && mkdir "$PD" && timeout 20 /usr/bin/python3 -I -B -c 'import hashlib, sys; from pathlib import Path; assert hashlib.sha256(open("scripts/c_pvr/gates.py", "rb").read()).hexdigest().startswith("3bced05e"); sys.path.insert(0, "scripts/c_pvr"); import gates as G; d = Path(sys.argv[1]); p = d / "p.json"; h = G.write_new(p, b"x\n", 0o444); assert p.read_bytes() == b"x\n"; p.unlink(); left = sorted(x.name for x in d.iterdir()); d.rmdir(); print("write_new", h[:16], "left", left, "PROBE PASS")' "$PD" || echo "P9c FAIL (or the probe dir existed)"; echo "P9d OK=$(timeout 120 sha256sum -c scripts/c_pvr/SHA256SUMS 2>&1 | grep -c ': OK$')"; } >> "$PRE/pre.txt" 2>&1
# P3 again here, then P22 last
{ echo "== P22 $(date -u +%FT%TZ)"; EXP=69; case $EXP in ''|*[!0-9]*) echo "EXP FAIL";; *) [ "$EXP" -ge 0 ] && [ "$EXP" -le 69 ] && echo "EXP=$EXP integer 0..69 OK";; esac; echo "ext4 free GB $(df --output=avail -B1G "$HOME" | tail -n 1)"; free -m | awk 'NR==2{print "mem available MB", $7}'; } >> "$PRE/pre.txt" 2>&1
sha256sum "$PRE/pre.txt"                           # pre.txt is closed here (§3.5); nothing appends to it again
```

| # | PASS |
|---|---|
| P0 | `d_watch live: ≥ 1` (if 0 at first, started by the commented line and its start time recorded); log absent, or its last event is not `FAIL` |
| P1 | 8f10bd60…, 3bced05e…, 4c0f36b8…, each disk = HEAD |
| P2 | `rc=0 OK=18` |
| P3 | only `(end P3)`, both times |
| P4 | `selftest ok … c_pvr.py 8f10bd60…`, then `selftest ok … c_pvr_run.py 4c0f36b8…` twice; each `rc=0` and < 300 s; the times are the record (about 5 s and about 65 s; N85). A timeout is a FAIL and N28 evidence: the PI is told before any window |
| P5 | `3 files changed, 533 insertions(+), 52 deletions(-)`; `none` |
| P6 | `commit`; doc HEAD = doc disk = the GO'd sha; each token count ≥ 1 |
| P7 | 0cf330d3, 8f707edd, edb07fbb, 72ae5ad3, c7136a5f, 175907e2, 67555b28, 6add90eb, ae4b6630, 2da2b395, ac5ed047, fa676be1; `^w25 decide 1`, `^w25 end 1`, `^dev-w25  0` |
| P8 | `IN 19 OK`, 19, 700, ext4; four `OK` lines with 2,192 / 8,377 / 1,676 / 21,953 and equal `files=`; 700; ext4; `DECODE PASS`; the manifest shas = the staged LOG line |
| P9 | 9p; `d_watch live: ≥ 1`, no FAIL as last event; `write_new 73cb3858a687a849 left [] PROBE PASS`; `P9d OK=18` |
| P10 | FT → /usr/bin/python3.12 e50d468e…; pip freeze 1a639a50…; `No broken requirements found.`; SSCD 9f26bd4c…; neither apt timer due within 6 h + 90 min (the live reading governs, G8); both `inactive` |
| P11 | only `(end P11)` |
| P11b | every rental/rented token listed has a later deleted or lost token for the same machine, and the recorded `ckey.vn live instances: 0` (PQ-D6; N11) |
| P12 | the dir: `No such file or directory`; `lock free rc=0` or `lock absent`; both outputs `No such file`; the `sem.mp` count recorded (not residue) |
| P13 | `gpu_backup.sh /dev/shm hits: 0` |
| P14 | inside §3.6, on the final string (N70): all True |
| P15 | `environ readable from outside: 1`; `uid inside 0`; `interfaces lo only: True` (the gates.py l.2192 form); `real W25 lock: flock OK` (or `absent`); `tmpfs dir mode 0o700 uid match True`; `LOG strict UTF-8 read OK`; `netns write_new 73cb3858a687a849 left [] PASS`; `rc=143`. Else `NS=''` and the failed line is the reason (N83) |
| P16 | `PI line: 1` (PIID filled): the PI line answers PQ-D1 to PQ-D8 and is written before P9 |
| P17 | each reading: data age ≤ 120 s; 5-hour ≥ 15% and 7-day ≥ 10% remaining; ≥ 90 min headroom at the measured rate for the coordinator's own work (launch, a few watch reads, §3.8). The run itself uses no Claude usage; a 3-6 h window outlasting the headroom is bounded by the 24 h code stop and the E2 backstop, and the pause stays open until the result line (CC-257 N12). five_hour None passes on 7-day ≥ 10% plus the P16 line only if PQ-D7 = YES (fails closed, G7) |
| P18 | the four shas of §3.3 |
| P19 | `S absent` |
| P20 | RESUME.txt written; sha recorded |
| P21 | only `(end P21)`; else the signal rule in the comment, then P11 and P21 again |
| P22 | `EXP=69 integer 0..69 OK`; ext4 free ≥ 20 GB; mem available ≥ 4,000 MB (decide's peak is well under 2 GB, §10) |
- P15 PASS: see the table above. The probe removes only the two names it created (exclusive create); it opens the real
  W25 lock without creating it and releases it at once.
- Why `-n` and not `-m`: a mount namespace would give a private /dev/shm and break the shared W25 lock and tmpfs dir
  (N82). Why it should hold: the tmpfs dir is made inside the namespace, so `st_uid == getuid()` (both 0 there); the
  lock is the same file; `kill` and `/proc/$PY/environ` from outside work for a namespace the same user owns (the
  probe checks both).
- The probe holds no address literal (CC-257 W4): the no-network check is the interface list, as in gates.py l.2192.
  The `write_new` probe checks that `/mnt/d` writes (the outputs) work from inside the namespace (N10).
- If any line fails: `NS=''`. `no_sockets()` (main l.2521) still blocks sockets in the main process; spawned workers
  open none (they hash local files). The result line states the failed probe line (N83).

## 6. Stall, wall and freeze plan (v1.4 §6 and §6A by reference, with these deltas)

- **E-ladder:** v1.4 §6 E1-E4 unchanged, with `$PY` = the `dev-w25` python and `EXP = 69`. No SIGKILL by any agent; no
  agent runs `wsl --shutdown`. `AUTO=0` (D-R7).
- **§6A applies verbatim:** C (spawn) is in force (same `main` statement, l.2487); A then B stay the backstop; the H4
  `hang.txt` line and the per-PID worker kill line are unchanged; `sem.mp-*` count only.
- **Exposure, stated:** a first window opens **69** `Pool(4)` (one per batch) against the 24 the W25 window opened
  with no hang. The hang rate stays unmeasured.
- **H3 is cleaner here:** there is no network phase, so a flat CPU (< 100 ticks in 15 min) points to a freeze, not a
  network wait. H3 stays a record only.
- **Pre-start window:** `dev_pre` runs before the 'dev-w25 start' row (no Pool there; it loads caches, rebuilds lists,
  checks 34,198 staged names). A SIGTERM there consumes nothing.

## 7. Exit branches and resume

v1.4 §7 applies with `w25` read as `dev-w25` in every row and these specifics:
- Rows keyed on `cut -f3` actions `dev-w25 start / decide / end / abort`; the 2 outputs `dev_w25_out_ids.json`,
  `dev_w25_counts.json` (`DEV_OUTS`, counts written last).
- **FAULT lost > cap:** the cap is 0 for every staged set. After a PASS decode check (§3.4) this means a file changed
  or a reader differs; full panel at 85.
- **Some outputs present but no 'dev-w25 decide' row:** no rerun (`dev_pre` refuses); full panel at 85.
- **Resume = the same run:** same RUN, `$IN`, `$STG` (re-checked by P8), owners, feats; parts in the sealed
  `dev_w25/parts` verified and skipped; **the 24 h deadline is fixed at the first start** (`dev_w25/deadline`); new tag
  `…w25devpause2`, fresh `$S` (`w25devrun_<D0>_2`); P0-P22 with v1.4 P12b's resume form (`^dev-w25 decide` 0,
  `^dev-w25 end` 0, `^dev-w25 start` = earlier windows; torn-row check). EXP on a resume = 69 minus the part lines of
  earlier windows. A one-judge read of the cause first.
- **'dev-w25 start' + 'dev-w25 abort' with a FAULT inside `dev_decide`, and neither output present** (CC-257 N13): the
  decide wrote nothing, so no look was taken. One-judge read of the cause, then a resume (parts kept). With any output
  present, the "no rerun" row above applies.
- A second abort or hang of the same class goes to the PI.

## 8. Outputs, the S7 read and the commit

### 8.1 Outputs
| output | where | goes to |
|---|---|---|
| `dev_w25_counts.json` (0o444; label, rule, run/code/owners/feats/lists/SSCD shas, `w25_counts_sha256`, `w25_run_sha256`, featured, queries, per datastore and pool: n / flagged / flagged_by_set / out / kept, `d_en_no_feature_row`, `nocaps_val_xm3600_by_id`, `o_b` note, `t2pool_note`) | `manuscript/prereg/2026-11-02_c_pvr_tier1/` | S7 read, commit |
| `dev_w25_out_ids.json` (per datastore and pool: the sorted ids that leave; no owner or reason column) | same | S7 read, commit |
| parts `<set>_NNNN.npz` (69) and `deadline` | `~/.vsps_sealed/c_pvr/dev_w25/` (0400) | never committed or copied; never listed by an agent |
| ACCESS_LOG rows; `w25_deletions.log` lines | `~/.vsps_sealed/c_pvr/` | mirrored by action field and tail only |
| `$PRE`, `$S` evidence; manifests; ids lists | ext4 | copies to `.session_backup/<date>/c_w25dev/` with SHA256SUMS; the staged images never leave `$STG` |

### 8.2 S7 result read (N81, BLOCKING for the S7 GO; one judge, reversible 85)
The judge asserts, from `dev_w25_counts.json`:
- `nocaps_val_xm3600_by_id` = **43** (RULE l.19; §4.4);
- `d_en_no_feature_row` = **2** (N88);
- `queries` = xm3600 3,600; nocaps_val 4,500; ktvic_test 558; openviic_test 2,001; kt_c 3,907; nocaps_test 10,496;
  ovqa_dev 1,070; vitextvqa_dev 1,676; t_a 1,070;
- `featured` = dvi_ktvic 2,192; dvi_openviic 8,377; vitextvqa_dev 1,676; textcaps 21,953 (= the staged counts);
- datastore `n` = d_vi 10,569; d_en 80,083; d_tc 20,883. t2pool `n` = nocaps_val 4,500; ktvic_test_confirm 272;
  openviic_test_confirm 981;
- shas: run 4c0f36b8, `w25_counts_sha256` 72ae5ad3, `w25_run_sha256` 290a75dc, lists edb07fbb, owners 0cf330d3,
  feats 8f707edd, SSCD 9f26bd4c, `code_sha256` = CODE; `rule` = RULE_TEXT (289c0a59);
- the §3.8 record: quiet held, rows in the expected order, trap line last, CODE re-hash 10 bad [], staged bytes
  unchanged, rc 0, stderr 0 bytes;
- the S7 record cites the drafting-time hand row `OPS-1105c-sealed-handrow` (LOG l.1570; G5);
- the S7 record (result line and the S7 CC) carries the corrected deferred-owner reason "textvqa_textcaps_val: images
  inside the pinned TextVQA archive, no val id list held" (E3), and states that no val member was extracted, decoded
  or featurized.
**Any departure, FAULT, abort, hang or Stop goes to a full panel at 85** (PI-1103ad).

### 8.3 Result commit and the datastore pin line
- After the S7 GO, the gatekeeper commits exactly the 2 outputs (ids and counts only; public image ids; no gold; no
  reason column), each re-hashed against its staged blob, with the NGRAM scan (`ngram_scan_cen.py`) PASS on both,
  output kept beside the snapshot. No AI-attribution line; no host, IP, port or PI address; no concrete tag.
- Then one LOG line `OPS-<MMDD>c-datastores` (coordinator): the final D-VI / D-EN / D-TC sizes and the shas of the
  three kept-id files derived from `dev_w25_out_ids.json` (datastore − out) and the tier-2 pool sizes. **Removal counts
  stay internal** (PI-1101o; CC-249 Ruling 4): never in a paper, cover letter or talk.
- These id files ARE the tier-1 datastores (N80): S11-S15 decode against them and nothing else.

## 9. O_B, D-EN and shared paths (N80, N88, N82, N86)

**N80: what leaving O_B out means (CC-254 Ruling 1.4).**
- `dev-w25` is one look and excludes O_B, so its D-VI / D-EN / D-TC id files are the tier-1 datastores. Nothing about
  O_B can be added to this run later.
- C_NEXT_STEPS §3 item 5 "O_B yields to OpenViVQA dev … and to ViTextVQA dev … by W25. This is computed in S6" is
  therefore **void**. It moves to a later step under the tier-2 prereg (IRREVERSIBLE, full panel), which must first
  license the O_B file-name read (§4.3 NB-OVQALOST: "The train file has the same limit until the tier-2 prereg
  licenses the O_B read") and then choose, **before any O_B pixel moves**:
  - **(a) query side (recommended):** O_B images with a RULE §3 match in a datastore or in a tier-1 dev set leave O_B,
    counted only. The datastores stay frozen as pinned in §8.3. Needs a §7.4 wording amendment, because §7.4 says the
    datastore loses every query image's near-duplicates.
  - **(b) datastore side, §7.4 as written:** the tier-2 datastore = the tier-1 datastore minus O_B matches, with the
    configuration change disclosed beside the tier-2 result.
  - Why (a): the tier-1 frozen config is then also the tier-2 config; (b) changes the retrieval pool between tiers.
- O_B × D-VI and the O_B pool count wait for that step. The `o_b` field of `dev_w25_counts.json` says so (O_B_NOTE).
  N86: that string cites §4.1 and §4.3; the operative basis is §4.3 alone. No code change (same-sha rule).

**N88: the 2 D-EN ids without a feature row** leave D-EN and are counted (`d_en_no_feature_row`). This is a pre-set
code rule (`rows(…, missing_ok=True)` → `extra`), not registered text. **Disclosed rule:** an image whose near-duplicate
status cannot be checked is treated as a lost image and leaves the datastore. It is conservative (a smaller D-EN, never
a leak). The count is internal (PI-1101o).

**N82: shared paths, expected.** `dev-w25` shares the W25 lock `/dev/shm/c_pvr_w25.lock`, the tmpfs dir
`/dev/shm/c_pvr_w25`, and `w25_deletions.log`, and writes its projection row as `w25 projection`. Its parts and
deadline are separate (`dev_w25/`). So P12 checks the shared lock and dir, and §3.8 expects one more `w25 projection`
row and a new trap line.

## 10. Time estimate (laptop CPU; Vietnam time for the PI)

| phase | work | estimate |
|---|---|---|
| T2 download | the archive, about 7.07 GB (about 6.6 GiB) [HF mirror size; HEAD governs] | 10-60 min [est.; bandwidth] |
| staging | /mnt/d: 2,192 + 8,377 + 1,520 small files (about 0.3 + 2.3 + 0.5 GB [est. from `du` shares of the source dirs: ktvic 622 MB / 4,327 files, openviic 3,702 MB / 13,300]) plus one 5.58 GB sequential zip hash; ext4: about 6.2 GB of train images out of the TextVQA archive [est.] | 30-60 min [est.] |
| decode check | 34,198 × (`_features` + `_mirror_hashes`), one process | 20-35 min [est.] |
| B0, P0-P22 | incl. P4 about 5 + 65 + 65 s | about 20 min |
| **window** | `dev_pre` (lists rebuild, 19 caches incl. the 251 MB D-EN cache) about 5-10 min [est.]; **34,198 images / 2.58 img/s = 13,255 s = 3.7 h** (rate measured in the W25 window: 11,566 images in about 74.7 min, CC-252 Ruling 1; it included the NoCaps fetch, and here there is none, so it is conservative for fetch time but the image sizes differ); decide: about 3.2e9 query-datastore pairs vs 1.4e9 in W25's decide (about 70 s), so about 3-6 min [est.] | **about 4 h** (range 3-6 h [est.]) |
| projection | after batch 1 (512 KTVIC images, about 3-4 min) | must project < 24 h, else `Stop` |
| memory in decide | `W.rule(datastore, query)`: `build_memory.near` and `w25.sscd_any` both work in chunks of 512 datastore rows (build_memory l.83-96, w25 l.214-220). The largest call is D-EN 80,083 × NoCaps test 10,496 (8.4e8 pairs): per chunk about 22 MB of SSCD similarities, about 43 MB per uint64 XOR before `bitwise_count`, and a 5 MB boolean sha match. Loaded features: D-EN about 164 MB of SSCD rows, the queries and staged sets about 130 MB | peak well under 2 GB [est.]; P22 floor 4,000 MB available |

Example: pause line 20:00 VN, end about 00:00 VN. The registered stop is 24 h after the first start (20:00 VN the
next day). Disk: about 16 GB new on ext4 (archive + staged copy) of 880 GB free at drafting; nothing goes to /dev/shm
(11 GB tmpfs) in this run.

## 11. Carried items

| item | where closed |
|---|---|
| **N77** TextCaps pixel pin | §3.2: one archive, T0, T0b (anchor named first), T1-T3, pin line, then the one-judge record check before staging; same bytes serve T_A on HC-n (N96); honest fallback F-a/F-b. **Departure stated (§3.2):** pin line before the read, because the values cannot exist before the download; the record check is the CC-249 form |
| **N78** ViTextVQA 156 | §3.3: by member name from zip 39420475 (re-hashed in full first); 1,520 re-hashed to ac5ed047; 156 trust-on-extract, disclosed |
| **N79** manifests, decode check, space, chunked copy | §3.3, §3.4, P8, P22, T1; d_watch live and no FAIL as the last d_watch.log event are checked by the staging command (E1, G3); the step-6 GO by the tested awk gate (G1); `feats_memory.npz` caf4a621 in `$IN` (§3.1). **Departure stated (§3.4):** the 4 manifest shas live in the staged and pause LOG lines, not in this file (the TextCaps manifest cannot exist before the download); P8 checks them |
| **N80** O_B | §9; §8.3 |
| **N81** S7 expected values | §8.2 |
| **N82** shared lock/tmpfs/log | §9, §3.8, P12 |
| **N83** no-network launch | §3.6 `NS`, P15 |
| **N85** selftest time | P4: `timeout -k 10 300`, times recorded |
| **N86** O_B_NOTE basis | §9 (record only; same-sha rule) |
| **N87** no traversal of `/` or `$HOME` | §2 (a v1.1 drafting breach is disclosed in §15; hand row `OPS-1105c-sealed-handrow`) |
| **N88** 2 D-EN ids | §9 |
| CC-252 **N68** exact P4 env line; stderr kept | P4 (`VNCORENLP_DIR="$HOME/c_pvr_tools/vncorenlp"` after `env -i`); §5 block form |
| CC-252 **N69** d_watch at the start | P0 at step 4, into the `$PRE` made there (E1), before any /mnt/d bulk read; re-checked (count and last event, G3) by the staging command and in P9 |
| CC-252 **N70** P14 two-field exception | removed: pre.txt closed first, P14 tests the final string (§3.6) |
| CC-252 **N71** `.pl_tmp` | no draft file; `TAG`/`PL` in one shell call (§3.6, §4.1) |
| CC-252 **N72** EXP record | P22 and the watch.txt line-2 check (§3.6, §3.7) |
| CC-252 **N74** clock steps | stamps across files are not ordering evidence at the 1-2 s scale; stall/wall margins are minutes |
| v1.4 N22, N28/N50, N47, N48, N52-N55, N58-N60 | by reference (§6, P21) |

## 12. Rulings needed (one judge, reversible 85)

| # | ruling | recommended | default |
|---|---|---|---|
| D-R1 | this file as the S5 run document (§2-§8) | GO | the window does not open |
| D-R2 | TextCaps pixels = the official TextVQA train/val archive by T0, T0b, T1-T3 (TOFU sha, anchor named before T2); values checked by a one-judge record read of the pin line before staging (the stated N77 departure); fallback F-a | YES | F-a: S6 waits |
| D-R3 | staging by `stage_dev.py` 5b2258ed (ids by `build_lists`, kept images only, per-file manifests) and the decode check `decode_check.py` 24175315 as preconditions; manifest shas pinned in the staged and pause LOG lines (the stated N79 departure) | YES | the window does not open |
| D-R4 | the 156 ViTextVQA images: trust-on-extract under zip 39420475 (no per-file pin exists) | YES | the window does not open |
| D-R5 | launch under `unshare -rn` if P15 passes, else without, reason recorded (N83) | YES | without, as W25 ran |
| D-R6 | LOG quiet = the G-B rule (§4.2); window only with no live rental | YES | same |
| D-R7 | watcher `AUTO=0` (as the W25 window ran; the coordinator watches) | `AUTO=0` | `AUTO=0` |
| D-R8 | registration: one gatekeeper commit of exactly this file before staging, byte-equal to the GO'd sha, NGRAM PASS, no concrete tag | YES | same |
| D-R9 | N80 recorded; (a) recommended to the tier-2 prereg | YES | the tier-2 prereg chooses |
| D-R10 | N88 disclosed rule | YES | same |
| D-R11 | S7 asserts §8.2; result commit §8.3 | YES | same |
| D-R12 | the val-images rules (i)-(iv) of §3.2: no val id list, no namelist, no val member extracted/decoded/featurized; bytes inside the pinned archive are not arrival; corrected reason in the pin line and the S7 record; owners json unchanged | YES | no download (F-a) |
| D-R13 | code freeze (§1) from registration to the S7 result commit | YES | same |

## 13. PI window questions (Vietnam time; each with a recommendation and a default)

| # | question | recommended | default |
|---|---|---|---|
| PQ-D1 | May the laptop run C's dev-set W25 window once, about 4 h (expected end about 4 h after start, e.g. 20:00 → 00:00 VN), on an evening after this file's GO? Worst case is the registered 24 h stop. **During the window no paper (A, B, C) writes to the LOG and no other laptop job runs.** | YES | the window does not open |
| PQ-D2 | For the window: laptop on mains power, sleep off, lid open? | YES (confirm on the day) | the window does not open |
| PQ-D3 | Gemini and the other tool closed for the whole window? | YES | the window does not open |
| PQ-D4 | Windows Update restart deferred until the window + 1 h? | YES | the window does not open |
| PQ-D5 | May the laptop download the public TextVQA train/val image archive (about 7.07 GB, about 6.6 GiB; it holds the TextCaps training images) from the dataset's official host, kept only on the WSL disk (never drive D, never a backup), so that C's English scene-text datastore can be cleaned and the same images later used for T_A? **The archive also holds the TextVQA/TextCaps validation images; they come with the file but are never extracted, opened or used**, and they leave with the archive when it is deleted after tier 1. Without the download, C's tier 1 cannot start (§3.2 fallback). | YES | tier 1 waits (F-a); no other source is used |
| PQ-D6 | The 30-min GPU backup copies to drive D, which the window must keep quiet. Open the window only when no rented machine (B's or C's) is live? | YES: schedule the window between rentals | the window waits until no rental is live |
| PQ-D7 | If the 5-hour usage field reads None at P17, may the window open on 7-day ≥ 10% plus your line (as PI-1104c allowed for W25)? | YES | wait for a numeric reading |
| PQ-D8 | For this roughly 4 h evening window, keep the watcher in alert-only mode (`AUTO=0`: it warns, and the coordinator sends the single stop signal by hand)? The 24 h stop in the code and your E2 backstop bound the risk. | YES, keep `AUTO=0` | `AUTO=0` |

Not asked (on record): the hang backstop A then B (PI-1104c PQ5); the 24 h stop is registered; if it fires, the parts
are kept and a one-judge read precedes any next step.

## 14. Touches during drafting (`date -u` 2026-11-05 about 05:00-05:50Z)
- **Read:** the sources at the top. Code text only.
- **Read, fields only:** `l1a_lists.json` top-level keys and `dev.image_sha256` (file → sha); `neardup.json` keys and
  `flagged_dev_files` names/criteria; `ViTextVQA_dev.json` `images` id/filename (json.load parsed the file into memory;
  no annotation field was accessed or printed, CC-245r2 precedent); `c_pvr_owner_feats.json` owner/cache/sha/n;
  `c_pvr_lists.json` d_vi counts, halves, `vitextvqa_dev_images`, `d_tc_images_before_w25`, len(`t_a_ids`).
- **Hashed:** the 6 `$IN/of_*.npz` (= manifest); the small pinned inputs of P7 (all equal their pins);
  `ngram_scan_cen.py`.
- **Listed (names, sizes, counts only):** `$IN`; `data/datasets/` and the ktvic/openviic/l1a image dirs (`du -s`, file
  count); `$HOME/c_pvr_tc_d`, `$HOME/c_pvr_tc_x`; `df` of `$HOME`, `/dev/shm`, `/mnt/d`; `ps` for d_watch and
  gpu_backup (neither was live at drafting, so P0 will start d_watch).
- **Scratch:** the three helper files were drafted in `/tmp/w25dev_draft_1105` to take their shas, and re-extracted
  from this file by the §3.3 marker command into `/tmp/w25dev_extract_1105b`: byte-equal (8633f55d, a8dd6d31,
  9507fbe7). One `import gates` check with `/usr/bin/python3 -I -B` (the `STAMP` regex; no file written, no bytecode).
- **Code read for §10:** `build_memory.near` l.83-96 (chunked) and `match_openviic.hamming`.
- **Not touched:** `~/.vsps_sealed` and everything under it (not opened, listed or statted); ACCESS_LOG; /dev/shm
  contents; any zip member; any NoCaps, TextCaps or Open Images caption or label; any OpenViVQA json;
  `gb_intermediate.json`.
- Nothing was run (no c_pvr command), downloaded or committed.

## 15. Touches during v1.1 drafting (`date -u` 2026-11-05 about 09:25-09:34Z)
- **Read:** CC-257.txt in full; the panel journal `wf_2ef57176-1db/journal.jsonl` by `grep` for the anchor, size and
  probe items only; gates.py l.2186-2194; c_pvr_run.py l.160-170 and l.255-258; CC-245 l.146; CC-247 l.39, l.78; LOG
  by `grep` for rental/delete tokens; v1 (this file's base) by line ranges.
- **Scratch:** the two changed helper files were drafted in `/tmp/w25dev_v11_1105` and re-extracted from this file
  by the §3.3 marker command: byte-equal (stage_dev.py 5b2258ed, decode_check.py 24175315, in.sha256 8633f55d).
- **N87 breach, disclosed (CC-243 R7 / CC-247 N24 precedent applies).** To locate the panel journal, the drafter ran
  `find / -path '*wf_2ef57176-1db/journal.jsonl' -not -path '/proc/*' -not -path "$HOME/.vsps_sealed/*"` at about
  09:27Z. `-not -path` filters output but does **not** prune, so the traversal very likely read the directory entries
  of `~/.vsps_sealed` (names and stat metadata only; no file content was opened or printed; the command printed
  nothing before it was stopped by the drafter after about 2 min). This is the same class as the CC-254 N87 incident.
  The drafter did not touch ACCESS_LOG; the coordinator wrote the hand row `OPS-1105c-sealed-handrow` (LOG l.1570,
  10:15:29Z) per that precedent. The journal was then
  found by listing one named path under `~/.claude/projects/`.
- **Not touched otherwise:** ACCESS_LOG; /dev/shm contents; any zip member; any NoCaps, TextCaps or Open Images
  caption or label; any OpenViVQA json; `gb_intermediate.json`. v1 afde0323 is unchanged.
- Nothing was run (no c_pvr command, no helper script), downloaded or committed.

## 16. Touches during v1.2 drafting (`date -u` 2026-11-05 about 10:40-10:55Z)
- **Read:** CC-257r2.txt in full; LOG.md by `awk`/`grep` only (the gate test of §3.3; the P11b token test; the hand-row
  line number); v1.1 by line ranges.
- **Ran (read-only):** the §3.3 awk gate for the eight ids of the test table; the widened P11b regex. Nothing else.
- **Not touched:** `~/.vsps_sealed` (no `find`, `du` or `ls -R` over `/` or `$HOME`); ACCESS_LOG; any archive member;
  any caption or label. v1 afde0323 and v1.1 2d3ecc2c are unchanged. Nothing run, downloaded or committed.
