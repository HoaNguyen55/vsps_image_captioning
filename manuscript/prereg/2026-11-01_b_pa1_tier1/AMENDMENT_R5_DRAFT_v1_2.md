# B-PA1-T1 AMENDMENT R5 (4090 launch amendment): DRAFT v1.2 for round 3 (last), full panel at irreversible 92

Status: **DRAFT v1.2, not adopted, not committed, licenses nothing.** v1 (`AMENDMENT_R5_DRAFT.md`, `8613a2b3`) and v1.1
(`AMENDMENT_R5_DRAFT_v1_1.md`, `08f3f4d1`) are kept unchanged. Route actually followed (CC-224 l.14): round 1 = CC-224,
full panel, NEXT_ROUND 86; round 2 = CC-224r2, full panel at 92, NEXT_ROUND 88; round 3 = full panel at irreversible
92, the last round. A diff read never grants GO; without GO in round 3 the topic goes to the PI as ESCALATE_TO_PI
(CC-224r2 l.16, l.101). Tier: irreversible 92 (CC-224 Ruling 1; CC-224r2 Ruling 1). Written 2026-11-02T04:10:28Z, last edited 2026-11-02T04:13:59Z
(`date -u`); v1.1 written 02:58:07Z, v1 01:20:39Z.
Amends the registered prereg `manuscript/prereg/2026-11-01_b_pa1_tier1/PREREG_DRAFT_v3_1.md`, sha256 `e9b30ca7`,
commit `5ff00c9` (LOG l.1141). v3.1 is not edited; where this file conflicts with v3.1, this file governs from its own
gatekeeper commit (CC-209c / CC-218 precedent, as in the 5ff00c9 message line 5). HEAD at drafting: `1f23d30`.
Label on every output: `TIER 1 / DEV-EXPLORE (B-PA1-T1)`. Every estimate here is AI opinion, not evidence.

