# Paper B v2: progress (writer, 2026-10-27)

Branch paper-v10, HEAD f8cccb68. Nothing committed. No registered number or verdict changed. Every new number has a src comment and a manifest row. No caption text from KTVIC, OpenViIC or UIT-ViIC was opened or written.

**Backup (INC-1027a).** The whole directory as it was before any edit is in `.session_backup/2026-10-27/paperB_v2/before/`, with 18 files in `SHA256SUMS`. The working files were checked against it right before editing: 18/18 OK.

## 1. What changed (file:line, after-edit line numbers)

| Order | Ruling | File:line | Change |
|---|---|---|---|
| 1 | CC-130 W6, PI-1026af | `sec3_data_and_audit.md:66` | Rewrote l.66's "not for our own models' KTVIC scores". The OpenViIC overlap does not reach our scores, but KTVIC's own duplicates do. |
| 1 | CC-130 W6, PI-1026af | `sec3_data_and_audit.md:68` (new paragraph, "Duplicates inside KTVIC") | Train 3589 = test 1335 and train 7511 = test 507 are byte-identical. dev300 2004 = train 4487. Sources: `exclusion.json` `image_sha256.ktvic_test` (c52a96d1), PREREG §1.1 at f8cccb68 (e44eadc9), CC-130, and the writer's own re-hash. Every model trained on all 3,769 or on the 3,469 images, and every model fine-tuned from one of them, trained on both test twins. The 867- and 1,734-image training-set-size runs hold train 7511 only. The registered 145.15 comes from models trained on bytes identical to 2 of the 558 test images. Disclosed, not re-scored. The count covers byte identity only, and the exploratory CLIP search is cited (11 at cos ≥ 0.95, checked only by eye; see §5 J1). |
| 1 | CC-130 W6 (dev twin) | `sec3_data_and_audit.md:9` | "trained without dev300" became "(by image id; one dev300 image has a byte-identical copy among the 3,469, Section 3.6)". |
| 1 | mirror | `supplementary_B.md:78` (S1, dev300-tuned rules) | The claim "no dev-side number … inflated" is caveated for dev 2004 = train 4487. Only the 867- and 1,734-image runs left 4487 out. S6/S7 dev numbers include that image and were not recomputed. |
| 1 | mirror | `supplementary_B.md:162` (S5, leakage test) | Added a pointer to the within-KTVIC duplicates in §3.6. |
| 1 | mirror | `supplementary_B.md:282` (S7, training-set size) | Only the full-size point (3,469) trained on 4487, the byte twin of dev 2004. That point, and through it the +9.40 slope, "can be biased upward" (CC-130 r4). The slope was not recomputed. |
| 1 | mirror | `supplementary_B.md:284` (S7, training count) | The 3,469 member images include both test twins. Disclosed, not re-scored. |
| 2 | CC-126 W3 | `outline_B.md:8–9` | New abstract (§3 below). It removes 55.12% and "nearly vanishes", puts protocol card + kit first, frames punctuation as a measured protocol hazard, keeps both registered FAILs, and gives the honest external-system sentence with the slot `[B-2: N external systems]`. The old abstract is in the backup. |
| 2 | CC-126 W3 | `sec1_intro.md:7` | Headline sentence: protocol card + kit, built on the audit. |
| 2 | CC-126 W3 | `sec1_intro.md:10` | Item 2 heading: "a measured protocol hazard whose cost depends on the scoring pipeline". |
| 2 | CC-126 W3 / K15 W4 | `sec1_intro.md:12` | Panel item: added "independence not established … a disagreement between panels, not independent support". |
| 2 | CC-126 W3 | `sec1_intro.md:16–18` | Contributions reordered to card → kit → audit. The kit bullet gets the honest external-system count plus the slot. The audit bullet gets "byte duplicates inside KTVIC's own split". |
| 2 | CC-126 W3 | `sec5_results.md:25` | The MBR-3 post hoc row (+3.14, 151.37, +3.05) and the closure-lift sentence were cut from the main text. A one-clause pointer to S7 remains, and its comment records the move. S7 (`supplementary_B.md:285`) already holds the row, the POST_HOC label, the closure-lift sentence and the full src, all unchanged. |
| 2 | CC-126 W3 | `sec8_conclusion.md:5` | Panel sentence: "although the independence of the two panels is not established". |
| 2 | CC-126 W3 | `cover_letter_B.md:14` | The kit is in the headline, with the honest count and the slot. |
| 2 | LRE card | `cover_letter_B.md:20` | Comment placeholder for the Special Focus flag (PI decision). |
| 3 | PI-1026ad/ae | `sec1_intro.md:22`, `sec2_related.md:17`, `sec7_limitations_ethics.md:38, 42`, `new_vs_FAIR.md:42` | Companion "(under review)" became "(in preparation)". Removed the false "title withheld for double-anonymized review", since A is now at SPIC, single-anonymized. "By the same authors" stays out (CC-074(c) kept by PI-1026ae). |
| 3 | PI-1026ad/ae | `paperB.bib:8, 491–492` | `companion2026underreview`: title "in preparation (title given to the editor)", note "In preparation". The key name is unchanged, so `citation_map_B.tsv` needs no edit. |
| 3 | PI-1026ad/ae | `cover_letter_B.md:18, 24` | Dropped IP&M, `{{A_IPM_DATE}}` and the double-anonymized clause. The companion is now "in preparation (working title; copy to the editor)", and a comment gives the wording to use if A is submitted first. Zenodo comment: "decision on Paper A (SPIC)". |
| — | provenance | `number_manifest_B.tsv:651–657` | 7 new rows: 3589 = 1335, 7511 = 507, 2004 = 4487, "2 (of 558)", 556, 11, 0.95. The 11 post hoc MBR-3 rows (640–650) now say "S7 only, moved from sec5.1 by CC-126 W3". |

FAIR 2026 was already cited normally (L.M.H. Nguyen et al., 2026; `nguyen2026vsps`), so no change was needed there. Its pages and DOI are still owed (§4).

## 2. Word counts

Method: HTML comments removed with a DOTALL regex, then whitespace tokens counted. Tables and headings are included. This method gives larger totals than the 8,115 in STATUS.md, which came from an older count, so compare only before against after.

