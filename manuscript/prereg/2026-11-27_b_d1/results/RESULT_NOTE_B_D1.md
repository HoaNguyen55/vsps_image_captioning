# Result note: Paper B, study D1+A3 (registered result; DEVELOPMENT)

- **Written by:** an agent that is neither the coder of the study nor the writer of the paper's text.
- **Written from:** RESULT_D1.json (sha c2fa610c) and checked against the judge's independent recomputation, out.json (df538c50).
- **Numbers:** every number below has a `d1_*` row in NUMBER_MANIFEST_D1.tsv. Each row gives `file::key`, and the out.json value where one exists.
- **Labels:** DEVELOPMENT, and REGISTERED PREDICTION for H1, H2, H3 and A3. Every p-value and bound is nominal: the three held-out folds share comparisons and files.

## Design in three sentences

1. On the 1,101 development comparisons (KTVIC test, spent references, the authors' own 73 files plus the published-baseline pair), H1 and H2 hold out one unit at a time (`syl`, `pyvi`, `uts`; 18 members each) and let the rest of the development family certify (36 members, or all 54 when `uts` is held out). At equal numbers of claims they count breaks under the held-out unit: FE-CERT against the top claims by z under `f0` (H1), and against Lu et al.'s AER ensemble reading (H2, σ_c fixed). A one-sided exact binomial test on the discordant breaks decides each label, with Holm at 0.05 over four p-values.
2. H3 counts how many certificates over a grid with T fixed at `tw` are lost when the `tm` and `tf` levels are added (k_T of n). The grid is scorer {CIDEr-D, BLEU-4, ROUGE-L} × U {`syl`, `rdr`, `pyvi`} × P × C. NULL needs a one-sided 95% Clopper–Pearson upper bound ≤ 0.05.
3. A3 applies 1,000 exchangeable sign-flip nulls to development comparisons and tests the per-member level under `f0` per direction. AT OR BELOW NOMINAL needs both 97.5% CP upper bounds ≤ 0.040. M1 = M1′ (FE-CERT = Lu's union-of-ties rule plus one convention) is a method check that cannot fail by design.

## Outcome table (labels exactly as registered)

| item | counts | test / bound | label |
|---|---|---|---|
| H1, FE-CERT vs reference-member margin, equal size | b_FE 3 vs b_MG 34, n 37; per fold `syl` 1 vs 12, `pyvi` 1 vs 12, `uts` 1 vs 10 (K 918 / 910 / 909) | one-sided exact p 6.2e-8, Holm reject | **SUPPORTED** |
| H2, FE-CERT vs Lu et al. AER ensemble, equal size | b_FE 3 vs b_AER 11, n 14; per fold 1 vs 5, 1 vs 4, 1 vs 2 | raw one-sided p 0.029 against Holm step 0.05/3 = 0.0167, not rejected; AER-fewer p 0.994 | **NOT SUPPORTED** |
| H3, tone placement beyond a scorer-and-tokenizer grid | k_T 0 of n 782; by unit 0 / 0 / 0 | one-sided 95% CP upper bound 0.0038 (≤ 0.05) | **NULL** |
| H3 DESCRIPTIVE | `syl`-only grid 796; k_U 14; k_TU 14 | — | DESCRIPTIVE |
| A3, per-member level on sign-flip nulls | r_f0⁺ 22/1000 = 0.022; r_f0⁻ 24/1000 = 0.024 | 97.5% CP 0.014–0.033 and 0.015–0.036; both uppers ≤ 0.040 | **AT OR BELOW NOMINAL** |
| A3 DESCRIPTIVE | r_A3 over F_dev 0.015 / 0.014; over F 0.015 / 0.013; max per-member rate over F_dev 0.025 (+), 0.030 (−) | — | DESCRIPTIVE |
| M1 = M1′ | equal on 1,101 of 1,101; mixed-direction all-significant 0 | — | METHOD CHECK |

**H2 DESCRIPTIVE**, at native size, per fold `syl` / `pyvi` / `uts`:
- Claims: FE 918 / 910 / 909; AER 931 / 933 / 931; AER per class 933 / 934 / 933; `f0` 936.
- Flip units: 25 / 18 / 16.
- Held-out flip coverage: FE 0.64 / 0.94 / 0.94; AER 0.44 / 0.61 / 0.75; AER per class 0.48 / 0.61 / 0.75.
- False-tie analogue: FE 0.002 / 0.010 / 0.013; AER 0 / 0 / 0; AER per class 0 / 0.001 / 0.001.
- FRAGILE over G_u: 44 / 52 / 59 of 1,101. The `uts` cell is POST HOC (registration §2).

## What each result allows and forbids

**H1**
- Allowed: the §8 sentence with "3 vs 34", one-sided exact p nominal, REGISTERED PREDICTION, DEVELOPMENT, plus scope: one benchmark, own files, folds share comparisons.
- Forbidden: "FE-CERT is more reliable" without that scope.

**H2**
- Allowed: the counts 3 vs 11 with "not significant after Holm's correction; NOT SUPPORTED". Raw p 0.029 only inside that phrase, with the step 0.0167 beside it. Coverage and false-tie-analogue rows in both directions, labelled DESCRIPTIVE and "not comparable with Lu et al.'s numbers".
- Forbidden:
  - "better than Lu et al." in any form;
  - "fewer breaks than AER" outside the NOT SUPPORTED row;
  - "trend" or "nearly significant";
  - the raw p without Holm;
  - any comparison with Lu's 73%, 72–91%, 66.1% or 88.0%.

**H3**
- Allowed: the §8 NULL sentence verbatim (0 of 782; bound 0.0038) in the abstract and the contributions. The tone axis is qualified wherever it is presented as a Vietnamese choice.
- Forbidden:
  - tone placement or "axes that come from the written language" as an unqualified contribution;
  - any rescue through k_U or FE-LOCUS;
  - the premise "T splits classes only under `syl`/`pyvi`" beyond the 9 toy strings.

**A3**
- Allowed: the §8 sentence with r_f0 and r_A3, with the max per-member rate (0.030 negative) printed beside it. §4.4 "Nominal, not exact" stays.
- Forbidden: "the guarantee is exact"; "A3 confirms the certificate".

**M1 = M1′**
- Allowed: "FE-CERT's decision rule is Lu et al.'s union-of-ties rule applied to the front-end family, with one convention…; checked on all 1,101 comparisons."
- Forbidden: presenting the rule as new.

**Pivot.** Registration §9 fires because H3 is not SUPPORTED. A Paper B pivot review with the PI is due, and no further Paper B study is registered without him. H1, H2 and A3 change the text only.

## Deviations and disclosures

1. **Host.** The host was the PI's own PC under ERRATUM_B_D1_1 (06769fe3), written before use, which replaces the rented-host rule. No hypothesis, threshold, seed or data changed.
2. **Faulted S0.** The one earlier session on a rented host ran S0 only. S0 stopped in its environment part before any data push, and the host was wiped and deleted (erratum header).
3. **Python and Java.** Both are at identical versions (3.12.3; 21.0.13.0.3) but came from other fetch sources, as erratum E2 H3 allows.
4. **Bootstrap draws.** B = 10,000 shared draws, against Lu et al.'s R = 2,000.
5. **σ_c.** σ_c is held fixed across resamples. This is the registration's own convention, because Lu et al. do not specify it.
6. **Break definition.** The break is CI-defined; Lu's flip is point-level. The coverage row is therefore not comparable with theirs.
7. **POST HOC.** The `uts` cell of the FRAGILE-over-G_u row was printed before the registration.
8. **Run custody.** Each stage ran once. G0 passed: 1,101 comparisons, max |diff| 2.8e-14 against tolerance 1e-6, verdict mismatch 0 (G0.json). The labels were independently re-derived by the judge (out.json), with no discrepancy.
9. **Judge's read (POST HOC; for Online Resource 1 only; no label moves).** Its counts are not in RESULT_D1.json and are not used in the text package. The read found that tone levels split classes in all 1,101 comparisons, including under `rdr`.

## Files and shas (read-only copies in ~/vsps_ro3/paperB_d1/)

- **Registration:** PREREG_DRAFT_B_D1_A3_v3.md bf3a55f7; ERRATUM_B_D1_1.md 06769fe3. Commits: registration adebac7; erratum and code fix 2233d21, with b_d1.py 4e044401.
- **Results:** RESULT_D1.json c2fa610c; G0.json 6c4f6664; S1.json 69734f80; PER_IMAGE_D1.npz 2badf5c8 (not committed). Inputs: DEV.json 88ff39aa; RESULT.json 25614b46.
- **Judge:** ruling CC-514 (83c10765…); out.json df538c50.
- **Paper text of record:** rev_2026-11-15/paper.md e8d94fbe (B repo 13549e5).
- **This package:** PACKAGE.diff, paper.md (patched), HUNK_MAP.md, NUMBER_MANIFEST_D1.tsv (built by make_manifest.py), BRIEF.md; shas in SHA256SUMS.
