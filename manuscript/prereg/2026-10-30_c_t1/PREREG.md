# C-T1: tier-1 DEV-EXPLORE prereg for Paper C (head-to-head baselines, third backbone, X1-X5)

Status: DRAFT v3 after rulings CC-172 (GO-with-fixes, 91%; W1-W10, N1-N11 applied) and CC-172a (GO-with-fixes,
92% after W11/W12; both applied, plus N-a..N-c, N-e). Nothing here has run. Not committed. Tier 1 only: nothing here authorises Flickr30K val or test.
Label on every output: `TIER 1 / DEV-EXPLORE (C-T1)`. Every estimate below is AI opinion, not evidence.
Code: `scripts/c_t1/c_t1.py` (CPU selftest: `python3 scripts/c_t1/c_t1.py --selftest`), `scripts/c_t1/c_t1_job.sh`.
Registry: `manuscript/prereg/2026-10-30_c_t1/c_t1_registry.json`. Split: `c_t1_f30k_lists.json` (file names only).

## 0. Why, and how it fits Paper C (PI-1029r)

PI-1029r approved acceptance-raising experiments for C: head-to-head baselines and a third backbone. They must fit C's
current storyline: a training-free retrieval-augmented prompt, the Vietnamese P1 headline, and the English comparison.
The C meta-review (manuscript/reviews/C_META_REVIEW.md §4) and the response (C_RESPONSE_TO_REVIEWERS.md) hand five
experiments to the coordinator. Each tier-1 block maps to one or more of them:

| reviewer item | what reviewers asked | C-T1 block | slot in C |
|---|---|---|---|
| (a) baselines, R1-R3 Table 1, meta-review item 3 | published training-free methods re-run on the same data; OpenFlamingo-style RICES | B3 LMCap (re-implemented), B6 RICES-format interleaved examples on C's own backbones | Table S15 block B (now a same-data block), §2 Table 1 |
| (b) X4, R2 Q1 / R4 M7 | a third backbone from another family; a deletion-free arm | B1, B2, B4 (third backbone, τ = −∞ only) | §6 per-backbone table, §8 English |
| X1, R5 #1 | several `rand` draws, their variance in the CI | B5 (draws 1, 2; draw 0 = C's own) | §5.2 estimand note, Table S16 |
| X2, R3 m4 | masked n-gram analysis of the gain | CPU on every scored run (`masked3` rows) | §6 construct validity, supplement |
| X3, R5 #3 | `ret`-vs-`rand` count-matched precision | CPU on the Vietnamese rows (existing reference gold only) | §6.6 P2 scope |
| X5, R2 Q1 / R4 M7 | memory swap on fixed images | B7 (COCO memory vs Flickr30K-train memory, same carve images) | §8.4 domain-coverage question |

Nothing here edits, re-scores or re-decodes C's registered test results. The paper files are not touched.

## 1. Test-set ledger (what tier 1 may and may not touch)

Sources: LOG CC-158 r4 / W6, CC-160 ruling 4 (test-set ownership), PI-1029h Q3, CC-147 l.35 and l.133.

