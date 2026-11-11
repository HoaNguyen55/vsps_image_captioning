# C-ATTR-DEV: registration of the development runs of the retrieval-attribution test (Paper C)

Version v1, DRAFT for the judge. Written 2026-11-11T04:01Z (11:01 VN). Not committed. Nothing in it has run. AI opinion, not expert-validated.

Label on every output file and every row: `DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY`.

Design note: `manuscript/directions/method_2026-11-11/METHOD_DELTA_C.md`. Source of the design: `manuscript/directions/DR_GAPS_C_2026-11-10.md` §3 (G1, G3, G4, G5; Propositions 1, 3, 4, 5) and `manuscript/directions/portfolio_2026-11-10/REVIEW_2_C_D2_D5.md` §1.3–1.4 (C-E2 to C-E5, C-E7, C-E9).

Marks used: **[read]** = I read the cited line or file today; **[API]** = read today from a public repository or model-card API, no account, no e-mail in any request; **chưa kiểm** = not verified.

## 0. Bindings

1. **No test set.** OV-test, XM-test2500, COCO Karpathy test, NoCaps val and Flickr30K test are never staged, decoded, scored or opened. No statistic is computed on any test ledger. No reported test row changes because of a number produced here (§7.7: label only).
2. **Development only.** Every row is labelled development. No row is called confirmatory, in any file.
3. **No new gold labels. No AI label.** References are used only to score captions with the registered metric.
4. **Full sets.** Every run decodes every image of its development set.
5. **Hardware.** One RTX 3090 or 3090 Ti (24 GB) per host.
6. **Never committed:** captions, shown-caption files, embeddings, per-image ledgers.
7. **A failed rule is reported** beside the rule, in the main text of the paper.
8. **Order of looks.** OV-dev-A is scored and the nomination file is hashed before any new OV-dev-B output is scored or opened (§7.5).
9. This registration amends no earlier registration.
10. InternVL3 runs **without the deletion step** (τ = −∞, no verifier) in every arm of this registration. Its registered τ = 0.10 rows are not touched.

## 1. What existed before, and what the author of this file saw

**Numbers the author knows** (from the paper at `vsps-paperC-tallip` `f6aa449`) [read]:
- OV-dev-B: pooled `ret` − `rand` +6.04 [4.54, 7.58]; Qwen2.5-VL +9.67 [7.68, 11.72]; InternVL3 at τ = −∞ +5.36 [3.53, 7.12] (Tables S16, S17). `rand` − `zs` +8.91 [7.70, 10.16] pooled (`06_results.md` §6.8).
- XM-dev500: pooled +1.46 [−1.07, 4.17]; Qwen2.5-VL +4.44 [0.98, 7.85]; InternVL3 at τ = −∞ +1.54 [−2.12, 5.25] (Tables S16, S17).
- OV-dev-A: Qwen2.5-VL `ret` − `rand` +8.00 [6.02, 10.01]; InternVL3 +0.15 [−1.52, 1.82] at its frozen τ (stage-2 PREREG l.81).
- Flickr30K val and carve: Table 13 and Table S19, including the masked rows and the size-confounded memory swap.

**Stored outputs** (file names and sha sidecars read; no caption, prediction or ledger file opened):
- `.session_backup/machines/M3/root/outputs/c_stage1/runs/`: `zs`, `ret`, `rand`, `fix` on OV-dev-A for both backbones at the frozen configurations.
- `.session_backup/machines/M3/root/outputs/c_stage2/runs/`: `zs`, `ret`, `rand`, `fix`, `blind` on OV-dev-B and XM-dev500 for both backbones.
- `.session_backup/machines/M1/root/outputs/c_t1/out/`: `rand` draws d1 and d2 on OV-dev-B for Qwen2.5-VL, InternVL3 and Aya-Vision; Aya-Vision `zs`, `ret`, `rand` d0 on OV-dev-B; Qwen2.5-VL `ret_img` on OV-dev-B; `lmcap_ri` and `lmcap_se` on OV-dev-B; carve runs with the COCO memory and with the Flickr30K-train memory.
- `.session_backup/machines/M1/root/outputs/c_t2/out/`: Flickr30K val runs (`zs`, `ret` for three backbones; `rand` d0 for Qwen2.5-VL and Aya-Vision; `lmcap_ri`).
- Scored development ledgers of C-T1: `.session_backup/2026-10-30/c_t1/ledgers/` (`ov_vi.jsonl`, `carve_coco.jsonl`, `carve_f30k.jsonl`, `T1_SUMMARY.json`).

**Already computed on OV-dev-B by C-T1** (from its code, `c_t1.py` `summarize`, l.925–962 [read]; the values were not opened): `ret` − `rand` over three draws with the between-draw SD, and `ret` − `rand` after masking shared 3-grams. These statistics are therefore **post hoc on OV-dev-B** in this registration.

**Other stored looks at OV-dev-B:** the ablation runs of the 2026-10-28 registration (number of examples k, memory size, deletion threshold; paper §6.8), under `.session_backup/machines/{M1,M2,M3}/root/outputs/c2_ablation/` (folder existence checked; contents not listed).

**Not found in the folders listed above:** a `perm` arm; a second `fix` set; `rand_img`; `lmcap_rand`; `lmcap_perm`; any backbone other than the three above; Aya-Vision on XM-dev500; size-matched memory-swap cells.

## 2. Arms

Definitions reuse the registered ones. New arms add a suffix to a registered seed and change nothing else.

| arm | examples shown to image q | seed or rule | source |
|---|---|---|---|
| `zs` | none; the registered short prompt | `evaluate.PROMPTS["short"]`, sha256 `8870589c…` | stage-2 PREREG l.96 [read] |
| `ret` | the k eligible clusters nearest to q; ties by cluster id | – | stage-2 PREREG l.182 [read]; `build_memory.exemplars` l.362–363 [read] |
| `rand`, draw d | k clusters drawn uniformly from q's eligible clusters; a prefix of 8 | d = 0: `paperC|rand|<set>|<image id>`; d ≥ 1: the same with `d<d>` appended | stage-2 PREREG l.183 [read]; `c_t1.rand_draw` l.156–159 [read]; C-T1 PREREG l.119–121 [read] |
| `fix`, set j | one set of 8 clusters per development set, drawn among clusters below the near cut for every image of the set | j = 0: `paperC|fix|<set>`; j ≥ 1: the same with `f<j>` appended | stage-2 PREREG l.184 [read]; `build_memory.exemplars` l.366–367 [read] |
| **`perm`, draw p** (new) | the retrieved list of another image π_p(q), filtered by q's own near cut and refilled further down π_p(q)'s list | §2.1 | DR_GAPS_C §3 G1 |
| `ret_img` | the `ret` clusters, each as its image followed by its caption line | – | C-T1 PREREG l.122–123 [read] |
| **`rand_img`** (new) | the `rand` d0 clusters in the `ret_img` format | as `rand` d0 | – |
| `lmcap_ri` | LMCap re-implementation: M-CLIP retrieval, K = 4, N = 3 fixed shots, XGLM-2.9B, beam 3, re-rank | – | C-T1 PREREG l.124–127 [read]; `c_t1.py` l.61 [read] |
| **`lmcap_rand`** (new) | as `lmcap_ri`, but the query's K = 4 captions are the first 4 clusters of q's `rand` d0 list that are not one of the N = 3 shot clusters (`lmcap_ri` skips them too, `c_t1.py` l.465 [read]); shots, template, beam and re-rank unchanged | as `rand` d0 | – |
| **`lmcap_perm`** (new) | as `lmcap_ri`, but the query's K = 4 captions are the first 4 of π_1(q)'s LMCap retrieval list that pass q's near cut and are not a shot cluster | §2.1, p = 1 | – |

