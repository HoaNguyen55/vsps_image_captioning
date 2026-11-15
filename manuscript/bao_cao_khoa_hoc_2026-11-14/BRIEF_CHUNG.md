# Common brief for the writers of the scientific report (14/11/2026)

## What the investigator asked for (verbatim)

> Dựa trên toàn bộ nội dung bài báo đã được xây dựng trong session hiện tại, hãy viết một báo cáo khoa học hoàn chỉnh. Với mỗi mục, hãy tổng hợp, phân tích và trình bày đầy đủ các nội dung liên quan, bao gồm cơ sở lý thuyết, phương pháp, thiết kế, kết quả và nhận xét (tùy theo nội dung từng mục). Yêu cầu: giữ nguyên nội dung và định hướng nghiên cứu đã thống nhất; sử dụng văn phong học thuật, logic, chuyên sâu và nhất quán; không bỏ sót thông tin quan trọng; không tự tạo số liệu, kết quả hoặc tài liệu tham khảo; giữ lại công thức, bảng biểu và hình minh họa cần thiết; đảm bảo báo cáo có thể sử dụng làm tài liệu rà soát và hoàn thiện bài báo khoa học.

The report covers Papers A, B and C and the conference version of Paper C. Each writer produces ONE part. The coordinator joins the parts, adds an overview and the status of work in progress, and builds the DOCX and PDF.

The reader is the principal investigator (a PhD student, Vietnamese). He will rewrite each paper himself and must be able to defend every claim. He uses this report to check the paper section by section and to see what still needs work.

## Output

- One Markdown file, in Vietnamese with full diacritics: `manuscript/bao_cao_khoa_hoc_2026-11-14/parts/<your part file>`. Write it in several steps (Write the first sections, then append with Edit) so that no single tool call carries the whole text.
- You may also write `parts/<your part>.allow.tsv` (see "Check"). Touch no other file. Do not commit, do not stage, do not push.

## Sources: read only what your prompt lists

Your prompt names the paper folder. Read the paper text in full before you write (every section file, the supplement, the study brief, the figure captions). Use the number manifest and the `prereg/` Markdown files of the same paper repo when you need the exact registered wording of a prediction or a rule.

Never open, list or search any of these: `.session_backup/`, `~/vsps_labels*`, `~/vsps_labels_b`, `~/.vsps_sealed`, `~/vsps_handoff`, `~/bpa1pull_1108`, any `results/` folder, any `key.json`, `assignment.json`, `practice.json`, `gt_cache.json`, any `*.jsonl` label file, any folder named `b_text_held`, `b_result_snapshot`, `b_stages` or `host_pull`, the folder `manuscript/prereg/` of the run repo, the folder `manuscript/journal_draft*` of the run repo (older copies; the paper repos are the valid text). Do not use the network. Do not run any scoring, model or data script.

## Hard rules on content

1. **No new number.** Every figure you write is copied, as printed, from the paper text, its supplement, its figure values or its number manifest. Keep the paper's own format: decimal point, the same number of digits, the same interval form. Do not round again, do not convert units, do not add, subtract or average. If you need a number the paper does not print, write that the paper does not report it.
2. **Registered results never change.** Copy each registered verdict word for word in English, in quotation marks (PASS, FAIL, MIXED, HELD, INCONCLUSIVE, UNDERPOWERED and so on), then explain it in Vietnamese. A FAIL is reported plainly with its estimate, its interval and its registered threshold. "Not detected" is not "no effect". Post hoc and exploratory rows keep their label (POST HOC, exploratory, development only) and get no verdict.
3. **No new reference.** Cite only works that are in the paper's `.bib` file(s), with pandoc syntax `[@key]` or `[@key1; @key2]`, using the exact bib key. Papers A and B write citations as author–year text and keep the keys in HTML comments and in `citation_map_*.tsv`; find the key there or in the `.bib` by author and year. If you cannot find the key, do not cite. Do not write a reference list: the coordinator builds it from the `.bib`.
4. **No text of any dataset caption or model output**, in any language. No host name, address or port. No name of a person other than cited authors.
5. **No internal process.** Do not mention ruling ids (CC-, OPS-, PI-, CP-), judges, agents, sessions, or how the text was produced. The report is about the science of the paper.
6. **Do not strengthen a claim.** Keep the paper's hedges. Do not write "first", "novel" or "no overlap" unless the paper states it, and then quote the paper's sentence.
7. Where the paper states a limit, a withdrawal, a failed prediction or a disclosure, it must appear in the report.