| set | status for C | tier-1 use |
|---|---|---|
| OpenViIC test (2,001 / 1,941) | spent (C-TEST, P1) | never; no image staged |
| XM-test2500 | spent (C-TEST, XM-a/XM-b) | never |
| COCO Karpathy test 5,000 | spent (C-EN P1-EN) | never |
| NoCaps val 4,500 | spent (C-EN S-NC) | never |
| XM3600, other images (XM-dev500 dev, XM600 A's) | no unspent C-owned images (CC-160: other XM3600 uses refused) | none |
| KTVIC test, UIT-ViIC test | other owners | never |
| **Flickr30K Karpathy test (1,000)** | **unspent; C's one-look set** (CC-158 Q3 → PI-1029h Q3 YES). A has read its reference chains (CC-147 l.35): disclosed. No system has decoded it. | **refused in tier 1** (files listed only to refuse them; images never extracted from the zip; caption rows dropped on read) |
| Flickr30K Karpathy val (1,014) | unspent | **refused in tier 1; reserved for tier 2** (dev-confirm rehearsal, a split never used for selection) |
| Flickr30K Karpathy train (29,000) | unspent | **tier 1**: carve of 1,000 (queries) + 28,000 (X5 memory) |
| KTVIC dev299, OV-dev-B (925) | C's dev sets (stage A, stage-2 gate) | tier 1 (dev-explore; Vietnamese rows stay descriptive) |

Consequence, stated up front: **no Vietnamese confirmatory claim is possible.** Every unspent Vietnamese test set
belongs to another paper. The Vietnamese rows of C-T1 (third backbone, LMCap, X1-X3) are reported in C as labelled dev
rows, beside the registered P1 result, and never as a new verdict. The only possible new confirmatory claim is English,
on Flickr30K test, through tier 2 (val) and tier 3 (test), each under its own prereg.

## 2. Data

- **Flickr30K** (nlphuji/flickr30k at `2b239bef`, ungated): `flickr_annotations_30k.csv` sha256 `395990db…ac137`
  (split counts checked: train 29,000 / val 1,014 / test 1,000) and `flickr30k-images.zip` sha256 `2ce2420c…7391`.
  Terms: Flickr30K non-commercial research terms. The laptop reads only `split` and `filename` to build the lists
  (`c_t1.py lists`); `c_t1.py store` writes the carve references and the X5 memory captions to a file outside the
  repo, dropping val and test rows as it reads.
- **Image custody (CC-172 W4, CC-170 W3 precedent)**: `flickr30k-images.zip` is opened **only on M1 (role m3)**, by
  `c_t1.py extract` (CPU, refuses on any other machine id): it reads only the 1,000 carve and 28,000 memory members,
  by list, into one train-only `.tar` (sha256 logged) and writes their manifests `{file: sha256}`. Only that `.tar`
  goes to M2, where it is extracted by list and **deleted before the job preflight**. The job's `guard` (preflight,
  before any GPU step) refuses any `*.zip`, `*.tar`, `*.tar.gz`, `*.tgz`, any `flickr30k-images*` path and any file
  named in the val or test lists anywhere under `$NCS_DATA` and `/root/outputs`.
- **Carve**: the 1,000 train file names with the smallest sha256(`c-t1-f30k-carve-2026-10-30|name`). File
  `c_t1_f30k_lists.json`, sha256 `eebcd95b…5968` (built on 2026-10-30; counts carve 1,000, memory 28,000, val 1,014,
  test 1,000). The carve is disjoint from the memory by construction.
- **Vietnamese**: C's stage-1 `lists.json` (pinned `5c479f03`), KTVIC dev299 (`decode_icl.manifest`) and OV-dev-B
  (`stage2.manifest2`), both with C's own refusal lists. References read at run time from `$NCS_DATA`, never written.
