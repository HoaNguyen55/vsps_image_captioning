#!/usr/bin/env python
"""CN-RLOO: copy-neutral RLOO on word-level, EOS-aware CIDEr-D for the QLoRA Qwen2.5-VL-7B captioner (B1 proposal P1).

    python scripts/train_rl.py --adapter RUN --sample-only g0/dev300.jsonl --images-file data/splits/ktvic_dev300.txt
    python scripts/train_rl.py --adapter RUN --out OUT --images-file data/splits/ktvic_train_minus_dev300.txt \\
        --dev-file data/splits/ktvic_dev300.txt --n-images 1000 --tau "$TAU" [--no-copy-mask] [--dry-run]
    # gate v2's one extension: OUT's policy continued to 3,469 images, the KL anchor still --adapter
    python scripts/train_rl.py ...the same settings... --n-images 3469 --resume OUT --out OUT_EXT
    python scripts/train_rl.py --self-check      # CPU; scripts/test_train_rl.py runs a tiny random Qwen2.5-VL

One 4-bit base (train_stage2.build_model) with two adapters: PEFT's "default" is the policy (the SFT adapter, or
--resume RUN's last/), "ref" the frozen KL anchor (always --adapter, the SFT adapter); dropout is 0, so the training
forward is the sampler. Per image: k samples at --temperature (1.0; 0.8 only for the D1e fallback arm), top_p 1,
top_k 0, no repetition penalty, max_new_tokens 40, evaluate.py's short prompt. Reward, copy mask and fragment guard:
rl_reward.py, with END from train minus the dev images; sampling and log-probs: rl_policy.py. Loss per response token,
averaged over the step's response tokens: -min(ratio*A, clip(ratio, 0.8, 1.2)*A) + beta*k3, one inner epoch (one
optimizer step per rollout batch, so the ratio is 1 and the clip never binds); the k responses are back-propagated
--micro at a time. Greedy dev CIDEr-D every --eval-every images is monitoring only: gate v2 (rl_report.py) scores
OUT/last with evaluate.py, and nothing here selects a checkpoint. Dev images are never trained on; test is never read.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from evaluate import check_adapter_base, references  # noqa: E402
from rl_policy import (CLIP, Policy, greedy, guard_mask, pg_loss, policy, prompt_pass, response_lengths,  # noqa: E402
                       response_logprobs, rollout, token_logprobs)
from rl_report import c3_verdict  # noqa: E402
from rl_reward import SPLIT, Reward, Segmenter, boot, content, function_end, replica_gap, rloo, syllables  # noqa: E402
from train_stage2 import MODEL_ID  # noqa: E402

EVAL_BATCH = 8
#: Settings a --resume run must share with the run it continues (it is that run, extended).
RESUME_KEYS = ("adapter", "images_file", "seed", "k", "beta", "lr", "tau", "no_copy_mask", "temperature", "micro",
               "images_per_step", "max_new_tokens")


def read_ids(path: str) -> list[str]:
    return Path(path).read_text(encoding="utf-8").split()


def schedule(pool: list[str], n: int, seed: int) -> list[str]:
    """n images: seeded reshuffles of the pool, one after another (an epoch never repeats an image)."""
    rng, order = random.Random(seed), []
    while len(order) < n:
        epoch = sorted(pool)
        rng.shuffle(epoch)
        order += epoch
    return order[:n]


def configure(model) -> None:
    """Policy = "default" (the only trainable adapter), every dropout off, eval mode (no checkpointing: the shared
    prompt cache needs use_cache)."""
    import torch

    model.set_adapter("default")
    for m in model.modules():
        if isinstance(m, torch.nn.Dropout):
            m.p = 0.0  # LoRA dropout 0.05 in the SFT adapters: off, so the training forward is the sampler
    trainable = [n for n, p in model.named_parameters() if p.requires_grad]
    assert trainable and all(".default." in n for n in trainable), trainable[:3]
    model.eval()


def load(args, with_ref: bool):
    """build_model's 4-bit base with the policy adapter (the SFT adapter, or --resume RUN's last/) as "default" and
    the SFT adapter again as "ref", the frozen KL anchor."""
    from train_stage2 import build_model

    start = str(Path(args.resume) / "last") if args.resume else args.adapter
    for a in {start, args.adapter}:
        check_adapter_base(a, MODEL_ID)
    model, proc = build_model(argparse.Namespace(vision_tokens=0, force_4bit=True, stage="rl", base_model=MODEL_ID,
                                                 adapter=start))  # 0: build_model's 512 tokens at 4-bit
    if with_ref:
        model.load_adapter(args.adapter, adapter_name="ref")
    configure(model)
    proc.tokenizer.padding_side = "left"  # batched greedy
    return model, proc


def save_last(model, opt, out: Path, state: dict) -> None:
    """OUT/last: the policy adapter (what evaluate.py and gate v2 score), its AdamW state and the schedule position."""
    import torch

    model.save_pretrained(str(out / "last"), selected_adapters=["default"])
    torch.save(opt.state_dict(), out / "last" / "optimizer.pt")
    (out / "last" / "state.json").write_text(json.dumps(state, indent=1), encoding="utf-8")


def resume_from(run: str, opt, args) -> int:
    """Load RUN's AdamW state and return how many images of the shared schedule it trained on, after checking that
    this run has RUN's settings (load() already took the policy weights from RUN/last)."""
    import torch

    state = json.loads((Path(run) / "last" / "state.json").read_text(encoding="utf-8"))
    mine = {k: getattr(args, k) for k in RESUME_KEYS}
    assert {k: state[k] for k in RESUME_KEYS} == mine, ({k: state[k] for k in RESUME_KEYS}, mine)
    opt.load_state_dict(torch.load(Path(run) / "last" / "optimizer.pt", map_location="cpu", weights_only=True))
    return int(state["images_done"])


