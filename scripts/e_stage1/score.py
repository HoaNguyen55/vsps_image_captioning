#!/usr/bin/env python3
"""Paper E stage 1 (EXPLORATORY / DEV): E scores, baselines, pair accuracy, Kendall tau-b against OIV7 verified
precision, and the stage-1 decision on E-dev-A. Design DESIGN.md §5-§7. CPU, LOCAL only: it reads the OIV7 labels.

  python scripts/e_stage1/score.py --selftest                                       CPU, no data
  python scripts/e_stage1/score.py score --split S --dir DIR [--ledger DIR/ledger.jsonl]
DIR holds pairs.jsonl and captions_all.jsonl (pairs.py) and obj_*.jsonl, whole_*.jsonl, embed.jsonl (judge.py, copied
back from M3). Prints and appends numbers, scorer names and file sha256 only; never a caption.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.stats import kendalltau

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e_lists as L  # noqa: E402
import pairs as PR  # noqa: E402
import clip_score  # noqa: E402  CLIP-S = 2.5 max(cos, 0)

LAMBDAS = (0.0, 0.025, 0.05, 0.1)  # count term: score - lambda * max(0, n - n_hat)
SELF = {"qwen25vl_7b": "qwen25vl_7b", "qwen3vl_8b": "qwen3vl_8b", "internvl3_s2": "internvl3_8b"}  # judge -> its own
B, SEED = 2000, 0
GATE = {"bc_gain": 0.10, "tau_gain": 0.05, "floor": 0.70, "lam_gain": 0.05, "lam_alarm": 0.05, "min_images": 40}


# ------------------------------------------------------------------------------------------------ scorers
def e_one(cap: dict, cache: dict, sub: bool, lam: float, n_hat: float) -> float | None:
    """Uniform mean over distinct mentioned classes of P(yes|image) - P(yes|no image) (or P(yes|image) alone),
    minus lam * max(0, n - n_hat). None when the caption names no class."""
    distinct = {}
    for c in cap["classes"]:
        distinct.setdefault(PR.key(c), c)
    if not distinct:
        return None
    d = [cache[(cap["image_id"], c)][0 if sub else 1] for c in distinct.values()]
    return float(np.mean(d)) - lam * max(0, len(d) - n_hat)


def own(judge: str, cap: dict) -> bool:
    return cap["source"] == f"vlm:{SELF.get(judge, judge)}"


def pooled(cap: dict, per_judge: dict) -> float | None:
    """Mean over judges that did not write the caption (judge != generator)."""
    xs = [f(cap) for j, f in per_judge.items() if not own(j, cap)]
    xs = [x for x in xs if x is not None]
    return float(np.mean(xs)) if xs else None


def scorers(caps: list[dict], obj: dict, whole: dict, emb: dict, n_hat: dict, chair: dict | None = None) -> dict:
    """{scorer name: {cid: score or None}}."""
    out = {}
    for lang in ("en", "vi"):
        judges = sorted(j for j, ql in obj if ql == lang)
        for sub in (True, False):
            for lam in LAMBDAS:
                fs = {j: (lambda c, j=j: e_one(c, obj[(j, lang)], sub, lam, n_hat[c["lang"]])) for j in judges}
                if fs:
                    out[f"E:{lang}:{'sub' if sub else 'raw'}:{lam}"] = {c["cid"]: pooled(c, fs) for c in caps}
    for k, i in (("raw", 0), ("sub", 1)):
        fs = {j: (lambda c, w=w, i=i: None if (r := w.get(c["cid"])) is None else r[0] - r[1] * i)
              for j, w in whole.items()}
        if fs:
            out[f"whole_{k}"] = {c["cid"]: pooled(c, fs) for c in caps}
    if emb:
        out["siglip2"] = {c["cid"]: emb[c["cid"]][0] for c in caps}
        out["mclip"] = {c["cid"]: clip_score.clip_s(emb[c["cid"]][1]) for c in caps}
    if chair is not None:
        out["chair_loo"] = chair
    return out


GLOBAL = ("siglip2", "mclip", "whole_raw", "whole_sub")  # the reference-free global baselines; chair_loo is context


# ------------------------------------------------------------------------------------------------ metrics
def pair_rows(pairs: list[dict], lang: str) -> dict[str, list[tuple]]:
    """{type: [(image, cid that must rank higher, other cid)]}; bc = add_present over add_absent on the same base."""
    out: dict[str, list[tuple]] = {}
    by_base: dict[str, dict] = {}
    for p in pairs:
        if p["lang"] != lang:
            continue
        by_base.setdefault(p["base"], {})[p["type"]] = p
        if p["winner"] == "base":
            out.setdefault(p["type"], []).append((p["image_id"], p["base"], p["pert"]))
    out["bc"] = [(t["add_present"]["image_id"], t["add_present"]["pert"], t["add_absent"]["pert"])
                 for t in by_base.values() if {"add_present", "add_absent"} <= set(t)]
    for typ in ("add_present", "delete", "pad_control"):  # difference only: (image, perturbed, base)
        out[f"d_{typ}"] = [(p["image_id"], p["pert"], p["base"]) for t in by_base.values() if (p := t.get(typ))]
    return out


def correct(s: dict, hi: str, lo: str) -> float:
    a, b = s.get(hi), s.get(lo)
    if a is None or b is None or math.isclose(a, b, abs_tol=1e-12):
        return 0.5
    return float(a > b)


def per_image(rows: list[tuple], val, images: list[str]) -> tuple[np.ndarray, np.ndarray]:
    pos = {i: n for n, i in enumerate(images)}
    num, den = np.zeros(len(images)), np.zeros(len(images))
    for img, x, y in rows:
        v = val(x, y)
        if v is not None:  # a difference row with an unscored caption is left out
            num[pos[img]] += v
            den[pos[img]] += 1
    return num, den


def ratio(num, den, idx) -> dict:
    point = num.sum() / max(den.sum(), 1)
    boot = num[idx].sum(1) / np.maximum(den[idx].sum(1), 1)
    return {"point": float(point), "ci": [float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))],
            "n_pairs": int(den.sum()), "n_images": int((den > 0).sum())}


def tau_rows(caps: list[dict], st: dict) -> list[tuple[str, str, float]]:
    """(image, cid, OIV7 verified precision) of model captions with at least one verifiable mention."""
    out = []
    for c in caps:
        if not c["source"].startswith("vlm:") or c["image_id"] not in st:  # an unlabelled image has nothing verifiable
            continue
        s = [st[c["image_id"]].get(x) for x in {PR.key(m): m for m in c["classes"]}.values()]
        n = sum(x in ("present", "absent") for x in s)
        if n:
            out.append((c["image_id"], c["cid"], sum(x == "present" for x in s) / n))
    return out


def tau(rows, s: dict, images: list[str], idx) -> dict:
    by = {i: [n for n, r in enumerate(rows) if r[0] == i] for i in images}
    x = np.array([s.get(r[1]) if s.get(r[1]) is not None else np.nan for r in rows], float)
    y = np.array([r[2] for r in rows])
    ok = ~np.isnan(x)
    t = lambda sel: float(kendalltau(x[sel], y[sel], variant="b").statistic)  # noqa: E731
    point = t(np.flatnonzero(ok))
    boot = [t(np.array([n for k in b for n in by[images[k]] if ok[n]], int)) for b in idx]
    return {"point": point, "boot": np.array(boot), "n_captions": int(ok.sum())}


def tau_ci(a: dict, b: dict | None = None) -> dict:
    v = a["boot"] - (b["boot"] if b else 0)
    return {"point": a["point"] - (b["point"] if b else 0), "ci": [float(np.nanpercentile(v, 2.5)),
                                                                     float(np.nanpercentile(v, 97.5))]}


def metrics(sc: dict, pairs: list[dict], caps: list[dict], st: dict, lang: str) -> dict:
    rows = pair_rows(pairs, lang)
    images = sorted({c["image_id"] for c in caps})
    idx = np.random.default_rng(SEED).integers(0, len(images), size=(B, len(images)))
    trows = tau_rows(caps, st) if lang == "vi" else []
    out = {}
    for name, s in sc.items():
        if all(s.get(c["cid"]) is None for c in caps):  # not run on this language (e.g. an optional judge step)
            continue
        m = {t: ratio(*per_image(r, lambda hi, lo, s=s: correct(s, hi, lo), images), idx) for t, r in rows.items()
             if not t.startswith("d_") and r}
        for t, r in rows.items():
            if t.startswith("d_") and r:
                both = lambda p, b, s=s: s.get(p) is not None and s.get(b) is not None  # noqa: E731
                m[t] = ratio(*per_image(r, lambda p, b, s=s: s[p] - s[b] if both(p, b) else None, images), idx)
                m[t + "_lower"] = ratio(*per_image(  # share ranking the perturbed caption strictly lower
                    r, lambda p, b, s=s: float(correct(s, b, p) == 1.0) if both(p, b) else None, images), idx)
        if trows:
            m["tau_b"] = tau(trows, s, images, idx)
        out[name] = m
    out["_rows"], out["_images"], out["_idx"] = rows, images, idx
    return out


def gain(m: dict, a: str, b: str, typ: str) -> dict:
    """Accuracy of scorer a minus scorer b on the same pairs, image bootstrap."""
    rows, images, idx = m["_rows"][typ], m["_images"], m["_idx"]
    return ratio(*per_image(rows, lambda hi, lo: correct(m["_s"][a], hi, lo) - correct(m["_s"][b], hi, lo), images),
                 idx)


# ------------------------------------------------------------------------------------------------ decision
def pt(x: dict | None) -> float:
    """A metric's point estimate for ranking; missing or nan (a constant scorer) ranks last."""
    v = (x or {}).get("point", float("nan"))
    return -math.inf if math.isnan(v) else v


