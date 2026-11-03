# PINS-A amendment to C-PVR-T1 — DRAFT v1.4

DRAFT v1.4, not committed. Written 2026-11-03T02:45:30Z (`date -u`). Internal prereg record, not paper text.

**Commit chain and base.** The PINS-A record to commit is `PINS_A_DRAFT.md` (v1, 7161d3b2) + `PINS_A_DRAFT_v1_1.md`
(d8342e45) + **this file**. v1.4 is self-contained: it restates every binding row and refers back only to v1.1, whose
text it keeps where a section says "unchanged from v1.1". `PINS_A_DRAFT_v1_2.md` (89d72557) and `PINS_A_DRAFT_v1_3.md`
(2cb191ed) stay **uncommitted snapshot records** (judge reads CC-236 and CC-236r2); nothing in v1.4 depends on them,
and neither is part of the commit chain.

**Rulings this text carries:** CC-234 (design GO 92: J-V = V1, J-L, J-O, J-T = 64 / 8, J-C = 32, J-A8(a) = A1 caption,
J-SEG = RDRSegmenter, J-OVQA = YES, lengths only); PI-1103g (LOG l.1315: Q-P1 = money ≤ 350k VND; Q-A8 = NO, A8
deletes REJECTED spans only; Q-V2 = NO); CC-236 (design GO 92; Q-LEX = L1, Q-A7 = (b), Q-SPLIT = `c_pvr_run.py`,
Q-LLAVA = keep, selftest override); CC-236r2 (GO 93 for pin 1).

**What v1.4 changes against the CC-236r2 code:** only the synthetic test sentences. The gatekeeper's 8/6-gram scan
(`ngram_scan_cen.py`) found that several fixture sentences shared 8- or 6-grams with existing caption corpora. Every
flagged sentence, in the code and in this text, was reworded to unusual synthetic wording that exercises the same case
(B1 accents, B2 compound objects, W2 colour phrase, EN decomposer, W1 failure, reassembly). No rule, value or code
path changed; the expected outputs changed only with the sentences. The scan output is in §4.5.

No registered gate, threshold or status changes. The stated overrides are listed in §12.

**Inputs** (sha256, first 8 hex): prereg `PREREG_DRAFT_v1_2.md` 0a2f0773 (commit 8282874); amendment
`AMENDMENT_CC222_DRAFT_v1_3.md` c565e67a (db97b93); `ERRATUM_CC227_GA_SCHEMA.md` a116fa85; `G_C1_record.json`
1f65b2ae; `G_C2_record.json` 767998f8 (2ab08b3); `scripts/c_pvr/gates.py` bf4d5f64; `C_PIVOT_CHECKPOINT_v1_1.md`
0e265477; `C_DIRECTION_v3_2026-11-01.md` 99dbe46b; decisions CC-229, CC-232, CC-234, CC-236 (and r2); LOG l.1315.

## 0. Status summary

| # | PINS-A item (prereg §9.1 l.632-635) | v1.1 | v1.4 |
|---|---|---|---|
| A1/A2 | VI captioner / verifier `Gregor/mblip-bloomz-7b` @ 4d95b91d | FILLED | FILLED; loader row W10 (§1) |
| A3 | EN `liuhaotian/llava-v1.5-7b` @ 4481d270 | FILLED, minor OPEN | FILLED (Q-LLAVA = keep, CC-236); conditions before any EN decode (§12) |
| A4 | prompts | VI drafted; verifier 3 options | **FILLED**: 6 files in `scripts/c_pvr/prompts/`, byte-equal to the shas of §2.1-2.2 (EN = W4); verifier V1 (CC-234 J-V; Q-V2 NO) |
| A4' | `max_new_tokens`, verifier-call cap | proposed | **FILLED** by CC-234 J-T / J-C; in code as one constant each (§2.5-2.6) |
| A4'' | proposition string, quote rule, arm seeds, generation dict | — | **FILLED**; GO in CC-236 Ruling 2 with conditions (a), (b) (§12) |
| A5 | k = 4, greedy, order | FILLED | FILLED (J-O) |
| A6 | decomposers | option chosen | rules GO (CC-236); **code fixed for B1, B2, W1, W2** (§4.2); fixtures, invariants and the judge's fuzz sentences pass |
| A7 | EN map | OPEN | L1 ruled (CC-236); plural rule fixed (W3); **rebuilt** `en_oiv7_map.json` 0fe2c438 |
| A8 | proxy regex / extractor / normaliser, `rapidfuzz` | OPEN | **FILLED** (`proxy_regex.txt` c7839aa4, `rapidfuzz` 3.14.6 in the lock, code §4.4) |
| A9 | retrieval encoder | FILLED | unchanged |
| A10 | OpenViVQA json sha256 | OPEN | OPEN until `ovqa-pin` runs after PINS-A pin 1 (§16); code and the counting-rule LOG template ready (§5, W5) |
| A11 | `OI_TEST_URL`; `c_pvr.py` sha | value FILLED; sha OPEN | `c_pvr.py` 76fc73c9 (fixture rewording of bc512418, which CC-236r2 read); URL byte-equal to `gates.py` l.66 |
| A12 | parity input shas | FILLED | unchanged; the `parity` command itself is OPEN under PINS-B (§4.1) |
| A13 | NB-CAP | P1 OPEN | money ≤ 350k VND (PI-1103g); **formula and ledger written (W7, §8)**; P1 OPEN until the speed test |

## 1. Model selection by N7 (A1, A2, A3) — unchanged from v1.1 §1, except two rows

- **A1/A2 loader row (W10), replaces v1.1 l.110:** `transformers` `Blip2ForConditionalGeneration` / `Blip2Processor`.
  The repo at 4d95b91d also holds `pytorch_model-*.bin` weights; **only the two safetensors shards are loaded**:
  `from_pretrained(snapshot, local_files_only=True, use_safetensors=True, torch_dtype=bfloat16)` (`c_pvr.py
  load_mblip`; the selftest asserts these keyword values). Before loading, the four files of the v1.1 table (two
  shards, `tokenizer.json`, `config.json`) are sha-checked; any mismatch is a FAULT and nothing is decoded.
  dtype **bfloat16** and **batch size 1** are [proposal] (padding changes greedy output; bf16 fits a 24 GB GPU).
- **A3 (still OPEN-minor):** LLaVA inference-code commit, CLIP tower weight sha. New: `liuhaotian/llava-v1.5-7b` ships
  only pickled `.bin` weights, so "safetensors only" cannot hold for the EN model as pinned. `c_pvr.py load_llava`
  refuses EN decode until the Q-LLAVA conditions of §12 are met (Q-LLAVA = keep, CC-236). The LLaVA-1.5 conversation string is in code
  (`LLAVA["conv"]`, the `llava_v1` template with the image token before the text) and must equal the pinned LLaVA
  commit's template; that check is part of the A3 row.

## 2. A4 — Prompts and verifier

### 2.1 Captioner prompts: FILLED

VI templates unchanged from v1.1 §2.1 (J-L: English instruction naming Vietnamese, the mBLIP Table 8 XM3600 template).
Rendering rules 1-6 of v1.1 §2.1 unchanged (J-O: rank 1 first; A2/A3 keep their draw order).

**W4, EN templates.** The v1.1 EN text had no source. PINS-A adopts the documented lmms-eval NoCaps default prompt
(`_default_template_nocaps_yaml`, default prompt "Provide a one-sentence caption for the provided image.", read by the
CC-234 judge on raw GitHub). The shas were computed with `printf` in the scratchpad at 2026-11-03T00:38:41Z, before
the repo files were created:

| file | exact text | sha256 |
|---|---|---|
| `cap_en_0.txt` (S4 = A0, EN) | `Provide a one-sentence caption for the provided image.` | `494392f0754c0f3adc0e644463073c8730ea4f39ed6ac640634195c3b76e84c2` |
| `cap_en_k.txt` (S1, S3, S5) | `Captions of similar images:⏎{demos}⏎Provide a one-sentence caption for the provided image.` | `7c4b0dfba310bafc1e21bfeab78856ead7e2d3591c2b2d674c4a6a1f8c2f1a7c` |

