# PINS-A amendment to C-PVR-T1 — DRAFT v1.1

DRAFT v1.1, not committed, not judge-read. Written 2026-11-03T00:01:26Z (`date -u`). Internal
prereg record, not paper text.

**Base.** v1 is `PINS_A_DRAFT.md` (sha256 7161d3b2), kept unchanged.

**What v1.1 adds:**
- the CC-232 carry list C1-C8 (§10);
- the PI's choice PI-1103b (LOG l.1299): CONTINUE with `Gregor/mblip-bloomz-7b` in both VI roles, under Option 1,
  "post hoc, documentation-only, not a registered gate";
- for the PINS-A read: a resolution of the verifier-form conflict as ranked options (§2.2), a drafted captioner prompt
  pinned by text sha (§2.1), `max_new_tokens` and verifier-call-cap proposals (§2.5-2.6), a build plan with owners and a
  selftest/mutant plan for every code file still missing (§4), and the `ovqa-pin` computation with its dev-set identity
  assertion (§5).

No registered gate, threshold, status or rule changes. Every new value is a [proposal] for the one-judge read.

**What PINS-A is.** Prereg `PREREG_DRAFT_v1_2.md` (0a2f0773, commit 8282874) §9.1 step 5, PINS-A (one-judge read). It
pins: the captioner and verifier (hub id @ revision), the prompts, k = 4, greedy decoding, the decomposers, the EN map
(N13), the proxy regex/extractor and `rapidfuzz` version, the retrieval encoder (NB-ENC), the OpenViVQA revision with
3 json shas and the image LFS shas (NB-OVQA, §8.1), `OI_TEST_URL` and the `c_pvr.py` sha (B3), the parity input shas
(NB-PARITY) and the M1 cap re-base rule (NB-CAP).

**Inputs** (sha256, first 8 hex):

| input | sha256 | commit |
|---|---|---|
| `AMENDMENT_CC222_DRAFT_v1_3.md` | c565e67a | db97b93 |
| `ERRATUM_CC227_GA_SCHEMA.md` | a116fa85 | |
| `G_C1_record.json` | 1f65b2ae | |
| `G_C2_record.json` | 767998f8 | 2ab08b3 |
| `scripts/c_pvr/gates.py` | bf4d5f64 | |
| `CC-229.txt` | d5e1c604 | |
| `CC-232.txt` (`.session_backup/2026-10-13/decisions/`) | — | |
| `C_PIVOT_CHECKPOINT_v1_1.md` | 0e265477 | |

**Rules applied:**
- N7: models are picked by the fixed candidate order, never by Flickr counts or scores.
- Repo revisions are commit hashes from the public HF API (no auth, no token). File shas are given only for files
  already on disk, or as hub LFS sha256 values from pointer metadata. No weight, image, zip or json data file was
  downloaded.
- Nothing is guessed: every value not filled is an explicit OPEN row with its owner.

## 0. Status summary

| # | PINS-A item (prereg §9.1 l.632-635) | v1 | v1.1 |
|---|---|---|---|
| A1/A2 | VI captioner / VI verifier | FILLED | FILLED (re-fetched 2026-11-02T23:55Z, identical) |
| A3 | EN benchmark captioner / verifier | FILLED | FILLED (minor OPEN unchanged) |
| A4 | prompts | OPEN | **captioner template DRAFTED and sha-pinned (§2.1)**. Verifier form: 3 ranked options (§2.2). Mapping and parser DRAFTED (§2.3). A8 needs no prompt (§2.4). Helper prompts for the cut-first arms A5, A9, A10 stay OPEN. |
| A4' | `max_new_tokens`, verifier-call cap | OPEN | **proposed with sources (§2.5, §2.6)** |
| A5 | k = 4, greedy | FILLED | FILLED, plus demonstration order and format (§2.1) |
| A6 | decomposers | OPEN | **option chosen for the read (§4.2)**; code still to be written (owner, tests: §4) |
| A7 | EN map (N13) | OPEN | OPEN, with a build plan (§4.3); not buildable from pinned inputs alone (reason given) |
| A8 | proxy regex / extractor / normaliser, `rapidfuzz` | OPEN | OPEN, with a build plan (§4.4); the spec is fixed in v3 §7 |
| A9 | retrieval encoder | FILLED | FILLED |
| A10 | OpenViVQA | revision and image LFS FILLED; json sha256 OPEN | json sha256 still OPEN; **computation and identity assertion specified (§5)** |
| A11 | `OI_TEST_URL`; `c_pvr.py` sha | value FILLED; sha OPEN | sha OPEN, with a build plan (§4.1) |
| A12 | parity input shas | FILLED | FILLED |
| A13 | NB-CAP | rule FILLED; P1 OPEN | unchanged; host question to the PI (Q-P1, §12) |
| W2, W3, W5 (CC-229) | carries | carried | carried (§9) |
| C1-C8 (CC-232) | carries | — | **carried (§10)** |

## 1. Model selection by N7 (A1, A2, A3) — unchanged from v1, N7 made explicit

**Fixed order** (`G_C1_record.json` `candidate_order`, closed 2026-11-02T00:27:14Z before any status):
1. Vintern-1B-v3_5
2. Vintern-1B-v2
3. Qwen2.5-VL-7B-Instruct
4. InternVL3-8B
5. aya-vision-8b
6. mblip-bloomz-7b
7. mblip-mt0-xl
8. Pangea-7B
9. centurio_aya
10. centurio_qwen

**Sets each role needs:**
- VI captioner: nocaps_test and openvivqa_dev.
- VI verifier (v4.1 l.276, "every registered test set"): the same two.
- `vitextcaps_test` and `viecap4h_private_test` are DEFERRED (CC-222 v1.3 §5.4) and do not block the pick.