def decide(m: dict) -> dict:
    """Stage-1 routing (DESIGN §7). m: metrics(...) on Vietnamese with m["_s"] = the scorers."""
    lams = sorted({float(k.split(":")[3]) for k in m if k.startswith("E:")})
    base = [k for k in m if k.startswith("E:") and k.endswith(":0.0")]
    best = max(base, key=lambda k: (pt(m[k].get("tau_b")), k.split(":")[1] == "en", k.split(":")[2] == "sub"))
    stem = best.rsplit(":", 1)[0]
    lam, calibration = 0.0, False
    for x in sorted(lams, reverse=True):
        k = f"{stem}:{x}"
        if x > 0 and pt(m[k].get("pad")) - pt(m[best].get("pad")) >= GATE["lam_gain"] and (
                pt(m[k].get("d_pad_control_lower")) - pt(m[best].get("d_pad_control_lower")) <= GATE["lam_alarm"]):
            lam, calibration = x, True
            break
    pick = f"{stem}:{lam}"
    glob = [g for g in GLOBAL if g in m]
    best_bc = max(glob, key=lambda g: pt(m[g].get("bc")))
    best_tau = max(glob, key=lambda g: pt(m[g].get("tau_b")))
    a1 = gain(m, pick, best_bc, "bc")
    a2 = tau_ci(m[pick]["tau_b"], m[best_tau]["tau_b"])
    checks = {"A1_bc": a1["point"] >= GATE["bc_gain"] and a1["ci"][0] > 0,
              "A2_tau": a2["point"] >= GATE["tau_gain"],
              "A3_floor": min(pt(m[pick].get("swap")), pt(m[pick].get("add_absent"))) >= GATE["floor"]}
    verdict = "ADVANCE" if all(checks.values()) else "FAIL"
    if a1["n_images"] < GATE["min_images"]:
        verdict = "JUDGE"
    return {"pick": pick, "calibration_kept": calibration, "best_global_bc": best_bc, "best_global_tau": best_tau,
            "A1": a1, "A2": a2, "checks": checks, "verdict": verdict}


