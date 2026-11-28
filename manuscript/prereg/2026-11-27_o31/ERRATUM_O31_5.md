# ERRATUM O31-5 to PREREG_DRAFT_O31_v3.md (5b33480b), ERRATUM_O31_1.md (91108b81), ERRATUM_O31_2.md (817eac8f), ERRATUM_O31_3.md (979486bf), COMPUTE_PLAN_O31_v3.md (7557ca3b) and ERRATUM_O31_4.md (0a0bd365)

**Status.** Read and amended by rulings CC-525 and CC-525r2 (2026-11-28) and split by rulings CC-525b and CC-525r2a (2026-11-28), and amended as the second part by ruling CC-526 (2026-11-28). This file is the second part of the amendment; the first is ERRATUM_O31_4 (0a0bd365), committed in the run repository at 7137f94 on 2026-11-28T06:51:22Z. This file is committed before the first G3 output. Nothing in it has run.

**State of the study when this is committed.** At the commit of ERRATUM_O31_4 (2026-11-28T06:51:22Z) no output of P0r, P1, G1 or G2 existed and of the §3.5 pass only the laptop step `kv` had run. At the commit of this erratum: P0r: not run; §3.5 pass: the laptop step `kv` run, launched 2026-11-28T05:18:19Z, LOG OPS-1128ca-o31-kv-w2, the feats step and the pass step not run; G1: not run; G2: not run; P1: not run; no G3 output exists.

**What reads what.** Some rules of this erratum take outputs of registered steps as inputs, as the registration's own rules do. Several read P1's `k0.json`, directly or through `ops5.json` of ERRATUM_O31_4, among them OP\*'s family set and thresholds (E-B2, E-B5, M1), P_floor (M1), OP\*'s store (M2), the supervision side of the transfer ratio (E-B3), and the five points, the new students and T-4 (E-B3, through `ops5.json` only); `k0.json` is built from the G1 records, the G2 probes and the §3.5 (a) exclusions. G-1 uses the tier-2 id list after the registered §3.5 removals and checks outside image sets, on the laptop, against the KV-4,224 W25 descriptors of the §3.5 pass. No constant, threshold, seed or choice in this erratum is set from any output of P0r, the §3.5 pass, G1, G2 or P1. Every line of this file outside the edits that rulings CC-525b, CC-525r2a and CC-526 made or approved is byte-identical to the file that ruling CC-525r2 fixed (sha256 0bebaa81feb61ebf45a443bcad073348a8a6cc76fbb1b1b0cb072c2be1e14faa), which rulings CC-525r2 and CC-525r2a name and which existed before the commit of ERRATUM_O31_4 (2026-11-28T06:51:22Z), that is, before any output of P0r, P1, G1 or G2 existed and before any output of the §3.5 pass other than the laptop step `kv`'s KV-4,224 ids and descriptors (which hold no grid-point value). Those edits state the facts of the split, move rules into ERRATUM_O31_4, point to it, align this text with it or restore wording of that file (E-B3); ruling CC-526 also adds one fail-closed trigger to the saved-source rules (E-B4) and states which text governs (Sources). None of them sets a constant, threshold or seed. No rule reads P0r's preview. G1 and G2 need no change.

**When it must be committed.** Before the first G3 output. The rule that picks the two extra operating points, the reporting row on the position of OP\* (R-c), and the form of the five-point test T-4 with its place in a family needed an earlier deadline, because every `k0.json`, P0r's preview included, holds the R_sup values that rule ranks and on which T-4's power depends; rulings CC-525b and CC-525r2a therefore register them in ERRATUM_O31_4 (0a0bd365), the first part of this split amendment. E-D.3 gives the deadline of each item.

**What it does.** It adds registered analyses, comparison systems and scope statements. It changes no registered element; E-D.1 lists them. Every addition is labelled either **tertiary** (a test in the new family T, with its own multiplicity correction) or **descriptive** (reported with intervals, no verdict). No addition changes a verdict of H1 to H5, of K0 or of any stop rule. No addition is a second chance for a registered hypothesis.

**Why.** Two reviews of the registration found that a reviewer could attack the paper on eighteen points:
- an adversarial design review (file `FINDINGS.tsv`, findings F01 to F18, and `PRIOR_WORK_CHECK.tsv`, 28 methods a reviewer may ask for);
- full-text dissections of the seven closest prior works (`MAP.tsv`, 23 break points, gap tags G1 to G8).
The dissections also correct the group's prior-art table. Two corrections matter most. First, the claimed novelty "(ii) transfer slopes across operating points" does not survive as worded. Second, the three-state verdict is partly taken. Sections E-A.3 and `PRIOR_ART_O31_SUMMARY_v3.md` carry the corrections.

**Sources.** Every number this erratum takes from the seven dissected works was checked against their saved full text (the HTML and PDF files listed in the dissections' `fetch_log.tsv`). Settings of VCD, DeCo, the EFUF code and the SENTINEL release that were not read verbatim in their primary source are marked "not read verbatim in the primary source" and listed in `OPEN_FOR_JUDGE.txt`. Every item of `OPEN_FOR_JUDGE.txt` is ruled in CC-525 and, under the split, in CC-525b, CC-525r2a and CC-526. Where `OPEN_FOR_JUDGE.txt`, `CODE_NEEDS.tsv`, `COMPUTE_ADDENDUM.tsv` or a ruling differs from ERRATUM_O31_4 or from this erratum as committed, the committed errata govern, and ERRATUM_O31_4 governs over this erratum.

---

## Terms used in this erratum

- **S0**: the base model, Qwen2.5-VL-7B-Instruct, decoding zero-shot with the FAIR detailed prompt. **S1**: the FAIR recipe retrained on the O31 pool. **S2**: the O31 student, trained at the operating point OP\*. These three are as in prereg §2.
- **Operating point**: one setting of the O31 verifier, that is, a pair (τ_acc, τ_rej) with a set of verifier families. The registered grid has 30 points (prereg §4.3).
  - **OP\*** is the point K0 chooses.
  - **OP_mid** is the point whose supervision recall is nearest the middle of the S1-to-OP\* range (prereg §4.5; ERRATUM_O31_1 E7).
  - **OP_strict** is FAIR's own verifier rule, which is S1's data.
- **Supervision recall R_sup** and **precision P_sup**: K0's numbers for a training store, at the `sft_caption` stage, on KTVIC-train references. R_sup is a per-image mean (macro average) over the 113-noun CHAIR-vi lexicon. P_sup is a ratio of sums (`scripts/o31/src/o31/gate.py` header).
- **R** (object recall) and **h** (hallucinated objects per caption): the registered outcome measures of §5. R is a ratio of sums over images. h is the count of mentioned objects absent from the gold, divided by the number of captions.
- **CMP** (count-matched object precision): the measure defined in §5. On each image, two systems are cut to the same number k_i of distinct mentioned classes, each keeping its first k_i classes in order of first mention, and precision is computed over the kept classes.
- **ρ** and **D**: the H1 and H2 statistics of §6.1.
- **Tier 1** is development: KTVIC test 558 and UIT-ViIC test 231, both already spent, in a development role. **Tier 2** is the development-confirm rehearsal on the Karpathy test 5,000. **Tier 3** is the one-look test (prereg §3.3, §3.4, §7).
- **Steps**, in registered order:
  - G1 makes the stage-1 records and Vintern probes for 69 images.
  - G2 runs the InternVL3 probes over the training pool.
  - P1 runs K0 on the full grid.
  - G3 trains S1, S2 at OP\* and S2 at OP_mid, then decodes them on tier 1.
  - G4 runs the ablations A-2 to A-4.
  - G7 trains seeds 43 and 44.
  - T2 is the tier-2 step and T3 the tier-3 step (COMPUTE_PLAN §1).
- **V-COCO**: the registered verifier yardstick (§3.2). It holds one entity proposition per COCO-80 class that S0's caption mentions, scored against COCO-2014 instance gold.
  - **RT** (retention) is P(SUPPORTED | class present).
  - **FA** (false accept) is P(SUPPORTED | class absent).
  - **DR strict** (strict detection recall) is P(REJECTED | class absent).
- **Family T**: the new tertiary family of this erratum (E-B1 and E-B3). It holds four members, with Holm's correction applied inside T only.
- **Descriptive**: reported with point estimates and 95 % intervals. There is no pass or fail rule, and a descriptive row never changes a registered verdict.

---

## E-A. Scope of the claims

### E-A.1 What the paper claims
1. **The registered claims, unchanged.** These are H1 and H2 (headline), H3, H4 and H5, with the verdict labels of §6.3, read on the sets and at the tiers the registration names.
2. **Object existence only.** The outcome measures concern whether an object of one of the COCO-80 classes is present:
   - on instance gold for tier 2 and tier 3, and for UIT-ViIC on the gold that §3.3 registers for it ("COCO instances ∪ Vietnamese refs"; added UIT-ViIC rows also on instances only, G-2);
   - the 113 nouns of the CHAIR-vi lexicon on reference-derived gold, for KTVIC.
   "Coverage" in the paper means this object recall. It does not mean detail, completeness or informativeness in general.
3. **Counts.** Counts are claimed only if module M4 is kept, and then only for the count claims M4 defines (a numeral attached to a COCO-80 mention, scored against instance counts).
4. **The verifier.** Its retention and false-accept rates are measured on COCO-80 entity propositions against instance gold, and in English on M-HalDetect span labels (§3.2). With E-B5, they are set beside published verifier rules on identical propositions.

### E-A.2 What the paper does not claim
1. **Other claim types.** It makes no claim about attributes, actions, spatial relations or other non-object content. The O31 verifier loosens acceptance for every proposition type (ERRATUM_O31_1 E4, step 3: entity, attribute, action and counting), so errors of these types may rise without showing in any registered measure. The paper says so in its limitations. Module M4(b) measures how large this blind spot is on human labels.
2. **Vietnamese retention by proposition type.** There is none: no Vietnamese per-proposition human labels exist, and ViHal stays held (§3.2, Q3).
3. **The English arm.** It is not a replication. It is the same Vietnamese-trained adapter, decoded with an English prompt (§6.2 H5; ERRATUM_O31_2 E6).
4. **Other student architectures.** There is no claim beyond Qwen2.5-VL-7B unless module M2 is kept. Even then the claim is descriptive.
5. **The pre-training gate.** The registered pre-SFT gate (K0) is part of the method and of the research process. It is not a contribution (finding F04 (c)).
6. **The three-state verdict and the cross-family rule.** Neither is new. Both are design details (E-A.3).
7. **The two COCO tiers.** If §3.4 ends in branch 1, tier 2 (the Karpathy test) and tier 3 (KV-4,224, which is Karpathy validation minus exclusions) are drawn from the same COCO val2014 pool. Tier 3 adds a fixed procedure and a single look. It does not add independence of distribution (F16). The paper states this in one sentence.

### E-A.3 What remains new (the corrected novelty statement, for the paper and the cover letter)

> Earlier work has already shown three things. First, the operating point of a training-data verifier changes the fine-tuned model: HalluciDoctor (App. B.2, Table 5) fine-tunes after each of five consistency thresholds, from 0.1 to 0.9, reads the students on CHAIR and MME, and picks the threshold on those benchmarks; SENTINEL (Tables 8 and 9) shows the same under preference optimisation. Second, the annotation source of the reward changes a student's object coverage under reinforcement learning (Beyond Saying Less, Table 2: on DOPA labels, Cover 52.0 when trained with MS COCO annotations and 69.6 with the denser DOPA annotations, while on MS COCO labels the order is reversed, 78.8 against 73.7), and reward weights give operating points between hallucination and omission (ClaimDiff-RL, Table 3). Third, a verifier can leave an uncertain middle band unused, as EFUF does with its two CLIP thresholds and SENTINEL with detector disagreement. We claim none of these. For supervised fine-tuning on verified propositions, and for object existence only, this study contributes three measurements. (a) The training-data verifier's retention of true objects and its false-accept rate, measured against human instance gold before any training and set beside published verifier rules on identical propositions. (b) The student's object recall and hallucinated-object count at five verifier operating points that a fixed rule chose before training, each beside the supervision recall measured for it before training, with a registered test of monotone ordering on the 5,000-image rehearsal set. (c) A test of whether the student lies above the base model's own truncation frontier: at a matched number of mentioned objects, against the base model's own captions and length-controlled versions of them, with the count-matched object precision of Objective 3.2 (the companion study's instrument, cited) used as an instrument only, with no claim about the instrument and no raw-versus-matched contrast (§5). The study's conditions are Vietnamese captions, no new human labels, no preference or reinforcement learning, one 24 GB GPU and no verifier at inference. They describe its setting and are not claimed as novelty on their own. Claim (b) is made only if T-4 PASSes. Claim (c) is made only in the form that each PASSing member supports (T-1: higher count-matched precision than S0's first-mentioned objects; T-2: dominance over S0-trunc; T-3: dominance over S0-two), and every member that FAILs, is NOT_IDENTIFIED or is NOT RUN is named in the same paragraph. If no member of (b) or (c) PASSes, the paper reports the failures and claims only (a) and the registered results of H1 to H5.