Alternative (not adopted; W4 accepted by CC-236): the v1.1 drafted text, `cap_en_0.txt` 40791b9b / `cap_en_k.txt`
3fcd6277, recorded as an undocumented choice. EN is benchmark-only, not a gate.

**Files now in the repo, byte-equal to the pinned shas** (`sha256sum scripts/c_pvr/prompts/*`; `c_pvr.py prompts()`
re-checks them at every start, and a changed byte is a FAULT in the selftest):

| file | sha256 |
|---|---|
| `cap_vi_0.txt` | f6e05b0b7510a1bf5c8a00b203a81f077f28bd5b59a5fc25d5afeead9e618feb |
| `cap_vi_k.txt` | 2653672de35c932dc2b3a088053dd7965a679eabb12f4cf4a363a89d31f9c42d |
| `demo_line.txt` | c068abccda584d10e3cf1e56b053fe6d107487b9276b9153608b57c4994af128 |
| `cap_en_0.txt` | 494392f0754c0f3adc0e644463073c8730ea4f39ed6ac640634195c3b76e84c2 |
| `cap_en_k.txt` | 7c4b0dfba310bafc1e21bfeab78856ead7e2d3591c2b2d674c4a6a1f8c2f1a7c |
| `ver_3way.txt` | bcb9230851622e5d9afa98f0765bf2bffd05b4b4ba37aa8bd0508d300881313d |

The four VI/verifier files were copied byte-for-byte from `.session_backup/2026-11-03/c_pins2/prompts/`.

### 2.2 Verifier form: V1 (CC-234 J-V; PI-1103g Q-V2 = NO)

`ver_3way.txt` bcb92308, mBLIP's documented 3-way template (S15 Table 8, XVNLI). The override of v4.1 l.276 ("đúng
prompt 3 nhãn của FAIR") stands as stated in v1.1 §2.2: no such prompt exists in `rescap/`; the registered prereg
§6.1 governs. V2 and V3 are not used.

### 2.3 Mapping, parser, proposition string: FILLED in code

- Mapping and parser unchanged from v1.1 §2.3; code `c_pvr.py parse_label`. Fixtures in the selftest (CC-234
  item 14): `Yes`, `yes.`, ` Maybe,`, `No` parse; the empty string, `Có`, `không`, `yesno` and `The answer is yes`
  are UNCERTAIN and counted as parse failures (the first ASCII-letter run of `The answer is yes` is `the`).
- **Proposition string (CC-234 item 3) [proposal]:** `{proposition}` = the span text after `clean()` (NFC, every
  whitespace run to one space, trimmed), with each ASCII double quote `"` replaced by `'`. Curly quotes are kept (they
  do not close the template's quote). Code `c_pvr.py proposition`; the template is filled by plain substring
  replacement, never `str.format`.
- C1 wording (no validated Vietnamese verifier) and the reporting list are unchanged from v1.1 §2.3.
- An object proposition carries `classes` (a list; one class, or several after the B2 merge of §4.2) and the
  character spans of its `mentions`. Its label applies to every class it carries (A12: deleted when any of its
  classes is verified absent).

### 2.4 A8 (W1; PI-1103g Q-A8 = NO)

- **Input = the A1 caption.** This is registered, not a proposal: C_DIRECTION v3 l.201 ("Tạo caption bằng A1"),
  brought into the prereg by §5.1's heading reference to the v3 §4 table (CC-234 Ruling 6(a)).
- **Deletion = REJECTED spans only.** Registered by v3 l.201 ("Mệnh đề REJECTED bị xoá bằng cùng luật xoá span");
  the PI kept it (PI-1103g, Q-A8 = NO). A8 is therefore **not** coupled to the chosen UNCERTAIN variant. v1.1 §2.4's
  coupling text is withdrawn; there is no override of v3 l.201.
- Same verifier, same prompt `ver_3way.txt`, same per-image cap (one constant, §2.6), same decomposer and the same
  span-deletion rule (prereg §6.4). No regeneration prompt.
- **Disclosed confound (CC-234 Ruling 6(b)):** under PVR-drop, PVR − A8 also differs in the UNCERTAIN rule (PVR deletes
  UNCERTAIN demonstration spans, A8 keeps UNCERTAIN caption spans). Under PVR-keep the two rules coincide. The tier-1
  report states this beside the primary contrast; no new arm.
- Code: `A8_INPUT = "A1"`, `A8_DELETE = "rejected"` (one switch; the value `"coupled"` exists only so the selftest
  can test both values, CC-234 item 6). An A8 caption whose propositions are all deleted becomes empty and is counted.

### 2.5 `max_new_tokens` (J-T; W3)

64 for captions, 8 for the verifier (CC-234 J-T). W3 wording fix to v1.1 §2.5: "CONCAP decoded mBLIP with at most 25
tokens" is replaced by "**CONCAP's own model decodes at most 25 tokens** (2507.20411v1, inference paragraph)". The 64
does not depend on that figure. Truncation share (`finish = length`) is reported per arm.

### 2.6 Per-image verifier-call cap (J-C)

32 calls per image, one constant `CAP` used by PVR (both variants), A8, S1 and S2. Overflow propositions, taken in
order (demonstration 1 first, left to right), are UNCERTAIN unverified and counted (`cap_hits`), never retried. Under
PVR-drop, overflow propositions are deleted (CC-234 Ruling 5). The selftest asserts that the PVR path and the A8 path
each spend exactly 32 calls on 40 propositions and that the literal 32 occurs once outside the selftest.

### 2.7 Arm seeds (CC-234 item 4) [proposal]

| arm | seed | use |
|---|---|---|
| A2 (random-k) | 20262002 | `random.Random(f"{seed}|{image_id}").sample(sorted(datastore ids), 4)`; draw order kept |
| A3 (sample-k in top-7) | 20262003 | `…sample(ranked[:7], 4)`; draw order kept |
| A7 (count-matched drop) | 20262007 | per demonstration, `sample(range(n_props), n_dropped_by_PVR)` |

- One generator per (arm seed, image id); string seeding is sha512-based, so the draws do not depend on the process
  hash seed or on the order in which images are processed (the selftest checks both).
- All three lie outside the bootstrap streams 20261102-20261603 (prereg §5.5-5.6: 20261102, 20261103, 20261104 + r,
  r < 500) and never share a generator with them.
- **A7 matching unit:** per demonstration, so A7 also matches PVR's emptied-demonstration count (v3 §5.4,
  "A7 khớp với PVR cả ở tỉ lệ này") (CC-236 GO 92).
- **A7 variant (Q-A7 = (b), CC-236 GO 91):** at tier 1, A7 follows **PVR-drop** (the tie-break default of prereg §6.3);
  at tiers 2-3 it follows the variant §6.3 selects. No new arm, no override of §5.1.
- **W5, binding on the tier-1 report:** any PVR-keep − A7 contrast is labelled **"not count-matched"**.

### 2.8 Generation settings (CC-234 item 2) [proposal]

One dict per call kind, written into every output header (`c_pvr.py header`):
`do_sample=False, num_beams=1, num_beam_groups=1, num_return_sequences=1, temperature=None, top_k=None, top_p=None,
typical_p=None, repetition_penalty=1.0, no_repeat_ngram_size=0, encoder_no_repeat_ngram_size=0, length_penalty=1.0,
diversity_penalty=0.0, min_new_tokens=0, early_stopping=False, use_cache=True, bad_words_ids=None,
forced_bos_token_id=None, forced_eos_token_id=None, renormalize_logits=False, output_scores=False,
return_dict_in_generate=False`, `max_new_tokens` 64 / 8, `eos_token_id` and `pad_token_id` from the pinned tokenizer.

- The model's own `generation_config` (from the repo's `generation_config.json`, if any) is **replaced** by this dict
  before each call, and the same dict is passed as `generation_config=` (`c_pvr.py generate`).
- Prompt ids are stripped from the output only when the output starts with them; otherwise the output is kept whole.
  Whether Blip2 `generate` echoes the prompt under the GPU host's `transformers` version is checked by the GPU-host
  selftest (OPEN with the GPU lock): if the echo were mis-stripped, every verifier answer would parse as a failure.
