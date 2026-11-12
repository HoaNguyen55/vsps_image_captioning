#!/usr/bin/env python3
"""A-CERT addendum VP (Paper A): Part V, a development re-computation of the certificate against a fuller gold on
COCO-5000, and Part P, its post hoc application to the released OPERA / "Less is More" comparisons.
Spec: manuscript/prereg/2026-11-11_a_cert/A_CERT_ADDENDUM_VP_v1_1.md (0e586fa9, commit bd7ef1c; it names this code
`a_cert_v.py`); rulings CC-335 and CC-336 Subject 1; A2 plan §1.3-1.5, §3.4-3.8 (cfea58d6). Code licence: CC-335
item (2), synthetic fixtures only until the one-judge code read.

  selftest --out F                       synthetic fixtures only (DEPS must exist on the host tree)
  v-freeze --selftest S --mutants M      label-free: no instance gold, no five-reference union, no G_top status
  v-score  --selftest S --mutants M      once, after the FREEZE_V pin line; v1.1 §12 step 5 fault rule
  p-fetch-check --logs DIR               the 25 pinned release files: size and git blob; prints their sha256
  p-score --logs DIR --gt-cache F --v-result F --selftest S --mutants M [--allow-gt-cache]
                                         POST HOC; gt_cache.json is refused without --allow-gt-cache (PI-1111i)
One audit hook guards every mode: label directories, sealed paths, the OC1 raw logs and gt_cache.json (without the
flag) are always refused; v-freeze refuses the instance gold; Part P refuses XM3600 / OC1 frozen inputs and writes only
under data/results/a_cert_p/.
Run: OMP_NUM_THREADS=2 nice -n 15 <venv python> -I -B scripts/a_cert/a_cert_vp.py <mode> ...
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import itertools
import json
import math
import os
import re
import shutil
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as Fr
from functools import partial
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import a_cert as ac  # noqa: E402
from a_cert import Fault, certify, committed, corner, delta_min, ols, pair_cells, sha, w_star, write_atomic  # noqa: E402

ROOT = ac.ROOT
SELF = "scripts/a_cert/a_cert_vp.py"
ADD = "manuscript/prereg/2026-11-11_a_cert/A_CERT_ADDENDUM_VP_v1_1.md"
LOG = ac.P_REAL["log"]
E1 = ".session_backup/2026-10-14/research_r10/E1/e1_chair_count.py"
E1V2 = ".session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json"
E1V2_SHA = "184f9ccac1b9a930e4b0f75d68d05fba43f41d855c76494eb3ebf58aa69c3591"
SYN = "data/coco_probe/chair_synonyms.txt"
VI = "data/coco_probe/coco80_vi.json"
IDS = "data/results/a_dchecks/freeze/coco5000_ids.txt"
INST = "data/results/a_dchecks/freeze/instance_gold_full5000.json"
INST_SHA = "bd36295146e505454f5110e817841d8300a024265c1f2cba2aade854119183f7"
KARPATHY = "data/datasets/karpathy/dataset_coco.json"

# §V.2 pins (A2 plan §2.1)
V_SHARDS = {
    "data/results/coco5000/distill-detailed.shard0of1.jsonl": "6453bfd5a2f7667d0cc879d3e4ca359553b9bda994760d227785da141ec001fd",
    "data/results/coco5000/distill-short.shard0of1.jsonl": "12ab5a6e2b707068a48f2247832bcd125559a291ea8f265946e9031d3ccef1b0",
    "data/results/coco5000/zeroshot-detailed.shard0of1.jsonl": "96e15f40cead64a993ff01ba2392857b1dae16155661ffddd7f2bac3af54365a",
    "data/results/coco5000/zeroshot-short.shard0of1.jsonl": "15ca56156796605c02397d13c60047bc6260d34ac65b8cc54f7651d71717feba",
    "data/results/coco_transfer_full5000/fuse2_s42-detailed.shard0of1.jsonl":
        "f205805a7ab12cbd93c9ef6e240772fff7ac237e559cae57916b6191c85ce257",
    "data/results/coco_transfer_full5000/fuse2_s42-short.shard0of1.jsonl":
        "cd947944d3cf578bbffdc40ca9ae920f9595511e9ee395f06585bcd1db6fbd2f",
    "data/results/coco_transfer_full5000/p1_s43-detailed.shard0of1.jsonl":
        "b12fbeb91e9023c2872db3b03724e7b9ecdfe264b1bb0a3928fb5e4028d1befd",
    "data/results/coco_transfer_full5000/p1_s43-short.shard0of1.jsonl":
        "b0dbbdc50af75a77fa3da2808018faf0b7c26b52db3a86fbdf333da601cfbb24",
    "data/results/coco5000_vcd/zeroshot-detailed.shard0of1.jsonl": "d6173e34823383202298ea7dc00afdd92604277a70bff5a9f1d93e1173396bbd",
}
V_IN = {**V_SHARDS, IDS: "d20da3dd48646d91a7ff7837c1c1f591d52c75e72921b2fd7f6854dc1093339f",
        KARPATHY: "2fd999220673258012acfb411a4e7e66af7d488050b2519b0badcc49b7600b8d",
        SYN: "b685537b36fe21b791c87151b96a991ceb582edff19f3da204dcc7a7905502f2",
        VI: "926e08571ef6e80a7f8aae8f2b73753d6c5c54c431a750ba2b67bfaae71b540b",
        "scripts/g2b/score_g2b.py": "66c665c7a71d3b97abbf89fd5bf13871910449ad1c053ff5fb0b18663e3e7ae5",
        "scripts/score_coco_probe.py": "d11db7e192f689980bb2b2bb717d852d9aa339ad857ce9411fe7bdd6fe416070"}

# §P.1 pinned release files: path under --logs -> (git blob, 12 hex; bytes). OPERA = shikiw/OPERA@e1bb7632508b,
# log/chair_eval_results/; less-is-more = yuezih/less-is-more@f26e187aadac, CHAIR-eval/data/
P_FILES = {f"OPERA/{p}": v for p, v in {
    "instructblip/beam5.jsonl": ("ab1ec53b09e6", 283122), "instructblip/greedy.jsonl": ("9d71c861dd33", 332619),
    "instructblip/ours.jsonl": ("bc94b6a680d6", 249114), "llava-1.5/beam5.jsonl": ("497f31742ae7", 256392),
    "llava-1.5/greedy.jsonl": ("31d15f027cce", 259599), "llava-1.5/ours.jsonl": ("37f4f4e04986", 249972),
    "minigpt4/beam5.jsonl": ("9ac5c7bb5dbf", 191640), "minigpt4/greedy.jsonl": ("fb9c19134273", 216771),
    "minigpt4/ours.jsonl": ("58fe578cc7b7", 167490), "shikra/beam5.jsonl": ("b79c8ad8a8b2", 257370),
    "shikra/greedy.jsonl": ("316f9faedb2d", 274452), "shikra/ours.jsonl": ("758dc7b0630b", 207744)}.items()}
P_FILES.update({f"less-is-more/{p}": v for p, v in {
    "Table1-results/r1-llava1.5-7b.jsonl": ("d1bb620af8eb", 351180), "Table1-results/r2-vcd.jsonl": ("96ea6e34275f", 344271),
    "Table1-results/r3-opera.jsonl": ("f152771e272a", 269160), "Table1-results/r4-opera-fast.jsonl": ("a87d1c7d8578", 261597),
    "Table1-results/r5-ours-inst.jsonl": ("72e0a15f278c", 305870), "Table1-results/r6-ours-cap.jsonl": ("72e0a15f278c", 305870),
    "Table1-results/r7-llava1.5-13b.jsonl": ("5968104f2b8d", 353597), "Table1-results/r8-ours-cap.jsonl": ("2142a538648c", 332205),
    "Table1-results/r9-llava-7b.jsonl": ("4bab4a2aa9d5", 251491), "Table1-results/r10-ours-cap.jsonl": ("1c1477d7e6ff", 224043),
    "Table1-results/r11-minigptv2.jsonl": ("04ee46f8d9fb", 235084), "Table1-results/r12-ours-cap.jsonl": ("5ff35e418e46", 180549),
    "chair-500.jsonl": ("8659bef29d46", 60390)}.items()})
FAM = {"F-A": [f"opera/instructblip__{d}" for d in ("greedy", "beam5", "ours")],
       "F-B": [f"opera/{m}__{d}" for m in ("llava-1.5", "minigpt4", "shikra") for d in ("greedy", "beam5", "ours")],
       "F-C": ["lim/" + s for s in ("r1-llava1.5-7b", "r2-vcd", "r3-opera", "r4-opera-fast", "r5-ours-inst",
                                    "r7-llava1.5-13b", "r8-ours-cap", "r9-llava-7b", "r10-ours-cap", "r11-minigptv2",
                                    "r12-ours-cap")]}
SYS24 = [*FAM["F-A"], *FAM["F-B"], *FAM["F-C"], "lim/r6-ours-cap"]
PUB15 = [(f"opera/{m}__ours", f"opera/{m}__{b}") for m in ("instructblip", "llava-1.5", "minigpt4", "shikra")
         for b in ("greedy", "beam5")] + [(f"lim/{x}", "lim/r1-llava1.5-7b") for x in ("r2-vcd", "r3-opera", "r4-opera-fast",
                                                                                     "r5-ours-inst")] + \
    [("lim/r8-ours-cap", "lim/r7-llava1.5-13b"), ("lim/r10-ours-cap", "lim/r9-llava-7b"),
     ("lim/r12-ours-cap", "lim/r11-minigptv2")]
GT_PREFIX = "f986f8ff"

# §V.3, §V.5, §V.6 constants
ALPHA_S, GRID, W0 = ac.ALPHA_S, ac.GRID, ac.W0
W0S = str(W0)
KS, R, B_BOOT = (1, 2, 3, 5), 20, 2000
SEED_REF = 20261114
SEED_MASK = 20261115
SEED_V3 = 20261116
SEED_K2 = 20261113
SEED_HALF = 20261111
U_HIDE = (0.30, 0.57)
V1_MIN_CERT, V1_MIN_PAIRS, V1_MIN_OTHER = 72, 5, 72
V1_ERR = Fr(1, 20)
V2_ALPHA = Fr(1, 40)
K2_GAIN = Fr(1, 20)
WFINE = tuple(j / 100 for j in range(1, 100))

# registered wording (checked verbatim against the addendum by the selftest)
V_LABEL = "development; outcome foreseeable from stored aggregates and an unreviewed calculation (disclosed)"
P_LABEL = "POST HOC; truth already scored by the paper"
P_FAMILY_LABEL = "post hoc; truth already scored by the paper; other model families"
METHODS_P = "POST HOC (released outputs the paper had already scored under the full gold)"
NOT_CERT_TAIL = "this does not say the published result is wrong"
REFUTED_I0 = "floor refuted by the instance labels"
V1_FAIL = ("the floor certificate at w0 made more than 5% errors on COCO-5000 against the fuller gold; it is withdrawn at "
           "that floor")
V2_REFUTED = ("on COCO-5000 the floor assumption fails at w0; the probability guarantee is not claimed there, and the error "
              "share of V1 is an empirical figure for one model family")
K2_SENT = "the certificate does not beat a margin ranking here"
V4A_SENT = ("from references alone, no precision order and no slope sign can be certified without an assumption on how "
            "often present objects are named.")
KV2_FLOOR, KV2_EMP = "the floor assumption failed on COCO-5000 at w0", "empirically valid on the sets tested"
NOT_VALIDATED = "was not validated"
VERBATIM = (V_LABEL, P_LABEL, P_FAMILY_LABEL, METHODS_P, NOT_CERT_TAIL, REFUTED_I0, V1_FAIL, V2_REFUTED, K2_SENT, V4A_SENT,
            KV2_FLOOR, KV2_EMP, NOT_VALIDATED)
KV_KEYS = ("KV0", "KV-EV", "KV1", "KV2", "KV3")
FORBIDDEN = ("wrong", "overturn", "unreliable", "fragile", "unsupported")
DROP_SENT = "Part P dropped: the matcher-identity gate failed (§P.2)"

RESCAP = tuple(f"rescap/{p}" for p in (
    "__init__.py", "chair.py", "metrics.py", "metrics_svp.py", "repro.py", "viz.py", "vocab.py", "pipeline/generate.py",
    "pipeline/realize.py", "pipeline/select.py", "pipeline/verify.py", "svp/__init__.py", "svp/entailment.py",
    "svp/matching.py", "vi/__init__.py", "vi/classifier.py", "vi/color.py", "vi/lexicon.py", "vlm/__init__.py",
    "vlm/base.py", "vlm/mock.py", "vlm/qwen_vl.py", "vlm/registry.py", "vlm/replay.py", "vlm/vintern.py"))
DEPS = (ac.SELF, "scripts/a_cert/a_cert_mutants.py", "scripts/g2b/score_g2b.py", "scripts/score_coco_probe.py",
        "scripts/xm3600_oiv7.py", "scripts/clean_supervision.py", "scripts/person_uncap.py", E1, SYN, VI, ADD, *RESCAP)

V_REAL = {"real": True, "out": "data/results/a_cert_v", "log": LOG, "ids": IDS, "systems": list(V_SHARDS), "inst": INST,
          "inst_sha": INST_SHA, "pins": V_IN}
P_REAL = {"real": True, "out": "data/results/a_cert_p", "log": LOG, "files": P_FILES, "gt_prefix": GT_PREFIX,
          "stored": E1V2, "stored_sha": E1V2_SHA}


# ------------------------------------------------------------------------------------------------ custody
MODE = {"m": "none", "gt": False, "w_ok": None}
P_MODES = ("p-fetch-check", "p-score")
P_DENY = ("/data/xm3600", "/datasets/xm3600", "xm3600_subset", "oiv7", "xm600", "/data/results/a_cert/", "a2_cpu_step")
WRITE_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC


def canon(path) -> str:
    return os.path.abspath(os.fsdecode(path)).replace(os.sep, "/").lower()


def blocked(path, write: bool = False) -> str | None:
    """The reason a path is refused in the current mode, or None."""
    low = canon(path)
    if ac.refused(os.path.abspath(os.fsdecode(path))):
        return "label or sealed path"
    if "a1_precheck/raw" in low:
        return "OC1 raw logs"
    if low.endswith("/gt_cache.json") and not (MODE["m"] == "p-score" and MODE["gt"]):
        return "gt_cache.json without --allow-gt-cache"
    if MODE["m"] == "v-freeze" and "instance_gold" in low:
        return "instance gold before the FREEZE_V pin"
    if MODE["m"] in P_MODES:
        if any(d in low for d in P_DENY):
            return "XM3600 / OC1 frozen input in Part P"
        ok = MODE["w_ok"]
        if write and not (ok and (low == ok or low.startswith(ok + "/"))):
            return "Part P writes only under its own output directory"
    return None


def _audit(event: str, args) -> None:
    pathlike = (str, bytes, os.PathLike)
    why = None
    if event == "open" and args and isinstance(args[0], pathlike):
        mode, flags = args[1] if len(args) > 1 else None, args[2] if len(args) > 2 else 0
        write = any(ch in mode for ch in "wax+") if isinstance(mode, str) else bool((flags or 0) & WRITE_FLAGS)
        why = blocked(args[0], write)
    elif event in ("os.listdir", "os.scandir") and args and isinstance(args[0], pathlike):
        why = blocked(args[0])
    elif event == "os.rename" and len(args) > 1:
        why = blocked(args[0], True) or blocked(args[1], True)
    elif event == "os.mkdir" and args and isinstance(args[0], pathlike):
        why = blocked(args[0], True)
    if why:
        raise Fault(f"custody: {why}")


# ------------------------------------------------------------------------------------------------ k-general budgets
def c_k(w, k):
    """Lemma B with k references (A2 plan §3.4): (1 - w)/(k w)."""
    return (1 - w) / (k * w)


def beta_Bk(cell: dict, w, a_s, k) -> float:
    """V-B (A2 plan §3.5) with c = c(w, k); equals a_cert.beta_B at k = 2."""
    c, f1, L = c_k(w, k), cell["f1"], math.log(2 / a_s)
    f1p = f1 + L + math.sqrt(L * L + 2 * L * f1)
    t = (1 + c) * L / 3
    return c * f1 + t + math.sqrt(t * t + 2 * c * (1 + c) * f1p * L)


def beta_Hk(cell: dict, w, a_s, k) -> float:
    """V-H (A2 plan §3.5, secondary) with c = c(w, k); a stored cell carries sz2 = sum_i |O_i|^2."""
    s2 = cell["sz2"] if "sz2" in cell else sum(s * s for s in cell["sz"])
    c = c_k(w, k)
    return c * cell["f1"] + (1 + c) * math.sqrt(0.5 * s2 * math.log(1 / a_s))


def beta_pb(cell: dict, w, a_s, use_i0: bool = True) -> float:
    """§P.3 P-b, k = 5: with use_i0 the cap is min(U, max(0, floor(beta) - I0)) (CC-335 N2); else min(U, floor(beta))."""
    b = beta_Bk(cell, w, a_s, 5)
    return max(0.0, b - cell["I0"]) if use_i0 else b


def pb_verdict(pc: dict, w, use_i0: bool = True, a_s=ALPHA_S) -> dict:
    """P-b at floor w. I0 > floor(beta) in any cell of the pair = floor refuted there: no certificate at that w."""
    if use_i0 and w > 0:
        bad = [c for c in "ABS" if pc[c]["I0"] > math.floor(beta_Bk(pc[c], w, a_s, 5))]
        if bad:
            return {"verdict": "NOT CERTIFIED", "better": None, "refuted_cells": bad}
    return {**certify(pc, w, a_s, partial(beta_pb, use_i0=use_i0)), "refuted_cells": []}


def pb_wstar(pc: dict, use_i0: bool = True, a_s=ALPHA_S):
    ws = w_star(pc, a_s, partial(beta_pb, use_i0=use_i0))
    if use_i0 and isinstance(ws, float) and ws > 0 and pb_verdict(pc, ws, True, a_s)["refuted_cells"]:
        return f"NI ({REFUTED_I0})"
    return ws


# ------------------------------------------------------------------------------------------------ golds and draws
def draws(n: int, k: int) -> np.ndarray:
    """§V.3: default_rng(20261114 + 100 k); R draws, each over the images in ascending id; choice(5, k) without
    replacement per image (stored sorted). Shape (R, n, k)."""
    rng = np.random.default_rng(SEED_REF + 100 * k)
    return np.array([[np.sort(rng.choice(5, k, replace=False)) for _ in range(n)] for _ in range(R)], dtype=np.int8)


def rung(refs_i: list, pick) -> dict:
    """Known present = named by at least one drawn reference; once = named by exactly one; no pair known absent."""
    if MODE["m"] == "v-freeze" and len(pick) >= len(refs_i):
        raise Fault("§V.7: the freeze formed an image's five-reference union")
    n = Counter(c for j in pick for c in refs_i[j])
    return {"kp": frozenset(n), "ka": frozenset(), "once": frozenset(c for c, v in n.items() if v == 1),
            "twice": frozenset()}


def top_gold(refs: list, inst: list) -> list:
    """G_top = classes named by any of the five references, union instance classes (§V.3)."""
    return [frozenset().union(*r[:5]) | i for r, i in zip(refs, inst)]


def prec(m: list, T: list, idx):
    n = sum(len(m[i]) for i in idx)
    return Fr(sum(len(m[i] & T[i]) for i in idx), n) if n else None


def right(p_better, p_worse) -> bool:
    """Truth of a unit: its direction holds under the truth gold; a tie is wrong (§V.3)."""
    return p_better is not None and p_worse is not None and p_better - p_worse > 0


def halves(n: int) -> list:
    perm = np.random.default_rng(SEED_HALF).permutation(n)
    return [np.sort(perm[: n // 2]), np.sort(perm[n // 2:])]


def digest(a) -> str:
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()


def fr(x):
    return Fr(*x) if x else None


def cluster_weights(n_pairs: int, seed: int) -> np.ndarray:
    """Pair-cluster bootstrap: per replicate, n_pairs pair draws with replacement (integers), as multiplicities."""
    rng = np.random.default_rng(seed)
    return np.array([np.bincount(rng.integers(0, n_pairs, n_pairs), minlength=n_pairs) for _ in range(B_BOOT)])


# ------------------------------------------------------------------------------------------------ verdict rules
def v1_declare(units: list) -> dict:
    """V1 evaluability (§V.5): >= 72 certified, from >= 5 pairs, >= 72 not certified; ABSTAIN / NOT DEFINED counted."""
    ce = [u for u in units if u["verdict"] == "CERTIFIED"]
    n_o = sum(u["verdict"] == "NOT CERTIFIED" for u in units)
    n_p = len({u["pair"] for u in ce})
    return {"n_cert": len(ce), "n_pairs_cert": n_p, "n_other": n_o, "n_excluded": len(units) - len(ce) - n_o,
            "evaluable": len(ce) >= V1_MIN_CERT and n_p >= V1_MIN_PAIRS and n_o >= V1_MIN_OTHER}


def v_rules(units: list, rt: list) -> dict:
    """V1 and V3 (§V.5) on units {pair, verdict}; rt[j] = unit j's direction holds under the truth."""
    dec = v1_declare(units)
    ce = [j for j, u in enumerate(units) if u["verdict"] == "CERTIFIED"]
    ot = [j for j, u in enumerate(units) if u["verdict"] == "NOT CERTIFIED"]
    fc = [j for j in ce if not rt[j]]
    e_c = Fr(len(fc), len(ce)) if ce else None
    e_n = Fr(sum(not rt[j] for j in ot), len(ot)) if ot else None
    n_p, f_p = Counter(units[j]["pair"] for j in ce), Counter(units[j]["pair"] for j in fc)
    major = sorted(p for p in n_p if 2 * f_p[p] > n_p[p])
    v1 = "NOT EVALUABLE" if not dec["evaluable"] else "PASS" if e_c <= V1_ERR and not major else "FAIL"
    pairs = sorted({u["pair"] for u in units})
    col = {p: q for q, p in enumerate(pairs)}
    M = np.zeros((len(pairs), 4))
    for j in ce + ot:
        q, o = col[units[j]["pair"]], 0 if units[j]["verdict"] == "CERTIFIED" else 2
        M[q, o] += 1
        M[q, o + 1] += not rt[j]
    G = cluster_weights(len(pairs), SEED_V3) @ M
    ok = (G[:, 0] > 0) & (G[:, 2] > 0)
    d = np.where(ok, G[:, 3] / np.where(ok, G[:, 2], 1) - G[:, 1] / np.where(ok, G[:, 0], 1), -1.0)
    ci = [float(x) for x in np.percentile(d, [2.5, 97.5])]
    disc = e_c is not None and e_n is not None and e_c < e_n and ci[0] > 0
    return {"V1": v1, "V3": "DISCRIMINATING" if disc else "NOT DISCRIMINATING", **dec,
            "n_cert_direction_fails": len(fc), "e_c": e_c, "e_n": e_n, "pairs_failing_in_most_certified_draws": major,
            "e_n_minus_e_c_ci95": ci, "n_replicates_empty_class": int((~ok).sum())}


