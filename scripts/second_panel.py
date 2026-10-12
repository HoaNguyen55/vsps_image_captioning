#!/usr/bin/env python
"""A second, independent human panel on KTVIC test: the UIT-OpenViIC captions of the same images.

    NCS_DATA=data python scripts/second_panel.py                      # -> data/results/second_panel.json
    NCS_DATA=data python scripts/second_panel.py --B 5000 --pairs p1-gold:fuse2_s42 p1_s43:fuse2_s42

KTVIC's images come from the UIT image pool that UIT-OpenViIC also captioned, with a different annotator
team and guideline (scripts/match_openviic.py -> data/ktvic_openviic_refs.json). On the matched test images,
with object_prf.py's image_counts/scores (exact match, and the CHAIR-vi hypernym credit P_h / R_spec):

  prf      every system and mode against (a) the 5 KTVIC refs, (b) the OpenViIC panel only, (c) their union.
  confirm  a mention no KTVIC reference names is "KTVIC-reference-false" (exact: not a KTVIC class;
           hypernym: not a KTVIC class or an ancestor of one); its share that the OpenViIC panel names
           (exact / hypernym-credited), the reference-false and the unconfirmed mentions per caption.
  human    1v4 calibration, as human_parity.py: each KTVIC caption against the other 4 (5 folds, fold
           average), the systems against the same 4. A held-out human's reference-false mentions are
           real objects (and lexical variants) the 4 left out, so the share of them the OpenViIC panel
           names is its sensitivity; system share / human share estimates the real fraction of a
           system's reference-false mentions (a lower bound if the panel misses system-only objects more).
  capture  two-panel capture-recapture over each image's mentioned classes (KTVIC panel = capture 1,
           OpenViIC panel = capture 2): Lincoln-Petersen N1*N2/M and Chapman (N1+1)(N2+1)/(M+1)-1 pooled
           over images, and the mean per-image Chapman; mentionable classes per image and each panel's
           recall n/N. Fine = lexicon classes, coarse = their root hypernym (người, phương tiện, ...).
           Salience makes the panels positively dependent, so N is under- and recall over-estimated.

95% percentile CIs resample images (B draws shared by every statistic, so paired differences use the
same images); paired p is two-sided, floored at 2/B, as object_prf.paired.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from object_prf import image_counts, scores  # noqa: E402
from rescap.chair import _ancestors, objects_in  # noqa: E402

RESULTS = ROOT / "data" / "results"
SYSTEMS = ("p1-gold", "p1_s43", "p1_s44", "fuse2_s42", "tags_fuse2_s42", "e5_s42", "e5dpo_s42", "zeroshot")
MODES = ("short", "detailed")
GOLDS = ("ktvic", "openviic", "union")
KEYS = ("P", "R", "F1", "P_h", "R_spec", "F1_spec")


def objs(text: str) -> frozenset[str]:
    return frozenset(objects_in(text))


def anc(classes) -> set[str]:
    return set().union(*(_ancestors(c) for c in classes)) if classes else set()


def root(c: str) -> str:
    """The most general class above c (HYPERNYMS chain end), for the coarse capture-recapture."""
    return max(_ancestors(c), key=lambda a: len(_ancestors(a)) == 1 and a != c) if len(_ancestors(c)) > 1 else c


def ref_false(m, gold, panel) -> tuple[int, int, int, int]:
    """(reference-false, of which the panel names; same two under the hypernym credit) for one caption."""
    rf = m - gold
    rf_h = {x for x in m if x not in anc(gold)}
    return len(rf), len(rf & panel), len(rf_h), sum(x in anc(panel) for x in rf_h)


def prf_arrays(rows: list[tuple], idx: np.ndarray) -> dict[str, np.ndarray]:
    """object_prf.scores over the resampled images idx (B, n), vectorised: {key: (B,) array}."""
    a = np.asarray(rows, dtype=float)
    out = {}

    def rec(col):
        v = a[:, col][idx]
        ok = ~np.isnan(v)
        return 100 * np.where(ok, v, 0).sum(1) / np.maximum(ok.sum(1), 1)

    m = np.maximum(a[:, 1][idx].sum(1), 1e-9)
    for p_key, tp_col, r_key, r_col, f_key in (("P", 0, "R", 3, "F1"), ("P_h", 2, "R_spec", 4, "F1_spec")):
        p, r = 100 * a[:, tp_col][idx].sum(1) / m, rec(r_col)
        out[p_key], out[r_key], out[f_key] = p, r, np.where(p + r > 0, 2 * p * r / np.maximum(p + r, 1e-9), 0)
    return out


def ratio(num: np.ndarray, den: np.ndarray, idx: np.ndarray) -> np.ndarray:
    return 100 * num[idx].sum(-1) / np.maximum(den[idx].sum(-1), 1e-9)


def ci(v: np.ndarray) -> list[float]:
    return [round(float(np.percentile(v, 2.5)), 2), round(float(np.percentile(v, 97.5)), 2)]


def delta(a: np.ndarray, b: np.ndarray, pa: float, pb: float) -> dict:
    """b - a on shared draws: point (from the full sample), CI, two-sided p floored at 2/B."""
    d = b - a
    p = min(1.0, 2 * min((d <= 0).mean(), (d >= 0).mean()))
    return {"d": round(pb - pa, 2), "ci95": ci(d), "p": round(max(p, 2 / len(d)), 4)}


def load_preds(stem: str, ids: list[str]) -> dict[str, str] | None:
    f = RESULTS / f"{stem}.preds.json"
    if not f.exists():
        return None
    raw = json.loads(f.read_text(encoding="utf-8"))
    preds = {str(k): (v[0] if isinstance(v, list) else v) or "" for k, v in raw.items()}
    missing = set(ids) - preds.keys()
    if missing:
        sys.exit(f"{f}: no caption for {len(missing)} matched images (e.g. {sorted(missing)[:3]})")
    return preds


def analyse(ktvic: dict[str, list[str]], panel: dict[str, list[str]], systems: dict[str, dict[str, str]],
            pairs: list[tuple[str, str]], B: int, seed: int = 0) -> dict:
    ids = sorted(ktvic.keys() & panel.keys(), key=lambda x: (len(x), x))
    n = len(ids)
    gk = [frozenset().union(*(objs(c) for c in ktvic[i])) for i in ids]
    go = [frozenset().union(*(objs(c) for c in panel[i])) for i in ids]
    gold = {"ktvic": gk, "openviic": go, "union": [a | b for a, b in zip(gk, go)]}
    idx = np.random.default_rng(seed).integers(0, n, size=(B, n))
    out = {"n_images": n, "B": B, "seed": seed,
           "panel_sizes": {"ktvic_captions_per_image": float(np.mean([len(ktvic[i]) for i in ids])),
                           "openviic_captions_per_image": float(np.mean([len(panel[i]) for i in ids])),
                           "ktvic_classes_per_image": float(np.mean([len(g) for g in gk])),
                           "openviic_classes_per_image": float(np.mean([len(g) for g in go])),
                           "union_classes_per_image": float(np.mean([len(a | b) for a, b in zip(gk, go)]))}}
    mentions = {name: [objs(preds[i]) for i in ids] for name, preds in systems.items()}

    # (1) P/R/F1 against each gold
    draws, points = {}, {}
    out["prf"] = {g: {} for g in GOLDS}
    for g in GOLDS:
        for name, ms in mentions.items():
            rows = [image_counts(set(m), set(t), _ancestors) for m, t in zip(ms, gold[g])]
            points[g, name], draws[g, name] = scores(rows), prf_arrays(rows, idx)
            out["prf"][g][name] = {**{k: round(points[g, name][k], 2) for k in KEYS},
                                   "ci95": {k: ci(draws[g, name][k]) for k in ("P", "R", "F1")}}

    # (2) KTVIC-reference-false mentions the OpenViIC panel names
    conf_draws, conf_points = {}, {}
    out["confirm"] = {}
    for name, ms in mentions.items():
        c = np.array([ref_false(m, t, p) for m, t, p in zip(ms, gk, go)], dtype=float)
        full = np.arange(n)[None]
        row = {}
        for tag, a, b in (("exact", 0, 1), ("hypernym", 2, 3)):
            share = ratio(c[:, b], c[:, a], idx)
            conf_draws[tag, name] = {"share": share, "rf": c[:, a][idx].mean(1), "confirmed": c[:, b][idx].mean(1),
                                     "unconfirmed": (c[:, a] - c[:, b])[idx].mean(1)}
            conf_points[tag, name] = {"share": float(ratio(c[:, b], c[:, a], full)[0]), "rf": c[:, a].mean(),
                                      "confirmed": c[:, b].mean(), "unconfirmed": (c[:, a] - c[:, b]).mean()}
            row[tag] = {"ref_false_per_caption": round(c[:, a].mean(), 3), "confirmed_per_caption": round(c[:, b].mean(), 3),
                        "unconfirmed_per_caption": round((c[:, a] - c[:, b]).mean(), 3),
                        "confirmed_share": round(conf_points[tag, name]["share"], 2),
                        "ci95": {"confirmed_share": ci(share), "ref_false_per_caption": ci(conf_draws[tag, name]["rf"]),
                                 "unconfirmed_per_caption": ci(conf_draws[tag, name]["unconfirmed"])}}
        out["confirm"][name] = row

    # paired differences (b - a) on the same images
    out["paired"] = {}
    for a, b in pairs:
        for mode in MODES:
            sa, sb = f"{a}-{mode}", f"{b}-{mode}"
            if sa not in mentions or sb not in mentions:
                continue
            d = {f"{k}_vs_{g}": delta(draws[g, sa][k], draws[g, sb][k], points[g, sa][k], points[g, sb][k])
                 for g in GOLDS for k in ("P", "R", "F1")}
            for tag in ("exact", "hypernym"):
                for k in ("share", "rf", "confirmed", "unconfirmed"):
                    d[f"confirm_{tag}_{k}"] = delta(conf_draws[tag, sa][k], conf_draws[tag, sb][k],
                                                    conf_points[tag, sa][k], conf_points[tag, sb][k])
            out["paired"][f"{sb} - {sa}"] = d

    out["human_1v4"] = human_1v4(ktvic, ids, go, mentions, idx)
    out["capture"] = capture(gk, go, mentions, gold["union"], idx)
    return out


def human_1v4(ktvic: dict[str, list[str]], ids: list[str], go: list[frozenset], mentions: dict, idx: np.ndarray) -> dict:
    """Fold-averaged (5 folds: caption k held out, gold = the other 4): P/R/F1 vs the 4 and vs the 4 + OpenViIC
    panel, and the share of reference-false mentions the OpenViIC panel names, for the held-out human and
    every system scored against the same 4."""
    n_folds = min(len(ktvic[i]) for i in ids)
    caps = [[objs(c) for c in ktvic[i][:n_folds]] for i in ids]
    rest = [[frozenset().union(*(cs[j] for j in range(n_folds) if j != k)) for k in range(n_folds)] for cs in caps]
    who = {"human": [[cs[k] for k in range(n_folds)] for cs in caps]}
    who.update({name: [[m] * n_folds for m in ms] for name, ms in mentions.items()})
    out = {"folds": n_folds, "gold": "union of the other KTVIC captions (+ the OpenViIC panel for *_plus_openviic)"}
    shares, prf_pt, prf_dr = {}, {}, {}
    for name, per_img in who.items():
        rec = {}
        for gname, extra in (("vs_4", False), ("vs_4_plus_openviic", True)):
            fold_draws, fold_pts = [], []
            for k in range(n_folds):
                rows = [image_counts(set(per_img[i][k]), set(rest[i][k] | (go[i] if extra else frozenset())), _ancestors)
                        for i in range(len(ids))]
                fold_pts.append(scores(rows))
                fold_draws.append(prf_arrays(rows, idx))
            prf_pt[name, gname] = {kk: float(np.mean([p[kk] for p in fold_pts])) for kk in ("P", "R", "F1")}
            prf_dr[name, gname] = {kk: np.mean([d[kk] for d in fold_draws], axis=0) for kk in ("P", "R", "F1")}
            rec[gname] = {kk: round(v, 2) for kk, v in prf_pt[name, gname].items()}
            rec[gname]["ci95"] = {kk: ci(v) for kk, v in prf_dr[name, gname].items()}
        c = np.array([[ref_false(per_img[i][k], rest[i][k], go[i]) for k in range(n_folds)] for i in range(len(ids))],
                     dtype=float)  # (n, folds, 4)
        for tag, a, b in (("exact", 0, 1), ("hypernym", 2, 3)):
            draw = np.mean([ratio(c[:, k, b], c[:, k, a], idx) for k in range(n_folds)], axis=0)
            point = float(np.mean([100 * c[:, k, b].sum() / max(c[:, k, a].sum(), 1e-9) for k in range(n_folds)]))
            shares[tag, name] = (point, draw)
            rec[f"confirm_{tag}"] = {"ref_false_per_caption": round(float(c[:, :, a].mean()), 3),
                                     "confirmed_share": round(point, 2), "ci95": ci(draw)}
        out[name] = rec
    for name in who:
        if name == "human":
            continue
        for gname in ("vs_4", "vs_4_plus_openviic"):
            out[name][gname]["delta_vs_human"] = {
                kk: delta(prf_dr["human", gname][kk], prf_dr[name, gname][kk], prf_pt["human", gname][kk],
                          prf_pt[name, gname][kk]) for kk in ("P", "R", "F1")}
        for tag in ("exact", "hypernym"):
            (ps, ds), (ph, dh) = shares[tag, name], shares[tag, "human"]
            out[name][f"confirm_{tag}"]["real_fraction_est"] = {
                "point": round(100 * ps / ph, 1) if ph else None, "ci95": ci(100 * ds / np.maximum(dh, 1e-9))}
    return out


def capture(gk: list[frozenset], go: list[frozenset], mentions: dict, union: list[frozenset], idx: np.ndarray) -> dict:
    out = {}
    for level, f in (("fine", lambda s: s), ("coarse", lambda s: frozenset(root(c) for c in s))):
        k, o = [f(s) for s in gk], [f(s) for s in go]
        n1 = np.array([len(s) for s in k], float)
        n2 = np.array([len(s) for s in o], float)
        m = np.array([len(a & b) for a, b in zip(k, o)], float)
        nu = np.array([len(a | b) for a, b in zip(k, o)], float)

        def est(ix):
            N1, N2, M, n = n1[ix].sum(-1), n2[ix].sum(-1), m[ix].sum(-1), ix.shape[-1]
            lp = N1 * N2 / np.maximum(M, 1e-9) / n
            chap = ((N1 + 1) * (N2 + 1) / (M + 1) - 1) / n
            per = ((n1[ix] + 1) * (n2[ix] + 1) / (m[ix] + 1) - 1).mean(-1)
            return {"N_lincoln_petersen": lp, "N_chapman": chap, "N_chapman_per_image_mean": per,
                    "recall_ktvic_panel": 100 * N1 / n / chap, "recall_openviic_panel": 100 * N2 / n / chap,
                    "recall_union": 100 * nu[ix].sum(-1) / n / chap}

        full, draws = est(np.arange(len(k))[None]), est(idx)
        res = {key: {"point": round(float(full[key][0]), 3), "ci95": ci(draws[key])} for key in full}
        res["per_image"] = {"n_ktvic": float(n1.mean()), "n_openviic": float(n2.mean()), "both": float(m.mean()),
                            "union": float(nu.mean())}
        if level == "fine":  # a system's mentions confirmed by either panel, over the estimated mentionable classes
            n_chap = (n1.sum() + 1) * (n2.sum() + 1) / (m.sum() + 1) - 1
            res["system_recall_lower_bound"] = {
                name: round(100 * sum(len(a & u) for a, u in zip(ms, union)) / n_chap, 2) for name, ms in mentions.items()}
        out[level] = res
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--refs", default=str(ROOT / "data" / "ktvic_openviic_refs.json"))
    ap.add_argument("--split", default="test")
    ap.add_argument("--systems", nargs="+", default=list(SYSTEMS))
    ap.add_argument("--pairs", nargs="+", default=["p1-gold:fuse2_s42", "p1-gold:tags_fuse2_s42", "p1_s43:fuse2_s42",
                                                   "p1_s44:fuse2_s42", "zeroshot:fuse2_s42"],
                    help="A:B system stems; B - A is reported in both modes")
    ap.add_argument("--B", type=int, default=2000)
    ap.add_argument("--out", default=str(RESULTS / "second_panel.json"))
    args = ap.parse_args()

    from evaluate import references

    ktvic = references(f"{args.split}_data.json")
    panel = json.loads(Path(args.refs).read_text(encoding="utf-8"))[args.split]
    ids = sorted(ktvic.keys() & panel.keys())
    systems = {}
    for s in args.systems:
        for mode in MODES:
            preds = load_preds(f"{s}-{mode}", ids)
            if preds is None:
                print(f"  no {s}-{mode}.preds.json: skipped")
            else:
                systems[f"{s}-{mode}"] = preds
    res = analyse(ktvic, panel, systems, [tuple(p.split(":")) for p in args.pairs], args.B)
    res = {"what": "KTVIC test, matched images: systems vs KTVIC refs, the OpenViIC panel, their union "
                   "(scripts/second_panel.py)", "refs_file": str(Path(args.refs).relative_to(ROOT))
           if Path(args.refs).is_relative_to(ROOT) else args.refs, "split": args.split, **res}
    report(res)
    Path(args.out).write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"-> {args.out}")
    return 0


def report(res: dict) -> None:
    print(f"{res['n_images']} matched images; panels: {res['panel_sizes']}")
    for name in res["prf"]["ktvic"]:
        print(f"  {name:26s} " + "  ".join(
            f"{g[:4]} P={res['prf'][g][name]['P']:5.1f} R={res['prf'][g][name]['R']:5.1f} F1={res['prf'][g][name]['F1']:5.1f}"
            for g in GOLDS) + "  | ref-false/cap {:.2f}, confirmed {:.1f}% {}".format(
            res["confirm"][name]["exact"]["ref_false_per_caption"], res["confirm"][name]["exact"]["confirmed_share"],
            res["confirm"][name]["exact"]["ci95"]["confirmed_share"]))
    for key, d in res["paired"].items():
        print(f"  {key:40s} " + "  ".join(f"{k}={v['d']:+.1f} {v['ci95']} p={v['p']}" for k, v in d.items()
                                         if k in ("P_vs_ktvic", "P_vs_union", "confirm_exact_share", "confirm_exact_unconfirmed")))
    h = res["human_1v4"]
    print(f"  1v4 human: {h['human']['vs_4']}  confirmed {h['human']['confirm_exact']}")
    for name in res["prf"]["ktvic"]:
        print(f"  1v4 {name:22s} {h[name]['confirm_exact']}")
    for level, c in res["capture"].items():
        print(f"  capture ({level}): " + ", ".join(f"{k}={v['point']} {v['ci95']}" for k, v in c.items() if isinstance(v, dict) and "point" in v))


def _check() -> None:
    assert ref_false({"người", "chó", "xe máy"}, {"phụ nữ", "chó"}, {"người", "xe máy"}) == (2, 2, 1, 1)
    assert ref_false({"chó"}, {"chó"}, set()) == (0, 0, 0, 0)
    assert root("phụ nữ") == "người" and root("xe máy") == "phương tiện" and root("chó") == "động vật" and root("bàn") == "đồ đạc"
    assert root("cây") == "cây"
    rows = [(1, 2, 1, 0.5, 0.5, 1.0), (0, 1, 0, float("nan"), float("nan"), float("nan")), (2, 2, 2, 1.0, 1.0, 1.0)]
    s, v = scores(rows), prf_arrays(rows, np.arange(3)[None])
    assert all(abs(s[k] - v[k][0]) < 1e-9 for k in KEYS), (s, v)
    # capture: 2 images, KTVIC {a,b}/{c}, OpenViIC {b}/{c,d}: N1=3 N2=3 M=2 -> LP 4.5 classes, 2.25/image
    c = capture([frozenset("ab"), frozenset("c")], [frozenset("b"), frozenset("cd")], {}, [], np.arange(2)[None])
    assert c["fine"]["N_lincoln_petersen"]["point"] == 2.25 and c["fine"]["N_chapman"]["point"] == round((16 / 3 - 1) / 2, 3)
    d = delta(np.zeros(100), np.ones(100), 0.0, 1.0)
    assert d["d"] == 1.0 and d["p"] == 0.02 and d["ci95"] == [1.0, 1.0]


if __name__ == "__main__":
    _check()
    sys.exit(main())
