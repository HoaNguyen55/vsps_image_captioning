# VSPS-J E2b tier-1 PREREG: open 7-8B verifiers with a typed 3-label output, paired against Vintern-1B (dev-explore)

Status: DRAFT for a judge read (tier REVERSIBLE, dev-explore, bar >= 90), 2026-11-01. Not committed, nothing launched.
Provenance: direction `manuscript/directions/VSPS_J_E2B_DIRECTION_v2_2026-11-01.md` (sha256 8967fbc0), adopted by
CC-215r2 (GO, panel round 2/3, median 92). Round 2 was a **full three-judge panel round plus a Codex read**, not the
"one-judge diff read" that v2 l.7 announced (NB-C16); its GO is a real GO.
**Licence scope (NB-C1, CC-215r2 ruling 2).** CC-215r2 licenses drafting this file. It is not a launch licence. The
order is: this draft, then a judge read, then the gatekeeper commit, then the unscored rate run (section 6). PI-1101r
("rate run after CC-215r2") is a not-before condition only. No unreviewed GPU script runs. Tier-1b probing (section 7)
needs its own post-rate amendment (block caps) and a judge read, and is gated by NB-C8.
Label on every output: `TIER 1 / DEV-EXPLORE (VSPS-J E2b)`. Every estimate is AI opinion. Every number marked
[measured] was computed on the laptop on 2026-11-01 by `e2b.py plan` (`e2b_plan.json`) or by the command beside it.
No test set is touched. No AMBER gold is read. No new labels. No AI output is used as gold.

Code: `scripts/vsps_j_e2b/` = `e2b.py` (plan, rate, probe, score, selftest), `test_e2b.py` (CPU selftest, no weights,
no data, every socket raises), `e2b_job.sh` (the rate-run block); SUMS in that folder. It imports
`scripts/vsps_j_m0/m0.py` unchanged (M0 guards, segments, keyword rule, prompt frame) and loads models through
`scripts/lb/decode_hf_vlm.py` `fetch()` / `check_snapshot()` / `load()` unchanged (AutoModelForImageTextToText, no
remote code; file shas pinned in the job). Plan file here: `e2b_plan.json` (ids, counts and shas only; no M-HalDetect
text).

## 1. Why E2b, and the claim (v2 section 1, NB-C5, NB-C14)

| block | result [measured, anchored] | reading |
|---|---|---|
| M0 (f77eea1), M-HalDetect val selection set, Vintern-1B zero-shot | AUROC 0.844 [0.833, 0.854]; precision at recall 80 = 55.0 | ranking works; reaching recall 80 costs precision |
| E1b (ed65b74), KTVIC train | logit kappa 0.889; retention 59.9 < 65.0 at the chosen vector -> E2-KT STOP | re-thresholding one 1B model does not lift retention |
| E1a (5d6db4c), UIT-ViIC test 231 | n_absent 48 < 200 -> descriptive only | DR inconclusive; RT far from 80 |

Moving along one curve does not raise precision at high recall; a better ranker is needed, hence a larger verifier.
The output is the 3-label set of FAIR 2026 (Hòa et al.; `rescap/metrics_svp.py` `VERDICTS`), credited as such.

**Registered claim form (for the tier-3 prereg; NB-C5 wording).** At the recall-matched operating point (section 4.1),
on the primary types {object, number}: the paired REJECTED-precision gain of the selected verifier over Vintern-1B
has **point estimate >= 5.0 points and a 95 % CI that excludes 0** (H1), with H2 (UNCERTAIN cap) and H3 (retention
non-inferiority). Never "a gain of at least 5.0". The 80 % recall of PI-1031g is a descriptive design goal, never a
PASS threshold (CC-207 W8).

**Prior art and narrowed novelty (NB-C14).** Added to R11 (identifiers checked by the CC-215r2 judges):
- POPE (Li et al. 2023, arXiv 2305.10355): yes/no object-existence probing of LVLMs;
- POPE-MUL / MME-MUL / AMBER-MUL (Qu et al. 2024, arXiv 2408.00550): multilingual hallucination probes, no Vietnamese;
- FaithScore (Jing et al. 2023, arXiv 2311.01477): atomic-fact verification of LVLM answers with a VLM verifier;
- Whitehead et al. 2022 (arXiv 2204.13631): reliable VQA, abstention / coverage-risk;
- AMBER (arXiv 2311.07397), carried from v2.

