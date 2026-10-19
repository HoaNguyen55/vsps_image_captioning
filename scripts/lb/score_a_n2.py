#!/usr/bin/env python3
"""A-N2 evaluator (Paper A, registered secondary) for manuscript/prereg/2026-10-19_a_n2_lvlm_gold_ladder.json (commit
327191c): 8 LVLMs on CV295 and UIT-ViIC test in English under the gold ladder. Every threshold, seed, family and rule is
read from the prereg; golds, scores, slopes and the sign/compound rules are scripts/g2b/score_g2b.py's, unchanged.
    score_a_n2.py gate   OUT.json   provenance of every input, the self-check (score_g2b's COCO-2500 slope cells) and
                                    the random reference subsets; reads no decode output
    score_a_n2.py dryrun OUT.json   SYNTHETIC golds and decode files end to end, through admission and every statistic
    score_a_n2.py run    OUT.json --gate G.json --outputs DIR [--g2b-results R.json --g2b-outputs D]
                                    the analysis; only with this file and G.json (an all-PASS gate) committed at HEAD
Outputs are never overwritten."""
from __future__ import annotations

import argparse
import functools
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

import numpy as np

HERE = Path(__file__).resolve()
ROOT = Path(subprocess.run(["git", "-C", str(HERE.parent), "rev-parse", "--show-toplevel"], capture_output=True,
                           text=True, check=True).stdout.strip())
sys.path[:0] = [str(ROOT), str(ROOT / "scripts"), str(ROOT / "scripts/g2b")]
PREREG = ("manuscript/prereg/2026-10-19_a_n2_lvlm_gold_ladder.json",
          "d5714e2b25e5f1d36fa42813cc5891a82d0b80a73e69fb08d940e05e2055f309")
JOB = ("scripts/queue/jobs/lb_a_n2_decode.sh", "efdde495987b477e96cf2fd4114709b0a03218e7aac2357bc4e19f677998330a")
G2B = "manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.json"  # GREEDY_EN families (pinned in frozen_files)
REGISTERED = "327191c7104439cf3903040f8b1d94ce2acc695a"  # the commit of the prereg, the decoder and the job (CC-033b)
SELFCHECK, FAMILY = "data/results/g2b/selfcheck.json", "COCO-2500 (check_coco)"  # score_g2b's committed self-check
LX = "coco80"  # score_g2b's key of the 80-class lexicon (en_classes on English text)
SEEN: dict[str, str] = {}  # every input read, with its sha256
g = None  # scripts/g2b/score_g2b.py, imported once its pins match


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pinned(rel, want: str | None = None, head: bool = True) -> bytes:
    """Bytes of `rel`, refused unless its sha256 is the pin `want` (if given) and, if `head`, its blob at HEAD."""
    p = ROOT / rel
    data = p.read_bytes()
    if head and data != subprocess.run(["git", "-C", str(ROOT), "cat-file", "blob", f"HEAD:{rel}"],
                                       capture_output=True).stdout or want and sha(data) != want:
        raise SystemExit(f"PROVENANCE FAIL: {rel} (sha256 {sha(data)}) differs from its pin or from its blob at HEAD")
    SEEN[p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.name] = sha(data)
    return data


