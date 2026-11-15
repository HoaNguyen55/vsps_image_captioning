# Records of the dated systematic search for Paper C (2026-11-15)

These are the working records behind `manuscript/reviews/C_SYSTEMATIC_SEARCH_2026-11-15.md` (sha256 `acdae5aab11e0e8c2ababae41f9c5b907bb1626cc0c64182a42166acb22c5b38`), copied from the session's scratch folder on 2026-11-15. `SHA256SUMS` lists every file of this folder except itself; check with `sha256sum -c SHA256SUMS` from inside the folder.

## What each file is

| path | what it is |
|---|---|
| `PROTOCOL_before_first_query.md` | the protocol as it stood before the first query (sha256 `258617e9…c28f`); the same bytes are the first 11,025 bytes of the search file |
| `log.tsv` | one line per request of the search: UTC time, source, query id, HTTP status or helper return code, hits and records fetched, for OpenAlex the credit headers, and the query string as sent (no key) |
| `raw/OA-*_p1.json`, `raw/OA-*_p1.hdr` | OpenAlex responses and response headers for the queries OA-1 to OA-8 and OA-C1 to OA-C7 |
| `raw/SEED-*.json`, `raw/SEED-*.hdr` | OpenAlex lookups of the seven seed papers (SEED-C7 is a title search) |
| `raw/AX-*_s0.xml` | arXiv API responses for AX-1 to AX-6 |
| `raw/S2-*.json`, `raw/S2-*.err` | Semantic Scholar bulk-search responses for S2-1 to S2-6 and the helper's error output (empty where there was none) |
| `raw/ACL-1.html` | the page the ACL Anthology search returned: a shell with a client-side search widget and no result row |
| `raw/LOOK-87.json` | OpenAlex lookup of one work at the full-text step, to find its open copy |
| `screening/merged.json` | the 574 unique works after merging and removing duplicates, with the queries that found each |
| `screening/step1.json` | the same list with the title-screen code of each work |
| `screening/step2.json` | the same list with the title-screen and abstract-screen codes; this is the full decision list |
| `scripts/oa.sh` | the OpenAlex call (the key is read from its file by curl and is not in the script) |
| `scripts/merge_search.py` | merging and duplicate removal (step 0) |
| `scripts/step1.py`, `scripts/step2.py` | the decisions of the title screen and of the abstract screen, as lists of work ids per code |
| `scripts/step2view.py` | the condensed view of the abstracts used at the abstract screen |
| `scripts/cells.py`, `scripts/pg.py`, `scripts/qcheck.py` | term counts per full text, page-located search, and the check of every quote against its page |
| `PDF_SHA256.tsv` | sha256, size in bytes and file name of the 17 full texts read at the full-text step, and of two more read for fix package v4 (the proceedings PDF of UniRAG and the data paper of ROCOv2). The file names give the source: `arxiv_<id>`, `acl_<anthology id>`, `ceur_4283_paper<n>` (CEUR-WS Vol-4283), `unige_192276` (the open archive of the University of Geneva), `air_2026446` (doi 10.65737/airmcs2026446) |
| `bib_lookups/lookups.tsv` | the bibliographic lookups made for fix package v4: UTC time, saved file, HTTP status, size, URL |
| `bib_lookups/crossref_*.json`, `arxiv_idlist.xml`, `ceur_Vol-4283_index.html`, `openreview_*.json`, `arxiv_rocov2.xml` | the raw responses of those lookups (the first OpenReview request had a wrong parameter name and got HTTP 400) |

The scripts are records of what was run. They hold paths of the scratch folder and are not meant to run from here.

## What is not here

- The PDFs and the texts extracted from them: they are third-party copies. `PDF_SHA256.tsv` identifies them.
- One journal landing page fetched through doi.org at the full-text step (sha256 `f0595891d30609aaa587a18d243143cf274185fea74e88a42b79b2dde2203d9c`): a third-party web page, not an API response.
- The response of dblp.org to one lookup: it was a bot-check page that printed the requesting network address. It was deleted and no further request was sent.

## Checks before copying

Every file was searched for the OpenAlex key, the Semantic Scholar key and the Hugging Face token (none found), for `api_key=`, `x-api-key`, `authorization` and `set-cookie` lines (none), and for e-mail addresses. The only address in the folder is the contact address vsps-research@example.org, in the protocol, in `scripts/oa.sh` and in the Crossref URLs of `bib_lookups/lookups.tsv`. The raw responses hold titles, abstracts and author names of public bibliographic records and nothing of the project.
