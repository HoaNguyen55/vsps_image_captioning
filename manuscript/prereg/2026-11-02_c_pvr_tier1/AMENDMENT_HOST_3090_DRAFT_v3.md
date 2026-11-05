# Host amendment (Q-custody′) to C-PVR-T1: one rented RTX 3090 / 3090 Ti — DRAFT v3, not approved

Status: DRAFT v3 for the one-judge FULL read, round 3/3 of the CC-254 Item 2 topic (CC-254r2 NEXT STEP), REVERSIBLE, bar 85
(PI-1103ae, LOG l.1440). This is the read named in prereg §8.3 l.617 ("an amendment with a one-judge read"). It binds
after a GO and a gatekeeper commit. It does not license a rental by itself: the rental trigger is the tier-1 run doc
GO (plan S11).

Earlier versions are left untouched:
- v1 = `AMENDMENT_HOST_3090_DRAFT.md` (80386f22): CC-254 NEXT_ROUND 80.
- v2 = `AMENDMENT_HOST_3090_DRAFT_v2.md` (8127874d): CC-254r2 NEXT_ROUND 82, BLOCKING N98 and N99.

§11 lists the changes v1 → v2. §12 lists the changes v2 → v3, each with its source.

**Commit order (CC-254r2 Ruling 6).** This file is committed **before** T1-REP, or jointly with it if both reach GO
together. It is the single home of r_host, S, the block ledger and T_down (§2, §3).

Written 2026-11-05 (UTC). Planning text only: nothing was rented, run or committed. AI opinion throughout.

Amends:
- `PREREG_DRAFT_v1_2.md` (0a2f0773…df2b, committed 8282874);
- `PINS_A_DRAFT_v1_4.md` (624b0804…b16b148, committed 3fb6725).

Line numbers come from `git show <commit>:<path>`.

Sources:
- PI-1104af (LOG l.1530): **Q-custody′ = YES**. C's tier-1 dev decodes and the tier-2 sets may run on one dedicated,
  single-tenant RTX 3090/3090 Ti of GPU_RENTAL_SPEC, named by a host amendment with a one-judge read, with an isolated
  tmpfs and logged pixel deletion. PQ-C2 = YES, up to 465k VND.
- PI-1104ae (l.1522): every paper uses a 3090 or 3090 Ti only.
- PI-1104ad (l.1521) and `manuscript/GPU_RENTAL_SPEC.md`.
- PI-1103g (l.1315): the cap is money, ≤ 350k VND.
- PI-1104ag (l.1534): Paper B 3090 rentals on the same ckey.vn balance.
- PI-1104ah (l.1536): Q3, Q5, Q8 = YES.
- OPS-1103m1-deleted (l.1375): M1 is gone.
- CC-254 (a40a2fef) Item 2: N89–N96.
- CC-254r2 (cc0c5292): N98–N103.
- CC-253 (9c6f55cb): MB2 (per-host ledger, one home) and MB3 (teardown reserve).
- PI-1105a (l.1543): rent sequentially, C first then B, one 3090 at a time, no top-up; B waits if the balance is
  short.
- Plan `C_NEXT_STEPS_2026-11-04.md` S8 and §4.

## Tóm tắt cho PI (tiếng Việt)

- Bản v2 sửa ba lỗi chặn của CC-254:
  - (N89) thêm dữ liệu datastore (id, câu demonstration, embedding) vào phạm vi máy;
  - (N90) luật trần tiền dựa vào PINS-A §8 đã commit, không dựa vào T1-REP khi T1-REP chưa được đăng ký;
  - (N91) tiền của C là số "đã chi" của chính máy C trên trang ckey, không phải chênh lệch số dư chung với máy của B.
- Thêm các mục không chặn N92–N96: kiểm tra dung lượng tmpfs, CPU "tương đương hoặc tốt hơn" có định nghĩa cụ thể,
  sổ tiền cộng dồn khi phải thuê lại máy, và T_A chỉ lấy từ bản trên laptop.