def config(P: dict) -> dict:
    """Constants from the prereg; refused if a registered sentence no longer reads as this scorer implements it."""
    ap, dc, pr = P["analysis_plan"], P["design_constants"], {p["id"]: p for p in P["predictions"]}
    sub = re.match(r"numpy\.random\.default_rng\((\d+)\); for k = 1\.\.K \(K = (\d+) on cv295 and uv231en\), for r = "
                   r"1\.\.(\d+), for each image of the FULL dataset in id order: choice\(n_refs_image, k, replace=False\)",
                   ap["random_subsets"])
    boot = re.match(r"(\d+) image-bootstrap draws per analysis set: numpy\.random\.default_rng\((\d+)\)\.multinomial\("
                    r"N, \[1/N\]\*N, size=(\d+)\) over the set's images in id order.* percentiles ([\d.]+) and ([\d.]+) "
                    r"of the replicates", ap["bootstrap"])
    p1 = re.match(r"`tau_b\(F1\[(\w+)\]\((\w+)\), F1\[(\w+)\]\((\w+)\)\)` (tau_lt) \(tau0 ([\d.]+);", pr["LBA-P1"]["rule"])
    km = re.search(r"fewer than (\d+) of the (\d+) models remain", next(k for k in P["kill_rules"] if k["id"] == "KM")["then"])
    ka = {k["id"]: re.findall(r"\b(cv295|uv231en)\b", k["when"]) for k in P["kill_rules"] if k["id"] in ("KA1", "KA2")}
    cfg = {"subset_seed": int(sub[1]), "K": int(sub[2]), "n_rep": int(sub[3]), "boot_seed": int(boot[2]),
           "n_boot": dc["n_boot"]["value"], "ci": dc["ci_percentiles"], "tau0": pr["LBA-P1"]["tau0"],
           "p1": dict(zip(("g1", "fam", "g2"), p1.groups())), "p2": re.findall(r"`([^`]+)` (sign_gt_0)",
                                                                           pr["LBA-P2"]["rule"]),
           "km_min_models": int(km[1]), "ka_sets": ka, "complete": {d: v["complete"].split(":")[0]
                                                                    for d, v in P["golds"].items()}}
    if not (int(boot[1]) == int(boot[3]) == cfg["n_boot"] and [float(boot[4]), float(boot[5])] == cfg["ci"]
            and float(p1[6]) == cfg["tau0"] == dc["tau0"]["value"] and p1[2] == p1[4] == "DETAILED"
            and len(cfg["p2"]) == 3 and pr["LBA-P2"]["rule"].endswith("; per set models_compound")
            and int(km[2]) == len(P["models"]) and set(cfg["complete"].values()) == {"inst"}
            and "[complete] = inst on both sets" in ap["tau"] and ka == {"KA1": ["cv295"], "KA2": ["cv295", "uv231en"]}
            and "(English: non-empty and clean_supervision.CJK_RE finds no match)" in ap["analysis_set"]
            and "fewer than half of the registered models are evaluable" in P["verdict_rules"]["models_compound"]
            and all(f"refs{cfg['K']}_randk" in v["variants"] for v in P["golds"].values())):
        raise SystemExit("REFUSED: a registered constant does not read as this scorer implements it")
    return cfg


def modules(F: dict):
    """score_g2b once it, the matchers and the data it reads at import match their pins; then every repo module
    loaded by that import must be committed unmodified at HEAD."""
    for rel in ("scripts/g2b/score_g2b.py", "scripts/score_coco_probe.py", "scripts/clean_supervision.py",
                "data/coco_probe/chair_synonyms.txt"):
        pinned(rel, F[rel])
    pinned("data/coco_probe/coco80_vi.json")  # read by score_g2b at import (load_vi_terms); unused for English
    import score_g2b
    for f in sorted({Path(getattr(x, "__file__", None) or "/").resolve() for x in list(sys.modules.values())} - {HERE}):
        if f.is_relative_to(ROOT):
            pinned(f.relative_to(ROOT).as_posix())
    return score_g2b


def contexts(P: dict, F: dict, cfg: dict) -> dict:
    """Per set, before any output is read: ids (manifest order, which is id order), image shas, the gold lexicon by
    score_g2b's conventions, the registered random reference subsets and every registered gold variant."""
    out, en = {}, g.MATCH[LX]["en"]
    for ds, spec in P["datasets"].items():
        rows = [r.split("\t") for r in pinned(spec["manifest"]["path"], spec["manifest"]["sha256"]).decode().splitlines()]
        ids = [r[0] for r in rows]
        if ds == "cv295":  # English Karpathy sentences (first 5) and COCO-2014 instance classes: score_g2b.coco_context
            want = pinned("data/coco_probe/probe_val2017_ids.txt", F["data/coco_probe/probe_val2017_ids.txt"]).split()
            pinned("data/coco_probe/instance_gold.json", F["data/coco_probe/instance_gold.json"])
            pinned("data/datasets/karpathy/dataset_coco.json", F["data/datasets/karpathy/dataset_coco.json"], head=False)
            lex, want = g.coco_context(ids)["lexicons"][LX], [x.decode() for x in want]
        else:  # the first 5 COCO English captions (uitviic_en) and the UIT-ViIC test COCO instance classes
            en_refs = "data/datasets/uitviic_en/test_data.json"
            pinned(en_refs, F[en_refs], head=False)
            refs = g.ann_refs(ROOT / en_refs)
            inst = json.loads(pinned("data/uitviic/instance_gold.json", F["data/uitviic/instance_gold.json"]))
            lex, want = {"refs": [[en(s) for s in refs[i][:5]] for i in ids],
                         "complete": [set(inst[i]["coco"]) for i in ids]}, list(refs)
        n_refs = [len(r) for r in lex["refs"]]
        if ids != sorted(want, key=int) or len(ids) != spec["n_images"] or min(n_refs) < cfg["K"]:
            raise SystemExit(f"REFUSED: {ds}: the manifest ids, the references or their counts fail their checks")
        sub = g.random_subsets(n_refs, cfg["K"], cfg["n_rep"], cfg["subset_seed"])
        var = g.gold_variants(lex, sub)
        out[ds] = {"ids": ids, "sha": {r[0]: r[2] for r in rows},
                   "variants": {k: var[k] for k in P["golds"][ds]["variants"]},
                   "facts": {"n_images": len(ids), "refs_per_image_min_max": [min(n_refs), max(n_refs)],
                             "random_subsets_sha256": sha(json.dumps(sub, sort_keys=True).encode())}}
    return out


