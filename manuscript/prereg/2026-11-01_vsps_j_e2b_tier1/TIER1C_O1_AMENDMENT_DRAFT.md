# VSPS-J E2b TIER-1c AMENDMENT (O1, draft): one post-hoc recall-parity config, one laptop screen on the select half

Status: DRAFT v1, drafting started 2026-11-03T00:05:24Z (`date -u`). Nothing is committed, run, logged or rented by
this file.
Tier: REVERSIBLE, bar >= 90 (CC-233 Ruling 4: drafting is GO; the CPU read needs its own ruling).
Label on every output: `TIER 1c / DEV-EXPLORE (POST HOC)`. Every estimate is AI opinion.

Licence chain:
- CC-233 (LOG l.1300) licenses drafting this file under O1-C1..C9.
- PI-1103c (LOG l.1302) chose O1 over O2. If O1 fails, the path goes to O2, which needs its own irreversible ≥ 92 ruling.
- Not licensed by this file: the read itself, any GPU, any tier-2 or tier-3 data.

Sources:
- `P` = `PREREG_DRAFT.md` (6bf702a9, commit 26ae375).
- `A1` = `AMENDMENT_1_DRAFT_v1_2.md` (55aead20, commit 348b088).
- `RES` = `.session_backup/2026-11-02/e2b_score/res.json` (9b9c3f6e).
- `E` = `scripts/vsps_j_e2b/e2b.py` (d3aa5384).
- `T2` = `TIER2_AMENDMENT_DRAFT_v1_1.md`.
- `LOG` = `.session_backup/2026-10-13/decisions/LOG.md`.

## 1. What O1 is, and what it is not

- **The tier-1 record stays as recorded.** The winner `internvl3_8b|FA` keeps its thresholds, numbers and select-half
  CIs (RES; OPS-1102e2b-score, LOG l.1243), and they are reported. Q-T2-0 (CC-233 Ruling 2) stands: that frozen
  config gets no tier-2 decode.
- **O1 is a new config named `internvl3_8b|FA|1c`.**
  - It uses the same backbone, form, frame and probe masses as the winner. Nothing is decoded again.
  - Only its operating point is new: E2b sits 2 strict-recall points above Vintern's own design point, both fit on the
    tune half.
- **It is post hoc.** Both the +2.0 cushion and the parity rule were chosen after the select-half result was seen
  (Δrecall -2.79, RES). Its select-half read is a **futility screen**, never evidence for any claim (CC-233 Ruling 3b).
- **No re-selection.** None of the four tier-1 cells is chosen again. qwen3vl_8b FA (Δprec +5.03), qwen25vl_7b FA and
  qwen3vl_8b FB stay as recorded and are not re-read.

## 2. Registered rules O1 departs from (O1-C2, CC-233 W1)

| # | registered rule | where | O1 instead |
|---|---|---|---|
| R1 | E2b `t_lo` = the smallest GRID value with tune strict recall >= R_DESIGN 0.83 | `P` l.202-206; `E` `band` | E2b `t_lo` = the smallest GRID value whose tune strict-recall hits reach Vintern's own tune hits + ⌈0.02·n_false⌉ (§3). R_DESIGN no longer sets E2b's point |
| R2 | Vintern recall-matched to the config's tune recall (`match_lo`) | `P` l.208-211; `E` `vintern_fn` | Vintern at its **own F-A band** (R_DESIGN 0.83, the GRID, `hi_rule`), as `P` l.218 defines for PA2 and `E` `cmd_score` `vown` computes |
| R3 | "Thresholds from the tune half are final; never refit …; never touched on select or held images" | `P` l.212 | A second threshold set, for a new config. Still tune half only and never touched on select or held. The tier-1 thresholds are not changed |
| R4 | The candidate list is complete: "Nothing else" | `P` l.216-222 (§4.2) | One extra config outside that list. `pick()` is not run |
| R5 | The select half is for config choice only, scored once | `P` l.222-227; A1 D2; CC-225r3 5(c) | A second read of the select half, under its own command and once-guard (§6), as a screen only |