- The `transformers` version is not chosen here (GPU lock, §11). Its `GenerationConfig` validation of `None` values
  is checked on the GPU host.

## 3. A5 — k and decoding: unchanged from v1.1 §3 (C5 wording carried)

## 4. Code and files (A6, A7, A8, A11)

Owner: the C code drafter. Laptop CPU only, `python -I`, interpreter = the C venv of the lock. No weights, no data,
synthetic fixtures only. Nothing committed.

### 4.1 Files (sha256 as drafted; proposed `scripts/c_pvr/SHA256SUMS` lines in §4.6)

| file | sha256 | status |
|---|---|---|
| `scripts/c_pvr/c_pvr.py` | 76fc73c903da3256993490d2963a953a5ece4318de914f250c5654a4925b5091 | FILLED (B1, B2, W1-W3 fixed; fixtures reworded for the scan): prompts, render, parser, proposition string, verify with cap, PVR/A2/A3/A6/A7/A8/A11/A12 helpers, reassembly, VI/EN decomposers, EN map builder, proxy, mBLIP loader + `generate`, `header`, `ovqa-pin` (fetch / skeleton / count), refusals, `RESCAP_RAW_TONE` FAULT, selftest |
| `scripts/c_pvr/prompts/*.txt` (6) | §2.1 | FILLED |
| `scripts/c_pvr/proxy_regex.txt` | c7839aa46bb8eadcfef593ca36ef65cebce92cb39ca55d6807648278fee8e222 | FILLED (§4.4) |
| `scripts/c_pvr/en_oiv7_map.json` | 0fe2c438fe3d86cb95d7fd5d9ef3733bddbb3ebbfb2445eb4874e599fa445146 | rebuilt by `c_pvr.py en-map --write` (L1, W3) |
| `scripts/c_pvr/requirements_c_pvr.lock` | fd2f0f1273213db74c00884bd461d524166d33df42d8fc62e439630b69846e75 | laptop lock: 46 wheels with sha256, `--require-hashes` install tested offline in a fresh venv; JDK and VnCoreNLP files as comments |
| `scripts/c_pvr/c_pvr_mutants.py` | 80d4b279df95b6a03504e3fa1102ca042a20f5b6ef31deb2a02ad9b94273dd64 | FILLED (§4.5) |

Not written, with the reason:
- `en_lexicon.json` and `build_en_map.py` as separate files: the L1 lexicon rule is code (`c_pvr.py build_en_map`),
  so the lexicon is not a second input file.
- `parity`: prereg §3.3 puts the loader in `gates.py load_labels`, and amendment v1.3 §1 adds G-B code to `gates.py`
  only through PINS-B. A loader in `c_pvr.py` would be a second loader, which parity exists to rule out. **OPEN, owner
  PINS-B.** No XM3600 label CSV was opened.
- `owners`, `lists`, `w25`, `score`: go to the second file `c_pvr_run.py` (Q-SPLIT, CC-236), written later under
  conditions (i)-(iv) of §12. `c_pvr_job.sh` and the GPU lock: later steps (§11).
- Cut-first arm helpers A4 (CLIP scorer), A5 (LMCap model + prompt), A9 (ITM scorer), A10 (re-derivation prompt):
  OPEN; each needs its pin before the speed test if kept, or a recorded cut (§11).
- `decompose_vi.py` / `decompose_en.py`: the decomposers are functions in `c_pvr.py` (draft v1.1 §4.1 allowed this).

### 4.2 Decomposers (A6; J-SEG; W2, W9)

**W2, reading of prereg §6.2 (CC-234 Ruling 7), replaces v1.1 §4.2's pyvi "explicit acceptance" wording:** the
proposition rules are deterministic hand-written rules; the segmenter or parser underneath must be pinned and
deterministic (fixed files, CPU, byte-identical output on re-run). The registered parenthetical names an EN dependency
parse, which is a trained model, so the same reading applies to both languages. Under it spaCy (pinned wheel + model)
is acceptable for EN; for VI the choice is RDRSegmenter (rule-based, house-pinned).

**Pins (W9: the jar alone does not pin the rules):**

| item | value | source |
|---|---|---|
| VnCoreNLP repo | github `vncorenlp/VnCoreNLP` commit 62bbc58fe5d113c898eae112656be97dcf50b3a0 (2023-02-11) | GitHub API, 2026-11-03T00:31Z |
| `VnCoreNLP-1.2.jar` | 9e2811cdbc2ddfc71d04be5dc36e185c88dcd1ad4d5d69e4ff2e1369dccf7793 | = the B protocol pin (`b2.py` l.1084) |
| `models/wordsegmenter/wordsegmenter.rdr` | 9e62f96bd93e37a24f364238e8d8ae986fa5dad6dbc9f4eae622ab3651b7fa06 | = the B record (`manuscript/prereg/2026-10-19_b_n2_record/b_n2_gate.json` `/env/wordsegmenter.rdr`), an independent cross-check |
| `models/wordsegmenter/vi-vocab` | 0a47c5b55bbce163029d37730a67b9479740388695c29c106c112b815613eaa5 | new pin, same commit |
| JDK | OpenJDK 21.0.12.1 (Ubuntu 24.04 package, `/usr/bin/java`) | `java -version` |
| call | `java -Xmx700m -XX:+UseSerialGC -XX:ActiveProcessorCount=1 -jar VnCoreNLP-1.2.jar -fin /dev/stdin -fout /dev/stdout -annotators wseg`, batched with a marker line (house pattern, `scripts/kit_b/protocol_pilot.py rdr`) | `c_pvr.py rdr`; no Python wrapper (no `py_vncorenlp`) |
| spaCy | `spacy` 3.8.18, `en_core_web_sm` 3.8.0 (wheel sha256 in the lock) | checked at load (`spacy_nlp`) |

**rescap import closure:** the code pins `rescap/chair.py` (e47d249a) and `rescap/vi/lexicon.py` (fbc945f2), as the
scorer does (prereg §2.3). The other modules that `import rescap.chair` loads are recorded, not asserted: the
selftest prints all 12 shas (§4.5) and the read compares them with HEAD: `rescap` b712bea4, `metrics` e0296ec5,
`repro` 72320019, `svp` 5b7f5292, `svp.entailment` 4462f44d, `svp.matching` a9253060, `vi` f898963e,
`vi.classifier` 966cdab1, `vi.color` 242fc46f, `vocab` c9143b2d.

The files sit on the laptop under `~/c_pvr_tools/vncorenlp/` (ext4; env `VNCORENLP_DIR` overrides); `rdr()` re-hashes
all three before every call.

