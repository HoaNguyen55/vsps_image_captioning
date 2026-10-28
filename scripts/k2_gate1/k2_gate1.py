#!/usr/bin/env python3
"""K2 Gate 1 dev gate on UIT-ViIC val 924 (rule: manuscript/prereg/2026-10-28_k2_gate1/RULE.md; CC-148 W3-W7,
W11-W13). Target builders, trainer, student decoder, detector pass, guard and caps. The decision is gate1_decide.py.

    python3 k2_gate1.py --selftest                                       CPU, synthetic rows (laptop or M3)
    python3 k2_gate1.py guard HEAD                                       M3 only: common.guard (M4 refused, CC-151)
    python3 k2_gate1.py manifest --set ut|probe --out TSV                CPU: pool (UT-2402 minus W25) or 40 probe ids
    python3 k2_gate1.py reg --manifest TSV --out REG.json                CPU: LB registration of the teacher decode
    $GD     k2_gate1.py detect --manifest TSV --out DET.json             GPU, venv-gd: D(img) at 0.30 on the pool
    python3 k2_gate1.py targets --teacher PREDS --detect DET --out T.json   CPU: unedited / gold / det / ref targets
    $VQ     k2_gate1.py decode --arm A [--adapter DIR] --manifest TSV --out-dir O   GPU, venv-q3, one pinned path (W7)
    python3 k2_gate1.py caps --timing PREDS --out CAPS.json              CPU: stage caps from the measured rates (W11)
    $VQ     k2_gate1.py train --arm A --targets T.json --out-dir O       GPU, venv-q3, w22_sft.load() verbatim
    $VQ|$GD k2_gate1.py imports --venv q3|gd                             CPU: every Gate 1 symbol; exit 3 = missing
    python3 k2_gate1.py left --ledger L --stage S [--caps CAPS.json]     CPU: timeout s = min(stage cap, total left);
                                                                         exit 4 = HELD (the step would cross NOT_AFTER)

Caption text is read only by code (targets, trainer); every printed line and every record is numbers and shas.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent / "grl"), str(HERE.parent / "w22_sft"), str(HERE.parent / "lb")]
import common as K  # noqa: E402
import k2_gate0 as KG  # noqa: E402

#: the HOLD files (CC-148 W9, CC-151 W2/W3): each must exist in the HEAD commit, not merely on disk
W25_REL = "manuscript/prereg/2026-10-28_k2_gate1/w25_excluded_ids.txt"  # written by W25 (scripts/w25), amendment 1
PREREG_REL = "manuscript/prereg/2026-10-28_mt4_kv/PREREG.md"  # conditional MT4 PREREG, both branches (PI-1026bb Q1)
VAL_TSV = "manuscript/prereg/2026-10-21_dev_pools/uitviic_val.tsv"
ARMS = ("unedited", "gold", "det", "ref")  # trained arms (RULE §3); base_s is decoded, never trained
SYSTEMS = ("base_s",) + ARMS
N_NEW, BATCH, EPOCHS = 512, 4, 2  # Gate 0 frozen max_new_tokens; B-N1 batch; CC-148 W4
TEACHER_RUN = "k2g1_qwen3vl_8b_ut-detailed"
# measured rates (RULE §7): W22-SFT C1 (w22_decide.json 100f7274), Gate 0 val decode, P2 detector pass
S512, S64, S_BF16, S_DET = 0.7892, 0.454, 3.25, 0.2089
LOAD_H, CAP_FACTOR, CPU_ALLOW, NF4_PLAN = 0.1, 1.2, 1.25, 2.0
GATE1_TOTAL_H = 36.0  # RULE §8: MT4 dev 40 GPU-h (PI-1026bb Q3: cap 170 = test 100 + dev 40 + English 30) - W22 - W25
NOT_AFTER = 1793966400  # 2026-11-06T12:00:00Z: A's N9 rescue starts on M3 (CC-148 W12, CC-151 W4)
CLEANUP_H = 2.0  # RULE §5: pull outputs, delete the staged UT/val images, verify; reserved before NOT_AFTER
N_REFS_PLAN, UT_PLAN, VAL_N, PROBE_N = 12012, 2402, 924, 40
LORA_TENSORS = 36 * 7 * 2  # lora_A + lora_B over 7 projections x 36 layers


# ------------------------------------------------------------------------------------------------ pool and guard
def at_head(rel: str, root: Path = K.ROOT) -> str:
    """The file as committed at HEAD. An untracked or uncommitted file is the HOLD (CC-151 W3)."""
    r = subprocess.run(["git", "-C", str(root), "show", f"HEAD:{rel}"], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"HELD: {rel} is not committed at HEAD (CC-148 W9 / CC-151 W2: W25 and the MT4 PREREG first)")
    return r.stdout


def pool(root: Path = K.ROOT) -> list[int]:
    """UT-2402 minus the committed W25 near-duplicate exclusions; the committed MT4 PREREG is the second HOLD."""
    at_head(PREREG_REL, root)
    ut = K.ids("ut2402")
    drop = {int(x) for x in at_head(W25_REL, root).split()}
    if not drop <= set(ut):
        raise SystemExit("REFUSED: a W25 id is not in UT-2402")
    return [i for i in ut if i not in drop]


def guard(head: str) -> dict:
    """M3 only (CC-151 r2): common.guard verbatim. M4 is refused until an amendment removes the C-EN record
    dependency of val_ids_ok / refused_sets (k2_gate0.py:301-311, common.py:112-122), which faults on M4."""
    if K.host_ok(head) != "m3":
        raise SystemExit("REFUSED: K2 Gate 1 runs on M3 only (CC-151 r2); M4 faults in val_ids_ok")
    return K.guard(head)


def staged_sha() -> dict[str, str]:
    return {f: h for h, f in (x.split("  ") for x in (K.UV / "images.sha256").read_text().splitlines())}


def manifest(which: str) -> str:
    """TSV rows id, file, sha256 (the LB manifest form) in ascending id order."""
    sha = staged_sha()
    ids = pool() if which == "ut" else pool()[:PROBE_N]  # probe: the first 40 pool ids, never a W25-excluded id
    if set(ids) & set(K.ids("val924")):
        raise SystemExit("REFUSED: a val id in a training manifest")
    return "".join(f"{i}\t{i:012d}.jpg\t{sha[f'{i:012d}.jpg']}\n" for i in ids)


def teacher_reg(man: Path) -> dict:
    """Gate 0's registration (B-N1 Qwen3-VL-8B block, venv-lb, bf16, batch 4, detailed prompt, 512 tokens) with the
    data set swapped from val to the UT pool."""
    r = KG.registration("val", N_NEW, man)
    ds = r["datasets"].pop("val") | {"n_images": len(man.read_text().splitlines())}
    r["datasets"]["ut"] = ds
    r["runs"] = [{"run_id": TEACHER_RUN, "model": "qwen3vl_8b", "dataset": "ut", "prompt_mode": "detailed"}]
    r["prereg_id"] = "2026-10-28_k2_gate1/TEACHER"
    return r


def rows_of(man: Path) -> list[tuple[str, str, str]]:
    return [tuple(x.split("\t")[:3]) for x in man.read_text().splitlines()]


# ------------------------------------------------------------------------------------------------ targets
def build_targets(preds: dict, ids: list[int], gold: dict, D: dict, refs: dict) -> tuple[dict, dict]:
    """(targets, counts). unedited = untruncate only; gold / det = k2_gate0.edit with gold or D(img) at 0.30;
    ref = every reference of the image. An empty edited target drops that image from that arm (RULE §3)."""
    t = {a: {} for a in ARMS}
    n = {"deleted_units": {"gold": 0, "det": 0}, "dropped_empty": {a: 0 for a in ARMS}}
    for i in ids:
        c = KG.untruncate(preds["predictions"][str(i)], preds["hit_max"][str(i)])
        for arm, text in (("unedited", c), ("gold", KG.edit(c, gold[i])), ("det", KG.edit(c, set(D[i])))):
            if arm != "unedited":
                text, gone = text
                n["deleted_units"][arm] += len(gone)
            if text:
                t[arm][str(i)] = [text]
            else:
                n["dropped_empty"][arm] += 1
        if refs.get(i):
            t["ref"][str(i)] = refs[i]
        else:
            n["dropped_empty"]["ref"] += 1
    n["examples_per_epoch"] = {a: sum(map(len, t[a].values())) for a in ARMS}
    return t, n


def cmd_targets(a) -> None:
    out = Path(a.out)
    if out.exists():
        raise SystemExit(f"REFUSED: {out} exists")
    preds = json.loads(Path(a.teacher).read_text(encoding="utf-8"))
    ids = pool()
    if sorted(map(int, preds["predictions"])) != ids or preds["max_new_tokens"] != N_NEW:
        raise SystemExit("REFUSED: the teacher decode is not the 512-token decode of the pool")
    det = json.loads(Path(a.detect).read_text())
    D = {int(i): v for i, v in det["D_0.30"].items()}
    if sorted(D) != ids:
        raise SystemExit("REFUSED: the detector record does not cover the pool")
    refs: dict[int, list[str]] = {}
    for x in json.loads((K.UV / "train_data.json").read_text(encoding="utf-8"))["annotations"]:
        refs.setdefault(int(x["image_id"]), []).append(x["caption"].strip())
    t, n = build_targets(preds, ids, K.gold(), D, refs)
    # the staged file is common.stage's cut to UT-2402 + val, so its sha is not SRC_PINS' release sha (CC-151 W5)
    n |= {"train_data_json_staged_sha256": K.sha_file(K.UV / "train_data.json"),
          "n_refs": sum(map(len, t["ref"].values()))}
    out.write_text(json.dumps({"targets": t, "teacher_sha256": K.sha_file(Path(a.teacher)),
                               "detect_sha256": K.sha_file(Path(a.detect))}, ensure_ascii=False))
    Path(str(out) + ".counts.json").write_text(json.dumps(n, indent=1))
    print(json.dumps(n))


# ------------------------------------------------------------------------------------------------ detector (venv-gd)
def cmd_detect(a) -> None:
    """k2_p2_detect's pinned model and rule (given-phrase mode, box threshold 0.30) on the UT pool."""
    import numpy as np
    import torch
    from groundingdino.util.inference import load_image

    import k2_p2_detect as PD

    out = Path(a.out)
    if out.exists():
        raise SystemExit(f"REFUSED: {out} exists")
    todo = rows_of(Path(a.manifest))
    model, caption, posmap, meta, calls = PD.load_detector()
    D, t = {}, []
    for i, f, h in todo:
        p = K.UV / "images" / f
        if K.sha_file(p) != h:
            raise SystemExit(f"FAULT: staged image {f} differs from the manifest")
        t0 = time.time()
        _, image = load_image(str(p))
        with torch.no_grad():
            o = model(image[None].to("cuda"), captions=[caption])
        D[i] = PD.present(PD.class_scores(o["pred_logits"].sigmoid()[0].float().cpu().numpy(), posmap), PD.BOX_T)
        t.append(time.time() - t0)
        if calls[0] == 0:
            raise SystemExit("FAULT: MultiScaleDeformableAttention CUDA op not used (CPU fallback)")
    rec = {"schema": "vsps.k2.gate1_detect.v1", "n_images": len(todo), "classes": list(PD.COCO80), **meta,
           "D_0.30": D, "s_per_image": round(float(np.mean(t)), 4)}
    out.write_text(json.dumps(rec, indent=1))
    print(json.dumps({"n_images": len(todo), "s_per_image": rec["s_per_image"]}))