**What does not change:**
- GRID 0.05-0.95 (`E` l.61; a 0.01 grid would be a second post-hoc choice, O1-C2);
- `hi_rule` with the 12 % tune UNCERTAIN cap;
- `band_label` (p <= t_lo → REJECTED, p >= t_hi → SUPPORTED);
- the H1-H4 constants (`P` l.249-256);
- the NB-C6 estimator (`P` l.264-269), with n_T3 set to the screen value of §4;
- macro over {object, number} (`macro_pair`);
- the probe masses, M0 p_yes, segments and W25 lists.

**Meaning of H1 changes.** O1 compares E2b at 2 points above Vintern's tune recall against Vintern at its own design
point. That is a dominance comparison, not the recall-matched comparison of `P` l.33-37. Any text says so (O1-C8, §8).

## 3. The config `internvl3_8b|FA|1c` (rule fixed before the read)

Per type t, on the tune rows of the 662-image selection set only (`half == "tune"`, 324 images):

1. **Vintern.**
   - `(tV_lo, tV_hi) = band(p_V, y)` on M0 arm-A p_yes, i.e. the registered `band` code: the smallest GRID value with
     strict recall >= 0.83, then `hi_rule`.
   - k_V = the number of gold-false tune probes with p_V <= tV_lo; n_f = the number of gold-false tune probes.
2. **Target, in integers.**
   - k* = k_V + ⌈2·n_f / 100⌉, computed as `k_V + (2 * n_f + 99) // 100`.
   - Integer counts avoid float ties. A grid value whose E2b tune hits equal k* exactly reaches the target.
3. **E2b.**
   - `tE_lo` = the smallest GRID value t with #{gold-false tune probes with fa_p <= t} >= k*.
   - `tE_hi = hi_rule(p_E, y, tE_lo)` (unchanged, with the 12 % cap). `p_E = fa_p(mass)` (`E` l.790).
4. **No fallback, primary types.** For object or number, the config is **infeasible** if either:
   - no GRID value reaches k*; or
   - Vintern's band falls back to (0.5, 0.5).
   Infeasible means a SCREEN NO-GO and the path goes to O2. This is written into the output; no other value is tried.
5. **Descriptive types** (colour, attribute, action, relation). The same rule applies. If it is unreachable, the
   registered fallback (0.5, 0.5) is recorded. These types never enter the decision.
6. **Exactly one cushion value: +2.0 points** (= the H4 margin). No second value, grid or comparator (O1-C6).
7. **EN (for a later tier 2 only; never computed by the screen):**
   - The EN thresholds of `|1c` use the same rule, steps 1-6, on the tune rows of `internvl3_8b_FA_en`.
   - Vintern's side is its own VI band, unchanged. The tune keys are the same, so k_V is the same.
   - They are computed only by `freeze` (T2 D C1), after a SCREEN GO. The screen never opens the EN folder.

## 4. Data, decision rule and reports (O1-C4, C5)

**Inputs.** Everything is read once, sha-checked, and already pulled. No new data.

| input | path | pin |
|---|---|---|
| winner vi cell only | `/home/hoanguyen/vsps_j_e2b_runs/e2b_probe_final/internvl3_8b_FA_vi/` | probes.jsonl 498aea9e, OUT_MANIFEST f710d24b (OPS-1102e2b-cell2-done, LOG l.1234) |
| tier-1 guard | `…/e2b_probe_final/SCORED.json` | 0101821e, res_sha256 = 9b9c3f6e (OPS-1102e2b-score, LOG l.1243) |
| M0 arm-A p_yes | `/home/hoanguyen/vsps_j_m0_runs/m0_final/out/probes.jsonl` | cccd5e0e |
| segments and gold | `val_raw.json` via `sets_and_segments(data, w25_lists())` | 2cbc7942; W25 lists 5b496f6f |
| record check | RES | 9b9c3f6e; asserts `winner == "internvl3_8b|FA"` |

No other cell folder is opened, the EN folder `internvl3_8b_FA_en` included. That is the code-level form of "no
re-selection" (O1-C4, O1-C7).

