# B-PA1-T1 AMENDMENT R6 Part II: tier-1 cap 22 → 28 GPU-h on the 3090, with the PI-1105c fallback — DRAFT v4, not approved

Status: **DRAFT v4, for round 3/3 (the last): full panel + Codex read-only. Not adopted, not committed, licenses
nothing.** It answers CC-256r2 (round 2/3, NEXT_ROUND 82; `.session_backup/2026-10-13/decisions/CC-256r2.txt`, sha
`8d649556`): BLOCKING R2-T1 (B-r2-1), R2-T2 (B-r2-2), R2-T3 (BP-1 … BP-3) and the NON-BLOCKING N-r2-a … N-r2-k.
R2-T4 (CX1 anchor) stays open for the round-3 Codex read. Through v3 it also answers CC-256 (round 1/3, NEXT_ROUND 75,
sha `ce0f30d2`), themes T1-T8 and CX1.

Kept unchanged:
- v1 (`AMENDMENT_R6_PART2_CAP_DRAFT.md`, `ccc0d80a`, 146 l.), the subject of CC-256;
- v2 (`AMENDMENT_R6_PART2_CAP_DRAFT_v2.md`, `797823d2`, 160 l.), a re-pin only;
- v3 (`AMENDMENT_R6_PART2_CAP_DRAFT_v3.md`, `18a59515`, 275 l.), the subject of CC-256r2.

**Which file is registered (N-r2-d).** Part I v4 l.7 and l.77 name `AMENDMENT_R6_PART2_CAP_DRAFT_v2.md` as the Part II
file. Those lines were written before v2 was superseded. The Part II file that goes to round 3 and, on GO, to the
gatekeeper commit is **this file** (`AMENDMENT_R6_PART2_CAP_DRAFT_v4.md`). The R6-II ADOPTED line names it by path and
sha.

**Tier: IRREVERSIBLE, full panel (three judges) + Codex read-only, bar 85.** It changes a registered cap after
registration (judge.md; PI-1103ad; CC-256 TIER).
- Round 2/3 (CC-256r2) ran on v3 before the R6-I ADOPTED line. It is recorded as a deliberate pre-adoption substance
  read (CC-256r2 Ruling 7).
- Round 3/3, the last, is a full panel + Codex read-only on this file, which cites the adopted Part I (effect clause
  step 3).
- A diff read never grants GO. Without a round-3 GO the topic goes to ESCALATE_TO_PI (CC-256r2 Ruling 6).

**Effect clause and sequence (CC-256 Ruling 6, T8).** In this order, each step after the previous one:
1. a gatekeeper commit of R6 Part I (Parts I+III file), after its own GO;
2. the LOG line `R6-I ADOPTED <CC id> <commit> <file sha>`;
3. a full-panel GO on a version of **this** file that cites the adopted Part I sha from step 2 (or a GO re-issued after
   step 2 for a version that already cites it);
4. a separate gatekeeper commit of this file (never in the same commit as Part I; the same gatekeeper session is fine);
5. the LOG line `R6-II ADOPTED <CC id> <commit> <file sha>`.

Steps 1 and 2 are done: gatekeeper commit `90ed1a6eb103f052c6c6df4e93292102ced3e8f5`, and LOG l.1572 "R6-I ADOPTED"
(PI-1105d, PI-1105f). Until step 5 the cap is 22 GPU-h, and R6 Part I §I.6 governs.

**Return trigger (widened, T8).** This file returns to its panel before any commit if either of these differs from
what is cited here:
- the adopted Part I sha: `AMENDMENT_R6_DRAFT_v4.md` `0b55d5f8`, commit `90ed1a6`, R6-I ADOPTED at LOG l.1572;
- any Part I line this file quotes or rows: H-6, H-7, H-46, §I.3 rules 0-4, §I.5 sequence, §I.6 (table, trim bullets,
  money table, balance bullets), PQ-1, or the VN summary money lines.

Written 2026-11-05T10:17:54Z (`date -u`); v3 05:16:43Z. HEAD at drafting `f5c6741`. Nothing rented, run or committed. Every
estimate is AI opinion, not evidence.

Cites and amends (none is edited):
- `AMENDMENT_R6_DRAFT_v4.md`, sha256 `0b55d5f8fb9b6edcb9a7c367c3da624ac446e48f41c50eec333234fb1b03f858` (643 l.),
  committed at `90ed1a6eb103f052c6c6df4e93292102ced3e8f5`, Part I (R6-I ADOPTED, LOG l.1572). §I.3 is the single home
  of r_host, block spend, T_down and the balance rule; §I.6 holds the 3090 estimates. Line numbers below are v4's.
  v4 = v3 `eb025dfc` + the l.272 clause fix + row V4-1 (l.599), so lines ≤ 598 are as in v3 and l.623 is now l.624.
