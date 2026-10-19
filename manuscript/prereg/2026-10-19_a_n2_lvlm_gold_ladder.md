# Pre-registration DRAFT: A-N2, a multi-LVLM leaderboard under gold completeness (Paper A Section 7)

- **ID:** `2026-10-19_a_n2_lvlm_gold_ladder`
- **Status:** DRAFT v2 (revised per PD-17): nothing is registered until the gatekeeper commits this pair together with the decoder and the set manifests, and that commit precedes the first decode; the paper cites that commit; the job checks every pin (tracked, equal to HEAD, sha256).
- **Status rule (D-W13-6):** REGISTERED only if the commit of this file precedes the first output of any run listed here; LOCALLY_FROZEN (sha-matching file on disk before, commit after) is EXPLORATORY in claims with the times disclosed; POST_HOC if written at or after an output; EXPLORATORY without a prereg.
- **Machine-readable companion:** `2026-10-19_a_n2_lvlm_gold_ladder.json`; every count and hash below is computed by `build_lb_v2.py` from the files in Section 15 (built 2026-10-19T03:12:44Z, HEAD `cbed6dbc88b8`).
- **Absence check:** files named `lbA_*` under data/results, .session_backup/machines: 0 found.

## 1. What this registers

Zero-shot English captions (short_en, detailed_en; greedy) from 8 open, HF-native LVLMs of several families and sizes on CV295 and UIT-ViIC test (English references, COCO instance gold). Registered: whether one-reference F1 ranks the models as complete gold does (LBA-P1), and whether each model's verbosity slope is ordered by gold completeness and positive under complete gold (LBA-P2, Paper A's C2 per model).

## 2. Models

| Key | Hub id @ revision | Licence | Params | Load dtype | Batch | Processor kwargs | Gated |
|---|---|---|---|---|---|---|---|
| llava15_7b | `llava-hf/llava-1.5-7b-hf` @ `b234b804b114d9e37bb655e11cbbb5f5e971b7a9` | llama2 | 7,063,427,072 | float16 | 8 | defaults | False |
| llava_ov_7b | `llava-hf/llava-onevision-qwen2-7b-ov-hf` @ `0d50680527681998e456c7b78950205bedd8a068` | apache-2.0 | 8,030,807,584 | float16 | 2 | defaults | False |
| qwen25vl_3b | `Qwen/Qwen2.5-VL-3B-Instruct` @ `66285546d2b821cf421d4f5eb2576359d3770cd3` | qwen-research | 3,754,622,976 | bfloat16 | 8 | {'min_pixels': 262144, 'max_pixels': 1048576} | False |
| qwen25vl_7b | `Qwen/Qwen2.5-VL-7B-Instruct` @ `cc594898137f460bfe9f0759e9844b3ce807cfb5` | apache-2.0 | 8,292,166,656 | bfloat16 | 4 | {'min_pixels': 262144, 'max_pixels': 1048576} | False |
| qwen3vl_8b | `Qwen/Qwen3-VL-8B-Instruct` @ `0c351dd01ed87e9c1b53cbc748cba10e6187ff3b` | apache-2.0 | 8,767,123,696 | bfloat16 | 4 | {'min_pixels': 262144, 'max_pixels': 1048576} | False |
| internvl3_8b | `OpenGVLab/InternVL3-8B-hf` @ `259a3b64a14623c0ec91a045cb43f7c5af5fa6af` | qwen | 7,944,373,760 | bfloat16 | 2 | defaults | False |
| idefics3_8b | `HuggingFaceM4/Idefics3-8B-Llama3` @ `fddb4ff79181e55a994674777e06cd5456ce3dc3` | apache-2.0 | 8,462,086,384 | bfloat16 | 2 | defaults | False |
| smolvlm2_2b | `HuggingFaceTB/SmolVLM2-2.2B-Instruct` @ `482adb537c021c86670beed01cd58990d01e72e4` | apache-2.0 | 2,246,784,880 | bfloat16 | 4 | defaults | False |

