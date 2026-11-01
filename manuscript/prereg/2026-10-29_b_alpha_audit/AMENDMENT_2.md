# B-α AMENDMENT_2: optional OpenAlex key, exact-phrase hyphenated OpenAlex query, fresh OUT (2026-11-01)

**Status:** binding from the gatekeeper commit that carries this file, `scripts/b_alpha/amendment_2.json`, the amended `scripts/b_alpha/b_alpha.py` and both `SHA256SUMS`, byte-identical to the CC-210h subject with the CC-210h verbatim edits (CC-210h_W.diff). Before that commit nothing here binds or runs.

**Parents:** RULE_v3.md (b25080c7…, commit 46a4348) and AMENDMENT_1.md (9989583c…, commit 097ce23).
- Neither file is edited.
- `patterns.json`, `english_words.txt` and `amendment_1.json` are unchanged, so the §2.1 block of RULE_v3 stays byte-equal.
- **PI decision:** PI-1101f (option A).

## 1. Why

- **The one resume ended in a final FAULT** (OPS-1101balpha-fault2):
  - OUT `/home/hoanguyen/vsps_balpha_runs/b_alpha_run1`, commit 097ce23, 2026-11-01T01:06:54Z–01:09:26Z;
  - FAULT at S1: OpenAlex answered **HTTP 401 Unauthorized** on page 2 (a cursor page) of the query `title_and_abstract.search:UIT-ViIC`;
  - every Semantic Scholar call, made with the AMENDMENT_1 key, answered 200.
- **OpenAlex budget.** The page-1 response of that query carried an OpenAlex notice: requests without an API key share one small free daily budget per IP address, and a free key with its own budget is offered. The 401 is read as that budget running out, or cursor paging now needing a key.
- **The unquoted hyphenated query is too broad.** The same page-1 `meta` block reported `count` = **1,074** for the unquoted `UIT-ViIC` query. OpenAlex splits hyphenated terms into separate words, so the query matched "UIT" and "ViIC" anywhere, not the dataset name.
- **What was read for the diagnosis.** The operator read only the `meta` block of that cached response (`count`, `next_cursor`, the notice). No record was printed or read: no title, abstract or id. No `candidates.json`, PDF or population full text exists in run1. That only the `meta` block was read rests on the operator's record (OPS-1101balpha-fault2); no judge opened run1's cache.

## 2. Optional OpenAlex API key

- **Supersedes** RULE_v3 l.71 ('No API key is used') for requests to `api.openalex.org` only, as AMENDMENT_1 §2a did for `api.semanticscholar.org`. No login is used. RULE l.69 still holds.
- **Registration.** The PI registers the key; PI-1101f allows the PI's university e-mail address on the OpenAlex registration form only. That address appears in no URL, header, payload or file of this job.
- **Use.**
  - If the environment variable `OA_API_KEY` (`amendment_2.json` `key_env`) is set and non-empty, the key is added to requests to `api.openalex.org` (`key_host`) as the URL query parameter `api_key=` (`key_param`). This is the OpenAlex authentication form named in the OpenAlex documentation (developers.openalex.org/api-reference/authentication, cited by the coordinator; the writer made no web call).
  - No other host receives it: not Semantic Scholar, not arXiv, not any PDF host.
  - If the variable is unset or empty, the URL is sent unchanged, exactly as before.
- **Never written.** The key sits in the URL, so it is added **only to the URL actually sent**:
  - the URL logged in `search_log.json`, the cache file name (sha1 of the URL) and every error text use the **unkeyed** URL;
  - an HTTP error from a keyed request is re-raised carrying the unkeyed URL;
  - `fault()` and the exit message redact both keys, raw and URL-encoded;
  - `search_log.json` records only `oa_key_used`: `true`/`false` per start, keyed by the `run_dates` entry, as `s2_key_used` does.

  So a run with a key and a run without one write the same log URLs and the same cache names for the same requests.
