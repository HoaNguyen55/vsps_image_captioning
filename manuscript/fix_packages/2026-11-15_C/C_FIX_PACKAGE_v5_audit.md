# Paper C (journal version, ACM TALLIP): fix package v5, the NOT READY items of the readiness audit

**Applies after the CC-413 commit** (fix package v4 with Annex B of ruling CC-413; that commit follows the CC-408 commit of fix package v2, which follows the freeze shell on 2026-11-16 after 05:00Z). Prepared 2026-11-15T10:36Z (2026-11-15, 17:36 Vietnam time). Nothing in this package has been applied, staged or committed. It is for a judge to read first.

## 0. Scope, state it applies to, and conventions

- **What it is.** The fixes for the nine NOT READY rows of `manuscript/READY_AUDIT_C_2026-11-15.md` (sha256 `4bf53e200eed3dda429745ba9366a66100e0fdafc6580a17cb9f14d2494703d6`), each re-verified for this package. "Item n" below is row n of section 3 of the audit.
- **State the OLD strings were written against.** The text after the three scheduled commits, built in memory and never written: every section file and the manifest by the functions of `apply_c_v2_cc408.py` (which uses the freeze transfer's own swap calls), then the 15 blocks of `C_FIX_PACKAGE_v4_search.md`, then the seven pairs of Annex B, read from the ruling file `CC-413.txt` (sha256 `b9c9ec64…`; annex bytes `3fb2a675…`). The apply script rebuilds this state and checks each file against the value below before it reads a block.
- **Files this package changes, and the value each must have:**

| file | blocks | must be at (sha256) | source of that value |
|---|---|---|---|
| `paper_v1_analysis/02_related_work.md` | 1 | `b9f0c1f88cde26884debce22099c5eed1fdadb782a28608ecfab20acd1efebee` | CC-413, targets after package v4 and Annex B |
| `paper_v1_analysis/03_method.md` | 1 | `5db109ab3b011cf658da599d5ef67636c7b282f378829abb3a35f176521da057` | CC-408 Ruling 9 |
| `paper_v1_analysis/04_data_and_splits.md` | 1 | `58529b1dc3444b9a89830661a0a724e4ee3fc5ed8bb8acb9383639a70320c540` | CC-408 Ruling 9 |
| `paper_v1_analysis/paperC.bib` | 4 | `550b88d118f4bdb5dadbb930f05263e14ba65ab6df84c82285ccc824e1c777b8` | CC-413 |
| `paper_v1_analysis/paperC_bib_audit.tsv` | 4 | `55ece5075b17ff2b5d78d5760264d82b8e55918a5829d3a1545fbd45a83145d4` | CC-413 |
| `scripts/paperC/c_pass2_check.py` | 1 | `a257bd14891403a11a709030bfb785c2c3f6302ca342a6ef96324fbe0c11e7e7` | paper HEAD `55315ca`; no scheduled commit changes it |
| `paper_v1_analysis/tex/readme.txt` | new file | must not exist | – |
| `paper_v1_analysis/number_manifest_C.tsv` | 2 operations, in a separate last step | lines before the two freeze rows: `bae5743928a30483d090f8abb6ee45aae78934d27c40a1122db688efe2c0f95f`; then the freeze row and the row for 40 | CC-408 Ruling 9; shell C2 |

- **Read, not changed:** `paper_v1_analysis/11_supplement_registered_rows.md` at `c4a24cd4da244af6d36385e9b7796cbb3b8d05883c6f513a2d365988650f0d55` (CC-413), for the list of the readme; every other section file, for the manifest step.
- **Order, binding.** Freeze shell, then package v2 (CC-408), then package v4 with Annex B (CC-413), then this package, then the tex rebuild. The write mode of the apply script refuses unless every file above is at its value at paper HEAD.
- **Two steps.** Step 1 writes the text, bibliography and tooling files. Step 2, run after step 1, writes the manifest only; it checks that the two freeze rows are present and unchanged.
- **What it does not touch.** No sentence of the paper changes except for three added citation keys. No number is added to or removed from any `.md` file of the paper. No registered label, verdict or rule is changed. No text is cut. The package holds no statement on AI tools. `tex/build.sh`, `tex/preamble.tex` and the built `tex/` files are not touched; the rebuild regenerates the build files.
- **Block format** as in v1 to v4: the OLD string is the text between the `OLD>>>` line and the `NEW>>>` line, without the line break that ends it; the NEW string likewise, up to the `EVIDENCE>>>` line; an `END>>>` line closes the block. The file token is the path inside the paper repository. Block ids are `C-A01` … `C-A13`. Block C-A13 is a new file (`NEWFILE>>>`; the file ends with one line break). Block C-M02 holds manifest rows (`ROWS>>>`). In the blocks on `paperC_bib_audit.tsv` and in C-M02 the fields are separated by tab characters.
- **Apply script:** `manuscript/fix_packages/2026-11-15_C/apply_c_v5_audit.py`. Default mode is a check that writes nothing.
- **Records of the lookups** (public pages and bibliographic records, fetched with a generic client name and no personal data): `manuscript/fix_packages/2026-11-15_C/v5_records/` with `SHA256SUMS`.
- **Custody.** Read for this package: the audit, the paper text and bibliography, the registration v1.1 of the attribution study, the decision log, one committed mutant-run log, public web pages. No label folder, sealed folder, key file, reference cache, test-set score book, result or decision JSON, and neither held Paper B folder was opened. No dataset caption and no model output is printed.

## 1. Table of items

| audit item | finding of the audit | verified | outcome | blocks |
|---|---|---|---|---|
| 8 | Table 1 overfull box (15.9 pt); font substitution for italic code font | not verifiable now: no build log is kept, and package v4 adds two rows to Table 1, so the box of the audit build is not the box of the rebuild | NOT A BLOCK: step of the rebuild (section 5) | 0 |
| 16 | `c_pass2_check.py` reads the archive manifest and normalises the text side only | yes: 581 tokens flagged as shipped, 40 after the change | BLOCK | C-A12 |
| 17 | four unkeyed quantities: 0.025, 0.0125, 22, 33 | yes, all four; and 73 has no row that names file 07 | MANIFEST ROWS (step 2) | C-M02 (5 rows) |
| 19 | 323 stale `used_in` pointers; five fields join a file name and a tag | partly: stale pointers yes (271 on the after-v4 text by the generous rule of section 4, which judges plain numbers only). The tag finding is wrong as stated: 504 fields end in a tag by design; the defect is 29 fields with the tag in the middle | MANIFEST OPERATION (step 2) | C-M03 |
| 20 | the V4 article is cited for the V7 labels; two uses carry no citation | partly: the Open Images V7 page itself asks for the V4 article to be cited for versions 5 to 7, so that key stays. The page that documents the V7 labels is added as a reference and cited at the three places | BLOCKS | C-A01 to C-A05 |
| 22a | `Hussain2026SciRepLVLM`: volume and article number now assigned | yes (Crossref today) | BLOCKS | C-A06, C-A07 |
| 22b | `Yang2023ReViLM`: published in Findings of EMNLP 2023 | yes (Crossref and ACL Anthology today); the published author order also differs | BLOCKS | C-A08, C-A09 |
| 22c | `Oduwole2025AfriCaption`: published at AfricaNLP 2026 | yes (Crossref and ACL Anthology today) | BLOCKS | C-A10, C-A11 |
| 23 (and 10) | no supplement `readme.txt` | yes | BLOCK, may be left for packaging (`SKIP`) | C-A13 |
| 27 | the label "C-ATTR-DEV" prints 14 times; rename it | the count is right; the fix is wrong | DROPPED (section 3) | 0 |

Counts: 12 OLD/NEW blocks and 1 new-file block under 13 ids (1 in each of files 02, 03 and 04; 4 in the bibliography; 4 in its audit table; 1 in the checker; the readme), and 2 manifest operations. Rows 10 and 23 of the audit are one finding.

## 2. Blocks

### C-A01 to C-A03. The Open Images V7 labels: a reference that documents them (item 20)

The released human-verified labels are the gold of the verified-precision score on XM3600. Section 2 cited the Open Images V4 article for them; Sections 3.6 and 4 named them with no citation. The V7 description page keeps that article as the citation for version 7 and prints a general reference to the dataset; the general reference is added, with the address of the V7 page, and cited at the three places.

```text
<<<C-A01 paper_v1_analysis/02_related_work.md OLD>>>
against the released Open Images V7 human-verified labels [@Kuznetsova2020OpenImages], following that study's mapping rule.
<<<C-A01 paper_v1_analysis/02_related_work.md NEW>>>
against the released Open Images V7 human-verified labels [@Kuznetsova2020OpenImages; @Krasin2017OpenImages], following that study's mapping rule.
<<<C-A01 EVIDENCE>>>
Source: the Open Images V7 description page, https://storage.googleapis.com/openimages/web/factsfigures_v7.html, fetched 2026-11-15T10:09Z (sha256 03f731edf0a6…; copy in `v5_records/factsfigures_v7.html`).
The page documents the labels. Quote: "the validation and test sets, as well as part of the training set have human-verified image-level labels. Most verifications were done with in-house annotators at Google."
The page keeps the existing citation for version 7. Quote: "If you use the Open Images dataset in your work (also V5-V7), please cite this article", followed by Kuznetsova et al., IJCV 2020. The audit's reading that the V4 article is the wrong citation for V7 is therefore not kept; the existing key stays.
The page adds a general reference. Quote: "Please also consider citing this general reference to the dataset", followed by Krasin et al., 2017. This is the new key; its entry points at the version 7 page (block C-A04).
No number token is added to the file: the key holds digits inside a word, which the token rule of the checker does not read.
<<<C-A01 END>>>
```

```text
<<<C-A02 paper_v1_analysis/03_method.md OLD>>>
Verified precision on XM3600 is scored offline against the released human-verified Open Images labels, and those labels never reached the GPU server.
<<<C-A02 paper_v1_analysis/03_method.md NEW>>>
Verified precision on XM3600 is scored offline against the released human-verified Open Images labels [@Krasin2017OpenImages], and those labels never reached the GPU server.
<<<C-A02 EVIDENCE>>>
As for C-A01. The sentence names the labels as the gold of a reported score and carried no citation.
<<<C-A02 END>>>
```

```text
<<<C-A03 paper_v1_analysis/04_data_and_splits.md OLD>>>
and, offline only, the released human-verified Open Images labels.
<<<C-A03 paper_v1_analysis/04_data_and_splits.md NEW>>>
and, offline only, the released human-verified Open Images labels [@Krasin2017OpenImages].
<<<C-A03 EVIDENCE>>>
As for C-A01. This is the sentence of the data section that lists what the XM3600 test uses; it carried no citation.
<<<C-A03 END>>>
```

### C-A04, C-A05. Bibliography entry and audit row for the new key (item 20)

```text
<<<C-A04 paper_v1_analysis/paperC.bib OLD>>>
  note      = {arXiv:2403.13164}
}
<<<C-A04 paper_v1_analysis/paperC.bib NEW>>>
  note      = {arXiv:2403.13164}
}

@misc{Krasin2017OpenImages,
  author    = {Krasin, Ivan and Duerig, Tom and Alldrin, Neil and Ferrari, Vittorio and Abu-El-Haija, Sami and Kuznetsova, Alina and Rom, Hassan and Uijlings, Jasper and Popov, Stefan and Kamali, Shahab and Malloci, Matteo and Pont-Tuset, Jordi and Veit, Andreas and Belongie, Serge and Gomes, Victor and Gupta, Abhinav and Sun, Chen and Chechik, Gal and Cai, David and Feng, Zheyun and Narayanan, Dhyanesh and Murphy, Kevin},
  title     = {{OpenImages}: A public dataset for large-scale multi-label and multi-class image classification},
  year      = {2017},
  url       = {https://storage.googleapis.com/openimages/web/factsfigures_v7.html},
  note      = {Dataset. The address is the description page of version 7 ({Open Images V7}), which documents the human-verified image-level labels}
}
<<<C-A04 EVIDENCE>>>
Source: the Open Images V7 description page, https://storage.googleapis.com/openimages/web/factsfigures_v7.html, fetched 2026-11-15T10:09Z (sha256 03f731edf0a6…; copy in `v5_records/factsfigures_v7.html`).
Authors, title and year: the BibTeX record that the page prints under "general reference to the dataset" (22 authors; title "OpenImages: A public dataset for large-scale multi-label and multi-class image classification."; year 2017). The final full stop of the title is dropped, as in the other entries.
The page gives the address of the dataset's home page for this reference. The entry gives the version 7 description page instead, and the note says so, because that page is where the human-verified labels of version 7 are described.
No DOI exists for this reference. The entry is appended at the end of the file, as package v4 did for its four entries.
<<<C-A04 END>>>
```

```text
<<<C-A05 paper_v1_analysis/paperC_bib_audit.tsv OLD>>>
Zong2025VLICLBench	arXiv:2403.13164	https://export.arxiv.org/api/query?id_list=2403.13164 ; https://api2.openreview.net/notes/search?term=VL-ICL%20Bench	200	OK (2026-11-15; arXiv v4, comment "ICLR 2025"; OpenReview forum cpGPPLLYYx, venue "ICLR 2025 Poster", same title and three authors; dblp.org answered with a bot-check page and was left alone)
<<<C-A05 paper_v1_analysis/paperC_bib_audit.tsv NEW>>>
Zong2025VLICLBench	arXiv:2403.13164	https://export.arxiv.org/api/query?id_list=2403.13164 ; https://api2.openreview.net/notes/search?term=VL-ICL%20Bench	200	OK (2026-11-15; arXiv v4, comment "ICLR 2025"; OpenReview forum cpGPPLLYYx, venue "ICLR 2025 Poster", same title and three authors; dblp.org answered with a bot-check page and was left alone)
Krasin2017OpenImages	url:https://storage.googleapis.com/openimages/web/factsfigures_v7.html	https://storage.googleapis.com/openimages/web/factsfigures_v7.html	200	OK (2026-11-15; the page prints this record as its "general reference to the dataset": 22 authors, 2017, no DOI; the same page describes the human-verified image-level labels of version 7 and asks for Kuznetsova et al. 2020 to be cited for versions 5 to 7 as well)
<<<C-A05 EVIDENCE>>>
One audit row for the new key, in the five tab-separated columns of the file (key, id, url_checked, http, status). The fields are separated by tab characters.
<<<C-A05 END>>>
```

### C-A06 to C-A11. Three entries brought to their published versions (items 22a, 22b, 22c)

No key changes, so no section file changes. Each entry has one block and its audit row one block.

```text
<<<C-A06 paper_v1_analysis/paperC.bib OLD>>>
@article{Hussain2026SciRepLVLM,
  author  = {Hussain, Muzammal and Khan, Imran and Rashid, Javed and Althobaiti, Turke and Saleem, Muhammad Shoaib and Alameri, Abdu Qaid},
  title   = {Benchmarking large vision language models for multilingual image caption generation in low resource settings},
  journal = {Scientific Reports},
  year    = {2026},
  doi     = {10.1038/s41598-026-70568-5},
  note    = {Accelerated Article Preview; volume and article number not yet assigned (Crossref, 2026-10-30)}
}
<<<C-A06 paper_v1_analysis/paperC.bib NEW>>>
@article{Hussain2026SciRepLVLM,
  author  = {Hussain, Muzammal and Khan, Imran and Rashid, Javed and Althobaiti, Turke and Saleem, Muhammad Shoaib and Alameri, Abdu Qaid},
  title   = {Benchmarking large vision language models for multilingual image caption generation in low resource settings},
  journal = {Scientific Reports},
  year    = {2026},
  volume  = {16},
  number  = {1},
  pages   = {36452},
  doi     = {10.1038/s41598-026-70568-5}
}
<<<C-A06 EVIDENCE>>>
Source: Crossref, https://api.crossref.org/works/10.1038/s41598-026-70568-5, fetched 2026-11-15T10:10Z (copy in `v5_records/`, sha256 34de899e19af…).
The record gives: type journal-article; container "Scientific Reports"; volume 16; issue 1; article-number 36452; published 2026-09-21; the same title and the same six authors in the same order.
The article number goes in the `pages` field, the form the file already uses for an article-numbered journal (`Bui2026OpenViICJournal`). The stale note goes.
The key is cited once (`01_introduction.md`, l.5); the sentence there does not print the volume.
<<<C-A06 END>>>
```

```text
<<<C-A07 paper_v1_analysis/paperC_bib_audit.tsv OLD>>>
Hussain2026SciRepLVLM	doi:10.1038/s41598-026-70568-5	https://api.crossref.org/works/10.1038/s41598-026-70568-5	200	OK (2026-10-30; title, 6 authors; Accelerated Article Preview, no volume yet)
<<<C-A07 paper_v1_analysis/paperC_bib_audit.tsv NEW>>>
Hussain2026SciRepLVLM	doi:10.1038/s41598-026-70568-5	https://api.crossref.org/works/10.1038/s41598-026-70568-5	200	OK (2026-11-15; Crossref: Scientific Reports 16(1), article 36452, published 2026-09-21; title, 6 authors; replaces the check of 2026-10-30, when no volume was assigned)
<<<C-A07 EVIDENCE>>>
The audit row of the entry of C-A06, with today's lookup. Tab-separated.
<<<C-A07 END>>>
```

```text
<<<C-A08 paper_v1_analysis/paperC.bib OLD>>>
@misc{Yang2023ReViLM,
  author        = {Yang, Zhuolin and Ping, Wei and Liu, Zihan and Korthikanti, Vijay and Nie, Weili and Huang, De-An and Fan, Linxi and Yu, Zhiding and Lan, Shiyi and Li, Bo and Liu, Ming-Yu and Zhu, Yuke and Shoeybi, Mohammad and Catanzaro, Bryan and Xiao, Chaowei and Anandkumar, Anima},
  title         = {{Re-ViLM}: Retrieval-Augmented Visual Language Model for Zero and Few-Shot Image Captioning},
  year          = {2023},
  note          = {Findings of EMNLP 2023 (per the arXiv record)},
  eprint        = {2302.04858},
  archivePrefix = {arXiv},
  url           = {https://arxiv.org/abs/2302.04858}
}
<<<C-A08 paper_v1_analysis/paperC.bib NEW>>>
@inproceedings{Yang2023ReViLM,
  author    = {Yang, Zhuolin and Ping, Wei and Liu, Zihan and Korthikanti, Vijay and Nie, Weili and Huang, De-An and Fan, Linxi and Yu, Zhiding and Lan, Shiyi and Li, Bo and Shoeybi, Mohammad and Liu, Ming-Yu and Zhu, Yuke and Catanzaro, Bryan and Xiao, Chaowei and Anandkumar, Anima},
  title     = {{Re-ViLM}: Retrieval-Augmented Visual Language Model for Zero and Few-Shot Image Captioning},
  booktitle = {Findings of the Association for Computational Linguistics: EMNLP 2023},
  year      = {2023},
  pages     = {11844--11857},
  publisher = {Association for Computational Linguistics},
  doi       = {10.18653/v1/2023.findings-emnlp.793},
  note      = {arXiv:2302.04858}
}
<<<C-A08 EVIDENCE>>>
Sources, fetched 2026-11-15T10:10Z to 10:13Z (copies in `v5_records/`): Crossref https://api.crossref.org/works/10.18653/v1/2023.findings-emnlp.793 (sha256 40be13d34b08…); ACL Anthology record https://aclanthology.org/2023.findings-emnlp.793.bib (sha256 753f7bb91d1f…) and its landing page.
Both records give: proceedings article; "Findings of the Association for Computational Linguistics: EMNLP 2023"; pp. 11844–11857; Association for Computational Linguistics; the same title; 16 authors.
Author order: the published record lists Shoeybi before Liu (Ming-Yu) and Zhu; the old entry had the order of the arXiv record (Liu, Zhu, Shoeybi). The new entry follows the published record. The 16 names are the same.
The sentence that cites the key (`02_related_work.md`, l.7: retrieval from an external image-text database added to a Flamingo-style model for zero- and few-shot captioning) agrees with the published abstract. Quote: "built upon the Flamingo, that supports retrieving the relevant knowledge from the external database for zero and in-context few-shot image-to-text generations".
The form (fields, a `note` with the arXiv id) is the form of the entries that package v4 added.
<<<C-A08 END>>>
```

```text
<<<C-A09 paper_v1_analysis/paperC_bib_audit.tsv OLD>>>
Yang2023ReViLM	arXiv:2302.04858	https://arxiv.org/abs/2302.04858	200	OK (2026-10-29; venue from arXiv record only, no DOI checked)
<<<C-A09 paper_v1_analysis/paperC_bib_audit.tsv NEW>>>
Yang2023ReViLM	doi:10.18653/v1/2023.findings-emnlp.793	https://api.crossref.org/works/10.18653/v1/2023.findings-emnlp.793 ; https://aclanthology.org/2023.findings-emnlp.793.bib	200	OK (2026-11-15; Crossref and ACL Anthology: Findings of EMNLP 2023, pp. 11844-11857, title, 16 authors; author order of the published record, which differs from the arXiv record in three places; arXiv 2302.04858 is the preprint)
<<<C-A09 EVIDENCE>>>
The audit row of the entry of C-A08. Tab-separated.
<<<C-A09 END>>>
```

```text
<<<C-A10 paper_v1_analysis/paperC.bib OLD>>>
@misc{Oduwole2025AfriCaption,
  author        = {Oduwole, Mardiyyah and Mireku, Prince and Adebanjo, Fatimo and Olajide, Oluwatosin and Aliyu, Mahi Aminu and Novikova, Jekaterina},
  title         = {{AfriCaption}: Establishing a New Paradigm for Image Captioning in {African} Languages},
  year          = {2025},
  eprint        = {2510.17405},
  archivePrefix = {arXiv},
  url           = {https://arxiv.org/abs/2510.17405}
}
<<<C-A10 paper_v1_analysis/paperC.bib NEW>>>
@inproceedings{Oduwole2025AfriCaption,
  author    = {Oduwole, Mardiyyah and Mireku, Prince and Adebanjo, Fatimo and Olajide, Oluwatosin and Aliyu, Mahi Aminu and Novikova, Jekaterina},
  title     = {{AfriCaption}: Establishing a New Paradigm for Image Captioning in {African} Languages},
  booktitle = {Proceedings of the 7th Workshop on African Natural Language Processing (AfricaNLP 2026)},
  year      = {2026},
  pages     = {44--55},
  publisher = {Association for Computational Linguistics},
  doi       = {10.18653/v1/2026.africanlp-main.5},
  note      = {arXiv:2510.17405}
}
<<<C-A10 EVIDENCE>>>
Sources, fetched 2026-11-15T10:10Z to 10:13Z (copies in `v5_records/`): Crossref https://api.crossref.org/works/10.18653/v1/2026.africanlp-main.5 (sha256 270d78632720…); ACL Anthology record https://aclanthology.org/2026.africanlp-main.5.bib (sha256 f0a02e86487f…) and its landing page.
Both records give: proceedings article; "Proceedings of the 7th Workshop on African Natural Language Processing (AfricaNLP 2026)"; pp. 44–55; Association for Computational Linguistics; year 2026; the same title; the same six authors in the same order.
The key keeps "2025" (the year of the preprint). A key is not printed; changing it would touch `02_related_work.md` for no gain. The printed citation becomes "Oduwole et al. 2026".
The sentence that cites the key (`02_related_work.md`, l.22: captioning data and a model for 20 African languages) agrees with the published abstract. Quote: "a comprehensive framework for multilingual image captioning in 20 African languages".
No sentence of the paper prints the year of this work in words or digits (searched in the after-v4 text).
<<<C-A10 END>>>
```

```text
<<<C-A11 paper_v1_analysis/paperC_bib_audit.tsv OLD>>>
Oduwole2025AfriCaption	arXiv:2510.17405	https://arxiv.org/abs/2510.17405	200	OK (2026-10-29; AfricaNLP 2026 per ACL Anthology search result, not cited as such)
<<<C-A11 paper_v1_analysis/paperC_bib_audit.tsv NEW>>>
Oduwole2025AfriCaption	doi:10.18653/v1/2026.africanlp-main.5	https://api.crossref.org/works/10.18653/v1/2026.africanlp-main.5 ; https://aclanthology.org/2026.africanlp-main.5.bib	200	OK (2026-11-15; Crossref and ACL Anthology: Proceedings of the 7th Workshop on African Natural Language Processing (AfricaNLP 2026), pp. 44-55, title, 6 authors, year 2026; the key keeps 2025, the year of the preprint arXiv 2510.17405)
<<<C-A11 EVIDENCE>>>
The audit row of the entry of C-A10. Tab-separated.
<<<C-A11 END>>>
```

### C-A12. The number checker reads this repository's manifest (item 16)

Two lines of `scripts/paperC/c_pass2_check.py`. This is ruling CC-413, point N4, as well.

```text
<<<C-A12 scripts/paperC/c_pass2_check.py OLD>>>
MAN = Path("/mnt/d/vsps_image_captioning/manuscript/journal_draft_C/number_manifest_C.tsv")
have = {l.split("\t")[0] for l in MAN.read_text().splitlines()[1:]}
<<<C-A12 scripts/paperC/c_pass2_check.py NEW>>>
MAN = Path(__file__).resolve().parents[2] / "paper_v1_analysis/number_manifest_C.tsv"  # the manifest of this repository
have = {l.split("\t")[0].replace("−", "-").replace("+", "").replace(",", "") for l in MAN.read_text(encoding="utf-8").splitlines()[1:]}  # normalised as the text tokens are
<<<C-A12 EVIDENCE>>>
Defect, verified: the file at paper HEAD (sha256 a257bd148914…) reads the manifest of the run repository's archive copy by an absolute path, and normalises "−", "+" and "," in the text tokens only. Run unchanged on files 00 to 11 of the after-v4 text it flags 581 tokens, the audit's figure.
After the change, on a scratch copy of the after-v4 tree: 40 tokens. Four are the quantities of audit item 17 (0.025, 0.0125, 22, 33; rows in C-M02). The other 36 are section numbers, dates, years and the like, which the audit read in context.
The path is taken from the script's own place (`scripts/paperC/` is two levels below the repository root), so the checker works wherever the repository is cloned.
The checker only prints a list. It writes no file and changes no number or sentence.
`PROVENANCE.md` l.204 lists the sha256 of this file as copied on 2026-11-01. That table records the copy and is not kept in step with later edits (the section files in it are in the same position), so it is not changed here.
<<<C-A12 END>>>
```

### C-A13. Supplement `readme.txt` (items 10 and 23)

A new file beside the build script. It may be left for the packaging step: `SKIP = ("C-A13",)` in the apply script changes no other target.

```text
<<<C-A13 paper_v1_analysis/tex/readme.txt NEWFILE>>>
Supplementary material for the manuscript
"Retrieved or Random Examples? Preregistered In-Context Captioning in Vietnamese and English"

File: paperC_supp_out.pdf (LaTeX source: paperC_supplement.tex; bibliography: paperC.bib)

The file holds Supplement S, the registered per-run rows and the supporting detail that the
main text refers to. It has no result that the main text does not state. Its parts, in order:

  - Registered per-run rows of the Vietnamese sets
  - All configurations tried
  - Rows not registered for any claim
  - English arm: every registered and reported row
  - Mechanism on the development set (OV-dev-B), dated 2026-10-27
  - Test-run operations (Sections 7 and 8.5)
  - Instrument definitions
  - Context from published systems (Section 8.7)
  - Stage B and the decomposition of InternVL3's contrast (Section 6.7)
  - Disclosure detail (Sections 5.4, 6.8, 7.1, 7.2, 8.1 and 8.5)
  - Demonstration-filtering diagnostic (exploratory, Section 6.9)
  - Flickr30K registration: development rows (Section 8.6)
  - Attribution study (C-ATTR-DEV): every row

The supplement is read with the main text: section and table numbers without the prefix S
refer to the main text.
<<<C-A13 EVIDENCE>>>
The venue card asks for supplementary material with a short `readme.txt`; no such file exists at paper HEAD.
The list is the list of the third-level headings of `11_supplement_registered_rows.md` after package v4, word for word; the first line of the list names the rows that stand before the first such heading. The apply script checks the list against the file.
The file names are those `tex/build.sh` writes. If the files are renamed at upload, the first line follows.
<<<C-A13 END>>>
```

## 3. Dropped, and what is not a block

- **Item 27, DROPPED: the label is registered text.** The registration of the attribution study (v1.1, sha256 prefix `44f81329d418`, l.13) reads: "Label on every output file and every row: `DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY`." Eleven of the 14 printed places are this label on a caption or a stamp (`05` l.136; `06` l.126, 148, 161, 198, 231; `11` l.991, 1003, 1028, 1048, 1120). Registered labels are printed word for word, so they stay. One place is the Box 1 row that defines the name (`05` l.27). The other two places name the registration itself (`05` l.138 "The registration (C-ATTR-DEV, version 1.1)"; `11` l.989, a heading). That is the name under which the registration is filed, and Box 1 defines it for the reader. A reader who looks for the registration needs that name. No change. (Line numbers are those of the after-v4 text.)
- **Item 8, NOT A BLOCK.** See section 5.
- **Item 20, the part not kept.** The audit calls the V4 article the wrong citation. The V7 page asks for it (quote in C-A01), so it stays.
- **Item 19, the part not kept.** The audit proposes to split the tag from the file names. The tag is a suffix that `scripts/paperC/c_pass2_manifest.py` writes (l.200) and reads (l.191: a row is its own if the line ends with the tag). C-M03 puts the tag back at the end of the 29 fields where a file name was later added after it.

## 4. The manifest step (a separate last step)

Run directly after step 1, while step 1 is in the working tree and not yet committed. The script takes the manifest from paper HEAD, checks that the lines before the two freeze rows have the sha256 of CC-408 Ruling 9, that the freeze row (key `decisions LOG::OPS-…`, value `NOT RUN`) and the row for 40 are the last two rows, and that the section files in the working tree are at their targets. It then applies two operations and checks that both freeze rows are unchanged, byte for byte.

### C-M02. Five rows (item 17)

Appended after the two freeze rows. Columns: number, file::key, raw_value, sha256_prefix, status, used_in. The script checks each source again: the registration by its sha256 prefix and the two quotes; the mutant log by its sha256 prefix and its summary line; each LOG line by its id (exactly one line), its sha256 prefix and its quote; and that each number is printed in each file its row names.

```text
<<<C-M02 paper_v1_analysis/number_manifest_C.tsv ROWS>>>
0.025	manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_DEV_PREREG_v1_1.md::§7.4 DETECTED (Holm step-down, family-wise one-sided α = 0.025)	'family-wise one-sided α = 0.025'	44f81329d418	registered text (v1.1)	05_preregistration_and_analysis.md,06_results.md
0.0125	derived::Holm step-down threshold of the smallest p̃ in a family of m = 2 claims = 0.025 / 2 (manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_DEV_PREREG_v1_1.md §7.4: α_j = 0.025 / (m − j + 1))	0.0125	44f81329d418	derived	06_results.md
22	scripts/c_attr/block0/MUTANTS_LOG.txt::summary line	'22/22 killed; survived: none'	a7eef59372d5	log	07_disclosures.md
33	decisions LOG::OPS-1112j-c-attr-1b-g0	'33/33 killed, survived none'	7b67276b8e24	log	07_disclosures.md
73	decisions LOG::OPS-1112bb-c-score-selftest	'73/73 killed; survived: none'	0b0f8e371d61	log	07_disclosures.md
<<<C-M02 EVIDENCE>>>
0.025: registration v1.1 (sha256 prefix 44f81329d418), §7.4, row DETECTED; quote: "the Holm step-down threshold at family-wise one-sided α = 0.025 over the m claims of the row's family". Printed in `05_preregistration_and_analysis.md` l.147 (twice) and `06_results.md` l.178.
0.0125: the same row of the registration; quote: "α_j = 0.025 / (m − j + 1) for the j-th smallest p". For m = 2 and j = 1 this is 0.025 / 2. Printed in `06_results.md` l.178 (InternVL3-8B, m = 2). The status is `derived`, the status of the two existing rows that are computed from a registered text. No result file was opened.
22: `scripts/c_attr/block0/MUTANTS_LOG.txt` in the run repository (sha256 prefix a7eef59372d5, committed in 7e7471f), summary line "22/22 killed; survived: none". This is the laptop record that the sentence of `07_disclosures.md` l.56 describes (LOG line OPS-1111ax-dev-gate02).
33: LOG line OPS-1112j-c-attr-1b-g0 (2026-11-11T19:01:10Z; sha256 prefix of the line 7b67276b8e24): gate g2 on the rented machine, "33/33 killed, survived none", run without network isolation.
73: LOG line OPS-1112bb-c-score-selftest (2026-11-12T11:07:02Z; sha256 prefix of the line 0b0f8e371d61): "73/73 killed; survived: none" on the rented machine. The audit counts 73 as keyed, but the four existing rows for 73 are GPU-second counts and none names `07_disclosures.md`; the row here is the mutant count.
The form of the LOG rows (key `decisions LOG::<id>`, sha256 prefix of the line) is the form of the freeze row that shell C2 appends.
<<<C-M02 END>>>
```

### C-M03. `used_in` pointers (item 19)

Only column 6 (`used_in`) changes; columns 1 to 5 of every existing row are checked to be unchanged. The rule, applied to every row except the two freeze rows and the five new rows:

1. The field is read as a comma-separated list of file names, with at most one tag (`|c-pass2`, `|cc309` or `|c-optionE-1029`).
2. A file name is kept if the file is not a section file of the paper folder, or if the row's value is not a plain number, or if the file still prints the number. Values that are not plain numbers (verdicts, labels, time stamps, hash prefixes, and descriptions such as "0 (rand, OV)" or "PASS (label DETECTED)") are not judged, because the manifest often holds a description and not the printed form; their pointers stay. "Prints" is read generously, so that no valid pointer is lost: the number appears as a token after "−", "+" and "," are normalised, with or without its sign and with or without trailing zeros, code spans and comments included.
3. The field is written as the kept names in their old order, then the tag, at the end. A row whose number is printed nowhere keeps an empty list (as 41 rows already have).

On the after-v4 text with the blocks of this package: 271 pointers go; 258 rows change; 29 tags move to the end of their field; 20 rows are left with no file name. Pointers removed, by file: `06_results.md` 173, `08_english_comparison.md` 38, `00_abstract.md` 20, `07_disclosures.md` 16, `02_related_work.md` 14, `09_limitations.md` 4, `05_preregistration_and_analysis.md` 4, `04_data_and_splits.md` 1, `V2_PROGRESS_C.md` 1. The script pins the four totals. (The audit counted 323 at paper HEAD with a stricter rule; the counts differ by the rule and by the state.)

The column is an index for the reader of the manifest. No tool gates on it, and no printed number depends on it. A judge may strike C-M03 and keep C-M02: `MAN_OPS = ("C-M02",)` in the apply script, with its own pinned target. The cut plan will make further pointers stale; the same function can be run again after it.

## 5. After application: the rebuild (item 8, and what follows from the blocks)

1. **Table 1 (item 8).** No build log is kept in the repository, so the overfull box of 15.9 pt could not be reproduced here without a build, and package v4 adds two rows to Table 1. At the rebuild, read the log of the main build for `Overfull \hbox` lines. If Table 1 still overflows, the fix is in the build, not in the paper text: a narrower first column or `\raggedright` cells for that table in `tex/build.sh` (the script already post-edits the pandoc output for layout). A cell of Table 1 is not shortened for layout: each cell is a checked statement about a cited paper.
2. **Italic code font (item 8).** The warning says that the italic shape of the code font does not exist and the upright shape is used. The output is the intended one. If the warning must go, declare the substitution in `tex/preamble.tex`; this needs a build to test and changes no glyph.
3. **References.** The reference list gains one entry (Krasin et al. 2017) and three entries change form: Hussain et al. gets volume and article number; Yang et al. and Oduwole et al. become proceedings papers, the latter with year 2026. `tex/paperC.bib` is a build copy and is regenerated.
4. **Checker.** After step 2, `python3 -I scripts/paperC/c_pass2_check.py 0*.md 1*.md` in the paper folder should list 36 tokens (section numbers, dates, years, comment text), none of them a quantity.
5. **Readme.** If the cut plan adds or renames a part of the supplement, `tex/readme.txt` follows; the check mode of the apply script fails on a list that differs from the headings.
6. **Words.** The package adds three citation keys and no running text. Nothing is cut.

## 6. For the investigator (not blocks)

None of the nine NOT READY rows needs an answer from the investigator. Two points are for information, with the default this package takes:

1. **The name "C-ATTR-DEV" stays in print** (item 27), because the label is registered text. If the investigator wants a reader-facing name beside it at the rewrite, the two places that are not the label are `05` l.138 and the heading at `11` l.989. Default: no change.
2. **The Open Images reference** (item 20) is the dataset's own "general reference" with the address of the V7 page. Default: as in C-A04.

Still with the investigator or a person's browser, from section 5 of the audit and unchanged by this package: every venue rule on an ACM page (title, abstract, citation style, statistics format, figures, length, TAPS packages, anonymity, prior-publication policy); author block and ORCID; funding, competing interests, CRediT, ethics; repository and archive DOI and the release of per-image scores; pages and DOI of `Nguyen2026FAIR`; the name order of `Vu2025VELVET`; the relation to the conference version.

## 7. Checks run

- `python3 -I -B apply_c_v5_audit.py` (check mode; nothing written): the after-v4 state is built in memory and every file is at the value of section 0; 13 blocks apply, each OLD once and each NEW once; content checks pass; the manifest step passes on the in-memory manifest (whose freeze row carries a dummy stamp, as in the check mode of `apply_c_v2_cc408.py`); every result equals its pinned target. The targets are in the script (`TARGETS`, `MAN_TARGETS`) and in the hand-over note.
- Content checks of the script: every citation key of files 02, 03 and 04 is defined exactly once in the bibliography; the bibliography gains one entry and the audit table one row; each changed entry has balanced braces and each of the four keys has exactly one audit row of five fields; the number tokens of files 02, 03 and 04 are unchanged; the changed checker parses and holds no absolute path; the readme list equals the headings of file 11.
- The changed checker, on a scratch copy of the after-v4 tree: 581 tokens before, 40 after.
- `git status` of the paper repository is unchanged by the checks (only the build files under `tex/` that were already modified, and one untracked draft under `docs/`).
- Not run: any write mode; any build; `c_pass2_manifest.py`, `c_pass2_supp.py`, `build_c_draft.py`.
