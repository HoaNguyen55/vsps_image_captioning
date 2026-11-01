# C-PVR-T1: tier-1 DEV-EXPLORE prereg for Paper C ("Verify Before You Borrow: Proposition-Verified Retrieval for Vietnamese Image Captioning", target ACM TALLIP)

Status: **v1.2 DRAFT for CC-220r3 full panel (final round) (irreversible, bar 92), not registered, not committed.**
v1.2 answers CC-220r2 (diff read, round 2/3, NEXT_ROUND; `.session_backup/2026-10-13/decisions/CC-220r2.txt`), the read of
v1.1); v1.1 answered CC-220 (round 1/3, NEXT_ROUND, median 87). v1 (`PREREG_DRAFT.md`, sha256 `fefccf22`) and
v1.1 (`PREREG_DRAFT_v1_1.md`, sha256 `8203ca11`) are kept byte-unchanged as **records only**.
Written 2026-11-01T22:24:34Z (`date -u`, at the end of the v1.2 edit; NB-RESTAMP). v1 drafting began 2026-11-01T17:56:28Z.
HEAD at drafting: `d68b1e7`. **These bytes are final for the round-3 read:** nobody restamps or edits this file at
registration; the gatekeeper commits it byte-equal to the judge-read sha (CC-218, CC-217r3), and the commit line
governs this DRAFT status line (CC-209c).
**Licence.** CC-219r3 (GO 92, `.session_backup/2026-10-13/decisions/CC-219r3.txt` sha256 `8c5bc929`) licenses
**drafting only** (CC-219r3 Ruling 4, l.44). Nothing here has run. No rental, decode, G-A/G-B/G-C run, NoCaps or Open
Images label read, or NoCaps-test pixel download happens before this file gets its own GO at >= 92 and a gatekeeper
commit. Registration = that commit.
**Direction implemented:** `manuscript/directions/C_DIRECTION_v4_1_2026-11-02.md`, committed in d68b1e7, sha256
`8334cf5d` (= the judge-read 7ebba35b plus the CC-219r3 NB6/N18 wording edits; commit message of d68b1e7). v4.1 wins over
v4 (6cf5cb5f) and v3 (99dbe46b). Where v4.1 and a CC ruling disagree, the ruling governs and the override is stated
(section 13). Ledger: `manuscript/directions/PORTFOLIO_3Y_2026-10-29.md` at HEAD, blob sha256 `910ab3bf` (§2.3).
Label on every output: `TIER 1 / DEV-EXPLORE (C-PVR-T1)`. Every estimate below is AI opinion, marked [est.]. Every
count cites its file and line. Values this draft proposes (no source; the panel fixes them) are marked [proposal].
Code (written after GO; CPU selftest before any GPU step): `scripts/c_pvr/c_pvr.py` (subcommands below),
`scripts/c_pvr/gates.py` (G-A, G-B, G-C2; pinned by sha before it runs), `scripts/c_pvr/test_c_pvr.py` (CPU selftest,
no weights, no data, every socket raises), `scripts/c_pvr/c_pvr_job.sh` (GPU block), `scripts/c_pvr/SHA256SUMS`.

## CC-220r2 closure table (round 2 → v1.2)

| item (CC-220r2 line) | what CC-220r2 asked | where closed in v1.2 |
|---|---|---|
| N-B1 (i) lost vs FAULT (l.123-130) | one classification, stated as an amendment of CC-220 B3's 404 clause; option (a): any exception after get's three tries = lost under the cap; "not a JPEG body", "redirected", "status N" = FAULT | §8.1 (new, the amendment); §5.6 points to it |
| N-B1 (ii) tier-3 gap + disclosure (l.131-133) | lost images leave P_obj^VI, R_obj^VI and the proxy at every tier (count only); disclose that > 10 departs from RULE l.50's 0-lost rule for KV/UT | §7.2 rule 3; §8.1 |
| N-B2 cap vs default (l.134-138) | cap = min(⌈1.25×P1⌉, 37) if Q-cost = YES, else 20; arms cut in 5.1 order; PI decides if it still does not fit | §10.1; §14 Q-cost |
| NB-RESTAMP (l.140-142) | restamp in v1.2; strike registration-time restamp | header; §16 |
| NB-V1COMMIT (l.143-145) | v1.2 (by sha) is the sole registered prereg; v1, v1.1 records only | header; §16 |
| NB-MD5 (l.146) | full-stream md5 also vs on-disk `full-{val,test}.md5` | §9.6 |
| NB-GBTENANCY (l.147) | §8 tenancy steps cover the G-B window | §8.2 (tenancy, now for W25 and G-B); §9.6 |
| NB-OVQALOST (l.148-151) | OpenViVQA lost/FAULT rule; named custody path for the 3 json files, never under data/ or a backup; keys and lengths only until the tier-3 freeze | §4.3; §8.1 |
| NB-SHAREFUSE (l.152) | C's fetch loop carries w25.fetch's XM3600 sha-refuse backstop | §8.1 |
| NB-STATE (l.153) | STATE C row refreshed after GO (coordinator) | §12 (stated coordinator obligation) |

## v1.2 changes (item → section)

| item | section |
|---|---|
| status line, WRITTEN stamp, v1/v1.1 records only, no registration-time restamp | header |
| CC-220r2 closure table; this table; CC-220 table rows B3, NB-LOST, NB-CAP, NB-STAMP updated | top |
| N-B1: amendment of CC-220 B3's 404 clause, fetch outcome classes, lost cap and its disclosure, OpenViVQA lost rule, XM3600 sha-refuse backstop | §8.1 (new) |
| tenancy steps 1-5 extended to the G-B window | §8.2, §9.6 |
| subsection heading for the W25 stop, M1 host and alternatives (no rule change) | §8.3 |
| guard G made an explicit PASS condition at tier 2 and tier 3 (consistency with B1) | §5.3 item 5, §5.4 |
| §9.5 placed before §9.6 (order only); PINS references named PINS-A / PINS-B | §9, §0, §3.4, §6 |
| §5.6 lost bullet points to §8.1 (one rule, stated once) | §5.6 |
| lost images leave the local metrics at every tier | §7.2 rule 3 |
| OpenViVQA json custody path and read limits | §4.3 |
| NB-MD5 | §9.6 |
| N-B2 conditional cap | §10.1, §14 Q-cost |
| NB-STATE | §12 |
| NB-V1COMMIT, NB-RESTAMP | §16 |

## CC-220 closure table (round 1 → v1.1; rows marked v1.2 were changed by CC-220r2)

| item (CC-220 line) | what CC-220 asked | where closed in v1.1 |
|---|---|---|
| B1 P(PASS) = registered PASS (l.51) | a replicate passes iff 5.4 (1), (2), (3) AND the 5.7(b) VI-script guard (>= 0.95) for both PVR and A8 | §5.6 P(PASS) bullet |
| B2 test-gold CSV custody (l.52) | stream-filter to `ga_remaining_ids.txt` (fetch.sh pattern), or /dev/shm only and unlink after the one read; never /mnt/d, data/ or a backup; sha256 + md5 logged; deletion in ACCESS_LOG.tsv; later subcommands refuse oidv7-*-annotations paths; re-download = own irreversible ruling | §9.6 (new); §3.1 Gold; §9.2 G-B row; §11 |
| B3 OI-test fetch URL (l.53) | separate OI `test/` URL template pinned in PINS; W25 functions unchanged; every id in the G-A OI-test list; 404 / non-JPEG = FAULT, no substitute | §8.1; §9.1 step 5. **v1.2:** the 404 clause is amended (CC-220r2 N-B1; §8.1) |
| B4 laptop tenancy enforced (l.54) | coordinator pause LOG line before `w25`; flock re-checked every batch; abort + trap-delete on a foreign `*_job.sh`; /dev/shm/c_pvr_w25 mode 0700; gpu_backup loops the only concurrent processes, never reading it; one shared uid = procedural isolation | §8.2 (v1.2: also the G-B window) |
| NB-OVQA (l.57, BINDING) | HF revision + 3 json sha256s; assert 1,070 / 3,545, else FAULT; strike "else disclosed missing" | §4.3; §13 O8 |
| NB-CAP (l.58, BINDING) | one M1 re-base in PINS from throughput only; ceiling <= 350k VND ≈ <= 37 GPU-h at 9,282 VND/h; 20 GPU-h on M1 ≈ 186k VND | §10.1, §10.2. **v1.2:** reopened as N-B2 (conditional on Q-cost) |
| NB-NOVAR (l.59, BINDING) | no variant passes δ_C/δ_R -> STOP; δ_C test form at tier 1 | §6.3 |
| NB-W25STOP (l.60, BINDING) | projected W25 runtime vs a pre-fixed wall-clock cap after batch 1; exceeded -> stop, Q-custody to PI | §8.3 |
| NB-LOST (l.61, BINDING) | lost NoCaps-test image = W25-flagged, counted, FAULT threshold | **v1.2:** reopened as N-B1; one rule in §8.1 |
| NB-T2POOL (l.62, tier-2 obligation) | tier-2 pools exclude every tier-1 dev image by id and W25; resolve the 43 NoCaps-val ∩ XM3600 | §4.4 (stated obligation) |
| NB-INSAMPLE (l.63) | SESOI_P, UNCERTAIN, go/stop labelled in-sample on XM3600-vi | §12 |
| NB-SEEDS (l.64) | separate outer-draw and inner-CI seed streams; percentile citation = e2b.py l.597/610 | §5.5, §5.6 |
| NB-STAMP (l.65) | restamp from `date -u` | header. **v1.2:** superseded by NB-RESTAMP |
| NB-SPEED (l.66) | speed-test outputs discarded, not scored | §10.1 |
| NB-COMMIT (l.67, gatekeeper) | commit message declares [proposal] values, T_A/O_B 1,070, seeds fixed as written; commit governs status line; 8/6-gram scan | header; §16 (v1.2: with NB-V1COMMIT) |
| NB-PINSTIER (l.68) | PINS pinning `gates.py` gets a 92 panel; one judge for prompt/model pins | §9.1 step 5; §14 Q-PINS |
| NB-2001 (l.69) | committed source for OpenViIC test 2,001 | §4.1 (LISTS_ADDENDUM l.21, committed) |
| NB-PARITY (l.70) | parity names its input CSVs; pin their shas | §3.3 |
| NB-NOVELTY (l.71) | CapMAS decomposes post hoc; C's novelty = position; carried to the tier-3 re-sweep | §1.3 |
| NB-LEDGER (l.72, coordinator obligation) | ViTextVQA dev recorded as spent by L1 in the next PORTFOLIO edit; STATE C row after GO | §12 (stated obligation) |
| NB-PARITYBIT (l.73) | `int(last_hex, 16) % 2 == 0` = explore | §4.2 |
| NB-SKILL (l.74) | SKILL.md marked untracked | §2.1 |
| NB-ENC (l.75) | encoder hub id + revision in PINS | §6.2 |
| Ruling 2 (l.42) | overrides O3, O4, O5, O7, P1, P2 accepted | §13 (status column) |
| Ruling 3 (l.43) | [proposal] / counted-after-GO values fixed at registration; counts pinned by sha in `c_pvr_lists.json` before the first decode; OpenViVQA exception | header; §4.1; §4.3 |
| Ruling 4 (l.44) | loss branch: never re-derived; any later ruling allowing it must start from CSVs whose shas equal those logged at G-B and reproduce GB_SEALED.sha256 byte for byte, else NOT COMPUTED | §9.4 loss branch |

