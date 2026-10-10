# CFP hunt brief (shared, today = 2026-10-10)

Paper to place: "Reducing Hallucinations in Detailed Vietnamese Image Captioning Using Supervision from Verified Propositions" (VSPS). Topics: vision-language models, image captioning, hallucination, data-centric fine-tuning, low-resource / Vietnamese NLP, multimodal evaluation. A FAIR 2026 conference version exists, so the target is either a journal extension (needs ~30%+ new material) or another venue that accepts extended versions.

Find venues whose submission is OPEN NOW or opens before 2027-06-30: deadlines from 2026-10-10 onward. Target quality: journals SJR/JCR Q2-Q3 (Q1 allowed if fit is excellent), Scopus- and/or ISI (SCIE/ESCI)-indexed, IEEE/ACM/Springer/Elsevier/IET/Wiley etc.; conferences whose proceedings are Scopus/IEEE Xplore/ACM DL/Springer LNCS/LNAI-indexed.

Rules: Verify every entry on the official CFP / journal page (WebFetch it). Never invent deadlines, quartiles or URLs. If a 2027 edition's date is not yet announced, put the expected month in notes and set "verified": false for that date. Quartile: give source (SJR 2024/2025 or JCR) if you confirmed it; else null. Avoid predatory / discontinued-from-Scopus venues (check Scopus discontinued list if unsure) and say so in notes.

Output ONLY the file .paper_work/cfp/NN_<slug>.json: a JSON array of objects with exactly these keys:
{"name": str, "acronym": str|null, "type": "conference"|"journal"|"special_issue", "publisher": str, "indexing": [str], "quartile": str|null, "quartile_source": str|null, "rank_other": str|null (e.g. CORE B, IF 3.2), "fit": 1-5 (5 = perfect topical fit for VSPS), "deadlines": [{"label": str, "date": "YYYY-MM-DD", "verified": bool}], "event_date": str|null, "location": str|null, "url": str (official page you opened), "apc": str|null, "review_time": str|null, "notes": str (why it fits, extension policy, risks)}
Rolling journals with no deadline: deadlines = [] and say "rolling" in notes. Aim for 12-25 good entries. Validate the JSON with python before finishing. Final message: <=8 lines with the top 3 picks.
