#!/usr/bin/env python3
"""G-RL pilot trainer: base sampling, the length anchors, the RFT pick, and one training loop for the three arms
(grl = on-policy RLOO on the gold reward; sftref = SFT on the UIT-ViIC references; rft = SFT on the base model's
best-of-k samples). Rule: manuscript/prereg/2026-10-27_grl_pilot/PILOT_RULE.md §3-§5.

    python3 scripts/grl/train.py --selftest                                        CPU, no model, synthetic rows
    python3 scripts/grl/train.py sample  --size 7b --out S.jsonl [--limit N]       GPU: k base samples per UT image
    python3 scripts/grl/train.py anchors --samples S.jsonl --out A.json            CPU
    python3 scripts/grl/train.py rft-pick --samples S.jsonl --anchors A.json --out P.jsonl     CPU
    python3 scripts/grl/train.py train --arm grl|sftref|rft --size 7b --out DIR --anchors A.json [--picks P.jsonl]
                                       [--max-steps N] [--dry-run] [--budget-hours H]                     GPU

Every arm: the same 4-bit NF4 base (train_stage2.build_model), the same fresh LoRA (seed 0, r 16, alpha 32,
language tower only, dropout 0), the same detailed prompt, the KL anchor = the base model (adapter disabled).
Policy primitives are rl_policy.py's, unchanged (rollout, prompt_pass, response_logprobs, pg_loss, guard_mask); the
G-RL update is train_rl.update with the base as the reference and the reference pass chunked like the policy pass.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent), str(HERE.parents[1])]
import common as K  # noqa: E402
import reward as RW  # noqa: E402
from rl_reward import rloo, syllables  # noqa: E402

C = K.CFG


def schedule(pool: list[str], n: int, seed: int) -> list[str]:
    """train_rl.schedule (seeded reshuffles of the sorted pool), copied so this file imports without torch."""
    import random

    rng, order = random.Random(seed), []
    while len(order) < n:
        epoch = sorted(pool)
        rng.shuffle(epoch)
        order += epoch
    return order[:n]


def names() -> dict[str, str]:
    """{image id: absolute image path} for the staged UT-2402 and val-924 images. rl_policy.image joins KTVIC/images
    with this value; an absolute right-hand path replaces the left side (pathlib), so the staged file is opened."""
    out = {}
    for split in ("train_data.json", "val_data.json"):
        for im in json.loads((K.UV / split).read_text(encoding="utf-8"))["images"]:
            out[str(im["id"])] = str(K.UV / "images" / im["file_name"])
    want = {str(i) for i in K.ids("ut2402") + K.ids("val924")}
    if set(out) != want:
        raise SystemExit("REFUSED: the staged UIT-ViIC files are not exactly UT-2402 + val-924")
    return out


def references() -> dict[str, list[str]]:
    """UT-2402 references (SFT-ref targets), read at run time from the staged train file only."""
    refs: dict[str, list[str]] = {}
    for a in json.loads((K.UV / "train_data.json").read_text(encoding="utf-8"))["annotations"]:
        refs.setdefault(str(a["image_id"]), []).append(a["caption"])
    return refs


# ------------------------------------------------------------------------------------------------ GPU side
def check_revision(hub: str, rev: str) -> None:
    """from_pretrained(hub) offline must resolve to the pinned revision (refs/main), as setup_gpu.sh records."""
    from huggingface_hub import constants

    ref = Path(constants.HF_HUB_CACHE) / f"models--{hub.replace('/', '--')}" / "refs" / "main"
    if not ref.is_file() or ref.read_text().strip() != rev:
        raise SystemExit(f"REFUSED: {hub} refs/main is not {rev[:8]} (download the pinned revision first)")


def load(size: str):
    """(Policy, model) with a fresh LoRA; the base is reached with model.disable_adapter()."""
    from transformers import set_seed

    from evaluate import PROMPTS
    from rl_policy import Policy
    from train_rl import configure
    from train_stage2 import build_model

    hub, rev, _, _ = K.MODELS[size]
    check_revision(hub, rev)
    set_seed(C["seed"])  # identical LoRA init in every arm
    model, proc = build_model(argparse.Namespace(vision_tokens=C["vision_tokens"], force_4bit=True, stage="grl",
                                                 base_model=hub, adapter=None, lora_r=C["lora_r"],
                                                 lora_alpha=C["lora_alpha"]))
    configure(model)
    proc.tokenizer.padding_side = "left"
    msg = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": PROMPTS[K.PROMPT_MODE]}]}]
    e = model.generation_config.eos_token_id
    return Policy(model, proc, proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True), names(),
                  [e] if isinstance(e, int) else list(e))


def peak_gb() -> float:
    import torch

    return torch.cuda.max_memory_reserved() / 1e9


def cmd_sample(a) -> int:
    """k samples per UT image from the base (adapter disabled), seed 0 schedule order."""
    from transformers import set_seed

    from rl_policy import rollout

    pol = load(a.size)
    order = schedule([str(i) for i in K.ids("ut2402")], K.N_TRAIN, C["seed"])[:a.limit or None]
    set_seed(C["seed"])
    out, t0 = Path(a.out), time.time()
    with out.open("w", encoding="utf-8") as fh, pol.model.disable_adapter():
        for n, i in enumerate(order, 1):
            if a.budget_hours and (time.time() - t0) / 3600 > a.budget_hours:
                print(f"cap: {a.budget_hours} GPU-h spent after {n - 1} images", flush=True)
                return 3
            _, _, ntok, done, texts, _, _ = rollout(pol, i, C["k"], C["max_new_tokens"], temperature=C["temperature"])
            fh.write(json.dumps({"image_id": i, "samples": texts, "finished": done.tolist(),
                                 "n_tokens": ntok.tolist()}, ensure_ascii=False) + "\n")
            if n % 25 == 0 or n == len(order):
                print(f"  [{n}/{len(order)}] {(time.time() - t0) / n:.2f}s/image", flush=True)
    fin = [d for r in map(json.loads, out.read_text(encoding="utf-8").splitlines()) for d in r["finished"]]
    summary = {"stage": "sample", "size": a.size, "images": len(order), "sec_per_image": (time.time() - t0) / len(order),
               "hours": (time.time() - t0) / 3600, "peak_reserved_gb": peak_gb(), "finished_share": float(np.mean(fin))}
    Path(a.out + ".summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    print(json.dumps(summary))
    return 0


def grl_update(pol, opt, params, groups: list[dict], first: bool) -> dict:
    """train_rl.update with the base model as the reference: one optimizer step over the step's rollouts, policy and
    reference log-probs both --micro responses at a time (the reference prompt runs once per image, no grad)."""
    import torch

    from rl_policy import CLIP, guard_mask, pg_loss, prompt_pass, response_logprobs

    model, micro, t = pol.model, C["micro"], C["temperature"]
    denom, kl = float(sum(int(g["n"].sum()) for g in groups)), 0.0
    for g in groups:
        k = len(g["n"])
        with torch.no_grad(), model.disable_adapter():
            rhead, rcache = prompt_pass(model, g["inputs"])
        head, cache = prompt_pass(model, g["inputs"])
        adv = torch.tensor(g["adv"], dtype=torch.float32, device=head.device)
        masks = []
        for s in range(0, k, micro):
            rows = slice(s, s + micro)
            with torch.no_grad(), model.disable_adapter():
                ref, _ = response_logprobs(model, rhead, rcache, g["inputs"], g["gen"][rows], g["n"][rows], t)
            lp, mask = response_logprobs(model, head, cache, g["inputs"], g["gen"][rows], g["n"][rows], t)
            loss, k3 = pg_loss(lp, lp.detach(), ref, adv[rows], mask, C["beta"], CLIP, denom)
            loss.backward(retain_graph=s + micro < k)
            kl += float((k3 * mask).sum())
            masks.append(mask)
            del lp, loss, ref
        if first:
            guard_mask(g["gen"], g["n"], g["done"], torch.cat(masks), pol.eos)
    return {**step_opt(opt, params, first), "kl_tok": kl / denom, "kl_caption": kl / sum(len(g["n"]) for g in groups)}


def step_opt(opt, params, first: bool) -> dict:
    import torch

    if first and any(p.grad is None for p in params):
        raise SystemExit(f"{sum(p.grad is None for p in params)}/{len(params)} trainable tensors got no gradient")
    norm = float(torch.nn.utils.clip_grad_norm_(params, 1.0))
    if not np.isfinite(norm) or (first and norm == 0.0):
        raise SystemExit(f"gradient norm {norm}: stopping before the adapter is corrupted or nothing is learnt")
    opt.step()
    opt.zero_grad(set_to_none=True)
    return {"grad_norm": norm}


def sft_update(pol, opt, params, batch: list[tuple[str, str]], first: bool) -> dict:
    """Token-mean NLL of the target captions (EOS appended), prompt and image as in sampling."""
    import torch

    from rl_policy import guard_mask, image, token_logprobs

    tok, dev = pol.proc.tokenizer, pol.model.device
    gens = [tok(c, add_special_tokens=False).input_ids[:C["max_new_tokens"] - 1] + [pol.eos[0]] for _, c in batch]
    denom, nll = float(sum(map(len, gens))), 0.0
    for (i, _), g in zip(batch, gens):
        inputs = pol.proc(text=[pol.text], images=[image(pol.names, i)], return_tensors="pt").to(dev)
        gen = torch.tensor([g], device=dev)
        n = torch.tensor([len(g)], device=dev)
        lp, mask = token_logprobs(pol.model, inputs, gen, n)
        if first:
            guard_mask(gen, n, torch.tensor([True], device=dev), mask, pol.eos)
        loss = -(lp * mask).sum() / denom
        loss.backward()
        nll += float(loss)
    return {**step_opt(opt, params, first), "nll_tok": nll}


def logp_check(pol, image_id: str) -> dict:
    """Gate 0 dry-run check (C3 (i)): generation-time log-probs of 2 samples equal the training forward's, and the
    sampler applies no processor. 2 samples, not k, so the check adds little to the measured peak."""
    import torch

    from rl_policy import rollout, token_logprobs

    inputs, gen, n, done, _, gen_lp, sgap = rollout(pol, image_id, 2, C["max_new_tokens"], True, C["temperature"])
    with torch.no_grad():
        lp, mask = token_logprobs(pol.model, inputs, gen, n, C["temperature"])
    gap = (lp - gen_lp)[mask.bool()].abs()
    return {"logp_gap_mean": float(gap.mean()), "logp_gap_max": float(gap.max()), "sampler_gap": sgap,
            "ok": float(gap.mean()) < K.GATE0["logp_gap_max"] and sgap == 0.0}


def cmd_train(a) -> int:
    import torch
    from transformers import set_seed

    from rl_policy import rollout

    gold = K.gold()
    window = tuple(json.loads(Path(a.anchors).read_text())["window"])
    pol = load(a.size)
    params = [p for p in pol.model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=C["rl_lr"] if a.arm == "grl" else C["sft_lr"], weight_decay=0.0)
    ut = [str(i) for i in K.ids("ut2402")]
    if a.arm == "grl":
        units, per = schedule(ut, K.N_TRAIN, C["seed"]), C["images_per_step"]
    else:
        refs = references() if a.arm == "sftref" else {}
        ex = ([(i, c) for i in ut for c in refs[i]] if a.arm == "sftref" else
              [(r["image_id"], r["caption"]) for r in map(json.loads, Path(a.picks).read_text().splitlines())])
        order = schedule([str(j) for j in range(len(ex))], C["sft_epochs"] * len(ex), C["seed"])
        units, per = [ex[int(j)] for j in order], C["sft_examples_per_step"]
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    log = (out / "log.jsonl").open("w", encoding="utf-8")
    checks = {"logp": logp_check(pol, ut[0])} if a.dry_run and a.arm == "grl" else {}
    if checks and not checks["logp"]["ok"]:
        raise SystemExit(f"dry-run log-prob check failed: {checks['logp']}")
    set_seed(C["seed"])
    t0, steps, stopped = time.time(), 0, None
    for step, s in enumerate(range(0, len(units), per), 1):
        if a.max_steps and step > a.max_steps:
            break
        if a.budget_hours and (time.time() - t0) / 3600 > a.budget_hours:
            stopped = "cap"
            break
        t, batch = time.time(), units[s:s + per]
        if a.arm == "grl":
            groups, why = [], Counter()
            for i in batch:
                inputs, gen, n, done, texts, _, _ = rollout(pol, i, C["k"], C["max_new_tokens"],
                                                            temperature=C["temperature"])
                rs = [RW.reward(c, d, gold[int(i)], window) for c, d in zip(texts, done.tolist())]
                r = np.array([x[0] for x in rs])
                why.update(x[1] for x in rs)
                groups.append({"inputs": inputs, "gen": gen, "n": n, "done": done, "r": r, "texts": texts,
                               "adv": rloo(r, np.zeros(len(r), bool))})
            t_roll = time.time() - t
            rec = {**grl_update(pol, opt, params, groups, step == 1), "reward": float(np.mean([g["r"] for g in groups])),
                   "gates": dict(why), "sec_rollout_per_image": t_roll / len(batch),
                   "syllables": float(np.mean([len(syllables(c)) for g in groups for c in g["texts"]]))}
        else:
            rec = sft_update(pol, opt, params, batch, step == 1)
        rec |= {"step": step, "units": s + len(batch), "sec_per_unit": (time.time() - t) / len(batch),
                "mem_gb": peak_gb()}
        log.write(json.dumps(rec, default=float) + "\n")
        log.flush()
        steps = step
    pol.model.save_pretrained(str(out / "last"), selected_adapters=["default"])
    recs = [json.loads(x) for x in (out / "log.jsonl").read_text().splitlines()]
    summary = {"stage": "train", "arm": a.arm, "size": a.size, "steps": steps, "units": recs[-1]["units"] if recs else 0,
               "unit": "image" if a.arm == "grl" else "example", "n_units_full": len(units),
               "sec_per_unit": float(np.mean([r["sec_per_unit"] for r in recs])) if recs else None,
               "hours": (time.time() - t0) / 3600, "peak_reserved_gb": peak_gb(), "checks": checks,
               "stopped": stopped, "label": "PILOT (not a confirmatory seed)"}
    (out / "summary.json").write_text(json.dumps(summary, indent=1, default=float) + "\n")
    print(json.dumps(summary, default=float))
    return 3 if stopped else 0


# ------------------------------------------------------------------------------------------------ CPU side
def read_samples(path: str) -> list[dict]:
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines()]


def cmd_anchors(a) -> int:
    rows = read_samples(a.samples)
    ids = [r["image_id"] for r in rows]
    if sorted(map(int, ids)) != K.ids("ut2402"):
        raise SystemExit("anchors need the base samples of all 2,402 UT images (step 0, train only)")
    lens = [len(syllables(c)) for r in rows for c, d in zip(r["samples"], r["finished"]) if d]
    rec = RW.anchors(lens) | {"finished_share": float(np.mean([d for r in rows for d in r["finished"]]))}
    Path(a.out).write_text(json.dumps(rec, indent=1) + "\n")
    print(json.dumps(rec))
    return 0


def pick(rows: list[dict], gold: dict, window) -> list[dict]:
    """RFT: per image the highest-reward sample (lowest index on ties); images whose best reward is 0 give none."""
    out = []
    for r in rows:
        scores = [RW.reward(c, d, gold[int(r["image_id"])], window)[0] for c, d in zip(r["samples"], r["finished"])]
        j = int(np.argmax(scores))
        if scores[j] > 0:
            out.append({"image_id": r["image_id"], "caption": r["samples"][j], "reward": scores[j]})
    return out


def cmd_pick(a) -> int:
    rows = read_samples(a.samples)
    picks = pick(rows, K.gold(), tuple(json.loads(Path(a.anchors).read_text())["window"]))
    Path(a.out).write_text("".join(json.dumps(p, ensure_ascii=False) + "\n" for p in picks), encoding="utf-8")
    rec = {"images": len(rows), "picked": len(picks), "mean_reward": float(np.mean([p["reward"] for p in picks]))}
    Path(a.out + ".summary.json").write_text(json.dumps(rec) + "\n")
    print(json.dumps(rec))
    return 0


def selftest() -> None:
    pool = [str(i) for i in range(10)]
    o = schedule(pool, 25, 0)
    assert sorted(o[:10]) == pool and sorted(o[10:20]) == pool and o == schedule(pool[::-1], 25, 0)
    g = {1: {"person", "sports ball"}, 2: {"dog"}}
    rows = [{"image_id": "1", "samples": ["một người", "một người cầm quả bóng", "một người cầm quả bóng"],
             "finished": [True, True, True]},
            {"image_id": "2", "samples": ["một người", "a dog"], "finished": [True, True]}]
    p = pick(rows, g, (1, 40))
    assert p == [{"image_id": "1", "caption": rows[0]["samples"][1], "reward": 1.0}], p  # tie -> lowest index; 0 -> none
    r = np.array([1.0, 0.0, 0.5])
    assert np.allclose(rloo(r, np.zeros(3, bool)), [0.75, -0.75, 0.0])
    print("train selftest ok")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", nargs="?", choices=("sample", "anchors", "rft-pick", "train"))
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--size", choices=tuple(K.MODELS), default="7b")
    ap.add_argument("--arm", choices=("grl", "sftref", "rft"))
    ap.add_argument("--out")
    ap.add_argument("--samples")
    ap.add_argument("--anchors")
    ap.add_argument("--picks")
    ap.add_argument("--limit", type=int, default=0, help="sample: first N images of the schedule (Gate 0 only)")
    ap.add_argument("--max-steps", type=int, default=0, help="train: stop after N optimizer steps (Gate 0 only)")
    ap.add_argument("--dry-run", action="store_true", help="train grl: the log-prob/sampler check first")
    ap.add_argument("--budget-hours", type=float, default=0.0, help="train/sample: stop (exit 3) once this is spent")
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return 0
    return {"sample": cmd_sample, "anchors": cmd_anchors, "rft-pick": cmd_pick, "train": cmd_train}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