## v1.1 changes (item → section)

| item | section |
|---|---|
| status line, WRITTEN stamp, v1 kept | header |
| CC-220 closure table; this table | top |
| B1 guard inside P(PASS); NB-SEEDS; NB-LOST | §5.5, §5.6 |
| B2 CSV custody (new §9.6) | §3.1, §9.2, §9.6, §11 |
| B3 OI-test URL; B4 tenancy; NB-W25STOP; NB-LOST fetch rule | §8 (v1.2: split into §8.1-§8.3) |
| NB-OVQA; NB-2001; NB-PARITYBIT; NB-T2POOL | §4.1-§4.4 |
| NB-PARITY input CSV pins | §3.3 |
| NB-NOVELTY | §1.3 |
| NB-SKILL | §2.1 |
| NB-ENC; NB-NOVAR | §6.2, §6.3 |
| NB-PINSTIER (PINS split into PINS-A one judge / PINS-B 92 panel) | §9.1, §14 |
| NB-CAP; NB-SPEED | §10 |
| NB-INSAMPLE; NB-LEDGER | §12 |
| Rulings 2-4 recorded | §9.4, §13 |
| Q-PINS added; Q-custody text per CC-220 | §14 |
| NB-COMMIT gatekeeper checklist (new §16) | §16 |

## Closure table (binding items from CC-219r3, CC-219r2, CC-219)

| item (source line) | what was asked | where closed here |
|---|---|---|
| NB1 = N21 custody (CC-219r3 l.54) | single-tenant custody host named before any NoCaps-test pixel moves; W25 in isolated tmpfs; never M8 while E2b or B jobs run; reword v4.1 l.327; amend l.450 for a W25-only pixel step; no rental W25 without the PI's Q-custody answer, else M1 or laptop; unnamed/shared host = BLOCKING | §8 (custody), §13 rows O1-O2, §14 Q-custody |
| NB2 = N17 retention (l.55) | one sha-pinned, G-A-filtered G-B intermediate kept unread at a named path with an access log; opened once at the tier-3 freeze; deletion barred | §9.4 |
| NB3 = N22 n_e_power (l.56) | n_e_power = n_e(G-B) − W25-flagged count (flagged vs earlier ledger owners); §9.2 datastore pairs (here §7.4) counted separately | §5.6, §7.3, §7.4 |
| NB4 ordering (l.57) | G-C desk check before G-A and G-B (CC-219 R10, l.54); Q11 ruled before any C rental (CC-219 R8, l.52) | §9.1 (order), §13 rows O3-O4 |
| NB5 = N19 (l.58) | gatekeeper PORTFOLIO = HEAD a4bcdca1 + judged C rows only | CLOSED by d68b1e7 (PORTFOLIO 910ab3bf); recorded §0 |
| NB6 = N18 (l.59) | v4.1 l.3, §15, STATE-row wording | CLOSED by d68b1e7 (v4.1 8334cf5d); STATE row is the coordinator's (§12) |
| NB7 = N20 (l.60) | PORTFOLIO l.168 aligned with l.193 | CLOSED by d68b1e7 (PORTFOLIO l.168 at HEAD) |
| NB8 = N12 cost (l.61) | C total ≈155-195 GPU-h (≈2.7-3.4M VND); tier 1 capped at 20 GPU-h pending a speed test; separate budget (M8 ends 11-15) | §10 |
| NB9 = N16 (l.62) | pin the 3,600-id XM3600 list; asserts length 3,600, splits 1,399/456/1,745, 54966ca7 a subset; oiv7_labels.json (2,584 keys) cannot serve | §2.2, §9.2 (G-A step 0) |
| NB10 prior art (l.63) | name CapMAS (arXiv 2412.15484) beside Woodpecker for the A8 control | §1.3 |
| NB11 carried (l.64) | CC-219 N1-N15 | rows below |
| CC-219 N1 (CC-219 l.73) | define "sign of (1)"; map "rule-dependent" to PASS/FAIL; A's +1.97 [-0.44, +4.01] as falsifier | §5.4 condition 3 |
| N2 (l.74) | CIDEr-VI guard reuse: split KTVIC/OpenViIC test by a pre-fixed id hash, or label in-sample | §4.2 |
| N3 (l.75) | NoCaps label loader + scorer pinned, parity selftest reproducing the XM3600 manifest (2,119; 4,453/8,276; conflict rule cmd_build l.115-118) | §3.3, §11 |
| N4 (l.76) | scorer asserts RESCAP_RAW_TONE unset (chair.py l.74, l.168) | §3.1, §11 |
| N5 (l.77) | power procedure fixed before G-B | §5.6 |
| N6 (l.78) | bootstrap spec | §5.5 |
| N7 (l.79) | differential verifiable-mention flag; per-arm Vietnamese guard at the test look | §5.7 |
| N8 (l.80) | G-C first | §9.1 |
| N9 (l.81) | "on the 69 mapped classes"; no NoCaps domain or novel-object claim for Vietnamese | §1.2 |
| N10 (l.82) | Q11 before any C tier-1 rental | §9.1, §14 Q11 |
| N11 (l.83) | ViTextCaps secondary only, frozen config, passing dev rehearsal before the cutoff | §4.4, §14 Q7 |
| N12 (l.84) | cost restated | §10 |
| N13 (l.85) | freeze the English P_obj^EN map before G-B | §3.4, §9.3 PINS |
| N14 (l.86) | ViTextVQA dev vs OpenViVQA dev roles | §4.3 |
| N15 (l.87) | A and B before C; STATE row after GO | §10.3, §12 |
| CC-219r2 N16-N20 (CC-219r2 l.49-53) | as NB9, NB2, NB6, NB5, NB7 | as above |
| CC-219r2 NB-W25 option (ii) (CC-219r3 Ruling 1, l.41) | n_e(G-B) post-G-A; power with pixel-only W25 subtraction; exact W25 difference once, from the sealed intermediate, at the tier-3 freeze | §5.6, §9.4 |
| CC-219 R5 / Q2 coverage rule (CC-219 l.49, l.98) | ruled by the panel; power procedure and G-B seal committed in this prereg before G-B | §9.3 G-B row, §5.6; §14 Q2 (FYI) |

## 0. What tier 1 is for, and the three tiers

- **Tier 1 = dev-explore (this file).** Dev data only. It fixes, before tier 2: SESOI_P, the headroom stop, the
  UNCERTAIN variant (PVR-drop or PVR-keep), and a go/stop on XM3600-vi (§6). k (= 4), the captioner, the verifier,
  the prompts and greedy decoding are **not** chosen by tier-1 data: they are pinned in the PINS-A amendment (§9.1) **before
  G-B** (§9.3).
- **Tier 2 = dev-confirm rehearsal** (own prereg; needs Q11 = YES): the frozen tier-1 config on NoCaps val (P_obj^VI)
  and O_B (proxy). Tier 3 is registered only if P(PASS) >= 0.98 at n_e_power (§5.6). Below 0.98 the test is never
  touched (three-tier rule).
- **Tier 3 = one official look** (own prereg, irreversible >= 92): NoCaps test (P_obj^VI, R_obj^VI; EvalAI CIDEr-EN
  benchmark) and OpenViVQA dev (proxy).
- **This prereg spends no test set and licenses no test read.** G-A reads ids only. G-B (one run, aggregates only,
  sealed) is registered here; it runs only after this prereg's own GO, after the PINS-A and PINS-B amendments (k, captioner,
  verifier, prompt, EN map; G-B code), and after Q11 = YES (§9.1). G-B reads test-label rows but is not a test look: no
  caption, prediction or score exists or is used (v4.1 l.399). The W25 pixel step on NoCaps test and OpenViVQA dev
  computes features only (no caption, prediction, label or score) on the named custody host (§8).
- **Priority.** A (SPIC) and B go before C on agent-days and GPU time (CC-219 R10, l.54; N15).

## 1. Claim, scope and prior art (v4.1 §1, §10)

### 1.1 Registered claim form (for the tier-3 prereg)
On NoCaps test images, after the pre-fixed image-level exclusions (§7), Vietnamese captions generated with
PVR-verified demonstrations have higher object precision P_obj^VI than post-hoc correction with the same verifier
(A8), against existing human-verified Open Images labels on the 69 mapped classes, with object recall R_obj^VI not
worse than a margin (v4.1 l.84-85). English is a benchmark only (PI-1101t; PI-1101u, LOG l.1112).

### 1.2 Scope (N9)
- "Object precision against human-verified labels **on the 69 mapped classes**" (manifest l.10). Not general
  Vietnamese caption quality; no reference-based Vietnamese CIDEr claim on held-out data outside branch N-A.
- No NoCaps in-/near-/out-of-domain or novel-object claim for Vietnamese.
- Forbidden: "first to verify retrieved content against the image", "a new verifier", any sentence that makes the
  English result the main result (v4.1 l.94-98). The paper never mentions overlap or duplication (PI-1101o/p).
- Title per CC-219 Ruling 9 (l.53).

### 1.3 Prior art and narrowed novelty (NB10)
- Allowed novelty (v4.1 l.92): position plus granularity, i.e. verifying the **retrieved input** at the
  **proposition level** (scene-text propositions included) **before** it is used as ICL.
- The A8 control (post-hoc correction with the same verifier) answers the two closest post-hoc works:
  **Woodpecker** (arXiv 2310.16045; `manuscript/directions/C_NOVELTY_AND_DATA_2026-11-01.md` l.110) and **CapMAS**
  (arXiv 2412.15484; CC-219r3 l.28, l.63).
- **NB-NOVELTY.** CapMAS already decomposes captions into propositions and checks them **post hoc**, so
  proposition-level decomposition is not claimed as new. C's claim is the **position**: verifying retrieved
  demonstrations **before** they enter ICL, tested head-to-head against post-hoc correction with the same verifier
  (A8). This point is carried to the re-sweep below.
- The tier-3 literature re-sweep of CC-214r3 (l.190-191) binds before the tier-3 prereg (v4.1 l.476).

## 2. Inputs pinned now (sha256 computed at drafting; first 8 hex, full sha in 2.3)

### 2.1 Instrument and rules (git-tracked and clean at HEAD unless marked)