def v2_rule(cells: list) -> dict:
    """V2 (§V.5): share of cells with x_top > floor(beta(cell; w0)); FLOOR SUPPORTED iff <= alpha_S = 0.025."""
    over = sum(x > fb for x, fb in cells)
    share = Fr(over, len(cells)) if cells else None
    lab = "FLOOR SUPPORTED" if share is not None and share <= V2_ALPHA else "FLOOR REFUTED"
    return {"label": lab, "n_cells": len(cells), "n_over_budget": over, "share": share}


def cov5(wrong, weights) -> Fr:
    """A2 plan §1.4: Cov@5% = max m/N over prefixes holding at most 5% wrong units (20 wrong <= m); 0 if none."""
    f = np.repeat(np.asarray(wrong, bool), np.asarray(weights, int))
    m = np.arange(1, len(f) + 1)
    ok = 20 * np.cumsum(f) <= m
    return Fr(int(m[ok].max()), len(f)) if ok.any() else Fr(0)


def k2_label(d, lb) -> str:
    """COCO K2: PASS iff Delta_cov >= 0.05 and the 5th bootstrap percentile is above 0 (Delta_cov <= 0 fails)."""
    return "PASS" if d >= K2_GAIN and lb > 0 else "NOT PASSED"


def k2_rule(rk: dict, wrong: np.ndarray, pair_of: np.ndarray) -> dict:
    """COCO K2 (§V.6 = A2 plan §1.4-1.5 K2) on the k = 2 units; rankings fixed at the freeze; seed 20261113."""
    def covs(wt):
        tot, N = int((wt * wrong).sum()), int(wt.sum())
        return {"B1": Fr(int(20 * tot <= N)), **{r: cov5(wrong[o], wt[o]) for r, o in rk.items()}}

    pt = covs(np.ones(len(wrong), int))
    d = pt["C"] - max(pt["B1"], pt["B2"], pt["B3"])
    ds = []
    for cnt in cluster_weights(int(pair_of.max()) + 1, SEED_K2):
        c = covs(cnt[pair_of])
        ds.append(float(c["C"] - max(c["B1"], c["B2"], c["B3"])))
    lb = float(np.percentile(ds, 5))
    return {"label": k2_label(d, lb), "Cov5": pt, "delta_cov": d, "LB_p5": lb,
            "note": "ABSTAIN / NOT DEFINED units sit last in every ranking and count as failing the truth"}


def rankings(u2: list) -> dict:
    """§V.6 orders of the k = 2 units (index = 20 pair + draw): C by w* ascending, NI last, ties |Delta| descending,
    then pair id (then draw); B2 by |Delta| descending; B3 by ln(n_A/n_B) descending, ties |Delta|. ABSTAIN last."""
    def key_c(j):
        u = u2[j]
        ws = math.inf if u["w_star"] in ("NI", None) else u["w_star"]
        return u["better"] is None, ws, -(fr(u["dabs"]) or 0), u["pair"], u["draw"]

    def key_b3(j):
        u = u2[j]
        ell = math.log(u["n_better"] / u["n_worse"]) if u["better"] is not None else -math.inf
        return u["better"] is None, -ell, -(fr(u["dabs"]) or 0), j

    J = range(len(u2))
    return {"C": sorted(J, key=key_c), "B2": sorted(J, key=lambda j: (u2[j]["better"] is None, -(fr(u2[j]["dabs"]) or 0), j)),
            "B3": sorted(J, key=key_b3)}


# ------------------------------------------------------------------------------------------------ Part V units
def unit_row(pc: dict, p: int, r: int, bB, bH) -> dict:
    vb = {str(x): certify(pc, x, ALPHA_S, bB) for x in GRID}
    bt = vb[W0S]["better"]
    a, b = ("B", "A") if bt == "B" else ("A", "B")
    d = abs(Fr(pc["tA"], pc["nA"]) - Fr(pc["tB"], pc["nB"])) if pc["nA"] and pc["nB"] else None
    return {"pair": p, "draw": r, "better": bt, "verdict": {x: v["verdict"] for x, v in vb.items()},
            "dmin": {x: None if v["dmin"] is None else float(v["dmin"]) for x, v in vb.items()},
            "vh": {str(x): certify(pc, x, ALPHA_S, bH)["verdict"] for x in GRID}, "w_star": w_star(pc, ALPHA_S, bB),
            "dabs": None if d is None else [d.numerator, d.denominator], "n_better": pc["n" + a], "n_worse": pc["n" + b],
            **{x: pc[x] for x in ("nA", "nB", "tA", "tB")},
            "cells": {c: {"U": pc[c]["U"], "f1": pc[c]["f1"], "sz2": sum(s * s for s in pc[c]["sz"])} for c in "ABS"}}


def fine_min(pc: dict, beta):
    """Smallest w of {0, 0.01, ..., 0.99} at which the unit is CERTIFIED (the certified set is an up-set in w)."""
    return next((x for x in (0.0, *WFINE) if certify(pc, x, ALPHA_S, beta)["verdict"] == "CERTIFIED"), None)


def units_at(w: dict, k: int, picks: np.ndarray, idx, fine: bool = False) -> list:
    """Every pair-draw at rung k on the images idx (label-free)."""
    pairs = list(itertools.combinations(w["sys"], 2))
    bB, bH = partial(beta_Bk, k=k), partial(beta_Hk, k=k)
    rows = []
    for r in range(R):
        gold = [rung(w["refs"][i], picks[r, i]) for i in range(len(w["ids"]))]
        for p, (A, B) in enumerate(pairs):
            pc = pair_cells(w["ms"], A, B, gold, idx)
            row = unit_row(pc, p, r, bB, bH)
            if fine:
                row["fmin_B"], row["fmin_H"] = fine_min(pc, bB), fine_min(pc, bH)
            rows.append(row)
    return sorted(rows, key=lambda u: (u["pair"], u["draw"]))


