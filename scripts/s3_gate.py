#!/usr/bin/env python
"""S3 (T3.3): the registered checks, job inputs, guards and verdicts of M3 CM-DPO stage 1 and CM-RFT on dev300.

    python scripts/s3_gate.py --check [--machine]       # registration and code shas, every registered constant and every
                                                        # input this machine holds; exit 1 on any failure
    python scripts/s3_gate.py --prep OUT                # OUT/rl1000_ids.txt, OUT/rl250_ids.txt and the evaluate.py
                                                        # datasets $NCS_DATA/datasets/ktvic_s3rl/rl{1000,250}_data.json
    python scripts/s3_gate.py --score OUT ARM           # needs the JVM: syllables, fragments, copy rates, CIDEr CI
    python scripts/s3_gate.py --akl-trigger OUT         # prints yes iff arm A failed guard G2 or G3
    python scripts/s3_gate.py --verdict OUT --out JSON  # every registered estimate, guard and verdict
    python scripts/s3_gate.py --selftest                # CPU, synthetic data: pairs, estimators, guards, verdicts, H5

Registration: manuscript/prereg/2026-10-18_tier3_S3.{md,json} (a68fb66) and its amendment 1 (59901cc: the H5 kill
rule). ARM is A (cmdpo_A_s42), R (cmrft_s42) or AKL (cmdpo_AKL_s42), each compared with p1dev_s42_redecode, P1_dev
decoded on the job's machine. OUT holds the job's files under the names scripts/queue/jobs/t3_3_s3_cm_dpo_rft.sh gives
them. Estimators (prereg §6): classes = rescap.chair.objects_in (matcher v2), exact; m = mean distinct classes per
caption; P/R/F1 = object_prf.scores; residual = F1 - prereg_ladder_check.at(frontier, m)[2]; panel_cm = the same F1 on
the panel images whose class count did not change, against the panel classes; paired percentile bootstrap over images,
B = 2000, numpy default_rng(0), as rl_reward.boot. The panel (data/ktvic_openviic_refs.json, git-excluded) is read here
only, sha-checked, and no caption text is written. Without it every other number is computed and a verdict that depends
on panel_cm is PENDING_PANEL; rerun --verdict where the file is.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]

REGISTERED = {  # the registration under test (a68fb66) and its amendment 1 (59901cc)
    "manuscript/prereg/2026-10-18_tier3_S3.json": "b39f682f21e6794f5e966779c381bfe6c68ae65d542af4b5571e3b7b9abf361f",
    "manuscript/prereg/2026-10-18_tier3_S3.md": "2741c448019cbae2cc57101fd8c3487327e8482fa91457eea115e9442ec48311",
    "manuscript/prereg/2026-10-18_tier3_S3_amendment1.json":
        "2aea5b27301792b0d7c301623797e3ca4db046adcbbf2227c1adfe768d943269",
}
PREREG = ROOT / "manuscript/prereg/2026-10-18_tier3_S3.json"
ADDENDUM = ROOT / "manuscript/prereg/2026-10-18_tier3_S3_instrument.json"
PANEL = ROOT / "data/ktvic_openviic_refs.json"
N2 = ROOT / "data/results/rl/p1dev_s42-dev300-short"  # the registered n2 decode of P1_dev (.preds.json, .json)
DRAFT = ROOT / ".session_backup/2026-10-14/research_r10/M3/cm_pairs.py"
DRAFT_CHANGED_LINES = (30, 109, 110, 111, 112, 113)  # cm_pairs.py vs the draft: the aislop import fix, the self-check
JOB_FILES = ("scripts/s3_gate.py", "scripts/cm_pairs.py", "scripts/cm_rft.py", "scripts/train_stage2_anchor.py",
             "scripts/queue/jobs/t3_3_s3_cm_dpo_rft.sh")
RUNS = {"A": "cmdpo_A_s42", "R": "cmrft_s42", "AKL": "cmdpo_AKL_s42"}
P1 = "p1dev_s42_redecode"

FRONTIER = {"M1": 1.7826, "TP1": 1.3996, "b": 0.7468, "c0": 5.4859, "c1": 25.9815}
B, BOOT_SEED = 2000, 0
D_RES_LO, PANEL_LO = 0, -0.5  # PD-9 Q2: d_res_lo > 0 and panel_cm_lo > -0.5
G1_DM, G2_CIDER, G3_CJK, G4_SYL, G5_FRAG, N_DEV = 0.2, 141.33, 1, (10.69, 13.06), 15, 300
COPY_N, COPY_X = 250, 2
PASS_D = {"A": 1.5, "AKL": 1.5, "R": 1.0}
GREY_D = {"A": 0.5, "AKL": 0.5, "R": 0.3}
DPO = {"beta": 0.1, "lr": 5e-6, "epochs": 1, "grad_accum": 8, "anchor_sft": 1.0, "token_kl": 0, "seed": 42}
AKL = dict(DPO, lr=2.5e-6, anchor_sft=0, token_kl=0.4)
DRY_PAIRS, DRY_GB = 20, 22
RFT = {"epochs": 1, "lr": 1e-5}
SAMPLER = {"n": 6, "temperatures": (0.5, 0.8), "top_p": 0.95, "seed": 42}
RL_N, RL_SEED, RL_SHA256 = 1000, 42, "3651875cf0368922f67b68816533838a7453658761e9bc728962fb84873866aa"
PRED = {
    "A": {"dm_abs_max": 0.1, "d_res": [0.5, 2.5], "d_res_point": 1.2, "dCHAIR_i_max": -0.005,
          "expected": {"d_res": [0.5, 2.0], "dCHAIR_i": [-0.02, -0.005], "dm_abs_max": 0.1, "dCIDEr": [-3, 2]}},
    "R": {"d_res": [0.3, 1.5], "dm_abs_max": 0.05,
          "expected": {"d_res": [0.3, 1.5], "dCHAIR_i": [-0.015, -0.003], "dCIDEr": [-2, 1]}},
}
ATTRIBUTION_MIN = 0.5
GUARD_RULES = {"G1": "|dm| <= 0.2", "G2": "dev CIDEr-D x100 >= 141.33", "G3": "<= 1 of 300 dev captions with CJK",
               "G4": "mean syllables in [10.69, 13.06]", "G5": "<= 15 of 300 fragment captions",
               "G6": "exact-copy rate on the first 250 RL images <= 2 x max(P1_dev's rate, 1/250)"}
DEVIATIONS = [
    {"id": "amendment1", "commit": "59901cc", "file": "manuscript/prereg/2026-10-18_tier3_S3_amendment1.json",
     "written_utc": "2026-10-18T09:19:13Z", "before_any_output": True, "decision": "judge CC-017 YES",
     "change": "H5 KILL fires iff (dR_UB < 0) OR (dP_LB > 0 AND dR < 0); H5 still changes no verdict",
     "reason": "R14-2's 'dR < 0 with LB > 0' cannot hold as written (A-verifier flag)"},
    {"id": "file_layout", "decision": "D-W13-4 (main, PI)",
     "change": "--anchor-sft and --token-kl live in scripts/train_stage2_anchor.py, which imports scripts/train_stage2.py "
               "unchanged, instead of an edit of train_stage2.py",
     "reason": "train_stage2.py (29312ef7) is registered byte for byte by the S1 and S5 preregs and used by every running "
               "job; no design, input, prediction, gate or constant changes"},
]
S = "sources"


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 23), b""):
            h.update(chunk)
    return h.hexdigest()


def _json(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _get(d, path: tuple):
    """The value at a key path, or None when the path is missing (a registered constant is never null)."""
    for k in path:
        if not isinstance(d, dict) or k not in d:
            return None
        d = d[k]
    return d


def _write_once(path: Path, text: str) -> None:
    """Never overwrite an output: an identical rewrite is a no-op, anything else is refused (write a _v2)."""
    path = Path(path)
    if path.exists():
        if path.read_text(encoding="utf-8") != text:
            raise SystemExit(f"{path} exists with other content: refusing to overwrite it (write a _v2)")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1, default=float) + "\n"


def _checks() -> list[tuple]:
    """(value in this code, its key path in the prereg JSON) for every registered constant the job uses."""
    import cm_pairs

    fp = "frozen_predictions"
    draft = ".session_backup/2026-10-14/research_r10/M3/cm_pairs.py:"
    return ([(v, ("frontier", k)) for k, v in FRONTIER.items()]
            + [(v, (S, f"frontier.{k}", "value")) for k, v in FRONTIER.items()]
            + [(v, (S, f"guards.M3[{n}]", "value"))
               for n, v in enumerate((G1_DM, G2_CIDER, G3_CJK, N_DEV, *G4_SYL, G5_FRAG, N_DEV))]
            + [(v, (S, f"dpo[{n}]", "value")) for n, v in enumerate(
                (DPO["beta"], DPO["lr"], DPO["epochs"], DPO["grad_accum"], DPO["anchor_sft"], DPO["seed"]))]
            + [(v, (S, f"sampler[{n}]", "value")) for n, v in enumerate(
                (SAMPLER["n"], SAMPLER["temperatures"][0], SAMPLER["n"], SAMPLER["temperatures"][1], SAMPLER["top_p"],
                 SAMPLER["seed"]))]
            + [(v, (S, f"builder[{n}]", "value")) for n, v in enumerate((cm_pairs.CAP, cm_pairs.MAX_DSYL,
                                                                        cm_pairs.COPY_TAU))]
            + [(getattr(cm_pairs, k), (S, draft + k, "value")) for k in ("CAP", "MAX_DSYL", "COPY_TAU")]
            + [(B, ("analysis", "ci", "B")), (B, (S, "bootstrap.B", "value")), (BOOT_SEED, (S, "bootstrap.seed", "value")),
               (D_RES_LO, ("gate", "PD9_conditions", "d_res_ci_lower_min_exclusive")),
               (PANEL_LO, ("gate", "PD9_conditions", "panel_cm_ci_lower_min_exclusive")),
               (COPY_N, (S, "copy.block_images", "value")), (COPY_X, (S, "copy.multiple", "value")),
               (PASS_D["A"], ("gate", "thresholds", "CM-DPO_pass_d_res")),
               (GREY_D["A"], ("gate", "thresholds", "CM-DPO_grey_d_res_min")),
               (PASS_D["R"], ("gate", "thresholds", "CM-RFT_pass_d_res")),
               (GREY_D["R"], ("gate", "thresholds", "CM-RFT_grey_d_res_min")),
               (AKL["token_kl"], (S, "fallback.A-KL[0]", "value")), (AKL["lr"], (S, "fallback.A-KL[1]", "value")),
               (DRY_PAIRS, (S, "dry_run[0]", "value")), (DRY_GB, (S, "dry_run[1]", "value")),
               (RFT["epochs"], (S, "rft[0]", "value")), (RFT["lr"], (S, "rft[1]", "value")),
               (RL_N, (S, "images.rule[0]", "value")), (RL_SEED, (S, "images.rule[2]", "value")),
               (RL_N, ("data", "rl_images", "n")), (RL_SHA256, ("data", "rl_images", "sha256_newline_joined")),
               (N_DEV, ("data", "splits", "data/splits/ktvic_dev300.txt", "n_images")),
               (PRED["A"]["dm_abs_max"], (fp, "CM-DPO", "H1_dm_abs_max")), (PRED["A"]["d_res"], (fp, "CM-DPO", "H2_d_res")),
               (PRED["A"]["d_res_point"], (fp, "CM-DPO", "H2_point")),
               (PRED["A"]["dCHAIR_i_max"], (S, "pred.CM-DPO.H5_dCHAIRi_max", "value")),
               (PRED["R"]["d_res"], (fp, "CM-RFT", "d_res")), (PRED["R"]["dm_abs_max"], (fp, "CM-RFT", "dm_abs_max")),
               (ATTRIBUTION_MIN, (S, "pred.DPO_minus_RFT_min", "value"))]
            + [(v, (fp, "CM-DPO", "expected", k)) for k, v in PRED["A"]["expected"].items()]
            + [(v, (fp, "CM-RFT", "expected", k)) for k, v in PRED["R"]["expected"].items()])


def _input_path(rel: str, data: Path) -> Path | None:
    """Where a registered input lives here: the repo path, else its $NCS_DATA path on a GPU machine."""
    cands = [ROOT / rel]
    for prefix, base in ((".session_backup/machines/n2/ncs-data/", data), ("data/datasets/", data / "datasets")):
        if rel.startswith(prefix):
            cands.append(base / rel[len(prefix):])
    return next((p for p in cands if p.is_file()), None)


def _required(rel: str, machine: bool) -> bool:
    """Repo inputs always; the start adapter's config on a GPU machine; the session records and the panel never."""
    if rel == ".session_backup/machines/n2/ncs-data/runs/p1dev_s42/adapter_config.json":
        return machine
    return not rel.startswith(".session_backup/") and rel != "data/ktvic_openviic_refs.json"


