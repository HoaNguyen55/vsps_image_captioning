# C-DIAG: dev-role exploratory prereg for Paper C (ACM TALLIP): filtering retrieved demonstrations with the CC-212 backbones — v1.2

Status: **DRAFT v1.2 for the CC-299r2 round-3 FULL panel (J1, J2, J3 + read-only Codex), IRREVERSIBLE 85. This is the
LAST round: no GO → ESCALATE_TO_PI, nothing committed. Not registered, not committed.** Nothing here has run, been
rented or decoded. No Stage-0 count exists.
v1 = `C_DIAG_PREREG_DRAFT_v1.md` (d6aae3f9) and v1.1 = `C_DIAG_PREREG_DRAFT_v1_1.md` (c472fb82) are kept byte-unchanged
as records.
Written from 2026-11-08T22:38:50Z (`date -u`), at HEAD `1417a8a`, branch `paper-v10`.
Answers: CC-299r2 (NEXT_ROUND 80; `.session_backup/2026-10-13/decisions/CC-299r2.txt` d97ccfd0), R2-W1-R2-W10 and the
NB items of §16; CC-299 (8ea61b11) W1-W11 and N1-N21 stay closed as in v1.1. PI lines on file: **PI-1109a** (Q1-Q9),
**PI-1109b** (Q10 = YES, the gate-only branch), **PI-1109c** (P1 and P2), **PI-1109d** (delegation rule).
Licence: PI-1108g (LOG l.1886) chose fallback B of `C_PIVOT_CHECKPOINT_v1_1.md` §5 B (l.315-323): a dev-only exploratory
diagnostic on already-spent sets, its own prereg and judge read before any GPU, its own capped money block.
Registration = a GO of the round-3 panel plus a gatekeeper commit of these bytes. **The GO fixes every [proposal]
value as written (N5).** No Stage 0, money block or rental happens before that.
Manuscript: the CC-212 manuscript, `manuscript/journal_draft_C/` ("Retrieved or Random Examples? Preregistered In-Context
Captioning in Vietnamese and English"). The title "Verify Before You Borrow" is dropped (PI-1108g Q3; CC-298 Q5).
Label on every output and every row: **`EXPLORATORY (C-DIAG): spent sets re-used in a dev role, in-sample, no
confirmatory claim`**.
Every estimate is AI opinion, marked [est.]. Values the panel fixes are marked [proposal]. Tags such as `[W4]` mark
where a CC-299 item is closed and `[R2-Wn]` where a CC-299r2 item is closed; the closure table is §15 and the
change table §16.

---

## 0. Sources read, and drafting touches

**v1 sources** (v1 §0) are carried. **Added in v1.1, read in full:** CC-299.txt (8ea61b11); the four round-1 reports
(J1, J2, J3, `manuscript/reviews/C_DIAG_codex_read.md` 4a77f897); LOG l.1887-1891 (PI-1108h, OPS-1108d-topup,
PI-1108i, CC-299, PI-1109a).
**Added, read in part:** `C_META_REVIEW.md` (595019fb) l.49-54, l.79-81; `06_results.md` (e4ff1603) l.49-59, l.83, l.89;
`11_supplement_registered_rows.md` (95d2ad86) l.229-244, l.553, l.608, l.762; `AMENDMENT_HOST_3090_DRAFT_v3.md` (e9c04955,
committed 5d6f5ca) §4-§5 and H-1 (l.241); `B_RUN_DOC_v1_1.md` (90240f83) l.85-95, §12.3 (l.749-770); LOG l.1530
(PI-1104af); `scripts/c_test/ctest.py` l.270-290; `scripts/c_test/c_test_chain.sh` (bbc92788) l.18, l.130-143;
`scripts/c_test/score_t.py` (de942942) l.130-175; `scripts/c_stage1/score.py` l.116-124; `scripts/c_pvr/c_pvr.py`
l.455-535, l.587-690; `scripts/c_pvr/c_pvr_score.py` (7f352276) l.115-130, l.246-264, l.600-700;
`T1_ANALYSIS_APPENDIX_v1_1.md` §2.
**Data touches in v1.1 (no caption text opened or printed):**
- sha256 only: `.session_backup/2026-10-26/c_test/staging/xm_test2500_data.json` (4779edd0) and its `.sha256` list
  (9ae7c0ac); `data/datasets/openviic/uit-openviic-annotation-dev.json` (2a68a3eb); the KTVIC and OpenViIC train
  annotation files (72ee9b57, d757520e); the eight CC-212 `preds.json` files of Appendix A.
- File names only: `.session_backup/2026-10-26/c_test/staging/`; `.session_backup/machines/M3/root/outputs/c_test/runs/`
  and `c_stage2/runs/`; `~/s11pull_1107/` and `final/c_pvr_out/out/` (a targeted path, not a glob); the
  `SHA256SUMS_tier1` lines of the two `xm3600_vi.PVR-*.jsonl` records (sha only).
- No sealed path, no `t2pool_*`, no NoCaps / TextCaps / Open Images test file, no COCO annotation file, no find over
  `$HOME`.
- **Added in v1.2, read in full:** CC-299r2.txt (d97ccfd0); the four round-2 reports; LOG lines PI-1109b, PI-1109c,
  PI-1109d, CC-299r2. **Read in part:** `B_RUN_DOC_v1_2.md` (6524845490e633000296658abc22b88180439e8537b3b7274c8af70fc6143bd6) l.403-408
  and §12.3 step 2 (l.851-852); `05_preregistration_and_analysis.md` l.12, l.37; CC-298.txt l.44, l.49-50, l.72;
  LOG l.1763 (two tokens only: the 8-hex manifest prefix and the build path); S11 v1.3 l.17. No new data file was
  touched in v1.2, and no directory was listed.
- **NGRAM scan (coordinator's request):** `ngram_scan_cen.py` (C_pass3 snapshot) was run on this file. It loads
  every `data/datasets/{ktvic,openviic,uitviic}/*.json` and the Karpathy COCO file into memory, KTVIC and OpenViIC
  test annotations (confirm halves) included, and prints counts only. No text was printed. This is the house
  gatekeeper scan, and it is disclosed because §2.3 bars C-DIAG code from those files.

---

## 1. Question and label

### 1.1 The two questions
- **Q-D1 (verifier).** Does a stronger verifier separate present from absent objects in the retrieved demonstrations?
  "Stronger" means the CC-212 backbones, Qwen2.5-VL-7B and InternVL3-8B, in place of the tier-1 mBLIP-BLOOMZ-7B,
  which recorded κ = 0.007, a "no" share of 98.7 % and a SUPPORTED share of 2.2 % on present objects (CC-298 item 7,
  l.59-60), on a different sample (§4.3 note).
- **Q-D2 (filtering).** If a verifier passes the validity gate (§4), does filtering the CC-212 retrieved demonstrations
  with it change object factuality (P_obj^VI, the tested family) and caption quality (CIDEr-VI, a harm guard)? The
  comparisons are against unguarded unfiltered retrieval (`ret`), random examples (`rand`) and a count-matched random
  removal (`ctl`).

### 1.2 Label and scope (binding)
- **[W6] Role of the sets.** XM-test2500 was scored once, for the registered CC-212 test (XM-a, XM-b;
  `04_data_and_splits.md` l.16). C-DIAG re-uses it in a dev role, exploratory and in-sample, under the binding ledger
  (PORTFOLIO l.191, "XM3600 (all)" dev-only spent). It is never called "development images" or a dev set.
  - **C_META_REVIEW l.81** ("None may re-score OpenViIC test, XM-test2500, …") is read as CC-299 Ruling 3 reads it:
    it bars a test look and any confirmatory or registered-contrast claim on XM-test2500. It does not bar this
    exploratory dev-role re-use. The precedent is CC-298: tier 1 decoded all of XM3600 as dev.
  - C_META_REVIEW §2 item 4 (l.54: "never re-score a used test set with a published scorer: that would be a second
    look") is met the same way. No C-DIAG number re-states, replaces or sits beside a registered CC-212 XM-test2500
    contrast (§5.3, §11 row 9).
  - **Ruling 3 stands** (CC-299r2 Ruling 2: confirmed by all three judges, on the condition that §5.3 computes no
    `ret − rand` contrast on any metric or set; v1.2 drops it, **[R2-W4]**). C_META_REVIEW l.81 covers its §4 items
    X1-X5; X3 is the registered `ret`-vs-`rand` object-precision test, and C-DIAG computes no such number.
- **No confirmatory claim**, no PASS, no "confirmed", no test look, and nothing here licenses one.
- **[R2-W9] Never on the critical path (PI-1109c P1).** C-DIAG never holds up the CC-212 revision or the TALLIP
  submission. If it is late, C proceeds without it, and the C-DIAG subsection is left out.
- **The headline stays CC-212's registered rows:** OpenViIC P1 +4.49 [3.52, 5.57] PASS; COCO P1-EN +3.08 [2.08, 4.03]
  PASS; XM-a +0.70 [-0.45, 1.97] FAIL; NoCaps val +1.73 [0.94, 2.50] FAIL (STUDY_BRIEF_C l.16, l.20, l.22-23;
  CC-212.txt l.40-41).
  - C-DIAG rows never appear in the title and never carry a headline sentence.
  - **[N12]** Main text: at most one table and one paragraph (meta-review item 13). The rest goes to the supplement.
  - Abstract: at most one clause, labelled exploratory, with no number.
- **Method word: "filtering"** in every claim (PI-1108g Q3; CC-298 Ruling 6; T1-REP v4 §1 l.90).
  - **[N9]** In the paper the model role is called the **"demonstration filter"**, not "verifier". CC-212's
    `03_method.md` l.40/58 already uses "verifier" for the Qwen3-VL output guard. "Verifier" stays in this prereg only,
    as the role name.
- **Not a PVR rescue.** There is no A8 arm and no PVR − A8 claim, and no tier-1 rule is re-decided.
- **Same model, two roles (limitation, stated in the paper).** Each backbone filters with itself (PI-1109a Q1). The
  filter and the captioner are the same model, so no sentence implies an independent check.
- The CC-212 post-decode object guard deletes objects from the model's own caption. C-DIAG filters input
  demonstrations before decoding. The paper keeps the two apart.

### 1.3 [W11] What the group has already seen on these sets, and what to expect
These results are known before C-DIAG runs. **Paper scope:** the CC-212 rows (XM-b, Table S8, the OV-dev-B guard, Table
S12) are also cited in the paper's C-DIAG paragraph. The tier-1 rows (R2-W6 (a)) are disclosure in this prereg only:
they span all of XM3600, XM600 included (`04_data_and_splits.md` l.29), so any mBLIP number in the paper comes only
from the §4.5 recompute on the 3,000 ids.

| seen result | value | source |
|---|---|---|
| XM-b: verified object precision, `ret` vs `zs`, pooled over both backbones (XM-test2500) | +0.59 [−0.31, 1.54] | `06_results.md` l.52 |
| neighbour-only object precision of `ret` on XM-test2500 (OI labels) | Qwen 92.82 [89.03, 96.28], 195 mentions, 7.0 % of images; InternVL3 100.00, 16 mentions | `11_supplement_registered_rows.md` l.229, l.239-241 (Table S8) |
| the CC-212 guard hypothesis on OV-dev-B: a registered negative | pooled precision +2.91 [0.46, 5.31] at a stripped CIDEr-D cost of −4.01 | `06_results.md` l.89 |
| InternVL3's CC-212 output verifier (Qwen3-VL-8B), AUROC of s on XM-test2500 `ret` items, τ = −∞ | 0.552 (1,063 items), not registered | `11_supplement_registered_rows.md` l.553, l.608 (Table S12) |
| **[R2-W6 (a)]** tier 1 on all XM3600 (which contains XM-test2500), **mBLIP captioner, tier-1 demonstrations (D-VI memory)**: P_obj^VI of A1 (top-k retrieval) | 83.380 | CC-298.txt l.72 |
| same: A12 oracle filter (absent objects removed by the labels) | 94.256; headroom A12 − A1 = 10.877 | CC-298.txt l.72, l.44 |
| same: PVR − A1 (demonstration filtering with mBLIP) | +8.62 [6.25, 11.05] | CC-298.txt l.49-50 (item 4) |
| same: A1 − A0 (retrieval vs zero-shot) | −7.34 [−9.66, −5.04] | CC-298.txt l.50 (HW-2) |

- **Headroom statement.** **[R2-W6 (b)]** The two captioners differ.
  - **mBLIP (tier 1):** retrieval lowered P_obj^VI by 7.34 points below zero-shot, and the oracle filter had 10.9
    points of headroom. That is the case where demonstration filtering can matter. PVR rose +8.62 over A1, but its
    verifier did not discriminate (κ = 0.007, CC-298 item 7), and PVR-drop emptied 72.2 % of the demonstrations on
    XM3600 (`score_tier1.json` `emptied_demo_share` 0.722). So the gain cannot be credited to discrimination, and the
    copy-channel split was not identified (C-M1 NOT_IDENTIFIED, CC-298 Ruling 4).
  - **CC-212 backbones:** retrieval barely moved object precision on XM-test2500 (XM-b, `ret` vs `zs`: +0.59, CI
    includes 0). For these backbones only, the objects that `ret` captions borrow from neighbours are few (Qwen: 195
    mentions over 2,500 images) and mostly correct (about 93 %). Table S8 reports `ret` **at the frozen τ**
    (header l.229): Qwen at τ = −∞ (unguarded, as in C-DIAG), InternVL3 at τ = 0.10 (guarded, unlike C-DIAG's
    unguarded decodes), so the InternVL3 row (16 mentions) is not the C-DIAG condition.
  - For the CC-212 backbones, removing every wrong borrowed object would move pooled P_obj^VI by well under 1 point
    [est.].
  - **The expected XM-test2500 outcome is S6, "no change shown".** The informative parts are Q-D1 (the gate), the
    demonstration-side odds (§4.4) and the OV-dev-B CIDEr-VI cost.
- **[W11, R2-W6 (c)] SESOI rationale.** SESOI_P = 2.0 points of P_obj^VI is **C-DIAG's own choice**, fixed before any
  C-DIAG data. No earlier study used it for precision: CC-212's +2.0 is in CIDEr-D (`05_preregistration_and_analysis.md`
  l.12, l.37), CC-212's precision rule was a −1.0 non-inferiority floor (`06_results.md` l.52), and tier 1's
  δ_C = δ_R = 2.0 are harm margins. The reasons for 2.0:
  1. 2 points of pooled precision is about one wrong object mention in 50 verified ones, a change a reader of a
     captioning paper would notice; a smaller gain would not change how the CC-212 result is read.
  2. It lies between the floor (1) and the tier-1 value (2.719) of the registered tier-1 SESOI rule
     max(1, 0.25 × headroom), without being computed from C-DIAG data.
  3. A smaller SESOI chosen because the CC-212-backbone headroom is small would be a threshold set to fit the
     expected data.
  4. A drop in mentions can raise P_obj trivially. The §6.4 labels and the count-matched column (§3.3, N20) report
     that route instead of rewarding it.
- **[Q8] Stage-0 headroom floor** (PI-1109a Q8; fixed now, before any count):
  - **The measure, per backbone b, on XM-test2500.** c_b = N_A / (N_A + N_P), where:
    - the units are the mapped object propositions (`decompose_vi` obj kind) in ranks 1..k_b of the CC-212 `ret`
      demonstrations (k = 8 for Qwen, 4 for InternVL3);
    - each is counted once per demonstration and class, as in T1-REP v4 §1;
    - status is that of (query image, class) by `status()`, with unknown excluded.
  - **Floor: c_b ≥ 0.10** [proposal].
  - **Reason for 0.10:**
    - It is about half the in-situ absent share seen in tier 1 on XM3600 (~19 %, J1 N9).
    - Below 10 %, the T1-REP v4 §2 identity bounds what any filter can do to the demonstrations. A strong filter
      (ρ = 0.8, φ = 0.1) moves c from 0.10 to about 0.024, so about 8 wrong object phrases per 100 are removed
      **[R2-W10 (b)]**.
      Most images then have nothing wrong to remove.
  - **Consequence:**
    - If c_b < 0.10, backbone b's Stage-2/3 blocks (both sets) are dropped before rental and reported as a headroom
      result, with the value.
    - **[R2-W1 (a)] Gate-only branch (PI-1109b).** Its trigger is **exactly: both backbones have c_b < 0.10** (the
      floor only). Then the gate runs alone under the gate-only rules of §8.3 (cap, solvency), §8.4 (delete), §9 and
      Appendix C (material).
    - **Any other cause of an empty main run means no rental:** one backbone dropped by the floor and the other by the
      VI-script precondition (§14 item 7), or both by the precondition.
  - **[NB-7]** The floor is probably not binding (tier 1 saw about 19 %); the binding limit is on the caption side
    (Table S8). It is kept, with the cut order, as written.
- **[NB-8] Expected value.** The likely result is the gate verdict, "no change shown" (S6) on XM-test2500 and a
  descriptive OV-dev-B CIDEr-VI cost; spend from about 25-30k VND (gate fails or gate-only) to about 187k VND (full run)
  [est., J2].
  - Computed on the laptop at Stage 0 from labels that never go to the host. Only c_b and the counts are printed.

---

## 2. Data ledger

### 2.1 Sets already spent by C (may be used)
Ledger: `manuscript/directions/PORTFOLIO_3Y_2026-10-29.md`, working tree 14d2ea22. It differs from the HEAD blob 2cb793d6
only at l.96, l.145 and l.177, so every cited line is equal at HEAD.

| set | size | spent by | source (file::line) |
|---|---|---|---|
| XM3600, all images | 3,600 | A (XM600 test), CC-212 (XM-dev500, XM-test2500), C tier 1 (all) | PORTFOLIO l.191, l.193; CC-298 J2-W6 l.141-142 |
| **XM-dev500** | 500 | CC-212 stage B secondary | `04_data_and_splits.md` l.13, l.25-27; `c_stage2/ex_xm_dev500.json` (9a79b97d) |
| **XM-test2500** | 2,500 (5,108 VI refs) | CC-212 test (XM-a FAIL, XM-b) | `04_data_and_splits.md` l.16, l.27-29; STUDY_BRIEF_C l.22; CC-212.txt l.40-41; `c_test/ex_xm_test2500.json` (242b30a2) |
| **OV-dev-B** | 925 | CC-212 stage B one-look gate | `04_data_and_splits.md` l.12; `2026-10-22_c_stage2/PREREG.md` l.103; `c_stage2/ex_ov_dev_b.json` (072b17d1) |
| OV-dev-A | 911 | CC-212 stage A | `04_data_and_splits.md` l.11 |
| KTVIC dev299 | 299 | CC-212 stage A | `04_data_and_splits.md` l.10 |
| OV-test / KTVIC-test explore halves | 1,020 / 286 | CC-212 test (whole OV-test), C tier 1 G1 | CC-298 l.47, J2-W6 l.141; PORTFOLIO l.191 |
| COCO Karpathy test / KT-C | 5,000 / 3,907 | CC-212 P1-EN / C tier 1 EN arm | STUDY_BRIEF_C l.20; PORTFOLIO l.191, l.193 |
| NoCaps val | 4,500 | CC-212 S-NC | STUDY_BRIEF_C l.23; PORTFOLIO l.191, l.193 |
| Flickr30K Karpathy test | 1,000 | C-T3 (E3, CC-212) | CC-212.txt l.31-33 |

**[N14]** PORTFOLIO l.171 still lists Flickr30K test as "unscored". That stale entry needs its own ledger line, not this
prereg.

### 2.2 Sets used by C-DIAG (PI-1109a Q4)

| role | set | why |
|---|---|---|
| validity gate (§4) | **XM-dev500** queries, by the §4.1 ladder | existing OI human labels; disjoint from XM-test2500 |
| full run: P_obj^VI (tested family) and CIDEr-VI | **XM-test2500** (dev-role re-use, §1.2) | OI labels and VI references |
| full run: CIDEr-VI (harm guard, descriptive) | **OV-dev-B** | in-domain; no OI labels |

Not used, although spent:
- **The OV-test and KTVIC-test explore halves.** Their reference files also hold the unspent confirm halves (CC-298
  J3-N6, l.152-153).
- **All-of-XM3600 and XM600.** The manuscript states that a full-XM3600 result cannot exist for this study
  (`04_data_and_splits.md` l.26, l.29).
- **OV-dev-A and KTVIC dev299:** they add cost and no label type.
- **English sets (COCO, KT-C, NoCaps val, Flickr30K): no English row, for cost** (PI-1109a Q5; tier 2 is barred,
  CC-298 Ruling 7) **[N11]**.

### 2.3 Unspent and untouched (binding)
No decode, no reference read, no label read, no feature pass and no open for any of these:
- **The confirm halves:** KTVIC test (272) and OpenViIC test (981) (CC-298 Ruling 7, l.94-95).
- **NoCaps test** (PORTFOLIO l.168, which also governs its overlap handling **[N19]**), **OpenViVQA dev** (l.169),
  ViTextCaps test and VieCap4H private test (l.167, l.170), and every other test split in PORTFOLIO §2.3.
- **XM600:** no XM600 reference is read (§2.4 W5). XM600 OI label rows are handled as stated in §2.4.
- No ledger owner changes.
- **[W10] How this is enforced:** C-DIAG code opens files only from the allow-list of Appendix B, each by (path,
  sha256). Any other open is a FAULT.
  - **Order of checks.** A path that matches an Appendix B entry (path and sha) is accepted. Only paths **not** on the
    list reach the deny backstop. The backstop refuses, with a FAULT naming the pattern, any of these exact basenames
    or prefixes: `test_data.json`, `uit-openviic-annotation-test.json`, `t2pool_*`, `nocaps_test*`,
    `image_info_test*`, `instances_*.json`, `captions_*.json`, and **any path with a `.vsps_sealed` component**
    **[R2-W7]** (CC-299 W10). No Appendix B input lies under `.vsps_sealed`, so the prefix refuses no registered input.
  - The backstop is name-exact on purpose: a broad `*test*` pattern would also refuse registered inputs such as
    `ex_xm_test2500.json` and the CC-212 `ct_*_xm_test2500-*.preds.json`.
  - The selftest asserts that every Appendix B path passes the backstop, that both stray copies are refused, and that a
    `~/.vsps_sealed/…` path is refused **[R2-W7]**.
  - At least two stray repo copies of `ktvic/test_data.json` exist outside `data/` (J3 W4). The allow-list makes them
    unreachable whatever their path.
  - Both checks are tested in `test_c_diag.py` and verified at the code read.

### 2.4 Gold, references and labels
- **[W5] Branch (a) holds: a pre-filtered XM-test2500 reference file exists.**
  - The file is `.session_backup/2026-10-26/c_test/staging/xm_test2500_data.json`, sha256 **4779edd0e57057b50ff5710f4a78f876a4815f0a74348a83357073f179b1eafa**.
  - It was written by CC-212's `ctest.py xm-subset` (l.275-290; chain `c_test_chain.sh` l.135-136). It equals the
    `ann_sha256` of `c_test/host_xm.json`. It holds the 2,500 XM-test2500 keys and their annotations, with the release
    sha inside.
  - C-DIAG's CIDEr-VI producer reads only this file for XM. **`full_data.json` is not on the allow-list**, so no
    XM600 or XM-dev500 reference is read. A Stage-0 check refuses the file unless its sha equals 4779edd0, it has
    2,500 keys, and its `release_sha256` equals 101d24ad.
- **OV-dev-B references:** `data/datasets/openviic/uit-openviic-annotation-dev.json`, sha256 2a68a3eb (= the release
  sha of stage-2 PREREG l.61). It holds OV-dev-A ∪ OV-dev-B, both spent. The producer keeps the 925 OV-dev-B keys; the
  911 OV-dev-A entries are parsed and dropped, never scored or printed.
- **Object gold:** the existing Open Images V7 human-verified labels for XM3600 (`data/xm3600/oiv7_labels.json`
  bac3953a), the 69-class map `vi_oiv7_map.json` (27f2b1ca) and `status()` of `scripts/xm3600_oiv7.py` (9a79403f)
  (tier-1 prereg §3.1, l.285-295).
  - `oiv7_labels.json` keys every labelled XM3600 image, XM600 included. No pre-filtered subset exists. So **one
    Stage-0 laptop step** (`c_diag.py label-subset`) parses it once and writes the XM-dev500 ∪ XM-test2500 subset,
    pinned by sha in the Stage-0 LOG line; the step asserts its keys ⊆ XM-dev500 ∪ XM-test2500 **[NB-3]**. **XM600 rows
    are loaded once to write the subset, and never scored or printed** (the CC-298 J3-N6 disclosure form). CC-212's verified scorer did the same (`score_t.py` l.152-154).
    Every later step reads only the subset.
- **No new gold labels. No AI label is evidence, ever.** Verifier outputs are measured against existing labels and
  never become labels.
- **Label custody.** Labels, statuses and label-derived masks never go to the GPU host, and there is no oracle arm.
  - One disclosed exception: the gate unit file (§4.1) holds no status, but its membership is label-derived (known
    status only, balanced).
  - The CC-212 sentence "those labels never reached the GPU server" (`03_method.md` l.87) stays true of CC-212's
    runs. The C-DIAG paragraph states the exception in one line.

---

## 3. Instrument and metrics

### 3.1 Demonstrations and propositions
- **Retrieval = CC-212's frozen exemplars, unchanged:** the `ret` and `rand` id lists of the three ex files (8 per query
  for `ret`). Shown caption per cluster: `decode_icl.shown` (l.176-178). Qwen takes `ret[:8]` in "first" order and
  InternVL3 `ret[:4]` in "last" order (`exemplar_ids` l.181-191; `frozen_config.json`).
- **Propositions:** `c_pvr.decompose_vi` (a503644a), on the laptop, over the shown captions of ranks 1-8.
  - Kinds are **obj** and **text**. An obj proposition exists only for a mention whose noun is a key of
    `vi_oiv7_map.json` (`_decompose_vi_one`, the `if noun in keys` filter), so **every obj proposition is mapped**.
  - Its span is every token since the previous span in the same chunk, then the mention, then trailing colour and
    size words (`build_props`). So it can carry a verb, numeral or relation.
  - A decomposition failure leaves that demonstration unfiltered. Failures are counted and reported per arm.

### 3.2 Verifier call (identical in the gate and the full run)
- Prompt `scripts/c_pvr/prompts/ver_3way.txt` (bcb92308) via `c_pvr.ver_prompt` / `proposition`, byte-identical to
  tier 1. The query image and the prompt go through the model's chat template. Greedy decoding,
  `MAX_NEW["verify"] = 8`, batch 1, bf16.
- Labels come from `c_pvr.parse_label`: yes → SUPPORTED, maybe → UNCERTAIN, no → REJECTED. A parse failure is
  UNCERTAIN, with no second call.
- **[W9 (a)] Why choice (a), not (b).**
  - (a) is a design rule fixed before any data exists, and it also cuts verifier calls, since text propositions are
    no longer asked.
  - (b) would make L1 depend on an in-situ κ computed from XM-test2500's labels. That would be a gate on the very set
    that is scored, set alongside its outcome.
- **[W9 (a)] Only obj propositions are asked.** They are asked in rank order, up to `CAP = 32` calls per image
  (`c_pvr.verify`). Text propositions are never asked and never removed.
- **Removal rule (fixed): remove REJECTED obj propositions only.** UNCERTAIN and parse failures stay, so a model that
  fails to parse cannot empty the prompt (the tier-1 A8 lesson).

### 3.3 Metrics (per arm, per set)
- **CIDEr-VI**, by the pinned route of `CIDER_VI_PIN_v1_1.md` (§2, §4, §6): NFC `CP.clean`, then RDRSegmenter (jar
  and model files re-hashed on every call), then lower-casing; `protocol_pilot.Cider` (6aee4282), one object per set,
  DF = that set's scored references; ×100.
  - The **as-written** column is the one the harm guard uses. The stripped column is reported beside it. If they give
    different §6.4 CIDEr states, the state carries "punctuation-dependent".
  - The paper notes that CC-212's tables decided on stripped CIDEr-D.
- **P_obj^VI** (XM-test2500 only), as in tier-1 prereg §3.1-§3.2:
  - mentions from `objects_in(caption, raw_tone=False)` on the 69 mapped classes, each once per caption;
  - P_obj^VI = present / (present + absent), pooled, with unknown out of the denominator;
  - P_obj^VI,wrong = present / (present + absent + unknown);
  - R_obj^VI = verified-present pairs mentioned / verified-present pairs;
  - CHAIR_i^VI = 1 − P_obj^VI;
  - the scorer asserts that `RESCAP_RAW_TONE` is unset.
  - **[N15]** P_obj^VI has the same form as CC-212's XM-b "verified precision": present / (present + absent) on the
    mapped classes, against the same OI labels. CC-212 called the matcher through `guard.objects_in`. The code read
    confirms that both calls give the same mentions, or the paper says the two are not interchangeable.
- **[N20] Count-matched precision ΔP_cm(filt vs ret)**, descriptive, XM only. It is CC-212's formula (supplement l.762)
  with `ret` in the place of `zs`: k_i = min(|M_i(filt)|, |M_i(ret)|), counted against the OI labels.
  - It is reported because object precision moves with caption length. The companion study's verbosity result is
    cited as the reason for the tool, not as a claim of this paper.
- **VI-script guard** (tier-1 §5.7(b), l.442-446): the share of captions with at least one Vietnamese-specific letter
  after NFC. Threshold **0.95 per arm**.
- **Empty captions:**
  - an empty caption scores CIDEr-VI 0, contributes no mention and **counts as non-Vietnamese** in the VI-script share;
  - the empty share is reported beside the VI-script share;
  - an empty share > 0.05 flags the arm, and its P_obj^VI is printed only with its mentions per caption.
- **Mention-share flag:** |verifiable-mention share(filt) − share(ret)| > 5.0 points is flagged (the tier-1 §5.7(a)
  form). It is not a gate.
- **Fallback share:** the share of images where every demonstration was emptied, so the prompt fell back to zero-shot
  (§5.1). It is reported per arm.

---

## 4. Verifier validity gate (Stage 1, before the full spend)

The gate exists because the tier-1 verifier failed silently (CC-298 item 7). It is staged and mechanical, and every
threshold, ladder rung and denominator is fixed here.

### 4.1 [W2] Sample and supply ladder (laptop, Stage 0; frozen by sha before any GPU step)
- **Unit.** One **bare** obj proposition in a CC-212 `ret` demonstration of an **XM-dev500** query. Its single mapped
  class has (query image, class) status present or absent by `status()`. Unknown units, and units mapping to two or
  more classes, are out.
- **Bare (fixed).** Every segmenter token outside the mention is in {"một"} ∪ the keys of `lexicon.CLASSIFIERS`
  (fbc945f2), after `norm_tone` and lower-casing.
  - **[N8]** An RDR token joined by "_" is split into its syllables first, and each syllable must be in that set.
  - Bare means "một con chó", "chiếc xe". A numeral, plural marker, colour, size, verb or relation makes a unit
    non-bare: a correct verifier may answer "no" to it on a present class.
- **Order.** Ascending sha256 of `f"{query_id}|{rank}|{prop_index}|{class}|c_diag_gate"`.
- **Ladder (fixed now; Stage 0 stops at the first rung where both cells reach 150):**

  | rung | demonstration ranks | at most per query and status |
  |---|---|---|
  | (a) | 1-4 | 3 |
  | (b) | 1-8 | 3 |
  | (c) | 1-8 | 5 |

  - At the chosen rung, walk the order and take units under the per-query cap until each cell holds 150.
  - If rung (c) is reached and a cell holds 100-149 units, that cell takes all it has.
  - **Fewer than 100 in either cell after rung (c) = FAULT, and C-DIAG ends before any rental** (CC-299 W2). No
    sample is chosen after a count, and nothing goes back to a judge for re-choosing.
  - Stage 0 prints the bare-unit supply per rung and cell (counts only, no status by unit).
- **Disclosure [W9, J1 N11].**
  - The gate is a balanced, bare-only subsample, so it validates a narrower proposition form than `filt` acts on.
    `filt` also removes compound obj propositions.
  - At rungs (b) and (c) it includes ranks 5-8, which InternVL3 never sees in its run.
  - The full run's in-situ table (§4.4) covers every obj proposition, descriptively.
- **The host gets** (query id, rank, proposition index, proposition text) in sha order, with no status (§2.4).
- **Image-blind pass:** the same calls with no image, through the model's text-only chat path (as CC-212
  `hf_verifier`, guard.py l.178-205).