def v4a(rows: list) -> None:
    """§V.4a: any reference-only (positives-only) certificate at w = 0 is a code fault (v1.1 §12 fault rule)."""
    if any(u["verdict"]["0.0"] == "CERTIFIED" or u["vh"]["0.0"] == "CERTIFIED" or u["w_star"] == 0.0 or
           u.get("fmin_B") == 0.0 or u.get("fmin_H") == 0.0 for u in rows):
        raise Fault("§V.4a: a C-ref certificate at w = 0")


def power_of(us: list) -> dict:
    n = max(1, len(us))
    return {"n_units": len(us), **{b: {x: sum(u[key][x] == "CERTIFIED" for u in us) / n for x in map(str, GRID)}
                                   for b, key in (("V-B", "verdict"), ("V-H", "vh"))}}


def worse(u: dict) -> str:
    return "B" if u["better"] == "A" else "A"


def holds(u: dict, pairs: list, Pt: dict) -> bool:
    if u["better"] is None:
        return False
    A, B = pairs[u["pair"]]
    hi, lo = (A, B) if u["better"] == "A" else (B, A)
    return right(Pt[hi], Pt[lo])


def x_top(ms: dict, gold: list, A: str, B: str, better: str, T: list, idx) -> tuple:
    """Unknown pairs of the worse-only and the shared cell that are in the truth gold T."""
    a, b = (ms[A], ms[B]) if better == "A" else (ms[B], ms[A])
    xw = xs = 0
    for i in idx:
        kn = gold[i]["kp"] | gold[i]["ka"]
        xw += len(((b[i] - a[i]) - kn) & T[i])
        xs += len(((a[i] & b[i]) - kn) & T[i])
    return xw, xs


# ------------------------------------------------------------------------------------------------ Part V world
def _g2b():
    sys.path[:0] = [str(ROOT / "scripts/g2b")]
    import score_g2b
    return score_g2b


def load_world_v(P: dict) -> dict:
    """Label-free: outputs through score_g2b.MATCH['coco80']['vi'], the first five Karpathy references through
    score_coco_probe.en_classes (check_coco_full.py); never the instance gold (score_g2b.coco_context would load it)."""
    g = _g2b()
    ids = sorted(int(x) for x in Path(ROOT, P["ids"]).read_text(encoding="utf-8").split())
    if len(set(ids)) != len(ids):
        raise Fault("duplicate image ids")
    ms = {}
    for rel in P["systems"]:
        caps = {}
        for line in Path(ROOT, rel).read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                caps[int(r["cocoid"])] = r["caption"]
        if not set(ids) <= set(caps):
            raise Fault("an output misses image ids")
        ms[Path(rel).name.split(".shard")[0] + ("+vcd" if "coco5000_vcd" in rel else "")] = \
            [frozenset(g.MATCH["coco80"]["vi"](caps[i])) for i in ids]
    kr = g.karpathy_refs(set(ids))
    if any(len(kr.get(i, ())) < 5 for i in ids):
        raise Fault("an image without five Karpathy references")
    return {"ids": ids, "sys": sorted(ms), "ms": ms,
            "refs": [[frozenset(g.sc.en_classes(s, g.SYN)) for s in kr[i][:5]] for i in ids]}


def load_inst(P: dict, ids: list) -> list:
    p = Path(ROOT, P["inst"])
    if sha(p) != P["inst_sha"]:
        raise Fault("instance gold differs from its pin")
    g = {int(k): frozenset(v["coco"]) for k, v in json.loads(p.read_text(encoding="utf-8")).items()}
    if not set(ids) <= set(g):
        raise Fault("instance gold misses image ids")
    return [g[i] for i in ids]


def check_pins(P: dict) -> dict:
    out = {}
    for p, want in P["pins"].items():
        out[p] = sha(Path(ROOT, p))
        if want and out[p] != want:
            raise Fault(f"pin mismatch: {p}")
    return out


def code_pins() -> dict:
    return {p: sha(ROOT / p) for p in (SELF, *DEPS) if p.endswith(".py")}


def kv0(P: dict) -> dict:
    """KV0: a passing selftest and an all-killed mutant record for this exact script and a_cert.py."""
    if not P["real"] and P.get("kv0") is None:
        return {"KV0": "fixture run (records not checked)"}
    st, mu = (json.loads(Path(x).read_text(encoding="utf-8")) for x in P["kv0"])
    me, a = sha(Path(__file__)), sha(ROOT / ac.SELF)
    if not (st.get("pass") is True and st.get("script_sha256") == me and st.get("a_cert_sha256") == a):
        raise Fault("KV0: no passing selftest record for this script and a_cert.py")
    if not (mu.get("source_sha256") == me and mu.get("n", 0) > 0 and mu.get("killed") == mu.get("n")):
        raise Fault("KV0: not every mutant killed for this script")
    return {"selftest_sha256": sha(P["kv0"][0]), "mutants_sha256": sha(P["kv0"][1]), "a_cert_sha256": a}


# ------------------------------------------------------------------------------------------------ Part V freeze
def v_freeze_core(w: dict) -> dict:
    n = len(w["ids"])
    idx = np.arange(n)
    units, picks_sha, power = {}, {}, {}
    for k in (1, 2, 3):
        pk = draws(n, k)
        picks_sha[str(k)] = digest(pk)
        units[str(k)] = units_at(w, k, pk, idx)
        v4a(units[str(k)])
        power[str(k)] = power_of(units[str(k)])
    p2, hv = draws(n, 2), halves(n)
    hu = []
    for h in (0, 1):
        for row in units_at(w, 2, p2, hv[h], fine=True):
            hu.append({**row, "half": h})
    v4a(hu)
    u2 = units["2"]
    n_cert = sum(u["verdict"][W0S] == "CERTIFIED" for u in u2)
    nulls = ac.null_select([{"verdict": u["verdict"][W0S], "dabs": fr(u["dabs"]), "idx": j, "n_better": u["n_better"],
                             "n_worse": u["n_worse"]} for j, u in enumerate(u2)], n_cert)
    dec = v1_declare([{"pair": u["pair"], "verdict": u["verdict"][W0S]} for u in u2])
    return {"schema": "vsps.a_cert_vp.freeze_v.v1", "label": V_LABEL,
            "status": "label-free: no instance gold opened, no five-reference union formed, no G_top status",
            "constants": {"alpha_S": ALPHA_S, "grid": GRID, "w0": W0, "R": R, "k_in_freeze": [1, 2, 3], "B": B_BOOT,
                          "seeds": {"refs": "20261114 + 100 k", "mask": SEED_MASK, "V3": SEED_V3, "COCO K2": SEED_K2,
                                    "halves": SEED_HALF},
                          "V1": [V1_MIN_CERT, V1_MIN_PAIRS, V1_MIN_OTHER, str(V1_ERR)], "V2_alpha": str(V2_ALPHA)},
            "ids_sha256": digest(np.array(w["ids"], dtype=np.int64)), "picks_sha256": picks_sha,
            "halves_sha256": digest(np.concatenate(hv)), "systems": w["sys"], "units": units, "half_units": hu,
            "nulls_w0": nulls, "rank_k2": rankings(u2), "v1_declared": dec,
            "KV-EV": "V1 evaluable" if dec["evaluable"] else "V1 NOT EVALUABLE: Part V reports power only",
            "power": power}


# ------------------------------------------------------------------------------------------------ Part V score
def calibrate(hu: list, info: list, h: int, beta) -> float:
    """A2 plan §3.8 on half h: w0 = max{w in 0.01..0.99 : share of strata with x_top > floor(beta) <= alpha_S}, else 0."""
    st = []
    for u, (_, xw, xs) in zip(hu, info):
        if u["half"] == h and u["better"] is not None:
            st += [(xw, u["cells"][worse(u)]), (xs, u["cells"]["S"])]

    def exceed(wv):
        return Fr(sum(x > math.floor(beta(c, wv, ALPHA_S, 2)) for x, c in st), max(1, len(st)))

    return max((wv for wv in WFINE if exceed(wv) <= V2_ALPHA), default=0.0)


def at_floor(u: dict, w0: float, key: str) -> str:
    if u["better"] is None:
        return u["verdict"]["0.0"]
    return "CERTIFIED" if w0 > 0 and u[key] is not None and u[key] <= w0 else "NOT CERTIFIED"


def transported(hu: list, info: list) -> dict:
    """§V.6 secondary: the margin threshold read from one half against the truth (largest |Delta| of a unit whose
    direction fails; certify iff |Delta| > it), applied to the other half; tau_P = the larger of the two (Part P)."""
    ev = [(u, x[0]) for u, x in zip(hu, info) if u["better"] is not None]
    tau = [max((fr(u["dabs"]) for u, ok in ev if u["half"] == h and not ok), default=Fr(0)) for h in (0, 1)]
    rows = []
    for h in (0, 1):
        sel = [ok for u, ok in ev if u["half"] == h and fr(u["dabs"]) > tau[1 - h]]
        rows.append({"half": h, "tau_points": float(100 * tau[1 - h]), "n_certified": len(sel),
                     "n_direction_fails": sum(not s for s in sel)})
    tp = max(tau)
    return {"label": V_LABEL + "; secondary (transported margin threshold)", "by_half": rows,
            "tau_P": [tp.numerator, tp.denominator]}


def xfit(w: dict, fz: dict, T: list, golds2: list) -> dict:
    """Cross-fitted floor (A2 plan §3.8, two image halves, seed 20261111) and V1, V3 at it; secondary."""
    pairs = list(itertools.combinations(w["sys"], 2))
    hv = halves(len(w["ids"]))
    Pt = [{s: prec(w["ms"][s], T, hv[h]) for s in w["sys"]} for h in (0, 1)]
    hu, info = fz["half_units"], []
    for u in hu:
        xw = xs = None
        if u["better"] is not None:
            A, B = pairs[u["pair"]]
            xw, xs = x_top(w["ms"], golds2[u["draw"]], A, B, u["better"], T, hv[u["half"]])
        info.append((holds(u, pairs, Pt[u["half"]]), xw, xs))
    out = {"label": V_LABEL + "; secondary (cross-fitted floor)"}
    for bud, key, beta in (("V-B", "fmin_B", beta_Bk), ("V-H", "fmin_H", beta_Hk)):
        w0h = [calibrate(hu, info, 1 - h, beta) for h in (0, 1)]
        units = [{"pair": u["pair"], "verdict": at_floor(u, w0h[u["half"]], key)} for u in hu]
        out[bud] = {"w0_by_half": w0h, **v_rules(units, [x[0] for x in info])}
    out["transported_margin"] = transported(hu, info)
    return out


def hide_probs(r_cnt: np.ndarray, u: float, law: str) -> np.ndarray:
    """§V.3 M-label: uniform h = u; salience h = min(1, s/(1 + r)) with s set so that the mean is exactly u."""
    if law == "uniform":
        return np.full(len(r_cnt), u)
    base, lo, hi = 1 / (1 + r_cnt), 0.0, float((1 + r_cnt).max())
    for _ in range(200):
        s = (lo + hi) / 2
        lo, hi = (s, hi) if np.minimum(1, s * base).mean() < u else (lo, s)
    return np.minimum(1, hi * base)


def masks(r_cnt: np.ndarray):
    """default_rng(20261115); for u in (0.30, 0.57), law in (uniform, salience), draw 1..20: one uniform per
    system-named pair in (image ascending, class ascending) order; hidden iff the uniform < h."""
    rng = np.random.default_rng(SEED_MASK)
    for u in U_HIDE:
        for law in ("uniform", "salience"):
            h = hide_probs(r_cnt, u, law)
            for r in range(R):
                yield u, law, r, rng.random(len(r_cnt)) < h


def mlabel(w: dict, T: list) -> dict:
    """M-label power table, C-label at w = 0 (cap X = U); a certificate against the truth is a code fault: STOP."""
    pairs = list(itertools.combinations(w["sys"], 2))
    idx = range(len(w["ids"]))
    Pt = {s: prec(w["ms"][s], T, idx) for s in w["sys"]}
    named = [frozenset().union(*(w["ms"][s][i] for s in w["sys"])) for i in idx]
    cells = [(i, c) for i in idx for c in sorted(named[i])]
    r_cnt = np.array([sum(c in ref for ref in w["refs"][i][:5]) for i, c in cells], float)
    in_t = [c in T[i] for i, c in cells]
    out = {}
    for u, law, _, hid in masks(r_cnt):
        kp, ka = [set() for _ in idx], [set() for _ in idx]
        for (i, c), h, t in zip(cells, hid, in_t):
            if not h:
                (kp if t else ka)[i].add(c)
        gold = [{"kp": kp[i], "ka": ka[i], "once": frozenset(), "twice": frozenset()} for i in idx]
        row = out.setdefault(f"u={u} {law}", {"n_units": 0, "n_certified": 0})
        for A, B in pairs:
            v = certify(pair_cells(w["ms"], A, B, gold, idx), 0.0)
            row["n_units"] += 1
            if v["verdict"] == "CERTIFIED":
                hi, lo = (A, B) if v["better"] == "A" else (B, A)
                if not right(Pt[hi], Pt[lo]):
                    raise Fault("M-label certificate against the truth: STOP (code fault)")
                row["n_certified"] += 1
    for row in out.values():
        row["share_certified"] = row["n_certified"] / max(1, row["n_units"])
    return {"label": V_LABEL + "; secondary (M-label power table)", **out}