def update(pol: Policy, opt, params, groups: list[dict], args, first: bool) -> dict:
    """One optimizer step on the rollouts of several images (one inner epoch)."""
    import torch

    model, denom, t = pol.model, float(sum(int(g["n"].sum()) for g in groups)), args.temperature
    kl, gaps = 0.0, []
    for g in groups:
        with torch.no_grad():
            model.set_adapter("ref")
            ref, _ = token_logprobs(model, g["inputs"], g["gen"], g["n"], t)
            model.set_adapter("default")
        head, cache = prompt_pass(model, g["inputs"])
        adv, k, lps, masks = torch.tensor(g["adv"], dtype=torch.float32, device=ref.device), len(g["n"]), [], []
        for s in range(0, k, args.micro):  # --micro responses per backward; the prompt graph stays until the last
            rows = slice(s, s + args.micro)
            lp, mask = response_logprobs(model, head, cache, g["inputs"], g["gen"][rows], g["n"][rows], t)
            loss, k3 = pg_loss(lp, lp.detach(), ref[rows], adv[rows], mask, args.beta, CLIP, denom)
            loss.backward(retain_graph=s + args.micro < k)
            kl += float((k3 * mask).sum())
            lps.append(lp.detach())
            masks.append(mask)
            del lp, loss  # this chunk's graph goes before the next chunk's forward
        lp, mask = torch.cat(lps), torch.cat(masks)
        if args.dry_run:
            guard_mask(g["gen"], g["n"], g["done"], mask, pol.eos)
        if g["gen_lp"] is not None:
            gaps.append((lp - g["gen_lp"])[mask.bool()].abs())
    if first and any(p.grad is None for p in params):
        raise SystemExit(f"{sum(p.grad is None for p in params)}/{len(params)} trainable tensors got no gradient")
    norm = float(torch.nn.utils.clip_grad_norm_(params, 1.0))
    if not np.isfinite(norm) or (first and norm == 0.0):
        raise SystemExit(f"gradient norm {norm}: stopping before the adapter is corrupted or nothing is learnt")
    opt.step()
    opt.zero_grad(set_to_none=True)
    gap = torch.cat(gaps) if gaps else None
    return {"kl_tok": kl / denom, "kl_caption": kl / sum(len(g["n"]) for g in groups), "grad_norm": norm,
            "logp_gap": None if gap is None else [float(gap.mean()), float(gap.max())]}


