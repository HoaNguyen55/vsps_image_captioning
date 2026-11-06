# PINS-A addendum S9: arm helpers A4, A5, A9, A10 — DRAFT v2

DRAFT v2. Not committed. Written 2026-11-06T01:10Z (`date -u`). This is an internal prereg record, not paper text.
The read is one judge at 85, reversible (PI-1103ae).

**Base and changes.** v2 replaces v1 (`PINS_A_ADDENDUM_S9_DRAFT_v1.md` f9279a63, kept unchanged as the CC-269 read
record). It closes CC-269 (NEXT_ROUND 80):
- B1, with PI-1106e;
- B2;
- N1-N10.

The change table is §11. No pin value (hub id, revision, file sha, prompt sha) changed from v1.

**What this is.** PINS-A v1.4 l.685-686 (3fb6725), as amended by T1-REP R-9 (4124ef3), names this file. It holds "the
arm helpers A4 CLIP filter and A9 ITM (never-cut, T1-REP R-1) and the cut-first helpers A5 LMCap and A10 prompt".
These are arm pins: one judge reads them, before the speed test. Plan row S9 (`C_NEXT_STEPS_2026-11-04.md` l.34).

**Naming.** In this file, A4, A5, A9 and A10 are the **prereg §5.1 arms**. They are not the PINS-A rows that share
those labels (PINS-A row A4 = prompts, A5 = k, A9 = retrieval encoder, A10 = OpenViVQA).

**Inputs** (sha256, first 8 hex):
- prereg `PREREG_DRAFT_v1_2.md` 0a2f0773 (8282874);
- `PINS_A_DRAFT_v1_4.md` 624b0804 (3fb6725), with v1.1 d8342e45 for the A1-A3 tables and the rendering rules;
- `AMENDMENT_T1_REPORTING_DRAFT_v4.md` 0e9793f3 (4124ef3);
- `AMENDMENT_T1_GUARD_DRAFT_v3.md` 9e03811c (f5c6741);
- `AMENDMENT_HOST_3090_DRAFT_v3.md` e9c04955 (5d6f5ca);
- `C_DIRECTION_v3_2026-11-01.md` l.191-208 (the arm table) and `C_NOVELTY_AND_DATA_2026-11-01.md` §1.2-1.3;
- the C-T1 precedent: `2026-10-30_c_t1/c_t1_registry.json` 09e6f90a (a03d3d2) and `scripts/c_t1/c_t1.py` 022af90e
  (l.61, l.212-223, l.416-470);
- `scripts/c_pvr/c_pvr.py` at HEAD 8f10bd60 (constants l.78-87, `proposition()` l.183, `build_props` l.342);
- `scripts/c_stage1/decode_icl.py` fa5a2511 (last commit 6129e8e) l.159-172: the code precedent for N8 (§6);
- rulings: CC-269 (`decisions/CC-269.txt`, NEXT_ROUND 80) and PI-1106e (LOG, 2026-11-06T01:06:42Z).

**What this file does not change.** No registered gate, threshold, arm list, cut order or Holm family. Prereg §5.1 as
amended by T1-REP R-1 binds:
- the cut order is A10 → A5 → A3 → A2 → A11;
- A4 and A9 are never cut;
- PVR − A4 and PVR − A9 on P_obj^VI are key secondaries.

Every value marked [proposal] is new and needs this read. Every value marked UNVERIFIED was not checked against a
primary source.

**Datastore wording (N10).** Here "D-VI" means D-VI as in host v3 l.210 ("serves the VI arms"): KTVIC train +
OpenViIC train as kept by `lists`. A4, A5, A9 and A10 are VI arms. Nothing here covers D-TC (T_A) or D-EN (S1-S5).

## 0. Summary

| arm | status (T1-REP R-1) | helper | pin | weights on GPU [est.] |
|---|---|---|---|---|
| A4 NES-style CLIP filter | **never-cut** | multilingual CLIP scorer | `laion/CLIP-ViT-H-14-frozen-xlm-roberta-large-laion5B-s13B-b90k` @ `f9ab955287d06ac45c7654f26fecd29301c70a1f` + `FacebookAI/xlm-roberta-large` @ `c23d21b0620b635a76227c604d44e43a9f0ee389` (config/tokenizer only) | 4.44 GiB fp32 |
| A9 ITM/ARA re-ranking | **never-cut** | the same scorer as A4 (Q-A9-SCORER (a), ruled in CC-269 Ruling 3; PI-1106e: no objection) | as A4 | as A4 (same pass) |
| A5 LMCap | cut-first (2nd) | text-only LM (Q-A5-GEN (a), **PI-1106e**) | `facebook/xglm-2.9B` @ `33c659ae27de09c0a54123d3902dac48cbb8592a` + template `lmcap_block_vi.txt` a1fb17d9 | 5.48 GiB fp16 |
| A10 RA-CoA-style re-derivation | cut-first (1st) | prompts on the pinned VI captioner | `Gregor/mblip-bloomz-7b` @ `4d95b91d…` (PINS-A A1/A2, unchanged) + `rederive_vi.txt` 478c5fdd + `rederive_cap_vi.txt` 93aa55e3 | none new |

