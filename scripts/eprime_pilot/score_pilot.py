#!/usr/bin/env python3
"""Paper E' pilot (EXPLORATORY / DEV-PILOT, CC-098; not confirmatory): local CPU scoring and the GO / NO-GO rule.
Note: manuscript/prereg/2026-10-23_eprime_pilot/PILOT_NOTE.md.

  python scripts/eprime_pilot/score_pilot.py --selftest [--kit-b DIR]                          CPU, no data
  NCS_DATA=data python scripts/eprime_pilot/score_pilot.py score --runs-dir D --lists L --kit-b DIR \
      --xm-full F --labels OIV7 --desc CSV --out J                                              CPU, local only
Metrics per (model, set, arm) over the final Vietnamese caption, matcher v2 (rescap.chair.objects_in), Paper A's:
  KTVIC  gold = union of the image's references; P = micro tp / mentions; R = mean per-image recall over images with
         gold (scripts/object_prf.scores, exact match)
  XM     gold = OIV7 human labels through xm3600_oiv7 (local only): P = present / (present + absent) mapped mentions,
         R = mentioned / present pairs, both micro; images without a label add nothing
  F1 = 2PR/(P+R); object count = distinct classes per caption; CIDEr-D = Paper B's kit, final punctuation stripped.
Matched count = Paper A's matched prefix (score.cm): per image the first k = min(count_X, count_Y) distinct classes of each
caption. Paired image bootstrap, B = 2000, seed 0, one resample per set shared by models and arms. The output holds
numbers only.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / "scripts/c_stage2")]
import decode_pilot as DP  # noqa: E402  set manifests and file layout
import score as S  # noqa: E402  stage-1 scorer: kit(), JAR_SHA256, references()

S2, lb = DP.S2, DP.lb
B, SEED = 2000, 0
GAIN, CIDER_FLOOR = 2.0, -1.0  # CC-098: +2.0 object F1 points; CIDEr-D not below -1.0
ARMS = ("d", "t", "a")


# ------------------------------------------------------------------------------------------------ rows and F1
def distinct(text: str, extract) -> list[str]:
    return list(dict.fromkeys(extract(text)))


def rows_of(kind: str, ment: list[list[str]], ref: list, XO=None, classes: set | None = None) -> np.ndarray:
    """(n, 4): numerator and denominator of P, numerator and denominator of R per image. ref: gold sets (ktvic) or
    {class: status} dicts (xm)."""
    out = []
    for m, r in zip(ment, ref, strict=True):
        if kind == "ktvic":
            tp = len(set(m) & r)
            out.append((tp, len(m), tp / len(r) if r else 0.0, float(bool(r))))
        else:
            c = XO.caption_rows(set(m), r, set(), classes)  # [mapped, present, absent, ., ., present pairs, mentioned, ..]
            out.append((c[1], c[1] + c[2], c[6], c[5]))
    return np.array(out, float)


def f1(x: np.ndarray, idx: np.ndarray) -> np.ndarray:
    """x: (n, 4); idx: (draws, n) -> (draws,) F1 x 100."""
    s = x[idx].sum(1)
    p, r = s[:, 0] / np.maximum(s[:, 1], 1), s[:, 2] / np.maximum(s[:, 3], 1)
    return 100 * np.where(p + r > 0, 2 * p * r / np.maximum(p + r, 1e-12), 0.0)


def prefixes(a: list[list[str]], b: list[list[str]]) -> tuple[list, list]:
    k = [min(len(x), len(y)) for x, y in zip(a, b, strict=True)]
    return [x[:n] for x, n in zip(a, k)], [y[:n] for y, n in zip(b, k)]


# ------------------------------------------------------------------------------------------------ a cell
def cider_s(E4, PA, segment, refs: list[list[str]], hyps: dict[str, list[str]]) -> dict[str, np.ndarray]:
    """Per-image CIDEr-D x100, Paper B's kit, final punctuation stripped; df from the set's references."""
    texts = sorted({x for r in refs for x in r} | {c for h in hyps.values() for c in h})
    seg = dict(zip(texts, (s.lower() for s in segment(texts))))
    ids = [f"{n:06d}" for n in range(len(refs))]  # sorted order = image order
    cider = E4.Cider({i: [seg[x] for x in r] for i, r in zip(ids, refs)})
    return {a: cider.per_image({i: " ".join(PA.strip_trailing_punct_tokens(seg[c].split())) for i, c in zip(ids, h)})
            for a, h in hyps.items()}


def cell(kind: str, preds: dict, ref: list, refs_text: list, tools: dict) -> dict:
    """preds: {arm: [caption per image]} in a fixed image order. Returns the per-image arrays of one (model, set)."""
    ment = {a: [distinct(c, tools["extract"]) for c in preds[a]] for a in ARMS}
    kw = {"XO": tools.get("XO"), "classes": tools.get("classes")}
    x = {a: rows_of(kind, ment[a], ref, **kw) for a in ARMS}
    xm = {}
    for p, q in (("a", "d"), ("a", "t"), ("t", "d")):
        mp, mq = prefixes(ment[p], ment[q])
        xm[(p, q)] = (rows_of(kind, mp, ref, **kw), rows_of(kind, mq, ref, **kw))
    return {"x": x, "xm": xm, "count": {a: float(np.mean([len(m) for m in ment[a]])) for a in ARMS},
            "cider": cider_s(tools["E4"], tools["PA"], tools["segment"], refs_text, {a: preds[a] for a in ARMS})}


def point(x: np.ndarray) -> float:
    return float(f1(x, np.arange(len(x))[None])[0])


# ------------------------------------------------------------------------------------------------ statistics
def ci(d: np.ndarray) -> list[float]:
    return [round(float(v), 3) for v in np.percentile(d, [2.5, 97.5])]


def contrast(cells: dict, idx: dict, p: str, q: str, matched: bool = False) -> dict:
    """F1(p) - F1(q), points x100. cells: {(model, set): cell}; idx: {set: (B, n) resample}. Pooled = mean over the
    cells; by_model = mean over a model's sets."""
    draws, pts = {}, {}
    for (m, s), c in cells.items():
        xp, xq = c["xm"][(p, q)] if matched else (c["x"][p], c["x"][q])
        draws[m, s] = f1(xp, idx[s]) - f1(xq, idx[s])
        pts[m, s] = point(xp) - point(xq)
    pool = np.mean(list(draws.values()), axis=0)
    models = sorted({m for m, _s in cells})
    return {"d": round(float(np.mean(list(pts.values()))), 3), "ci95": ci(pool),
            "by_model": {m: round(float(np.mean([v for (mm, _s), v in pts.items() if mm == m])), 3) for m in models},
            "by_cell": {f"{m}|{s}": round(float(v), 3) for (m, s), v in pts.items()}}