## Structure of a part

Use the prefix letter given in your prompt (below: `X`). Number headings, tables, figures and equations by hand: `## X.3`, `### X.3.2`, **Bảng X.4**, **Hình X.2**, equation tag `(X.5)`. Do not rely on automatic numbering.

- `# Phần X. <tên bài báo bằng tiếng Việt> (<English title as in the title page>)`
- `## X.1 Thông tin chung`: title, target venue and its limits as the paper folder records them, article type, what the paper claims in one paragraph, the list of contributions as the paper states them, and the paper's own section map.
- Then **one `##` section for each section of the paper, in the paper's order** (introduction, related work, data, method or measurement setup, theory, each results section, the comparison with English data, discussion, limitations and ethics, declarations, conclusion; the supplement gets one section that walks through its parts). In each of these sections write two blocks:
  - `**Nội dung.**` A faithful and complete account of the section: the theoretical basis, definitions and notation, formulas (LaTeX in `$...$` or `$$...$$`, copied from the paper, with every symbol explained), the design (data, splits, systems, registered predictions and decision rules, statistics and how intervals are computed), the results with their tables, and what the paper concludes from them. Reproduce the tables that carry the main results as Markdown pipe tables with a caption line `**Bảng X.n.** …` that names the paper section it comes from. Long supplementary tables may be summarised, with a pointer to the supplement section.
  - `**Nhận xét rà soát.**` Your analysis as a careful reviewer: what the section establishes and how strongly; where a number, a definition or a name differs between two places of the paper (give both places); what a referee is likely to ask; what is missing or unclear; what should be fixed before submission. Ground every remark in the text (name the file and the section). Do not speculate about results that are not in the paper.
- Figures: the available files are in `manuscript/bao_cao_khoa_hoc_2026-11-14/figs/`. Insert them as `![Hình X.n. <chú thích tiếng Việt>](figs/<file>.svg)` where the paper uses them, with the caption translated from the paper's caption.
- `## X.<n> Bảng đối chiếu khẳng định – bằng chứng`: one row per claim of the abstract, introduction and conclusion: the claim (short), its status (REGISTERED PASS / FAIL / MIXED / POST HOC / DESCRIPTIVE / EXPLORATORY), the section, the table or figure, the key number(s), and the manifest key (`file::key`, in a code span) when the manifest gives one.
- `## X.<n+1> Danh mục việc cần rà soát và hoàn thiện`: the consolidated list of your review remarks, ordered by importance, each with the place in the paper and a concrete suggestion. Separate "lỗi hoặc mâu thuẫn cần sửa" from "điểm nên làm rõ" and "câu hỏi phản biện có thể gặp".
- `## X.<n+2> Thuật ngữ và ký hiệu`: a table of the paper's terms and symbols, English and Vietnamese, with a one-line meaning.

## Style

- Academic Vietnamese: complete, connected sentences; each paragraph develops one idea and links to the next. No telegraphic fragments, no chains of isolated one-sentence paragraphs, no slogans.
- Give the English technical term in parentheses at first use, then use one Vietnamese term consistently (list it in the glossary). Keep dataset, model and metric names in their original form.
- Be complete rather than short. Do not pad: every sentence should carry content from the paper or a grounded review remark.

## Check (must pass before you finish)

Run the checker from the run repo root and repeat until it reports `UNMATCHED: 0` and `MISSING from bib: 0`:

```
python3 -I manuscript/bao_cao_khoa_hoc_2026-11-14/checks/check_part.py <part.md> --src <source files> --bib <bib files> --allow <part>.allow.tsv
```

`--src` is the list of source files given in your prompt. The checker looks up every decimal, every percentage and every integer of 100 or more. For an unmatched number, first correct it to the printed form. Only a number that is genuinely not a paper figure (for instance a page limit taken from a file outside `--src`, which you then add to `--src`) may go in the allow file, one line `token<TAB>reason`. The lines listed under `review [...]` must be empty or explained in your final message.

## Final message

Give: the path of your part, its word count, the last checker output, the content of your allow file with reasons, and the five most important review findings. State plainly anything you could not do.
