# Amendment to B-PA1-T1 prereg v3.1 §6.1 and §6.4 step 4: agent-drafted step-4 map additions (D-8), with the pre-drafted (ii) entries, v1.3

Status: **DRAFT v1.3 for its irreversible-tier read, round 3/3 (the last); not pinned, not committed, licenses
nothing.** Written 2026-11-08 from 12:50Z to 13:20Z (`date -u`) at HEAD `d7d84a6`. Label: `TIER 1 / DEV-EXPLORE
(B-PA1-T1)`.

- **Supersedes v1.2** (`D8_AMENDMENT_DRAFT_v1_2.md` 4f8f47dc), v1.1 (171da1d7) and v1 (89f22d66). All are kept
  unchanged and never pinned; nothing is struck in place (CC-296 Ruling 11).
- It answers **CC-296r2** (`CC-296r2.txt` 982e2ef6, NEXT_ROUND round 2/3):
  - W4: the 19 strikes in 14 classes (§5);
  - W5: this file;
  - N6-N9.
  W3 is carried as pin condition P1, the gatekeeper's step (§7). CC-296 (cc61d584) and its LOG erratum stay closed as
  ruled.
- Amends `PREREG_DRAFT_v3_1.md` (`e9b30ca7…`, commit 5ff00c9) §6.1 and §6.4 step 4. v3.1 is not edited.
- **Agent-drafted.** The drafter is `claude-opus-5-5`, and this file and the entries file it governs are its proposals.
  Neither is gold or evidence; a judge reads them.
- **When it takes effect.** Only when its sha is on pin line (A) of §7. Lines (A) and (B) are written in that order
  **after** the round-3 GO **and after the CC-295r3 commit `H_B`**, and before the rental.
  - This is the CC-296 Ruling 9 order; it overrides the "before `H_B`" of v1.1.
  - Basis: CC-295r2 "Before a B rental (in order)", CC-295r2 W8 and CC-296r2 P1.
- Basis of the amendment:
  - PI-1108e Q2 (a) (LOG l.1852): "step-4 map additions are agent-drafted proposals (never gold) under a new logged
    amendment, judge-read at the irreversible tier before the rental";
  - CC-295 Ruling 6 (reading 18), W5 and its D-8 line; CC-295r2 W7 and W8;
  - CC-296 Rulings 1-12; CC-296r2 Rulings 1-9;
  - B_RUN_DOC v1 §11.2 item 2 and §17 D-8.
- Form: the map v1 precedent, `AMENDMENT_6_1_CROSSWALK_ALIAS.md` c089f7b7 with PI-1103f and its CC-235 read.
- Objects365 class names appear only in the git-excluded entries file (§5), never here (CC-228 Ruling 6(b); the c089f7b7
  header). Classes are named here by their pinned id. Two loanwords that equal a class name (ids 275 and 283) are
  described, never quoted (CC-296r2 N7).

## 1. Replaced text (v3.1 §6.1, l.328-330)

Old: "Entries proposed by an open LLM are tagged `instrument` (never gold) and listed separately; the instrument LLM's
id, revision and prompt sha are recorded in `b_pa1_registry.json` (W2)."

New:

> **Step-4 instrument entries (PI-1108e Q2 (a)).** No open-LLM instrument is used. An entry that no pinned
> Vietnamese dictionary in the repo gives is an agent-drafted proposal, tagged `instrument`, never gold, and listed
> separately. Each such entry names its drafter id.
> - It is drafted under the rules of the step-4 amendment: D8-1 to D8-8, with the §3 reader's readings of D8-3.
> - It is read by a judge at the irreversible tier.
> - It enters the map only through `b_pa1_map_amendments.log`, from an entries file whose own sha and whose named
>   amendment's sha both stand on LOG pin lines.
>
> `b_pa1_registry.json` records `instrument_llm.mode = "agent-drafted, amendment-logged"`, `id = null` and `revision =
> none`. Its drafting-instruction entries point by name to the LOG-pinned step-4 amendment. `instrument` entries never
> enter the §6.2 dictionary-only rows.

