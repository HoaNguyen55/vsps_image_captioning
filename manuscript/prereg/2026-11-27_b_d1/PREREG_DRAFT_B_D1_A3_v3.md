# B-D1/A3 preregistration DRAFT v2 (Paper B, LRE): FE-CERT against Lu et al.'s readings and a reference-member margin; the tone-placement axis beyond a scorer-and-tokenizer grid; the null level of the per-member test

Drafted 2026-11-27 (v1 at 09:22Z; v2 after ruling CC-505, 2026-11-27T09:36:27Z, NEXT_ROUND 74; v3 after ruling CC-505r2, 2026-11-27T09:46:59Z, CONDITIONAL GO 87) by agent b-d1. Status: **DRAFT v3. Not registered.** This becomes the registration once committed after the CC-505r2 record checks. The title line is unchanged from v2, because CC-505r2 R5 allows only this status line and the changes line.

- Until that commit, nobody computes, prints or opens any quantity defined below. That includes counts over subfamilies taken from the values in `DEV.json`.
- The PI rule (analyses of existing files are POST HOC unless registered first) applies: this file is that registration.
- Every number already printed in the paper, its result note or Online Resource 1 that touches an estimand here is listed in §2 and stays POST HOC.
- No caption text was read to write this draft. `DEV.json`, `V.json` and `RESULT.json` were opened for key names and hashes only. The printed counts of §2 were copied from the FE-CERT result note.
- Changes from v1: each CC-505 item is closed in place. The hunk map is in `V1_TO_V2.diff`.
- v3 after CC-505r2: only R1a–R1d (the wording of the 0.05 bar) and R2 (the pivot rule id) changed. The hunks are in `V2_TO_V3.diff`.

## 0. Sources (read-only)

| item | path | sha256 |
|---|---|---|
| Paper B text of record | `paper/rev_2026-11-15/paper.md` in the B repo at 13549e5 (copy `~/vsps_ro3/b_now3/`) | `e8d94fbe…` (CC-505 SUBJECT) |
| FE-CERT registration | `manuscript/prereg/2026-11-12_b_fecert/B_FECERT_PREREG_v1_1.md` | `736b7e6a8ea2007270a3329db7ad6a09197c4804c9bc3821ea6bd4ceb5a61aa0` |
| FE-CERT result note | `manuscript/prereg/2026-11-12_b_fecert/results/B_FECERT_RESULT_NOTE_v1.md` | at HEAD |
| FE-CERT code | `scripts/b_fecert/b_fecert.py` | `67e43dea1b37c3bbfaa3fe5081d6f3d36848397451ad0a24d67fa67389b06b59` |
| family code | `scripts/b_fecert/family.py` | `7cb2c69b8b7840388568fd5f9b248e2cf25df28185386be875a65d921a9e4178` |
| CIDEr-D implementation | `scripts/kit_b/protocol_pilot.py` (`Cider`, l.78–115) | `6aee428207a2d1a045cd72d054e26a2e2ac8d9c2e414cb0c161e3b95dffd92bf` |
| stage-1 output (development family on D) | `manuscript/prereg/2026-11-12_b_fecert/results/b_work/DEV.json` (OPS-1113cx-pin) | `88ff39aa9552b671a0e439aec961d0fefe02df1f52a2a5df9765a9d8226f7e8d` |
| stage-2b output | `…/b_work/RESULT.json` (OPS-1113de-pin) | `25614b469cf59dc61f15e839b89a8e78ca0b316905afc4bd2ae52eaa0d32b43a` |
| family, census, systems | `FAMILY.json` / `CENSUS.json` / `SYSTEMS.tsv` | `431d92a4…` / `2252167b…` / `30ac9555cd6cdc8fd50f47e637e734fac564c692605f590ba213a60a3be6e1a0` |
| Lu et al., arXiv 2611.04099 v2, PDF | `~/novelty90_A_work/fulltext/2611.04099.pdf` | `61a3d859772f3db2288b10c6455fbc8f00011682abc8c663587220fcbac5097a` |
| rubric | `RUBRIC_v1.md` | `3071ed8d6827c9ad00f13fd12f2b4c4c9dfdbc0d22a63115c31d02996eab0bcc` |

## 1. Where the comparisons live, and what is stored

