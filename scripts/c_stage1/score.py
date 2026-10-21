#!/usr/bin/env python3
"""Paper C stage 1 (EXPLORATORY / DEV): metrics of every run at every guard threshold, and the stage-1 decision
rules, fixed before any output (DESIGN.md §6-§7).

  python scripts/c_stage1/score.py --selftest [--kit-b DIR]                                     CPU, no data
  python scripts/c_stage1/score.py score --runs R ... --zs Z ... --cache C ... --lists L [--kit-b DIR] --ledger F
  python scripts/c_stage1/score.py decide --ledger F --phase pilot|prescreen|advance
CIDEr-D comes from Paper B's kit, imported unchanged and pinned by sha256: scripts/kit_b/protocol_pilot.py
(RDRSegmenter of VnCoreNLP 1.2, the pycocoevalcap CIDEr-D re-implementation, protocol P0: lower-cased words) and
punctuation_audit.strip_trailing_punct_tokens. Every arm is scored as written and with its final punctuation
stripped; the decisions use the stripped column. Objects: CHAIR_i from rescap.chair.chair (gold = union of the
image's references, matcher v2) and the matched-prefix count-matched precision of Paper A §3.3(b) against the
zero-shot arm. The ledger holds numbers and ids only.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import re
import sys
import tempfile
import unicodedata
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import decode_icl as C  # noqa: E402
import guard as G  # noqa: E402
import plan_f1 as PF  # noqa: E402  auroc (scripts/ is on the path via decode_icl)
import rl_reward  # noqa: E402  copy_stat, syllables
from rescap import chair as CH  # noqa: E402

lb = C.lb
KIT_B_DEFAULT = C.ROOT / ".session_backup/2026-10-21/zenodo_build/code/scripts/kit_b"
KIT_B = {"protocol_pilot.py": "6aee428207a2d1a045cd72d054e26a2e2ac8d9c2e414cb0c161e3b95dffd92bf",
         "punctuation_audit.py": "a7e8024030f56cbff07124278cd631964b7b1197607426d7212fd665b6c2f9b1"}
DRAWS, SEED = 2000, 0
VERBATIM = 0.90  # copy_stat m at or above this against a shown example = a near-verbatim copy (cm_pairs.py rule)
COPY_MAX, HIT_MAX, PCM_FLOOR, D_MIN = 0.05, 0.02, -1.0, 2.0
LENGTH_GAP = 0.10  # CC-079: ret vs rand mean length differing by more than this = "not separated from length"


def kit(folder: Path):
    """(protocol_pilot, punctuation_audit) of Paper B's kit, sha-checked; this repo's rescap.chair is loaded first so
    the kit's `from rescap.chair import norm_tone` resolves here, and the kit's sys.path inserts are undone."""
    saved = list(sys.path)
    mods = {}
    for name, h in KIT_B.items():
        p = Path(folder) / name
        if not p.is_file() or lb.sha256_file(p) != h:
            raise SystemExit(f"{p}: not Paper B's kit file (sha256 {h[:8]}); pass --kit-b")
        spec = importlib.util.spec_from_file_location(p.stem, p)
        mods[p.stem] = sys.modules[p.stem] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mods[p.stem])
    sys.path[:] = saved
    return mods["protocol_pilot"], mods["punctuation_audit"]


def references(ds: str, lists: dict, data: Path | None = None) -> dict[str, list[str]]:
    """{image id: references} of a stage-1 dev set, read at run time from $NCS_DATA."""
    data = data or lb.DATA
    ids = {i for i, _f, _h in C.manifest(ds, lists)}
    if ds == "ktvic_dev299":
        out: dict[str, list[str]] = {}
        for a in json.loads((data / "datasets/ktvic/train_data.json").read_text(encoding="utf-8"))["annotations"]:
            if str(a["image_id"]) in ids:
                out.setdefault(str(a["image_id"]), []).append(a["caption"])
        return out
    ann = json.loads((data / "datasets/openviic/uit-openviic-annotation-dev.json").read_text(encoding="utf-8"))
    return {f: [c.strip() for c in ann[f]["captions"]] for f in ids}


def grams(text: str) -> set:
    s = rl_reward.syllables(text)
    return {tuple(s[n:n + 4]) for n in range(len(s) - 3)}


def style(captions: list[str]) -> dict:
    """CC-079 style report: mean length in syllables, share ending in punctuation, share opening with one of the
    run's top-3 opening bigrams (first two syllables)."""
    syl = [rl_reward.syllables(c) for c in captions]
    opens = [tuple(x[:2]) for x in syl]
    top = {b for b, _n in Counter(opens).most_common(3)}
    end = [bool(c.strip()) and unicodedata.category(c.strip()[-1]).startswith("P") for c in captions]
    return {"mean_syllables": float(np.mean([len(x) for x in syl])), "ends_punct": float(np.mean(end)),
            "top3_open_share": float(np.mean([o in top for o in opens]))}


