# T1-GUARD: amendment to C-PVR-T1 (CIDEr-VI guard form) — DRAFT v3, not approved

Status: DRAFT v3 for round 3/3 of CC-253 (full 3-judge panel plus a read-only Codex read; CC-253r2 NEXT_ROUND 80 on the pair, GUARD itself with no open BLOCKING item). Tier: IRREVERSIBLE, bar 85
(PI-1103ad, LOG l.1439; CC-253 TIER). It changes a registered STOP rule. It binds only after a GO and a gatekeeper
commit, and only if no tier-1 decode exists at the commit (§6).

v1 = `AMENDMENT_T1_GUARD_DRAFT.md` (226ac28c, 194 l.) and v2 = `AMENDMENT_T1_GUARD_DRAFT_v2.md` (f506df3f, 250 l.) are left
untouched. §11 lists the only changes v2 → v3 (CC-253r2 N7, N8, re-pin). §10 lists
every change against v1 with its source.

Written 2026-11-05 (UTC). Planning text only: nothing was run, rented, decoded or committed. AI opinion throughout.

Amends `PREREG_DRAFT_v1_2.md` (sha256 0a2f0773…df2b, committed 8282874). Line numbers below come from `git show
8282874:<path>`, which is byte-equal to the working copy.

Sources:
- PI-1104ah (LOG l.1536): meta Q3 = YES, pool the two explore halves into one 1,306-image guard set.
- Plan `C_NEXT_STEPS_2026-11-04.md` S2 and §2.1 row 4.
- `C_TALLIP_2026-11-03_META_REVIEW.md` item 4 (R2 M1).
- CC-253 (9c6f55cb): MB6, CX1, N-1 to N-5, N-9.

## Tóm tắt cho PI (tiếng Việt)

- PI đã chọn gộp (PI-1104ah, Q3 = CÓ). Tập guard tầng 1 gồm hai nửa explore KTVIC và OpenViIC, 1.306 ảnh. XM3600 chỉ
  báo cáo, không làm cổng. Tầng 2 gộp hai nửa confirm (1.253 ảnh). δ_C giữ 2,0.
- Dạng đã đăng ký, khi Δ = 0, chỉ qua khoảng 0,416 (SD 18,53) hoặc 0,169 (SD 26,34). Dạng gộp qua 0,974 hoặc 0,783.
  Khi tác hại thật bằng đúng −2, xác suất lọt qua vẫn là 0,025.
- Bản v2 sửa số 0,447 → 0,446, bỏ chữ "cận dưới (Slepian)", ghi rõ việc bác bỏ NB-NOVAR của CC-220, và cố định tập
  tham chiếu dùng để tính DF của CIDEr.
- Rủi ro ở tầng 2: cổng G2 khi Δ = 0 qua 0,938 hoặc 0,588, thấp hơn mức 0,98. δ_C = 2,5 cho G2 là câu hỏi PI (CC-253
  PI 4). Đề nghị KHÔNG, mặc định 2,0.

## 1. The defect, recomputed from committed files

Inputs (numeric fields only; no caption text was opened):
- `data/results/metrics_v2/main_s42-short.cider.json` cea22ac6…, `main_s43-short.cider.json` 219b97e9…,
  `official-short.cider.json` d25ea28c… (all committed d8ee09e). Field read: `per_image["CIDEr-D"]`, 558 KTVIC-test
  images, the same id set in all three files.
- `manuscript/prereg/2026-11-02_c_pvr_tier1/c_pvr_lists.json` edb07fbb… (committed cc90c96): `halves.ktvic_test`
  explore 286 / confirm 272; `halves.openviic_test` explore 1,020 / confirm 981.

Paired per-image SD of the CIDEr-D difference (recomputed here):

| pair | meaning | SD, all 558 | SD, KTVIC explore half (286, by the §4.2 rule) |
|---|---|---|---|
| s42 − s43 | two near-identical systems | **18.53** (18.528) | 19.03 |
| s42 − official | two different systems | **26.34** (26.342) | 27.69 |

The §4.2 half rule applied to the 558 ids gives 286 explore images, the count pinned in `c_pvr_lists.json`.

**Basis registered: SD = 18.53 and 26.34, the two-decimal values.** Every probability in this file is computed from
these two values. The explore-half SDs are disclosed beside them as a check.

Caveats:
- these SDs come from trained KTVIC models, not from mBLIP ICL arms, so the real SD can be larger or smaller;
- no OpenViIC SD is on file, so the KTVIC SD is used for both sets;
- every probability below uses the normal approximation P(LB > −δ | Δ) = Φ((Δ + δ)/(SD/√n) − z), with z = Φ⁻¹(0.975) = 1.95996 for every number in this file, to the percentile
  bootstrap CI of §5.5.