- **What exists.** FE-CERT scored 1,123 comparisons: 1,101 in D and 22 first-look comparisons (FL).
  - D: the 73 own KTVIC test files plus the pair of the two published baselines, on 558 images and 2,790 spent references. Label DEVELOPMENT.
  - FL: 22 first scorings of other groups' released files. Their references include KTVIC and UIT-ViIC test references (result note l.1072, l.1091).
- **FL is not used anywhere in D1 or A3** (CC-505 B5). Any new analysis on FL would be exploration on a one-look test set. `V.json` is not an input.
- **Stored, per D comparison and per class** (a class is the members with identical tokens): `DEV.json::comparisons[i].classes[k] = {members, cider, rouge, bleu}`, each metric `[D, L, U, sd_boot]`, for F_dev (54 members: `syl`, `rdr`, `pyvi`).
- **Not stored:**
  - per-class statistics of the held-out members (`uts`). `RESULT.json::comparisons[i]` holds only `F`, `F_dev`, `changed_F` and `D_f0` (result note J3);
  - any per-image score.
- **Inputs for the re-score.** All are on the laptop with matching hashes, checked by sha256 only:
  - 73/73 own files equal to `SYSTEMS.tsv`;
  - the baselines `85a7dcdb…` and `b12747b5…`;
  - the references `cc22ec6a…`, equal to `FAMILY.json::refs_sha256`.
- **CPU only, no decoding.**
  - H3 needs only the stored class statistics of `DEV.json`.
  - H1 and H2 (the `uts` fold, AER) and A3 need a per-image × per-member CIDEr-D matrix: one re-score of the stored files with the FE-CERT scorer, unchanged, gated by G0 (§6).
  - This re-score of spent KTVIC references is licensed for D1 only, after the registration commit, label DEVELOPMENT (CC-505 ruling 7).
- **Swap identity** (CC-505 C2(b)). Document frequencies come from the references only (`Cider.__init__`). The per-image score of image i reads only hypothesis i and the references of i. A swap of the two captions of image i therefore multiplies `d_{i,f}` by −1 under every member f. A self-test confirms it (§6 S0).

## 2. Numbers already printed or seen (POST HOC; no rule below is decided by them)

On D unless stated:
- Over F_dev: 909 CERTIFIED, 59 FRAGILE (2 REVERSED), 133 NULL-STABLE, 936 significant under `f0`, 27 CHANGED.
- Over F: 908 CERTIFIED, 62 FRAGILE, 28 CHANGED.
- FRAGILE over F_dev 59/1,101 equals the H2 beside-row "contract-induced flip incidence" for fold `uts` (G_u = F_dev), so that cell is POST HOC.
- Held-out (`uts`) breaks of certificates over F_dev: 1 of 909 on D. This is the FE-CERT cell of fold `uts` in H1/H2. The FL figures (1 of 9; 2 of 72 in V) are printed but not used.
- NC control: syllable-family certificates broken by `rdr`/`pyvi` in 6 of 915 (r_NC 0.0066). Post hoc: all 6 NC breaks lie among the 54 near-margin syllable certificates (paper l.248).
- FE-PRED AUC of z_f0 for CHANGED: 0.8012 over D ∪ FL, and 0.9546 over the 946 comparisons significant under `f0` (extra row). The FE-CERT registration expected this (l.308).
- Table 7 rows (D ∪ FL): BLEU-4 over F 862 CERTIFIED; ROUGE-L 891; F without `ck` 919; with `chr` 893; without `pk` 925.
- **Per-level breaking counts** (result note n091–n136; `RESULT.json::counts.*.breaking_levels`; paper Fig. 2 and Table E2 of Online Resource 1). These count axis levels over the breaking classes of non-certified comparisons:
  - D over F_dev:
    - units: `syl` 654, `rdr` 573, `pyvi` 525;
    - tone: `tw` 575, `tm` 588, `tf` 589;
    - punctuation: `pk` 604, `pf` 617, `pa` 531;
    - case: `cf` 850, `ck` 902.
  - D over F:
    - units: `syl` 690, `rdr` 609, `pyvi` 561, `uts` 630;
    - tone: `tw` 821, `tm` 834, `tf` 835;
    - punctuation: `pk` 844, `pf` 875, `pa` 771;
    - case: `cf` 1,207, `ck` 1,283.
  - FL over F_dev and over F: n102–n112 and n125–n136, printed but not used.
