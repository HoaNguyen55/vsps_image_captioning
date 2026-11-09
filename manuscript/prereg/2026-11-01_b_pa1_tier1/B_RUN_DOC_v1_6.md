# B-PA1-T1 tier-1 GPU block run document v1.6 (Paper B, LRE; HB-T1, live re-entry for block W)

Status: **DRAFT v1.6, not read, not registered, licenses nothing.** The live run stays under the registered v1.5
until this file is read GO and registered (§0.4b).
- It supersedes the registered `B_RUN_DOC_v1_5.md` (b2d91672, commit fd60098, CC-305 GO 88) and, before it, v1.4
  (d1b0211b, 55ff846), under which HB-T1 was rented; the records v1.3, v1.2, v1.1 and v1 stay. All are kept unchanged.
- v1.6 = v1.5 + the W import-chain fix of the §1.4 sparse set, after the W stop at l.1939 (§0.4b, §A6). Finished
  2026-11-09T04:44Z (`date -u`) at HEAD `fd60098`; code `H_B″` = `860a3b741ecb82d8fbe31d997212965bc146404a` unchanged; LOG up to
  l.1939 (cited by line number only).
- It is filled from the B code with the F-4 fix (`-X utf8` on PYM / PYL / PYW in `b_pa1_job.sh`), read by CC-304 and
  committed as `H_B″` = **`860a3b741ecb82d8fbe31d997212965bc146404a`** (860a3b7, OPS-1109c-hbpp-commit l.1927) on
  top of `H_B′` = 6d674cedca8eb0a1d2897d102e2d052b2423b182 (F-1 / F-2 / F-3, CC-300 GO 90). P8 pin: §1.1 form.
- It follows C's `S11_RUN_DOC_v1_3.md` form. Nothing was rented, run or committed. No host, IP or port appears here:
  the aliases `hbt1` and `hbt1p` (re-rental) live only in `~/.ssh/config`.
- Every estimate and every [proposal] is AI opinion.

**Read order (§0.4b).** `H_B″`, its P8 pin (l.1928) and the R2 line (l.1934) stand. The **R-B read = the GO one-judge
FULL read of this file's sha (any round; REVERSIBLE 85)**; it also meets P2's FULL read. Then the P0 NGRAM line and
the registration commit of exactly this file. No new rental: HB-T1 (ckey 106594) continues at §0.4b.

Sources win over this file where they differ:
- `PREREG_DRAFT_v3_1.md` e9b30ca7 (5ff00c9);
- `AMENDMENT_R5_DRAFT_v1_2.md` 9cb21917 (3091bf6);
- `AMENDMENT_R6_DRAFT_v4.md` 0b55d5f8 (90ed1a6; R6-I/III ADOPTED l.1572-1573);
- `AMENDMENT_R6_PART2_CAP_DRAFT_v4.md` 0c5f919b (a030cc7; R6-II ADOPTED l.1585);
- `ERRATUM_LINEAGE_GEMMA3N_v1_2.md` 11c36760 (6e17728; OPS-1108b-erratum-pin);
- `D8_AMENDMENT_DRAFT_v1_3.md` c041c4ab (b242e0c; OPS-1108b-d8a-pin, -d8e-pin);
- `scripts/b_pa1/B_GPU_READINGS.md` 98642130 at `H_B″` (readings as ruled, the F-1 / F-2 / F-3 hunk map under CC-300 and
  the F-4 entry under CC-304);
- CC-295 … CC-295r4, CC-296 … CC-296r3, CC-300, CC-301 (v1.2 read), CC-301r2 (v1.3 read), CC-301r3 (v1.4 GO 89), CC-302, CC-303, CC-304, CC-299r2 R2-W8 (C-DIAG solvency form), and the PI
  lines of §0.1.

## Tóm tắt cho PI (tiếng Việt)

- Bản v1.3 sửa hai lỗi chặn của CC-301 (82 điểm): kiểm tra P19 chỉ quét lệnh, không quét lời văn; phần tiền theo
  PI-1109c: C-DIAG giữ trước khoản xấu nhất thật của B = W_B + O_B = 474.354 đ (403.680 + 70.674 cho một lần thuê lại).
- Bản v1.5: máy 106263 lỗi đọc (FAULT, CC-302), đã xoá, loại vĩnh viễn; máy HB-T1 mới 106594 đang chạy (trần 28 giờ,
  10.938 đ/giờ). Mã nay là `H_B″` (F-4: `-X utf8`, CC-304); chạy lại selftest trên cùng máy, không thuê máy mới.
- Số dư 1.079.499 đ sau khi nạp 500 nghìn: đủ cho nhánh trần 28 giờ. Nếu khối chẩn đoán C-DIAG của bài C (tối đa
  210 nghìn đ) chạy song song, phần còn lại của nó được trừ trước khi xét.
- Theo PI-1108h: khi số dư còn 50.000 đ, báo PI nạp tiền. Laptop bật 24/7.
- Theo PI-1108i: nếu mất máy, được thuê lại một lần (HB-T1′) sau khi một giám khảo đọc phụ lục mất máy.
- Câu hỏi mới cho PI: không có (§18; PI-1109d).
- Bản v1.4 (CC-301r2, 83 điểm): dòng `DOC=` nay chỉ đúng tệp này, để bước đăng ký P1 qua được; thêm vài câu chữ
  (NB1-NB4), không đổi tiền hay lệnh chạy nào khác.

## A6. v1.5 → v1.6 change table (W stop 1, l.1939)

| # | change | source | v1.6 section |
|---|---|---|---|
| Q1 | §1.4 sparse set adds the W import chain: `scripts/c_stage1/decode_icl.py`, `scripts/g2b/decode_qwen3vl.py`, `scripts/lb/decode_hf_vlm.py`, `scripts/match_openviic.py`, `scripts/evaluate.py` (decode_hf_vlm finds ROOT by it); FILL_SPARSE updated; the `data` / `manuscript` absence check stays | OPS-1109b-hbt1-w-stop1 l.1939; the coordinator's laptop probe | §1.2, §1.4 |
| Q2 | retry env `~/bpa1_env_3.sh`: guards on env_2 = 3aef29d7, sources it, overrides `DOC` (v1.6) and `HR` (`_3`), prints `ENV3 OK`; every block sources it | S11 `_2` rule, as v1.5 Z2 | §0.3, §1.3, every sh block |
| Q3 | §0.4b re-entry: `REENTRY v1.6`; P0-P2, P9, new P26; `$HR` `_3`; host `mv -n ~/b_pa1_repo ~/b_pa1_repo_hbpp`, transfer, host checks; no new selftest (code unchanged; HOSTCHECK binds code sha, freeze and GPU uuid, not the path); the stopped run's `RUN.w9.started` moved aside after checks; push w again; launch w | this event; job l.80, l.97-103, l.129-135 | §0.4b, §1.4, §4 |
| Q4 | P26: the W import chain runs from the exact sparse tree on the laptop (`feats --blocks 1` into a scratch dir writes part_0000 with 500 ids) | the coordinator's probe | §4, §0.4b |
| Q5 | §12.1: this stop's class (other JOB STOP from a run-doc defect, before any output; no resume used; W 1 s counted by `left --w`) and the decision under PI-1109d | job l.129-135, l.157-166; gpu `left --w`; PI-1109d, PI-1109f | §12.1 |
| Q6 | the decide1 pin form cites "B_RUN_DOC v1.6 §9.2" (not yet written); header and §19 | the file names itself | header, §9.2 step 5, §19 |

## A5. v1.4 → v1.5 change table (live run; F-4)

| # | change | source | v1.5 section |
|---|---|---|---|
| Z1 | code pinned to `H_B″` = `860a3b741ecb82d8fbe31d997212965bc146404a` (F-4): job 8ff70aaa, job selftest 56dba902, mutants 8b9b4c06, SHA256SUMS_GPU 8c39fae7, readings 98642130; gpu, models, mid, validator, setup, registry, locks and SHA256SUMS unchanged; the P8 pin form on SUMS_GPU 8c39fae7 (`pin_line` True on a scratch copy) | CC-304; `git diff 6d674ced -- scripts/b_pa1` (5 paths) | header, §1.1, §1.2, §4 P2, P3, P24 |
| Z2 | retry env `~/bpa1_env_2.sh` (S11 `_2` rule): sources the write-once `~/bpa1_env.sh` (51aad3fd) and overrides only `DOC` (v1.5), `H_B` and `HR`; every laptop block sources it; `$PRE`, `$X`, `$PUSHW`, `$PUSHA`, `$PULL`, `$S4` and `~/bpa1_env_w.sh` (WMAN 29da438e) stay | S11 §1.3 rule; v1.4 §1.3 | §0.3, §1.3, every sh block |
| Z3 | re-entry order on the live HB-T1: rebuild `$HR` at `H_B″`, move the H_B′ host repo aside, transfer, host checks; stale HOSTCHECK files moved aside; mode `selftest` again; the R2 line still to write | coordinator's v1.5 brief; CC-303 W4 | §0.4, §1.4, §8 |
| Z4 | kept facts: T0 2026-11-09T00:40:26Z, cap 28, RH 10,938, FEE 30, CAP.json 02193716, `~/b_pa1_out` (freezes, setup.log, frame) — no new rental, no repeated setup | OPS-1109b-hbt1-rent l.1919, -setup l.1920 | §0.4, §0.5 |
| Z5 | live events recorded: FAULT machine 106263 (CC-302 GO 90; deleted, 4,694 VND, excluded); HB-T1 = 106594, i5-14400F (PI-1109e); selftest stops 1 (CC-303 GO 87, prep2) and 2 (F-4); PI-1109e, PI-1109f rows | LOG l.1914-1925 | §0.1, §0.5 |
| Z6 | §6 step 2: the C toolchain and Python 3.12 headers are standard host prep, with the torch.compile probe after setup; part of HB-T1′ prep | CC-303 W1-W3, W5 | §6 step 2, §12.3 step 4 |
| Z7 | R1 / prompts pins stand (written at `H_B′`, registry 3651d1a8 unchanged); the R2 form names the first build at `H_B′` and the selftest at `H_B″` | registry unchanged; reading 4 | §4 P4, §8.3 |
| Z8 | the decide1 pin form cites "B_RUN_DOC v1.5 §9.2" (the line is not yet written) | the file names itself (CC-301r2 W1 rule) | §9.2 step 5 |

## A4. v1.3 → v1.4 change table (CC-301r2 NEXT_ROUND 83)

| # | change | source | v1.4 section |
|---|---|---|---|
| Y1 | **W1 BLOCKING.** `DOC=` names `B_RUN_DOC_v1_4.md` (the one `DOC=` line); no fenced block names an older run doc; the decide1 pin form cites "B_RUN_DOC v1.4 §9.2" | CC-301r2 W1, item 13 | §1.3, §9.2 step 5 |
| Y2 | **W1.** The R-B read = "the GO one-judge FULL read of this file's sha under CC-301 (any round)", not "round 2" | CC-301r2 W1, item 7 | header, §0.3 row 3, §4 P1 |
| Y3 | NB1: W_B + O_B is a planning reserve; B's binding check is §12.3 step 2 at the live RH′ + FEE′, and a shortfall there is a B wait, never an overspend; on HB-T1′, h_B and r_B are its own billed hours and RH′; O_B uses the rental line's FEE, not a literal 30 | CC-301r2 NB1, item 16 | §5.1, §17 D-19 |
| Y4 | NB2: under HB-T1′ no `logs/done.<IM>.*` of the interrupted mode is restored, so each of its steps runs again and skips what exists; this replaces v1.3's short-file rule (and its gpu line numbers); step 8's skip sentence follows | CC-301r2 NB2; job l.138; gpu l.303-317, l.500-520, l.715-765, l.777-837, l.840-846 | §12.3 step 5 |
| Y5 | NB3: the C-DIAG cap is cited from `C_DIAG_PREREG_DRAFT_v1_2.md` afbb61fb l.708-712 (or the registered C-DIAG file) | CC-301r2 NB3 | §3 RB11, §5.1, §17 D-19 |
| Y6 | NB4: one §14 line: under HB-T1′ the earlier manifests are checked on the `$PULL/snap_<mode>` copies | CC-301r2 NB4 | §14 step 4 |
| Y7 | header (version, supersedes v1.3, CC-301r2 in the read list, finish stamp), this table, one PI-summary bullet, the §19 v1.4 entry | this change | header, summary, §A4, §19 |

## A3. v1.2 → v1.3 change table (CC-301 NEXT_ROUND 82)