| file | sha256 | last commit | role |
|---|---|---|---|
| `rescap/chair.py` (`objects_in`, `raw_tone=False`) | e47d249a | a0accb5 | caption -> lexicon classes |
| `rescap/vi/lexicon.py` | fbc945f2 | 996c32f | classes and classifiers |
| `data/xm3600/vi_oiv7_map.json` | 27f2b1ca | e564ed6 | 69 mapped classes (manifest l.10) |
| `scripts/xm3600_oiv7.py` (`status`, `statuses`; `build` path barred for NoCaps test) | 9a79403f | e564ed6 | present / absent / unknown rule |
| `data/xm3600/manifest.json` | 263015f9 | e564ed6 | parity targets (§3.3) |
| `data/xm3600/oiv7_labels.json` | bac3953a | e564ed6 | XM3600 dev gold (A12 oracle on XM3600-vi); never the 3,600-id list |
| `rescap/metrics_svp.py` (3-label VERDICTS) | 13cef8d1 | 1e87064 | FAIR verifier label set (v4.1 l.252) |
| `manuscript/prereg/2026-10-28_w25_neardup/RULE.md` | 289c0a59 | - | W25 §3 (C1 ∨ C2 ∨ C3) |
| `scripts/w25/w25.py` | d6d12780 | 8f99bc8 | W25 features and rule |
| `manuscript/prereg/2026-10-28_w25_neardup/oiv7_val_ids.txt` | 4b7a1813 | - | 41,620 OIV7 val ids (`wc -l`; RULE l.19) |
| `manuscript/prereg/2026-10-28_w25_neardup/xm3600_in_oiv7_val_ids.txt` | 54966ca7 | - | 456 XM3600 ids in OIV7 val (`wc -l`; RULE l.21) |
| `manuscript/prereg/2026-10-27_c_en/cen_memory_allowed.tsv` | 175907e2 | - | D-EN base (PORTFOLIO l.193) |
| `manuscript/prereg/2026-10-27_grl_pilot/kv5000.txt` | b7a7a89d | - | Karpathy val 5,000, excluded from C (PORTFOLIO l.193) |
| `.session_backup/2026-11-01/c_direction_v3_idcheck/idcheck.py` / `idcheck_out.txt` | 040e78ef / 13d59e15 | untracked | G-D (v4.1 l.397) |
| `.claude/skills/venue-tallip/SKILL.md` | ff4fdfb2 | untracked (not in the index) | title rule (v4.1 l.406) |
| `scripts/c_en/cen_fetch.py` (`OI_URL` l.51 = OI `validation/` only) | e51918e9 | ed1e6c4 | fetch helper `get`; its URL constant is NOT used for NoCaps test (§8, B3) |
| `manuscript/prereg/2026-10-22_c_stage1/LISTS_ADDENDUM.md` | aa3923b9 | 6129e8e | OpenViIC test 2,001, KTVIC test 558 (l.21) |
| `manuscript/prereg/2026-10-21_dev_pools/exclusion.json` (`image_sha256.xm3600_all_images`) | c52a96d1 | 249028d | XM3600 sha-refuse backstop in C's fetch loop (§8.1) |

### 2.2 The 3,600-id XM3600 list (N16)
- Source file (gitignored, not committed): `data/datasets/xm3600/oiv7/xm3600_ids.txt`, sha256 `1bd00f46`, 3,600
  lines, 61,200 bytes (`wc -l`, `stat` at drafting; not parsed). A byte-identical copy (same sha) sits at
  `.session_backup/machines/n2/ncs-data/datasets/xm3600/oiv7/xm3600_ids.txt`.
- At G-A step 0 (after GO) it is copied to `manuscript/prereg/2026-11-02_c_pvr_tier1/xm3600_all_ids.txt` and must
  equal 1bd00f46; `gates.py` then asserts: (a) 3,600 unique 16-hex ids; (b) OI split counts test 1,399 / validation 456
  / train 1,745 (manifest l.303-306), taken from the `Subset` column of
  `data/datasets/xm3600/raw/image_attributions.csv` (sha256 `288de413`; ids and subset only, as `xm3600_oiv7.py`
  l.103-105 reads it); (c) every id of 54966ca7 is in the list; (d) the 456 equal the list ∩ 4b7a1813.
  Any assert failing is a FAULT and G-A stops.
- `data/xm3600/oiv7_labels.json` cannot serve: it keys only images with a verified label (2,584; manifest l.13;
  CC-219r2 l.49).
- **Not verified at drafting:** 54966ca7 ⊂ 1bd00f46 and the split asserts (no data file was parsed).

### 2.3 Full sha256 values
```
e47d249ac7290070f2387d3fa8b22dac77728265ad276f55aa6520f5cbc591a3  rescap/chair.py
fbc945f2247418275144ac75b893f7c51f8951b9ea42018680d433775dd79eb9  rescap/vi/lexicon.py
27f2b1ca3f2bf47d43c8f00e8409472c8d571eb720d47b8107a1c77bd208d16a  data/xm3600/vi_oiv7_map.json
9a79403f4fc38609282d40082ab7f878133edca8aff9e0dc2462db467b7193f0  scripts/xm3600_oiv7.py
263015f9dc46ebe2cea80055e04ed39baf80a356f4e027cd3756464279135bef  data/xm3600/manifest.json
bac3953a511a9793c22e928a29b68ae05dbf9654502abcbe7b64fd9f6d74c8b2  data/xm3600/oiv7_labels.json
13cef8d1a0fa38ea3e7ae42b355d184d0ee21589a85661897c5f78d98a431b7b  rescap/metrics_svp.py
289c0a595e0141fa40ad80c62b4f0d0d42970429b5b5900bf5a0f510ca7ec174  manuscript/prereg/2026-10-28_w25_neardup/RULE.md
d6d127807929c0534e6140d77831b682e3a7202484fa074d56229e0d091316c0  scripts/w25/w25.py
4b7a1813487dc5d74a5bd4aca7c36d0f6d2d3042d9cc6cf4091180dc473eabb0  manuscript/prereg/2026-10-28_w25_neardup/oiv7_val_ids.txt
54966ca78ce310201c091282603c9398155b8b05aaae9eb4cdf0abed88e6c5ef  manuscript/prereg/2026-10-28_w25_neardup/xm3600_in_oiv7_val_ids.txt
175907e23fc0f78e2d304e09a4b8bb5364943c9f2208cc24f8e59e215ad771af  manuscript/prereg/2026-10-27_c_en/cen_memory_allowed.tsv
b7a7a89dd86f75f60dc1984613bde9048118c37bc5246e028c7b22aeb4199477  manuscript/prereg/2026-10-27_grl_pilot/kv5000.txt
040e78effe93fbb99a118ad2f8a78d2a2046ee3a9a8660984db3f159fd53ebc3  .session_backup/2026-11-01/c_direction_v3_idcheck/idcheck.py
13d59e152d604cd96dfe55b8998af5105efdf8c5d83703c67f311b04a8031baf  .session_backup/2026-11-01/c_direction_v3_idcheck/idcheck_out.txt
ff4fdfb22e0b80d1b61759bf1232539d53506c5a1d5e15973777fc278683edaa  .claude/skills/venue-tallip/SKILL.md
1bd00f466afc196ab51a6b86d3c1a5b6ea1e553393362b98199aa892287e1922  data/datasets/xm3600/oiv7/xm3600_ids.txt
288de413d25e9c70dadfd42ee59256aa1082673e615d0eda02c3875fe2b36ecd  data/datasets/xm3600/raw/image_attributions.csv
8334cf5d5ea8905f55db90670e69539605e991d4ea9959b988e1e2fe5a456ef4  manuscript/directions/C_DIRECTION_v4_1_2026-11-02.md
910ab3bf1da0c01aeda3aeb23690fa590cd00763966246b6e1e95aa9d838095a  manuscript/directions/PORTFOLIO_3Y_2026-10-29.md (HEAD blob)
e51918e958ad86e832dd34fbf5ed86d2f7fc13cf41b602dfe537afa43af4c673  scripts/c_en/cen_fetch.py
aa3923b9fe51a200aed6cc491251d1703eb9b3c5a028b769a58a3f2b6079db98  manuscript/prereg/2026-10-22_c_stage1/LISTS_ADDENDUM.md
c52a96d18925b974878ae1a970c3f9133fb3482216676fd41871eeabb68cc77f  manuscript/prereg/2026-10-21_dev_pools/exclusion.json
779afb19a4c3c25f100f871e92bbe8e937d6fa7f20ea75c4d0f7a23953056e76  data/datasets/xm3600/oiv7/xm3600-train-annotations-human-imagelabels.csv
b7967190d6b05d6c97d38fe238046091905aabfe5bd268df4efe1c2a9a3db9d0  data/datasets/xm3600/oiv7/xm3600-val-annotations-human-imagelabels.csv
06567dd986bf571db62d69af5abec0973a37f2552b1e00c50147cf490f72c19a  data/datasets/xm3600/oiv7/xm3600-test-annotations-human-imagelabels.csv
84a4373a0efb7fd6d93fe19b0e7ceb6c1b855c233d13b9b78a9a33655c9fdce3  data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv
75c22a0814037cee2bf328101aefdb3852a499c3e65fcdb1707e8fa2992f6c07  data/datasets/xm3600/oiv7/fetch.sh
e1af682181bcbbdfea6c76fb083e90481aa834efa1138efde869c1cc21e40de0  data/datasets/xm3600/oiv7/full-train.md5
5770ed7c94cb6ae9ebd5e8746a95382d6475d0887c87ad4c05afa664ec840d8a  data/datasets/xm3600/oiv7/full-val.md5
2eebd937f99edec5267abd697f1b839d9846fc4ba4fd070d833b048bbc9ace54  data/datasets/xm3600/oiv7/full-test.md5
```

### 2.4 Drafting-touch disclosure (anchor no_data_read)
No NoCaps or Open Images label, caption or image was read. No gate ran. Files touched while drafting, none parsed or
displayed: `data/datasets/xm3600/oiv7/xm3600_ids.txt` (sha, `wc -l`, `stat`), `data/datasets/xm3600/full_data.json`
(sha 101d24ad = RULE l.21; `wc -l`), `data/datasets/xm3600/raw/captions.zip` (sha 7964f969, `wc -l`, `stat`),
`data/datasets/xm3600/raw/image_attributions.csv` (sha only), `data/datasets/vitextvqa_raw/ViTextVQA_dev.json`
(sha c6ab6a7b only), `data/xm3600/oiv7_labels.json` (sha only). Two incidental prints, both of spent XM3600 (A's set,
dev only, already committed): a `find` listing showed XM3600 image **file names** (ids) under `data/datasets/xm3600/raw/`;
a `grep` on the committed `manifest.json` showed five per-class present/absent pair counts (l.31-47). A `find` / `ls`
listed file **names** only of NoCaps-val files already on disk (`data/datasets/nocaps/nocaps_val_4500_captions.json`
and C-EN fetch/guard files under `.session_backup/`); none was opened. No NoCaps-test file exists on the laptop.
**v1.1 touches** (no data parsed or displayed): file names listed in `data/datasets/xm3600/oiv7/`; sha256 of the
three `xm3600-*-annotations-human-imagelabels.csv` (spent XM3600 rows), `oidv7-class-descriptions.csv`, the three
`full-*.md5`, `fetch.sh`; code read: `fetch.sh` (whole), `scripts/c_en/cen_fetch.py` l.45-56, `scripts/c_en/cen_pool.py`
l.27, l.139, `scripts/vsps_j_e2b/e2b.py` l.595-612; `git grep` of committed text for "2,001".
**v1.2 touches** (no data parsed or displayed): code read: `scripts/c_en/cen_fetch.py` l.236-252, `scripts/w25/w25.py`
l.78-84 and l.150-175; sha256 of `manuscript/prereg/2026-10-21_dev_pools/exclusion.json` (not opened); file names listed
in `.session_backup/2026-11-02/snap/`.

## 3. Outcome, instrument and gold (v4.1 §3.1)

### 3.1 Mention mapping and status
- Each Vietnamese caption -> `objects_in(caption, raw_tone=False)` -> lexicon classes; keep the 69 keys of
  27f2b1ca; each class counted once per caption (as `xm3600_oiv7.py score`). The vocabulary is fixed now (W3).
- **N4:** the scorer asserts `os.environ.get("RESCAP_RAW_TONE")` is unset before the first call (chair.py l.74,
  l.168 read it); set -> FAULT.
