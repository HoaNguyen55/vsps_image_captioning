#!/usr/bin/env python
"""Tier-3 S1 (T3.2): seed consensus over the three P1_dev seeds, a delta-space soup and a cross-seed MBR, on dev300.

Pre-registration: manuscript/prereg/2026-10-18_tier3_S1.{md,json} (the JSON's sha256 is pinned below). Instrument
addendum: manuscript/prereg/2026-10-18_tier3_S1_instrument.json. Job: scripts/queue/jobs/t3_2_s1_seed_consensus.sh.

    python scripts/seed_consensus.py --selftest                 # CPU: soup, MBR and gate on synthetic inputs
    python scripts/seed_consensus.py check --out O/check.json   # job start: prereg, code, inputs, base, machine
    python scripts/seed_consensus.py soup --runs $NCS_DATA/runs --report O/soup_selfcheck.json   # CPU only
    python scripts/seed_consensus.py mbr --dir O                # needs JAVA_HOME (RDRSegmenter worker)
    python scripts/seed_consensus.py gate --dir O               # needs JAVA_HOME

soup  PeftModel.add_weighted_adapter([s42, s43, s44], [1/3]*3, adapter_name='soup', combination_type='cat'): rank 48,
      alpha 48, so its update B A is the mean of the members' updates. It is built on a float32 stand-in host
      (lora_host): peft 0.21.2 gives a new adapter its base layer's dtype, so on the bf16 base the soup's factors would
      be bf16 and the registered float32 self-check could not hold (--selftest shows it failing there).
mbr   per image, the member caption a maximising sum over b != a of rl_reward.CiderD(c_a, [c_b]), document frequencies
      from the references of the 3,469 train-minus-dev300 images, RDRSegmenter words, ties to the lower seed. The
      members are the same-machine re-decode of s42 (procedure step 0), s43 and s44.
gate  D_v = mean over dev images of CIDEr_i(v) minus the members' mean CIDEr_i (x100, rl_report.dev_scores), with a
      paired bootstrap CI; dCHAIR_i in points; v is eligible iff D_v >= +1.0 and dCHAIR_i <= +1.0; PASS iff one is
      eligible (carried: the larger D_v, tie the soup), KILL otherwise. The thresholds are read from the registration.
Never overwrites an output: a JSON report that exists gets the next free _v2, _v3, ... name, and the soup and the MBR
captions, which later steps read by name, are refused. Writes numbers, hashes, adapters and the model's own captions
only, never a reference or panel caption.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from functools import reduce
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]

PREREG = ROOT / "manuscript/prereg/2026-10-18_tier3_S1.json"
PREREG_SHA256 = "e485da949cce2ee97fbc569c0b977549e0f55c56a91ca43d8356b87f15686bd2"  # committed in a68fb66
ADDENDUM = ROOT / "manuscript/prereg/2026-10-18_tier3_S1_instrument.json"
JOB_FILE = "scripts/queue/jobs/t3_2_s1_seed_consensus.sh"
PANEL = ROOT / "data/ktvic_openviic_refs.json"
N2_DECODE = ROOT / "data/results/rl/p1dev_s42-dev300-short.json"  # the registered n2 decode of p1dev_s42
N2_PREDS = ROOT / "data/results/rl/p1dev_s42-dev300-short.preds.json"
SPLITS = ("data/splits/ktvic_dev300.txt", "data/splits/ktvic_train_minus_dev300.txt")

MEMBERS = ("p1dev_s42", "p1dev_s43", "p1dev_s44")  # seed order: MBR ties go to the earlier one
SOUP = "p1dev_soup3_s42s43s44"
SOUP_CALL = "PeftModel.add_weighted_adapter([s42, s43, s44], [1/3]*3, adapter_name='soup', combination_type='cat')"
SEEDS, VARIANTS = ("s42", "s43", "s44"), ("soup", "mbr")
RESULT = {"s42": "p1dev_s42_redecode-dev300-short", "s43": "p1dev_s43-dev300-short", "s44": "p1dev_s44-dev300-short",
          "soup": f"{SOUP}-dev300-short", "mbr": "p1dev_mbr3-dev300-short"}
BOOT = {"seed": 0, "b": 2000}  # rl_reward.boot arguments; asserted against analysis.ci below
#: Registered inputs that only document where a number came from (the base's HF record, P1_dev's train runtime). They
#: live in the local session backup, not on the GPU machine; when present they must match.
PROVENANCE_ONLY = frozenset({".session_backup/2026-10-18/paperA_tasks/P3/hf_meta/qwen25vl7b.json",
                             ".session_backup/machines/n2/ncs-data/runs/p1dev_s42/metrics.jsonl"})
N2_NCS = ".session_backup/machines/n2/ncs-data/"
#: Values this code is written for, by key path in the registration; load_prereg() asserts every one.
REGISTERED = (
    (("job", "job_name"), "t3_2_s1_seed_consensus"),
    (("models", "member_s42", "adapter"), MEMBERS[0]),
    (("models", "soup", "name"), SOUP),
    (("models", "soup", "call"), SOUP_CALL),
    (("data", "test_split_read"), False),
    (("data", "panel", "path"), "data/ktvic_openviic_refs.json"),
    (("data", "splits", SPLITS[0], "n_images"), 300),
    (("data", "splits", SPLITS[1], "n_images"), 3469),
    (("data", "sft_rows", "rows"), 3469),
    (("data", "panel", "dev_images_with_panel"), 296),
    (("analysis", "ci", "B"), BOOT["b"]),
    (("analysis", "ci", "rng"), f"numpy default_rng({BOOT['seed']})"),
    (("analysis", "ci", "level"), "95%"),  # rl_reward.boot's 2.5 / 97.5 percentiles
    (("registered_before_output", "output_names"),
     ["p1dev_s43", "p1dev_s44", "p1dev_soup3", "p1dev_mbr3", "p1dev_s42_redecode", "t3_2_s1"]),
)


# ----------------------------------------------------------------------------------------------- shared
def sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 24), b""):
            h.update(block)
    return h.hexdigest()


def fresh(path: Path) -> Path:
    """`path`, or its first free `_v2`, `_v3`, ... sibling: an output that exists is never overwritten."""
    out, n = path, 2
    while out.exists():
        out, n = path.with_name(f"{path.stem}_v{n}{path.suffix}"), n + 1
    return out


def _jsonable(x):
    if isinstance(x, np.bool_):
        return bool(x)
    if isinstance(x, np.integer):
        return int(x)
    if isinstance(x, np.floating):
        return float(x)
    raise TypeError(f"not JSON-serialisable: {type(x).__name__}")


def write_json(path: Path, obj: dict) -> Path:
    out = fresh(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=_jsonable) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    return out


def load_prereg() -> dict:
    """The registration, refused unless byte-identical to the committed file, with every value in REGISTERED."""
    raw = PREREG.read_bytes()
    if hashlib.sha256(raw).hexdigest() != PREREG_SHA256:
        raise SystemExit(f"{PREREG} is not the committed registration (sha256 {PREREG_SHA256})")
    reg = json.loads(raw)
    wrong = [(path, want) for path, want in REGISTERED if reduce(lambda d, k: d[k], path, reg) != want]
    if wrong or set(reg["models"]["new_members"]) != set(MEMBERS[1:]):
        raise SystemExit(f"code and registration disagree: {wrong}")
    return reg


def provenance() -> dict:
    """machine_id, git_head_sha and the hook / train_stage2 sha256 (the committed hook's own record), plus this run."""
    from checkpoint_resume_hook import provenance_metadata

    meta = provenance_metadata(None)
    meta.update(script="scripts/seed_consensus.py", script_sha256=sha256(__file__), prereg_sha256=PREREG_SHA256,
                instrument_sha256=sha256(ADDENDUM) if ADDENDUM.is_file() else None,
                utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                env={k: os.environ.get(k) for k in ("NCS_DATA", "NCS_DATASET", "RESCAP_RAW_TONE", "HF_HUB_OFFLINE",
                                                     "CUDA_VISIBLE_DEVICES")})
    return meta


def split_ids(reg: dict) -> tuple[list[str], list[str]]:
    """(dev300 ids, train-minus-dev300 ids), sorted as strings, with the registered sizes and no overlap."""
    dev, rest = (sorted((ROOT / p).read_text(encoding="utf-8").split()) for p in SPLITS)
    n = [reg["data"]["splits"][p]["n_images"] for p in SPLITS]
    if [len(dev), len(rest)] != n or set(dev) & set(rest):
        raise SystemExit(f"split sizes {len(dev)}, {len(rest)} (registered {n}) or the splits overlap")
    return dev, rest


# ----------------------------------------------------------------------------------------------- check
def resolve(rel: str, ncs: Path) -> Path:
    """Where a registered input is read on this machine: NCS_DATA for the n2 backup's and data/datasets' copies."""
    if rel.startswith(N2_NCS):
        return ncs / rel[len(N2_NCS):]
    if rel.startswith("data/datasets/"):
        return ncs / rel[len("data/"):]
    return ROOT / rel


def _input_rows(reg: dict, ncs: Path) -> list[dict]:
    want = dict(reg["inputs_sha256"])
    want[f"{N2_NCS}runs/p1dev_s42/adapter_model.safetensors"] = reg["models"]["member_s42"]["adapter_sha256"]
    rows = []
    for rel, sha in sorted(want.items()):
        path = resolve(rel, ncs)
        if not path.is_file():
            rows.append({"check": f"input {rel}", "ok": rel in PROVENANCE_ONLY, "path": str(path), "status": "absent"})
            continue
        rows.append({"check": f"input {rel}", "ok": sha256(path) == sha, "path": str(path)})
    return rows


def _base_rows(base: dict) -> list[dict]:
    """The base loads from the HF cache (HF_HUB_OFFLINE=1): refs/main must be the registered revision, shards intact."""
    from huggingface_hub import constants

    repo = Path(constants.HF_HUB_CACHE) / f"models--{base['id'].replace('/', '--')}"
    main = repo / "refs" / "main"
    rev = main.read_text(encoding="utf-8").strip() if main.is_file() else None
    rows = [{"check": "base refs/main", "ok": rev == base["revision"], "refs_main": rev}]
    for name, sha in base["shards_sha256"].items():
        shard = repo / "snapshots" / base["revision"] / name
        rows.append({"check": f"base {name}", "ok": shard.is_file() and sha256(shard) == sha})
    return rows


def _instrument_rows(reg: dict) -> list[dict]:
    files = ["scripts/seed_consensus.py", JOB_FILE]
    add = json.loads(ADDENDUM.read_text(encoding="utf-8")) if ADDENDUM.is_file() else {}
    tracked = [PREREG, PREREG.with_suffix(".md"), ADDENDUM, *(ROOT / f for f in [*files, *reg["code_at_head"]])]
    rel = [str(p.relative_to(ROOT)) for p in tracked]
    in_git = subprocess.run(["git", "-C", str(ROOT), "ls-files", "--error-unmatch", *rel], capture_output=True)
    dirty = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--", *rel], capture_output=True,
                           text=True).stdout.strip()
    return [{"check": f"code_at_head {f}", "ok": sha256(ROOT / f) == s} for f, s in reg["code_at_head"].items()] + [
        {"check": "instrument addendum", "ok": add.get("prereg_sha256") == PREREG_SHA256
         and add.get("new_files") == {f: sha256(ROOT / f) for f in files} and add.get("deviations") == []},
        {"check": "committed and unmodified at HEAD", "ok": in_git.returncode == 0 and not dirty, "dirty": dirty}]