| order | model | nocaps_test | openvivqa_dev | pick |
|---|---|---|---|---|
| 1-5 | Vintern-1B-v3_5, Vintern-1B-v2, Qwen2.5-VL-7B, InternVL3-8B, Aya-Vision-8B | UNCHECKABLE (G-C1) | UNCHECKABLE | skipped |
| **6** | **Gregor/mblip-bloomz-7b** | **CLEAN** | **CLEAN** (CC-229 Q2, web-crawl branch) | **VI captioner and VI verifier** (PI-1103b) |
| 7 | Gregor/mblip-mt0-xl | CLEAN | CLEAN | not pinned |
| 8 | neulab/Pangea-7B | UNCHECKABLE (G-C2, decided by documentation) | UNCHECKABLE | — |
| 9-10 | centurio_aya, centurio_qwen | UNCHECKABLE | UNCHECKABLE | — |
| EN | liuhaotian/llava-v1.5-7b | CLEAN | N/A | EN captioner and verifier (prereg l.457; v4.1 l.264) |

**N7 / C6, binding.** No bloomz-7b → mt0-xl swap and no Pangea route, after any Vietnamese score of any kind:
published, dev, speed-test or tier-1 (prereg §6.2; CC-222 v1.3 l.579-580; CC-232 C6).
- Pangea is barred first because it is UNCHECKABLE in G-C2; second, because it sits later in the fixed order.
- mt0-xl could enter only if bloomz-7b were removed by a registered route (a HIT, or an UNCHECKABLE through an
  amendment on new documentation, CC-222 v1.3 §5.3 (f)). A score never removes it.
- No Vintern model is pinned, so O_B keeps its tier-2 role (prereg l.367).

### A1 / A2 — `Gregor/mblip-bloomz-7b` (VI captioner = VI verifier)

| field | value | source |
|---|---|---|
| revision | `4d95b91d56fcdce86504c951a28f016b15e219a1` | HF API `sha`. Read 2026-11-02T15:24:28Z and again 23:55:01Z: identical. Equals G-C1 S12. |
| `model-00001-of-00002.safetensors` | LFS sha256 `44be39143faaddf0b43e45f61f1d15a2804f0397e542e3c87b922a11b91a4c16`, 9,922,998,656 B | tree API at the revision; the response body is byte-identical at both reads (8dd1fdde) |
| `model-00002-of-00002.safetensors` | LFS sha256 `19dcdb305a64144c84cb9f924cf760e4577f7c4233d37048e63f89df5f9e95d6`, 8,592,229,664 B | same |
| `tokenizer.json` | LFS sha256 `17a208233d2ee8d8c83b23bc214df737c44806a1919f444e89b31e586cd956ba`, 14,500,471 B | same |
| `config.json` | raw sha256 `39cac8ff4edd7c57f6514e105fede0d42d939ac7b40bf795a91646d23bc7b7a9` (7,169 B); git-blob SHA-1 b56aa3de… | raw at the revision (v1, 15:42:20Z) |
| other non-LFS files (git-blob SHA-1) | `preprocessor_config.json` 0b0fa393…, `model.safetensors.index.json` 9465df3c…, `special_tokens_map.json` fdafe480…, `tokenizer_config.json` 612d97d5… | tree API |
| loader | `transformers` `Blip2ForConditionalGeneration` / `Blip2Processor`, loading safetensors only | card S12 |
| web-scale pretraining | "unknown (disclosed)"; Web CapFilt (CC3M + CC12M + SBU) | `G_C2_record.json` |
| `n_flickr_host_unparsed` (PI risk control (1)) | 0 (`mblip_capfilt_raw`: 128,759 static-host hits) and 0 in both mixes | committed scan records |

**Load-time check, binding on `c_pvr_job.sh`:** each safetensors shard, `tokenizer.json` and `config.json` is checked
against this table. Any mismatch is a FAULT, and nothing is decoded.

### A3 — `liuhaotian/llava-v1.5-7b` (EN captioner and verifier, S1-S5)

| field | value |
|---|---|
| revision | `4481d270cc22fd5c4d1bb5df129622006ccd9234` (re-read 23:55:01Z, identical) |
| `pytorch_model-00001-of-00002.bin` | LFS `492fdfa63cf314097d99da81a3586d54a97adc1471a0ae0535f5caa269b86314`, 9,976,634,558 B |
| `pytorch_model-00002-of-00002.bin` | LFS `c0eb94eb3fa578a4c63567f2eca6b0acf6a44a891c257aca0df88ffa891de72e`, 3,542,276,251 B |
| `mm_projector.bin` | LFS `be33a3b477e091832a3c8a9fabf5769c43b4cb2c161fc8c464b7bb214f16143a` |
| `tokenizer.model` | LFS `9e556afd44213b6bd1be2b850ebbbd98f5481437a8021afaf58ee7fb1818d347` |
| `config.json` | raw sha256 `f112de882e31171a105f0d3f69d9e6e8700a40149f0944f4b507d3a41789e492`; `mm_vision_tower` `openai/clip-vit-large-patch14-336` @ `ce19dc912ca5cd21c8a653c79e251e808ccabcd1` |
| still OPEN-minor | CLIP tower weight sha; LLaVA inference-code commit (§11) |
| Flickr matches | none |

## 2. A4 — Prompts

### 2.1 Captioner prompt: DRAFTED [proposal], pinned by text sha

**Instruction language: English, naming the target language (CC-232 C4).** The reasons are fixed before any output:
- (i) This is the exact evaluation template behind mBLIP's published XM3600 numbers: "Caption in $LANGUAGE:" (S15
  Table 8).
- (ii) mBLIP §3 ("Output Language") controls output language by combining English prompts that explicitly name the
  target language with translated instructions.
- (iii) The card expects the best results with high-resource-language prompts.
- (iv) App. B reports output-language drift for some non-English prompts.

A Vietnamese-language instruction has no documented anchor for this model. The Vietnamese output is guarded by guard G
(VI-script share ≥ 0.95, prereg §5.7(b)), which is reported for every arm.

**Templates.** Each is UTF-8, LF line ends, no trailing newline. The sha256 is of the exact bytes. `{demos}` is the
demonstration block; `{i}` and `{caption}` fill one demonstration line.

