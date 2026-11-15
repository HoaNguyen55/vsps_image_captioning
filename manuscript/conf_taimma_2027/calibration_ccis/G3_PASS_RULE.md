# Gate G3: pass rule and aggregation

**Status: confirmed by CC-424 (CONDITIONAL GO 87) with the texts of its Annex A; fixed from the LOG pin line of CC-424 ruling 3.** Written 2026-11-15, before any card was scored. Coordinator file; not for scorers.

## Rule (as the coordinator's plan states it)

Source: `manuscript/KE_HOACH_GOAL_2026-11-15.md` l.86 (task 4, G3): three blind scorers score our card with the five CCIS reference cards, no web search; expected: our score at least the median of the five reference cards on T1, T5 and T6.

Written out:

1. For each card c (X1 … X6) and criterion t, the card value v(c, t) is the median of the three scorers' integer scores.
2. For t in {T1, T5, T6}, the reference value ref(t) is the median of v(c, t) over the five reference cards (`SHUFFLE_KEY_DO_NOT_SHOW_SCORERS.md` says which five).
3. Line A: v(ours, t) ≥ ref(t) for T1 **and** T5 **and** T6. A tie passes.
4. Line B (the investigator's rule of 10 Nov, PI-1110r: the paper's mean at or above the mean of the venue's papers): 5 × S(ours) ≥ the sum of S(c) over the five reference cards, where S(c) is the sum of v(c, t) over T1 to T7. This is the comparison of the two means in whole numbers. A tie passes.
5. **G3 PASS** if line A **and** line B hold. Otherwise **G3 FAIL**, with the failing line and criteria named.
6. One run. The verdict from the first three valid TSVs is the verdict of record. From the LOG pin line on, no card, brief, rubric, key, reference set or rule changes, and no second scoring is run on this paper text. A FAIL goes to the principal investigator with the full table. A new run needs a changed paper text, a new judge ruling and three fresh scorers, and the first verdict stays in the notice.

Every v and ref is an integer (median of three integers; median of five integers), so no tie-break is needed.

## Validity of the inputs

- One TSV per scorer at `scores/S1.tsv`, `scores/S2.tsv`, `scores/S3.tsv`, in the format of `SCORER_BRIEF.md`: the exact header, 48 rows, each (card, criterion) pair once, integer scores 0–5.
- A scorer is void on one of three grounds only: (i) the TSV is missing or fails the format lines of the code below (header, 49 rows, the 48 pairs, integers 0–5); (ii) the scorer's final reply or tool record shows a read of a file other than the six blind copies, the brief and the rubric; (iii) a reason field or the final reply states which card is whose. A score value is never a ground. Every void is written to the LOG with its ground before the aggregation code is run for the first time. A void TSV is kept as `scores/<id>.void.tsv`. The slot is re-run once, by a fresh scorer, on the same brief and order. A second void in the same slot stops the gate (reported as "G3 not decided", to the principal investigator). No aggregation from fewer than three valid TSVs.
- Scores are read as written; none is edited, dropped or re-scored after the TSVs exist.

## Aggregation (reference code; run from `calibration_ccis/` after the six blind copies exist)

```
python3 -I -c "
import csv, statistics as st
key = {'X1':'R2','X2':'R5','X3':'OURS','X4':'R4','X5':'R1','X6':'R3'}
T = ['T%d' % i for i in range(1, 9)]
s = {}
for f in ('S1','S2','S3'):
    rows = list(csv.reader(open('scores/%s.tsv' % f, encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE))
    assert rows[0] == ['scorer_id','card_id','criterion','score','reason'] and len(rows) == 49, f
    got = {(r[1], r[2]): int(r[3]) for r in rows[1:]}
    assert set(got) == {(x, t) for x in key for t in T} and all(0 <= v <= 5 for v in got.values()), f
    for k, v in got.items(): s.setdefault(k, []).append(v)
v = {k: st.median(x) for k, x in s.items()}
ours = [x for x in key if key[x] == 'OURS'][0]
res = {}
for t in ('T1','T5','T6'):
    ref = st.median(v[(x, t)] for x in key if x != ours)
    res[t] = (v[(ours, t)], ref, v[(ours, t)] >= ref)
    print(t, 'ours', v[(ours, t)], 'ref', ref, 'pass' if res[t][2] else 'FAIL')
S = {x: sum(v[(x, t)] for t in T[:7]) for x in key}
refsum = sum(S[x] for x in key if x != ours)
B = 5 * S[ours] >= refsum
print('B', 'ours x5', 5 * S[ours], 'refsum', refsum, 'pass' if B else 'FAIL')
print('G3', 'PASS' if B and all(r[2] for r in res.values()) else 'FAIL')
for x in key: print(key[x], [v[(x, t)] for t in T])
"
```

## Reported beside the verdict (descriptive only, no gate)

- v(c, t) for all six cards and T1–T8; the three raw scores of our card on T1, T5, T6.
- Mean of v over T1–T7 per card (the input of line B). T8 is outside every mean and outside G3: all six cards name the same venue class.
- In the notice, beside the verdict: the scoring was blind to the labels only. The rubric text and the content of our card (the only preregistered study and the only Vietnamese captioning study in the set) let a scorer infer which card is the group's; the rubric's T1, T3 and T6 lines name preregistration and the one look, which only our card has, so line A on T6 separates little. The reference set is five CCIS chapters read as open preprints (`REFERENCE_SET_NOTES.md` section 4).
- The addendum's Q2 line (T1, T5, T6 ≥ 3 and mean ≥ 2.9) is a different rule and is not part of G3; it may be printed as a descriptive line only.

## Points for the judge to confirm before scoring

1. **The rule itself** as written in 1–3 above, including "ties pass" and "all three criteria".
2. **Instrument.** The brief uses the verbatim copy of rubric sections 1–2 used for the blind scoring of 2026-11-13 (`directions/calibration_2026-11-13_A_phaseB/RUBRIC_T1-T8_AND_ANCHORS.md`, sha 572c2988…), so section 4 of the full rubric (earlier scores of the group's papers) is not shown. That copy is in Vietnamese and keeps two group-specific lines a scorer could use to guess our card: T3 names "COCO, Flickr30K, NoCaps, XM3600-en", and T1 asks why Vietnamese is a necessary case. It also keeps the T6 line on overlap wording that PI-1110n replaced. Options: keep it for comparability with 11-10 and 11-13 (recommended default), or make a copy with those three lines neutralised, which changes the instrument.
3. **Tells on our card that cannot be removed without misdescribing the paper:** it is the only card with a preregistration, PASS/FAIL labels and registered sensitivities; it is longer than the reference cards (paper card about 780 words against 567–633).
4. **Card version.** Our card is provisional; scoring waits for the card rebuilt from the paper text of record under CC-424 ruling 3, its sha recorded in the shuffle key.
5. **Scorers.** Three fresh scorers, as the plan states; none has read the draft, the plan files or the reference notes.
