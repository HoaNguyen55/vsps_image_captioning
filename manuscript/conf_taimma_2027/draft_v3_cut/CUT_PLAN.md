# Cut plan: TAIMMA draft of Paper C, from 19 pages to 15 or fewer

Written 2026-11-15 (UTC). A proposal for a ruling. Page figures come from `PAGE_BUDGET.md`: v2.1 values are measured on the as-run PDF, v3 values are estimates.

## 1. The problem in numbers

- Built: 19 pages in both layouts; 18.71 pages of content in the default layout. Limit: 12 to 15 pages, references included (CC-414 Ruling 2 criterion).
- To land at 14.5 or under, 4.2 pages must go; the request asks for options of at least 4.5.
- What cannot shrink (CC-414 Ruling 2 and plan A.5): Section 7 with the compute line (1.63), the end sections with their [PI] placeholders (0.61), the registered rules and results with their labels and sensitivities (rules table 0.96, Vietnamese results table 0.88, English results table 0.55 before the cut), the abstract, contributions and conclusion that must each carry the two FAILs and the P1 scope. With the front matter and the reference list, about 9.4 of the 18.71 pages are fixed or nearly fixed.
- Venue facts used (`manuscript/cfp/TAIMMA_CONF_2026-11-13.md`): full paper "minimum 12 pages, maximum 15 pages"; Springer LNCS template; whether references count is not stated; **supplementary material is not stated**; no extra-page charge is stated; the paper must be "original, unpublished, and not under review elsewhere". So no table can be moved to a supplement on the venue's word, and no pointer to a journal version is possible: that version is not published and cannot be under review at the same time.

## 2. Options

### Option A: the ruled cuts only (CC-414 Ruling 2, c1 to c4)

| item | saving (pages) | scientific cost |
|---|---|---|
| c1: last sentence of S2-02 | 0.03 | none (repeats S1-02) |
| c2: numbers of the NoCaps domain sentence (stay in the table) | 0.03 | none |
| c3: last sentence of S1-03 | 0.02 | none |
| c4: related-work table replaced by two sentences | 0.75 | the column "examples shown" is lost; every "no; no" stays in words |
| c4: English rows of the per-arm table | 0.16 | the 12 English per-arm scores are not printed |
| c4: C42, `rand` minus `zs` on COCO | 0.05 | one descriptive English contrast lost |
| c4: C28 removed, C27 cut to one clause | 0.11 | the PTB column of the Vietnamese sets and the near-verbatim shares are not printed |
| **total** | **1.15** | |

Result: about 17.6 pages of content, an 18-page PDF. **Option A does not meet the limit.** Every registered negative, limit, disclosure and label stays where it is in v2.1.

### Option B (recommended): keep both languages and every registered row; remove the figure and three of the seven tables, fold their content into the text

Option A plus:

| item | saving (pages) | scientific cost |
|---|---|---|
| Fig. 1 removed (it holds a whole page) | 1.00 | no number is lost (all 12 intervals are in the two results tables); the paper has no figure, and the side-by-side picture of the four sets is gone |
| sets table (Table 3 of v2.1) folded into S4-01, S4-02, S6-01 and the caption of the rules table | 0.81 | no size is lost except the three NoCaps domain counts; the reader has no one-glance list of the ten sets |
| configuration table (Table 2 of v2.1) folded into one sentence of S3-05 | 0.12 | none (every cell is in the sentence) |
| rules table set in two columns (name; estimand, set and rule) | 0.19 | none (every word of every cell kept) |
| NoCaps rows by domain label (C41) and their two sentences | 0.17 | a reported, non-gating descriptive split is lost; it was the only printed gradient from in-domain to out-domain images. Named in S7-D12 |
| copy baselines removed whole (the remaining clause of C27, the definition S3-02b, one reference) | 0.18 | a registered non-gating secondary is not printed: the reader no longer sees that `ret` beats the two copy baselines. Named in S7-D12. This goes further than the ruling ("C27 to one clause") |
| S2-01 (opening of related work), one reference | 0.19 | the split into method papers and analysis papers is lost; S1-04 still says that no method is proposed |
| the sentence of S2-02 on text-driven in-context learning, one reference | 0.12 | one related-work fact lost (it motivated the `rand` control together with the c1 sentence) |
| the clause of S1-01 that cites the low-resource taxonomy, one reference | 0.10 | none for the argument |
| the sentence of S2-04 on other Vietnamese captioners, three references (last in the order) | 0.33 | no Vietnamese captioner paper is cited any more, the group's own earlier conference paper included: a reviewer from that community may miss them |
| additions: the rows that left are named in S7-D12; one caption sentence moved into S6-04 | costs 0.07 | none |
| **total with Option A** | **4.31** | |

Result: **about 14.4 pages of content, a 15-page PDF** (default layout; about 14.5 in the other layout). This is the draft in `paper.md`.

Reference list: 34 to 27 entries. Each of the 7 leaves only because the sentence that cited it left (rule (c) of the request); no citation was taken out of a kept sentence.

### Option C: move the English comparison out (Section 6, the English rows of three tables, five references, the English sentences of abstract, introduction and conclusion)

| item | saving (pages) | scientific cost |
|---|---|---|
| Section 6 with the English results table and the figure | 2.30 | the English arm is not in the paper |
| English rows of the per-arm, sets and rules tables | about 0.5 | |
| five references used only there | about 0.4 | |
| English sentences of the abstract, S1-06, S1-07, S8-01, S8-02 | about 0.15 | |
| the non-English part of Option A | 0.9 | as in Option A |
| **total** | **about 4.3** | |

