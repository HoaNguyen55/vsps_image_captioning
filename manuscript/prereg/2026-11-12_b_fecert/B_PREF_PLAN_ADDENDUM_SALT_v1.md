# Addendum to B_PREF_LABELLING_PLAN_v1_1.md: salted question ids and the instruction slot (v1, 2026-11-12)

Amends `B_PREF_LABELLING_PLAN_v1_1.md` (sha256 `59ae449be9fefb45af2bd78e02894cf6beab861579b5080eab543e41b3db61d0`) for CC-361 BLOCKING D15 and D16 (ruling 2(c), ruling 6). Nothing else in the plan changes. To be read on its own (REVERSIBLE tier) and registered **before any `build_pairs.py` run on real files**. It is a gate condition on the build, the pin package, serving and labelling, not on the stage-0b commit.

## 1. Question ids (D15)

**Registered rule (plan §9, `build_pairs.py` item):** `qid = sha256(f"{SEED}|{part}|{image}|{a}|{b}")[:12]`, SEED = 20261112.

**Why it changes.** Every input of that hash is public or guessable: the seed is in the plan, the image id is in the served image path, and a and b are two of 33 own `-short` file names. A rater who reads the page source could hash every candidate (about 33 × 32 × 3 per screen) and recover which systems wrote the two captions and which screens are repeats. That breaks the blinding of plan §3.2.

**New rule.** `qid = sha256(f"{SALT}|{SEED}|{part}|{image}|{a}|{b}")[:12]`, where:
- `SALT = secrets.token_hex(16)` (128 random bits from the operating system), drawn once per build, inside `build_pairs.build`, on the build host;
- part, image, a, b and SEED are as before; `repeat_of` uses the same SALT with part `main`.

The draw order of plan §2.4 (one `random.Random(20261112)`) is unchanged: the salt touches only the qid, never which pairs, sides, order or repeats are drawn. Two builds on the same inputs therefore give the same screens, sides and order, and different qids. Stage H takes the main pairs in sorted-qid order, so the κ bootstrap interval of plan §5.4 is drawn in salted-qid order; it is reproducible from the committed key.json.

**Self-test only:** the self-tests inject the fixed salt `"5a17" * 8`, so that `build_pairs.py --selftest` gives equal fixture sha256 across two processes. A further self-test check builds twice without an injected salt and requires two different salts and disjoint qid sets. The fixed salt is never used on real files: `build_pairs.py` has no command-line option for a salt.

## 2. What `key.json` holds

`key.json` = `{"salt": SALT, "items": {qid: {image, part, stratum, a, b, file_left, file_right, d_syl, d_word, d_pk, repeat_of}}}`.

- The salt is written **only** to `key.json`. It is not in `assignment.json`, `practice.json`, `BUILD.json`, `ITEMS_MANIFEST.tsv` or stdout (self-test check).
- `BUILD.json` logs the sha256 of `key.json` at build time, as before, so the salt is fixed from the build onward.

## 3. When it is committed

As plan §6 says for `key.json`: never before the closing line. The salt is committed with `key.json` after the closing LOG line, so that anyone can then recompute every qid from the key. Until then the PI, as a rater, does not open `key.json`, and agents read only its sha256.

## 4. The instruction slot of `pair.html` (D16)

- `pair.html` carries the registered Vietnamese block of `B_PREF_INSTRUCTIONS_VI_v1.md` (file sha256 `68466875ea6d0501493e5344bebcf9ca9716aa59dbe9ed878737fbdda0c369a5`; block sha256 `45d59b54ecc70e31cf142e87c251e425005b87bb9d6c928f27c809923e87d5bf`; CC-364) between the markers `<!--BEGIN-VI-INSTRUCTIONS-->` and `<!--END-VI-INSTRUCTIONS-->`: six `<li>` items and one `<p>`.
- At start, `pair_server.py` recomputes the block from the page, following the registration's byte rule: `"N. " + textContent of <li> N` for N = 1 to 6, then the textContent of the paragraph, each followed by LF. It compares the result with `45d59b54…` and refuses to start on any difference. The page bytes it checked are the bytes it serves.
- The rest of D16 is met: the one-judge fidelity read (CC-364), the blind back-translation of line 5 (OPS-1112bo) and the PI's meaning check (PI-1112e). Labelling still waits for the other conditions of CC-361 ruling 4.
