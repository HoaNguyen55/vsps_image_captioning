"""Batched greedy decoder stub (COMPUTE_PLAN §1, CC-501 Q13). Argument-checked; NOT run before the prereg commit.

Greedy (do_sample False, num_beams 1), left padding, batch 1 or 8. Q13 parity rule, fixed before the check runs:
on 50 KTVIC-test (dev) images, for EACH of S0, S1 and S2, every caption's token ids at batch 8 must equal batch 1;
any mismatch -> batch 1 for every system and every tier.
"""
from __future__ import annotations

SYSTEMS = ("S0", "S1", "S2")
PARITY_N = 50
PROMPTS = {"vi": "Mô tả chi tiết bức ảnh này bằng tiếng Việt."}  # build_dpo_data.PROMPT; the EN prompt is fixed in the run doc


def parity(tok_b1: dict[str, dict[str, list[int]]], tok_b8: dict[str, dict[str, list[int]]]) -> dict:
    """tok[system][image_id] = generated token ids. Returns {batch, mismatches}; batch 8 only if all 3 systems
    have exactly the same 50 images and token-equal outputs."""
    mism = {}
    for s in SYSTEMS:
        a, b = tok_b1.get(s, {}), tok_b8.get(s, {})
        if len(a) != PARITY_N or a.keys() != b.keys():
            mism[s] = "image set"
            continue
        bad = sorted(i for i in a if list(a[i]) != list(b[i]))
        if bad:
            mism[s] = bad
    return {"batch": 1 if mism else 8, "mismatches": mism}


def check(cfg: dict) -> dict:
    errs = []
    if cfg.get("system") not in SYSTEMS + ("A-1", "A-2", "A-3", "A-4"):
        errs.append("system")
    if cfg.get("batch") not in (1, 8):
        errs.append("batch must be 1 or 8")
    if cfg.get("batch") == 8 and not cfg.get("parity_passed"):
        errs.append("batch 8 needs the Q13 parity record")
    if cfg.get("lang") not in ("vi", "en"):
        errs.append("lang")
    if cfg.get("do_sample", False) or cfg.get("num_beams", 1) != 1:
        errs.append("greedy only")
    if errs:
        raise ValueError("REFUSED decode config: " + "; ".join(errs))
    return cfg


def run(cfg: dict):  # pragma: no cover - GPU host only, after the prereg commit
    check(cfg)
    import torch  # noqa: F401
    raise NotImplementedError("decoder: run on the host after the prereg commit")