| file (to be created as `scripts/c_pvr/prompts/<name>`) | exact text | sha256 |
|---|---|---|
| `cap_vi_0.txt` (A0; VI zero-shot) | `Caption in Vietnamese:` | `f6e05b0b7510a1bf5c8a00b203a81f077f28bd5b59a5fc25d5afeead9e618feb` |
| `cap_vi_k.txt` (VI k-shot: A1-A4, A6, A7, A12, PVR-drop, PVR-keep) | `Captions of similar images:⏎{demos}⏎Caption in Vietnamese:` | `2653672de35c932dc2b3a088053dd7965a679eabb12f4cf4a363a89d31f9c42d` |
| `demo_line.txt` | `{i}. {caption}` | `c068abccda584d10e3cf1e56b053fe6d107487b9276b9153608b57c4994af128` |
| `cap_en_0.txt` (S4 = A0, EN) | `Write a one-sentence caption for this image in English.` | `40791b9bdb05d3d81efaeae36e339fa8b10e2d9124f88302a145cb1bb0c1f335` |
| `cap_en_k.txt` (S1, S3, S5, EN) | `Captions of similar images:⏎{demos}⏎Write a one-sentence caption for this image in English.` | `3fcd627787f90e8eaaff9aad6f8dfb2b74978427fcdba967a4e3e62c903143cb` |

(⏎ marks a single LF, byte 0x0A.) These templates were written in the scratchpad and hashed with `sha256sum`. No
template has been run on any model or data. The sha256 values are binding only once the files exist under
`scripts/c_pvr/prompts/` byte-equal and the PINS-A read accepts them.

**Rendering rules (fixed now, for every arm and both languages):**
1. **k = 4.** The demonstration block is up to 4 lines, `demo_line.txt` joined by a single LF, with `{i}` = 1..n.
2. **Order.** A1, PVR-drop, PVR-keep, A6, A7 and A12 keep the retrieval rank: rank 1 (most similar) first, numbered 1.
   A2 (random-k) keeps its draw order. A3 (sample-k in top-7) keeps its sample order.
   - Recorded so it is not mistaken for evidence: no document shows how zero-shot mBLIP weighs demonstration position.
3. **Emptied demonstrations.** A demonstration emptied by span deletion is **dropped, never back-filled** (prereg
   §6.4). The remaining lines are renumbered 1..n with n < 4. If n = 0, the arm uses `cap_vi_0.txt` for that image,
   and the event is counted per arm.
4. **Demonstration text.** NFC, then the fixed whitespace/punctuation table of prereg §6.4: newlines and runs of
   whitespace collapse to one space, and the text is trimmed. Nothing else changes (no case change, no translation).
5. **EN arms (LLaVA).** The rendered text is placed in the LLaVA-1.5 conversation template, with the image token
   before the text. The conversation mode is pinned with the LLaVA code commit (OPEN-minor, §11).
6. **C3, recorded:** no document shows zero-shot mBLIP using retrieved captions in the prompt. CONCAP and PAELLA train
   for it; mBLIP's paper does not test it. Whether the k = 4 block is used at all is learned only from the tier-1
   A1 − A0 contrast on XM3600-vi dev. That contrast is reported, not gated, except through the registered headroom
   STOP.

### 2.2 Verifier form: the v4.1 l.276 / prereg §6.1 / `verify.py` conflict — ranked options

**The conflict.**
- C_DIRECTION v4.1 l.276 says the verifier runs with "đúng prompt 3 nhãn của FAIR" (FAIR's exact 3-label prompt).
- The registered prereg §6.1 (l.449-452) says: FAIR's 3-label scheme (SUPPORTED / UNCERTAIN / REJECTED,
  `rescap/metrics_svp.py` l.51), a label-generating prompt, label parsing, greedy decoding, **no scalar threshold**.
- No single label-generating 3-label prompt exists in `rescap/`. FAIR's verifier, `rescap/pipeline/verify.py`
  (e1ce1682, commit 07fd1d5), derives the 3 labels from Vietnamese yes/no probes (`probe_yes_no`,
  `rescap/vlm/base.py` l.323, e8fee5bc, "Chỉ trả lời 'có' hoặc 'không'"), a stricter re-ask, a negation probe and C/S
  `Thresholds` (verify.py l.20, l.295-315).
- So the three sources cannot all hold. Each option below overrides one of them explicitly. Precedence: a registered
  prereg line governs over a direction-document line (prereg §13 practice: v4.1 lines are overridden by stated rows).

| rank | option | what it overrides | for | against |
|---|---|---|---|---|
| **V1 — Recommended; Default** | A label-generating 3-way prompt `ver_3way.txt` (below). It keeps FAIR's 3-label scheme (`VERDICTS`), greedy, no threshold. It is mBLIP's own documented 3-way template (S15 Table 8, XVNLI), with `{proposition}` in place of `$HYPOTHESIS`. | v4.1 l.276's word "exact FAIR prompt" (a direction-doc line), with the reason: no such prompt exists, so the line cannot be met. **Satisfies the registered prereg §6.1 as written.** | the registered text wins; one greedy call per proposition (cheap; fits the per-image cap); the format the model was evaluated in; gives UNCERTAIN a direct route ("maybe") | mBLIP "fails to predict the neutral class" zero-shot (S15 §4.3), so UNCERTAIN may be rare (C2: reported, never hidden); the proposition is Vietnamese while the answer is requested in English (as in mBLIP's own XVNLI use, where the hypotheses were non-English) |
| V2 | FAIR's `verify.py` probe pipeline as "FAIR's 3-label scheme": Vietnamese yes/no probe, stricter re-ask, negation probe and `Thresholds`, with `probe_k = 1` (greedy) and the thresholds pinned by value | **registered prereg §6.1** ("no scalar threshold"), which needs a stated override in this amendment | the closest to "FAIR's" verifier in code; the negation probe guards against yes-bias (C7) | overrides a registered line; FAIR's thresholds were tuned for other backbones (Vintern / Qwen), not mBLIP; with `probe_k = 1` the C/S thresholds act on a single-sample "confidence"; 2-3 calls per proposition (cap pressure); Vietnamese yes/no prompts meet the output-language drift of App. B |
| V3 | A Vietnamese 3-way prompt, e.g. `"{proposition}" có đúng với bức ảnh không? Trả lời: có, không, hoặc không chắc.` | v4.1 l.276 (as V1) | matches the caption language | no documented anchor for mBLIP; translated label words; the output-language risk falls on the label itself; the parser must handle Vietnamese label variants |

**V1 template:**