- **Redirects.** A URL parameter would be carried by a redirect, so for keyed OpenAlex requests a redirect to **another host** is refused (`SameHostRedirect`). That is an HTTP error with no URL in it, and it becomes a FAULT at the current step. A same-host redirect is followed, so the key goes only to `api.openalex.org`.
- **401/403 (coordinator item 2).** An OpenAlex 4xx other than 404 and 429 stays a FAULT at S1 (RULE l.55). **Supersedes** the RULE l.55 clause "the only allowed fix is the documented parameter form `search.title_and_abstract=<string>` plus `filter=publication_year:2020-2026`, by amendment" for the 401 of OPS-1101balpha-fault2. Reason: page 1 of the same filter answered 200, so the filter form was not rejected; the OpenAlex authentication page (§7) states that a free key "is required for cursor paging past the first page", so the 401 came from the cursor page and the parameter form would meet the same 401. The fix is the key; the filter form is kept (CC-210a r7). With a valid key a 401 is not expected; it would mean the key or the account failed. A key that is not activated answers 403 `key_not_activated`. A 429 keeps the RULE_v3 retry schedule (4–64 s), and OpenAlex spacing stays 1 s.
- **Key files and the operator.** Both keys live only in RAM-only files on tmpfs (mode 600, outside the repo):
  - `/dev/shm/oakey` (OpenAlex);
  - `/dev/shm/s2key` (Semantic Scholar, recreated by the coordinator before the run).

  Inside the run's tmux shell the operator loads them with `export OA_API_KEY="$(cat /dev/shm/oakey)"` and `export S2_API_KEY="$(cat /dev/shm/s2key)"`. They are never echoed and never typed on a logged line. After the run (any outcome) both files are deleted, both variables unset, and the tmux session killed.

## 3. The only query change: the hyphenated OpenAlex dataset name becomes an exact phrase

- `amendment_2.json` `openalex.queries` **supersedes** `patterns.json` `openalex.queries` for the run of §4. The only difference: `UIT-ViIC` (unquoted) becomes `"UIT-ViIC"` (a quoted exact phrase). This also supersedes the OpenAlex string list in the prose of RULE l.55. The RULE §2.1 block and `patterns.json` stay byte-equal and unchanged by design; for the run they are not the OpenAlex query list, `amendment_2.json` is.
  - Before: `"Vietnamese image captioning"`, `UIT-ViIC`, `"UIT ViIC"`, `KTVIC`, `OpenViIC`, `VieCap4H`.
  - After: `"Vietnamese image captioning"`, `"UIT-ViIC"`, `"UIT ViIC"`, `KTVIC`, `OpenViIC`, `VieCap4H`.
- **Why.** Unquoted, OpenAlex splits the hyphenated name into separate words (1,074 hits, §1). The quoted phrase matches the dataset name as a phrase, which is how the Semantic Scholar arm already sends it (`"UIT ViIC"`, AMENDMENT_1 / CC-210 W2b). The OpenAlex search documentation states the same rule: "Hyphenated and slashed terms are split into separate words by the search engine" (§7). So the change follows from the documentation; the count only showed it.
- **Every query re-checked:**
  - `"Vietnamese image captioning"` and `"UIT ViIC"` are already quoted phrases;
  - `KTVIC`, `OpenViIC` and `VieCap4H` are single tokens with no hyphen, so quoting would not change their meaning; they are unchanged;
  - no other hyphenated name is in either list;
  - the Semantic Scholar queries are unchanged.
- **Unchanged:** the dataset pattern used for inclusion (§1.3), the Q1 citing-works arm, the Q3 dataset records, every cell, threshold, cap, type list, E3 title and the verdict rule.
- **Decided before any population record was read.** The only input was the `meta` count of run1's page 1 (§1). No title, abstract, id or full text of any candidate was read.
- **Direction.** The change narrows the OpenAlex keyword arm to phrase matches. A paper that names UIT-ViIC is still reached through the quoted phrase, the space-form phrase, the Q1 citing works of the UIT-ViIC record, and the Semantic Scholar arm. Inclusion is still decided by the dataset and metric patterns on the full text, so a paper lost by this change could count only if it names the dataset in its full text and is reached by none of the other three routes. The change does alter the run in one way: about 1,000 token-split candidates would have used up the 300-PDF cap (RULE l.547), so the PDF order, not the rule, would have decided which papers count as accessible.

## 4. Continuation: a fresh OUT, run1 kept

- **run1 is closed and kept unchanged** as a disclosed record (`/home/hoanguyen/vsps_balpha_runs/b_alpha_run1`):
  - two FAULTs at S1 (OPS-1101balpha-fault1, a Semantic Scholar 429; OPS-1101balpha-fault2, an OpenAlex 401);
  - no `candidates.json`, no population data;
  - its 22 cached API responses are never opened again;
  - it is not deleted, renamed or replaced (RULE l.549).