def bank(ment: dict, ctx: dict, complete: str, **kw) -> SimpleNamespace:
    """What score_g2b.eval_stat reads of a score_g2b Dataset (rows(system, gold, lexicon), the complete gold's name),
    the registered gold names and, for an A-N2 set, its KM-kept models and their families (kw)."""
    return SimpleNamespace(rows=functools.cache(lambda s, gold, _lx: g.rows(ment[s], ctx["variants"][gold])),
                           complete=complete, golds=list(ctx["variants"]), **kw)


def tau_b(x, y):
    """Kendall tau-b over axis 0 (systems), per column: (concordant - discordant) / sqrt(pairs untied in x * pairs
    untied in y); nan when a vector is all ties or holds a nan."""
    i, j = np.triu_indices(len(x), 1)
    dx, dy = np.sign(x[i] - x[j]), np.sign(y[i] - y[j])
    with np.errstate(invalid="ignore", divide="ignore"):
        return (dx * dy).sum(0) / np.sqrt((dx != 0).sum(0) * (dy != 0).sum(0))


def tau_lt(point: float, ci: list | None, tau0: float) -> str:
    """verdict_rules.tau_lt; NOT_EVALUABLE when the point or the CI is undefined (score_g2b.verdict's convention)."""
    if ci is None or not np.isfinite(point):
        return "NOT_EVALUABLE"
    return "PASS" if ci[1] < tau0 else "FAIL" if point >= tau0 else "INCONCLUSIVE"


def models_compound(verdicts: list[str], n_registered: int) -> str:
    """verdict_rules.models_compound over the KM-kept models' compound verdicts; FAIL is checked first, as in compound."""
    ev = [v for v in verdicts if v != "NOT_EVALUABLE"]
    if "FAIL" in ev:
        return "FAIL"
    if len(ev) < n_registered / 2:
        return "NOT_EVALUABLE"
    return "PASS" if all(v == "PASS" for v in ev) else "INCONCLUSIVE"


def registered(P: dict, run: dict, ctx: dict) -> dict:
    """The provenance scripts/lb/decode_hf_vlm.py records for `run` when the decode tests this registration."""
    m, n = P["models"][run["model"]], P["decode"]["max_new_tokens"][run["prompt_mode"]]
    return {"schema": "vsps.lb_decode.v1", "prereg_id": P["prereg_id"], "prereg_sha256": PREREG[1],
            "decoder_sha256": P["decoder"]["sha256"], "job_sha256": JOB[1], **run,
            **{k: m[k] for k in ("hub_id", "revision", "batch_size", "dtype", "attn_implementation", "processor_kwargs")},
            "prompt_text_sha256": P["decode"]["prompts"][run["prompt_mode"]]["text_sha256"],
            "manifest_sha256": P["datasets"][run["dataset"]]["manifest"]["sha256"], "max_new_tokens": n,
            "generate_kwargs": {"max_new_tokens": n, "do_sample": False, "num_beams": 1},
            "packages": P["venv"]["packages"], "n_images": len(ctx["ids"]), "image_sha256": ctx["sha"]}


def admit(P: dict, run: dict, odir: Path, ctx: dict) -> tuple[dict | None, list[str]]:
    """(output, []) when the decode tests this registration, else (None, reasons): its sha256 sidecar; CC-033b (decoder
    and job sha, a git_head that contains the registration commit); KD (every registered setting); the manifest."""
    f = odir / f"{run['run_id']}.preds.json"
    side = Path(f"{f}.sha256")
    if not (f.is_file() and side.is_file()):
        return None, ["output or its sha256 sidecar missing"]
    data = f.read_bytes()
    SEEN[f"outputs/{f.name}"] = h = sha(data)
    if h != side.read_text(encoding="utf-8").split()[0]:
        return None, ["sha256 differs from its sidecar"]
    o = json.loads(data)
    bad = [f"{k} differs from the registration" for k, v in registered(P, run, ctx).items() if o.get(k) != v]
    if subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", REGISTERED, str(o.get("git_head"))],
                      capture_output=True).returncode:
        bad.append(f"git_head {o.get('git_head')} does not contain {REGISTERED[:7]}")
    if o.get("predictions", {}).keys() != ctx["sha"].keys() or not all(isinstance(c, str)
                                                                         for c in o["predictions"].values()):
        bad.append("captions do not cover exactly the manifest's images")
    return (None, bad) if bad else (o, [])