def _check_weights(pre: dict, data: Path) -> list[str]:
    """The start adapter and the base snapshot this machine loads (refs/main = the registered revision)."""
    bad = []
    adapter = data / "runs/p1dev_s42/adapter_model.safetensors"
    if not adapter.is_file() or _sha(adapter) != pre["models"]["start_and_reference"]["adapter_sha256"]:
        bad.append(f"{adapter}: missing or not the registered p1dev_s42 adapter")
    base = pre["models"]["base"]
    hub = Path(os.environ.get("HF_HUB_CACHE") or Path(os.environ.get("HF_HOME", Path.home() / ".cache/huggingface")) / "hub")
    repo = hub / ("models--" + base["id"].replace("/", "--"))
    ref = repo / "refs" / "main"
    if not ref.is_file() or ref.read_text(encoding="utf-8").strip() != base["revision"]:
        bad.append(f"{ref}: the cached base is not revision {base['revision']}")
    for name, want in base["shards_sha256"].items():
        shard = repo / "snapshots" / base["revision"] / name
        if not shard.is_file() or _sha(shard) != want:
            bad.append(f"{shard}: missing or sha256 differs")
    return bad


def _check_anchor(ids: list[str], sft: Path | None, refs: dict) -> list[str]:
    """The anchor caption, refs[i][0], is P1's own SFT target (prompt and response) on every RL image."""
    from evaluate import PROMPTS

    if sft is None:
        return []
    rows = {str(r["image_id"]): r for r in (json.loads(x) for x in sft.read_text(encoding="utf-8").splitlines()
                                            if x.strip())}
    off = [i for i in ids if i not in rows or rows[i]["response"] != refs[i][0] or rows[i]["prompt"] != PROMPTS["short"]]
    return [f"{sft}: the first reference is not P1's SFT target on {len(off)} RL images"] if off else []


