# A-E3 Annex B scoring note v1: descriptive rows on existing golds (no labels)

Written 2026-11-12T04:13Z (`date -u`). vsps HEAD `26574ef`. Writer agent. Draft for a one-judge read. No A-E3 output, caption file or label file was opened; `~/vsps_labels/` and the A-E3 pull dir were not opened, listed or stat-ed. Read: the run document, CC-349/351, the plan, and code (`xm3600_oiv7.py`, `crosslingual_gap.py`). AI opinion. "chưa kiểm" = not checked.

**Binds:** run document v1.1 (`1df371cc…`) §11 and Annex B; CC-349 ruling 5 and N5; CC-351 "LATER, WITH THEIR OWN READS".
**Gate:** a judge read before the commit (tier and bar: N-5). **No 7a output is opened, displayed or scored by anyone before this note is committed.** The only reads before that are the §8 pull checks of the run document (sha256, sidecars, counts, `hit_max` sums), which print counts only.
**Label of every row:** "DEVELOPMENT / A-E3, descriptive, new decodes on previously analysed images". No verdict, no hypothesis.

## 1. Which outputs are scored
- Only the 600-image Vietnamese runs `ae3_<key>_xm600-{short,detailed}.preds.json` of models in `passed_7a.txt`, from the pulled 444 copy `.session_backup/machines/ATTR_H1/root/a_e3/out/` (hc2; run document §8 step 1), and of models in `passed_7c.txt`, from the pulled 444 copy `.session_backup/machines/ATTR_H1_7c/root/a_e3/out/` (A-E3 addendum v1 §5.2 step 4; CC-359).
- Not scored: 50-image runs, models that failed G4, HELD outputs (G5), any run reported NOT RUN.
- S6: with fewer than two passing models the arm adds no family comparison, and no difference row of §2 row B3 is printed.

## 2. Rows, script, and where each runs

| Row | Content | Script | Reads gold? | Runs on |
|---|---|---|---|---|
| B0 (N5, before any other row is printed) | One model-card row per passing model: language model and vision encoder as read from `config.json` at the pin; Vietnamese output (the G4 share from the pull line); training-data exposure to COCO-vi, UIT-ViIC and XM3600/Crossmodal-3600 from the model card or paper ("chưa kiểm" allowed and disclosed); licence line (Aya cc-by-nc-4.0 + Cohere Labs acceptable-use policy; Gemma Terms of Use; Idefics3 apache-2.0 card on the Llama 3.1 Community License; LLaVA-1.5 Llama 2 Community License; SmolVLM2 apache-2.0; LLaVA-1.6-Mistral apache-2.0) | none (text row, writer agent, from public cards) | no | laptop (file writing only) |
| B1 | Flattening: `{id: caption}` = the `predictions` key of each file, one flat file per run, sha256 of every flat file logged | the one-liner in §3 | no (reads caption text in code; prints nothing) | laptop, inside the B2 step (see §4) |
| B2 | Per system in S_E: the paper's existing XM3600 measures: `refs` object P/R/F1 against the Vietnamese XM3600 references, and the `oiv7` block (verifiable share, verified precision, verified-negative hallucination, % captions naming a verified-absent class, verified-positive recall), with the scorer's bootstrap (B = 2,000, `default_rng(0)`) | `scripts/xm3600_oiv7.py score` (sha256 `9a79403f…`), unchanged | **yes**: `data/xm3600/oiv7_labels.json`, `vi_oiv7_map.json`, `data/datasets/xm3600/test_data.json` | **laptop** (§4) |
| B3 | Per model: the short-to-detailed difference of each B2 measure (point values, read from the B2 JSON), printed beside the paper's two families' stored values (Q25: `data/results/xm3600/xm3600_oiv7.json`; Q3: `data/results/g2b/g2b_score.json`) | arithmetic on the B2 JSON | no (reads aggregates only) | laptop (file writing only) |
| B4 | Hit-max share per run = sum of `hit_max` / 600 | the per-run `hit_max` sums already logged in the 7a pull OPS line (run document §8 step 3) | no | no new run |
| B5 (7b, later) | English reference-gold ladder only: XM3600-en references, COCO-80 classes, CHAIR's English synonyms | **none exists for new files** (chưa kiểm): `scripts/crosslingual_gap.py score` has the English matcher (`matcher("en")` → `score_coco_probe.en_classes`) but reads only its fixed `PREDS` table. A short new script is needed, with its own code read | **yes**: XM3600-en references | laptop (§4) |

No Vietnamese-versus-English gap row and no Open Images row for 7b (CC-349 Q10).

