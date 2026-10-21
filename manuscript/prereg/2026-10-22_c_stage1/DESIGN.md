# Paper C, stage 1: design note for dev-only exploration

**Label: EXPLORATORY / DEV.** This note is not a registration.

| field | value |
|---|---|
| Paper | C: retrieval-augmented in-context captioning for Vietnamese, with an object guard from a different VLM |
| Authority | PI decision of 2026-10-22, 00:15 VN (`manuscript/cfp/QQ34_VENUES_AND_PLAN_2026-10-21.md`, §2.1 and "Quyết định của PI") |
| Written | 2026-10-22, before any Paper C output exists. No list, embedding, caption, guard score or metric of C exists. |
| Machine | M3 only (one RTX 3090 24 GB). The list build in §2.4 is CPU-only and runs off M3. |
| Code | `scripts/c_stage1/` (4 files). Their sha256 are in `SHA256SUMS` next to this note. `decode_icl.py` pins this note's sha256, so this note cannot list the code's hashes. |

## 0. Bindings

1. **Outputs are never committed.** This covers lists of captions, embeddings, example files, captions, guard caches and the ledger. They live on M3 under `/root/outputs/c_stage1/` and in the 30-minute backup.
   - The only stage-1 file that may be committed is `lists.json` (ids, file names and image sha256 only), through the lists addendum (§2.6).
2. **No registered claim comes from stage 1.** Every stage-1 number is a dev-A exploration number. It is recorded in the ledger (§7.5) and reported in the paper's "all configurations tried" appendix.
3. **Stage 2 needs its own prereg, committed before any OV-dev-B or XM-dev500 image is decoded.** It fixes the configuration chosen by §7.3, the SESOI, the metrics and the kill rules.
4. **A test prereg is committed before any OV-test or XM-test2500 image is decoded.** There is one test look.
5. **No test-set tuning.** Stage 1 decodes, embeds and scores dev-A images only (§2.5).
6. **No "first" or "novel" claims** ("đầu tiên" included), in any paper text. The paper states only differences from the closest work (QQ34 §2.1 table).
   - The paper must cite Li et al. (ACL 2024, 10.18653/v1/2024.acl-long.503) on token copying from retrieved captions.
   - It must cite ViG (MAPR 2026, 10.1109/mapr72750.2026.11685699).
7. **Existing data and labels only.** No new annotation.
   - The guard's verifier probabilities and every model caption are model signals. They are never gold, labels or evidence.
   - Gold is the references the datasets released.
8. **One GPU.** Everything runs on M3. No second machine is planned.
9. **No dataset caption is written into any committed file.**
   - The prompt templates (§4.1) are fixed by this design; they are not taken from any dataset, paper or prior prompt, and contain no dataset caption.
   - Memory captions are read from `$NCS_DATA` at run time, put into prompts in memory, and never written. Output files hold example ids and prompt sha256 only.

10. **Judge conditions of CC-079 (2026-10-22), carried here:**
    - **C2, hard stop before any lists build or decode.** The lists addendum records the SigLIP2 hub id, revision, licence and model-card README sha256, and the SSCD weights' source URL, licence and sha256. If either licence is not permissive for research use, stop and return to the judge. `build_memory.py` enforces this: `lists` requires `--sscd-url` and `--sscd-licence`, and `embed` reads the licence from the snapshot's README front matter; both refuse a licence outside `build_memory.RESEARCH_OK` (apache-2.0, mit, bsd-2-clause, bsd-3-clause, cc-by-4.0, cc-by-nc-4.0).
    - **C3.** Before the addendum commit, `lists.json` must pass an 8-gram scan against the KTVIC (train, test) and OpenViIC (train, dev, test) captions with 0 hits. `build_memory.py lists` runs this scan on its own output, records the hit count, and refuses to write the file if it is not 0. Paper C commits scores only (numbers, ids, sha256): never preds, exemplar files or captions.
    - **C5.** Paper B's kit is loaded by sha256 only; `score.kit` refuses on any mismatch (selftest-checked). `scripts/kit_b/` is committed through the gatekeeper before the stage-2 prereg.
    - **C6.** The stage-2 prereg names XM-dev500 as the only carve-out from `exclusion.json`, with the image-sha rule of §2.3. It keeps XM600 and XM-test2500 refused. It first checks that Paper A's 150-image XM3600 adjacency diagnostic (references only) lies inside XM600, and discloses that it used XM600 references.
    - **Q3.** The dev-pool greedy file `5280baa4…` is reused as the `zs` arm (§9), with the reuse disclosed in the run record and the paper. `guard.zs_ok` must pass at run time; if it fails, the `zs` run is decoded fresh.
    - **Q8.** The 0.92 near cut and the deletion rule, with its zero-shot fallback, stay as written. Regeneration is not explored in stage 1; if added later, it is a new arm in the stage-2 prereg. Thresholds are never tuned on a test set.
    - **Style report.** See §6.2 and §7.3: the length rule can block ADVANCE.