| file | exact text | sha256 |
|---|---|---|
| `ver_3way.txt` (VI verifier; also the EN verifier for S1/S2, for parity) | `Is it guaranteed true that "{proposition}"? Yes, no, or maybe? Answer in English:` | `bcb9230851622e5d9afa98f0765bf2bffd05b4b4ba37aa8bd0508d300881313d` |

For LLaVA (S1, S2), the same text sits in the LLaVA conversation template.

### 2.3 Mapping, parser and reporting (C2, C7): DRAFTED [proposal]

- **Mapping** (from S15 Table 8: entailment → yes, contradiction → no, neutral → maybe): `yes` → SUPPORTED; `maybe`
  → UNCERTAIN; `no` → REJECTED.
- **Parser** (one function, `c_pvr.py parse_label`):
  1. Take the decoded answer.
  2. Apply NFC and casefold.
  3. Take the first maximal run of ASCII letters `[a-z]+`.
  4. Map `yes`, `no` or `maybe` as above.
  5. Anything else is UNCERTAIN and also counted as a **parse failure**. That covers empty output, other words and
     Vietnamese "có"/"không" (prereg §6.3: "Parse failures, empty or off-set answers = UNCERTAIN").
  - There is no fuzzy matching and no second call.
- **Reported for every arm that calls the verifier (PVR-drop, PVR-keep, A8, and S1/S2 in EN), per set and per tier.**
  All are descriptive, never a gate:
  - **UNCERTAIN share** = UNCERTAIN / all verifier answers, split into "maybe" and "parse failure" (C2; prereg §6.3);
  - **yes share** = SUPPORTED / all verifier answers. It is printed beside every PVR − A6 and PVR − A7 contrast (C7).
    Like POPE's yes share (S15 Table 4), it reads yes-bias, and it is not a new gate;
  - the per-image verifier-call cap hits (§2.6).
- **C1, binding wording:** no PINS, report or paper text may imply a validated Vietnamese verifier. There is no
  published Vietnamese verification or VQA number for mBLIP. The record says "verifier: mBLIP-bloomz-7b, Vietnamese
  verification ability not documented".

### 2.4 A8 needs no prompt of its own

A8 is "post-hoc correction with the same verifier, same prompt and same per-image verifier-call cap" (prereg §5.1
l.383), and its correction is the shared span deletion (prereg §6.4: "shared by PVR, A6, A7 and A8's output deletion").
- A8 = the A1 caption (A1 is the uncorrected same-k caption, prereg §5.1 [proposal for the read: A8 corrects the A1
  output]), decomposed by the same decomposer.
- Each proposition is verified with `ver_3way.txt` under the same cap.
- Spans are deleted with the same rule as the chosen UNCERTAIN variant: drop deletes REJECTED and UNCERTAIN spans;
  keep deletes REJECTED spans only.
- No regeneration prompt. This keeps "same prompt" literal.
- **Open for the read:** whether A8 corrects the A1 caption or the A0 caption. Recommended: A1, since it isolates the
  input-side position, which is the NB-NOVELTY claim (prereg §1.3). Default: A1.

### 2.5 `max_new_tokens`: [proposal] with sources

| call | value | source |
|---|---|---|
| captions (VI and EN, every arm) | **64** | XM3600-vi references average **18.0 words, 79.3 characters** per caption (Thapliyal et al. 2022, arXiv 2205.12522v2, **Table 1**; archived `8e7925415a106d58_2205.12522v2.txt`). mBLIP trained with a maximum target length of 128 (S15 App. A); CONCAP decoded mBLIP with at most 25 tokens (2507.20411v1 §4.1), shorter than a mean Vietnamese caption is likely to need under the BLOOM tokenizer [est.]. 64 is ≥ 3.5 × the mean word count, so truncation should be rare. **Truncation share (`finish` at the cap) is reported per arm**, descriptive. |
| verifier (`ver_3way.txt`) | **8** | the house yes/no probe uses `max_new_tokens=8` (`rescap/vlm/base.py` l.324-325); one label word is needed |

### 2.6 Per-image verifier-call cap: [proposal]

- The prereg requires "the same per-image verifier-call cap" for PVR and A8 (l.383), but registers no value.
- **Proposal: 32 calls per image** [est.]:
  - PVR verifies the propositions of up to 4 demonstrations. At ≈ 18 words per caption (Table 1 above), that is an
    assumed 4-8 propositions each, so 16-32 calls.
  - A8 verifies one caption and rarely reaches 32.
- **Overflow rule:** propositions beyond the cap, taken in order (demonstration 1 first, then left to right), get
  UNCERTAIN unverified. They are counted per arm (`cap_hits`), never re-tried.
- The cap is the same for every verifying arm. Its value is fixed before the speed test, because the speed test
  projects P1 under this cap.

### 2.7 Helper prompts of the cut-first arms: OPEN

| arm | what is missing | note |
|---|---|---|
| A5 LMCap | its text-only LM prompt and its model (LMCap uses `facebook/xglm-2.9B`, LMCap text) | **OPEN**; also needs a model pin; second in the §5.1 cut order |
| A9 ITM/ARA re-ranking | an image-text matching scorer: mBLIP has no ITM head; a candidate is the encoder of A9 itself, e.g. NB-ENC SigLIP2 | **OPEN** (scorer choice); third in the cut order |
| A10 RA-CoA re-derivation | a re-derivation prompt | **OPEN**; first in the cut order |
| A11 foreign-text deletion | no prompt: it is the §4.4 extractor plus deletion | covered by §4.4 |
| A4 NES CLIP filter (< 0.2) | a CLIP scorer pin | **OPEN-minor** (NB-ENC SigLIP2 is not CLIP; the read must name the scorer) |

These arms may be cut by the §5.1 order if the projection exceeds the cap. Each still needs its pin before the first
output if kept.

## 3. A5 — k and decoding: FILLED

| item | value | source |
|---|---|---|
| demonstrations | **k = 4** | prereg §5.1 l.385, §0 l.148 |
| decoding | **greedy** (no sampling, beam 1), every arm and every model | prereg §5.1 l.385, §6.1 |
| order and format | §2.1 | this draft [proposal] |

**C5, binding wording:** 54.29 is never cited as C's expected performance. Any mention reads "published, beam 5"
(S15 §4.1); C decodes greedy.