def load_runs(P: dict, odir: Path, ctxs: dict) -> tuple[dict, dict, dict]:
    """Admitted captions and per-run facts by run id, and every exclusion with its reasons, in prereg run order."""
    caps, facts, excluded = {}, {}, {}
    for run in P["runs"]:
        o, why = admit(P, run, odir, ctxs[run["dataset"]])
        if why:
            excluded[run["run_id"]] = why
            continue
        caps[run["run_id"]] = o["predictions"]
        facts[run["run_id"]] = {k: o[k] for k in ("machine_id", "git_head", "git_dirty", "parity_slice0")} | {
            "hit_max_share": float(np.mean(list(o["hit_max"].values())))}
    return caps, facts, excluded


def stats(P: dict, cfg: dict, B: SimpleNamespace, idx: np.ndarray, verdicts: bool) -> dict:
    """LBA-P1, LBA-P2 and (with verdicts) the descriptive tables over the images idx, on one set of shared draws."""
    n, spec, fam, kept = len(idx), {r["run_id"]: r["model"] for r in P["runs"]}, B.fam, B.kept
    if not n:
        return {"n_images": 0, "LBA-P1": {"verdict": "NOT_EVALUABLE"}, "LBA-P2": {"models": {}, "verdict": "NOT_EVALUABLE"}}
    Ws = [np.ones((1, n)), np.random.default_rng(cfg["boot_seed"]).multinomial(n, [1 / n] * n, size=cfg["n_boot"])
          .astype(float)]
    ci = functools.partial(g.ci, lo_q=cfg["ci"][0], hi_q=cfg["ci"][1])
    runs = [r for m in kept for r in fam[f"PAIR_{m}"]]
    S = {(r, gl): [g.scores(B.rows(r, gl, LX), idx, W) for W in Ws] for r in runs for gl in B.golds}

    def tau(g1: str, g2: str, f: str) -> dict:
        if not fam[f]:
            return {"point": float("nan"), "ci95": None, "n_models": 0}
        x, y = ([np.stack([S[(r, B.complete if gl == "complete" else gl)][k]["F"] for r in fam[f]]) for k in (0, 1)]
                for gl in (g1, g2))
        return {"point": float(tau_b(x[0], y[0])[0]), "ci95": ci(tau_b(x[1], y[1])), "n_models": len(fam[f])}

    def slope(expr: str, m: str) -> tuple[float, list | None]:
        pt, rep = g.eval_stat(B, expr.replace("PAIR_m", "PAIR"), {"PAIR": fam[f"PAIR_{m}"]}, LX, idx, Ws, None)
        return float(pt[0]), ci(rep)

    p1 = cfg["p1"]
    out = {"n_images": n, "LBA-P1": tau(p1["g1"], p1["g2"], p1["fam"]), "LBA-P2": {"models": {}}}
    for m in kept:
        parts = [dict(zip(("stat", "rule", "point", "ci95"), (e, r, *slope(e, m)))) for e, r in cfg["p2"]]
        for p in parts if verdicts else []:
            p["verdict"] = g.verdict(p["rule"], p["point"], p["ci95"])
        out["LBA-P2"]["models"][m] = {"parts": parts} | ({"verdict": g.compound([p["verdict"] for p in parts])}
                                                         if verdicts else {})
    if not verdicts:
        return out
    out["LBA-P1"]["verdict"] = "NOT_EVALUABLE" if len(kept) < cfg["km_min_models"] else tau_lt(
        out["LBA-P1"]["point"], out["LBA-P1"]["ci95"], cfg["tau0"])
    out["LBA-P2"]["verdict"] = models_compound([v["verdict"] for v in out["LBA-P2"]["models"].values()],
                                               len(P["models"]))
    scale, K = {"P": 100, "R": 100, "F": 100, "M": 1}, f"refs{cfg['K']}_randk"
    out["descriptive"] = {
        "scores_P_R_F1_x100_M": {r: {gl: {k: [float(s * S[(r, gl)][0][k][0]), ci(s * S[(r, gl)][1][k])]
                                          for k, s in scale.items()} for gl in B.golds} for r in runs},
        "slopes_not_predicted": {m: {f"slope[{gl}](PAIR_m)": slope(f"slope[{gl}](PAIR_m)", m) for gl in (p1["g1"], K)}
                                 for m in kept},
        "tau_b": {f"{a} vs complete ({f})": tau(a, "complete", f) for f, a in (("DETAILED", "refs_all"),
                                                                              ("SHORT", p1["g1"]), ("SHORT", "refs_all"))},
        "ranking_by_F1": {f: {gl: [spec[r] for r in sorted(fam[f], key=lambda r: -S[(r, gl)][0]["F"][0])]
                              for gl in B.golds} for f in ("DETAILED", "SHORT")}}
    return out