## 1. Question and arms

**Question (exploratory).** Does a zero-shot VLM, given k Vietnamese captions of its nearest training images as text-only examples, gain CIDEr-D over the same VLM given k random captions, at equal k and with the same guard? And does it do so without losing count-matched object precision against its own zero-shot caption?

Arms. All arms use the same backbone, the same short-caption decoding and the same guard.

| arm | examples shown to image q |
|---|---|
| `ret` (method) | the k memory clusters nearest to q by SigLIP2 image cosine (§3) |
| `rand` (control) | k memory clusters drawn at random for q (seeded, §3.3) |
| `fix` (style control) | one fixed set of k clusters per dev set, the same for every image (§3.3). Combined with B's punctuation normalisation in scoring (§6.1), this is the "style only" control. |
| `zs` (lower bound) | none: B's `short` prompt verbatim |

## 2. Data

### 2.1 Memory (retrieval pool)

| source | images | captions shown | terms (as recorded in Paper B §3.7) |
|---|---|---|---|
| KTVIC train minus dev300 (`data/splits/ktvic_train_minus_dev300.txt`, sha256 `006080b4…`) | 3,469 | the image's first caption in `train_data.json` annotation order | public at github.com/pacman-ctm/ktvic; no licence file, no terms; asks for a citation of Pham et al. (2024) |
| UIT-OpenViIC train (`uit-openviic-annotation-train.json`) | 9,088 (all captioned) | `captions[0]` | "publicly available for research purposes" (repository); the arXiv version says non-commercial research; no licence file |

- Use is research use only: captions go into prompts at run time and are never redistributed.
- Whether this use is covered by the terms is judge question Q1.

**De-duplication** (rule in §2.4):
- A memory image is dropped if it is byte-identical to, or a near-duplicate of, any image in the protected set:
  - KTVIC test (558) and KTVIC dev300 (300);
  - OpenViIC dev (2,011, both halves) and OpenViIC test (2,001);
  - all 3,600 XM3600 images;
  - any further test-image folder passed with `--protected`, e.g. CV295, CHAIR-500 or UIT-ViIC test, wherever their pixels are on disk.
- A memory image is also dropped if its sha256 is in `exclusion.json` (§2.5).
- Remaining images that are near-duplicates of each other are merged into one **cluster** by union-find. KTVIC and OpenViIC share many images (KTVIC took its images from a pool that OpenViIC shares).
- Each cluster is shown at most once per image. Its caption is taken from its member in the query's own dataset (KTVIC for dev299, OpenViIC for OV-dev-A) if it has one, otherwise from its first member.

### 2.2 Stage-1 dev sets (dev-A)

| set | images | references | notes |
|---|---|---|---|
| `ktvic_dev299` | 299 (`manuscript/prereg/2026-10-21_dev_pools/ktvic_dev299.tsv`, sha256 `a4ac7fdb…`) | the image's KTVIC train references | KTVIC dev300 minus image `1437`, a near-duplicate of a test image. **Not fresh**: dev300 chose S1 and other dev-side settings, and its zero-shot dev-pool captions exist (§9). The memory excludes dev300 and every copy of it. |
| `ov_dev_a` | half of OpenViIC dev, after filtering; about 930 expected (exact count in `lists.json`) | the image's OpenViIC dev captions | used once all dev299 choices are fixed (§7.3) |

### 2.3 Sets defined now, refused in stage 1

- **OV-dev-A / OV-dev-B.** The 2,011 OpenViIC dev files are ordered by sha256(`"paperC|ovdev|"` + image sha256). The first 1,005 form A-raw; the remaining 1,006 form B-raw. The split is assigned **before** de-duplication, so the filter cannot change membership.
  - A-raw is then filtered: an image is dropped if it is listed in `exclusion.json` or is a near-duplicate of KTVIC test, OpenViIC test, XM3600, any `--protected` set, KTVIC dev300 or **any B-raw image**.
  - B-raw is filtered against the same sets except dev-A.
  - Only `ov_dev_a` is decoded in stage 1.