Each pin above equals the committed C-T1 registry pin for the same hub id, except the two A10 prompts, which are new.
The match covers hub, revision and files. The dtype differs for M-CLIP: C-T1 used fp16, here it is fp32 [proposal]
(N2). All four revisions were still the hub head at the read (§7) and at the CC-269 re-read (00:46Z).

## 1. A4 (never-cut): NES-style CLIP filter

**Registered:** prereg §5.1 l.382, "A4 NES-style CLIP filter (< 0.2)". Direction v3 l.197 says entities whose CLIP
cosine to the image is < 0.2 are removed from the demonstrations. This is inference only.

**NES, as read in CC-269 item 6** (arxiv.org/html/2511.08909; AAAI-26; N3):
- S_sim is the raw cosine similarity, with no logit scale.
- τ_sim = 0.2. An entity is positive when its similarity exceeds τ.
- The encoder is CLIP-ViT-B/32 (implementation section). The filter step does not name a variant.
- No text template is stated for the filter. App. F uses "A photo of entity" only for zero-shot entity
  classification.

**Scorer pin.** One multilingual CLIP. The demonstrations are Vietnamese, and an English-only CLIP has no Vietnamese
text tower, so `openai/clip-vit-large-patch14-336` (LLaVA's tower) is not used. SigLIP2 (NB-ENC) is not a CLIP
(PINS-A v1.1 l.266). The chosen model is the M-CLIP of LMCap and of C-T1 (`mclip_h14`). It is already used in
`scripts/clip_score.py` (l.31).

| file at `f9ab9552…` | kind | value | bytes |
|---|---|---|---|
| `open_clip_pytorch_model.bin` | LFS sha256 | `ee81ce53c8591d48ee5e7b390b2f10d502c721df5920c3096c6bdb54d1459881` | 4,772,387,963 |
| `preprocessor_config.json` | git-blob SHA-1 | `c13c679c06519325749d1eef242ff98e2a5d2165` | 315 |
| `tokenizer.json` | git-blob SHA-1 | `463f3414782c1c9405828c9b31bfa36dda1f45c5` | 9,096,718 |

open_clip builds the text tower `xlm-roberta-large-ViT-H-14` and loads its config and tokenizer **by name** from the HF
cache. The weights come from the checkpoint above (C-T1 registry note). So the following are also pinned, at
`FacebookAI/xlm-roberta-large` @ `c23d21b0620b635a76227c604d44e43a9f0ee389`:

| file | git-blob SHA-1 | bytes |
|---|---|---|
| `config.json` | `8e5fb14e1352fd8fc678a7b293b63cfb5cf091f6` | 616 |
| `sentencepiece.bpe.model` | `db9af13bf09fd3028ca32be90d3fb66d5e470399` | 5,069,051 |
| `tokenizer.json` | `463f3414782c1c9405828c9b31bfa36dda1f45c5` | 9,096,718 |
| `tokenizer_config.json` | `34ddbd64a4cd3f2d9d8a9120d3662d0bf91baead` | 25 |

The XLM-R weight files (`model.safetensors`, `pytorch_model.bin`, …) are **not** fetched.

- **Licence:** `mit` (card tag) for both repos.
- **open_clip name:** `xlm-roberta-large-ViT-H-14`.
- **Packages:** C-T1 used `open_clip_torch==2.32.0` and `ftfy==6.3.1`. Neither is in `requirements_c_pvr.lock` (54
  lines; the GPU lock is OPEN, l.8). The GPU lock must add both, exact-pinned, with open_clip's own dependencies
  (e.g. torchvision).

**Parameters:**
- **τ = 0.2**, strict: drop when cos < 0.2; cos = 0.2 is kept. Registered.
  - NES keeps cos > τ. The two rules differ only at exact equality, and the registered text binds (CC-269 Ruling 2).
- **cos** = the dot product of the L2-normalised `encode_image` and `encode_text` outputs. Computed in **fp32**
  [proposal], because fp16 can flip pairs at the threshold. The image goes through open_clip's own preprocess for this
  model.
- **Unit** [proposal]: each `kind == "obj"` proposition that the A6 decomposer (`decompose_vi`, PINS-A §4.2) emits for
  a demonstration. Text propositions (`kind == "text"`) are left alone. NES is nouns only; scene text is A11's job.
- **Scored text** [proposal]: the object mention itself, not the whole proposition. It is the span text of the
  proposition's `mentions`, joined by one space, passed through `proposition()` (clean + quote rule).
  - No template is used. NES states no template for its filter, so a bare mention is the literal reading.
  - Departure, disclosed: the only template NES states ("A photo of entity", App. F, for classification) is not used
    (N3).
- **Deletion** [proposal]: a dropped proposition is removed by **the same span-deletion and reassembly rule as
  PVR-drop** (prereg §5.4; A6 reassembly). So PVR − A4 differs only in the keep/drop decision.
- **Demonstrations:** A1's top-4 from D-VI for the query image, in A1 order, with the §6 caption rule. A demonstration
  emptied by deletion follows the PVR-drop emptied-demonstration rule.
- **Scale note.** τ = 0.2 was set on CLIP-ViT-B/32 cosines. Here it is applied to M-CLIP H-14 with Vietnamese bare
  nouns, so its effect is UNVERIFIED (U2). The threshold is registered and is **never tuned**.
- **Degeneracy label** (N4; fixed now, before any output; descriptive only):
  - Report, per set, the share of A4 object propositions dropped.
  - If that share on XM3600-vi is **> 0.90**, A4 is labelled "near-total filter" in every table that reports
    PVR − A4.
  - If it is **< 0.05**, A4 is labelled "near-null filter" in those tables.
  - The label changes no gate, no Holm member and no τ.
- **Text length:** open_clip's tokenizer truncates at the model's context length. That length for this model is
  UNVERIFIED (U4). Mentions are short, so this matters for A9 (§3), not for A4.

## 2. A5 (cut-first, 2nd): LMCap

**Registered:** prereg §5.1 "A5 LMCap". Prereg §5 takes the arm definitions from direction v3 l.191-205. Direction v3
l.198 reads in full: "| A5 | LMCap | Theo bài gốc, ánh xạ sang captioner chung |". In English: "per the original
paper, mapped to the common captioner". PINS-A v1.1 §2.7 left the model OPEN.

**Generator: `facebook/xglm-2.9B` (Q-A5-GEN = (a), PI-1106e, 2026-11-06T01:06:42Z).** The PI decided this question,
as CC-269 B1 required.
- **Departure (B1).** A5 departs from direction v3 l.198's clause "mapped to the common captioner". A5 uses LMCap's
  own text-only generator, XGLM-2.9B, not the common captioner mBLIP.
- **Reason (B1).** LMCap's defining property is an image-blind multilingual LM prompted with retrieved captions.
  - On mBLIP, with the image visible and the same k = 4, A5 would be an A1 prompt variant: same model, same k,
    different template. It would not test that property.
  - XGLM-2.9B is the generator LMCap publishes (Ramos et al., Findings ACL 2023). It is the C-T1 pin and template
    already read under CC-172a.
  - It also costs less GPU than another mBLIP pass.
  - The PI's stated reason: it is closer to the original LMCap (PI-1106e).
- **Generator confound, stated beside every PVR − A5 contrast:** A5's generator is a 2.9B text-only LM; PVR's is the
  7B VLM mBLIP, which sees the image. So PVR − A5 mixes the demonstration treatment with the generator. It is not a
  same-generator contrast.
- **Option (b), not used, recorded:** the LMCap template on the pinned mBLIP, with the image visible.

**XGLM pin** (`33c659ae27de09c0a54123d3902dac48cbb8592a`, licence `mit`, not gated):

| file | kind | value | bytes |
|---|---|---|---|
| `pytorch_model.bin` | LFS sha256 | `9aa29d6635e7936bdd020bd8dab855ba8e7d3b507a1af78a98a7039648f66f23` | 5,883,279,159 |
| `sentencepiece.bpe.model` | LFS sha256 | `c49dc7e82c10227af764e518924cf2f9d50c00462750d184fa74697bba65eef8` | 4,920,706 |
| `config.json` | git-blob SHA-1 | `5259f0909bbb98005e355a94f0a9ad9902dc1810` | 548 |
| `generation_config.json` | git-blob SHA-1 | `b73e8f8fc85a983669324aeb7b0f9fc92e18f9f8` | 168 |
| `special_tokens_map.json` | git-blob SHA-1 | `169adeb038b8bde6ecf79666dbfa49fcbaf9a087` | 276 |
| `tokenizer.json` | git-blob SHA-1 | `98f7774e39cd7ce59acfe522852863101ccad1d8` | 9,032,074 |
| `tokenizer_config.json` | git-blob SHA-1 | `9a478583cf78963e92ee738bf7dababc1b376cb2` | 335 |

Loader: `transformers` `XGLMForCausalLM` / `AutoTokenizer`, with `local_files_only=True` and `torch_dtype=float16`
(as in C-T1).

**Template** `scripts/c_pvr/prompts/lmcap_block_vi.txt`: 177 bytes, UTF-8, no trailing newline, sha256
`a1fb17d9b73e85667a84c3ff0daee6ff3a3a5b79cc0963af9eb0bd69eb480213`. The exact bytes:

```
I am an intelligent image captioning bot. Similar images have the following captions: {captions} A creative short caption I can generate to describe this image in vietnamese is:
```

- `{captions}` = `" ".join(c.strip() + "</s>" for c in caps)`.
- Prompt = for each of the N shots, `block(shot_caps) + " " + shot_answer.strip() + "</s> "`, then `block(query_caps)`.
- This is byte-equal to C-T1 `lmcap_block` / `lmcap_prompt` (l.212-223) with `LANG_NAME["vi"] = "vietnamese"`. It
  was checked on the bytes in v1 and again in CC-269 item 3.
- C-T1 took the text from LMCap App. D (C-T1 PREREG l.94, PDF sha256 `2125a242…`). The PDF was not re-read (U5).

**Parameters:**
- **K = 4** captions per block (= prereg k = 4, and LMCap's K).
- **Query captions** [proposal]: A1's top-4 for the query image from D-VI, in A1 order, with the §6 caption rule. This
  is C-T1's `lmcap_se` same-examples variant: every retrieval arm uses the same post-W25 datastore (direction v3
  l.208). LMCap's own M-CLIP retrieval (`lmcap_ri`) is not run.
- **N = 3 fixed shots** (LMCap) [proposal]:
  - drawn once from D-VI (the post-W25 datastore pinned in the OPS-1106c-datastores LOG line) with a new seed
    `SEEDS["A5"] = 20262005`, in the `SEEDS` pattern;
  - each shot's 4 captions come from A1's retrieval with the shot image as the query, the shot itself excluded;
  - each shot's answer is the caption that the §6 rule assigns to the shot id (N8);
  - a shot image is never a tier-1 query image.
- **Decoding:** greedy, 1 candidate, `max_new_tokens = 64` (`MAX_NEW["caption"]`, J-T), stop at `</s>`, batch 1.

**Departures from LMCap as published** (disclosed; no registered line is overridden):

| item | LMCap | here | why |
|---|---|---|---|
| decoding | beam 3, 3 candidates, M-CLIP image-text re-rank | greedy, 1 candidate, no re-rank | prereg §5.1 registers "k = 4, greedy decoding" for every arm |
| max new tokens | 40 | 64 | one caption constant for every captioning arm (J-T) |
| retrieval | M-CLIP image→caption over English COCO | A1's SigLIP2 top-4 from D-VI (Vietnamese) | same retrieved evidence as A1 and PVR |

Beam 3 + M-CLIP re-rank would override prereg §5.1 ("greedy decoding") for one arm and would need a PI line. It is not
proposed.

## 3. A9 (never-cut): ITM/ARA caption re-ranking

**Registered:** prereg §5.1 "A9 ITM/ARA caption re-ranking". Direction v3 l.202: keep the top k after caption–image
ITM scoring (BLIP-ITM style, Adjudicated Captioning).

**Scorer: the A4 M-CLIP of §1**, with the same pins and in the same fp32 pass. This is Q-A9-SCORER (a), ruled in
CC-269 Ruling 3; PI-1106e raised no objection.
- BLIP-ITM has an English-only text side, and mBLIP has no ITM head (PINS-A v1.1 l.263). So no multilingual
  cross-attention ITM head is pinned. M-CLIP's cosine is a contrastive image–text match score that **stands in for
  ITM**. It is disclosed as such.
- **Disclosed cost:** both key secondaries, PVR − A4 and PVR − A9, rest on one scorer. They differ in granularity
  (mention vs whole caption), not in scorer.
- The alternative, NB-ENC SigLIP2 (`google/siglip2-so400m-patch14-384` @ `e8e48729…`), is not used. It would both build
  the pool and order it.

**Parameters** [proposal]:
- **Pool:** A1's top-7 from D-VI for the query image, with the §6 caption rule. This is the same pool A3 samples from
  (`A3_TOP = 7`, `c_pvr.py` l.79).
- **Score:** each caption's full text (cleaned as for A1 display, PINS-A v1.1 rendering rule 4) against the query
  image. cos as in §1, fp32.
- **Keep:** the 4 highest scores. Ties go to the better A1 rank. The 4 are shown in descending score order.
- No threshold; nothing is deleted inside a caption.
- **Truncation count** (N6; descriptive; closes U4 descriptively): per arm and set, the number of A9 captions that the
  open_clip tokenizer truncates. Ids and counts only.

## 4. A10 (cut-first, 1st): RA-CoA-style re-derivation

**Registered:** prereg §5.1 "A10 RA-CoA-style re-derivation". Direction v3 l.203: the retrieved values are dropped,
and the VLM is asked about each key on the query image. RA-CoA (TMLR 2026):
- takes attribute **keys** from the top-K retrieved products;
- discards their retrieved values;
- asks the VLM once per key on the query image, with no yes/no check;
- also shows 2 unverified exemplars (`C_NOVELTY_AND_DATA` §1.2-1.3).

**Model:** the pinned VI captioner `Gregor/mblip-bloomz-7b` @ `4d95b91d56fcdce86504c951a28f016b15e219a1`. This is
PINS-A A1/A2, with the same load-time checks, bf16 and batch 1. No new weights.

**Prompts** (both new; [proposal]). The style follows the CC-232 C4 rule: an English instruction that names the target
language, as in `cap_vi_0.txt` and `ver_3way.txt`. UTF-8, no trailing newline, like the 6 existing prompt files.

1. `scripts/c_pvr/prompts/rederive_vi.txt`: 68 bytes, sha256
   `478c5fdde54423222384897653fb080c55b7c0a04c1b30cc850ca4becd87c312`.
   ```
   Describe "{key}" in this image in a few words. Answer in Vietnamese:
   ```
2. `scripts/c_pvr/prompts/rederive_cap_vi.txt`: 54 bytes, sha256
   `93aa55e3bbaab95f4a5374f6df623d7d58d6b91aab184ecd2a69270b78c8b509`. Exactly 3 lines, joined by `\n`.
   ```
   Facts about this image:
   {facts}
   Caption in Vietnamese:
   ```

**Why a new caption template:** `cap_vi_k.txt` heads its block "Captions of similar images:". The re-derived lines
are not captions of other images, so that header would be false. Only the header differs; the tail "Caption in
Vietnamese:" is `cap_vi_k.txt`'s.

**Procedure** [proposal]:
- **Keys:**
  - the `kind == "obj"` propositions of A1's top-4 demonstrations (D-VI, §6 caption rule; A6 decomposer), in
    demonstration order, then text order;
  - key text = the mention text as in §1, after `proposition()` (clean + the fixed quote rule `"` → `'`);
  - a key string that recurs is asked once.
- **Calls:** one mBLIP call per key, on the query image, with `rederive_vi.txt` (`{key}` replaced).
  - Greedy; `GEN_BASE`; new constant `MAX_NEW["rederive"] = 16` [proposal]. 8 (the verify value) is too short for "a
    few words".
  - The calls count against **CAP = 32** per image, with the PINS-A §2.6 overflow rule: keys beyond the cap, in order,
    are not asked. They are counted in `cap_hits` and never retried.
  - This **extends J-C** [proposal] (N5). J-C set CAP as the verifier cap for PVR, A8, S1 and S2 (`c_pvr.py` l.80).
    Here the same value bounds A10's re-derivation calls, so the per-image call budgets are equal.
- **Answers:** cleaned by `clean()`. An empty answer drops its key.
- **Facts block:** the remaining (key, answer) pairs in key order, through `demo_line.txt` (`{i}. {caption}`) with
  `caption = key + ": " + answer`.
- **Caption call:** `rederive_cap_vi.txt` with `{facts}` replaced, `MAX_NEW["caption"] = 64`.
- **Empty case:** if no key is left (no object proposition, or every answer empty), A10 uses the A0 prompt
  `cap_vi_0.txt`. The count is reported.
- **What retrieved text enters (B2):** no retrieved caption text enters the A10 caption prompt **except the key
  strings**, which are the object-mention spans of A1's demonstrations. The retrieved values (the rest of each
  caption) are dropped.