| File | Before | After | Δ |
|---|---|---|---|
| sec1_intro | 1,152 | 1,210 | +58 |
| sec2_related | 1,092 | 1,092 | 0 |
| sec3_data_and_audit | 4,082 | 4,391 | +309 |
| sec4_system | 991 | 991 | 0 |
| sec5_results | 1,405 | 1,369 | −36 |
| sec6_discussion | 922 | 922 | 0 |
| sec7_limitations_ethics | 1,903 | 1,909 | +6 |
| sec8_conclusion | 294 | 304 | +10 |
| **Main, sec1–sec8** | **11,841** | **12,188** | **+347** |
| supplementary_B | 7,326 | 7,504 | +178 |
| cover_letter_B | 566 | 593 | +27 |

## 3. New abstract (245 words with the slot, 242 without; LRE 150–250)

Vietnamese image-captioning systems are compared mainly by CIDEr (consensus-based image description evaluation) on KTVIC, but a KTVIC number alone does not name its scoring protocol. We propose a protocol card naming the segmenter, CIDEr variant, scale, punctuation policy and object matcher of every score, and release an open kit that scores any system's outputs under a declared card and reruns the audit on the reader's data. With one fine-tuned Qwen2.5-VL-7B model as a fixed instrument (word-level CIDEr-D 148.23, three seeds), we measure four properties of KTVIC. Each image's five references come from one writer: objects named by exactly two references sit in adjacent slots at a share of 0.7102, against 0.40 under exchangeability. No reference ends with a period, a measured protocol hazard: where a pipeline replaces the Penn Treebank (PTB) tokenizer and loses its punctuation removal, one period per caption costs the instrument 35.17 CIDEr-D points; with PTB-style removal, nothing (post hoc). Word segmentation against syllable tokenisation moves the same outputs by 15.64 points. 401 of the 558 test images are in the UIT-OpenViIC training split, whose separately written captions disagree with KTVIC's on objects; their independence is not established. The punctuation fix did not re-rank four public vision–language models (Kendall's τ_b = 1.0; registered prediction FAIL), and the registered final-system test failed (−0.39 [−2.44, +1.67] CIDEr-D against its members' mean). Beyond the released outputs of two published KTVIC baselines, the kit has so far scored only the authors' systems [B-2: N external systems].

There are 5 words of headroom. When B-2 fills the slot and the sentence grows, cut "(consensus-based image description evaluation)" first, if LRE accepts CIDEr as a metric name.

## 4. Open items for the PI

1. **ORCIDs** (or a homepage or CV) for all three authors. `cover_letter_B.md` still has three `[AUTHOR TO PROVIDE]` lines, and LRE requires one per author.
2. **Zenodo reserved DOI.** It appears in `sec7_limitations_ethics.md` §7.2 and `cover_letter_B.md`. The deposit is private until A's decision (CC-074(c), PI-1026ae).
3. **FAIR 2026 DOI and pages.** `paperB.bib` `nguyen2026vsps` note: "[AUTHOR TO PROVIDE: pages and DOI once listed on IEEE Xplore]".
4. **Kit licence.** The text says MIT (§7.2, §7.5; K15 also says MIT). Please confirm MIT for the B deposit. OpenViIC has no LICENSE file, so the kit ships pointers only.
5. **Deposit count.** §7.4 and the cover letter say "42 of its 604 rows" (B deposit v4, 2026-10-22). The working manifest has 649 rows before today and 656 after. Paper A's manifest has 600 rows. The deposit needs a rebuild and a recount before 11-30. I left the 42/604 sentence unchanged because it describes deposit v4 truthfully, but it goes stale as soon as the deposit is rebuilt.
6. **Special Focus (less-resourced languages): flag it or not.** If yes, the cover letter needs the flag (placeholder at `cover_letter_B.md:20`), the textbook method descriptions must go, and a "comprehensive evaluation" is expected. K15 W2 warns it may be returned if the kit has no external runs and the DOI is not public.
7. **Length.** LRE expects 18–25 pages. Main text is 12,188 tokens and the supplement 7,504 (§2). The page count needs a compile in the Springer Nature template, which has not been done. K15 §3.2's cuts (ladder, levers, κ, matcher v3, S4 leaderboard to the supplement) are not applied yet.
8. **Paper A status when B is submitted.** A is due 11-11..11-20 and B in 12/2026. **[Corrected 2026-10-28, CC-145 J3/W4: stale. A goes to SPIC 12-21..12-30, latest 01-15 (PI-1026ap); B freezes 11-30 and goes to LRE in 12/2026, so B precedes A and "in preparation" stays. Update the places below only when A is actually submitted.]** If A is submitted first, every "in preparation" becomes "under review at SPIC (submitted <date>)". The places are `sec1:22`, `sec2:17`, `sec7:38, 42`, `paperB.bib:491–492` and `cover_letter_B.md:18`.

## 5. Open items for the judge

