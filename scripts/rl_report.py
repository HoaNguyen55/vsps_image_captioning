#!/usr/bin/env python
"""CPU reports for the CN-RLOO pilot (B1 sec. 3, judge D1's conditions). Nothing here trains or decodes.

    # G0 (35_b): tau and the step-0 statistics of the k rollouts on the dev images and on SFT'd train images
    python scripts/rl_report.py --g0 g0/dev300.jsonl g0/train300.jsonl --out g0/g0_report.json
    # G1 gate (judge C2): evaluate.py dev scores of P1_dev and of the RL adapter, plus the run's rollout log
    python scripts/rl_report.py --gate RUN --p1dev p1dev-dev300-short.json --rl rl-dev300-short.json --g0 g0_report.json
    # RL starts only from a sane baseline (judge D1b): exit 1 unless P1_dev's dev CIDEr-D (evaluate.py) >= 120
    python scripts/rl_report.py --floor p1dev-dev300-short.json
    # CN vs plain (judge C2): keep CN unless plain beats it by >= 3 dev CIDEr-D
    python scripts/rl_report.py --compare CN_RUN/gate.json PLAIN_RUN/gate.json --out compare.json
    # anti-gaming: dev predictions scored against the dev images' UIT-OpenViIC captions (scoring only, never trained on)
    python scripts/rl_report.py --panel p1dev-dev300-short.json rl-dev300-short.json --out panel.json

Gate (judge C2, point estimates; the CI test is left to the final 3-seed comparison): dev CIDEr-D (evaluate.py) of the
RL adapter >= P1_dev + 2.0; exact-copy rate of the rollouts on SFT'd images over the last 250 images <= 2x the step-0
rate (G0's train file); share of dev captions ending in a function word <= 1%. 35_d is skipped when copies at tau
take < 5% of the positive RLOO advantage on the SFT'd train images (G0's `skip_35d`): the mask would then be moot.
Pre-registered (judge D1b): a failed gate whose final KL per caption (mean over the last 250-image block) is below
0.2 nat is "under-moved", not "RL failed", and gets exactly one CN rerun at lr 5e-5 before any conclusion.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

from rl_reward import ROOT, SPLIT, CiderD, Reward, Segmenter, boot, function_end, rloo, syllables

GATE_DEV_GAIN, GATE_FW_END, KEEP_PLAIN_MARGIN, SKIP_35D_SHARE = 2.0, 0.01, 3.0, 0.05
LOGP_GAP, SAMPLER_TOL, REPLICA_TOL, MEM_GB = 0.02, 1e-5, 1e-6, 22.0  # judge D1, C3
UNDER_MOVED_KL, RERUN_LR, P1DEV_FLOOR = 0.2, 5e-5, 120.0  # judge D1b, pre-registered


def _ci(x) -> str:
    m, lo, hi = (100 * v for v in boot(x))
    return f"{m:+.1f} [{lo:+.1f}, {hi:+.1f}]"


def _jsonl(path) -> list[dict]:
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def _set_scores(toks: dict, refs: dict, idx: tuple) -> np.ndarray:
    """Plain CIDEr-D (no end token; df from these images' references idx, as pycocoevalcap) of every candidate."""
    ids = list(toks)
    c = CiderD([[refs[i][t] for t in idx] for i in ids])
    return np.array([[c.score(t, [refs[i][j] for j in idx]) for t in toks[i]] for i in ids])


def summarise(rows: list[dict], scored: list[tuple], tau: float, reward: Reward) -> dict:
    """What RL sees at step 0 on one rollout file (x100 where CIDEr-D)."""
    R, M, D = (np.array([s[j][:-1] for s in scored]) for j in range(3))
    G = np.array([s[0][-1] for s in scored])
    sd = R.std(1)
    adv = np.array([rloo(r, np.zeros(len(r), bool)) for r in R])
    pos = np.clip(adv, 0, None)
    copies = {"exact": D == 0, "near_le1_word_edit": D <= 1, "at_tau": M >= tau}
    samples = [c for r in rows for c in r["samples"]]
    toks = {r["image_id"]: [s.split() for s in reward.seg(r["samples"] + [r["greedy"]])] for r in rows
            if len(reward.refs[r["image_id"]]) >= 5}
    full = _set_scores(toks, reward.refs, (0, 1, 2, 3, 4))
    out = {"n_images": len(rows), "k": R.shape[1], "reward_x100": 100 * R.mean(), "greedy_reward_x100": 100 * G.mean(),
           "within_sd_x100_mean_median": [100 * sd.mean(), 100 * np.median(sd)],
           "between_image_share": R.mean(1).var() / (R.mean(1).var() + R.var(1).mean()),
           "frac_groups_sd_lt_5": (sd < 0.05).mean(), "frac_samples_beat_greedy": (R > G[:, None]).mean(),
           "distinct_per_group": np.mean([len(set(r["samples"])) for r in rows]),
           "finished_rate": np.mean([f for r in rows for f in r["finished"]]),
           "syllables": np.mean([len(syllables(c)) for c in samples]),
           "fw_end": {"samples": np.mean([function_end(c) for c in samples]),
                      "greedy": np.mean([function_end(r["greedy"]) for r in rows])},
           "m_percentiles": {p: np.percentile(M, p) for p in (50, 90, 95, 99)},
           "copy_rate": {k: v.mean() for k, v in copies.items()},
           "copy_share_of_positive_rloo_advantage": {k: pos[v].sum() / pos.sum() for k, v in copies.items()},
           "mean_rloo_adv_x100_copies_at_tau": 100 * adv[copies["at_tau"]].mean() if copies["at_tau"].any() else None,
           "mean_rloo_adv_x100_others": 100 * adv[~copies["at_tau"]].mean(),
           "greedy_cider_x100": 100 * full[:, -1].mean(),
           "oracle_best_of_k_minus_greedy_same_refs": _ci(full[:, :-1].max(1) - full[:, -1])}
    for name, (a, b) in {"A012_B34": ((0, 1, 2), (3, 4)), "A234_B01": ((2, 3, 4), (0, 1))}.items():
        sa, sb = _set_scores(toks, reward.refs, a), _set_scores(toks, reward.refs, b)
        pick = sa[:, :-1].argmax(1)
        out[f"best_of_k_{name}_minus_greedy"] = _ci(sb[np.arange(len(sb)), pick] - sb[:, -1])
    return out


def g0_report(dev: str, train: str, pct: float = 99.0) -> dict:
    """tau (the pct-th percentile of m over the dev rollouts) and the step-0 statistics of each rollout file."""
    from evaluate import references

    reward = Reward(references(SPLIT), Segmenter())
    rows = {"dev": _jsonl(dev), "train": _jsonl(train)}
    scored = {name: [reward(r["image_id"], r["samples"] + [r["greedy"]], r["finished"] + [r["greedy_finished"]])
                     for r in rs] for name, rs in rows.items()}
    tau = float(np.percentile([m for s in scored["dev"] for m in s[1][:-1]], pct))
    out = {"tau": tau, "tau_rule": f"{pct:g}th percentile of m over the k rollouts on the dev images",
           **{name: summarise(rows[name], scored[name], tau, reward) for name in rows}}
    share = out["train"]["copy_share_of_positive_rloo_advantage"]["at_tau"]
    out["skip_35d"] = bool(share < SKIP_35D_SHARE)
    out["skip_35d_rule"] = (f"copies at tau take {share:.3f} of the positive RLOO advantage on the SFT'd train images; "
                            f"35_d (plain RLOO) is skipped below {SKIP_35D_SHARE}")
    return out


def _cider(result: str) -> float:
    rows = json.loads(Path(result).read_text(encoding="utf-8"))["results"]
    return next(r for r in rows if r["tokenization"] == "word-level")["scores_scaled_x100"]["CIDEr"]


def _preds(path: str) -> dict[str, str]:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    d = d.get("predictions", d)
    return {str(k): v[0] if isinstance(v, list) else v for k, v in d.items()}


def gate(run: Path, p1dev: str, rl: str, g0: str, block: int = 250) -> dict:
    """Judge C2 on one G1 arm, with D1b's pre-registered verdict; writes RUN/gate.json."""
    log = _jsonl(run / "log.jsonl")
    steps, evals = [r for r in log if "step" in r], [r for r in log if "eval" in r]
    blocks: dict[int, list[int]] = {}
    for r in steps:
        b = blocks.setdefault((r["images"] - 1) // block, [0, 0])
        b[0], b[1] = b[0] + r["exact_copies"], b[1] + r["rollouts"]
    trajectory = [x / n for x, n in (blocks[b] for b in sorted(blocks))]
    t0 = json.loads(Path(g0).read_text(encoding="utf-8"))["train"]
    step0 = max(t0["copy_rate"]["exact"], 1 / (t0["n_images"] * t0["k"]))  # at least one copy, so 2x is not 0
    fw = float(np.mean([function_end(c) for c in _preds(rl).values()]))
    dev = {"p1dev": _cider(p1dev), "rl": _cider(rl)}
    out = {"dev_cider_evaluate_py": dev, "dev_gain": dev["rl"] - dev["p1dev"],
           "exact_copy_trajectory_per_block": trajectory, "exact_copy_step0_g0": step0, "fw_end_dev": fw,
           "checks": {f"dev_gain_ge_{GATE_DEV_GAIN}": dev["rl"] - dev["p1dev"] >= GATE_DEV_GAIN,
                      "exact_copy_last_block_le_2x_step0": trajectory[-1] <= 2 * step0,
                      f"fw_end_dev_le_{GATE_FW_END}": fw <= GATE_FW_END},
           "in_run_dev_cider": {"step0": evals[0]["cider"], "best": max(e["cider"] for e in evals),
                                "last": evals[-1]["cider"], "last_at_images": evals[-1]["eval"]},
           "kl_caption_final": {"last_block_mean": float(np.mean([r["kl_caption"] for r in steps
                                                                  if (r["images"] - 1) // block == max(blocks)])),
                                "last_step": steps[-1]["kl_caption"]},
           "in_run_summary": json.loads((run / "summary.json").read_text(encoding="utf-8"))}
    out["pass"] = all(out["checks"].values())
    moved = out["kl_caption_final"]["last_block_mean"] >= UNDER_MOVED_KL
    out["verdict"] = "pass" if out["pass"] else "RL failed" if moved else "under-moved"
    out["verdict_rule"] = (f"pre-registered (judge D1b): a failed gate with the final KL per caption (mean over the "
                           f"last {block}-image block) < {UNDER_MOVED_KL} nat is 'under-moved', not 'RL failed', and "
                           f"gets exactly one CN rerun at lr {RERUN_LR} (same seed, images, beta, tau) before any "
                           f"conclusion")
    (run / "gate.json").write_text(json.dumps(out, indent=1, default=float), encoding="utf-8")
    return out


def c3_verdict(out: Path, c3: dict, summary: dict, groups: int) -> int:
    """Judge D1 C3 on train_rl.py --dry-run: writes OUT/c3.json; non-zero unless every guard holds."""
    c3.update({"mask_groups_checked": groups, "peak_reserved_gb": summary["peak_reserved_gb"],
               "sec_per_image": summary["sec_per_image"], "kl_caption_last": summary["kl_caption_last"]})
    c3["checks"] = {f"logp_gap_mean_lt_{LOGP_GAP}": c3["logp_gap_mean_max"][0] < LOGP_GAP,
                    "sampler_is_the_policy": c3["sampler_gap"] < SAMPLER_TOL,
                    f"reward_replica_le_{REPLICA_TOL}": c3["reward_replica_max_abs_diff"] <= REPLICA_TOL,
                    "loss_mask_generated_tokens_only": groups > 0,  # train_rl.guard_mask asserted on every group
                    f"peak_memory_le_{MEM_GB}gb": c3["peak_reserved_gb"] <= MEM_GB}
    c3["pass"] = all(c3["checks"].values())
    (out / "c3.json").write_text(json.dumps(c3, indent=1, default=float), encoding="utf-8")
    print(json.dumps(c3, indent=1, default=float), flush=True)
    return 0 if c3["pass"] else 1


def compare(cn: str, plain: str) -> dict:
    """Judge C2: CN vs plain by the copy-rate trajectory; keep CN unless plain beats it by >= 3 dev CIDEr-D."""
    a, b = (json.loads(Path(p).read_text(encoding="utf-8")) for p in (cn, plain))
    diff = b["dev_cider_evaluate_py"]["rl"] - a["dev_cider_evaluate_py"]["rl"]
    return {"dev_cider": {"cn": a["dev_cider_evaluate_py"]["rl"], "plain": b["dev_cider_evaluate_py"]["rl"]},
            "plain_minus_cn": diff, "exact_copy_trajectory": {"cn": a["exact_copy_trajectory_per_block"],
                                                               "plain": b["exact_copy_trajectory_per_block"]},
            "verdict": {"cn": a["verdict"], "plain": b["verdict"]},
            "keep": "plain" if diff >= KEEP_PLAIN_MARGIN else "cn",
            "rule": f"keep CN unless plain beats it by >= {KEEP_PLAIN_MARGIN} dev CIDEr-D (evaluate.py)"}


def floor(result: str) -> dict:
    """Judge D1b: no RL from a broken baseline; P1_dev's dev CIDEr-D (evaluate.py) must reach the floor."""
    c = _cider(result)
    return {"p1dev_dev_cider_evaluate_py": c, "floor": P1DEV_FLOOR, "pass": c >= P1DEV_FLOOR}


def panel(paths: list[str]) -> dict:
    """Word-level CIDEr-D of each prediction file against the UIT-OpenViIC captions of the same KTVIC train images
    (data/ktvic_openviic_refs.json, git-excluded: read here, never copied), paired deltas vs the first file."""
    from pycocoevalcap.cider.cider import Cider

    second = json.loads((ROOT / "data" / "ktvic_openviic_refs.json").read_text(encoding="utf-8"))["train"]
    preds = [_preds(p) for p in paths]
    ids = sorted(set.intersection(*(set(p) for p in preds)) & {i for i, c in second.items() if c})
    seg = Segmenter()
    gts = {i: seg(second[i]) for i in ids}
    per = [np.asarray(Cider().compute_score(gts, {i: [s] for i, s in zip(ids, seg([p[i] for i in ids]))})[1])
           for p in preds]
    return {"n_images": len(ids), "panel": "UIT-OpenViIC captions of the dev images (scoring only)",
            "cider_x100": {Path(p).name: 100 * x.mean() for p, x in zip(paths, per)},
            "delta_vs_first_x100": {Path(p).name: _ci(x - per[0]) for p, x in zip(paths[1:], per[1:])}}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--g0", nargs=2, metavar=("DEV_JSONL", "TRAIN_JSONL"))
    ap.add_argument("--gate", metavar="RUN")
    ap.add_argument("--p1dev")
    ap.add_argument("--rl")
    ap.add_argument("--g0-report")
    ap.add_argument("--compare", nargs=2, metavar=("CN_GATE", "PLAIN_GATE"))
    ap.add_argument("--panel", nargs="+", metavar="PREDS")
    ap.add_argument("--floor", metavar="P1DEV_RESULT", help="exit 1 unless its dev CIDEr-D >= the floor")
    ap.add_argument("--out")
    args = ap.parse_args()
    if args.g0:
        out = g0_report(*args.g0)
    elif args.gate:
        out = gate(Path(args.gate), args.p1dev, args.rl, args.g0_report)
    elif args.compare:
        out = compare(*args.compare)
    elif args.panel:
        out = panel(args.panel)
    elif args.floor:
        out = floor(args.floor)
    else:
        ap.error("one of --g0, --gate, --compare, --panel, --floor")
    text = json.dumps(out, ensure_ascii=False, indent=1, default=float)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    print(text)
    return 1 if args.floor and not out["pass"] else 0


if __name__ == "__main__":
    sys.exit(main())