def _machine_rows(reg: dict, ncs: Path) -> list[dict]:
    import peft
    import torch
    import transformers
    from evaluate import KTVIC
    from train_stage2 import _vision_token_budget

    venv, host = reg["machines"]["venv"], socket.gethostname()
    gpu = torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
    have = {"torch": torch.__version__, "transformers": transformers.__version__, "peft": peft.__version__}
    return [{"check": "machine", "ok": host in (reg["machines"]["M1"], reg["machines"]["M2"]), "machine_id": host},
            {"check": "venv versions", "ok": all(venv[k] == v for k, v in have.items()), **have},
            {"check": "card rule gives P1_dev's 512 vision tokens, 4-bit", "gpu": gpu,
             "ok": gpu is not None and "RTX 3090" in gpu and _vision_token_budget() == (512, True)},
            {"check": "env", "ok": "NCS_DATASET" not in os.environ and os.environ.get("HF_HUB_OFFLINE") == "1"
             and KTVIC == ncs / "datasets" / "ktvic"}]


def check(reg: dict, out: Path) -> int:
    """Every registered constant (load_prereg), code and input sha256, the base snapshot and the machine, at start."""
    ncs = Path(os.environ["NCS_DATA"])
    rows = _instrument_rows(reg) + _input_rows(reg, ncs) + _base_rows(reg["models"]["base"]) + _machine_rows(reg, ncs)
    bad = [r["check"] for r in rows if not r["ok"]]
    write_json(out, {"pass": not bad, "failed": bad, "checks": rows, "provenance": provenance()})
    print("check PASS" if not bad else f"check FAIL: {bad}")
    return 1 if bad else 0


