# Amendment to B-PA1-T1 prereg v3.1: scoring rules for its §6.4 steps 6-8 (v1)

Status: **DRAFT for the CC-316 round-2 read; not pinned, not committed.** Written 2026-11-11T01:53:15Z (`date -u`).
Label: `TIER 1 / DEV-EXPLORE (B-PA1-T1)`. Amends `PREREG_DRAFT_v3_1.md` (`e9b30ca7…`, commit 5ff00c9), namely
v3.1 §1 l.91-92, §6.4 steps 6-8, §7.1, §7.3, §8.1-§8.3, §8.5, §8.6 and §11. v3.1 is not edited. This amendment takes
effect when its sha is on the pin line of §10 below. That line must come before the `SHA256SUMS_rest` pin line, which
is the only mechanical lock on `join` (CC-316 Ruling 3), and so before the first read of `annotations[]`.
Basis: CC-316 (`116b421e`, LOG l.2090) W1, W2, W5, W6, W10; coordinator decision LOG OPS-1111d-cc316 (l.2092) under
PI-1109d / PI-1110i. No Objects365 class name and no map term appears in this file (CC-228); examples use made-up
tokens. **In this file a bare "§n" is a section of this amendment; a section of the prereg is written "v3.1 §n".**

## 0. What had been opened when these rules were fixed

- **No governed output of the tier-1 run has been opened.** The LOG lines that record it:
  - OPS-1110b-t1-handoff (l.2047): the hand-off; steps 6-8 are listed as next, "each after its code read";
  - OPS-1110g-b-t1-status (l.2057): sets re-verified by sha, "blocked at prereg v3.1 s6.4 step 6 (gold join)";
  - OPS-1110i-b-scorer-written (l.2060): "no governed output, gold or sealed path opened, nothing run on real data";
  - OPS-1111d-cc316 (l.2092): the Q1 and Q2 rules are "fixed before any governed output is opened".
- Earlier reads of run outputs on record:
  - the registered mechanical steps of the run itself: the acceptance walk and trim records, and the step-4 coverage
    count over the A1 captions (v3.1 l.370; LOG l.1984, "counts only");
  - at the hand-off, "only file names, line counts, sha256 values and the STOP / EXIT lines of `logs/job.log`"
    (`T1_HANDOFF_STATUS_2026-11-10.md` §1).

  On this record, no decomposition, verification, judge or CLIPScore row has been read.
- `annotations[]` of the train annotation file has never been read: its first read is step 6 (v3.1 l.374).
- `SHA256SUMS_rest` has no LOG pin line (CC-316 Ruling 3), so `join` refuses today.
- The writer of this file opened no pulled output, no sealed path and no `annotations[]` content. Inputs: the
  registered text, CC-316, the code, and structure counts of the frozen final map.

Frozen final map `866b5cb7` (LOG l.1992; a frozen registered input, not a governed output). Structure counts,
reproduced by the writer from `.session_backup/b_pa1_t1_step4_1108/final/b_pa1_map_final.json` and equal to CC-316
l.34-36: 570 terms, 658 rows, **37 terms with more than one row** (at most 8), 336 classes, **192 classes named by
more than one term**, 16 terms with rows of both tags, 5 terms with no row. Rules §1(b)-(d) will therefore apply on
the real data.

## 1. Gold object precision of a caption (CC-316 Q1; W1, W10)

Registered lines that this section extends:
- v3.1 l.91-92: "computed only on **mapped object propositions** (head noun maps to an Objects365 class through the
  frozen map, §6)";
- v3.1 l.351, the parity rule: "a mention is a distinct COCO-80 class named in one reference";
- v3.1 l.416: "Primary: captions with defined gold precision (≥ 1 mapped mention) and a defined B score";
- direction l.156: "Mention không ánh xạ được vào lớp nào được **loại** khỏi precision ở phân tích chính";
- erratum (d): "every Vietnamese term of A's lexicon gets one VN → Objects365 row per Objects365 class that the
  crosswalk links to the term's COCO-80 class".