| # | change | source | v1.3 section |
|---|---|---|---|
| X1 | **W1 BLOCKING.** P19 greps only the commands: the ` ```sh ` blocks of this file (`awk '/^```sh$/,/^```$/'`) and the extracted pull loop `$PRE/bpa1_pull.sh`, for `pgrep -f`, `pkill` and `kill-session`; both give 0. Prose (P14, P19) is no longer counted | CC-301 W1, Ruling 4 | §4 P19 |
| X2 | **W2 BLOCKING.** C-DIAG's own check reserves B's real worst case once: W_B + O_B, W_B = max(0, 40 − h_B) × r_B, O_B = (4 + 1 + 2) × r_B + 30 or 0 once B's resume is used or its block ended; 403,680 + 70,674 = **474,354 VND** at planning rates. The PI's "~464k" assumed 6 h; the form binds. Dropped: "the two docs reserve the same money", the C-DIAG v1.1 `B_resume` bullet and the 403,680 reserve row | PI-1109c (l.1896); CC-299r2 R2-W8, Ruling 4; CC-301 W2 | §0.1, §5.1, §5.2, §5.3, §4 P25, §17 D-19, §18 |
| X3 | `hbt1-lbefore`, `hbt1-rent` and `hbt1-balance` lines log h_B, r_B, W_B, O_B and "B real worst case (PI-1109c) = W_B + O_B"; P25 reads the latest of them | CC-301 W2 | §5.1, §5.2, §5.4, §4 P25 |
| X4 | §0.1 adds PI-1109c (l.1896) and PI-1109d (l.1897, the four PI question kinds); §18 cites PI-1109d | LOG l.1896-1897 | §0.1, §18 |
| X5 | W3: the R-B read = the GO FULL read of this file's sha (CC-301 round 2); no extra read on the rental path; "CC-300 (when written)" → "CC-300" | CC-301 W3, Ruling 6 | header, §0.3 row 3, §4 P1 |
| X6 | W4: §2 anchors (patch l.1184, l.1190; owners l.1191; map l.1334, crosswalk l.1335, parity1 l.1336); the decide1 pin form cites v1.3 §9.2; §0.2 money "at most 333,066 VND" for 33 billed h | CC-301 W4; boolean checks of those LOG lines | §0.2, §2, §9 step 5 |
| X7 | W5: §1.1 records the `pin_line` names: `scripts/b_pa1/SHA256SUMS_GPU` + `H_B′` → True (bare name → False); `B_GPU_READINGS.md` + `H_B′` → True (path form → False) | CC-301 W5; re-run at drafting | §1.1 |
| X8 | W6: §12.3 step 1: every unmatched START counted; a `done.<step>` with no whole ledger end counts as open; S and SW whole seconds, open parts rounded up; why the sorted rsync order makes `job.log` cover a truncated ledger | CC-301 W6, item 10 | §12.3 step 1 |
| X9 | W7: §12.3 step 5: the parts source is keyed on the interrupted mode `IM`: `IM` = w → the load-checked loop pull; `IM` ≠ w → the `snap_w` snapshot, its `SHA256SUMS_w` check re-run first (laptop W → nothing to restore); a pulled `done.<step>` whose own output file is short of its per-file n (captions 2,000; decomp_d1 8,000; h_decomp_d1 = H rows) is not restored | CC-301 W7; job l.138, l.170; gpu l.770-810 | §12.3 step 5 |
| X10 | W8: `validate.txt` has 2 lines; the pin's `validate:` slot takes line 1; the `step4-i-none` line states no (i) entry was added, so no irreversible read was needed | CC-301 W8, item 11 | §11.2 step 3 |
| X11 | W9: the 12 h warning before T = the first 6-hourly read where (B0 − T) / Σ r_live ≤ 18 h | CC-301 W9 | §5.4 |
| X12 | W10: CC-300 W6-W8 still carried as stated | CC-301 W10 | §16 |
| X13 | header: supersedes v1.2 (6524845); HEAD 6d674ced unchanged; LOG up to l.1899 | this change | header |

## A2. v1.1 → v1.2 change table

| # | change | source | v1.2 section |
|---|---|---|---|
| V1 | code pinned to `H_B′` 6d674cedca8eb0a1d2897d102e2d052b2423b182 (CC-300 GO 90): job e02e6f4a, job selftest 0e42e1a7, gpu e5c34c79, mutants a550ab4f, new `b_pa1_d8i_validate.py` 21857fd0, SHA256SUMS_GPU 9ee60e7e, readings e8c4be00; `b_pa1_mid.py` b8afa120 and the registry 3651d1a8 unchanged; P8 pin OPS-1109b-p8-pin (l.1895) checked with `pin_line` (CC-300 W5) | CC-300; OPS-1109b-p8-pin | §1.1, §1.2, §1.3, §4 P3 |
| V2 | F-1 CLOSED (CC-300 Ruling 1): a narrow `SHA256SUMS_a1decode` (exactly the 4 caption files, in ACCEPT order, never a glob; written in teardown before the EXIT line), and `SHA256SUMS_a1decode_all` (out, logs, w25_parts; written last) | job l.44, l.50-52, l.170-174 | §1.1, §11.1, §14 |
| V3 | CC-300 W1: §11.1 and RB13 wait on `EXIT a1decode rc=0` AND `SHA256SUMS_a1decode_all`; full `sha256sum -c` of `_all`; the narrow file has 4 lines, each verbatim in `_all` (`grep -vxFf` empty), because `_all` does not hash the narrow file; §14 names `_all` where a1decode is the last done mode | CC-300 W1 | §3 RB13, §11.1, §14 |
| V4 | F-2 closed in code: the (i) validator `b_pa1_d8i_validate.py`, with its exact command and output form in the (i) path | validator l.1-145 | §11.2 step 3 |
| V5 | F-3 CLOSED (CC-300 Ruling 2): `cap-init --used-w-sec SW` (0 ≤ SW ≤ S), subtracted by `left --w`; the v1.1 'loss during w → PI decides until F-3' branch is dropped | gpu l.435, l.871-879; CC-300 W2 | §1.1, §12.3 |
| V6 | CC-300 W2/W3: §12.3 defines SW with the same D-12 open-step rule as S (SW ≤ S); `cap-init … --used-sec S --used-w-sec SW`; the finished `part_*.npz` of `w25_parts/` are **restored** from the pull (never `.part_*` temp files), so W resumes from the parts that exist; §9.2's parity re-checks block 0; PI-1108i allows the one re-rental | CC-300 W2, W3; reading 21; PI-1108i | §12.3, §17 D-12, D-18 |
| V7 | PQ-B4 answered by PI-1108h (laptop online 24/7, sleep and Windows Update off); PQ-B5 in progress (CC-300); PQ-B6 answered by PI-1108i (one HB-T1′ without a fresh PI line, after a one-judge read of a short machine-loss addendum) | LOG l.1887, l.1889 | §4 P16, §12.3, §18 |
| V8 | PI-1108h: warn the PI to top up when the balance reaches 50,000 VND | LOG l.1887 | §5.4 |
| V9 | money: balance 1,079,499 VND after the 500k top-up; Σ R_j and the L-before formula handle a parallel C-DIAG rental (M_D 210k, 20.0 billed host-h; PI-1109a); B's worst case W_B = max(0, 40 − h_B) × r_B, the C-DIAG prereg's own form (superseded by PI-1109c: §A3 X2) | LOG l.1888, l.1891; C_DIAG_PREREG_DRAFT_v1_1 l.631-644 | §3 RB9-RB11, §5, §17 D-19 |
| V10 | P2 (CC-300 Ruling 8), P3 (SUMS_GPU 9ee60e7e), P16 (PI-1108h), P24 (met at `H_B′`) updated; P25 (C-DIAG state) added | CC-300 W4, W5 | §4 |
| V11 | every `job l.` reference renumbered to the fixed job.sh | job e02e6f4a | throughout |
| V12 | F-2 reworded to the stricter code (CC-300 W4); the (i) validator step with its exact command and output form | CC-300 W4; validator l.54-94 | §1.1, §11.2 step 3 |
| V13 | CC-300 W6-W8 recorded as non-blocking carried items | CC-300 W6, W7, W8 | §16 |
| V14 | §12.3: S / SW from whole ledger lines (a torn tail from `rsync --partial` ignored; an unmatched job.log START is open from its stamp); finished modes restored from their verified snapshots; pulled `part_*.npz` load-checked (frame 863ad3e9, block index, 500 rows) before restore | `rsync --partial` in the §13 loop | §12.3 steps 1, 5 |
| V15 | §11.2: tokens_i > 0 but no entry proposed → no (i) file, no validate, no (i) pin, amend (ii) only, one OPS line (the validator's `src_i` needs ≥ 1 entry) | validator `src_i` check | §11.2 step 3 |
| V16 | header anchors: HEAD 6d674ced, LOG up to l.1895; §5 figures confirmed by count-only greps of l.1887, l.1888, l.1891 | this change | header, §5 |

## A. v1 → v1.1 item map (record; kept as in v1.1)

| # | item | source | v1.1 section |
|---|---|---|---|
| M1 | `H_B` = 6e17728; GPU code in sibling files with `SHA256SUMS_GPU`; `b_pa1.py` not edited | OPS-1108b-hb-commit, -p8-pin; CC-295 Ruling 1 | §1.1 |
| M2 | two GPU venvs (main 4.53.3, legacy 4.45.2) and the W venv; freeze rule | CC-295 Ruling 2; reading 4 | §1.1, §6, §8 |
| M3 | every FILL_ slot filled from the code or the LOG; run-day values are shell variables | coordinator brief | §1.2, §1.3 |
| M4 | job takes 5 arguments: MODE, H_B, MAN, MAPF, EXTRA (NBLK for `w`; the `h_input.jsonl` sha for `rest`) | `b_pa1_job.sh` l.3, l.24-25, l.111-124 | §9-§11 |
| M5 | frame file at `~/b_pa1_out/in/o365_train_frame.tsv`, checked by the job | job l.109 | §6 step 7 |
| M6 | SSCD path: laptop file (9f26bd4c) pushed to `~/b_pa1_models/`, checked by `setup sscd` | OPS-1108b-p6-laptop-start; setup l.104-109 | §1.3, §6 |
| M7 | setup stages main / weights (`all`), gated with the token on stdin, sscd; cap-init | setup l.4-5; gpu `cap-init` | §6 |
| M8 | RB6 / D-9 (lazy download) struck: eager download, 141.1 GB, disk precheck | CC-295 Ruling 3; reading 5; CC-295r2 N-d | §3, §6, §17 |
| M9 | disk: offer rule of PI-1108f (CC-295r2 Q1 default) and the `--output=avail` ≥ 185 GB check at host prep | PI-1108f; CC-295r2 Ruling 15 | §5.2, §6 |
| M10 | money stop = `money-stop`, then one TERM to `~/b_pa1_out/job.pid` after a cmdline check; never `tmux kill-session` | CC-295 W1; CC-295r3 Ruling 5; reading 20 | §5.4 |
| M11 | read cadence by `balance-cadence` (hourly near the threshold) | CC-295 N13; reading 20 | §5.4 |
| M12 | core-stop handling (rc 13, CORE_STOP.json), PA3, every final marker | CC-295 W3; reading 24 | §12 |
| M13 | HB-T1′ as an either/or branch with RESUME.json / RESUME_USED | reading 21; CC-295r3 N-i; CC-295r4 N-j | §12.3 |
| M14 | interlude 2: htrans, then the push of `in/h_input.jsonl`; coverage; the (i) path draft → irreversible read → pin (B) form → amend; fallback map v1 + D-8 (ii) | CC-295r3 interlude note; PI-1108d PQ-B1; PI-1108f Q2; D-8 §7 | §11.2 |
| M15 | parity2-start and mapfinal pin forms (reading 17), tested against the code | reading 17; mid l.286-310 | §11.2 |
| M16 | `decide --extra` lists all five C7 caches; the decide1 "P6 met" pin form | P6_RECOMPUTE §6.5, §7 item 2 | §9.2 |
| M17 | P9 R1 pin lines (registry 3651d1a8, model pins, prompt shas) before the rental; R2 freezes after mode selftest, before `w` | CC-295r4 pin list; reading 4 | §4, §8.3 |
| M18 | the host never gets `b_pa1_lists.json`; slice A = the MANIFEST names in frame order (v1 §9.4 push of the lists struck) | reading 1 | §9.4 |
| M19 | `selftest` mode takes MAN `-` | job l.86 | §8 |
| M20 | §9.3 (more W blocks): the whole set 0..N′−1 is re-pushed with a new manifest (the trap wiped `w`) | gpu `w_block_ok`; job l.114 | §9.3 |
| M21 | W venv: `W venv ok: freeze 1a639a50` in setup.log is checked before mode `w`; the laptop fallback runs `parity` too | setup l.59; job l.122; R5 §D.2 | §9.1 |
| M22 | pull-loop alerts add MONEY / PA3 / CORE STOP; per-mode snapshot pulls verify each manifest before the next launch | job l.49, l.163-165; C lesson (OPS-1108a-hc1-pulled) | §13, §14 |
| M23 | C's push lessons: stop a stalled stream by pid, stdout-only failing list, manifest last, new hosts lack python3.12 / tmux / rsync | OPS-1108a-hc1-push2-stall, -push-speed, -prep | §6, §7 |
| M24 | L-before with Σ R_j = 0 (C deleted, balance 579,499 at 13:31Z); PQ-B3 top-up timing | OPS-1108a-hc1-deleted l.1867; PI-1108d | §5 |
| M25 | CPU floor from PI-1107a | PI-1107a | §5.2 |
| M26 | D-1..D-10 updated to the rulings; D-9 struck; new readings D-11..D-17 | rulings | §17 |
| M27 | PQ-B1..B3 answered (PI-1108d); new PQ-B4..B6 | PI-1108d | §18 |
| M28 | NEW blocking defect F-1, pre-rental item F-2 (no (i) validator), and the HB-T1′ W-cap gap F-3 | this drafting's tests and code reading | §1.1, §12.3 |

## 0. Summary

### 0.1 Sources and PI lines

| line | effect here |
|---|---|
| PI-1104ag (l.1534) | run PA1 tier 1; D4 28 h; D5 HB-CUS (separate doc); D6 κ (not run here) |
| PI-1104ae (l.1522), PI-1107a (l.1754) | 1 × RTX 3090 / 3090 Ti 24 GB; CPU floor Ryzen 7 5800XT class |
| PI-1101q (l.1091) | a launch is not held only because the balance does not cover the whole chain |
| PI-1105c, PI-1105e (l.1550, l.1568) | the P-3 band; the trim rule decides A3 / H; PQ-2 NO (HB-CUS money not required for 28 h) |
| PI-1107b (l.1756) | full PA1, 3 tiers; the PI funds tier 3 |
| PI-1108b, PI-1108c (l.1835-1836) | start B now; B may run in parallel with C. C's HC-1 was deleted at about 13:31Z (l.1867); a parallel C-DIAG is handled by PI-1109a (below) |
| PI-1108d (l.1842) | PQ-B1 YES (HB-T1 may idle up to 6 h in the mid-run laptop step); PQ-B2 NO overlap (if not rented by 2026-11-13T01:00Z, B waits until 1/12); PQ-B3 YES (the PI tops up ≥ 200k VND before HB-T1 is deleted; PI action) |
| PI-1108e (l.1852) | Q1 Gemma-3n lineage erratum; Q2 (a) step-4 additions agent-drafted, read at the irreversible tier |
| PI-1108f (l.1863) | Q1 round 4 of the code read (done: CC-295r4 GO); Q2 if the (i) read is not GO inside the 6 h window, step 4 closes with map v1 + D-8 (ii); disk default of CC-295r2 Q1 applies |
| PI-1108h (l.1887) | the laptop is online 24/7, with sleep and Windows Update off (answers PQ-B4); warn the PI to top up when the balance reaches 50,000 VND |
| OPS-1108d-topup (l.1888) | +500,000 VND; balance 1,079,499 VND |
| PI-1108i (l.1889) | one re-rental HB-T1′ without a fresh PI line, after a one-judge read of a short machine-loss addendum (answers PQ-B6) |
| PI-1109a (l.1891) | Paper C's diagnostic block C-DIAG (≤ 210k VND / 20 h, own host) may run in parallel with B if its solvency check passes with B's worst case reserved |
| PI-1109c (l.1896) | point 2: C-DIAG's solvency check reserves **B's real worst case once**: W_B plus the HB-T1′ resume overhead, without counting B's cap twice ("~464k VND"). The binding form is W_B + O_B (CC-299r2 R2-W8, Ruling 4), 474,354 VND at planning rates (§5.1) |
| PI-1109d (l.1897) | only four kinds of question go to the PI: direction, money above the cap, a data licence or test look, and submission; everything else is decided by the agents |
| PI-1109e (l.1917) | the i5-14400F of offer 106594 meets the CPU floor (PI-1107a) |
| PI-1109f (l.1925) | on a suspected machine problem or unexplained errors, the coordinator may rent another machine |

### 0.2 What runs

| item | value |
|---|---|
| What runs | on HB-T1: mode `selftest` (hostcheck main + legacy, T8 wipe check); mode `w` (block W, CPU); mode `s` (§4.3 walk, §4.4 gate, A4 rates, smoke, rates.json, TRIM.json); `a1decode`; `a1score`; `rest` (A2, then TRIM's A3, H, A4). On the laptop: interludes 1 and 2, the pull loop, the final pull |
| Host | HB-T1 = one RTX 3090 / 3090 Ti of GPU_RENTAL_SPEC with the PI-1107a CPU floor and the PI-1108f disk rule; deleted after the final pull |
| Cap | 28 or 22 GPU-h, chosen once by P-3 at the rental line; written once by `cap-init` into CAP.json. GPU-h = the sum of step wall seconds in `ledger.jsonl` (reading 21, reading 30) |
| Data on HB-T1 | the frame file (ids and Objects365 train file names) on disk; W-set and slice-A images only in `/dev/shm/b_pa1_hb/<set>` (0700); `in/h_input.jsonl` (B's own captions × 6 transforms). Never the map, gold, an annotation file, `b_pa1_lists.json` or a test-role id list (CC-295 Ruling 12) |
| Weights | eager, 141.1 GB pinned (15 registry models; 13 with `download: true`), under `~/b_pa1_models/hf` (reading 5) |
| Time | setup about 1-2 h on a fast link [est.] (planning 4 h); cap ≤ 28 h; interludes ≤ about 1 h + ≤ 6 h; teardown 1 h. **At most about 40 billed h** |
| Money | expected about 269k VND; at most 333,066 VND without idle (33 billed h = setup 4 + cap 28 + teardown 1, at 10,092 VND/h, + fee 30); §5 |

### 0.3 Order and performers

Each laptop shell block starts with `. "$HOME/bpa1_env_3.sh"` (§1.3; it sources `bpa1_env_2.sh`, which sources `bpa1_env.sh`).

| # | step | who | gate |
|---|---|---|---|
| 0 | done under v1.4: steps 1-5 (pins l.1910-1911, rental l.1919, setup l.1920). Now: CC-304 GO; commit `H_B″`; its P8 pin; one-judge FULL read of this file; then §0.4 | judge; gatekeeper | GO 85 |
| 1 | P9 R1 and prompt pin lines (§4 P4) | gatekeeper | before the rental |
| 2 | env file (§1.3), host repo (§1.4), W farm (§7.1), `--extra` manifest (§9.2), dry `load_extra` (P7b) | coordinator | P0-P23 |
| 3 | R-B read = the GO one-judge FULL read of this file's sha, filled (any round); registration commit of exactly this file | one judge (REVERSIBLE 85); gatekeeper | GO |
| 4 | L-before, offer check, P-3, rent, rental line = T0 (§5) | coordinator; the PI only if no offer passes | all P PASS |
| 5 | host prep, facts, avail check, repo, setup, frame, cap-init (§6) | coordinator | every check PASS |
| 6 | mode `selftest`, HOSTCHECK pull, R2 pin line (§8) | coordinator; gatekeeper | HOSTCHECK OK |
| 7 | push W, mode `w`, interlude 1: parity, decide, "P6 met" pin, pick, slice-A farm (§9) | coordinator; gatekeeper | in order |
| 8 | push A, mode `s`, trim, L-S (§10) | coordinator | 4 accepted, core fits |
| 9 | push A, `a1decode`; interlude 2; push A, `a1score`; push A, `rest` (§11) | coordinator; judge for (i); gatekeeper | parity run 2 passes |
| 10 | stops, resume, HB-T1′ (§12); pull loop (§13) | coordinator; one judge on a STOP | – |
| 11 | final pull, verification, wipe, L-final, delete, L-after (§14, §15) | coordinator | JOB DONE rest or a final stop |
| 12 | hand-off (§16) | coordinator | – |

### 0.4 Re-entry at `H_B″` on the live HB-T1 (no new rental)
1. CC-304 GO; the gatekeeper commits `H_B″` (exactly the 5 F-4 paths) and writes the P8 line (§1.1 form).
2. The coordinator replaces each H_B″ placeholder in this file with the 40-hex sha (one `sed` over the file; P2 then
   counts none left). Then the one-judge FULL read of the filled file (R-B), the P0 NGRAM line and the registration
   commit of exactly this file.
3. Laptop: write `~/bpa1_env_2.sh` (§1.3). Append `REENTRY v1.5 <date -u>` to `$PRE/pre.txt`, then re-run P0-P4 and
   P24 under it, and P9 at step 4. The other P rows were met before the rental (v1.4) and stand.
4. Host repo: rebuild `$HR` at `H_B″` (§1.4), move the `H_B′` copy aside on the host, transfer, run the host checks.
5. §8: stale HOSTCHECK files aside, mode `selftest` at `H_B″`, §8.2, then the R2 line (§8.3, still to be written).
6. Continue at §9.1 as written.
- Kept, not repeated: §5 (L-before2 l.1918, the rental line l.1919: T0 2026-11-09T00:40:26Z, cap 28, RH 10,938,
  FEE 30), §6 steps 1, 2 and 4-10 (setup line l.1920, CAP.json 02193716), and `~/b_pa1_out` with CAP.json,
  `freeze_*.sha256`, `logs/setup.log` and `in/o365_train_frame.tsv`. The venvs and weights are untouched by F-4.
- The host bills idle meanwhile, inside the registered 6 h idle bound of §0.2 (PI-1108d PQ-B1).

### 0.4b Re-entry for block W (v1.6; same HB-T1, same `H_B″`, no new rental)
Event (l.1939, OPS-1109b-hbt1-w-stop1). At `H_B″` the selftest passed (HOSTCHECK OK; R2 line l.1934) and push w passed
(l.1936). Mode w (launch l.1937) stopped 1 s after `START w.feats9` with `ModuleNotFoundError: decode_icl`: the §1.4
sparse set lacked the W import chain (`b_pa1_w25` → `w25` → `c_stage1/build_memory` → `decode_icl` →
`lb/decode_hf_vlm` → …). The trap wiped the W set (4,501 files). The ledger holds `w.feats9` = 1 s. The GPU entry
points import only `scripts/b_pa1/` and venv packages, which the passed selftest covers.
1. Laptop: write `~/bpa1_env_3.sh` (§1.3). Append `REENTRY v1.6 <date -u>` to `$PRE/pre.txt`; re-run P0-P2 under it.
2. Rebuild `$HR` (`_3`) with the §1.4 block (five paths added); P9 ("HR OK"); then **P26** (block below).
3. Host: `ssh -o BatchMode=yes hbt1 'mv -n ~/b_pa1_repo ~/b_pa1_repo_hbpp && [ ! -e ~/b_pa1_repo ]'`, then the §1.4
   transfer and the host checks (HEAD = `H_B″`, unchanged).
4. **No new selftest.** The code is unchanged, so the job's `CODE` (the sha of `scripts/b_pa1/SHA256SUMS_GPU`, job l.80)
   is still 8c39fae7…, and the HOSTCHECK files bind only code, freeze and GPU uuid (job l.99-103), not the repo path.
   The repo move invalidates none of them, and the R2 line (l.1934) stands. The five added files are bound by the
   job's `git diff --quiet HEAD --` at `H_B″` (job l.67-70).
5. **The stopped run's marker** (§12.1 ruling). The job made `RUN.w9.started` before the step (job l.135). A restart
   with the same `MODE=w EXTRA=9` would refuse without RESUME.json, or would use the one resume (job l.129-133). This
   stop is not a resume cause, so the marker is moved aside, after these checks on the host (counts and names only):
   `RESUME.json` and `RESUME_USED` absent; no `logs/done.w.*`; `w25_parts/` holds 0 `part_*` files; the last two
   `ledger.jsonl` rows are the `w.feats9` start and its end with rc 1. Then
   `mkdir -p -m 700 ~/b_pa1_stale_hbp && mv -n ~/b_pa1_out/RUN.w9.started ~/b_pa1_stale_hbp/RUN.w9.started.stop1`.
   The ledger stays, so the 1 s counts for the cap and for `left --w` (W budget 3,599 s left).
6. Push w again (§7.2, `SET=w`, the same WMAN 29da438e), then launch mode w (§9.1 step 3, `MODE=w EXTRA=$NBLK`).
- One OPS line `OPS-<MMDD>b-hbt1-w-reentry` records steps 1-5: env_3 sha, HR OK, the P26 result, the host checks, the
  marker checks and its move.
- The pull loop started at l.1938 (from v1.5) keeps running: `$PRE` and `$PULL` are the same under env_3.

**P26 block** (laptop, a CPU dry run of the W import chain from the exact sparse tree; `$X` holds the W images):
```sh
. "$HOME/bpa1_env_3.sh"; Q=$PRE/p26_parts; [ ! -e "$Q" ] || { echo "GUARD: $Q"; exit 1; }
mkdir -m 700 "$Q" && cd "$HR" || exit 1
"$WV" -I -B scripts/b_pa1/b_pa1_w25.py feats --frame "$FRAME" --images "$X" --sscd "$SSCD_L" --parts "$Q" --blocks 1 \
  > "$PRE/p26.log" 2>&1 || { echo "P26 FAIL rc=$?"; exit 1; }