The claim is narrowed to three parts only: (i) Vietnamese prompts and label words; (ii) an UNCERTAIN class decided
**per detail type**, with its share capped and costed against recall and retention; (iii) the paired, recall-matched
precision gain over the Vietnamese 1B verifier that the VSPS pipeline uses today. Why this is more than "POPE in
Vietnamese": POPE scores a model's own yes/no answers on templated existence questions; E2b uses a model as a
**verifier of other systems' free-text details**, with abstention as a costed output and a paired operating-point
comparison against a deployed baseline. The word "first" is not used. A full OpenAlex / Semantic Scholar sweep runs
before the tier-3 prereg (NB-C14); novelty doubt is about 35 % (J2), under the 80 % pivot trigger.

## 2. Construct

### 2.1 Candidates (fixed before any output; NB-C13)

| key | hub id @ revision | registry (sha) | LM / vision | role |
|---|---|---|---|---|
| `qwen25vl_7b` | Qwen/Qwen2.5-VL-7B-Instruct @ cc594898 | B-N1 (9ff02dc2) | Qwen2.5 / own ViT | candidate; N9 applies |
| `internvl3_8b` | OpenGVLab/InternVL3-8B-**hf** @ 259a3b64 | B-N1 (9ff02dc2) | Qwen2.5 / InternViT | candidate |
| `aya_vision_8b` | CohereLabs/aya-vision-8b @ d7601ac8 | C-T1 file (09e6f90a); the same pin is used by C-T2/C-T3 and A-T3 (NB-C16 relabel) | Command R7B / SigLIP2 | candidate; the only other-family model |
| `qwen3vl_8b` | Qwen/Qwen3-VL-8B-Instruct @ 0c351dd0 | B-N1 (9ff02dc2) | Qwen3 / own ViT | optional: in only if its rate smoke passes before the 2.0 GPU-h mark |

- **Change from v2, flagged (open question Q2).** v2 named `OpenGVLab/InternVL3-8B` @ 853e3a79 with
  `trust_remote_code`. This draft uses the HF-native conversion `InternVL3-8B-hf` @ 259a3b64, already pinned file by
  file in B-N1, so every candidate loads through one audited path with no remote code. The two checkpoints are **not**
  claimed equivalent.
- **Environment.** All four candidates run in venv-lb (transformers 4.57.6; `pip freeze` sha 685ffe2a, setup_gpu.sh
  H_LB). Qwen3-VL needs transformers >= 4.57, so no separate venv is needed; v2's "own venv" clause becomes "passes the
  rate smoke before the 2.0 GPU-h mark".
- **Image input (pinned).** The registry processor kwargs: Qwen models `min_pixels` 262,144, `max_pixels` 1,048,576;
  InternVL3-hf and Aya the snapshot defaults (disclosed). The number of input tokens per probe is logged (rate and
  tier-1b rows), so the tiling actually used is on record.
- **Family rule (v2 2.1).** Two models share a family if they share the LM line or the vision-encoder line. Vintern,
  Qwen2.5-VL, InternVL3 and Qwen3-VL are one family; only Aya is other-family. "Other-family" is used only for Aya.
- **N9 (self-verification).** Qwen2.5-VL-7B (the stage-1 generator of the E1a records) is never the verifier for a
  claim on VSPS-generated records. If it wins the selection rule, it is the benchmark verifier, and the VSPS-record
  verifier is the best feasible non-Qwen2.5-VL single-model config under the same rule (`pick()`). The selection uses
  only the M-HalDetect selection set; no E1a or other VSPS record enters it.
- **Aya** is gated (CC-BY-NC-4.0): the project HF account accepts the licence; the token is passed as `HF_TOKEN` on the
  host only and never logged. No PI address is used anywhere.
- **Baseline.** Vintern-1B-v3_5 @ b98f263e, M0 arm A, **not re-run**: `probes.jsonl` sha256 **cccd5e0e** (32,054 rows =
  16,027 per arm, 769 images, field `p_yes` float, key (rec, seg); OPS-1031m0done) [measured; closes v2 l.106 "[chưa
  kiểm]", NB-C9]. `score` refuses any other file.

### 2.2 Prompts, label words and token sets (frozen; shas in `e2b_plan.json`)

- **F-A vi = M0's frame byte for byte** (`m0.instruct(m0.question(span))`): the English span inside the Vietnamese
  có/không template. The paired Vintern baseline saw exactly this text, so Δprec does not mix prompt wording and
  model. Disclosed difference in the score path: M0's `p_yes` came from `generate(..., output_scores=True)` scores,
  i.e. after `repetition_penalty` 1.05 (`m0.GEN_CFG`; có and không both occur in the prompt), while E2b reads the raw
  forward logits. Neither path is changed; the paired comparison carries this difference.
- F-A en: the English yes/no frame. F-B vi: the M0 question plus "answer with exactly one of three words: ĐÚNG, KHÔNG
  RÕ, SAI". F-B en: the same with SUPPORTED, UNCERTAIN, REJECTED. (Templates in `e2b.prompt`; this adds the EN span
  template, NB-C16.) Spans are never translated.
