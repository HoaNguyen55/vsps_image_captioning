# Paper A fix package v6

Written 2026-11-15T10:37Z (2026-11-15, 17:37 Vietnam time). Target journal of the paper: Signal Processing: Image Communication.

**What this file is.** Proposed changes for the 15 items that the readiness audit of 2026-11-15 marks NOT READY and fixable by an agent. Each item was checked again in the files before a change was written. Each text change is an exact OLD/NEW pair with its evidence, or a step of the script that is described in Section 4. Nothing has been applied, staged or committed. The package is outcome-free with respect to Section 6.7 and Supplementary S11: it quotes nothing from them, from the abstract body or from the highlights, so no `*_HELD.md` file was needed. The two steps that touch the abstract and the cover letter (T1, V1) are written as patterns, so that the sentences they act on are not printed here.

**Inputs.**
- Audit: `manuscript/READY_AUDIT_A_2026-11-15.md`, sha256 `500de478c594214bac0294bfa3b33c4c1939b0513e8e75160067b6a45c699aab`, read in full.
- Paper: `/mnt/d/vsps_papers/vsps-paperA-spic/paper/`, HEAD `0b542cf` (package v5 applied under CC-416). The working tree of `paper/` is clean.
- Decisions LOG `.session_backup/2026-10-13/decisions/LOG.md`: PI-1026az (l.635), PI-1110o (l.2072), PI-1115i (l.2662), PI-1115k (l.2669), CC-416 (l.2673), read before any declaration was touched. The one block in `declarations.md` (A6-D01) changes the heading only.
- Source files of the numbers: `data/results/a_m1/a_m1_result.json`, `data/results/a_n2/a_n2_run.json`, `data/results/a_n3/a_n3_run.json`, `.session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json` and `c3_n2_exchangeability_all_datasets.json`; `data/results/a_dchecks/` was opened and is not the source of any row.
- Registered addendum `manuscript/prereg/2026-11-11_a_cert/A_CERT_ADDENDUM_VP_v1_1.md`: its headings and the lines that name Part V and Part P, for the two glosses of group L.
- Not opened: any label folder, key file, label file, `gt_cache.json`, `b_text_held`, `b_result_snapshot`, CC-394.txt, CC-396.txt.
- Held zones. Of `sec7_verbosity_sign.md` only lines before `## 6.7` were displayed, and of both supplement files only lines before `## S11`. Scripts read those files whole (to compare bytes, to count words, to list the citation keys of the supplement, and to build the two PDFs in a scratch folder; the PDFs were not opened) and printed none of their text. The abstract body, the cover letter and the highlights were read, because audit items A5-02, A4-02 and A5-05 act on them; this package prints none of their sentences.

**The groups.**
- **Group N (numbers; audit A2-02, A2-03, A2-04, A2-05).** 34 manifest rows (step S1) and 2 unprinted source comments. No printed number changes.
- **Group F (build; audit A3-02, A3-05, A3-07, A5-05).** 2 blocks in the build filter (figure captions; breaks in DOIs printed as text) and one new build script for the supplement PDF and the highlights file (step B1).
- **Group H (audit A3-06).** 46 blocks in Supplementary S1–S10: 29 headings retitled by content and 17 places in notes and caption labels where a revision of the manuscript is named.
- **Group R (audit A2-07).** A reference list for the supplement, appended after its last line (step R1; the list is the file `SUPP_REFERENCES_A_v6.md` of this folder).
- **Group L (audit A4-04).** 2 blocks in Section 9.1: two registered labels glossed where they are used.
- **Group D (audit A5-12).** 1 block: the heading of the declarations.
- **Group T (audit A5-02) and group V (audit A4-02).** Steps T1 and V1: the abstract made to stand alone, and the abstract's sentence on the registered predictions copied into the cover letter.

Section 6.7 and Supplementary S11 stay byte-unchanged; the script asserts it. `sec7_verbosity_sign.md`, `highlights_A.md`, the title page, `sec1_introduction.md` and the anonymised declarations are not written. No statement on AI tools is added and nothing says that no AI tool was used. No agreement clause is touched: the script counts the clauses in every file before and after.

## 1. Counts

- 53 blocks: `supplementary.md` 47 (46 of group H, 1 comment of group N), `build/filter.lua` 2, `sec11_limitations_ethics.md` 2, `sec5_exchangeability.md` 1 (comment), `declarations.md` 1.
- 7 steps that are not blocks (Section 4): S1 (34 manifest rows), R1 (reference list, 98 entries), B1 (new file `build/build_A_supp.sh`), T1 (abstract, three patterns), V1 (cover letter, one sentence), S2 (published supplement and provenance table), S3 (length comment).
- 11 files after the package (Section 7.3): 10 changed, 1 new.
- Audit items: 15 checked; 14 lead to a change, of which 6 in a form other than the audit's (A2-03, A2-05, A2-07, A3-07, A4-04, A5-05); 1 is not a change of text (A6-02). One half of A4-04 and part of A2-05 are dropped (Section 6.1).
- Main text: 19,265 words at HEAD; +22 in Section 9.1 (two glosses), −5 in `declarations.md` (the heading); 19,282 after the package. Nothing is cut. Abstract: 250 words at HEAD, 241 after step T1.

## 2. Table of blocks

| Id | Group | Audit item | File | Line at HEAD | What changes |
|---|---|---|---|---|---|
| A6-N01 | N | A2-03 | `sec5_exchangeability.md` | 43 | Section 5.4: unprinted source comment for the coverage bound |
| A6-N02 | N | A2-05 | `supplementary.md` | 620 | S5, caption of Table S5.M: unprinted source comment for the whole table |
| A6-F01 | F | A3-02 | `build/filter.lua` | 7 | Build filter: figure captions read from `figs/CAPTIONS.md` |
| A6-F02 | F | A3-07 | `build/filter.lua` | 43 | Build filter: line breaks inside DOIs that are printed as text |
| A6-H01 | H | A3-06 | `supplementary.md` | 239 | Heading at source l.239 retitled by content |
| A6-H02 | H | A3-06 | `supplementary.md` | 273 | Heading at source l.273 retitled by content |
| A6-H03 | H | A3-06 | `supplementary.md` | 284 | Heading at source l.284 retitled by content |
| A6-H04 | H | A3-06 | `supplementary.md` | 327 | Heading at source l.327 retitled by content |
| A6-H05 | H | A3-06 | `supplementary.md` | 966 | Heading at source l.966 retitled by content |
| A6-H06 | H | A3-06 | `supplementary.md` | 976 | Heading at source l.976 retitled by content |
| A6-H07 | H | A3-06 | `supplementary.md` | 980 | Heading at source l.980 retitled by content |
| A6-H08 | H | A3-06 | `supplementary.md` | 984 | Heading at source l.984 retitled by content |
| A6-H09 | H | A3-06 | `supplementary.md` | 988 | Heading at source l.988 retitled by content |
| A6-H10 | H | A3-06 | `supplementary.md` | 997 | Heading at source l.997 retitled by content |
| A6-H11 | H | A3-06 | `supplementary.md` | 1001 | Heading at source l.1001 retitled by content |
| A6-H12 | H | A3-06 | `supplementary.md` | 1005 | Heading at source l.1005 retitled by content |
| A6-H13 | H | A3-06 | `supplementary.md` | 1009 | Heading at source l.1009 retitled by content |
| A6-H14 | H | A3-06 | `supplementary.md` | 1013 | Heading at source l.1013 retitled by content |
| A6-H15 | H | A3-06 | `supplementary.md` | 1017 | Heading at source l.1017 retitled by content |
| A6-H16 | H | A3-06 | `supplementary.md` | 1045 | Heading at source l.1045 retitled by content |
| A6-H17 | H | A3-06 | `supplementary.md` | 1055 | Heading at source l.1055 retitled by content |
| A6-H18 | H | A3-06 | `supplementary.md` | 1138 | Heading at source l.1138 retitled by content |
| A6-H19 | H | A3-06 | `supplementary.md` | 1171 | Heading at source l.1171 retitled by content |
| A6-H20 | H | A3-06 | `supplementary.md` | 1202 | Heading at source l.1202 retitled by content |
| A6-H21 | H | A3-06 | `supplementary.md` | 1208 | Heading at source l.1208 retitled by content |
| A6-H22 | H | A3-06 | `supplementary.md` | 1234 | Heading at source l.1234 retitled by content |
| A6-H23 | H | A3-06 | `supplementary.md` | 1242 | Heading at source l.1242 retitled by content |
| A6-H24 | H | A3-06 | `supplementary.md` | 1260 | Heading at source l.1260 retitled by content |
| A6-H25 | H | A3-06 | `supplementary.md` | 1266 | Heading at source l.1266 retitled by content |
| A6-H26 | H | A3-06 | `supplementary.md` | 1284 | Heading at source l.1284 retitled by content |
| A6-H27 | H | A3-06 | `supplementary.md` | 1316 | Heading at source l.1316 retitled by content |
| A6-H28 | H | A3-06 | `supplementary.md` | 1332 | Heading at source l.1332 retitled by content |
| A6-H29 | H | A3-06 | `supplementary.md` | 1344 | Heading at source l.1344 retitled by content |
| A6-H30 | H | A3-06 | `supplementary.md` | 968 | Note or caption label at source l.968: revision wording replaced |
| A6-H31 | H | A3-06 | `supplementary.md` | 968 | Note or caption label at source l.968: revision wording replaced |
| A6-H32 | H | A3-06 | `supplementary.md` | 1021 | Note or caption label at source l.1021: revision wording replaced |
| A6-H33 | H | A3-06 | `supplementary.md` | 1173 | Note or caption label at source l.1173: revision wording replaced |
| A6-H34 | H | A3-06 | `supplementary.md` | 1173 | Note or caption label at source l.1173: revision wording replaced |
| A6-H35 | H | A3-06 | `supplementary.md` | 1187 | Note or caption label at source l.1187: revision wording replaced |
| A6-H36 | H | A3-06 | `supplementary.md` | 1204 | Note or caption label at source l.1204: revision wording replaced |
| A6-H37 | H | A3-06 | `supplementary.md` | 1204 | Note or caption label at source l.1204: revision wording replaced |
| A6-H38 | H | A3-06 | `supplementary.md` | 1204 | Note or caption label at source l.1204: revision wording replaced |
| A6-H39 | H | A3-06 | `supplementary.md` | 1224 | Note or caption label at source l.1224: revision wording replaced |
| A6-H40 | H | A3-06 | `supplementary.md` | 1282 | Note or caption label at source l.1282: revision wording replaced |
| A6-H41 | H | A3-06 | `supplementary.md` | 1298 | Note or caption label at source l.1298: revision wording replaced |
| A6-H42 | H | A3-06 | `supplementary.md` | 1238 | Note or caption label at source l.1238: revision wording replaced |
| A6-H43 | H | A3-06 | `supplementary.md` | 1286 | Note or caption label at source l.1286: revision wording replaced |
| A6-H44 | H | A3-06 | `supplementary.md` | 1286 | Note or caption label at source l.1286: revision wording replaced |
| A6-H45 | H | A3-06 | `supplementary.md` | 1286 | Note or caption label at source l.1286: revision wording replaced |
| A6-H46 | H | A3-06 | `supplementary.md` | 1353 | Note or caption label at source l.1353: revision wording replaced |
| A6-L01 | L | A4-04 | `sec11_limitations_ethics.md` | 25 | Section 9.1: the label Part P glossed at its only use in the main text |
| A6-L02 | L | A4-04 | `sec11_limitations_ethics.md` | 25 | Section 9.1: the label Part V glossed at its only use in the main text |
| A6-D01 | D | A5-12 | `declarations.md` | 1 | Heading of the declarations: the placement note removed |