cd "$R" && "$WV" -I -B -c '
import sys
from pathlib import Path
sys.path[:0] = [sys.argv[1] + "/scripts/b_pa1", sys.argv[1] + "/scripts/w25"]
import b_pa1_w25 as W
p = Path(sys.argv[2]) / "part_0000.npz"
f = W.w25.load(p)
print("P26", p.name, "n", len(f["ids"]), "OK" if len(f["ids"]) == 500 and W.part_meta(p).get("frame_sha256") == sys.argv[3] else "FAIL")' "$HR" "$Q" "$FRAME_SHA" >> "$PRE/pre.txt"
tail -n 1 "$PRE/pre.txt"
```

### 0.5 Live-run record under v1.4 (LOG by line number only)
| event | LOG | ruling |
|---|---|---|
| NGRAM, R1 and prompts pins for v1.4 | l.1909-1911 | – |
| L-before and rental of machine 1 (ckey 106263) | l.1912-1913 | – |
| setup stop: the same file gave 4 different sha256 values (silent read corruption) | l.1914 | CC-302 GO 90: FAULT machine (§5.2) |
| machine 1 wiped and deleted; spend 4,694 VND; permanently excluded | l.1916 | CC-302 W1, W2 |
| PI-1109e: i5-14400F meets the CPU floor | l.1917 | PI line |
| L-before2 and rental of HB-T1 = ckey 106594, T0 2026-11-09T00:40:26Z, cap 28, RH 10,938, FEE 30 | l.1918-1919 | – |
| setup done; CAP.json 02193716 | l.1920 | – |
| selftest stop 1: no C compiler (Gemma auto-compile) | l.1921 | CC-303 GO 87: host prep |
| host prep: build-essential, python3.12-dev, probe | l.1923 | CC-303 W1-W3 |
| selftest stop 2: UnicodeEncodeError 'ascii' at models.py l.441 | l.1924 | F-4, CC-304 |
| PI-1109f: the coordinator may rent another machine on a suspected machine problem | l.1925 | PI line |
- CC-302 NB1 (a read-stability check at §6 step 2) and CC-303 W6 (the Gemma auto-compile disclosure) are carried, not
  added here.

## 1. Code, environment and the same-sha rule

### 1.1 Which sha runs

`H_B″` = **`860a3b741ecb82d8fbe31d997212965bc146404a`**: the gatekeeper commit of the F-4 code after CC-304 GO (on top of 55ff846; exactly the 5 paths of
`git diff 6d674ced -- scripts/b_pa1`). It sits on `H_B′` = 6d674cedca8eb0a1d2897d102e2d052b2423b182 (F-1 / F-2 / F-3,
CC-300 GO 90). The host checks out `H_B″`. The job refuses unless `git rev-parse HEAD` = `H_B″`,
`git diff --quiet HEAD --`, both SUMS of `scripts/b_pa1` check, and `host_w25.sums` checks (job l.67-70). The earlier
commit `6e17728` (CC-295r4) is the base of the fix; the erratum pin keeps naming it, because that is the commit at
which the erratum was frozen (CC-300 W5).

| file | sha at `H_B″` (`SHA256SUMS_GPU` -c 12/12 OK) | changed vs `H_B′` 6d674ced |
|---|---|---|
| scripts/b_pa1/b_pa1_gpu.py | e5c34c793d88f607b2d223ac61ea0829085e53298e892b0189412d1f10945071 | no |
| scripts/b_pa1/b_pa1_models.py | 88da91829afb5fc609b51e76b542e9fb9876c20db848370860575dedc4dd9429 | no |
| scripts/b_pa1/b_pa1_mid.py | b8afa120670a10e2eb2f9d95e981680005e8c028ecbb8b1bc32e2ea75e9de4c0 | no (the D-8 (B) pin quotes it) |
| scripts/b_pa1/b_pa1_gpu_mutants.py | 8b9b4c0660693b4c5967c2fa28b60c547227162c11090795f19fe44e058135cb | yes (F-4 mutant) |
| scripts/b_pa1/b_pa1_job.sh | 8ff70aaa40246836a34e815621d4ca910f7d2370e0acfa54b43ebf1ee47f2888 | yes (F-4: `-X utf8` on PYM / PYL / PYW, job l.31; one line, so every job line number is unchanged) |
| scripts/b_pa1/b_pa1_job_selftest.sh | 56dba90252a7d81b239f22ed906e111d43b592f5730a63c4e3ce3dce70bf4ed4 | yes (F-4 check) |
| scripts/b_pa1/b_pa1_d8i_validate.py | 21857fd0ee058bfb2d08ec39269212c199f3fda022d04ec9cab96b91d1f472e6 | no |
| scripts/b_pa1/b_pa1_setup_host.sh | 740c07e3bee6479e37b319c4e6ba3329ec9bd46b495d4d33b4257be8daaa847a | no |
| scripts/b_pa1/b_pa1_registry.json | 3651d1a815cd12349fb610666f8d13a8223599017a4f58a3653f581b55a3265f | no |
| scripts/b_pa1/requirements_b_pa1_main.lock (venv `b_pa1_main_3812fd04`) | 3812fd042500b72ba7bff28285c019676cdcc843b2e92a0a7a489a92d010829d | no |
| scripts/b_pa1/requirements_b_pa1_legacy.lock (venv `b_pa1_legacy_4b2e87fe`) | 4b2e87fefb86b94906ffa229f717090cb9a976880c44c6ff99d74d6cd1ec5f9f | no |
| scripts/b_pa1/requirements_b_pa1_w.txt (venv `b_pa1_w`) | 1a639a50adf550c50c6dfe284146e279b2a2bf2a716ade743e9eb357ccbf0778 | no |
| scripts/b_pa1/SHA256SUMS_GPU (12 lines) | 8c39fae7c1296b751e7d2042711b5ea881297c14393e0e95a8e690204e0b5509 | yes |
| scripts/b_pa1/SHA256SUMS (b_pa1.py c481fcf4, b_pa1_w25.py 54ea786d, …) | d879cb430cec2b0e9a58b2e3dc0a164cf24aee1ad8b6fbf30c3199881f6969a0 | no |
| scripts/b_pa1/B_GPU_READINGS.md (document, not in SUMS) | 98642130e872b6e9e23dc26dc9729c4442b46b531038daeb5afc52d3451d479d | yes (F-4 entry) |

**P8 pin line at `H_B″`: to be written** (gatekeeper, after the commit, before the full read), in the names that
`pin_line` matches (CC-301 W5):
```
<date -u +%FT%TZ> OPS-<MMDD>b-p8f4-pin: PIN scripts/b_pa1/SHA256SUMS_GPU 8c39fae7c1296b751e7d2042711b5ea881297c14393e0e95a8e690204e0b5509 H_B 860a3b741ecb82d8fbe31d997212965bc146404a B_GPU_READINGS.md 98642130e872b6e9e23dc26dc9729c4442b46b531038daeb5afc52d3451d479d (P8 at H_B″, F-4 -X utf8, CC-304 GO <score>; job 8ff70aaa job_selftest 56dba902 mutants 8b9b4c06; unchanged gpu e5c34c79 models 88da9182 mid b8afa120 validator 21857fd0 registry 3651d1a8 setup 740c07e3 SHA256SUMS d879cb43)
```
Tested at drafting on a scratch LOG copy with a stand-in 40-hex for `860a3b741ecb82d8fbe31d997212965bc146404a`: `pin_line(sha 8c39fae7…,
"scripts/b_pa1/SHA256SUMS_GPU", H_B″)` → True and `pin_line(sha 98642130…, "B_GPU_READINGS.md", H_B″)` → True. The
`H_B′` P8 line (OPS-1109b-p8-pin, l.1895) and the H_B one (OPS-1108b-p8-pin) stay in the LOG as they are.

**F-4 (closed in code; CC-304).** Selftest stop 2 (l.1924) was `UnicodeEncodeError: 'ascii'` at `b_pa1_models.py`
l.441 (`write_text` of the HOSTCHECK json with `ensure_ascii=False` under an ASCII locale). `-I` ignores PYTHONUTF8,
so the fix puts `-X utf8` on the three job interpreters (job l.31): every job read and write is UTF-8 on any locale.

- **Same-sha rule.** No byte of `scripts/b_pa1/` or of the §1.4 path set changes from mode `selftest` to the final
  pull. A change is a new commit, a new read and a fresh mode `selftest`. HOSTCHECK is bound to code, freeze and GPU
  uuid (reading 29).
- **Freezes (reading 4).** Setup writes `~/b_pa1_out/freeze_<venv>.sha256` once at the first build. Every job start
  compares against it (job l.74-79). The laptop compares the pulled values with the R2 pin line (§8.3). The W venv is
  checked against the constant 1a639a50 (job l.122).

**F-1 (closed in code; CC-300).** v1.1 found that the job's done-mode manifest listed every file under out, logs and
w25_parts, while `b_pa1_mid.pulled_captions` (l.72-93; `coverage --pulled` and `htrans`) needs exactly the 4
`out/a1decode/captions_<k>.jsonl` files.
- The fixed job writes, for a done a1decode:
  - in teardown, **before** the EXIT line: a narrow `SHA256SUMS_a1decode` over exactly the 4 files. The names come from
    the `a1decode.decode.<k>` steps, never a glob, so a `.torn.<UTC>` file left by `resume` stays out (job l.50,
    l.171-174);
  - **last**, after the EXIT line: `SHA256SUMS_a1decode_all` over out, logs and w25_parts (job l.52, l.172).
- So the narrow file can exist before `_all`. Every wait and snapshot uses `_all` (§11.1, RB13). Other done modes keep
  one full manifest `SHA256SUMS_<mode>`.

**F-2 (delivered; CC-300 Ruling 3; wording per CC-300 W4).** The (i) validator `scripts/b_pa1/b_pa1_d8i_validate.py`
(21857fd0, bound by SHA256SUMS_GPU, so by P8 and the job's same-sha check):
- lines (A) and (B) must already stand on the **real** LOG (it only reads the real LOG);
- only the (i) pin form (md §7, filled in its slot order: full sha; `<8-hex>` md, coverage, mid) is appended to a
  **scratch copy** of the LOG;
- then `cmd_amend` (ii), `cmd_amend` (i) and `cmd_final` of the committed mid b8afa120 run on one scratch amendments
  log;
- it prints one counts-only line (8-hex shas and counts, never a term, token or class name) ending `RESULT PASS`
  (rc 0) or `RESULT FAIL <checks>` (rc 1, the refusal form);
- it is stricter than v1.1 asked: the (i) file must be named `b_pa1_d8_i_entries_v1.json`, its provenance must name
  md c041c4ab, every entry must be src i, and the coverage must come from `--pulled` (not classes-only).

**F-3 (closed in code; CC-300).** `cap-init --used-w-sec SW` (refused unless 0 ≤ SW ≤ S) writes `used_w_before_sec`.
`left --w` = min(left, 3600 − SW − the W seconds in this ledger) (gpu l.435, l.871-879). HB-T1′ therefore never gets a
second full 1.0 GPU-h for block W (§12.3).

### 1.2 Filled values (each from the code at `H_B″` or a LOG line)

| v1 token | v1.2 value | source |
|---|---|---|
| FILL_H_B | `860a3b741ecb82d8fbe31d997212965bc146404a` (`H_B″`, CC-304 GO; on `H_B′` 6d674cedca8eb0a1d2897d102e2d052b2423b182) | the P8 line at `H_B″` (§1.1) |
| FILL_SUMS_B | SHA256SUMS d879cb43… (unchanged) + SHA256SUMS_GPU 8c39fae7… (12 files) | the P8 line at `H_B″` (§1.1) |
| FILL_CODE_READ | CC-304 GO (F-4) on CC-300 GO 90 (the F-1/F-2/F-3 fix, reversible 85) and the base read CC-295r4 (A) GO 89; erratum CC-295r4 (B) GO 90 | CC-300.txt; CC-295r4.txt |
| FILL_LOCK, FILL_SETUP_SH | locks 3812fd04 / 4b2e87fe, W reqs 1a639a50; setup 740c07e3 | §1.1 |
| FILL_REGISTRY | 3651d1a8 (P9 R1 line still to write, §4 P4) | registry at H_B |
| FILL_FREEZE_GPU | run-day: `freeze_main.sha256`, `freeze_legacy.sha256` from the first build → R2 line (§8.3) | reading 4 |
| FILL_P6 | OPS-1108b-p6a-pin (c7_xm3600_all 90b39859…), OPS-1108b-p6b-pin (c7_ktvic_refused_dup 24b8603f…) | LOG l.1855-1856 |
| FILL_C7_MANIFEST | `$PRE/c7_extra.json`, built by §9.2's block, five caches | P6_RECOMPUTE §7 item 2 |
| FILL_SSCD_LAPTOP_PATH | `/home/hoanguyen/backups/vsps_image_captioning/.session_backup/2026-10-22/c_stage1/sscd_disc_mixup.torchscript.pt` (9f26bd4c) | OPS-1108b-p6-laptop-start |
| FILL_WMAN | run-day: `bpa1_env_w.sh` (§7.1) | §7.1 |
| FILL_STEP4 | `b_pa1_mid.py coverage` / `amend` / `final` (§11.2) | mid l.1-14 |
| FILL_PARITY2 | `b_pa1_mid.py parity2 --map <final dir>/b_pa1_map_final.json` | mid l.286 |
| FILL_SPARSE | §1.4: `scripts/b_pa1/`, the four w25 SUMS files, and the W import chain `scripts/c_stage1/decode_icl.py`, `scripts/g2b/decode_qwen3vl.py`, `scripts/lb/decode_hf_vlm.py`, `scripts/match_openviic.py`, `scripts/evaluate.py` (W stop 1, l.1939; P26) | §1.4; P26 |
| FILL_RHOST, FILL_F | run-day: `RH` (panel rate rounded up to a whole VND, D-16), `FEE` | rental line |
| FILL_GATED_STAGE | `bash scripts/b_pa1/b_pa1_setup_host.sh gated` with the token on stdin | setup l.5 |
| FILL_CAP_INIT | `b_pa1_gpu.py cap-init --cap-h 28\|22 --r-host RH --fee FEE --t0 T0` | gpu l.871 |

### 1.3 Notation (env files; each written once)
- `~/bpa1_env.sh` was written once by the registered v1.4 §1.3 block (sha 51aad3fd, chmod 400). It names v1.4 as `DOC`
  and `H_B′` as `H_B`, and it holds the live run's `D0` and dirs. It stays unchanged.
- `~/bpa1_env_2.sh` was written once by the registered v1.5 §1.3 block (sha 3aef29d7, chmod 400). It names v1.5 as
  `DOC`, `H_B″` as `H_B` and `$HOME/bpa1hr_<D0>_2` as `HR`, which exists. It stays unchanged.
- v1.6 adds the **retry env `~/bpa1_env_3.sh`** (the same rule). It sources `bpa1_env_2.sh`, then overrides only `DOC`
  (this file) and `HR` (a new `_3` dir). `H_B` stays `H_B″`. Every laptop block of this file sources `bpa1_env_3.sh`.
- `bpa1_env_w.sh` (WMAN 29da438e, §7.1) and, later, `bpa1_env_a.sh` (AMAN, §9.4) are sourced if present, as before.
```sh
[ ! -e "$HOME/bpa1_env_3.sh" ] || { echo "GUARD: bpa1_env_3.sh exists"; exit 1; }
[ "$(sha256sum < "$HOME/bpa1_env_2.sh" | cut -c1-8)" = 3aef29d7 ] || { echo "STOP: bpa1_env_2.sh is not 3aef29d7"; exit 1; }
cat > "$HOME/bpa1_env_3.sh" <<'EOF'
. "$HOME/bpa1_env_2.sh"
DOC=manuscript/prereg/2026-11-01_b_pa1_tier1/B_RUN_DOC_v1_6.md
HR=$HOME/bpa1hr_${D0}_3
EOF
chmod 400 "$HOME/bpa1_env_3.sh"; sha256sum "$HOME/bpa1_env_3.sh"
. "$HOME/bpa1_env_3.sh" && [ "$H_B" = 860a3b741ecb82d8fbe31d997212965bc146404a ] && [ -f "$R/$DOC" ] && [ ! -e "$HR" ] && echo "ENV3 OK $H_B" | tee -a "$PRE/pre.txt"
```
- Kept from `bpa1_env.sh`: `$PRE` (the live checklist `pre.txt`, `hbt1_facts.txt`, `cap_init.txt`, `c7_extra.json`),
  `$X` and the W farm `$PUSHW` with `bpa1_env_w.sh` (no W push has run; the W set does not depend on the code sha),
  `$PUSHA`, `$PULL` and `$S4`.
- New: `$HR` = `$HOME/bpa1hr_<D0>_3` (0700), because the host repo is rebuilt with the five added paths and §1.4
  refuses an existing `$HR`. The `_2` `$HR` and the first `$HR` stay on the laptop as records.
- `$S4` holds every step-4 file: coverage, the (i) entries, the amendments log, the final map. It lies under
  `.session_backup/`, which `outside_tree` allows and git excludes (`.git/info/exclude` l.9).
- `HPY` is the literal text `~/venvs/b_pa1_main_3812fd04/bin/python`. It is placed unquoted inside an ssh command
  string, so the host's shell expands the tilde (main-lock prefix 3812fd04, job l.30-31).
- On the host, run from `~/b_pa1_repo`:
  - `~/b_pa1_out` holds `in/`, `out/`, `logs/`, `w25_parts/`, CAP.json, `ledger.jsonl`, `freeze_*.sha256`,
    `HOSTCHECK_*.json`, `RUN.*`, `job.pid` and the manifests;
  - `~/b_pa1_models` holds HF_HOME `hf/` and the SSCD file;
  - `~/venvs/` holds the three venvs;
  - images live in `/dev/shm/b_pa1_hb/<set>`.
- `NBLK = 9` [proposal]: 4,500 frame images in one W push (v3.1 l.252-254 needs 4,000 survivors).

### 1.4 The repository on HB-T1: sparse, code only (D-10, decided)
`host_w25.sums` sits at the repo root and is required by the job (l.70; reading 32). It holds only the committed
w25 SUMS lines of the four files the host runs. The id files that `scripts/w25/SHA256SUMS` also lists (`kv5000.txt`,
`ut2402.txt`, `exclusion.json`, …) never reach the host (CC-295 Ruling 12).
```sh
. "$HOME/bpa1_env_3.sh"
[ ! -e "$HR" ] || { echo "GUARD: $HR exists"; exit 1; }
git clone -q --no-local --filter=blob:none --no-checkout -u 'git -c uploadpack.allowFilter=true upload-pack' "file://$R" "$HR"
git -C "$HR" sparse-checkout set --no-cone 'scripts/b_pa1/' 'scripts/w25/w25.py' 'scripts/w25/SHA256SUMS' 'scripts/grl/common.py' \
  'scripts/grl/id_counts.py' 'scripts/c_en/cen_fetch.py' 'scripts/c_stage1/build_memory.py' \
  'scripts/c_stage1/decode_icl.py' 'scripts/g2b/decode_qwen3vl.py' 'scripts/lb/decode_hf_vlm.py' 'scripts/match_openviic.py' \
  'scripts/evaluate.py'