def truth_rows(w: dict, fz: dict, T: list, golds2: list) -> dict:
    """Every Part V row under one truth gold T; the certified set, orientation and rankings come from FREEZE_V."""
    pairs = list(itertools.combinations(w["sys"], 2))
    n = range(len(w["ids"]))
    Pt = {s: prec(w["ms"][s], T, n) for s in w["sys"]}
    u2 = fz["units"]["2"]
    rt = [holds(u, pairs, Pt) for u in u2]
    units = [{"pair": u["pair"], "verdict": u["verdict"][W0S]} for u in u2]
    cells, cell_rows = [], []
    for j, u in enumerate(u2):
        if u["better"] is None:
            continue
        A, B = pairs[u["pair"]]
        for name, cl, x in zip(("worse-only", "S"), (worse(u), "S"), x_top(w["ms"], golds2[u["draw"]], A, B, u["better"], T, n)):
            c = u["cells"][cl]
            fb = math.floor(beta_Bk(c, W0, ALPHA_S, 2))
            cells.append((x, fb))
            cell_rows.append({"label": V_LABEL, "unit": j, "cell": name, "x_top": x, "floor_beta_w0": fb, "f1": c["f1"],
                              "U": c["U"],
                              "w_hat": c["f1"] / (c["f1"] + 2 * x) if c["f1"] + x else None})
    pair_of = np.array([u["pair"] for u in u2])
    k2 = k2_rule({r: np.array(o) for r, o in fz["rank_k2"].items()}, np.array([not x for x in rt]), pair_of)
    table = []
    for p, (A, B) in enumerate(pairs):
        us = [u for u in u2 if u["pair"] == p]
        d = Pt[A] - Pt[B] if Pt[A] is not None and Pt[B] is not None else None
        table.append({"label": V_LABEL, "pair": p, "A": A, "B": B,
                      "share_certified_w0": sum(u["verdict"][W0S] == "CERTIFIED" for u in us) / max(1, len(us)),
                      "better_under_truth": None if d is None else "A" if d > 0 else "B" if d < 0 else "tie"})
    return {"label": V_LABEL, "V1_V3": v_rules(units, rt), "V2": {**v2_rule(cells), "cells": cell_rows}, "COCO K2": k2,
            "nulls_w0": {k: {"n": len(ix), "n_direction_fails": sum(not rt[j] for j in ix)}
                         for k, ix in fz["nulls_w0"].items()},
            "pair_table": table, "w_star_beside_truth": [{"label": V_LABEL, "unit": j, "w_star": u["w_star"], "holds": rt[j]}
                                                         for j, u in enumerate(u2)],
            "cross_fit": xfit(w, fz, T, golds2), "M_label": mlabel(w, T)}


def kv_block(reg: dict, evaluable: bool, k0: dict) -> dict:
    v1, v2 = reg.get("V1"), reg.get("V2")
    kv2 = "not triggered"
    if v2 == "FLOOR REFUTED":
        kv2 = f"V2 FLOOR REFUTED: the guarantee sentence of v1.1 §4.2 is printed with '{KV2_FLOOR}'" + \
            (f"; the certificate is described as '{KV2_EMP}'" if v1 == "PASS" else "")
    return {"KV0": {"status": "passed: selftest, mutants and pins checked before this run", **k0},
            "KV-EV": "V1 evaluable at the freeze" if evaluable else
            f"V1 NOT EVALUABLE at the freeze: Part V reports power only; the certificate {NOT_VALIDATED}",
            "KV1": "V1 FAIL: the floor w0 is withdrawn in the paper for every data set; Part P prints w* only"
            if v1 == "FAIL" else "not triggered",
            "KV2": kv2, "KV3": "no second fault (a second fault stops the analysis and goes to the PI)"}


def v_score_core(w: dict, fz: dict, P: dict, k0: dict) -> dict:
    n = len(w["ids"])
    picks = {k: draws(n, k) for k in KS}
    if {str(k): digest(picks[k]) for k in (1, 2, 3)} != fz["picks_sha256"] or \
            digest(np.concatenate(halves(n))) != fz["halves_sha256"] or w["sys"] != fz["systems"]:
        raise Fault("draws, halves or systems differ from FREEZE_V")
    u5 = units_at(w, 5, picks[5], np.arange(n))  # never in the freeze (§V.7); before the instance gold is opened
    v4a(u5)
    power = {"label": V_LABEL, "by_k": {**fz["power"], "5": power_of(u5)},
             "note": "k = 5 forms the five-reference union, which §V.7 bars from the freeze; computed in v-score before "
                     "the instance gold is opened"}
    head = {"schema": "vsps.a_cert_vp.v_result.v1", "label": V_LABEL, "power": power}
    dec = fz["v1_declared"]
    if not dec["evaluable"]:
        reg = {"V1": "NOT EVALUABLE", "V2": "not computed (KV-EV)", "V3": "not computed (KV-EV)",
               "COCO K2": "not computed (KV-EV)"}
        return {**head, "registered": reg, "KV": kv_block(reg, False, k0),
                "sentences": [f"the certificate {NOT_VALIDATED}", V4A_SENT]}
    golds2 = [[rung(w["refs"][i], picks[2][r, i]) for i in range(n)] for r in range(R)]
    inst = load_inst(P, w["ids"])
    top = top_gold(w["refs"], inst)
    prim, sec = truth_rows(w, fz, top, golds2), truth_rows(w, fz, inst, golds2)
    reg = {"V1": prim["V1_V3"]["V1"], "V2": prim["V2"]["label"], "V3": prim["V1_V3"]["V3"],
           "COCO K2": prim["COCO K2"]["label"]}
    sent = [s for s, on in ((V1_FAIL, reg["V1"] == "FAIL"), (V2_REFUTED, reg["V2"] == "FLOOR REFUTED"),
                            (K2_SENT, reg["COCO K2"] != "PASS"), (V4A_SENT, True)) if on]
    return {**head, "registered": reg, "KV": kv_block(reg, True, k0), "sentences": sent,
            "primary_truth_G_top": prim,
            "secondary_instance_only_truth": {**sec, "label": V_LABEL + "; secondary (instance-only truth)",
                                              "n_ref_named_pairs_not_in_instance_gold": sum(
                                                  len(frozenset().union(*r[:5]) - i) for r, i in zip(w["refs"], inst))},
            "transported_threshold": prim["cross_fit"]["transported_margin"]}


# ------------------------------------------------------------------------------------------------ modes: refusal, fault
def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def refuse_run(P: dict, target: Path) -> str | None:
    if target.exists():
        return "output exists (one pass only)"
    d = Path(ROOT, P["out"], "faults")
    prev = sorted(d.glob("FAULT_*.json")) if d.exists() else []
    if len(prev) >= 2:
        return "KV3: a second fault occurred; the analysis goes to the PI"
    if prev and json.loads(prev[-1].read_text(encoding="utf-8"))["script_sha256"] == sha(Path(__file__)):
        return "a rerun after a fault needs a fixed, re-pinned and code-read script (v1.1 §12 step 5)"
    return None


def fault(P: dict, e: BaseException) -> int:
    """v1.1 §12 step 5: no statistic is written or printed; only the exception type (marker for KV3)."""
    d = Path(ROOT, P["out"], "faults")
    n = len(list(d.glob("FAULT_*.json"))) + 1 if d.exists() else 1
    write_atomic(d / f"FAULT_{n}.json", {"utc": now(), "type": type(e).__name__, "script_sha256": sha(Path(__file__))})
    print(f"FAULT {type(e).__name__}")
    return 2


def v_freeze(P: dict, world_fn=None) -> int:
    MODE.update(m="v-freeze", gt=False, w_ok=None)
    out = Path(ROOT, P["out"], "freeze", "FREEZE_V.json")
    why = refuse_run(P, out)
    if why:
        print(f"REFUSED {why}")
        return 3
    try:
        if P["real"] and not (committed(SELF) and committed(ADD) and committed(ac.SELF)):
            raise Fault("a_cert_vp.py, a_cert.py and the addendum must equal their HEAD blobs")
        k0 = kv0(P)
        pins = check_pins(P)
        w = (world_fn or load_world_v)(P)
        fz = v_freeze_core(w)
        fz.update(pins=pins, code=code_pins(), kv0=k0, utc=now())
        json.dumps(fz, default=float)
    except BaseException as e:  # noqa: BLE001  (fault rule: exception type only)
        return fault(P, e)
    print(json.dumps({"wrote": str(out), "sha256": write_atomic(out, fz)}))
    return 0


def v_score(P: dict, world_fn=None) -> int:
    MODE.update(m="v-score", gt=False, w_ok=None)
    res = Path(ROOT, P["out"], "score", "A_CERT_V_RESULT.json")
    why = refuse_run(P, res)
    if why:
        print(f"REFUSED {why}")
        return 3
    try:
        fz, fsha = ac.pinned_freeze({"freeze": str(Path(P["out"], "freeze", "FREEZE_V.json")), "log": P["log"]})
        if P["real"] and not (committed(SELF) and committed(ADD) and committed(ac.SELF)):
            raise Fault("a_cert_vp.py, a_cert.py and the addendum must equal their HEAD blobs")
        k0 = kv0(P)
        if check_pins(P) != fz["pins"] or code_pins() != fz["code"]:
            raise Fault("inputs or code differ from FREEZE_V")
        w = (world_fn or load_world_v)(P)
        out = v_score_core(w, fz, P, k0)
        out["provenance"] = {"freeze_sha256": fsha, "script_sha256": sha(Path(__file__)), "utc": now()}
        json.dumps(out, default=float)
    except BaseException as e:  # noqa: BLE001
        return fault(P, e)
    print(json.dumps({"wrote": str(res), "sha256": write_atomic(res, out)}))
    return 0


# ------------------------------------------------------------------------------------------------ Part P
def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def fetch_check(P: dict) -> dict:
    """§P.1: each pinned file present with its byte size and git blob; sha256 printed for the fetch LOG line."""
    base, rows, ok = Path(P["logs"]), [], True
    for rel, (blob, size) in P["files"].items():
        f = base / rel
        data = f.read_bytes() if f.is_file() else None
        good = data is not None and len(data) == size and git_blob(data).startswith(blob)
        rows.append({"path": rel, "bytes": None if data is None else len(data), "blob12": blob,
                     "sha256": None if data is None else hashlib.sha256(data).hexdigest(), "ok": good})
        ok &= good
    extra = sorted(p.relative_to(base).as_posix() for p in base.rglob("*")
                   if p.is_file() and p.relative_to(base).as_posix() not in P["files"])
    return {"files": rows, "extra_files": extra, "all_ok": bool(ok and not extra)}


def _e1():
    """E1's CHAIR matcher (e1_chair_count.py parses sys.argv[1:6] and opens the synonyms at import; no zip opened)."""
    spec = importlib.util.spec_from_file_location("e1_chair_count", ROOT / E1)
    mod = importlib.util.module_from_spec(spec)
    argv = sys.argv[:]
    sys.argv = [str(ROOT / E1), str(ROOT / SYN), "", "", "", ""]
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.argv = argv
    return mod


def p_name(rel: str) -> str:
    top, rest = rel.split("/", 1)
    return "opera/" + rest[:-len(".jsonl")].replace("/", "__") if top == "OPERA" else "lim/" + Path(rest).stem


def p_world(P: dict) -> dict:
    """Captions as E1 / h3_n1.py load them; gt_cache.json as h3_n1.load_gt reads its cache (refs: every caption's
    class list in file order; inst: instance classes)."""
    caps = {}
    for rel in P["files"]:
        if rel.endswith("chair-500.jsonl"):
            continue
        rows = [json.loads(x) for x in Path(P["logs"], rel).read_text(encoding="utf-8").splitlines() if x.strip()]
        caps[p_name(rel)] = {int(r["image_id"]): r["caption"] for r in rows} if rel.startswith("OPERA/") else \
            {int(re.sub(r"\D", "", r["image_id"].split(".")[0])): r["text"] for r in rows}
    gc = json.loads(Path(P["gt_cache"]).read_text(encoding="utf-8"))
    return {"caps": caps, "refs": {int(k): [frozenset(s) for s in v] for k, v in gc["refs"].items()},
            "inst": {int(k): frozenset(v) for k, v in gc["inst"].items()}}


def matcher_gate(pw: dict, e1, stored: dict) -> dict:
    """§P.2: P_cls, M_cls and n_img of the 24 systems, by E1's own rule (images with instances; gold = instances
    and every reference), equal the stored rows of e1_x1pb_verification_v2.json to the printed precision."""
    rows, ok = {}, True
    for s in SYS24:
        caps = pw["caps"][s]
        keep = [i for i in caps if i in pw["inst"]]
        a = e1.agg([e1.per_image(caps[i], set(pw["inst"][i]).union(*pw["refs"][i])) for i in keep])
        got = {"P_cls": float(a["P_cls"]), "M_cls": float(a["M_cls"]), "n_img": len(keep)}
        want = {k: stored[s][k] for k in got}
        rows[s] = {"recomputed": got, "stored": want, "equal": got == want}
        ok = ok and got == want
    return {"label": P_LABEL, "systems": rows, "passed": ok}


def inter_idx(pw: dict, pos: dict, A: str, B: str) -> list:
    """B6: every pair statistic, certificate and truth uses the intersection of the two systems' image ids."""
    return [pos[i] for i in sorted(set(pw["caps"][A]) & set(pw["caps"][B]))]


def p_unit(ms: dict, A: str, B: str, gold: list, idx: list, k: int, r: int) -> dict:
    pc = pair_cells(ms, A, B, gold, idx)
    beta = partial(beta_Bk, k=k)
    v, ws = certify(pc, W0, ALPHA_S, beta), w_star(pc, ALPHA_S, beta)
    if ws == 0.0:
        raise Fault("§V.4a: a reference-only certificate at w = 0 (Part P)")
    d = abs(Fr(pc["tA"], pc["nA"]) - Fr(pc["tB"], pc["nB"])) if pc["nA"] and pc["nB"] else None
    return {"k": k, "draw": r, "verdict": v["verdict"], "better": {"A": A, "B": B}.get(v["better"]), "w_star": ws,
            "dabs": d}