def analyse(P: dict, cfg: dict, ds: str, ctx: dict, caps: dict) -> dict:
    """One set: KM, the clean analysis set (KL), LBA-P1 and LBA-P2 with verdicts and the descriptive tables on it; the
    same predictions on all images as a sensitivity analysis without verdicts."""
    kept = [m for m in P["models"] if all(r in caps for r in P["families"][ds][f"PAIR_{m}"])]
    runs = [r for m in kept for r in P["families"][ds][f"PAIR_{m}"]]
    fam = {f: [r for r in rs if r in runs] for f, rs in P["families"][ds].items()}
    ids, en = ctx["ids"], g.MATCH[LX]["en"]
    B = bank({r: g.mentions(caps[r], ids, en) for r in runs}, ctx, cfg["complete"][ds], fam=fam, kept=kept)
    clean = np.array([k for k, i in enumerate(ids) if all(g.is_clean(caps[r][i], "en") and caps[r][i].strip()
                                                          for r in runs)], int)
    return {"models_kept": kept, "models_left_by_KM": [m for m in P["models"] if m not in kept], "n_images": len(ids),
            "analysis_set_n": len(clean), "verdicts_on_analysis_set": stats(P, cfg, B, clean, True),
            "sensitivity_all_images": stats(P, cfg, B, np.arange(len(ids)), False)}


def kill_rules(P: dict, cfg: dict, res: dict, excluded: dict) -> dict:
    v = {ds: r["verdicts_on_analysis_set"] for ds, r in res.items()}
    fails = {ds: [m for m, x in v[ds]["LBA-P2"]["models"].items() if x["verdict"] == "FAIL"] for ds in v}
    return {"KA1": {"fires": any(v[d]["LBA-P1"]["verdict"] == "FAIL" for d in cfg["ka_sets"]["KA1"])},
            "KA2": {"fires": any(v[d]["LBA-P2"]["verdict"] == "FAIL" for d in cfg["ka_sets"]["KA2"]),
                    "failing_models": fails},
            "KM": {ds: r["models_left_by_KM"] for ds, r in res.items()},
            "KL": {ds: r["analysis_set_n"] for ds, r in res.items()}, "KD_and_CC-033b_exclusions": excluded}


def selfcheck(F: dict) -> list[dict]:
    """score_g2b's COCO-2500 family (9 systems, 2,500 images, single golds) through this scorer's path (bank and
    score_g2b.eval_stat): every slope cell of the committed selfcheck.json, at score_g2b's 2-decimal precision for it.
    Its captions are Vietnamese, matched as score_g2b.selfcheck does (coco80 'vi'); its golds are A-N2's cv295 golds."""
    S = json.loads(pinned(SELFCHECK))
    ref = ".session_backup/2026-10-14/r11_litmaps/L1/check_coco.json"
    pinned(ref, S["references_sha256"][ref], head=False)
    man = json.loads(pinned("data/coco_probe/manifest.json", F["data/coco_probe/manifest.json"]))
    ids = [str(i["cocoid"]) for i in sorted(man["images"], key=lambda x: x["cocoid"])]
    files = sorted(f.relative_to(ROOT).as_posix() for d in ("coco5000", "coco_transfer", "coco5000_vcd")
                   for f in (ROOT / "data/results" / d).glob("*.shard*.jsonl"))
    for rel in files:
        pinned(rel)
    lex, vi = g.coco_context(ids)["lexicons"][LX], g.MATCH[LX]["vi"]
    B = bank({f: g.mentions(g.read_captions(ROOT / f), ids, vi) for f in files},
             {"variants": g.gold_variants(lex, None, firstk=True)}, "inst")
    out = []
    for c in (c for c in S["cells"] if c["family"] == FAMILY and c["stat"] == "slope"):
        mine = g.eval_stat(B, f"slope[{c['gold']}](ALL)", {"ALL": files}, LX, np.arange(len(ids)),
                           [np.ones((1, len(ids)))], None)[0][0]
        out.append({"gold": c["gold"], "reference": c["reference"], "reproduced": round(float(mine), 2),
                    "ok": round(float(mine), 2) == c["reference"] == c["reproduced"]})
    return out