**Decision rule.** The screen is SCREEN GO iff `ppass(rows, n_t3=1004, B_out=500, B_in=1000, seed=20261102)` gives
**P̂ >= 0.98**.
- `rows` = `per_image_counts(select, f1c_E, f1c_V)` over the **338 select-half images only**.
- Outer loop: `default_rng(20261102)`, 1,004 image rows drawn with replacement.
- Inner loop: the registered estimator (`paired_ci` logic: ratio per type, macro, difference), with B_in 1,000 and seed
  20261102 + b.
- PASS = H1 ∧ H2 ∧ H3 ∧ H4 at the `P` §5 constants:
  - H1: point >= 5.0 and LB > 0;
  - H2: U <= 15.0;
  - H3: Δret LB > -2.0;
  - H4: Δrecall LB > -2.0.
- **Undefined replicates.** An outer replicate is **not passing**, and is counted, if either:
  - its own point is undefined (a primary type with no REJECTED); or
  - its inner run drops > 1 % of replicates.
- **1,004 is a screen parameter**, taken from A1 l.330 (AMBER generative 1,004; never fetched). It is **not** a registered
  tier-3 n; tier 3 is not chosen (`P` l.266-270).
- **Implied SESOI** (feasibility output, section C): at n = 1,004 the screen needs a select-point Δrecall of about +1.50
  or more and a Δprec of about 6.44 or more.
- The screen is **lenient by construction.** It is a plug-in: it resamples from the 338 and ignores their own sampling
  variance. Tier 2 re-tests on fresh data (CC-233 Ruling 3d).

**Reported beside the decision (descriptive, never an input to it):**
- MC SE = sqrt(P̂(1 − P̂)/500).
- **Predictive P̂.** The outer replicate first redraws the 338 select images (seed 20261105), then draws 1,004 from that
  redraw. The inner loop is unchanged.
- Select-half `paired_ci` (B 10,000, seed 20261101): Δprec, U, Δret, Δrecall; per-type tables for both systems;
  thresholds; tune hits k_V, k*, and E2b's tune hits.
- **Held 107, report-only** (Q-T2-B YES; O1-C4): `table()` for both systems on the held images. This is the first
  directly computed Vintern held column. It is never read by the decision function, and the selftest asserts that.
- The tier-1 winner's RES numbers, quoted unchanged beside O1's.

**Output.**
- `res_1c.json` is written first in the ext4 runs folder (`/home/hoanguyen/vsps_j_e2b_runs/e2b_probe_final/`), created
  with O_EXCL.
- It is labelled `TIER 1c / DEV-EXPLORE (POST HOC)`, with `screen` = "SCREEN GO", "SCREEN NO-GO" or "INFEASIBLE".
- Then the guard `SCORED_1C.json` is written (§6).
- Only after both exist is a byte copy placed in `.session_backup/2026-11-03/e2b_t1c/`. The copy's sha must equal the
  guard's.

## 5. Feasibility of the screen and the estimates (CC-233 W2, NB7)

**Reproduce script (re-created; the scratchpad copy was lost in the /mnt/d outage, OPS-1103-eio).**
- `.session_backup/2026-11-03/e2b_t1c/feasibility.py`, sha256
  07fc0e33335dea98727b714ea19a3277c1c6780721fa7872142327d34bc41790. It reads only RES 9b9c3f6e.
- Output: `.session_backup/2026-11-03/e2b_t1c/feasibility_out.txt`, sha256
  c307e49acef1cc835cf3f26e8c9364421222cf05dacf981e990e6f72f531ebbc.
- Run as `python3 -I .session_backup/2026-11-03/e2b_t1c/feasibility.py .session_backup/2026-11-02/e2b_score/res.json`.
- Its numbers equal CC-233's recomputation:
  - plug-in P(H4) at n = 1,004: 0.0021;
  - predictive P(H4) at n = 1,004 / 2,300 / 4,300: 0.075 / 0.117 / 0.150.