- Pair (image i, class c) status via `status()`: present (a `pos` class verified present, Confidence 1); absent (not
  present and a `neg` class verified absent, Confidence 0); unknown otherwise, including two-way conflicts.
- Gold: `oidv7-{val,test}-annotations-human-imagelabels.csv` (CC BY 4.0), md5 checked against the bucket, rows
  filtered by id while reading, under the custody rule of §9.6 (B2): the full CSVs are never stored. No new labels, no
  AI-silver, no model-made label.

### 3.2 Metrics
- **Primary P_obj^VI** = present / (present + absent), pooled over mentions, image-level bootstrap. Primary rule:
  unknown mentions leave the denominator. Registered sensitivity: P_obj^VI,wrong = present / (present + absent +
  unknown).
- CHAIR_i^VI = 1 − P_obj^VI; CHAIR_s^VI secondary.
- **R_obj^VI** = verified-present pairs mentioned / verified-present pairs (the recall guard).
- Always reported per set and arm: verified present / absent pair counts on the mapped vocabulary; verifiable-mention
  share = (present + absent) / mapped mentions, beside P_obj^VI.
- CIDEr-VI (dev and tier-2 guard only; NoCaps test has no Vietnamese reference, so tier 3 has no CIDEr-VI).

### 3.3 New NoCaps loader and its parity selftest (N3)
- `gates.py load_labels(ids, csv_paths)` is a new loader (the `xm3600_oiv7.py build` path with `pairs_per_class`
  l.161 and the per-image LABELS file l.174-176 is barred for NoCaps test). Conflict rule copied from `cmd_build`
  l.115-118: pos = classes seen only with Confidence 1; neg = only with 0; mixed -> neither.
- **Parity selftest (laptop CPU, after GO, before G-B):** the same loader on the XM3600 rows reproduces the committed
  manifest exactly: 2,119 images with a verified label on a mapped class (l.14); 4,453 present / 8,276 absent pairs
  (l.16-17). Any difference = FAULT; G-B does not run. The XM3600 label rows are A's spent dev gold.
- **Parity inputs (NB-PARITY), all on disk, gitignored, already stream-filtered by the house `fetch.sh`; pinned in
  PINS-A by these shas (computed at drafting, files not opened):**
  `data/datasets/xm3600/oiv7/xm3600-train-annotations-human-imagelabels.csv` `779afb19`,
  `xm3600-val-annotations-human-imagelabels.csv` `b7967190`, `xm3600-test-annotations-human-imagelabels.csv`
  `06567dd9`, `oidv7-class-descriptions.csv` `84a4373a`; producer `fetch.sh` `75c22a08`; full-file md5 records
  `full-train.md5` `e1af6821`, `full-val.md5` `5770ed7c`, `full-test.md5` `2eebd937` (full sha256 in §2.3).

### 3.4 English benchmark map (N13)
No English -> Open Images class map exists in the repo (searched `data/` at drafting). `scripts/c_pvr/en_oiv7_map.json`
is built from class names only (`oidv7-class-descriptions.csv`, no label rows) and an English lexicon pinned in PINS-A,
frozen by sha in PINS-A **before G-B**, never amended after. P_obj^EN is descriptive, never a gate.

## 4. Sets and roles (v4.1 §3.2-§3.3, §9.2)

### 4.1 Tier-1 dev sets (spent or train splits; v4.1 l.184, l.450)

| set | size (source) | role | datastore |
|---|---|---|---|
| XM3600-vi | 3,600 images (manifest l.12); 2,119 carry a verified mapped label (l.14) | P_obj^VI dev: SESOI_P, headroom, UNCERTAIN; CIDEr-VI dev (in-sample) | D-VI |
| KT-C | 3,907 (PORTFOLIO l.193) | English benchmark arm only (format, speed, P_obj^EN descriptive) | D-EN |
| T_A (TextCaps train slice) | 1,070 images [proposal, = OpenViVQA dev size, C_TEST l.28], first by sha256(id + "c_pvr_TA") order | English scene-text dev | D-TC |
| ViTextVQA dev | count by `c_pvr.py lists` after GO (file sha c6ab6a7b) | Vietnamese scene-text dev (§4.3) | D-VI |
| KTVIC test | 558 (v3 l.143), explore half only (§4.2) | CIDEr-VI guard dev | D-VI |
| OpenViIC test | 2,001 (`manuscript/prereg/2026-10-22_c_stage1/LISTS_ADDENDUM.md` l.21, committed: `ov_test 2,001`; also DESIGN.md l.69, l.359), explore half only | CIDEr-VI guard dev | D-VI |

KTVIC test 558 is also in the committed LISTS_ADDENDUM l.21 (`kt_test 558`) and XM3600 3,600 (`xm_all 3,600`).
Not touched in tier 1: COCO Karpathy val (all 5,000, kv5000.txt), NoCaps val, O_B, every test set (v4.1 l.450).
D-EN = 80,083 (PORTFOLIO l.193); D-VI and D-TC are counted by `c_pvr.py lists` after GO (v3 l.374-375).
**Counted-after-GO values (CC-220 Ruling 3):** ViTextVQA dev, D-VI, D-TC and the per-half counts of §4.2 are written
by `c_pvr.py lists` to `c_pvr_lists.json`, whose sha is pinned in a gatekeeper LOG line **before the first decode**.
The rules that produce them are fixed here; the counts are not choices.

