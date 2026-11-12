# C-ATTR-DEV: paper text package v1 (Paper C, ACM TALLIP)

Version v1.1 = v1 (sha256 `7b706265…`, written 2026-11-12T06:46Z, 13:46 VN) + the text fixes of ruling CC-358, applied by script. Not committed before CC-358. For a judge read before any score exists. Label of every row and sentence in this package: `DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY`. AI opinion, not expert-validated.

**Status when written.** No C-ATTR-DEV output has been scored or opened. The text below therefore holds no result: every result number is a named placeholder, and every registered outcome has its sentence written now. The writer read only registrations, rulings, code, LOG lines (through `cut -c1-1300`) and paper text. Nothing under `.session_backup/machines/`, no `.preds.json`, no ledger, no result file and no test set was opened. Two run-status facts in the LOG are used as facts, because they carry no score: the step-1.0 identity counts (OPS-1111ba) and the D1 identity counts (OPS-1112j-c-attr-1b-pause).

**Sources (sha256 prefix).** Registration v1.1 `44f81329`; erratum 1 `f9f0842e`; addendum v1.2 `5858d69d`; block-1 run document v1.1 `e12a1c6b`; block-1b run document v1.1 `196a3279`; scoring run document v1.1 `464eeb0f`; rulings CC-331, CC-332, CC-339 (LOG line only), CC-340, CC-341, CC-346, CC-348; code `scripts/c_attr/c_attr_score.py` `bb2077b9` and `c_attr.py` `6e0de1ae` (read for key names only), `c_attr_job.sh` (output file names), `c_attr_lists.py` (diagnostic key names); paper repo `vsps-paperC-tallip` at `f6aa449`, folder `paper_v1_analysis/` (numbering, notation, table style). The run-repo draft `manuscript/journal_draft_C/` lacks Sections 3.7 and 6.9 of the paper repo, so the paper repo's numbering is used.

**How to read the placeholders.**
- A placeholder is `{{ALIAS::key.path}}`. The aliases name files (paths as on the host; the pulled 0444 copies sit under `.session_backup/machines/ATTR_H1/root/...`):

