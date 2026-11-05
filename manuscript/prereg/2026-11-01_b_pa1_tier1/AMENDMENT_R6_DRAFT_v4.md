# B-PA1-T1 AMENDMENT R6 (3090 host, custody host, κ design): DRAFT v3, Parts I and III only, not approved

Status: **DRAFT v3, for the one-judge FULL read in round 3/3 (the last round), not adopted, not committed, licenses
nothing.** It answers CC-255r2 (round 2/3, NEXT_ROUND 83; `.session_backup/2026-10-13/decisions/CC-255r2.txt`, sha
`5fe7eea3`) and, through v2, CC-255 (round 1/3, NEXT_ROUND 80; sha `f012f5c8`). Kept unchanged: v2
(`AMENDMENT_R6_DRAFT_v2.md`, `4bfd5132`, 572 l.) and v1 (`AMENDMENT_R6_DRAFT.md`, `3b25457c`, 470 l.). **Part II (cap 22 → 28 GPU-h) is no longer in this file.** It is now
`AMENDMENT_R6_PART2_CAP_DRAFT_v2.md` (re-pinned to this file), a standalone irreversible amendment that cites this
file's Part I (CC-255 N112; CC-255r2 Ruling 6).

| part | content | tier and read | source of the tier |
|---|---|---|---|
| **I** | tier-1 host HB-T1 (E-10 restatement), custody host HB-CUS (D5), per-machine ledger with T_down, sequencing (PI-1105a), 3090 estimates at the registered 22 h cap | **reversible, one-judge FULL read, round 3/3, bar 85** | R5 E-10 (l.359-360); v3.1 l.272; PI-1103ae (LOG l.1440); CC-255 Ruling 2 |
| **III** | κ (D6): design-only registration and the preregistered Proposition 3 data check; nothing run | **reversible, same read, bar 85** | B_UPGRADE_PLAN §6 step 5; CC-255 Rulings 7-8 |

**Effect clause (CC-255 N112).** Each part binds only after:
- its own GO;
- a gatekeeper commit of this file;
- a LOG line `R6-<I|III> ADOPTED <CC id> <commit> <file sha>` that follows both and pins the commit and the file sha.

Part III does not depend on Part I. A GO on one part with a NEXT_ROUND on the other is committed only with the
NEXT_ROUND part marked "not adopted" in a new file version; the ADOPTED line then pins that version's sha.

Written 2026-11-05T05:09:16Z (`date -u`); v2 02:17:06Z. HEAD at drafting `cc90c96`. Planning text only: nothing was rented, run or
committed. Every estimate and every [proposal] is AI opinion, not evidence.

Amends (neither file is edited; this file governs where it conflicts, from its effect clause on):
- `PREREG_DRAFT_v3_1.md`, sha256 `e9b30ca7…66fb`, registered at commit `5ff00c9`;
- `AMENDMENT_R5_DRAFT_v1_2.md`, sha256 `9cb21917…5e85423`, registered at commit `3091bf6` (CC-224r3 GO 93).

Line numbers are those of the committed bytes. CC-255 Ruling 1 re-hashed both local files equal to their commits.

**Name.** "R6" is the B plan's name for this amendment (B_UPGRADE_PLAN §3.5). It is **not** registration item R6 of
v3.1 l.656 (the Objects365 annotation sha), which is unchanged.

Notation: [measured] = from a rates file or a LOG line; [assumed ×1.5] = the v3.1 §9.1 4090 assumption × 1.5, the
factor v3.1 l.487 itself uses between a 3090 and a 4090; [derived] = arithmetic on cited numbers; [proposal] = chosen here.

Sources:
- **PI-1104ag** (LOG l.1534):
  - D1+D2: run PA1 tier 1 after this amendment; the VJCS floor version is prepared and NOT submitted without a PI line;
  - D4: cap 28 h (Part II file);
  - D5: a separate custody 3090, cap 9 h, about 84k VND, named in R6;
  - D6: κ is B's method contribution.
- **PI-1105a** (l.1543, 2026-11-05T01:39:32Z): rent sequentially (C first, then B; one 3090 of the spec at a time),
  NO top-up for now; if the balance is short, B waits.
- **PI-1105c** (l.1550, 04:47:02Z): if C's spend leaves too little money for B's 28 h cap, B runs at the registered
  22 h cap (A3 and H NOT RUN) instead of waiting for a top-up. At 22 h it changes nothing in Part I; it answers Part
  II's P-3 (CC-255r2 N138).
- **PI-1105b** (l.1544, 01:40:24Z): the spent KTVIC test references may be reused as a dev set for the κ Proposition 3
  check (descriptive only, CPU, no new labels, labelled descriptive in the paper, never a confirmatory claim).
