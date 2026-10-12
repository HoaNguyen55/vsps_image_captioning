# Shared context for round R6: a method that RAISES THE KEY METRICS, with breakthrough novelty (read fully first)

## What changed (user, 2026-10-12)
The user wants the new work to reach the best achievable scores on the important captioning metrics, with a new method
whose novelty is a step beyond prior art. Earlier rounds optimised novelty of ANALYSIS (typicality vs truth, frontier
invariance); this round optimises METRICS + METHOD NOVELTY. Analysis results are the diagnostic backbone that should
motivate the method, not the headline. The old vi/en "5% gap" rule is dropped.

## Target metrics (KTVIC test, 558 images, short prompt, word-level RDRSegmenter, x100 - exactly as data/results/*.json)
Primary: CIDEr(-D). Also BLEU-4, METEOR, ROUGE-L (higher) and CHAIR_i / CHAIR_s (lower; rescap/chair.py). Object P/R/F1
(scripts/object_prf.py) secondary. Generalisation: UIT-ViIC test (231, Vietnamese refs, COCO images) and COCO Karpathy (English).

| system (short mode)              | B-1  | B-4  | METEOR | ROUGE-L | CIDEr | CHAIR_i | CHAIR_s | mentions/cap |
|----------------------------------|------|------|--------|---------|-------|---------|---------|--------------|
| GRIT (published KTVIC SOTA)      | 74.7 | 40.6 | 36.6   | 59.7    | 136.0 | -       | -       | -            |
| zero-shot Qwen2.5-VL-7B          | 30.7 | 5.5  | 24.4   | 25.6    | 29.0  | 42.9    | 62.0    | 2.17         |
| P1 seed 42 (SFT on 1st caption)  | 79.0 | 45.5 | 39.1   | 64.2    | 149.8 | 19.2    | 28.7    | 1.80         |
| P1 seed 43                       | 79.1 | 45.2 | 39.1   | 64.0    | 143.9 | 17.7    | 26.7    | 1.76         |
| P1 seed 44                       | 79.0 | 44.8 | 39.1   | 63.8    | 143.7 | 18.3    | 27.6    | 1.79         |
| P1 s43 + GDINO tags in prompt    | 79.4 | 44.7 | 38.7   | 64.0    | 145.0 | 17.5    | 26.7    | 1.79         |
| fuse2 seed 42                    | 77.4 | 42.3 | 39.4   | 63.7    | 143.9 | 21.9    | 35.8    | 2.09         |
| fuse2 s42 + GDINO tags           | 78.6 | 43.7 | 39.1   | 63.8    | 146.4 | 19.5    | 32.1    | 2.02         |
| fuse2 obj-consensus MBR, 6 x T0.8| 66.3 | 32.7 | 37.6   | 57.3    | 98.0  | 27.1    | 49.6    | 2.53         |
| E5 rejection-sampling FT         | 76.0 | 41.3 | 38.9   | 62.5    | 137.9 | 22.5    | 36.0    | 2.08         |
| E5 + DPO                         | 73.0 | 36.4 | 37.4   | 59.6    | 123.1 | 23.0    | 37.6    | 2.01         |
P1 mean of 3 seeds: CIDEr 145.8 (SD ~3.4), B-4 45.2, METEOR 39.1, ROUGE-L 64.0, CHAIR_i 18.4. Single-seed MDE ~2.5-3.8 points.
Other SOTA: UIT-ViIC ObjectAoA B-4 49.7, METEOR 37.3, ROUGE-L 64.8, CIDEr 148.8 (arXiv 2211.05405);
UIT-OpenViIC MDSANet+CAMO CIDEr 76.48. Full SOTA notes: manuscript/novel_direction/R2_01_sota_bar.md.

## Success bar for a "breakthrough" method
- At least +8 CIDEr over the P1 3-seed mean (about 2.3 seed SDs) with CHAIR_i not worse; or a Pareto shift (CIDEr >= P1 and
  CHAIR_i lower by >= 4 points). It must be replicated on UIT-ViIC, and on COCO if the method is language-agnostic.
- Gains must survive 3 seeds and paired bootstrap over images. No hyperparameter may be chosen on KTVIC test: use a dev split
  of KTVIC TRAIN images (e.g. 300 images, random.Random(0).sample(sorted(train_ids), 300), held out of training while
  tuning), then retrain on full train. Pilot numbers computed on test preds are effect-size ESTIMATES and must be labelled so.