git -C "$HR" checkout -q "$H_B"
git -C "$HR" config remote.origin.url /nonexistent
grep -E '  scripts/(w25/w25\.py|grl/common\.py|c_en/cen_fetch\.py|c_stage1/build_memory\.py)$' "$HR/scripts/w25/SHA256SUMS" > "$HR/host_w25.sums"
[ "$(git -C "$HR" rev-parse HEAD)" = "$H_B" ] && git -C "$HR" diff --quiet HEAD -- \
  && (cd "$HR/scripts/b_pa1" && sha256sum --quiet -c SHA256SUMS && sha256sum --quiet -c SHA256SUMS_GPU) \
  && (cd "$HR" && sha256sum --quiet -c host_w25.sums) && [ "$(wc -l < "$HR/host_w25.sums")" = 4 ] \
  && [ ! -e "$HR/data" ] && [ ! -e "$HR/manuscript" ] \
  && echo "HR OK $(git -C "$HR" cat-file --batch-all-objects --batch-check | awk '$2=="blob"' | wc -l) blobs" >> "$PRE/pre.txt"
```
- Re-entry (§0.4b step 3): first `ssh -o BatchMode=yes hbt1 'mv -n ~/b_pa1_repo ~/b_pa1_repo_hbpp && [ ! -e ~/b_pa1_repo ]'`.
  The v1.5 copy (code only) is kept aside and never run, like `~/b_pa1_repo_hbp`; both go with the host's delete.
- The five W import-chain paths (W stop 1, l.1939) are code only; `decode_hf_vlm` finds the repo root by
  `scripts/evaluate.py`. P26 runs this exact tree on the laptop before the transfer.
- Transfer: `tar -C "$HR" -cf - . | ssh -o BatchMode=yes hbt1 'mkdir -m 700 b_pa1_repo && tar --no-same-owner -C b_pa1_repo -xf -'`.
  Then the same checks run on the host, and its `git rev-parse HEAD` must equal `$H_B` (`H_B″`). `--no-same-owner` avoids git's "dubious ownership" refusal (S11 §1.4).
- `git status` is never run on the host: it would try to fetch a missing blob.
- `scripts/b_pa1/` also brings `b_pa1_mid.py`, `map_v1.py` and the readings file. They are laptop tools and documents,
  and none holds data.

## 2. Data pins

| item | value | record |
|---|---|---|
| frame | `o365_train_frame.tsv` 863ad3e9… (69,519 lines `id TAB images/v1/patchN/<file>`; slice order) | l.1226 |
| patch archives | `patch0.tar.gz` 3,850,237,397 B, `patch1.tar.gz` 3,835,218,513 B (members `patchN/<file>`) | l.1184, l.1190; members l.1228 |
| owners, overlay | ae4b6630, 6c5e7282 | l.1191 (both), l.1196; b_pa1_w25.py |
| C7 caches (decide --extra) | c7a `c7_coco_gap_val2014.npz` 72b1de15…, c7b `c7_pascal50s_a.npz` 00ef3975…, c7c `c7_a_t3_val2017.npz` 95144514…, `c7_xm3600_all.npz` 90b39859…, `c7_ktvic_refused_dup.npz` 24b8603f… | l.1317-1319, l.1855-1856 |
| map v1 frozen | map 497b430a…, crosswalk 869ab3e8…, categories 2c7bf111…, R7 shas; parity1 done (Δmicro −0.001) | map l.1334, crosswalk l.1335, parity1 l.1336 |
| D-8 | md c041c4ab… (b242e0c); (ii) entries 6ad473f3… (347 entries, 233 classes; git-excluded) | l.1881-1882 |
| erratum | ERRATUM_LINEAGE_GEMMA3N_v1_2.md 11c36760… (Gemma-3n V = MobileNet-V5 fixed at this line) | l.1879 |
| registry | 3651d1a8… (15 models, 10 prompts; §4 P4 lines) | §1.1 |
| SSCD | 9f26bd4c… (`w25.SSCD_SHA`) | R5 §D.2 |
| parity-2 inputs | refs 54abc0fb…, gold 278d15b9…, exclusion.json c52a96d1… (the parity1-start tokens, l.1335; re-hashed before the start line) | l.1335 |

## 3. Registered [proposal] items

| # | item | value | source |
|---|---|---|---|
| RB1 | tmpfs layout | `/dev/shm/b_pa1_hb/` 0700; set dirs `w`, `a` (and `st` in selftest). Each mode's trap wipes its set dir and appends to `~/b_pa1_out/b_pa1_hb_deletions.log` | job l.21-22, l.48 |
| RB2 | W staging | the first `NBLK` × 500 frame images for features only; the W trap wipes them; slice-B images are never decoded, scored or staged after W; the host never gets the lists file | reading 1; D-6 |
| RB3 | cap ledger | CAP.json written once by `cap-init` from the rental line; `left` = cap − used before − ended steps − in-step elapsed | reading 21; CC-295 Ruling 9 |
| RB4 | job modes and arguments | `selftest H_B -`; `w H_B WMAN - NBLK`; `s H_B AMAN - -`; `a1decode H_B AMAN - -`; `a1score H_B AMAN MAPF -`; `rest H_B AMAN MAPF HIN` (HIN = the `h_input.jsonl` sha, or `-` if TRIM drops H) | job l.3-9, l.113-126 |
| RB5 | trim | `s.trim` decides once from measured rates; a CORE STOP if the core does not fit | readings 23-24 |
| RB6 | ~~lazy weights~~ | **struck**: eager download of every Rule-S-passing pin (141.1 GB) | CC-295 Ruling 3; reading 5 |
| RB7 | HF token | stdin into the download process only (`setup gated`), never argv, file or log | setup l.13-14, l.97-101 |
| RB8 | streams | 6 parallel streams; each ssh pid in a pid file. A stream is stalled if its share of the tmpfs grows < 50 KB/s for ≥ 10 min (two `du -sb` reads) while a fresh 20 MB probe runs ≥ 10× faster. It is stopped by pid, and no remote `tar -x` may be left. Top-up from a **stdout-only** failing list | rented-GPU skill; OPS-1108a-hc1-push2-stall, -push-speed |
| RB9 | money-stop threshold | T = (T_down + 0.5 h) × Σ r_live: 1.5 h × r_B ≈ 15,138 VND with B alone; with C-DIAG (or any other rental) live, its rate is added, e.g. 1.5 h × (10,092 + r_CD). Separate from it, the PI-1108h top-up warning fires at 50,000 VND (§5.4) | R6 §I.3 rule 4; PI-1108h; D-4 |
| RB10 | ledger cross-check | L-before − L-after (R6 §I.3 rule 1, valid while B alone bills); with C-DIAG or another rental live, minus that rental's per-instance delta over the same panel reads | D-3 |
| RB11 | Σ R_j | the remaining capped spend of every other **live** rental at the panel read. For C-DIAG: R_CD = 210,000 − S_CD, with S_CD = its per-instance spent at the same page load (its block ≤ 210k VND, ≤ 20 h; PI-1109a; C-DIAG v1.2 afbb61fb l.708-712), or the cap form of its own registered run doc if that differs. A rental not yet made is not counted by B: under PI-1109a the second renter reserves the first one's worst case | PI-1108c; PI-1109a; D-2 |
| RB12 | read cadence | after each panel read: `b_pa1_gpu.py balance-cadence --balance B --threshold T --burn Σr` gives the hours to the next read (6, then 1 within 6 h × Σ r of T, 0 = money stop now) | reading 20; CC-295 N13 |
| RB13 | per-mode manifest check | after each JOB DONE, once the mode's last manifest exists (`SHA256SUMS_<mode>`; for a1decode `SHA256SUMS_a1decode_all`, written after the narrow file), a snapshot pull and a full `sha256sum -c` of that manifest before the next launch; for a1decode also the narrow `SHA256SUMS_a1decode`: 4 lines, each verbatim in `_all` (`grep -vxFf` empty; CC-300 W1). Earlier manifests' `logs/` lines fail later by design, because logs are append-only across modes | job l.50-52, l.170-174; D-13 |
| RB14 | (i) cut-off | the (i) read must be GO by (a1decode `JOB DONE` host stamp) + 5 h; otherwise step 4 closes with map v1 + D-8 (ii) (PI-1108f Q2) | D-11 |
| RB15 | PA3 at parity run 2 | the coordinator writes `~/b_pa1_out/PA3.json` on the host (so every later mode refuses: job l.66), then the final pull and the delete | D-15 |
| RB16 | r_host for cap-init | the panel rate rounded up to a whole VND (C's `r_host_up`); cap-init accepts 1,000-100,000 | D-16 |

## 4. Preconditions (coordinator, laptop; each a STOP; output to `$PRE/pre.txt`)

All PASS before the rental, except P18 and P20 (after the rental, before the first push).

| # | check | PASS |
|---|---|---|
| P0 | LOG holds an NGRAM PASS line for this file at its read sha | present |
| P1 | R-B GO (= the GO one-judge FULL read of this file's sha, filled, any round); registration commit of exactly this file; `git ls-files --error-unmatch $DOC`; `sha256sum $DOC` = the read sha | equal |
| P2 | CC-304 GO, the commit `H_B″` `860a3b741ecb82d8fbe31d997212965bc146404a` and its P8 pin (`OPS-<MMDD>b-p8f4-pin`, §1.1) exist; `grep -c '<H_B″''>' "$R/$DOC"` = 0 (the split quote keeps this check out of the fill); this file GO at a one-judge FULL read. Until then this file is a record, not a run doc | present |
| P3 | code at `H_B″`: `git cat-file -e "$H_B^{commit}"`; `git diff --quiet "$H_B" HEAD -- scripts/b_pa1 scripts/w25 scripts/grl scripts/c_en scripts/c_stage1`; `(cd scripts/b_pa1 && sha256sum --quiet -c SHA256SUMS && sha256sum --quiet -c SHA256SUMS_GPU)`; SUMS_GPU sha = 8c39fae7c1296b751e7d2042711b5ea881297c14393e0e95a8e690204e0b5509; SUMS = d879cb43… | all OK |
| P4 | **P9 R1 and prompt lines exist**: written at `H_B′` (OPS-1109b-r1-pin l.1910, OPS-1109b-prompts-pin l.1911). They stand at `H_B″`: the registry 3651d1a8 is unchanged | present |
| P5 | P6 lines: OPS-1108b-p6a-pin, -p6b-pin (l.1855-1856) | present |
| P6 | R6-I / III / II ADOPTED (l.1572, 1573, 1585); erratum pin (l.1879); D-8 pins (l.1881, 1882); the registered files re-hash (e9b30ca7, 9cb21917, 0b55d5f8, 0c5f919b, 11c36760, c041c4ab; entries 6ad473f3) | equal |
| P7 | frame = FRAME_SHA; owners ae4b6630 and overlay 6c5e7282 re-hash | equal |
| P7b | the `--extra` manifest (§9.2) re-hashed; a dry `load_extra` of all five caches with `EXPECT` passes on the laptop (this catches an owner-order or count mismatch before the host bills) | 5 OK |
| P8 | `mkdir -m 700 "$PRE"` (absent before) | – |
| P9 | `$HR` built and checked (§1.4) | "HR OK …" |
| P10 | W farm (§7.1): WMAN line with n = `NBLK` × 500; extracted count equal; no non-regular file | equal |
| P11 | tmpfs need: W-set bytes × 1.25 and slice-A bytes × 1.25 each well below the host's `/dev/shm` avail (checked at §6) | stated |
| P12 | the pull loop extracted from §13 (`awk '/^#!\/bin\/bash$/,/^done$/' $DOC`, the only such block); sha recorded; `grep -c '/dev/shm'` = 0 | 0 |
| P13 | `grep -c hbt1 ~/.config/vsps/gpu_backup.sh` = 0 (the old loop pulls the model cache) | 0 |
| P14 | d_watch live: `ps -eo args \| grep -c '[d]_watch.sh'` (bracketed listing; no `pgrep -f`) | ≥ 1 |
| P15 | usage guard `~/.config/vsps/usage_check.sh`: fields above the stop level | recorded |
| P16 | PI-1108h (answers PQ-B4): the laptop is online 24/7, sleep and Windows Update off; the coordinator checks mains power and the network at T0 | stated |
| P17 | no other heavy /mnt/d reader or writer during §7.1 and the pushes | stated |
| P18 | ssh key login for `hbt1` in BatchMode; no password in any argv | rc 0 (after T0) |
| P19 | no self-matching process pattern **in the commands** (CC-301 W1): `awk '/^```sh$/,/^```$/' "$DOC" \| grep -c -e 'pgrep -f' -e pkill -e kill-session` = 0, and `grep -c -e 'pgrep -f' -e pkill -e kill-session "$PRE/bpa1_pull.sh"` (the P12 loop) = 0. Prose is not checked; processes are stopped only by pid files | 0 and 0 |
| P20 | clock skew \|host − laptop\| < 60 s | after T0 |
| P21 | HF token readable, mode 600 (never printed) | 600 |
| P22 | laptop step-4 tools: `/usr/bin/python3` 3.12.3; `/usr/bin/java`; R7 dir `.session_backup/machines/n2/ncs-data/vncorenlp/`; `$MP -I -B scripts/b_pa1/b_pa1_mid.py selftest` rc 0 | rc 0 |
| P23 | rental time ≤ 2026-11-13T01:00Z (PI-1108d PQ-B2: no overlap with A's 15-30/11 turn; else B waits until 1/12) | true |
| P24 | met at `H_B″` (CC-300 Ruling 3; the validator is unchanged by F-4): `b_pa1_d8i_validate.py` 21857fd0 is in SHA256SUMS_GPU 8c39fae7; `$MP -I -B scripts/b_pa1/b_pa1_d8i_validate.py selftest` rc 0 on the laptop on the day | rc 0 |
| P25 | C-DIAG state at the L-before read: not rented, or live (named by its LOG line, with S_CD and r_CD from the same page load). If C-DIAG rents after B, its own check reserves B's real worst case W_B + O_B (PI-1109c; CC-299r2 R2-W8; §5.1), read from B's latest `hbt1-lbefore` / `hbt1-rent` / `hbt1-balance` line | stated |
| P26 | (§0.4b) the W import chain from the exact `$HR` tree: the P26 block's `feats --blocks 1` into `$PRE/p26_parts` writes `part_0000.npz` with 500 ids and the frame sha; the line `P26 part_0000.npz n 500 OK` is in `$PRE/pre.txt` | OK |

**P4 line forms, as written at `H_B′`** (l.1910-1911; record; they are not written again, since the registry is
unchanged at `H_B″`; v3.1 l.653-659, §7.4):
```
<date -u +%FT%TZ> OPS-<MMDD>b-r1-pin: PIN scripts/b_pa1/b_pa1_registry.json 3651d1a815cd12349fb610666f8d13a8223599017a4f58a3653f581b55a3265f H_B 6d674cedca8eb0a1d2897d102e2d052b2423b182 (R1, v3.1 l.653-659; model pins internvl2_5_8b=OpenGVLab/InternVL2_5-8B@e9e4c0dc1db56bfab10458671519b7fa3dd29463 internvl2_5_2b=OpenGVLab/InternVL2_5-2B@573169ee54df216786bb9a189e9a32a060a008cf mblip_mt0_xl=Gregor/mblip-mt0-xl@5e3ca094d5de4c53ed5548b20fd21a7787cafd1a mblip_bloomz_7b=Gregor/mblip-bloomz-7b@4d95b91d56fcdce86504c951a28f016b15e219a1 gemma3n_e4b=google/gemma-3n-E4B-it@c1221e9c62e34a43ab7ffacd1be0ea71f126ef10 minicpm_v4=openbmb/MiniCPM-V-4@6f69a8235885be89608f3a71ffd40695b379e1e7 gemma3_4b=google/gemma-3-4b-it@093f9f388b31de276ce2de164bdc2081324b9767 phi3_5_vision=microsoft/Phi-3.5-vision-instruct@12b77fb40b63a2c73c68243d3f767aab688a1b2a molmo_7b_o=allenai/Molmo-7B-O-0924@7a8c4bf80c839c243a6908c6ebbb0f1ee576d7ca llava15_7b=llava-hf/llava-1.5-7b-hf@b234b804b114d9e37bb655e11cbbb5f5e971b7a9 qwen2_5_vl_3b=Qwen/Qwen2.5-VL-3B-Instruct@66285546d2b821cf421d4f5eb2576359d3770cd3 internvl3_2b=OpenGVLab/InternVL3-2B@899155015275a9b7338c7f4677e19c784e0e5a21 qwen2_5_7b=Qwen/Qwen2.5-7B-Instruct@a09a35458c702b33eeacc393d103063234e8bc28 mclip=laion/CLIP-ViT-H-14-frozen-xlm-roberta-large-laion5B-s13B-b90k@f9ab955287d06ac45c7654f26fecd29301c70a1f xlmr=xlm-roberta-large@c23d21b0620b635a76227c604d44e43a9f0ee389; file shas and safetensors totals in the registry; Rule S skips internvl2_5_8b 8075365376 and mblip_bloomz_7b 8163280384; gated manual gemma3n_e4b and gemma3_4b, operator access HTTP 200 on 2026-11-08; lineage per registry, Gemma-3n V = MobileNet-V5 by OPS-1108b-erratum-pin; CC-295r4 (A) GO)
<date -u +%FT%TZ> OPS-<MMDD>b-prompts-pin: PIN scripts/b_pa1/b_pa1_registry.json 3651d1a815cd12349fb610666f8d13a8223599017a4f58a3653f581b55a3265f prompts captioner 8870589c4a32307cbbeb68e363490007682237c0b5a3a1ee7e21cb91fce93886 d1 f39a472f60bb04aeb79c11b3b6317e86c7382ea28085430f1c9357e4ba9327ec d2 4c37cf262e711ee233f1ca4cdda38f05acf1ad86e590ab8b737ee94870716d89 v1 0fba6d6bc88966f1f5cc0b255c8b8484083f9e20fbfe9d455964aa38e5e555bc v2 340e20e1841cd0c94d0b6bd1e34d01e8173bb2974fe2cf2951d77c81f0a775fe ja 8513ac07ea22f59d0be56dca1c6059004fda9a9a08f7caa9b67d2260bc835476 jb 1efe7f049aa8bb48852fe533df0997f0c5bb0bbe8a36a9cb98ad6df96fd1adbe jc 5f556b64c21739a3ce44f3f10f8fb4a33eb1b89017637f637c55c6875b045f61 instrument_i 4ac3f695d09bc4c1ba660a3268aee363db0a55b541ec1b17037c492d46e2dbd4 instrument_ii 79950e29e3a6b9cb0b8e67a4ed34e5be3f9a6ca8461beae94008423606623ac1 (v3.1 §7.4 prompt shas, NFC sha256 of each registry prompts.<name>.text, enforced by load_reg; the English E1 pair is not written, R5 E-12; before block S)
```
- The registry is unchanged by the fix (3651d1a8, CC-300 Subject), so the R1 line carries `H_B′` and the same registry sha (CC-300 W5: the R1 and prompts pins cite `H_B′`).

## 5. Money

### 5.1 L-before (R6 §I.3 rule 3; Part II §2 step 3; PI-1108c; PI-1109a; immediately before renting)
- Read the ckey panel in one page load: the balance B0 and every live rental with its per-instance spent.
  - Expected: none, or Paper C's C-DIAG on its own host (P25).
- **Σ R_j** (RB11) = the remaining capped spend of every other live rental. For C-DIAG, R_CD = 210,000 − S_CD. Its
  cap is "20.0 billed host-hours AND M_D = 210,000 VND, whichever binds first" (`manuscript/prereg/2026-11-08_c_diag/
  C_DIAG_PREREG_DRAFT_v1_2.md` afbb61fb, l.708-712, or the registered C-DIAG file), so its money bound is M_D.
- **Band:** L_eff = B0 − Σ R_j.
  - L_eff ≥ 35 × RH + FEE → cap 28;
  - else L_eff ≥ 29 × RH + FEE → cap 22;
  - else nothing is rented and B waits (PI-1105e PQ-1 (a)).
  - 35 and 29 are cap + 4 h setup + T_down 1 h + 2 h idle margin (R6 §I.3 rule 3).
  - Part II §2 step 1 ("after C's machine is deleted and its delete line and L-after are logged") holds as written:
    OPS-1108a-hc1-deleted, l.1867 (D-1). A parallel C-DIAG is a different block, under PI-1109a.
- **B's real worst case, reserved by C-DIAG's own check** (PI-1109a; PI-1109c point 2: once, without counting B's cap
  twice; binding form CC-299r2 R2-W8 and Ruling 4). C-DIAG's doc owns the check; B states and logs its terms:
  - W_B = max(0, 40 − h_B) × r_B, where h_B is HB-T1's billed hours so far (0 before B rents), and r_B is HB-T1's rate
    (or the offer rate before the rental). 40 h is §0.2's upper bound of billed hours (setup ≤ 4, cap 28, idle ≤ 6 by
    PI-1108d PQ-B1, teardown 1, with margin), so B's cap is inside W_B;
  - O_B = the HB-T1′ resume overhead = the non-cap terms of §12.3 step 2, (4 + 1 + 2) × r_B + FEE, with FEE from the
    rental line (30 at planning). It is 0 once B's one
    resume is used (RESUME.json or RESUME_USED exists) or B's block has ended. The cap left is already inside W_B, so
    the cap is counted once;
  - **W_B + O_B** = 403,680 + 70,674 = **474,354 VND** at 10,092 VND/h before the rental. The PI's "~464k" assumed a
    6 h overhead; the PI's form binds, not the rounded figure, and 7 h is the safe side (CC-299r2 item 11, Ruling 4);
  - this is a **planning reserve** for C-DIAG's check (CC-301r2 NB1). B's binding check is its own §12.3 step 2 at the
    live RH′ + FEE′; a shortfall there is a B wait under "the PI decides", never an overspend;
  - on HB-T1′, h_B = HB-T1′'s own billed hours and r_B = RH′ (40 h ≥ setup 4 + cap left ≤ 28 + idle 6 + teardown 1),
    and O_B = 0, since its one resume is used;
  - HB-CUS is in neither term: it rents only after HB-T1 is deleted, with its own L-before (R6 §I.5).
- Line `OPS-<MMDD>b-hbt1-lbefore` (`date -u`): B0, each live rental by its LOG name with S_j and R_j, L_eff, the band;
  then h_B, r_B, W_B, O_B and "B real worst case (PI-1109c) = W_B + O_B = <VND>".

### 5.2 The offer and the rental line
- **Fields** (R6 §I.1 with PI-1107a; rented-GPU skill):
  - 1 × RTX 3090 / 3090 Ti 24 GB; CUDA ≥ 12.4;
  - **CPU Ryzen 7 5800XT class (8C/16T, Zen 3) or better.** PI-1107a replaces R6 §I.1's 5900X row, as S11 §5.2 did
    (D-5). `manuscript/GPU_RENTAL_SPEC.md` l.10 still reads 5900X and is stale;
  - RAM ≥ 32 GB; disk ≥ 200 GB at ≥ 1000 MB/s; network ≥ 400 Mbps; uptime > 99 %; maximum rental time ≥ 72 h;
  - Ubuntu 24.04, or 22.04 with deadsnakes python3.12.
- **Order** (R6-II ADOPTED W4, with the PI-1108f disk default, D-14):
  - among the offers that pass every field, find the lowest r_host, `r_min`;
  - if an offer with disk ≥ 250 GB has r_host ≤ `r_min`, take the cheapest such offer;
  - otherwise take the cheapest offer, then the lowest setup fee;
  - log the set of accepted offers with r_host, fee and disk at the P-3 decision.
  - Offers come from `/ajax/getgpu3?gpu=RTX%203090&sort=price_asc&count=all`; parse each field's number.
- **No offer passes:** poll every 15 min for up to 12 h, then show the PI the closest (skill). Never rent off-spec.
- Rental line `OPS-<MMDD>b-hbt1-rent` (`date -u`; this stamp is **T0**). It holds:
  - the offer id (LOG only) and every field value, including the disk size;
  - r_host as the panel writes it, RH (rounded up, D-16) and FEE;
  - B0, Σ R_j with each live rental named (C-DIAG or none), L_eff, the band and the cap ("28" or "22 (P-3)");
  - h_B (0), r_B (= RH), W_B, O_B and "B real worst case (PI-1109c) = W_B + O_B = <VND>";
  - "all GPU_RENTAL_SPEC fields met (PI-1107a CPU floor)", R6 v4 0b55d5f8, and this file's sha.
  This line fixes the cap for HB-T1 and HB-T1′.
- **FAULT machine.** If a setup check contradicts the offer, or the free-space check of §6 step 2 fails, no B file
  moves and the machine is deleted; its spend counts. It is not HB-T1. The next accepted rental decides P-3 afresh
  (Part II §2 step 4, N-r2-f). After two FAULT machines in a row, the PI is asked [proposal].

### 5.3 Projection (B0 = 1,079,499 VND after the 500k top-up, OPS-1108d-topup l.1888; RH = 10,092, FEE = 30)

| item | no C-DIAG live | C-DIAG live at its start (R_CD = 210,000) |
|---|---|---|
| L_eff | 1,079,499 | 869,499 |
| 28 h band threshold 35 × 10,092 + 30 = 353,250 | **28 h**, margin 726,249; break-even r ≈ 30,841 VND/h | **28 h**, margin 516,249; break-even r ≈ 24,841 VND/h |
| HB-T1 expected 26.7 h / at most 33 h + FEE / at most + 6 h idle | 269,456 / 333,066 / 393,618 | the same |
| left after HB-T1 at most + 6 h idle (and C-DIAG at its 210k cap) | 685,881 | 475,881 |
| B's real worst case reserved by C-DIAG's own check, W_B + O_B (PI-1109c; CC-299r2 R2-W8) | 474,354 | 474,354 |
| HB-CUS L-before 16 × 10,092 + 30 = 161,502 | passes | passes (margin 314,379) |

- This is a projection only. The band and the cap come from the live L-before.
- PI-1108d PQ-B3 (the PI tops up ≥ 200k before HB-T1's delete) was met early by OPS-1108d-topup (+500k). The tier-3
  funding (PI-1107b) is still separate. The top-up warning of §5.4 applies throughout.

### 5.4 During the block
- **Reads.** Read the panel at each mode start and at the cadence of RB12 (burn = Σ r_live, so C-DIAG's rate is
  added while it is live). Each read gives one line `OPS-<MMDD>b-hbt1-balance`: B0, B's per-instance spent, each other
  live rental's spent, the hours to the next read, and the current h_B, r_B, W_B, O_B and "B real worst case
  (PI-1109c) = W_B + O_B = <VND>" (§5.1), for a C-DIAG check made after B has started (P25).
- **Top-up warning (PI-1108h).** When a read shows B0 ≤ **50,000 VND**, tell the PI at once to top up, in one message
  with B0, the burn and the hours to T. Also warn the PI at least 12 h before the balance would reach T (rented-GPU
  skill): with reads 6 h apart, that is at the first read where (B0 − T) / Σ r_live ≤ 18 h (CC-301 W9). The warning never stops the job; only T does.
- **L-S** (R6 §I.3 rule 5) at the end of mode `s`, together with the trim decision.
- **Money stop** (R6 §I.3 rule 4; reading 20). When a read shows B0 ≤ T (RB9): write the marker, then send one TERM to
  the job by its pid file. **Never `tmux kill-session`.** Between modes, the marker alone stops the next mode at its
  preflight (job l.66).
```sh
. "$HOME/bpa1_env_3.sh"; BAL=${BAL:?balance read}; THR=${THR:?threshold, RB9}
ssh -o BatchMode=yes hbt1 "cd ~/b_pa1_repo && $HPY -I -B scripts/b_pa1/b_pa1_gpu.py money-stop --balance $BAL --threshold $THR" || exit 1
ssh -o BatchMode=yes hbt1 'p=$(cat ~/b_pa1_out/job.pid 2>/dev/null) && [ -d /proc/$p ] && tr "\0" " " < /proc/$p/cmdline | grep -qF scripts/b_pa1/b_pa1_job.sh && kill -TERM "$p"; echo "term rc=$?"' >> "$PRE/money_stop.txt"
```
  - The job forwards the TERM to the running step's process group, closes the ledger step, wipes the set, logs "MONEY
    STOP (final) on signal" and writes `SHA256SUMS_<run>_stop` last (CC-295r4 items 4d-4j).
  - Then §14 and §15. There is no top-up and no resume for this cause.

## 6. Host prep and setup (after T0; every check is a STOP)

1. `ssh-copy-id` (password from a 0600 file outside the repo, never printed); BatchMode login (P18).
2. **Facts → `$PRE/hbt1_facts.txt`**, names and numbers only:
   - `nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader`, and the driver CUDA ≥ 12.4;
   - `lscpu | grep -E 'Model name|^CPU\(s\)|Thread|Core'`;
   - skew (P20); `free -g` ≥ 32; `df -B1 /dev/shm`;
   - **free space: `df -B1 --output=avail ~ | tail -n 1` ≥ 185,000,000,000.** A failure is a bounded setup stop:
     FAULT machine (§5.2). Eager weights × 1.1 = 155.2 GB, plus three venvs and the OS (CC-295r2 Ruling 15);
   - one 4 GB direct-I/O `dd` write and read on `~` (≥ 1000 MB/s each), then `rm ~/bpa1_dd`;
   - `. /etc/os-release; echo $VERSION_ID`;
   - `command -v git tmux rsync flock python3.12`. New hosts may lack python3.12, tmux and rsync (OPS-1108a-hc1-prep):
     `apt-get install -y git tmux rsync util-linux python3.12 python3.12-venv`. On 22.04, first add the deadsnakes PPA.
     This is host prep, with no repo code change;
   - **C toolchain and Python 3.12 headers (CC-303 W1-W3; done on HB-T1 at l.1923).** Gemma's forward auto-compiles
     (torch inductor), which needs a C compiler (selftest stop 1, l.1921). As root, no `apt-get upgrade`: `python3.12
     -V`; `DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential python3.12-dev`; `python3.12 -V`; then
     `command -v gcc cc g++` and `test -f /usr/include/python3.12/Python.h`, each a STOP. After step 4 builds the main
     venv, from `$HOME`: `$HPY -I -c "import torch; f=torch.compile(lambda x: x*2+1); print(f(torch.ones(4,device='cuda')).sum().item())"`
     prints `12.0` with rc 0, else STOP. `gcc --version | head -1`, the `dpkg-query -W` versions of gcc, g++,
     build-essential, python3.12-dev and libpython3.12-dev, python3.12 -V before and after, and the probe rc go to
     `$PRE/hbt1_facts.txt` and the setup line. HB-T1′ runs this as part of its §6 prep (CC-303 W5).
3. Repo: the §1.4 transfer and the host checks.
4. **Setup, main + ungated weights**, in tmux (the weights stage checks need × 1.1 ≤ free before any fetch, setup l.73-77):
   `ssh -o BatchMode=yes hbt1 'cd ~/b_pa1_repo && tmux new -d -s b_setup "bash scripts/b_pa1/b_pa1_setup_host.sh all > ~/b_pa1_setup_all.out 2>&1"'`.
   PASS: `~/b_pa1_out/logs/setup.log` holds `SETUP main OK`, `SETUP weights OK`, `gpu ok`, `main lock 3812fd04 freeze …
   torch 2.6.0+cu124`, `legacy lock 4b2e87fe freeze …`, `open_clip …`, `W venv ok: freeze 1a639a50` (else the R5 §D.2
   laptop fallback for block W, §9.1), `disk ok …`, `refs/main ok xlmr …`. Any `SETUP STOP` = STOP.
5. **Gated weights** (RB7), only after `SETUP weights OK` is in setup.log (step 4 runs in tmux, so the two fetches must
   never overlap); in the foreground, never in tmux; idempotent if the ssh drops:
   `ssh -o BatchMode=yes hbt1 'cd ~/b_pa1_repo && bash scripts/b_pa1/b_pa1_setup_host.sh gated' < ~/.cache/huggingface/token`.
   PASS: `SETUP gated OK`; `ssh -o BatchMode=yes hbt1 'env | grep -c HF_TOKEN'` = 0.
6. **SSCD**: `ssh -o BatchMode=yes hbt1 'mkdir -p ~/b_pa1_models && cat > ~/b_pa1_models/sscd_disc_mixup.torchscript.pt' < "$SSCD_L"`,
   then `ssh -o BatchMode=yes hbt1 'cd ~/b_pa1_repo && bash scripts/b_pa1/b_pa1_setup_host.sh sscd'` → `SETUP sscd OK 9f26bd4c`.
7. **Frame** to `~/b_pa1_out/in/`, sha-checked before the rename:
```sh
. "$HOME/bpa1_env_3.sh"
ssh -o BatchMode=yes hbt1 'cat > ~/b_pa1_out/in/o365_train_frame.tsv.tmp' < "$FRAME" || exit 1
ssh -o BatchMode=yes hbt1 "cd ~/b_pa1_out/in && [ \"\$(sha256sum < o365_train_frame.tsv.tmp | cut -c1-64)\" = $FRAME_SHA ] && mv o365_train_frame.tsv.tmp o365_train_frame.tsv && echo FRAME OK" >> "$PRE/pre.txt"
```
8. **Cap init (RB3, RB16)**, once, from the rental-line values:
```sh
. "$HOME/bpa1_env_3.sh"; CAPH=${CAPH:?28 or 22}; RH=${RH:?}; FEE=${FEE:?}; T0=${T0:?rental line stamp}
ssh -o BatchMode=yes hbt1 "cd ~/b_pa1_repo && $HPY -I -B scripts/b_pa1/b_pa1_gpu.py cap-init --cap-h $CAPH --r-host $RH --fee $FEE --t0 $T0" > "$PRE/cap_init.txt"
```
   It prints the CAP.json sha.
9. `/dev/shm/b_pa1_hb` does not exist before the first push; setup never makes it (setup l.17, l.60).
10. Line `OPS-<MMDD>b-hbt1-setup`: the facts, the free space, python, `H_B`, the setup.log sha, the CAP.json sha, the W
    venv result.

## 7. Push (one per mode; the trap wipes on every exit)

### 7.1 The W farm (laptop; ext4; P17)
Frame names are `images/v1/patchN/<file>`; tar members are `patchN/<file>`. Extraction into `$X/images/v1` puts each
image at `$X/<frame name>`. Tested at v1 drafting on a synthetic fixture.
```sh
. "$HOME/bpa1_env_3.sh"
[ ! -e "$X" ] && [ ! -e "$PUSHW" ] && mkdir -m 700 "$X" "$PUSHW" "$PUSHW.parts" || { echo "GUARD: $X or $PUSHW"; exit 1; }
[ "$(sha256sum < "$FRAME" | cut -c1-64)" = "$FRAME_SHA" ] || { echo "STOP: frame sha"; exit 1; }
N=$((NBLK * 500)); head -n "$N" "$FRAME" | cut -f2 > "$PRE/w_names.txt"
[ "$(wc -l < "$PRE/w_names.txt")" = "$N" ] && [ "$(grep -vc '^images/v1/patch[01]/[^/]*\.jpg$' "$PRE/w_names.txt")" = 0 ] \
  || { echo "STOP: frame names"; exit 1; }
