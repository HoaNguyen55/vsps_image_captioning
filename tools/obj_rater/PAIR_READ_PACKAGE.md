# Pair tool: read package (Paper B pairwise preferences; plan `B_PREF_LABELLING_PLAN_v1_1.md` sha256 59ae449b…)

Files written only, never run. CC-353 4(e) bars building on real files, serving or testing the page or server, and every
self-test until the IRREVERSIBLE-tier code read. On the laptop only `py_compile` was run, with the cache prefix in the
scratchpad. `server.py`, `rater.html` and `build_assignment.py` are unchanged (e3beb936, 84a90787, 497e5747).

| File | Derived from | Plan |
|---|---|---|
| `pair_server.py` | `server.py` | §9 pair_server 1-6; CC-353 W8 |
| `pair.html` | `rater.html` | §9 pair.html 1-7; §3.2; §4; CC-353 N6b |
| `build_pairs.py` | `build_assignment.py`, `build_topup.py` (self-test style) | §2.1, §2.3, §2.4, §3.1, §6, §9 build_pairs 1-4 |

## Contract for `PAIR_CANDIDATES.json` (stage 1 must write this; `scripts/b_fecert/` does not exist yet)

```
{"epsilon": 10.0,
 "images": {"<KTVIC image id, digits>": [{"a": "<name>-short", "b": "<name>-short", "stratum": "P"|"U"|"C",
                                          "d_syl": <float>, "d_word": <float>, "d_pk": <float>}, ...]}}
```
d = CIDEr-D(a) − CIDEr-D(b) × 100 per image (plan §2.2). An image with no candidate may be listed with `[]` or
omitted; it is never drawn. Precondition: the build host has the KTVIC `images/` folder beside `--test-json` (every
candidate image file must exist). Captions are read from `<preds-dir>/<name>.preds.json`
(`{image_id: str | [str, ...]}`; the first element is used, as in `ptb_protocol.load_preds`).

## What `build_pairs.py` checks before drawing (it stops; it never filters)

- `epsilon` = 10.0. Each name ends in `-short`. Each image id is digits, is in `test_data.json :: images`, has a
  `filename` matching `[0-9]{11}\.(jpg|jpeg|png)`, and that file exists under `images/`.
- Per image, no candidate repeats. `a` ≠ `b`. The stated stratum equals the stratum recomputed from the three d values
  at ε = 10 (plan §2.3).
- Both display texts are non-empty and differ in ≥ 2 lower-cased tokens (multiset symmetric difference).
- **Not re-checked: different families.** The builder has only the three registered inputs, so B_KAPPA §4.3 and the
  stage-C family column stay with stage 1.

## Order of the `rng` calls (one `random.Random(20261112)`; ids sorted as integers)

1. Step 3: `rng.sample` for P from the sorted E_P, then U from the sorted E_U minus the drawn images, then C likewise.
   The size is min(quota, pool). Each drawn set is then sorted.
2. Step 4: `rng.choice` per image in this order: P images, U images, C images. The candidates of the image's stratum
   are sorted by (a, b).
3. Step 6: `rng.random() < 0.5` per pair in the same order; True puts file a on the left.
4. Step 7: `rng.shuffle` of the main pairs.
5. Step 8: the repeat pool is the main pairs at shuffled positions 0 … n − 100. A pair only reaches this pool if a
   position 100 screens after its first showing exists. Then:
   - `rng.sample(pool, min(30, |pool|))`;
   - for each sampled pair in sample order, `rng.randint(f + 100, len(seq))` gives the insertion index, where f is the
     pair's current position;
   - the repeat's sides are swapped.

   A later insertion can only widen an earlier gap, so every gap stays ≥ 100. With fewer than 100 main pairs the pool
   is empty and there are no repeats (no loop, no crash).
6. Step 9: `rng.sample` of 8 from the sorted images that have a candidate and were not drawn. For each, in id order:
   `rng.choice` over all its candidates, then `rng.random()` for the side.

qid = `sha256(f"{SEED}|{part}|{image}|{a}|{b}")[:12]`, where part is `main`, `repeat` or `practice` and (a, b) is the
candidate's order (not the side). Served `sid` = qid, and no `part` field is served.

## Points where the plan or the task was ambiguous (reading coded)

1. **Instruction text.** §4 registers only the English gist of items 1-6. Vietnamese is registered only for the
   question and the four answer names. The page shows the six English sentences byte-for-byte, with `**` rendered as
   `<b>`, plus the §2.4 l.65 time sentence for N6b. **No Vietnamese translation was written, because it would be
   unregistered text.** A registered Vietnamese text is needed before labelling; this does not block the code read.
