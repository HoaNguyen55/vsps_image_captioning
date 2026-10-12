#!/usr/bin/env python
"""CN-RLOO: copy-neutral RLOO on word-level, EOS-aware CIDEr-D for the QLoRA Qwen2.5-VL-7B captioner (B1 proposal P1).

    python scripts/train_rl.py --adapter RUN --sample-only g0/dev300.jsonl --images-file data/splits/ktvic_dev300.txt
    python scripts/train_rl.py --adapter RUN --out OUT --images-file data/splits/ktvic_train_minus_dev300.txt \\
        --dev-file data/splits/ktvic_dev300.txt --n-images 1000 --tau "$TAU" [--no-copy-mask] [--dry-run]
    python scripts/train_rl.py --self-check      # CPU; scripts/test_train_rl.py runs a tiny random Qwen2.5-VL

One 4-bit base (train_stage2.build_model) with two adapters from the SFT dir: PEFT's "default" is the policy, "ref"
the frozen KL anchor; dropout is 0, so the training forward is the sampler. Per image: k samples at T=1, top_p 1,
top_k 0, no repetition penalty (on-policy), max_new_tokens 40, evaluate.py's short prompt; reward: rl_reward.py.
Loss per response token, averaged over the step's response tokens: -min(ratio*A, clip(ratio, 0.8, 1.2)*A) + beta*k3,
one inner epoch (one optimizer step per rollout batch, so the ratio is 1 and the clip never binds). The prompt (~600
tokens) runs once per image and its KV cache serves the k responses, as in generate(): this replaces gradient
checkpointing (a k x 600-token forward is what made SFT cost 0.92 s per row). Greedy dev CIDEr-D (as evaluate.py)
every --eval-every images selects OUT/best. Dev images are never trained on; KTVIC test is never read.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from evaluate import KTVIC, PROMPTS, check_adapter_base, file_names, references  # noqa: E402
from rl_report import c3_verdict  # noqa: E402
from rl_reward import SPLIT, Reward, Segmenter, boot, content, function_end, replica_gap, rloo, syllables  # noqa: E402
from train_stage2 import MODEL_ID  # noqa: E402

GREEDY_MAX_NEW, EVAL_BATCH, CLIP = 160, 8, 0.2  # evaluate.py's max_new_tokens; dev batch; PPO ratio clip (B1)


@dataclass
class Policy:
    """The model and what every decoding call needs with it."""
    model: object
    proc: object
    text: str  # evaluate.py's short prompt in the chat template
    names: dict  # image id -> file name
    eos: list


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


def image(names: dict, image_id: str):
    from PIL import Image

    return Image.open(KTVIC / "images" / names[image_id]).convert("RGB")


def chat(proc) -> str:
    msg = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": PROMPTS["short"]}]}]
    return proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)


def load(args, with_ref: bool):
    """build_model's 4-bit base + SFT adapter ("default", trainable), the same adapter again as "ref" (frozen)."""
    import torch

    from train_stage2 import build_model

    check_adapter_base(args.adapter, MODEL_ID)
    model, proc = build_model(argparse.Namespace(vision_tokens=0, force_4bit=True, stage="rl", base_model=MODEL_ID,
                                                 adapter=args.adapter))  # 0: build_model's 512 tokens at 4-bit
    if with_ref:
        model.load_adapter(args.adapter, adapter_name="ref")
    model.set_adapter("default")
    for m in model.modules():
        if isinstance(m, torch.nn.Dropout):
            m.p = 0.0  # LoRA dropout 0.05 in the SFT adapters: off, so the training forward is the sampler
    trainable = [n for n, p in model.named_parameters() if p.requires_grad]
    assert trainable and all(".default." in n for n in trainable), trainable[:3]
    model.eval()  # no checkpointing: the shared prompt cache needs use_cache (see token_logprobs)
    proc.tokenizer.padding_side = "left"  # batched greedy
    return model, proc


def response_lengths(gen, eos: list[int]):
    """(tokens up to and including the first EOS, finished?) per row; a row without EOS was cut by max_new_tokens."""
    import torch

    hit = torch.isin(gen, torch.tensor(eos, device=gen.device))
    first = hit.int().argmax(1) + 1
    done = hit.any(1)
    return torch.where(done, first, torch.full_like(first, gen.shape[1])), done


