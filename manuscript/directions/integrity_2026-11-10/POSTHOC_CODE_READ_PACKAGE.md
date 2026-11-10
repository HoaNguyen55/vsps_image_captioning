# Post hoc rows C1, C2, B1, B2: code-read package (gate 3)

Stamp 2026-11-10T20:13:59Z. Code read under CC-315 (b), conditions R1-R4. Plan `POSTHOC_ROWS_PLAN_v1_1.md` (91a357c0); `PY`, `RUN`, `SCR`, `IDS`, `POST` as there. No row was computed. No real ledger, decide file or B2 record was opened or hashed. Fixtures are synthetic (`fix_*` in `selftest.py`, seed 20261110).

## Files in `scripts/posthoc_1110/`

| file | sha256 |
|---|---|
| `posthoc_rows.py` | 8e84d392b4dfc8d9695a765614d242a72b2f9623e40c0220837ce5a1092fd267 |
| `selftest.py` | 777ea8c218c7c6c17b5d52e4c7c9edc6d6e3c129b4fc3014636eaa553e95aa2b |
| `mutants.py` | 2a36e109b8a8132d4e0566b4929776909aa439e60761828fdc0d1fb03c2902a9 |
| `SELFTEST_OUTPUT.txt` | 060e976fb4efbcfb90c2b8aaf97ce92e6cfc6d0ebaf866111166cd2a3faffb53 |
| `SHA256SUMS` | e19d2cf7a87f3f24eeb413704392194c754c2217bf63f8ca1e7f925c42e7252f |

Venv for every row and test: `~/.venvs/c_stage1_lists` (Python 3.12.3, numpy 2.5.4), `-I -B`.

## Rule to code (`posthoc_rows.py`)

| rule | where |
|---|---|
| R1 hook armed before any registered import; logs each open under the data roots | `arm` :132-147, `run` :281, output key `opened` |
| R1 roots, exemption, sealed and name stops | `SCOPE` :32, `EXEMPT` :33, `DENY` :34, `refusal` :121 |
| R1 fixed allow-list: inputs, pin, output, script, import chain | `ROWS` :42, `CHAIN` :95 |
| R1 a swallowed stop still stops; one row per process; no `.pyc` | :298, :276, :23 |
| R2 statement | `NOTE` :38, :294 |
| R3 COCO only | `ROWS["c2"]` :55; no other C2 row |
| R4 label, no verdict, `POST`, once, one stdout line | :290, :27, :274, :304 |
| Rules 1-2: registered block copied unchanged | :189, :211, :243, :266 |
| Rule 3: reported whatever the value | `run` never branches on the estimate |
| Rule 4: registered estimator, B, seed | C1 `DD.gate` :180; C2 `ci`, `draws` :211; B1 :224, :231, :234; B2 :255 |
| Rule 5: sha first; fixed `--ids`, `--out` | :284, :315 |
| Rule 6: identity within 1e-9 | `same` :157; C1 :184, C2 :206, B1 :237, B2 :262 |
| Rule 7: gate order | not code |
| Pinned list is the only exclusion source | :286, `kept` :150 |
| CC-315 item 6, Ruling 7 (B2) | :251, :260, :265 |

The R2 and Ruling 7 sentence wording is carried to gate 6.

## Results (`SELFTEST_OUTPUT.txt`)

- Selftest: `selftest ok`, about 20 s, 19 fixture runs, each a fresh process. The audit list must equal the declared files exactly (this enumerates the import chain). Undeclared, swallowed and denied opens stop the row, as do a wrong sha, pinned id, n or identity value and a second run. Planted values give exact literals only when exactly the pinned ids are removed.
- C1's fixture uses the real pinned order and 12-id pin with synthetic scores; the 12 ids lie inside the 1,941. Pin sizes: 12, 1, 7, 16.
- Mutants: 52 of 52 killed; the control passes. aislop: 100.

## Commands after a code-read GO (from `RUN`, once each)

```
PY SCR/posthoc_rows.py c1 --ids IDS/pin_c_ov_test_ret_union.txt --out POST/c1_ov_test_posthoc.json
PY SCR/posthoc_rows.py c2 --ids IDS/pin_c2_coco_test_ret_union.txt --out POST/c2_coco_posthoc.json
PY SCR/posthoc_rows.py b1 --ids IDS/pin_k_ktvic_dev300.txt --out POST/b1_mask7_posthoc.json
PY SCR/posthoc_rows.py b2 --ids IDS/pin_k_ktvic_test.txt --out POST/b2_ktvic_test_posthoc.json
```

Each prints one line (path, sha256, n; no estimate) for the operator's OPS line. Runtime: seconds per row; C1 ran at the real n on a fixture, C2 (5,000 images) is an estimate, under 15 s.

## Open questions and disclosed choices

1. One script with a ROW argument (321 lines) replaces the plan's four scripts and line caps.
2. B2 identity is at four decimals, as the plan's constants; rule 6 asks 1e-9. The `result_sha256` check is an addition from CC-315 item 6.
3. `cider_3seed_mean.json` is sha-checked, never parsed; the plan gives it no role.
4. A stopped row exits with its reason and writes no file. Does a stop use up "run once"?
5. R1 names are `annotation-test|preds|caption`, matched on the file name outside interpreter `lib` folders. Other caption files stop only inside the five roots.
6. C2's import chain opens `data/coco_probe/chair_synonyms.txt` (a lexicon), allow-listed. C2 and B1 chain files are fixed by path, not sha-checked at run time; C1's are, by `ctest.check_pins`.
7. Ops (needs an OPS line): the gatekeeper n-gram scan ran once on this file; it parses the caption files in `data/datasets/` (KTVIC, OpenViIC with test annotations, UIT-ViIC, COCO Karpathy). Counts only, 0 hits; not needed here.
