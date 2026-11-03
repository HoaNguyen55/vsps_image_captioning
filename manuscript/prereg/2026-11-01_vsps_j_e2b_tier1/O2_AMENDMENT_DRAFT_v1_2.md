# VSPS-J E2b O2 AMENDMENT (draft v1.2): what follows the failed O1 screen

**Status.** DRAFT v1.2, written 2026-11-03T12:47:34Z (`date -u`). v1 = `O2_AMENDMENT_DRAFT.md` e97760a4 (drafting started
2026-11-03T11:52:48Z) and v1.1 = `O2_AMENDMENT_DRAFT_v1_1.md` 2b704b13 both stay byte-equal. v1.1 = v1 plus F1-F4
(§15). v1.2 = v1.1 plus CC-244 round 1 (NEXT_ROUND, median 88): BLOCKING B1, B2(i), B2(ii), C1 and NON-BLOCKING
N1-N15, mapped in §16. Nothing in this file has been committed, run,
rented or decoded.
**Tier.** IRREVERSIBLE, bar >= 92. Full 3-judge panel plus a read-only Codex pass, capped at 3 rounds. Round 1 = CC-244 (NEXT_ROUND 88);
this v1.2 goes to round 2/3 as a full panel with Codex (CC-244 Ruling 11). The sources for
this tier are CC-233 (TIER line and Ruling 3e), CC-233r2 (TIER line), CC-241r2 (Ruling 6d) and PI-1103c (LOG l.1302):
"O2 … needs its own irreversible 92 ruling".
**Label.** Every output carries `O2 / VSPS-J E2b PATH DECISION`. Every estimate in this file is AI opinion.
**PI default (03/11).** Draft O2 and take it to the panel.

**Sources** (sha256 prefixes recomputed 2026-11-03 ~11:53Z):

| key | file | sha256 prefix |
|---|---|---|
| `P` | `PREREG_DRAFT.md` | 6bf702a9 (commit 26ae375) |
| `A1` | `AMENDMENT_1_DRAFT_v1_2.md` | 55aead20 (commit 348b088); v1.1 030dcfb3 also read |
| `O1` | `TIER1C_O1_AMENDMENT_DRAFT.md` | 1895dad7 (commit 8511fe6) |
| `T2` | `TIER2_AMENDMENT_DRAFT_v1_1.md` | 6ebfc798 (untracked) |
| `V2` | `manuscript/directions/VSPS_J_E2B_DIRECTION_v2_2026-11-01.md` | 8967fbc0 |
| `BV3` | `manuscript/directions/B_DIRECTION_v3_2026-11-01.md` | ef1e3cc5 |
| `CV3` | `manuscript/directions/C_DIRECTION_v3_2026-11-01.md` | 99dbe46b |
| `UP` | `manuscript/UPGRADE_PLAN_2026-10-27.md` | 0851abe3 |
| `RES` | `.session_backup/2026-11-02/e2b_score/res.json` | 9b9c3f6e |
| `R1C` | `.session_backup/2026-11-03/vj_o1/res_1c.json` | e58904ff; guard `SCORED_1C.json` 7cb88360 |
| CC files | CC-233 f496a212, CC-233r2 ea0d0245, CC-241 b69af346, CC-241r2 d28f4786 | |
| `LOG` | `.session_backup/2026-10-13/decisions/LOG.md` | |

**What was read for this draft.** Only the `screen`, `rule`, `decision`, `fit`, `infeasible_reasons` and
`tier1_winner_record` fields of R1C were opened. The `select`, `predictive_descriptive` and `held_report_only` blocks
were not opened (the CC-244 judges opened the same fields only, N15). The following were never opened: any `probes.jsonl` contents, `val_raw.json`, any test-set file, and
any AMBER, VALSE or e-SNLI-VE file.

## 0. Summary

1. **E2b has no path left to its registered claim (H1-H4).**
   - Q-T2-0 closed the frozen tier-1 winner (CC-233 Ruling 2).
   - The one post-hoc O1 screen came out SCREEN NO-GO: P̂ = 0.248 < 0.98 (LOG l.1416).
   - O1-C6 forbids any second cushion, grid or comparator variant.
2. **O2 as registered** means no tier 2, plus one of two paper paths: a PA4 measurement paper on dev results only, or a
   PA1 Pareto report. PA1 needs a new registered criterion before any test claim (CC-233 Ruling 3e; T2 A.6 row 2).
3. **PA1 is blocked today.** No config is eligible, a criterion registered now would be post hoc, NB-C8 is unmet, and
   AMBER is proposed for L2-P2, pending a PI line (PORTFOLIO l.69, l.174).
4. **PA4 spends 0 test looks and 0 GPU-h, but not 0 reads (N2):** its tables would be the first opening of R1C's
   `select`, `predictive_descriptive` and `held_report_only` blocks. By the Q2 row of `UP` §7 (l.97), a dev-only paper
   cannot reach JVCIR's tier. PI-1029m (LOG l.756) reads "papers must aim at PASS results; failures mentioned only as
   context once a PASS is found"; "no PASS, no paper" is the coordinator's adopted reading of it, not the PI's words.
5. **Recommended: option (a).** Stop VSPS-J tier 2 here and park the VSPS-J paper. All E2b tier-2 and tier-3 candidate
   sets stay unread. The E2b dev record (tier 1, the pre-check and O1) is kept and reported briefly wherever it is used.
   No direction is adopted.