**Rules (one per language, same span builder; design GO in CC-236, implementation GO in CC-236r2):**
1. Text = `clean()` of the caption.
2. Tokens: RDRSegmenter words (VI) or spaCy tokens (EN). The EN parse is used for sentence split, `cc` conjunctions
   and the NOUN/PROPN tags.
   - **B1, alignment.** RDRSegmenter rewrites old-style tone placement in its output (`tòa` → `toà`, `hòa`, `khỏe`,
     `thủy`, `Thúy`, `qúy` → `quý`; judge's `fuzz2.py`). Syllables are therefore aligned to character offsets after a
     length-preserving fold on **both** sides, `rescap.chair.norm_tone(x.lower())` (the same fold as the mention
     search). Offsets and every output string stay on the original caption; a fold that changed a length is a
     FAULT.
   - **`_` in a caption.** `_` is RDRSegmenter's word joiner (it splits `a_b` into `a`, `_`, `b`). The segmenter and
     the mention search see the caption with each `_` replaced by a space (same length, so offsets do not move);
     spans and proposition text are cut from the original (`Chiếc xe_máy màu đỏ.` → `Chiếc xe_máy màu đỏ`).
3. Chunks end at `,` `;` `:` `.` `!` `?`, at the VI words `và`, `cùng`, `còn`, `nhưng`, `trong khi` (EN: a token with
   dependency `cc`, or a sentence start), and at every token inside a scene-text span (rule 6).
4. Object mentions: VI = `rescap/chair.py objects_in` (e47d249a, the outcome instrument, prereg §3.1) located in the
   caption, kept when the class is one of the 69 keys of `vi_oiv7_map.json`; EN = longest match of the
   `en_oiv7_map.json` forms on lowercased tokens whose last token is a NOUN/PROPN.
5. One proposition per mapped mention: every token since the previous proposition in the same chunk (or since the
   chunk start), so quantity words, classifiers, determiners, adjectives and the relation verb or preposition come
   with the mention; then the mention; then, VI only, following attribute words: single colours
   (`rescap.vi.lexicon.COLORS`), `màu`, size words (`lớn, nhỏ, to, cao, thấp, dài, ngắn`) and, **W2**, whole
   multi-word colour phrases (`rescap.chair._COLOUR_PHRASES`, e.g. `xanh lá cây`), taken only when the phrase ends on
   a token boundary inside the same chunk (`Một chiếc áo màu xanh lá cây treo trên cây.` → `Một chiếc áo màu xanh lá
   cây` | `treo trên cây`). Tokens after the last mention of a chunk belong to no proposition.
   - **B2 rule [proposal, the judge's recommended form]:** mentions whose token ranges overlap (two objects inside one
     segmenter word: `thuyền_buồm`, `quần_áo`, `giày_dép`, `người_người`) are merged into **one** proposition that
     carries every class. It is verified once (one call against the cap), and its label applies to all its classes.
     `Người đàn ông râu bạc thêu quần áo tím.` → `Người đàn ông` [đàn ông] | `râu bạc thêu quần áo tím` [quần, áo].
     The span end can no
     longer fall to or below the mention start (no index wrap).
   - **Invariants, checked on every caption at run time and on every fixture in the selftest:** each object
     proposition contains every one of its mention spans; propositions are ordered and pairwise disjoint. A breach
     is a FAULT for that caption (rule 9).
6. One scene-text proposition per quoted or cue span of the §4.4 extractor, kind `text` (`scene_spans`). Its deletion
   span includes the quote marks. Digit and all-caps tokens are not separate propositions here, so a count stays
   inside its object proposition (`2 con chó đang chạy trên cỏ.` → `2 con chó`); the proxy and A11 keep the full
   v3 §7.2 extractor.
7. Reassembly (`rebuild`, shared by PVR, A6, A7, A8, A11): delete the dropped spans; a sentence that lost a span and
   has no noun left is dropped (VI noun = any `objects_in` mention; EN noun = a NOUN/PROPN token); then the fixed table
   (whitespace runs to one space; no space before `. , ; : ! ?`; a run of `, ; :` to its first mark; `, ; :` before
   `. ! ?` removed; leading punctuation and trailing `, ; :` removed). A demonstration whose propositions are all
   dropped is emptied: dropped, never back-filled; n = 0 uses the zero-shot template.
8. `RESCAP_RAW_TONE` set before the first `objects_in` call is a FAULT (N4) and aborts the run.
9. **W1, per-caption decomposition failure [proposal]:** a caption whose decomposition FAULTs (alignment, a mention
   not located, an invariant breach, a failed segmenter call) gets **zero propositions, is kept whole in every arm**
   (it still passes the reassembly table, like an A6 caption) and is counted per arm and set as **`decomp_fail`**,
   reported beside P_obj^VI, never a gate. A batch segmenter failure falls back to one call per caption, so one
   caption cannot abort a batch. The recorded reason is this file's FAULT text or an exception class name; no
   FAULT text carries a caption word. Only a pin mismatch of the segmenter files (and rule 8) aborts.
   - The per-arm and per-set `decomp_fail` counts are read from the `decompose` records by the job or scorer (the
     arm helpers such as `a8_caption` do not carry the flag).
   - **No hidden fallback:** a batch in which **every** caption is a `decomp_fail` (e.g. a Java that starts but fails
     on every call) is a run-level FAULT, owned by `c_pvr_job.sh`; otherwise PVR and A8 would silently equal A1.

Fixtures and expected propositions (synthetic sentences written for the test; the selftest asserts all 14 VI and
2 EN fixtures, the classes on 5 of them, the invariants on all, and that none is a `decomp_fail`):
- `Một người đàn ông tí hon ôm áo tím ngáp cạnh chiếc xe đạp gỗ.` → `Một người đàn ông` | `tí hon ôm áo tím` |
  `ngáp cạnh chiếc xe đạp`;
- B1: `Tòa nhà cao bên cạnh dòng sông.` → `Tòa nhà cao` | `bên cạnh dòng sông`; `Người thủy thủ khỏe mạnh đứng trên
  thuyền hòa bình.` → `Người` | `thủy thủ khỏe mạnh đứng trên thuyền`; `Chiếc xe_máy màu bạc ngủ đông.` → `Chiếc
  xe_máy màu bạc`;
- B2: `Ba chiếc thuyền buồm hát vang trên sông băng.` → `Ba chiếc thuyền buồm` [thuyền, buồm] | `hát vang trên
  sông`; `Quần áo tự gấp mình trên dây điện.` → `Quần áo` [quần, áo]; `Một gian hàng đổi giày dép lấy dưa.` → `Một
  gian hàng đổi giày dép` [giày, dép]; `Bàn ghế nhảy múa trong phòng.` → `Bàn ghế` [ghế] | `nhảy múa trong phòng`
  (`bàn` is not one of the 69); `người người người` → `người người` | `người`;
- W2: `Một chiếc áo màu xanh lá cây treo trên cây.` → `Một chiếc áo màu xanh lá cây` | `treo trên cây`;
- W1: a caption made unalignable by a stub segmenter is a `decomp_fail`, kept whole, while the other caption of the
  same batch decomposes normally.
- EN: `A man in a mauve shirt juggling a bicycle, and two dogs are knitting near the volcano.` → `A man` | `in a
  mauve shirt` | `juggling a bicycle` | `two dogs`.

**Determinism:** the selftest runs `decompose` twice per language in two fresh processes (different hash seeds) and
requires byte-equal output.

**Judge's reproducers against the fixed code** (offline, `unshare -rn`, venv python): see §4.5.

Disclosed: the RDRSegmenter (rule-based) and the spaCy parser (a trained model, CPU) were run on synthetic sentences
only. No captioner or verifier was run.

### 4.3 EN class map (A7): L1 (CC-236), plural rule fixed (W3), rebuilt

`c_pvr.py en-map --write` builds `en_oiv7_map.json` (0fe2c438fe3d86cb95d7fd5d9ef3733bddbb3ebbfb2445eb4874e599fa445146) deterministically from `vi_oiv7_map.json` (27f2b1ca)
alone, under L1 (Q-LEX = L1, CC-236 GO 93): forms = each class's `pos` OI display names, lowercased, a trailing
qualifier in parentheses dropped, plus one plural; `pos`/`neg` copied unchanged; tie rule (own `neg` list,
then shortest `pos`, then file order); 70 collisions recorded; 8 classes get no form.

**W3, plural rule (fixed now, because the map is frozen before G-B and never amended after, prereg §3.4):** the head
word is the word before ` of ` if there is one, else the last word; no plural is added when the head already ends in
`s` but not `ss`/`us` (`jeans`, `shorts`, `trousers`, `sneakers`, `high heels`, `flip-flops`, `cut flowers`, `moths
and butterflies`) or is itself an irregular plural (`people`); irregular table `buffalo, human, man, woman, child,
person, goose, knife, mouse, foot, tooth` (`human` → `humans`, not `humen`); `bird of prey` →
`birds of prey`. The junk forms of the first build (`humen`, `peoples`, `jeanses`, `shortses`, `trouserses`, `sneakerses`, `high
heelses`, `flip-flopses`, `cut flowerses`, `moths and butterflieses`, `bird of preys`) are gone; `humans` is covered.
440 forms in all (first build: 449). Selftest invariants: 69 keys equal to the VI map's, `pos`/`neg` equal per class,
forms unique across classes, the file equal to a fresh build, plus these plural cases.

Set difference against the first build (f4c02920 → 0fe2c438), computed, not stated: removed exactly the 11 junk
forms above; added exactly `humans` and `birds of prey`; `_collisions` and every `pos`/`neg` list unchanged. Known
remaining junk, harmless because it never matches a caption: `aircrafts` and 7 `… aircrafts` forms (the plural rule
does not know that `aircraft` is invariant). Not fixed, to keep this diff to the CC-236 items; a later fix would need
its own diff read before G-B.

### 4.4 Scene-text proxy (A8): FILLED

- `proxy_regex.txt` (c7839aa4), applied only to the NFC-casefolded question text, each line wrapped in word
  boundaries: `chữ`, `dòng chữ`, `ghi gì`, `viết gì`, `tên (?:cửa hàng|quán|đường)`, `biển (?:hiệu|báo) ghi`, `số
  (?:điện thoại|nhà)`, `giá`. **This is exactly the v3 §7.1 example list, with no addition**: the "…" inside `tên
  (cửa hàng|quán|đường|…)` is not extended, and nothing was tuned on ViTextVQA or OpenViVQA questions (none were
  read). Extending it is a choice for the read, made before any question is read.
- Extractor (`extract`, the proxy's and A11's; the decomposer uses its quote and cue part only, §4.2 rule 6): quoted spans `"…"`, `“…”`, `«…»`, and `'…'` only when the opening quote does not
  follow a letter or digit and the closing quote does not precede one (so English possessives are not quotes)
  [proposal]; spans after `dòng chữ`, `có tên`, `chữ`, `ghi` cut at the first `. , ; : ! ?` or quote; tokens with a
  digit, or all-caps with ≥ 2 letters [proposal]; overlapping finds are dropped, earliest and longest first.
- Normaliser (`norm`): NFC → casefold → every non-letter/digit (and `_`) to a space → whitespace collapsed; diacritics
  kept. `strip_marks=True` (NFD, marks removed, `đ` → `d`) is the sensitivity analysis only.
- Match classes (`classify`): match = equal, or containment when the shorter string has ≥ 3 characters; near = a
  shared token of ≥ 2 characters, or `rapidfuzz.distance.Levenshtein.normalized_similarity` ≥ 0.5 (selftest: equal
  to a stdlib Levenshtein on four pairs); otherwise uncovered. P_text = match / (match + near + w · uncovered), w = 1
  default, w = 0 sensitivity; R_text counts the selected answers found in the caption at token boundaries.
- `rapidfuzz` 3.14.6, wheel sha256 in the lock (venv `~/.venvs/c_pvr`, nothing installed globally).

### 4.5 Selftest and mutants

**Selftest** (`~/.venvs/c_pvr/bin/python -I -B scripts/c_pvr/c_pvr.py selftest`, run under `unshare -rn`, sockets also
patched to raise): v1.1 §4.5 checks 1-13, CC-234 item 14, the fixtures and
invariants of §4.2, direct breach tests of both invariants, the merge rule, the injected per-caption failure (W1),
and the plural cases (W3). Output:

```
rescap import closure (sha256[:8]): rescap=b712bea4 rescap.chair=e47d249a rescap.metrics=e0296ec5 rescap.repro=72320019 rescap.svp=5b7f5292 rescap.svp.entailment=4462f44d rescap.svp.matching=a9253060 rescap.vi=f898963e rescap.vi.classifier=966cdab1 rescap.vi.color=242fc46f rescap.vi.lexicon=fbc945f2 rescap.vocab=c9143b2d
selftest ok  TIER 1 / DEV-EXPLORE (C-PVR-T1)  c_pvr.py 76fc73c903da3256993490d2963a953a5ece4318de914f250c5654a4925b5091
```

**N-gram scan (gatekeeper's `ngram_scan_cen.py`, on `c_pvr.py`, `c_pvr_mutants.py` and this file):** **NGRAM SCAN PASS**: 0 hits (8-gram and 6-gram) against KTVIC, OpenViIC, UIT-ViIC and COCO-Karpathy; positive controls hit in all four corpora.

**Mutants** (`c_pvr_mutants.py`, 80d4b279): the unmutated copy runs first and must pass; each mutant replaces one
exact string and runs the selftest on a copy under the scratchpad on ext4 (never `/mnt/d`). Result: **83 mutants, 83 killed, 0 survived; 1 equivalent (`b_old_form`, survives as proven)**.

Added for CC-236: `align_no_fold`, `align_raw_compare` (B1); `no_underscore_map`; `no_merge`,
`merge_drops_class`, `check_contain_off`, `check_disjoint_off` (B2, one per invariant); `decomp_fail_aborts`,
`decomp_fail_drops_caption` (W1); `no_colour_phrase` (W2); `plural_no_human`, `plural_only_rule_off`,
`plural_last_word` (W3). `vi_no_attr` and `en_no_plural` were re-targeted to the new code lines.

**Equivalent mutant (proof in the harness):** `b_old_form` restores the first draft's span-end expression
`min(max(right(i1), i1), nxt)` in place of `max(min(right(i1), nxt), i1)`. After `merge_units`, the next unit starts
at or after the current unit's end, so `nxt ≥ i1`; `right()` only moves forward, so `right(i1) ≥ i1`. Both
expressions then equal `min(right(i1), nxt)`. The first draft's defect needed overlapping units, which `no_merge` covers (the
invariant check then fires and the fixtures fail).

**Judge's reproducers** (`.session_backup/2026-11-03/cc236_fuzz/`, run against the final code, offline; the judge's
sentences are not quoted here, to keep this text clear of the n-gram scan):
- `fuzz.py` (26 sentences): **26 OK, 0 FAULT**; a copy that also prints `decomp_fail` shows none. The accent case, the
  `_` case, the colour phrase and the repeated `người` decompose as the rules of §4.2 say (spans disjoint).