def gate(P: dict, F: dict, cfg: dict) -> tuple[dict, dict]:
    """Provenance of every input, the golds and random subsets, then the self-check; reads no decode output."""
    pinned(P["decoder"]["path"], P["decoder"]["sha256"])
    pinned(*JOB)
    if subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", REGISTERED, "HEAD"]).returncode:
        raise SystemExit(f"REFUSED: HEAD does not contain the registration commit {REGISTERED[:7]}")
    ctxs, sc = contexts(P, F, cfg), selfcheck(F)
    return {"sets": {ds: c["facts"] for ds, c in ctxs.items()}, "self_check": {"family": FAMILY, "cells": sc},
            "all_pass": len(sc) > 0 and all(c["ok"] for c in sc), "decode_outputs_read": False}, ctxs


def g2b_exact(P: dict, caps: dict, results: str, odir: str) -> dict:
    """Qwen3-VL exact-match share with G2-B's GREEDY_EN decodes (descriptive), read only after G2-B is scored: G2-B's
    results file must be committed at HEAD and each decode must hash to the sha256 it records (CC-027 (c))."""
    R = json.loads(pinned(Path(results).resolve().relative_to(ROOT).as_posix()))
    G = json.loads(pinned(G2B, {r["path"]: r["sha256"] for r in P["frozen_files"]}[G2B]))
    if R.get("schema") != "vsps.g2b_score.v1":
        raise SystemExit("REFUSED: --g2b-results is not a G2-B score file")
    q = next(k for k, m in P["models"].items() if m["hub_id"] == G["model"]["hub_id"])
    out = {}
    for ds, theirs in (("cv295", "cv295"), ("uv231en", "uv231")):
        for rid in G["families"][theirs]["GREEDY_EN"]:
            mine, f = f"lbA_{q}_{ds}-{rid.split('-')[1]}", Path(odir) / f"{rid}.preds.json"
            pinned(f, R["outputs_sha256"][f.name], head=False)
            t = g.read_captions(f)
            out[mine] = {"vs": rid, "share": float(np.mean([caps[mine][i] == t.get(i) for i in sorted(caps[mine],
                                                                                                    key=int)]))
                         } if mine in caps else "run excluded or missing"
    return out


def run(P: dict, F: dict, cfg: dict, a) -> dict:
    """The registered analysis, only from this scorer committed at HEAD with its committed all-PASS gate output."""
    pinned(HERE.relative_to(ROOT).as_posix())
    rel = Path(a.gate).resolve().relative_to(ROOT).as_posix()
    G = json.loads(pinned(rel))
    if [G["mode"], G["all_pass"], G["script_sha256"], G["prereg"]["sha256"]] != ["gate", True, sha(HERE.read_bytes()),
                                                                                  PREREG[1]]:
        raise SystemExit("REFUSED: the gate file is not a committed all-PASS gate of this scorer")
    body, ctxs = gate(P, F, cfg)
    if not body["all_pass"] or body["sets"] != G["sets"]:
        raise SystemExit("REFUSED: the self-check failed, or the sets or random subsets differ from the gate's")
    caps, facts, excluded = load_runs(P, Path(a.outputs), ctxs)
    spec = {r["run_id"]: r["dataset"] for r in P["runs"]}
    res = {ds: analyse(P, cfg, ds, ctx, {r: c for r, c in caps.items() if spec[r] == ds}) for ds, ctx in ctxs.items()}
    return {"gate": {"path": rel, "sha256": SEEN[rel]}, "self_check": body["self_check"], "excluded_runs": excluded,
            "runs": facts, "datasets": res, "kill_rules": kill_rules(P, cfg, res, excluded),
            "qwen3vl_exact_match_vs_g2b": g2b_exact(P, caps, a.g2b_results, a.g2b_outputs) if a.g2b_results else
            "not computed: G2-B's GREEDY_EN decodes are read only after G2-B is scored (CC-027 (c))"}


