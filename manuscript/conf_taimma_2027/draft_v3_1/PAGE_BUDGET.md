# Page budget: TAIMMA draft, v2.1 as built and the v3 cut draft

Written 2026-11-15T08:43Z (date -u). Nothing here is a build: the v3 column is an estimate made from the measured pages of v2.1.

## 1. How the pages were measured

- Source: the as-run build record of 15 Nov 2026, `out_3/paper_lncs.pdf` (default layout, 19 pages, reference list from page 16) and `out_4/paper_lncs.pdf` (end sections as full unnumbered sections, 19 pages, reference list from page 17). Draft built: `draft_v2_1/paper.md` f65f53ab...; class llncs, style splncs04, letter paper.
- Method: `pdftotext -bbox-layout` gives every text line with its page and its vertical position. A unit starts at the first line of its paragraph, caption or heading and ends where the next unit starts; white space at a page end is charged to the unit that crosses it. One page = the height of the text block, 562 pt (46 lines of 12 pt). The last page is 0.71 full in the default layout, so the 19 pages hold 18.71 pages of content (18.78 in the other layout).
- Fig. 1 sits alone on page 13 (a float page: the plot and its caption fill about 0.6 of it, the rest is white). It is charged one full page, because removing it removes the page.
- The reference list: 34 entries on 140 lines of 9 pt.

## 2. Measured pages by section (v2.1) and estimate (v3 cut draft), default layout

| section | v2.1 measured | v3 estimated | change |
|---|---|---|---|
| Front matter (title block, abstract, keywords) | 0.75 | 0.75 | +0.00 |
| 1 Introduction | 1.06 | 1.02 | -0.04 |
| 2 Related work | 1.57 | 0.64 | -0.93 |
| 3 Method | 1.63 | 1.47 | -0.16 |
| 4 Data and registered plan | 2.99 | 1.94 | -1.05 |
| 5 Results in Vietnamese | 2.84 | 2.49 | -0.35 |
| 6 English comparison | 2.30 | 1.12 | -1.18 |
| 7 Disclosures and limitations | 1.63 | 1.68 | +0.05 |
| 8 Conclusion | 0.48 | 0.48 | +0.00 |
| End sections (ethics and data, availability, acknowledgments, interests) | 0.61 | 0.61 | +0.00 |
| References | 2.85 | 2.20 | -0.65 |
| **total** | **18.71** (19 pages) | **14.40** (15 pages, the last one about 0.4 full) | **-4.31** |

In the other layout (`END_SECTIONS=starred`) the end sections take 0.75 instead of 0.61 and v2.1 holds 18.78 pages; the v3 estimate there is about 14.47.

Of the 18.71 pages of v2.1: the seven tables take 4.67, the figure 1.00, the reference list 2.85, Section 7 with its heading and the compute line 1.63, the end sections 0.61, the front matter 0.75. The running text and headings of Sections 1 to 6 and 8 take the other 7.20.

## 3. Measured pages by unit (v2.1, default layout) and estimate (v3)

"v3 estimated" = the measured value plus the modelled change of that unit. A unit with an empty last cell is unchanged and keeps its measured value. Unit names are the paragraph markers of `paper.md`; table numbers are those of v2.1.