# ------------------------------------------------------------------------------------------------ GPU: shared
def encode(proc, img, text: str):
    """Chat-template prompt for one image, as w22_sft.cmd_run builds it."""
    return proc.apply_chat_template([{"role": "user", "content": [{"type": "image", "image": img},
                                                                 {"type": "text", "text": text}]}],
                                    add_generation_prompt=True, tokenize=True, return_dict=True, return_tensors="pt")


def cmd_train(a) -> None:
    """One arm, seed 0, 2 epochs, last checkpoint (CC-148 W4). Config = W22-SFT C1 verbatim: w22_sft.load(gc=False),
    AdamW lr 1e-4 wd 0, 8 micro-batches of 1 per step, constant lr, no clipping. The last partial accumulation group
    takes one optimiser step. Non-finite loss = FAULT (exit 3)."""
    import torch
    from PIL import Image
    from train import schedule

    import w22_sft as W

    out = Path(a.out_dir) / a.arm
    if (out / "adapter_model.safetensors").exists():
        raise SystemExit(f"REFUSED: {out} already holds an adapter")
    T = json.loads(Path(a.targets).read_text(encoding="utf-8"))["targets"][a.arm]
    keys = [f"{i}:{k}" for i in sorted(T, key=int) for k in range(len(T[i]))]
    order = schedule(keys, EPOCHS * len(keys), K.CFG["seed"])
    sha = staged_sha()
    text = W.prompt()
    dev = torch.device("cuda:0")
    torch.cuda.reset_peak_memory_stats()
    proc, net = W.load(a.snapshot, False)
    opt = torch.optim.AdamW([p for p in net.parameters() if p.requires_grad], lr=W.LR, weight_decay=0.0)
    lens, t0 = [], time.time()
    for n, key in enumerate(order, 1):
        i, k = key.split(":")
        f = f"{int(i):012d}.jpg"
        if K.sha_file(K.UV / "images" / f) != sha[f]:
            raise SystemExit(f"FAULT: {f} differs from images.sha256")
        with Image.open(K.UV / "images" / f) as im:
            enc = encode(proc, im.convert("RGB"), text)
        tgt = torch.tensor([proc.tokenizer(T[i][int(k)], add_special_tokens=False)["input_ids"] + [W.EOT]])
        lens.append(tgt.shape[1])
        ids = torch.cat([enc["input_ids"], tgt], 1)
        batch = {kk: v.to(dev) for kk, v in enc.items() if kk not in ("input_ids", "attention_mask")}
        batch["pixel_values"] = batch["pixel_values"].to(torch.bfloat16)
        batch.update(input_ids=ids.to(dev), attention_mask=torch.ones_like(ids).to(dev),
                     labels=torch.cat([torch.full_like(enc["input_ids"], -100), tgt], 1).to(dev))
        loss = net(**batch, use_cache=False).loss
        if not torch.isfinite(loss):
            print(f"FAULT: non-finite loss at example {n}")
            sys.exit(3)
        (loss / W.ACCUM).backward()
        if n % W.ACCUM == 0 or n == len(order):
            opt.step()
            opt.zero_grad(set_to_none=True)
        if n % 500 == 0:
            print(f"{a.arm} {n}/{len(order)}", flush=True)
    net.save_pretrained(out)
    import numpy as np

    L = np.array(lens)
    rec = {"arm": a.arm, "examples": len(order), "examples_per_epoch": len(keys), "epochs": EPOCHS,
           "optimizer_steps": math.ceil(len(order) / W.ACCUM), "s_per_example": round((time.time() - t0) / len(order), 4),
           "peak_reserved_b": torch.cuda.max_memory_reserved(),
           "label_len": {"mean": round(float(L.mean()), 2), "p50": int(np.percentile(L, 50)),
                         "p99": int(np.percentile(L, 99)), "max": int(L.max()), "over_512": int((L > N_NEW).sum())},
           "adapter_sha256": K.sha_file(out / "adapter_model.safetensors")}
    (out / "train.json").write_text(json.dumps(rec, indent=1))
    print(json.dumps(rec))