- **XM-dev500 / XM-test2500.** These are the 3,000 XM3600 images not in XM600 (the 600 images of `$NCS_DATA/datasets/xm3600/test_data.json`, the set of `data/xm3600_subset.txt`), ordered by sha256(`"paperC|xm|"` + image sha256): the first 500 are dev, the remaining 2,500 test.
  - `exclusion.json` refuses all 3,600 XM3600 images, so XM-dev500 stays refused until the stage-2 prereg carves it out (Q7).
- **OV-test** is all 2,001 OpenViIC test files. It is a Paper C test set. Its annotation file is never read and never copied to M3. The lists step reads its file names from the annotation file's keys only, locally.

### 2.4 Near-duplicate rule (the registered rule, reused unchanged)

- `scripts/match_openviic.py` (sha256 `c0d9dd30…`) provides `_features` (pHash and dHash with imagehash on the EXIF-oriented RGB image, plus SSCD `small_288` input), `_mirror_hashes` and `hamming`.
- Two images are near-duplicates when **min(pHash, dHash) ≤ 10 and SSCD cosine ≥ 0.5**, taking for each hash the nearer of the direct and the mirrored distance. Byte-identical files always match.
- This is the rule of the dev-pool exclusion (dev-pools DESIGN §5).
- It is tuned for precision, so a retrieval-time cut backs it up (§3.2).
- SSCD weights: `sscd_disc_mixup.torchscript.pt`. They are **not on this machine**, and their sha256 is TO VERIFY. `lists.json` records the sha256 of the file used.
- This step reads image pixels, file names and ids only, and computes no model output. Its only use of captions is the C3 8-gram scan of its own output, which prints a count and nothing else. It runs on CPU off M3, and takes about 1–2 CPU-h.

### 2.5 Refusal (enforced in code)

`decode_icl.manifest`, `check_exemplars` and `guard score` refuse to run if any of the following holds:
- an input image's id is listed in `exclusion.json` for its namespace (KTVIC, COCO, XM3600);
- an input image's sha256 is listed in `exclusion.json` (every test set A and B registered or used: KTVIC test, XM3600, CV295, CHAIR-500, UIT-ViIC test);
- the image is listed in `lists.json` `refuse`: all OpenViIC test and OV-dev-B files (by file name in a separate `openviic` namespace, since KTVIC and OpenViIC share numbering) and all of their sha256, plus all XM3600 sha256;
- an example cluster contains the query image itself, or a refused image.

Each `--selftest` checks the refusal with a KTVIC test id, a refused sha256 and an OpenViIC test file.

**On M3**, stage 1 needs:
- the dev-A images;
- the memory images;
- KTVIC `train_data.json`;
- the OpenViIC train and dev annotation files.

The operator removes OpenViIC test and XM3600 files and annotations from `$NCS_DATA` on M3 before stage 1 and records this in the run record. KTVIC test images may remain from Papers A and B; the code refuses them.

### 2.6 Lists addendum (before any decode)

1. Run `build_memory.py lists` locally (CPU) to write `lists.json`.
2. Commit `lists.json` through the gatekeeper, together with a one-line change that sets `decode_icl.LISTS_SHA256`. `SHA256SUMS` is updated in the same commit.
3. Decoding refuses while `LISTS_SHA256` is unset.

The addendum also records (C2: all before any lists build or decode; stop if a licence is not permissive):
- the SigLIP2 hub id, revision, licence and model-card README sha256 (§3.1);
- the SSCD weights' source URL, licence and sha256;
- the C3 8-gram scan result of `lists.json` (must be 0 hits);
- the counts in `lists.json["counts"]`.

## 3. Retrieval

### 3.1 Embedder

| item | value |
|---|---|
| model | `google/siglip2-so400m-patch14-384`, image tower only (`AutoModel.get_image_features`, fp16, L2-normalised) |
| revision | **TO VERIFY**: resolved once on M3 at fetch, a 40-hex commit (`--revision` is required), recorded in the lists addendum before the embedding run. The snapshot's per-file sha256 go into the embedding file. |
| licence | **TO VERIFY** from the model card at that revision. Apache-2.0 is expected; the model is not cached here, so this is unchecked. If the licence is not permissive for research use, stage 1 stops (Q2). |
| venv | B-N1's `/root/venv-lb` (transformers 4.57.6) |
| images embedded | one representative per memory cluster (its first member) and every dev-A image, about 10–11k in total |

