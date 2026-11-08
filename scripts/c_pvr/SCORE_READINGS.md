# S16 scorer: readings of the registered docs and the CC-293 hunk map

Files:
- `scripts/c_pvr/c_pvr_score.py` (score), `c_pvr_cm.py` (cm), `c_pvr_cay.py` (cay), `c_pvr_score_mutants.py`.
- Line numbers refer to the round-3 files whose sha256 values are in `scripts/c_pvr/SHA256SUMS` (round-2 references
  remapped line by line; items 45-46 and §3 are new in round 3).

Every item is a place where the code had to read a registered doc, fill a gap or choose a form. An item not listed
here is not an approved reading (CC-293 W3). Each item names its source and its code lines. "CC-293" in the last
column gives the round-1 ruling where there is one; "new" marks a reading added in round 2.

## 1. Readings

| # | reading | source | code | CC-293 |
|---|---|---|---|---|
| 1 | `score --tier 1` lives in a third file, `c_pvr_score.py`, under the Q-SPLIT conditions (imports behind shas, no second constant value). The prereg §11 l.758 and T1-ANALYSIS §1 say `c_pvr.py score`; PINS-A §12 says `c_pvr_run.py score`. Both are pinned in the running host's H. | prereg §11; PINS-A §12; T1-ANALYSIS §1 | score l.13-19, l.49-56, l.85-100 | Ruling 5: accepted; the gatekeeper LOG line states the rename |
| 2 | File split: 'cây' rule = cay; C-M1 / C-M2 = cm; `score --tier 1` and the T1-REP descriptives = score (the descriptives are a section of score, l.714-794). | S11 §15 ("each committed after its own code read") | cay, cm, score | Ruling 6: one commit of the 4 files + SUMS |
| 3 | §6.3 (iii) with T1-GUARD G-1: the candidates are the variants that pass δ_C and δ_R (both strict `>`). One passes: that one. Both pass: PVR-drop if \|ΔP_obj^VI(drop − keep)\| < SESOI_P / 2, else the higher P_obj^VI. | prereg §6.3; T1-GUARD G-1, G-3 | score l.494-516 | traced, as registered |
| 4 | §12 order: the decision string is the first STOP in the order (ii) headroom, (iii) variant, (iv) go. (iii) and (iv) are still computed and printed after a headroom STOP. | prereg §12 | score l.518-522 | traced |
| 5 | Both PVR variants are computed every time (primary, Holm family, headline, ΔP by feature); `selected` marks the §6.3 one. Under a §6.3 STOP no family is the registered one. | prereg §5.2, §6.3 | score l.572-597, l.929-937 | traced |
| 6 | T1-REP §1 rule (ii) uses the §5.2 family with PVR = PVR-drop, whichever variant §6.3 selects (V = PVR-drop at tier 1). | T1-REP §1; PINS-A l.158-159 | score l.650-657, l.945 | Ruling 7: faithful |
| 7 | Doc conflict, stated: the registered HW-* sentences say "Verifying …" / "verification" whatever the T1-REP §1 naming rule gives. They are emitted verbatim. | T1-REP §1 vs §4 | score l.525-547 | open for round 2 |
| 8 | HW numbers are in points (×100), 2 decimals, "x [lo, hi]". (The round-1 `datastore` field is replaced by item 42.) | T1-REP §4 | score l.550-551 | – |
| 9 | T1-REP §1 labels are rebuilt from the two runs' masks: REJECTED = PVR-keep mask, UNCERTAIN = PVR-drop mask and not PVR-keep mask, else SUPPORTED. Each image is checked against both records' yes / no / maybe + parse_fail + cap_hits and the cap tail. One failing image switches the table to the N2 fallback (item 37). The check cannot see swaps that leave the counts equal (disclosed in the record, `SWAP`). | T1-REP §1; c_pvr_gpu OUT_KEYS | score l.246-259, l.695-697 | Ruling 7: allowed; N2 applied |
| 10 | A class carried by several propositions of one demonstration takes the first one's label. The count of such units whose propositions carry different labels is printed (`unit_label_conflicts`). | T1-REP §1 ("each class is counted once per demonstration caption") | score l.261-264, l.397-400 | Ruling 7: allowed; N9 applied |
| 11 | §1 statistics: precision of REJECTED for absent = REJ∧absent / REJ∧(absent ∪ present); recall = REJ∧absent / all absent units; SUPPORTED share = SUP∧present / all present units; κ on {REJ, SUP} × {absent, present}. Verifier shares are over calls + cap_hits; the parse-failure share is over calls. Parse failures exist as aggregate counts only. A8's "output-side labels" are its aggregate counts. | T1-REP §1 | score l.660-707 | – |
| 12 | The prereg §5.5 FAULT (> 1 % undefined replicates) applies to the registered numbers and decisions. The registered non-gating descriptives (the §1 table, the §6 strata, the type / feature rates, ΔP by feature) count their drops instead, and above 1 % carry the note "> 1 % undefined replicates, prereg §5.5; descriptive". The p-value divides by the kept replicates. | prereg §5.2, §5.5 | score l.283-298 (strict), l.589, l.593, l.668, l.712 (non-strict) | Ruling 7: allowed; N3 applied |
| 13 | §2 analytic pool-level null: ρ0 = φ0 = removed known-status units / (N_A + N_P), OR0 = 1, c′0 = c. | T1-REP §2 | score l.642 | – |
| 14 | A created unit (a class in a rebuilt text that was no unit of d) is counted, not a FAULT. It is not 0 when a demonstration failed decomposition (no props). The `out` count (proposition classes the scorer does not score on the original text) is 0 under the scorer of record. | T1-ANALYSIS §3 | score l.226-243 | – |
| 15 | 'cây' rule read literally: occurrences of the word in the raw NFC lower-cased string, so a 'cây' inside "xanh lá cây" is an occurrence that remains and the class is kept. Keys are matched as written (no norm_tone); a "word" is a letter; the boundary is the next non-\w character. K is recomputed from the lexicon. | T1-REP §5 rules 1-5 | cay l.27-57 | Ruling 7: faithful |
| 16 | The sensitivity scorer also acts on demonstration units: (d, cây) is no unit when every 'cây' of d is ignored, and survival uses the same scorer. "Mentions ignored" = captions whose 'cây' class the rule removes, per arm and set. | T1-REP §5 ("c, ρ, φ and OR under both scorers") | score l.196-213, l.336, l.774 | – |
| 17 | CHAIR_s^VI = share of all captions with at least one absent mention. R_obj^VI = ΣH⁺ / Σ verified-present pairs. | prereg §3.2 | score l.307-308 | – |
| 18 | Item 9 forms chosen and pinned here: the Vietnamese-letter set (no f, j, w, z) and the §5.7(b) letter set; tokens = NFC, lower case, every Unicode P* character removed, whitespace split; distinct-n corpus-level; repeated 3-gram per caption; truncation over records with a generation (A8's `finish = a8` excluded); empty = blank after strip. | T1-REP §6 item 9 ("the regex is pinned in the S10 scorer"); prereg §5.7(b) | score l.716-743 | – |
| 19 | Segmenter failure rate = the `decomp_fail` share of `CP.decompose_vi` on each VI arm's captions. `--no-segment` gives a NOT_COMPUTED reason; English sets say n/a. | T1-REP §6 item 9 | score l.775-778 | – |
| 20 | Item 15 features of an object proposition (union over its mentions): 'classifier' = a mention right after con / cái / chiếc / cây at a word boundary; 'tone' = norm_tone changes the mention; 'split' = item 32. The short error analysis of rewritten demonstrations is a manual step, not code. | T1-REP §6 item 15 | score l.422-450 | W2 applied (split added) |
| 21 | Per-image wall clock = (last − first utc stamp) / (n − 1), 1 s resolution. | T1-REP §6 item 8 | score l.745-748 | Ruling 7: allowed |
| 22 | §5.7(b) guard at tier 1: computed on XM3600-vi for the variant and A8. It labels the primary contrast (item 43) and passes INCONCLUSIVE on to C-M2; it does not change the §12 go / stop. | prereg §5.7(b); T1-ANALYSIS §5.4, §9.3 | score l.932-936 | Ruling 8 |
| 23 | DEGRADED is computed from the sha-checked a1_decomp files (M > N / 2 per set), not from the OPS line. | S11 v1.3 §10.3 | score l.169-181 | traced |
| 24 | A partial or absent arm is no result: it leaves every contrast and the Holm family (m shrinks) and is printed with its row count, separately from cut arms (item 38). An incomplete decision arm (A1, A8, A12, PVR-drop, PVR-keep) gives NOT_DECIDED. C-M1 / C-M2 give NOT_RUN (T1-ANALYSIS §9.2). | prereg §5.2; T1-ANALYSIS §9.2 | score l.848-864, l.581-586, l.908-910 | Ruling 7: allowed; N4 applied |
| 25 | T1-GUARD stratified bootstrap: one generator seeded 20261102, KTVIC explore drawn first, then OpenViIC explore. | T1-GUARD §2.1 | score l.797-809 | Ruling 7: allowed |
| 26 | G1 applies to κ⁻(A7−PVR) only; the κ⁺ ratios get G2 only. §9.2 NOT_RUN takes precedence over the §9.1 item 9 FAULT. | T1-ANALYSIS §4.3, §9.1, §9.2 | cm l.73-100, l.276-284 | Ruling 3: faithful |
| 27 | C-M1 / C-M2 run only when the §12 decisions are final. While the §6.3 variant is NOT_DECIDED (no CIDEr-VI input, item 45), or a decision arm is incomplete, both are NOT_RUN with their supplement lines and no sentence; C-M1 is not run on its own. The PVR-drop fallback applies only to a §6.3 STOP. | T1-ANALYSIS §1, §5.1 | score l.957-968; cm l.299 (CC-293r2 W4 d: NOT_DECIDED) | – |
| 28 | Doc conflict, stated: §9.4 says POST_HOC numbers are descriptive, while the §8 l.391 row prints "not computed". The code keeps the numbers without any label (item 36) and prints the supplement line "C-Mx not computed: POST_HOC §9.4: descriptive numbers in cm_tier1.json, no label, no sentence" (CC-293r2 N-F). POST_HOC = the appendix sha on disk is not 59b6eae5. | T1-ANALYSIS §8, §9.4 | score l.960; cm l.324-333 | Ruling 7: trigger allowed; W1 applied |
| 29 | C-M2 bounds and band are in points (×100). A DEGRADED or INCONCLUSIVE C-M2 sentence is kept with `usable_as_claim: false`. | T1-ANALYSIS §5.4 | cm l.165-180, l.317-320 | – |
| 30 | Base rate: the committed manifest targets as `gates.py` WANT_B holds them (4,453 / 8,276); no manifest is read. | T1-REP §7; prereg §3.3 l.311 | score l.55, l.98, l.898-900 | N6 applied |
| 31 | SigLIP similarity: optional `--emb SET=Q,D` through `c_pvr_manifest.emb`; without it the record says NOT_COMPUTED. The npz files are not pinned anywhere. | T1-REP §4 | score l.783-795, l.884-886 | N5 applied |
| 32 | 'split' (item 15, "compounds the rule-based segmenter splits") = a multi-syllable mention that covers more than one RDRSegmenter word. Tokens come from decompose_vi's RDR / align path without its clean() step (`CP.rdr` on the '_'-free text, `CP.align`, `CP.cover`; CC-293r2 N-C) for the demonstrations A1 retrieves and the XM3600-vi captions of PVR-drop, PVR-keep and A8. A text that cannot be segmented or aligned decides no 'split' and is counted; a segmenter pin mismatch aborts. | T1-REP §6 item 15; PINS-A §4.2 | score l.428-441, l.470-491, l.888-895 | new (W2) |
| 33 | ΔP_obj^VI by feature = P_obj^VI(v) − P_obj^VI(A8) over the caption mentions that carry the feature, for both variants; a class counts in a feature stratum if any of its occurrences in the caption has the feature. A caption whose mentions `CP.vi_mentions` cannot locate adds no class and is counted. Descriptive, non-strict. The tone test reads the lower-cased caption, not its '_'-free form (CC-293r2 N-C); the S16 dev report discloses both N-C points beside the 'split' / 'tone' counts. | T1-REP §6 item 15 | score l.340-345, l.452-467, l.593-594, l.602 | new (W2) |
| 34 | ΔP_obj^VI by proposition type: 'obj' = the primary contrast (every mapped caption mention is an object mention); 'text' = NOT_COMPUTED, with the reason quoted from prereg §3.1 and T1-REP §1. | prereg §3.1; T1-REP §1, §6 item 15 | score l.595-597, l.605-608 | new (W2) |
| 35 | T1-GUARD §2.1 per-set ΔCIDEr-VI(v − A1) for each explore half, with a CI from the same stratified replicates (the stratum's replicate sum / its n). Descriptive. | T1-GUARD §2.1 | score l.804-809 | new (W2) |
| 36 | POST_HOC record: the numbers stay; every label, verdict and case field at every depth goes (IDENTIFIED, NOT_IDENTIFIED, E1_*, OVERID_*, SIGN_*, PLACEBO_*, case). Gate names (G1 / G2) and `kappa: null` stay, since they are inputs, not labels. No main-text sentence. The record's reason reads "§9.4: descriptive numbers in cm_tier1.json, no label, no sentence" (CC-293r2 N-F). | T1-ANALYSIS §9.4 | cm l.254-266, l.324-328 | new (W1) |
| 37 | §1 table fallback (fixed before data): when any image fails the count check, the record prints the reconstructed cells labelled "not valid" and, from each run read alone, the exact precision and recall of REJECTED for absent (PVR-keep) and the SUPPORTED share on present (PVR-drop). κ is NOT_COMPUTABLE. | CC-293 N2 | score l.397-403, l.660-678 | new (N2) |
| 38 | JOB DONE = the pulled SUMS file is named `SHA256SUMS_tier1`: then a non-cut absent or partial arm is a FAULT. Partial arms are allowed only under `SHA256SUMS_tier1_cap` or a STOP pull. | S11 v1.3 §13; CC-293 N4 | score l.862-864 | new (N4) |
| 39 | `--rerun-of OPS-…`: the stamp "re-run after FAULT <OPS id>, code <sha of c_pvr_score.py>" goes into both records' top-level label and into each main-text sentence's label. | T1-ANALYSIS §9.1; CC-293 N10 | score l.877-881, l.949-953, l.1490 | new (N10) |
| 40 | No silent drop-out: every registered item that cannot run prints a NOT_COMPUTED reason (A1 − A0, the headline, the mention strata, the segmenter rate, 'split', the by-type rates, the §2 identity, the similarity). `--cider` (when given, item 45) must cover xm3600_vi A0, A1, PVR-drop and PVR-keep, and both explore halves' A1, PVR-drop and PVR-keep. | CC-293 N5 | score l.589-592, l.775-778, l.812-823, l.921-944 | new (N5) |
| 45 | The no-CIDEr path. Exactly one of `--cider` (with `--cider-sha`) or `--no-cider REASON` is given; neither, both, or `--cider` without its sha is a FAULT. `--no-cider` is a FAULT under a JOB DONE pull (`SHA256SUMS_tier1`), where S16 waits for the CIDEr-VI pin. Under `--no-cider` every CIDEr-free number is computed as before (P_obj^VI, the primary contrast, the Holm family, SESOI_P, headroom, δ_R, T1-REP §1-§7); variant = None, variant_status = "NOT_DECIDED: no CIDEr-VI input (<reason>)", go_rule = None; decision = the headroom STOP if (ii) fires, else "NOT_DECIDED (§6.3 variant: no CIDEr-VI input)"; guard_G1, the XM3600-vi ΔCIDEr-VI and A1 − A0 CIDEr-VI print NOT_COMPUTED with the reason; the reason is in `inputs.cider`. | CC-293r2 W4, Ruling 12; prereg §12 order; S11 v1.3 §13 | score l.494-522, l.597-598, l.834-837, l.875-876, l.914, l.924, l.962, l.1485-1487 | new (W4) |
| 46 | `--cider` values must be int or float (not bool), finite, and in [0, 1000] (CIDEr-D ×100); anything else is a FAULT. | CC-293r2 N-H | score l.824-825 | new (N-H) |
| 41 | `c_pvr_cm.SEED` must equal `c_pvr.BOOT_SEEDS[0]` (20261102), checked at load. | prereg §5.5; Q-SPLIT (i) | score l.99-100 | new (N6) |
| 42 | HW-3 names the datastore inside the sentence, in HW-2's form: "With this datastore (KTVIC and OpenViIC training captions), verifying retrieved demonstrations before use raised …". Wording fixed before data. | T1-REP §4 ("with the datastore named in the claim sentence") | score l.541-543 | new (N7) |
| 43 | §5.7(b) labels at tier 1: "VI-guard FAIL (§5.7 b, PVR)" and "VI-guard INCONCLUSIVE (§5.7 b, A8)". | prereg §5.7(b); CC-293 Ruling 8 | score l.933-934 | new (N8) |
| 44 | A FAULT stops the whole run, C-M2 too. Accepted because the only T1-REP §2 FAULT (the c′ identity) is exact on integers and cannot fire; the others are integrity FAULTs that void every number. | CC-293 Ruling 9 | score l.25-28 | new (N12) |

## 2. Hunk map, round 1 → round 2 (CC-293)

Round-1 shas: cay 129ae59d, cm fc594fff, score ab6b9ede, mutants 74575707, SUMS 3ffd4da1. cay is unchanged.

| CC-293 item | change | where |
|---|---|---|
| W1 | `scrub()` drops every label, verdict and case field of a POST_HOC record at every depth. `analyse()` computes first, then scrubs and drops the sentences. Selftests: the serialized cm record has no label string (cm); the written `cm_tier1.json` of a POST_HOC world has none (score). | cm l.254-266, l.324-333, l.544-559; score l.1431-1442 |
| W2 (a) | 'split' feature on demonstrations and captions from RDRSegmenter tokens (items 32-33). | score l.340-345, l.404-409, l.422-491, l.888-895 |
| W2 (b) | ΔP_obj^VI by feature (item 33); by type: obj = primary, text = NOT_COMPUTED with the quoted reason (item 34). | score l.593-608 |
| W2 (c) | Per-set ΔCIDEr-VI CIs from the stratified replicates (item 35). | score l.804-809 |
| W3 | this file | `scripts/c_pvr/SCORE_READINGS.md` |
| N1 | Kill cases: `holds0` closed at 0; an OR CI wholly above 1 gives no G1; the strata zero clause; δ_C on the CI lower bound (point > −2, lower < −2); created vs units (a 'cây' freed by a deletion). The five hand mutants are in the runner: `g2_holds0_open`, `g1_wholly_below`, `g_guard_point`, `g2_strata_no_zero`, `h_created_vs_carried`. | cm l.405-409, l.511-522; score l.1050-1052, l.1194-1197; mutants l.66-74 |
| N2 | §1 fallback, per-run statistics (item 37); the swap disclosure. | score l.397-403, l.660-678, l.695-697 |
| N3 | Note on non-strict estimates above 1 % undefined (item 12). | score l.294-295 |
| N4 | Holm record lists cut / partial / absent separately; JOB DONE FAULT (item 38). | score l.581-586, l.862-864 |
| N5 | `--cider` must hold xm3600_vi A0; NOT_COMPUTED reasons (item 40). | score l.817-818, l.884-886, l.921-943 |
| N6 | Seed assert; base rate from `gates.py` WANT_B (pinned 3bced05e). | score l.55, l.97-100, l.898-900 |
| N7 | HW-3 wording (item 42). | score l.541-543 |
| N8 | §5.7(b) wording (item 43). | score l.933-934 |
| N9 | `unit_label_conflicts` count (item 10). | score l.397-400, l.666 |
| N10 | `--rerun-of` stamp (item 39). | score l.877-881, l.949-953, l.1490 |
| N11 | Docstring status line. | score l.2-3 |
| N12 | Docstring note on the global abort (item 44). | score l.25-28 |
| Ruling 5 (G-2) | Docstring states the command rename. | score l.17-19 |
| Ruling 6 (G-3) | cm changed, so the CODE dict pin of cm in score and the SUMS lines are updated in the same diff. | score l.54; SHA256SUMS |

## 3. Hunk map, round 2 → round 3 (CC-293r2)

Round-2 shas: cm 623ec5c1, score 1e15ce7a, mutants 80ed1657, SUMS e73094ba, SCORE_READINGS 3a80668d. cay is unchanged.

| CC-293r2 item | change | where |
|---|---|---|
| W4 (a), (b) | `--cider` / `--cider-sha` optional, `--no-cider REASON` added; exactly one, with the sha; `--no-cider` refused under `SHA256SUMS_tier1`; the reason in `inputs.cider`. | score l.834-837, l.875-876, l.1485-1487 |
| W4 (c) | decide(): NOT_DECIDED replaces PENDING, headroom STOP first; NOT_COMPUTED reasons for guard_G1, ΔCIDEr-VI and A1 − A0 CIDEr-VI. | score l.494-522, l.597-598, l.914, l.924 |
| W4 (d) | cm_stage treats NOT_DECIDED as not final: C-M1 / C-M2 NOT_RUN. | score l.962 |
| W4 (e) | Selftests: the no-CIDEr decide cases; w2 (no CIDEr, headroom STOP first, reason recorded); w6 (cap-stop pull, no CIDEr, no headroom STOP: registered numbers present, NOT_DECIDED, C-M1 / C-M2 NOT_RUN); FAULT worlds for `--no-cider` under JOB DONE, neither flag, both flags, `--cider` without sha. Runner mutants `w4_*`. | score l.1124-1127, l.1337-1339, l.1362-1372, l.1403-1411, l.1443-1454; mutants l.146-160 |
| W4 (f) | Items 45-46 and this section; SUMS lines for cm, score and mutants. | SCORE_READINGS.md; SHA256SUMS |
| N-A | Both POST_HOC selftests use an independent literal oracle (`IDENTIFIED\|E1_\|OVERID_\|SIGN_\|PLACEBO_\|"K[1-5]"\|INCONCLUSIVE\|DEGRADED`), not CM.LABELS; the cm case also sets degraded. Runner mutants `w1_labels_no_placebo`, `w1_labels_no_sign`. | cm l.544-547; score l.1441-1442; mutants l.167-168; equivalent `w1_labels_no_sign` with its proof, mutants l.184-189 |
| N-B | Kill cases for the seven survivors: FC columns and PF on one synthetic image (`_st_fc`); split counters all 0 in w1; one unit-label conflict in w1; the N3 note; seg_toks re-raises a pin FAULT, falls back text by text, and gives None on an unaligned text. Runner mutants `w2_*`, `n3_note_never`, `seg_swallow_pin_both` (two replacements), `seg_no_text_fallback`. | score l.1068-1098, l.1163-1164, l.1218-1219, l.1300-1302; mutants l.170-181 |
| N-C | seg_toks docstring wording; items 32-33. | score l.471-473 |
| N-F | POST_HOC reason wording; its selftest. | cm l.328-329, l.556; mutants l.169 |
| N-G | Docstring status line. | score l.2-3 |
| N-H | cider_in value check (item 46); FAULT worlds for NaN, 1000.5, −0.1 and a bool. Runner mutants `nh_*`. | score l.824-825, l.1374-1380; mutants l.161-165 |
| N-D, N-E | Not code: N-D goes to the tier-3 prereg; N-E is an S16 OPS-line step (the sha256 of every `--emb` npz, or a line that no `--emb` was given). | – |
| CODE pin | cm changed, so its pin in score and the SUMS lines changed in the same diff. | score l.54; SHA256SUMS |