## 4. Code and files still to be written (A6, A7, A8, A11), owners and tests

**Owner for every code file:** a C code-drafter agent assigned by the coordinator. Ken is unavailable (house rule), and
the ≤ 3 background-agent limit applies. Review is the PINS-A one-judge read, then the gatekeeper commit. No GPU and no
model are needed for any item below. All of them run on the laptop CPU under `python3 -I`.

### 4.1 File list

| file | content | pinned by | blocks |
|---|---|---|---|
| `scripts/c_pvr/c_pvr.py` | the subcommands of prereg §11: `ovqa-pin` (§5), `parity`, `owners`, `lists`, `w25`, `render` (prompts §2.1), `decompose`, `parse_label` (§2.3), `filter` (span deletion §6.4), `score`, `proxy`. It asserts `OI_TEST_URL` byte-equal to `gates.py` l.66, the PINS shas at start, and `RESCAP_RAW_TONE` unset. It refuses `oidv7-*-annotations*`, `/dev/shm/c_pvr_gb/` and `nocaps_val_4500_captions.json` paths. | sha256 in SHA256SUMS | A11, every later step |
| `scripts/c_pvr/prompts/*.txt` | the 6 templates of §2.1 and §2.2, byte-equal to the shas there | the shas in §2.1 and §2.2 | A4 |
| `scripts/c_pvr/decompose_vi.py`, `decompose_en.py` (or functions inside `c_pvr.py`) | deterministic proposition rules on top of the segmenter or parser of §4.2: one proposition per mapped object mention with its attached attribute, count or relation, and scene-text propositions (prereg §1.3) | sha256 | A6 |
| `scripts/c_pvr/en_lexicon.json`, `scripts/c_pvr/build_en_map.py`, `scripts/c_pvr/en_oiv7_map.json` | §4.3 | three shas, frozen before G-B | A7 |
| `scripts/c_pvr/proxy_regex.txt`, extractor and normaliser (in `c_pvr.py` or `proxy.py`) | v3 §7 items 1-6 exactly | shas before the first tier-1 output | A8 |
| `scripts/c_pvr/requirements_c_pvr.lock` | exact versions and wheel sha256 for `rapidfuzz`, `transformers`, `torch`, `accelerate`, `pillow`, the VnCoreNLP wrapper and the EN parser package and model; one lock per host (laptop scoring, GPU decode) | sha256 | A6, A8, A1/A3 minor |
| `scripts/c_pvr/c_pvr_job.sh` | the GPU job of prereg §11 (`--selftest`, `speed`, `tier1`), the load-time checks of §1, and the tenancy rules | sha256 | GPU block (after Q11) |
| `scripts/c_pvr/test_c_pvr.py` (or `c_pvr.py selftest`) and `scripts/c_pvr/c_pvr_mutants.py` | §4.5 | shas in SHA256SUMS | the read |

### 4.2 Decomposers (A6): option for the read