# ----------------------------------------------------------------------------------------------- soup
def _natural(path: str) -> tuple:
    return tuple((0, int(p), "") if p.isdigit() else (1, 0, p) for p in path.split("."))


def lora_host(factors: dict):
    """A float32 stand-in for the base model: one nn.Linear per LoRA target named in `factors` (a member's
    adapter_model.safetensors), shaped from its A and B, with a zero-stride weight that takes no memory, in the base's
    layer order. add_weighted_adapter never reads base weights; the host only fixes the dtype the soup is stored in."""
    import torch

    class Host(torch.nn.Module):
        def prepare_inputs_for_generation(self, *args, **kwargs):  # read by PeftModelForCausalLM; never called
            raise NotImplementedError

    host, pre = Host(), "base_model.model."
    for path in sorted({k[len(pre):].rsplit(".lora_", 1)[0] for k in factors}, key=_natural):
        a, b = factors[f"{pre}{path}.lora_A.weight"], factors[f"{pre}{path}.lora_B.weight"]
        layer = torch.nn.Linear(a.shape[1], b.shape[0], bias=False, device="meta")
        layer.weight = torch.nn.Parameter(torch.zeros((), dtype=torch.float32).expand(b.shape[0], a.shape[1]),
                                          requires_grad=False)
        *parents, leaf = path.split(".")
        node = host
        for name in parents:
            if name not in node._modules:
                node.add_module(name, torch.nn.Module())
            node = node._modules[name]
        node.add_module(leaf, layer)
    return host