## Hard constraints
- EXISTING DATASETS AND EXISTING HUMAN LABELS ONLY. The user will NOT create datasets or gold labels: no annotation, no new
  benchmark. AI-made labels (data/object_gold/annot_claude.json, "AI-silver") are NOT evidence and must never be used to
  evaluate. Model-generated signals INSIDE a training method (RL rollouts, self-training on existing images, detector outputs)
  are allowed as method components, but flag any proposal that depends on synthetic training data so the user can veto it.
- The paper claims ONE RTX 3090 (24 GB). Each run must fit one 3090; QLoRA 4-bit; open models only. Report GPU-h per run.
  Two rented 3090s (n2, n3) exist only for throughput.
- Leakage: KTVIC images are UIT-OpenViIC images. 401/558 KTVIC test images are in OpenViIC TRAIN, the rest in OpenViIC dev/test.
  Any use of OpenViIC must drop every content-matched KTVIC test image (mapping in data/ktvic_openviic_refs.json -> keys
  "train"/"test" = KTVIC image id -> OpenViIC captions; "_pairs"). That file is git-excluded (licence: non-commercial research,
  no redistribution): read it, never copy its captions into committed files.

## Assets (repo /mnt/d/vsps_image_captioning; NCS_DATA=data from the repo root)
- KTVIC: data/datasets/ktvic/{train,test}_data.json + images/ (3,769 train / 558 test, 5 refs; refs were typed by one person
  from 3 participants - say "5 reference captions", adjacent caption indices are dependent).
- Second human panel: UIT-OpenViIC captions for 3,768/3,769 KTVIC TRAIN images and 555/558 TEST images
  (data/ktvic_openviic_refs.json; manuscript/novel_direction/R5_01_SECOND_PANEL.md). Longer (17.5 vs 12.1 words), more objects.
- OpenViIC full: data/datasets/openviic/ (13,300 images, train/dev/test annotation json).
- UIT-ViIC: data/datasets/uitviic/{train,val,test}_data.json + COCO-2014 instance labels data/uitviic/instance_gold.json.
- COCO Karpathy: data/datasets/karpathy/dataset_coco.json (English refs); Vietnamese COCO-80 matcher scripts/score_coco_probe.py.
- XM3600 (vi + en human captions; OIV7 verified labels): data/datasets/xm3600*, data/xm3600/.
- Grounding-DINO tags for KTVIC test: data/results/tags_gdino.json (train-image tags do not exist yet; a GPU job can make them).
- Hidden-state existence probe (E2): AUROC 0.807 on Qwen2.5-VL-7B layer 24 (features /root/probe500.npz on n2/n3;
  scripts/probe_existence.py); probe-selected object sets beat SUPPORTED by +18 P / +11 R at equal size, but selecting RFT data
  with it gave no effect.
- Samples: 6 short-prompt samples per KTVIC test image at T=0.8, top_p 0.95 for fuse2_s42 and p1_s43:
  n2:/root/ncs-data/samples/{fuse2_s42-test-short.jsonl,p1_s43-test-short.jsonl} (copy read-only with scp -P 2022).
- Predictions of every system: data/results/<system>-<mode>.preds.json; scoring: scripts/evaluate.py (do not edit it - another
  agent is changing it), scripts/score_ci.py (load_preds), scripts/object_prf.py (paired bootstrap), scripts/metrics_v2.py.
- Training: scripts/train_stage2.py (SFT; --loss-mask legacy|assistant; legacy kept prompt tokens in the loss in every run so
  far; a mask-fix check pair is running), scripts/build_gold_sft.py (targets: first / consensus / all / fused / unfused).

## Already tried or killed (do not re-propose unless you fix the stated reason)
- Round 1 (scooped or ~0 gain): annotator-bagged LoRA committee; phrase-graft fusion; PU/propensity RFT selection; CoverageDial
  k-annotator conditioning; ACF-RLOO held-out-panel RL (prior art RLOO/SCST/BalCapRL/CCCaption); PanelOPSD; FuseEdit-DPO
  (HALVA, TL-DPO); evidence-gated PU reward (ClaimDiff-RL, VCap); MIND mention head (PatchGate); complement decoding.