- `fuzz2.py` prints RDRSegmenter's own output, unchanged by design (7 accent rewrites and the `_` split, as the judge
  found); the code aligns through them.
- `fuzz3.py` (6 sentences) run unchanged stops with `KeyError: 'cls'`, because the proposition key is now `classes`
  (a list, B2). A copy with only that key renamed (`sed 's/p\["cls"\]/p["classes"]/'`) shows every compound pair
  merged into one proposition carrying both classes, every proposition containing its objects, and no overlapping
  span.

History (disclosed): first draft ab9ea051, 70/70 killed, after 3 early survivors were fixed (a fixture that could not tell the sentence-drop rule apart; a dead left-extension; a custody test path on `/mnt/d`, which created an empty `/mnt/d/x`, removed). CC-236's fuzz sentences then exposed B1 and B2; both were fixed in one diff (bc512418, 83/83 + 1 equivalent, CC-236r2 GO 93); after the rewording: 76fc73c9, 83/83 + 1 equivalent again. For the n-gram scan the fixture sentences were reworded (this version).

| mutant | result |
|---|---|
| `maybe_to_supported` | KILLED |
| `parsefail_to_supported` | KILLED |
| `parse_last_run` | KILLED |
| `parse_skips_leading_word` | KILLED |
| `quote_rule_removed` | KILLED |
| `order_reversed` | KILLED |
| `backfill` | KILLED |
| `n0_keeps_kshot` | KILLED |
| `k_5` | KILLED |
| `no_prompt_sha` | KILLED |
| `clean_no_nfc` | KILLED |
| `no_sentence_drop` | KILLED |
| `no_emptied` | KILLED |
| `tidy_space_before_punct` | KILLED |
| `cap_33` | KILLED |
| `overflow_order_reversed` | KILLED |
| `cap_split_per_arm` | KILLED |
| `a8_uses_a0` | KILLED |
| `a8_switch_coupled` | KILLED |
| `a8_coupled_is_rejected` | KILLED |
| `pvr_drop_is_keep` | KILLED |
| `seed_a2` | KILLED |
| `seed_a3` | KILLED |
| `seed_a7` | KILLED |
| `seed_in_boot_range` | KILLED |
| `a3_top_8` | KILLED |
| `repetition_penalty_1_5` | KILLED |
| `num_beams_5` | KILLED |
| `sampling_on` | KILLED |
| `max_new_caption_25` | KILLED |
| `safetensors_off` | KILLED |
| `not_local_only` | KILLED |
| `repo_genconfig_kept` | KILLED |
| `no_prompt_strip` | KILLED |
| `no_weight_sha` | KILLED |
| `dtype_fp16` | KILLED |
| `diacritics_stripped` | KILLED |
| `norm_no_nfc` | KILLED |
| `ge3_to_ge2` | KILLED |
| `near_0_4` | KILLED |
| `near_no_token_rule` | KILLED |
| `w_default_0` | KILLED |
| `question_no_boundary` | KILLED |
| `caps_one_letter` | KILLED |
| `apostrophe_quotes` | KILLED |
| `no_relation_gap` | KILLED |
| `vi_no_attr` | KILLED |
| `align_no_fold` | KILLED |
| `align_raw_compare` | KILLED |
| `no_underscore_map` | KILLED |
| `no_merge` | KILLED |
| `merge_drops_class` | KILLED |
| `check_contain_off` | KILLED |
| `check_disjoint_off` | KILLED |
| `decomp_fail_aborts` | KILLED |
| `decomp_fail_drops_caption` | KILLED |
| `no_colour_phrase` | KILLED |
| `plural_no_human` | KILLED |
| `plural_only_rule_off` | KILLED |
| `plural_last_word` | KILLED |
| `vi_va_not_delim` | KILLED |
| `en_cc_not_delim` | KILLED |
| `no_text_props` | KILLED |
| `decomposer_digit_tokens` | KILLED |
| `raw_tone_unchecked` | KILLED |
| `no_vnc_sha` | KILLED |
| `en_map_pos_altered` | KILLED |
| `en_tie_no_own` | KILLED |
| `en_no_plural` | KILLED |
| `oi_url_changed` | KILLED |
| `sha1_no_blob_header` | KILLED |
| `ovqa_main_revision` | KILLED |
| `ovqa_no_unlink` | KILLED |
| `ovqa_no_sha1_check` | KILLED |
| `ovqa_dev_qa_3546` | KILLED |
| `ovqa_dev_images_1071` | KILLED |
| `ovqa_test_count_off` | KILLED |
| `ovqa_rule_sha_unchecked` | KILLED |
| `ovqa_dev_images_optional` | KILLED |
| `ovqa_zip_sha_unchecked` | KILLED |
| `skeleton_leaks_values` | KILLED |
| `custody_mnt_allowed` | KILLED |
| `refusal_removed` | KILLED |
| `b_old_form` | EQUIVALENT (survives, proof above) |