- Bản v3 sửa hai lỗi chặn của CC-254r2:
  - (N98) giữ lại 1 giờ tiền máy (T_down = 1 giờ × r_host) cho bước kéo kết quả, ghi log xoá và xoá máy. Vì vậy máy
    dừng chạy khi tiền của C chạm M − T_down, và tổng tiền không vượt 350 nghìn (465 nghìn nếu dùng PQ-C2).
  - (N99) thêm dòng cũ → mới cho PINS-A §8 l.544-546: tiền đọc theo số "đã chi" của từng máy, không đọc theo số dư.
- File này là nơi duy nhất định nghĩa r_host, S, sổ tiền và T_down. T1-REP chỉ trích dẫn, và file này commit trước
  T1-REP.
- PI đã trả lời (PI-1105a): thuê lần lượt, C trước rồi B, mỗi lần một máy 3090, không nạp thêm tiền. Nếu thiếu tiền
  thì B chờ.

## 1. Host class (acceptance rule)

The host is labelled **HC-n**: HC-1 for the tier-1 block, HC-2 for a tier-2 re-rental or a machine-loss re-rental,
and so on. "HC-n", "laptop" and "M1" (historical) are the only host names in repo files. No provider id, IP or port is
written in the repo.

A rental is accepted only if the ckey.vn offer meets **every** field below. The offer's value of each field is written
into the rental LOG line (§3) before any C file moves. If no offer meets every field, nothing is rented: the
coordinator tells the PI the closest offer and a recommendation (GPU_RENTAL_SPEC "How to apply").

| field | required (GPU_RENTAL_SPEC) | offer value | setup check on the host (before any C file moves) |
|---|---|---|---|
| GPU | 1 × NVIDIA RTX 3090 or RTX 3090 Ti, 24 GB VRAM; never a 4090, 5090 or RTX Pro (PI-1104ae) | recorded at rental | `nvidia-smi` name and total memory |
| CUDA | ≥ 12.4 | recorded at rental | driver-reported CUDA version |
| CPU | AMD Ryzen 9 5900X **or better**, made operational: a 5900X, or any CPU with ≥ 12 physical cores / 24 threads of the same generation or newer (AMD Zen 3 or later; Intel desktop or server parts released in 2020 or later). Any other CPU: the PI gets the offer and a recommendation, and nothing is rented | recorded at rental | `lscpu`: model name, cores, threads |
| RAM | ≥ 32 GB | recorded at rental | `free -g` total |
| tmpfs | `/dev/shm` size ≥ 1.25 × the measured byte size of everything §5 places in tmpfs for that block | – | `df -B1 /dev/shm`. The size is measured from the laptop copies and the S7 id files, and is written in the run doc before the rental |
| disk | 200 GB, read/write ≥ 1000 MB/s | recorded at rental | size by `df`; one timed sequential write and read of a 4 GB scratch file, then deleted |
| network | ≥ 400 Mbps | recorded at rental | not re-measured; the weight-download rate is logged |
| uptime | > 99% | recorded at rental | – |
| online time | offer's maximum rental time ≥ 72 h (not hours paid) | recorded at rental | – |
| r_host | VND per GPU-h, the offer's hourly price | **recorded at rental** | – |

A setup check that contradicts the offer, or a tmpfs below the required size, is a FAULT. No C file moves, the
coordinator logs it, and the machine is deleted. The money spent counts against the block (§3).

## 2. r_host and the cap rule it feeds (standalone)

- r_host is the offer's VND/h at rental. It is recorded once, in the rental LOG line, and never changed during an
  instance.
- **The registered cap rule.** r_host enters the cap rule registered now: PINS-A §8 (3fb6725) l.540-543.
  - The formula is `cap_GPUh = min(⌈1.25 × P1⌉, ⌊350,000 / r_host⌋)`.
  - If the projection does not fit, arms are cut in the registered §5.1 order (A10 → A5 → A9 → A3 → A2 → A4 → A11).
  - If it still does not fit, PQ-C2 applies (PI-1104af): the 350,000 in the formula is replaced by at most 465,000
    VND.
  - If it still does not fit, the PI decides.
- **Once T1-REP is registered** (`AMENDMENT_T1_REPORTING_DRAFT.md`, af3e847d, under the CC-253 panel read; PI-1104ah
  Q8 = YES), its §9 / R-3 / R-4 form replaces the formula and cut order above. That form uses the money left,
  ⌊(M − S) / r_host⌋, and the cut order A10 → A5 → A3 → A2 → A11.