- `PREREG_DRAFT_v3_1.md` `e9b30ca7` (5ff00c9).
- `AMENDMENT_R5_DRAFT_v1_2.md` `9cb21917` (3091bf6).

Sources:
- **PI-1104ag** D4 (LOG l.1534): tier-1 cap 28 h on the 3090.
- **PI-1105a** (l.1543): one 3090 at a time, C first; no top-up; B waits if the balance is short.
- **PI-1105c** (l.1550, 2026-11-05T04:47:02Z), verbatim: "if C's spend leaves too little money for B's 28 h tier-1 cap,
  B runs at the registered 22 h cap (A3 and H NOT RUN) instead of waiting for a top-up." (T1)
- **PI-1105e** (l.1568, 2026-11-05T09:26:04Z), answering CC-256r2 PQ-1 and PQ-2 (R2-T2):
  - PQ-1 (a) YES: below 29 × r_host + f after C, B waits; there is no cap below 22 h.
  - PQ-1 (b): the registered trim rule decides on measured rates; there is no forced NOT RUN. The PI was told that at a
    ×1.2 factor A3 would run in the 22 h branch, borderline.
  - PQ-2 NO: 28 h does not also require money for HB-CUS; the trade-off goes into the paper's limitations.
- **PI-1105d** (l.1564) and **PI-1105f** (l.1571): R6 Part I v4 adopted and committed alone (90ed1a6).
- **PI-1104ae** (l.1522): the host change to a 3090.
- **CC-217r3 Ruling 5** (l.48), the licence (T7).
- **v3.1 W13** (l.33, l.503-505).
- LOG l.1141 (OPS-1102b, "NB7 cap 22 h frozen").
- C host v3 (`AMENDMENT_HOST_3090_DRAFT_v3.md` `e9c04955`, committed 5d6f5ca), §3: C's T_down sits inside C's M (T6).
- B_UPGRADE_PLAN `8f8cc1e8` §3.3, §5 D4.
- CC-256; CC-256r2.

## Tóm tắt cho PI (tiếng Việt)

- Trần tầng 1 là 28 GPU-giờ trên HB-T1. Theo PI-1105c, khi tiền còn lại sau C không đủ cho 28 giờ nhưng vẫn đủ cho 22
  giờ, B chạy ở trần 22 giờ đã đăng ký thay vì chờ.
- Quy tắc theo dải số dư L-before:
  - L-before ≥ 35 × r_host + f: trần 28 giờ (f = phí setup của offer);
  - 35 × r_host + f > L-before ≥ 29 × r_host + f: trần 22 giờ;
  - L-before < 29 × r_host + f: B chờ, không có trần dưới 22 giờ (PI-1105a; PI-1105e PQ-1 (a)).
  - Quyết định một lần, trước lần thuê HB-T1 đầu tiên. Máy thuê lại sau sự cố không quyết lại.
- Ở 28 giờ dự kiến A3 và H chạy, A4 bị cắt. Chi phí dự kiến khoảng 248 nghìn đ, tối đa khoảng 306 nghìn đ (chưa tính
  giờ chờ). So với 22 giờ: +89 nghìn đ dự kiến, +56 nghìn đ tối đa.
- Ở 22 giờ, luật cắt đã đăng ký quyết định theo tốc độ đo được, không có lệnh cấm A3 và H (PI-1105e PQ-1 (b)). Ở tốc
  độ giả định, A3 và H không chạy. Nếu hệ số thật là ×1,2 (nhanh hơn giả định khoảng 15%), A3 sẽ chạy (sát ngưỡng),
  H thì không.
- Sửa lỗi đếm hai lần: T_down của C đã nằm trong M của C. Nếu C dùng 465 nghìn đ, 28 giờ vẫn qua được với r_host ≤
  khoảng 9.528 đ/giờ (thừa khoảng 8.618 đ ở 9.282 đ/giờ).
- Đánh đổi (N-d): ở 28 giờ, nếu C dùng 465 nghìn đ thì máy custody HB-CUS gần như chắc phải chờ. Nghĩa là A3 và H
  được ưu tiên hơn các dòng custody. PI-1105e PQ-2 = KHÔNG đổi; đánh đổi này được ghi vào phần hạn chế của bài báo.

## 1. Licence, W13, and why

**W13, quoted in full.**
- v3.1 l.33 (closure row): "| W13 | cap fixed before registration (PI Q-a; default 20 h) | §9.1, §15 |".
- v3.1 l.503-505: "The cap is fixed before registration and never changed after block S rates are seen (W13; PI Q-a: 20
  vs 22-24 GPU-h; default 20)."

**Licence: CC-217r3 Ruling 5** (l.48), verbatim: "The 4090 cap is frozen at registration (CC-217r2 Ruling 6). If the PI
chooses 22 GPU-h, it goes into v3.1 before the commit; any later change is an amendment read before block S and never
after a rate is seen."