### 3.2 Neighbours and the near-duplicate cut

- Cosine is computed between L2-normalised image embeddings.
- **Near cut:** a cluster with cosine ≥ 0.92 to image q is never shown to q, in any arm. This backs up §2.4. The number of cut clusters per image is recorded.
- `ret`: the 8 eligible clusters with the highest cosine, ties broken by cluster id. k ∈ {2, 4} takes prefixes of these 8.
- Order:
  - `first`: the most similar example is "Ví dụ 1";
  - `last`: the most similar example is last, next to the instruction.

### 3.3 Random and fixed examples

- `rand`: per image, `random.Random(int(sha256("paperC|rand|<set>|<image id>")[:8], 16)).sample(eligible clusters, 8)`. k = 2 and 4 take prefixes, so the examples nest across k.
- `fix`: per dev set, `random.Random(int(sha256("paperC|fix|<set>")[:8], 16)).sample(clusters below the near cut for every image of the set, 8)`, with prefixes for k = 2 and 4.
- The ids, never the text, are in `exemplars.json` (not committed).

## 4. Prompts and decoding

### 4.1 Prompt texts (fixed)

The three ICL arms share one template; only the example block differs. The template is fixed by this design; it is not taken from any dataset, paper or prior prompt, and contains no dataset caption. `decode_icl.TEMPLATE_SHA256` = `7478361a133cf3944ce4e9952fd32cd97660cd747cb2f45bfdda30cd8a4a3a00` (sha256 of `json.dumps({"header", "line", "tails"}, ensure_ascii=False, sort_keys=True)`).

```
HEADER: Dưới đây là chú thích của một vài bức ảnh khác. Các chú thích này chỉ cho thấy cách viết, chúng không mô tả bức ảnh cần chú thích.
LINE:   Ví dụ {i}: {caption}
T1:     Hãy viết chú thích cho bức ảnh này bằng MỘT câu tiếng Việt ngắn gọn, theo cách viết của các ví dụ. Chỉ nêu những gì thực sự nhìn thấy trong ảnh. Không liệt kê, không giải thích.
T2:     Hãy viết chú thích cho bức ảnh này bằng MỘT câu tiếng Việt ngắn gọn, theo cách viết của các ví dụ. Không liệt kê, không giải thích.
```

- Prompt = HEADER, k LINEs and the tail, joined by newlines.
- The text comes after the image in the user turn of the model's own chat template, as in the LB decoder.
- An example caption is shown with its whitespace collapsed and is otherwise as released.
- `zs` uses `scripts/evaluate.py` `PROMPTS["short"]` verbatim (sha256 `8870589c…`, checked through `lb.prompt_text`).

### 4.2 Models and decoder

| key | role | hub id @ revision | licence (B-N1) | batch |
|---|---|---|---|---|
| `qwen25vl_7b` | generator | `Qwen/Qwen2.5-VL-7B-Instruct` @ `cc594898137f460bfe9f0759e9844b3ce807cfb5` | Apache-2.0 | 4 |
| `internvl3_8b` | generator | `OpenGVLab/InternVL3-8B-hf` @ `259a3b64a14623c0ec91a045cb43f7c5af5fa6af` | `qwen` (card metadata) | 2 |