def length_gap(ret: dict, rand: dict) -> dict:
    a, b = ret["style"]["mean_syllables"], rand["style"]["mean_syllables"]
    gap = abs(a - b) / b if b else math.inf
    return {"ret": a, "rand": b, "rel_gap": gap, "not_separated_from_length": gap > LENGTH_GAP}


def tau_name(t: float) -> str:
    return {math.inf: "inf", -math.inf: "-inf"}.get(t, f"{t:.2f}")


# ------------------------------------------------------------------------------------------------ scoring
def items_of(r: dict, zs: dict, caps: dict) -> list[tuple[str, str]]:
    """The run's neighbour-only (image, class) items."""
    src = C.DATASETS[r["dataset"]]["src"]
    return [(i, o) for i, c in r["predictions"].items()
            for o in G.neighbour_only(c, zs["predictions"][i], [C.shown(caps[x], src) for x in r["exemplars"][i]])]


def guard_ready(r: dict, zs: dict, cache: dict, caps: dict) -> bool:
    ver = G.VERIFIER[r["model"]]
    return all((ver, r["dataset"], i, o) in cache for i, o in items_of(r, zs, caps))


def variants(r: dict, zs: dict, cache: dict, caps: dict) -> list[tuple[str, dict, dict]]:
    """(tau, {id: caption}, counts) of one run at every threshold; the zero-shot arm only unguarded. Before the
    run's guard cache is complete, only the thresholds that need no verifier (-inf, +inf)."""
    if r is zs:
        return [("-inf", dict(zs["predictions"]), {"no": 0, "rej": 0, "fallback": 0, "deleted": 0})]
    src, ver = C.DATASETS[r["dataset"]]["src"], G.VERIFIER[r["model"]]
    taus = G.TAUS if guard_ready(r, zs, cache, caps) else (-math.inf, math.inf)
    out = []
    for t in taus:
        capt, cnt = {}, {"no": 0, "rej": 0, "fallback": 0, "deleted": 0}
        for i, c in r["predictions"].items():
            shown = [C.shown(caps[x], src) for x in r["exemplars"][i]]
            no = G.neighbour_only(c, zs["predictions"][i], shown)
            sc = {} if t in (math.inf, -math.inf) else {o: cache[(ver, r["dataset"], i, o)] for o in no}
            capt[i], no, rej, how = G.guarded(c, zs["predictions"][i], shown, sc, t)
            cnt["no"] += len(no)
            cnt["rej"] += len(rej)
            cnt[how] = cnt.get(how, 0) + 1
        out.append((tau_name(t), capt, cnt))
    return out


def cm(caption: str, base: str, gold: set) -> tuple[int, int, int]:
    """(tp of the caption's first k classes, tp of the base's first k, k), k = min of their class counts."""
    a, b = G.classes(caption), G.classes(base)
    k = min(len(a), len(b))
    return sum(G.key(o) in gold for o in a[:k]), sum(G.key(o) in gold for o in b[:k]), k