**Override, stated (T7).**
- This amendment overrides the "fixed before registration" half of W13. It keeps the "never changed after block S
  rates are seen" half in full.
- Reasons:
  1. The host class changed after registration (PI-1104ae: 3090 only). M8 (the 4090) was deleted (LOG l.1262) before
     any B GPU step.
  2. The PI chose 28 h on the 3090 (PI-1104ag D4) and the 22 h fallback (PI-1105c).
  3. No B rate exists. The LOG has no B launch, block-W or block-S line (CC-255 Ruling 3; CC-256 Ruling 1).
- This is a later change of the kind CC-217r3 Ruling 5 allows: an amendment read before block S.
- **There is no precedent.** v1's "as 20 → 22 h was (PI-1102a; R5 E-7)" is withdrawn. 22 h was frozen at registration
  (5ff00c9 message line 6; LOG l.1141 NB7; R5 l.291 row 8, l.563), and E-7 only aligned the text.

**Block set, not a factor claim (N-a).**
- At the assumed rates, the registered 22 4090-h ran W, S, A1, A2, A3 and H, with A4 trimmed (R5 E-7). The 28 h cap
  on HB-T1 runs the same block set at the assumed 3090 rates (§2). It restores that set and does not add A4 at the
  assumed rates. At ×1.2 it still does not add A4: k ≈ 0.847 > 0.817, A4's bound (§3) (N-r2-a).
- In 4090-hours, 28 3090-h ≈ 19 4090-h at the ×1.5 factor, but ≈ 23.3 at ×1.2 (28 / 1.2 = 23.33; R2-T1). So the hour comparison depends on the
  factor and is not the argument.

**Money (N-c).** At most (28 + 4 + T_down 1) × 9,282 ≈ 306,306 VND, excluding idle (R6 v4 §I.3 rule 6). That is below
R5's registered 455,000 VND at the M8 rate (E-7). Against 22 h:
- expected spend: +89,107 VND (247,829 − 158,722);
- at most: +55,692 VND (306,306 − 250,614). B_UPGRADE_PLAN's "+56,000" is this at-most delta only.

## 2. The branch rule (PI-1105c; T1, T2, T3, CX1)

**P-3: an unconditional rule, decided once.**
1. **When.** Once, immediately before the **first** HB-T1 rental, after C's machine is deleted and its delete line and
   L-after are logged (R6 v4 §I.5).
2. **Offer first, then the cap (N-f).**
   - The offer is chosen by the R6 v4 §I.1 acceptance rule alone.
   - Among the offers that meet every field at that time, the one with the lowest r_host is taken. This file is the
     rule's only home, and it is adopted by value with this file in the R6-II ADOPTED line, as N158 did for R6-I's
     values (N-r2-c).
   - P-3 is then computed from that offer's r_host and setup fee. A cap is never chosen by shopping between offers.
3. **Band**, with L-before = the balance read for the first HB-T1 rental line, and f = the offer's setup fee:

| L-before | tier-1 cap | source |
|---|---|---|
| ≥ 35 × r_host + f | **28 GPU-h** (this file) | PI-1104ag D4 |
| < 35 × r_host + f and ≥ 29 × r_host + f | **22 GPU-h**, the Part I regime unchanged | PI-1105c |
| < 29 × r_host + f | **no rental; B waits** (PI-1105a). No cap below 22 h exists | PI-1105a; PI-1105e PQ-1 (a); R6 v4 §I.3 rule 3 (CX1, below-29 case) |

4. **Logging.** The first HB-T1 rental line records r_host, f, L-before, the band and the resulting cap ("28" or
   "22 (P-3)"). That line fixes the cap.
   - **A first machine deleted by a FAULT before any B file moves (N-r2-f).** A machine deleted by a §I.1 setup-check
     FAULT before any B file moves (R6 v4 §I.1) is not HB-T1 and not HB-T1′. The next accepted rental is the first
     HB-T1. P-3 is decided for it from its own offer and its own L-before, and logged with a pointer to the FAULT line.
     No B block has run then, so no rate exists and W13's second half is kept. The FAULT machine's spend counts in the
     balance only.
5. **One decision for the tier (T2).**
   - The cap is the **tier-1 total in GPU-h across HB-T1 and HB-T1′**.
   - A machine-loss re-rental HB-T1′ **never re-decides** it. HB-T1′ runs under the cap fixed in step 4, with the GPU-h
     left of it.
   - A money shortfall at HB-T1′ takes the R6 v4 §I.3 rule 4 fail-closed stop, or the v3.1 l.519-520 path (one resume;
     then the PI decides). It never takes a cap switch after block S.
   - **The "PI decides" path sets no new cap (N-r2-h).** Under v3.1 l.519-520 the PI may decide to resume once or to
     stop. A different cap would be a change after a rate is seen, which CC-217r3 Ruling 5 forbids. It would need a
     new amendment and could not apply to this tier-1 run.
   - Row C-11 states HB-T1′'s L-before.