In every arm a cluster whose SigLIP2 cosine to q is ≥ 0.92 is never shown to q (`build_memory.NEAR_COS`, l.31 [read]). Shorter lists are prefixes of the 8-example list (`N_EX = 8`, l.32 [read]).

### 2.1 The `perm` arm, exactly

- Let the set's images be in manifest order, indices 0 … n − 1.
- π_p is a cyclic permutation without fixed point, built by Sattolo's algorithm with `random.Random(BM.seed("perm", <set>, "p<p>"))`: for i from n − 1 down to 1, draw j = `randrange(i)` and swap positions i and j. It depends on the set name and p only, never on an output.
- Let q′ = π_p(q). Let L(q′) be q′'s eligible ranking by `c_t1.eligible` (cosine to q′, descending; ties by cluster id; cosine to q′ below 0.92).
- The `perm` list of q is the first 8 clusters c of L(q′) with cosine(q, c) < 0.92. A cluster taken from beyond q′'s own first 8 is a **refill**.
- The k-prefix and the order rule (`first` or `last`) are applied as `c_t1.example_ids` applies them to `ret`.
- D = 2 (p = 1, 2) in every block.
- Diagnostics, printed per set and p: the share of refilled slots; the share of slots that `perm` and `ret` have in common for the same q; the mean cosine to q of the shown clusters in `ret`, `perm` and `rand`; the number of images with π_1(q) = π_2(q).
- **Gate.** If the refill share at 8 slots exceeds 0.10 on a set, `perm` on that set is reported as a diagnostic and carries no rule.

## 3. Backbones

### 3.1 The three stored backbones

| key | hub id @ revision | licence | k, order, tail | τ here | source of the configuration |
|---|---|---|---|---|---|
| `qwen25vl_7b` | `Qwen/Qwen2.5-VL-7B-Instruct` @ `cc594898137f460bfe9f0759e9844b3ce807cfb5` | apache-2.0 [API] | 8, first, T1 | −∞ (registered) | stage-2 PREREG l.72–78 [read]; `frozen_config.json` sha256 `2f0c32be7720b672f6e4aae229aba69da8742e0f9e32d34c5137e985ea36aa16` (computed today) |
| `internvl3_8b` | `OpenGVLab/InternVL3-8B-hf` @ `259a3b64a14623c0ec91a045cb43f7c5af5fa6af` (stage-1 DESIGN l.182 [read]) | `qwen` (card metadata, stage-1 DESIGN l.182 [read]; not re-read today) | 4, last, T2 | −∞ (binding 10) | the same |
| `aya_vision_8b` | `CohereLabs/aya-vision-8b` @ `d7601ac8fd3baf6f59c5fc9514c618ef0f24268f` [API] | cc-by-nc-4.0, gated "auto" [API] | 4, last, T1 | −∞ | C-T1 registry sha256 `09e6f90a…`; `t_config.json` of C-T1 [read] |

Qwen2.5-VL and InternVL3 share the Qwen2.5 language-model line. Aya-Vision's language model is Command R7B (C-T1 PREREG l.106 [read]).

### 3.2 New backbones outside the Qwen language-model lineage

All in bfloat16 on one 24 GB GPU. Sizes are parameter counts from the model-card API today; memory use in practice is chưa kiểm for each.

| order | key | hub id @ revision [API] | licence, gate [API] | language model | parameters | status of the pins |
|---|---|---|---|---|---|---|
| 1 (stored) | `aya_vision_8b` | §3.1 | §3.1 | Command R7B | 8.63 B | complete; already run |
| 2 | `gemma3_4b` | `google/gemma-3-4b-it` @ `093f9f388b31de276ce2de164bdc2081324b9767` | gemma terms; gated "manual" | Gemma 3 | 4.30 B | `l1b_registry.json` (sha256 `cd210a7c…`) has 4 null hashes (two safetensors, `tokenizer.json`, `tokenizer.model`) [read]; gate acceptance on the operator account chưa kiểm |
| 3 | `idefics3_8b` | `HuggingFaceM4/Idefics3-8B-Llama3` @ `fddb4ff79181e55a994674777e06cd5456ce3dc3` | apache-2.0; not gated | Llama 3.1 | 8.46 B | complete in `l1b_registry.json` [read]; Vietnamese ability chưa kiểm |
| 4 (fallback) | `llava16_mistral_7b` | `llava-hf/llava-v1.6-mistral-7b-hf` @ `2424fdd47412fccc66d91719126b420e9fbd7065` | apache-2.0; not gated | Mistral-7B-Instruct-v0.2 (its `config.json` [API]) | 7.57 B | no pins yet; a backbone of the RAICL paper |
| 5 (fallback) | `internvl25_8b` | `OpenGVLab/InternVL2_5-8B` @ `e9e4c0dc1db56bfab10458671519b7fa3dd29463` | mit; not gated | InternLM2.5-7B-chat (its `config.json` [API]) | 8.08 B | no pins yet; loader path in our harness chưa kiểm |
| 6 (fallback) | `llama32_11b_vision` | `meta-llama/Llama-3.2-11B-Vision-Instruct` @ `9eb2daaa8597bf192a8b0e73f848f3a102794df5` | llama3.2; gated "manual" | Llama 3.2 | 10.67 B (about 21.3 GB of weights) | no pins yet; fit under 24 GB chưa kiểm |

Excluded: `google/gemma-3-12b-it` (12.19 B parameters [API], about 24.4 GB in bfloat16) and every model on a Qwen language model (C-T1 PREREG l.109–110 [read]).

**The target is three non-Qwen backbones: orders 1, 2 and 3.** Rules, reused from C-T1 PREREG §6 (l.179–193 [read]):
- A model is skipped, never fetched and never a STOP, while any pin is null or its gate is not accepted. The next order number takes its place.
- **Vietnamese check** on its `zs` captions of KTVIC dev299: the share of captions with a Vietnamese-only letter or tone mark must be ≥ 0.95. Below that the model is NOT VIETNAMESE-ASSESSABLE and the next order number runs.
- **Configuration**: the stage-A rule with τ fixed at −∞. Among the 7 `ret` runs on dev299 (k ∈ {2, 4, 8} × {first, last} with T1, plus k = 4, last, T2), the highest stripped CIDEr-D with ΔP_cm against `zs` ≥ −1.0, near-verbatim copy share ≤ 0.05 and hit-max rate ≤ 0.02; ties to the smaller k, then `last`, then T1. No eligible run: the model fails selection and the next order number runs.
- Selection uses dev299 only. No dev299 row is a result of this registration.
- If fewer than three non-Qwen backbones have finished block 2 by 2026-11-14 18:00 VN, the number reached is reported and the rest are NOT RUN.

## 4. Prompts, k, memory and decoding (all reused)