def dev_eval(pol: Policy, dev: list[str], reward: Reward, batch: int) -> tuple[dict, np.ndarray, float]:
    """Greedy dev captions (4-bit, batched: monitoring only), their per-image CIDEr-D as evaluate.py scores
    (pycocoevalcap, df from the dev references), and the share that copies a dev reference."""
    from pycocoevalcap.cider.cider import Cider

    caps = {i: c for i, (c, _) in greedy(pol, dev, batch).items()}
    seg = dict(zip(dev, reward.seg([caps[i] for i in dev])))
    gts = {i: [" ".join(r) for r in reward.refs[i]] for i in dev}
    per = np.asarray(Cider().compute_score(gts, {i: [seg[i]] for i in dev})[1])
    exact = np.mean([content(seg[i].split()) in [content(r) for r in reward.refs[i]] for i in dev])
    return caps, per, float(exact)


def train(args) -> int:
    import torch
    from transformers import set_seed

    from rescap.chair import objects_in

    refs = references(SPLIT)
    pool, held = (read_ids(args.images_file) if args.images_file else sorted(refs)), read_ids(args.dev_file)
    dev = held[:args.dev_limit] if args.dev_limit else held
    assert not set(pool) & set(held), "dev images in the RL pool"
    assert set(pool) | set(held) <= set(refs), f"images without {SPLIT} references"
    reward = Reward(refs, Segmenter(), end_from=set(refs) - set(held))
    order = schedule(pool, args.n_images or len(pool), args.seed)
    pol = policy(*load(args, with_ref=True))
    model, params = pol.model, [p for p in pol.model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=args.lr, weight_decay=0.0)
    start = resume_from(args.resume, opt, args) if args.resume else 0
    assert start < len(order), f"{args.resume} already trained {start} of the {len(order)} images"
    set_seed(args.seed + start)  # a resumed run draws new samples, not the first run's
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    logf = (out / "log.jsonl").open("w", encoding="utf-8")

    def log(rec: dict) -> None:
        line = json.dumps(rec, ensure_ascii=False, default=float)
        logf.write(line + "\n")
        logf.flush()
        print(line, flush=True)

    def dev_round(done: int, base: np.ndarray | None = None) -> tuple[dict, np.ndarray, dict]:
        t = time.time()
        caps, per, exact = dev_eval(pol, dev, reward, EVAL_BATCH)
        (out / f"dev_{done}.json").write_text(json.dumps(caps, ensure_ascii=False, indent=1), encoding="utf-8")
        return caps, per, {"eval": done, "cider": 100 * per.mean(), "exact_copy": exact, "sec": time.time() - t,
                           "delta_vs_first": [100 * v for v in boot(per - (per if base is None else base))],
                           "fw_end": np.mean([function_end(c) for c in caps.values()]),
                           "fragments": np.mean([reward.fragment(x.split()) for x in reward.seg(list(caps.values()))]),
                           "syllables": np.mean([len(syllables(c)) for c in caps.values()])}

    started = time.time()
    caps, base, rec = dev_round(start)
    log(rec)
    last, c3, steps = rec, {}, []
    if args.dry_run:
        c3["reward_replica_max_abs_diff"] = replica_gap(reward, {i: caps[i] for i in dev[:20]})
    for step, s in enumerate(range(start, len(order), args.images_per_step), 1):
        t, batch, groups = time.time(), order[s:s + args.images_per_step], []
        for i in batch:
            inputs, gen, n, done, texts, gen_lp, sgap = rollout(pol, i, args.k, args.max_new_tokens,
                                                                args.dry_run and step == 1, args.temperature)
            r, m, dist, frag = reward(i, texts, done.tolist())
            at_tau = m >= args.tau if args.tau is not None else np.zeros(len(m), bool)
            groups.append({"inputs": inputs, "gen": gen, "n": n, "done": done, "gen_lp": gen_lp, "sgap": sgap,
                           "texts": texts, "r": r, "dist": dist, "at_tau": at_tau, "frag": frag,
                           "adv": rloo(r, at_tau & (not args.no_copy_mask), nonpos=frag)})
        stats = update(pol, opt, params, groups, args, first=step == 1)
        R = np.array([g["r"] for g in groups])
        caps_k = [c for g in groups for c in g["texts"]]
        rec = {"step": step, "images": s + len(batch), "rollouts": R.size, "reward": 100 * R.mean(),
               "reward_sd": 100 * R.std(1).mean(), "exact_copies": int(sum((g["dist"] == 0).sum() for g in groups)),
               "near_copies": int(sum((g["dist"] <= 1).sum() for g in groups)),
               "copies_at_tau": int(sum(g["at_tau"].sum() for g in groups)),
               "masked": 0 if args.no_copy_mask else int(sum(g["at_tau"].sum() for g in groups)),
               "fragments": int(sum(g["frag"].sum() for g in groups)),
               "mentions": np.mean([len(objects_in(c)) for c in caps_k]),
               "fw_end": np.mean([function_end(c) for c in caps_k]),
               "syllables": np.mean([len(syllables(c)) for c in caps_k]),
               "finished": np.mean([d for g in groups for d in g["done"].tolist()]), **stats,
               "sec_per_image": (time.time() - t) / len(batch), "mem_gb": torch.cuda.max_memory_reserved() / 1e9}
        log(rec)
        steps.append(rec)
        if args.dry_run and step == 1:
            c3["logp_gap_mean_max"] = stats["logp_gap"]
            c3["sampler_gap"] = max(g["sgap"] for g in groups)
        done_n = s + len(batch)
        if done_n // args.eval_every > s // args.eval_every or done_n == len(order):
            _, _, last = dev_round(done_n, base)
            log(last)
    save_last(model, opt, out, {"images_done": len(order), "resumed_from": args.resume,
                                **{k: getattr(args, k) for k in RESUME_KEYS}})
    summary = {"args": vars(args), "images": [start, len(order)], "steps": len(steps),
               "dev_monitoring_first_last": [100 * base.mean(), last["cider"]],
               "kl_caption_last": steps[-1]["kl_caption"],
               "sec_per_image": np.mean([r["sec_per_image"] for r in steps]),
               "hours": (time.time() - started) / 3600, "peak_reserved_gb": torch.cuda.max_memory_reserved() / 1e9,
               "peak_allocated_gb": torch.cuda.max_memory_allocated() / 1e9}
    (out / "summary.json").write_text(json.dumps(summary, indent=1, default=float), encoding="utf-8")
    print(json.dumps(summary, indent=1, default=float), flush=True)
    if args.dry_run:
        return c3_verdict(out, c3, summary, len(order))
    return 0


