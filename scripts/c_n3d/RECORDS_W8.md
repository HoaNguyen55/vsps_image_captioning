# C-N3D host records that close the run (CC-511 W8, modelled on CC-506 W5)

Each record is a text file written on the rented host and pulled to the laptop. Its sha256 is entered in a LOG line. No record holds a caption, a per-image row or a study number. The only exception is the decision file of record (iii), which holds aggregates only.

| # | record | made by | when | must show |
|---|---|---|---|---|
| (i) | `S0_RECORD_<machine>.txt` | `host_selftest.sh s0 ROOT DATA` | after the code, the CODE and RESOURCES files of the PUSH LIST and `$NCS_DATA/vncorenlp/` are pushed, **before** any decode file, list file or `$NCS_DATA` caption or reference file is pushed | see the S0 list below |
| (ii) | `CUSTODY_RECORD_<machine>.txt` | `host_selftest.sh custody ROOT DATA` | after the data push; the first data step | `data_pins: ok`; the sha256 of the segmenter model files; the 11 custody counts, all 0; `custody: all counts 0`. Anything else is a STOP and ends the run. |
| (iii) | `RUN_RECORD_<machine>.txt` (the operator writes it from the console) | `host_selftest.sh run ROOT DATA OUT` | after the decision file is written | see the run list below |
| (iv) | LOG line | coordinator | after (iii) | the decision file name and sha256, and the sha256 of records (i)–(iii) |

**The S0 record must show:**
- the machine id;
- the python, numpy and java versions;
- the pip-freeze sha256;
- the jar and segmenter model sha256, with the jar at `9e2811cd…`;
- `CODE.sha256` OK;
- the selftest output with every group of mutants killed;
- `closure: ok`, with the pinned module count;
- an empty "not on the PUSH LIST" list;
- an empty "forbidden names" list, covering no OV-test, C-CONF, `c_t2`, `c_t3`, `c_en` output or ledger file;
- the signed statement that the host was never a C-CONF host.

**The run record must show:**
- `custody: all counts 0`;
- `parity: ok` (each gate passed; no value is printed);
- the decision file name and its sha256 from the host;
- `cpu_h_parent`, `wall_h` and `utc` from the decision file;
- the decision file pulled and re-hashed on the laptop, with the sha equal;
- the per-image intermediates and the `$NCS_DATA` caption and reference files deleted on the host, shown by a listing after deletion;
- the host files cleaned after the machine is deleted (PI-1115s).

The order is fixed:
1. Push the code and the PUSH LIST.
2. Make the S0 record.
3. Push the data.
4. Make the custody record.
5. Make the run record.
6. Pull, re-hash and clean the host.

A STOP at any step ends the work on that host. No re-run follows without a judge ruling.