def student(snapshot: str, adapter: str | None):
    """The one pinned decode path (W7): w22_sft.load() (4-bit NF4 + fresh LoRA), the arm's adapter state loaded into
    it, eval, KV cache on, left padding. base_s and the timing probe keep the fresh LoRA (lora_B = 0, asserted), so
    the base runs the identical path, LoRA compute included, with an exactly zero update."""
    import w22_sft as W

    proc, net = W.load(snapshot, False)
    if adapter:
        from peft import set_peft_model_state_dict
        from safetensors.torch import load_file

        sd = load_file(str(Path(adapter) / "adapter_model.safetensors"))
        res = set_peft_model_state_dict(net, sd)
        if len(sd) != LORA_TENSORS or res.unexpected_keys:
            raise SystemExit(f"FAULT: adapter has {len(sd)} tensors, unexpected {res.unexpected_keys[:3]}")
        if not any(p.abs().max().item() != 0 for n, p in net.named_parameters() if "lora_B" in n):
            raise SystemExit("FAULT: every lora_B of the loaded adapter is zero (it would decode as base_s; CC-151 W5)")
    elif any(p.abs().max().item() != 0 for n, p in net.named_parameters() if "lora_B" in n):
        raise SystemExit("FAULT: the fresh LoRA of the base path is not zero")
    proc.tokenizer.padding_side = "left"
    net.eval()
    net.config.use_cache = True
    net.generation_config.use_cache = True
    return proc, net