- **Consequences for the design:**
  - A size-matched margin contrast judged on CHANGED is close to a function of the printed AUC, so it is not a criterion here.
  - The tone counts (`tm`, `tf` close to `tw`) are a seen neighbour of H3. §5 H3 says how its threshold avoids leaning on them.

## 3. Methods compared (exact rules as implemented)

Shared machinery, reused unchanged from `b_fecert.py`:
- `stats(d, W)`: `D` = mean per-image difference; `L`, `U` = 2.5th and 97.5th percentiles of `W @ d / n`; `sd_boot`.
- `W = boot_W(558, seed 20261112)`, B = 10,000, identical for every method, member and comparison.
- `sig`: +1 if `L > 0`, −1 if `U < 0`, else 0 (touching counts as not significant).
- Classes by token identity.

**M1 FE-CERT** (`certify`, unchanged): CERTIFIED with direction s over G if every class of G has `sig = s`.

**M1′ Lu union-of-ties.**
- Lu, verbatim: "the union-of-ties rule (declare tied if any flipping contract does)" (p. 14). "A pair is tied when a segment-bootstrap CI of the paired difference contains zero; orderings are claimed only for CI-excluding pairs (touching counts as tied)" (§5, p. 13).
- Each member of G is a contract, with the per-member CI above. An ordering is claimed iff no contract is tied.
- **Mixed-direction convention.** Lu leave this case undefined. If no contract is tied but the significant directions differ, no ordering is claimed.
- With this convention M1′ = M1 by construction. This is a **METHOD CHECK that cannot fail by design** (CC-505 ruling 2), not a hypothesis. The mechanical check requires equal verdicts on 1,101/1,101; otherwise it is a FAULT.
- Reported: the count of comparisons with every contract significant in mixed directions.

**M2 Lu AER ensemble reading.**
- Lu, verbatim: "(i) marginalization: report the registered contract-set average ρ̄(M) = E_{c∈C} z_c(ρ(M, c)), z_c the within-contract standardization over systems; (ii) tolerance: a pair is tied when a segment-bootstrap CI of the paired difference contains zero …" (§5, p. 13).
- Implemented as follows:
  - C = the members of the fold's certifying family G_u, equal weight per member, CIDEr-D only.
  - z_c: score minus the mean over systems, divided by σ_c, the SD (ddof 1) of corpus CIDEr-D under member c over all 75 files on the KTVIC list.
  - **σ_c is computed once on the full sample and held fixed across resamples. This is this registration's own convention.** Lu et al. do not state whether z_c is re-standardized within resamples. Fixing σ_c keeps the ensemble linear in the per-image differences.
  - Ensemble per-image difference `e_i = (1/|C|) Σ_c d_{i,c}/σ_c`; then `stats(e, W)`. Ordering a>b iff `L > 0`, b>a iff `U < 0`, otherwise tied.
  - Corpus CIDEr-D is the mean of per-image scores, so this is a faithful reading of Lu's (i)+(ii) (CC-505 ruling 1).
- Not implemented:
  - (iii) "prescription": the systems are fixed output files, with no seeds to prescribe;
  - (iv) "gate": vacuous, since every member passed the FE-CERT preconditions.
- Deviation: B = 10,000 shared image resamples, against Lu's R = 2,000.
- Sensitivity row (DESCRIPTIVE): weight per class instead of per member.

**M3 Reference-member margin at equal size.**
- `z_f0 = |D_f0| / sd_boot(D_f0)` under `f0` (`rdr.tw.pk.cf`).
- Candidates: comparisons of D with `sig_f0 ≠ 0`, ranked by `z_f0` descending, ties broken by id ascending.
- Claims: the top K, with direction `sign(D_f0)`.

**M4 Single contract `f0`** (DESCRIPTIVE): every comparison with `sig_f0 ≠ 0`.

**Size matching.** For methods X and Y in one fold, K = min(|C_X|, |C_Y|). Each method keeps its top K by its own margin: z_min for M1, z_f0 for M3, `|Δ_E|/sd_boot(E)` for M2. M3 is defined at the size of M1.