## 3. Blocks

Each OLD string is given exactly as it stands in the file at HEAD, and each NEW string exactly as it should stand. A marker line is not part of a string; the string is the text between two marker lines, without the line break before the next marker. The strings of A6-F01 and A6-F02 have several lines (A6-F02 ends with a line break, shown as an empty line before the next marker); every other string is a single line. Blocks of one file are applied in the order given.

<<<A6-N01 sec5_exchangeability.md OLD>>>
(Chao, 1987; Supplementary S1.M, S5).
<<<A6-N01 sec5_exchangeability.md NEW>>>
(Chao, 1987; Supplementary S1.M, S5).<!-- src: data/results/a_m1/a_m1_result.json (sha256 5687a66b2078) :: sets.coco5000.descriptive.U.E1.C_hat_5.{point, ci95} = 0.8656 [0.8540, 0.8760]; POST_HOC descriptive, development data; manifest rows of fix package v6 -->
<<<A6-N01 EVIDENCE>>>
Audit A2-03 says no source was located. The source exists: `data/results/a_m1/a_m1_result.json (sha256 5687a66b2078)`, run-repository commit `a245481`, with `sets.coco5000.descriptive.U.E1.C_hat_5.point` = 0.8655522661539696 and `.ci95` = [0.8539986685138505, 0.8759792742077801], which print as 0.866 and 0.854–0.876. The sentence is right; it lacked the comment and the manifest rows (step S1). Unprinted: the script asserts that the printed text of the file is the same before and after. The OLD string is the citation bracket only, so no other word of the paragraph is in this package.

<<<A6-N02 supplementary.md OLD>>>
every bound asymptotic, under (A1); Supplementary S1.M).
<<<A6-N02 supplementary.md NEW>>>
every bound asymptotic, under (A1); Supplementary S1.M).<!-- src: data/results/a_m1/a_m1_result.json (sha256 5687a66b2078) :: sets.{coco5000,uitviic231}.E5.U.{phi_1..phi_5, U}; descriptive.U.E1.{C_hat_5, m_hat_5}; descriptive.L.E1.C_hat_5; V1.{D_L, label}; V2A.{eps_3, label}; descriptive.U.eps.{eps_2, eps_4}; B = 2000; manifest rows of fix package v6 -->
<<<A6-N02 EVIDENCE>>>
Table S5.M (source l.620 and the lines after it) carries no source comment and the manifest has no row from this file (`grep -c a_m1 number_manifest.tsv` = 0). All 34 values of the table were recomputed from the file by a script and found in the printed table as written (rounding half up to three decimals); labels `V1.label` = CONSISTENT (both sets), `V2A.label` = FAIL (COCO-5000) and UNDERPOWERED (UIT-ViIC) equal the printed ones. Unprinted; the published copy is unchanged by this block.

<<<A6-F01 build/filter.lua OLD>>>
local function figure(img)
  return pandoc.RawBlock('latex', string.format(
    '\\begin{figure}[htbp]\\centering\\includegraphics[width=\\linewidth,height=0.8\\textheight,keepaspectratio]{%s}\\par\\smallskip{\\small %s}\\end{figure}',
    img.src:gsub('%.svg$', '.pdf'), pandoc.utils.stringify(img.caption)))
end
<<<A6-F01 build/filter.lua NEW>>>
-- Captions: figs/CAPTIONS.md holds one paragraph per figure that opens with the bold label ("**Fig. 1.**");
-- the alt text of the image ("Fig. 1") selects it. A figure without a caption paragraph stops the build.
local captions = {}
for _, blk in ipairs(pandoc.read(io.open(pandoc.path.directory(PANDOC_SCRIPT_FILE) .. '/../figs/CAPTIONS.md'):read('a'), 'markdown').blocks) do
  local lead = blk.t == 'Para' and blk.content[1]
  if lead and lead.t == 'Strong' then
    captions[(pandoc.utils.stringify(lead):gsub('%.$', ''))] = pandoc.write(pandoc.Pandoc({ pandoc.Plain(blk.content) }), 'latex')
  end
end

local function figure(img)
  local alt = pandoc.utils.stringify(img.caption)
  return pandoc.RawBlock('latex', string.format(
    '\\begin{figure}[htbp]\\centering\\includegraphics[width=\\linewidth,height=0.8\\textheight,keepaspectratio]{%s}\\par\\smallskip{\\small %s}\\end{figure}',
    img.src:gsub('%.svg$', '.pdf'), captions[alt] or error('no caption paragraph in figs/CAPTIONS.md for ' .. alt)))
end
<<<A6-F01 EVIDENCE>>>
Defect confirmed: the filter prints the alt text of the image as the caption, and the alt texts are `Fig. 1`, `Fig. 2`, `Fig. 3` (`sec3_measurement_setup.md` l.15, `sec7_verbosity_sign.md` l.26 and l.92, both before Section 6.7) and `Fig. S1` (`supplementary.md` l.102). The audit offers two fixes; this is the second (the build reads the caption file), so no section file changes, the captions stay in one place and outside the word count, and `sec7_verbosity_sign.md` is not written. Line 3 of `CAPTIONS.md` (internal id and paths) does not open with a bold label and is not read. Tested in a scratch copy of HEAD with this block and A6-F02: `build_A_cas.sh` gives 38 pages, no undefined reference, and the three figure environments of the `.tex` open with `\textbf{Fig. 1.}`, `\textbf{Fig. 2.}`, `\textbf{Fig. 3.}` followed by the caption paragraphs, with math kept as math. A missing caption paragraph now stops the build with an error.

<<<A6-F02 build/filter.lua OLD>>>
function Str(s)

<<<A6-F02 build/filter.lua NEW>>>
function Str(s)
  -- DOIs printed as text (Table 2.1): allow a break after / . _ -
  if s.text:match('^10%.%d%d%d%d+/%S') then
    return pandoc.RawInline('latex', (s.text:gsub('[\\{}#$%%&_^~]', esc):gsub('([/._-])', '%1\\allowbreak{}')))
  end

<<<A6-F02 EVIDENCE>>>
The audit's diagnosis and fix are both wrong, and the item is kept with another fix. (1) `xurl` is already loaded: `build/shims.tex` has `\IfFileExists{xurl.sty}{\usepackage{xurl}}{}` and `kpsewhich xurl.sty` finds it. (2) The wide boxes are not in the reference list: the log places them at lines 500-566 of the built `.tex`, which is Table 2.1 of Section 2, whose first column prints DOIs as plain text (for example `doi 10.52202/079017-3538`). Tested in a scratch copy of HEAD: overfull boxes 23 before, 17 after; wider than 10 pt 11 before, 5 after; the 5 left are all between the heading of Section 6.7 and the next section of the `.tex` (lines 2093-2109) and are not touched. The largest box left outside Section 6.7 is 5.7 pt (one word in Table 2.1). Rendering only: the words of the paper are unchanged.

<<<A6-H01 supplementary.md OLD>>>
### Data, fidelity and specification curve (moved from the main text in revision 1)
<<<A6-H01 supplementary.md NEW>>>
### Data, fidelity and specification curve
<<<A6-H01 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.239. The content title is kept; only the bracket goes. The words under the heading are unchanged.

<<<A6-H02 supplementary.md OLD>>>
### Material moved from Section 6 in revision 1
<<<A6-H02 supplementary.md NEW>>>
### Count controls, placebos and positive controls
<<<A6-H02 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.273. Retitled by content: the subsection opens with the count-effect paragraph and holds the sub-heading on placebos and positive controls. No section number is given, because the number in the old heading is that of an older numbering. The words under the heading are unchanged.

<<<A6-H03 supplementary.md OLD>>>
#### Placebos and positive controls (old Section 6.3)
<<<A6-H03 supplementary.md NEW>>>
#### Placebos and positive controls
<<<A6-H03 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.284. Only the bracket goes. The words under the heading are unchanged.

<<<A6-H04 supplementary.md OLD>>>
### Table S4.0: full registration ledger (moved from Section 1.2 in revision 1)
<<<A6-H04 supplementary.md NEW>>>
### Table S4.0: full registration ledger
<<<A6-H04 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.327. Only the bracket goes. The words under the heading are unchanged.