v3.1 §12 l.577 ("The `instrument` entries of the map and their source are recorded in `b_pa1_registry.json`") stands
as written. The source is now this amendment.

**Registry state (CC-296 N1, closed).** The registry draft `b_pa1_registry.json` 10000b58 (untracked; under CC-295r3)
records `instrument_llm.mode = "agent-drafted, amendment-logged"`, `id` null and `revision` none. Its `instrument_i` and
`instrument_ii` entries register no drafting rule; they point by name to the step-4 amendment named in each entries
file's provenance and pinned on a LOG line (CC-295r2 W8).

## 2. Scope: two parts, one rule set

| part | trigger (v3.1 §6.1) | drafted | read (irreversible tier, bar 85; PI-1103ad) | pinned | logged |
|---|---|---|---|---|---|
| (ii) | Objects365 classes with no Vietnamese entry in map v1: **262 = 365 − 103** (CC-295 item 10; CC-296 item 2) | now, from class names and map v1 only (§5) | before the rental, with this file | line (B) of §7 | at §6.4 step 4, first |
| (i) | R7-segmented tokens in ≥ 10 slice-A captions of the 4 accepted captioners, covered neither by a map term nor by the stop list | at step 4, from the (i) token list only | mid-run, before the final freeze (D-8; CC-235 precedent), under the same rules and the §3 readings | its own line in form (B), §7 | at step 4, after (ii) |

Both parts:
- are **add-only**: a new entry points to an existing class, and no existing entry is edited or removed;
- never use any decomposer, verifier, judge, CLIPScore or gold output, nor UIT-ViIC references (v3.1 §6.1);
- close at step 4, after which the final map sha is frozen. Nothing is added after that, in tier 1 or later.

## 3. Drafting rules (fixed before any tier-1 output; each follows a registered rule)

| rule | text | follows |
|---|---|---|
| D8-1 | An entry is the ordinary Vietnamese name whose everyday primary sense is the class's referent (**identity**), a kind of it (**kind-of**), or a common regional or spelling **variant** of such a name. Each '/'-alternative of a class name may give its own entry. At most 3 entries per (ii) class. If no ordinary name exists, there is no entry | alias R1, R2 |
| D8-2 | **No broader term.** No entry for a term that, in everyday use, also denotes objects of another pinned class, including a class that is a kind of it. Match order never makes such a term specific. The class then gets only specific terms: a named kind, or a qualified compound that does not denote the other class. If no specific term exists, it gets no entry. This covers a residual "Other …" class, and a broad-category class all of whose names cover other pinned classes | alias R3; PI-1103f hypernym NO; CC-296 Rulings 6-7 |
| D8-3 | **Homonym guard.** If a bare noun is also a common non-object word, or heads a common compound with another sense, then: (ii) uses a classifier or specific form instead (cái, chiếc, con, quả, trái, đôi, khẩu, hạt, …); (i) adds no entry for that token. See the reader's readings below | precision; CC-296 Ruling 2; CC-296r2 Ruling 7 |
| D8-4 | **Referent split.** If the class name's everyday senses (ii), or the token's (i), denote different physical objects, there is no entry; the candidates are listed for the reader. This includes a Vietnamese term whose referent differs by region | addendum 72f27238 §1 (a), (c) |
| D8-5 | **List-context reading.** In this list of physical-object classes, a sense that is a human being, abstract, an activity, a body part or a substance is not a reading. A bare game name gets the game's Vietnamese name | alias R4; PI-1103f Q-R4 |
| D8-6 | **Add-only, mechanical.** No term equals a map term or an earlier logged term after `b_pa1_mid.norm` (NFC, lower case, rescap tone norm); one class per term; existing entries untouched. An (i) entry's term is the listed token itself | v3.1 §6.1; `check_entries` |
| D8-7 | **Barred inputs.** No mention or document frequency beyond the (i) trigger itself, no count from any set, no UIT-ViIC, no gold, no Paper A output, no expected Δ. No dictionary or web text is pasted in or cited as a drafter's rationale; a record of a reader's ruling may cite it (CC-296r2 N8). The reader applies the references of §6 | v3.1 §6.1; alias §2 "never used" |
| D8-8 | A misspelled class name is read as the evident word. The entries file keeps the exact pinned string | — |