- **Label words:** F-A {có, Có} vs {không, Không} (vi), {yes, Yes} vs {no, No} (en). F-B uppercase only: ĐÚNG /
  KHÔNG RÕ / SAI and SUPPORTED / UNCERTAIN / REJECTED.
- **Token sets:** for each word, bare and with a leading space, the first non-blank token id (Vintern `_yes_no_ids`
  form). Sets must be pairwise disjoint per form and language, and for F-B vi the UNCERTAIN set must not share an id
  with the first tokens of plain "không" / "Không". A clash is a FAULT for that candidate x form, and that form is not
  run for it (no fix-up after seeing the clash). **The real tokenizers are not on the laptop:** this gate runs on the
  host when each model loads (`token_sets.json` is written per tier-1b run). The CPU selftest proves only the rule on
  a fake tokenizer.
- **One forward pass per probe:** softmax over the next-token logits at the last position (= one greedy step); the
  label masses are summed over each set. F-A: P(yes) = m_yes / (m_yes + m_no), internal only. F-B: argmax of the three
  masses; total mass < 0.5 -> UNCERTAIN, counted as malformed.
- **No score is ever output.** The system output is the label. Masses stay in internal logs for diagnosis.
- No few-shot (M0 DROP, dR -28.6), no training, no AI labels as gold.
- Known gold bias (CC-207 W3): unmarked M-HalDetect text defaults to Accurate. Stated here and in the paper.

### 2.3 Detail types (keyword rule v2, `e2b_type`)