**Route.** This amendment is written for **route 1b** only (CC-224 option 1b l.29; CC-224r2 l.98): E1 and E2 are
pre-fixed NOT RUN at tier 1 by erratum E-12, and M8 receives only the Objects365 frame. If the PI answers Q-EN = 1a,
R5 returns to the panel before any commit; no route-1a text is part of this amendment (CC-224r2 W3, option 1').

**Commit precondition (CC-224r2 W5 l.72, Ruling 8 l.62).** A round-3 GO licenses the gatekeeper commit only after a
logged PI line reading **Q-EN = 1b**, time-stamped before the commit and cited in the commit message. If the PI answers
1a or does not answer, the GO lapses: no commit, and R5 returns to the panel. No default answer is applied.

**Licence if adopted (CC-224 Ruling 10 l.60; CC-224r2 Ruling 10 l.64).** The gatekeeper commit plus laptop ids-only steps.
No 4090 step until P3, P4 and P6-P10 are met (P2 is met, §D.1). No M1 slot until Q2 and the MT4 hand-over.
**Licence line for the feature recomputes (CC-224r2 Ruling 9 l.63, N7; J-j), reversible 90:** after the R5 commit, the
laptop CPU recomputes of §A.5 may run, each once its code meets P8 (selftest, SUMS LOG line, one-judge code read) and
its start is logged; the M1 CPU recompute slot may run on the same two conditions and, in addition, only under Q2 and
the MT4 hand-over (v3.1 l.269-270). Until a recompute has run, the blocks it holds stay held (P6).

**Why R5 exists.** No 4090 step, block W included, runs before this amendment is adopted, a logged PI top-up exists and
the N18 novelty rescan is logged (v3.1 l.7-9, l.521-523; CC-217r2 Ruling 4 l.44; CC-217r3 Ruling 4 l.47 and Q1 l.80;
5ff00c9 message line 9). The one-judge read of CC-217r3 Q1 is the minimum review, not the tier (CC-224 l.16). R5 is also
registration item R5 (v3.1 l.656-657) and carries CC-217r3 NB2, NB3, NB5, NB8, NB10, NB11 (5ff00c9 message line 9).

**Inputs (re-hashed at drafting):** owners build `.session_backup/2026-11-02/b_pa1/b_pa1_owners.json` sha256 `ae4b6630`
(LOG l.1150); builder `scripts/b_pa1/b_pa1.py` `bce9e873`, SUMS `924e812d` (LOG l.1149); KV-5,000 id list
`manuscript/prereg/2026-10-27_grl_pilot/kv5000.txt` `b7a7a89d` (ids only, used for the §B.2 #12 recount; CC-224 l.38);
PORTFOLIO_3Y at HEAD `910ab3bf`; `C_DIRECTION_v4_1_2026-11-02.md` `8334cf5d`; `B_DIRECTION_v3_2026-11-01.md` `ef1e3cc5`;
CC-224 ruling `.session_backup/2026-10-13/decisions/CC-224.txt`. No dataset, image, feature value, caption or label was
read. Feature-cache shas were computed (sha only); no npz was opened.

Notation: "[proposal]" = chosen here, not sourced; "[derived]" = arithmetic on cited numbers.

## v1.2 changes (against v1.1 `08f3f4d1`; CC-224r2)

| CC-224r2 item | change in v1.2 | where |
|---|---|---|
| W1 (l.68) | l.501 total row added to the E-12 list as 18.8 (+25% = 23.5); the false "restated by E-7" deleted | E-12 |
| W2 (l.69) | E-7 re-anchored: l.511 from "At the assumed rates" through l.516 "R5 restates the rate.)" replaced, so the trim criterion of l.510-511 stays; "inside the 20 h cap" cited as l.283-284 | E-7 |
| W3 (l.70) | E-12 (ii) struck; "if Q-EN = 1a, R5 returns to the panel before any commit"; §D.6 reduced to that sentence | header, E-12, §D.6 |
| W4 (l.71) | l.27 and l.422-426 added to the E-12 list (no English prompt written or pinned at tier 1); catch-all for other E1/E2/Composite/Polaris/H3 mentions; P9 restricted | E-12, P9 |
| W5 (l.72) | commit precondition: logged PI line Q-EN = 1b before the commit, cited in the commit message; else the GO lapses | header, §H, §I |
| N1 | header gives the route followed (rounds 2 and 3 full panels at 92) | header |
| N2 | P2 closed by PI-1102b (LOG l.1163) and OPS-1102topup (LOG l.1164); Q5 marked answered | §D.1, §H |
| N3 | E-14 replaces the whole l.313-316 bullet from its start | E-14 |
| N4 | E-15: a late G2/G4 match neither reverses a PA3 outcome nor fires a new one | E-15, §A.3 |
| N5 | "rental" defined as any host other than the custody host M1 | E-13, §A.1 |
| N6 | the M1 slot fails closed (1.0 h wall cap; unpinned K2) | §A.5 |
| N7 | licence line for the laptop and M1 recomputes at reversible 90 | header, §G J-j |
| N8 | M8 idle bill while S and A1 wait; the M1 slot gated too | §D.1 P6, §D.4 |
| N9 | K6 row cites LOG l.938 (a) and (b) | §A.2 |
| N10 | §D.4 labelled non-binding coordinator scheduling (PI Q4) | §D.4 |
| N11 | tier-2 English set: obligation and candidates (AI opinion), with the Flickr8K seal conflict | §D.7 |
| N12, N13 | the N14 OPS line and the gatekeeper 8/6-gram re-scan on the committed bytes listed as coordinator steps | §I |

## v1.1 changes (against v1 `8613a2b3`; kept as a record)

| CC-224 item | change in v1.1 | where |
|---|---|---|
| W1 gate-1 number | "~776 / ~38" replaced by at most **92** survivors, about **4.5** Composite-COCO images; recount shown; 14.9 GPU-h, E1 row, E-7 tail and Q6 replaced; EMPTY/THIN and outside-val2014 rules added; the 25-30% attrition withdrawn by erratum | §B.2 #12, E-7, E-14, §D.3, §H |
| W2 J-b | the "reading" removed. Route 1b: no COCO image staged, so J-b, P5, C1, the COCO-side C2 extractors and AMBER Q1 are moot. DOCCI dropped from J-b. 1a closure path in §D.6 | §A.6, §D.1, §D.5, §D.6, §G |
| W3 G2 scope | G2 only with a cited spent line; #4, #8, #10-#14, #22 and #24 (if held) are G3; per-block holds stated | §A.3, §A.4, §D.1 P6, §D.3, §D.4 |
| W4 freeze | binding freeze sentence | §A.3, E-15 |
| W5 J-i | verbatim erratum E-12 replacing v3.1 l.505-507 (trigger, deadline end of A2, reporting, no PA3, not a cap event) | E-12 |
| W6 A.5 fetch | erratum E-13 for the M1 gap fetch from the public COCO archive; citation fixed to v3.1 l.285-286 | E-13, §A.5 |
| W7 K2 pin | K2 is not a valid gate-2 source until a gatekeeper LOG pin line exists (coordinator step) | §A.2, §A.4 #2-#3, §D.1 P6 |
| N1 | A-T3 2014/2017 disclosure; direct featuring of val2017 in the M1 slot proposed | §A.2, §A.5, §G J-d |
| N2, N13 | 1a only: one-judge read of C1, overlay, C2 and a logged recount with a positive control; Composite release by URL and version | §D.6 |
| N3 | trim projected with the actual survivor count; H margin worded | E-7, §D.3 |
| N4 | title, status, P1, §G: full panel at irreversible 92 (CC-224) | header, §D.1, §G |
| N5 | P2 blocks the launch, not the adoption | §D.1 |
| N6 | E-range now E-1..E-15 | §C |
| N7 | LOG l.982 cited for Flickr30K test spent; PORTFOLIO l.171 "unscored" stale | §A.4 #23, §B.2 #13 |
| N8 | E-10 wording: the instance named in the launch LOG line | E-10 |
| N9 | G3 holds S and A1 until the M1 W25 slot after MT4 tier 2 (ETA 11-03) | §D.1 P6, §D.3, §D.4, Q2 |
| N10 | J-c accepted with citations; J-f: registered run order kept, interleave withdrawn | §B.2 #6, §D.3, §G |
| N11 | N18 queries include 2025-2026 Vietnamese and multilingual hallucination-metric work | §E |
| N12 | #24 PASCAL-50S: held or not recorded at P6 | §A.4, §D.1 P6 |
| licence (Ruling 10) | licence paragraph: commit plus laptop ids-only steps; feature recomputes flagged as not ids-only (new J-j) | header, §A.5, §G |
| N14 | the OPS-1102b-r5-draft LOG figures ("~38", "E-1..E-10") are superseded by CC-224; the next OPS line says so (coordinator step) | §I |

---

## A. Feature source and pre-fixed rule for every owner (CC-217r3 NB5, CC-217r2 W8)

### A.1 Two gates, kept apart

- **Gate 1, custody (id-first).** What may be staged on a rental. Composite-COCO and Polaris-test-COCO are matched, by
  id/file name on the laptop, against every COCO-id-space owner, before any image is staged; only id survivors and the
  Objects365 slice frame may reach the 4090 (v3.1 l.263, mirrored l.288; CC-217r3 B1 l.54, Ruling 2 l.45). **Under
  route 1b gate 1 is not run, because no COCO image is staged at all (E-12); the registered custody text is kept and is
  met more strictly.** In this amendment a "rental" is any host other than the custody host M1 (M1 is itself rented;
  CC-224r2 N5).
- **Gate 2, W25 completeness.** What B may decode or score. C1 byte match, C2 min(pHash, dHash) ≤ 10 incl. mirror AND
  SSCD ≥ 0.5, C3 SSCD > 0.75, against the features of every owner (v3.1 l.279-281; RULE.md l.38-42). Comparison on the
  laptop (v3.1 l.288). Owner caches never leave the laptop and never reach a rental [proposal, as E2b AMENDMENT_1 l.267].

### A.2 When a cache counts

A cache is a valid gate-2 source only if all three hold: (a) its sha256 is pinned in a committed file or a LOG line;
(b) a record states what it covers, as a count or a committed id list; (c) it was made by `build_memory.features` with
SSCD `sscd_disc_mixup` sha `9f26bd4c` in the venv-cenfeat freeze `1a639a50` (RULE.md l.28-30). A backup-mirror
SHA256SUMS line alone does **not** meet (a). The C stage-1 `feat_cache/feat_*.npz` files and the C `emb_*` SigLIP files
(E2b AMENDMENT_1 l.260) are not used.

| cache (laptop path) | sha256 | pin (a) | coverage record (b) | fn/env (c) |
|---|---|---|---|---|
| K1 `.session_backup/machines/M1/root/outputs/c_en/feats_coco_kval.npz` | `9783f7a6` | committed: RULE.md l.18 | KV-5,000 = `cen_coco_kval.tsv` `f7d8369f` (C-EN PREREG l.11), 0 unreadable (RULE.md l.18) | RULE.md l.29 |
| K2 `.../c_en/feats_coco_test.npz` | `2bc3b83e` | **none yet** (mirror `SHA256SUMS_feats` l.2 only). **Not a valid gate-2 source until a gatekeeper LOG pin line exists**, written before first use (coordinator step; provenance `chain_feats.log` l.11-12) | Karpathy test 5,000 = `cen_coco_test.tsv` `67555b28` (C-EN PREREG l.11, l.57) | same chain |
| K3 `.../c_en/feats_memory.npz` | `caf4a621` | committed: C-T3 PREREG l.132; LOG l.962 | 112,320 images (C-T3 PREREG l.131) of `cen_memory_allowed.tsv` `175907e2`, 112,322 rows = Karpathy train + restval 113,287 minus 965 refused ids (C-EN PREREG l.11, l.73) | same chain |
| K4 `.../c_en/feats_nocaps_val.npz` | `b69dac29` | committed: RULE.md l.19 | NoCaps val, 4,457 rows used after the 43 XM3600 ids (RULE.md l.19) | RULE.md l.29 |
| K5 `.../outputs/w25/feats_ut.npz` | `17d3ebf0` | committed: `2026-10-28_k2_gate1/w25_decide.json` l.34 | UT-2,402 (RULE.md l.17) | RULE.md l.30 |
| K6 `~/vsps_w25k1/oiv7_val.npz` | `2ca7e2f5` | committed: `2026-10-30_mt4_k1k6/w25k1_decide.json` l.74 | 41,164 (same file l.64) | LOG l.938 (a) freeze `1a639a50`, SSCD `9f26bd4c`; (b) parity n = 50 |
| K7 `~/vsps_w25k1/ktvic_test.npz` | `cd985050` | committed: w25k1_decide.json l.75 | 558 (l.65) | as K6 |
| K8 `~/vsps_w25k1/uitviic_test.npz` | `4f478490` | committed: w25k1_decide.json l.76 | 231 (l.66) | as K6 |
| K9 `~/vsps_w25k1/openviic_test.npz` | `f4c79b82` | committed: w25k1_decide.json l.77 | 2,001 (l.67) | as K6 |

Note on K8: E2b AMENDMENT_1 l.257 lists UIT-ViIC test 231 as having "no SSCD cache on any mirror". K8 is that cache
(laptop, outside `.session_backup`); a factual conflict for the E2b author, not a B item.

**COCO-id coverage rule [proposal].** K1 ∪ K2 ∪ K3 are keyed by COCO image id and together span the Karpathy split of
COCO 2014 train + val (123,287 = 113,287 + 5,000 + 5,000 [derived from C-EN PREREG l.73 and l.11]). For a COCO-id-space
owner O, covered(O) = O ∩ (the K1, K2, K3 id lists); gap(O) = the rest. Until K2 is LOG-pinned, its 5,000 ids count as
gap. Known gap sources: the 965 memory-side refusals (231 UIT-ViIC test, 372 CHAIR-500, 367 POPE-500, overlapping;
C-EN PREREG l.73), of which the UIT-ViIC test part is covered by K8, and 2 memory images without features
(112,322 − 112,320 [derived]). gap(O) is computed by an ids-only laptop step (C3, §D.5), counts printed, never feature
values.

**A-T3 val2017 disclosure (CC-224 N1).** COCO val2017 ids are COCO image ids, so the coverage rule reaches A-T3 val2017
through the 2014 caches. This assumes that each 2017 file carries the same pixels as the 2014 file with the same id;
**that assumption is unverified** and is disclosed in the W25 record. Proposed removal of the assumption: feature the
val2017 images directly in the M1 slot (§A.5), where they are held (LOG l.860), about 12 min CPU [derived: 5,000 ×
0.14 s/img, RULE.md l.113]; if they are no longer on M1, the assumption stays, disclosed.

### A.3 Pre-fixed rules for owners without a full cache [proposal]

- **G1 (cached).** Comparison against the pinned cache(s) on the laptop.
- **G2 (spent owner with a cited spent line, held by the group, gap not featured).** Deferred, a new rule extending W8:
  the gap is featured in the first custody-host slot (§A.5) and then checked against `b_pa1_dev_contacts.json`; any match
  leaves B's tier-1 rows, count only, no refill (v3.1 l.316). The check closes before the tier-2 prereg and before any
  slice-B use. Not a stop. **G2 applies only to an owner whose spent status is cited to PORTFOLIO l.191, a LOG line or a
  ruling (CC-224 Ruling 4 l.54).** Every other owner with a gap is G3. This departs from PORTFOLIO l.188 ("run the W25
  filter across all ledger owners before any decode") and from v3.1 l.317-319 ("not clean (a)" for an owner the rule
  cannot be applied to) only for the cited-spent owners, and only in time: their check runs before tier 2, not before
  tier-1 decodes.
- **G3 (owner without a cited spent line, images held by the group, gap not featured).** "Not clean (a)" (v3.1
  l.317-319) for every B block that would decode or score an image not yet checked against it, until the custody-host
  recompute is done.
- **G4 (images not held by the group, any status).** W8 deferred owner (v3.1 l.293-296; CC-217r2 W8 l.63): listed with
  its count, covered later against `b_pa1_dev_contacts.json` on arrival; not a stop. Where no count is published at
  HEAD, the count is recorded at arrival, before the check (a disclosed gap in W8's "with a count").
- **Slices.** Slice A and slice B keep their registered n = 2,000 as built from provisional survivors; a later G2 or G4
  match drops the image, counted, with no refill (v3.1 l.254, l.316).
- **Freeze (binding; CC-224 W4 l.68; E-15).** A G2 or G4 match found after any tier-1 freeze (SE_A/SESOI, NI,
  `T1_THRESHOLDS.json`, the judge prompt, the gate set, map v1, the A3 lever choice) never reopens that freeze. It is
  reported as a count. Any re-analysis without those images is one sensitivity row labelled POST HOC. The tier-2 prereg
  re-derives from the clean set. Such a match neither reverses a PA3 outcome nor fires a new one.

### A.4 Owner table (42 owners in `b_pa1_owners.json` + 2 conditional ledger rows)

Status = the builder's status (ae4b6630). Gate-1 column: "pool" = in the COCO id-first pool (not run under route 1b);
"n/a" = not a COCO id space. "Spent line" = the citation that allows G2.

| # | owner | status (n) | id space | gate 1 | gate-2 feature source | spent line | rule |
|---|---|---|---|---|---|---|---|
| 1 | kv4224_mt4 | held (4,224; ids `86d93863` = MT4 PREREG l.29 pin, LOG l.1150) | coco | pool | K1 (superset KV-5,000) | — (unspent) | G1 |
| 2 | karpathy_test_5000 | held (5,000) | coco | pool | K2 once LOG-pinned; until then none | PORTFOLIO l.191 | G1 after the K2 pin; before it G2 |
| 3 | m0_karpathy_test_probes_91 | held (91) | coco | pool | K2 (⊂ Karpathy test) once LOG-pinned | PORTFOLIO l.191-192 | as #2 |
| 4 | m0_dev_touched_3454 | held (3,454) | coco | pool | K1 ∪ K2 ∪ K3 by id; gap → M1 slot | none for the whole set (PORTFOLIO l.189: 73 ids never decoded) | G1; gap **G3** |
| 5 | a_t3_val2017 | held ids (5,000) | coco | pool | K1 ∪ K2 ∪ K3 by COCO id (disclosed, §A.2); direct featuring in the M1 slot proposed | LOG l.1037-1038 (A-T3 tier 3 done and scored) | G1; gap G2 |
| 6 | uitviic_test_231 | held (231) | coco | pool | K8 | PORTFOLIO l.191 | G1 |
| 7 | uitviic_val_924 | held (924) | coco | pool | K1 ∪ K2 ∪ K3 by id; gap → laptop CPU (UIT-ViIC images on the laptop) | PORTFOLIO l.191 | G1; gap G2 |
| 8 | uitviic_train_pool | held (2,695) | coco | pool | K1 ∪ K2 ∪ K3 by id, plus K5 for its UT-2,402 part; gap → laptop CPU or M1 | none (PORTFOLIO l.186 "needs ruling") | G1; gap **G3** |
| 9 | ut2402 | held (2,402) | coco | pool | K5 | — | G1 |
| 10 | coco_restval_b4 | held (30,504) | coco | pool | K3 | none (l.176 "feature cache only") | G1; gap **G3** |
| 11 | refused_coco2500 | held (2,500) | coco | pool | K1 ∪ K2 ∪ K3 by id; gap → M1 slot | none cited | G1; gap **G3** |
| 12 | refused_cv295 | held (295) | coco | pool | K1 ∪ K2 ∪ K3 by id; gap → M1 slot | none cited | G1; gap **G3** |
| 13 | refused_chair500 | held (500) | coco | pool | K1 (61, MT4 PREREG l.29) + K2 by id; the 372 memory-side ids have no cache (C-EN PREREG l.73) → M1 slot | none cited | gap **G3** (a certain gap) |
| 14 | refused_pope500 | held (500) | coco | pool | K1 (70, MT4 PREREG l.29) + K2 by id; 367 memory-side ids → M1 slot | none cited | gap **G3** (a certain gap) |
| 15 | xm3600_all | held (3,600) | openimages | n/a | laptop CPU recompute from `data/datasets/xm3600` (3,600 image files on the laptop) | PORTFOLIO l.191 | G2 until recomputed, then G1 |
| 16 | xm600_a | held (600) | openimages | n/a | ⊂ #15 | PORTFOLIO l.191 (⊂ XM3600 all) | as #15 |
| 17 | xm_test2500_c | held (2,500) | openimages | n/a | ⊂ #15 | PORTFOLIO l.191 | as #15 |
| 18 | oiv7_val | held (41,620) | openimages | n/a | K6 (41,164) + the 456 XM ids via #15 | — | G1 (XM part as #15) |
| 19 | nocaps_val | held (4,500) | openimages | n/a | K4 (4,457) + the 43 XM ids via #15 | — | G1 (XM part as #15) |
| 20 | ov_test_c | held (2,001) | openviic | n/a | K9 | — | G1 |
| 21 | ktvic_test_558 | held (558) | ktvic | n/a | K7 | — | G1 |
| 22 | refused_ktvic_dev_near_duplicate_of_test | held (1) | ktvic | n/a | laptop CPU (KTVIC images on the laptop) | none | **G3** until the laptop recompute (minutes; no M1 wait) |
| 23 | flickr30k_test_c | held (1,000) | flickr30k | n/a | no SSCD cache; M1 slot | LOG l.982 (C-T3 tier 3 scored, one look); PORTFOLIO l.171 "unscored" is stale | G2 |
| 24 | pascal50s_a | held (1,000) | pascal_voc2008 | n/a | M1 slot if its images are held there, else none; held-or-not recorded at P6 (N12) | none (l.165 unspent) | held → **G3**; not held → G4 |
| 25 | ade20k_val_a | held-nowhere (2,000) | ade20k | n/a | none: the M1 copy (LOG l.805) was lost with M1 on 10-29 (LOG l.821-822); hashes `4d83e0c2` (LOG l.807) have no SSCD | — | G4 |
| 26 | amber_generative | held-nowhere (1,004) | unresolved | moot under 1b (§A.6) | none (no AMBER image held; LOG l.1118) | — | G4 |
| 27 | docci | held-nowhere (n at arrival) | docci | n/a | none | — | G4 |
| 28 | h500 | held-nowhere (500) | ktvic | n/a | none (no list at HEAD) | — | G4; owner: PI Q3 |
| 29 | longcap | held-nowhere (n at arrival) | unresolved | moot under 1b | none | — | G4 |
| 30 | thumb | held-nowhere (n at arrival) | unresolved | moot under 1b | none | — | G4 |
| 31 | vapr | held-nowhere (n at arrival) | unresolved | moot under 1b | none | — | G4 |
| 32 | mtvqa_test | held-nowhere | mtvqa | n/a | none | — | G4 |
| 33 | textvqa_textcaps_val | held-nowhere | openimages | n/a | none | — | G4 |
| 34 | vindr_cxr_test | held-nowhere (3,000) | vindr_cxr | n/a | none | — | G4 |
| 35 | vintext_test | held-nowhere | vintext | n/a | none | — | G4 |
| 36 | viocrvqa_test | held-nowhere | viocrvqa | n/a | none | — | G4 |
| 37 | visignvqa_test | held-nowhere | visignvqa | n/a | none | — | G4 |
| 38 | vitextvqa_test | held-nowhere | vitextvqa | n/a | none (the laptop holds ViTextVQA dev subsets only) | — | G4 |
| 39 | vizwiz_val | held-nowhere (7,750) | vizwiz | n/a | none | — | G4 |
| 40 | nocaps_test_c | deferred (10,600) | openimages | n/a | none | — | G4 = W8 (v3.1 l.293-296) |
| 41 | openvivqa_dev_c | deferred (1,070) | openvivqa | n/a | none | — | G4 = W8 |
| 42 | b_pa1_dev_contacts | not yet written | mixed | exempt (W3) | — | — | owner for every later pass (v3.1 l.311) |
| c1 | ViTextCaps test (conditional) | builder: skipped | — | n/a | none (not released, PORTFOLIO l.167) | — | G4 conditional (§B.2 #6) |
| c2 | VieCap4H private test (conditional) | builder: skipped | — | n/a | none (references not published, l.170) | — | G4 conditional |

Not owners for B [proposal]: C's dev, rehearsal and datastore roles (XM3600-vi, KT-C, D-EN, T_A, O_B), because "C dev,
rehearsal and datastore images yield to every other owner" (PORTFOLIO l.193); their spent parents are owners above.
Objects365 v2 val: B's own one-look set, never its own owner (W3; builder ledger row).

**Summary after R5 v1.2.** Gate 1: not run under route 1b. Gate 2:
- G3 owners that hold S and A1 until the **M1 W25 slot**: #13 and #14 (certain gaps, 372 and 367 ids), and #4, #8, #10,
  #11, #12 if C3 finds a gap, and #24 if its images are held on M1.
- G3 owner that holds S and A1 only until a **laptop** recompute: #22 (and #8 if its gap images are on the laptop).
- G2 (no hold; checked before tier 2): #2, #3 until K2 is pinned; #5, #7 gaps; #15-#17 until recomputed; #23.
- G4 (no hold): #25-#41, c1, c2.

### A.5 Custody-host slots [proposal]

- **Laptop CPU (no GPU), not an ids-only step: after the R5 commit, P8 for C4, a logged start and the header licence line (J-j):** #15-#17
  (XM3600, 3,600 images), #22 (1 KTVIC image), #7 and #8 gaps if their images are on the laptop. Pinned env: the W25-K1 laptop venv, freeze `1a639a50`, SSCD `9f26bd4c` (LOG l.938 (a)).
  About 10 min [derived: 3,601 × 0.14 s/img, RULE.md l.113, × 1.2 for a 4-vCPU laptop [proposal]]. Never the laptop for
  A-T3 val2017 (v3.1 l.285-286).
- **M1 W25 slot, CPU only, wall cap 1.0 h [proposal], header licence line (J-j):** the COCO gap ids (given the K2 LOG pin of W7,
  §I: at most 965 + 2 − 231 = 736 [derived, C-EN PREREG l.73, C-T3 PREREG l.131, K8], plus any gap C3 finds; without the
  K2 pin the 5,000 Karpathy-test ids join the gap and the 1.0 h cap may not hold), fetched under E-13; A-T3 val2017
  featured directly (§A.2, N1); #23 Flickr30K test 1,000 and #24 PASCAL-50S 1,000 if held on M1. Slot: only after MT4 releases M1, never
  while an MT4 K1+K6 job is live or queued, never delaying MT4 tier 2 or 3 (v3.1 l.269-270; CC-215 B8 l.71; PI-1101q LOG
  l.1091). MT4 tier 2 ETA: 11-03T03:30Z at projection, 11-03T11:30Z at caps (LOG l.1100). The slot precedes B's M1
  custody decode block (v3.1 l.264-272). Whether it may use the gap before MT4 tier 3: PI Q2. Money gate: P2 (met,
  LOG l.1163-1164); each start still logs a balance line (LOG l.1164). **Fails closed (CC-224r2 N6):** if the slot hits
  its 1.0 h wall cap, or K2 is still unpinned when it starts, S and A1 stay held; a re-run needs its own logged line.

### A.6 The four unresolved id spaces

**Under route 1b these id spaces matter only for gate 2, where all four owners are G4 (held nowhere).** Gate 1 is not
run, so no extractor (C2), no `id_first` run (C1), no AMBER read (Q1) and no Composite or Polaris id list (P5) is needed
for tier 1. The paths below are kept for the later W25 passes (the deferred check against `b_pa1_dev_contacts.json`);
a route-1a use would come back to the panel (§D.6).

| owner | where an id list could come from (ids only) | id space expected |
|---|---|---|
| VaPR | local release `.session_backup/2026-10-15/r13_data/vapr_30k/vapr-30k.json` (HF `VaPR-UCLA/vapr-30k` at `261940f2`, q4 prereg l.9); image-path field only | LLaVA-665K image paths (q4 prereg l.9); COCO paths give COCO ids [unverified] |
| LongCap(-Arena) | local release `.session_backup/2026-10-15/r13_data/longcap_arena_vela_repo/` (VELA `666e33c7`, q2 prereg l.9-10); image-id column only | unknown until extracted |
| THumB | no local copy (R12 raw files were in a removed scratchpad, `h1_g2_g3_polaris_docci.py` l.36-37); the public THumB release, image-id field only, sha recorded at fetch, no PI e-mail | COCO ids if THumB images are Karpathy test images [unverified] |
| AMBER generative | no local copy (LOG l.1118); the public AMBER query file, image-name field only; fenced by CC-207 Q2 NOT YET (E2b PREREG l.181-189) | unknown |

DOCCI is not among them: its id space is `docci` (owner #27), not unresolved (CC-224 W2 l.66).

### A.7 Owners file: keep ae4b6630, add an R5 overlay (J-g accepted, CC-224 Ruling 9 l.59)

`b_pa1_owners.json` `ae4b6630` stays frozen (LOG l.1150; NB8). No id list changes. R5 adds a small ids-free overlay
`b_pa1_r5_rules.json` (owner key → rule G1-G4, spent-line citation, feature source and sha), generated from §A.4 and
pinned by sha in the R5 commit. The laptop decide step (C5) reads both and checks both shas.

---

## B. Owner names refreshed from PORTFOLIO §2.3 at HEAD, and the reported conflicts

### B.1 Names (PORTFOLIO_3Y `910ab3bf` at HEAD `1f23d30`)

C's sets come from PORTFOLIO l.167-171 and l.193 and `C_DIRECTION_v4_1` (CC-219r3 GO, LOG l.1127; commit `d68b1e7`,
LOG l.1128): NoCaps test (10,600; l.168), OpenViVQA dev (1,070 images; l.169), Flickr30K Karpathy test (l.171);
conditional, only if publicly released before C's tier-3 freeze: ViTextCaps test (l.167), VieCap4H private test (l.170;
C_DIRECTION_v4_1 l.182-183). Other owners as §A.4, by the first cell of each §2.3 row (builder ledger, ae4b6630).

### B.2 Conflicts

| # | conflict | evidence | resolution |
|---|---|---|---|
| 1 | H-500 owner: ledger B, v3.1 l.302 lists it with A's test lists | PORTFOLIO l.172 "B (needs PI line, W5)"; B_DIRECTION_v3 l.357 lists H-500 apart from A's sets | Erratum E-5; owner to the PI (Q3). For this pass: #28, G4 |
| 2 | `kv4224.txt` absent at HEAD | derived from `scripts/grl/id_counts.py` `0c590058` `kv_pool_a_excluded`; ids sha `86d93863` = MT4 PREREG l.29 pin, MATCH (LOG l.1150) | Resolved; erratum E-9. Gate-2 features use the KV-5,000 superset K1 (RULE.md l.22: a superset only excludes more) |
| 3 | CC-214 citation (v3.1 l.306) | C ledger rests on CC-219r3 / C_DIRECTION_v4_1 (PORTFOLIO l.193); CC-217r3 NB5 l.63 | Erratum E-6 |
| 4 | `exclusion.json` extra owners (coco2500, cv295, chair500, pope500), plus UIT-ViIC val 924 and nocaps val | v3.1 l.297-299 "Never a closed list; at least" | Resolved: kept (#11-#14, #7, #19); extra owners only exclude more |
| 5 | OIV7 val held as all 41,620, ledger row 41,164 (l.175) | RULE.md l.21-22; PI-1102a Q11 (LOG l.1140), ledger ruling ≥ 92 pending | Resolved: superset; the 456 XM ids are #15, the NoCaps val ids #19; no shared id space with B's sets |
| 6 | ViTextCaps and VieCap4H dropped by the builder as "stale" | PORTFOLIO l.167, l.170 and C_DIRECTION_v4_1 l.182-183 keep them as conditional C owners; v3.1 l.293-296 names them W8 deferred | Kept as G4 conditional (c1, c2); departs from the literal "drop" of CC-217r3 NB5 l.63. Accepted on the merits (CC-224 Ruling 9 l.59, N10) |
| 7 | NB3's correction target "B_DIRECTION_v3 l.48" (also in v3.1 l.263) | l.48 of `ef1e3cc5` is a heading; the rental rule is at l.228-229 | Erratum E-2 cites l.228-229 |
| 8 | Cap: v3.1 l.503 says 20 GPU-h; commit 5ff00c9 message line 6 freezes 22 GPU-h (PI-1102a B-Q2) | CC-217r3 Ruling 5 l.48 wanted 22 h in the file; it went into the commit line only | Erratum E-7; the commit line governs (CC-209c) |
| 9 | ADE20K val: builder says held nowhere; LOG l.805/l.807 show a 10-29 download on M1 | M1 lost 10-29 ~21:30Z (LOG l.821-822); hashes `4d83e0c2` without SSCD | Builder is right: G4 (#25) |
| 10 | E2b AMENDMENT_1 l.257: "UIT-ViIC test 231 ... no SSCD cache" | K8 `4f478490`, pinned at w25k1_decide.json l.76 | For the E2b author; B uses K8 |
| 11 | No id list or pinned release exists for Composite-COCO | CC-217r3 NB3 l.61; R12 raw files gone (`h1_g2_g3_polaris_docci.py` l.36-37) | Moot under route 1b (E-12). Under 1a, R5 returns to the panel (§D.6) |
| 12 | Registered attrition "roughly 25-30%" (v3.1 l.313-316) vs the registered gate-1 pool | **Recount below** (ids only): at most **92** val2014 ids survive gate 1; about **4.5** Composite-COCO images | Erratum E-14 withdraws the 25-30%; E-12 (route 1b) makes E1/E2 NOT RUN; the English benchmark moves to tier 2 (PI Q-EN) |
| 13 | Flickr30K test status | PORTFOLIO l.171 says "unscored"; LOG l.982 records the C-T3 tier-3 score (one look) | LOG l.982 governs; #23 is spent (G2). The PORTFOLIO cell is stale (N7) |

**Gate-1 recount (§B.2 #12), from ids only, run on the laptop at drafting.** Inputs: the owner id lists in
`b_pa1_owners.json` `ae4b6630` and the KV-5,000 id list `kv5000.txt` `b7a7a89d` (the owners file holds no Karpathy-val
list, so this one ids-only file is needed; CC-224 l.38 checked the same file).
1. Under the Karpathy split convention, val2014 = restval + Karpathy val + Karpathy test: 30,504 + 5,000 + 5,000 =
   40,504 [derived, convention]. kv4224_mt4 ∪ karpathy_test_5000 ∪ coco_restval_b4 = 39,728 ids, pairwise disjoint
   (counted). So the val2014 ids outside those three owners are KV-5,000 ∖ KV-4,224 = 5,000 − 4,224 = **776**
   (counted: kv4224_mt4 ⊂ kv5000, residual 776).
2. Residual ∩ each other COCO-id owner (counted): a_t3_val2017 **80**, m0_dev_touched_3454 **434**, refused_chair500
   **61**, refused_pope500 **70**, uitviic_train_pool **132**; every other COCO owner **0** (karpathy_test_5000,
   coco_restval_b4, m0 probes 91, uitviic_test_231, uitviic_val_924, ut2402, refused_coco2500, refused_cv295).
3. The five counts sum to 777 but overlap: their union inside the residual is **684** (counted; 777 − 684 = 93 ids
   counted twice).
4. Survivors: 776 − 684 = **92** val2014 ids (counted), i.e. 92 / 40,504 = 0.23% of val2014 [derived].
5. Expected Composite-COCO survivors under independence: 1,996 × 92 / 40,504 ≈ **4.5** [derived; 1,996 from v3.1
   l.232]. Polaris-test-COCO: the same 0.23% of its count, from the same 92 ids (shared with Composite).
This agrees with CC-224 l.39 and replaces v1's "≤ 776" and "≈ 38", which omitted step 2.

---

## C. Errata to the registered text (E-1..E-15; v3.1 is not edited; these bind from the R5 commit)

- **E-1 (NB2, CC-217r3 l.60).** l.255, for "Slice B images are never decoded, scored or staged in tier 1." read:
  "Slice B images go to the 4090 for W25 features only; they are never decoded or scored in tier 1."
- **E-2 (NB3(i), l.61).** l.263, for "(CC-217r3 B-new-1; B_DIRECTION_v3 l.48.)" read "(CC-217r3 B-new-1;
  B_DIRECTION_v3 l.228-229.)". (In `ef1e3cc5`, l.48 is a heading; §B.2 #7.)
- **E-3 (NB3(ii)).** l.278, for "(PORTFOLIO_3Y l.185)" read "(PORTFOLIO_3Y §2.3 l.188, blob `910ab3bf`)".
- **E-4 (NB3(iii)).** l.290-292, for "not against A's registered Composite/Polaris lists
  (`manuscript/prereg/2026-10-14_h1_polaris_docci.md`, G2 Polaris test); B's dev use of them is the disclosed reuse of
  §2 / N9." read "not against A's registered Polaris list (`manuscript/prereg/2026-10-14_h1_polaris_docci.md`, G2 Polaris
  test); A registered no Composite list. B's dev use of Polaris and Composite is the disclosed reuse of §2 / N9."
- **E-5 (NB5, §B.2 #1).** l.301-302, delete ", H-500" from A's list; add a bullet "H = 500 KTVIC-train ∩ OV-train-only
  (PORTFOLIO l.172; owner per PI Q3 of R5; no list at HEAD, R5 rule G4)."
- **E-6 (NB5, §B.2 #3, #6).** l.293-295, for "(C's planned one-look sets: ViTextCaps test, NoCaps test, VieCap4H
  private test, until held)" read "(C's unspent sets not held: NoCaps test 10,600 and OpenViVQA dev 1,070, PORTFOLIO
  l.168-169; conditional, if publicly released: ViTextCaps test and VieCap4H private test, l.167, l.170)". l.305-306, for
  "C's planned one-look sets: ViTextCaps test, NoCaps test, VieCap4H private test (PLAN_2026-11-01 l.70), and any CC-214
  assignment present at run time;" read "C's sets per CC-219r3 / C_DIRECTION_v4_1 (`8334cf5d`) and PORTFOLIO l.167-171,
  l.193 at run time;".
- **E-7 (NB7, §B.2 #8; PI-1102a B-Q2; numbers restated after CC-224 W1).** l.283-284 "inside the 20 h cap" → "inside the
  22 h cap". l.503: "Hard cap: 22 GPU-h (PI-1102a B-Q2, commit 5ff00c9)". l.511 from "At the assumed rates" through
  l.516 "R5 restates the rate.)" replaced by (route 1b, with E-12; the criterion of l.510-511, "blocks are dropped from
  the bottom of the trim order until 1.25 × (projected remaining hours) ≤ remaining cap.", stays in force):
  "At the assumed rates the trim rule drops A4 (after S: 22 − 1.0 − 0.9 = 20.1 h remain; A1 + A2 + A3 + H =
  5.4 + 1.1 + 5.8 + 0.6 = 12.9 h, 12.9 × 1.25 = 16.1 ≤ 20.1; with A4, 16.9 × 1.25 = 21.1 > 20.1). The expected spend is
  then W + S + A1 + A2 + A3 + H = 14.8 GPU-h plus 4 h setup = 18.8 h, about 329,000 VND at M8's 17,499 VND/h, and at most
  (22 + 4) × 17,499 ≈ 455,000 VND at the cap. With W + S taking 1.9 h as assumed, H runs only if block-S rates are at
  most 24.6% above the assumed ones, A3 runs up to 30.7% above, and A4 runs only if they are at least 4.9% below; the
  rule itself always uses the measured remaining cap after S, so these thresholds move if W or S run long or short."
  [derived from v3.1 l.491-502 and LOG l.1109:
  20.1/16.125 = 1.246; 12.3 × 1.25 = 15.375, 20.1/15.375 = 1.307; 20.1/21.125 = 0.951; 17,499 × 18.8 = 328,981;
  17,499 × 26 = 454,974]. l.648 Q-a status: "PI-1102a: 22 h". (v1's 17.9 h / 383,000 VND and 14.9 h figures are
  withdrawn: the first assumed the registered 3.1 h of E1, the second rested on the wrong 776 bound.) The l.501 total
  row is restated in the E-12 list. The M8 idle bill while S and A1 wait (§D.4) is not in these figures.
- **E-8 (CC-218 N15 l.80 = CC-215r2 ruling 7 l.50, NB-C10 l.64; E2b AMENDMENT_1 l.318).** Add to §2 after l.107,
  verbatim from E2b PREREG l.193-194: "B's verifier is chosen only from B's own tier 1, never from E2b outputs; E2b's
  number gold (iscrowd rule, v2 4.4) and B's (section 3.3 K cap) differ by design." (B's K cap is v3.1 l.97-98.)
- **E-9 (§B.2 #2).** l.300, for "MT4 KV-4,224 (COCO instances_val2014; `2026-10-28_mt4_kv`)" read "MT4 KV-4,224
  (derived by `scripts/grl/id_counts.py` `0c590058` `kv_pool_a_excluded`, ids sha `86d93863` = MT4 PREREG l.29 pin;
  `kv4224.txt` is not at HEAD)".
- **E-10 (CC-217 N15 l.102; CC-224 N8 l.81).** l.485-487: the host is **the ckey instance named in the launch LOG line**
  (instance 111947, alias M8, at drafting), RTX 4090, **17,499 VND/h** plus a 30 VND setup fee (LOG l.1109); maximum
  rental to 2026-11-15T14:20Z (LOG l.1109). No host name, IP or port. A host substitution needs a new E-10 restatement
  and a one-judge diff read before any B step on the new host.
- **E-11 (§5.4 owner list).** l.297-311 is read together with §A.4 of this amendment (42 owners + c1, c2) and the
  overlay of §A.7.
- **E-12 (CC-224 W5 l.69; CC-224r2 W1, W3, W4; replaces v3.1 l.505-507 from "The core" to "the PI decides.").**
  Verbatim replacement text:
  "Route 1b (in force only on a logged PI line Q-EN = 1b that precedes the R5 commit). The core W + S + A1 + A2 ≈
  8.4 h (10.5 h with +25%) is never trimmed; if it cannot finish under the cap, tier 1 stops and the PI decides. E1
  (Composite-COCO) and E2 (Polaris-test-COCO) are NOT RUN at tier 1. Trigger: that PI line, fixed before any rate or
  output exists, from id-list counts only (gate 1 leaves at most 92 val2014 ids, R5 §B.2). No Composite-COCO or
  Polaris-test-COCO image is fetched or staged on any host, and gate 1 is not run. Deadline: the NOT RUN status is
  written into the tier-1 run log no later than the end of block A2. Reporting: the tier-1 report lists E1 and E2 as
  "NOT RUN (pre-fixed, R5 E-12)", and no reason text appears in the paper, supplement or cover letter (§2, PI-1101p
  Q3). No PA3, not a stop, not a cap event; nothing else in tier 1 waits for E1 or E2. If Q-EN = 1a, R5 returns to
  the panel before any commit."
  (The CC-224 W5 text for a route-1a contingency, E-12 (ii) of v1.1, is struck; CC-224r2 Ruling 6.)
  **Lines overridden under E-12** (each read at v3.1 `e9b30ca7`; they apply with E1, E2, Composite-COCO and
  Polaris-test-COCO struck):
  - l.27 (closure row W6, W7): the English E1 prompts are not written or pinned at tier 1.
  - l.69-72 (§0: "and the English dev block E1 (Composite-COCO). E1's GPU outputs may be produced early, ..."): struck
    from "and the English dev block E1" to "(§6.4)."; the 4090 list reads "block W, every slice-A block, the Vietnamese
    gate (§4.4)".
  - l.89 (H3 row): "no tier-1 row (R5 E-12); the English human-rated benchmark is in the tier-2 prereg, on a set
    outside the COCO val2014 owners named by a ledger ruling at ≥ 92 (PI-1026; R5 §D.7)".
  - l.232-233 (§5.1 rows Composite, Polaris): role "not used at tier 1 (R5 E-12)".
  - l.236-238 (Composite source-label removal; caption counts from metadata): not applied at tier 1.
  - l.239-241 (BLEU/CIDEr/BERTScore on Composite-COCO and Polaris): not computed on them at tier 1.
  - l.263 and l.288 (id-first custody sentence): kept verbatim; nothing from Composite or Polaris is staged, so only the
    Objects365 slice frame goes to the 4090.
  - l.282-283 (block W): "and the id survivors of Composite-COCO and Polaris-test-COCO" struck.
  - l.313-316: as E-14.
  - l.422-426 (§7.4): under E-12 no English prompt is written or pinned at tier 1; the tier-2 prereg selects the
    English decomposer and verifier prompts. The pre-S pins of l.422-424 and P9 cover every listed prompt except the
    English E1 decomposer and verifier prompts; l.425-426 has no tier-1 effect.
  - l.492 (§9.1 row W): "W25 features of the Objects365 slice frame only (§5.4)".
  - l.499-500 (§9.1 rows E1, E2): "NOT RUN (R5 E-12)".
  - l.501 (total row): "18.8 (+25% = 23.5)" = W 1.0 + S 0.9 + A1 5.4 + A2 1.1 + A3 5.8 + H 0.6 + A4 4.0, with E1 and E2
    NOT RUN [derived from l.492-498; CC-224r2 l.43].
  - l.505 (trim order): "A4, H, A3" (E2 struck).
  - l.508-509 (run order W5): "W, S, A1, A2, then A3, H, A4"; the E1 sentence struck.
  - l.526 (§9.2 rates leaving tier 1): r_e,EN and p_EN are not measured at tier 1; they are measured in the tier-2
    English block and enter P_EN of l.528 from there.
  - l.548 (§10 descriptive list): "English rows (H3)" has no tier-1 entry.
  - **Catch-all:** any other v3.1 mention of E1, E2, Composite-COCO, Polaris-test-COCO or H3 (for example l.278,
    l.289-291, l.611, l.627, l.644, l.649) is void at tier 1 under E-12.
- **E-13 (CC-224 W6 l.70; departs from v3.1 l.284-286, "recomputed on the host that already holds that set under its
  custody rule").** Add after the sentence ending "never on a rented host." (l.286): "Owner ids in a W25 gap whose
  images no host holds today (R5 §A.2) are featured on M1 only. M1 is the m3-role custody host for test images
  (CC-209 r1(a)). The steps are fetch, feature, delete, log: the images are fetched on M1 from the public COCO archive, featured by `build_memory.features` in the pinned env,
  deleted as soon as their features exist, and the deletion is logged with UTC time, folder and file count (RULE.md
  l.68 pattern). Never on a rental (any host other than the custody host M1), and never on the laptop for A-T3
  val2017 (l.285-286). The M1 slot rule of §5.3 (l.269-270) applies."
- **E-14 (CC-224 W1 l.65; CC-224r2 N3; replaces the whole v3.1 l.313-316 bullet, from "- **Expected attrition" to
  "replace the losses.").** "- **Expected attrition and shortfall branch (N8):** Composite-COCO and Polaris-test-COCO
  are val2014 ids, matched by id against every COCO-id-space owner of `b_pa1_owners.json` (l.263). Gate 1 leaves at
  most 92 of the 40,504 val2014 ids (R5 §B.2 #12, counted from owner ids), about 0.23% of each set, about 4.5
  Composite-COCO images. The earlier estimate of roughly 25-30% is withdrawn. A set with 0 survivors is EMPTY (NOT RUN,
  reported, no PA3, not a stop, not a cap event); a set with 1-499 survivors is THIN and no English tier-1 conclusion is
  drawn from it. A Composite or Polaris id outside val2014 (a train2014 id, or an id with no COCO split) is matched
  against every COCO-id-space owner like the others and is counted separately by split in the report; a non-COCO id is
  removed by source label first (l.236-237). Under E-12 these counts are computed only if the id lists are ever
  built; no image is staged. Nothing is added to replace the losses."
- **E-15 (CC-224 W4 l.68).** Add to §5.4 after l.316 and to §6.4 after step 8: "A G2 or G4 match (R5 §A.3) found after
  any tier-1 freeze (SE_A/SESOI, NI, `T1_THRESHOLDS.json`, the judge prompt, the gate set, map v1, the A3 lever choice)
  never reopens that freeze. It is reported as a count. Any re-analysis without those images is one sensitivity row
  labelled POST HOC. The tier-2 prereg re-derives from the clean set. Such a match neither reverses a PA3 outcome nor
  fires a new one."

---

## D. The 4090 block plan (route 1b)

### D.1 Preconditions (each a LOG line with shas, in this order where it matters)

| P | condition | status at drafting |
|---|---|---|
| P1 | this R5 amendment adopted by the round-3 full panel at irreversible 92 (CC-224, CC-224r2), then the gatekeeper commit, which needs a logged PI line Q-EN = 1b time-stamped before it (commit precondition) | open; no PI line on Q-EN yet (CC-224r2 l.50) |
| P2 | a **logged PI top-up** (balance line). Blocks the launch, not the adoption (CC-224 N5); it also gates the M1 slot | **met at text level**: PI-1102b (LOG l.1163, 2026-11-02T03:56:44Z, "closes B R5 P2") and OPS-1102topup (LOG l.1164: +1,000,000 VND, balance 1,194,532 VND at ~11:00 VN 02/11; M1 + M8 26,781 VND/h, ~44.6 h). Each launch and each M1 slot start still logs its own balance line (LOG l.1164) |
| P3 | N18 rescan done and logged (§E) | open |
| P4 | Objects365 v2 train annotation file + `patch0`, `patch1` on the laptop, R6 sha (v3.1 l.74-77, l.656-657); after the top-up (PI-1102a B-Q4) | open |
| P5 | gate 1 (Composite/Polaris id lists, `id_first`) | **moot under route 1b** (E-12) |
| P6 | gate-2 owner side: G1 caches present at their shas; K2 LOG-pinned by the gatekeeper before its first use (W7); C3 coverage run, gap counts logged; laptop recomputes (#15-#17, #22, #7/#8 if on the laptop) done; #24 held-or-not recorded (N12); the M1 W25 slot done for the G3 gaps (#13, #14 and any C3 gap of #4, #8, #10-#12, #24). **Until this slot, S and A1 are held** (G3) | open; the recomputes wait for the R5 commit and the licence line (header); the M1 slot also waits for P2 (met), MT4 tier 2 (ETA 11-03T03:30-11:30Z, LOG l.1100) and Q2 |
| P7 | M8 hand-over: single tenant; no image on M8 other than B's Objects365 frame (v3.1 l.263). E2b's 769 images (E2b AMENDMENT_1 l.263) deleted, deletion logged, before any B image is staged | open |
| P8 | code C3-C6 (§D.5): CPU selftest, SHA256SUMS LOG line and a one-judge code read of each piece before first use (CC-223; CC-224 Ruling 10) | open |
| P9 | R-items by first use (v3.1 l.653-659): R2 venv freezes before step 1; R1 model pins before each model's first output; prompt shas before block S for every v3.1 l.422-424 prompt except the English E1 decomposer and verifier prompts, which are not written at tier 1 (E-12) | open |
| P10 | map v1 and parity run 1 (laptop) each with their own logged start (CC-217r3 Ruling 6 l.49), before A1-decode | open, not needed for W |

### D.2 Block W on M8, first

- Stages only the Objects365 slice frame along the registered order (blocks of 500 until 4,000 survivors); no COCO
  image and no COCO archive (v3.1 l.263, l.283; E-12).
- Features: `build_memory.features` (unchanged), SSCD `9f26bd4c`, in a venv built from freeze `1a639a50`, CPU
  [proposal]. **Comparability check before use:** n = 50 frame images featured on M8 and on the laptop, in the
  OPS-1030w25k1e (b) form (LOG l.938); pass iff hashes are equal on all 50 and SSCD cosine ≥ 0.9999 [proposal].
- **Env risk:** M8 has Python 3.12.3 only and venv-cenfeat was built on M3 (E2b AMENDMENT_1 l.273-275). A failed install
  or check is an operator FAULT, not a W25 outcome; fallback [proposal]: block-W features on the laptop CPU in the W25-K1
  venv (LOG l.938 (a)) from the PI's laptop download. No GPU-h.
- Only feature files leave M8, by hand pull with sha, logged. Decisions on the laptop (C5), counts only, no reason text,
  no overlap wording (PI-1101o, PI-1101p Q3; v3.1 l.320).
- Block W needs no owner feature; it is not held by G3. Cap 1.0 GPU-h (v3.1 l.492) inside the 22 h.

### D.3 Order and caps inside 22 GPU-h (registered run order W5, v3.1 l.508, without E1/E2 under E-12)

| order | block | GPU-h est. (v3.1 l.491-502) | cumulative | at the assumed rates | held by |
|---|---|---|---|---|---|
| 1 | W | 1.0 | 1.0 | runs | — |
| 2 | S (smoke + VN gate on the first 231 slice-A images) | 0.9 | 1.9 | runs; trim rule applied at its end | G3: the header licence line for recomputes, then the M1 W25 slot (P6) and the #22 laptop recompute |
| 3 | A1 (A1-decode, then laptop steps 4-5, then A1-score) | 5.4 | 7.3 | runs (core) | as S |
| 4 | A2 | 1.1 | 8.4 | runs (core) | follows A1 |
| — | E1, E2 | 0 | — | NOT RUN (E-12) | — |
| 5 | A3 (levers) | 5.8 | 14.2 | runs while rates ≤ +30.7% at W + S = 1.9 h (E-7) | follows A2 |
| 6 | H (H2 descriptive) | 0.6 | 14.8 | runs while rates ≤ +24.6% at W + S = 1.9 h (E-7) | follows |
| 7 | A4 | 4.0 | — | trimmed unless rates ≥ 4.9% below assumed, at W + S = 1.9 h (E-7) | — |

Expected 14.8 GPU-h + 4 h setup [derived]; cap 22 GPU-h with per-step `timeout`; CAP STOP final; one resume only for
machine loss or a guard failure (v3.1 l.503-520). Setup on M8 may be shorter than 4 h because M8 is already set up (LOG
l.1109); the planning number stays 4 h [proposal]. The registered run order is kept; v1's E1 interleave is withdrawn
(J-f, CC-224 N10).

M1 (separate host, unchanged): the custody decode block, about 5.8 h, hard cap 9 GPU-h at 9,282 VND/h, only after MT4
releases M1 (v3.1 l.264-272, l.517-518), preceded by the §A.5 W25 slot.

### D.4 Host and order on M8 [proposal; non-binding coordinator scheduling, PI Q4; CC-224r2 N10]

Contenders: B tier 1 (22 h cap + setup), VSPS-J E2b tier 1b-i (≤ 6.5 h in its v1.1, held for PI QG1 and its CC-223r2 read; LOG
l.1148, l.1165), C tier 1 (cap min(⌈1.25 × P1⌉, 37) GPU-h; PI-1102a Q-cost, and Q-custody "M8 after E2b or new rental, named by
amendment", LOG l.1140). M8 is idle since 00:27:36Z (LOG l.1146) and is rented to 2026-11-15T14:20Z (LOG l.1109).

1. **Ready first, single tenant, never concurrent** (CC-215r2 ruling 3 l.46: E2b runs alone on the GPU).
2. **E2b 1b-i first if its gates clear before B's.** B's block W cannot start before the Objects365 download (P4), and
   B's S and A1 are held until the M1 W25 slot after MT4 tier 2 (P6, ETA 11-03), so a 6.5 h E2b block (E2b
   AMENDMENT_1 v1.1 caps, LOG l.1165) fits inside B's wait. E2b then deletes its 769 images with a logged deletion (P7).
3. **B tier 1 next.** Block W may run as soon as P1-P4, P7-P9 hold, before the M1 slot; S and A1 follow the recompute licence and the
   slot. **Idle bill (CC-224r2 N8):** M8 bills 17,499 VND/h whether idle or not (LOG l.1109, l.1140); every hour M8
   waits between W and S costs about 17,499 VND and is outside the 455,000 VND cap figure of E-7. Recommended
   [proposal]: start W only when the M1 slot is scheduled, or fill the wait with E2b or C (items 2 and 4). If B
   is ready while E2b 1b-i has not started, B goes first (CC-215r2 ruling 3 ranks VSPS-J after B tier 1 and ready C
   jobs; a ruling on the rate run, applied by analogy).
4. **C tier 1 after B** on M8, or on a new rental by C's own amendment.
5. Fit: 6.5 + (22 + 4) + 37 = 69.5 h [derived], against about 13 days to 11-15T14:20Z.
6. Keep the queue full; the idle-delete rule (PI-1031c, LOG l.976) applies. The OPS-1102balance-risk default (LOG
   l.1155) is cancelled by PI-1102b (LOG l.1163). If M8 is deleted, the new host needs a new E-10
   restatement and a one-judge diff read (E-10).

### D.5 Code still to write under route 1b (none written; each needs P8 before first use)

- C3 coverage step: owner ids vs the K1-K3 id lists (`cen_*.tsv`), counts printed; gap id lists sha-pinned.
- C4 block-W feature wrapper (frame in blocks of 500). `scripts/w25/w25.py` cannot run as committed outside m3 and on
  these sets (E2b AMENDMENT_1 l.229-232); reuse `build_memory.features` and `w25.rule` unchanged.
- C5 laptop decide: W25 criteria C1-C3 against every G1 cache, reading the §A.7 overlay; counts only; exclusions as sha-pinned id
  lists.
- C6 `b_pa1.py slices` (ijson streamed, `images[]` only; v3.1 l.251-255).
- Moot under route 1b: C1 (`id_first` CLI) and C2 (ids-only extractors for Polaris test, Composite, VaPR, LongCap,
  THumB, AMBER).

### D.6 If the PI picks route 1a

R5 returns to the panel before any commit (CC-224r2 W3, Ruling 6). No route-1a text is part of this amendment; v1.1's
§D.6 and E-12 (ii) are struck.

### D.7 Tier-2 English set (obligation under E-12; CC-224r2 N11; PI-1026)

- **Obligation.** The tier-2 prereg names one English human-rated set for the English benchmark, outside every owner in
  `b_pa1_owners.json` and §A.4, chosen by a ledger ruling at ≥ 92 before the tier-2 prereg is read. It selects the
  English decomposer and verifier prompts (E-12 list, l.422-426) and measures r_e,EN and p_EN (l.526).
- **Candidates (AI opinion, not a choice):** Flickr8K-Expert / Flickr8K-CF ratings; Composite's Flickr8K and Flickr30K
  parts. Each must pass W25 against C's Flickr30K test 1,000 (owner #23) and every other owner, and must not touch C's
  NoCaps sets (#19, #40) or A's registered lists.
- **Conflict to settle in that ruling:** Flickr8K-Expert is sealed for B as its English one-look candidate (v3.1
  l.131-133, §3), and Flickr8K-CF and Composite's Flickr8K part share the Flickr8K image pool. Using any of them as a
  tier-2 dev set would need the seal rule settled first; Composite's Flickr30K part avoids the Flickr8K seal but meets
  owner #23 by W25.

---

## E. N18 novelty rescan (requirement only; this draft does not run it)

- **Source:** CC-217 N18 (l.105, "before the 4090 spend"); v3.1 l.620, l.65-66, l.521-523; B_DIRECTION_v3 P10 l.397.
- **Covers:** an OpenAlex + Semantic Scholar rescan for the B claim (object-grounded, decomposed, Vietnamese caption
  factuality metric vs a same-backbone judge), including the P10 list: ALOHa (2404.02904), FaithScore (2311.01477),
  CapMAS (2412.15484), DCScore (2503.07906), CompreCap, CapProbe, OpenCHAIR, Gomes et al. (2502.06600). Query families
  [proposal]: proposition-level or decompose-then-verify caption metrics; **2025-2026 Vietnamese and multilingual
  hallucination-metric work** (CC-224 N11); Objects365- or detector-grounded caption evaluation; VLM-as-judge vs a
  decomposed verifier. Also checked: the R11 literature map rebuilt on OpenAlex + S2.
- **How:** laptop, no GPU, no data read; API requests carry no PI address (vsps-research@example.org or none).
- **Output [proposal]:** `manuscript/prereg/2026-11-01_b_pa1_tier1/N18_RESCAN.md` with queries, `date -u` stamps, hit
  counts, the papers read, and an AI-opinion novelty-doubt percentage; its sha goes in a LOG line. No "first" claim.
- **Gate:** done and logged **before block W** (P3). A doubt ≥ 80% triggers the pivot rule and goes to the PI before
  any 4090 step [proposal]. The rescan never edits v3.1.

---

## F. Closure table

### F.1 CC-217r3 NB1-NB11 and CC-217r2 / CC-217 / CC-218 carries

| item | asked | where closed |
|---|---|---|
| NB1 (l.59) | STATE refreshed, said in the commit line | closed at the commit: 5ff00c9 message line 7; LOG l.1141 |
| NB2 (l.60) | slice-B wording | E-1 |
| NB3 (l.61) | three citation fixes | E-2 (with the l.228-229 correction), E-3, E-4 |
| NB4 (l.62) | no map v1 / parity licence | closed: 5ff00c9 line 8; still binds (P10) |
| NB5 (l.63) | feature source per owner; held-nowhere rule; C names; CC-219 for CC-214 | §A.2-A.7, §B, E-5, E-6; c1, c2 kept (accepted, CC-224 Ruling 9) |
| NB6 (l.64) | actual parent; commit governs DRAFT line | closed: 5ff00c9 line 5 |
| NB7 (l.65) | cap frozen at commit | closed (5ff00c9 line 6, 22 h); text aligned by E-7 |
| NB8 (l.66) | R4 selftest + SUMS before the owners run; sha frozen; R5 re-checks | closed: LOG l.1149 precedes l.1150; `ae4b6630` re-hashed equal; kept by §A.7 |
| NB9 (l.67) | 8/6-gram scan at commit | closed: 5ff00c9 line 11; the gatekeeper re-runs it on the R5 bytes [proposal] |
| NB10 (l.68) | optional re-admit order, only before registration | lapsed; under E-7 H runs anyway; no re-admit order added |
| NB11 (l.69) | model checks pin-time; owner list captured with shas | unchanged R1 (v3.1 l.191-193); `ae4b6630` + §A.4 |
| CC-217r2 Ruling 4 (l.44) / B3 (l.52) | no 4090 step before R5 + read + logged top-up + N18 | licence paragraph; P1-P3 |
| CC-217r2 Ruling 2 (l.42) | caches; recompute only on the custody host, never a rental | §A.2, §A.5, E-13 |
| CC-217r2 W4 (l.59) | R-items pinned before first use | P8-P9 |
| CC-217r2 W8 (l.63) | deferred owners fixed in R5 | §A.3 G4; #25-#41, c1, c2 |
| CC-217r2 Q-a / Ruling 6 | cap fixed before registration | PI-1102a 22 h; E-7 |
| CC-217r2 Q-b (l.82) | custody covers test-role features | PI-1102a B-Q3 YES; §A.1, E-13 |
| CC-217r2 Q-d (l.84) | Objects365 arrival | PI-1102a B-Q4; P4 |
| CC-217r2 top-up (l.85) | top-up logged | closed: PI-1102b (LOG l.1163), OPS-1102topup (LOG l.1164); P2 |
| CC-217 N15 (l.102) | instance id only, rate restated | E-10 |
| CC-217 N18 (l.105) | rescan before 4090 spend | §E |
| CC-218 N15 (l.80) | NB-C10 reciprocal sentence | E-8 |

### F.2 CC-224 (round 1)

| item | asked | where closed in v1.1 |
|---|---|---|
| W1 (l.65) | 92 survivors, ~4.5 images; fix #12, E1 row, 14.9 h, E-7 tail, Q6; EMPTY rule; outside-val2014 rule; withdraw 25-30% | §B.2 #12 with recount; E-7; E-12; E-14; §D.3; Q-EN |
| W2 (l.66) | remove the J-b reading; close by (a), (b) or (c); drop DOCCI | route (b) = 1b: E-12, §A.1, §A.6, §D.5; the 1a text is struck (CC-224r2 W3); DOCCI dropped (§A.6) |
| W3 (l.67) | G2 only with a cited spent line; #8, #11-#14 G3; per-block holds | §A.3, §A.4 spent-line column, summary, P6, §D.3, §D.4 |
| W4 (l.68) | freeze sentence | §A.3, E-15 |
| W5 (l.69) | verbatim E-12 replacing l.505-507 | E-12 |
| W6 (l.70) | M1 public-archive fetch erratum; cite l.285-286 | E-13; §A.5 |
| W7 (l.71) | K2 not valid until LOG-pinned | §A.2 K2 row, §A.4 #2-#3, P6; coordinator step (§I) |
| N1 (l.74) | A-T3 2014/2017 disclosure | §A.2, §A.5 |
| N2 (l.75) | 1a: read of C1/overlay/C2 + logged recount with positive control | struck with E-12 (ii); applies if 1a returns to the panel |
| N3 (l.76) | margin wording; project with actual survivors | E-7, §D.3 |
| N4 (l.77) | "full panel at irreversible 92 (CC-224)" | title, status, P1, §G |
| N5 (l.78) | P2 blocks launch, not adoption | P2 |
| N6 (l.79) | E-range | E-1..E-15 (§C heading) |
| N7 (l.80) | LOG l.982; PORTFOLIO l.171 stale | §A.4 #23, §B.2 #13 |
| N8 (l.81) | E-10 wording; host substitution rule | E-10, §D.4 item 6 |
| N9 (l.82) | G3 holds S and A1 until the M1 slot | P6, §D.3, §D.4, Q2 default |
| N10 (l.83) | J-c citation; J-f registered order | §B.2 #6, §D.3, §G |
| N11 (l.84) | N18 query additions | §E |
| N12 (l.85) | PASCAL-50S held or not at P6 | §A.4 #24, P6 |
| N13 (l.86) | Composite URL and version before any fetch (1a) | as N2 |
| N14 (l.87) | OPS line notes supersession | §I (coordinator step) |
| Q-tier (l.99) | irreversible 92 | answered by the ruling; carried to the PI as Q-tier |
| Q6 (J2, l.103) | restval yields ids to B? | Q-RV (§H) |

### F.3 CC-224r2 (round 2)

| item | asked | where closed in v1.2 |
|---|---|---|
| W1 (l.68) | l.501 total 18.8 (+25% = 23.5) in the E-12 list; delete "restated by E-7" | E-12 list; E-7 tail |
| W2 (l.69) | E-7 anchor l.511 "At the assumed rates" through l.516 "R5 restates the rate.)"; cite l.283-284 | E-7 |
| W3 (l.70) | strike E-12 (ii); "if Q-EN = 1a, R5 returns to the panel before any commit" | E-12, header, §D.6 |
| W4 (l.71) | l.27, l.422-426 in the E-12 list; English prompts not written or pinned at tier 1; catch-all | E-12 list, P9, §D.7 |
| W5 (l.72) | GO licenses the commit only after a logged PI line Q-EN = 1b, cited in the commit message; else the GO lapses | header (commit precondition), §H, §I |
| N1 | header route | header |
| N2 | P2 closed (l.1163); Q5 answered | P2, §H |
| N3 | E-14 from the start of the l.313 bullet | E-14 |
| N4 | E-15: no PA3 reversal or new PA3 | E-15, §A.3 |
| N5 | rental = any host other than M1 | §A.1, E-13 |
| N6 | M1 slot fails closed | §A.5 |
| N7 | licence line for recomputes, reversible 90 | header, §G J-j |
| N8 | idle M8 bill; M1 slot gated | §D.4 item 3, P6 |
| N9 | K6 cites LOG l.938 (a)(b) | §A.2 |
| N10 | §D.4 non-binding | §D.4 heading |
| N11 | tier-2 English set named early | §D.7 |
| N12 | N14 OPS line not yet logged | §I |
| N13 | gatekeeper 8/6-gram re-scan on the committed bytes | §I |

---

## G. Items for the review (round 3, last full panel at irreversible 92)

- **J-a** G2, limited to owners with a cited spent line (§A.3), is a new rule extending W8 and a timed departure from
  PORTFOLIO l.188 and v3.1 l.317-319 for those owners only.
- **J-b** Moot under route 1b (no COCO image staged; gate 1 not run); DOCCI is not in it. Under 1a, R5 returns to the
  panel (§D.6).
- **J-c** Accepted (CC-224 Ruling 9): c1, c2 kept as conditional owners (CC-217r3 NB5 l.63; PORTFOLIO l.167, l.170).
- **J-d** A-T3 2014/2017 pixel identity: disclosed; direct featuring of val2017 in the M1 slot proposed (§A.2).
- **J-e** Block-W env check and the laptop fallback (§D.2).
- **J-f** Closed: the registered run order is kept (CC-224 N10).
- **J-g** Accepted: overlay on `ae4b6630` (§A.7).
- **J-h** Answered: irreversible 92 (CC-224 Ruling 1).
- **J-i** Closed by E-12.
- **J-j** Feature recomputes (laptop CPU for XM3600, the KTVIC image and laptop-held gaps; the M1 slot under E-13) are
  not ids-only steps (CC-224r2 Ruling 9). v1.2 writes the licence line into the header for the panel to rule at
  reversible 90: after the R5 commit, each on P8 plus a logged start; the M1 slot also under Q2 and the MT4 hand-over.
  While they wait, S and A1 stay held (P6).
- **J-k** New in v1.2: the Flickr8K seal conflict of the tier-2 English candidates (§D.7) is for the tier-2 ledger
  ruling, not for R5.

---

## H. Questions for the PI (each with a recommendation and a default)

| # | question | recommended | default if no answer |
|---|---|---|---|
| Q5 | Top-up | **answered and logged**: PI-1102b (LOG l.1163) and OPS-1102topup (LOG l.1164, balance 1,194,532 VND at ~11:00 VN 02/11). Nothing more needed | — |
| Q-EN | Gate 1 leaves at most 92 val2014 ids, so Composite-COCO and Polaris-test-COCO have about 4-5 images each and give no English conclusion at tier 1. Route 1b (E1/E2 pre-fixed NOT RUN at tier 1 under E-12; the tier-2 prereg names an English human-rated set outside the COCO val2014 owners by a ledger ruling at ≥ 92, §D.7) or 1a (keep E1/E2)? | **1b** (all three judges, CC-224 l.100, CC-224r2 l.98). It costs H3 at tier 1 only (v3.1 l.89); the English comparison (PI-1026) moves to tier 2 | **no R5 commit** (CC-224r2 l.98, W5). A 1a answer sends R5 back to the panel; no default is applied silently |
| Q-tier | Accept R5 at irreversible 92, stricter than the one-judge read of CC-217r3 Q1? | YES | 92 |
| Q1 | AMBER ids-only read (image-name field of the public query file)? | NO (CC-224 l.101); moot under 1b | no read; E1/E2 handled under E-12 |
| Q2 | May B's CPU-only W25 slot on M1 (≤ 1.0 h wall, no GPU) use the gap after MT4 tier 2 ends, if MT4 tier 3 is not ready to launch then? | YES: it never delays MT4 | only after MT4 releases M1 fully (v3.1 l.269-270); until then B's S and A1 stay held by the G3 owners (P6) |
| Q3 | H-500 (PORTFOLIO l.172 "needs PI line"): is its owner B? | keep it listed as a B owner (G4, no list) | kept listed, owner unconfirmed |
| Q4 | M8 order (non-binding scheduling): E2b 1b-i first if ready before B, then B tier 1, then C tier 1 (or C on a new rental) | YES (§D.4) | ready first, B ahead on a tie, single tenant |
| Q-RV | Should B4 restval yield ids to B (CC-224 Q6, J2)? | NO (gate 2 would exclude them anyway); moot for staging under 1b | NO |

---

## I. Coordinator steps outside this file (not done by the drafter)

- Write the gatekeeper LOG pin line for K2 `feats_coco_test.npz` `2bc3b83e` (provenance `chain_feats.log` l.11-12,
  mirror `SHA256SUMS_feats` l.2) before its first use (W7).
- The next OPS line notes that CC-224 supersedes the OPS-1102b-r5-draft figures "~38" and "E-1..E-10" (CC-224 N14;
  still not logged, CC-224r2 N12).
- Record the PI's Q-EN answer in a PI line before the R5 commit. A GO licenses the commit only on a line reading
  Q-EN = 1b, time-stamped before the commit and cited in the commit message (CC-224r2 W5); otherwise the GO lapses.
- The gatekeeper re-runs the 8/6-gram scan on the committed R5 bytes before the commit (CC-224r2 N13; CC-217r3 NB9).
- The K2 LOG pin is still not written; it binds at P6 (CC-224r2 Ruling 2).