This paragraph replaces the "NEW" row of `PRIOR_ART_O31_SUMMARY_v2.md`. It is provisional until the nine works marked "not read" in `PRIOR_ART_O31_v3.tsv` (Less is More, MOCHa, VFC, LURE, OPA-DPO, RLAIF-V, HALVA, Nullu, MHR) are read in full before the paper draft; a work that already reports (a), (b) or (c) sends the line to a K5 read. Its sources are verified as follows:
- HalluciDoctor App. B.2 Table 5: thresholds 0.1, 0.3, 0.5, 0.7 and 0.9 with CHAIR 19.9, 16.1, 13.8, 14.2 and 13.6 and MME 1153.2, 1178.6, 1207.2, 1012.9 and 739.1 (the dissection quoted only three of the five);
- SENTINEL App. B.3 to B.4, Tables 8 and 9, and App. E Table 19 (Qwen2.5-VL-7B-Instruct: Object HalBench Resp. 15.0 → 4.7, Ment. 9.2 → 2.8);
- Beyond Saying Less Table 2 (Qwen2.5-VL baseline vs SCAPO with MS COCO and with DOPA annotations);
- ClaimDiff-RL Table 3, which has three severity-weight settings, with MEDC on a 3K validation set and Hall and Miss on the 160-image diagnostic;
- EFUF App. A.1 (T₀ = 32, T₁ = 23, T₂ = 27.5).

### E-A.4 Statements the method and limitation sections must carry (text only, no new run)
1. **Verified self-distillation (F07 (c)).** The generator of the stage-1 propositions and the student are the same model, Qwen2.5-VL-7B-Instruct, so S1 and S2 are verified self-distillation.
2. **Verifier lineage (F07).** Both verifier families descend from InternVL.
   - Vintern-1B-v3_5 names InternVL2.5-1B as its base (its model card). That model is an InternViT encoder with a Qwen2.5-0.5B language model; the language model was checked only in a secondary source.
   - InternVL3-8B pairs an InternViT encoder with a Qwen2.5-7B language model (registration §10; the encoder was not checked in this erratum).
   - The verifiers therefore share an encoder family and a language-model family with each other, and the language-model family with the student. Before any paper text states this, each fact is read from the pinned snapshots' `config.json` files and model cards.
3. **Selector scores (ERRATUM_O31_1 E6; F09).** S2's selection order still uses FAIR's recorded support and contradiction scores. Only the verdicts change between arms.
4. **Outcome gold is human.** No language model judges any outcome. All outcome gold is human: COCO instance annotations, KTVIC and UIT-ViIC references, and M-HalDetect span labels (F12).
5. **Cost table (F14).** The method section carries one table, filled from the run records under E-B8 R-f.
6. **The two COCO tiers** (E-A.2 item 7).

---

## E-B. Core additions

### General rules for every E-B item

- **G-1 Sets.**
  - Tier 1 is KTVIC test 558 and UIT-ViIC test 231, in their development roles (§3.3), each with exactly the image-id list of the registered tier-1 rows.
  - Tier 2 is the Karpathy test 5,000, in its development-confirm role (§3.4). Every added tier-2 row decodes and scores exactly the image-id list of the registered tier-2 rows (after every removal that §3.4 and §3.5 register; its sha recorded before the first T2 decode) and no other Karpathy-test image. Where a registered precondition of an added row removes images from a tier-1 or tier-2 list (PS-3 of E-B4), that row scores the rest of that list, with every system in the row re-scored on it; no image outside these lists is added.
  - No addition uses the tier-3 set in any role, except the tier-3 row of E-B8 R-a, which is computed at the registered tier-3 look from its registered outputs, with no new decode or probe.
  - No addition places any tier-3 image, gold file or descriptor, or anything derived from them, on the PI's PC before the registered tier-3 step (ERRATUM_O31_2 E1 O-H8).
  - Any image set from outside the registration that may contain COCO val2014 images (Visual Genome images in E-B4, MME images in M3) is checked on the laptop before any of its bytes goes to the PC, by exact sha and the committed W25 rule against KV-4,224's W25 descriptors (as ERRATUM_O31_2 E2 uses them) and, if §3.4 ends in branch 2, against AMBER-1,004 under that branch's amendment. A hit never goes to the PC. Visual Genome images never go to the PC at all (PS-3).
- **G-2 Gold.**
  - Added rows on UIT-ViIC and at tier 2 use COCO-2014 instance gold for the 80 classes (the E11 form). An added UIT-ViIC row with gold = instances ∪ references is labelled as such. G-2 governs the added rows only: every registered row and the stop rule K1 keep the gold that the registration gives them (§3.2, §3.3, ERRATUM_O31_1 E11); G-2 changes none of them.
  - KTVIC rows use the 113-noun CHAIR-vi lexicon on references.
  - KTVIC and COCO numbers are never pooled (§5).
- **G-3 Decoding.**
  - Every new decode of a Qwen2.5-VL-7B system is greedy, with at most 160 new tokens (the `decode.py` setting).
  - It loads the bf16 base (E5).
  - It uses the batch rule of the registered decodes (the Q13 parity rule), unless the item says batch 1.