def selftest(cfg: dict) -> bool:
    """Toy cases with known answers; reads no data file."""
    from scipy.stats import kendalltau
    assert abs(tau_b(np.array([1, 2, 2, 3]), np.array([1, 2, 3, 3])) - 0.8) < 1e-12  # C 4, D 0, one tie in each
    X, Y = np.random.default_rng(5).integers(0, 4, (2, 8, 40))  # 8 systems, 40 columns, many ties
    assert np.allclose(tau_b(X, Y), [kendalltau(X[:, b], Y[:, b], variant="b").statistic for b in range(40)],
                       equal_nan=True)
    assert [tau_lt(p, c, cfg["tau0"]) for p, c in ((0.5, [0.1, 0.89]), (0.9, [0.5, 1.0]), (0.8, [0.5, 0.95]),
                                                   (np.nan, None))] == ["PASS", "FAIL", "INCONCLUSIVE", "NOT_EVALUABLE"]
    assert [models_compound(v, 8) for v in (["PASS"] * 4, ["PASS"] * 3 + ["NOT_EVALUABLE"], ["PASS", "FAIL"],
                                            ["PASS"] * 5 + ["INCONCLUSIVE"])] == \
        ["PASS", "NOT_EVALUABLE", "FAIL", "INCONCLUSIVE"]
    assert not g._check_rules()  # score_g2b's own unit checks of sign_gt_0, compound and NOT_EVALUABLE
    try:
        pinned(PREREG[0], "0" * 64)
    except SystemExit as refused:
        assert "PROVENANCE FAIL" in str(refused)
        return True
    raise AssertionError("a wrong pin was accepted")