### 4.6 Proposed `scripts/c_pvr/SHA256SUMS` lines (the gatekeeper adds them at commit)

```
76fc73c903da3256993490d2963a953a5ece4318de914f250c5654a4925b5091  scripts/c_pvr/c_pvr.py
80d4b279df95b6a03504e3fa1102ca042a20f5b6ef31deb2a02ad9b94273dd64  scripts/c_pvr/c_pvr_mutants.py
c7839aa46bb8eadcfef593ca36ef65cebce92cb39ca55d6807648278fee8e222  scripts/c_pvr/proxy_regex.txt
0fe2c438fe3d86cb95d7fd5d9ef3733bddbb3ebbfb2445eb4874e599fa445146  scripts/c_pvr/en_oiv7_map.json
fd2f0f1273213db74c00884bd461d524166d33df42d8fc62e439630b69846e75  scripts/c_pvr/requirements_c_pvr.lock
494392f0754c0f3adc0e644463073c8730ea4f39ed6ac640634195c3b76e84c2  scripts/c_pvr/prompts/cap_en_0.txt
7c4b0dfba310bafc1e21bfeab78856ead7e2d3591c2b2d674c4a6a1f8c2f1a7c  scripts/c_pvr/prompts/cap_en_k.txt
f6e05b0b7510a1bf5c8a00b203a81f077f28bd5b59a5fc25d5afeead9e618feb  scripts/c_pvr/prompts/cap_vi_0.txt
2653672de35c932dc2b3a088053dd7965a679eabb12f4cf4a363a89d31f9c42d  scripts/c_pvr/prompts/cap_vi_k.txt
c068abccda584d10e3cf1e56b053fe6d107487b9276b9153608b57c4994af128  scripts/c_pvr/prompts/demo_line.txt
bcb9230851622e5d9afa98f0765bf2bffd05b4b4ba37aa8bd0508d300881313d  scripts/c_pvr/prompts/ver_3way.txt
```

## 5. A10 — OpenViVQA (W5)

Revision, LFS and blob ids unchanged from v1.1 §5. `c_pvr.py ovqa-pin` implements v1.1 §5 with these details:
- `fetch`: one `curl -sS --fail -A vsps-research -o <name>.part <URL at cc85c24c>` per json into
  `~/.vsps_sealed/c_pvr/ovqa/` (mode 0700, refused under `/mnt/`); one pass gives size, sha256 and git-blob SHA-1;
  size and SHA-1 must equal the hub values; a mismatch or a curl error unlinks the `.part`, logs a FAULT row in
  `ACCESS_LOG.tsv` and stops; on success the file is renamed, set 0400 and logged; `ovqa_pin.json` is written once.
- `skeleton`: per file, key names at the top level only, value type names and container lengths, record field names
  (≤ 24, else their count); no value and no string length is printed.
- `count --rule F --rule-sha H [--dev-zip Z]`: the rule file's sha must equal the one in its LOG line.

**W5, the pre-written counting-rule LOG line (template for the coordinator; written before any count is computed):**
> `<date -u> OPS-11xx-ovqa-rule: counting rule for c_pvr.py ovqa-pin count, file <path> sha256 <H>, written from the
> skeleton only (no field value read). Per file it names the top-level container of images and of QA; (b) uses
> container lengths only: a file whose distinct-image count would need field values asserts its QA length only.
> Expected counts come from the 11-01 scratchpad count recorded in C_TEST_DATA_AND_LETTERS l.28 (dev 1,070 / 3,545;
> train 9,129 / 30,833; test 1,000 / 14,035), made before C's custody rules; the check is an identity check, not
> exploration. (c) dev image names (the one string field allowed, for the §8 fetch list) must be 1,070 distinct
> members of dev-images.zip after its LFS sha256 ff6a0e87 matches; only the count is printed.`

The dev rule must name an images container (1,070 is asserted for dev); for train and test, `"images": null` asserts
the QA length only. Any mismatch is a FAULT and the proxy is not run. The three sha256 values stay OPEN until the run.

## 6. A11 — `OI_TEST_URL` and `c_pvr.py`

`OI_TEST_URL = "https://open-images-dataset.s3.amazonaws.com/test/{file}"`, byte-equal to `gates.py` l.66 (bf4d5f64):
the selftest reads the assignment from `gates.py` by AST and compares. `c_pvr.py` sha256 76fc73c903da3256993490d2963a953a5ece4318de914f250c5654a4925b5091 (as drafted; it
changes if the read asks for edits, and the final sha is the one committed).

## 7. A12 — Parity inputs: unchanged from v1.1 §7

## 8. A13 — NB-CAP (PI-1103g; W7 of CC-236)

- **Answered (PI-1103g, LOG l.1315):** the tier-1 cap is **money, ≤ 350k VND**. Origin: C_DIRECTION v4.1 l.457 set a
  hard cap of 20 GPU-h on a 4090 ("khoảng 350 nghìn đồng ở 17.499 đ/giờ"); 350,000 / 17,499 = 20.0 GPU-h. The hours
  reading (37 GPU-h on any host, up to 647,463 VND on a 4090) would be new spend beyond PI-1102a Q-cost; not used.
- **Formula (CC-236 Ruling 5, W7):**
  `cap_GPUh = min(⌈1.25 × P1⌉, ⌊350,000 / r_host⌋)`, where P1 is the GPU-h projection from the speed test on the
  named host and `r_host` (VND per GPU-h) is named in the Q-custody host amendment (prereg §8.3 l.617, one-judge
  read). If the projection does not fit, arms are cut in the §5.1 order (A10 → A5 → A9 → A3 → A2 → A4 → A11); if it
  still does not fit, the PI decides.