def score_set(ds: str, runs: list[dict], zs_by_model: dict, refs: dict, ctx: dict) -> list[dict]:
    """Ledger rows of every run (and each model's zero-shot) on one dev set. ctx: the guard cache, the memory
    captions, the segmenter and the two kit modules."""
    cache, caps, segment, E4, PA = (ctx[k] for k in ("cache", "caps", "segment", "E4", "PA"))
    ids = sorted(refs)
    gold = {i: CH._gold_objects(refs[i]) for i in ids}
    mem4 = set().union(*(grams(c) for cc in caps.values() for c in cc.values()))
    todo = [(r, zs_by_model[r["model"]]) for r in runs] + [(z, z) for z in zs_by_model.values()]
    for r, _z in todo:
        if sorted(r["predictions"]) != ids:
            raise SystemExit(f"{r['run_id']}: its images are not the {ds} set")
    var = [(r, z, v) for r, z in todo for v in variants(r, z, cache, caps)]
    texts = sorted({c for *_x, (_t, capt, _n) in var for c in capt.values()} | {x for rs in refs.values() for x in rs})
    seg = dict(zip(texts, (s.lower() for s in segment(texts))))
    cider = E4.Cider({i: [seg[x] for x in refs[i]] for i in ids})
    rows = []
    for r, z, (tau, capt, cnt) in var:
        is_zs = r is z
        spec = {"arm": "zs", "k": 0, "order": None, "tpl": None} if is_zs else r["spec"]
        w = cider.per_image({i: seg[capt[i]] for i in ids})
        s = cider.per_image({i: " ".join(PA.strip_trailing_punct_tokens(seg[capt[i]].split())) for i in ids})
        ch = CH.chair({i: capt[i] for i in ids}, {i: refs[i] for i in ids})
        tri = np.array([cm(capt[i], z["predictions"][i], gold[i]) for i in ids])
        g = [grams(capt[i]) for i in ids]
        src = C.DATASETS[ds]["src"]
        ver = None if is_zs else [rl_reward.copy_stat(rl_reward.syllables(capt[i]), [rl_reward.syllables(
            C.shown(caps[x], src)) for x in r["exemplars"][i]])[0] >= VERBATIM for i in ids]
        n_cls = sum(len(G.classes(r["predictions"][i])) for i in ids)
        rows.append({
            "label": C.LABEL, "design_sha256": C.PINS[C.DESIGN], "run_id": r["run_id"], "model": r["model"],
            "dataset": ds, **{k: spec[k] for k in ("arm", "k", "order", "tpl")}, "tau": tau, "n": len(ids),
            "cider_w": float(w.mean()), "cider_s": float(s.mean()), "chair_i": ch.chair_i,
            "mentions_per_image": ch.mentions_per_caption,
            "pcm_vs_zs": 100 * float((tri[:, 0].sum() - tri[:, 1].sum()) / max(tri[:, 2].sum(), 1)),
            "neighbour_only_rate": cnt["no"] / max(n_cls, 1), "rejected_per_image": cnt["rej"] / len(ids),
            "fallback_rate": cnt["fallback"] / len(ids), "deleted_rate": cnt["deleted"] / len(ids),
            "copy4_memory": sum(len(x & mem4) for x in g) / max(sum(len(x) for x in g), 1),
            "verbatim_share": None if ver is None else float(np.mean(ver)),
            "hit_max_rate": float(np.mean([r["hit_max"][i] for i in ids])), "style": style([capt[i] for i in ids]),
            "guard_auroc": None if is_zs or tau != "-inf" else auroc(r, z, cache, caps, gold),
            "per_image": {"ids": ids, "cider_s": s.round(4).tolist(), "cider_w": w.round(4).tolist(),
                          "tp_cm": tri[:, 0].tolist(), "tp_cm_zs": tri[:, 1].tolist(), "k_cm": tri[:, 2].tolist()},
            "inputs": {"run_sha256": r["_sha256"], "zs_sha256": z["_sha256"], **ctx.get("inputs", {}),
                       "exemplars_sha256": r.get("exemplars_sha256")}, "utc": lb.utc()})
    return rows