**Departures from RA-CoA** (disclosed):

| item | RA-CoA | here | consequence |
|---|---|---|---|
| keys | attribute names of a fixed fashion schema (e.g. a garment property), from retrieved products | object mentions parsed from the retrieved captions (A6 decomposer) | **retrieved object identities enter the prompt by design**, as keys. A10 re-derives what is said about each retrieved object; it does not remove a retrieved object that is absent from the query image. So A10 is not a filter of object identity |
| exemplars | 2 retrieved exemplars, shown unverified | none | a whole demonstration would bring the retrieved values back |
| domain, language | fashion/furniture, English | general images, Vietnamese answers under an English instruction (CC-232 C4) | — |

## 5. VRAM on one RTX 3090 (24 GiB = 24,576 MiB; PI-1104ae; GPU_RENTAL_SPEC)

All figures are [est.]. They come from the LFS byte counts at the pinned revisions, converted to GiB (2^30 B), as in
CC-269 Ruling 6. The CUDA context and activations are not counted. The measured peak from the GPU-host selftest and the
speed test binds; it is UNVERIFIED until then (U1).

| model | weights on GPU | alone | together with mBLIP |
|---|---|---|---|
| mBLIP-bloomz-7b, bf16 (every VI mBLIP arm, PVR, A10; not A5) | ≤ 17.24 GiB (shards 18,515,228,320 B; bf16 load is at most this) | fits | — |
| M-CLIP ViT-H-14 / XLM-R-L, fp32 (A4, A9) | 4.44 GiB | fits | 21.69 GiB; headroom 2.31 GiB before context and activations |
| XGLM-2.9B, fp16 (A5) | 5.48 GiB | fits | 22.72 GiB; headroom 1.28 GiB before context and activations |