def cider_contrast(cells: dict, idx: dict, p: str, q: str) -> dict:
    draws = [(c["cider"][p] - c["cider"][q])[idx[s]].mean(1) for (_m, s), c in cells.items()]
    pts = [float((c["cider"][p] - c["cider"][q]).mean()) for c in cells.values()]
    return {"d": round(float(np.mean(pts)), 3), "ci95": ci(np.mean(draws, axis=0))}


def decide(s: dict) -> dict:
    """CC-098's rule on the summary s (points x100):
    d, lo           pooled (A - D) object F1 and its 95% CI lower bound
    by_model        each model's (A - D) F1
    matched, m_lo   pooled (A - D) F1 on the matched prefix and its CI lower bound
    cider           pooled (A - D) CIDEr-D;  a_minus_t  pooled (A - T) F1
    GO: d >= 2.0, lo > 0, every model > 0, matched CI lower bound > 0, cider >= -1.0, a_minus_t >= 0.
    NO-GO: d <= 0 or the matched gain vanishes (matched <= 0). Anything else is INCONCLUSIVE (no spend, judge rules)."""
    checks = {"gain>=2.0": s["d"] >= GAIN, "ci_lo>0": s["lo"] > 0, "each_model>0": all(v > 0 for v in s["by_model"].values()),
              "matched_ci_lo>0": s["m_lo"] > 0, "cider>=-1.0": s["cider"] >= CIDER_FLOOR, "A>=T": s["a_minus_t"] >= 0}
    nogo = {"A<=D": s["d"] <= 0, "matched<=0": s["matched"] <= 0}
    verdict = "GO" if all(checks.values()) else "NO-GO" if any(nogo.values()) else "INCONCLUSIVE"
    return {"verdict": verdict, "go_checks": checks, "nogo_triggers": nogo}


# ------------------------------------------------------------------------------------------------ score (local)
def read_arm(runs_dir: Path, model: str, ds: str, arm: str, items: list) -> list[str]:
    d = json.loads((runs_dir / f"ep_{model}_{ds}-{arm}.preds.json").read_text(encoding="utf-8"))
    ok = (d.get("pilot_schema") == DP.SCHEMA and d["n_images"] == len(items) and d["max_new_tokens"] == 60
          and list(d["predictions"]) == [i for i, _f, _h in items]
          and all(d["image_sha256"][i] == h for i, _f, h in items))
    if not ok:
        raise SystemExit(f"{model} {ds} {arm}: not a pilot output of exactly this set")
    return [d["predictions"][i] for i, _f, _h in items]