def rollout(pol: Policy, image_id: str, k: int, max_new: int, with_logp: bool = False):
    """k samples from the policy itself; with_logp adds the generation-time log-probs of the sampled tokens and the
    largest gap between processed and raw next-token log-probs (0 when nothing reshapes the sampler)."""
    import torch

    inputs = pol.proc(text=[pol.text], images=[image(pol.names, image_id)], return_tensors="pt").to(pol.model.device)
    with torch.no_grad():
        out = pol.model.generate(**inputs, do_sample=True, temperature=1.0, top_p=1.0, top_k=0, repetition_penalty=1.0,
                                 num_return_sequences=k, max_new_tokens=max_new, eos_token_id=pol.eos, use_cache=True,
                                 return_dict_in_generate=True, output_logits=with_logp, output_scores=with_logp)
    gen = out.sequences[:, inputs["input_ids"].shape[1]:]
    n, done = response_lengths(gen, pol.eos)
    texts = [pol.proc.tokenizer.decode(g[:m], skip_special_tokens=True).strip() for g, m in zip(gen, n.tolist())]
    gen_lp = sampler_gap = None
    if with_logp:
        raw = torch.stack(out.logits, 1).float().log_softmax(-1)
        gen_lp = raw.gather(-1, gen[..., None]).squeeze(-1)
        sampler_gap = float((torch.stack(out.scores, 1).float().log_softmax(-1) - raw).abs().nan_to_num(0).max())
    return inputs, gen, n, done, texts, gen_lp, sampler_gap


def token_logprobs(model, inputs, gen, n):
    """Log-probs of the k responses under the active adapter, and the loss mask: generated tokens up to and including
    the first EOS, nothing else. The prompt runs once (lm_head on its last position only, which predicts the first
    response token) and its KV cache is repeated for the k responses, which run as one continuation."""
    import torch

    k, T = gen.shape
    hook = model.get_base_model().lm_head.register_forward_pre_hook(lambda _m, a: (a[0][:, -1:],))
    try:
        p = model(**inputs, use_cache=True)
    finally:
        hook.remove()
    cache = p.past_key_values
    cache.batch_repeat_interleave(k)
    L = inputs["input_ids"].shape[1]
    mask = torch.arange(T, device=gen.device)[None] < n[:, None]
    att = torch.cat([inputs["attention_mask"].expand(k, -1), mask.long()], 1)
    r = model(input_ids=gen, attention_mask=att, past_key_values=cache, use_cache=True,
              cache_position=torch.arange(L, L + T, device=gen.device))
    logits = torch.cat([p.logits.expand(k, -1, -1), r.logits[:, :-1]], 1).float()
    return logits.gather(-1, gen[..., None]).squeeze(-1) - logits.logsumexp(-1), mask.float()


def pg_loss(lp, old, ref, adv, mask, beta: float, clip: float, denom: float):
    """Clipped policy gradient + beta * k3 KL to the reference, summed over response tokens / denom (token mean)."""
    import torch

    ratio = torch.exp(lp - old)
    a = adv[:, None]
    pg = -torch.minimum(ratio * a, ratio.clamp(1 - clip, 1 + clip) * a)
    d = ref - lp
    k3 = torch.exp(d) - d - 1
    return ((pg + beta * k3) * mask).sum() / denom, k3.detach()


def guard_mask(gen, n, done, mask, eos: list[int]) -> None:
    """Judge C3 (iii): the loss covers generated tokens only, up to and including the first EOS."""
    is_eos = np.isin(gen.cpu().numpy(), eos)
    for row, (m, d, keep) in enumerate(zip(n.tolist(), done.tolist(), mask.cpu().numpy())):
        assert keep.shape == (gen.shape[1],) and keep[:m].all() and not keep[m:].any(), row
        assert not is_eos[row, :m - 1].any() and is_eos[row, m - 1] == d and (d or m == gen.shape[1]), row


def update(pol: Policy, opt, params, groups: list[dict], args, first: bool) -> dict:
    """One optimizer step on the rollouts of several images (one inner epoch)."""
    import torch

    model, denom = pol.model, float(sum(int(g["n"].sum()) for g in groups))
    kl, gaps = 0.0, []
    for g in groups:
        with torch.no_grad():
            model.set_adapter("ref")
            ref, _ = token_logprobs(model, g["inputs"], g["gen"], g["n"])
            model.set_adapter("default")
        lp, mask = token_logprobs(model, g["inputs"], g["gen"], g["n"])
        if args.dry_run:
            guard_mask(g["gen"], g["n"], g["done"], mask, pol.eos)
        if g["gen_lp"] is not None:
            gaps.append((lp.detach() - g["gen_lp"])[mask.bool()].abs())
        adv = torch.tensor(g["adv"], dtype=lp.dtype, device=lp.device)
        loss, k3 = pg_loss(lp, lp.detach(), ref, adv, mask, args.beta, CLIP, denom)
        loss.backward()
        kl += float((k3 * mask).sum())
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