def _check_instrument() -> list[str]:
    """On a GPU machine: this job's files are the ones the instrument addendum pins."""
    if not ADDENDUM.is_file():
        return [f"{ADDENDUM.relative_to(ROOT)} is missing: the job is queued only after it is committed"]
    pins = _json(ADDENDUM)["files_sha256"]
    return [f"{rel}: sha256 differs from the instrument addendum" for rel, want in pins.items() if _sha(ROOT / rel) != want]


def check(machine: bool = False) -> dict:
    """Refuse to run (SystemExit) unless the registration, every registered constant and every input here match."""
    import cm_pairs
    from evaluate import DATA, KTVIC, PROMPTS, references

    bad = [f"{rel}: sha256 differs from the registration" for rel, want in REGISTERED.items() if _sha(ROOT / rel) != want]
    if bad:
        raise SystemExit("S3 check FAILED:\n  " + "\n  ".join(bad))
    if KTVIC.name != "ktvic":
        bad.append(f"NCS_DATASET={KTVIC.name}: the registered splits and gold are on KTVIC train")
    if os.environ.get("RESCAP_RAW_TONE") == "1":
        bad.append("RESCAP_RAW_TONE=1 selects matcher v1; the registration uses matcher v2")
    if cm_pairs.PROMPT_SHORT != PROMPTS["short"]:
        bad.append("cm_pairs.PROMPT_SHORT is not evaluate.py's short prompt")
    pre = _json(PREREG)
    bad += [f"{'/'.join(map(str, p))}: prereg {_get(pre, p)!r}, code {v!r}" for v, p in _checks() if _get(pre, p) != v]
    bad += [f"{rel}: not the registered code_at_head" for rel, want in pre["code_at_head"].items()
            if _sha(ROOT / rel) != want]
    present, absent = [], []
    for rel, want in pre["inputs_sha256"].items():
        p = _input_path(rel, DATA)
        if p is not None and _sha(p) != want:
            bad.append(f"{rel} ({p}): sha256 differs from the registration")
        elif p is not None:
            present.append(rel)
        elif _required(rel, machine):
            bad.append(f"{rel}: missing on this machine")
        else:
            absent.append(rel)
    if DRAFT.is_file():  # its sha256 is checked above with the other inputs; line-for-line replacements only
        a, b = (p.read_text(encoding="utf-8").splitlines() for p in (DRAFT, ROOT / "scripts/cm_pairs.py"))
        if len(a) != len(b) or tuple(n + 1 for n in range(len(a)) if a[n] != b[n]) != DRAFT_CHANGED_LINES:
            bad.append("scripts/cm_pairs.py differs from the M3 draft on other lines than the listed ones")
    if machine:
        bad += _check_weights(pre, DATA) + _check_instrument()
    ids = rl_ids()
    bad += _check_anchor(ids, _input_path(".session_backup/machines/n2/ncs-data/gold_p1dev/sft.jsonl", DATA),
                         references("train_data.json"))
    if bad:
        raise SystemExit("S3 check FAILED:\n  " + "\n  ".join(bad))
    return {"ok": True, "machine": machine, "constants_checked": len(_checks()), "code_at_head": len(pre["code_at_head"]),
            "inputs_present": present, "inputs_absent_here": absent, "rl_images": len(ids), "provenance": provenance()}


def provenance() -> dict:
    """The committed hook's stamp (machine_id, git_head_sha, hook and train_stage2 shas) plus this job's script shas."""
    import checkpoint_resume_hook as hook

    meta = hook.provenance_metadata(None)
    del meta["resumed_from_step"]  # per training run: recorded in that run's resume_manifest.json
    meta["job_files_sha256"] = {p: _sha(ROOT / p) for p in JOB_FILES if (ROOT / p).is_file()}
    return meta


def dev_ids() -> list[str]:
    return sorted((ROOT / "data/splits/ktvic_dev300.txt").read_text(encoding="utf-8").split())


def rl_ids() -> list[str]:
    """The 1,000 RL images: train_rl.schedule(train minus dev300, 1000, 42), checked against the registered list."""
    import train_rl

    ids = train_rl.schedule(train_rl.read_ids(str(ROOT / "data/splits/ktvic_train_minus_dev300.txt")), RL_N, RL_SEED)
    if ids != _json(PREREG)["data"]["rl_images"]["ids"] or hashlib.sha256(
            "".join(i + "\n" for i in ids).encode()).hexdigest() != RL_SHA256:
        raise SystemExit("the RL image schedule differs from the registered 1,000 ids")
    return ids


def prep(out: Path) -> None:
    """The RL id files and two evaluate.py datasets (KTVIC layout: the train references of the RL images, images link)."""
    from evaluate import DATA, KTVIC

    ids = rl_ids()
    _write_once(out / "rl1000_ids.txt", "".join(i + "\n" for i in ids))
    _write_once(out / "rl250_ids.txt", "".join(i + "\n" for i in ids[:COPY_N]))
    data = _json(KTVIC / "train_data.json")
    d = DATA / "datasets" / "ktvic_s3rl"
    for name, keep in (("rl1000_data.json", set(ids)), ("rl250_data.json", set(ids[:COPY_N]))):
        sub = {"images": [im for im in data["images"] if str(im.get("id", im.get("image_id"))) in keep],
               "annotations": [a for a in data["annotations"] if str(a["image_id"]) in keep]}
        if len(sub["images"]) != len(keep):
            raise SystemExit(f"{name}: {len(sub['images'])} of {len(keep)} images found in train_data.json")
        _write_once(d / name, json.dumps(sub, ensure_ascii=False))
    link = d / "images"
    if not link.exists():
        link.symlink_to(KTVIC / "images")
    if link.resolve() != (KTVIC / "images").resolve():
        raise SystemExit(f"{link} does not point at {KTVIC / 'images'}")


