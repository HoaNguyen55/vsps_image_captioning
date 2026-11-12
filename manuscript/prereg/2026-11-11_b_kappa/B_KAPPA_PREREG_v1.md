# B-KAPPA: registration of the orthographic canonicaliser κ and its rank-swap prediction (Paper B, LRE). DRAFT v1, not approved

Written 2026-11-11T04:04Z by a planning agent. AI-designed. Nothing here has run. No code exists. No score under an alternative written form was computed for this draft, and no prediction file (`*.preds.json`) was opened. "unverified" = not checked today. Thresholds marked [proposal] are for the judge.

Design note: `manuscript/directions/method_2026-11-11/METHOD_DELTA_B.md`.

**What this file registers.**
1. The exact κ, as the adopted R6-III κ plus three listed amendments (§2).
2. Its unit tests, property checks and mutants (§3).
3. A rank-swap prediction on stored KTVIC outputs, pinned by sha before the scores it predicts exist (§4 to §8).
4. Secondary statistics, an English control and third-party descriptive rows (§9 to §11).
5. The code to write (§12), custody (§6, §13) and open questions (§15).

**What it amends.** `manuscript/prereg/2026-11-01_b_pa1_tier1/AMENDMENT_R6_DRAFT_v4.md`, sha256 `0b55d5f8fb9b6edcb9a7c367c3da624ac446e48f41c50eec333234fb1b03f858`, commit `90ed1a6`, Part III (adopted: LOG "R6-III ADOPTED", 2026-11-05T10:16:44Z). That file is not edited. Part III's P3-arm check (§III.4, K-a to K-d, POST_HOC) stays as registered and runs unchanged as §11.3 here.

**What it does not touch.** PA1 (stopped by its registered trigger, CC-330), its labels, map v1, any Paper B text, any other paper.

**Authority.** The method choice is the PI's decision of 2026-11-11 as stated in the task brief. No LOG line for it was found at 03:27Z (unverified). CC-330 Q1 says route (a) needs the PI's explicit line. Nothing in this file runs before that line is in the LOG and the rulings of §15 exist.

---

## 1. Label, data role and rules

- **Evidence label of the main test:** `REGISTERED PREDICTION, DEVELOPMENT DATA (spent KTVIC test references)`. It is never called confirmatory, held-out or a test-set result.
- **Label of everything computed on already-seen files:** `POST HOC / DESCRIPTIVE`.
- KTVIC test is a spent set (CP-071 and later looks). Its references are used here in a development role. PI-1105b allows that for the κ P3 check, "descriptive only". The wider use here needs a ruling (§15 Q2).
- No new labels. No AI label is used as evidence. CPU only. A FAIL is reported. Logs and outputs hold counts and scores only, never caption text.
- One I/O-heavy command at a time on /mnt/d.

---

## 2. κ: exact specification

### 2.1 Base text (unchanged from R6-III §III.1)

κ applies these steps in this order. Each step acts on the previous step's output.

1. NFC over the whole string.
2. Each underscore U+005F becomes one space U+0020.
3. Every maximal run of whitespace becomes one space; leading and trailing whitespace is removed.
4. Case fold.
5. Remove the maximal trailing run of characters from the final-punctuation set and whitespace.
6. Split into letter runs; rewrite each g2-variable run with the canonical tone-mark placement; keep every other run and every delimiter as it is.
7. NFC over the whole string.

M_κ(x, R) := M(κ(x), κ(R)). A metric that needs words segments after κ with one pinned segmenter.

### 2.2 Definitions that make the steps exact (amendment A-3: clarifications, no change of intent)

