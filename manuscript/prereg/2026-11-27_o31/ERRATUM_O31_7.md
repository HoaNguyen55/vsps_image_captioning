# ERRATUM O31-7 to PREREG_DRAFT_O31_v3.md (5b33480b), ERRATUM_O31_1.md (91108b81), ERRATUM_O31_2.md (817eac8f), ERRATUM_O31_3.md (979486bf), COMPUTE_PLAN_O31_v3.md (7557ca3b), ERRATUM_O31_4.md (0a0bd365), ERRATUM_O31_5.md (ababc533) and ERRATUM_O31_6.md (22b5ad23)

**Status.** Written on 2026-11-28; read and amended by ruling CC-533 (2026-11-28), which also ruled the computational details drafted for E7-17 and registered those it adopted. This file is committed before the first G3 output. Nothing in it has run. It registers the clarification of two computational details of T-4 that ruling CC-530 (ruling 3) wrote; the items of the triage of the second adversarial review (`TRIAGE.tsv` and `E7_CANDIDATES.md`, folder SHA256SUMS 42af0afd) that the triage marks allowed as text or as descriptive rows; three optional modules (M7 to M9) of about 3 GPU-hours in all; one section reserved to the investigator (E7-15), which binds only on his recorded yes; what a work read in full after ERRATUM_O31_6 takes from the study (E7-13 (d), arXiv 2611.23179); and eleven computational details left open by ERRATUM_O31_5 and ERRATUM_O31_6 (E7-17).

