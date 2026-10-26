## 3. Method

The method has four parts: a captioned memory (3.1), example selection for each query image (3.2), a prompt and decoder (3.3), and a post-decode deletion step (3.4). Section 3.5 gives the configurations that the development stages froze. Section 3.6 describes the scorer.

### 3.1 Memory

The memory combines the KTVIC training images outside the KTVIC development carve with the UIT-OpenViIC training images: {{LISTS:counts.groups.kt_mem|i}} + {{LISTS:counts.groups.ov_train|i}} = {{LISTS:counts.memory_candidates|i}} candidates.

A candidate is dropped in three cases:
- it is byte-identical to, or a near-duplicate of, an image in any protected set (the KTVIC test and development images, all OpenViIC development and test images, all {{LISTS:counts.groups.xm_all|i}} XM3600 images, and the test images that the companion papers use);
- its hash is on the group's refusal list;
- it cannot be read.

Two images are near-duplicates when min(pHash, dHash) ≤ {{C:nd_hash|i}} and their SSCD [Pizzi2022SSCD] cosine is ≥ {{C:nd_sscd|f1}}, taking for each hash the nearer of the direct and mirrored distances.

{{LISTS:counts.memory_dropped|i}} candidates were dropped, leaving {{LISTS:counts.memory_images|i}} images. KTVIC and OpenViIC share many images, so near-duplicates inside the memory are merged by union-find into {{LISTS:counts.memory_clusters|i}} clusters. Each cluster is shown at most once per query. For an OpenViIC query the shown caption is the cluster's OpenViIC member's first caption, if the cluster has one; otherwise, and for every XM3600 query, it is the first member's first caption. Captions are read at run time and placed only in prompts.

### 3.2 Example selection

Images are embedded with the SigLIP2 image tower [Tschannen2025SigLIP2] (so400m, patch 14, 384 px; L2-normalised, fp16). The memory embeds one representative per cluster. A cluster whose cosine to the query is ≥ {{C:near_cut|p}} is never shown to that query in any arm. This second near-duplicate cut backs up the pixel rule of Section 3.1.

| arm | examples shown to query q |
|---|---|
| `ret` | the k eligible clusters with the highest cosine to q; ties broken by cluster id |
| `rand` | k eligible clusters drawn for q by a generator seeded from a hash of the set name and the image id |
| `fix` | one set of k clusters, drawn once per test set from clusters below the near cut for every image of that set, shown to every image |
| `zs` | none; the same zero-shot short-caption prompt the companion papers use |

In every arm, shorter example lists are prefixes of the 8-example list. The `ret`, `rand` and `fix` arms share one prompt template and differ only in the example block. `nn_top1` and `nn_cons` are not model arms. They output a memory caption directly: the nearest cluster's caption, or the consensus caption among the k nearest, with document frequencies taken from the memory pool. They need no GPU.

### 3.3 Prompt and decoding

The prompt follows the image in the user turn of each model's own chat template. It has three parts:
- a fixed Vietnamese header stating that the captions below belong to other images, show only how to write, and do not describe the image to be captioned;
- k numbered example lines;
- a tail asking for one short Vietnamese sentence in the style of the examples, with no listing and no explanation.

Tail T1 also asks the model to state only what is visible; tail T2 omits that sentence. "Order" fixes where the most similar example goes: `first` puts it first, `last` puts it next to the instruction. The template was written for this study, contains no dataset caption, and is pinned by its sha256 in the released code (prefix `7478361a`).

Decoding is greedy (one beam, no sampling) with at most {{C:new_tokens|i}} new tokens, in bf16 with each model's pinned snapshot and processor settings. Every snapshot file is pinned by hash. The pinned revisions are unchanged from stage A:

| role | hub id | revision (prefix) |
|---|---|---|
| generator | Qwen/Qwen2.5-VL-7B-Instruct | `cc594898` |
| generator | OpenGVLab/InternVL3-8B-hf | `259a3b64` |
| verifier for InternVL3 | Qwen/Qwen3-VL-8B-Instruct | `0c351dd0` |
| verifier for Qwen2.5-VL (stage B only) | OpenGVLab/InternVL3-8B | `853e3a79` |
| embedder | google/siglip2-so400m-patch14-384 | `e8e48729` |