- **Memories** (unchanged, restored from the backup and sha-checked by the job, file `RESTORED_SHA256`):
  - Vietnamese: C's 8,190-cluster KTVIC+OpenViIC memory; SigLIP2 vectors `c_stage1/emb.npz` (`59e65f6f`); example
    files `c_stage1/exemplars.json` (`b52a03db`), `c_stage2/ex_ov_dev_b.json` (`072b17d1`), query vectors
    `c_stage2/emb_ov_dev_b.npz` (`5ad23a67`).
  - English (B3, B4, B6): C-EN's COCO memory, 111,927 clusters (`cen_memory.json` `b77e4bde`,
    `cen_memory_emb.npz` `add1d92a`). Shown caption = members[0]'s first sentence, as in C-EN. All 111,927
    members[0] images are staged per file (never a val2014/test2014 archive), and all 8,190 Vietnamese cluster
    representatives; `c_t1.py memcheck` verifies every entry's sha256 before any GPU step (W10). The example image of a
    `ret_img` example is the cluster's members[0], while the Vietnamese shown caption may come from another member
    of the same near-duplicate cluster (C's `shown` rule; N10).
  - Restore step (N11, staging checklist): `.session_backup/machines/M3/root/outputs/c_stage1` → `/root/outputs/c_stage1`,
    `…/c_stage2` (incl. the six pinned `runs/` files below) → `/root/outputs/c_stage2`, `.session_backup/machines/M1/root/outputs/c_en`
    (`cen_memory.json`, `cen_memory_emb.npz`) → `/root/outputs/c_en`; then `sha256sum -c RESTORED_SHA256`.
  - X5 (B7): the 28,000 other Flickr30K train images, each its own cluster (no within-memory near-duplicate merge;
    a disclosed simplification), shown caption = the first reference.
- **Near-duplicates**: C's retrieval-time cut (SigLIP2 cosine ≥ 0.92 never shown) applies in every arm and to LMCap's
  retrieval. The pixel rule against Flickr30K test is a tier-3 prereg item (it needs test-image hashes, which tier 1
  never stages).

## 3. Candidates and ranking (task 1)

### 3.1 Baselines

Licences checked on 2026-10-30 (GitHub and HF APIs, no account, no e-mail in any request).

| rank | candidate | training-free? | code / weights licence | fits one 3090? | Vietnamese? | reviewer impact | decision |
|---|---|---|---|---|---|---|---|
| 1 | **LMCap** (Ramos et al., Findings ACL 2023): M-CLIP image→caption retrieval, K = 4, N = 3 fixed shots, XGLM-2.9B, beam 3, M-CLIP re-rank of 3 candidates | yes | repo RitaRamo/lmcap has **no licence file** → not run; re-implemented from the paper (§3 and App. D, PDF sha256 `2125a242…`). Weights: XGLM-2.9B MIT, M-CLIP ViT-H-14/XLM-R MIT | yes (~8 GB) | yes (XGLM covers vi; LMCap reports XM3600 vi = 26.5 CIDEr) | high: the only published training-free, retrieval-augmented, multilingual captioner; already cited in Table S15 | **B3, both languages** |
| 2 | **RICES-format interleaved examples** (Flamingo / OpenFlamingo; RICES from Yang et al. 2022) on C's own backbones | yes | own code; same pinned backbones | yes, batch 1 | yes | high: the exact contrast reviewers raised (image+caption demonstrations vs C's text-only captions), same examples, same k | **B6** (Qwen2.5-VL both languages; third backbone on the carve) |
| 3 | OpenFlamingo-9B itself, RICES | yes | code MIT; checkpoint public; MPT-7B Apache-2.0 | yes (fp16 ~18 GB) | **no** (English LM) | medium: English only; OpenFlamingo already reports RICES vs random (cited) | deferred: added only if the judge asks; needs its own old-stack venv |
| 4 | MeaCap-TF (CVPR 2024) | yes | **no licence file** | yes | no | medium-low: English only, re-implementation would be large (CBART keyword-to-sentence) | not run; published rows stay in Table S15 |
| 5 | ViECap (ICCV 2023) | no (text-only training) | **no licence file** | yes | no | low: reopens the "training-free" label problem (meta-review item 9) | not run |
| 6 | EVCap (CVPR 2024) | no (trained projector) | **no licence file** | **no** (Vicuna-13B bf16 > 24 GB) | no | low | not run |
| floor | `nn_top1`, `nn_cons` (C's copy baselines) | yes | own | CPU | yes | already in C | reused |

### 3.2 Third backbone (non-Qwen language model; InternVL3's LM is Qwen2.5)

| rank | model | LM family | params / bf16 fit | Vietnamese | licence / gate | pins | decision |
|---|---|---|---|---|---|---|---|
| 1 | **Aya-Vision-8B** (CohereLabs, rev `d7601ac8`) | Command R7B | 8.6 B, ~17 GB | listed (one of 23 languages) | CC-BY-NC-4.0 + Cohere acceptable use (research); gated "auto" | git blobs pinned; 4 safetensors + tokenizer.json sha256 masked → filled from the authenticated tree API before any fetch (as CC-168 W1) | **primary** |
| 2 | Gemma-3-4B-it (rev `093f9f38`) | Gemma 3 | 4.3 B | multilingual (140 languages) | Gemma terms; gated "manual" | borrowed from L1-b registry; 4 null hashes (same blocker) | fallback 1 |
| 3 | Idefics3-8B-Llama3 (rev `fddb4ff7`) | Llama 3.1 | 8.5 B | weak (English-tuned) | Apache-2.0, ungated | complete (L1-b) | fallback 2 (always runnable; likely fails the Vietnamese check) |
| — | Gemma-3-12B, Pixtral-12B | — | > 24 GB in bf16 | — | — | — | excluded (would need quantisation, a confound) |
| — | MiniCPM-V, Molmo-D, Vintern, LLaVA-OV-Qwen | Qwen line | — | — | — | — | excluded (same lineage as the reviewers' concern) |

All load through `AutoModelForImageTextToText` in venv-lb (transformers 4.57.6; Aya Vision since 4.50). The third
backbone runs **deletion-free (τ = −∞)**, which is X4's "deletion-free arm" and avoids InternVL3's verifier confound.

## 4. Arms (unchanged definitions from C, plus three new ones)

- `zs`, `ret`, `rand` exactly as C §3.2-3.3 (C's Vietnamese template sha `7478361a`, C-EN's English template
  `b329e57a`, greedy, 60 new tokens, each model's own chat template). Asserted by the selftest.
- `rand` draw d ∈ {0, 1, 2} (X1): draw 0 is C's rule byte for byte (`random.Random(seed("rand", set, id))`); draw
  d ≥ 1 appends `d<d>` to the seed. **Checked on real data**: `c_t1.py draws` reproduces C's committed `rand` and
  `ret` lists exactly on OV-dev-B (925/925) and KTVIC dev299 (299/299) from the restored vectors.
- `ret_img` (RICES format, B6): the same k clusters in the same order as `ret`, each example given as its image
  followed by its caption line; then the query image and the tail. Header, lines and tail are C's template text.
- `lmcap_ri` (LMCap as published, re-implemented): M-CLIP retrieval over the same memory's shown captions (C's
  near cut and the shots excluded), K = 4, N = 3 fixed shots (drawn once per set among clusters below the near cut for
  every query; each shot's 4 captions by the same retrieval from its image; its answer = its own caption), App. D
  template with XGLM's `</s>`, beam 3, 3 returned candidates, M-CLIP image–text re-rank, 40 new tokens.
- `lmcap_se` (same-examples control): as `lmcap_ri` but the 4 captions are C's own top-4 `ret` clusters, so LMCap
  sees the same retrieved evidence as C's top-4. It still differs from `ret` in k (4 vs the backbone's k), the
  template, the fixed shots, the decoding (beam 3 + M-CLIP re-rank) and the generator (text-only XGLM vs a VLM that
  sees the image) (N5).
- Deviations from the LMCap paper, disclosed (N6): the datastore is one shown caption per memory cluster, not every
  caption; the Vietnamese rows retrieve Vietnamese captions (C's memory), while the paper retrieves English COCO
  captions for every language. That English-datastore setting is **not run** here (CC-172a W11: its demonstration
answers would be English under a Vietnamese instruction, unlike App. D); shots come from the memory; XGLM in fp16; max new
  tokens not stated in the paper (40 here). PDFs read: ACL Anthology `2023.findings-acl.104` (sha256 `2125a242…`)
  and arXiv 2305.19821 (sha256 `177cc075…`, the judge's copy).

## 5. Blocks, order and GPU budget

Rates measured on C's own runs (stage-2 PREREG l.386 and C-EN PREREG l.134): Qwen2.5-VL 0.84-0.96 s/image,
InternVL3 1.46-1.51 s/image, C-EN 6.33 GPU-h for 5,000 images × 6 decodes + verifier. Aya-Vision is **unmeasured**
(assumed 1.5 s/image, as InternVL3); RICES assumed 4.5 s/image (Qwen, 9 images per prompt, batch 1).

| block (priority order) | content | GPU-h est. |
|---|---|---|
| B0 | CPU X1 parity draws (OV-dev-B, dev299); SigLIP2 vectors of the carve; carve example lists vs COCO memory | 0.4 |
| S | smoke (W-d / N7): the first fetchable third backbone, `zs` and `ret_img` k = 8 on 16 carve images; 16 LMCap items; seconds logged and charged; never scored | 0.2 |
| B1 | third backbone: `zs` on dev299 + Vietnamese check (§6.2), then the 7 `ret` configurations of C's stage A on dev299; score + select on the host | 1.0 |
| B2 | third backbone on OV-dev-B: `zs`, `ret` (selected), `rand` d0 | 1.2 |
| B3 | LMCap `ri` and `se`, OV-dev-B and carve | 0.7 |
| B4 | carve, English, COCO memory: Qwen (k8 first T1), InternVL3 (k4 last T2, **τ = −∞ only**; its registered τ = 0.10 needs the verifier, added at tier 2 only if InternVL3 advances), third backbone (its selected config, no English tuning, as C-EN) × `zs`/`ret`/`rand` | 3.3 |
| B5 | X1: `rand` draws 1 and 2 on OV-dev-B for all three backbones (draw 0 = C's stage-2 decodes, already scored) | 2.1 |
| B6 | RICES `ret_img`: Qwen on OV-dev-B and the carve; third backbone on the carve | 4.1 |
| B7 | X5: SigLIP2 vectors of the 28,000-image Flickr30K memory; Qwen and third backbone `ret` + `rand` d0 with it | 2.1 |
| **total** | | **15.1** (+25% = 18.9) |

**Hard cap 20 GPU-h** (job wall time per GPU step, `b1.left` accounting, every step under `timeout` for the time
left; a timeout is a CAP STOP, final). The cap trims from the bottom: B7, then B6, then B5 are reported NOT RUN. No
step is retried after a failure other than a resume of its own partial file. One machine (dev role, machine id m4),
one RTX 3090; never concurrent with another job (`b1.take_lock`). B3 and Aya's rates are re-estimated from the smoke
(N9); the stop order (B7 → B6 → B5) does not change.

**Queue and staging on M2 (W5).** L1-b → A-T1 → BD-T1 → C-T1. C-T1 may start only after BD-T1 tier 1 has finished
and cleaned up (BD-T1's guard refuses `*openviic*` paths and its H images; OV-dev-B holds 341 of them). A has priority
with pre-emption: if A-T1 is ready it runs first; if it is stalled, C-T1 may run rather than idle M2. If any A or B
job becomes ready while C-T1 runs, C-T1 stops between steps, `ktvic/` and `openviic/` are unstaged (logged), and C-T1
resumes later from its `.done`/partial files. After C-T1, `ktvic/` and `openviic/` are deleted (logged) before any
later BD job on M2. Disclosure added to CC-171's r1: "C-T1 also ran base models (third backbone, LMCap, RICES) on
ov_dev_b, never a KTVIC-trained adapter."

Existing C decodes reused, not re-run (W3): the six stage-2 OV-dev-B run files of Qwen2.5-VL and InternVL3 (`zs`,
`ret`, `rand` d0; sha256 pinned in `c_t1.py C2_RUNS`) are admitted to C-T1's scorer by pin, re-scored with it, and
gated: their τ = −∞ per-image stripped CIDEr-D must equal the stage-2 ledger `be716482` within 1e-4, else STOP. The
summary reads C-T1 ledgers only, never the stage-2 ledger.

## 6. Third-backbone rules (fixed now)

6.1 **Order**: aya_vision_8b → gemma3_4b → idefics3_8b. A model is skipped (never fetched, never a STOP) while any
pin is null or its gate is not accepted on the operator's account (`c_t1.py fetch` writes `.c_t1_ok` only after
every pinned file checks; `pinsok` gates each model; W9). The first model that passes 6.2 AND 6.3 is the third
backbone. If none passes, the third backbone is reported NOT RUN and every other block still runs (N8; PI Q2 default
YES).

6.2 **Vietnamese check** on its `zs` captions of dev299: share of captions with a Vietnamese-only letter (ă â đ ê ô
ơ ư) or a Vietnamese tone mark ≥ 0.95. Below that, the backbone is NOT VIETNAMESE-ASSESSABLE and the next one runs.

6.3 **Configuration**: C's stage-A rule (stage-1 DESIGN l.272-278), unchanged except τ fixed at −∞: among the 7 `ret`
runs on dev299 (k ∈ {2, 4, 8} × {first, last} with T1, plus k = 4 last T2), the highest stripped CIDEr-D with ΔP_cm
vs `zs` ≥ −1.0, near-verbatim copy share ≤ 0.05 and hit-max rate ≤ 0.02; ties to the smaller k, then `last`, then
T1. No eligible run: that backbone FAILS selection and the next backbone in 6.1 runs (W1). The selection ledger is
written fresh on every (re)run (W6). The same configuration is used in English with C-EN's template (no English
tuning, as C-EN).

## 7. Scoring

Exact laptop commands after the pull (W3; one score call per (set, memory), then one summary). `$R` = the pulled
`/root/outputs/c_t1/out`, `$K` = `scripts/kit_b`, `$CL` = C's stage-1 `lists.json`, `$C2` = the restored stage-2
`runs/`, `$L2` = the stage-2 ledger `be716482`, `$ST` = the caption stores outside the repo:

```
python3 scripts/c_t1/c_t1.py score --set ov_dev_b --memory vi --runs $R/t1_*_ov_dev_b-*-mvi*.preds.json $R/t1_*_ov_dev_b-zs.preds.json \
    $R/t1_lmcap-*_ov_dev_b-mvi.preds.json --c2-dir $C2 --c2-ledger $L2 --kit-b $K --c-lists $CL --ledger $LED/ov_vi.jsonl
python3 scripts/c_t1/c_t1.py score --set f30k_carve --memory coco --runs $R/t1_*_f30k_carve-zs.preds.json $R/t1_*_f30k_carve-*-mcoco*.preds.json $R/t1_lmcap-*_f30k_carve-mcoco.preds.json \
    --refs $ST/carve_refs.json --captions $ST/coco_captions.json --ledger $LED/carve_coco.jsonl
python3 scripts/c_t1/c_t1.py score --set f30k_carve --memory f30k --runs $R/t1_*_f30k_carve-*-mf30k*.preds.json \
    --refs $ST/carve_refs.json --captions $ST/f30k_memory_captions.json --ledger $LED/carve_f30k.jsonl
python3 scripts/c_t1/c_t1.py summary --ledger $LED/ov_vi.jsonl $LED/carve_coco.jsonl $LED/carve_f30k.jsonl \
    --out .session_backup/2026-10-30/c_t1/T1_SUMMARY.json
```
The dev299 ledger is the selection set and is never summarised. Smoke outputs are never scored (`score` refuses them).

- Vietnamese: C's scorer unchanged (`c_stage1/score.py score_set` for model runs, `c_stage2/score2.py plain_row` for
  LMCap and masked rows; kit B, RDRSegmenter, stripped CIDEr-D decision column, df over the set's own references).
- English: C-EN's PTB CIDEr-D (pycocoevalcap 1.2), df over the carve's own 5 references per image.
- Contrasts: paired per-image differences, percentile bootstrap over images, B = 2,000, seed 0 (C's settings).
- X1: `ret` minus the per-image mean of the 3 draws, bootstrap over images, plus the between-draw SD of the contrast.
- X2: each scored `ret`/`rand` caption re-scored with every token removed that sits in a word 3-gram shared with
  its shown examples (`masked3`); `ret`−`rand` on the masked column, descriptive.
- X3: `ret`−`rand` difference of C's ΔP_cm vs `zs` (reference gold, existing labels only), bootstrap, descriptive.
  Not run in English (C-EN's COCO-80 matcher would need a Flickr class map, not built here).

## 8. What tier 1 decides (and what it does not)

Tier 1 makes **no confirmatory claim**. It labels candidate tier-2 claims on the **carve** (English) by a rule fixed
now, and reports everything else as descriptive dev rows.

- Candidate claims (each per backbone, SESOI = +2.0 PTB CIDEr-D, C-EN's carried-over value):
  - E1: third backbone `ret` − `rand` d0;
  - E2: Qwen2.5-VL `ret` − `rand` d0;
  - E3: each backbone's `ret` − `lmcap_ri` (head-to-head with the published training-free baseline).
- Label: **NOMINATE** iff the carve's 95% CI lower bound ≥ +2.0; **WATCH** iff only the point is ≥ +2.0; **DROP**
  otherwise. A planning P(PASS) is printed beside each: normal approximation at n = 1,000, joint = max(0, Φ(z1) +
  Φ(z2) − 1), the Fréchet LOWER bound (W7), with z1 = (d − 2.0)/SE and z2 = d/SE − Φ⁻¹(1 − 0.05/m) (Bonferroni
  on Holm's first step, CC-172a W12), printed at m = 1 and at m = the number of NOMINATEd claims. Vietnamese contrasts carry
  the label DESCRIPTIVE only (N2).
- **Kill gate** (OpenFlamingo's Flickr-30K reversal, App. Tab. 9): if Qwen2.5-VL's `ret` − `rand` point on the carve
  is below 0, E1 and E2 are DROPPED for Flickr30K (E3 may still be nominated).
- **Tier-2 and tier-3 rules, fixed now (W7; copied verbatim into the tier-2 prereg, never redefined after data):**
  - val PASS per claim = point ≥ +2.0 PTB CIDEr-D AND 95% CI lower bound > 0 (C's A1 form), percentile bootstrap,
    B = 2,000, seed 0, on Flickr30K val (all 1,014 images, never used in tier 1);
  - predicted P(PASS on test, n = 1,000) from the pooled carve ∪ val per-image differences, joint = Φ(z1) + Φ(z2) − 1
    (Fréchet lower bound), z2 = d/SE − Φ⁻¹(1 − 0.05/m) with m = the size of the tier-3 family (CC-172a W12),
    labelled as such;
  - "PASS with margin" (PI-1029n, CC-171 W2 form) = val point ≥ +2.0 AND that pooled predicted P ≥ 0.98;
  - claim family = every claim NOMINATEd here AND passing with margin at tier 2. Tier-3 multiplicity: **Holm over the
    family at α = 0.05** (one-sided bootstrap p for Δ ≤ 0, Holm-adjusted); a claim PASSes at test iff point ≥ +2.0
    AND its Holm-adjusted p < 0.05. Holm is chosen now; no primary claim is named;
  - tier 3 (one look at Flickr30K test; irreversible tier, 92-98 band, PI-1029o) only if both margin conditions
    hold; no low-power route (CC-171 W4).
- Descriptive only, whatever the numbers: every Vietnamese row; RICES `ret_img` − `ret`; X1, X2, X3; X5 memory swap.
  In C they enter as labelled dev rows (supplement and one paragraph in §6/§8), never in the abstract as a verdict.

## 9. Honesty notes for the paper

- SESOI +2.0 is C's planning value (stage-2 PREREG l.284), carried to English uncalibrated (C-EN); stated so.
- LMCap and RICES are run as re-implementations or format variants on our memory and backbones; Table S15's published
  numbers stay as published. The same-data rows are labelled "this study, dev".
- The third backbone is chosen on dev299 by C's own stage-A rule; its OV-dev-B row is not a fresh test.
- If the kill gate fires, or tier 2 fails, that is reported in C's discussion (PI-1029m form: brief, not hidden).
- InternVL3 enters the carve at τ = −∞ only (its registered secondary in C-EN), labelled as such.
- Every backbone (and XGLM) may have seen Flickr30K/COCO in pre-training; the exposure is equal across arms of one
  backbone, which is why only within-backbone contrasts are nominated (N10).

## 10. Binding-rule compliance

- Three-tier method (PI-1029n): this is tier 1 on dev data; Flickr30K val and test are refused (listed only to refuse
  them). No spent test set is decoded, scored or staged; C's OpenViIC/COCO verdicts are untouched.
- No new human labels; no AI label is used as evidence (X3 uses existing reference gold only).
- Full official splits: the Vietnamese dev sets are used whole; the Flickr30K carve is a pre-fixed, salted, disclosed
  dev partition of train (train is not an evaluation split); tier 2/3 use full val and full test.
- Captions: no OpenViIC/KTVIC/UIT-ViIC (or Flickr30K) caption text in any repo file; outputs and stores live under
  `/root/outputs/c_t1` and `$NCS_DATA`, pulled to `.session_backup` only. n-gram scan of this file: 0 hits.
- No personal e-mail in any web request (the HF/GitHub/arXiv/ACL reads here carried none); no host, IP or port in
  repo files. Licences: §3 tables; unlicensed code is not run.
- Cost: ≤ 20 GPU-h, one RTX 3090, dev role only. No commit, GPU use or machine access by the drafting agent.

## 11. Open items (to close before the job may start; CC-172 W-list mapped)

- W-a: Aya-Vision gate accepted on the operator's account; its 5 null sha256 values filled from the authenticated HF
  tree API at `d7601ac8` in the commit that records the gate (else gemma3_4b, else idefics3_8b). The selftest
  asserts "all null or all 64-hex" per model, so filling them does not break the preflight; SUMS are regenerated and
  the selftest re-run in that same commit (W2).
- W-b: venv-t1 built (venv-lb freeze + open_clip_torch 2.32.0 + ftfy 6.3.1, exact pins), its freeze sha recorded and
  read by one judge (`T1_FREEZE`). The xlm-roberta-large config/tokenizer files that open_clip loads by name are
  pinned in the registry (`xlm_roberta_large`, rev `c23d21b0`) and fetched into the HF cache with `c_t1.py fetch`;
  the preflight's `t1check` builds M-CLIP offline before any GPU step (W8).
- W-c: `RESTORED_SHA256` and the two SHA256SUMS files written by the gatekeeper at commit.
- W-d: the smoke (block S) times Aya `zs` and `ret_img` at k = 8 and 16 LMCap items; if the projected total exceeds
  20 GPU-h, B6 drops the third backbone first.
- Preflight order in the job (W8, W4, W10, W9): HEAD and SUMS → venv freezes → selftest in venv-lb AND venv-c1score
  → custody guard → memcheck (vi, coco) → XGLM/M-CLIP `pinsok` → `t1check` → GPU steps.
- PI questions (CC-172, for information): Q1 if M1 cannot host the Flickr30K extract within ~2 days, the zip is NOT
  opened on the laptop (default: wait for M1); Q2 if no non-Qwen backbone qualifies, the other blocks run (default YES).