**Rule** [proposal]: the helpers are **not co-resident with mBLIP, by rule** (N1). Co-residence is not shown to fail;
the headroom above is small, and separate passes are always feasible and simpler to make deterministic.
1. An M-CLIP pass writes the A4 and A9 scores (ids and floats only) for every tier-1 query.
2. An XGLM pass writes the A5 captions.
3. Then the mBLIP passes run.

Each pass unloads its model, and `torch.cuda.empty_cache()` is called before the next load. The speed test (S13) times
every pass, so P1 includes them.

## 6. Demonstration caption of a multi-caption D-VI image (N8)

**The gap.** D-VI images carry several captions each: KTVIC train has 2,192 images and 10,960 captions; OpenViIC
train has 8,377 images and 37,785 captions (host v3 l.210). The kept ids are image ids. A1, and through it A4, A9,
A10 and the A5 shots, need **one** demonstration text per image id.

**Search.** No rule picking that caption exists in the registered or drafted text that was searched:
- `PREREG_DRAFT_v1_2.md` (§7.4 defines D-VI as "KTVIC train + OpenViIC train human captions" and stops there);
- `PINS_A_DRAFT.md`, `_v1_1` and `_v1_4` (v1.1 rendering rule 4 normalises the text but does not choose it);
- `AMENDMENT_CC222_DRAFT_v1_3.md`;
- host v3, T1-REP v4 and `W25_DEV_RUN_DOC_v1_4.md`.