def cmd_decode(a) -> None:
    """Greedy, 512 new tokens, batch 4, detailed prompt, through decode_hf_vlm's generate / slices / writer."""
    import decode_hf_vlm as LB
    import torch

    import w22_sft as W

    man = Path(a.manifest)
    if man.resolve() == K.pinned(VAL_TSV).resolve():
        KG.val_ids_ok(man)  # W19 before any val decode
    elif {int(r[0]) for r in rows_of(man)} & set(K.ids("val924")):
        raise SystemExit("REFUSED: a non-val manifest holds a val id")
    out = Path(a.out_dir) / f"k2g1_{a.arm}.preds.json"
    if out.exists():
        raise SystemExit(f"REFUSED: {out} exists")
    if (a.arm in ARMS) != (a.adapter is not None):
        raise SystemExit("REFUSED: base_s and timing decode without an adapter, every trained arm with its own")
    started = LB.utc()
    proc, net = student(a.snapshot, a.adapter)
    prompt = W.prompt()
    items = rows_of(man)
    gen = LB.make_generate(proc, net, prompt, N_NEW, K.UV / "images")
    part = Path(str(out) + ".partial.jsonl")
    kw = {"max_new_tokens": N_NEW, "do_sample": False, "num_beams": 1}
    key = LB.run_key(K.sha_file(man), {"arm": a.arm}, {"adapter": a.adapter}, kw, prompt, items)
    t0 = time.time()
    rows = LB.decode_slices(items, BATCH, gen, part, key)
    s_img = (time.time() - t0) / len(items)
    prov = {k: None for k in LB.PROV_FIELDS} | {
        "schema": LB.SCHEMA, "prereg_id": "2026-10-28_k2_gate1/STUDENT", "decoder_sha256": K.sha_file(Path(__file__)),
        "run_id": f"k2g1_{a.arm}", "model": "qwen3vl_8b_nf4_peft", "dataset": man.name, "prompt_mode": "detailed",
        "max_new_tokens": N_NEW, "batch_size": BATCH, "dtype": "nf4/bf16", "manifest_sha256": K.sha_file(man),
        "n_images": len(items), "parity_slice0": {"n": 0, "identical": 0}, "resumed": False, "started_utc": started,
        "finished_utc": LB.utc(), "machine_id": os.environ.get("VSPS_MACHINE_ID"), "packages": LB.packages(),
        "venv_freeze_sha256": os.environ.get("VSPS_VENV_FREEZE_SHA256"), "adapter": a.adapter,
        "adapter_sha256": K.sha_file(Path(a.adapter) / "adapter_model.safetensors") if a.adapter else None,
        "s_per_image_decode": round(s_img, 4), "gpu": torch.cuda.get_device_name(0)}
    LB.write_output(out, prov, rows)
    print(json.dumps({"arm": a.arm, "n": len(items), "s_per_image": round(s_img, 4)}))