- **What counts against the 350k VND [recommended, W7]:** every VND billed for the C tier-1 block on the named host,
  **speed test included**, read from the rental balance lines before and after (house money-gate pattern, LOG
  l.1164). Idle billed time of that block counts.
- P1 must come from a speed test on the named host. M1 is kept only until 18:00 VN 03/11 (PI-1102o); the C GPU block
  is several steps away (§16), so a rental for C needs the host amendment first, and no C spend happens before Q11.

## 9. CC-229 carries W2, W3, W5: unchanged from v1.1 §9

## 10. CC-232 carries C1-C8: unchanged from v1.1 §10

## 11. Rows: closed, still OPEN

**Closed (ruled or filled; pinned only by the two-stage pin of §16):** the A4 prompts and verifier form, 64 / 8 and `CAP`, the A8 input and deletion rule, the A6 segmenter, parser and
code, the A7 map, the A8 proxy files and `rapidfuzz`, the A11 sha, Q-P1; Q-LEX L1, Q-A7
(b), Q-SPLIT, Q-LLAVA and the selftest override (CC-236 Ruling 3); the [proposal] values (CC-236 Ruling 2, with
conditions); B1, B2, W1-W3 fixed in code (pending CC-236r2).

**Still OPEN:**

| row | why open | owner | closed by |
|---|---|---|---|
| code pin (`c_pvr.py`, `c_pvr_mutants.py`, `en_oiv7_map.json`) | CC-236 NEXT_ROUND | CC-236r2 one-judge diff read | GO, then PINS-A pin 1 (§16) |
| A10 3 json sha256 + identity (a)-(c) | download after pin 1 | coordinator: counting-rule LOG line, then `ovqa-pin` | PINS-A pin 2 (§16) |
| A13 P1 and `r_host` | speed test; host amendment | coordinator | host amendment + P1 LOG line |
| GPU lock, GPU-host selftest (prompt echo; `GenerationConfig` with `None`; `weights_only` wrapper) | on the named host | C code drafter on the host | lock + selftest output + read |
| LLaVA code commit, CLIP tower sha, LLaVA env | Q-LLAVA conditions | coordinator + drafter | pins + read |
| `c_pvr_job.sh` | GPU block (two-pass decomposition on the laptop recommended) | C code drafter | file sha + read |
| `c_pvr_run.py` (`owners`, `lists`, `w25`, `score`) | Q-SPLIT conditions (i)-(iv) | C code drafter | own selftest + mutants + read, before `owners` runs |
| `parity` (N3) | the loader belongs to `gates.py` under PINS-B | PINS-B drafter | PINS-B |
| cut-first helpers A4, A5, A9, A10 | model/scorer/prompt not chosen | drafter → PINS-A addendum (one judge), before the speed test | pins or a §5.1 cut |
| W3 n_e_power drop (≤ 4) | needs G-B | G-B run | `gb_counts.json` |

## 12. Rulings recorded (CC-236) and stated overrides

| item | ruling | conditions |
|---|---|---|
| Q-LEX | **L1** (GO 93) | plural rule fixed in the same diff (W3, done) |
| Q-A7 | **(b)** (GO 91): A7 follows PVR-drop at tier 1, the §6.3-selected variant at tiers 2-3 | W5 label "not count-matched" on any PVR-keep − A7 contrast |
| Q-SPLIT | **second file `c_pvr_run.py`** (GO 92) | (i) it imports every shared constant from `c_pvr.py` (`OI_TEST_URL`, `LABEL`, `SEALED`, `refuse`/`BARRED`, `CAP`, `prompts`) and holds no second value; its selftest asserts amendment v1.3 l.133's equality for `w25`; (ii) it refuses to run unless sha256(`c_pvr.py`) equals the PINS-A pin; (iii) own selftest and mutants; (iv) this text renames the §11 command lines (below) |
| Q-LLAVA | **keep `liuhaotian/llava-v1.5-7b` @ 4481d270** (GO 91) | before any EN decode, speed test included: every `.bin` shard and the CLIP tower files sha-checked; `torch.load` forced to `weights_only=True` by a wrapper that FAULTs if a caller passes `weights_only=False`, asserted in the GPU-host selftest; LLaVA code commit pinned and its conv template byte-compared with `LLAVA["conv"]`. The LLaVA code may need its own `transformers` version (two environments in the GPU lock; feasibility note) |
| [proposal] values (proposition string, seeds, A7 matching, generation dict, bf16, batch 1, extractor) | GO (Ruling 2) | (a) batch size and dtype change only by a diff read before the first tier-1 output, on throughput/memory evidence from the speed test, whose outputs are never read (NB-SPEED); never after any tier-1 output. (b) the GPU-host selftest decides the prompt-echo strip; a failure is fixed by a code diff read before the speed test |
| B2 merge rule, W1 `decomp_fail` rule, W2 colour phrases | GO in CC-236r2 (93) | — |

**Stated overrides of registered lines:**

| registered line | what it says | PINS-A | reason |
|---|---|---|---|
| amendment v1.3 l.119-120, prereg §11 l.746 | `test_c_pvr.py` stays for the `c_pvr.py` subcommands; `python3 scripts/c_pvr/test_c_pvr.py` | the selftest is `~/.venvs/c_pvr/bin/python -I -B scripts/c_pvr/c_pvr.py selftest` (GO 95). **W6:** the interpreter is the C venv of `requirements_c_pvr.lock`, not `/usr/bin/python3`, because spaCy and rapidfuzz are not stdlib | the `gates.py selftest` precedent (v1.3 l.119) |
| prereg §11 l.753-756, amendment v1.3 l.109-110 | `owners`, `lists`, `w25`, `score` are `c_pvr.py` subcommands | they are `c_pvr_run.py` subcommands (GO 92), under conditions (i)-(iv) | one pinned sha must not churn when unrelated subcommands are added (v1.3 l.114 precedent) |

**Renamed §11 command lines (W6):**
```
~/.venvs/c_pvr/bin/python -I -B scripts/c_pvr/c_pvr.py selftest          # replaces python3 scripts/c_pvr/test_c_pvr.py
~/.venvs/c_pvr/bin/python -I -B scripts/c_pvr/c_pvr.py ovqa-pin fetch|skeleton|count ...
~/.venvs/c_pvr/bin/python -I -B scripts/c_pvr/c_pvr_run.py owners && ~/.venvs/c_pvr/bin/python -I -B scripts/c_pvr/c_pvr_run.py lists
~/.venvs/c_pvr/bin/python -I -B scripts/c_pvr/c_pvr_run.py w25 --host laptop --pause-tag <OPS tag>
~/.venvs/c_pvr/bin/python -I -B scripts/c_pvr/c_pvr_run.py score --tier 1
```
`parity` stays with PINS-B (`gates.py`); `gate-b` is `gates.py` (amendment v1.3).

**For the PI:** none. Q-P1 and Q-A8 are answered (PI-1103g); Q-LEX, Q-A7, Q-SPLIT and Q-LLAVA are ruled (CC-236).

## 13. What this draft does not change

- No registered gate, threshold or status. Overrides: only the two command-line rows of §12.
- `gates.py` bf4d5f64, `gates_mutants.py`, SHA256SUMS, `PINS_A_DRAFT.md`, `PINS_A_DRAFT_v1_1.md`,
  `PINS_A_DRAFT_v1_2.md`, the snapshot `.session_backup/2026-11-03/snap/c_pins_v12/` and every committed record are
  byte-unchanged; `PINS_A_DRAFT_v1_2.md` and `PINS_A_DRAFT_v1_3.md` stay uncommitted snapshot records. `proxy_regex.txt`, the
  6 prompt files and the lock are unchanged since their first drafting.
- No model was run (segmenter and parser on synthetic sentences only). No OpenViVQA, NoCaps, Open Images label or
  XM3600 label file was opened or downloaded. No GPU was touched. No LOG line. Not committed.
- **W8 (carried, for the coordinator):** regenerate `.session_backup/2026-11-03/c_pins2/INDEX.txt` without its own row;
  STATE row C text: "C: G-C2 done (2ab08b3, CC-229); pivot CONTINUE (PI-1103b); PINS-A design GO (CC-234, CC-236),
  PI-1103g (cap money ≤ 350k VND; A8 REJECTED-only). Next: CC-236r2 diff read, PINS-A pin 1, `ovqa-pin`, pin 2,
  PINS-B, Q11 ledger ruling, G-B."
