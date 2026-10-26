# Addendum C3 to PREREG 2026-10-26_b_posthoc: mapping, names and paths only

- **Scope.** PREREG §A.4 (sha256 `08afefd4fe87229c2d48415fc3f46f3ef95de11c05b52f937e953a807483f823`, commit 13da5d7) allows this addendum to supply the member mapping, the output names and the paths, and nothing else. Every rule, gate, constant and reporting line stays as in PREREG §A.2-A.6.
- **Runner.** `scripts/b_f1/posthoc_mbr3.py`, sha256 `afa827b02d8dc0e1c210dd3eadf85af8adb6323c1b080f2a476d2a405ee3d63e`.
  - `run` refuses unless the runner, the PREREG and this addendum equal their blobs at HEAD.
  - `run` also refuses unless the JSON block below names that runner sha, the PREREG and the §A.2 member files.
- **Synthetic dry-run record.** `manuscript/prereg/2026-10-26_b_posthoc/c3_dryrun_synthetic.json`. It was made with `posthoc_mbr3.py dry` from synthetic ids, references and captions only, and it read no KTVIC file and no member file. Its sha256 is listed in this folder's `SHA256SUMS_C3`.

```json
{
 "prereg": {"path": "manuscript/prereg/2026-10-26_b_posthoc/PREREG.md", "sha256": "08afefd4fe87229c2d48415fc3f46f3ef95de11c05b52f937e953a807483f823"},
 "runner": {"path": "scripts/b_f1/posthoc_mbr3.py", "sha256": "afa827b02d8dc0e1c210dd3eadf85af8adb6323c1b080f2a476d2a405ee3d63e"},
 "members": {
  "s42": ["data/results/p1assist_s42-short.preds.json", "ca5ce25366b04def1ca1099344a0e4a610bf767e357140525e4290913ffe2fef"],
  "s43": ["data/results/p1assist_s43-short.preds.json", "13343482926cade1e3640185e3c5bd7cd504df5f2a2099ffb614d7a9bcb51861"],
  "s44": ["data/results/p1assist_s44-short.preds.json", "9344cb3504f3b925156ee59952735e946a97de29b682583d217de4198060f248"]
 },
 "names": {"mbr": "p1r_mbr3_posthoc-test-short"},
 "paths": {
  "record": "data/results/b_posthoc/b_posthoc_mbr3_run.json",
  "dry_record": "manuscript/prereg/2026-10-26_b_posthoc/c3_dryrun_synthetic.json",
  "mbr_preds": "a temporary directory outside the repository, deleted at exit; only its sha256 is recorded"
 }
}
```

- **Member mapping.** `s42`, `s43` and `s44` are the keys of `score_b_f1.py` (S1's order, so MBR ties go to the lower seed). Each maps to the §A.2 file of the same P1-R seed.
- **Command, run once (PREREG §A.5), from the repo root after this addendum is committed.** The environment is as B-F1's scoring: python 3.12.3, numpy 2.5.4, pycocoevalcap 1.2, py_vncorenlp 0.1.4, pyjnius 1.9.0, VnCoreNLP jar 9e2811cd, rdr 9e62f96b and `JAVA_TOOL_OPTIONS=-XX:ActiveProcessorCount=1`.

  ```
  NCS_DATA=<dir holding datasets/ktvic> VNCORENLP_DIR=<VnCoreNLP 1.2 dir> JAVA_HOME=<JDK> \
    python scripts/b_f1/posthoc_mbr3.py run
  ```