# ------------------------------------------------------------------------------------------------ caps (W11)
def cap(proj_h: float) -> float:
    """ceil(1.2 x projection), up to 0.1 GPU-h (CC-148 W11)."""
    return math.ceil(round(10 * CAP_FACTOR * proj_h, 6)) / 10


def plan(s_dec: float, s_worst: float | None = None, n_pool: int = UT_PLAN, n_refs: int = N_REFS_PLAN) -> dict:
    """Stage projections (GPU-h, one load each) and caps. Training terms carry the CPU-preprocessing allowance
    (W22 rates exclude it); SFT-ref is priced at the 512-token rate (RULE §8, W4). s_dec = the measured base-path
    decode rate (base_s); s_worst = the same rate scaled to 512 steps in every slice (trained arms)."""
    s_worst = s_dec if s_worst is None else s_worst
    p = {"teacher": n_pool * S_BF16 / 3600, "detect": n_pool * S_DET / 3600,
         "timing": PROBE_N * S_BF16 * NF4_PLAN / 3600,
         **{f"train_{a}": EPOCHS * n_pool * S512 * CPU_ALLOW / 3600 for a in ("unedited", "gold", "det")},
         "train_ref": EPOCHS * n_refs * S512 * CPU_ALLOW / 3600,
         **{f"decode_{s}": VAL_N * (s_dec if s == "base_s" else s_worst) / 3600 for s in SYSTEMS}}
    p = {k: round(v + LOAD_H, 4) for k, v in p.items()}
    caps = {k: cap(v) for k, v in p.items()}
    return {"projection_h": p, "cap_h": caps, "projection_total_h": round(sum(p.values()), 4),
            "cap_total_h": round(sum(caps.values()), 1), "gate1_total_h": GATE1_TOTAL_H,
            "fits": sum(caps.values()) <= GATE1_TOTAL_H + 1e-9}