<<<A6-H05 supplementary.md OLD>>>
### Material moved from Section 6 in revision 2
<<<A6-H05 supplementary.md NEW>>>
### Extended text for Sections 6.2 to 6.6
<<<A6-H05 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.966. Its sub-headings cover Sections 6.2 to 6.6; S7 already has a heading "Further detail for Section 6" (l.877), so that name is not reused. The words under the heading are unchanged.

<<<A6-H06 supplementary.md OLD>>>
#### Moved from Section 6.2 (revision 2, for length)
<<<A6-H06 supplementary.md NEW>>>
#### Extended text for Section 6.2
<<<A6-H06 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.976. The section number was checked against the headings of the main text (`sec7_verbosity_sign.md` l.43-102: 6.2 XM3600, 6.3 second backbone, 6.4 PASCAL-50S and COCO val2017, 6.5 system-level robustness, 6.6 mechanism check) and against the first words of the paragraph under the heading. The words under the heading are unchanged.

<<<A6-H07 supplementary.md OLD>>>
#### Moved from Section 6.3 primary result (revision 2, for length)
<<<A6-H07 supplementary.md NEW>>>
#### Extended text for Section 6.3: primary result
<<<A6-H07 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.980. The section number was checked against the headings of the main text (`sec7_verbosity_sign.md` l.43-102: 6.2 XM3600, 6.3 second backbone, 6.4 PASCAL-50S and COCO val2017, 6.5 system-level robustness, 6.6 mechanism check) and against the first words of the paragraph under the heading. The words under the heading are unchanged.

<<<A6-H08 supplementary.md OLD>>>
#### Moved from Section 6.3, truncation (revision 2, for length)
<<<A6-H08 supplementary.md NEW>>>
#### Extended text for Section 6.3: truncation
<<<A6-H08 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.984. The section number was checked against the headings of the main text (`sec7_verbosity_sign.md` l.43-102: 6.2 XM3600, 6.3 second backbone, 6.4 PASCAL-50S and COCO val2017, 6.5 system-level robustness, 6.6 mechanism check) and against the first words of the paragraph under the heading. The words under the heading are unchanged.

<<<A6-H09 supplementary.md OLD>>>
#### Moved from Section 6.3 secondary (revision 2, for length)
<<<A6-H09 supplementary.md NEW>>>
#### Extended text for Section 6.3: secondary claims
<<<A6-H09 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.988. The section number was checked against the headings of the main text (`sec7_verbosity_sign.md` l.43-102: 6.2 XM3600, 6.3 second backbone, 6.4 PASCAL-50S and COCO val2017, 6.5 system-level robustness, 6.6 mechanism check) and against the first words of the paragraph under the heading. The words under the heading are unchanged.

<<<A6-H10 supplementary.md OLD>>>
#### Moved from Section 6.3 eight LVLMs (revision 2, for length)
<<<A6-H10 supplementary.md NEW>>>
#### Extended text for Section 6.3: eight LVLMs
<<<A6-H10 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.997. The section number was checked against the headings of the main text (`sec7_verbosity_sign.md` l.43-102: 6.2 XM3600, 6.3 second backbone, 6.4 PASCAL-50S and COCO val2017, 6.5 system-level robustness, 6.6 mechanism check) and against the first words of the paragraph under the heading. The words under the heading are unchanged.

<<<A6-H11 supplementary.md OLD>>>
#### Moved from Section 6.4 design (revision 2, for length)
<<<A6-H11 supplementary.md NEW>>>
#### Extended text for Section 6.4: design
<<<A6-H11 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.1001. The section number was checked against the headings of the main text (`sec7_verbosity_sign.md` l.43-102: 6.2 XM3600, 6.3 second backbone, 6.4 PASCAL-50S and COCO val2017, 6.5 system-level robustness, 6.6 mechanism check) and against the first words of the paragraph under the heading. The words under the heading are unchanged.

<<<A6-H12 supplementary.md OLD>>>
#### Moved from Section 6.4 P50-O2 bullet (revision 2, for length)
<<<A6-H12 supplementary.md NEW>>>
#### Extended text for Section 6.4: the P50-O2 bullet
<<<A6-H12 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.1005. The section number was checked against the headings of the main text (`sec7_verbosity_sign.md` l.43-102: 6.2 XM3600, 6.3 second backbone, 6.4 PASCAL-50S and COCO val2017, 6.5 system-level robustness, 6.6 mechanism check) and against the first words of the paragraph under the heading. The words under the heading are unchanged.

<<<A6-H13 supplementary.md OLD>>>
#### Moved from Section 6.4 without a verdict (revision 2, for length)
<<<A6-H13 supplementary.md NEW>>>
#### Extended text for Section 6.4: without a verdict
<<<A6-H13 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.1009. The section number was checked against the headings of the main text (`sec7_verbosity_sign.md` l.43-102: 6.2 XM3600, 6.3 second backbone, 6.4 PASCAL-50S and COCO val2017, 6.5 system-level robustness, 6.6 mechanism check) and against the first words of the paragraph under the heading. The words under the heading are unchanged.

<<<A6-H14 supplementary.md OLD>>>
#### Moved from Section 6.4 system dependence (revision 2, for length)
<<<A6-H14 supplementary.md NEW>>>
#### Extended text for Section 6.4: system dependence
<<<A6-H14 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.1013. The section number was checked against the headings of the main text (`sec7_verbosity_sign.md` l.43-102: 6.2 XM3600, 6.3 second backbone, 6.4 PASCAL-50S and COCO val2017, 6.5 system-level robustness, 6.6 mechanism check) and against the first words of the paragraph under the heading. The words under the heading are unchanged.

<<<A6-H15 supplementary.md OLD>>>
#### Moved from Section 6.5 (whole section body, with Table 6.3, now Table S7.8) (revision 2, for length)
<<<A6-H15 supplementary.md NEW>>>
#### Extended text for Section 6.5 (whole section body, with Table S7.8)
<<<A6-H15 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.1017. The section number was checked against the headings of the main text (`sec7_verbosity_sign.md` l.43-102: 6.2 XM3600, 6.3 second backbone, 6.4 PASCAL-50S and COCO val2017, 6.5 system-level robustness, 6.6 mechanism check) and against the first words of the paragraph under the heading. The words under the heading are unchanged.

<<<A6-H16 supplementary.md OLD>>>
#### Moved from Section 6.6 closing paragraphs (revision 2, for length)
<<<A6-H16 supplementary.md NEW>>>
#### Extended text for Section 6.6: closing paragraphs
<<<A6-H16 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.1045. The section number was checked against the headings of the main text (`sec7_verbosity_sign.md` l.43-102: 6.2 XM3600, 6.3 second backbone, 6.4 PASCAL-50S and COCO val2017, 6.5 system-level robustness, 6.6 mechanism check) and against the first words of the paragraph under the heading. The words under the heading are unchanged.

<<<A6-H17 supplementary.md OLD>>>
### Material moved from Section 8.3 in revision 1
<<<A6-H17 supplementary.md NEW>>>
### Short captions, long paragraphs and preference data: full text
<<<A6-H17 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.1055. Retitled by content: the subsection gives the full text behind Section 7.3, whose title in the main text is "Short captions, long paragraphs and preference data (summary)". The number 8.3 of the old heading is that of an older numbering. The words under the heading are unchanged.

<<<A6-H18 supplementary.md OLD>>>
## S9 Related work: details moved from Section 2
<<<A6-H18 supplementary.md NEW>>>
## S9 Related work: further detail for Section 2
<<<A6-H18 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.1138. The section number S9 and the pointers to it are unchanged. The words under the heading are unchanged.

<<<A6-H19 supplementary.md OLD>>>
### Material moved from Section 2 in revision 2
<<<A6-H19 supplementary.md NEW>>>
### Longer wording of Section 2
<<<A6-H19 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.1171. The section number was checked against the headings of the main text (`sec7_verbosity_sign.md` l.43-102: 6.2 XM3600, 6.3 second backbone, 6.4 PASCAL-50S and COCO val2017, 6.5 system-level robustness, 6.6 mechanism check) and against the first words of the paragraph under the heading. The words under the heading are unchanged.

<<<A6-H20 supplementary.md OLD>>>
## S10 Material moved from the main text in revision 2
<<<A6-H20 supplementary.md NEW>>>
## S10 Extended text for Sections 1–9
<<<A6-H20 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.1202. The title the audit proposes. The section number S10 and the pointers to it are unchanged; no visible text of the paper refers to S10 by its title. The words under the heading are unchanged.

<<<A6-H21 supplementary.md OLD>>>
### From Section 1
<<<A6-H21 supplementary.md NEW>>>
### Extended text for Section 1
<<<A6-H21 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.1208. Not "Further detail for Section 1", as the audit proposes: headings of that form exist in S1, S2, S5, S7 and S8, and S10 l.1286 points to one of them by its title. The words under the heading are unchanged.

<<<A6-H22 supplementary.md OLD>>>
### From Section 2
<<<A6-H22 supplementary.md NEW>>>
### Extended text for Section 2
<<<A6-H22 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.1234. Not "Further detail for Section 2", as the audit proposes: headings of that form exist in S1, S2, S5, S7 and S8, and S10 l.1286 points to one of them by its title. The words under the heading are unchanged.

<<<A6-H23 supplementary.md OLD>>>
### From Section 3
<<<A6-H23 supplementary.md NEW>>>
### Extended text for Section 3
<<<A6-H23 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.1242. Not "Further detail for Section 3", as the audit proposes: headings of that form exist in S1, S2, S5, S7 and S8, and S10 l.1286 points to one of them by its title. The words under the heading are unchanged.

<<<A6-H24 supplementary.md OLD>>>
### From Section 4
<<<A6-H24 supplementary.md NEW>>>
### Extended text for Section 4
<<<A6-H24 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.1260. Not "Further detail for Section 4", as the audit proposes: headings of that form exist in S1, S2, S5, S7 and S8, and S10 l.1286 points to one of them by its title. The words under the heading are unchanged.

