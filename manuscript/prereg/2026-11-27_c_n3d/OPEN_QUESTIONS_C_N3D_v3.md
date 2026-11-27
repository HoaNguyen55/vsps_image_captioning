# OPEN QUESTIONS C-N3D v2 (v1 2026-11-27T12:14Z; revised under CC-509)

Each question gives a recommendation and a default. The default holds unless a judge or the PI rules otherwise. All of these are reversible design items (delegation rule), except where a question is marked PI.

| id | question | recommendation | default |
|---|---|---|---|
| OQ-1 | How does N3D relate to C-RAA step T8? | **RULED (CC-509 ruling 3): N3D supersedes T8.** T8 is withdrawn from the C-RAA run order; T1–T7 are unchanged. craa-prep drops T8 (its `zs` runs, 0.57 GPU-h, and the `raa_failcat` call) and logs one line citing CC-509. If C-RAA tier 2 inherits N3D's rules, it needs its own code and its own code read. | closed |
| OQ-2 | Should OV-dev-A nominate first? | **No.** OV-dev-A has no batch-1 `zs` decode, so nominating there would mix decode policies. | register directly on OV-dev-B; XM-dev500 descriptive |
| OQ-3 | Should Flickr30K val join the English rows? | **No.** It is the rehearsal that was used once, and REG2 binding 1 says it is never staged. Its files are on the HASH-ONLY LIST [W1]. | closed: never pushed |
| OQ-4 | Decode policy of the Flickr30K carve decodes? | Read it from the c_t1 run record during the code read, and print it as a row label. If the decodes were batched, label the rows "A1 not met; batched decode; descriptive". | label per the record |
| OQ-5 | Split τ_pair by category with `perm`? | Not in v2. The `perm` files are hash-only [W1]. | no |
| OQ-6 | Gold for BO and ZL on XM-dev500? | Verified OIV7 labels through `xm3600_oiv7.statuses`, unchanged, and the reference union otherwise. The pins are fixed in prereg §4 [W6c]. | as in prereg |
| OQ-7 | Have per-image values been seen? | The CC-509 grep found none. The C-ATTR per-image ledgers exist and are hash-only [N1]. | closed |
| OQ-8 | Are the thresholds right? | Keep them: Δ ≥ +0.10; C_L ≥ 0.60 tested against 0.50, with C_L − C_W ≥ +0.10; at least 30 images per group. The power is about 0.4–0.5 at a true +0.10 (prereg §6). | keep |
| OQ-9 | Does the result enter the abstract or the contributions? (**PI**) | No. It goes in Section 6.10.10 and the supplement only, and the PI decides after the rewrite. | not in the abstract |
| OQ-10 | Which host? [W2] | A rented host only: a dedicated rental, or a host rented for a non-C-CONF job (for example B-D1) after its registered job ends. Never a host that holds, or will hold, any OV-test byte (the committed name-and-sha256 list `ov_test_files.tsv` is not an OV-test byte; CC-483r2 ruling 5), the C-CONF token or a C-CONF output. | as stated |
| OQ-11 (new) | The laptop OpenViIC dev annotation file hashes to `2a68a3eb…`, while the pin used by C-ATTR and C-CONF is `550cfe06…` (host data folder `ncs-data/`). Why? | Do not open either file to find out. At the code read, compare their sizes and modification times, and check the Drive copy's hash. Use only the file that equals the pin, and STOP otherwise. The 2a68a3eb copy is never pushed. | closed (CC-509 r2) |