def cmd_caps(a) -> None:
    """After the timing probe (40 UT-2402 train images, base_s path, no text read): the decode rate fixes the five
    decode caps. Exit 2 if the caps exceed the Gate 1 total (NOT-RUN, cost, before any training)."""
    t = json.loads(Path(a.timing).read_text(encoding="utf-8"))
    targets = json.loads(Path(a.targets).read_text(encoding="utf-8"))["targets"]
    s = t["s_per_image_decode"]
    s_w = worst_rate(s, [{"n_tokens": t["n_tokens"][i], "hit_max": t["hit_max"][i]} for i in t["n_tokens"]])
    r = plan(s, s_w, len(pool()), sum(map(len, targets["ref"].values())))
    r |= {"s_per_image_base_path_measured": s, "s_per_image_worst_512": round(s_w, 4)}
    Path(a.out).write_text(json.dumps(r, indent=1))
    print(json.dumps({k: r[k] for k in ("projection_total_h", "cap_total_h", "fits")}))
    sys.exit(0 if r["fits"] else 2)


def cmd_imports(a) -> None:
    """Import check first (beside w22_sft.py imports): the symbols Gate 1 adds, in the venv that runs them."""
    try:
        if a.venv == "q3":
            import decode_hf_vlm  # noqa: F401
            from peft import set_peft_model_state_dict  # noqa: F401
            from safetensors.torch import load_file  # noqa: F401
            from train import schedule  # noqa: F401

            import w22_sft  # noqa: F401
        else:
            import torch
            from groundingdino.util.inference import load_image  # noqa: F401

            import k2_p2_detect  # noqa: F401
            if not torch.cuda.is_available():
                raise ImportError("torch sees no CUDA device")
    except Exception as e:  # noqa: BLE001 - any failure is a clean STOP before the GPU
        print(f"IMPORT CHECK FAILED ({a.venv}): {type(e).__name__}: {e}")
        sys.exit(3)
    print(f"k2_gate1 imports ok ({a.venv})")


def worst_rate(s_probe: float, rows: list[dict]) -> float:
    """Gate 0's freeze scaling (k2_gate0.freeze): the probe rate times 512 over the probe's mean slice steps, i.e. a
    student whose every slice runs to 512 tokens (a trained arm may decode longer than the base)."""
    return s_probe * N_NEW / KG.slice_steps(rows, N_NEW, BATCH)


def used_seconds(ledger: Path, now: float | None = None) -> float:
    """`NAME start EPOCH` before a step and `NAME SECONDS` after it (b1.used_seconds rule): an open start is charged
    to the next start or to now, so a reboot cannot undercount."""
    if not ledger.exists():
        return 0.0
    total, open_t = 0.0, None
    for p in (x.split() for x in ledger.read_text().splitlines() if x.strip()):
        if len(p) == 3 and p[1] == "start":
            total += float(p[2]) - open_t if open_t is not None else 0.0
            open_t = float(p[2])
        else:
            total, open_t = total + float(p[1]), None
    return total + ((time.time() if now is None else now) - open_t if open_t is not None else 0.0)


def left(ledger: Path, stage: str, caps: Path | None = None, now: float | None = None) -> int:
    """Timeout seconds for a stage: min(its cap, the Gate 1 total minus every GPU second so far). Before caps.json
    exists (teacher, detect, timing) the caps come from plan() at the planning decode rate. A step whose timeout
    would end after NOT_AFTER - CLEANUP_H is HELD (exit 4): a rerunnable fault, never a cost stop (CC-151 W4)."""
    c = json.loads(caps.read_text())["cap_h"] if caps else plan(S_BF16 * NF4_PLAN)["cap_h"]
    t = max(0, int(min(round(c[stage] * 3600), GATE1_TOTAL_H * 3600 - used_seconds(ledger))))
    if (time.time() if now is None else now) + t > NOT_AFTER - CLEANUP_H * 3600:
        print(f"HELD: {stage} ({t} s) would cross NOT_AFTER 2026-11-06T12:00Z minus {CLEANUP_H} h cleanup")
        sys.exit(4)
    return t