**Reader's reading of D8-3, part 1 (CC-296 Ruling 2).** This is a labelled reading, not a new rule, and it binds the
(i) part at step 4 too.

The matcher fact behind it (`score_coco_probe.vi_objects`, then `vi_classes`):
- the caption text is first rewritten by the `LEX_V2` rules;
- each term is then matched as a substring delimited only by non-letters. A term therefore fires inside any
  space-separated compound or reduplicative that contains it;
- terms are tried in list order (map v1 terms first, then the logged additions), and each matched span is consumed.

So D8-3 fires when the term, as a delimited string, also carries one of these in common everyday language:
- (a) a distinct lexical sense: a homonym, a body part, or an adjective or verb;
- (b) a different physical object, through a common compound or reduplicative.

It does **not** fire for a figurative extension of the object itself, for example 'phao cứu sinh', 'hồng tâm', 'cần
câu' (in 'cần câu cơm'), 'chìa khoá' and 'bức tranh'. When D8-3 fires, the fix is a classifier or specific form that
the other sense does not contain; if none exists, there is no entry.

**Reader's reading of D8-3, part 2 (CC-296r2 Ruling 7 (c)-(f)).** Also a labelled reading, not a new rule; it binds
the (i) part at step 4 too.
- **(c) Both sides of the term.** D8-3 is tested on both sides of the delimited term.
  - A classifier form fixes only a left-side compound.
  - A right-side compound (term + modifier) that names another object or carries another sense is fixed only by a
    right-qualified specific form that the compound does not contain. If none exists, there is no entry.
- **(d) Colour names.** A colour name built on the term ('xanh trứng vịt', 'vàng trứng gà', 'màu cà tím') is a
  distinct lexical sense under (a).
- **(e) Folk kinds.** A compound that names a folk kind of the referent does NOT fire, for example 'bướm đêm', 'tôm hùm
  đất', 'trứng vịt lộn', 'nấm mèo' and 'hươu sao'. A compound that names an object not understood as a kind of it DOES
  fire, for example 'sư tử biển', 'tỏi tây', 'chanh leo', 'lựu đạn' and 'thang máy'.
- **(f) "Common everyday language" is the reader's call, recorded by id.** Specialist or rare compounds do not fire.
  - Ruled not common (CC-296r2): ids 191 ('bộ chuyển đổi xúc tác'), 223 ('nhà máy in'), 239 ('cái ví dụ', speech
    only), 251 ('mít xoài', a cultivar), 299 ('trái dừa nước'), and 275 (a bird compound of the loanword, described,
    not quoted).
  - Kept as folk kinds under (e): ids 322 ('bướm đêm') and 359 ('tôm hùm đất'). A step-4 or later challenge to any of
    these must cite new evidence.
- **The figurative exception of part 1 stands**, for example 'kẹo đồng' (188), 'não cá vàng' (274), 'lá cờ đầu' (28),
  'lột mặt nạ' (209), 'lá bài tẩy' (277) and 'cây nấm lùn' (292).

Further rules:
- **Tag.** `dictionary` only when a pinned dictionary source of map v1 gives the link; otherwise `instrument`. None of
  the 262 (ii) classes is COCO-linked, and map v1's dictionary sources are COCO-80 lexicons, so every (ii) entry is
  `instrument`.
- **Order.** Entries are ordered longest first: by words, then characters, then class id. `amend` logs them in that
  order, and `final_doc` appends them after the map v1 terms (b_pa1_mid reading 15).
- **Coverage.** Every listed class or token is worked through, in id or token order. No class or token is ranked or
  selected by any criterion.

## 4. Enforcement in code, and the amendment-log form

`scripts/b_pa1/b_pa1_mid.py`, read at `b8afa120` (a draft under CC-295r3; the committed sha at `H_B` governs, P1):
- **The entries-file pin (CC-295r2 W7).** `amend` refuses any entries file whose own sha256 does not stand, with its
  file name, on a LOG pin line (`b_pa1.pin_line`; an 8-hex sha never matches).
