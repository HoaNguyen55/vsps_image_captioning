#!/usr/bin/env python
"""Tier-3 S5 (T3.4): data-scaling probe of the P1_dev recipe at 25% and 50% of the training images. Diagnostic only
(PD-9 Q1): no selection, no claim, no gate on any other job.

    python scripts/scaling_probe.py --selftest          # CPU: synthetic data, the registered subsets, the n2 metrics
    python scripts/scaling_probe.py --check [--machine] [--instrument]
    python scripts/scaling_probe.py --subsets DIR [--instrument]     # the ids files and DIR/registered.sha256
    python scripts/scaling_probe.py --analyse DIR       # DIR/scaling.json, or its next _vN (never overwritten)

Registered in manuscript/prereg/2026-10-18_tier3_S5.{md,json} (commit a68fb66). Every mode first checks both prereg
files' sha256, asserts each constant below against the JSON, and checks the sha256 of every code_at_head file and of
each registered input this job reads; --machine adds the p1dev_s42 adapter and the base snapshot in the HF cache,
--instrument the addendum's pins of this file and of the job file. A mismatch exits non-zero before any output.

Subsets: prefixes of train_rl.schedule(ids of train minus dev300, 3469, 42), sizes floor(3469 x pct / 100): nested.
Analysis on dev300 of p1dev_s42_f25, _f50 and p1dev_s42_redecode (the 100% point, decoded on the job's machine):
CIDEr-D x100 (mean of rl_report.dev_scores per-image values), object F1 vs the five KTVIC references (object_prf.scores,
exact classes) and CHAIR_i (rescap.chair); OLS y = a + b log2(N) over the three points; 95% paired percentile bootstrap
over dev images (B = 2000, numpy default_rng(0): rl_reward.boot's draw, shared by the three models; corpus metrics
recomputed, slope refitted). It covers dev-image sampling only, one training seed per size.
Decision: FUND_EXTERNAL_IMAGE_DATA if CI_lo(b) > +1; CLOSE_DATA_VOLUME_LEVERS if b < +1; INCONCLUSIVE otherwise.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]

import checkpoint_resume_hook as hook  # noqa: E402
import rl_report  # noqa: E402
from evaluate import DATA, KTVIC, references  # noqa: E402
from object_prf import image_counts, scores  # noqa: E402
from rescap.chair import chair, objects_in  # noqa: E402
from rl_reward import boot  # noqa: E402
from train_rl import read_ids, schedule  # noqa: E402
from train_stage2 import MODEL_ID  # noqa: E402

PREREG = ROOT / "manuscript/prereg/2026-10-18_tier3_S5.json"
PREREG_SHA256 = {PREREG: "39a8433b5d16774309f499d34627e3b186f7feb6acf6f825dec72f37c70e3cbe",
                 PREREG.with_suffix(".md"): "a5f7f6adf72ab484a0dc212b61d66459e53dd7f054fecf05c549a99cf0f2eea8"}
INSTRUMENT = ROOT / "manuscript/prereg/2026-10-18_tier3_S5_instrument.json"
JOB, JOB_FILE = "t3_4_s5_data_scaling", "scripts/queue/jobs/t3_4_s5_data_scaling.sh"
POOL, DEV = "data/splits/ktvic_train_minus_dev300.txt", "data/splits/ktvic_dev300.txt"
N2 = "data/results/rl/p1dev_s42-dev300-short.json"
POOL_N, DEV_N, SEED = 3469, 300, 42
PCTS = {"f25": 25, "f50": 50}
RUNS = {"f25": "p1dev_s42_f25", "f50": "p1dev_s42_f50", "f100": "p1dev_s42_redecode"}
B, BOOT_SEED, LEVEL = 2000, 0, 95
FUND_IF_LO_GT, CLOSE_IF_B_LT = 1, 1
OUTCOMES = ("FUND_EXTERNAL_IMAGE_DATA", "CLOSE_DATA_VOLUME_LEVERS", "INCONCLUSIVE")
PRED = {"CIDEr_D_x100": [1, 4], "F1": [0, 2]}
METRICS = ("CIDEr_D_x100", "F1", "CHAIR_i")
#: Registered inputs this job never reads: the OpenViIC panel (not in the registered analysis; never opened).
NOT_READ = ("data/ktvic_openviic_refs.json",)
#: Fragments of the registered procedure that the job file must contain, and flags it must not use.
JOB_FLAGS = ("build_gold_sft.py --annotations", "train_stage2.py --stage sft",
             "--epochs 2 --seed 42 --loss-mask assistant", "NCS_DATASET=ktvic_dev",
             "evaluate.py --model qwen2.5-vl-7b --adapter", "--split dev_data.json --prompt short")
JOB_FORBIDDEN = ("--four-bit", "--max-new-tokens", "--max-vision-tokens", "--limit", "test_data.json")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def verify(want: dict[Path, str]) -> None:
    """Exit unless every file exists with its registered sha256."""
    found = {p: sha256(p) if p.is_file() else None for p in want}
    bad = {str(p): {"registered": s, "found": found[p]} for p, s in want.items() if found[p] != s}
    if bad:
        raise SystemExit("sha256 check failed, refusing to run:\n" + json.dumps(bad, indent=1))


def sizes() -> dict[str, int]:
    """Training images per point: floor(3469 x pct / 100) for each subset, all 3469 for the 100% point."""
    return {k: POOL_N * pct // 100 for k, pct in PCTS.items()} | {"f100": POOL_N}


def registered(P: dict) -> None:
    """Assert every constant above against the frozen JSON (prereg section 9)."""
    src, data, ana, rule, pred = P["sources"], P["data"], P["analysis"], P["decision_rule"], P["frozen_predictions"]
    n = sizes()
    got = {
        "job": (P["job"]["job_name"], JOB),
        "output names": (sorted(P["registered_before_output"]["output_names"]), sorted([*RUNS.values(), "t3_4_s5"])),
        "base": (P["models"]["base"]["id"], MODEL_ID),
        "test split read": (data["test_split_read"], False),
        "pool": (data["splits"][POOL]["n_images"], POOL_N),
        "dev": (data["splits"][DEV]["n_images"], DEV_N),
        "f100": (data["f100"]["n_images"], n["f100"]),
        "seed": (src["seed"]["value"], SEED),
        "pcts": ([src[f"fractions_pct[{j}]"]["value"] for j in range(len(PCTS))], list(PCTS.values())),
        "subset rule": (data["subset_rule"], f"prefixes of train_rl.schedule(ids of {POOL}, {POOL_N}, {SEED}) (one "
                        f"seeded permutation), sizes floor({POOL_N} x pct / 100); nested by construction"),
        "points": (ana["points"], f"x = log2(N) for N = {', '.join(map(str, n.values()))} training images"),
        "B": ([ana["ci"]["B"], src["bootstrap.B"]["value"]], [B, B]),
        "rng": ([ana["ci"]["rng"], src["bootstrap.seed"]["value"]], [f"numpy default_rng({BOOT_SEED})", BOOT_SEED]),
        "level": (ana["ci"]["level"], f"{LEVEL}%"),
        "rule": (rule["rule"], f"FUND_EXTERNAL_IMAGE_DATA if CI_lo(b) > +{FUND_IF_LO_GT}; CLOSE_DATA_VOLUME_LEVERS if "
                 f"b < +{CLOSE_IF_B_LT}; INCONCLUSIVE otherwise (no external-data spend)"),
        "thresholds": ([rule["fund_if_b_ci_lower_gt"], rule["close_if_b_lt"]], [FUND_IF_LO_GT, CLOSE_IF_B_LT]),
        "outcomes": (sorted(rule["meaning"]), sorted(OUTCOMES)),
        "predictions": ([pred["b_cider_per_doubling"], pred["F1_slope_per_doubling"]],
                        [PRED["CIDEr_D_x100"], PRED["F1"]]),
    }
    for k in PCTS:
        s = data["subsets"][k]
        got[k] = ([s["n_images"], len(s["ids"]), src[f"subset.{k}.n"]["value"], s["ids_file_name"]],
                  [n[k], n[k], n[k], f"ktvic_train_minus_dev300_{k}_s{SEED}.txt"])
    bad = {k: v for k, v in got.items() if v[0] != v[1]}
    if bad:
        raise SystemExit(f"registered constants differ from this file's, refusing to run: {bad}")


def base_snapshot(base: dict) -> dict[Path, str]:
    """The registered base revision in this machine's HF cache: refs/main must name it and HF_HUB_OFFLINE must be 1,
    so it is the revision every from_pretrained loads; returns its shards with their registered sha256."""
    from huggingface_hub import constants

    repo = Path(constants.HF_HUB_CACHE) / f"models--{base['id'].replace('/', '--')}"
    main = repo / "refs" / "main"
    if os.environ.get("HF_HUB_OFFLINE") != "1":
        raise SystemExit("HF_HUB_OFFLINE=1 is required: the base must load from the checked cache snapshot")
    if not main.is_file() or main.read_text(encoding="utf-8").strip() != base["revision"]:
        raise SystemExit(f"{main} does not name the registered base revision {base['revision']}")
    return {repo / "snapshots" / base["revision"] / f: s for f, s in base["shards_sha256"].items()}


def pinned(P: dict) -> dict[Path, str]:
    """The addendum's sha256 of this file and of the job file; the job file must carry the registered procedure."""
    pins = json.loads(INSTRUMENT.read_text(encoding="utf-8"))
    files = pins["new_files"]
    if pins["prereg_sha256"] != PREREG_SHA256[PREREG] or {"scripts/scaling_probe.py", JOB_FILE} - set(files):
        raise SystemExit(f"{INSTRUMENT} does not pin this prereg, scripts/scaling_probe.py and {JOB_FILE}")
    job, procedure = (ROOT / JOB_FILE).read_text(encoding="utf-8"), json.dumps(P["procedure"])
    missing = [f for f in JOB_FLAGS if f not in job or f not in procedure]
    forbidden = [f for f in JOB_FORBIDDEN if f in job]
    if missing or forbidden:
        raise SystemExit(f"{JOB_FILE}: registered fragments missing {missing}, unregistered flags {forbidden}")
    return {ROOT / f: s for f, s in files.items()}