## 4. Criterion for H1/H2: survival under a unit held out of the certifying family

| fold u (held out) | certifying family G_u | breaking family H_u | data |
|---|---|---|---|
| `syl` | `rdr` ∪ `pyvi` (36 members) | 18 `syl` members | `DEV.json` |
| `pyvi` | `syl` ∪ `rdr` (36) | 18 `pyvi` members | `DEV.json` |
| `uts` | F_dev (54) | 18 `uts` members | re-score (G0) |

- `rdr` stays in every G_u because `f0` is an `rdr` member.
- **Break** (`held_break`, unchanged): a claim (c, s) breaks in fold u if some class of H_u has `sig ≠ s`. A class counts for a family when one of its members is in it.
- One unit = (comparison, fold), pooled over the three folds. Units share files and comparisons, so every p-value and bound is **nominal**.
- **Pool:** D only (1,101).
- **Deviation from Lu's flip definition.** The break here is CI-defined. Lu's held-out coverage (p. 14) uses "the point-level flip definition". Our coverage row is therefore not comparable with their 73%.

## 5. Hypotheses and rules (thresholds fixed in this file before any D1 quantity exists)

H1 and H2 use Holm at 0.05 over the **four one-sided exact binomial p-values**: H1 FE fewer breaks, H1 MG fewer, H2 FE fewer, H2 AER fewer. H3 and A3 have their own rules.

### H1: FE-CERT against the reference-member margin at equal size

- Estimand, pooled over folds at K = |C_FE,u| per fold:
  - b_FE = breaks among claims made by FE-CERT only;
  - b_MG = breaks among claims made by MARGIN only.
  - Shared claims break identically.
- Labels, in this order:
  1. n = b_FE + b_MG < 10: **NOT_EVALUABLE** (counts printed).
  2. Holm-adjusted p ≤ 0.05 for b_MG > b_FE: **SUPPORTED**.
  3. Holm-adjusted p ≤ 0.05 for b_FE > b_MG: **MARGIN BETTER**.
  4. Otherwise: **NOT SUPPORTED**.
- Bound from printed numbers only (CC-505 C7), stated in place of an expectation:
  - in fold `uts` at most 27 discordant claims per side, with FE-CERT at 1 break there;
  - the judge's estimate is P(n ≥ 10) ≈ 0.6.
  - No outcome is predicted here.

### H2: FE-CERT against Lu's AER ensemble at equal size

- Same estimand, order and rule as H1, with M2 in place of M3. Labels: **NOT_EVALUABLE / SUPPORTED / AER BETTER / NOT SUPPORTED**.
- Beside the label (DESCRIPTIVE, native size per method M1, M2, M4):
  - number of claims;
  - **held-out flip coverage**: among units with `sig_f0 ≠ 0` and a break of the `f0` direction under H_u, the share with no ordering claimed;
  - **false-tie analogue**: among units with `sig_f0 ≠ 0` and no such break, the share with no ordering claimed. It is an analogue only. Lu's false-tie rate is "a tie is declared while some single contract CI-excludes" (p. 14), a different quantity, and it is not compared with their 72–91% or 66.1%/88.0%.
  - Lu's contract-induced flip incidence over G_u (the share FRAGILE over G_u). The `uts`-fold cell is POST HOC (§2).

### H3: what tone placement changes beyond a scorer-and-tokenizer grid (CC-505 B3: option (ii))

**Why the unit axis is a tokenizer contract.**
- Lu et al.'s grids carry a tokenizer axis: "consecutive-scorer flip rates 5.0% (tokenizer)" (Table 3 notes, p. 12), and "the MT scorer and tokenizer axes persist [86]" (§4.4, p. 12). Their reference [86] is Post (2018), whose sacreBLEU tokenizers include language-specific ones.
- A Vietnamese word segmenter (`rdr`, `pyvi`) or whitespace syllables (`syl`) decides how a string becomes tokens before scoring. That is a tokenizer contract in Lu's sense.
- Punctuation handling (P) and case (C) are tokenizer or format options of the same kind (13a punctuation splitting; lowercasing).
- So U, P and C go **inside** the contract grid. None of them is credited as beyond Lu et al.