The model list is frozen in the commit of this file (PD-17 J5). Decoder: `scripts/lb/decode_hf_vlm.py` (draft `decode_hf_vlm_v2.py`), sha256 `e2de18811e2ffeb61ed72cb2399d41123e9a8f6ccd73a5ec35f778dcbe2f5ac4`; committed with this prereg; a run stops unless the decoder's own sha256 equals this pin, and the job checks it with every other pin (PD-17 (d)).
Every pinned file (config, tokenizer, processor, chat template, generation config, weights) is listed with its hash in the JSON (`models.<key>.files`: LFS sha256 or git blob sha1 at the revision); the job fetches only those files and the decoder re-checks them. trust_remote_code is never set.
Venv: a copy of the G2-B venv (/root/venv-qwen3vl) as /root/venv-lb plus num2words 0.5.14, which SmolVLMProcessor needs; nothing else in the venv changes (PD-17 J5); package versions and the pip freeze sha256 are recorded in EVENTS before queueing; packages {'torch': '2.5.1+cu121', 'torchvision': '0.20.1+cu121', 'transformers': '4.57.6', 'accelerate': '1.15.0'}.

## 3. Decoding

- **max_new_tokens:** {'short_en': 60, 'detailed_en': 160}
- **loader:** AutoProcessor.from_pretrained(snapshot, trust_remote_code=False, **processor_kwargs); tokenizer.padding_side='left'; AutoModelForImageTextToText.from_pretrained(snapshot, trust_remote_code=False, attn_implementation, device_map={'': 'cuda:0'}, dtype)
- **message:** [{'role': 'user', 'content': [{'type': 'image', 'image': PIL.Image.open(path).convert('RGB')}, {'type': 'text', 'text': PROMPTS[mode]}]}], one conversation per image; processor.apply_chat_template(batch, add_generation_prompt=True, tokenize=True, return_dict=True, return_tensors='pt', padding=True), cast to the model dtype
- **greedy:** model.generate(**inputs, max_new_tokens=n, do_sample=False, num_beams=1); every other setting from the snapshot's generation_config.json (recorded in each output)
- **text:** tokens up to and including the first EOS, decoded with skip_special_tokens=True, stripped; n_tokens and hit_max (no EOS within n) recorded per image
- **batching:** fixed slices of the manifest order of the model's registered batch size; slice 0 is also decoded at batch size 1 and the identical-caption count is recorded (no gate)
- **checks:** package versions equal venv.packages (else KD); every pinned snapshot file hashes to its pin; the set manifest hashes to its pin; each image hashes to its manifest row
- **prompt_source:** scripts/evaluate.py PROMPTS (texts read and sha-checked by the decoder)

Prompts (`scripts/evaluate.py` PROMPTS; sha256 checked by the decoder):

| Mode | sha256 (16) | New tokens |
|---|---|---|
| short_en | `0cdbdf77fae4c04b` | 60 |
| detailed_en | `525a4e1bf5849e2c` | 160 |