- Round 2: IFCR capture-recapture precision (references are dependent); implicit-threshold mechanism (wrong prediction);
  V5 triage of new training methods (annotator-resampled rows, consensus-naming contrast, certified minimal pairs, instance-gated
  cross-lingual fusion, exchange-rate grid, vote-then-fuse) - none worth GPU for PRECISION; only a policy-diverse adapter
  committee gave ~+2 P at 0 GPU-h. Note: that triage was about precision vs a second panel, NOT about CIDEr.
- Empirical: E5 rejection-sampling FT and its DPO lowered CIDEr (memorisation; short-mode collapse); MBR at T=0.8 lowered CIDEr
  to ~97; tags help fuse2 (+2.5 CIDEr) not P1 (+1.1); training-time fusion beats inference self-fusion at equal length.
- Verified findings to build on: (1) reference-based precision measures typicality more than truth (an independent panel
  halves fusion's precision cost); (2) frontier invariance: every training target lies on one precision-vs-object-count curve,
  only external evidence (detector tags) moved off it (+1.87 P), pre-registered in manuscript/prereg/.

## Rules for agents
- Literature: read full text (arXiv HTML/PDF) of the closest 2023-2026 papers; at least 10 targeted scoop searches. If
  WebSearch fails, use the arXiv API (export.arxiv.org/api/query), OpenAlex (api.openalex.org) and Semantic Scholar
  (api.semanticscholar.org/graph/v1). Cite arXiv ids / DOIs. Never invent numbers or papers.
- Known techniques may be used as components (SCST, MBR, LoRA...). Say exactly which element is new, with the closest prior
  and the delta. Rank by expected metric gain x novelty x cost.
- CPU only, locally with `nice -n 15`, <= 4 threads, bootstrap B <= 2000. No GPU, no VLM/LLM loading. n2
  (`ssh -p 2022 root@n2.ckey.vn`) and n3 (`ssh -p 2241 root@n3.ckey.vn`): read-only copies only; if you must compute there:
  `nice -n 19 taskset -c 12-15`, <= 4 threads, <= 4 GB RAM, write only under /root/r6/. Never touch /root/queue or the GPUs.
- The repo is READ-ONLY for you. Write code and outputs only under
  /tmp/claude-1000/-mnt-d-vsps-image-captioning/755eae04-5e4c-4ce1-ab21-d4bc106761ee/scratchpad/research_r6/<your id>/
  and write REPORT.txt there with a Bash heredoc (the Write tool may refuse report files).

## Added after launch (binding for verifiers and the synthesis)
- OpenViIC as TRAINING data has a cost beyond leakage: the plan R5-00 (manuscript/novel_direction/R5_00_KE_HOACH_BAI.md, and V5
  sec. 7) keeps OpenViIC as the INDEPENDENT evaluation panel. A model trained on OpenViIC captions (even of KTVIC train images)
  learns OpenViIC naming, so its second-panel precision is no longer an independent check. A proposal that trains on OpenViIC
  must keep a no-OpenViIC variant for every second-panel analysis, or move the truth check to COCO instance labels
  (UIT-ViIC, COCO Karpathy), and must state this cost.
- Power: with 3 seeds per arm a between-seed t-test detects about +12.7 CIDEr (P1 mean 145.8 -> about 158.5; R5-00). A +8
  CIDEr claim needs 5+ seeds per arm or paired image-level bootstrap pooled across seeds; say which.
- GPU RESULTS that landed after launch (2026-10-12; binding for verifiers and the synthesis). All are KTVIC test, short mode,
  single seed 42, response-only loss, set_seed before LoRA init:
  - p1assist_s42 (P1): CIDEr 148.7, B-4 45.9, CHAIR_i 18.3.
  - mr5assist_s42 (multi-reference SFT, all 5 captions, 1 epoch): CIDEr 147.5, B-4 44.8, CHAIR_i 19.5. That is -1.2 CIDEr vs
    the matched P1, so B2's predicted +3 to +9 did NOT appear at this seed.
  - Legacy-mask P1 runs: 149.8 / 143.9 / 143.7 / 147.7.
  - Mask effect, judge D5: short +0.99 [-3.44, +5.17] n.s.; detailed CHAIR_i -1.79 [-3.49, -0.23].
  - P1_dev on dev300: CIDEr 144.3. The CN-RLOO pilot (jobs 35_b..35_d) is running on n2.