- **PQ-C2 applies in either form.** This amendment registers no cap formula of its own. Whichever of the two forms is
  registered at the P1 LOG line is the one applied, and the P1 line names it.
- **Money stop (this amendment, standalone; CC-254r2 N98).**
  - What counts is set by PINS-A §8 l.544-546 as amended by H-21: every VND billed for the C block on HC-n, setup,
    selftest, speed test, idle time and teardown included, read as per-instance spent.
  - Decoding stops when C's block spend (§3) reaches **M − T_down**. M is 350,000 VND, or at most 465,000 VND under
    PQ-C2. T_down (§3) is then used only for teardown, in this order: final output pull → deletion log → L-final →
    machine delete → L-after.
  - So the block total stays ≤ M. A cap stop is final.
- **Registered prereg l.724 and l.726 (CC-254r2 N101).**
  - Prereg §10.1 l.722 delegates the cap rule to PINS-A. PINS-A §8 l.537-538 already sets the 37-h reading aside
    ("not used").
  - On HC-n the PINS-A form above therefore governs. It applies until T1-REP R-3 replaces prereg l.722-729 as one
    block (CC-253 MB1).
  - This file makes no cap change.
- **The P1 line (CC-254r2 N102).** The bare PINS-A form ⌊350,000 / r_host⌋ ignores S, which is already spent. The S11
  run doc must therefore apply the fit check against the money left, ⌊(M − S − T_down) / r_host⌋. If T1-REP is not
  registered by then, it states a PI question.
- Planning figures use 9,282 VND/h (M1, LOG l.923) [est.]. A dearer offer that meets the spec lowers the cap. It is not
  a reason to rent off-spec.

## 3. Money ledger: per-instance spend, balance as solvency (N91, N95)

**Single home (CC-254r2 N98(b); CC-253 MB2).** This section is the only definition of:
- r_host;
- S = HC-n's per-instance spent at the P1 line, summed over the block's instances;
- the block ledger;
- **T_down = 1.0 h × r_host**, the teardown reserve, pinned now at the top of the 0.5–1 h range of CC-253 MB3. It
  covers the final output pull, the last backup, the logged deletion and the machine delete.

T1-REP §9, once registered, replaces only the cap formula and the cut order. It cites this section for S and T_down.

**C's spend is per instance, never a balance difference.** Other papers' rentals draw on the same ckey.vn balance: B's
PA1 3090 at a 28 h cap and B's custody 3090 at about 9 h (PI-1104ag). C's spend is therefore the panel's per-instance
"spent" figure for each HC-n instance, as in the LOG l.1164 precedent ("since …, spent …"). It is read with the panel
page reloaded and written in LOG lines with `date -u` stamps.

| line | when | content |
|---|---|---|
| L-before | immediately before renting | account balance, plus every other live rental named by its LOG line with its remaining capped spend R_j = its money cap − its spent so far (from its own panel row). **Solvency rule:** balance ≥ 350,000 + 3 × r_host + Σ_j R_j. If it fails, nothing is rented: the PI is asked (top-up, or wait for the other block) |
| rental line `OPS-<MMDD>c-hc<n>-rent` | at rental | the offer's id (LOG only, as in l.923), every §1 field value, r_host, the L-before balance and Σ_j R_j, "all GPU_RENTAL_SPEC fields met" |
| L-P1 | at the P1 LOG line | HC-n's per-instance spent = S (setup, selftest, speed test and idle time included); the account balance (solvency check) |
| L-final | immediately before the machine delete | HC-n's per-instance spent; the account balance |
| L-after | after the machine delete | account balance; HC-n absent from the panel |

- **Block ledger.** C's block spend = the sum of per-instance spent over every HC-n instance of that block.
- **Machine loss (N95).** If an instance is lost before its L-final read, its spent is taken from the panel's usage
  history. If that history is unavailable, the bound r_host × (loss time − rental time) is used. The re-rental (H-4)
  continues the same block ledger and the same M.