- **Registry mode and amendment pin.** `amendment_ok` refuses every `instrument` entry unless both hold:
  - the registry's `instrument_llm.mode` is `agent-drafted, amendment-logged`;
  - the entries file's `provenance.amendment` has a `name` and `sha256` that stand on a LOG pin line (line (A), §7).
- **`check_entries`.** It refuses:
  - an entries file without provenance `drafter` and `utc`;
  - an entry without `vi`, `src` i|ii, `tag` dictionary|instrument or a reason;
  - a class that is not in the pinned list;
  - an (ii) entry whose class is not listed, or an (i) entry whose term is not a listed token;
  - a term already in the map or the log;
  - an `instrument` entry without a drafter id (`[A-Za-z0-9._:+-]{1,80}`).
- **`amend`** appends one line per accepted entry to `b_pa1_map_amendments.log`, in file order, never edits a line,
  and refuses a line of any other form. **The amendment-log form** (approved, CC-296 Ruling 8):

```
<YYYY-MM-DDTHH:MM:SSZ> ADD src=<i|ii> tag=<dictionary|instrument> o365_id=<class id> entries=<64-hex sha of the entries file, as on its own pin line: line (B) of §7 for (ii), the (i) line of §7 for (i); CC-295r2 W7> drafter=<drafter id, '-' for dictionary> vi=<the normalised Vietnamese term as a JSON string>
```

- **`final`** writes the final map: map v1 plus the logged rows in log order. It records the log's sha
  (`amendments_log_sha256`), which the final-map freeze pin and parity run 2 carry.

## 5. The pre-drafted (ii) entries, v1.3 (part (ii), read with this file)

**Entries file** `.session_backup/2026-11-08/b_pa1/d8_ii/b_pa1_d8_ii_entries_v1_3.json` (git-excluded, in the `amend
--entries` schema).
- The v1, v1.1 and v1.2 files (ade835e7, f8527a06, 1b06acaf) are kept unchanged and are never pinned.
- The v1.3 file holds:
  - `provenance`: drafter, utc, and `amendment` = this file's repo path and sha;
  - `entries[]`: vi, src, tag, o365, why, drafter;
  - `not_proposed[]` and `shadowed_by_earlier_terms[]`;
  - `changes_from_v1[]`, `changes_from_v1_1[]` (carried unchanged) and `changes_from_v1_2[]` (v1.2 → v1.3, one row
    per class, naming its D8 rule and "CC-296r2 Ruling 6").
- It embeds this file's sha, so its own sha is not written here; it stands on line (B).

**Builder, validator and sweep tools:** `.session_backup/2026-11-08/b_pa1/d8_ii/build_v1_3/`.
- `d8_data_v1_3.py` is an explicit patch over `d8_data_v1_2.py`. `strike()` asserts that each struck term is present,
  that a class has at most 3 entries, and that a no-entry class is empty. The earlier data modules are beside it.
- `build_d8.py` is unchanged from v1.2 (CC-296r2 N9).
- `validate_v1_3.py` is `validate_v1_2.py` with the two file names changed. Its summary line now prints each case's
  computed status in place of fixed words (CC-296r2 N6). On a passing run the line has the same wording as v1.2's.
- The round-2 reader's tools are copied from `/tmp/cc296r2_tools/` so that round 3 can re-run them (CC-296r2 W4). The
  shas are in the package report:
  - `sweep.py` and `probe.py`: only the entries filename is changed (v1_2 → v1_3), as W4 asks.
  - `cand.py` and `inside13.py` **keep reading v1_2**, a stated deviation from W4's wording. Both rebuild v1.3 from
    v1.2 by applying the Ruling 6 STRIKE and CAND lists. Pointed at the v1.3 file, they would find no struck term and
    would add the 16 replacements a second time.
  - `inside13.py`: its hard-coded `/tmp/cc296r2_tools/cand.py` path is changed to the `build_v1_3/cand.py` copy, so it
    survives the loss of `/tmp`.
  - The other files are byte-equal.
  - The package report shows that the v1.3 file equals `cand.py`'s reconstruction.
  `sweep_out.json` holds class names; like the whole directory, it is git-excluded and never committed.

**Inputs** (class names and map v1 only):

