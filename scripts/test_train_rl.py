#!/usr/bin/env python
"""CPU test of train_rl.py's policy path on a tiny RANDOM Qwen2.5-VL (2 layers, hidden 64; the 7B is never loaded),
driven by the real Qwen2.5-VL processor and KTVIC train images, on the installed transformers/PEFT code path.

    NCS_DATA=/root/ncs-data nice -n 19 taskset -c 12-15 python scripts/test_train_rl.py

Checks: the loss (ratio 1, clip, k3); the prompt-cache-shared log-probs and their gradients equal a full-sequence
forward; generation-time log-probs equal the training forward and the sampler applies no processor (judge D1 C3 (i));
the loss mask covers generated tokens only (C3 (iii)); the "ref" adapter is frozen and untouched by switching;
batched left-padded greedy equals one image at a time; generate() with lm_head on the last position only emits the
same tokens; an optimizer step back-propagated --micro responses at a time equals the unchunked step.
"""
from __future__ import annotations

import argparse
import sys

import numpy as np

from evaluate import file_names
from rl_reward import SPLIT
from train_rl import (Policy, chat, greedy, guard_mask, image, last_position, pg_loss, response_lengths, rollout,
                      schedule, token_logprobs, update)
from train_stage2 import MODEL_ID

EOS = [151645, 151643]


def check_loss() -> None:
    import torch

    # ratio 1 (one inner epoch): the gradient is -A/denom on every response token, and k3 is 0 at the reference
    lp = torch.tensor([[-1.0, -2.0, -3.0], [-0.5, -0.5, -9.0]], requires_grad=True)
    m2, adv = torch.tensor([[1.0, 1.0, 1.0], [1.0, 1.0, 0.0]]), torch.tensor([2.0, -1.0])
    loss, k3 = pg_loss(lp, lp.detach(), lp.detach(), adv, m2, beta=0.1, clip=0.2, denom=5.0)
    loss.backward()
    assert torch.allclose(lp.grad, -adv[:, None] * m2 / 5) and abs(loss.item() + (2 * 3 - 1 * 2) / 5) < 1e-6
    assert float((k3 * m2).abs().sum()) == 0.0
    # the clip binds for A > 0 above 1 + clip and not for A < 0; k3 > 0 off the reference and pulls towards it
    lp = torch.zeros(2, 1, requires_grad=True)
    loss, _ = pg_loss(lp, torch.full((2, 1), -np.log(1.5)), lp.detach(), torch.tensor([1.0, -1.0]), torch.ones(2, 1),
                      0.0, 0.2, 2.0)
    loss.backward()
    assert lp.grad[0, 0] == 0 and torch.isclose(lp.grad[1, 0], torch.tensor(0.75))
    lp = torch.tensor([[-1.0]], requires_grad=True)
    loss, k3 = pg_loss(lp, lp.detach(), torch.tensor([[-2.0]]), torch.zeros(1), torch.ones(1, 1), 1.0, 0.2, 1.0)
    loss.backward()
    assert k3.item() > 0 and lp.grad.item() > 0  # gradient descent lowers log p towards the reference's -2
    order = schedule(["a", "b", "c"], 7, 0)
    assert order == schedule(["c", "b", "a"], 7, 0) and sorted(order[:3]) == sorted(order[3:6]) == ["a", "b", "c"]


def tiny_policy():
    """Random 2-layer Qwen2.5-VL with a trainable "default" LoRA (random B) and a zero-B "ref" adapter."""
    import torch
    from peft import LoraConfig, get_peft_model
    from transformers import Qwen2_5_VLConfig, Qwen2_5_VLForConditionalGeneration

    torch.manual_seed(0)
    cfg = Qwen2_5_VLConfig(
        vocab_size=152064, hidden_size=64, intermediate_size=128, num_hidden_layers=2, num_attention_heads=4,
        num_key_value_heads=2, max_position_embeddings=4096, rope_scaling={"type": "mrope", "mrope_section": [2, 3, 3]},
        image_token_id=151655, video_token_id=151656, vision_start_token_id=151652, vision_end_token_id=151653,
        vision_config={"depth": 2, "hidden_size": 32, "intermediate_size": 64, "num_heads": 2, "out_hidden_size": 64,
                       "fullatt_block_indexes": [1]})
    base = Qwen2_5_VLForConditionalGeneration._from_config(cfg, attn_implementation="sdpa", torch_dtype=torch.float32)
    lora = LoraConfig(r=4, lora_alpha=8, task_type="CAUSAL_LM",
                      target_modules=r"^(?!.*visual).*\.(q_proj|k_proj|v_proj|o_proj|gate_proj|up_proj|down_proj)$")
    model = get_peft_model(base, lora)
    model.add_adapter("ref", lora)
    with torch.no_grad():
        for name, p in model.named_parameters():
            if "lora_B.default" in name:
                p.normal_(0, 0.05)
    model.set_adapter("default")
    return model.eval()


def full_logprobs(model, inputs, gen, mask):
    """The k x (prompt + response) forward that token_logprobs avoids."""
    import torch

    k, L = gen.shape[0], inputs["input_ids"].shape[1]
    out = model(input_ids=torch.cat([inputs["input_ids"].expand(k, -1), gen], 1),
                attention_mask=torch.cat([inputs["attention_mask"].expand(k, -1), mask.long()], 1),
                pixel_values=inputs["pixel_values"].repeat(k, 1), image_grid_thw=inputs["image_grid_thw"].repeat(k, 1))
    return out.logits[:, L - 1:-1].float().log_softmax(-1).gather(-1, gen[..., None]).squeeze(-1)


