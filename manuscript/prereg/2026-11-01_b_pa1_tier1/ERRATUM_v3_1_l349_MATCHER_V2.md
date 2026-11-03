# Erratum to B-PA1-T1 prereg v3.1, l.349 ("matcher v2")

Status: **DRAFT for the CC-230 round-2 read; not pinned, not committed.** Written 2026-11-02T23:05Z (`date -u`).
Label: `TIER 1 / DEV-EXPLORE (B-PA1-T1)`.
Amends: `manuscript/prereg/2026-11-01_b_pa1_tier1/PREREG_DRAFT_v3_1.md`, sha256 `e9b30ca7…` (commit 5ff00c9). v3.1 itself
is not edited. This erratum takes effect when the gatekeeper pins its sha on the r3b line (below), before the map v1
build start line. Basis: CC-230 Ruling 1 and W1 (B-1 upheld).

## (a) Text

**Old (v3.1 l.349, verbatim):**
> - Matcher v2 = Paper A's Vietnamese matcher (`rescap/chair.py` `e47d249a`; lexicon file set pinned at registration, R3).

**New:**
> - Matcher v2 = Paper A's Vietnamese COCO-80 matcher: `scripts/score_coco_probe.py` `vi_objects(caption, terms,
>   "v2")`, that is, the LEX_V2 rewrites, then `vi_classes` over `load_vi_terms()` of `data/coco_probe/coco80_vi.json`
>   `926e0857`. It is used together with A's English synonym list `data/coco_probe/chair_synonyms.txt` `b685537b` (read
>   by `load_synonyms`, used for the Objects365 → COCO-80 crosswalk). It loads the rescap file set pinned on LOG l.1246
>   (12 files, including `rescap/chair.py` `e47d249a` for `norm_tone` and `rescap/vi/lexicon.py` `fbc945f2` for
>   CLASSIFIERS). Files pinned at R3 (LOG l.1246) plus the R3 addendum (r3b line). `RESCAP_RAW_TONE` stays unset.

## (b) Evidence

- `rescap/chair.py` l.150 `objects_in` returns head nouns of the KTVIC lexicon (`NOUN_CLASSIFIER`), not COCO-80
  classes, so it cannot produce the §6.3 mentions ("a distinct COCO-80 class named in one reference").
- CC-114 l.42: "matcher v2 = LEX_V2 rewrites + the lexicon, v1 = the lexicon alone" (`score_coco_probe`).
- `scripts/g2b/score_g2b.py` l.43: Paper A's `MATCH["coco80"]["vi"] = sc.vi_objects(c, VI_TERMS)`.
- v3.1 §6.1 l.327-328 already names "Paper A's tone-normalised COCO-80 lexicon (matcher v2, cited as A)". l.349 is a
  citation slip against the prereg's own text.
- `score_coco_probe.py` (a0accb5, 2026-10-13T23:47Z), `coco80_vi.json` (ee7cad1, 2026-10-12T07:33Z) and
  `chair_synonyms.txt` (1f30d09, 2026-08-30) are tracked and unchanged against HEAD. All three predate the Objects365
  class list (extracted 2026-11-02T11:09:57Z).

## (c) Supersession

From the r3b pin of this file:
- CC-228 Ruling 4(c) (l.99), where "List each file that matcher v2 loads, found by importing rescap.chair" is read
  with matcher v2 as defined in (a);
- the note "chair.py = v3.1 l.349 e47d249a" on LOG l.1246 (OPS-1102b-r3-pin). The pinned rescap files stay pinned and
  unchanged; the note's identification of matcher v2 is superseded.

## (d) Disclosure: the crosswalk also makes the main rows

v3.1 §6.1 l.330 presents the Objects365 → COCO-80 crosswalk as serving "parity gate and the COCO-80 sensitivity only".
In map v1 as built by `scripts/b_pa1/map_v1.py` (`build_docs`, the `rows = …` line), every Vietnamese term of A's
lexicon gets one VN → Objects365 row per Objects365 class that the crosswalk links to the term's COCO-80 class. So the
crosswalk also generates the main-analysis VN → Objects365 rows of map v1. Because the crosswalk is frozen with map v1
(l.23) and amendments are add-only (l.336-343), a wrong or missing link would be permanent in the main rows. This is
why the §6.1 alias amendment (`AMENDMENT_6_1_CROSSWALK_ALIAS.md`) adds strikes and makes aliases and the Q1 read
mandatory before the freeze.

## (e) Related registered-text readings (CC-230 Ruling 9, N4)

The registered §6.3 statistic (v2 side unrestricted) governs. It supersedes the "COCO-80 overlap" wording of CC-213r2
N3 (l.118-119) and of `B_DIRECTION_v3_2026-11-01.md` l.150. Under the overlap reading Δ ≡ 0 and the gate would test
nothing.

## Pin line (gatekeeper; before the map v1 build start line)

`<date -u> OPS-1102b-r3b-pin: PIN scripts/score_coco_probe.py d11db7e192f689980bb2b2bb717d852d9aa339ad857ce9411fe7bdd6fe416070 PIN data/coco_probe/coco80_vi.json 926e08571ef6e80a7f8aae8f2b73753d6c5c54c431a750ba2b67bfaae71b540b PIN data/coco_probe/chair_synonyms.txt b685537b36fe21b791c87151b96a991ceb582edff19f3da204dcc7a7905502f2 PIN manuscript/prereg/2026-11-01_b_pa1_tier1/ERRATUM_v3_1_l349_MATCHER_V2.md <full sha of this file> (R3 addendum: matcher v2 = score_coco_probe.vi_objects lexicon v2 + the rescap files of LOG l.1246; erratum to v3.1 l.349 per CC-230 W1, superseding CC-228 Ruling 4(c) and the l.1246 chair.py note; all tracked, git diff HEAD empty; RESCAP_RAW_TONE unset)`
