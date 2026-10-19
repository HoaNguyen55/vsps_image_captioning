# Pre-registration DRAFT: B-N1, a protocol-card leaderboard of public VLMs on Vietnamese benchmarks (Paper B)

- **ID:** `2026-10-19_b_n1_vi_leaderboard`
- **Status:** DRAFT v2 (revised per PD-17): nothing is registered until the gatekeeper commits this pair together with the decoder and the set manifests, and that commit precedes the first decode; the paper cites that commit; the job checks every pin (tracked, equal to HEAD, sha256).
- **Status rule (D-W13-6):** REGISTERED only if the commit of this file precedes the first output of any run listed here; LOCALLY_FROZEN (sha-matching file on disk before, commit after) is EXPLORATORY in claims with the times disclosed; POST_HOC if written at or after an output; EXPLORATORY without a prereg.
- **Machine-readable companion:** `2026-10-19_b_n1_vi_leaderboard.json`; every count and hash below is computed by `build_lb_v2.py` from the files in Section 15 (built 2026-10-19T03:12:44Z, HEAD `cbed6dbc88b8`).
- **Absence check:** files named `lbB_*` under data/results, .session_backup/machines: 0 found.

## 1. What this registers

Zero-shot Vietnamese captions (short, detailed; greedy) from 4 public VLMs whose language model is documented for Vietnamese, on the full KTVIC test set (401 leaked / 157 clean by an OpenViIC train copy) and UIT-ViIC test, scored with the committed protocol-card scorer with and without the punctuation fix. Registered: the fix re-ranks the zero-shot systems on KTVIC (LBB-P1); KTVIC and UIT-ViIC rank them equivalently under the fix (LBB-P2); the fix raises that agreement (LBB-P3).

## 2. Models

| Key | Hub id @ revision | Licence | Params | Load dtype | Batch | Processor kwargs | Gated |
|---|---|---|---|---|---|---|---|
| qwen25vl_3b | `Qwen/Qwen2.5-VL-3B-Instruct` @ `66285546d2b821cf421d4f5eb2576359d3770cd3` | qwen-research | 3,754,622,976 | bfloat16 | 8 | {'min_pixels': 262144, 'max_pixels': 1048576} | False |
| qwen25vl_7b | `Qwen/Qwen2.5-VL-7B-Instruct` @ `cc594898137f460bfe9f0759e9844b3ce807cfb5` | apache-2.0 | 8,292,166,656 | bfloat16 | 4 | {'min_pixels': 262144, 'max_pixels': 1048576} | False |
| qwen3vl_8b | `Qwen/Qwen3-VL-8B-Instruct` @ `0c351dd01ed87e9c1b53cbc748cba10e6187ff3b` | apache-2.0 | 8,767,123,696 | bfloat16 | 4 | {'min_pixels': 262144, 'max_pixels': 1048576} | False |
| internvl3_8b | `OpenGVLab/InternVL3-8B-hf` @ `259a3b64a14623c0ec91a045cb43f7c5af5fa6af` | qwen | 7,944,373,760 | bfloat16 | 2 | defaults | False |

The model list is frozen in the commit of this file (PD-17 J5). Decoder: `scripts/lb/decode_hf_vlm.py` (draft `decode_hf_vlm_v2.py`), sha256 `e2de18811e2ffeb61ed72cb2399d41123e9a8f6ccd73a5ec35f778dcbe2f5ac4`; committed with this prereg; a run stops unless the decoder's own sha256 equals this pin, and the job checks it with every other pin (PD-17 (d)).
Every pinned file (config, tokenizer, processor, chat template, generation config, weights) is listed with its hash in the JSON (`models.<key>.files`: LFS sha256 or git blob sha1 at the revision); the job fetches only those files and the decoder re-checks them. trust_remote_code is never set.
Venv: a copy of the G2-B venv (/root/venv-qwen3vl) as /root/venv-lb plus num2words 0.5.14, which SmolVLMProcessor needs; nothing else in the venv changes (PD-17 J5); package versions and the pip freeze sha256 are recorded in EVENTS before queueing; packages {'torch': '2.5.1+cu121', 'torchvision': '0.20.1+cu121', 'transformers': '4.57.6', 'accelerate': '1.15.0'}.