**What O1 must overturn.** The tune → select drift of the frozen winner is about -2.8 points (macro; object / number):
- E2b tune 85.8 / 83.2 [measured, RES `tune_recall`] → select 82.2 / 80.2;
- Vintern tune >= 85.8 / >= 83.2 [derived: `match_lo`, ≈ under the no-tie case; RES stores no Vintern tune recall] →
  select 87.1 / 80.9.

If the same drift holds, a +2.0 tune cushion gives an expected select Δrecall of about -0.8. The screen needs about
+1.5. Moving Vintern to its own 0.83 point also tends to raise Vintern's REJECTED precision, which shrinks Δprec
(CC-233 Ruling 3c). res.json stores no Vintern own-band numbers (PA2 was void), so this cannot be checked before the
read.

| estimate (AI opinion) | judge (CC-233 Ruling 3c) | drafter |
|---|---|---|
| P(O1 passes its screen) | **about 10 %** | about 10-15 % (revised down from the 25-35 % of TIER2 v0, after Ruling 3c) |
| P(any route reaches a tier-2 GO; NB-C8 and a fresh tier-2 P̂ are also needed) | about 3-5 % | about 3-5 % |

## 6. Machine, caps, guard, stop (O1-C6, C7, C9)

- **Machine:** the laptop CPU only. GPU cap 0. Venv: `~/.venvs/vsps_j_m0` (the tier-1 `score` venv), run with
  `python -I`.
- **CPU wall cap: 1 h** from the command's start, checked between outer replicates. At the cap the command stops before
  `res_1c.json` and `SCORED_1C.json` exist. That is an operator FAULT with no outcome: one re-run under A1's
  operator-FAULT protocol, then a judge.
- **Cost estimate** [proposal]: 2 × 500 × 1,000 inner replicates on about 1,004 × 20 counts. About 1-3 min with numpy.
- **Effort cap:** 1 person-day, and only after the ready A/B/C steps (PI-1103c).
- **Once-guard:** `SCORED_1C.json` in the ext4 runs folder, holding {res_1c sha256, RES sha, input shas, utc}.
  - It is written only after `res_1c.json`, and its sha goes into an OPS line.
  - The command refuses to start if **either** `SCORED_1C.json` **or** `res_1c.json` already exists in the runs folder.
    A crash between the two writes therefore cannot open a second look; it goes to a judge.
  - `res_1c.json` is created with O_EXCL.
  - This command never writes or checks `SCORED.json` or `SCORED_EN.json`.
- **Stop condition (one shot):**
  - SCREEN NO-GO, INFEASIBLE, or no GO on this amendment within 2 judge rounds → **O2 automatically** (PI-1103c). O2's
    adoption as the VSPS-J path still needs its own irreversible ≥ 92 ruling.
  - No second cushion, grid or comparator variant, ever.
- **A SCREEN GO licenses nothing on GPU.** Tier 2 still needs all of:
  - NB-C8 met (a VALSE ledger decision, or CC-207 Q2 answered);
  - T2 with W1-W4 closed;
  - its own ≥ 92 ruling.
  In T2, `internvl3_8b|FA|1c` would be frozen **beside** the tier-1 winner; the winner's record is unchanged.
- NB-C8 does not bind this 0 GPU-h laptop re-read (CC-233 Ruling 3b). It binds any tier-2 cell.

## 7. Custody and sealing

- Read: dev only (M-HalDetect val tune and select masses, already scored).
- Opened as report-only: the held 107.
- Never opened: any tier-2 set (M-HalDetect train, Karpathy test instances), any tier-3 candidate (AMBER, VALSE),
  e-SNLI-VE, UIT-ViIC test.
- No new labels and no AI label as gold. No M-HalDetect text goes into any output.

## 8. Paper wording (O1-C8)

If O1 is ever reported, the text says three things:
- O1 is a post-hoc dev-explore config, chosen after the tier-1 select-half result was seen.
- It compares E2b against Vintern-1B at Vintern's own design point, not at matched recall.
- Its select-half figures are a screen and support no claim.

The tier-1 winner's numbers are reported as recorded.

## 9. Code changes O1 needs (names and places only; no code is written before this amendment's GO)

