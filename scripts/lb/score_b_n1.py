#!/usr/bin/env python3
"""B-N1 scorer (Paper B) for manuscript/prereg/2026-10-19_b_n1_vi_leaderboard.json (commit 327191c): 4 public VLMs on
KTVIC test (the full 558 for verdicts, the clean 157 as a sensitivity) and UIT-ViIC test; CIDEr-D from scripts/evaluate.py
run unchanged, as written and with the punctuation fix (scoring.fix); every threshold is read from the prereg.
    score_b_n1.py gate   OUT.json                              provenance of every input and the self-check on the
                                                               reference rows; reads no decode output
    score_b_n1.py dryrun OUT.json                              SYNTHETIC references, splits and decode files end to end
    score_b_n1.py run    OUT.json --gate G.json --outputs DIR  the analysis; only with this file and G.json at HEAD
Needs NCS_DATA, VNCORENLP_DIR, JAVA_HOME (a JDK, for jnius), `java` on PATH and RESCAP_RAW_TONE unset. Outputs are never
overwritten."""
from __future__ import annotations

import argparse
import functools
import hashlib
import importlib
import json
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from importlib.metadata import version
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
ROOT = Path(subprocess.run(["git", "-C", str(HERE.parent), "rev-parse", "--show-toplevel"], capture_output=True,
                           text=True, check=True).stdout.strip())
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
PREREG = ("manuscript/prereg/2026-10-19_b_n1_vi_leaderboard.json",
          "9ff02dc259258de1add426abd02131f2122e3476a81f9a076066ed6d74906134")
JOB = ("scripts/queue/jobs/lb_b_n1_decode.sh", "836612617f456deb112986a6f9b0b7b949528fcd85ea9393c9d62a4fa1ff7372")
REGISTERED = "327191c7104439cf3903040f8b1d94ce2acc695a"  # the commit of the prereg, the decoder and the job (CC-033b)
STATS = {"LBB-P1": "tau_b(CIDEr_as_written(ZS), CIDEr_fix(ZS))",  # the statistics this scorer computes
         "LBB-P2": "tau_b(CIDEr_fix(ZS) on the full ktvic_test, CIDEr_fix(ZS) on uitviic_test)",
         "LBB-P3": "tau_b(fix) - tau_b(as written)"}
FIX = ("the punctuation fix: strip trailing whitespace and the characters . ! ? ... (U+2026) from the end of every "
       "candidate AND every reference before segmentation")
fix = functools.partial(re.compile("[\\s.!?…]+$").sub, "")  # FIX, as B-N2's S2 (same pinned sentence)
V1 = "import json, sys; from rescap.chair import objects_in; json.dump([objects_in(t) for t in json.load(sys.stdin)], sys.stdout)"
VARIANTS = (("as_written", None), ("fix", fix))
R14 = ("R14 (CC-039): no caption of this run names an object under the pinned matcher (rescap.chair.chair as "
       "scripts/evaluate.py calls it: chair_i is None, so evaluate.py:421 raises); excluded before scripts/evaluate.py "
       "is called")
SEEN: dict[str, str] = {}  # every input read, with its sha256


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
    dc, pr = P["design_constants"], {p["id"]: p for p in P["predictions"]}
    boot = re.match(r"(\d+) image-bootstrap draws per analysis set: numpy\.random\.default_rng\((\d+)\)\.multinomial\("
                    r"N, \[1/N\]\*N, size=(\d+)\) over the set's images in id order.* percentiles ([\d.]+) and ([\d.]+) "
                    r"of the replicates", dc["bootstrap"])
    km = re.search(r"a tau with fewer than (\d+) models is NOT_EVALUABLE", next(k for k in P["kill_rules"]
                                                                               if k["id"] == "KM")["then"])
    cfg = {"seed": int(boot[2]), "n_boot": dc["n_boot"]["value"], "ci": dc["ci_percentiles"], "min_models": int(km[1]),
           "rules": {k: re.search(r"` .*?\b(tau_lt|tau_ge|sign_gt_0)\b", pr[k]["rule"])[1] for k in STATS},
           "tau0": {k: pr[k].get("tau0") for k in STATS}, "mode": "short"}
    if not (int(boot[1]) == int(boot[3]) == cfg["n_boot"] and [float(boot[4]), float(boot[5])] == cfg["ci"]
            and all(re.match(r"`([^`]+)`", pr[k]["rule"])[1] == s for k, s in STATS.items())
            and all(f"(tau0 {pr[k]['tau0']:g}:" in pr[k]["rule"] for k in ("LBB-P1", "LBB-P2"))
            and cfg["rules"] == {"LBB-P1": "tau_lt", "LBB-P2": "tau_ge", "LBB-P3": "sign_gt_0"}
            and all("(short prompt)" in pr[k]["claim"] for k in ("LBB-P1", "LBB-P2"))
            and P["scoring"]["fix"].startswith(FIX) and "on the clean 157" in P["scoring"]["sets_for_verdicts"]):
        raise SystemExit("REFUSED: a registered constant does not read as this scorer implements it")
    return cfg