def _assert_loaded(model, name: str, factors: dict) -> None:
    """Every factor in the member's file is in the model as saved: a silent load failure would leave zero-init B's,
    and the soup of those would still pass the registered self-check."""
    import torch

    params = dict(model.named_parameters())
    loaded = [params.get(k.removesuffix(".weight") + f".{name}.weight") for k in factors]
    same = [p is not None and torch.equal(p, t.to(p.dtype)) for p, t in zip(loaded, factors.values(), strict=True)]
    if not all(same) or sum(f".{name}." in k for k in params) != len(factors):
        raise SystemExit(f"{name}: {same.count(False)} of {len(factors)} factors not loaded as saved")


def build_soup(dirs: list[Path], host=None):
    """The registered soup of the adapters in `dirs` (their names are the adapter names) and its self-check rows."""
    from peft import PeftModel
    from safetensors.torch import load_file

    factors = [load_file(str(d / "adapter_model.safetensors")) for d in dirs]
    names = [d.name for d in dirs]
    model = PeftModel.from_pretrained(lora_host(factors[0]) if host is None else host, str(dirs[0]),
                                      adapter_name=names[0], torch_device="cpu")
    for d in dirs[1:]:
        model.load_adapter(str(d), adapter_name=d.name, torch_device="cpu")
    for name, f in zip(names, factors, strict=True):
        _assert_loaded(model, name, f)
    model.add_weighted_adapter(names, [1 / 3] * 3, adapter_name="soup", combination_type="cat")
    return model, soup_self_check(model, names)


def _soup_layers(model) -> list:
    """(name, LoRA layer) of every module the soup adapts, in the base's layer order."""
    from peft.tuners.lora import LoraLayer

    return [(n, m) for n, m in model.named_modules() if isinstance(m, LoraLayer) and "soup" in m.lora_A]


def soup_self_check(model, members: list[str]) -> list[dict]:
    """Registered: for the first and the last q_proj and down_proj, the soup's update equals the mean of the members'
    updates (torch.allclose, default tolerances, float32)."""
    import torch

    layers, rows = _soup_layers(model), []
    for proj in ("q_proj", "down_proj"):
        hits = [x for x in layers if x[0].endswith(f".{proj}")]
        for name, m in (hits[0], hits[-1]):
            soup = m.get_delta_weight("soup").float()
            mean = sum(m.get_delta_weight(a).float() for a in members) / len(members)
            rows.append({"module": name, "shape": list(soup.shape), "dtype": str(m.lora_A["soup"].weight.dtype),
                         "max_abs_diff": float((soup - mean).abs().max()),
                         "allclose": bool(torch.allclose(soup, mean))})
    return rows


def save_soup(model, out: Path) -> dict:
    """Save only the soup adapter at `out` (which must not exist) and check the file holds the checked factors."""
    import torch
    from safetensors.torch import load_file

    tmp = Path(tempfile.mkdtemp(prefix=f".{out.name}.", dir=out.parent))
    model.save_pretrained(str(tmp), selected_adapters=["soup"], save_embedding_layers=False)
    os.replace(tmp / "soup", out)
    shutil.rmtree(tmp)
    saved, params = load_file(str(out / "adapter_model.safetensors")), dict(model.named_parameters())
    same = all(torch.equal(params[k.removesuffix(".weight") + ".soup.weight"], t) for k, t in saved.items())
    if not same or len(saved) != sum(".soup." in k for k in params):
        raise SystemExit(f"{out}: the saved soup is not the checked one")
    cfg = json.loads((out / "adapter_config.json").read_text(encoding="utf-8"))
    return {"dir": str(out), "adapter_model_sha256": sha256(out / "adapter_model.safetensors"),
            "adapter_config_sha256": sha256(out / "adapter_config.json"), "r": cfg["r"],
            "lora_alpha": cfg["lora_alpha"], "base_model_name_or_path": cfg["base_model_name_or_path"],
            "n_tensors": len(saved), "saved_equals_checked": same}


def soup(reg: dict, runs: Path, report: Path) -> int:
    """Members' shas and LoRA configs against the registration, the soup and its self-check; saved only if it holds."""
    import peft

    lora, base = reg["models"]["member_s42"]["lora"], reg["models"]["base"]["id"]
    dirs = [runs / m for m in MEMBERS]
    cfgs = [json.loads((d / "adapter_config.json").read_text(encoding="utf-8")) for d in dirs]
    shas = {d.name: sha256(d / "adapter_model.safetensors") for d in dirs}
    bad = [d.name for d, c in zip(dirs, cfgs, strict=True)
           if {k: c[k] for k in lora} != lora or c["base_model_name_or_path"] != base]
    s42_ok = shas[MEMBERS[0]] == reg["models"]["member_s42"]["adapter_sha256"]
    if peft.__version__ != reg["models"]["soup"]["peft"] or not s42_ok or bad:
        raise SystemExit(f"peft {peft.__version__}, s42 sha {shas[MEMBERS[0]]}, configs off the recipe: {bad}")
    if (runs / SOUP).exists():  # the decode reads this path, so a second soup is refused rather than renamed
        raise SystemExit(f"{runs / SOUP} exists")
    model, rows = build_soup(dirs)
    ok = all(r["allclose"] for r in rows)
    rep = {"call": SOUP_CALL, "rule": reg["models"]["soup"]["self_check"], "self_check": rows, "self_check_pass": ok,
           "members_adapter_sha256": shas, "host": "float32 stand-in (lora_host), zero-stride base weights",
           "peft": peft.__version__, "soup": save_soup(model, runs / SOUP) if ok else None,
           "provenance": provenance()}
    write_json(report, rep)
    print(f"soup self-check {'PASS' if ok else 'FAIL'}: {[(r['module'], r['max_abs_diff']) for r in rows]}")
    return 0 if ok else 1