def greedy(pol: Policy, ids: list[str], batch: int) -> dict:
    """evaluate.py's decoding (greedy, 160 new tokens, the generation config's repetition penalty), batched with left
    padding: {image_id: (caption, finished)}."""
    import torch

    out = {}
    for s in range(0, len(ids), batch):
        chunk = ids[s:s + batch]
        inputs = pol.proc(text=[pol.text] * len(chunk), images=[image(pol.names, i) for i in chunk], padding=True,
                          return_tensors="pt").to(pol.model.device)
        with torch.no_grad():
            seqs = pol.model.generate(**inputs, do_sample=False, max_new_tokens=GREEDY_MAX_NEW, eos_token_id=pol.eos,
                                      use_cache=True)
        gen = seqs[:, inputs["input_ids"].shape[1]:]
        n, done = response_lengths(gen, pol.eos)
        for i, g, m, d in zip(chunk, gen, n.tolist(), done.tolist()):
            out[i] = (pol.proc.tokenizer.decode(g[:m], skip_special_tokens=True).strip(), d)
    return out


def dev_eval(pol: Policy, dev: list[str], reward: Reward, batch: int) -> tuple[dict, np.ndarray, float]:
    """Greedy dev captions, their per-image CIDEr-D exactly as evaluate.py scores (pycocoevalcap, df from the dev
    references), and the share that copies a dev reference."""
    from pycocoevalcap.cider.cider import Cider

    caps = {i: c for i, (c, _) in greedy(pol, dev, batch).items()}
    seg = dict(zip(dev, reward.seg([caps[i] for i in dev])))
    gts = {i: [" ".join(r) for r in reward.refs[i]] for i in dev}
    per = np.asarray(Cider().compute_score(gts, {i: [seg[i]] for i in dev})[1])
    exact = np.mean([content(seg[i].split()) in [content(r) for r in reward.refs[i]] for i in dev])
    return caps, per, float(exact)


def policy(model, proc) -> Policy:
    e = model.generation_config.eos_token_id
    return Policy(model, proc, chat(proc), file_names(SPLIT), [e] if isinstance(e, int) else list(e))