6. **The trim rule decides in the 22 h branch (T3; CX1; PI-1105e PQ-1 (b)).**
   - In the 22 h branch, the Part I 22 h regime governs unchanged, including the measured-rate trim rule (v3.1
     l.510-511). There is **no forced NOT RUN** (PI-1105e).
   - At the assumed rates the rule trims A3 and H. A3 runs only if block S measures rates ≥ 14.8% below the assumed
     ones, and H only if ≥ 18.8% below (R6 v4 §I.6).
   - **The ×1.2 case, disclosed (CC-256r2 Ruling 4).** Decode (0.8409 s) is already measured, so at ×1.2 only scoring
     shrinks: k = (0.8409 + 2.79 × 1.2/1.5) / 3.63 ≈ 0.847, about 15.3% below the assumed rates.
     - In the 22 h branch, A3 then **runs**, borderline: 0.847 is below its 0.852 bound (0.860 if S scales).
     - H does not run (0.847 is above 0.812, or 0.822 if S scales).
     - In the 28 h branch, A4 does not run (0.847 > 0.817).
   - PI-1105c's words "(A3 and H NOT RUN)" are read as this expected outcome at the assumed rates. The PI confirmed the
     reading in PI-1105e, knowing the ×1.2 case.

## 3. Arithmetic at 28 h [derived; R6 v4 §I.6 rates; block W 1.0 h, not scaled]

- After W + S: 28 − 2.35 = 25.65 h remain.
- With A4: 25.35 × 1.25 = 31.69 > 25.65. A4 drops.
- A1 + A2 + A3 + H = 19.35 × 1.25 = 24.19 ≤ 25.65. **A3 and H run; A4 NOT RUN** at the assumed rates.
- Thresholds with W + S = 2.35 h as assumed: H ≤ +6.0% (1.060); A3 ≤ +11.2% (1.112); A4 needs ≥ 19.1% below (0.809).
- **The thresholds move with the measured W and S (N-b).** If S scales with the same rate error as the later blocks
  (factor k on S and on A1-H):
  - H runs while k ≤ 27 / (24.1875 + 1.35) = 1.057 (+5.7%);
  - A3 runs while k ≤ 27 / (23.0625 + 1.35) = 1.106 (+10.6%);
  - A4 needs k ≤ 27 / (31.6875 + 1.35) = 0.817 (18.3% below).
  - The trim rule itself always uses the measured remaining cap after S (v3.1 l.510-511).
- The thin margins are disclosed, with no re-admit rule (CC-256 Ruling 4).

| HB-T1 branch | expected (blocks + setup 4 + T_down 1) | at most (cap + setup + T_down, excl. idle) | L-before (R6 v4 §I.3 rule 3, f = 0) |
|---|---|---|---|
| 22 h (Part I; the P-3 branch) | 17.1 h ≈ 158,722 | 27 h ≈ 250,614 | 29 × r_host ≈ 269,178 |
| **28 h (this file)** | 26.7 h ≈ 247,829 | 33 h ≈ 306,306 | 35 × r_host ≈ 324,870 |

## 4. Balance under PI-1105a (from 798,488, LOG l.1375; T6 corrected)

**C's T_down is not subtracted again (T6).** C host v3 §3 stops C's decoding when C's block spend reaches M − T_down,
so C's block total stays ≤ M. C's T_down is already inside C's 350,000 or 465,000. v1's figures 439,206, 324,206,
"fails by ≈ 664", 191,377, 132,900 and 76,377 are withdrawn.

| C's spend (≤ M) | left for B | band at 9,282 VND/h | break-even r_host for 28 h (N-c) | break-even for 22 h | HB-CUS after HB-T1 expected / at most (L-before 148,512) |
|---|---|---|---|---|---|
| 350,000 | 448,488 | 28 h (passes 324,870 by 123,618) | ≈ 12,814 | ≈ 15,465 | 28 h: 200,659 (passes) / 142,182 (**waits**) |
| 465,000 (PQ-C2) | 333,488 | 28 h (**passes by ≈ 8,618**) | **≈ 9,528** (2.7% above planning) | ≈ 11,500 | 28 h: 85,659 (**waits**) / 27,182 (**waits**) |
| 465,000, P-3 branch, recomputed at r_host = 9,529 (the first whole VND/h at which P-3 fires: 35 × 9,529 = 333,515 > 333,488) | 333,488 | 22 h (L-before 29 × 9,529 = 276,341, passes) | — | ≈ 11,500 | 22 h: HB-T1 expected 17.1 h ≈ 162,946, at most 27 h ≈ 257,283; HB-CUS L-before 16 × 9,529 = 152,464: 170,542 (passes) / 76,205 (**waits**) (N-r2-b) |

