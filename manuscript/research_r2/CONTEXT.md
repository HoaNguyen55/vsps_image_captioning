# Shared context for round-2 novelty research (read fully before starting)

## Project
Vietnamese image captioning paper targeting a Q1 journal (Pattern Recognition / Neurocomputing / IEEE TMM).
Backbone Qwen2.5-VL-7B-Instruct, QLoRA 4-bit, 512 vision tokens, one RTX 3090 (24 GB) per experiment; the paper may only claim 1 GPU.

## Hard constraints from the user
- EXISTING DATASETS AND EXISTING LABELS ONLY. The user will NOT create new datasets or gold labels: no human annotation,
  no new benchmark that needs labelling. AI-made labels (e.g. data/object_gold/annot_claude.json, "AI-silver") are NOT evidence.
- Every experiment fits one 3090 and ideally <= ~10 GPU-hours.

## Data available (run local scripts with NCS_DATA=data from the repo root /mnt/d/vsps_image_captioning)
- KTVIC (daily-life images; 3,769 train / 558 test; 5 Vietnamese refs each): data/datasets/ktvic/{train,test}_data.json.
- UIT-ViIC (COCO ball-sport images; train 2,695 / val 924 / test 231; 5 Vietnamese refs) WITH COCO-2014 instance labels for
  every image: data/datasets/uitviic/*.json, data/uitviic/instance_gold.json (scripts/build_uitviic_gold.py).
- COCO-2014 Karpathy test (2,500 / 5,000 images; English refs + instance labels): data/coco_probe/, scripts/score_coco_probe.py
  (Vietnamese matcher over the 80 classes, data/coco_probe/coco80_vi.json); existing Vietnamese zero-shot and old-VSPS captions on
  COCO in data/results/coco5000/. COCO annotation files may be under data/datasets/coco_probe/annotations/.
- POPE / RePOPE (scripts/pope_vi.py).
- Public datasets that already exist (XM3600 has Vietnamese human captions; Flickr30k; COCO train) may be used if useful.

## Systems and numbers (KTVIC test, 558 images; object P/R/F1 vs the union of the 5 refs, scripts/object_prf.py;
## "short" = one-sentence prompt, "detailed" = describe-in-detail prompt -> fuse2 writes two reference-style sentences)
- Zero-shot: short P 52.3 R 32.5 F1 40.1; detailed 31.6/57.1/40.7.
- P1 = SFT on the first human caption (1 row/image, 942 steps): short P 77.9 R 41.4 F1 54.1, CIDEr-D 149.8, CHAIR_i 19.2
  (seed 43: 78.8/41.7/54.5, CIDEr 143.9 -> seed noise in CIDEr is ~6 points).
- fuse2 = SFT on the consensus caption (short prompt) + greedy fusion of 2 human captions (detailed prompt), scripts/build_gold_sft.py:
  short 75.7/47.1/58.1, CIDEr 143.9, CHAIR_i 21.9; detailed 68.0/61.2/64.4, CIDEr-D 23.9 (Gaussian length penalty), CHAIR_i 29.0.
- fuse2 + Grounding-DINO object tags in the prompt (inference only): short 77.9/46.7/58.4; paired vs P1: dP 0.0, dR +5.3, dF1 +4.3
  (p=0.0004), dCIDEr -3.4 n.s., dCHAIR_i +0.3 n.s.; detailed 70.7/59.7/64.8.
- Human parity (scripts/human_parity.py, manuscript/novel_direction/R4_01_HUMAN_PARITY.md): against the same held-out annotators,
  one human P 85.3 / R 46.9; fuse2-short 72.9 / 48.5; P1-short 75.2 / 42.8 -> recall reaches one human, precision trails by ~12.
  Two humans fused 76.1 / 66.6 vs fuse2-detailed 59.6 / 63.6.
- Leakage-free offline ranking of training-target policies on train (build from 3 annotators, score vs the other 2), object F1:
  fuse2 67.7 > random-pair fusion 65.7 > consensus 62.9 > unfused-2-rows 61.9 > P1 60.6 > multiref-all-5 58.9.
- Null or negative so far: rejection-sampling fine-tuning on train images (E5; memorisation) and its DPO (short mode collapses);
  hidden-state existence probe (AUROC 0.807 but no selection effect); naming ladder; old VSPS hedging pipeline (dominated by P1).
- Running/queued on 2x3090: seeds 43/44 of P1 and fuse2; target-policy ladder (consensus-only, random-pair fusion, unfused 2 rows,
  P1 at 4 epochs, multiref all 5); length-matched controls (two-sentence prompt, self-fusion and object-consensus MBR over 6 samples);
  COCO Karpathy transfer + POPE/RePOPE asked in Vietnamese; UIT-ViIC transfer and in-domain P1 vs fuse2 (scored with COCO instances);
  Qwen2.5-VL-3B P1 vs fuse2; cross-fitted RFT (train on half A, sample on unseen half B).

## Round-1 research (do NOT re-propose these unless you fix the reason they were killed)
Files: /tmp/claude-1000/-mnt-d-vsps-image-captioning/755eae04-5e4c-4ce1-ab21-d4bc106761ee/scratchpad/wf/{critique_*,ideate_*,verify_*}.json
Killed as scooped / ~0 gain: ABC-Fuse annotator-bagged LoRA committee (acts as a consensus filter; IC3, ATED prior art);
phrase-graft one-sentence fusion (Marsi & Krahmer; Zheng et al. 2018); PU/propensity-corrected RFT selection (~0);
CoverageDial k-annotator conditioning (CaptionSmiths, Florence-2); ACF-RLOO held-out-annotator-panel RL (panel coupled to targets;
RLOO/SCST/BalCapRL/CCCaption prior art); PanelOPSD self-distillation; FuseEdit-DPO (HALVA, TL-DPO); evidence-gated PU reward
(ClaimDiff-RL, VCap); MIND mention-inventory head (PatchGate); complement decoding. Kept only as an ablation: object-consensus MBR.
The three simulated reviewers' verdict: fusion is a data-selection heuristic with close prior art (Nagasawa 2021, Zheng 2018,
concatenated-reference baselines, CCCaption CVPR 2026); precision is the open problem; the paper needs a principled contribution.

## Code
Repo /mnt/d/vsps_image_captioning is READ-ONLY for you (another process commits). Write your scripts and outputs ONLY under
/tmp/claude-1000/-mnt-d-vsps-image-captioning/755eae04-5e4c-4ce1-ab21-d4bc106761ee/scratchpad/research_r2/<your id>/.
Useful modules: scripts/build_gold_sft.py (consensual, fusion_set, fused), scripts/object_prf.py (image_counts, scores, paired),
scripts/human_parity.py (leave-annotators-out protocols), scripts/score_coco_probe.py (vi_classes, load_vi_terms), rescap/chair.py
(objects_in, _ancestors), scripts/evaluate.py (references, PROMPTS). Predictions: data/results/<system>-<mode>.preds.json.

## Compute for pilots
This machine has 4 cores shared with other agents: run pilots with `nice -n 15` and bootstrap B <= 2000.
For heavier CPU work you may use n3: `ssh -p 2241 root@n3.ckey.vn` (16 cores; repo /root/vsps, venv /root/vsps/.venv,
NCS_DATA=/root/ncs-data) with `nice -n 19`, writing only under /root/r2/. NEVER use either GPU, never touch /root/queue.

## What "deep" means here
1. Read the full text (arXiv HTML/PDF) of the 6-12 closest papers (2023-2026, top venues + recent arXiv); extract exact mechanisms
   and reported numbers. Run at least 10 targeted searches for scooping.
2. Propose AT MOST 2 ideas, each (a) genuinely new relative to that literature (closest prior + precise delta), (b) implementable on
   one 3090 within ~10 GPU-h, (c) backed by a CPU pilot on existing data that estimates the achievable effect or an upper bound
   (run it; report numbers with CIs), (d) aligned with the paper's story: learning faithful, high-coverage Vietnamese captions from
   multiple partial human references.
3. If nothing survives your own pilot, say so: a well-founded negative is useful.

## Output
- Full report: research_r2/<id>/REPORT.md (English; sources with arXiv ids/DOIs; pilot code next to it).
- Final message (<= 350 words): for each idea: title; mechanism (2 lines); closest prior + delta; pilot numbers with CIs; GPU-h;
  kill criterion; your confidence. Plus one line on the most important literature finding.