## 3. Decoding

- **max_new_tokens:** {'short': 60, 'detailed': 160}
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
| short | `8870589c4a32307c` | 60 |
| detailed | `0addb5dd720e4f24` | 160 |

Runs: 16 = 4 models x 2 sets x 2 prompts, ids `lbB_<model>_<set>-<mode>` (evaluate.py's `-<mode>` suffix), queued model by model.

## 4. Image sets

| Set | Images | Manifest (id, file, sha256) | sha256 | Images under $NCS_DATA/datasets/ |
|---|---|---|---|---|
| ktvic_test | 558 | `data/lb/sets/ktvic_test.tsv` | `456243c0cfc82b0c3cc4ad52c694e11b4d9702f3ca14cd8103c3a82cd74a90eb` | ktvic/images |
| uitviic_test | 231 | `data/lb/sets/uitviic_test.tsv` | `dbadc28724d7a07b599325cd996084934d76e6c4c6a885e64e8de333d6a6665b` | uitviic/images |

- **KTVIC split:** leaked = a KTVIC test image with a matched copy in the UIT-OpenViIC TRAIN split (data/ktvic_openviic_refs.json _pairs.test, split field; ids only); clean = the rest. Leaked 401 (`data/lb/splits/ktvic_test_openviic_train_leaked.txt`, sha256 `56e57ea468e48b692ed704ab4655f53cb878309bc3953cfb8dfd57b56590380f`); clean 157 (`data/lb/splits/ktvic_test_openviic_train_clean.txt`, sha256 `4832c16b4499a70b5b6d5c3967a22f551283b45b3a885ba011301b6a4e90015e`). Checks: {'count_equals': '_provenance.summary.per_split.test.matched_openviic_train_copy = 401', 'same_set_as_viclip_ot_rule_sscd_ge_0.8': True}.
- **Panel and lists:** panel `data/ktvic_openviic_refs.json` sha256 `4eb02cc43841bae4f844ee74d4c01b58e677dc8d6abafdd998c9f5b5706f725d` (not in git); derived by `.session_backup/2026-10-19/LB_leaderboards/build_lb_v2.py` (ktvic_split, sha256 `e7ac1054964e2d7cc629ce40b9db5a0fe0e44ffbe27c94d819e010f7266a02fe`); 8-gram scan (.session_backup/2026-10-14/r11_litmaps/openviic_leak_scan.py): 0 of 2 files flagged; the two ID-only lists and their provenance file are committed with this prereg (PD-17 J6).
- **Inclusion rule:** a public VLM enters B-N1 if its card lists 'vi', or the card of its language model names Vietnamese or claims >= 100 languages (fixed before any output); sources in models.*.vietnamese_source.
- **Replacement rule:** PD-17 J5, written before any decode and applied at drafting time: a candidate replaces Gemma-3 only if it is ungated, HF-native (no remote code; its class ships with transformers 4.57.6), Vietnamese documented (the inclusion rule), pinned to a revision with per-file hashes, and its licence is recorded; candidates are the fixed list of the LB brief and the gap analysis, checked in order. Result: no candidate qualifies, so B-N1 runs with 4 models and the 4-model tau0 applies.

| Candidate | Revision | Licence | Ungated | HF-native | Vietnamese documented | Pinned per file | Licence recorded | First failure |
|---|---|---|---|---|---|---|---|---|
| `llava-hf/llava-1.5-7b-hf` | `b234b804b114` | llama2 | True | True | False | True | True | vietnamese_documented |
| `llava-hf/llava-1.5-13b-hf` | `5dda2880bda0` | llama2 | True | True | False | False | True | vietnamese_documented |
| `llava-hf/llava-onevision-qwen2-7b-ov-hf` | `0d5068052768` | apache-2.0 | True | True | False | True | True | vietnamese_documented |
| `HuggingFaceM4/Idefics3-8B-Llama3` | `fddb4ff79181` | apache-2.0 | True | True | False | True | True | vietnamese_documented |
| `HuggingFaceTB/SmolVLM2-2.2B-Instruct` | `482adb537c02` | apache-2.0 | True | True | False | True | True | vietnamese_documented |
| `openbmb/MiniCPM-V-2_6` | `6c04d9e3022b` | None | False | False | False | False | False | ungated |
| `5CD-AI/Vintern-1B-v3_5` | `b98f263eab24` | mit | True | False | True | True | True | hf_native |
| `Vi-VLM/Vistral-V-7B` | `6c8313eb5904` | apache-2.0 | False | False | True | True | True | ungated |

- **Reference rows:** our fine-tuned systems, existing outputs: reference rows only; they enter no verdict and no tau (PD-17 (c)): `data/results/p1_s43-short.preds.json`, `data/results/p1_s43-detailed.preds.json`, `data/results/fuse2_s42-short.preds.json`, `data/results/fuse2_s42-detailed.preds.json`, `data/results/uitviic/uitviic_p1_s43-short.preds.json`, `data/results/uitviic/uitviic_p1_s43-detailed.preds.json`, `data/results/uitviic/uitviic_fuse2_s42-short.preds.json`, `data/results/uitviic/uitviic_fuse2_s42-detailed.preds.json`.

## 5. Scoring

- **cider:** scripts/evaluate.py (committed protocol-card scorer): RDRSegmenter word level, CIDEr-D x100 (rescap.metrics.CaptionMetrics), NCS_DATASET in {ktvic, uitviic}, predictions as {image_id: caption}; the segmenter name it records must not be a whitespace fallback
- **fix:** the punctuation fix: strip trailing whitespace and the characters . ! ? ... (U+2026) from the end of every candidate AND every reference before segmentation (Paper B Section 3.3, 'final period stripped'), then the same scorer; as written = the committed scorer unchanged
- **per_image:** per-image CIDEr-D from one scorer call per set, system and variant (IDF from the full set's references); bootstrap replicates are means of per-image scores over the shared draws
- **objects:** object P/R/F1 as scripts/object_prf.py's KTVIC convention (unique classes, reference-derived gold, exact matches): matcher v1 = rescap.chair.objects_in with RESCAP_RAW_TONE=1, v2 = the tone-normalised default; both sets
- **sets_for_verdicts:** LBB-P1 and LBB-P2 use the FULL KTVIC test set (558 images); both are also reported on the clean 157 as a sensitivity analysis that changes no verdict, because the models' training data is unknown (PD-17 (b))
- **language_guard:** share of captions failing rescap.vlm.mock.looks_vietnamese or matching CJK_RE, per run; verdicts use full sets (evaluate.py refuses subset scoring); clean-intersection values are a sensitivity analysis
- **evaluator:** written after this registration, committed through the gatekeeper before any output is scored
- **Bootstrap:** 1000 image-bootstrap draws per analysis set: numpy.random.default_rng(0).multinomial(N, [1/N]*N, size=1000) over the set's images in id order, shared by every system, gold and family of the analysis (paired). 95% CI = percentiles 2.5 and 97.5 of the replicates.

## 6. Verdict rules

- `sign_gt_0`: PASS if ci95_lo > 0; FAIL if point <= 0; else INCONCLUSIVE
- `compound`: FAIL if any part is FAIL; else NOT_EVALUABLE if any part is NOT_EVALUABLE; else PASS if every part is PASS; else INCONCLUSIVE
- `counting`: Kill rules count FAIL only. INCONCLUSIVE is reported as inconclusive and never as support. Earlier preregistrations scored sign and ordering claims on point estimates; 'not FAIL' here is that criterion, so the outcomes can be compared.
- `multiplicity`: No correction; every prediction is reported separately, per dataset, with its CI.
- `tau_lt`: PASS if ci95_hi < tau0; FAIL if point >= tau0; else INCONCLUSIVE
- `tau_ge`: PASS if ci95_lo >= tau0; FAIL if point < tau0; else INCONCLUSIVE
- `tau_b`: Kendall tau-b between two vectors of per-model point estimates (ties handled as in tau-b); the CI comes from the same statistic on every shared bootstrap draw (both rankings recomputed on each draw)

tau0 = 0.9: IR convention for equivalent system rankings (Voorhees, SIGIR 2001; Buckley & Voorhees, SIGIR 2004 use it for incomplete judgments); chosen before any LB output; citation to be checked in bib v4 (A-N6).

## 7. Frozen predictions

| ID | Tier | Sets | Claim | Statistic and rule |
|---|---|---|---|---|
| **LBB-P1** | primary | ktvic_test | the punctuation fix changes the zero-shot CIDEr-D ranking on KTVIC test (short prompt) | `tau_b(CIDEr_as_written(ZS), CIDEr_fix(ZS))` on the full KTVIC test set, tau_lt (tau0 1: at least 1 discordant pair of 6 (no ties)); ZS = the B-N1 zero-shot models |
| **LBB-P2** | primary | ktvic_test, uitviic_test | under the fix, KTVIC test and UIT-ViIC test rank the zero-shot systems equivalently (short prompt) | `tau_b(CIDEr_fix(ZS) on the full ktvic_test, CIDEr_fix(ZS) on uitviic_test)` tau_ge (tau0 0.6: at most 1 discordant pair of 6 (no ties)). Why this tau0: departs from the 0.9 convention cited for LBA-P1: with n = 4 (or 5) one discordant pair is the smallest possible disagreement, so tau0 lets exactly one swapped pair count as agreement (PD-17 J7); the bootstrap-CI rule stays, and with so few systems INCONCLUSIVE is a likely and honest outcome |
| **LBB-P3** | secondary | ktvic_test, uitviic_test | the fix raises cross-benchmark agreement | `tau_b(fix) - tau_b(as written)` (the LBB-P2 statistic minus its as-written twin) sign_gt_0 |
| **LBB-D1** | descriptive | ktvic_test | leaked minus clean gap per model and reference row: CIDEr-D (both variants), object F1 (v1, v2) | reported with CIs from bootstrap draws within each part, no verdict |
| **LBB-S1** | sensitivity | ktvic_test | LBB-P1 and LBB-P2 recomputed on the clean 157 KTVIC test images | reported with CIs; changes no verdict (the models' training data is unknown) |
| **LBB-D2** | descriptive | ktvic_test, uitviic_test | the leaderboard: CIDEr-D (both variants), BLEU-4, ROUGE-L, object P/R/F1 (v1, v2), end-punctuation rate, length, language-guard share, hit_max share, parity, both prompts | reported, no verdict; reference rows shown beside, outside every tau |

## 8. Kill rules

| ID | Fires when | Consequence |
|---|---|---|
| **KB1** | LBB-P1 is FAIL | Paper B does not claim that the fix re-ranks public zero-shot systems; it reports the shifts only |
| **KB2** | LBB-P2 is FAIL | Paper B does not claim that KTVIC rankings transfer to UIT-ViIC; it reports the discordant pairs |
| **KM** | a model has a run missing or excluded by KD on a set | the model leaves every tau on that set; a tau with fewer than 4 models is NOT_EVALUABLE |
| **KD** | a run whose provenance differs from this registration (model file, prompt, decoding, batch size, package version) | the run does not test this registration |

## 9. How the paper reports the outcome

- Every verdict is quoted as computed, with the protocol card (segmenter, CIDEr-D, x100, punctuation variant).
- Exposure labels: KTVIC leaked/clean by OpenViIC train copy; UIT-ViIC test = COCO train2014 images. The training data of the public models are not verified by this registration.
- B-N1 belongs to Paper B, and its claims follow KB1 and KB2 (PD-17 (e)); Paper A cites none of its numbers.
- PD-6 (c) note for Paper B: Paper A's G2-B uses the same model (Qwen3-VL-8B) on the same UIT-ViIC test images (UV231) with a different statistic (verbosity slopes under gold levels), so no number is primary in both papers.

## 10. Overlap and disclosure

- UIT-ViIC test images are also Paper A images (G2-B in Vietnamese; A-N2 in English). B-N1 decodes its own Qwen3-VL runs; they use the same prompts, new-token limits and pixel bounds as G2-B's *-short-T0 and *-detailed-T0 UV231 runs, at another batch size, and no G2-B output is read (PD-17 J3).
- XM600 is dropped: XM3600 belongs to Paper A (PD-6; PD-17 J3).

## 11. Departures from the source plans

- XM3600-vi (gap analysis B-N1) is dropped (PD-17 J3).
- Gemma-3-4b-it is dropped (gated: no tokens or credentials on rented machines, PD-17 J5); the replacement rule found no qualifying model, so B-N1 has 4 models.
- Vintern-1B-v3.5 is left out for scope: one HF-native decoder for every model, so that every model runs through the same audited code path (PD-17 J4). Vistral-V-7B is not HF-native and is gated.
- LLaVA-OneVision-7B, LLaVA-1.5-7B, Idefics3-8B and SmolVLM2-2.2B fail the inclusion rule.
- Qwen2.5-VL-7B is decoded again with this harness; the existing zero-shot outputs (older harness) stay Paper B's backbone baseline, and their exact-match share with the new decodes is reported.

## 12. What the author saw before registering

- Paper B Sections 3 and 5 (punctuation audit, transfer table), the overlap file's summary counts (ids only), the r10 leakage counts, PD-17. No B-N1 output exists (absence_check); no caption of any public model on these sets was opened for this draft.

## 13. Cost

- .session_backup/2026-10-18/gpu_jobs/GPU_JOB_PLAN_v1.md line '56_multiref_s42': eval of KTVIC test, short + detailed, Qwen2.5-VL-7B = 0.7 h -> 2.26 s per caption (batch-1 harness, upper bound); models <= 5B params at half that (planning assumption).
- GPU-h by model (upper bound): qwen25vl_3b 0.49, qwen25vl_7b 0.99, qwen3vl_8b 0.99, internvl3_8b 0.99; total 3.46 GPU-h; weights on disk 57.5 GB; snapshots are fetched at the pinned revision, pinned files only.
- Machine: M2, after G2-B and S2 (PD-17).

## 14. Judge rulings applied (PD-17)

- J3: XM600 dropped; B-N1 decodes its own Qwen3-VL runs; PD-6 (c) note in Section 9.
- J4: Vintern-1B-v3.5 excluded for scope (one audited HF-native decoder), disclosed in Section 11.
- J5: num2words added, nothing else changes; Gemma-3 dropped; replacement rule applied: none qualifies, 4 models.
- J6: ID-only lists committed; panel sha256 4eb02cc4, deriving script sha256 e7ac1054, counts 401/157, 8-gram scan: 0 of 2 files flagged.
- J7: LBB-P2 tau0 = 0.6 with 4 models (at most 1 discordant pair of 6 (no ties)); bootstrap-CI rules kept.
- (b) full KTVIC test set for LBB-P1/P2, clean set as sensitivity; (c) reference rows outside every verdict and tau; (d) decoder pinned with the prereg; (e) Paper B, KB1/KB2.
- GPU plan: B-N1 runs on M2 after G2-B and S2; check disk space before prefetching.

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
| `rescap/chair.py` | `e47d249ac7290070f2387d3fa8b22dac77728265ad276f55aa6520f5cbc591a3` | a0accb5 2026-10-14T06:47:37+07:00 | objects_in: matchers v1 (raw tone) and v2 | equals HEAD |
| `scripts/object_prf.py` | `6b711280d70b780d596414896d832738da58f1b079015dee888605d1ba350adc` | 20ea9d4 2026-10-12T19:53:25+07:00 | object P/R/F1 | equals HEAD |
| `rescap/vlm/mock.py` | `33793de01b4f2790964342b1af2d4c2de18d793ae4693608283992475ed62ce7` | 1f30d09 2026-08-30T10:06:13+07:00 | looks_vietnamese | equals HEAD |
| `data/datasets/ktvic/test_data.json` | `cc22ec6a8883773cb23c87ad5b64925f5a53c21982117274b53621f454e7ebbf` | not in git (git-excluded or untracked) | KTVIC test | n/a |
| `data/ktvic_openviic_refs.json` | `4eb02cc43841bae4f844ee74d4c01b58e677dc8d6abafdd998c9f5b5706f725d` | not in git (git-excluded or untracked) | overlap panel (ids and split fields only; not in git) | n/a |
| `.session_backup/2026-10-14/r11_litmaps/openviic_leak_scan.py` | `3c56217ec71d6856a5f51f79ffe899a4056f1318d606ff77515b19229789138b` | not in git (git-excluded or untracked) | OpenViIC 8-gram scanner (counts only) | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/sets/ktvic_test.tsv` | `456243c0cfc82b0c3cc4ad52c694e11b4d9702f3ca14cd8103c3a82cd74a90eb` | not in git (git-excluded or untracked) | KTVIC test manifest (draft) | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/splits/ktvic_test_openviic_train_lists_v2.provenance.json` | `95717c89cc28c029eae3a04f8f462671e1b4a581844c74e0017af6e4d03ae3ba` | not in git (git-excluded or untracked) | list provenance (draft) | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/splits/ktvic_test_openviic_train_leaked.txt` | `56e57ea468e48b692ed704ab4655f53cb878309bc3953cfb8dfd57b56590380f` | not in git (git-excluded or untracked) | leaked ids (draft) | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/splits/ktvic_test_openviic_train_clean.txt` | `4832c16b4499a70b5b6d5c3967a22f551283b45b3a885ba011301b6a4e90015e` | not in git (git-excluded or untracked) | clean ids (draft) | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/readme_Qwen__Qwen2-7B-Instruct.md` | `174c5a5d83d0f9670e0b96df86f2dddb2de5ab958f885653525b3d2c977f24b5` | not in git (git-excluded or untracked) | Vietnamese documentation | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/readme_Qwen__Qwen2.5-7B-Instruct.md` | `f366f33bbf6bcadbb7d87f0a21a7b65584a56b8d58b0743c77c88bee625b93a6` | not in git (git-excluded or untracked) | Vietnamese documentation | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/readme_Qwen__Qwen3-8B.md` | `0f36caaff9c2516411a7738db384606263ba653c1e63e61d72f511606164d5a6` | not in git (git-excluded or untracked) | Vietnamese documentation | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/pypi_num2words.json` | `04e1409b01edb7099c8f89c52e8e8c8446df7aef96e760985cff450ed011d228` | not in git (git-excluded or untracked) | num2words version | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/llava-hf__llava-1.5-13b-hf.info.json` | `a2d3a6487196b431a398d7a7b28e54fef208477c66a7bf21a3952260959c73be` | not in git (git-excluded or untracked) | replacement-rule candidate | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/openbmb__MiniCPM-V-2_6.info.json` | `e399dc2ad29bef68f21600ea252733773719ae8a92c8e021699164364161e320` | not in git (git-excluded or untracked) | replacement-rule candidate | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/5CD-AI__Vintern-1B-v3_5.info.json` | `f713d511e10a33a96196c7a6f722b7481bf749cced14904c645cbc69e248a4ef` | not in git (git-excluded or untracked) | replacement-rule candidate | n/a |
| `.session_backup/2026-10-19/LB_leaderboards/hf_api/Vi-VLM__Vistral-V-7B.info.json` | `14b90c261fdff2db60ef1fc2ded5ede731ddb37ac4598622b830558f7c831281` | not in git (git-excluded or untracked) | replacement-rule candidate | n/a |

## 16. Deviations

- A change after the commit goes into a new dated file in `manuscript/prereg/` and is reported as a deviation.
- Outputs made with another model file, prompt, decoding setting, batch size, package version or instrument do not test this registration (KD).