def p_family(pw: dict, e1, fam: str, names: list, g0: int) -> tuple:
    """P-a on one released image set: M-ref of §V.3 (draws over the set's images in ascending id), every same-image
    pair on the intersection of its two systems' ids; truth = precision direction under G_top there."""
    ids = sorted(set().union(*(set(pw["caps"][s]) for s in names)))
    if any(len(pw["refs"].get(i, ())) < 5 for i in ids):
        raise Fault("an image without five references in gt_cache.json")
    pos = {i: j for j, i in enumerate(ids)}
    ms = {s: [frozenset(e1.nodes(pw["caps"][s][i])) if i in pw["caps"][s] else frozenset() for i in ids] for s in names}
    refs = [pw["refs"][i][:5] for i in ids]
    inst = [pw["inst"].get(i, frozenset()) for i in ids]
    top = top_gold(refs, inst)
    golds = {}
    for k in KS:
        pk = draws(len(ids), k)
        golds[k] = [[rung(refs[j], pk[r, j]) for j in range(len(ids))] for r in range(R)]
    rows = []
    for g, (A, B) in enumerate(itertools.combinations(names, 2), g0):
        idx = inter_idx(pw, pos, A, B)
        pa, pb = prec(ms[A], top, idx), prec(ms[B], top, idx)
        rows.append({"pair": g, "family": fam, "A": A, "B": B, "n_images": len(idx),
                     "chair_better": A if right(pa, pb) else B if right(pb, pa) else None,
                     "units": [p_unit(ms, A, B, golds[k][r], idx, k, r) for k in KS for r in range(R)]})
    return rows, {"ms": ms, "refs": refs, "inst": inst, "top": top, "pos": pos}


def med_w(us: list):
    vals = [math.inf if u["w_star"] == "NI" else u["w_star"] for u in us if u["w_star"] is not None]
    if not vals:
        return None
    m = float(np.median(vals))
    return "NI" if m == math.inf else m


def fmt(ws) -> str:
    return "not defined (tie)" if ws is None else ws if isinstance(ws, str) else f"{ws:.4f}"


def p_row(row: dict, method: str, base: str, k: int, kv1: bool, tau) -> dict:
    """One published comparison at k references, in the §P.4 wording (POST HOC label on every number)."""
    us = [u for u in row["units"] if u["k"] == k]
    ws, where = med_w(us), f"image set {row['family']} ({row['n_images']} images)"
    rec = {"label": P_LABEL, "comparison": f"{method} vs {base}", "k": k, "image_set": row["family"],
           "n_images": row["n_images"], "median_w_star": ws}
    if kv1:
        rec["sentence"] = f"with {k} references, the median break-down floor of this published comparison on {where} " \
                          f"is w* = {fmt(ws)}"
        return rec
    cm = sum(u["verdict"] == "CERTIFIED" and u["better"] == method for u in us)
    cb = sum(u["verdict"] == "CERTIFIED" and u["better"] == base for u in us)
    c, n = cm + cb, len(us)
    rec.update({"share_certified_w0": c / n, "n_certified_method_direction": cm, "n_certified_baseline_direction": cb,
                "n_certified_equal_to_chair_gold_direction": sum(
                    u["verdict"] == "CERTIFIED" and u["better"] == row["chair_better"] for u in us)})
    if tau is not None:
        rec["transported_margin_secondary"] = {"tau_points": float(100 * tau), "share_of_draws_above": sum(
            u["dabs"] is not None and u["dabs"] > tau for u in us) / n}
    state = f"certified in all {n} reference draws" if c == n else \
        f"not certified in any of the {n} reference draws" if c == 0 else \
        f"certified in {c} and not certified in {n - c} of the {n} reference draws"
    rec["sentence"] = f"with {k} references, the direction of this published comparison is {state} against gold " \
                      f"incompleteness at floor w0 = {W0} on {where}; its median break-down floor is w* = {fmt(ws)}" + \
                      ("" if c == n else f"; {NOT_CERT_TAIL}")
    return rec


def i0_cells(ms: dict, A: str, B: str, inst_only: list, idx: list) -> dict:
    a, b = ms[A], ms[B]
    return {"A": sum(len((a[i] - b[i]) & inst_only[i]) for i in idx),
            "B": sum(len((b[i] - a[i]) & inst_only[i]) for i in idx),
            "S": sum(len(a[i] & b[i] & inst_only[i]) for i in idx)}


def p_b_row(pw: dict, fw: dict, fam: str, method: str, base: str, kv1: bool) -> dict:
    """§P.3 P-b: known present = G_top, unknown = every other mention, k = 5; both caps printed (CC-335 N2)."""
    n5 = [Counter(c for r in rs for c in r) for rs in fw["refs"]]
    gold = [{"kp": t, "ka": frozenset(), "once": frozenset(c for c, v in m.items() if v == 1), "twice": frozenset()}
            for t, m in zip(fw["top"], n5)]
    inst_only = [i - frozenset(m) for i, m in zip(fw["inst"], n5)]
    idx = inter_idx(pw, fw["pos"], method, base)
    pc = pair_cells(fw["ms"], method, base, gold, idx)
    for c, v in i0_cells(fw["ms"], method, base, inst_only, idx).items():
        pc[c]["I0"] = v
    if certify(pc, 0.0)["verdict"] == "CERTIFIED":
        raise Fault("§V.4a: a positives-only P-b certificate at w = 0")
    vi, vp = pb_verdict(pc, W0), pb_verdict(pc, W0, False)
    wi, where = pb_wstar(pc), f"image set {fam} ({len(idx)} images)"
    rec = {"label": P_LABEL + "; secondary (P-b: the CHAIR gold itself, k = 5; no truth exists)",
           "comparison": f"{method} vs {base}", "image_set": fam, "n_images": len(idx),
           "I0_by_cell": {c: pc[c]["I0"] for c in "ABS"}, "w_star_cap_I0": wi, "w_star_cap_min_U_floor_beta": pb_wstar(pc, False)}
    if kv1:
        rec["sentence"] = f"with 5 references and the instance labels, the break-down floor of this published " \
                          f"comparison on {where} is w* = {fmt(wi)}"
        return rec
    cert = vi["verdict"] == "CERTIFIED"
    rec.update({"verdict_w0_cap_I0": vi["verdict"], "verdict_w0_cap_min_U_floor_beta": vp["verdict"],
                "certified_direction": {"A": method, "B": base}.get(vi["better"]) if cert else None,
                "cells_with_floor_refuted_at_w0": vi["refuted_cells"]})
    rec["sentence"] = f"with 5 references and the instance labels, the direction of this published comparison is " \
                      f"{'certified' if cert else 'not certified'} against gold incompleteness at floor w0 = {W0} on " \
                      f"{where}; its break-down floor is w* = {fmt(wi)}" + \
                      (f"; {REFUTED_I0} in cell(s) {', '.join(vi['refuted_cells'])} at w0" if vi["refuted_cells"] else "") + \
                      ("" if cert else f"; {NOT_CERT_TAIL}")
    return rec


def p_score_core(P: dict, e1, vres: dict) -> dict:
    pw = p_world(P)
    stored = json.loads(Path(ROOT, P["stored"]).read_text(encoding="utf-8"))["systems"]
    gate = matcher_gate(pw, e1, stored)
    head = {"schema": "vsps.a_cert_vp.p_result.v1", "label": P_LABEL, "methods_sentence": METHODS_P,
            "matcher_gate": gate}
    if not gate["passed"]:
        return {**head, "dropped": DROP_SENT}
    kv1 = vres.get("registered", {}).get("V1") == "FAIL"
    tp = (vres.get("transported_threshold") or {}).get("tau_P")
    tau = Fr(*tp) if tp and not kv1 else None
    rows, fw, g = [], {}, 0
    for fam, names in FAM.items():
        r, fw[fam] = p_family(pw, e1, fam, names, g)
        rows, g = rows + r, g + len(r)
    by = {frozenset((r["A"], r["B"])): r for r in rows}
    fam_of = {s: f for f, names in FAM.items() for s in names}
    pub = [p_row(by[frozenset(mb)], *mb, k, kv1, tau if k == 2 else None) for mb in PUB15 for k in KS]
    pb = [p_b_row(pw, fw[fam_of[m]], fam_of[m], m, b, kv1) for m, b in PUB15]
    same = {"label": P_FAMILY_LABEL, "n_pairs": len(rows),
            "pairs": [{"label": P_FAMILY_LABEL, "A": r["A"], "B": r["B"], "image_set": r["family"],
                       "n_images": r["n_images"], **{f"median_w_star_k{k}": med_w([u for u in r["units"] if u["k"] == k])
                                                     for k in KS},
                       **({} if kv1 else {f"share_certified_w0_k{k}": sum(
                           u["verdict"] == "CERTIFIED" for u in r["units"] if u["k"] == k) / R for k in KS})}
                      for r in rows]}
    if kv1:
        same["V1_V3"] = "not computed: KV1 (Part V V1 FAIL) withdraws the CERTIFIED labels at w0"
    else:
        u94 = [(r, u) for r in rows for u in r["units"] if u["k"] == 2]
        same["V1_V3"] = {"label": P_FAMILY_LABEL, "k": 2, "w0": W0, **v_rules(
            [{"pair": r["pair"], "verdict": u["verdict"]} for r, u in u94],
            [u["better"] is not None and u["better"] == r["chair_better"] for r, u in u94])}
    ns = [r["n_images"] for r in by.values() if (r["A"], r["B"]) in PUB15 or (r["B"], r["A"]) in PUB15]
    agg = [] if kv1 else [{"label": P_LABEL, "k": k, "text": (
        f"mean share of the {R} reference draws certified over the 15 published comparisons: "
        f"{np.mean([x['share_certified_w0'] for x in pub if x['k'] == k]):.3f} (k = {k}, w0 = {W0}, image sets F-A, F-B "
        f"and F-C as released, {min(ns)} to {max(ns)} images per comparison)")} for k in KS]
    return {**head, "KV1_w_star_only": kv1, "P_a": {"published": pub, "aggregate": agg, "same_image_pairs": same},
            "P_b": pb}


def p_score(P: dict) -> int:
    MODE.update(m="p-score", gt=bool(P.get("allow_gt")), w_ok=canon(Path(ROOT, P["out"])))
    res = Path(ROOT, P["out"], "score", "A_CERT_P_RESULT.json")
    why = "gt_cache.json needs --allow-gt-cache (PI-1111i)" if not P.get("allow_gt") else refuse_run(P, res)
    if why:
        print(f"REFUSED {why}")
        return 3
    try:
        if P["real"] and not (committed(SELF) and committed(ADD) and committed(ac.SELF)):
            raise Fault("a_cert_vp.py, a_cert.py and the addendum must equal their HEAD blobs")
        k0 = kv0(P)
        log = Path(ROOT, P["log"]).read_text(encoding="utf-8")
        vsha = sha(Path(ROOT, P["v_result"]))
        if "PI-1111i" not in log or vsha not in log:
            raise Fault("no PI-1111i line, or the Part V result is not pinned in the LOG")
        files = fetch_check(P)
        if not files["all_ok"] or any(f["sha256"] not in log for f in files["files"]):
            raise Fault("release files differ from their pins or from the fetch LOG line")
        if not sha(Path(P["gt_cache"])).startswith(P["gt_prefix"]) or sha(Path(ROOT, P["stored"])) != P["stored_sha"]:
            raise Fault("gt_cache.json or the stored E1 rows differ from their pins")
        out = p_score_core(P, _e1(), json.loads(Path(ROOT, P["v_result"]).read_text(encoding="utf-8")))
        out["provenance"] = {"v_result_sha256": vsha, "script_sha256": sha(Path(__file__)), "kv0": k0, "utc": now(),
                             "release_sha256": {f["path"]: f["sha256"] for f in files["files"]}}
        json.dumps(out, default=float)
    except BaseException as e:  # noqa: BLE001
        return fault(P, e)
    print(json.dumps({"wrote": str(res), "sha256": write_atomic(res, out)}))
    return 0


# ------------------------------------------------------------------------------------------------ selftest fixtures
def fixture_v(n: int = 60, tiers=("g", "t1", "t2")) -> tuple:
    """Deterministic world: 20 classes, 4 present per image, named by all five references (f1 = 0, so the k = 2 budget
    at w0 is 26). Tier g names the present classes, t1 adds one unknown absent class, t2 also one unknown class that
    the instance gold holds on even images; variant v adds 'zz' (instance-present, unreferenced) on images 0..v-1.
    Expected at k = 2, w0: the 27 cross-tier pairs CERTIFIED and right, the 9 within-tier pairs NOT CERTIFIED and
    failing under G_top, so V1 PASS (540 certified), V3 DISCRIMINATING, V2 FLOOR REFUTED."""
    true = [frozenset(f"c{(i + d) % 20:02d}" for d in range(4)) for i in range(n)]
    ms = {}
    for t in tiers:
        for v in range(3):
            ms[f"s_{t}_v{v}"] = [frozenset(true[i] | ({f"f{i % 7}"} if t != "g" else set()) |
                                           ({f"h{i % 5}"} if t == "t2" else set()) | ({"zz"} if i < v else set()))
                                 for i in range(n)]
    inst = [true[i] | ({f"h{i % 5}"} if i % 2 == 0 else set()) | ({"zz"} if i < 2 else set()) for i in range(n)]
    return {"ids": list(range(1, n + 1)), "sys": sorted(ms), "ms": ms, "refs": [[true[i]] * 5 for i in range(n)]}, inst


