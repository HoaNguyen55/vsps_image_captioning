# Novelty-check brief (shared by all 10 agents)

Paper under check: "A Method for Reducing Hallucinations in Detailed Vietnamese Image Captioning Using Supervision from Verified Propositions" (VSPS, FAIR 2026; journal extension planned).
Full text: /tmp/claude-1000/-mnt-d-vsps-image-captioning/60eefc4d-7f53-4b8f-b12b-b72a95ec8810/scratchpad/review/paper.txt (2-column, interleaved). Existing lit scan (do not just repeat it; use it to avoid re-verifying): /mnt/d/vsps_image_captioning/.paper_work/Q2_LITERATURE.md

VSPS core claims to test for overlap:
- C1 Data-level: proposition-level verification controls SFT supervision data quality (instead of correcting outputs post hoc or at decoding); verification only offline, deployed model single-pass; standard SFT loss, no extra term.
- C2 Three-state verification SUPPORTED / UNCERTAIN / REJECTED ("not visible ≠ false"), via dual affirmative + negated yes/no queries, K=5 sampled answers each, a split vote closes the evidence gate; ceiling rules may only lower a verdict; colour cross-check with a second model.
- C3 Neutralization: an UNCERTAIN proposition is reduced to its still-verifiable part by dropping the under-evidenced component (main case: gendered Vietnamese person nouns "người phụ nữ" → "người"), recovered offline from stored unanimous evidence, no re-query.
- C4 Typed atomic propositions (entity, attribute, action, count, relation) → budgeted selection → template / constrained-LM rendering where every output span traces to a proposition and verdict.
- C5 Vietnamese detailed-captioning hallucination evaluation: CHAIR on KTVIC with a Vietnamese object lexicon, unsupported-gender-attribution metric, COCO-2014 evaluated in Vietnamese.

For EVERY paper you report give: full title; authors; venue + year (journal/conference; mark IEEE / Elsevier / Springer / ACM and whether Scopus-indexed if you can tell); DOI or arXiv/URL that you actually opened or confirmed; 1–2 sentence summary of method; overlap rating against each relevant claim (none / low / medium / HIGH) with a one-sentence reason; the concrete distinguishing point VSPS can state; recommendation (must cite & contrast / should cite / optional). Never invent papers, venues or DOIs; if you cannot confirm a paper exists, list it under "unverified". Prefer 2024–2026 papers; include older seminal ones only if overlap is medium+.

Output: write ONLY your file .paper_work/novelty/NN_<topic>.md (NN = your agent number). Do not edit any other file. End the file with a section "Highest-overlap risks" (max 5) and a suggested 1–3 sentence novelty statement the paper could use for your topic. Your final message: a 10-line summary listing any HIGH-overlap papers.