def train(args) -> int:
    import torch
    from transformers import set_seed

    refs = references(SPLIT)
    pool, held = (read_ids(args.images_file) if args.images_file else sorted(refs)), read_ids(args.dev_file)
    dev = held[:args.dev_limit] if args.dev_limit else held
    assert not set(pool) & set(held), "dev images in the RL pool"
    assert set(pool) | set(held) <= set(refs), f"images without {SPLIT} references"
    set_seed(args.seed)
    reward = Reward(refs, Segmenter())
    order = schedule(pool, args.n_images or len(pool), args.seed)
    pol = policy(*load(args, with_ref=True))
    model, params = pol.model, [p for p in pol.model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=args.lr, weight_decay=0.0)
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
                           "delta_vs_step0": [100 * v for v in boot(per - (per if base is None else base))],
                           "fw_end": np.mean([function_end(c) for c in caps.values()]),
                           "syllables": np.mean([len(syllables(c)) for c in caps.values()])}

    started = time.time()
    caps, base, rec = dev_round(0)
    log(rec)
    best, best_per, best_at, c3, steps = base.mean(), base, 0, {}, []
    model.save_pretrained(str(out / "best"), selected_adapters=["default"])
    if args.dry_run:
        c3["reward_replica_max_abs_diff"] = replica_gap(reward, {i: caps[i] for i in dev[:20]})
    for step, s in enumerate(range(0, len(order), args.images_per_step), 1):
        t, batch, groups = time.time(), order[s:s + args.images_per_step], []
        for i in batch:
            inputs, gen, n, done, texts, gen_lp, sgap = rollout(pol, i, args.k, args.max_new_tokens,
                                                                args.dry_run and step == 1)
            r, m, dist = reward(i, texts, done.tolist())
            at_tau = m >= args.tau if args.tau is not None else np.zeros(len(m), bool)
            groups.append({"inputs": inputs, "gen": gen, "n": n, "done": done, "gen_lp": gen_lp, "sgap": sgap,
                           "texts": texts, "r": r, "dist": dist, "at_tau": at_tau,
                           "adv": rloo(r, at_tau & (not args.no_copy_mask))})
        stats = update(pol, opt, params, groups, args, first=step == 1)
        R = np.array([g["r"] for g in groups])
        caps_k = [c for g in groups for c in g["texts"]]
        rec = {"step": step, "images": s + len(batch), "rollouts": R.size, "reward": 100 * R.mean(),
               "reward_sd": 100 * R.std(1).mean(), "exact_copies": int(sum((g["dist"] == 0).sum() for g in groups)),
               "near_copies": int(sum((g["dist"] <= 1).sum() for g in groups)),
               "copies_at_tau": int(sum(g["at_tau"].sum() for g in groups)),
               "masked": 0 if args.no_copy_mask else int(sum(g["at_tau"].sum() for g in groups)),
               "fw_end": np.mean([function_end(c) for c in caps_k]), "syllables": np.mean([len(syllables(c)) for c in caps_k]),
               "finished": np.mean([d for g in groups for d in g["done"].tolist()]), **stats,
               "sec_per_image": (time.time() - t) / len(batch), "mem_gb": torch.cuda.max_memory_reserved() / 1e9}
        log(rec)
        steps.append(rec)
        if args.dry_run and step == 1:
            c3["logp_gap_mean_max"] = stats["logp_gap"]
            c3["sampler_gap"] = max(g["sgap"] for g in groups)
        done_n = s + len(batch)
        if done_n // args.eval_every > s // args.eval_every or done_n == len(order):
            _, per, rec = dev_round(done_n, base)
            rec["best"] = bool(per.mean() > best)
            if rec["best"]:
                best, best_per, best_at = per.mean(), per, done_n
                model.save_pretrained(str(out / "best"), selected_adapters=["default"])
            log(rec)
    model.save_pretrained(str(out / "last"), selected_adapters=["default"])
    summary = {"args": vars(args), "images": len(order), "steps": len(steps), "dev_step0": 100 * base.mean(),
               "dev_best": 100 * best, "best_at_images": best_at,
               "delta_best_vs_step0": [100 * v for v in boot(best_per - base)],
               "kl_caption_last": steps[-1]["kl_caption"], "sec_per_image": np.mean([r["sec_per_image"] for r in steps]),
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
            _, _, _, done, texts, _, _ = rollout(pol, i, args.k, args.max_new_tokens)
            fh.write(json.dumps({"image_id": i, "samples": texts, "finished": done.tolist(), "greedy": g[i][0],
                                 "greedy_finished": g[i][1]}, ensure_ascii=False) + "\n")
            if n % 25 == 0 or n == len(ids):
                print(f"  [{n}/{len(ids)}] {(time.time() - started) / n:.2f}s/image", flush=True)
    return 0


def _check() -> None:
    """CPU: reward, EOS handling, copy statistic and RLOO with masked copies (rl_reward._check), then EOS at the token
    level and the loss mask. scripts/test_train_rl.py: the loss, and the policy path on a tiny random Qwen2.5-VL."""
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
    print("train_rl self-check ok")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--adapter", help="SFT adapter dir: the policy's start and the KL reference")
    ap.add_argument("--out", help="run dir: log.jsonl, dev_<n>.json, best/, last/, summary.json (+ c3.json)")
    ap.add_argument("--sample-only", metavar="JSONL", help="G0: k rollouts + the greedy caption per image, no training")
    ap.add_argument("--images-file", help="training (or sampling) image ids, one per line; default every train image")
    ap.add_argument("--dev-file", help="dev image ids: selection only, asserted disjoint from the training images")
    ap.add_argument("--dev-limit", type=int, default=0)
    ap.add_argument("--n-images", type=int, default=0, help="images to train on / sample (default: the whole pool)")
    ap.add_argument("--images-per-step", type=int, default=5)
    ap.add_argument("--k", type=int, default=8)
    ap.add_argument("--max-new-tokens", type=int, default=40)
    ap.add_argument("--tau", type=float, default=None, help="copy threshold on m(c): the G0 report's tau")
    ap.add_argument("--no-copy-mask", action="store_true", help="plain RLOO: copies keep their advantage")
    ap.add_argument("--beta", type=float, default=0.03)
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--eval-every", type=int, default=250, help="images between greedy dev evaluations")
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
    return train(args)


if __name__ == "__main__":
    sys.exit(main())