| # | file / place | change |
|---|---|---|
| K1 | `E` `paired_ci` (l.772) | Split out `ci_from_table(T, B, seed)` → (per-replicate stats, dropped mask). `paired_ci` calls it. No logic change; a golden-number test pins the equality |
| K2 | `E` new `point_from_rows(rows)` | The un-resampled ratio estimator (Δprec, U, Δret, Δrecall) on a count table, the same ratio-per-type-then-macro order as `paired_ci`; NaN when a primary type has no REJECTED |
| K3 | `E` new constants and `rules_pass(point, ci)` | `H1_MIN = 5.0`, `H2_MAX = 15.0`, `PASS_GATE = 0.98`, `N_SCREEN = 1004`, `B_OUT = 500`, `B_IN = 1000`, `SEED_T2 = 20261102`, `SEED_PRED = 20261105`, `CUSHION_PTS = 2`. H3 and H4 reuse `RET_MARGIN` (-2.0). Returns bool. H1 uses `>=` 5.0 and LB `> 0`; H2 `<=`; H3/H4 LB `>` |
| K4 | `E` new `ppass(rows, n_t3, B_out, B_in, seed, pre_n=None, pre_seed=None)` | Nested bootstrap of §4. `pre_n` / `pre_seed` give the predictive variant. Returns {p_hat, mc_se, n_undefined, B_out, B_in, seed, n_t3}. Checks the wall cap between outer replicates |
| K5 | `E` new `fit_1c(pE, pV, op)` | §3: Vintern `band`; integer k_V and k*; E2b smallest-GRID `tE_lo`; `hi_rule`; returns per-type thresholds plus {k_V, k*, kE, n_f, feasible}. Reads only `half == "tune"` rows |
| K6 | `E` new `cmd_screen_1c` + `main()` subparser `screen-1c` | Refuses if `SCORED_1C.json` or `res_1c.json` exists in the runs folder. Checks: RES sha 9b9c3f6e and its winner; `SCORED.json` res_sha256 = 9b9c3f6e; M0 via `m0_pv`. Loads **only** `internvl3_8b_FA_vi` via `classify` (DONE required; never `*_en`). Then `fit_1c` → label functions → `per_image_counts(select)` → `ppass` (decision) → predictive `ppass`, `paired_ci` and `table`s (report) → `held` tables (report-only, after the decision field is set). Writes `res_1c.json` (O_EXCL), then `SCORED_1C.json`, and prints the guard sha |
| K7 | `e2b.py` size | It is already over the size rule (A1 N19). K1-K6 add about 140 lines [proposal]. Recommended: put K2-K6 in a new `scripts/vsps_j_e2b/e2b_1c.py` that imports `e2b`, leaving `e2b.py` with K1 only (QJ5 / Q9 revisited) |
| K8 | `scripts/vsps_j_e2b/SHA256SUMS` | Add lines for `e2b_1c.py` and the changed `e2b.py` / `test_e2b.py` at the gatekeeper commit |

**Selftest plan (`test_e2b.py`; CPU, no weights, no data, sockets raise):**
- **T1 `fit_1c`, synthetic tune data with known counts:**
  - k* integer arithmetic: n_f 100 → +2; n_f 698 → +14 (⌈13.96⌉); n_f 50 → +1;
  - a grid value hitting k* exactly is accepted;
  - unreachable k* → `feasible False` on a primary type;
  - a Vintern (0.5, 0.5) fallback → infeasible;
  - `tE_lo` ∈ GRID;
  - `tE_hi == hi_rule(p, y, tE_lo)`;
  - select or held rows injected with extreme values leave the thresholds unchanged.
- **T2 `rules_pass` boundaries:**
  - Δprec point exactly 5.0 with LB 0.1 passes; LB exactly 0.0 fails;
  - U exactly 15.0 passes;
  - H3 or H4 LB exactly -2.0 fails.
- **T3 `ppass`:**
  - a toy with a large positive effect gives P̂ = 1.0; a toy with Δrecall -10 gives P̂ = 0.0;
  - the same seed gives the same P̂;
  - mc_se formula;
  - a toy with a primary type having no REJECTED counts as not passing, and is counted;
  - an inner-drop > 1 % replicate counts as not passing;
  - `pre_n` changes the outer draw only.
