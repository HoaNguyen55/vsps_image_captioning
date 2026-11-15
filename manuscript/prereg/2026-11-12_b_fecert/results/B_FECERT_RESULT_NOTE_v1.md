HELD from the PI until the Paper B closing line (CC-388 W6); judges and agents only.

# B-FECERT result note v1 (Paper B, LRE): mechanical recomputation of the registered labels

Written at 2026-11-13T18:22:09Z (`date -u`) by the result-note writer agent (launch line OPS-1114g). The writer is not the coder and not a rater. It ran no study code and wrote no paper text. For the one-judge result read of registration l.416. Repository HEAD at writing: `5eee5e3`, branch `paper-v10`.

How to read this note. 'l.N' is line N of the registration `B_FECERT_PREREG_v1_1.md`. A tag such as [n012] points to a row of the table in section 8. Evidence labels are those of registration l.26-32. Verdict words in capitals are copied from the registration. Nothing here is interpreted beyond the registered rule.

## 0. Differences between the recomputed labels and the code's labels

**None.** 58 items are covered: 56 registered items and 2 rows that only the code defines (I-37, I-39). For 44 the recomputed label or value equals what the code wrote. For 0 it differs. 10 could not be recomputed from the files this note may open (the code's value is reported). 2 have no code key to compare with. 2 have no value. The list is in section 2.11.

The 44 equal items are not equally independent of the code. 22 were recomputed from stored statistics or stored values without using a label of the code. 12 rest on the code's own per-comparison or per-case strings: every label that involves the held-out members (the P1 label and its rows, the P2 label, the counts over F, the FE-PRED rows) and the tallies of the planted cases and printed pairs. 10 are record checks (stamps, return codes, presence of fields). The basis of each item is in section 2.11.

### 0.1 Points for the judge (not differences; none is resolved here)

- **J1. Wording of the LOW-SENSITIVITY sentence against the set NC used.** The registered sentence (l.277) says 'in at most 5% of its near-margin certificates'. NC used the fallback set: only 54 certificates of Cert_NC have z_min^NC ≤ 4, which is below 59, so V_NC is all 915 certificates of Cert_NC (I-03). The label follows the rule mechanically. Whether the verbatim sentence may be printed with the words 'near-margin' is for the judge.
- **J2. §11 against §6.1 on what is printed for P1.** Row l.379 reads 'counts and bound only' for INCONCLUSIVE. Line 277 and row K-NC (l.364) say P1 carries LOW-SENSITIVITY 'whatever its outcome'. The §11 row for PASS names the NC figure; the row for INCONCLUSIVE does not. Section 4 gives the candidate sentences with this point marked.
- **J3. Breaks rest on the code's verdict strings.** P1 breaks (I-02, I-05, I-06) and k_FL (I-10, I-11) were recomputed from `RESULT.json::comparisons[i].F`, not from held-out percentiles, which are not stored. The parts that rest on F_dev statistics (V, N, NC, n_FL, the F_dev counts) were recomputed from stored percentiles.
- **J4. One M_new distance lies close to the tolerance.** For ktvic_vittrans, METEOR, the distance is 0.049983 against a tolerance of 0.050000001 (I-17). It is inside. The value is reported so that the judge sees it.
- **J5. K-plant.** 9 of 24 planted cases are IDENTIFIED, fewer than 12 (I-22). By l.298 and l.384 FE-ID is a reproduction table without identification labels. The planted check uses three metrics at one decimal (l.246); the baselines are held to four metrics for non-r* members and five for r* (CC-361 D12). This note draws no conclusion from that.
- **J6. Structural zeros.** In the code rows 'F_without_pk' (I-38) and 'F_held' (I-39), 'significant under f0' and CHANGED are 0 because f0 is not a member of those families. They must not be read as outcomes.
- **J7. Items the registration schedules that have no value yet.** The O5 row beside r* (l.293; I-21) is not produced by stage 3. The matched f0 scores 'Y' of the two baselines (l.382) have no key of their own in FEID.json (section 4, sentence C-P3). 'r for uts' (l.275) has no key of its own (I-09).
- **J8. §17 defaults bind the paper text.** PI-2, PI-3 and PI-6 have no answer on record in the files this note read. Their defaults block several candidate sentences of section 4.
- **J9. Commit timing against the hold.** Committing RESULT.json, FEID.json, V.json, NC.json, DEV.json or this note before the Paper B closing line would put stage figures into the repository history, which the principal investigator can read. See section 7.
- **J10. Calendar.** The calendar row l.416 places stages 2a, 2b and 3 on 11-14 (Vietnam date). Stage 2a started at 22:46 and stage 2b ended at 23:46 Vietnam time on 11-13; stage 3 ended at 00:42 on 11-14. The order rules of l.349 held (S-02). No registered rule makes the calendar date a gate other than K-time.
- **J11. Denominator of 'r for D and for FL separately' (l.275).** The registration does not say whether these two rows are taken within V or within all of Cert_dev. The code takes them within Cert_dev (I-06). Both denominators are in this note: N and its D and FL parts in I-01, Cert_dev and its parts in I-06.
- **J12. Record facts** R1 to R5 of section 5 (a 2-second difference in one LOG line, library count lines in the stdout of stage 3, one PTB lexer warning, the output list of stage 3, a second segmenter value in the census).

## 1. Header

### 1.1 Input files and their pins

Pulled host folder: `.session_backup/2026-11-13/b_stages/host_pull/20261113T174234Z/` (pull 2, LOG line OPS-1114e). Each sha256 was computed for this note and compared with the LOG pin line.

| File (`b_work/`) | sha256 (computed) | Pin line | Equal to the pin |
|---|---|---|---|
| FAMILY.json | `431d92a4a2eaf0516446c9f9aef453ee52d311b6e329d97cd1abb4c4e8017f77` | OPS-1113cr-pin | yes |
| CENSUS.json | `2252167b435890c5dbf70a97e0fc918bc6989c48acda636427d4dd2889599afa` | OPS-1113cs-pin | yes |
| SYSTEMS.tsv | `30ac9555cd6cdc8fd50f47e637e734fac564c692605f590ba213a60a3be6e1a0` | OPS-1113cs-pin | yes |
| GATE2.json | `26110b5f1d87a8369e54e0a696c171698cd980ee6ae1ef2153e8b93c5ee93c61` | OPS-1113cv-pin | yes |
| DEV.json | `88ff39aa9552b671a0e439aec961d0fefe02df1f52a2a5df9765a9d8226f7e8d` | OPS-1113cx-pin | yes |
| NC.json | `1d2e05d2e0098ea1bb11bc7a484b4c158c6ca698b45f9a3929cfe8b0da08428d` | OPS-1113cx-pin | yes |
| V.json | `1f011538bf06a601c2104116ccef31f470eed473b2a96c9e6f8a5408f126f6b9` | OPS-1113dd-pin | yes |
| RESULT.json | `25614b469cf59dc61f15e839b89a8e78ca0b316905afc4bd2ae52eaa0d32b43a` | OPS-1113de-pin | yes |
| FEID.json | `1f56a5ce8c5fd434b19409322d275478ec999d41d34447cfca719a35b040b1f7` | OPS-1114d-pin | yes |

Every input equals its pin: **yes** (9 of 9). FEID.json records `printed_sha256` = 2a962a2b…, the pin of PRINTED.json (OPS-1113df-pin; PIN-1112-b-fecert-printed).

Records read (`b_records/`), with the sha256 computed for this note:

| File | sha256 |
|---|---|
| runs.log | `ea5a6f33451c4444befdeeaa0d1f33aa85ab64be126c40087a36813838f51fe5` |
| PRE_G.txt | `3ad9c6a7e86a8804bd13c06539787700934518c5936182ab5d7b2b5a706aa364` |
| F.stdout | `912f96980809f7e75631388f2a565cbff8520b772a30a65c5a0fe446f59a69e5` |
| C.stdout | `910315f81e9fff23ab7c3583ce5a3728aa36a5c0c3518563760d4a50d4311d16` |
| G.stdout | `97a4fbb38c00823dffdfd3440ac844f1fe321bb3cb0ed8a464c3dde27aaabc8a` |
| 1.stdout | `2fed78d1a4f3d022e3969854620744d7e01694d6792cb370bb1c36a3529b8cba` |
| pin.stdout | `5a7b816459ab861d4219fece7541806ca0e7518f5a5a488b37c77085aa91ff9e` |
| 2a.stdout | `b29805ed94a869601dfff2496c1467f194930eac8b2a8ce00510a1b62ad7ba92` |
| 2b.stdout | `7baec8eb9f96253fdb34c202a26d5604326c52d20519705143f29879508171ed` |
| 3.stdout | `875076818c391fa110403be7248c89a8c2219a679167614d64bc1a060b55fd3c` |
| 3.stderr | `fc07dd11dc9e08ae8267828fe6131f467c2ef0ac0bf602839217da5bbaccba78` |

Also read: the `.rc`, `.args`, `.start`, `.end`, `.time` and `.outputs.sha256` files of F, C, G, 1, pin, 2a, 2b and 3, and the `.rc` files matched by `*.rc`. The stderr files of F, C, G, 1, pin, 2a and 2b are empty.

### 1.2 Registration, code and rulings

| File | sha256 |
|---|---|
| `manuscript/prereg/2026-11-12_b_fecert/B_FECERT_PREREG_v1_1.md` | `736b7e6a8ea2007270a3329db7ad6a09197c4804c9bc3821ea6bd4ceb5a61aa0` |
| `scripts/b_fecert/b_fecert.py` | `67e43dea1b37c3bbfaa3fe5081d6f3d36848397451ad0a24d67fa67389b06b59` |
| `scripts/b_fecert/family.py` | `7cb2c69b8b7840388568fd5f9b248e2cf25df28185386be875a65d921a9e4178` |
| `scripts/b_fecert/READ_PACKAGE.md` | `acb0b7915651866dc7c9dced1bbf6aff88ab3ed4babd21e531583e85b798826c` |
| `.session_backup/2026-10-13/decisions/CC-350.txt` | `f4e05e266059340636cdef47b49f7e0b4e7b9e4d4ce4d2a4f417995370eda493` |
| `.session_backup/2026-10-13/decisions/CC-353.txt` | `4198ee6f6bd03d793f72fd1979ece34684a4637e9138cd1b9328dda9d3737133` |
| `.session_backup/2026-10-13/decisions/CC-354.txt` | `0df1c34a5aef5d47a81a638d4abe5fec36369b896e3f7de64e44393268f78647` |
| `.session_backup/2026-10-13/decisions/CC-361.txt` | `86da758825948b3afb122b4610ca8a826cfb417708486aa55518ccfbb86b198c` |
| `.session_backup/2026-10-13/decisions/CC-384.txt` | `8f9cc73ececc5a6a8263fc460fa086dc775ac8948b9c34df7b3aa3bdf8f0e423` |
| `.session_backup/2026-10-13/decisions/CC-385.txt` | `400e04250728248f976fd6ddf80f4c9782f8840b366318aa7772fdaf166a53a8` |
| `.session_backup/2026-10-13/decisions/CC-388.txt` | `d4053e424ad0438fbf25d6edb98e7b86b73f0ead0b16cd74daa68739e802c603` |
| `.session_backup/2026-10-13/decisions/CC-390.txt` | `85fec22eec6df593df42a4b7c2a6d0f95bfbf87a725e1a147f1246d2bd459a9b` |

The registration and the two code files are unchanged in the working tree against HEAD (`git status` shows no change under their folders). The stage-0b commit of the code is 9e6578a (CC-385 GO 88).

### 1.3 LOG pin lines

Read with `grep -n '<id>-pin' … | cut -c1-400`. The last column is the sha256 of the line text itself (the single line that starts with the stamp and the id), so that a later change of a pin line can be seen.

| Pin id | LOG line | Stamp (UTC) | Files and sha256 the line carries | sha256 of the line text |
|---|---|---|---|---|
| OPS-1113cr-pin | 2508 | 2026-11-13T15:14:18Z | FAMILY.json 431d92a4… | `4a264bd29b0a066e7a59dfb84475e3b38a3bccbc6f4f6f4fe3c98b9618bb83e9` |
| OPS-1113cs-pin | 2509 | 2026-11-13T15:14:31Z | CENSUS.json 2252167b…; SYSTEMS.tsv 30ac9555… | `00a7057cfbc3661502cbc0ac7417d20a32e79df84211c5b3ba746779d7d90eb4` |
| OPS-1113cv-pin | 2512 | 2026-11-13T15:15:25Z | GATE2.json 26110b5f… | `2e68774b4f580e8c984704505bb7a8075cf908ed2f0102da703218484e873b3d` |
| OPS-1113cx-pin | 2515 | 2026-11-13T15:44:18Z | DEV.json 88ff39aa…; NC.json 1d2e05d2…; PAIR_CANDIDATES.json 2274d989… (that file was not opened or hashed for this note) | `9ed70bc17ff913d27625323e779e49e89bccdbbec17f9d89fddab4905cb25dd9` |
| OPS-1113dd-pin | 2522 | 2026-11-13T15:50:07Z | V.json 1f011538… | `33bfe02de6b6596840afc000b3dca7b0770eb3b8f90cc50866662137ab81a689` |
| OPS-1113de-pin | 2525 | 2026-11-13T16:47:09Z | RESULT.json 25614b46… | `9c0042f69607af344e22a412016fa30db1e5000f61045f7071ba67a56a675de0` |
| OPS-1113df-pin | 2526 | 2026-11-13T16:48:25Z | PRINTED.json 2a962a2b… (not opened for this note) | `0fe145befaff7936004d8b6234893582ef2fc71290d37f4314246e4590e7a55d` |
| OPS-1114d-pin | 2533 | 2026-11-13T17:42:28Z | FEID.json 1f56a5ce… | `e83ff0db481561959bf622c4ee7efdae2ee06af1db8b4e6a631e85de2ed2f342` |

### 1.4 Stages run (from `b_records/runs.log`)

| Step | Start (UTC) | End (UTC) | Wall time (s) | rc | Output |
|---|---|---|---|---|---|
| F | 2026-11-13T15:13:36Z | 2026-11-13T15:13:56Z | 20.34 | 0 | FAMILY.json |
| C | 2026-11-13T15:14:22Z | 2026-11-13T15:14:22Z | 0.70 | 0 | SYSTEMS.tsv, CENSUS.json |
| G | 2026-11-13T15:14:52Z | 2026-11-13T15:14:53Z | 0.84 | 0 | GATE2.json |
| 1 | 2026-11-13T15:15:29Z | 2026-11-13T15:43:34Z | 1685.51 | 0 | DEV.json, NC.json, PAIR_CANDIDATES.json |
| pin | 2026-11-13T15:44:05Z | 2026-11-13T15:44:05Z | 0.66 | 0 | read-only copies of DEV.json and NC.json; the pin line text |
| build | 2026-11-13T15:45:39Z | 2026-11-13T15:45:44Z | 4.41 | 0 | pair files of the human arm (not opened; section 5) |
| 2a | 2026-11-13T15:46:36Z | 2026-11-13T15:49:47Z | 190.41 | 0 | V.json |
| 2b | 2026-11-13T15:50:11Z | 2026-11-13T16:46:31Z | 3380.12 | 0 | RESULT.json |
| 3 | 2026-11-13T16:48:41Z | 2026-11-13T17:42:10Z | 3209.15 | 0 | FEID.json, PLANT_KEY.json, PLANT_PRINTED.json |

The five G0 checks (self-test, pair-builder self-test twice, mutants, toy environment) ran before the data push, 2026-11-13T14:45:09Z to 14:47:33Z, all rc 0 (LOG line OPS-1113ck). All registered stages F, C, G, 1, 2a, 2b and 3 ran once, on one rented host, CPU only, on 2026-11-13 (UTC). Stage H has not run.

### 1.5 What this note opened and did not open

- Opened read-only: the registration (all of it); b_fecert.py (l.1-150, l.289-672, l.945-1444), family.py and READ_PACKAGE.md (in full); rulings CC-388 (in full), CC-390 (in full, lines cut at 330 characters), CC-385 (l.72-249), and the first 12 lines plus grep hits of CC-350, CC-353, CC-354, CC-361, CC-384 and CC-385 (cut at 260 characters); the nine work files of 1.1; the records of 1.1.
- LOG.md: by `grep -n '<id>' | cut`, never above 2,500 characters per line. In addition, for the eight pin lines of 1.3 an anchored grep of the line was piped to `sha256sum`, `wc -c`, `grep -c` and `cut -c1-20` to hash it, count it and read its stamp; nothing beyond the stamp was displayed by those calls. This is a departure from the plain `grep | cut` form. Ids read: the pin ids of 1.3; OPS-1113ch to OPS-1113cz, OPS-1113da, OPS-1113dg, OPS-1114e, OPS-1114f, OPS-1114g; OPS-1113br; PIN-1112-b-fecert-printed; PI-1113g (300 characters). Lines of other papers that fall in the id range were seen to 260 characters only and are not used.
- One listing to disclose: an `ls` of the registration folder at the start showed the name and size of the repository copy of PRINTED.json. The file was not opened or hashed.
- Not opened, not listed, not hashed: PAIR_CANDIDATES.json, PLANT_KEY.json, PLANT_PRINTED.json, build.stdout, build.stderr, any pair or label folder, any key, assignment, practice or label file, the sealed folders, pilot_results.json, any `*.preds.json`, any data set file. Not opened and not hashed: PRINTED.json (either copy). The sha256 of PLANT_KEY.json quoted in section 7 is copied from `3.outputs.sha256`.
- Caption text: no field with caption text of a data set or of a system output was met. `FAMILY.json::F3` holds the registered toy strings (not data); they are not copied. `FEID.json::printed_comparisons.pairs[i].x` and `.y` hold system names as printed in the two public sources; they are not captions.
- Computation: small read-only Python on the JSON files (`python3 -I`), standard library only, no study module imported, no bootstrap, no scoring. The script is in Appendix A.

### 1.6 Statuses used in section 2

- **EQUAL**: the label or value recomputed here equals what the code wrote (or enforced by its return code).
- **DIFFERENT**: it does not. Listed in section 0.
- **NOT RECOMPUTABLE (code value reported)**: the inputs of the rule are not stored in the files this note may open.
- **NO CODE KEY (recomputed only)**: recomputed here; the code wrote no key of its own to compare with.
- **NO VALUE**: no value exists yet.

## 2. Registered items: rule, quantities, recomputed label, code label

Each block has: (a) the registered rule with its line number; (b) the quantities with `file::key`, value and evidence label; (c) the label recomputed by this note; (d) the label the code wrote; (e) equal or not. A tag such as [n012] points to the row of section 8.

### 2.0 The decision rule used in every certificate (registration §3.2)

- l.160: "sig+(f): L_f > 0. sig−(f): U_f < 0."
- l.161: "**CERTIFIED (a > b over G)**: sig+(f) for every class f of G. **CERTIFIED (b > a)**: sig−(f) for every class. The output names the direction."
- l.162: "**REVERSED**: sig+ under some member and sig− under another."
- l.163: "**FRAGILE**: not certified, and significant under at least one member (REVERSED is a subset)."
- l.164: "**NULL-STABLE**: significant under no member."
- l.167: "**CHANGED (the conclusion changes)**: the comparison is significant under f0 and not CERTIFIED over G. Its denominator is the number of comparisons significant under f0."

Stored statistics. For every comparison and every class, `DEV.json::comparisons[i].classes[k].cider` and `V.json::fl[i].classes[k].cider` hold four numbers: D_f, the 2.5th percentile, the 97.5th percentile and sd_boot. They cover the 54 members of F_dev only. The statistics of the held-out members are not stored in any file this note may open. `RESULT.json::comparisons[i]` holds, per comparison, the verdict strings over F and over F_dev, D under f0 and the CHANGED flag.

## 2.1 P1, held-out front-end check

### I-01. P1 verdict set V

(a) l.269: "Cert_dev = every comparison in D ∪ FL that is CERTIFIED over F_dev. Margin of a certified comparison: z_min = the smallest, over the classes of F_dev, of |D_f| / sd_boot(D_f). **Verdict set** V = the certified comparisons with z_min ≤ 4 (near-margin). If |V| < 59, V = Cert_dev"

(b) Quantities:

| Quantity | file::key | Value | Evidence label |
|---|---|---|---|
| D comparisons | `DEV.json::comparisons` (length) | 1101 [n001] | DEVELOPMENT |
| FL comparisons (formed) | `V.json::fl` (length) | 22 [n002] | FIRST SCORING OF RELEASED OUTPUTS |
| Cert_dev | `V.json::cert_dev` | 918 [n003] | DEVELOPMENT (D part), FIRST SCORING OF RELEASED OUTPUTS (FL part) |
| Cert_dev, FL part | `V.json::cert_dev_FL` | 9 [n004] | FIRST SCORING OF RELEASED OUTPUTS |
| Certified with z_min ≤ 4 | derived from the class statistics | 72 [n005] | as Cert_dev |
| N = \|V\| | `V.json::N` | 72 [n006] | as Cert_dev |
| V, D part / FL part | derived from `V.json::V` (ids) | 68 [n007] / 4 [n008] | DEVELOPMENT / FIRST SCORING OF RELEASED OUTPUTS |
| Set used | `V.json::rule` | "near-margin z_min <= 4" | DESCRIPTIVE |
| Classes with sd_boot = 0 | derived | 0 [n009] | DESCRIPTIVE |

(c) Recomputed. Step 1: for each of the 1101 + 22 comparisons, sig per class of F_dev from the stored percentiles (l.160). Step 2: CERTIFIED when every class has the same non-zero sig (l.161): 918 comparisons, 9 of them in FL. Step 3: z_min = smallest |D_f| / sd_boot over the classes of F_dev. Step 4: 72 certified comparisons have z_min ≤ 4. Step 5: 72 is not below 59, so V is the near-margin set and N = 72. The recomputed id list equals `V.json::V` in content and in order: yes.

(d) Code: `V.json::cert_dev` = 918, `cert_dev_FL` = 9, `N` = 72, `rule` = "near-margin z_min <= 4", `V` = 72 ids.

(e) EQUAL.

### I-02. P1 label

(a) l.271: "The certified direction is not significant under at least one class of F_held."

l.272: "r = breaks / N, N = |V|."

l.273: "N < 59 (59 is the smallest N for which zero breaks give a one-sided 95% Clopper–Pearson upper bound below 0.05): NOT_EVALUABLE. If the one-sided 95% Clopper-Pearson upper bound <= 0.05: **PASS** ("certificates on the development family held under the held-out front ends in this pool"). Lower one-sided 95% bound > 0.05: **FAIL** ("the development family does not cover the front-end variation that matters"). Otherwise: **INCONCLUSIVE**."

(b) Quantities:

| Quantity | file::key | Value | Evidence label |
|---|---|---|---|
| N | `RESULT.json::P1.N` | 72 [n010] | DEVELOPMENT + FIRST SCORING OF RELEASED OUTPUTS (set fixed on F_dev before stage 2b) |
| breaks | `RESULT.json::P1.breaks` | 2 [n011] | HELD-OUT FRONT END |
| r | `RESULT.json::P1.r` | 0.0278 [n012] | HELD-OUT FRONT END |
| one-sided 95% Clopper–Pearson upper bound | `RESULT.json::P1.cp_upper_95` | 0.0849 [n013] | HELD-OUT FRONT END |
| one-sided 95% Clopper–Pearson lower bound | `RESULT.json::P1.cp_lower_95` | 0.0050 [n014] | HELD-OUT FRONT END |
| held-out units | `RESULT.json::units.held` | ['uts'] | HELD-OUT FRONT END |
| label | `RESULT.json::P1.label` | INCONCLUSIVE | REGISTERED PREDICTION (code key `P1.evidence` = "REGISTERED PREDICTION") |

(c) Recomputed. Step 1: N = 72 (I-01). Step 2: a comparison certified over F_dev breaks exactly when it is not CERTIFIED over F, because F = F_dev plus the held-out members and the classes of F_dev are already significant in the certified direction. The verdict string over F of `RESULT.json::comparisons` is not CERTIFIED for 2 of the 72 ids of V (ids: `D:p1assist_s43-detailed|tags_p1_s43-detailed`, `FL:G2:G2_cnn_t5|G2_vit_t5`; both strings are FRAGILE). So breaks = 2. Step 3: r = 2/72 = 0.0278. Step 4: Clopper–Pearson bounds by bisection on the binomial tail (standard library only): upper 0.084869, lower 0.004958. Check of the method against l.273: zero breaks give an upper bound of 0.04951 at N = 59 and 0.05034 at N = 58. Step 5: N is not below 59. The upper bound is above 0.05, so not PASS. The lower bound is not above 0.05, so not FAIL. Label: **INCONCLUSIVE**.

Limit of this recomputation: breaks were derived from the code's own per-comparison verdict strings over F. The held-out class statistics are not stored, so the significance under each held-out class could not be recomputed from percentiles.

(d) Code: `RESULT.json::P1.label` = **INCONCLUSIVE**; N = 72, breaks = 2, r = 0.027777777777777776, cp_upper_95 = 0.08486917446626821, cp_lower_95 = 0.004957895842999783.

(e) EQUAL (bounds agree to better than 1e-9).

### I-03. Sensitivity control NC

(a) l.277: "On D only, with the verdict-set rule of P1: Cert_NC = the D comparisons CERTIFIED over the 18 `syl` members; z_min^NC = the smallest, over the `syl` classes, of |D_f| / sd_boot(D_f); V_NC = the comparisons of Cert_NC with z_min^NC <= 4; if |V_NC| < 59, V_NC = Cert_NC. A break is: the certified direction is not significant under at least one `rdr` or `pyvi` class. r_NC = breaks / |V_NC|. NC.json records which set was used and |V_NC|. If |V_NC| < 59 after the fallback, NC is NOT_EVALUABLE and P1 carries the words 'sensitivity not measured'. If r_NC <= 0.05, P1 is labelled LOW-SENSITIVITY whatever its outcome: 'a one-unit family was broken by the other development units in at most 5% of its near-margin certificates, so the held-out check had little room to fail'."

(b) Quantities (all on D, F_dev members only):

| Quantity | file::key | Value | Evidence label |
|---|---|---|---|
| Cert_NC | `NC.json::cert_NC` | 915 [n015] | DEVELOPMENT |
| Cert_NC with z_min^NC ≤ 4 | derived from `DEV.json` class statistics | 54 [n016] | DEVELOPMENT |
| \|V_NC\| | `NC.json::V_NC` | 915 [n017] | DEVELOPMENT |
| Set used | `NC.json::rule` | "fallback: all of Cert" | DESCRIPTIVE |
| breaks | `NC.json::breaks` | 6 [n018] | DEVELOPMENT |
| r_NC | `NC.json::r_NC` | 0.0066 [n019] | DEVELOPMENT |
| status | `NC.json::status` | LOW-SENSITIVITY | DEVELOPMENT (code key `label` = "SENSITIVITY CONTROL (§6.1 NC)") |

(c) Recomputed. Step 1: 915 D comparisons are CERTIFIED over the 18 `syl` members. Step 2: 54 of them have z_min^NC ≤ 4. Step 3: 54 is below 59, so the fallback applies and V_NC = Cert_NC, |V_NC| = 915. Step 4: |V_NC| is not below 59, so NC is evaluable. Step 5: in 6 comparisons of V_NC the certified direction is not significant under at least one `rdr` or `pyvi` class. Step 6: r_NC = 6/915 = 0.0066, which is ≤ 0.05. Status: **LOW-SENSITIVITY**.

(d) Code: `NC.json::status` = **LOW-SENSITIVITY**; cert_NC = 915, V_NC = 915, rule = "fallback: all of Cert", breaks = 6, r_NC = 0.006557377049180328.

(e) EQUAL. See point J1 of section 0.1 on the wording of the registered sentence.

### I-04. P1 carries the NC words (K-NC)

(a) l.277: "If |V_NC| < 59 after the fallback, NC is NOT_EVALUABLE and P1 carries the words 'sensitivity not measured'. If r_NC <= 0.05, P1 is labelled LOW-SENSITIVITY whatever its outcome: 'a one-unit family was broken by the other development units in at most 5% of its near-margin certificates, so the held-out check had little room to fail'."

l.364: "| K-NC | r_NC ≤ 0.05 | P1 carries LOW-SENSITIVITY |"

(b) `NC.json::status` = LOW-SENSITIVITY; `NC.json::r_NC` = 0.0066 [n019].

(c) Recomputed: NC is evaluable and r_NC ≤ 0.05, so P1 carries **LOW-SENSITIVITY** whatever its outcome. The words 'sensitivity not measured' do not apply.

(d) Code: `RESULT.json::P1.NC` = "LOW-SENSITIVITY"; key `P1.LOW-SENSITIVITY` is present and holds the registered sentence; key `P1.words` is absent.

(e) EQUAL.

### I-05. P1 FL row

(a) l.274: "**FL row (reported with its own Clopper–Pearson interval, no verdict).** r over the FL comparisons in Cert_dev. If its lower one-sided 95% bound exceeds 0.05, the paper states this beside the P1 label whatever the label is."

(b) Quantities:

| Quantity | file::key | Value | Evidence label |
|---|---|---|---|
| FL comparisons in Cert_dev | `RESULT.json::P1_beside.FL_row.n` | 9 [n020] | FIRST SCORING OF RELEASED OUTPUTS |
| breaks | `RESULT.json::P1_beside.FL_row.breaks` | 1 [n021] | FIRST SCORING OF RELEASED OUTPUTS, HELD-OUT FRONT END |
| lower one-sided 95% bound | `RESULT.json::P1_beside.FL_row.cp_lower_95` | 0.0057 [n022] | FIRST SCORING OF RELEASED OUTPUTS, HELD-OUT FRONT END |
| upper one-sided 95% bound | `RESULT.json::P1_beside.FL_row.cp_upper_95` | 0.4291 [n023] | FIRST SCORING OF RELEASED OUTPUTS, HELD-OUT FRONT END |

(c) Recomputed: 9 FL comparisons are certified over F_dev; 1 of them is not CERTIFIED over F (`FL:G2:G2_cnn_t5|G2_vit_t5`). Bounds: lower 0.005683, upper 0.429136. The lower bound does not exceed 0.05, so the statement beside the P1 label is not required. No verdict.

(d) Code: n = 9, breaks = 1, cp_lower_95 = 0.005683044988048048, cp_upper_95 = 0.42913554703143447, state_beside_P1 = False.

(e) EQUAL (same limit as I-02: breaks from the code's verdict strings).

### I-06. P1 rows reported beside it: all of Cert_dev, D, FL

(a) l.275: "**Reported beside it (no verdict):** r over all of Cert_dev; r for D and for FL separately; r for `uts`, and DESCRIPTIVE 'with chr' rows (chr members added to F_held), no verdict; the reversal count."

(b) and (c):

| Row | file::key | Code value | Recomputed | Evidence label |
|---|---|---|---|---|
| all of Cert_dev: n | `RESULT.json::P1_beside.all_Cert_dev.n` | 918 [n024] | 918 | DEVELOPMENT + FIRST SCORING OF RELEASED OUTPUTS |
| all of Cert_dev: breaks | `RESULT.json::P1_beside.all_Cert_dev.breaks` | 2 [n025] | 2 | HELD-OUT FRONT END |
| D: breaks (of 909 [n026] certified) | `RESULT.json::P1_beside.D_only.breaks` | 1 [n027] | 1 | DEVELOPMENT, HELD-OUT FRONT END |
| FL: breaks (of 9 certified) | `RESULT.json::P1_beside.FL_only.breaks` | 1 [n028] | 1 | FIRST SCORING OF RELEASED OUTPUTS, HELD-OUT FRONT END |

The ids of the comparisons in Cert_dev that are not CERTIFIED over F: `D:p1assist_s43-detailed|tags_p1_s43-detailed`, `FL:G2:G2_cnn_t5|G2_vit_t5`. Both are in V. No verdict.

(d) Code: the values in the table. The code stores no denominator for the D row; it is derived here.

(e) EQUAL (same limit as I-02).

### I-07. P1 reversal count

(a) l.271: "**Reversal** (reported inside the break count): significant in the opposite direction, or a point-sign flip, under a held-out class."

(b) `RESULT.json::P1.reversals` = 0 [n029] (HELD-OUT FRONT END); `P1_beside.all_Cert_dev.reversals` = 0; `D_only.reversals` = 0; `FL_only.reversals` = 0.

(c) Not recomputable in full. The part 'significant in the opposite direction' can be read from the verdict strings: both breaks are FRAGILE over F, not REVERSED, so that part is 0. The part 'a point-sign flip under a held-out class' needs D_f under the held-out classes, which is not stored.

(d) Code: reversals = 0.
(e) NOT RECOMPUTABLE (code value reported).

### I-08. P1 'with chr' row

(a) l.275: "DESCRIPTIVE 'with chr' rows (chr members added to F_held), no verdict"

(b) `RESULT.json::P1_beside.with_chr_DESCRIPTIVE`: N = 72, breaks = 16 [n030], reversals = 3 [n031]. Label: DESCRIPTIVE; `chr` is not in F (l.133).

(c) Not recomputable: the statistics of the `chr` and `uts` classes are not stored.
(d) Code: the values above.
(e) NOT RECOMPUTABLE (code value reported).

### I-09. P1 'r for uts'

(a) l.275: "r for `uts`"

(b) `RESULT.json::units.held` = ['uts']; `FAMILY.json::units_dropped` = []; `CENSUS.json::uts_moved_to_dev` = False.

(c) F_held holds the 18 `uts` members and nothing else, so r for `uts` is the P1 estimand itself: 2/72.

(d) Code: no separate key.
(e) NO CODE KEY (recomputed only).

## 2.2 P2, conclusions that change on other groups' outputs

### I-10. P2 label

(a) l.282: "Over FL: n_FL = comparisons significant under f0; k_FL = those CHANGED over F (§3.2)."

l.283: "n_FL < 10: NOT_EVALUABLE (counts reported, no label). k_FL ≥ 3 and k_FL / n_FL ≥ 0.10: **SUPPORTED** ("the front end changes the conclusion of k of n significant comparisons among other groups' released outputs"). Otherwise: **NOT SUPPORTED**, reported as "the certificate changed few conclusions in this pool (k of n)"."

(b) Quantities:

| Quantity | file::key | Value | Evidence label |
|---|---|---|---|
| formed FL comparisons | `GATE2.json::formed` | 22 [n032] | DESCRIPTIVE (structure only) |
| n_FL | `RESULT.json::P2.n_FL` | 10 [n033] | FIRST SCORING OF RELEASED OUTPUTS |
| k_FL | `RESULT.json::P2.k_FL` | 2 [n034] | FIRST SCORING OF RELEASED OUTPUTS; F includes the HELD-OUT FRONT END members |
| k_FL / n_FL | `RESULT.json::counts.FL_over_F.CHANGED_share` | 0.2000 [n035] | FIRST SCORING OF RELEASED OUTPUTS |
| label | `RESULT.json::P2.label` | NOT SUPPORTED | REGISTERED PREDICTION (code key `P2.evidence` = "REGISTERED PREDICTION") |

(c) Recomputed. Step 1: sig under f0 from the class of `V.json::fl[i].classes` that holds member `rdr.tw.pk.cf`: non-zero for 10 of the 22 FL comparisons, so n_FL = 10. Step 2: of these, 2 are not CERTIFIED over F by the verdict string of `RESULT.json::comparisons`, so k_FL = 2 (ids: `FL:G2:G2_cnn_lstm|G2_cnn_t5`, `FL:G2:G2_cnn_t5|G2_vit_t5`). Step 3: n_FL is not below 10, so the rule is evaluable. Step 4: k_FL ≥ 3 is false (2 < 3); k_FL / n_FL = 0.2000 is ≥ 0.10. Both conditions are needed. Label: **NOT SUPPORTED**.

(d) Code: `RESULT.json::P2.label` = **NOT SUPPORTED**; n_FL = 10, k_FL = 2.

(e) EQUAL (k_FL uses the code's verdict strings over F; n_FL is recomputed from stored percentiles).

### I-11. P2 per repository and leave-one-out

(a) l.284: "k_FL per repository and with each repository left out"; l.204: "Every FL count is reported per repository and with each repository left out in turn (§6.2)."

(b) and (c):

| Repository (owner) | file::key | n (significant under f0) | k (CHANGED over F) | Recomputed n, k | Evidence label |
|---|---|---|---|---|---|
| loc110504 | `RESULT.json::P2.per_repository_n_k.loc110504` | 9 [n036] | 2 [n037] | 9, 2 | FIRST SCORING OF RELEASED OUTPUTS |
| vanngthi | `RESULT.json::P2.per_repository_n_k.vanngthi` | 1 [n038] | 0 [n039] | 1, 0 | FIRST SCORING OF RELEASED OUTPUTS |
| all but loc110504 | `RESULT.json::P2.leave_one_repository_out.loc110504` | 1 [n040] | 0 [n041] | 1, 0 | FIRST SCORING OF RELEASED OUTPUTS |
| all but vanngthi | `RESULT.json::P2.leave_one_repository_out.vanngthi` | 9 [n042] | 2 [n043] | 9, 2 | FIRST SCORING OF RELEASED OUTPUTS |

Formed comparisons per repository (`GATE2.json::comparisons[i].repo`): loc110504: 20 [n044]; vanngthi: 2 [n045].

(d) Code: the values in the table.
(e) EQUAL.

### I-12. Always-reported counts over F_dev (D and FL)

(a) l.284: "**Always reported:** the counts of CERTIFIED, FRAGILE, REVERSED and NULL-STABLE over F and over F_dev;"; l.284: "the same counts for D, labelled DEVELOPMENT"

(b), (c) and (d). Recomputed from the stored percentiles of every class of F_dev. FRAGILE includes REVERSED (l.163).

| Row | file::key | comparisons | CERTIFIED | FRAGILE | REVERSED | NULL-STABLE | significant under f0 | CHANGED | CHANGED share | point-sign flips | Recomputed equal | Evidence label |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D_over_F_dev_DEVELOPMENT | `RESULT.json::counts.D_over_F_dev_DEVELOPMENT` | 1101 [n046] | 909 [n047] | 59 [n048] | 2 [n049] | 133 [n050] | 936 [n051] | 27 [n052] | 0.0288 [n053] | 58 [n054] | yes | DEVELOPMENT |
| FL_over_F_dev | `RESULT.json::counts.FL_over_F_dev` | 22 [n055] | 9 [n056] | 6 [n057] | 0 [n058] | 7 [n059] | 10 [n060] | 1 [n061] | 0.1000 [n062] | 3 [n063] | yes | FIRST SCORING OF RELEASED OUTPUTS |

The same rows are also stored at `DEV.json::counts_F_dev` and `V.json::counts_FL_F_dev`; both equal the rows above (yes).

(e) EQUAL.

### I-13. Always-reported counts over F (D and FL)

(a) l.284: "**Always reported:** the counts of CERTIFIED, FRAGILE, REVERSED and NULL-STABLE over F and over F_dev;"

(b), (c) and (d). Tallied from the code's per-comparison verdict strings over F (`RESULT.json::comparisons[i].F`) and from sig under f0 recomputed from the stored percentiles. This checks that the summary row agrees with the per-comparison strings. It is not an independent recomputation of the verdicts over F.

| Row | file::key | comparisons | CERTIFIED | FRAGILE | REVERSED | NULL-STABLE | significant under f0 | CHANGED | CHANGED share | point-sign flips (code only) | Tally equal | Evidence label |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D_over_F_DEVELOPMENT | `RESULT.json::counts.D_over_F_DEVELOPMENT` | 1101 [n064] | 908 [n065] | 62 [n066] | 2 [n067] | 131 [n068] | 936 [n069] | 28 [n070] | 0.0299 [n071] | 65 [n072] | yes | DEVELOPMENT; F includes the HELD-OUT FRONT END members |
| FL_over_F | `RESULT.json::counts.FL_over_F` | 22 [n073] | 8 [n074] | 8 [n075] | 0 [n076] | 6 [n077] | 10 [n078] | 2 [n079] | 0.2000 [n035] | 3 [n080] | yes | FIRST SCORING OF RELEASED OUTPUTS; F includes the HELD-OUT FRONT END members |

Verdict strings over F by direction. D: CERTIFIED (a > b) 536 [n081], CERTIFIED (b > a) 372 [n082], FRAGILE 60 [n083], NULL-STABLE 131 [n084], REVERSED 2 [n085]. FL: CERTIFIED (a > b) 3 [n086], CERTIFIED (b > a) 5 [n087], FRAGILE 8 [n088], NULL-STABLE 6 [n089]. (These are counts of the strings in `RESULT.json::comparisons[i].F`; they sum to the table rows.)

The pair of the two KTVIC baselines (in D, l.186): over F_dev "CERTIFIED (b > a)", over F "CERTIFIED (b > a)"; in V: no. Label: DEVELOPMENT. The pair names two published systems, so in paper text the defaults of §17 PI-3 and PI-6 apply (section 4).

(e) EQUAL (tally of code strings; point-sign flips over F are not recomputable).

FL comparisons one by one (ids are this project's internal file codes; the id is `FL:<group>:<a>|<b>`, written here with ' / ' for the bar; the order a, b fixes the direction words):

| id | repository | images n | verdict over F_dev (recomputed = code) | verdict over F (code) | sig under f0 (recomputed) | CHANGED over F | in V |
|---|---|---|---|---|---|---|---|
| `FL:G1:X4a / X4b` | loc110504 | 578 | NULL-STABLE | NULL-STABLE | 0 | no | no |
| `FL:G1:X4a / X4c` | loc110504 | 578 | CERTIFIED (b > a) | CERTIFIED (b > a) | − | no | yes |
| `FL:G1:X4a / X4d` | loc110504 | 578 | CERTIFIED (b > a) | CERTIFIED (b > a) | − | no | no |
| `FL:G1:X4a / X4e` | loc110504 | 578 | NULL-STABLE | NULL-STABLE | 0 | no | no |
| `FL:G1:X4b / X4c` | loc110504 | 578 | FRAGILE | FRAGILE | 0 | no | no |
| `FL:G1:X4b / X4d` | loc110504 | 578 | CERTIFIED (b > a) | CERTIFIED (b > a) | − | no | no |
| `FL:G1:X4b / X4e` | loc110504 | 578 | NULL-STABLE | NULL-STABLE | 0 | no | no |
| `FL:G1:X4c / X4d` | loc110504 | 578 | CERTIFIED (b > a) | CERTIFIED (b > a) | − | no | no |
| `FL:G1:X4c / X4e` | loc110504 | 578 | NULL-STABLE | NULL-STABLE | 0 | no | no |
| `FL:G1:X4d / X4e` | loc110504 | 578 | CERTIFIED (a > b) | CERTIFIED (a > b) | + | no | no |
| `FL:G2:G2_cnn_lstm / G2_cnn_lstm_attention` | loc110504 | 279 | NULL-STABLE | FRAGILE | 0 | no | no |
| `FL:G2:G2_cnn_lstm / G2_cnn_t5` | loc110504 | 279 | FRAGILE | FRAGILE | + | yes | no |
| `FL:G2:G2_cnn_lstm / G2_qwen2` | loc110504 | 279 | FRAGILE | FRAGILE | 0 | no | no |
| `FL:G2:G2_cnn_lstm / G2_vit_t5` | loc110504 | 279 | NULL-STABLE | NULL-STABLE | 0 | no | no |
| `FL:G2:G2_cnn_lstm_attention / G2_cnn_t5` | loc110504 | 279 | CERTIFIED (a > b) | CERTIFIED (a > b) | + | no | yes |
| `FL:G2:G2_cnn_lstm_attention / G2_qwen2` | loc110504 | 279 | FRAGILE | FRAGILE | 0 | no | no |
| `FL:G2:G2_cnn_lstm_attention / G2_vit_t5` | loc110504 | 279 | NULL-STABLE | NULL-STABLE | 0 | no | no |
| `FL:G2:G2_cnn_t5 / G2_qwen2` | loc110504 | 279 | CERTIFIED (b > a) | CERTIFIED (b > a) | − | no | yes |
| `FL:G2:G2_cnn_t5 / G2_vit_t5` | loc110504 | 279 | CERTIFIED (b > a) | FRAGILE | − | yes | yes |
| `FL:G2:G2_qwen2 / G2_vit_t5` | loc110504 | 279 | FRAGILE | FRAGILE | 0 | no | no |
| `FL:G3:X3_detect / X3_original` | vanngthi | 924 | CERTIFIED (a > b) | CERTIFIED (a > b) | + | no | no |
| `FL:G4:X3_flickr_detect / X3_flickr_original` | vanngthi | 100 | FRAGILE | FRAGILE | 0 | no | no |

Source of the table: `V.json::fl[i]` (id, repo, n, class statistics) and `RESULT.json::comparisons[i]` (F, F_dev, changed_F). Label: FIRST SCORING OF RELEASED OUTPUTS. The recomputed verdict over F_dev equals the code's string `comparisons[i].F_dev` for every one of the 1123 [n090] comparisons of D and FL together (yes). The recomputed CHANGED flag equals `changed_F` for every one of them (yes).

### I-14. Breaking axis levels over F_dev

(a) l.165: "**Nominal direction**: the significant direction under f0; if f0 is not significant, the direction significant under more classes; if neither, none."

l.166: "**Breaking set** of a FRAGILE comparison: the classes under which the nominal direction is not significant, reported with counts per axis level (for example "breaks under every `uts` member and under ck with pk")."

l.284: "the breaking axis levels"

(b), (c), (d). Each count is the number of (comparison, member) pairs in a breaking class whose member name carries that level. Recomputed from the stored percentiles and member lists.

| Row | file::key | syl | rdr | pyvi | uts | tw | tm | tf | pk | pf | pa | cf | ck | Recomputed equal | Evidence label |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D_over_F_dev_DEVELOPMENT | `RESULT.json::counts.D_over_F_dev_DEVELOPMENT.breaking_levels` | 654 [n091] | 573 [n092] | 525 [n093] | – | 575 [n094] | 588 [n095] | 589 [n096] | 604 [n097] | 617 [n098] | 531 [n099] | 850 [n100] | 902 [n101] | yes | DEVELOPMENT |
| FL_over_F_dev | `RESULT.json::counts.FL_over_F_dev.breaking_levels` | 36 [n102] | 81 [n103] | 72 [n104] | – | 63 [n105] | 63 [n106] | 63 [n107] | 63 [n108] | 63 [n109] | 63 [n110] | 99 [n111] | 90 [n112] | yes | FIRST SCORING OF RELEASED OUTPUTS |

(e) EQUAL.

### I-15. Breaking axis levels over F

(a) As I-14.

(b) and (d) Code values (not recomputable: the held-out class statistics and member lists are not stored):

| Row | file::key | syl | rdr | pyvi | uts | tw | tm | tf | pk | pf | pa | cf | ck | Evidence label |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D_over_F_DEVELOPMENT | `RESULT.json::counts.D_over_F_DEVELOPMENT.breaking_levels` | 690 [n113] | 609 [n114] | 561 [n115] | 630 [n116] | 821 [n117] | 834 [n118] | 835 [n119] | 844 [n120] | 875 [n121] | 771 [n122] | 1207 [n123] | 1283 [n124] | DEVELOPMENT; HELD-OUT FRONT END members included |
| FL_over_F | `RESULT.json::counts.FL_over_F.breaking_levels` | 54 [n125] | 99 [n126] | 90 [n127] | 48 [n128] | 97 [n129] | 97 [n130] | 97 [n131] | 96 [n132] | 96 [n133] | 99 [n134] | 153 [n135] | 138 [n136] | FIRST SCORING OF RELEASED OUTPUTS; HELD-OUT FRONT END members included |

(c) Not recomputable.
(e) NOT RECOMPUTABLE (code value reported).

## 2.3 P3, FE-ID on the KTVIC baselines

### I-16. P3 scope and M_new

(a) l.289: "BLEU-1 to BLEU-4, METEOR, ROUGE-L and CIDEr-D as computed by pycocoevalcap 1.2 (`COCOEvalCap`; METEOR and the PTB tokeniser need Java on the host). Printed metrics outside this list (for example SPICE) are listed and not used. A metric in scope whose scorer fails its host precondition (pycocoevalcap import, Java, METEOR jar) is dropped from P3a before any baseline is scored, recorded in `FEID.json`. If CIDEr-D or BLEU-4 cannot be computed by r\*, P3 is NOT RUN."

l.292: "The REGISTERED PREDICTION is P3a restricted to the in-scope printed metrics other than CIDEr-D and BLEU-4 (set M_new, from PRINTED.json)"

(b) `FEID.json::P3.M_new` = ['BLEU-1', 'METEOR', 'ROUGE-L']; `P3.dropped_K_coco` = []; `P3.not_used` = {'ktvic_resnetlstm': [], 'ktvic_vittrans': []}; `FEID.json::printed_sha256` = `2a962a2ba09403cd…` (equal to the pin 2a962a2b…: yes). This note did not open PRINTED.json. The printed strings are read from FEID.json only.

(c) Recomputed: the in-scope printed metrics in the FEID rows of the two baselines are BLEU-1, BLEU-4, METEOR, ROUGE-L and CIDEr-D. Without CIDEr-D and BLEU-4: M_new = ['BLEU-1', 'METEOR', 'ROUGE-L']. No in-scope metric was dropped by K-coco. No printed metric of the two baselines is outside the scope list. Ruling CC-354, ruling 1(d) (its l.96-99), names the same three metrics (six values).

(d) Code: `P3.M_new` = ['BLEU-1', 'METEOR', 'ROUGE-L'].
(e) EQUAL.

### I-17. P3a registered label on M_new

(a) l.290: "r\* (the released script, never run) reproduces every in-scope printed metric of both baselines in `PRINTED.json` within half a unit of the last printed digit."

l.292: "The REGISTERED PREDICTION is P3a restricted to the in-scope printed metrics other than CIDEr-D and BLEU-4 (set M_new, from PRINTED.json): SUPPORTED if r* reproduces every metric of M_new for both baselines; otherwise NOT SUPPORTED, with the failing metric and the distance. If M_new is empty, P3 carries no registered label: the reproduction of CIDEr-D and BLEU-4 by r* is reported as POST HOC."

l.235: "A member **reproduces** when |score_m − p_m| ≤ 0.5 × 10^(−d_m) + 1e-9 for every printed metric m."

(b) Quantities (printed strings as carried by FEID.json; r* values on the ×100 scale):

| Baseline | Metric | printed (`…printed`) | r* (`…rstar`) | distance (`…distance`) | tolerance 0.5 × 10^(−d) + 1e-9 | reproduced: recomputed / code | Evidence label |
|---|---|---|---|---|---|---|---|
| ktvic_resnetlstm | BLEU-1 | 53.0 [n137] | 52.9625 [n138] | 0.0375 [n139] | 0.050000001 | yes / yes | REGISTERED PREDICTION, DEVELOPMENT DATA (M_new) |
| ktvic_resnetlstm | METEOR | 27.5 [n140] | 27.5207 [n141] | 0.0207 [n142] | 0.050000001 | yes / yes | REGISTERED PREDICTION, DEVELOPMENT DATA (M_new) |
| ktvic_resnetlstm | ROUGE-L | 42.3 [n143] | 42.2898 [n144] | 0.0102 [n145] | 0.050000001 | yes / yes | REGISTERED PREDICTION, DEVELOPMENT DATA (M_new) |
| ktvic_vittrans | BLEU-1 | 56.1 [n146] | 56.1162 [n147] | 0.0162 [n148] | 0.050000001 | yes / yes | REGISTERED PREDICTION, DEVELOPMENT DATA (M_new) |
| ktvic_vittrans | METEOR | 30.1 [n149] | 30.1500 [n150] | 0.0500 [n151] | 0.050000001 | yes / yes | REGISTERED PREDICTION, DEVELOPMENT DATA (M_new) |
| ktvic_vittrans | ROUGE-L | 44.7 [n152] | 44.6944 [n153] | 0.0056 [n154] | 0.050000001 | yes / yes | REGISTERED PREDICTION, DEVELOPMENT DATA (M_new) |

Key prefix of the table: `FEID.json::P3.M_new_rows.<baseline>.<metric>`.

(c) Recomputed. Each printed string has one decimal, so the tolerance is 0.05 + 1e-9. Each of the six distances is at or below it. r* reproduces every metric of M_new for both baselines. Label: **SUPPORTED**. The largest distance is 0.049983 (ktvic_vittrans, METEOR), against a tolerance of 0.050000001.

(d) Code: `FEID.json::P3.label` = **SUPPORTED**; `P3.evidence` = "REGISTERED PREDICTION, DEVELOPMENT DATA (M_new only)".

(e) EQUAL. Custody condition for this label (CC-385 W4): LOG line OPS-1113br reads 'did not open … complete', so the branch is 'run as registered' and M_new keeps its label (also recorded in OPS-1113dg and OPS-1114d).

### I-18. P3a, CIDEr-D and BLEU-4 part (POST HOC)

(a) l.290: "Informed by O3 (a seen proxy, E4 row `P4_T3bug…`), so it is POST HOC-informed for CIDEr-D and BLEU-4 and a registered prediction only for the other printed metrics ("Labels", below)."

l.292: "P3a is POST HOC-informed for CIDEr-D and BLEU-4 (O3: a seen proxy)."

(b) Quantities:

| Baseline | Metric | printed | r* | distance | tolerance | reproduced: recomputed / code | Evidence label |
|---|---|---|---|---|---|---|---|
| ktvic_resnetlstm | BLEU-4 | 15.5 [n155] | 15.4684 [n156] | 0.0316 [n157] | 0.050000001 | yes / yes | POST HOC (O3) |
| ktvic_resnetlstm | CIDEr-D | 21.8 [n158] | 21.7899 [n159] | 0.0101 [n160] | 0.050000001 | yes / yes | POST HOC (O3) |
| ktvic_vittrans | BLEU-4 | 19.3 [n161] | 19.3315 [n162] | 0.0315 [n163] | 0.050000001 | yes / yes | POST HOC (O3) |
| ktvic_vittrans | CIDEr-D | 36.8 [n164] | 36.7682 [n165] | 0.0318 [n166] | 0.050000001 | yes / yes | POST HOC (O3) |

Key prefix: `FEID.json::P3.cider_bleu4_POST_HOC.<baseline>.<metric>`.

(c) Recomputed: all four values are within the tolerance. No registered label attaches to this part.
(d) Code: `reproduced` = true in all four rows.
(e) EQUAL.

### I-19. P3b (POST HOC check)

(a) l.291: "No matched member of F reproduces the printed CIDEr-D of either baseline."

l.292: "P3b is POST HOC for `syl`, `rdr` and `pyvi` (O4) and is reported as a POST HOC check for every matched member."

(b) and (d) Code: `FEID.json::fe_id.<baseline>.P3b_matched_F_reproducing_CIDEr-D_POST_HOC` is a list of the matched members of F that reproduce the printed CIDEr-D. Its length is 0 [n167] for ktvic_resnetlstm and 0 [n168] for ktvic_vittrans. Label: POST HOC.

(c) Not recomputable: the per-member scores are not stored. A weaker check is possible: no reproducing class of I-41 holds a matched member of F.
(e) NOT RECOMPUTABLE (code value reported).

### I-20. Identification label and margin of each baseline

(a) l.292: "The identification label and the margin are reported for each baseline."

l.237: "**IDENTIFIED**: the reproducing members form exactly one class. **AMBIGUOUS**: two or more classes. **OUTSIDE**: none. Reported beside it: the smallest distance, on the printed scale, between the reproducing class and the nearest other class (the identifiability margin)."

l.298: "Fewer than 12 of the 24 IDENTIFIED: P3's identification label is NOT_EVALUABLE and FE-ID is reported as a reproduction table."

(b) Quantities:

| Baseline | classes in F⁺ (`fe_id.<b>.classes`) | reproducing classes (length of `fe_id.<b>.reproducing`) | margin (`fe_id.<b>.margin`) | code label (`fe_id.<b>.label`) |
|---|---|---|---|---|
| ktvic_resnetlstm | 23 [n169] | 3 [n170] | null | "NOT_EVALUABLE (K-plant): reproduction table only" |
| ktvic_vittrans | 23 [n171] | 2 [n172] | null | "NOT_EVALUABLE (K-plant): reproduction table only" |

(c) Recomputed. Step 1 (I-22): 9 of the 24 planted cases are IDENTIFIED. Step 2: 9 is fewer than 12, so K-plant applies and the identification label of both baselines is **NOT_EVALUABLE**; FE-ID is reported as a reproduction table. Step 3, for the record only: the number of reproducing classes is above one for both baselines, so the §5.1 rule would not have given IDENTIFIED either. Under l.384 no identification label is reported. The margin is defined for a single reproducing class only; it is null.

(d) Code: `P3.identification` = {"ktvic_resnetlstm": "NOT_EVALUABLE (K-plant): reproduction table only", "ktvic_vittrans": "NOT_EVALUABLE (K-plant): reproduction table only"}; `P3.margin` = {"ktvic_resnetlstm": null, "ktvic_vittrans": null}.
(e) EQUAL.

### I-21. O5 row beside r* (POST HOC)

(a) l.293: "O5 (stored ROUGE-L under the E4 row `P4_T3bug…`) is not used for P3; it is reported, after P3, as POST HOC beside r\*."

(b) to (d) FEID.json has no key for this row. The stored file that holds O5 is on the list of files this note may not open. No value.
(e) NO VALUE. Listed in sections 3 and 6.

## 2.4 P4, planted check (METHOD CHECK, not a registered prediction)

### I-22. P4 counts among the 24 planted cases, and K-plant

(a) l.297: "Reported: the IDENTIFIED, AMBIGUOUS and OUTSIDE counts among the 24 and the identifiability margins (the identifiability rate at one printed decimal)."

l.298: "Fewer than 12 of the 24 IDENTIFIED: P3's identification label is NOT_EVALUABLE and FE-ID is reported as a reproduction table."

l.246: "24 cases: each of the 24 own files of the E4 seen set (B_KAPPA §4.2) is scored under one member of F⁺ drawn with `random.Random(20261113)` by a `plant` step that writes the truth to `PLANT_KEY.json` and only the rounded CIDEr-D, BLEU-4 and ROUGE-L (one decimal, as KTVIC prints) to `PLANT_PRINTED.json`."

(b) Quantities:

| Quantity | file::key | Value | Evidence label |
|---|---|---|---|
| planted cases | `FEID.json::plants` (length) | 24 [n173] | DEVELOPMENT; METHOD CHECK (§6.4, not a prediction) |
| IDENTIFIED | `FEID.json::P4.IDENTIFIED` | 9 [n174] | DEVELOPMENT; METHOD CHECK (§6.4, not a prediction) |
| AMBIGUOUS | `FEID.json::P4.AMBIGUOUS` | 15 [n175] | DEVELOPMENT; METHOD CHECK (§6.4, not a prediction) |
| OUTSIDE | `FEID.json::P4.OUTSIDE` | 0 [n176] | DEVELOPMENT; METHOD CHECK (§6.4, not a prediction) |
| identification | `FEID.json::P4.identification` | "NOT_EVALUABLE (K-plant)" | DEVELOPMENT; METHOD CHECK (§6.4, not a prediction) |

(c) Recomputed from `FEID.json::plants[*].label`: IDENTIFIED 9, AMBIGUOUS 15, OUTSIDE 0; they sum to 24. 9 is fewer than 12: **K-plant applies**. The identifiability rate at one printed decimal is 9 of 24.

(d) Code: IDENTIFIED 9, AMBIGUOUS 15, OUTSIDE 0; `P4.identification` = "NOT_EVALUABLE (K-plant)"; `P4.label` = "METHOD CHECK (§6.4)".
(e) EQUAL.

This note did not open PLANT_KEY.json or PLANT_PRINTED.json. No rule recomputed here needed a field of them.

### I-23. P4 wrong recovery

(a) l.296: "Because each planted member reproduces its own rounded scores under the same code, an IDENTIFIED class always contains the true member unless the code is wrong. A wrong recovery is therefore a FAULT (stage 3 stops; a re-run needs a judge line), not a FAIL."

(b) and (d) Code: a wrong recovery raises a FAULT and stage 3 stops (b_fecert.py l.590-594). Stage 3 ended with rc 0 and wrote FEID.json, and its stderr holds no FAULT line. So the code found no wrong recovery.

(c) Not recomputable: FEID.json does not keep the reproducing class of each planted case (the field is dropped at b_fecert.py l.1321), and the PLANT files stay shut. Opening them would not give the class lists.
(e) NOT RECOMPUTABLE (code value reported).

### I-24. P4 identifiability margins

(a) l.297: "Reported: the IDENTIFIED, AMBIGUOUS and OUTSIDE counts among the 24 and the identifiability margins (the identifiability rate at one printed decimal)."

(b) and (d) Code: `FEID.json::P4.margins` holds a margin for each IDENTIFIED case and null for the others (checked: yes). The 9 [n177] margins range from 0.0752 [n178] to 1.7429 [n179] on the printed scale. Classes per planted case (`plants[*].classes`): 28 [n180] to 128 [n181]. Label: DEVELOPMENT; METHOD CHECK (§6.4, not a prediction).

(c) Not recomputable: per-class scores are not stored.
(e) NOT RECOMPUTABLE (code value reported).

## 2.5 Preconditions and the structure gate (groups G1 to G6)

### I-25. F1, real decomposer

(a) l.142: "Each word unit is run on the KTVIC test references. Every string must come back non-empty and aligned; a whitespace fallback or more than 0.5% failed strings drops that unit from F (recorded in `FAMILY.json` before any score). A failure of `rdr` is a FAULT: nothing proceeds."

(b) Quantities (`FAMILY.json::F1.<unit>`):

| Unit | strings | failed | aligned | whitespace fallback | dropped: recomputed / code | Evidence label |
|---|---|---|---|---|---|---|
| rdr | 2790 [n182] | 0 [n183] | True | False | no / no | DESCRIPTIVE (references only; no system output) |
| pyvi | 2790 [n184] | 0 [n185] | True | False | no / no | DESCRIPTIVE (references only; no system output) |
| uts | 2790 [n186] | 0 [n187] | True | False | no / no | DESCRIPTIVE (references only; no system output) |

(c) Recomputed: for each unit the failed share is 0, which is not above 0.5%; the output is aligned; there is no whitespace fallback. No unit is dropped. `rdr` does not fail, so no FAULT.

(d) Code: `dropped` = false for the three units; `FAMILY.json::units_dropped` = [].
(e) EQUAL.

### I-26. F2, versions recorded

(a) l.143: "The jar sha256, the pyvi and underthesea versions and wheel sha256, the Python and `unicodedata.unidata_version` are written into `FAMILY.json`."

(b) `FAMILY.json::env`: jar sha256 `9e2811cd…` (registration l.112: 9e2811cd…); pyvi 0.1.1 (wheel sha256 `e5e9e0e4…`); underthesea 9.5.0 (wheel sha256 `81400f41…`); Python 3.12.3; unidata_version 15.0.0; numpy 2.5.4; pycocoevalcap 1.2; Java 21_0_13_0_3 (dots written as underscores); protocol_pilot sha256 `6aee4282…` (l.112: 6aee4282…); underthesea call signature recorded: yes; r* import: True.

(c) Recomputed: every field that l.143 names is present. pyvi is 0.1.1, as l.113 requires.
(d) Code: stage F ran `env_check` and ended with rc 0.
(e) EQUAL.

### I-27. F3, tone placement under each unit (toy strings)

(a) l.144: "On the toy strings of B_KAPPA §3.1 (no dataset text), each word unit's output for the tm and tf spellings is recorded. This replaces the assumption of O9 by a code record."

(b) `FAMILY.json::F3.<unit>` holds, for 9 toy strings (5 of B_KAPPA §3.1 and 4 additions flagged `addition`), the tokens of the tm and tf spellings and an `equal` flag. The field holds registered toy strings, not data set text; they are not copied here. Count of toy strings with equal tokens: rdr: 9 [n188] of 9; pyvi: 0 [n189] of 9; uts: 9 [n190] of 9. Label: DESCRIPTIVE.

(c) A record, not a rule with a label. The counts are read from the `equal` flags.
(d) Code: no label.
(e) NO CODE KEY (recomputed only).

### I-28. G-repro

(a) l.339: "G-repro: f0 reproduces the committed CIDEr-D of the 67 own files that have a score file within 0.01 (B_KAPPA §5.1 rule: a mismatch on a seen file is a FAULT)"

(b) `FAMILY.json::G_repro`: 67 [n191] rows; largest `abs_diff` = 0.0016 [n192] CIDEr-D points; `no_committed_score` lists 6 [n193] own files without a score file. Label: DEVELOPMENT.

(c) Recomputed: 67 of 67 rows have abs_diff ≤ 0.01. No mismatch, so no FAULT.
(d) Code: `ok` = true in 67 of 67 rows; stage F rc 0.
(e) EQUAL.

### I-29. Family sizes

(a) l.131: "| F_dev (development) | `syl`, `rdr`, `pyvi` | 54 |"; l.132: "| F_held (held-out) | `uts` | 18 |"; l.133: "| F = F_dev ∪ F_held | | 72 |"; l.233: "|F+| = 90 x 3 + 1 = 271"

(b) `FAMILY.json::family` = {'F': 72, 'F_dev': 54, 'F_held': 18, 'F_plus': 271}; `FAMILY.json::n_images` = 558 [n194], `n_refs` = 2790 [n195] (l.184: 558 images, 2,790 references).

(c) Recomputed by enumeration (3 T levels × 3 P levels × 2 C levels per unit): {'F': 72, 'F_dev': 54, 'F_held': 18, 'F_plus': 271}. The 54 names of `DEV.json::members` equal the enumeration of F_dev: yes.
(d) Code: as (b).
(e) EQUAL.

### I-30. Structure gate v2, files with stored gate values

(a) l.218: "it parses to {image id: one caption string} (a list value: its first element, as `load_preds` of the kit does);"

l.219: "coverage: at least 95% of the image ids of its reference file have a caption, and at most 5% of its rows have ids absent from that reference file (those rows are dropped);"

l.220: "duplicate ids at most 1% of rows (first occurrence kept);"

l.221: "empty captions at most 1% of rows;"

l.222: "reference-copy share at most 5%: captions equal, after N and casefold, to one of the image's own references;"

l.223: "at least 50% of captions contain a letter with a Vietnamese diacritic (detects stripped diacritics or another language)."

(b), (c), (d). Key prefix `GATE2.json::files.<group>/<file>`. Shares shown to four decimals.

| Group/file | rows | coverage | unknown ids | duplicates | empty | reference copies | diacritic | admitted: recomputed / code | Evidence label |
|---|---|---|---|---|---|---|---|---|---|
| G1/X4a | 578 [n196] | 1.0000 [n197] | 0.0000 [n198] | 0.0000 [n199] | 0.0000 [n200] | 0.0000 [n201] | 1.0000 [n202] | yes / yes | DESCRIPTIVE (structure only; no score) |
| G1/X4b | 578 [n203] | 1.0000 [n204] | 0.0000 [n205] | 0.0000 [n206] | 0.0000 [n207] | 0.0000 [n208] | 1.0000 [n209] | yes / yes | DESCRIPTIVE (structure only; no score) |
| G1/X4c | 578 [n210] | 1.0000 [n211] | 0.0000 [n212] | 0.0000 [n213] | 0.0000 [n214] | 0.0000 [n215] | 1.0000 [n216] | yes / yes | DESCRIPTIVE (structure only; no score) |
| G1/X4d | 578 [n217] | 1.0000 [n218] | 0.0000 [n219] | 0.0000 [n220] | 0.0000 [n221] | 0.0000 [n222] | 1.0000 [n223] | yes / yes | DESCRIPTIVE (structure only; no score) |
| G1/X4e | 578 [n224] | 1.0000 [n225] | 0.0000 [n226] | 0.0000 [n227] | 0.0000 [n228] | 0.0000 [n229] | 1.0000 [n230] | yes / yes | DESCRIPTIVE (structure only; no score) |
| G2/G2_cnn_lstm | 279 [n231] | 1.0000 [n232] | 0.0000 [n233] | 0.0000 [n234] | 0.0000 [n235] | 0.0000 [n236] | 1.0000 [n237] | yes / yes | DESCRIPTIVE (structure only; no score) |
| G2/G2_cnn_lstm_attention | 279 [n238] | 1.0000 [n239] | 0.0000 [n240] | 0.0000 [n241] | 0.0000 [n242] | 0.0000 [n243] | 1.0000 [n244] | yes / yes | DESCRIPTIVE (structure only; no score) |
| G2/G2_cnn_t5 | 279 [n245] | 1.0000 [n246] | 0.0000 [n247] | 0.0000 [n248] | 0.0000 [n249] | 0.0000 [n250] | 1.0000 [n251] | yes / yes | DESCRIPTIVE (structure only; no score) |
| G2/G2_qwen2 | 279 [n252] | 1.0000 [n253] | 0.0000 [n254] | 0.0000 [n255] | 0.0000 [n256] | 0.0000 [n257] | 1.0000 [n258] | yes / yes | DESCRIPTIVE (structure only; no score) |
| G2/G2_vit_t5 | 279 [n259] | 1.0000 [n260] | 0.0000 [n261] | 0.0000 [n262] | 0.0000 [n263] | 0.0000 [n264] | 1.0000 [n265] | yes / yes | DESCRIPTIVE (structure only; no score) |
| G3/X3_detect | 924 [n266] | 1.0000 [n267] | 0.0000 [n268] | 0.0000 [n269] | 0.0000 [n270] | 0.0087 [n271] | 1.0000 [n272] | yes / yes | DESCRIPTIVE (structure only; no score) |
| G3/X3_original | 924 [n273] | 1.0000 [n274] | 0.0000 [n275] | 0.0000 [n276] | 0.0000 [n277] | 0.0032 [n278] | 1.0000 [n279] | yes / yes | DESCRIPTIVE (structure only; no score) |
| G4/X3_flickr_detect | 100 [n280] | 1.0000 [n281] | 0.0000 [n282] | 0.0000 [n283] | 0.0000 [n284] | 0.0000 [n285] | 1.0000 [n286] | yes / yes | DESCRIPTIVE (structure only; no score) |
| G4/X3_flickr_original | 100 [n287] | 1.0000 [n288] | 0.0000 [n289] | 0.0000 [n290] | 0.0000 [n291] | 0.0000 [n292] | 1.0000 [n293] | yes / yes | DESCRIPTIVE (structure only; no score) |
| G6/ktvic_resnetlstm | 558 [n294] | 1.0000 [n295] | 0.0000 [n296] | 0.0000 [n297] | 0.0000 [n298] | 0.0036 [n299] | 1.0000 [n300] | yes / yes | DESCRIPTIVE (structure only; no score) |
| G6/ktvic_vittrans | 558 [n301] | 1.0000 [n302] | 0.0000 [n303] | 0.0000 [n304] | 0.0000 [n305] | 0.0108 [n306] | 1.0000 [n307] | yes / yes | DESCRIPTIVE (structure only; no score) |

Recomputed with the six thresholds of l.219-223: all 16 files with stored values pass every rule. Code: `admitted` = true for the same 16 files.
(e) EQUAL.

### I-31. Structure gate v2, files that failed rule 1

(a) l.218: "it parses to {image id: one caption string} (a list value: its first element, as `load_preds` of the kit does);" READ_PACKAGE.md l.42-43 records the coded reading: the X1 and X2 files have no id key and the K2 file is a metric table with no caption column, so each fails rule 1.

(b) and (d) Code: `GATE2.json::files.G5/X1`: admitted = False, reasons = ['1 parse']; `GATE2.json::files.G5/X2`: admitted = False, reasons = ['1 parse']; `GATE2.json::files.G6/K2`: admitted = False, reasons = ['1 parse']. Label: DESCRIPTIVE.

(c) Not recomputable: no gate value is stored for a file that does not parse. Count of files not admitted: 3 [n308] of 19 [n309].
(e) NOT RECOMPUTABLE (code value reported).

### I-32. Comparisons formed, per group

(a) l.225: "A comparison of two admitted files is **formed** when their covered id sets overlap in at least 95% of the reference file's ids and the comparison is scored on that intersection."

(b), (c), (d):

| Group | repository | comparisons listed | formed (code) | images in each comparison (`comparisons[i].n`) | Evidence label |
|---|---|---|---|---|---|
| G1 | loc110504 | 10 [n310] | 10 [n311] | 578 [n312] | DESCRIPTIVE |
| G2 | loc110504 | 10 [n313] | 10 [n314] | 279 [n315] | DESCRIPTIVE |
| G3 | vanngthi | 1 [n316] | 1 [n317] | 924 [n318] | DESCRIPTIVE |
| G4 | vanngthi | 1 [n319] | 1 [n320] | 100 [n321] | DESCRIPTIVE |
| G5, G6 | trannam710; SuperCoolGuy855 | 0 | 0 | – | DESCRIPTIVE |

Total formed: `GATE2.json::formed` = 22 [n032] of 22 [n322] listed. The registered maximum was 32 (l.202).

Recomputed. The reference-id count of a group is not stored. It is derived here as rows / coverage, which is exact because unknown ids and duplicates are 0 for every admitted file. With that count, n ≥ 95% of the reference ids holds for all 22 comparisons. G5 and G6 have fewer than two admitted files apart from the baseline pair, which is in D (l.186). So they form no FL comparison.

(e) EQUAL (with the derivation stated).

### I-33. GATE2.json logged before any FL score

(a) l.225: "The coordinator logs its sha256 before any FL score exists."; l.211: "Nothing in FL is scored under any member before this registration and its code are committed (§9)."

(b) LOG pin line OPS-1113cv (GATE2.json) is stamped 2026-11-13T15:15:25Z. The first stage that scores an FL file is 2a; `runs.log` gives its start as 2026-11-13T15:46:36Z. The stage-0b commit of the code is 9e6578a (CC-385).

(c) Recomputed: the pin line precedes the start of stage 2a.
(d) Code: stage 2a checks the GATE2.json pin line through `inputs()` and ended with rc 0.
(e) EQUAL.

## 2.6 Census (stage C)

### I-34. Systems, families, strata and the size of D

(a) l.184: "Files: the 73 own KTVIC test files `data/results/<name>.preds.json` (names = keys of `data/results/tone_norm/ktvic_side_by_side.json :: systems`, B_KAPPA §4.1); references `data/datasets/ktvic/test_data.json` field `caption` (558 images, 2,790 references)."

l.185: "Strata: prompt mode (`-short`, `-detailed`, `-two`). Families: the file-name rule of B_KAPPA §4.3 (26 families)."

l.186: "**D** = all unordered pairs of own files in the same stratum and in different families, plus the one pair of the two KTVIC baselines (ResNet101-LSTM against ViT-Transformer; `.session_backup/2026-10-22/b2/thesis_code_1a8d105/simple_evaluate/`, aggregate use only). Its size is printed by stage C; no number is promised here."

(b) Quantities:

| Quantity | file::key | Value | Evidence label |
|---|---|---|---|
| own files | `SYSTEMS.tsv` rows with role = own | 73 [n323] | DESCRIPTIVE |
| baseline files | `SYSTEMS.tsv` rows with role = baseline | 2 [n324] | DESCRIPTIVE |
| families | `CENSUS.json::families` | 26 [n325] | DESCRIPTIVE |
| own files in stratum short | `CENSUS.json::strata.short` | 33 [n326] | DESCRIPTIVE |
| own files in stratum detailed | `CENSUS.json::strata.detailed` | 35 [n327] | DESCRIPTIVE |
| own files in stratum two | `CENSUS.json::strata.two` | 5 [n328] | DESCRIPTIVE |
| size of D | `CENSUS.json::D_size` | 1101 [n329] | DESCRIPTIVE (the comparisons themselves are DEVELOPMENT) |

(c) Recomputed from `SYSTEMS.tsv`: 73 own files in 26 families; pairs in the same stratum and in different families, plus the one baseline pair: 1101. The recomputed id set equals `CENSUS.json::D`: yes.

(d) Code: `D_size` = 1101; `families` = 26; the code FAULTs unless the census is 73 systems and 26 families (b_fecert.py l.1044), and stage C ended with rc 0.
(e) EQUAL.

### I-35. Segmenter census: does `uts` stay held out

(a) l.340: "segmenter census (CC-350 N4): any `underthesea` score on a system output moves `uts` to F_dev before stage 1 and is logged (F_held may then be empty, and P1 is then NOT_EVALUABLE); a character-unit score is logged only"

(b) Quantities:

| Quantity | file::key | Value | Evidence label |
|---|---|---|---|
| own score files read (segmenter field only) | `CENSUS.json::segmenter_census` (own keys) | 67 [n330] | DESCRIPTIVE |
| b2_external score files read (field names only) | `CENSUS.json::b2_score_sha256` (length) | 1 [n331] | DESCRIPTIVE |
| own score files with a row whose segmenter is "rdrsegmenter" | `CENSUS.json::segmenter_census` | 67 [n332] | DESCRIPTIVE |
| own score files with a row whose segmenter is "whitespace" | `CENSUS.json::segmenter_census` | 22 [n333] | DESCRIPTIVE |
| underthesea hits | `CENSUS.json::underthesea_hits` (length) | 0 [n334] | DESCRIPTIVE |
| character-unit hits (logged only) | `CENSUS.json::character_unit_hits_logged_only` (length) | 0 [n335] | DESCRIPTIVE |

(c) Recomputed: a scan of the strings stored in `CENSUS.json::segmenter_census` (hit = 'underthesea' in the string or a `_uts` suffix; READ_PACKAGE.md l.62) finds 0 hits, and 0 character-unit hits. So `uts` is not moved to F_dev. F_held keeps its 18 members and P1 is not made NOT_EVALUABLE by the census.
(d) Code: `CENSUS.json::uts_moved_to_dev` = False; `DEV.json::units_held` = ['uts'].
(e) EQUAL. The census itself (which strings sit in the stored score files) is the code's reading; this note did not open those files.

## 2.7 Secondary and control rows (§6.6; each without a verdict)

### I-36. FE-PRED row

(a) l.308: "**FE-PRED row.** Over D ∪ FL: the area under the ROC curve of |D_f0| / sd_boot(D_f0) for predicting CHANGED. Expected high (O1); reported to show that the margin under one member already predicts fragility."

(b) `RESULT.json::secondary.FE_PRED_AUC` = 0.8012 [n336]. Comparisons: 1123 [n090]; CHANGED over F: 30 [n337]; not CHANGED: 1093 [n338]. Label: DESCRIPTIVE (DEVELOPMENT for the D part, FIRST SCORING OF RELEASED OUTPUTS for the FL part).

(c) Recomputed as the coded reading (READ_PACKAGE.md l.81): the probability that a CHANGED comparison has the smaller |D_f0| / sd_boot(D_f0), ties counted one half, over all comparisons of D ∪ FL. z under f0 is recomputed from the stored f0 class; the CHANGED flag as in I-10. Value: 0.801159.

(d) Code: 0.801158889905459.
(e) EQUAL. The registration does not say which direction of the score counts as 'predicting CHANGED'; the coded reading is used.

### I-37. FE-PRED extra row (not registered)

(a) No registered rule. The code adds this row and names it EXTRA (CC-361 NB2; READ_PACKAGE.md l.143).

(b) `RESULT.json::secondary.FE_PRED_AUC_f0_significant_EXTRA` = 0.9546 [n339], over the 946 [n340] comparisons significant under f0.

(c) Recomputed: 0.954585.
(d) Code: 0.9545851528384279.
(e) EQUAL. The registration names no such row; by l.31 a number outside the named labels is DESCRIPTIVE. It is a code row and carries no registered rule.

### I-38. BLEU-4 and ROUGE-L certificates; F without ck, with chr, without pk

(a) l.309: "BLEU-4 and ROUGE-L certificates with the same rule."

l.310: "Certificates over F without ck, with `chr`, and without pk (sensitivity to the admissibility calls)."

(b) and (d) Code values, over D ∪ FL together (`RESULT.json::secondary.<row>`):

| Row | comparisons | CERTIFIED | FRAGILE | REVERSED | NULL-STABLE | significant under f0 | CHANGED | CHANGED share | point-sign flips | Evidence label |
|---|---|---|---|---|---|---|---|---|---|---|
| BLEU-4_over_F | 1123 [n341] | 862 [n342] | 120 [n343] | 20 [n344] | 141 [n345] | 909 [n346] | 47 [n347] | 0.0517 [n348] | 118 [n349] | DESCRIPTIVE |
| ROUGE-L_over_F | 1123 [n350] | 891 [n351] | 122 [n352] | 16 [n353] | 110 [n354] | 970 [n355] | 79 [n356] | 0.0814 [n357] | 94 [n358] | DESCRIPTIVE |
| F_without_ck | 1123 [n359] | 919 [n360] | 63 [n361] | 0 [n362] | 141 [n363] | 946 [n364] | 27 [n365] | 0.0285 [n366] | 51 [n367] | DESCRIPTIVE |
| F_with_chr_DESCRIPTIVE | 1123 [n368] | 893 [n369] | 119 [n370] | 4 [n371] | 111 [n372] | 946 [n373] | 53 [n374] | 0.0560 [n375] | 104 [n376] | DESCRIPTIVE |
| F_without_pk | 1123 [n377] | 925 [n378] | 53 [n379] | 0 [n380] | 145 [n381] | 0 [n382] | 0 [n383] | null [n384] | 63 [n385] | DESCRIPTIVE |

(c) Not recomputable: these rows need the statistics of the held-out or `chr` classes, or the BLEU-4 and ROUGE-L statistics of the held-out classes. Structural note on the row 'F_without_pk': f0 has level pk, so f0 is not a member of that family, and the code then counts 0 comparisons as significant under f0 and 0 as CHANGED. That 0 is a property of the family, not a measured outcome.

(e) NOT RECOMPUTABLE (code value reported).

### I-39. Certificates over the held-out members alone (code row)

(a) No registered row of its own. The registration defines the decision rule for a family G that may be F_held (l.158) and labels the held-out members HELD-OUT FRONT END (l.29).

(b) and (d) Code values (`RESULT.json::counts.F_held_HELD-OUT_FRONT_END`), over D ∪ FL together: comparisons 1123 [n386], CERTIFIED 937 [n387], FRAGILE 32 [n388], REVERSED 0 [n389], NULL-STABLE 154 [n390], point_flips 40 [n391]. significant under f0 = 0 and CHANGED = 0 for the structural reason of I-38 (f0 is not a `uts` member). Label: HELD-OUT FRONT END.

(c) Not recomputable.
(e) NOT RECOMPUTABLE (code value reported).

### I-40. English control

(a) l.311: "**English control (CONTROL).** If at least three English output files of different systems exist on disk for one English test set (coordinator names them at the code read; unverified today), the English analogue family (units: PTB tokens, whitespace; case; pk to pa) is run on them and the CERTIFIED share is reported. Otherwise NOT RUN. No claim beyond Vietnamese is made from it (§14)."

(b) and (d) Code: `RESULT.json::secondary.English_control` = "NOT RUN (no English output files named at the code read; §6.6, Q13)". Label: CONTROL.

(c) Recomputed: READ_PACKAGE.md l.98 records that no English output files were named at the code read (question Q13, default NOT RUN). The registered consequence is **NOT RUN**.
(e) EQUAL.

## 2.8 FE-ID finding and printed comparisons

The P3 labels are items I-16 to I-21. The planted check is items I-22 to I-24.

### I-41. FE-ID reproduction table of the two baselines

(a) l.233: "F⁺ = every member f of F (§2.4) and the 18 `chr` members, 90 members in all (`chr` is not in F, CC-350 ruling 2, but identification needs no admissibility), applied three ways: **matched** (both sides), **outputs only** (references get N only, then whitespace split), **references only** (outputs get N only); plus **r\***, the released-script member: pycocoevalcap 1.2 `COCOEvalCap` (PTB tokeniser, both sides as released, underscores kept). |F+| = 90 x 3 + 1 = 271, `chr` included."

l.235: "A member **reproduces** when |score_m − p_m| ≤ 0.5 × 10^(−d_m) + 1e-9 for every printed metric m."

l.238: "What it cannot show: that the true pipeline is in F⁺, or that the released outputs are the ones that were scored. Every FE-ID sentence carries both caveats."

(b) and (d) Code values (`FEID.json::fe_id.<baseline>`). Member names only; no text.

| Baseline | reproducing class | members | way and unit of its members | smallest distance of any class to the printed values (`nearest_distance`) |
|---|---|---|---|---|
| ktvic_resnetlstm | 1 | 18 [n392] | outputs only: 18; unit rdr | 0.0375 [n393] |
| ktvic_resnetlstm | 2 | 6 [n394] | outputs only: 6; unit pyvi |  |
| ktvic_resnetlstm | 3 | 1 [n395] | r* (released script) |  |
| ktvic_vittrans | 1 | 18 [n396] | outputs only: 18; unit rdr | 0.0438 [n397] |
| ktvic_vittrans | 2 | 1 [n398] | r* (released script) |  |

Pool: `FEID.json::pool` = 271 [n399] entries of F⁺; `rstar_in_pool` = True. Printed metrics used: non-r* members ['BLEU-1', 'BLEU-4', 'CIDEr-D', 'ROUGE-L']; r* ['BLEU-1', 'BLEU-4', 'CIDEr-D', 'METEOR', 'ROUGE-L']. `METEOR_excluded_for_members` = True (forced reading of CC-361 D12: no member-specific METEOR scorer). In the class of 18 'outputs only' members of ktvic_resnetlstm and of ktvic_vittrans, the unit is `rdr` with every T, P and C level. In the class of 6 'outputs only' `pyvi` members of ktvic_resnetlstm, the T level is `tf` with every P and C level.

(c) Not recomputable: the per-member scores and token keys are not stored. The class counts above are read from the stored member lists.
(e) NOT RECOMPUTABLE (code value reported).

### I-42. Printed comparisons (§5.5)

(a) l.258: "Census: every pair of systems that one source prints side by side (KTVIC table: 3 systems, 3 pairs; K2 README: up to 3 pairs; FL repositories: whatever `PRINTED.json` holds)."

l.259: "For each printed pair: whether both sides' outputs are released and admitted (**re-scorable**), one side only (**one-sided**), or neither."

l.261: "Reported as "k of n printed comparisons change order under matched scoring; m of n are not certified over F", with n stated. No word such as "wrong", "error" or "invalid" is attached to a published score."

(b) Quantities:

| Quantity | file::key | Value | Evidence label |
|---|---|---|---|
| printed pairs | `FEID.json::printed_comparisons.pairs` (length) | 6 [n400] | DESCRIPTIVE |
| pairs of kind re-scorable | `…pairs[i].kind` | 1 [n401] | DESCRIPTIVE |
| pairs of kind one-sided | `…pairs[i].kind` | 2 [n402] | DESCRIPTIVE |
| pairs of kind neither | `…pairs[i].kind` | 3 [n403] | DESCRIPTIVE |
| n re-scorable | `FEID.json::printed_comparisons.n_rescorable` | 1 [n404] | DESCRIPTIVE |
| k: order changes under f0 | `FEID.json::printed_comparisons.order_changes_under_f0` | 0 [n405] | DESCRIPTIVE |
| m: not certified over F | `FEID.json::printed_comparisons.not_certified_over_F` | 0 [n406] | DESCRIPTIVE |
| re-scorable pair: printed CIDEr gap | `…pairs[0].printed_gap` | -15.00 [n407] | DESCRIPTIVE (difference of two printed values) |
| re-scorable pair: gap under f0 | `…pairs[0].f0_gap` | -24.02 [n408] | DEVELOPMENT; POST HOC (O4 holds both f0 values) |
| re-scorable pair: certificate over F | `…pairs[0].certificate_F` | "CERTIFIED (b > a)" | DEVELOPMENT; F includes the HELD-OUT FRONT END members |
| one-sided pair: released side under f0 minus the other side as printed | `…pairs[1].gap_released_f0_minus_other_printed` | -87.15 [n409] | DEVELOPMENT; POST HOC (O4); note in the file: "one side re-scored; the other side's pipeline unknown" |
| one-sided pair: released side under f0 minus the other side as printed | `…pairs[2].gap_released_f0_minus_other_printed` | -63.13 [n410] | DEVELOPMENT; POST HOC (O4); note in the file: "one side re-scored; the other side's pipeline unknown" |

Sources of the pairs: K2: 3, KTVIC: 3. The re-scorable pair is the pair of the two KTVIC baselines. The one-sided pairs are each baseline against the third printed KTVIC row, whose outputs are not released here. The K2 pairs are 'neither' because K2 was not admitted (I-31).

(c) Recomputed from the pair rows: n = 1; k = 0 (the printed gap and the gap under f0 have the same sign); m = 0 (the verdict string starts with CERTIFIED).

(d) Code: n_rescorable = 1, order_changes_under_f0 = 0, not_certified_over_F = 0; label "DESCRIPTIVE".
(e) EQUAL.

### I-43. FE-ID on other files with a printed value

(a) l.346: "| 3 FE-ID | KTVIC baselines, K2 and FL files with a printed value"

(b) and (d) Code: `FEID.json::fe_id` has keys ['ktvic_resnetlstm', 'ktvic_vittrans']. b_fecert.py l.97-99 maps the three K2 rows and the third KTVIC row of PRINTED.json to no file.

(c) Recomputed: K2 is not admitted (I-31) and the registered map gives it no file; no FL repository row is in the registered map. So FE-ID has a value for the two baselines only.
(e) EQUAL.

## 2.9 Kill gates and evaluability (§10)

| Item | Gate (registration line) | Condition and consequence, as registered | Quantity | Recomputed | Code | Equal |
|---|---|---|---|---|---|---|
| K-01 | K-rdr (l.359) | "F1 fails for `rdr`, or G-repro fails on a seen file" → "FAULT; nothing proceeds" | F1 for `rdr` (I-25); G-repro (I-28) | not triggered | stage F rc 0, no FAULT | EQUAL |
| K-02 | K-unit (l.360) | "F1 fails for `pyvi` or `uts`" → "that unit is dropped before any score, recorded in `FAMILY.json`; if F_held becomes empty, P1 is NOT_EVALUABLE" | F1 for `pyvi`, `uts` (I-25) | not triggered; F_held not empty | `units_dropped` = [] | EQUAL |
| K-03 | K-FL (l.361) | "fewer than 10 FL comparisons significant under f0" → "P2 NOT_EVALUABLE; counts reported" | n_FL = 10 (I-10) | not triggered (n_FL is not fewer than 10) | P2 label is "NOT SUPPORTED", not NOT_EVALUABLE | EQUAL |
| K-04 | K-FL20 (l.362) | "fewer than 20 formed FL comparisons" → "the application claim in the paper is descriptive ("k of n in a small pool"), as REDESIGN_B set it" | formed FL comparisons = 22 (I-32) | not triggered (not fewer than 20) | `GATE2.json::K_FL20` = False; `RESULT.json::P2.K_FL20_descriptive` = False | EQUAL |
| K-05 | K-N (l.363) | "N < 59 in the verdict set V after the fallback of §6.1" → "P1 NOT_EVALUABLE" | N = 72 (I-01) | not triggered (N is not below 59) | P1 label is "INCONCLUSIVE", not NOT_EVALUABLE | EQUAL |
| K-06 | K-NC (l.364) | "r_NC ≤ 0.05" → "P1 carries LOW-SENSITIVITY" | r_NC = 0.0066 (I-03) | TRIGGERED: P1 carries LOW-SENSITIVITY | `P1.NC` = "LOW-SENSITIVITY" | EQUAL |
| K-07 | K-print (l.365) | "`PRINTED.json` not logged by 2026-11-15 12:00 VN" → "P3 NOT RUN; O3 stays POST HOC in the text" | PIN-1112-b-fecert-printed at 2026-11-12T07:03:50Z (LOG l.2268); pin-form line OPS-1113df at 2026-11-13T16:48:25Z; limit 2026-11-15T05:00Z | not triggered | stage 3 ran with `--printed`; `printed_sha256` = `2a962a2b…` | EQUAL |
| K-08 | K-coco (l.366) | "pycocoevalcap 1.2 or Java fails its host precondition for CIDEr-D or BLEU-4" → "P3 NOT RUN; other in-scope metrics dropped one by one as §6.3 says" | `P3.dropped_K_coco` = []; `rstar_in_pool` = True; `env_rstar`: pycocoevalcap 1.2, Java 21_0_13_0_3, r* import True | not triggered; no metric dropped | P3 label is "SUPPORTED", not NOT RUN | EQUAL |
| K-09 | K-plant (l.367) | "fewer than 12 of 24 planted cases IDENTIFIED" → "P3's identification label NOT_EVALUABLE; FE-ID reported as a reproduction table (P4 method check, §6.4)" | IDENTIFIED = 9 of 24 (I-22) | TRIGGERED: identification label NOT_EVALUABLE; reproduction table | `P4.identification` = "NOT_EVALUABLE (K-plant)" | EQUAL |
| K-10 | K-human (l.368) | "labelling plan §7" → "as registered there" | human arm not started | open (labelling plan §7) | no HUMAN.json | NO VALUE |
| K-11 | K-time (l.369) | "a stage not finished by 2026-11-16 12:00 VN" → "that stage NOT RUN, reported as such" | limit 2026-11-16T05:00Z; last stage end 2026-11-13T17:42:10Z (`runs.log`) | not triggered for stages F, C, G, 1, 2a, 2b, 3; open for stage H | every stage rc 0 (the code refuses or FAULTs after K-time) | EQUAL |

## 2.10 Stop rules, order and provenance (§9)

### S-01. A FAULT stops the chain

(a) l.351: "A FAULT stops the chain; a re-run after a fix needs a judge line and is disclosed."

(b) `runs.log`: every stage and the pin step ended with rc 0; the `.rc` files hold 0. The stderr files of F, C, G, 1, pin, 2a and 2b are empty (0 bytes). The stderr of stage 3 holds 58 PTB tokeniser speed lines and one PTB lexer warning (section 5, fact R3), and no FAULT or REFUSED line. LOG line OPS-1114e: 'No stage returned rc 3 or 4; no CHAIN_STOP; every stage ran once'.
(c) Recomputed: no FAULT; no re-run.
(d) Code: rc 0 everywhere.
(e) EQUAL.

### S-02. Order: pin before 2a; V.json line before 2b; PRINTED line before 3

(a) l.349: "**Before the pin nobody may** run a held-out member on any system output, score any FL file, or change a threshold, the family or the gate. Stage 2a checks that no `RESULT*.json` exists and that the pin line precedes its start line. Stage 2b refuses to start without the V.json LOG line."

l.346: "after `PRINTED.json` is logged"

(b) Stamps of the LOG pin lines and stage starts of `runs.log` (UTC, 2026-11-13):

| Stage | Needs the line | Line stamp | Stage start | Line first |
|---|---|---|---|---|
| C | OPS-1113cr (FAMILY.json) | 15:14:18Z | 15:14:22Z | yes |
| G | OPS-1113cs (CENSUS.json) | 15:14:31Z | 15:14:52Z | yes |
| 1 | OPS-1113cv (GATE2.json) | 15:15:25Z | 15:15:29Z | yes |
| 2a | OPS-1113cx (DEV.json, NC.json) | 15:44:18Z | 15:46:36Z | yes |
| 2b | OPS-1113dd (V.json) | 15:50:07Z | 15:50:11Z | yes |
| 3 | OPS-1113de (RESULT.json) | 16:47:09Z | 16:48:41Z | yes |
| 3 | OPS-1113df (PRINTED.json) | 16:48:25Z | 16:48:41Z | yes |

(c) Recomputed: every required line precedes its stage. No held-out member and no FL file was scored before the pin of DEV.json and NC.json: the first such stage, 2a, started after it. RESULT.json was written by stage 2b only, after stage 2a.
(d) Code: each stage checks its lines (`prev_ok`, `inputs`, `pin_line`) and refuses otherwise; all rc 0.
(e) EQUAL.

### S-03. Provenance chain inside the output files

(a) l.333: "Each stage is a subcommand of `scripts/b_fecert/b_fecert.py`, refuses to start without the sha256 of its inputs and the LOG line of the previous stage, and writes its output sha256 with a `date -u` stamp."

(b) and (c) Checked in the eight JSON files: `registration_sha256` equals 736b7e6a… in all: yes; `code_sha256` holds the same eight module hashes in all, with b_fecert.py 67e43dea… and family.py 7cb2c69b… equal to the repository files: yes; `prev_sha256` of each file equals the pinned sha of the previous stage's file: yes; every entry of `inputs_sha256` equals the pinned sha of the named file: yes. This note re-hashed only b_fecert.py and family.py; the other six module hashes are reported as recorded (protocol_pilot.py 6aee4282… as at registration l.112; build_pairs.py 49692235… as in CC-388).
(d) Code: wrote these fields.
(e) EQUAL.

### S-04. Each stage ran once

(a) Ruling CC-385, ruling 5 (its l.147): 'each stage once'. l.351: "a re-run after a fix needs a judge line"

(b) and (c) `runs.log` has one start line and one end line for each of F, C, G, 1, pin, build, 2a, 2b and 3. Outputs are written once (`write_once`).
(d) Code: rc 0; LOG line OPS-1114e says the same.
(e) EQUAL.

## 2.11 List of items and statuses

Basis of an EQUAL status: **A** = recomputed here from stored statistics or stored values, without using a label of the code; **B** = rests on the code's own per-comparison or per-case strings (verdicts over F, CHANGED flags, per-case identification labels, per-pair rows), tallied or combined here; **C** = record check (stamps, return codes, presence of a field or key).

| Item | Title | Status | Basis |
|---|---|---|---|
| I-01 | P1 verdict set V | EQUAL | A |
| I-02 | P1 label | EQUAL | B |
| I-03 | Sensitivity control NC | EQUAL | A |
| I-04 | P1 carries the NC words (K-NC) | EQUAL | A |
| I-05 | P1 FL row | EQUAL | B |
| I-06 | P1 rows reported beside it: all of Cert_dev, D, FL | EQUAL | B |
| I-07 | P1 reversal count | NOT RECOMPUTABLE (code value reported) | – |
| I-08 | P1 'with chr' row | NOT RECOMPUTABLE (code value reported) | – |
| I-09 | P1 'r for uts' | NO CODE KEY (recomputed only) | – |
| I-10 | P2 label | EQUAL | B |
| I-11 | P2 per repository and leave-one-out | EQUAL | B |
| I-12 | Always-reported counts over F_dev (D and FL) | EQUAL | A |
| I-13 | Always-reported counts over F (D and FL) | EQUAL | B |
| I-14 | Breaking axis levels over F_dev | EQUAL | A |
| I-15 | Breaking axis levels over F | NOT RECOMPUTABLE (code value reported) | – |
| I-16 | P3 scope and M_new | EQUAL | A |
| I-17 | P3a registered label on M_new | EQUAL | A |
| I-18 | P3a, CIDEr-D and BLEU-4 part (POST HOC) | EQUAL | A |
| I-19 | P3b (POST HOC check) | NOT RECOMPUTABLE (code value reported) | – |
| I-20 | Identification label and margin of each baseline | EQUAL | B |
| I-21 | O5 row beside r* (POST HOC) | NO VALUE | – |
| I-22 | P4 counts among the 24 planted cases, and K-plant | EQUAL | B |
| I-23 | P4 wrong recovery | NOT RECOMPUTABLE (code value reported) | – |
| I-24 | P4 identifiability margins | NOT RECOMPUTABLE (code value reported) | – |
| I-25 | F1, real decomposer | EQUAL | A |
| I-26 | F2, versions recorded | EQUAL | C |
| I-27 | F3, tone placement under each unit (toy strings) | NO CODE KEY (recomputed only) | – |
| I-28 | G-repro | EQUAL | A |
| I-29 | Family sizes | EQUAL | A |
| I-30 | Structure gate v2, files with stored gate values | EQUAL | A |
| I-31 | Structure gate v2, files that failed rule 1 | NOT RECOMPUTABLE (code value reported) | – |
| I-32 | Comparisons formed, per group | EQUAL | A |
| I-33 | GATE2.json logged before any FL score | EQUAL | C |
| I-34 | Systems, families, strata and the size of D | EQUAL | A |
| I-35 | Segmenter census: does `uts` stay held out | EQUAL | A |
| I-36 | FE-PRED row | EQUAL | B |
| I-37 | FE-PRED extra row (not registered) | EQUAL | B |
| I-38 | BLEU-4 and ROUGE-L certificates; F without ck, with chr, without pk | NOT RECOMPUTABLE (code value reported) | – |
| I-39 | Certificates over the held-out members alone (code row) | NOT RECOMPUTABLE (code value reported) | – |
| I-40 | English control | EQUAL | C |
| I-41 | FE-ID reproduction table of the two baselines | NOT RECOMPUTABLE (code value reported) | – |
| I-42 | Printed comparisons (§5.5) | EQUAL | B |
| I-43 | FE-ID on other files with a printed value | EQUAL | C |
| K-01 | K-rdr | EQUAL | A |
| K-02 | K-unit | EQUAL | A |
| K-03 | K-FL | EQUAL | A |
| K-04 | K-FL20 | EQUAL | A |
| K-05 | K-N | EQUAL | A |
| K-06 | K-NC | EQUAL | A |
| K-07 | K-print | EQUAL | C |
| K-08 | K-coco | EQUAL | C |
| K-09 | K-plant | EQUAL | B |
| K-10 | K-human | NO VALUE | – |
| K-11 | K-time | EQUAL | C |
| S-01 | A FAULT stops the chain | EQUAL | C |
| S-02 | Order: pin before 2a; V.json line before 2b; PRINTED line before 3 | EQUAL | C |
| S-03 | Provenance chain inside the output files | EQUAL | A |
| S-04 | Each stage ran once | EQUAL | C |

Counts: 58 items; 44 EQUAL; 0 DIFFERENT; 10 not recomputable; 2 without a code key; 2 without a value.

## 3. NOT RUN, FAULT and K-rule outcomes: registered items without a value

| Kind | Item | Registered consequence (quoted) or note |
|---|---|---|
| FAULT | none | All stages rc 0 (S-01). No registered FAULT consequence applies. |
| NOT RUN | English control (I-40) | l.311: "Otherwise NOT RUN. No claim beyond Vietnamese is made from it (§14)." |
| NOT_EVALUABLE by K-plant | Identification label and margin of each KTVIC baseline (I-20) | l.367: "P3's identification label NOT_EVALUABLE; FE-ID reported as a reproduction table (P4 method check, §6.4)"; l.384: "with fewer than 12 IDENTIFIED, FE-ID is reported as a reproduction table without identification labels" |
| no value | O5 row beside r* (I-21) | l.293: "it is reported, after P3, as POST HOC beside r\*." The row is owed; stage 3 does not produce it. |
| no value (gate) | FL comparisons of groups G5 and G6; FE-ID and a re-scorable printed pair for K2 (I-31, I-32, I-43) | Rule 1 of l.218 (l.218: "it parses to {image id: one caption string}"). The three files do not parse; a file that is not admitted forms no comparison (l.225). K2's printed pairs are 'neither' (l.259). |
| no value (open) | Stage H and the human hypotheses H-P and H-U; K-human (K-10) | l.347: "label files after the closing LOG line"; l.369: "that stage NOT RUN, reported as such" if stage H has not finished by K-time. |
| no key | 'r for uts' (I-09); matched f0 scores 'Y' of the two baselines (C-P3 in section 4) | No registered consequence. The first equals the P1 estimand by construction. The second can be derived (section 4) or needs a small registered-output step; for the judge. |

K-rules triggered: K-NC (K-06) and K-plant (K-09). K-rules not triggered: K-rdr, K-unit, K-FL, K-FL20, K-N, K-print, K-coco, and K-time for stages F to 3. Open: K-human, and K-time for stage H. Counts for the record: NOT RUN 1; FAULT 0; NOT_EVALUABLE by a K-rule 1; rows of the table above without a value: 6.

## 4. What the registered text allows to be claimed, and what it does not

Each candidate sentence copies the registered label words. Each carries its evidence label. A sentence marked BLOCKED may not enter paper text until the named decision exists. These are candidates for the judge, not paper text.

### 4.1 Candidate sentences

- **C-P1** (REGISTERED PREDICTION; label INCONCLUSIVE; l.273, l.379 'counts and bound only'). "P1, the held-out front-end check, is INCONCLUSIVE: of N = 72 [n010] near-margin certificates on the development family (z_min ≤ 4), 2 [n011] broke under the held-out front ends (r = 0.0278 [n012]; one-sided 95% Clopper–Pearson upper bound 0.0849 [n013], lower bound 0.0050 [n014])." Required beside it (l.276): "Comparisons share files, so they are not independent; the Clopper–Pearson bound is a nominal summary." The N certificates are 68 [n007] DEVELOPMENT comparisons and 4 [n008] first-look comparisons.
- **C-P1-LS** (l.277, l.364; see J1 and J2). "P1 is labelled LOW-SENSITIVITY: 'a one-unit family was broken by the other development units in at most 5% of its near-margin certificates, so the held-out check had little room to fail'." NC figure: 6 [n018] of 915 [n017] (r_NC = 0.0066 [n019]; DEVELOPMENT). Fact to state with it: the set used was the fallback set, all of Cert_NC (54 [n016] certificates had z_min^NC ≤ 4).
- **C-P1-FL** (FIRST SCORING OF RELEASED OUTPUTS; no verdict; l.274). "Among the 9 [n020] first-look comparisons certified over the development family, 1 [n021] broke under the held-out front ends (one-sided 95% Clopper–Pearson bounds 0.0057 [n022] and 0.4291 [n023])." The lower bound does not exceed 0.05, so l.274 requires no statement beside the P1 label.
- **C-P1-beside** (no verdict; l.275). "Over all 918 [n024] certificates on the development family, 2 [n025] broke; 1 [n027] in D and 1 [n028] in FL. A reversal was not detected (count 0 [n029])." DESCRIPTIVE 'with chr' row, no verdict: 16 [n030] breaks and 3 [n031] reversals of 72 [n411] when the `chr` members are added to F_held; `chr` is not admissible (l.133).
- **C-P2** (REGISTERED PREDICTION; label NOT SUPPORTED; l.283, l.381). "the certificate changed few conclusions in this pool (2 [n034] of 10 [n033])". Row l.381 adds: "the method is then presented as a cheap check whose usual answer is CERTIFIED, with the counts". The counts over F for FL: 8 [n074] CERTIFIED, 8 [n075] FRAGILE (of which 0 [n076] REVERSED), 6 [n077] NULL-STABLE of 22 [n073]. Whether the words 'usual answer is CERTIFIED' fit these counts is for the judge. Per repository and leave-one-out as in I-11. Label of every FL figure: "a first scoring of other groups' released outputs" (l.425). Under the default of §17 PI-6 the first-look systems are not named in paper text: counts by repository only (l.427, l.498).
- **C-D** (DEVELOPMENT; no verdict; l.284). "On the 1101 [n064] development comparisons, 908 [n065] are CERTIFIED over F and 28 [n070] of the 936 [n069] significant under f0 are CHANGED." Own-file results are DEVELOPMENT (l.425); the files are variants of the authors' own systems (l.430).
- **C-P3** (REGISTERED PREDICTION, DEVELOPMENT DATA, on M_new only; label SUPPORTED; l.382). "The printed scores of the two KTVIC baselines are reproduced by pipeline r* (every metric of M_new within half a unit); under matched scoring (f0) the values are Y". CIDEr-D and BLEU-4 stay POST HOC (l.382, l.426). Both caveats of l.238 go with it: it cannot show "that the true pipeline is in F⁺, or that the released outputs are the ones that were scored". **BLOCKED** by §17 PI-2 (default: "kept out of paper text until the PI answers") and, for the values Y, by PI-3 (default: "values computed, not printed"). On Y: FEID.json has no key for the f0 CIDEr-D of each baseline. It can be derived from the one-sided rows of I-42 as the printed value of the third KTVIC row (136.0, quoted at l.260) plus the stored gap: 48.85 [n412] for ktvic_resnetlstm and 72.87 [n413] for ktvic_vittrans. These equal the O4 values of l.70 to two decimals, so they are POST HOC. The derivation is this note's, not a stored value; the judge rules whether it may be used.
- **C-P3b** (POST HOC; l.291-292). "No matched member of F reproduces the printed CIDEr-D of either baseline." The code's lists are empty for both baselines (I-19; not recomputed). BLOCKED by PI-2 as C-P3.
- **C-P4** (DEVELOPMENT; METHOD CHECK (§6.4, not a prediction); l.297-298). "Among the 24 planted cases, 9 [n174] were IDENTIFIED, 15 [n175] AMBIGUOUS and 0 [n176] OUTSIDE (the identifiability rate at one printed decimal). Fewer than 12 were IDENTIFIED, so the identification label is NOT_EVALUABLE and FE-ID is reported as a reproduction table." No wrong recovery raised a FAULT.
- **C-FEID** (reproduction table without identification labels; l.384). The table of I-41, with both caveats of l.238 and the neutral wording of l.254 and l.426. BLOCKED by PI-2 as C-P3.
- **C-printed** (DESCRIPTIVE; l.261). "0 [n405] of 1 [n404] printed comparisons change order under matched scoring; 0 [n406] of 1 [n404] are not certified over F", with n stated, and with the 2 [n402] one-sided and 3 [n403] 'neither' pairs named as such. An order change was not detected in a pool of one pair. The pair names two published systems: PI-6 (default: "verdicts reported as counts by repository, systems not named") and PI-3 apply.
- **C-gate** (DESCRIPTIVE). "Of 19 [n309] files put through the structure gate, 16 [n414] were admitted and 3 [n308] failed rule 1; 22 [n032] first-look comparisons were formed, 20 [n044] from repository loc110504 and 2 [n045] from repository vanngthi." The 19 files are the 17 files of other groups and the two KTVIC baseline files (the baseline pair itself is in D). Line 430 asks the paper to state the share that comes from one repository.
- **C-secondary** (DESCRIPTIVE; no verdict; l.308-310). The FE-PRED value 0.8012 [n336] and the rows of I-38, each labelled where printed. The extra row of I-37 has no registered label.
- **C-control** (CONTROL). "The English control was NOT RUN." (l.311)
- **C-multiplicity** (l.318). "about 2.5% of comparisons with a true null under some member may be certified in error"; no family-wise claim.

### 4.2 What may not be claimed (registered limits, quoted)

- l.28: "Never called "held-out test", "test-set result" or "confirmatory""
- l.425: "FL results are "a first scoring of other groups' released outputs"; where the references are KTVIC or UIT-ViIC test references, the text says that those references were used before. Never "held-out test"."
- l.63: "None may be cited as a result of this registration."
- l.79: "Every certificate on the 73 own files and the two baselines is `DEVELOPMENT`."
- l.174: "**Not guaranteed:** front ends outside G; learned metrics; human agreement; anything about another language; the absence of training exposure of the systems (irrelevant to the certificate, which concerns the metric's verdict on given outputs, not system quality)."
- l.173: "**Nominal, not exact.** Each per-member test here is a percentile bootstrap at one-sided 2.5% per direction, so the guarantee is nominal. It holds conditional on the reference sets and on the document frequencies of the full list."
- l.238: "What it cannot show: that the true pipeline is in F⁺, or that the released outputs are the ones that were scored. Every FE-ID sentence carries both caveats."
- l.261: "No word such as "wrong", "error" or "invalid" is attached to a published score."
- l.426: "No sentence says that the published scores are wrong or erroneous. Its CIDEr-D and BLEU-4 part is POST HOC (seen October 2026)."
- l.276: "Comparisons share files, so they are not independent; the Clopper–Pearson bound is a nominal summary."
- l.318: "no family-wise claim"
- l.319: "No overall "success" statement combines them; none is dropped from the report."
- l.351: "**After stage 2**, any further analysis on FL files is POST HOC."
- l.424: "The certificate is called a combination of known ideas, credited as in §3.3. No "first" claim."
- l.427: "Neither statement is changed without the PI's answer."
- l.428: "No claim beyond Vietnamese. The English control is a control."
- l.430: "The 73 own files are described as variants of the authors' own systems; 12 of the 14 other-group systems have no paper; up to 20 of 32 FL comparisons come from one repository."
- l.445: "Further limits: the own files are one backbone family; CIDEr-D is the only metric with a verdict; per-image human preferences say nothing direct about system-level orders; the family is enumerated, so nothing is guaranteed outside it; the bootstrap guarantee is nominal; KTVIC images and references were used before."
- l.304: "The human result never changes F, a certificate, a P1 to P3 label or the P4 method check."
- l.387: "Every FAIL appears where a PASS would have appeared, at the same length."
- On spent references: l.26 labels every number on the own KTVIC files and the two baselines as computed 'on spent references'; l.28 says the references of a first scoring 'may be spent (KTVIC test, UIT-ViIC test)'; l.425 requires that 'where the references are KTVIC or UIT-ViIC test references, the text says that those references were used before'. The formed FL comparisons use the reference files of groups G1 to G4 (l.196-199); whether any of them is a UIT-ViIC test reference file in the sense of l.425 is not settled by the files this note read.
- Wording rule of this note: where a count is 0 the candidate says that the thing was not detected in this pool. It does not say that there is no effect.
- §17 defaults in force until the principal investigator answers: PI-2 l.494: "kept out of paper text until the PI answers"; PI-3 l.495: "values computed, not printed"; PI-6 l.498: "verdicts reported as counts by repository, systems not named".

## 5. Deviations and environment facts a paper must disclose

From the LOG lines OPS-1113ch to OPS-1114f, one line each. Lines in that id range that belong to other papers are left out. The machine is called 'the rented host'.

| LOG id | Fact |
|---|---|
| OPS-1113ch | Rental and environment. One rented host with one RTX 3090, a 16-core CPU and 64 GB of memory, Ubuntu 24.04; all stages ran on CPU only. DEVIATION recorded there: the offer taken was not the cheapest passing offer; the reason given is the unmeasured stage times before K-time and that the same host type made the G0 records of record. Java was installed at the pinned build (version 21_0_13_0_3); Python 3.12.3. |
| OPS-1113ci | Code on the host: a git archive of commit 9e6578a restricted to 34 paths, sums checked; the segmenter jar and its models (8 files) checked on the host. No data was on the host before G0. |
| OPS-1113cj | Environment fix before G0: the host image had no `python3` command; the packages python3 and python3-venv were installed; no pin and no code changed. The browser environment for the page tests was set up before G0. The study environment was built from the 34 pinned wheels; its freeze hash equals the pin. |
| OPS-1113ck | G0 passed at the first attempt: self-test 47 of 47, pair-builder self-test 39 of 39 twice with equal fixtures, mutants 94 of 94 killed, toy environment as recorded. |
| OPS-1113cl | Source line for the fetched files and the one b2 score file, written before the data push because stage C reads the score file's field names. |
| OPS-1113cm | DEVIATION: the first data push stopped after about 10 seconds ('1 score files, not 67'). Cause: a loop in the laptop push script lost its input to a remote shell call, so one name of 73 was pushed. Five files were on the host, each equal to its laptop sha; no stage had run. In the same hour the first page-test run stopped with rc 9 because the host image lacked the `ss` tool (synthetic fixtures only). |
| OPS-1113cn | The push-script fix of ruling CC-390 was applied by byte match: two lines of the laptop helper changed (the loop reads from its own file descriptor). No study code changed. The as-run script is kept beside it. |
| OPS-1113co | Environment change AFTER G0 (allowed by CC-390 ruling 4 and its addendum 1): the package iproute2 was installed while no stage was running. It pulled in one upgrade, libcap2 from patch level 2_66-5ubuntu2_2 to 2_66-5ubuntu2_4, and four new packages. Afterwards the Java version, the freeze hash of the study environment and the jar hash were re-read and equal their pins. G0 was not re-run. |
| OPS-1113cp | Page tests of the pair page on synthetic fixtures: the second run passed 19 of 19; the first run (rc 9) is kept as a record and is not the cited run. No study data was read by these tests. |
| OPS-1113cq | Data push by the fixed script: 167 files by explicit name, manifest hash equal on both sides, host check 'OK (167 files)'. No label, key, image, printed-values file or pilot file was on the host. |
| OPS-1113ct | GATE-PRE-G passed before stage G: every first-look file and reference file equals its pinned hash; both baselines match their blobs. |
| OPS-1113cu | Timing note (report only): stages F, C and G each ended in under 30 seconds; no code or rule changed. |
| OPS-1113cy | After stage 1 and the pin step: first pull (126 files, hashes checked on both sides); DEV.json and NC.json copied read-only to the registered pins folder (l.343). No stage-1 figure was displayed. |
| OPS-1113cz | The build of the pair files for the human arm ran once, between the pin and stage 2a (order allowed by CC-388 ruling 3 #1; it reads no score). Its five output files were moved to the laptop label folder and deleted from the host. No output file and no build count was opened or shown. Nothing is served yet. |
| OPS-1113dg | GATE-3 before stage 3: the pin-form line for PRINTED.json (OPS-1113df) was logged; the file was sent to the host by hash only. Custody line OPS-1113br ('did not open … complete') gives the branch 'run as registered' for M_new. |
| OPS-1114e | End of the stage block: no stage returned rc 3 or 4, every stage ran once, all ended about 59 hours before K-time. Second pull: 163 files, hashes checked on both sides. The coordinator opened no work file and no stdout of stages 1, 2a, 2b, 3 or of the build. |
| OPS-1114f | The rented host was deleted at about 2026-11-13T17:45:20Z after the second pull. The deletion is the removal line for the study data on the host. No label and no key was ever on it. Stage H will need a new host with a new G0 line. |

Also to disclose, from the rulings: the custody sentence of CC-385 W5 on the agent that wrote the second version of the code (it read the pinned transcription of the printed values and copied real printed values into two self-test fixtures; corrected by record, OPS-1113bm). Its bracketed last clause is kept, because OPS-1113br says 'did not open … complete'.

Record facts found while writing this note (not in the LOG; not resolved here):

- **R1.** `runs.log`, `1.start` and `DEV.json::utc_start` give the start of stage 1 as 2026-11-13T15:15:29Z. LOG line OPS-1113cy gives 15:15:31Z. Other start and end stamps of the JSON files differ from `runs.log` by at most 2 seconds (the runner and the code each read the clock).
- **R2.** `3.stdout` holds 29 pairs of count lines printed by the BLEU scorer of pycocoevalcap ('testlen', 'reflen', 'guess', 'correct', and a 'ratio' line) before the STAGE line. They are aggregate n-gram counts of the 29 r* runs (1 toy check, 24 planted files, 2 baselines in the FE-ID table, 2 baselines for P3). They hold no text. The docstring of the code (b_fecert.py l.22) says that outputs and stdout hold 'names, counts, labels, scores and sha256 only'; these lines are counts.
- **R3.** `3.stderr` holds one PTB lexer warning: an untokenizable U+FFFD character. It sits between the reference line and the output line of the 24th r* run after the toy check. By the order of the code (b_fecert.py l.1286) that run is the last file of the planted set, an own file, not a KTVIC baseline. This reading of the position is this note's inference. The warning does not touch the P3 rows, which come from the baseline runs.
- **R4.** `3.outputs.sha256` lists FEID.json and PLANT_KEY.json. PLANT_PRINTED.json, also written by stage 3, is not in that list; it is in the pull list of OPS-1114e.
- **R5.** The census found the segmenter value "whitespace" beside "rdrsegmenter" in some own score files (I-35). It is not an underthesea or character-unit hit, so no rule fires.

## 6. What is still open

- The one-judge result read of this note (l.416).
- Labelling by both raters and the Paper B closing LOG line (l.415; closing form of CC-388 ruling 5(c)). Until then this note and every stage figure stay held from the principal investigator (CC-388 W6).
- Stage H after the closing line, on a new rented host with a new G0 line (OPS-1114f; CC-388 ruling 5(c)), before K-time 2026-11-16T05:00Z; then the pin of HUMAN.json and the human result read (l.417). If stage H does not finish by K-time it is NOT RUN (l.369).
- K-human and the human hypotheses H-P and H-U (labelling plan). By l.304 the human result decides only the recommended default member.
- The O5 row beside r* (l.293): owed, POST HOC, from the stored E4 file, by an agent allowed to open it, after this read.
- The matched f0 scores 'Y' of the two baselines for the sentence of l.382: no stored key; a ruling on the derivation of section 4 or on a small output step.
- Answers of the principal investigator to §17 PI-2, PI-3 and PI-6 (wording toward the KTVIC authors; printing matched baseline scores; naming other-group systems). They may be asked without any figure.
- A ruling on points J1 and J2 (the LOW-SENSITIVITY sentence).
- The custody disclosure sentence of CC-385 W5 for the paper's custody section.
- The citations of l.172 and l.176 marked 'unverified today' in the registration, to be read before any text cites them.
- The result commit (section 7) and the commit of key.json after the closing line (CC-385 W1).
- The freeze of 2026-11-16 12:00 Vietnam time (l.418).
- Any further analysis on the FL files is POST HOC (l.351).

## 7. Proposed commit list for the result commit (for the judge to rule)

The registration names no result file as 'committed'. A search of the registration for 'commit' finds only the stage-0a and stage-0b commits (l.337-338), the commit of documents (l.413-414) and background lines. So the list below is a proposal, not a registered list. Nothing under `.session_backup/2026-11-13/` or `.session_backup/2026-11-12/b_fecert/` is tracked today.

**Custody point first (J9).** Every file of group B below, and this note, holds figures of stages 1, 2a, 2b or 3. A commit puts them in the history of the repository that the principal investigator reads. CC-388 W6 holds such figures from him until his closing line. Proposal: commit group A now if the judge agrees; commit group B and this note only after the closing line. The judge rules.

Group A: structure and environment only (no stage-1 to stage-3 figure):

| Path (under the pulled folder) | sha256 | Bytes |
|---|---|---|
| `b_work/FAMILY.json` | `431d92a4a2eaf0516446c9f9aef453ee52d311b6e329d97cd1abb4c4e8017f77` | 11,826 |
| `b_work/CENSUS.json` | `2252167b435890c5dbf70a97e0fc918bc6989c48acda636427d4dd2889599afa` | 55,350 |
| `b_work/SYSTEMS.tsv` | `30ac9555cd6cdc8fd50f47e637e734fac564c692605f590ba213a60a3be6e1a0` | 10,721 |
| `b_work/GATE2.json` | `26110b5f1d87a8369e54e0a696c171698cd980ee6ae1ef2153e8b93c5ee93c61` | 12,817 |
| `b_records/runs.log` | `ea5a6f33451c4444befdeeaa0d1f33aa85ab64be126c40087a36813838f51fe5` | 1,280 |

Group B: result files (after the closing line):

| Path | sha256 | Bytes | Note |
|---|---|---|---|
| `b_work/NC.json` | `1d2e05d2e0098ea1bb11bc7a484b4c158c6ca698b45f9a3929cfe8b0da08428d` | 1,643 |  |
| `b_work/V.json` | `1f011538bf06a601c2104116ccef31f470eed473b2a96c9e6f8a5408f126f6b9` | 143,460 |  |
| `b_work/RESULT.json` | `25614b469cf59dc61f15e839b89a8e78ca0b316905afc4bd2ae52eaa0d32b43a` | 298,859 |  |
| `b_work/FEID.json` | `1f56a5ce8c5fd434b19409322d275478ec999d41d34447cfca719a35b040b1f7` | 11,778 |  |
| `b_work/DEV.json` | `88ff39aa9552b671a0e439aec961d0fefe02df1f52a2a5df9765a9d8226f7e8d` | 21,637,043 | about 21.6 MB; the judge may prefer the pinned read-only copy under `.session_backup/2026-11-12/b_fecert/pins/` or a hash-only record |
| `b_records/3.stdout` | `875076818c391fa110403be7248c89a8c2219a679167614d64bc1a060b55fd3c` | 3,921 | library count lines and tokeniser lines (R2, R3) |
| `b_records/3.stderr` | `fc07dd11dc9e08ae8267828fe6131f467c2ef0ac0bf602839217da5bbaccba78` | 4,025 | library count lines and tokeniser lines (R2, R3) |
| `manuscript/prereg/2026-11-12_b_fecert/results/B_FECERT_RESULT_NOTE_v1.md` | (sha256 in the writer's message to the coordinator) | | this note |

The other small records of `b_records/` for stages F to 3 (`.rc`, `.args`, `.start`, `.end`, `.time`, `.outputs.sha256`, the stdout of F, C, G, 1, pin, 2a, 2b, and PRE_G.txt) hold stamps, commands with host-side paths, and hashes. They can go with group A if the judge wants the run record in the repository; the `.args` and `.time` files should first pass the usual scan for host strings.

NOT to be committed in the result commit, and why:

- `b_work/PAIR_CANDIDATES.json` (pin 2274d989…): input of the human arm; not opened for this note; held at least until the closing line (labelling-plan custody).
- `b_work/PLANT_KEY.json` (sha256 9386e704f8c9481ac0c1f69f652084074aa722e75d5cc0cd7b1289a9b7a837a2 as copied from `3.outputs.sha256`) and `b_work/PLANT_PRINTED.json`: not opened and not hashed for this note. They are method-check files (l.246, l.346) and hold rounded scores of own files; the judge rules whether they join group B.
- `b_records/build.stdout`, `build.stderr` and every build output (key, assignment, practice, BUILD counts, items manifest): human-arm custody (CC-388 ruling 3 #10); key.json is committed only after the closing line (CC-385 W1).
- Any label file, any file under the label folders, the sealed folders.
- Any data file: references, `*.preds.json`, stored score files, the fetched files of other groups (no caption text is committed, l.44; the files of repositories without a licence are aggregate-only, l.209), pilot_results.json.
- The page-test folders of `b_records/` (synthetic fixtures; they belong to the pair-tool record, not to the result).

## 8. Table of every figure in this note

Columns: tag; value as shown; file; key (or how the figure was derived); raw value; first 8 hex digits of the file's sha256; evidence label. 'derived' means the figure has no key of its own and was computed by this note from the named file. Stamps, hashes, line numbers and the registered constants of the next table are not listed here. Counts copied from LOG lines in sections 1.4 and 5 (the G0 checks, the file counts of pushes and pulls, the page tests) are LOG facts under the named ids and are not listed. The wall times and return codes of section 1.4 are copied from `runs.log` and are not listed. The cells of the table of first-look comparisons in section 2.2 are covered by the pattern row at the end.

| Tag | Shown | File | Key | Raw value | sha256 prefix | Label |
|---|---|---|---|---|---|---|
| n001 | 1101 | DEV.json | `derived: len(comparisons)` | 1101 | 88ff39aa | DEVELOPMENT |
| n002 | 22 | V.json | `derived: len(fl)` | 22 | 1f011538 | FIRST SCORING OF RELEASED OUTPUTS |
| n003 | 918 | V.json | `cert_dev` | 918 | 1f011538 | DEVELOPMENT + FIRST SCORING OF RELEASED OUTPUTS |
| n004 | 9 | V.json | `cert_dev_FL` | 9 | 1f011538 | FIRST SCORING OF RELEASED OUTPUTS |
| n005 | 72 | DEV.json + V.json | `derived: count of Cert_dev with z_min <= 4` | 72 | 88ff39aa + 1f011538 | DEVELOPMENT + FIRST SCORING OF RELEASED OUTPUTS |
| n006 | 72 | V.json | `N` | 72 | 1f011538 | DEVELOPMENT + FIRST SCORING OF RELEASED OUTPUTS |
| n007 | 68 | V.json | `derived: ids of V starting with D:` | 68 | 1f011538 | DEVELOPMENT |
| n008 | 4 | V.json | `derived: ids of V starting with FL:` | 4 | 1f011538 | FIRST SCORING OF RELEASED OUTPUTS |
| n009 | 0 | DEV.json + V.json | `derived: classes of F_dev with sd_boot <= 0` | 0 | 88ff39aa + 1f011538 | DESCRIPTIVE |
| n010 | 72 | RESULT.json | `P1.N` | 72 | 25614b46 | DEVELOPMENT + FIRST SCORING OF RELEASED OUTPUTS |
| n011 | 2 | RESULT.json | `P1.breaks` | 2 | 25614b46 | HELD-OUT FRONT END |
| n012 | 0.0278 | RESULT.json | `P1.r` | 0.027777777777777776 | 25614b46 | HELD-OUT FRONT END |
| n013 | 0.0849 | RESULT.json | `P1.cp_upper_95` | 0.08486917446626821 | 25614b46 | HELD-OUT FRONT END |
| n014 | 0.0050 | RESULT.json | `P1.cp_lower_95` | 0.004957895842999783 | 25614b46 | HELD-OUT FRONT END |
| n015 | 915 | NC.json | `cert_NC` | 915 | 1d2e05d2 | DEVELOPMENT |
| n016 | 54 | DEV.json | `derived: count of Cert_NC with z_min^NC <= 4` | 54 | 88ff39aa | DEVELOPMENT |
| n017 | 915 | NC.json | `V_NC` | 915 | 1d2e05d2 | DEVELOPMENT |
| n018 | 6 | NC.json | `breaks` | 6 | 1d2e05d2 | DEVELOPMENT |
| n019 | 0.0066 | NC.json | `r_NC` | 0.006557377049180328 | 1d2e05d2 | DEVELOPMENT |
| n020 | 9 | RESULT.json | `P1_beside.FL_row.n` | 9 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n021 | 1 | RESULT.json | `P1_beside.FL_row.breaks` | 1 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS, HELD-OUT FRONT END |
| n022 | 0.0057 | RESULT.json | `P1_beside.FL_row.cp_lower_95` | 0.005683044988048048 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS, HELD-OUT FRONT END |
| n023 | 0.4291 | RESULT.json | `P1_beside.FL_row.cp_upper_95` | 0.42913554703143447 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS, HELD-OUT FRONT END |
| n024 | 918 | RESULT.json | `P1_beside.all_Cert_dev.n` | 918 | 25614b46 | DEVELOPMENT + FIRST SCORING OF RELEASED OUTPUTS |
| n025 | 2 | RESULT.json | `P1_beside.all_Cert_dev.breaks` | 2 | 25614b46 | HELD-OUT FRONT END |
| n026 | 909 | DEV.json | `derived: count of D comparisons CERTIFIED over F_dev` | 909 | 88ff39aa | DEVELOPMENT |
| n027 | 1 | RESULT.json | `P1_beside.D_only.breaks` | 1 | 25614b46 | DEVELOPMENT, HELD-OUT FRONT END |
| n028 | 1 | RESULT.json | `P1_beside.FL_only.breaks` | 1 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS, HELD-OUT FRONT END |
| n029 | 0 | RESULT.json | `P1.reversals` | 0 | 25614b46 | HELD-OUT FRONT END |
| n030 | 16 | RESULT.json | `P1_beside.with_chr_DESCRIPTIVE.breaks` | 16 | 25614b46 | DESCRIPTIVE |
| n031 | 3 | RESULT.json | `P1_beside.with_chr_DESCRIPTIVE.reversals` | 3 | 25614b46 | DESCRIPTIVE |
| n032 | 22 | GATE2.json | `formed` | 22 | 26110b5f | DESCRIPTIVE |
| n033 | 10 | RESULT.json | `P2.n_FL` | 10 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n034 | 2 | RESULT.json | `P2.k_FL` | 2 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS, HELD-OUT FRONT END |
| n035 | 0.2000 | RESULT.json | `counts.FL_over_F.CHANGED_share` | 0.2 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n036 | 9 | RESULT.json | `P2.per_repository_n_k.loc110504.0` | 9 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n037 | 2 | RESULT.json | `P2.per_repository_n_k.loc110504.1` | 2 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n038 | 1 | RESULT.json | `P2.per_repository_n_k.vanngthi.0` | 1 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n039 | 0 | RESULT.json | `P2.per_repository_n_k.vanngthi.1` | 0 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n040 | 1 | RESULT.json | `P2.leave_one_repository_out.loc110504.n` | 1 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n041 | 0 | RESULT.json | `P2.leave_one_repository_out.loc110504.k` | 0 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n042 | 9 | RESULT.json | `P2.leave_one_repository_out.vanngthi.n` | 9 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n043 | 2 | RESULT.json | `P2.leave_one_repository_out.vanngthi.k` | 2 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n044 | 20 | GATE2.json | `derived: formed comparisons with repo loc110504` | 20 | 26110b5f | DESCRIPTIVE |
| n045 | 2 | GATE2.json | `derived: formed comparisons with repo vanngthi` | 2 | 26110b5f | DESCRIPTIVE |
| n046 | 1101 | RESULT.json | `counts.D_over_F_dev_DEVELOPMENT.comparisons` | 1101 | 25614b46 | DEVELOPMENT |
| n047 | 909 | RESULT.json | `counts.D_over_F_dev_DEVELOPMENT.CERTIFIED` | 909 | 25614b46 | DEVELOPMENT |
| n048 | 59 | RESULT.json | `counts.D_over_F_dev_DEVELOPMENT.FRAGILE` | 59 | 25614b46 | DEVELOPMENT |
| n049 | 2 | RESULT.json | `counts.D_over_F_dev_DEVELOPMENT.REVERSED` | 2 | 25614b46 | DEVELOPMENT |
| n050 | 133 | RESULT.json | `counts.D_over_F_dev_DEVELOPMENT.NULL-STABLE` | 133 | 25614b46 | DEVELOPMENT |
| n051 | 936 | RESULT.json | `counts.D_over_F_dev_DEVELOPMENT.significant_under_f0` | 936 | 25614b46 | DEVELOPMENT |
| n052 | 27 | RESULT.json | `counts.D_over_F_dev_DEVELOPMENT.CHANGED` | 27 | 25614b46 | DEVELOPMENT |
| n053 | 0.0288 | RESULT.json | `counts.D_over_F_dev_DEVELOPMENT.CHANGED_share` | 0.028846153846153848 | 25614b46 | DEVELOPMENT |
| n054 | 58 | RESULT.json | `counts.D_over_F_dev_DEVELOPMENT.point_flips` | 58 | 25614b46 | DEVELOPMENT |
| n055 | 22 | RESULT.json | `counts.FL_over_F_dev.comparisons` | 22 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n056 | 9 | RESULT.json | `counts.FL_over_F_dev.CERTIFIED` | 9 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n057 | 6 | RESULT.json | `counts.FL_over_F_dev.FRAGILE` | 6 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n058 | 0 | RESULT.json | `counts.FL_over_F_dev.REVERSED` | 0 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n059 | 7 | RESULT.json | `counts.FL_over_F_dev.NULL-STABLE` | 7 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n060 | 10 | RESULT.json | `counts.FL_over_F_dev.significant_under_f0` | 10 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n061 | 1 | RESULT.json | `counts.FL_over_F_dev.CHANGED` | 1 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n062 | 0.1000 | RESULT.json | `counts.FL_over_F_dev.CHANGED_share` | 0.1 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n063 | 3 | RESULT.json | `counts.FL_over_F_dev.point_flips` | 3 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n064 | 1101 | RESULT.json | `counts.D_over_F_DEVELOPMENT.comparisons` | 1101 | 25614b46 | DEVELOPMENT; F includes the HELD-OUT FRONT END members |
| n065 | 908 | RESULT.json | `counts.D_over_F_DEVELOPMENT.CERTIFIED` | 908 | 25614b46 | DEVELOPMENT; F includes the HELD-OUT FRONT END members |
| n066 | 62 | RESULT.json | `counts.D_over_F_DEVELOPMENT.FRAGILE` | 62 | 25614b46 | DEVELOPMENT; F includes the HELD-OUT FRONT END members |
| n067 | 2 | RESULT.json | `counts.D_over_F_DEVELOPMENT.REVERSED` | 2 | 25614b46 | DEVELOPMENT; F includes the HELD-OUT FRONT END members |
| n068 | 131 | RESULT.json | `counts.D_over_F_DEVELOPMENT.NULL-STABLE` | 131 | 25614b46 | DEVELOPMENT; F includes the HELD-OUT FRONT END members |
| n069 | 936 | RESULT.json | `counts.D_over_F_DEVELOPMENT.significant_under_f0` | 936 | 25614b46 | DEVELOPMENT; F includes the HELD-OUT FRONT END members |
| n070 | 28 | RESULT.json | `counts.D_over_F_DEVELOPMENT.CHANGED` | 28 | 25614b46 | DEVELOPMENT; F includes the HELD-OUT FRONT END members |
| n071 | 0.0299 | RESULT.json | `counts.D_over_F_DEVELOPMENT.CHANGED_share` | 0.029914529914529916 | 25614b46 | DEVELOPMENT; F includes the HELD-OUT FRONT END members |
| n072 | 65 | RESULT.json | `counts.D_over_F_DEVELOPMENT.point_flips` | 65 | 25614b46 | DEVELOPMENT; F includes the HELD-OUT FRONT END members |
| n073 | 22 | RESULT.json | `counts.FL_over_F.comparisons` | 22 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; F includes the HELD-OUT FRONT END members |
| n074 | 8 | RESULT.json | `counts.FL_over_F.CERTIFIED` | 8 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; F includes the HELD-OUT FRONT END members |
| n075 | 8 | RESULT.json | `counts.FL_over_F.FRAGILE` | 8 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; F includes the HELD-OUT FRONT END members |
| n076 | 0 | RESULT.json | `counts.FL_over_F.REVERSED` | 0 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; F includes the HELD-OUT FRONT END members |
| n077 | 6 | RESULT.json | `counts.FL_over_F.NULL-STABLE` | 6 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; F includes the HELD-OUT FRONT END members |
| n078 | 10 | RESULT.json | `counts.FL_over_F.significant_under_f0` | 10 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; F includes the HELD-OUT FRONT END members |
| n079 | 2 | RESULT.json | `counts.FL_over_F.CHANGED` | 2 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; F includes the HELD-OUT FRONT END members |
| n080 | 3 | RESULT.json | `counts.FL_over_F.point_flips` | 3 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; F includes the HELD-OUT FRONT END members |
| n081 | 536 | RESULT.json | `derived: comparisons of set D with F = CERTIFIED (a > b)` | 536 | 25614b46 | DEVELOPMENT; HELD-OUT FRONT END members included |
| n082 | 372 | RESULT.json | `derived: comparisons of set D with F = CERTIFIED (b > a)` | 372 | 25614b46 | DEVELOPMENT; HELD-OUT FRONT END members included |
| n083 | 60 | RESULT.json | `derived: comparisons of set D with F = FRAGILE` | 60 | 25614b46 | DEVELOPMENT; HELD-OUT FRONT END members included |
| n084 | 131 | RESULT.json | `derived: comparisons of set D with F = NULL-STABLE` | 131 | 25614b46 | DEVELOPMENT; HELD-OUT FRONT END members included |
| n085 | 2 | RESULT.json | `derived: comparisons of set D with F = REVERSED` | 2 | 25614b46 | DEVELOPMENT; HELD-OUT FRONT END members included |
| n086 | 3 | RESULT.json | `derived: comparisons of set FL with F = CERTIFIED (a > b)` | 3 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; HELD-OUT FRONT END members included |
| n087 | 5 | RESULT.json | `derived: comparisons of set FL with F = CERTIFIED (b > a)` | 5 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; HELD-OUT FRONT END members included |
| n088 | 8 | RESULT.json | `derived: comparisons of set FL with F = FRAGILE` | 8 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; HELD-OUT FRONT END members included |
| n089 | 6 | RESULT.json | `derived: comparisons of set FL with F = NULL-STABLE` | 6 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; HELD-OUT FRONT END members included |
| n090 | 1123 | RESULT.json | `derived: len(comparisons)` | 1123 | 25614b46 | DESCRIPTIVE |
| n091 | 654 | RESULT.json | `counts.D_over_F_dev_DEVELOPMENT.breaking_levels.syl` | 654 | 25614b46 | DEVELOPMENT |
| n092 | 573 | RESULT.json | `counts.D_over_F_dev_DEVELOPMENT.breaking_levels.rdr` | 573 | 25614b46 | DEVELOPMENT |
| n093 | 525 | RESULT.json | `counts.D_over_F_dev_DEVELOPMENT.breaking_levels.pyvi` | 525 | 25614b46 | DEVELOPMENT |
| n094 | 575 | RESULT.json | `counts.D_over_F_dev_DEVELOPMENT.breaking_levels.tw` | 575 | 25614b46 | DEVELOPMENT |
| n095 | 588 | RESULT.json | `counts.D_over_F_dev_DEVELOPMENT.breaking_levels.tm` | 588 | 25614b46 | DEVELOPMENT |
| n096 | 589 | RESULT.json | `counts.D_over_F_dev_DEVELOPMENT.breaking_levels.tf` | 589 | 25614b46 | DEVELOPMENT |
| n097 | 604 | RESULT.json | `counts.D_over_F_dev_DEVELOPMENT.breaking_levels.pk` | 604 | 25614b46 | DEVELOPMENT |
| n098 | 617 | RESULT.json | `counts.D_over_F_dev_DEVELOPMENT.breaking_levels.pf` | 617 | 25614b46 | DEVELOPMENT |
| n099 | 531 | RESULT.json | `counts.D_over_F_dev_DEVELOPMENT.breaking_levels.pa` | 531 | 25614b46 | DEVELOPMENT |
| n100 | 850 | RESULT.json | `counts.D_over_F_dev_DEVELOPMENT.breaking_levels.cf` | 850 | 25614b46 | DEVELOPMENT |
| n101 | 902 | RESULT.json | `counts.D_over_F_dev_DEVELOPMENT.breaking_levels.ck` | 902 | 25614b46 | DEVELOPMENT |
| n102 | 36 | RESULT.json | `counts.FL_over_F_dev.breaking_levels.syl` | 36 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n103 | 81 | RESULT.json | `counts.FL_over_F_dev.breaking_levels.rdr` | 81 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n104 | 72 | RESULT.json | `counts.FL_over_F_dev.breaking_levels.pyvi` | 72 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n105 | 63 | RESULT.json | `counts.FL_over_F_dev.breaking_levels.tw` | 63 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n106 | 63 | RESULT.json | `counts.FL_over_F_dev.breaking_levels.tm` | 63 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n107 | 63 | RESULT.json | `counts.FL_over_F_dev.breaking_levels.tf` | 63 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n108 | 63 | RESULT.json | `counts.FL_over_F_dev.breaking_levels.pk` | 63 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n109 | 63 | RESULT.json | `counts.FL_over_F_dev.breaking_levels.pf` | 63 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n110 | 63 | RESULT.json | `counts.FL_over_F_dev.breaking_levels.pa` | 63 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n111 | 99 | RESULT.json | `counts.FL_over_F_dev.breaking_levels.cf` | 99 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n112 | 90 | RESULT.json | `counts.FL_over_F_dev.breaking_levels.ck` | 90 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS |
| n113 | 690 | RESULT.json | `counts.D_over_F_DEVELOPMENT.breaking_levels.syl` | 690 | 25614b46 | DEVELOPMENT; HELD-OUT FRONT END members included |
| n114 | 609 | RESULT.json | `counts.D_over_F_DEVELOPMENT.breaking_levels.rdr` | 609 | 25614b46 | DEVELOPMENT; HELD-OUT FRONT END members included |
| n115 | 561 | RESULT.json | `counts.D_over_F_DEVELOPMENT.breaking_levels.pyvi` | 561 | 25614b46 | DEVELOPMENT; HELD-OUT FRONT END members included |
| n116 | 630 | RESULT.json | `counts.D_over_F_DEVELOPMENT.breaking_levels.uts` | 630 | 25614b46 | DEVELOPMENT; HELD-OUT FRONT END members included |
| n117 | 821 | RESULT.json | `counts.D_over_F_DEVELOPMENT.breaking_levels.tw` | 821 | 25614b46 | DEVELOPMENT; HELD-OUT FRONT END members included |
| n118 | 834 | RESULT.json | `counts.D_over_F_DEVELOPMENT.breaking_levels.tm` | 834 | 25614b46 | DEVELOPMENT; HELD-OUT FRONT END members included |
| n119 | 835 | RESULT.json | `counts.D_over_F_DEVELOPMENT.breaking_levels.tf` | 835 | 25614b46 | DEVELOPMENT; HELD-OUT FRONT END members included |
| n120 | 844 | RESULT.json | `counts.D_over_F_DEVELOPMENT.breaking_levels.pk` | 844 | 25614b46 | DEVELOPMENT; HELD-OUT FRONT END members included |
| n121 | 875 | RESULT.json | `counts.D_over_F_DEVELOPMENT.breaking_levels.pf` | 875 | 25614b46 | DEVELOPMENT; HELD-OUT FRONT END members included |
| n122 | 771 | RESULT.json | `counts.D_over_F_DEVELOPMENT.breaking_levels.pa` | 771 | 25614b46 | DEVELOPMENT; HELD-OUT FRONT END members included |
| n123 | 1207 | RESULT.json | `counts.D_over_F_DEVELOPMENT.breaking_levels.cf` | 1207 | 25614b46 | DEVELOPMENT; HELD-OUT FRONT END members included |
| n124 | 1283 | RESULT.json | `counts.D_over_F_DEVELOPMENT.breaking_levels.ck` | 1283 | 25614b46 | DEVELOPMENT; HELD-OUT FRONT END members included |
| n125 | 54 | RESULT.json | `counts.FL_over_F.breaking_levels.syl` | 54 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; HELD-OUT FRONT END members included |
| n126 | 99 | RESULT.json | `counts.FL_over_F.breaking_levels.rdr` | 99 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; HELD-OUT FRONT END members included |
| n127 | 90 | RESULT.json | `counts.FL_over_F.breaking_levels.pyvi` | 90 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; HELD-OUT FRONT END members included |
| n128 | 48 | RESULT.json | `counts.FL_over_F.breaking_levels.uts` | 48 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; HELD-OUT FRONT END members included |
| n129 | 97 | RESULT.json | `counts.FL_over_F.breaking_levels.tw` | 97 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; HELD-OUT FRONT END members included |
| n130 | 97 | RESULT.json | `counts.FL_over_F.breaking_levels.tm` | 97 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; HELD-OUT FRONT END members included |
| n131 | 97 | RESULT.json | `counts.FL_over_F.breaking_levels.tf` | 97 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; HELD-OUT FRONT END members included |
| n132 | 96 | RESULT.json | `counts.FL_over_F.breaking_levels.pk` | 96 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; HELD-OUT FRONT END members included |
| n133 | 96 | RESULT.json | `counts.FL_over_F.breaking_levels.pf` | 96 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; HELD-OUT FRONT END members included |
| n134 | 99 | RESULT.json | `counts.FL_over_F.breaking_levels.pa` | 99 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; HELD-OUT FRONT END members included |
| n135 | 153 | RESULT.json | `counts.FL_over_F.breaking_levels.cf` | 153 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; HELD-OUT FRONT END members included |
| n136 | 138 | RESULT.json | `counts.FL_over_F.breaking_levels.ck` | 138 | 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; HELD-OUT FRONT END members included |
| n137 | 53.0 | FEID.json | `P3.M_new_rows.ktvic_resnetlstm.BLEU-1.printed` | "53.0" | 1f56a5ce | DESCRIPTIVE (value printed in a public source) |
| n138 | 52.9625 | FEID.json | `P3.M_new_rows.ktvic_resnetlstm.BLEU-1.rstar` | 52.96247049791305 | 1f56a5ce | REGISTERED PREDICTION, DEVELOPMENT DATA (M_new) |
| n139 | 0.0375 | FEID.json | `P3.M_new_rows.ktvic_resnetlstm.BLEU-1.distance` | 0.037529502086947275 | 1f56a5ce | REGISTERED PREDICTION, DEVELOPMENT DATA (M_new) |
| n140 | 27.5 | FEID.json | `P3.M_new_rows.ktvic_resnetlstm.METEOR.printed` | "27.5" | 1f56a5ce | DESCRIPTIVE (value printed in a public source) |
| n141 | 27.5207 | FEID.json | `P3.M_new_rows.ktvic_resnetlstm.METEOR.rstar` | 27.520659917897234 | 1f56a5ce | REGISTERED PREDICTION, DEVELOPMENT DATA (M_new) |
| n142 | 0.0207 | FEID.json | `P3.M_new_rows.ktvic_resnetlstm.METEOR.distance` | 0.02065991789723398 | 1f56a5ce | REGISTERED PREDICTION, DEVELOPMENT DATA (M_new) |
| n143 | 42.3 | FEID.json | `P3.M_new_rows.ktvic_resnetlstm.ROUGE-L.printed` | "42.3" | 1f56a5ce | DESCRIPTIVE (value printed in a public source) |
| n144 | 42.2898 | FEID.json | `P3.M_new_rows.ktvic_resnetlstm.ROUGE-L.rstar` | 42.28984731645076 | 1f56a5ce | REGISTERED PREDICTION, DEVELOPMENT DATA (M_new) |
| n145 | 0.0102 | FEID.json | `P3.M_new_rows.ktvic_resnetlstm.ROUGE-L.distance` | 0.010152683549236485 | 1f56a5ce | REGISTERED PREDICTION, DEVELOPMENT DATA (M_new) |
| n146 | 56.1 | FEID.json | `P3.M_new_rows.ktvic_vittrans.BLEU-1.printed` | "56.1" | 1f56a5ce | DESCRIPTIVE (value printed in a public source) |
| n147 | 56.1162 | FEID.json | `P3.M_new_rows.ktvic_vittrans.BLEU-1.rstar` | 56.11621876456202 | 1f56a5ce | REGISTERED PREDICTION, DEVELOPMENT DATA (M_new) |
| n148 | 0.0162 | FEID.json | `P3.M_new_rows.ktvic_vittrans.BLEU-1.distance` | 0.016218764562019317 | 1f56a5ce | REGISTERED PREDICTION, DEVELOPMENT DATA (M_new) |
| n149 | 30.1 | FEID.json | `P3.M_new_rows.ktvic_vittrans.METEOR.printed` | "30.1" | 1f56a5ce | DESCRIPTIVE (value printed in a public source) |
| n150 | 30.1500 | FEID.json | `P3.M_new_rows.ktvic_vittrans.METEOR.rstar` | 30.1499830285999 | 1f56a5ce | REGISTERED PREDICTION, DEVELOPMENT DATA (M_new) |
| n151 | 0.0500 | FEID.json | `P3.M_new_rows.ktvic_vittrans.METEOR.distance` | 0.049983028599900337 | 1f56a5ce | REGISTERED PREDICTION, DEVELOPMENT DATA (M_new) |
| n152 | 44.7 | FEID.json | `P3.M_new_rows.ktvic_vittrans.ROUGE-L.printed` | "44.7" | 1f56a5ce | DESCRIPTIVE (value printed in a public source) |
| n153 | 44.6944 | FEID.json | `P3.M_new_rows.ktvic_vittrans.ROUGE-L.rstar` | 44.69437809001194 | 1f56a5ce | REGISTERED PREDICTION, DEVELOPMENT DATA (M_new) |
| n154 | 0.0056 | FEID.json | `P3.M_new_rows.ktvic_vittrans.ROUGE-L.distance` | 0.005621909988064999 | 1f56a5ce | REGISTERED PREDICTION, DEVELOPMENT DATA (M_new) |
| n155 | 15.5 | FEID.json | `P3.cider_bleu4_POST_HOC.ktvic_resnetlstm.BLEU-4.printed` | "15.5" | 1f56a5ce | DESCRIPTIVE (value printed in a public source) |
| n156 | 15.4684 | FEID.json | `P3.cider_bleu4_POST_HOC.ktvic_resnetlstm.BLEU-4.rstar` | 15.468443151721303 | 1f56a5ce | POST HOC |
| n157 | 0.0316 | FEID.json | `P3.cider_bleu4_POST_HOC.ktvic_resnetlstm.BLEU-4.distance` | 0.0315568482786972 | 1f56a5ce | POST HOC |
| n158 | 21.8 | FEID.json | `P3.cider_bleu4_POST_HOC.ktvic_resnetlstm.CIDEr-D.printed` | "21.8" | 1f56a5ce | DESCRIPTIVE (value printed in a public source) |
| n159 | 21.7899 | FEID.json | `P3.cider_bleu4_POST_HOC.ktvic_resnetlstm.CIDEr-D.rstar` | 21.789915485782338 | 1f56a5ce | POST HOC |
| n160 | 0.0101 | FEID.json | `P3.cider_bleu4_POST_HOC.ktvic_resnetlstm.CIDEr-D.distance` | 0.010084514217663099 | 1f56a5ce | POST HOC |
| n161 | 19.3 | FEID.json | `P3.cider_bleu4_POST_HOC.ktvic_vittrans.BLEU-4.printed` | "19.3" | 1f56a5ce | DESCRIPTIVE (value printed in a public source) |
| n162 | 19.3315 | FEID.json | `P3.cider_bleu4_POST_HOC.ktvic_vittrans.BLEU-4.rstar` | 19.33146749835939 | 1f56a5ce | POST HOC |
| n163 | 0.0315 | FEID.json | `P3.cider_bleu4_POST_HOC.ktvic_vittrans.BLEU-4.distance` | 0.03146749835939033 | 1f56a5ce | POST HOC |
| n164 | 36.8 | FEID.json | `P3.cider_bleu4_POST_HOC.ktvic_vittrans.CIDEr-D.printed` | "36.8" | 1f56a5ce | DESCRIPTIVE (value printed in a public source) |
| n165 | 36.7682 | FEID.json | `P3.cider_bleu4_POST_HOC.ktvic_vittrans.CIDEr-D.rstar` | 36.76816339336237 | 1f56a5ce | POST HOC |
| n166 | 0.0318 | FEID.json | `P3.cider_bleu4_POST_HOC.ktvic_vittrans.CIDEr-D.distance` | 0.031836606637625664 | 1f56a5ce | POST HOC |
| n167 | 0 | FEID.json | `derived: len(fe_id.ktvic_resnetlstm.P3b_matched_F_reproducing_CIDEr-D_POST_HOC)` | 0 | 1f56a5ce | POST HOC |
| n168 | 0 | FEID.json | `derived: len(fe_id.ktvic_vittrans.P3b_matched_F_reproducing_CIDEr-D_POST_HOC)` | 0 | 1f56a5ce | POST HOC |
| n169 | 23 | FEID.json | `fe_id.ktvic_resnetlstm.classes` | 23 | 1f56a5ce | DEVELOPMENT data; POST HOC for CIDEr-D/BLEU-4 |
| n170 | 3 | FEID.json | `derived: len(fe_id.ktvic_resnetlstm.reproducing)` | 3 | 1f56a5ce | DEVELOPMENT data; POST HOC for CIDEr-D/BLEU-4 |
| n171 | 23 | FEID.json | `fe_id.ktvic_vittrans.classes` | 23 | 1f56a5ce | DEVELOPMENT data; POST HOC for CIDEr-D/BLEU-4 |
| n172 | 2 | FEID.json | `derived: len(fe_id.ktvic_vittrans.reproducing)` | 2 | 1f56a5ce | DEVELOPMENT data; POST HOC for CIDEr-D/BLEU-4 |
| n173 | 24 | FEID.json | `derived: len(plants)` | 24 | 1f56a5ce | DEVELOPMENT; METHOD CHECK (§6.4, not a prediction) |
| n174 | 9 | FEID.json | `P4.IDENTIFIED` | 9 | 1f56a5ce | DEVELOPMENT; METHOD CHECK (§6.4, not a prediction) |
| n175 | 15 | FEID.json | `P4.AMBIGUOUS` | 15 | 1f56a5ce | DEVELOPMENT; METHOD CHECK (§6.4, not a prediction) |
| n176 | 0 | FEID.json | `P4.OUTSIDE` | 0 | 1f56a5ce | DEVELOPMENT; METHOD CHECK (§6.4, not a prediction) |
| n177 | 9 | FEID.json | `derived: count of non-null P4.margins` | 9 | 1f56a5ce | DEVELOPMENT; METHOD CHECK (§6.4, not a prediction) |
| n178 | 0.0752 | FEID.json | `derived: min of non-null P4.margins` | 0.0751623757154114 | 1f56a5ce | DEVELOPMENT; METHOD CHECK (§6.4, not a prediction) |
| n179 | 1.7429 | FEID.json | `derived: max of non-null P4.margins` | 1.7428894041424314 | 1f56a5ce | DEVELOPMENT; METHOD CHECK (§6.4, not a prediction) |
| n180 | 28 | FEID.json | `derived: min of plants[*].classes` | 28 | 1f56a5ce | DEVELOPMENT; METHOD CHECK (§6.4, not a prediction) |
| n181 | 128 | FEID.json | `derived: max of plants[*].classes` | 128 | 1f56a5ce | DEVELOPMENT; METHOD CHECK (§6.4, not a prediction) |
| n182 | 2790 | FAMILY.json | `F1.rdr.strings` | 2790 | 431d92a4 | DESCRIPTIVE |
| n183 | 0 | FAMILY.json | `F1.rdr.failed` | 0 | 431d92a4 | DESCRIPTIVE |
| n184 | 2790 | FAMILY.json | `F1.pyvi.strings` | 2790 | 431d92a4 | DESCRIPTIVE |
| n185 | 0 | FAMILY.json | `F1.pyvi.failed` | 0 | 431d92a4 | DESCRIPTIVE |
| n186 | 2790 | FAMILY.json | `F1.uts.strings` | 2790 | 431d92a4 | DESCRIPTIVE |
| n187 | 0 | FAMILY.json | `F1.uts.failed` | 0 | 431d92a4 | DESCRIPTIVE |
| n188 | 9 | FAMILY.json | `derived: count of F3.rdr[*].equal` | 9 | 431d92a4 | DESCRIPTIVE |
| n189 | 0 | FAMILY.json | `derived: count of F3.pyvi[*].equal` | 0 | 431d92a4 | DESCRIPTIVE |
| n190 | 9 | FAMILY.json | `derived: count of F3.uts[*].equal` | 9 | 431d92a4 | DESCRIPTIVE |
| n191 | 67 | FAMILY.json | `derived: len(G_repro)` | 67 | 431d92a4 | DEVELOPMENT |
| n192 | 0.0016 | FAMILY.json | `derived: max of G_repro[*].abs_diff` | 0.0015735977053967787 | 431d92a4 | DEVELOPMENT |
| n193 | 6 | FAMILY.json | `derived: len(no_committed_score)` | 6 | 431d92a4 | DESCRIPTIVE |
| n194 | 558 | FAMILY.json | `n_images` | 558 | 431d92a4 | DESCRIPTIVE |
| n195 | 2790 | FAMILY.json | `n_refs` | 2790 | 431d92a4 | DESCRIPTIVE |
| n196 | 578 | GATE2.json | `files.G1/X4a.rows` | 578 | 26110b5f | DESCRIPTIVE |
| n197 | 1.0000 | GATE2.json | `files.G1/X4a.coverage` | 1.0 | 26110b5f | DESCRIPTIVE |
| n198 | 0.0000 | GATE2.json | `files.G1/X4a.unknown` | 0.0 | 26110b5f | DESCRIPTIVE |
| n199 | 0.0000 | GATE2.json | `files.G1/X4a.dup` | 0.0 | 26110b5f | DESCRIPTIVE |
| n200 | 0.0000 | GATE2.json | `files.G1/X4a.empty` | 0.0 | 26110b5f | DESCRIPTIVE |
| n201 | 0.0000 | GATE2.json | `files.G1/X4a.refcopy` | 0.0 | 26110b5f | DESCRIPTIVE |
| n202 | 1.0000 | GATE2.json | `files.G1/X4a.diacritic` | 1.0 | 26110b5f | DESCRIPTIVE |
| n203 | 578 | GATE2.json | `files.G1/X4b.rows` | 578 | 26110b5f | DESCRIPTIVE |
| n204 | 1.0000 | GATE2.json | `files.G1/X4b.coverage` | 1.0 | 26110b5f | DESCRIPTIVE |
| n205 | 0.0000 | GATE2.json | `files.G1/X4b.unknown` | 0.0 | 26110b5f | DESCRIPTIVE |
| n206 | 0.0000 | GATE2.json | `files.G1/X4b.dup` | 0.0 | 26110b5f | DESCRIPTIVE |
| n207 | 0.0000 | GATE2.json | `files.G1/X4b.empty` | 0.0 | 26110b5f | DESCRIPTIVE |
| n208 | 0.0000 | GATE2.json | `files.G1/X4b.refcopy` | 0.0 | 26110b5f | DESCRIPTIVE |
| n209 | 1.0000 | GATE2.json | `files.G1/X4b.diacritic` | 1.0 | 26110b5f | DESCRIPTIVE |
| n210 | 578 | GATE2.json | `files.G1/X4c.rows` | 578 | 26110b5f | DESCRIPTIVE |
| n211 | 1.0000 | GATE2.json | `files.G1/X4c.coverage` | 1.0 | 26110b5f | DESCRIPTIVE |
| n212 | 0.0000 | GATE2.json | `files.G1/X4c.unknown` | 0.0 | 26110b5f | DESCRIPTIVE |
| n213 | 0.0000 | GATE2.json | `files.G1/X4c.dup` | 0.0 | 26110b5f | DESCRIPTIVE |
| n214 | 0.0000 | GATE2.json | `files.G1/X4c.empty` | 0.0 | 26110b5f | DESCRIPTIVE |
| n215 | 0.0000 | GATE2.json | `files.G1/X4c.refcopy` | 0.0 | 26110b5f | DESCRIPTIVE |
| n216 | 1.0000 | GATE2.json | `files.G1/X4c.diacritic` | 1.0 | 26110b5f | DESCRIPTIVE |
| n217 | 578 | GATE2.json | `files.G1/X4d.rows` | 578 | 26110b5f | DESCRIPTIVE |
| n218 | 1.0000 | GATE2.json | `files.G1/X4d.coverage` | 1.0 | 26110b5f | DESCRIPTIVE |
| n219 | 0.0000 | GATE2.json | `files.G1/X4d.unknown` | 0.0 | 26110b5f | DESCRIPTIVE |
| n220 | 0.0000 | GATE2.json | `files.G1/X4d.dup` | 0.0 | 26110b5f | DESCRIPTIVE |
| n221 | 0.0000 | GATE2.json | `files.G1/X4d.empty` | 0.0 | 26110b5f | DESCRIPTIVE |
| n222 | 0.0000 | GATE2.json | `files.G1/X4d.refcopy` | 0.0 | 26110b5f | DESCRIPTIVE |
| n223 | 1.0000 | GATE2.json | `files.G1/X4d.diacritic` | 1.0 | 26110b5f | DESCRIPTIVE |
| n224 | 578 | GATE2.json | `files.G1/X4e.rows` | 578 | 26110b5f | DESCRIPTIVE |
| n225 | 1.0000 | GATE2.json | `files.G1/X4e.coverage` | 1.0 | 26110b5f | DESCRIPTIVE |
| n226 | 0.0000 | GATE2.json | `files.G1/X4e.unknown` | 0.0 | 26110b5f | DESCRIPTIVE |
| n227 | 0.0000 | GATE2.json | `files.G1/X4e.dup` | 0.0 | 26110b5f | DESCRIPTIVE |
| n228 | 0.0000 | GATE2.json | `files.G1/X4e.empty` | 0.0 | 26110b5f | DESCRIPTIVE |
| n229 | 0.0000 | GATE2.json | `files.G1/X4e.refcopy` | 0.0 | 26110b5f | DESCRIPTIVE |
| n230 | 1.0000 | GATE2.json | `files.G1/X4e.diacritic` | 1.0 | 26110b5f | DESCRIPTIVE |
| n231 | 279 | GATE2.json | `files.G2/G2_cnn_lstm.rows` | 279 | 26110b5f | DESCRIPTIVE |
| n232 | 1.0000 | GATE2.json | `files.G2/G2_cnn_lstm.coverage` | 1.0 | 26110b5f | DESCRIPTIVE |
| n233 | 0.0000 | GATE2.json | `files.G2/G2_cnn_lstm.unknown` | 0.0 | 26110b5f | DESCRIPTIVE |
| n234 | 0.0000 | GATE2.json | `files.G2/G2_cnn_lstm.dup` | 0.0 | 26110b5f | DESCRIPTIVE |
| n235 | 0.0000 | GATE2.json | `files.G2/G2_cnn_lstm.empty` | 0.0 | 26110b5f | DESCRIPTIVE |
| n236 | 0.0000 | GATE2.json | `files.G2/G2_cnn_lstm.refcopy` | 0.0 | 26110b5f | DESCRIPTIVE |
| n237 | 1.0000 | GATE2.json | `files.G2/G2_cnn_lstm.diacritic` | 1.0 | 26110b5f | DESCRIPTIVE |
| n238 | 279 | GATE2.json | `files.G2/G2_cnn_lstm_attention.rows` | 279 | 26110b5f | DESCRIPTIVE |
| n239 | 1.0000 | GATE2.json | `files.G2/G2_cnn_lstm_attention.coverage` | 1.0 | 26110b5f | DESCRIPTIVE |
| n240 | 0.0000 | GATE2.json | `files.G2/G2_cnn_lstm_attention.unknown` | 0.0 | 26110b5f | DESCRIPTIVE |
| n241 | 0.0000 | GATE2.json | `files.G2/G2_cnn_lstm_attention.dup` | 0.0 | 26110b5f | DESCRIPTIVE |
| n242 | 0.0000 | GATE2.json | `files.G2/G2_cnn_lstm_attention.empty` | 0.0 | 26110b5f | DESCRIPTIVE |
| n243 | 0.0000 | GATE2.json | `files.G2/G2_cnn_lstm_attention.refcopy` | 0.0 | 26110b5f | DESCRIPTIVE |
| n244 | 1.0000 | GATE2.json | `files.G2/G2_cnn_lstm_attention.diacritic` | 1.0 | 26110b5f | DESCRIPTIVE |
| n245 | 279 | GATE2.json | `files.G2/G2_cnn_t5.rows` | 279 | 26110b5f | DESCRIPTIVE |
| n246 | 1.0000 | GATE2.json | `files.G2/G2_cnn_t5.coverage` | 1.0 | 26110b5f | DESCRIPTIVE |
| n247 | 0.0000 | GATE2.json | `files.G2/G2_cnn_t5.unknown` | 0.0 | 26110b5f | DESCRIPTIVE |
| n248 | 0.0000 | GATE2.json | `files.G2/G2_cnn_t5.dup` | 0.0 | 26110b5f | DESCRIPTIVE |
| n249 | 0.0000 | GATE2.json | `files.G2/G2_cnn_t5.empty` | 0.0 | 26110b5f | DESCRIPTIVE |
| n250 | 0.0000 | GATE2.json | `files.G2/G2_cnn_t5.refcopy` | 0.0 | 26110b5f | DESCRIPTIVE |
| n251 | 1.0000 | GATE2.json | `files.G2/G2_cnn_t5.diacritic` | 1.0 | 26110b5f | DESCRIPTIVE |
| n252 | 279 | GATE2.json | `files.G2/G2_qwen2.rows` | 279 | 26110b5f | DESCRIPTIVE |
| n253 | 1.0000 | GATE2.json | `files.G2/G2_qwen2.coverage` | 1.0 | 26110b5f | DESCRIPTIVE |
| n254 | 0.0000 | GATE2.json | `files.G2/G2_qwen2.unknown` | 0.0 | 26110b5f | DESCRIPTIVE |
| n255 | 0.0000 | GATE2.json | `files.G2/G2_qwen2.dup` | 0.0 | 26110b5f | DESCRIPTIVE |
| n256 | 0.0000 | GATE2.json | `files.G2/G2_qwen2.empty` | 0.0 | 26110b5f | DESCRIPTIVE |
| n257 | 0.0000 | GATE2.json | `files.G2/G2_qwen2.refcopy` | 0.0 | 26110b5f | DESCRIPTIVE |
| n258 | 1.0000 | GATE2.json | `files.G2/G2_qwen2.diacritic` | 1.0 | 26110b5f | DESCRIPTIVE |
| n259 | 279 | GATE2.json | `files.G2/G2_vit_t5.rows` | 279 | 26110b5f | DESCRIPTIVE |
| n260 | 1.0000 | GATE2.json | `files.G2/G2_vit_t5.coverage` | 1.0 | 26110b5f | DESCRIPTIVE |
| n261 | 0.0000 | GATE2.json | `files.G2/G2_vit_t5.unknown` | 0.0 | 26110b5f | DESCRIPTIVE |
| n262 | 0.0000 | GATE2.json | `files.G2/G2_vit_t5.dup` | 0.0 | 26110b5f | DESCRIPTIVE |
| n263 | 0.0000 | GATE2.json | `files.G2/G2_vit_t5.empty` | 0.0 | 26110b5f | DESCRIPTIVE |
| n264 | 0.0000 | GATE2.json | `files.G2/G2_vit_t5.refcopy` | 0.0 | 26110b5f | DESCRIPTIVE |
| n265 | 1.0000 | GATE2.json | `files.G2/G2_vit_t5.diacritic` | 1.0 | 26110b5f | DESCRIPTIVE |
| n266 | 924 | GATE2.json | `files.G3/X3_detect.rows` | 924 | 26110b5f | DESCRIPTIVE |
| n267 | 1.0000 | GATE2.json | `files.G3/X3_detect.coverage` | 1.0 | 26110b5f | DESCRIPTIVE |
| n268 | 0.0000 | GATE2.json | `files.G3/X3_detect.unknown` | 0.0 | 26110b5f | DESCRIPTIVE |
| n269 | 0.0000 | GATE2.json | `files.G3/X3_detect.dup` | 0.0 | 26110b5f | DESCRIPTIVE |
| n270 | 0.0000 | GATE2.json | `files.G3/X3_detect.empty` | 0.0 | 26110b5f | DESCRIPTIVE |
| n271 | 0.0087 | GATE2.json | `files.G3/X3_detect.refcopy` | 0.008658008658008658 | 26110b5f | DESCRIPTIVE |
| n272 | 1.0000 | GATE2.json | `files.G3/X3_detect.diacritic` | 1.0 | 26110b5f | DESCRIPTIVE |
| n273 | 924 | GATE2.json | `files.G3/X3_original.rows` | 924 | 26110b5f | DESCRIPTIVE |
| n274 | 1.0000 | GATE2.json | `files.G3/X3_original.coverage` | 1.0 | 26110b5f | DESCRIPTIVE |
| n275 | 0.0000 | GATE2.json | `files.G3/X3_original.unknown` | 0.0 | 26110b5f | DESCRIPTIVE |
| n276 | 0.0000 | GATE2.json | `files.G3/X3_original.dup` | 0.0 | 26110b5f | DESCRIPTIVE |
| n277 | 0.0000 | GATE2.json | `files.G3/X3_original.empty` | 0.0 | 26110b5f | DESCRIPTIVE |
| n278 | 0.0032 | GATE2.json | `files.G3/X3_original.refcopy` | 0.003246753246753247 | 26110b5f | DESCRIPTIVE |
| n279 | 1.0000 | GATE2.json | `files.G3/X3_original.diacritic` | 1.0 | 26110b5f | DESCRIPTIVE |
| n280 | 100 | GATE2.json | `files.G4/X3_flickr_detect.rows` | 100 | 26110b5f | DESCRIPTIVE |
| n281 | 1.0000 | GATE2.json | `files.G4/X3_flickr_detect.coverage` | 1.0 | 26110b5f | DESCRIPTIVE |
| n282 | 0.0000 | GATE2.json | `files.G4/X3_flickr_detect.unknown` | 0.0 | 26110b5f | DESCRIPTIVE |
| n283 | 0.0000 | GATE2.json | `files.G4/X3_flickr_detect.dup` | 0.0 | 26110b5f | DESCRIPTIVE |
| n284 | 0.0000 | GATE2.json | `files.G4/X3_flickr_detect.empty` | 0.0 | 26110b5f | DESCRIPTIVE |
| n285 | 0.0000 | GATE2.json | `files.G4/X3_flickr_detect.refcopy` | 0.0 | 26110b5f | DESCRIPTIVE |
| n286 | 1.0000 | GATE2.json | `files.G4/X3_flickr_detect.diacritic` | 1.0 | 26110b5f | DESCRIPTIVE |
| n287 | 100 | GATE2.json | `files.G4/X3_flickr_original.rows` | 100 | 26110b5f | DESCRIPTIVE |
| n288 | 1.0000 | GATE2.json | `files.G4/X3_flickr_original.coverage` | 1.0 | 26110b5f | DESCRIPTIVE |
| n289 | 0.0000 | GATE2.json | `files.G4/X3_flickr_original.unknown` | 0.0 | 26110b5f | DESCRIPTIVE |
| n290 | 0.0000 | GATE2.json | `files.G4/X3_flickr_original.dup` | 0.0 | 26110b5f | DESCRIPTIVE |
| n291 | 0.0000 | GATE2.json | `files.G4/X3_flickr_original.empty` | 0.0 | 26110b5f | DESCRIPTIVE |
| n292 | 0.0000 | GATE2.json | `files.G4/X3_flickr_original.refcopy` | 0.0 | 26110b5f | DESCRIPTIVE |
| n293 | 1.0000 | GATE2.json | `files.G4/X3_flickr_original.diacritic` | 1.0 | 26110b5f | DESCRIPTIVE |
| n294 | 558 | GATE2.json | `files.G6/ktvic_resnetlstm.rows` | 558 | 26110b5f | DESCRIPTIVE |
| n295 | 1.0000 | GATE2.json | `files.G6/ktvic_resnetlstm.coverage` | 1.0 | 26110b5f | DESCRIPTIVE |
| n296 | 0.0000 | GATE2.json | `files.G6/ktvic_resnetlstm.unknown` | 0.0 | 26110b5f | DESCRIPTIVE |
| n297 | 0.0000 | GATE2.json | `files.G6/ktvic_resnetlstm.dup` | 0.0 | 26110b5f | DESCRIPTIVE |
| n298 | 0.0000 | GATE2.json | `files.G6/ktvic_resnetlstm.empty` | 0.0 | 26110b5f | DESCRIPTIVE |
| n299 | 0.0036 | GATE2.json | `files.G6/ktvic_resnetlstm.refcopy` | 0.0035842293906810036 | 26110b5f | DESCRIPTIVE |
| n300 | 1.0000 | GATE2.json | `files.G6/ktvic_resnetlstm.diacritic` | 1.0 | 26110b5f | DESCRIPTIVE |
| n301 | 558 | GATE2.json | `files.G6/ktvic_vittrans.rows` | 558 | 26110b5f | DESCRIPTIVE |
| n302 | 1.0000 | GATE2.json | `files.G6/ktvic_vittrans.coverage` | 1.0 | 26110b5f | DESCRIPTIVE |
| n303 | 0.0000 | GATE2.json | `files.G6/ktvic_vittrans.unknown` | 0.0 | 26110b5f | DESCRIPTIVE |
| n304 | 0.0000 | GATE2.json | `files.G6/ktvic_vittrans.dup` | 0.0 | 26110b5f | DESCRIPTIVE |
| n305 | 0.0000 | GATE2.json | `files.G6/ktvic_vittrans.empty` | 0.0 | 26110b5f | DESCRIPTIVE |
| n306 | 0.0108 | GATE2.json | `files.G6/ktvic_vittrans.refcopy` | 0.010752688172043012 | 26110b5f | DESCRIPTIVE |
| n307 | 1.0000 | GATE2.json | `files.G6/ktvic_vittrans.diacritic` | 1.0 | 26110b5f | DESCRIPTIVE |
| n308 | 3 | GATE2.json | `derived: count of files with admitted = false` | 3 | 26110b5f | DESCRIPTIVE |
| n309 | 19 | GATE2.json | `derived: len(files)` | 19 | 26110b5f | DESCRIPTIVE |
| n310 | 10 | GATE2.json | `derived: comparisons with group G1` | 10 | 26110b5f | DESCRIPTIVE |
| n311 | 10 | GATE2.json | `derived: formed comparisons with group G1` | 10 | 26110b5f | DESCRIPTIVE |
| n312 | 578 | GATE2.json | `derived: comparisons[i].n for group G1` | 578 | 26110b5f | DESCRIPTIVE |
| n313 | 10 | GATE2.json | `derived: comparisons with group G2` | 10 | 26110b5f | DESCRIPTIVE |
| n314 | 10 | GATE2.json | `derived: formed comparisons with group G2` | 10 | 26110b5f | DESCRIPTIVE |
| n315 | 279 | GATE2.json | `derived: comparisons[i].n for group G2` | 279 | 26110b5f | DESCRIPTIVE |
| n316 | 1 | GATE2.json | `derived: comparisons with group G3` | 1 | 26110b5f | DESCRIPTIVE |
| n317 | 1 | GATE2.json | `derived: formed comparisons with group G3` | 1 | 26110b5f | DESCRIPTIVE |
| n318 | 924 | GATE2.json | `derived: comparisons[i].n for group G3` | 924 | 26110b5f | DESCRIPTIVE |
| n319 | 1 | GATE2.json | `derived: comparisons with group G4` | 1 | 26110b5f | DESCRIPTIVE |
| n320 | 1 | GATE2.json | `derived: formed comparisons with group G4` | 1 | 26110b5f | DESCRIPTIVE |
| n321 | 100 | GATE2.json | `derived: comparisons[i].n for group G4` | 100 | 26110b5f | DESCRIPTIVE |
| n322 | 22 | GATE2.json | `derived: len(comparisons)` | 22 | 26110b5f | DESCRIPTIVE |
| n323 | 73 | SYSTEMS.tsv | `derived: rows with role = own` | 73 | 30ac9555 | DESCRIPTIVE |
| n324 | 2 | SYSTEMS.tsv | `derived: rows with role = baseline` | 2 | 30ac9555 | DESCRIPTIVE |
| n325 | 26 | CENSUS.json | `families` | 26 | 2252167b | DESCRIPTIVE |
| n326 | 33 | CENSUS.json | `strata.short` | 33 | 2252167b | DESCRIPTIVE |
| n327 | 35 | CENSUS.json | `strata.detailed` | 35 | 2252167b | DESCRIPTIVE |
| n328 | 5 | CENSUS.json | `strata.two` | 5 | 2252167b | DESCRIPTIVE |
| n329 | 1101 | CENSUS.json | `D_size` | 1101 | 2252167b | DESCRIPTIVE |
| n330 | 67 | CENSUS.json | `derived: segmenter_census keys not under b2_external/` | 67 | 2252167b | DESCRIPTIVE |
| n331 | 1 | CENSUS.json | `derived: len(b2_score_sha256)` | 1 | 2252167b | DESCRIPTIVE |
| n332 | 67 | CENSUS.json | `derived: own files whose segmenter list holds rdrsegmenter` | 67 | 2252167b | DESCRIPTIVE |
| n333 | 22 | CENSUS.json | `derived: own files whose segmenter list holds whitespace` | 22 | 2252167b | DESCRIPTIVE |
| n334 | 0 | CENSUS.json | `derived: len(underthesea_hits)` | 0 | 2252167b | DESCRIPTIVE |
| n335 | 0 | CENSUS.json | `derived: len(character_unit_hits_logged_only)` | 0 | 2252167b | DESCRIPTIVE |
| n336 | 0.8012 | RESULT.json | `secondary.FE_PRED_AUC` | 0.801158889905459 | 25614b46 | DESCRIPTIVE (D ∪ FL) |
| n337 | 30 | RESULT.json | `derived: count of comparisons[i].changed_F` | 30 | 25614b46 | DESCRIPTIVE |
| n338 | 1093 | RESULT.json | `derived: count of comparisons[i] with changed_F false` | 1093 | 25614b46 | DESCRIPTIVE |
| n339 | 0.9546 | RESULT.json | `secondary.FE_PRED_AUC_f0_significant_EXTRA` | 0.9545851528384279 | 25614b46 | DESCRIPTIVE (code row; no registered label of its own) |
| n340 | 946 | RESULT.json + DEV.json + V.json | `derived: comparisons significant under f0 (D and FL)` | 946 | 25614b46 + 88ff39aa + 1f011538 | DESCRIPTIVE |
| n341 | 1123 | RESULT.json | `secondary.BLEU-4_over_F.comparisons` | 1123 | 25614b46 | DESCRIPTIVE |
| n342 | 862 | RESULT.json | `secondary.BLEU-4_over_F.CERTIFIED` | 862 | 25614b46 | DESCRIPTIVE |
| n343 | 120 | RESULT.json | `secondary.BLEU-4_over_F.FRAGILE` | 120 | 25614b46 | DESCRIPTIVE |
| n344 | 20 | RESULT.json | `secondary.BLEU-4_over_F.REVERSED` | 20 | 25614b46 | DESCRIPTIVE |
| n345 | 141 | RESULT.json | `secondary.BLEU-4_over_F.NULL-STABLE` | 141 | 25614b46 | DESCRIPTIVE |
| n346 | 909 | RESULT.json | `secondary.BLEU-4_over_F.significant_under_f0` | 909 | 25614b46 | DESCRIPTIVE |
| n347 | 47 | RESULT.json | `secondary.BLEU-4_over_F.CHANGED` | 47 | 25614b46 | DESCRIPTIVE |
| n348 | 0.0517 | RESULT.json | `secondary.BLEU-4_over_F.CHANGED_share` | 0.0517051705170517 | 25614b46 | DESCRIPTIVE |
| n349 | 118 | RESULT.json | `secondary.BLEU-4_over_F.point_flips` | 118 | 25614b46 | DESCRIPTIVE |
| n350 | 1123 | RESULT.json | `secondary.ROUGE-L_over_F.comparisons` | 1123 | 25614b46 | DESCRIPTIVE |
| n351 | 891 | RESULT.json | `secondary.ROUGE-L_over_F.CERTIFIED` | 891 | 25614b46 | DESCRIPTIVE |
| n352 | 122 | RESULT.json | `secondary.ROUGE-L_over_F.FRAGILE` | 122 | 25614b46 | DESCRIPTIVE |
| n353 | 16 | RESULT.json | `secondary.ROUGE-L_over_F.REVERSED` | 16 | 25614b46 | DESCRIPTIVE |
| n354 | 110 | RESULT.json | `secondary.ROUGE-L_over_F.NULL-STABLE` | 110 | 25614b46 | DESCRIPTIVE |
| n355 | 970 | RESULT.json | `secondary.ROUGE-L_over_F.significant_under_f0` | 970 | 25614b46 | DESCRIPTIVE |
| n356 | 79 | RESULT.json | `secondary.ROUGE-L_over_F.CHANGED` | 79 | 25614b46 | DESCRIPTIVE |
| n357 | 0.0814 | RESULT.json | `secondary.ROUGE-L_over_F.CHANGED_share` | 0.08144329896907217 | 25614b46 | DESCRIPTIVE |
| n358 | 94 | RESULT.json | `secondary.ROUGE-L_over_F.point_flips` | 94 | 25614b46 | DESCRIPTIVE |
| n359 | 1123 | RESULT.json | `secondary.F_without_ck.comparisons` | 1123 | 25614b46 | DESCRIPTIVE |
| n360 | 919 | RESULT.json | `secondary.F_without_ck.CERTIFIED` | 919 | 25614b46 | DESCRIPTIVE |
| n361 | 63 | RESULT.json | `secondary.F_without_ck.FRAGILE` | 63 | 25614b46 | DESCRIPTIVE |
| n362 | 0 | RESULT.json | `secondary.F_without_ck.REVERSED` | 0 | 25614b46 | DESCRIPTIVE |
| n363 | 141 | RESULT.json | `secondary.F_without_ck.NULL-STABLE` | 141 | 25614b46 | DESCRIPTIVE |
| n364 | 946 | RESULT.json | `secondary.F_without_ck.significant_under_f0` | 946 | 25614b46 | DESCRIPTIVE |
| n365 | 27 | RESULT.json | `secondary.F_without_ck.CHANGED` | 27 | 25614b46 | DESCRIPTIVE |
| n366 | 0.0285 | RESULT.json | `secondary.F_without_ck.CHANGED_share` | 0.02854122621564482 | 25614b46 | DESCRIPTIVE |
| n367 | 51 | RESULT.json | `secondary.F_without_ck.point_flips` | 51 | 25614b46 | DESCRIPTIVE |
| n368 | 1123 | RESULT.json | `secondary.F_with_chr_DESCRIPTIVE.comparisons` | 1123 | 25614b46 | DESCRIPTIVE |
| n369 | 893 | RESULT.json | `secondary.F_with_chr_DESCRIPTIVE.CERTIFIED` | 893 | 25614b46 | DESCRIPTIVE |
| n370 | 119 | RESULT.json | `secondary.F_with_chr_DESCRIPTIVE.FRAGILE` | 119 | 25614b46 | DESCRIPTIVE |
| n371 | 4 | RESULT.json | `secondary.F_with_chr_DESCRIPTIVE.REVERSED` | 4 | 25614b46 | DESCRIPTIVE |
| n372 | 111 | RESULT.json | `secondary.F_with_chr_DESCRIPTIVE.NULL-STABLE` | 111 | 25614b46 | DESCRIPTIVE |
| n373 | 946 | RESULT.json | `secondary.F_with_chr_DESCRIPTIVE.significant_under_f0` | 946 | 25614b46 | DESCRIPTIVE |
| n374 | 53 | RESULT.json | `secondary.F_with_chr_DESCRIPTIVE.CHANGED` | 53 | 25614b46 | DESCRIPTIVE |
| n375 | 0.0560 | RESULT.json | `secondary.F_with_chr_DESCRIPTIVE.CHANGED_share` | 0.056025369978858354 | 25614b46 | DESCRIPTIVE |
| n376 | 104 | RESULT.json | `secondary.F_with_chr_DESCRIPTIVE.point_flips` | 104 | 25614b46 | DESCRIPTIVE |
| n377 | 1123 | RESULT.json | `secondary.F_without_pk.comparisons` | 1123 | 25614b46 | DESCRIPTIVE |
| n378 | 925 | RESULT.json | `secondary.F_without_pk.CERTIFIED` | 925 | 25614b46 | DESCRIPTIVE |
| n379 | 53 | RESULT.json | `secondary.F_without_pk.FRAGILE` | 53 | 25614b46 | DESCRIPTIVE |
| n380 | 0 | RESULT.json | `secondary.F_without_pk.REVERSED` | 0 | 25614b46 | DESCRIPTIVE |
| n381 | 145 | RESULT.json | `secondary.F_without_pk.NULL-STABLE` | 145 | 25614b46 | DESCRIPTIVE |
| n382 | 0 | RESULT.json | `secondary.F_without_pk.significant_under_f0` | 0 | 25614b46 | DESCRIPTIVE |
| n383 | 0 | RESULT.json | `secondary.F_without_pk.CHANGED` | 0 | 25614b46 | DESCRIPTIVE |
| n384 | null | RESULT.json | `secondary.F_without_pk.CHANGED_share` | null | 25614b46 | DESCRIPTIVE |
| n385 | 63 | RESULT.json | `secondary.F_without_pk.point_flips` | 63 | 25614b46 | DESCRIPTIVE |
| n386 | 1123 | RESULT.json | `counts.F_held_HELD-OUT_FRONT_END.comparisons` | 1123 | 25614b46 | HELD-OUT FRONT END |
| n387 | 937 | RESULT.json | `counts.F_held_HELD-OUT_FRONT_END.CERTIFIED` | 937 | 25614b46 | HELD-OUT FRONT END |
| n388 | 32 | RESULT.json | `counts.F_held_HELD-OUT_FRONT_END.FRAGILE` | 32 | 25614b46 | HELD-OUT FRONT END |
| n389 | 0 | RESULT.json | `counts.F_held_HELD-OUT_FRONT_END.REVERSED` | 0 | 25614b46 | HELD-OUT FRONT END |
| n390 | 154 | RESULT.json | `counts.F_held_HELD-OUT_FRONT_END.NULL-STABLE` | 154 | 25614b46 | HELD-OUT FRONT END |
| n391 | 40 | RESULT.json | `counts.F_held_HELD-OUT_FRONT_END.point_flips` | 40 | 25614b46 | HELD-OUT FRONT END |
| n392 | 18 | FEID.json | `derived: len(fe_id.ktvic_resnetlstm.reproducing[0])` | 18 | 1f56a5ce | DEVELOPMENT data; POST HOC for CIDEr-D/BLEU-4 |
| n393 | 0.0375 | FEID.json | `fe_id.ktvic_resnetlstm.nearest_distance` | 0.037529502086947275 | 1f56a5ce | DEVELOPMENT data |
| n394 | 6 | FEID.json | `derived: len(fe_id.ktvic_resnetlstm.reproducing[1])` | 6 | 1f56a5ce | DEVELOPMENT data; POST HOC for CIDEr-D/BLEU-4 |
| n395 | 1 | FEID.json | `derived: len(fe_id.ktvic_resnetlstm.reproducing[2])` | 1 | 1f56a5ce | DEVELOPMENT data; POST HOC for CIDEr-D/BLEU-4 |
| n396 | 18 | FEID.json | `derived: len(fe_id.ktvic_vittrans.reproducing[0])` | 18 | 1f56a5ce | DEVELOPMENT data; POST HOC for CIDEr-D/BLEU-4 |
| n397 | 0.0438 | FEID.json | `fe_id.ktvic_vittrans.nearest_distance` | 0.04382275678143799 | 1f56a5ce | DEVELOPMENT data |
| n398 | 1 | FEID.json | `derived: len(fe_id.ktvic_vittrans.reproducing[1])` | 1 | 1f56a5ce | DEVELOPMENT data; POST HOC for CIDEr-D/BLEU-4 |
| n399 | 271 | FEID.json | `pool` | 271 | 1f56a5ce | DESCRIPTIVE |
| n400 | 6 | FEID.json | `derived: len(printed_comparisons.pairs)` | 6 | 1f56a5ce | DESCRIPTIVE |
| n401 | 1 | FEID.json | `derived: pairs with kind re-scorable` | 1 | 1f56a5ce | DESCRIPTIVE |
| n402 | 2 | FEID.json | `derived: pairs with kind one-sided` | 2 | 1f56a5ce | DESCRIPTIVE |
| n403 | 3 | FEID.json | `derived: pairs with kind neither` | 3 | 1f56a5ce | DESCRIPTIVE |
| n404 | 1 | FEID.json | `printed_comparisons.n_rescorable` | 1 | 1f56a5ce | DESCRIPTIVE |
| n405 | 0 | FEID.json | `printed_comparisons.order_changes_under_f0` | 0 | 1f56a5ce | DESCRIPTIVE |
| n406 | 0 | FEID.json | `printed_comparisons.not_certified_over_F` | 0 | 1f56a5ce | DESCRIPTIVE |
| n407 | -15.00 | FEID.json | `printed_comparisons.pairs.0.printed_gap` | -14.999999999999996 | 1f56a5ce | DESCRIPTIVE (difference of two printed values) |
| n408 | -24.02 | FEID.json | `printed_comparisons.pairs.0.f0_gap` | -24.021803977146778 | 1f56a5ce | DEVELOPMENT; POST HOC (O4) |
| n409 | -87.15 | FEID.json | `printed_comparisons.pairs.1.gap_released_f0_minus_other_printed` | -87.15370965143708 | 1f56a5ce | DEVELOPMENT; POST HOC (O4) |
| n410 | -63.13 | FEID.json | `printed_comparisons.pairs.2.gap_released_f0_minus_other_printed` | -63.131905674290294 | 1f56a5ce | DEVELOPMENT; POST HOC (O4) |
| n411 | 72 | RESULT.json | `P1_beside.with_chr_DESCRIPTIVE.N` | 72 | 25614b46 | DESCRIPTIVE |
| n412 | 48.85 | FEID.json | `derived: 136.0 + printed_comparisons.pairs[1].gap_released_f0_minus_other_printed (136.0 from registration l.260)` | 48.84629034856292 | 1f56a5ce | DEVELOPMENT; POST HOC (O4) |
| n413 | 72.87 | FEID.json | `derived: 136.0 + printed_comparisons.pairs[2].gap_released_f0_minus_other_printed (136.0 from registration l.260)` | 72.8680943257097 | 1f56a5ce | DEVELOPMENT; POST HOC (O4) |
| n414 | 16 | GATE2.json | `derived: count of files with admitted = true` | 16 | 26110b5f | DESCRIPTIVE |
| table of 22 first-look comparisons (section 2.2) | 22 rows | V.json + RESULT.json | `V.json::fl[i].{id, repo, n, classes}`; `RESULT.json::comparisons[i].{F, F_dev, changed_F}` | per row | 1f011538 + 25614b46 | FIRST SCORING OF RELEASED OUTPUTS; verdicts over F include the HELD-OUT FRONT END members |

Registered constants quoted in this note (not results):

| Constant | Value | Registration line |
|---|---|---|
| near-margin bound on z_min | 4 | l.269 |
| smallest N for a P1 verdict | 59 | l.269, l.273 |
| P1 bound on r | 0.05 | l.273 |
| NC bound on r_NC | 0.05 | l.277 |
| P2: smallest n_FL | 10 | l.283 |
| P2: smallest k_FL and share | 3 and 0.10 | l.283 |
| K-FL20 | 20 formed comparisons | l.362 |
| K-plant | 12 of 24 IDENTIFIED | l.298, l.367 |
| G-repro tolerance | 0.01 | l.339 |
| F1 failed-string share | 0.5% | l.142 |
| gate thresholds | 95%, 5%, 1%, 1%, 5%, 50%; overlap 95% | l.219-225 |
| reproduction tolerance | 0.5 × 10^(−d) + 1e-9 | l.235 |
| family sizes | 54, 18, 72, 271 | l.131-133, l.233 |
| KTVIC test size | 558 images, 2,790 references | l.184 |
| maximum FL comparisons | 32 | l.202 |
| printed value of the third KTVIC row | 136.0 | l.260 |
| K-print and K-time | 2026-11-15 12:00 and 2026-11-16 12:00 Vietnam time | l.365, l.369 |
| Clopper-Pearson method check (not a result) | upper bound for 0 breaks: 0.04951 at N = 59, 0.05034 at N = 58 | l.273; computed by this note |
| bootstrap | 10,000 draws, seed 20261112, two-sided 95% percentile interval | l.156 |

## Appendix A. The recomputation script

The full text of the script follows; sha256 of the script file `78d933df9e6e689ed06890fcf64275aefa1521a63eb1bec114bdc9a9b1fa83ac` (the text below plus one final newline). Run as `python3 -I recompute.py <b_work folder> <out.json>`. Standard library only. It reads the eight JSON files and SYSTEMS.tsv and writes one JSON file of recomputed values, from which the figures of this note were filled in by a second script. The second script is not shown. It reads the same files for the code's values, sets each status by comparing the recomputed value with the code's value, runs the record checks (stamps of `runs.log`, return codes, the hash chain of section 2.10), derives the two f0 values of sentence C-P3, and formats the tables and the table of section 8. The scratch copies of both scripts and of the JSON of recomputed values were kept outside the repository and deleted after the note was written, so that no figure lies outside this held note.

```python
#!/usr/bin/env python3
"""Read-only recomputation of the registered B-FECERT labels from the pinned output files.
Imports nothing from the study. Usage: python3 -I recompute.py <b_work dir> <out.json>
Rule lines refer to B_FECERT_PREREG_v1_1.md (sha256 736b7e6a...)."""
import csv
import json
import math
import sys
from collections import Counter

W, OUT = sys.argv[1], sys.argv[2]


def L(n):
    with open(f"{W}/{n}", encoding="utf-8") as f:
        return json.load(f)


# ---- registered constants (line numbers of the registration)
Z_NEAR, N_MIN, R_MAX = 4.0, 59, 0.05          # l.269, l.273
NFL_MIN, KFL_MIN, KFL_SHARE = 10, 3, 0.10     # l.283
FL20, PLANT_MIN, GREPRO_TOL = 20, 12, 0.01    # l.362, l.298/l.367, l.339
GATE = {"coverage": 0.95, "unknown": 0.05, "dup": 0.01, "empty": 0.01, "refcopy": 0.05, "diacritic": 0.50}  # l.219-223
F1_MAX = 0.005                                # l.142
UNITS_DEV, UNITS_HELD = ("syl", "rdr", "pyvi"), ("uts",)   # l.131-132
F0 = "rdr.tw.pk.cf"                           # l.137


def members(units):                           # l.119: 3 x 3 x 2 = 18 per unit
    return {f"{u}.{t}.{p}.{c}" for u in units for t in ("tw", "tm", "tf") for p in ("pk", "pf", "pa") for c in ("cf", "ck")}


def sig(s):                                   # l.160: sig+ L_f > 0, sig- U_f < 0; s = [D, L, U, sd]
    return 1 if s[1] > 0 else -1 if s[2] < 0 else 0


def z(s):                                     # l.269: |D_f| / sd_boot(D_f); sd = 0 is flagged, not ruled in the text
    return abs(s[0]) / s[3] if s[3] > 0 else (math.inf if abs(s[0]) > 1e-9 else 0.0)


def certify(c, G, metric="cider"):            # l.160-168
    cls = [cl for cl in c["classes"].values() if G & set(cl["members"])]
    if not cls:
        return None
    sg = [sig(cl[metric]) for cl in cls]
    f0 = [s for cl, s in zip(cls, sg) if F0 in cl["members"] and F0 in G]
    cert = 1 if all(s == 1 for s in sg) else -1 if all(s == -1 for s in sg) else 0
    if cert:
        v = "CERTIFIED (a > b)" if cert == 1 else "CERTIFIED (b > a)"
    else:
        v = "REVERSED" if (1 in sg and -1 in sg) else "FRAGILE" if any(sg) else "NULL-STABLE"
    Ds = [cl[metric][0] for cl in cls if abs(cl[metric][0]) > 1e-9]
    return {"verdict": v, "cert": cert, "sig_f0": (f0[0] if f0 else None),
            "changed": bool(f0) and f0[0] != 0 and not cert,
            "point_flip": any(d > 0 for d in Ds) and any(d < 0 for d in Ds),
            "z_min": min(z(cl[metric]) for cl in cls), "n_classes": len(cls),
            "sd0": sum(cl[metric][3] <= 0 for cl in cls)}


def tally(vs):
    vs = [v for v in vs if v]
    n_sig = sum(v["sig_f0"] not in (None, 0) for v in vs)
    k = sum(v["changed"] for v in vs)
    return {"comparisons": len(vs), "CERTIFIED": sum(bool(v["cert"]) for v in vs),
            "FRAGILE": sum((not v["cert"]) and v["verdict"] != "NULL-STABLE" for v in vs),  # REVERSED is a subset (l.163)
            "REVERSED": sum(v["verdict"] == "REVERSED" for v in vs),
            "NULL-STABLE": sum(v["verdict"] == "NULL-STABLE" for v in vs),
            "significant_under_f0": n_sig, "CHANGED": k, "CHANGED_share": (k / n_sig if n_sig else None),
            "point_flips": sum(v["point_flip"] for v in vs)}


def verdict_set(cert):                        # l.269: z_min <= 4; if |V| < 59, V = Cert
    near = [i for i, zz in cert if zz <= Z_NEAR]
    return (near, "near-margin") if len(near) >= N_MIN else ([i for i, _ in cert], "fallback")


def binom_cdf(k, n, p):
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(0, k + 1))


def bisect(f, lo=0.0, hi=1.0):                # f decreasing in p; root of f(p) = 0
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def cp_upper(k, n, a=0.05):                   # one-sided 95% Clopper-Pearson upper bound (l.273)
    return 1.0 if k >= n else bisect(lambda p: binom_cdf(k, n, p) - a)


def cp_lower(k, n, a=0.05):                   # one-sided 95% lower bound
    return 0.0 if k <= 0 else bisect(lambda p: a - (1 - binom_cdf(k - 1, n, p)))


def p1_label(n, breaks, held_empty):          # l.273, l.360, l.363
    if held_empty or n < N_MIN:
        return "NOT_EVALUABLE"
    if cp_upper(breaks, n) <= R_MAX:
        return "PASS"
    if cp_lower(breaks, n) > R_MAX:
        return "FAIL"
    return "INCONCLUSIVE"


def p2_label(n, k):                           # l.283
    if n < NFL_MIN:
        return "NOT_EVALUABLE"
    return "SUPPORTED" if (k >= KFL_MIN and k / n >= KFL_SHARE) else "NOT SUPPORTED"


def tol(p):                                   # l.235: 0.5 x 10^(-d) + 1e-9
    d = len(p.split(".")[1]) if "." in p else 0
    return 0.5 * 10 ** (-d) + 1e-9


def auc(pos, neg):                            # coded reading of l.308: P(z0 of CHANGED < z0 of not CHANGED), ties 0.5
    if not pos or not neg:
        return None
    return sum((p < q) + 0.5 * (p == q) for p in pos for q in neg) / (len(pos) * len(neg))


R = {}  # results

# ---------------------------------------------------------------- self-check of the Clopper-Pearson code against l.273
R["cp_check"] = {"upper_0_of_59": cp_upper(0, 59), "upper_0_of_58": cp_upper(0, 58),
                 "closed_form_59": 1 - 0.05 ** (1 / 59), "closed_form_58": 1 - 0.05 ** (1 / 58)}
assert R["cp_check"]["upper_0_of_59"] < 0.05 < R["cp_check"]["upper_0_of_58"]
assert abs(R["cp_check"]["upper_0_of_59"] - R["cp_check"]["closed_form_59"]) < 1e-9

fam, cen, gate, dev, nc, vj, res, fe = (L(n) for n in ("FAMILY.json", "CENSUS.json", "GATE2.json", "DEV.json", "NC.json",
                                                         "V.json", "RESULT.json", "FEID.json"))

# ---------------------------------------------------------------- provenance chain inside the files
R["chain"] = {n: {"registration_sha256": o.get("registration_sha256"), "stage": o.get("stage"),
                  "prev_sha256": o.get("prev_sha256"), "inputs_sha256": o.get("inputs_sha256"),
                  "code": {k.split("/")[-1]: v for k, v in o.get("code_sha256", {}).items()},
                  "utc_start": o.get("utc_start"), "utc_end": o.get("utc_end")}
              for n, o in (("FAMILY.json", fam), ("CENSUS.json", cen), ("GATE2.json", gate), ("DEV.json", dev),
                           ("NC.json", nc), ("V.json", vj), ("RESULT.json", res), ("FEID.json", fe))}

# ---------------------------------------------------------------- stage F
f1 = {}
for u, r in fam["F1"].items():
    share = r["failed"] / max(1, r["strings"])
    f1[u] = {"strings": r["strings"], "failed": r["failed"], "aligned": r["aligned"],
             "whitespace_fallback": r["whitespace_fallback"], "share": share,
             "dropped_recomputed": (not r["aligned"]) or r["whitespace_fallback"] or share > F1_MAX,
             "dropped_code": r["dropped"]}
gr = fam["G_repro"]
R["F"] = {"F1": f1, "units_dropped_code": fam["units_dropped"],
          "units_dropped_recomputed": [u for u in ("pyvi", "uts") if f1[u]["dropped_recomputed"]],
          "rdr_fault_recomputed": f1["rdr"]["dropped_recomputed"],
          "env": {k: (v if not isinstance(v, dict) else v) for k, v in fam["env"].items()},
          "F3_equal": {u: [sum(bool(x["equal"]) for x in v), len(v), sum(bool(x["addition"]) for x in v)] for u, v in fam["F3"].items()},
          "G_repro": {"n": len(gr), "max_abs_diff": max(x["abs_diff"] for x in gr),
                      "n_within_recomputed": sum(x["abs_diff"] <= GREPRO_TOL for x in gr),
                      "n_ok_code": sum(bool(x["ok"]) for x in gr)},
          "no_committed_score_n": len(fam["no_committed_score"]),
          "n_images": fam["n_images"], "n_refs": fam["n_refs"], "family": fam["family"],
          "family_recomputed": {"F": len(members(UNITS_DEV + UNITS_HELD)), "F_dev": len(members(UNITS_DEV)),
                                "F_held": len(members(UNITS_HELD)), "F_plus": (len(members(UNITS_DEV + UNITS_HELD)) + 18) * 3 + 1}}

# ---------------------------------------------------------------- stage C
rows = list(csv.DictReader(open(f"{W}/SYSTEMS.tsv", encoding="utf-8"), delimiter="\t"))
own = [r for r in rows if r["role"] == "own"]
base = [r for r in rows if r["role"] == "baseline"]
D_re = [f"D:{x['name']}|{y['name']}" for k, x in enumerate(own) for y in own[k + 1:]
        if x["stratum"] == y["stratum"] and x["family"] != y["family"]]
if len(base) == 2:
    D_re.append(f"D:{base[0]['name']}|{base[1]['name']}")
R["C"] = {"own": len(own), "baselines": len(base), "families_recomputed": len({r["family"] for r in own}),
          "families_code": cen["families"], "strata_recomputed": dict(Counter(r["stratum"] for r in own)),
          "strata_code": cen["strata"], "D_size_recomputed": len(D_re), "D_size_code": cen["D_size"],
          "D_set_equal": set(D_re) == set(cen["D"]), "D_len_code": len(cen["D"]),
          "underthesea_hits": len(cen["underthesea_hits"]), "uts_moved_to_dev_code": cen["uts_moved_to_dev"],
          "uts_moved_recomputed": bool(cen["underthesea_hits"]),
          "char_hits": len(cen["character_unit_hits_logged_only"]),
          "census_files": len(cen["segmenter_census"]),
          "b2_score_files": len(cen["b2_score_sha256"]),
          "value_types": dict(sum((Counter(v) for v in cen["value_types"].values()), Counter()))}
seg_vals = Counter()
for f, ss in cen["segmenter_census"].items():
    if not f.startswith("b2_external/"):
        seg_vals.update(ss)
toks = [(f, x.lower()) for f, ss in cen["segmenter_census"].items() for x in ss]  # coded reading of l.340 (READ_PACKAGE.md l.62)
R["C"]["uts_hits_recomputed"] = len({f for f, x in toks if "underthesea" in x or x.endswith("_uts")})
R["C"]["chr_hits_recomputed"] = len({f for f, x in toks if "char" in x or x.endswith("_chr")})
R["C"]["own_segmenter_values"] = dict(seg_vals)
R["C"]["own_census_files"] = sum(not f.startswith("b2_external/") for f in cen["segmenter_census"])
R["C"]["b2_field_names_n"] = sum(len(ss) for f, ss in cen["segmenter_census"].items() if f.startswith("b2_external/"))

# ---------------------------------------------------------------- stage G
G = {}
for k, v in gate["files"].items():
    if "coverage" in v:
        bad = [n for n, ok in (("2 coverage", v["coverage"] >= GATE["coverage"]), ("2 unknown", v["unknown"] <= GATE["unknown"]),
                               ("3 dup", v["dup"] <= GATE["dup"]), ("4 empty", v["empty"] <= GATE["empty"]),
                               ("5 refcopy", v["refcopy"] <= GATE["refcopy"]), ("6 diacritic", v["diacritic"] >= GATE["diacritic"])) if not ok]
        G[k] = {**{x: v[x] for x in ("rows", "coverage", "unknown", "dup", "empty", "refcopy", "diacritic")},
                "admitted_recomputed": not bad, "reasons_recomputed": bad, "admitted_code": v["admitted"], "reasons_code": v["reasons"]}
    else:
        G[k] = {"admitted_recomputed": None, "admitted_code": v["admitted"], "reasons_code": v["reasons"]}
comps = gate["comparisons"]
formed_chk = []
for c in comps:  # formed needs the reference-id count; derivable only when both files have unknown = dup = 0
    a, b = gate["files"][f"{c['group']}/{c['a']}"], gate["files"][f"{c['group']}/{c['b']}"]
    est = None
    if all(x.get("unknown") == 0 and x.get("dup") == 0 for x in (a, b)):
        ra, rb = a["rows"] / a["coverage"], b["rows"] / b["coverage"]
        est = (ra, rb)
    formed_chk.append({"id": c["id"], "n": c["n"], "formed_code": c["formed"], "refs_est": est,
                       "formed_recomputed": (None if est is None or abs(est[0] - est[1]) > 1e-6 else c["n"] >= 0.95 * est[0])})
R["G"] = {"files": G, "n_files": len(G), "n_admitted_code": sum(v["admitted_code"] for v in G.values()),
          "comparisons": len(comps), "formed_sum_recomputed": sum(c["formed"] for c in comps), "formed_code": gate["formed"],
          "K_FL20_recomputed": sum(c["formed"] for c in comps) < FL20, "K_FL20_code": gate["K_FL20"],
          "per_group": {g: [sum(1 for c in comps if c["group"] == g), sum(c["formed"] for c in comps if c["group"] == g)]
                        for g in sorted({c["group"] for c in comps})},
          "per_repo": {g: [sum(1 for c in comps if c["repo"] == g), sum(c["formed"] for c in comps if c["repo"] == g)]
                       for g in sorted({c["repo"] for c in comps})},
          "n_by_comp": sorted({(c["group"], c["n"]) for c in comps}),
          "formed_chk": formed_chk, "label_code": gate["label"], "refs_sha256": gate["refs_sha256"]}

# ---------------------------------------------------------------- stage 1: D over F_dev, NC
Gd = members(UNITS_DEV)
syl, other = members(("syl",)), members(("rdr", "pyvi"))
D = dev["comparisons"]
vD = {c["id"]: certify(c, Gd) for c in D}
t_dev = tally(vD.values())
code_dev = {k: v for k, v in dev["counts_F_dev"].items() if k != "breaking_levels"}
ncv = {c["id"]: certify(c, syl) for c in D}
cert_nc = [(i, v["z_min"]) for i, v in ncv.items() if v and v["cert"]]
Vnc, nc_rule = verdict_set(cert_nc)
byid = {c["id"]: c for c in D}
nc_breaks = 0
for i in Vnc:
    s = ncv[i]["cert"]
    cls = [cl["cider"] for cl in byid[i]["classes"].values() if other & set(cl["members"])]
    nc_breaks += any(sig(x) != s for x in cls)
r_nc = nc_breaks / len(Vnc) if Vnc else None
nc_status = ("NOT_EVALUABLE" if len(Vnc) < N_MIN else "LOW-SENSITIVITY" if r_nc <= R_MAX else "not LOW-SENSITIVITY")
R["1"] = {"members_equal_enumeration": set(dev["members"]) == Gd, "units_dev": dev["units_dev"], "units_held": dev["units_held"],
          "label_code": dev["label"], "n_D": len(D),
          "classes_per_comparison": [min(len(c["classes"]) for c in D), max(len(c["classes"]) for c in D)],
          "sd0_classes": sum(v["sd0"] for v in vD.values()),
          "counts_recomputed": t_dev, "counts_code": code_dev, "counts_equal": {k: t_dev[k] == code_dev[k] for k in t_dev},
          "NC": {"cert_NC": len(cert_nc), "near_margin_n": sum(zz <= Z_NEAR for _, zz in cert_nc), "V_NC": len(Vnc),
                 "rule": nc_rule, "breaks": nc_breaks, "r_NC": r_nc, "status": nc_status},
          "NC_code": {k: nc[k] for k in ("label", "cert_NC", "V_NC", "rule", "breaks", "r_NC", "status")}}

# ---------------------------------------------------------------- stage 2a: FL over F_dev, V
FL = vj["fl"]
vFLd = {c["id"]: certify(c, Gd) for c in FL}
t_fld = tally(vFLd.values())
code_fld = {k: v for k, v in vj["counts_FL_F_dev"].items() if k != "breaking_levels"}
vd = {**vD, **vFLd}
cert = [(i, v["z_min"]) for i, v in vd.items() if v and v["cert"]]
V, v_rule = verdict_set(cert)
R["2a"] = {"n_FL": len(FL), "all_formed": all(c["formed"] for c in FL), "label_code": vj["label"],
           "sd0_classes": sum(v["sd0"] for v in vFLd.values()),
           "counts_recomputed": t_fld, "counts_code": code_fld, "counts_equal": {k: t_fld[k] == code_fld[k] for k in t_fld},
           "cert_dev": len(cert), "cert_dev_FL": sum(i.startswith("FL:") for i, _ in cert),
           "near_margin_n": sum(zz <= Z_NEAR for _, zz in cert), "N": len(V), "rule": v_rule,
           "V_in_D": sum(i.startswith("D:") for i in V), "V_in_FL": sum(i.startswith("FL:") for i in V),
           "V_equal_code_set": set(V) == set(vj["V"]), "V_equal_code_order": V == vj["V"],
           "code": {k: vj[k] for k in ("N", "rule", "cert_dev", "cert_dev_FL")}, "V_len_code": len(vj["V"]),
           "z_min_range_in_V": [min(zz for i, zz in cert if i in set(V)), max(zz for i, zz in cert if i in set(V))]}

# ---------------------------------------------------------------- stage 2b
rc = {c["id"]: c for c in res["comparisons"]}
assert set(rc) == set(vd), "RESULT comparisons differ from D + FL"
certF = lambda i: rc[i]["F"].startswith("CERTIFIED")  # noqa: E731
fdev_equal = sum(rc[i]["F_dev"] == vd[i]["verdict"] for i in vd)
# a comparison certified over F_dev breaks exactly when it is not CERTIFIED over F (F = F_dev + F_held)
brk = lambda sel: sum(not certF(i) for i in sel)  # noqa: E731
dir_conflict = sum(1 for i in vd if vd[i]["cert"] and certF(i) and rc[i]["F"] != vd[i]["verdict"])
N = len(V)
b = brk(V)
held_empty = not dev["units_held"]
p1 = {"N": N, "breaks": b, "r": (b / N if N else None), "cp_upper_95": cp_upper(b, N), "cp_lower_95": cp_lower(b, N),
      "label": p1_label(N, b, held_empty)}
cert_all = [i for i, _ in cert]
flc = [i for i in cert_all if i.startswith("FL:")]
dc = [i for i in cert_all if i.startswith("D:")]
fb = brk(flc)
beside = {"FL_row": {"n": len(flc), "breaks": fb, "cp_lower_95": cp_lower(fb, len(flc)) if flc else None,
                     "cp_upper_95": cp_upper(fb, len(flc)) if flc else None,
                     "state_beside_P1": (cp_lower(fb, len(flc)) > R_MAX) if flc else None},
          "all_Cert_dev": {"n": len(cert_all), "breaks": brk(cert_all)},
          "D_only": {"n": len(dc), "breaks": brk(dc)}, "FL_only": {"n": len(flc), "breaks": fb}}
# P2
sig0 = {i: vd[i]["sig_f0"] for i in vd}
fl_ids = [c["id"] for c in FL]
n_fl = sum(sig0[i] not in (None, 0) for i in fl_ids)
chg = {i: (sig0[i] not in (None, 0)) and not certF(i) for i in vd}
k_fl = sum(chg[i] for i in fl_ids)
repos = sorted({c["repo"] for c in FL})
per_repo = {r: [sum(sig0[c["id"]] not in (None, 0) for c in FL if c["repo"] == r), sum(chg[c["id"]] for c in FL if c["repo"] == r)] for r in repos}
loo = {r: {"n": n_fl - per_repo[r][0], "k": k_fl - per_repo[r][1]} for r in repos}
p2 = {"n_FL": n_fl, "k_FL": k_fl, "share": (k_fl / n_fl if n_fl else None), "label": p2_label(n_fl, k_fl),
      "per_repository_n_k": per_repo, "leave_one_repository_out": loo, "K_FL20_descriptive": len(FL) < FL20,
      "K_FL": n_fl < NFL_MIN}


def tally_F(ids):  # from the code's per-comparison F verdict strings (held-out class statistics are not stored)
    vs = [rc[i]["F"] for i in ids]
    ns = sum(sig0[i] not in (None, 0) for i in ids)
    k = sum(chg[i] for i in ids)
    return {"comparisons": len(vs), "CERTIFIED": sum(v.startswith("CERTIFIED") for v in vs),
            "FRAGILE": sum(v in ("FRAGILE", "REVERSED") for v in vs), "REVERSED": sum(v == "REVERSED" for v in vs),
            "NULL-STABLE": sum(v == "NULL-STABLE" for v in vs), "significant_under_f0": ns, "CHANGED": k,
            "CHANGED_share": (k / ns if ns else None)}


d_ids = [c["id"] for c in D]
cnt = res["counts"]
strip = lambda o, keys: {k: o[k] for k in keys}  # noqa: E731
KEYS8 = ("comparisons", "CERTIFIED", "FRAGILE", "REVERSED", "NULL-STABLE", "significant_under_f0", "CHANGED", "CHANGED_share")
tF_FL, tF_D = tally_F(fl_ids), tally_F(d_ids)
z0 = {}
for c in D + FL:
    z0[c["id"]] = z(next(cl["cider"] for cl in c["classes"].values() if F0 in cl["members"]))
d_f0_maxdiff = max(abs(rc[c["id"]]["D_f0"] - next(cl["cider"][0] for cl in c["classes"].values() if F0 in cl["members"])) for c in D + FL)
allids = list(vd)
auc_all = auc([z0[i] for i in allids if chg[i]], [z0[i] for i in allids if not chg[i]])
s0 = [i for i in allids if sig0[i] not in (None, 0)]
auc_sig = auc([z0[i] for i in s0 if chg[i]], [z0[i] for i in s0 if not chg[i]])
sec = res["secondary"]
R["2b"] = {"F_dev_verdict_strings_equal": [fdev_equal, len(vd)], "direction_conflicts": dir_conflict,
           "changed_flags_equal": sum(chg[i] == rc[i]["changed_F"] for i in vd),
           "D_f0_maxdiff": d_f0_maxdiff, "units_code": res["units"], "label_D": res["label_D"], "label_FL": res["label_FL"],
           "P1_recomputed": p1, "P1_code": res["P1"], "beside_recomputed": beside, "beside_code": res["P1_beside"],
           "P2_recomputed": p2, "P2_code": res["P2"],
           "counts_recomputed": {"FL_over_F": tF_FL, "FL_over_F_dev": {k: t_fld[k] for k in KEYS8},
                                 "D_over_F_DEVELOPMENT": tF_D, "D_over_F_dev_DEVELOPMENT": {k: t_dev[k] for k in KEYS8}},
           "counts_code": {k: {x: (v[x] if x in v else None) for x in list(KEYS8) + ["point_flips"]} for k, v in cnt.items()},
           "breaking_levels_code": {k: v["breaking_levels"] for k, v in cnt.items()},
           "secondary_code": {k: (v if not isinstance(v, dict) else {x: v[x] for x in list(KEYS8) + ["point_flips"]}) for k, v in sec.items()},
           "secondary_breaking_levels_code": {k: v["breaking_levels"] for k, v in sec.items() if isinstance(v, dict)},
           "AUC_recomputed": auc_all, "AUC_sig_recomputed": auc_sig,
           "AUC_pos_neg": [sum(chg.values()), len(chg) - sum(chg.values())], "AUC_sig_pos_neg": [sum(chg[i] for i in s0), len(s0) - sum(chg[i] for i in s0)],
           "F_verdicts_by_set": {s: dict(Counter(rc[i]["F"] for i in ids)) for s, ids in (("D", d_ids), ("FL", fl_ids))},
           "F_dev_verdicts_by_set": {s: dict(Counter(vd[i]["verdict"] for i in ids)) for s, ids in (("D", d_ids), ("FL", fl_ids))},
           "V_F_verdicts": dict(Counter(rc[i]["F"] for i in V)),
           "fl_table": [{"id": c["id"], "repo": c["repo"], "n": c["n"], "F_dev": vd[c["id"]]["verdict"], "F": rc[c["id"]]["F"],
                         "sig_f0": sig0[c["id"]], "changed": chg[c["id"]], "z_min_dev": vd[c["id"]]["z_min"], "in_V": c["id"] in set(V)} for c in FL],
           "baseline_pair": {"F_dev": vd.get("D:ktvic_resnetlstm|ktvic_vittrans", {}).get("verdict"),
                             "F": rc.get("D:ktvic_resnetlstm|ktvic_vittrans", {}).get("F"),
                             "in_V": "D:ktvic_resnetlstm|ktvic_vittrans" in set(V)}}

# ---------------------------------------------------------------- stage 3
p3 = fe["P3"]
P3 = {"label_code": p3.get("label"), "evidence_code": p3.get("evidence"), "M_new_code": p3.get("M_new"),
      "dropped_K_coco": p3.get("dropped_K_coco"), "not_used": p3.get("not_used"), "identification_code": p3.get("identification"),
      "margin_code": p3.get("margin"), "rows": {}, "old": {}}
ok_all = True
for part, key in (("rows", "M_new_rows"), ("old", "cider_bleu4_POST_HOC")):
    for bn, ms in p3.get(key, {}).items():
        for m, r in ms.items():
            rep = r["rstar"] is not None and abs(r["rstar"] - float(r["printed"])) <= tol(r["printed"])
            dist = None if r["rstar"] is None else abs(r["rstar"] - float(r["printed"]))
            P3[part][f"{bn}::{m}"] = {"printed": r["printed"], "rstar": r["rstar"], "tol": tol(r["printed"]), "distance_recomputed": dist,
                                      "distance_code": r["distance"], "reproduced_recomputed": rep, "reproduced_code": r["reproduced"]}
            if part == "rows":
                ok_all = ok_all and rep
m_new_re = sorted({k.split("::")[1] for k in P3["rows"]})
P3["M_new_recomputed"] = m_new_re
P3["label_recomputed"] = ("no registered label (M_new empty)" if not m_new_re else "SUPPORTED" if ok_all else "NOT SUPPORTED")
pl = fe["plants"]
pc = Counter(v["label"] for v in pl.values())
p4 = fe["P4"]
P4 = {"n": len(pl), "IDENTIFIED": pc.get("IDENTIFIED", 0), "AMBIGUOUS": pc.get("AMBIGUOUS", 0), "OUTSIDE": pc.get("OUTSIDE", 0),
      "other_labels": {k: v for k, v in pc.items() if k not in ("IDENTIFIED", "AMBIGUOUS", "OUTSIDE")},
      "K_plant_recomputed": pc.get("IDENTIFIED", 0) < PLANT_MIN,
      "code": {k: p4[k] for k in ("IDENTIFIED", "AMBIGUOUS", "OUTSIDE", "identification", "label")},
      "margins_non_null": sorted(v for v in p4["margins"].values() if v is not None),
      "classes_range": [min(v["classes"] for v in pl.values()), max(v["classes"] for v in pl.values())],
      "nearest_distance_range": [min(v["nearest_distance"] for v in pl.values()), max(v["nearest_distance"] for v in pl.values())],
      "margin_null_iff_not_identified": all((v["margin"] is None) == (v["label"] != "IDENTIFIED") for v in pl.values())}
FE = {}
for bn, r in fe["fe_id"].items():
    rep = r.get("reproducing", [])
    n_rep = len(rep)
    lab51 = "IDENTIFIED" if n_rep == 1 else "AMBIGUOUS" if n_rep >= 2 else "OUTSIDE"
    FE[bn] = {"label_code": r["label"], "classes": r.get("classes"), "reproducing_classes": n_rep,
              "reproducing_members": [len(c) for c in rep],
              "reproducing_kinds": [dict(Counter(("r*" if m == "r*" else m.split(":")[0] if ":" in m else "matched") for m in c)) for c in rep],
              "reproducing_units": [dict(Counter(("r*" if m == "r*" else m.split(":")[-1].split(".")[0]) for m in c)) for c in rep],
              "reproducing_members_names": rep,
              "rstar_reproduces": any("r*" in c for c in rep),
              "label_5_1_recomputed": lab51, "margin": r.get("margin"), "nearest_distance": r.get("nearest_distance"),
              "printed_used": r.get("printed_used"), "METEOR_excluded_for_members": r.get("METEOR_excluded_for_members"),
              "P3b_list_len": len(r.get("P3b_matched_F_reproducing_CIDEr-D_POST_HOC", [])),
              "P3b_from_reproducing": sum(1 for c in rep for m in c if ":" not in m and m != "r*" and not m.startswith("chr."))}
pcm = fe["printed_comparisons"]
pairs = pcm["pairs"]
resc = [p for p in pairs if p.get("kind") == "re-scorable"]
PC = {"label_code": pcm["label"], "n_pairs": len(pairs), "kinds": dict(Counter(p.get("kind") for p in pairs)),
      "sources": dict(Counter(p.get("source") for p in pairs)),
      "n_rescorable_recomputed": len(resc), "n_rescorable_code": pcm["n_rescorable"],
      "order_changes_recomputed": sum(p["printed_gap"] * p["f0_gap"] < 0 for p in resc), "order_changes_code": pcm["order_changes_under_f0"],
      "not_certified_recomputed": sum(not p["certificate_F"].startswith("CERTIFIED") for p in resc), "not_certified_code": pcm["not_certified_over_F"],
      "rescorable_rows": [{k: p.get(k) for k in ("source", "kind", "printed_gap", "f0_gap", "order_changes", "certificate_F")} for p in resc],
      "one_sided_rows": [{k: p.get(k) for k in ("source", "kind", "gap_released_f0_minus_other_printed", "note")} for p in pairs if p.get("kind") == "one-sided"],
      "pair_keys": sorted({k for p in pairs for k in p})}
R["3"] = {"env_rstar": fe["env_rstar"], "printed_sha256": fe["printed_sha256"], "pool": fe["pool"], "rstar_in_pool": fe["rstar_in_pool"],
          "label_code": fe["label"], "P3": P3, "P4": P4, "fe_id": FE, "printed_comparisons": PC, "fe_id_files": list(fe["fe_id"].keys())}

# ---------------------------------------------------------------- additions: breaking levels over F_dev (l.165-166), break ids
def breaking_levels(comps, Gs):
    tot = Counter()
    for c in comps:
        cls = [cl for cl in c["classes"].values() if Gs & set(cl["members"])]
        sg = [sig(cl["cider"]) for cl in cls]
        cert = all(s == 1 for s in sg) or all(s == -1 for s in sg)
        f0 = [s for cl, s in zip(cls, sg) if F0 in cl["members"] and F0 in Gs]
        s0 = f0[0] if f0 else 0
        nominal = s0 or (1 if sg.count(1) > sg.count(-1) else -1 if sg.count(-1) > sg.count(1) else 0)
        if cert or not nominal:
            continue
        for cl, s in zip(cls, sg):
            if s != nominal:
                for mn in cl["members"]:
                    if mn in Gs:
                        tot.update(mn.split("."))
    return dict(sorted(tot.items()))


R["breaking"] = {"D_F_dev_recomputed": breaking_levels(D, Gd), "D_F_dev_code_DEV": dict(sorted(dev["counts_F_dev"]["breaking_levels"].items())),
                 "D_F_dev_code_RESULT": dict(sorted(cnt["D_over_F_dev_DEVELOPMENT"]["breaking_levels"].items())),
                 "FL_F_dev_recomputed": breaking_levels(FL, Gd), "FL_F_dev_code_V": dict(sorted(vj["counts_FL_F_dev"]["breaking_levels"].items())),
                 "FL_F_dev_code_RESULT": dict(sorted(cnt["FL_over_F_dev"]["breaking_levels"].items()))}
R["breaks_in_V"] = [{"id": i, "F_dev": vd[i]["verdict"], "F": rc[i]["F"], "z_min_dev": vd[i]["z_min"]} for i in V if not certF(i)]
R["breaks_in_Cert_dev"] = [i for i in cert_all if not certF(i)]
R["V_strata"] = dict(Counter(("FL" if i.startswith("FL:") else i.split("|")[0].rsplit("-", 1)[-1]) for i in V))
R["counts_2b_equal"] = {k: {x: R["2b"]["counts_recomputed"][k][x] == R["2b"]["counts_code"][k][x] for x in KEYS8} for k in R["2b"]["counts_recomputed"]}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(R, f, indent=1, sort_keys=True, default=str)
print("written", OUT)
```
