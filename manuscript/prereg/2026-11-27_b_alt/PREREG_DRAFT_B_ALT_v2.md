# B-ALT preregistration DRAFT v2 (Paper B, LRE; RQ9 / Objective 3.3): FE-LOCUS. Is the CIDEr-D shift caused by changing the Vietnamese word segmenter carried by a short, reference-derived list of frequent disagreement types, or by the long tail?

Drafted 2026-11-27 by agent b-alt. **Status: DRAFT v2. Not registered. Not runnable.**

**Changes from v1.1 (ruling CC-510, NEXT_ROUND 72, 2026-11-27T12:24:40Z).** The hunk map is in `V1_1_TO_V2.diff`.
- W1: the primary estimand is now κ_head, tested per draw against the band [min, max] of c_ref^B and c_out^B. Floor (v) is added, and so are mutants M9 and M10.
- W2: the English arm is struck.
- W3: the PI gate is stated as the ruling words it.
- W4: full paths and full sha256 values are given.
- Non-blocking items N2–N5 are applied in this file.
- N1 and N6 (corrections to ALTERNATIVES, which stays unchanged as an older file):
  - the English NOT RUN line is `paper.md:444`, not `:294`;
  - ALT-3's expected rubric gain is about +0.8, not +1.3, because its C9 step overlaps the benchmark's A2 item (CC-510 ruling 5).

**PI gate (CC-510 W3, ruling words).** "D1 §9 requires the PI before any further Paper B study if H3 is not SUPPORTED. Before D1's result, this registration is a new Paper B direction item, which the coordinator's reading of PI-1127i does not cover. It is committed only after the PI's yes to the question in CC-510."

**What happens before the registration commit.**
- Nobody computes, prints or opens any quantity defined below.
- That includes the disagreement census of §3.2 and any count over the references.

**What was not read.** No caption, reference or score file was opened to write this draft.

## 0. Sources (read-only)

| item | path (repository-relative unless stated) | sha256 |
|---|---|---|
| Paper B text of record | `paper/rev_2026-11-15/paper.md`, B repo at 13549e5 (copy `~/vsps_ro3/b_now3/`) | `e8d94fbe219efab4fbb09cc92a6e3af6209bba6fb1b13fec02c19b5f3f44d0a9` |
| FE-CERT registration v1.1 | `manuscript/prereg/2026-11-12_b_fecert/B_FECERT_PREREG_v1_1.md` | `736b7e6a8ea2007270a3329db7ad6a09197c4804c9bc3821ea6bd4ceb5a61aa0` |
| FE-CERT code | `scripts/b_fecert/b_fecert.py` | `67e43dea1b37c3bbfaa3fe5081d6f3d36848397451ad0a24d67fa67389b06b59` |
| family code | `scripts/b_fecert/family.py` | `7cb2c69b8b7840388568fd5f9b248e2cf25df28185386be875a65d921a9e4178` |
| CIDEr-D | `scripts/kit_b/protocol_pilot.py` (`Cider`) | `6aee428207a2d1a045cd72d054e26a2e2ac8d9c2e414cb0c161e3b95dffd92bf` |
| stage-1 output (G0 only) | `manuscript/prereg/2026-11-12_b_fecert/results/b_work/DEV.json` | `88ff39aa9552b671a0e439aec961d0fefe02df1f52a2a5df9765a9d8226f7e8d` |
| family | `manuscript/prereg/2026-11-12_b_fecert/results/b_work/FAMILY.json` | `431d92a4a2eaf0516446c9f9aef453ee52d311b6e329d97cd1abb4c4e8017f77` |
| systems | `manuscript/prereg/2026-11-12_b_fecert/results/b_work/SYSTEMS.tsv` | `30ac9555cd6cdc8fd50f47e637e734fac564c692605f590ba213a60a3be6e1a0` |
| D1 registration (neighbour) | `manuscript/prereg/2026-11-27_b_d1/PREREG_DRAFT_B_D1_A3_v3.md` (commit adebac7) | `bf3a55f7641cc91b7ba99b5e4ef9d8623d857a2b594bfb7471636f9cf9f939e9` |

Where the hashes come from:
- paper.md and the D1 file: computed by `sha256sum` on 2026-11-27.
- The other rows: copied in full from D1 v3 §0 and from the FE-CERT result-file hash listing (`b_work/FAMILY.json`, `b_work/SYSTEMS.tsv`).
- At the commit, the coordinator checks every row by `sha256sum`.

## 1. Question and idea provenance