def score(out: Path, arm: str) -> dict:
    """The JVM half (RDRSegmenter): caption stats (G4, G5), exact-copy rates (G6), the paired per-image CIDEr-D CI."""
    from rl_report import _dev_reward, _preds, caption_stats, dev_scores
    from rl_reward import boot

    dev = dev_ids()
    reward = _dev_reward(dev)
    ids, p1, p1_per = dev_scores(str(out / f"{P1}-dev300-short.json"), reward)
    ids_arm, a, a_per = dev_scores(str(out / f"{RUNS[arm]}-dev300-short.json"), reward)
    if not ids == ids_arm == dev:
        raise SystemExit("P1_dev and the arm were not both decoded on the 300 dev images")
    block = rl_ids()[:COPY_N]
    copies = {}
    for who, path in (("p1dev", out / "p1dev_s42-rl1000-short.preds.json"), ("arm", out / f"{RUNS[arm]}-rl250-short.preds.json")):
        caps = _preds(str(path))
        missing = set(block) - caps.keys()
        if missing:
            raise SystemExit(f"{path}: {len(missing)} of the first {COPY_N} RL images are not captioned")
        n = sum(int(reward(i, [caps[i]], [True])[2][0] == 0) for i in block)  # smallest word edit distance 0
        copies[who] = {"n_exact": n, "n_images": COPY_N, "rate": n / COPY_N}
    res = {"arm": arm, "run": RUNS[arm], "caption_stats": {"p1dev": caption_stats(p1, reward), "arm": caption_stats(a, reward)},
           "cider_x100_per_image_paired": boot(a_per - p1_per), "exact_copy_first_250_rl_images": copies,
           "provenance": provenance()}
    _write_once(out / f"score_{arm}.json", _dump(res))
    return res


def _union(texts) -> frozenset:
    from rescap.chair import objects_in

    return frozenset().union(*(objects_in(t) for t in texts))


def _exact(c: str) -> set:
    return {c}


def _rows(preds: dict, gold: dict, ids: list[str]) -> list[tuple]:
    from object_prf import image_counts
    from rescap.chair import objects_in

    return [image_counts(set(objects_in(preds[i] or "")), set(gold[i]), _exact) for i in ids]


def summary(rows: list[tuple]) -> dict:
    """object_prf P/R/F1 (x100), m = mean distinct classes per caption, residual = F1 - frontier F1 at m."""
    from object_prf import scores
    from prereg_ladder_check import at

    s = scores(rows)
    m = sum(r[1] for r in rows) / len(rows)
    return {"P": s["P"], "R": s["R"], "F1": s["F1"], "m": m, "residual": s["F1"] - at(FRONTIER, m)[2]}


def paired(base: list[tuple], arm: list[tuple], keys: tuple) -> dict:
    """arm minus base on the same images: {key: [point, lo, hi]}, percentile bootstrap B = 2000, default_rng(0)."""
    sb, sa = summary(base), summary(arm)
    idx = np.random.default_rng(BOOT_SEED).integers(0, len(base), (B, len(base)))
    draws = []
    for d in idx:
        b, a = summary([base[i] for i in d]), summary([arm[i] for i in d])
        draws.append([a[k] - b[k] for k in keys])
    lo, hi = np.percentile(np.array(draws), [2.5, 97.5], axis=0)
    return {k: [sa[k] - sb[k], float(lo[n]), float(hi[n])] for n, k in enumerate(keys)}


def matched(base: list[tuple], arm: list[tuple]) -> dict:
    """The count-matched estimator: images whose number of distinct classes is the same in both, F1 arm minus base."""
    keep = [n for n in range(len(base)) if base[n][1] == arm[n][1]]
    est = paired([base[n] for n in keep], [arm[n] for n in keep], ("F1",))["F1"] if keep else None
    return {"n_images": len(base), "n_matched": len(keep), "matched_share": len(keep) / len(base), "dF1": est}


def load_decode(path: Path, ids: list[str]) -> dict:
    """An evaluate.py dev result: predictions, word-level CIDEr-D and BLEU-4 (x100), CHAIR_i (0-1)."""
    d = _json(path)
    word = next(r for r in d["results"] if r["tokenization"] == "word-level")
    if word["segmenter"] != "rdrsegmenter" or d["prompt_style"] != "short" or sorted(map(str, d["predictions"])) != ids:
        raise SystemExit(f"{path}: not a short-prompt RDRSegmenter result on the {len(ids)} dev images")
    return {"preds": {str(k): v for k, v in d["predictions"].items()}, "CIDEr": word["scores_scaled_x100"]["CIDEr"],
            "BLEU-4": word["scores_scaled_x100"]["BLEU-4"], "CHAIR_i": d["chair"]["CHAIR_i"]}


def _cjk(preds: dict) -> int:
    from cjk_rate import score_mapping

    return score_mapping(preds)["cjk_captions"]


def decode_guards(dec: dict) -> dict:
    """G2 and G3, which need nothing but the dev decode."""
    return {"G2": dec["CIDEr"] >= G2_CIDER, "G3": _cjk(dec["preds"]) <= G3_CJK}


def akl_triggered(dec_a: dict) -> bool:
    """Prereg §5: A-KL runs only if arm A's verdict is KILL and G2 or G3 failed. A guard failure is a KILL, so the
    trigger is G2 or G3 failing on arm A's dev decode."""
    return not all(decode_guards(dec_a).values())


def guard_table(dm: float, dec: dict, stats: dict, copy: dict) -> dict:
    return {"G1": abs(dm) <= G1_DM, **decode_guards(dec), "G4": G4_SYL[0] <= stats["syllables"] <= G4_SYL[1],
            "G5": stats["fragments"] <= G5_FRAG,
            "G6": copy["arm"]["rate"] <= COPY_X * max(copy["p1dev"]["rate"], 1 / COPY_N)}