This is stated plainly: **no registered rule exists.**

**Code precedent (not registered).** C stage-1 `scripts/c_stage1/decode_icl.py` (fa5a2511, commit 6129e8e)
`memory_captions`, l.159-172, chooses "the first released caption of each member":
- KTVIC: the first entry of `train_data.json` `annotations`, in file order, whose `image_id` equals the id;
- OpenViIC: `captions[0]` of the id's entry in `uit-openviic-annotation-train.json`.

**Rule** [proposal, Q-DEMOCAP; for the judge and the PI to rule]:
- The demonstration text of a D-VI image id is **its first caption in source json order**: KTVIC = the first
  `annotations` entry with that `image_id`; OpenViIC = `captions[0]`.
- PINS-A v1.1 rendering rule 4 then applies (NFC; whitespace runs collapse to one space; trim).
- It is deterministic and needs no seed or model. It is the same choice as C stage-1.
- It binds every VI retrieval arm (A1-A12, PVR), the A9 pool and the A5 shots alike. It is fixed before any output,
  and no caption is chosen by score.
- The source json files are pinned by sha256 in the S10 code; a mismatch is a FAULT.

**Scope.** No such rule was found for D-EN or D-TC either. They serve no arm of this file, so they are not ruled here.
The S10 read must confirm a rule for each of them (flag carried).