**Question (RQ9).** When the word segmenter changes from RDRSegmenter (`rdr`, the unit of `f0`) to pyvi (`pyvi`), each system comparison's CIDEr-D difference shifts.
- Is that shift removed by pinning the segmentation of a short list of disagreement types, taken from the references alone and covering 80% of disagreement occurrences?
- Or does most of it stay, because CIDEr-D's IDF weights give rare types more than their frequency share?

| observation | file::line |
|---|---|
| the unit moves scores (15.64 points syllable against word); pyvi moves one system's score far less than syllables do (149.12 against 149.79; τ 0.994) | `paper.md:76` |
| RDRSegmenter rewrites tone placement itself (9 of 9 toy strings); pyvi does not (0 of 9) | `paper.md:219`, Table 1 caption |
| breaks grow with a unit's departure from the family (character unit 16 of 72, underthesea 2 of 72) | `paper.md:251`, `:268` |
| the paper gives no account of where breaks come from | `paper.md:412`; BENCH_B C9 row |

Borrowed parts:
- tf-idf weighting (Vedantam et al. 2015);
- a standard front end (Post 2018);
- lists of permissible variants (Bhogale et al., ICASSP 2026; Aepli et al., WMT 2023).

## 2. Numbers already printed or seen (POST HOC; no rule below is decided by them)

On D (1,101 development comparisons) unless stated:
- **Everything in D1 prereg v3 §2:**
  - 909 / 59 / 2 / 133 over F_dev; 908 / 62 / 131 over F; 936 significant under `f0`; CHANGED 27 and 28;
  - point-sign flips 58 and 65;
  - held-out breaks 1 of 909, and 2 of 72 in V (1 of 68 development);
  - NC 6 of 915, all among 54 near-margin;
  - AUC 0.8012 and 0.9546;
  - the Table 7 rows;
  - the per-level breaking counts: D over F_dev units `syl` 654, `rdr` 573, `pyvi` 525; tone `tw` 575, `tm` 588, `tf` 589; punctuation `pk` 604, `pf` 617, `pa` 531; case `cf` 850, `ck` 902; and the same over F.
- **From `paper.md:76`:** 149.79 (`rdr`), 165.43 (`syl`), 149.12 (`pyvi`), τ 0.969 and 0.994, on one system (POST HOC).
- **Toy strings:** tone spellings equal under `rdr` 9 of 9, `uts` 9 of 9, `pyvi` 0 of 9.
- **Character unit:** 16 breaks and 3 reversals of 72; 893 CERTIFIED and CHANGED 53 of 946 with `chr` added.
- **Not seen:**
  - any per-type disagreement count;
  - any `rdr`→`pyvi` shift on a comparison. These shifts are differences of class statistics already stored in `DEV.json` (the `rdr.ℓ` and `pyvi.ℓ` classes). The drafter did not open them. D1's S2 reads the same class statistics, so if D1 runs first, those values exist and are added here at the commit. Floor (iv) can be read from `DEV.json`; it is therefore checked on the half-B re-score only, never from the stored file;
  - any pinned score;
  - any quantity of §4.
- **D1 outputs.** If D1's `RESULT_D1.json` is pinned before this study's S2, its labels and counts are added to this list at the commit, and no rule below changes. This study never opens `PER_IMAGE_D1.npz`.

## 3. Definitions (exact)

### 3.1 Members and pairs

- G_w is the 36 word-unit members of F_dev (`rdr` and `pyvi`, each × T{`tw`,`tm`,`tf`} × P{`pk`,`pf`,`pa`} × C{`cf`,`ck`}), built with `family.py` unchanged.
- For each level triple ℓ = (T, P, C), r_ℓ = `rdr.ℓ` and p_ℓ = `pyvi.ℓ`. There are 18 pairs, and r at ℓ = (`tw`,`pk`,`cf`) is `f0`.
- s_{x,i,f} is the per-image CIDEr-D of file x on image i under member f, with document frequencies from the references under f (FE-CERT scorer, unchanged).
- For comparison c = (a, b): d_{c,i,f} = s_{a,i,f} − s_{b,i,f}, and D_{c,f} is its mean over the 558 images.

### 3.2 Image split and disagreement census (half A references only)

0. **Split (fixed now; CC-510 N4).** `ids = sorted(ids)`; `perm = numpy.random.default_rng(20261127).permutation(558)`; half A = `[ids[k] for k in perm[:279]]`; half B = the rest. The census and the dictionary use **half A's references only**. Every estimand of §3.4 uses **half B only**. The pin list is therefore tested on images whose references never shaped it.
1. Apply `rdr.tw.pk.cf` and `pyvi.tw.pk.cf` to each half-A reference (279 × 5 = 1,395 strings).
2. **Syllable alignment.** Split every token at `_` and spaces into syllables. Map each syllable to its key: NFC, lower case, and the tone mark moved by the `tm` rule. A string is aligned if the two key sequences are equal.
   - Unaligned strings are counted and left out of the census.
   - Precondition: unaligned ≤ 0.5% of strings, otherwise FAULT.