6. **(a) is a recommendation to the PI, not a fallback (B1).** Nothing takes effect if the panel misses 92. Until a 92
   GO or a direct PI line, VSPS-J stays as Q-T2-0 and O1-C6 left it: no tier 2, nothing adopted, nothing spent, no
   automatic step. Once a GO exists, (a) is also the PI's default for Q-O2-1 (§13).

## 1. What O2 is, as registered, and where its licence comes from

**No trigger in P or V2 fired (N1).** O2 does not come from a tier-1 rule or a V2 fallback firing on its own terms:
- `P` l.228 sends the path to "PA1 (Pareto report) / PA4 (measurement paper) per v2 section 6" only "**If nothing is
  feasible**". A config was feasible: `internvl3_8b|FA` won (LOG l.1243).
- `V2` §6 l.403 makes PA1 the fallback "**nếu H1 trượt**" (if H1 fails). H1's point and CI criteria were met descriptively on
  the selection-biased select half (Δprec +7.77 [5.40, 10.13]) (N4). The conjunct that the CC-233 post-hoc plug-in
  projection judged out of reach is H4 (recall drift); H4 never ran as a registered test.
- **O2 entry itself was registered post hoc, before the read (N1).** The TIER1C §6 amendment (`O1` l.180-182,
  committed 8511fe6, OPS-1103vj-1c-commit 08:31:54Z) wrote "→ O2 automatically" before the 11:28:55Z screen launch
  (LOG l.1415). That amendment was itself drafted after the tier-1 select result was seen.

**The licence for O2 is a chain of later rulings:**
- **CC-233 Ruling 3e, rank 2:** "O2 PA4 measurement paper (or PA1, which needs a new registered criterion before any
  test claim). This is a main-direction change, irreversible 92 when adopted."
- **CC-233 For the PI:** "(O2) stop E2b at tier 1 and plan VSPS-J as a measurement paper (PA4), dev results only.
  Adopting it as VSPS-J's direction needs a >= 92 ruling."
- **`T2` A.6 row 2:** "O2. No tier 2; PA4 measurement paper (or PA1 Pareto, which needs a new registered criterion
  before any test claim) | Main-direction change | its own irreversible >= 92 ruling | … | Automatic if O1 fails
  (PI-1103c)".
- **`O1` §6 (O1-C6):** "SCREEN NO-GO, INFEASIBLE, or no GO on this amendment within 2 judge rounds → O2 automatically
  (PI-1103c). O2's adoption as the VSPS-J path still needs its own irreversible ≥ 92 ruling. No second cushion, grid or
  comparator variant, ever."
- **PI-1103c (LOG l.1302):** "fails -> O2 (needs its own irreversible 92 ruling)".

**The two paper paths O2 names** (`V2` §6 l.403-407):
- **PA1:** "Báo cặp trên test: recall chặt và độ chính xác REJECTED của E2b so với Vintern ở cùng điểm khớp. Luật đăng
  ký trước tầng 3; không thay primary." In English: report, on test, E2b's strict recall and REJECTED precision against
  Vintern's at the same matched point. The rule is registered before tier 3 and does not replace the primary.
- **PA4 (the floor):** "Bài đo lường: bộ kiểm chứng 3 nhãn theo loại, VI/EN, với phân tích lỗi theo loại." In English:
  a measurement paper on the typed 3-label verifier, VI and EN, with a per-type error analysis.

**What "automatic" means here.** It means only that the path is now O2 rather than a tier 2. It does not adopt PA4 or
PA1. This file asks the panel which state VSPS-J enters (§12).

## 2. Where E2b stands (dev results only; all already spent)

| step | result | source |
|---|---|---|
| Tier 1 (registered rule, select half, 338 images; selection-biased) | Winner `internvl3_8b|FA` (vi frame): Δprec +7.77 [5.40, 10.13]; U 3.08 [2.33, 3.93]; Δret +15.22 [12.44, 17.88]; Δrecall −2.79 [−5.66, +0.24] | LOG l.1243; R1C `tier1_winner_record` (equal) |
| Other cells (Δprec point) | qwen3vl FA +5.03; qwen25vl FA +0.70; qwen3vl FB +1.71 (Δret −8.53) | LOG l.1243 |
| EN arm (descriptive, comparison only) | object prec_R 49.5 vs Vintern 42.5; retention 65.0 vs 47.0; recall 83.4 vs 87.1 | LOG l.1253 |
| Pre-check, Q-T2-0 | Post-hoc plug-in projection from the select half, made after the result was seen: H4 is out of reach. Plug-in P(H4) = 0.0021 at n = 1,004; predictive ≤ ~0.15 for H4 alone. Result: no tier-2 decode of the frozen winner | CC-233 Rulings 1-2 |
| O1 tier-1c screen (post hoc, one shot) | SCREEN NO-GO. P̂ = 0.248, MC SE 0.019, n_pass 124 / B_out 500, 0 undefined, 0 inner faults; gate 0.98 | R1C `decision`; LOG l.1416 |
| O1 fit (tune half, primary types) | **object:** n_f 724, k_V 613, k* 628, kE 647, so the realised tune cushion was +4.70 points (34/724), above the +2.0 target because of the 0.05 grid. **number:** n_f 612, k_V 518, k* = kE = 531, an exact hit (+2.12 points). Both feasible; `infeasible_reasons` empty | R1C `fit` |
| O1 fit (descriptive type) | attribute: Vintern band has no feasible t_lo, so the registered (0.5, 0.5) fallback applies. It never entered the decision | R1C `fit` |