M0's rule unchanged (first match count > attribute > relation > object), then M0 "attribute" splits into colour /
attribute by a fixed colour list, and M0 "relation" into action / relation by a fixed verb list (both lists are
subsets of M0's own word lists; sha `type_rule_sha256` in the plan). Hence **object and number are exactly M0's object
and count sets** (asserted by the selftest on 2,000 random phrases). Primary = {object, number} (PA3, CC-207 ruling
5); colour, attribute, action, relation are descriptive.

## 3. Data, split and custody

### 3.1 M-HalDetect val (pin 2cbc7942), the only tier-1 selection data

| set | images | segments | Inaccurate | role |
|---|---|---|---|---|
| probe split (val - 17 dropped owner images) | 769 | 16,027 | 4,605 | probed; reported beside at frozen thresholds |
| selection set (minus the 106 held) | 663 | 13,813 | 3,993 | every choice |
| - tune half | 325 | 6,731 | 1,964 | thresholds only |
| - select half | 338 | 7,082 | 2,029 | config choice only, at frozen thresholds |
| held out (91 Karpathy test + exclusion.json ids) | 106 | 2,214 | 612 | never in any choice, never in the rate run |

All [measured], equal to M0 PREREG l.98-104. Primary-type counts in the selection set [measured]: object 4,736
(1,424 Inaccurate), number 3,100 (1,322); tune / select per type in `e2b_plan.json`. 435 UNSURE spans: descriptive
only, never UNCERTAIN gold.

**Tune/select parity rule (NB-C9, fixed):** `half(id)` = sha256 over the **UTF-8 bytes of `str(int(coco_id))` +
"e2b"** (decimal, no zero padding; the M0 key `image` is an int); the **last hex character** of the hexdigest decides:
even -> tune, odd -> select. Pinned examples (selftest and plan): 139 tune, 285 tune, 632 select, 724 tune, 776
select. `half()` refuses non-int input. Author-saw note: to pin cccd5e0e, the M0 `probes.jsonl` was opened once for
its row count, arm counts, keys and the type of `p_yes`; no value was printed or used, and the plan never reads it.
Vintern thresholds are matched only inside `score`.

### 3.2 Ledger lines (NB-C11; PORTFOLIO_3Y section 2.3, one line per read, exact text in the judge-read request)

1. M-HalDetect val, selection set, rate run: 200 spans on 171 images of the 663 (plan `rate`, sha `dbd4a685...`).
2. M-HalDetect val, full 769 (tier 1b-i): includes the 91 Karpathy-test images (dev only, spent; PORTFOLIO l.188),
   held out of every choice.
3. M-HalDetect train (tier 2), 4. COCO Karpathy test object/number (tier 2), 5. UIT-ViIC test 231 (tier 1b-ii),
   6. e-SNLI-VE dev: each gets its own line **in the amendment that licenses that read**, not here.

**W25 (PORTFOLIO l.185).** The M0 (CC-208 r8) and E1a (CC-209 r6) exceptions do not carry over (v2 l.210).
- Lines 1-2 re-decode only images M0 already decoded; id intersections with A-T3 3,232 (0), KV-4,224 (0) and
  UT-2,532 (17, dropped) were removed by M0 [measured, m0_plan custody]; the exclusion.json lists (coco_karpathy_test
  91, coco2500 44, cv295 5, chair500 10, pope500 7; union 106) are held out. No near-duplicate (SSCD) pass has been run
  on these 769. **Requested here: a W25 exception for lines 1-2 (no new image decoded), open question Q5.** Default if
  refused: the tier-1b-i M-HalDetect probe waits for a W25 pass in the next amendment; the rate run is unaffected
  (timing only, no output read).
- Tier 2 (Karpathy test, M-HalDetect train): W25 against A-T3 and every other owner **before the tier-2 decode**;
  dropped intersections listed by count (KV-4,224, UT-2,532, exclusion.json).
- e-SNLI-VE dev: see 3.4.

### 3.3 Tier 1b-ii, the E1a custody arm (ruling 4, NB-C3, CC-209 Q1 open)

UIT-ViIC test 231 (records E1a) never leaves M1 or the laptop. On M1 it runs only after MT4 tier 3 (if gated in,
PI-1101q) and after B's M1 custody block (CC-217 B3); **VSPS-J slips, never A or B** (CC-207 r8). Its output goes
under `/root/vsps_j_e1a/`, which the M1 full backup pull already excludes (`--exclude='/vsps_j_e1a/'`, checked
today in `~/.config/vsps/gpu_backup.sh`). It is descriptive only and enters no choice. Its code (probing the recorded
Vintern questions with the winner) is **not in this draft**: it comes with its own amendment and judge read once M1
is free (open question Q6).

### 3.4 e-SNLI-VE dev (proxy for UNCERTAIN, descriptive; N14, B7)

Not on the laptop and not under `.session_backup/machines/` [checked by `find` today]; no SSCD feature cache for it
exists. **W25 decision:** e-SNLI-VE dev is **not read in this block**. Before any read, an amendment names (a) the
machine: M1 (machine id m3), where the W25 environment (`venv-cenfeat`, `scripts/w25/w25.py` rule C1/C2/C3) and C's
Flickr30K test staging live; (b) a fresh feature cache `/root/e2b_w25/feats_esnlive_dev.npz`, pinned by sha after
computation; (c) the comparison sets: Flickr8K-Expert (B, sealed; image bytes only), C's Flickr30K Karpathy test and
every ledger owner. Counts only (PI-1101o). e-SNLI-VE test stays sealed. It slots on M1 under the same ordering as
3.3.

### 3.5 AMBER (NB-C15, CC-207 Q2 NOT YET)

AMBER's truth source is `inference.py` (truth = `ground_truth[id-1]['truth']` from `data/annotations.json`), cited
instead of the README. `annotations.json` has never been fetched or read. **Correction to v2 l.236-237:** one copy of
the AMBER discriminative query file (no answers) **still exists**:
`/tmp/claude-1000/-mnt-d-vsps-image-captioning/5a363495-c9d6-40f3-8f9c-a7285ef7a0e6/scratchpad/amber/qd.json`,
1,738,529 bytes, sha256 1502887a..., written 2026-11-01 20:02 VN during the v1 drafting. v2's `find` searched by the
original file name and missed it. It was hashed today, not opened. Recommended: delete it and log the sha (open
question Q7). The AMBER key stays unread until an irreversible >= 92 panel approves a tier-3 choice.

### 3.6 Boundaries (ruling 7, NB-C10)

- **Reciprocal B line:** B's verifier is chosen only from B's own tier 1, never from E2b outputs; E2b's number gold
  (iscrowd rule, v2 4.4) and B's (section 3.3 K cap) differ by design. The same sentence goes into B's prereg.
- C's verifier is never chosen from E2b outputs (CC-214); VSPS-J reports no C downstream result; Objects365 v2 val
  stays B's.

## 4. Tier-1 rules (scored once, `e2b.py score`, laptop)

### 4.1 Operating points

- **F-A band, per type, on the tune half:** t_lo = the smallest value on {0.05, ..., 0.95} with strict recall >= 0.83
  (design goal 80 + 3; under F-A, dev recall is therefore near-tautological and carries no evidence, B1); t_hi = the
  smallest grid value >= t_lo with P(gold true | p >= t_hi) >= 0.90, else t_lo (empty band); while the tune UNCERTAIN
  share > 12 %, t_hi steps down the grid toward t_lo (the cap wins over the 0.90 floor). No feasible t_lo, or no
  gold-false probe in that type -> one threshold 0.5. A probe at p = t_lo is REJECTED.
- **F-B:** no knob.
- **Vintern recall-matched, per config and type:** t_lo(Vintern) = the lowest distinct tune p_yes whose strict recall
  reaches the config's tune strict recall (none rejected if that recall is 0); then the same t_hi rule and 12 % cap.
  Both systems are 3-label systems under one band rule. The residual tune recall gap and the select-half recall gap
  are reported.
- Thresholds from the tune half are final; never refit on all 663, never touched on select or held images.

### 4.2 Candidate configurations (complete list, NB-C13)

- 8 single-model configs: {qwen25vl_7b, internvl3_8b, aya_vision_8b, qwen3vl_8b} x {F-A, F-B}, vi frames, minus any
  candidate x form dropped by the rate run (keep rule, token FAULT, smoke FAULT, error after one retry).
- 2 PA2 vote configs: Vintern-1B (its own F-A band on its M0 p_yes) with Aya F-A, and with Aya F-B: REJECTED if either
  rejects, SUPPORTED if both support, else UNCERTAIN. **PA2 is eligible only if no single-model config is feasible.**
- Nothing else. The EN frame runs only for the winner, descriptive.

### 4.3 Selection rule (select half, frozen thresholds; `pick()`)

- Per config: Δprec = macro REJECTED precision (config - its matched Vintern) over {object, number}; U = the config's
  macro UNCERTAIN share; Δret = macro retention difference.
- Feasible: U <= 12 % and Δret >= -2.0 (point estimates).
- Winner: the largest Δprec; within 0.5 points prefer F-B, then Aya, then the candidate order above. Then N9.
- If nothing is feasible: no tier 2; PA1 (Pareto report) / PA4 (measurement paper) per v2 section 6.
- Macro is fixed a priori: equal weights; a type with an undefined metric is left out and recorded.

### 4.4 Same-backbone ablation (NB-C4, descriptive, mandatory)

The winner forced binary vs its 3-label output, at matched tune strict recall, same backbone, select half:
- F-A winner: binary = REJECTED iff p <= t_lo, else SUPPORTED. The REJECTED set is identical by construction, so the
  ablation shows what the band costs or buys in retention and SUPPORTED precision.
- F-B winner: q = m_R / (m_R + m_S) (renormalised over the two label sets); binary = REJECTED iff q >= cut, cut = the
  highest tune q whose strict recall reaches the 3-label tune recall of that type.
- **Attribution rule:** until this ablation shows a gain of the 3-label output over its binary twin, paper text credits
  H1 to the 8B verifier versus the 1B baseline, not to the 3-label scheme (ruling 6).

### 4.5 Reported (descriptive)

Per config and type: REJECTED precision, strict and loose recall, retention, SUPPORTED precision, UNCERTAIN share,
malformed share (F-B). For the winner: image-cluster bootstrap CIs on the select half (B 10,000, seed 20261101; Δprec,
U, Δret, Δrecall), the full 769 and the held 106 at frozen thresholds, the EN-frame arm, recall vs the 80 % goal.

## 5. Registered now for the later tiers (binding on the tier-2 / tier-3 preregs)

- **H1:** Δprec point estimate >= 5.0 and 95 % CI LB > 0. **H2:** macro UNCERTAIN <= 15.0 % (point). **H3:** 95 % CI
  LB of Δretention > -2.0. PASS = all three (intersection, no alpha split). CI: paired image-cluster bootstrap,
  B 10,000, seed 20261101, ratio estimators per type, then macro, then difference; replicates with an undefined
  primary precision are dropped and counted; > 1 % dropped = FAULT (`paired_ci`).
- **H4, recall-drift guard (NB-C2, mandatory before the tier-3 prereg and any tier-3 output):** 95 % CI LB of the
  paired strict-recall difference (selected - Vintern) > -2.0, as a PASS conjunct (PI Q-recall default YES). Reason:
  thresholds are matched on English span-form dev and then applied to the VI/EN templates, so an H1 gain could be
  bought by a template-induced recall drop.
- **Why -2.0, fixed a priori (NB-C6):** (a) it equals the program's earlier precision floor (E1 H1 floor P0 - 2.0),
  so one margin governs the program; (b) it sits below the M-HalDetect annotator ambiguity (UNSURE 435 / 16,885 =
  2.6 % [measured, v1 section 3]), so a smaller loss cannot be told from gold noise; (c) in use, it means at most one
  more correct detail lost per 50 correct details.
- **Why 15 %, fixed a priori (NB-C6):** the tier-1 tune cap is 12 %; +3 points is the same slack as the recall design
  margin (80 + 3) for the tune-to-test shift. Above about one detail in seven unresolved, the 3-label output hands too
  much back to manual review to count as a verifier. These are reasons, not data.
- **Tier-2 P(PASS) >= 0.98 (NB-C6, three-tier rule):** nested image-cluster bootstrap on the frozen tier-2 config.
  Outer: unit = image, B_out 500, seed 20261102; each replicate draws n_T3 images with replacement from the tier-2
  pool (n_T3 = the registered tier-3 image count once tier 3 is chosen; until then the tier-2 pool size). Inner: the
  full H1-H4 rule, each CI with B_in 1,000, seed 20261102 + replicate index. P(PASS) = the share of outer replicates
  passing all of H1-H4 jointly; its Monte Carlo SE is reported. Per-image, per-type count tables (`per_image_counts`)
  make this cheap. Below 0.98: no test touch. Code comes with the tier-2 amendment.
- **Tier 3** (AMBER after CC-207 Q2, or VALSE) is not decided here (irreversible, >= 92).
- **NB-C8 gate:** tier-1b spend waits until a feasible tier-3 candidate exists: the VALSE desk check (section 10) is
  completed to a ledger decision, or CC-207 Q2 is answered.

## 6. The unscored rate run (block 1a; v2 5.1 as corrected; NB-C3, NB-C7, NB-C12)

- **Slot.** M8 = the dedicated RTX 4090 of PI-1101r (shared by B tier 1, C and E2b, each after its own GO). The rate
  run runs **alone** on that GPU: the job refuses a non-4090 or a busy GPU at launch, and `e2b.py` checks
  `nvidia-smi --query-compute-apps` before and after each candidate by a count rule (no compute app before this process
  initialises CUDA, at most one after; PIDs are not compared, since container and host PID spaces may differ); any
  other compute process -> FAULT (a shared GPU invalidates s/probe). It queues behind ready B tier-1 and C jobs (judge.md rule 3; VSPS-J has no date). It starts
  only after (i) this draft's judge read and the gatekeeper commit and (ii) the PI's logged top-up (kept unless the PI
  lifts it, Q-top-up). v2's "delete the machine right away" and the M1 option are void (M8 is shared; NB-C17: the M1
  rate run is not carried over).