# ------------------------------------------------------------------------------------------------ selftest
def hold_selftest(repo: Path) -> None:
    """CC-151 W3: an untracked (or uncommitted) HOLD file is HELD; the same files committed at HEAD release it."""
    g = ["git", "-C", str(repo), "-c", "user.name=x", "-c", "user.email=x", "-c", "core.hooksPath=/dev/null"]
    for rel, text in ((W25_REL, f"{K.ids('ut2402')[0]}\n"), (PREREG_REL, "synthetic\n")):
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_text(text)
    subprocess.run(g[:3] + ["init", "-q"], check=True)
    for stage in ("untracked", "committed"):
        try:
            got = pool(repo)
        except SystemExit as e:
            assert stage == "untracked" and str(e).startswith("HELD"), e
        else:
            assert stage == "committed" and len(got) == UT_PLAN - 1 and K.ids("ut2402")[0] not in got, got[:3]
        if stage == "untracked":
            subprocess.run(g + ["add", W25_REL, PREREG_REL], check=True)
            subprocess.run(g + ["commit", "-qm", "x"], check=True)


def selftest() -> None:
    import tempfile

    g = {"person", "sports ball"}
    head = ("một người khoác áo sọc tím lấp lánh đang tâng quả bóng bạc lơ lửng giữa bãi cát vàng óng dưới mái "
            "vòm kính cong queo cạnh hàng cờ đuôi nheo phất phơ")  # k2_gate0 selftest string (CC-125 X5: synthetic)
    preds = {"predictions": {"1": head + ", cạnh con chó.", "2": "con chó 人.", "3": head + ". con chó đang"},
             "hit_max": {"1": False, "2": False, "3": True}}
    D = {1: ["person", "sports ball", "dog"], 2: [], 3: ["person", "sports ball"]}
    t, n = build_targets(preds, [1, 2, 3], {1: g, 2: g, 3: g}, D, {1: ["r a", "r b"], 3: ["r c"]})
    assert t["unedited"]["1"] == [head + ", cạnh con chó."] and t["gold"]["1"] == [head + "."], t["gold"]
    assert t["det"]["1"] == [head + ", cạnh con chó."]  # D says dog: the detector editor keeps the clause
    assert "2" not in t["gold"] and "2" not in t["det"] and t["unedited"]["2"] == ["con chó 人."]
    assert t["unedited"]["3"] == [head + "."]  # untruncate drops the unfinished last unit
    assert n["dropped_empty"] == {"unedited": 0, "gold": 1, "det": 1, "ref": 1}, n
    assert n["deleted_units"] == {"gold": 2, "det": 1} and n["examples_per_epoch"]["ref"] == 3, n
    # caps: by hand for a 3.25 s/img student rate (= the bf16 anchor)
    p = plan(S_BF16)
    assert p["projection_h"]["teacher"] == round(2402 * 3.25 / 3600 + 0.1, 4) and p["cap_h"]["teacher"] == 2.8, p
    assert p["cap_h"]["detect"] == 0.3 and p["cap_h"]["train_gold"] == 1.7 and p["cap_h"]["train_ref"] == 8.1, p
    assert p["cap_h"]["decode_base_s"] == 1.2 and p["fits"], p  # 924 x 3.25 / 3600 + 0.1 = 0.9342 -> 1.121 -> 1.2
    assert cap(1.0) == 1.2 and cap(0.25) == 0.3 and cap(0.5) == 0.6  # exact products are not rounded up
    assert abs(worst_rate(4.0, [{"n_tokens": 256, "hit_max": False}] * 8) - 8.0) < 1e-9  # half the steps: x2
    assert worst_rate(4.0, [{"n_tokens": 9, "hit_max": True}] * 4) == 4.0  # every slice already at 512
    w = plan(S_BF16, 2 * S_BF16)
    assert w["cap_h"]["decode_base_s"] == 1.2 and w["cap_h"]["decode_gold"] == 2.2, w["cap_h"]
    big = plan(30.0)  # a 30 s/img student decode cannot fit the total
    assert not big["fits"] and big["cap_total_h"] > GATE1_TOTAL_H
    with tempfile.TemporaryDirectory() as d:
        led = Path(d) / "gpu_seconds.tsv"
        led.write_text("teacher start 100\nteacher 50\ndetect start 1000\n")
        assert used_seconds(led, now=1030) == 80.0
        led.write_text("a start 100\nb start 160\nb 10\n")  # a never closed: charged to the next start
        assert used_seconds(led) == 70.0
        early = NOT_AFTER - 10 ** 6  # well before the N9 window
        assert left(led, "teacher", now=early) == 10080  # the 2.8 GPU-h cap; 70 s used of the 36 h total
        led.write_text(f"x {int(GATE1_TOTAL_H * 3600) - 600}\n")  # 600 s of the total left: below the 2.8 h cap
        assert left(led, "teacher", now=early) == 600 and left(led, "detect", now=early) == 600
        led.write_text(f"x {int(GATE1_TOTAL_H * 3600) + 5}\n")
        assert left(led, "detect", now=early) == 0
        led.write_text("")
        edge = NOT_AFTER - CLEANUP_H * 3600 - 10080
        assert left(led, "teacher", now=edge) == 10080  # ends exactly at NOT_AFTER - cleanup: allowed
        try:
            left(led, "teacher", now=edge + 1)
        except SystemExit as e:
            assert e.code == 4, e
        else:
            raise AssertionError("a step crossing NOT_AFTER was started")
        hold_selftest(Path(d) / "repo")
    from train import schedule

    keys = [f"{i}:{k}" for i in ("1", "3") for k in range(2)]
    o = schedule(keys, 2 * len(keys), 0)
    assert sorted(o[:4]) == sorted(keys) == sorted(o[4:]) and o == schedule(keys, 8, 0)  # each epoch once, seeded
    reg = teacher_reg(K.pinned(VAL_TSV))
    assert reg["runs"][0]["dataset"] == "ut" and reg["datasets"]["ut"]["n_images"] == 924
    assert reg["decode"]["max_new_tokens"] == {"detailed": 512}
    src = Path(__file__).read_text()
    assert "W.load(a.snapshot, False)" in src and "W.load(snapshot, False)" in src  # W22 load path, C1
    print("k2_gate1 selftest ok")