**How to read P̂ = 0.248.** It is a lenient plug-in estimate of P(PASS of H1-H4 at n = 1,004). It resamples from the
338 select images and ignores their own sampling variance (`O1` §4). It is **not** the probability that "the screen
passes", so it is not comparable with the judges' ~10 % prior for that event (CC-233 Ruling 3c). The decision was
binary: below 0.98, NO-GO.

## 3. What O2 registers

O2 has two parts. The panel rules on each one.

**O2-(i): closure record (part of every option except (e) and (f) in §12).**
- **Closed:** the E2b registered claim form `P` l.33-37 and H1-H4 (`P` §5) for both `internvl3_8b|FA` (Q-T2-0) and
  `internvl3_8b|FA|1c` (O1 NO-GO). Neither gets a tier-2 or tier-3 look without a new direction, a new prereg and its
  own >= 92 ruling (F1). Q-T2-0 stays what CC-233 Ruling 2 ruled it: REVERSIBLE, a status quo. So option (a) stays
  reversible.
- **O1-C6 survives F1 (N3).** Its ban on any second cushion, grid or comparator variant for `|1c` ("ever", `O1`
  l.182) stands. Any revival is a NEW config, confirmed on fresh dev-confirm data. The M-HalDetect val select half
  and the held 107 count as explored and never serve as confirmation.
- **Not reopened by:** a new cushion, grid, comparator, type subset (O5), a re-opened Q-recall (O6), or an EN-only tier 3
  (O4).
- **What reviving VSPS-J would take:** a new direction document, a new prereg, and its own >= 92 ruling. It may re-use
  the E2b dev record only as dev-explore evidence.
- **Already binding.** This records a state that Q-T2-0, O1-C6 and the O1 NO-GO already impose. It adds no new
  restriction.

**O2-(ii): the paper path for VSPS-J. Exactly one of these:**
- **PARK.** No paper path is adopted. The E2b dev record is sealed as is (§5) and used only as in §7. This is option (a).
- **PA4.** A dev-only measurement paper on the typed 3-label verifier (vi primary, EN comparison), with the scope and
  gates of §4. This is option (b), or (c) at a venue one tier lower.
- **PA1.** Not registrable now (§4.3). It is listed so the panel can close it explicitly. This is option (d).

## 4. Decision rules (with numbers)

### 4.1 This file

- **GO on an option:**
  - the full 3-judge panel median is >= 92;
  - BLOCKING open = 0;
  - anchors pass (numbers against the sha-pinned files above; citations by line);
  - Codex (read-only) raises no new BLOCKING.
- **Round cap:** 3 (round 1 = CC-244). After round 3 without GO: **ESCALATE_TO_PI** with the open list. Meanwhile
  VSPS-J stays as Q-T2-0 and O1-C6 left it (no tier 2); nothing is adopted or spent; no automatic step (B1).
- **Option (a)** adopts no direction and spends nothing. It is reversible in substance. It is ruled here at 92 because it is
  the O2 decision that PI-1103c sent to a 92 ruling, closes the registered H1-H4 record and sets the brief-result
  wording (CC-244 TIER). It is a recommendation to the PI (§0 item 6, Q-O2-1), not a fallback.
- **After a GO on (a):** the next STATE file marks VSPS-J PARKED (STATE_2026-11-03 l.22 still lists JVCIR) (N12).
  Not before.

### 4.2 The PA4 gates (bind only if option (b) or (c) is chosen)

- **W-1, scope.**
  - PA4 uses only the aggregates already in RES (9b9c3f6e), `res_en.json` (f1fea816) and R1C (e58904ff), plus the
    earlier VSPS-J rows these cite (M0 f77eea1, E1b ed65b74, E1a 5d6db4c).
  - **No new read:**
    - no `probes.jsonl` contents;
    - no `val_raw.json`;
    - no re-read of held-107 probe rows; the R1C `held_report_only` aggregate is the only held source (N2);
    - no M-HalDetect text;
    - no new decode.
  - **First opening (N2).** PA4's tables would be the first opening of R1C's `select`, `predictive_descriptive` and
    `held_report_only` blocks (aggregates already computed; no new data read). That opening is allowed only under a
    92 GO on (b) or (c).
  - **Error analysis by type** uses only the human M-HalDetect labels and the registered keyword type rule (`P` §2.3),
    through the count tables already in those files.
  - **Not allowed:**
    - manual error categories (they would be new labels);
    - LLM error tags (AI labels are not evidence).
- **W-2, writing gate.** Writing starts only when a judge reads a comparison table at GO >= 90 (reversible). The table
  sets PA4 against the cited prior art of `P` §1 (POPE 2305.10355, AMBER (2311.07397, 2023), AMBER-MUL (Qu et al. 2024,
  2408.00550), FaithScore
  2311.01477, Whitehead et al. 2204.13631). It must show novelty, newness and rigour each >= the cited papers (PI 10-31
  writing gate).