| input | sha256 |
|---|---|
| map v1 `.session_backup/2026-11-03/b_pa1/map_v1_build2/b_pa1_map_v1.json` (freeze l.1334) | 497b430abfcdc1ef6d36cb306e7c3b76fd1bedac2a500584f0d80244e6a3fed5 |
| crosswalk v1, same dir | 869ab3e84dab3749691f3e91ee981124f721d47f7718bd737214e9fe8bb42631 |
| class list `.session_backup/2026-11-02/b_pa1/o365_categories_v1.json` (R6 pin) | 2c7bf111b062b0515a86693d5da160bc5ece25d64bf604c5c6d9e5ad033de360 |
| alias v2 (link rules R1-R4) | 9e7f359b5aa557a71e1005d2b0adf871fe5fd952c7f657e78facebeca255ceb3 |
| (ii) list, classes only: `.session_backup/2026-11-08/b_pa1/d8_ii/coverage_classes_only/coverage.json` | 775dd9ed1bcb890020a299b421a3e7ed203eaf9b66f2ca6a2ddc7a3bfc5354e9 |

The (ii) classes ∩ crosswalk links = 0. No caption, count, gold, UIT-ViIC content, Paper A output or dictionary text
was used by the drafter.

**Counts (v1.2 in brackets; each equals the CC-296r2 Ruling 6 expectation):**

