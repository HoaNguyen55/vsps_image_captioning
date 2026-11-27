# ERRATUM C-N3D 2: the host is the investigator's own PC (ruled in CC-511e2)

Registration: `manuscript/prereg/2026-11-27_c_n3d/` (commit 39b8bc4; erratum 1 at 9b50ee9; code at 3c41593).
Status: ruled by CC-511e2 (2026-11-27). Commit before any N3D file reaches the PC. No input has been opened and no N3D quantity exists. Errata are allowed before use.

**Why.** PI-1127m (2026-11-27) stops all new rentals and offers the investigator's own PC (RTX 3090, kept on). The registered host rule cannot be met word for word on that PC:
- COMPUTE v3 §1 "host share" (CC-509 W2), prereg v3 §2 "No GPU" and §10 step 2, and CC-511r2 K3 call for "a rented host only … never a host that holds, or will hold, any OV-test byte, the C-CONF token or a C-CONF output".
- The PC held unread committed OV-test files as git objects until 2026-11-26T19:44:35Z, outside any token (K14; LOG OPS-1126br-pc-w8; ERRATUM-1127b). Those objects were removed and the PC was rescanned clean.
- The PC may later become the C-CONF test host (CC-481r2e3).

**The purpose of the rule** (CC-509 W2): N3D must never share a host with OV-test bytes or with C-CONF material. Its inputs, intermediates and outputs must never sit beside them. Under this erratum, that purpose is met by separation in time with records, not by renting a new machine. Every N3D input is pinned by sha256, so no other file on the PC can enter a row. The custody check (step 2a) is unchanged.

**Replacement text.** It replaces the host clauses named above and the operator statement of record (i).
"The host is the investigator's own PC (PI-1127m), in its own folder `~/vsps_host/c_n3d/` only. On that PC, all of the following hold:
1. **Before any push.** A host-wide test-set file-name scan over the user's folders, `/tmp` and `/dev/shm` finds 0 hits. The only files exempt are the committed refusal and id lists (`ov_test_files.tsv`, `ov_test_dev299_neardup_files.txt`, `exclusion.json`, `lists.json`, `c_conf_carve_order.json`, `c_t1_f30k_lists.json`) and the scan's own list. No `.git` without a blob filter exists anywhere under the user's folders. No C-CONF folder, token or output exists on the PC.
2. **The push.** Files reach the PC by tar push of the PUSH LIST, the code folder and the `$NCS_DATA` pins only. No `.git` and no directory push from the repository.
3. **The order.** Record (i), the S0 record, comes before the data push. The custody check (step 2a) is the first data step. Then comes the one run under the 4 h kill.
4. **No overlap with C-CONF.** N3D starts only if no C-CONF set-up step has begun on the PC. N3D ends, with the pull, the re-hash, the wipe and the 0-name find logged, before the first C-CONF staging step on the PC. A C-CONF set-up that begins while N3D is unfinished is a STOP for N3D: the N3D folder is wiped, no partial output is used, and N3D does not run again on that PC without a new ruling.
5. **After the pull.** `~/vsps_host/c_n3d/` is removed in full. Two finds then show 0: a find over the user's folders, `/tmp` and `/dev/shm` for the N3D folder and for the names on its PUSH LIST outside the other studies' own folders, and the test-set file-name scan of item 1. Both are logged before any C-CONF staging.
6. **Once C-CONF has staged anything on the PC,** that PC is closed to N3D."

**Operator statement.** The S0 record's printed line "this host has never held an OV-test byte …" does not hold for this PC. It is replaced in the record by this signed statement: "This PC holds no OV-test byte, no C-CONF token and no C-CONF output at this time (scan of item 1 attached). It held unread committed OV-test git objects until 2026-11-26T19:44:35Z (K14), which were removed and rescanned clean. C-CONF staging will not begin before the N3D wipe record (erratum 2 item 5)." The code is unchanged (CODE.sha256 bdcb1ec1).

**Not changed.** Estimands, thresholds, sets, pins, the custody counts, the code, the 4 h stop, the records (i)–(iv) of RECORDS_W8.md (only the statement above is replaced), and erratum 1. The KTVIC and OpenViIC train caption files sit only inside `~/vsps_host/c_n3d/` and are wiped with it (erratum 1 E1).

**Disclosure.** In the paper's N3D note: "run on the investigator's own PC, which until 2026-11-26 held unread committed test files as git objects (removed before this run); every input was pinned by sha256".