- **PQ-C2 solvency.** Raising M to at most 465,000 needs, at that moment, a balance ≥ (M − C's block spend so far) + 3 ×
  r_host + Σ_j R_j. Under PQ-C2 the money stop is at 465,000 − T_down, so the block total stays ≤ 465,000.
- **Under PI-1105a** (sequential rentals, C first), no other rental is live at C's L-before, so Σ_j R_j = 0 there.
  The rule stays general for later blocks. If that fails, the PI is asked. The machine is deleted if the wait exceeds setup time.
- **Account balance STOP.** The registered "balance < 3 GPU-h" STOP (§10.1 l.730) reads the account balance, because
  machines die at balance 0.
- **Tier 2.** A tier-2 block keeps its own ledger lines, of the same form, under the money cap of the tier-2 prereg.
  This amendment sets no tier-2 cap.

## 4. Single tenancy, isolated tmpfs, logged deletion

1. **One tenant.** From rental to delete, HC-n holds only C's job and files. No other paper's job, file or account
   touches it while any C file of §5 is on it.
   - After the logged C deletion, another paper may use the same machine only under its own GO and its own money
     line.
   - With no such GO ready, the machine is deleted (delete-when-idle rule).
2. **Images and datastore material only in tmpfs.**
   - Every C image of §5, and every datastore file of §5 (ids, demonstration caption text, embeddings, A4/A9 helper
     inputs), goes only to `/dev/shm/c_pvr_hc/` (mode 0700), never to disk. Model weights and code may sit on disk;
     the machine delete removes them.
   - Images are pushed from the laptop's copies over the SSH channel. A non-custody set may instead be fetched from a
     source pinned by its own LOG pin line. **No TextCaps pixel source is pinned yet (CC-254 N77), so T_A and any
     D-TC image come only from the laptop copy until that pin exists.**
   - Every file is sha256-checked on arrival against the run-doc manifest. A mismatch is a FAULT.
   - No third-party storage is used.
   - Size: measured, not estimated (§1 tmpfs row). The v1 "≤ 4 GB" figure is withdrawn.
3. **Logs hold ids only.** Per-image logs and prompt dumps on HC-n hold demonstration ids only, never caption text
   (meta item 17; asserted by the S10 code). Demonstration caption text never leaves HC-n except inside pulled outputs
   that hold ids only.
4. **Logged deletion.**
   - After the final pull, the run script deletes `/dev/shm/c_pvr_hc/`.
   - It appends (utc, folder, file count, manifest count) to `c_pvr_hc_deletions.log`, which is pulled to the laptop.
   - A trap deletes the folder on any exit.
   - The coordinator then writes the deletion LOG line, L-final, the machine delete, and L-after.
5. **Backups.** The 30-minute `gpu_backup` loop pulls outputs and logs, never `/dev/shm`. Its script is checked once
   for the absence of `/dev/shm` paths, as in prereg §8.2 step 4.
6. **Procedural isolation, disclosed.** The provider has root on HC-n, so the isolation is procedural, not an OS
   boundary.
   - The material placed there is spent dev sets, train slices, datastore material and the tier-2 rehearsal sets. No
     unspent test set goes there.
   - This is the trade-off the PI accepted in PI-1104af.

## 5. Sets and material covered

**Query sets.**

| set | tier | role | note |
|---|---|---|---|
| XM3600-vi (3,600) | 1 | P_obj^VI dev | custody dev set (spent) |
| KT-C (3,907) | 1 | English benchmark arms S1–S5 | custody dev set (spent) |
| KTVIC test explore half (286) | 1 | CIDEr-VI guard | custody dev set |
| OpenViIC test explore half (1,020) | 1 | CIDEr-VI guard | custody dev set |
| T_A (1,070) | 1 | English scene-text dev | non-custody; laptop copy only until N77 |
| ViTextVQA dev (1,676) | 1 | Vietnamese scene-text dev | earlier owner, spent |
| NoCaps val | 2 | P_obj^VI rehearsal | released to C by Q11 (CC-242r2 GO); NB-T2POOL first |
| KTVIC / OpenViIC confirm halves (272 / 981) | 2 | CIDEr-VI guard | NB-T2POOL first |
| O_B (1,070) | 2 | proxy rehearsal | **host coverage only. It is not a licence to read, fetch or feature O_B**: that needs the tier-2 prereg (prereg §4.3 l.363-367; CC-254 Ruling 1.4, N80) |

**Datastore material (N89).** All of it is non-custody. Each datastore is the final id file of the dev-W25 / §7.4
result (plan S7), pinned by sha in that result's LOG line. Counts below are before §7.4.

| datastore | source (prereg §7.4) | what may go to HC-n | note |
|---|---|---|---|
| D-VI | KTVIC train (2,192 images, 10,960 captions) + OpenViIC train (8,377 images, 37,785 captions), as kept by `lists` (`c_pvr_lists.json` edb07fbb) | ids; demonstration caption text; retrieval embeddings (SigLIP2 `google/siglip2-so400m-patch14-384` @ e8e48729); the images only if they are embedded on HC-n | serves the VI arms |
| D-EN | `cen_memory_allowed.tsv` (175907e2) minus restval B4 and UIT-ViIC ids, 80,083 | ids; demonstration caption text; the pinned `cen_memory_emb.npz` embeddings; the images only if they are embedded on HC-n | serves S1–S5 |
| D-TC | TextCaps train minus T_A, 20,883 images | ids; demonstration caption text; embeddings; the images only if they are embedded on HC-n and only from the laptop copy until N77 | serves T_A |
| A4 / A9 helper inputs | PINS-A cut-first addendum (plan S9) | the pinned helper weights (on disk) and their per-pair inputs drawn from the material above | no new data source |

- Every row follows the same §4 rules: tmpfs only, sha-checked arrival, ids-only logs, logged deletion.
- Weights may sit on disk; the machine delete removes them.
- Whether datastore images are embedded on HC-n or embeddings are pushed is fixed in the run doc. The §1 tmpfs check
  covers whichever is chosen.

**Not covered:** NoCaps test and OpenViVQA dev (tier 3), and any set or material not listed in §5. The host for those
is named in the tier-3 prereg.

## 6. 3090 hour estimates [est.]

Factor: 3090 hours = 4090 hours × 1.5 (house factor, plan §1). The 20 4090-h base is v4.1's cap, not a workload
measurement. Batch-1 bf16 decoding is bound by memory bandwidth (936 against 1008 GB/s), so the true factor may be
nearer 1.2. The speed-test P1 is binding.

| part | 3090 GPU-h | VND at 9,282 |
|---|---|---|
| setup + host selftest (billed) | about 4 | about 37k |
| speed test | ≤ 1.5 (registered ≤ 1.0 on a 4090) | ≤ 14k |
| tier-1 decode | about 30 (24 at factor 1.2); capped by the registered cap rule of §2 | about 278k before the cap |
| **tier-1 block** | about 35.5 billed hours, including about 4 h of setup; money ≤ 350k (≤ 465k under PQ-C2) | about 330k |
| tier 2 (NoCaps val + confirm halves + O_B, about 4–5 arms) | about 8–13 + about 4 setup | about 111–158k; the cap is set in the tier-2 prereg |

## 7. Registered lines changed (old → new)

| # | where | old (quoted) | new |
|---|---|---|---|
| H-1 | prereg §8 l.525-527 (8282874) | "test images, spent test sets in a dev role included, sit only on M1 (the test-capable GPU host) or the laptop (the data home)" | "… sit only on the laptop (the data home) or a host HC-n named by the host amendment, for the sets and material of its §5 only (PI-1104af; M1 deleted, LOG l.1375). This narrows CC-209 Ruling 1(a) (via CC-217r2 B1) for C's §5 sets only." |
| H-2 | prereg §7.4 l.518-521 | "custody dev sets (XM3600, KT-C, KTVIC test, OpenViIC test) on the laptop CPU or M1; non-custody images (…) on M1 in the C block, or on the laptop" | "custody dev sets … on the laptop CPU or HC-n; non-custody images (…) on HC-n in the C block (host amendment §5 datastore rows), or on the laptop" |
| H-3 | prereg §8.3 l.609-612 | "**Spent-test dev decodes** (…) **run on M1 only**, … so tier 1 has **one named GPU host: M1**. M1's GPU class differs from the 4090 the cap was sized on (CC-209 l.29-30); the speed test restates the projection (§10)." | "**Spent-test dev decodes** (…) run on HC-n only (host amendment), never while another paper's job is live on it. T_A and ViTextVQA dev run in the same block, so tier 1 has one named GPU host class: HC-n, 1 × RTX 3090/3090 Ti of GPU_RENTAL_SPEC. The cap is money (PI-1103g); the speed test on HC-n gives P1 (§10)." |
| H-4 | prereg §8.3 l.613-614 | "**If M1 lapses or is never free:** the tier-1 GPU block is reported NOT RUN; no substitute host is used except through the Q-custody amendment below; nothing is shrunk to fit (full-split rule)." | "If no offer meets GPU_RENTAL_SPEC, or the §3 solvency rule fails: the PI is asked (closest offer + recommendation); the block waits and is never moved to an off-spec host. If HC-n is lost mid-block: one re-rental under this amendment, same block ledger (§3) and machine-loss resume (§10.1). Nothing is shrunk to fit (full-split rule)." |
| H-5 | prereg §8.3 l.617-619 | "**Alternative only by amendment:** if the PI answers Q-custody YES, an amendment with a one-judge read names one dedicated single-tenant rental (id recorded before any pixel moves), …" | "**Q-custody′ = YES (PI-1104af); this is that amendment.** The rental id is recorded in the rental LOG line before any pixel moves; the rest as written." |
| H-6 | prereg §8.3 l.620 | "No host, IP or port is written in the repo; "M1" and "laptop" are the only names used." | "…; "HC-n", "laptop" and "M1" (historical) are the only names used." |
| H-7 | prereg §9.1 step 8 l.641 | "then the M1 tier-1 block (§10)." | "then the HC-n tier-1 block (§10)." |
| H-8 | prereg §10.1 l.719 | "### 10.1 Tier-1 block (M1, after Q11 = YES and step 8 of 9.1)" | "### 10.1 Tier-1 block (HC-n, after Q11 = YES and step 8 of 9.1)" |
| H-9 | prereg §10.1 l.720 | "Speed test <= 1.0 GPU-h" | "Speed test <= 1.5 GPU-h on HC-n (= 1.0 4090-h × 1.5)" |
| H-10 | prereg §10.1 l.722-723 | "P1 = projected tier-1 GPU-h on M1 from the speed-test throughput only" | "P1 = projected tier-1 GPU-h on HC-n from the speed-test throughput only" |
| H-11 | prereg §10.1 l.730 | "STOP conditions: cap; balance < 3 GPU-h; two failed restarts; M1 needed by A, B, MT4 or a custody block; headroom …" | "STOP conditions: cap (C's per-instance spend reaches M − T_down, host amendment §2–§3; T_down then pays the teardown); account balance < 3 GPU-h; two failed restarts; a §1 setup check fails; headroom …" |
| H-12 | prereg §10.2 l.735-736 | "**Tier 1 on M1** (9,282 VND/h, LOG l.1109): default 20 GPU-h hard ≈ 186k VND; …" | "**Tier 1 on HC-n** (r_host at rental; 9,282 VND/h [est.]): about 35.5 billed hours including about 4 h of setup, money ≤ 350k VND (≤ 465k under PQ-C2) (host amendment §6)." |
| H-13 | prereg §10.3 l.742 | "C's M1 block queues behind MT4, B's M1 custody block and any A job." | "C's HC-n block is a separate rental; it is rented only after the tier-1 run doc GO and when the §3 solvency rule passes." |
| H-14 | prereg §11 l.756-757 | "GPU=M1 bash scripts/c_pvr/c_pvr_job.sh …" (two lines) | "GPU=HC bash scripts/c_pvr/c_pvr_job.sh …" (same arguments; the env value is fixed by the S10 code read) |
| H-15 | prereg §13 O5 l.787 | "tier-1 GPU host = M1 (spent-test dev sets may not go to a rental) unless Q-custody YES" | "tier-1 GPU host = HC-n (Q-custody′ YES, PI-1104af; host amendment)" |
| H-16 | prereg §14 Q-custody l.803 | "… sit on one dedicated single-tenant rented 4090 …" (open question) | answered row: "Q-custody′ = YES for the tier-1 dev decodes, their datastores and the tier-2 sets on one RTX 3090/3090 Ti (PI-1104af, PI-1104ae). NoCaps-test and OpenViVQA-dev pixels are not covered." |
| H-17 | prereg §15 P6 l.822 | "One tier-1 GPU host (M1) …" | "One tier-1 GPU host class (HC-n) …" |
| H-18 | PINS-A §8 l.541-542 (3fb6725) | "`r_host` (VND per GPU-h) is named in the Q-custody host amendment (prereg §8.3 l.617, one-judge read)" | "`r_host` is recorded in the rental LOG line under the host amendment §2" |
| H-19 | PINS-A §8 l.547 | "P1 must come from a speed test on the named host. M1 is kept only until 18:00 VN 03/11 (PI-1102o); …" | "P1 must come from a speed test on HC-n. M1 was deleted (LOG l.1375); …" |
| H-20 | PINS-A l.683 | "the Q-custody host amendment (`r_host`, money ledger)" | unchanged text; it now points to this file (§2, §3) |
| H-21 | PINS-A §8 l.544-546 (3fb6725) | "every VND billed for the C tier-1 block on the named host, **speed test included**, read from the rental balance lines before and after (house money-gate pattern, LOG l.1164). Idle billed time of that block counts." | "every VND billed for the C tier-1 block on HC-n, setup, selftest, speed test, idle time and teardown included, read as HC-n's per-instance panel 'spent' (host amendment §3; LOG l.1164 form); balance lines are solvency checks only; decoding stops at M − T_down (host amendment §2–§3)." |

Unchanged:
- the laptop as the W25 custody host (§8, l.528-530);
- §8.1 and §8.2;
- M8 never used (l.615-616, now moot);
- every set role;
- the PINS-A §8 cap formula itself. This amendment cites it (§2) and does not change it. T1-REP R-4 changes it, if
  registered.

## 8. Carried, not in this file

- CC-254 N97 (STATE): the next STATE C row must say that tier 1 runs on a 3090 (PI-1104ae), and that W25 ran and was
  committed at cc90c96.
- CC-254 N77 (TextCaps pixel pin): a separate pin and read. §4.2 and §5 depend on it only for the fetch route.

## 9. Rulings needed

| # | from | question | recommended | default if no answer |
|---|---|---|---|---|
| H-J1 | judge | Do §1–§5 meet prereg §8.3 l.617-619, with N89 (datastore rows), N90 (standalone cap citation) and N91 (per-instance spend) closed? | YES | tier-1 GPU block stays NOT RUN |
| H-J2 | judge | Speed-test budget ≤ 1.5 GPU-h (H-9) | YES (CC-254 2.10) | – |
| H-J3 | judge | Tier-2 host coverage now, with O_B gated by the tier-2 prereg | YES (CC-254 2.10) | – |
| H-J4 | judge | Solvency rule: L-before ≥ 350,000 + 3 × r_host + Σ_j R_j | YES | as written |
| H-J5 | judge | Procedural-isolation disclosure | YES (CC-254 2.10) | – |
| PI-B | PI (CC-254 "For the PI"); **answered by PI-1105a (LOG l.1543)**: sequential, C first then B, one 3090 at a time, no top-up, B waits if short | C's block (≤ 350k, at most 465k VND) and B's two 3090s (about 343k VND) together exceed the last balance read (798,488 VND, 03/11). Top up about 300k VND before the second rental, or run the blocks sequentially? | sequentially, in the order the run docs get a GO, plus a top-up before the second | sequential; the second machine is rented only when the §3 solvency rule passes |

## 10. Drafting-touch disclosure

Read:
- CC-254 and CC-254r2 in full; CC-253 MB2 and MB3;
- LOG l.1164, l.1534, l.1536 and l.1538;
- the v1 draft and its sources.

No rental page, provider id or host address was opened or written. No image, caption or label file was opened.
`~/.vsps_sealed` was not touched.

## 11. Change table against v1 (80386f22)

| # | v1 place | v2 change | source |
|---|---|---|---|
| C-1 | §5 "Not covered: … and any other set" | datastore rows added for D-VI, D-EN, D-TC and the A4/A9 helper inputs: ids, demonstration caption text, embeddings, images only if embedded on HC-n. All non-custody, from the final S7 id files, under the §4 rules. "Not covered" now means sets and material not listed. H-2 and H-16 point to these rows | CC-254 N89 (BLOCKING) |
| C-2 | §2 "enters only the T1-REP §9 rule"; §6 "capped by the T1-REP §9 rule" | §2 rewritten to cite the registered PINS-A §8 l.540-543 formula and §5.1 cut order, with the T1-REP §9 / R-3 / R-4 form applying only once registered. PQ-C2 applies in either form. The money stop is grounded in PINS-A §8 l.544-546. §6 cites §2 | CC-254 N90 (BLOCKING), wording as suggested |
| C-3 | §3 "S = L-before − L-P1"; "block total = L-before − L-after"; "balance ≥ 350,000 + 3 × r_host" | C's spend = the panel's per-instance "spent" for each HC-n instance (L-P1, L-final). Balance lines are solvency checks only. L-before ≥ 350,000 + 3 r_host + Σ_j R_j over every other live rental, each named by its LOG line. PQ-C2 solvency is treated the same way. H-11 and H-13 follow | CC-254 N91 (BLOCKING); PI-1104ag; LOG l.1164 |
| C-4 | §1 table | tmpfs row: `df -B1 /dev/shm` ≥ 1.25 × the measured size, else a FAULT; §4.2 "≤ 4 GB" withdrawn | CC-254 N92 |
| C-5 | H-1 | adds "narrows CC-209 Ruling 1(a) (via CC-217r2 B1) for C's §5 sets only" | CC-254 N93 |
| C-6 | §1 CPU row | "or better" made operational (≥ 12 cores / 24 threads, Zen 3 or later, or Intel 2020 or later; otherwise the PI is asked) | CC-254 N94 |
| C-7 | §3; H-4; H-12 | machine-loss re-rental continues one block ledger (sum of per-instance spend; history or an r_host × time bound). H-12 says "about 35.5 billed hours including about 4 h of setup" | CC-254 N95 |
| C-8 | §4.2 "fetched from their pinned source" | T_A and D-TC images only from the laptop copy until the TextCaps pixel pin (N77) | CC-254 N96 |
| C-9 | §2 cut-order note | PI-1104ah Q8 = YES recorded; the new cut order binds only through T1-REP's registration | PI-1104ah (LOG l.1536) |
| C-10 | §9 | H-J2, H-J3 and H-J5 marked as answered by CC-254 2.10; PI-B question added | CC-254 2.10 and "For the PI" |
| C-11 | new §8 | N97 (STATE) and N77 carried, not in this file | CC-254 N97, N77 |
| C-12 | header, VN summary, §10 | v2 status (round 2/3 diff read); sources updated | CC-254 NEXT STEP |

## 12. Change table against v2 (8127874d)

| # | v2 place | v3 change | source |
|---|---|---|---|
| D-1 | §3 | single-home sentence added (r_host, S, block ledger, T_down); T1-REP §9 replaces only the formula and cut order and cites §3 | CC-254r2 N98(b); CC-253 MB2 |
| D-2 | §2 money stop; §3 PQ-C2 line; H-11 | T_down = 1.0 h × r_host pinned in §3. Decoding stops at M − T_down, so the block total stays ≤ 350k (≤ 465k under PQ-C2). The teardown order is stated | CC-254r2 N98(a); CC-253 MB3 |
| D-3 | §7 | new row H-21: PINS-A §8 l.544-546 (balance-line reading) → per-instance spent, balance lines as solvency checks; §2 points to it | CC-254r2 N99 |
| D-4 | header, VN summary, §9 PI-B, §3 | PI-1105a recorded as the answer; the top-up recommendation is dropped; Σ_j R_j = 0 at C's L-before; CC-253, CC-254r2 and PI-1105a added to the sources | CC-254r2 N100; PI-1105a |
| D-5 | §2 | sentence on prereg l.724 / l.726: l.722 delegates to PINS-A, which sets the 37-h reading aside; the PINS-A form governs until T1-REP R-3 | CC-254r2 N101 |
| D-6 | §2 | the S11 run doc applies the fit check against the money left ⌊(M − S − T_down)/r_host⌋, or states a PI question if T1-REP is not registered | CC-254r2 N102 (recommended route) |
| D-7 | header | commit order: this file first, or jointly with T1-REP | CC-254r2 Ruling 6 |
| D-8 | – | N103 is handled in T1-REP v2 (§9 cites host §3 for S and T_down; R-4 is limited to PINS-A l.540-543, and l.544-546 is left to H-21) | CC-254r2 N103 |