| role | Recommended = Default [proposal] | alternative | why |
|---|---|---|---|
| VI word segmenter | **VnCoreNLP-1.2 RDRSegmenter** (`wseg`), jar sha256 `9e2811cdbc2ddfc71d04be5dc36e185c88dcd1ad4d5d69e4ff2e1369dccf7793` (the house B protocol pin, `scripts/b2_external/b2.py` l.1084; re-hashed on the run host; needs a JDK) | `pyvi` 0.1.1 (installed on the laptop; a trained CRF, so it needs an explicit acceptance against prereg §6.2's "rule-based") | RDRSegmenter is rule-based (Ripple-Down Rules), deterministic and already house-pinned |
| VI object mentions | `rescap/chair.py objects_in(raw_tone=False)` (e47d249a) on the 69 classes of `vi_oiv7_map.json` (27f2b1ca) | — | the same instrument as the outcome (prereg §3.1), so the propositions that are filtered and the mentions that are scored agree |
| EN parser | a spaCy dependency parse with a pinned small English model, exact versions plus wheel shas in the lock | a rule-only chunker (no parse) | prereg §6.2 names an "EN dependency parse"; inference is deterministic. **The exact version is not chosen here.** |

The decomposer sees no image, so there is no contamination by construction (v4.1 l.264 table).

### 4.3 EN class map (A7): build plan; not built now

- **Why it is not built now.** The instructions allow a small data file only if it can be built deterministically
  from inputs that are already pinned. The EN map cannot: it needs an English mention lexicon (surface forms, plurals,
  synonyms → class), and none is pinned. Building one now would be a choice, not a derivation.
- **Plan.**
  1. `en_lexicon.json` is written by the code drafter. It holds one entry per VI class key of `vi_oiv7_map.json` (69),
     with the English surface forms of that class. The source is the OI display names in
     `oidv7-class-descriptions.csv` (84a4373a), plus their regular plurals and a short hand list.
  2. `build_en_map.py` copies each class's `pos` / `neg` OI display-name lists **unchanged** from `vi_oiv7_map.json`.
     Only the mention side is English.
  3. Output `en_oiv7_map.json`, sorted keys, fixed separators.
  4. All three shas are frozen before G-B and never amended after (prereg §3.4).
- **Selftest:** the 69 keys equal the VI map's 69; every `pos`/`neg` list is byte-equal to the VI map's; every surface
  form is unique across classes.
- P_obj^EN stays descriptive, never a gate.

### 4.4 Scene-text proxy (A8): build plan

The spec is fixed in C_DIRECTION v3 §7 items 1-6 and v4.1 §7 item 7:
- **regex list:** applied to question text only; the phrase classes are given in v3 §7.1;
- **extractor:** quoted spans, spans after cue words, all-caps or digit tokens (v3 §7.2); A11 uses the same extractor;
- **normaliser:** NFC → casefold → strip punctuation, keep letters and digits → collapse whitespace, **keep Vietnamese
  diacritics** in the main rule (v3 §7.3);
- **match classes:** match / near / uncovered (v3 §7.4, ≥ 3-character rule). Near uses
  `rapidfuzz.distance.Levenshtein.normalized_similarity` ≥ 0.5 (v3 §7.4);
- **weights:** w = 1 and w = 0 (v3 §7.5);
- **guard:** R_text (v3 §7.6);
- SESOI_T = 2.0 and δ_RT = 2.0 (prereg §6.4).

What remains is code plus the literal regex file. The examples in v3 §7.1 end with "…", so the full list is a drafting
choice. It must be written and sha-pinned before the first tier-1 output, and is never tuned after. `rapidfuzz` is
pinned in the laptop lock (§4.1); the version is chosen at install, and none is installed today.

### 4.5 Selftest and mutant plan (house pattern: `gates.py selftest` and `gates_mutants.py`, CC-226r3 101/101)

- **Selftest** (`python3 -I scripts/c_pvr/c_pvr.py selftest`): stdlib plus the pinned lock only; no weights, no data;
  sockets raise (prereg §11 l.746). Fixtures are synthetic sentences written for the test. No dataset caption,
  question or answer is used.
- Checks:
  1. each prompt file's sha equals §2.1 / §2.2;
  2. `render` with 4, 3 and 0 demonstrations (n = 0 falls back to `cap_vi_0.txt`), the whitespace table and the
     renumbering;
  3. `parse_label` on `Yes`, `yes.`, ` Maybe,`, `No`, the empty string, `Có`, `không` and `yesno`, with the expected
     labels and parse-failure flags;
  4. span deletion: an emptied demonstration is dropped and not back-filled;
  5. the cap overflow order;
  6. the VI decomposer on fixture sentences (expected propositions), and the EN decomposer likewise;
  7. the EN-map invariants (§4.3);
  8. the extractor and normaliser (diacritics kept), the ≥ 3-character rule, the near threshold 0.5 against a stdlib
     reference Levenshtein, and the w = 1 / 0 arithmetic;
  9. `OI_TEST_URL` equal to `gates.py` l.66;
  10. the git-blob SHA-1 function against git's known vector for the empty blob (`e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`);
  11. the refusals (annotation CSVs, `/dev/shm/c_pvr_gb/`, `nocaps_val_4500_captions.json`);
  12. `RESCAP_RAW_TONE` set → FAULT;
  13. the 1,070 / 3,545 assertion on a synthetic json.
- **Mutants** (`c_pvr_mutants.py`, one rule flipped each; every mutant must be killed, or proved equivalent in writing):
  - maybe → SUPPORTED;
  - a parse failure → SUPPORTED;
  - first-word parse → last word;
  - demonstration order reversed;
  - back-fill of emptied demonstrations;
  - n = 0 keeps the k-shot template;
  - cap 32 → 33, and the overflow order reversed;
  - diacritics stripped in the main rule;
  - NFC removed;
  - ≥ 3 → ≥ 2;
  - near threshold 0.5 → 0.4;
  - w default flipped;
  - `OI_TEST_URL` one character changed;
  - the SHA-1 blob header dropped;
  - count asserts off by one;
  - a refusal removed;
  - the EN map with one `pos` list altered.
- **Read:** the PINS-A one-judge read sees the selftest output and the mutant table. The gatekeeper commits the files
  byte-equal with SHA256SUMS.

## 5. A10 — OpenViVQA (NB-OVQA, prereg §4.3, §8.1)

**Pinned now (unchanged from v1; re-read 2026-11-02T23:55:04Z, tree body byte-identical, 6c2be14e):** revision
`cc85c24c863afb05b5a52f68950f9ba6b69975cf`, with:

| file | size (B) | hub id |
|---|---|---|
| `dev-images.zip` | 165,039,269 | LFS sha256 `ff6a0e878bd0718425b3bf7e0455322111dc6e1ea2410cfd3eb7703216580f06` |
| `test-images.zip` | 152,452,885 | LFS sha256 `e0ea3a805731376c31c517abd114f2dca6d52f193444e9eaa6cb2513f9d957bf` |
| `train-images.zip` | 1,337,946,616 | LFS sha256 `b01ba9365acf041042ee6a5f4c4acef98b7abfec2d673aa1b7b40bb8d5a40ba7` |
| `vlsp2023_dev_data.json` | 762,438 | git-blob SHA-1 `415ddd8b6fbb01f2c5d9b8fa0b2554fd9149992d` |
| `vlsp2023_test_data.json` | 2,500,527 | git-blob SHA-1 `0ae3f6982b42391a985d9b5fe454ab482aa5bb4d` |
| `vlsp2023_train_data.json` | 6,596,293 | git-blob SHA-1 `dae982c1463f49708c976d5de4dae453cd5eb266` |

**How `c_pvr.py ovqa-pin` computes the three json sha256 values.** It runs after the PINS-A GO, on the laptop, with no
token (the dataset is public).

1. For each of the 3 files: `curl -sS --fail -A vsps-research -o ~/.vsps_sealed/c_pvr/ovqa/<name>.part
   'https://huggingface.co/datasets/uitnlp/OpenViVQA-dataset/resolve/cc85c24c863afb05b5a52f68950f9ba6b69975cf/<name>'`.
   - The directory is mode 0700 on WSL ext4, never under `/mnt/d`, `data/`, the repo or a backup path (prereg §4.3,
     NB-OVQALOST).
   - The URL carries the pinned revision, never `main`.
2. One pass over the bytes computes three things: the **sha256**; the **git-blob SHA-1** = sha1(`b"blob %d\0" % size`
   + bytes); and the size.
   - The size must equal the table above, and the SHA-1 must equal the hub's blob id. That cross-check ties the
     downloaded bytes to revision cc85c24c without trusting the transport.
   - Any mismatch is a **FAULT**: the `.part` file is unlinked and logged, and the proxy is not run.
   - On a match, the file is renamed into place and set to mode 0400.
3. The three sha256 values, sizes, SHA-1 results and the revision go into `~/.vsps_sealed/c_pvr/ovqa/ovqa_pin.json`
   and a gatekeeper LOG line. Each read is logged in `~/.vsps_sealed/c_pvr/ACCESS_LOG.tsv`.

**Dev-set identity assertion (keys and lengths only; no question or answer string is read, printed or stored).** The
schema is not yet known: no json has been opened under C's custody. So the assertion has two fixed steps.
1. **Skeleton.** For each file, print the key skeleton only: key names, value types, and container lengths, to depth 2,
   with no string values. This is allowed by §4.3, "a read of keys and lengths only".
2. **Counting rule.** The coordinator writes it into a LOG line **before** any count is computed. It names which
   container holds images and which holds QA, from the skeleton alone. Then:
   - (a) **the file named `vlsp2023_dev_data.json` at the pinned revision must give 1,070 distinct images and 3,545 QA
     items** (C_TEST l.28; prereg §4.3);
   - (b) recommended: also `train` = 9,129 / 30,833 and `test` = 1,000 / 14,035 (C_TEST l.28), lengths only. This ties
     each file name to its split; a swapped or re-split file fails;
   - (c) the dev json's image file-name field (the only string field allowed, for the §8 fetch list) must name only
     members of `dev-images.zip`. The zip's LFS sha256 must equal ff6a0e87 before its central directory is listed (no
     image decoded).