def verdict(arm: str, d_res: float, d_res_lo: float, panel_lo: float | None, guards_ok: bool) -> str:
    """Prereg §8. panel_lo None (no panel here): the verdict if it does not depend on panel_cm, else PENDING_PANEL."""
    if panel_lo is None:
        both = {verdict(arm, d_res, d_res_lo, x, guards_ok) for x in (-math.inf, math.inf)}
        return both.pop() if len(both) == 1 else "PENDING_PANEL"
    common = guards_ok and panel_lo > PANEL_LO
    if common and d_res >= PASS_D[arm] and d_res_lo > D_RES_LO:
        return "PASS"
    if arm == "R":
        grey = d_res >= GREY_D[arm]
    else:
        grey = GREY_D[arm] <= d_res < PASS_D[arm] or (d_res >= PASS_D[arm] and d_res_lo <= D_RES_LO)
    return "GREY" if common and grey else "KILL"


def h5(dP: list[float], dR: list[float]) -> dict:
    """Amendment 1 (59901cc): HOLDS iff dP > 0 and dR > 0 (points); KILL iff dR_UB < 0 or (dP_LB > 0 and dR < 0);
    otherwise NOT_SHOWN. Strict inequalities: a value of exactly 0 never fires. H5 changes no verdict."""
    clause1, clause2 = dR[2] < 0, dP[1] > 0 and dR[0] < 0
    state = "KILL" if clause1 or clause2 else "HOLDS" if dP[0] > 0 and dR[0] > 0 else "NOT_SHOWN"
    return {"state": state, "clause1_dR_UB_lt_0": clause1, "clause2_dP_LB_gt_0_and_dR_lt_0": clause2,
            "dP": dP, "dR": dR, "changes_verdict": False}


def _inside(x: float, lo_hi: list) -> bool:
    return lo_hi[0] <= x <= lo_hi[1]


def predictions(arm: str, d_res: float, dm: float, dchair: float, dcider: float) -> dict:
    """The frozen predictions (prereg §7) against the results; reported, none gates (A-KL is judged as arm A)."""
    p = PRED["R" if arm == "R" else "A"]
    out = {"d_res_in_registered_range": _inside(d_res, p["d_res"]), "abs_dm_le_registered_max": abs(dm) <= p["dm_abs_max"],
           "expected_d_res": _inside(d_res, p["expected"]["d_res"]),
           "expected_dCHAIR_i": _inside(dchair, p["expected"]["dCHAIR_i"]),
           "expected_dCIDEr": _inside(dcider, p["expected"]["dCIDEr"])}
    if arm != "R":
        out.update(H5_dCHAIR_i_le_max=dchair <= p["dCHAIR_i_max"], expected_abs_dm=abs(dm) <= p["expected"]["dm_abs_max"])
    return out


def _panel_block(dec: dict, p1: dict, panel: dict | None) -> tuple[dict, float | None]:
    if panel is None:
        return {"status": "panel file absent here: panel_cm and the verdicts that depend on it are pending"}, None
    pids = sorted(panel)
    pa, pp = _rows(dec["preds"], panel, pids), _rows(p1["preds"], panel, pids)
    plain, cm = paired(pp, pa, ("F1", "m")), matched(pp, pa)
    block = {"panel_cm": cm, "plain_dF1": plain["F1"], "dm": plain["m"], "n_images": len(pids)}
    return block, (cm["dF1"][1] if cm["dF1"] else -math.inf)  # no matched image: panel_cm cannot clear -0.5


def arm_block(arm: str, dec: dict, p1: dict, gold: dict, panel: dict | None, scored: dict) -> dict:
    """Every registered estimate, guard and verdict of one arm against the same-machine P1_dev decode."""
    ids = sorted(gold)
    ra, rp = _rows(dec["preds"], gold, ids), _rows(p1["preds"], gold, ids)
    est = paired(rp, ra, ("residual", "P", "R", "F1", "m"))
    panel_block, panel_lo = _panel_block(dec, p1, panel)
    stats, copy = scored["caption_stats"], scored["exact_copy_first_250_rl_images"]
    guards = guard_table(est["m"][0], dec, stats["arm"], copy)
    dchair, dcider = dec["CHAIR_i"] - p1["CHAIR_i"], dec["CIDEr"] - p1["CIDEr"]
    return {"run": RUNS[arm],
            "verdict": verdict(arm, est["residual"][0], est["residual"][1], panel_lo, all(guards.values())),
            "d_res": est["residual"], "panel": panel_block, "guards": guards, "guards_hold": all(guards.values()),
            "h5": h5(est["P"], est["R"]), "dP": est["P"], "dR": est["R"], "dF1": est["F1"], "dm": est["m"],
            "ktvic5": {"arm": summary(ra), "p1dev": summary(rp)}, "ktvic5_count_matched": matched(rp, ra),
            "reported": {"CIDEr": {"arm": dec["CIDEr"], "p1dev": p1["CIDEr"], "d": dcider,
                                   "paired_ci_per_image": scored["cider_x100_per_image_paired"]},
                         "BLEU-4": {"arm": dec["BLEU-4"], "p1dev": p1["BLEU-4"], "d": dec["BLEU-4"] - p1["BLEU-4"]},
                         "CHAIR_i": {"arm": dec["CHAIR_i"], "p1dev": p1["CHAIR_i"], "d": dchair},
                         "caption_stats": stats, "cjk_captions": {"arm": _cjk(dec["preds"]), "p1dev": _cjk(p1["preds"])},
                         "exact_copy_first_250_rl_images": copy},
            "predictions": predictions(arm, est["residual"][0], est["m"][0], dchair, dcider)}


def _extra(out: Path, arm: str) -> dict:
    """Pairs built, RFT images kept, and the run's own record (copied into OUT/runs/<run>/ by the job)."""
    run = out / "runs" / RUNS[arm]
    if arm == "R":
        rep = _json(out / "cm/R/_rft_report.json")
        return {"rft": {k: rep[k] for k in ("images", "kept", "rows")}, "training": _json(run / "resume_manifest.json")}
    rep, tr = _json(out / "cm/A/_build_report.json"), _json(run / "train_summary.json")
    return {"pairs": {"pairs_built": rep["pairs"], "images_with_pairs": rep["images"]},
            "training": {k: tr[k] for k in ("ordering_accuracy", "ordering_accuracy_per_pair_type", "pairs",
                                            "optimizer_steps", "regulariser", "coef", "term_mean", "resumed_from_step",
                                            "provenance")}}


def s3_outcome(a: str, r: str) -> str:
    """S3 passes when an arm PASSES (prereg §8); GREY carries no claim."""
    if "PASS" in (a, r):
        return "PASS"
    return "PENDING_PANEL" if "PENDING_PANEL" in (a, r) else "FAIL"


