# B-α AMENDMENT_1: Semantic Scholar request behaviour (2026-11-01)

**Status:** DRAFT. CC-210f (GO-with-fixes 92) read it; the commit is licensed by the CC-210g diff read of the CC-210f fixes. It binds only after CC-210g and a gatekeeper commit that carries this file, `scripts/b_alpha/amendment_1.json`, the amended `scripts/b_alpha/b_alpha.py` and both `SHA256SUMS`, byte-identical to the CC-210g subject. Nothing here is committed or run.

**Parent:** `RULE_v3.md` (sha256 b25080c7…, commit 46a4348). RULE_v3.md, `patterns.json` and `english_words.txt` are **not changed** by this amendment. The §2.1 block therefore stays byte-equal.

## 1. Why

- The registered run (OPS-1101balpha-prerun; OUT `/home/hoanguyen/vsps_balpha_runs/b_alpha_run1`) started 2026-11-01T00:01:21Z.
- It ended with FAULT at S1 at 00:03:38Z (OPS-1101balpha-fault1). Semantic Scholar answered HTTP 429 on `/paper/ARXIV:2401.08100` (the KTVIC resolution) after the frozen retries, about 124 s of back-off in all.
- Unauthenticated Semantic Scholar requests share one rate-limit pool. On 2026-11-01 the PI chose to register a Semantic Scholar API key with the PI's own address on the registration form only (PI-1101d). That address appears in no URL, header, payload or file of this job (§2a).
- At the FAULT: 6 live API requests were logged (5 × HTTP 200, 1 × HTTP 429). No `candidates.json` existed, no population text had been fetched, and no PDF had been downloaded.

## 2. What changes (Semantic Scholar host only)

The values are frozen in `scripts/b_alpha/amendment_1.json` (in `SHA256SUMS`). They apply to requests whose host is `semanticscholar.org` or a subdomain of it, i.e. `api.semanticscholar.org`.

| Item | RULE_v3 / 46a4348 | AMENDMENT_1 |
|---|---|---|
| Spacing between requests | ≥ 3 s (`patterns.json` `semantic_scholar.min_spacing_s` = 3; RULE l.543 "at least 3 s") | **5 s** (`amendment_1.json` `min_spacing_s`). This still satisfies "at least 3 s", so RULE l.543 holds. `patterns.json` keeps its value of 3, which is the floor |
| Attempts per URL | 6 | **10** |
| Retried HTTP codes | 429 only | **429, 500, 502, 503, 504** |
| Wait before attempt n+1 (n = 0, 1, …) | 2^(n+2) s (4, 8, 16, 32, 64) | **max(Retry-After, min(5 × 2^n, 300))** seconds. Retry-After is honoured when it is a whole number of seconds, capped at 600 s; an HTTP-date Retry-After is ignored. Without Retry-After the waits are 5, 10, 20, 40, 80, 160, 300, 300, 300 (1,215 s in all) |
| Total wait per URL | 124 s | **≤ 1,800 s**. A retry whose wait would push the URL's total wait past 1,800 s is not made; the error stands |
| After the last attempt | HTTPError → FAULT at the current step | unchanged: HTTPError → FAULT (RULE l.64) |

**Unchanged** (no byte change in `patterns.json` or `RULE_v3.md`):
- every query, pattern, threshold and cap (400 API requests, 300 PDFs, the 6 h wall);
- the OpenAlex and S2 type lists, E1–E5, the E3 titles and the pre-read set;
- T, the verdict table, the two-way decide, the cells and the quotes rule;
- OpenAlex, arXiv and other hosts: spacing 1 s (arXiv 3 s); 6 attempts; only 429 retried, at 4–64 s; a 5xx is not retried.

## 2a. Optional Semantic Scholar API key (PI-1101d)

The PI registered a Semantic Scholar API key (PI-1101d). It was approved on 2026-11-01.
- Supersedes RULE_v3 l.71 ('No API key is used') for requests to api.semanticscholar.org only. No login is used. RULE l.69 still holds.
- **Rate limit (fact from the approval e-mail; the key itself is not quoted anywhere).** The key's limit is 1 request per second, cumulative across all endpoints. The 5 s spacing of §2 (at most one request per 5 s to Semantic Scholar) is compliant.
- **Use.** If the environment variable `S2_API_KEY` is set and non-empty when the job starts, the key is sent as the `x-api-key` header on requests to `api.semanticscholar.org` **only**. Other hosts never receive it, including other `*.semanticscholar.org` hosts such as PDF mirrors, and OpenAlex and arXiv. The key is attached as an unredirected header, so an HTTP redirect does not carry it to the next URL (CC-210f W1).
- **No reduced spacing.** The spacing stays at 5 s with a key. All retry and wait values of §2 are unchanged.
- **Never written.** The key, any part of it, and any hash of it are never written to any file, log, cache, `FAULT.json`, console output or exit message.
  - Request headers are passed to the HTTP call only. They are not logged, and urllib does not put request headers in its exceptions.
  - The FAULT text and the exit message pass through a redaction step that replaces the key with `[REDACTED]`, in case any message echoes it.