mkdir -p "$X/images/v1"
for p in 0 1; do
  t=$P0TGZ; [ "$p" = 1 ] && t=$P1TGZ
  sed -n "s|^images/v1/\(patch$p/[^/]*\)$|\1|p" "$PRE/w_names.txt" > "$PRE/w_members_p$p.txt"
  ionice -c3 nice -n 19 tar -xzf "$t" -C "$X/images/v1" --no-same-owner -T "$PRE/w_members_p$p.txt" 2> "$PRE/x_p$p.err"
  echo "extract p$p rc=$? names=$(wc -l < "$PRE/w_members_p$p.txt")" >> "$PRE/pre.txt"
done
[ "$(find "$X/images" -type f | wc -l)" = "$N" ] && [ -z "$(find "$X" ! -type d ! -type f)" ] || { echo "STOP: extracted set"; exit 1; }
(cd "$X" && xargs -d '\n' sha256sum < "$PRE/w_names.txt") > "$PUSHW/MANIFEST.sha256"
[ "$(wc -l < "$PUSHW/MANIFEST.sha256")" = "$N" ] || { echo "STOP: manifest count"; exit 1; }
cut -c67- "$PUSHW/MANIFEST.sha256" | awk -v d="$PUSHW.parts" '{ print > sprintf("%s/p%02d", d, (NR-1) % 6) }'
B=$(cut -c67- "$PUSHW/MANIFEST.sha256" | (cd "$X" && xargs -d '\n' stat -c %s) | awk '{s+=$1} END {print s}')
M=$(sha256sum < "$PUSHW/MANIFEST.sha256" | cut -c1-64); echo "WMAN $M n=$N bytes=$B" >> "$PRE/pre.txt"
[ ! -e "$HOME/bpa1_env_w.sh" ] && echo "WMAN=$M" > "$HOME/bpa1_env_w.sh" && chmod 400 "$HOME/bpa1_env_w.sh" || { echo "GUARD: bpa1_env_w.sh"; exit 1; }
```
- `tar -T` streams each 3.8 GB archive once from /mnt/d in the idle I/O class. A non-zero tar rc with the full count is
  recorded, not a STOP; the count and the per-file shas bind.

### 7.2 One push (six streams; pid files; manifest last; stdout-only failing list)
Set `SET=w` or `SET=a` in the calling shell first.
```sh
. "$HOME/bpa1_env_3.sh"; for e in w a; do [ -r "$HOME/bpa1_env_$e.sh" ] && . "$HOME/bpa1_env_$e.sh"; done
T=$(date -u +%Y%m%dT%H%M%SZ)
case "$SET" in w) F=$PUSHW; MAN=${WMAN:-} ;; a) F=$PUSHA; MAN=${AMAN:-} ;; *) echo "SET must be w or a"; exit 1 ;; esac
[ -n "$MAN" ] && [ "$(sha256sum < "$F/MANIFEST.sha256" | cut -c1-64)" = "$MAN" ] || { echo "STOP: manifest sha"; exit 1; }
ssh -o BatchMode=yes hbt1 "[ ! -e /dev/shm/b_pa1_hb/$SET ] && mkdir -p /dev/shm/b_pa1_hb && chmod 700 /dev/shm/b_pa1_hb && mkdir -m 700 /dev/shm/b_pa1_hb/$SET" \
  || { echo "STOP: stale set dir $SET"; exit 1; }