- **Unicode version.** The one of the pinned interpreter (`unicodedata.unidata_version`; the laptop's Python 3.12.3 reports 15.0.0). It is written into every output.
- **Whitespace (steps 3, 5).** The 25 code points with the Unicode White_Space property: U+0009 to U+000D, U+0020, U+0085, U+00A0, U+1680, U+2000 to U+200A, U+2028, U+2029, U+202F, U+205F, U+3000. The list is hard-coded. The self-test compares it with the interpreter (`str.isspace`) and prints any difference.
- **Case fold (step 4).** Python `str.casefold()`. The P1 claim for g5 covers letters whose case mapping is one-to-one; the Latin letters with Vietnamese diacritics are such letters.
- **Final-punctuation set (step 5).** U+002E `.`, U+0021 `!`, U+003F `?`, U+2026 `…`, U+003B `;`, U+003A `:`, U+002C `,`. Nothing else. A closing quote, a bracket, U+3002 or a zero-width character ends the run.
- **Letter run (step 6).** A maximal run of characters whose general category starts with `L` or `M`. Every other character is a delimiter and is kept.
- **Tone marks.** U+0300 (huyền), U+0301 (sắc), U+0309 (hỏi), U+0303 (ngã), U+0323 (nặng). **Vowel modifiers.** U+0306 (breve), U+0302 (circumflex), U+031B (horn). đ is U+0111.
- **Onsets.** b, c, ch, d, đ, g, gh, gi, h, k, kh, l, m, n, ng, ngh, nh, p, ph, qu, r, s, t, th, tr, v, x, and the empty onset. "qu" is one onset: its u is not part of the vowel cluster. "q" alone is not an onset.

### 2.3 Step 6 exactly (amendment A-2: strict domain)

A letter run r (of the text after steps 1 to 5) is **g2-variable** when NFD(r) is exactly:

- some onset from the list (possibly empty), then
- the two base letters of one pair: (o, a), (o, e) or (u, y), with no vowel modifier on either, then
- the end of the run,

with exactly one tone mark in the run, attached to the first or to the second letter of the pair. For the pair (u, y) the letter before u must not be q.

Step 6 rewrites a g2-variable run so that the tone mark sits on the **canonical** letter of the pair, then recomposes (NFC). Every other run is returned unchanged.

- Examples that are g2-variable: hoà / hòa, toà / tòa, hoá / hóa, khoẻ / khỏe, xoè / xòe, thuỷ / thủy, uỷ / ủy.
- Examples that are not: *hoàn*, *huýt* (a coda follows); *ngoài*, *khuỷu* (three vowels); *quý*, *quả* (qu onset); *thuế*, *thuở* (a modifier); *hoa* (no tone mark); *hoàbình* (not one syllable).

**Why this is an amendment.** R6-III says "each letter run that parses as a Vietnamese syllable is recomposed from φ". On a correctly written syllable that recomposition changes nothing except on these three open clusters. A parser that also accepts a misplaced mark (*thúê*) would rewrite it to *thuế* and so merge two strings that no G move relates (`DR_GAPS_B_2026-11-10.md` G1). The strict domain removes that case. Consequence: a misplaced mark passes through and is counted (§9, residue), not repaired.

### 2.4 Canonical direction (amendment A-1; needs the judge line of PI-1110d)

**Proposed: main-vowel placement.** The tone mark of a g2-variable run goes on the second letter of the pair: hoà, khoẻ, thuỷ.

R6-III step 6 says "new-style placement rule", which in B's labels meant hòa. This amendment reverses the output direction and drops the words "old" and "new". Use "main-vowel placement" (hoà) and "first-vowel placement" (hòa) everywhere.

Evidence for the proposal (all checked 2026-11-11 unless marked):
- **The pinned segmenter itself writes main-vowel forms, whatever the input.** Run today with the pinned jar on toy strings only (no system output, no metric): "hòa bình" and "hoà bình" both come out as `hoà_bình`; "tòa nhà" and "toà nhà" both as `toà nhà`; "sức khỏe" and "sức khoẻ" both as `sức_khoẻ`; "thủy thủ" and "thuỷ thủ" both as `thuỷ_thủ`. It also turns "qúy khách" into `quý_khách`. A first-vowel κ would be undone by the next stage of the pipeline.
- Its word list holds only main-vowel forms. `.session_backup/machines/n2/ncs-data/vncorenlp/models/wordsegmenter/vi-vocab`: hoà 43 / hòa 0, toà 12 / tòa 0, hoá 59 / hóa 0, thuỷ 67 / thủy 0, khoẻ 4 / khỏe 0; 0 first-vowel hits over the 15 patterns (crude UTF-8 decode of the file; counts only).
- `rescap.chair.norm_tone` (the paper's matcher v2) already writes main-vowel forms. One direction in the paper, not two.
- 0 of the 2,790 KTVIC test references change at string level under `norm_tone` (`E4/pilot_results.json :: tone_norm_changes.refs_raw`). With main-vowel κ the references stay as written on this generator.
- 95.3% of "toà nhà" mentions in KTVIC train are main-vowel (`data/results/tone_norm/SUMMARY.md` §1).
- Decision 1989/QĐ-BGDĐT (2018), Art. 8, is reported to prescribe main-vowel placement. Read from a secondary copy only (`DR_GAPS_B` §4): unverified. The paper must not cite it as read until an official copy is opened.

The properties of §2.6 hold for either direction. Under the committed protocol P0 the score after κ does not depend on the direction, because the segmenter rewrites the placement after κ either way. The direction matters for pipelines without that segmenter (syllable tokens, substring matchers) and for the text the released tool emits. It is fixed before any code.

### 2.5 The transform set G

κ quotients exactly these moves, each defined on any string:

| id | Move | Meaning-preserving? |
|---|---|---|
| g1 | Replace the string by a canonically equivalent one (NFC, NFD or mixed) | Yes, by the Unicode definition of canonical equivalence |
| g2 | In a g2-variable run, move the tone mark to the other letter of the pair | Yes by orthographic norm: both placements are in use. Argued, not proved; no human-validity claim |
| g3 | Replace a space by an underscore or back | Yes when the underscore is segmenter markup. Not claimed when "_" is content |
| g4 | Change the length or kind of a whitespace run; add or remove leading or trailing whitespace | Yes |
| g5 | Change letter case | Not in general (proper names). A scoring convention; P0 already lower-cases |
| g6 | Change the maximal trailing run over the final-punctuation set and whitespace | Not in general ("?" carries meaning). A scoring convention, as in the COCO scorer |

Outside G: i/y spelling (kỹ / kĩ); internal punctuation; a misplaced tone mark; *qúy* against *quý*; zero-width characters; diacritic loss; synonyms.

### 2.6 Properties claimed

- **Idempotence.** κ(κ(x)) = κ(x) on the domain D: text whose characters have a case folding that is stable under NFC. D contains every Latin letter with Vietnamese diacritics. It excludes U+0345-type characters (Unicode 15.0 §3.13, D145; `DR_GAPS_B` G1). The check runs on every string κ is applied to in this study; a violation is listed and that character class is named as outside the claim.
- **Not invertible.** g3 to g6 discard information. No inverse is claimed.
- **P1, exact invariance.** For every g in G, every text metric M, every x and R: M_κ(g(x), R) = M_κ(x, R), and the same for g applied to a reference. Proof: κ∘g = κ for each generator (R6-III §III.2 proof lines; the g2 line now reads "g2 changes only the letter that carries the mark inside a g2-variable run, and step 6 writes one of the two"). Assumptions: A3 (the metric reads text only through κ); the segmenter runs after κ and is deterministic; g5 within its one-to-one scope.
- **P2, mark preservation.** κ never removes, adds or changes a tone mark, a vowel modifier or đ, and never moves a mark out of its letter run. So two letter runs that differ in tone, modifier or đ have different κ outputs. With the strict step 6 this holds for every letter run, not only for parsable syllables. Diacritic stripping has P1 and not P2.
- **P4, exactness.** Let ≡ be the smallest equivalence relation that contains every G move. Then κ(x) = κ(y) exactly when x ≡ y.
  - "If": this is P1.
  - "Only if": every step of κ is a composition of G moves, so x ≡ κ(x) = κ(y) ≡ y.
  - The proof is elementary. The registered evidence is the machine check of §3.3 on a generated universe. A counterexample there is a finding against the claim, not a code detail.
  - G is not a group (g3 to g6 are not invertible). The paper credits the invariance-factorisation idea to the statistics literature by analogy only (`DR_GAPS_B` §4 item 3).
- **Not claimed.** Better agreement with humans. Equal scores across segmenters. That the κ score is the same under the other canonical direction in a pipeline whose tokeniser treats the two placements differently. Anything about learned metrics that do not read κ output. Restored diacritics. No "first" claim.

---

## 3. Unit tests, property checks, mutants

### 3.1 Unit tests (must all pass; "=" equal κ outputs, "≠" distinct)

| Pair or case | Expect | Checks |
|---|---|---|
| hoà / hòa; khoẻ / khỏe; thuỷ / thủy; uỷ / ủy; xoè / xòe | = | g2 |
| each of the above, NFC against NFD | = | g1 |
| κ("hòa") is exactly "hoà" (NFC) | exact string | direction (A-1) |
| mắt / mặt; má / mà; đá / dá; hoa / hoà; o / ô / ơ; u / ư; a / ă / â | ≠ | P2 |
| "hoà." / "hòa."; "Hoà_bình" / "hòa bình"; "hoà, bình" / "hòa, bình"; "HOÀ" / "hòa" | = | step order (R6-III composition pairs) |
| "xe  máy" / "xe máy"; " xe máy " / "xe máy"; U+00A0 in place of the space | = | g4 |
| "xe máy!" / "xe máy"; "xe máy ..." / "xe máy"; "xe máy…" / "xe máy" | = | g6 |
| "hòa." / "hòa.”"; "xe, máy" / "xe máy"; "xe máy?" / "xe máy ?!" | ≠, ≠, = | g6 domain |
| "hoàbình" / "hòabình" | ≠ | g2 domain (one unparsable run) |
| thúê / thuế; qúy / quý; qủa / quả; hoàn / hòan; toán / tóan | ≠ | strict domain (A-2) |
| quả, quý, giữa, gì, già, khuỷu, ngoài, thuở, thuế, nguyễn, rượu, được | κ(x) = x | no rewrite outside the three pairs |
| "pizza", "wifi", "café", "José", "naïve", "ß", "İ" | κ(x) = casefold of x, NFC | non-Vietnamese tokens pass through |
| "toà屋", "nhà123", "3D", "xe-máy", "xe/máy", "①" | no placement rewrite in a mixed-script run; digits and symbols kept | mixed scripts, delimiters |
| U+200B, U+200C, U+200D, U+FEFF inside or at the end of the text | kept; text with and without them ≠ | outside G |
| "" and whitespace-only text | "" | empty input |
| κ(κ(x)) = κ(x) on every string above; one U+0345 string is listed as outside D whatever it gives | = | idempotence |

### 3.2 Coverage of Vietnamese syllable forms

Two inventories. No count is stated here; the code prints them.

1. **Generated inventory.** Every combination onset × nucleus × coda × tone from these tables, written with the tone mark on the letter the placement rule gives (and on both letters for the three open pairs).
   - Nuclei: a ă â e ê i o ô ơ u ư y; ai ao au ay âu ây eo êu ia iê iu oa oă oe oi oo ôi ơi ua uâ uê ui uô uơ uy ưa ươ ưi ưu yê; iêu oai oao oay oeo uây uôi uya uyê uyu ươi ươu yêu.
   - Codas: none, c, ch, m, n, ng, nh, p, t.
   - Placement rule (used by the generator and by the residue count, not by κ): (a) a nucleus with ơ carries the mark on ơ; (b) otherwise a nucleus with exactly one of ă â ê ô carries it there; otherwise one with ư carries it on ư; (c) otherwise: one vowel, on it; three vowels, on the middle one; two vowels with a coda, on the second; two vowels without a coda, on the first, except oa, oe, uy (the g2 pairs).
   - The inventory over-generates (not every combination is a word). The properties must hold on the superset.
2. **Observed inventory.** Every distinct letter run that carries a tone mark in: KTVIC train and test references, UIT-ViIC train references, and the segmenter's `vi-vocab` if it decodes as text (else NOT COMPUTED). Reported: the share of such runs that are in the generated inventory (R6-III A1; bar 99% of reference tokens), and the list of the rest by type and count. With the strict step 6, P1 and P2 do not depend on this share; it says how much real text the machine check of P4 covers.

### 3.3 Property checks (run by `kappa.py --enum`; any failure blocks the code read)

- **E1 idempotence:** κ(κ(s)) = κ(s) for every s in both inventories and in every context below.
- **E2 soundness (P1):** for every generated syllable s, every context c and every applicable G move g: κ(g(c(s))) = κ(c(s)). Contexts: alone; "s."; "s_s′"; "s s′" with one, two and U+00A0 spaces; title case; upper case; NFD; "s, s′"; "s!?"; leading and trailing whitespace. Pairs of adjacent moves (g∘h) are included.
- **E3 separation (P2, P4):** let canon(s) be the generated item written lower-case, NFC, with the main-vowel placement. For any two generated strings s, t: κ(s) = κ(t) exactly when canon(s) = canon(t). (The comparison is on spellings, because "g" + "ia" and "gi" + "a" generate the same string.)
- **E4 no rewrite outside the domain:** for every generated syllable that is not g2-variable, step 6 returns it unchanged.
- **E5 differential oracle:** on every generated g2-variable run, step 6 equals `rescap.chair.norm_tone` (`rescap/chair.py`, sha `e47d249a`). Disagreements outside that set (*qúy*-type, which `norm_tone` rewrites and κ does not) are listed, not hidden. If Q1 is ruled the other way, the oracle is the inverse of the `norm_tone` table.
- **E6 already-normalised text:** for every reference string of KTVIC train and test and UIT-ViIC train, κ(κ(r)) = κ(r); the share with κ(r) = r is reported per step.
- **E7 what the segmenter already absorbs (reported, not a gate):** for every generated g2-variable run, the pinned segmenter's output for the first-vowel and the main-vowel spelling; and the same for the *qúy*-type residue. Expected from the toy check: equal in every case.

**Reading.** E1 to E4 with zero counterexamples and every mutant killed: the exactness claim P4 may be written, scoped to the generated universe plus the proof. Any counterexample that cannot be fixed without widening G: P4 is dropped from the paper, κ stays as a tested normaliser, and the change needs a judge line.

### 3.4 Mutants (each must be killed by §3.1 or §3.3)

m1 strips tone marks. m2 skips step 1. m3 writes the first-vowel placement. m4 drops unparsable runs. m5 splits on whitespace and parses whole tokens before steps 2 to 5 (R6-III m5). m6 accepts a misplaced mark and repairs it (*thúê* to *thuế*). m7 treats "qu" as a vowel cluster (*quý* to *qúy* or the reverse). m8 runs step 6 before case fold only for lower-case input (upper-case *HÒA* not rewritten). m9 strips internal punctuation at step 5. m10 omits step 7. m11 applies step 6 when a coda follows (*hoàn* to *hòan*). m12 uses `str.split()` whitespace in place of the fixed list.

---

## 4. The rank-swap test: data

### 4.1 The stored outputs

- 73 files `data/results/<name>.preds.json` for the 558 KTVIC test images. They were not opened for this draft, so the schema is taken from the loader: `scripts/kit_b/ptb_protocol.py::load_preds` reads `{image_id: value}` and takes the value itself when it is a string and its first element when it is a list, then strips it. That loader is used for all three prompt modes. Whether `-detailed` and `-two` files hold lists is unverified; stage C reports the value type per file (type only).
- The list of names: keys of `data/results/tone_norm/ktvic_side_by_side.json :: systems` (sha256 `d8b48b41…`; 73 keys). `data/results/tone_norm/SUMMARY.json` (sha `dd511d3a…`) `meta.ktvic_total_systems` = 73.
- All 73 are tracked in git and unmodified at `da37725` (`git ls-files -s`, `git status`; checked 2026-11-11). **Pin:** stage C writes `SYSTEMS.tsv` (name, mode, family, role, sha256 of the file, git blob id) and the coordinator logs its sha. No sha256 of a prediction file is stated here.
- **They are our own systems.** All 73 are variants of one backbone family (zero-shot, fine-tuned recipes, seeds, decode variants) under three prompt modes. They are not 73 independent published systems.
- Prompt modes by name suffix: 33 `-short`, 35 `-detailed`, 5 `-two`.
- References: `data/datasets/ktvic/test_data.json` (sha `cc22ec6a…`), field `caption` (558 images, 2,790 references).

### 4.2 What has already been looked at (custody census, first pass)

| Earlier look | Files | What was computed under another written form |
|---|---|---|
| E4 pilot, 2026-10-14 (`.session_backup/2026-10-14/research_r10/E4/pilot_results.json`, sha `17c67171…`; code `scripts/kit_b/protocol_pilot.py` l.41–43, l.245–257) | 24 `-short` files + the two published KTVIC baselines | CIDEr-D, BLEU-4, ROUGE-L under strip-punctuation (P7), tone normalisation on outputs and references (P6, P6b), case-sensitive (P5), syllable and pyvi tokenisation; rank statistics against P0, including flip counts |
| Period audit and PTB protocol (`c8_l5_d1_d3a_cpu_audit.json`, `data/results/b_ptb/ptb_protocol.json`) | p1assist_s42-short, fuse2_s42-short, zeroshot-short (and p1ep4_s42-short, not among the 73) | CIDEr-D with a period appended, stripped, and with PTB-style removal |
| tone_norm audit, 2026-10-14 (`data/results/tone_norm/`) | all 73 | per-file counts of captions changed by placement normalisation; object P/R/F1 under it. No n-gram score |
| B-N1 (`data/results/b_n1/b_n1_run.json`) | four public zero-shot models, not among the 73 | CIDEr-D with and without the punctuation fix; LBB-P1 FAIL, τ_b = 1.0 |
| B-2 external (`.session_backup/2026-10-28/b2_external/`, path from the paper's source comment; unverified) | K1, K5, K6, not among the 73 | every protocol column of the kit |

- **Seen set S (24 files):** the `-short` files of p1assist_s42, p1assist_s43, p1assist_s44, p1-gold, p1_s43, p1_s44, p1mask_s42, mr5assist_s42, fuse2_s42, fuse2_s43, fuse2_s44, tags_fuse2_s42, tags_p1_s43, e5_s42, e5dpo_s42, p1_s43mbr, fuse2_s42mbr, zeroshot, tags_zeroshot, vcd, main_s42, vsps, official, p2-noverif4090.
- **Candidate unseen set U (49 files):** the other 9 `-short` files (main_s43, main_s44, off4090sft, official4090, offsft-diag, roundA, roundB, seed43, seed44), all 35 `-detailed` files and all 5 `-two` files.
- **The census is not complete.** 47 scripts under `scripts/` read prediction files and contain a form-related keyword (a broad search, so an upper bound). For this draft `protocol_pilot.py` was read, `ptb_protocol.py` and `punctuation_audit.py` were checked by their function lists and result files, and the docstrings of `h2_precheck/flipbudget.py` and `vi_diagnostics.py` were read (neither rescores under another form). The other 42 are unverified. Stage C finishes the census (§6). Any U file found with an earlier n-gram score under another written form moves to S.
- **Raw scores are known.** Every file was scored under the committed protocol P0. That is intended: raw scores are inputs to the rule. 6 of the 73 have no committed score file `data/results/<name>.json` (main_s44-detailed, main_s44-short, vcd-detailed, vsps_base-detailed, vsps_clean-detailed, vsps_neutral-detailed); §5.1 says which scorer produces all raw scores.

### 4.3 Families, strata and roles

- **Stratum** = prompt mode. Ranks are compared only inside one stratum.
- **Family** = one training recipe; seeds and decode variants of a recipe are one family. Default rule from the file name: drop the mode suffix; drop a trailing `mbr` or `selffuse`; drop `_s42`, `_s43`, `_s44`; map `p1-gold` to `p1` and `seed43`, `seed44` to `seed`. This gives 26 families (e5, e5dpo, fuse2, main, mr5assist, off4090sft, official, official4090, offsft-diag, p1, p1assist, p1mask, p2-noverif4090, roundA, roundB, seed, tags_fuse2, tags_p1, tags_zeroshot, v3, vcd, vsps, vsps_base, vsps_clean, vsps_neutral, zeroshot). Every family has at least one U file. The code read checks the rule against the run records; where a record says two keys are one recipe, they are merged. No split is allowed.
- **Split of U (split-half by family).** Sort the family keys by code point. seed = the first 8 hex digits of the sha256 of `SYSTEMS.tsv` before the role column is filled, read as an integer. `random.Random(seed).shuffle(keys)`. The first ⌈n/2⌉ keys are the **prediction families**; the rest are calibration families. A U file takes the role of its family: `U-pred` or `U-cal`.
- **Calibration set** Cal = S ∪ U-cal. **Prediction set** Pred = U-pred.
- **Primary pair set 𝒫:** all unordered pairs of Pred files in the same stratum and in different families.
- **Disclosed weakness.** The same checkpoint can sit on both sides in different prompt modes (its `-short` file in S, its `-detailed` file in Pred). The rule uses only pooled per-class parameters from Cal, and same-family pairs are excluded from 𝒫.

---

## 5. Scores and written forms

### 5.1 Scorer (reused, not rewritten)

- Tokens of a text t under P0: `lower(rdr(t)).split()`, with `rdr` from `scripts/kit_b/protocol_pilot.py` (sha256 `6aee4282…`): VnCoreNLP 1.2 RDRSegmenter, jar sha256 `9e2811cd…` (equal to the protocol card; the jar is at `.session_backup/machines/n2/ncs-data/vncorenlp/`, checked 2026-11-11).
- CIDEr-D: `Cider(refs).per_image(hyps)` of the same file (n = 4, σ = 6, document frequencies from the scored references only, ×100). ROUGE-L and BLEU-4: `rouge_l`, `bleu4` of the same file.
- **Gate G-repro.** For the 67 files with a committed score file, the raw CIDEr-D mean from this scorer must equal `results[0].scores_scaled_x100.CIDEr` within 0.01. All 67 record `segmenter` = `rdrsegmenter`, word-level, 558 images, and no fallback warning (metadata read 2026-11-11).
  - The kit scorer's reproduction is so far asserted on one `-short` file (`protocol_pilot.py --check`) and was repeated for the 26 systems of the E4 pilot. It is untested on `-detailed` and `-two` files, where the committed scorer (`rescap/metrics.py`, py_vncorenlp) and the kit's command-line segmenter may split multi-sentence text differently.
  - **Rule fixed now.** A mismatch on any of the 24 S files is a FAULT: nothing proceeds. A mismatch on a U file excludes that file (role `excluded`, listed with the size of the mismatch) and the chain continues. More than 5 excluded U files [proposal] is a FAULT. Exclusions happen in stages 2a and 2b, before the pin; 𝒫 is formed from the files that remain.
  - The 6 files without a committed score file cannot be checked this way. They stay in, flagged `no_committed_score`, and the result is also reported without them (SECONDARY).

### 5.2 The two written forms

- **Form A (as written).** a_{i,c} = per-image CIDEr-D of file i on image c, outputs and references as stored, P0 tokens. A_i = mean over the 558 images.
- **Form K (canonical).** k_{i,c} = the same with κ applied to every output and every reference before `rdr`. K_i = mean.
- This is the **end-to-end arm**: M(x, R) against M(κx, κR). It is the comparison two groups with different form policies would differ by.
- Shift δ_i = A_i − K_i. A **swap** of files i and j: (A_i − A_j) and (K_i − K_j) have opposite signs and both exceed 1e-9 in absolute value. Pairs with a gap ≤ 1e-9 in either form are ties: excluded and counted.
- Primary metric: CIDEr-D. ROUGE-L: secondary, same rule. BLEU-4 (pooled counts): observed swaps only, no prediction.

### 5.3 Which generators can move a P0 score

P0 already collapses whitespace and lower-cases after segmenting. So:
- g6 (final punctuation): yes. This is the measured 35.17-point hazard.
- g2 (placement): **no, under P0.** The pinned segmenter rewrites the placement itself (§2.4, toy-string check of 2026-11-11), so both placements reach the metric as the same tokens. g2 moves a score only where that step is absent: syllable (whitespace) tokens, the object matcher (30 of 73 files, sec3 §3.5), and other segmenters (unverified). The segmenter even repairs *qúy*, which is outside G.
- g3 (underscore): only for outputs that carry underscores (expected: the published baselines; unverified for the 73).
- g1 (composition): only if some text is not NFC. Counted.
- g5 (case): only if case-folding before segmentation changes the segmentation. Counted.
- g4 (whitespace): expected none. Counted.

**Consequence, stated plainly.** Under the paper's committed scorer the main test is about final punctuation. The Vietnamese-specific generator g2 is inert there. It is measurable only in the syllable column of §5.5.

### 5.4 Caption classes (counted without any score)

For a caption x let T0(x) be its P0 token sequence. Let κ₋₅ be κ without step 5 and κ₋₆ be κ without step 6.

- **N** (untouched): T0(κ(x)) = T0(x).
- **P** (final punctuation only): not N, and T0(κ₋₅(x)) = T0(x). Without step 5, κ changes nothing.
- **T** (placement only): not N, not P, and T0(κ₋₆(x)) = T0(x). Under P0 this class is expected to be empty (§5.3); a non-empty class T under P0 is listed and explained. It is used in the syllable column.
- **O** (other): every other touched caption.
- An image is **ref-touched** when T0(κ(r)) ≠ T0(r) for at least one of its references.
- Class of (file i, image c): P, T or O by the output; **R** when the output is N and the image is ref-touched; N otherwise.
- Length bin of (i, c): `short` when len(T0(x)) ≤ L*, else `long`. L* is fixed in stage 2a (§7).

### 5.5 Syllable column (SECONDARY; no verdict)

- Tokens: `t.strip().lower().split()` (the E4 protocol "P1_syllable_raw", the form `evaluate.py --also-syllable` scores). No segmenter runs, so g2, g3 and g6 can all move a score.
- Everything of §5.2, §5.4, §7 and §8 is repeated with these tokens: its own classes, its own calibration, its own predicted set, written into the same `PREDICTION.json` before the pin, and the same counts, precision, recall and intervals after the look.
- It carries no PASS or FAIL label of its own. It is reported beside the primary result as the place where tone-mark placement is measurable.
- Reproduction: 22 of the committed score files also hold a raw syllable-token score (`results[1]`, segmenter `whitespace`); the gate of §5.1 is applied to them in this column.
- The S files were already scored under syllable protocols in the E4 pilot, as in the primary column.

---

## 6. Stages, order, custody

Each stage is one subcommand of `scripts/b_kappa/b_kappa.py`. Each refuses to start unless the sha256 of its inputs and the LOG pin line of the previous stage are present (the `pin_line` pattern of `scripts/b_pa1/b_pa1.py` l.330). Each logs its start and its output sha with a `date -u` stamp.

| Stage | Opens | Computes | Writes | Who may look |
|---|---|---|---|---|
| C census | file names, git index, earlier result files' key names; no prediction text | sha256 per prediction file; the earlier-look table of §4.2 completed; S, U; families; the split | `SYSTEMS.tsv`, `CENSUS.md` | coordinator, judge |
| 0 κ and references | references only (KTVIC train and test, UIT-ViIC train) | §3.2 observed inventory, §3.3 E6, reference class counts per step | `stage0.json` | coordinator, judge |
| 1 counts | all 73 prediction files | classes of §5.4 in both columns (§5.5), token lengths, residue counts. **No metric is imported in this stage** | `kappa_pi.json` (counts only) | coordinator, judge |
| 2a calibration | Cal files only | a, k per image; L*; class ratios; G-repro for Cal | `calib.json` | coordinator, judge |
| 2b prediction | Pred files, **form A only** | a per image; G-repro for Pred; the predicted sets of §7 | `PREDICTION.json` | coordinator, judge |
| pin | — | — | LOG line with the sha256 of `PREDICTION.json`; a read-only (444) copy under `.session_backup/2026-11-11/b_kappa/pins/` | coordinator |
| 3 look | Pred files | k per image; observed swaps; §8 verdict; §9 statistics | `RESULT.json` | after the pin only |

**Before the pin the coordinator may look at:** everything in stages C, 0, 1, 2a and 2b, including the touched counts and raw scores of Pred files and the κ scores of Cal files.

**Before the pin nobody may:** compute or view any score of a Pred file under form K or under any single κ step; run any earlier script (`protocol_pilot.py`, `ptb_protocol.py`, `punctuation_audit.py`, `evaluate.py --also-syllable`) on a Pred file; change the rule, the split, 𝒫 or a threshold. Stage 3 checks that no file named `RESULT*.json` exists and that the LOG pin line precedes its own start line.

**After stage 3:** one judge reads the result (reversible, 85). Any further analysis on Pred files is POST HOC.

**A FAULT** (G-repro mismatch, a failed identity, a gate that does not hold) stops the chain. A re-run after a code fix needs a judge line and is disclosed.

---

## 7. The prediction rule (fixed now, before any score under form K exists for a U file)

**Calibration (stage 2a), on Cal captions only.**
- L* = the median of len(T0(x)) over all Cal captions whose class is not N.
- For each class q ∈ {P, T, O, R} and bin b: ρ_{q,b} = Σ(a − k) / Σ a over the Cal captions of that cell.
- A cell with fewer than 30 captions or Σ a = 0 uses the ratio of class q with both bins pooled. If that still has fewer than 30 captions, it uses the ratio pooled over all non-N Cal captions. If that has fewer than 30, ρ = 0 and `calibration_thin` = true.
- ρ_N := 0 by rule.

**Rule R1 (primary).** For a Pred file j:
- δ̂_j = (1/558) Σ_c ρ_{q(j,c), b(j,c)} · a_{j,c};
- K̂_j = A_j − δ̂_j.
- A pair (i, j) in 𝒫 is **predicted to swap** when (A_i − A_j) and (K̂_i − K̂_j) have opposite signs and both exceed 1e-9. The set is F_pred.

**Why a relative ratio, not the plan's pooled additive shift.** Paper B's own numbers show the shift per touched caption is far from constant: one period costs 35.17 points at a score of 148.66 and 4.32 points at 33.30 (sec3 §3.3). The assumption A-μ of R6-III is therefore known to fail across score levels, and the rule of `DEPTH_PLAN_2026-11-07.md` §3.2 (δ̂_i = π_i·μ̄) is kept only as a baseline.

**Baselines written into the same pinned file (no verdict of their own).**
- **B0, π-blind.** The |F_pred| pairs of 𝒫 with the smallest |A_i − A_j| (ties broken by the pair's names in code-point order).
- **R0, the plan's rule.** δ̂_j = π_j·μ̄, with π_j the non-N share of file j and μ̄ the mean of (a − k) over non-N Cal captions.

`PREDICTION.json` holds: the sha256 of the κ code, of `SYSTEMS.tsv`, `kappa_pi.json` and `calib.json`; L*; every ρ with its cell size; A_j, δ̂_j, K̂_j per Pred file; 𝒫; F_pred; the B0 and R0 sets; the ROUGE-L version of all of these; the bootstrap seed.

---

## 8. Pass rule (fixed now)

Observed swap set F_obs: the pairs of 𝒫 that swap between form A and form K (§5.2), on all 558 images.

- precision = |F_pred ∩ F_obs| / |F_pred|; recall = |F_pred ∩ F_obs| / |F_obs|; F1 as usual. An empty denominator makes that quantity 0.
- **NOT_EVALUABLE** when |F_pred ∪ F_obs| < 5 [proposal, from `DR_GAPS_B` G3]. Reported as: "few or no swaps were predicted and few or none were observed", with both counts. It is never written as a PASS.
- **PASS** when |F_pred ∪ F_obs| ≥ 5, precision ≥ 0.80, recall ≥ 0.80 [proposal, `DEPTH_PLAN` §3.2], and F1(F_pred) > F1(B0).
- **FAIL** otherwise.
- **Interval (reported, not part of the rule).** Paired bootstrap over images: B = 2,000 draws, seed 20261111; each draw resamples the 558 image indices once for all files, recomputes A, K and F_obs from the per-image scores (document frequencies fixed at the full-set values), and scores the fixed F_pred. Percentile 95% intervals for precision, recall and F1. Draws with an empty F_obs are counted and dropped from the recall interval.
- Reported beside the verdict: the confusion counts; the per-stratum split; the number of ties; the same for B0 and R0; `calibration_thin`.

**If it fails.** The FAIL goes into the paper at the place and length a PASS would have had, with the counts and intervals. The claim "κ predicts which pairs swap" is withdrawn. κ, P1, P2, P4 and the measured shifts stay. No second rule is tried on the Pred files under a registered label; anything further is POST HOC.

**If it is NOT_EVALUABLE.** The paper says that κ changes scores and not rankings among these files, and reports the shifts. This agrees with the earlier registered FAIL of B-N1 (LBB-P1, τ_b = 1.0), which is cited beside it.

---

## 9. Secondary statistics (labelled SECONDARY; no verdict)

- Share of captions affected, per file and per class (N, P, T, O, R), and per κ step, from stage 1.
- Reference side: the share of KTVIC test references changed, per κ step.
- Size of the score shift per file: δ_i for CIDEr-D, ROUGE-L and BLEU-4, with image-bootstrap intervals; for Pred files also δ̂_i, the mean absolute error of δ̂ and the sign agreement.
- τ_b between the form-A and form-K rankings, per stratum; and τ_b(K̂, K) beside τ_b(A, K).
- The mean shift of N-class captions on images that are not ref-touched (expected 0; a non-zero value shows that reference changes moved the document frequencies).
- Material swaps: observed swaps with both gaps ≥ 1.0 CIDEr-D point [proposal].
- Residue outside G, counts per file: runs with a misplaced tone mark (by the placement rule of §3.2), *qúy*-type runs, zero-width characters, internal punctuation tokens, non-NFC text.
- Every statistic above in the syllable column of §5.5.
- The same statistics on S files, labelled POST HOC / DESCRIPTIVE.

---

## 10. English control (label CONTROL; no verdict)

Purpose: show what part of the method is Vietnamese-specific and what part is a pipeline property.

- **Data (references only, train splits, full).** COCO: `data/datasets/karpathy/dataset_coco.json`, images whose split is `train` or `restval`. Flickr30K: `data/datasets/flickr30k_entities/annotations.zip` (31,783 files under `Sentences/`; the entity markup `[/EN#…/… phrase]` is removed by a fixed regular expression); "train" here = every image id not in the val and test lists of `manuscript/prereg/2026-10-30_c_t1/c_t1_f30k_lists.json`. This is the complement of Paper C's lists, not a file of an official train split; whether it equals the usual Flickr30K train split is unverified, and the paper calls it "the complement of the val and test lists". That list is Paper C's; reading it needs the coordinator's owner line (§15 Q8). No val or test caption is read.
- **Candidate.** For each image, the first listed reference is the candidate and the others are its references (fixed rule; no model output).
- **Registered expectations.**
  - EN-1: step 6 alters zero letter runs in both reference sets, so κ equals κ_EN (steps 1 to 5 and 7). Any altered run is listed.
  - EN-2: under the standard English pipeline (pycocoevalcap PTB tokeniser, which lower-cases and removes punctuation), κ changes the token sequence of at most 0.5% of captions [proposal] and the mean CIDEr-D by less than 0.1 point [proposal]. A larger value is reported as such.
  - EN-3: under a P0-like pipeline (whitespace tokens, lower-case, punctuation kept), the shift is not zero. Reported: the share of references that end with a final-punctuation character, the shift, and the shift from appending one period to every candidate (the English mirror of the 35.17 result).
- pycocoevalcap is not importable in the system Python (checked today); the scoring environment is named at the code read. If it cannot be set up by 11-15, EN-2 is NOT RUN and EN-1 and EN-3 stand alone.
- This step is CPU-heavy for the laptop (the full COCO train references). It may run on a rented CPU host under the existing rule; the references are public.

---

## 11. Descriptive rows beside the test (each labelled POST HOC / DESCRIPTIVE)

1. **Published KTVIC baselines.** ResNet101+LSTM and ViT+Transformer outputs (`.session_backup/2026-10-22/b2/thesis_code_1a8d105/simple_evaluate/`; public at `github.com/pacman-ctm/thesis-code`, HTTP 200 and both files listed on 2026-11-11; no licence; aggregate statistics only, by permission of 2026-10-21). Form A, form K, shift, class shares. They were in the E4 pilot, so nothing here is a first look. Their outputs carry underscores and no punctuation (sec3 §3.3), so g3 is the only generator expected to act.
2. **K1 (Swin-BART, KTVIC test)**, `.session_backup/machines/M3/root/outputs/b2_external/preds/K1.preds.json`. Only with the ruling of §15 Q6: the B-2 registration says the run "ranks no system and compares no row with ours". K5 (UIT-ViIC test) and K6 (UIT-OpenViIC test) are not used without one judge line each; OpenViIC also needs Paper C's owner line.
3. **The R6-III P3 arm**, exactly as registered (§III.4: stage order, K-a to K-d), on all 73 files, with the direction of A-1. Label as registered there: `POST_HOC / DESCRIPTIVE (B κ P3 check)`.
4. **No ranking of published systems** is printed in the paper without a separate ruling. The committed paper says "We rank no Vietnamese system" (sec5 §5.1).

---

## 12. Code to write (new folder `scripts/b_kappa/`; nothing else is edited)

| File | Content | Self-test | Mutants |
|---|---|---|---|
| `kappa.py` | `kappa(text)`, `steps(text)` (the output after each step), `is_g2_variable(run)`, the tables of §2.2 and §3.2, the generator and checks E1 to E6 (`--enum`) | `--selftest`: §3.1 table, exit 0 only if all pass; prints the Unicode version and the whitespace comparison | m1 to m12 (§3.4) |
| `b_kappa.py` | stages C, 0, 1, 2a, 2b, 3, each for the primary and the syllable column; `english`; `thirdparty`; `p3arm`; gates and pin checks | `--selftest` on synthetic fixtures built in memory: three toy corpora with known classes, known swaps and a known verdict (one PASS, one FAIL, one NOT_EVALUABLE); the identity δ = Σ_class π·μ to 1e-9; G-repro on a toy; refusal to run stage 3 without a pin line | r1 to r10 below |
| `mutants.py` | applies each mutant to a copy in a temporary folder, runs the matching self-test, and requires a non-zero exit for every mutant | prints "killed n of n"; exit 0 only if all are killed | — |
| `SHA256SUMS` | the three files | — | — |

Runner mutants: r1 the prediction reads form-K scores of a Pred file (leak); r2 the swap test compares signs of A and K̂ wrongly (same sign counts as a swap); r3 ties are not excluded; r4 the bootstrap resamples files, not images; r5 a U-pred file enters the calibration; r6 precision and recall are exchanged; r7 the evaluable threshold is 4 or 6; r8 B0 is ranked by form-K gaps; r9 the class test uses raw strings in place of P0 tokens; r10 stage 1 imports a metric.

**Reused as they are:** `scripts/kit_b/protocol_pilot.py` (`rdr`, `Cider`, `bleu4`, `rouge_l`; sha `6aee4282…`); `scripts/kit_b/ptb_protocol.py` (`load_refs`, `load_preds`, `sha`; sha `ea5fbe6e…`); `rescap/chair.py::norm_tone` as the oracle of E5; the pin-line gate pattern of `scripts/b_pa1/b_pa1.py`. No existing file is changed.

**Code read (P8 form):** self-tests and mutants re-run by the judge; SUMS LOG line; one-judge FULL read, reversible, 85. The κ file is read first and can receive its GO alone (R6-III: "nothing runs before the κ-code read").

---

## 13. Dates (results are needed by 2026-11-16)

| Date | Step | Gate |
|---|---|---|
| 11-11 | PI line in the LOG; judge read of this file (§15) | no ruling, nothing runs |
| 11-12 | `kappa.py`, mutants, `--enum`; κ code read. Stage C | counterexample that needs a wider G: P4 dropped. Fewer than 20 U files left after the census [proposal]: the test is relabelled POST HOC |
| 11-13 | runner code read; stages 0, 1, 2a, 2b | fewer than 99% of toned reference runs in the generated inventory: the paper says the machine check of P4 does not cover the references' forms. \|F_pred\| < 5: the PI is told NOT_EVALUABLE is likely; the look still runs |
| 11-14 | pin; stage 3; result read | PASS, FAIL or NOT_EVALUABLE, reported as it falls |
| 11-15 | English control; descriptive rows; R6-III P3 arm | rows not finished are NOT RUN |
| 11-16, 12:00 VN | freeze | — |

---

## 14. Paper-text clauses (binding on any writer)

- The main test is called a pre-registered prediction on development data. It is never called confirmatory, held-out or a test-set evaluation.
- The 73 files are described as variants of the authors' own systems.
- P1 and P4 are stated as elementary; P1 is "by construction". The LREC 2026 diacriticity paper, sacreBLEU, semCER, MultiLexNorm++ and the rank-flip precedents of `DR_GAPS_B` §4 are cited. No "first" claim.
- The earlier B-N1 FAIL is cited beside any swap result.
- The paper says that under its committed scorer the registered test concerns final punctuation, that the segmenter already absorbs tone-mark placement, and that placement effects are shown in the syllable column and the object matcher only.
- The direction is named "main-vowel" or "first-vowel". Decision 1989/QĐ-BGDĐT is not cited as read until an official copy is opened.

---

## 15. Open questions for the judge (each with a recommended answer)

| # | Question | Recommended answer | Default if no ruling |
|---|---|---|---|
| Q1 | Which canonical direction does κ write: main-vowel (hoà) or first-vowel (hòa, R6-III as adopted)? | **Main-vowel.** The pinned segmenter itself emits that form for either input (toy-string check today), so a first-vowel κ would be undone by the pipeline; `norm_tone` and the KTVIC references already use it (0 of 2,790 test references change). Under P0 the choice moves no score. This amends R6-III (A-1) | No κ code is written |
| Q2 | May the KTVIC test references be used in a development role for this wider test (end-to-end arm, all generators, a pinned prediction with a verdict), beyond the letter of PI-1105b ("κ P3 check, descriptive only")? | **Yes**, once the PI's 2026-11-11 decision is a LOG line. The set is spent, no unused set is touched, and the label of §1 keeps the claim at development level. The PI-1105b clause "never a confirmatory claim" stays | Only the R6-III P3 arm runs, POST HOC |
| Q3 | The 73 outputs were all scored under the current form, and 24 of them (plus 4 in the period audit) were already rescored under other forms, with flip counts. What does that mean for the test? | Raw scores are legitimate inputs. The 24 are calibration only. The registered test is on U-pred files, and only if stage C finds no earlier look at them. The paper states the census. Without a clean census the label falls to POST HOC | As recommended |
| Q4 | Is the label "registered prediction, development data" acceptable where PI-1105b said "descriptive"? | **Yes**, for U-pred only | "DESCRIPTIVE" for everything |
| Q5 | Primary rule: R1 (class and length ratios × raw caption score) or the plan's R0 (π·μ̄)? | **R1.** B's own numbers show μ is not constant (35.17 against 4.32 points for the same period). R0 stays as a baseline | R1 |
| Q6 | May K1 be rescored under κ as a descriptive row, given the B-2 registration's "ranks no system"? May K5 and K6? | K1: **yes**, as an unranked row. K5, K6: **no** for now (other test sets; one look each; OpenViIC is Paper C's) | None is rescored |
| Q7 | Is the strict step 6 (A-2: only the three open pairs; a misplaced mark passes through; *qúy* is not merged with *quý*) the right reading of R6-III? | **Yes.** It is what makes P4 true. The residue is counted. If any file has a residue above 1% of captions [proposal], a later amendment may widen G | Strict |
| Q8 | May the Flickr30K train references be defined as the complement of Paper C's val and test name list? | **Yes** (names only; no val or test caption is read) | COCO only |
| Q9 | Are the family rule from file names and the family-level split acceptable, given that one checkpoint can appear on both sides in different prompt modes? | **Yes**, with same-family pairs excluded and the weakness stated. The code read checks the rule against run records | As recommended |
| Q10 | Are the thresholds acceptable: precision and recall ≥ 0.80; evaluable at 5; the F1 > B0 condition; 30 captions per cell; 20 U files; B = 2,000? | **Yes** | As written |
| Q12 | Under P0 the Vietnamese-specific generator g2 is inert, because the segmenter absorbs it. Should the syllable column (§5.5), where g2 acts, carry a registered verdict too, or become the primary column? | **Keep P0 primary and the syllable column SECONDARY.** P0 is the paper's committed protocol card; one verdict avoids a choice after the fact. The paper must then say that the registered test is about final punctuation and that placement is shown descriptively | As recommended |
| Q13 | Is the G-repro rule acceptable (S mismatch = FAULT; U mismatch = that file excluded; more than 5 = FAULT; 6 files without a committed score kept and flagged)? | **Yes** | As written |
| Q11 | Tier of this registration? | Reversible, one judge, FULL read, 85: CPU only, spent set, no money, no new label. The route question (LRE with κ as the method) is the PI's (CC-330 Q1) | — |

---

## 16. Disclosure: what the drafter opened

- Read in full or in part: the plan, review and rubric files named in the task; R6-III; CC-330; the committed Paper B sections at `aed7647`.
- Aggregates and key names only: `data/results/tone_norm/SUMMARY.md` l.1–22 (it states per-file counts of captions changed by placement, for example 67, 58 and 50 for three zero-shot-type `-detailed` files and 0 for the KTVIC-fine-tuned files, and one object-F1 change); key names of `SUMMARY.json`, `ktvic_side_by_side.json`, `cjk_rate.json`, the E4 pilot file, the period audit and `ptb_protocol.json`; one reference-side count (`tone_norm_changes.refs_raw` = 0).
- **By accident:** the first 900 bytes of `.session_backup/2026-10-22/b2/pilot_repro.log`, which show CIDEr-D under several E4 protocols for four S files (p1assist_s42, s43, s44, p1-gold). For those four the tone-normalised and case-sensitive rows equal P0. These are seen files; no U file's score under another form was seen.
- `data/results/zeroshot-short.json` (a score file of an S system) was loaded to read key names; it also holds a `predictions` key, which was not printed.
- No `*.preds.json` was opened. Their existence and git state were checked.
- The pinned segmenter was run once on twelve toy strings typed for the purpose (six placement pairs); no reference, no system output, no metric.
- Scorer metadata (`prompt_style`, `split`, `n_images`, `results[*].tokenization`, `segmenter`, `warnings`) of the 67 committed score files; no score value and no prediction was printed.
- Network: two HTTP status checks and one GitHub directory listing of the public baseline repository, with a generic client name.
- The placement counts for the 73 files (tone_norm audit) were known to the project before this draft. The split rule does not use them.