**State of the study when this is committed.** At the commit of ERRATUM_O31_6, by its line 5: P0r had run, launched 2026-11-28T11:33:56Z (its preview `k0.json` exists on the test computer and, since 11:58:38Z, as a pulled copy on the laptop); the §3.5 pass had run (kv, feats and pass, the last at 2026-11-28T12:11:35Z); G1 had run in part, launched 2026-11-28T12:18:27Z, with its stage-1 step in progress and its probe step not started; G2 and P1 had not run; no G3 output existed. At the commit of this erratum: P0r: run, launched 2026-11-28T11:33:56Z, LOG OPS-1128co-o31-p0r (the preview k0.json exists on the test computer and, since 11:58:38Z, as a pulled copy on the laptop); §3.5 pass: run and complete (kv 2026-11-28T05:18:19Z; feats launched 2026-11-28T12:03:44Z and 12:07:16Z; pass 2026-11-28T12:11:35Z), LOG OPS-1128cq-o31-stop5-pause; G1: run, launched 2026-11-28T12:18:27Z and ended 2026-11-28T14:33Z (stage-1 for the 69 images and their Vintern probes; its outputs were pulled to the laptop at 14:34Z, after the last write of this erratum's draft at 13:30Z), LOG OPS-1128df-o31-stop6-go; G2: launched 2026-11-28T15:05:42Z and stopped at about 2026-11-28T15:34:58Z by an out-of-memory fault in the batch-parity phase of its first 50 images, with no output (no smoke.json, no shard, no probe row), LOG OPS-1128dg-o31-g2-oom; not relaunched at this commit; P1: not run; no G3 output exists. P0r's preview exists. It was not read for any choice in this erratum, and no value of it is used, quoted or conditioned on here.

**What reads what.**
- E7-1 is the text of ruling CC-530; it reads no output. Its two readings are taken from registered text (ERRATUM_O31_4 E4-7; PREREG §6.3; ERRATUM_O31_1 E9).
- E7-2, E7-3, E7-4 and E7-11 read the registered decodes of S0, S0-two, S0-trunc, S1, S2 and the E-B6 arms (G3, G4 and T2), and the human references of UIT-ViIC test 231.
- E7-5, E7-6, E7-7 and E7-13 are text and read no output of this study; E7-13 (d) reads one saved public full text (arXiv 2611.23179v1).
- E7-17 is text; each reading it fixes governs a row or record when that row or record is computed, and reads nothing now.
- E7-8 (a) and E7-9 PR-0′ are arithmetic over assumed values and read no data. E7-8 (b) reads what ERRATUM_O31_4 E4-3 and E4-7 already compute (`ops5.json` and the T-4 components), only if `ops5.json` says IDENTIFIED. E7-9 PR-1′ reads the seed-42 G3 decodes on UIT-ViIC test 231.
- E7-10 reads the image ids of the official COCO-2017 train split and the E-B5 tables.
- E7-12 reads the OP\* store by its identity in the decision of P1's `k0.json` (its rows and its sha256) and the recorded FAIR verdicts of the stage-1 records.
- Modules M7 to M9 (E7-14) read OP\*'s family set and thresholds by identity, the P-a and P-b proposition sets of E-B5, the registered comparator settings and the seed-42 adapters of S1 and S2.
- E7-15, on a recorded yes only, reads the registered tier-3 decodes of S0 and S2 at the registered tier-3 look.

No constant, threshold, seed, bin edge, word list or choice in this erratum is set from any output of P0r, the §3.5 pass, G1, G2 or P1. Rules here read gate quantities only as the committed errata already do: OP\* and OP_mid by their identity in the decision of P1's `k0.json` (as E-B2, E-B5, E-B6 and M2 do, ERRATUM_O31_5 l.7, and as M6 does, ERRATUM_O31_6 l.210), and OP_25, OP_75 and IDENTIFIED through `ops5.json` only (ERRATUM_O31_4 E4-4). Where a row reads a G1 or G2 output (a stage-1 record, a probe table, a store built from them), it reads it as an input after it exists, as K0 and E-B6 do; no rule, constant or branch here was set from such an output. No rule reads P0r's preview. Every constant is quoted from a text committed before the preview existed, or is fixed here and is free of any gate value by construction (each item says which). The writer of this erratum opened no `k0.json`, no store, caption, probe, decode or test file, no file of the investigator's PC and no session record of a run.

**What it changes.**
- E7-1 fixes two computational details of T-4 (the denominator of V_k; a replicate without gold), in the words of ruling CC-530.
- E7-2 registers a disclosure printed beside T-3 in every case, and count-matched rows of S2 against S0-two and S0-trunc.
- E7-3 registers T-1's quantities by number of matched classes, as description.
- E7-4 replaces the words of three result-triggered wording rules of ERRATUM_O31_5 (l.400, l.436, l.533) whose triggers were undefined, each by a reading under which the rule fires at least as often as under any reading of the old words.
- E7-5 adds rows 32 to 43 to the never-write list of ERRATUM_O31_6 E6-3, among them the allowed form of a multiplicity guard on the two readings that license positive wording (ERRATUM_O31_5 l.342 and l.588), and a reporting row R-h that lists every registered inferential statement.
- E7-6 defines "the summary of results" and adds a verdict sentence to the abstract.
- E7-7 fixes what the paper claims if tier 3 does not run, without changing any gate.
- E7-8 to E7-12 add descriptive rows at no GPU cost.
- E7-13 names the further prior works that the paper must cite and the works that must be read in full before the paper draft.
- E7-14 adds three optional modules, M7 to M9, each with its own job and cap outside every registered cap.
- E7-13 (d) registers what a work read in full after ERRATUM_O31_6 (arXiv 2611.23179) takes from the study, replaces one sentence of the scope statement E6-2 (ERRATUM_O31_6 l.58) that became misleading, and adds a paragraph and citations to it.
- E7-17 fixes eleven computational details that ERRATUM_O31_5 and ERRATUM_O31_6 leave open, in the texts that ruling CC-533 adopted.
- E7-15 is reserved to the investigator: the replication of T-1 and T-2 at tier 3, in a separate family of two, with a combining rule. It binds only on his recorded yes before the first G3 output, and is otherwise void.

**What it does not change.** No hypothesis, threshold, margin, seed, set, role of a set, grid, gate, estimand, registered statistic, family, member of a family, cap of a registered or earlier added job, or stop rule. Family T keeps its four members, T-1 to T-4, with Holm's correction inside T (ERRATUM_O31_5 E-B1); no member is added, removed, replaced or re-weighted (ERRATUM_O31_4 E4-7). E7-1 fixes how two quantities of T-4's registered form are computed; it changes neither Δ_k, z_k, p_k nor p_T4. The one exception to this paragraph is E7-15, and only on the investigator's recorded yes: it then adds a separate family T3 of two registered statistics read at the tier-3 look, and replaces the words of ERRATUM_O31_5 that bar them (l.102, l.147, l.157 and l.749); it still changes no hypothesis, threshold, gate, member of T or stop rule. Without that yes, E7-15 is void and this paragraph holds without exception. E7-18 lists what stays.

**Why now.** ERRATUM_O31_5 E-B3 requires T-4 to be registered before the first G3 output (l.247), and ruling CC-530 found its form incomplete in two details (ruling 3). The rows of E7-2 to E7-4 and E7-9 to E7-12 read G3 decodes, so their forms must exist before those decodes; F11 may be added as a module only if committed before the first G3 output (ERRATUM_O31_5 l.744); the keep or drop answers of the modules and the investigator's answer on E7-15 are due by the same point. After the first G3 output a student result could shape any of them.

**Sources.** The candidate texts come from `E7_CANDIDATES.md` and `TRIAGE.tsv` (triage folder SHA256SUMS 42af0afd), written against the sixth-erratum draft; every line number below was re-derived on the committed files: PREREG_DRAFT_O31_v3.md 5b33480b ("PREREG"), ERRATUM_O31_1.md 91108b81, ERRATUM_O31_2.md 817eac8f, COMPUTE_PLAN_O31_v3.md 7557ca3b, DIRECTION_NOTE_O31_v2.md 1705f523, ERRATUM_O31_4.md 0a0bd365, ERRATUM_O31_5.md ababc533 and ERRATUM_O31_6.md 22b5ad23. Statements about prior works rest on the saved texts listed in `PRIOR_WORK_NEW.tsv` of the second review, with how each was read; a quote used here was checked in the saved text. The texts of E7-17 are those that ruling CC-533 adopted. A line number written without a file name ("l.N") is a line of ERRATUM_O31_5 (ababc533), except where the same sentence names another file or a section of PREREG (§), whose line it then is. Where `CODE_NEEDS_E7.tsv` or `COMPUTE_ADDENDUM_E7.tsv` differ from this erratum, this erratum governs. ERRATUM_O31_4, ERRATUM_O31_5 and ERRATUM_O31_6 govern over this erratum, except for the words that E7-4 replaces, the sentence of ERRATUM_O31_6 l.58 that E7-13 (d) replaces, the open details that the adopted texts of E7-17 fix and, on the investigator's recorded yes only, the words that E7-15 replaces.

---

## E7-1. Two computational details of T-4 (ERRATUM_O31_4 E4-7), clarified
ERRATUM_O31_4 E4-7 does not state the denominator of V_k, or how a replicate without gold enters V_k. Both are fixed here by readings taken from registered text. This changes no hypothesis, threshold, margin, seed, set, grid, gate, estimand, family, membership or stop rule. Δ_k, z_k, p_k and p_T4 are unchanged.
- V_k is the sample variance of the B = 10,000 replicate values of Δ_k, with B − 1 = 9,999 in the denominator. This is the convention E4-7 states for σ²_seed. It is the larger of the two readings, by the factor B / (B − 1). For Δ_k > 0 it gives the larger p_k; for Δ_k ≤ 0, p_k ≥ 0.5 under either reading. So T-4 can pass under this reading only if it also passes under the other.
- A replicate in which Σ_i |G_i| over the resampled images is 0 has no R at any of the five points (§6.3 'Ratios'; ERRATUM_O31_1 E9). If one or more of the 10,000 replicates is undefined, T-4 is NOT_IDENTIFIED. This extends E4-7's rule for a zero denominator (read as 'at any k' by ruling CC-526 N9) to the denominator Σ_i |G_i| of R. T-4 then enters its family with p = 1, and the number of undefined replicates is reported. The same holds if Σ_i |G_i| over the full tier-2 list is 0.
- Neither reading uses a value of any k0.json (P0r's preview included), of the §3.5 pass, or of G1, G2, P1 or G3. The tier-2 decodes on which T-4 is computed do not exist. Under each reading T-4 is no more likely to pass than under the other.

---

## E7-2. A disclosure beside T-3, and count-matched rows against the two length controls (R2-04; F01)

**(i) Disclosure (registered text).** The following sentence is printed beside T-3 in every case, after a PASS as well as after a FAIL, a NOT_IDENTIFIED or a NOT RUN:
> "T-3 compares hallucinated objects per caption, a count per caption, between the student and the base model under a fixed two-sentence prompt. That prompt is not matched to the student in length or in the number of objects mentioned. At equal precision per mentioned object, the system that names fewer objects has the lower count and also the lower object recall; T-3 requires the student to have both the higher recall and the lower count. The comparison at a matched number of mentioned objects is T-1."

After a FAIL of T-3, this sentence follows the sentence that ERRATUM_O31_5 l.164 requires and never replaces or qualifies it. Neither this sentence nor the rows of (ii) may be cited in the title, the abstract or the conclusion to discount a FAIL of T-2 or T-3 (row 37 of E7-5).

**(ii) Descriptive rows.**
- **Question:** At a matched number of mentioned classes, is S2 more precise than each length-controlled version of S0?
- **Metric and unit:** the image. CMP and CMR (ERRATUM_O31_5 E-B1 (a) and (a′), l.136-139) with X = S2 and Y = S0-two, and with X = S2 and Y = S0-trunc. On each image k_i = min(m_S2,i, m_Y,i), and each system keeps its first k_i distinct classes in order of first mention. Images with k_i = 0 are left out of both sums, counted and reported.
- **Also printed beside T-2 and T-3:** for each of S2, S0-trunc and S0-two, the mean distinct classes per caption and CHAIR_i, and the paired differences of mean distinct classes per caption (S2 − S0-trunc, S2 − S0-two) with their intervals. These are quantities that ERRATUM_O31_5 l.146 already registers; only their placement and the two differences are new.
- **Data and role:** tier 1 (KTVIC test 558 with the 113-noun lexicon on references; UIT-ViIC test 231 with instance gold, G-2) at seed 42; tier 2 (the registered tier-2 list, instance gold, ERRATUM_O31_1 E11). At tier 2, S2's three seeds are paired with the single S0-type decode as G-4 states. Never tier 3.
- **Decision rule:** descriptive, no rule. Paired 95 % intervals (G-4). **Family:** none.
- **Settings fixed now:** none new. The cut rule, j\* and the prompt are those of E-B1 (l.141-145).
- **Reads:** the registered decodes of S0, S0-two and S2, and S0-trunc (CPU from S0).
- **Against the claim:** none of its own; printed in every case.
- **GPU-hours:** 0. **New code:** yes (CODE_NEEDS_E7 C36).
- **Why it is safe to register after the gate preview, and before G1 and G2 end:** it fixes no constant, reads no `k0.json` value and no store, and reads no output of G1 or G2; every input is a registered decode that does not exist yet. T-3's form, its membership of family T and l.164 are unchanged. A replacement of T-3 by a count-matched form would change a member of family T (ERRATUM_O31_5 l.154; ERRATUM_O31_6 l.17) and is not offered (ruling CC-533).

---

## E7-3. T-1's quantities by number of matched classes (R2-03; F01)

- **Question:** If T-1 fails, is S2 equal to S0 only at its first, most salient classes, or at every number of matched classes?
- **Metric and unit:** for T-1's pairing (X = S2, Y = S0; E-B1 (a)), CMP_S2, CMP_S0, their difference and CMR_S2 and CMR_S0, computed separately over three bins of k_i: k_i = 1, k_i = 2 and k_i ≥ 3.
  - At tier 1 (seed 42), the bin of an image is set by its k_i.
  - At tier 2, with three seeds, the bin is set per (image, seed pair) cell from that pair's k_ij (S2 seed j paired with S0's single decode, G-4). Each bin sums TP and k over its cells. The bootstrap resamples images, each image carrying its three cells.
  - The number of images (and, at tier 2, of cells) in each bin is reported.
- **Data and role:** tier 1 (KTVIC test 558, UIT-ViIC test 231) and tier 2 (the registered tier-2 list). Never tier 3.
- **Decision rule:** descriptive, no rule. Paired 95 % intervals within each bin, recomputed in every replicate from the resampled images (G-4). A replicate in which a bin is empty is undefined for that bin; it is counted, reported and left out of that bin's interval (ERRATUM_O31_1 E9). **Family:** none.
- **Against the claim:** none of its own. If T-1 FAILs, ERRATUM_O31_5 l.163 applies unchanged and the bins are printed beside it. They are never cited in the title, the abstract or the conclusion to qualify the FAIL (row 37 of E7-5).
- **Settings fixed now:** the bin edges 1, 2 and 3 or more. They count classes mentioned in captions; no `k0.json` holds such a count.
- **Reads:** the registered decodes of S0 and S2. **GPU-hours:** 0. **New code:** yes (C37).
- **Why it is safe to register after the gate preview, and before G1 and G2 end:** its one constant is a count of mentioned classes, which no gate file holds; it reads no output of G1, G2 or P1, and no decode it reads exists yet.

---

## E7-4. Three result-triggered rules whose triggers were undefined (R2-22, R2-16)

Three wording rules of ERRATUM_O31_5 turn on a word that no committed text defines. Each is replaced below by a reading under which the rule fires at least as often as under any reading of the old words: where the old word sets a bar, the new text sets the lowest bar that the word can carry, and it uses point estimates, not intervals, where the old text names no interval. No other trigger changes. Each OLD string occurs exactly once in ababc533 (ruling CC-533).

**(a) "explains most" (E-B6, l.400).**
- OLD: `while the budget effect explains most of S2 − S1, the paper states that the recall gain comes from the budget rule, not from the verifier.`
- NEW: `while the budget effect explains most of S2 − S1, the paper states that the recall gain comes from the budget rule, not from the verifier, and names the set. The condition is evaluated on each tier-1 set separately, with both of its parts on the same set. "The budget effect explains most of S2 − S1" holds on a set iff the point estimate of S2 − S1 is above 0 and, in at least one of the two decompositions S2 − S1 = (S2 − A-3) + (A-3 − S1) and S2 − S1 = (A-8 − S1) + (S2 − A-8), the point estimate of the budget contrast (S2 − A-3 in the first, A-8 − S1 in the second) is at least one half of the point estimate of S2 − S1 (ERRATUM_O31_7 E7-4). If the point estimate of S2 − S1 is not above 0 on a set, the paper states that S2 shows no recall gain over S1 on that set.`
- Why this reading: "most" cannot mean less than one half, so "at least one half" fires at least as often as any reading of it; "at least one of the two decompositions" fires whenever either does; point estimates fire at least as often as any interval condition. The other half of the condition (the verifier effect's interval includes 0 at both budgets) is unchanged. The review's alternative, which also requires the budget effect's interval to exclude 0, would make the sentence fire less often and is not offered.

**(b) "far below 0.98" (E-B7, l.436).**
- OLD: `a projected P(H2) far below 0.98 is reported in the decision record`
- NEW: `a projected P(H2) below 0.98 is reported in the decision record`
- Why: every reading of "far below 0.98" is a subset of "below 0.98".

**(c) "a large share" (E-B8 R-g, l.533).**
- OLD: `a large share for S0 means S0 is already truncated by the cap. This is stated beside E-B1.`
- NEW: `the share for S0 is printed beside E-B1 in every case, and whenever it is above 0 the sentence "S0 reaches the 160-token cap in x % of its captions on this set, and these captions are cut by the cap", with x the share in per cent, is printed with it (ERRATUM_O31_7 E7-4).`
- Why: every reading of "a large share" is a subset of "a share above 0", and the sentence keeps the old meaning (those captions of S0 are cut by the cap).

**Why it is safe to register after the gate preview, and before G1 and G2 end:** text only. Its one number, one half, is the plain meaning of "most"; it holds no gate value and reads no output of G1, G2 or P1. **GPU-hours:** 0. **New code:** yes (C38, the three triggers as computed conditions).

---

## E7-5. Further rows of the never-write list, and a reporting row of every inferential statement (R2-22, R2-19, R2-27; F03 (c), F11)

**(a) Rows 32 to 43 of the list of ERRATUM_O31_6 E6-3.** They bind as that list binds: every paper text and cover letter of this study; a sentence on this list is BLOCKING at the read of that text, as K6 is. Rows 1 to 31 stay as committed.

| # | Never write | Why (locator) | Allowed instead |
|---|---|---|---|
| 32 | In the title, the abstract or the conclusion, any sentence whose only licence is the descriptive reading of ERRATUM_O31_5 l.342 ("favouring VR-O31 over rule X") or of l.588 ("the effect replicates on a second backbone") | these readings use uncorrected intervals, and l.157 claims no error rate across families; a sentence licensed by a registered verdict (for example H4 PASS) is not affected; E6-3 row 15 and G-6 (l.128) already limit the l.342 wording, and this row extends the limit to every rule X and to l.588 | the sentence in the results section, under row 33 and E6-3 row 15 |
| 33 | Anywhere, a sentence licensed by ERRATUM_O31_5 l.342 or l.588 without, in the same sentence, the words "a descriptive reading, not corrected for multiple comparisons" | as row 32 | the licensed sentence with those words |
| 34 | Any sentence that calls this work the first hallucination study, dataset, benchmark or detector for Vietnamese | ViHallu (arXiv 2601.04711, abstract: "the first large-scale shared task for detecting hallucinations in Vietnamese LLMs"; text only; read as an abstract) | describe the resource gap (E6-3 row 2) |
| 35 | Vietnamese results of S2 and English results of C-SEN in one table row or one comparative sentence | ERRATUM_O31_5 l.259-261: C-SEN meets S2 in English at tiers 1 and 2; its Vietnamese row is "outside the model's training language" | the English comparison (S2, C-SEN and S0, all decoded in English) in its own table, so labelled |
| 36 | "the baselines are the state of the art of 2026", "the strongest available baselines", or similar | the comparators are VCD (2024), DeCo (2025) and the SENTINEL adapter; newer methods on the same base model exist (SAKED, CIM, ReflectCAP, REVERSE; E7-13); E6-3 row 28 | "decoding-time methods that recent work still uses as baselines", citing the works of E7-13 that use them |
| 37 | "T-3 failed by construction", "T-3 was unfair", or the disclosure or rows of E7-2 or the bins of E7-3 cited in the title, the abstract or the conclusion to discount a FAIL of T-1, T-2 or T-3 | T-3 is a registered test whose construction was stated before any output (ERRATUM_O31_5 l.145, l.152); l.163-164; G-6 (l.128) | the E7-2 disclosure beside T-3, after the l.164 sentence |
| 38 | That T-4 failed "for lack of power", or that the order "is real but underpowered", or any reading of the rows of E7-8 as a verdict | T-4's verdict is ERRATUM_O31_4 E4-7's alone; the rows of E7-8 are descriptive | the verdict, with E7-8 (a) and (b) printed beside it |
| 39 | If tier 3 does not run: "dev-confirmed", "nearly confirmed", "would have passed at tier 3"; that the registered claim of PREREG §1 holds, is supported, is indicated or is suggested by a tier-1 or tier-2 result; the headline sentence of PREREG l.144 in any form | PREREG l.14-16, l.144, l.177; ERRATUM_O31_5 l.739 (F03 (c) not taken); K6 | the wording of E7-7 |
| 40 | For the rows of module M9: "mechanism", "cause", "the model learns to perceive", or any account of what is learned inside the network | M9 is a descriptive probe of the students' answers with no test (E7-14) | "a descriptive probe of the students' own yes/no answers" |
| 41 | That a proposition counted in E7-12 is wrong, an error or a hallucination | E7-12 counts exposure, not error; no human label touches a training proposition (E6-3 row 26) | "accepted by the O31 rule and not by FAIR's recorded verdicts" |
| 42 | That the detectors or CLIP "never saw", "were not trained on" or are "unseen" on the images of E7-10, unless a saved source states the training data of that model | no saved file states YOLO's or Grounding DINO's training data (ERRATUM_O31_6 l.231); E7-10 defines its subset by the COCO-2017 split only | "the images of UIT-ViIC test 231 outside the official COCO-2017 train split" |
| 43 | "The first" or "unlike prior work" for asking whether a hallucination gain is more than saying less or stopping earlier, or for comparing a trained model with its base model at matched recall, with the base model's stopping or sentence-cut curve, with the base model under a shorter prompt, or with the base caption truncated per image to the trained model's object count; "recall-controlled evaluation" or "stopping-controlled gain" as this study's terms or method; any sentence that carries a result of Say Less, Hallucinate Less? over to supervised fine-tuning, to Qwen2.5-VL, to Vietnamese or to this study's systems, or that cites it as predicting a verdict of T-1 to T-3 | Say Less, Hallucinate Less? (arXiv 2611.23179; Sec. 2, Tab. 2; App. C, Tab. C1; E7-13 (d)): preference-optimised LLaVA-1.5-7B checkpoints, English, greedy decoding, one prompt (Sec. 7) | "Say Less, Hallucinate Less? asks this question for preference-optimised LLaVA-1.5-7B checkpoints in English; this study asks it for supervised fine-tuning on verified propositions in Vietnamese" |

Rows 32 and 33 are the allowed form of a multiplicity guard on the two readings that license positive wording. The numeric conditions of l.342 (the interval lower bound of the RT difference above 0; the interval upper bound of the FA difference at most +5.0 points, applied to VR-EFUF as ERRATUM_O31_6 E6-7.7 states) and of l.588 (ρ_G point at least 0.50; the interval upper bound of D_G below 0) are unchanged. A Holm condition on these readings would change committed numeric conditions and is not offered (ruling CC-533).

The "why" column of E6-3 row 5 ("frontier" in any form) also rests on ReflectCAP (arXiv 2604.12357, saved text l.63: "ReflectCAP reaches the Pareto frontier of the trade-off between factuality and coverage"), a method on the same base model. This is an addition to the reasons of row 5; its words are unchanged.

**(b) Reporting row R-h (methods section, or the supplement with a pointer from the methods section).** One table lists every registered inferential statement and every registered reading that licenses or forces a sentence, each with its file and line, and states for each whether an error rate is controlled for it:
- the primary family, H1 ∧ H2 (PREREG §6.1, intersection–union): controlled;
- the secondary family, H3, H4, H5a and H5b (PREREG §6.2-6.3, Holm): controlled;
- family T, T-1 to T-4 (ERRATUM_O31_5 E-B1 and E-B3, Holm): controlled;
- family T3, only if E7-15 binds: controlled;
- the descriptive readings and result-triggered wording rules, none controlled:
  - PREREG l.152 (T-a "reached") and l.184 (A-1's slope prediction);
  - ERRATUM_O31_4 l.43 (an edge OP\* stated as a limitation);
  - ERRATUM_O31_5 l.200, l.235, l.293, l.342, l.354, l.355, l.400 (as E7-4 defines it), l.436 (as E7-4 replaces it), l.455, l.469, l.533 (as E7-4 replaces it), l.571, l.588, l.602, l.632, l.666 and l.695;
  - ERRATUM_O31_6 l.201 (M6), and ERRATUM_O31_6 l.342 (E6-7.7, which applies the reading of ERRATUM_O31_5 l.342 to VR-EFUF only and makes the statement of ERRATUM_O31_5 l.354 if either EFUF row meets its condition);
  - this erratum: E7-7, E7-9 (PR-1′ upper bound below 0.98) and M8 (E7-14).

The table is printed in every case. It reads no output. **GPU-hours:** 0.

**Why it is safe to register after the gate preview, and before G1 and G2 end:** text and a list only; it fixes no number and reads no output of P0r, G1, G2 or P1.

---

## E7-6. "The summary of results" defined, and a verdict sentence in the abstract (R2-26)

- Wherever ERRATUM_O31_5 or a later erratum requires a statement "in its summary of results" (for example l.164 and l.293), the summary of results is a subsection with that title at the start of the results section of the main text, not in the supplement.
- The abstract has one sentence that gives, for H1 ∧ H2 and for each member of family T (and of family T3 if E7-15 binds), its verdict (PASS, FAIL, UNDERPOWERED, NOT_IDENTIFIED or NOT RUN, or a plain-language equivalent that keeps each distinction) and the set on which it was read, named as E6-3 row 13 allows.
- Why it is allowed: it adds an obligation and moves nothing out of view (K6, PREREG l.201). It reads no output and holds no gate value. **GPU-hours:** 0.

---

## E7-7. The claim form if tier 3 does not run (R2-23, R2-24; F03, F16)

The registered claim is stated for the tier-3 images (PREREG §1, l.14-16), and its headline sentence (§6.1, l.144) is the tier-3 reading of H1 ∧ H2. This section fixes what the paper claims if tier 3 does not run, whatever the reason: no set is assigned (branch 3 of §3.4, PREREG l.69), K1 fires (PREREG l.196), K2 fires (PREREG l.197; §7, l.177), the tier-3 panel does not approve the look (PREREG l.178), or the look is not made. It changes no gate, threshold, branch rule or stop rule; it only narrows what the paper may write.

1. The paper states, in its summary of results (E7-6) and in its abstract, that the registered claim of §1 was not tested on a one-look set, and names the cause: no set assigned (Q1, PREREG l.248), K1, K2 with the value of P(PASS), or no approved look.
2. The headline sentence of PREREG l.144 is not written in any form, with or without a qualifier (row 39 of E7-5).
3. Any reading of H1 or H2 at tier 1 or tier 2 is reported as a development result on the set on which it was read ("reported briefly as a dev result", PREREG l.177), with P(PASS) beside it where the rehearsal ran, and never as support for the claim of §1.
4. Family T keeps its registered wording: "a registered test on the rehearsal set (Karpathy test, used in FAIR 2026)" (ERRATUM_O31_5 l.157; E6-3 row 13).
5. H4, the one registered test of line (a), is a tier-3 test (PREREG l.148). The paper states that it was not run; line (a) is then a development measurement on UIT-ViIC test 231 and, against the earlier FAIR rule, a rehearsal on the base model's mentions of the Karpathy test images.
6. If K1 fires, ERRATUM_O31_6 E6-2 (Conditions) governs: the paper is the brief development report of §9.

**Why it is safe to register after the gate preview, and before G1 and G2 end:** text only, reading no output; it can only remove positive wording. **GPU-hours:** 0.

---

## E7-8. T-4: power arithmetic, the interval of the seed variance, the components and the identities of the five points (R2-14, R2-15; F04)

**(a) PR-T4, fixed now (arithmetic only; it reads no data).** Under T-4's form (ERRATUM_O31_4 E4-7), pair k passes its own step iff z_k = Δ_k / sqrt(V_k + 2σ²_seed) ≥ z\*. Under Holm with four members, z\* is 1.645 (p < 0.05) if T-4 holds the largest of the four ordered p-values and every other member has passed, and 2.241 (p < 0.0125) if it holds the smallest. Since p_T4 = max_k p_k, every adjacent pair must reach z\*. The student-recall gap Δ (points of R) needed at every adjacent pair:

| V_k (SE of Δ_k) | σ_seed | needed Δ at z\* = 1.645 | needed Δ at z\* = 2.241 |
|---|---|---|---|
| 0.09 (0.3) | 0.5 | 1.26 | 1.72 |
| 0.09 (0.3) | 1.0 | 2.38 | 3.24 |
| 0.16 (0.4) | 0.5 | 1.34 | 1.82 |
| 0.16 (0.4) | 1.0 | 2.42 | 3.29 |
| 0.25 (0.5) | 0.5 | 1.42 | 1.94 |
| 0.25 (0.5) | 1.0 | 2.47 | 3.36 |

The values of V_k and σ_seed are round assumed values that no output supplied. The table is not converted into gaps of supervision recall, because that would need the R_sup spacing of the five points, which only `k0.json` files hold.

**(b) Rows at tier 2, only if `ops5.json` says IDENTIFIED and T-4 is computed (ERRATUM_O31_4 E4-4).**
- The 95 % interval of σ²_seed from its 4 degrees of freedom (two sample variances with 2 each, ERRATUM_O31_4 l.55): [4 s² / χ²(0.975; 4), 4 s² / χ²(0.025; 4)] = [0.359 s², 8.257 s²], where s² is the registered σ²_seed. z_k is recomputed with σ²_seed at each bound.
- The four Δ_k, V_k, z_k and p_k that E4-7 computes, with the pair that contains S1 marked.
- For each of the five points, beside the R_sup, P_sup and store sha256 that ERRATUM_O31_4 E4-3 already reports: for OP_strict, "FAIR's recorded verdicts, B = 9" (ERRATUM_O31_4 l.16); for the other four, the family set, τ_acc and τ_rej of the grid point that `ops5.json` (OP_25, OP_75) or the decision of P1's `k0.json` (OP_mid, OP\*) names, in the grid order of ERRATUM_O31_1 E7 (l.52).

**Decision rule.** None. The z values at the bounds are not a verdict; T-4's verdict is E4-7's alone. No statistic is computed over a subset of the pairs: a maximum p over the three O31 pairs would be a second test across the five points, which E4-7 forbids.

**Against the claim.** If T-4 FAILs, the paper states the verdict and prints (a) and (b) beside it (row 38 of E7-5).

**Why it is safe to register after the gate preview, and before G1 and G2 end:** (a) uses round assumed values and is deliberately not translated into R_sup gaps; P0r's preview holds R_sup values that bear on T-4's power (ERRATUM_O31_5 l.9), and none is used. (b) prints what E4-3 and E4-7 already compute or name, through `ops5.json` only as E4-4 allows, and reads no G1 or G2 output. No member of family T is added, removed or re-weighted. **GPU-hours:** 0. **New code:** yes (C39).

---

## E7-9. Power reading for H1 and for the joint gate, advisory (extends E-B7; R2-24, F03)

**PR-0′ (fixed now; arithmetic only; reads no data).** H1 passes on a point bar (ρ ≥ 0.50) together with an interval bar on R_S2 − R_S1 (PREREG l.137); PR-0′ uses the point bar only, so it is an upper bound on P(H1). Under a normal approximation, the share of outer draws with ρ̂ ≥ 0.50 is Φ((ρ − 0.50) / SE_ρ). A share of 0.98 needs ρ ≥ 0.50 + 2.054 SE_ρ, and 0.99 needs ρ ≥ 0.50 + 2.326 SE_ρ. (This agrees with ERRATUM_O31_5 l.411: an interval bar needs 1.96 + 2.054 = 4.01 SE.) With FAIR's COCO values (R_S0 63.3, R_S1 45.9; PREREG l.64; their gold is instances ∪ references, while H1 uses instance gold, ERRATUM_O31_1 E11, l.70), R_S2 = 45.9 + 17.4 ρ:

| SE_ρ at n = 4,224 | ρ for 0.98 | R_S2 for 0.98 | ρ for 0.99 | R_S2 for 0.99 |
|---|---|---|---|---|
| 0.02 | 0.541 | 55.3 | 0.547 | 55.4 |
| 0.03 | 0.562 | 55.7 | 0.570 | 55.8 |
| 0.04 | 0.582 | 56.0 | 0.593 | 56.2 |
| 0.05 | 0.603 | 56.4 | 0.616 | 56.6 |

The joint gate needs P(H1 ∧ H2) ≥ 0.98 (PREREG l.174). It is met if each of P(H1) and P(H2) is at least 0.99, because P(H1 ∧ H2) ≥ P(H1) + P(H2) − 1, and it fails if either is below 0.98. The design expectation of COCO recall, about 52 to 57 (DIRECTION_NOTE_O31_v2 l.64, an opinion), gives ρ of about 0.35 to 0.64 at FAIR's values; the R_S2 values above lie at its top.

**PR-1′ (at the G3 read).**
- From the seed-42 G3 decodes of S0, S1 and S2 on UIT-ViIC test 231, with COCO-80 instance gold only: ρ̂ and SE_231, the standard deviation (denominator B_def − 1) of ρ over the defined replicates of the shared index matrix (G-4; a replicate with R_S0 − R_S1 ≤ 0 is undefined, as E-B8 R-a states, l.449), and SE_4224 = SE_231 × sqrt(231 / 4,224).
- P(H1) = Φ((ρ̂ − 0.50) / SE_4224), the point-bar projection.
- With E-B7's projected P(H2) (l.426): the bounds max(0, P(H1) + P(H2) − 1) ≤ P(H1 ∧ H2) ≤ min(P(H1), P(H2)).
- If R̂_S0 − R̂_S1 < 2.0 on the 231, PR-1′ is NOT_IDENTIFIED (as H1 itself, PREREG l.138).

**Decision rule.** Descriptive and advisory, as E-B7 (l.431-433). It starts, stops and waives nothing; K1 and K2 remain the only registered stops. The assumptions of l.433 apply and are stated, together with the gold difference of FAIR's values.

**Against the claim.** If the upper bound min(P(H1), P(H2)) is below 0.98, this is reported in the decision record and, if the line stops, in the paper.

**Why it is safe to register after the gate preview, and before G1 and G2 end:** arithmetic over values committed in PREREG and the direction note before any `k0.json` existed, and the registered G3 decodes only; no `k0.json` value and no output of G1 or G2 enters. **GPU-hours:** 0. **New code:** yes (C40; it extends E-B7's calculator).

---

## E7-10. Verifier rows outside the COCO-2017 training images (R2-08; F13)

- **Question:** Do the E-B5 rows change on the images that are not in the official COCO-2017 train split?
- **Data:** the image ids of the official COCO-2017 train split, read from the `images` array of that split's instance annotation file. The file is pinned by sha256 at pin time and its licence checked (PREREG §10, l.217; ERRATUM_O31_5 l.732). Only the `id` field of each entry of `images` is read; no annotation in it is read. The file stays on the laptop and never goes to the investigator's PC, because it may hold annotations of COCO val2014 images of the tier-3 set (ERRATUM_O31_5 l.103; ERRATUM_O31_2 O-H8). U = the UIT-ViIC test 231 images whose COCO id is not among those ids.
- **Metric and unit:** every E-B5 row (RT, FA, DR strict and the UNCERTAIN shares, per rule, and the single-family rows) recomputed on the propositions of U, with intervals clustered by image: each replicate resamples the 231 images with the shared index matrix and keeps those in U. The count of U is reported. If U is empty, the rows are NOT_IDENTIFIED; a replicate with no image of U is undefined (ERRATUM_O31_1 E9).
- **Data and role:** UIT-ViIC test 231 in its registered role (ERRATUM_O31_5 l.330). Never tier 3.
- **Decision rule:** descriptive, no rule. The reading of ERRATUM_O31_5 l.342 applies to the full P-b only and is never licensed by a row on U. **Family:** none.
- **Against the claim:** none of its own. The rows on U are printed beside the full rows in every case, with the count. Which data a detector or CLIP was trained on is stated only where a saved source says so (row 42 of E7-5).
- **Settings fixed now:** the split (official COCO-2017 train), the field read, the custody rule.
- **GPU-hours:** 0 (CPU). **New code:** yes (C41).
- **Why it is safe to register after the gate preview, and before G1 and G2 end:** the split is a public fact unrelated to any output of this study; no constant takes a gate value; it reads no output of G1, G2 or P1.

---

## E7-11. Negation and hedge cues near mentions (R2-18)

- **Question:** How many of the mentions that the frozen extractor counts are not plain assertions?
- **Cue list (fixed now; NFC, lower-cased, matched on whole syllables of the extractor's normalised text).**
  - Negation: "không có", "không thấy", "không phải", "không hề", "không còn", "chẳng có".
  - Hedge: "có thể", "có lẽ", "dường như", "hình như", "có vẻ", "trông như", "trông giống", "giống như".
  - An occurrence of "có thể" immediately followed by "thấy" or "nhìn" is not a cue ("có thể thấy", "có thể nhìn thấy" mean "one can see").
  - No single-syllable cue is used, because "không" alone also starts nouns such as "không khí" and "không gian".
- **Rule.** Within one sentence (the sentence rule of E-B1, ERRATUM_O31_5 l.141), split into whitespace syllables, a matched COCO-80 mention is cued iff a cue's last syllable precedes the mention's first syllable with at most four syllables between them.
- **Reported, per system and set:** the share of matched mentions that are cued, separately among mentions counted as hallucinated and among those counted as correct; h and CHAIR_i recomputed with the cued mentions removed, beside the registered h and CHAIR_i.
- **Data and role:** every Vietnamese decode at tiers 1 and 2, and the human references of UIT-ViIC test 231 (as E-B8 R-d). English rows are not covered: no English cue list is registered. Never tier 3.
- **Decision rule:** descriptive, no rule. **Family:** none. The registered h and CHAIR_i are unchanged and remain the outcome measures.
- **Against the claim:** none of its own; printed beside h for every system in every case.
- **GPU-hours:** 0. **New code:** yes (C42).
- **Why it is safe to register after the gate preview, and before G1 and G2 end:** the lists, the exclusion and the window are fixed before any decode is read; they are words of Vietnamese and a syllable count, and hold no gate value; no output of G1, G2 or P1 is read.

---

## E7-12. Exposure of S2's training targets to non-object propositions newly accepted (R2-06; F06)

- **Question:** How much of S2's detailed supervision rests on attribute, action and counting propositions that the O31 rule accepts and FAIR's recorded verdicts did not?
- **Metric and unit:** the proposition, on the training pool after the §3.5 (a) removals. For each type (entity, attribute, action, counting; spatial relations are always UNCERTAIN, PREREG §4.2):
  - (i) the number of propositions whose state at OP\* is SUPPORTED and whose recorded FAIR verdict is not SUPPORTED;
  - (ii) the number of these that the selector placed in S2's detailed targets;
  - (iii) their share among all propositions of that type in S2's detailed targets;
  - for reference, the number of selected propositions of each type in the S1 store.
- **Reads:** the OP\* store build, by its identity in the decision of P1's `k0.json`, as E-B6, M2 and M6 read it (ERRATUM_O31_5 l.7; ERRATUM_O31_6 l.210); the recorded verdicts of the stage-1 records.
- **New code:** a separate CPU replay of the OP\* store build that logs, per row, the ids of the propositions it rendered. It calls the existing store build outside `run_k0`, as the A-8 store build does (ERRATUM_O31_5 l.402). `k0.py` and `gate.run_k0` are not changed (ERRATUM_O31_4 l.34). The replay's `sft.jsonl` must be byte-identical to OP\*'s store: its sha256 must equal `sft_sha256` of `decision.op_star` in P1's `k0.json` (ERRATUM_O31_1 E5, l.44); otherwise the item is NOT RUN (C43).
- **Decision rule:** descriptive, no rule. **Family:** none. No labels: a newly accepted proposition is not thereby wrong, and the paper says so (row 41 of E7-5).
- **Against the claim:** printed in the limitations beside E-A.2 item 1 (ERRATUM_O31_5 l.63) in every case.
- **GPU-hours:** 0.
- **Why it is safe to register after the gate preview, and before G1 and G2 end:** counts only, with no constant and no branch on any `k0.json` number; OP\* enters by identity and by its store sha, as in the committed errata; the stage-1 records and probe tables are read as inputs once they exist, as K0 reads them, and no rule here was set from them; P0r's preview is not read.

---

## E7-13. Prior works that the paper must name, and works to be read in full before the paper draft (R2-27, R2-12; F17)

Parts (a) to (c) change no word of the statement of ERRATUM_O31_6 E6-2 and add nothing to the count of works read in full (23); they use the mechanism of E6-2 status (i) (ERRATUM_O31_6 l.66). Part (d) replaces one sentence of E6-2 (l.58) and adds one paragraph and four citations to it, for a work read in full after E6-2 was committed.

**(a) Works to be read in full before the paper draft, with the rule of E6-2 status (i).** SelfVal (arXiv 2601.22451v2) and the 2026 filter study (arXiv 2605.21300v1, "Reducing Object Hallucination in LVLMs via Emphasizing Image-negative Tokens") were read in sections only by the second review. Each is read in full before the paper draft. No statement of the paper rests on either before that. Either one sends the line to a K5 read if it reports (a), (b) or (c) in the form of E6-2. What the second review read in sections, to be confirmed by the full read:
- SelfVal is the nearest published analogue of the inference-time baseline S0-filter (E-B2): in its Filter-then-Aggregate variant it discards each sentence whose object score is below a threshold and then regenerates a caption from the kept candidates; its base models include Qwen2.5-VL; it uses VCD and DeCo as baselines.
- The 2026 filter study fine-tunes LLaVA-v1.5-7B after removing the data with the highest or the lowest visual dependence, beside random removal, and reports CHAIR, recall and the mean length of the kept data and of the responses.

**(b) Works the paper must name in its related work, each with how it was read** (rows of `PRIOR_WORK_NEW.tsv` of the second review): SAKED (2602.09825), LISA (2507.19110), CIM (2603.01696), ReflectCAP (2604.12357), REVERSE (2504.13169), CHAIR-DPO (2508.20181), CapMAS (2412.15484), the compact-VLM data filter (2507.20156), DBD (2406.12663), ViHallu (2601.04711), M2CQA (2602.05437), CycleCap (2603.18282), DetailVerifyBench (2604.05623), SC-Captioner (2508.06125) and ICLA (2603.00437), with SelfVal and the 2026 filter study of (a), and Say Less, Hallucinate Less? (2611.23179) of (d). None supports a negative statement until it is read in full (E6-3 rows 10 and 11). These rows are added to the table of record of prior works, with how each was read, by a later erratum before any paper text; `PRIOR_ART_O31_v4.tsv` is committed and is not changed by this erratum.

**(c) What the other works on the same base model change.** SAKED (Table 1) reports a DeCo row on Qwen2.5-VL; it may be cited as evidence that DeCo runs on that model and that others report it there, and no setting is taken from it (ERRATUM_O31_5 l.277, with the words that ERRATUM_O31_6 E6-7.7 replaced). CIM (reinforcement learning for captioning "without requiring additional annotations", run on Qwen2.5-VL-7B; saved text l.77, l.735) and ReflectCAP (inference-time notes) change no comparator, because reinforcement learning and inference-time methods are outside this study's setting (ERRATUM_O31_6 l.64: no preference or reinforcement learning, no verifier at inference); they are cited as work on the same base model and goal. ReflectCAP's "Pareto frontier" is a further reason for E6-3 row 5 (E7-5).

**(d) Say Less, Hallucinate Less? (arXiv 2611.23179v1, 17 November 2026), read in full by the writer of this erratum.** Its saved text is `research_1128/synth/src/full/2611.23179v1/html.txt` (folder SHA256SUMS 3910aa6c); the locators below are its lines ("html l.N") and its section, table and appendix numbers, and every quote was checked in that file (by the writer, and in ruling CC-533, ruling 3). It is in no table of this registration.
- **What it reports.** It studies four public preference-optimised checkpoints of one base model, LLaVA-1.5-7B: RLAIF-V (open-source AI feedback), CHAIR-DPO (a CHAIR-based reward), CSR (self-rewarding with CLIP-based calibration) and HA-DPO (dispreferred responses with inserted hallucinations) (Sec. 3, html l.202-203). Captions are English, from the prompt "Please describe this image in detail.", with greedy decoding and at most 512 new tokens (html l.365). The sets are CHAIR-500 (500 random COCO val2014 images), AMBER's 1,004 generative images and a held-out set of 500 other COCO val2014 images (html l.215-221), scored with the public CHAIR script and AMBER's script (html l.219). Its comparator is the base model made to stop earlier by a positive end-of-sequence logit bias, read at the trained model's object recall ("the base stopping curve"), with the bias chosen on one random half of the images and the models compared on the other half, over five splits in both directions (Sec. 2.3, html l.189-194), and paired image-bootstrap intervals from 1,000 draws (Sec. 2.4, html l.197-199). Its numbers, in CHAIRi points (a percentage of mentions) and in percent of the raw CHAIRi gain:
  - the stopping curve reproduces 61, 77 and 86 percent of the CHAIRi gain of RLAIF-V, CHAIR-DPO and CSR on CHAIR-500 (and 20, 64 and 103 percent of the AMBER CHAIR gain) (Sec. 4.2, Tab. 2, html l.383), and 58, 61 and 74 percent on the held-out set (App. L, Tab. L1, html l.1908); the abstract states "58 to 86 percent of the CHAIRi gain of three checkpoints on two disjoint COCO sets" (html l.87);
  - at equal recall, RLAIF-V keeps 4.3 to 5.0 CHAIRi points, CHAIR-DPO 2.4 to 4.6 and CSR 1.3 to 2.5 over the two COCO sets, and HA-DPO no measurable gain (html l.117, l.388);
  - matching caption length with the same bias reproduces only 0 to 24 percent of the gain (Sec. 4.3, html l.397);
  - as diagnostics, two "oracle" rows "truncate each base caption to the word count or to the object-mention count of the PO caption of the same image" and "do not serve as a matching axis" (App. C, html l.943); the object-count truncation reproduces 52, 52 and 57 percent of the CHAIRi gain on CHAIR-500 (Tab. C1, html l.983-986); an "exploratory frontier" takes the best point over end-of-sequence biases, sentence truncations and a short-answer prompt (html l.944; a symbol of the saved text is missing in "first--sentence truncations");
  - a training-free restoration that appends base-only object categories to the trained model's caption, with thresholds fixed on development data before the held-out set was generated (Sec. 6.1, html l.559).
  It states its scope as one backbone, greedy decoding and one detailed-caption prompt (html l.606), "no causal claim on the training effect" (html l.609) and nominal intervals "without a correction for multiple comparisons" (html l.610). It trains no model.
- **What it takes from this study.** The question of E6-2 ("does the fine-tuning do more than make the student say less?") is asked and answered there for preference optimisation: "How much of their hallucination gain can a base model reproduce by stopping earlier?" (html l.101). A trained model has been compared with its own base model's stopping curve at matched recall, with paired intervals, which is the construction of O1 (ERRATUM_O31_6 E6-4) with an end-of-sequence bias in place of a sentence cut; and the base caption has been truncated per image to the trained model's object-mention count, as a diagnostic. The share of the gain that the base model reproduces under a short-answer prompt, and at the best point over end-of-sequence biases, truncations to the first k sentences and that prompt, has also been reported (App. C, Tab. C1, html l.938-944 and l.969-997): these are close to the comparators of T-3 (one shorter prompt) and T-2 (one sentence cut), read as shares of the gain and with no test.
- **What remains for this study.** Supervised fine-tuning on verified propositions, not preference optimisation; Vietnamese captions on Qwen2.5-VL-7B; the training-data verifier measured against human instance gold (line (a)); registered paired tests, under Holm within family T, of precision at a matched number of distinct mentioned classes per image (T-1) and of dominance in both recall and hallucinated objects per caption over one sentence cut and one fixed prompt (T-2, T-3). The work reports shares of a gain, not a test of count-matched precision, and its per-image truncation counts object mentions, not distinct classes.
- **The evidence base.** The work joins the evidence base of E6-2 as a further work read in full. The negative statements of lines (a) and (b) ("among the works we read in full, none reports ...") still hold with it, because it trains no model, so it reports no supervision recall beside a student and tests no order, and it measures no verifier that built fine-tuning data. Line (c) has no negative statement of that form; its sentence that became misleading is replaced below.
- **(i) Its row for the table of record of prior works**, in the eleven columns of `PRIOR_ART_O31_v4.tsv`: the file `PRIOR_ART_ROW_2611.23179.tsv`, committed with this erratum as the row of record for this work until the next version of the table of record takes it.
- **(ii) The concession in E6-2.** One committed sentence of E6-2 becomes misleading without it: line (c) says of the registered tests, against Less is More's curves, "what they add is the per-image matching and the registered paired tests", while this work already reports a per-image object-count truncation and paired intervals at matched recall. The sentence is replaced (the OLD string occurs exactly once in 22b5ad23, at l.58; ruling CC-533):
  - OLD: `Where Less is More drew curves over several settings, our tests use one cut point and one prompt; what they add is the per-image matching and the registered paired tests.`
  - NEW: `Where Less is More drew curves over several settings, our tests use one cut point and one prompt. Say Less, Hallucinate Less? (arXiv 2611.23179, Sec. 2 and Tab. 2; App. C, Tab. C1) already compares preference-optimised models with their base model's stopping curve at matched recall, with paired intervals, reports the share of their gain that the base model reproduces under a short-answer prompt and at the best point over end-of-sequence biases, truncations to the first k sentences and that prompt, and truncates each base caption to the object-mention count of the trained model's caption of the same image as a diagnostic; what our tests add, for supervised fine-tuning on verified propositions, is registered paired tests of precision at a matched number of distinct mentioned classes per image (T-1) and of dominance over one sentence cut and one prompt (T-2, T-3).`
  - In addition, the following paragraph is added to E6-2 after its five items ("First" to "Fifth") and before the paragraph that begins "Multilingual object-hallucination mitigation also exists"; it does not change the count of "five things" shown by the 23 works, because the work was read after them: `A further work, read in full after this statement was registered, asks the same question for preference optimisation. Say Less, Hallucinate Less? (arXiv 2611.23179) studies four public preference-optimised checkpoints of LLaVA-1.5-7B in English, with greedy decoding and one detailed-caption prompt, on two disjoint sets of 500 COCO val2014 images and on AMBER (Sec. 3). Its base model, made to stop earlier by an end-of-sequence logit bias until it reaches each trained model's object recall, reproduces 58 to 86 percent of the CHAIRi gain of three checkpoints on the two COCO sets, while matching caption length reproduces 0 to 24 percent (Tab. 2; Sec. 4.3; App. L). In App. C (Tab. C1) it also reports the share of the gain that the base model reproduces under a short-answer prompt and at the best point over end-of-sequence biases, truncations to the first k sentences and that prompt, and, as diagnostics, when each base caption is truncated to the word count or the object-mention count of the trained model's caption of the same image. Its intervals are nominal, without a correction for multiple comparisons (Sec. 7), and it evaluates public checkpoints and trains no model (Sec. 3). We claim none of this.`
  - In the table "What carries each claim" of E6-2, the rows "the question", "(c) T-1", "(c) T-2, T-3" and "(c) O1" must also cite Say Less, Hallucinate Less? (Sec. 2, Tab. 2; App. C, Tab. C1). This is an addition; no cell is reworded.
- **(iii) Never-write row 43** (E7-5).
- **Status.** By E6-2 status (i), a work read later that reports (a), (b) or (c) in the form registered sends the line to a K5 read. This work reports the question of E6-2 and comparators of (c) (the base model's recall-matched stopping curve, a shorter prompt, truncations to the first k sentences and a per-image object-count truncation, with paired intervals) for preference optimisation; it reports no registered test, no supervised fine-tuning and no count-matched precision on distinct classes. Ruling CC-533 takes the cautious reading: the work counts as reporting (c) under E6-2 status (i), so the line goes to a K5 read before any paper text, and that read weighs its Sec. 2, Sec. 4.3, Tab. 2 and App. C. The K5 read of E6-2 status (ii), held when the verdicts of family T exist, weighs it again. K5 itself is unchanged.

**Why it is safe to register after the gate preview, and before G1 and G2 end:** scope text only; it reads no output of this study, only saved public texts. **GPU-hours:** 0.

---

## E7-14. Optional modules M7, M8 and M9 (R2-08, R2-13, R2-01; F11)

The rules of E-C of ERRATUM_O31_5 (l.544) apply to each module: it is self-contained, descriptive, with no rule and no family; it adds no member to family T or to any registered family; rules G-1 to G-6 apply. **Default: each of M7, M8 and M9 is kept**, unless the investigator's answer to drop it is recorded before the first G3 output; an answer recorded after the first G3 output changes nothing, and the answers on M1 to M6 do not affect them. The record of any answer states its UTC stamp, which must be earlier than the first G3 output; which `k0.json` files existed when it was given (P0r's preview, P1's verdict) and whether `ops5.json` existed; whether any K0 number, any row or word count of any store, or any decode or probe of the training pool was shown to the investigator; and that the question quoted none of them (as ERRATUM_O31_6 l.185).

**Common gating and caps.** Each module is one GPU job. It runs after the G3 read and only if K1 has not fired (G-5, ERRATUM_O31_5 l.119), on the investigator's PC under O-H1 to O-H8, with its own `launch.json`, never inside a registered launch, so no hour counts against a registered cap. Its cap is ceil(1.3 × its planned GPU-hours), counted as wall time from its own `launch.json` (ERRATUM_O31_2 E7, l.61); K4 applies to that job alone, and a K4 stop makes that module's rows NOT RUN and stops nothing else. Speeds are the COMPUTE_PLAN v3 planning values for one RTX 3090 (3.2 s per detailed decode; 0.07 s per Vintern probe; 0.47 s per InternVL3 probe, COMPUTE_PLAN l.13); a student probe is planned at the InternVL3 speed, the nearest recorded 7-8B single probe. Plans marked "estimate" have no measured anchor. `COMPUTE_ADDENDUM_E7.tsv` lists the three jobs.

### M7. The O31 families probed in English on P-a and P-b (R2-08; F13)

- **Question:** Within one language, how does the O31 rule compare with the detector and CLIP rules, which get English class names (ERRATUM_O31_5 l.339)?
- **Probe (fixed now).** "Is there a {name} in the image? Answer yes or no.", with {name} the COCO English category name of the class, as the detectors and CLIP get it. It goes through the probe code path of the registered V-COCO probes (§4.1; ERRATUM_O31_2 E4), with this string in place of the Vietnamese Q⁺. s = p(yes) / (p(yes) + p(no)) at the answer position. The yes set is the first tokens of "Yes" and "yes", and the no set the first tokens of "No" and "no", in each family's tokenizer, recorded with their ids before the first probe. Each family must pass the §4.1 smoke rule (median yes-plus-no mass of at least 0.5 over its first 20 probes), or its English rows are NOT RUN.
- **States:** §4.2 with ERRATUM_O31_1 E2, at OP\*'s family set and thresholds (by identity, as E-B5 reads them), and the single-family rows at OP\*'s thresholds.
- **Reported:** on P-b, RT, FA, DR strict and the UNCERTAIN shares; on P-a, RT (FA on P-a is never read, ERRATUM_O31_5 l.331); each beside the Vietnamese VR-O31 row and the detector and CLIP rows, with intervals clustered by image (E-B5).
- **Data and role:** UIT-ViIC test 231, instance gold, in the role of E-B5. Never tier 3.
- **Decision rule:** descriptive, no rule. The reading of ERRATUM_O31_5 l.342 does not apply to the English rows. **Family:** none.
- **Against the claim:** none of its own; printed in every case beside the rows it mirrors.
- **GPU-hours (estimate):** P-b about 2,000 × (0.07 + 0.47) s = 0.30; P-a about 0.12 (G3v's plan, ERRATUM_O31_5 l.120); model loads about 0.20. **Plan 0.62, cap ceil(1.3 × 0.62) = 1.**
- **New code:** yes (C44).
- **Why it is safe to register after the gate preview, and before G1 and G2 end:** the template and token sets are fixed now and hold no gate value; OP\* enters by identity only; it reads no output of G1 or G2; its propositions are the registered P-a and P-b.

### M8. Weight sensitivity of the two decoding comparators at tier 1, with no selection (R2-13, the nearest allowed form)

- **Systems:** C-VCD at α ∈ {0.5, 2}, and C-DeCo at α ∈ {0.1, 0.3}, with every other setting as ERRATUM_O31_5 l.271-279 registers it and as ERRATUM_O31_6 E6-7.7 (l.340-341) fixes it: C-VCD keeps the port's noise, β 0.1, T 500, the noise seed 42 per image, greedy selection and batch 1, and is named "VCD as ported in FAIR 2026"; C-DeCo keeps layers 18 to 24 of 28, top-p 0.9, top-k 20, greedy decoding and batch 1. The registered rows (C-VCD α 1; C-DeCo α 0.6) are unchanged and are the only comparator rows of E-B4.
- **Why these values:** half and double VCD's run default α = 1 (ERRATUM_O31_6 l.249); for DeCo, two further points of the range that the DeCo paper states ("α is set within the range of 0.1 to 0.6", ERRATUM_O31_6 l.269), whose upper end, 0.6, is the registered value.
- **Data and role:** UIT-ViIC test 231, instance gold, Vietnamese with the S0 prompt. Tier 2, KTVIC and every registered comparator row are unchanged. Never tier 3.
- **Reported:** R, h, CHAIR_i, CMP of S2 against each setting (k-matched as E-B1 (a)), and words per caption, beside the registered rows.
- **Decision rule:** descriptive, no rule. Nothing is selected: no setting replaces a registered setting, enters any comparison of E-B4 or is run at tier 2. No paper text says, from these rows, that a comparison of S2 with C-VCD or C-DeCo holds at every setting, is robust to α or does not depend on α; the rows are printed beside the registered rows and are never cited in the title, the abstract or the conclusion. **Family:** none.
- **Against the claim:** if any of these settings has R ≥ R_S2 and h ≤ h_S2, with both paired intervals excluding an S2 advantage, the paper states it in its results and its summary of results, as ERRATUM_O31_5 l.293 does for the registered settings, and names the setting.
- **GPU-hours:** C-VCD 2 × 231 × 3.2 s × 2 passes = 0.82; C-DeCo 2 × 231 × 3.2 s × 1.2 = 0.49 (the 1.2 factor of l.297). **Plan 1.31, cap ceil(1.3 × 1.31) = 2.**
- **New code:** yes (C45).
- **Why it is safe to register after the gate preview, and before G1 and G2 end:** the values are fixed before any comparator output, from the saved sources that ERRATUM_O31_6 records, and hold no gate value; it reads no output of G1, G2 or P1. Choosing a comparator weight on UIT-ViIC test 231, as the review proposed, would contradict ERRATUM_O31_5 l.270 ("no tuning on any evaluation data") and is not offered (ruling CC-533). It changes none of the settings that ERRATUM_O31_6 E6-7.7 settled.

### M9. The students' own existence probe (F11; R2-01)

- **Question:** After fine-tuning, does a student separate present from absent classes differently, or does it name classes at a different level of its own yes-score?
- **Systems:** S0, S1 (seed 42) and S2 at OP\* (seed 42), each as the bf16 base with its adapter (ERRATUM_O31_2 E5).
- **Probe:** the §4.1 Q⁺ in Vietnamese with the first listed term of `coco80_vi.json`, on P-b of UIT-ViIC test 231 (as E-B5, l.338). s is read from the student's own logits at the answer position, with the §4.1 token sets (yes c/có, no kh/không) resolved in the Qwen2.5-VL tokenizer and checked as for M0 (as M1, l.561). Batch 1. A student that fails the §4.1 smoke rule has its rows NOT RUN.
- **Reported per student:**
  - the AUROC of s against instance presence, with intervals clustered by image, and the paired differences S1 − S0, S2 − S0 and S2 − S1 on the same resampled images;
  - for each P-b proposition, whether the class is mentioned in that student's registered seed-42 G3 decode of the image (the frozen extractor), giving the mention rate among present and among absent classes in ten bins of s, [0, 0.1), [0.1, 0.2), …, [0.9, 1.0];
  - the lower edge of the first bin, in ascending order of s, at which the mention rate over all P-b propositions of that bin reaches 0.5, or "not reached".
- **Data and role:** UIT-ViIC test 231 (P-b), instance gold. Never tier 3.
- **Decision rule:** descriptive, no rule. No expectation is registered for these rows (ruling CC-533). **Family:** none.
- **Against the claim:** the rows are described as "a descriptive probe of the students' own yes/no answers"; the paper never calls them a mechanism, a cause or an account of what is learned inside the network (row 40 of E7-5).
- **GPU-hours (estimate):** 3 students × about 2,000 propositions × 0.47 s = 0.78; adapter and model loads about 0.30. **Plan 1.08, cap ceil(1.3 × 1.08) = 2.**
- **New code:** yes (C46).
- **Why it is safe to register after the gate preview, and before G1 and G2 end:** P-b is built from the gold, COCO-2014 train co-occurrence and a fixed random stream (ERRATUM_O31_5 l.332-335); the students enter by identity; the bins are fixed now and hold no gate value; it reads no output of G1 or G2. With no test, the power reading that ERRATUM_O31_5 l.744 tied to a mechanism prediction is not needed.

**Total of M7 to M9:** plan 3.01 GPU-hours; caps 1 + 2 + 2 = 5 hours.

---

## E7-15. Reserved to the investigator: the replication of T-1 and T-2 at tier 3 (R2-25; FOR_THE_PI item 5)

**This section binds only if the investigator says yes and the yes is recorded before the first G3 output. Otherwise it is void: none of its words is registered, and every committed line it names stays as committed. If it binds and tier 3 does not run, family T3 is NOT RUN (last row of the table below).** The record of the answer has the content listed for the modules in E7-14 (as ERRATUM_O31_6 l.185) and also states the investigator's answer to Q1 (PREREG l.248) at that time.

**What it reverses.** The committed text bars any tier-3 row of family T: ERRATUM_O31_5 l.102 ("No addition uses the tier-3 set in any role, except the tier-3 row of E-B8 R-a"), l.147 (E-B1: "Never tier 3."), l.157 ("never as a tier-3 result") and l.749 ("no later panel may add them at tier 3"). On the recorded yes, and only then, these words are replaced as follows (each OLD occurs exactly once in ababc533; ruling CC-533). ERRATUM_O31_5 l.223 ("the ordering test uses tier 2. Never tier 3.") is not touched: T-4 stays at tier 2.
- l.102. OLD: `No addition uses the tier-3 set in any role, except the tier-3 row of E-B8 R-a, which is computed at the registered tier-3 look from its registered outputs, with no new decode or probe.` NEW: `No addition uses the tier-3 set in any role, except the tier-3 row of E-B8 R-a and, under ERRATUM_O31_7 E7-15, the members of family T3, each computed at the registered tier-3 look from its registered outputs, with no new decode or probe.`
- l.147. OLD: `- **Data and role:** tier 1 (descriptive rows, seed 42) and tier 2 (the family T tests). Never tier 3.` NEW: `- **Data and role:** tier 1 (descriptive rows, seed 42) and tier 2 (the family T tests). Never tier 3, except the replication of T-1 and T-2 in the separate family T3 of ERRATUM_O31_7 E7-15, at the registered tier-3 look.`
- l.157. OLD: `A T verdict is reported as a registered test on the rehearsal set, never as confirmed and never as a tier-3 result (K6).` NEW: `A T verdict is reported as a registered test on the rehearsal set, never as confirmed and never as a tier-3 result (K6); the tier-3 replication of T-1 and T-2 is the separate family T3 of ERRATUM_O31_7 E7-15 and is reported only as E7-15 allows.`
- l.749. OLD: `E-B1, E-B2 and E-B4 have their rows and tests at tier 2, which shares tier 3's population (E-A.2 item 7); no later panel may add them at tier 3.` NEW: `E-B1, E-B2 and E-B4 have their rows and tests at tier 2, which shares tier 3's population (E-A.2 item 7); no later panel may add them at tier 3. The one exception is the replication of T-1 and T-2 in the separate family T3, registered by ERRATUM_O31_7 E7-15 on the investigator's recorded yes before the first G3 output.`

**Family T3.**
- **Members:** T3-1 and T3-2, which are T-1 and T-2 in exactly their registered form (ERRATUM_O31_5 l.150-151): T3-1, the null CMP_S2 − CMP_S0 ≤ 0; T3-2, p = max(p_R, p_h) for S2 against S0-trunc. T-3 and T-4 have no tier-3 member (T-3 would need a new S0-two decode; T-4 stays at tier 2).
- **Data:** the tier-3 images, gold as the tier-3 set registers it (PREREG l.67; ERRATUM_O31_1 E11), the registered tier-3 decodes of S0 (one decode) and S2 (three seeds), paired as at tier 2 (G-4; ERRATUM_O31_1 E12); S0-trunc cut at the j\* of the tier-1 freeze commit (ERRATUM_O31_5 l.144), on the CPU. No new decode or probe; GPU-hours 0.
- **Statistics:** the G-4 bootstrap on the tier-3 images (B = 10,000, seed 20261127) and its one-sided p. Holm's correction within T3 at α = 0.05, two members. A member PASSes iff its Holm-adjusted p < 0.05. A member that is NOT_IDENTIFIED or NOT RUN enters with p = 1.
- **Place:** T3 is separate from the primary family, the secondary family and family T, and changes none of their verdicts or adjusted p-values; no error rate across families is claimed. It is computed at the one registered tier-3 look, on the scoring machine that the tier-3 ruling names (PREREG l.76), and is named in the frozen-config commit that precedes the look (PREREG l.178). It is never computed before the look and never on any other set.

**Combining rule (no second chance, ERRATUM_O31_5 l.11).** The tier-2 verdict of T-1 or T-2 governs the wording of claim (c) for that member (ERRATUM_O31_6 E6-2, Conditions). The tier-3 verdict adds one statement only, printed beside the tier-2 verdict:

| tier-2 verdict (family T) | tier-3 verdict (family T3) | what the paper writes for that member |
|---|---|---|
| PASS | PASS | claim (c) in the member's form, as E6-2 allows, with "replicated on the one-look set" |
| PASS | FAIL, NOT_IDENTIFIED or NOT RUN | claim (c) in the member's form, as E6-2 allows, with "not replicated on the one-look set" and the tier-3 verdict in the same sentence |
| FAIL, NOT_IDENTIFIED or NOT RUN | PASS | no claim (c) in that member's form; the sentences of ERRATUM_O31_5 l.163-165 as registered; the tier-3 result is printed beside the tier-2 verdict with "the registered tier-2 verdict governs, and no claim is made"; it is never cited in the title, the abstract or the conclusion as support |
| FAIL, NOT_IDENTIFIED or NOT RUN | FAIL, NOT_IDENTIFIED or NOT RUN | both verdicts, side by side, with the sentences of l.163-165 |
| any | tier 3 does not run (no set assigned, K1, K2, no approved look) | T3 is NOT RUN, with its cause; E7-7 applies |

Rows 1 to 4 apply only if the tier-3 look is made, and a tier-3 NOT RUN in those rows is a member NOT RUN at a look that was made; if the look is not made, the last row alone applies. A tier-3 FAIL is never hidden, replaced or qualified by the tier-2 verdict, and a tier-3 PASS never replaces a tier-2 verdict that is not PASS.

**Why it is safe to register after the gate preview, and before G1 and G2 end:** its members, data, decodes and statistics are registered texts committed before any `k0.json` existed; it reads no output of P0r, G1, G2 or P1; the investigator's answer, if given, is given after the preview exists, and the record says so. **New code:** yes (C47).

**Nothing else is reserved here.** The keep or drop answers on M1 and M2 (ERRATUM_O31_5 l.544), on M6 (ERRATUM_O31_6 l.185) and on M7 to M9 (E7-14), and the answer to Q1 (PREREG l.248), are governed by their own texts and need no text here.

---

## E7-16. When each item must be committed, and companion files

**Last commit points.**
- E7-1: before the first G3 output, the deadline that E-B3 sets for registering T-4 (ERRATUM_O31_5 l.247). Ruling CC-530 states that, if this text is not committed by then, T-4 is NOT RUN with the cause "form incomplete in the committed text", stays a member and enters family T with p = 1 (ERRATUM_O31_4 E4-7).
- E7-2 to E7-4, E7-8 (a), E7-9 to E7-12, M7 to M9 with their keep or drop records, and the investigator's answer under E7-15: before the first G3 output.
- E7-5 to E7-7 and E7-13: before any paper text, and with this erratum before the first G3 output.
- E7-17: before the first G3 output, and in every case before the first output of the row, job or record each one governs (CD-9 before the t0 of G3's launch.json).
- E7-8 (b): before the first T2 output, and with this erratum before the first G3 output.
- This erratum is committed as one file before the first G3 output. If a G3 output exists first, the items whose last commit point is the first G3 output (E7-1 to E7-4, E7-8 to E7-12, M7 to M9 and E7-15) are not registered and the matter goes to the investigator, as ERRATUM_O31_6 l.360 provides for its own items (an adopted text of E7-17 whose row has no output yet may still be registered before that row's first output); E7-5 to E7-7 and E7-13 may still be registered before any paper text.

**Companion files.** `COMPUTE_ADDENDUM_E7.tsv` adds planned GPU-hours and caps for M7, M8 and M9 only; no registered cap changes, and no addition has tier-3 hours. `CODE_NEEDS_E7.tsv` adds C35 to C58; C35 amends the T-4 statistic of CODE_NEEDS C24 to the readings of E7-1, and C48 to C58 apply the texts of E7-17 (their "if adopted" holds for all eleven; where a row differs from E7-17, E7-17 governs). `PRIOR_ART_ROW_2611.23179.tsv` holds the row of E7-13 (d) (i). The draft's `OPEN_POINTS.txt` and `SELF_CHECK.txt` are not committed; ruling CC-533 rules every open point and records the checks of every OLD string and quote.

---

---

## E7-17. Computational details left open by errata 5 and 6

The code author of packages 2 to 4 reported values that ERRATUM_O31_5 and ERRATUM_O31_6 leave open; the code refuses to run until a registered text fixes them (`OPEN.txt` of `o31_code2_pkg2`, `o31_code2_pkg3` and `o31_code2_pkg4`). They are of the kind of E7-1. Ruling CC-533 read the eleven texts drafted for this section and adopted all eleven, CD-6, CD-7, CD-9 and CD-10 with changed or added words. For each: the committed words that leave the point open, the readings considered, the reading adopted, and the registered text. Each registered text fills words that ERRATUM_O31_5 or ERRATUM_O31_6 leaves open and contradicts none of them, except that CD-9 replaces the time of a deadline by a recorded time that precedes it. Each was fixed without reading any gate value or any output of P0r, the §3.5 pass, G1, G2 or P1 (CD-7 reads the `stats.seconds` of the G1 records when the table is made, as l.513 already registers), and each fixes its numbers before any output of the row, job or record it governs exists. Where the readings are ordered in their effect, the one adopted cannot make a registered test or a descriptive reading easier to pass or to license positive wording; where no reading is ordered, the item says so. Points that are pure implementation choices with no effect on any reported number are not registered (last paragraph of this section).

**CD-1 (pkg2 Q2). "Line break" in the sentence rule.**
- Committed words: ERRATUM_O31_5 l.141, "a sentence ends at ".", "!", "?" or "…" followed by white space or the end of the text, and at every line break. Empty pieces are dropped."
- Readings considered: "\n" only; "\n", "\r\n" and "\r"; every boundary at which Python's `str.splitlines()` splits (also "\x0b", "\x0c", "\x1c" to "\x1e", "\x85", U+2028 and U+2029); and whether pieces are stripped of white space before the empty check.
- Adopted: the `str.splitlines()` reading, with stripping, as the code does. No reading is ordered in its effect on T-2, O1, E-B2 or M6 (the number of sentences moves j\* and the cut in either direction); the reading is fixed before any decode exists, and its effect is reported.
- Registered text: `In the sentence rule of E-B1 (ERRATUM_O31_5 l.141), a line break is every boundary at which Python 3's str.splitlines() splits a string ("\n", "\r", "\r\n", "\x0b", "\x0c", "\x1c", "\x1d", "\x1e", "\x85", U+2028 and U+2029). Each piece is stripped of surrounding white space before the empty check and before the join. For every system and set, the number of captions that contain a line-break character other than "\n" is reported beside the rows that use the sentence rule.`

**CD-2 (pkg2 Q4). The join of S0-filter's kept sentences, and a class with no verdict.**
- Committed words: ERRATUM_O31_5 l.184-187: S0-filter "removes every sentence of S0's caption that mentions a COCO-80 class whose V-COCO verdict, under OP\*'s family set and thresholds, is not SUPPORTED"; "Mentions are then extracted again from the kept text." No join is given, and no case of a class that the sentence-level extraction finds but that has no V-COCO verdict.
- Readings considered: the join by single spaces (E-B1's join), by line breaks, or the original separators; a class without a verdict kept or removed.
- Adopted: the single-space join of E-B1; the caption unchanged when no sentence is removed; a class without a verdict counts as not SUPPORTED, so its sentence is removed. The last follows the committed words ("whose V-COCO verdict ... is not SUPPORTED") and the principle of ERRATUM_O31_1 E2 that a missing score never supports. No reading is ordered in its effect on the dominance sentence of l.200; the count of such classes is reported.
- Registered text: `S0-filter's kept sentences are joined by single spaces, as E-B1 joins kept sentences; a caption from which no sentence is removed is left unchanged. A COCO-80 class that the sentence-level extraction finds but that has no V-COCO verdict counts as not SUPPORTED, and every sentence that mentions it is removed; the number of such classes and of the sentences removed for them is reported per set.`

**CD-3 (pkg2 Q7). The bootstrap standard error of E-B7's power reading.**
- Committed words: ERRATUM_O31_5 l.425, "the estimate D̂ and its bootstrap SE_231 (G-4)"; l.426, "SE_4224 = SE_231 × sqrt(231 / 4,224), with P(H2) = Φ(−D̂ / SE_4224 − 1.96)". Neither the denominator nor undefined replicates are fixed.
- Readings considered: the standard deviation of the B replicate values with B or with B − 1 in the denominator; undefined replicates left out or not.
- Adopted: B − 1, the convention of ERRATUM_O31_4 E4-7 for σ²_seed and of E7-1 for V_k, and the same for E7-9's SE_231. It gives the larger SE. For D̂ < 0 a larger SE gives a smaller projected P(H2), so the reading never raises P(H2) towards 0.98; for D̂ ≥ 0, P(H2) ≤ Φ(−1.96) < 0.98 under either reading, so the sentence of l.436 (as E7-4 replaces it) fires under both. h divides by the number of captions, so a replicate of D cannot be undefined; if one occurs, the reading is NOT_IDENTIFIED. The interval of ρ̂ that l.427 reports uses R-a's rule (a replicate with R_S0 − R_S1 ≤ 0 is undefined, l.449).
- Registered text: `In E-B7 PR-1 (ERRATUM_O31_5 l.425-427), SE_231 is the standard deviation of the B = 10,000 replicate values of D on the shared index matrix of UIT-ViIC test 231, with B − 1 in the denominator. If any replicate of D is undefined, PR-1 is NOT_IDENTIFIED and the count is reported. The interval of ρ̂ reported with PR-1 leaves out the replicates with R_S0 − R_S1 ≤ 0 and reports their number, as E-B8 R-a does.`

**CD-4 (pkg2 Q8). The seed draw of row R-b.**
- Committed words: ERRATUM_O31_5 l.463, "three seed indices are drawn with replacement from {42, 43, 44} (numpy PCG64, seed 20261130), one draw per replicate shared by S1 and S2". The call form and its order against the image index matrix are open, and the forms give different numbers.
- Readings considered: one call of shape (B, 3) or B calls of 3; `choice` or `integers`; one stream with the image indices or a separate stream.
- Adopted: one call of shape (10,000, 3) on its own stream. No form is ordered in its effect (R-b is a sensitivity interval); the form is fixed before any tier-2 output.
- Registered text: `The seed draws of R-b (ERRATUM_O31_5 l.463) are numpy.random.default_rng(20261130).integers(0, 3, size=(10000, 3)), one call on a stream of its own, separate from the image index matrix (seed 20261127, ERRATUM_O31_1 E9). Row b is used with row b of the image index matrix; the values 0, 1 and 2 stand for the seeds 42, 43 and 44; the same row is used for S1 and S2, so that the E12 pairs are resampled as pairs.`

**CD-5 (pkg2 Q9). The unit of row R-d when an image has several references, and the tie at the fifth class.**
- Committed words: ERRATUM_O31_5 l.479-481: "the unit is the (image, class) pair; the extractor (`extract.mentions`) runs on the existing Vietnamese references of UIT-ViIC test 231; output: per class, precision and recall of the lexicon's mentions against instance presence; the human "hallucination" floor h_ref; and the five classes with the lowest precision among those with at least 5 mentions." l.488: "the human floor is printed beside every h".
- Readings considered: a pair counts as mentioned when any reference mentions the class (union), or the unit is each reference caption; h_ref per image (over the union of references) or per reference caption; a tie at the fifth lowest precision broken or not.
- Adopted: precision and recall on the (image, class) pair with the union of the references, as the committed unit says (this part is not ordered: a false mention repeated across references can raise the union's precision, and the union changes which classes reach 5 mentioned pairs); h_ref per reference caption, by the §5 definition of h applied to each reference as one caption, because h of every system is per caption and the union of several captions mentions more absent classes, which would raise the floor printed beside every h and make a system's h look closer to the human floor (this part is ordered: it gives the lower floor); every class tied at the fifth lowest precision is named (ordered: it names at least as many).
- Registered text: `In R-d (ERRATUM_O31_5 l.479-481), an (image, class) pair is mentioned iff the frozen extractor finds the class in at least one of the image's references; per-class precision and recall are computed over these pairs against instance presence. The human floor h_ref is h of §5 against instance presence with each reference caption counted as one caption: the §5 count of mentioned objects not in the gold, summed over all reference captions of the 231 images, divided by the number of reference captions. If several classes tie at the fifth lowest precision among those with at least 5 mentioned pairs, every tied class is named.`

**CD-6 (pkg2 Q10). Distinct-2, self-BLEU-4 and the store-overlap share of row R-e.**
- Committed words: ERRATUM_O31_5 l.496-499: "the store-overlap share, which is the share of a caption's word 4-grams that occur among the 4-grams of its arm's training store's detailed targets"; "distinct-2"; "self-BLEU-4 on min(500, n) captions per system and set ... each scored against the others".
- Readings considered: distinct-2 over the whole set of captions or as a mean over captions; self-BLEU-4 at corpus or sentence level, its BLEU variant and smoothing; the share as a mean of per-caption shares or over pooled 4-grams.
- Adopted: the definitions below. R-e is descriptive with no reading in either direction ("Against the claim: none", l.505), so no reading is ordered; each is the common form of its measure, fixed before any decode exists.
- Registered text: `In R-e (ERRATUM_O31_5 l.496-499), on the §5 tokens: distinct-2 of a system on a set is the number of distinct word bigrams divided by the number of word bigrams, both counted over all its captions on that set, with bigrams taken within each caption. Self-BLEU-4 of a system on a set is the mean, over its sampled captions, of the sentence-level BLEU-4 of each caption against all other sampled captions of that system as references (uniform weights 0.25 for orders 1 to 4, clipped n-gram counts, the brevity penalty with the closest reference length (ties to the shorter), and, for an order with no matched n-gram, a matched count of 0.1 in place of 0); a caption is never its own reference; a sampled caption with fewer than four tokens is left out of the mean and counted, and stays among the references of the others. The store-overlap share of a caption is the number of its word 4-gram positions whose 4-gram occurs in the set of 4-grams of the arm's training store's detailed targets, divided by its number of 4-gram positions; a system's value on a set is the mean over its captions that have at least one 4-gram, and the number of captions without one is reported.`

**CD-7 (pkg2 Q12). The sources of the cost table R-f.**
- Committed words: ERRATUM_O31_5 l.513, "stage-1 GPU-seconds per image (record field `stats.seconds` for the 69 G1 images; FAIR's planning value for the rest), probe GPU-hours, SFT hours and inference GPU-seconds per image, all from the run records."
- Readings considered: which record and field gives each number; what happens if FAIR's planning value cannot be located.
- Adopted: wall time from each job's own `launch.json` t0, the clock of the caps (ERRATUM_O31_2 E7), so that loads, pauses and restarts are counted and no cost is understated; a value that no named record holds is printed as "not recorded", never estimated. R-f is a cost statement with no reading, so no reading is easier to pass; this one cannot lower a reported cost.
- Registered text: `In R-f (ERRATUM_O31_5 l.513), probe GPU-hours, SFT hours and the GPU-seconds of a decode are the wall time of the job from the t0 of its own launch.json to its end stamp in its run record (the clock of ERRATUM_O31_2 E7), summed over the jobs of each item; inference GPU-seconds per image are that wall time divided by the number of images the job decoded or probed. Stage-1 GPU-seconds per image are the mean of stats.seconds over the 69 G1 records, printed with n = 69; for the other 3,698 images FAIR's planning value is printed only if a saved FAIR record that states it is named with its file and line before the table is written, and otherwise the cell reads "not recorded". Every time taken from a launch.json includes the job's model loads, pauses and restarts, and the table says so. No value is estimated.`

**CD-8 (pkg3 S2). The image budget of C-VCD.**
- Committed words: no committed sentence names the visual-token budget of any decode. ERRATUM_O31_5 l.305 ("New code") places C-VCD in "the VCD port moved into the O31 decoder", and G-3 (l.110-112) ties every new decode to the `decode.py` setting; the registered S0 and student decodes use `decode.py`'s image processing (512 visual tokens, the budget of the training recipe, PREREG l.33). FAIR 2026's port used 1,024. So the committed text fixes 512 only by the reading of l.305 with G-3.
- Readings considered: 512 (the O31 decoder), or 1,024 (the port as FAIR 2026 ran it).
- Adopted: 512, the budget of S0 and S2, against which C-VCD is compared; at 1,024 the comparator would see a different image budget from both systems it is compared with. Neither budget is ordered in its effect on VCD, so the difference from the port is disclosed.
- Registered text: `C-VCD, and M8's C-VCD rows, decode with decode.py's image processing (min_pixels 256 × 28 × 28 and max_pixels 512 × 28 × 28, that is at most 512 visual tokens), the budget of S0 and of the students; the port as FAIR 2026 ran it used 1,024. The disclosure sentence of C-VCD in ERRATUM_O31_6 E6-7.7 is followed in every paper text by the sentence "The VCD row uses the image budget of S0 and the students (at most 512 visual tokens), where the port in FAIR 2026 used 1,024."` (This adds a sentence after the committed disclosure and changes no word of it.)

**CD-9 (pkg4 T1). The form of a keep or drop record, and the time against which it is checked.**
- Committed words: ERRATUM_O31_5 l.544, "the keep or drop decision is recorded before the first G3 output ... An answer recorded after the first G3 output changes nothing"; ERRATUM_O31_6 l.185 lists the content of M6's record. Neither fixes the form of the record, where it lives, or which time "the first G3 output" is.
- Readings considered: any written record; a record committed in the run repository; "the first G3 output" as the time of the first file the G3 job writes, or as an earlier, recorded time.
- Adopted: a record in a fixed form, in the decision log or committed in the run repository, with a `date -u` stamp checked against the t0 of G3's `launch.json`. That time is recorded and precedes every G3 output, so no answer given after any G3 output can count. This is not ordered: an answer given between that t0 and the first G3 output would not count, and a module that falls back to its default may remove or add rows that bear on the claim in either direction; the point is that the time can be read from a record. It narrows the committed deadline to a recorded time that precedes every G3 output. A keep or drop answer names who gave it, because E-C gives the keep or drop to the investigator (ERRATUM_O31_5 l.544); for E7-15, which is reserved to him, only his own answer counts; a later record replaces an earlier one only while both precede that time.
- Registered text: `A keep or drop answer (ERRATUM_O31_5 E-C; ERRATUM_O31_6 E6-5; ERRATUM_O31_7 E7-14) and the investigator's answer under ERRATUM_O31_7 E7-15 count only if each is written in a record of the form {"decisions": {"M1": "keep" or "drop", ..., "M9": "keep" or "drop", "E7-15": "yes" or "no"}, "recorded_utc": an ISO-8601 UTC stamp taken from date -u}, in which a key may be absent, with the content that ERRATUM_O31_6 l.185 lists and, for each answer, who gave it (the investigator, by a pointer to his message, or an agent under a standing delegation of his, by its log id), kept in the decision log or committed in the run repository, and only if its recorded_utc is earlier than the t0 of G3's launch.json. For this check the time of the first G3 output is the t0 of G3's launch.json. Where two such records differ on a key, the later one counts. For E7-15 only the investigator's own answer counts; no default, delegated decision or answer of an agent stands for it. A module with no counting answer takes its default, and E7-15 without a counting "yes" of his own is void.`

**CD-10 (pkg4 T3). The source of M3's MME copy, and the yes/no parser.**
- Committed words: ERRATUM_O31_5 l.631, "the dataset pinned by revision and sha at pin time (its source and licence are not yet checked). If it cannot be pinned or its licence does not allow this use, M3 is NOT RUN"; l.619, "An answer counts as "yes" or "no" only if the lower-cased output starts with that word."
- Readings considered: which source and how it is recorded (E5 l.635 already requires the pin "in every case before the first MME output"); "starts with that word" as a string prefix (which would count "yesterday" or "nothing") or as the first word.
- Adopted: the source named in a pin record before the first MME output, as l.635 requires, with the UTC stamp of the pin record reported beside M3's rows, so that a reader can see whether the source was fixed before any student output existed; the first word, read as the first maximal run of letters. Neither part is ordered: the parser applies to every system alike.
- Registered text: `M3's MME copy is the one named in a pin record (repository or source, revision, per-file sha256 and its terms of use, read from the saved card or terms) made before the first MME output (ERRATUM_O31_5 l.635); without such a record, or if the terms do not allow this use, M3 is NOT RUN. An output counts as "yes" (or "no") iff the first maximal run of letters of the stripped, lower-cased output equals "yes" (or "no"). The UTC stamp of the pin record, and whether it is earlier than the t0 of G3's launch.json, are reported beside M3's rows.`

**CD-11 (pkg4 T4). Numerals and tokens of M4 (a).**
- Committed words: ERRATUM_O31_5 l.646-647: "A Vietnamese numeral token immediately before a matched COCO-80 mention, or separated from it by exactly one classifier token from a fixed list. All matching is on the extractor's normalised text"; "digit strings from 2 to 99".
- Readings considered: digit strings with leading zeros ("02") counted or not; a token with attached punctuation ("hai,") a numeral or not; the claim attached to every matched mention or to the first mention of a class; "người" read as a classifier or as part of the person mention.
- Adopted: the code's readings, with one rule that prevents a numeral from making two claims. They apply to every system alike, and no reading is ordered in its effect on l.666's sentence.
- Registered text: `In M4 (a) (ERRATUM_O31_5 l.646-647), a token is a whitespace-separated piece of the extractor's normalised text; a digit string is a numeral iff it matches [1-9][0-9]? and its value is 2 to 99; a token with attached punctuation is not a numeral. Every matched mention span counts, not only the first of its class. A numeral makes at most one claim: it attaches to the first matched mention span that begins immediately after it, or after exactly one classifier token of the list; where "người" can be read both as the classifier and as part of the person mention, the claim attaches to the person mention once.`

**Not taken here** (implementation only; each ruled in CC-533): pkg4 T5 (M0's operating set is defined by M0's own registration; the wrapper computes it with M0's code), the exact z value of PR-0 (pkg2 Q7, second part), the wiring of the §5 tokeniser (pkg2 Q10, last part), the stop token kept in the token ids of C-VCD (pkg3 S2), and the bootstrap of M3 across subtasks (pkg4 T3, which follows ERRATUM_O31_1 E9).

---

## E7-18. What stays as registered

- The prereg (5b33480b), ERRATUM_O31_1 to ERRATUM_O31_6 and COMPUTE_PLAN v3, as committed and as earlier errata amend them.
- ERRATUM_O31_5 (ababc533), except the words of l.400, l.436 and l.533 that E7-4 replaces and, on the investigator's recorded yes under E7-15 only, the words of l.102, l.147, l.157 and l.749 that E7-15 replaces. Every E-B item, every module M1 to M5 with its default, family T and its four members, Holm within T, the G-rules, E-D.1 to E-D.3 and E-E stay.
- ERRATUM_O31_6 (22b5ad23), except the sentence of l.58 that E7-13 (d) replaces, with the paragraph and the citations that E7-13 (d) adds to E6-2; no other word of E6-2 is reworded; the list of E6-3 gains rows 32 to 43 and nothing in rows 1 to 31 changes; O1, O2, M6 and every setting that E6-7.7 settled (the rule after SENTINEL NOT RUN; C-VCD with the port's noise; C-DeCo's L and layers; VR-EFUF and VR-EFUF-repo; M5's batch, targets and loss) stay.
- In particular: H1 to H5, their thresholds, margins, statistics and families; T-a; K0 to K6; the grid, K0, P_floor, OP\*, OP_mid and their tie rules; the five-point rule, what its result allows, the edge row and T-4's form and place (ERRATUM_O31_4 E4-2 to E4-7, with the two computational details of E7-1); the sets, their roles, the tiers, the branch rule and custody; the training recipe, seeds and N_steps; every cap of every registered or earlier added job.
