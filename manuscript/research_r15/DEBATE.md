# R15 debate: research direction under no-GPU (2026-10-18)

## Round 1 — Strategist

Sources: PD-6..PD-9 = `.session_backup/2026-10-13/decisions/PD-{6,7,8,9}.txt`; SYN = `manuscript/research_r14/R14_00_SYNTHESIS.md`;
OA = `manuscript/journal_draft/outline.md`; OB = `manuscript/journal_draft_B/outline_B.md`; ST = `manuscript/journal_draft_B/STATUS.md`;
SL = `manuscript/cfp/TWO_PAPER_SHORTLIST.md`; R13 = `manuscript/research_r13/R13_LIT_UPDATE.md`. `manuscript/research_r15/{A,B}/` are empty: no REVIEW_*.md exists yet.

### Situation in four lines
- Paper A is drafted through §9. Its human-validity pillar is weak: DOCCI MIXED, LongCap-Arena MIXED with the kill fired, THumB/Composite failed; only Polaris and VaPR PASS (OA l.6, l.32, l.46-47).
- Paper A still has GPU items pending: N9, the E1 K2 placebo, G2-B and B3 (OA l.44-45).
- Paper B has a full first draft with 10 PENDING manifest rows (ST). No method has been validated: the kNN prior was killed (OB "D18 §5.2"), B1 was aborted (PD-8), and M3/S1-S5 never ran (SYN, PD-9).
- The freeze rule says a job not done by 2026-11-15 is dropped (PD-6 Q2). That leaves 28 days.

### D1 — Paper A framing
Options:
- (a) a measurement-validity paper on three threats (count, gold completeness, exchangeability), with human evidence stated narrowly (OA);
- (b) a "count-matched precision is the better metric" paper;
- (c) a pure theory paper (proposition C2) with empirics as illustration.

Recommendation: **(a), 88%.**
- (b) is refuted by our own data: count-matched precision does not track humans better (OA l.32).
- (c) throws away E1 and the spec curve, which are our distinct deltas against 2609.01888 (PD-7 Q1; R13 §A1).
- The negative human result becomes a finding, not a hole: humans penalise count, so the confound is real, but the fix does not align better with humans. Keep "no first/novel" (PD-7 Q1).
- Strip [PENDING] N9/G2-B/B3 into the "consistent" fallback that PD-6 Q4(c) already permits, unless D4 buys them.