PVR and A1 share the captioner, the prompt, k and greedy decoding, and differ only in the demonstrations. So the
near-identical pair (18.53) is the closer analogue. The registered figures still carry both.

Operating characteristics of the registered form (each condition is P(CI lower bound > −2.0 | Δ = 0)):

| condition (registered) | n | half-width at 18.53 / 26.34 | P pass, 18.53 | P pass, 26.34 |
|---|---|---|---|---|
| KTVIC explore half | 286 | 2.15 / 3.05 | 0.446 | 0.250 |
| OpenViIC explore half | 1,020 | 1.14 / 1.62 | 0.932 | 0.679 |
| XM3600-vi (in-sample) | 3,600 | 0.61 / 0.86 | 1.000 | 0.995 |
| **tier 1, all three jointly (per variant)** | – | – | **0.416** | **0.169** |
| tier 2, 2 contrasts × 2 confirm halves (272 / 981) | – | – | **0.156** | **0.025** |

How the joint rows are computed:
- They are products of the single-condition probabilities, so they assume independence and are approximate.
- At tier 1 the three sets are image-disjoint and the bootstrap resamples images, so the product is close to exact.
- At tier 2 the two contrasts share PVR and the same images. Their dependence is not modelled, so the tier-2 product is
  an approximation only, neither a lower nor an upper bound.

The order of magnitude is the point. A null-effect PVR is stopped more often than it passes, so the guard acts as a
superiority test. That is not the registered intent: v4.1 l.154 labels δ_C "lenient".

## 2. The fix (option (a); PI-1104ah Q3 = YES)

### 2.1 Tier 1 (amends §6.3 NB-NOVAR)

- **Guard set G1** = KTVIC-test explore half ∪ OpenViIC-test explore half: 286 + 1,020 = 1,306 images before §7.4. Any
  image that §7.4 or W25 removes leaves it before any decode. The final n is printed and pinned with the dev-W25 result
  (plan S7).
- **Per-image score.** CIDEr-VI per image is computed separately within each source set, against that set's own
  references.
  - The document-frequency (DF) corpus is fixed in G-7: the references of that source set's explore-half images that
    remain in G1.
  - Two reference corpora are never mixed in one CIDEr computation. Pooling only averages per-image scores.
  - The SD basis of §1 used DF over all 558 KTVIC references. This difference in DF corpus is disclosed and goes in the
    caveats.
- **Estimand.** Δ_G1 = mean over the G1 images of [s_i(variant) − s_i(A1)]. It is image-weighted: OpenViIC carries
  1,020 / 1,306 = 0.781 of the weight before §7.4.
- **CI.** The paired image bootstrap of §5.5 (B = 10,000, percentile 95%, seed 20261102), **stratified by source set**:
  each replicate draws the KTVIC and OpenViIC counts of G1 with replacement within each set, so the weights stay fixed.
- **Rule.** A variant passes δ_C iff the CI lower bound of Δ_G1 > −δ_C, with δ_C = 2.0 (unchanged, v4.1 l.154). The δ_R
  clause is unchanged.
- **Why XM3600-vi leaves the gate.** XM3600-vi is the set on which SESOI_P, the UNCERTAIN variant and the go/stop are
  selected (§12, NB-INSAMPLE). A guard measured on the selection set adds no independent check, and at n = 3,600 its
  pass rate at Δ = 0 is already 0.995–1.000. So it gates nothing and only stays descriptive.
- **Descriptive only (never gating):**
  - XM3600-vi ΔCIDEr-VI(variant − A1) with its CI, labelled in-sample;
  - the per-set Δ with CIs for the KTVIC and OpenViIC explore halves.
- **Unchanged:** the STOP clause, l.476-477. The guard STOPs tier 1 only if neither variant passes.

### 2.2 Tier 2 (amends §5.3(3); binding on the tier-2 prereg)