| alias | file | written by |
|---|---|---|
| `NOM` | `c_attr_score/res/c_attr_nomination.json` | stage `ova` (or `close`) |
| `VER` | `c_attr_score/res/VERDICT.json` | stage `ovb` (`cmd_summary` over the two batch-1 ledgers) |
| `DFS` | `c_attr_score/res/DFSENS.json` | stage `ovb` (§9 row) |
| `SUM` | `c_attr_score/res/SUMMARY.json` | stage `rest` (every ledger) |
| `CB_<set>_<m>` | `c_attr_score/res/COPYBOUND_<set>_<m>.json` | stage `posthoc` |
| `PH` | `c_attr_score/res/POSTHOC.json` | stage `posthoc` |
| `VFY` | `c_attr_score/res/VERIFY.json` | stage `verify` |
| `S10A_<m>_<set>` | `outputs/c_attr/parity/S10a_<m>_<set>.json` | block 1, step 1.0 (a) |
| `S10B_<m>` | `outputs/c_attr/parity/S10b_<m>.json` | block 1, step 1.0 (b) |
| `STEP10_<m>` | `outputs/c_attr/parity/STEP10_<m>.json` | block 1, step 1.0 verdict |
| `D1_<m>` | `outputs/c_attr_b1/parity/D1_<m>.json` | block 1b, D1 (final pull; call 2 rewrote it) |
| `STEP1B0_<m>` | `outputs/c_attr_b1/parity/STEP1B0_<m>.json` | block 1b, D1 verdict |
| `CAP` | `outputs/c_attr_b1/CAP_1B.json` | block 1b, plan after D1 |
| `GS1`, `GS1B` | `outputs/c_attr/gpu_seconds.tsv`, `outputs/c_attr_b1/gpu_seconds.tsv` (sum of non-`start` rows / 3600, the job's `JOB DONE gpu_h` rule) | the jobs |
| `K0` | `scripts/c_attr/block0/K0_REPORT.json` (committed) | block 0 |
| `LOG:<id>` | the decisions LOG line with that id | coordinator |

- `<m>` ∈ {`qwen25vl_7b`, `internvl3_8b`, `aya_vision_8b`}; display names Qwen2.5-VL-7B, InternVL3-8B, Aya-Vision-8B. `<set>` ∈ {`ov_dev_a`, `ov_dev_b`, `xm_dev500`}. `<est>` ∈ {`tau_any`, `tau_sel`, `tau_marg`, `tau_pair`, `placebo_d1_d2`}.
- The scorer's row keys are `<m>|<est>`. Inside this file they are written `<m>~<est>` so that Markdown tables stay intact: `~` stands for `|`.
- Interval macro: `[[A::P]]` renders as `{{A::P.d}} [{{A::P.lo}}, {{A::P.hi}}]`, signed, two decimals, as in Table 13 of the paper. `[[A::P|90]]` adds the 90% interval `{{A::P.lo90}}`, `{{A::P.hi90}}`. The p-like statistic is `{{A::P.p}}`, printed to three significant digits, or as "at its floor (1/2,001)" when equal to 1/2,001.
- There is no PASS/FAIL key. A nominated claim PASSES if and only if `{{VER::sets.ov_dev_b.rows.<m>~<est>.label}}` = `DETECTED` (registration §7.5 item 3). This mapping is written into the text, not chosen later.

**Content.** §1 placement map; §2 method text; §3 batch-size subsection; §4 result shells with the fixed sentence for every registered outcome; §5 disclosure and limitation text; §6 claim→evidence table, manifest rows and the list open for the judge.

---

## 1. Where each piece goes

The paper repo's numbering at `f6aa449` is used. New tables continue after Table 14 (main) and Table S19 (supplement). Nothing in this package changes a registered number, verdict, threshold or sentence of the existing paper; the only edits to existing text are the corrections owed under CC-340 W6 (same-slice parity, not batch invariance).

| # | piece (this file) | place in the paper | relation to existing text |
|---|---|---|---|
| P1 | §2.1 "3.8 Arms and estimands of the attribution study" | Section 3, new subsection 3.8 | follows 3.7; 3.1–3.7 unchanged. The opening paragraph of Section 3 gets one clause: "… and Section 3.8 the arms of a later development study that splits the retrieval gain." |
| P2 | §2.2 glossary rows | Section 5, Box 1 | appended after the row "detected"; no existing row changes |
| P3 | §2.3 "5.7 The attribution registration (development)" | Section 5, new subsection 5.7 | follows 5.6; 5.6 gets one closing sentence pointing to 5.7 (text in §2.3) |
| P4 | §3 "6.10.2 Batch composition changed greedy captions (kill gate K1)" | Section 6, inside new 6.10 | new |
| P5 | §4 "6.10 Attribution of the retrieval gain on development data" (6.10.1, 6.10.3–6.10.8), Tables 15–17 | Section 6, new subsection 6.10 | inserted after 6.9; "6.10 Compute" becomes **6.11 Compute**, with one added sentence (§4.10) |
| P6 | §4 supplement tables S20–S26 | supplement, new section "Attribution study (C-ATTR-DEV): every row" | placed after "Flickr30K registration: development rows (Section 8.6)" |
| P7 | §5.1 "7.5 The attribution study" and Box 2 rows | Section 7: new 7.5 after 7.4; four new rows at the end of Box 2 | Box 2 row 1 is corrected (§5.4) |
| P8 | §5.2 limitation bullets and threat sentences | Section 9.1 (two new bullets after "One test look, one machine, one run, one random draw"), 9.2 (one sentence in Internal validity, one in Construct validity), 9.3 (one sentence) | the bullet "One test look …" loses its last sentence and gains the corrected one (§5.4) |
| P9 | §5.4 corrections owed under CC-340 W6 | Box 2 row 1; Section 9.1 bullet "One test look …"; supplement "Test-run operations → Decode-parity check before the Vietnamese test" (closing paragraph); supplement line "Decode parity on 52 OV-dev-B images" in the development-ablation record | replaces the words "found no run-to-run variation" where they imply batch invariance; no number changes |
| P10 | §6.2 manifest rows | `number_manifest_C.tsv` | appended rows, status `PENDING_SCORE` until the stages run |
| — | abstract, introduction, contributions, conclusion | not touched by this package | whether any development row may enter them is open for the judge (§6.4, item J1) |

---

## 2. Method text (paper-ready)

### 2.1 Section 3.8: Arms and estimands of the attribution study

> **3.8 Arms and estimands of the attribution study (development data only)**
>
> The registered contrast `ret` − `rand` (Section 3.2) shows whether retrieved examples beat random examples from the same memory. It does not show why. A retrieved list differs from a random list in two ways at once: it is a list that suits *this* image, and it is a list of the kind that retrieval produces for *any* image (captions of near-typical scenes, of similar length and wording). A later development study, registered separately (Section 5.7) and labelled "development, non-confirmatory", splits the contrast into these two parts with one added arm, and bounds how much of the retrieval gain can travel through n-grams copied from the shown captions. It uses development sets only and changes no registered result of this paper.
>
> **The permuted arm.** In `perm`, image q is shown the retrieved list of another image of the same set. The images of a set, in manifest order, are permuted by a cyclic permutation π_p without a fixed point, built by Sattolo's algorithm [@Sattolo1986] from a generator seeded by the set name and the permutation index p, so that π_p depends on neither the images' content nor any output. Image q takes the eligible ranking of its donor q′ = π_p(q) (cosine to q′, descending; ties by cluster id; cosine to q′ below the near cut 0.92) and keeps the first k clusters whose cosine to q is also below 0.92; when q's own near cut removes one of the donor's first eight, the list is refilled from further down the donor's ranking. Order rule, prompt tail and k are those of the backbone's `ret` arm. Two permutations are used (p = 1, 2). If more than 10% of the eight slots of a set needed a refill, `perm` on that set would be a diagnostic with no rule; the refill share was computed before any decode (Table S26).
>
> **Arms used.** `zs`, `ret` and `rand` are those of Section 3.2. `rand` is drawn R times per image, with draw d seeded by the set name, the image id and d; `perm` is built D = 2 times. R = 3 on OV-dev-B and XM-dev500 and R = 1 on OV-dev-A; D = 2 on every set. `fix` sets f1–f4 (Section 3.2, one set of k clusters per set, drawn among clusters below the near cut for every image) were added on OV-dev-B and XM-dev500 for Qwen2.5-VL-7B. All arms of a backbone share one prompt template, one k, one order rule and one decoder, and differ only in the example block; the code checks that the prompt hashes of two arms differ only through that block.
>
> **Backbones.** Qwen2.5-VL-7B and InternVL3-8B at the configurations of Table 2, and Aya-Vision-8B at the configuration of Section 3.7. InternVL3-8B runs **without the deletion step** (τ = −∞, no verifier) in every arm of this study, because the step's fall-back to the zero-shot caption would make `perm` a mixture of two arms; its registered τ = 0.10 rows are untouched. Qwen2.5-VL-7B and InternVL3-8B share the Qwen2.5 language-model line; Aya-Vision-8B's language model is Command R7B.
>
> **Estimands.** For one backbone at its configuration, one set and image i, let s_i(a) be the stripped CIDEr-D (Section 3.6) of arm a; for `rand` and `perm`, s_i is the mean over that image's R draws or D permutations. Then
> - τ_any = mean_i [s_i(`rand`) − s_i(`zs`)], the gain from seeing any in-domain captions;
> - τ_sel = mean_i [s_i(`ret`) − s_i(`rand`)], the registered retrieval contrast of Section 5.2, per backbone;
> - τ_marg = mean_i [s_i(`perm`) − s_i(`rand`)], the part that any retrieved-type list gives, whichever image it was retrieved for;
> - τ_pair = mean_i [s_i(`ret`) − s_i(`perm`)], the part that needs the list retrieved for this image.
>
> Per image, `ret` − `zs` = τ_any + τ_marg + τ_pair, and τ_sel = τ_marg + τ_pair exactly. No estimand is pooled over backbones. In this section and in Section 6.10, τ with a subscript is an estimand; τ alone remains the deletion threshold of Section 3.4.
>
> **A bound on copying.** For a caption y and a list S of shown captions, masked_n(y, S) removes from y every token that lies in an n-gram also present in a caption of S. The loss is loss(y; S) = s(y) − s(masked_n(y, S)), with the same references and document frequencies; the references are never masked. Tokens are counted in two units: (i) syllables, the space-separated units of the lower-cased caption, and (ii) words after RDRSegmenter segmentation, the masked text then being scored as segmented. n = 3 decides; n = 2 and n = 4 are sensitivity rows. For image q, with R_q the k captions shown to q in `ret`,
>
> κ_q = loss(y_ret,q; R_q) − loss(y_zs,q; R_q).
>
> The zero-shot caption was written without R_q, so its loss against R_q measures overlap that needs no copying (a placebo). K_ret = mean_q κ_q is an upper bound on the copy-carried part of `ret` − `zs`, and L_cp = mean_q [(s_q(`ret`) − s_q(`rand`)) − κ_q] a lower bound on the part of the retrieval contrast that does not travel through copied n-grams. Both rest on assumption A_cp: without copying, masking with R_q would cost the `ret` and `zs` captions the same score. A_cp can fail in one direction only: a better `ret` caption shares more correct words with captions of similar images, so K_ret can only overstate copying; L_cp also assumes that copying does not lower the `rand` score. The direction of A_cp is checked by K_nc = mean_q [loss(y_rand,q; R_q) − loss(y_zs,q; R_q)]: the `rand` caption never saw R_q either. If K_nc is REVERSED on a set (Section 5.7), the stated direction is contradicted and the bound is withdrawn for that set. Two further checks are made: κ of a `zs` run against itself is zero by construction (a self-test of the scorer), and K_ret is checked for an increase from n = 2 to n = 4; if it increases, the bound carries the flag "monotonicity check failed". Three companions are descriptive: K_rand (the `rand` d0 caption against its own shown list, with the same placebo), K_ret − K_nc (printed, never called a bound), and the loss of the stored image-blind caption (written from the examples alone) against R_q. K_nc and K_rand use draw d0. κ_q is unrelated to the agreement coefficient κ of Section 6.9.
>
> The copy bound is computed on CPU from the **stored** `zs`, `ret` and `rand` d0 decodes of the earlier registrations (Section 5.1), so its L_cp is a bound on the stored, batched `ret` − `rand` d0 contrast, not a split of the batch-size-1 τ_sel of Section 6.10.3 (Section 6.10.2 explains the two decoding policies). For Aya-Vision-8B on XM-dev500 no stored decode exists, and its row uses the block-1 batched decodes (Section 6.10.2).
>
> **Not used.** The registration also names a memory swap on fixed English images, re-implemented third-party arms with random and permuted examples (a re-implementation of the LMCap recipe by this study; not the authors' code (no licence); not a statement about the published numbers [@Ramos2023LMCap]; and an image-caption-pair prompt format, as used by RAGCap; not RAGCap [@Bazi2025RAGCap]) and further backbones outside the Qwen language-model line. Section 6.10.8 states which of them ran.

### 2.2 Box 1, rows appended (Section 5)

| term | meaning |
|---|---|
| `perm` | the retrieved list of another image of the same set, under a fixed cyclic permutation, filtered by the query's own near cut (Section 3.8) |
| τ_any, τ_sel, τ_marg, τ_pair | development estimands of the attribution study: `rand` − `zs`, `ret` − `rand`, `perm` − `rand`, `ret` − `perm` (Section 3.8); τ alone is still the deletion threshold |
| DETECTED, REVERSED, NEGLIGIBLE, UNRESOLVED | the four labels of the attribution study (Section 5.7). DETECTED in capitals is a registered rule (point ≥ +2.0 and a Holm-stepped p-like statistic); it is not the lowercase "detected" above |
| split of a known τ_sel | wording attached to every τ_pair and τ_marg row on OV-dev-A and OV-dev-B, where τ_sel was already known (Section 5.7) |
| A1, K1, D1 | the attribution study's batch-independence assumption, the kill gate that tested it, and the batch-size-1 determinism check that replaced it (Section 6.10.2) |
| K_ret, L_cp, K_nc, κ_q | the copy bound and its direction check (Section 3.8); κ_q is not the agreement κ of Section 6.9 |
| C-ATTR-DEV | the attribution study's registration; every row carries "development, non-confirmatory" |

### 2.3 Section 5.7: The attribution registration (development)

Closing sentence appended to Section 5.6:

> A further registration, written after every test set of this paper had been decided, splits the retrieval contrast on development data only (Section 5.7); it amends no earlier registration.

New subsection:

> **5.7 The attribution registration (development)**
>
> > **Development data only: DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY.** No test set was staged, decoded, scored or opened. No reported test row, interval or label changes because of a number of this study. Nothing here enters a verdict of Sections 6.2–6.9 or 8.
>
> **Files and order.** The registration (C-ATTR-DEV, version 1.1) was committed before any of its outputs existed, with an erratum written before the first decode. After kill gate K1 fired (Section 6.10.2) and before any output was scored, an addendum (version 1.2) changed the batch size and the batch-independence check, with what follows from them (every contrast arm decoded anew, a new compute cap, row labels for the two decoding policies, and a scoring order that puts batched outputs last); no set, list, arm, draw, seed, k, prompt, memory, model snapshot, SESOI, α, label rule or family rule changed. Each file, each code version and each run document was reviewed and committed before the step it governs. The registered scoring order is enforced by the code (Section 5.7, "Order of looks").
>
> **Sets.** OV-dev-A (911 images) nominates; OV-dev-B (925) carries the one registered look; XM-dev500 (500) gives reported rows with no rule. KTVIC dev299 would serve only to configure new backbones. The sets, lists and stored decodes are those of the earlier stages (Sections 4 and 5.1); every image of a set is decoded.
>
> **What a first look means here.** On OV-dev-A and OV-dev-B the sum τ_sel = τ_marg + τ_pair was already known for Qwen2.5-VL-7B and InternVL3-8B from the development stages (Tables S10–S11, S16 and S17), and on OV-dev-B also for Aya-Vision-8B, from the exploration runs of the Flickr30K registration (its stored, batched value appears only in Table S22). Because the identity holds per image, τ_pair and τ_marg on these sets are a first look at how a known sum splits, not at the size of the retrieval effect. OV-dev-B has also carried the stage-B rule, the ablations of Section 6.8 and earlier masked rows; XM-dev500 carried the stage-B rows, including the near-verbatim copy share, and the units of an earlier diagnostic study of the group. Every row and sentence about τ_pair or τ_marg on OV-dev-A or OV-dev-B therefore carries the words "split of a known τ_sel", and a pass on OV-dev-B is reported as "the nominated split held on a re-used development set, at batch size 1", never as new evidence that retrieval helps. At batch size 1, τ_sel on OV-dev-A and OV-dev-B carries "batch-1 re-decode of a known τ_sel" and stays outside every family.
>
> **Interval and p-like statistic.** Every interval is a paired image bootstrap of the per-image differences, with B = 2,000 resamples drawn as `numpy.random.default_rng(0).integers(0, n, (B, n))`, one index matrix per set shared by every interval on that set, and percentile bounds (as in Section 5.4). Each image's random draws are seeded by its own id and are independent across images, so the variance of the draw-averaged difference d̄_i is [Var(m_I) + E σ²_I / R] / n, with m_i the image's expected difference and σ²_i its between-draw variance (law of total variance). The image bootstrap of d̄_i estimates exactly this quantity, so the interval includes the variance of the random draw at any R ≥ 1 (Proposition 3a of the registration); the same holds for `perm` over D. A shared `fix` set is different (Section 6.10.5). The one-sided p-like statistic is p̃ = (1 + #{b : bootstrap mean_b ≤ 0}) / (B + 1), the registered form of Section 8.6; its floor is 1/2,001, and it is not an exact p-value.
>
> **Labels.** With SESOI = +2.0 stripped CIDEr-D points (Section 5.2), each contrast with point θ̂ gets exactly one label, first match:
> - **DETECTED:** θ̂ ≥ +2.0 and p̃ ≤ α_j, where α_j is the Holm step-down threshold [@Holm1979] at family-wise one-sided α = 0.025 over the m claims of the row's family: the claims are taken in order of p̃ (ties by claim name), the j-th is compared with 0.025 / (m − j + 1), and the step-down stops at the first claim that fails either condition; no later claim is DETECTED. A row outside every family has m = 1, so its rule is θ̂ ≥ +2.0 and p̃ ≤ 0.025. That rule agrees with "95% percentile lower bound > 0" except when exactly 50 of the 2,000 bootstrap means are ≤ 0, where the lower bound can exceed 0 while p̃ = 51/2,001 > 0.025; the p̃ rule decides.
> - **REVERSED:** the 95% upper bound is below 0.
> - **NEGLIGIBLE:** the 90% interval lies inside (−2.0, +2.0), a two one-sided test at 0.05 per side [@Schuirmann1987].
> - **UNRESOLVED:** none of the above.
>
> For m = 1 this matches the form of the registered P1 rule (a point at the SESOI and a one-sided 0.025 bound), except that P1 requires a point above +2.0 and DETECTED a point of at least +2.0; at any m it is stricter than the Holm-adjusted one-sided 0.05 of the Flickr30K registration.
>
> **Nomination, then one look.**
> 1. *Nomination (OV-dev-A).* For Qwen2.5-VL-7B and InternVL3-8B, each alone, τ_pair and τ_marg are computed with R = 1 and D = 2. Claim H_pair(m) is nominated if the 95% lower bound of τ_pair is at least +2.0, and H_marg(m) if that of τ_marg is. This is the nomination rule of the Flickr30K registration (Section 8.6).
> 2. The nomination file lists the nominated claims; its sha256 was written to the decisions log before any new OV-dev-B output was scored.
> 3. *One look (OV-dev-B).* Each nominated claim PASSES if its contrast on OV-dev-B is DETECTED, with the nominated claims as the Holm family.
> 4. The nominated claims of Qwen2.5-VL-7B, the backbone that carries the registered P1 result, are reported first. This order has no separate α; the Holm family decides.
> 5. If nothing is nominated, there is no registered claim, and the OV-dev-B rows are reported with their labels and the sentence "no claim was nominated on OV-dev-A".
> 6. Components that were not nominated, and Aya-Vision-8B's τ_pair and τ_marg (it has no OV-dev-A decodes), are descriptive rows with labels.
>
> **Multiplicity.** One registered family: the nominated claims. One secondary family: τ_sel of each backbone first decoded under this registration outside the Qwen line (S-BB; Section 6.10.8). Everything else is reported with an unadjusted interval and a label, with no family-wise statement. No post hoc statistic replaces a failed rule; a post hoc row may stand beside it, labelled post hoc.
>
> **Failure wording, fixed in the registration.** A nominated claim that is not DETECTED on OV-dev-B is reported in the main text as "FAIL: the claim nominated on OV-dev-A did not hold on OV-dev-B", with its interval. Nothing nominated gives the sentence of item 5. Under either outcome the study keeps τ_any, τ_sel, the variance terms and the copy bound, and makes no registered claim about the split.
>
> **XM-dev500.** Rows are reported per backbone with interval and label and carry no rule: at n = 500 the known half-width of Qwen2.5-VL-7B's τ_sel interval is about ±3.4 (Table S16), so neither DETECTED at +2.0 nor NEGLIGIBLE can be decided reliably.
>
> **Variance.** (a) For each backbone and set with R ≥ 2: the mean within-image variance over draws, σ̂²_w; its share of the image-bootstrap variance, σ̂²_w / (nR) against s²(d̄_i) / n; and a placebo, `rand` d1 − `rand` d2, with its interval. A placebo row is flagged when |θ̂| ≥ 2.0 and its 95% interval excludes 0; a flag is not a stop, and a flagged set goes to review before its rows are used. On OV-dev-B these rows are post hoc for the three stored backbones (earlier development runs had already computed between-draw spreads there); on XM-dev500 they are descriptive. (b) For one shared `fix` set (Qwen2.5-VL-7B, y_iF = s_i(`ret`) − s_i(`fix`_F), F = 0 … 4), a two-way layout with one value per cell gives MS_F, MS_I and MS_E; V̂_b = max(0, (MS_F − MS_E)/n) is the between-set variance and V̄_img the mean over F of s²_i(y_iF)/n, the variance a single-set image bootstrap sees; ω̂ = V̂_b / V̄_img, with the approximate 95% upper bound ω^U from the lower 5% quantile of F(R_F − 1, (R_F − 1)(n − 1)). The registered label rule is: ω^U ≤ 0.25 gives "the fixed-set rows are practically unconditional"; otherwise every `fix` row of the paper carries "conditional on the realised fixed set", with ω̂ and ω^U printed. With five sets, ω^U is about 4.6 times the interaction share even when V_b = 0 (a property of the bound, stated in the registration). The five-set row is ȳ_·· with standard error √[(MS_F + MS_I − MS_E)/(n R_F)] and a t interval with R_F − 1 = 4 degrees of freedom. No test interval is widened, recomputed or relabelled with a number from this analysis.
>
> **Copy bound: tiers and reading.** On OV-dev-B the bound is **post hoc**: it was specified after naive masked rows on that set had been seen, and is computed once on stored outputs. On XM-dev500 it is a first look at κ, although the stage-B near-verbatim copy share on that set had been seen. The reading sentences were fixed in the registration: L_cp DETECTED gives "a retrieval-specific effect of at least +2.0 remains under the most pessimistic copy attribution"; an L_cp point ≤ 0 gives "the bound does not exclude that the whole retrieval-specific effect is carried by copied n-grams; this agrees with, and does not prove, the published short-cut account" [@Li2025UnveilingICL]; any other outcome gives "partly bounded".
>
> **Memory source (English only).** The registered Vietnamese memory cannot be swapped for an out-of-source one: it holds 6,017 clusters with OpenViIC images only, 2,133 with both, and 40 with KTVIC images only. The memory swap is therefore registered on English data, on the 1,014 Flickr30K val images, for Qwen2.5-VL-7B and Aya-Vision-8B. M_T is the same-source Flickr30K-train memory (28,000 images, each its own cluster, first reference shown); M_O is an other-source memory of 28,000 clusters drawn from the COCO memory by a seeded sample (subsample j = 0; a second subsample j = 1 for Qwen2.5-VL-7B only), so the two memories have the same size. In each cell `ret` and `rand` d0 are decoded at the frozen configuration with the near cut, and
>
> δ = mean_i {[s_i(`ret`; M_T) − s_i(`rand`; M_T)] − [s_i(`ret`; M_O) − s_i(`rand`; M_O)]},
>
> with the interval and label above and the two τ_sel printed beside it. Caption length is not matched across memories: `rand` in each cell carries that memory's length and style, and δ differences it out. Rule L applies per cell: if |len_ret − len_rand| / len_rand exceeds 0.10, the cell is marked "not separated from length". M_O is one shared subsample, so its interval is conditional on it; the j = 1 row shows the spread and supports no variance estimate. Reading, fixed in the registration: δ DETECTED gives "on fixed images the retrieval-specific effect is larger with a same-source memory"; δ NEGLIGIBLE gives "the source of the memory did not change the retrieval-specific effect on these images"; REVERSED or UNRESOLVED are reported as such; no claim about XM3600 or NoCaps follows from any outcome. A post hoc companion uses the stored cells of the 1,000-image Flickr30K train carve, where the other-source memory is the full COCO memory (111,927 clusters) against the 28,000-image Flickr30K-train memory, with `rand` d0; it is labelled "post hoc; size-confounded", and no reading sentence is applied to it.
>
> **Document-frequency sensitivity.** CIDEr-D document frequencies come from the references only (Section 3.6), so one image's score does not depend on another image's caption. As a check of that choice, the OV-dev-B contrasts τ_pair and τ_marg of Qwen2.5-VL-7B (each flagged nominated or not) are recomputed in rows 1–200 of OV-dev-B's shared index matrix, with document frequencies recomputed over the references of the resampled images (an image drawn twice counts twice; ref_len = log 925). The 95% percentile interval of the 200 resample means is printed beside the fixed-document-frequency interval over the same 200 rows. The row is descriptive and has no rule.
>
> **Scoring parity.** Before any new run was scored, the scorer had to reproduce the stored per-image stripped CIDEr-D of the six stage-B OV-dev-B runs within 1e-4, and the document-frequency row must reproduce its own ledger within 1e-4.
>
> **Order of looks.** The scoring ran in stages on a rented machine, CPU only, from read-only copies whose hashes had been logged: (1) a verification stage (copies against their logged checksums, stored decodes against their pins, the scoring environment, the prompt-hash comparison of every batch-size-1 run with the batched or stored run of the same cell, which opened the batch-size-1 OV-dev-B run files before the nomination file existed but computed and printed only counts of per-image prompt-hash matches, no caption and no score; and the scoring parity gate); (2) batch-size-1 OV-dev-A and the nomination file, its sha256 logged; (3) batch-size-1 OV-dev-B, the verdict file and the document-frequency row, their sha256 logged; (4) batch-size-1 XM-dev500 and then every batched output, in their own section; (5) the post hoc rows (copy bound and the swap companion). Each stage required the logged sha256 of the previous stage's file and ran once. The scorer refused every OV-dev-B run before the nomination file existed and every batched run before the OV-dev-B verdict.
>
> **Budget.** Block 1 had a hard cap of 12 GPU-hours. Block 1b had a hard cap of min(40, 1.5 P) GPU-hours, with P the projection from the batch-size-1 rates measured in D1, logged before its first registered step; its steps ran in a fixed order (Tier A: Qwen2.5-VL-7B, then InternVL3-8B, on OV-dev-A and OV-dev-B; Tier B: Aya-Vision-8B on OV-dev-B and `zs` on OV-dev-B for all three; Tier C: XM-dev500 for all three), so a cap stop would have dropped Tier C first, then Tier B. Tier A was never to run in part. A freeze at 2026-11-16 12:00 (UTC+7) ended every unfinished step.

---

## 3. Section 6.10.2: Batch composition changed greedy captions (kill gate K1)

Placed inside Section 6.10, after 6.10.1. Every number here is a count of identical caption strings; no score was computed for this subsection.

> **6.10.2 Batch composition changed greedy captions (kill gate K1)**
>
> **What was registered.** The attribution registration assumed that one image's caption does not depend on the other images decoded in the same batch (assumption A1). Before any attribution arm was used, each backbone re-decoded the first 50 OV-dev-B items of its stored `ret` run twice on the new machine: (a) in the stored order and batch slices, compared with the stored captions (host parity; also on the first 50 OV-dev-A items for Qwen2.5-VL-7B and InternVL3-8B); and (b) in reversed order at batch size 1, compared with the same machine's decode (a). Each comparison prints only the number of identical strings and the ids of the others. A pass needs all 50. A failure of (b) was kill gate K1: the backbone leaves the registered families, and its rows are printed "A1 not met".
>
> **What happened.** Host parity held for every backbone and set checked (Table S20). Check (b) failed for all three backbones: {{S10B_qwen25vl_7b::identical}}/{{S10B_qwen25vl_7b::n}} captions were identical for Qwen2.5-VL-7B, {{S10B_internvl3_8b::identical}}/{{S10B_internvl3_8b::n}} for InternVL3-8B and {{S10B_aya_vision_8b::identical}}/{{S10B_aya_vision_8b::n}} for Aya-Vision-8B. The registered report sentence applies: "K1 fired: no backbone met A1 under registration v1.1; block 1 as registered carries no claim." No nomination rule was computed on the batched decodes; a nomination file with zero claims and the reason K1 was written, and its sha256 logged, before any score existed.
>
> **What it means.** The decoder is greedy (one beam, no sampling), runs in bf16 with each model's own processor, and pads every batch on the left to the length of its longest prompt. Check (a) shows that a decode is reproducible given its batch: the same images in the same slices on the new machine gave the stored strings. Check (b) shows that it is not invariant to the batch: for these three models, {{S10B_qwen25vl_7b::failing_ids|count}}, {{S10B_internvl3_8b::failing_ids|count}} and {{S10B_aya_vision_8b::failing_ids|count}} of 50 greedy captions changed (Qwen2.5-VL-7B, InternVL3-8B, Aya-Vision-8B) when the same images were decoded one at a time. The determinism check D1 below decoded the same 50 items at batch size 1 in the stored order and found every string equal to the reversed batch-size-1 decode, so at batch size 1 the order of the items changed none of these captions; the differences in (b) go with the change of batch composition, not with the change of order. A reading of the decoder code, made after K1 fired and not tested here, is that batch-mates change the padding and the shape of the numerical work, and that small numerical differences can flip a greedy choice. In this study the arms differ by their example blocks, so their prompts have different lengths and different padding; a per-image difference between two arms decoded in batches can therefore contain a batch-mate term that differs by arm. Fixed batch slices do not remove it, and an image bootstrap does not see the coupling of images within a slice.
>
> **What it does not show.** No score was compared: K1 rests on string identity only. The check says nothing about the quality of either caption, about the sign or size of any score difference, or about whether batched or one-at-a-time decoding gives better captions; it does not show that any batched result of this paper is biased. It does not identify the numerical cause. It covers these three models, this software stack and 50 OV-dev-B items each.
>
> **Consequences for this paper.** Every registered contrast of this paper between two text-example arms of one backbone (stages A and B, the Vietnamese and English tests, the Flickr30K registration) was decoded in fixed batches, with the same batch policy for both arms. The LMCap re-implementation and the interleaved image-caption arm were decoded one query at a time, so their contrasts with a backbone's `ret` (Tables 13, 14 and S19) set a decode at batch size 1 beside a batched one. All these rows are results of the systems as run; none of their numbers changes, and none is relabelled. The decode-parity checks reported earlier as 52/52 identical captions re-decoded the same items in the same slices on the same stack: they show run-to-run parity, not batch invariance (Section 9.1 and Box 2 are corrected accordingly).
>
> **Consequences for the attribution study.** After K1 fired, and before any of its outputs was scored or opened, an addendum to the registration (version 1.2) changed the batch size and the A1 check, with what follows from them (Section 5.7). Every arm that enters an attribution contrast was decoded anew at batch size 1, with the same prompts (per-image prompt hashes compared with the batched or stored run of the same cell), the same model snapshots and the same environment; all arms of one backbone and set came from one machine. A1 holds by construction at batch size 1 once the decode is deterministic, so the addendum replaced A1 by a determinism check, D1: the first 50 OV-dev-B `ret` items decoded at batch size 1 in the stored order must equal, as strings, the reversed batch-size-1 decode of check (b). D1 passed for all three backbones ({{D1_qwen25vl_7b::identical}}/{{D1_qwen25vl_7b::n}}, {{D1_internvl3_8b::identical}}/{{D1_internvl3_8b::n}}, {{D1_aya_vision_8b::identical}}/{{D1_aya_vision_8b::n}}). Every attribution row in Tables 15 and 16 and in Tables S21 and S23(a) comes from batch-size-1 decoding and carries the registered label "batch size 1; registered in v1.2 after K1 fired, on string-identity counts only". The batched block-1 rows are printed only as descriptive rows, each labelled "A1 not met; batched decode; descriptive": the sensitivity row of Table S22, the fixed-set rows of Table S23(b) and Aya-Vision-8B's XM-dev500 row of Table 17. On the post hoc reading above, their contrast between `ret` and `perm` is best read as the effect of switching a whole fixed-slice decoding policy rather than as a per-image effect; this reading was not tested.

Notes for the transfer (not paper text):
- `{{S10B_<m>::failing_ids|count}}` = the length of the `failing_ids` list, which the comparator writes (`c_attr.py` `cmd_compare`); it equals `n − identical`. Values of record in the LOG (OPS-1111ba): 8, 13 and 19 changed captions. The manifest rows of §6.2 key them to the comparator files.
- The batch size of each stored batched run comes from its model specification (`c_attr.model_spec(<m>)["batch_size"]`, recorded in each run's `spec.batch_size`). The block-1 run document records that Qwen2.5-VL-7B's stored slices hold 4 images; the others are not stated in any file read for this package, so the paper text above states no batch size. Add the sizes only with a manifest row.

---

## 4. Result shells (Section 6.10 and supplement)

Rules for every shell below:
- Each row prints its tier label in the table caption or a column: `DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY` (caption), the batch label (`{{…batch}}`), and the note (`{{…note}}`: "split of a known τ_sel" or "batch-1 re-decode of a known τ_sel") where the scorer wrote one.
- A row whose key is absent from its file is printed "NOT RUN" with the reason from §4.9; it is never filled from another file.
- Labels are copied from the `label` key. No sentence re-derives a label.

### 4.1 Section 6.10 opening and 6.10.1 (what ran)

> **6.10 Attribution of the retrieval gain on development data**
>
> > **Development data only (OV-dev-A, OV-dev-B, XM-dev500): DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY.** This study was registered after every test set of this paper had been decided. It changes no verdict of Sections 6.2–6.9 or 8 and enters neither the abstract nor the contributions. OV-dev-A and OV-dev-B are re-used development sets on which the retrieval contrast τ_sel was already known (Section 5.7).
>
> **6.10.1 What ran.** Block 1 decoded the `perm`, `fix` and extra `rand` arms, and Aya-Vision-8B's `zs`, `ret` and `rand` d0 on XM-dev500, in batches, as registered; it ended with all its registered steps complete, in {{GS1::gpu_h}} GPU-hours of its 12-hour cap, and carries no registered claim (Section 6.10.2). Block 1b re-decoded every arm that enters an attribution contrast at batch size 1 under the hard cap of {{CAP::cap_h}} GPU-hours fixed after D1, and used {{GS1B::gpu_h}} GPU-hours. All {{SUM::n_b1_runs}} registered batch-size-1 runs (Tiers A, B and C) finished, with no cap stop and no job stop. Scoring followed the registered order (Section 5.7); its verification stage passed, with the per-image prompt hashes of {{VFY::prompts.b1_runs}} batch-size-1 runs compared in {{VFY::prompts.pairs}} pairs and {{VFY::prompts.unequal|count}} unequal pairs, and the scoring parity gate passed ({{VFY::parity_7_1.result}}).

Transfer notes: `SUM::n_b1_runs` is not a scorer key. LOG OPS-1112af records 55 OK lines (the 50 planned runs of OPS-1112j, 3 D1 and 2 other lines), no CAP STOP and no JOB STOP (its words "10 on OV-dev-A" are loose: each Tier-A backbone ran 4 OV-dev-A and 6 OV-dev-B runs); the count and the step names are confirmed from `c_attr_b1/logs/job.log` (`OK` / `CAP STOP` / `JOB STOP` lines) and `STEPS_1B.tsv` at the pull; the manifest row names that source. If the verification stage did not pass, no row of §4.2–4.8 exists, and §4.9 item V applies.

### 4.2 Section 6.10.3: the registered claim (nomination, then one look)

**Table 15. Nomination on OV-dev-A (911 images) at batch size 1. DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY. Stripped CIDEr-D points, paired 95% bootstrap CIs, B = 2,000; R = 1, D = 2. Rule: a claim is nominated if its 95% lower bound is at least +2.0. Every row: "batch size 1; registered in v1.2 after K1 fired, on string-identity counts only".**

| backbone | estimand | difference [95% CI] | note | nominated? |
|---|---|---|---|---|
| Qwen2.5-VL-7B | τ_pair | [[NOM::rows.qwen25vl_7b~tau_pair]] | split of a known τ_sel | yes if `H_pair(qwen25vl_7b)` ∈ `{{NOM::nominated}}`, else no |
| Qwen2.5-VL-7B | τ_marg | [[NOM::rows.qwen25vl_7b~tau_marg]] | split of a known τ_sel | yes if `H_marg(qwen25vl_7b)` ∈ `{{NOM::nominated}}`, else no |
| Qwen2.5-VL-7B | τ_sel | [[NOM::rows.qwen25vl_7b~tau_sel]] | batch-1 re-decode of a known τ_sel | not a candidate |
| InternVL3-8B (τ = −∞) | τ_pair | [[NOM::rows.internvl3_8b~tau_pair]] | split of a known τ_sel | yes if `H_pair(internvl3_8b)` ∈ `{{NOM::nominated}}`, else no |
| InternVL3-8B (τ = −∞) | τ_marg | [[NOM::rows.internvl3_8b~tau_marg]] | split of a known τ_sel | yes if `H_marg(internvl3_8b)` ∈ `{{NOM::nominated}}`, else no |
| InternVL3-8B (τ = −∞) | τ_sel | [[NOM::rows.internvl3_8b~tau_sel]] | batch-1 re-decode of a known τ_sel | not a candidate |

Transfer note: the nomination file's rows hold the labels the scorer applied with m = 1 (`NOM::rows.<m>~<est>.label`). Table 15 does not print them: on OV-dev-A the rule is the nomination rule, and printing a DETECTED label there would read as a second rule. The τ_sel rows come from the nomination file's `rows`; if the judge prefers, they can be taken from `VER::sets.ov_dev_a.rows.<m>~tau_sel` instead (same ledger), and the note "batch-1 re-decode of a known τ_sel" is then the scorer's own `note`.

**Table 16. The one look at OV-dev-B (925 images) at batch size 1. DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY. Stripped CIDEr-D points, paired 95% bootstrap CIs, B = 2,000, one index matrix; R = 3 `rand` draws and D = 2 permutations averaged per image. p̃: one-sided p-like statistic (floor 1/2,001). m: size of the row's Holm family (1 outside every family). Every row: "batch size 1; registered in v1.2 after K1 fired, on string-identity counts only".**

| backbone | estimand | difference [95% CI] | p̃ | family, m | label | note |
|---|---|---|---|---|---|---|
| Qwen2.5-VL-7B | τ_pair | [[VER::sets.ov_dev_b.rows.qwen25vl_7b~tau_pair]] | {{…~tau_pair.p}} | {{…~tau_pair.family}}, {{…~tau_pair.m}} | {{…~tau_pair.label}} | split of a known τ_sel |
| Qwen2.5-VL-7B | τ_marg | [[VER::sets.ov_dev_b.rows.qwen25vl_7b~tau_marg]] | {{…p}} | {{…family}}, {{…m}} | {{…label}} | split of a known τ_sel |
| Qwen2.5-VL-7B | τ_sel | [[VER::sets.ov_dev_b.rows.qwen25vl_7b~tau_sel]] | {{…p}} | none, 1 | {{…label}} | batch-1 re-decode of a known τ_sel |
| InternVL3-8B (τ = −∞) | τ_pair | [[VER::sets.ov_dev_b.rows.internvl3_8b~tau_pair]] | {{…p}} | {{…family}}, {{…m}} | {{…label}} | split of a known τ_sel |
| InternVL3-8B (τ = −∞) | τ_marg | [[VER::sets.ov_dev_b.rows.internvl3_8b~tau_marg]] | {{…p}} | {{…family}}, {{…m}} | {{…label}} | split of a known τ_sel |
| InternVL3-8B (τ = −∞) | τ_sel | [[VER::sets.ov_dev_b.rows.internvl3_8b~tau_sel]] | {{…p}} | none, 1 | {{…label}} | batch-1 re-decode of a known τ_sel |
| Aya-Vision-8B | τ_pair | [[VER::sets.ov_dev_b.rows.aya_vision_8b~tau_pair]] | {{…p}} | none, 1 | {{…label}} | split of a known τ_sel; first look, no registered claim |
| Aya-Vision-8B | τ_marg | [[VER::sets.ov_dev_b.rows.aya_vision_8b~tau_marg]] | {{…p}} | none, 1 | {{…label}} | split of a known τ_sel; first look, no registered claim |
| Aya-Vision-8B | τ_sel | [[VER::sets.ov_dev_b.rows.aya_vision_8b~tau_sel]] | {{…p}} | none, 1 | {{…label}} | batch-1 re-decode of a known τ_sel |
| each backbone | τ_any | [[VER::sets.ov_dev_b.rows.<m>~tau_any]] | {{…p}} | none, 1 | {{…label}} | – |

`{{…}}` abbreviates the row's own key path in the same file. Order of rows: the nominated claims of Qwen2.5-VL-7B first (§7.5 item 4 of the registration), then InternVL3-8B, then Aya-Vision-8B. The family column reads `registered (§7.5)` for a nominated claim (the scorer's family name; printed in the paper as "nominated claims") and "none" otherwise. τ_any exists only where the batch-size-1 `zs` run of Tier B finished.

**Sentences of Section 6.10.3, one per registered outcome.** Exactly one of Z, N0 or N+ applies; under N+, one of PASS or FAIL applies to each nominated claim.

- **Z (block 1b closed without a verdict; release clause).** Applies when `NOM::closed` exists. Not expected: D1 passed for every backbone (OPS-1112j) and Tier A completed (OPS-1112af), so `close` has no registered trigger; if `NOM::closed` exists anyway, a judge line comes first. Sentence: "Block 1b closed without a verdict ({{NOM::closed}}). No batch-size-1 OV-dev-A or OV-dev-B row was scored, so the attribution study carries no registered claim; its remaining rows (Sections 6.10.4–6.10.7) are descriptive." Table 15 and Table 16 are then omitted, with the line "NOT RUN: block 1b closed ({{NOM::closed}})".
- **N0 (nothing nominated).** Applies when `{{NOM::nominated}}` is empty and `NOM::closed` is absent; `{{VER::no_claim}}` then reads "no claim was nominated on OV-dev-A". Sentences: "On OV-dev-A no τ_pair or τ_marg row of Qwen2.5-VL-7B or InternVL3-8B had a 95% lower bound of at least +2.0 (Table 15): no claim was nominated on OV-dev-A, so the attribution study has no registered claim. The OV-dev-B rows of Table 16 are reported with their labels as descriptive rows; τ_pair and τ_marg there are a split of a known τ_sel. The study keeps τ_any, τ_sel, the variance terms (Section 6.10.5) and the copy bound (Section 6.10.6)."
- **N+ (m ≥ 1 claims nominated).** Opening sentence: "On OV-dev-A, {{NOM::nominated|count}} claim(s) met the nomination rule: {{NOM::nominated|names}} (Table 15). The nomination file was hashed and its sha256 logged before any new OV-dev-B output was scored, and the nominated claims form one Holm family of size m = {{NOM::nominated|count}} at family-wise one-sided α = 0.025." Then, for each nominated claim c = H_e(m), Qwen2.5-VL-7B's claims first (registration §7.5 item 4), then InternVL3-8B's, each backbone's claims in order of p̃ on OV-dev-B (the Holm order itself is by p̃ over the whole family and is computed from the keys, not from this reporting order):
  - **PASS** (`{{VER::sets.ov_dev_b.rows.<m>~<est>.label}}` = DETECTED): "<Claim c>: PASS. On OV-dev-B, <backbone>'s <estimand> was [[VER::sets.ov_dev_b.rows.<m>~<est>]] (p̃ = {{…p}}, Holm threshold {{α_j}}, m = {{…m}}): the nominated split held on a re-used development set, at batch size 1. This is a split of a known τ_sel, not new evidence that retrieval helps."
  - **FAIL** (label ≠ DETECTED): "FAIL: the claim nominated on OV-dev-A did not hold on OV-dev-B. <Backbone>'s <estimand> was [[VER::sets.ov_dev_b.rows.<m>~<est>]] (p̃ = {{…p}}, m = {{…m}}; label {{…label}}), against the registered rule of a point of at least +2.0 and p̃ at or below the Holm threshold." Add, only where the claim's own point is ≥ +2.0 and its p̃ ≤ its own α_j but an earlier claim in the p̃ order failed: "The Holm step-down had stopped at <earlier claim>, so no later claim could be DETECTED."
  - Closing sentence when at least one nominated claim FAILED: "For each failed claim the study keeps τ_any, τ_sel, the variance terms and the copy bound, and makes no registered claim about that component."
  - α_j is not a scorer key. It is computed in the text from the registered rule, α_j = 0.025 / (m − j + 1) with j the claim's rank by p̃ on OV-dev-B (ties by claim name); the manifest row cites `VER::alpha_familywise_one_sided`, `VER::sets.ov_dev_b.rows.<m>~<est>.p` and `VER::nominated`.
- **Rows that are not nominated** (any outcome). One sentence per row, by label, never merged across labels:
  - DETECTED: "<Backbone>'s <estimand> on OV-dev-B was [[…]] (p̃ = {{…p}}, m = 1): DETECTED, a descriptive row with no registered claim{{; split of a known τ_sel | ; batch-1 re-decode of a known τ_sel}}."
  - REVERSED: "<Backbone>'s <estimand> on OV-dev-B was [[…]]: REVERSED (95% upper bound below zero), a descriptive row{{note}}."
  - NEGLIGIBLE: "<Backbone>'s <estimand> on OV-dev-B was [[…|90]]: NEGLIGIBLE (90% interval inside (−2.0, +2.0)), a descriptive row{{note}}. This label has low power by design: at the planned standard error of Qwen2.5-VL-7B on OV-dev-B (about 1.03) it needs a point within about ±0.3 of zero (registration §7.13; values are for m = 1)."
  - UNRESOLVED: "<Backbone>'s <estimand> on OV-dev-B was [[…]]: UNRESOLVED (none of the registered labels applies), a descriptive row{{note}}."
- **Aya-Vision-8B** (any outcome): "Aya-Vision-8B has no OV-dev-A decodes, so its τ_pair and τ_marg on OV-dev-B are a first look with labels and no registered claim; on this set they are still a split of a known τ_sel." Then its rows by the label sentences above.

### 4.3 Section 6.10.4: XM-dev500 at batch size 1 (no rule)

**Table S21. XM-dev500 (500 images) at batch size 1, every backbone. DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; no rule (registration §7.8). Stripped CIDEr-D points, paired 95% bootstrap CIs, B = 2,000; R = 3, D = 2. Every row: "batch size 1; registered in v1.2 after K1 fired, on string-identity counts only".**

| backbone | τ_any | τ_sel | τ_marg | τ_pair | placebo `rand` d1 − d2 (flag) |
|---|---|---|---|---|---|
| Qwen2.5-VL-7B | [[SUM::sets.xm_dev500.rows.qwen25vl_7b~tau_any]] {{label}} | [[…~tau_sel]] {{label}} | [[…~tau_marg]] {{label}} | [[…~tau_pair]] {{label}} | [[…~placebo_d1_d2]] ({{…flag}}) |
| InternVL3-8B (τ = −∞) | same keys, `internvl3_8b` | | | | |
| Aya-Vision-8B | same keys, `aya_vision_8b` | | | | |

Sentence: "On XM-dev500 the rows carry no rule: at n = 500 neither DETECTED at +2.0 nor NEGLIGIBLE can be decided reliably (Section 5.7). Table S21 gives every row with its label; no XM-dev500 row enters a family or a scope sentence." If Tier C did not run: "XM-dev500 at batch size 1: NOT RUN (Tier C, {{reason}}; Section 6.10.1)." No other sentence about XM-dev500 numbers is written; labels speak for themselves in the table.

### 4.4 Placebo, variance components and the fixed set (Section 6.10.5)

**Table S23. Variance components. DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY.**

(a) Per-image draws, batch size 1 (rows with R ≥ 2; "batch size 1; registered in v1.2 after K1 fired, on string-identity counts only"):

| set | backbone | σ̂²_w | draw part σ̂²_w/(nR) | total s²(d̄_i)/n | share | placebo d1 − d2 [95% CI] | flag | tier |
|---|---|---|---|---|---|---|---|---|
| OV-dev-B | <m> | {{SUM::sets.ov_dev_b.variance.<m>.sigma2_w}} | {{….draw_part}} | {{….total}} | {{….share}} | [[SUM::sets.ov_dev_b.rows.<m>~placebo_d1_d2]] | {{….flag}} | post hoc (registration §7.7a) |
| XM-dev500 | <m> | {{SUM::sets.xm_dev500.variance.<m>.sigma2_w}} | {{….draw_part}} | {{….total}} | {{….share}} | [[SUM::sets.xm_dev500.rows.<m>~placebo_d1_d2]] | {{….flag}} | descriptive |

(b) One shared `fix` set, Qwen2.5-VL-7B (`fix` f0 stored, f1–f4 from block 1; batched only, so "A1 not met; batched decode; descriptive"):

| set | MS_F | MS_I | MS_E | V̂_b | V̄_img | ω̂ | ω^U | label (registered rule) | five-set row ȳ_·· [t interval, 4 df] |
|---|---|---|---|---|---|---|---|---|---|
| OV-dev-B | {{SUM::batched.ov_dev_b.fixed_set.qwen25vl_7b.MS_F}} | {{….MS_I}} | {{….MS_E}} | {{….V_b}} | {{….V_img}} | {{….omega}} | {{….omega_upper}} | {{….label}} | {{….dev_row.d}} [{{….dev_row.lo}}, {{….dev_row.hi}}] |
| XM-dev500 | {{SUM::batched.xm_dev500.fixed_set.qwen25vl_7b.MS_F}} | … | … | … | … | … | … | {{….label}} | … |

Sentences:
- Placebo not flagged on any set: "No `rand`-against-`rand` placebo row was flagged (|θ̂| ≥ 2.0 with a 95% interval that excludes zero; Table S23a)."
- Placebo flagged: "The `rand` d1 − d2 placebo of <backbone> on <set> was flagged ([[…]]). Under the registration a flagged set goes to a recorded review before its rows are used; {{review id and its consequence}}." (The consequence sentence is the judge's; it is not pre-written here. See §6.4, item J8.)
- Draw share: "The random draw accounted for a share {{…share}} of the image-bootstrap variance of <backbone>'s draw-averaged τ_sel on <set>; the intervals of Tables 16 and S21 include this part (Section 5.7)."
- Fixed set, ω^U ≤ 0.25: "With five fixed sets on <set>, ω̂ = {{omega}} and ω^U = {{omega_upper}}: by the registered rule the fixed-set rows are practically unconditional. These rows come from batched decodes (A1 not met; batched decode; descriptive)." This sentence stays in Section 6.10.5 and is attached to no registered row (CC-358, J7).
- Fixed set, ω^U > 0.25: "With five fixed sets on <set>, ω̂ = {{omega}} and ω^U = {{omega_upper}}: by the registered rule every `fix` row is conditional on the realised fixed set. These rows come from batched decodes (A1 not met; batched decode; descriptive). No test interval is widened, recomputed or relabelled with this number." Whether the label is attached to the existing `fix` rows of Tables 6 and S1–S4 is open for the judge (§6.4, item J7); until a ruling, the sentence stands in Section 6.10.5 only.
- Fixed set NOT RUN (fewer than two fixed sets scored): "Fixed-set variance on <set>: NOT RUN ({{reason}})."

### 4.5 Section 6.10.6: the copy bound (post hoc on OV-dev-B; first look at κ on XM-dev500)

**Table 17. Copy bound at n = 3 on stored decodes. DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY. Stripped CIDEr-D points, paired 95% bootstrap CIs, B = 2,000. OV-dev-B: POST HOC. XM-dev500: first look at κ (the stage-B near-verbatim copy share on this set had been seen). The rows bound the stored, batched `ret` − `rand` d0 contrast, not the batch-size-1 τ_sel of Table 16. Aya-Vision-8B on XM-dev500 uses block-1 batched decodes: "A1 not met; batched decode; descriptive".**

| set | backbone | unit | K_ret [95% CI], label | L_cp [95% CI], label | K_nc [95% CI], label | bound | flags |
|---|---|---|---|---|---|---|---|
| OV-dev-B | <m> | (i) syllables | [[CB_ov_dev_b_<m>::bound.i_syllables.n3.K_ret]], {{….label}} | [[…n3.L_cp]], {{….label}} | [[…n3.K_nc]], {{….label}} | withdrawn if `n3.withdrawn` is true in either unit of the set, else in force | "monotonicity check failed" if `{{CB_ov_dev_b_<m>::bound.i_syllables.monotonicity check failed}}` is true |
| OV-dev-B | <m> | (ii) words | same keys under `bound.ii_words` | | | | |
| XM-dev500 | <m> | (i), (ii) | same keys in `CB_xm_dev500_<m>` | | | | |

**Table S24** (supplement) prints every n (2, 3, 4), both units, and the companions K_rand (`….K_rand`), K_ret − K_nc (`….K_ret_minus_K_nc`, label "descriptive; never called a bound") and the blind loss (`….blind_loss`; printed "NOT RUN: no admitted blind run staged" when `{{CB_<set>_<m>::blind}}` says so), with the tier from `….tier`.

Sentences, per set × backbone × unit, at n = 3 (both units are reported; the registration does not make one unit decide, see §6.4, item J4):
- **Bound withdrawn** (`n3.withdrawn` true in either unit of the set, i.e. K_nc REVERSED at n = 3 in unit (i) or (ii); registration §8 withdraws the bound "for that set"): "On <set>, unit <u>, K_nc was REVERSED ([[…K_nc]]): the stated direction of assumption A_cp is contradicted, and the copy bound is withdrawn for this set, in both units. K_ret and L_cp are printed in Table S24 without a reading." No reading sentence follows for either unit of that set.
- **Bound in force, L_cp DETECTED:** "On <set>, unit <u>, L_cp was [[…L_cp]], DETECTED: a retrieval-specific effect of at least +2.0 remains under the most pessimistic copy attribution."
- **Bound in force, L_cp point ≤ 0:** "On <set>, unit <u>, L_cp was [[…L_cp]]: the bound does not exclude that the whole retrieval-specific effect is carried by copied n-grams; this agrees with, and does not prove, the published short-cut account [@Li2025UnveilingICL]."
- **Bound in force, any other L_cp outcome:** "On <set>, unit <u>, L_cp was [[…L_cp]] ({{…label}}): partly bounded."
- **Monotonicity flag** (appended to whichever sentence applies): "This bound carries the flag 'monotonicity check failed': K_ret increased from n = 2 to n = 4 (Table S24)."
- **Tier clause**, appended once per set: OV-dev-B "These rows are post hoc: the bound was specified after naive masked rows on this set had been seen, and was computed once on stored outputs." XM-dev500 "These rows are a first look at κ on XM-dev500, although the stage-B near-verbatim copy share on this set had been seen."
- **Row NOT RUN** (`PH::copy_bound.<set>~<m>` begins with "NOT RUN"): "Copy bound, <set>, <backbone>: NOT RUN ({{PH::copy_bound.<set>~<m>}})."
- **English copy bound** (always, as of this package): "The English copy bound on the Flickr30K carve and Flickr30K val, registered as a post hoc row, was not coded and was not run."
- **Placebo check of κ** (registration §8 "κ of a `zs` run against itself is 0"): the scorer holds it as a self-test on planted data, not as an output key. The paper states: "κ of a `zs` caption against itself is zero by construction; the scorer's self-test checks it." No number is printed.

### 4.6 Section 6.10.7: batched rows (descriptive sensitivity row)

**Table S22. Batched block-1 rows with the stored runs of the same set, every backbone. "A1 not met; batched decode; descriptive". No family, no PASS or FAIL, no scope sentence. On OV-dev-A and OV-dev-B the `ret`, `zs` and `rand` d0 columns are the stored decodes (and, on OV-dev-B, stored `rand` d1–d2 where they exist), and `perm` p1–p2 and `fix` f1–f4 come from block 1, decoded on the new machine with host parity passed.**

| set | backbone | τ_sel | τ_marg | τ_pair | τ_any | R, D | host label |
|---|---|---|---|---|---|---|---|
| <set> | <m> | [[SUM::batched.<set>.rows.<m>~tau_sel]] {{label}} | [[…~tau_marg]] {{label}} | [[…~tau_pair]] {{label}} | [[…~tau_any]] {{label}} | {{…~tau_sel.R}}, {{…~tau_pair.D}} | {{…host}} if present |

Sentence: "Table S22 prints the batched block-1 rows beside the batch-size-1 rows as a descriptive sensitivity row. They carry 'A1 not met; batched decode; descriptive'. On the post hoc, untested reading of Section 6.10.2, their `ret` − `perm` contrast is the effect of switching a whole fixed-slice decoding policy, and their image-bootstrap intervals do not account for any coupling of images within a batch slice." If `{{…host}}` is absent for every row: "Host parity held for every backbone, so no base arm was re-decoded." No sentence compares a batched row with its batch-size-1 counterpart; that comparison is open for the judge (§6.4, item J10).

### 4.7 Document-frequency sensitivity (Section 6.10.3, last paragraph; Table S25a)

**Table S25 (a). Document-frequency sensitivity, Qwen2.5-VL-7B, OV-dev-B, batch size 1. Rows 1–200 of the set's shared index matrix. Descriptive, no rule.**

| estimand | nominated? | point | 95% interval, df recomputed per resample | 95% interval, df fixed, same 200 resamples |
|---|---|---|---|---|
| τ_pair | {{DFS::rows.tau_pair.nominated}} | {{DFS::rows.tau_pair.d}} | [{{DFS::rows.tau_pair.lo_df_resampled}}, {{DFS::rows.tau_pair.hi_df_resampled}}] | [{{DFS::rows.tau_pair.lo_df_fixed}}, {{DFS::rows.tau_pair.hi_df_fixed}}] |
| τ_marg | {{DFS::rows.tau_marg.nominated}} | {{DFS::rows.tau_marg.d}} | [{{…lo_df_resampled}}, {{…hi_df_resampled}}] | [{{…lo_df_fixed}}, {{…hi_df_fixed}}] |

Sentences:
- Computed (`DFS::status` = "computed"): "Recomputing document frequencies inside 200 bootstrap resamples gave the intervals of Table S25a beside the fixed-document-frequency intervals over the same resamples; the row is descriptive and has no rule."
- NOT RUN (`DFS::status` begins "NOT RUN"): "The document-frequency sensitivity row was not run ({{DFS::status}})."
- Stopped by its parity check (the `ovb` stage stopped with "SENSITIVITY PARITY FAIL" after the verdict file existed): "The document-frequency sensitivity row was not run: its full-document-frequency scores did not reproduce the ledger within 1e-4 ({{LOG:<OPS line of the stop>}}). The verdict of Section 6.10.3 was written before this check and is unaffected; any later computation of the row would be post hoc."

### 4.8 Post hoc swap companion (Section 6.10.6, last paragraph; Table S25b)

**Table S25 (b). Memory-source companion on stored Flickr30K carve cells (English, 1,000 Flickr30K train images). "POST HOC; size-confounded (full COCO memory, 111,927 clusters, against the Flickr30K-train memory, 28,000)". PTB CIDEr-D points, paired 95% bootstrap CIs, B = 2,000.**

| backbone | τ_sel, Flickr30K-train memory | τ_sel, COCO memory | δ [95% CI], label | rule L, Flickr30K-train cell | rule L, COCO cell |
|---|---|---|---|---|---|
| <m> | [[PH::swap.rows.<m>.tau_sel_f30k]] | [[PH::swap.rows.<m>.tau_sel_coco]] | [[PH::swap.rows.<m>.delta]], {{….label}} | {{PH::swap.length.<m>~<mem_f30k>.rel_gap}}; "not separated from length" if `{{…not separated from length}}` is true | {{PH::swap.length.<m>~<mem_coco>.rel_gap}}; same |

Sentences:
- Computed: "A post hoc companion compares the retrieval contrast with a same-source and an other-source memory on the same 1,000 Flickr30K train images: δ = [[PH::swap.rows.<m>.delta]] for <backbone> ({{label}}). The two memories differ in size as well as source (111,927 against 28,000 clusters), so δ does not separate source from size; it is post hoc and size-confounded, and no reading sentence of the registration is applied to it." Add per cell with the flag true: "The <memory> cell of <backbone> is not separated from length (rule L)."
- Rule L NOT RUN for a cell (no carve run with a hash of record was staged): "Rule L, <backbone>, <memory>: NOT RUN (no carve run with a hash of record)."
- Swap NOT RUN (`PH::swap` begins "NOT RUN"): "The post hoc memory-source companion was not run ({{PH::swap}})."
- The registered swap on fixed Flickr30K val images (block 4, size matched by construction) and its fixed reading sentences are reported only if block 4 ran (§4.9, item B4).

### 4.9 Section 6.10.8: NOT RUN and stop cases (exact sentences)

Paper heading: **6.10.8 What did not run.** The sentences below that apply are printed under it, in this order: V, S or T (if one applies), Tier B, Tier C, B2 with the scope sentence, B3, B4.

- **V (verification stage failed).** "Scoring of the attribution study stopped at its verification stage ({{LOG:<id>}}); no attribution row exists." Tables 15–17 and S21–S25 are omitted.
- **S (a later scoring stage stopped: `ova`, `ovb` before its verdict file exists, `rest` or `posthoc`).** "Scoring of the attribution study stopped at its <stage> stage ({{LOG:<id>}}); the rows of that stage and of every later stage were not computed." The tables of those stages are printed "NOT RUN" with this sentence. A stop of `ovb` after its verdict file exists is the document-frequency case of §4.7.
- **T (Tier A in part: a cap stop, a job stop or the freeze before the last Tier-A step).** Does not apply: block 1b ended with JOB DONE, no cap stop and no job stop (LOG OPS-1112af; CC-358, J3); kept as a record only. The registration's run document makes this a stop before any score, pending a judge line. Sentence, if no judge line licenses scoring: "Block 1b stopped before its registered family was complete ({{reason}}); under the run document no batch-size-1 output was scored." Any other wording follows the judge's line (§6.4, item J3).
- **Tier B dropped** (Aya-Vision-8B on OV-dev-B, or the `zs` runs): "Aya-Vision-8B at batch size 1 on OV-dev-B: NOT RUN (Tier B, {{reason}})." or "τ_any at batch size 1 on OV-dev-B: NOT RUN (Tier B `zs` runs, {{reason}})."
- **Tier C dropped:** "XM-dev500 at batch size 1: NOT RUN (Tier C, {{reason}})."
- **B2 (block 2: new backbones outside the Qwen line).** If not run: "Block 2, which would have added backbones outside the Qwen language-model line, was not run by its registered cut-off (2026-11-14 18:00, UTC+7) or before the freeze; the secondary family S-BB is empty." If run, its rows need their own text package (the scoring run document covers block 1b, block 1 and block 0 only).
- **Scope sentence (registration §7.6), every case.** The sentence is chosen by the number of non-Qwen backbones whose τ_sel on OV-dev-B is DETECTED, counting Aya-Vision-8B's row with the flag that it is outside every family ("batch-1 re-decode of a known τ_sel"):
  - 2 or more: "the retrieval-specific effect is not limited to the Qwen language-model line";
  - exactly 1: "the retrieval-specific effect was seen for one backbone outside the Qwen line";
  - 0: "the retrieval-specific effect was not seen outside the Qwen line on this set".
  With block 2 not run, the count is Aya-Vision-8B's row alone ({{VER::sets.ov_dev_b.rows.aya_vision_8b~tau_sel.label}}), and the sentence adds: "This count rests on one backbone, Aya-Vision-8B, whose row is post hoc (its τ_sel on this set was known before the registration) and a batch-1 re-decode of a known τ_sel; no backbone first decoded under this registration was run." Which Aya-Vision-8B row counts is open for the judge (§6.4, item J5).
- **B3 (block 3: re-implemented third-party arms).** If not run: "Block 3 was not run before the freeze: the arms that apply the split to a re-implementation of the LMCap recipe by this study; not the authors' code (no licence); not a statement about the published numbers, and to an image-caption-pair prompt format, as used by RAGCap; not RAGCap, have no rows. The registered positive control, which needs the LMCap re-implementation's τ_sel on OV-dev-B, was therefore not run." (Note, not paper text: in every case the paper calls this study an "attribution analysis", never a "test" of the method; CC-358, J6.)
- **B4 (block 4: English arms on Flickr30K val).** If not run: "Block 4 was not run before the freeze: the English `perm` and extra `rand` arms and the size-matched memory swap on fixed Flickr30K val images have no rows. The memory-source question on Vietnamese data could not be posed in any case: the registered Vietnamese memory holds 40 KTVIC-only clusters out of 8,190, so no out-of-source Vietnamese memory exists in it."

### 4.10 Section 6.11 Compute: sentence added

> The attribution study used {{GS1::gpu_h}} GPU-hours in block 1 (cap 12) and {{GS1B::gpu_h}} in block 1b (cap {{CAP::cap_h}}), on one 24 GB GPU; its scoring ran on CPU.

### 4.11 Supplement Table S20 and Table S26

**Table S20. Step-1.0 and D1 string-identity counts (first 50 items; counts only, no score).**

| backbone | (a) host parity, OV-dev-B | (a) host parity, OV-dev-A | (b) A1, reversed, batch size 1 against (a) | K1 | D1, batch size 1, stored order against reversed |
|---|---|---|---|---|---|
| Qwen2.5-VL-7B | {{S10A_qwen25vl_7b_ov_dev_b::identical}}/{{…n}} | {{S10A_qwen25vl_7b_ov_dev_a::identical}}/{{…n}} | {{S10B_qwen25vl_7b::identical}}/{{…n}} | {{STEP10_qwen25vl_7b::A1}} → fired if FAIL | {{D1_qwen25vl_7b::identical}}/{{…n}}, {{STEP1B0_qwen25vl_7b::D1}} |
| InternVL3-8B | {{S10A_internvl3_8b_ov_dev_b::identical}}/{{…n}} | {{S10A_internvl3_8b_ov_dev_a::identical}}/{{…n}} | {{S10B_internvl3_8b::identical}}/{{…n}} | {{STEP10_internvl3_8b::A1}} | {{D1_internvl3_8b::identical}}/{{…n}}, {{STEP1B0_internvl3_8b::D1}} |
| Aya-Vision-8B | {{S10A_aya_vision_8b_ov_dev_b::identical}}/{{…n}} | – (no OV-dev-A run) | {{S10B_aya_vision_8b::identical}}/{{…n}} | {{STEP10_aya_vision_8b::A1}} | {{D1_aya_vision_8b::identical}}/{{…n}}, {{STEP1B0_aya_vision_8b::D1}} |

Values of record in the LOG (counts, not scores): (a) 50/50 on every check, (b) 42/50, 37/50, 31/50 (OPS-1111ba); D1 50/50 for each (OPS-1112j-c-attr-1b-pause). The verdict files are pinned by full sha256 in the addendum's values table (STEP10) and re-hashed at the final pull (STEP1B0, D1).

**Table S26. `perm` list diagnostics (block 0, computed before any decode; list properties, no score).**

| set | p | refill share at 8 slots | gate (≤ 0.10) | share of slots shared with `ret` (k = 4; k = 8) | mean cosine to q of shown clusters, k = 8: `ret`, `perm`, `rand` d0 |
|---|---|---|---|---|---|
| <set> | p1, p2 | {{K0::diagnostics.<set>.p<p>.refill_share_8}} | {{K0::diagnostics.<set>.p<p>.refill_gate}} | {{K0::diagnostics.<set>.p<p>.overlap_with_ret_4}}; {{….overlap_with_ret_8}} | {{….mean_cos_ret_8}}, {{….mean_cos_perm_8}}, {{….mean_cos_rand_d0_8}} |

Plus one line per set: images with π_1(q) = π_2(q): {{K0::diagnostics.<set>.same_donor_p1_p2}}. Sentence: "On every set the refill share stayed within the registered gate, so `perm` carries its rules on every set (Table S26)." If a gate had read otherwise, the sentence would be "On <set> the refill share exceeded 0.10, so `perm` there is a diagnostic with no rule"; the block-1 run document v1.1 §1 records the gate as passed on every set before any decode (a list property, not a score); the sentence is checked against the keys at transfer.

---

## 5. Disclosure and limitation text

### 5.1 Section 7.5: The attribution study (new subsection after 7.4)

> **7.5 The attribution study**
>
> The attribution study of Sections 3.8, 5.7 and 6.10 uses development sets only. It was registered after every test set of this paper had been decided, so its design could take their results into account; OV-dev-A and OV-dev-B had already carried the stage-A and stage-B rows, the ablations of Section 6.8 and earlier masked rows, and on both the sum τ_sel was known before the split was looked at (Section 5.7). The following were disclosed in its records.
>
> - **Block order.** Block 0 (CPU: list construction, the `perm` list check and the refill gate) ran before any decode. Block 1 decoded the new arms in batches; kill gate K1 fired at its first step (Section 6.10.2), and the block was left running as registered and ended by itself with all its steps complete. The addendum for block 1b was written after K1 fired and before any block-1 output was scored or opened; the only block-1 information seen then was the identity counts, the ids of the differing items, the timing lines and the verdict-file hashes, none of which carries a score. Block 1b re-decoded every contrast arm at batch size 1. Scoring followed in the registered order (Section 5.7). Blocks 2–4 {{status sentence of §4.9, items B2–B4}}.
> - **Mutant check on the rented machine.** The block-1 run document required the code's mutant tests to run on the rented machine before any decode. The machine's container refused the user namespaces that the mutant runner used for network isolation, so that check was not run there. A recorded review accepted, as a deviation, the record of the same mutant run made earlier on the authors' laptop on byte-identical code (22 of 22 mutants killed), together with the self-tests that passed on the rented machine. The later mutant runs for the block-1b code (33 of 33 killed) and for the scoring code (73 of 73 killed) ran on the rented machine with an option that drops the network isolation, and are recorded as not network-isolated.
> - **Checksum lists of the output trees.** The decode job writes the checksum list of its output tree before its last log lines, so a check of the pulled tree against that list reports one mismatch, the job's own log file. The whole-tree digest of the pulled copy was compared with the machine's instead, and matched; the scoring stage exempts only that log file and refuses any unlisted file.
> - **Software environment.** The decode environment's Python was 3.10.22 where the earlier record names 3.10.12, with the package freeze equal to its pin; the CPU environment was built from a committed freeze that adds scipy. Host parity (Section 6.10.2) and the scoring parity gate (Section 5.7) are the checks that bind these differences. The model download used a fixed address of the model host's content network, with TLS verification on and every model file accepted only on its pinned hash.
> - **Other work on the same machine.** CPU-only work of another study of the group ran on the rented machine while blocks 1 and 1b decoded: code self-tests and mutant runs and, during block 1b, the staging of that study's inputs (disk, network and hashing; no model load and no GPU use). The registration's rule is that no job runs beside another; these instances are disclosed here as deviations from it. The host checks of the attribution study's own scoring code also ran while block 1b decoded (CPU only, low priority, never during the D1 step). Whether CPU load can change a greedy GPU string was not tested; timings may have been longer, and the block-1b cap is counted as job wall time.
> - **Scorer fixes before any score.** Four scorer defects were found and fixed before any score existed, each without changing a registered quantity: OV-dev-A references are read through the stage-A reader that produced the stored OV-dev-A scores; masked columns no longer enter the draw means; a second `zs` run of one backbone in one call is refused; and a stored `zs` scored in two calls enters the summary once.
> - **What was post hoc.** The copy bound on OV-dev-B (specified after naive masked rows on that set were seen); the variance rows of the three stored backbones on OV-dev-B; the memory-source companion on the Flickr30K carve (size-confounded); and the batch-size-1 design itself, which was registered after K1 fired, though before any score. The reading that left padding couples images within a batch (Section 6.10.2) is a post hoc reading of the decoder code, not a tested claim. The document-frequency sensitivity row was defined in the registration and fixed in exact terms by a ruling before any score.
> - **Earlier contact.** Aya-Vision-8B's τ_sel on OV-dev-B was known from the exploration runs of the Flickr30K registration, and its stored, batched value is printed only in Table S22; the stage-B near-verbatim copy share on XM-dev500 had been seen before the κ rows there.

**Box 2, rows appended (Section 7):**

| item | effect on data | exposure of test data | verdict changed? |
|---|---|---|---|
| attribution study registered after all test verdicts, on re-used development sets where τ_sel was known (Section 5.7) | development rows only, labelled | none | no |
| kill gate K1 fired; block-1b at batch size 1 registered after K1, before any score (Section 6.10.2) | batched rows descriptive only | none | no |
| mutant check of block 1 not run on the rented machine; laptop record accepted; later mutant runs not network-isolated (Section 7.5) | none | none | no |
| other CPU checks beside running decodes; pulled-tree checksum list omits the job's final log lines (Section 7.5) | none | none | no |

### 5.2 Section 9: limitation and threat text

**Section 9.1, two new bullets after "One test look, one machine, one run, one random draw":**

> - **The attribution study is development-only, on re-used sets.** Its rows come from OV-dev-A, OV-dev-B and XM-dev500, which had carried earlier development rows; on OV-dev-A and OV-dev-B τ_sel was known, so τ_pair and τ_marg there are a split of a known sum. Whatever the outcome of its one look (Section 6.10.3), it is a development result for the backbones and configurations of that look, not a test result, and it says nothing about other sets, models or memories. Its registered claim can involve only Qwen2.5-VL-7B and InternVL3-8B, which share the Qwen2.5 language-model line; Aya-Vision-8B's rows are a first look with no claim. The copy bound rests on assumption A_cp, which can only overstate copying, and it bounds the stored batched contrast, not the batch-size-1 one.
> - **Batch composition changes greedy captions.** For all three backbones, decoding the same images one at a time instead of in batches changed {{S10B_qwen25vl_7b::failing_ids|count}}, {{S10B_internvl3_8b::failing_ids|count}} and {{S10B_aya_vision_8b::failing_ids|count}} of 50 greedy captions (Section 6.10.2). The registered results of this paper are therefore results of the systems as run: fixed batches for both arms of every contrast between text-example arms of one backbone, and one query at a time for the LMCap re-implementation and the interleaved image-caption arm (Section 6.10.2). No number changes; but a per-image difference between arms decoded in batches can contain a batch-mate term, and the image bootstrap does not model the coupling of images within a batch slice. The attribution study's rows avoid this by decoding at batch size 1; the check is by string identity and says nothing about which policy gives better captions.

**Section 9.2, Internal validity, sentence appended:**

> In the attribution study, `perm` keeps the kind of list that retrieval produces while breaking its link to the query image; it is built from a fixed permutation that depends on no output, it is filtered by the query's own near cut, and its refill share was checked before any decode (Table S26).

**Section 9.2, Construct validity, sentence appended after the masked-rows sentence:**

> The attribution study's copy bound replaces the naive masked contrast by a placebo-corrected one: the zero-shot caption, which never saw the shown captions, measures the overlap that needs no copying, and the `rand` caption checks the direction of that assumption (Section 3.8); it remains a bound under a stated assumption, not an estimate of copying.

**Section 9.3, sentence appended:**

> In our checks (three models, one software stack, 50 development items each), greedy captions were reproduced exactly when the same images were decoded in the same batch slices, and some changed when the same images were decoded one at a time (Section 6.10.2). An exact re-run therefore needs the same batch slices as well as the same snapshots and software; the batch size of each backbone is fixed in the released code.

### 5.3 Supplement: section header text

> **Attribution study (C-ATTR-DEV): every row.** Development data only; DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY. Tables S20–S26 give every row of the study's scoring files, with the label, family, tier and batch label the scorer wrote. Batch-size-1 rows carry "batch size 1; registered in v1.2 after K1 fired, on string-identity counts only"; batched rows carry "A1 not met; batched decode; descriptive". The registration, its erratum and addendum, the run documents and the rulings that read them are released with the code.

### 5.4 Corrections owed under CC-340 W6 (same-slice parity, not batch invariance)

| place | current text (paper repo `f6aa449`) | replacement |
|---|---|---|
| Section 9.1, bullet "One test look, one machine, one run, one random draw", last sentence | "Decode-parity checks on the same machine and software stack found no run-to-run variation on development data (52/52 identical captions per backbone; supplement, "Test-run operations", and Table S14)." | "Decode-parity checks that re-decoded the same development images in the same batch slices on the same software stack gave identical captions (52/52 per backbone; supplement, "Test-run operations", and Table S14); they show run-to-run parity, not independence from batch composition; a later development check found that decoding one image at a time changed some captions (Section 6.10.2)." |
| Box 2, row 1, column "effect on data" | "development images only (52/52 identical captions per backbone at the check of record)" | "development images only (52/52 identical captions per backbone at the check of record; same items in the same batch slices, so run-to-run parity, not batch invariance; Section 6.10.2)" |
| Supplement, "Decode-parity check before the Vietnamese test, and its reruns", closing paragraph | (paragraph beginning "All three attempts used development data only.") | append: "These checks re-decoded the same images in the same batch slices; they establish run-to-run parity, not independence from batch composition (Section 6.10.2)." |
| Supplement, development-ablation record, "Decode parity on 52 OV-dev-B images: 52/52 identical for both backbones." | as quoted | append: "(same items, same batch slices: run-to-run parity)" |

None of these corrections changes a number, a verdict or a check of record; they change what the checks are said to show.

---

## 6. Claim → evidence, manifest rows, and open points

### 6.1 Claim → evidence table

Status words: REGISTERED (PASS/FAIL by the registered rule), DESCRIPTIVE (labelled row, no rule), POST HOC, FACT (a count or run record, not a score), NOT RUN.

| # | claim (as it may appear) | section | status | table | evidence (`file::key`) |
|---|---|---|---|---|---|
| C1 | K1 fired for all three backbones (identity counts) | 6.10.2 | FACT | S20 | `S10B_<m>::identical`, `::n`, `::failing_ids`; `STEP10_<m>::A1`; LOG OPS-1111ba |
| C2 | host parity held | 6.10.2 | FACT | S20 | `S10A_<m>_<set>::identical`; `STEP10_<m>::host_parity` |
| C3 | at batch size 1 the item order changed none of the 50 captions (D1) | 6.10.2 | FACT | S20 | `D1_<m>::identical`, `::n`; `STEP1B0_<m>::D1`; LOG OPS-1112j-c-attr-1b-pause |
| C4 | the differences in (b) go with batch composition, not order | 6.10.2 | FACT (inference from C1 and C3 counts only) | S20 | C1 + C3 |
| C5 | left padding couples batch-mates | 6.10.2 | POST HOC reading of code, not tested | – | `scripts/lb/decode_hf_vlm.py` (`padding_side = "left"`, `padding=True`, greedy); CC-340 ruling 2 |
| C6 | registered rows of the paper are "the system as run in fixed batches"; no number changes | 6.10.2, 9.1 | FACT about procedure | – | CC-340 ruling 2, W6 |
| C7 | the 52/52 checks were same-slice parity | 9.1, Box 2, supplement | FACT about procedure | – | addendum v1.2 V9; CC-340 W6; supplement "Test-run operations" |
| C8 | which claims were nominated, or none | 6.10.3 | REGISTERED step | 15 | `NOM::nominated`, `NOM::rows.<m>~<est>.{d,lo,hi}`; nomination sha in the LOG |
| C9 | each nominated claim PASS or FAIL | 6.10.3 | REGISTERED (PASS iff label DETECTED) | 16 | `VER::sets.ov_dev_b.rows.<m>~<est>.{d,lo,hi,p,label,family,m,note,batch}`; `VER::nominated`; `VER::alpha_familywise_one_sided` |
| C10 | "no claim was nominated on OV-dev-A" | 6.10.3 | REGISTERED sentence (case N0) | 15, 16 | `VER::no_claim`; `NOM::nominated` = [] |
| C11 | block 1b closed without a verdict | 6.10.3 | REGISTERED release clause (case Z) | – | `NOM::closed`; LOG "1b closed: <reason>" |
| C12 | τ_sel, τ_any and non-nominated τ_pair/τ_marg rows on OV-dev-B, with labels | 6.10.3 | DESCRIPTIVE | 16 | `VER::sets.ov_dev_b.rows.<m>~<est>.*` |
| C13 | Aya-Vision-8B split on OV-dev-B | 6.10.3 | DESCRIPTIVE (first look) | 16 | `VER::sets.ov_dev_b.rows.aya_vision_8b~{tau_pair,tau_marg}.*` |
| C14 | scope sentence of §7.6 | 6.10.3 / 4.9 | REGISTERED sentence; count rests on Aya-Vision-8B alone if block 2 not run | 16 | `VER::sets.ov_dev_b.rows.aya_vision_8b~tau_sel.label` (+ S-BB rows if block 2 ran) |
| C15 | XM-dev500 rows | 6.10.4 | DESCRIPTIVE, no rule | S21 | `SUM::sets.xm_dev500.rows.<m>~<est>.*` |
| C16 | placebo flags; draw share | 6.10.5 | DESCRIPTIVE (OV-dev-B post hoc) | S23a | `SUM::sets.<set>.rows.<m>~placebo_d1_d2.{d,lo,hi,flag}`; `SUM::sets.<set>.variance.<m>.{sigma2_w,draw_part,total,share}` |
| C17 | fixed-set label (ω^U rule) | 6.10.5 | DESCRIPTIVE label; batched, A1 not met | S23b | `SUM::batched.<set>.fixed_set.qwen25vl_7b.{omega,omega_upper,label,dev_row}` |
| C18 | copy-bound reading sentence per set × backbone × unit | 6.10.6 | POST HOC (OV-dev-B); first look at κ (XM-dev500) | 17, S24 | `CB_<set>_<m>::bound.<unit>.n3.{K_ret,L_cp,K_nc}.{d,lo,hi,label}`, `….n3.withdrawn`, `….monotonicity check failed`; `PH::copy_bound.<set>~<m>` |
| C19 | English copy bound not coded, not run | 6.10.6 | NOT RUN | – | scoring run document v1.1 step 5; CC-348 ruling 4 |
| C20 | batched rows printed as sensitivity row | 6.10.7 | DESCRIPTIVE ("A1 not met; batched decode; descriptive") | S22 | `SUM::batched.<set>.rows.<m>~<est>.*` |
| C21 | document-frequency sensitivity | 6.10.3 | DESCRIPTIVE | S25a | `DFS::status`, `DFS::rows.{tau_pair,tau_marg}.*` |
| C22 | memory-source companion on the carve | 6.10.6 | POST HOC; size-confounded | S25b | `PH::swap.rows.<m>.{delta,tau_sel_f30k,tau_sel_coco}.*`; `PH::swap.length.*` |
| C23 | `perm` refill gate passed | 3.8, 9.2 | FACT (list property) | S26 | `K0::diagnostics.<set>.p<p>.{refill_share_8,refill_gate}` |
| C24 | GPU-hours of blocks 1 and 1b | 6.11 | FACT | – | `GS1::gpu_h` (LOG OPS-1112c: 6.41), `GS1B::gpu_h`, `CAP::cap_h` (LOG OPS-1112j-c-attr-1b-pause) |
| C25 | blocks 2–4, positive control, swap: status | 6.10.8 / 4.9 | NOT RUN or own package | – | LOG lines at K7 |

### 6.2 Manifest rows to append to `number_manifest_C.tsv`

Columns as the skill requires (`number | file::key | raw_value | sha256_prefix | status | used_in`). `raw_value` and `sha256_prefix` are filled at transfer from the pulled 0444 files; `status` is `PENDING_SCORE` for every score row and `FACT_RECORDED` for the counts whose values are in the LOG.

| number | file::key | raw_value | sha256_prefix | status | used_in |
|---|---|---|---|---|---|
| K1 count, Qwen2.5-VL-7B | `S10B_qwen25vl_7b::identical` (and `::n`) | (LOG OPS-1111ba: 42 of 50) | at pull | FACT_RECORDED | 6.10.2; S20 |
| K1 count, InternVL3-8B | `S10B_internvl3_8b::identical` | (LOG: 37 of 50) | at pull | FACT_RECORDED | 6.10.2; S20 |
| K1 count, Aya-Vision-8B | `S10B_aya_vision_8b::identical` | (LOG: 31 of 50) | at pull | FACT_RECORDED | 6.10.2; S20 |
| changed captions | `S10B_<m>::failing_ids` (length) | (LOG: 8, 13, 19) | at pull | FACT_RECORDED | 6.10.2 |
| host parity counts | `S10A_<m>_<set>::identical` | (LOG: 50 of 50 each) | at pull | FACT_RECORDED | S20 |
| D1 counts | `D1_<m>::identical` | (LOG: 50 of 50 each) | at pull (final) | FACT_RECORDED | 6.10.2; S20 |
| block-1 GPU-h | `GS1::gpu_h` | (LOG OPS-1112c: 6.41) | at pull | FACT_RECORDED | 6.10.1; 6.11 |
| block-1b cap | `CAP::cap_h` | (LOG OPS-1112j: 17.95) | `6d42608e` (LOG) | FACT_RECORDED | 6.10.1; 6.11 |
| block-1b GPU-h | `GS1B::gpu_h` | (LOG OPS-1112af: 12.27) | at pull | FACT_RECORDED | 6.10.1; 6.11 |
| block-1b runs | `SUM::n_b1_runs` (`job.log` OK lines, `STEPS_1B.tsv`) | (LOG OPS-1112af: 55 OK lines = 50 runs + 3 D1 + 2 other; OPS-1112j: 50 planned runs; no CAP STOP, no JOB STOP) | `bd9139b0` (STEPS_1B.tsv, LOG) | FACT_RECORDED | 6.10.1 |
| every row of Tables 15–17, S21–S25 | the keys printed in §4 | – | at pull | PENDING_SCORE | 6.10; S21–S25 |
| refill shares, overlaps, cosines | `K0::diagnostics.*` | committed | `15108f2b` | FACT_RECORDED | S26 |

The values in parentheses are the LOG's values of record, given so that the transfer can check the pulled files against them; they are counts and run facts, not scores. Every score-bearing number stays a placeholder until the stage files exist.

### 6.3 Pre-transfer checks (to run on the filled text)

- Every number in Sections 3.8, 5.7, 6.10 and the supplement tables maps to a manifest row; a placeholder left unfilled blocks the transfer.
- The four fixed strings appear exactly as registered: "split of a known τ_sel", "batch-1 re-decode of a known τ_sel", "batch size 1; registered in v1.2 after K1 fired, on string-identity counts only", "A1 not met; batched decode; descriptive".
- No "PASS" outside case N+; no "no claim was nominated" applied to the batched block 1 (CC-340 ruling 1c); no "test" for the attribution analysis; no "RAGCap-style"; no sentence that a published system was tested, confirmed or overturned.
- No caption text, no host name or address; no p-value other than the registered p̃.
- Holm threshold α_j recomputed by hand from `VER` for each nominated claim and compared with the label.
- The two third-party strings appear verbatim wherever those arms are named: "re-implementation of the LMCap recipe by this study; not the authors' code (no licence); not a statement about the published numbers" and "image-caption-pair prompt format, as used by RAGCap; not RAGCap" (erratum 1, E6).
- Every past-tense procedure sentence is confirmed against its OPS line before transfer, and changed or cut if the step did not happen as written: "Block 1b re-decoded every arm …" (block-1b pull line), "the scoring ran in stages … each stage … ran once" and "its verification stage passed" (the OPS lines after `verify`, `ova`/`close`, `ovb`, `rest`, `posthoc`), "The nomination file was hashed and its sha256 logged before any new OV-dev-B output was scored" (nomination OPS line before the `ovb` line), "D1 passed for all three backbones" (final-pull STEP1B0 hashes), and the block-1b GPU-hours and steps (`job.log` at the pull).

### 6.4 Open for the judge

- **J1 (abstract, introduction, conclusion).** The Vietnamese test registration bars secondaries from the title, abstract and contributions; the attribution registration says nothing about them. Recommended: no development row enters the abstract or contributions; the introduction and conclusion may name the study and its K1 finding in one sentence each, without numbers. Default: the package's placement map (no change there).
- **J2 (citations not in `paperC.bib`).** `[@Sattolo1986]` (Sattolo 1986, Information Processing Letters 22(6)), `[@Holm1979]` (Holm 1979, Scandinavian Journal of Statistics 6(2)) and `[@Schuirmann1987]` (Schuirmann 1987, Journal of Pharmacokinetics and Biopharmaceutics 15(6)) are cited from memory and are **chưa kiểm**; each needs a bib entry checked against the publisher page, or the sentence loses its citation. CC-331 N9: both Li et al. records were checked on Crossref on 2026-11-12 (CC-358); the copy-bound reading sentence cites the TPAMI 2026 paper `[@Li2025UnveilingICL]` (its "short-cut" finding), not the ACL 2024 robustness paper, and the finding is checked against that paper's text at transfer. Sattolo, Schuirmann and Holm were checked on 2026-11-12 (CC-358); their bib entries are added at transfer. `[@Bazi2025RAGCap]` is in the bib; its use here only names the prompt format.
- **J3 (Tier A in part).** The run document makes a cap stop, job stop or freeze inside Tier A a stop before any score, pending a judge line; the registration has no text for that case. The shell only says no output was scored. The paper wording for any later licensed scoring needs the judge's line.
- **J4 (which copy-bound unit decides).** The registration fixes n = 3 as deciding but names no deciding unit between (i) syllables and (ii) words. The package reports both, each with its own reading sentence. Recommended: keep both, never merge; if the two units disagree, print both sentences.
- **J5 (Aya-Vision-8B in the scope sentence).** The registration counts "Aya-Vision's post hoc row"; addendum v1.2 makes the batch-size-1 row the reported one ("batch-1 re-decode of a known τ_sel"). Recommended: count the batch-size-1 row of Table 16, with the flag; the stored batched row stays in Table S22. Also: whether the scope sentence is printed at all when block 2 did not run (count of one backbone). Recommended: print it with the added sentence of §4.9.
- **J6 (the word "test").** K5 drops "test" only when the positive control fails; with block 3 not run, the control was never run. The package uses "attribution analysis" throughout. Recommended: keep that.
- **J7 (fixed-set label from A1-not-met rows).** The ω^U rule would label "every `fix` row of the paper" conditional; the five-set rows are batched (A1 not met), as were the paper's registered `fix` rows. Recommended: print the label in Section 6.10.5 only, and add it to Tables 6 and S1–S4 only after a ruling.
- **J8 (placebo flag).** The registration sends a flagged set to the judge before its rows are used; the package has no sentence for the ruling's outcome by design.
- **J9 (power sentence beside NEGLIGIBLE).** CC-331 (Q5) requires the power statement wherever NEGLIGIBLE is used. The package prints the registered design property (about ±0.3 at the planned standard error; values for m = 1) and no other planning value. Recommended: accept; it states the label's power, not an expected result.
- **J10 (batched against batch-size-1 comparison).** The registration prints batched rows "beside" the batch-size-1 rows; it does not license a difference between them, and CC-340 W7 allows a slice-cluster bootstrap on batched rows only as a labelled post hoc row. The package writes no comparison sentence and no slice-cluster row. Recommended: none in the main text.
- **J11 (copy-bound rows on stored batched decodes).** The scoring run document labels only Aya-Vision-8B's XM-dev500 copy-bound row "A1 not met"; the other rows use stored decodes of earlier registrations, decoded in batches, where A1 was not a registered assumption. The package says in Table 17's caption that the rows bound the stored batched contrast. Recommended: no "A1 not met" label on the stored rows; the caption sentence stands.
- **J12 (nomination table labels).** Table 15 omits the m = 1 labels the nomination file holds, to avoid a second rule on OV-dev-A. Recommended: keep them in the supplement only.
- **J13 (Aya-Vision-8B's earlier OV-dev-B τ_sel).** It is known to the authors from the Flickr30K registration's exploration runs; its stored, batched value enters Table S22 through the `rest` stage. Ruled (CC-358): disclose it as known (Sections 5.7 and 7.5) and print it only in Table S22, labelled "A1 not met; batched decode; descriptive".
- **J14 (block-2 to block-4 text).** If any of blocks 2–4 runs before the freeze, its scoring needs code, a run document and a read, and its paper text needs its own package; this package covers only the not-run sentences.
- **J16 (who reviewed).** The rulings that read the registration, code and run documents (CC-331 to CC-348) were made by AI judge agents, and the coder and writers are AI agents. The paper text above says "reviewed" and "a recorded review" without naming who. ACM requires the research-process use of AI tools to be described in the Methods section; under PI-1110n the PI decides those sentences. Recommended: the PI adds the AI-use description at submission; until then no sentence of this package says or implies that the reviews were human.
- **J17 (paper-text placement of 6.10.2).** The task asked for the batch-size finding as its own subsection; it is 6.10.2 inside the attribution section, with cross-references from 9.1, 9.3 and Box 2. Alternative: a short Section 9.3 paragraph only. Recommended: keep 6.10.2, because the batch-size-1 label of every attribution row depends on it.
- **J15 (glossary clash).** "A1" here is the batch-independence assumption; the paper does not use "A1" for stage-A rows, but the registration does ("stage-1 A1 rows"). Recommended: never write "A1 rows" in the paper.