# ----------------------------------------------------------------------------------------------- mbr
def medoid(toks: list[list[str]], cider) -> int:
    """argmax over a of the sum over b != a of CIDEr-D(c_a, [c_b]); np.argmax keeps the first maximum (lower seed)."""
    util = [sum(cider.score(c, [o]) for j, o in enumerate(toks) if j != k) for k, c in enumerate(toks)]
    return int(np.argmax(util))


def mbr(reg: dict, d: Path) -> int:
    """MBR captions of the three members from their evaluate.py dev results; the selection reads no dev reference."""
    from rl_report import _dev_reward, _preds
    from rl_reward import CiderD

    dev, rest = split_ids(reg)
    preds = d / f"{RESULT['mbr']}.preds.json"
    if preds.exists():  # evaluate.py scores this path, so a second selection is refused rather than renamed
        raise SystemExit(f"{preds} exists")
    caps = {s: _preds(str(d / f"{RESULT[s]}.json")) for s in SEEDS}
    if any(sorted(c) != dev for c in caps.values()):
        raise SystemExit("a member's dev result does not cover exactly the dev300 images")
    reward = _dev_reward(dev)
    cider = CiderD([reward.refs[j] for j in rest])  # document frequencies: train-minus-dev300 references only
    toks = {s: [t.split() for t in reward.seg([caps[s][i] for i in dev])] for s in SEEDS}
    pick = [SEEDS[medoid([toks[s][n] for s in SEEDS], cider)] for n in range(len(dev))]
    preds.write_text(json.dumps({i: caps[s][i] for i, s in zip(dev, pick, strict=True)}, ensure_ascii=False, indent=1),
                     encoding="utf-8")
    write_json(d / "p1dev_mbr3_selection.json", {
        "rule": reg["procedure"]["mbr"], "preds": preds.name, "preds_sha256": sha256(preds), "dev_ids": dev,
        "picked_member": pick, "picked_counts": {s: pick.count(s) for s in SEEDS}, "df_images": len(rest),
        "inputs_sha256": {f"{RESULT[s]}.json": sha256(d / f"{RESULT[s]}.json") for s in SEEDS},
        "provenance": provenance()})
    print(f"MBR picks {dict((s, pick.count(s)) for s in SEEDS)} -> {preds}")
    return 0


# ----------------------------------------------------------------------------------------------- gate
def _exact(c: str) -> set:
    return {c}


def system_stats(res: dict, cap: dict, gold: dict, panel_gold: dict) -> dict:
    """CIDEr-D and BLEU-4 (evaluate.py, word level), CHAIR_i in points and mentions per caption (evaluate.py's
    CHAIR-vi), object P / R / F1 over unique exact classes against the dev references and against the panel."""
    from object_prf import image_counts, scores
    from rescap.chair import objects_in

    word = next(r for r in res["results"] if r["tokenization"] == "word-level")["scores_scaled_x100"]
    out = {"CIDEr": word["CIDEr"], "BLEU4": word["BLEU-4"], "CHAIR_i": 100 * res["chair"]["CHAIR_i"],
           "mentions_per_caption": res["chair"]["mentions_per_caption"]}
    for tag, g in (("ktvic5", gold), ("panel", panel_gold)):
        s = scores([image_counts(set(objects_in(cap[i])), g[i], _exact) for i in g])
        out.update({f"P_{tag}": s["P"], f"R_{tag}": s["R"], f"F1_{tag}": s["F1"]})
    return out


def variant_deltas(per: dict, chair_i: dict) -> tuple[dict, dict]:
    """D_v [mean, 95% lo, hi] of per-image CIDEr-D minus the members' per-image mean, and dCHAIR_i (points)."""
    from rl_reward import boot

    base = sum(per[s] for s in SEEDS) / len(SEEDS)
    d = {v: boot(per[v] - base, **BOOT) for v in VARIANTS}
    return d, {v: chair_i[v] - sum(chair_i[s] for s in SEEDS) / len(SEEDS) for v in VARIANTS}


