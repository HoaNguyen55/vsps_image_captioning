# Pre-registration: G2-B extended, the Qwen3-VL-8B-Instruct zero-shot ladder (Paper A Section 7.6)

- **ID:** `2026-10-18_g2b_qwen3vl_ladder`
- **Status:** registered before any G2-B output. `build_g2b_prereg.py` checked at 2026-10-18T18:26:41Z (HEAD `a513216222ad`) that no G2-B output, job file or Qwen3-VL caption of a CV295, UV231 or XM600 image exists in `data/results/` or in the machine backups (last successful backups: O-2293424 2026-10-15T03:03:38Z, O-2293440 2026-10-15T03:08:33Z, O-2308423 2026-10-18T18:00:37Z, O-2308428 2026-10-18T10:01:25Z), and that the live monitor snapshots of M1 and M2 name no G2-B job (M1_STATUS.md 2026-10-18T17:44Z, M2_STATUS.md 2026-10-18T18:20:08Z). The only Qwen3-VL captions in the project are B1 step-1 outputs on KTVIC dev300 (Section 13). Times are UTC.
- **Machine-readable companion:** `manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.json`. Every hash, count and pinned value below is read from that file, which the builder computes from the sources.
- **Authority:** G2 section 4 'Pre-registration' (predictions P1-P4, kill rules K1-K3); D15 MT19 (scope); H3 section 2 P3 and section 3 (extension, language guard, N1 stop rule); PD-4 Q6 and PD-6 Q3 (G2-B in the GPU order); PD-6 Q1(a) (ownership); CC-007 (binding note); PD-2 Q5 (dev300 guard). Hashes in Section 14.

## 1. What this registers

G2-B repeats the frontier measurement of Paper A Section 7 with a second backbone, `Qwen/Qwen3-VL-8B-Instruct`, used zero-shot. A ladder of three temperatures and two Vietnamese prompts is decoded on the three image sets of Paper A Section 7.6: CV295 (COCO val2017 images of the COCO probe), UV231 (UIT-ViIC test) and XM600 (XM3600 evaluation subset). As CC-007 requires, the registered claims are the ordering of the verbosity slope by gold completeness and its two endpoints. The sign of the slope under multi-reference gold is not predicted.

Not registered here:
- KTVIC runs: Paper B owns KTVIC numbers (PD-6 Q1(a)); D15 also allowed KTVIC test/dev300, but nothing on KTVIC is decoded or analysed under this registration.
- the C3 kappa (two-gold transfer) tests of H3 section 2 P3: Paper B owns C3 (PD-6 Q1(a)).
- any claim that one backbone is better (S0 contamination and MDE argument; D13(ii)).

## 2. Model

- Hub id `Qwen/Qwen3-VL-8B-Instruct`, revision `0c351dd01ed87e9c1b53cbc748cba10e6187ff3b`, licence Apache-2.0, 17,545,915,883 bytes of weights (from `manuscript/prereg/2026-10-14_b1_qwen3vl_predictions.json`).
- Checksum manifest: `.session_backup/2026-10-13/research_r9/C8_backbone/SHA256SUMS`, sha256 `dc7bd4a45eb3c56e00c56f68cd937871258b679b741949bd38a383950ffc52d8`, 14 entries. It equals the manifest pinned by the B1 and S0 preregistrations, and its four shard hashes equal B1's `weight_shards_sha256`.
- On the machine: snapshot `/root/ncs-data/models/Qwen3-VL-8B-Instruct-0c351dd`. Before decoding, the job checks that the snapshot's `SHA256SUMS` has the sha256 above and that `sha256sum -c SHA256SUMS` passes.
- Environment: a separate venv as pinned by B1 (torch 2.5.1+cu121, torchvision 0.20.1+cu121, transformers 4.57.6, accelerate 1.15.0; Python 3.10.12); pip freeze sha256 `bf152944ea4389f609207c5f9589c214b2ff6a4ae3b2e2a9c877e64a57fbe605` (local copy `.session_backup/2026-10-13/research_r9/C8_backbone/FREEZE.txt`). The listed packages must have these versions (KD); any other freeze difference is recorded and reported as a deviation.

| Shard | sha256 |
|---|---|
| model-00001-of-00004.safetensors | `d5d0aef0eb170fc7453a296c43c0849a56f510555d3588e4fd662bb35490aefa` |
| model-00002-of-00004.safetensors | `8be88fb5501e4d5719a6d4cc212e6a13480330e74f3e8c77daa1a68f199106b5` |
| model-00003-of-00004.safetensors | `83de00eafe6e0d57ccd009dbcf71c9974d74df2f016c27afb7e95aafd16b2192` |
| model-00004-of-00004.safetensors | `0a88b98e9f96270973f567e6a2c103ede6ccdf915ca3075e21c755604d0377a5` |

## 3. Decoding