P=$PRE/push_${SET}_$T; mkdir -m 700 "$P" || exit 1
for i in 0 1 2 3 4 5; do
  ( set -o pipefail
    tar -C "$X" -cf - -T "$F.parts/p0$i" | ssh -o BatchMode=yes hbt1 "tar --no-same-owner -C /dev/shm/b_pa1_hb/$SET -xf -" &
    echo $! > "$P/pid.p0$i"; wait $!; echo "p0$i rc=$?" >> "$P/rc" ) &
done; wait
grep -c 'rc=0$' "$P/rc"                                                   # 6, unless a stalled stream was stopped (RB8)
tar -C "$F" -cf - MANIFEST.sha256 | ssh -o BatchMode=yes hbt1 "tar --no-same-owner -C /dev/shm/b_pa1_hb/$SET -xf -"   # the manifest last
ssh -o BatchMode=yes hbt1 "cd /dev/shm/b_pa1_hb/$SET && stat -c %a . && sha256sum < MANIFEST.sha256 && find . ! -type d | wc -l && find . ! -type d ! -type f | wc -l" \
  > "$P/arrival.txt" 2> "$P/arrival.err"
ssh -o BatchMode=yes hbt1 "cd /dev/shm/b_pa1_hb/$SET && sha256sum -c MANIFEST.sha256 2>/dev/null | grep -v ': OK\$'" > "$P/failing.txt"
sed -n 's/: FAILED.*$//p' "$P/failing.txt" | LC_ALL=C sort -u > "$P/top.list"; wc -l < "$P/top.list"
```
- **PASS:** mode 700; sha = MAN; count = n + 1; non-regular 0; `top.list` empty.
- **Stall (RB8):** sample `ssh -o BatchMode=yes hbt1 "du -sb /dev/shm/b_pa1_hb/$SET"` twice, 10 min apart. Then:
  - stop the stalled stream by `kp "$P/pid.p0<i>" ssh`;
  - check that no remote `tar -x` is left: `ssh -o BatchMode=yes hbt1 'ps -eo args | grep -c "[t]ar --no-same-owner -C /dev/shm/b_pa1_hb"'` = 0;
  - write one OPS deviation line.
- **Top-up:** `tar -C "$X" -cf - -T "$P/top.list" | ssh -o BatchMode=yes hbt1 "tar --no-same-owner -C /dev/shm/b_pa1_hb/$SET -xf -"`,
  then both arrival commands again, into `arrival2.txt` / `failing2.txt`. A second failure of the same file = STOP and read.
- Line `OPS-<MMDD>b-hbt1-push-<set>`: stamp, streams, seconds, stopped streams, top-up count, arrival sha and count.

## 8. Host selftest (mode `selftest`) and the R2 line

### 8.1 Run
Re-entry: the two v1.4 selftest runs (l.1921, l.1924) left `JOB STOP` lines in `logs/job.log` and may have left
`HOSTCHECK_*.json`. Before the run at `H_B″`, move any HOSTCHECK file aside (never used again) and record the job.log
length N0; `/dev/shm/b_pa1_hb` must be absent (CC-303 W4):
```sh
. "$HOME/bpa1_env_3.sh"; [ ! -e "$PRE/st_n0.txt" ] || { echo "GUARD: st_n0.txt"; exit 1; }
ssh -o BatchMode=yes hbt1 '[ ! -e /dev/shm/b_pa1_hb ] || exit 1; mkdir -p -m 700 ~/b_pa1_stale_hbp || exit 1
  for f in ~/b_pa1_out/HOSTCHECK_*.json; do [ ! -e "$f" ] || mv -n "$f" ~/b_pa1_stale_hbp/ || exit 1; done
  [ "$(ls ~/b_pa1_out | grep -c "^HOSTCHECK_")" = 0 ] && wc -l < ~/b_pa1_out/logs/job.log' > "$PRE/st_n0.txt" || { echo "STOP: pre-selftest"; exit 1; }
cat "$PRE/st_n0.txt"
```
```sh
. "$HOME/bpa1_env_3.sh"
ssh -o BatchMode=yes hbt1 "cd ~/b_pa1_repo && tmux new -d -s b_st_\$(date -u +%H%M%S) 'bash scripts/b_pa1/b_pa1_job.sh selftest $H_B -'" || exit 1
```

### 8.2 Pass criteria
- `logs/job.log` after line N0 (`$PRE/st_n0.txt`) is `HOSTCHECK OK` then `EXIT selftest rc=0`, with no `JOB STOP`.
  The earlier `JOB STOP` lines (≤ N0) are appended to `$PRE/alerts_seen` before the pull loop starts, so §13 does not
  alert on them again.
- Each pulled HOSTCHECK file's `code` field = 8c39fae7c1296b751e7d2042711b5ea881297c14393e0e95a8e690204e0b5509 (the
  `H_B″` SUMS_GPU), so no stale file is in use.
- Pull `HOSTCHECK_main.json`, `HOSTCHECK_legacy.json`, `freeze_main.sha256`, `freeze_legacy.sha256`, `logs/setup.log`
  and `logs/hostcheck.log` to `$PULL/selftest/`.
- The coordinator checks (T1-T9 as read in CC-295):
  - both Y/N id sets are non-empty and disjoint, and each word's token count and first token are recorded (reading 27);
  - ten single-digit tokens;
  - every captioner's effective decode settings are num_beams 1, do_sample false, repetition_penalty 1.0, 60 new
    tokens (reading 11);
  - each HOSTCHECK file's code / freeze / gpu_uuid fields are filled.
- Any failed criterion = no push; a one-judge read.

### 8.3 R2 line (gatekeeper; after 8.2, before mode `w`; reading 4; not yet written)
```
<date -u +%FT%TZ> OPS-<MMDD>b-r2-pin: PIN freeze_main <64-hex of the pulled freeze_main.sha256> freeze_legacy <64-hex of the pulled freeze_legacy.sha256> freeze_w 1a639a50adf550c50c6dfe284146e279b2a2bf2a716ade743e9eb357ccbf0778 (R2, v3.1 l.653-655, reading 4; first host build on HB-T1 ckey 106594 at H_B′ 6d674cedca8eb0a1d2897d102e2d052b2423b182, selftest at H_B″ 860a3b741ecb82d8fbe31d997212965bc146404a; locks requirements_b_pa1_main.lock 3812fd04 requirements_b_pa1_legacy.lock 4b2e87fe requirements_b_pa1_w.txt 1a639a50; setup.log <sha>; W venv ok; before mode w)
```

## 9. Block W and interlude 1

### 9.1 Push and launch
1. Check `W venv ok: freeze 1a639a50` in the pulled setup.log.
   - If it is absent, use the **R5 §D.2 fallback**: `feats` runs on the laptop in `$WV` with `--images "$X"
     --sscd "$SSCD_L" --parts "$PRE/w25_parts_laptop" --blocks $NBLK`, and no GPU-h is spent.
   - `parity` still runs on those parts, because `decide` needs `parity.json`.
   - The host bills idle meanwhile. Then go to §9.2 step 2.
2. Push the W set (§7.2, `SET=w`).
3. Launch (RB4; the job runs `feats` with the committed flags and the W cap `left --w`, job l.142-150):
```sh
. "$HOME/bpa1_env_3.sh"; for e in w a; do [ -r "$HOME/bpa1_env_$e.sh" ] && . "$HOME/bpa1_env_$e.sh"; done
MODE=${MODE:?w|s|a1decode|a1score|rest}; MAPF=${MAPF:--}; EXTRA=${EXTRA:--}
case "$MODE" in w) MAN=${WMAN:-} ;; *) MAN=${AMAN:-} ;; esac
[ -n "$MAN" ] && [ -n "$H_B" ] || { echo "STOP: MAN or H_B empty"; exit 1; }
T_J=$(ssh -o BatchMode=yes hbt1 date -u +%FT%TZ) && [ -n "$T_J" ] || exit 1
echo "T_J $MODE $T_J MAN=$MAN MAPF=$MAPF EXTRA=$EXTRA" >> "$PRE/pre.txt"
ssh -o BatchMode=yes hbt1 "cd ~/b_pa1_repo && tmux new -d -s b_${MODE}_\$(date -u +%H%M%S) 'bash scripts/b_pa1/b_pa1_job.sh $MODE $H_B $MAN $MAPF $EXTRA'" || exit 1
```
   - For W: `MODE=w EXTRA=$NBLK`. Line `OPS-<MMDD>b-hbt1-w-launch`: T_J, `H_B`, WMAN, NBLK, R6 v4 0b55d5f8, this
     file's sha (R6 §I.7 "a launch line citing this file's sha").
4. Start the pull loop (§13) after this launch.

### 9.2 Interlude 1 (laptop; HB-T1 bills idle)
1. After `JOB DONE w`, take the snapshot pull and check the manifest (RB13): `rsync -a -e 'ssh -o BatchMode=yes'
   hbt1:b_pa1_out/ "$PULL/snap_w/b_pa1_out/"`, then `(cd "$PULL/snap_w/b_pa1_out" && sha256sum --quiet -c
   SHA256SUMS_w)` silent. Check the deletion-log line (W set wiped; count = n + 1).
2. Comparability (R5 §D.2, n = 50): `cd "$R" && "$WV" -I -B scripts/b_pa1/b_pa1_w25.py parity --frame "$FRAME" --images
   "$X" --sscd "$SSCD_L" --parts "$PULL/snap_w/b_pa1_out/w25_parts"`. FAULT = stop and read.
3. The `--extra` manifest. It is built before the rental (P7b) and holds all five C7 caches with their pinned values;
   the owner lists are exactly the meta owners (`load_extra`):
```sh
. "$HOME/bpa1_env_3.sh"; E=$PRE/c7_extra.json; [ ! -e "$E" ] || { echo "GUARD: $E"; exit 1; }
A=$R/.session_backup/2026-11-03/b_pa1/w25slot/out; Q=$R/.session_backup/2026-11-08/b_pa1/p6_laptop/out
cat > "$E" <<EOF
{"caches": {
 "c7a": {"path": "$A/c7_coco_gap_val2014.npz", "sha256": "72b1de15618c4e53ad099666257d5810f263e159e32256df2f5599297bef7a3d", "n": 734, "owners": ["coco_restval_b4", "m0_dev_touched_3454", "refused_chair500", "refused_pope500", "uitviic_train_pool"]},
 "c7b": {"path": "$A/c7_pascal50s_a.npz", "sha256": "00ef39757bb11fa2ac0333ba7b5304a855f41fc91dca39ee8349c4b6337b0c94", "n": 1000, "owners": ["pascal50s_a"]},
 "c7c": {"path": "$A/c7_a_t3_val2017.npz", "sha256": "95144514c601007b512528e7478140f3df9a91885ef40027dd4f6e3136a2ce80", "n": 5000, "owners": ["a_t3_val2017"]},
 "c7_xm3600_all": {"path": "$Q/c7_xm3600_all.npz", "sha256": "90b39859e0c17367c64f4c772451088c046f76b92b94b6c99fad3e3c066a7481", "n": 3600, "owners": ["nocaps_val", "oiv7_val", "xm3600_all", "xm600_a", "xm_test2500_c"]},
 "c7_ktvic_refused_dup": {"path": "$Q/c7_ktvic_refused_dup.npz", "sha256": "24b8603f7c216a102455e2550d92e257ee57e33a40e246d3f38dd3b31625a73e", "n": 1, "owners": ["refused_ktvic_dev_near_duplicate_of_test"]}}}
