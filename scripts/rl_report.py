#!/usr/bin/env python
"""CPU reports for the CN-RLOO pilot (B1 sec. 3; judge decisions D1, D1b, D1e, D1f). Nothing here trains or decodes.

    # G0 (35_b): tau and the step-0 statistics of the k rollouts on the dev images and on SFT'd train images
    python scripts/rl_report.py --g0 g0/dev300.jsonl g0/train300.jsonl --out g0/g0_report.json
    # gate v2 (D1e; manuscript/prereg/2026-10-13_rl_gate_v2.md): the LAST checkpoint's evaluate.py dev result against
    # P1_dev's, plus the run's rollout log; --look 2 after the one extension
    python scripts/rl_report.py --gate RUN --p1dev p1dev-dev300-short.json --rl rl-dev300-short.json --g0-report g0.json
    # RL starts only from a sane baseline (D1b): exit 1 unless P1_dev's dev CIDEr-D (evaluate.py) >= 120
    python scripts/rl_report.py --floor p1dev-dev300-short.json
    # CN vs plain, symmetric: the copy mask is claimed only if CN - plain >= +3.0 with a paired 95% lower bound > 0
    python scripts/rl_report.py --compare CN_RUN/gate.json PLAIN_RUN/gate.json --out compare.json
    # fragment rate of prediction files (END from the references of train minus dev300)
    python scripts/rl_report.py --fragments p1dev-dev300-short.preds.json
    # anti-gaming: dev predictions scored against the dev images' UIT-OpenViIC captions (scoring only, never trained on)
    python scripts/rl_report.py --panel p1dev-dev300-short.json rl-dev300-short.json --out panel.json
    python scripts/rl_report.py --self-check      # verdict rules and the fragment probes; needs JAVA_HOME

Gate v2: delta = per-image word-level CIDEr-D of the run's last checkpoint minus P1_dev's on the 300 dev images (both
decoded by evaluate.py, bf16; recomputed here and checked against evaluate.py's corpus score), paired bootstrap B=2000.
  pass         delta >= +3.0, 95% lower bound > 0, and every guard holds.
  under-moved  not pass, every guard holding, and the final KL per caption (mean over the last 250-image block)
               < 0.2 nat: one CN rerun at lr 5e-5, judged by the same rule.
  grey         +1.0 <= delta < +3.0, or delta >= +3.0 with lower bound <= 0, every guard holding: one extension to all
               3,469 train-minus-dev images (train_rl.py --resume), judged once more with --look 2.
  kill         anything else (a guard failure is a kill at any KL), and anything but pass at look 2. "clean_kill"
               when the run moved (KL >= 0.2) and every guard held: then one CN fallback arm at the other temperature.
Guards: dev captions ending in a function word <= 1%; fragment captions <= P1_dev's + round(0.02 n), compared as
integer counts (+6 of 300, judge D1f); mean syllables >= 0.9x P1_dev's; exact-copy rate of the rollouts in the last
250 images <= 2x the step-0 rate (G0; for an arm sampled at another temperature, its own first 250 images, since G0
sampled at T = 1.0). Mentions per caption and CHAIR_i are reported, never gated. The run's in-run 4-bit dev scores are
monitoring only and select nothing.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

from rl_reward import ROOT, SPLIT, CiderD, Reward, Segmenter, boot, function_end, rloo, syllables

GATE_GAIN, GREY_FLOOR, GATE_FW_END, FRAG_MARGIN, LEN_RATIO, CLAIM_MARGIN = 3.0, 1.0, 0.01, 0.02, 0.9, 3.0  # D1e, D1f
SKIP_35D_SHARE = 0.05  # D1: G0 measured 0.111 on the SFT'd train images, so the plain arm is never skipped
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


def _dev_reward(dev_ids) -> Reward:
    """Train references segmented as evaluate.py does, END from the references of train minus the dev images."""
    from evaluate import references

    refs = references(SPLIT)
    return Reward(refs, Segmenter(), end_from=set(refs) - set(dev_ids))


def dev_scores(result: str, reward: Reward) -> tuple[list[str], dict, np.ndarray]:
    """(dev ids, predictions, per-image word-level CIDEr-D x100) of an evaluate.py dev result, recomputed as
    evaluate.py scores (pycocoevalcap, df from these images' references) and checked against its corpus CIDEr."""
    from pycocoevalcap.cider.cider import Cider

    preds = _preds(result)
    ids = sorted(preds)
    seg = reward.seg([preds[i] for i in ids])
    per = 100 * np.asarray(Cider().compute_score({i: [" ".join(r) for r in reward.refs[i]] for i in ids},
                                                 {i: [x] for i, x in zip(ids, seg)})[1])
    assert abs(per.mean() - _cider(result)) < 1e-6, (result, per.mean(), _cider(result))
    return ids, preds, per


def caption_stats(preds: dict, reward: Reward) -> dict:
    caps = list(preds.values())
    return {"n": len(caps), "fw_end": float(np.mean([function_end(c) for c in caps])),
            "fragments": int(sum(reward.fragment(x.split()) for x in reward.seg(caps))),
            "syllables": float(np.mean([len(syllables(c)) for c in caps]))}


def fragments_ok(rl: int, p1dev: int, n: int) -> bool:
    """Judge D1f: the run's fragment captions <= P1_dev's + round(0.02 n) (+6 of 300), as integer counts."""
    return rl <= p1dev + round(FRAG_MARGIN * n)


def verdict(gain: float, lower: float, guards_ok: bool, kl_final: float, look: int) -> str:
    """The pre-registered decision of gate v2 (judges D1e, D1f), in this order."""
    if gain >= GATE_GAIN and lower > 0 and guards_ok:
        return "pass"
    if look == 2:
        return "kill"
    if kl_final < UNDER_MOVED_KL and guards_ok:  # D1f: a guard failure is a kill at any KL
        return "under-moved"
    if guards_ok and (GREY_FLOOR <= gain < GATE_GAIN or (gain >= GATE_GAIN and lower <= 0)):
        return "grey"
    return "kill"


def gate(run: Path, p1dev: str, rl: str, g0: str, look: int = 1, block: int = 250) -> dict:
    """Gate v2 on the last checkpoint of one RL run (judge D1e); writes RUN/gate.json."""
    reward = _dev_reward(_preds(p1dev))
    ids, p1, p1_per = dev_scores(p1dev, reward)
    ids_rl, r1, rl_per = dev_scores(rl, reward)
    assert ids == ids_rl, "P1_dev and the RL run were scored on different images"
    gain = boot(rl_per - p1_per)
    log = _jsonl(run / "log.jsonl")
    steps, evals = [r for r in log if "step" in r], [r for r in log if "eval" in r]
    blocks: dict[int, list[int]] = {}
    for r in steps:
        b = blocks.setdefault((r["images"] - 1) // block, [0, 0])
        b[0], b[1] = b[0] + r["exact_copies"], b[1] + r["rollouts"]
    trajectory = [x / n for x, n in (blocks[b] for b in sorted(blocks))]
    kl_final = float(np.mean([r["kl_caption"] for r in steps if (r["images"] - 1) // block == max(blocks)]))
    temperature = json.loads((run / "summary.json").read_text(encoding="utf-8"))["args"]["temperature"]
    if temperature == 1.0:
        t0 = json.loads(Path(g0).read_text(encoding="utf-8"))["train"]
        step0 = max(t0["copy_rate"]["exact"], 1 / (t0["n_images"] * t0["k"]))  # at least one copy, so 2x is not 0
    else:  # G0 sampled at T = 1.0, so a tempered arm's own first block stands in for its step 0
        step0 = max(trajectory[0], 1 / blocks[min(blocks)][1])
    sp, sr = caption_stats(p1, reward), caption_stats(r1, reward)
    guards = {f"fw_end_le_{GATE_FW_END}": sr["fw_end"] <= GATE_FW_END,
              "fragments_le_p1dev_plus_2pt_counts": fragments_ok(sr["fragments"], sp["fragments"], sp["n"]),
              f"syllables_ge_{LEN_RATIO}x_p1dev": sr["syllables"] >= LEN_RATIO * sp["syllables"],
              "exact_copy_last_block_le_2x_step0": trajectory[-1] <= 2 * step0}
    ok = all(guards.values())
    v = verdict(gain[0], gain[1], ok, kl_final, look)
    chair = {k: json.loads(Path(p).read_text(encoding="utf-8"))["chair"] for k, p in (("p1dev", p1dev), ("rl", rl))}
    out = {"look": look, "verdict": v, "clean_kill": v == "kill" and ok and kl_final >= UNDER_MOVED_KL,
           "dev_gain_x100_mean_lo_hi": gain, "dev_cider_evaluate_py": {"p1dev": _cider(p1dev), "rl": _cider(rl)},
           "guards": guards, "caption_stats": {"p1dev": sp, "rl": sr},
           "mentions_per_caption": {k: c["mentions_per_caption"] for k, c in chair.items()},
           "chair_i": {k: c["CHAIR_i"] for k, c in chair.items()},
           "exact_copy_trajectory_per_block": trajectory, "exact_copy_step0": step0,
           "exact_copy_step0_source": "G0" if temperature == 1.0 else f"first {block} images at T = {temperature}",
           "kl_caption_final": kl_final, "kl_caption_last_step": steps[-1]["kl_caption"],
           "in_run_dev_cider_monitoring_only": [[e["eval"], e["cider"]] for e in evals],
           "dev_ids": ids, "per_image_cider_x100": rl_per.tolist(),
           "rule": "gate v2, judge D1e; manuscript/prereg/2026-10-13_rl_gate_v2.md"}
    (run / "gate.json").write_text(json.dumps(out, indent=1, default=float), encoding="utf-8")
    return out


def c3_verdict(out: Path, c3: dict, summary: dict, groups: int) -> int:
    """Judge D1 C3 on train_rl.py --dry-run: writes OUT/c3.json; non-zero unless every guard holds."""
    c3.update({"mask_groups_checked": groups, "peak_reserved_gb": summary["peak_reserved_gb"],
               "sec_per_image": summary["sec_per_image"], "kl_caption_last": summary["kl_caption_last"]})
    c3["checks"] = {f"logp_gap_mean_lt_{LOGP_GAP}": bool(c3["logp_gap_mean_max"][0] < LOGP_GAP),
                    "sampler_is_the_policy": bool(c3["sampler_gap"] < SAMPLER_TOL),
                    f"reward_replica_le_{REPLICA_TOL}": bool(c3["reward_replica_max_abs_diff"] <= REPLICA_TOL),
                    "loss_mask_generated_tokens_only": groups > 0,  # rl_policy.guard_mask asserted on every group
                    f"peak_memory_le_{MEM_GB}gb": bool(c3["peak_reserved_gb"] <= MEM_GB)}
    c3["pass"] = all(c3["checks"].values())
    (out / "c3.json").write_text(json.dumps(c3, indent=1, default=float), encoding="utf-8")
    print(json.dumps(c3, indent=1, default=float), flush=True)
    return 0 if c3["pass"] else 1


def compare(cn: str, plain: str) -> dict:
    """CN vs plain RLOO on the same dev images, symmetric (judge D1e): the copy mask is claimed only if CN - plain >=
    +3.0 with a paired 95% lower bound > 0; the copy-rate trajectories are reported side by side."""
    a, b = (json.loads(Path(p).read_text(encoding="utf-8")) for p in (cn, plain))
    assert a["dev_ids"] == b["dev_ids"], "CN and plain were scored on different dev images"
    diff = boot(np.asarray(a["per_image_cider_x100"]) - np.asarray(b["per_image_cider_x100"]))
    return {"cn_minus_plain_x100_mean_lo_hi": diff,
            "dev_cider_evaluate_py": {"cn": a["dev_cider_evaluate_py"]["rl"],
                                      "plain": b["dev_cider_evaluate_py"]["rl"]},
            "verdict": {"cn": a["verdict"], "plain": b["verdict"]},
            "exact_copy_trajectory": {"cn": a["exact_copy_trajectory_per_block"],
                                      "plain": b["exact_copy_trajectory_per_block"]},
            "claim_copy_mask": bool(diff[0] >= CLAIM_MARGIN and diff[1] > 0),
            "rule": f"the copy mask is claimed only if CN - plain >= +{CLAIM_MARGIN} with a paired 95% lower bound > 0"}


def fragments(paths: list[str]) -> dict:
    """Share of captions whose last word ends no reference of train minus dev300, per prediction file (judge D1e)."""
    reward = _dev_reward((ROOT / "data" / "splits" / "ktvic_dev300.txt").read_text(encoding="utf-8").split())
    out = {"end_words": len(reward.end)}
    for p in paths:
        caps = list(_preds(p).values())
        out[Path(p).name] = {"n": len(caps),
                             "fragment_rate": float(np.mean([reward.fragment(x.split()) for x in reward.seg(caps)]))}
    return out


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


def _check() -> None:
    """Gate v2's decision table (D1f: a guard failure is a kill at any KL), the fragment-count boundary, and the
    fragment guard on the judge's probe with the real segmenter and END."""
    assert verdict(3.5, 0.4, True, 0.5, 1) == "pass" and verdict(3.5, 0.4, True, 0.1, 1) == "pass"
    assert verdict(3.5, -0.2, True, 0.5, 1) == "grey" and verdict(1.0, -4.0, True, 0.5, 1) == "grey"
    assert verdict(0.99, -4.0, True, 0.5, 1) == "kill" and verdict(-2.0, -8.0, True, 0.5, 1) == "kill"
    assert verdict(3.5, 0.4, False, 0.5, 1) == "kill" and verdict(2.0, -1.0, False, 0.5, 1) == "kill"
    assert verdict(2.0, -1.0, True, 0.19, 1) == "under-moved" and verdict(-2.0, -8.0, True, 0.1, 1) == "under-moved"
    assert verdict(-2.0, -8.0, False, 0.1, 1) == "kill" and verdict(2.0, -1.0, False, 0.19, 1) == "kill"  # D1f
    assert fragments_ok(15, 9, 300) and not fragments_ok(16, 9, 300) and fragments_ok(9, 9, 300)  # D1f: +6 of 300
    assert verdict(2.0, -1.0, True, 0.5, 2) == "kill" and verdict(2.0, -1.0, True, 0.1, 2) == "kill"
    assert verdict(3.5, 0.4, True, 0.5, 2) == "pass"
    reward = _dev_reward((ROOT / "data" / "splits" / "ktvic_dev300.txt").read_text(encoding="utf-8").split())
    probes = reward.seg(["một người đang cầm điện thoại di", "một người đang cầm điện thoại di động"])
    assert [reward.fragment(x.split()) for x in probes] == [True, False], probes
    print(f"rl_report self-check ok ({len(reward.end)} END words)")


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
    ap.add_argument("--look", type=int, choices=(1, 2), default=1, help="gate: 2 after the one extension")
    ap.add_argument("--fragments", nargs="+", metavar="PREDS")
    ap.add_argument("--self-check", action="store_true")
    ap.add_argument("--out")
    args = ap.parse_args()
    if args.self_check:
        _check()
        return 0
    if args.g0:
        out = g0_report(*args.g0)
    elif args.gate:
        out = gate(Path(args.gate), args.p1dev, args.rl, args.g0_report, args.look)
    elif args.compare:
        out = compare(*args.compare)
    elif args.panel:
        out = panel(args.panel)
    elif args.floor:
        out = floor(args.floor)
    elif args.fragments:
        out = fragments(args.fragments)
    else:
        ap.error("one of --g0, --gate, --compare, --panel, --floor, --fragments, --self-check")
    text = json.dumps(out, ensure_ascii=False, indent=1, default=float)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    print(text)
    return 1 if args.floor and not out["pass"] else 0


if __name__ == "__main__":
    sys.exit(main())