**Why tone placement is the caption-specific axis left.**
- T (`tw`, `tm`, `tf`) moves a tone mark between two vowels of the same syllable (oa, oe, uy). It is an orthographic normalisation of written Vietnamese, not a tokenizer choice, and Lu et al.'s grids do not vary it.
- A reader could file it under Lu's "output format" coordinate. The paper says so in one sentence.
- Two segmenters (`rdr`, `uts`) rewrite tone placement themselves (paper §6.1, toy strings), so T can split classes only under `syl` and `pyvi`. This is a fact about the family, not an outcome.

**Grids** (all statistics stored in `DEV.json`; no re-score):
- G_contract = scorer {CIDEr-D, BLEU-4, ROUGE-L} × U {`syl`, `rdr`, `pyvi`} × P {`pk`, `pf`, `pa`} × C {`cf`, `ck`}, with T fixed at `tw`. That is 18 members × 3 scorers = 54 contracts.
- G_caption = all three scorers over all 54 F_dev members (162 contracts). It adds only the `tm` and `tf` levels.
- Verdict per grid: M1 (union-of-ties) over its contracts, which requires every contract to be significant in the same direction.

**Estimand.**
- n = comparisons of D certified over G_contract.
- k_T = those not certified over G_caption.
- Every such break comes from a class with T ≠ `tw`, so k_T measures tone placement alone.

**Threshold source** (CC-505 B3(b), first branch).
- The bands reuse the two constants that the FE-CERT registration fixed on 2026-11-12, before its stage 1 ran on 2026-11-13: R_MAX = 0.05, the bar of its held-out rule P1 (PASS at a one-sided 95% Clopper–Pearson upper bound <= 0.05, FAIL at a lower bound > 0.05) (v1.1 l.277, l.364; code l.70), and N_MIN = 59 (code l.69).
- The rule has the same form as P1: one-sided 95% Clopper–Pearson bounds against 0.05.
- **Stated honestly.** The decision to reuse these constants for H3 is made today, after NC 6/915 and Table E2 were printed. The values themselves were fixed before any FE-CERT number existed, and neither is tuned to the printed counts. The v1 bands (0.5% and 1%), which were chosen with NC in view, are withdrawn.

**Labels, in this order:**
1. n < 59: **NOT_EVALUABLE**.
2. Lower bound > 0.05: **SUPPORTED**. Tone placement overturns more than 5% of the certificates of a scorer-and-tokenizer grid.
3. Upper bound ≤ 0.05: **NULL**. Tone placement overturns at most 5% of the grid's certificates.
4. Otherwise: **INCONCLUSIVE**.

- Trip points (arithmetic only, CP via `scipy.stats.beta`):
  - n = 850: NULL iff k_T ≤ 31, SUPPORTED iff k_T ≥ 54;
  - n = 600: ≤ 20 and ≥ 40;
  - n = 300: ≤ 8 and ≥ 22.
- No outcome is predicted. The v1 sentence "A NULL is the more likely outcome" is withdrawn (CC-505 C6).

**DESCRIPTIVE rows (no label):**
- k_U: certified over the `syl`-only grid (scorer × P × C, U = `syl`, T = `tw`; the v1 estimand), but not over G_contract.
- k_TU: certified over that `syl`-only grid, but not over G_caption.
- The split of k_T by unit of the breaking class (`syl`, `pyvi`).

### A3: the null level of the per-member test, and why the certificate cannot fail it otherwise (CC-505 B4)

**Why A3 cannot fail through the intersection rule.**
- On any null where some member f has population mean ≤ 0 in direction s, CERTIFIED in direction s implies that member f's test rejected in direction s.
- So P(CERTIFIED) ≤ P(member f rejects) for that member (the intersection–union argument).
- On the swap nulls below, `f0` ∈ F_dev and W is shared, so **r_A3 ≤ r_f0 exactly**.
- The certificate's level can exceed nominal only if a per-member percentile bootstrap exceeds its own nominal level. A3 therefore tests that per-member level, and the rule is put on it.

**Construction.**
- Draw 1,000 comparisons from D without replacement (seed 20261127).
- For each, draw σ ∈ {−1, +1}^558, i.i.d. fair (seed 20261127 + index).
- Set `d'_{i,f} = σ_i · d_{i,f}` for every member f: the exchangeable null.
- Apply M1 over F_dev and the per-member test under `f0`, both with the same W.

