#!/usr/bin/env python
"""Policy side of CN-RLOO (scripts/train_rl.py): sampling, prompt-cache-shared log-probs, the clipped PG + k3 loss,
the loss-mask guard and evaluate.py-style greedy decoding. GPU at run time; scripts/test_train_rl.py checks it on CPU
with a tiny random Qwen2.5-VL.

The prompt (image + instruction, ~600 tokens) runs once per image and its KV cache serves the k responses, as in
generate(). lm_head runs on the last position only wherever the other positions are unused: Qwen2.5-VL's forward in
transformers 4.51 has no logits_to_keep, and fp32 logits for k x ~600 prompt positions are a 2.7 GB block (the 24.9 GB
reserved peak of the first 4-bit dry run). With --temperature T (the D1e fallback arm), logits are divided by T in the
sampler and in every log-prob, so the gradient and the KL are those of the distribution actually sampled.
"""
from __future__ import annotations

import sys
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from evaluate import KTVIC, PROMPTS, file_names  # noqa: E402
from rl_reward import SPLIT  # noqa: E402

GREEDY_MAX_NEW, CLIP = 160, 0.2  # evaluate.py's max_new_tokens; PPO ratio clip (B1)


@dataclass
class Policy:
    """The model and what every decoding call needs with it."""
    model: object
    proc: object
    text: str  # evaluate.py's short prompt in the chat template
    names: dict  # image id -> file name
    eos: list


def image(names: dict, image_id: str):
    from PIL import Image

    return Image.open(KTVIC / "images" / names[image_id]).convert("RGB")


def chat(proc) -> str:
    msg = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": PROMPTS["short"]}]}]
    return proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)


def policy(model, proc) -> Policy:
    e = model.generation_config.eos_token_id
    return Policy(model, proc, chat(proc), file_names(SPLIT), [e] if isinstance(e, int) else list(e))


def response_lengths(gen, eos: list[int]):
    """(tokens up to and including the first EOS, finished?) per row; a row without EOS was cut by max_new_tokens."""
    import torch

    hit = torch.isin(gen, torch.tensor(eos, device=gen.device))
    first = hit.int().argmax(1) + 1
    done = hit.any(1)
    return torch.where(done, first, torch.full_like(first, gen.shape[1])), done


@contextmanager
def last_position(model):
    """lm_head on the last position only, all that generate() and the prompt pass use."""
    hook = model.get_base_model().lm_head.register_forward_pre_hook(lambda _m, a: (a[0][:, -1:],))
    try:
        yield
    finally:
        hook.remove()


def rollout(pol: Policy, image_id: str, k: int, max_new: int, with_logp: bool = False, temperature: float = 1.0):
    """k samples from the policy itself (top_p 1, top_k 0, no repetition penalty); with_logp adds the
    generation-time log-probs of the sampled tokens and the largest gap between processed and raw next-token
    log-probs at this temperature (0 when nothing else reshapes the sampler)."""
    import torch

    inputs = pol.proc(text=[pol.text], images=[image(pol.names, image_id)], return_tensors="pt").to(pol.model.device)
    with torch.no_grad(), last_position(pol.model):
        out = pol.model.generate(**inputs, do_sample=True, temperature=temperature, top_p=1.0, top_k=0,
                                 repetition_penalty=1.0, num_return_sequences=k, max_new_tokens=max_new,
                                 eos_token_id=pol.eos, use_cache=True, return_dict_in_generate=True,
                                 output_logits=with_logp, output_scores=with_logp)
    gen = out.sequences[:, inputs["input_ids"].shape[1]:]
    n, done = response_lengths(gen, pol.eos)
    texts = [pol.proc.tokenizer.decode(g[:m], skip_special_tokens=True).strip() for g, m in zip(gen, n.tolist())]
    gen_lp = sampler_gap = None
    if with_logp:
        raw = (torch.stack(out.logits, 1).float() / temperature).log_softmax(-1)
        gen_lp = raw.gather(-1, gen[..., None]).squeeze(-1)
        sampler_gap = float((torch.stack(out.scores, 1).float().log_softmax(-1) - raw).abs().nan_to_num(0).max())
    return inputs, gen, n, done, texts, gen_lp, sampler_gap


def prompt_pass(model, inputs):
    """The prompt (image + instruction) once: the logits of its last position, which predict the first response
    token, and its KV cache."""
    with last_position(model):
        p = model(**inputs, use_cache=True)
    return p.logits, p.past_key_values


def response_logprobs(model, head, cache, inputs, gen, n, temperature: float = 1.0):
    """Log-probs of the responses `gen` after a prompt_pass, run as one continuation on a per-response copy of the
    prompt cache (the prompt graph itself is left for other chunks), and the loss mask: generated tokens up to and
    including the first EOS, nothing else."""
    import torch
    from transformers import DynamicCache

    k, T = gen.shape
    rep = DynamicCache()
    for i, (key, value) in enumerate(zip(cache.key_cache, cache.value_cache)):
        rep.update(key.repeat_interleave(k, 0), value.repeat_interleave(k, 0), i)
    L = inputs["input_ids"].shape[1]
    mask = torch.arange(T, device=gen.device)[None] < n[:, None]
    att = torch.cat([inputs["attention_mask"].expand(k, -1), mask.long()], 1)
    r = model(input_ids=gen, attention_mask=att, past_key_values=rep, use_cache=True,
              cache_position=torch.arange(L, L + T, device=gen.device))
    logits = torch.cat([head.expand(k, -1, -1), r.logits[:, :-1]], 1).float() / temperature
    return logits.gather(-1, gen[..., None]).squeeze(-1) - logits.logsumexp(-1), mask.float()


def token_logprobs(model, inputs, gen, n, temperature: float = 1.0):
    """Log-probs of the k responses under the active adapter (prompt run once), and the loss mask."""
    return response_logprobs(model, *prompt_pass(model, inputs), inputs, gen, n, temperature)


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


def greedy(pol: Policy, ids: list[str], batch: int) -> dict:
    """evaluate.py's decoding (greedy, 160 new tokens, the generation config's repetition penalty), batched with left
    padding: {image_id: (caption, finished)}."""
    import torch

    out = {}
    for s in range(0, len(ids), batch):
        chunk = ids[s:s + batch]
        inputs = pol.proc(text=[pol.text] * len(chunk), images=[image(pol.names, i) for i in chunk], padding=True,
                          return_tensors="pt").to(pol.model.device)
        with torch.no_grad(), last_position(pol.model):
            seqs = pol.model.generate(**inputs, do_sample=False, max_new_tokens=GREEDY_MAX_NEW, eos_token_id=pol.eos,
                                      use_cache=True)
        gen = seqs[:, inputs["input_ids"].shape[1]:]
        n, done = response_lengths(gen, pol.eos)
        for i, g, m, d in zip(chunk, gen, n.tolist(), done.tolist()):
            out[i] = (pol.proc.tokenizer.decode(g[:m], skip_special_tokens=True).strip(), d)
    return out