- Model: `Qwen3VLForConditionalGeneration.from_pretrained(snapshot, attn_implementation='sdpa', device_map={'': 0}, **dtype_kwarg(torch.bfloat16))`.
- Processor: `AutoProcessor.from_pretrained(snapshot, min_pixels=262144, max_pixels=1048576)`.
- Input: [{'role': 'user', 'content': [{'type': 'image'}, {'type': 'text', 'text': PROMPTS[mode]}]}]; apply_chat_template(tokenize=False, add_generation_prompt=True); processor(text=[text], images=[PIL.Image.open(path).convert('RGB')], return_tensors='pt').
- New tokens: short 60, short_en 60, detailed 160, detailed_en 160 (B1 step-1 decoding).
- Greedy rungs: `model.generate(**inputs, max_new_tokens=n, do_sample=False)` (T = 0; the call of coco_probe.generate and of B1 step 1).
- Sampled rungs and the sample pool: `model.generate(**inputs, max_new_tokens=n, do_sample=True, temperature=T, top_p=0.95, top_k=0, num_return_sequences=k)` (the call of e5_sample.py; k = sequences_per_image; every other generation setting comes from the snapshot's pinned generation_config.json).
- Seed: torch.manual_seed(42) once, before the first image of each sampled run; images in id order.
- Text: processor.batch_decode(ids[:, input_len:], skip_special_tokens=True), each stripped.
- Check: sha256 of SHA256SUMS in the snapshot equals model.checksum_manifest.sha256, then sha256sum -c SHA256SUMS passes.
- Check: the venv pip freeze sha256 is recorded; torch, torchvision, transformers, accelerate must have the versions of model.venv.packages (otherwise KD); any other difference from model.venv.freeze_sha256 is recorded and reported as a deviation, and the outputs still test this registration.
- Check: every image of the run exists; a sha256 list of the decoded image files is written per dataset. CV295 decodes the COCO-2014 files named in data/coco_probe/manifest.json; UV231 and XM600 decode the files named in their test_data.json.
- Every output records: prereg_id, run_id, machine_id, git_head, hook_sha256, job_sha256, venv_freeze_sha256, backbone, revision, dataset, prompt_mode, temperature, top_p, top_k, seed, max_new_tokens, sequences_per_image, n_images, started_utc, finished_utc.
- `preds.json`: provenance fields + 'predictions': {image_id: caption}.
- `samples.jsonl`: first line provenance; then one line per image: {'image_id': id, 'samples': [...]}.
- `sidecar`: <output>.sha256 per file (GPU job plan rule).

Prompts (`scripts/evaluate.py` `PROMPTS`):

| Mode | Text | sha256 (16) |
|---|---|---|
| `short` | Mô tả bức ảnh này bằng MỘT câu tiếng Việt ngắn gọn, giống chú thích ảnh. Không liệt kê, không giải thích. | `8870589c4a32307c` |
| `detailed` | Mô tả chi tiết bức ảnh này bằng tiếng Việt. | `0addb5dd720e4f24` |
| `short_en` | Describe this image in ONE short English sentence, like a caption. Do not list items or explain. | `0cdbdf77fae4c04b` |
| `detailed_en` | Describe this image in detail in English. | `525a4e1bf5849e2c` |

Runs (23), in queue order:

| Run | Set | Prompt | T | Captions per image |
|---|---|---|---|---|
| `g2b_q3_cv295-short-T0` | cv295 | short | 0.0 | 1 |
| `g2b_q3_cv295-detailed-T0` | cv295 | detailed | 0.0 | 1 |
| `g2b_q3_uv231-short-T0` | uv231 | short | 0.0 | 1 |
| `g2b_q3_uv231-detailed-T0` | uv231 | detailed | 0.0 | 1 |
| `g2b_q3_xm600-short-T0` | xm600 | short | 0.0 | 1 |
| `g2b_q3_xm600-detailed-T0` | xm600 | detailed | 0.0 | 1 |
| `g2b_q3_cv295-short-T05` | cv295 | short | 0.5 | 1 |
| `g2b_q3_cv295-detailed-T05` | cv295 | detailed | 0.5 | 1 |
| `g2b_q3_uv231-short-T05` | uv231 | short | 0.5 | 1 |
| `g2b_q3_uv231-detailed-T05` | uv231 | detailed | 0.5 | 1 |
| `g2b_q3_xm600-short-T05` | xm600 | short | 0.5 | 1 |
| `g2b_q3_xm600-detailed-T05` | xm600 | detailed | 0.5 | 1 |
| `g2b_q3_cv295-short-T08` | cv295 | short | 0.8 | 1 |
| `g2b_q3_cv295-detailed-T08` | cv295 | detailed | 0.8 | 1 |
| `g2b_q3_uv231-short-T08` | uv231 | short | 0.8 | 1 |
| `g2b_q3_uv231-detailed-T08` | uv231 | detailed | 0.8 | 1 |
| `g2b_q3_xm600-short-T08` | xm600 | short | 0.8 | 1 |
| `g2b_q3_xm600-detailed-T08` | xm600 | detailed | 0.8 | 1 |
| `g2b_q3_cv295-short_en-T0` | cv295 | short_en | 0.0 | 1 |
| `g2b_q3_cv295-detailed_en-T0` | cv295 | detailed_en | 0.0 | 1 |
| `g2b_q3_uv231-short_en-T0` | uv231 | short_en | 0.0 | 1 |
| `g2b_q3_uv231-detailed_en-T0` | uv231 | detailed_en | 0.0 | 1 |
| `g2b_q3_uv231-short-T05x6` | uv231 | short | 0.5 | 6 |

## 4. Image sets and exposure

| Set | Images | Ids | References per image | COCO membership |
|---|---|---|---|---|
| CV295 | 295 | `data/coco_probe/probe_val2017_ids.txt` | 5-6 English (first 5 used) | listed in val2017: 295; COCO-2014 split val2014: 295 |
| UV231 | 231 | `data/datasets/uitviic/test_data.json` | 5 Vietnamese | coco_url folder train2017: 231; COCO-2014 split train2014: 231 |
| XM600 | 600 | `data/xm3600_subset.txt` | Vietnamese; images with 2 references: 573, 3 references: 27 | COCO file names: 0 (Open Images) |

- CV295 ids all in the probe manifest: True; XM600 ids equal the subset file: True.
- Criterion: membership in COCO train2017, the criterion of D15 and the S0 contamination caveat; it is not proof that a backbone never saw an image.
- **Flag (UV231).** D15 MT19 lists UIT-ViIC test among the uncontaminated splits and says G2-B runs with 'zero touch of COCO train2017'. Every UV231 image is a COCO train2017 image (datasets.uv231.coco_url_split, datasets.uv231.coco2014_split), so that premise is wrong for UV231.
- **Handling.** The registered default, for the judge to confirm before the commit: UV231 is decoded and analysed as registered; its FAIL outcomes count toward every kill rule; a PASS on UV231 is not counted as support from images outside COCO train2017; Paper A labels UV231 results 'COCO train2017 images; exposure during pre-training possible'. The Paper A Section 7.6 phrase 'images outside the backbone's likely COCO training overlap' must not include UIT-ViIC test (for the A-writer; this file does not edit drafts).

## 5. Gold levels and matchers

**CV295.** One reference `refs1_randk`, all references `refs_all`, complete gold `inst`. References: English Karpathy sentences of the image, first 5 in file order.
- `refs1_randk`: union of 1 of the image's first 5 references, drawn without replacement; mean over the random subsets.
- `refs2_randk`: union of 2 of the image's first 5 references, drawn without replacement; mean over the random subsets.
- `refs3_randk`: union of 3 of the image's first 5 references, drawn without replacement; mean over the random subsets.
- `refs4_randk`: union of 4 of the image's first 5 references, drawn without replacement; mean over the random subsets.
- `refs_all`: union of the first 5 references (refs5).
- `inst`: COCO-2014 instance classes (complete gold).
- `inst+refs_all`: instance classes union refs_all (descriptive only).
- instance: `data/coco_probe/instance_gold.json [cocoid]['coco']`.
- matcher vi outputs: `score_coco_probe.vi_objects(caption, load_vi_terms())`.
- matcher en outputs: `score_coco_probe.en_classes(caption, load_synonyms())`.
- matcher references: `score_coco_probe.en_classes(sentence, load_synonyms())`.

**UV231.** One reference `refs1_randk`, all references `refs_all`, complete gold `inst`. References: Vietnamese UIT-ViIC references, first 5 in file order.
- `refs1_randk`: union of 1 of the image's first 5 references, drawn without replacement; mean over the random subsets.
- `refs2_randk`: union of 2 of the image's first 5 references, drawn without replacement; mean over the random subsets.
- `refs3_randk`: union of 3 of the image's first 5 references, drawn without replacement; mean over the random subsets.
- `refs4_randk`: union of 4 of the image's first 5 references, drawn without replacement; mean over the random subsets.
- `refs_all`: union of the first 5 references (refs5).
- `inst`: COCO-2014 instance classes (complete gold).
- `inst+refs_all`: instance classes union refs_all (descriptive only).
- Lexicon coco80 (primary): outputs_vi `score_coco_probe.vi_objects`; outputs_en `score_coco_probe.en_classes`; references `score_coco_probe.vi_objects`; instance `data/uitviic/instance_gold.json [id]['coco']`.
- Lexicon vi_objects_in (secondary; Vietnamese outputs only): outputs_vi `rescap.chair.objects_in`; references `rescap.chair.objects_in`; instance `union of objects_in(name) over data/uitviic/instance_gold.json [id]['vi']`.

**XM600.** One reference `refs1_randk`, all references `refs_all`, complete gold `oiv7_verified`. References: Vietnamese XM3600 references (2-3 per image).
- `refs1_randk`: one of the image's 2-3 references, drawn at random; mean over the random draws.
- `refs_all`: union of all 2-3 references.
- `oiv7_verified`: OIV7 human-verified labels on the mapped lexicon classes (complete gold).
- matcher: `rescap.chair.objects_in (outputs and references)`.
- oiv7: `xm3600_oiv7.statuses(resolve_map(oidv7-class-descriptions.csv), oiv7_labels); P = verified precision over verified mapped mentions, R = recall over verified-present classes (micro), F1 = 2PR/(P+R) (F1_pos of evaluate_xm3600_predictions_v3); M on the x-axis = mentions per caption under objects_in`.

## 6. Families

`Q25_GREEDY` is Qwen2.5-VL-7B-Instruct zero-shot greedy (existing outputs, Section 14); `VOTE` is the mention sets named by at least t of the pool's samples (g2_frontier.pool_points `vote>=t`).

| Set | Family | Members |
|---|---|---|
| CV295 | LADDER | `g2b_q3_cv295-short-T0`, `g2b_q3_cv295-detailed-T0`, `g2b_q3_cv295-short-T05`, `g2b_q3_cv295-detailed-T05`, `g2b_q3_cv295-short-T08`, `g2b_q3_cv295-detailed-T08` |
| CV295 | GREEDY_VI | `g2b_q3_cv295-short-T0`, `g2b_q3_cv295-detailed-T0` |
| CV295 | T05_PAIR | `g2b_q3_cv295-short-T05`, `g2b_q3_cv295-detailed-T05` |
| CV295 | T08_PAIR | `g2b_q3_cv295-short-T08`, `g2b_q3_cv295-detailed-T08` |
| CV295 | Q25_GREEDY | `data/results/coco5000/zeroshot-short.shard0of1.jsonl`, `data/results/coco5000/zeroshot-detailed.shard0of1.jsonl` |
| CV295 | GREEDY_EN | `g2b_q3_cv295-short_en-T0`, `g2b_q3_cv295-detailed_en-T0` |
| UV231 | LADDER | `g2b_q3_uv231-short-T0`, `g2b_q3_uv231-detailed-T0`, `g2b_q3_uv231-short-T05`, `g2b_q3_uv231-detailed-T05`, `g2b_q3_uv231-short-T08`, `g2b_q3_uv231-detailed-T08` |
| UV231 | GREEDY_VI | `g2b_q3_uv231-short-T0`, `g2b_q3_uv231-detailed-T0` |
| UV231 | T05_PAIR | `g2b_q3_uv231-short-T05`, `g2b_q3_uv231-detailed-T05` |
| UV231 | T08_PAIR | `g2b_q3_uv231-short-T08`, `g2b_q3_uv231-detailed-T08` |
| UV231 | Q25_GREEDY | `data/results/uitviic/uitviic_zeroshot-short.preds.json`, `data/results/uitviic/uitviic_zeroshot-detailed.preds.json` |
| UV231 | GREEDY_EN | `g2b_q3_uv231-short_en-T0`, `g2b_q3_uv231-detailed_en-T0` |
| UV231 | VOTE | `g2b_q3_uv231-short-T05x6:vote>=1`, `g2b_q3_uv231-short-T05x6:vote>=2`, `g2b_q3_uv231-short-T05x6:vote>=3`, `g2b_q3_uv231-short-T05x6:vote>=4`, `g2b_q3_uv231-short-T05x6:vote>=5`, `g2b_q3_uv231-short-T05x6:vote>=6` |
| XM600 | LADDER | `g2b_q3_xm600-short-T0`, `g2b_q3_xm600-detailed-T0`, `g2b_q3_xm600-short-T05`, `g2b_q3_xm600-detailed-T05`, `g2b_q3_xm600-short-T08`, `g2b_q3_xm600-detailed-T08` |
| XM600 | GREEDY_VI | `g2b_q3_xm600-short-T0`, `g2b_q3_xm600-detailed-T0` |
| XM600 | T05_PAIR | `g2b_q3_xm600-short-T05`, `g2b_q3_xm600-detailed-T05` |
| XM600 | T08_PAIR | `g2b_q3_xm600-short-T08`, `g2b_q3_xm600-detailed-T08` |
| XM600 | Q25_GREEDY | `data/results/xm3600/xm3600_zeroshot-short.preds.json`, `data/results/xm3600/xm3600_zeroshot-detailed.preds.json` |

## 7. Analysis plan

- **Analysis sets.** An analysis is one prediction on one dataset (all its parts), one kill-rule check or one descriptive table; its systems are the union of the families it names (analysis_set_families). Each analysis uses its clean subset: the images for which every caption of every one of its systems is clean. A Vietnamese caption is clean if rescap.vlm.mock.looks_vietnamese is true and clean_supervision.CJK_RE finds no match; an English caption is clean if CJK_RE finds no match; a sample pool is clean if all its samples are clean. Images missing from any run of the analysis are dropped from it. Verdicts use clean subsets only (H3 section 2 P3: score only the clean subset and say so). The same statistics on all images are reported as a sensitivity analysis, without verdicts. The clean-subset size of every analysis is reported.
- **Systems of each analysis.** G2B-E1, G2B-E2, G2B-O1, G2B-P1, G2B-NS, G2B-O2, G2B-P3b, K3, descriptive LADDER tables: LADDER; G2B-P2: GREEDY_VI + GREEDY_EN; G2B-P3a: GREEDY_VI + VOTE (its sample pool); G2B-P4: GREEDY_VI + Q25_GREEDY.
- **Inputs.** The evaluator reads the backup copies under .session_backup/machines/<machine>/root/outputs/g2b_qwen3vl/ and checks each against its .sha256 sidecar first.
- **Random reference subsets.** numpy.random.default_rng(1); for k = 1..K (K = 4 on cv295 and uv231, 1 on xm600), for r = 1..20, for each image of the FULL dataset in id order: choice(n_refs_image, k, replace=False). Drawn once per dataset, before any output is read, then restricted to the analysis set.
- **Bootstrap.** 1000 image-bootstrap draws per analysis set: numpy.random.default_rng(0).multinomial(N, [1/N]*N, size=1000) over the set's images in id order, shared by every system, gold and family of the analysis (paired). 95% CI = percentiles 2.5 and 97.5 of the replicates.
- **Per-system scores.** For system x, gold variant g with subsets s = 1..S (S = n_random_subsets for *_randk, else 1) and image weights w over the analysis set: TP_xs = sum_i w_i |m_xi & G_is|; Mtot_x = sum_i w_i |m_xi|; P_xs = TP_xs / Mtot_x; R_xs = mean over images with non-empty G_is of |m_xi & G_is| / |G_is| (w-weighted); F_xs = 2 P R / (P + R), 0 if P + R = 0. P_x, R_x, F_x = means over s; M_x = Mtot_x / sum_i w_i; TPbar_x = P_x * M_x (check_mstar.prf, mixed F1). For oiv7_verified, P, R and F1 are the OIV7 quantities of the gold definition (verified precision, micro recall over verified-present classes, F1_pos), w-weighted, and TPbar_x = P_x * M_x with M_x from objects_in.
- `slope[g](F)`: OLS slope of 100 * F_x on ln M_x over the systems x of family F (check_mstar.slope).
- `b[g](F)`: OLS slope of ln max(TPbar_x, 1e-09) on ln M_x over F (check_mstar.mstar b; two systems give the two-point slope).
- `res[g](y | F)`: 100 * P_y - 100 * exp(a_F) * M_y ** (b_F - 1), with (a_F, b_F) the OLS fit of ln TPbar on ln M over F (g2_frontier.fit residual, in precision points).
- `mres[g](Y | F)`: mean of res[g](y | F) over the systems y of Y.
- `rmse[g](F)`: sqrt(mean over x in F of res[g](x | F) ** 2), point estimate (g2_frontier rmse_ols_P).
- `differences`: a difference of two statistics is computed on the same bootstrap draw (paired).
- Descriptive outputs (no verdict): per system and gold: P, R, F1, M and TPbar with CIs; slope[g](LADDER) and b[g](LADDER) for every gold variant, with CIs, including the multi-reference golds whose sign is not predicted (CC-007); M*_mixed and sign(slope) vs sign(M*_mixed - median M) per gold (check_mstar.mstar): a goodness-of-fit check, not a prediction (H3 section 1a: close to built in); every registered statistic on all images (sensitivity), and on the uv231 secondary lexicon; clean-subset sizes; share of captions failing each guard, per run.
- **Evaluator.** Written after this registration, against Sections 'analysis_plan' and 'predictions'. It reuses the pinned matchers unchanged and reproduces the conventions of the pinned reference implementations. Its sha256 goes into its results JSON; it is committed through the gatekeeper before its results file exists (CHECKLIST C3).

## 8. Verdict rules

- `sign_gt_0`: PASS if ci95_lo > 0; FAIL if point <= 0; else INCONCLUSIVE
- `sign_lt_0`: PASS if ci95_hi < 0; FAIL if point >= 0; else INCONCLUSIVE
- `equiv_abs_le`: PASS if -delta <= ci95_lo and ci95_hi <= delta; FAIL if ci95_hi < -delta or ci95_lo > delta; else INCONCLUSIVE
- `diff_abs_gt`: PASS if ci95_lo > delta or ci95_hi < -delta; FAIL if -delta <= ci95_lo and ci95_hi <= delta; else INCONCLUSIVE
- `compound`: FAIL if any part is FAIL; else NOT_EVALUABLE if any part is NOT_EVALUABLE; else PASS if every part is PASS; else INCONCLUSIVE
- `not_evaluable`: NOT_EVALUABLE if the analysis set is empty or a statistic is undefined (a system with M_x = 0, or fewer than 2 distinct M_x in a family)
- `counting`: Kill rules count FAIL only. INCONCLUSIVE is reported as inconclusive and never as support. Earlier preregistrations scored sign and ordering claims on point estimates; 'not FAIL' here is that criterion, so the outcomes can be compared.
- `multiplicity`: No correction; every prediction is reported separately, per dataset, with its CI.

## 9. Frozen predictions

Family `LADDER` unless stated; primary lexicon on UV231 (the secondary lexicon repeats E1, E2, O1, O2 and P1 as secondary results that no kill rule counts).

| ID | Tier | Sets | Claim | Statistic and rule | Source |
|---|---|---|---|---|---|
| **G2B-E1** | primary | cv295, uv231, xm600 | one-reference endpoint: the verbosity slope is negative under one random reference (the empirical half of N1; Paper A does not derive this sign from Proposition 1) | `slope[refs1_randk](LADDER)` sign_lt_0 | CC-007 binding note; H3 section 2 P3; H3 section 3 (KN1) |
| **G2B-E2** | primary | cv295, uv231, xm600 | complete-gold endpoint: the verbosity slope is positive under the complete gold (the large-gold endpoint of Proposition 1) | `slope[complete](LADDER)` sign_gt_0 | CC-007 binding note; H3 section 2 P3 |
| **G2B-O1** | primary | cv295, uv231, xm600 | ordering (Proposition 1): slope(one reference) < slope(all references) < slope(complete gold) | `slope[refs_all](LADDER) - slope[refs1_randk](LADDER)` sign_gt_0; `slope[complete](LADDER) - slope[refs_all](LADDER)` sign_gt_0 | CC-007 binding note; H3 section 2 P3 |
| **G2B-P1** | primary | cv295, uv231, xm600 | exponent ordering: b(all references) - b(one reference) > 0 and b(complete) > b(all references) | `b[refs_all](LADDER) - b[refs1_randk](LADDER)` sign_gt_0; `b[complete](LADDER) - b[refs_all](LADDER)` sign_gt_0 | G2 section 4 P1 |
| **G2B-NS** | not predicted | cv295, uv231, xm600 | the sign of slope[refs_all](LADDER) and of slope[refsK_randk](LADDER), K >= 2, is NOT predicted; it is reported with its CI only | reported, no verdict | CC-007 binding note |
| **G2B-O2** | secondary | cv295, uv231 | the verbosity slope rises at every added reference, k = 1..5 | `slope[refs2_randk](LADDER) - slope[refs1_randk](LADDER)` sign_gt_0; `slope[refs3_randk](LADDER) - slope[refs2_randk](LADDER)` sign_gt_0; `slope[refs4_randk](LADDER) - slope[refs3_randk](LADDER)` sign_gt_0; `slope[refs_all](LADDER) - slope[refs4_randk](LADDER)` sign_gt_0 | H3 P6 and COCO-2500 P1 (k-step form) |
| **G2B-P2** | secondary | cv295, uv231 | language-free exponent: |b_EN - b_VI| <= 0.05 under the complete gold | `b[complete](GREEDY_EN) - b[complete](GREEDY_VI)` equiv_abs_le (delta 0.05) | G2 section 4 P2 |
| **G2B-P3a** | secondary | uv231 | vote family vs greedy prompt family: |b difference| <= 0.05 under the complete gold | `b[complete](VOTE) - b[complete](GREEDY_VI)` equiv_abs_le (delta 0.05) | G2 section 4 P3 |
| **G2B-P3b** | secondary | cv295, uv231, xm600 | temperature leaves the exponent within 0.05 and lowers the T=0.8 intercept (complete gold) | `b[complete](T05_PAIR) - b[complete](GREEDY_VI)` equiv_abs_le (delta 0.05); `b[complete](T08_PAIR) - b[complete](GREEDY_VI)` equiv_abs_le (delta 0.05); `mres[complete](T08_PAIR | GREEDY_VI)` sign_lt_0 | G2 H3; D15 MT19 (ladder rationale) |
| **G2B-P4** | secondary | cv295, uv231, xm600 | backbones share the exponent within 0.05 but differ in intercept by more than 2 precision points at matched M (complete gold; Qwen2.5-VL-7B zero-shot comparator) | `b[complete](GREEDY_VI) - b[complete](Q25_GREEDY)` equiv_abs_le (delta 0.05); `mres[complete](GREEDY_VI | Q25_GREEDY)` diff_abs_gt (delta 2) | G2 section 4 P4 |

## 10. Kill rules

| ID | Fires when | Consequence | Source |
|---|---|---|---|
| **K1** | G2B-P1 is FAIL on 2 or more of the 3 datasets (uv231 counts; primary lexicon) | Section 7.6 drops the completeness account for this backbone and reports only that the exponent is dataset-specific | G2 section 4 K1 |
| **K2** | G2B-P2 is FAIL on both cv295 and uv231. G2's K2 counts backbones (2 or more of 3); here one backbone has English outputs, so K2 cannot be evaluated as written | Section 7.6 reports the exponent per language for Qwen3-VL-8B | G2 section 4 K2 (restricted form) |
| **K3** | rmse[g](LADDER) > 3 precision points (point estimate) for a gold variant g of a dataset (Section 5 variants, primary lexicon) | for that dataset and gold the frontier is reported only as a local linearisation around its operating range: no extrapolated frontier value and no M* reading | G2 section 4 K3 |
| **KN1** | G2B-E1 is FAIL (one-reference slope >= 0) on any dataset (uv231 counts) | the sign-flip claim (N1) is dropped from Paper A; only the ordering result can remain | H3 section 3; XM3600 prereg kill_rule.h3_p2_r11_stop_rule; Paper A section 7.6 |
| **KL** | always applied: verdicts are computed on clean subsets only | Section 7.6 states that only clean captions were scored and gives the clean-subset sizes | H3 section 2 P3 (language guard); PD-2 Q5 |
| **KD** | a run whose provenance shows a model file, prompt, decoding setting (Section 3), pinned package version or pinned instrument different from this registration | the run does not test this registration; it is reported as a deviation and left out of every verdict | this registration |

## 11. How Paper A Section 7.6 reports the outcome

- Table 7.1 gets one row per image set for this backbone: the `LADDER` slope at one reference, all references and the complete gold, with CIs, on clean subsets, graded 'frozen'; the all-references cell says that its sign was not predicted.
- Every registered verdict is quoted as the evaluator computed it (PASS, FAIL, INCONCLUSIVE or NOT_EVALUABLE), failures included, with the clean-subset sizes.
- 'Replicates on a second backbone' may be written only for CV295 and XM600, and only where G2B-E1, G2B-E2 and G2B-O1 all PASS. UV231 outcomes are reported with the exposure label of Section 4.
- Kill-rule consequences are applied as written, and the text says which rules fired.
- Full-set (sensitivity) numbers are never presented as verdicts.

## 12. Departures from the source plans

- KTVIC is left out (D15 and H3 section 2 P3 include KTVIC test/dev300): Paper B owns KTVIC numbers (PD-6 Q1(a)), and Paper A Section 7.6 names only CV295, UIT-ViIC test and XM3600.
- the T=0.5 sample pool is decoded on UV231 only (H3 section 2 P3: on KTVIC and UV231), because KTVIC is left out.
- the C3 kappa tests of H3 section 2 P3 are left out: Paper B owns C3 (PD-6 Q1(a)).
- the English arm is the greedy short/detailed pair of this backbone on CV295 and UV231 (G2 section 4 planned English and Vietnamese prompt families for three backbones); XM600 has no English-to-OIV7 class map, so it has no English arm.
- K2 is evaluated in a restricted form, because only one backbone has English outputs.
- clean-subset scoring is applied in every case (H3 section 2 P3 makes it conditional on a failed dev300 language guard).
- every sign and ordering claim, including the second part of G2 P1 (b(instance) > b(5 refs), stated there without an interval), is scored with the three-way rule of Section 8.
- G2B-P3b (temperature ladder) is added from G2's H3 and the D15 MT19 rationale for the ladder; G2 section 4 P3 itself is G2B-P3a.
- UV231 handling: D15's 'uncontaminated' premise does not hold for UV231 (Section 4).

## 13. What the author saw before registering

- Paper A Section 7 (with the Table 7.1 slopes of the Qwen2.5-VL-7B families on these image sets), the G2 and H3 reports, D15, PD-2, PD-4, PD-6, CC-007, and the XM3600, B1 and S0 preregistrations.
- The B1 step-1 summary `data/results/b1_qwen3vl/step1_dev300_guard.json` (sha256 `c728db659a191268`): language-guard rates, object scores and mentions per caption of Qwen3-VL-8B zero-shot (greedy, the same two prompts) on KTVIC dev300. It is a Paper B file and no number from it is used here. By B1's thresholds its language guard short fails, detailed passes (computed by the builder; rule: vietnamese_share >= vietnamese_share_min and cjk_rate <= cjk_rate_max (B1 thresholds)). Under H3 section 2 P3 a failed dev300 language guard sends G2-B to clean-subset scoring; this registration scores clean subsets in every case (KL), so no analysis choice depends on that outcome.
- The content of every prediction comes from G2 section 4, H3 section 2 P3 and the list in Paper A Section 7.6, with CC-007 removing the multi-reference sign. Their operational form (families, verdict rules, the P3b and P4 statistics, clean-subset scoring, the UV231 handling) was written after reading the B1 summary; none of these choices uses a number from it.
- Existing Qwen3-VL caption files (B1, KTVIC dev300; not opened): `data/results/b1_qwen3vl/b1_qwen3vl_zs-dev300-detailed.preds.json`, `data/results/b1_qwen3vl/b1_qwen3vl_zs-dev300-short.preds.json`.
- While checking file formats, the first lines of one existing Qwen2.5-VL-7B zero-shot COCO caption file were displayed. No Qwen3-VL caption of a CV295, UV231 or XM600 image exists.

## 14. Frozen inputs, instruments and sources

A file tracked in git is pinned by its blob at the HEAD of the build (the version a machine at that HEAD runs); the last column says whether the working tree differs. Other files are pinned by their bytes on disk.

**Sources**

| File | sha256 | Git (last commit) | Role | Working tree |
|---|---|---|---|---|
| `manuscript/research_r10/G2/REPORT.txt` | `1751952ee71d4f96bbc1c7d0b5d937a905fb67273739f00fff1c388892146e4d` | 6c647a6 2026-10-14T14:01:40+07:00 | G2 report; section 4 'Pre-registration' (P1-P4, K1-K3) | equals HEAD |
| `manuscript/research_r12/H3/REPORT.txt` | `626fef8cbddddd6253dc551be183ae0d8b42eb34cefc4f5a2addc9be00a3b3c3` | b7aa8af 2026-10-14T22:26:25+07:00 | H3 report; section 2 P3 (G2-B+), section 3 (N1 stop rule) | equals HEAD |
| `manuscript/journal_draft/sec7_verbosity_sign.md` | `88496cea18a7a60dd646330197f91847a832f4c5a57e79bdfa2e7a9eb5a036a3` | 5a81b8d 2026-10-15T08:47:52+07:00 | Paper A section 7.6 placeholder | differs from HEAD (disk sha256 9713daa538e27e8a3eb6851e634ebbe339a2ca8a7d8be673f6841b3d6db35b8a) |
| `.session_backup/2026-10-13/decisions/D15.txt` | `10f929349bdf20641007ef91667b6eee55337d0caffa2816b4ce922d775608b9` | not in git (git-excluded or untracked) | judge D15, MT19: G2-B scope | n/a |
| `.session_backup/2026-10-13/decisions/PD-2.txt` | `ff23ade0884a3dde58be0e905e9af77cccf5b7adcd739208398daa59a3fa5578` | not in git (git-excluded or untracked) | judge PD-2, Q5: zero-shot dev300 guard | n/a |
| `.session_backup/2026-10-13/decisions/PD-4.txt` | `16cc01b0d72288a832d8c519e2b38ada6b98649c5fd2af9b9b9be3bc264d26b0` | not in git (git-excluded or untracked) | judge PD-4, Q6: GPU order | n/a |
| `.session_backup/2026-10-13/decisions/PD-6.txt` | `2c48d6491af85ae5d8b2fe279e0c49a14d0f59b6fc547061ae2c3cdea79dad22` | not in git (git-excluded or untracked) | judge PD-6, Q1(a) ownership, Q3 G2-B extended | n/a |
| `.session_backup/2026-10-13/decisions/CC-007.txt` | `e2b2967cdba3aca6e08f71933c5004f5109ad36217e7f05785471e637a8b926b` | not in git (git-excluded or untracked) | judge CC-007, binding note on the multi-reference sign | n/a |
| `manuscript/prereg/2026-10-14_xm3600_predictions.md` | `1dfaeb0f6d1bc10f662622a56a1c29538f16dc200b08f550584ba6b543984cc8` | 4ccbee3 2026-10-14T23:38:04+07:00 | format template; N1 kill rules | equals HEAD |
| `manuscript/prereg/2026-10-14_xm3600_predictions.json` | `5d0134bfded091d47153226c427ceb8ee29fe8b2a698daf8d533d8365fb5dc32` | 4ccbee3 2026-10-14T23:38:04+07:00 | format template; N1 kill rules | equals HEAD |
| `manuscript/prereg/2026-10-14_b1_qwen3vl_predictions.json` | `31f77dd5df4d718d1e22c6e9d92e5ddf3c8d69cf8351a1c06652a6bb614939a6` | 16795cd 2026-10-14T23:57:52+07:00 | model pin, decoding, guard | equals HEAD |
| `manuscript/prereg/2026-10-13_s0_qwen3vl.md` | `a9c616ca06503413224466d71d674c7655da0c371a1646b3ceb2c82f86ed69b8` | 4592d69 2026-10-14T06:47:31+07:00 | model pin; val2017 subset | equals HEAD |
| `.session_backup/2026-10-18/gpu_jobs/GPU_JOB_PLAN_v1.md` | `9a8ae864fc2a393ea9d35c75e4ce4578d84e298f90ad4c7d81c07ce1d40bcba3` | not in git (git-excluded or untracked) | M2 queue item 7 | n/a |

**Instruments**

| File | sha256 | Git (last commit) | Role | Working tree |
|---|---|---|---|---|
| `scripts/evaluate.py` | `a68d56826d90d8a409493cd6f49007e906c6cb4f5668314edb9b8e7a632e8236` | d4de7b0 2026-10-12T19:24:19+07:00 | PROMPTS: the four prompt texts | equals HEAD |
| `scripts/coco_probe.py` | `930a3899e229e22a1b9326951210e49da3be2904cecd1a4214f02ac8b261ebb8` | 4592d69 2026-10-14T06:47:31+07:00 | greedy Qwen3-VL decode call (generate, do_sample=False) | equals HEAD |
| `scripts/e5_sample.py` | `35ec0d26622ac87138773d00454cd858e6e7fe7cda51217d0b0a2bbcc460baef` | a94fd5b 2026-10-12T11:16:45+07:00 | sampling call (temperature, top_p, top_k=0, seed) | equals HEAD |
| `scripts/score_coco_probe.py` | `d11db7e192f689980bb2b2bb717d852d9aa339ad857ce9411fe7bdd6fe416070` | a0accb5 2026-10-14T06:47:37+07:00 | COCO-80 matchers: vi_objects/load_vi_terms (vi), en_classes/load_synonyms (en) | equals HEAD |
| `data/coco_probe/coco80_vi.json` | `926e08571ef6e80a7f8aae8f2b73753d6c5c54c431a750ba2b67bfaae71b540b` | ee7cad1 2026-10-12T14:33:16+07:00 | Vietnamese COCO-80 lexicon (load_vi_terms) | equals HEAD |
| `data/coco_probe/chair_synonyms.txt` | `b685537b36fe21b791c87151b96a991ceb582edff19f3da204dcc7a7905502f2` | 1f30d09 2026-08-30T10:06:13+07:00 | English synonyms (load_synonyms) | equals HEAD |
| `rescap/chair.py` | `e47d249ac7290070f2387d3fa8b22dac77728265ad276f55aa6520f5cbc591a3` | a0accb5 2026-10-14T06:47:37+07:00 | objects_in: 113-entry Vietnamese lexicon, tone-normalised by default | equals HEAD |
| `scripts/xm3600_oiv7.py` | `9a79403f4fc38609282d40082ab7f878133edca8aff9e0dc2462db467b7193f0` | e564ed6 2026-10-12T16:46:56+07:00 | resolve_map, statuses, caption_rows: OIV7 verified labels | equals HEAD |
| `rescap/vlm/mock.py` | `33793de01b4f2790964342b1af2d4c2de18d793ae4693608283992475ed62ce7` | 1f30d09 2026-08-30T10:06:13+07:00 | looks_vietnamese (language guard) | equals HEAD |
| `rescap/vlm/base.py` | `e8fee5bc5b729534af67c6e462a27f0d83ba611f18ff8e3f2717b11eb393ae93` | 1f30d09 2026-08-30T10:06:13+07:00 | dtype_kwarg (bf16 loading, as in B1 step 1) | equals HEAD |
| `scripts/clean_supervision.py` | `01f172002a607ba9ee55bccb332439f10650832cae1f64a9b74b35c48cd9c231` | 93070e1 2026-10-10T13:48:37+07:00 | CJK_RE (CJK guard) | equals HEAD |
| `scripts/abs_halluc.py` | `76819c8e1c439cce2c5651e50e2a86d28078c2cbb67db22bc6327401bbcfc481` | a0accb5 2026-10-14T06:47:37+07:00 | CJK (re-export of CJK_RE) | equals HEAD |

**Reference implementations**

| File | sha256 | Git (last commit) | Role | Working tree |
|---|---|---|---|---|
| `.session_backup/2026-10-14/r11_litmaps/L1/scripts/check_mstar.py` | `6e2c0042ac44fe3e111fd88bc4783cf12c73a54ae938ee0d1802222b3048fb95` | not in git (git-excluded or untracked) | per_image, prf, slope, mstar | n/a |
| `.session_backup/2026-10-14/r11_litmaps/L1/scripts/check_coco.py` | `6acd7f8af318484813d566a127d529387e677c9706d049af2336d4387ca34b00` | not in git (git-excluded or untracked) | COCO gold: first 5 Karpathy refs, en_classes, instances | n/a |
| `.session_backup/2026-10-14/r11_verify/c2_n1_uitviic_mstar.py` | `09a149d42fc2bd117433cecb2fff1ce8ae4b3309dc8f2a9a95e45bc9327be890` | not in git (git-excluded or untracked) | UIT-ViIC gold under both lexicons | n/a |
| `.session_backup/2026-10-14/r12_verify/evaluate_xm3600_predictions_v3.py` | `24356632c1c9b8023d8319de5ebc30b15c517f7f5b3ad7d519eea9c73d2c626d` | not in git (git-excluded or untracked) | XM3600 gold: refs, OIV7 F1_pos, M on objects_in | n/a |
| `.session_backup/2026-10-14/research_r10/G2/g2_frontier.py` | `0ac9198ec742f1f7e28c46573b4d18d0f806e39a66b093c542a20dde18b51649` | not in git (git-excluded or untracked) | fit (b_ols, residuals, rmse_ols_P), pool_points, ci | n/a |

**Data**

| File | sha256 | Git (last commit) | Role | Working tree |
|---|---|---|---|---|
| `data/coco_probe/probe_val2017_ids.txt` | `73f8698901f08e7b1bd53dd2842e77683af41e4e9e19276c3e8e6efba5273453` | 4592d69 2026-10-14T06:47:31+07:00 | CV295 image ids (cocoid) | equals HEAD |
| `data/coco_probe/manifest.json` | `931e572ec8ea5eadf4c49aafcc062a837429b4e6bcc1f96fc0ec0ee1ecaa7e35` | 1f30d09 2026-08-30T10:06:13+07:00 | COCO probe image file names | equals HEAD |
| `data/coco_probe/instance_gold.json` | `963af2c6cc71e7a5e32c2f8f1ca6a0f1ef0a1f02dadf40926ddb05eebd04f81e` | d4de7b0 2026-10-12T19:24:19+07:00 | COCO-2014 instance labels (CV295) | equals HEAD |
| `data/datasets/karpathy/dataset_coco.json` | `2fd999220673258012acfb411a4e7e66af7d488050b2519b0badcc49b7600b8d` | not in git (git-excluded or untracked) | English Karpathy references (CV295) | n/a |
| `.session_backup/2026-10-13/research_r9/C8_backbone/s0/val2017_names.txt` | `612097d209d870b260f9b4cb9c5ccdc32586da617ccf0f25c0627e60f8877285` | not in git (git-excluded or untracked) | COCO val2017 file list | n/a |
| `data/datasets/uitviic/test_data.json` | `54abc0fb068ad1108d7d57b21328d4d68bcf8f41aa168f80ec7c275fb4ac8214` | not in git (git-excluded or untracked) | UV231 images and Vietnamese references | n/a |
| `data/uitviic/instance_gold.json` | `278d15b97e3eeb9496a0282bb91deb365117becf24d174fbb1e0507203b12ea4` | 093cbfc 2026-10-12T11:58:11+07:00 | COCO-2014 instance labels (UV231) | equals HEAD |
| `data/datasets/xm3600/test_data.json` | `0a613214f95605ff137879f70cb84f8160172c28a650317766ac4a1d9c3b72e8` | not in git (git-excluded or untracked) | XM600 images and Vietnamese references | n/a |
| `data/xm3600_subset.txt` | `f5ab86c7f3126ab6683e97b769e462aa149ca22b081a889d0a0027904d503952` | e564ed6 2026-10-12T16:46:56+07:00 | XM600 image ids | equals HEAD |
| `data/xm3600/oiv7_labels.json` | `bac3953a511a9793c22e928a29b68ae05dbf9654502abcbe7b64fd9f6d74c8b2` | e564ed6 2026-10-12T16:46:56+07:00 | OIV7 human-verified labels | equals HEAD |
| `data/xm3600/vi_oiv7_map.json` | `27f2b1ca3f2bf47d43c8f00e8409472c8d571eb720d47b8107a1c77bd208d16a` | e564ed6 2026-10-12T16:46:56+07:00 | lexicon class to OIV7 class map | equals HEAD |
| `data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv` | `84a4373a0efb7fd6d93fe19b0e7ceb6c1b855c233d13b9b78a9a33655c9fdce3` | not in git (git-excluded or untracked) | OIV7 class names (resolve_map) | n/a |

**Model copies**

| File | sha256 | Git (last commit) | Role | Working tree |
|---|---|---|---|---|
| `.session_backup/2026-10-13/research_r9/C8_backbone/SHA256SUMS` | `dc7bd4a45eb3c56e00c56f68cd937871258b679b741949bd38a383950ffc52d8` | not in git (git-excluded or untracked) | checksum manifest (local copy) | n/a |
| `.session_backup/2026-10-13/research_r9/C8_backbone/FREEZE.txt` | `bf152944ea4389f609207c5f9589c214b2ff6a4ae3b2e2a9c877e64a57fbe605` | not in git (git-excluded or untracked) | venv pip freeze (local copy) | n/a |

**Comparators (Qwen2.5-VL-7B zero-shot)**

| File | sha256 | Git (last commit) | Covers all ids |
|---|---|---|---|
| `data/results/coco5000/zeroshot-short.shard0of1.jsonl` | `15ca56156796605c02397d13c60047bc6260d34ac65b8cc54f7651d71717feba` | 1e03989 2026-09-30T02:19:27+07:00 | True |
| `data/results/coco5000/zeroshot-detailed.shard0of1.jsonl` | `96e15f40cead64a993ff01ba2392857b1dae16155661ffddd7f2bac3af54365a` | 1e03989 2026-09-30T02:19:27+07:00 | True |
| `data/results/uitviic/uitviic_zeroshot-short.preds.json` | `76361ccde3db90b9eaa8cf0bf2b7bb055f3535a013626de3dae924bce59baea8` | 685580c 2026-10-13T08:54:54+07:00 | True |
| `data/results/uitviic/uitviic_zeroshot-detailed.preds.json` | `0589973c264b9de43da7e63f40b19ba267a3d08e272c75f51f106cad764828d9` | 685580c 2026-10-13T08:54:54+07:00 | True |
| `data/results/xm3600/xm3600_zeroshot-short.preds.json` | `1f3573324772c67de3eebcdef326f84a39ecbe7fd705ceb5dd4e6863a0d73d4c` | not in git (git-excluded or untracked) | True |
| `data/results/xm3600/xm3600_zeroshot-detailed.preds.json` | `47db3b9d279508e89f0332482c3e268a119186af9e0cbf6426cc85ce1a52a32f` | not in git (git-excluded or untracked) | True |

Builder: `.session_backup/2026-10-18/paperA_tasks/P2/build_g2b_prereg.py` (sha256 `a16df2ebd4bdcb650da85a57e7c3575560b0a735b3d9105bc5224bfbbcaebb6d`). Paper A placeholder: `manuscript/journal_draft/sec7_verbosity_sign.md` at HEAD, lines 84-95 (Section 7.6 unchanged in the working tree).

## 15. Deviations

- A change after the commit of this file goes into a new dated file in `manuscript/prereg/` and is reported as a deviation in Paper A.
- Outputs made with a model file, prompt, decoding setting or instrument other than those above do not test this registration (KD).
- A verdict from an evaluator whose rules differ from Sections 7-10 does not test this registration.