None of them says how a term with several rows, or two terms of one class, is scored. The rule below is the
coordinator's decision (OPS-1111d-cc316), which takes CC-316's recommended answer.

**(e) Matcher.** M(text) = `score_coco_probe.vi_objects(text, terms)` with its default lexicon `"v2"` and
`RESCAP_RAW_TONE` unset. `terms` is every term of the final map in the map's file order, each paired with itself:
`[(t["vi"], t["vi"]) for t in map["terms"]]`, as on the new-map side of parity run 2 (`map_v1.parity`). M returns a
**set** of map terms. The file order governs, with the shadowed terms as ruled in CC-296r3 (W10). The matcher runs
over all 570 terms. A tag set is applied only afterwards, so a term outside the tag set, or a term with no row, still
consumes the span it matches.

**(a) Unit.** For a tag set T, a **mention** of a caption is one term of M(caption) that has at least one row tagged
in T. M returns a set, so a term that occurs several times in one caption is one mention. This is the term-level form
of "distinct … named in one reference" (l.351). A matched term with no row in T is not a mention. It is excluded
(direction l.156), and step 6 counts the hits of terms that have no row at all.

**(b) Hit rule: ANY-OF.** A mention is **correct** iff at least one of its rows tagged in T points to a class that
has at least one annotation record for the image (§8(a) below). A term with several rows is one mention, never one
mention per class.

**(c) Two terms, one class.** Two different terms of M(caption) are two mentions, each scored by (b), also when they
point to the same class.

**(d) Tag sets.** Primary analysis: T = {`dictionary`, `instrument`}. Dictionary-only rows of v3.1 §6.2: T =
{`dictionary`}. Rows of a term outside T are ignored in (a) and (b).

**Gold precision** = correct mentions / mentions. With no mention it is undefined; the caption leaves the
gold-defined set and is counted (l.416-418).

Example with made-up tokens. Rows: `zthu` → classes 1 and 2; `zcun` → class 2; `zcho` → class 2. Caption
"zthu zcun zcho zthu"; the image has a box of class 1 only. Mentions: `zthu`, `zcun`, `zcho` (three; `zthu` once).
Correct: `zthu`, because class 1 is boxed. Precision 1/3.

## 2. Mapped object proposition: the head noun (CC-316 Q2; W1)

Extends l.92 (quoted above) and l.384-385: "score = share of mapped object propositions answered yes among those not
abstained".

An object proposition (decomposition `type` = `object`) is **mapped** under tag set T iff M(its `object` string)
contains at least one term with a row tagged in T. M is the matcher of §1(e): the same function, lexicon, term list
and order as on the gold side.
- No other normalisation is applied to the string before M.
- An empty `object` string is unmapped.
- A string in which M finds several terms is still one mapped proposition; B's score needs no class.
- T is the tag set of the analysis (§1(d)), the same on the gold side and on B's side.

## 3. Undefined values (CC-316 Q3; W2)

A τ_c is undefined when one of its two columns is constant, or when fewer than two captions enter it.

**3.1 Step 7 (no B output is open yet): stop.** `thresholds` stops, writes no file, and the case goes to a judge
when:
- (a) a J-a, J-b, J-c or CLIPScore value of any A1 caption of the 4 accepted captioners is null (possible only when
  p(Y) + p(N) = 0 or the digit mass is 0); or
- (b) the point τ_c against gold of any of these four baselines on the gold-defined set is undefined; or
- (c) a bootstrap replicate that enters SE_A is undefined.

(a) is CC-316's rule. (b) and (c) give the same stop to an undefined τ at step 7 (§11 O1). SESOI is never formed
from an undefined SE_A.