### 4.2 [W3] Measures (laptop, after the labels are pulled)
Let N_P and N_A be the present and absent units sent. Each unit gets one label in {SUPPORTED, UNCERTAIN, REJECTED}; a
parse failure is UNCERTAIN and is also counted on its own.

| measure | numerator | denominator |
|---|---|---|
| no-rate on present (V2) | REJECTED among present | **N_P** (UNCERTAIN and parse failures included) |
| no-rate on absent (V2) | REJECTED among absent | **N_A** (likewise included) |
| SUPPORTED share on present (V3) | SUPPORTED among present | **N_P** (likewise included) |
| UNCERTAIN share (V4) | UNCERTAIN, parse failures included | **N_P + N_A** |
| κ (V1) | Cohen's κ on the 2 × 2 {REJECTED, SUPPORTED} × {absent, present} | units labelled REJECTED or SUPPORTED only; UNCERTAIN excluded and counted beside it |
| κ_blind (V5) | the same κ on the image-blind labels | as κ |

- **Degenerate κ.** κ is undefined when a row or column of the 2 × 2 is empty, or p_e = 1. **Undefined κ = V1 FAIL.**
  **Undefined κ_blind is treated as 0** for V5.
- **κ CI.** Percentile bootstrap over query-image clusters: resample XM-dev500 query ids with replacement and take all
  their units, B = 10,000. `rng = numpy.random.default_rng(20261109)`; `idx = rng.integers(0, n_q, size=(B, n_q))` over
  the sorted query ids, where **n_q = the number of gate queries with at least one unit** **[NB-1]**.
  - A replicate whose κ is undefined is dropped and counted.
  - **More than 1 % dropped = FAULT.** That verifier then gets no verdict, does not proceed, and is reported as
    "gate FAULT (degenerate κ)".