3. **Disagreement span.** A span is a maximal run of syllables [i, j) whose two ends are token boundaries under both segmenters, and inside which the two boundary sets differ. Its **type** is the space-joined key sequence of the run.
4. **Ranking.** Count each type's occurrences over the aligned references. Rank by count, descending; break ties by Unicode code-point order of the type.
5. **Π_head** is the shortest prefix of the ranking whose cumulative count is at least 0.80 of all occurrences. Its realised coverage is c_Π ≥ 0.80. **Π_all** is every type.
6. **Dictionary.** For each type in Π, the pattern is its modal `rdr` boundary pattern over its reference occurrences. Ties go to the pattern with fewer tokens, then to the lexicographically smallest boundary vector.
7. **Provenance.** The census function takes only the reference file path. A self-test asserts that it is never passed an output file (§5 mutant M1).

### 3.3 Pinned members

- For a member m ∈ G_w and a list Π, the pinned member m^Π runs m's pipeline unchanged, then applies one post-step to the token sequence of each string, outputs and references alike.
  - It scans the key sequence left to right, longest match first, for occurrences of Π types.
  - At each occurrence it sets token boundaries at both ends and inside, following the dictionary pattern.
  - Characters are kept as m wrote them. Only the boundaries move.
  - Strings that are unaligned under m are left unchanged.
- The pin applies the same dictionary to `rdr` and `pyvi` members. It is a scorer-agnostic normal form for those types.

### 3.4 Estimands

- All D below are means over the **279 half-B images**. Document frequencies stay those of the scorer, unchanged: the full reference list under each member, pinned or not.
- IDF uses the references of all 558 images, half A included. That is the scorer's constant, not a leak of the pin list (CC-510 N5).
- Shift: δ_{c,ℓ} = D_{c,p_ℓ} − D_{c,r_ℓ}.
- Pinned shift: δ^Π_{c,ℓ} = D_{c,p_ℓ^Π} − D_{c,r_ℓ^Π}.
- Sign: σ_{c,ℓ} = sign(δ_{c,ℓ}) on the full half B, held fixed across resamples, with zero for an exact 0. This keeps the estimator linear and avoids the upward bias of |·| under resampling.
- ρ_head = 1 − Σ σ δ^{Π_head} / Σ σ δ, summed over the 1,101 × 18 units (c, ℓ). ρ_all is the same with Π_all.
- **Primary (CC-510 W1):**
  - κ_head = ρ_head / ρ_all = Σ σ (δ − δ^{Π_head}) / Σ σ (δ − δ^{Π_all}).
  - Why the ratio: two parts of δ cannot be removed by any boundary pin.
    - RDRSegmenter rewrites tone placement itself after the T step (`family.py` applies T before the segmenter; `paper.md:219`).
    - Some disagreement types occur only in outputs.
  - Both parts would lower ρ_head with no IDF effect. κ_head keeps only the boundary-removable part.
  - κ_head can fall outside [0, 1], because CIDEr-D is not additive over types: the length penalty works on token counts, and n-grams cross span ends. It is printed as computed.
- **Proportional reference values:**
  - c_ref^B: the share of half-B reference occurrences of Π_all types whose type is in Π_head.
  - c_out^B: the same share over the half-B outputs of the 75 files. It is counted at S2, after `CENSUS_ALT.json` is pinned, with the §3.2 alignment and span rules applied to output strings.
  - Both are recomputed in every bootstrap draw from image-level counts, with the same W_B: c = Σ_i w_i n_head,i / Σ_i w_i n_all,i.
- Interval: W_B = `boot_W(279, seed 20261128)`, B = 10,000, over half-B images. G0 alone uses the FE-CERT draws on all 558.
  - In each draw, every numerator and denominator is recomputed from `W_B @ d / n`, and c_ref^B and c_out^B from the weighted counts.
  - Per draw: Δ_lo = κ_head − min(c_ref^B, c_out^B) and Δ_hi = κ_head − max(c_ref^B, c_out^B).
  - L(·) and U(·) are the 2.5th and 97.5th percentiles over the draws.
- Units share files and images, so the interval is **nominal**.

## 4. Hypotheses and rules (fixed here before any quantity exists)