| item | value |
|---|---|
| classes with entries / no entry | 233 / 29 (235 / 27) |
| entries (all `instrument`, `src=ii`, drafter `claude-opus-5-5`) | 347 (350) = 318 − 19 + 16 + 32: 19 struck, 16 Ruling 6 replacements |
| by type | identity 182, variant 56, kind-of 44, classifier form 65 (189 / 56 / 42 / 63). Struck: identity 8, kind-of 4, classifier form 7. Added: classifier form 9, kind-of 6, identity 1 |
| entries per class | 1 entry: 129 classes; 2 entries: 94; 3 entries: 10 (129 / 97 / 9) |
| no entry, by rule | D8-2 11 (ids 4, 90, 104, 106, 112, 121, 129, 162, 226, 245, 256); D8-4 12 (125, 130, 132, 171, 176, 215, 216, 243, 244, 295, 304, 321); D8-3 3 (301, 310, 325); D8-1/D8-5 1 (253); D8-5 1 (340); D8-6 1 (257) |
| shadowed entries (never fire under list order) | 19 (19), the same set; no replacement is shadowed. 14 classes have no live entry, the same 14: ids 10, 43, 48, 122, 124, 160, 168, 169, 306, 317, 335, 345, 355, 365. For 355 and 365 the cause is the `LEX_V2` rewrite of 'bóng bàn' |
| "inside another class's term" (the term stands inside another class's term but does not denote it) | ids 64, 182, 183, 190, 365 (v1.2: also 238, which leaves with 'cơm') |

**Changes v1.2 → v1.3** (CC-296r2 Ruling 6 = W4; 19 entries struck in 14 classes; replacements only from the Ruling 6
list; the full row for each is in `changes_from_v1_2[]`):

| id | rule | struck | replacement (accepted) |
|---|---|---|---|
| 72 | D8-3(a)/(b) | 'nến' | 'cây nến', 'ngọn nến' |
| 136 | D8-3(b) | 'quả chanh', 'trái chanh' | 'chanh vàng' |
| 158 | D8-3 | 'xẻng' | 'cái xẻng' |
| 159 | D8-3(a) | 'ớt' | 'quả ớt', 'trái ớt' |
| 167 | D8-3(a) | 'thớt' | 'cái thớt' |
| 173 | D8-3(b) | 'cái thang', 'chiếc thang' | 'thang nhôm' |
| 186 | D8-3(a)/(b) | 'quả trứng', 'trứng gà', 'trứng vịt' | 'quả trứng vịt', 'trứng luộc', 'trứng ốp la' |
| 238 | D8-3(b) | 'cơm' | 'cơm trắng' |
| 262 | D8-3(a)/(b) | 'tỏi' | 'tép tỏi' |
| 297 | D8-3(a) | 'cà tím' | 'quả cà tím', 'trái cà tím' |
| 310 | D8-3(b) | 'quả lựu', 'trái lựu' | — no entry |
| 325 | D8-3(a)/(b) | the bare animal term | — no entry |
| 337 | D8-3(b) | 'củ cải' | 'củ cải trắng' |
| 351 | D8-3(a) | 'phở' | — ('bún', 'mì tôm' kept) |

The v1.1 → v1.2 changes (29 classes) are in v1.2 §5 and in `changes_from_v1_1[]`; the v1 → v1.1 changes are in
`changes_from_v1[]`. CC-296r2 Ruling 1 closed W1, and Ruling 2 accepted keeping the older tables only in the entries
file.

**Reader-check outcomes.** CC-296 Rulings 5-7 are carried as written (CC-296r2 Ruling 4), except where CC-296r2
Ruling 6 overrules them:
- the pre-accepted 136 and 186 forms are struck;
- the keeps 'cơm' and 'thớt' (CC-296 Ruling 4) and 'phở' (CC-296 Ruling 7) are struck.

**Kept borderline entries (CC-296 Ruling 4, N3, as amended by CC-296r2 Ruling 3):**
- the figurative-extension set of §3;
- 'thuốc lá', 'xà phòng'/'xà bông', 'khoai tây chiên' (231; 304 stays no entry), 'bún', 'mì tôm', 'vòi nước', 'hộp
  quẹt', 'máy ủi', 'quạt hút' and 'mắt kính';
- the 5 entries inside another class's term (ids 64, 182, 183, 190, 365).

**Sweep keep list (CC-296r2 Ruling 8), by id:** 13 17 24 28 29 30 32 34 49 53 54 55 60 61 64 65 96 108 143 148 163 175
180 185 188 191 197 199 209 213 219 223 228 232 233 237 239 241 247 251 252 260 264 267 274 275 276 277 283 284 287 289
292 299 308 312 322 324 342 343 352 354 358 359 362. Their sweep firings are non-phrases, kinds, dishes, parts or
accessories, or uses ruled under part 2 (e)/(f) of §3.

**Parity run 2 cannot move because of the (ii) entries** (CC-296 item 4). The (ii) classes have no crosswalk link.
Under list-order matching with consumed spans, the appended terms match only residual text and add no COCO-80 class.
So the micro and macro Δ are unchanged by them, and only `o365_hits_without_coco80` can rise. The (i) entries are not
covered by this statement.

## 6. Mandatory read (irreversible tier, bar 85; round 3 is the last)

- **What.** This file and the v1.3 entries file, before the rental. Round 3 is a one-judge FULL read (CC-296r2 Ruling
  9). The (i) entries are read at step 4 under the same rules and the §3 readings.
- **The reader may use:**
  - the class list, map v1, the crosswalk and alias v2;
  - the three references of addendum §1 (OLD, RHU/Collins, WIK). For Vietnamese terms, **WIK includes
    vi.wiktionary** (CC-296 item 9), and the quotes the reader relies on are recorded in the ruling.
  No caption, no gold, no UIT-ViIC.
- **Scope (CC-296r2 Ruling 9):**
  - W4/W5 by id;
  - the mechanical re-runs: counts, order, shadows, rebuild and `validate_v1_3.py`;
  - a re-run of `build_v1_3/sweep.py` on the v1.3 entries. It must give no firing outside the §5 sweep keep list and
    the kinds of the Ruling 6 replacements, and it must end with 0 ERR lines; any "search too busy" query is re-run
    until it answers.
- **A correction** makes a new entries file (new name, new sha) tied to a cited D8 rule. Earlier files are kept. A
  change to this file makes a new version, and the entries file is rebuilt against its new sha.
- **No GO in round 3:** ESCALATE_TO_PI. The (ii) entries are then not used pre-drafted, and B runs with map v1 plus (i)
  only.

## 7. Pin lines and order (CC-296 Ruling 9; CC-296r2 P1)

**Order:**
1. The round-3 GO of this read.
2. CC-295r3 GO and the gatekeeper commit `H_B`.
3. **P1 (gatekeeper):**
   - check that the working `b_pa1_mid.py` sha256 equals `git show H_B:scripts/b_pa1/b_pa1_mid.py`;
   - re-run `build_v1_3/validate_v1_3.py` in a fresh empty dir;
   - quote its one line verbatim on line (B), but only if the line ends "RESULT PASS" and its `mid=` prefix equals the
     committed sha;
   - if CC-295r3 changed `norm`, `check_entries`, `amendment_ok`, `cmd_amend`, `final_doc`, `vi_classes` or the
     matcher order, also re-run the count and shadow checks (CC-296 Ruling 10).
4. Line (A), then line (B).
5. The P9 pin lines, then the rental.

The amendment's own pin is line (A); the entries file's own pin (CC-295r2 W7) is line (B). Two rules for the lines:
- no class name stands on either line, and line (B) carries only the 8-hex md prefix;
- the md path with its full sha stands only on line (A).

(A) the amendment:

```
<date -u +%FT%TZ> OPS-<MMDD>b-d8a-pin: PIN manuscript/prereg/2026-11-01_b_pa1_tier1/D8_AMENDMENT_DRAFT_v1_3.md <full 64-hex sha> (v3.1 §6.1/§6.4 step 4 amendment D-8 per PI-1108e Q2 (a), CC-295 W5/reading 18; rules D8-1..D8-8 with the §3 readings of D8-3 (CC-296 Ruling 2, CC-296r2 Ruling 7); read at irreversible 85 by CC-296r<k> GO; agent-drafted, drafter claude-opus-5-5; logged only at step 4)
```

(B) the (ii) entries file:

```
<date -u +%FT%TZ> OPS-<MMDD>b-d8e-pin: PIN b_pa1_d8_ii_entries_v1_3.json <full 64-hex sha> (D-8 part (ii) entries, git-excluded at .session_backup/2026-11-08/b_pa1/d8_ii/; provenance.amendment = D8_AMENDMENT_DRAFT_v1_3.md <8-hex>; CC-295r2 W7; read by CC-296r<k> GO; (ii) 347 instrument entries for 233 classes, 29 with no entry, 19 shadowed; map v1 497b430a; mid <8-hex committed sha at H_B>; validate v1_3: <the quoted one-line result>; logged only at step 4)
```

(i) the step-4 (i) entries file (form (B); written after the mid-run (i) read's GO, before `amend` of (i)):

```
<date -u +%FT%TZ> OPS-<MMDD>b-d8i-pin: PIN b_pa1_d8_i_entries_v1.json <full 64-hex sha> (D-8 part (i) entries, git-excluded; provenance.amendment = D8_AMENDMENT_DRAFT_v1_3.md <8-hex>; CC-295r2 W7; read by CC-<id> GO at irreversible 85 (mid-run, D-8); (i) <n> entries for <n> listed tokens of coverage.json <8-hex>; mid <8-hex>; validate: <the quoted one-line result>; logged only at step 4, after (ii))
```

**At step 4:**
- `amend` with the pinned (ii) file;
- then `amend` with the pinned (i) file;
- `final`, the final-map freeze pin and parity run 2 (B_RUN_DOC §11.2).

## 8. Limits

- **No map changes now.** No entry exists in any map. Map v1 stays frozen. Nothing is logged before step 4.
- **A proposal only.** Agent-drafted, never gold, never evidence. Tagged `instrument`, outside the §6.2 rows.
- **Vietnamese senses.** No pinned Vietnamese dictionary exists in the repo. Senses rest on WIK (vi.wiktionary
  included) and the reader's knowledge, with the quotes recorded. The drafter checked none of them. The round-2 sweep
  is bounded by vi.wiktionary's titles and the reader's knowledge (CC-296r2 confidence).
- **Code state.** The validator results bind `b_pa1_mid.py` b8afa120 only. P1 re-runs them at `H_B`.
- **Recall.** Over rounds 1-2, 51 of v1.1's 350 entries were struck or replaced (32, then 19). Six classes have no entry
  because of strikes: 162, 176, 256, 301, 310 and 325. This protects precision in the main Objects365 rows; the parity
  Δ is unaffected.
- It says nothing about B's results: no Δ, no count from any set.