def modules(F: dict) -> None:
    """The instruments at their prereg pins; then every repo module they load must be committed unmodified at HEAD
    (scripts/evaluate.py and the v1 child process load the same files)."""
    for rel in ("scripts/evaluate.py", "rescap/chair.py", "scripts/object_prf.py", "rescap/vlm/mock.py",
                "scripts/clean_supervision.py"):
        pinned(rel, F[rel])
    for m in ("clean_supervision", "object_prf", "rescap.chair", "rescap.metrics", "rescap.vlm.mock"):
        importlib.import_module(m)
    for f in sorted({Path(getattr(x, "__file__", None) or "/").resolve() for x in list(sys.modules.values())} - {HERE}):
        if f.is_relative_to(ROOT):
            pinned(f.relative_to(ROOT).as_posix())


def refs_of(data: bytes) -> dict:
    """{image id: [captions]} of a test_data.json, as scripts/evaluate.py's references() reads it."""
    refs: dict[str, list[str]] = {}
    for a in json.loads(data).get("annotations", []):
        if a.get("caption"):
            refs.setdefault(str(a["image_id"]), []).append(a["caption"])
    return refs


def sets(P: dict, data: Path) -> dict:
    """Per set, sha-checked: ids (manifest order, which is id order), image shas, the NCS_DATASET name and references
    as scripts/evaluate.py reads them; KTVIC adds its leaked/clean id lists."""
    F, out = {r["path"]: r["sha256"] for r in P["frozen_files"]}, {}
    for ds, spec in P["datasets"].items():
        name = spec["image_dir"].split("/")[0]
        rows = [r.split("\t") for r in pinned(spec["manifest"]["path"], spec["manifest"]["sha256"]).decode().splitlines()]
        S = {"name": name, "ids": [r[0] for r in rows], "sha": {r[0]: r[2] for r in rows}, "refs": refs_of(pinned(
            data / "datasets" / name / "test_data.json", F[f"data/datasets/{name}/test_data.json"], head=False))}
        parts = {k: pinned(v["path"], v["sha256"]).decode().split() for k, v in spec.get("split", {}).items()
                 if k in ("leaked", "clean")}
        if not (name in ("ktvic", "uitviic") and S["ids"] == sorted(S["refs"], key=int) == sorted(S["ids"], key=int)
                and len(S["ids"]) == spec["n_images"] and all(len(p) == spec["split"][k]["n"] for k, p in parts.items())
                and sorted(sum(parts.values(), []), key=int) == (S["ids"] if parts else [])):
            raise SystemExit(f"REFUSED: {ds}: the manifest, its references or the leaked/clean lists fail their checks")
        out[ds] = S | ({"parts": parts} if parts else {})
    return out


def reference_rows(P: dict) -> dict:
    """The prereg's reference rows (existing outputs of our fine-tuned systems; no tau, no verdict), sha-checked."""
    out = {}
    for f in P["reference_rows"]["files"]:
        m = re.fullmatch(r"data/results/(uitviic/uitviic_)?(\w+)-(short|detailed)\.preds\.json", f["path"])
        ds, raw = "uitviic_test" if m[1] else "ktvic_test", json.loads(pinned(f["path"], f["sha256"]))
        out[f"ref_{m[2]}_{ds}-{m[3]}"] = {"set": ds, "mode": m[3], "path": f["path"], "caps": {
            str(k): v[0] if isinstance(v, list) else v for k, v in raw.items()}}  # as scripts/evaluate.py:316
    return out


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


def load_runs(P: dict, odir: Path, S: dict) -> tuple[dict, dict]:
    """Admitted ZS systems (with their per-run facts) by run id, and every exclusion with its reasons, in prereg order;
    an admitted run none of whose captions names an object is excluded before scripts/evaluate.py is called (R14). The
    fix strips only trailing [\\s.!?…], which no matcher token holds, so the fixed captions name the same objects."""
    from rescap.chair import chair
    zs, excluded = {}, {}
    for run in P["runs"]:
        o, why = admit(P, run, odir, S[run["dataset"]])
        if not why and chair(o["predictions"], S[run["dataset"]]["refs"], strict_ids=False).chair_i is None:
            why = [R14]
        if why:
            excluded[run["run_id"]] = why
            continue
        zs[run["run_id"]] = {"set": run["dataset"], "mode": run["prompt_mode"], "caps": o["predictions"], "facts": {
            k: o[k] for k in ("machine_id", "git_head", "git_dirty", "parity_slice0")} | {
            "hit_max_share": float(np.mean(list(o["hit_max"].values())))}}
    return zs, excluded