**Floor (NOT_EVALUABLE),** checked in this order:
- (i) a G0 FAULT;
- (ii) unaligned > 0.5% (FAULT);
- (iii) fewer than 30 disagreement types in the half-A census;
- (iv) on half B, Σ|δ| < 0.01 · Σ|D_{c,r_ℓ}|, meaning pyvi barely moves the comparisons;
- (v) checked after (iv): L(ρ_all) < 0.20, meaning the boundary-removable part is too small to split.

**What the construction implies (stated before any number).**
- Under a proportional null, where every disagreement occurrence moves the shift equally, κ_head lies near the occurrence coverage of Π_head among the removable types. That coverage is about 0.80 by construction.
- The proportional value is not known in advance, because references and outputs may differ. So the null is a band, [min, max] of c_ref^B and c_out^B, recomputed in each draw.
- The 0.50 bar is a secondary, practical row (H-L2).

**H-L1 (primary): IDF weighting of the boundary-removable shift, against the proportional band.**
1. U(Δ_lo) < 0: **TAIL-WEIGHTED**. In the boundary-removable part of the shift, the frequent types carry less than their share of occurrences, so rarer types carry more.
2. L(Δ_hi) > 0: **HEAD-WEIGHTED**.
3. Otherwise: **PROPORTIONAL**.

No outcome is predicted. The tf-idf argument points to TAIL-WEIGHTED. The concentration of frequent compounds in short captions points the other way.

**H-L2 (secondary, registered, its own label): is the list a practical normal form?**
1. L(ρ_head) > 0.50 on half B: **PRACTICAL**. A list built on other images' references removes more than half of the shift.
2. U(ρ_head) < 0.50: **NOT PRACTICAL**.
3. Otherwise: **INCONCLUSIVE**.

- H-L2 stays on ρ_head: the practical question is about the whole shift (CC-510 W1).
- H-L1 and H-L2 are not combined, and each is printed with "nominal".
- The resource claim (§8) needs PRACTICAL. Because the list was built on half A and tested on half B, PRACTICAL is an out-of-sample result, not in-sample coverage.

**DESCRIPTIVE rows (no label):**
- ρ_head and ρ_all with their intervals; c_ref^B and c_out^B. The remainder 1 − ρ_all is split by T level: the `tw` pairs against the `tm`/`tf` pairs, which bounds the part of RDRSegmenter's own tone rewriting.
- The occurrences in outputs of types outside Π_all (output-only disagreement).
- FRAGILE over G_w, raw against pinned, with CHANGED defined against `f0` and `f0^Π` respectively.
- How far the pin moves the reference member: Σ|D_{c,r^Π} − D_{c,r}| / Σ|D_{c,r}|.
- |Π_head|, c_Π (half A), c_Π^B, and the 20 most frequent types. The types are printed only if OPEN_QUESTIONS Q4 is answered yes; otherwise counts only.

## 4b. English arm: not run (CC-510 W2)

E0 fails on the record before any output file is opened.
- uv231 is UIT-ViIC test, which CC-505 W5 removed from Paper B as a one-look set.
- cv295 is part of Paper A's A-T3 images. A fixed rule excludes it from Paper A's own development checks (CC-266 ruling 2) and from Paper C's KT-C (PORTFOLIO_3Y l.193).
- Paper A's registered English-arm claims rest on both sets.

B's English control stays NOT RUN (paper.md:444).

**English control: NOT RUN, no admissible stored set.**

## 5. Stages, gates and order

**Host (CC-510 ruling 6).** The D1 rented host, used only after D1's `RESULT_D1.json` is pinned on the LOG. Not the PI's PC, not the laptop; the laptop writes files only. This study has its own S0 judge code read, its own `env_check`, and **its own hard stop at 8 CPU-h**, separate from D1's 8 CPU-h.

**S0, on the host, before any data:**
- **Code read** by a judge.
- **Self-tests** on invented-syllable stub data:
  - the split: half sizes 279 and 279, disjoint, reproducible from the seed; the census reads no half-B id (mutant M8: the census reads all 558);
  - head-only world: ρ_head = κ_head = 1 within 1e-9;
  - tail-only world: ρ_head = 0;
  - a known mixed world;
  - with Π empty, δ^Π = δ exactly;
  - adding a constant non-removable shift (a tone-rewrite or output-only component planted on every unit) leaves κ_head unchanged and lowers ρ_head;
  - per-draw recomputation of c_ref^B and c_out^B from weighted image counts.
  - the pin is idempotent;
  - census tie-breaks;
  - the alignment counter;
  - the label boundaries: Δ_lo and Δ_hi at 0, ρ_head at 0.50, and L(ρ_all) at 0.20, each both > and <.
