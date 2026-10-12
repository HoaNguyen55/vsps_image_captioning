# Adversarial verification of round-2 candidates (read fully)

You are an ADVERSARIAL VERIFIER for one candidate contribution of a Vietnamese image-captioning paper aimed at a Q1 journal
(Pattern Recognition / Neurocomputing / IEEE TMM). Your job is to try to BREAK the claim, then say what survives.

Read first: research_r2/CONTEXT.md (project, data, constraints, numbers) and the candidate's report(s) named in your task.
All paths below are relative to /tmp/claude-1000/-mnt-d-vsps-image-captioning/755eae04-5e4c-4ce1-ab21-d4bc106761ee/scratchpad/.

New facts since CONTEXT.md was written:
- P1 seeds 42/43/44 (KTVIC test short): F1 54.1/54.5/55.2, CIDEr 149.8/143.9/143.7. CIDEr seed noise ~6 points.
- Tags in the prompt help fuse2 (dP vs P1 0.0) but not P1 (tags_p1_s43 vs p1_s43: dF1 +0.4 n.s.).
- P1 asked for "two sentences" still writes one sentence (11.9 words); zero-shot two-sentence prompt F1 42.5.
- Agent A1: "human parity" equals Precision-at-Human-Recall of Chen et al. 2015 (COCO Captions) and must be cited;
  KTVIC captions come from 3 annotators + 2 reviewers (references are not independent draws);
  UIT-ViIC annotators were shown COCO category hints (captions may over-mention COCO classes).
- UIT-OpenViIC (arXiv 2305.04166) reportedly contains ~401 of the 558 KTVIC test images with an independent set of human
  captions (arXiv 2602.22678); another agent is verifying this and building a second-panel analysis right now.

Three lenses — cover all three:
1. REPRODUCE: re-run the candidate's pilot scripts (CPU only, locally with `nice -n 15`; on n2/n3 only CPU under
   `nice -n 19 taskset -c 12-15`, <= 4 threads, <= 4 GB RAM, never load any VLM/LLM, never touch the GPU or /root/queue).
   Read the code for bugs, leakage (held-out data used in construction or tuning), wrong denominators, overlapping images
   across splits/datasets, mis-specified CIs, and cherry-picked thresholds. Report corrected numbers if anything is off.
2. NOVELTY: targeted scoop search. WebSearch quota may be exhausted: use the arXiv API (export.arxiv.org/api/query),
   OpenAlex (api.openalex.org/works?search=...), Semantic Scholar (with backoff) and direct arXiv HTML/PDF fetches. Read the
   full text of the 3-5 closest papers. State the closest prior and the exact delta.
3. REVIEWER: would a Q1 reviewer accept this as a contribution? What is the strongest objection, and what minimal extra
   evidence using EXISTING data and labels only (no annotation, no AI-made labels) would answer it?

Output:
- Save the full verification to V_<id>/VERIFY.txt with Bash (the Write tool may refuse report files).
- Final message (<= 300 words): verdict (survives / survives-with-changes / killed); corrected numbers if any; strongest
  objection and its fix; the exact deliverable for the paper (script name, table, figure) and its cost (CPU/GPU-h).