- **J1 (CC-130 W6, the stronger sentence).** CC-130 said near-duplicates inside KTVIC "were not searched". The repo shows they were. `data/dedup/ktvic_dup_train_test.json` (944c372e, commit 8bac46b, 2026-10-10) is a CLIP ViT-B/32 search with `n_dup` = 11 test images at cos ≥ 0.95. It includes cos = 1.0 pairs that are not byte-identical: test 303 ↔ train 3160, and test 331 ↔ train 3589, which is the same train image as the 1335 twin. I cite this as EXPLORATORY with the key `n_dup` only. The README's eye-check "about 15" is not keyed and is not used. Ruling needed: is this sentence acceptable, or should the main text say "byte identity only" and leave out the CLIP count?
- **J2 (external-system count, CC-126 W13).** The new sentence says "beyond the released outputs of two published KTVIC baselines, the kit has so far scored only the authors' systems". Those two baselines already enter §3.3 and §3.4. Please confirm that the count under W13 is 0, meaning third-party decodes under the B-2 description-only prereg, and that the baselines do not count toward it. "Validated on external systems" is used nowhere, and it stays out until there are at least 3.
- **J3 (title of Paper A in B).** CC-088 A-2 and CC-074(c) withheld A's title because A was under double-anonymized review. A is now single-anonymized at SPIC and B is single-blind. I removed the false rationale, kept the title out of the manuscript and gave it in the cover letter as a working title. Should A's title be restored in B's text and bib, and should the bib key `companion2026underreview` be renamed (13 rows in `citation_map_B.tsv`)?
- **J4 (scope of the caveat).** §3.6 now says that every model trained on all 3,769 or on the 3,469 images, and every model fine-tuned from one of them, trained on both test twins. That covers P1-R's 148.23 and the audit scores, not only 145.15. The S5 f25/f50 runs (867, 1,734) hold 7511 only, and only the full-size point saw 4487. Source: the B-1 PREREG level membership and l.51 (L3/L4 = S5 subsets). E5 DPO and count-matched DPO/RFT use 1,000–1,500-image preference subsets on full-trained bases, and twin membership was not checked for those subsets. Please check against CC-130 W6.
- **J5 (the 157-image clean set).** S7's post hoc row reports +3.95 on "the 157 clean images" (no OpenViIC copy). I did not check whether test 1335 or 507 is among the 157, because that needs the per-image overlap list. This is not a re-score, only a membership check.
- **J7 (ruling-fixed abstract sentences).** The new abstract replaces CP-071's fixed final-test sentence ("did not raise CIDEr-D over its members' mean … registered verdict FAIL; the interval includes 0") with "the registered final-system test failed (−0.39 [−2.44, +1.67] CIDEr-D against its members' mean)". It also drops the PD-28 (2)/PD-27c kit-content sentence (word lists, no KTVIC counts or captions, v3 excluded), which stays in sec1 and §7.2. Both changes were made to stay within 250 words. Please approve them, or name what to cut instead.
- **J6 (K15 §3.2 cuts and §3.3 additions).** These are not applied in this pass, because CC-126 W3 lists only the items done here. They are needed for the 18–25 page target.

## 6. Files and SHA-256 (before → after)

| File | Before | After |
|---|---|---|
| cover_letter_B.md | 5f799728… | 0e759a50478d478a0a603279d3360c2ebbf9daf628bfb4313ba4d29aafc9f9df |
| new_vs_FAIR.md | 86610b03… | 93e515755085f9df14d875b7c5e520d998ac6e62c4d01c0bb7bea569ebfb4ac0 |
| number_manifest_B.tsv | 8f7af572… | 8664d6d9e47855fb437ab53d02a2b35857e27aeeb6a2e59c3c67c6043c9fcfca |
| outline_B.md | 42947467… | ace043ac912294c5ede2481f97ec6c7bad5669f8e1ebfd7b12fd55d6aaa327e2 |
| paperB.bib | 71cf5f27… | b66d210ccec2ef4613ebecc6fba3acd41d1544b5cdf4f43657a4390698dd3735 |
| sec1_intro.md | f5be47f5… | 884e58c574d8fbf824d7ef4a63a6434b86c06cb529cf39904b44774a6f0a6748 |
| sec2_related.md | 270a8551… | 81651cb2d4267cf681b28717d12bb6651b665a3e375faa8a1a84ea7c38afb5d8 |
| sec3_data_and_audit.md | b1b463a8… | a4acdffc3141e75842dfab7a8ef0ed57e2b8d30c4de1818aa560b22d02a15a0c |
| sec5_results.md | f8b16aa8… | 4f5e2ffe7b06dd0989c9253fc4f63241ebd91d5cf1b049a16b978432fae9c13f |
| sec7_limitations_ethics.md | ead8f090… | e79c1cc98d679b5b8597c4bfd8b2bcb3f5962d36d5a59438c34cc624ffd5f708 |
| sec8_conclusion.md | 6428f374… | 6a459a2b830bb913c4ff7dd26d9ebaa0a2e3f4a0d4bc9c8c0acf0caf532daba2 |
| supplementary_B.md | b469384a… | b16346eec571724e55417cb87fa27c0e448370c4357846784e44307c6addd349 |

The full before-shas are in `.session_backup/2026-10-27/paperB_v2/before/SHA256SUMS`. At the end, the six files that were not edited (STATUS, WRITER_B_LOG, citation_map_B, sec4, sec6, title_page_B) still equal the backup byte for byte. This file (V2_PROGRESS_B.md) is new.

---

# Pass 2 (writer, 2026-10-28): B-2 result, J items, scorecard-targeted text

Branch paper-v10, HEAD 42f6e9a. Nothing committed. Before-copy: `.session_backup/2026-10-28/snapshots/B_pass2/before/` (19 files, SHA256SUMS; the working files equalled pass 1's "after" shas at the start). After-copy and `SNAP.sha256`: `.session_backup/2026-10-28/snapshots/B_pass2/`. No registered number or verdict changed. No `*.preds.json` was opened. No caption text was read or written. The 6/8-gram scan (`ngram_scan_cen.py`) over sec1–sec8, outline, supplement, cover letter and manifest gives **NGRAM SCAN PASS, 0 hits**.

**Inputs used for B-2.**
- `.session_backup/2026-10-28/b2_external/score/scores.json` (sha256 e1a6e0d8…, which matches the B2-LOOK line `LOG.md:587`) and `table.md` (f0db61f3…, also matching).
- `gate.json` (5519b26d).
- PREREG `2026-10-28_b2_external/PREREG.md` (31176ff0 at e9d5897), including Amendments 1–2 and §7/§9.
- CC-138 and CC-138a–d.
- From the M3 mirror: `gpu_seconds.tsv` (4bc43820), `logs/job.log`, and `preds/K*.prov.json` (K6 41f51c73).

Note: the M3 mirror has no `score/` folder. The score files are only on the laptop path.

## P2.1 Changes, by scorecard criterion

The criteria are CC-126 W1 / UPGRADE_PLAN §7. I did not self-score; the 11-30 panel scores.

| Criterion | File:place | Change |
|---|---|---|
| Evidence | `sec3_data_and_audit.md` §3.7, new block "The kit on external systems" + **Table 3.2** (two panels of one table) + notes + text | The B-2 table, with §7.1's exact title and labels, rows by stable id, no rank, difference or bold, and licence wording per Q3. All §4 columns come from `scores.json`, including `empty`, `ROUGEL_PTB` and residual punctuation, which `table.md` omits. The text covers each system's own columns only (§7.2): K1/K6 P0 = P0s = PTB, SYL/PYVI vs P0; K5 P0/P0s/PTB with 23.81% end-punct and 198 PTB tokens; 57/231 empty as a count only. The §7.3 sentences use the templates verbatim. |
| Evidence (disclosures) | same block + Table 3.2 notes | The disclosures are: the 10 gate-excluded files with reasons; K1's twins (1335 = 3589, 507 = 7511) with the minus-twins 106.88/106.88; and the 3 truncated OpenViIC files by name under T6 (CC-138d writer obligation, note 3). They also cover K5's empties, both STOPs (OPS-1028c-op, OPS-1028f-op; ids in src comments), §9 exposure and §9 unknown protocols. K1 is "named for KTVIC; card names no dataset", not table.md's flat "trained on KTVIC train". Note 2 states that the 556-image column is K1's own single look, so §3.6's "second look" sentence is not contradicted. |
| Reproducibility | `supplementary_B.md` new **S9** (run record) | S9 records the inventory and eligibility, the gate with per-file reasons and sources, and the post hoc structure diagnostic (labelled). It also records the §5.2 monitoring deviation, the latent CAP_KEYS defect, the pinned revisions and versions, the smoke rule with the second image (368), the GPU-seconds per step (620 total vs the 3 GPU-h cap), both stops and amendments with times, the one-look log, and "what the run does not show". |
| Application | `sec6_discussion.md` §6.4 | Recommendations 1–2 shown in use on three third-party systems, with 620 GPU-s on one 24 GB GPU. |
| Application / positioning | `outline_B.md` abstract (248 words) | The slot sentence is replaced by the §7.3 templates: "run on 3 external systems from 3 sources, so it is validated on external systems (descriptive scores, no ranking)". The abstract carries no B-2 score. The CIDEr gloss is kept, because the LRE card says no undefined abbreviations. |
| Positioning | `sec1_intro.md` contributions + "What we do not claim" | The kit bullet now gives the count, the bar and 0/10 output files passing. "What we do not claim" adds that the Table 3.2 rows are compared neither with each other nor with ours. |
| Positioning | `sec5_results.md` §5.1 last paragraph; `sec7` "Comparators" | A pointer to Table 3.2 as descriptive, not compared. |
| Evidence (honesty) | `sec7_limitations_ethics.md` §7.1 new "External systems" | The paragraph states four limits: 3 systems, all checkpoints; decoded by us under transformers 4.57.6; not an outside user's run; 2 aggregates-only by licence; K5's 57 empties. It also says the run carries no quality claim. |
| Positioning | `sec8_conclusion.md` | One sentence with the §7.3 templates. |
| Venue fit | `cover_letter_B.md` | The slot sentence is replaced by the §7.3 templates. The 42/604 count is made count-free (see P2.3). |
| Length / venue fit | `sec5_results.md` §5.2 → `supplementary_B.md` new **S10** | Following the K15 §3.2 cut list, the κ / within-pool paragraph is moved verbatim with its src. §5.2 keeps a one-sentence pointer. The 6 manifest rows are marked "moved to S10". |
| Evidence (J5) | `supplementary_B.md` S7 | One sentence: neither twin (1335, 507) is among the 157 clean images (src: clean list 4832c16b = MBR-3 record input). |
| Provenance | `number_manifest_B.tsv` | **+80 rows** (656 → 736 data rows; status suffixes on 13 moved rows): every Table 3.2 cell, 106.88 ×2, 23.81%, external_systems/distinct_sources, the gate counts, 9 systems / 4 owners, cap, 620 GPU-s and the per-step seconds, the truncated-file count, image 368, the versions, GPU, beams, B = 2,000, the 0.5 rule, the stop times, and the 157-membership check. K6's 41.71 rows say they are not §5.2's 41.71 (P1 seed 43 on UIT-ViIC). |
| Length / venue fit | `sec3_data_and_audit.md` §3.5 → `supplementary_B.md` new **S11** | The v3 sensitivity paragraph is moved verbatim with its src, per the K15 §3.2 list. §3.5 keeps one sentence and a pointer. 7 manifest rows are marked "moved to S11". |
| Evidence (wording) | `sec3` §3.6 | "a score of our systems on the other 556 test images would be a second look" (this squares with Table 3.2 note 2). |
| — | `outline_B.md` section map / open items | Adds S9, S10, Table 3.2 and the B-2 run line. |

Not changed: `sec2`, `sec4`, `new_vs_FAIR.md`, `paperB.bib`, `citation_map_B.tsv`, `title_page_B.md`, STATUS, WRITER_B_LOG. `b2.py` is **not** added to Table 3.1, because it is not in the deposit (see P2.4).

## P2.2 Word counts (same method as §2)

| File | Pass 1 after | Pass 2 after | Δ |
|---|---|---|---|
| sec1_intro | 1,210 | 1,304 | +94 |
| sec2_related | 1,092 | 1,092 | 0 |
| sec3_data_and_audit | 4,391 | 5,401 | +1,010 (Table 3.2 ≈ 330 of it; v3 paragraph out) |
| sec4_system | 991 | 991 | 0 |
| sec5_results | 1,369 | 1,339 | −30 |
| sec6_discussion | 922 | 970 | +48 |
| sec7_limitations_ethics | 1,909 | 2,079 | +170 |
| sec8_conclusion | 304 | 336 | +32 |
| **Main, sec1–sec8** | **12,188** | **13,512** | **+1,324** |
| supplementary_B | 7,504 | 8,806 | +1,302 |
| cover_letter_B | 593 | 610 | +17 |
| Abstract | 245 (with slot) | 248 | +3 (LRE 150–250) |

**Page proxy (pandoc + xelatex, sec1–sec8 only, without references, title page or declarations' bib; not the Springer template):**

| Font | Before pass 2 | After pass 2 |
|---|---|---|
| TeX Gyre Termes 10 pt, 2.5 cm margins (closest to Springer's 10 pt Times) | 19 pp | 21 pp |
| DejaVu Serif, 2.5 cm (the 10-25 smoke command) | 23 pp | 26 pp |

With references (about 3–4 pp), the Times proxy lands near 24–25 pp, at the top of LRE's "typically 18–25". A Springer-template compile is still owed. The next cuts that cost no evidence are condensing the §3.3 XM3600 paragraph, and shortening §1 "What moved to the supplement" if PD-24 (a)'s one-line list may be shortened (judge). They are J6.

## P2.3 Deposit recount (V2 §4 item 5): resolved as far as files allow

- **Deposit v4: 42 withheld of 604 rows.** Recounted 2026-10-28 from `.session_backup/2026-10-22/b_deposit_v4/ktvic_eval_kit_v4.tar.gz :: manifests/number_manifest_B.tsv`, `archive_path` containing `withheld:`. So the old sentence was true of v4.
- **"649 / 656".** These were working-manifest data rows before and after pass 1 (657 lines with the header). They are now **736 data rows**.
- **A's 600.** This is Paper A's manifest. It is unrelated to B's count and needs no action.
- **The text.** §7.4 item 1 and the cover letter no longer print a count. They say that rows citing unreleasable sources "are marked as withheld", and the v4 count sits in a comment. The withheld count for the rebuilt deposit cannot be computed now, because the working TSV has no `archive_path` column. The kit builder fills it in at the rebuild.

## P2.4 Judge items: status

| Item | Status | Basis |
|---|---|---|
| J1 CLIP near-dup sentence | **open** (judge) | No ruling since OPS-1027c. The text is unchanged. |
| J2 external-system count | **closed by B-2** | `scores.json` gives external_systems 3 and distinct_sources 3, with w13 allowed. PREREG §1.1 lists the two KTVIC baselines (K3) as "not new: scorer gate only, not counted". The §7.3 sentences are now used. |
| J3 A's title in B | **open** (judge/PI) | The facts changed with PI-1026ap (LOG after l.587): A goes to SPIC 12-21..12-30 (latest 01-15), B freezes 11-30 and goes to LRE in 12/2026. B will probably be submitted before or with A, so "in preparation" stays right for now. V2 §4 item 8 ("A due 11-11..11-20") is stale. |
| J4 scope of the twin caveat | **resolved from files** (judge to confirm) | Every preference/RL model starts from a base that holds both twins. E5 RFT/DPO start from fuse2 (3,769; the RFT set contains the 7,538 fuse2 rows, Table S1.1). Count-matched DPO/RFT start from LoRA `p1dev_s42` (3,469), per `manuscript/prereg/2026-10-18_tier3_S3.md` l.24. So the §3.6 sentence "every model fine-tuned from one of them" covers them whatever their subsets hold. No text change was needed. |
| J5 twins in the 157 | **closed** | `data/lb/splits/ktvic_test_openviic_train_clean.txt` (sha 4832c16b, equal to the MBR-3 record's input sha) has 157 ids, and neither 1335 nor 507 is among them. Both are in the 401-id leaked list (56e57ea4). The cross-check against `data/ktvic_openviic_refs.json` (4eb02cc4, not in git) agrees: both have an OpenViIC train copy, and 401 test ids have one. This was a membership check by id; no caption field was printed. A sentence was added to S7. |
| J6 K15 §3.2 cuts | **partly done** | κ was moved to S10 and the v3 numbers to S11. Still open: the XM3600 paragraph and the §1 "What moved" list (PD-24 (a)), plus a Springer compile. |
| J7 abstract wording | **open** (judge) | The final-test and kit-content sentences are as in pass 1. Only the slot sentence changed (§7.3 templates). |
| New J8 | **open** (judge) | Should the main-text Table 3.2 carry all §4 columns, as now? The other choice is a 4-column core in the main text with the full table in S9, which would save about 200 tokens. PREREG allows "one table in §3.7 or the supplement". |

## P2.5 Q1 path and open items for the PI

- **The B-2 condition of UPGRADE_PLAN §7 is met.** There are 3 systems from 3 owners, and CC-138 W8 did not fire.
- **B stays planned at LRE Q2** (PI-1026am). The other Q1 conditions are not met by text:
  - the DOI is still blank or private (PI-1026ao/ap);
  - "run by outsiders" is not met, because B-2 is our run of the kit on outsiders' systems (sec7 says so);
  - the 11-30 panel re-score is still to come.
- **Artifacts (still owed).** The deposit needs a rebuild that adds `scripts/b2_external/` and its SUMS to the kit, and a new withheld count. The 8-gram release scan must be rerun.
- **Carried from V2 §4.** The ORCIDs, the Zenodo DOI, the FAIR DOI and pages, the MIT confirmation, the Special Focus flag and the length compile are unchanged.

## P2.6 Numbers I could not source

None in the new text. Every new number has a manifest row with file, key and sha prefix. `table.md` does not show the `empty`, `ROUGEL_PTB` and residual-punctuation columns; they are taken from `scores.json`.

# Pass 3 (writer, 2026-10-28): CC-145 W1–W4 and J1/J3/J6/J7/J8

Branch paper-v10. Nothing committed. **Before-copy:** `.session_backup/2026-10-28/snapshots/B_pass3/before/` (19 files, `SHA256SUMS`). At the start, the live files were checked against `B_pass2/SNAP.sha256`: 19/19 OK (INC-1027a). **After-copy:** `.session_backup/2026-10-28/snapshots/B_pass3/` with `SNAP.sha256`.

Rules kept:
- No registered number or verdict changed, and no new number was written. A script compared every visible number in the edited files against the pass-2 text; the only new tokens are table labels (S9.1, S13.1, S14.1, S14.2) and decision ids.
- No `*.preds.json` was opened. No caption text was read or written.
- `scripts/`, `manuscript/prereg/`, `manuscript/ken/` and the A and C folders were not touched.
- The 6/8-gram scan (`ngram_scan_cen.py`) over sec1–sec8, outline, supplement, cover letter, new_vs_FAIR and the manifest: **NGRAM SCAN PASS, 0 hits.**

## P3.1 W1 / J8: Table 3.2 to S9

| File | Change |
|---|---|
| `sec3_data_and_audit.md` §3.7 "The kit on external systems" | The block was cut to one paragraph with counts only and no B-2 score: who ran it ("we ran it ourselves"); what the pre-registration fixed; 0 of 10 output files passed the gate; the 3 checkpoints by name; 620 GPU-seconds; the §7.3 sentence "We ran the kit on 3 external systems from 3 sources". "Validated" is kept only in that body sentence, with "by a run of the authors" and "not yet run by an outside group" (CC-145 W2). The paragraph ends with a pointer to S9 / Table S9.1. |
| `supplementary_B.md` S9 | Moved there whole, with cells, notes and src unchanged: Table 3.2 (now **Table S9.1**), its notes, the PREREG §7.2 per-system column bullets, and the PREREG §9 exposure paragraph. Note 1 now points to S9's own structure-gate paragraph. The eligibility list and the stops paragraph were already in S9, so the main-text copies were deleted rather than duplicated. The §7.1 four-limits bullets were also moved here as "Limits (moved from Section 7.1)". **PREREG §9 disclosures (twins, exposure, unknown protocols) are all in S9.** |
| Cross-references | sec1 contributions and "What we do not claim", sec5 §5.1, sec6 §6.4, sec7 §7.1 "Comparators" / "External systems", outline (l.36, 42, 65) and the S9 intro: "Table 3.2" became "Section 3.7" / "Supplementary S9, Table S9.1". |
| `number_manifest_B.tsv` | All 53 rows with "sec3 §3.7 Table 3.2" now read "Supplement S9 Table S9.1, moved from sec3 §3.7 Table 3.2 by CC-145 W1 2026-10-28". |

## P3.2 W2 / J7: the authors' run, not "validated"

The §7.3 bound: "the kit was run on N external systems from M sources" is allowed for any N, and "validated" is allowed but not required (CC-145 ruling 4 J7).

| File | Before | After |
|---|---|---|
| `outline_B.md` abstract | "…the kit was run on 3 external systems from 3 sources, so it is validated on external systems (descriptive scores, no ranking)." | "Under a description-only pre-registration, we ran the kit on 3 external systems from 3 sources (descriptive scores, no ranking)." This is CC-145 W2's sentence verbatim. |
| `cover_letter_B.md` | "…so it is validated on external systems." | "…we ran the kit on 3 external systems from 3 sources (three released third-party checkpoints, each decoded by us and scored once on the test split it reports on; descriptive scores, no ranking). No outside group has yet run the kit." |
| `sec8_conclusion.md` | "…so it is validated on external systems." | "…we ran the kit on 3 external systems from 3 sources (descriptive scores, no ranking); it reported every protocol column for each. No outside group has yet run it." |
| `sec1_intro.md` kit bullet | "That meets the bar fixed in advance, so the kit is validated on external systems." | "That meets the bar fixed in advance for calling the kit validated on external systems, in a run by the authors, not by an outside group." |
| `sec3` §3.7 | "so the kit is validated on external systems" | "…in the registered sense, by a run of the authors… It has not yet been run by an outside group (Section 7.1)." |

Other points:
- **J7 is closed.** The CP-071 final-test sentence change and dropping the PD-28(2)/PD-27c kit-content sentence are approved. That sentence remains in sec1 (kit bullet) and §7.2, both checked.
- **Abstract: 241 words** (pass-1 method; LRE 150–250).
- "Validated" no longer appears in visible text anywhere except the two body sentences above (sec1, sec3), each with "by the authors".

## P3.3 W3 / J6: cuts and the Springer compile

**Build.** `manuscript/build/build_B_springer.sh` (sn-jnl, `sn-apa`, sn-apacite, XeLaTeX; the template named by `.claude/skills/venue-lre/` and the build script). It was not edited.
- **Output:** `.session_backup/2026-10-28/builds/B_springer_pass3/paperB_LRE.pdf` (sha256 9307ac2e760ec178…); supplement `supplementary_B_OnlineResource1.pdf` (sha256 0aed6d87e17f01ab…).
- **Report:** 0 overfull hboxes; label check 0; 46 references; "supplement cites 6 keys; not in the main reference list: none".
- **Visible placeholders:** only the Zenodo DOI. The FAIR pages/DOI placeholder appears in the reference list.

**Real page count (Springer template, PDF pages, title page and references included):**

| State | Pages | References start |
|---|---|---|
| Pass 2 as left (baseline compile, this pass) | **36** | p. 32 |
| After the table column widths and W1 | 31 | p. 27 |
| After the J6 cuts, the ruling restores and the offsetting cuts (final) | **25** | p. 21, line 28 |
| Online Resource 1 (supplement, plain pandoc build) | 24 | — |

**Margin is about one line.** p. 25 is full (last entry Zhu et al. 2025). Any added main-text line, such as a longer FAIR reference once its DOI and pages are filled, may make it 26. Keep the next edits length-neutral, or cut first.

**Rendering-only changes (no words changed).** Proportional pipe-table separators set the column widths: §3.7 Table 3.1 (since moved), Table 4.1, Table 4.2, Table 6.1 (since moved), Table 7.1 (since moved) and Table S9.1(a). The equal `|---|` separators had given each column the same width. That pushed Table 3.1 over three pages.

**Moved to the supplement, verbatim with src (all supplement-able: no headline, no registered verdict leaves the main text).** Each move leaves a src comment saying "CC-145 J6" in both places.

| From | To | What |
|---|---|---|
| sec1 "What moved to the supplement" (PD-24 (a) list) | Supplement top, **Section map** | The whole verdict list and its code comment. sec1 keeps one line plus "The single pre-registered test of the final system failed (Section 5.1)". §5.1, §7.1 and the abstract still state −0.39 [−2.44, +1.67] FAIL. |
| §3.3 XM3600 paragraph | **S12** | The system scores 48.39 / 41.17 / 38.61, the gaps −7.22 / −9.78 with CIs, and the PTB values and gaps. Main keeps 217/1,227 (17.69%), the 0.0% / 99.5% end rates, +2.71 / +2.75 with CIs and PTB 0.00. The §7.1 "XM3600 decomposition is partial" paragraph is folded into the last main sentence; its text is in S12. |
| §3.3 PTB paragraph | **S12**, **S15** | The token counts (775 / 1 / 0; 19 residual of 2 types) go to S12. Only the baseline code-path sentence (test.py, GRIT engine lines and commits) goes to S15. The CC-092 R6 provenance sentence (repository, commit, access date, permission, no licence, aggregates only, readers fetch) stays verbatim in §3.3. |
| §3.2 permutation null | **S16** | The method sentence, the CI, the lag-1 null 0.0355 and the train/dev300 sentence. Main keeps 0.4504 and "no draw of 1,000 reaches 0.7102". |
| §3.5 role/child paragraph | **S11** | 30.02 / 21.39 / 27.12 / 26.01. Main keeps the flip and the "publish the matcher" reading. |
| §3.6 UIT-ViIC/COCO/POPE paragraph | **S14** | 133 / 2,695 / 59 / 4 / 21. The §7.2 "Leakage rules" keep the rule with 21 and 59. |
| §3.7 Table 3.1, archive-extras paragraph, "Not released", OpenViIC rule, text-scan detail | **S14** (Table 3.1 becomes **Table S14.2**) | Main keeps a five-part summary of the kit, the licence and archive, the datasets (the data-availability statement stays self-contained), a one-sentence "Not released" and a short text-scan paragraph. |
| §4.3 software paragraph | **S15** | Main keeps "single 24 GB NVIDIA RTX 3090; greedy". |
| §5.1 final test: the git-bundle sentence only | **S7** | CC-070 (b): "One supplement line is enough". Everything else in §5.1 is unchanged (see restores below). |
| §6.4 Table 6.1 | **S14** (**Table S14.1**) | |
| §7.3 Table 7.1 | **S13** (**Table S13.1**) | |

**Deleted as duplicates; the content remains elsewhere.**
- §7.2: the three dataset-source sentences (verbatim in §3.7 "Datasets").
- §5.2: "Leakage rule" (§7.2) and the companion-slope sentence (Table S13.1).
- §5.1: the comparator paragraph, condensed (sec1 / §7.1).
- §7.1: "Comparators" and "Method-side tests", condensed (each removed sentence checked present in S2.2 / S6.6).
- §6.4: two sentences (§3.7); the sentence repeating 620 GPU-s (§3.7).
- sec8: one XM3600 sentence (§3.3).
- §3.1: the dev-gated system list (Table S1.1). The CC-109 W2 sec3:9 wording ("only the dev-gated family is trained without dev300") stays.
- §2: the HDUCap/ViG access detail, condensed (date kept).
- §3.6: one rule sentence (§7.2).
- §7.4: the 34.33 example sentence. **34.33 had no manifest row.** It was a pre-existing unkeyed number in the main text and is now gone.
- §7.2: "only 11 documented short matches in pinned code". It **conflicted with** the scan paragraph's "9 lines" (now in S14), whose own comment gives BUILD_RECORD "5 files, 11 lines". See P3.5.

**Restored after a ruling check (advisor review, same day).** Every cut sentence whose comment cites a ruling was checked against that ruling. Wherever the ruling fixes main-text wording or location, the sentence was restored verbatim and its supplement copy deleted:
- §5.1 mask bullet: CP-112 W1/W2 and CP-112a W3 fix the training-count sentence, 147.67 beside 149.79, and the seeding clause in sec5.1.
- §5.1 final test: CC-109 W4 fixes the members on 3,469, "no system was retrained" and the §9 closure in sec5.1. CC-126 W3 fixes the one-clause pointer to the post hoc MBR-3 row in S7.
- §4.1: the CC-109 W6 sentence.
- §7.1 "Earlier human ratings": the PD-21b disclosure text.
- §3.3: the CC-092 R6 provenance sentence.

Kept as moved, because the ruling allows it:
- The git-bundle line (CC-070 b allows one supplement line).
- The PD-24 (a) list. PD-24 (a) had asked the main text to name every moved verdict, and CC-145 J6 explicitly allows a one-line pointer to a section map.
- The XM3600 system scores. CC-088 B-3 asked B to print its own XM3600 CIDEr-D; B still prints them in S12, and CC-145 J6 ordered the condensation. **Flag for the 11-30 panel:** confirm that S12 satisfies B-3.

Added: one clause in the sec1 pointer, "The punctuation fix did not re-rank four public VLMs (Kendall's τ_b = 1.0; registered prediction FAIL; Supplementary S4)". Without it, the abstract's τ_b FAIL had no body statement once the PD-24 (a) list moved.

Offsetting cuts (no ruling cited in their comments; each states content kept elsewhere):
- sec8 first paragraph condensed to one sentence, with the CC-126 W3 panel sentence verbatim;
- sec1 audit bullet condensed;
- §2: the 231-image sentence and the interface sentence (§3.1 and §3.2 state them), the QLoRA/LoRA sentence (§4.1 cites them) and one panel-disagreement sentence. The CC-024 exposure caveat is kept.
- §6.2 count bullet condensed; §6.5's last sentence condensed (§7.1 "One model family");
- §7.2 UIT-OpenViIC paragraph (it repeats §3.1 "UIT-OpenViIC panel" and §3.7).

Also, the supplement intro's "None of these results is a contribution of the paper" is now scoped to S1–S8.

**Manual number check (manifest column 1 against visible numbers in sec1–sec8, the abstract and the cover letter).** No miss other than labels, commit hashes, settings (64-bit hash, seed 43, ResNet101, SHA-256, POPE-500, train2017) and B-1's own wording "up to 35 points". The one real miss, 34.33, was cut (P3.3).

**Manifest.** 31 further rows whose number no longer appears anywhere in the visible main text now carry "; supplement only since CC-145 W1/J6 (2026-10-28)". The tags on 147.67 and 150 were removed again after the restores. A script checked that every number that left the main text is in the supplement; the only exceptions are 34.33 (unkeyed, cut) and "HTTP 403" (an access detail, now only in a comment). Six 3,769 rows that the first pass tagged by mistake were untagged, because 3,769 is still in the main text.

**Word counts (pass-1 method; comments stripped):**

| File | Pass 2 | Pass 3 | Δ |
|---|---|---|---|
| sec1_intro | 1,304 | 1,121 | −183 |
| sec2_related | 1,092 | 999 | −93 |
| sec3_data_and_audit | 5,401 | 3,683 | −1,718 |
| sec4_system | 991 | 894 | −97 |
| sec5_results | 1,339 | 1,189 | −150 |
| sec6_discussion | 970 | 713 | −257 |
| sec7_limitations_ethics | 2,079 | 1,358 | −721 |
| sec8_conclusion | 336 | 292 | −44 |
| **Main** | **13,512** | **10,249** | **−3,263** |
| supplementary_B | 8,806 | 12,207 | +3,401 |
| Abstract | 248 | 241 | −7 |

## P3.4 W4 / J1 / J3: text, and the deposit rebuild (checklist only, NOT run)

- **J1 (done).**
  - §3.6 keeps the CLIP sentence as EXPLORATORY, keyed on `n_dup` = 11 at cos ≥ 0.95, with no "about 15". Byte identity is stated as the only count.
  - The src comment now records the CC-145 J1 acceptance and the explicit correction of CC-130's "were not searched" (`data/dedup/ktvic_dup_train_test.json`, commit 8bac46b, 2026-10-10).
  - No B file says "not searched" except V2 §5's historical J1 entry.
- **J3 (done).**
  - A's title stays out of B's text and bib, and "in preparation" stays.
  - The title appears in the cover letter only, which is allowed.
  - The "open for the judge" comments in `sec7` §7.3 and `cover_letter_B.md` now say CLOSED by CC-145 J3.
  - `companion2026underreview` was not renamed.
  - V2 §4 item 8 carries a dated correction (A at SPIC 12-21..12-30, PI-1026ap; B first).
- **Deposit rebuild: checklist for the kit builder** (gatekeeper and judge round, before 11-30; NOT run in this pass):
  1. Start from deposit v4 (`.session_backup/2026-10-22/b_deposit_v4/`, builder `make_b_deposit.py`, gates `gates_b.py` and `run_kit_gates.py`). Make a v5 builder copy; do not edit v4.
  2. Add `scripts/b2_external/` (`b2.py`, `b2_chain.sh`, `b2_job.sh`) with its committed `SHA256SUMS`, and exclude `__pycache__/`.
     - Check each file against `scripts/b2_external/SHA256SUMS` and against the PREREG `2026-10-28_b2_external` §11 pins.
     - Add `manuscript/prereg/2026-10-28_b2_external/PREREG.md` (31176ff0 at e9d5897).
     - Add the B-2 records only as **score-only copies made by the builder's strip** (`tools/strip_and_check.py`), with the original sha recorded (`scores.json` e1a6e0d8, `table.md` f0db61f3), as §3.7 describes for every result file. Per CP-071 (v4 stripped `test_ids` and per-image arrays), no per-image array or test-id list ships; K1 and K6 are aggregates only by licence.
     - Add no predictions; K1 and K6 are aggregates only by licence.
     - Add `gate.json` (5519b26d) only if it holds no caption field. Check its keys first.
  3. Replace the kit-component table (now Supplementary Table S14.2) with a row for `b2.py`, but only if the file ships. Pass 2 kept it out of the table because it was not in the deposit.
  4. Rebuild `manifests/number_manifest_B.tsv` from the working manifest (736 data rows, statuses as of pass 3) with the builder's `archive_path` column. **Recount the withheld rows** (`archive_path` containing `withheld:`; v4 was 42 of 604). §7.4 item 1 and the cover letter print no count, so the text needs no change unless a count is wanted.
  5. **Rerun the 8-gram release scan** (`release_scan` as in `release_scan_v4.json`: 8-grams of lower-cased `\w+` tokens against KTVIC, UIT-OpenViIC, XM3600, UIT-ViIC, M-HalDetect and the two baselines' outputs; ceiling 12).
     - Require 0 unpinned hit files.
     - Reconcile the pinned-code count: the S14 text says "3 files, 9 lines", while the v4 comment says BUILD_RECORD `code_hits_documented` "5 files, 11 lines". Fix the S14 text to the rebuilt BUILD_RECORD.
  6. Rerun the kit gates (`kit_b` scripts reproduce manifest values) and the tar-metadata rules (mtime 0, uid/gid 0, mode 0644). Record the new tarball sha in a BUILD_REPORT v5.
  7. Keep the deposit private (PI-1026ae). The public DOI remains PI-reserved (CC-145 W6 / "For the PI" Q1).

## P3.5 Open items

- **PI:** ORCIDs ×3, the Zenodo DOI and the public-DOI decision (CC-145 Q1), the FAIR 2026 pages and DOI, the MIT confirmation, and the Special Focus flag. All are unchanged from V2 §4.
- **Page margin.** The compile is 25 pp with about one line of slack (see P3.3). Filling the FAIR reference DOI and pages, or any new main-text sentence, can push it to 26. The next length-neutral cut, if needed, is sec1 item 2 (the punctuation paragraph repeats §3.3).
- **Deposit rebuild.** Checklist P3.4; not run.
- **Text-scan count conflict.** The scan paragraph (S14) says "3 files, 9 lines"; its comment and BUILD_RECORD v4 say "5 files, 11 lines". The number was not changed here (no new numbers). The rebuild decides it (checklist step 5).
- **Statements and Declarations placement.** In the compile, §7.5 is followed by sec8 Conclusion and then the references. LRE wants Statements and Declarations immediately before the reference list. Moving §7.5 after sec8 (or into the template's back matter) is a build or structure change I did not make; it is page-neutral.
- **Supplement format.** The supplement is a plain pandoc build (DejaVu Serif). Table S9.1(b)'s 12 columns wrap but are legible. If LRE wants the supplement in the template too, it needs its own build.
- **For the 11-30 panel.** Venue fit can be re-scored on a real compile (25 pp, sn-jnl). The cuts moved no registered verdict out of the main text: the final-test FAIL, the τ_b FAIL and the post hoc labels remain.

## B-1 / paper D report notes (CC-152 W3, 2026-10-28)
- s43 L5 was retrained from scratch after a segfault (STOP-M4-5); the step-200 checkpoint could not be loaded (STOP-M4-6, CC-152a), so it was NOT resumed.
- The M4 HEAD moved from 70994446 to 847dd45d mid-run; B-1 code and dependencies byte-identical (CC-152 Q1).