**3.2 Step 8 (B outputs are open): no stop; the rule is fixed here.**
- **(a) Replicate.** Δ*_j of a resample is undefined when either τ_c in it is undefined. An undefined Δ* **ranks
  below every defined replicate**. It is therefore counted in #{Δ*_j ≤ SESOI}, and as ≤ −NI for H1a. A percentile
  bound that falls on an undefined replicate, or interpolates with one, is itself undefined: it is printed as null,
  and the comparison it enters is false. With B = 10,000 and linear interpolation (§7), the one-sided 95% bound uses
  the 500th and 501st smallest replicates, so it is defined iff at most 499 replicates are undefined. The 97.5% bound
  uses the 250th and 251st, so it is defined iff at most 249 are. The number of undefined replicates of each
  hypothesis is printed.
- **(b) Point.** A hypothesis whose point Δτ_c is undefined (either τ_c in it is undefined) does not pass. In code
  this follows from (a): a τ_c that is undefined on a caption set is undefined on every resample of that set, so
  p = 1 and the bound is undefined. An undefined point Δτ_c(B − judge) counts as the PA3 effect trigger **fired**.
- **(c) Lever.** If the τ_c of B (0.5-imputed, v3.1 §7.2) of any compared configuration is undefined, no
  configuration is selected: `config` is null, H1a, H1b and H1c do not pass, the PA3 effect trigger counts as fired,
  and no further B-τ row is computed.
- **(d) Descriptive rows** (τ_b, v3.1 §8.7, the 0.5-imputed set, abstain-as-wrong, dictionary-only): an undefined
  value is printed as null. No verdict depends on them.
- **(e)** Every undefined number is written as JSON `null`, never as NaN.

## 4. Tier-1 planning P(PASS): NOT COMPUTED, a recorded deviation (CC-316 Q4; W2)

v3.1 l.473-475 fix the form, and l.476 says: "Tier 1 prints the same number from slice A as a planning value". Three
inputs have no registered value:
- N_val: "N_val chưa xác nhận ở nguồn gốc" (direction l.238; 80,000 comes from a secondary source, and the val
  `images[]` count is the tier-3 P2 step, v3.1 l.130);
- the unit of n for slice A;
- the seed of ε.

CC-316 allows two options: fix the three values now, or record a deviation. It recommends the deviation, and this
amendment takes it. **The tier-1 planning P(PASS) is not computed.** This drives no tier-1 label: the tier-1 effect
trigger is the point Δ (l.559), and the 0.98 gate belongs to tier 2 (l.562). `T1_RESULT.json` carries the text
`NOT COMPUTED at tier 1 (recorded deviation from v3.1 l.476; AMENDMENT_T1_SCORING_RULES_v1.md §4)`. The deviation
gets its own OPS line (§10). The tier-2 prereg fixes N_val, the unit of n and the ε seed before slice B is opened.

## 5. Descriptive rows without a formula; `T1_CONFIG.json` (CC-316 Q5; W6)

v3.1 l.548-551 list partial τ (mentions per caption controlled), the count-matched analysis, the COCO-80 restriction
and system-level τ as descriptive tier-1 outputs. No formula is registered for them, and this amendment defines none.
CC-316 offers two routes and recommends neither (§11 O6). So that the consequence is not decided after the fact:
code v2 does not compute these rows. Unless a later amendment that defines them is committed before step 8 runs, each
is computed afterwards, labelled POST HOC beside the registered rows, with no verdict (PI-1110n item 6). The same
holds for the distinct-class reading of gold precision (§11 O7).

`T1_CONFIG.json` (l.543-544, l.410-413) is assembled after step 8 from `T1_RESULT.json` and the registry, by a small
separate script under its own read, before the tier-2 prereg.

## 6. τ by the registered scipy call (CC-316 Q6; W3)

