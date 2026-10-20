# Triage of the mock reviews (2026-10-20)

**Sources:**
- `review/PAPER_A_MOCK_REVIEW_2026-10-20.md`: 4 FATAL / 23 MAJOR / 17 MINOR
- `review/PAPER_B_MOCK_REVIEW_2026-10-20.md`: 5 FATAL / 17 MAJOR / 10 MINOR

Main checked the load-bearing claims against the drafts, and they hold. The external references the panels suggested have **not** yet been checked: HQM arXiv 2406.17115, Geva 2019, Caglayan 2020, the VieCap4H DOI, TALLIP, and an "IP&M low-resource special issue, 2027-08-31". Each must be checked before it enters a plan or a bib. A 2027-08-31 deadline would miss the Jan 2027 goal in any case.

## Kind 1: rewriting only (about 60% of the volume; no decision needed)

**Paper A**
- Stale "pending/scheduled" text: DONE 2026-10-20 (sec1, sec3, sec7, sec10, sec11).
- §10.6 "Open items" and the remaining TODOs: N9/B3 wording; the declarations AI-use TODO; licence TODOs.
- Internal codes on the visible page: 49 distinct codes, "frozen locally" 29 times. Replace them with plain wording, and keep the source trail in comments.
- Table 7.1's Source column (JSON keys) and the supplementary's [sX.YY] markers move into comments.
- Declarations: data and code availability, CRediT, funding, competing interests.
- Add an M-HalDetect bib entry.
- Cut the prose from 12,556 words to at most 12,000.

**Paper B**
- Write the missing abstract and conclusion. Resolve the TODOs and PENDING markers.
- DPO contradiction: sec4:79 predates S3, so update it to the S3 FAIL.
- Add an explicit A↔B overlap table. Under the PD-6 ledger the XM3600 and UIT-ViIC slopes belong to Paper A; take them off Paper B's primary lines (sec3:15, sec3:38, sec5:78) and cite Paper A instead.

## Kind 2: scope decisions for the judge

- **Paper A narrows to one plain-language confirmatory claim:** gold completeness decides the sign of F1's verbosity reward, registered on XM3600 and with a second backbone on 3 sets.
  - The theory becomes a descriptive decomposition (sec4:42 and sec4:56 support the reviewers).
  - Count control, human validity and preference data are labelled exploratory.
  - The 8-LVLM ranking result (A-N2) is the practical result.
- **The abstract** is the map's verbatim frame. A plain-language abstract needs a CONFIRMATION_MAP amendment that keeps the claim strength unchanged: one judge question.
- **Disclosures:** image reuse (cv295 is a discovery set; xm600 against §7.5 needs an image-list check), the 160-token cap, harness agreement, and K2 run in the harness that failed fidelity.
- **SCAR random-deletion null** (CPU, existing outputs): post hoc. The judge fixes its design first; it can only be exploratory.

## Kind 3: substantive gaps

- **Paper B's resource has no access route.** What can realistically ship:
  - code, the protocol card, the matcher and the scripts, under an open-source licence, archived with a DOI (e.g. Zenodo);
  - pointers to the original datasets;
  - no OpenViIC text and no KTVIC references.
  - Checkpoints only if the backbone licence allows; the 3B model is under the Qwen Research licence.
  - Establish what can legally ship before promising it.
- **Paper B has no method result.** Reviewers advise moving the ladder, the second backbone, the leaderboard and Section 6 to a supplement and centring the paper on the audit plus the kit.
- **Paper A's theory and count control** are real losses of scope, not writing issues.

## GPU decision

- None of Paper A's fixes need a GPU.
- Paper B's fatal items are rights, completeness and overlap. B-F1 fixes none of them, and its dev lower bound of +0.004 makes INCONCLUSIVE likely.
- **Hold the rental until the Paper B shape is decided.** If the method results move to a supplement, B-F1 stays a cheap registered run (at most 5 GPU-h) that can happen any time before the B draft. It is not on the critical path.

## Realistic outlook (no promise)

- **Paper A, after kind 1 + kind 2:** a narrow, honest measurement paper with a confirmed claim and a practical ranking result. "Major revision" is plausible at IP&M; not guaranteed.
- **Paper B, after kind 1 + kind 3:** an audit-and-kit paper. LRE fits only if the kit really ships. Otherwise its odds are low at any Q1/Q2 venue.