- **W-3, tier gate.** A judge scorecard (CC-126, 6 × 0-5) must reach the target venue's row of `UP` §7:
  - for JVCIR (Q2): >= 20/30, every criterion >= 2, novelty >= 3, and a headline that is a registered PASS or
    leave-one-system-out stable and not post hoc, artefacts >= 2, writing >= 3;
  - for a Q3 venue: >= 16/30, every criterion >= 2, novelty >= 2, at least one registered result (PASS or an
    informative FAIL) as the paper's axis, writing >= 3.
- **W-4, order.** PA4 never takes a writer slot, an agent or a laptop window from a ready A, B or C step (standing goal;
  `A1` header). The gate check runs once, at the first writer slot that A, B and C do not need. "Do work early" applies
  only after A, B and C.
- **Failure route:** if W-2 or W-3 fails, VSPS-J moves to option (a) automatically (reversible). There is no retry with
  re-scoped claims.

### 4.3 Why PA1 cannot be registered now

- **No eligible config.** The frozen winner is closed (Q-T2-0) and `|1c` failed its screen. PA1 "at the frozen
  operating point" (`V2` l.403) therefore has no config that may go to tier 2 under the three-tier rule (a failed or
  pre-failed rehearsal never touches test).
- **A criterion written now would be post hoc.** Any Pareto criterion registered now is fixed after the select-half
  recall gap and the O1 P̂ were seen. That is the same defect that puts O6 against (CC-233 Ruling 3e).
- **NB-C8 is unmet** (`P` l.271-272; `A1` B.3). There is no VALSE ledger line, and CC-207 Q2 is still NOT YET. Tier 3
  has no candidate.
- **AMBER is proposed for L2-P2, pending a PI line** (F2). PORTFOLIO l.69 and l.174 list AMBER generative (1,004 images)
  as fallback-only under CC-147 r4, proposed for L2-P2, and say it needs a new PI line. An AMBER tier 3 for
  VSPS-J would draw on those same images [the AMBER image set; not re-checked here], so it needs a ledger ruling first.
  VALSE needs an id fetch under its own >= 92 ruling (CC-218).
- **Cost if PA1 were ever licensed:**
  - T2-K arm: 11.81 GPU-h est. (cap 17.5), about 277k VND, or about 376k VND at the cap, setup included (CC-233r2;
    `T2` B.7);
  - plus a tier-3 decode that has not been estimated.

## 5. What is spent and what stays unspent

**Spent before O2 (dev only; recorded; O2 changes none of it):**

| set | how it was used | reads |
|---|---|---|
| M-HalDetect val probe split: 769 images / 16,027 segments (after W25; 17 images reserved for another study were excluded before probing) | tier 1b-i, all 4 cells, vi | scored once (LOG l.1243) |
| Tune half: 324 images | thresholds | tier 1, and `|1c` (O1) |
| Select half: 338 images | config choice, then the O1 screen | **two reads**: tier-1 score, O1 screen |
| Held: 107 images after W25 (the prereg's 106 was before W25; selection 662 vs 663) | report-only, never in a choice | **two reads, report-only**: the tier-1 E2b column, then the O1 tables. **Not fresh.** |
| Winner, EN frame, 769 images | descriptive | score-en once (LOG l.1253) |
| Karpathy-test images inside M-HalDetect val: 91 | dev only, held out of every choice | spent (PORTFOLIO l.192) |
| Rate run: 171 images / 200 spans | timing only, unscored | — |

**Spent by O2:**
- 0 test-set looks (E2b has never had a test look; under O2-(i) H1-H4 get none without a new direction, a new prereg
  and its own >= 92 ruling);
- 0 GPU-h;
- 0 decodes, 0 new labels;
- 0 new reads under (a) and (e); under (b)/(c), the first opening of three R1C blocks (N2);
- laptop CPU 0 runs for options (a), (d) and (e).

**Stays unread and unspent** (O2 opens none of these; any later use needs its own ledger ruling):
- **M-HalDetect train:** T2-S pool 2,176 of 2,695. Never decoded by E2b (M0-touched ids only).
- **Karpathy test:** T2-K 4,198. VSPS-J reads nothing. C's KT-C 3,907 part stays as C's ledger records it.
- **AMBER:** `annotations.json` never fetched; the query-file copy was deleted (OPS-1101amber-del, LOG l.1118); the
  images are proposed for L2-P2, pending a PI line (F2).
- **VALSE:** no fetch.
- **e-SNLI-VE:** dev and test.
- **Owned by other papers:**
  - KV-4,224 (MT4);
  - Objects365 v2 val (B);
  - A-T3's 593 val2017 ids (sealed, A).
- **Custody only, not re-read:** UIT-ViIC test 231 (E1a records; spent dev, M1/laptop custody, `P` §3.3).

**Not reassigned.** O2 frees no set to another owner. Reassignment goes through the PORTFOLIO §2.3 ledger, under its
own ruling.

## 6. Kill criteria

Every threshold here is a proposal, fixed before any O2 step.

| # | trigger | effect |
|---|---|---|
| K-1 | Any step under O2 needs a decode, a GPU, a rental, or a read of a tier-2, tier-3 or test file | Not O2: stop. It needs a new amendment and its own >= 92 ruling |
| K-2 | (PA4) W-2 writing gate is not GO >= 90 | Option (a), automatically |
| K-3 | (PA4) the W-3 scorecard is below the target venue's row of `UP` §7 at its one check | Option (a), automatically |
| K-4 | (PA4) the judges' novelty doubt reaches >= 80 % (pivot rule, PI 10-27) | Option (a) |
| K-5 | (PA4) a judge finds a salami conflict with A, B or C (§8) | The item leaves VSPS-J; A, B and C are never changed for VSPS-J |
| K-6 | Any draft text hides the tier-1 numbers, the Q-T2-0 pre-check or the O1 NO-GO, or calls a dev gain confirmed | BLOCKING at that text's read |
| K-7 | PA4 would take a slot from a ready A, B or C step (W-4) | PA4 pauses |
| K-8 | The PI says stop | Option (a) |

## 7. How the O1 failure (and the tier-1 record) is reported

**The rule.** These results are reported briefly, as dev results, and are never hidden or dressed as evidence
(papers-aim-for-pass, PI-1029m).

**Where.**
- **Option (a):** in the sealed E2b dev record and wherever VSPS-J material is used later: the thesis, or a later
  VSPS-J paper's short "what we tried" paragraph or supplement.
- **Options (b)/(c):** a short subsection or supplement of PA4, never the headline.
- **Never in A, B or C (§8).**

**Fixed wording** (adapt the language; keep the content):
> The registered tier-1 rule selected InternVL3-8B with the yes/no frame. On the selection half of M-HalDetect val
> (338 images; selection-biased), at a recall-matched operating point fit on the tune half, its REJECTED precision
> exceeded Vintern-1B's by +7.77 points [5.40, 10.13]. Its strict recall was 2.79 points lower [−5.66, +0.24], which a
> post-hoc plug-in projection from the selection half, made after this result was seen, against the pre-registered
> P(PASS) >= 0.98 gate, judged too large for the registered recall guard. We therefore did not run the confirmation
> step. After seeing this result, we screened one alternative operating point, post hoc: InternVL3-8B set at least 2
> strict-recall points above Vintern-1B's own design point on the tune half (registered cushion, 0.05 threshold grid;
> realised +4.7 object, +2.1 number); this compares the two at Vintern's design point, not at matched recall. A
> one-shot lenient plug-in bootstrap screen estimated P(PASS) = 0.248 (Monte Carlo SE 0.019), below the pre-fixed 0.98
> gate. This screen supports no claim.