def evaluate(caps: dict, name: str, mode: str, ds: str, data: Path, fixed: bool) -> dict:
    """results[0] of scripts/evaluate.py, unchanged, in a fresh process on {id: caption}; for the fix, on the fixed
    captions and a copy of the set's test_data.json with every reference fixed (a temporary NCS_DATA)."""
    with tempfile.TemporaryDirectory() as tmp:
        t, root = Path(tmp), data
        if fixed:
            d = json.loads((data / "datasets" / ds / "test_data.json").read_text(encoding="utf-8"))
            for a in d["annotations"]:
                a["caption"] = fix(a["caption"]) if a.get("caption") else a.get("caption")
            (t / "datasets" / ds).mkdir(parents=True)
            (t / "datasets" / ds / "test_data.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
            root = t
        p = t / f"{name.rsplit('-', 1)[0]}-{mode}.preds.json"
        p.write_text(json.dumps({i: fix(c) if fixed else c for i, c in caps.items()}, ensure_ascii=False), encoding="utf-8")
        r = subprocess.run([sys.executable, str(ROOT / "scripts/evaluate.py"), "--predictions", str(p), "--prompt", mode,
                            "--name", name, "--out", str(t / "scored.json")], capture_output=True, encoding="utf-8",
                           errors="replace", env=os.environ | {"NCS_DATA": str(root), "NCS_DATASET": ds})
        if r.returncode:
            raise SystemExit(f"REFUSED: scripts/evaluate.py failed on {name}:\n{r.stdout[-1500:]}\n{r.stderr[-1500:]}")
        return json.loads((t / "scored.json").read_text(encoding="utf-8"))["results"][0]


def per_image(refs: dict, caps: dict, edit=None) -> dict:
    """{id: c(i)}: one Cider().compute_score over every id of `refs` (IDF from all of them) on CaptionMetrics._align and
    _tokenize, as rescap.metrics scores CIDEr-D; ids in evaluate.py's order, so the mean is its CIDEr bit for bit."""
    from pycocoevalcap.cider.cider import Cider
    from rescap.metrics import CaptionMetrics
    edit, ids, cm = edit or (lambda text: text), sorted(refs), CaptionMetrics(language="vi", segmenter="rdrsegmenter",
                                                                             tokenize=True)
    gt, res = cm._tokenize(*cm._align({i: [edit(x) for x in refs[i]] for i in ids}, {i: [edit(caps[i])] for i in ids}))
    if cm.segmenter != "rdrsegmenter":
        raise SystemExit(f"REFUSED: the segmenter fell back ({cm.segmenter})")
    return dict(zip(gt, map(float, Cider().compute_score(gt, res)[1])))


def score_all(systems: dict, S: dict, data: Path) -> dict:
    """Both variants of every system: scripts/evaluate.py's row (fresh processes, 4 at a time) and the per-image vector
    in id order; refused unless every segmenter is RDRSegmenter and F0 holds (per-image mean = evaluate.py's CIDEr)."""
    jobs = [(n, k) for n in systems for k, _ in VARIANTS]
    with ThreadPoolExecutor(4) as ex:
        rows = dict(zip(jobs, ex.map(lambda j: evaluate(systems[j[0]]["caps"], j[0], systems[j[0]]["mode"], S[systems[
            j[0]]["set"]]["name"], data, j[1] == "fix"), jobs)))
    out = {}
    for n, s in systems.items():
        out[n] = {}
        for k, edit in VARIANTS:
            vec, x = per_image(S[s["set"]]["refs"], s["caps"], edit), rows[(n, k)]["scores_scaled_x100"]
            if rows[(n, k)]["segmenter"] != "rdrsegmenter" or 100 * float(np.mean(list(vec.values()))) != x["CIDEr"]:
                raise SystemExit(f"REFUSED (F0): {n} {k}: segmenter {rows[(n, k)]['segmenter']}, or the per-image mean "
                                 f"differs from scripts/evaluate.py's CIDEr {x['CIDEr']}")
            out[n][k] = {"CIDEr": x["CIDEr"], "BLEU-4": x["BLEU-4"], "ROUGE-L": x["ROUGE-L"],
                         "vec": np.array([vec[i] for i in S[s["set"]]["ids"]])}
    return out


def objects(texts: list[str]) -> dict:
    """rescap.chair.objects_in per text: v2 = the tone-normalised default, here; v1 = RESCAP_RAW_TONE=1 set before the
    import (the import builds tone-dependent tables), in a child process."""
    from rescap.chair import objects_in
    r = subprocess.run([sys.executable, "-c", V1], input=json.dumps(texts), capture_output=True, text=True, check=True,
                       cwd=ROOT, env=os.environ | {"RESCAP_RAW_TONE": "1", "PYTHONPATH": str(ROOT)})
    return {"v1": [set(x) for x in json.loads(r.stdout)], "v2": [set(objects_in(t)) for t in texts]}


def obj_rows(S: dict, systems: dict) -> dict:
    """object_prf.image_counts rows per system and matcher, in id order (object_prf's KTVIC convention: unique classes,
    gold = the union over an image's references, exact matches)."""
    import object_prf as op
    from rescap.chair import _ancestors
    gold = {}
    for ds, s in S.items():
        it = {k: iter(v) for k, v in objects([r for i in s["ids"] for r in s["refs"][i]]).items()}
        gold[ds] = {k: [set().union(*(next(it[k]) for _ in s["refs"][i])) for i in s["ids"]] for k in it}
    out = {}
    for n, s in systems.items():
        o, gd = objects([s["caps"][i] for i in S[s["set"]]["ids"]]), gold[s["set"]]
        out[n] = {k: [op.image_counts(m, gk, _ancestors) for m, gk in zip(o[k], gd[k])] for k in o}
    return out


def guard_fails(c: str) -> bool:
    """scoring.language_guard: the caption fails rescap.vlm.mock.looks_vietnamese or matches clean_supervision.CJK_RE."""
    from clean_supervision import CJK_RE
    from rescap.vlm.mock import looks_vietnamese
    return not looks_vietnamese(c) or bool(CJK_RE.search(c))


def tau_b(x, y):
    """Kendall tau-b over axis 0 (systems), per column: (concordant - discordant) / sqrt(pairs untied in x * pairs
    untied in y); nan when a vector is all ties or holds a nan."""
    i, j = np.triu_indices(len(x), 1)
    dx, dy = np.sign(x[i] - x[j]), np.sign(y[i] - y[j])
    with np.errstate(invalid="ignore", divide="ignore"):
        return (dx * dy).sum(0) / np.sqrt((dx != 0).sum(0) * (dy != 0).sum(0))


def draws(n: int, cfg: dict) -> np.ndarray:
    """The registered image-bootstrap weights (B x n) of an analysis set of n images in id order."""
    return np.random.default_rng(cfg["seed"]).multinomial(n, [1 / n] * n, size=cfg["n_boot"]).astype(float) if n \
        else np.zeros((cfg["n_boot"], 0))


def ci(rep: np.ndarray, q: list) -> list | None:
    return [float(np.percentile(rep, q[0])), float(np.percentile(rep, q[1]))] if np.all(np.isfinite(rep)) else None


def rule(name: str, point: float, c: list | None, tau0: float | None = None) -> str:
    """tau_lt, tau_ge and sign_gt_0 of the prereg's verdict_rules; NOT_EVALUABLE when the point or the CI is undefined."""
    if c is None or not np.isfinite(point):
        return "NOT_EVALUABLE"
    if name == "tau_lt":
        return "PASS" if c[1] < tau0 else "FAIL" if point >= tau0 else "INCONCLUSIVE"
    if name == "tau_ge":
        return "PASS" if c[0] >= tau0 else "FAIL" if point < tau0 else "INCONCLUSIVE"
    return "PASS" if c[0] > 0 else "FAIL" if point <= 0 else "INCONCLUSIVE"  # sign_gt_0


def cider_table(R: dict, rid: dict, keep: dict, sel: dict, cfg: dict) -> dict:
    """C[(set, variant)][model] = (point, replicates) of the short ZS runs over the images sel[set] (positions in id
    order) on that set's draws; on a full set the point is scripts/evaluate.py's CIDEr."""
    C = {}
    for ds, pos in sel.items():
        W = draws(len(pos), cfg)
        for k, _ in VARIANTS:
            C[(ds, k)] = {}
            for m in keep[ds]:
                r = R[rid[(m, ds, cfg["mode"])]][k]
                v = r["vec"][pos]
                with np.errstate(invalid="ignore", divide="ignore"):
                    C[(ds, k)][m] = (r["CIDEr"] if len(pos) == len(r["vec"]) else 100 * float(np.mean(v)),
                                     100 * (W @ v) / len(v))
    return C


def taus(C: dict, keep: dict, cfg: dict, verdicts: bool) -> dict:
    """LBB-P1 (KTVIC, as written vs fix), LBB-P2 (fix, KTVIC vs UIT-ViIC) and LBB-P3 (LBB-P2 minus its as-written twin)
    over the models KM keeps on the set(s) of each; every replicate recomputes both rankings on the shared draws."""
    K, U = "ktvic_test", "uitviic_test"
    both = [m for m in keep[K] if m in keep[U]]

    def tau(a, b, ms):
        if len(ms) < 2:
            return float("nan"), np.full(cfg["n_boot"], np.nan)
        (x, X), (y, Y) = ((np.array([C[k][m][0] for m in ms]), np.stack([C[k][m][1] for m in ms])) for k in (a, b))
        return float(tau_b(x, y)), tau_b(X, Y)

    p2, tw = tau((K, "fix"), (U, "fix"), both), tau((K, "as_written"), (U, "as_written"), both)
    out = {}
    for k, (pt, rep), ms in (("LBB-P1", tau((K, "as_written"), (K, "fix"), keep[K]), keep[K]), ("LBB-P2", p2, both),
                             ("LBB-P3", (p2[0] - tw[0], p2[1] - tw[1]), both)):
        out[k] = {"statistic": STATS[k], "point": pt, "ci95": ci(rep, cfg["ci"]), "models": ms}
        if verdicts:
            out[k]["verdict"] = "NOT_EVALUABLE" if len(ms) < cfg["min_models"] else rule(
                cfg["rules"][k], pt, out[k]["ci95"], cfg["tau0"][k])
    return out


def gaps(R: dict, rows: dict, systems: dict, S: dict, cfg: dict) -> dict:
    """LBB-D1, no verdict: leaked minus clean per KTVIC system (ZS runs and reference rows): CIDEr-D in both variants
    (per image, IDF from all 558) and object F1 v1/v2; each part on its own registered draws."""
    import object_prf as op
    pos = {i: k for k, i in enumerate(S["ktvic_test"]["ids"])}
    parts = [np.array(sorted(pos[i] for i in S["ktvic_test"]["parts"][p])) for p in ("leaked", "clean")]
    W = [draws(len(p), cfg) for p in parts]

    def gap(stat) -> dict:
        (a, A), (b, B) = (stat(p, w) for p, w in zip(parts, W))
        return {"leaked": a, "clean": b, "gap": a - b, "ci95": ci(A - B, cfg["ci"])}

    def cider(v):
        return lambda p, w: (100 * float(v[p].mean()), 100 * (w @ v[p]) / len(p))

    def f1(rs):
        return lambda p, w: (op.scores([rs[j] for j in p])["F1"],
                             np.array([op.scores([rs[j] for j in np.repeat(p, c.astype(int))])["F1"] for c in w]))

    return {n: {f"CIDEr_{k}": gap(cider(R[n][k]["vec"])) for k, _ in VARIANTS} | {
        f"object_F1_{k}": gap(f1(rows[n][k])) for k in ("v1", "v2")} for n, s in systems.items() if s["set"] == "ktvic_test"}


def board(R: dict, rows: dict, systems: dict, S: dict) -> dict:
    """LBB-D2, no verdict: the leaderboard, ZS runs and reference rows alike, both prompts."""
    import object_prf as op
    out = {}
    for n, s in systems.items():
        caps = [s["caps"][i] for i in S[s["set"]]["ids"]]
        out[n] = {"CIDEr_as_written": R[n]["as_written"]["CIDEr"], "CIDEr_fix": R[n]["fix"]["CIDEr"],
                  "BLEU-4": R[n]["as_written"]["BLEU-4"], "ROUGE-L": R[n]["as_written"]["ROUGE-L"],
                  "objects_P_R_F1": {k: {m: op.scores(rows[n][k])[m] for m in ("P", "R", "F1")} for k in ("v1", "v2")},
                  "end_punctuation_rate": float(np.mean([fix(c) != c.rstrip() for c in caps])),
                  "length_mean_syllables": float(np.mean([len(c.split()) for c in caps])),
                  "language_guard_fail_share": float(np.mean([guard_fails(c) for c in caps]))} | s.get("facts", {})
    return out


def analyse(P: dict, cfg: dict, S: dict, systems: dict, R: dict, rows: dict) -> dict:
    """KM, the registered predictions on the full sets with verdicts; LBB-S1 (clean 157) and the language-guard clean
    intersection as sensitivity analyses without verdicts; LBB-D1 and LBB-D2; the kill rules."""
    rid, modes = {(r["model"], r["dataset"], r["prompt_mode"]): r["run_id"] for r in P["runs"]}, P["decode"]["max_new_tokens"]
    keep = {ds: [m for m in P["models"] if all(rid[(m, ds, md)] in systems for md in modes)] for ds in S}
    full, pos = {ds: np.arange(len(S[ds]["ids"])) for ds in S}, {i: k for k, i in enumerate(S["ktvic_test"]["ids"])}
    clean = full | {"ktvic_test": np.array(sorted(pos[i] for i in S["ktvic_test"]["parts"]["clean"]))}
    guard = {ds: np.array([k for k, i in enumerate(S[ds]["ids"]) if not any(guard_fails(systems[rid[(m, ds, md)]][
        "caps"][i]) for m in keep[ds] for md in modes)], int) for ds in S}

    def sens(sel: dict) -> dict:
        t = taus(cider_table(R, rid, keep, sel, cfg), keep, cfg, False)
        return {"n_images": {ds: len(p) for ds, p in sel.items()}, "LBB-P1": t["LBB-P1"], "LBB-P2": t["LBB-P2"]}

    pred = taus(cider_table(R, rid, keep, full, cfg), keep, cfg, True)
    return {"KM_models_kept": keep, "predictions": pred, "LBB-S1_clean157": sens(clean),
            "language_guard_clean_intersection": sens(guard), "LBB-D1": gaps(R, rows, systems, S, cfg),
            "LBB-D2": board(R, rows, systems, S),
            "kill_rules": {"KB1": {"fires": pred["LBB-P1"].get("verdict") == "FAIL"},
                           "KB2": {"fires": pred["LBB-P2"].get("verdict") == "FAIL"},
                           "KM": {ds: [m for m in P["models"] if m not in keep[ds]] for ds in S}}}


def gate(P: dict, cfg: dict, data: Path) -> tuple[dict, tuple]:
    """Provenance of every input, then the self-check: every reference row through this scorer's path, its as-written
    CIDEr equal to its committed full-set value (float equality); F0 and RDRSegmenter in both variants (else refused).
    Reads no decode output."""
    pinned(P["decoder"]["path"], P["decoder"]["sha256"])
    pinned(*JOB)
    if subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", REGISTERED, "HEAD"]).returncode:
        raise SystemExit(f"REFUSED: HEAD does not contain the registration commit {REGISTERED[:7]}")
    S, refs = sets(P, data), reference_rows(P)
    R, checks = score_all(refs, S, data), {}
    for n, s in refs.items():
        res = json.loads(pinned(s["path"].removesuffix(".preds.json") + ".json"))
        want = next(r for r in res["results"] if r["segmenter"] == "rdrsegmenter")["scores_scaled_x100"]["CIDEr"]
        checks[n] = {"committed_CIDEr_x100": want, "reproduced_CIDEr_x100": R[n]["as_written"]["CIDEr"],
                     "ok": want == R[n]["as_written"]["CIDEr"] and res["n_images"] == len(S[s["set"]]["ids"])}
    return {"sets": {ds: {"n_images": len(x["ids"])} | {k: len(v) for k, v in x.get("parts", {}).items()}
                     for ds, x in S.items()},
            "self_check": {"rows": checks, "F0_and_segmenter_both_variants": True},
            "all_pass": all(c["ok"] for c in checks.values()), "decode_outputs_read": False}, (S, refs, R)


def run(P: dict, cfg: dict, a, data: Path) -> dict:
    """The registered analysis, only from this scorer committed at HEAD with its committed all-PASS gate output."""
    pinned(HERE.relative_to(ROOT).as_posix())
    rel = Path(a.gate).resolve().relative_to(ROOT).as_posix()
    G = json.loads(pinned(rel))
    if [G["mode"], G["all_pass"], G["script_sha256"], G["prereg"]["sha256"]] != ["gate", True, sha(HERE.read_bytes()),
                                                                                  PREREG[1]]:
        raise SystemExit("REFUSED: the gate file is not a committed all-PASS gate of this scorer")
    body, (S, refs, R) = gate(P, cfg, data)
    if not body["all_pass"] or body["sets"] != G["sets"]:
        raise SystemExit("REFUSED: the self-check failed, or the sets differ from the gate's")
    zs, excluded = load_runs(P, Path(a.outputs), S)
    R |= score_all(zs, S, data)
    out = analyse(P, cfg, S, zs | refs, R, obj_rows(S, zs | refs))
    out["kill_rules"]["KD_CC-033b_and_R14_exclusions"] = excluded
    return {"gate": {"path": rel, "sha256": SEEN[rel]}, "self_check": body["self_check"], "excluded_runs": excluded} | out


def selftest(cfg: dict) -> bool:
    """Toy cases with known answers; reads no data file."""
    t0 = cfg["tau0"]
    assert abs(tau_b(np.array([1, 2, 3, 4]), np.array([1, 2, 4, 3])) - 4 / 6) < 1e-12  # 5 concordant, 1 discordant
    assert abs(tau_b(np.array([1, 2, 2, 3]), np.array([1, 2, 3, 3])) - 0.8) < 1e-12  # one tie in each
    assert np.isnan(tau_b(np.ones(4), np.arange(4.0)))
    assert np.allclose(tau_b(np.array([[1, 1], [2, 2], [3, 4], [4, 3]]), np.array([[1, 1], [2, 2], [3, 3], [4, 4]])),
                       [1, 4 / 6])
    assert [rule("tau_lt", p, c, t0["LBB-P1"]) for p, c in ((2 / 3, [1 / 3, 2 / 3]), (1.0, [2 / 3, 1.0]),
                                                            (2 / 3, [1 / 3, 1.0]))] == ["PASS", "FAIL", "INCONCLUSIVE"]
    assert [rule("tau_ge", p, c, t0["LBB-P2"]) for p, c in ((1.0, [2 / 3, 1.0]), (1 / 3, [0.0, 1.0]),
                                                            (2 / 3, [1 / 3, 1.0]))] == ["PASS", "FAIL", "INCONCLUSIVE"]
    assert [rule("sign_gt_0", p, c) for p, c in ((0.3, [0.1, 0.5]), (0.0, [-0.2, 0.2]), (0.1, [-0.1, 0.3]),
                                                 (np.nan, None))] == ["PASS", "FAIL", "INCONCLUSIVE", "NOT_EVALUABLE"]
    assert [fix(t) for t in ("một con chó .", "a?! …\n", "a. b", "...")] == ["một con chó", "a", "a. b", ""]
    assert (draws(5, cfg).sum(1) == 5).all() and draws(0, cfg).shape == (cfg["n_boot"], 0)
    try:
        pinned(PREREG[0], "0" * 64)
    except SystemExit as refused:
        assert "PROVENANCE FAIL" in str(refused)
        return True
    raise AssertionError("a wrong pin was accepted")


def dryrun(P: dict, cfg: dict) -> dict:
    """SYNTHETIC: made-up Vietnamese references, splits and captions under a temporary NCS_DATA; 16 decode files with
    the registered provenance and a made-up reference system go through admission, both scorer variants, F0, KM and
    every statistic. Built in: model 0 copies a reference ending ' . . .' and model 1 drops its last word, so the fix
    reorders them on KTVIC (LBB-P1 point < 1); model 3 copies a reference on leaked ids only (LBB-D1 gap > 0); one CJK
    caption (KTVIC guard intersection 29 of 30); a copy with a wrong job sha is excluded, and KM below 4 models. Model
    3's UIT-ViIC detailed run names no object: R14 excludes it before scripts/evaluate.py is called, so KM keeps 3
    models on UIT-ViIC and LBB-P2 and LBB-P3 are NOT_EVALUABLE."""
    objs = ["người đàn ông", "con chó", "con mèo", "chiếc xe máy", "cái bàn", "cái ghế", "cái cây", "chiếc ô tô"]
    where, verbs = ["trên đường phố", "trong căn phòng", "ở công viên", "bên bờ sông"], ["đang đứng", "đang ngồi", "đang đi"]
    head = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    models, S = list(P["models"]), {}
    with tempfile.TemporaryDirectory() as tmp:
        data, odir, bad = Path(tmp) / "ncs", Path(tmp) / "out", Path(tmp) / "bad"
        for d in (odir, bad):
            d.mkdir()
        for ds, name, n, end, first in (("ktvic_test", "ktvic", 30, "", 1), ("uitviic_test", "uitviic", 20, " .", 2)):
            ids = [str(3 * k + first) for k in range(n)]
            raw = json.dumps({"images": [{"id": int(i), "file_name": f"{i}.jpg"} for i in ids], "annotations": [
                {"id": 5 * k + j, "image_id": int(i), "caption": f"{objs[k % 8]} {verbs[j % 3]} {where[(k + j) % 4]} "
                                                                 f"cạnh {objs[(k + j + 1) % 8]}{end}"}
                for k, i in enumerate(ids) for j in range(5)]}, ensure_ascii=False).encode()
            (data / "datasets" / name).mkdir(parents=True)
            (data / "datasets" / name / "test_data.json").write_bytes(raw)
            S[ds] = {"name": name, "ids": ids, "sha": {i: sha(i.encode()) for i in ids}, "refs": refs_of(raw)}
        K = S["ktvic_test"]["ids"]
        S["ktvic_test"]["parts"] = {"leaked": K[:20], "clean": K[20:]}
        for run in P["runs"]:
            k, rs = models.index(run["model"]), S[run["dataset"]]["refs"]
            caps = {i: [rs[i][0] + " . . .", rs[i][0].rsplit(" ", 1)[0], rs[i][1].rsplit(" ", 2)[0],
                        rs[i][0] if i in K[:20] else "một con chó"][k] for i in rs}  # evaluate.py:421 needs >= 1 object
            caps = caps if run["prompt_mode"] == "short" else {i: f"{c} và {rs[i][2]}" for i, c in caps.items()}
            if k == 2 and run["dataset"] == "ktvic_test" and run["prompt_mode"] == "detailed":
                caps[K[5]] = "一只狗"  # fails the language guard
            if k == 3 and run["dataset"] == "uitviic_test" and run["prompt_mode"] == "detailed":
                caps = {i: "một bức ảnh rất đẹp" for i in caps}  # names no object: excluded by R14
            o = registered(P, run, S[run["dataset"]]) | {"git_head": head, "git_dirty": False, "machine_id": "synthetic",
                                                         "parity_slice0": {"n": 2, "identical": 1}, "predictions": caps,
                                                         "hit_max": {i: False for i in caps}}
            for d, extra in ((odir, {}), (bad, {"job_sha256": "0" * 64})):
                f = d / f"{run['run_id']}.preds.json"
                f.write_text(json.dumps(o | extra, ensure_ascii=False, indent=1), encoding="utf-8")
                Path(f"{f}.sha256").write_text(f"{sha(f.read_bytes())}  {f.name}\n", encoding="utf-8")
        zs, excluded = load_runs(P, odir, S)
        bad_excluded = load_runs(P, bad, S)[1]
        refs = {f"ref_syn_{ds}-{md}": {"set": ds, "mode": md, "caps": {i: r[3] for i, r in S[ds]["refs"].items()}}
                for ds in S for md in ("short", "detailed")}
        calls, real = [], globals()["evaluate"]  # every scripts/evaluate.py call, by system name
        globals()["evaluate"] = lambda caps, name, *rest: calls.append(name) or real(caps, name, *rest)
        try:
            R = score_all(zs | refs, S, data)
        finally:
            globals()["evaluate"] = real
        out = analyse(P, cfg, S, zs | refs, R, obj_rows(S, zs | refs))
    rid = {(r["model"], r["dataset"], r["prompt_mode"]): r["run_id"] for r in P["runs"]}
    pr, (r0, r1) = out["predictions"], (R[rid[(models[k], "ktvic_test", "short")]] for k in (0, 1))
    zero = rid[(models[3], "uitviic_test", "detailed")]
    assert excluded == {zero: [R14]} and len(bad_excluded) == 16 and all(v == ["job_sha256 differs from the "
                                                                              "registration"] for v in bad_excluded.values())
    assert zero not in calls and sorted(calls) == sorted(n for n in zs | refs for _ in VARIANTS)  # never on the R14 run
    assert out["KM_models_kept"] == {"ktvic_test": models, "uitviic_test": models[:3]} and pr["LBB-P1"]["models"] == models
    assert pr["LBB-P2"]["verdict"] == pr["LBB-P3"]["verdict"] == "NOT_EVALUABLE" and pr["LBB-P2"]["models"] == models[:3]
    assert pr["LBB-P1"]["point"] < 1 and pr["LBB-P1"]["verdict"] != "FAIL" and all(p["ci95"] for p in pr.values())
    assert r1["fix"]["CIDEr"] == r1["as_written"]["CIDEr"] < r0["fix"]["CIDEr"] and r0["as_written"]["CIDEr"] < r0["fix"]["CIDEr"]
    assert out["LBB-D1"][rid[(models[3], "ktvic_test", "short")]]["CIDEr_as_written"]["gap"] > 0 and len(out["LBB-D1"]) == 10
    assert out["language_guard_clean_intersection"]["n_images"] == {"ktvic_test": 29, "uitviic_test": 20}
    assert out["LBB-S1_clean157"]["n_images"]["ktvic_test"] == 10 and "verdict" not in json.dumps(out["LBB-S1_clean157"])
    assert "ref_syn" not in json.dumps(pr) and set(out["LBB-D2"]) == set(zs) | set(refs)
    km = taus(cider_table(R, rid, {"ktvic_test": models[:3], "uitviic_test": models}, {d: np.arange(len(S[d]["ids"]))
                                                                                      for d in S}, cfg),
              {"ktvic_test": models[:3], "uitviic_test": models}, cfg, True)
    assert all(v["verdict"] == "NOT_EVALUABLE" for v in km.values())  # 3 models: KM leaves every tau NOT_EVALUABLE
    return {"SYNTHETIC": "made-up references, splits and captions; no reference, split, manifest or decode file is read",
            "excluded_runs": excluded, "evaluate_py_called_on": sorted(set(calls)),
            "excluded_runs_of_the_wrong_job_copies": bad_excluded, "KM_check_3_models": km} | out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=("gate", "dryrun", "run"))
    ap.add_argument("out")
    ap.add_argument("--gate", help="run: the committed output of gate")
    ap.add_argument("--outputs", help="run: the folder of the 16 decode outputs and their .sha256 sidecars")
    a = ap.parse_args()
    if Path(a.out).exists() or not (os.environ.get("NCS_DATA") and os.environ.get("VNCORENLP_DIR")) or \
            "RESCAP_RAW_TONE" in os.environ or (a.mode == "run" and not (a.gate and a.outputs)):
        raise SystemExit("REFUSED: OUT exists (never overwritten), NCS_DATA or VNCORENLP_DIR is unset, RESCAP_RAW_TONE "
                         "is set, or run lacks --gate/--outputs")
    P = json.loads(pinned(*PREREG))
    cfg = config(P)
    modules({r["path"]: r["sha256"] for r in P["frozen_files"]})
    vnc, data = Path(os.environ["VNCORENLP_DIR"]), Path(os.environ["NCS_DATA"])
    env = {"python": sys.version.split()[0]} | {p: version(p) for p in ("numpy", "pycocoevalcap", "py_vncorenlp",
                                                                         "pyjnius")}
    env |= {f.name: sha(f.read_bytes()) for f in (vnc / "VnCoreNLP-1.2.jar", vnc / "models/wordsegmenter/wordsegmenter.rdr")}
    head = {"id": P["prereg_id"], "mode": a.mode, "prereg": dict(zip(("path", "sha256"), PREREG)),
            "script_sha256": sha(HERE.read_bytes()), "config": cfg, "env": env, "toy_selftest_pass": selftest(cfg)}
    body = gate(P, cfg, data)[0] if a.mode == "gate" else dryrun(P, cfg) if a.mode == "dryrun" else run(P, cfg, a, data)
    with open(a.out, "x", encoding="utf-8") as f:  # "x": an existing output is never overwritten
        json.dump(head | body | {"inputs_sha256": SEEN}, f, ensure_ascii=False, indent=1, default=lambda o: o.item())
    print(json.dumps({"mode": a.mode, "all_pass": body.get("all_pass"), "excluded": list(body.get("excluded_runs", {})),
                      "verdicts": {k: v.get("verdict") for k, v in body.get("predictions", {}).items()}}))
    return 0 if body.get("all_pass", True) else 1


if __name__ == "__main__":
    sys.exit(main())