def decide(d: dict, dchair: dict, gate: dict) -> dict:
    """The registered gate on point estimates: eligible iff D_v >= dev_cider_min and dCHAIR_i <= chair_margin_points;
    PASS iff a variant is eligible, carrying the larger D_v (tie: the soup); KILL otherwise; K1 and K2 as registered."""
    lo, margin = gate["dev_cider_min"], gate["chair_margin_points"]
    eligible = {v: d[v] >= lo and dchair[v] <= margin for v in VARIANTS}
    passed = any(eligible.values())
    carried = max((v for v in VARIANTS if eligible[v]), key=lambda v: (d[v], v == "soup")) if passed else None
    big = [v for v in VARIANTS if d[v] >= lo]
    k1, k2 = not big, bool(big) and all(dchair[v] > margin for v in big)
    if passed == (k1 or k2):
        raise AssertionError("the kill rules and the PASS rule disagree")
    return {"eligible": eligible, "verdict": "PASS" if passed else "KILL", "carried": carried, "K1": k1, "K2": k2}


def predictions_hold(delta: dict, pred: dict) -> dict:
    """Each frozen prediction against one variant's deltas vs the member mean (descriptive; registered for the
    carried variant)."""
    inside = {q: pred[q][0] <= delta[q] <= pred[q][1] for q in ("dCIDEr", "dBLEU4", "dF1", "dCHAIRi_points")}
    return {**inside, "dmentions": abs(delta["dmentions"]) <= pred["dmentions_abs_max"]}


def _golds(dev: list[str]) -> tuple[dict, dict]:
    """Classes named by the 5 dev references of each image, and by the panel on the images that have one."""
    from evaluate import references
    from rescap.chair import objects_in

    refs = references("train_data.json")
    panel = json.loads(PANEL.read_text(encoding="utf-8"))["train"]
    gold = {i: set().union(*(objects_in(r) for r in refs[i])) for i in dev}
    return gold, {i: set().union(*(objects_in(c) for c in panel[i])) for i in dev if panel.get(i)}


def _score(d: Path, dev: list[str]) -> tuple[dict, dict, dict]:
    """(evaluate.py result, captions, per-image word-level CIDEr-D x100) of every system; rl_report.dev_scores
    recomputes the per-image scores and asserts that their mean is evaluate.py's corpus CIDEr within 1e-6."""
    from rl_report import _dev_reward, dev_scores

    reward = _dev_reward(dev)
    res, caps, per = {}, {}, {}
    for k, name in RESULT.items():
        ids, caps[k], per[k] = dev_scores(str(d / f"{name}.json"), reward)
        if ids != dev:
            raise SystemExit(f"{name}: not scored on exactly the dev300 images")
        res[k] = json.loads((d / f"{name}.json").read_text(encoding="utf-8"))
    return res, caps, per


def _step0(reg: dict, caps_s42: dict, cider_s42: float, dev: list[str]) -> dict:
    """The same-machine re-decode of p1dev_s42 against the registered n2 decode: reported, never used to select."""
    from rl_report import _cider, _preds

    ref = reg["p1dev_reference_dev300"]
    if _cider(str(N2_DECODE)) != ref["CIDEr_D_x100"] or sha256(N2_PREDS) != ref["preds_sha256"]:
        raise SystemExit("the registered n2 decode of p1dev_s42 differs from the registration")
    n2 = _preds(str(N2_PREDS))
    return {"identical_caption_share": float(np.mean([caps_s42[i] == n2[i] for i in dev])),
            "cider_x100_redecode_minus_n2": cider_s42 - ref["CIDEr_D_x100"],
            "use": "reported only, never used to select anything"}


def gate(reg: dict, d: Path) -> int:
    """Every system's dev scores, the deltas vs the member mean, the gate and the registered descriptive readouts."""
    dev, _ = split_ids(reg)
    res, caps, per = _score(d, dev)
    gold, panel_gold = _golds(dev)
    if len(panel_gold) != reg["data"]["panel"]["dev_images_with_panel"]:
        raise SystemExit(f"{len(panel_gold)} dev images with a panel, registered {reg['data']['panel']}")
    stats = {k: system_stats(res[k], caps[k], gold, panel_gold) for k in RESULT}
    member_mean = {q: sum(stats[s][q] for s in SEEDS) / len(SEEDS) for q in stats["s42"]}
    deltas = {v: {q: stats[v][q] - member_mean[q] for q in member_mean} for v in VARIANTS}
    dvals, dchair = variant_deltas(per, {k: s["CHAIR_i"] for k, s in stats.items()})
    verdict = decide({v: dvals[v][0] for v in VARIANTS}, dchair, reg["gate"])
    pred, member_cider = reg["frozen_predictions"], [stats[s]["CIDEr"] for s in SEEDS]
    readout = {v: {"dCIDEr": dvals[v][0], "dBLEU4": deltas[v]["BLEU4"], "dF1": deltas[v]["F1_ktvic5"],
                   "dCHAIRi_points": dchair[v], "dmentions": deltas[v]["mentions_per_caption"]} for v in VARIANTS}
    out = {
        **verdict, "rule": reg["gate"]["rule"], "eligible_rule": reg["gate"]["eligible"],
        "status": reg["gate"]["status"],
        "D_cider_x100_mean_lo_hi": dvals, "dCHAIR_i_points": dchair,
        "predictions_vs_member_mean": {v: {"values": readout[v], "inside": predictions_hold(readout[v], pred)}
                                       for v in VARIANTS},
        "predictions_apply_to": pred["applies_to"], "systems": stats, "member_mean": member_mean,
        "deltas_vs_member_mean": deltas,
        "members_cider_spread": {"values": dict(zip(SEEDS, member_cider, strict=True)),
                                 "range": max(member_cider) - min(member_cider)},
        "all_three_members_agree_share": float(np.mean([len({caps[s][i] for s in SEEDS}) == 1 for i in dev])),
        "step0_s42_redecode_vs_registered_n2": _step0(reg, caps["s42"], stats["s42"]["CIDEr"], dev),
        "n_images": len(dev), "n_panel_images": len(panel_gold), "dev_ids": dev,
        "per_image_cider_x100": {k: per[k].tolist() for k in RESULT},
        "inputs_sha256": {**{f"{n}.json": sha256(d / f"{n}.json") for n in RESULT.values()},
                          **{p.name: sha256(p) for p in (d / "p1dev_mbr3_selection.json", PANEL, N2_DECODE, N2_PREDS)}},
        "provenance": provenance(),
    }
    write_json(d / "gate.json", out)
    print(f"S1 gate {out['verdict']} (carried {out['carried']}): D_soup {dvals['soup']}, D_mbr {dvals['mbr']}, "
          f"dCHAIR_i {dchair}")
    return 0