def auroc(r: dict, z: dict, cache: dict, caps: dict, gold: dict) -> dict | None:
    """AUROC of the guard score on this run's neighbour-only items, against the reference gold (dev diagnostic);
    None before the run's guard cache is complete."""
    if not guard_ready(r, z, cache, caps):
        return None
    ver = G.VERIFIER[r["model"]]
    items = items_of(r, z, caps)
    y = np.array([G.key(o) in gold[i] for i, o in items], int)
    if not len(y) or y.min() == y.max():
        return {"n": len(y), "pos": int(y.sum())}
    pw = np.array([cache[("p_with", ver, r["dataset"], i, o)] for i, o in items])
    pn = np.array([cache[("p_without", ver, r["dataset"], i, o)] for i, o in items])
    return {"n": len(y), "pos": int(y.sum()), "s": PF.auroc(pw - pn, y), "p_with": PF.auroc(pw, y),
            "p_without": PF.auroc(pn, y)}


def load_cache(paths: list[Path]) -> dict:
    out = {}
    for p in paths:
        for x in Path(p).read_text(encoding="utf-8").splitlines():
            r = json.loads(x)
            k = (r["verifier"], r["dataset"], r["image_id"], r["class"])
            out[k] = r["p_with"] - r["p_without"]
            out[("p_with", *k)], out[("p_without", *k)] = r["p_with"], r["p_without"]
    return out


JAR_SHA256 = "9e2811cdbc2ddfc71d04be5dc36e185c88dcd1ad4d5d69e4ff2e1369dccf7793"  # Paper B's protocol card


def cmd_score(a) -> None:
    lists = C.load_lists(a.lists)
    E4, PA = kit(a.kit_b)
    if lb.sha256_file(E4.VNC / "VnCoreNLP-1.2.jar") != JAR_SHA256:
        raise SystemExit(f"{E4.VNC}/VnCoreNLP-1.2.jar is not the jar of Paper B's protocol card")
    caps = C.memory_captions(lists)
    cache = load_cache(a.cache)
    runs = [G.read_preds(p) for p in a.runs]
    zss = [G.read_preds(p) for p in a.zs]
    for z in zss:
        G.zs_ok(z, z["_sha256"], z["model"], z["dataset"])
    led = Path(a.ledger)
    with led.open("a", encoding="utf-8") as f:
        for ds in sorted({r["dataset"] for r in runs + zss}):
            zs_by = {z["model"]: z for z in zss if z["dataset"] == ds}
            ctx = {"cache": cache, "caps": caps, "segment": E4.rdr, "E4": E4, "PA": PA,
                   "inputs": {"lists_sha256": lb.sha256_file(a.lists),
                              "cache_sha256": {Path(p).name: lb.sha256_file(Path(p)) for p in a.cache}}}
            rows = score_set(ds, [r for r in runs if r["dataset"] == ds], zs_by, references(ds, lists), ctx)
            f.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in rows)
    print(f"appended to {led}")


# ------------------------------------------------------------------------------------------------ decisions
def boot(x: np.ndarray) -> dict:
    """Mean of x with a percentile 95% CI over images (paired bootstrap, B = DRAWS, numpy default_rng(SEED))."""
    idx = np.random.default_rng(SEED).integers(0, len(x), (DRAWS, len(x)))
    lo, hi = np.percentile(x[idx].mean(1), [2.5, 97.5])
    return {"d": float(x.mean()), "lo": float(lo), "hi": float(hi)}


def pcm_ci(row: dict) -> dict:
    p = row["per_image"]
    tp, tz, k = (np.array(p[n], float) for n in ("tp_cm", "tp_cm_zs", "k_cm"))
    idx = np.random.default_rng(SEED).integers(0, len(k), (DRAWS, len(k)))
    draws = 100 * (tp[idx].sum(1) - tz[idx].sum(1)) / np.maximum(k[idx].sum(1), 1)
    lo, hi = np.percentile(draws, [2.5, 97.5])
    return {"d": 100 * float((tp.sum() - tz.sum()) / max(k.sum(), 1)), "lo": float(lo), "hi": float(hi)}