### 4.3 PASS rule (per verifier; all five must hold) [proposal]

| # | condition | tier-1 value: **different sample (in situ, all units, ~19 % absent), not comparable [N7]** |
|---|---|---|
| V1 | κ defined, κ point ≥ 0.40 **and** κ 95 % CI lower bound ≥ 0.20 | 0.007 [0.004, 0.010] |
| V2 | no-rate on present ≤ 0.40 **and** no-rate on absent ≥ 0.40 | "no" share 98.7 % overall |
| V3 | SUPPORTED share on present ≥ 0.50 | 2.25 % |
| V4 | UNCERTAIN share ≤ 0.20 | 1 "maybe" in 17,583 calls |
| V5 | κ − κ_blind ≥ 0.20 (κ_blind undefined → 0) | not measured |

V2-V5 use point values. The tier-1 column is for the prereg only and never enters the paper (J2 N5).
- **Pass:** that verifier filters its own backbone's demonstrations in Stage 2, if its backbone passed the headroom
  floor (§1.3) and the VI-script precondition (§14).
- **Fail:** that verifier stops. Its gate table is reported in full, and its backbone gets no C-DIAG arms. **Nothing is
  tuned.**
- **Both fail:** C-DIAG ends after Stage 1, and the host is deleted at once.
- **[R2-W1 (d)] Gate-only branch:** there is no Stage 2/3 whatever the verdict. The host is deleted right after the gate
  pull, before the verdict is computed; the verdict is computed on the laptop after the delete, so no wait is billed.
  The main branch keeps its rules (a PASS continues to S2).
- **Verdict.** `c_diag_score.py gate` prints the verdict, which is recorded by sha in an OPS line. The coordinator only
  relays it; no judgement enters.
- **[N2] Wait bound (main branch).** If no verdict is relayed within 1.0 h of the gate pull, the host is pulled and
  deleted. A later
  re-rental needs a fresh §8.3 check, and its cost counts against the same cap.

### 4.4 In-situ table (full run, descriptive, never gating)
On XM-test2500, for every verifier that runs:
- the T1-REP v4 §1 3 × 3 table (with unknown) over every obj proposition asked, with the §4.2 measures;
- the T1-REP v4 §2 odds identity: ρ, φ, OR_filt, OR_ctl, and OR_filt / OR_ctl with an image-bootstrap CI.

Under W9 (a), `ctl` is count-matched on the same obj units. **[R2-W10 (d)]** OR_filt / OR_ctl is the exact selectivity
ratio of T1-REP §2 **only for images with zero cap hits**: `a7_masks` draws among every obj proposition of a
demonstration, including those beyond CAP = 32 that `filt` never asks (NB-4). The ratio is reported on all images and,
beside it, on the zero-cap-hit images; the cap-hit count is reported.

### 4.5 [Q6, R2-W5] Tier-1 mBLIP verifier table, recomputed post hoc (CPU, no GPU; PI-1109a Q6)
- **Command:** `scripts/c_diag/c_diag_t1table.py`, laptop, coordinator-run. **[R2-W5 (a)]** It uses the same `allow`
  function as C-DIAG, with **its own exact (path, sha256) list of nine data inputs**; any other open is a FAULT, and
  the §2.3 deny backstop applies.

  | # | input | sha256 |
  |---|---|---|
  | T1 | `~/s11pull_1107/final/c_pvr_out/SHA256SUMS_tier1` | 7cf129106dd0ef2c382f4a9a4fd480295e5fc36e3e81b6522439370d500850e8 |
  | T2 | `~/s11pull_1107/final/c_pvr_out/out/xm3600_vi.PVR-drop.jsonl` | 8bdc38ec2b89078040c677abbbaec29258cb446b1d916cab1bbd606c6bfaab31 |
  | T3 | `~/s11pull_1107/final/c_pvr_out/out/xm3600_vi.PVR-keep.jsonl` | ca7a9a208ab8f3c35c12c633a67cb065a13207343b60c71afd3c570fb62b6450 |
  | T4 | `~/c_pvr_h4_1107/MANIFEST.sha256` | 4849a08f1fc384f1901fd294950f9ea20a5622879838c4a5ecac73cec62c3efe (= TMAN) |
  | T5 | `~/c_pvr_h4_1107/manifest/xm3600_vi.json` | its line in T4; must begin **f81323d1** (LOG l.1763) |
  | T6 | the §2.4 label subset | its Stage-0 sha |
  | T7 | `manuscript/prereg/2026-10-22_c_stage1/lists.json` | 5c479f03… (v1 Appendix A) |
  | T8 | `data/xm3600/vi_oiv7_map.json` | 27f2b1ca… |
  | T9 | `data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv` | 84a4373a… |

  Code imports are pinned by `scripts/c_diag/SHA256SUMS`.