- **Guard set G2** = KTVIC-test confirm half ∪ OpenViIC-test confirm half: 272 + 981 = 1,253 images before NB-T2POOL.
- **DF corpus.** The references of each source set's confirm-half images that remain in G2 (G-7).
- **Same rules as §2.1:** per-set scoring, image-weighted estimand, stratified bootstrap.
- **Rule.** Both ΔCIDEr-VI(PVR − A8) and ΔCIDEr-VI(PVR − A1) on G2 need a CI lower bound > −δ_C, with δ_C = 2.0.
- Per-set Δ with CIs are reported, never gating.
- **Tier-2 path risk, recorded (CC-253 N-9).**
  - G2's approximate pass rate at Δ = 0 is 0.938 (SD 18.53) or 0.588 (SD 26.34). Both are below the 0.98 rehearsal
    norm.
  - δ_C = 2.5 for G2 (0.995 / 0.845) is a PI question for tier 2 only, to be decided before any tier-2 data (CC-253 PI
    question 4). Recommended NO; default 2.0.
  - The tier-2 prereg recomputes this at the final G2 n.

### 2.3 Why pooling, not options (b) or (c)

- (b) "per-set reporting, CI condition on the pooled set only" is the same rule as (a). Its reporting is already in
  §2.1.
- (c) widens δ_C per set. Giving the 286-image KTVIC half 0.80 power at Δ = 0 needs δ_C = 2.80 × SD / √286: **3.07** at
  SD 18.53, **4.36** at SD 26.34. On KTVIC test the mean per-image CIDEr-D of the trained s42 system is 17.32, so a 3–4.4
  point margin is not "lenient".
- Pooling keeps δ_C at 2.0 and fixes the power through n.

### 2.4 Overrule, stated (CC-253 Ruling 10, N-5)

- **Overruled:** CC-220 NB-NOVAR (CC-220.txt l.59), "state the δ_C test form at tier 1". It produced the registered
  three-set form at prereg §6.3 l.472-475.
- **Replaced by:** the G1 form of §2.1, under PI-1104ah Q3 = YES (LOG l.1536).
- **Kept:** NB-NOVAR's STOP part ("if neither UNCERTAIN variant passes δ_C/δ_R, STOP before tier 2").
- **Not adopted:** options W and F (§4). They stay off without a new PI line.

## 3. Operating characteristics of the fix

Normal approximation as in §1; δ_C = 2.0 unless marked. n = 1,306 before §7.4.

| Δ (variant − A1, CIDEr-VI points) | G1 pass, SD 18.53 | G1 pass, SD 26.34 | G1 pass, δ_C 2.5, 18.53 / 26.34 |
|---|---|---|---|
| 0 (no harm) | **0.974** | **0.783** | 0.998 / 0.929 |
| −0.5 | 0.833 | 0.539 | 0.974 / 0.783 |
| −1.0 | 0.496 | 0.278 | 0.833 / 0.539 |
| −1.5 | 0.162 | 0.101 | 0.496 / 0.278 |
| −2.0 (harm = margin) | **0.025** | **0.025** | 0.162 / 0.101 |
| −3.0 | < 0.001 | < 0.001 | 0.002 / 0.004 |

- **Harm control.** At Δ = −δ_C the pass rate is 0.025 for every n. Pooling does not loosen the bound on a harm of the
  registered size. It removes only the false STOP at Δ = 0.
- **Check at the explore-half SDs** (19.03 / 27.69): G1 pass at Δ = 0 is 0.967 / 0.742.
- **Tier-1 STOP from the guard alone.** A STOP needs both variants to fail. At Δ = 0 for both variants, P(STOP) ≤ 1 −
  0.974 = 0.026 (SD 18.53) or ≤ 0.217 (SD 26.34). Under the registered form, a single variant fails about 0.58 / 0.83
  of the time (1 − the joint product).
- **Tier 2, G2 (1,253), two contrasts, Δ = 0.** Product under independence, approximate: 0.938 (SD 18.53) or 0.588
  (SD 26.34). With δ_C = 2.5: 0.995 / 0.845.
- **Final n (CC-253 N-3).** The result line of the dev-W25 run (plan S7) recomputes the G1 and G2 rows at the final n
  after §7.4 / W25, as a descriptive note. Papers state the final n only, never 1,306 or the difference (PI-1101o).

**Known weakness: masking.** A harm confined to the smaller set is diluted by pooling (weight 0.219).

| KTVIC-only harm h (OpenViIC Δ = 0) | pooled Δ | G1 pass, 18.53 | G1 pass, 26.34 | option F: P(KTVIC point > −4), 18.53 / 26.34 |
|---|---|---|---|---|
| −3 | −0.66 | 0.745 | 0.453 | 0.819 / 0.740 |
| −5 | −1.09 | 0.423 | 0.236 | 0.181 / 0.260 |
| −8 | −1.75 | 0.070 | 0.053 | < 0.001 / 0.005 |

Per-set Δ stays descriptive, so a set-confined harm is visible in the report but does not STOP.