The three virtual environments on the test machine (generation, scoring and verifier) matched their registered freezes: `{{C:venv_freeze_1|raw}}`, `{{C:venv_freeze_2|raw}}` and `{{C:venv_freeze_3|raw}}` (sha256 prefixes). Processor settings are those pinned with each snapshot.

### 3.4 Neighbour-only objects and the deletion step

An object class o in a caption is **neighbour-only** when three conditions hold:
1. the object matcher finds o in the caption;
2. o is absent from the same model's zero-shot caption of the image;
3. o appears in at least one example shown with the image.

Each neighbour-only class can be put to a verifier. The verifier answers an English yes/no question about the class, built from the fixed English class map of companion B's verifier protocol, which we use unchanged and cite to B. With p the normalised probability of "yes" at the answer position, the score is s = p(with image) − p(question alone). A class is rejected when s < τ.

Rejected classes are removed by a fixed rule:
1. Cut the caption at commas, semicolons, conjunctions and locative words.
2. Drop each unit that names a rejected class, then rejoin the rest.
3. Fall back to the model's zero-shot caption when the subject unit is hit or the result is malformed.

At τ = −∞ nothing is rejected and the caption is unchanged. The step is related to Negative Entity Suppression [Lu2025NES, arXiv 2511.08909; venue unverified], which filters entities absent from the input out of retrieved captions in zero-shot captioning and also suppresses them at the attention level. Our step instead acts after decoding, on the model's own caption, and only on classes that the examples introduced.

The verifier for each generator is a different VLM. For InternVL3-8B the verifier is Qwen3-VL-8B-Instruct, and for Qwen2.5-VL-7B it is InternVL3-8B. The lineage is shared in part: InternVL3-8B's language model is Qwen2.5-7B, and Qwen3-VL belongs to the Qwen line. A run stops if, over the first {{C:verifier_stop_q|i}} questions, the median probability mass on yes and no is below {{C:verifier_stop_mass|f1}}, since the position read would then not be the answer position.

### 3.5 Frozen configurations

Development stage A chose one configuration per backbone on the {{CHAIN:dev299_staged|i}}-image KTVIC development carve. The rule picked the highest stripped CIDEr-D among candidates that met three conditions:
- a ΔP_cm against zero-shot of at least {{C:s1_pcm|f1}};
- a near-verbatim copy share of at most {{C:s1_copy_max|p}};
- a hit-max rate of at most {{C:s1_hitmax|p}}.

The search covered {{C:s1_ret_runs|i}} `ret` runs per backbone (k ∈ {{C:s1_k|raw}} × both orders with tail T1, plus k = 4, `last`, with tail T2), each scored at τ ∈ {{C:s1_tau|raw}}. These configurations then advanced on OpenViIC development half A and passed a registered gate on development set B (Section 5.1). Nothing was changed for the test.

**Table 1. Frozen configurations, unchanged from the development stages.**

| | Qwen2.5-VL-7B | InternVL3-8B |
|---|---|---|
| k | {{FC:models.qwen25vl_7b.k|i}} | {{FC:models.internvl3_8b.k|i}} |
| order | first | last |
| prompt tail | T1 | T2 |
| guard threshold τ | {{FC:models.qwen25vl_7b.tau|raw}} (no deletion) | {{FC:models.internvl3_8b.tau|raw}} |
| verifier at test | none | Qwen3-VL-8B-Instruct |

At its frozen τ, InternVL3's `ret`, `rand` and `fix` captions pass through the deletion step of Section 3.4 before scoring. Qwen2.5-VL's captions are scored as decoded.

### 3.6 Scoring

All arms are scored by the companion B scoring kit, loaded by hash. Candidates and references are segmented with RDRSegmenter (VnCoreNLP 1.2) [Nguyen2018VnCoreNLP] and lower-cased. CIDEr-D (×100) uses document frequencies computed over the scored set's own references.

**The decision column is stripped CIDEr-D: trailing punctuation tokens are removed from candidates and references.** This keeps any arm from gaining by a final period alone. The as-written column and a PTB-tokenised column are also reported.

The object matcher is the tone-normalised matcher of companion A. CHAIR_i and the count-matched precision use the union of an image's references as gold. Verified precision on XM3600 is scored offline against the released human-verified Open Images labels, and those labels never reached the decoding machine.