def check(machine: bool = False, weights: bool = False, instrument: bool = False) -> dict:
    """The registered self-checks; returns the prereg JSON or exits. machine: the p1dev_s42 adapter files; weights:
    the base snapshot (15 GB hashed); instrument: the addendum's pins."""
    verify(PREREG_SHA256)
    P = json.loads(PREREG.read_text(encoding="utf-8"))
    registered(P)
    want = {ROOT / f: s for f, s in P["code_at_head"].items()}
    for f, s in P["inputs_sha256"].items():
        if f.startswith("data/datasets/"):
            want[DATA / f.removeprefix("data/")] = s
        elif not f.startswith(".session_backup/") and f not in NOT_READ:
            want[ROOT / f] = s
    if machine:
        f100 = P["models"]["f100"]
        run = DATA / "runs" / f100["adapter"]
        want |= {run / "adapter_model.safetensors": f100["adapter_sha256"],
                 run / "adapter_config.json": f100["adapter_config_sha256"]}
    if weights:
        want |= base_snapshot(P["models"]["base"])
    if instrument:
        want |= pinned(P)
    verify(want)
    return P


def subsets(pool: list[str], seed: int = SEED) -> dict[str, list[str]]:
    """The registered rule: prefixes of one seeded permutation of the pool (train_rl.schedule over all of it),
    sizes floor(len(pool) x pct / 100), so each subset is nested in the next."""
    order = schedule(pool, len(pool), seed)
    return {k: order[: len(pool) * pct // 100] for k, pct in PCTS.items()}


def write_once(path: Path, body: bytes) -> None:
    """Write body unless the file exists; an existing file must already hold exactly body (never overwritten)."""
    if not path.exists():
        path.write_bytes(body)
    elif path.read_bytes() != body:
        raise SystemExit(f"{path} exists with other content; refusing to overwrite it")


def write_subsets(P: dict, d: Path) -> list[str]:
    """Each subset's ids file from the JSON, asserted equal to the rule's prefix, free of dev300 images and at its
    registered sha256; then d/registered.sha256: the registered sha256 of the ids files and of the sft.jsonl files
    build_gold_sft.py must reproduce from them (sha256sum -c format, names relative to d)."""
    rule, dev = subsets(read_ids(ROOT / POOL)), set(read_ids(ROOT / DEV))
    d.mkdir(parents=True, exist_ok=True)
    lines = []
    for k, s in P["data"]["subsets"].items():
        body = ("\n".join(s["ids"]) + "\n").encode()
        if s["ids"] != rule[k] or dev & set(s["ids"]) or hashlib.sha256(body).hexdigest() != s["ids_sha256"]:
            raise SystemExit(f"{k}: the registered ids are not the rule's prefix, hold dev300 images or miss "
                             "their sha256")
        write_once(d / s["ids_file_name"], body)
        lines += [f"{s['ids_sha256']}  {s['ids_file_name']}", f"{s['sft_jsonl_sha256']}  gold_p1dev_{k}/sft.jsonl"]
    write_once(d / "registered.sha256", ("\n".join(lines) + "\n").encode())
    return lines


def fresh(path: Path) -> Path:
    """path, or the first of path_v2, path_v3, ... that does not exist: an output is never overwritten."""
    out, v = path, 2
    while out.exists():
        out, v = path.with_name(f"{path.stem}_v{v}{path.suffix}"), v + 1
    return out


def ols(x, y) -> tuple:
    """(a, b) of y = a + b x by ordinary least squares, per column when y is (len(x), k)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    xc = x - x.mean()
    b = xc @ (y - y.mean(0)) / (xc @ xc)
    return y.mean(0) - b * x.mean(), b


def corpus(m: dict, idx: np.ndarray) -> dict[str, np.ndarray]:
    """Each metric of one model on every row of image indices idx (k, n), recomputed from its per-image values."""
    return {"CIDEr_D_x100": m["cider"][idx].mean(1),
            "F1": np.array([scores([m["rows"][j] for j in r])["F1"] for r in idx]),
            "CHAIR_i": m["halluc"][idx].sum(1) / m["mentions"][idx].sum(1)}


def decide(b: float, ci_lo: float) -> str:
    """The registered rule, its clauses in their written order."""
    if ci_lo > FUND_IF_LO_GT:
        return "FUND_EXTERNAL_IMAGE_DATA"
    if b < CLOSE_IF_B_LT:
        return "CLOSE_DATA_VOLUME_LEVERS"
    return "INCONCLUSIVE"


def fit(models: dict[str, dict], n_train: dict[str, int]) -> dict:
    """Per metric: OLS of the full-sample value on log2(N) over the points (in n_train's order) and the 95% paired
    percentile bootstrap CI of its slope; then the frozen-prediction hits and the decision."""
    keys = list(n_train)
    x = np.log2([n_train[k] for k in keys])
    n = len(models[keys[0]]["cider"])
    assert all(len(models[k][f]) == n for k in keys for f in ("cider", "rows", "mentions", "halluc"))
    idx = np.random.default_rng(BOOT_SEED).integers(0, n, (B, n))
    full = {k: corpus(models[k], np.arange(n)[None]) for k in keys}
    draws = {k: corpus(models[k], idx) for k in keys}
    tail = (100 - LEVEL) / 2
    fits = {}
    for metric in METRICS:
        y = [float(full[k][metric][0]) for k in keys]
        a, b = ols(x, y)
        lo, hi = np.percentile(ols(x, np.stack([draws[k][metric] for k in keys]))[1], [tail, 100 - tail])
        fits[metric] = {"y": dict(zip(keys, y)), "a": float(a), "b": float(b), "ci95": [float(lo), float(hi)]}
    b, lo = fits["CIDEr_D_x100"]["b"], fits["CIDEr_D_x100"]["ci95"][0]
    return {"N": n_train, "x_log2N": dict(zip(keys, x.tolist())), "fits": fits,
            "frozen_prediction_hit": {m: bool(PRED[m][0] <= fits[m]["b"] <= PRED[m][1]) for m in PRED},
            "bootstrap": {"B": B, "rng": f"numpy default_rng({BOOT_SEED})", "level_pct": LEVEL, "n_images": n,
                          "paired": "one index draw (rl_reward.boot's) shared by every model"},
            "decision": {"verdict": decide(b, lo), "b": b, "ci_lo_b": lo}}


def dev_refs() -> dict[str, list[str]]:
    """The five KTVIC references of each dev300 image, as dev_data.json holds them (KTVIC train's)."""
    if KTVIC.name != "ktvic":
        raise SystemExit("unset NCS_DATASET: the dev300 references are read from KTVIC train")
    refs = references("train_data.json")
    return {i: refs[i] for i in sorted(read_ids(ROOT / DEV))}


def object_counts(preds: dict[str, str], gt: dict[str, list[str]]) -> dict:
    """Per image, in sorted id order: object_prf rows against the union of the references' classes (exact classes,
    gold as object_prf.ktvic_block builds it) and rescap.chair counts, called as evaluate.py calls it."""
    ids = sorted(gt)
    ch = chair({i: preds[i] for i in ids}, gt, strict_ids=False)
    assert [c["image_id"] for c in ch.per_caption] == ids
    gold = {i: set().union(*(set(objects_in(r)) for r in gt[i])) for i in ids}
    return {"rows": [image_counts(set(objects_in(preds[i])), gold[i], lambda o: {o}) for i in ids],
            "mentions": np.array([c["n_mentions"] for c in ch.per_caption]),
            "halluc": np.array([len(c["hallucinated"]) for c in ch.per_caption]),
            "CHAIR_i": ch.chair_i, "mentions_per_caption": ch.mentions_per_caption}


def per_image(result: Path, reward, gt: dict[str, list[str]]) -> dict:
    """One evaluate.py dev300 result as per-image arrays, each checked against the result's own numbers: CIDEr-D x100
    by rl_report.dev_scores (which asserts their mean), CHAIR_i equal to the result's."""
    res = json.loads(result.read_text(encoding="utf-8"))
    head = (res["split"], res["prompt_style"], res["n_images"], {r["segmenter"] for r in res["results"]})
    if head != ("dev_data.json", "short", DEV_N, {"rdrsegmenter"}):
        raise SystemExit(f"{result}: not a short-prompt dev300 decode scored with RDRSegmenter: {head}")
    ids, preds, cider = rl_report.dev_scores(str(result), reward)
    m = object_counts(preds, gt)
    if ids != sorted(gt) or m["CHAIR_i"] != res["chair"]["CHAIR_i"]:
        raise SystemExit(f"{result}: other images, or CHAIR_i {m['CHAIR_i']} is not its {res['chair']['CHAIR_i']}")
    return m | {"preds": preds, "cider": cider, "adapter": res["adapter"]}


def n2_reproduced(P: dict, m: dict) -> dict:
    """The registered n2 decode's object and CHAIR numbers, recomputed here to their registered rounding: the
    instrument must reproduce them before its numbers on the new models are the registered metrics."""
    s, ref = scores(m["rows"]), P["p1dev_reference_dev300"]
    got = {"P_ktvic5": round(s["P"], 3), "R_ktvic5": round(s["R"], 3), "F1_ktvic5": round(s["F1"], 3),
           "CHAIR_i": m["CHAIR_i"], "mentions_per_caption": m["mentions_per_caption"]}
    bad = {k: [v, ref[k]] for k, v in got.items() if v != ref[k]}
    if bad:
        raise SystemExit(f"the registered n2 numbers are not reproduced (recomputed, registered): {bad}")
    return got


def point(P: dict, key: str, result: Path, run: Path, m: dict) -> dict:
    """One point's provenance and full-sample numbers; its adapter must carry the registered LoRA recipe and base."""
    cfg = json.loads((run / "adapter_config.json").read_text(encoding="utf-8"))
    lora = P["models"]["f100"]["lora"]
    if {k: cfg.get(k) for k in lora} != lora or cfg.get("base_model_name_or_path") != P["models"]["base"]["id"]:
        raise SystemExit(f"{run}: not the registered LoRA recipe on the registered base")
    if m["adapter"] is not None and Path(m["adapter"]).resolve() != run.resolve():
        raise SystemExit(f"{result} was decoded with {m['adapter']}, not {run}")
    s = scores(m["rows"])
    return {"name": RUNS[key], "N": sizes()[key], "result": str(result), "result_sha256": sha256(result),
            "preds_sha256": sha256(result.with_suffix(".preds.json")), "adapter": str(run),
            "adapter_sha256": sha256(run / "adapter_model.safetensors"),
            "resumed_from_step": hook.provenance_metadata(run)["resumed_from_step"],
            "CIDEr_D_x100": float(m["cider"].mean()), "P": s["P"], "R": s["R"], "F1": s["F1"],
            "CHAIR_i": m["CHAIR_i"], "mentions_per_caption": m["mentions_per_caption"]}


def analyse(d: Path) -> Path:
    """The registered analysis of the three dev300 decodes in d; writes d/scaling.json or its next _vN."""
    P = check(machine=True, instrument=True)
    gt = dev_refs()
    reward = rl_report._dev_reward(sorted(gt))
    runs = {k: DATA / "runs" / RUNS[k] for k in PCTS} | {"f100": DATA / "runs" / P["models"]["f100"]["adapter"]}
    results = {k: d / f"{RUNS[k]}-dev300-short.json" for k in runs}
    n2 = per_image(ROOT / N2, reward, gt)
    reproduced = n2_reproduced(P, n2)
    models = {k: per_image(results[k], reward, gt) for k in runs}
    points = {k: point(P, k, results[k], runs[k], models[k]) for k in runs}
    same = sum(models["f100"]["preds"][i] == n2["preds"][i] for i in gt)
    cider = {"n2": float(n2["cider"].mean()), "redecode": float(models["f100"]["cider"].mean())}
    out = {"prereg_id": P["prereg_id"], "job": JOB, "status": P["decision_rule"]["status"], "split": P["data"]["split"],
           "provenance": hook.provenance_metadata(None) | {
               "prereg_sha256": PREREG_SHA256[PREREG], "instrument_sha256": sha256(INSTRUMENT),
               "scaling_probe_sha256": sha256(Path(__file__).resolve()), "job_file_sha256": sha256(ROOT / JOB_FILE)},
           "points": points, **fit(models, sizes()),
           "step0_agreement": {"use": "reported, never used to select anything", "n2_result": N2,
                               "identical_captions": same, "n_images": len(gt), "identical_share": same / len(gt),
                               "CIDEr_D_x100": cider, "redecode_minus_n2": cider["redecode"] - cider["n2"]},
           "n2_reproduced": reproduced | {"CIDEr_D_x100_per_image_mean": cider["n2"]}}
    out["decision"] |= {"rule": P["decision_rule"]["rule"],
                        "consequence": P["decision_rule"]["meaning"][out["decision"]["verdict"]]}
    path = fresh(d / "scaling.json")
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out["decision"], ensure_ascii=False, indent=1), f"\nwrote {path}")
    return path


def _refused(fn, *args) -> bool:
    try:
        fn(*args)
    except SystemExit:
        return True
    return False


def _alternating(spread: int) -> np.ndarray:
    return spread * np.where(np.arange(DEV_N) % 2, -1, 1)


def _synthetic(slope: int, spread: int) -> dict[str, dict]:
    """Three models on DEV_N images. CIDEr-D_i = c_i + slope x + d_i s, with d = +-spread alternating (mean 0, so the
    full-sample slope is exactly slope) and s = -1, 0, +1 over the points; the object rows and CHAIR counts are the
    same on every image within a model, so their bootstrap CIs collapse onto their point slopes."""
    x = np.log2(list(sizes().values()))
    c, d = 100 + 5 * (np.arange(DEV_N) % 7), _alternating(spread)
    out = {}
    for j, k in enumerate(sizes()):
        row = image_counts(set("abcd"[: j + 1]) | {"z"}, set("abcd"), lambda o: {o})
        out[k] = {"cider": c + slope * x[j] + d * (j - 1), "rows": [row] * DEV_N,
                  "mentions": np.full(DEV_N, 4), "halluc": np.full(DEV_N, j)}
    return out


def _test_fit() -> None:
    """OLS on known lines; then fit() on synthetic models: the paired CIDEr-D CI is the slope plus slope(s) times
    rl_reward.boot's CI of mean(d) (the same index draw), the F1 and CHAIR_i CIs collapse onto their slopes, the
    output is plain JSON and repeatable, and each registered outcome comes out of the data at least once."""
    x = np.log2(list(sizes().values()))
    a, b = ols(x, 5 + 3 * x)
    assert abs(a - 5) < 1e-9 and abs(b - 3) < 1e-9, (a, b)
    assert np.allclose(ols(x, np.outer(x, [0, 1, 2]) + 7)[1], [0, 1, 2])
    k = ols(x, [-1, 0, 1])[1]
    outcomes = set()
    for slope, spread, want in ((3, 1, "FUND_EXTERNAL_IMAGE_DATA"), (0, 1, "CLOSE_DATA_VOLUME_LEVERS"),
                                (2, 30, "INCONCLUSIVE")):
        models = _synthetic(slope, spread)
        out = fit(models, sizes())
        assert json.dumps(out) == json.dumps(fit(models, sizes()))
        f, (_, lo, hi) = out["fits"], boot(_alternating(spread))
        assert abs(f["CIDEr_D_x100"]["b"] - slope) < 1e-9 and np.allclose(f["CIDEr_D_x100"]["ci95"],
                                                                          [slope + k * lo, slope + k * hi])
        f1 = [scores(models[key]["rows"])["F1"] for key in sizes()]
        for metric, y in (("F1", f1), ("CHAIR_i", [0, 1 / 4, 2 / 4])):
            assert np.allclose(f[metric]["ci95"], [ols(x, y)[1]] * 2) and np.isclose(f[metric]["b"], ols(x, y)[1])
        lo_b, hi_b = PRED["CIDEr_D_x100"]
        assert out["frozen_prediction_hit"]["CIDEr_D_x100"] == (lo_b <= slope <= hi_b)
        assert out["decision"]["verdict"] == want, (slope, spread, out["decision"])
        outcomes.add(out["decision"]["verdict"])
    assert outcomes == set(OUTCOMES)


def _test_corpus() -> None:
    """corpus() on a hand-made model and a draw with a repeat: CIDEr-D is the mean of the per-image values, F1
    object_prf's exact F1 (not the hypernym-credited F1_spec), CHAIR_i all hallucinated over all mentions."""
    anc = {"dog": {"dog", "animal"}}
    rows = [image_counts({"dog", "animal"}, {"dog", "cat"}, lambda o: anc.get(o, {o})),
            image_counts({"car"}, {"bus"}, lambda o: {o})]
    m = {"cider": np.array([10, 40]), "rows": rows, "mentions": np.array([1, 3]), "halluc": np.array([1, 0])}
    got, drawn = corpus(m, np.array([[0, 0, 1]])), scores([rows[0], rows[0], rows[1]])
    assert got["CIDEr_D_x100"].tolist() == [20] and got["CHAIR_i"].tolist() == [2 / 5]
    assert got["F1"].tolist() == [drawn["F1"]] != [drawn["F1_spec"]]


def _test_decide() -> None:
    """The rule's boundaries (both inequalities strict) and its written clause order."""
    table = {(1, 1): "INCONCLUSIVE", (2, 1): "INCONCLUSIVE", (0.99, 0.5): "CLOSE_DATA_VOLUME_LEVERS",
             (1.5, 1.01): "FUND_EXTERNAL_IMAGE_DATA", (5, 0.9): "INCONCLUSIVE", (0.5, 1.5): "FUND_EXTERNAL_IMAGE_DATA"}
    for (b, lo), want in table.items():
        assert decide(b, lo) == want, (b, lo, decide(b, lo))


def _test_subsets(P: dict) -> None:
    """The rule on a synthetic pool (deterministic, independent of the pool's order, nested, floor sizes, seeded),
    then on the real pool: the registered ids and counts, nested, no dev300 image; ids files written once."""
    pool = [str(i) for i in range(1, 102)]
    a = subsets(pool)
    assert a == subsets(pool[::-1]) and [len(v) for v in a.values()] == [25, 50] and a["f50"][:25] == a["f25"]
    assert subsets(pool, SEED + 1) != a and set(a["f50"]) < set(pool)
    real, reg = subsets(read_ids(ROOT / POOL)), P["data"]["subsets"]
    assert [len(real[k]) for k in PCTS] == [reg[k]["n_images"] for k in PCTS] == [sizes()[k] for k in PCTS]
    assert all(real[k] == reg[k]["ids"] for k in PCTS) and real["f50"][: sizes()["f25"]] == real["f25"]
    assert not set(real["f50"]) & set(read_ids(ROOT / DEV)) and set(real["f50"]) < set(read_ids(ROOT / POOL))
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        assert write_subsets(P, d) == write_subsets(P, d)
        assert all(sha256(d / reg[k]["ids_file_name"]) == reg[k]["ids_sha256"] for k in PCTS)
        (d / reg["f25"]["ids_file_name"]).write_text("1\n", encoding="utf-8")
        assert _refused(write_subsets, P, d)


def _test_refusals(P: dict) -> None:
    """A changed constant or file is refused; an existing output is never overwritten."""
    bad = json.loads(json.dumps(P))
    bad["analysis"]["ci"]["B"] = B - 1
    assert _refused(registered, bad)
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "scaling.json"
        f.write_text("{}", encoding="utf-8")
        assert _refused(verify, {f: hashlib.sha256(b"[]").hexdigest()})
        verify({f: hashlib.sha256(b"{}").hexdigest()})
        assert fresh(f).name == "scaling_v2.json"
        fresh(f).write_text("{}", encoding="utf-8")
        assert fresh(f).name == "scaling_v3.json" and _refused(write_once, f, b"[]")


def selftest() -> None:
    """CPU only: the registered checks, refusals, subsets, decision table, corpus metrics and fit on synthetic data,
    then the object and CHAIR numbers of the registered n2 decode recomputed (CIDEr-D needs the segmenter: --analyse
    checks it)."""
    P = check()
    _test_refusals(P)
    _test_subsets(P)
    _test_decide()
    _test_corpus()
    _test_fit()
    n2_reproduced(P, object_counts(rl_report._preds(str(ROOT / N2)), dev_refs()))
    print("scaling_probe self-test ok")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--selftest", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--subsets", type=Path, metavar="DIR")
    mode.add_argument("--analyse", type=Path, metavar="DIR")
    ap.add_argument("--machine", action="store_true", help="--check: also the p1dev_s42 adapter and the base weights")
    ap.add_argument("--instrument", action="store_true", help="--check, --subsets: also the addendum's pins")
    args = ap.parse_args()
    if args.selftest:
        selftest()
    elif args.check:
        check(machine=args.machine, weights=args.machine, instrument=args.instrument)
        print("scaling_probe check ok")
    elif args.subsets:
        print("\n".join(write_subsets(check(instrument=args.instrument), args.subsets)))
    else:
        analyse(args.analyse)
    return 0


if __name__ == "__main__":
    sys.exit(main())