- **W9 (process):** this round ran no repo-wide `find` or aislop scan on `/mnt/d`; tests, mutants and scans used
  ext4 copies (scratchpad), and only the named files were read or written on `/mnt/d`.

## 14. Network and file touches (`date -u`; times from the command stamps or file mtimes)

| when (UTC) | what | result |
|---|---|---|
| 2026-11-03T00:30Z | GET `api.github.com/repos/vncorenlp/VnCoreNLP/commits/master` (user-agent `vsps-research`, no auth) | commit 62bbc58f |
| 00:31:03Z-00:31:06Z | GET `github.com/vncorenlp/VnCoreNLP/raw/62bbc58f/…` jar, `wordsegmenter.rdr`, `vi-vocab` into `~/c_pvr_tools/vncorenlp/` | shas §4.2 (jar and rdr equal the house pins) |
| 00:31:16Z-00:31:31Z | `pip download spacy rapidfuzz` from PyPI (pip's default user-agent) into `~/c_pvr_tools/wheels/`; venv `~/.venvs/c_pvr` created | 45 wheels |
| 00:31:34Z | GET `github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/…whl` | 1 wheel; lock §4.1 |
| 00:31Z-01:3xZ | local, CPU, offline (`unshare -rn`): RDRSegmenter and spaCy on synthetic sentences; selftest; mutants (copies under the scratchpad) | §4.5 |
| read only | `scripts/c_pvr/gates.py`, `gates_mutants.py`; `rescap/chair.py`, `rescap/vi/lexicon.py` and their imports; `data/xm3600/vi_oiv7_map.json` (class keys and OI display names; no label); `data/coco_probe/chair_synonyms.txt` (head 5 lines); `scripts/b2_external/b2.py`, `scripts/kit_b/protocol_pilot.py` (code); prereg v1.2, amendment v1.3, C_DIRECTION v3 §4-§7; LOG l.1140, l.1282, l.1299, l.1315; CC-234 | — |
| written (first draft) | `scripts/c_pvr/{c_pvr.py, c_pvr_mutants.py, proxy_regex.txt, en_oiv7_map.json, requirements_c_pvr.lock, prompts/*.txt}` | superseded shas, §4.1 has the current ones |
| CC-236 round (2026-11-03T02:04:45Z and before; no network) | read CC-236 and the judge's three fuzz scripts; edited `c_pvr.py`, `c_pvr_mutants.py` in place; rebuilt `en_oiv7_map.json`; wrote this file; selftest, mutants, fuzz offline under `unshare -rn` on ext4 copies | §4.5 |

## 15. CC-234 and CC-236 fixes: where closed

| fix | closed in |
|---|---|
| CC-234 W1-W10 | closed (CC-236 Ruling 1): W1 §2.4, W2 §4.2, W3 §2.5, W4 §2.1, W5 §5, W6 §8, W9 §4.2, W10 §1; W7, W8 coordinator texts (§13) |
| CC-236 B1 (accent rewrite; `_`) | §4.2 rule 2; fixtures; mutants `align_no_fold`, `align_raw_compare`, `no_underscore_map` |
| CC-236 B2 (two objects in one word; index wrap) | §4.2 rule 5; invariants; mutants `no_merge`, `merge_drops_class`, `check_contain_off`, `check_disjoint_off`; equivalent `b_old_form` |
| W1 (per-caption failure) | §4.2 rule 9 |
| W2 (colour phrases) | §4.2 rule 5 |
| W3 (plural rule; map rebuilt) | §4.3 |
| W4 (two-stage pin) | §16 |
| W5 ("not count-matched") | §2.7 |
| W6 (interpreter; renamed §11 lines) | §12 |
| W7 (cap formula; what counts) | §8 |
| W8 (INDEX, STATE) | §13, coordinator |
| W9 (no repo-wide scans of /mnt/d) | §13 |

## 16. Two-stage pin (CC-236 Ruling 5; W4)

NB-OVQA (prereg §4.3) puts the 3 OpenViVQA json shas in PINS-A, but they are produced by `c_pvr.py ovqa-pin`, which
must be pinned before it touches OpenViVQA bytes (custody). So PINS-A is pinned in **exactly two stages**. Each is a
gatekeeper commit plus a LOG pin line with full shas, naming the CC GO. A filled row is final: it changes only by a
diff read, and never after any tier-1 output. **"PINS-A committed" in the G-B preconditions (prereg §9.3) means both
stages.**

**Stage 1, PINS-A pin 1 (after the CC-236r2 GO):**
- A1/A2: `Gregor/mblip-bloomz-7b` @ 4d95b91d + the 4 file shas + loader row (safetensors only, bf16, batch 1).
- A3: `liuhaotian/llava-v1.5-7b` @ 4481d270 (hub id @ revision).
- A4: the 6 prompt files (shas §2.1); verifier V1; parser and mapping.
- A4': 64 / 8; `CAP` 32.
- A4'': proposition string and quote rule; seeds; A7 matching; generation dict.
- A5: k = 4, greedy, rank 1 first.
- A6: VnCoreNLP 62bbc58f jar / rdr / vi-vocab, JDK 21.0.12.1, spaCy 3.8.18 + en_core_web_sm 3.8.0, the fixed
  decomposer rules (§4.2).
- A7: `en_oiv7_map.json` 0fe2c438 and the L1 rule.
- A8: `proxy_regex.txt` c7839aa4, extractor, normaliser, `rapidfuzz` 3.14.6.
- A9: retrieval encoder `google/siglip2-so400m-patch14-384` @ e8e48729 (prereg §6.2, unchanged).
- A11: `OI_TEST_URL` and the new `c_pvr.py` sha.
- A12: parity input shas (prereg §3.3, unchanged).
- A13: the NB-CAP rule and formula of §8.
- The lock fd2f0f12, `c_pvr_mutants.py`, and the SHA256SUMS lines of §4.6.

**Stage 2, PINS-A pin 2 (A10):** the counting-rule LOG line is written from the skeleton only (template §5, W5); then
`ovqa-pin fetch` / `skeleton` / `count` run under the stage-1 sha (CC-234 J-OVQA: lengths-only identity check). LOG
pin line: revision cc85c24c, the 3 json sha256 values, the `ovqa_pin.json` sha, counts 1,070 / 3,545; 9,129 / 30,833;
1,000 / 14,035 (or FAULT), and `dev-images.zip` LFS ff6a0e87 if (c) is run. A FAULT stops the proxy (NB-OVQA).

**Not PINS-A rows** (prereg §9.1 does not list them), but each is pinned before the first GPU decode (the speed test)
by its own LOG line and, where code is involved, a one-judge read: P1; the Q-custody host amendment (`r_host`, money
ledger); the GPU lock (incl. the LLaVA env); the GPU-host selftest; `c_pvr_job.sh`; the LLaVA code commit and CLIP
tower sha; `c_pvr_run.py` (before `owners` runs). The cut-first arm helpers (A4 CLIP filter, A5 LMCap, A9 ITM, A10
prompt) are arm pins: a PINS-A addendum (one-judge read) before the speed test; they do not gate G-B. Dropping an arm
for any reason other than the §5.1 cost rule overrides §5.1 and goes to the PI.

**Order (CC-236 Ruling 5):** (1) this fix; (2) CC-236r2 diff read; (3) gatekeeper commit + pin 1; (4) counting-rule
LOG line, `ovqa-pin`; (5) pin 2; (6) PINS-B full panel at 92 (drafting may start now; GO and commit after pin 2);
(7) Q11 ledger ruling at 92; (8) G-B once; (9) `c_pvr_run.py` read, `owners` / `lists`, pixel and dev W25 /
self-retrieval; (10) host amendment, GPU lock, host selftest, `c_pvr_job.sh`, LLaVA/CLIP pins, cut-first addendum;
(11) speed test, P1 LOG line, cap re-base; (12) tier-1 block under ≤ 350k VND.