## 7. Provenance of the pins

- **HF API reads**, 2026-11-06T00:25:18Z-00:25:21Z. Public, no auth, no token, no e-mail; user-agent `vsps-research`.
  - Model info: `laion/CLIP-ViT-H-14-frozen-xlm-roberta-large-laion5B-s13B-b90k`, `FacebookAI/xlm-roberta-large`,
    `facebook/xglm-2.9B`, `Gregor/mblip-bloomz-7b`.
  - `tree/<rev>?recursive=true` for the first three.
  - Every info `sha` equals the pinned revision. Every tree value equals the C-T1 registry 09e6f90a.
  - Only API JSON was read; no weight or tokenizer file was downloaded.
  - CC-269 re-fetched all of these at 00:46Z and found them identical.
- **Response bodies, sha256.** The bodies and the 3 prompt files are archived at
  `.session_backup/2026-11-06/s9_hf/` (git-excluded).

| body | sha256 |
|---|---|
| mclip info | `25c4292292ae0d3b6a919c010427a01b3e91457ae885be144bd4692d5d3bfac9` |
| mclip tree | `f708cbbc4452249eeb716ccb207f5b89c949f6d8c559ca657156a7fb26f41ad6` |
| xlmr info | `8157fcb65fed6db1de530544bc32119c516dd8876a90b013ebcef3255460e477` |
| xlmr tree | `27f86b41c2e4679c097fc47dfe4db1ee5b271d9222a07e26c54dff039dbcc0c2` |
| xglm info | `44c7dddc6023b31aa9aea31f4745b974f55e35256b0ca9e89a0a01a74f254752` |
| xglm tree | `c971a8757d82f3ad70683f3509a33e2244e00d96c485189625ba918f5b9613be` |
| mblip info | `c93119f96c7ecba3ebf02789ceafb1a4010310bc2201f2c1c4b9fd7ad59ff852` |