**Estimand (per direction, against the one-sided 2.5% per direction of paper §4.4).**
- r_f0⁺ and r_f0⁻: the share of nulls significant under `f0` with `L > 0` (respectively `U < 0`).
- Beside them, r_A3⁺ and r_A3⁻ for the certificate, and the maximum over the 54 members of the per-member rates (DESCRIPTIVE).

**Rule** (on r_f0; one-sided 97.5% Clopper–Pearson per direction, Bonferroni over the two directions):
1. Both upper bounds ≤ 0.040: **AT OR BELOW NOMINAL**. The margin is the same 1.5 points as v1 (0.05 → 0.065), now per direction (0.025 → 0.040). It passes at ≤ 27 of 1,000 per direction.
2. Either lower bound > 0.025: **ABOVE NOMINAL**. This trips at about 36 of 1,000.
3. Otherwise: **INCONCLUSIVE**.

- Second row (DESCRIPTIVE): the same nulls over F (72 members).
- Scope:
  - the global exchangeable null only, not the least-favourable configuration of the intersection–union test;
  - the nulls share W and source files.

## 6. Stages, gates and order

- **Host.** S0, S1 and S2 run on a rented host only (CC-505 ruling 9). The laptop writes files only. Details are in `COMPUTE_B_D1_v2.md`, including the **hard stop at 8 CPU-h**.
- **S0 (host, before any data).**
  - Code read by a judge.
  - Self-tests on stub data:
    - swap identity: re-scoring swapped texts equals the sign flip, to 1e-12;
    - the M1 = M1′ identity;
    - AER algebra on a hand-computed toy;
    - binomial and CP boundaries at the trip points of §5;
    - fold construction;
    - the G_contract/G_caption membership.
  - Mutants to kill:
    - union-of-ties without the mixed-direction convention;
    - σ_c recomputed per resample;
    - margin taken from the wrong member;
    - `rdr` held out;
    - touching counted as significant;
    - `tw` excluded from G_caption;
    - the A3 rule placed on r_A3.
  - `env_check` passes in the pinned segmenter environment.
- **S1 (host).**
  - Re-score D: 54 F_dev and 18 `uts` members, 75 files, per-image CIDEr-D, with `b_fecert.scorer` unchanged.
  - Write `PER_IMAGE_D1.npz`: aggregate scores only, mode 444, never committed, pinned by sha on the LOG.
- **G0 reproduction gate:**
  - (a) For every D comparison and every F_dev class, the statistics recomputed from the matrix with W equal `DEV.json` within 1e-6 on `D`, `L`, `U`, `sd`, with identical class membership.
  - (b) The verdict over F (72 members) recomputed from the matrix equals `RESULT.json::comparisons[i].F`, and `D_f0` equals the stored `D_f0`, on all 1,101.
  - Any difference is a **FAULT**: stop, judge line, no D1 quantity.
- **S2 (host).**
  - H1, H2, H3, A3 and the DESCRIPTIVE rows into `RESULT_D1.json`, once. Then pin.
  - The result note is written by an agent that is neither the coder nor the text writer.
- No stage runs twice without a judge line. Nothing from S2 is opened before its pin line.

## 7. What counts as a registered gain

- H1 SUPPORTED: over the reference-member margin.
- H2 SUPPORTED: over Lu et al.'s ensemble reading.
- H3 SUPPORTED: the Vietnamese tone-placement axis matters beyond a scorer-and-tokenizer grid. This is the only arm aimed at B's remaining novelty.
- No label makes FE-CERT "better than Lu et al." in general: one benchmark, one backbone, the authors' own files.
- A3 is not a value claim. AT OR BELOW NOMINAL supports only the per-member sentence of §8.

## 8. Outcome map (what the paper may say; every p is printed with "nominal")