# ----------------------------------------------------------------------------------------------- selftest
def _write_member(d: Path, factors: dict, lora: dict, base: str) -> Path:
    from peft import LoraConfig
    from safetensors.torch import save_file

    d.mkdir(parents=True)
    save_file(factors, str(d / "adapter_model.safetensors"))
    LoraConfig(task_type="CAUSAL_LM", base_model_name_or_path=base, **lora).save_pretrained(str(d))
    return d


def _synthetic(r: int, layers: int, fill) -> dict:
    """LoRA factors for q_proj (4 x 4) and down_proj (4 x 6) of `layers` layers; fill(shape, kind) gives each tensor."""
    shapes = {"self_attn.q_proj": (4, 4), "mlp.down_proj": (4, 6)}
    out = {}
    for n in range(layers):
        for mod, (o, i) in shapes.items():
            key = f"base_model.model.model.layers.{n}.{mod}"
            out[f"{key}.lora_A.weight"], out[f"{key}.lora_B.weight"] = fill((r, i), "A"), fill((o, r), "B")
    return out


def _test_soup(reg: dict, tmp: Path) -> None:
    import torch

    lora, base = reg["models"]["member_s42"]["lora"], reg["models"]["base"]["id"]
    r, layers = lora["r"], 11  # 11 layers: the last is layers.10, which a string sort would put before layers.9

    def spike(a):  # A[0, 0] = a and B[0, 0] = 1, so the member's update is (alpha / r) a = 2a at [0, 0], 0 elsewhere
        def fill(shape, kind):
            t = torch.zeros(shape)
            t[0, 0] = a if kind == "A" else 1
            return t
        return fill
    exact = [_write_member(tmp / "exact" / m, _synthetic(r, layers, spike(a)), lora, base)
             for m, a in zip(MEMBERS, (3, 6, 9), strict=True)]
    model, rows = build_soup(exact)
    assert [x["module"].split(".layers.")[1] for x in rows] == ["0.self_attn.q_proj", "10.self_attn.q_proj",
                                                               "0.mlp.down_proj", "10.mlp.down_proj"], rows
    for _, m in _soup_layers(model):
        want = torch.zeros_like(m.get_delta_weight("soup"))
        want[0, 0] = 2 * (3 + 6 + 9) / 3  # the mean update, exactly representable
        assert torch.equal(m.get_delta_weight("soup"), want) and m.lora_A["soup"].weight.dtype == torch.float32
    assert all(x["allclose"] for x in rows), rows
    gen = torch.Generator().manual_seed(0)
    one = _synthetic(r, layers, lambda shape, kind: torch.randn(shape, generator=gen) / 10)
    same = [_write_member(tmp / "same" / m, one, lora, base) for m in MEMBERS]
    model, rows = build_soup(same)  # three copies of one member: the soup reproduces that member
    assert all(x["allclose"] for x in rows), rows
    for _, m in _soup_layers(model):
        assert torch.allclose(m.get_delta_weight("soup"), m.get_delta_weight(MEMBERS[0]))
    saved = save_soup(model, tmp / "same" / SOUP)
    assert saved["saved_equals_checked"] and (saved["r"], saved["lora_alpha"]) == (3 * r, 3 * r), saved
    rand = [_write_member(tmp / "rand" / m, _synthetic(r, layers, lambda shape, kind: torch.randn(
        shape, generator=gen) / 10), lora, base) for m in MEMBERS]
    assert all(x["allclose"] for x in build_soup(rand)[1])
    host = lora_host(one)
    for layer in (m for m in host.modules() if isinstance(m, torch.nn.Linear)):
        layer.weight = torch.nn.Parameter(layer.weight.to(torch.bfloat16), requires_grad=False)
    bf16 = build_soup(rand, host=host)[1]  # the soup takes its base's dtype: on a bf16 base the check fails
    assert not any(x["allclose"] for x in bf16) and all(x["dtype"] == "torch.bfloat16" for x in bf16), bf16