Any mismatch is a FAULT, and the proxy is not run. **That `vlsp2023_dev_data.json` is OpenViVQA dev is not a fact until
(a)-(c) pass.**

## 6. A11 — `OI_TEST_URL` and `c_pvr.py`

- `OI_TEST_URL = "https://open-images-dataset.s3.amazonaws.com/test/{file}"` (`gates.py` l.66, bf4d5f64; CC-222 v1.3
  §8). FILLED.
- `c_pvr.py` sha256: **OPEN** until the file is written (§4.1) and read. Its selftest asserts byte-equality of the URL.

## 7. A12 — Parity inputs (NB-PARITY): FILLED, unchanged from v1 §10

Re-hashed at v1 drafting, all equal to prereg §2.3:

| file | sha256 (first 8 hex) |
|---|---|
| `xm3600-train-annotations-human-imagelabels.csv` | 779afb19 |
| `xm3600-val-annotations-human-imagelabels.csv` | b7967190 |
| `xm3600-test-annotations-human-imagelabels.csv` | 06567dd9 |
| `oidv7-class-descriptions.csv` | 84a4373a |
| `fetch.sh` | 75c22a08 |
| `full-train.md5` | e1af6821 |
| `full-val.md5` | 5770ed7c |
| `full-test.md5` | 2eebd937 |
| `manifest.json` | 263015f9 |
| `vi_oiv7_map.json` | 27f2b1ca |
| `chair.py` | e47d249a |
| `lexicon.py` | fbc945f2 |

Full values are in v1 §10 and prereg §2.3. They were not re-hashed in v1.1, to keep the load on `/mnt/d` light (EIO
mitigation); the PINS-A read re-hashes them.

## 8. A13 — NB-CAP: unchanged from v1 §11

- cap = min(⌈1.25 × P1⌉, 37) GPU-h, one re-base for M1 (Q-cost YES, PI-1102a). This is ≤ 37 GPU-h ≈ ≤ 343k VND at
  9,282 VND/h (cap ≤ 350k, prereg §10).
- P1 stays OPEN until the speed test.
- The host question is now asked as Q-P1 (§12).

## 9. CC-229 carries: W2 and W3 unchanged from v1 §12-13; W5 added

- **W2, internal only** (it contains overlap wording, so never in the paper; PI-1101o). Verbatim:
  > "openvivqa_dev: OpenViVQA images are a Google Images web scrape (arXiv 2305.04183 §3.2.1); web-crawl overlap unknown, disclosed"

  Paper-facing sentence (CC-222 v1.3 §5.4 l.561-562, verbatim):
  > "CLEAN on the Vietnamese sets rests on the published training-data documentation and a name check of the released training lists; web-crawled components are unknown."
- **W3:** the Flickr exclusion union for the pinned set {bloomz-7b; llava-v1.5-7b} is **4 images** (`513d6796c322ced5`,
  `821f75f1f4061c79`, `bfdd3df591001b36`, `c32ddd2ae971e5b5`; LLaVA has none). They leave P_obj^VI, R_obj^VI and the
  proxy at every tier, count only. The drop in n_e_power is **OPEN, ≤ 4**, until G-B, and is printed beside the
  W25-flagged and lost counts.
- **W5 (process):** every runner done-line prints rc from the pipeline (`set -o pipefail`). The gatekeeper refuses a
  done line with an empty rc. This applies to `ovqa-pin`, `parity`, `lists`, `w25` and the GPU job.

## 10. CC-232 carries C1-C8 (binding on PINS-A, the tier-1 report and the paper)

| # | carry | where satisfied |
|---|---|---|
| C1 | no wording may imply a validated Vietnamese verifier | §2.3 (C1 wording) |
| C2 | the yes/maybe/no mapping is pinned before the first output; the UNCERTAIN share is always reported for PVR and A8; the verifier-form conflict is resolved by a stated override | §2.2 (V1 / V2 / V3; the override is named), §2.3 |
| C3 | the k = 4 format, language and order are pinned; the record states that zero-shot mBLIP ICL is undocumented | §2.1 rules 1-6 |
| C4 | the instruction language is pinned, with the reason given before outputs | §2.1 (English instruction naming Vietnamese; reasons i-iv) |
| C5 | 54.29 is never C's expected performance; it is cited as "published, beam 5" | §3 |
| C6 | N7: no mt0-xl swap and no Pangea route after any score | §1 |
| C7 | the yes / SUPPORTED share is printed beside every PVR − A6/A7 contrast (descriptive) | §2.3 |
| C8 | the CC-229 W2, W3 and W5 carries | §9 |

Also carried from PI-1103b / CC-232 W1: the pivot criterion on record is "post hoc, documentation-only, not a
registered gate". The 33.6 bar is never used as a gate on C's outputs.

## 11. Remaining OPEN rows and owners