- **Recorded.** `search_log.json` records only `s2_key_used`: `true`/`false` per start (keyed by the `run_dates` entry).
- **Unset.** If the variable is unset or empty, the behaviour is exactly that of §2. The transport is called with the URL alone, as before.
- **Operator.** The key is held only in the RAM-only file `/dev/shm/s2key` (tmpfs, mode 600, never on disk, outside the repo). At the resume the operator loads it inside the tmux shell with `export S2_API_KEY="$(cat /dev/shm/s2key)"`. The key is never echoed, never typed on a logged command line and never printed. After the run the operator deletes `/dev/shm/s2key`. Whether a key was used is reported only through `s2_key_used`.
- **Effect on the result.** None, given the same API answers. A key changes only the rate limit applied to the requests, not which records the API returns for a query.

## 3. How retries count against the 400-request cap

- The existing counter semantics hold (RULE l.546, CC-210b W2). The counter counts **live requests per URL**: each URL that is not replayed from the cache or the 404 log adds 1 to `n_api` (or `n_pdf`) once, before its first attempt. Retries of the same URL do not add to the counter.
- Each logged entry now also records `attempts` and `waited_s`, so the number of HTTP attempts is visible in `search_log.json`.
- The cap is still a total over the start and the resume: the resume seeds its counter from the live (non-cached) entries already logged.
- For this OUT that is **6**: the five 200s plus the one 429.
- The re-query of the logged 429 URL is one new live request (7). The 5 cached 200s replay without counting.
- The wall cap is still checked before each live request, per start. Waits inside one URL's retries can overshoot it by at most 1,800 s (disclosed; RULE l.548).

## 4. The one resume runs on the amended code

> **The one resume of RULE §1.1 for the OUT `/home/hoanguyen/vsps_balpha_runs/b_alpha_run1` runs on the code of the commit that carries this amendment.**

For this OUT only, this supersedes 'same frozen files' in RULE_v3 l.485 and l.548: the frozen files of the resume are those of the amendment commit (RULE_v3.md, patterns.json and english_words.txt unchanged; b_alpha.py and amendment_1.json amended). RULE_v3 '## Amendments (none ...)' and the RULE status lines are not edited; this file and its commit govern (CC-209b r4, CC-209c r6 precedent).

- It is the same OUT, the same frozen `patterns.json`, `english_words.txt` and RULE_v3.md, and the same `search_log.json` and cache.
- It is not a second resume, not a new OUT, and not a rerun after `cells.json`.
- The resume re-checks the amended `SHA256SUMS` (scripts: b_alpha.py, amendment_1.json, english_words.txt, patterns.json; prereg: RULE_v3.md, AMENDMENT_1.md) and the §2.1 equality.
- It sha-checks the 5 cached responses against `search_log.json`.
- It reuses `toolcheck.json` (pass true; T1/T2 extraction is unaffected by this amendment).
- It records `s2_key_used` for the resume start (§2a).
- **What the code does on the resume (verified in the selftest, E2E o12/o13):**
  - the 5 logged HTTP 200 URLs are served from the cache and are not re-queried;
  - the logged HTTP 429 URL is re-queried live, because only 2xx responses are cached and only 404s are replayed from the log;
  - after a 429 burst, a 200 or 404 completes S1;
  - a 429 that persists through 10 attempts or the 1,800 s wait cap is a FAULT at S1. Since this is the one resume, that FAULT is final (`resumable` false), and continuing needs a further amendment or a pivot (§9). This would happen before any population text is read.

## 5. Operator

- Before the resume, append a LOG line that records `sha256sum -c` OK on both amended SUMS, `git status --porcelain` empty for `scripts/b_alpha` and the committed prereg paths, the offline selftest ok, and the commit id.
- If the key is used, load it inside the tmux shell with `export S2_API_KEY="$(cat /dev/shm/s2key)"` (§2a; never echo it). The pre-resume LOG line also records that `/dev/shm/s2key` is mode 600 on tmpfs, outside the repo, and that the offline selftest was run with the key loaded (it isolates the key).
- After the run, delete `/dev/shm/s2key` and record that in the post-run LOG line.
- Then run, in tmux on AC power: `python3 -I -B scripts/b_alpha/b_alpha.py run --run --resume --out /home/hoanguyen/vsps_balpha_runs/b_alpha_run1`.
- The OUT is never deleted, renamed or replaced (RULE l.549).

## 6. Disclosure

- **No result was seen before this amendment.** No candidate list exists, and the only data in the OUT are 5 API responses: two dataset-record resolutions, two citing-work pages and one more resolution. No operator or writer has opened them.
- The amendment changes only how long the job waits for Semantic Scholar. Given the same API answers it cannot change which papers are found. Retries can only turn a transient S2 error into an answer; this also applies to PDF URLs on *.semanticscholar.org hosts (openAccessPdf), where a transient 5xx may now yield a PDF instead of fetch_fail. Non-HTTP errors on S2 (timeout, connection reset, truncated response) are still not retried and are a final FAULT on the one resume.
- AI-designed, not expert-validated (PI-1026bg).

**§8.1 addendum (CC-210f ruling 6)**

| When (UTC) | Who | What | Population contact |
|---|---|---|---|
| 2026-11-01 ~00:33Z | CC-210f judge | documentation only (RULE l.55, amendment commit day): help.openalex.org/api-entities/works/filter-works (last updated 2026-10-29), …/works/search-works (2026-10-28; `filter=field.search:` deprecated, still works; `title_and_abstract.search` still named; `search.title_and_abstract` documented), help.openalex.org/data/work-types (2026-10-26); 3 curl with the placeholder contact, no WebFetch; page shas byte-identical to the CC-210c/CC-210d reads; plus a loopback-only (127.0.0.1) urllib redirect probe, not a web call | none (no population record, no S1/S2 request) |