EOF
chmod 400 "$E"; echo "C7X $(sha256sum < "$E" | cut -c1-64)" >> "$PRE/pre.txt"
```
   - Each cache's LOG pin line carries every token `load_extra` requires (file name, full sha, `n=`, `listed=` /
     `missing=` / `unreadable=` / `truncated=`, list sha). Tested at drafting with `b_pa1.pin_line` on the real LOG
     (read only): True for all five.
   - P7b (coordinator, before the rental) runs `load_extra` on each entry with `EXPECT`. The owner order must match
     the meta; it was not checked at drafting, because the caches hold test-role features.
4. Decide (C5): `cd "$R" && "$WV" -I -B scripts/b_pa1/b_pa1_w25.py decide --frame "$FRAME" --parts
   "$PULL/snap_w/b_pa1_out/w25_parts" --out-dir "$PRE/decide1" --extra "$PRE/c7_extra.json"`. It prints counts only;
   its record must show all five caches compared.
5. **"P6 met" pin** (gatekeeper; P6_RECOMPUTE §6.5 form, tested there with `pin_line`):
```
<date -u +%FT%TZ> OPS-<MMDD>b-decide1-pin: PIN <full 64-hex sha of w25_decide.json> w25_decide.json P6 met (B_RUN_DOC v1.6 §9.2; CC-226r2 Ruling 3(a)(ii): G3 residual 0 for #4 #8 #10 #13 #14 via c7a OPS-1103b-c7a-pin, #24 via c7b OPS-1103b-c7b-pin, #22 via OPS-1108b-p6b-pin; G2 #15-#17 via OPS-1108b-p6a-pin; decide --extra manifest <C7X sha> = c7a c7b c7c c7_xm3600_all c7_ktvic_refused_dup)
```
6. Pick: `"$IJ" -I -B scripts/b_pa1/b_pa1.py slices pick --frame "$FRAME" --decide "$PRE/decide1" --out
   "$PRE/b_pa1_lists.json"`. One OPS line: the lists sha and the slice counts (ids only, no reason text, no overlap
   wording; PI-1101o). **The lists file never goes to the host** (reading 1).

### 9.3 Fewer than 4,000 survivors
`pick` refuses. Then:
- extract up to N′ = (NBLK + k) × 500 names with §7.1, into new `_2` dirs (a retry env);
- build a **full** new W manifest over blocks 0..N′−1, because the trap wiped `w` and `inputs --set w --nblk N′`
  checks the whole set (gpu `w_block_ok`);
- push it as `SET=w`; launch `MODE=w EXTRA=N′` (RK = `wN′`, a new run; `feats` skips the existing parts);
- run a logged decide into `$PRE/decide2`, write a new pin line, then pick.
The added time counts against W's 1.0 GPU-h block cap; a W timeout is a final CAP STOP.

### 9.4 Slice-A farm
```sh
. "$HOME/bpa1_env_3.sh"
[ ! -e "$PUSHA" ] && mkdir -m 700 "$PUSHA" "$PUSHA.parts" || { echo "GUARD: $PUSHA"; exit 1; }
python3 -I -c 'import json,sys; print("\n".join(str(i) for i in json.load(open(sys.argv[1]))["slice_a"]))' "$PRE/b_pa1_lists.json" > "$PRE/a_ids.txt"
awk -F'\t' 'NR==FNR { a[$1]; next } ($1 in a) { print $2 }' "$PRE/a_ids.txt" "$FRAME" > "$PRE/a_names.txt"
[ "$(wc -l < "$PRE/a_ids.txt")" = 2000 ] && [ "$(wc -l < "$PRE/a_names.txt")" = 2000 ] || { echo "STOP: slice A count"; exit 1; }
[ "$(grep -F -x -f "$PRE/a_names.txt" <(cut -c67- "$PUSHW/MANIFEST.sha256") | wc -l)" = 2000 ] || { echo "STOP: slice A not in the W set"; exit 1; }
(cd "$X" && xargs -d '\n' sha256sum < "$PRE/a_names.txt") > "$PUSHA/MANIFEST.sha256"
cut -c67- "$PUSHA/MANIFEST.sha256" | awk -v d="$PUSHA.parts" '{ print > sprintf("%s/p%02d", d, (NR-1) % 6) }'
M=$(sha256sum < "$PUSHA/MANIFEST.sha256" | cut -c1-64); echo "AMAN $M n=2000" >> "$PRE/pre.txt"
[ ! -e "$HOME/bpa1_env_a.sh" ] && echo "AMAN=$M" > "$HOME/bpa1_env_a.sh" && chmod 400 "$HOME/bpa1_env_a.sh" || { echo "GUARD: bpa1_env_a.sh"; exit 1; }
```
- `a_names.txt` is in frame order, which is slice order (reading 1).
- AMAN goes into one OPS line `OPS-<MMDD>b-hbt1-aman` before the first `SET=a` push. The host takes slice A from the
  manifest names in frame order, and the gate set is its first 231.

## 10. Block S
1. Push slice A (`SET=a`); launch `MODE=s` (§9.1 block).
2. Mode `s` runs, in order: `s.gate.<k>` for the 10 walk models (desk skips from the registry: candidates 1 and 4
   fail Rule S), `s.a4rate` (16 images per A4 model), `s.smoke` (64 images, rates only), `s.trim`. It writes
   `out/s/ACCEPT.json`, `rates_smoke.json`, `rates.json` and `TRIM.json`, and logs "E1 E2 NOT RUN (pre-fixed, R5
   E-12)" (readings 8, 9, 23, 28).
3. Outcomes:
   - **PA3** (fewer than 4 accepted): rc 3, PA3.json, `SHA256SUMS_s_stop` (job l.163). Go to §12.4.
   - **CORE STOP** (core does not fit): rc 13, CORE_STOP.json (job l.164-165). Go to §12.4.
   - **JOB DONE s**: snapshot pull to `$PULL/snap_s/` and check `SHA256SUMS_s` (RB13).
4. Lines:
   - `OPS-<MMDD>b-hbt1-s`: the accepted list (registry keys), gate shares, rates.json sha;
   - `OPS-<MMDD>b-hbt1-trim`: TRIM.json sha, cap left, the kept and dropped blocks;
   - `OPS-<MMDD>b-hbt1-ls` (L-S): balance and per-instance spent (B's and any other live rental's); the PI-1108h top-up warning if B0 ≤ 50,000.

## 11. A1-decode, interlude 2, A1-score, rest

### 11.1 A1-decode (CC-300 W1)
Push slice A; launch `MODE=a1decode`. After `JOB DONE a1decode`, the job writes the narrow `SHA256SUMS_a1decode`
**before** its EXIT line and `SHA256SUMS_a1decode_all` **last** (job l.50-52, l.170-174). The narrow file can therefore
exist before `_all`, so the wait is on `_all`. Then comes a full check of `_all`, and a check that the 4 narrow lines
each stand verbatim in `_all` (`_all` covers out, logs and w25_parts, so it does not hash the narrow file itself):
```sh
. "$HOME/bpa1_env_3.sh"; S=$PULL/snap_a1decode/b_pa1_out
ssh -o BatchMode=yes hbt1 'tail -n 1 ~/b_pa1_out/logs/job.log | grep -q "EXIT a1decode rc=0" && [ -s ~/b_pa1_out/SHA256SUMS_a1decode_all ] && flock -n ~/b_pa1_out/.job.lock true' \
  || { echo "WAIT: SHA256SUMS_a1decode_all not written yet (or the job still holds its lock)"; exit 1; }
[ ! -e "$S" ] || { echo "GUARD: $S exists"; exit 1; }
mkdir -p "$(dirname "$S")" && rsync -a -e 'ssh -o BatchMode=yes' hbt1:b_pa1_out/ "$S/" || exit 1
(cd "$S" && sha256sum --quiet -c SHA256SUMS_a1decode_all) || { echo "STOP: SHA256SUMS_a1decode_all check"; exit 1; }
[ "$(wc -l < "$S/SHA256SUMS_a1decode")" = 4 ] && [ -z "$(grep -vxFf "$S/SHA256SUMS_a1decode_all" "$S/SHA256SUMS_a1decode")" ] \
  || { echo "STOP: the narrow manifest is not 4 lines of _all"; exit 1; }
grep -m 1 'JOB DONE a1decode' "$S/logs/job.log" | cut -c1-20 > "$PRE/t_i0.txt"; cat "$PRE/t_i0.txt"
```
- **t_i0** = the host stamp of the `JOB DONE a1decode` line. The 6 h idle window and the (i) cut-off (RB14) run
  from t_i0.
- Line `OPS-<MMDD>b-hbt1-a1decode`: t_i0, the `_all` sha and its line count, the narrow sha (4 lines).

### 11.2 Interlude 2 (laptop; HB-T1 bills idle ≤ 6 h, PI-1108d PQ-B1)
`SNAP=$PULL/snap_a1decode/b_pa1_out`. Every step-4 file goes under `$S4`; the D-8 (ii) entries are at `$D8II`. All
commands run from `$R` with `$MP -I -B scripts/b_pa1/…`. At `H_B″` (mid unchanged), `coverage --pulled` and `htrans` read exactly the
narrow `SHA256SUMS_a1decode` and `SHA256SUMS_s` of `$SNAP` (F-1 closed; CC-300 item 4: the committed
`pulled_captions` accepts the job's manifests).

1. **Block-H input** (only if TRIM keeps H; else HIN = `-`): `$MP -I -B scripts/b_pa1/b_pa1_mid.py htrans --pulled "$SNAP"
   --lists "$PRE/b_pa1_lists.json" --frame "$FRAME" --out "$S4/h_input.jsonl"`. Then the push of `in/h_input.jsonl`:
```sh
. "$HOME/bpa1_env_3.sh"; H=$S4/h_input.jsonl; HIN=$(sha256sum < "$H" | cut -c1-64)
ssh -o BatchMode=yes hbt1 'cat > ~/b_pa1_out/in/h_input.jsonl.tmp' < "$H" || exit 1
ssh -o BatchMode=yes hbt1 "cd ~/b_pa1_out/in && [ \"\$(sha256sum < h_input.jsonl.tmp | cut -c1-64)\" = $HIN ] && mv h_input.jsonl.tmp h_input.jsonl && echo HIN OK $HIN" >> "$PRE/pre.txt"
```
   - Line `OPS-<MMDD>b-hbt1-hin`: HIN, row count (231 × 6 = 1,386), `htrans` at `H_B`. HIN becomes EXTRA for `rest`.
2. **Coverage** (§6.1 (i) and (ii); counts only): `$MP -I -B scripts/b_pa1/b_pa1_mid.py coverage --pulled "$SNAP" --map
   "$MAP1" --categories "$CATS" --out-dir "$S4/cov"`. A record line `OPS-<MMDD>b-coverage-pin: PIN coverage.json
   <64-hex> (step 4 statistics from the a1decode snapshot; tokens_i <n>; classes_ii 262; counts only)` follows.
3. **The (i) path** (D-8 §2, §7; CC-295r3 interlude note; inside RB14's cut-off):
   - **draft**: if tokens_i > 0, the agent drafts `$S4/d8_i/b_pa1_d8_i_entries_v1.json` (this exact name: the
     validator and the md §7 form require it) from the (i) token list only, under D8-1..D8-8 and the §3 readings
     (CC-296 Ruling 2, CC-296r2 Ruling 7, CC-296r3 N13). Every entry has src i; `provenance.amendment` = {name: the
     md v1.3 repo path, sha256: c041c4ab…}.
   - **no entry proposed:** if tokens_i > 0 but the D8 rules give no entry for any listed token, there is no (i)
     file, no validate and no (i) pin. The validator's `src_i` check needs ≥ 1 entry, so a retry would loop while
     HB-T1 bills. `amend` runs with (ii) only, and one OPS line `OPS-<MMDD>b-step4-i-none` records it with the
     token count and states that no (i) entry was added, so no irreversible read was needed (CC-301 item 11, W8). This is the rules' outcome, not the PI-1108f fallback, though the map result is the same;
   - **validate** (F-2; CC-300 Ruling 3), on the laptop. (A) and (B) already stand on the real LOG (l.1881-1882); the
     default `--entries-ii` is the pinned (ii) file `$D8II`:
```sh
. "$HOME/bpa1_env_3.sh"; cd "$R" || exit 1
$MP -I -B scripts/b_pa1/b_pa1_d8i_validate.py --entries-i "$S4/d8_i/b_pa1_d8_i_entries_v1.json" --coverage "$S4/cov/coverage.json" \
  > "$S4/d8_i/validate.txt"; echo "rc=$?" >> "$S4/d8_i/validate.txt"; cat "$S4/d8_i/validate.txt"
```
     `validate.txt` then has 2 lines: line 1 the validator's result line, line 2 `rc=<n>`. Expected on PASS (rc 0),
     line 1 has counts and 8-hex shas only (validator l.88-94):
     `validate_d8i code=21857fd0 mid=b8afa120 md=c041c4ab entries_ii=6ad473f3 entries_i=<8-hex> coverage=<8-hex>: (A)+(B)
     on LOG yes; (ii) added 347/347; (i) added <n>/<n> for <t> of <k> listed tokens; LOG_RE <347+n>/<347+n>; final
     221+<347+n>; RESULT PASS`. Then:
     - `RESULT FAIL <checks>` with rc 1 is a refusal. The draft is corrected under the same name and validated again.
       Nothing is pinned or amended from a FAIL;
     - after the (i) pin, the file never changes.
   - **read**: a one-judge FULL read at IRREVERSIBLE 85 of the (i) file and the PASS line;
   - **pin** (gatekeeper; D-8 §7 (i) form, verbatim):
```
<date -u +%FT%TZ> OPS-<MMDD>b-d8i-pin: PIN b_pa1_d8_i_entries_v1.json <full 64-hex sha> (D-8 part (i) entries, git-excluded; provenance.amendment = D8_AMENDMENT_DRAFT_v1_3.md c041c4ab; CC-295r2 W7; read by CC-<id> GO at irreversible 85 (mid-run, D-8); (i) <n> entries for <n> listed tokens of coverage.json <8-hex>; mid <8-hex>; validate: <the quoted one-line result>; logged only at step 4, after (ii))
```
   - the `validate:` slot carries line 1 of `validate.txt` (the PASS line) verbatim, never the `rc=` line; `coverage.json <8-hex>` and `mid <8-hex>`
     are the `coverage=` and `mid=` values of that line (b8afa120);
   - **fallback** (PI-1108f Q2): if tokens_i = 0, or the read is not GO by t_i0 + 5 h, step 4 closes with map v1 +
     D-8 (ii) only. One OPS line `OPS-<MMDD>b-step4-fallback` records the reason; the (i) part is reported as not
     added.
4. **Amend**, (ii) first, then (i) if pinned: `$MP -I -B scripts/b_pa1/b_pa1_mid.py amend --coverage "$S4/cov/coverage.json"
   --map "$MAP1" --categories "$CATS" --entries "$D8II" --log "$S4/b_pa1_map_amendments.log"`, then the same with
   `--entries "$S4/d8_i/b_pa1_d8_i_entries_v1.json"`. Each prints `added` and `log_lines`.
5. **Final**: `$MP -I -B scripts/b_pa1/b_pa1_mid.py final --map "$MAP1" --categories "$CATS" --log
   "$S4/b_pa1_map_amendments.log" --out-dir "$S4/final"`. It prints `final_map_sha256` (= MAPF) and `crosswalk_sha256`
   (= 869ab3e8…).
6. **Mapfinal pin** (gatekeeper; reading 17; tested at drafting with `map_v1.at` and PIN_RE):
```
<date -u +%FT%TZ> OPS-<MMDD>b-mapfinal-pin: PIN b_pa1_map_final.json <MAPF 64-hex> crosswalk 869ab3e84dab3749691f3e91ee981124f721d47f7718bd737214e9fe8bb42631 map_v1 497b430abfcdc1ef6d36cb306e7c3b76fd1bedac2a500584f0d80244e6a3fed5 amendments_log <64-hex sha of b_pa1_map_amendments.log> (v3.1 §6.4 step 4 closed; final map frozen; n_added <n> = (ii) <n> + (i) <n>; D-8 v1.3 c041c4ab; mid b8afa120; no amendment after this line)
```
7. **Parity run 2** (v3.1 §6.3; once). The coordinator re-hashes the three input files; they must equal the l.1335
   tokens. Then, after the mapfinal pin, exactly one start line, with the run dir = the resolved `$S4/final` (tested:
   pin then start → accepted; start before pin, two starts or no pin → refused):
```
<date -u +%FT%TZ> OPS-<MMDD>b-parity2-start: <MAPF 64-hex> 869ab3e84dab3749691f3e91ee981124f721d47f7718bd737214e9fe8bb42631 54abc0fb068ad1108d7d57b21328d4d68bcf8f41aa168f80ec7c275fb4ac8214 278d15b97e3eeb9496a0282bb91deb365117becf24d174fbb1e0507203b12ea4 c52a96d18925b974878ae1a970c3f9133fb3482216676fd41871eeabb68cc77f <resolved $S4/final> (parity run 2, ONCE, binding: v3.1 §6.3/§6.4 step 5; tokens = final map, crosswalk, UIT-ViIC test refs, instance gold, exclusion.json, run dir; PA3 fires iff |Delta micro| > 2.0)
```
   Then `$MP -I -B scripts/b_pa1/b_pa1_mid.py parity2 --map "$S4/final/b_pa1_map_final.json"`, and the done line:
```
<date -u +%FT%TZ> OPS-<MMDD>b-parity2-done: <MAPF 64-hex> rc <rc>; parity2.json <64-hex> (O_EXCL, once). Printed record only: delta_micro_points <x>, abs_delta_micro_gt_2 <bool>, delta_macro_points <x>, n_refs <n>, drop counts as printed
```
   - **|Δ| > 2.0 → PA3** (D-15): `ssh -o BatchMode=yes hbt1 'printf "{\"pa3\": \"parity run 2\"}\n" > ~/b_pa1_out/PA3.json'`,
     then §14 and §15; the PI is told.
8. Line `OPS-<MMDD>b-step4-closed`: t_i0, the close stamp (≤ t_i0 + 6 h), MAPF, HIN, idle hours billed.

### 11.3 A1-score and rest
- Push slice A; launch `MODE=a1score MAPF=<MAPF>` (EXTRA `-`). After JOB DONE: snapshot pull and manifest check.
- Push slice A; launch `MODE=rest MAPF=<MAPF> EXTRA=<HIN or ->`. The job refuses a TRIM that keeps H without a 64-hex
  EXTRA (job l.126). `JOB DONE rest` or a final stop ends the block.

## 12. Stops and the resume rule (v3.1 l.517-520; readings 20-24, 30-31)

### 12.1 Stop classes

| class | job signal | rule |
|---|---|---|
| CAP STOP | rc 124; rc 137 with EL ≥ LEFT; LEFT ≤ 0; a W timeout | final (CAP_STOP.json, `SHA256SUMS_<run>_stop`); §14 |
| MONEY STOP | MONEY_STOP.json + one TERM (§5.4) | final; no top-up, no resume |
| PA3 | rc 3 (walk), or parity run 2 (RB15) | final; §12.4 |
| CORE STOP | rc 13, CORE_STOP.json (written by `s.trim` or the job) | final; the PI decides (v3.1 l.506 as R5 E-12); §12.4 |
| guard failure | a job refusal (sha, freeze, manifest, tmpfs mode, MAPF / EXTRA form), or rc 137 before LEFT (OOM, outside KILL) | the one registered resume (§12.2) after a one-judge cause read |
| machine loss | ssh dead; host gone or rebooted | the one registered resume as HB-T1′ (§12.3) |
| other JOB STOP | a step rc ≠ 0 that is not a guard | not a registered resume cause: one OPS line within 15 min; the PI decides. If the wait exceeds the setup time, pull and delete (PI-1031c) |

**W stop 1 (l.1939), classified.** `w.feats9` ended rc 1 (`ModuleNotFoundError`) 1 s after its START, before any part
file: a step rc ≠ 0 that is not a guard (§12.1 "other JOB STOP"), caused by a run-doc defect (the §1.4 sparse set), not
by the code, the data or the machine. It is not a registered resume cause, so **no resume is used**: RESUME.json and
RESUME_USED stay absent, and the one resume stays for a guard failure or machine loss. Under PI-1109d the restart is
not one of the four PI kinds, so the coordinator decides it. PI-1109f (another machine) is not needed: the selftest
passed on this host. The decision is §0.4b: fix the run doc, move the stopped run's marker aside after its checks, and
run W again as the same run `w9`. The ledger keeps `w.feats9` = 1 s, so the cap and `left --w` count it.

### 12.2 Same-host resume (guard failure; once in total)
1. Host state: the set dir is absent and the deletion log's last line count is as expected. A trapped exit always
   wipes (reading 31); only a KILL of the job leaves it, and then wipe by hand: `ssh -o BatchMode=yes hbt1 "cd ~/b_pa1_repo && $HPY -I -B scripts/b_pa1/b_pa1_gpu.py wipe --dir /dev/shm/b_pa1_hb/<set> --log ~/b_pa1_out/b_pa1_hb_deletions.log"`.
2. Cause read GO (one judge, REVERSIBLE 85): CC id `CC-<id>`.
3. `ssh -o BatchMode=yes hbt1 "cd ~/b_pa1_repo && $HPY -I -B scripts/b_pa1/b_pa1_gpu.py resume --cause guard --cc CC-<id>"`.
   Add `--close-sec <N>` only if the ledger has an open step (after a KILL), with N from the pull-loop evidence. It
   writes RESUME.json (exclusive) and moves torn tails aside.
4. Re-push the set; restart the same mode with the same `H_B`, MAN, MAPF and EXTRA. The job makes `RESUME_USED`
   (noclobber) and skips finished steps.

### 12.3 Machine loss: HB-T1′ (reading 21; CC-295r3 N-i; CC-295r4 N-j; CC-300 W2, W3; PI-1108i)
Preconditions:
- the lost machine is confirmed gone on the panel (R6 §I.5 item 4);
- the last pull `$PULL/loop/b_pa1_out/` is on the laptop;
- a **one-judge read of a short machine-loss addendum** (REVERSIBLE 85). PI-1108i licenses the one re-rental with no
  fresh PI line (D-17). The addendum states the loss evidence, S, SW, the restore list below and the branch taken.

**Branch, decided from the pull (N-j: a branch, not a sequence):**
- **Either `RESUME.json` or `RESUME_USED` is in the pull → no resume.** The one resume is used, and the PI decides
  (v3.1 l.519-520). No HB-T1′ is rented under this file.
- **Neither is present → HB-T1′,** in this order. This holds whichever mode was running, `w` included: F-3 is closed,
  so W's 1.0 GPU-h stays one total over both hosts.
  1. **S and SW** from the pulled `ledger.jsonl` (D-12; CC-300 W2):
     - S = the sum of `sec` over all ended steps, plus, for an open step, the seconds from its `start` stamp `t` to the
       **later** of the last pull-loop evidence stamps (the last `pull.log` line and the last host-stamped `job.log`
       line in the pull);
     - SW = the sum of `sec` over the ended steps whose name starts with `w.`, plus the same open-step seconds if the
       open step is a `w.` step;
     - so SW ≤ S by construction, which `cap-init` also enforces;
     - **whole ledger lines only.** The pull loop runs `rsync --partial`, so a loss mid-pull can leave the pulled
       `ledger.jsonl` with a torn last line, which is ignored. If `job.log` shows `START <step>` with no whole ledger
       `end` for it, that step counts as open from the earlier of its whole ledger `start` `t` and its job.log
       `START` stamp (the safe side of D-12);
     - every such open step is counted: several `START` lines with no whole ledger `end` add up, one open part each;
     - a `logs/done.<step>` with no whole ledger `end` for that step also counts the step as open, by the same rule;
     - S and SW are whole seconds: each open part is rounded **up** to a whole second before the sum (`cap-init` takes
       an int);
     - why `job.log` covers a truncated ledger (CC-301 item 10): rsync sends in sorted name order, and `ledger.jsonl`
       sorts before `logs/`. A loss that truncates the ledger stops the pull before `logs/`, so the pulled `job.log` is
       the earlier full copy. Each step whose ledger lines are lost then shows as a `START` with no whole ledger `end`
       and is counted open up to the last evidence stamp: an over-count, the safe side of D-12;
     - both values and their evidence lines go into the addendum.
  2. L-before for HB-T1′ (Part II row C-11; §5.1 with Σ R_j): L_eff ≥ (cap left + 4 + 1 + 2) × RH′ + FEE′, with cap
     left = CAPH − S/3600. If it fails, there is no cap switch and the PI decides.
  3. Rent under §5.2. The cap is not re-decided (Part II §2 step 5). Alias `hbt1p`.
  4. §6 prep (the step 2 C toolchain and probe included, CC-303 W5), facts, repo and setup on a fresh `~/b_pa1_out`. The new freeze files must equal the R2 pin line, else STOP
     and read. Then the frame (§6 step 7), and:
     `ssh -o BatchMode=yes hbt1p "cd ~/b_pa1_repo && $HPY -I -B scripts/b_pa1/b_pa1_gpu.py cap-init --cap-h $CAPH --r-host $RH2 --fee $FEE2 --t0 $T02 --used-sec $S --used-w-sec $SW"`.
  5. **Restore** into the fresh `~/b_pa1_out`:
     - each **finished** mode's `out/<mode>/` from its manifest-checked snapshot `$PULL/snap_<mode>/b_pa1_out/` (RB13).
       Only the interrupted mode's `out/<mode>/` comes from the loop pull; `resume`'s `untorn` handles its torn tails;
     - `logs/` and `RUN.*` from the loop pull, **without any `logs/done.<IM>.*`** of the interrupted mode `IM`
       (`--exclude "done.$IM.*"` on that rsync; CC-301r2 NB2). Every step name starts with its mode (gpu l.500-520,
       job `w.feats<N>`), so each step of `IM` runs again (job l.138) and skips what exists: `Out` skips existing
       keys (gpu l.303-317; every a1decode / a1score / rest step writes through it, l.777-837), and the block-S steps
       write only what is absent (gpu l.715-765, gate l.840-846).
       This covers every step, the ja / clip / verify outputs included. The finished modes' `done.*` are restored;
     - the **finished parts** `w25_parts/part_*.npz` that pass a laptop load-check (CC-300 W3; the pull's `--partial`
       can leave a short file under its final name). Never a `.part_*` temp file. The source is keyed on the
       interrupted mode `IM` (CC-301 W7):
       - `IM` = `w` (the first W run or a §9.3 run): the loop pull, load-checked, since its newest parts exist only
         there;
       - `IM` ≠ `w`: W is finished, so the parts come from `$PULL/snap_w/b_pa1_out/w25_parts`, the snapshot of the
         last JOB DONE w (§9.2 step 1 runs after every JOB DONE w, a §9.3 run included; the job names that manifest
         `SHA256SUMS_w`, job l.170). Its §9.2 step 1 check is re-run first; a failure is a STOP. If W ran on the
         laptop (§9.1 R5 §D.2 fallback), there are no host parts and nothing is restored:
```sh
. "$HOME/bpa1_env_3.sh"; IM=${IM:?set IM to the interrupted mode}; P=$PULL/loop/b_pa1_out/w25_parts
if [ "$IM" != w ]; then P=$PULL/snap_w/b_pa1_out/w25_parts
  [ -d "$P" ] || { echo "no host W parts (laptop W): nothing to restore"; exit 0; }
  (cd "$PULL/snap_w/b_pa1_out" && sha256sum --quiet -c SHA256SUMS_w) || { echo "STOP: snap_w manifest"; exit 1; }
fi
K=$PRE/hbt1p_parts.txt; [ ! -e "$K" ] || { echo "GUARD: $K"; exit 1; }
cd "$R" && "$WV" -I -B -c '
import sys
from pathlib import Path
sys.path[:0] = [sys.argv[1] + "/scripts/b_pa1", sys.argv[1] + "/scripts/w25"]
import b_pa1_w25 as W
for p in sorted(Path(sys.argv[2]).glob("part_*.npz")):
    try:
        f, m = W.w25.load(p), W.part_meta(p)
        ok = m.get("frame_sha256") == sys.argv[3] and m.get("block") == int(p.stem.split("_")[1]) and len(f["ids"]) == 500 and not f["unreadable"]
    except Exception as e:
        ok = False; print(p.name, "error", type(e).__name__, file=sys.stderr)
    print(p.name, "keep" if ok else "drop")' "$R" "$P" "$FRAME_SHA" > "$K" || exit 1
sed -n 's/ keep$//p' "$K" > "$K.list"; wc -l < "$K.list"
rsync -a --files-from="$K.list" -e 'ssh -o BatchMode=yes' "$P/" hbt1p:b_pa1_out/w25_parts/
```
       The kept and dropped names go into the addendum. A dropped or missing block is computed again by `feats`
       within W's budget (3600 − SW);
     - **never** CAP.json, `ledger.jsonl`, `freeze_*.sha256` or `HOSTCHECK_*.json`.

     **Why the parts are restored (D-18).**
     - `feats` skips a block whose part file exists (`b_pa1_w25.py` l.256), so W resumes from the parts that exist.
       Without them, W would redo every block on 1.0 GPU-h − SW, and a W timeout is a final CAP STOP for the run
       (CC-300 W3 (c)).
     - A part is written by temp-and-rename, so a pulled `part_*.npz` is a finished file.
     - Both hosts run W in the same frozen venv (1a639a50, job l.122) with the same SSCD file (9f26bd4c), so the parts
       of the two hosts are one feature set.
     - The §9.2 parity check (n = 50, laptop against `part_0000`) re-checks block 0, whichever host made it.
     - `decide` re-checks that the parts are blocks 0..n−1 of the frame (`frame_feats`).
  6. `resume --cause machine --cc CC-<addendum read>`. The fresh ledger has no open step, so there is no `--close-sec`.
  7. If the interrupted mode is `rest` and TRIM keeps H: re-push `$S4/h_input.jsonl` to `~/b_pa1_out/in/` with the
     §11.2 sha-checked block (the job checks it against EXTRA, gpu l.803-805).
  8. Mode `selftest` on HB-T1′ (fresh HOSTCHECK, new uuid; reading 29), then re-push the interrupted mode's set (the
     full W set under WMAN for `w`, slice A otherwise), then restart the interrupted mode with the same arguments.
     The job sees `RUN.<RK>.started` and `RESUME.json` and makes `RESUME_USED`; the existing parts and rows are skipped
     (step 5).

### 12.4 Final stops other than CAP and MONEY (PA3, CORE STOP)
- The final pull (§14) and a check of `SHA256SUMS_<run>_stop`. One OPS line `OPS-<MMDD>b-hbt1-pa3` or `-corestop`
  quotes the job line.
- The PI is told, with a recommendation. No later mode can run on this `~/b_pa1_out` (job l.66; reading 24), and no
  cap can change after rates exist (W13). So the host is deleted right after the pull (§15) [proposal].

## 13. Backups every 30 min (laptop; no /dev/shm)
```sh
#!/bin/bash
# B-PA1-T1 HB-T1 pull loop: b_pa1_out only, every 30 min. No tmpfs path.
. "$HOME/bpa1_env_3.sh"; A="$PRE/alerts.txt"
mkdir -p "$PULL/loop"
while true; do
  t0=$(date +%s)
  rsync -a --partial --timeout=600 -e 'ssh -o BatchMode=yes -o ConnectTimeout=30' \
    hbt1:b_pa1_out/ "$PULL/loop/b_pa1_out/" 2>> "$PULL/loop/rsync.err"; rc=$?
  echo "$(date -u +%FT%TZ) pull rc=$rc $(du -sb "$PULL/loop" | cut -f1)" >> "$PULL/loop/pull.log"
  [ "$rc" != 0 ] && echo "$(date -u +%FT%TZ) PULL rc=$rc" >> "$A"
  grep -h 'JOB STOP\|CAP STOP\|MONEY STOP\|PA3 STOP\|CORE STOP\|JOB DONE\|RESUME' "$PULL/loop/b_pa1_out/logs/job.log" 2>/dev/null \
    | while IFS= read -r x; do grep -qxF -- "$x" "$PRE/alerts_seen" 2>/dev/null && continue
        echo "$x" >> "$PRE/alerts_seen"; echo "$(date -u +%FT%TZ) $x" >> "$A"; done
  s=$(( 1800 - ($(date +%s) - t0) )); [ $s -gt 0 ] && sleep $s
done
```
- Start it after the W launch, in the S11 self-pid form:
  `setsid nohup bash -c 'echo $$ > "$1"; exec bash "$2"' _ "$PRE/pull.pid" "$PRE/bpa1_pull.sh" > /dev/null 2>&1 < /dev/null &`.
  Stop it only by `kpg "$PRE/pull.pid" bpa1_pull.sh`.
- It pulls to laptop ext4 only; /mnt/d gets one copy at §14. It never pulls `~/b_pa1_models` (weights) or tmpfs.
- B's logs live in `~/b_pa1_out/logs/`, never under `out/`. Every file under `out/` is a model output or a block
  record. A laptop tool takes its input list from a mode manifest, so a log file cannot be mistaken for an output (the
  C lesson of OPS-1108c-s16-fault1, where ids logs sat under `out/logs/`).

## 14. Final pull and verification (after JOB DONE rest or a final stop)
1. The trap ran: `logs/job.log` ends with the EXIT line; the deletion log's last line count is as expected;
   `ssh -o BatchMode=yes hbt1 '[ ! -e /dev/shm/b_pa1_hb/a ] && [ ! -e /dev/shm/b_pa1_hb/w ]'` rc 0;
   `ssh -o BatchMode=yes hbt1 'flock -n ~/b_pa1_out/.job.lock true'` rc 0 (no job running).
2. Stop the pull loop: `kpg "$PRE/pull.pid" bpa1_pull.sh`.
3. Final pull: `rsync -a -e 'ssh -o BatchMode=yes' hbt1:b_pa1_out/ "$PULL/final/b_pa1_out/"`, and `git rev-parse HEAD`
   plus the `git diff --quiet HEAD --` rc of `~/b_pa1_repo`.
4. Verify (RB13, D-13):
   - the last manifest passes `sha256sum -c` in full, `logs/job.log` included (the EXIT trap writes it last). It is
     `SHA256SUMS_rest`, or the `_stop` one, or **`SHA256SUMS_a1decode_all`** where a1decode is the last done mode
     (e.g. after a PA3 at parity run 2);
   - each earlier manifest passes on its non-`logs/` lines: `SHA256SUMS_w`, `SHA256SUMS_s`,
     **`SHA256SUMS_a1decode_all`** and `SHA256SUMS_a1score`. Their `logs/` lines were checked by that mode's snapshot
     pull, because logs are append-only across modes;
   - under HB-T1′ the earlier manifests are not restored to the new host, so their non-`logs/` checks run on the
     `$PULL/snap_<mode>` copies (CC-301r2 NB4);
   - the narrow `SHA256SUMS_a1decode` (4 lines) passes in full, and each line stands in `_all` (CC-300 W1);
   - every jsonl ends in `\n`, ids are unique (counts only), CAP.json sha = the setup line, TRIM / ACCEPT / rates shas
     = the `s` lines.
5. One copy of `$PULL/final` and every `$PULL/snap_*` to `.session_backup/machines/HBT1/root/`, with SHA256SUMS, at a
   time with no other heavy /mnt/d writer.
6. Line `OPS-<MMDD>b-hbt1-pulled`: files, bytes, manifest shas and results, the dropped blocks, every STOP / resume line.

## 15. Wipe, delete, L-final, L-after
1. The trap logged the wipe (R6 §I.4 item 4); §14 step 1 checked it.
2. **L-final:** HB-T1's per-instance spent, with the page reloaded, immediately before the delete click; and the
   balance.
3. Delete HB-T1 in the panel, after checking that the instance is the one behind the `hbt1` alias.
4. **L-after:** the balance; HB-T1 absent. Cross-check L-before − L-after (RB10).
5. Line `OPS-<MMDD>b-hbt1-deleted`: L-final, L-after, the deletion-log line, the block spend, the cross-check.
6. Laptop retention: `$X` stays until the tier-2 plan rules (slice B is staged from it); manifests and parts stay as
   records.

## 16. Hand-off (not part of this file's licence)
- Laptop §6.4 steps 6-8: the gold join of slice A, the baselines, `T1_THRESHOLDS.json` and its LOG sha, then any τ of
  B. Each needs its code read first. `b_pa1_dev_contacts.json` comes from the pulled files (reading 25).
- `rates.json` → the tier-2 prereg (v3.1 §9.2). N-h: the §8.4 pick form is copied verbatim into the tier-2 prereg.
- HB-CUS (R6 §I.5): its own run doc, after HB-T1's delete line and L-after, with `ACCEPT.json` known.
- κ Part III runs nothing before the κ-code read.
- One line `OPS-<MMDD>b-t1-handoff` citing the pulled sets, CAP.json, TRIM.json, ACCEPT.json, the amendments log sha,
  MAPF, parity run 2, every STOP / resume line, L-final and L-after.
- **Carried NON-BLOCKING items (CC-300 W6-W8), none a rental gate:**
  - W6: at the next validator edit, add fixtures for its unexercised checks `one_form`, `form_filled` and `ii_added`,
    or state in the readings hunk map why they are dominated (CC-300 Ruling 6 (e));
  - W7: the STATE file's B row is refreshed at the next STATE write (H_B, CC-295r4, CC-296r3, run doc v1.1 / v1.2 / v1.3,
    CC-300, CC-301, H_B′);
  - W8: CC-295r4 N-f′ (HM36 at the next b_pa1_mid.py change, with CC-296 Ruling 10 re-run), N-j (met here: §12.3 is
    written as a branch), N-k and N-m stay open as stated in CC-295r4.

## 17. Readings (v1 D-1..D-10 updated to the rulings; D-11..D-19)

| # | reading | status |
|---|---|---|
| D-1 | P-3 timing against "after C's machine is deleted" | **moot**: C's delete line and L-after exist (OPS-1108a-hc1-deleted, l.1867); Part II §2 step 1 holds as written |
| D-2 | L-before = B0 − Σ R_j | Σ R_j = 0 unless C-DIAG (or another rental) is live; each live rental named with its registered remaining capped spend (RB11, D-19). For the v1.2 reader |
| D-3 | ledger cross-check | registered form while B alone bills; with another rental, its delta subtracted (RB10). For the v1.2 reader |
| D-4 | money-stop threshold and cadence | CC-295 Ruling 11: sound in principle; code: `money-stop`, `next_read_h` (reading 20). Threshold 1.5 h × Σ r_live (RB9). For the v1.2 reader |
| D-5 | CPU floor PI-1107a over R6 §I.1's 5900X row | as S11 §5.2. For the v1.2 reader |
| D-6 | W set staged for features only; wiped; the host never gets the lists | accepted in substance: CC-295 Ruling 12 (custody), CC-295r3 Ruling 6 reading 1. The reader confirms |
| D-7 | GPU-h = step wall seconds | **decided**: CC-295 Ruling 9; readings 21, 30 |
| D-8 | step-4 additions | **decided**: PI-1108e Q2 (a); D-8 v1.3 GO (CC-296r3), pins l.1881-1882; (i) mid-run read at the irreversible tier; fallback PI-1108f Q2 |
| D-9 | ~~lazy weights~~ | **struck**: eager download (CC-295 Ruling 3; reading 5) |
| D-10 | host path set and subset SUMS | **decided**: CC-295 Ruling 12; reading 32 |
| D-11 | (i) cut-off = t_i0 + 5 h (RB14), leaving ≤ 1 h of the 6 h window for both amends, `final`, the pins, parity run 2, the h_input push and the launch | new; for the v1.2 reader |
| D-12 | HB-T1′'s S and SW count an open step to the later evidence stamp (more GPU-h used, the safe side of the cap); SW is the `w.` part of S, so SW ≤ S (CC-300 W2) | for the v1.2 reader |
| D-13 | per-mode snapshot verification; earlier manifests' `logs/` lines excluded at the final pull | new; for the v1.2 reader |
| D-14 | disk: the PI-1108f offer rule; a failed `--output=avail` ≥ 185 GB check is a FAULT machine (Part II §2 step 4, N-r2-f) | offer rule decided (PI-1108f default); FAULT classification for the v1.2 reader |
| D-15 | PA3 at parity run 2: the coordinator writes PA3.json on the host | new; for the v1.2 reader |
| D-16 | RH = the panel rate rounded up to a whole VND (C's `r_host_up`) | new; for the v1.2 reader |
| D-17 | HB-T1′ needs a one-judge read of a short machine-loss addendum, and no fresh PI line | **decided**: PI-1108i |
| D-18 | HB-T1′ restores the finished `w25_parts/part_*.npz` (never `.part_*`), so W resumes from existing parts; the §9.2 parity re-checks block 0 (§12.3 step 5) | new (CC-300 W3); for the v1.2 reader |
| D-19 | Σ R_j with a parallel C-DIAG: R_CD = 210,000 − S_CD (its M_D bound, C-DIAG v1.2 afbb61fb l.708-712); burn and T add C-DIAG's rate. B's real worst case for C-DIAG's own check = W_B + O_B (PI-1109c point 2; CC-299r2 R2-W8): W_B = max(0, 40 − h_B) × r_B, O_B = 7 × r_B + FEE (the rental line's) or 0 once B's resume is used or its block ended; logged on B's lbefore / rent lines. A planning reserve: B's binding check is §12.3 step 2 at RH′ + FEE′; on HB-T1′, h_B and r_B are its own billed hours and RH′ (CC-301r2 NB1) | B-side parts ACCEPTED by CC-301 Ruling 3; the reserve form per PI-1109c |

## 18. PI questions (each with a recommendation and a default; Vietnam time = UTC+7)

Answered or closed:
- PQ-B1, PQ-B2 and PQ-B3 by PI-1108d (PQ-B3 met early by OPS-1108d-topup);
- Q2 by PI-1108f;
- the disk question by PI-1108f's default;
- PQ-B4 by PI-1108h (laptop online 24/7, sleep and Windows Update off);
- PQ-B5 done as recommended (CC-300 GO 90, `H_B′` 6d674ced, OPS-1109b-p8-pin);
- PQ-B6 by PI-1108i (one HB-T1′ after a one-judge addendum read, no fresh PI line).

**No PI question.** Under PI-1109d only direction, money above the cap, a data licence or test look, and submission
go to the PI; nothing in this file is of those kinds. The C-DIAG parallel case is ruled by PI-1109a and PI-1109c, and
its money form is §5.1 / D-19.

## 19. Touches during drafting
- v1.1 (2026-11-08 about 14:15-15:30Z):
  - read the B prereg dir, LOG lines by targeted grep, CC-295 … CC-295r4 and CC-296 … CC-296r3, `B_GPU_READINGS.md`,
    the code at `H_B`, `P6_RECOMPUTE_2026-11-08.md` §6-§7, D-8 v1.3 and the rented-GPU skill;
  - tested, in `/tmp` or read-only: F-1 on a synthetic fixture, `pin_line` for the five C7 pins, the mapfinal /
    parity2-start forms, `balance-cadence`, and `bash -n`;
  - one targeted LOG grep then printed a Paper C S16 line. It was not read further and nothing here uses it.
- v1.2 (2026-11-08 about 17:33-19:00Z):
  - read CC-300 in full, the `git diff` of `scripts/b_pa1` against 6e17728, and `b_pa1_d8i_validate.py`;
  - LOG only by line number and by `pin_line` booleans (the P8 pin at l.1895); no LOG text was printed;
  - re-ran `bash -n` on every sh block and the NGRAM scan.
- v1.3 (2026-11-08, finished 2026-11-08T22:49Z):
  - read CC-301 in full, CC-299r2's R2-W8 lines, and the O_B / W_B rows of `C_DIAG_PREREG_DRAFT_v1_2.md` (same form);
  - LOG only by `grep -c`, line-number booleans (l.1184, l.1190, l.1191, l.1196, l.1334-1336, l.1896, l.1897) and
    `pin_line` booleans; no LOG text was printed;
  - read `b_pa1_job.sh` l.125-160 and `b_pa1_gpu.py` l.765-780 for W7; re-ran `bash -n` on every sh block and the
    pull loop, and the NGRAM scan.
- v1.4 (2026-11-08, finished 2026-11-08T23:13Z):
  - read CC-301r2 in full; booleans of `C_DIAG_PREREG_DRAFT_v1_2.md` afbb61fb l.708-712; read gpu l.500-520 (step
    names), l.707-765, l.777-837 and l.840-865 (rerun-safe steps), job l.112-124 for NB2;
  - CC-301r2 item 12 calls v1.3's gpu lines off by one. `git show 6d674ced:` with `awk NR` gives `def need` at l.770
    and the three `need()` calls at l.790, l.793 and l.810, so v1.3's numbers were right; NB2 removes that bullet;
  - re-ran `bash -n` on every sh block and the pull loop, P19's two greps, and the NGRAM scan.
- v1.5 (2026-11-09, finished 2026-11-09T03:45Z):
  - read CC-302 and CC-303 (their rulings and fixes), the `git diff 6d674ced -- scripts/b_pa1` (5 paths), job l.31-104,
    models l.425-444, gpu cap-init; shas of `~/bpa1_env.sh` and `~/bpa1_env_w.sh` and their variable names only;
  - LOG by OPS-id tokens and line-number booleans (l.1909-1925); no LOG text was printed;
  - tested the P8 F-4 form with `pin_line` on a scratch LOG in /tmp; re-ran `bash -n`, P19's greps and NGRAM.
- v1.6 (2026-11-09, finished 2026-11-09T04:44Z):
  - read job l.129-170 and gpu `cmd_resume` (the RUN marker and the one-resume path); env_2's sha only;
  - LOG by OPS-id tokens only (l.1926-1939); no LOG text was printed;
  - re-ran `bash -n` on every sh block and the pull loop, P19's greps and NGRAM. P26 itself was not run here.
- Never opened: a cache, caption, label, sealed file, test image, `c_datastores/`, `t2pool_*` or Paper C output file.
- No ssh, no rental, no commit, no LOG write.