def fixture_p(tmp: Path, e1) -> dict:
    """Synthetic release logs in the pinned layout, a gt_cache.json, stored E1 rows and a LOG; opera/instructblip__beam5
    lacks images 1 and 2, so its pairs have 18 shared images and the others 20."""
    words, seen = [], set()
    for wd, c in sorted(e1.inv.items()):
        if wd.isalpha() and wd not in ("toilet", "seat") and c not in seen and e1.nodes(wd) == [c]:
            words.append(wd)
            seen.add(c)
    words = words[:30]
    fam_ids = {"F-A": range(1, 21), "F-B": range(101, 121), "F-C": range(201, 221)}
    logs, refs, inst, caps = tmp / "logs", {}, {}, {}
    for fam, names in FAM.items():
        for j, s in enumerate(names):
            caps[s] = {i: " and ".join([words[(i + d) % 10] for d in range(3)] +
                                        ([words[10 + (i + j) % 10]] if (i + j) % 3 == 0 else []) +
                                        ([words[20 + j % 10]] if j % 2 else []))
                       for i in fam_ids[fam] if not (s == "opera/instructblip__beam5" and i in (1, 2))}
        for i in fam_ids[fam]:
            t = [e1.inv[words[(i + d) % 10]] for d in range(3)]
            refs[i] = [[t[0]] + ([t[1]] if r % 2 == 0 else []) + ([t[2]] if r == 0 else []) for r in range(5)] + \
                ([[e1.inv[words[29]]]] if i % 2 == 0 else [])
            inst[i] = t + ([e1.inv[words[10]]] if i % 4 == 0 else [])
    caps["lim/r6-ours-cap"] = caps["lim/r5-ours-inst"]
    pins = {}
    for rel in P_FILES:
        f = logs / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        if rel.endswith("chair-500.jsonl"):
            rows = [{"image_id": i} for i in fam_ids["F-C"]]
        elif rel.startswith("OPERA/"):
            rows = [{"image_id": i, "caption": c} for i, c in caps[p_name(rel)].items()]
        else:
            rows = [{"image_id": f"{i}.jpg", "text": c} for i, c in caps[p_name(rel)].items()]
        f.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
        pins[rel] = (git_blob(f.read_bytes())[:12], f.stat().st_size)
    gt = tmp / "h3" / "gt_cache.json"
    write_gt(gt, json.dumps({"refs": {str(i): v for i, v in refs.items()}, "inst": {str(i): v for i, v in inst.items()}}))
    stored = {}
    for s in SYS24:
        keep = list(caps[s])
        a = e1.agg([e1.per_image(caps[s][i], set(inst[i]).union(*refs[i])) for i in keep])
        stored[s] = {"P_cls": float(a["P_cls"]), "M_cls": float(a["M_cls"]), "n_img": len(keep)}
    (tmp / "stored.json").write_text(json.dumps({"systems": stored}), encoding="utf-8")
    vres = {"PASS": tmp / "v_pass.json", "FAIL": tmp / "v_fail.json"}
    vres["PASS"].write_text(json.dumps({"registered": {"V1": "PASS"}, "transported_threshold": {"tau_P": [1, 50]}}),
                            encoding="utf-8")
    vres["FAIL"].write_text(json.dumps({"registered": {"V1": "FAIL"}}), encoding="utf-8")
    log = tmp / "LOG_P.md"
    log.write_text("".join(f"x OPS-fetch {hashlib.sha256((logs / r).read_bytes()).hexdigest()}\n" for r in P_FILES) +
                   f"x PI-1111i: yes\nx V {sha(vres['PASS'])}\nx V {sha(vres['FAIL'])}\n", encoding="utf-8")
    return {"real": False, "log": str(log), "files": pins, "logs": str(logs), "gt_cache": str(gt), "gt_prefix": "",
            "stored": str(tmp / "stored.json"), "stored_sha": sha(tmp / "stored.json"), "v_result": str(vres["PASS"]),
            "v_fail": str(vres["FAIL"]), "allow_gt": True, "kv0": None}