def sample_only(args) -> int:
    """G0: k rollouts and the greedy caption per image (the RL step-0 distribution), one jsonl row per image."""
    from transformers import set_seed

    pool = read_ids(args.images_file)
    ids = schedule(pool, args.n_images or len(pool), args.seed)
    assert set(ids) <= set(references(SPLIT)), f"images without {SPLIT} references"
    set_seed(args.seed)
    pol = policy(*load(args, with_ref=False))
    g = greedy(pol, ids, EVAL_BATCH)
    out = Path(args.sample_only)
    out.parent.mkdir(parents=True, exist_ok=True)
    started = time.time()
    with out.open("w", encoding="utf-8") as fh:
        for n, i in enumerate(ids, 1):
            _, _, _, done, texts, _, _ = rollout(pol, i, args.k, args.max_new_tokens, temperature=args.temperature)
            fh.write(json.dumps({"image_id": i, "samples": texts, "finished": done.tolist(), "greedy": g[i][0],
                                 "greedy_finished": g[i][1]}, ensure_ascii=False) + "\n")
            if n % 25 == 0 or n == len(ids):
                print(f"  [{n}/{len(ids)}] {(time.time() - started) / n:.2f}s/image", flush=True)
    return 0


def _check() -> None:
    """CPU: reward, EOS handling, copy statistic, fragment guard and RLOO with masked copies (rl_reward._check), EOS
    at the token level, the loss mask, and the schedule an extension continues. scripts/test_train_rl.py: the loss,
    --resume and the policy path on a tiny random Qwen2.5-VL."""
    import torch

    from rl_reward import _check as reward_check

    reward_check()
    eos = [151645, 151643]
    gen = torch.tensor([[5, 6, 151645, 151643], [5, 6, 7, 8], [151643, 0, 0, 0]])
    n, done = response_lengths(gen, eos)
    assert n.tolist() == [3, 4, 1] and done.tolist() == [True, False, True]
    mask = (torch.arange(4)[None] < n[:, None]).float()
    guard_mask(gen, n, done, mask, eos)
    for broken in (mask.roll(1, 1), torch.ones_like(mask)):
        try:
            guard_mask(gen, n, done, broken, eos)
        except AssertionError:
            continue
        raise RuntimeError("guard_mask accepted a loss mask beyond the generated tokens")
    pool = [str(i) for i in range(3469)]
    full = schedule(pool, 3469, 42)
    assert full[:1000] == schedule(pool, 1000, 42) and sorted(full) == sorted(pool)  # the extension sees new images
    print("train_rl self-check ok")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--adapter", help="SFT adapter dir: the policy's start and, always, the KL reference")
    ap.add_argument("--out", help="run dir: log.jsonl, dev_<n>.json, last/, summary.json (+ c3.json)")
    ap.add_argument("--resume", metavar="RUN", help="continue RUN's policy (RUN/last) and AdamW state to --n-images")
    ap.add_argument("--sample-only", metavar="JSONL", help="G0: k rollouts + the greedy caption per image, no training")
    ap.add_argument("--images-file", help="training (or sampling) image ids, one per line; default every train image")
    ap.add_argument("--dev-file", help="dev image ids: monitoring only, asserted disjoint from the training images")
    ap.add_argument("--dev-limit", type=int, default=0)
    ap.add_argument("--n-images", type=int, default=0, help="images to train on / sample (default: the whole pool)")
    ap.add_argument("--images-per-step", type=int, default=5)
    ap.add_argument("--k", type=int, default=8)
    ap.add_argument("--micro", type=int, default=4, help="responses per backward chunk (memory, not the gradient)")
    ap.add_argument("--max-new-tokens", type=int, default=40)
    ap.add_argument("--temperature", type=float, default=1.0, help="sampling temperature; log-probs use the same")
    ap.add_argument("--tau", type=float, default=None, help="copy threshold on m(c): the G0 report's tau")
    ap.add_argument("--no-copy-mask", action="store_true", help="plain RLOO: copies keep their advantage")
    ap.add_argument("--beta", type=float, default=0.03)
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--eval-every", type=int, default=250, help="images between greedy dev evaluations (monitoring)")
    ap.add_argument("--dry-run", action="store_true", help="judge D1 C3 guards: OUT/c3.json, exit 1 unless all hold")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--self-check", action="store_true")
    args = ap.parse_args()
    if args.self_check:
        _check()
        return 0
    if not args.adapter:
        ap.error("--adapter is required")
    if args.sample_only:
        if not args.images_file:
            ap.error("--sample-only needs --images-file")
        return sample_only(args)
    if not (args.out and args.dev_file):
        ap.error("training needs --out and --dev-file")
    if args.tau is None and not args.no_copy_mask:
        ap.error("CN-RLOO needs --tau (the G0 report's); --no-copy-mask runs plain RLOO")
    if args.resume and (args.dry_run or Path(args.resume).resolve() == Path(args.out).resolve()):
        ap.error("--resume writes a new --out and is never a dry run")
    return train(args)


if __name__ == "__main__":
    sys.exit(main())