<<<A6-H25 supplementary.md OLD>>>
### From Section 5
<<<A6-H25 supplementary.md NEW>>>
### Extended text for Section 5
<<<A6-H25 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.1266. Not "Further detail for Section 5", as the audit proposes: headings of that form exist in S1, S2, S5, S7 and S8, and S10 l.1286 points to one of them by its title. The words under the heading are unchanged.

<<<A6-H26 supplementary.md OLD>>>
### From Section 6
<<<A6-H26 supplementary.md NEW>>>
### Extended text for Section 6
<<<A6-H26 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.1284. Not "Further detail for Section 6", as the audit proposes: headings of that form exist in S1, S2, S5, S7 and S8, and S10 l.1286 points to one of them by its title. The words under the heading are unchanged.

<<<A6-H27 supplementary.md OLD>>>
### From Section 7
<<<A6-H27 supplementary.md NEW>>>
### Extended text for Section 7
<<<A6-H27 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.1316. Not "Further detail for Section 7", as the audit proposes: headings of that form exist in S1, S2, S5, S7 and S8, and S10 l.1286 points to one of them by its title. The words under the heading are unchanged.

<<<A6-H28 supplementary.md OLD>>>
### From Section 8
<<<A6-H28 supplementary.md NEW>>>
### Extended text for Section 8
<<<A6-H28 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.1332. Not "Further detail for Section 8", as the audit proposes: headings of that form exist in S1, S2, S5, S7 and S8, and S10 l.1286 points to one of them by its title. The words under the heading are unchanged.

<<<A6-H29 supplementary.md OLD>>>
### From Section 9
<<<A6-H29 supplementary.md NEW>>>
### Extended text for Section 9
<<<A6-H29 EVIDENCE>>>
Audit A3-06, confirmed: the heading names a revision of the manuscript, which a reader of a first submission has not seen. Source l.1344. Not "Further detail for Section 9", as the audit proposes: headings of that form exist in S1, S2, S5, S7 and S8, and S10 l.1286 points to one of them by its title. The words under the heading are unchanged.

<<<A6-H30 supplementary.md OLD>>>
*Paragraphs in this subsection are the pre-revision-2 main-text wording. Their
<<<A6-H30 supplementary.md NEW>>>
*Paragraphs in this subsection give an earlier, longer wording of the main text. Their
<<<A6-H30 EVIDENCE>>>
Audit A3-06, confirmed: the note dates the text by a revision of the manuscript. The new words keep what the note discloses (the paragraphs are an earlier, longer wording; what was corrected since) and drop the revision number. Source l.968. 