- **Custody trade-off, disclosed (N-d; CC-256 D1).** At 28 h, HB-CUS waits whenever HB-T1 runs to its maximum, and
  also at its expected spend if C uses PQ-C2. So the 28 h cap puts A3 and H ahead of the descriptive custody rows (UIT-ViIC 231 + KTVIC 558).
- J2's alternative (28 h only if L-before ≥ ≈ 396,341 = HB-T1 expected 247,829 + HB-CUS L-before 148,512) is PQ-2.
  **PI-1105e: NO.**
- **Limitation sentence for the paper (PI-1105e PQ-2), draft for the PI's rewrite:** "The descriptive custody rows
  (UIT-ViIC 231 and KTVIC 558) were run only if enough money was left after the tier-1 block; if not, they are reported
  NOT RUN. This is a disclosed trade-off in favour of the A3 and H blocks."
- **C's teardown overrun (N-r2-g).**
  - §4's "left for B" assumes C's block total ≤ M (C host v3 §3). If C's teardown runs past its 1 h T_down, the excess
    lowers B's real balance. The band reads that real balance, so the rule still holds.
  - In the 22 h branch, the overrun is absorbed: under PQ-C2, 333,488 − 269,178 = 64,310, about 6.9 h at 9,282.
  - In the 28 h branch under PQ-C2, the margin is only 8,618, which is less than 1 h. An overrun there moves B to the
    22 h branch, as PI-1105c intends.
  - B's own 2 h idle margin covers B's idle time, not C's.

## 5. Registered lines changed (old → new), branch-aware

"Old" is the text of the adopted R6 Part I v4 (`0b55d5f8`, commit 90ed1a6; line numbers of v4). The original registered line
is cited beside it.

**"[cap]"** in a new text below reads: "28 GPU-h, or 22 GPU-h when P-3 fires, as logged in the first HB-T1 rental line
(R6 Part II §2)".

| # | where | old (quoted) | new |
|---|---|---|---|
| C-1 | v3.1 l.503 as R5 E-7 l.337 | "Hard cap: 22 GPU-h (PI-1102a B-Q2, commit 5ff00c9)" | "Hard cap: [cap] on HB-T1, the tier total across HB-T1 and HB-T1′ (PI-1104ag D4; PI-1105c; R6 Part II)" |
| C-2 | v3.1 l.283-284 as R5 E-7 l.336-337 | "inside the 22 h cap" | "inside the [cap]" |
| C-3 | v3.1 l.511-516 as R5 E-7 l.339-347, restated by R6 v4 H-6 (l.318) | "At the assumed 3090 rates the trim rule drops A4, H and A3 (after S: 22 − 1.0 − 1.35 = 19.65 h remain; …) … A4 at least 38.0% below; …" | **28 h branch:** "At the assumed 3090 rates the trim rule drops A4 (after S: 28 − 1.0 − 1.35 = 25.65 h remain; A1 + A2 + A3 + H = 19.35 h, × 1.25 = 24.19 ≤ 25.65; with A4, 25.35 × 1.25 = 31.69 > 25.65). The expected spend is W + S + A1 + A2 + A3 + H = 21.7 GPU-h plus setup and T_down (R6 §I.3), about 248,000 VND at 9,282 VND/h; at most about 306,000 VND (cap + setup + T_down, excluding idle). With W + S taking 2.35 h as assumed, H runs only if block-S rates are at most 6.0% above the assumed ones, A3 up to 11.2% above, and A4 only if they are at least 19.1% below; these move with the measured W and S; the rule itself always uses the measured remaining cap after S." **22 h branch:** H-6's text unchanged; the trim rule decides on measured rates, with no forced NOT RUN (PI-1105e); at ×1.2 (k ≈ 0.847) A3 would run, borderline, and H would not (§2 item 6) |
| C-4 | R5 §D.3 l.460 and l.473 | "Order and caps inside 22 GPU-h"; "cap 22 GPU-h with per-step `timeout`" | "Order and caps inside the [cap]"; "cap [cap] with per-step `timeout`" |
| C-5 | R6 v4 §I.6 table l.245-254, last column "at 22 h, assumed rates" | A3 "trimmed unless rates ≥ 14.8% below assumed"; H "… ≥ 18.8% below …"; A4 "… ≥ 38.0% below …" | the "at 22 h" column is **kept** (the P-3 branch). A column "at 28 h, assumed rates" is **added**: W, S "runs"; A1, A2 "runs (core)"; A3 "runs while rates ≤ +11.2%"; H "runs while rates ≤ +6.0%"; A4 "trimmed unless rates ≥ 19.1% below" |
| C-6 | v3.1 l.648 Q-a status, as R5 E-7 l.347-348 | "PI-1102a: 22 h" | "PI-1102a: 22 h; PI-1104ag D4: 28 h on a 3090, with the PI-1105c 22 h fallback (R6 Part II §2)" |
| C-7 | R6 v4 §I.3 rule 3 (l.142) | "HB-T1 at 22 h: 29 × r_host ≈ 269,178 VND." | kept, and a line is **added**: "HB-T1 at 28 h: 35 × r_host ≈ 324,870 VND. Which applies is decided once by R6 Part II §2 (P-3 band); the setup fee is added once." |
| C-8 | R5 §D.2 l.458, as R6 v4 H-46 (l.358) | "Cap 1.0 GPU-h (v3.1 l.492) inside the 22 h." | "Cap 1.0 GPU-h (v3.1 l.492) inside the [cap]." W's per-step `timeout` stays 1.0 GPU-h, and a W timeout stays a final CAP STOP (R6 v4 §I.6, H-46) |
| C-9 | R6 v4 §I.6 money table, HB-T1 row (l.269) | "HB-T1 (22 h) \| 12.1 + 5 = 17.1 h ≈ 158,722 \| 27 h ≈ 250,614 \| 269,178" | row **kept** (P-3 branch); row **added**: "HB-T1 (28 h) \| 21.7 + 5 = 26.7 h ≈ 247,829 \| 33 h ≈ 306,306 \| 324,870" |
| C-10 | R6 v4 §I.3 rule 3 | — | **unconditional** (T1): "P-3 (PI-1105c): before the first HB-T1 rental, L-before ≥ 35 × r_host + f → 28 GPU-h; 35 × r_host + f > L-before ≥ 29 × r_host + f → 22 GPU-h; L-before < 29 × r_host + f → no rental, B waits (PI-1105a). Decided once, logged in the first HB-T1 rental line, never re-decided (R6 Part II §2)." |
| C-11 | R6 v4 §I.3 rule 3 and §I.5 step 4 (HB-T1′) | rule 3: "balance ≥ (cap + 4 h setup + T_down + 2 h idle margin) × r_host + setup fee" | add: "For HB-T1′, 'cap' reads 'the GPU-h left of the tier-1 cap fixed in the first HB-T1 rental line'. If HB-T1′ fails its L-before: no cap switch; v3.1 l.519-520 applies (the PI decides)." |
| C-12 (T5) | R5 §D.3 l.473 as set by R6 v4 H-7 (l.319) | "Expected 12.1 GPU-h + 4 h setup + T_down [derived; R6 §I.3]" | "Expected 21.7 GPU-h + 4 h setup + T_down (12.1 under P-3) [derived; R6 §I.3; R6 Part II]" |