| unit | v2.1 measured | v3 estimated | change |
|---|---|---|---|
| title and author block (placeholders) | 0.26 | 0.26 | |
| abstract | 0.41 | 0.41 | |
| keywords | 0.08 | 0.08 | |
| heading 1 | 0.04 | 0.04 | |
| S1-01 | 0.21 | 0.21 | |
| S1-02 | 0.21 | 0.19 | -0.02 |
| S1-03 | 0.17 | 0.15 | -0.02 |
| S1-04 | 0.03 | 0.03 | |
| S1-05 | 0.09 | 0.09 | |
| S1-06 | 0.17 | 0.17 | |
| S1-07 | 0.14 | 0.14 | |
| heading 2 | 0.04 | 0.04 | |
| S2-01 | 0.09 | 0.00 | -0.09 |
| S2-02 | 0.19 | 0.12 | -0.07 |
| S2-03 | 0.13 | 0.13 | |
| S2-04 | 0.19 | 0.17 | -0.02 |
| S2-05 | 0.11 | 0.18 | +0.07 |
| Table 1 (analyses of in-context captioning) | 0.82 | 0.00 | -0.82 |
| heading 3 | 0.04 | 0.04 | |
| S3-01 | 0.13 | 0.13 | |
| S3-02 | 0.18 | 0.18 | |
| S3-02b | 0.04 | 0.00 | -0.04 |
| S3-03 | 0.15 | 0.15 | |
| S3-04 | 0.19 | 0.19 | |
| S3-05 | 0.28 | 0.35 | +0.07 |
| Table 2 (frozen configurations) | 0.19 | 0.00 | -0.19 |
| S3-06 | 0.13 | 0.13 | |
| S3-07 | 0.30 | 0.30 | |
| heading 4 | 0.04 | 0.04 | |
| S4-01 | 0.23 | 0.25 | +0.02 |
| Table 3 (sets) | 0.90 | 0.00 | -0.90 |
| S4-02 | 0.17 | 0.19 | +0.02 |
| S4-03 | 0.30 | 0.30 | |
| Table 4 (predictions and rules) | 0.96 | 0.77 | -0.19 |
| S4-04 | 0.28 | 0.28 | |
| S4-05 | 0.11 | 0.11 | |
| heading 5 | 0.04 | 0.04 | |
| S5-01 | 0.06 | 0.06 | |
| Table 5 (CIDEr-D per arm) | 0.37 | 0.21 | -0.16 |
| Table 6 (Vietnamese results) | 0.88 | 0.88 | |
| heading 5.1 | 0.04 | 0.04 | |
| S5-02 | 0.15 | 0.15 | |
| S5-03 | 0.13 | 0.13 | |
| S5-04 | 0.17 | 0.17 | |
| S5-05 | 0.22 | 0.22 | |
| heading 5.2 | 0.04 | 0.04 | |
| S5-06 | 0.13 | 0.13 | |
| S5-07 | 0.18 | 0.18 | |
| heading 5.3 | 0.04 | 0.04 | |
| S5-08 | 0.11 | 0.11 | |
| S5-09 | 0.09 | 0.09 | |
| S5-10 | 0.19 | 0.00 | -0.19 |
| heading 6 | 0.04 | 0.04 | |
| S6-01 | 0.19 | 0.24 | +0.05 |
| Table 7 (English results) | 0.55 | 0.42 | -0.13 |
| S6-02 | 0.19 | 0.14 | -0.05 |
| S6-03 | 0.19 | 0.12 | -0.07 |
| Fig. 1 (its own float page, page 13) | 1.00 | 0.00 | -1.00 |
| S6-04 | 0.14 | 0.16 | +0.02 |
| heading 7 | 0.04 | 0.04 | |
| S7 disclosures (lead-in and 11 bullets) | 0.90 | 0.95 | +0.05 |
| S7 limitations (7 bullets) | 0.61 | 0.61 | |
| S7 compute line | 0.08 | 0.08 | |
| heading 8 | 0.04 | 0.04 | |
| S8-01 | 0.19 | 0.19 | |
| S8-02 | 0.11 | 0.11 | |
| S8-03 | 0.14 | 0.14 | |
| DECL-01/02 | 0.28 | 0.28 | |
| DECL-03 | 0.15 | 0.15 | |
| DECL-04 | 0.09 | 0.09 | |
| DECL-05 | 0.09 | 0.09 | |
| References (34 entries, 140 lines) | 2.85 | 2.20 | -0.65 |
| **total** | **18.71** | **14.40** | **-4.31** |

## 4. How the v3 column was estimated

- Running text: lines = characters of the rendered paragraph divided by 83 per 10 pt line (80 for a list item). Checked on v2.1, this model gives 286 lines where 322 were measured, so every modelled change is multiplied by 1.13. One line = 12 pt.
- Tables: the column widths are computed by the same rule as the build filter `lncs.lua` (the computed widths equal the as-run widths of Tables 2 to 7 of v2.1 to three decimals). Cell lines are then wrapped with approximate glyph widths of the 9 pt font. On v2.1 this gives exactly the cell lines seen in the PDF for Tables 5, 6 and 7 (11, 32 and 21). One cell line = 10.95 pt, one row = 2.5 pt more, one caption line = 12 pt.
- Reference list: the 7 entries that leave take 32 of the 140 lines (counted in the PDF), so 2.85 becomes 2.20.
- Not modelled: where the page breaks fall after the cut (a table row or a heading pushed to the next page), and the text that will replace the placeholders (author block, licences, acknowledgments, interests).

## 5. Target budget (at most 14.5 pages, same class and layout)

| block | v2.1 measured | target | v3 estimated |
|---|---|---|---|
| Front matter | 0.75 | 0.75 | 0.75 |
| 1 Introduction | 1.06 | 1.02 | 1.02 |
| 2 Related work | 1.57 | 0.64 | 0.64 |
| 3 Method | 1.63 | 1.47 | 1.47 |
| 4 Data and registered plan | 2.99 | 1.94 | 1.94 |
| 5 Results in Vietnamese | 2.84 | 2.49 | 2.49 |
| 6 English comparison | 2.30 | 1.12 | 1.12 |
| 7 Disclosures and limitations | 1.63 | 1.68 | 1.68 |
| 8 Conclusion | 0.48 | 0.48 | 0.48 |
| End sections | 0.61 | 0.61 | 0.61 |
| References | 2.85 | 2.20 | 2.20 |
| margin not given to a block | | 0.10 | |
| **total** | **18.71** | **14.50** | **14.40** |

The target of each block is the v3 estimate; the blocks sum to 14.40 and the rest up to 14.5 is margin. Section 7 and the end sections cannot shrink (CC-414 Ruling 2: no disclosure or limitation bullet, the compute line and the declarations are never cut). Section 7 grows by about two lines, because its bullet "Not reported here" now names the rows that left.

## 6. How sure the estimate is

- Estimate for the v3 draft with today's placeholders: **14.4 pages of content, that is a 15-page PDF** in the default layout; about 14.5 in the other layout.
- My range: 14.0 to 14.9. Chance that the host build gives 15 pages or fewer with today's placeholders: about 85%. It is not higher because the model was checked against one build only and the page breaks are not modelled.
- The real author block (three authors, addresses, e-mails), one licence entry per data set, the acknowledgment and the interests statement are not in the count. Together they may add 0.2 to 0.4 page. With them the chance of 15 pages or fewer is about 70%. `CUT_PLAN.md` section 5 lists the next cuts, in order, if the build is over.
- The lower limit of 12 pages is not at risk.