def write_gt(path: Path, text: str) -> None:
    """A synthetic gt_cache.json can only be written the way p-score may open one (flag on, own directory)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    MODE.update(m="p-score", gt=True, w_ok=canon(path.parent))
    try:
        path.write_text(text, encoding="utf-8")
    finally:
        MODE.update(m="selftest", gt=False, w_ok=None)


def quiet(fn, *a):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = fn(*a)
    MODE.update(m="selftest", gt=False, w_ok=None)
    return rc, buf.getvalue()


def keys_of(o) -> set:
    if isinstance(o, dict):
        return set(o) | set().union(*(keys_of(v) for v in o.values()))
    if isinstance(o, list):
        return set().union(*(keys_of(v) for v in o))
    return set()


# ------------------------------------------------------------------------------------------------ selftest checks
def _check_wording(ck: dict) -> None:
    txt = (ROOT / ADD).read_text(encoding="utf-8")
    missing = [s for s in VERBATIM if s not in txt]
    ck["wording_verbatim_in_addendum" + (f" (missing {missing})" if missing else "")] = not missing
    ck["KV_names_and_COCO_K2"] = KV_KEYS == ("KV0", "KV-EV", "KV1", "KV2", "KV3") and all(
        f"{k}:" in txt for k in KV_KEYS) and "**COCO K2**" in txt


def _check_math(ck: dict) -> None:
    E = 2.0  # alpha_S = 2 gives L = 0: the slack-0 budgets of A2 plan §3.10 (beta = c f1)
    cell = lambda U, f1=0, sz=(): {"U": U, "f1": f1, "sz": list(sz)}  # noqa: E731
    ck["c_k_general"] = abs(c_k(0.2, 2) - 2) < 1e-12 and abs(c_k(0.2, 1) - 4) < 1e-12 and abs(c_k(0.25, 5) - 0.6) < 1e-12
    ok = True
    for k in KS:
        for wv in (0.1, 0.2, 0.3, 0.5):
            p = np.linspace(wv, 0.999, 200)
            ratio = (1 - p) ** k / (k * p * (1 - p) ** (k - 1))
            ok &= bool(np.all(ratio <= c_k(wv, k) * (1 + 1e-12))) and abs(ratio[0] - c_k(wv, k)) < 1e-9
    ck["lemma_B_ratio_le_c_k_with_equality_at_w"] = ok
    cells = [cell(9, f, [1, 2, 3]) for f in (0, 3, 10)]
    ck["beta_k2_equals_a_cert"] = all(beta_Bk(c, x, ALPHA_S, 2) == ac.beta_B(c, x, ALPHA_S) and
                                      beta_Hk(c, x, ALPHA_S, 2) == ac.beta_H(c, x, ALPHA_S)
                                      for c in cells for x in (0.1, 0.2, 0.5))
    T1 = {"nA": 4, "tA": 3, "nB": 12, "tB": 5, "A": cell(1), "B": cell(7, 2), "S": cell(0)}
    T2 = {"nA": 10, "tA": 7, "nB": 20, "tB": 13, "A": cell(2), "B": cell(6, 2), "S": cell(1, 3)}
    ws = {k: w_star(T1, E, partial(beta_Bk, k=k)) for k in (1, 2, 5)}
    ck["toy_T1_w_star_k1_k2_k5"] = all(isinstance(x, float) for x in ws.values()) and 1 / 3 < ws[1] <= 1 / 3 + 1e-8 and \
        0.2 < ws[2] <= 0.2 + 1e-8 and 1 / 11 < ws[5] <= 1 / 11 + 1e-8 and ws[2] == ac.w_star(T1, E)
    r2 = certify(T2, 0.6, E, partial(beta_Bk, k=2))
    w2 = w_star(T2, E, partial(beta_Bk, k=2))
    ck["toy_T2_paired_+0.05_w_star_0.5"] = r2["verdict"] == "CERTIFIED" and r2["dmin"] == Fr(1, 20) and \
        isinstance(w2, float) and 0.5 < w2 <= 0.5 + 1e-8
    rng = np.random.default_rng(1)
    ok2 = ok4 = True
    for _ in range(300):
        uA, uB, uS = (int(x) for x in rng.integers(0, 4, 3))
        nA, nB = int(rng.integers(uA + uS + 1, 14)), int(rng.integers(uB + uS + 1, 14))
        tA, tB = int(rng.integers(0, nA - uA - uS + 1)), int(rng.integers(0, nB - uB - uS + 1))
        XB, XS = int(rng.integers(0, uB + 1)), int(rng.integers(0, uS + 1))
        en = min(Fr(tA + a + s, nA) - Fr(tB + b + s, nB) for a in range(uA + 1) for b in range(XB + 1) for s in range(XS + 1))
        ok2 &= en == delta_min(tA, nA, tB, nB, XB, XS)
        pc = {"nA": nA, "tA": tA, "nB": nB, "tB": tB, "A": cell(uA, 2), "B": cell(uB, int(rng.integers(0, 6))),
              "S": cell(uS, int(rng.integers(0, 6)))}
        if Fr(tA, nA) > Fr(tB, nB):
            for k in KS:
                d = [certify(pc, x, ALPHA_S, partial(beta_Bk, k=k))["dmin"] for x in (*GRID, 0.7, 1.0)]
                ok4 &= all(a <= b for a, b in zip(d, d[1:]))
    ck["closed_form_equals_enumeration_300"], ck["dmin_monotone_in_w_every_k"] = ok2, ok4
    ok3 = True
    for _ in range(50):
        x, lo = rng.normal(size=6), rng.normal(size=6)
        hi = lo + rng.random(6)
        en = [ols(x, np.where(np.array(b, bool), hi, lo)) for b in itertools.product((0, 1), repeat=6)]
        cmin, cmax = corner(x, lo, hi, ols)
        ok3 &= abs(cmin - min(en)) < 1e-12 and abs(cmax - max(en)) < 1e-12
    ck["corner_range_equals_enumeration"] = ok3
    se, ok5 = 2 * math.sqrt(ALPHA_S * (1 - ALPHA_S) / 2000), True
    for k in (1, 3, 5):
        for wv in (0.1, 0.2, 0.3):
            for law in ("point", "beta22"):
                p = np.full((2000, 300), wv) if law == "point" else wv + (1 - wv) * rng.beta(2, 2, (2000, 300))
                N = rng.binomial(k, p)
                x, f1 = (N == 0).sum(1), (N == 1).sum(1)
                ok5 &= np.mean([xx > beta_Bk({"f1": int(ff)}, wv, ALPHA_S, k) for xx, ff in zip(x, f1)]) <= ALPHA_S + se
    ck["size_simulation_beta_Bk_k1_k3_k5"] = bool(ok5)


def _check_v4(ck: dict) -> None:
    """§V.4 / §V.4a: with a positives-only gold, w = 0 certifies no pair and no slope sign; the freeze faults on one."""
    rng, ok, cls = np.random.default_rng(3), True, [f"c{j}" for j in range(8)]
    for _ in range(300):
        sub = lambda: frozenset(str(c) for c in rng.choice(cls, int(rng.integers(0, 5)), replace=False))  # noqa: E731
        refs = [[sub() for _ in range(5)] for _ in range(6)]
        ms = {"a": [sub() for _ in range(6)], "b": [sub() for _ in range(6)]}
        k = int(rng.integers(1, 6))
        gold = [rung(refs[i], sorted(rng.choice(5, k, replace=False))) for i in range(6)]
        v = certify(pair_cells(ms, "a", "b", gold, range(6)), 0.0)
        ok &= v["verdict"] != "CERTIFIED" and (v["dmin"] is None or v["dmin"] <= 0)
    ck["V4_identity_pairs_300"] = ok
    ok = True
    for _ in range(100):
        n = rng.integers(1, 30, 4)
        if len(set(n.tolist())) == 1:
            continue
        t = np.array([rng.integers(0, m + 1) for m in n])
        lo_, hi_ = corner(np.log(n), t / n, (t + (n - t)) / n, ols)
        ok &= lo_ <= 1e-12 and hi_ >= -1e-12
    ck["V4_identity_slopes_100"] = bool(ok)
    row = {"verdict": {"0.0": "CERTIFIED"}, "vh": {"0.0": "NOT CERTIFIED"}, "w_star": 0.0}
    clean = {"verdict": {"0.0": "NOT CERTIFIED"}, "vh": {"0.0": "NOT CERTIFIED"}, "w_star": "NI", "fmin_B": 0.3}
    try:
        v4a([clean, row])
        ck["V4a_fault_on_w0_certificate"] = False
    except Fault:
        ck["V4a_fault_on_w0_certificate"] = True
    v4a([clean])


def _check_golds(ck: dict) -> None:
    refs = [frozenset("ab"), frozenset("b"), frozenset("c"), frozenset("a"), frozenset("d")]
    g02, g01 = rung(refs, [0, 2]), rung(refs, [0, 1])
    ck["rung_known_present_from_drawn_only"] = g02["kp"] == frozenset("abc") and g02["once"] == frozenset("abc") and \
        g01["kp"] == frozenset("ab") and g01["once"] == frozenset("a") and not g02["ka"]
    MODE["m"] = "v-freeze"
    try:
        rung(refs, [0, 1, 2, 3, 4])
        ck["rung_guard_five_union_in_freeze"] = False
    except Fault:
        ck["rung_guard_five_union_in_freeze"] = True
    MODE["m"] = "v-score"
    ck["rung_five_union_allowed_in_score"] = rung(refs, [0, 1, 2, 3, 4])["kp"] == frozenset("abcd")
    MODE["m"] = "selftest"
    ck["top_gold_five_refs_and_instances"] = top_gold([[frozenset("a"), frozenset("b"), frozenset("c"), frozenset("d"),
                                                        frozenset("e"), frozenset("f")]], [frozenset("g")]) == \
        [frozenset("abcdeg")]
    ok = True
    for k, seed in ((1, 20261214), (2, 20261314), (3, 20261414), (5, 20261614)):
        rng = np.random.default_rng(seed)
        ok &= [[sorted(int(x) for x in rng.choice(5, k, replace=False)) for _ in range(3)] for _ in range(20)] == \
            draws(3, k).tolist()
    ck["reference_draws_seed_20261114_plus_100k"] = ok
    rng = np.random.default_rng(20261111)
    perm = rng.permutation(10)
    ck["halves_seed_20261111"] = [h.tolist() for h in halves(10)] == [sorted(perm[:5].tolist()), sorted(perm[5:].tolist())]
    r_cnt = np.array([0, 0, 1, 2, 5, 3, 0], float)
    rng, ok = np.random.default_rng(20261115), True
    got = list(masks(r_cnt))
    want = [(u, law, r, rng.random(7) < hide_probs(r_cnt, u, law)) for u in (0.30, 0.57) for law in ("uniform", "salience")
            for r in range(20)]
    ck["masking_seed_20261115_and_order"] = len(got) == 80 and all(
        a[:3] == b[:3] and np.array_equal(a[3], b[3]) for a, b in zip(got, want))
    h = hide_probs(r_cnt, 0.57, "salience")
    ck["salience_law_mean_u_capped_at_1"] = abs(h.mean() - 0.57) < 1e-9 and h.max() <= 1 and h[0] >= h[4] and \
        bool(np.all(hide_probs(r_cnt, 0.3, "uniform") == 0.3))
    ck["tie_is_wrong"] = right(Fr(1, 2), Fr(2, 4)) is False and right(Fr(3, 5), Fr(1, 2)) is True and \
        right(None, Fr(1, 2)) is False


def _units(spec: list) -> tuple:
    """spec: (pair, verdict, holds, count) rows -> units and truths."""
    us, rt = [], []
    for p, v, h, c in spec:
        us += [{"pair": p, "verdict": v}] * c
        rt += [h] * c
    return us, rt


def _check_rules(ck: dict) -> None:
    C, N = "CERTIFIED", "NOT CERTIFIED"
    other = [(10 + p, N, True, 10) for p in range(10)]

    def v1(spec):
        return v_rules(*_units(spec))["V1"]

    ck["V1_not_evaluable_71_certified"] = v1([(p, C, True, 8) for p in range(8)] + [(9, C, True, 7)] + other) == \
        "NOT EVALUABLE"
    ck["V1_not_evaluable_4_pairs"] = v1([(p, C, True, 20) for p in range(4)] + other) == "NOT EVALUABLE"
    ck["V1_not_evaluable_71_others"] = v1([(p, C, True, 8) for p in range(10)] + other[:7] + [(30, N, True, 1)]) == \
        "NOT EVALUABLE"
    ck["V1_evaluable_at_72_5_72"] = v_rules(*_units([(p, C, True, 18) for p in range(4)] + [(4, C, True, 0)] +
                                                    [(5, C, True, 0)]))["V1"] == "NOT EVALUABLE" and \
        v1([(p, C, True, 18) for p in range(3)] + [(3, C, True, 9), (4, C, True, 9)] + other[:7] + [(30, N, True, 2)]) == \
        "PASS"
    four = [(p, C, p >= 4, 8) for p in range(10)]
    ck["V1_pass_at_5_percent"] = v1([(p, C, True, 7) for p in range(4)] + [(p, C, False, 1) for p in range(4)] +
                                    [(p, C, True, 8) for p in range(4, 10)] + other) == "PASS"
    ck["V1_fail_above_5_percent"] = v1([(p, C, True, 7) for p in range(5)] + [(p, C, False, 1) for p in range(5)] +
                                       [(p, C, True, 8) for p in range(5, 10)] + other) == "FAIL" and v1(four + other) == "FAIL"
    ck["V1_fail_pair_wrong_in_most_draws"] = v1([(0, C, False, 2)] + [(p, C, True, 9) for p in range(1, 10)] + other) == "FAIL"
    ck["V1_pass_pair_wrong_in_half"] = v1([(0, C, False, 1), (0, C, True, 1)] + [(p, C, True, 9) for p in range(1, 10)] +
                                          other) == "PASS"
    r = v_rules(*_units([(p, C, True, 8) for p in range(10)] + [(p, "ABSTAIN", True, 1) for p in range(5)] + other))
    ck["V1_abstain_excluded_and_counted"] = r["n_excluded"] == 5 and r["n_cert"] == 80 and r["V1"] == "PASS"
    mixed = [(p, C, True, 8) for p in range(10)] + [(p, N, False, 3) for p in range(10)] + [(p, N, True, 7) for p in range(10)]
    r = v_rules(*_units(mixed))
    ck["V3_discriminating"] = r["V3"] == "DISCRIMINATING" and r["e_n"] == Fr(3, 10) and r["e_c"] == 0 and \
        abs(r["e_n_minus_e_c_ci95"][0] - 0.3) < 1e-12
    ck["V3_not_discriminating_when_e_n_le_e_c"] = v_rules(*_units([(p, C, True, 8) for p in range(10)] + other))["V3"] == \
        "NOT DISCRIMINATING"
    ok = True
    for n, seed, lit in ((36, SEED_V3, 20261116), (36, SEED_K2, 20261113)):
        rng = np.random.default_rng(lit)
        ok &= np.array_equal(cluster_weights(n, seed)[:5],
                             [np.bincount(rng.integers(0, n, n), minlength=n) for _ in range(5)])
    ck["bootstrap_seeds_V3_20261116_K2_20261113"] = ok
    ck["V2_boundary_one_in_40"] = v2_rule([(27, 26)] + [(0, 26)] * 39)["label"] == "FLOOR SUPPORTED" and \
        v2_rule([(27, 26)] * 2 + [(0, 26)] * 38)["label"] == "FLOOR REFUTED" and \
        v2_rule([(26, 26)] * 40)["label"] == "FLOOR SUPPORTED"
    one = np.ones(40, int)
    ck["cov5_by_hand"] = cov5([0] * 10 + [1] + [0] * 9 + [1] * 20, one) == Fr(1, 2) and \
        cov5([0] * 19 + [1] + [0] * 20, one) == 1 and cov5([1] + [0] * 39, one) == 1 and \
        cov5([1, 1] + [0] * 38, one) == Fr(1) and cov5([1] * 40, one) == 0 and \
        cov5([1, 0], [1, 19]) == 1 and cov5([1, 0], [2, 19]) == 0
    ck["COCO_K2_label_boundaries"] = [k2_label(Fr(1, 20), 0.01), k2_label(Fr(1, 20) - Fr(1, 10 ** 6), 0.01),
                                      k2_label(Fr(1, 5), 0.0), k2_label(Fr(0), 0.01)] == \
        ["PASS", "NOT PASSED", "NOT PASSED", "NOT PASSED"]
    u2 = [{"pair": p, "draw": 0, "better": b, "w_star": ws, "dabs": d, "n_better": nb, "n_worse": 10}
          for p, b, ws, d, nb in ((0, "A", 0.3, [1, 10], 12), (1, "B", "NI", [1, 2], 30), (2, "A", 0.1, [1, 20], 5),
                                  (3, "A", 0.1, [1, 5], 8), (4, None, None, [0, 1], 10))]
    rk = rankings(u2)
    ck["COCO_K2_rankings_C_B2_B3"] = rk == {"C": [3, 2, 0, 1, 4], "B2": [1, 3, 0, 2, 4], "B3": [1, 0, 3, 2, 4]}
    wrong, pair_of = np.array([False, True, False, False, True]), np.arange(5)
    k2 = k2_rule({r: np.array(o) for r, o in rk.items()}, wrong, pair_of)
    ck["COCO_K2_point_values"] = k2["Cov5"]["C"] == Fr(3, 5) and k2["Cov5"]["B2"] == 0 and k2["Cov5"]["B3"] == 0 and \
        k2["Cov5"]["B1"] == 0 and k2["delta_cov"] == Fr(3, 5)


def _check_pb(ck: dict) -> None:
    E = 2.0
    cl = lambda U, f1, i0: {"U": U, "f1": f1, "sz": [], "I0": i0}  # noqa: E731
    pc = {"nA": 10, "tA": 9, "nB": 14, "tB": 9, "A": cl(1, 0, 0), "B": cl(5, 20, 1), "S": cl(0, 0, 0)}
    ck["Pb_I0_cap_tighter_adds_certificate"] = pb_verdict(pc, 0.5, True, E)["verdict"] == "CERTIFIED" and \
        pb_verdict(pc, 0.5, False, E)["verdict"] == "NOT CERTIFIED" and certify(pc, 0.0)["verdict"] == "NOT CERTIFIED"
    wi, wp = pb_wstar(pc, True, E), pb_wstar(pc, False, E)
    ck["Pb_w_star_both_caps"] = isinstance(wi, float) and 4 / 9 < wi <= 4 / 9 + 1e-8 and isinstance(wp, float) and \
        0.5 < wp <= 0.5 + 1e-8
    bad = {**pc, "B": cl(5, 20, 5)}
    ck["Pb_floor_refuted_no_certificate"] = pb_verdict(bad, 0.5, True, E) == {"verdict": "NOT CERTIFIED", "better": None,
                                                                             "refuted_cells": ["B"]}
    refa = {**pc, "A": cl(1, 0, 1)}
    ck["Pb_refuted_any_cell_gives_NI"] = pb_wstar(refa, True, E) == f"NI ({REFUTED_I0})" and \
        pb_verdict(refa, 0.5, True, E)["refuted_cells"] == ["A"]
    ck["git_blob_known_values"] = git_blob(b"").startswith("e69de29bb2d1") and git_blob(b"hello\n").startswith("ce013625030b")


def _check_custody(ck: dict, tmp: Path) -> None:
    def refused(path, mode="r", m="selftest", gt=False, w_ok=None):
        MODE.update(m=m, gt=gt, w_ok=w_ok)
        try:
            with open(path, mode):
                pass
            return False
        except Fault:
            return True
        except OSError:
            return False
        finally:
            MODE.update(m="selftest", gt=False, w_ok=None)

    gtp = tmp / "cust" / "gt_cache.json"
    write_gt(gtp, "{}")
    ck["guard_label_dir"] = refused(tmp / "vsps_labels" / "x.jsonl") and refused(tmp / "vsps_labels" / "x", "w", "p-score")
    ck["guard_sealed_and_HBT1"] = blocked("/h/.vsps_sealed/a") is not None and \
        blocked("/r/.session_backup/machines/HBT1/x") is not None and blocked("/h/bpa1pull_1108/a") is not None
    ck["guard_OC1_raw_always"] = all(refused(tmp / "a1_precheck" / "raw" / "x.jsonl", "r", m) for m in
                                     ("selftest", "v-freeze", "v-score", "p-score"))
    ck["guard_gt_cache_needs_flag"] = refused(gtp) and refused(gtp, "r", "p-score") and \
        not refused(gtp, "r", "p-score", True) and refused(gtp, "r", "v-score", True)
    ip = tmp / "cust" / "instance_gold_full5000.json"
    ip.write_text("{}", encoding="utf-8")
    ck["guard_instance_gold_in_freeze_only"] = refused(ip, "r", "v-freeze") and not refused(ip, "r", "v-score")
    ok_dir = canon(tmp / "pout")
    ck["guard_P_refuses_XM3600_and_OC1_inputs"] = refused(tmp / "data/xm3600/oiv7_labels.json", "r", "p-score", True, ok_dir) \
        and refused(tmp / "data/results/a_cert/freeze/FREEZE.json", "r", "p-score", True, ok_dir)
    ck["guard_P_writes_only_under_its_output"] = refused(tmp / "elsewhere.json", "w", "p-score", True, ok_dir) and \
        not refused(tmp / "pout" / "x.json", "w", "p-score", True, ok_dir) and \
        not refused(tmp / "elsewhere.json", "r", "p-score", True, ok_dir)
    MODE.update(m="p-score", gt=True, w_ok=ok_dir)
    try:
        tempfile.mkstemp(dir=tmp / "cust")
        ck["guard_P_os_open_write_refused"] = False
    except Fault:
        ck["guard_P_os_open_write_refused"] = True
    finally:
        MODE.update(m="selftest", gt=False, w_ok=None)
    st, mu = tmp / "cust" / "st.json", tmp / "cust" / "mu.json"
    me = sha(Path(__file__))
    st.write_text(json.dumps({"pass": True, "script_sha256": me, "a_cert_sha256": sha(ROOT / ac.SELF)}), encoding="utf-8")
    mu.write_text(json.dumps({"source_sha256": me, "n": 3, "killed": 3}), encoding="utf-8")
    okk = "a_cert_sha256" in kv0({"real": True, "kv0": (st, mu)})
    mu.write_text(json.dumps({"source_sha256": me, "n": 3, "killed": 2}), encoding="utf-8")
    try:
        kv0({"real": True, "kv0": (st, mu)})
        ck["KV0_records_checked"] = False
    except Fault:
        ck["KV0_records_checked"] = okk


def _check_loader_v(ck: dict, tmp: Path) -> None:
    """The real Part V loader on tiny synthetic files (score_g2b.karpathy_refs with its ROOT pointed at the fixture)."""
    g = _g2b()
    terms = [t for t, _ in g.VI_TERMS[:40]]
    words = sorted(g.SYN)[:30]
    ids = [11, 7, 3]
    caps = {i: " và ".join(terms[(i + j) % 40] for j in range(3)) for i in ids}
    sents = {i: [f"a {words[(i + j) % 30]} near a {words[(i + 2 * j) % 30]}" for j in range(6)] for i in ids}
    root = tmp / "lv"
    shard = root / "data/results/coco5000/sx.shard0of1.jsonl"
    shard.parent.mkdir(parents=True)
    rows = {**caps, 99: terms[0]}  # id 99 is outside the id list: the loader must drop it
    shard.write_text("".join(json.dumps({"cocoid": i, "caption": rows[i]}) + "\n" for i in (7, 3, 99, 11)), encoding="utf-8")
    (root / "ids.txt").write_text("11\n7\n3\n", encoding="utf-8")
    kp = root / "data/datasets/karpathy/dataset_coco.json"
    kp.parent.mkdir(parents=True)

    def karpathy(n_sent):
        kp.write_text(json.dumps({"images": [{"filepath": "val2014", "sentences": [{"raw": s} for s in sents[i][:n_sent]],
                                              "cocoid": i} for i in ids]}), encoding="utf-8")

    karpathy(6)
    old, P = g.ROOT, {"ids": str(root / "ids.txt"), "systems": [str(shard)]}
    g.ROOT = root
    try:
        w = load_world_v(P)
        ck["loader_v_ids_sorted_and_named"] = w["ids"] == [3, 7, 11] and w["sys"] == ["sx"]
        ck["loader_v_mentions_by_id"] = all(w["ms"]["sx"][k] == g.MATCH["coco80"]["vi"](caps[i])
                                            for k, i in enumerate(w["ids"])) and any(w["ms"]["sx"])
        ck["loader_v_first_five_refs"] = all(w["refs"][k] == [g.sc.en_classes(s, g.SYN) for s in sents[i][:5]]
                                             for k, i in enumerate(w["ids"])) and any(any(r) for r in w["refs"])
        karpathy(4)
        try:
            load_world_v(P)
            ck["loader_v_refuses_four_references"] = False
        except Fault:
            ck["loader_v_refuses_four_references"] = True
        karpathy(6)
        (root / "ids.txt").write_text("11\n7\n3\n5\n", encoding="utf-8")
        try:
            load_world_v(P)
            ck["loader_v_refuses_missing_caption"] = False
        except Fault:
            ck["loader_v_refuses_missing_caption"] = True
    finally:
        g.ROOT = old


def _check_v_e2e(ck: dict, tmp: Path) -> None:
    w, inst = fixture_v()
    ip = tmp / "vinst" / "instance_gold_full5000.json"
    ip.parent.mkdir()
    ip.write_text(json.dumps({str(i): {"coco2014": "val2014", "coco": sorted(inst[k])} for k, i in enumerate(w["ids"])}),
                  encoding="utf-8")
    logp = tmp / "LOG_V.md"
    base = {"real": False, "log": str(logp), "inst": str(ip), "inst_sha": sha(ip), "pins": {}, "kv0": None}
    wf = lambda P: w  # noqa: E731
    P1 = {**base, "out": str(tmp / "v1")}
    rc, _ = quiet(v_freeze, P1, wf)
    fzp = tmp / "v1" / "freeze" / "FREEZE_V.json"
    fz = json.loads(fzp.read_text(encoding="utf-8")) if fzp.exists() else {}
    ck["V_freeze_runs_label_free"] = rc == 0 and fz.get("label") == V_LABEL
    dec = fz.get("v1_declared", {})
    ck["V_freeze_declares_evaluable_540_of_720"] = dec.get("evaluable") is True and dec.get("n_cert") == 540 and \
        dec.get("n_pairs_cert") == 27 and dec.get("n_other") == 180 and len(fz["units"]["2"]) == 720
    ck["V_freeze_holds_no_k5_and_nulls"] = sorted(fz.get("units", {})) == ["1", "2", "3"] and \
        set(fz.get("nulls_w0", {})) == {"constant", "margin", "length"} and len(fz.get("half_units", [])) == 1440
    logp.write_text("x no pin\n", encoding="utf-8")
    rc, so = quiet(v_score, P1, wf)
    ck["V_score_refuses_without_pin_no_statistic"] = rc == 2 and so == "FAULT Fault\n" and \
        not (tmp / "v1" / "score").exists()
    logp.write_text(f"x OPS-a-cert-vp-freeze FREEZE_V sha256 {sha(fzp)}\n", encoding="utf-8")
    rc, so = quiet(v_score, P1, wf)
    ck["V_rerun_after_fault_needs_fixed_script"] = rc == 3 and so.startswith("REFUSED")

    def score_copy(name, mutate=None, wf_=wf):
        d = tmp / name / "freeze"
        d.mkdir(parents=True)
        f = d / "FREEZE_V.json"
        z = json.loads(fzp.read_text(encoding="utf-8"))
        if mutate:
            mutate(z)
        f.write_text(json.dumps(z), encoding="utf-8")
        with open(logp, "a", encoding="utf-8") as fh:
            fh.write(f"x FREEZE_V sha256 {sha(f)}\n")
        rc_, so_ = quiet(v_score, {**base, "out": str(tmp / name)}, wf_)
        rp = tmp / name / "score" / "A_CERT_V_RESULT.json"
        return rc_, so_, json.loads(rp.read_text(encoding="utf-8")) if rp.exists() else {}

    rc, so, res = score_copy("v2")
    reg = res.get("registered", {})
    ck["V_score_valid_run_writes_once"] = rc == 0 and json.loads(so)["wrote"].endswith("A_CERT_V_RESULT.json")
    ck["V_fixture_V1_PASS_V3_DISCRIMINATING_V2_REFUTED"] = reg.get("V1") == "PASS" and \
        reg.get("V3") == "DISCRIMINATING" and reg.get("V2") == "FLOOR REFUTED" and \
        res["primary_truth_G_top"]["V1_V3"]["e_c"] == 0 and res["primary_truth_G_top"]["V1_V3"]["e_n"] == 1
    ck["V_result_KV_names_COCO_K2_no_bare_K2"] = set(res.get("KV", {})) == set(KV_KEYS) and "COCO K2" in reg and \
        "K2" not in keys_of(res)
    ck["V_result_labels_on_every_block"] = res.get("label") == V_LABEL and all(
        res[b]["label"].startswith(V_LABEL) for b in ("power", "primary_truth_G_top", "secondary_instance_only_truth",
                                                      "transported_threshold")) and \
        res["primary_truth_G_top"]["M_label"]["label"].startswith(V_LABEL) and \
        res["primary_truth_G_top"]["cross_fit"]["label"].startswith(V_LABEL)
    ck["V_k5_power_in_score_only"] = "5" in res.get("power", {}).get("by_k", {}) and "5" not in fz["power"]
    ml = [v for t in ("primary_truth_G_top", "secondary_instance_only_truth") for k, v in res[t]["M_label"].items()
          if k != "label"]
    ck["V_M_label_exact_no_STOP_and_power_printed"] = len(ml) == 8 and all(v["n_units"] == 720 for v in ml) and \
        any(v["n_certified"] > 0 for v in ml)
    ck["V_sentences_fixed"] = V2_REFUTED in res.get("sentences", []) and V4A_SENT in res["sentences"] and \
        V1_FAIL not in res["sentences"] and KV2_EMP in res["KV"]["KV2"]
    rc, so = quiet(v_score, {**base, "out": str(tmp / "v2")}, wf)
    ck["V_score_refuses_second_pass"] = rc == 3 and so.startswith("REFUSED")
    j = next(k for k, u in enumerate(fz["units"]["2"]) if u["verdict"][W0S] == "NOT CERTIFIED")

    def flip(z):
        z["units"]["2"][j]["verdict"][W0S] = "CERTIFIED"

    rc, _, res3 = score_copy("v3", flip)
    r3 = res3.get("primary_truth_G_top", {}).get("V1_V3", {})
    ck["V_certified_set_from_freeze"] = rc == 0 and r3.get("n_cert") == 541 and r3.get("V1") == "FAIL" and \
        res3["registered"]["V1"] == "FAIL" and V1_FAIL in res3["sentences"]
    rc, so, res4 = score_copy("v4", None, lambda P: 1 / 0)
    ck["V_fault_writes_and_prints_no_statistic"] = rc == 2 and so == "FAULT ZeroDivisionError\n" and not res4 and \
        (tmp / "v4" / "faults" / "FAULT_1.json").exists()
    flt = tmp / "v5" / "faults"
    flt.mkdir(parents=True)
    for n in (1, 2):
        (flt / f"FAULT_{n}.json").write_text(json.dumps({"script_sha256": "x"}), encoding="utf-8")
    rc, so = quiet(v_score, {**base, "out": str(tmp / "v5")}, wf)
    ck["V_KV3_second_fault_to_PI"] = rc == 3 and "KV3" in so
    wg, _ = fixture_v(tiers=("g",))
    Pg = {**base, "out": str(tmp / "vg"), "inst": str(tmp / "nowhere" / "instance_gold_full5000.json")}
    rc1, _ = quiet(v_freeze, Pg, lambda P: wg)
    fg = tmp / "vg" / "freeze" / "FREEZE_V.json"
    with open(logp, "a", encoding="utf-8") as fh:
        fh.write(f"x FREEZE_V sha256 {sha(fg) if fg.exists() else '-'}\n")
    rc2, _ = quiet(v_score, Pg, lambda P: wg)
    rg = tmp / "vg" / "score" / "A_CERT_V_RESULT.json"
    resg = json.loads(rg.read_text(encoding="utf-8")) if rg.exists() else {}
    ck["V_KV_EV_power_only_without_instance_gold"] = rc1 == 0 and rc2 == 0 and \
        resg.get("registered", {}).get("V1") == "NOT EVALUABLE" and "primary_truth_G_top" not in resg and \
        f"the certificate {NOT_VALIDATED}" in resg.get("sentences", [])


def _check_p_e2e(ck: dict, tmp: Path) -> None:
    e1 = _e1()
    P = fixture_p(tmp / "pf", e1)
    fc = fetch_check(P)
    bad = dict(P["files"])
    rel0 = next(iter(bad))
    bad[rel0] = ("000000000000", bad[rel0][1])
    ck["p_fetch_check_pins_and_mismatch"] = fc["all_ok"] and len(fc["files"]) == 25 and \
        not fetch_check({**P, "files": bad})["all_ok"]

    def run(name, **kw):
        Q = {**P, "out": str(tmp / name), **kw}
        rc_, so_ = quiet(p_score, Q)
        rp = tmp / name / "score" / "A_CERT_P_RESULT.json"
        return rc_, so_, json.loads(rp.read_text(encoding="utf-8")) if rp.exists() else {}

    rc, so, res = run("p1")
    ck["P_valid_run_writes_only_under_its_output"] = rc == 0 and json.loads(so)["wrote"].startswith(str(tmp / "p1"))
    pub, pb = res.get("P_a", {}).get("published", []), res.get("P_b", [])
    rows = pub + pb + res.get("P_a", {}).get("aggregate", []) + res.get("P_a", {}).get("same_image_pairs", {}).get("pairs", [])
    ck["P_rows_carry_POST_HOC_label"] = len(pub) == 60 and len(pb) == 15 and all(
        r["label"].startswith("POST HOC; truth already scored by the paper") for r in pub + pb) and \
        res.get("label") == "POST HOC; truth already scored by the paper" and \
        res["P_a"]["same_image_pairs"]["label"] == P_FAMILY_LABEL and all(r.get("label") for r in rows)
    sents = [r["sentence"] for r in pub + pb]
    ck["P_not_certified_always_followed_by_tail"] = all(s.endswith(NOT_CERT_TAIL) for s in sents if "not certified" in s) \
        and all("w0 = 0.2" in s and "image set" in s for s in sents)
    text = json.dumps(res).lower().replace(NOT_CERT_TAIL, "")
    ck["P_forbidden_words_absent"] = not any(f in text for f in FORBIDDEN)
    nimg = {(r["comparison"], r["k"]): r["n_images"] for r in pub}
    ck["P_pairs_on_intersection_of_ids"] = nimg.get(("opera/instructblip__ours vs opera/instructblip__beam5", 2)) == 18 and \
        nimg.get(("opera/instructblip__ours vs opera/instructblip__greedy", 2)) == 20 and \
        res["P_a"]["same_image_pairs"]["n_pairs"] == 94
    ck["P_aggregate_states_k_w0_set"] = all(f"k = {a['k']}, w0 = 0.2, image sets" in a["text"]
                                            for a in res["P_a"]["aggregate"]) and len(res["P_a"]["aggregate"]) == 4
    ck["P_matcher_gate_passes_on_identity"] = res.get("matcher_gate", {}).get("passed") is True and \
        len(res["matcher_gate"]["systems"]) == 24
    rc, _, res2 = run("p2", v_result=P["v_fail"])
    ck["P_KV1_prints_w_star_only"] = rc == 0 and res2.get("KV1_w_star_only") is True and not any(
        k in keys_of(res2) for k in ("share_certified_w0", "verdict_w0_cap_I0", "n_certified_method_direction")) and \
        isinstance(res2["P_a"]["same_image_pairs"]["V1_V3"], str) and not res2["P_a"]["aggregate"]
    st = json.loads(Path(P["stored"]).read_text(encoding="utf-8"))
    st["systems"]["lim/r6-ours-cap"]["P_cls"] += 0.01
    (tmp / "pf" / "stored_bad.json").write_text(json.dumps(st), encoding="utf-8")
    rc, _, res3 = run("p3", stored=str(tmp / "pf" / "stored_bad.json"), stored_sha=sha(tmp / "pf" / "stored_bad.json"))
    ck["P_matcher_gate_mismatch_drops_part_P"] = rc == 0 and res3.get("dropped") == DROP_SENT and "P_a" not in res3
    rc, so, _ = run("p4", allow_gt=False)
    ck["P_refuses_gt_cache_without_flag"] = rc == 3 and so.startswith("REFUSED") and not (tmp / "p4").exists()
    (Path(P["logs"]) / "extra.txt").write_text("x", encoding="utf-8")
    ck["p_fetch_check_refuses_extra_file"] = fetch_check(P)["extra_files"] == ["extra.txt"]


def selftest(out: Path) -> int:
    ck = {}
    MODE.update(m="selftest", gt=False, w_ok=None)
    missing = [p for p in DEPS if not (ROOT / p).exists()]
    ck["deps_present" + (f" (missing {missing})" if missing else "")] = not missing
    tmp = Path(tempfile.mkdtemp(prefix="a_cert_vp_selftest_"))
    groups = (_check_wording, _check_math, _check_v4, _check_golds, _check_rules, _check_pb,
              partial(_check_custody, tmp=tmp), partial(_check_loader_v, tmp=tmp), partial(_check_v_e2e, tmp=tmp),
              partial(_check_p_e2e, tmp=tmp))
    for fn in groups:
        try:
            fn(ck)
        except BaseException as e:  # noqa: BLE001  (a crash is a failed check, so a crashing mutant is caught)
            name = getattr(fn, "func", fn).__name__
            ck[f"{name}: no exception ({type(e).__name__}: {str(e)[:80]})"] = False
        finally:
            MODE.update(m="selftest", gt=False, w_ok=None)
    with contextlib.suppress(Exception):
        shutil.rmtree(tmp)
    ck = {k: bool(v) for k, v in ck.items()}
    rec = {"schema": "vsps.a_cert_vp.selftest.v1", "script_sha256": sha(Path(__file__)), "a_cert_sha256": sha(ROOT / ac.SELF),
           "checks": ck, "n": len(ck), "pass": all(ck.values())}
    Path(out).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print("\n".join(f"{'ok  ' if v else 'FAIL'} {k}" for k, v in ck.items()))
    print("selftest ok" if rec["pass"] else "selftest FAILED")
    return 0 if rec["pass"] else 1


# ------------------------------------------------------------------------------------------------ main
def main(argv: list) -> int:
    MODE.update(m=argv[0] if argv else "none", gt="--allow-gt-cache" in argv, w_ok=None)
    sys.addaudithook(_audit)
    for a in argv[1:]:
        why = blocked(a) if not a.startswith("--") else None
        if why:
            raise Fault(f"custody: {why} (argument)")
    ap = argparse.ArgumentParser(prog="a_cert_vp.py")
    sp = ap.add_subparsers(dest="mode", required=True)
    sp.add_parser("selftest").add_argument("--out", required=True)
    for m in ("v-freeze", "v-score"):
        s = sp.add_parser(m)
        s.add_argument("--selftest", required=True)
        s.add_argument("--mutants", required=True)
    sp.add_parser("p-fetch-check").add_argument("--logs", required=True)
    s = sp.add_parser("p-score")
    for x in ("--logs", "--gt-cache", "--v-result", "--selftest", "--mutants"):
        s.add_argument(x, required=True)
    s.add_argument("--allow-gt-cache", action="store_true")
    a = ap.parse_args(argv)
    if a.mode == "selftest":
        return selftest(Path(a.out))
    if a.mode in ("v-freeze", "v-score"):
        P = {**V_REAL, "kv0": (a.selftest, a.mutants)}
        return v_freeze(P) if a.mode == "v-freeze" else v_score(P)
    if a.mode == "p-fetch-check":
        r = fetch_check({**P_REAL, "logs": a.logs})
        print(json.dumps(r, indent=1))
        return 0 if r["all_ok"] else 1
    return p_score({**P_REAL, "logs": a.logs, "gt_cache": a.gt_cache, "v_result": a.v_result,
                    "allow_gt": a.allow_gt_cache, "kv0": (a.selftest, a.mutants)})


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
