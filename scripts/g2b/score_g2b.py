#!/usr/bin/env python3
"""G2-B analysis (Paper A Section 7.6), as registered in manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.json.

Every threshold, seed, family, gold, prediction and kill rule comes from the committed prereg JSON. The matchers are
the pinned project matchers, imported unchanged (score_coco_probe, rescap.chair, xm3600_oiv7, looks_vietnamese, CJK_RE).

  selfcheck  reproduces committed values of three existing Qwen2.5-VL-7B families with this code path (single golds,
             point estimates of the slope of F1 on ln M and of the exponent b): COCO-2500 (L1 check_coco.json),
             UIT-ViIC test under both lexicons (c2_n1_uitviic_mstar.json) and XM3600 (xm3600_full_verdict.json).
             Exit 1 if any value differs, or if the verdict rules fail their unit checks.
  score      scores the G2-B decodes in --outputs-dir: sidecar and provenance (KD) checks, clean subsets, random
             reference subsets, image bootstrap, the registered statistics, verdicts, kill rules, descriptive tables.
             Run it only after the decodes have landed.

  python3 scripts/g2b/score_g2b.py selfcheck --out data/results/g2b/selfcheck.json
  python3 scripts/g2b/score_g2b.py score --outputs-dir DIR --out RESULTS.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
import score_coco_probe as sc  # noqa: E402
import xm3600_oiv7 as xo  # noqa: E402
from clean_supervision import CJK_RE  # noqa: E402
from rescap.chair import objects_in  # noqa: E402
from rescap.vlm.mock import looks_vietnamese  # noqa: E402

PREREG = ROOT / "manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.json"
SCHEMA = "vsps.g2b_score.v1"
SB = ROOT / ".session_backup/2026-10-14"
VI_TERMS, SYN = sc.load_vi_terms(), sc.load_synonyms()
MATCH = {"coco80": {"vi": lambda c: sc.vi_objects(c, VI_TERMS), "en": lambda c: sc.en_classes(c, SYN)},
         "objects_in": {"vi": lambda c: set(objects_in(c))}}
TERM = re.compile(r"(slope|b|mres)\[([^\]]+)\]\(([A-Z0-9_]+)(?: \| ([A-Z0-9_]+))?\)")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def jload(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


# ------------------------------------------------------------------------------------------------ data
def karpathy_refs(want: set[int]) -> dict[int, list[str]]:
    """Raw Karpathy sentences of `want` (check_coco.karpathy_refs parsing)."""
    text = (ROOT / "data/datasets/karpathy/dataset_coco.json").read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r'"cocoid": (\d+)\}', text):
        c = int(m.group(1))
        if c in want:
            s = text.rfind('{"filepath"', 0, m.start())
            out[c] = [x["raw"] for x in json.loads(text[s:m.end()])["sentences"]]
    return out


def ann_refs(path: Path) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for a in jload(path)["annotations"]:
        if a.get("caption"):
            out.setdefault(str(a["image_id"]), []).append(a["caption"])
    return out


def coco_context(ids: list[str]) -> dict:
    """COCO probe images: English Karpathy references (first 5) and COCO-2014 instance classes."""
    kr = karpathy_refs({int(i) for i in ids})
    inst = jload(ROOT / "data/coco_probe/instance_gold.json")
    return {"ids": ids, "lexicons": {"coco80": {
        "refs": [[sc.en_classes(s, SYN) for s in kr[int(i)][:5]] for i in ids],
        "complete": [set(inst.get(i, {}).get("coco", [])) for i in ids]}}}


def uitviic_context() -> dict:
    refs = ann_refs(ROOT / "data/datasets/uitviic/test_data.json")
    inst = jload(ROOT / "data/uitviic/instance_gold.json")
    ids = sorted(refs, key=int)
    out = {"ids": ids, "lexicons": {}}
    for lex, fn in (("coco80", MATCH["coco80"]["vi"]), ("objects_in", MATCH["objects_in"]["vi"])):
        comp = [set(inst[i]["coco"]) for i in ids] if lex == "coco80" else \
            [set().union(*(fn(w) for w in inst[i]["vi"])) for i in ids]
        out["lexicons"][lex] = {"refs": [[fn(r) for r in refs[i][:5]] for i in ids], "complete": comp}
    return out


def xm3600_context() -> dict:
    refs = ann_refs(ROOT / "data/datasets/xm3600/test_data.json")
    ids = sorted(refs)
    labels = {k: v for k, v in jload(ROOT / "data/xm3600/oiv7_labels.json").items() if not k.startswith("_")}
    vmap = xo.resolve_map(ROOT / "data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv")
    st = xo.statuses(vmap, labels)
    fn = MATCH["objects_in"]["vi"]
    return {"ids": ids, "lexicons": {"objects_in": {"refs": [[fn(r) for r in refs[i]] for i in ids],
                                                    "oiv7": [st.get(i, {}) for i in ids], "mapped": set(vmap)}}}


def read_captions(path: Path) -> dict[str, str | list[str]]:
    """{image id: caption} from a preds.json (project or G2-B format) or a COCO-probe jsonl; a G2-B .samples.jsonl
    gives {image id: [samples]}."""
    name = Path(path).name
    if name.endswith(".samples.jsonl"):
        rows = [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines()[1:]]
        return {str(r["image_id"]): r["samples"] for r in rows}
    if name.endswith(".jsonl"):
        rows = [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]
        return {str(r["cocoid"]): r["caption"] for r in rows}
    d = jload(path)
    d = d.get("predictions", d)
    return {str(k): (v[0] if isinstance(v, list) else v) or "" for k, v in d.items()}


def mentions(caps: dict, ids: list[str], fn, vote: int | None = None) -> list[set]:
    """Mention sets per image; for a sample pool, the classes named by at least `vote` samples."""
    if vote is None:
        return [fn(caps.get(i, "")) for i in ids]
    out = []
    for i in ids:
        count: dict[str, int] = {}
        for c in caps.get(i, []):
            for o in fn(c):
                count[o] = count.get(o, 0) + 1
        out.append({o for o, n in count.items() if n >= vote})
    return out


def is_clean(cap, lang: str) -> bool:
    caps = cap if isinstance(cap, list) else [cap]
    return all(isinstance(c, str) and not CJK_RE.search(c) and (lang == "en" or looks_vietnamese(c)) for c in caps)


# ------------------------------------------------------------------------------------------------ golds and scores
def random_subsets(n_refs: list[int], kmax: int, n_rep: int, seed: int) -> dict[int, list[list[tuple]]]:
    """Registered draw: default_rng(seed); for k = 1..kmax, for r, for each image in id order: choice(n, k)."""
    rng = np.random.default_rng(seed)
    return {k: [[tuple(int(j) for j in rng.choice(n, k, replace=False)) for n in n_refs] for _ in range(n_rep)]
            for k in range(1, kmax + 1)}


def gold_variants(lex: dict, subsets: dict | None, firstk: bool = False) -> dict[str, list[list[set]]]:
    refs = lex["refs"]
    union = [set().union(*r) for r in refs]
    out = {"refs_all": [union]}
    for k, reps in (subsets or {}).items():
        out[f"refs{k}_randk"] = [[set().union(*(refs[i][j] for j in sub[i])) for i in range(len(refs))]
                                 for sub in reps]
    if firstk:
        for k in range(1, 6):
            out[f"refs{k}_firstk"] = [[set().union(*r[:k]) for r in refs]]
    if "complete" in lex:
        out["inst"] = [lex["complete"]]
        out["inst+refs_all"] = [[c | u for c, u in zip(lex["complete"], union)]]
        out["inst+refs1_firstk"] = [[c | (r[0] if r else set()) for c, r in zip(lex["complete"], refs)]]
    return out


def rows(ment: list[set], gold: list[list[set]]) -> dict:
    tp = np.array([[len(m & g) for m, g in zip(ment, gs)] for gs in gold], float)
    gl = np.array([[len(g) for g in gs] for gs in gold], float)
    return {"tp": tp, "has": (gl > 0).astype(float), "rec": np.divide(tp, gl, out=np.zeros_like(tp), where=gl > 0),
            "m": np.array([len(m) for m in ment], float)}


def oiv7_rows(ment: list[set], lex: dict) -> dict:
    pm, am, pos = [], [], []
    for m, s in zip(ment, lex["oiv7"]):
        pr = {c for c, v in s.items() if v == "present"}
        ab = {c for c, v in s.items() if v == "absent"}
        mm = m & lex["mapped"]
        pm.append(len(mm & pr))
        am.append(len(mm & ab))
        pos.append(len(pr))
    return {"pm": np.array(pm, float), "am": np.array(am, float), "pos": np.array(pos, float),
            "m": np.array([len(m) for m in ment], float)}


def div(a, b, empty):
    return np.divide(a, b, out=np.full(np.broadcast(a, b).shape, empty, float), where=b > 0)


def scores(r: dict, idx: np.ndarray, W: np.ndarray) -> dict:
    """check_mstar.prf (mixed F1, mean over subsets) with weights W (B, n) over the images idx; OIV7: F1_pos."""
    msum = W @ r["m"][idx]
    M = msum / W.sum(1)
    if "tp" in r:
        tp, has, rec = r["tp"][:, idx], r["has"][:, idx], r["rec"][:, idx]
        P = div(tp @ W.T, msum[None, :], 0.0)
        R = div((rec * has) @ W.T, has @ W.T, np.nan)
        F = div(2 * P * R, P + R, 0.0)
        P, R, F = P.mean(0), R.mean(0), F.mean(0)
    else:
        pm = W @ r["pm"][idx]
        P = div(pm, W @ (r["pm"][idx] + r["am"][idx]), 0.0)
        R = div(pm, W @ r["pos"][idx], 0.0)
        F = div(2 * P * R, P + R, 0.0)
    return {"P": P, "R": R, "F": F, "M": M, "TP": P * M}


# ------------------------------------------------------------------------------------------------ statistics
def ols(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """OLS slope along axis 0 (systems), for every bootstrap column."""
    dx = x - x.mean(0)
    with np.errstate(invalid="ignore", divide="ignore"):
        return (dx * (y - y.mean(0))).sum(0) / (dx ** 2).sum(0)


def family_fit(sc_list: list[dict], floor: float) -> tuple[np.ndarray, np.ndarray]:
    with np.errstate(divide="ignore", invalid="ignore"):
        lm = np.log(np.stack([s["M"] for s in sc_list]))
        lt = np.log(np.maximum(np.stack([s["TP"] for s in sc_list]), floor))
    b = ols(lm, lt)
    return lt.mean(0) - b * lm.mean(0), b


def stat_slope(sc_list, floor):
    with np.errstate(divide="ignore", invalid="ignore"):
        lm = np.log(np.stack([s["M"] for s in sc_list]))
    return ols(lm, 100 * np.stack([s["F"] for s in sc_list]))


def stat_b(sc_list, floor):
    return family_fit(sc_list, floor)[1]


def residuals(targets: list[dict], ref: list[dict], floor: float) -> np.ndarray:
    a, b = family_fit(ref, floor)
    with np.errstate(invalid="ignore", over="ignore"):
        return np.stack([100 * t["P"] - 100 * np.exp(a) * t["M"] ** (b - 1) for t in targets])


def ci(rep: np.ndarray, lo_q: float, hi_q: float) -> list[float] | None:
    return None if not np.all(np.isfinite(rep)) else [float(np.percentile(rep, lo_q)), float(np.percentile(rep, hi_q))]


def verdict(rule: str, point: float, interval: list[float] | None, delta: float | None = None) -> str:
    """The registered verdict rules (prereg verdict_rules), from the point estimate and the 95% CI."""
    if interval is None or not np.isfinite(point):
        return "NOT_EVALUABLE"
    lo, hi = interval
    if rule == "sign_gt_0":
        return "PASS" if lo > 0 else "FAIL" if point <= 0 else "INCONCLUSIVE"
    if rule == "sign_lt_0":
        return "PASS" if hi < 0 else "FAIL" if point >= 0 else "INCONCLUSIVE"
    if rule == "equiv_abs_le":
        return "PASS" if -delta <= lo and hi <= delta else "FAIL" if hi < -delta or lo > delta else "INCONCLUSIVE"
    if rule == "diff_abs_gt":
        return "PASS" if lo > delta or hi < -delta else "FAIL" if -delta <= lo and hi <= delta else "INCONCLUSIVE"
    raise ValueError(rule)


def compound(parts: list[str]) -> str:
    if "FAIL" in parts:
        return "FAIL"
    if "NOT_EVALUABLE" in parts:
        return "NOT_EVALUABLE"
    return "PASS" if all(p == "PASS" for p in parts) else "INCONCLUSIVE"


def _check_rules() -> list[str]:
    """Unit checks of the verdict rules; returns the failures."""
    cases = [("sign_gt_0", 1.0, [0.2, 2.0], None, "PASS"), ("sign_gt_0", 0.5, [-0.1, 1.0], None, "INCONCLUSIVE"),
             ("sign_gt_0", 0.0, [-1.0, 1.0], None, "FAIL"), ("sign_lt_0", -1.0, [-2.0, -0.1], None, "PASS"),
             ("sign_lt_0", 0.0, [-1.0, 1.0], None, "FAIL"), ("equiv_abs_le", 0.0, [-0.04, 0.04], 0.05, "PASS"),
             ("equiv_abs_le", 0.1, [0.06, 0.2], 0.05, "FAIL"), ("equiv_abs_le", 0.0, [-0.06, 0.04], 0.05,
                                                                 "INCONCLUSIVE"),
             ("diff_abs_gt", 3.0, [2.5, 4.0], 2, "PASS"), ("diff_abs_gt", 1.0, [-1.0, 1.5], 2, "FAIL"),
             ("diff_abs_gt", 2.5, [1.0, 4.0], 2, "INCONCLUSIVE"), ("sign_gt_0", float("nan"), None, None,
                                                                  "NOT_EVALUABLE")]
    bad = [str(c) for c in cases if verdict(c[0], c[1], c[2], c[3]) != c[4]]
    bad += [] if compound(["PASS", "FAIL", "NOT_EVALUABLE"]) == "FAIL" else ["compound FAIL"]
    bad += [] if compound(["PASS", "NOT_EVALUABLE"]) == "NOT_EVALUABLE" else ["compound NOT_EVALUABLE"]
    bad += [] if compound(["PASS", "INCONCLUSIVE"]) == "INCONCLUSIVE" else ["compound INCONCLUSIVE"]
    return bad


def mstar_mixed(sc_list: list[dict], floor: float) -> float:
    """check_mstar.mstar numeric argmax of F(M) on the fitted P and R curves (point estimates)."""
    lm = np.log([float(s["M"][0]) for s in sc_list])
    lt = np.log(np.maximum([float(s["TP"][0]) for s in sc_list], floor))
    lr = np.log(np.maximum([float(s["R"][0]) for s in sc_list], floor))
    b = float(ols(lm[:, None], lt[:, None])[0])
    d = float(ols(lm[:, None], lr[:, None])[0])
    a, c = lt.mean() - b * lm.mean(), lr.mean() - d * lm.mean()
    grid = np.exp(np.linspace(np.log(0.2), np.log(60), 4000))
    pg, rg = np.exp(a) * grid ** (b - 1), np.minimum(np.exp(c) * grid ** d, 1.0)
    return float(grid[(2 * pg * rg / (pg + rg)).argmax()])


# ------------------------------------------------------------------------------------------------ selfcheck
def selfcheck(out: Path) -> int:
    """Reproduce committed family values (single golds) of three existing families with this code path."""
    reg = jload(PREREG)
    floor = reg["design_constants"]["tp_floor"]["value"]
    cells = []

    def compare(fam: str, ctx_lex: dict, systems: dict, kind: str, golds: dict, refs: dict) -> None:
        ids = ctx_lex["ids"]
        idx = np.arange(len(ids))
        one = np.ones((1, len(ids)))
        lex = ctx_lex["lex"]
        ment = {s: mentions(c, ids, MATCH[kind]["vi"]) for s, c in systems.items()}
        variants = gold_variants(lex, None, firstk=True)
        for gname, (key_path, sdp, bdp) in golds.items():
            if gname == "oiv7_verified":
                sl = [scores(oiv7_rows(ment[s], lex), idx, one) for s in systems]
            else:
                sl = [scores(rows(ment[s], variants[gname]), idx, one) for s in systems]
            ref = refs[gname]
            for stat, mine, dp, ref_v in (("slope", stat_slope(sl, floor)[0], sdp, ref[0]),
                                          ("b", stat_b(sl, floor)[0], bdp, ref[1])):
                diff = abs(round(float(mine), dp) - ref_v)
                cells.append({"family": fam, "gold": gname, "stat": stat, "reference_key": key_path[stat],
                              "reference": ref_v, "reproduced": round(float(mine), dp), "abs_diff": round(diff, 10),
                              "ok": diff <= 0.5 * 10 ** -dp + 1e-9})

    # COCO-2500: check_coco.json (9 systems, 2,500 images)
    cref = jload(SB / "r11_litmaps/L1/check_coco.json")["gold"]
    cids = [str(i["cocoid"]) for i in sorted(jload(ROOT / "data/coco_probe/manifest.json")["images"],
                                              key=lambda x: x["cocoid"])]
    res = ROOT / "data/results"
    csys = {f.name.split(".shard")[0] + ("+vcd" if d == "coco5000_vcd" else ""): read_captions(f)
            for d in ("coco5000", "coco_transfer", "coco5000_vcd") for f in sorted((res / d).glob("*.shard*.jsonl"))}
    cctx = coco_context(cids)
    cmap = {**{f"refs{k}_firstk": f"refs{k}_firstk" for k in range(1, 6)}, "inst": "inst", "inst+refs_all": "inst+refs5"}
    compare("COCO-2500 (check_coco)", {"ids": cids, "lex": cctx["lexicons"]["coco80"]}, csys, "coco80",
            {g: ({"slope": f"gold.{k}.slope", "b": f"gold.{k}.b"}, 2, 3) for g, k in cmap.items()},
            {g: (cref[k]["slope"], cref[k]["b"]) for g, k in cmap.items()})

    # UIT-ViIC test: c2_n1_uitviic_mstar.json (10 systems, 231 images), both lexicons
    uref = jload(SB / "r11_verify/c2_n1_uitviic_mstar.json")["uitviic_test"]["lexicons"]
    usys = {**{"transfer_" + f.name.removeprefix("uitviic_").removesuffix(".preds.json"): read_captions(f)
               for f in sorted((res / "uitviic").glob("*.preds.json")) if "zeroshot" not in f.name},
            **{f.name.removeprefix("uitviic_").removesuffix(".preds.json"): read_captions(f)
               for f in sorted((res / "uitviic").glob("*zeroshot*.preds.json"))},
            **{"ind_" + f.name.removeprefix("uitviic_").removesuffix(".preds.json"): read_captions(f)
               for f in sorted((res / "uitviic_ind_test").glob("*.preds.json"))}}
    uctx = uitviic_context()
    umap = {**{f"refs{k}_firstk": f"refs{k}_firstk" for k in range(1, 6)}, "inst": "inst_only",
            "inst+refs_all": "inst_plus_refs5", "inst+refs1_firstk": "inst_plus_refs1_firstk"}
    for lex in ("coco80", "objects_in"):
        lk = "coco80" if lex == "coco80" else "vi_objects_in"
        grp = {g: uref[lk]["gold_variants"][k]["groups"]["all_10"] for g, k in umap.items()}
        compare(f"UIT-ViIC test all_10 ({lk})", {"ids": uctx["ids"], "lex": uctx["lexicons"][lex]}, usys, lex,
                {g: ({"slope": f"uitviic_test.lexicons.{lk}.gold_variants.{k}.groups.all_10.slope_F1_mixed_per_logM",
                      "b": f"uitviic_test.lexicons.{lk}.gold_variants.{k}.groups.all_10.b"}, 2, 4)
                 for g, k in umap.items()},
                {g: (grp[g]["slope_F1_mixed_per_logM"], grp[g]["b"]) for g in umap})

    # XM3600: xm3600_full_verdict.json, matcher v2 (6 systems, 600 images)
    xref = jload(SB / "r12_verify/xm3600_full_verdict.json")["matcher_v2_tone_normalised"]["n1_f1_vs_logM_slopes"]
    xsys = {f.name.removesuffix(".preds.json"): read_captions(f) for f in sorted((res / "xm3600").glob("*.preds.json"))}
    xctx = xm3600_context()
    xmap = {"refs1_firstk": "refs1_firstk", "refs_all": "refs_all", "oiv7_verified": "oiv7_verified"}
    pre = "matcher_v2_tone_normalised.n1_f1_vs_logM_slopes"
    compare("XM3600 (full verdict, v2)", {"ids": xctx["ids"], "lex": xctx["lexicons"]["objects_in"]}, xsys,
            "objects_in", {g: ({"slope": f"{pre}.{k}.slope_F1_per_logM", "b": f"{pre}.{k}.b_in_sample"}, 4, 4)
                           for g, k in xmap.items()},
            {g: (xref[k]["slope_F1_per_logM"], xref[k]["b_in_sample"]) for g, k in xmap.items()})

    rule_failures = _check_rules()
    pin_failures = check_pins(reg)
    result = {"schema": SCHEMA + ".selfcheck", "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "scorer_sha256": sha256_file(Path(__file__)), "prereg_sha256": sha256_file(PREREG),
              "pinned_files_differing_from_prereg": pin_failures,
              "system_counts": {"COCO-2500": len(csys), "UIT-ViIC": len(usys), "XM3600": len(xsys)},
              "references_sha256": {str(p.relative_to(ROOT)): sha256_file(p) for p in (
                  SB / "r11_litmaps/L1/check_coco.json", SB / "r11_verify/c2_n1_uitviic_mstar.json",
                  SB / "r12_verify/xm3600_full_verdict.json")},
              "verdict_rule_unit_failures": rule_failures, "cells": cells, "n_cells": len(cells),
              "n_ok": sum(c["ok"] for c in cells)}
    result["pass"] = result["n_ok"] == result["n_cells"] and not rule_failures and not pin_failures
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("n_cells", "n_ok", "pass", "verdict_rule_unit_failures")}))
    return 0 if result["pass"] else 1


# ------------------------------------------------------------------------------------------------ score
def git_blob_sha(rel: str) -> str | None:
    r = subprocess.run(["git", "-C", str(ROOT), "show", f"HEAD:{rel}"], capture_output=True)
    return hashlib.sha256(r.stdout).hexdigest() if r.returncode == 0 else None


def check_pins(reg: dict) -> list[str]:
    """Instruments and data must still equal their prereg pins (HEAD blob and disk for tracked files)."""
    bad = []
    for rec in reg["frozen_files"]["instruments"] + reg["frozen_files"]["data"]:
        path = ROOT / rec["path"]
        blob = git_blob_sha(rec["path"])
        disk = sha256_file(path) if path.exists() else None
        if disk != rec["sha256"] or (blob is not None and blob != rec["sha256"]):
            bad.append(rec["path"])
    return bad


def provenance_problems(reg: dict, run: dict, prov: dict, n_images: int) -> list[str]:
    """KD: settings recorded by the decoder that differ from the registration."""
    dc, m = reg["design_constants"], reg["model"]
    sampled = run["temperature"] != 0
    want = {"prereg_id": reg["prereg_id"], "prereg_sha256": sha256_file(PREREG), "backbone": m["hub_id"],
            "revision": m["revision"], "dataset": run["dataset"], "prompt_mode": run["prompt_mode"],
            "temperature": run["temperature"], "sequences_per_image": run["sequences_per_image"],
            "max_new_tokens": reg["decode"]["max_new_tokens"][run["prompt_mode"]],
            "top_p": dc["top_p"]["value"] if sampled else None, "top_k": dc["top_k"]["value"] if sampled else None,
            "seed": dc["sampling_seed"]["value"] if sampled else None, "packages": m["venv"]["packages"],
            "snapshot_SHA256SUMS": m["checksum_manifest"]["sha256"], "n_images": n_images,
            "prompt_text_sha256": reg["decode"]["prompts"][run["prompt_mode"]]["text_sha256"]}
    return [f"{k}: {prov.get(k)!r} != {v!r}" for k, v in want.items() if prov.get(k) != v]


def load_runs(reg: dict, outputs: Path, n_ids: dict) -> tuple[dict, dict]:
    caps, excluded = {}, {}
    for run in reg["runs"]:
        rid = run["run_id"]
        f = outputs / f"{rid}.{'samples.jsonl' if run['sequences_per_image'] > 1 else 'preds.json'}"
        side = Path(str(f) + ".sha256")
        if not f.exists() or not side.exists():
            excluded[rid] = ["output or sidecar missing"]
            continue
        if side.read_text(encoding="utf-8").split()[0] != sha256_file(f):
            excluded[rid] = ["sha256 differs from its sidecar"]
            continue
        prov = json.loads(f.read_text(encoding="utf-8").splitlines()[0]) if run["sequences_per_image"] > 1 \
            else jload(f)
        probs = provenance_problems(reg, run, prov, n_ids[run["dataset"]])
        if probs:
            excluded[rid] = probs
            continue
        caps[rid] = read_captions(f)
    return caps, excluded


class Dataset:
    """One G2-B image set: contexts, systems, mention cache, gold variants and the random subsets."""

    def __init__(self, reg: dict, name: str, caps: dict, lang: dict):
        self.reg, self.name, self.caps, self.lang = reg, name, caps, lang
        g = reg["golds"][name]
        self.complete = g["complete"]
        ctx = {"cv295": lambda: coco_context(sorted(
            (ROOT / "data/coco_probe/probe_val2017_ids.txt").read_text().split(), key=int)),
               "uv231": uitviic_context, "xm600": xm3600_context}[name]()
        self.ids, self.lex = ctx["ids"], ctx["lexicons"]
        kmax = max([int(m.group(1)) for v in g["variants"] if (m := re.fullmatch(r"refs(\d+)_randk", v))])
        dc = reg["design_constants"]
        first = next(iter(self.lex.values()))
        self.subsets = random_subsets([len(r) for r in first["refs"]], kmax, dc["n_random_subsets"]["value"],
                                      dc["set_by_this_registration"]["subset_seed"])
        self.variants = {lx: gold_variants(v, self.subsets) for lx, v in self.lex.items()}
        self._ment: dict = {}
        self._rows: dict = {}

    def system_caps(self, sysname: str):
        base, _, vote = sysname.partition(":vote>=")
        return self.caps[base], (int(vote) if vote else None)

    def ment(self, sysname: str, lx: str) -> list[set]:
        key = (sysname, lx)
        if key not in self._ment:
            caps, vote = self.system_caps(sysname)
            self._ment[key] = mentions(caps, self.ids, MATCH[lx][self.lang.get(sysname.partition(":")[0], "vi")],
                                       vote)
        return self._ment[key]

    def rows(self, sysname: str, gold: str, lx: str) -> dict:
        key = (sysname, gold, lx)
        if key not in self._rows:
            ment = self.ment(sysname, lx)
            self._rows[key] = oiv7_rows(ment, self.lex[lx]) if gold == "oiv7_verified" else \
                rows(ment, self.variants[lx][gold])
        return self._rows[key]

    def clean_index(self, systems: list[str], clean: bool) -> np.ndarray:
        keep = []
        for n, i in enumerate(self.ids):
            ok = True
            for s in systems:
                caps, _ = self.system_caps(s)
                if i not in caps or (clean and not is_clean(caps[i], self.lang.get(s.partition(":")[0], "vi"))):
                    ok = False
                    break
            if ok:
                keep.append(n)
        return np.array(keep, int)


def eval_stat(ds: Dataset, expr: str, fams: dict, lx: str, idx: np.ndarray, Ws: list[np.ndarray],
              floor: float) -> list[np.ndarray]:
    """Value of a registered statistic expression ('t1' or 't1 - t2') for each weight matrix in Ws."""
    terms = [TERM.fullmatch(t.strip()) for t in expr.split(" - ")]
    if not all(terms):
        raise ValueError(f"cannot parse {expr!r}")
    out = []
    for W in Ws:
        vals = []
        for t in terms:
            fn, gold, fam, ref = t.groups()
            gold = ds.complete if gold == "complete" else gold
            sl = [scores(ds.rows(s, gold, lx), idx, W) for s in fams[fam]]
            if fn == "slope":
                vals.append(stat_slope(sl, floor))
            elif fn == "b":
                vals.append(stat_b(sl, floor))
            else:
                rl = [scores(ds.rows(s, gold, lx), idx, W) for s in fams[ref]]
                vals.append(residuals(sl, rl, floor).mean(0))
        out.append(vals[0] - vals[1] if len(vals) == 2 else vals[0])
    return out


def analysis_families(reg: dict) -> dict[str, list[str]]:
    out = {}
    for keys, fams in reg["analysis_plan"]["analysis_set_families"].items():
        for k in keys.split(", "):
            out[k] = [f.split(" (")[0] for f in fams]
    return out


def evaluate_prediction(reg: dict, ds: Dataset, pred: dict, lx: str, fams: dict, sets: dict, clean: bool) -> dict:
    dc = reg["design_constants"]
    floor, lo_q, hi_q = dc["tp_floor"]["value"], dc["ci_lo_percentile"]["value"], dc["ci_hi_percentile"]["value"]
    used = sets[pred["id"]]
    missing = [s for f in used for s in fams.get(f, [None]) if s is None or s.partition(":")[0] not in ds.caps]
    if missing:
        return {"verdict": "NOT_EVALUABLE", "reason": f"systems missing or excluded: {missing}", "parts": []}
    systems = sorted({s for f in used for s in fams[f]})
    idx = ds.clean_index(systems, clean)
    n = len(idx)
    if n == 0:
        return {"verdict": "NOT_EVALUABLE", "reason": "empty analysis set", "n_images": 0, "parts": []}
    W = np.random.default_rng(dc["set_by_this_registration"]["bootstrap_seed"]).multinomial(
        n, np.full(n, 1.0 / n), size=dc["n_boot"]["value"]).astype(float)
    parts = []
    for part in pred["parts"]:
        point, rep = eval_stat(ds, part["stat"], fams, lx, idx, [np.ones((1, n)), W], floor)
        interval = ci(rep, lo_q, hi_q)
        p = float(point[0])
        parts.append({"stat": part["stat"], "rule": part["rule"], "delta": part.get("delta"), "point": p,
                      "ci95": interval,
                      "verdict": verdict(part["rule"], p, interval, part.get("delta")) if clean else None})
    out = {"n_images": n, "n_images_full": len(ds.ids), "systems": systems, "parts": parts}
    if clean:
        out["verdict"] = compound([x["verdict"] for x in parts]) if parts else None
    return out


def descriptive(reg: dict, ds: Dataset, fams: dict, lx: str, clean: bool) -> dict:
    """Per-system scores and per-gold family statistics of LADDER (with CIs), M*_mixed and sign agreement."""
    dc = reg["design_constants"]
    floor, lo_q, hi_q = dc["tp_floor"]["value"], dc["ci_lo_percentile"]["value"], dc["ci_hi_percentile"]["value"]
    lad = fams["LADDER"]
    if any(s not in ds.caps for s in lad):
        return {"note": "LADDER incomplete"}
    idx = ds.clean_index(lad, clean)
    n = len(idx)
    W = np.random.default_rng(dc["set_by_this_registration"]["bootstrap_seed"]).multinomial(
        n, np.full(n, 1.0 / n), size=dc["n_boot"]["value"]).astype(float)
    golds = [g for g in reg["golds"][ds.name]["variants"]]
    out = {"n_images": n, "golds": {}}
    for g in golds:
        pts = [scores(ds.rows(s, g, lx), idx, np.ones((1, n))) for s in lad]
        reps = [scores(ds.rows(s, g, lx), idx, W) for s in lad]
        slope, b = stat_slope(pts, floor)[0], stat_b(pts, floor)[0]
        med = float(np.median([float(p["M"][0]) for p in pts]))
        mm = mstar_mixed(pts, floor)
        scale = {"P": 100, "R": 100, "F": 100, "M": 1, "TP": 1}  # P, R, F1 in points, as in Table 7.1
        out["golds"][g] = {
            "systems": {s: {k: [float(scale[k] * pts[j][k][0]), ci(scale[k] * reps[j][k], lo_q, hi_q)]
                            for k in scale} for j, s in enumerate(lad)},
            "slope_F1_per_lnM": [float(slope), ci(stat_slope(reps, floor), lo_q, hi_q)],
            "b": [float(b), ci(stat_b(reps, floor), lo_q, hi_q)],
            "rmse_P": float(np.sqrt(np.mean(residuals(pts, pts, floor)[:, 0] ** 2))),
            "Mstar_mixed": mm, "median_M": med, "sign_agrees_with_Mstar_mixed": bool(np.sign(slope) == np.sign(mm - med))}
    return out


def guard_shares(ds: Dataset) -> dict:
    out = {}
    for rid, caps in ds.caps.items():
        lang = ds.lang.get(rid, "vi")
        vals = [c for i in ds.ids for c in ((caps.get(i) if isinstance(caps.get(i), list) else [caps.get(i)]) or [])
                if isinstance(c, str)]
        if vals:
            out[rid] = {"captions": len(vals), "cjk": sum(bool(CJK_RE.search(c)) for c in vals),
                        "not_vietnamese": None if lang == "en" else sum(not looks_vietnamese(c) for c in vals)}
    return out


def kill_rules(reg: dict, verdicts: dict, rmse: dict, excluded: dict) -> dict:
    rm = reg["design_constants"]["rmse_max_P"]["value"]
    k1_text = next(k["rule"] for k in reg["kill_rules"] if k["id"] == "K1")
    k1_min = int(re.search(r"FAIL on (\d+) or more", k1_text).group(1))  # the registered count (K1)
    p1 = [d for d, v in verdicts.items() if v.get("G2B-P1") == "FAIL"]
    p2 = [d for d, v in verdicts.items() if v.get("G2B-P2") == "FAIL"]
    e1 = [d for d, v in verdicts.items() if v.get("G2B-E1") == "FAIL"]
    k3 = [f"{d}:{g}" for d, gs in rmse.items() for g, v in gs.items() if v > rm]
    p2_sets = [d for d in verdicts if "G2B-P2" in verdicts[d]]
    return {"K1": {"datasets_with_P1_FAIL": p1, "min_count": k1_min, "fires": len(p1) >= k1_min},
            "K2": {"datasets_with_P2_FAIL": p2, "fires": bool(p2_sets) and sorted(p2) == sorted(p2_sets)},
            "K3": {"cells_rmse_above": k3, "fires": bool(k3)},
            "KN1": {"datasets_with_E1_FAIL": e1, "fires": bool(e1)},
            "KL": {"applied": True, "rule": "verdicts use clean subsets only"},
            "KD": {"excluded_runs": excluded, "fires": bool(excluded)}}


def score(outputs: Path, out: Path) -> int:
    reg = jload(PREREG)
    bad = check_pins(reg)
    if bad:
        raise SystemExit(f"pinned files differ from the prereg: {bad}")
    lang = {r["run_id"]: ("en" if r["prompt_mode"].endswith("_en") else "vi") for r in reg["runs"]}
    n_ids = {"cv295": reg["datasets"]["cv295"]["n_images"], "uv231": reg["datasets"]["uv231"]["n_images"],
             "xm600": reg["datasets"]["xm600"]["n_images"]}
    caps, excluded = load_runs(reg, outputs, n_ids)
    for d, recs in reg["comparators"].items():
        for rec in recs.values():
            if sha256_file(ROOT / rec["path"]) != rec["sha256"]:
                raise SystemExit(f"comparator {rec['path']} differs from its pin")
            caps[rec["path"]] = read_captions(ROOT / rec["path"])
    sets = analysis_families(reg)
    result = {"schema": SCHEMA, "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "scorer_sha256": sha256_file(Path(__file__)), "prereg_sha256": sha256_file(PREREG),
              "outputs_sha256": {f.name: sha256_file(f) for f in sorted(outputs.glob("g2b_q3_*")) if
                                 not f.name.endswith((".sha256", ".partial.jsonl"))},
              "excluded_runs": excluded, "datasets": {}}
    verdicts, rmse = {}, {}
    for name in ("cv295", "uv231", "xm600"):
        mine = {k: v for k, v in caps.items() if k.startswith(f"g2b_q3_{name}-") or k in
                {r["path"] for r in reg["comparators"][name].values()}}
        ds = Dataset(reg, name, mine, lang)
        fams = reg["families"][name]
        lexes = list(ds.lex)
        primary = lexes[0]
        block = {"primary_lexicon": primary, "predictions": {}, "secondary_lexicon": {}, "sensitivity_full_set": {},
                 "guard_shares": guard_shares(ds)}
        for pred in reg["predictions"]:
            if name not in pred["datasets"] or not pred["parts"]:
                continue
            block["predictions"][pred["id"]] = evaluate_prediction(reg, ds, pred, primary, fams, sets, clean=True)
            block["sensitivity_full_set"][pred["id"]] = evaluate_prediction(reg, ds, pred, primary, fams, sets,
                                                                            clean=False)
            if len(lexes) > 1 and pred["id"] in ("G2B-E1", "G2B-E2", "G2B-O1", "G2B-O2", "G2B-P1"):
                block["secondary_lexicon"][pred["id"]] = evaluate_prediction(reg, ds, pred, lexes[1], fams, sets,
                                                                             clean=True)
        block["descriptive"] = descriptive(reg, ds, fams, primary, clean=True)
        if len(lexes) > 1:
            block["descriptive_secondary_lexicon"] = descriptive(reg, ds, fams, lexes[1], clean=True)
        verdicts[name] = {k: v.get("verdict") for k, v in block["predictions"].items()}
        rmse[name] = {g: v["rmse_P"] for g, v in block["descriptive"].get("golds", {}).items()}
        block["e1_e2_o1_all_pass"] = all(verdicts[name].get(k) == "PASS" for k in ("G2B-E1", "G2B-E2", "G2B-O1"))
        result["datasets"][name] = block
    result["verdicts"] = verdicts
    result["kill_rules"] = kill_rules(reg, verdicts, rmse, excluded)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    Path(str(out) + ".sha256").write_text(f"{sha256_file(out)}  {out.name}\n", encoding="utf-8")
    print(json.dumps({"verdicts": verdicts, "kill_rules": {k: v.get("fires") for k, v in result["kill_rules"].items()}}))
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="mode", required=True)
    s1 = sub.add_parser("selfcheck")
    s1.add_argument("--out", type=Path, default=ROOT / "data/results/g2b/selfcheck.json")
    s2 = sub.add_parser("score")
    s2.add_argument("--outputs-dir", type=Path, required=True)
    s2.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    sys.exit(selfcheck(a.out) if a.mode == "selfcheck" else score(a.outputs_dir, a.out))


if __name__ == "__main__":
    main()