**Pointers:** RES 9b9c3f6e; R1C e58904ff; SCORED_1C 7cb88360; LOG l.1243, l.1300, l.1415-1416.

**Wording rules:**
- the 17 excluded images are described only as "reserved for another study, excluded before probing";
- no wording of the kind PI-1101o bars, in either direction (no statement and no denial);
- the main claim stays Vietnamese, and EN is a comparison only (PI-1101t);
- the 3-label scheme is credited to FAIR 2026 (Hòa et al.).

## 8. Salami boundaries

**Against A** (SPIC: gold completeness and the verbosity slope of object-hallucination metrics):
- VSPS-J makes no claim about metric validity, gold completeness or verbosity slope, and reports no CHAIR or object-F1
  slope.
- It uses none of A's registered or sealed sets: XM3600-vi 600, PASCAL-50S, the 3,226 reserved COCO images, A-T3's
  593 val2017 ids (sealed) (N11). Internal record only, never paper text (PI-1101o): 92 ids in the tier-1 selection
  set are A-touched ids by the `counts()` definitions (`A1` l.566-567); they are not A's registered or sealed sets.
- "Number" items are called number propositions. VSPS-J cites A and makes no count-channel or caption-level count claim
  (`V2` R10, l.397).

**Against B** (LRE: KTVIC audit, protocol card and kit):
- Proposition-level verifier recall, precision, retention and AUROC against gold belong to VSPS-J. B never reports them
  (`BV3` §2.1(b), l.85-86).
- VSPS-J does not use Objects365 v2 val and reports no system-level τ (`BV3` §2.1(e), l.96-99).
- B's verifier is never chosen from E2b outputs (`P` §3.6 l.193-194).
- VSPS-J makes no KTVIC benchmark-validity claim. E1b (KTVIC train) is cited only as VSPS-J's own earlier dev row.

**Against C** (TALLIP: PVR on NoCaps with Open Images labels):
- C reports no verifier recall, precision, retention or AUROC, and uses no VSPS-J output (`CV3` §2(a)-(c), l.79-89).
- VSPS-J reports no C downstream result and does not choose C's verifier (`P` §3.6 l.195-196; `V2` R9, l.396).
- VSPS-J uses no NoCaps, OIV7, OpenViVQA or XM3600 data and no mBLIP model.
- Under O2, VSPS-J reads nothing in the Karpathy test, so the KT-C 3,907 part stays C's.

**Against FAIR 2026:**
- The 3-label output and the Vintern-1B verifier are FAIR's and are cited.
- FAIR's numbers are cited, never re-reported as new.
- PA4's numbers are new dev numbers on M-HalDetect, a set FAIR did not use.

## 9. Compute

| option | machine | GPU cap | CPU | money |
|---|---|---|---|---|
| (a) park, (e) defer | none (this file and one LOG line) | 0 | 0 runs | 0 |
| (b)/(c) PA4 | laptop only | 0; no rental | writing; optionally one table build of ≤ 10 min on 3 JSON files (§10) | 0 |
| (d) PA1 | rented RTX 4090 (not licensed) | T2-K 11.81 GPU-h est., cap 17.5, plus tier 3 (not estimated) | — | about 277k VND, or about 376k at the cap, setup included (CC-233r2) |