## 3. Commands (laptop, after this note is committed and the 7a and 7c pulls are verified; one pass over both, CC-359)

```
P=.session_backup/machines/ATTR_H1/root/a_e3/out; Q=.session_backup/machines/ATTR_H1_7c/root/a_e3/out; F=data/results/a_e3/xm600_vi_flat; mkdir -p $F
for dk in $(sed "s#^#$P:#" $P/passed_7a.txt) $(sed "s#^#$Q:#" $Q/passed_7c.txt); do d=${dk%%:*}; k=${dk#*:}; for m in short detailed; do
  python3 -I -B -c 'import json,sys; d=json.load(open(sys.argv[1],encoding="utf-8")); json.dump(d["predictions"],open(sys.argv[2],"w",encoding="utf-8"),ensure_ascii=False,sort_keys=True,indent=1)' \
    $d/ae3_${k}_xm600-$m.preds.json $F/ae3_${k}_xm600-$m.preds.json; done; done
sha256sum $F/*.preds.json > $F/SHA256SUMS_flat
NCS_DATA=data nice -n 19 ~/.venvs/c_stage1_lists/bin/python -B scripts/xm3600_oiv7.py score --results $F --split test_data.json \
  --out data/results/a_e3/annexB_7a_score.json > /dev/null
sha256sum data/results/a_e3/annexB_7a_score.json
```
- Interpreter: the venv of the base build (run document §9.1); whether it holds numpy and the scorer's imports (`object_prf`, `second_panel`, `rescap.chair`) is chưa kiểm and is not tested on the laptop (PI-1111j); a missing import is an exception under the rule below.
- The scorer prints aggregate tables only (no caption text); stdout is discarded so nothing is displayed before the one-judge result read.
- The scorer's `human_xm3600` row is in its output by design; it is the same as the paper's stored row and is not reported again.
- The run is one pass. On an exception, the exit status and exception type are logged, and no rerun follows without a judge line.

## 4. Where scoring runs: laptop, as a recorded deviation from PI-1111j

- **Rule.** PI-1111j (LOG l.2178) moves CPU scoring to a rented host. The coordinator's recorded reading of PI-1111j keeps the PI's label file and sealed material on the laptop.
- **Why B2 and B5 stay on the laptop.** They read the Open Images labels and the XM3600 references, which are the label gold. Run document §7 custody and §9.1 keep them off the hosts ("the builder reads the Open Images labels, which never go to a host"), and S8 bars `xm3600_oiv7.py` on the host. The same holds for the top-up build (`build_topup.py`), which also reads the Open Images labels.
- **Why B1 stays on the laptop too.** It reads caption text, which S8 bars on the host, and the copy of record is the laptop pull (run document §8).
- **Load.** One CPU process under `nice -n 19`, 600 images × the S_E runs, B = 2,000 bootstrap draws. Run document Annex B says every earlier XM3600 score ran on the laptop (chưa kiểm; see N-1). Expected minutes, not hours (chưa kiểm).
- **Logged.** One OPS DEVIATION line: "Annex B B2 scored on the laptop (reads Open Images labels and references; PI-1111j deviation under run document §7 custody)", with UTC start and end, the command, the exit status and the sha256 of every input, flat file and output.
- **Not on the host.** Nothing in this note runs on hc2. hc2's full clone `/root/vsps` does hold the git-tracked label files (CC-349 ruling 1), but the A-E3 custody rule does not allow scoring there (open question N-1).

## 5. Decided by CC-355: each recommended value below is adopted and binds (CC-355 W6)
| # | Question | Recommended |
|---|---|---|
| N-1 | Laptop scoring (deviation from PI-1111j) or host scoring on hc2 in a separate tree after the A-E3 decodes, using the label files already in `/root/vsps` | Laptop, as §4; one short run; a host run would put gold into an A-E3 work tree, against run document §7. Fact for the judge: the scorer's own header shows its `score` example with host paths (`NCS_DATA=/root/ncs-data … --results /root/ncs-data/results/xm3600`), so at least the original XM3600 scoring may have run on a host |
| N-5 | Tier and bar of the read of this note | One judge, REVERSIBLE, bar 85, as for the run document |
| N-2 | Annex B says "reference P/R/F1 against refs ∩ OIV7"; the scorer's `refs` block uses all lexicon classes, and its `oiv7` block the mapped classes | Use the scorer unchanged (the paper's existing measures) and name both blocks as they are |
| N-3 | B3: point differences only, or paired bootstrap intervals (needs new code) | Point differences only; no interval, no claim |
| N-4 | B5 needs a new 7b script | Write it after 7b decodes, with its own one-judge code read; no 7b row before then |