def verdict_all(out: Path, dev: list[str], refs: dict, panel: dict | None, n2: dict) -> dict:
    """The S3 report: every arm, the A-KL rule shown with arm A, the attribution contrast, the re-decode agreement."""
    gold = {i: _union(refs[i]) for i in dev}
    p1 = load_decode(out / f"{P1}-dev300-short.json", dev)
    decs = {a: load_decode(out / f"{r}-dev300-short.json", dev) for a, r in RUNS.items()
            if (out / f"{r}-dev300-short.json").is_file()}
    if not {"A", "R"} <= decs.keys():
        raise SystemExit("arms A and R must both have a dev300 decode")
    triggered = akl_triggered(decs["A"])
    if triggered != ("AKL" in decs):
        raise SystemExit(f"A-KL trigger {'fired' if triggered else 'did not fire'} but its dev decode is "
                         f"{'missing' if triggered else 'present'}")
    arms = {a: dict(arm_block(a, d, p1, gold, panel, _json(out / f"score_{a}.json")), **_extra(out, a))
            for a, d in decs.items()}
    rows = {a: _rows(d["preds"], gold, dev) for a, d in decs.items()}
    attribution = {f"d_res({a}) - d_res(R)": paired(rows["R"], rows[a], ("residual",))["residual"] for a in decs if a != "R"}
    eff = "AKL" if triggered else "A"
    same = sum(p1["preds"][i] == n2["preds"][i] for i in dev)
    return {
        "outcome": s3_outcome(arms[eff]["verdict"], arms["R"]["verdict"]), "arm_A_counts_as": eff,
        "verdicts": {a: b["verdict"] for a, b in arms.items()},
        "A_and_A-KL": {"rule": "A-KL runs only if arm A's verdict is KILL and G2 or G3 failed; its verdict replaces A's",
                       "A_verdict": arms["A"]["verdict"], "A_failed_guards": [g for g, ok in arms["A"]["guards"].items() if not ok],
                       "triggered": triggered, "A-KL_verdict": arms["AKL"]["verdict"] if triggered else None},
        "attribution": {"values": attribution, "registered_min": ATTRIBUTION_MIN, "gates": False},
        "redecode_agreement": {"n_identical": same, "share_identical": same / len(dev), "CIDEr_redecode": p1["CIDEr"],
                               "CIDEr_n2": n2["CIDEr"], "dCIDEr": p1["CIDEr"] - n2["CIDEr"],
                               "use": "reported only; selects nothing (prereg §5 step 0)"},
        "arms": arms, "p1dev_redecode": summary(_rows(p1["preds"], gold, dev)), "guard_rules": GUARD_RULES,
        "panel_file": "read and sha-checked; no caption text written" if panel is not None else "absent here",
        "deviations": DEVIATIONS, "provenance": provenance()}


def load_panel(dev: list[str]) -> dict | None:
    """Panel classes (objects_in) of the dev images that have panel captions, or None when the file is not here."""
    if not PANEL.is_file():
        return None
    reg = _json(PREREG)["data"]["panel"]
    if _sha(PANEL) != reg["sha256"]:
        raise SystemExit(f"{PANEL}: sha256 differs from the registration")
    second = _json(PANEL)["train"]
    panel = {i: _union(second[i]) for i in dev if second.get(i)}
    if len(panel) != reg["dev_images_with_panel"]:
        raise SystemExit(f"panel covers {len(panel)} dev images, registered {reg['dev_images_with_panel']}")
    return panel


def _raises(fn, exc: type[BaseException]) -> bool:
    """True when fn() raises exc (the selftests' refusal checks)."""
    try:
        fn()
    except exc:
        return True
    return False


def _test_pairs() -> None:
    """cm_pairs.build: count match, |dsyl| <= 2, TP(w) >= TP(l) + 1, the candidate filters, CAP 4 largest dTP first."""
    import cm_pairs
    from evaluate import PROMPTS
    from rescap.chair import objects_in

    ref = "phụ nữ với xe máy trên đường"  # synthetic captions stay under 8 syllables (the OpenViIC 8-gram scan)
    refs = {"1": [ref] * 5, "2": ["con chó và con mèo"] * 5}
    s1 = ["phụ nữ ngồi xe máy",  # k 2, TP 2
          "phụ nữ ngồi ô tô",  # k 2, TP 1
          "đàn ông cạnh ô tô",  # k 2, TP 0
          "phụ nữ ngồi xe máy",  # duplicate
          "một chiếc xe máy", "một con chó",  # k 1, TP 1 and 0
          "", "phụ nữ 高", "phụ nữ ngồi trên", ref,  # empty, CJK, function-word end, copy
          "phụ nữ xe máy lạ lạ lạ lạ"]  # k 2, TP 2, 8 syllables: no partner within 2
    s2 = ["một con chó", "con chó nhỏ", "một con mèo", "một chiếc xe máy", "một cái bàn", "một chiếc ô tô"]  # 3 x 3

    def lex(c):
        return frozenset(objects_in(c))

    def sig(c):
        return len(lex(c)), lex(c), frozenset()

    gold = {i: frozenset().union(*map(lex, refs[i])) for i in refs}
    rows, rep = cm_pairs.build({"1": s1, "2": s2}, refs, {"1": "1.jpg", "2": "2.jpg"}, gold, sig, "cm")
    assert (rows, rep) == cm_pairs.build({"1": s1, "2": s2}, refs, {"1": "1.jpg", "2": "2.jpg"}, gold, sig, "cm")
    one = [(r["chosen"], r["rejected"]) for r in rows if r["image_id"] == "1"]
    assert one[0] == (s1[0], s1[2]) and set(one) == {(s1[0], s1[2]), (s1[0], s1[1]), (s1[1], s1[2]), (s1[4], s1[5])}, one
    assert rep["dropped_candidates"] == 4 and rep["pairs"] == 8 and rep["images"] == 2, rep
    assert sum(r["image_id"] == "2" for r in rows) == cm_pairs.CAP  # 9 candidate pairs, capped
    for r in rows:
        w, lo = lex(r["chosen"]), lex(r["rejected"])
        g = gold[r["image_id"]]
        assert len(w) == len(lo) >= 1 and len(w & g) >= len(lo & g) + 1 and r["pair_type"] == f"cm_k{len(w)}"
        assert abs(len(cm_pairs.syl(r["chosen"])) - len(cm_pairs.syl(r["rejected"]))) <= cm_pairs.MAX_DSYL
        assert r["ref"] == refs[r["image_id"]][0] and r["prompt"] == PROMPTS["short"] and "MODEL" in r["candidate_source"]