- **Licences:** card tags. `mit` for all four repos. mBLIP's `mit` tag sits over a BLOOMZ base, which is very likely
  BigScience RAIL (CC-269 item 7). mBLIP was already pinned in PINS-A pin 1, so nothing new enters here.
  - Before any paper text, confirm the BLOOMZ base licence and the XGLM / M-CLIP training-data terms (U6, N9).

## 8. Binding on S10 (GPU-side code)

S10's code **must load exactly these pins and nothing else** for A4, A5, A9 and A10. This is checked the same way as
the PINS-A A1/A2 load-time check (v1.1 l.114-115).

1. **Sha check before load.** Before any helper loads, every file in §1-§2 is checked against its pin:
   - LFS files by sha256;
   - non-LFS files by git-blob SHA-1, with `c_pvr.py blob_hashes` (l.801; selftested at l.1238-1240). Their raw
     sha256 is not pinned here (U7).

   A mismatch is a FAULT, and nothing is scored or decoded.
2. **Offline load.** Snapshots load offline (`HF_HUB_OFFLINE=1`, `local_files_only=True`) at the pinned revisions.
   The XLM-R files are present in the cache under `xlm-roberta-large` before open_clip is built (C-T1 `t1check`
   precedent).
3. **Pickle weights.** `open_clip_pytorch_model.bin` and XGLM `pytorch_model.bin` are pickles. They load only through
   the Q-LLAVA `torch.load` wrapper (`weights_only=True`; it FAULTs on `weights_only=False`). The GPU-host selftest
   asserts this for both files.
4. **Prompt files** (N7). The 3 new prompt files are written into `scripts/c_pvr/prompts/` **at S10**, not at the
   gatekeeper commit of this file.
   - They go into `PROMPTS` in `c_pvr.py` with the shas above, byte-equal to the §2 and §4 code blocks.
   - The S10 diff read sha-checks them against this file.
   - The selftest renders one A5 prompt and one A10 prompt on synthetic strings and compares them byte for byte.
5. **New constants** go in `c_pvr.py`, one value each, imported by `c_pvr_run.py` (Q-SPLIT (i)):
   - `NES_TAU = 0.2`;
   - `A4_DEGEN = (0.05, 0.90)`;
   - `A9_POOL = 7`;
   - `SEEDS["A5"] = 20262005`;
   - `LMCAP_N = 3`;
   - `MAX_NEW["rederive"] = 16`;
   - the A5 generator (XGLM, PI-1106e) and the A9 scorer (M-CLIP, CC-269).
6. **Demonstration caption rule** (§6, once ruled). One function, used by every VI retrieval arm. It is selftested on a
   synthetic KTVIC-style and OpenViIC-style json with several captions per id.
7. **Logs hold ids only** (meta item 17).
   - A4 and A9 scores are written as id + float.
   - The A9 truncation counts (§3) are ids and counts.
   - A10 answers stay in the output files, never in per-image logs.