# ------------------------------------------------------------------------------------------------ IO (CPU, local)
def load_dir(d: Path) -> tuple[dict, dict, dict]:
    obj, whole, emb = {}, {}, {}
    for f in sorted(d.glob("obj_*.jsonl")):
        judge, lang = f.stem[4:].rsplit("_", 1)
        obj[(judge, lang)] = {(r["image_id"], r["class"]): (r["p_with"] - r["p_without"], r["p_with"])
                              for r in PR.read_jsonl(f)}
    for f in sorted(d.glob("whole_*.jsonl")):
        whole[f.stem[6:]] = {r["class"]: (r["p_with"], r["p_without"]) for r in PR.read_jsonl(f)}
    if (d / "embed.jsonl").exists():
        emb = {r["cid"]: (r["siglip2_cos"], r["mclip_cos"]) for r in PR.read_jsonl(d / "embed.jsonl")}
    return obj, whole, emb


def chair_loo(caps: list[dict], refs: dict) -> dict:
    """-CHAIR_i of each Vietnamese caption against the image's other references (all of them for model captions)."""
    from rescap.chair import chair

    out = {}
    for c in caps:
        if c["lang"] != "vi":
            continue
        k = -1 if c["source"].startswith("vlm:") else int(c["cid"].split("|")[2][1:])
        gold = [r for n, r in enumerate(refs[c["image_id"]]["vi"]) if n != k]
        ci = chair({c["cid"]: c["text"]}, {c["cid"]: gold}).chair_i
        out[c["cid"]] = None if ci is None else -ci
    return out


