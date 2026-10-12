# Round R7: re-evaluate "image captioning + knowledge graphs (KG)" for the Vietnamese captioning paper

## The user's request (2026-10-12)
Besides RL, search reputable journals and high-quality scientific papers on combining image captioning with knowledge
graphs. Evaluate the direction and find possible novelties. If it is not suitable, write an analysis; if it is suitable,
also write an analysis. Either way: detailed, specific reasons and convincing scientific evidence.

## What already exists (READ FIRST, build on it, do not redo it)
A 3-round KG research programme was run on 2026-10-10 in the repo /mnt/d/vsps_image_captioning:
- manuscript/research_wall/11_knowledge_graph_captioning.md: trend scan with OpenAlex counts. Summary: injecting an external
  KG into the generator is mature and flat; graphs used for verification, evaluation and hallucination are rising;
  Vietnamese has no scene-graph data, parser or graph metric.
- manuscript/kg_plan/: 20 topic files (01..20), review rounds R2_*, R3_*, plans 00_KE_HOACH_v1/v2 and 00_KE_HOACH.md (v3).
  Verdicts:
  - KG injection into the generator, graph-token adapters, relation encoders: HIGH overlap, dropped.
  - Scene-graph reward: HIGH overlap.
  - Surviving core: KG-structured hierarchical backoff for uncertain entities and predicates (ViHG-Cap), plus a Vietnamese
    graph metric.
  - That core required NEW human annotation (gold scene graphs, human scoring; about 200 annotator-hours).
- Key files: kg_plan/00_KE_HOACH.md, 17_novelty_redteam.md, R3_01_overlap_novelty.md, R3_02_reviewer_v2.md,
  03_vn_resources_feasibility.md, 09_cultural_knowledge.md, 05_kg_rag.md, 06_graph_injection.md, 12_graph_training_objectives.md.

## What changed since then (the re-evaluation must use these)
- Constraint: NO new labels or annotation of any kind; AI-made labels are not evidence. The old ViHG-Cap evaluation plan
  is therefore infeasible as written. Existing "truth" sources now available instead:
  - an independent second human panel (UIT-OpenViIC captions for 555/558 KTVIC test images and 3,768 train images);
  - COCO-2014 instance labels on UIT-ViIC and COCO Karpathy;
  - XM3600 with OIV7 verified labels.
- Goal: METRICS FIRST. The best achievable KTVIC CIDEr, BLEU-4, METEOR and ROUGE-L, with CHAIR_i lower, plus method novelty
  for a Q1 journal. P1 (SFT on the first caption) is at CIDEr 145.8 (3 seeds); GRIT, the published SOTA, is at 136.0.
- New findings:
  1. KTVIC's 5 references form a paraphrase chain; multi-reference SFT is the best target (R6 B2).
  2. Reference-based precision measures typicality more than truth (two-panel analysis, R5_01).
  3. Frontier invariance: training targets move along one precision-vs-coverage curve; only external evidence (detector tags)
     moved off it.
  4. RL on CIDEr-D is the main lever (R6 B1: expected +5 to +9). It has a regurgitation hazard; CN-RLOO masks copies.
  Reports: /tmp/claude-1000/-mnt-d-vsps-image-captioning/755eae04-5e4c-4ce1-ab21-d4bc106761ee/scratchpad/research_r6/
  {CONTEXT_R6.md, B1_rl/REPORT.txt, B2_targets_data/REPORT.txt, B3_decoding/REPORT.txt}.
- Hardware: one RTX 3090 claimed (two rented for throughput); Qwen2.5-VL-7B 4-bit QLoRA.

## Rules
- Reputable sources only:
  - journals: TPAMI, IJCV, TIP, TMM, TCSVT, TNNLS, Pattern Recognition, Neurocomputing, Knowledge-Based Systems,
    Information Fusion, ESWA, ACM TOMM, IP&M;
  - conferences: CVPR, ICCV, ECCV, NeurIPS, ICLR, AAAI, IJCAI, ACL, EMNLP, NAACL, ACM MM;
  - arXiv preprints only when recent and clearly marked.
  Open or confirm every paper (arXiv API, Semantic Scholar, OpenAlex, Crossref, CVF/ACL open access). Never invent papers,
  venues, DOIs or numbers. Put unconfirmed items under "Unverified".
- Report reported gains AS NUMBERS: baseline vs +KG on the same benchmark, with the baseline's strength.
- CPU only, nice -n 15, at most 2 threads; this machine has 8 GB RAM. Never load a VLM. The repo is read-only for you.
- Write your report with a Bash heredoc to
  /tmp/claude-1000/-mnt-d-vsps-image-captioning/755eae04-5e4c-4ce1-ab21-d4bc106761ee/scratchpad/research_kg/<your id>/REPORT.txt.
  Write in English; technical terms as usual.