- **PI-1104ae** (l.1522); **PI-1104ad** (l.1521) and `manuscript/GPU_RENTAL_SPEC.md`.
- OPS-1102m8-deleted (l.1262); OPS-1103m1-deleted (l.1375, balance 798,488 VND, the latest balance line; nothing
  rented since); OPS-1031m1 (l.923, 9,282 VND/h, M1's 3090 rate, no newer 3090 rate in the repo); OPS-1102topup
  (l.1164, the per-instance "spent" form).
- `manuscript/directions/B_UPGRADE_PLAN_2026-11-04.md`, current sha `8f8cc1e8` (LOG OPS-1104b erratum; CC-255 N111).
- C's `AMENDMENT_HOST_3090_DRAFT.md` §1 and §4 (template for §I.1 and §I.4; not edited).
- CC-253 MB2 (per-host ledger) and MB3 (teardown reserve); CC-254 N93; CC-254r2 N98-N100; CC-255 N104-N114;
  CC-255r2 N130-N138.
- CC-209 Ruling 1, CC-213r3 P7, CC-217r3, CC-224, CC-224r2, CC-224r3, as R5 cites them.

## Tóm tắt cho PI (tiếng Việt)

- Phần I (một giám khảo, đảo ngược được, 85):
  - Máy tầng 1 HB-T1: một RTX 3090/3090 Ti đạt mọi trường của GPU_RENTAL_SPEC. Giá trị thật và r_host được ghi vào
    dòng LOG lúc thuê.
  - Máy custody HB-CUS (D5): trần 9 GPU-giờ, chỉ giữ UIT-ViIC 231 và KTVIC 558.
  - Theo PI-1105a, mỗi lúc chỉ một máy chạy: máy của C trước, rồi HB-T1, rồi HB-CUS. Không nạp thêm tiền. Thiếu tiền
    thì B chờ.
  - Sổ tiền tính theo từng máy (số "spent" trên panel). Mỗi máy giữ dự phòng tháo máy T_down = 1 giờ.
  - Ở trần 22 giờ chỉ chạy lõi. HB-T1 tốn khoảng 159 nghìn đ (tối đa khoảng 251 nghìn đ, chưa tính giờ chờ). HB-CUS
    tốn khoảng 100 nghìn đ (tối đa khoảng 130 nghìn đ).
  - Nếu C dùng 350 nghìn đ thì số dư đủ cho cả hai máy của B. Nếu C dùng 465 nghìn đ thì HB-CUS có thể phải chờ.
- Phần III (cùng lượt đọc): sửa thứ tự các bước của κ để Mệnh đề 1 đúng. Bước kiểm Mệnh đề 3 dùng tham chiếu KTVIC
  test đã dùng (PI-1105b), chỉ mô tả, không chạy gì bây giờ.
- Bản v3: nếu khối W quá 1,0 GPU-giờ thì đó là CAP STOP cuối cùng theo luật đã đăng ký. Không chuyển W sang laptop
  khi quá giờ; laptop chỉ dùng khi cài đặt hoặc kiểm tra thất bại.
- Trần 28 giờ nằm ở tệp riêng `AMENDMENT_R6_PART2_CAP_DRAFT_v2.md` (hội đồng đủ).

---

# Part I: hosts (reversible, one judge, 85)

## I.1 Host class and acceptance rule (as C's host amendment §1)

Host labels in repo files:
- **HB-T1**, the tier-1 host;
- **HB-T1′**, its one machine-loss re-rental (v3.1 l.519-520);
- **HB-CUS**, the custody host, and **HB-CUS′**, its one machine-loss re-rental;
- "laptop";
- "M1" and "M8", historical only.

No provider id, IP or port is written in the repo. The provider id appears only in the LOG rental line, as at l.923
and l.1109.

A rental is accepted only if the ckey.vn offer meets **every** field below. The offer value of each field goes into
the rental LOG line (§I.3) before any B file moves. If no offer meets every field, nothing is rented: the coordinator
tells the PI the closest offer and a recommendation (GPU_RENTAL_SPEC, "How to apply").

| field | required (GPU_RENTAL_SPEC) | offer value | setup check on the host, before any B file moves |
|---|---|---|---|
| GPU | 1 × NVIDIA RTX 3090 or RTX 3090 Ti, 24 GB; never a 4090, 5090 or RTX Pro (PI-1104ae) | recorded at rental | `nvidia-smi` name and total memory |
| CUDA | ≥ 12.4 | recorded at rental | driver-reported CUDA version |
| CPU | AMD Ryzen 9 5900X or better | recorded at rental | `lscpu` model name |
| RAM | ≥ 32 GB | recorded at rental | `free -g` total |
| disk | 200 GB, read/write ≥ 1000 MB/s | recorded at rental | `df` size; one timed sequential write and read of a 4 GB scratch file, then deleted |
| network | ≥ 400 Mbps | recorded at rental | not re-measured; the weight-download rate is logged |
| uptime | > 99% | recorded at rental | — |
| online time | the offer's maximum rental time ≥ 72 h (not hours paid) | recorded at rental | — |
| r_host | the offer's hourly price only (defined in §I.3 rule 0); the setup fee is a separate field | **recorded at rental**, with the setup fee | — |

A setup check that contradicts the offer is a FAULT. No B file moves, the coordinator logs it, and the machine is
deleted. Its per-instance spend is logged (§I.3) and is not part of any block's GPU-h.

## I.2 r_host

r_host is defined only in §I.3 rule 0 (CC-255r2 N132). This section only points there.

## I.3 Money ledger: the single home of r_host, block spend, T_down and the balance rule (CC-253 MB2/MB3; CC-255 N105)

**Single home.** For B, this section is the only definition of r_host, block spend, T_down and the balance rule.
§I.5, §I.6, H-6, H-16, H-47 and the Part II file cite it and do not restate it.

0. **r_host** = the offer's hourly price in VND per GPU-h, without the setup fee (CC-255r2 N132).
   - It is recorded once per machine, in that machine's rental LOG line, and never changed during the block.
   - The setup fee is a separate rental-line field. It is added once to L-before (rule 3).
   - B's caps are in **GPU-h** (v3.1 l.503 as R5 E-7; v3.1 l.266) and do not move with r_host. A dearer offer raises
     the money at the cap, and rule 3 decides whether the rental may start.
   - Planning figures use **9,282 VND/h** (M1, LOG l.923) and a setup fee of 0 [measured for M1, estimated for the
     new hosts; M8's fee was 30 VND, l.1109].
1. **Block spend** = the machine's own per-instance "spent" read on the ckey.vn panel (LOG l.1164 form), page
   reloaded, **immediately before the delete click**. After a delete the panel lists no instance (LOG l.1375). It
   includes setup, selftest, spec checks, idle time and teardown up to that read. The last minutes after the read are
   covered by the cross-check L-before − L-after, which is valid because only one machine bills at a time
   (CC-255r2 N133).
   - Balance lines are solvency checks only. Under PI-1105a only one machine bills at a time, so a balance difference
     is a valid cross-check but never the ledger figure.
2. **T_down (pinned now) = 1 h × r_host** for each machine (≈ 9,282 VND at the planning rate). It covers the final
   pull, the backup, the logged deletion (§I.4 item 4), the machine delete and L-after.
   - Teardown is outside the GPU-h cap and inside the block spend.
3. **Balance rule (L-before)**: balance ≥ (cap + 4 h setup + T_down + 2 h idle margin) × r_host + setup fee. This replaces v1's
   unnamed "+3 h", which was T_down + 2 h.
   - HB-T1 at 22 h: 29 × r_host ≈ 269,178 VND.
   - HB-CUS at 9 h: 16 × r_host ≈ 148,512 VND [derived].
   - If the balance is lower, nothing is rented and **B waits (PI-1105a; no top-up)**.
4. **Fail-closed money stop.** If, before CAP STOP, the balance falls to (T_down + 0.5 h, one backup cycle) × r_host
   (≈ 13,923 VND), the coordinator stops the job, pulls, logs the deletion and deletes the machine. This guards against
   a machine dying at balance 0 before its final pull. The stopped block is reported as stopped at that point,
   like a CAP STOP. There is no top-up and no resume for this cause.
5. **Lines**, each stamped by `date -u`:

| line | when | content |
|---|---|---|
| L-before | immediately before renting | balance; rule 3 |
| rental line `OPS-<MMDD>b-hb<t1\|cus>-rent` | at rental | the offer's id (LOG only), every §I.1 field value, r_host, the setup fee, L-before, "all GPU_RENTAL_SPEC fields met", and the LOG line of the previous machine's delete (§I.5) |
| L-S | HB-T1 only, at the end of block S with the trim decision | balance and the per-instance spent so far |
| delete line + L-after | spent read immediately before the delete click; L-after read after it | per-instance spent (= block spend, rule 1), L-after, and the cross-check L-before − L-after |

6. **"At most" figures** in this file (§I.6, H-6, H-16) are GPU-h cap + setup + T_down. They **exclude idle time**,
   which is billed and is bounded only by the delete-when-idle rule (PI-1031c: delete when idle > setup time).

## I.4 Single tenancy, isolated tmpfs, logged deletion (C's §4 clauses, applied to B)

For each of HB-T1, HB-T1′, HB-CUS and HB-CUS′:

1. **One tenant.** From rental to delete, the host holds only B's job and B's files for its own block. No other
   paper's job, file or account touches it while any B image is on it.
   - HB-T1 and HB-CUS are **never the same machine** (PQ-3), and never live at the same time (§I.5).
   - HB-T1 holds only the Objects365 slice frame (v3.1 l.263; R5 E-1, E-12). HB-CUS holds only UIT-ViIC test 231 and
     KTVIC test 558 (v3.1 l.261).
   - After the logged deletion of B's files the machine is deleted. Reuse by another paper is not foreseen under
     PI-1105a.
2. **Images only in tmpfs.**
   - Every B image goes only to `/dev/shm/b_pa1_hb/` (mode 0700), never to disk. Weights and code may sit on disk.
   - On HB-CUS, the KTVIC reference text read by the custody score runs (v3.1 l.264-266) also sits only in that folder.
   - Images are pushed from the laptop's copies over the SSH channel. Each file is sha256-checked on arrival against
     the run manifest; a mismatch is a FAULT. No third-party storage is used.
   - A UIT-ViIC 231 image that the laptop does not hold is fetched on HB-CUS per file, by id only, from the public
     COCO archive, never the zip. This is the R5 E-13 fetch-delete-log pattern, extended to HB-CUS by H-45. Otherwise
     that image's row is NOT RUN.
   - Size [est.]: HB-T1 ≤ 4 GB for the frame (blocks of 500 to 4,000 survivors, v3.1 l.282-283); HB-CUS ≤ 1 GB for 789
     images. Both fit inside ≥ 32 GB RAM.
3. **Logs hold ids only.** Per-image logs and prompt dumps hold image ids only, never caption or reference text.
4. **Logged deletion.**
   - After the final pull, the run script deletes `/dev/shm/b_pa1_hb/`.
   - It appends (utc, folder, file count, manifest count) to `b_pa1_hb_deletions.log`, which is pulled to the laptop.
   - A trap deletes the folder on any exit.
   - The coordinator writes the deletion LOG line, deletes the machine through the panel, and writes the delete line
     and L-after (§I.3).
5. **Backups.** The 30-minute `gpu_backup` loop pulls outputs and logs, never `/dev/shm`. Its script is checked once
   for the absence of `/dev/shm` paths before the first image moves.
6. **Procedural isolation, disclosed.** The provider has root on the host, so the isolation is procedural, not an OS
   boundary.
   - HB-T1 holds Objects365 train images only. HB-CUS holds the two spent custody sets only.
   - No unspent test set and none of the never-on-a-rental sets of v3.1 l.286-287 goes to either host.
   - M1 was itself a rented 3090 with provider root (l.923), so HB-CUS is no weaker than the host it replaces.

## I.5 Custody host HB-CUS (D5) and the one-machine sequence (PI-1105a; CC-255 N104, N110)

- **Role.** HB-CUS is the "PI-named custody host" of v3.1 l.272 (CC-213r3 P7; PI-1104ag D5). It runs only the
  registered custody block of v3.1 l.264-268: the 4 accepted captioners decode UIT-ViIC 231 and KTVIC 558, and B's
  score runs on one KTVIC reference per image, untransformed and under the 6 PA2 transforms. Descriptive rows only.
- **Narrowing of CC-209 Ruling 1 (N110).** HB-CUS narrows CC-209 Ruling 1 (spent test images only on M1) to HB-CUS,
  for UIT-ViIC 231 and KTVIC 558 only, under CC-213r3 P7 and PI-1104ag D5. Every other test-role set keeps the
  registered rule (laptop only, now that M1 is deleted).
- **Not a recompute host.** No W25 feature is computed on HB-CUS. Any remaining recompute stays on the laptop CPU under
  R5 §A.5 (M1's E-13 slot is spent: OPS-1103b-w25slot-done, l.1316).
- **Cap.** Unchanged from v3.1 l.266: hard cap 9 GPU-h, per-step `timeout`, final CAP STOP. Setup and T_down are
  outside the cap and inside the ledger (§I.3) [PQ-2].
- **Sequence: one B or C 3090 live at any time (PI-1105a).**
  1. C's tier-1 machine first. **HB-T1 is rented only after C's machine is deleted and C's delete line and L-after are
     logged.** If C's block is not ready, this ordering still holds (PI-1105a: "C first, then B"). A change needs a PI
     line.
  2. **HB-CUS is rented only after HB-T1 is deleted, with its delete line and L-after logged**, and after block S's
     accepted-captioner list exists (v3.1 l.74).
  3. Each rental passes its own L-before (§I.3 rule 3), or B waits (PI-1105a).
  4. A machine-loss re-rental (HB-T1′, HB-CUS′) is the same machine slot. It also starts only after the lost machine
     is confirmed gone on the panel.
- **If HB-CUS never runs** (no offer meets the spec, the balance rule fails, or HB-CUS′ is lost too): the custody rows
  are NOT RUN; no PA3 fires; nothing else in tier 1 waits for them (v3.1 l.271-272, unchanged in effect).

## I.6 3090 estimates at the registered cap of 22 GPU-h

Per-caption costs on HB-T1:
- decode 0.8409 s [measured on a 3090, short mode, `rates.json`, v3.1 l.487];
- decomposition r_e 0.9 s, verification p·r_v 5 × 0.3 s, judge r_j 0.375 s, CLIPScore 0.015 s [assumed ×1.5];
- scoring 2.79 s; per A1 caption 3.63 s (4090: 2.42 s).

The true factor for batch-1 bf16 decoding may be nearer 1.2 (936 vs 1008 GB/s; C host draft §6). Block S measures the
rates, and the trim rule always uses the measured rates.

**Block W is not scaled (CC-255 N106 (g)).** Block W runs SSCD and pHash/dHash on the host CPU (R5 §D.2 l.450), so
the GPU factor has no basis for it. Its registered estimate and block cap stay **1.0 GPU-h** (v3.1 l.492; R5 l.458).
The GPU-hosted blocks S to A4 are scaled.

**A W timeout is a final CAP STOP (CC-255r2 N130, option (i)).**
- The registered rule (v3.1 l.503-504, kept by R5 §D.3 l.473) says "per-step `timeout` for the time left; a timeout
  is a final CAP STOP".
- Block W's per-step `timeout` is its block cap of **1.0 GPU-h** (R5 l.458). This is less than the time left of the
  22 h, so it is the binding bound. A W step that reaches it is a final CAP STOP for tier 1, as registered.
- The R5 §D.2 laptop fallback (l.453-455) covers only "a failed install or check", an operator FAULT. It **never**
  covers a timeout. v2's sentence linking the two is withdrawn.
- No rule changes. W's 1.0 h is a 4090-era estimate for CPU work; on a CPU of the GPU_RENTAL_SPEC class (Ryzen 9
  5900X or better) it is not expected to bind [est.], and nothing here relies on that.

| order | block | 4090 GPU-h (v3.1 l.491-497) | HB-T1 GPU-h | cumulative | at 22 h, assumed rates |
|---|---|---|---|---|---|
| 1 | W | 1.0 | 1.0 (CPU, not scaled) | 1.0 | runs |
| 2 | S | 0.9 | 1.35 [assumed ×1.5] | 2.35 | runs; trim rule applied at its end |
| 3 | A1 | 5.4 | 8.1 | 10.45 | runs (core) |
| 4 | A2 | 1.1 | 1.65 | 12.1 | runs (core) |
| — | E1, E2 | — | — | — | NOT RUN (R5 E-12) |
| 5 | A3 | 5.8 | 8.7 | 20.8 | trimmed unless rates ≥ 14.8% below assumed |
| 6 | H | 0.6 | 0.9 | 21.7 | trimmed unless rates ≥ 18.8% below assumed |
| 7 | A4 | 4.0 | 6.0 | 27.7 | trimmed unless rates ≥ 38.0% below assumed |

Trim arithmetic at 22 h [derived; the criterion of v3.1 l.510-511 is unchanged]:
- After W + S: 22 − 2.35 = 19.65 h remain.
- With A4: (8.1 + 1.65 + 8.7 + 0.9 + 6.0) × 1.25 = 25.35 × 1.25 = 31.69 > 19.65. A4 drops.
- A1 + A2 + A3 + H = 19.35 × 1.25 = 24.19 > 19.65. H drops.
- A1 + A2 + A3 = 18.45 × 1.25 = 23.06 > 19.65. A3 drops.
- A1 + A2 = 9.75 × 1.25 = 12.19 ≤ 19.65. **A4, H and A3 NOT RUN; (d1,v1) frozen (v3.1 §7.2).**
- Thresholds: 19.65 / 23.0625 = 0.852; 19.65 / 24.1875 = 0.812; 19.65 / 31.6875 = 0.620.
- Core W + S + A1 + A2 = 12.1 h, 15.125 h with +25%, inside 22 h, so the core is never trimmed (R5 E-12).

Money [derived, 9,282 VND/h; definitions in §I.3]:

| machine | expected (blocks + setup 4 + T_down 1) | at most (cap + setup + T_down, excluding idle, §I.3 rule 6) | L-before |
|---|---|---|---|
| HB-T1 (22 h) | 12.1 + 5 = 17.1 h ≈ 158,722 | 27 h ≈ 250,614 | 269,178 |
| HB-CUS (9 h) | 5.8 + 5 = 10.8 h ≈ 100,246 | 14 h ≈ 129,948 (of which the 9 h cap part 83,538, the "about 84k" of D5) | 148,512 |

**Balance under PI-1105a** (from 798,488, l.1375; C's figure is C's whole block spend, T_down included, C host v3 l.103-106 at 5d6f5ca; nothing more is subtracted):
- **C at 350,000:** 448,488 is left.
  - HB-T1 passes L-before (269,178).
  - After HB-T1's expected spend, 289,766 is left; after its maximum, 197,874. HB-CUS passes either way (148,512).
- **C at 465,000 (PQ-C2):** 333,488 is left.
  - HB-T1 passes.
  - After HB-T1's expected spend, 174,766 is left, and HB-CUS passes.
  - After HB-T1's maximum, 82,874 is left, and **HB-CUS waits**.

## I.7 Order, timing and licence

- **Order:** C's machine, deleted → HB-T1 runs W → S → A1 → A2 (→ A3, H, A4 as the trim rule allows), the registered
  order (v3.1 l.508 as R5 E-12), deleted → HB-CUS (§I.5).
- **Timing:** B tier 1 never takes A's 15-30/11 writing turn (v3.1 l.521, unchanged). Under PI-1105a, HB-T1 starts
  when C's machine is gone (PQ-5).
- **Licence after Part I is adopted.** Part I does not license a rental by itself. HB-T1 is rented only after all of:
  - the R6-I ADOPTED line;
  - P6: the laptop recomputes #15-#17 and #22 (no done line in the LOG at drafting);
  - P9: venv freezes, model pins and prompt shas (R5 l.443);
  - C's delete line (§I.5);
  - an L-before that meets §I.3;
  - a launch line citing this file's sha.
- **Precondition status** (R5 §D.1; B_UPGRADE_PLAN §3.2):

| status | preconditions |
|---|---|
| met | P1 (3091bf6); P2 at text level (each rental logs its own balance); P3 (`284b5d03`); P4; P8 (CC-226r3); P10 (map `497b430a`; parity run 1 as logged at l.1336) |
| met for the M1 slot | P6 (l.1316-1319); the laptop recomputes are still open |
| replaced by §I.4 | P7 |
| open | P9 |

## I.8 Registered lines changed by Part I (old → new)

H-1 … H-37 keep v1's numbers; new rows are H-38 … H-53.
- † = changed against v1 in v2, in numbers or substance.
- H-2, H-10, H-15, H-18, H-20, H-22 and H-27 also changed against v1 in v2, as wording follow-ons of V2-2 and V2-10
  (CC-255r2 N134). They are left unmarked.
- ‡ = changed in v3.

| # | where (commit) | old (quoted) | new |
|---|---|---|---|
| H-1 | v3.1 l.484 (5ff00c9) | "### 9.1 Tier-1 blocks on one named RTX 4090" | "### 9.1 Tier-1 blocks on one named RTX 3090 / 3090 Ti (HB-T1, R6 Part I)" |
| H-2 | R5 E-10 l.357-360 (3091bf6), restating v3.1 l.485-487 | "l.485-487: the host is **the ckey instance named in the launch LOG line** (instance 111947, alias M8, at drafting), RTX 4090, **17,499 VND/h** plus a 30 VND setup fee (LOG l.1109); maximum rental to 2026-11-15T14:20Z (LOG l.1109). No host name, IP or port. A host substitution needs a new E-10 restatement and a one-judge diff read before any B step on the new host." | "l.485-487: the host is **HB-T1**, one RTX 3090 or 3090 Ti accepted under R6 §I.1, named by its rental LOG line, with r_host and the setup fee recorded there (R6 §I.2-§I.3). M8 was deleted (LOG l.1262). No host name, IP or port in the repo. A further substitution, other than the one machine-loss re-rental HB-T1′ under R6 §I.1, needs a new E-10 restatement and a one-judge diff read before any B step on the new host." |
| H-3 | v3.1 l.486-488 | "(17,513 VND/h below is M5's past rate) … Assumed per-caption costs on a 4090, to be measured in block S: decode 0.56 s (3090 short-mode 0.8409 s / 1.5, an assumption), decomposition r_e 0.6 s, verification p·r_v = 5 × 0.2 s, judge r_j 0.25 s, CLIPScore 0.01 s; pipeline ≈ 1.86 s." | "(planning rate 9,282 VND/h, M1's 3090 rate, LOG l.923; r_host per R6 §I.3) … Assumed per-caption costs on the 3090, to be measured in block S: decode 0.8409 s (measured, short mode), decomposition r_e 0.9 s, verification p·r_v = 5 × 0.3 s, judge r_j 0.375 s, CLIPScore 0.015 s (4090 assumptions × 1.5); scoring ≈ 2.79 s." |
| H-4 † | v3.1 l.491-497 GPU-h column; total row l.501 as R5 E-12 ("18.8 (+25% = 23.5)") | "1.0 / 0.9 / 5.4 / 1.1 / 5.8 / 0.6 / 4.0"; "18.8 (+25% = 23.5)" | "1.0 (W, CPU, not scaled) / 1.35 / 8.1 / 1.65 / 8.7 / 0.9 / 6.0"; "27.7 (+25% = 34.625)" (R6 §I.6) |
| H-5 † | R5 E-12 l.365-366 | "The core W + S + A1 + A2 ≈ 8.4 h (10.5 h with +25%) is never trimmed" | "The core W + S + A1 + A2 ≈ 12.1 h on HB-T1 (15.125 h with +25%) is never trimmed" |
| H-6 † | R5 E-7 l.339-347, the restated v3.1 l.511-516 (this covers l.513 and l.515, which name 17,513 VND/h and the 4090) | "At the assumed rates the trim rule drops A4 (after S: 22 − 1.0 − 0.9 = 20.1 h remain; … about 329,000 VND at M8's 17,499 VND/h, and at most (22 + 4) × 17,499 ≈ 455,000 VND at the cap. With W + S taking 1.9 h as assumed, H runs only if block-S rates are at most 24.6% above the assumed ones, A3 runs up to 30.7% above, and A4 runs only if they are at least 4.9% below; …" | "At the assumed 3090 rates the trim rule drops A4, H and A3 (after S: 22 − 1.0 − 1.35 = 19.65 h remain; A1 + A2 + A3 = 18.45 h, × 1.25 = 23.06 > 19.65; A1 + A2 = 9.75 h, × 1.25 = 12.19 ≤ 19.65). The expected spend is W + S + A1 + A2 = 12.1 GPU-h plus setup and T_down (R6 §I.3), about 159,000 VND at 9,282 VND/h; at most about 251,000 VND (cap + setup + T_down, excluding idle; R6 §I.3 rule 6). With W + S taking 2.35 h as assumed, A3 runs only if block-S rates are at least 14.8% below the assumed ones, H at least 18.8% below, A4 at least 38.0% below; the rule itself always uses the measured remaining cap after S." The l.510-511 criterion stays in force |
| H-7 † | R5 §D.3 l.460-474 | the table "1.0 … 14.8" and "Expected 14.8 GPU-h + 4 h setup [derived]" | the R6 §I.6 table and "Expected 12.1 GPU-h + 4 h setup + T_down [derived; R6 §I.3]" |
| H-8 | v3.1 l.229 (host column, slice A) | "named rented RTX 4090" | "HB-T1 (R6)" |
| H-9 † | v3.1 l.263 | "The rented 4090 holds no other images." and "Only the id survivors and the Objects365 slice frame go to the 4090, for C1-C3 features." | "HB-T1 holds no other images (R6 §I.4)." and "Only the Objects365 slice frame goes to HB-T1, for C1-C3 features (no id survivors exist under R5 E-12)." The rest of the line is unchanged |
| H-10 | v3.1 l.259 | "### 5.3 Custody and the M1 block (W12; CC-209 r1(a); B3)" | "### 5.3 Custody and the custody block on HB-CUS (W12; CC-209 r1(a) as narrowed by R6 §I.5; B3)" |
| H-11 | v3.1 l.261 | "UIT-ViIC test 231 and KTVIC test 558 never leave M1 or the laptop." | "UIT-ViIC test 231 and KTVIC test 558 never leave the laptop or HB-CUS (R6 §I.4-§I.5)." |
| H-12 | v3.1 l.230-231 (host column) | "M1 only for decodes (§5.3)" / "M1 only for decodes" | "HB-CUS only for decodes (§5.3, R6)" |
| H-13 | v3.1 l.264 | "**M1 block (descriptive custody rows):**" | "**Custody block on HB-CUS (descriptive custody rows):**" (content and the 5.8 h estimate unchanged) |
| H-14 † | v3.1 l.269-270 | "**Slot:** only after MT4 releases M1, never while an MT4 K1+K6 job is live or queued on M1, and it never delays MT4 tier 2 or tier 3 (CC-215 B8, CC-216, PI-1101q)." | "**Slot:** HB-CUS is rented only after HB-T1 is deleted (delete line and L-after logged) and block S's accepted-captioner list exists, with its own L-before; one B or C 3090 live at any time (PI-1105a; R6 §I.5)." |
| H-15 | v3.1 l.271-272 | "**If M1 lapses or is never free:** these rows are reported NOT RUN; … A PI-named custody host is the only alternative (CC-213r3 P7; default: wait)." | "**If HB-CUS never runs (no offer, the balance rule fails, or HB-CUS′ is lost too):** these rows are reported NOT RUN; no PA3 fires from that; nothing else in tier 1 waits for them. HB-CUS is the PI-named custody host (PI-1104ag D5; R6 §I.5)." |
| H-16 † | v3.1 l.517-518 and R5 §D.3 l.478-479 | "M1 block (custody rows, §5.3): about 5.8 h (W9), **hard cap 9 GPU-h** at M1's 9,282 VND/h (≈ 54,000 VND expected, ≤ 84,000 VND at the cap), only after MT4 releases M1." / "M1 (separate host, unchanged): the custody decode block, about 5.8 h, hard cap 9 GPU-h at 9,282 VND/h, only after MT4 releases M1 (…), preceded by the §A.5 W25 slot." | "Custody block on HB-CUS (§5.3): about 5.8 h (W9), **hard cap 9 GPU-h** at r_host (≈ 54,000 VND for the 5.8 h and ≤ 84,000 VND for the 9 h cap at 9,282 VND/h; setup, T_down and idle are extra, R6 §I.3), rented after HB-T1 is deleted (R6 §I.5)." |
| H-17 | v3.1 l.285-286 | "recomputed on the host that already holds that set under its custody rule (M1, or the laptop CPU where allowed; never the laptop for A-T3 val2017), never on a rented host" | "… (the laptop CPU where allowed; M1 is deleted, LOG l.1375, and its E-13 slot is spent, l.1316; HB-CUS is not a recompute host; never the laptop for A-T3 val2017), never on a rented host" |
| H-18 | v3.1 l.288 (first sentence) | "Custody-set features (UIT-ViIC 231, KTVIC 558): laptop CPU or M1 under §5.3." | "Custody-set features (UIT-ViIC 231, KTVIC 558): laptop CPU under §5.3." |
| H-19 | v3.1 l.526 | "Measured on the named 4090 at the end of tier 1" | "Measured on HB-T1 at the end of tier 1" |
| H-20 | v3.1 l.529 | "**PI trigger:** P3 > 150 GPU-h (4090) → the PI decides" | "**PI trigger:** P3 > 150 GPU-h on the named host (number unchanged; on a 3090 this is stricter, ≈ 100 4090-h) → the PI decides" (CC-255 Ruling 4) |
| H-21 | v3.1 l.533 | "ckey balance in hours of the named 4090" | "ckey balance in hours of the named tier-3 host" |
| H-22 | v3.1 l.564 | "machine loss, M1 busy or M1 lapsed \| never a trigger" | "machine loss, HB-T1 or HB-CUS lost, no offer meeting GPU_RENTAL_SPEC, or B waiting under PI-1105a \| never a trigger" |
| H-23 † | v3.1 l.521-522 | "B's 4090 rentals are staggered with C tier 3 and VSPS-J E2b on the dedicated 4090 (PI-1101r)." | "B's HB-T1 and HB-CUS are rented one at a time, after C's machine is deleted, single-tenant (PI-1105a; R6 §I.4-§I.5)." The A-turn sentence is unchanged |
| H-24 | R5 l.23 (header licence) | "No 4090 step until P3, P4 and P6-P10 are met (P2 is met, §D.1)." | "No HB-T1 step until P3, P4, P6 and P8-P10 are met and R6 Part I is adopted; P7 is replaced by R6 §I.4." |
| H-25 | R5 P7 l.441 | "M8 hand-over: single tenant; no image on M8 other than B's Objects365 frame (v3.1 l.263). E2b's 769 images … deleted, deletion logged, before any B image is staged" | "HB-T1 single tenancy, tmpfs and logged deletion per R6 §I.4 (M8 deleted, LOG l.1262)." |
| H-26 | R5 §D.2 l.446-456 | "### D.2 Block W on M8, first" … "n = 50 frame images featured on M8 and on the laptop" … "M8 has Python 3.12.3 only" … "Only feature files leave M8" | "### D.2 Block W on HB-T1, first" … "on HB-T1 and on the laptop" … "HB-T1's Python version is recorded at setup; a failed install or check is an operator FAULT, fallback as written" … "Only feature files leave HB-T1" |
| H-27 | R5 §D.4 l.481-501 | "### D.4 Host and order on M8 [proposal; non-binding …]" (items 1-6) | struck as moot (M8 deleted; E2b and C have their own hosts). Order and timing: R6 §I.5, §I.7 |
| H-28 ‡ | v3.1 l.7-8 | "No 4090 step, block W included, runs before the R5 launch amendment" | "No HB-T1 step, block W included, runs before the R5 launch amendment and R6 Part I". The rest of l.8-9 is unchanged; its "logged PI top-up" clause is met by PI-1102b (R5 P2 l.436), and no new top-up is made (PI-1105a) |
| H-29 | v3.1 l.69 | "**Needs the 4090 (dedicated per PI-1101r) and, before its first step, the R5 amendment" | "**Needs HB-T1 (R6 §I.1, single tenant per §I.4) and, before its first step, the R5 amendment and R6 Part I" |
| H-30 | v3.1 l.73-74 | "**Needs M1 after MT4 releases it (§5.3):** … which happens in block S on the 4090." | "**Needs HB-CUS (§5.3, R6 §I.5):** … which happens in block S on HB-T1." |
| H-31 | v3.1 l.216-217 | "on the 4090, always. The gate never depends on M1 (B3c holds whether M1 is busy or gone)" | "on HB-T1, always. The gate never depends on HB-CUS (B3c holds whether HB-CUS is rented or not)" |
| H-32 | v3.1 l.241-242 | "one descriptive row (M1 block; NOT RUN if M1 is never free)" / "in the one M1 block (§5.3)" | "one descriptive row (custody block on HB-CUS; NOT RUN if HB-CUS never runs)" / "in the one custody block on HB-CUS (§5.3)" |
| H-33 | v3.1 l.361 and l.460 | "from the M1 block" / "the KTVIC row of the M1 block" | "from the custody block on HB-CUS" / "the KTVIC row of the custody block on HB-CUS" |
| H-34 | v3.1 l.459 | "≈ 5.3 h on a 4090 at the assumed rates" | "≈ 5.3 h on a 4090 at the assumed rates (≈ 8.0 h on a 3090 [assumed ×1.5])" |
| H-35 | v3.1 l.619 and l.638 | "one descriptive row in the M1 block (§5.1)" / "captions as a descriptive second row only from M1" | "one descriptive row in the custody block on HB-CUS (§5.1)" / "captions as a descriptive second row only from HB-CUS" |
| H-36 | v3.1 l.620 | "v3 P10 novelty rescan before any 4090 spend" | "v3 P10 novelty rescan before any HB-T1 spend" (met: N18_RESCAN `284b5d03`) |
| H-37 | v3.1 l.646 | "on the 4090, never UIT-ViIC 231 on M1" | "on HB-T1, never UIT-ViIC 231 on HB-CUS" |
| H-38 | v3.1 l.282 (N106 a) | "**Compute (N8):** block W on the named 4090, first after setup" | "**Compute (N8):** block W on HB-T1 (host CPU, R5 §D.2), first after setup" |
| H-39 | v3.1 l.288 (mirror of l.263; N106 b) | "Only the id survivors and the Objects365 slice frame go to the 4090, for C1-C3 features." | "Only the Objects365 slice frame goes to HB-T1, for C1-C3 features (no id survivors exist under R5 E-12)." |
| H-40 | R5 E-1 l.320 (N106 c) | "Slice B images go to the 4090 for W25 features only; they are never decoded or scored in tier 1." | "Slice B images go to HB-T1 for W25 features only; they are never decoded or scored in tier 1." |
| H-41 | v3.1 l.522-523 (N106 d) | "No B 4090 step, block W included, before the commit, the R5 amendment with its one-judge read, a logged PI top-up and the N18 novelty rescan (CC-217r2 Ruling 4)." | "No B HB-T1 step, block W included, before the commit, the R5 amendment, R6 Part I adopted, an L-before that meets R6 §I.3 (no top-up under PI-1105a) and the N18 novelty rescan (CC-217r2 Ruling 4; P2 met by PI-1102b)." |
| H-42 | R5 l.15 (N106 e) | "and M8 receives only the Objects365 frame." | "and HB-T1 receives only the Objects365 frame (R6 §I.4)." |
| H-43 | R5 l.474-475 (N106 e) | "Setup on M8 may be shorter than 4 h because M8 is already set up (LOG l.1109); the planning number stays 4 h [proposal]." | "Setup on HB-T1 is planned at 4 h (a fresh rental); setup is outside the GPU-h cap and inside the R6 §I.3 ledger." |
| H-44 | R5 §A.1 l.99-102 (N106 f) | "Objects365 slice frame may reach the 4090 (…)" / "In this amendment a "rental" is any host other than the custody host M1 (M1 is itself rented; CC-224r2 N5)." | "Objects365 slice frame may reach HB-T1 (…)" / "In this amendment a "rental" is any host other than the laptop. M1 is deleted (LOG l.1375). HB-T1 and HB-CUS are rentals. HB-CUS may hold only UIT-ViIC 231 and KTVIC 558, under R6 §I.4-§I.5; every other "never on a rental" rule binds both hosts." |
| H-45 | R5 E-13 l.406-410 (N106 f) | "are featured on M1 only. … the images are fetched on M1 from the public COCO archive … Never on a rental (any host other than the custody host M1), and never on the laptop for A-T3 val2017 (l.285-286). The M1 slot rule of §5.3 (l.269-270) applies." | Kept as the record of the spent M1 slot (l.1316). Added: "The per-file public-COCO fetch, delete and log pattern of this erratum is extended to HB-CUS for UIT-ViIC 231 images only, for the custody decodes (R6 §I.4 item 2); no feature recompute runs on HB-CUS." |
| H-46 ‡ | R5 §D.2 l.458 (N106 g) | "Cap 1.0 GPU-h (v3.1 l.492) inside the 22 h." | unchanged; restated for HB-T1: block W is host-CPU work, estimate and cap 1.0 GPU-h, not scaled. The cap is W's per-step `timeout`; a W timeout is a final CAP STOP (v3.1 l.503-504; R5 l.473); the R5 §D.2 laptop fallback covers only a failed install or check (R6 §I.6). No cap number and no rule changes |
| H-47 | v3.1 l.535-537 (N105 d) | "**PI-1101q** (…): ordinary GPU launches need not be covered by the balance for the whole chain. This stricter full-balance gate is kept **on purpose, for the irreversible one look only** (CC-213r3 Ruling 4, P4 default); tier 1 and tier 2 follow PI-1101q." | "… tier 2 follows PI-1101q; tier 1 on HB-T1 and HB-CUS follows the R6 §I.3 balance rule (L-before per machine) and PI-1105a (one machine at a time, no top-up, B waits)." The tier-3 full-balance gate is unchanged |
| H-48 | R5 E-7 l.350 (N105 d) | "The M8 idle bill while S and A1 wait (§D.4) is not in these figures." | "Idle time on HB-T1 or HB-CUS is billed inside the per-machine block spend (R6 §I.3 rule 1) and is not in the "at most" figures (rule 6); the delete-when-idle rule bounds it." |
| H-49 ‡ | R5 l.29 | "**Why R5 exists.** No 4090 step, block W included, runs before this amendment is adopted" | "… No HB-T1 step, block W included, runs before this amendment and R6 Part I are adopted". The rest of l.29-30 is unchanged; its "logged PI top-up" clause is met by PI-1102b (R5 P2 l.436), and no new top-up is made (PI-1105a) |
| H-50 | R5 E-12 l.379 | "the 4090 list reads "block W, every slice-A block, the Vietnamese gate (§4.4)"" | "the HB-T1 list reads "block W, every slice-A block, the Vietnamese gate (§4.4)"" |
| H-51 | R5 E-12 l.386-387 | "only the Objects365 slice frame goes to the 4090." | "only the Objects365 slice frame goes to HB-T1." |
| H-52 | R5 l.429 | "## D. The 4090 block plan (route 1b)" | "## D. The HB-T1 block plan (route 1b; R6 Part I)" |
| H-53 | R5 l.465 (§D.3 row S, "held by" column) | "G3: the header licence line for recomputes, then the M1 W25 slot (P6) and the #22 laptop recompute" | "G3: the header licence line for recomputes and the #22 laptop recompute (the M1 W25 slot is done, LOG l.1316)" |

**Kept, not changed** (each still true as a record, or moot). This list and H-1 … H-53 together cover every line of
v3.1 and R5 that names the 4090, M1 or M8 (`grep -nP '4090|\bM1\b|\bM8\b'` on both committed files):
- **v3.1**
  - l.19, l.21, l.29, l.51: closure rows quoting past rulings.
  - l.65: "No GPU, no M1" describes laptop T1a and is still true.
  - l.232-233: Composite-COCO and Polaris, moot under R5 E-12.
  - l.273 (N113): "The parity gate never needs M1"; true, and the gate is met (l.1336).
  - l.626 and l.656: citations of PI-1101r and of the registered file name.
  - l.648: the Q-a record; its status changes only by the Part II file.
  - l.283 ‡: the phrase "and the id survivors of Composite-COCO and Polaris-test-COCO" is moot under R5 E-12, as H-9
    and H-39 say (CC-255r2 N136).
- **R5, records**
  - l.23 ‡, second sentence ("No M1 slot until Q2 and the MT4 hand-over."): spent (l.1316) (CC-255r2 N136).
  - l.1: the title of a registered file.
  - l.26, l.436, l.440: the M1 slot clauses, spent (l.1316).
  - l.56-59, l.74, l.76, l.84: v1.1 and v1.2 change tables.
  - l.117: a cache path at its historical location.
  - l.141-142, l.178-199, l.225-226, l.237, l.240, l.242: M1-slot feature sources, spent (l.1316-1319); #25 was lost
    with M1 on 10-29.
  - l.292: the ADE20K record.
  - l.342: inside the E-7 span replaced by H-6.
  - l.536 and l.547: §E, N18, met by P3.
  - l.568-665: closure tables, review items and PI questions, all answered records.
- **Money lines ‡** (`grep -nP 'top-up|balance|VND|PI-1101q'` on both committed files; CC-255r2 N137). None conflicts
  with PI-1105a:
  - v3.1 l.8, l.21, l.70, l.523 and R5 l.29, l.568, l.575, l.659 read a top-up that already exists (PI-1102b, LOG
    l.1163-1164);
  - v3.1 l.529, l.533 and l.563 are tier 3 and unchanged (H-21 relabels l.533);
  - v3.1 l.486 and l.513-518 are covered by H-3, H-6 and H-16;
  - R5 l.342-348 and l.358 are covered by H-6 and H-2;
  - R5 l.492-499 is §D.4, struck by H-27.

Unchanged by Part I: every set role; the trim criterion (v3.1 l.510-511); the 22 GPU-h tier-1 cap; the custody cap of
9 GPU-h; block W's 1.0 GPU-h; the one-resume rule (l.519-520); the never-on-a-rental list (l.286-287); W25 (§5.4); the
run order; the tier-3 full-balance gate.

---

# Part III: κ, design-only registration (reversible, one-judge read, 85)

**Additive.** Part III changes no registered line. It does not touch map v1 (`497b430a`), block H or H2 (v3.1 §8.4),
any tier-1 block, any PA3 trigger or any verdict. Nothing runs until both of these exist:
- a separate κ-code read in P8 form (selftest, mutants, SUMS LOG line, one-judge read);
- a logged start.

No label is made, and no AI label is used as evidence. The κ text is AI-designed. The propositions are mathematics;
the data check is descriptive.

## III.1 Definition (fixed here; order corrected per CC-255 N107)

- **Syllable code** φ(s) = (base letters, vowel modifiers ⊂ {breve U+0306, circumflex U+0302, horn U+031B}, the
  flag đ, tone ∈ {ngang, huyền U+0300, sắc U+0301, hỏi U+0309, ngã U+0303, nặng U+0323}). It is read from the NFD form.
  **đ is a base-letter special case** (U+0111 has no NFD decomposition): the parser reads it as base "d" plus the
  flag, and recomposition writes U+0111 (N113).
- **Transform set G** (a fixed list; κ quotients exactly these):
  - g1: NFC ↔ NFD;
  - g2 ‡: tone-mark placement, old ↔ new style (*hoà* ↔ *hòa*), **only inside a step-6 letter run that parses as one
    Vietnamese syllable in both styles** (CC-255r2 N131). A run that does not parse as one syllable, such as the
    unspaced "hoàbình", is outside g2;
  - g3: segmentation markup (*xe_máy* ↔ *xe máy*);
  - g4 ‡: whitespace runs, where whitespace is **step 3's class**: Unicode White_Space under the pinned Unicode
    version of the κ code (N131);
  - g5: letter case;
  - g6 ‡: a change of the **maximal trailing run over step 5's set** {. ! ? … ; : ,} ∪ whitespace (N131). A closing
    quote or bracket after the final period is not in that set and is outside g6;
  - g7 (the i/y table) is **off** and not part of this registration.
- **κ, in this order** (each step acts on the previous step's output):
  1. NFC over the whole string;
  2. each underscore → one space;
  3. collapse every whitespace run to one space, trim both ends;
  4. case fold;
  5. strip the sentence-final punctuation: the maximal trailing run of characters in {. ! ? … ; : ,} and whitespace;
  6. split into letter runs (maximal runs of Unicode letters and combining marks; every other character is a
     delimiter and is kept). Each letter run that parses as a Vietnamese syllable is recomposed from φ with the
     new-style placement rule; a run that does not parse is kept as it is;
  7. NFC over the whole string, pass-through runs included.
- A metric that needs words segments **after** κ with one pinned segmenter. M_κ(x, R) := M(κ(x), κ(R)).

## III.2 The three properties (statements)

- **P1 (exact invariance).** For every g ∈ G **as defined in §III.1**, every text metric M, every candidate x and
  reference set R:
  M_κ(g(x), R) = M_κ(x, R), and the same holds for g applied to any reference.
  - *Proof line, checked against the §III.1 order.* κ∘g = κ for each generator:
    - g1 is removed by step 1, and every later step reads only step 1's output;
    - g3, g4, g5 and g6 change only what steps 2, 3, 4 and 5 normalise. These steps leave letters other than case
      unchanged, so the letter runs reaching step 6 are equal;
    - g2 changes only the mark placement inside a letter run that parses in both styles. The parser accepts both
      styles, and step 6 writes one, so step 6's output is equal.
  - Because each generator is absorbed on every string, compositions are absorbed too
    (κ∘g∘h = κ∘h = κ).
  - **Scope:** g5 is claimed for letters whose case mapping is one-to-one under the pinned Unicode version. The
    Latin letters with Vietnamese diacritics are such letters. Others (e.g. "ß", dotted "İ") are outside the claim
    and are listed as selftest pass-through cases.
  - The cases CC-255 named are now covered:
    - "hoà." vs "hòa." (step 5 runs before step 6);
    - "hoà_bình" vs "hòa bình" (step 2 runs before step 6);
    - an unparsable run in NFD vs NFC (step 1 and step 7 act on the whole string).
- **P2 (tone separation).** For parsable syllables s, s′: if φ(s) and φ(s′) differ in tone, in a vowel modifier or in
  the đ flag, then κ(s) ≠ κ(s′). κ restricted to parsable syllables is a function of φ (case aside), and φ is
  recoverable from κ(s) by NFD plus the đ rule. Diacritic stripping meets P1 and fails P2.
- **P3 (rank-flip condition).** References are κ in both arms. The **raw** score is M_i := M(x_i, κR) (CC-255 N107),
  and system i's orthographic shift is δ_i = M(x_i, κR) − M(κx_i, κR).
  - Then M_i − M_j = (M_κ,i − M_κ,j) + (δ_i − δ_j). So a ranking flip between i and j needs
    |δ_i − δ_j| ≥ |M_κ,i − M_κ,j| (a necessary condition, exact).
  - A caption c is *touched* when κ(x_c) ≠ x_c.
  - For a metric that is the mean of per-caption scores, each depending only on that caption and the fixed
    references: **δ_i = π_i · μ_i** exactly. π_i is the touched share and μ_i the mean shift over touched captions.
  - "Form rate drives flips" (|δ_i − δ_j| ≈ |μ̄| · |π_i − π_j|) holds only under the assumption **A-μ: μ_i ≈ μ_j**. It
    is checked on data (§III.4) and is not a guarantee.
- **Assumptions checked without labels:**
  - A1, parse coverage ≥ 99% of reference syllables (else P1 and P2 are stated for the parsable part only);
  - A2, every g ∈ G is meaning-preserving, argued from orthographic norms; no human-validity claim is made;
  - A3, the metric reads text only through κ.
- **Not claimed:** better agreement with humans; synonyms or regional words; agreement between segmenters; restoring
  unaccented text. No "first" claim.

## III.3 Selftest and mutants (fixed now, for the later code read)

- **Selftest pairs**, each of which must map to equal κ outputs unless marked "distinct":

| pair | what it checks |
|---|---|
| *quả*, *giữa* | qu/gi onsets parse |
| *hoà/hòa*, *khoẻ/khỏe*, *thuỷ/thủy* | g2 |
| each of the above in NFC vs NFD | g1 |
| *mắt* vs *mặt* (distinct) | P2, tone |
| *đá* vs *dá* (distinct) | P2, the đ flag |
| **composition pairs (N107):** "hoà." / "hòa."; "Hoà_bình" / "hòa bình"; "hoà, bình" / "hòa, bình"; "HOÀ" / "hòa"; an unparsable run in NFD vs NFC | step order |
| a trailing "!" and case change | g5, g6 |
| ‡ "hoàbình" vs "hòabình" (**distinct**: outside g2, one unparsable run) | the g2 domain (N131) |
| ‡ "hòa." vs "hòa.”" (**distinct**: the closing quote is outside step 5's set) | the g6 domain (N131) |
| ‡ "hòa." followed by U+00A0 vs "hòa." (equal: U+00A0 is White_Space) | the g4/g6 whitespace class |

- **Mutants** that must fail the selftest:
  - m1: κ strips tone marks (breaks P2);
  - m2: κ without step 1 (breaks P1 on g1);
  - m3: κ keeps the old placement (breaks P1 on g2);
  - m4: κ drops unparsable runs (breaks pass-through);
  - m5 ‡: the v1 order on whitespace tokens. κ splits on whitespace, parses each whole token, and only then runs
    steps 2-5. "hoà." and "hòa." then fail to parse as tokens and pass through unequal, which breaks the composition
    pairs. With letter-run splitting, a parse-first κ would map those pairs equal, so m5 is defined on whitespace
    tokens (CC-255r2 N135).

## III.4 Preregistered data check of P3 (POST_HOC, descriptive; no run in this amendment)

**Permission.** PI-1105b allows the spent KTVIC test references as a dev set for this check: descriptive only, CPU,
no new labels. This answers v1's PQ-4.

**Paper-text clause (binding on the paper, PI-1105b; N109).** In the paper this check is labelled descriptive and is
never stated as a confirmatory claim.

**Inputs**, named by manifest keys only; no file was opened for this draft.
- The 73 stored KTVIC system outputs of the tone_norm audit:
  - `data/results/tone_norm/SUMMARY.json`, sha `dd511d3a…`, key `meta.ktvic_total_systems` = 73, at
    `number_manifest_B.tsv` l.54;
  - scored against the spent KTVIC test references (CP-071; dev role, v3.1 l.231).
- The per-caption output files are not in `data/results/tone_norm/`, which holds aggregates only (CC-255 Ruling 8).
  The κ-code read locates them and LOG-pins the file list and shas before κ runs.

**What was already seen (disclosure; N109).**
- The tone_norm audit already showed per-system changed-caption counts and B's object-metric P/R/F1 under another
  normaliser (m1). It did not show ROUGE-L, CIDEr-D or BLEU under κ.
- The K-c and K-d thresholds are therefore fixed before any κ score exists, but after related counts were seen. The
  POST_HOC label stays.

**A1 coverage check:** KTVIC train and UIT-ViIC train references only (laptop CPU); syllable parse rate; bar 99%.

**Metrics:**
- caption-averaged, so the identity applies: ROUGE-L in the kit's pinned pycocoevalcap form (mean of per-image scores);
- CIDEr-D: the identity also applies if the pinned scorer computes document frequencies from the references only (κR
  in both arms). The κ-code read checks this in the pinned code (R6-K3); if it does not hold, CIDEr-D is an
  empirical row only;
- corpus BLEU-4: an empirical row only, because it is not caption-averaged;
- tokenisation: the kit's registered default, pinned at the code read.

**Order (pre-fixed):**
1. Stage 1, with no score computed: apply κ to every system output, count π_i per system, write `kappa_pi.json`, and
   LOG-pin its sha.
2. Stage 2: compute M_κ,i = M(κx_i, κR), the raw M_i = M(x_i, κR) (the same κR, N107), δ_i and μ_i with the same
   scorer.

**Checks and pre-fixed readings** [thresholds are proposals for the judge]:

| id | check | reading |
|---|---|---|
| K-a | \|δ_i − π_i·μ_i\| ≤ 1e-9 per system, per caption-averaged metric | must hold by arithmetic; a failure is a code FAULT, not a finding |
| K-b | every observed flip pair (raw order ≠ κ order, both against κR) satisfies \|δ_i − δ_j\| ≥ \|M_κ,i − M_κ,j\| | holds by arithmetic given the N107 definition; a failure is a FAULT |
| K-c | A-μ over systems with ≥ 30 touched captions: (max μ_i − min μ_i) ≤ 0.5·\|μ̄\| (μ̄ = pooled mean shift) | "A-μ held" or "A-μ not held", reported with the spread |
| K-d | π-only predictor F_π = {(i,j): \|μ̄\|·\|π_i − π_j\| ≥ \|M_κ,i − M_κ,j\|} against the observed flips F_obs | **descriptive reading**: "consistent with the π-only reading" iff A-μ held, \|F_obs\| ≥ 3 and recall \|F_obs ∩ F_π\| / \|F_obs\| ≥ 0.8; otherwise "not consistent"; "no flips" if \|F_obs\| = 0 (reported, as meta-review item 13 asks). Precision is reported beside it |

**Output and compute.**
- Output label: `POST_HOC / DESCRIPTIVE (B κ P3 check)`. No PA3, no PA1 verdict, and no change to any freeze (R5 E-15
  applies by analogy). Logs hold counts only, never caption text.
- Compute: laptop CPU only. Each stage logs its start and its output sha.

---

## Change table v1 → v2 (`3b25457c` → `4bfd5132`; record)

| id | v2 location | change | source |
|---|---|---|---|
| V2-1 | header, effect clause | Part II removed to `AMENDMENT_R6_PART2_CAP_DRAFT.md`; ADOPTED lines pin commit + file sha | CC-255 N112, Ruling 9 |
| V2-2 | §I.5, H-14, H-23, §I.7 | one 3090 live at a time: C deleted → HB-T1 → deleted → HB-CUS; "may run while HB-T1 runs" deleted | CC-255 N104; PI-1105a |
| V2-3 | §I.3 | single home; per-instance "spent" ledger; T_down = 1 h × r_host pinned; "+3 h" = T_down + 2 h idle; fail-closed money stop; "at most" excludes idle | CC-255 N105 (a)-(c); CC-253 MB2/MB3; CC-254r2 N98 |
| V2-4 | H-47, H-48 | rows for v3.1 l.535-537 and R5 l.350 | CC-255 N105 (d); CC-254r2 N99 logic |
| V2-5 | H-9†, H-38 … H-46, H-49 … H-53, kept list | every 4090/M1/M8 line rowed or listed with a reason; R5 rental definition restated; E-13 fetch extended to HB-CUS for UIT-ViIC 231 | CC-255 N106 (a)-(g) |
| V2-6 | §I.6, H-4†, H-5†, H-6†, H-7†, H-46 | block W stays 1.0 GPU-h (host CPU, not scaled); arithmetic redone: 19.65 h after W + S; core 12.1 h; thresholds 14.8 / 18.8 / 38.0% | CC-255 N106 (g), Ruling 3 |
| V2-7 | §III.1-§III.4 | κ step order fixed (NFC → underscores → whitespace → case → final punctuation → parse letter runs → NFC); P1 proof line rechecked; raw M_i := M(x_i, κR); composition selftests; mutant m5 | CC-255 N107, Ruling 7 |
| V2-8 | §I.3 rule 3, PQ-1, VN summary | "the PI is asked for a top-up" → "B waits (PI-1105a)"; PQ-1 answered; balance redone at 22 h | CC-255 N108; PI-1105a |
| V2-9 | §III.4, PQ-4 | PQ-4 answered; paper-text clause; K-d as a descriptive reading; disclosure of what tone_norm showed; per-caption files pinned at the code read | CC-255 N109; PI-1105b |
| V2-10 | §I.5 | CC-209 Ruling 1 narrowed to HB-CUS for the two spent sets | CC-255 N110; CC-254 N93 |
| V2-11 | sources | B_UPGRADE_PLAN sha 0d08133d → 8f8cc1e8 | CC-255 N111 |
| V2-12 | §III.1, kept list | underscores → one space; đ as a base-letter case; v3.1 l.273 kept | CC-255 N113 |
| V2-13 | — | STATE_2026-11-03's B row predates PI-1104ae/ag and PI-1105a; the files and newest PI lines win; refresh at the next STATE write (coordinator) | CC-255 N114 |
| V2-14 | §I.6, HB-CUS | 3090 money now includes T_down: HB-T1 ≈ 158,722 expected / 250,614 at most; HB-CUS ≈ 100,246 / 129,948 | derived from V2-3 |

## Change table against v2 (`4bfd5132`)

| id | v3 location | change | source |
|---|---|---|---|
| V3-1 | §I.6, H-46, R6-J7 | a W timeout is a final CAP STOP (registered v3.1 l.503-504, R5 l.473); W's per-step `timeout` is its 1.0 GPU-h block cap; the R5 §D.2 laptop fallback covers only a failed install or check; v2's timeout-fallback sentence withdrawn | CC-255r2 N130 (option i) |
| V3-2 | §III.1 g2, g4, g6; P1; §III.3 | g2 limited to a step-6 letter run that parses as one syllable in both styles; g6 = the maximal trailing run over step 5's set; g4 = step 3's whitespace class; P1 "as defined in §III.1"; domain selftests "hoàbình"/"hòabình", "hòa."/"hòa.”", NBSP | CC-255r2 N131 |
| V3-3 | §I.1, §I.2, §I.3 rule 0, rule 3 | r_host = hourly price only, defined only in §I.3 rule 0; setup fee a separate field, added once to L-before | CC-255r2 N132 |
| V3-4 | §I.3 rule 1, lines table | spent read immediately before the delete click; L-before − L-after is the cross-check | CC-255r2 N133 |
| V3-5 | §I.8 preamble | † meaning stated; seven v2 wording follow-ons named; ‡ = changed in v3 | CC-255r2 N134 |
| V3-6 | §III.3 m5 | m5 = the v1 whitespace-token order, so the composition pairs kill it | CC-255r2 N135 |
| V3-7 | H-28, H-49, kept list | top-up clauses met by PI-1102b, no new top-up; R5 l.23 second sentence and v3.1 l.283 "id survivors" kept as spent/moot | CC-255r2 N136 |
| V3-8 | kept list | money-line grep record; no conflict with PI-1105a | CC-255r2 N137 |
| V3-9 | sources | PI-1105c added: no Part I change at 22 h; it answers Part II's P-3 | CC-255r2 N138 |
| V3-10 | header, VN summary | round 3/3; Part II file is now `AMENDMENT_R6_PART2_CAP_DRAFT_v2.md`, re-pinned to this file | CC-255r2 Ruling 6 |
| V3-11 | — | STATE_2026-11-03 B row refresh: carried to the coordinator's STATE write | CC-255 N114 (carried) |
| V4-1 | §I.6 l.272 | v4's only change from v3 (`eb025dfc`): the balance parenthetical no longer subtracts C's T_down a second time (C's 350,000 / 465,000 is its whole block spend, T_down included); no printed figure changes | CC-255r3 N150, Ruling 5 |

No figure of §I.6, §I.3 or the balance lines changes in v3, except that L-before now adds the setup fee (0 in the
planning figures).

## Rulings needed (round 3/3, one judge, FULL read, reversible 85; a diff read cannot grant GO)

| # | part | question | recommended | default if no answer |
|---|---|---|---|---|
| R6-J1 | I | With N104-N106 closed, do §I.1-§I.3 and H-2 meet R5 E-10's "new E-10 restatement"? | YES | no HB-T1 step |
| R6-J2 | I | HB-CUS as the PI-named custody host (v3.1 l.272), with the CC-209 R1 narrowing (§I.5)? | YES (CC-255 Ruling 5: 86 in substance) | custody rows NOT RUN |
| R6-J5 | I | §I.3: T_down = 1 h, idle margin 2 h, fail-closed stop at (T_down + 0.5 h) × r_host? | YES | as written |
| R6-J7 | I | Block W kept at 1.0 GPU-h, not scaled, with its per-step `timeout` = 1.0 GPU-h and a W timeout = final CAP STOP as registered (§I.6, H-46): no cap number and no rule changes, so no Part II-type change? | YES | as written |
| R6-J8 | I | Do H-1 … H-53 plus the kept list cover every 4090/M1/M8 line of both files? | YES | rows added in round 3 |
| R6-K1 | III | Is P1 now true for G as defined in §III.1 (g2, g4, g6 domains; N131), within the g5 scope? Are P2 (with đ) and P3 (raw M_i := M(x_i, κR)) correct? | YES | no κ code |
| R6-K2 | III | Are the stage order and the K-a … K-d readings pre-fixed enough to count as preregistered, with the POST_HOC label and PI-1105b's clause? | YES (CC-255 Ruling 8: 85) | P3 stays a paper-text statement only |
| R6-K3 | III, κ-code read | Does CIDEr-D qualify (document frequencies from references only)? | check in the pinned code | empirical row only |

Rulings J3 (×1.5 restatement) and J4 (trigger label) were YES in CC-255 (Rulings 3-4), and J6 was YES in substance
(Ruling 5). They carry unchanged except for V2-6.

## Open PI questions

| # | question | recommended | default if no answer |
|---|---|---|---|
| PQ-1 | Balance and top-up | **answered: PI-1105a** (sequential, no top-up, B waits). At the 22 h caps the balance covers both B machines after C at 350,000. After C at 465,000, HB-CUS waits unless HB-T1 spends ≤ about 185,000 (§I.6) | — |
| PQ-2 | HB-CUS setup (≈ 4 h) and T_down (1 h) outside the 9 GPU-h cap, at most 129,948 VND at 9,282 VND/h (excluding idle)? | YES (same convention as tier 1) | YES; the cap stays 9 GPU-h |
| PQ-3 | May the custody block reuse the HB-T1 machine after B's logged tier-1 deletion? | NO: D5 says separate, and v3.1 l.263 keeps the tier-1 host free of other images (CC-255 Ruling 5) | NO |
| PQ-4 | P3 data check on the spent KTVIC test references | **answered: PI-1105b** | — |
| PQ-5 | Timing: HB-T1 starts when C's machine is gone (PI-1105a); if that falls inside A's 15-30/11 turn, wait until after 30/11? | YES (v3.1 l.521) | wait until after 30/11 |
| PQ-6 | §9.2 trigger on a 3090: keep 150 GPU-h (stricter)? | keep 150 (CC-255 Ruling 4) | 150 |

## Drafting-touch disclosure

Read:
- v3: CC-255r2 in full; LOG l.1550 (PI-1105c); v3.1 l.7-9; R5 l.23, l.29-30. v2 (below):
- CC-255 in full; CC-253 l.113-121; CC-254r2 (grep plus the N98-N100 lines);
- LOG l.1164, l.1543-1546;
- v3.1 l.263, l.273, l.282-283, l.288, l.522-523, l.535-537;
- R5 l.15-16, l.29, l.99-102, l.320, l.349-350, l.379, l.387, l.406-410, l.429, l.450, l.457-458, l.465, l.474-475;
- R5 lines 1-665 that match the 4090/M1/M8 grep, at most 170 characters each;
- the v1 inputs.

No rental page, provider id or host address was opened. No image, caption, reference, label or sealed file was
opened, and `~/.vsps_sealed` was not touched.