Result: about 14.4 pages, and the figure would have to be redrawn without its English panel. **Option C is not open without a new ruling and a PI decision, and I do not recommend it:**

- It cuts plan A.5 rows: S-NC FAIL (C37), the S-NC sensitivity FAIL (C38), the "not detected" rows on COCO and NoCaps (C35, C40) and the reported row below zero on COCO (C34). Ruling 2 says a plan A.5 row is never cut.
- It leaves the five English disclosures of Section 7 (D03 to D07) without their subject, and they may not be cut either.
- The venue does not state that supplementary material is accepted, and a pointer to the journal version is not possible (section 1).
- The PI's rule of 26 Oct 2026 asks every paper to compare the Vietnamese results with English data sets.

### Variant B-fig: Option B but keep Fig. 1

The figure costs 0.6 page if it shares a page with text and 1.0 as built. Keeping it puts Option B at 15.0 to 15.4. To pay for it, the per-arm table and the sentences that read it (C29, C54; 0.27) and about 0.4 more would have to go; nothing of that size is left outside the protected list. Not recommended; the figure is the first large unit to restore if the venue confirms that references do not count.

## 3. Where the protected statements are in Option B

| statement (plan A.5 or CC-414 never-cut list) | where it stays |
|---|---|
| XM-a FAIL, +0.70 [−0.45, 1.97], with the rule and the registered wording | abstract, S1-07, results table (T6), S5-06, S8-02 |
| XM prediction "not confirmed" | results table (T6), S5-07, S8-02 |
| S-NC FAIL, +1.73 [0.94, 2.50], point below +2.0, transfer claim not made | abstract, S1-07, English table (T7), S6-03, S8-02 |
| S-NC sensitivity FAIL (3,500 images) | English table (T7), S6-03, S8-02 |
| Guard hypothesis H_G "not passed" | S3-05 (unchanged W1 text) |
| Scope of P1 beside every pooled P1 number | abstract, S1-06, caption of T6, S5-02, S8-01 |
| InternVL3 at τ = −∞ "not detected" (five label rows) | T6 (two), T7 (three), in words in S5-04 and S6-03 |
| Reported rows against the claim (InternVL3 below zero on XM and COCO; the XM count-matched row) | T6, T7, S5-06, S5-07, S6-02, abstract, S1-06, S8-01 |
| What the deletion step did on OpenViIC test | S5-04 (unchanged) |
| Registered sensitivities of every prediction and of the registered secondary | T6 and T7 (unchanged cells), caption of the rules table |
| Post hoc rows without the flagged queries | S5-05, S6-02 (unchanged), S7-D08 |
| All 11 disclosure bullets and all 7 limitation bullets | Section 7; only S7-D12 changed, by an addition |
| Compute line | S7-03 (unchanged) |
| Declarations with their [PI] placeholders | end sections (unchanged) |
| The two labels that wait for the re-check after 16 Nov 05:00Z (dagger note with S5-09; S7-L06) | byte-unchanged |
| NOT RUN statements | v2.1 holds none in scope S1; none added, none removed |

The checker's plan-A.5 check passes on the cut draft: 24 of 24 required statements, in the same places as in v2.1.

## 4. Recommendation

**Option B.** Confidence that it is the right option: **75%**. Confidence that its build gives 15 pages or fewer with today's placeholders: about 85%; about 70% once the PI's author block, licences and acknowledgment are in.

Why it is not higher:

- No build was run; the estimate rests on one measured build and a model of line and table wrapping. Page breaks after the cut are not modelled.
- Option B goes beyond CC-414 Ruling 2 in ten items, so it needs a ruling; a judge may prefer to keep the figure or the sets table and cut elsewhere.
- The paper loses its only figure and keeps four tables; this weakens the presentation of a results paper.
- The cut of the sentence on other Vietnamese captioners removes the citation of the group's own earlier conference paper. That is a PI decision.
- The text of Sections 5 and 7 may still change at the re-check after 16 Nov 05:00Z, and the placeholders will grow.

## 5. If the host build differs from the estimate

**Still over 15 pages: cut next, in this order, one at a time, measuring after each** (none of these is on the protected list; OLD texts are in `draft_v2_1/paper.md`):

1. S3-07, the sentence "The equal number of mentions keeps a longer caption from being penalised for naming more objects." (0.03; a rationale, not a definition).
2. S1-03, the sentence that lists the four prompts (0.05; S1-05 and S3-02 define them).
3. The per-arm table (Table 2 of v3) with the second sentence of S5-08 and the first sentence of S8-03 (0.27). Cost: the 16 Vietnamese per-arm scores (C29) and the descriptive reading that random examples already score well above zero-shot (C54) leave the paper; the dagger note would then stand only in S5-09, which waits for the re-check. This is a real loss and should be the last resort.

If the PDF is still over 15 after step 3 (about 14.05 by the estimate, so only if the estimate is wrong by a full page), the remaining candidates are all on the protected list. I would stop there and report the count; I do not propose a cut of an A.5 item.

**Room left (14.6 pages of content or fewer after the PI text is in): restore in this order:**

1. E06b, the sentence on other Vietnamese captioners with its three references (+0.33).
2. One clause on the copy baselines, as CC-414 ruled (+0.18).
3. The NoCaps rows by domain label with their two sentences (+0.17).
4. The sentence of S2-02 on text-driven in-context learning (+0.12).

The sets table (+0.81) and the figure (+0.6 to +1.0) fit only if the venue states that references do not count toward the 15 pages (the reference list is 2.2 pages).

## 6. A layout point for the host build (no text change)

In the v2.1 build the figure took a page of its own with about 0.4 page of white space. This matters only if the figure is restored: its placement should then be set so that it shares a page with text.
