"""LoRA SFT launcher stub (prereg §2, COMPUTE_PLAN §2): FAIR's scripts/train_stage2.py --stage sft, unchanged, with
max_steps = N_steps injected into its SFTConfig. Argument-checked here; NOT run before the prereg commit.

Fixed recipe: Qwen2.5-VL-7B-Instruct, 4-bit NF4 double-quant bf16 compute (train_stage2 --force-4bit), LoRA r 16,
alpha 32 (dropout 0.05 in train_stage2), lr 1e-4, batch 1 x grad-accum 8, 512 visual tokens, transformers 4.51.3,
seeds 42 (dev) / 42, 43, 44 (tiers 2-3), --loss-mask legacy (erratum E8). N_steps = optimiser steps of two epochs over S1's store
= 2 * floor(rows_S1 / 8) (all rows, detailed + short; the floor mirrors HF's steps-per-epoch).
"""
from __future__ import annotations

import sys

BASE = "Qwen/Qwen2.5-VL-7B-Instruct"
FIXED = {"lr": 1e-4, "grad_accum": 8, "lora_r": 16, "lora_alpha": 32, "vision_tokens": 512}
TRANSFORMERS = "4.51.3"
SEEDS = (42, 43, 44)
ARMS = ("S1", "S2", "A-1", "A-2", "A-3", "A-4")


def n_steps(rows_s1: int, epochs: int = 2, grad_accum: int = 8) -> int:
    if rows_s1 < grad_accum:
        raise ValueError("S1 store smaller than one optimiser step")
    return epochs * (rows_s1 // grad_accum)


def check(cfg: dict) -> dict:
    """Refuse any setting outside the registered recipe. cfg: arm, seed, data, out, steps, rows_s1, base_model,
    and the FIXED keys."""
    errs = []
    if cfg.get("arm") not in ARMS:
        errs.append(f"arm {cfg.get('arm')!r}")
    if cfg.get("seed") not in SEEDS:
        errs.append(f"seed {cfg.get('seed')!r}")
    if cfg.get("base_model", BASE) != BASE:
        errs.append("base model")
    errs += [f"{k}={cfg.get(k)!r} (fixed {v})" for k, v in FIXED.items() if cfg.get(k, v) != v]
    rows = cfg.get("rows_s1")
    if not isinstance(rows, int) or rows < FIXED["grad_accum"] or cfg.get("steps") != n_steps(rows):
        errs.append(f"steps {cfg.get('steps')} != N_steps({rows})")
    if not cfg.get("data") or not cfg.get("out"):
        errs.append("data/out")
    if errs:
        raise ValueError("REFUSED training config: " + "; ".join(errs))
    return cfg


def argv(cfg: dict) -> list[str]:
    """train_stage2.py arguments for one arm (epochs is ignored by HF once max_steps > 0)."""
    check(cfg)
    return ["train_stage2.py", "--stage", "sft", "--data", str(cfg["data"]), "--out", str(cfg["out"]),
            "--epochs", "2", "--lr", str(FIXED["lr"]), "--grad-accum", str(FIXED["grad_accum"]),
            "--lora-r", str(FIXED["lora_r"]), "--lora-alpha", str(FIXED["lora_alpha"]),
            "--vision-tokens", str(FIXED["vision_tokens"]), "--force-4bit", "--seed", str(cfg["seed"]),
            "--loss-mask", "legacy",
            "--base-model", BASE]


def launch(cfg: dict) -> int:  # pragma: no cover - GPU host only, after the prereg commit
    from . import repo

    repo()
    import transformers
    import trl

    if transformers.__version__ != TRANSFORMERS:
        raise SystemExit(f"FAULT transformers {transformers.__version__} != {TRANSFORMERS}")
    real = trl.SFTConfig

    def pinned(*a, **k):
        return real(*a, **{**k, "max_steps": cfg["steps"]})
    trl.SFTConfig = pinned
    import train_stage2

    sys.argv = argv(cfg)
    return train_stage2.main()