v3.1 l.431: "τ_c via `scipy.stats.kendalltau(x, y, variant="c")`, scipy pinned in the venv freeze". The R2-pinned
venv `~/.venvs/c_stage1_lists` (freeze `1a639a50…`, LOG l.938 and l.1224) holds `scipy==1.18.1` and `numpy==2.5.4`.
The writer froze it again on 2026-11-10 (UTC) and got the same sha. Every point τ_c and every bootstrap replicate is this
call. A replicate is the call on the expanded resample, in which an image drawn k times contributes its captions k
times. τ_b is the same call with `variant="b"`. Both output files record `scipy.__version__`. The earlier package
line "No scipy" was wrong (CC-316 W8).

## 7. Conventions (CC-316 Q7; W5). The tier-2 prereg copies them verbatim (v3.1 l.436)

1. **Percentile:** `numpy.percentile` with its default linear interpolation. The one-sided lower bound at level
   1 − α is the 100·α percentile of the B replicates.
2. **SD:** `numpy.std` with ddof 0 (SE_A).
3. **Generator:** one `numpy.random.default_rng(20261101)` per bootstrap call. Each resample is one draw
   `integers(0, n, n)` of image indices, shared by every statistic of that call, so deltas are paired. The calls are:
   SE_A at step 7; the primary analysis at step 8 (B, judge, CLIPScore, B_open); the dictionary-only analysis at
   step 8.
4. **Resampling unit:** the n images that have at least one caption in the caption set of the call, in ascending
   image id. The sets are the gold-defined set for SE_A, the primary analysis set at step 8, and the dictionary-only
   analysis set for its rows. It is never all 2,000 slice-A images. All captions of a drawn image in that set move
   together.
5. **Ties in a selection:** "within 0.005" is inclusive. A candidate is in the tie band iff τ_c ≥ best − 0.005, and
   the first candidate of the registered order in the band is kept.