def diff(a: dict, b: dict) -> np.ndarray:
    if a["per_image"]["ids"] != b["per_image"]["ids"]:
        raise SystemExit(f"{a['run_id']} and {b['run_id']} are not on the same images")
    return np.array(a["per_image"]["cider_s"]) - np.array(b["per_image"]["cider_s"])


def find(rows: list[dict], tau: str = "-inf", **want) -> dict:
    hit = [r for r in rows if r["tau"] == tau and all(r[k] == v for k, v in want.items())]
    if len(hit) != 1:
        raise SystemExit(f"ledger: {len(hit)} rows for {want} at tau {tau}")
    return hit[0]


def pilot(rows: list[dict]) -> dict:
    """§7.1: Qwen2.5-VL, dev299, k = 4, retrieval (most similar last, T1) vs random (T1), no guard."""
    base = {"model": "qwen25vl_7b", "dataset": "ktvic_dev299", "k": 4, "tpl": "T1"}
    ret, rand = find(rows, arm="ret", order="last", **base), find(rows, arm="rand", **base)
    fix = [r for r in rows if r["tau"] == "-inf" and r["arm"] == "fix" and all(r[k] == v for k, v in base.items())]
    d = boot(diff(ret, rand))
    return {**d, "verdict": "GO" if d["d"] > 0 else "STOP", "length": length_gap(ret, rand),
            "style": {"ret": ret["style"], "rand": rand["style"], "fix": fix[0]["style"] if fix else None}}


def pick(rows: list[dict], model: str) -> dict:
    """§7.2: the retrieval configuration and threshold carried to the rest of dev-A, from dev299 alone."""
    cand = [r for r in rows if r["model"] == model and r["dataset"] == "ktvic_dev299" and r["arm"] == "ret"
            and r["pcm_vs_zs"] >= PCM_FLOOR and r["verbatim_share"] <= COPY_MAX and r["hit_max_rate"] <= HIT_MAX]
    if not cand:
        raise SystemExit(f"{model}: no retrieval configuration passes the floors on dev299")
    tau = {n: i for i, n in enumerate(tau_name(t) for t in G.TAUS)}
    return min(cand, key=lambda r: (-r["cider_s"], r["k"], r["order"] != "last", r["tpl"] != "T1", tau[r["tau"]]))


def advance(rows: list[dict]) -> dict:
    """§7.3, on OV-dev-A only (not used by pick): pooled over both backbones, retrieval + guard beats random + guard
    by >= D_MIN CIDEr-D (stripped) with CI lower bound > 0; per backbone, count-matched precision against zero-shot
    has CI lower bound > PCM_FLOOR and the near-verbatim copy share is <= COPY_MAX. If ret and rand differ in mean
    length by more than LENGTH_GAP for either backbone, the gain is "not separated from length": no ADVANCE."""
    rep, diffs = {}, []
    for m in C.MODELS:
        p = pick(rows, m)
        cfg = {"model": m, "dataset": "ov_dev_a", "k": p["k"], "tpl": p["tpl"]}
        ret = find(rows, p["tau"], arm="ret", order=p["order"], **cfg)
        rand, fix = find(rows, p["tau"], arm="rand", **cfg), find(rows, p["tau"], arm="fix", **cfg)
        zs = find(rows, arm="zs", model=m, dataset="ov_dev_a")
        diffs.append(diff(ret, rand))
        rep[m] = {"pick": {k: p[k] for k in ("run_id", "tau", "cider_s")}, "vs_rand": boot(diffs[-1]),
                  "vs_fix": boot(diff(ret, fix)), "vs_zs": boot(diff(ret, zs)), "pcm_vs_zs": pcm_ci(ret),
                  "verbatim_share": ret["verbatim_share"], "length": length_gap(ret, rand),
                  "style": {"ret": ret["style"], "rand": rand["style"], "fix": fix["style"]}}
    pooled = boot(np.mean(diffs, axis=0))
    ok = (pooled["d"] >= D_MIN and pooled["lo"] > 0
          and all(rep[m]["pcm_vs_zs"]["lo"] > PCM_FLOOR and rep[m]["verbatim_share"] <= COPY_MAX for m in C.MODELS))
    tied = any(rep[m]["length"]["not_separated_from_length"] for m in C.MODELS)
    verdict = "FAIL" if not ok else "JUDGE: not separated from length" if tied else "ADVANCE"
    return {"pooled_vs_rand": pooled, "per_model": rep, "verdict": verdict}