2. **Record name.** The task said `BUILD_PAIRS.json`; plan §6, §9.3 and §9.5 say `BUILD.json`. The code uses the plan's
   name through one constant (`pair_server.BUILD_RECORD`), and writes the plan's five outputs.
3. **Endpoint sentence in §9 build_pairs 4.** The self-test opens no socket. Instead:
   - the fixture holds `.png`, `.jpeg` and `.jpg` images, and all three are drawn;
   - `pair_server.check_start` is called in-process to check the content types and every start refusal.

   The HTTP endpoint test stays a host check (plan §9).
4. **Served `meta`.** "counts" is read as `n_screens` only. No per-stratum count is served (§3.2, §6).
5. **`test_data.json`.** Only `images[].id` and `images[].filename` are read; `annotations` is never touched. The key
   name `id` was not verified, because the file was not opened (one-look set). A missing key fails loudly.
6. **Image whitelist.** The server lists every `filename` of `test_data.json` (plan item 2), not only the images in the
   assignment. `test_data.json` must sit beside `--images`.
7. **Repeat pool and rng order:** see above. §2.4 fixes neither.
8. **Start refusals.** `pair_server.py` stops in each of these cases:
   - port 8790 or 8791;
   - `--dir` under `/mnt` or `~/vsps_labels/` (compared by path components, so `~/vsps_labels_b` passes; the unresolved
     path is checked before `resolve()`, so `~/vsps_labels` is never stat'ed);
   - the sha256 of `assignment.json`, `practice.json` or `key.json` differs from `BUILD.json`.

   It does not require `--dir` to be under `~/vsps_labels_b/`.
9. **Blinding weakness (for the judge).** The registered qid pattern is an unsalted hash of a public seed, the image
   and two of 33 public file names. A rater who reads the page source could recover the system names and which
   screens are repeats by brute force (about 33 × 32 × 3 hashes per screen). Kept as registered.
   Recommendation: a secret salt kept only in `key.json`, which needs a plan amendment.
10. **Asserts.** `server.py` uses `assert` for its refusals. The new files use `raise SystemExit("STOP: …")`, so the
    checks survive `python -O`.

## Self-test checks (`build_pairs.py --selftest`; on the host named at the code read, not on the laptop)

1. display normalisation on toy strings: NFC, '_', the 25 White_Space characters only, the final run, the first letter
2. strata from the d values at ε 10: P, U, C, both flips, below the margin
3. refuses an --out under /mnt
4. refuses an --out under ~/vsps_labels/
5. refuses to overwrite an existing --out
6. stops when a stratum disagrees with its d values
7. stops on a file paired with itself
8. stops on a file that is not -short
9. stops on an image outside the test file
10. stops when the display texts differ in fewer than 2 tokens
11. quotas P 100, U 160; a C shortfall takes all
12. one pair per image; images disjoint across strata and practice
13. every pair is a candidate of its own stratum
14. left/right balance within 3 sd
15. 30 repeats, sides swapped, each ≥ 100 screens after its first showing
16. qids unique; qid formula
17. served files: no file name, stratum, score, role or reference; one q per screen
18. served captions = the display text of the keyed left and right files
19. 8 practice pairs from images not drawn for the main set
20. every image path exists; .jpg, .jpeg and .png all drawn
21. no caption or reference text in key.json, BUILD.json, the manifest or stdout
22. manifest: qid and image id only
23. BUILD.json holds every input and output sha256
24. determinism: two builds byte-equal
25. pair_server content types
26. pair_server refuses 8790 and 8791
27. pair_server refuses a --dir under /mnt or ~/vsps_labels/
28. pair_server refuses to start when key.json differs from BUILD.json

Still open for the host (plan §9): the HTTP endpoint test (private files not served; a bad label, a bad qid and an image
outside the regex refused; `.png` served), the headless practice-round page test, and the load test.

---

# Round 2 (CC-361)

Diff base: `.session_backup/2026-11-12/b_fecert/code_r1/tools/obj_rater/` (unchanged). The unified diff is `tools/obj_rater/PAIR_R1_R2.diff`. File shas are in `tools/obj_rater/PAIR_SHA256SUMS` (NB9). `server.py`, `rater.html`, `build_assignment.py` and `build_topup.py` are byte-identical. **Nothing of round 2 has run** (hc2 deleted 15:47Z), and the D18 records are OWED. The recipe and the expected counts are in `scripts/b_fecert/READ_PACKAGE.md` (Round 2, D18). For this tool:
- `build_pairs.py --selftest` must give `SELFTEST PASS 39/39`, twice, with equal `fixture sha256` lines;
- the pair-tool mutants are R5 and R27-R34 in `scripts/b_fecert/mutants.py`, inside `killed 94 of 94`.

| D / NB | What changed | Where | Check (build_pairs --selftest unless named) | Mutant |
|---|---|---|---|---|
| D3 | `load_inputs` STOPs unless PAIR_CANDIDATES.json is `{epsilon: 10.0, eligible_images: {P,U,C}, images: {id: [...]}}` and every candidate is exactly `{a, b, stratum, d_syl, d_word, d_pk}`. Image names come only from `test_data.json :: images[].filename`. | build_pairs.py l.85-97 | "stops on a candidate field outside …"; b_fecert `pairs_integration` (stage 1 → build → H) | R5 |
| D4 | key.json = `{"salt", "items": {qid: {image, part, stratum, a, b, file_left, file_right, d_syl, d_word, d_pk, repeat_of}}}`, the contract b_fecert stage H reads (`key_items`). | build_pairs.py `build` | "key.json = {salt, items} …"; b_fecert `key_contract` | R6-R8 (b_fecert side) |
| D14 | The image-file existence check is dropped from build_pairs; the regex and test_data membership checks stay. `pair_server.check_start` STOPs unless every assignment and practice image is listed in test_data.json and exists under `--images` on the laptop. | build_pairs.py l.108-109; pair_server.py l.99-103 | "built with no images folder …"; "pair_server refuses to start when a served image is missing on the laptop" | R29 |
| D15 | `qid(salt, part, image, a, b) = sha256(f"{salt}|{SEED}|{part}|{image}|{a}|{b}")[:12]`. `build(..., salt=None)` draws `secrets.token_hex(16)`. There is no CLI option for a salt. The self-test injects `FIX_SALT = "5a17" * 8`. The salt is written only to key.json. Addendum: `manuscript/prereg/2026-11-12_b_fecert/B_PREF_PLAN_ADDENDUM_SALT_v1.md`. | build_pairs.py l.44, l.80, l.123 ff. | "qids … salted, never unsalted"; "the salt is only in key.json …"; "with no injected salt each build draws a fresh 128-bit secret"; two-process fixture shas; b_fecert `key_contract` | R27, R28 |
| D16 | pair.html carries the registered block of `B_PREF_INSTRUCTIONS_VI_v1.md` (68466875…, CC-364) between `<!--BEGIN-VI-INSTRUCTIONS-->` and `<!--END-VI-INSTRUCTIONS-->`: six `<li>` and one `<p>`, which replace the English gist and the English time sentence. `pair_server.instructions_block` recomputes `"N. " + li text` (N = 1-6) and the `<p>` text, each with LF, and `check_start` refuses unless the sha256 equals `45d59b54…`. The checked bytes are the bytes served (`make_handler(..., page)`). On the laptop, sed/awk over pair.html gives `45d59b54…`. Labelling still waits for the back-translation, the PI check and the fidelity read (ruling 2(b)). | pair.html l.47-57; pair_server.py l.36-40, l.62-73, l.76-104, l.115 | "pair_server starts on the built fixture with the real pair.html"; "pair.html carries the registered Vietnamese block …"; "… differs by one character" ×2 (item 2 and the time line) | R30 (one character altered in pair.html), R31 |
| NB5 | `check_start` STOPs unless `--annotator` is PI or R2 and `--dir` is under `~/vsps_labels_b/` (testable root argument). The old annotator regex is removed. "One server at a time" stays procedural. | pair_server.py l.32, l.76 ff. | "pair_server: --annotator PI or R2 only"; "… or outside ~/vsps_labels_b/" | R32, R33 |
| NB9 | Required `--candidates-sha` (the sha on the stage pin line, which now carries PAIR_CANDIDATES.json). `PAIR_SHA256SUMS` added. | build_pairs.py l.88-90, `main` | "stops when PAIR_CANDIDATES.json differs from --candidates-sha" | R34 |

Round 2b (h2, 2026-11-13): test side only. `stops()` treats any other exception as "not refused", so mutant R5 now FAILs by name. Expected counts are unchanged: PASS 39/39 twice, and killed 94 of 94 in the b_fecert mutant run. The 03:09Z record run (`scripts/b_fecert/host_checks_r2/`) killed 92 of 94 (R5, R8 survived).

Not literal, or for the panel:
1. `check_start` now returns `(served types, page bytes)` and takes `annotator`, `labels_root` and `page_path`, so that the self-test can reach every refusal without a socket.
2. The ten round-1 ambiguities: points 1 (instructions), 3 (endpoint test, ruling 3(c)), 8 (start refusals) and 9 (salt) are closed as above. Points 2, 4, 5, 6, 7 and 10 still await an explicit ruling (NB19).
3. The endpoint, headless and load tests stay after stage 0b (ruling 3(c)).