- **[R2-W5 (b)] Narrow manifest check.** The step does **not** call `c_pvr_score.manifests()`, which loops over every
  `G.SETS` entry (c_pvr_score.py l.113-127). It checks sha(T4) = TMAN, reads only the `manifest/xm3600_vi.json` line
  of T4, asserts that sha(T5) equals that line and begins with f81323d1 (the prefix recorded at LOG l.1763, OPS-1107c-h4
  build line), and writes the full sha into its record.
- **[R2-W5 (c)] Path and custody.** The build is `~/c_pvr_h4_1107` (S11 v1.3 l.17; LOG l.1763: "out ~/c_pvr_h4_1107
  (0700 ext4)"). It is **not** under `~/.vsps_sealed`; the v1.1 words "sealed laptop build" were wrong. S16 read it
  through `safe()` with no ACCESS_LOG hand row, and the same holds here: no hand row is due. The step is still run by
  the coordinator, not by a subagent, because T5 holds train caption text. No text is printed.
- **[R2-W5 (e)] Licence and record.** PI-1109a Q6 licenses the reopening. T1-ANALYSIS v1.1 §2.2 says these inputs were
  "opened only at S16", so the coordinator writes one OPS line (command line in full, the nine shas) **before** the
  step opens T2-T5.
- **Disclosure.** T2, T3 and T5 hold all 3,600 XM3600 queries, XM600 included. The XM600 rows are loaded and
  discarded, never scored or printed (the §2.4 / CC-298 J3-N6 form).
- **Procedure:**
  - labels per proposition: `c_pvr_score.verifier_labels` (l.246-258), unchanged;
  - unit label: `unit_label` (l.261-263);
  - the cells, κ and shares of `s1_table` (l.660-695), with its FALLBACK rule;
  - **queries restricted to the 3,000 sorted ids of XM-dev500 ∪ XM-test2500** (from T7).
  - **[R2-W5 (d)] Own draw:** `rng = numpy.random.default_rng(20261111)`; `idx = rng.integers(0, 3000, size=(10000,
    3000))` over those sorted ids; percentile 95 % CIs; undefined replicates dropped and counted, > 1 % = FAULT. It does
    not use the §6.1 arrays.
- **Label:** "post hoc (PI-1109a Q6), descriptive; tier-1 verifier mBLIP-BLOOMZ-7B on tier-1 demonstrations (D-VI
  memory, not CC-212's), in situ, all units; restricted to the XM-dev500 ∪ XM-test2500 images".
  - It is **not** a V1-V5 gate result. No sentence says mBLIP "failed this check".
  - The paper wording comes from outcome row 10 of §11.

---

## 5. Arms

### 5.1 Arms per backbone b (one that passed the floor, the precondition and the gate; self-filtering, PI-1109a Q1)

| arm | demonstrations | XM-test2500 | OV-dev-B |
|---|---|---|---|
| `rand` | CC-212 `rand` ids, CC-212 frozen k / order / template | yes | yes |
| `ret` | CC-212 `ret` ids, frozen config (Qwen k8 first T1; InternVL3 k4 last T2) | yes | yes |
| `filt` | `ret` demonstrations after removing the REJECTED obj propositions (`c_pvr.rebuild` / `demos_after`); an emptied demonstration is dropped and never back-filled; the others keep their order | yes | yes |
| `ctl` | **[W9 (a)]** `ret` demonstrations after a random removal **count-matched per demonstration and per stratum** | yes | no |

- **The `ctl` strata.** The strata are {mapped obj, unmapped obj, text}. Under §3.1 every obj proposition is mapped, and
  `filt` removes no text proposition. So matching = the same number of obj propositions as `filt` in each
  demonstration, drawn among that demonstration's obj propositions; the unmapped-obj and text counts are 0 by
  construction.
  - **[N4]** It is `c_pvr.a7_masks(image_id, obj_masks)` unchanged, applied to the obj-only mask lists and mapped back.
  - Seed: `arm_rng("A7", image_id)` = `random.Random(f"20262007|{image_id}")` (c_pvr.py l.327-330, SEEDS["A7"]).
  - **[R2-W10 (c)]** The emptied-demonstration counts of `filt` and `ctl` need not match: `rebuild` can also empty a
    demonstration through its sentence rule. Both counts are reported.
  - **[NB-4]** `ctl` matches counts, not tokens, and can remove obj propositions beyond CAP = 32 that `filt` cannot
    reach. Disclosed beside every `filt − ctl` number, with the cap-hit count.
- **Prompt:** CC-212 `decode_icl.prompt(tpl, captions)` with the backbone's frozen template.
- **All demonstrations emptied:** that image is decoded with the CC-212 zero-shot prompt (`short`, 8870589c…,
  DESIGN l.175) and counted in the fallback share.
- **Decoding:** CC-212 settings: greedy, 60 new tokens, bf16, sdpa, batch 4 (Qwen) / 2 (InternVL3) (DESIGN l.181-185).
  All arms of a backbone run in one job, one environment and one host.
- **Output guard off (τ = −inf) in every arm** (PI-1109a Q2), InternVL3's `ret` and `rand` included. This is
  disclosed as a deviation from the frozen InternVL3 config (τ = 0.10).
  - **[N17]** For InternVL3 every C-DIAG statement says "unguarded retrieval". No C-DIAG row is called a reproduction
    of a CC-212 contrast.
  - No CPU row against the registered τ = 0.10 output is added.
- No `zs` arm.

### 5.2 Execution order
gate → Qwen XM-test2500 → Qwen OV-dev-B → InternVL3 XM-test2500 → InternVL3 OV-dev-B. This is the reverse of the cut
order (§8.3).

### 5.3 [W7, R2-W4] Parity check (supplement only; never a result)
- **What is compared.** For each backbone, set and arm in {`ret`, `rand`}, the re-decoded captions are compared with
  CC-212's **pre-guard** decodes. The CC-212 `preds.json` files hold the raw decodes; the guard is applied only at
  scoring (`score.py variants`, l.116-124; `score_t.py` l.160), so they are the τ = −inf outputs that PI-1109a Q2 names.
  The eight comparator files are pinned in Appendix A.
- **Reported (and nothing else):**
  1. the **byte-equal share** per (backbone, set, arm), by per-caption sha256 on the laptop, no text opened;
  2. each arm's **re-decode minus original** under the same scorer (CIDEr-VI on both sets; P_obj^VI on XM), point and
     percentile CI, **no p**, supplement only.
- **`ret − rand` is not computed on any metric or set** (CC-299r2 Rulings 2-3). No C-DIAG number is a `ret`-vs-`rand`
  contrast.
- **[NB-6] Batch grouping.** Byte equality under batched greedy decoding needs CC-212's batch grouping. The re-decode of
  `ret` and `rand` uses CC-212's decode order and batch sizes (4 / 2) from the CC-212 run records. If that order cannot
  be reconstructed from the records at Stage 0, the byte-equal share is declared **not computable** and only item 2 is
  reported.
- A byte-equal share < 0.95 is disclosed beside every C-DIAG row. It is not a stop.
---

## 6. Statistics

### 6.1 Settings [N1]
- **Unit = image.** Per set, image ids are sorted ascending as strings. The paired resample serves every arm and
  backbone of that set.
- **One generator:** `rng = numpy.random.default_rng(20261108)`. It draws `idx_XM = rng.integers(0, 2500, size=(10000,
  2500))` first, then `idx_OV = rng.integers(0, 925, size=(10000, 925))`. These two index arrays are shared by every arm
  and backbone; B = 10,000; percentile 95 % CIs (2.5 / 97.5).
- Ratio estimators are recomputed per replicate. Replicates with an undefined ratio are dropped and counted; > 1 % is a
  FAULT.
- **[W4] Test p: choice (ii), a paired arm-swap permutation test**, used only for the Holm family:
  - **Permutation.** For each image independently, with probability 1/2, swap the two arms' per-image (present, absent)
    mention counts. Then recompute the pooled ratio difference Δ_perm.
  - **Draws.** R = 10,000 permutations from `numpy.random.default_rng(20261110)`, one Bernoulli(1/2) vector of length
    2,500 per permutation, shared across the contrasts.
  - **p** = (1 + #{|Δ_perm| ≥ |Δ̂|}) / (R + 1), two-sided. **Floor 1/10,001.** This is not "the form CC-212 used",
    whose floor was 1/2,001 (CC-212.txt l.32).
  - **[R2-W3] The null, stated.** H0: within each image, the two arms' per-image (present, absent) count pairs are
    exchangeable, so swapping the arm labels leaves their joint distribution unchanged. This is **stronger than "equal
    pooled precision"**: equal pooled precision can hold while H0 fails. Under H0 the arm-swap distribution is exact;
    a rejection means the arms differ in some way within images, not by itself that pooled precision differs. For that
    reason a label never rests on the p alone (§6.4: the CI must agree in sign).
  - **Why (ii) and not (i).** The arm-swap test is exact under H0, needs no centring assumption and handles the
    pooled-ratio statistic directly. A null-centred bootstrap (i) is only approximate for a ratio of sums.
  - The percentile CIs above still carry the SESOI and harm rules.

### 6.2 SESOI and margins (fixed now; rationale in §1.3)
- **SESOI_P = 2.0 points of P_obj^VI** (tier-1's 2.719 came from mBLIP's A12 headroom and does not transfer).
- **δ_C = 2.0 CIDEr-VI points; δ_R = 2.0 points of R_obj^VI** (tier-1 values). There is no CIDEr gain label (W1 (a)),
  so SESOI_C is not used.

### 6.3 [W1 (a)] The Holm family: P_obj contrasts only
- **Family:** for each backbone whose **XM-test2500 block completed**: P_obj^VI `filt − ret`, `filt − ctl` and
  `filt − rand`. So m ≤ 3 per backbone and ≤ 6 in total. Holm step-down at α = 0.05 on the §6.1 permutation p.
- **m** = the contrasts of completed XM blocks. Cuts, gate FAILs, floor drops and precondition drops remove whole
  blocks. m is fixed at the last cut and printed in the S4 record before any contrast is computed. **A guard label
  never removes a contrast from the family.**
- **Why choice (a), not (b).**
  - Q-D2's object-factuality question is the only one with independent gold on the scored images.
  - Filtering is not expected to raise CIDEr-VI; it removes words that the references may contain. A CIDEr gain label
    would mainly cost P_obj power.
  - CIDEr-VI therefore acts only as a harm guard under fixed CI rules. Its states are reported as descriptive costs
    and are never stated as tested claims.
- **Outside the family (descriptive):**
  - CIDEr-VI on both sets;
  - R_obj^VI;
  - P_obj^VI,wrong;
  - ΔP_cm;
  - the §4.4 quantities;
  - the §5.3 parity check (no p at all).

### 6.4 [W1] Labels: complete and mutually exclusive

**Per-contrast P_obj state** (each Holm-family contrast; first matching row):

| state | condition |
|---|---|
| GF / GC / GB | guard: `filt` VI-script < 0.95 (GF), the comparator < 0.95 (GC), or both (GB; **both labels printed**, CC-298 Ruling 3) |
| UP | Holm reject, point ≥ SESOI_P **and** CI lower bound > 0 |
| UPs | **[R2-W3]** Holm reject, point > 0, **CI lower bound > 0**, and not UP (so point < SESOI_P) |
| DOWN | **[R2-W3]** Holm reject, point < 0 **and CI upper bound < 0** |
| NS | everything else: not Holm reject; point = 0; or a Holm reject whose CI includes 0 |

**Harm states, per backbone and set, from `filt − ret`** (CI rules, descriptive):
- **CIDEr-VI states** (also used for `filt − rand` on OV-dev-B):
  - C1: upper bound < 0 and lower bound ≤ −δ_C;
  - C2: upper bound < 0 and lower bound > −δ_C;
  - C3: upper bound ≥ 0 and lower bound ≤ −δ_C;
  - C4: upper bound ≥ 0 and lower bound > −δ_C.
- **R_obj^VI states** (XM only): R1-R4, the same four forms with δ_R.
- **C_ok** = C2 or C4 on XM-test2500. **R_ok** = R2 or R4.
- A guard failure on `filt` or `ret` gives that CIDEr or R comparison the guard state, and C_ok / R_ok are false.

**Backbone summary label on XM-test2500.** Decided by the `filt − ret` state first, then by `filt − ctl` and the harm
flags:

| `filt − ret` | `filt − ctl` | R_ok ∧ C_ok | label |
|---|---|---|---|
| GF / GC / GB | any | any | **S0** guard label(s), verbatim |
| DOWN | any | any | **S5** "filtering lowered object precision" (R and C states shown beside) |
| NS | any | any | **S6** "no change in object precision shown" |
| UPs | any | true | **S4** "precision rose (x [CI]); a rise of SESOI_P is not shown" |
| UPs | any | false | **S4c** "precision rose (x [CI]); a rise of SESOI_P is not shown; a recall or CIDEr-VI cost is not excluded" |
| UP | UP or UPs | true | **S1** "filtering raised object precision beyond count-matched removal" |
| UP | UP or UPs | false | **S2** "precision rose; a recall or CIDEr-VI cost is not excluded" |
| UP | GF / GC / GB / DOWN / NS | true | **S3** "precision rose; not shown beyond count-matched removal" |
| UP | GF / GC / GB / DOWN / NS | false | **S3c** = S3 + "; a recall or CIDEr-VI cost is not excluded" |

- **Other labels:**
  - `filt − rand` on XM: its per-contrast P state (Holm), worded by §11 row 6.
  - OV-dev-B, per backbone: the CIDEr state of `filt − ret` and of `filt − rand` (C1-C4 or a guard label),
    descriptive, worded by §11 row 7.
- **Exclusive and exhaustive by construction.** Appendix D first maps every primitive combination (guard, Holm, point
  sign, CI bounds) to exactly one state, then enumerates all 7 × 7 × 2 × 2 = 196 combinations of
  (`filt − ret` state, `filt − ctl` state, R_ok, C_ok). Each maps to exactly one label: S0 84, S1 2, S2 6, S3 5, S3c 15,
  S4 7, S4c 21, S5 28, S6 28.
  - `test_c_diag.py` repeats the enumeration against the scorer's own function.

### 6.5 Descriptive numbers that will be reported
- **Per set and arm:**
  - CIDEr-VI (as written, stripped);
  - XM only: P_obj^VI, P_obj^VI,wrong, R_obj^VI, CHAIR_i^VI;
  - mentions per caption; verifiable-mention share; VI-script share; empty share; mean syllables; fallback share;
    emptied-demonstration share; obj propositions removed per image; verifier calls, cap hits, parse-failure share.
- **Family:** each contrast's point [95 % CI], permutation p, Holm-adjusted p, state and summary label; m.
- **Descriptive contrasts:**
  - harm states with point [CI];
  - ΔP_cm (filt vs ret);
  - the parity check (§5.3).
- **Gate:**
  - the §4.2 table and measures with CIs, V1-V5 per verifier, the ladder rung used, and the supply per rung;
  - c_b of the headroom floor.
- **In situ:** the §4.4 table and odds identity, and the §4.5 post hoc mBLIP table.
- **Run:** GPU-h and VND per stage; the cuts applied.

---

## 7. Models and pins

| key | hub id @ revision | role | source |
|---|---|---|---|
| `qwen25vl_7b` | `Qwen/Qwen2.5-VL-7B-Instruct` @ `cc594898137f460bfe9f0759e9844b3ce807cfb5` | captioner and its own demonstration filter | DESIGN l.181 |
| `internvl3_8b` | `OpenGVLab/InternVL3-8B-hf` @ `259a3b64a14623c0ec91a045cb43f7c5af5fa6af` | captioner and its own demonstration filter | DESIGN l.182 |

- The S2 instrument `OpenGVLab/InternVL3-8B` @ 853e3a79 (DESIGN l.216) is not used.
- **Per-file sha256 placeholders.** These are filled at Stage 0 from the CC-212 run records or a fresh snapshot at the
  pinned revision, then frozen. A mismatch with a CC-212 record is a FAULT.
  - Qwen: the safetensors shards `<sha>` each; `config.json`, `generation_config.json`, `preprocessor_config.json`,
    `tokenizer.json`, `tokenizer_config.json` and `chat_template.json` `<sha>` each.
  - InternVL3-hf: the safetensors shards `<sha>` each; `config.json`, `generation_config.json`,
    `preprocessor_config.json`, `processor_config.json`, `tokenizer.json`, `tokenizer_config.json` and the chat
    template `<sha>` each.
- **Environment:** the CC-212 decode venv (transformers 4.57.6, DESIGN l.347), with its freeze sha `<sha>` from the
  CC-212 record; torch / CUDA `<pin>`. VnCoreNLP is pinned per `CIDER_VI_PIN_v1_1` §3 and runs on the laptop only.
- **Hardware:** one rented 1× RTX 3090 / 3090 Ti 24 GB of GPU_RENTAL_SPEC (PI-1107a CPU floor). One model is loaded at
  a time.
  - **[N16]** CC-212 decoded both backbones on RTX 3090-class cards (DESIGN l.304). The CC-212 records read here give
    no VRAM peak, so `hostcheck` measures and records the peak of each backbone at a full k-demonstration prompt. The
    mBLIP probe figure is no longer cited.
- **Offline:** each snapshot is fetched once by `--revision` (never `main`) and shard-checked. The job then runs with
  `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1`.

---

## 8. Compute, money and stop rules

### 8.1 Speed numbers [N3, N21]
- **Borrowed rates:**
  - CC-212 test host, per image-arm, at CC-212 batch sizes (2026-10-27_c_en PREREG l.134): Qwen 0.40 s (XM) / 0.69 s
    (OV); InternVL3 1.30 s / 1.24 s;
  - RTX 3090 zero-shot (DESIGN l.304-307): Qwen 0.70 s, InternVL3-hf 1.27 s per image.
- **Planning rate for verifier calls (batch 1), [est.]:** Qwen **0.70 s**, InternVL3 **1.30 s**. These are the slower
  of the borrowed per-image rates, since verifier calls run at batch 1.
- **Calls per demonstration ≤ 1.221.** That is tier-1 `mean_calls` 4.884 / 4, counted over all kinds; obj-only (§3.2)
  can only be fewer.
  - **Stage 0 replaces it with the exact obj-proposition counts** per backbone and set, and re-projects **before
    renting** (§8.3).
- The rates come from the M3 host. Any 3090 difference is absorbed mechanically by the projection and the cut order.

### 8.2 Estimate per stage [est.; planning rates]

| stage | work | GPU-h |
|---|---|---|
| S1 gate | 300 units × 2 passes × 2 verifiers (Qwen 600 × 0.70 s, InternVL3 600 × 1.30 s) | 0.33 |
| S2-Q verify | Qwen, ranks 1-8: XM 24,420 calls (4.75 h) + OV 9,035 calls (1.76 h) at 0.70 s | 6.51 |
| S3-Q decode | Qwen: XM 4 arms × 2,500 × 0.40 s (1.11 h) + OV 3 × 925 × 0.69 s (0.53 h) | 1.64 |
| S2-I verify | InternVL3, ranks 1-4: XM 12,210 calls (4.41 h) + OV 4,518 calls (1.63 h) at 1.30 s | 6.04 |
| S3-I decode | InternVL3: XM 4 × 2,500 × 1.30 s (3.61 h) + OV 3 × 925 × 1.24 s (0.96 h) | 4.57 |
| loads and gate wait | 4 model loads; one laptop round trip | 0.6 |
| **GPU subtotal, no cut** | | **19.7** |
| billed overhead | setup, hostcheck, push of ≈ 3,800 images, 2 snapshot fetches, pull, delete (tier-1 LOG l.1807-1867) | ≈ 1.4 |
| **billed, no cut** | | **≈ 21.1 > 20.0** |
| **billed, cut 1 applied** (InternVL3 OV-dev-B, −2.59 h) | | **≈ 18.5** |

- **At planning rates, cut 1 is expected.** The pre-rental re-projection with the exact Stage-0 counts decides it, and
  it may restore the cut block if the counts are lower.
- **[N3] One verifier only:** Qwen ≈ 10.3 h billed; InternVL3 ≈ 12.8 h billed **[R2-W10 (a)]** (0.22 + 6.04 + 4.57 +
  0.6 + 1.4 = 12.83).

### 8.3 Money block, solvency and cuts
- **A new block** (PI-1109a Q3). C's tier-1 block is closed at 218,959 VND (PI-1108g Q2; LOG l.1867), and C-DIAG takes
  nothing from it.
- **Cap: 20.0 billed host-hours AND M_D = 210,000 VND, whichever binds first.** At r = 10,091.01 VND/h, 20.0 h =
  201,820 VND + 30 VND setup. If the offer rate is higher, the hour cap becomes (210,000 − 30) / r.
- **[R2-W1 (b)] Gate-only branch cap: 3.0 billed host-hours**, inside the 210,000 VND block. It replaces the 20 h cap
  for that branch. A cap stop there is "incomplete", with no partial number.
- **[R2-W8, J1 N-6] Cap extension.** A judge may extend a cap only inside the 210,000 VND block. Any spend beyond it is
  the PI's (PI-1109d item 2).
- **[N10, Q7] Solvency and order (PI-1109a Q7), checked immediately before renting, from the panel:**

  **[R2-W8] (PI-1109c P2: B's real worst case, counted once)**

  `PASS_parallel  ⇔  Bal ≥ M_D + 3·r_D + Σ_live + W_B + O_B + W`

  | term | meaning |
  |---|---|
  | Bal | panel balance now |
  | M_D | 210,000 |
  | r_D | C-DIAG offer rate |
  | 3·r_D | three hours of C-DIAG's rate: the house L-before buffer for overrun, pull and delete (OPS-1108a-hc1-lbefore form) |
  | Σ_live | remaining cost of every other live rental except B's HB-T1 |
  | W_B | B's worst-case remaining spend = max(0, 40 − h_B) × r_B (`B_RUN_DOC_v1_2.md` 6524845… l.403-408). h_B = HB-T1 billed hours so far (0 before B rents); r_B = HB-T1's rate, or the offer rate before the rental. The 40 h already includes B's whole cap (setup ≤ 4, cap 28, idle ≤ 6, teardown 1, margin) |
  | O_B | 0 if B's one resume is used or B's block has ended; else the **non-cap** terms of B §12.3 step 2 (l.851-852): (4 + 1 + 2) × r_B + 30 = 7·r_B + 30 (PI-1108i). The resume's cap left is already inside W_B |
  | W | 50,000, the top-up warning line (PI-1108h) |

  - **PASS:** C-DIAG rents its own host now, in parallel with B. B keeps priority on agent time.
  - **FAIL:** B goes first. The check is repeated when B's block ends (W_B = O_B = 0) or after a top-up.
  - **Worked value** (not a check): Bal = 1,079,499 (LOG l.1888), r = 10,092, B not rented, Σ_live = 0, so the
    right-hand side = 210,000 + 30,276 + 0 + 403,680 + 70,674 + 50,000 = 764,630 → PASS by **314,869** (CC-299r2
    Ruling 4).
  - **[R2-W1 (e)] Gate-only branch:** the same formula with M_D replaced by 3.0 · r_D + 30. Worked value: 30,306 +
    30,276 + 403,680 + 70,674 + 50,000 = 584,936 → PASS by 494,563.
- **Projection (mechanical) [N2]:**
  - **First run:** at the end of S1, from the measured gate rates (with image) and the planning caption rates.
  - **Re-runs:** after the first 100 queries of every verify and decode stage, with that stage's measured rate, and at
    each stage start.
  - **Form:** elapsed billed time + rate × work left + 0.5 h (pull and delete).
  - **On excess:** if it exceeds the cap, the highest **not-yet-started** block in the cut order is removed. This
    repeats until the projection fits.
  - **If nothing removable is left** (only the running block or never-cut blocks), the run continues, and a cap stop is
    final.
- **Cut order (first cut first):**
  1. InternVL3 OV-dev-B;
  2. Qwen OV-dev-B;
  3. InternVL3 XM-test2500.
  - Never cut: the gate, or the Qwen XM-test2500 arms.
  - If the Qwen block is dropped before rental (floor, precondition) or by the gate, the never-cut set is InternVL3
    XM-test2500.

### 8.4 Stop rules
- **Cap:** JOB STOP. The partial block is reported "incomplete", with no contrast or label and no partial output read.
  The host is pulled and deleted. The cap may be extended only by a judge before any partial output of that block is
  read.
- **FAULT:**
  - **Causes:** a pin, sha or SUMS mismatch; an open outside the allow-list; a selftest failure; a crash after 3
    attempts per step; a FAULT case named in §4.1, §4.2 or §6.1.
  - **Response:** JOB STOP and one OPS line with every command line quoted in full, with no number from the affected
    stage. The fix goes through a one-judge read, then the stage re-runs on the same inputs as "re-run after FAULT"
    (T1-ANALYSIS v1.1 §9.1 / CC-297 path). A re-run is not a new look.
  - **Exception:** data-degeneracy FAULTs (§4.1 supply, §4.2 κ, and §6.1 / §4.5 undefined-ratio replicates > 1 %
    **[R2-W10 (e)]**) are final for that verifier or block, because a re-run would give the same data.
- **Gate FAIL:** that verifier stops. If both fail, the host is deleted right after the gate pull.
- **[R2-W1 (d)] Gate-only branch:** the host is deleted right after the gate pull, whatever the verdict (§4.3).
- **Before rental:** floor or VI-script precondition failures drop blocks (§1.3, §14). If nothing remains, there is no
  rental, except the gate-only branch, whose trigger is exactly "both c_b < 0.10" (§1.3, R2-W1 (a)).
- **Idle:** if the host waits more than 1 h for anything other than the gate verdict, it is pulled and deleted.

---

## 9. Run stages and custody

| stage | where | what |
|---|---|---|
| S0 | laptop CPU | allow-list check; ids and manifests; label subset (§2.4); decomposition; gate ladder and sample (§4.1); headroom floor (§1.3); VI-script precondition (§14); exact call counts and the re-projection (§8); snapshot pins; CPU selftest; one LOG line with every sha |
| S0r | — | code read (one judge, 85) and host-amendment read (Appendix C, one judge, 85) before any rental |
| S1 | host | gate calls for both verifiers → pull labels → laptop `c_diag_score.py gate` → verdict OPS line. **Gate-only branch [R2-W1]:** pull, then delete the host, then compute the verdict; S2-S4 do not run (the §4.5 step may still run) |
| S2/S3 | host | per remaining backbone: verify the obj propositions of ranks 1..k → `filt` / `ctl` texts on the host → decode `rand`, `ret`, `filt`, `ctl` |
| S4 | laptop CPU | m record; CIDEr-VI producer; P_obj^VI; bootstrap; permutation; Holm; labels; §4.5 recompute (coordinator) → result read (§13) |

**[W8] Custody.**
- **Licence.** XM3600 images are a spent test set in a dev role.
  - CC-209 Ruling 1(a) (l.95-104) does **not** license them on a rented host ("NOT ALLOWED as written", l.100).
  - The licence is **PI-1104af** (LOG l.1530), with **host amendment v3 H-1** (`AMENDMENT_HOST_3090_DRAFT_v3.md` l.241,
    committed 5d6f5ca). Both cover only C's tier-1/tier-2 §5 sets.
  - **PI-1109a Q9** extends PI-1104af to C-DIAG's XM3600 pixels on the tier-1 conditions: tmpfs only, no labels on the
    host, wipe at the end.
  - The C-DIAG host amendment (**Appendix C**) names the host and the covered material. It needs a one-judge read
    before any rental (§14).
- **On the host:**
  - images: the XM-dev500 gate query images, XM-test2500 and OV-dev-B; **in the gate-only branch, only the XM-dev500
    gate query images [R2-W1 (c)]**;
  - the shown-caption texts of KTVIC / OpenViIC **train** demonstrations;
  - the gate unit file without status.
  - Never on the host: a label, status, reference, test file or label-derived mask.
- Outputs hold ids, labels, masks, counts and the query caption. Logs hold ids only.
- **[N18]** The gate unit file and the manifests hold train caption text. They live only in laptop scratch and host
  tmpfs, never under the repo, and are **never committed**. Only their shas are logged.
- No host name, IP or port appears in any repo file.

---

## 10. Code: reuse and minimal new code (listed, not written)

### 10.1 Reused unchanged (imported behind sha pins)
- `scripts/c_pvr/c_pvr.py` (a503644a): `clean`, `rdr`, `decompose_vi`, `proposition`, `ver_prompt`, `parse_label`,
  `verify`, `split_back`, `a7_masks`, `arm_rng`, `demos_after`, `rebuild`, `CAP`, `MAX_NEW`.
- `scripts/c_pvr/prompts/ver_3way.txt` (bcb92308).
- `scripts/c_stage1/decode_icl.py` (fa5a2511): `exemplar_ids`, `shown`, `prompt`, `memory_captions`, `lb.load`, the
  decode settings. `guard.py` (5f930e96): the text-only path of `hf_verifier`, as a pattern.
- `scripts/kit_b/protocol_pilot.py` (6aee4282) `Cider`; `scripts/kit_b/punctuation_audit.py` (a7e80240).
- `scripts/xm3600_oiv7.py` (9a79403f) `status`, `statuses`, `resolve_map`; `rescap/chair.py` (e47d249a) `objects_in`,
  `norm_tone`; `rescap/vi/lexicon.py` (fbc945f2) `CLASSIFIERS`.
- For §4.5 only: `scripts/c_pvr/c_pvr_score.py` (7f352276) functions `verifier_labels`, `unit_label` and the
  `s1_table` arithmetic (`manifests` is not used, R2-W5 (b)). This reuses read-only helpers, not the scorer's labelling path, so the CC-298 Ruling 3
  deferred fix does not bind it.
- **Not reused:** the `c_pvr_score.py score` command, and `c_pvr_cider_vi.py`'s set table (it fixes sizes 286 / 1,020).

### 10.2 New code (minimal)
1. **`scripts/c_diag/c_diag.py`** (laptop). Subcommands:
   - `allow`, the Appendix B allow-list guard, used by every subcommand;
   - `lists`;
   - `label-subset` (§2.4);
   - `decomp`;
   - `gate-sample` (§4.1 ladder);
   - `floor` (§1.3);
   - `vi-pre` (§14 item 7);
   - `counts`;
   - `manifest`;
   - `pins`.
2. **`scripts/c_diag/c_diag_gpu.py`** (host). Subcommands:
   - `hostcheck`, which records VRAM peaks;
   - `gate`, with image and image-blind;
   - `verify` (obj only);
   - `texts` (`filt`, and `ctl` via `a7_masks` on obj-only masks);
   - `decode`.
3. **`scripts/c_diag/c_diag_job.sh`:**
   - stages, cap, projection and cut order;
   - the manifest sha as an argument (CC-298 J3-N3);
   - `SHA256SUMS_<mode>` written **after** "JOB DONE" and the trap's EXIT line (CC-297 N-4);
   - pixel and caption-text material only under `/dev/shm/c_diag_hd/`, with a trap wipe and a deletion log
     (Appendix C).
4. **`scripts/c_diag/c_diag_score.py`** (laptop). Subcommands:
   - `gate` (§4.2-4.3);
   - `cider` (two reference files only, §2.4);
   - `score` (P_obj^VI, guards, bootstrap, permutation, Holm with m, §6.4 labels, §4.4, ΔP_cm, parity);
   - (§4.5 is not here: it is the coordinator-run `c_diag_t1table.py`, item 7, under its own allow-list.)
5. **`scripts/c_diag/test_c_diag.py`** (CPU selftest; no weights, no data, every socket raises). It checks:
   - the gate rule on synthetic counts, where the tier-1 values must FAIL, and degenerate κ;
   - the ladder;
   - the bare-unit rule with "_" compounds;
   - REJECTED-obj-only removal; the stratified `ctl` match; the zero-shot fallback; empty-caption scoring;
   - the both-fail guard label; the primitive-to-state map and the 196-row label enumeration of Appendix D; the
     CI/p sign rule (a Holm reject whose CI includes 0 → NS); the permutation p floor; the Holm order with m from
     completed blocks;
   - the gate-only branch: trigger only on both c_b < 0.10, 3.0 h cap, gate images only, delete before verdict;
   - the allow-list and the deny backstop, including the two stray `ktvic/test_data.json` copies.
6. **`scripts/c_diag/SHA256SUMS`.**
7. **`scripts/c_diag/c_diag_t1table.py`** (laptop, coordinator-run, §4.5): about 60 lines that import
   `verifier_labels`, `unit_label` and the `s1_table` arithmetic (not `manifests`). **[R2-W5 (a)]** It uses the same
   `allow` function with its own nine-entry list (§4.5).

---

## 11. What the paper may and may not say

Every row is labelled "XM-test2500 (scored once for the registered CC-212 test, re-used here in a dev role) / OV-dev-B /
XM-dev500, exploratory, in-sample". Every row uses "demonstration filter" for the model role and "filtering" for the
method. XM-test2500 is never called "development images" (W6).

| # | outcome | may say | may not say |
|---|---|---|---|
| 1 | Both demonstration filters fail the gate | "With the same prompt, neither model separated present from absent objects in the retrieved examples at the pre-set bar (κ = x [CI]; …). Filtering was not run." | any filtering effect; "checking examples cannot work"; any tuned retry |
| 2 | One fails | row 1 for that model; rows 3-8 for the other | pooling the backbones |
| 2a | **[R2-W2 (i)]** Gate PASS (main branch) | "Model b passed the pre-set bar on bare object units of the XM-dev500 images (κ = x [CI]; no-rates y / z; SUPPORTED share on present w), rung r of the supply ladder." | "verification", "verified", "the model verifies"; any filtering effect from the gate alone; any generalisation beyond bare object units of the rung used |
| 2b | **[R2-W2 (ii)]** Gate outcome, gate-only branch | row 2a or row 1 for each model, plus "Filtering was not run: the retrieved examples had too few absent objects to filter (headroom floor: c = x for Qwen2.5-VL, y for InternVL3, below 0.10)." | as row 2a; any statement about filtering's effect |
| 3 | S1 | "On the XM-test2500 images, re-used in a dev role (exploratory, in-sample), filtering the retrieved examples with model b raised object precision by x [CI] points over unguarded unfiltered retrieval, and by y [CI] over removing the same number of object phrases at random (Holm-adjusted)." | "confirmed", test, any generalisation; abstract headline; "first"; "verification" |
| 4 | S2 / S3 / S3c / S4 / S4c | the label text of §6.4, verbatim, with x [CI]; **[NB-5]** for every S1-S4c, the R_obj and CIDEr-VI states (XM) and the OV-dev-B CIDEr-VI state are shown beside it | dropping the "not shown beyond…", "a rise of SESOI_P is not shown" or "cost not excluded" clause |
| 5 | S5 / S6 | "Filtering lowered object precision by x [CI]" / "No change in object precision was shown (x [CI])." | "no effect", "equivalent" |
| 6 | `filt − rand` (XM) | its P state worded as in rows 3-5, against "random examples", without the `ctl` clause | the same as rows 3-5 |
| 7 | OV-dev-B CIDEr-VI states | C1: "CIDEr-VI fell by x [CI]; a fall beyond 2.0 is not excluded"; C2: "CIDEr-VI fell by x [CI], within 2.0"; C3: "CIDEr-VI changed by x [CI]; a fall beyond 2.0 is not excluded"; C4: "no CIDEr-VI fall beyond 2.0 (x [CI])". Each is labelled descriptive. | any CIDEr gain claim; calling a state a tested result |
| 8 | Guard label (S0, or a guard state) | the label(s) verbatim, with the VI-script and empty shares | any number from that contrast as a finding |
| 9 | **[W7, R2-W4]** Parity check | supplement only: the byte-equal share per (backbone, set, arm) and each arm's re-decode-minus-original point [CI], labelled "parity check" | any p; main text; any `ret − rand` number; beside or instead of XM-a, XM-b, InternVL3 τ = −∞ rows or the stage-B gate |
| 9a | **[R2-W4]** `ret` vs `rand` object precision | nothing | any C-DIAG `ret − rand` object-precision statement on XM-test2500; presenting any C-DIAG number as C_META X3 or as an answer to R5 #3 |
| 10 | §4.5 mBLIP table | "An earlier pilot demonstration filter showed near-chance agreement with the existing labels on these images (κ = x [CI]; post hoc)." | "failed this check" or any V1-V5 wording; all-XM3600 numbers |
| 11 | Headroom floor drop or cap stop / FAULT | the floor value c_b, or "incomplete", with the reason in one line | any partial number |

In every row:
- No AI-use text and no data-overlap or duplication wording (PI-1101e, PI-1101o).
- The CC-212 seen results of §1.3 are cited beside the C-DIAG paragraph; its tier-1 rows are not (§1.3, row 10).
- **[N13] Before any text is written,** the paper is positioned against arXiv 2511.08909 and arXiv 2406.02265 (J2
  N8). Neither is verified here; this file made no network read.

---

## 12. PI questions

**Answered by PI-1109a and folded in:**
- Q1 self/self (§1.2, §5.1).
- Q2 guard off with sha parity (§5.1, §5.3).
- Q3 money block (§8.3).
- Q4 sets and ladder (§2.2, §4.1).
- Q5 no English row, for cost (§2.2).
- Q6 the post hoc mBLIP table (§4.5).
- Q7 the solvency formula (§8.3).
- Q8 the floor at 0.10 (§1.3).
- Q9 the custody extension plus the host amendment (§9, Appendix C).

**[R2-W1 (g)] Answered by PI-1109b:** Q10 = **YES**. The gate-only branch is binding text: trigger §1.3, cap and
solvency §8.3, delete §4.3 and §8.4, stages §9, material Appendix C, wording §11 row 2b.

**[R2-W9] Answered by PI-1109c:** P1 = YES (C-DIAG never holds up the CC-212 revision or the TALLIP submission; §1.2,
§14 item 8). P2 = YES (the solvency check reserves B's real worst case once, W_B + O_B; §8.3).

**PI-1109d (delegation).** Only direction, money above a cap or a new block, data licence / custody / test looks, and
submission go to the PI. Every other choice in v1.2 is the drafter's, stated where it is made (§16). **No PI question
is open.**

---

## 13. Judge tier

- **This file:** IRREVERSIBLE, threshold 85, FULL three-judge panel (rigor, path, adversary), mode `panel`, **round
  3/3, the last**, with Codex read-only (CC-299r2 ROUND 3). A diff read cannot grant GO (judge-panel.js verdict();
  CC-296 Ruling 12). No GO → ESCALATE_TO_PI. Ruling 3 stands with the §5.3 drop (§1.2).
- **Later reads (fixed now):**
  - code read: one judge, reversible 85;
  - host amendment (Appendix C): one judge, 85 (PI-1104af's own condition; CC-299 Ruling 5);
  - S1 gate verdict: mechanical;
  - S4 result read: one judge, reversible 85, but a **full panel if any STOP, cap stop, FAULT or gate FAIL occurred**.

---

## 14. Preconditions (each a STOP if unmet)

1. This file GO'd and committed byte-equal. Every [proposal] value is fixed as written (N5).
2. **[R2-W1 (h)]** PI answers on file: **PI-1109a, PI-1109b and PI-1109c** (done). Any later non-default answer
   means a v1.3 and a re-read.
3. The code (§10.2) committed with `SHA256SUMS`, and its one-judge read GO. CC-297 N-4 and CC-298 J3-N3 are met in the
   new job code, and the allow-list is verified.
4. **[W8]** The Appendix C host amendment read GO (one judge, 85), and PI-1109a Q9 = YES (done).
5. Stage-0 pins filled and logged: the §7 `<sha>` placeholders, the label-subset sha, the gate sample sha, the CC-212
   venv lock, and the image sha lists of XM-dev500 gate queries, XM-test2500 (`staging/xm_test2500.sha256` 9ae7c0ac)
   and OV-dev-B (from `lists.json`).
6. Stage-0 results logged: the gate ladder rung and supply, c_b, the exact call counts, the re-projection and its cuts,
   and the §8.3 solvency check PASS (or "B first").
7. **[N6] VI-script precondition.** The VI-script share of the frozen CC-212 `ret` and `rand` decodes (Appendix A files)
   must be ≥ 0.95 per (backbone, set, arm). It is computed on the laptop, aggregate only. A block whose `ret` or `rand`
   fails is dropped before rental and reported.
8. **[R2-W9]** C-DIAG never holds up the CC-212 revision or the TALLIP submission; if it is late, C proceeds without
   it (PI-1109c P1).

---

## 15. Closure table (CC-299r2; CC-299 below)

**15.1 CC-299r2 (round 2) items.**

| item | closed at (line in v1.2) |
|---|---|
| R2-W1 (a) trigger = both c_b < 0.10 only; other empty runs → no rental | l.163; l.166; l.770 |
| R2-W1 (b) 3.0 billed-hour cap inside the block; cap stop = incomplete | l.710 |
| R2-W1 (c) gate images only on the host | l.795; l.1146; l.1171 |
| R2-W1 (d) no S2/S3; delete after the gate pull, verdict after the delete | l.406; l.768; l.781; l.1182 |
| R2-W1 (e) own solvency check (M_D → 3.0·r_D + 30) | l.736 |
| R2-W1 (f) §11 rows | l.879; l.880 |
| R2-W1 (g) Q10 = YES (PI-1109b), default text removed | l.913 |
| R2-W1 (h) §14 item 2; this table | l.941 |
| R2-W2 (i) main-branch gate PASS row | l.879 |
| R2-W2 (ii) gate-only row; filtering-not-run (headroom) wording | l.880 |
| R2-W3 null disclosed | l.543 |
| R2-W3 UPs / DOWN / NS with CI sign agreement | l.585; l.586; l.587 |
| R2-W3 S4 / S4c wording | l.607 |
| R2-W3 Appendix D regenerated | l.1193; l.1195 |
| R2-W4 §5.3: byte-equal share + re-decode − original only; no ret − rand | l.508; l.517 |
| R2-W4 §11 rows 9 and 9a (may-not: X3, R5 #3) | l.887; l.888 |
| R2-W4 Ruling 3 stands | l.81 |
| R2-W5 (a) own allow function and nine-entry list | l.426; l.865 |
| R2-W5 (b) narrow manifest check, f81323d1 (LOG l.1763) | l.443 |
| R2-W5 (c) path ~/c_pvr_h4_1107; no hand row due | l.447 |
| R2-W5 (d) own 3,000-id draw, seed 20261111 | l.461 |
| R2-W5 (e) PI-1109a Q6 + OPS line before reopening | l.451 |
| R2-W6 (a) tier-1 P_obj results disclosed | l.115 |
| R2-W6 (b) headroom scoped to CC-212 backbones; Table S8 at frozen τ | l.120 |
| R2-W6 (c) SESOI rationale rewritten (C-DIAG's own choice; value 2.0) | l.135 |
| R2-W7 `.vsps_sealed` back in the deny backstop; selftest | l.228; l.233 |
| R2-W8 W_B + O_B; 3·r_D row; worked 314,869 | l.716; l.725; l.727; l.728; l.734 |
| R2-W8 / J1 N-6 cap extension only inside 210k | l.712 |
| R2-W9 P1 in §1.2, §12, §14 | l.85; l.916; l.954 |
| R2-W10 (a) 12.8 h | l.702 |
| R2-W10 (b) "about 8" | l.158 |
| R2-W10 (c) both emptied counts reported | l.488 |
| R2-W10 (d) exact ratio only at zero cap hits | l.420 |
| R2-W10 (e) undefined-ratio FAULT is final | l.766 |
| NB-1 n_q defined | l.385 |
| NB-2 per-subcommand allow-list | l.1140 |
| NB-3 label-subset keys asserted | l.255 |
| NB-4 ctl beyond cap disclosed | l.490 |
| NB-5 R/C and OV states beside S1-S4c | l.882 |
| NB-6 batch grouping or not computable | l.519 |
| NB-7 floor kept, probably non-binding | l.168 |
| NB-8 value note | l.170 |

**15.2 CC-299 (round 1) items, unchanged since v1.1, at their v1.2 lines.**

| item | line(s) in v1.2 |
|---|---|
| W1 | l.557; l.577 |
| W2 | l.336 |
| W3 | l.368 |
| W4 | l.536 |
| W5 | l.239 |
| W6 | l.72 |
| W7 | l.508 |
| W8 | l.785 |
| W9 | l.287 |
| W10 | l.223 |
| W11 | l.103 |
| N1 | l.528 |
| N2 | l.411 |
| N3 | l.672 |
| N4 | l.486 |
| N5 | l.14 |
| N6 | l.951 |
| N7 | l.392 |
| N8 | l.342 |
| N9 | l.94 |
| N10 | l.714 |
| N11 | l.214 |
| N12 | l.91 |
| N13 | l.895 |
| N14 | l.196 |
| N15 | l.311 |
| N16 | l.662 |
| N17 | l.499 |
| N18 | l.801 |
| N19 | l.219 |
| N20 | l.314 |
| N21 | l.672 |

Not acted on here, by design: NB-9 (round 3 is final; this file closes everything in one pass), NB-10 (B's run-doc
carry-over, fixed at B's next version), NB-11 (folded into R2-W4), NB-12 (STATE C row: the coordinator's file),
NB-13 (CC-299 N13-N21 carried as in v1.1).

## 16. Change table v1.1 → v1.2 (every edit; nothing else changed)

| where | edit | item |
|---|---|---|
| header | v1.2 status, round 3/3, CC-299r2, PI-1109a/b/c/d | R2-W1 (h), R2-W9 |
| §0 | v1.2 sources | record |
| §1.2 | Ruling 3 stands; P1 never on the critical path | R2-W4, R2-W9 |
| §1.3 | paper scope of the seen results; tier-1 results (prereg only); headroom scoped, with the mBLIP facts (κ, emptied share); Table S8 τ; SESOI rationale; "about 8"; gate-only trigger; NB-7, NB-8 | R2-W6, R2-W10 (b), R2-W1 (a) |
| §2.3 | `.vsps_sealed` deny + selftest | R2-W7 |
| §2.4 | label-subset key assert | NB-3 |
| §4.2 | n_q | NB-1 |
| §4.3 | gate-only delete; wait bound scoped to the main branch | R2-W1 (d) |
| §4.4 | exact ratio only at zero cap hits | R2-W10 (d), NB-4 |
| §4.5 | rewritten: own allow-list (9 inputs), narrow manifest check, path, own draw, OPS line | R2-W5 |
| §5.1 | both emptied counts reported; `ctl` beyond cap disclosed | R2-W10 (c), NB-4 |
| §5.3 | rewritten: no `ret − rand`; byte-equal + re-decode − original; batch grouping | R2-W4, NB-6 |
| §6.1 | null stated | R2-W3 |
| §6.4 | UPs / DOWN / NS; S4 / S4c wording; pointer to D.1 | R2-W3 |
| §8.2 | 12.8 h | R2-W10 (a) |
| §8.3 | gate-only cap and solvency; cap-extension rule; W_B + O_B; 3·r_D row; worked value | R2-W1 (b, e), R2-W8 |
| §8.4 | final degeneracy FAULTs; gate-only delete; before-rental rule | R2-W10 (e), R2-W1 (a, d) |
| §9 | gate-only S1 and host material | R2-W1 (c, d) |
| §10 | t1table without `manifests`; selftest items | R2-W5, R2-W1, R2-W3, R2-W7 |
| §11 | rows 2a, 2b, 4 (NB-5), 9, 9a; footer: tier-1 rows not cited in the paper | R2-W2, R2-W4, NB-5, R2-W6 |
| §12 | Q10 answered; P1 / P2; PI-1109d; no open question | R2-W1 (g), R2-W9 |
| §13 | round 3/3 | R2-W1 (h) |
| §14 | item 2 (PI lines), item 8 (P1) | R2-W1 (h), R2-W9 |
| §15-§16 | rewritten / new | R2-W1 (h) |
| Appendix A | v1.2 shas | record |
| Appendix B | row 8 (per subcommand), rows 13-14, row 15 (gate-only) | NB-2, R2-W5, R2-W1 (c) |
| Appendix C | material table per branch; gate-only delete | R2-W1 (c, d) |
| Appendix D | regenerated (D.1, D.2) | R2-W3 |

---

## Appendix A. sha256 of files cited

v1 Appendix A is carried unchanged. Added in v1.1:
```
8ea61b114050558f…  .session_backup/2026-10-13/decisions/CC-299.txt
4a77f897977e8018…  manuscript/reviews/C_DIAG_codex_read.md
595019fb5bc29b43…  manuscript/reviews/C_META_REVIEW.md
e4ff1603365720be…  manuscript/journal_draft_C/06_results.md
95d2ad861c1f0f83…  manuscript/journal_draft_C/11_supplement_registered_rows.md
8a444378bc9e0568…  manuscript/journal_draft_C/03_method.md
e9c049556bc684ed…  manuscript/prereg/2026-11-02_c_pvr_tier1/AMENDMENT_HOST_3090_DRAFT_v3.md
90240f83cae072e1…  manuscript/prereg/2026-11-01_b_pa1_tier1/B_RUN_DOC_v1_1.md
4779edd0e57057b50ff5710f4a78f876a4815f0a74348a83357073f179b1eafa  .session_backup/2026-10-26/c_test/staging/xm_test2500_data.json
9ae7c0ac4bb065ca…  .session_backup/2026-10-26/c_test/staging/xm_test2500.sha256
2a68a3eb4d41926deb524aa8f98c80f112472474906d73d9763c790fb0cac847  data/datasets/openviic/uit-openviic-annotation-dev.json
72ee9b57c350fb5f215e1f04701c515a51e5e415240e51a77c8ce00ce6316a0f  data/datasets/ktvic/train_data.json
d757520e76b8490df6c7275c2beb8b3ecef0342635a436bea8c3cfd07eb49df0  data/datasets/openviic/uit-openviic-annotation-train.json
8bdc38ec2b89078040c677abbbaec29258cb446b1d916cab1bbd606c6bfaab31  ~/s11pull_1107/final/c_pvr_out/out/xm3600_vi.PVR-drop.jsonl
ca7a9a208ab8f3c35c12c633a67cb065a13207343b60c71afd3c570fb62b6450  ~/s11pull_1107/final/c_pvr_out/out/xm3600_vi.PVR-keep.jsonl
7cf129106dd0ef2c382f4a9a4fd480295e5fc36e3e81b6522439370d500850e8  ~/s11pull_1107/final/c_pvr_out/SHA256SUMS_tier1
de94294256789ebc3ad960162f468e8233597866013d5b4f9ffbccac7a18e4b5  scripts/c_test/score_t.py
bbc9278859f86d9ef8ec3e163974ab9179d74ebf56847e72e7fbef2d708f29ee  scripts/c_test/c_test_chain.sh
84a4373a0efb7fd6d93fe19b0e7ceb6c1b855c233d13b9b78a9a33655c9fdce3  data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv
```
CC-212 pre-guard comparators (W7; `.session_backup/machines/M3/root/outputs/`):
```
89713e89ecb893044ace5260d1b1a87842e52f585b16c73892772002654f8538  c_test/runs/ct_qwen25vl_7b_xm_test2500-ret-k8-first-T1.preds.json
813d2da26f84315421b447c0d4ee7db608d79925ab927e58ed1816a5ed642b66  c_test/runs/ct_qwen25vl_7b_xm_test2500-rand-k8-T1.preds.json
bc31f08fd822991448a62f1d5a3e81a02f457be2bc5ab46ca6343822c9c2b5b5  c_test/runs/ct_internvl3_8b_xm_test2500-ret-k4-last-T2.preds.json
be73fa22a184e0fca9a9ee9320ea39d4efb557c6e205868be1e804d85ccffca5  c_test/runs/ct_internvl3_8b_xm_test2500-rand-k4-T2.preds.json
9fa11f7bc552be6310f8ffa9526bcc375352ced54b45ef2cb8085ec87902c03a  c_stage2/runs/c2_qwen25vl_7b_ov_dev_b-ret-k8-first-T1.preds.json
53ce8591417cbffe2d6d9368eb5bfd46b123ce695d8cdd6e936faadf7b7118a1  c_stage2/runs/c2_qwen25vl_7b_ov_dev_b-rand-k8-T1.preds.json
b05d9163aa9a85356d23d9ff50612750c1bbbf8022fed6caf9cb0476c35002fb  c_stage2/runs/c2_internvl3_8b_ov_dev_b-ret-k4-last-T2.preds.json
991d289bb43b1bcb935e3717aede594147ba533da723501ae473f9af87f43a5b  c_stage2/runs/c2_internvl3_8b_ov_dev_b-rand-k4-T2.preds.json
```

Added in v1.2:
```
d97ccfd00e17741dece653be4714464b09af27e1d9dd91748b170d34c429e371  .session_backup/2026-10-13/decisions/CC-299r2.txt
4f63f301ca2b1d5544874da552b0912b9153dad261bbe5797857cb28a9fc1a91  manuscript/reviews/C_DIAG_codex_read.md (round 2 appended)
6524845490e633000296658abc22b88180439e8537b3b7274c8af70fc6143bd6  manuscript/prereg/2026-11-01_b_pa1_tier1/B_RUN_DOC_v1_2.md
cafdcb83a7f92c5bb4498eda68c0ae693f8a072a1f54e7831cfbd9f1e63f6389  manuscript/journal_draft_C/05_preregistration_and_analysis.md
c472fb827069a88769f2783d08c37bf5c0408d7dc112fcaa39ca28385be79e62  manuscript/prereg/2026-11-08_c_diag/C_DIAG_PREREG_DRAFT_v1_1.md
4849a08f1fc384f1901fd294950f9ea20a5622879838c4a5ecac73cec62c3efe  ~/c_pvr_h4_1107/MANIFEST.sha256 (TMAN; from LOG / S11 docs, not re-hashed here)
f81323d1…  ~/c_pvr_h4_1107/manifest/xm3600_vi.json (8-hex prefix, LOG l.1763; full sha written by the §4.5 step)
```

## Appendix B. [W10] Input allow-list (path, sha256); every other open is a FAULT

| # | path (repo-relative unless `~`) | sha256 (8 hex; full in Appendix A or the v1 Appendix A) | used by |
|---|---|---|---|
| 1 | `manuscript/prereg/2026-10-22_c_stage1/lists.json` | 5c479f03 | lists, image sha lists |
| 2 | `manuscript/prereg/2026-10-22_c_stage2/frozen_config.json` | 2f0c32be | configs |
| 3-5 | `.session_backup/machines/M3/root/outputs/c_test/ex_xm_test2500.json`; `c_stage2/ex_ov_dev_b.json`; `c_stage2/ex_xm_dev500.json` | 242b30a2; 072b17d1; 9a79b97d | exemplars |
| 6 | `.session_backup/2026-10-26/c_test/staging/xm_test2500_data.json` | 4779edd0 | XM references |
| 7 | `data/datasets/openviic/uit-openviic-annotation-dev.json` | 2a68a3eb | OV-dev-B references |
| 8 | `data/xm3600/oiv7_labels.json` | bac3953a | `label-subset` only (§2.4); **[NB-2]** the guard holds a per-subcommand list, so no other subcommand can open it (checked at the code read) |
| 9 | the label subset written at Stage 0 | `<Stage-0 sha>` | gate, floor, scoring |
| 10 | `data/xm3600/vi_oiv7_map.json`; `data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv` | 27f2b1ca; 84a4373a | class map |
| 11 | `data/datasets/ktvic/train_data.json`; `data/datasets/openviic/uit-openviic-annotation-train.json` | 72ee9b57; d757520e | demonstration captions |
| 12 | the eight CC-212 `preds.json` of Appendix A | as listed | parity, VI-script precondition |
| 13-14 | (moved) the §4.5 inputs are read only by `c_diag_t1table.py`, under its own nine-entry list (§4.5) | — | — |
| 15 | XM-dev500 gate, XM-test2500 and OV-dev-B image files | per-file shas from `lists.json` / `staging/xm_test2500.sha256` (9ae7c0ac) | push. **[R2-W1 (c)] Gate-only branch: the XM-dev500 gate query images only**; the push manifest of that branch lists no XM-test2500 or OV-dev-B file |
| 16 | the VnCoreNLP jar and model files | `CIDER_VI_PIN_v1_1` §3 | segmenter |
| 17 | code files | `scripts/c_diag/SHA256SUMS` and the §10.1 pins | imports |

- **Deny backstop (§2.3):** evaluated only for paths not on this list. The list is part of the registered bytes; adding a
  path needs a new version and a re-read, so the backstop cannot be bypassed by a quiet edit.
- The test annotation files are refused by path and are never opened or hashed by C-DIAG code.

## Appendix C. [W8, Q9] C-DIAG host amendment (draft; one-judge read, 85, before any rental)

**Title.** Host amendment HD-1 to C-DIAG: one rented RTX 3090 / 3090 Ti for the C-DIAG dev-role decodes.

**Licence.** PI-1104af (LOG l.1530), extended by PI-1109a Q9 to C-DIAG's XM3600 pixels on the tier-1 conditions. It
follows `AMENDMENT_HOST_3090_DRAFT_v3.md` (5d6f5ca) §1-§4 in form. It does not amend that file, and it widens no other
licence.

1. **Host class.** One 1× RTX 3090 / 3090 Ti 24 GB offer of GPU_RENTAL_SPEC with the PI-1107a CPU floor. It is named
   "HD-1" in the rental LOG line; its address lives only in `~/.ssh/config`.
2. **One tenant.** From rental to delete, HD-1 holds only C-DIAG's job and files. Another paper may use it only after
   the logged C-DIAG deletion, under its own GO and money line; otherwise it is deleted.
3. **tmpfs only.** Every image and every demonstration-caption file goes only to `/dev/shm/c_diag_hd/` (mode 0700),
   never to disk. Weights and code may sit on disk; the machine delete removes them. Every file is sha-checked on
   arrival against the Stage-0 manifest, and a mismatch is a FAULT. No third-party storage is used.
4. **Covered material (and nothing else):**

   | material | class | main branch | gate-only branch [R2-W1 (c)] |
   |---|---|---|---|
   | XM-dev500 gate query images (only those in the gate sample) | spent XM3600, custody | yes | yes |
   | XM-test2500 images (2,500) | spent XM3600, custody | yes | **no** |
   | OV-dev-B images (925) | spent dev, non-custody | yes | **no** |
   | shown-caption texts of the CC-212 demonstrations (KTVIC / OpenViIC train) | datastore text | yes | only the gate units' texts, inside the gate unit file |
   | the gate unit file (ids and proposition texts, no status) | label-derived membership, disclosed (§2.4) | yes | yes |

   **Never on HD-1:** a label, status, label-derived mask, reference file, XM600 file, test-role file or any material
   not listed.
5. **Logs hold ids only.** Demonstration and caption text never appear in logs.
6. **Logged deletion.** In the gate-only branch the host is deleted right after the gate pull, whatever the verdict
   (§4.3). After the final pull the job deletes `/dev/shm/c_diag_hd/` and appends (utc, folder, file count,
   manifest count) to `c_diag_hd_deletions.log`, which is pulled. A trap deletes the folder on any exit. The coordinator
   writes the deletion LOG line, L-final, the machine delete and L-after.
7. **Backups.** The 30-minute backup loop never pulls `/dev/shm`. Its script is checked once for `/dev/shm` paths.
8. **Procedural isolation, disclosed.** The provider has root, so the isolation is procedural. Only spent sets and train
   caption text go there. This is the trade-off accepted in PI-1104af and PI-1109a.
9. **Registered line changed:** none in any committed file. This amendment adds C-DIAG's material under H-1's form
   ("a host HC-n named by the host amendment, for the sets and material of its §5 only"), with HD-1 and §4 above in
   place of HC-n and §5.

## Appendix D. [W1, R2-W3] Truth tables (regenerated for v1.2)

**D.1 Primitive → per-contrast P_obj state.** Primitives: guard ∈ {OK, GF, GC, GB}; Holm reject ∈ {T, F}; point ∈
{< 0, = 0, (0, SESOI_P), ≥ SESOI_P}; CI lower bound > 0 ∈ {T, F}; CI upper bound < 0 ∈ {T, F}. Only combinations
consistent with CI lower ≤ point ≤ CI upper are possible: 7 (point, CI) patterns × 2 Holm values = 14 per guard value,
56 in all.

| guard | Holm reject | point | CI lower > 0 | CI upper < 0 | state | count |
|---|---|---|---|---|---|---|
| GF / GC / GB | any | any | any | any | GF / GC / GB | 14 each, 42 |
| OK | T | ≥ SESOI_P | T | F | UP | 1 |
| OK | T | (0, SESOI_P) | T | F | UPs | 1 |
| OK | T | < 0 | F | T | DOWN | 1 |
| OK | every other consistent combination (Holm F; point = 0; or a Holm reject whose CI includes 0) | | | | NS | 11 |
| **total** | | | | | | **56** |

So UPs always has point < SESOI_P and CI lower bound > 0, and the S4/S4c sentence "precision rose (x [CI]); a rise of
SESOI_P is not shown" is true in every case where it is printed. DOWN always has its CI below 0.

**D.2 XM summary label (196 combinations).** States as in §6.4 and D.1.
- `filt − ret` ∈ {GF, GC, GB, UP, UPs, DOWN, NS}
- `filt − ctl` ∈ the same 7 states
- R_ok ∈ {T, F}
- C_ok ∈ {T, F}

| `filt − ret` | rows | label(s) |
|---|---|---|
| GF / GC / GB | 3 × 7 × 4 = 84 | S0 (28 each) |
| DOWN | 28 | S5 |
| NS | 28 | S6 |
| UPs | 28 | S4 when R_ok ∧ C_ok (7), else S4c (21) |
| UP, `filt − ctl` ∈ {UP, UPs} | 8 | S1 when R_ok ∧ C_ok (2), else S2 (6) |
| UP, `filt − ctl` ∈ {GF, GC, GB, DOWN, NS} | 20 | S3 when R_ok ∧ C_ok (5), else S3c (15) |
| **total** | **196** | each exactly one label |

The enumeration was re-run for v1.2 by a short script in the drafter's scratch (not committed). It printed: D.1, 56
primitive combinations → GF 14, GC 14, GB 14, UP 1, UPs 1, DOWN 1, NS 11, with every UPs at point < SESOI_P; D.2,
196 rows → S0 84, S1 2, S2 6, S3 5, S3c 15, S4 7, S4c 21, S5 28, S6 28. `test_c_diag.py` repeats both against the
scorer's functions.