def check_policy() -> None:
    import torch
    from transformers import AutoProcessor

    model = tiny_policy()
    proc = AutoProcessor.from_pretrained(MODEL_ID, min_pixels=4 * 784, max_pixels=16 * 784)
    proc.tokenizer.padding_side = "left"
    pol = Policy(model, proc, chat(proc), file_names(SPLIT), EOS)
    ids = sorted(pol.names)[:3]
    # generation-time log-probs == training forward; nothing reshapes the sampler; the mask is the generated tokens
    inputs, gen, n, done, _, gen_lp, gap = rollout(pol, ids[0], 4, 6, True)
    lp, mask = token_logprobs(model, inputs, gen, n)
    guard_mask(gen, n, done, mask, EOS)
    logp_gap = float((lp - gen_lp)[mask.bool()].abs().max())
    assert gap < 1e-5 and logp_gap < 1e-4, (gap, logp_gap)
    # EOS first, in the middle and never: values and gradients equal the full-sequence forward
    gen = torch.tensor([[151645, 151643, 151643, 151643, 151643], [11, 12, 151645, 151643, 151643], [11, 12, 13, 14, 15]])
    n, done = response_lengths(gen, EOS)
    assert n.tolist() == [1, 3, 5] and done.tolist() == [True, True, False]
    lp, mask = token_logprobs(model, inputs, gen, n)
    guard_mask(gen, n, done, mask, EOS)
    (lp * mask).sum().backward()
    shared = {k: p.grad.clone() for k, p in model.named_parameters() if p.grad is not None}
    model.zero_grad()
    lf = full_logprobs(model, inputs, gen, mask)
    (lf * mask).sum().backward()
    assert torch.allclose(lp * mask, lf * mask, atol=1e-5), (lp * mask - lf * mask).abs().max()
    full = {k: p.grad for k, p in model.named_parameters() if p.grad is not None}
    assert shared.keys() == full.keys() and shared and all(".default." in k for k in shared)
    grad_gap = max(float((shared[k] - full[k]).abs().max() / full[k].abs().max()) for k in shared)
    assert grad_gap < 1e-4, grad_gap  # per tensor, relative to its scale: fp32 noise is ~1e-5
    # "ref" (zero B) is the base model; switching back leaves only the policy trainable
    with torch.no_grad():
        model.set_adapter("ref")
        ref_lp, _ = token_logprobs(model, inputs, gen, n)
        model.set_adapter("default")
        with model.disable_adapter():
            base_lp, _ = token_logprobs(model, inputs, gen, n)
    assert torch.allclose(ref_lp, base_lp, atol=1e-6) and not torch.allclose(ref_lp, lp.detach(), atol=1e-3)
    assert all(".default." in k for k, p in model.named_parameters() if p.requires_grad)
    # batched left-padded greedy (dev evaluation) == one image at a time
    one = {i: greedy(pol, [i], 1)[i] for i in ids}
    assert greedy(pol, ids, 3) == one, one
    # lm_head on the last position only changes no generated token
    batch = proc(text=[pol.text] * 2, images=[image(pol.names, i) for i in ids[:2]], padding=True, return_tensors="pt")
    with torch.no_grad():
        plain = model.generate(**batch, do_sample=False, max_new_tokens=6, eos_token_id=EOS)
        with last_position(model):
            hooked = model.generate(**batch, do_sample=False, max_new_tokens=6, eos_token_id=EOS)
    assert torch.equal(plain, hooked)
    step_gap = check_micro(pol, inputs, gen, n, done)
    print(f"tiny Qwen2.5-VL: logp gap {logp_gap:.2e}, sampler gap {gap:.2e}, shared vs full forward: "
          f"values {float((lp * mask - lf * mask).abs().max()):.2e}, grads {grad_gap:.2e} (relative), "
          f"{len(shared)} LoRA tensors; hooked generate == plain; --micro 2 vs unchunked step {step_gap:.2e}")


def check_micro(pol, inputs, gen, n, done) -> float:
    """update() with the k responses back-propagated 2 at a time takes the same SGD step as all at once."""
    import torch

    params = [p for p in pol.model.parameters() if p.requires_grad]
    start = [p.detach().clone() for p in params]
    group = {"inputs": inputs, "gen": gen, "n": n, "done": done, "gen_lp": None, "adv": np.array([0.7, -0.2, -0.5])}
    steps, stats = [], []
    for micro in (2, 3):
        with torch.no_grad():
            for p, p0 in zip(params, start):
                p.copy_(p0)
        pol.model.zero_grad(set_to_none=True)  # check_policy's own backward passes left gradients behind
        args = argparse.Namespace(beta=0.03, dry_run=True, micro=micro)
        stats.append(update(pol, torch.optim.SGD(params, lr=1.0), params, [group], args, first=True))
        steps.append([p.detach() - p0 for p, p0 in zip(params, start)])
    assert abs(stats[0]["grad_norm"] - stats[1]["grad_norm"]) < 1e-4 * stats[1]["grad_norm"], stats
    gap = max(float((a - b).abs().max() / b.abs().max()) for a, b in zip(*steps) if b.abs().max() > 0)
    assert gap < 1e-4, gap
    return gap


if __name__ == "__main__":
    check_loss()
    check_policy()
    print("test_train_rl ok")
    sys.exit(0)