**Part I 22 h lines kept as the P-3 branch** (T4; each "governs under P-3; superseded in the 28 h branch by the row
named"):

| # | R6 v4 line | text (short quote) | 28 h branch |
|---|---|---|---|
| K-1 | l.221 | "## I.6 3090 estimates at the registered cap of 22 GPU-h" | read with §3 of this file and C-5, C-9 |
| K-2 | l.257-263 | "After W + S: 22 − 2.35 = 19.65 h remain." … "Core W + S + A1 + A2 = 12.1 h, 15.125 h with +25%, inside 22 h" | §3 of this file. The core sentence holds in both branches |
| K-3 | l.272-279 | "**Balance under PI-1105a** (from 798,488, l.1375; C's figure is C's whole block spend, T_down included, …)" … "**HB-CUS waits**" | §4 of this file. v4's l.272 clause agrees with §4 (V4-1, N150) |
| K-4 | l.624 (PQ-1) | "At the 22 h caps the balance covers both B machines after C at 350,000. After C at 465,000, HB-CUS waits unless HB-T1 spends ≤ about 185,000" | §4 of this file |
| K-5 | l.70 and l.72 (VN summary) | "Ở trần 22 giờ chỉ chạy lõi. HB-T1 tốn khoảng 159 nghìn đ …"; "Nếu C dùng 350 nghìn đ thì số dư đủ cho cả hai máy của B …" | the VN summary of this file |
| K-6 | l.318 (H-6) | the 22 h trim text | C-3 (28 h branch) |
| K-7 | l.319 (H-7) | "Expected 12.1 GPU-h + 4 h setup + T_down" | C-12 |
| K-8 | l.238-239 (§I.6, W timeout) | "This is less than the time left of the 22 h, so it is the binding bound." | holds in the 28 h branch with "28 h": W's 1.0 GPU-h is still the binding bound (C-8) (N-r2-e) |
| K-9 | l.398-399 ("Unchanged by Part I") | "… the 22 GPU-h tier-1 cap; …" | superseded in the 28 h branch by C-1 (the cap is "[cap]"); unchanged under P-3 (N-r2-e) |

Unchanged in both branches: the trim order (A4, H, A3); the trim criterion (v3.1 l.510-511); the core rule; CAP STOP;
the one-resume rule; block W's 1.0 GPU-h and its timeout rule; the custody cap of 9 GPU-h; every R6 v4 Part I clause
not named above.

## Change table against v1 (`ccc0d80a`; the CC-256 subject) and v2 (`797823d2`)

| id | change | source |
|---|---|---|
| P4-1 | PI-1105c encoded as an unconditional three-band rule; C-10 unconditional; R6-P3 and PQ-II-1 closed as answered; "Proposed" and the "B waits" default inside the band removed; VN summary states the adopted rule | CC-256 T1 (J1 B1, J2 W1, J3 B1) |
| P4-2 | below-29 case stated (B waits; no cap below 22 h); "A3 and H NOT RUN" read as the trim rule's expected outcome (PQ-1 defaults) | CC-256 CX1, T3 (J1 B3, J2 W5) |
| P4-3 | P-3 decided once before the first HB-T1 rental; the cap is the tier total across HB-T1/HB-T1′; HB-T1′ never re-decides; C-11 | CC-256 T2 (J1 B2, J2 W4, J3 B2) |
| P4-4 | "[cap]" in C-1, C-2, C-4, C-8; C-3, C-5, C-7, C-9 keep the 22 h text as the P-3 branch and add 28 h beside it | CC-256 T1, T4 |
| P4-5 | K-1 … K-7 rows for the Part I 22 h lines kept as the P-3 branch | CC-256 T4 (J1 B4, J2 W3, J3 B5) |
| P4-6 | C-12: H-7 "Expected 12.1" → "21.7 (12.1 under P-3)" | CC-256 T5 |
| P4-7 | C's T_down no longer subtracted again; 8,618 margin, ≈ 9,528 break-even; v1's six figures withdrawn | CC-256 T6 (J1 B6, J2 W2, J3 B3) |
| P4-8 | W13 quoted in full (l.33, l.503-505); CC-217r3 Ruling 5 cited as the licence; the override of "fixed before registration" stated with its reasons; the false 20 → 22 h precedent withdrawn | CC-256 T7 (J1 B7, J2 W6, J3 B4) |
| P4-9 | effect clause = the Ruling 6 sequence; re-pin to the adopted Part I sha; return trigger widened to any quoted Part I line | CC-256 T8, Ruling 6 (J2 W6, J3 B6) |
| P4-10 | "restores" restated as the block set; the factor dependence stated | CC-256 N-a |
| P4-11 | thresholds move with the measured W and S (+5.7 / +10.6 / −18.3% if S scales) | CC-256 N-b |
| P4-12 | both money deltas; break-evens 12,814 / 9,528 (and 22 h: 15,465 / 11,500); the P-3 22 h row for PQ-C2 | CC-256 N-c |
| P4-13 | the custody trade-off disclosed in the VN summary and §4 | CC-256 N-d, D1 |
| P4-14 | HEAD 5d6f5ca; C host v3 listed; offer rule (spec first, lowest r_host, P-3 after) | CC-256 N-e, N-f |
| P4-15 | v2's re-pin to R6 v3 and its C-7/C-8 notes are carried | v2 P3-1 … P3-3 |

Carried, not in this file: N-g (STATE refresh, CC-255 N114), N-h (Codex read-only on this version before any GO),
N-STAMP (judge-panel utc).

## Change table against v3 (`18a59515`; the CC-256r2 subject)

| id | v4 location | change | source |
|---|---|---|---|
| P5-1 | §1 block-set note | "≈ 23.5 at ×1.2" → "≈ 23.3" | CC-256r2 R2-T1 (B-r2-1) |
| P5-2 | sources; §2 item 6; §2 band table; C-3 22 h branch; VN summary; PQ table | PI-1105e cited for PQ-1 (a), (b) and PQ-2; "the trim rule decides", no forced NOT RUN; ×1.2 case disclosed (k ≈ 0.847; A3 runs borderline at 22 h; H not; A4 not at 28 h) | CC-256r2 R2-T2 (B-r2-2), Ruling 4; PI-1105e |
| P5-3 | return trigger; cites; effect clause; "v4's"; every "R6 v3" citation | re-pinned to Part I v4 `0b55d5f8`, commit `90ed1a6`, R6-I ADOPTED LOG l.1572; steps 1-2 marked done | CC-256r2 R2-T3 (BP-1) |
| P5-4 | K-3 | no longer calls Part I l.272 wrong; v4's l.272 agrees with §4 | CC-256r2 R2-T3 (BP-2), N-r2-j |
| P5-5 | "Flag for R6 Part I" section | closed as resolved by Part I v4 V4-1 | CC-256r2 R2-T3 (BP-2) |
| P5-6 | K-4; disclosure | Part I l.623 → l.624 | CC-256r2 R2-T3 (BP-3) |
| P5-7 | tier paragraph (v3 l.13-15) | reworded: round 2 ran before R6-I ADOPTED (Ruling 7); round 3 = full panel + Codex; a diff read never grants GO | CC-256r2 R2-T3, Ruling 7 |
| P5-8 | §1 | "does not add A4" qualified: at the assumed rates, and still at ×1.2 | N-r2-a (P-2) |
| P5-9 | §4 | the P-3 row recomputed at r_host = 9,529, where P-3 first fires | N-r2-b (P-4) |
| P5-10 | §2 item 2 | "[proposal]" removed; the lowest-r_host rule lives only here and is adopted by value with this file | N-r2-c (P-5) |
| P5-11 | status | the registered Part II is this file, not `_v2` named in Part I v4 l.7/l.77 | N-r2-d (P-3) |
| P5-12 | K-8, K-9 | rows for Part I l.239 and l.399 | N-r2-e (P-6) |
| P5-13 | §2 item 4 | P-3 after a FAULT-deleted first machine: the next accepted rental is the first HB-T1 and P-3 is decided for it | N-r2-f (NB-5) |
| P5-14 | §4 | C's teardown overrun: absorbed in the 22 h branch; at 28 h under PQ-C2 it moves B to 22 h | N-r2-g (NB-8) |
| P5-15 | §2 item 5 | the v3.1 l.519-520 "PI decides" path sets no new cap | N-r2-h (NB-9) |
| P5-16 | VN summary | "+ f" added to the three band thresholds | N-r2-i (Codex) |
| P5-17 | §4 | the PQ-2 limitation sentence for the paper | PI-1105e PQ-2 |

No figure of §3 or of the C-rows changes. R2-T4 (CX1 anchor) stays open until the round-3 Codex read of this file.
N-r2-k is a record only. N-g, N-h and N-STAMP are carried.

## Rulings needed (round 3/3, the last: full panel + Codex read-only, irreversible 85)

| # | question | recommended | default if no answer |
|---|---|---|---|
| R6-P1 | 22 → 28 GPU-h under CC-217r3 Ruling 5, overriding W13's "fixed before registration" half only, for the reasons of §1? | YES (CC-256 Ruling 1: justified in substance) | 22 h; A3 and H expected NOT RUN |
| R6-P2 | Thin margins disclosed, no re-admit rule? | YES (CC-256 Ruling 4) | as written |
| R6-P4 | Does §2 (three bands, one decision, tier-total cap, HB-T1′ never re-decides, the trim-rule reading) encode PI-1105c with no post-rate choice left open? | YES | — |
| R6-P5 | Offer rule: spec acceptance, lowest r_host among the accepted offers, then P-3? | YES | as written |
| R6-P6 | After a FAULT-deleted first machine (before any B file moves), is P-3 decided for the next accepted rental (§2 item 4), with no rate in existence? | YES | as written |
| R6-P7 | Does the round-3 Codex read close the CX1 anchor (R2-T4) on this file? | YES | the topic goes to ESCALATE_TO_PI |

## PI questions (PQ-1 and PQ-2 answered; no open question)

| # | question | recommended | default |
|---|---|---|---|
| PQ-1 | PI-1105c reading. (a) Below 29 × r_host + f, does B wait? (b) Is "(A3 and H NOT RUN)" the trim rule's expected outcome rather than a forced NOT RUN? | **answered: PI-1105e** (a) YES; (b) the registered trim rule decides, no forced NOT RUN; the ×1.2 case was disclosed | — |
| PQ-2 | Should 28 h also require money for HB-CUS (L-before ≥ ≈ 396,341, else 22 h)? | **answered: PI-1105e NO**; the trade-off goes into the paper's limitations (§4) | — |
| PQ-3 | (note) At C = 465k, 28 h fits only if r_host ≤ ≈ 9,528; at C = 350k, up to ≈ 12,814 | — | — |
| PQ-4 | Swap the trim order to A4, A3, H? | NO, keep the frozen order | no change |

## Flag for R6 Part I: resolved

v3's flag (Part I v3 l.272 double-counted C's T_down) is resolved by Part I v4 V4-1 (l.599; CC-255r3 N150). v4 is
committed at 90ed1a6 and adopted at LOG l.1572. Nothing is open here.

## Drafting-touch disclosure

Read:
- CC-256 in full, and the CC-256 workflow journal (J2's final return in full; labels of the others);
- R6 v4 l.10, l.66-75, l.142, l.221-279, l.318-319, l.358, l.398-399, l.624 (v4 = v3 + l.272 + l.599);
- v4: CC-256r2 in full; LOG l.1564, l.1568, l.1571-1573;
- v3.1 l.30-36, l.503-505;
- CC-217r3 l.48;
- LOG l.1549-1556;
- C host v3 §3, through CC-256's quote of its l.100-106.

No rental page, image, caption, reference, label or sealed file was opened.