Runs: 32 = 8 models x 2 sets x 2 prompts, ids `lbA_<model>_<set>-<mode>` (evaluate.py's `-<mode>` suffix), queued model by model.

## 4. Image sets

| Set | Images | Manifest (id, file, sha256) | sha256 | Images under $NCS_DATA/datasets/ |
|---|---|---|---|---|
| cv295 | 295 | `data/lb/sets/cv295.tsv` | `16d1ddd47385aedab6422bf308b0a202846321171aa20cd481a1042829d3f4b1` | coco_probe/val2014 |
| uv231en | 231 | `data/lb/sets/uitviic_test.tsv` | `dbadc28724d7a07b599325cd996084934d76e6c4c6a885e64e8de333d6a6665b` | uitviic/images |

Gold levels (score_g2b.py conventions, imported unchanged):

- **cv295:** references: English Karpathy sentences, first 5 in file order (score_g2b.coco_context); complete gold: inst: data/coco_probe/instance_gold.json [cocoid]['coco']; matcher: score_coco_probe.en_classes(text, load_synonyms()) for outputs and references; variants: `refs1_randk` union of 1 of the image's first 5 references, drawn without replacement; mean over the random subsets; `refs2_randk` union of 2 of the image's first 5 references, drawn without replacement; mean over the random subsets; `refs3_randk` union of 3 of the image's first 5 references, drawn without replacement; mean over the random subsets; `refs4_randk` union of 4 of the image's first 5 references, drawn without replacement; mean over the random subsets; `refs_all` union of the first 5 references (refs5); `inst` COCO-2014 instance classes (complete gold); `inst+refs_all` instance classes union refs_all (descriptive only)
- **uv231en:** references: data/datasets/uitviic_en/test_data.json: the first 5 COCO English captions of each image in Karpathy order (crosslingual_gap.py build); complete gold: inst: data/uitviic/instance_gold.json [id]['coco']; matcher: score_coco_probe.en_classes(text, load_synonyms()) for outputs and references; variants: `refs1_randk` union of 1 of the image's first 5 references, drawn without replacement; mean over the random subsets; `refs2_randk` union of 2 of the image's first 5 references, drawn without replacement; mean over the random subsets; `refs3_randk` union of 3 of the image's first 5 references, drawn without replacement; mean over the random subsets; `refs4_randk` union of 4 of the image's first 5 references, drawn without replacement; mean over the random subsets; `refs_all` union of the first 5 references (refs5); `inst` COCO-2014 instance classes (complete gold); `inst+refs_all` instance classes union refs_all (descriptive only)

## 5. Families and analysis plan

- **analysis_set:** per dataset, the images whose caption is clean in every run of every model kept by KM (English: non-empty and clean_supervision.CJK_RE finds no match); every statistic of the dataset uses this one set; its size is reported; all-image values are a sensitivity analysis without verdicts
- **random_subsets:** numpy.random.default_rng(1); for k = 1..K (K = 4 on cv295 and uv231en), for r = 1..20, for each image of the FULL dataset in id order: choice(n_refs_image, k, replace=False). Drawn once per dataset, before any output is read, then restricted to the analysis set.
- **bootstrap:** 1000 image-bootstrap draws per analysis set: numpy.random.default_rng(0).multinomial(N, [1/N]*N, size=1000) over the set's images in id order, shared by every system, gold and family of the analysis (paired). 95% CI = percentiles 2.5 and 97.5 of the replicates.
- **scores:** per run and gold: P, R, F1, M as score_g2b.scores (check_mstar.prf mixed F1, mean over random subsets), imported unchanged
- **slope:** slope[g](F): OLS slope of 100 * F1_x on ln M_x over the runs x of family F (score_g2b.stat_slope); for PAIR_m the two-point slope
- **tau:** tau_b(F1[g1](DETAILED), F1[g2](DETAILED)) over the models' detailed_en runs; [complete] = inst on both sets
- **descriptive:** per model and gold: P, R, F1, M with CIs; slope[refs1_randk](PAIR_m) and slope[refsK_randk] (signs not predicted); tau_b for refs_all vs complete and for the SHORT family; the ranking table; share of hit_max captions; parity_slice0; Qwen3-VL exact-match share against G2-B's GREEDY_EN decodes on cv295 and uv231 (read only after G2-B is scored, CC-027 (c))
- **evaluator:** written after this registration, against this file; imports score_g2b.py functions unchanged; committed through the gatekeeper before its results file exists (CHECKLIST C3)
- **Families:** `PAIR_<model>` = its short_en and detailed_en runs on the set; `DETAILED` = the detailed_en runs of all models; `SHORT` = the short_en runs.

## 6. Verdict rules

- `sign_gt_0`: PASS if ci95_lo > 0; FAIL if point <= 0; else INCONCLUSIVE
- `sign_lt_0`: PASS if ci95_hi < 0; FAIL if point >= 0; else INCONCLUSIVE
- `equiv_abs_le`: PASS if -delta <= ci95_lo and ci95_hi <= delta; FAIL if ci95_hi < -delta or ci95_lo > delta; else INCONCLUSIVE
- `diff_abs_gt`: PASS if ci95_lo > delta or ci95_hi < -delta; FAIL if -delta <= ci95_lo and ci95_hi <= delta; else INCONCLUSIVE
- `compound`: FAIL if any part is FAIL; else NOT_EVALUABLE if any part is NOT_EVALUABLE; else PASS if every part is PASS; else INCONCLUSIVE
- `not_evaluable`: NOT_EVALUABLE if the analysis set is empty or a statistic is undefined (a system with M_x = 0, or fewer than 2 distinct M_x in a family)
- `counting`: Kill rules count FAIL only. INCONCLUSIVE is reported as inconclusive and never as support. Earlier preregistrations scored sign and ordering claims on point estimates; 'not FAIL' here is that criterion, so the outcomes can be compared.
- `multiplicity`: No correction; every prediction is reported separately, per dataset, with its CI.
- `tau_lt`: PASS if ci95_hi < tau0; FAIL if point >= tau0; else INCONCLUSIVE
- `tau_ge`: PASS if ci95_lo >= tau0; FAIL if point < tau0; else INCONCLUSIVE
- `models_compound`: over the models evaluable on the set: FAIL if any model is FAIL; PASS if every model is PASS; else INCONCLUSIVE; NOT_EVALUABLE if fewer than half of the registered models are evaluable
- `tau_b`: Kendall tau-b between two vectors of per-model point estimates (ties handled as in tau-b); the CI comes from the same statistic on every shared bootstrap draw (both rankings recomputed on each draw)

tau0 = 0.9: IR convention for equivalent system rankings (Voorhees, SIGIR 2001; Buckley & Voorhees, SIGIR 2004 use it for incomplete judgments); chosen before any LB output; citation to be checked in bib v4 (A-N6).

## 7. Frozen predictions

| ID | Tier | Sets | Claim | Statistic and rule |
|---|---|---|---|---|
| **LBA-P1** | primary | cv295, uv231en | one-reference F1 does not rank public LVLMs as complete gold does | `tau_b(F1[refs1_randk](DETAILED), F1[complete](DETAILED))` tau_lt (tau0 0.9; with 8 models: at least 2 discordant pairs of 28 (no ties)) |
| **LBA-P2** | primary | cv295, uv231en | C2 per model: the verbosity slope rises with gold completeness and is positive under complete gold | per model m, compound of `slope[refs_all](PAIR_m) - slope[refs1_randk](PAIR_m)` sign_gt_0, `slope[complete](PAIR_m) - slope[refs_all](PAIR_m)` sign_gt_0 and `slope[complete](PAIR_m)` sign_gt_0; per set models_compound |
| **LBA-NS** | not predicted | cv295, uv231en | the one-reference and multi-reference slope signs and every other tau are reported with CIs only | reported, no verdict |

## 8. Kill rules

| ID | Fires when | Consequence |
|---|---|---|
| **KA1** | LBA-P1 is FAIL on cv295 | Paper A states that one-reference F1 ranked these LVLMs as complete gold did (tau >= tau0) and makes no claim that incomplete gold reorders public-model rankings |
| **KA2** | LBA-P2 is FAIL on cv295 or uv231en | Paper A reports C2 as not holding for every public LVLM, names the failing models, and does not write 'replicates across models' |
| **KM** | a model has a run missing or excluded by KD on a set | the model leaves every analysis of that set; LBA-P1 is NOT_EVALUABLE there if fewer than 6 of the 8 models remain (fewer than 15 pairs) |
| **KL** | always | verdicts use the clean analysis set only; its size is reported |
| **KD** | a run whose provenance shows a model file, prompt, decoding setting, batch size or package version other than registered | the run does not test this registration; it is reported as a deviation |

## 9. How the paper reports the outcome

- LB-A verdicts are registered SECONDARY: they appear in the body (Section 7) as computed (PASS, FAIL, INCONCLUSIVE, NOT_EVALUABLE) with the clean-set sizes, never in the abstract or the conclusions (confirmation map section 6; PD-16; PD-17 (e)).
- CV295 lies inside COCO-2500, so on CV295 A-N2 is a replication with new models on discovery images, not an image-out-of-sample test (binding 3, PD-10; PD-17 J1). The paper says so wherever a CV295 verdict appears.
- uv231en results carry the exposure label 'COCO train2014 images; exposure during pre-training possible' (PD-17 J1).
- No count-control (C1) prediction: C1 is NOT-TESTABLE (PD-15) and the map cannot be amended.

## 10. Overlap and disclosure

- Binding 3 (PD-10): CV295 lies inside COCO-2500, so A-N2 on CV295 is a new-model replication on 295 discovery images with the same references and instance gold, not an image-out-of-sample test.
- uv231en shares no image with COCO-2500 (PD-10), but its 231 images are COCO train2014 images, also used by G2-B (Vietnamese captions) and by B-N1 (Paper B, Vietnamese captions); A-N2 uses English captions and English references only, and no KTVIC data (PD-6).
- Qwen3-VL-8B is the G2-B backbone. G2-B's GREEDY_EN runs (cv295, uv231) use the same prompts and new-token limits at batch size 1; A-N2 decodes them again with this harness so that every model shares one harness.

## 11. Departures from the source plans

- XM600 is not decoded: English captions have no complete gold there (no English-to-OIV7 class map, G2-B Section 12), and building one would be new annotation (PD-17 J1). UIT-ViIC test, with COCO's existing English captions and its COCO instance gold, takes its place.
- Qwen3-VL-8B is decoded again instead of reusing G2-B (one harness; G2-B outputs stay unread, CC-027 (c)).
- Optional P3 (count control) is left out (PD-15).
- Gemma-3-4b-it is dropped (gated: no tokens or credentials on rented machines, PD-17 J5). LLaVA-1.5-13B (VRAM), MiniCPM-V-2.6 (remote code, gated), Vintern-1B-v3.5 (scope, PD-17 J4) and Vistral-V-7B (not HF-native, gated) are left out (MODELS_v2.md).

## 12. What the author saw before registering

- Paper A Section 7 (Table 7.1 slopes, families F-B and F-C), the G2-B prereg, PD-10, PD-15, PD-16, CC-027 and the gap analysis. No A-N2 output exists (absence_check).
- The image sha256 lists that G2-B's --check-inputs wrote on M2 (inputs; no G2-B caption or partial file was opened). Hugging Face metadata (hf_api/). No caption of any model on these sets was opened for this draft.
- tau0 = 0.9 is the IR equivalence convention, fixed before any output.
- The UIT-ViIC test English references already enter Paper A Section 5 (exchangeability, stage 1); A-N2 uses them as gold, and no model output on them was opened.

## 13. Cost

- .session_backup/2026-10-18/gpu_jobs/GPU_JOB_PLAN_v1.md line '56_multiref_s42': eval of KTVIC test, short + detailed, Qwen2.5-VL-7B = 0.7 h -> 2.26 s per caption (batch-1 harness, upper bound); models <= 5B params at half that (planning assumption).
- GPU-h by model (upper bound): llava15_7b 0.66, llava_ov_7b 0.66, qwen25vl_3b 0.33, qwen25vl_7b 0.66, qwen3vl_8b 0.66, internvl3_8b 0.66, idefics3_8b 0.66, smolvlm2_2b 0.33; total 4.62 GPU-h; weights on disk 113.6 GB; snapshots are fetched at the pinned revision, pinned files only.
- Machine: M1, after S3 (PD-17).

## 14. Judge rulings applied (PD-17)

- J1: English XM600 dropped (a new English-to-OIV7 map would be new annotation); UIT-ViIC test in English with COCO's existing English captions and instance gold; exposure label kept; binding-3 wording for CV295.
- J5: num2words added, nothing else in the venv changes; Gemma-3 dropped.
- J7: LBA-P1 keeps tau0 = 0.9: with 8 models, at least 2 discordant pairs of 28 (no ties).
- (d): the decoder is committed and sha-pinned with this prereg; the decoder and the job check the pins.
- (e): registered secondary, body only (map section 6).
- GPU plan: A-N2 runs on M1 after S3; check disk space before prefetching.

## 15. Frozen inputs, instruments and sources

A tracked file is pinned by its bytes on disk; the last columns give its last commit and whether the working tree differs from HEAD. Files written by this task (sets, splits, decoder) are drafts to be committed at the paths given in the JSON.

| File | sha256 | Git (last commit) | Role | Working tree |
|---|---|---|---|---|
| `manuscript/GAP_ANALYSIS_Q1Q2_2026-10-19.md` | `0a71aa436a10b74b3d7ed5151c7cc705ad1eca9986e41199c3f9d5de778d6845` | not in git (git-excluded or untracked) | source plan (section 3) | n/a |
| `manuscript/paperA_plan/AGENT_RULES.md` | `9109261d247270c4d8306a116a72ce14157eed5b891b4eda3eb558f033470f99` | not in git (git-excluded or untracked) | agent rules | n/a |
| `.session_backup/2026-10-13/decisions/PD-10.txt` | `4d4122659d9d9c20f0f3d441a803ea2edb87ad2dba078be7f2c3faabce80f2cd` | not in git (git-excluded or untracked) | binding 3 (overlap wording); confirmation map | n/a |
| `.session_backup/2026-10-13/decisions/PD-15.txt` | `81d94e742d4e120e0eb1e9ca6fac11b371135b07f89cdaf293ef38c2c1be7dd3` | not in git (git-excluded or untracked) | C1 NOT-TESTABLE | n/a |
| `.session_backup/2026-10-13/decisions/PD-16.txt` | `06eedc3385ee1279fc2859d0a3213147a092712c6554c916422cd5fa5e7eb403` | not in git (git-excluded or untracked) | registration route; preregs before any decode | n/a |
| `.session_backup/2026-10-13/decisions/PD-17.txt` | `62c69969c405baa8a2367000d1e217fb2e42aa9703274df03670a365cbd35948` | not in git (git-excluded or untracked) | rulings on the LB drafts (J1, J3-J7, (a)-(e)) | n/a |
| `.session_backup/2026-10-13/decisions/CC-027.txt` | `a00da9db5e19d756647b3397ba95a0a511b1a0b07a456e5efddbee1c9db9c386` | not in git (git-excluded or untracked) | G2-B outputs unread until scoring | n/a |
| `manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.json` | `c506bc777b483f5097561d2894a535f33e5e9e27745af07c0f979fbac5560055` | 0932ba1 2026-10-19T01:31:57+07:00 | format; prompts; new tokens; venv; constants | equals HEAD |
| `manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.md` | `2e6b3e87114478f7664a02b3c1b04eaca8dc7a24337dc1ce0293dbc4a0d2608b` | 0932ba1 2026-10-19T01:31:57+07:00 | format template | equals HEAD |
| `scripts/queue/jobs/m2_07_g2b_qwen3vl_ladder.sh` | `c3ded1997e00ae0d0dc4c92fd5733a93c2b84166188c27dc42ea944c61a44446` | f942714 2026-10-19T03:11:56+07:00 | job format | equals HEAD |
| `.session_backup/2026-10-18/gpu_jobs/GPU_JOB_PLAN_v1.md` | `9a8ae864fc2a393ea9d35c75e4ce4578d84e298f90ad4c7d81c07ce1d40bcba3` | not in git (git-excluded or untracked) | cost anchor | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/decode_hf_vlm_v2.py` | `e2de18811e2ffeb61ed72cb2399d41123e9a8f6ccd73a5ec35f778dcbe2f5ac4` | not in git (git-excluded or untracked) | the decoder (draft v2; committed as scripts/lb/decode_hf_vlm.py) | n/a |
| `scripts/g2b/decode_qwen3vl.py` | `8a855ef483c933621776099b6f9de3b60c4fbfaaf706bb40c74e7d84d9dfb5e5` | f942714 2026-10-19T03:11:56+07:00 | prompt_text, sha256_file, utc (imported unchanged) | equals HEAD |
| `scripts/evaluate.py` | `a68d56826d90d8a409493cd6f49007e906c6cb4f5668314edb9b8e7a632e8236` | d4de7b0 2026-10-12T19:24:19+07:00 | PROMPTS; protocol-card scorer | equals HEAD |
| `rescap/vlm/base.py` | `e8fee5bc5b729534af67c6e462a27f0d83ba611f18ff8e3f2717b11eb393ae93` | 1f30d09 2026-08-30T10:06:13+07:00 | dtype_kwarg | equals HEAD |
| `scripts/clean_supervision.py` | `01f172002a607ba9ee55bccb332439f10650832cae1f64a9b74b35c48cd9c231` | 93070e1 2026-10-10T13:48:37+07:00 | CJK_RE (language guard) | equals HEAD |
| `.session_backup/machines/O-2308428/root/outputs/g2b_qwen3vl/uv231_images.sha256` | `17545f03a29a592f611625eb0dd4957132ce44ddefbdad9db642cc78fcd378d4` | not in git (git-excluded or untracked) | UIT-ViIC test image hashes (G2-B --check-inputs on M2) | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/sets/uitviic_test.tsv` | `dbadc28724d7a07b599325cd996084934d76e6c4c6a885e64e8de333d6a6665b` | not in git (git-excluded or untracked) | UIT-ViIC test manifest (draft; data/lb/sets/) | n/a |
| `data/datasets/uitviic/test_data.json` | `54abc0fb068ad1108d7d57b21328d4d68bcf8f41aa168f80ec7c275fb4ac8214` | not in git (git-excluded or untracked) | UIT-ViIC test ids, files, Vietnamese references | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/fetch_log.json` | `3fec7086e4322b9a87dbd205e3ed0ff9b57c02592d55b5eb7659fbd6f2a5deee` | not in git (git-excluded or untracked) | fetch record | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/llava-hf__llava-1.5-7b-hf.info.json` | `2aae954650cade9d8d6049b8579c2b7ce63883623a340899cef0d1e849931b98` | not in git (git-excluded or untracked) | HF metadata | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/llava-hf__llava-1.5-7b-hf.tree.json` | `5894b5e041c6f6565eac35af3c837141a1da608f960ca7b7f0192f3184b6eabc` | not in git (git-excluded or untracked) | HF metadata | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/llava-hf__llava-onevision-qwen2-7b-ov-hf.info.json` | `180be64ccbe1bf557c2bf2fbeda7c31de38aeb93e74cdd8529e66be07309889f` | not in git (git-excluded or untracked) | HF metadata | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/llava-hf__llava-onevision-qwen2-7b-ov-hf.tree.json` | `91fec816d5fadbfe18716386c29f8e762026048d8cbc87299a2c3aa6a11bcc9f` | not in git (git-excluded or untracked) | HF metadata | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/Qwen__Qwen2.5-VL-3B-Instruct.info.json` | `595e127ac0af48def2af445a47375e970ac48a5d01af467ba27c8b3fd6234c89` | not in git (git-excluded or untracked) | HF metadata | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/Qwen__Qwen2.5-VL-3B-Instruct.tree.json` | `96fe2dd92d557c09ae2a1cd050a09d22093f010f61b01e24fa54d4ccee9ee671` | not in git (git-excluded or untracked) | HF metadata | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/Qwen__Qwen2.5-VL-7B-Instruct.info.json` | `e14a77ff74900ec45e3eb3a533607713d187b3c2ba2adc3b003d564a370c889d` | not in git (git-excluded or untracked) | HF metadata | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/Qwen__Qwen2.5-VL-7B-Instruct.tree.json` | `dc9fb97fe125df9628c35f9cd7eb812aaa187e0b81a19f03c2631c97f67f95dd` | not in git (git-excluded or untracked) | HF metadata | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/Qwen__Qwen3-VL-8B-Instruct.info.json` | `dfd342867284b9ea787f1bc9377bdfdb3cb667298cadb33d46948a3cd8348563` | not in git (git-excluded or untracked) | HF metadata | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/Qwen__Qwen3-VL-8B-Instruct.tree.json` | `13901b0c2702f46e541fae48f20309fb5b2413a74326eed4eb1f963a60b6d623` | not in git (git-excluded or untracked) | HF metadata | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/OpenGVLab__InternVL3-8B-hf.info.json` | `6ac5308f0ac2d37edaab5b9a81e4d14600eef6133965b1bf3e90bc000234fd18` | not in git (git-excluded or untracked) | HF metadata | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/OpenGVLab__InternVL3-8B-hf.tree.json` | `c9e4264bd505d6a353b1aa6d9dba145f099fa0c212d400a7f23dd514e6d579cd` | not in git (git-excluded or untracked) | HF metadata | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/HuggingFaceM4__Idefics3-8B-Llama3.info.json` | `429c06cbf10728ab71be88d3533abe8242edde839ba6365a593327ba672befd1` | not in git (git-excluded or untracked) | HF metadata | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/HuggingFaceM4__Idefics3-8B-Llama3.tree.json` | `61b33af5dfe4d7f351b52231f2d2cfa59d2c905fb8c47e00f931da68cf61795b` | not in git (git-excluded or untracked) | HF metadata | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/HuggingFaceTB__SmolVLM2-2.2B-Instruct.info.json` | `8e2e30701e7c625bdfd1e530648341ec2e6fd0ab1c8455a2e3bf9e13eca9afaf` | not in git (git-excluded or untracked) | HF metadata | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/HuggingFaceTB__SmolVLM2-2.2B-Instruct.tree.json` | `92848655b3609167165ef0b31c89bbaac86d39ab46780b753f2d54744e6d25b3` | not in git (git-excluded or untracked) | HF metadata | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/build_lb_v2.py` | `e7ac1054964e2d7cc629ce40b9db5a0fe0e44ffbe27c94d819e010f7266a02fe` | not in git (git-excluded or untracked) | builder (v2) | n/a |
| `scripts/g2b/score_g2b.py` | `66c665c7a71d3b97abbf89fd5bf13871910449ad1c053ff5fb0b18663e3e7ae5` | f942714 2026-10-19T03:11:56+07:00 | scores, slopes, golds (imported unchanged) | equals HEAD |
| `scripts/score_coco_probe.py` | `d11db7e192f689980bb2b2bb717d852d9aa339ad857ce9411fe7bdd6fe416070` | a0accb5 2026-10-14T06:47:37+07:00 | en_classes, load_synonyms | equals HEAD |
| `data/coco_probe/chair_synonyms.txt` | `b685537b36fe21b791c87151b96a991ceb582edff19f3da204dcc7a7905502f2` | 1f30d09 2026-08-30T10:06:13+07:00 | English synonyms | equals HEAD |
| `data/coco_probe/probe_val2017_ids.txt` | `73f8698901f08e7b1bd53dd2842e77683af41e4e9e19276c3e8e6efba5273453` | 4592d69 2026-10-14T06:47:31+07:00 | CV295 ids | equals HEAD |
| `data/coco_probe/manifest.json` | `931e572ec8ea5eadf4c49aafcc062a837429b4e6bcc1f96fc0ec0ee1ecaa7e35` | 1f30d09 2026-08-30T10:06:13+07:00 | file names | equals HEAD |
| `data/coco_probe/cv295_val2014.sha256` | `5aee7a6b1d357444294ffc0bc4e183ed6b26f6bd5b24217cecce6af3da62c0e8` | f942714 2026-10-19T03:11:56+07:00 | CV295 image hashes (official val2014 bytes) | equals HEAD |
| `data/coco_probe/instance_gold.json` | `963af2c6cc71e7a5e32c2f8f1ca6a0f1ef0a1f02dadf40926ddb05eebd04f81e` | d4de7b0 2026-10-12T19:24:19+07:00 | CV295 complete gold | equals HEAD |
| `data/datasets/karpathy/dataset_coco.json` | `2fd999220673258012acfb411a4e7e66af7d488050b2519b0badcc49b7600b8d` | not in git (git-excluded or untracked) | CV295 English references | n/a |
| `data/datasets/uitviic_en/test_data.json` | `07734c7434d78eb5968dc4d986727487366a361b6714b4e98415a99fb8d7a01c` | not in git (git-excluded or untracked) | UIT-ViIC test English references | n/a |
| `data/uitviic/instance_gold.json` | `278d15b97e3eeb9496a0282bb91deb365117becf24d174fbb1e0507203b12ea4` | 093cbfc 2026-10-12T11:58:11+07:00 | UIT-ViIC test complete gold | equals HEAD |
| `.session_backup/machines/O-2308428/root/outputs/g2b_qwen3vl/cv295_images.sha256` | `5aee7a6b1d357444294ffc0bc4e183ed6b26f6bd5b24217cecce6af3da62c0e8` | not in git (git-excluded or untracked) | cross-check of the CV295 manifest | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/sets/cv295.tsv` | `16d1ddd47385aedab6422bf308b0a202846321171aa20cd481a1042829d3f4b1` | not in git (git-excluded or untracked) | CV295 manifest (draft) | n/a |

## 16. Deviations

- A change after the commit goes into a new dated file in `manuscript/prereg/` and is reported as a deviation.
- Outputs made with another model file, prompt, decoding setting, batch size, package version or instrument do not test this registration (KD).
