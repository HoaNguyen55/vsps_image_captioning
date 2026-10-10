# Round-2 critique brief (2026-10-10)

You are an independent, adversarial critic of the draft plan /mnt/d/vsps_image_captioning/.paper_work/kg_plan/00_KE_HOACH.md (Vietnamese). Read it fully. Read round-1 evidence files 01..20_*.md in the same folder only where needed to check a claim. Do not trust the draft: try to break it on your assigned axis.

PRIVACY (hard rule): never put any email address, name or personal data in any request (no `mailto=` for OpenAlex/Crossref, no email in User-Agent, no personal data in queries). Anonymous requests only.

Evidence rules: open/confirm every paper you cite (arXiv abs page or API, ACL Anthology, CVF, OpenReview, Semantic Scholar). If an API returns 429, wait and retry, or use the arXiv listing/abs pages. Never invent papers, venues, numbers. Unconfirmed → "Chưa xác minh".

Output ONLY .paper_work/kg_plan/R2_NN_<slug>.md in Vietnamese with sections: (1) Verdict on your axis (pass / needs-fix / fail) per plan component; (2) Findings, each: claim in plan → evidence → severity (BLOCKER / MAJOR / MINOR) → concrete fix (exact text change or plan change); (3) What the plan got right (brief). Final message <= 10 lines: count of BLOCKER/MAJOR and the top fix.
