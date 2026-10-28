#!/usr/bin/env python3
"""W22-SFT memory probe (CC-148 W2; rule: manuscript/prereg/2026-10-28_w22_sft/PREREG.md). Does QLoRA NF4 SFT of
Qwen3-VL-8B @ 0c351dd at 512-token targets, micro-batch 1, fit one 24 GB GPU, and how fast is it?

    python3 w22_sft.py --selftest                        CPU, stdlib only (laptop or M3)
    python3 w22_sft.py snapcheck --snapshot DIR          CPU: the 14 B-N1 pins of the cached snapshot
    $VQ w22_sft.py imports --snapshot DIR                CPU, venv-q3: every module the probe uses; exit 3 = missing
    $VQ w22_sft.py plan --out PLAN.json                  CPU: the 40 + 1 UT-2402 train images, sha-checked
    $VQ w22_sft.py run --config c1|c2 --plan PLAN --snapshot DIR --out C.json     GPU, one config per process
    python3 w22_sft.py decide --dir O [--cost WHY]       CPU: w22_decide.json (one look)

Targets are synthetic token ids (no caption text from any dataset). The forward runs with use_cache=False and the
probe builds no KV-cache object, so the cache-attribute removal in transformers 4.56+ (K19 §5) cannot reach it.
No adapter is saved.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent / "grl")]
import common as K  # noqa: E402  (read-only: pinned id lists, sha_file, UV)

LIMIT_B = 23_500_000_000  # CC-148 W2: GB unit pinned to 1e9; integer compare, no rounding
CAP_S = 2700  # 0.75 GPU-h for every GPU process of W22-SFT, faulted ones included
DEV_CAP_H = 20.0  # CC-148 W11: Gate 1 dev
N_PROBE, ACCUM, T_LONG, T_SHORT, N_SHORT = 40, 8, 512, 64, 16
REG_IDS = (368, 419, 431, 488, 531)  # the first five ids of ut2402.txt (K19 §3)
EOT, FIRST_SPECIAL = 151645, 151643  # <|im_end|>; ids >= 151643 are special (Qwen3 tokenizer)
LORA = {"r": 16, "lora_alpha": 32, "lora_dropout": 0.0, "bias": "none",
        "target_modules": r"^(?!.*visual).*\.(q_proj|k_proj|v_proj|o_proj|gate_proj|up_proj|down_proj)$"}
LORA_PARAMS = 36 * 1_212_416  # 36 layers x r16 over q, k, v, o (4096/1024 out) and gate, up, down (12288)
LR = 1e-4
BN1 = "manuscript/prereg/2026-10-19_b_n1_vi_leaderboard.json"
BN1_SHA = "9ff02dc259258de1add426abd02131f2122e3476a81f9a076066ed6d74906134"
PROMPT_SHA = "0addb5dd720e4f24ac912d6fede9cb718e4051bc6944a85d9e7a92b0abb7ed08"  # evaluate.py PROMPTS["detailed"]
# PREREG §4 projection terms (counts and sources there)
UT, VAL, S_DEC, S_DET, N_REFS = 2402, 924, 3.24, 0.209, 12012  # S_DET: P2 detector s/img (OPS-1028i-op)
N_EDIT_ARMS, EPOCHS, N_VAL_DECODES, N_LOADS, LOAD_H = 3, 2, 5, 11, 0.1
FREEZE_PINS = {"torch": "2.5.1+cu121", "transformers": "4.57.6", "peft": "0.21.2", "bitsandbytes": "0.50.2",
               "accelerate": "1.15.0"}


# ------------------------------------------------------------------------------------------------ pure rules
def probe_ids(ut: list[int]) -> list[int]:
    """Fixed rule: the first 40 lines of the pinned, ascending ut2402.txt (anyone can check with head -40)."""
    return ut[:N_PROBE]


def worst(sizes: dict[int, tuple[int, int]]) -> int:
    """The UT-2402 image with the largest w x h (PIL header), ties to the lowest id."""
    return min(sizes, key=lambda i: (-sizes[i][0] * sizes[i][1], i))


def target_ids(n: int) -> list[int]:
    """n label positions built from token-id arithmetic only: n - 1 ordinary ids, then <|im_end|>."""
    return [1000 + (k * 7919) % 140000 for k in range(n - 1)] + [EOT]


def mem_fail(rec: dict) -> bool:
    return bool(rec.get("oom")) or int(rec["peak_reserved_b"]) > LIMIT_B


def projection(s512: float, s64: float) -> dict:
    """Gate 1 dev GPU-h (PREREG §4): teacher decode and detector pass of UT-2402, three edited-target arms at the
    512-token rate, SFT-ref on its 12,012 references at the 64-token rate, five val-924 decodes, eleven loads."""
    dec = ((UT + N_VAL_DECODES * VAL) * S_DEC + UT * S_DET) / 3600
    train = (N_EDIT_ARMS * EPOCHS * UT * s512 + EPOCHS * N_REFS * s64) / 3600
    return {"decode_h": round(dec, 4), "train_h": round(train, 4), "load_h": N_LOADS * LOAD_H,
            "dev_h": round(dec + train + N_LOADS * LOAD_H, 4)}


def verdict(c1: dict | None, c2: dict | None, cost: str | None = None) -> dict:
    """PREREG §5, first match wins."""
    for name, rec in (("c1", c1), ("c2", c2)):
        if rec is None:
            break
        if mem_fail(rec):
            if name == "c2":
                return {"verdict": "FAIL", "class": "memory (C1 and C2)", "route": "7B self-distillation (PI Q3)"}
            continue
        if not rec.get("complete"):
            break
        p = projection(rec["s_ex_512"], rec["s_ex_64"])
        if p["dev_h"] > DEV_CAP_H:
            return {"verdict": "FAIL", "class": f"speed ({name})", "projection": p,
                    "route": "7B self-distillation (PI Q3)"}
        return {"verdict": "PASS", "config": name, "projection": p}
    return {"verdict": "NOT-RUN", "class": "cost -> TO-PI", "why": cost or "no complete config within the cap"}


def remaining(used_s: int) -> int:
    return max(0, CAP_S - used_s)


def git_blob(p: Path) -> str:
    d = p.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(d) + d).hexdigest()


def prompt() -> str:
    m = re.search(r'"detailed":\s*"([^"]+)"', (K.ROOT / "scripts/evaluate.py").read_text(encoding="utf-8"))
    if not m or hashlib.sha256(m.group(1).encode()).hexdigest() != PROMPT_SHA:
        raise SystemExit("REFUSED: evaluate.py PROMPTS['detailed'] differs from 0addb5dd")
    return m.group(1)


# ------------------------------------------------------------------------------------------------ CPU commands
def cmd_snapcheck(a) -> None:
    bn1 = K.ROOT / BN1
    if K.sha_file(bn1) != BN1_SHA:
        raise SystemExit("REFUSED: the B-N1 registration differs from its pin")
    files = json.loads(bn1.read_text(encoding="utf-8"))["models"]["qwen3vl_8b"]["files"]
    snap = Path(a.snapshot)
    for f, pin in sorted(files.items()):
        got = K.sha_file(snap / f) if pin["kind"] == "sha256" else git_blob(snap / f)
        if got != pin["hash"]:
            raise SystemExit(f"REFUSED: {snap / f} differs from its B-N1 pin")
    print(f"snapshot ok: {len(files)} files match B-N1")


def cmd_imports(a) -> None:
    """Every module and symbol the run uses, inside the pinned venv, before any GPU step. Exit 3 on anything missing."""
    try:
        import accelerate
        import bitsandbytes
        import numpy  # noqa: F401
        import peft
        import torch
        import transformers
        from peft import LoraConfig, get_peft_model  # noqa: F401
        from PIL import Image  # noqa: F401
        from transformers import (AutoConfig, AutoModelForImageTextToText, AutoProcessor,  # noqa: F401
                                  BitsAndBytesConfig, Qwen3VLForConditionalGeneration)

        got = {"torch": torch.__version__, "transformers": transformers.__version__, "peft": peft.__version__,
               "bitsandbytes": bitsandbytes.__version__, "accelerate": accelerate.__version__}
        if got != FREEZE_PINS:
            raise ImportError(f"versions {got} differ from {FREEZE_PINS}")
        if not torch.cuda.is_available():
            raise ImportError("torch sees no CUDA device")
        import bitsandbytes.functional as bnbf  # a 4 KB NF4 round trip proves the CUDA library, not the CPU stub
        x = torch.randn(64, 64, device="cuda", dtype=torch.bfloat16)
        q, st = bnbf.quantize_4bit(x, quant_type="nf4")
        if (bnbf.dequantize_4bit(q, st) - x).abs().mean().item() > 0.2:
            raise ImportError("bitsandbytes NF4 round trip is wrong")
        del x, q, st
        torch.cuda.empty_cache()
        cfg = AutoConfig.from_pretrained(a.snapshot)
        if cfg.model_type != "qwen3_vl":
            raise ImportError(f"model_type {cfg.model_type} is not qwen3_vl")
        AutoProcessor.from_pretrained(a.snapshot, **bn1_model()["processor_kwargs"])
    except Exception as e:  # noqa: BLE001 - any failure here is a clean STOP before the GPU
        print(f"IMPORT CHECK FAILED: {type(e).__name__}: {e}")
        sys.exit(3)
    print(f"imports ok: {got}")


def bn1_model() -> dict:
    bn1 = K.ROOT / BN1
    if K.sha_file(bn1) != BN1_SHA:
        raise SystemExit("REFUSED: the B-N1 registration differs from its pin")
    return json.loads(bn1.read_text(encoding="utf-8"))["models"]["qwen3vl_8b"]


def cmd_plan(a) -> None:
    """The 40 probe ids + the worst-case image, all UT-2402 train (never val-924), sha-checked against the staged
    images.sha256 written by common.stage. Opens no release json and no val image."""
    from PIL import Image

    ut, val = K.ids("ut2402"), set(K.ids("val924"))
    shas = {f: h for h, f in (x.split("  ") for x in (K.UV / "images.sha256").read_text().splitlines())}
    names = {i: f"{i:012d}.jpg" for i in ut}
    missing = [n for n in names.values() if n not in shas or not (K.UV / "images" / n).is_file()]
    if missing:
        raise SystemExit(f"STOP: {len(missing)} UT-2402 images are not staged (e.g. {missing[0]})")
    sizes = {}
    for i, n in names.items():
        with Image.open(K.UV / "images" / n) as im:
            sizes[i] = im.size
    pick = probe_ids(ut) + [worst(sizes)]
    if set(pick) & val or not set(pick) <= set(ut):
        raise SystemExit("REFUSED: a probe id is not UT-2402 train")
    for i in pick:
        if K.sha_file(K.UV / "images" / names[i]) != shas[names[i]]:
            raise SystemExit(f"REFUSED: {names[i]} differs from images.sha256")
    Path(a.out).write_text(json.dumps({"ids": pick, "worst_id": pick[-1], "worst_wh": sizes[pick[-1]],
                                       "files": {str(i): [names[i], shas[names[i]]] for i in pick}}, indent=1))
    print(f"plan: {len(pick)} train images, worst {pick[-1]} {sizes[pick[-1]]}")


# ------------------------------------------------------------------------------------------------ GPU
def load(snapshot: str, gc: bool):
    """The pinned load path (PREREG §2); the Gate 1 trainer uses it verbatim. No prepare_model_for_kbit_training:
    it would turn on checkpointing by default and upcast the untied embed/lm_head to fp32."""
    import torch
    from peft import LoraConfig, get_peft_model
    from transformers import AutoModelForImageTextToText, AutoProcessor, BitsAndBytesConfig

    m = bn1_model()
    proc = AutoProcessor.from_pretrained(snapshot, **m["processor_kwargs"])
    q = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True,
                           bnb_4bit_compute_dtype=torch.bfloat16)
    net = AutoModelForImageTextToText.from_pretrained(snapshot, quantization_config=q, dtype=torch.bfloat16,
                                                      attn_implementation="sdpa", device_map={"": 0})
    net.config.use_cache = False
    if gc:
        net.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
        net.enable_input_require_grads()
    torch.manual_seed(0)
    net = get_peft_model(net, LoraConfig(task_type="CAUSAL_LM", **LORA))
    n = sum(p.numel() for p in net.parameters() if p.requires_grad)
    if n != LORA_PARAMS:
        raise SystemExit(f"FAULT: {n} trainable parameters, not {LORA_PARAMS} (LoRA reached the vision tower?)")
    net.train()
    return proc, net


def cmd_run(a) -> None:
    import torch
    from PIL import Image

    plan = json.loads(Path(a.plan).read_text())
    files = plan["files"]
    text = prompt()
    dev = torch.device("cuda:0")
    rec = {"config": a.config, "gc": a.config == "c2", "gpu": torch.cuda.get_device_name(0),
           "gpu_total_b": torch.cuda.get_device_properties(0).total_memory, "limit_b": LIMIT_B,
           "alloc_conf": os.environ.get("PYTORCH_CUDA_ALLOC_CONF"), "complete": False, "oom": False,
           "phase_peak_b": {"load": 0, "forward": 0, "backward": 0, "optimizer": 0}, "examples": []}
    out = Path(a.out)

    def save():
        rec["peak_reserved_b"] = max(rec["phase_peak_b"].values())
        tmp = out.with_suffix(".part")
        tmp.write_text(json.dumps(rec, indent=1))
        os.replace(tmp, out)

    def peak(phase):
        torch.cuda.synchronize()
        rec["phase_peak_b"][phase] = max(rec["phase_peak_b"][phase], torch.cuda.max_memory_reserved())
        torch.cuda.reset_peak_memory_stats()

    phase = "load"
    try:
        torch.cuda.reset_peak_memory_stats()
        t0 = time.time()
        proc, net = load(a.snapshot, rec["gc"])
        peak("load")
        rec["load_s"] = round(time.time() - t0, 2)
        opt = torch.optim.AdamW([p for p in net.parameters() if p.requires_grad], lr=LR, weight_decay=0.0)

        def example(i, n_tgt, step_opt):
            nonlocal phase
            name, sha = files[str(i)]
            if K.sha_file(K.UV / "images" / name) != sha:
                raise SystemExit(f"REFUSED: {name} differs from the plan")
            with Image.open(K.UV / "images" / name) as im:
                img = im.convert("RGB")
            enc = proc.apply_chat_template([{"role": "user", "content": [{"type": "image", "image": img},
                                                                         {"type": "text", "text": text}]}],
                                           add_generation_prompt=True, tokenize=True, return_dict=True,
                                           return_tensors="pt")
            tgt = torch.tensor([target_ids(n_tgt)])
            ids = torch.cat([enc["input_ids"], tgt], 1)
            batch = {k: v.to(dev) for k, v in enc.items() if k not in ("input_ids", "attention_mask")}
            batch["pixel_values"] = batch["pixel_values"].to(torch.bfloat16)
            batch.update(input_ids=ids.to(dev), attention_mask=torch.ones_like(ids).to(dev),
                         labels=torch.cat([torch.full_like(enc["input_ids"], -100), tgt], 1).to(dev))
            torch.cuda.synchronize()
            ts = time.time()
            phase = "forward"
            loss = net(**batch, use_cache=False).loss
            peak("forward")
            phase = "backward"
            (loss / ACCUM).backward()
            peak("backward")
            if step_opt:
                phase = "optimizer"
                opt.step()
                opt.zero_grad(set_to_none=True)
                peak("optimizer")
            torch.cuda.synchronize()
            rec["examples"].append({"id": i, "target": n_tgt, "seq": ids.shape[1],
                                    "grid_thw": enc["image_grid_thw"].tolist(), "opt": step_opt,
                                    "s": round(time.time() - ts, 4), "loss_finite": bool(torch.isfinite(loss))})
            save()

        ids = plan["ids"]
        for k, i in enumerate(ids[:N_PROBE]):  # 5 optimizer steps x 8 at 512 targets
            example(i, T_LONG, (k + 1) % ACCUM == 0)
        example(plan["worst_id"], T_LONG, True)  # worst-case vision tokens, one step of 1
        for k, i in enumerate(ids[:N_SHORT]):  # SFT-ref rate: 2 optimizer steps x 8 at 64 targets
            example(i, T_SHORT, (k + 1) % ACCUM == 0)
        ex = rec["examples"]
        rec["s_ex_512"] = round(sum(e["s"] for e in ex[ACCUM:N_PROBE]) / (N_PROBE - ACCUM), 4)  # steps 2-5
        rec["s_ex_64"] = round(sum(e["s"] for e in ex[N_PROBE + 1:]) / N_SHORT, 4)
        rec["s_opt_step_512"] = round(rec["s_ex_512"] * ACCUM, 4)
        free, total = torch.cuda.mem_get_info()
        rec["device_used_end_b"] = total - free  # beside the torch figure: includes the CUDA context
        rec["all_losses_finite"] = all(e["loss_finite"] for e in ex)
        rec["complete"] = True
    except (torch.cuda.OutOfMemoryError, RuntimeError) as e:
        if not isinstance(e, torch.cuda.OutOfMemoryError) and "out of memory" not in str(e).lower():
            raise
        rec["phase_peak_b"][phase] = max(rec["phase_peak_b"][phase], torch.cuda.max_memory_reserved())
        rec.update(oom=True, oom_phase=phase, oom_msg=str(e)[:300])
    save()
    print(json.dumps({k: rec.get(k) for k in ("config", "complete", "oom", "peak_reserved_b", "s_ex_512", "s_ex_64")}))


def cmd_memfail(a) -> None:
    sys.exit(0 if mem_fail(json.loads(Path(a.rec).read_text())) else 1)


def cmd_decide(a) -> None:
    d = Path(a.dir)
    out = d / "w22_decide.json"
    if out.exists():
        raise SystemExit("REFUSED: w22_decide.json exists (one look)")
    recs = {c: json.loads((d / f"{c}.json").read_text()) if (d / f"{c}.json").is_file() else None for c in ("c1", "c2")}
    v = verdict(recs["c1"], recs["c2"], a.cost)
    for c, r in recs.items():
        if r:
            v[c] = {k: r.get(k) for k in ("complete", "oom", "peak_reserved_b", "phase_peak_b", "s_ex_512", "s_ex_64",
                                          "s_opt_step_512", "device_used_end_b", "all_losses_finite", "gpu")}
            v[c]["sha256"] = K.sha_file(d / f"{c}.json")
    v["limit_b"], v["cap_s"], v["dev_cap_h"] = LIMIT_B, CAP_S, DEV_CAP_H
    out.write_text(json.dumps(v, indent=1))
    print(json.dumps(v))


# ------------------------------------------------------------------------------------------------ selftest
def selftest() -> None:
    ut = K.ids("ut2402")
    assert len(ut) == 2402 and ut == sorted(ut) and tuple(probe_ids(ut)[:5]) == REG_IDS and len(probe_ids(ut)) == 40
    assert not set(probe_ids(ut)) & set(K.ids("val924"))
    assert worst({5: (640, 480), 3: (480, 640), 9: (500, 500)}) == 3
    for n in (T_LONG, T_SHORT):
        t = target_ids(n)
        assert len(t) == n and t[-1] == EOT and all(0 < x < FIRST_SPECIAL for x in t[:-1]) and t == target_ids(n)
    ok = {"complete": True, "oom": False, "peak_reserved_b": LIMIT_B, "s_ex_512": 1.0, "s_ex_64": 0.3}
    assert not mem_fail(ok) and mem_fail(ok | {"peak_reserved_b": LIMIT_B + 1}) and mem_fail(ok | {"oom": True})
    p = projection(1.0, 0.3)  # by hand: ((2402 + 4620) * 3.24 + 2402 * 0.209) / 3600 = 23253.298 / 3600 = 6.4592;
    # train (14412 + 7207.2) / 3600 = 6.0053; loads 1.1; dev 13.5646
    assert p == {"decode_h": 6.4592, "train_h": 6.0053, "load_h": 1.1, "dev_h": 13.5646}, p
    slow = ok | {"s_ex_512": 2.5}  # train (36030 + 7207.2)/3600 = 12.0103 -> dev 19.5696 (PASS)
    fast_fail = ok | {"s_ex_512": 2.7}  # 38912.4 + 7207.2 -> 12.8110 -> dev 20.3702 (FAIL)
    assert projection(2.5, 0.3)["dev_h"] == 19.5696 and projection(2.7, 0.3)["dev_h"] == 20.3702
    big = ok | {"peak_reserved_b": LIMIT_B + 1}
    assert verdict(ok, None) == {"verdict": "PASS", "config": "c1", "projection": p}
    assert verdict(slow, None)["verdict"] == "PASS"
    assert verdict(fast_fail, None)["class"] == "speed (c1)"
    assert verdict(big, ok)["config"] == "c2"
    assert verdict(ok | {"oom": True}, fast_fail)["class"] == "speed (c2)"
    assert verdict(big, big)["class"] == "memory (C1 and C2)"
    assert verdict(big, None, "cap")["verdict"] == "NOT-RUN"
    assert verdict(big, ok | {"complete": False}, "cap")["verdict"] == "NOT-RUN"  # C2 cut by the cap, under the limit
    assert verdict(ok | {"complete": False}, None, "cap")["verdict"] == "NOT-RUN"
    assert verdict(big, big | {"complete": False})["class"] == "memory (C1 and C2)"
    assert verdict(None, None, "cap")["why"] == "cap"
    assert remaining(0) == 2700 and remaining(2000) == 700 and remaining(3000) == 0
    assert prompt() and K.sha_file(K.ROOT / BN1) == BN1_SHA
    assert bn1_model()["processor_kwargs"] == {"min_pixels": 262144, "max_pixels": 1048576}
    src = Path(__file__).read_text()
    bad = ["key" + "_cache", "Dynamic" + "Cache", "past_key" + "_values", "rl_" + "policy", "train_" + "stage2"]
    assert not [b for b in bad if b in src], "the probe must not use the cache API or the RL/7B trainers"
    print("w22_sft selftest ok")


def main() -> None:
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    for c in ("snapcheck", "imports"):
        sp.add_parser(c).add_argument("--snapshot", required=True)
    sp.add_parser("plan").add_argument("--out", required=True)
    sp.add_parser("memfail").add_argument("--rec", required=True)
    r = sp.add_parser("run")
    r.add_argument("--config", choices=("c1", "c2"), required=True)
    for f in ("--plan", "--snapshot", "--out"):
        r.add_argument(f, required=True)
    d = sp.add_parser("decide")
    d.add_argument("--dir", required=True)
    d.add_argument("--cost")
    a = ap.parse_args()
    {"snapcheck": cmd_snapcheck, "imports": cmd_imports, "plan": cmd_plan, "memfail": cmd_memfail, "run": cmd_run,
     "decide": cmd_decide}[a.cmd](a)


if __name__ == "__main__":
    main()