- **Embedder:** `google/siglip2-so400m-patch14-384` @ `e8e487298228002f3d8a82e0cd5c8ea9c567f57f`, fp16 (stage-2 PREREG l.96 [read]; revision equals today's card head [API]).
- **Vietnamese memory:** `lists.json` `memory`, 10,501 images in 8,190 clusters; near cut 0.92; shown-caption rule of stage-2 PREREG l.207 (stage-2 PREREG l.96 [read]). Memory vectors `c_stage1/emb.npz` sha256 `59e65f6f6432af97504c59c72fa07b644acbff26938e1365473fad659421f7c0`.
- **English memory:** the C-EN COCO memory, 111,927 clusters: `cen_memory.json` `b77e4bde…`, `cen_memory_emb.npz` `add1d92a…` (C-T1 `RESTORED_SHA256` [read]). Shown caption: members[0]'s first sentence (C-T1 PREREG l.71–72 [read]).
- **Templates:** Vietnamese `decode_icl.TEMPLATE_SHA256` `7478361a133cf3944ce4e9952fd32cd97660cd747cb2f45bfdda30cd8a4a3a00` (`decode_icl.py` l.57 [read]); English `cen_decode.EN_TEMPLATE_SHA256` `b329e57a62d67a5afa62ff04503ed30992028839eb65284c3c6cae93a64ed713` (`cen_decode.py` l.50 [read]). Tails T1 and T2 as registered.
- **Decoding:** greedy, one beam, at most 60 new tokens, each model's own chat template, bfloat16 (stage-2 PREREG l.96 [read]; C-T1 PREREG l.117–118 [read]). LMCap: beam 3, 40 new tokens, fp16 (`c_t1.py` l.61 [read]).
- **k:** the frozen k of each backbone (§3.1); the selected k for a new backbone (§3.2). `rand`, `perm` and `fix` always use the same k and tail as that backbone's `ret`.
- No threshold, prompt or k is tuned on OV-dev-A, OV-dev-B, XM-dev500, the Flickr30K carve or Flickr30K val.

## 5. Development sets and image-id lists

| set | images | role here | id list | pin |
|---|---|---|---|---|
| KTVIC dev299 | 299 | configuration choice for new backbones only | `decode_icl.manifest` over `lists.json` | `decode_icl.py` sha256 `fa5a251160d4fd4fb0cd130af33614283863a84e6ed7905f3da81bb6255010db` and `lists.json` sha256 `5c479f03e8be544f4cd12b5d997b5dc92b6c622df061760cd02f6ba82f6b4371` (stage-1 `SHA256SUMS` [read]; the second recomputed today, equal) |
| OV-dev-A | 911 | nomination (§7.5) | `lists.json` `sets.ov_dev_a` (count read today: 911) | the same |
| OV-dev-B | 925 | the rule-bearing set | `lists.json` `sets.ov_dev_b` (925) | the same |
| XM-dev500 | 500 | reported rows, no rule | `lists.json` `sets.xm_dev500` (500) | the same |
| Flickr30K carve | 1,000 | CPU re-analysis of stored runs only | `c_t1_f30k_lists.json` `carve` (1,000) | sha256 `eebcd95b78b1dc98398550b1f89fea5622e8cbd9f20ad6b07b0d9292ba745968` (C-T1 `SHA256SUMS` [read]; recomputed today, equal) |
| Flickr30K val | 1,014 | English rows and the memory swap | `c_t1_f30k_lists.json` `refuse.val`, as `c_t2.py` reads it (l.142–144 [read]) | the same |

Stored example and vector files, with their sidecar sha256 [read]:
- `c_stage1/exemplars.json` `b52a03db40834bfa6556b70cf23dd3924a0024a3651a42c867f07d4603451068` (holds OV-dev-A lists);
- `c_stage2/ex_ov_dev_b.json` `072b17d14d89aa21110794be27168cf4ef4212a569a4d55d54c5acf1de7e5a41`; `emb_ov_dev_b.npz` `5ad23a678650ae736243a45c39915aaf795a5a46721fd855f67d155945bc8c95`;
- `c_stage2/ex_xm_dev500.json` `9a79b97dddd573b6092410f33dc2b069213a4407bb029102e05979811f66a17a`; `emb_xm_dev500.npz` `48ec2476e0f8ae4ce375d9ca9ccf05bbcdba86139ba66c2c5a868acf08347982`.

Refusals stay in force: the code refuses every image of `lists.json` `refuse` and `sets.xm_test2500`, the OpenViIC test files, and the Flickr30K test file names (`c_t1_f30k_lists.json` `refuse.test`). Flickr30K images are not on the laptop (checked: `data/datasets/` has no Flickr30K image folder). They are fetched again on the host from `nlphuji/flickr30k` @ `2b239befc81b6e3f035ce6bd52f5f4d60f5625f7` (zip sha256 `2ce2420c0d17f0531deaa89ac657b4d5067ec519da16ff1ea12acbf5619c7391`), and only the 1,014 val members are extracted, by list, under the C-T2 custody rule (C-T2 PREREG l.160–162 [read]).

**No Vietnamese memory swap.** Counted today from `lists.json` `memory` (counts only): 6,017 clusters hold only OpenViIC images, 2,133 hold both, and 40 hold only KTVIC images. A KTVIC-only memory cannot be formed. The swap of §7.9 is English only.

## 6. Runs

### 6.1 Rates used (measured, per decoded image, model load included)

From the timing files of our own runs, `gpu_seconds.tsv` of C-T1 and C-T2 (`.session_backup/machines/M1/root/outputs/c_t1/` and `c_t2/`) [read], seconds per step divided by the set size. The card model of that 24 GB host was not re-read (chưa kiểm; the C-T1 registration names an RTX 3090, l.160–161).

| backbone, arm type | Vietnamese (OV-dev-B, 925) | English (Flickr30K val, 1,014) |
|---|---|---|
| Qwen2.5-VL, text examples, k = 8 | 723–735 s → 0.78–0.79 s | 372–382 s → 0.37–0.38 s |
| InternVL3, text examples, k = 4, no verifier | 1,285–1,301 s → 1.39–1.41 s | 1,273 s → 1.26 s |
| Aya-Vision, text examples, k = 4 | 1,424–1,490 s → 1.54–1.61 s (`zs` 1,549 s → 1.67 s) | 1,359–1,393 s → 1.34–1.37 s |
| LMCap re-implementation | 1,047–1,054 s → 1.13–1.14 s | 747 s → 0.74 s |
| Qwen2.5-VL `ret_img`, k = 8 | 3,257 s → 3.52 s | – |

They agree with the paper's block rates of 0.8–1.1 GPU-seconds per caption (15,528 captions in 4.61 GPU-h; 20,000 in 4.90; 30,000 in 6.33; 27,000 in 6.88; 7,000 in 1.86: paper §6.10, §8.5, §8.6, as collected in `RUBRIC_C_2026-11-09.md` §4 l.274 [read]) and with stage-2 PREREG l.386 [read].

**Planning rates** (point): Qwen2.5-VL 0.80 s (Vietnamese), 0.38 s (English); InternVL3 1.40 s, 1.26 s; Aya-Vision 1.60 s, 1.37 s; LMCap 1.14 s, 0.74 s; `ret_img` and `rand_img` 3.52 s. The rate on XM-dev500 is assumed equal to OV-dev-B (chưa kiểm). **High** = point × 1.5. Gemma-3-4B (1.0 s) and Idefics3 or a fallback (2.0 s) are **not measured** (chưa đo); the smoke step replaces them.

### 6.2 Block 0: CPU, laptop, no rental (2026-11-12)

| step | content |
|---|---|
| 0.1 | Build the list file: `perm` p1, p2 for OV-dev-A, OV-dev-B, XM-dev500, Flickr30K val; `fix` f1–f4 for OV-dev-B and XM-dev500; `rand` d1, d2 for XM-dev500 and Flickr30K val; the swap subsamples (§7.9). **Parity gate K0:** the builder must reproduce the stored `ret` and `rand` d0 lists on OV-dev-B (925/925), XM-dev500 (500/500) and OV-dev-A (911/911), and the stored `fix` f0 sets. A mismatch stops everything before any rental. |
| 0.2 | `perm` diagnostics and the refill gate (§2.1). |
| 0.3 | Copy bound (§8) on stored outputs: OV-dev-B, XM-dev500, Flickr30K carve and val. |
| 0.4 | Variance components (§7.7a) from the stored three draws on OV-dev-B (post hoc). |
| 0.5 | The swap contrast δ on the stored carve cells (post hoc, size-confounded; §7.9). |
| 0.6 | Laptop dry run of every host mode of `c_attr_job.sh` in the host tree, with `--limit 2` and no model load. |

### 6.3 Block 1: the core attribution result on the Vietnamese sets (hard cap 12 GPU-h)

Run order as listed. New decodes only; every stored run is reused by its sha256 and never decoded again.

| step | backbone | arm × draws | sets (images) | captions | GPU-h, point |
|---|---|---|---|---|---|
| 1.0 | Qwen2.5-VL, Aya-Vision, InternVL3 | two re-decodes of the first 50 items of the stored `ret` run: (a) same order and batch size (host parity); (b) reversed order, batch size 1 (batch-invariance) (§9) | OV-dev-B (50 each, twice) | 300 | 0.26 |
| 1.1 | Qwen2.5-VL | `perm` p1, p2 | OV-dev-A (911), OV-dev-B (925), XM-dev500 (500) | 4,672 | 1.04 |
| 1.2 | Aya-Vision | `zs`, `ret`, `rand` d0 on XM-dev500; `perm` p1, p2 on OV-dev-B and XM-dev500 | XM-dev500 (500), OV-dev-B (925) | 4,350 | 1.93 |
| 1.3 | InternVL3, τ = −∞ | `perm` p1, p2 | OV-dev-A, OV-dev-B, XM-dev500 | 4,672 | 1.82 |
| 1.4 | Qwen2.5-VL | `fix` f1, f2, f3, f4 | OV-dev-B, XM-dev500 | 5,700 | 1.27 |
| 1.5 | all three | `rand` d1, d2 | XM-dev500 | 3,000 | 1.06 |
| **block 1** | | | | **22,694** | **7.4** (high 11.1) |

If the cap binds, steps are dropped from the bottom: 1.5, then the XM-dev500 half of 1.4, then 1.4, then 1.3. A dropped step is reported NOT RUN.

**Host-parity fallback (inside the same cap).** Every `ret` − `perm` contrast pairs a stored decode with a decode on the new host. If check (a) of step 1.0 fails for a backbone, that backbone's `zs`, `ret` and `rand` d0 are decoded again on the new host for the sets of its `perm` step, before that step. Its rows then use the new-host arms only (R = 1), carry the label "base arms re-decoded on the new host", and stay in their families. Extra cost at point rates: Qwen2.5-VL 7,008 captions, 1.6 GPU-h; InternVL3 7,008 captions, 2.7 GPU-h; Aya-Vision (OV-dev-B only) 2,775 captions, 1.2 GPU-h. The drop order above makes room.

After block 1 the following exist for Qwen2.5-VL, InternVL3 (τ = −∞) and Aya-Vision: `zs`, `ret`, `rand` × 3, `perm` × 2 on OV-dev-B and on XM-dev500; and, for Qwen2.5-VL, `fix` × 5 on both sets.

### 6.4 Block 2: new non-Qwen backbones (hard cap 12 GPU-h)

For each of the two new backbones in the order of §3.2:

| step | arm × draws | set (images) | captions |
|---|---|---|---|
| 2.0 | smoke: `zs` and `ret` k = 8 on 16 dev299 images; timing only, never scored | dev299 (16) | 32 |
| 2.1 | `zs`; the Vietnamese check; the 7 `ret` configurations; selection | dev299 (299) | 2,392 |
| 2.2 | `zs`, `ret`, `rand` d0–d2, `perm` p1–p2 | OV-dev-B (925) | 6,475 |
| 2.3 | the same 7 runs | XM-dev500 (500) | 3,500 |
| **per backbone** | | | **12,367** (+ 32) |

**Selection is scored on the host, by the job** (as block B1 of C-T1, C-T1 PREREG l.149 [read]). This is the one exception to §10.3–10.4: the job scores dev299 only, and the only outputs anyone reads before the pull are the selection file (model, k, order, tail, the Vietnamese-check share, selection PASS or FAIL) and the smoke timing. Before step 2.2 the job also decodes the first 50 OV-dev-B `ret` items a second time in reversed order at batch size 1 and compares them with the main run (A1, §9); 50 captions per backbone.

GPU-h, point, at the unmeasured planning rates: 3.4 (Gemma-3-4B) + 6.9 (Idefics3 or a fallback) = **10.3**. After each smoke the block is re-projected. If the projection exceeds the cap, step 2.3 of the slower backbone is dropped first, then step 2.3 of the other.

### 6.5 Block 3: third-party re-implementations, Vietnamese (hard cap 5 GPU-h)

| step | arm | set (images) | captions | GPU-h, point |
|---|---|---|---|---|
| 3.1 | `lmcap_rand`, `lmcap_perm` | OV-dev-B (925) | 1,850 | 0.59 |
| 3.2 | `lmcap_ri`, `lmcap_rand`, `lmcap_perm` | XM-dev500 (500) | 1,500 | 0.48 |
| 3.3 | Qwen2.5-VL `rand_img` d0 (k = 8) | OV-dev-B (925) | 925 | 0.90 |
| 3.4 | Qwen2.5-VL `ret_img`, `rand_img` d0 | XM-dev500 (500) | 1,000 | 0.98 |
| **block 3** | | | **5,275** | **2.9** (high 4.4) |

Steps 3.3 and 3.4 need the images of the 8,190 cluster representatives on the host, checked by sha256 before any GPU step (the `memcheck` of C-T1 PREREG l.74 [read]).

### 6.6 Block 4: English, Flickr30K val (hard cap 8 GPU-h)

| step | backbone | arm × draws | captions | GPU-h, point |
|---|---|---|---|---|
| 4.1 | Qwen2.5-VL, Aya-Vision | `perm` p1, p2 and `rand` d1, d2, COCO memory | 8,112 | 1.97 |
| 4.2 | Qwen2.5-VL, Aya-Vision | memory swap: `ret` and `rand` d0 with M_T, and with M_O subsample s0 (§7.9) | 8,112 | 1.97 |
| 4.3 | Qwen2.5-VL | `ret` and `rand` d0 with M_O subsample s1 | 2,028 | 0.21 |
| 4.4 | LMCap | `lmcap_rand`, `lmcap_perm`, COCO memory | 2,028 | 0.42 |
| 4.5 | InternVL3, τ = −∞ | `rand` d0–d2, `perm` p1–p2, COCO memory | 5,070 | 1.77 |
| **block 4** | | | **25,350** | **6.3** (high 9.5) |

Step 4.5 is dropped first, then 4.3. Query vectors (`emb_f30k_val.npz`), Flickr30K-train memory vectors (`emb_f30k_memory.npz`) and COCO memory vectors exist; no new embedding is planned. The Flickr30K-train caption store is rebuilt by `c_t2.py store` (`f30k_memory`, l.147–153 [read]). The COCO caption store used by C-T2 (`coco_captions.json`, C-T2 PREREG l.140) must be restored or rebuilt from the C-EN memory; where it is kept now is chưa kiểm.

### 6.7 Totals and hosts

- Captions: 22,694 + 24,734 + 5,275 + 25,350 = **78,053**. GPU-h, point: 7.4 + 10.3 + 2.9 + 6.3 = **26.9**. Sum of hard caps: **37**.
- Two hosts of the registered specification, rented together. Host H1: block 1, then block 3. Host H2: block 2, then block 4. No job runs beside another on one host.
- Block 1 does not wait for block 2.

## 7. Statistics

### 7.1 Per-image score

- **Vietnamese:** stripped CIDEr-D × 100 from kit B (`protocol_pilot.py` `6aee4282…`, `punctuation_audit.py` `a7e80240…`), RDRSegmenter of VnCoreNLP 1.2 (jar sha256 `9e2811cdbc2ddfc71d04be5dc36e185c88dcd1ad4d5d69e4ff2e1369dccf7793`), lower-cased, document frequencies over the scored set's own references (stage-2 PREREG l.226–232 [read]).
- **English:** PTB-tokenised CIDEr-D × 100, document frequencies over the set's own references (paper §8.1; C-T1 PREREG §7).
- Document frequencies come from references only, so one image's score does not depend on another image's caption.
- **Scoring parity gate.** Before any new run is scored, the scorer must reproduce the stored per-image stripped CIDEr-D of the Qwen2.5-VL `ret` run on OV-dev-B within 1e-4 (the tolerance of `c_t1.C2_PARITY_TOL`, l.75 [read]). A mismatch stops scoring. The laptop scoring environment (package freeze sha256, Java version) is written into the run record; its equality with the stage-2 environment is chưa kiểm and is settled by this gate.

### 7.2 Estimands

For one backbone at its configuration, one set, and image i:
- s_i(a) is the score of arm a; for `rand`, `perm` and `fix` the per-image value is the mean over that image's R draws, D permutations or R_F sets.
- τ_any = mean_i [s_i(`rand`) − s_i(`zs`)].
- τ_sel = mean_i [s_i(`ret`) − s_i(`rand`)].
- τ_marg = mean_i [s_i(`perm`) − s_i(`rand`)].
- τ_pair = mean_i [s_i(`ret`) − s_i(`perm`)].
- Identity, exact per image: `ret` − `zs` = τ_any + τ_marg + τ_pair, and τ_sel = τ_marg + τ_pair.

No pooled estimand over backbones is computed. Every row is per backbone.

R, D and R_F by set: OV-dev-B R = 3, D = 2, R_F = 5; XM-dev500 R = 3, D = 2, R_F = 5; OV-dev-A R = 1, D = 2; Flickr30K val R = 3, D = 2.

### 7.3 Interval

- Paired image bootstrap of the per-image differences of §7.2: B = 2,000, `numpy.random.default_rng(0).integers(0, n, (B, n))`, one index matrix per set shared by every interval on that set, percentile bounds (stage-2 PREREG l.251–254 [read]; `c_t1.boot_idx`, l.874–875 [read]).
- **Random-draw variance.** Each image has its own seeded draws, independent across images. With d̄_i the draw-averaged difference, Var(mean d̄_i) = [Var(m_I) + E σ²_I / R] / n, where m_i is the image's expected difference and σ²_i its between-draw variance (Proposition 3a; law of total variance). The image bootstrap of d̄_i estimates exactly this quantity, so the interval includes the variance of the random draw at any R ≥ 1. The same holds for `perm` over D.
- A shared `fix` set is different: §7.7b.
- p-like statistic for Holm: (1 + #{b : bootstrap mean_b ≤ 0}) / (B + 1), the registered Flickr30K form (paper §8.6); its floor is 1/2,001.

### 7.4 Labels and the smallest effect of interest

SESOI = **+2.0** stripped CIDEr-D points, the registered value (stage-2 PREREG l.283 [read]; test P1). In English the same +2.0 on PTB CIDEr-D, carried over without recalibration as in the paper (§8.1).

For any contrast with point estimate θ̂:

| label | rule |
|---|---|
| DETECTED | θ̂ ≥ +2.0 and the 95% lower bound > 0 (the form of the registered P1 rule) |
| REVERSED | the 95% upper bound < 0 |
| NEGLIGIBLE | the 90% interval lies inside (−2.0, +2.0) |
| UNRESOLVED | none of the above |

The labels exclude each other. NEGLIGIBLE is a two one-sided test at 0.05 per side.

### 7.5 Nomination on OV-dev-A, then the registered claim on OV-dev-B

The order mirrors the group's tier method: explore, then one registered look.

1. **Nomination (OV-dev-A, 911 images; Qwen2.5-VL and InternVL3 at τ = −∞, each alone).** Compute τ_pair and τ_marg with D = 2 and the stored `rand` d0. Nominate claim H_pair(m) if the 95% lower bound of τ_pair is ≥ +2.0. Nominate H_marg(m) if the 95% lower bound of τ_marg is ≥ +2.0. This is the nomination rule of C-T1 (`c_t1.advance`, l.905–908 [read]).
2. The nomination file `c_attr_nomination.json` lists the nominated claims. Its sha256 is written to the decisions LOG **before** any new OV-dev-B output is scored or opened.
3. **Registered claim (OV-dev-B, 925 images, one look).** Each nominated claim PASSES if its contrast on OV-dev-B is DETECTED. With more than one nominated claim, Holm at 0.05 over the nominated claims on the p-like statistic replaces "95% lower bound > 0"; θ̂ ≥ +2.0 is still required.
4. **Primary:** the nominated claims of Qwen2.5-VL, the backbone that carries the registered P1 result.
5. If nothing is nominated, there is no registered claim. The OV-dev-B rows are then reported with their labels and the sentence "no claim was nominated on OV-dev-A".
6. Components that were not nominated are reported with labels, as descriptive rows.
7. Aya-Vision and the new backbones have no OV-dev-A runs. Their τ_pair and τ_marg rows on OV-dev-B are a first look with labels and no registered claim.

### 7.6 Breadth family on OV-dev-B

- Family S-BB: τ_sel (R = 3) of every backbone first decoded under this registration (block 2). Each is DETECTED if θ̂ ≥ +2.0 and its Holm-adjusted p-like statistic is below 0.05, Holm over the backbones that completed step 2.2.
- τ_sel of Qwen2.5-VL, InternVL3 and Aya-Vision on OV-dev-B is post hoc (§1) and stays outside the family. It is printed beside it.
- Scope sentence, fixed now, counting the non-Qwen backbones (Aya-Vision's post hoc row is counted and flagged):

| non-Qwen backbones with τ_sel DETECTED on OV-dev-B | sentence |
|---|---|
| 2 or more | "the retrieval-specific effect is not limited to the Qwen language-model line" |
| exactly 1 | "the retrieval-specific effect was seen for one backbone outside the Qwen line" |
| 0 | "the retrieval-specific effect was not seen outside the Qwen line on this set" |

τ_any of the new backbones is reported with its interval and label, outside every family.

### 7.7 Variance

**(a) Per-image draws (Proposition 3a).** For each backbone and set with R ≥ 2: the mean within-image variance over draws σ̂²_w; the draw part σ̂²_w / (nR) as a share of the total s²(d̄_i) / n; the `rand`-against-`rand` placebo, mean of s_i(d1) − s_i(d2) with its interval. A placebo row is **flagged** when |θ̂| ≥ 2.0 and its 95% interval excludes 0. A flag is not a STOP: under the null each row has about a 2.5% chance per side of an interval that excludes 0, so the size condition is required; a flagged set goes to the judge before its rows are used. On OV-dev-B for the three stored backbones these rows are post hoc. On XM-dev500 they are a first look and descriptive.

**(b) One shared set (Proposition 3b).** Qwen2.5-VL, per set, y_iF = s_i(`ret`) − s_i(`fix`_F), F = 0 … 4. Two-way layout, one value per cell:
- MS_F = n Σ_F (ȳ_·F − ȳ_··)² / (R_F − 1); MS_I = R_F Σ_i (ȳ_i· − ȳ_··)² / (n − 1); MS_E = Σ (y_iF − ȳ_i· − ȳ_·F + ȳ_··)² / ((n − 1)(R_F − 1)).
- V̂_b = max(0, (MS_F − MS_E) / n). V̄_img = the mean over F of s²_i(y_iF) / n, which is what a single-set image bootstrap sees.
- ω̂ = V̂_b / V̄_img. Approximate 95% upper bound: V_b^U = max(0, (MS_F / F_0.05(R_F − 1, (R_F − 1)(n − 1)) − MS_E) / n); ω^U = V_b^U / V̄_img. For OV-dev-B the F quantile is about 0.178.
- **Rule (a label, not a verdict):** ω^U ≤ 0.25 → "the fixed-set rows are practically unconditional" (standard-error inflation at most 12%). Otherwise → every `fix` row of the paper is labelled "conditional on the realised fixed set", with ω̂ and ω^U printed.
- **Power, said plainly:** with five sets, ω^U is about 4.6 times the interaction share even when V_b = 0. The "practically unconditional" label is unlikely. The expected outcome is the "conditional" label plus an estimate.
- The five-set development row: ȳ_·· with standard error √[(MS_F + MS_I − MS_E) / (n R_F)] and a t interval with R_F − 1 = 4 degrees of freedom (conservative).
- **No test interval is widened, recomputed or relabelled with a number from this section** in this registration (question Q4).

### 7.8 XM-dev500 and English rows

Reported per backbone with the interval and the label of §7.4. They carry no registered claim: at n = 500 the known half-width for Qwen2.5-VL is about ±3.4 (Table S16), so neither DETECTED at +2.0 nor NEGLIGIBLE can be decided reliably. English rows on Flickr30K val are reported within English only; no cross-language difference is computed.

### 7.9 Memory swap on fixed images (English only)

- Images: Flickr30K val, all 1,014. Backbones: Qwen2.5-VL, Aya-Vision.
- **M_T (same source):** the Flickr30K-train memory of C-T1: 28,000 images, each its own cluster, first reference shown (C-T1 PREREG l.80–81 [read]).
- **M_O (other source):** 28,000 clusters of the COCO memory, drawn by `random.Random(BM.seed("swap", "coco", "s<j>")).sample(sorted(cluster ids), 28000)`, j = 0. A second subsample j = 1 is run for Qwen2.5-VL only.
- In every cell: `ret` and `rand` d0 at the frozen configuration, with the near cut.
- δ = mean_i {[s_i(`ret`; M_T) − s_i(`rand`; M_T)] − [s_i(`ret`; M_O) − s_i(`rand`; M_O)]}, with the interval and label of §7.3–7.4. The two τ_sel are printed beside it.
- Size is matched by construction. Caption length is **not** matched: `rand` in each cell carries that memory's length and style, and δ differences it out. The length gap |len_ret − len_rand| / len_rand is printed per cell; above 0.10 the cell is marked "not separated from length" (the registered rule L).
- M_O is one shared subsample. Its interval is conditional on that subsample; the j = 1 row shows the spread and supports no variance estimate (one degree of freedom).
- Post hoc companion, CPU: the same δ on the stored carve cells (full COCO memory, 111,927 clusters, against 28,000), labelled post hoc and size-confounded.
- Reading, fixed now. δ DETECTED: "on fixed images the retrieval-specific effect is larger with a same-source memory". δ NEGLIGIBLE: "the source of the memory did not change the retrieval-specific effect on these images". δ REVERSED or UNRESOLVED: reported as such. No claim about XM3600 or NoCaps follows from any outcome.

### 7.10 Third-party re-implementations

- LMCap: τ_sel = `lmcap_ri` − `lmcap_rand`; τ_pair = `lmcap_ri` − `lmcap_perm`; τ_marg = `lmcap_perm` − `lmcap_rand`; labels of §7.4. **Positive control:** LMCap's generator never sees the image, so its only image information is the retrieved captions. τ_sel must be DETECTED on OV-dev-B. If it is not, the test failed a case with a known answer (§10.1, K5).
- RAGCap-style: τ_sel = `ret_img` − `rand_img` for Qwen2.5-VL, labels of §7.4, beside the text-only τ_sel of the same backbone.
- Every row is labelled "re-implementation by this study; not the published system; not a statement about the published numbers".

### 7.11 Multiplicity, in one place

- One registered family: the nominated claims (§7.5), Holm at 0.05.
- One secondary family: S-BB (§7.6), Holm at 0.05.
- Everything else is reported with an unadjusted interval and a label, with no family-wise statement.

### 7.12 What is reported if a rule fails

- A nominated claim that is not DETECTED on OV-dev-B: "FAIL: the claim nominated on OV-dev-A did not hold on OV-dev-B", with the interval, in the main text.
- No nomination: the sentence of §7.5 item 5.
- S-BB with no DETECTED row: the third scope sentence of §7.6.
- A failed positive control: reported, and the word "test" is not used for the method.
- No post hoc statistic replaces a failed rule. A post hoc row may stand beside it with the label "post hoc" (PI-1110n).

### 7.13 Power (planning values)

Assumption: τ_pair has about the standard error of `ret` − `rand`, read from the half-widths of Table S16. The true standard errors are unknown until the run.
- OV-dev-B, Qwen2.5-VL: standard error about 1.03. Chance of DETECTED: about 0.49 at a true +2.0, 0.97 at +4.0, above 0.99 at +6.0. NEGLIGIBLE needs |θ̂| below about 0.3: low power.
- OV-dev-A, Qwen2.5-VL: half-width about 2.0 (stage-2 PREREG l.81). A claim is nominated when θ̂ is above about +4.0.
- XM-dev500, Qwen2.5-VL: standard error about 1.75. Chance of DETECTED about 0.63 at a true +4.0. NEGLIGIBLE cannot be reached. Hence no rule there.

## 8. Copy bound and placebo (CPU only)

- **Units.** (i) Syllables: whitespace tokens of the lower-cased caption, `c_t1.masked` unchanged (l.718–726 [read]). (ii) Segmented words: RDRSegmenter tokens. In English only (i) is used; its tokens are words.
- **Masking.** masked_n(y, S) removes from y every token that lies in an n-gram also present in a caption of S. n = 3 decides; n = 2 and n = 4 are sensitivity rows.
- **Loss.** loss(y; S) = s(y) − s(masked_n(y, S)), with the same references and document frequencies.
- **Per image.** κ_q = loss(y_ret,q; R_q) − loss(y_zs,q; R_q), where R_q is the list of k captions shown to q in `ret`. The `zs` caption was written without R_q: it is the placebo.
- **Reported.** K_ret = mean κ_q with its interval: an upper bound on the copy-carried part of `ret` − `zs`. L_cp = mean_q [(s_q(`ret`) − s_q(`rand`)) − κ_q] with its interval: a lower bound on the retrieval-specific effect that does not travel through copied n-grams.
- **Proposition 4, and when it holds.** Assumption A_cp: without copying, masking with R_q would cost the `ret` and `zs` captions the same score. It fails in one direction: a better `ret` caption shares more correct words with captions of similar images. So K_ret can only overstate copying. L_cp also assumes that copying does not lower the `rand` score.
- **Direction check of A_cp.** K_nc = mean_q [loss(y_rand,q; R_q) − loss(y_zs,q; R_q)]: the `rand` caption never saw R_q, so K_nc measures overlap that needs no copying. Expected sign: ≥ 0. If K_nc is REVERSED on a set, the stated direction is contradicted and the bound is withdrawn for that set.
- **Companions, descriptive:** K_rand (the `rand` d0 caption against its own shown list, same placebo); K_ret − K_nc, printed and never called a bound; loss of the stored `blind` caption against R_q (a caption written from the examples alone).
- **Reading, fixed now.** L_cp DETECTED: "a retrieval-specific effect of at least +2.0 remains under the most pessimistic copy attribution". L_cp point ≤ 0: "the bound does not exclude that the whole retrieval-specific effect is carried by copied n-grams; this agrees with, and does not prove, the published short-cut account". Otherwise: "partly bounded".
- **Sets and tier.** OV-dev-B, Flickr30K carve and val: pre-specified on stored outputs, **not a first look** (naive masked rows were computed there). XM-dev500: first look (C-T1 never scored it). Backbones: the three stored ones in block 0; the new ones after block 2.
- **Checks.** κ of a `zs` run against itself is 0; K_ret does not increase from n = 2 to n = 4.
- Not done: a decoding-time ban of n-grams (GPU option of the sketch) and an overlap-stratified curve.

## 9. Assumption checks

| assumption | check | consequence of failure |
|---|---|---|
| A1, no interference: one image's caption does not depend on its batch | step 1.0 (b), and the same check for every new backbone before its step 2.2: the first 50 `ret` items are decoded in reversed order at batch size 1; all 50 captions must equal, as strings, the captions of the same host's ordinary decode | that backbone leaves the registered families; its rows are printed as "A1 not met" |
| host parity: the new host reproduces the stored decodes | step 1.0 (a): the same 50 items in the stored order and batch size; all 50 captions must equal the stored ones | the fallback of §6.3: base arms decoded again on the new host; no backbone is dropped for this reason |
| A2, π independent of outcomes | by construction (§2.1); the list file is built and hashed in block 0, before any decode | – |
| A3, same template, k, order and decoder across arms | the code asserts that the prompt text sha256 differs between arms only through the example block; one loader per backbone | STOP |
| `perm` keeps the retrieval marginal | refill share ≤ 0.10 (§2.1) | `perm` is a diagnostic on that set |
| Proposition 3a, independent per-image draws | by construction (seed includes the image id); the `rand`-against-`rand` placebo of §7.7a | a flagged set goes to the judge |
| reference-only document frequencies | §7.1; a CPU sensitivity row recomputes document frequencies inside 200 bootstrap resamples for the OV-dev-B primary contrast | reported |
| A_cp direction | K_nc (§8) | bound withdrawn for that set |

What the propositions do not give: no claim about content against wording; no statement beyond the backbone, memory, template and set of the row; no test-set statement.

## 10. Stop rules, caps, custody, monitoring

### 10.1 Kill gates

| id | date | result | consequence |
|---|---|---|---|
| K0 | 11-12 | list parity fails (§6.2) | STOP, no rental |
| K0b | 11-12 | refill share > 0.10 | `perm` is a diagnostic on that set; if that set is OV-dev-B, there is no registered claim |
| K1 | 11-13 | a backbone fails the batch-order check (step 1.0 b) | that backbone leaves the families |
| K1b | 11-13 | a backbone fails host parity (step 1.0 a) | fallback of §6.3; rows labelled; nothing is dropped |
| K2 | 11-13 | nothing nominated on OV-dev-A | no registered claim; the method keeps τ_any, τ_sel, the variance terms and the copy bound |
| K3 | 11-13 | a nominated claim fails on OV-dev-B | reported as FAIL; same narrowing as K2 |
| K4 | 11-14 | third scope sentence of §7.6 | the paper's scope stays "one language-model line" |
| K5 | 11-15 | LMCap τ_sel not DETECTED on OV-dev-B | the positive control failed; the word "test" is dropped; third-party rows are printed without interpretation |
| K6 | 11-15 | a swap cell cannot be built or a Flickr30K file fails its sha256 | swap NOT RUN |
| K7 | 11-16, 12:00 VN | freeze | every unfinished step is NOT RUN |

### 10.2 Compute caps

- Block 1: 12 GPU-h. Block 2: 12. Block 3: 5. Block 4: 8. Counted as job wall time per GPU step, every step under `timeout` for the time left; a timeout is a CAP STOP and is final for that step (the accounting of C-T1 PREREG l.158–160 [read]).
- A failed step is resumed only from its own partial file, at most 3 attempts, then JOB STOP.
- A set that is not complete for an arm gives no row for that arm.
- Any refused image stops the step before the model loads.

### 10.3 Custody

- Host outputs live under `/root/outputs/c_attr/`. Each finished run writes its file and a sha256 sidecar.
- The laptop pulls a block only after the block's job has ended, re-hashes every file against the host list, and stores a read-only (444) copy under `.session_backup/machines/<host>/root/outputs/c_attr/`. Scoring reads the read-only copy only.
- No file is read, pinned or committed while its producer is still running. The one exception is the dev299 selection file of block 2 (§6.4).
- OV-dev-A outputs of step 1.1 and 1.3 are scored first; the nomination file is hashed; only then are the OV-dev-B outputs of those steps scored.
- Committed: this file, the list file (image and cluster ids only), the registry, the nomination file, the summary of numbers, the run record. Never committed: binding 6.
- The host is deleted after the pull is verified. If a fix would take longer than the set-up time, the host is backed up and deleted.

### 10.4 What may be opened while a run is going

Counts of finished items, progress lines, timing lines, return codes and fault lines. Nothing else: no caption, no per-image score, no partial ledger, no partial summary.

## 11. Code

`c_t2.py` is `c_t1.py` with one set added (its header, l.3 [read]). The same pattern is used: the new decoder is a copy of `c_t2.py` with the listed changes, and the diff against `c_t2.py` is part of the judge's code read.

### 11.1 To write

| file | content | self-test (must pass) | mutants (the self-test must fail on each) |
|---|---|---|---|
| `scripts/c_attr/c_attr_lists.py` (CPU) | builds `perm` lists (§2.1), `fix` f1–f4, `rand` d1–d2 for the new sets, swap subsamples; parity gate K0; diagnostics | a toy memory of 12 clusters and 6 images: no image is its own donor; no shown cluster at cosine ≥ 0.92 to q; draw 0 and f0 equal the stored rule; refill counted correctly | identity permutation allowed; near-cut filter applied to the donor only; `fix` seed without the `f<j>` suffix; refill taken from q's own list; `randrange(i + 1)` in place of `randrange(i)` |
| `scripts/c_attr/c_attr.py` (host) | `c_t2.py` plus: sets `ov_dev_a`, `xm_dev500`; arms `perm`, `fix` with a set index, `rand_img`, `lmcap_rand`, `lmcap_perm`; the 50-item re-decode mode; the guard with the refusal lists of §5 | run ids are unique per arm, draw and set; a second decode of an existing run id is refused; example ids of `perm` come from the list file only; the prompt sha256 of two arms differs only through the example block; every test file name is refused | `perm` reading the `ret` list; `rand_img` using `ret` clusters; `lmcap_rand` keeping one retrieved caption; guard without the Flickr30K test names; deletion step applied to InternVL3 |
| `scripts/c_attr/c_attr_score.py` (CPU) | per-image scores through the registered kit; §7 statistics, labels, Holm, nomination file, ANOVA; §8 copy bound | planted data: `ret` = `perm` + 3 and `perm` = `rand` give τ_pair = 3 and τ_marg = 0; a planted V_b is recovered within tolerance; κ of a `zs` run is 0; one index matrix per set; labels at the boundaries (θ̂ = 2.0; lower bound = 0); Holm on a three-claim toy case; the nomination file is refused if an OV-dev-B `perm` score already exists | draw 0 used in place of the draw mean; unpaired bootstrap; a fresh index matrix per contrast; κ without the placebo term; Holm skipped; "≥" and ">" swapped in a label; V_b divided by V_a in place of V̄_img; masking applied to the references |
| `scripts/c_attr/c_attr_job.sh` (host) | block order of §6, caps and timeouts of §10.2, lock, heartbeat, refusals, dry-run mode | the laptop dry run of §6.2 step 0.6: every mode starts, checks its inputs and stops before a model load | – (shell; covered by the dry run) |
| `scripts/c_attr/c_attr_mutants.py` | applies each mutant above to a temporary copy and runs the self-test; prints one PASS or FAIL line per mutant | all mutants killed | – |
| `manuscript/prereg/2026-11-11_c_attr_dev/c_attr_registry.json` | pins of the new backbones: `gemma3_4b` and `idefics3_8b` borrowed from `l1b_registry.json` by path and sha256; fallbacks with every file hash from the public tree API | no null hash for a model that is fetched | – |
| `manuscript/prereg/2026-11-11_c_attr_dev/c_attr_lists.json` | output of `c_attr_lists.py`; ids only | sha256 sidecar; parity gate K0 | – |

### 11.2 Reused unchanged (sha256 checked at code freeze)

- `scripts/c_stage1/build_memory.py` `e771b92d…` (`seed`, `NEAR_COS`, `N_EX`); `scripts/c_stage1/decode_icl.py` `fa5a2511…` (templates, `shown`, `memory_captions`, `manifest`) (stage-1 `SHA256SUMS` [read]).
- `scripts/c_t1/c_t1.py` `022af90e…` (`eligible`, `rand_draw`, `example_ids`, `masked`, `boot_idx`, `contrast`, `advance`, the LMCap code); `scripts/c_t2/c_t2.py` `6113844a…` (`extract`, `store`, Flickr30K val handling) (their `SHA256SUMS` [read]).
- `scripts/c_stage2/stage2.py` (`manifest2`), `scripts/c_en/cen_decode.py` (English template and `zs` prompt), `scripts/kit_b/` (scorer), `scripts/lb/` (the loader used by `c_t1.py`; its exact file was not opened, chưa kiểm).
- How much of `cmd_lmcap` (`c_t1.py` l.415–500) can take a different caption list without edits was not read in full (chưa kiểm); the plan allows one small change there, inside the copy.

## 12. Schedule

| date (VN) | step |
|---|---|
| 11-11 | this draft to the judge; code written with self-tests and mutants |
| 11-12 | judge ruling; commit through the gatekeeper; block 0; dry run; two hosts rented and set up |
| 11-13 | block 1 (H1); block 2 starts (H2); OV-dev-A scored, nomination hashed, OV-dev-B scored |
| 11-14 | block 2 ends; block 3 (H1); S-BB scored |
| 11-15 | block 4 (H2); positive control and swap scored; hosts deleted after verified pulls |
| 11-16, 12:00 | freeze; one results table with every row, its tier label and its rule |

## 13. Open questions for the judge, each with a recommended answer

| # | question | recommended answer |
|---|---|---|
| Q1 | Does the "at most 20 GPU-h per paper" line (PI-1109m, as read in REVIEW_2 §1.4) still bind this package? The plan needs 26.9 GPU-h at point rates under 37 GPU-h of caps. Whether that line survives PI-1110r is chưa kiểm. | It does not bind: PI-1110r removes cost as a decision factor. Keep the per-block caps as stop rules. |
| Q2 | May OV-dev-A nominate the claim before the one look at OV-dev-B (§7.5)? Its `ret` and `rand` rows were seen at stage A; only `perm` is new there. | Yes. It follows the group's tier method and fixes the direction of the claim without a look at OV-dev-B. |
| Q3 | InternVL3 at τ = −∞ only, with no verifier (binding 10)? | Yes. The deletion step with its zero-shot fallback would make `perm` a mixture of two arms. |
| Q4 | May a V_b estimated here widen or relabel a reported **test** interval? | No. Label only: "conditional on the realised fixed set". Anything more is a second look and needs its own ruling. |
| Q5 | Is the NEGLIGIBLE label (90% interval inside ±2.0) acceptable beside the registered DETECTED form, given its low power (§7.13)? | Yes, with the power statement printed wherever the label is used. |
| Q6 | The backbone list and its order (§3.2): Gemma-3-4B needs a manual gate and four hashes; Idefics3 may fail the Vietnamese check. | Accept the ordered list with fallbacks 4–6 and the 11-14 18:00 VN cut-off. |
| Q7 | Are `lmcap_rand` / `lmcap_perm` on our LMCap re-implementation and `rand_img` beside `ret_img` acceptable as the third-party application, given that no published system can be re-run (RAGCap: no code; RAICL: no code found; LMCap: no licence file)? | Yes, with the fixed label of §7.10. No sentence may say that a published result was overturned or confirmed. |
| Q8 | The Vietnamese memory swap cannot be formed from the registered memory (40 KTVIC-only clusters). Should a new out-of-source Vietnamese memory (for example UIT-ViIC train; licence and counts chưa kiểm) be built for fixed OV-dev-B images? | Not in this package. It needs a new memory build, a new near-duplicate pass and a licence check. State plainly that the swap is English only. |
| Q9 | May Flickr30K val, already used once as a rehearsal set, carry new development arms, with its images fetched again on a host under the C-T2 custody rule? | Yes. It has a development role only; Flickr30K test stays refused by name. |
| Q10 | Tier labels of the copy bound: "pre-specified on stored outputs, not a first look" on OV-dev-B and Flickr30K; "first look" on XM-dev500. | Accept. |
| Q11 | XM-dev500 equals the two development halves of Paper E (stage-2 PREREG l.109). Does any rule of that paper restrict new decodes there? Its current status is chưa kiểm. | No restriction: Paper E was stopped by the PI on 2026-10-25 (memory note); the judge confirms. |
| Q12 | Are two 50-item re-decodes per backbone (same order for host parity; reversed order at batch size 1 for A1) enough? | Yes, beside the 52/52 identical captions already on record (paper §9.1). |
| Q13 | Two hosts at once? | Yes: block 1 must not wait for the gated or unmeasured backbones of block 2. |
| Q14 | Judge tier for this registration. | Reversible: development sets only, no test look, no licence step, no submission. |

## 14. What this draft does not do

- It opens no test file and plans no test look.
- It does not claim that any published result is wrong.
- It does not include the memory-size ladder (G2), the per-example influence analysis (G6), a decoding-time n-gram ban, or a reference-free score (C-E8).
- It does not change any text of the paper. Paper text follows a separate ruling after the results table of 11-16.
- It writes no code. §11 lists what must be written.
- It promises no PASS.