| row | why open | owner | closed by |
|---|---|---|---|
| A4 verifier form | V1 / V2 / V3 choice (§2.2) | PINS-A one judge (with the PI only if V2 is chosen, since V2 overrides a registered line) | the ruling names the option and the override |
| A4 prompt files | not yet in the repo; the text and shas are drafted (§2.1, §2.2) | C code drafter | files byte-equal to the shas, then the read |
| A4 cut-first arm helpers (A5, A9, A10; the A4 scorer) | model or scorer and prompt not chosen | C code drafter → the read; or cut by the §5.1 order | pins, or a recorded cut |
| A4' `max_new_tokens` 64 / 8; verifier-call cap 32 | proposals | PINS-A one judge | ruling |
| A8 input caption (A1 vs A0) | proposal: A1 | PINS-A one judge | ruling |
| A6 VI segmenter (VnCoreNLP jar vs `pyvi`) | choice, and the jar is not on the laptop | PINS-A one judge; the coordinator installs the jar and JDK on the run host | ruling, plus the jar re-hash on the host |
| A6 EN parser and version | not installed; version not chosen | C code drafter (lock file) | lock with wheel shas |
| A6 decomposer code | not written | C code drafter | file sha + selftest + mutants |
| A7 `en_lexicon.json`, `build_en_map.py`, `en_oiv7_map.json` | the lexicon is a choice, not derivable (§4.3) | C code drafter | three shas, frozen before G-B |
| A8 proxy regex file, extractor, normaliser | code; the regex list is literal text to write | C code drafter | shas before the first tier-1 output |
| A8 `rapidfuzz` version | not installed | C code drafter (laptop lock) | exact version + wheel sha |
| A10 3 json sha256 values; dev identity | download belongs to `ovqa-pin` custody | coordinator runs `c_pvr.py ovqa-pin` after the PINS-A GO | `ovqa_pin.json` + LOG line; (a)-(c) pass |
| A11 `c_pvr.py` sha256 | not written | C code drafter | SHA256SUMS + read |
| A13 P1 | needs the speed test (after Q11) | coordinator (GPU block) | speed-test LOG line |
| W3 n_e_power drop (≤ 4) | needs G-B | G-B run | `gb_counts.json` |
| A1/A3 minor: `transformers` / `torch` / LLaVA-code versions; CLIP tower weight sha | not chosen / not fetched | C code drafter (GPU lock); coordinator (metadata) | lock + one tree-API read |

## 12. Questions (each with a recommendation and a default)

**For the PINS-A one-judge read:**

| # | question | recommended | default |
|---|---|---|---|
| J-V | Verifier form (§2.2) | **V1** (mBLIP 3-way label prompt; overrides only v4.1 l.276; satisfies the registered §6.1) | V1 |
| J-L | Instruction language for VI captions | English instruction naming Vietnamese ("Caption in Vietnamese:", the published template) | same |
| J-O | Demonstration order | rank 1 first (retrieval order) | same |
| J-T | `max_new_tokens` | 64 captions / 8 verifier | same |
| J-C | Per-image verifier-call cap and overflow | 32; overflow → UNCERTAIN, unverified, counted | same |
| J-A8 | A8 input caption | A1 caption | A1 |
| J-SEG | VI segmenter | VnCoreNLP-1.2 RDRSegmenter, jar 9e2811cd | same; `pyvi` 0.1.1 only with an explicit "not rule-based" acceptance |
| J-OVQA | `ovqa-pin` asserts train and test lengths too | YES (lengths only) | YES |

**For the PI** (the coordinator writes the Vietnamese):

| # | question | recommended | default |
|---|---|---|---|
| Q-P1 | Q-custody is YES, so C's tier-1 decode may run on a single-tenant rented 4090 instead of M1. The 37 GPU-h cap is an M1 money ceiling (≤ 350k VND). On a 4090 at 17,499 VND/h, the same money is ≈ 20 GPU-h [est.; 350,000 / 17,499 = 20.0]. Keep the cap as money (≤ 350k VND, restated in GPU-h by the host amendment), or as hours (37 GPU-h on any host, up to ≈ 647k VND on a 4090)? | keep it as **money** (≤ 350k VND); the host amendment restates the GPU-h | M1 and 37 GPU-h as registered; a rental only through its own amendment |
| Q-V2 | Only if the judge prefers V2: accept overriding the registered prereg §6.1 ("no scalar threshold") to use FAIR's probe-and-threshold verifier? | NO (V1 keeps the registered text) | NO |

## 13. What this draft does not change

- No registered gate, threshold, status or rule changes. `gates.py` bf4d5f64, provenance e242623f, G-C1 1f65b2ae, G-C2
  767998f8, SUMS, `PINS_A_DRAFT.md` 7161d3b2 and `C_PIVOT_CHECKPOINT_DRAFT.md` 38c7ef4a are byte-unchanged.
- One look per test set. No model was run, no prompt was tried, and no OpenViVQA, NoCaps, Objects365 or label file was
  opened.
- G-B still needs PINS-A and PINS-B committed and the Q11 ledger ruling at ≥ 92.
- No LOG line. Not committed.

## 14. Network and file touches (`date -u`)

| when (UTC) | what | result |
|---|---|---|
| 2026-11-02T23:55:01Z-23:55:04Z | GET HF API model/dataset info and `tree/<rev>?recursive=true` for bloomz-7b, llava-v1.5-7b, siglip2, OpenViVQA (public; user-agent `vsps-research`; no auth, token or e-mail) | revisions identical to v1. Tree bodies byte-identical to v1 (8dd1fdde, 8931c0e7, a3f5d9da, 6c2be14e). Info bodies: bloomz 2f4c58de, siglip2 3c3e2335, OpenViVQA e153572e (identical); llava 03fc78bb (differs from v1's d3bfa800 in non-pinned fields; the `sha` is the same). Scratch copies: `/tmp/claude-1000/-mnt-d-vsps-image-captioning/078aa393-7328-44fb-9c0d-f6e088395441/scratchpad/c_pins2/hf/`. **The coordinator should archive them by sha.** The v1 responses were lost with the wiped scratchpad. |
| 2026-11-02T23:5xZ | local | `.session_backup/2026-11-02/c_pins_evidence/` (`8e7925415a106d58_2205.12522v2.txt`, Table 1; `f7d26f6e96c993e3_2501.05122v1.pdf`, Table 41), copied to the scratchpad and read there; `CC-232.txt`; LOG l.1299; `data/xm3600/vi_oiv7_map.json` (`_note` and 3 entries: class keys and OI display names only, no label); first lines of `oidv7-class-descriptions.csv` (class names); `rescap/pipeline/verify.py` and `rescap/vlm/base.py` (code); C_DIRECTION v3 §7, v4.1 §7; C_TEST l.28 |
| scratchpad only | prompt templates written and hashed | `…/c_pins2/prompts/` (6 files, shas in §2.1 and §2.2) |
