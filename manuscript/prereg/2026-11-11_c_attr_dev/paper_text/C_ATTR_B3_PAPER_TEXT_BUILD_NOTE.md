# Build note: block-3 paper-text package v1 and the W1 recompute script

Written 2026-11-13 (UTC). DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY. Nothing committed, staged or stashed; the paper repo was read only. No LOG or CC file written. AI opinion, not expert-validated.

## Files
- `C_ATTR_B3_PAPER_TEXT_v1.md`: the package (placement, ruled sentences beside their paper-ready forms, E1–E16, shells C1/C2, 127 manifest rows and the placeholder → display map, transfer gates, what is not changed, open points J-B3-1 to J-B3-12, conflicts with the 1b guards).
- `c_attr_b3_ledger_recompute.py`: the W1 recompute (stdlib + numpy), for a reader named by a judge.
- `SHA256SUMS_B3_PAPER_TEXT`: sums of the three files above.

## What I verified
- CC-378 sha `b78f184b…` = the brief's. Paper repo HEAD `44bbdd9979ea…`; the nine paper files equal the CC-365 TARGET shas (03, 05, 06, 07, 09, 11, manifest, bib, audit).
- `data/results/c_attr_1113_b3score/`: `sha256sum -c SHA256SUMS` 28/28 OK; B3_SUMMARY `61bf697b`, K5 `bd9b0158` and the decode files equal CC-378 ruling 8. The folder is untracked at writing (gatekeeper commit in progress).
- Every number in the package was read from its file by one `python3 -I` script in my scratchpad (JSON/TSV/log status lines only) and printed in the house format. Labels, d, bounds and p agree with CC-378 ruling 4's orientation values. Rounding: p 0.8095952 → "0.810" (three significant digits).
- Each E-row OLD occurs exactly once at HEAD. The 16 rows apply in order to scratch copies (`git show HEAD:`), and each NEW occurs once afterwards. A fill pass on those copies from the placeholder map (§5.1 of the package) left no unfilled or unmapped placeholder, and I read the filled 03, 06 and 11 text. Both erratum-E6 strings are unbroken in 03 (one each) and 06 (Table 18 caption). Placeholder braces balance. The added lines hold no CC/OPS/PI id, no "C-T1", "kit B" or machine label, no "confirm", "RAGCap-style" or "no overlap". The only "test" words are "test set", "self-test" and existing text. The only "validate" words are negated ("does not re-validate").
- Code read for definitions only (not run): `c_attr_score.py` at ca24e13 (`cca5e327`: `pair`, `summary`, `detected`, `label`, `b3_rows`, `st_b3k5`, `st_b3rest`, `B3_EST`) and `c_attr.py` (`a3bd7b93`: `set_columns`, `read_ledgers`, `boot_idx` with B = 2,000 and seed 0, `cmd_score` ledger rows, `tag`, `lmcap_query`, `rices_content`).
- `c_attr_b3_ledger_recompute.py` byte-compiles (`python3 -X pycache_prefix=<scratchpad> -m py_compile`); no `__pycache__` was written in the repo.

## What I could not verify
- **The recompute itself and its `--selftest`: not run** (brief: no tests; the ledgers are not opened by me). The ledger row layout the script relies on is taken from the code: `run_id`, `dataset`, `variant` (absent or `plain` for plain rows, `masked3` for the frozen rows), `tau` (absent or `"-inf"`), `per_image.ids`, `per_image.cider_s`. If the ledger's `run_id` strings differ from the ten registered ids of run doc v1.1 §2, the script prints FAIL for every affected row, with no values, and the matter goes to a judge.
- The sha256 of `led/b3_ov_dev_b.jsonl` and `led/b3_xm_dev500.jsonl` is not pinned in any file I could read. The script refuses a `k5.jsonl` that is not `87c2ef2c…` (K5.json `inputs`) and a B3_SUMMARY that is not `61bf697b…`. For the other two it prints their sha256, and the reader checks them against the OPS-1113ao folder digest.
- **numpy version.** The scoring environment is recorded only as an importlib.metadata listing hash (`e95831b6…`). Its numpy version is not visible to me. `default_rng(0).integers` streams are not promised stable across numpy versions. The script prints its numpy version. A FAIL on every row with plausible-looking diffs would point to a stream mismatch, not to a wrong number. The safest reader environment is the scoring venv's freeze.
- The manifest rows are keyed to `data/results/c_attr_1113_b3score/…` paths, which are valid only after the gatekeeper's records commit.
- One existing sentence was made false by the record, not by block 3's results: 05 "Files and order" says that each run document was committed before the step it governs. The block-3 run-document erratum 1 (reviewed by CC-370 at 19:37:46Z, before the 19:44:24Z relaunch) was committed in ca24e13 at 2026-11-13T00:03:08Z, after the decode ended (23:27:30Z). E16 and the E11 sentence state this; the run document v1.1 and the decode code (60358b2, 18:28:19Z) and the scoring run document and code (ca24e13, before the 00:22Z scoring stages) were on time.

## Read departures and custody (stated, as in CC-371 W1 practice)
- LOG reads: `cut -c1-300` for the lines I grepped (PI-1112e, OPS-1113o/s/x/ac/an–ar, CC-370). One departure: LOG line 2352 (PI-1112e) was read through `cut -c300-1500` to reach item 3 (release scope; contributions). Two `grep -o` reads printed short LOG contexts after `b3_ov_dev_b.jsonl`/`k5.jsonl` (to look for ledger sha pins; none found beyond "k5.jsonl 4 lines, count only").
- Paper and code copies: `git show HEAD:` copies of the six paper files and `git show ca24e13:` copies of `c_attr_score.py` and `c_attr.py` were written to my scratchpad (read and string-replaced there only).
- Files opened under `data/results/c_attr_1113_b3score/`: `res/*.json`, `decode/CAP_3.json`, `STEPS_3.tsv`, both `gpu_seconds*.tsv`, `D1_*.json`, `SHA256SUMS_B3` (names), `job.log` (status lines by grep), `s0_hs/mutants.log` and `selftest.log` (last lines). All are in the CC-378 ruling-8 commit list and free of captions.
- Several read-only commands were issued in parallel (one command at a time was the brief; the parallel ones were small reads of rulings and paper files).
- Not opened: anything under `.session_backup/machines/` (no `led/`, no `in/`), any `.preds.json`, partial, list, caption or reference file, any test-set file, `~/vsps_labels/`, any `key.json`, `data/results/a_cert*/`, `data/results/a_e3/`, `~/.vsps_sealed`. No ledger was hashed.

## Where the recompute may run (question for the judge, J-B3-10)
The PI's rule puts scoring-type computation on the rented host (PI-1111j; the 2026-11-11 rule that self-tests, mutants and CPU scoring run on the rented machine). No host exists now: the block-3 host was deleted after the pull. The recompute is a 2,000 × n integer bootstrap on two sets (n = 925 and 500), a few seconds of CPU. It reads three 0444 ledgers that already sit on the laptop as pull copies and prints no per-image value.
- **Option A (recommended):** a named one-off on the laptop under a judge line, by a reader whose brief permits opening `led/` (CC-378 Q3 says "minutes of CPU on the laptop copy, numbers only"). Run `--selftest` first, then the real call from the pull folder. Log the full stdout in one OPS line.
- **Option B:** the first step on the next rented host, with the three ledgers and B3_SUMMARY pushed and sha-checked. This keeps the rule as written, but the transfer waits until a host exists.
- Either way: if any row FAILs, STOP and take it to a judge (W1). Nothing in the paper repo changes before the PASS or a ruled waiver.