- **T4 K1 equality:** `paired_ci` on a fixed seeded table equals its pre-refactor golden output to 1e-12.
- **T5 `cmd_screen_1c` on a fake runs folder:**
  - a second run is refused (`SCORED_1C.json`);
  - RES sha, winner or SCORED.json mismatches are refused;
  - opening any folder other than `internvl3_8b_FA_vi` raises (open is patched);
  - held rows never reach `ppass` (the call arguments are spied);
  - `res_1c.json` exists before `SCORED_1C.json`;
  - an existing `res_1c.json` without a guard is refused;
  - the EN folder is never opened;
  - the wall-cap stop leaves neither file.

**Mutant plan (author mutants, each must be killed by T1-T5; judge mutants added at the code read):**

| # | mutant | killed by |
|---|---|---|
| M1 | cushion 2 → 0 | T1 |
| M2 | ⌈·⌉ → ⌊·⌋ | T1 (n_f 698) |
| M3 | `>=` k* → `>` | T1 (exact hit) |
| M4 | GRID → 0.01 steps | T1 (`tE_lo` ∈ GRID) |
| M5 | Vintern by `match_lo` instead of `band` | T1 |
| M6 | fit on tune ∪ select | T1 |
| M7 | held rows in `ppass` | T5 |
| M8 | n_t3 = 338 | T3 / T5 spy |
| M9 | seeds swapped | T3 determinism golden |
| M10 | H4 margin -3.0 | T2 |
| M11 | gate `>` 0.98 | T5 (P̂ = 0.98 toy) |
| M12 | undefined replicate counted as pass | T3 |
| M13 | once-guard removed | T5 |
| M14 | a non-winner cell opened | T5 |
| M15 | predictive P̂ used for the decision | T5 |
| M16 | `SCORED_1C.json` written before `res_1c.json` | T5 |
| M17 | infeasible primary type falls back to (0.5, 0.5) | T1 |
| M18 | the start check looks only at `SCORED_1C.json` (an orphan `res_1c.json` is accepted) | T5 |
| M19 | the EN folder is loaded as well | T5 |

## 10. Questions (each with a recommendation and a default)

| # | question | recommendation | default |
|---|---|---|---|
| Q1C-1 | Adopt §3 exactly: Vintern's own band, integer k* = k_V + ⌈0.02·n_f⌉, E2b's smallest GRID `t_lo` reaching k*, no fallback on primary types | **YES** | as written |
| Q1C-2 | K7: put the O1 code in a new `e2b_1c.py` (only K1 touches `e2b.py`) | **YES** (keeps `e2b.py` from growing) | new file |
| Q1C-3 | The descriptive types use the registered (0.5, 0.5) fallback when unreachable; they never enter the decision | **YES** | as written |
| Q1C-4 | The run slot: after the code read GO, on the laptop, in an idle window with no A/B/C laptop step running (EIO mitigation: one writer on /mnt/d) | **YES** | next idle window |

## 11. CC-233 closure map (O1 items)

| item | where |
|---|---|
| O1-C1 new name, label, record unchanged | header, §1 |
| O1-C2 departures with lines, GRID kept, post hoc disclosed | §1, §2 |
| O1-C3 `t_hi` by `hi_rule`, Vintern own band (`P` l.218), tie rule | §3 |
| O1-C4 no re-selection, one cushion, one select read, held report-only | §1, §3.6, §4 |
| O1-C5 decision rule, SESOI, MC SE, predictive | §4 |
| O1-C6 dev only, laptop, GPU 0, CPU 1 h, effort 1 day, one shot, fail → O2 | §6 |
| O1-C7 own once-guard, single runs folder | §4, §6, K6 |
| O1-C8 paper wording | §8 |
| O1-C9 a screen GO licenses no GPU | §6 |
| W1 (O1 part) | §2 |
| W2 | §5 |
| NB7 | §5 table |
| NB9 | §4 |