def _test_verdicts() -> None:
    """Prereg §8 on its boundaries; a guard failure is a KILL; no panel -> pending only when it could matter."""
    for arm in ("A", "AKL"):
        assert verdict(arm, 1.6, 0.1, -0.4, True) == "PASS" and verdict(arm, 1.5, 1e-9, -0.4999, True) == "PASS"
        assert verdict(arm, 1.5, 0.0, -0.4, True) == "GREY" and verdict(arm, 2.0, -0.3, -0.4, True) == "GREY"
        assert verdict(arm, 0.5, -1.0, -0.4, True) == "GREY" and verdict(arm, 0.49, -1.0, -0.4, True) == "KILL"
        assert verdict(arm, 1.6, 0.1, -0.5, True) == "KILL" and verdict(arm, 1.6, 0.1, -0.4, False) == "KILL"
        assert verdict(arm, 1.6, 0.1, None, True) == "PENDING_PANEL" and verdict(arm, 0.2, -1.0, None, True) == "KILL"
        assert verdict(arm, 1.6, 0.1, None, False) == "KILL"
    assert verdict("R", 1.0, 1e-9, -0.4, True) == "PASS" and verdict("R", 1.2, -0.1, -0.4, True) == "GREY"
    assert verdict("R", 0.3, -1.0, -0.4, True) == "GREY" and verdict("R", 0.29, -1.0, -0.4, True) == "KILL"
    assert verdict("R", 1.2, 0.2, -0.6, True) == "KILL" and verdict("R", 0.5, -1.0, None, True) == "PENDING_PANEL"
    assert s3_outcome("KILL", "PASS") == "PASS" and s3_outcome("GREY", "KILL") == "FAIL"
    assert s3_outcome("PENDING_PANEL", "KILL") == "PENDING_PANEL" and s3_outcome("PASS", "PENDING_PANEL") == "PASS"


def _test_h5() -> None:
    """Amendment 1: each clause alone, both, neither (holds / not shown), and the boundaries (a 0 never fires)."""
    def state(dp, dr):
        r = h5(dp, dr)
        return r["state"], r["clause1_dR_UB_lt_0"], r["clause2_dP_LB_gt_0_and_dR_lt_0"]

    assert state([0.5, -0.2, 1.2], [-0.8, -1.5, -0.1]) == ("KILL", True, False)  # clause 1 only
    assert state([1.0, 0.2, 1.8], [-0.3, -1.2, 0.6]) == ("KILL", False, True)  # clause 2 only
    assert state([1.0, 0.2, 1.8], [-0.8, -1.5, -0.1]) == ("KILL", True, True)
    assert state([0.8, -0.1, 1.7], [0.4, -0.5, 1.3]) == ("HOLDS", False, False)  # neither: holds
    assert state([0.3, -0.4, 1.0], [-0.2, -1.0, 0.6]) == ("NOT_SHOWN", False, False)  # neither: not shown
    assert state([0.2, -0.3, 0.7], [-0.5, -1.0, 0.0]) == ("NOT_SHOWN", False, False)  # dR_UB exactly 0
    assert state([0.5, 0.0, 1.0], [-0.2, -0.9, 0.5]) == ("NOT_SHOWN", False, False)  # dP_LB exactly 0
    assert state([0.9, 0.1, 1.7], [0.0, -0.6, 0.6]) == ("NOT_SHOWN", False, False)  # dR exactly 0
    assert not h5([1.0, 0.2, 1.8], [-0.8, -1.5, -0.1])["changes_verdict"]


def _synthetic(n: int = 120) -> tuple:
    """Dev-like images: odd ids name a woman, a motorbike and a road (P1_dev says car), even ids a dog and a cat."""
    refs = {str(i): ["phụ nữ với xe máy trên đường" if i % 2 else "con chó và con mèo"] * 5 for i in range(1, n + 1)}
    p1 = {i: "phụ nữ ngồi ô tô" if int(i) % 2 else "con chó nằm" for i in refs}
    better = {i: "phụ nữ ngồi xe máy" if int(i) % 2 and int(i) % 3 else c for i, c in p1.items()}
    more = {i: c + " trên đường" if int(i) % 2 else c for i, c in p1.items()}  # one more class on half the images
    panel = {i: _union(refs[i]) for i in list(refs)[:-4]}
    return refs, p1, better, more, panel


def _scored(syl: float = 11.9, frag: int = 9, copy_arm: float = 0.008, copy_p1: float = 0.004) -> dict:
    stats = {"n": N_DEV, "fw_end": 0.0, "fragments": frag, "syllables": syl}
    return {"caption_stats": {"p1dev": stats, "arm": stats}, "cider_x100_per_image_paired": [0.5, -2.0, 3.0],
            "exact_copy_first_250_rl_images": {"p1dev": {"rate": copy_p1}, "arm": {"rate": copy_arm}}}


def _test_estimators() -> None:
    """Verdicts from data: a fixed-count TP gain PASSES, a count rise or no change KILLs, no panel -> pending."""
    refs, p1, better, more, panel = _synthetic()
    gold = {i: _union(rs) for i, rs in refs.items()}
    ids = sorted(gold)
    rp = _rows(p1, gold, ids)
    s = summary(rp)  # by hand: TP 1 per image; |M| 2 (odd) and 1 (even); recall 1/3 (odd) and 1/2 (even)
    p, r = 100 * 120 / 180, 100 * (1 / 3 + 1 / 2) / 2
    tp_f = FRONTIER["TP1"] * (1.5 / FRONTIER["M1"]) ** FRONTIER["b"]
    p_f, r_f = 100 * tp_f / 1.5, FRONTIER["c0"] + FRONTIER["c1"] * tp_f
    assert abs(s["P"] - p) < 1e-9 and abs(s["R"] - r) < 1e-9 and s["m"] == 1.5, s
    assert abs(s["residual"] - (2 * p * r / (p + r) - 2 * p_f * r_f / (p_f + r_f))) < 1e-9, s
    assert paired(rp, rp, ("residual", "F1"))["F1"] == [0.0, 0.0, 0.0]
    cm = matched(rp, _rows(more, gold, ids))
    assert cm["n_matched"] == len(ids) // 2 and cm["matched_share"] == 0.5
    ok = {"preds": better, "CIDEr": 145.0, "BLEU-4": 42.0, "CHAIR_i": 0.2}
    base = {"preds": p1, "CIDEr": 144.3, "BLEU-4": 42.5, "CHAIR_i": 0.23}
    a = arm_block("A", ok, base, gold, panel, _scored())
    assert a["verdict"] == "PASS" and a["d_res"][1] > D_RES_LO and a["panel"]["panel_cm"]["dF1"][1] > PANEL_LO, a["d_res"]
    assert a["guards_hold"] and a["dm"][0] == 0 and a["h5"]["state"] == "HOLDS"
    assert arm_block("R", ok, base, gold, panel, _scored())["verdict"] == "PASS"
    k = arm_block("A", dict(ok, preds=more), base, gold, panel, _scored())
    assert k["verdict"] == "KILL" and not k["guards"]["G1"] and k["dm"][0] == 0.5
    assert arm_block("A", dict(ok, preds=p1), base, gold, panel, _scored())["verdict"] == "KILL"  # no gain
    assert arm_block("A", ok, base, gold, None, _scored())["verdict"] == "PENDING_PANEL"
    assert arm_block("A", dict(ok, preds=more), base, gold, None, _scored())["verdict"] == "KILL"
    for bad in (_scored(syl=10.6), _scored(frag=16), _scored(copy_arm=0.0081)):  # G4, G5, G6 just outside
        assert arm_block("A", ok, base, gold, panel, bad)["verdict"] == "KILL"
    assert arm_block("A", ok, base, gold, panel, _scored(syl=13.06, frag=15, copy_arm=0.008))["verdict"] == "PASS"
    cjk2 = dict(ok, preds=dict(better, **{ids[0]: "高", ids[1]: "한"}))  # 2 CJK captions: G3 fails, A-KL fires
    for dec in (cjk2, dict(ok, CIDEr=141.32)):
        assert akl_triggered(dec) and arm_block("A", dec, base, gold, panel, _scored())["verdict"] == "KILL"
    assert not akl_triggered(dict(ok, CIDEr=141.33))