def cmd_score(a) -> None:
    L.local_only("score")
    split = L.load_split(a.split)
    d = Path(a.dir)
    pairs, caps = PR.read_jsonl(d / "pairs.jsonl"), PR.read_jsonl(d / "captions_all.jsonl")
    ids = set(L.check_images({c["image_id"] for c in caps}, split))
    data = L.C.lb.DATA
    labels = {k: v for k, v in json.loads(PR.X.LABELS.read_text(encoding="utf-8")).items() if k in ids}
    st = PR.X.statuses(PR.X.resolve_map(data / "datasets/xm3600/oiv7/oidv7-class-descriptions.csv"), labels)
    n_hat = {lang: float(np.median([len({PR.key(x) for x in c["classes"]}) for c in caps
                                    if c["source"] == "ref" and c["lang"] == lang])) for lang in ("vi", "en")}
    obj, whole, emb = load_dir(d)
    need = {(c["image_id"], x) for c in caps for x in c["classes"]}
    dropped = sorted(f"{j}_{q}" for (j, q), v in obj.items() if not need <= v.keys())  # stopped by the cap
    obj = {k: v for k, v in obj.items() if need <= v.keys()}
    sc = scorers(caps, obj, whole, emb, n_hat, chair_loo(caps, PR.references(data, ids)))
    res = {}
    for lang in ("vi", "en"):
        m = metrics(sc, pairs, [c for c in caps if c["lang"] == lang], st, lang)
        m["_s"] = sc
        res[lang] = m
    dec = decide(res["vi"])
    inputs = {f.name: L.sha256_file(f) for f in sorted(d.glob("*.jsonl"))}
    rows = [{"lang": lang, "scorer": k, "metric": t, **{x: y for x, y in v.items() if x != "boot"}}
            for lang, m in res.items() for k, mm in m.items() if not k.startswith("_") for t, v in mm.items()]
    out = {"label": L.LABEL, "design_sha256": L.DESIGN_SHA256, "split_sha256": L.SPLIT_SHA256, "n_hat": n_hat,
           "object_caches": sorted(f"{j}_{q}" for j, q in obj), "whole_judges": sorted(whole),
           "incomplete_caches_dropped": dropped,
           "inputs_sha256": inputs, "decision": dec, "rows": rows}
    with open(a.ledger or d / "ledger.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(out, default=float) + "\n")
    print(json.dumps(dec, default=float, indent=1))


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def selftest() -> None:
    cache = {("i1", "chó"): (0.6, 0.9), ("i1", "mèo"): (-0.2, 0.5), ("i1", "ghế"): (0.4, 0.8)}
    cap = lambda cid, cl, src="ref", img="i1": {"cid": cid, "image_id": img, "lang": "vi", "source": src,  # noqa: E731
                                                "classes": cl}
    assert e_one(cap("a", ["chó", "chó", "ghế"]), cache, True, 0.0, 1) == 0.5, "distinct classes, uniform mean"
    assert abs(e_one(cap("a", ["chó", "ghế"]), cache, True, 0.1, 1) - 0.4) < 1e-9, "count term above n_hat"
    assert e_one(cap("a", ["chó"]), cache, False, 0.0, 1) == 0.9 and e_one(cap("a", []), cache, True, 0, 1) is None
    fs = {"qwen25vl_7b": lambda c: 1.0, "qwen3vl_8b": lambda c: 0.0, "internvl3_s2": lambda c: 0.5}
    assert pooled(cap("v", [], "vlm:qwen3vl_8b"), fs) == 0.75, "a judge never scores its own generator's caption"
    assert pooled(cap("v", [], "vlm:internvl3_8b"), fs) == 0.5 and pooled(cap("r", []), fs) == 0.5
    assert correct({"x": 1, "y": 1}, "x", "y") == 0.5 and correct({"x": 2, "y": 1}, "x", "y") == 1.0
    assert correct({"x": None, "y": 1}, "x", "y") == 0.5, "a caption with no mention is a tie"
    # synthetic pairs on 50 images: E ranks every pair right, the global baseline is at chance
    pairs, caps, st = [], [], {}
    for n in range(50):
        i = f"i{n}"
        st[i] = {"chó": "present", "mèo": "absent"}
        for t, w in (("swap", "base"), ("add_absent", "base"), ("add_present", None), ("pad", "base"),
                     ("pad_control", None)):
            pairs.append({"lang": "vi", "image_id": i, "base": f"b{n}", "pert": f"{t}{n}", "type": t, "winner": w})
        caps += [cap(f"b{n}", ["chó"], img=i), cap(f"g{n}", ["chó"], "vlm:qwen25vl_3b", i),
                 cap(f"h{n}", ["chó", "mèo"], "vlm:qwen25vl_3b", i), cap(f"k{n}", ["mèo"], "vlm:qwen25vl_3b", i)]
    good = {f"b{n}": 1.0 for n in range(50)} | {f"swap{n}": 0.0 for n in range(50)} | {
        f"add_absent{n}": 0.2 for n in range(50)} | {f"add_present{n}": 0.9 for n in range(50)} | {
        f"pad{n}": 0.5 for n in range(50)} | {f"pad_control{n}": 1.0 for n in range(50)} | {
        f"g{n}": 0.9 for n in range(50)} | {f"h{n}": 0.5 for n in range(50)} | {f"k{n}": 0.1 for n in range(50)}
    flat = {k: 0.5 for k in good}
    sc = {f"E:en:sub:{x}": good for x in LAMBDAS} | {f"E:en:raw:{x}": flat for x in LAMBDAS} | {
        g: flat for g in GLOBAL}
    m = metrics(sc, pairs, caps, st, "vi")
    m["_s"] = sc
    assert m["E:en:sub:0.0"]["bc"]["point"] == 1.0 and m["siglip2"]["bc"]["point"] == 0.5
    assert m["E:en:sub:0.0"]["tau_b"]["point"] == 1.0 and math.isnan(m["siglip2"]["tau_b"]["point"])
    assert m["E:en:sub:0.0"]["d_pad_control_lower"]["point"] == 0.0
    dec = decide({**m, **{g: {**m[g], "tau_b": {**m[g]["tau_b"], "point": 0.0, "boot": np.zeros(B)}}
                          for g in GLOBAL}})
    assert dec["verdict"] == "ADVANCE" and dec["pick"] == "E:en:sub:0.0" and not dec["calibration_kept"], dec
    weak = {k: (good if k == "E:en:raw:0.0" else flat) for k in sc}
    m2 = metrics(weak, pairs, caps, st, "vi")
    m2["_s"] = weak
    for g in GLOBAL:
        m2[g]["tau_b"] = {"point": 0.0, "boot": np.zeros(B)}
    assert decide(m2)["pick"] == "E:en:raw:0.0", "the (language, subtraction) pick is the best tau"
    flat_all = {k: flat for k in sc}
    m3 = metrics(flat_all, pairs, caps, st, "vi")
    m3["_s"] = flat_all
    for k in flat_all:
        m3[k]["tau_b"] = {"point": 0.0, "boot": np.zeros(B)}
    assert decide(m3)["verdict"] == "FAIL"
    few = metrics(sc, pairs[:5 * 30], caps[:4 * 30], {k: st[k] for k in list(st)[:30]}, "vi")
    few["_s"] = sc
    for g in GLOBAL:
        few[g]["tau_b"] = {"point": 0.0, "boot": np.zeros(B)}
    assert decide(few)["verdict"] == "JUDGE", "fewer than 40 images with bc pairs goes back to the judge"
    print("selftest ok: E score, count term, judge != generator pooling, tie rule, pair rows, accuracy, tau-b, "
          "pick, ADVANCE / FAIL / JUDGE")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("score")
    p.add_argument("--split", type=Path, required=True)
    p.add_argument("--dir", type=Path, required=True)
    p.add_argument("--ledger", type=Path)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    {"score": cmd_score}.get(a.cmd, lambda _a: ap.error("mode?"))(a)


if __name__ == "__main__":
    main()