def dryrun(P: dict, cfg: dict) -> dict:
    """SYNTHETIC: made-up ids, references, instance classes and captions; 32 decode files written with the registered
    provenance go through admission, KM, the analysis set and every statistic. Even-indexed models name the 2 classes
    every reference names, odd ones every instance class, each with k//2 false classes: one-reference gold ranks the
    first kind higher and complete gold the second (LBA-P1 PASS on cv295 is built in). On uv231en three runs carry a
    wrong job sha, a wrong decoder sha and a git_head before the registration, so KM keeps 5 models there."""
    rng, en = np.random.default_rng(11), g.MATCH[LX]["en"]
    words = ("dog cat car bus horse sheep cow bird boat bench chair clock vase book cup bowl banana apple pizza cake "
             "kite truck train umbrella").split()
    git = functools.partial(subprocess.run, capture_output=True, text=True, check=True)
    head, before = (git(["git", "-C", str(ROOT), "rev-parse", r]).stdout.strip() for r in ("HEAD", f"{REGISTERED}^"))
    models, ctxs = list(P["models"]), {}
    bad = {f"lbA_{models[1]}_uv231en-short_en": {"job_sha256": "0" * 64},
           f"lbA_{models[2]}_uv231en-detailed_en": {"decoder_sha256": "0" * 64},
           f"lbA_{models[3]}_uv231en-short_en": {"git_head": before}}
    with tempfile.TemporaryDirectory() as tmp:
        for ds, n in (("cv295", 120), ("uv231en", 80)):
            ids = [str(100 + 7 * k) for k in range(n)]
            inst = {i: [str(w) for w in rng.choice(words, rng.integers(4, 7), replace=False)] for i in ids}
            refs = {i: [f"A photo of a {inst[i][0]} and a {inst[i][1]}" + (f" by a {rng.choice(inst[i][2:])}" if
                                                                          rng.random() < 0.3 else "") + "."
                        for _ in range(5)] for i in ids}
            lex = {"refs": [[en(s) for s in refs[i]] for i in ids], "complete": [set(inst[i]) for i in ids]}
            var = g.gold_variants(lex, g.random_subsets([5] * n, cfg["K"], cfg["n_rep"], cfg["subset_seed"]))
            ctxs[ds] = {"ids": ids, "sha": {i: sha(i.encode()) for i in ids},
                        "variants": {k: var[k] for k in P["golds"][ds]["variants"]}}
            for run in (r for r in P["runs"] if r["dataset"] == ds):
                k = models.index(run["model"])
                caps = {i: "A " + " and a ".join(inst[i][:1 + (k >= 4)]) + "." if run["prompt_mode"] == "short_en"
                        else "There is a " + ", a ".join(
                    (inst[i] if k % 2 else inst[i][:2]) + [str(w) for w in rng.choice(
                        [w for w in words if w not in inst[i]], k // 2, replace=False)]) + "." for i in ids}
                if ds == "cv295" and k < 2:
                    caps[ids[3 + k]] = "一只狗" if k else ""  # two captions outside the analysis set (KL)
                o = registered(P, run, ctxs[ds]) | {"git_head": head, "git_dirty": False, "machine_id": "synthetic",
                                                    "parity_slice0": {"n": 2, "identical": 2}, "predictions": caps,
                                                    "hit_max": {i: i == ids[0] for i in ids}} | bad.get(run["run_id"], {})
                f = Path(tmp) / f"{run['run_id']}.preds.json"
                f.write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding="utf-8")
                Path(f"{f}.sha256").write_text(f"{sha(f.read_bytes())}  {f.name}\n", encoding="utf-8")
        caps, facts, excluded = load_runs(P, Path(tmp), ctxs)
    spec = {r["run_id"]: r["dataset"] for r in P["runs"]}
    res = {ds: analyse(P, cfg, ds, ctxs[ds], {r: c for r, c in caps.items() if spec[r] == ds}) for ds in ctxs}
    cv, uv = (res[d]["verdicts_on_analysis_set"] for d in ("cv295", "uv231en"))
    kr = kill_rules(P, cfg, res, excluded)
    assert {r: [w.split()[0] for w in why] for r, why in excluded.items()} == {
        r: [next(iter(o))] for r, o in bad.items()}
    assert res["cv295"]["analysis_set_n"] == 118 and res["uv231en"]["models_kept"] == models[:1] + models[4:]
    assert cv["LBA-P1"]["verdict"] == "PASS" and uv["LBA-P1"]["verdict"] == "NOT_EVALUABLE"  # 5 of 8 kept (KM)
    assert all(cv["LBA-P2"]["models"][m]["verdict"] == "PASS" for m in models[1::2])  # every instance class named
    assert kr["KA2"]["fires"] and models[0] in kr["KA2"]["failing_models"]["cv295"] and not kr["KA1"]["fires"]
    assert all(np.isfinite(t["point"]) for r in (cv, uv) for t in r["descriptive"]["tau_b"].values())
    assert all(p["ci95"] for r in (cv, uv) for x in r["LBA-P2"]["models"].values() for p in x["parts"])
    assert "verdict" not in json.dumps(res["cv295"]["sensitivity_all_images"])
    assert len(facts) == 29 and facts[f"lbA_{models[0]}_cv295-short_en"]["hit_max_share"] == 1 / 120
    return {"SYNTHETIC": "made-up ids, references, instance classes and captions; no reference, gold, manifest or "
                         "decode file is read", "excluded_runs": excluded, "datasets": res, "kill_rules": kr}


def main() -> int:
    global g
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=("gate", "dryrun", "run"))
    ap.add_argument("out")
    ap.add_argument("--gate", help="run: the committed output of gate")
    ap.add_argument("--outputs", help="run: the folder of the 32 decode outputs and their .sha256 sidecars")
    ap.add_argument("--g2b-results", help="run: G2-B's committed results file (enables the exact-match share)")
    ap.add_argument("--g2b-outputs", help="run: the folder of G2-B's decodes")
    a = ap.parse_args()
    if Path(a.out).exists() or (a.mode == "run" and not (a.gate and a.outputs)) or bool(a.g2b_results) != bool(
            a.g2b_outputs):
        raise SystemExit("REFUSED: OUT exists (never overwritten), run lacks --gate/--outputs, or one --g2b-* is alone")
    P = json.loads(pinned(*PREREG))
    F, cfg = {r["path"]: r["sha256"] for r in P["frozen_files"]}, config(P)
    g = modules(F)
    head = {"id": P["prereg_id"], "mode": a.mode, "prereg": dict(zip(("path", "sha256"), PREREG)),
            "script_sha256": sha(HERE.read_bytes()), "config": cfg, "toy_selftest_pass": selftest(cfg)}
    body = gate(P, F, cfg)[0] if a.mode == "gate" else dryrun(P, cfg) if a.mode == "dryrun" else run(P, F, cfg, a)
    with open(a.out, "x", encoding="utf-8") as f:  # "x": an existing output is never overwritten
        json.dump(head | body | {"inputs_sha256": SEEN}, f, ensure_ascii=False, indent=1, default=lambda o: o.item())
    print(json.dumps({"mode": a.mode, "all_pass": body.get("all_pass"), "excluded": list(body.get("excluded_runs", {})),
                      "verdicts": {d: {p: r["verdicts_on_analysis_set"][p].get("verdict") for p in ("LBA-P1", "LBA-P2")}
                                   for d, r in body.get("datasets", {}).items()}}))
    return 0 if body.get("all_pass", True) else 1


if __name__ == "__main__":
    sys.exit(main())