- **Images:** only the plan's 171 images (200 spans) from the 663-image selection set; no held image, no UIT-ViIC.
  Bytes pinned by sha in `e2b_plan.json` (from M0's pulled `images.sha256`, 7a3f3468); none matches exclusion.json.
  The plan also pins all 769 probe images for tier 1b (`probe_images`; only held ids may match exclusion.json).
- **Preflight before t0:** plan, image shas, the `val_raw.json` pin, the span-image mapping and all four registry
  entries are checked before `launch.json` is written, so a mis-staged input neither starts the clock nor spends the
  one resume. A snapshot pin mismatch is a FAULT with a STOP marker.
- **Candidates:** the four of 2.1, in that order; Qwen3-VL last and only if its smoke passes before 2.0 GPU-h.
- **Cap 3.0 GPU-h from t0, downloads included.** t0 = `launch.json`, written by `e2b.py rate` **before the first
  snapshot fetch**; every fetch runs inside the clock. This supersedes v2's "t0 = billing start" (M8 is shared, and
  PI-1101r lets setup run before any GO). At the cap: CAP_STOP, the rest is not run.
- **Per candidate x form:** token-set gate; smoke on the first 10 items (finite masses and label mass >= 0.5 on all
  10; booleans only); then 200 timed probes through **the exact tier-1 probe function**.