def latest(rows: list[dict]) -> list[dict]:
    """The last ledger row per (run, set, tau): re-scoring a run supersedes its earlier rows."""
    return list({(r["run_id"], r["dataset"], r["tau"]): r for r in rows}.values())


def cmd_decide(a) -> None:
    rows = latest([json.loads(x) for x in Path(a.ledger).read_text(encoding="utf-8").splitlines() if x])
    out = {"pilot": pilot, "advance": advance}.get(a.phase, lambda rs: {m: pick(rs, m)["run_id"] for m in C.MODELS})
    print(json.dumps(out(rows), indent=1, default=str))


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def fake_run(model, ds, spec, preds, exemplars) -> dict:
    rid = C.run_spec(f"c1_{model}_{ds}-{spec}")
    return {"run_id": rid["run_id"], "model": model, "dataset": ds, "spec": rid, "predictions": preds,
            "exemplars": exemplars, "hit_max": {i: False for i in preds}, "_sha256": "f" * 64}


def selftest(kit_dir: Path) -> None:
    E4, PA = kit(kit_dir)
    # sentences written for this test, not dataset captions
    refs = {"1": ["một con chó nằm trên bãi cỏ", "con chó nằm trên cỏ"],
            "2": ["hai âm đàn ông giả thử cạnh chuỗi xe máy", "hai người đứng gần xe máy"]}
    caps = {"m0": {"ktvic": "một con chó nằm trên bãi cỏ xanh"}, "m1": {"ktvic": "chiếc xe máy và cái bàn"}}
    zs = fake_run("qwen25vl_7b", "ktvic_dev299", "zs", {"1": "một con chó.", "2": "hai người đàn ông."}, {})
    ret = fake_run("qwen25vl_7b", "ktvic_dev299", "ret-k2-last-T1",
                   {"1": "một con chó nằm trên bãi cỏ xanh.",
                    "2": "hai âm đàn ông giả thử cạnh chuỗi xe máy và cái bàn."},
                   {"1": ["m1", "m0"], "2": ["m0", "m1"]})
    cache = {}
    for o, pw, pn in (("xe máy", 0.6, 0.2), ("bàn", 0.3, 0.5)):  # s = +0.4 and -0.2
        k = ("internvl3_s2", "ktvic_dev299", "2", o)
        cache[k], cache[("p_with", *k)], cache[("p_without", *k)] = pw - pn, pw, pn
    split_punct = lambda ts: [re.sub(r"([.,])", r" \1", t) for t in ts]  # noqa: E731  stands in for RDRSegmenter
    ctx = {"cache": cache, "caps": caps, "segment": split_punct, "E4": E4, "PA": PA}
    rows = score_set("ktvic_dev299", [ret], {"qwen25vl_7b": zs}, refs, ctx)
    by = {(r["arm"], r["tau"]): r for r in rows}
    assert set(by) == {("zs", "-inf")} | {("ret", tau_name(t)) for t in G.TAUS}
    assert by[("ret", "0.10")]["rejected_per_image"] == 0.5 and by[("ret", "inf")]["rejected_per_image"] == 1.0
    assert by[("ret", "-inf")]["cider_s"] >= by[("ret", "-inf")]["cider_w"], "the final period costs CIDEr-D"
    assert by[("ret", "-inf")]["verbatim_share"] == 0.5 and by[("zs", "-inf")]["verbatim_share"] is None
    assert by[("ret", "0.10")]["chair_i"] < by[("ret", "-inf")]["chair_i"], "deleting the invented table helps"
    early = score_set("ktvic_dev299", [ret], {"qwen25vl_7b": zs}, refs, {**ctx, "cache": {}})
    assert {(r["arm"], r["tau"]) for r in early} == {("zs", "-inf"), ("ret", "-inf"), ("ret", "inf")}, "no cache yet"
    assert all(r["guard_auroc"] is None for r in early)
    assert len(latest(rows + rows)) == len(rows), "re-scored rows supersede earlier ones"
    assert cm("chó, mèo, bàn", "chó, ghế", {"chó", "bàn"}) == (1, 1, 2)
    # decisions on a synthetic ledger
    led = []
    for m in C.MODELS:
        for ds, gain in (("ktvic_dev299", 3.0), ("ov_dev_a", 3.0)):
            for arm, order, k, add in (("ret", "last", 4, gain), ("ret", "first", 4, 1.0), ("rand", None, 4, 0.0),
                                       ("fix", None, 4, 0.5), ("zs", None, 0, -5.0)):
                x = np.linspace(10, 20, 40) + add + np.sin(np.arange(40))
                led.append({"model": m, "dataset": ds, "arm": arm, "order": order, "k": k, "tpl": None if arm == "zs"
                            else "T1", "tau": "-inf", "run_id": f"{m}-{ds}-{arm}-{order}", "cider_s": float(x.mean()),
                            "pcm_vs_zs": 0.0, "verbatim_share": 0.0, "hit_max_rate": 0.0,
                            "style": {"mean_syllables": 12.0, "ends_punct": 0.0, "top3_open_share": 0.5},
                            "per_image": {"ids": [str(n) for n in range(40)], "cider_s": x.tolist(),
                                          "tp_cm": [1] * 40, "tp_cm_zs": [1] * 40, "k_cm": [2] * 40}})
    assert pilot(led)["verdict"] == "GO" and pick(led, "qwen25vl_7b")["order"] == "last"
    assert advance(led)["verdict"] == "ADVANCE"
    flat = [{**r, "per_image": {**r["per_image"], "cider_s": [10.0] * 40}} for r in led]
    assert advance(flat)["verdict"] == "FAIL" and pilot(flat)["verdict"] == "STOP"
    long = [{**r, "style": {**r["style"], "mean_syllables": 14.0}} if r["arm"] == "ret" else r for r in led]
    assert advance(long)["verdict"] == "JUDGE: not separated from length", "a >10% length gap blocks ADVANCE"
    assert pilot(long)["length"]["not_separated_from_length"] and pilot(long)["verdict"] == "GO"
    st = style(["một con chó.", "một con mèo", "hai cái bàn."])
    assert st["ends_punct"] == 2 / 3 and abs(st["mean_syllables"] - 3) < 1e-9 and st["top3_open_share"] == 1.0
    with tempfile.TemporaryDirectory() as tmp:  # C5: a kit file that differs by one byte is refused
        for name in KIT_B:
            data = (Path(kit_dir) / name).read_bytes()
            (Path(tmp) / name).write_bytes(data + b"\n" if name == "punctuation_audit.py" else data)
        assert C.refuses(lambda: kit(Path(tmp))), "a changed kit file must be refused"
    print("selftest ok: kit scorer and its sha refusal, punctuation variants, guard thresholds, objects, copies, "
          "style report and length rule, decision rules")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--kit-b", type=Path, default=KIT_B_DEFAULT)
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("score")
    p.add_argument("--runs", nargs="*", type=Path, default=[])
    p.add_argument("--zs", nargs="+", type=Path, required=True)
    p.add_argument("--cache", nargs="*", type=Path, default=[])
    p.add_argument("--lists", type=Path, required=True)
    p.add_argument("--kit-b", type=Path, default=KIT_B_DEFAULT)
    p.add_argument("--ledger", required=True)
    p = sub.add_parser("decide")
    p.add_argument("--ledger", required=True)
    p.add_argument("--phase", choices=("pilot", "prescreen", "advance"), required=True)
    a = ap.parse_args()
    if a.selftest:
        return selftest(a.kit_b)
    {"score": cmd_score, "decide": cmd_decide}.get(a.cmd, lambda _a: ap.error("mode?"))(a)


if __name__ == "__main__":
    main()