| outcome | allowed sentence (template) | not allowed |
|---|---|---|
| H1 SUPPORTED | "On the 1,101 development comparisons, FE-CERT certificates broke less often under a unit held out of the family than equally many claims chosen by the margin under the reference member (b_FE vs b_MG; one-sided exact p, nominal; REGISTERED, DEVELOPMENT)." | "FE-CERT is more reliable" without the scope |
| H1 NOT SUPPORTED / NOT_EVALUABLE | "At equal size, FE-CERT and a threshold on the reference member's margin lost similar numbers of conclusions under held-out units (b_FE, b_MG; nominal p). The family showed no advantage over a one-member margin on these comparisons." For NOT_EVALUABLE: "too few discordant breaks (n) to compare." | dropping the row |
| H1 MARGIN BETTER | Printed as such in the abstract and the discussion. | softening |
| H2 any label | The same forms with "the ensemble reading of Lu et al. (2026)", the coverage row and the false-tie **analogue** beside it | comparison with Lu's own coverage or false-tie numbers |
| H3 SUPPORTED | "Adding tone-placement levels to a grid of three scorers, three segmentation units, punctuation and case overturned k_T of its n certificates, more than 5%, the bar of the FE-CERT registration's held-out rule (one-sided 95% Clopper–Pearson lower bound, nominal; REGISTERED, DEVELOPMENT)." | "contract grids are insufficient" in general |
| H3 NULL | "Tone placement overturned at most 5% of the certificates of a scorer-and-tokenizer grid (k_T of n; NULL). Beyond such a grid, the Vietnamese-specific part of the family changed at most 5% of the grid's certificates on these comparisons (one-sided upper bound)." This goes into the abstract and the contributions paragraph, and "axes that come from the written language" is qualified there. | keeping the axes as an unqualified contribution |
| H3 INCONCLUSIVE | counts and bounds only | |
| A3 AT OR BELOW NOMINAL | "On exchangeable sign-flip nulls, the per-member bootstrap was at or below its nominal level in each direction (r_f0⁺, r_f0⁻ with bounds), and the intersection rule cannot raise the certificate's level above it (r_A3⁺, r_A3⁻)." | "the guarantee is exact"; "A3 confirms the certificate" |
| A3 ABOVE NOMINAL | "The per-member percentile bootstrap exceeded its nominal level on exchangeable nulls (r_f0); the certificate inherits that excess." Paper §4.4 is revised. | |
| M1 = M1′ | "FE-CERT's decision rule is Lu et al.'s union-of-ties rule applied to the front-end family, with one convention Lu et al. leave open: when every contract is significant but in different directions, no ordering is claimed. The identity was checked on all 1,101 comparisons." | presenting the rule as new |

- Falsifiers of the value claim: H1 MARGIN BETTER, H2 AER BETTER, H3 NULL.
- Every label is printed whichever way it falls.

## 9. After the result (pre-written path rule; CC-505 B7, pivot rule PI-1026z)

- **If the primary H3 label is not SUPPORTED** (NULL, INCONCLUSIVE or NOT_EVALUABLE):
  - The coordinator opens a Paper B pivot review with the PI, using `PIVOT_REVIEW_B_vi.md`. The options are:
    1. submit B at its current scope with the H3 sentence of §8;
    2. N1 LEXFORM;
    3. a pilot of one of the two extension directions of Objective 3.3, each under its own pre-fixed threshold;
    4. stop B.
  - Recommendation: option 1.
  - **No further Paper B study is registered without the PI.**
- **If it is SUPPORTED:** S2 (new decodes, development data only) may be proposed to a judge.
- The H1, H2 and A3 labels do not change this path. They change only the text of §8.

## 10. Data and scope rules

- Development data only: already-scored stored files on spent KTVIC test references. No decoding, and no look at any unspent split. The carve-out H is not available to B (PI-1101p).
- Labels on D: DEVELOPMENT, plus REGISTERED PREDICTION for H1, H2, H3 and A3.
- FL: not used (§1).
- No caption text is printed. The human-arm, pair and label files are not touched.
- The drafting agent writes nothing to `/mnt/d`. The commit is made by the coordinator after the judge GO.

## 11. Not done, and why

- Lu's (iii) and (iv): see §3 M2.
- Median-of-z and a scorer-grid AER: left out, to keep two primary contrasts.
- The least-favourable null of the intersection–union test: see §5 A3.
- The English control: still NOT RUN, as in FE-CERT.
- `uts` inside the H3 grids: left out, to keep H3 free of the re-score and of the held-out role of `uts` in H1/H2.