- **Mutants to kill:**
  - M1: the census is fed an output file;
  - M2: the pin is applied to `pyvi` only;
  - M3: T/P/C levels are mismatched in a pair;
  - M4: σ is recomputed per draw;
  - M5: W is reseeded;
  - M6: ≥ is used in place of > at a label boundary;
  - M7: the tone key is not applied in alignment;
  - M8: the census uses half-B references, or the estimands use half-A images;
  - M9: the H-L1 label read from ρ_head instead of κ_head;
  - M10: c_ref^B or c_out^B held at its full-sample value in every draw.
- `env_check` passes in the FE-CERT segmenter environment: VnCoreNLP 1.2 jar sha `9e2811cd…`, pyvi 0.1.1.

**S1, on the host.**
- Census: Π_head, Π_all and the dictionary go into `CENSUS_ALT.json`. Pin it by sha on the LOG before S2.
- Re-score the 75 files under the 36 G_w members and their 36 pinned versions. Per-image CIDEr-D only, written to `PER_IMAGE_ALT.npz` with mode 444. It is never committed and is pinned by sha.

**G0, the reproduction gate.** For each D comparison and each G_w class, the D, L, U and sd recomputed from the raw matrix with W must equal `DEV.json` within 1e-6. Any difference is a **FAULT**: stop, write a judge line, and compute no ALT quantity.

**S2, on the host.** H-L1, H-L2 and the DESCRIPTIVE rows go into `RESULT_ALT.json`, computed once, then pinned.
- The result note is written by an agent who is neither the coder nor the text writer.
- No stage runs twice without a judge line.

## 6. Data and scope

- D only: the 73 own KTVIC-test files plus the two baseline files, the 2,790 spent references. Label DEVELOPMENT, plus REGISTERED PREDICTION for H-L1 and H-L2.
- Not used:
  - the first-look pool;
  - underthesea (its re-score is licensed to D1 only);
  - the syllable and character units;
  - any test split;
  - any label, pair or human-arm file;
  - D1's per-image matrix.
- No decoding. GPU 0.
- The re-score of spent references is licensed for this study only after its registration commit (the D1 precedent, CC-505 ruling 7).
- No caption text is printed. Type strings are printed only under Q4.

## 7. Outcome map (what the paper may say; every interval is "nominal")

| outcome | allowed sentence (template) | not allowed |
|---|---|---|
| H-L1 TAIL-WEIGHTED | "In the boundary-removable part of the CIDEr-D shift between RDRSegmenter and pyvi, a list of the most frequent disagreement types, built from the references of half of the images, removed κ_head [L, U] of that part on the other half, less than their share of disagreement occurrences there; rarer types carry more of the boundary-removable part (REGISTERED, DEVELOPMENT; nominal)." | "certificates are necessary" in general; causal IDF language beyond the label; any statement about the non-removable part beyond the ρ_all row |
| H-L1 HEAD-WEIGHTED / PROPORTIONAL | the same template with "more than" or "in proportion to" their share | |
| H-L2 PRACTICAL | "… removed more than half of the whole shift (ρ_head) on images whose references were not used to build it. The list is released as a normal form, as type strings if OQ4 is answered yes, otherwise as counts and census code." | "segmentation instability is solved"; any claim for other segmenters, metrics or data |
| H-L2 NOT PRACTICAL / INCONCLUSIVE | the estimate and interval; no release sentence | |
| NOT_EVALUABLE | the failing floor and its count | |

Every label is printed whichever way it falls. None of them changes a FE-CERT label, F, or a D1 label.

No FE-LOCUS row, including the T-level split of 1 − ρ_all, is used to qualify D1's H3 label. H3 sentences come from D1 alone (CC-510 N3).

## 8. After the result

- **H-L2 PRACTICAL.** The pin list is released, as types or as counts only (Q4), together with the census code. That release is the C8 resource claim.
- **Any H-L1 label.** One analysis paragraph (C9) goes in, whichever way it falls.
- **H-L2 not PRACTICAL.** The resource claim is dropped.
- **No further B study follows** from any label without the PI.

## 9. Not done, and why

- underthesea and other segmenters: underthesea is held to D1, and the unseen segmenters belong to N2-R (ALTERNATIVES §2.2).
- Syllable against word: that difference is the unit choice itself, not a set of loci. Pinning would turn one unit into the other.
- BLEU-4 and ROUGE-L: CIDEr-D is the only metric with a verdict in FE-CERT.
- A per-type Shapley split: left out. Its cost grows with |Π|, and the head/tail question does not need it.
- A full-text read of OIWER and of Aepli et al.: owed before any claim sentence (REVIEW90 K3). It is not needed for the rules.