## 4. Options not adopted (recorded; off without a new PI line)

| option | text | cost at Δ = 0 | gain |
|---|---|---|---|
| W: δ_C = 2.5 | "δ_C = 2.5" in §2.1 and §2.2 | none; pass rises to 0.998 / 0.929 (G1) and 0.995 / 0.845 (G2) | P ≥ 0.9 under the larger SD at tier 1. A −2.0 harm then passes 0.162 / 0.101 |
| F: per-set floor | add "and the per-set point estimate of Δ > −2δ_C (−4.0) on each source set" | P(KTVIC point > −4 \| 0) = 0.9999 / 0.995; OpenViIC > 0.9999 | stops a KTVIC-only harm of −5 with 0.82 / 0.74 |

## 5. Registered lines changed (old → new)

| # | where (8282874) | old (quoted) | new |
|---|---|---|---|
| G-1 | §6.3 l.472-475 | "a variant "passes δ_C" iff the paired image-bootstrap (§5.5) 95% CI lower bound of ΔCIDEr-VI(variant − A1) > −δ_C (2.0) on each of XM3600-vi (in-sample), the KTVIC-test explore half and the OpenViIC-test explore half; it "passes δ_R" iff …" | "a variant "passes δ_C" iff the stratified paired image-bootstrap (§5.5 settings; strata = source set) 95% CI lower bound of ΔCIDEr-VI(variant − A1) > −δ_C (2.0) on the pooled guard set G1 = KTVIC-test explore half ∪ OpenViIC-test explore half (per-image CIDEr-VI computed within each source set, DF corpus per G-7; image-weighted mean). XM3600-vi and the per-set halves are reported with CIs, descriptive and never gating. It "passes δ_R" iff …" (δ_R text unchanged) |
| G-2 | §5.3 l.397-398 | "3. ΔCIDEr-VI(PVR − A8) and ΔCIDEr-VI(PVR − A1) on the KTVIC and OpenViIC **confirm halves**: CI lower bound > −δ_C (δ_C = 2.0, labelled lenient; v4.1 l.154);" | "3. ΔCIDEr-VI(PVR − A8) and ΔCIDEr-VI(PVR − A1) on the pooled guard set G2 = KTVIC confirm half ∪ OpenViIC confirm half after NB-T2POOL (same scoring, DF rule G-7, estimand and stratified bootstrap as §6.3): CI lower bound > −δ_C (δ_C = 2.0, labelled lenient; v4.1 l.154); per-set values descriptive;" |
| G-3 | §6.3 l.469-470 | "(iii) choose the variant with the higher dev P_obj^VI that passes δ_C (CIDEr-VI) and δ_R vs A1" | unchanged text. "passes δ_C" now means the G-1 form |
| G-4 | §4.2 l.348 | "XM3600-vi CIDEr-VI is labelled in-sample." | unchanged; add: "XM3600-vi CIDEr-VI is descriptive only (T1-GUARD)." |
| G-5 | §4.1 table l.331 role | "… CIDEr-VI dev (in-sample)" | unchanged text. Its guard role ends by G-1 |
| G-6 | new | – | the power statement of §3 (Δ = 0 and harm rows, both SDs) is registered as the guard's operating characteristics. PAPER gives δ_C's one-sentence reason and states that the guard is measured on in-domain queries and does not transfer to NoCaps (meta item 4, R1 m4, R4 m9) |
| G-7 | new | – | "CIDEr-VI DF corpus: per source set, the references of that set's guard-half images that remain after §7.4 / W25 (tier 1: explore half in G1; tier 2: confirm half in G2). Never pooled across sets." |

Lines not changed: δ_C = 2.0, δ_R, the STOP clause (l.476-477), the §5.5 B, seed and percentile form, the half rule
(§4.2), and §5.4 (tier 3 has no CIDEr-VI).

## 6. Timing condition (binding)

- This amendment is valid only if no tier-1 output exists when it is committed.
- Evidence now:
  - no C GPU host exists since M1 was deleted (LOG l.1375, OPS-1103m1-deleted);
  - the host amendment is committed (5d6f5ca, e9c04955), but it licenses no rental by itself: the rental trigger is the
    tier-1 run doc GO (plan S11), which has not been written;
  - the LOG has no C speed-test or decode line.
- The gatekeeper re-checks the LOG at commit. If any C tier-1 decode line exists by then, this amendment goes to the
  tier-2 prereg instead (meta-review "Decision", l.57).

## 7. Change table (against the registered prereg)