def _result(preds: dict, cider: float) -> dict:
    """evaluate.py's result layout."""
    return {"split": "dev_data.json", "n_images": len(preds), "prompt_style": "short", "predictions": preds,
            "results": [{"tokenization": "word-level", "segmenter": "rdrsegmenter",
                         "scores_scaled_x100": {"CIDEr": cider, "BLEU-4": 42.0}}], "chair": {"CHAIR_i": 0.2}}


def _test_report() -> None:
    """--verdict end to end on synthetic files in OUT's layout, without and with the A-KL fallback."""
    refs, p1, better, _, panel = _synthetic()
    dev = sorted(refs)
    train = {"ordering_accuracy": 0.6, "ordering_accuracy_per_pair_type": {}, "pairs": 20, "optimizer_steps": 2,
             "regulariser": "anchor_sft", "coef": 1.0, "term_mean": 0.4, "resumed_from_step": [], "provenance": {}}
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        files = {f"{P1}-dev300-short.json": _result(p1, 144.3), "cmdpo_A_s42-dev300-short.json": _result(better, 145.0),
                 "cmrft_s42-dev300-short.json": _result(p1, 144.0), "score_A.json": _scored(), "score_R.json": _scored(),
                 "cm/A/_build_report.json": {"pairs": 20, "images": 9}, "cm/R/_rft_report.json": {"images": 1000,
                                                                                               "kept": 3, "rows": 6},
                 "runs/cmdpo_A_s42/train_summary.json": train, "runs/cmrft_s42/resume_manifest.json": {"resumed_from_step": []}}
        for name, obj in files.items():
            _write_once(out / name, _dump(obj))
        n2 = {"preds": dict(p1, **{dev[0]: "khác"}), "CIDEr": 144.334}
        rep = verdict_all(out, dev, refs, panel, n2)
        assert rep["outcome"] == "PASS" and rep["verdicts"] == {"A": "PASS", "R": "KILL"}, rep["verdicts"]
        assert rep["redecode_agreement"]["n_identical"] == len(dev) - 1 and not rep["A_and_A-KL"]["triggered"]
        assert rep["attribution"]["values"]["d_res(A) - d_res(R)"][0] > ATTRIBUTION_MIN
        (out / "cmdpo_A_s42-dev300-short.json").unlink()
        _write_once(out / "cmdpo_A_s42-dev300-short.json", _dump(_result(better, 140.0)))  # G2 fails: A-KL fires
        assert _raises(lambda: verdict_all(out, dev, refs, panel, n2), SystemExit), "A-KL fired without its decode"
        for name, obj in {"cmdpo_AKL_s42-dev300-short.json": _result(better, 145.0), "score_AKL.json": _scored(),
                          "runs/cmdpo_AKL_s42/train_summary.json": dict(train, regulariser="token_kl", coef=0.4)}.items():
            _write_once(out / name, _dump(obj))
        rep = verdict_all(out, dev, refs, panel, n2)
        both = rep["A_and_A-KL"]
        assert both["triggered"] and both["A_verdict"] == "KILL" and both["A_failed_guards"] == ["G2"]
        assert both["A-KL_verdict"] == "PASS" and rep["arm_A_counts_as"] == "AKL" and rep["outcome"] == "PASS"
        assert rep["deviations"][0]["commit"] == "59901cc" and rep["arms"]["A"]["panel"]["panel_cm"]["n_matched"] > 0


def selftest() -> None:
    _test_pairs()
    _test_verdicts()
    _test_h5()
    _test_estimators()
    _test_report()
    print("s3_gate selftest ok: pairs, verdict table, H5 (amendment 1), estimators, report")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--machine", action="store_true", help="--check on a GPU machine: weights and addendum pins too")
    ap.add_argument("--prep", metavar="OUT")
    ap.add_argument("--score", nargs=2, metavar=("OUT", "ARM"))
    ap.add_argument("--akl-trigger", metavar="OUT")
    ap.add_argument("--verdict", metavar="OUT")
    ap.add_argument("--out", help="--verdict: the report JSON (never overwritten)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
    elif a.check:
        print(_dump(check(a.machine)), end="")
    elif a.prep:
        prep(Path(a.prep))
    elif a.score:
        if a.score[1] not in RUNS:
            ap.error(f"ARM is one of {sorted(RUNS)}")
        print(_dump(score(Path(a.score[0]), a.score[1])), end="")
    elif a.akl_trigger:
        dec = load_decode(Path(a.akl_trigger) / f"{RUNS['A']}-dev300-short.json", dev_ids())
        print("yes" if akl_triggered(dec) else "no")
    elif a.verdict and a.out:
        from evaluate import references
        from rl_report import _preds

        dev = dev_ids()
        n2 = {"preds": _preds(str(N2) + ".preds.json"), "CIDEr": load_decode(Path(str(N2) + ".json"), dev)["CIDEr"]}
        rep = verdict_all(Path(a.verdict), dev, references("train_data.json"), load_panel(dev), n2)
        _write_once(Path(a.out), _dump(rep))
        print(_dump({k: rep[k] for k in ("outcome", "arm_A_counts_as", "verdicts", "A_and_A-KL")}), end="")
    else:
        ap.error("one of --check, --prep, --score, --akl-trigger, --verdict with --out, --selftest")
    return 0


if __name__ == "__main__":
    sys.exit(main())