- Both blocks come from the B-N1 registration (`2026-10-19_b_n1_vi_leaderboard.json`, sha256 `9ff02dc2…`), with every snapshot file pinned and checked by `lb.check_snapshot`.
- Decoding is greedy (`do_sample=False, num_beams=1`), with 60 new tokens (B-N1's `short`), bf16, sdpa, B-N1 processor kwargs and the B-N1 venv.
- `decode_icl.py` wraps the committed LB decoder unchanged (`lb.load`, `lb.make_generate`, which takes one text per image, `lb.decode_slices` with fixed slices and resume, and `lb.write_output`).
- The resume key includes the sha256 of every per-image prompt.
- `lb.make_generate`'s self-test already checks that a left-padded batch of prompts of different lengths gives the batch-1 captions.

### 4.3 Run grid

`decode_icl.py --list-runs` gives 20 runs per (set, backbone):
- `zs`;
- `ret` k ∈ {2, 4, 8} × order {first, last} with T1;
- `ret` k = 4, last, T2;
- `rand` and `fix`, each at k ∈ {2, 4, 8} × {T1, T2}.

The T2 controls exist only so that a T2 pick has its matched controls. Phases:

| phase | set | runs |
|---|---|---|
| P0 pilot | dev299 | qwen25vl_7b: `ret-k4-last-T1`, `rand-k4-T1` (zero-shot reused, §9) |
| P1 pre-screen | dev299 | both backbones: the 7 `ret` runs, `rand` and `fix` at k ∈ {2, 4, 8} with T1, and `zs` for internvl3_8b. That is 13 ICL runs per backbone, P0 included. If §7.2 picks T2, the matched `rand` and `fix` with T2 are added. |
| P2 rest of dev-A | ov_dev_a | per backbone: `zs`, the picked `ret` run, and `rand` and `fix` at the picked k and template |

## 5. Guard

- **Neighbour-only objects.**
  - A class o in a caption is neighbour-only when three conditions hold. First, `rescap.chair.objects_in` (matcher v2) finds o in the caption. Second, o is not in the image's own `zs` caption (same backbone). Third, o is in at least one of the examples shown with the image.
  - All comparisons are on `canonical(o)`; there is no hypernym credit.
  - The `zs` arm has none by definition. Classes in neither the `zs` caption nor the examples are not guarded; their share is reported.
- **Verifier.** It is a different VLM from the generator. The lineage is shared in part: InternVL3-8B's LLM is Qwen2.5-7B, and Qwen3-VL is in the Qwen line. The paper states this next to the mapping.

  | generator | verifier | protocol | environment |
  |---|---|---|---|
  | `qwen25vl_7b` | `OpenGVLab/InternVL3-8B` @ `853e3a797a661694b1b8ece0cb72dc2b23e3dac9` | S2's instrument unchanged: `xv_ef1.verifier`, `readme_loader` and `same_as_readme`, with shards checked against S2's pins | S2's venv, transformers 4.51.3 (the B-F1 venv on M3) |
  | `internvl3_8b` | `Qwen/Qwen3-VL-8B-Instruct` @ `0c351dd01ed87e9c1b53cbc748cba10e6187ff3b` | S2's question and P(yes) rule through the model's own chat template, one forward pass (`guard.hf_verifier`). The run stops if, over the first 20 questions, the median yes + no next-token mass is below 0.5, since the position read would then not be the answer position. | B-N1 venv |

- **Question and score.** The question is S2's English template "Is there {np} in the image? Answer yes or no.", with S2's 112-class `english_class_map`, read from the pinned S2 prereg (sha256 `ac6404b6…`).
  - p = P(Yes + yes) / (P(Yes + yes) + P(No + no)) at the first answer position.
  - It is computed with the image and with the question alone (no image, asked once per class).
  - The score is **s = p_with − p_without**.
  - The cache stores one row per (set, image, class), which all runs and thresholds share, so the threshold grid costs no GPU.
- **Threshold grid.** τ ∈ {−∞ (no guard), 0.0, 0.1, 0.2, 0.3, +∞ (delete every neighbour-only class, no verifier)}. Class o is rejected when s < τ.
- **Deletion rule (deterministic, `guard.delete`).**
  1. Keep the end punctuation aside.
  2. Cut the caption into units at commas, semicolons, `và`, `cùng với` and the locatives `bên cạnh`, `cạnh`, `gần`, `phía trước`, `phía sau`, `trước`, `sau`, `trên`, `dưới` and `trong`.
  3. Drop every unit that names a rejected class, together with the separator before it. If the first unit (the subject) names one, go to the fallback: cutting the subject would leave a fragment.
  4. Rejoin the rest and re-append the end punctuation.
  5. If the first unit was hit, or the result is empty, ends on a function word (`rl_reward.function_end`), or names any class set other than (original − rejected), use the image's `zs` caption instead ("fallback").
  - Deleted and fallback rates are reported.
  - The regeneration variant of the plan (decode again with an instruction to omit o) is not part of stage 1.

## 6. Metrics (dev only)

### 6.1 Protocol card (Paper B §4.2)

| item | stage 1 |
|---|---|
| sets | `ktvic_dev299` (299 images, KTVIC train references, 5 per image); `ov_dev_a` (count in `lists.json`, OpenViIC dev references, as released) |
| segmenter | RDRSegmenter, VnCoreNLP 1.2, through `scripts/kit_b/protocol_pilot.py` `rdr`, applied to candidates and references, lower-cased (protocol P0). `score.py` refuses a jar whose sha256 is not Paper B's `9e2811cd…`. |
| n-gram metric | CIDEr-D ×100, kit B's pycocoevalcap re-implementation, df over the scored set's references |
| punctuation | every arm scored as written **and** with trailing punctuation tokens stripped (`punctuation_audit.strip_trailing_punct_tokens`). **Decisions use the stripped column**, so no arm gains from the final period alone; this is B's normalisation, applied to all arms. |
| decoding | greedy, one caption per image, prompts of §4.1 |
| object matcher | v2 (tone-normalised), `rescap.chair` |
| uncertainty | paired image bootstrap, B = 2000, `numpy.default_rng(0)`, percentile 95% CI; when pooling backbones the image is the cluster (per-image differences averaged over backbones) |
| scorer process | separate from generation (CPU) |
| kit | `protocol_pilot.py` sha256 `6aee4282…` and `punctuation_audit.py` sha256 `a7e80240…`, loaded by sha from the staged kit (`.session_backup/2026-10-21/zenodo_build/code/scripts/kit_b`, not in git; Q5). `rescap.chair` is loaded from this repo first, and the kit's path inserts are undone. |

### 6.2 Reported per run and threshold (`score.py`, ledger rows)

- CIDEr-D, as written and stripped.
- CHAIR_i (`rescap.chair.chair`, gold = union of the image's references), and mentions per image.
- **Count-matched precision against `zs`.** This is Paper A §3.3(b), the matched prefix. k_i = min(|M_i(run)|, |M_i(zs)|) over distinct classes in order of mention, and ΔP_cm = 100 · (Σ tp_run(k_i) − Σ tp_zs(k_i)) / Σ k_i.
- Neighbour-only rate (neighbour-only classes / all classes, before the guard), rejected classes per image, and deleted and fallback rates.
- **4-gram copy rate against the memory**: the share of the caption's syllable 4-grams found in any shown-caption of any memory cluster. `zs` is the baseline.
- **Near-verbatim copy share**: captions with `rl_reward.copy_stat` m ≥ 0.90 against the examples shown (the `cm_pairs.py` copy rule).
- hit_max rate.
- **Style report** (CC-079), for every run including `ret`, `rand` and `fix`: mean caption length in syllables (`rl_reward.syllables`), the share of captions ending in punctuation, and the share of captions that open with one of the run's top-3 opening bigrams (first two syllables). `score.py decide` prints these for `ret`, `rand` and `fix` in the pilot and advance reports.
- Guard diagnostic, at τ = −∞ rows: the AUROC of s, of p_with and of p_without on the run's neighbour-only items against reference gold. This uses dev references only and is not a gate.

## 7. Decision rules (fixed now; `score.py decide`)

### 7.1 P0 pilot (go/no-go)

ΔCIDEr-D (stripped) is computed for `ret-k4-last-T1` − `rand-k4-T1`, on qwen25vl_7b, dev299, without the guard.
- **GO** if the point estimate > 0.
- **STOP** otherwise: no further C GPU work. Per QQ34 §2.5, the lead and judge choose between refocusing C on "fixed style + guard" and moving E to first place.

### 7.2 P1 pick (dev299 only)

For each backbone, the candidates are the 7 `ret` runs × 6 thresholds.
- **Eligible** if all three hold:
  - ΔP_cm against `zs` ≥ −1.0;
  - near-verbatim copy share ≤ 0.05;
  - hit_max rate ≤ 0.02.
- **Pick** the eligible candidate with the highest stripped CIDEr-D. Ties go to the smaller k, then `last`, then T1, then the lower τ.
- No eligible candidate means that backbone fails stage 1.

### 7.3 P2 advance to stage 2 (ov_dev_a only; these images played no part in the pick)

Each backbone uses its picked (`ret` run, τ), and `rand` and `fix` at the same k, template and τ. **ADVANCE** if all hold:
- **A1:** pooled over both backbones (per-image differences averaged over backbones), ΔCIDEr-D (stripped) of `ret` − `rand` has a point estimate ≥ +2.0 and a 95% CI lower bound > 0;
- **A2:** per backbone, the 95% CI lower bound of ΔP_cm against `zs` is > −1.0;
- **A3:** per backbone, the near-verbatim copy share is ≤ 0.05.

Δ against `fix` and against `zs` are reported with CIs and do not gate. There is no per-backbone rescue: if A1 fails pooled, stage 1 fails.

**Length rule (CC-079).** If, for either backbone, the mean caption length of `ret` and of `rand` differ by more than 10% (|len_ret − len_rand| / len_rand > 0.10), the A1 gain is reported as **"not separated from length"**. Then the run cannot ADVANCE, whatever A1–A3 say; `decide` returns verdict `JUDGE` and the run goes back to the judge, who may require a length-matched comparison in stage 2. The pilot report carries the same flag but its GO/STOP rule is unchanged. This rule changes no threshold of A1–A3.

### 7.4 After stage 1

- **ADVANCE:** write the stage-2 prereg for dev-B (OV-dev-B and XM-dev500, one look) with the picked configurations frozen. Its gate is QQ34 §2.4: CI lower bound > 0 and point estimate ≥ 2 × SESOI.
- **FAIL:** at most one more dev-A round, and only under a new stage-1b design note that lists everything seen here, within C's dev budget of 20 GPU-h in total. Then C stops.

### 7.5 Ledger

`score.py score` appends one JSON row per (run, τ). A row holds numbers, ids and input sha256 only (run, zero-shot, `lists.json`, examples and guard cache files), never a caption. Every configuration decoded is scored and kept, broken ones included.
- A run scored before its guard cache is complete gets only the τ = −∞ and +∞ rows, which need no verifier.
- `decide` uses the last row per (run, set, τ), so re-scoring a run supersedes its earlier rows.

## 8. Budget (one RTX 3090)

**Measured speeds** (RTX 3090, short prompt, KTVIC test 558, B-N1 run records, load and slice-0 parity included):
- Qwen2.5-VL-7B: 0.70 s/image;
- InternVL3-8B-hf: 1.27 s/image;
- S2 verifier (InternVL3-8B, 12 tiles): 1,306 items in 1,528 s, i.e. 1.17 s/item for two passes (`score.json` of the S2 job).

**Assumed:**
- ICL prompts cost ×1.3 (point) to ×2.0 (high) for the longer text. That gives Qwen 0.91 / 1.40 s and InternVL3 1.65 / 2.54 s.
- The guard costs 1.0 / 1.2 s per (image, class) item, with the no-image pass once per class.
- Neighbour-only items per image: P1 about 4–5 unique across 13 runs; P2 about 2.5–3 across 3 runs.
- The Qwen3-VL verifier speed is unmeasured and assumed equal.

| step | computation | GPU-h point | GPU-h high |
|---|---|---|---|
| SigLIP2 embeddings | about 10–11k images, one load | 0.2 | 0.3 |
| P0 pilot | 2 runs × 299 × 0.91 s (no guard needed) | 0.15 | 0.23 |
| P1 Qwen2.5 | 11 more runs × 299 × 0.91 s | 0.83 | 1.28 |
| P1 InternVL3 | 13 runs × 299 × 1.65 s + zs 299 × 1.27 s | 1.89 | 2.90 |
| P1 guard | 2 verifiers × 299 × 4–5 items × 1.0–1.2 s | 0.67 | 1.00 |
| P2 Qwen2.5 | 930 × (0.70 + 3 × 0.91) s | 0.89 | 1.27 |
| P2 InternVL3 | 930 × (1.27 + 3 × 1.65) s | 1.61 | 2.30 |
| P2 guard | 2 × 930 × 2.5–3 items × 1.0–1.2 s | 1.30 | 1.86 |
| T2 controls, only if §7.2 picks T2 | up to 2 × 2 runs × 299 | 0 | 0.40 |
| model loads (about 10 processes) | | 0.30 | 0.40 |
| **stage 1 total** | | **about 7.8** | **about 11.9** |

- **Hard cap: 12 GPU-h for stage 1.** The operator sums GPU time from the run records and stops the queue when the cap is reached. The cap is inside the plan's C dev budget of 20 GPU-h.
- **Without the pre-screen**, the full grid on all of dev-A (about 1,230 images, 2 backbones, 20 runs each) plus the guard would take about 25–30 GPU-h.
- **CPU:** the lists build takes about 1–2 CPU-h, off M3. Scoring takes minutes, since RDR runs in one batched pass per set.
- **Order on M3:**
  1. `build_memory embed`;
  2. `exemplars` (CPU);
  3. P0;
  4. score P0 and apply §7.1;
  5. P1 decodes, Qwen2.5 then InternVL3;
  6. guard items and cache, the Qwen3-VL verifier and the InternVL3 verifier in separate processes, never with a generator loaded (24 GB holds one model);
  7. score and §7.2;
  8. P2;
  9. guard;
  10. score and §7.3.

## 9. Reuse of dev-pool outputs

- **Reused (model and prompt match): `dp_qwen25vl_7b_ktvic_dev299-short-T0.preds.json`** (sha256 `5280baa49a6901fd862f7c376fc71d060477deea5235569afacca649f0378ded`). It serves as the `zs` arm and as the guard's own zero-shot caption for qwen25vl_7b on dev299.
  - Its provenance matches C's `zs` run in every decode setting: Qwen2.5-VL-7B @ `cc594898`, prompt `short` sha256 `8870589c…`, 60 new tokens, greedy, batch 4, transformers 4.57.6, manifest `a4ac7fdb…`.
  - It was made by generator `7ffb7344…` at git `249028d`, with git_dirty false.
  - `guard.zs_ok` checks these fields and this sha256 before use.
- **Not reused:**
  - the Qwen3-VL pools (not a C backbone);
  - every `detailed` run (C uses `short`);
  - every sampled pool (C decodes greedy).
- **Decoded fresh:** the `zs` of internvl3_8b on dev299, and of both backbones on ov_dev_a. There is no InternVL3 pool.

## 10. What was read before this note was written

- **The reused dev-pool file.** Only its provenance fields were read, plus one count: hit_max is true for 1 of 299 captions. No caption was read and nothing was scored. The same applies to the other 11 dev-pool files: only their names and the PASS line in WORKFLOW_LOG were seen.
- **The OpenViIC annotation files.** Their key structure and counts were read (train 9,088, dev 2,011 and test 2,001 images, all captioned). No caption was printed.
- **KTVIC `train_data.json`.** Its key structure and counts were read (3,769 images, 18,845 annotations).
- **XM3600 `full_data.json` and `test_data.json`.** Their key structure and counts were read.
- **Timing records.** The `score.json` of S2 (items and seconds) and the start and finish times of the four B-N1 KTVIC-test short runs. No caption was read from either.
- **Plan figures.** The QQ34 plan's quoted figures: S2 AUROC 0.634, the B punctuation audit, B-F1 FAIL, and kNN AUROC 0.58.
- **Never opened:** `data/ktvic_openviic_refs.json` was not opened. The de-duplication recomputes matches from pixels.

## 11. Open questions for the judge (each with the default this note uses)

| # | question | default |
|---|---|---|
| Q1 | Do the KTVIC and UIT-OpenViIC terms (no licence file; citation and research use) cover showing their train captions to a model as in-context examples? | Yes, as research use. Captions appear only in run-time prompts, and no output is released. |
| Q2 | SigLIP2 revision and licence (unverified here) | Resolve on M3 at fetch and record in the lists addendum; stop if the card is not permissive. |
| Q3 | May the dev-pool greedy `dp_qwen25vl_7b_ktvic_dev299-short-T0` serve as the `zs` arm? | Yes: model, revision, prompt, cap, decoding and venv match (§9). |
| Q4 | Is the verifier a different VLM? Only in part: InternVL3-8B's LLM is Qwen2.5-7B (its README), so S2's verifier shares an LLM base with Qwen2.5-VL, and Qwen3-VL is in the Qwen line with InternVL3's LLM. | Qwen2.5-VL is checked by S2's InternVL3 (the only verifier with a measured image signal); InternVL3 is checked by Qwen3-VL-8B (a different vision tower and LLM generation). The paper states the shared lineage. |
| Q5 | The kit_b scorer is only in the git-excluded staging tree. | Stage 1 loads it by sha256 from there. Commit `scripts/kit_b/` before the stage-2 prereg. |
| Q6 | Is computing perceptual hashes and SSCD descriptors of test images (CPU, off M3, no caption, no model output) allowed as "not touching" them? | Yes; the dev-pool exclusion used the same match records. |
| Q7 | XM-dev500 is refused by `exclusion.json` (all 3,600 XM3600 hashes). | The stage-2 prereg carves out XM-dev500 explicitly and keeps XM600 and XM-test2500 refused. |
| Q8 | The 0.92 SigLIP2 near cut and the deletion rule (§5) versus the plan's regeneration variant. The rule never cuts the subject unit: a rejected class there means the zero-shot caption is used. | Keep both as written for stage 1. Regeneration is not explored. |
| Q9 | The SSCD weights are not on this machine, and their sha256 is unknown. | Fetch from the SSCD release on the list-build machine and record the sha256 in `lists.json` and the addendum. |

## 12. What this note does not do

- It registers no hypothesis, SESOI or verdict. The thresholds in §7 are stage-1 routing rules only.
- It decodes, embeds and scores no test or dev-B image.
- It reads no reference until `score.py` runs on dev-A outputs.
- It commits no output.