8. **Packages.** `open_clip_torch` and `ftfy` enter the GPU lock exact-pinned. Whether `open_clip_torch==2.32.0` runs
   with the C GPU `transformers` version is checked at lock time (U8).

## 9. UNVERIFIED

| # | item | how it closes |
|---|---|---|
| U1 | peak VRAM of every pass on the rented 3090 | GPU-host selftest + speed test |
| U2 | the effect of τ = 0.2 (set on CLIP-ViT-B/32) on M-CLIP H-14 with Vietnamese bare nouns | not closable before output; τ registered, never tuned; drop share and the §1 degeneracy label reported |
| U3 | NES text template | **partly closed (CC-269 item 6)**: NES states none for the filter; the bare mention is disclosed (§1) |
| U4 | open_clip context length for `xlm-roberta-large-ViT-H-14` | open_clip config at the locked version; the §3 truncation count |
| U5 | LMCap App. D template text (carried from C-T1, PDF 2125a242…, not re-read) | optional re-read before paper text (CC-269: byte-equal to C-T1, read under CC-172a) |
| U6 | licences beyond the HF card tags (BLOOMZ base of mBLIP; XGLM / M-CLIP training data) | read before paper text (N9) |
| U7 | raw sha256 of the non-LFS files (tokenizers, configs) | S10 records them on the host after the blob check |
| U8 | `open_clip_torch` 2.32.0 / `ftfy` 6.3.1 (and open_clip's deps) with the C GPU lock | GPU lock build and read |

## 10. For the round-2 one-judge diff read

- B1: closed by PI-1106e (§2).
- B2: closed by the §4 sentence and departure table.
- N1-N10: folded in (§11).
- **Q-DEMOCAP (new, §6):** first caption in source json order [proposal]. It is for the judge, then a PI line if the
  judge wants one. It blocks the S10 read, not this file.
- **Order:** GO → gatekeeper commit of this file → S10 implements §8 → before the speed test (S13).
- If A10 or A5 is later cut by the §5.1 cost rule, its pins stay recorded, unused.

## 11. Change table (v1 f9279a63 → v2)

| # | CC-269 item | where | change |
|---|---|---|---|
| 1 | B1 | §0, §2 | Q-A5-GEN = (a) XGLM-2.9B cited to PI-1106e; v3 l.198 quoted in full; the departure sentence and its reason; the generator confound stated beside PVR − A5; option (b) recorded as not used; "the judge rules it" removed |
| 2 | B2 | §4 | the false sentence "Retrieved caption text never enters the A10 caption prompt" replaced by the key-string exception; new RA-CoA departure table (object mentions as keys, so retrieved object identities enter by design) |
| 3 | N1 | §0, §5 | sizes in GiB (2^30 B); "does not fit" replaced by "not co-resident by rule", with headroom 2.31 / 1.28 GiB [est.]; mBLIP row no longer lists A5 |
| 4 | N2 | §0 | "equals C-T1" qualified: hub, revision and files; dtype differs (C-T1 fp16, here fp32 [proposal]) |
| 5 | N3 | §1 | NES facts from CC-269 item 6 recorded; the bare mention disclosed as departing from NES's only stated template |
| 6 | N4 | §1, §8.5 | A4 degeneracy label fixed now: XM3600-vi drop share > 0.90 "near-total" / < 0.05 "near-null"; descriptive only |
| 7 | N5 | §4 | A10 calls against CAP named as an extension of J-C [proposal] |
| 8 | N6 | §3, §8.7 | A9 truncation count per arm and set (ids and counts) |
| 9 | N7 | §8.4 | prompt files land in `scripts/c_pvr/prompts/` at S10, sha-checked in the S10 read |
| 10 | N8 | §6 (new), §2, §3, §4, §8.6 | no registered caption-selection rule found; C stage-1 code precedent cited; Q-DEMOCAP rule "first caption in source json order" [proposal]; A5 "shot's own caption" now reads "the caption the §6 rule assigns to the shot id" |
| 11 | N9 | §7, U6 | the BLOOMZ base licence and training-data terms are to be confirmed before paper text |
| 12 | N10 | header, §1-§3 | D-VI wording tied to host v3 l.210 ("serves the VI arms"); D-TC and D-EN excluded |
| 13 | Ruling 3 | §0, §3 | Q-A9-SCORER = (a) M-CLIP recorded as ruled, PI no objection; the one-scorer cost disclosed |
| 14 | items 2, 7 | §1 | "keep cos > τ" vs registered "drop < 0.2" noted; open_clip deps added to the lock note |
| — | — | all | no hub id, revision, file sha, prompt byte or prompt sha changed |