- **G-4 Statistics.**
  - Intervals use the paired image bootstrap with B = 10,000 and seed 20261127, the shared index matrix, and the CI and undefined-replicate rules of ERRATUM_O31_1 E9.
  - Where a system has three seeds, each image's counts are averaged over the seeds before resampling (§6.3).
  - S0 has a single decode. It is paired with each seed j of a student as in E12: the counts are computed per pair and then averaged over the three pairs.
  - One-sided p-values have the §6.3 form, p = (1 + #{b on the null side}) / (1 + B).
- **G-5 Gating and caps.**
  - Every new GPU job runs after the G3 read and only if K1 has not fired. The one exception is G3v (next bullet), the job of a registered tier-1 row.
  - Rows that need no new GPU job are computed from the decodes and probes that exist, also when K1 has fired: E-B1 (a) and (b), E-B2 at tier 1, E-B7 and E-B8. The registered tier-1 V-COCO probes (§7 tier 1: Vintern and InternVL3 Q⁺ on the V-COCO propositions of S0's G3 decode of UIT-ViIC test 231, that is, P-a) run as their own job G3v right after the G3 decodes, whatever K1 shows: planned 0.12 GPU-hours, cap 1 h. E-B2's tier-1 row and E-B5's P-a rows read G3v's tables. A K1 stop therefore still reports the truncation controls and the inference-time filter at tier 1.
  - Every tier-2 row runs in the T2 period, after the tier-1 freeze commit, as its own job with its own `launch.json`. No added job runs inside the launch of a registered job (G3, G4, G7, T2, T2v), so no added hour counts against a registered cap. Added tier-2 jobs run whatever K2 shows, and nothing they produce enters P(PASS).
  - Every new job's cap is ceil(1.3 × its planned GPU-hours) as listed in `COMPUTE_ADDENDUM.tsv` (for G3v, in the bullet above), counted as wall time from its own `launch.json` (ERRATUM_O31_2 E7). K4 applies to that job alone: a K4 stop of an added job makes its rows NOT RUN and stops no registered step. In `COMPUTE_ADDENDUM.tsv`, "within T2" means in the T2 period and "with A-3 in G4" means right after the G4 job, each as its own job under this rule; where that file and this erratum differ, this erratum governs.
  - Every new job runs on the PI's PC under O-H1 to O-H8.
- **G-6 Reporting.**
  - Every row is reported whatever its result, beside the registered rows and with its label.
  - K6 applies: no text may hide a failed row or call a development result confirmed.
  - Caption text is never printed or committed (§3.5).
  - No added row (E-B or E-C) is cited in the title, abstract or conclusion as support for a claim whose registered hypothesis (H1 to H5) FAILed, was UNDERPOWERED or NOT_IDENTIFIED, or did not run; such a row is reported only beside that verdict. No added row changes, qualifies or replaces a registered verdict label; the label is printed as computed. In particular, unless H4 PASSes, no E-B5 row is described in the title, abstract or conclusion as favouring VR-O31 over VR-FAIR.

---

### E-B1. Length and truncation controls (finding F01)

- **Question:** Is S2's lower hallucination count against S0 more than the effect of naming fewer objects? That is, does S2 lie above S0's own truncation frontier?
- **Metric and unit:** the unit of analysis is the image. Four new systems or measures are defined, all derived from S0.
  - **(a) CMP of S2 against S0.** This is the §5 measure with X = S2 and Y = S0. On each image, k_i = min(m_S2,i, m_S0,i), where m is the number of distinct COCO-80 classes mentioned, so S0 keeps only its first k_i classes; in practice this truncates S0 per image to S2's count.
  - **(a′) Count-matched recall CMR_X** = 100 × Σ_i TP_X,i(k_i) / Σ_i |G_i|, over the images with k_i > 0.
    - Images with k_i = 0 are left out of both sums, counted and reported.
    - On one image set with one k_i, CMR_S2 − CMR_S0 = (Σk / Σ|G|) × (CMP_S2 − CMP_S0). CMR therefore shares the CMP test, and it is reported but not tested separately.
  - **(b) S0-trunc.** S0's caption keeps only its first j\* sentences.
    - *Sentence rule.* After Unicode NFC, a sentence ends at ".", "!", "?" or "…" followed by white space or the end of the text, and at every line break. Empty pieces are dropped. A final piece without end punctuation, for example a caption cut at 160 tokens, counts as a sentence. A caption with fewer than j\* sentences is kept whole. The kept sentences are joined by single spaces.
    - *Mentions.* They are extracted again from the cut text with the frozen extractor (`extract.mentions`, `coco80_vi.json`).
    - *The rule for j\*.* On UIT-ViIC test 231, from the G3 decodes of S0 and of S2 at OP\* (seed 42), j\* is the j in {1, …, 12} that minimises |mean_i m(S0 cut at j)_i − mean_i m_S2,i|. Ties go to the smaller j.
    - *When j\* is fixed.* Its value is written into the tier-1 freeze commit, before any T2 output, and is then used unchanged at tier 2. The same j\* is used for the KTVIC test 558 rows. The UIT-ViIC 231 rows of S0-trunc are in-sample for j\*, and the paper says so.
  - **(c) S0-two.** S0 decoded with the repository's existing two-sentence prompt, `PROMPTS["two"]` of `scripts/evaluate.py` at a68d5682. Its UTF-8 sha256 is 5e634d4ee5e037c804b8ed45652f97af1759f1dc9e156237fd56a5e7aad7767f. The repository describes it as a length-matched control for the two-sentence detailed output of reference-fusion SFT (`scripts/evaluate.py` l.67), not for S2. No other shorter prompt is used.
  - Each system is reported with R, h, CHAIR_i, words per caption, distinct classes per caption and the share of captions that reach the 160-token cap.
- **Data and role:** tier 1 (descriptive rows, seed 42) and tier 2 (the family T tests). Never tier 3.
- **Systems:** S2 (at OP\*) against S0, S0-trunc and S0-two; S1 is reported beside them.
- **Decision rule:** three members of family T, all at tier 2, each with a one-sided bootstrap p (G-4).
  - **T-1:** null CMP_S2 − CMP_S0 ≤ 0.
  - **T-2 (S2 dominates S0-trunc):** p = max(p_R, p_h), where p_R is for the null R_S2 − R_trunc ≤ 0 and p_h for the null h_S2 − h_trunc ≥ 0.
  - **T-3 (S2 dominates S0-two):** the same form with S0-two.
  - The tier-1 rows are descriptive.
- **Family:** T. It has four members, T-1 to T-4 (T-4 is in E-B3). Holm's correction is applied within T at α = 0.05.
  - A member PASSes iff its Holm-adjusted p < 0.05.
  - A member that is NOT_IDENTIFIED or NOT RUN enters Holm's correction with p = 1, so the family size stays at four.
  - T is separate from the registered secondary family (H3, H4, H5a and H5b) and changes none of its adjusted p-values. T changes no verdict of H1 to H5. Holm within T controls the family-wise error of T alone at 0.05; no error rate across the primary family, the secondary family and T is claimed. T is tested at tier 2, a set spent by FAIR 2026 and used here in its development-confirm role; it shares its images and its S0, S1 and S2 decodes with the tier-2 rehearsal of §7, which is a pass share and gates only through K2. A T verdict is reported as a registered test on the rehearsal set, never as confirmed and never as a tier-3 result (K6). A member whose arm stops under K3 or K4 is NOT RUN.
- **Settings fixed now:**
  - the sentence rule, the range of j and its tie rule (this erratum);
  - the prompt string and its sha (`scripts/evaluate.py` a68d5682);
  - decoding as G-3.
- **Against the claim:**
  - *If T-1 fails:* the paper states that, at a matched number of mentioned objects per image, S2 is not more precise than S0's first-mentioned objects. It does not use the words "beyond saying less", "above the truncation frontier" or similar.
  - *If T-2 or T-3 fails:* the paper states in its summary of results that S2 does not beat that length-controlled version of S0.
  - Each failed member is reported beside the H1 and H2 verdicts.
- **GPU-hours:**
  - (a) and (b): 0, because they use decodes the registration already produces.
  - (c): 0.7 at tier 1 (789 images at 3.2 s) and 4.5 at tier 2.
  - **Total 5.2.**
- **New code:** yes.
  - the "two" prompt key in `decode.py`;
  - the sentence rule, S0-trunc and the j\* chooser;
  - CMP and CMR against a single-decode system with seed pairing;
  - the family T machinery.
  - See CODE_NEEDS C01 to C04.
- **Commit before:** the first G3 output, for the j\* rule and the tier-1 rows; the first T2 output, for T-1 to T-3. This erratum is committed before the first G3 output.
- **Closes:** F01; MAP gap G1 (ratio metrics hide counts).
- **Provenance:** O1, where VSPS cut captions from 117 to 34 words while object recall fell from 57.1 to 37.1. The truncation-frontier argument itself is literature: LURE and Less is More, as cited in F01.

### E-B2. "Delete unverified objects at inference" baseline on S0 (finding F02)

- **Question:** Does deleting, at inference, the parts of S0's caption that the O31 verifier does not support give the same object recall and hallucination as fine-tuning? If so, what the fine-tuning buys is only inference cost.
- **Metric and unit:** the image.
  - **S0-filter** removes every sentence of S0's caption that mentions a COCO-80 class whose V-COCO verdict, under OP\*'s family set and thresholds, is not SUPPORTED, that is, REJECTED or UNCERTAIN. The combiner is §4.2 with E2: a missing family score never supports.
  - A class mentioned in several sentences removes every one of them.
  - Mentions per sentence are found by running `extract.mentions` on each sentence (sentence rule of E-B1).
  - Mentions are then extracted again from the kept text.
  - Reported: R, h, CMP of S2 against S0-filter, words per caption, and the inference GPU-seconds per image (the S0 decode plus the probes, from the run records).
- **Data and role:**
  - Tier 1 uses UIT-ViIC test 231, with the registered tier-1 V-COCO probes on S0's mentions (§7 tier 1).
  - Tier 2 uses the Karpathy test 5,000, with the registered T2 V-COCO probes on S0's mentions (COMPUTE_PLAN T2 row).
  - KTVIC test is not used, because no registered probe exists there.
- **Systems:** S0-filter against S2 (and S0, S1).
- **Decision rule:** descriptive, no rule. Paired 95 % CIs (G-4).
- **Family:** none.
- **Settings fixed now:**
  - the sentence rule (E-B1);
  - "not SUPPORTED" as the deletion criterion, which is the rule named in F02;
  - OP\*'s family set and thresholds, from P1.
- **Against the claim:** if S0-filter has R ≥ R_S2 and h ≤ h_S2, and both paired CIs exclude an advantage of S2, the paper states that on these sets the verifier applied to S0 at inference matches or beats the student. It also states that S2's remaining advantage is that it needs no verifier at inference, and gives the cost per image.
- **GPU-hours:** 0. It reuses the registered probes.
- **New code:** yes: sentence-level deletion by V-COCO verdict (CODE_NEEDS C05).
- **Commit before:** the first G3 output, for the tier-1 row; the first T2 output, for the tier-2 row.
- **Closes:** F02.
- **Provenance:** O9, which says that coverage depends on what is done with UNCERTAIN, together with the registered configuration (5) (S3) idea. The comparison itself is from the literature (F02). E-B2 is a baseline only: it makes no claim about inference-time filtering as a method and shares no claim with Paper C's inference-time verifier.

### E-B3. Five operating points and the monotone-ordering test (finding F04)

- **Question:** Does the student's object recall follow the supervision recall across verifier operating points chosen before training? This is the "dial" that a deployer would use.
- **Metric and unit:**
  - **The rule that picks two extra points, a pure function of P1's `k0.json`.**
    - OP_25, OP_75 and whether the five points are IDENTIFIED come from ERRATUM_O31_4 E4-2 and E4-3 (`ops5.json`). The new students, the tier-1 and tier-2 decodes of E-B3 and T-4 run only if `ops5.json` says IDENTIFIED. The two-point TR_R and TR_h between S1 and OP\* (from the G3 decodes, no new decode) are still reported if those decodes exist.
  - **New students.** One student is trained at each of OP_25 and OP_75 with the S2 recipe: seed 42, N_steps of E8, and the store's `sft.jsonl` sha recorded as E5. The OP_mid student already exists in G3 (A-1).
  - **Tier-2 outcome.** R and h of the five students at seed 42. The seed-42 S1 and S2 decodes already exist at tier 2.
  - **Transfer ratio, on one kind of gold only (KTVIC, tier 1).** Both sides use the same definitions:
    - the supervision side is k0.json's R_sup and the supervision h_sup = Σ_i |M_i \ G_i| / N, over the detailed store caption of each image, with gold = the 113-lexicon objects of the training references and N = the images with non-empty gold;
    - the student side applies the same `gate.funnel` definitions (R macro, P micro) and the same h to each student's KTVIC test 558 decodes, against the test references.
    - Reported: the five (supervision, student) pairs; TR_R = ΔR_student / ΔR_sup and TR_h = Δh_student / Δh_sup between S1 and OP\*; and least-squares slopes over the five points.
    - No ratio or slope is computed across gold types. A-1 stays as registered. Its UIT-ViIC rows compare caption gold with instance gold, and the paper labels them so.
- **Data and role:**
  - the extra points are chosen from the in-sample training-pool numbers of P1 (a design quantity);
  - the transfer ratio uses tier 1 (KTVIC test 558; dose-response is a listed role of that set, §3.3);
  - the ordering test uses tier 2. Never tier 3.
- **Systems:** S1 and the S2-recipe students at OP_25, OP_mid, OP_75 and OP\*, all at seed 42.
- **Decision rule:** **T-4** (family T), at tier 2. Predicted direction: R increases with R_sup. h is predicted not to decrease with R_sup, but h is descriptive and has no test.
  - T-4 is ERRATUM_O31_4 E4-7.
  - The transfer ratio is descriptive.
- **Family:** T (four members; E-B1).
- **Settings fixed now:**
  - the five points: ERRATUM_O31_4 E4-2 and E4-3;
  - seed 42 for all five points;
  - T-4's statistic: ERRATUM_O31_4 E4-7.
- **Against the claim:**
  - *If T-4 FAILs, or is NOT_IDENTIFIED by its zero-denominator rule (ERRATUM_O31_4 E4-7):* the paper reports the five points as a descriptive table beside that verdict and does not claim a monotone dial; claim (b) of E-A.3 is not made in any form. *If T-4 is NOT RUN, or the result in `ops5.json` is NOT RUN or NOT_IDENTIFIED (ERRATUM_O31_4 E4-2 and E4-3):* the paper reports that verdict with its cause and does not make claim (b) of E-A.3. When the result in `ops5.json` is NOT RUN or NOT_IDENTIFIED, no table of student results across the five points is offered (ERRATUM_O31_4 E4-4); the content of `ops5.json` is reported in every case. Which other rows exist follows the family-T rules of E-B1.
  - *If TR_R (point) lies outside [0.7, 1.3], the band of A-1's registered R-slope prediction:* the paper states that the student's recall does not follow the supervision recall one to one, and gives TR_R with its interval. A-1's own prediction is reported as registered, whatever TR_R shows.
- **GPU-hours:**
  - 2 SFT runs × 4.3 = 8.6;
  - tier-1 decodes of the two new students: 2 × 0.7 = 1.4;
  - tier-2 decodes of the OP_25, OP_mid and OP_75 students: 3 × 4.5 = 13.5.
  - **Total 23.5.**
- **New code:** yes:
  - the point chooser, a pure function of k0.json;
  - h_sup from the stores;
  - the student-side funnel;
  - the T-4 statistic.
  - See CODE_NEEDS C04, C06, C07, C23 (the `ops5.json` writer of ERRATUM_O31_4 E4-3) and C24 (the E4-7 statistic). P1's code (`k0.py`, `gate.run_k0`) is not changed: the chooser reads its output.
- **Commit before:** the first G3 output, for the transfer ratio, the new students and the registration of T-4 (ERRATUM_O31_4 E4-4).
- **Closes:** F04 (a) and (b); MAP break points SCAPO BP4, HalluciDoctor BP1 and SENTINEL BP3 (wording risk on novelty (ii)).
- **Provenance:** O2: the student's recall copies the supervision's recall (funnel 36.6 at `sft_caption` → student 37.1).

### E-B4. External comparison methods on one 24 GB GPU (finding F05)

- **Question:** How does S2 compare with published methods that a reviewer will name? Two are decoding-time methods on the same base model. The third is a released training-time model on the same base.
- **Metric and unit:** the image.
  - Reported: R, h, CHAIR_i, CMP of S2 against the comparator (k-matched as in E-B1 (a)), words per caption, and the measured inference GPU-seconds per image.
  - For English rows, the same measures are computed with the English COCO-80 extractor of H5 (CHAIR synonym map), with classes ordered by first mention.
- **Data and role:**
  - **C-VCD and C-DeCo:** Vietnamese, with the S0 prompt, at tier 1 (KTVIC test 558 and UIT-ViIC test 231) and at tier 2.
  - **C-SEN:**
    - in English at tier 1 (UIT-ViIC test 231) and at tier 2, against S0 and S2 decoded with the E6 English prompt (the registered H5 decodes at tier 2, and two new tier-1 decodes on the 231);
    - in Vietnamese at tier 1 only, labelled "outside the model's training language".
  - Never tier 3.
- **Systems:**
  - **C-VCD:** visual contrastive decoding on S0.
  - **C-DeCo:** dynamic correction decoding on S0.
  - **C-SEN:** the released SENTINEL LoRA adapter for Qwen2.5-VL-7B-Instruct (repository id `psp-dada/Qwen2.5-VL-7B-Instruct-SENTINEL`, as listed in the SENTINEL README and model card), loaded on the same bf16 base.
  - All three are compared with S0, S1 and S2.
- **Decision rule:** descriptive, no rule. Paired 95 % CIs (G-4).
- **Family:** none.
- **Settings fixed now (no tuning on any evaluation data):**
  - **C-VCD:** α = 1, β = 0.1 (adaptive plausibility), and diffusion noise step T = 500 of a 1,000-step linear schedule (β_t from 1e-4 to 0.02), with the noise seed 42 per image.
    - Sources: SENTINEL Table 12, which lists VCD's settings for its baseline (α 1.0, plausibility 0.1, noise step 500; read in the saved full text), and the group's own port in `scripts/baselines.py` (sha 1b7bf812), which FAIR 2026 used.
    - The VCD paper's own §4.1 values were not read verbatim in the primary source and are not verified here. The noise is the port's `diffusion_noise` (`scripts/baselines.py` 1b7bf812 l.80-86: a linear β schedule from 1e-4 to 0.02 over 1,000 steps, read in the saved file); SENTINEL Table 12 gives the step only. The schedule was not checked against VCD's released code, and the paper states this.
    - Greedy selection over the contrastive distribution, as in the port. The VCD paper samples, so this is a judge item.
    - Batch 1.
  - **C-DeCo:**
    - **Source rule (fails closed).** Before C09 is written, the DeCo paper and the official repository files that set the candidate layer range, α, top-p and top-k are saved at a pinned commit with their sha256, and each value is recorded with its file and line, together with L, the decoder-layer count of the models for which the governing source (below) gives the range, read as the language model's decoder-layer count in their saved `config.json` files, with their sha256; if those models do not all have the same L, or L cannot be read so, C-DeCo is NOT RUN. The saved repository's default governs; where it gives none, the saved paper's value governs; a value found in neither makes C-DeCo NOT RUN. The values expected from the unsaved reading are candidate layers 20 to 28 of 32, α = 0.6, top-p 0.9 and top-k 20; a different saved value replaces them and is reported. In this rule, in the saved-source rules of VR-SEN and VR-EFUF (E-B5) and in M5's batch-size rule, a setting that is read from saved files and for which the governing saved source gives more than one value, with nothing in that source marking one of them as the default, makes the item that needs it NOT RUN, and the paper reports it so.
    - **Layer mapping (this erratum's choice; DeCo reports no Qwen2.5-VL model).** A range [l_lo, l_hi] for an L-layer model maps to Qwen2.5-VL-7B's 28 decoder layers (`num_hidden_layers` = 28, checked in the pinned `config.json`) as [ceil(l_lo × 28 / L), floor(l_hi × 28 / L)], counting the first decoder layer as 1. With 20 to 28 of 32 this gives 18 to 24.
    - Greedy decoding, which is one of the strategies the paper tests. Batch 1.
  - **C-SEN:**
    - the released adapter at a pinned revision with per-file sha;
    - decoding as G-3;
    - no further training, and no preference optimisation is run by the group.
- **Precondition for C-SEN (registered; it fails closed):**
  - **PS-1, the adapter.** It is public and pinned. Its base is `Qwen/Qwen2.5-VL-7B-Instruct`, and its licence (Apache-2.0 per its card and README) is checked again at pin time.
  - **PS-2, its training images are identifiable.** This needs either the per-model training file of the dataset `psp-dada/SENTINEL` for this adapter, or a statement by the authors (dataset card or repository) that this adapter's pairs come from `image_data.jsonl`. Otherwise C-SEN is NOT RUN.
  - **PS-3, the overlap pass.** It runs on the laptop, with descriptors only and no SENTINEL training image on the PI's PC, because some Visual Genome images are COCO val2014 images and could belong to the tier-3 set (G-1).
    - (i) The COCO id of each training image is taken from the Visual Genome image metadata (`coco_id`) and compared with the ids of UIT-ViIC test 231 and the Karpathy test 5,000.
    - (ii) Exact sha and the committed W25 near-duplicate rule (CC-153) are applied with x = each evaluation set (UIT-ViIC 231, Karpathy test 5,000, KTVIC test 558) against the training images.
    - A hit leaves x for every C-SEN row: every system in those rows is re-scored on the reduced set, and the counts are reported.
    - If any part of PS-3 cannot be completed for a set, the C-SEN rows on that set are NOT RUN.
- **Against the claim:**
  - If a comparator has R ≥ R_S2 and h ≤ h_S2, with both paired CIs excluding an S2 advantage, the paper states this in its results and its summary of results. It names what S2 still offers: no extra inference passes (against VCD and DeCo) and no preference training (against SENTINEL).
  - A comparator whose run is NOT RUN is reported as NOT RUN, with the reason.
- **GPU-hours:**
  - C-VCD: about 2 forward passes per token, so 1.4 at tier 1 and 9.0 at tier 2 = 10.4.
  - C-DeCo: about 1.2× decode time (the review's figure), so 0.8 at tier 1 and 5.4 at tier 2 = 6.2.
  - C-SEN:
    - Vietnamese tier 1: 0.7;
    - English tier 1 for C-SEN, S0 and S2 on the 231: 0.6;
    - English tier 2: 4.5;
    - subtotal 5.8.
  - **Total 22.5** (22.46 before rounding).
- **New code:** yes:
  - the VCD port moved into the O31 decoder (the port's loader reads KTVIC only);
  - DeCo for Qwen2.5-VL (new);
  - the PEFT adapter load;
  - the English ordered extractor;
  - the PS-3 pass.
  - See CODE_NEEDS C08 to C11.
- **Commit before:** the first G3 output. The set of comparators and their settings must not depend on any student result. In every case this is before the first comparator output.
- **Closes:** F05; PRIOR_WORK_CHECK rows VCD, DeCo and SENTINEL; MAP break point SENTINEL BP1.
- **Provenance:** literature only (F05). VCD also ran in FAIR 2026 on KTVIC.

### E-B5. Verifier retention and rejection measured directly, for four rules on identical propositions (MAP break points EFUF BP1, SENTINEL BP2 and FeedQuill BP2)

- **Question:** On the same image and class pairs and the same human gold, does the O31 rule keep more true objects than published verifier rules, at an equal or smaller false-accept rate?
- **Metric and unit:**
  - The unit of analysis is the proposition, an (image, COCO-80 class) pair. Intervals are clustered by image: the 231 images are resampled with the shared index matrix.
  - Per rule: RT, FA, DR strict, and the share of UNCERTAIN among present and among absent classes.
  - The four rules:
    - **VR-SEN (SENTINEL style).** GroundingDINO and YOLO-World detect the English class name. SUPPORTED iff both detect it, REJECTED iff neither does, UNCERTAIN otherwise (SENTINEL §3.2 and App. B.4).
    - **VR-EFUF (EFUF style).** The CLIP score S = the maximum, over sliding windows, of CLIP(class name, window) (EFUF Eq. 1). SUPPORTED iff S > 32, REJECTED iff S < 23, UNCERTAIN otherwise (EFUF App. A.1).
    - **VR-FAIR.** FAIR's recorded verifier rule: Vintern-1B with K = 5 sampled dual queries and unanimity, the H4 comparator V_FAIR.
    - **VR-O31.** The registered three-state rule at OP\* (§4.2 with E2).
  - Single-family rows (Vintern alone and InternVL3 alone, at OP\*'s thresholds) are added at no cost.
  - **Error correlation between the two O31 families (F07 (b)):**
    - the Spearman correlation of s between Vintern-1B and InternVL3-8B over the absent classes of P-b;
    - over the absent classes of P-b, the number with both families' s ≥ τ_acc(OP\*), divided by the number with at least one family's s ≥ τ_acc(OP\*) (the joint share of the OR rule's false accepts).
- **Data and role:** UIT-ViIC test 231, with COCO-2014 instance gold. This use is within the set's registered role: §3.2 names it as the V-COCO development set, and the §3.3 table gives it "instance-gold dev for the student and for V-COCO". There are two proposition sets on the same 231 images:
  - **P-a:** the registered V-COCO propositions, one per COCO-80 class mentioned in S0's G3 decode. The earlier study E1a found only 48 absent classes on these images (O5), so FA on P-a is reported with its CI but never read.
  - **P-b (balanced set):** on each image,
    - every COCO-80 class with at least one instance annotation (crowd included);
    - the three absent classes with the highest summed co-occurrence with the image's present classes (co-occurrence of classes c and d = the number of COCO-2014 train images with at least one instance annotation of each), ties broken by the smaller category id;
    - three further absent classes drawn uniformly at random without replacement from the absent classes not already chosen, listed in ascending category-id order, by one `numpy.random.default_rng(20261129)` stream used image by image in ascending image-id order (`rng.choice(remaining, 3, replace=False)`).
    - An absent class has no annotation at all, crowd included. P-b has about 2,000 propositions. P-b is not the POPE benchmark; the paper never calls it POPE and never sets its numbers beside POPE results (§5).
  - Probe texts:
    - Vintern and InternVL3 get the §4.1 Q⁺ template, with the matched Vietnamese phrase for P-a and the first listed term of `coco80_vi.json` for P-b;
    - detectors and CLIP get the COCO English category name of the same class.
- **Systems:** VR-SEN, VR-EFUF, VR-FAIR and VR-O31 (and the single-family rows).
- **Decision rule:** descriptive, no rule.
  - A difference may be described in the paper as "favouring VR-O31 over rule X" only if, on P-b, the CI lower bound of RT(VR-O31) − RT(X) is above 0 and the CI upper bound of FA(VR-O31) − FA(X) is at most +5.0 points.
  - This is H4's form applied as a descriptive reading. It is not H4, it is not on the tier-3 set, and it changes no H4 verdict.
- **Family:** none.
- **Settings fixed now:**
  - **VR-EFUF:**
    - **Source rule (fails closed).** Before C12 is written, the EFUF repository files `common/args.py` and `insight/clip.py` are saved at a pinned commit with their sha256. The CLIP checkpoint, image preprocessing, patch size, window size, stride, the text form of an object and the score scale are taken from them and recorded with file and line; the values expected from the unsaved reading are `openai/clip-vit-base-patch32`, 48 px patches, windows of 4 × 4 patches and stride 1 patch. If any of these cannot be read in the saved files, VR-EFUF and M5 are NOT RUN.
    - the maximum over windows, as in the paper's Eq. 1 (saved full text). The repository's `average_top_k` default is not used: the paper is the published method, and the paper states the difference;
    - thresholds 32 and 23.
  - **VR-SEN:** the detector checkpoints, thresholds and text-prompt form (one class per prompt, or all names joined) of the released SENTINEL code (`model/detector/grounding_dino.py` and `yolo_model.py`) at a pinned commit. They could not be read for this draft (HTTP 503). Before C12 is written, those files are saved with their sha256, and each value is recorded with its file and line. If any of these values cannot be read in the saved files, VR-SEN is NOT RUN and reported so; no value is chosen by anyone.
  - **VR-FAIR:** the rescap verifier code that T2v will use, with torch, NumPy and Python `random` seeded with 42 once per job. Its sampled answers are not claimed to be bit-reproducible.
  - **VR-O31:** OP\* from P1.
- **Against the claim:**
  - If VR-SEN or VR-EFUF keeps as many true classes as VR-O31 at an equal or smaller FA on P-b, the paper states that its verifier's retention is not better than that published rule's.
  - If VR-O31's FA on P-b exceeds VR-FAIR's by more than 5 points, the paper says so beside T-a.
  - Detectors and CLIP were trained on data that includes COCO. The paper states this as a limitation of the comparison.
- **GPU-hours:**
  - VR-FAIR on P-a and P-b: about 0.8;
  - InternVL3 and Vintern on P-b: about 0.3;
  - detectors and CLIP: about 0.3;
  - model loads: 0.6.
  - **Total 2.0.** The Vintern and InternVL3 probes on P-a are registered.
- **New code:** yes:
  - the P-b builder;
  - detector and CLIP wrappers;
  - VR-FAIR on a given proposition list (shared with T2v);
  - RT, FA and DR with clustered intervals.
  - See CODE_NEEDS C12.
- **Commit before:** the first G3 output (P-a is formed from G3's S0 decode).
- **Closes:** MAP gap G2 (verifier retention never reported); F07 (b); PRIOR_WORK_CHECK rows EFUF and SENTINEL.
- **Provenance:**
  - O4 (the answer source, not the threshold, moves retention);
  - O5 (retention 36.6 / 42.6 on T-COCO);
  - O7 (a cross-family verifier moves precision and retention together);
  - O8 (detector gates cost recall).

### E-B6. The 2 × 2 that separates the verifier change from the budget change (finding F09)

- **Question:** How much of S2's recall gain over S1 comes from the verifier, and how much from the coverage-scaled budget?
- **Metric and unit:** the image; R and h (§5).
  - **The four arms:**
    - S1 (FAIR verdicts, B = 9);
    - A-3 (O31 verdicts at OP\*, B = 9; registered);
    - **A-8 (new: FAIR's recorded verdicts with the scaled budget B_i of §4.4);**
    - S2 (O31 verdicts at OP\*, scaled budget).
  - **The contrasts:**
    - the verifier effect at each budget (A-3 − S1; S2 − A-8);
    - the budget effect at each verifier (A-8 − S1; S2 − A-3);
    - the interaction (S2 − A-3) − (A-8 − S1).
  - The supervision side of the same 2 × 2 (R_sup and P_sup of the four stores) is reported from CPU builds.
- **Data and role:** tier 1 (KTVIC test 558 and UIT-ViIC test 231), seed 42.
- **Systems:** S1, A-3, A-8 and S2.
- **Decision rule:** descriptive, no rule. Paired 95 % CIs.
- **Family:** none.
- **Settings fixed now:**
  - A-8's store follows the order of ERRATUM_O31_1 E4: recorded statuses, then `person_uncap`, then the build with `scaled=True` (E5 filters). This is the same call K0 makes for S1, except for the budget.
  - Its store sha is recorded (E5).
  - Training: the S2 recipe, seed 42, N_steps.
  - A-8 runs as its own job right after the G4 job (its cap in `COMPUTE_ADDENDUM.tsv`), never inside G4's launch.
- **Against the claim:** if the verifier effect's CI includes 0 at both budgets, while the budget effect explains most of S2 − S1, the paper states that the recall gain comes from the budget rule, not from the verifier.
- **GPU-hours:** 1 SFT (4.3) + tier-1 decodes (0.7). **Total 5.0.** The store is built on CPU.
- **New code:** yes: the A-8 store build, a call of the existing `store.rebuild` outside `run_k0` (CODE_NEEDS C13).
- **Commit before:** the first G3 output, so that the arm is not chosen after S2 has been seen.
- **Closes:** F09.
- **Provenance:** O2. The recorded funnel splits the loss between the verifier (−18.0) and the selector, filters and renderer, so budget and verifier are separate levers.

### E-B7. Power reading for H2 (finding F03), advisory

- **Question:** Before the GPU-hours of G4 to T2 are spent, how likely is H2, with its frozen margin, to pass?
- **Metric and unit:**
  - **PR-0 (fixed now; arithmetic only; reads no data).** Under a normal approximation, H2 at tier 3 passes with probability Φ(−δ / SE − 1.96), where δ is the true D. For P ≥ 0.98, δ must be at most −4.01 × SE.
    - With FAIR's COCO values (h_S0 0.45, h_S1 0.17; O1), the margin is 0.07, so D = h_S2 − 0.24.
    - The table below gives the largest h_S2 that allows P(H2) ≥ 0.98. It is an upper bound for the joint H1 ∧ H2 gate.

    | SE(D) at n = 4,224 | required D | largest h_S2 |
    |---|---|---|
    | 0.005 | ≤ −0.020 | 0.220 |
    | 0.0075 | ≤ −0.030 | 0.210 |
    | 0.010 | ≤ −0.040 | 0.200 |
    | 0.015 | ≤ −0.060 | 0.180 |
    | 0.020 | ≤ −0.080 | 0.160 |

    The design expectation of h_S2, about 0.17 to 0.25 (DIRECTION_NOTE §4), spans this whole range.
  - **PR-1 (at the G3 read).**
    - Inputs: from the seed-42 G3 decodes of S0, S1 and S2 on UIT-ViIC test 231, the estimate D̂ and its bootstrap SE_231 (G-4), computed with COCO-80 instance gold only, the units of tier 2 and tier 3 (E11). A second row with gold = instances ∪ references is labelled as such.
    - Projection: SE_4224 = SE_231 × sqrt(231 / 4,224), with P(H2) = Φ(−D̂ / SE_4224 − 1.96).
    - Also reported: the largest h_S2 for P(H2) ≥ 0.98 given ĥ_S0 and ĥ_S1 of the 231, and ρ̂ with its CI.
- **Data and role:** PR-0 uses no data. PR-1 uses tier 1 (UIT-ViIC test 231).
- **Systems:** S0, S1 and S2 (seed 42).
- **Decision rule:** descriptive, no rule.
  - The reading is advisory. It does not start, stop or change any registered step, and it neither fires nor waives K1 or K2, which remain the only registered stops.
  - If the PI decides on this reading not to spend further GPU-hours, that decision lies outside the registration. The paper reports it together with the reading (K6).
  - The projection assumes that the per-image variance transfers from 231 COCO images to 4,224, and it uses one seed where tiers 2 and 3 average three. The judge states both assumptions.
- **Family:** none.
- **Settings fixed now:** the formulas above; the projection from 231 to 4,224; instance-only gold for the main row.
- **Against the claim:** a projected P(H2) far below 0.98 is reported in the decision record and, if the line stops, in the paper.
- **GPU-hours:** 0.
- **New code:** yes: a small calculator (CODE_NEEDS C14).
- **Commit before:** the first G3 output. PR-1 reads G3 outputs, so its form must exist before them.
- **Closes:** F03 (a) and (b). F03 (c) is not taken (E-D.2).
- **Provenance:** O1 (FAIR's COCO values set the margin).

### E-B8. Reporting rows at no GPU cost (findings F10 (b, c), F12, F14, F15, F18)

Each row below is descriptive, no rule; family none; GPU-hours 0. Each is reported beside the registered rows, whatever its result.

- **R-a. CI of ρ (F18).**
  - **Question:** How precise is the recall recovery that the headline names?
  - **Metric and unit:** the percentile 95 % CI of ρ, from the replicates H1 already draws. A replicate with R_S0 − R_S1 ≤ 0 is undefined (E9).
  - **Data and role:** tier 2, and tier 3 at the registered look (ρ is a registered tier-3 quantity whose replicates H1 already draws; decided by CC-525, `OPEN_FOR_JUDGE.txt` A5).
  - **Systems:** S0, S1 and S2.
  - **Decision rule:** descriptive, no rule.
  - **Family:** none.
  - **Settings fixed now:** E9.
  - **Against the claim:** a CI of ρ that reaches below 0.5 is printed in the same sentence as the H1 headline. The registered headline text itself is unchanged.
  - **GPU-hours:** 0.
  - **New code:** yes, small (C15).
  - **Commit before:** the first T2 output.
  - **Closes:** F18.
  - **Provenance:** literature only (review F18).
- **R-b. Seeds (F10 (b)).**
  - **Question:** Does the interval change when training noise is resampled?
  - **Metric and unit:** a two-level bootstrap. In each of the shared replicates, three seed indices are drawn with replacement from {42, 43, 44} (numpy PCG64, seed 20261130), one draw per replicate shared by S1 and S2 so that the E12 pairs are resampled as pairs, and the image's count is the mean over the drawn seeds. Output: the CIs of ρ, D and the H3 Δ under this scheme. Per-seed values are already registered (§6.3).
  - **Data and role:** tier 2.
  - **Systems:** S0, S1 and S2.
  - **Decision rule:** descriptive, no rule.
  - **Family:** none.
  - **Settings fixed now:** the seed and the draw.
  - **Against the claim:** a sensitivity CI that crosses the registered bound is reported beside the verdict.
  - **GPU-hours:** 0.
  - **New code:** yes (C15).
  - **Commit before:** the first T2 output.
  - **Closes:** F10 (b).
  - **Provenance:** literature only.
- **R-c. Edge of the grid (F10 (c)).** R-c is ERRATUM_O31_4 E4-5.
- **R-d. Lexicon validity on human text (F12).**
  - **Question:** How well does the frozen Vietnamese mention extractor agree with COCO instance gold when the text is human?
  - **Metric and unit:**
    - the unit is the (image, class) pair;
    - the extractor (`extract.mentions`) runs on the existing Vietnamese references of UIT-ViIC test 231;
    - output: per class, precision and recall of the lexicon's mentions against instance presence; the human "hallucination" floor h_ref; and the five classes with the lowest precision among those with at least 5 mentions.
    - Counts only; no text.
  - **Data and role:** UIT-ViIC test 231 (its gold is instances ∪ references, §3.3).
  - **Systems:** human references.
  - **Decision rule:** descriptive, no rule.
  - **Family:** none.
  - **Settings fixed now:** the frozen extractor; the minimum of 5 mentions.
  - **Against the claim:** classes with low precision on human text are named in the paper, and the human floor is printed beside every h.
  - **GPU-hours:** 0.
  - **New code:** yes (C15).
  - **Commit before:** the first G3 output.
  - **Closes:** F12.
  - **Provenance:** literature only (review F12).
- **R-e. Naturalness of the student's captions (F15).**
  - **Question:** Does the student only learn the renderer's templates?
  - **Metric and unit:** per system and set:
    - the store-overlap share, which is the share of a caption's word 4-grams that occur among the 4-grams of its arm's training store's detailed targets (for S0, against S2's store);
    - distinct-2;
    - self-BLEU-4 on min(500, n) captions per system and set, the same image ids for every system of a set (drawn once per set by `numpy.random.default_rng(20261131).choice(n, min(500, n), replace=False)` over the image ids in ascending order; all 231 on UIT-ViIC), each scored against the others. Word n-grams here and in the store-overlap share use the §5 tokenisation (Vietnamese: NFC, then the pinned RDRSegmenter, lower-cased, punctuation tokens removed; English: PTB).
  - **Data and role:** tiers 1 and 2.
  - **Systems:** S0, S1, S2 and the E-B1 and E-B4 systems.
  - **Decision rule:** descriptive, no rule.
  - **Family:** none.
  - **Settings fixed now:** the n-gram orders, the sample size and the seed.
  - **Against the claim:** none; the shares are printed for every system, S2's and S1's side by side, with no qualitative label.
  - **GPU-hours:** 0.
  - **New code:** yes (C15).
  - **Commit before:** the first G3 output.
  - **Closes:** F15.
  - **Provenance:** literature only.
- **R-f. Cost table (F14).**
  - **Question:** What does the method cost per new domain?
  - **Metric and unit:** stage-1 GPU-seconds per image (record field `stats.seconds` for the 69 G1 images; FAIR's planning value for the rest), probe GPU-hours, SFT hours and inference GPU-seconds per image, all from the run records.
  - **Data and role:** run records.
  - **Systems:** all arms.
  - **Decision rule:** descriptive, no rule.
  - **Family:** none.
  - **Settings fixed now:** the sources named.
  - **Against the claim:** none. It is a cost statement.
  - **GPU-hours:** 0.
  - **New code:** yes, small (C15).
  - **Commit before:** the first G3 output.
  - **Closes:** F14.
  - **Provenance:** literature only.
- **R-g. Token-cap share.**
  - **Question:** How many captions are cut by the 160-token cap?
  - **Metric and unit:** the share of captions whose decode record has `hit_max` true, per system and set.
  - **Data and role:** tiers 1 and 2.
  - **Systems:** all decoded systems.
  - **Decision rule:** descriptive, no rule.
  - **Family:** none.
  - **Settings fixed now:** the cap of `decode.py`.
  - **Against the claim:** a large share for S0 means S0 is already truncated by the cap. This is stated beside E-B1.
  - **GPU-hours:** 0.
  - **New code:** yes, small (C15).
  - **Commit before:** the first G3 output.
  - **Closes:** the length half of F01.
  - **Provenance:** O1.

---

## E-C. Optional modules

Each module is self-contained. The PI keeps or drops each one, and the keep or drop decision is recorded before the first G3 output, so that no module is chosen after a student result has been seen. For each module whose keep or drop answer from the PI is not recorded before the first G3 output, its default applies, whatever is recorded for the other modules: M3, M4 and M5 are kept; M1 and M2 are dropped (Gemma 3's terms need the PI's own acceptance). An answer recorded after the first G3 output changes nothing. Every module is descriptive, with no rule and no family. Dropping a module changes nothing else in this erratum: no module adds a member to family T or to any registered family. Rules G-1 to G-6 of E-B apply to every module.

### M1. A third verifier family outside the Qwen and InternVL lines, as a swap ablation A-7 (finding F07 (a))

- **Question:** Is S2's gain tied to the two InternVL-line verifiers, or does a verifier from another family give it too?
- **Exactly which variant:** the swap ablation only. A-7 replaces InternVL3-8B with the new family: the family set becomes {Vintern ∪ new}.
  - The K0-grid variant, which would add the new family to the 30-point grid, is **not offered**. It would change the set over which OP\* and K0 are chosen, and this erratum changes neither.
  - That variant is not offered; it could only have been registered before the first P0r output.
- **Metric and unit:**
  - A-7's operating point is chosen by the K0 rule (the highest R_sup with P_sup ≥ P_floor; ties as E7) over the 15 (τ_acc, τ_rej) points with the family set {Vintern ∪ Gemma}. This is a replay with no K0 verdict. If no point meets P_floor, A-7 is NOT RUN.
  - Reported: the student's R and h on tier 1, the error correlation of each family pair (as E-B5), and the new family's RT and FA on P-a and P-b.
- **Data and role:** probes on the training pool (in-sample, for training); tier 1 for the student; UIT-ViIC test 231 for the verifier rows.
- **Systems:** A-7 against S2 and S1.
- **Model:** `google/gemma-3-4b-it` in bf16, pinned by revision and per-file sha.
  - It shares neither the encoder family nor the language-model family of the others. Its language model is Gemma; its encoder is SigLIP-based per the Gemma 3 report, which was not checked again here.
  - Its card states "over 140 languages" and 256 image tokens per 896 × 896 image, and says it is supported from transformers 4.50.0, so it runs in the `PY` environment (4.51.3). This is to be checked at pin time.
  - The model is gated on its hub, so the PI's account must accept its terms before the download.
  - A Vietnamese smoke check (the §4.1 rule: median yes/no mass ≥ 0.5 over the first 20 probes, with token sets checked as for M0) must pass, or the module is NOT RUN.
- **Decision rule:** descriptive, no rule.
- **Family:** none.
- **Settings fixed now:**
  - the Q⁺ probe form and score of §4.1;
  - the token-set rule;
  - batch 1 (no batch-8 parity rule is registered for it);
  - the 15 τ points;
  - the K0 selection rule;
  - the S2 training recipe, with seed 42.
- **Against the claim:** if A-7's student recall is close to S1's (the CI of R_A7 − R_S1 includes 0) while S2's is not, the paper states that the gain depends on the InternVL-line verifier.
- **GPU-hours:**
  - pool probes: about 176,000 × 0.2 s ≈ 9.8 (the speed is an unmeasured estimate, which the smoke replaces);
  - verifier-set probes: 0.2;
  - SFT: 4.3;
  - tier-1 decodes: 0.7.
  - **Total about 15.0.**
- **New code:** yes: a Gemma probe family, and a replay of the 15 points with that family set (CODE_NEEDS C16).
- **Commit before:** the keep or drop decision before the first G3 output; the module text before its first probe job.
- **Closes:** F07 (a); MAP break point FeedQuill BP2 (part).
- **Provenance:** O7 (a cross-family verifier moves precision and retention together) and O8.

### M2. A second student backbone of another family, trained on the same stores (finding F08)

- **Question:** Does the S1-to-S2 effect hold for a student that is neither Qwen nor InternVL, trained on byte-identical stores? For that student the stores are off-policy.
- **Metric and unit:** the image.
  - ρ_G and D_G are computed in the H1 and H2 forms for the triple (M2-S0 zero-shot, M2-S1, M2-S2), with CIs. R, h and CMP are also reported.
  - The paper may use the words "the effect replicates on a second backbone" only if, at tier 2, ρ_G (point) ≥ 0.50 and the CI upper bound of D_G is below 0. This is a descriptive reading, not a verdict.
- **Data and role:** tier 1 and tier 2, in Vietnamese with the S0 prompt. Never tier 3.
- **Systems:** M2-S0, M2-S1 (S1's `sft.jsonl`) and M2-S2 (S2's `sft.jsonl` at OP\*), all `google/gemma-3-4b-it`, seed 42.
- **Decision rule:** descriptive, no rule.
- **Family:** none.
- **Settings fixed now:**
  - QLoRA as §2: NF4 with double quantisation, bf16 compute, r = 16, α = 32, learning rate 1e-4, batch 1 with gradient accumulation 8;
  - N_steps by the E8 rule on S1's rows;
  - loss on the target tokens only;
  - the language-model linear layers as LoRA targets, with the vision tower frozen;
  - the model's own image processing, 256 tokens per image, with pan-and-scan off;
  - Gemma's own chat template with the Vietnamese detailed prompt;
  - decoding as G-3.
  - K3 applies to each arm: more than 2.0 % language-check failures stops that arm.
- **Against the claim:** if the reading fails, the paper states that the effect is shown for Qwen2.5-VL-7B only.
- **GPU-hours:**
  - 2 SFT × 4.3 = 8.6 (planning value; the 4B model is likely faster);
  - tier-1 decodes: 3 × 0.7 = 2.1;
  - tier-2 decodes: 3 × 4.5 = 13.5.
  - **Total about 24.2.**
- **New code:** yes: training and decoding for a Gemma student (CODE_NEEDS C17).
- **Commit before:** the keep or drop decision before the first G3 output; the module text before its first SFT.
- **Closes:** F08.
- **Provenance:** literature only (review F08; the on-policy argument of OPA-DPO).

### M3. A general-capability check on one public benchmark (MAP break points ClaimDiff-RL BP3 and FeedQuill BP4)

- **Question:** Does caption fine-tuning cost the student general ability (the "alignment tax")?
- **Metric and unit:** MME (perception and cognition), with its own scoring.
  - Per subtask, accuracy and accuracy+ (both questions of an image correct). The subtask score is 100 × (accuracy + accuracy+). The totals are the perception and cognition sums.
  - CIs come from a paired bootstrap over MME images (B = 10,000, seed 20261127).
  - An answer counts as "yes" or "no" only if the lower-cased output starts with that word. Any other answer is wrong. No language model extracts answers.
- **Data and role:** MME, a public benchmark outside the registration, used here only as a development check.
  - **Custody precondition:** on the laptop, before any MME image goes to the PI's PC, every MME image is checked against KV-4,224 by exact sha and the committed W25 rule, using the existing W25 memory.
  - A hit is removed from M3's MME set, and the count is reported. Some MME subtasks use COCO val2014 images.
- **Systems:** S0, S1 (seed 42) and S2 (OP\*, seed 42).
- **Decision rule:** descriptive, no rule.
- **Family:** none.
- **Settings fixed now:**
  - MME's own question text, which ends in its yes/no instruction;
  - greedy decoding with at most 10 new tokens;
  - the bf16 base;
  - batch 1;
  - the dataset pinned by revision and sha at pin time (its source and licence are not yet checked). If it cannot be pinned or its licence does not allow this use, M3 is NOT RUN.
- **Against the claim:** an S2 − S0 drop whose CI excludes 0 is stated in the paper as a cost of the method, beside S1's drop.
- **GPU-hours:** about 1.5 (3 systems × 2,374 questions, short answers; estimate).
- **New code:** yes: an MME runner and scorer, and the laptop overlap pass (CODE_NEEDS C18).
- **Commit before:** the keep or drop decision before the first G3 output; in every case before the first MME output.
- **Closes:** MAP gap G6.
- **Provenance:** literature only (ClaimDiff-RL Table 2; FeedQuill Table 7).

### M4. Counts and the blind spot of object-only measures (finding F06; MAP gap G3)

- **Question:**
  - (a) Do count errors rise with the looser verifier?
  - (b) What share of human-labelled errors can an object-existence measure not see, including this study's own measures and SCAPO-style object rewards?
- **Metric and unit:**
  - **(a) Count claims, unit = claim.**
    - *What counts as a claim.* A Vietnamese numeral token immediately before a matched COCO-80 mention, or separated from it by exactly one classifier token from a fixed list. All matching is on the extractor's normalised text.
    - *Numerals:* hai, ba, bốn, năm, sáu, bảy, tám, chín and mười, and digit strings from 2 to 99. The word "một" is excluded, because it also works as an indefinite article, and vague quantifiers are excluded.
    - *Classifiers:* con, cái, chiếc, người, quả, trái, cây, bức, tấm, cuốn, quyển, chú, đứa, bông, ngôi, tòa (also spelled toà), miếng, lát.
    - *Gold:* the gold count c is the number of the class's instances with iscrowd = 0. A claim is unscorable, and counted as such, if any iscrowd = 1 instance of that class exists.
    - *Scoring:* a claim is correct iff its number equals c. Reported: the count-claim error rate (wrong / scorable) and wrong count claims per caption.
  - **(b) The rewarded-error rate, unit = annotated segment.**
    - Segments and labels follow M0's rule (eligible labels ACCURATE and INACCURATE).
    - A segment is "object-clean" if it mentions at least one COCO-80 class (English CHAIR synonym map, `extract.en_classes`) and every class it mentions is present in the image's COCO-2014 instances.
    - The rewarded-error rate is the share of object-clean segments that humans labelled INACCURATE. It is broken down by M0's claim-type rule (count, attribute, relation, object).
- **Data and role:**
  - (a) uses UIT-ViIC test 231 (tier 1) and tier 2, with Vietnamese decodes and instance gold.
  - (b) uses M-HalDetect validation labels (V-EN's development role, §3.2), restricted to M0's operating set, which already excludes Karpathy-test images and the images other studies own. It runs on CPU and needs no images.
- **Systems:** (a) S0, S1 and S2, plus the E-B1 and E-B4 systems. (b) The measure itself.
- **Decision rule:** descriptive, no rule.
- **Family:** none.
- **Settings fixed now:**
  - the numeral and classifier lists;
  - the crowd rule and the exclusion of "một" (this erratum's choice; a judge item);
  - M0's segment and claim-type rules, unchanged.
- **Against the claim:**
  - (a) If S2's count-claim error rate is above S1's, with the CI of the difference excluding 0, the paper states that the recall gain comes with more count errors.
  - (b) The rate is printed in the limitations as the share of human-labelled errors that the paper's object measures cannot see.
- **GPU-hours:** 0.
- **New code:** yes: a count-claim extractor and a rewarded-error counter that reuses M0 (CODE_NEEDS C19 and C20).
- **Commit before:** the keep or drop decision before the first G3 output.
- **Closes:** F06 (b); MAP break point SCAPO BP2.
- **Provenance:** (a) literature only (F06). (b) O6 (M-HalDetect, all claim types) and O9 (no spatial relation was ever SUPPORTED).

### M5. A training-time comparator that is not preference optimisation: EFUF-style unlearning (finding F05 (3))

- **Question:** Does a published training-time method that needs no preference pairs and no verifier at inference match S2 at the same base and pool?
- **Metric and unit:** the image. Reported: R, h, CMP of S2 against C-EFUF, and words per caption.
- **Data and role:**
  - Training uses the O31 training pool after the §3.5 part (a) removals.
  - The model's own detailed captions are needed, and the stage-1 records hold only the rendered caption (`scripts/generate_stage1.py`, record field `caption`). S0's detailed decode of every pool image is therefore made anew.
  - Evaluation is at tier 1 and tier 2, in Vietnamese. Never tier 3.
- **Systems:** C-EFUF against S0 and S2.
- **Decision rule:** descriptive, no rule.
- **Family:** none.
- **Settings fixed now:** EFUF's published settings, App. A.1:
  - the multimodal mapping layers only are trained, which for Qwen2.5-VL is the vision-language merger;
  - AdamW, learning rate 1e-5, weight decay 0.05, 1 epoch;
  - λ₁ = 0.3 and λ₂ = 0.2;
  - T₀ = 32, T₁ = 23 and T₂ = 27.5;
  - subsentences delimited by punctuation (§4.2);
  - the CLIP scorer as E-B5 VR-EFUF.
  - Object mentions come from the frozen lexicon (COCO-80 only), mapped to English class names. This replaces EFUF's LLaMA-2-70B object extraction, a stated deviation.
  - The batch size is the EFUF repository default, read in the saved repository files (the EFUF source rule of E-B5) and recorded with file and line; if it cannot be read there, M5 is NOT RUN.
  - Seed 42.
- **Against the claim:** if C-EFUF dominates S2 (R ≥, h ≤, both CIs excluding an S2 advantage), the paper says so.
- **GPU-hours:**
  - S0 pool decodes: 3,767 × 3.2 s ≈ 3.4;
  - CLIP: 0.5;
  - training: 3.0 (estimate; projector only, one epoch);
  - tier-1 decodes: 0.7;
  - tier 2: 4.5.
  - **Total about 12.1.**
- **New code:** yes: CLIP scoring of subsentences, the D⁺, D⁻ and D^s builder, the three-stream loss and merger-only training (CODE_NEEDS C21).
- **Commit before:** the keep or drop decision before the first G3 output.
- **Closes:** F05 (training-time comparator); MAP break point EFUF BP2 (part).
- **Provenance:** O3 (editing the model's own captions keeps recall but transfers about a third of the hallucination gain).

### Not a module: a preference-optimisation (DPO) comparator
No DPO comparator is trained. DPO is deferred by the proposal (Table 2, FAIR 2029) and needs the PI's own word. It is listed as an open question in `OPEN_FOR_JUDGE.txt`. Evaluating the released SENTINEL adapter (E-B4) runs no preference optimisation.

---

## E-D. What this erratum does not change, what it does not take, and when each item must be committed

### E-D.1 Unchanged (explicit list)
- RQ8 and the claim form of §1.
- The systems S0, S1, S2 and S3, and the training recipe, seeds, N_steps (E8) and loss mask of §2.
- The training pool, the twin exclusion and the 69 G1 images (§3.1; ERRATUM_O31_3).
- The yardsticks V-COCO, V-EN and V-VI (§3.2).
- The roles of every set (§3.3 and §3.4), the tier-3 branch rule and Q1.
- Custody and the §3.5 overlap rule (with E2 and E13).
- The probe form, score, token sets and families (§4.1, E3, E4).
- The three states and the combiner (§4.2, E2).
- The 30-point grid (§4.3).
- The store build and budget constants (§4.4, E4 to E6).
- Gate K0, P_floor, OP\*, OP_mid and their tie rules (§4.5, E7).
- Every metric definition of §5.
- H1 to H5, their thresholds, the H2 margin (frozen, PI-Q-H2), T-a, the secondary family of four with Holm, and the statistics of §6.3 (E1, E9, E12).
- The three-tier path, P(PASS) ≥ 0.98, B_out, B_in and the rehearsal seed (§7, E10).
- The ablations A-1 to A-6, as registered (§8).
- The stop rules K0 to K6 (§9).
- Models, licences and deviations (§10, §11), for the models and data the registration names. The models and data this erratum adds (CLIP ViT-B/32, GroundingDINO, YOLO-World, the SENTINEL adapter, Gemma 3 4B, Visual Genome metadata and images, COCO-2014 train instance annotations, MME) are pinned by revision and per-file sha, and their licences are checked at pin time as §10 requires; an item whose licence does not allow this research use is NOT RUN. Gemma 3's terms must be accepted on the PI's account (M1, M2).
- The host rules and the caps of every registered job (ERRATUM_O31_2; COMPUTE_PLAN).
- The G1 generator, the seed and the file matching (ERRATUM_O31_3).
- The G2 probe form, environment and batch rule.
- ERRATUM_O31_4 (0a0bd365): the point rule (E4-2, E4-3), what its result allows (E4-4), the edge row (E4-5), the text left as it was (E4-6), and T-4's form and place in a family (E4-7).

### E-D.2 Review items not taken (one sentence each)
- **F03 (c), a "dev-confirmed" wording for the case where H1 and H2 pass at tier 2 but P(PASS) < 0.98.** Not taken: K6 forbids calling a development result confirmed, and §7 already fixes how that branch is reported.
- **F06 (c), attribute and action rates scored by a held-out verifier family.** Not taken: it would add a model-judged outcome to a paper whose outcome gold is all human; M4 covers counts with human gold.
- **F06 (d), an open-vocabulary check on AMBER.** Not taken: it would spend the branch-2 tier-3 candidate, which is the PI's decision under §3.4.
- **F10 (a), a per-seed condition on the headline wording.** Not taken: the headline rule of §6.1 is registered text; per-seed values are already reported (§6.3), and R-b adds a sensitivity row.
- **F10 (d), a second learning rate.** Not taken: about 10 GPU-hours, for a sensitivity that no other finding depends on.
- **F11, a probe of mention policy against perception.** Not taken in this erratum: it adds two new mechanism predictions that need their own power reading; it can be added as a module only if committed before the first G3 output.
- **F13, a verifier row on KTVIC test images.** Not taken: KTVIC gold is caption-derived, so "absent" is unreliable and FA cannot be read; possible contamination of the verifiers' training data with COCO is stated as a limitation.
- **F16, presentation of the tiers.** Not an erratum item: the tier-3 answer Q1 is already due before the first G3 output, and E-A.2 item 7 adds the sentence.
- **F18 rewording of the headline.** Not taken as worded: the headline text is registered; R-a prints the CI of ρ in the same sentence instead.
- **F05: OPERA, PAI, Nullu, LURE, Woodpecker and HALVA.** Not taken: two decoding-time methods, one released training-time model and the optional M5 cover the three families a reviewer will name, within one GPU's budget.
- **Tier-3 rows of F01, F02 and F05.** Not taken, decided now (CC-525): at tier 3 this erratum adds only the interval of the registered tier-3 statistic ρ (E-B8 R-a). E-B1, E-B2 and E-B4 have their rows and tests at tier 2, which shares tier 3's population (E-A.2 item 7); no later panel may add them at tier 3.

### E-D.3 Last commit point of each item

| Item | Last point at which it must be committed |
|---|---|
| E-B1 j\* rule and tier-1 rows; E-B2 tier-1 row; E-B3 transfer ratio, new students and T-4 (ERRATUM_O31_4 E4-4); E-B4 (all); E-B5; E-B6; E-B7; E-B8 R-d to R-g | before the first G3 output |
| keep or drop of each module M1 to M5 | before the first G3 output |
| E-B1 T-1 to T-3; E-B2 tier-2 row; E-B8 R-a and R-b | before the first T2 output |

This erratum is committed as one file before the first G3 output.

## E-E. Text left as it was
Everything else in the prereg, ERRATUM_O31_1, ERRATUM_O31_2, ERRATUM_O31_3, ERRATUM_O31_4 and COMPUTE_PLAN v3 is unchanged. COMPUTE_ADDENDUM.tsv adds planned GPU-hours and caps for the new jobs only. This erratum is not the tier-2 amendment that COMPUTE_PLAN's T2 row requires; that amendment may not change any item here.