def cmd_score(a) -> None:
    if os.environ.get("VSPS_MACHINE_ID"):
        raise SystemExit("scoring uses OIV7 labels and runs locally only; VSPS_MACHINE_ID is set")
    import xm3600_oiv7 as XO
    from rescap import chair as CH

    lists = DP.C.load_lists(a.lists)
    E4, PA = S.kit(a.kit_b)
    if lb.sha256_file(E4.VNC / "VnCoreNLP-1.2.jar") != S.JAR_SHA256:
        raise SystemExit("the VnCoreNLP jar is not the one of Paper B's protocol card")
    plan = {ds: DP.manifest(ds, lists) for ds in DP.SETS}
    ids = {ds: [i for i, _f, _h in rows] for ds, rows in plan.items()}
    kt = S.references("ktvic_dev299", lists)
    full = json.loads(Path(a.xm_full).read_text(encoding="utf-8"))
    xm: dict[str, list[str]] = {}
    for x in full["annotations"]:
        xm.setdefault(str(x["image_id"]), []).append(x["caption"])
    labels = json.loads(Path(a.labels).read_text(encoding="utf-8"))
    vmap = XO.resolve_map(a.desc)
    st = XO.statuses(vmap, {i: labels[i] for i in ids["xm_dev300"] if i in labels})
    refs = {"ktvic_dev299": [kt[i] for i in ids["ktvic_dev299"]], "xm_dev300": [xm[i] for i in ids["xm_dev300"]]}
    ref = {"ktvic_dev299": [CH._gold_objects(r) for r in refs["ktvic_dev299"]],
           "xm_dev300": [st.get(i, {}) for i in ids["xm_dev300"]]}
    tools = {"extract": CH.objects_in, "E4": E4, "PA": PA, "segment": E4.rdr, "XO": XO, "classes": set(vmap)}
    cells = {}
    for model in DP.MODELS:
        for ds, kind in (("ktvic_dev299", "ktvic"), ("xm_dev300", "xm")):
            preds = {arm: read_arm(a.runs_dir, model, ds, arm, plan[ds]) for arm in ARMS}
            cells[model, ds] = cell(kind, preds, ref[ds], refs[ds], tools)
    rng = np.random.default_rng(SEED)
    idx = {ds: rng.integers(0, len(ids[ds]), (B, len(ids[ds]))) for ds in DP.SETS}
    res = {f"{p}-{q}": {"f1": contrast(cells, idx, p, q), "f1_matched": contrast(cells, idx, p, q, True),
                       "cider_s": cider_contrast(cells, idx, p, q)} for p, q in (("a", "d"), ("a", "t"), ("t", "d"))}
    per_cell = {f"{m}|{s}": {arm: {"f1": round(point(c["x"][arm]), 3), "count": round(c["count"][arm], 3),
                                   "cider_s": round(float(c["cider"][arm].mean()), 3)} for arm in ARMS}
                for (m, s), c in cells.items()}
    ad = res["a-d"]
    summ = {"d": ad["f1"]["d"], "lo": ad["f1"]["ci95"][0], "by_model": ad["f1"]["by_model"],
            "matched": ad["f1_matched"]["d"], "m_lo": ad["f1_matched"]["ci95"][0], "cider": ad["cider_s"]["d"],
            "a_minus_t": res["a-t"]["f1"]["d"]}
    out = {"label": DP.LABEL, "draws": B, "seed": SEED, "n": {s: len(v) for s, v in ids.items()},
           "contrasts": res, "per_cell": per_cell, "summary": summ, "decision": decide(summ),
           "inputs": {"lists_sha256": lb.sha256_file(a.lists), "labels_sha256": lb.sha256_file(a.labels),
                      "runs_sha256": {p.name: lb.sha256_file(p) for p in sorted(Path(a.runs_dir).glob("ep_*.preds.json"))}}}
    Path(a.out).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"summary": summ, "decision": out["decision"]["verdict"]}))


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def selftest(kit_dir: Path) -> None:
    import xm3600_oiv7 as XO

    # rows and F1: KTVIC (gold sets) and XM (OIV7 statuses), synthetic class tokens
    kx = rows_of("ktvic", [["c1", "c2"], ["c3"], []], [{"c1"}, {"c3", "c4"}, set()])
    assert kx.tolist() == [[1, 2, 1.0, 1.0], [1, 1, 0.5, 1.0], [0, 0, 0.0, 0.0]]
    p, r = 2 / 3, 1.5 / 2
    assert abs(point(kx) - 100 * 2 * p * r / (p + r)) < 1e-9
    st = [{"c1": "present", "c2": "absent", "c3": "present"}, {}]
    xx = rows_of("xm", [["c1", "c2"], ["c1"]], st, XO, {"c1", "c2", "c3"})
    assert xx.tolist() == [[1, 2, 1, 2], [0, 0, 0, 0]], xx.tolist()
    # matched prefix: first k = min counts, in order of mention
    assert prefixes([["c1", "c2", "c3"], []], [["c4"], ["c5"]]) == ([["c1"], []], [["c4"], []])
    # a toy cell: arm a names the gold, d does not, t equals d; the same resample for every arm
    gold, n = [{"c1", "c2"}] * 40, 40
    ext = lambda t: t.split()  # noqa: E731  caption = class tokens
    E4, PA = S.kit(kit_dir)
    tools = {"extract": ext, "E4": E4, "PA": PA, "segment": lambda ts: ts}
    preds = {"a": [f"c1 c2 u{k}" for k in range(n)], "d": ["c1 c9"] * n, "t": ["c1 c9"] * n}
    c = cell("ktvic", preds, gold, [[f"c1 c2 u{k}", f"c1 u{k} w2"] for k in range(n)], tools)
    idx = {"s": np.random.default_rng(0).integers(0, n, (B, n))}
    cells = {("m1", "s"): c, ("m2", "s"): c}
    ad, tt, ad_m = (contrast(cells, idx, p_, q_, m) for p_, q_, m in (("a", "d", False), ("t", "d", False), ("a", "d", True)))
    assert ad["d"] > 20 and ad["ci95"][0] > 0 and ad_m["d"] > 20 and set(ad["by_model"]) == {"m1", "m2"}
    assert tt["d"] == 0 and tt["ci95"] == [0.0, 0.0] and c["count"] == {"a": 3.0, "d": 2.0, "t": 2.0}
    cc = cider_contrast(cells, idx, "a", "d")
    assert cc["d"] > 0 and c["cider"]["a"].shape == (n,)
    hy = cider_s(E4, PA, lambda ts: ts, [["c1 c2 ."]] * 2, {"x": ["c1 c2 .", "c1 c2"]})["x"]
    assert abs(hy[0] - hy[1]) < 1e-9, "final punctuation is stripped before CIDEr-D"
    # the rule: GO, each GO check failing alone, and the two NO-GO triggers
    good = {"d": 3.0, "lo": 0.5, "by_model": {"m1": 2.0, "m2": 4.0}, "matched": 2.5, "m_lo": 0.4, "cider": -0.5, "a_minus_t": 0.0}
    assert decide(good)["verdict"] == "GO"
    for k, v in {"d": 1.9, "lo": 0.0, "by_model": {"m1": 0.0, "m2": 5.0}, "m_lo": 0.0, "cider": -1.01, "a_minus_t": -0.01}.items():
        assert decide({**good, k: v})["verdict"] == "INCONCLUSIVE", k
    assert decide({**good, "d": 0.0, "lo": -1.0, "matched": 1.0})["verdict"] == "NO-GO", "(c) <= (a)"
    assert decide({**good, "matched": 0.0, "m_lo": -2.0})["verdict"] == "NO-GO", "gain vanishes at matched count"
    assert decide({**good, "d": 2.0})["verdict"] == "GO" and decide({**good, "cider": -1.0})["verdict"] == "GO", "boundaries"
    print("selftest ok: object rows (KTVIC, OIV7), matched prefix, paired bootstrap, stripped CIDEr-D, GO/NO-GO rule")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--kit-b", type=Path, default=HERE.parents[1] / "scripts/kit_b")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("score")
    p.add_argument("--runs-dir", type=Path, required=True)
    p.add_argument("--lists", type=Path, required=True)
    p.add_argument("--xm-full", type=Path, required=True, help="datasets/xm3600/full_data.json (references)")
    p.add_argument("--labels", type=Path, required=True, help="data/xm3600/oiv7_labels.json (local)")
    p.add_argument("--desc", type=Path, required=True, help="oidv7-class-descriptions.csv")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--kit-b", type=Path, default=argparse.SUPPRESS)
    a = ap.parse_args()
    if a.selftest:
        return selftest(a.kit_b)
    if a.cmd != "score":
        ap.error("score or --selftest")
    cmd_score(a)


if __name__ == "__main__":
    main()