### 4.2 CIDEr-VI guard split (N2)
`half(id)`: h = sha256(UTF-8 bytes of the dataset's native image id string + "c_pvr").hexdigest(); explore (tier 1)
iff `int(h[-1], 16) % 2 == 0`, else confirm (tier 2) (NB-PARITYBIT). Applied to KTVIC test and OpenViIC test before any decode; counts per half
printed and pinned in `c_pvr_lists.json`. XM3600-vi CIDEr-VI is labelled in-sample.

### 4.3 Scene-text roles (N14)
- **ViTextVQA dev:** tier-1 dev for the Vietnamese proxy pipeline (question regex coverage, extractor behaviour,
  P_text/R_text descriptive). Spent by L1 (C_TEST l.30), so it is an **earlier owner**: OpenViVQA-dev images that
  overlap it under W25 leave C's proxy (count only), the same logic as CC-219 W1 (§13 row O7).
- **OpenViVQA dev** (1,070 images / 3,545 QA; C_TEST l.28; PORTFOLIO l.169): C's unspent proxy one-look set (tier 3).
  Only 3 json files were read for counts (C_TEST l.28); their shas are not on record. **NB-OVQA (binding, before any
  OpenViVQA byte is used):** `c_pvr.py ovqa-pin` downloads the 3 json files of `uitnlp/OpenViVQA-dataset` at one HF
  commit revision (recorded, never `main`), records the revision and the 3 sha256 values in PINS-A, and asserts dev =
  1,070 images / 3,545 QA (C_TEST l.28) from keys and lengths only (no question or answer text printed); any
  mismatch = FAULT and the proxy is not run. No image is fetched before the W25 step of §8.
- **OpenViVQA json custody (NB-OVQALOST).** The 3 json files are downloaded only to `~/.vsps_sealed/c_pvr/ovqa/` on the
  laptop's WSL ext4 home (directory mode 0700), never under `data/`, `/mnt/d`, the repo or any backup path. Until
  the tier-3 freeze, the dev and test files get **a read of keys and lengths only**, plus the image file-name field
  needed for the §8 fetch list; no question or answer string is read, printed or stored. The train file has the same
  limit until the tier-2 prereg licenses the O_B read. Each read is logged in `~/.vsps_sealed/c_pvr/ACCESS_LOG.tsv`.
  Lost OpenViVQA images and their FAULT cap: §8.1.
- **O_B** (OpenViVQA train slice, 1,070 images [proposal, same rule as T_A with suffix "c_pvr_OB"]): tier-2 rehearsal
  for the proxy; not used if any Vintern model is the VI captioner or verifier (v3 l.251).

### 4.4 Later tiers
- Tier 2: NoCaps val (P_obj^VI; only after Q11 = YES); O_B; KTVIC/OpenViIC confirm halves (CIDEr-VI guard).
- **NB-T2POOL (stated obligation, binds the tier-2 prereg):** every tier-2 pool excludes every tier-1 dev image by id
  and by W25 (RULE §3) before any tier-2 decode; the 43 NoCaps-val images that are XM3600 images (RULE l.19) leave
  NoCaps val (XM3600 is a tier-1 dev set), counted. The tier-2 prereg states the resulting pool sizes.
- Tier 3: NoCaps test (10,600 images, OI test only; v4.1 l.179, l.196); OpenViVQA dev; ViTextCaps test only if
  publicly released before the tier-3 freeze, secondary, frozen config, passing ViTextCaps-dev rehearsal (P(PASS) >=
  0.98) before the cutoff (N11; CC-219 R7, l.51); VieCap4H private test only if its references are published.

## 5. Arms, contrasts and statistics (v4.1 §4; v3 §4 table l.191-205)

### 5.1 Arms
A0 zero-shot; A1 top-k (UniRAG-style); A2 random-k; A3 sample-k in top-7 (inference-time transfer of Li et al. ACL
2024); A4 NES-style CLIP filter (< 0.2); A5 LMCap; A6 decompose without filtering; A7 count-matched random drop; **A8
post-hoc correction with the same verifier, same prompt and same per-image verifier-call cap (Woodpecker / CapMAS
style)**; A9 ITM/ARA caption re-ranking; A10 RA-CoA-style re-derivation; A11 foreign-text deletion; A12 oracle filter
(dev only); PVR-drop and PVR-keep (§6.3). k = 4, greedy decoding. Vietnamese arms on Vietnamese sets and NoCaps test
(D-VI); English arms S1-S5 = PVR, A8, A1, A0, A6 (D-EN). Cut order if the projection exceeds the cap: A10 -> A5 -> A9
-> A3 -> A2 -> A4 -> A11; never cut PVR-drop, PVR-keep, A8, A1, A0, A6, A7, A12 (v4.1 l.458).

### 5.2 Primary contrast and family
- **One primary contrast:** PVR − A8 on P_obj^VI (primary unknown rule), paired by image.
- **Holm family (secondary):** PVR vs A0-A7 and A9-A11 on P_obj^VI; A12 and cut arms out. Two-sided paired-bootstrap
  p = min(1, 2 × min(#{Δ* <= 0}, #{Δ* >= 0}) / B) [proposal], Holm step-down at family α = 0.05 [proposal].

### 5.3 Tier-2 PASS (dev-confirm; registered here, binding on the tier-2 prereg)
1. ΔP_obj^VI(PVR − A8): 95% CI lower bound > 0 **and** point estimate >= SESOI_P;
2. ΔR_obj^VI(PVR − A1): CI lower bound > −δ_R (δ_R = 2.0 points; v4.1 l.155);
3. ΔCIDEr-VI(PVR − A8) and ΔCIDEr-VI(PVR − A1) on the KTVIC and OpenViIC **confirm halves**: CI lower bound > −δ_C
   (δ_C = 2.0, labelled lenient; v4.1 l.154);
4. the condition-3 sign check of 5.4 holds on NoCaps val;
5. guard G of 5.4 (the 5.7(b) VI-script share >= 0.95 for both PVR and A8) holds on NoCaps val.

### 5.4 Tier-3 decision rule (written now; binding on the tier-3 prereg)
PASS iff, on NoCaps test after §7: (1) ΔP_obj^VI(PVR − A8) CI lower bound > 0 and point estimate >= SESOI_P; (2)
ΔR_obj^VI(PVR − A1) CI lower bound > −δ_R; (3) **(N1)** the **point estimate** of ΔP_obj^VI(PVR − A8) under the
unknown = wrong rule is > 0. If (1) and (2) hold but (3) fails, the claim is labelled "rule-dependent" and the headline
is **FAIL**; both numbers are reported. Named falsifier: A's +1.97 [-0.44, +4.01], whose sign flips under unknown =
wrong (CC-219 l.27, l.73), is the pattern that fails condition 3. **PASS also requires guard G:** the 5.7(b) VI-script share is >= 0.95 for both
PVR and A8 (PVR below -> FAIL; A8 below -> INCONCLUSIVE). Not gates: CIDEr-EN
(EvalAI, point estimates, v4.1 l.316), P_obj^EN, the Holm family, the proxy (own rule, §6.4). A registered FAIL is
still reported briefly.

### 5.5 Bootstrap (N6)
Unit = image; paired (one image resample serves both arms); B = 10,000; percentile 95% CI (2.5 / 97.5 percentiles);
seed 20261102 [proposal]. B follows the E2b prereg (`manuscript/prereg/2026-11-01_vsps_j_e2b_tier1/PREREG_DRAFT.md`
l.250-251); the percentile form follows its code, `scripts/vsps_j_e2b/e2b.py` l.597, l.610 (NB-SEEDS citation fix).
Ratio estimators (pooled present / (present + absent)) are recomputed per replicate. Replicates with an undefined
ratio are dropped and counted; > 1% dropped = FAULT.

### 5.6 Power procedure and n_e_power (N5, N22; fixed before G-B)
- **n_e(G-B)** = NoCaps-test images left after G-A's id exclusions with >= 1 verified label on a mapped class.
- **n_e_power = n_e(G-B) − (W25-flagged count)**, where the W25-flagged count = G-A-remaining NoCaps-test images
  flagged by W25 against earlier ledger owners (pixels only, no label read; §8). The §7.4 self-retrieval
  (datastore/dev-yield) pairs are a separate count and never enter n_e_power. Conservative by construction (some
  flagged images carry no mapped label).
- **Lost images** (classed only by §8.1) are added to the W25-flagged count for n_e_power. The lost/FAULT rule and
  its cap are stated in §8.1 and nowhere else.
- **P(PASS)** at tier 2 = nested bootstrap on the frozen tier-2 per-image tables of NoCaps val: outer B_out = 500
  replicates, each drawing n_e_power images with replacement from the NoCaps-val images that carry a verified mapped
  label; inner B_in = 1,000 for each CI [proposal; sizes follow E2b l.265-267]. **Seed streams (NB-SEEDS):** outer
  draws from one generator seeded 20261103; inner CI of outer replicate r from a separate generator seeded
  20261104 + r [proposal]; the two streams never share a generator.
- **B1 (CC-220 l.51): a replicate PASSES iff 5.4 conditions (1), (2) and (3) all hold AND the 5.7(b) VI-script guard
  (>= 0.95) holds for both PVR and A8 on that replicate's tier-2 per-image tables.** P(PASS) = share of outer
  replicates that pass, i.e. exactly the registered tier-3 PASS (N5 names (1) and (2); (3) and the guard are added
  because the tier-3 PASS needs them). A replicate where A8 fails the guard counts as not passing (the tier-3 outcome
  would be INCONCLUSIVE, not PASS). Monte Carlo SE reported. Effect threshold = SESOI_P as fixed in tier 1.
- **SESOI_P is never scaled with n** (W5); only P(PASS) is projected to n_e_power.

### 5.7 Mention-share flag and Vietnamese guard (N7)
- (a) **Flag:** |verifiable-mention share(PVR) − share(A8)| > 5.0 points [proposal] on any set is flagged and reported
  beside P_obj^VI. Not a gate.
- (b) **Per-arm Vietnamese guard** (tier 3 has no CIDEr-VI): VI-script share = share of captions containing >= 1
  Vietnamese-specific letter (ă â đ ê ô ơ ư or a tone-marked vowel, after NFC) [proposal]. PVR and A8 must each reach
  >= 0.95 [proposal]. PVR below -> FAIL; A8 below -> the primary contrast is INCONCLUSIVE. Reported for every arm at
  every tier.

## 6. Verifier, models, UNCERTAIN and the proxy (v4.1 §5, §7)

### 6.1 Verifier type
FAIR's 3-label scheme (SUPPORTED / UNCERTAIN / REJECTED; `rescap/metrics_svp.py` l.51), label-generating prompt,
label parsing, greedy. No scalar threshold. No VSPS-J S_hi or per-type thresholds. C's verifier is never chosen from
VSPS-J E2b outputs (E2b prereg l.195).

### 6.2 Models by role and G-C
- Candidate order (fixed now; "first passing model" rule of v4.1 l.276): VI captioner / VI verifier:
  Vintern-1B-v3_5, Vintern-1B-v2, Qwen2.5-VL-7B-Instruct, InternVL3-8B, Aya-Vision-8B, then any further candidate
  listed in the G-C1 record in its listed order (the list closes when G-C1 is committed). EN benchmark: LLaVA-1.5-7B.
  Decomposers: deterministic rule-based (VI segmenter, EN dependency parse), pinned in PINS-A. Retrieval encoder: the
  encoder of `cen_memory_emb.npz`, `google/siglip2-so400m-patch14-384` @ `e8e487298228002f3d8a82e0cd5c8ea9c567f57f`
  (`scripts/c_en/cen_pool.py` l.27, l.139); this hub id and revision are pinned in PINS-A (NB-ENC); web-scale
  pretraining recorded "unknown".
- Status per model × set: CLEAN / HIT / UNCHECKABLE (v3 §9.1). Q5 default (CC-219 Ruling 6, l.50): published SFT
  data joinable by OI id is checkable; an OI-based SFT part with undeterminable split membership = UNCHECKABLE = treated
  as contaminated; web-scale pretraining "unknown", disclosed. Localized Narratives covers OI train/val/test, so any SFT
  mix with it is joined by OI id (v4.1 l.268).
- No CLEAN VI captioner or no CLEAN VI verifier on NoCaps test -> STOP (v4.1 §10.1 row 2); no English-only fallback.

### 6.3 UNCERTAIN (v4.1 §5.3)
Order: (i) self-retrieval rule (§7.4); (ii) SESOI_P from A12 and A1 on XM3600-vi; (iii) choose the variant with the higher
dev P_obj^VI that passes δ_C (CIDEr-VI) and δ_R vs A1; if |ΔP_obj^VI| < SESOI_P / 2, PVR-drop. Parse failures, empty
or off-set answers = UNCERTAIN; the UNCERTAIN share is always reported for PVR and A8.
- **Tier-1 test forms (NB-NOVAR):** a variant "passes δ_C" iff the paired image-bootstrap (§5.5) 95% CI lower bound of
  ΔCIDEr-VI(variant − A1) > −δ_C (2.0) on each of XM3600-vi (in-sample), the KTVIC-test explore half and the
  OpenViIC-test explore half; it "passes δ_R" iff the CI lower bound of ΔR_obj^VI(variant − A1) > −δ_R (2.0) on
  XM3600-vi.
- **If neither PVR-drop nor PVR-keep passes both, STOP before tier 2** (no variant is carried; reported as a
  registered dev result).

### 6.4 Demonstrations and the proxy
- Span deletion, sentence drop when no noun is left, fixed whitespace/punctuation table; shared by PVR, A6, A7 and
  A8's output deletion; emptied demonstrations are dropped, never back-filled (v3 §5.4).
- Proxy (v3 §7 items 1-6; v4.1 §7.7): primary contrast PVR − A8 on P_text (w = 1), triviality check PVR − A11;
  SESOI_T = 2.0 points P_text; δ_RT = 2.0 points R_text; same sign under w = 1 and w = 0. Regex list, extractor,
  normaliser and `rapidfuzz` version pinned by sha in PINS-A **before the first tier-1 output**.

## 7. Ledger and image-level rule (v4.1 §9.3; PORTFOLIO l.188, l.193)

### 7.1 Owners
`c_pvr.py owners` builds `c_pvr_owners.json` from PORTFOLIO §2.3 at HEAD and every one-look/spent list under
`manuscript/prereg/` at HEAD (never a closed list); its sha is frozen before any feature pass. Spent sets C uses as dev
are **earlier owners**: XM3600 (all 3,600), NoCaps val, KT-C/Karpathy test, KTVIC test, OpenViIC test, and ViTextVQA
dev for the proxy (§4.3).

### 7.2 Rules
1. C's dev, rehearsal and datastore images yield to every other owner, except sets spent before that owner registered.
2. Only C's non-spent splits (T_A, O_B) yield to C's test sets.
3. NoCaps-test images that overlap an earlier owner (G-A id join or W25) **or are lost in the W25 fetch (§8.1)**
   leave P_obj^VI, R_obj^VI and the local proxy **at every tier** (count only); EvalAI CIDEr-EN keeps the full split.
   OpenViVQA-dev images that overlap an earlier owner or are lost (§8.1) leave the proxy at every tier (count only).
4. Methods: id join where id spaces are shared (G-A); W25 RULE §3 otherwise. Features and ids only. Counts only,
   never reason text in the paper (PI-1101o/p).

### 7.3 Counts kept apart (N22)
(a) G-A id overlaps (removed before G-B); (b) W25-flagged NoCaps-test images vs earlier owners, plus lost images (§8.1), each counted separately (n_e_power, §5.6);
(c) §7.4 self-retrieval removals from D-VI / D-EN / D-TC (datastore side only). Each is printed separately.

### 7.4 Datastores and the self-retrieval rule (v3 §9.2 l.369-388; v4.1 §9.2; CC-214r2 ruling 3)
- **D-EN** = `cen_memory_allowed.tsv` (175907e2) minus restval (B4, incl. T2-2000) and UIT-ViIC ids = 80,083
  (PORTFOLIO l.193). **D-VI** = KTVIC train + OpenViIC train human captions, minus B's H-500 and every other owner's
  ids, no UIT-ViIC train pool (v4.1 l.349). **D-TC** = TextCaps train captions minus T_A, T_B and their W25
  near-duplicates; serves T_A only (v4.1 l.348). D-VI and D-TC counts are printed by `c_pvr.py lists` and pinned by sha.
- **Rule (fixed now, every tier):** each query image and its W25 near-duplicates (RULE §3, C1 ∨ C2 ∨ C3) are removed
  from every datastore. Enforced at set level once, before tier 1: datastore used = D − (every image of every C query
  set of §4 and §8 and their W25 near-duplicates). Pending before any decode (v4.1 l.369-374): W25 for NoCaps test ×
  D-VI and × D-EN; XM3600 × D-VI; NoCaps val × D-VI; every Vietnamese query set × D-VI; C3 for KT-C × D-EN.
- SESOI_P, headroom and the go/stop are computed only after this rule; any tier-1 output made before it is discarded.
  Removals are reported as counts only.
- **Hosts:** NoCaps-test and OpenViVQA-dev features on the laptop (§8); custody dev sets (XM3600, KT-C, KTVIC test,
  OpenViIC test) on the laptop CPU or M1; non-custody images (KTVIC/OpenViIC train, TextCaps train, ViTextVQA dev) on
  M1 in the C block, or on the laptop. Other owners' features come only from sha-pinned caches, recomputed only on the
  host that already holds that set; comparisons run on the laptop.

## 8. Custody (N21; CC-209 Ruling 1(a), l.95-104; CC-217r2 B1)

- **Standing rule applied:** test images, spent test sets in a dev role included, sit only on M1 (the test-capable
  GPU host) or the laptop (the data home) (CC-209 l.11, l.95-104). C's unspent one-look sets never go to a host that
  runs another paper's job (CC-217r2 B1 precedent; B PA1 v3 l.286-288).
- **Named custody host for the W25 pixel step of NoCaps test and OpenViVQA dev: the laptop** (WSL2, ext4 home, 4
  vCPU / 20 GB). This is the prereg that first downloads these pixels, so this is where the host is named (NB1
  rewording of v4.1 l.327).
- **OI-test fetch URL (B3, CC-220 l.53).** `cen_fetch.OI_URL` (cen_fetch.py l.51) points at OI `validation/` only, and
  `w25.py` l.163 calls it; NoCaps test is OI test only (v4.1 l.179). C therefore registers its own constant
  `OI_TEST_URL = "https://open-images-dataset.s3.amazonaws.com/test/{file}"` in `scripts/c_pvr/c_pvr.py`, pinned by
  value and by the file sha in PINS-A. Only the URL template differs: the fetch call is the unchanged `cen_fetch.get`
  (no redirect, status 200, JPEG body; RULE §1), and features and rule are the unchanged W25 functions
  (`build_memory.features`, RULE §3 C1-C3); `cen_fetch.py` and `w25.py` are not edited. Before each request,
  `c_pvr.py w25` asserts the id is in G-A's OI-test list (`ga_remaining_ids.txt` ∩ the official OI test id list);
  any id outside it = FAULT. No substitute source (no other bucket, mirror or the NoCaps CDN). How each fetch outcome
  is classed is fixed **once**, in §8.1; no other section restates it. OpenViVQA-dev images come only from the
  PINS-A-pinned HF revision (NB-OVQA), same tmpfs rule.
- **Batches.** <= 512 images (as RULE l.70) into `/dev/shm/c_pvr_w25/b<NNNN>/` (tmpfs), features computed, each batch
  unlinked as soon as its features exist, each deletion logged in `~/.vsps_sealed/c_pvr/w25_deletions.log` (utc,
  folder, file count); a trap deletes `/dev/shm/c_pvr_w25` on any exit.

### 8.1 Fetch outcomes, lost images and FAULTs (the single statement of this rule; CC-220r2 N-B1)
- **Amendment of CC-220 B3's 404 clause (CC-220r2 Ruling 3, option (a); the round-3 panel rules on it).** CC-220 B3
  (l.53) reads "A 404 or non-JPEG response is a FAULT, with no substitute source". The unchanged `cen_fetch.get`
  cannot tell a 404 apart: `OPEN = urllib.request.urlopen` (cen_fetch.py l.60) raises `HTTPError` on a 404, and
  every exception is returned as its class name (l.248-249), the same string a 5xx gives. The clause is therefore
  amended to: **"Any exception after `get`'s three tries is a lost image under the lost cap; `get`'s explicit
  outcomes 'status N', 'redirected' and 'not a JPEG body' are a FAULT; no substitute source."** This matches the
  house definition of a lost image in RULE l.50 and keeps `cen_fetch.py` unedited.
- **Outcome classes of `get(url)` (cen_fetch.py l.236-251, three tries, the last try's string is returned):**

  | `get` returns | source line | class |
  |---|---|---|
  | bytes, `""` | l.246-247 | fetched |
  | `f"status {status}"` (a non-200 status without an exception) | l.242-243 | FAULT |
  | `"redirected"` (final URL differs) | l.242-243 | FAULT |
  | `"not a JPEG body"` (no JPEG SOI) | l.244-245 | FAULT |
  | `type(e).__name__` of any exception (e.g. `HTTPError` for 404 or 5xx, a timeout class) | l.248-249 | lost |

  A fetched body that the unchanged W25 feature code cannot decode is also lost. An id outside G-A's OI-test list is
  a FAULT before any request (§8).
- **XM3600 sha-refuse backstop (NB-SHAREFUSE; w25.py l.157-169, CC-153 r4).** C's fetch loop carries `w25.fetch`'s
  rule unchanged: the refuse set is `exclusion.json` `image_sha256.xm3600_all_images` (the 3,600 XM3600 image
  sha256s; loaded as `w25.xm_shas()`, w25.py l.80-83; `manuscript/prereg/2026-10-21_dev_pools/exclusion.json` sha256
  `c52a96d1`), and a body whose sha256 is in it is never written and is a FAULT ("the id drop missed it").
- **What a lost NoCaps-test image does:** it is counted and reported; it counts as W25-flagged for n_e_power (§5.6);
  and it **leaves P_obj^VI, R_obj^VI and the local proxy at every tier, count only**, exactly as a W25-flagged
  image does (§7.2 rule 3). It is never scored locally at tier 1, 2 or 3, even if a later fetch succeeds.
- **Lost cap, NoCaps test:** more than **10** lost (0.1% of 10,600, the RULE l.50 OIV7 rate) is a FAULT: `w25` stops
  and the case goes to the PI [proposal on the rate reuse].
- **Disclosed departure from RULE l.50.** RULE l.50 also says "KV and UT must have 0 lost (FAULT otherwise)". KV and
  UT are protected there: a lost UT image could enter training unchecked, and a lost KV image would leave a protected
  test image unchecked. C's NoCaps test is not in that position: a lost image is excluded from every local metric at
  every tier, so a loss can only shrink n, never put an unchecked image into a C metric. That is why a cap above 0 is
  used for C and disclosed here. The one place a lost image can still appear is EvalAI CIDEr-EN, which keeps the full
  split by rule (v4.1 l.322) and is a benchmark, never a gate; for those images the W25 and self-retrieval checks
  could not be run, and their count is reported beside CIDEr-EN.
- **OpenViVQA dev (NB-OVQALOST).** Images come only from the PINS-A-pinned HF revision; PINS-A also records the hub's
  LFS sha256 of each image file or archive at that revision (metadata only, no download), and a downloaded file whose
  sha256 differs is a FAULT. An image listed in the dev json but absent from the pinned files, or
  not decodable by the W25 feature code, is lost: counted, reported, and it **leaves the proxy at every tier, count
  only**. More than **1** lost (0.1% of 1,070, rounded down) is a FAULT [proposal]. The XM3600 backstop applies to
  this loop too.

### 8.2 Single tenancy, enforced (B4, CC-220 l.54; CC-219r3 NB1 l.54; NB-GBTENANCY)
The same five steps govern **two windows**: the W25 pixel window (`c_pvr.py w25`, tmpfs `/dev/shm/c_pvr_w25`, lock
`/dev/shm/c_pvr_w25.lock`) and the G-B window (`c_pvr.py gate-b`, tmpfs `/dev/shm/c_pvr_gb`, lock
`/dev/shm/c_pvr_gb.lock`; §9.6).
  1. Before the window opens, the coordinator writes a LOG line pausing every other paper's laptop job for that
     window; the subcommand refuses to start unless that LOG line exists (checked by its OPS tag and utc stamp) and no
     foreign `*_job.sh` process is live.
  2. The subcommand holds an exclusive flock on its lock file, re-checked **at every batch** (W25) or **before and
     after each streamed CSV and before the single read** (G-B); if a foreign `*_job.sh` process appears at any check,
     it aborts, the trap deletes its tmpfs folder, and the abort is logged. An aborted G-B prints nothing; running it
     again is a re-download and needs its own irreversible ruling (§9.6).
  3. Both tmpfs folders are created mode 0700.
  4. The `gpu_backup` loops are the only allowed concurrent processes, and only because they pull remote hosts and
     never read either tmpfs folder (checked once before each window: their scripts contain no `/dev/shm` path).
  5. All agents run under one laptop uid, so this isolation is **procedural**, not an OS boundary; this is recorded.
### 8.3 W25 runtime stop, GPU host and alternatives
- **W25 wall-clock stop (NB-W25STOP).** Cap = **24 h wall-clock** for the whole laptop pixel W25 (NoCaps test +
  OpenViVQA dev) [proposal]. After the first batch, `w25` projects the total = elapsed for batch 1 × (total images /
  batch-1 images) and logs it; if the projection exceeds 24 h, or the running total reaches 24 h, `w25` stops, the
  trap deletes tmpfs, the features already made are kept, and Q-custody goes to the PI. No restart on the laptop
  without a new LOG pause line and the PI's answer.
- **Spent-test dev decodes** (XM3600-vi, KT-C, KTVIC test, OpenViIC test) **run on M1 only**, after MT4 and B's M1
  custody block release it, never while another paper's job is live or queued on it. T_A and ViTextVQA dev (not test
  sets) run in the same M1 block, so tier 1 has **one named GPU host: M1**. M1's GPU class differs from the 4090 the cap
  was sized on (CC-209 l.29-30); the speed test restates the projection (§10).
- **If M1 lapses or is never free:** the tier-1 GPU block is reported NOT RUN; no substitute host is used except
  through the Q-custody amendment below; nothing is shrunk to fit (full-split rule).
- **M8 is never used by C** while VSPS-J E2b or B tier-1 jobs run, and M8's maximum rental ends 2026-11-15 21:20 VN
  (LOG l.1109).
- **Alternative only by amendment:** if the PI answers Q-custody YES, an amendment with a one-judge read names one
  dedicated single-tenant rental (id recorded before any pixel moves), isolated tmpfs, no other paper's job while it
  holds pixels, logged deletion after the pull. Until then no C pixel or decode goes to a rental.
- No host, IP or port is written in the repo; "M1" and "laptop" are the only names used.

## 9. Gates, order and exact inputs/outputs

### 9.1 Order (CC-219 R8, R10 over v4.1 l.388, l.390, l.449, l.608)
1. **G-C1** desk read (model cards, technical reports, published SFT lists; no data) — first, before anything else.
   If no VI captioner or no VI verifier can still become CLEAN, STOP here.
2. **G-D** id check (ids only).
3. **G-A** NoCaps-test id join (ids only).
4. **G-C2** OI-id join of the public SFT image lists named in G-C1 against G-A's NoCaps-test OI ids (ids only). Any
   HIT or UNCHECKABLE removes that model for NoCaps test. No CLEAN VI captioner or verifier -> STOP.
5. **PINS amendments (NB-PINSTIER), gatekeeper LOG line with shas each:**
   - **PINS-A** (one-judge read): captioner and verifier (hub id @ revision), prompts, k = 4, greedy, decomposers, EN
     map (N13), proxy regex/extractor and `rapidfuzz` version, retrieval encoder (NB-ENC), OpenViVQA revision + 3 json
     shas + image-file LFS shas (NB-OVQA, §8.1), `OI_TEST_URL` and `c_pvr.py` sha (B3), parity input shas (NB-PARITY), the M1 cap re-base rule
     (NB-CAP).
   - **PINS-B** (full panel at 92): `gates.py` sha, i.e. the one test-gold read (G-B, its stream filter of §9.6 and
     the sealed-file writer) [registered default; the PI may relax it via Q-PINS].
6. **Q11 answered YES** (PI line + ledger ruling >= 92). Under the default HOLD: C stops after step 5; G-B never runs
   (no test-gold exposure for a branch that cannot reach tier 2), and no C GPU work runs on any host.
7. **G-B** once, laptop CPU, under the §8.2 tenancy steps (§9.3, §9.6).
8. Pixel W25 (laptop, §8) and dev-set W25 / self-retrieval (§7.4); then the M1 tier-1 block (§10).

### 9.2 Gate table

| gate | runs on | reads | writes / prints |
|---|---|---|---|
| G-C1 | laptop, web | model cards, reports, SFT lists | `G_C1_record.json`: per model × set {CLEAN-candidate, HIT, UNCHECKABLE} with source URLs and dates; committed before G-D |
| G-D | laptop CPU | ids only | copies `idcheck.py` / `idcheck_out.txt` to `scripts/c_pvr/`, re-runs, compares bytes: equal to 13d59e15 or the diff is reported |
| G-A | laptop CPU | public `nocaps_test_image_info.json` and `nocaps_val_image_info.json` (ids and OI ids only; shas pinned at download; the NoCaps val captions file on disk is never opened); official OI test image-id list; 4b7a1813; the 3,600-id list (§2.2, step 0 asserts); 54966ca7 | counts: NoCaps test in OI test / OI val / other; overlaps with the 41,164 of L2-P1 (RULE l.19), with the 3,600 XM3600 ids (≈118 expected by chance: 1,399 × 10,600 / 125,436; v4.1 l.196), with NoCaps val; remaining count. Writes `ga_remaining_ids.txt` (ids only, sha in LOG) |
| G-C2 | laptop CPU | G-C1 SFT id lists; `ga_remaining_ids.txt` | per model: HIT count, CLEAN / HIT / UNCHECKABLE; appended to `G_C1_record.json` |
| G-B | laptop CPU, once | `oidv7-{val,test}-annotations-human-imagelabels.csv` streamed from the bucket and filtered to `ga_remaining_ids.txt` in the stream (full files never stored; §9.6); md5 vs bucket; 27f2b1ca | see 9.3; CSV custody 9.6 |

### 9.3 G-B (one run; aggregates only; sealed)
- Preconditions: this prereg committed (CC-219 R5, l.49; the coverage rule is ruled, Q2 FYI in §14); parity selftest
  passed (§3.3); PINS-A and PINS-B committed; Q11 = YES; `gates.py` sha equals PINS-B.
- **Prints and writes only:** n_e(G-B); total verified present pairs; total verified absent pairs; coverage share
  n_e(G-B) / remaining images. No per-class or per-image NoCaps-test count or file, except the single sealed
  intermediate of 9.4. The XM3600 build path (`pairs_per_class` l.161; per-image LABELS l.174-176) is barred by name
  and by a selftest that fails if those keys are emitted.
- The four numbers go to `gb_counts.json` and a LOG line. No vocabulary change after G-B (W3).
- Power check at tier 2 uses n_e_power (§5.6). If P(PASS) < 0.98: no tier 3 for P_obj^VI; C stops (v4.1 l.171).

### 9.4 The sealed intermediate (N17; NB-W25 (ii))
- **Exactly one file:** `~/.vsps_sealed/c_pvr/gb_intermediate.json` on the laptop's WSL ext4 home (not `/mnt/d`,
  where chmod is unreliable), written once by G-B with sorted keys and fixed separators (deterministic bytes): for each
  G-A-remaining NoCaps-test id with >= 1 verified label on a mapped class, its mapped-class present / absent sets. Mode
  0400 after writing. Never printed, never copied, never in the repo or any backup.
- sha256 recorded in `manuscript/prereg/2026-11-02_c_pvr_tier1/GB_SEALED.sha256` (gatekeeper commit right after G-B)
  and in the LOG.
- **Access log:** `~/.vsps_sealed/c_pvr/ACCESS_LOG.tsv`, append-only (utc, actor, action, sha); a LOG line mirrors each
  entry. Allowed entries for the sealed file: `write` (G-B) and **one** `open` at the tier-3 freeze; the same log also
  records the `unlink` of the filtered CSVs (§9.6) and each OpenViVQA json read (§4.3).
- **The one open** (pinned tier-3 code): verify the sha, compute the exact W25 difference n_e(G-B) − n_e(after W25)
  (report-only; gates nothing), and build the tier-3 label table. **This file is the sole tier-3 label source** for
  P_obj^VI and R_obj^VI [accepted, CC-220 Ruling 2 (P1)], so the primary outcome has exactly one read of test gold.
- **Deletion is barred** (CC-219r3 NB2, l.55). **Loss branch:** if the file is missing or fails its sha,
  the exact W25 difference is reported "NOT COMPUTED" and is never re-derived; tier 3 for P_obj^VI then needs its own
  irreversible ruling on a label source (no silent re-read).
- **Reconciliation (CC-220 Ruling 4, l.44):** if such a ruling ever allows re-derivation, it must start from a fresh
  download whose full-stream CSV shas (sha256 and md5) equal those logged at G-B (§9.6) and must reproduce
  `GB_SEALED.sha256` byte for byte; otherwise the result stays NOT COMPUTED. CC-219r3 NB2 (N17) is CLOSED for the
  sealed file itself (CC-220 Ruling 4).

### 9.5 English benchmark on EvalAI (registered now for the tier-3 prereg; v4.1 §8)
- Same registered look as the Vietnamese arms. Five named arms, one submission each: S1 PVR (chosen UNCERTAIN
  variant), S2 A8, S3 A1, S4 A0, S5 A6. No resubmission; a submission that fails format is reported "missing", never
  replaced. A format checker runs first on NoCaps val (only after Q11 = YES).
- CIDEr-EN rule (benchmark, not a gate): point estimates only, full split; CIDEr(S1) − CIDEr(S2) >= −δ_C and
  CIDEr(S1) − CIDEr(S3) >= −δ_C (δ_C = 2.0); reported pass or fail; no CI.
- The lifetime submission cap is verified on the NoCaps EvalAI page in the tier-3 prereg, with the read date (W13). A
  higher cap still means 5 arms; a lower cap cuts S5, then S4.
- Account: Q6 (§14). No NoCaps-test look without it.

### 9.6 Test-gold CSV custody and lifetime (B2, CC-220 l.52; v4.1 l.395 = CC-219 W2)
- **Stream-filter at download (house pattern `data/datasets/xm3600/oiv7/fetch.sh`, sha 75c22a08).** For s in {val,
  test}: `curl -sSL https://storage.googleapis.com/openimages/v7/oidv7-$s-annotations-human-imagelabels.csv` is piped
  through `tee` into `sha256sum` and `md5sum` (full-stream hashes) and into an `awk` filter that keeps the header and
  the rows whose ImageID is in `ga_remaining_ids.txt` (fetch.sh's `NR==FNR{ids[$1];next} FNR==1 || ($1 in ids)`).
  **The full CSV is never written to any disk.**
- The filtered rows go only to `/dev/shm/c_pvr_gb/filtered-$s.csv` (tmpfs, directory mode 0700), never under
  `/mnt/d`, `data/`, the repo or any backup path. G-B reads them **once**, then unlinks them and the directory before
  it exits; a trap unlinks them on any exit.
- The full-stream md5 is compared with the bucket's `x-goog-hash` md5 **and** with the on-disk md5 records
  `data/datasets/xm3600/oiv7/full-val.md5` (sha256 `5770ed7c`) and `full-test.md5` (sha256 `2eebd937`), both pinned in
  §2.3 (NB-MD5). Any mismatch = FAULT, and G-B does not run. The full-stream sha256 and md5 and the filtered files'
  sha256 are written to `gb_counts.json` and the LOG.
- The whole G-B window runs under the §8.2 tenancy steps 1-5 (coordinator pause line, flock `/dev/shm/c_pvr_gb.lock`
  re-checked before and after each stream and before the read, abort + trap-delete, mode 0700, gpu_backup check)
  (NB-GBTENANCY).
- The deletion of the filtered files is logged in `~/.vsps_sealed/c_pvr/ACCESS_LOG.tsv` (utc, actor, `unlink`,
  sha) and mirrored in the LOG.
- `score` and every subcommand after G-B **refuse** any input path matching `oidv7-*-annotations*` or
  `/dev/shm/c_pvr_gb/` (selftest checks the refusal). The only test-gold artifact that survives G-B is the sealed
  intermediate of §9.4.
- **Any re-download** of these CSVs needs its own irreversible ruling (>= 92), with the Ruling-4 conditions above.

## 10. GPU, cost and schedule (N12; v4.1 §11)

### 10.1 Tier-1 block (M1, after Q11 = YES and step 8 of 9.1)
- Speed test <= 1.0 GPU-h: 200 XM3600-vi images × every VI arm + 200 KT-C images × S1-S5 (v4.1 l.456). **Its
  outputs are discarded, never scored or read (NB-SPEED)**; only seconds per caption per arm are kept.
- **Cap (CC-220r2 N-B2; the rule is pinned in PINS-A before the speed test and any output).** P1 = projected tier-1
  GPU-h on M1 from the speed-test throughput only (never from any output).
  - **If the PI answers Q-cost = YES:** cap = min(⌈1.25 × P1⌉, 37) GPU-h (one re-base for M1, NB-CAP; 37 = the money
    ceiling <= 350k VND at 9,282 VND/h, LOG l.1109; MT4 AMENDMENT_COST precedent as cited in CC-220 l.58).
  - **Otherwise (the default):** cap = **20 GPU-h hard** (v4.1 l.457; about 186k VND on M1).
  - In both cases, if ⌈1.25 × P1⌉ exceeds the cap, arms are cut in the order of §5.1 until it fits; if it still does
    not fit, the PI decides before any decode (no set is shrunk). Projection before every block; a cap stop is final;
    one resume only for machine loss.
- STOP conditions: cap; balance < 3 GPU-h; two failed restarts; M1 needed by A, B, MT4 or a custody block; headroom
  < 2 points (v4.1 l.461).

### 10.2 Cost restated (CC-219 l.31, l.84; CC-219r3 l.61)
- **C total ≈ 155-195 GPU-h (4090 hours) ≈ 2.7-3.4M VND** at 17,499 VND/h (LOG l.1109) [est.].
- **Tier 1 on M1** (9,282 VND/h, LOG l.1109): default 20 GPU-h hard ≈ 186k VND; only with Q-cost = YES, the
  re-based ceiling <= 37 GPU-h ≈ <= 350k VND (§10.1) [est.; arithmetic 20 × 9,282 = 185,640; 350,000 / 9,282 = 37.7].
- Budget separately from M8 (maximum rental ends 2026-11-15 21:20 VN, LOG l.1109).
- Laptop W25 for NoCaps test (10,600 images) and OpenViVQA dev (1,070) on 4 vCPU: runtime unknown [est.: not
  estimated]; projected after the first batch and stopped at the 24 h wall-clock cap (§8.3, NB-W25STOP).

### 10.3 Priority (N15)
A and B first on agent-days and GPU time; C's M1 block queues behind MT4, B's M1 custody block and any A job.

## 11. Run commands (after GO; names fixed now)
```
python3 scripts/c_pvr/test_c_pvr.py                       # CPU selftest: no weights, no data, sockets raise
python3 scripts/c_pvr/c_pvr.py gate-c1 --record G_C1_record.json
python3 scripts/c_pvr/c_pvr.py gate-d
python3 scripts/c_pvr/c_pvr.py gate-a --info <nocaps_test_image_info.json> --val-info <nocaps_val_image_info.json> --oi-test-ids <ids>
python3 scripts/c_pvr/c_pvr.py gate-c2
python3 scripts/c_pvr/c_pvr.py ovqa-pin                          # NB-OVQA: revision + 3 json shas, 1,070 / 3,545 asserts
python3 scripts/c_pvr/c_pvr.py parity --xm3600-csv-dir data/datasets/xm3600/oiv7   # N3 parity, shas per PINS-A
python3 scripts/c_pvr/c_pvr.py gate-b --stream --pause-tag <OPS tag>   # once; §8.2 tenancy; stream-filter to /dev/shm/c_pvr_gb, unlink after (§9.6); refuses if gb_counts.json exists
python3 scripts/c_pvr/c_pvr.py owners && python3 scripts/c_pvr/c_pvr.py lists
python3 scripts/c_pvr/c_pvr.py w25 --host laptop --pause-tag <OPS tag>   # §8 URL, §8.1 outcomes, §8.2 tenancy, 24 h stop
GPU=M1 bash scripts/c_pvr/c_pvr_job.sh --selftest && GPU=M1 bash scripts/c_pvr/c_pvr_job.sh speed
GPU=M1 bash scripts/c_pvr/c_pvr_job.sh tier1
python3 scripts/c_pvr/c_pvr.py score --tier 1                     # laptop; asserts RESCAP_RAW_TONE unset
```
`gate-b` and `score` refuse to run if any SUMS file, PINS sha or `gates.py` sha differs; `gate-b` refuses a second
run; every subcommand after G-B refuses `oidv7-*-annotations*` and `/dev/shm/c_pvr_gb/` paths (§9.6). Every output
carries the tier label.

## 12. What tier 1 decides and cannot claim
- **Decides (in order):** (i) SESOI_P = max(1.0 point; 0.25 × (P_obj^VI(A12) − P_obj^VI(A1))) on XM3600-vi after
  §7.4 self-retrieval, fixed at the end of tier 1 (v4.1 l.453); (ii) headroom: A12 − A1 < 2 points -> STOP before tier
  2 (v4.1 l.246); (iii) UNCERTAIN variant (§6.3); (iv) go to tier 2 iff point ΔP_obj^VI(PVR − A8) >= SESOI_P on
  XM3600-vi (v4.1 l.452). The proxy rule is fixed before the first output.
- **In-sample label (NB-INSAMPLE):** SESOI_P, the UNCERTAIN choice and the go/stop are in-sample selections on
  XM3600-vi; they are labelled so in every output. Tier 2 (fresh data, frozen config) is the confirmation.
- **Cannot claim:** any test or tier-3 result; any NoCaps number beyond G-A/G-B counts; reference-based Vietnamese
  quality. XM3600-vi P_obj^VI may be optimistic because the map was built on XM3600 (v4.1 l.197).
- **NB-LEDGER (coordinator obligation):** the next PORTFOLIO §2.3 edit records ViTextVQA dev as spent by L1 (C_TEST
  l.30).
- **NB-STATE / N15 (coordinator obligation after GO; CC-220r2 l.153):** the stale `STATE_2026-11-01` C row (l.18) is
  refreshed by the coordinator after this prereg's GO (PI-1101u, CC-219r3 and the files win over it). This draft does
  not edit STATE.

## 13. Overrides of v4.1 and conflicts found (stated, not silent)

| # | v4.1 line | what this prereg does | ground |
|---|---|---|---|
| O1 | l.327 "máy test của C ... ghi tên trong prereg tầng 3" | host named in the prereg that first downloads the pixels (this one: laptop, W25 only) | CC-219r3 NB1 l.54 |
| O2 | l.450 "không chạm ... bất kỳ tập test nào" | amended: the W25-only pixel step on NoCaps test and OpenViVQA dev is allowed (features only) | CC-219r3 NB1 |
| O3 | l.390, l.449 "G-A, G-B, G-C theo thứ tự" | G-C1 first; G-C2 after G-A (it needs NoCaps-test OI ids); both before G-B | CC-219 R10 l.54; CC-219r3 Ruling 5 l.45 |
| O4 | l.388, l.608 "Q11 trước prereg tầng 2" | Q11 before any C GPU work and before G-B | CC-219 R8 l.52 |
| O5 | l.455-457 "một RTX 4090" for tier 1 | tier-1 GPU host = M1 (spent-test dev sets may not go to a rental) unless Q-custody YES | CC-209 Ruling 1(a) l.95-104; CC-217r2 B1 |
| O6 | l.256 "ảnh Open Images val và test" | stale; NoCaps test = OI test only (l.179), G-A confirms | CC-219 W1 |
| O7 | v3 l.143 "ViTextVQA dev ... không có trong sổ" vs C_TEST l.30 "Dev đã dùng ở L1" | ViTextVQA dev treated as an earlier owner for OpenViVQA-dev overlaps | CC-219 W1 logic |
| O8 | v3 §9.2 "chép ... sha của 3 file đó" | v1.1: the 3 OpenViVQA json files are pinned (HF revision + 3 sha256, 1,070 / 3,545 asserts, else FAULT) before any OpenViVQA byte is used (§4.3); v1's "else disclosed missing" is struck | CC-220 Ruling 3, NB-OVQA |
| O9 | l.395 "chỉ giữ sha" | the one sealed intermediate (§9.4) is the named exception; the raw CSVs are never stored (§9.6) | CC-219r3 NB2 l.55; CC-220 B2 |
| O10 | l.395 timing of the sealed file vs tier-3 scoring | sealed file = sole tier-3 label source | CC-220 Ruling 2 (P1 accepted) |

**CC-220 Ruling 2 (l.42): accepted overrides.** O3 (G-C split), O4 (Q11 before any C GPU work and before G-B), O5
(tier 1 on M1 unless Q-custody YES), O7 (ViTextVQA dev an earlier owner), P1 (sealed file = sole tier-3 label source)
and P2 (G-B held until Q11 = YES) are ACCEPTED by the panel. They override v4.1 l.256, l.388, l.390, l.449, l.608
explicitly; v4.1 l.256 is superseded by this prereg (O6).

## 14. Questions for the PI (each with a recommended answer and a default)

| # | question | recommended | default |
|---|---|---|---|
| Q-custody | May C's NoCaps-test and OpenViVQA-dev pixels (W25, later tier-3 decode) and C's spent-test dev sets (tier-1 decode) sit on one dedicated single-tenant rented 4090, named by amendment before any pixel moves, isolated tmpfs, no other paper's job, logged deletion after the pull? Also asked automatically if the laptop W25 hits its 24 h stop (§8.3) | YES, on M8 after VSPS-J E2b frees it (about 11-15) or on a new rental; removes the 3090 cap squeeze and the open-ended laptop runtime (CC-220 l.86) | laptop for W25 (B4 enforced), M1 for every C decode |
| Q-PINS | Should the PINS amendment that pins `gates.py` (the one test-gold read) get a full 92 panel? | YES for PINS-B (`gates.py`); one judge for PINS-A (prompts, models) | registered as written here: PINS-B at 92; if the PI relaxes it, a one-judge read plus a note (CC-220 l.88) |
| Q11 | Correct L2-P1 to 36,707 images (41,164 − 4,457; RULE l.19) and release NoCaps val to C as its tier-2 rehearsal, by a ledger ruling >= 92, before any C GPU work? | YES | HOLD: C stops after PINS; no G-B, no C GPU work |
| Q5 | What counts as checkable? | CC-219 Ruling 6 | Ruling 6 for shortlisting; tier-3 registration waits for your line |
| Q2 (FYI) | Coverage rule (one G-B count + power at n_e_power) was ruled by CC-219 R5; do you overrule it? | no | CC-219 R5 stands |
| Q-a | G-C1 desk read first, before more agent-days | YES (this order) | G-C1 first |
| Q-cost | Accept a C tier-1 cap re-based on M1 to min(⌈1.25 × P1⌉, 37) GPU-h (<= 350k VND) and a C total ≈155-195 4090-GPU-h (≈2.7-3.4M VND) [est.] after A and B? This answer sets the registered cap directly (§10.1, CC-220r2 N-B2) | YES | 20 GPU-h hard cap (≈186k VND), arms cut in the §5.1 order; if it still does not fit, you decide before any decode; no C spend before Q11 |
| Q6 | EvalAI account (tier 3 only): a group-managed research address, not the PI's and not the example.org placeholder | YES | no NoCaps-test look until it exists |
| Q7 | ViTextCaps: weekly recheck; cutoff at the tier-2 prereg freeze with a passing dev rehearsal | tier-2 freeze | tier-2 freeze |

## 15. Questions for the panel (each with a recommended answer and a default)

| # | question | recommended | default |
|---|---|---|---|
| P1 | Sealed intermediate as the sole tier-3 label source (one test-gold read), loss branch = no silent re-read | YES | YES |
| P2 | G-B waits for Q11 = YES (no test-gold exposure on a branch that stops) | YES | YES |
| P3 | G-C split into G-C1 (first) and G-C2 (after G-A), instead of joining against the whole OI test list | split | split |
| P4 | T_A and O_B at 1,070 images each (= OpenViVQA dev) by sha order | YES | YES |
| P5 | Proposed values: 5.7 flag 5.0 points, VI-script guard 0.95, Holm two-sided α 0.05, seeds 20261102 (CI) / 20261103 (outer draws) / 20261104 + r (inner CIs), lost-image FAULT > 10 (NoCaps test) and > 1 (OpenViVQA dev), laptop W25 wall-clock cap 24 h | accept | accept (fixed at registration, CC-220 Ruling 3) |
| P6 | One tier-1 GPU host (M1) rather than splitting T_A / ViTextVQA dev onto a rental | M1 only | M1 only |

P1-P4 and P6 were accepted by CC-220 Ruling 2-3; they stay listed for the record.

## 16. Gatekeeper checklist at registration (NB-COMMIT, CC-220 l.67)
- The commit message declares fixed as written: every [proposal] value (P5 list), T_A and O_B at 1,070 images, the
  seeds, and that counted-after-GO values are pinned by sha in `c_pvr_lists.json` before the first decode (CC-220
  Ruling 3).
- **Byte-equal commit (NB-RESTAMP; CC-218, CC-217r3):** this file is committed exactly as judge-read, sha256 equal to
  the round-3 subject. Nobody restamps or edits it at registration; the "Written" stamp in the header is the v1.2
  stamp. The commit line governs the DRAFT status line (CC-209c).
- **Sole registered prereg (NB-V1COMMIT):** the commit message names `PREREG_DRAFT_v1_2.md` with its sha256 as the
  only registered C tier-1 prereg. v1 (`PREREG_DRAFT.md`, fefccf22) and v1.1 (`PREREG_DRAFT_v1_1.md`, 8203ca11) are
  records only, kept in `.session_backup/2026-11-02/snap/` (`C_tier1_PREREG_DRAFT_fefccf22.md`, `C_tier1_PREREG_DRAFT_v1_1_8203ca11.md`); they
  are not committed as prereg; their working copies in this folder are not added to git.
- 8-gram / 6-gram scan of this file with positive controls, result in the commit message.
- No LOG line is written by the drafter.