def main() -> None:
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
    if sys.argv[1:2] == ["guard"]:
        print(json.dumps(guard(sys.argv[2])))
        return
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    m = sp.add_parser("manifest")
    m.add_argument("--set", choices=("ut", "probe"), required=True)
    m.add_argument("--out", required=True)
    r = sp.add_parser("reg")
    r.add_argument("--manifest", required=True)
    r.add_argument("--out", required=True)
    d = sp.add_parser("detect")
    d.add_argument("--manifest", required=True)
    d.add_argument("--out", required=True)
    t = sp.add_parser("targets")
    for f in ("--teacher", "--detect", "--out"):
        t.add_argument(f, required=True)
    c = sp.add_parser("caps")
    for f in ("--timing", "--targets", "--out"):
        c.add_argument(f, required=True)
    tr = sp.add_parser("train")
    tr.add_argument("--arm", choices=ARMS, required=True)
    for f in ("--targets", "--out-dir", "--snapshot"):
        tr.add_argument(f, required=True)
    de = sp.add_parser("decode")
    de.add_argument("--arm", choices=SYSTEMS + ("timing",), required=True)
    de.add_argument("--adapter")
    for f in ("--manifest", "--out-dir", "--snapshot"):
        de.add_argument(f, required=True)
    sp.add_parser("imports").add_argument("--venv", choices=("q3", "gd"), required=True)
    u = sp.add_parser("left")
    u.add_argument("--ledger", required=True)
    u.add_argument("--stage", required=True)
    u.add_argument("--caps")
    a = ap.parse_args()
    if a.cmd == "manifest":
        Path(a.out).write_text(manifest(a.set))
    elif a.cmd == "reg":
        Path(a.out).write_text(json.dumps(teacher_reg(Path(a.manifest)), indent=1) + "\n")
    elif a.cmd == "left":
        print(left(Path(a.ledger), a.stage, Path(a.caps) if a.caps else None))
    else:
        try:
            {"imports": cmd_imports, "detect": cmd_detect, "targets": cmd_targets, "caps": cmd_caps,
             "train": cmd_train, "decode": cmd_decode}[a.cmd](a)
        except Exception as e:  # an OOM is NOT-RUN (fault) -> TO-PI, never a switch to C2 (CC-151 r13)
            if type(e).__name__ != "OutOfMemoryError":
                raise
            print(f"FAULT: CUDA out of memory in {a.cmd}")
            sys.exit(5)


if __name__ == "__main__":
    main()