<<<A6-H31 supplementary.md OLD>>>
(Table 6.2 before revision 2 is Table S7.5, Table 6.3 before revision 2 is Table S7.8;
<<<A6-H31 supplementary.md NEW>>>
(Tables 6.2 and 6.3 of that wording are Tables S7.5 and S7.8;
<<<A6-H31 EVIDENCE>>>
Audit A3-06, confirmed: the note dates the text by a revision of the manuscript. The new words keep what the note discloses (the paragraphs are an earlier, longer wording; what was corrected since) and drop the revision number. Source l.968. Same mapping of the two tables, said once.

<<<A6-H32 supplementary.md OLD>>>
(Table 6.3 before revision 2)
<<<A6-H32 supplementary.md NEW>>>
(Table 6.3 of the earlier wording)
<<<A6-H32 EVIDENCE>>>
Audit A3-06, confirmed: the note dates the text by a revision of the manuscript. The new words keep what the note discloses (the paragraphs are an earlier, longer wording; what was corrected since) and drop the revision number. Source l.1021. Caption of Table S7.8.

<<<A6-H33 supplementary.md OLD>>>
are the pre-revision-2 main-text wording of Section 2,
<<<A6-H33 supplementary.md NEW>>>
give an earlier, longer wording of Section 2,
<<<A6-H33 EVIDENCE>>>
Audit A3-06, confirmed: the note dates the text by a revision of the manuscript. The new words keep what the note discloses (the paragraphs are an earlier, longer wording; what was corrected since) and drop the revision number. Source l.1173. 

<<<A6-H34 supplementary.md OLD>>>
Table S9.1 is Table 2.1 before revision 2,
<<<A6-H34 supplementary.md NEW>>>
Table S9.1 is Table 2.1 of that wording,
<<<A6-H34 EVIDENCE>>>
Audit A3-06, confirmed: the note dates the text by a revision of the manuscript. The new words keep what the note discloses (the paragraphs are an earlier, longer wording; what was corrected since) and drop the revision number. Source l.1173. 

<<<A6-H35 supplementary.md OLD>>>
(Table 2.1 before revision 2)
<<<A6-H35 supplementary.md NEW>>>
(Table 2.1 of the earlier wording)
<<<A6-H35 EVIDENCE>>>
Audit A3-06, confirmed: the note dates the text by a revision of the manuscript. The new words keep what the note discloses (the paragraphs are an earlier, longer wording; what was corrected since) and drop the revision number. Source l.1187. Caption of Table S9.1.

<<<A6-H36 supplementary.md OLD>>>
*Paragraphs in this section are the pre-revision-2 main-text wording, kept verbatim
<<<A6-H36 supplementary.md NEW>>>
*Paragraphs in this section give an earlier, longer wording of the main text, kept verbatim
<<<A6-H36 EVIDENCE>>>
Audit A3-06, confirmed: the note dates the text by a revision of the manuscript. The new words keep what the note discloses (the paragraphs are an earlier, longer wording; what was corrected since) and drop the revision number. Source l.1204. The rest of the note (what is replaced by pointers, what follows the corrected wording, the two statements that predate later results) is unchanged.

<<<A6-H37 supplementary.md OLD>>>
the pre-revision-2 "Position of this paper" paragraph
<<<A6-H37 supplementary.md NEW>>>
the earlier "Position of this paper" paragraph
<<<A6-H37 EVIDENCE>>>
Audit A3-06, confirmed: the note dates the text by a revision of the manuscript. The new words keep what the note discloses (the paragraphs are an earlier, longer wording; what was corrected since) and drop the revision number. Source l.1204. 

<<<A6-H38 supplementary.md OLD>>>
Captions marked "pre-revision" are
<<<A6-H38 supplementary.md NEW>>>
Captions marked "earlier caption" are
<<<A6-H38 EVIDENCE>>>
Audit A3-06, confirmed: the note dates the text by a revision of the manuscript. The new words keep what the note discloses (the paragraphs are an earlier, longer wording; what was corrected since) and drop the revision number. Source l.1204. Goes with the three caption labels of A6-H39 to A6-H41.

<<<A6-H39 supplementary.md OLD>>>
**Pre-revision caption of Table 1.**
<<<A6-H39 supplementary.md NEW>>>
**Earlier caption of Table 1.**
<<<A6-H39 EVIDENCE>>>
Audit A3-06, confirmed: the note dates the text by a revision of the manuscript. The new words keep what the note discloses (the paragraphs are an earlier, longer wording; what was corrected since) and drop the revision number. Source l.1224. Label of the caption only; the caption text is unchanged.

<<<A6-H40 supplementary.md OLD>>>
**Pre-revision caption of Table 5.1.**
<<<A6-H40 supplementary.md NEW>>>
**Earlier caption of Table 5.1.**
<<<A6-H40 EVIDENCE>>>
Audit A3-06, confirmed: the note dates the text by a revision of the manuscript. The new words keep what the note discloses (the paragraphs are an earlier, longer wording; what was corrected since) and drop the revision number. Source l.1282. Label of the caption only; the caption text is unchanged.

<<<A6-H41 supplementary.md OLD>>>
**Pre-revision caption of Table 6.1.**
<<<A6-H41 supplementary.md NEW>>>
**Earlier caption of Table 6.1.**
<<<A6-H41 EVIDENCE>>>
Audit A3-06, confirmed: the note dates the text by a revision of the manuscript. The new words keep what the note discloses (the paragraphs are an earlier, longer wording; what was corrected since) and drop the revision number. Source l.1298. Label of the caption only; the caption text is unchanged.

<<<A6-H42 supplementary.md OLD>>>
The pre-revision-2 wording of this paragraph
<<<A6-H42 supplementary.md NEW>>>
The earlier wording of this paragraph
<<<A6-H42 EVIDENCE>>>
Audit A3-06, confirmed: the note dates the text by a revision of the manuscript. The new words keep what the note discloses (the paragraphs are an earlier, longer wording; what was corrected since) and drop the revision number. Source l.1238. 

<<<A6-H43 supplementary.md OLD>>>
*The pre-revision COCO-5000,
<<<A6-H43 supplementary.md NEW>>>
*The earlier COCO-5000,
<<<A6-H43 EVIDENCE>>>
Audit A3-06, confirmed: the note dates the text by a revision of the manuscript. The new words keep what the note discloses (the paragraphs are an earlier, longer wording; what was corrected since) and drop the revision number. Source l.1286. 

<<<A6-H44 supplementary.md OLD>>>
and the pre-revision Table 6.2 are not
<<<A6-H44 supplementary.md NEW>>>
and the earlier Table 6.2 are not
<<<A6-H44 EVIDENCE>>>
Audit A3-06, confirmed: the note dates the text by a revision of the manuscript. The new words keep what the note discloses (the paragraphs are an earlier, longer wording; what was corrected since) and drop the revision number. Source l.1286. 

<<<A6-H45 supplementary.md OLD>>>
every value of the pre-revision Table 6.2.
<<<A6-H45 supplementary.md NEW>>>
every value of the earlier Table 6.2.
<<<A6-H45 EVIDENCE>>>
Audit A3-06, confirmed: the note dates the text by a revision of the manuscript. The new words keep what the note discloses (the paragraphs are an earlier, longer wording; what was corrected since) and drop the revision number. Source l.1286. 

<<<A6-H46 supplementary.md OLD>>>
*The pre-revision "PASCAL-50S outputs" paragraph
<<<A6-H46 supplementary.md NEW>>>
*The earlier "PASCAL-50S outputs" paragraph
<<<A6-H46 EVIDENCE>>>
Audit A3-06, confirmed: the note dates the text by a revision of the manuscript. The new words keep what the note discloses (the paragraphs are an earlier, longer wording; what was corrected since) and drop the revision number. Source l.1353. 

<<<A6-L01 sec11_limitations_ethics.md OLD>>>
on the released image sets of Part P and is not checked
<<<A6-L01 sec11_limitations_ethics.md NEW>>>
on the released image sets of Part P (the application of the certificate to 15 published comparisons, Supplementary S11.6) and is not checked
<<<A6-L01 EVIDENCE>>>
Audit A4-04, confirmed for this line: "Part P" is printed once in the main text (l.25) and defined there nowhere. The label is registered, so it stays; a gloss is added instead of the audit's replacement. Registered addendum `manuscript/prereg/2026-11-11_a_cert/A_CERT_ADDENDUM_VP_v1_1.md`, title line: "(V) a development re-computation of the certificate against a fuller gold on COCO-5000 and (P) its application to 15 published comparisons". Place: `number_manifest.tsv` has 1,283 rows whose status carries both "supp S11.6" and "Part P label", and none that pairs Part P with S11.5. Nothing of S11 was read for this block.

<<<A6-L02 sec11_limitations_ethics.md OLD>>>
the instance-only rows of Part V
<<<A6-L02 sec11_limitations_ethics.md NEW>>>
the instance-only rows of Part V (the development re-computation against a fuller gold on COCO-5000, Supplementary S11.5)
<<<A6-L02 EVIDENCE>>>
As A6-L01. Registered addendum `manuscript/prereg/2026-11-11_a_cert/A_CERT_ADDENDUM_VP_v1_1.md`, title line: "(V) a development re-computation of the certificate against a fuller gold on COCO-5000 and (P) its application to 15 published comparisons". Place: 118 manifest rows carry both "supp S11.5" and "Part V label", none pairs Part V with S11.6; row D-2 of Table S4.0 (published supplement l.321) sends the Part V check on COCO-5000 to S11.5.

<<<A6-D01 declarations.md OLD>>>
# Declarations (placed immediately before the references)
<<<A6-D01 declarations.md NEW>>>
# Declarations
<<<A6-D01 EVIDENCE>>>
Audit A5-12, confirmed: l.1 is a level-1 heading and `build_A_cas.sh` passes `md/declarations.md` to pandoc after the sections, so the bracket is printed in the PDF. The placement is fixed by the build order, not by the note. The agreement clauses of the file are in l.19 and are not touched (counted before and after by the script: 3 and 3). The anonymised copy has the same kind of note in its heading; it is not built for this journal (single-anonymized) and is left as it is (CC-407 N8 open).

## 4. Steps that are not blocks

**S1. Manifest rows** (audit A2-02, A2-03, A2-04, A2-05). 34 rows appended to `number_manifest.tsv`, tab-separated, six columns as in the file:

```
[0.366, 0.403] (UIT-ViIC VI all splits adjacency share CI)	A	.session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json	B2_L2_exchangeability.datasets.uitviic_vi_all_objects_in.adjacent_share_ci95	3d79842d4f2c	keyed (95% interval of a Table 5.1 / Supplementary S5 row; audit A2-02, A2-05; fix package v6)
[-0.015, -0.002] (UIT-ViIC VI all splits lag-1 Jaccard excess CI)	A	.session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json	B2_L2_exchangeability.datasets.uitviic_vi_all_objects_in.jac_diff_ci95	3d79842d4f2c	keyed (95% interval of a Table 5.1 / Supplementary S5 row; audit A2-05; fix package v6)
[0.380, 0.429] (UIT-ViIC images, COCO EN references adjacency share CI)	A	.session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json	B2_L2_exchangeability.datasets.uitviic_images_coco_en_refs_coco80.adjacent_share_ci95	3d79842d4f2c	keyed (95% interval of a Table 5.1 / Supplementary S5 row; audit A2-02, A2-05; fix package v6)
[-0.001, +0.011] (UIT-ViIC images, COCO EN references lag-1 Jaccard excess CI)	A	.session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json	B2_L2_exchangeability.datasets.uitviic_images_coco_en_refs_coco80.jac_diff_ci95	3d79842d4f2c	keyed (95% interval of a Table 5.1 / Supplementary S5 row; audit A2-05; fix package v6)
[0.478, 0.488] (Flickr30k Entities chains adjacency share CI)	A	.session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json	B2_L2_exchangeability.datasets.flickr30k_entities_chains_visual.adjacent_share_ci95	3d79842d4f2c	keyed (95% interval of a Table 5.1 / Supplementary S5 row; audit A2-02, A2-05; fix package v6)
[+0.053, +0.056] (Flickr30k Entities chains lag-1 Jaccard excess CI)	A	.session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json	B2_L2_exchangeability.datasets.flickr30k_entities_chains_visual.jac_diff_ci95	3d79842d4f2c	keyed (95% interval of a Table 5.1 / Supplementary S5 row; audit A2-05; fix package v6)
[0.385, 0.470] (UIT-OpenViIC panel first five adjacency share CI)	A	.session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json	B2_L2_exchangeability.datasets.openviic_panel_first5_objects_in.adjacent_share_ci95	3d79842d4f2c	keyed (95% interval of a Table 5.1 / Supplementary S5 row; audit A2-02, A2-05; fix package v6)
[-0.014, +0.018] (UIT-OpenViIC panel first five lag-1 Jaccard excess CI)	A	.session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json	B2_L2_exchangeability.datasets.openviic_panel_first5_objects_in.jac_diff_ci95	3d79842d4f2c	keyed (95% interval of a Table 5.1 / Supplementary S5 row; audit A2-05; fix package v6)
[0.401, 0.519] (UIT-OpenViIC panel exactly five adjacency share CI)	A	.session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json	B2_L2_exchangeability.datasets.openviic_panel_exact5_objects_in.adjacent_share_ci95	3d79842d4f2c	keyed (95% interval of a Table 5.1 / Supplementary S5 row; audit A2-02, A2-05; fix package v6)
[-0.013, +0.029] (UIT-OpenViIC panel exactly five lag-1 Jaccard excess CI)	A	.session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json	B2_L2_exchangeability.datasets.openviic_panel_exact5_objects_in.jac_diff_ci95	3d79842d4f2c	keyed (95% interval of a Table 5.1 / Supplementary S5 row; audit A2-05; fix package v6)
[0.440, 0.466] (Flickr30k captions, COCO-80 matcher adjacency share CI)	A	.session_backup/2026-10-14/r11_verify/c3_n2_exchangeability_all_datasets.json	k5_exchangeability_audit.flickr30k_captions_coco80.adjacent_share_ci95	abc04948644a	keyed (95% interval of a Table 5.1 / Supplementary S5 row; audit A2-05; fix package v6)
[0.458, 0.498] (UIT-OpenViIC full test exactly five adjacency share CI)	A	.session_backup/2026-10-14/r11_verify/c3_n2_exchangeability_all_datasets.json	k5_exchangeability_audit.openviic_full_test_exact5_objects_in.adjacent_share_ci95	abc04948644a	keyed (95% interval of a Table 5.1 / Supplementary S5 row; audit A2-05; fix package v6)
0.478 (exponent b, COCO one reference)	A	.session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json	B1_L1_mstar_and_stopping.check_coco_gold.refs1_firstk.b	3d79842d4f2c	keyed (supp S1; audit A2-05; fix package v6)
0.9 (A-N2 ranking rule: PASS if the upper bound is below it)	A	data/results/a_n2/a_n2_run.json	config.tau0	1f6ce422e016	keyed (registered rule constant; supp S7; audit A2-05; fix package v6)
3,419 (A-N3 COCO-2014 images of the analysis set)	A	data/results/a_n3/a_n3_run.json	checks.analysis_set.reproduced.images_analysis	7a5a614d2068	keyed (sec8 §7.2, supp S10; audit A2-04; fix package v6)
2,356; 1,376; 1,287; 1,740; 3,629 (COCO-5000 pairs named by 1..5 references)	A	data/results/a_m1/a_m1_result.json	sets.coco5000.E5.U.phi_1..phi_5	5687a66b2078	keyed (POST_HOC descriptive; development data; run status BOUND_ONLY; supp Table S5.M; audit A2-03, A2-05; fix package v6)
10,388 (COCO-5000 pairs in the five-reference union gold)	A	data/results/a_m1/a_m1_result.json	sets.coco5000.E5.U.U	5687a66b2078	keyed (POST_HOC descriptive; development data; run status BOUND_ONLY; supp Table S5.M; audit A2-03, A2-05; fix package v6)
0.866 [0.854, 0.876] (COCO-5000 C_hat_5, upper bound on coverage)	A	data/results/a_m1/a_m1_result.json	sets.coco5000.descriptive.U.E1.C_hat_5.{point,ci95}	5687a66b2078	keyed (POST_HOC descriptive; development data; run status BOUND_ONLY; supp Table S5.M; sec5 §5.4; audit A2-03, A2-05; fix package v6)
0.134 [0.124, 0.146] (COCO-5000 m_hat_5, lower bound on the missing share)	A	data/results/a_m1/a_m1_result.json	sets.coco5000.descriptive.U.E1.m_hat_5.{point,ci95}	5687a66b2078	keyed (POST_HOC descriptive; development data; run status BOUND_ONLY; supp Table S5.M; audit A2-03, A2-05; fix package v6)
0.927 [0.918, 0.934] (COCO-5000 C_hat_5 restricted to labelled classes)	A	data/results/a_m1/a_m1_result.json	sets.coco5000.descriptive.L.E1.C_hat_5.{point,ci95}	5687a66b2078	keyed (POST_HOC descriptive; development data; run status BOUND_ONLY; supp Table S5.M; audit A2-03, A2-05; fix package v6)
0.332 [0.321, 0.343] (COCO-5000 D_L check against labels; label CONSISTENT)	A	data/results/a_m1/a_m1_result.json	sets.coco5000.V1.D_L.{point,ci95}	5687a66b2078	keyed (POST_HOC descriptive; development data; run status BOUND_ONLY; supp Table S5.M; audit A2-03, A2-05; fix package v6)
-0.325 [-0.339, -0.312] (COCO-5000 eps_3, three-to-five-reference check; label FAIL)	A	data/results/a_m1/a_m1_result.json	sets.coco5000.V2A.eps_3.{point,ci95}	5687a66b2078	keyed (POST_HOC descriptive; development data; run status BOUND_ONLY; supp Table S5.M; audit A2-03, A2-05; fix package v6)
-0.746 [-0.754, -0.737] (COCO-5000 eps_2, descriptive)	A	data/results/a_m1/a_m1_result.json	sets.coco5000.descriptive.U.eps.eps_2.{point,ci95}	5687a66b2078	keyed (POST_HOC descriptive; development data; run status BOUND_ONLY; supp Table S5.M; audit A2-03, A2-05; fix package v6)
-0.101 [-0.111, -0.091] (COCO-5000 eps_4, descriptive)	A	data/results/a_m1/a_m1_result.json	sets.coco5000.descriptive.U.eps.eps_4.{point,ci95}	5687a66b2078	keyed (POST_HOC descriptive; development data; run status BOUND_ONLY; supp Table S5.M; audit A2-03, A2-05; fix package v6)
61; 67; 45; 48; 208 (UIT-ViIC-231 pairs named by 1..5 references)	A	data/results/a_m1/a_m1_result.json	sets.uitviic231.E5.U.phi_1..phi_5	5687a66b2078	keyed (POST_HOC descriptive; development data; run status BOUND_ONLY; supp Table S5.M; audit A2-03, A2-05; fix package v6)
429 (UIT-ViIC-231 pairs in the five-reference union gold)	A	data/results/a_m1/a_m1_result.json	sets.uitviic231.E5.U.U	5687a66b2078	keyed (POST_HOC descriptive; development data; run status BOUND_ONLY; supp Table S5.M; audit A2-03, A2-05; fix package v6)
0.951 [0.920, 0.972] (UIT-ViIC-231 C_hat_5, upper bound on coverage)	A	data/results/a_m1/a_m1_result.json	sets.uitviic231.descriptive.U.E1.C_hat_5.{point,ci95}	5687a66b2078	keyed (POST_HOC descriptive; development data; run status BOUND_ONLY; supp Table S5.M; audit A2-03, A2-05; fix package v6)
0.049 [0.028, 0.080] (UIT-ViIC-231 m_hat_5, lower bound on the missing share)	A	data/results/a_m1/a_m1_result.json	sets.uitviic231.descriptive.U.E1.m_hat_5.{point,ci95}	5687a66b2078	keyed (POST_HOC descriptive; development data; run status BOUND_ONLY; supp Table S5.M; audit A2-03, A2-05; fix package v6)
0.952 [0.923, 0.972] (UIT-ViIC-231 C_hat_5 restricted to labelled classes)	A	data/results/a_m1/a_m1_result.json	sets.uitviic231.descriptive.L.E1.C_hat_5.{point,ci95}	5687a66b2078	keyed (POST_HOC descriptive; development data; run status BOUND_ONLY; supp Table S5.M; audit A2-03, A2-05; fix package v6)
0.463 [0.427, 0.494] (UIT-ViIC-231 D_L check against labels; label CONSISTENT)	A	data/results/a_m1/a_m1_result.json	sets.uitviic231.V1.D_L.{point,ci95}	5687a66b2078	keyed (POST_HOC descriptive; development data; run status BOUND_ONLY; supp Table S5.M; audit A2-03, A2-05; fix package v6)
-0.186 [-0.266, -0.080] (UIT-ViIC-231 eps_3, three-to-five-reference check; label UNDERPOWERED)	A	data/results/a_m1/a_m1_result.json	sets.uitviic231.V2A.eps_3.{point,ci95}	5687a66b2078	keyed (POST_HOC descriptive; development data; run status BOUND_ONLY; supp Table S5.M; audit A2-03, A2-05; fix package v6)
-0.805 [-0.832, -0.771] (UIT-ViIC-231 eps_2, descriptive)	A	data/results/a_m1/a_m1_result.json	sets.uitviic231.descriptive.U.eps.eps_2.{point,ci95}	5687a66b2078	keyed (POST_HOC descriptive; development data; run status BOUND_ONLY; supp Table S5.M; audit A2-03, A2-05; fix package v6)
-0.026 [-0.098, 0.067] (UIT-ViIC-231 eps_4, descriptive)	A	data/results/a_m1/a_m1_result.json	sets.uitviic231.descriptive.U.eps.eps_4.{point,ci95}	5687a66b2078	keyed (POST_HOC descriptive; development data; run status BOUND_ONLY; supp Table S5.M; audit A2-03, A2-05; fix package v6)
2,000 (bootstrap resamples, Table S5.M)	A	data/results/a_m1/a_m1_result.json	sets.{coco5000,uitviic231}.B	5687a66b2078	keyed (POST_HOC descriptive; development data; run status BOUND_ONLY; supp Table S5.M; audit A2-03, A2-05; fix package v6)
```

How the rows were checked: a script (not part of the package) read each key from the source file, rounded half up to the printed decimals, and required the printed form to stand in the paper as written (Table 5.1 of Section 5.2, the two tables of Supplementary S5, Table S5.M, S1, S7, Section 7.2). The apply script checks six columns per row and that the sha256 prefix of the row equals the source file in the run repository. What the audit asked and what was found:
- A2-02 (the two Flickr30k bounds): confirmed. The manifest holds the point value of each row of Table 5.1 and of the S5 table, but an interval only for one row (UIT-ViIC English test, rows 471-472). The other intervals matched manifest values by rounding, by chance. So rows are added for the interval of every row whose point value comes from these two files: 5 corpora with the share and the Jaccard interval (file `c1_b1_b6_reproduction.json`, the file that manifest rows 111-116 already use for the point values; the audit names the other file, which holds the same values) and 2 corpora with the share interval (file `c3_n2_exchangeability_all_datasets.json`). 12 rows.
- A2-03 (0.866): the audit found no source. The source is `data/results/a_m1/a_m1_result.json` (run-repository commit `a245481`, "dev run result, status BOUND_ONLY"). 19 rows cover every value of Table S5.M and the sentence of Section 5.4. The file is not among the score-only copies under `results/` of the paper repository: see J-4.
- A2-04 (3,419): confirmed; `checks.analysis_set.reproduced.images_analysis` = 3419. 1 row.
- A2-05 (36 supplement numbers): 24 of the line hits are the numbers above; 2 more rows are added (0.478, the exponent b in S1; 0.9, the registered rule constant of the A-N2 ranking prediction in S7). The other hits are not defects (Section 6.1, item 2).

**R1. Reference list of the supplement** (audit A2-07). The file `SUPP_REFERENCES_A_v6.md` (sha256 in Section 7.2) is appended to `supplementary.md` after its last line, with one empty line between. It holds the heading `## References for the Supplementary Material`, one lead sentence and 98 entries in alphabetical order.
- Which works: every work that the supplement cites at HEAD, found with the build tool `prep.py cites` on the source file (175 mentions in S1–S10, 97 keys; S11 adds one key, found by the same tool, which printed the key only). The audit lists 30 keys that are missing from the main list; one of them, `zhou2024aligning`, is not cited in the supplement: the one mention "Zhou et al., 2024a" (source l.1157) is `zhou2024analyzing`, as the source comment beside it says, and the tool took both keys only because it was run on the copy without comments. So 29 works are in no printed list today.
- Why all 98 and not the 29: the supplement is published as a separate file and cites by author and year, while the main list is numbered in order of first citation; a reader cannot look up an author-year mention in it. See J-2.
- How the entries were made: `pandoc --citeproc` (pandoc 3.5, its default author-date style) from `paper/paperA.bib`, one paragraph per entry; no entry was typed by hand. Three years were given the letter that the text prints: `nguyen2026vsps` 2026a, `nguyen2026metric` 2026b, `zhou2024analyzing` 2024a.
- Place: after S11, because a reference list closes a document. The bytes of S11 are not changed: the script asserts that the text from `## S11` to the old end of the file stands once and unchanged in both supplement files.

**B1. New build script** `paper/build/build_A_supp.sh` (audit A3-05, A5-05), the file `build_A_supp.sh` of this folder (sha256 in Section 7.2). It builds, into a folder outside the repository, (1) the supplement PDF from `supplementary_SPIC.md`, with Fig. S1 from the vector file `figs/fig4_lambda_channels.pdf` and its caption from `figs/CAPTIONS.md` (through the filter of A6-F01), and (2) `highlights_A.docx` from the bullet lines of `highlights_A.md` with the comments removed. It writes no source.
- Tested in a scratch copy of HEAD with A6-F01 and A6-F02: PDF of 151 pages (158 pages with the reference list of R1), 0 undefined references, 0 missing characters, 72 overfull boxes (wide tables; not looked at one by one, and S11 is part of the count); `highlights_A.docx` written with 5 bullets. The PDF and the Word file were not opened.
- A5-05 asks for the Word file itself. It is not put into the repository: it is built from `highlights_A.md`, which may still change with the update of Section 6.7, and a second copy could then disagree. See J-5.
- A3-05 also says that `scrub_supp.py` stops on its leak check because of hits inside S11. That is unchanged and belongs to the S11 update (CC-407 W5). Step S2 uses the function `scrub()` only, as packages v2 and v4 did.

**T1. The abstract stands alone** (audit A5-02). Three replacements on the printed text of the abstract paragraph of `abstract_A.md`, each with the number of matches the script requires:

| Pattern (Python regular expression) | Replaced by | Matches |
|---|---|---|
| `` \((?:H\d[a-z]?, )*H\d[a-z]?\)`` (a space, then a bracket that holds only hypothesis codes) | nothing | 3 |
| `\(H\d[a-z]? [A-Z_]+; single annotator; Section 6\.7(?:\.\d+)?\)` | `(single annotator)` | 1 |
| `\bfour LVLMs\b` | `four large vision-language models` | 1 |

- Defect confirmed: the abstract has one section pointer, eight hypothesis codes that it does not define, and the abbreviation LVLMs, used once and not written out.
- What stays: every count, every outcome word and every number of the sentences. What goes: the codes in brackets, one verdict token that stood with a code inside the bracket of the second pattern, and the section pointer. The registered labels and verdicts stay verbatim where they are reported (Section 6.7, Table 1, S11); see J-1.
- The script asserts: the numbers printed after the step are a subset of those printed before (no number is added, so nothing needs a new manifest key, and nothing comes from a held zone); 241 words, limit 250; an unprinted comment that records the step is put directly after the paragraph.
- The patterns are given in place of OLD/NEW strings because the OLD strings would print outcomes of the held study in this file.

**V1. The cover letter and the abstract say the same** (audit A4-02). The script takes from the abstract, as it stands after T1, the one sentence that begins "Of seven predictions" and ends "was not validated." and puts it into the Main-result bullet of `cover_letter_A.md` (l.13), after the words "rest on one verbose system (both post hoc). " and before "Two of five registered", followed by an unprinted comment.
- Defect confirmed: the abstract reports the whole set of outcomes on the new single-annotator labels and says that the proposed certificate was not validated; the cover letter gives one passing outcome of that set and stops.
- Of the audit's two ways (add the abstract's clauses, or take the single outcome out of the letter) the first is taken: it removes nothing and the letter's own head comment says that every claim in it is a sentence of the abstract.
- The sentence is copied by the script and is not printed here. The script asserts that the printed letter after the step equals the printed letter before it plus exactly that sentence.
- If T1 is skipped, V1 copies the sentence as it stands at HEAD.

**S2. Published supplement and provenance table.** `supplementary_SPIC.md` is rebuilt as `scrub(supplementary.md)` and `supplementary_provenance_internal.tsv` from the same call, as in packages v2 and v4. Asserted: at HEAD the published copy equals `scrub()` of the source; after the package every leak hit lies inside S11, as at HEAD; no revision-history wording is left in the printed S1–S10 (pattern `HISTORY` of the script). In the provenance table, which is an internal file, the one new comment of A6-N02 raises the running number of every later row by one, the rows of S11 among them, and the heading column follows the new titles; no comment text of a row changes.

**S3. Length comment of `abstract_A.md`** (an HTML comment before `## Abstract`). Five replacements, each on a string that occurs once: the list of recounts gains "; recounted after fix package v6 of 2026-11-15"; "Main text now: 19,265 words" becomes "Main text now: 19,282 words"; "Over the limit by 10,765 words." becomes "Over the limit by 10,782 words."; "Abstract: 250 words" becomes "Abstract: 241 words"; the line "Longest files:" is rebuilt from the counts (`sec11_limitations_ethics.md` 2,140 becomes 2,162).

## 5. OLD occurs once

Counted in `git show HEAD:paper/<file>` (HEAD `0b542cf`). "NEW at HEAD outside OLD" is counted after the OLD string is taken out, because several NEW strings are the OLD string without its bracket.

| Id | File | OLD at HEAD | NEW at HEAD outside OLD | NEW after the package |
|---|---|---|---|---|
| A6-N01 | `sec5_exchangeability.md` | 1 | 0 | 1 |
| A6-N02 | `supplementary.md` | 1 | 0 | 1 |
| A6-F01 | `build/filter.lua` | 1 | 0 | 1 |
| A6-F02 | `build/filter.lua` | 1 | 0 | 1 |
| A6-H01 | `supplementary.md` | 1 | 0 | 1 |
| A6-H02 | `supplementary.md` | 1 | 0 | 1 |
| A6-H03 | `supplementary.md` | 1 | 0 | 1 |
| A6-H04 | `supplementary.md` | 1 | 0 | 1 |
| A6-H05 | `supplementary.md` | 1 | 0 | 1 |
| A6-H06 | `supplementary.md` | 1 | 0 | 1 |
| A6-H07 | `supplementary.md` | 1 | 0 | 1 |
| A6-H08 | `supplementary.md` | 1 | 0 | 1 |
| A6-H09 | `supplementary.md` | 1 | 0 | 1 |
| A6-H10 | `supplementary.md` | 1 | 0 | 1 |
| A6-H11 | `supplementary.md` | 1 | 0 | 1 |
| A6-H12 | `supplementary.md` | 1 | 0 | 1 |
| A6-H13 | `supplementary.md` | 1 | 0 | 1 |
| A6-H14 | `supplementary.md` | 1 | 0 | 1 |
| A6-H15 | `supplementary.md` | 1 | 0 | 1 |
| A6-H16 | `supplementary.md` | 1 | 0 | 1 |
| A6-H17 | `supplementary.md` | 1 | 0 | 1 |
| A6-H18 | `supplementary.md` | 1 | 0 | 1 |
| A6-H19 | `supplementary.md` | 1 | 0 | 1 |
| A6-H20 | `supplementary.md` | 1 | 0 | 1 |
| A6-H21 | `supplementary.md` | 1 | 0 | 1 |
| A6-H22 | `supplementary.md` | 1 | 0 | 1 |
| A6-H23 | `supplementary.md` | 1 | 0 | 1 |
| A6-H24 | `supplementary.md` | 1 | 0 | 1 |
| A6-H25 | `supplementary.md` | 1 | 0 | 1 |
| A6-H26 | `supplementary.md` | 1 | 0 | 12 |
| A6-H27 | `supplementary.md` | 1 | 0 | 1 |
| A6-H28 | `supplementary.md` | 1 | 0 | 1 |
| A6-H29 | `supplementary.md` | 1 | 0 | 1 |
| A6-H30 | `supplementary.md` | 1 | 0 | 1 |
| A6-H31 | `supplementary.md` | 1 | 0 | 1 |
| A6-H32 | `supplementary.md` | 1 | 0 | 1 |
| A6-H33 | `supplementary.md` | 1 | 0 | 1 |
| A6-H34 | `supplementary.md` | 1 | 0 | 1 |
| A6-H35 | `supplementary.md` | 1 | 0 | 1 |
| A6-H36 | `supplementary.md` | 1 | 0 | 1 |
| A6-H37 | `supplementary.md` | 1 | 0 | 1 |
| A6-H38 | `supplementary.md` | 1 | 0 | 1 |
| A6-H39 | `supplementary.md` | 1 | 0 | 1 |
| A6-H40 | `supplementary.md` | 1 | 0 | 1 |
| A6-H41 | `supplementary.md` | 1 | 0 | 1 |
| A6-H42 | `supplementary.md` | 1 | 0 | 1 |
| A6-H43 | `supplementary.md` | 1 | 0 | 1 |
| A6-H44 | `supplementary.md` | 1 | 0 | 1 |
| A6-H45 | `supplementary.md` | 1 | 0 | 1 |
| A6-H46 | `supplementary.md` | 1 | 0 | 1 |
| A6-L01 | `sec11_limitations_ethics.md` | 1 | 0 | 1 |
| A6-L02 | `sec11_limitations_ethics.md` | 1 | 0 | 1 |
| A6-D01 | `declarations.md` | 1 | 0 | 1 |

Agreement clauses, counted as the string "agreed to this use" in the printed text: `declarations.md` 3 before and after, `sec11_limitations_ethics.md` 2 and 2, `anon/declarations_anon.md` 1 and 1 (not written), `cover_letter_A.md` 0 and 0.

## 6. Not in this package

### 6.1 Dropped or changed against the audit, with the reason

1. **A4-04, first half (`sec1_introduction.md` l.45): dropped.** The audit asks to delete "AD-1′" and to write "premise not met" for "PREMISE_NOT_MET". Both stand in a row of Table 1, the registration ledger, whose verdicts are copied from the decide files. "PREMISE_NOT_MET" is the registered verdict and "AD-1′" the registered name of the test; the rule of this package is that registered labels and verdicts stay verbatim. Both are mapped in the supplement: Table S4.0, row A26 ("A-T3 AD-1′", published copy l.307), the row with the verdict (l.311), and S7 (l.714-722). That is the same footing as the ledger identifiers that the audit accepts under A5-16. If the investigator wants a gloss in the row at the rewrite, it is one bracket; see I-6.
2. **A2-05, the hits that are not defects.** The checker looks for a number as a separate token and misses a bound inside a manifest row that holds a whole interval, and a share that the manifest holds as a fraction. Already keyed: l.234 6.03 (manifest row 172, `[0.75,6.03]`); l.246 0.579 (row 69); l.248 5.27 and 4.67 (rows 166, 169) and 3.41 (row 60, 3.407); l.453 and l.821 0.414 and 0.647 (row 253) and 0.533 (row 252, 0.5333); l.592 25.00 and 37.27 (row 127) and 4.80 (row 123); l.746 6.5% and 70.5% (rows 629 and 626, as 0.065 and 0.705); l.929 41.5% (the row for 0.415 named in the source comment). The supplement line numbers are those of the published copy, as in the audit.
3. **A3-07 as proposed (`\usepackage{xurl}` in `cas.pandoc.tex`): replaced by A6-F02.** The package is already loaded and the wide boxes are in Table 2.1, not in the reference list (evidence of A6-F02). The table of Section 6.7.4 is not touched; 5 boxes wider than 10 pt remain there (the audit counted 4).
4. **A2-07: 29 works, not 30**, and the list holds all 98 cited works (step R1).
5. **A2-03: "remove the sentence" is not needed**; the source was found (step S1, A6-N01).
6. **A5-05: no Word file in the repository**; a build step instead (step B1, J-5).
7. **A6-02 (a full read of Sections 2–11 and S1–S10 since packages v2–v5): not a block.** It is a read by a reviewing agent, best done after this package is applied, so that it covers the text as it will be submitted. While checking the items above, this agent read in full: Table 5.1 and Section 5.4, Table S5.M and its notes, the S5 tables, every heading of S1–S10, the notes of S7, S9 and S10 named in group H, and the paragraph of Section 9.1 of group L. It found nothing beyond the items of this package, but that is not the sentence-by-sentence read the audit asks for.

### 6.2 For the investigator, or waiting for the journal guide (no block)

- **I-1 (audit A1-01, A6-01).** Second annotator, the investigator's extra labelling session, the code run, the update and the review of Section 6.7 and S11. After the update, the reference list of step R1 needs the keys that the new S11 cites (one at HEAD), and step T1 and V1 need a second look, because the sentence they act on reports the held study.
- **I-2 (audit A4-03).** Related-manuscript statements (`declarations.md` l.23, `cover_letter_A.md` l.25): they depend on the dates on which Paper B and the conference version of Paper C are submitted.
- **I-3 (audit A5-01, A5-03, A5-11, A5-13; guide not read).** Abstract limit, keyword limit, reference style and journal abbreviations, length. After T1 the abstract has 241 words, so a different way of counting no longer breaks a limit of 250. No length is cut here.
- **I-4 (audit A5-06, A5-07, A5-09).** Addresses, e-mails, further ORCIDs; the deposit and its link; the declarations in the submission system.
- **I-5 (custody; the audit's flag).** The outcomes of the held study are printed outside the held sections in eight places that the audit lists. V1 adds one more sentence of that kind to the cover letter. If those figures are held from the investigator, the cover letter and the abstract are part of what is held; this package changes neither the scope nor the figures.
- **I-6 (optional, at the rewrite).** A gloss for "AD-1′" in the Table 1 row of Section 1.2, if wanted (6.1 item 1).
- **I-7 (the statement on AI tools).** Nothing is added and nothing says that no AI tool was used (PI-1115i item 6). The words "large vision-language models" of T1 name the systems under study.

### 6.3 For the judge

- **J-1 (T1 and the rule on registered verdicts).** T1 takes one verdict token and eight codes out of the abstract. They are not reworded and stay verbatim in the body. If the judge reads the rule as "no registered token leaves the abstract", set `SKIP = ("T1",)`; V1 then copies the sentence with its codes, and A5-02 stays open for the investigator.
- **J-2 (R1: 98 entries or 29).** The list holds every work the supplement cites. The audit's smaller list (only the works missing from the main list) would leave author-year mentions that resolve only through a numbered list in another file. If the judge prefers the smaller list, the file has to be rebuilt; it is not a SKIP.
- **J-3 (R1 and S11).** The list is put after S11 and includes the one key that S11 cites. No byte of S11 changes and nothing of S11 is printed here, but the key set of S11 was computed by a tool. If the judge wants S11 left out of even that, the entry `fernandezbarrios2026disagreement` is removed and the list is rebuilt after the S11 update.
- **J-4 (the source of Table S5.M in the release).** `data/results/a_m1/a_m1_result.json` is tracked in the run repository and is not under `results/` of the paper repository, where the score-only copies of the cited result files are. Adding it is a release step for the gatekeeper (it holds counts and bounds only: 14 kB), together with a `PROVENANCE.md` row.
- **J-5 (A5-05).** Build step, not a committed Word file. To have the file in the repository, run B1 after the S11 update and commit its output.
- **J-6 (group H, the retitled headings).** The new titles are this agent's wording. Two headings whose old section number belongs to an older numbering (A6-H02, A6-H17) are retitled by content without a number. Each block can be skipped alone; the script then reports the wording that is left and still passes if a group H id is in SKIP.
- **J-7 (A6-F01 raises an error when a figure has no caption paragraph).** This also holds for `build_A_elsarticle.sh`, which uses the same filter.
- **J-8 (tests run here).** Document builds were run on the laptop in a scratch folder: the journal build before and after the filter change and the supplement build (about 10 s each). The whole package was also applied by a copy of the script, in write mode, to a scratch git copy of HEAD (11 files written, all equal to the targets), and both builds were run on the result: main PDF 39 pages (38 at HEAD; the captions add text), no undefined reference, 17 overfull boxes; supplement PDF 158 pages. These are builds of documents, not tests of scoring code; no file of the paper repository was written, and its `git status` is clean.

## 7. Script, pins and targets

### 7.1 Script

`manuscript/fix_packages/2026-11-15_A/apply_a_v6.py`.
- Check mode (default; nothing written): `python3 -I -B apply_a_v6.py`
- Write mode: `python3 -I -B apply_a_v6.py --write --ruling <id of the GO ruling>`: writes 11 files to the working tree of the paper repository. It never runs `git add` or `git commit`.
- With a block or a step skipped by the ruling, set `SKIP` and replace `TARGETS` by the values the ruling fixes. Steps: `S1`, `R1`, `B1`, `T1`, `V1`, `S3`.

Assertions: pins of this file, of the reference list and of the build script; `0b542cf` is HEAD or an ancestor; clean `paper/` tree; base sha256 of the 13 files read; each OLD once at HEAD and no NEW at HEAD outside its OLD; a block changes printed text unless it is one of the two comment blocks, which must not; every supplement block lies before S11; the bytes from `## S11` to the old end of file stand once and unchanged in both supplement files; the published copy equals `scrub()` of the source; leak hits only inside S11; no revision wording left in S1–S10; the abstract changes only by the three patterns and prints no new number; the cover letter gains exactly the abstract's sentence; `sec7_verbosity_sign.md`, `highlights_A.md`, the title page, `sec1_introduction.md` and the anonymised declarations are not written; no run of eight words from Section 6.7, S11, the abstract body or the highlights occurs in this package, in its two files or in the script; the count of agreement clauses is unchanged in every file; no NEW string and no step adds wording on AI tools.

### 7.2 Pins

| Object | sha256 |
|---|---|
| `SUPP_REFERENCES_A_v6.md` | `147aa1e9204528c022c2763d8cb497c962a3d47a8a6d22f81ecaf5c1bdee0381` |
| `build_A_supp.sh` | `e3a4cab2a1d4a5d23facaf8812498c70e536d99ac5386e1a8abb8c1da09183f4` |

The sha256 of this package file is pinned in the script and reported with the script's own sha256 in the hand-over message.

### 7.3 Targets (files after the package; SKIP empty)

| File under `paper/` | sha256 at HEAD `0b542cf` | sha256 after the package |
|---|---|---|
| `abstract_A.md` | `b566eb8e8f4ca29d9ccc5383c987aca53bd54678cddd414e68836d81c7c29752` | `91e9802c81a7807051a0862a9b13bd47598c5a11b7e5d7031c792cf63fab967f` |
| `build/build_A_supp.sh` | new file | `e3a4cab2a1d4a5d23facaf8812498c70e536d99ac5386e1a8abb8c1da09183f4` |
| `build/filter.lua` | `7ce939e753ec1913f53c67543c0fbebee7420d3558e945bde9be7e0d88e5063a` | `89e187af95d4f70ba617eb9c7c488b9b70a78f0bc0e26cca7a64fb5833840108` |
| `cover_letter_A.md` | `7c14bb274f6e50c47abdbaceeebacad22da86d52043ac731dbac6835b8737957` | `fc7102d343e9b996fdfaaee3afd9e61d973f14b7d432ab3376825e23901690e6` |
| `declarations.md` | `3b2381ca23d22682dd431dfed5c7a738c2ae41bf55356fa5291b23c6a598b5d2` | `69ceb15e18535fca9e50664b8b0dd20e4ec421739a827fc4c70f7f54f85e5906` |
| `number_manifest.tsv` | `dd2bce1797bb5bbe52da2d832750038bbfc7f2d39c10d99fe6eacb9de9b716c8` | `f5d517cc56df8302fd43996f677bbead29f6fd0bfd95029b08620cc83de91b07` |
| `sec11_limitations_ethics.md` | `dff441d598ae945c459dfbc348d2dd51e2a8c2a2621a62a781c0d6836d74a34f` | `bb7ff51c373bc4427639fec39b7826b170eb7e2a0969322a25884aacca3ad3b3` |
| `sec5_exchangeability.md` | `280b0e87e80d387df432515d392d50400a39c798581ad8b2e25c5ce52883a8fd` | `9167bd8ce84bf8ef6e8ed65ba2e93abde128328d3daf8f289e910f0097dcfa27` |
| `supplementary.md` | `dd7277069ced9d4d66c2b57e933d06a9b05cc41aae546b5cefa0c10ddcccc2ee` | `67d36d9583e7b032c74d2a91529782af056e2ec077fccf373f35b1ed36d5b88d` |
| `supplementary_SPIC.md` | `0c746c2127cac8bcb25340172e3859cc3c023d4739e7e8d812967287e554f280` | `68b1dfab60d90610e35014d49080fb1ca45a4eab71b6bea8773f3c5b27f85026` |
| `supplementary_provenance_internal.tsv` | `1162582f16633e11d26d9d1a72fd20a3b04389a51453c3e1e8c2605068002a07` | `1fcc915f39f77aa287429766402ccd4c335ebbcb102eda6d4fa69e282d437d62` |

Read and not written (sha256 at HEAD, asserted): `sec7_verbosity_sign.md` `b6f46b8aaf33ef133b54e5e4d91f2c1f037e061d48f495e1b23eed5b0aaf4817`; `highlights_A.md` `64c671615bd5106cba42cf168ff7ff85460bd9bd72b3c52a2d9903861c281aa5`; `anon/declarations_anon.md` `e407d32ddd13b2903482472e35cf011e71177ea23f271425e9e38f60ee5172ca`.