def _test_mbr() -> None:
    from rl_reward import CiderD

    corpus = [["con chó chạy trên cỏ", "một con chó đang chạy"], ["hai người đi xe máy", "người đàn ông lái xe"],
              ["chiếc thuyền trên sông", "một chiếc thuyền nhỏ"], ["con mèo nằm trên ghế", "một con mèo ngủ"]]
    cider = CiderD([[r.split() for r in refs] for refs in corpus])

    def pick(*caps):
        return medoid([c.split() for c in caps], cider)
    agree, odd = "con chó chạy trên cỏ", "chiếc thuyền trên sông"
    assert pick(agree, agree, odd) == 0 and pick(odd, agree, agree) == 1 and pick(agree, odd, agree) == 0
    assert pick(odd, odd, odd) == 0  # all three agree: the lower seed
    assert pick("con chó chạy trên bãi cỏ", "con mèo nằm trên ghế", "con chó nằm trên ghế") == 2  # between the two


def _test_gate(reg: dict) -> None:
    g = reg["gate"]
    lo, margin = g["dev_cider_min"], g["chair_margin_points"]
    rng = np.random.default_rng(1)
    base = rng.integers(100, 200, 300).astype(float)
    per = {"s42": base, "s43": base + 3, "s44": base + 6}  # per-image member mean: base + 3, exactly
    chair = {"s42": 20, "s43": 22, "s44": 24, "soup": 21, "mbr": 22}  # member mean 22
    d, dchair = variant_deltas({**per, "soup": base + 3 + lo + 1 / 2, "mbr": base + 3 + lo - 1 / 2}, chair)
    assert d["soup"][0] == lo + 1 / 2 and d["soup"][1] <= d["soup"][0] <= d["soup"][2] and dchair["soup"] == -1
    v = decide({k: x[0] for k, x in d.items()}, dchair, g)
    assert (v["verdict"], v["carried"], v["K1"], v["K2"]) == ("PASS", "soup", False, False), v
    d, dchair = variant_deltas({**per, "soup": base + 3 + lo / 2, "mbr": base + 3 + lo / 4}, chair)
    v = decide({k: x[0] for k, x in d.items()}, dchair, g)
    assert (v["verdict"], v["carried"], v["K1"], v["K2"]) == ("KILL", None, True, False), v
    v = decide({"soup": lo + 1, "mbr": lo}, {"soup": margin + 1 / 2, "mbr": margin + 1 / 10}, g)
    assert (v["verdict"], v["K1"], v["K2"]) == ("KILL", False, True), v
    v = decide({"soup": lo, "mbr": lo + 1}, {"soup": margin, "mbr": margin}, g)  # both at the bars: eligible
    assert (v["verdict"], v["carried"]) == ("PASS", "mbr"), v
    v = decide({"soup": lo + 1, "mbr": lo + 1}, {"soup": 0, "mbr": 0}, g)
    assert v["carried"] == "soup", v  # tie: the soup
    pred = reg["frozen_predictions"]
    inside = {"dCIDEr": pred["dCIDEr_central"], "dBLEU4": pred["dBLEU4"][0], "dF1": 0, "dCHAIRi_points": 0,
              "dmentions": 0}
    assert all(predictions_hold(inside, pred).values())
    assert not predictions_hold({**inside, "dmentions": 2 * pred["dmentions_abs_max"]}, pred)["dmentions"]


def selftest() -> None:
    reg = load_prereg()
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        (t / "x.json").write_text("{}", encoding="utf-8")
        assert fresh(t / "x.json") == t / "x_v2.json" and fresh(t / "y.json") == t / "y.json"
        assert sorted(["a.10.b", "a.9.b", "a.0.b"], key=_natural) == ["a.0.b", "a.9.b", "a.10.b"]
        _test_soup(reg, t)
    _test_mbr()
    _test_gate(reg)
    print("seed_consensus selftest ok")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="mode")
    sub.add_parser("check").add_argument("--out", type=Path, required=True)
    s = sub.add_parser("soup")
    s.add_argument("--runs", type=Path, required=True, help="directory holding p1dev_s42, p1dev_s43, p1dev_s44")
    s.add_argument("--report", type=Path, required=True)
    for mode in ("mbr", "gate"):
        sub.add_parser(mode).add_argument("--dir", type=Path, required=True, help="the job's output directory")
    args = ap.parse_args()
    if args.selftest:
        selftest()
        return 0
    if args.mode is None:
        ap.error("--selftest or one of check, soup, mbr, gate")
    reg = load_prereg()
    if args.mode == "check":
        return check(reg, args.out)
    if args.mode == "soup":
        return soup(reg, args.runs, args.report)
    return {"mbr": mbr, "gate": gate}[args.mode](reg, args.dir)


if __name__ == "__main__":
    sys.exit(main())