6. **Holm:** p_j = (1 + #{Δ*_j ≤ SESOI}) / (B + 1). A step passes iff p ≤ α. Hypotheses are ordered by ascending p;
   with equal p, H1b is first. **The p form governs** where the p form and the CI form of v3.1 §8.3 disagree
   (CC-316's recommendation). The CI lower bound at the Holm level is printed beside it, with a flag `forms_agree`.
7. **H1a:** passes iff the 5th percentile of Δ*(B − judge) > −NI.
8. **PA3 effect trigger:** fires iff the point Δτ_c(B − judge) is not ≥ SESOI. This is "< SESOI" of l.559, plus the
   undefined case of §3.2(b).

`T1_THRESHOLDS.json` and `T1_RESULT.json` carry these conventions in a `conventions` field.

## 8. Readings that CC-316 found determined (Q8), recorded

- (a) Every annotation record of an image counts as a box, `iscrowd` records included. v3.1 names `iscrowd` only for
  count propositions (l.97-98).
- (b) Dev contacts are the image ids of every row of every `out/` jsonl of the pull except `walk.jsonl` (l.143
  "decodes or scores"). Block-W feature images are neither decoded nor scored. A1 decodes all 2,000 images, so the
  contacts must equal slice A exactly; `contacts` refuses otherwise.
- (c) The scorer does not read the registry or the crosswalk, so it does not pin them.

## 9. Why these rules cannot bias the result

- **Timing.** They are fixed before any annotation or score is read (§0). `join` stays locked until the
  `SHA256SUMS_rest` pin line, and that line is written only after this file and code v2 have a GO and are committed.
- **Source.** Each rule comes from the registered text, from CC-316's reading of it, or from structure counts of the
  frozen map. None comes from an outcome.
- **Direction.** Every rule for an undefined value either stops before a B output is open, or counts against the
  hypothesis.
- **Code pins.** The rules are implemented by:
  - `scripts/b_pa1/b_pa1_score_v2.py` `4ab648e433918be89d416a0c8be60117675e4cf8b643e4269bc1c5c0a1e063cc`;
  - `scripts/b_pa1/b_pa1_score_v2_mutants.py` `fe939e7188d1c041403d295902120bd88dfcabdcb9f01786f548f1bded78272f`;
  - `scripts/b_pa1/SHA256SUMS_SCORE_v2` `227c724f7837a5b5e23fe2d0176405407126b80b4a8665d332129117507e32dc`.

  Its imports are unchanged and already pinned: `b_pa1.py` `c481fcf4`, `b_pa1_mid.py` `b8afa120`, `map_v1.py`
  `6bcab7e4`, `scripts/score_coco_probe.py` `d11db7e1`. `JOIN.json` records the scorer sha and these four shas;
  `thresholds` and `tau` refuse if any differs. A later code revision needs its own read and a new sums file. It may
  not change a rule of this amendment.

## 10. Pin and deviation lines (gatekeeper; after the round-2 GO, with the commit)

`<date -u +%FT%TZ> OPS-<MMDD>b-t1rules-pin: PIN manuscript/prereg/2026-11-01_b_pa1_tier1/AMENDMENT_T1_SCORING_RULES_v1.md <full sha256 of this file> PIN scripts/b_pa1/SHA256SUMS_SCORE_v2 <full sha256> (amendment to prereg v3.1 per CC-316 W1, W2: gold mentions any-of, head noun through the matcher, undefined values, tier-1 P(PASS) not computed, conventions; fixed before the first read of annotations[]; code v2 per SHA256SUMS_SCORE_v2; read by CC-<id> GO; commit <id>)`

`<date -u +%FT%TZ> OPS-<MMDD>b-t1-ppass-deviation: DEVIATION from prereg v3.1 l.476: the tier-1 planning P(PASS) is NOT COMPUTED (AMENDMENT_T1_SCORING_RULES_v1.md §4; CC-316 Q4, recommended option). Reason: N_val is unconfirmed (direction l.238; the val images[] count is the tier-3 P2 step, v3.1 l.130), and no n unit or ε seed is registered; choosing them after Δ is seen would be post hoc. Registered checks that still bind: the tier-1 PA3 effect trigger is the point Δτ_c(B − judge) < SESOI (l.559); the P(PASS) ≥ 0.98 gate is tier 2 on slice B (l.562, form l.473-475).`

The `SHA256SUMS_rest` pin line of CC-316 Ruling 3 is written only after both lines above.

## 11. Open points for the round-2 judge

| # | point | what this file does | status |
|---|---|---|---|
| O1 | §3.1(b), (c): an undefined baseline τ or SE_A replicate at step 7 | stop, as for a null value | extension of CC-316's sentence, which names only the null value |
| O2 | §3.2(a): the coded form of "counted as Δ* ≤ SESOI (and ≤ −NI)" | ranks below every defined replicate; a bound on it is null and fails | CC-316 gives the direction; no number was chosen |
| O3 | §3.2(b): an undefined τ on the baseline side of a point Δ | same consequence as for B's τ | CC-316 names B's τ only |
| O4 | §3.2(c): an undefined lever τ | no configuration; nothing passes; trigger fired | literal reading of CC-316; the alternative is to drop that configuration and select among the rest |
| O5 | §4: N_val, unit of n, ε seed | left to the tier-2 prereg | CC-316's first option (N_val = 80,000 labelled "secondary-source planning value", n = images in the primary analysis set, ε from a named seed) stays the candidate |
| O6 | §5: the four Q5 rows | not defined; POST HOC unless defined before step 8 | CC-316 recommends neither route |
| O7 | §1: the distinct-class reading as one descriptive row | not registered; POST HOC if computed | optional in CC-316 Ruling 2 and named in its PI-question default; the coordinator's decision names any-of only |
| O8 | CC-316 V6: which matcher files the scorer re-hashes | the four modules CC-316 names | the `rescap/` files that `vi_objects` loads stay under the R3 LOG pin (l.1246) only; parity run 2 re-hashed them through `map_v1.r3` |