### D2 — Paper B framing
Options:
- (a) audit-only (fits D7: B's experiment freeze is 2026-11-30): a controlled 148.23 system as the measuring instrument plus the KTVIC validity audit and the pre-registered negatives (OB, D18 §5.2);
- (b) rent about 13 GPU-h for PD-9 Stage 1 and upgrade to method + audit (PD-9 Q4);
- (c) a hybrid: write (a) now and run only S1 seed consensus (4.3 GPU-h, SYN), included only if its dev gate (>= +1.0 CIDEr) and the single prereg'd test look both pass.

Recommendation: **(a) as the committed framing, with (c) as an optional add-on, 80%.**
- The Stage-1 priors are weak. SYN itself caps detector methods at F1 +0.6 to +1.7. The reranking ceiling is only +0.6 F1 on the panel. The one solid CIDEr lever is a +3.05 test-pool proxy that is labelled exploratory (PD-9 Q5).
- LRE, the primary venue, rewards the audit, not SOTA (SL Paper B #1). A method win changes the venue only marginally.
- So 13 GPU-h buys a low chance of a change that matters little. S1 alone is the cheapest and highest-prior item.
- Do not run S3 (M3 DPO). Its gate needs a panel-side gain (PD-9 Q2), and the panel ceiling is +0.6 (SYN). That gate will most likely fail.

### D3 — Venue order
Paper A, recommended order (75%):
1. ACL 2027 via ARR (2027-01-04) as the primary target. It fits the January goal, and Findings is an acceptable floor.
2. TACL after ARR. Not before: simultaneous submission is barred (SL A#2), and the MIXED human evidence weakens a TACL-first bid (OA l.6).
3. IP&M (Q1, SCIE) as the WoS fallback.
4. TMLR as the safety (Q2, not WoS).

This flips OA l.6 (TACL first). TACL's page and policy terms are [CHƯA XÁC MINH] (SL), while ARR has a hard date that matches the goal.

Caveat: ARR has no quartile (SL A#1). If "Q1-submittable" must mean a journal, then IP&M goes first by 2026-12-20, and ARR waits for the next cycle with A not resubmitted elsewhere in the meantime. **The user must state which reading of "Q1" counts.** This is the one question I cannot settle (<80%).

Paper B, recommended order (85%): LRE -> IP&M special issue (closes 2027-08-31) -> TALLIP (OB venue table). All conference routes bar prior-published extensions (SL Paper B note).

### D4 — Rent a GPU?
Options:
- (0) no rental;
- (1) about 6 GPU-h for Paper A's own pending items (N9 + E1 K2 placebo + G2-B; G2-B is +1.7, PD-6 Q3) plus S1 (4.3) = about 10-12 GPU-h on one 24 GB card, about 1-2 days;
- (2) the full Stage 1 plus the PD-6 core ladder (about 60-90 GPU-h, PD-6 Q2).

Recommendation: **(1), 70%. At this confidence the user decides** (memory: judge protocol). Rationale and rules:
- N9 decides whether C1 is "rank change" or "consistent" (PD-6 Q4c). That is Paper A's headline, and it is cheap.
- Hard cap: 15 GPU-h. A's runs finish by 2026-11-10 and B's S1 by 2026-11-30 (D7 tightens PD-6 Q2's 11-15 for A). Use the 30-min backup (memory: gpu-backup-30min).
- If the user declines, (0) is viable. A uses the PD-6 Q4(c) wording, and B is audit-only. Nothing breaks.

### D5 — CPU-only work now (95%)
1. Paper A:
   - an end-to-end self-review;
   - the src-comment completeness check on every number (ST asks for this for B; do the same for A);
   - rewrite §1/§8 around the "confound real, fix not human-aligned" result.
2. Paper B:
   - fix the six Gemini prose errors (ST "Mismatches" 1-4, 6);
   - resolve the 56-58 run-ID clash (ST);
   - write the post-hoc calibration note (PD-8 §3);
   - convert the PENDING rows to "not run / reviewer-requested" if there is no rental.
3. XM3600 period-appended CIDEr-D: CPU-scorable from the committed predictions (ST TODO).
4. The paired CI for the UIT-ViIC role/child CHAIR_i flip (ST TODO), also CPU.
5. Literature:
   - read HDUCap and ViG via another access route before 2026-11-01 (PD-7 Q5; ST 403 note);
   - verify the [VERIFY] citations;
   - re-check 2609.01888 for a newer version (PD-7 Q1).
6. Send the KTVIC/OpenViIC licence e-mails if they are not already sent (PD-6 Q4a). LRE checks availability.
7. Write the S1/N9 preregs now, so that any rental starts on committed preregs (PD-9 Q1).
8. Create `research_r15/A|B/REVIEW_*.md` red-team reviews of both drafts. The directories are empty.

### D6 — Risks and kill/switch rules
| Risk | Evidence | Kill / switch rule |
|---|---|---|
| Scoop on C1 (count confound) | 2609.01888 and 3 others (PD-7 Q1; R13 §A1) | Re-run the scoop-watch on 2026-12-10 (PD-7). If a paper does per-image count matching on published methods, demote C1 and lead with C2 (gold-completeness proposition) and the spec curve. |
| Human-validity reviewers reject A | 3 of 5 sets fail or are MIXED (OA l.32) | No more human sets (no annotation). If ARR returns "weak evidence", switch to TMLR (graded on correctness), not TACL. |
| N9 shows no rank change | PD-6 Q4c | Report C1 as "consistent" and submit anyway. Never re-specify N9 after seeing it. |
| Rental slips past the freeze | PD-6 Q2; D7 | A job not done by its D7 freeze (A 11-10, B 11-30) is dropped. S1 runs only if it starts by 2026-11-05 (PD-9 Q3). |
| S1 fails its dev gate | SYN gate | Do not run test. Report it as a pre-registered negative in B §6. B stays audit-only. |
| Salami or self-plagiarism flag between A and B | PD-6 Q1a-c | Claim ledger: no shared primary number. Disclose each paper to the other's editor. B is >= 30% new vs FAIR (ST: about 88%). |
| No KTVIC licence, so LRE flags availability | PD-6 Q4a | Release only code, splits, IDs and aggregates. If there is no reply by 2026-12-15, state "available from the dataset authors". |
| ARR not counted as "Q1" by the user | SL A#1 | Switch A's first target to IP&M, submitted by 2026-12-20. |
| Writing bandwidth (the real bottleneck, PD-6 Q2) | ST "stopped early" | The complete-draft dates in D7 are hard (A 2026-11-20, B 2026-12-25). If A misses 11-20 by more than 7 days, its target moves to ARR 2027-01-04 and B's red-team slot shifts; if it misses by 14 days, A goes to TMLR. |

### D7 — Roadmap (user rule: complete draft 1 month before submission), 85%
| Date | Paper A (submit 2026-12-20) | Paper B (submit 2027-01-25) |
|---|---|---|
| now-11-05 | CPU items D5.1/3/5; preregs D5.7; rental decision by 10-22 | D5.2/4/6 fixes; B mostly frozen already (ST) |
| 2026-11-10 | **Experiment freeze** (N9/E1 K2/G2-B or the PD-6 Q4c fallback) | — |
| 2026-11-20 | **Complete draft** (all §, abstract, appendix, manifest 0 PENDING) | writing continues |
| 11-21 to 11-30 | Internal red-team review (research_r15/A/REVIEW_*.md) | **Experiment freeze 11-30** (S1 or nothing) |
| 12-01 to 12-14 | Revision window 1 (red-team fixes, number re-trace) | drafting |
| 12-10 | Scoop-watch re-run (PD-7) | — |
| 12-15 to 12-19 | Revision window 2: polish, cover letter, disclosure of B | — |
| **2026-12-20** | **Submit** (IP&M or early ARR, per D3 caveat) | — |
| 2026-12-25 | — | **Complete draft** |
| 12-26 to 2027-01-05 | — | Internal red-team review (research_r15/B/REVIEW_*.md) |
| 01-06 to 01-20 | — | Revision windows 1-2 (FAIR-overlap check, licence wording) |
| **2027-01-25** | — | **Submit** to LRE |

Consistency notes:
- A's freeze moves from 11-15 (PD-6 Q2) to 11-10 so that the 11-20 draft has 10 writing days.
- D4's rental must therefore start by 2026-10-25.

### Asks to the Red Team
- Attack D2: is audit-only really enough for LRE to accept a Q1-level contribution without a method?
- Attack D3: is it a mistake to put ARR ahead of TACL, given the Q1 goal?
- Attack D4: is renting for S1 worth it at all, given the +3.05 figure is a test-pool proxy only?
- Attack D7: is 10 days enough to go from frozen experiments (11-10) to A's complete draft (11-20)?

## Round 2 — Red Team

Checked against: PD-6..PD-9, SYN (`R14_00_SYNTHESIS.md`), OA, OB, ST, SL, and `journal_draft/sec*.md` (about 19.3k words, 12 PENDING tags across 6 files).

### Errors in Round 1 that I found in the sources
1. **VaPR is not human evidence.** It is the positive control of the §9 preference audit (PD-7 Q4; OA §9 row). Round 1 lists "Polaris and VaPR PASS" as the human pillar. The registered human record is therefore: Polaris PASS; DOCCI MIXED; LongCap-Arena MIXED with the kill fired; THumB/Composite exploratory and failed. That is **1 registered pass out of 3 registered sets**.
2. **"Drafted through §9" understates the draft.** §1-§11 all exist (OA section table). What is missing is pending slots, not prose.
3. **Length is the hidden cost.** OA plans TACL at about 10 pages. ARR long papers are 8 pages, and the draft is about 19k words. If ARR is the target, a cut of more than half is needed, and D7 has no slot for it.
4. **D7 is inconsistent with D3.** D7 submits A on 2026-12-20 "IP&M or early ARR". ARR has no early date: the cycle closes 2027-01-04. Only IP&M fits 12-20.
5. **ST asks for "human sign-off of matcher v3".** That collides with the no-new-gold-labels rule (memory). B must report matcher v3 as unattested (ST mismatch 3), not plan an annotation.

### D1 — Paper A framing: AMEND (85%)
Option (a) is right. However, "the negative human result becomes a finding" is only half true. §10 recommends a two-column standard (count-matched next to raw). If count-matched precision does not track humans better (OA l.32), a reviewer will ask why anyone should report it.
- Change: justify the count-matched column on **construct validity** (it removes a mechanical confound that humans also see, from LongCap-Arena) and **not on human alignment**. State plainly in §1 and §10 that it is a *control*, not a *better score*.
- Lead the paper with C2 plus the out-of-sample XM3600/COCO-2500 confirmations, which are the strongest registered evidence. Move C1 to second place: it is the scoop-exposed claim (PD-7 Q1), and its Holm-surviving count is only 2/15 or 6/15 (OA abstract src).

### D2 — Paper B framing: AMEND (75%)
Audit-only can clear LRE, but only as a **resource** paper. LRE's scope is resources and evaluation. An audit of a dataset we cannot redistribute (PD-6 Q4a: licence not cleared) gives the reader nothing to reuse.
- Change: make the deliverable a released evaluation kit: matcher v3 plus lexicons, split and ID files, the two-gold protocol, the audit scripts, and the 148.23 checkpoints if the Qwen licence allows. Then the paper is "resource plus validity audit", which is LRE's core genre.
- Drop optional add-on (c), S1. A +1 to +3 CIDEr on an already-controlled system does not change LRE's verdict (Round 1's own argument), and its prior is a test-pool proxy (PD-9 Q5). Under PD-9 Q4 it would also pull B back toward a "method" framing that LRE reviewers would then judge as weak SOTA.
- Risk left open: LRE is Q2 in CS Applications (SL). That counts toward the ">=Q2" goal, but **not** as the Q1 paper in a CS sense. Use A for the Q1 slot.

### D3 — Venue order: DISAGREE (80%)
ARR-first works against the user's goal (memory: two papers >=Q2, one Q1-submittable, submitted by Jan 2027).
- ARR has no quartile (SL A#1). If the ACL review gives "Findings", committing uses up the work. Moving it to TACL afterwards depends on TACL's prior-version policy, which is [CHƯA XÁC MINH] (SL). So the most likely ARR outcome (Findings) gives a paper with no quartile.
- IP&M fits better: Q1, SCIE, about 2 days to a first decision (SL A#3), and it accepts our 19k-word length with no cut. Submit on **2026-12-20**. A fast desk reject still leaves ARR 2027-01-04 open, with 15 days to cut to 8 pages. If it goes to review, the goal is already met.
- Revised order: **IP&M (12-20) -> on desk reject, ARR 01-04 -> TMLR**. Drop TACL as a target until its page limits and policies are verified. Our human evidence (1/3 registered) is weakest exactly where TACL's bar is highest.
- This removes Round 1's only <80% question. The ARR/Q1 ambiguity disappears if IP&M goes first. Still confirm with the user (one line).

### D4 — GPU rental: AMEND (70%; the user decides)
- **N9 is not needed.** D6 already says that if N9 shows no rank change, we report "consistent" and submit anyway (PD-6 Q4c). So N9 changes one word of C1, not whether the paper is submitted. Combined with the D1 amend (C1 no longer leads), its value drops further.
- **S1: no** (see D2). **G2-B/B3:** these support the "3 datasets x 2 backbones" claim (PD-6 Q3). Without them, the claim narrows to what has run, which is a one-sentence edit.
- Memory: the rented GPUs expired, and on 2026-10-15 the user stopped work after data loss. A new rental restarts the backup and ops burden.
- Change: default to option **(0)**. If the user wants one rental, cap it at about 6 GPU-h: N9 plus E1 K2 placebo plus G2-B, started by 10-25 with the 30-min backup. No S1.

### D5 — CPU work: AGREE with additions (90%)
- Add: a **length plan for A** (a 10-page TACL/IP&M version now, and an 8-page ARR cut skeleton kept ready for the desk-reject path).
- Add: a **B release-kit checklist** (D2 amend) and a check of Springer/LRE's "expansion of previous work" wording against the FAIR overlap (SL B#1).
- Remove the "human sign-off" item from B's TODO (error 5).
- Order: put D5.6 (licence e-mails) **first**. It has the longest external lead time and gates LRE availability.

### D6 — Risks: AMEND (85%)
- The human-validity row should say "1/3 registered pass", not "3 of 5 fail or MIXED".
- The switch "ARR weak evidence -> TMLR" is superseded by D3. New switch: IP&M desk reject -> ARR 01-04. IP&M reject after review (around 2027-05) -> TMLR, or ARR for EMNLP.
- Add a risk: **the B framing drifts to "method"** if any GPU result arrives (PD-9 Q4). Rule: B's framing is frozen as resource-plus-audit on 11-30, whatever arrives.
- Add a risk: **A/B ledger leak through matcher v3.** It is B-owned (PD-6 Q1a). A must cite it, not re-report its numbers.

### D7 — Roadmap: AMEND (80%)
The 10-day window (11-10 -> 11-20) is realistic **only because** the prose already exists. The work is filling 12 PENDING tags or swapping in their fallback, plus the D1 rewrite of §1/§10. Two real problems:
1. With no rental (D4 default), A has nothing to freeze on 11-10. Move A's complete-draft date **earlier, to 11-15**. That gives 5 weeks before 12-20, more than the user's 1-month rule.
2. B is already fully drafted (ST). A complete B draft on 12-25 wastes 6 weeks and stacks B's red-team on top of the holidays. Move B's complete draft to **12-10**, after A's red-team (11-16 to 11-25). Then B's red-team runs 12-11 to 12-20, and B could be submitted to LRE early in January, ahead of 01-25.
- Keep the 12-10 scoop-watch, and add a second one on 2026-12-18, two days before IP&M submission (PD-7 Q1: re-check just before submitting).
- If any rental happens, A's freeze stays 11-10, with a hard stop. Anything not done is reported as reviewer-requested.

### Net position
Write both papers from what exists, rent no GPU by default, and send A to IP&M on 12-20, which is the direct Q1 route. The case against the Strategist's plan is that ARR and S1 add risk and cost without moving either paper toward the user's quartile goal.

## Round 3 — Strategist
### Errors 1-5: all accepted
1. VaPR is the §9 positive control (PD-7 Q4), not human evidence. The registered human record is 1/3 pass: Polaris PASS, DOCCI MIXED, LongCap-Arena MIXED (OA l.32).
2. §1-§11 all exist; what remains are 12 PENDING slots (OA section table).
3. The length cost is real. An ARR cut needs a skeleton, and D5 now includes one.
4. ARR has no early slot, so 12-20 is IP&M only (SL A#1, A#3).
5. No human sign-off of matcher v3 (memory: no new gold labels). B reports matcher v3 as unattested (ST mismatch 3).
### D1 — accept the amend → CONVERGED (88%)
Paper A is a three-threat measurement-validity paper.
- **Lead:** C2, with the XM3600 and COCO-2500 out-of-sample confirmations (OA §7).
- **Second:** C1, the count control. It is scoop-exposed (PD-7 Q1) and only 2-6 of 15 methods survive (OA abstract).
- **Role of the count-matched column:** justify it in §1 and §10 as a construct-validity *control* (humans see the confound, per LongCap-Arena; OA l.32), never as a better score.
### D2 — accept with one condition → CONVERGED (82%)
Paper B is resource plus validity audit.
- **What is released:** code, matcher v3 and its lexicons, splits and IDs, the two-gold protocol, the audit scripts and aggregate scores. These are exactly the items PD-6 Q4a already permits.
- **Condition:**
  - checkpoints are released only if both the Qwen research licence and the KTVIC terms allow derivative weights. Until confirmed, list them as "on request". KTVIC has no licence file (PD-6 Q4a).
  - matcher v3 is shipped labelled unattested.
- **S1 dropped.** The Red Team is right that it would pull B toward a weak method framing (PD-9 Q4), and its prior is a test-pool proxy (PD-9 Q5).
- **Goal accounting:** B counts toward ">=Q2". LRE is Q1 in Linguistics but Q2 in CS Applications (SL B#1), so A carries the Q1 slot.
### D3 — accept, with one rebuttal → CONVERGED (82%)
Order: IP&M on 12-20, then ARR on 01-04 if IP&M desk-rejects, then TMLR.
- **Rebuttal:** "about 2 days to first decision" is IP&M's published median (SL A#3), not a promise.
  - If IP&M has not decided by 2027-01-02, A stays at IP&M and skips ARR, because dual submission is barred.
  - The ARR path is opportunistic, not planned.
- TACL dropped until verified (SL A#2). User confirms IP&M counts as Q1 (Q1, SCIE: very likely yes).
### D4 — accept the amend → CONVERGED: no rental by default (75%)
- **N9:** it changes one word of C1 and does not decide whether A is submitted (PD-6 Q4c). C1 is no longer the lead (D1).
- **G2-B/B3:** without them, the "3 datasets x 2 backbones" claim narrows to what has run (PD-6 Q3).
- **Ops burden:** a rental restarts the backup and ops work after the 10-15 data loss (memory).
- **If the user wants a rental anyway:** at most 6 GPU-h, covering N9, the E1 K2 placebo and G2-B. It must start by 10-25 and use the 30-min backup. No S1.
- **This is the user's choice.**
### D5 — accept additions → CONVERGED (92%)
Order:
1. Licence e-mails to KTVIC and OpenViIC (PD-6 Q4a).
2. Paper A: rewrite §1/§10 per D1, a 10-page IP&M version, an 8-page ARR cut skeleton, and the number-source check.
3. Paper B fixes:
   - ST mismatches 1-4 and 6;
   - the 56-58 run-ID clash;
   - the PD-8 calibration note;
   - PENDING rows become "not run / reviewer-requested".
4. CPU scoring: XM3600 with the period appended, and the UIT-ViIC paired CI (ST).
5. Literature: HDUCap and ViG, the [VERIFY] citations, and a re-check of 2609.01888 (PD-7).
6. B release-kit checklist, plus the Springer "expansion" wording against the FAIR overlap (SL B#1; ST: about 88% new).
7. Red-team reviews written to `research_r15/{A,B}/REVIEW_*.md`.
Removed: matcher v3 sign-off; S1/N9 preregs only if the user rents.
### D6 — accept the amends → CONVERGED (85%)
| Risk | Kill / switch rule |
|---|---|
| Scoop on C1 (PD-7 Q1) | Scoop-watch on 12-10 and 12-18. If someone has done per-image count matching on published methods, C1 shrinks to a "replication under control" paragraph. |
| Human evidence is 1/3 registered (OA l.32) | Collect no new sets (no annotation). Frame the evidence as bounded (D1). |
| IP&M desk reject | Go to ARR on 01-04 using the cut skeleton. If IP&M rejects after review, go to TMLR or to ARR for EMNLP 2027. |
| B framing drifts to "method" (PD-9 Q4) | B's framing is frozen as resource plus audit on 11-30. Any late GPU result goes to an appendix at most. |
| A/B ledger leak via matcher v3 (PD-6 Q1a) | A cites B for matcher v3 and never re-reports its numbers. Run a ledger diff before each submission. |
| Rental, if any, slips | A's freeze is a hard 11-10. Anything unfinished becomes reviewer-requested. |
| KTVIC licence: no reply | After 12-15, write "available from the dataset authors" (PD-6 Q4a). |
| A's draft is late | More than 5 days past 11-15: drop the ARR skeleton work. More than 14 days: A goes to TMLR. |
### D7 — accept the amend → CONVERGED (82%)
| Date | Paper A | Paper B |
|---|---|---|
| 10-19 to 11-14 | D5 items 1-5; experiment freeze 11-10 (a no-op without a rental) | D5 items 3 and 6 |
| **11-15** | **Complete draft**, 0 PENDING (5 weeks before submission) | — |
| 11-16 to 11-25 | Red-team review (`research_r15/A`) | — |
| 11-26 to 12-17 | Revision windows 1 and 2; scoop-watch on 12-10 | Experiment freeze 11-30 (framing freeze) |
| **12-10** | — | **Complete draft** |
| 12-11 to 12-20 | — | Red-team review (`research_r15/B`) |
| 12-18 | Second scoop-watch, then cover letter (disclose B) | — |
| **12-20** | **Submit to IP&M** | — |
| 12-21 to 01-15 | ARR cut only if IP&M desk-rejects; ARR deadline 01-04 | Revision windows, holiday-padded |
| **by 01-25** | — | **Submit to LRE** (early January if the revisions are done) |
### Final converged decisions
| D | decision | conf | needs user? |
|---|---|---|---|
| D1 | A: three-threat validity paper; C2 leads, C1 second; count-matched precision framed as a control | 88% | no |
| D2 | B: resource plus validity audit with a release kit; no S1; checkpoints only if licences allow | 82% | no |
| D3 | A: IP&M 12-20 → ARR 01-04 on desk reject → TMLR. B: LRE → IP&M SI → TALLIP | 82% | yes (does IP&M count as Q1?) |
| D4 | No GPU rental; optional cap of 6 GPU-h (N9, E1 K2, G2-B) started by 10-25 | 75% | yes (rental choice) |
| D5 | CPU list in the order above; licence e-mails first | 92% | no |
| D6 | Kill/switch table above | 85% | no |
| D7 | A: draft 11-15, submit 12-20. B: draft 12-10, submit by 01-25 | 82% | no |

## User decisions (2026-10-18)
- D4: NO GPU rental at this time. Pending GPU items (N9, E1 K2 placebo, G2-B, B3) are dropped; Paper A uses the narrower "consistent" wording.
- D3: IP&M counts as the Q1 journal. Paper A -> IP&M on 2026-12-20.
All D1-D7 are now final.
