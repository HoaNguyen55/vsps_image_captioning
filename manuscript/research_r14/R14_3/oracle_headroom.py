#!/usr/bin/env python
"""R14-3 oracle headroom on KTVIC dev300 (CPU only). Pool per image = P1_dev greedy + 6 T0.5 + 6 T0.8 samples.

Ceilings for any reranker over this pool: per-image oracle by CIDEr-D, by object F1, count-matched (|M| = greedy's)
precision oracle, and split-reference oracles (select on refs 0-2 / panel-independent, score on refs 3-4 / panel).
Writes numbers only. Run: nice -n 19 python3 manuscript/research_r14/R14_3/oracle_headroom.py
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import random
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from object_prf import image_counts, scores  # noqa: E402
from rescap.chair import chair, objects_in  # noqa: E402
from rl_reward import CiderD  # noqa: E402

OUT = Path(__file__).with_name("oracle_headroom.json")
GREEDY = ROOT / "data/results/rl/p1dev_s42-dev300-short.preds.json"
SAMPLES = {"T0.5": ROOT / "data/results/upe/p1dev_s42-dev300-short-T0.5.jsonl",
           "T0.8": ROOT / "data/results/upe/p1dev_s42-dev300-short-T0.8.jsonl"}
EXACT = lambda c: {c}  # noqa: E731


def rdr():
    os.environ["PATH"] = f"/home/hoanguyen/jdk21/bin:{os.environ.get('PATH', '')}"
    spec = importlib.util.spec_from_file_location("e4", ROOT / ".session_backup/2026-10-14/research_r10/E4/protocol_pilot.py")
    e4 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(e4)
    e4.VNC = ROOT / ".session_backup/machines/n2/ncs-data/vncorenlp"
    return lambda texts: [s.lower().split() for s in e4.rdr(texts)]


def cls(t: str) -> frozenset:
    return frozenset(objects_in(t))


def main() -> None:
    ids = sorted((ROOT / "data/splits/ktvic_dev300.txt").read_text().split())
    tr = json.loads((ROOT / "data/datasets/ktvic/train_data.json").read_text(encoding="utf-8"))
    refs: dict[str, list[str]] = {}
    for a in tr["annotations"]:
        if str(a["image_id"]) in set(ids) and a.get("caption"):
            refs.setdefault(str(a["image_id"]), []).append(a["caption"])
    panel = json.loads((ROOT / "data/ktvic_openviic_refs.json").read_text(encoding="utf-8"))["train"]
    g = {str(k): (v[0] if isinstance(v, list) else v) for k, v in json.loads(GREEDY.read_text(encoding="utf-8")).items()}
    smp = {T: {str(r["image_id"]): r["samples"] for r in map(json.loads, p.read_text(encoding="utf-8").splitlines())}
           for T, p in SAMPLES.items()}
    pool = [[g[i]] + smp["T0.5"][i] + smp["T0.8"][i] for i in ids]
    N, K = len(ids), len(pool[0])
    assert N == 300 and K == 13 and all(len(refs[i]) == 5 for i in ids)

    tok = rdr()
    flat = tok([c for row in pool for c in row] + [r for i in ids for r in refs[i]])
    ptok = [flat[n * K:(n + 1) * K] for n in range(N)]
    it = iter(flat[N * K:])
    rtok = [[next(it) for _ in range(5)] for _ in ids]

    def cider(sub):  # (N, K) CIDEr-D x100 against refs[sub], DF from those refs
        cd = CiderD([[r[j] for j in sub] for r in rtok])
        return np.array([[100 * cd.score(ptok[n][k], [rtok[n][j] for j in sub]) for k in range(K)] for n in range(N)])
    C = {"all5": cider(range(5)), "A012": cider([0, 1, 2]), "B34": cider([3, 4]), "A234": cider([2, 3, 4]),
         "B01": cider([0, 1])}

    pc = [[cls(c) for c in row] for row in pool]
    gold = {"ktvic5": [frozenset().union(*map(cls, refs[i])) for i in ids],
            "A012": [frozenset().union(*map(cls, refs[i][:3])) for i in ids],
            "B34": [frozenset().union(*map(cls, refs[i][3:])) for i in ids]}
    pos = [n for n, i in enumerate(ids) if panel.get(i)]
    gold["panel"] = [frozenset().union(*map(cls, panel[i])) if panel.get(i) else frozenset() for i in ids]
    rows = {k: [[image_counts(set(pc[n][j]), set(gv[n]), EXACT) for j in range(K)] for n in range(N)]
            for k, gv in gold.items()}
    hall = np.zeros((N, K)); ment = np.zeros((N, K))
    for j in range(K):
        res = chair({i: pool[n][j] for n, i in enumerate(ids)}, refs, strict_ids=False)
        by = {str(d["image_id"]): d for d in res.per_caption}
        for n, i in enumerate(ids):
            ment[n, j], hall[n, j] = by[i]["n_mentions"], len(by[i]["hallucinated"])

    def f1_img(r):
        tp, m, _, rec, _, _ = r
        p = tp / m if m else 0.0
        rec = 0.0 if rec != rec else rec
        return 2 * p * rec / (p + rec) if p + rec else 0.0

    def summary(pick, cand=range(K)):
        a = np.arange(N)
        out = {"cider_all5": float(C["all5"][a, pick].mean()),
               "chair_i": float(100 * hall[a, pick].sum() / max(ment[a, pick].sum(), 1)),
               "classes_per_cap": float(np.mean([len(pc[n][pick[n]]) for n in range(N)]))}
        for gk in ("ktvic5", "panel"):
            idx = range(N) if gk == "ktvic5" else pos
            s = scores([rows[gk][n][pick[n]] for n in idx])
            out[f"P_{gk}"], out[f"R_{gk}"], out[f"F1_{gk}"] = s["P"], s["R"], s["F1"]
        return {k: round(v, 3) for k, v in out.items()}

    res = {"inputs": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()[:16] for p in [GREEDY, *SAMPLES.values()]},
           "n_images": N, "n_panel_images": len(pos), "pools": {}}
    for name, cand in {"N7_T0.5": list(range(7)), "N7_T0.8": [0] + list(range(7, 13)), "N13": list(range(13))}.items():
        cand = np.array(cand)
        greedy = np.zeros(N, int)

        def best(score):  # argmax over cand, ties to the earliest (greedy first)
            return cand[np.argmax(score[:, cand], axis=1)]
        f1k = np.array([[f1_img(rows["ktvic5"][n][j]) for j in range(K)] for n in range(N)])
        f1a = np.array([[f1_img(rows["A012"][n][j]) for j in range(K)] for n in range(N)])
        same = np.array([[len(pc[n][j]) == len(pc[n][0]) for j in range(K)] for n in range(N)])
        tp_same = np.where(same, np.array([[rows["ktvic5"][n][j][0] for j in range(K)] for n in range(N)]), -1)
        tpa_same = np.where(same, np.array([[rows["A012"][n][j][0] for j in range(K)] for n in range(N)]), -1)
        rng = random.Random(0)
        rand = [summary(np.array([rng.choice(cand) for _ in range(N)])) for _ in range(50)]
        r = {"greedy": summary(greedy),
             "random_mean50": {k: round(float(np.mean([d[k] for d in rand])), 3) for k in rand[0]},
             "oracle_cider_all5": summary(best(C["all5"])),
             "oracle_f1_ktvic5": summary(best(f1k)),
             "oracle_tp_count_matched": summary(best(tp_same)),
             "oracle_f1_selectA012": summary(best(f1a)),
             "oracle_tpA012_count_matched": summary(best(tpa_same))}
        a = np.arange(N)
        for sel, ev in (("A012", "B34"), ("A234", "B01")):
            pk = best(C[sel])
            r[f"split_cider_select{sel}_eval{ev}"] = {
                "greedy": round(float(C[ev][a, 0].mean()), 3), "oracle": round(float(C[ev][a, pk].mean()), 3),
                "same_refs_oracle": round(float(C[sel][a, pk].mean() - C[sel][a, 0].mean()), 3)}
        r["oracle_f1_selectA012_evalB34"] = {
            "greedy": round(scores([rows["B34"][n][0] for n in range(N)])["F1"], 3),
            "oracle": round(scores([rows["B34"][n][best(f1a)[n]] for n in range(N)])["F1"], 3),
            "oracle_count_matched_tpA012": round(scores([rows["B34"][n][best(tpa_same)[n]] for n in range(N)])["F1"], 3)}
        res["pools"][name] = r
        OUT.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