No option in this file licenses any GPU or rental.

## 10. Code

**For the O2 decision and for options (a), (d) and (e): none.**

**`e2b_1c.py screen-1c` is never run again.** Its once-guard refuses because `SCORED_1C.json` and `res_1c.json` exist
(`O1` §6), and O1-C6 bars any re-screen.

**CC-241r2 N6/N9/N10 are not closed silently (C1; chair's route, round 2 rules on it).** CC-241r2 l.144 carried N6
(hardening a-k) "as post-screen work in a later code round"; l.147 folds N9 into N6(k); l.148 puts N10 in the N6 round.
- **Overruled for this config, with the reason:** CC-241r2 N6 (l.144) presumed a later code round for `|1c`. None can
  exist: the once-guard refuses and O1-C6 bars any re-screen.
- **N6(a)-(j) and N10 become DORMANT.** They reopen automatically if `e2b_1c.py`, `test_e2b_1c.py` or
  `e2b_1c_mutants.py` is ever reused for any run.
- **N6(k) and N9 are closed by citation, not as moot:** `e2b.py` a952755f l.62 (R_DESIGN 0.83, P_TRUE_HI 0.90,
  U_TUNE 0.12); `e2b_1c.py` a0abefd6 l.88 and l.97 (inner seed `seed + b`, b from 0, i.e. 20261102 + b); CC-241r2 l.67.
- This is a record change only; no file is edited.

**For options (b)/(c), optional and only after a 92 GO on PA4:**
- **What:** `scripts/vsps_j_e2b/e2b_pa4_tables.py`, which builds the paper tables from RES, `res_en.json` and R1C.
- **Inputs:** read by sha (9b9c3f6e, f1fea816, e58904ff). It refuses any other input and opens no other path.
- **Before any run:**
  - **selftest** on synthetic JSON:
    - a sha mismatch is refused;
    - opening any other path raises;
    - numbers round-trip exactly, with no re-computation of CIs;
    - sockets raise;
  - **mutants:** a wrong sha accepted; a `probes.jsonl` opened; a value rounded before the write;
  - a one-judge code read (reversible 90) and a gatekeeper commit with SUMS lines.
- **Run limits:** laptop CPU, a 10-minute cap, one run, output sha in an OPS line.
- **No change to** `e2b.py`, `e2b_1c.py` or their tests.

## 11. Honest prior (AI opinion)

| event | estimate | basis |
|---|---|---|
| The E2b registered claim (H1-H4) passes under any O2 option | **0, by construction** (no test look) | O2-(i) |
| Under the earlier paths, for the record: the frozen winner passes H4 at tier 3 | plug-in 0.0021; predictive ≤ ~0.15 (H4 alone) | CC-233 Ruling 1b |
| Under the earlier paths, for the record: `|1c` | screen P̂ = 0.248 < 0.98 (lenient plug-in): NO-GO | LOG l.1416 |
| PA4 meets the Q2 row of `UP` §7 (JVCIR) | **about 5 %** | Q2 needs a registered PASS, or a headline that is stable when each system is left out and is not post hoc. A dev-only headline chosen after the select read is neither |
| PA4 meets the Q3 row (a registered result, PASS or informative FAIL, as the axis) | drafter about 15-25 % (v1 35-45 %); **judges ≤ 10-15 %** (CC-244 Ruling 9; option (c) 15/15/12) | H4 never ran as a registered test: the Q-T2-0 pre-check is a post-hoc projection and O1 is post hoc. The `UP` §7 Q3 row (l.98) needs a registered PASS or informative FAIL as the axis. If the tier-1 selection outputs do not count, this is near 0 |
| PA4 is accepted at JVCIR if written | **≤ 5 %** (v1.1 said about 10 %, which was inconsistent with the Q2-row estimate; N5) | dev-only, selection-biased, recall loss against the deployed baseline; acceptance cannot be likelier than meeting the Q2 row |
| PA1, if it were ever licensed: a fresh tier-2 rehearsal reaches P̂ >= 0.98 | ≤ 5 % | CC-233 Ruling 3c gave 3-5 % before O1; the NO-GO does not raise it; still blocked (§4.3) |

## 12. Options (each with a confidence that it is the right choice; AI opinion)

| # | option | tier | spends | confidence |
|---|---|---|---|---|
| **(a)** | **Stop VSPS-J tier 2 here and park.** O2-(i) closure record. No paper path is adopted. The E2b dev record is sealed as is and reported briefly where used (§7: thesis, or a later VSPS-J paper). All tier-2 and tier-3 candidate sets stay unread. Any revival needs a new direction and its own 92 ruling. CC-241r2 N6/N9/N10 handled as in §10 | reversible in substance; ruled here at 92 (§4.1) | nothing | **90 (recommended to the PI, not a fallback); judges 95/92/93 on the merits (CC-244)** |
| (b) | O2 = PA4 at JVCIR (Q2), under the W-1..W-4 gates of §4.2 | irreversible 92 (main direction) | 0 GPU, 0 test looks; writer time after A/B/C | drafter 25; **judges 12/8/10** (CC-244): by `UP` §7 (l.97) it cannot meet the Q2 row (K-3 would fire), and it conflicts with the adopted form of PI-1029m (LOG l.756); first opening of three R1C blocks |
| (c) | O2 = PA4 at a Q3 venue (one tier lower), same gates with the Q3 row | irreversible 92 | as (b) | drafter 25 (v1 40); **judges 15/15/12** (CC-244): the blocker is the `UP` §7 Q3 row (l.98), which needs a registered PASS or informative FAIL as the axis, and H4 never ran as a registered test (N7); needs Q-O2-2 = YES; first opening of three R1C blocks |
| (d) | O2 = PA1: register a Pareto criterion now, then a tier-2 rehearsal, then tier 3 | irreversible 92, plus later 92 rulings for tier 2, the ledger and tier 3 | up to 17.5 GPU-h at T2-K, about 376k VND, plus tier 3; T2-K and a tier-3 set | drafter 8; **judges 4/3/3**: blocked (§4.3); the criterion would be post hoc |
| (e) | Defer: no ruling now; nothing recorded | reversible | nothing | drafter 60; **judges 55/50/55**: the same practical state as (a), but VSPS-J stays undecided and the 92 question comes back later. It is the interim state now (CC-244) |
| (f) | Any new post-hoc variant (second cushion, 0.01 grid, number-only O5, Q-recall O6, EN-only O4, switch to qwen3vl) | rule change after the outcome | varies | drafter ≤ 5; **judges 2/1/≤2**: against O1-C6 ("ever", `O1` l.182), CC-233 Ruling 3e and PI-1101t |

**Why (a) over (b) and (c).**
- Under the PI's own rules, a VSPS-J paper without a PASS headline falls below the bar:
  - PI-1029m (LOG l.756): "papers must aim at PASS results; failures mentioned only as context once a PASS is found".
    "No PASS, no paper" is the coordinator's adopted reading (N6);
  - `UP` §7: Q2 needs a registered PASS or a stable, non-post-hoc headline.
- (a) spends nothing and keeps every fresh set fresh. It keeps the E2b record intact for later use, and it frees writer
  time for A, B and C.
- PA4 stays documented here. Adopting it later costs one 92 ruling and loses nothing.

**Why (a) over (e).** The two are the same in practice. (a) closes the question in the record, so the next STATE file
and later agents do not reopen a tier-2 look on E2b.

## 13. Questions for the PI (each with a recommended answer and a default)

| # | question | recommended | default |
|---|---|---|---|
| Q-O2-1 | Which state does VSPS-J enter after the failed O1 screen: (a) stop tier 2 and park, (b) PA4 at JVCIR, (c) PA4 at a Q3 venue, (d) PA1, or (e) defer? Note (N8): (a) leaves PI-1031g (VSPS Q2 journal goal: recall >= 80 % with the other metrics clearly better; LOG l.990) open for a future new direction, and it departs from the PA4 content of O2 that you saw in CC-233's "For the PI" | **(a)** | (a), taking effect only after a 92 GO or your direct line; until then nothing changes (B1) |
| Q-O2-2 | Make an exception to PI-1029m and to the Q2 row of `UP` §7, so that a VSPS-J paper may have no PASS headline (dev-only PA4)? | **NO** | NO |
| Q-O2-3 | Report the E2b dev record (tier-1 numbers, the Q-T2-0 pre-check, the O1 NO-GO) briefly, with the §7 wording, in the thesis and in any later VSPS-J paper, and never in A, B or C? | **YES** | YES |
| Q-O2-4 | Keep every E2b tier-2 and tier-3 candidate set unread and unassigned (M-HalDetect train T2-S 2,176; Karpathy test T2-K 4,198; AMBER; VALSE; e-SNLI-VE), with any reassignment only through the PORTFOLIO ledger under its own ruling? | **YES** | YES |
| Q-O2-5 | Give VSPS-J a new direction search (one novelty-iterate run at the PI-1103a pass level) toward PI-1031g? Conditions (N9): after A is submitted; after you answer the MT4-pause question (STATE_2026-11-03 l.23); with 7-day usage headroom; with fresh dev-confirm data named before it starts. Reversible | **YES, under those conditions**; not now | none until the PI asks |

## 14. Binding rules: check

| rule | how this file meets it |
|---|---|
| One look per test set | 0 test looks under every option except (d), which is blocked and would need its own 92 rulings |
| Full official splits | No new run. PA4 reports the full 769-image probe split beside the select and held numbers, as `P` §4.5 registered. The pre-probing exclusion is disclosed with the §7 wording |
| No new gold | No annotation. M-HalDetect human labels only. Manual error categories are barred (W-1) |
| AI labels are not evidence | Model outputs are system outputs and never gold. LLM error tags are barred (W-1) |
| Main claim Vietnamese | vi frame primary. EN is a comparison arm, descriptive (`P` l.220; PI-1101t). O4 (EN-only) is rejected |
| No data-overlap wording | §7 wording rules. This file's paper-facing text uses "reserved for another study" only |
| Three-tier method | No config went to tier 2. A pre-failed or failed rehearsal never touches test (§4.3) |
| Irreversible >= 92 | §4.1: a full panel plus Codex, 3 rounds |
| Questions carry a recommendation and a default | §13 |
| Post-hoc results labelled as post hoc | §1, §2, §7 (B2) |
| A past ruling is never contradicted silently | §10 (C1: CC-241r2 N6 overruled for this config with a reason) |
| A/B/C first | W-4, K-7; option (a) frees writer time |

## 15. v1.1 changes (v1 e97760a4 stays byte-equal)

| # | fix | where |
|---|---|---|
| F1 | "Neither gets a tier-2 or tier-3 look, ever" → "… without a new direction, a new prereg and its own >= 92 ruling". Q-T2-0 stays REVERSIBLE as CC-233 Ruling 2 ruled, so option (a) carries no new irreversible closure and may stay the default (§0 item 6, §4.1). The "default" wording is superseded in v1.2 by CC-244 B1 (§16): (a) is a recommendation to the PI, not a fallback | §3, §5 |
| F2 | AMBER: "assigned to / is L2-P2's" → "proposed for L2-P2, pending a PI line" (PORTFOLIO l.69, l.174; CC-147 r4 fallback-only) | §0, §4.3, §5 |
| F3 | The Q3 estimate is lowered and qualified, because H4 was never run as a registered test: §11 Q3 row 35-45 % → 15-25 %; option (c) 40 → 25. The recommendation is unchanged | §11, §12 |
| F4 | The §7 fixed wording "a pre-fixed feasibility check" → "a check under the pre-registered P(PASS) >= 0.98 rule" (`P` l.264-269; the check was applied after the outcome). Superseded in v1.2 by CC-244 B2(i) (§16) | §7 |

## 16. v1.2 changes: CC-244 item → section (v1 e97760a4 and v1.1 2b704b13 stay byte-equal)

| CC-244 item | change | where |
|---|---|---|
| B1 | Deleted "Option (a) then needs only a reversible >= 90 read". After round 3 without GO: ESCALATE_TO_PI with the open list; VSPS-J stays as Q-T2-0 and O1-C6 left it; nothing adopted or spent; no automatic step. (a) is a recommendation to the PI, not a fallback | §0 item 6, §4.1, §12 (a), §13 Q-O2-1 |
| B2(i) | Fixed wording: "a post-hoc plug-in projection from the selection half, made after this result was seen, against the pre-registered P(PASS) >= 0.98 gate" | §7; also §2 pre-check row, §1 |
| B2(ii) | Fixed wording: "set at least 2 strict-recall points above Vintern-1B's own design point on the tune half (registered cushion, 0.05 threshold grid; realised +4.7 object, +2.1 number)" | §7 |
| C1 | CC-241r2 N6 (l.144) overruled for this config with the reason; N6(a)-(j) and N10 DORMANT (reopen on any reuse); N6(k) and N9 closed by citation (e2b.py a952755f l.62; e2b_1c.py a0abefd6 l.88, l.97; CC-241r2 l.67) | §10, §12 (a), §14 |
| N1 | §1 heading "No trigger in P or V2 fired"; O2 entry registered post hoc by TIER1C §6 (l.180-182, 8511fe6, 08:31:54Z) before the 11:28:55Z launch (LOG l.1415) | §1 |
| N2 | "No new reads" true for (a) and (e) only; (b)/(c) = first opening of R1C's select, predictive_descriptive and held_report_only blocks; W-1 reconciled (no held probe rows; the held aggregate is the only held source) | §0 item 4, §4.2 W-1, §5, §12 (b)(c) |
| N3 | O1-C6 "ever" survives F1; revival = NEW config on fresh dev-confirm data; select half and held 107 count as explored | §3 |
| N4 | "H1's point and CI criteria were met descriptively on the selection-biased select half" | §1 |
| N5 | Judges' ≤ 10-15 % for (c) shown beside the drafter's 15-25 %; JVCIR acceptance 10 % → ≤ 5 %, consistent with the Q2-row 5 % | §11 |
| N6 | PI-1029m quoted from LOG l.756; "no PASS, no paper" marked as the coordinator's adopted reading | §0 item 4, §12 |
| N7 | Option (c): "below the PI's Q1/Q2 bar" dropped; blocker = `UP` §7 Q3 row (l.98) | §12 (c) |
| N8 | Q-O2-1 notes that PI-1031g (LOG l.990) stays open and that (a) departs from CC-233's PA4 content | §13 |
| N9 | Q-O2-5 conditions: A submitted, MT4-pause answer, 7-day usage headroom, fresh dev-confirm data named | §13 |
| N10 | §7: "at a recall-matched operating point fit on the tune half"; "lenient plug-in" before the screen P(PASS) | §7 |
| N11 | "none of A's registered or sealed sets"; 92 A-touched ids (A1 l.566-567) noted as internal record only, never paper text | §8 |
| N12 | Title "draft v1.2"; after a GO on (a), the next STATE file marks VSPS-J PARKED, not before | title, §4.1 |
| N13 | Request path error (UPGRADE_PLAN lives at `manuscript/UPGRADE_PLAN_2026-10-27.md`); the draft already cites it correctly | no change |
| N14 | AMBER = 2311.07397 (2023); AMBER-MUL = Qu et al. 2024, 2408.00550 | §4.2 W-2 |
| N15 | Custody: the CC-244 judges opened only the same R1C fields | header "What was read" |
| Tier and round | Round 1 = CC-244 NEXT_ROUND 88; round 2 = full panel + Codex | header |