- **Unscored by construction:** rate rows carry only {cand, form, i, sec, n_tok, phase} (`RATE_KEYS`; `rate_row`
  raises on any other key; selftest). No p_yes, no label mass, no text. `rate.json` holds per form n, mean, median,
  keep, the median input tokens, load time, peak VRAM, image-prefix reuse (none).
- **Keep rule (NB-C12).** The 1.7 3090/4090 factor and the 1.0 s/probe (3090) threshold were fixed in advance and
  never measured. The rate is measured on the 4090 directly. **Keep a candidate x form iff its MEAN s/probe <=
  0.50 s on the 4090** (= 0.85 / 1.7: the threshold may not exceed the 0.85 s/probe upper bound behind the 22-93 GPU-h
  table, and 0.50 also sits under that table's 4090 top of 0.53). The ruling text also names 0.59 (= 1.0 / 1.7); 0.59
  would put the table's top out of range, so this draft registers 0.50 (open question Q1). 1B rates are not
  transferred to 7-8B.
- **Errors:** an OOM or load error gets one retry inside the cap; a second failure drops that candidate. A crashed
  process may resume once (`launch.json` start counter); a STOP is never resumed.
- **OUT and backup (NB-C3 correction).** v2 l.354-356 is false: `gpu_backup.sh`'s full pull copies all of
  `root@host:/root/` minus a fixed exclude list, and **M8 is in its machine list**; `/e2b_rate/` is not excluded.
  Launch precondition: the operator adds `--exclude='/e2b_rate/'` to that full pull and restarts the M8 loop, logged
  in the launch OPS line (the laptop config is not in the repo; nobody edits it as part of this draft). Snapshots go to
  `/root/.cache/e2b_hub`, and the job refuses `DATA` / `IMAGES` outside `/root/.cache/`, which the pull already
  excludes. If the exclude were
  missed, the copy would hold timing rows only (no scores, no text). Pull by hand once to
  `.session_backup/2026-11-0x/e2b_rate/` with `OUT_MANIFEST.sha256`, re-checked on the laptop.
- No host, IP or port is written in the repo; "M8" is the only name used.
- **Commands:** `PY=/root/venv-lb/bin/python bash scripts/vsps_j_e2b/e2b_job.sh --selftest`, then
  `PY=... HF_TOKEN=... DATA=<val_raw.json dir> IMAGES=<171 images> bash scripts/vsps_j_e2b/e2b_job.sh rate`. The job
  checks three SUMS files, the LB loader shas, the venv-lb freeze, runs the selftest, and writes the OUT manifest.

## 7. Tier-1b blocks (not licensed by this draft)

| block | probes | machine | gate |
|---|---|---|---|
| 1b-i M-HalDetect val, each kept candidate x form, vi frames | <= 8 x 16,027 | M8 (alone not required) | post-rate amendment with per-block caps; NB-C8; W25 decision (Q5) |
| 1b-i EN frame, winner only | 16,027 | M8 | same |
| 1b-ii E1a custody arm | about 18.4k + about 5k per kept config | **M1 only** | section 3.3 ordering; own amendment |
| e-SNLI-VE dev | <= 17,858 | M1 | section 3.4 W25 first; own amendment |

- `e2b.py probe` (written, selftested on CPU): refuses a candidate x form without keep=true in the pulled `rate.json`;
  checks the 769 staged images against the plan shas before t0;
  M0's seeded image order over the 769; per-probe rows (rec, seg, image, label masses, n_tok, sec); projection before
  every image = GPU-h used since the first t0 (resume included) + remaining x running MEAN s/probe (the rate mean
  before the first probe); projection > block cap -> PROJECTION_STOP; FAULT on a non-finite mass; one resume.
- Cost at the keep bound: 8 x 16,027 x 0.50 s = 17.8 GPU-h at most, plus 2.2 h for the EN arm; the post-rate amendment
  restates it from the measured means.

## 8. STOP and FAULT rules

- Rate run: FAULT (exit 2) on a foreign GPU process, plan / image / registry / snapshot pin mismatch; CAP_STOP (exit 4)
  at 3.0 GPU-h. A token or smoke FAULT drops only that candidate x form and is recorded.
- Tier-1b: FAULT on a non-finite mass; PROJECTION_STOP (exit 3); every stop writes the M0 STOP marker; a stopped
  folder is never resumed or scored (`m0.refuse_if_stopped`).
- Score: refuses a stopped run, a probes file not equal to its `.sha256`, incomplete coverage of the 16,027 segments,
  or any M0 file other than cccd5e0e. Bootstrap > 1 % undefined replicates -> FAULT.

## 9. What tier 1 can and cannot claim

- **Can (dev-explore):** which config the fixed rule selects; its recall-matched Δprec, UNCERTAIN share and Δretention
  against Vintern-1B on the select half, with CIs; the binary-vs-3-label ablation; s/probe of 7-8B verifiers on a 4090.
- **Cannot:** any test or tier-3 claim; any >= 80 % recall claim; any claim that the 3-label scheme (rather than model
  scale) causes the gain unless 4.4 supports it; any cross-family claim except for Aya; any result on VSPS records
  (E1a is descriptive and not in this block).

## 10. VALSE desk check (NB-C8, N12; CPU, 2 web fetches (README page, paper PDF parsed locally), no data downloaded)

- **Licence:** the GitHub repository (Heidelberg-NLP/VALSE) is MIT. No separate licence is stated for the annotation
  files; images are fetched from the source datasets under their own terms (README).
- **Sources** (paper, arXiv 2112.07566, Table 1 and section 3): existence and counting from Visual7W (COCO images);
  plurality and spatial relations from **COCO 2017 val**; actions from SWiG (imSitu images, not COCO); coreference
  from VisDial v1.0 (COCO images; train set plus a small val "clean" set); Foil-it from FOIL-it (COCO).
- **Foil construction (Table 1):** existence (nothing <-> something) and counting (numeral replacement) are rule-based
  from human Visual7W answers; plurality is rule-based NP replacement (sg2pl / pl2sg, quantifiers) filtered by GRUEN
  and an NLI model; relations use SpanBERT (MLM) proposals filtered by GRUEN and NLI; actions use SWiG roles with
  BERT (MLM) proposals; coreference is yes <-> no. Every instance was validated by three crowd annotators (valid = at least
  2/3). For E2b's primary types (object ~ existence, number ~ counting) the foils are rule-based from human answers,
  so they do not fall under the "AI-silver negatives" exclusion that removed SugarCrepe; the MLM-built pieces
  (relations, actions) would.
- **Overlap (source level only):** every COCO-based piece can intersect our ledger. COCO 2017 val is drawn from the
  2014 images, so plurality / relations can hit Karpathy test (spent dev), M-HalDetect (dev-touched), A-T3's 593
  val2017 ids (sealed) and KV-4,224; Visual7W-based existence / counting can hit the same pools. Per-image overlap
  needs VALSE's image ids, i.e. an id-only fetch, which this check did not do.
- **Form:** caption vs foil (pairwise), not the yes/no template form; per CC-207 ruling 5, a VALSE tier 3 needs a
  same-form tier-2 rehearsal, or tier 3 narrows to English with Vietnamese descriptive (v2 R5).
- **Status for NB-C8:** licence checked; overlap known at source level only. The gate is **not yet met**: it needs a
  ledger decision to fetch VALSE ids only (existence + counting files, ids parsed by a script that prints counts, text
  never displayed) and a W25 / id-overlap count against every owner (open question Q4).

## 11. CC-215r2 non-blocking map

| item | where closed |
|---|---|
| NB-C1 licence scope | header |
| NB-C2 recall-drift guard (H4) | section 5 |
| NB-C3 backup sentence, E1a output path | sections 3.3, 6 |
| NB-C4 same-backbone ablation | section 4.4 |
| NB-C5 H1 wording | sections 1, 5 |
| NB-C6 -2.0 and 15 % reasons; tier-2 P(PASS) spec | section 5 |
| NB-C7 slot text (M8 alone, queue, top-up, E1a order) | sections 3.3, 6 |
| NB-C8 tier-1b gate; VALSE check | sections 5, 7, 10 |
| NB-C9 probes pin cccd5e0e; parity rule | sections 2.1, 3.1 |
| NB-C10 reciprocal B line | section 3.6 |
| NB-C11 ledger lines, W25 | sections 3.2, 3.4 |
| NB-C12 cost labels; keep threshold | section 6 |
| NB-C13 full candidate set incl. PA2 | section 4.2 |
| NB-C14 novelty, R11 | section 1 |
| NB-C15 AMBER inference.py; copy status | section 3.5 |
| NB-C16 stale wording, EN template, Aya pin label, round-2 header | header, sections 2.1, 2.2 |
| NB-C17 v1 clauses not carried | sections 3.5, 6, 3.1 (selection set only) |

## 12. Open questions for the judge read (each with a recommendation and a default)

| # | question | recommendation | default |
|---|---|---|---|
| Q1 | Keep threshold on the 4090: 0.50 s/probe (fits the 0.85 bound and the 22-93 GPU-h table) or 0.59 (ruling text; needs the table top recomputed)? | 0.50 | 0.50 |
| Q2 | Accept InternVL3-8B-hf @ 259a3b64 (B-N1 pinned, no remote code) in place of v2's InternVL3-8B @ 853e3a79 (remote code)? Not claimed equivalent | yes | yes |
| Q3 | Qwen3-VL-8B is in venv-lb already: keep it optional (smoke before 2.0 GPU-h) rather than a full candidate? | keep optional | optional |
| Q4 | Allow an id-only fetch of VALSE existence + counting files to count per-image overlap (ids parsed by script, text never shown), with its own ledger line? | yes, after this read | no fetch |
| Q5 | W25 exception for the M-HalDetect val re-read (769 images M0 already decoded; id intersections already dropped)? | yes | no: tier-1b-i waits for a W25 pass |
| Q6 | Tier 1b-ii (E1a, M1) and e-SNLI-VE get their code and caps in separate amendments, not in this prereg? | yes | yes |
| Q7 | Delete the leftover AMBER query-file copy (sha 1502887a, never opened today) and log the deletion? | yes | keep untouched, disclosed |
| Q8 | Rate-run disk: four snapshots (about 17 GB each, about 70 GB) stay in `/root/.cache/e2b_hub` for tier 1b, unless the host disk is short | keep | keep |
| Q9 | One aislop finding stays open: `e2b.py` is over the 400-line size rule and two functions take 7-8 parameters; split into e2b.py + e2b_score.py before the commit? | split at commit time, no logic change | leave |