- **The continuation is one fresh run in a new OUT folder** `/home/hoanguyen/vsps_balpha_runs/b_alpha_run2`:
  - with the one resume of RULE §1.1 for that OUT;
  - with fresh request counters (run1's 24 live requests are not counted);
  - with the caps unchanged (400 API requests, 300 PDFs, a 6 h wall per start);
  - with a fresh tool check;
  - on the code of the commit that carries this amendment;
  - on the commit day or later, with `OA_API_KEY` loaded. This **supersedes**, for run2, the RULE §10 row "the first fresh UTC day after the commit" (CC-210 ruling 5), whose reason was the keyless OpenAlex daily budget per IP; a keyed run uses the key's own daily budget. Without the key run2 is not started (§5).
- **Rule basis.** **Supersedes**, for this continuation only, RULE §1.1 "Exactly one path continues it: `run --run --resume --out <the same OUT>`" and "One FAULT gives one resume in total": run1's one resume is used, and the continuation is a second OUT. This is allowed because (i) the one look is `cells.json` (RULE §4), and the RULE l.485 breach clause applies only once `cells.json` exists; (ii) RULE §7 and CC-210b W2 already foresee continuing a FAULTed search by amendment before any population text is read; (iii) run1 never reached S2: no candidate list and no population text exist. So run2 is not a second look; the one look is `cells.json` in run2. A run2 FAULT after its one resume needs a further amendment and a judge read; once run2's `candidates.json` exists, no search string, pattern, cap or threshold may change in any later continuation. RULE §9 (pivot only before S2) still holds.
- **No cache replay from run1 (coordinator item 5).** run2 starts with an empty cache and an empty log. Reasons:
  - run1's responses were fetched without an OpenAlex key and under the old query list, so a replay would mix two query designs in one census;
  - a fresh run makes the candidate list a single, clean product of the amended design;
  - the cost is about 20 repeated API requests.

  Nothing from run1 (cache, search_log, FAULT.json, toolcheck.json) is read by run2.

## 5. Operator (before and after run2)

1. **Pre-run LOG line** naming the one OUT `/home/hoanguyen/vsps_balpha_runs/b_alpha_run2`, with:
   - the commit id;
   - `sha256sum -c` OK on both SUMS (scripts: b_alpha.py, amendment_1.json, amendment_2.json, english_words.txt, patterns.json; prereg: RULE_v3.md, AMENDMENT_1.md, AMENDMENT_2.md);
   - `git status --porcelain` empty for the committed paths;
   - `test -s` and mode 600 on tmpfs for `/dev/shm/oakey` and `/dev/shm/s2key` (stat only);
   - after the two exports in a **new** tmux session, `[ -n "$OA_API_KEY" ] && [ -n "$S2_API_KEY" ]` true (no echo);
   - the offline selftest ok with both keys loaded.
   If either key file is missing or empty: stop and ask.
2. Run, in that tmux shell on AC power: `python3 -I -B scripts/b_alpha/b_alpha.py run --run --out /home/hoanguyen/vsps_balpha_runs/b_alpha_run2`.
3. On a FAULT: the one resume `run --run --resume --out /home/hoanguyen/vsps_balpha_runs/b_alpha_run2`, with both keys loaded again.
4. **After the run (any outcome):**
   - count key occurrences in the OUT and the console log (`grep -rlF`, count only);
   - `rm` both key files;
   - `unset` both variables;
   - kill the tmux session;
   - write a post-run LOG line with `oa_key_used`, `s2_key_used` and both removals.

## 6. Disclosure

- **No result was seen before this amendment.** run1 has no candidate list. The only thing read from its responses was the `meta` block of one OpenAlex page (§1).
- AMENDMENT_2 changes how OpenAlex is authenticated, one OpenAlex query string (unquoted → quoted phrase), and the OUT folder. It changes no pattern, cell, threshold, cap, type list, E3 title or verdict rule.
- AI-designed, not expert-validated (PI-1026bg).

## 7. §8.1 addendum (CC-210h)

| When (UTC) | Who | What | Population contact |
|---|---|---|---|
| 2026-11-01 ~01:45Z | CC-210h judge | documentation only (AMENDMENT_2 §2, RULE l.55): developers.openalex.org/api-reference/authentication (served at help.openalex.org/api/authentication/, last updated 2026-10-15, sha256 4fa50338…: the key is sent as the `api_key` query parameter or as an `Authorization: Bearer` header; a free key "is required for cursor paging past the first page"; a key that is not activated answers 403 `key_not_activated`; `per_page` maximum 100, while run1's keyless OpenAlex pages with per-page=200 answered 200); help.openalex.org/api-entities/works/filter-works (54bd6d9a…), …/works/search-works (cde7f1c6…; "Hyphenated and slashed terms are split into separate words by the search engine"; double quotes match an exact phrase in `title_and_abstract.search`), help.openalex.org/data/work-types (5e517f6a…), all three byte-identical to the CC-210c/CC-210d/CC-210f reads; 4 curl with the placeholder contact, no WebFetch, no key; plus loopback-only (127.0.0.1) probes, not web calls | none (no population record, no S1/S2 request) |