| id | section | type | effect |
|---|---|---|---|
| G-1 | §6.3 NB-NOVAR | registered STOP form | three per-set gates → one pooled gate (G1, 1,306); XM3600 descriptive; CC-220 NB-NOVAR form overruled (§2.4) |
| G-2 | §5.3(3) | registered tier-2 PASS condition | four per-set gates → two pooled gates (G2, 1,253) |
| G-3, G-5 | §6.3 (iii), §4.1 | meaning only | follow G-1 |
| G-4 | §4.2 | added sentence | XM3600 CIDEr-VI descriptive |
| G-6 | new | registered power statement | §3 table |
| G-7 | new | registered DF corpus | per source set, per half, after §7.4 / W25 |

## 8. Rulings needed

| # | from | question | recommended | default if no answer |
|---|---|---|---|---|
| R-G1 | panel + Codex | Adopt G-1, G-2 and G-7 (pooled guard sets, per-set scoring and DF, stratified bootstrap) as PI-1104ah Q3 chose? | YES | registered form stands (near-automatic STOP) |
| R-G2 | panel | Are MB6 (0.446), CX1 (products under independence, approximate; no Slepian bound) and N-1 to N-5 and N-9 closed? | YES | – |
| R-G3 | panel | Is the SD basis (18.53 / 26.34 from KTVIC trained-model pairs, both carried, DF-corpus difference disclosed) adequate before any mBLIP output? | YES | as written |
| PI 4 (CC-253) | PI | δ_C = 2.5 for G2 at tier 2 (before any tier-2 data) | NO, keep 2.0 | 2.0 |

## 9. Drafting-touch disclosure

Read:
- the three `.cider.json` files above (field `per_image["CIDEr-D"]`, numbers only; ids used only for the §4.2 half
  rule);
- `c_pvr_lists.json` (`halves` counts);
- CC-253, CC-220.txt l.59, and the CC-253 workflow journal (judge returns).

Not opened: any caption or reference text, any NoCaps, TextCaps or OI test file, any label file, `~/.vsps_sealed`.

Computation: Python stdlib `statistics.NormalDist` on the laptop, no network.

## 10. Change table against v1 (226ac28c)

| # | v1 place | v2 change | source |
|---|---|---|---|
| V-1 | §1 table, KTVIC 286 at SD 18.53 | 0.447 → **0.446**. The basis is pinned as the two-decimal SDs; every number was recomputed from them (Φ = 0.44644) | CC-253 MB6 |
| V-2 | §1 "positively correlated … at least the product (Slepian)"; §3 "the product is a lower bound" | the joint rows are now products under independence, approximate. At tier 1 they are close to exact (image-disjoint sets). At tier 2 the dependence is not modelled and no bound is claimed | CC-253 CX1 |
| V-3 | status line, VN summary, §8 "PI Q3 … No PI line" | PI-1104ah Q3 = YES cited; the default row is removed | CC-253 N-1 |
| V-4 | §2.1, §2.2 | DF corpus pinned as new row G-7 (tier 1 explore half, tier 2 confirm half, after §7.4 / W25); the DF difference from the SD basis is disclosed | CC-253 N-2 |
| V-5 | §3 | the final-n recomputation goes in the S7 result line as a descriptive note; papers give the final n only | CC-253 N-3; PI-1101o |
| V-6 | new §2.4; §2.1 | CC-220 NB-NOVAR form explicitly overruled; one sentence on why XM3600 leaves the gate; W and F off without a new PI line | CC-253 N-5, Ruling 10 |
| V-7 | §2.2, §4 | G2 tier-2 path risk (0.938 / 0.588 < 0.98) recorded; δ_C 2.5 for G2 is a PI question, recommended NO | CC-253 N-9, PI question 4 |
| V-8 | §6 | timing evidence updated: host amendment still in draft (CC-254) | CC-254 Item 2 |
| V-9 | header | v2 status, round 2 of CC-253 | CC-253 NEXT STEP |

## 11. Change table against v2 (f506df3f)

| # | v2 place | v3 change | source |
|---|---|---|---|
| X-1 | §1 caveat formula | one z throughout: z = Φ⁻¹(0.975) = 1.95996, the value every number was computed with. No number changes (0.44644 → 0.446) | CC-253r2 N7 |
| X-2 | §6 timing evidence | "host amendment still in draft" replaced: the host amendment is committed at 5d6f5ca, and no tier-1 run doc or rental exists | CC-253r2 N8 |
| X-3 | header | v3 status for round 3/3; every other line is byte-equal to v2 | CC-253r2 NEXT STEP (re-pin) |
