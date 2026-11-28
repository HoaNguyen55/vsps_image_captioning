"""Batched greedy decoder for S0 and the student arms (COMPUTE_PLAN v3 §1-§2, CC-501 Q13).

Registered settings = FAIR's scripts/evaluate.py (sha pinned) load_model + generate, replicated with a pinned snapshot
path and a device argument: Qwen/Qwen2.5-VL-7B-Instruct @ cc594898 (B-N1 entry qwen25vl_7b), sdpa, the base loaded in
bf16 for every arm (ERRATUM_O31_2 E5; the 4-bit load is not offered), LoRA adapter through PeftModel (base checked against
adapter_config.json), processor min_pixels 256*28*28 and max_pixels 512*28*28, chat template with the image first,
generate(max_new_tokens=160, do_sample=False) and the model's own generation_config otherwise, transformers 4.51.3.
Batch 8 uses left padding; it is allowed only after the Q13 parity rule (below), else batch 1 for every system and
tier. Output: <out>.preds.json {image_id: caption} with a .sha256 sidecar, resumable through <out>.partial.jsonl;
the log prints counts only.

Q13 parity rule, fixed before the check runs: on 50 KTVIC-test (dev) images, for EACH of S0, S1 and S2, every
caption's token ids at batch 8 must equal batch 1; any mismatch -> batch 1 for every system and every tier.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

SYSTEMS = ("S0", "S1", "S2")
ARMS = SYSTEMS + ("A-1", "A-2", "A-3", "A-4")
PARITY_N = 50
P = 28 * 28
SETTINGS = {"base": "Qwen/Qwen2.5-VL-7B-Instruct", "revision": "cc594898137f460bfe9f0759e9844b3ce807cfb5",
            "registry_key": "qwen25vl_7b", "transformers": "4.51.3", "max_new_tokens": 160,
            "min_pixels": 256 * P, "max_pixels": 512 * P, "attn": "sdpa", "dtype": "bfloat16"}
PROMPTS = {"vi": "Mô tả chi tiết bức ảnh này bằng tiếng Việt."}  # = evaluate.PROMPTS["detailed"]
PROMPTS["en"] = "Describe this image in detail in English."  # ERRATUM_O31_2 E6 = evaluate.PROMPTS["detailed_en"]


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
    if cfg.get("system") not in ARMS:
        errs.append("system")
    if cfg.get("batch") not in (1, 8):
        errs.append("batch must be 1 or 8")
    if cfg.get("batch") == 8 and not cfg.get("parity_passed"):
        errs.append("batch 8 needs the Q13 parity record")
    if cfg.get("lang") not in ("vi", "en"):
        errs.append("lang")
    if cfg.get("do_sample", False) or cfg.get("num_beams", 1) != 1:
        errs.append("greedy only")
    if cfg.get("max_new_tokens", SETTINGS["max_new_tokens"]) != SETTINGS["max_new_tokens"]:
        errs.append("max_new_tokens is 160 (evaluate.py)")
    if (cfg.get("system") == "S0") != (cfg.get("adapter") is None):
        errs.append("S0 has no adapter; every other arm needs one")
    if errs:
        raise ValueError("REFUSED decode config: " + "; ".join(errs))
    return cfg


def parity_passed(record: dict) -> bool:
    """A Q13 parity record allows batch 8 only if it is the decision of parity() over all three systems."""
    return record.get("batch") == 8 and record.get("mismatches") == {}


# ------------------------------------------------------------------ generation
def until_eos(ids: list[int], stop: set[int]) -> tuple[list[int], bool]:
    """Token ids up to and including the first stop token; hit_max = no stop token within the budget."""
    for k, t in enumerate(ids):
        if t in stop:
            return ids[:k + 1], False
    return ids, True


def make_generate(model, processor, prompt: str, max_new_tokens: int = SETTINGS["max_new_tokens"]):
    """gen(images) -> [(token_ids, caption, hit_max)]; evaluate.generate's inputs, batched with left padding."""
    import torch

    processor.tokenizer.padding_side = "left"
    gc = model.generation_config
    stop = {t for t in ([gc.eos_token_id] if isinstance(gc.eos_token_id, int) else list(gc.eos_token_id or []))}
    if gc.pad_token_id is not None:
        stop.add(gc.pad_token_id)

    def gen(images):
        messages = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": prompt}]}]
        text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = processor(text=[text] * len(images), images=list(images), return_tensors="pt",
                           padding=True).to(model.device)
        with torch.no_grad():
            ids = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
        out = []
        for row in ids[:, inputs.input_ids.shape[1]:].tolist():
            kept, hit = until_eos(row, stop)
            out.append((kept, processor.batch_decode([kept], skip_special_tokens=True)[0].strip(), hit))
        return out
    return gen


def read_items(tsv: Path) -> list[tuple[str, str, str]]:
    """[(image_id, file, sha256)] from a TSV manifest; ids unique."""
    rows = [tuple(x.split("\t")) for x in tsv.read_text(encoding="utf-8").splitlines() if x.strip()]
    if any(len(r) != 3 for r in rows) or len({r[0] for r in rows}) != len(rows):
        raise SystemExit(f"{tsv}: not distinct (id, file, sha256) rows")
    return rows


def run(gen, items: list, folder: Path, out: Path, batch: int, keep_tokens: bool = False) -> dict:
    """Resumable decode of `items` in fixed slices of `batch`; each image's bytes are checked against its sha.
    Writes <out>.preds.json and its .sha256 when every image is done."""
    from PIL import Image

    part = Path(str(out) + ".partial.jsonl")
    have = {json.loads(x)["image_id"]: json.loads(x) for x in part.read_text(encoding="utf-8").splitlines()} \
        if part.exists() else {}
    if any(r["batch"] != batch for r in have.values()):
        raise SystemExit("REFUSED resume at another batch size than the partial file")
    todo = [it for it in items if it[0] not in have]
    with open(part, "a", encoding="utf-8") as fh:
        for i in range(0, len(todo), batch):
            sl = todo[i:i + batch]
            ims = []
            for _iid, f, h in sl:
                b = (folder / f).read_bytes()
                if hashlib.sha256(b).hexdigest() != h:
                    raise SystemExit(f"FAULT {f}: sha256 differs from the manifest")
                ims.append(Image.open(folder / f).convert("RGB"))
            for (iid, _f, _h), (ids, cap, hit) in zip(sl, gen(ims)):
                row = {"image_id": iid, "caption": cap, "n_tokens": len(ids), "hit_max": hit, "batch": batch}
                if keep_tokens:
                    row["ids"] = ids
                have[iid] = row
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            fh.flush()
    preds = {iid: have[iid]["caption"] for iid, _f, _h in items}
    pf = Path(str(out) + ".preds.json")
    pf.write_text(json.dumps(preds, ensure_ascii=False, indent=1), encoding="utf-8")
    sha = hashlib.sha256(pf.read_bytes()).hexdigest()
    Path(str(pf) + ".sha256").write_text(f"{sha}  {pf.name}\n")
    print(f"decoded {len(items)} images; hit_max {sum(have[i]['hit_max'] for i, _f, _h in items)}")
    return {"n": len(items), "sha256": sha, "rows": [have[i] for i, _f, _h in items]}


# ------------------------------------------------------------------ host loader (GPU; replicates evaluate.load_model)
def check_adapter(adapter: Path) -> str:
    """evaluate.check_adapter_base: the adapter was trained on the pinned base; returns the adapter weights' sha."""
    cfg = json.loads((adapter / "adapter_config.json").read_text(encoding="utf-8"))
    if cfg.get("base_model_name_or_path") != SETTINGS["base"]:
        raise SystemExit(f"adapter {adapter} was trained on {cfg.get('base_model_name_or_path')}, not {SETTINGS['base']}")
    return hashlib.sha256((adapter / "adapter_model.safetensors").read_bytes()).hexdigest()


def load_student(snapshot: Path, adapter: Path | None, device: str = "cuda:0"):  # pragma: no cover
    import torch
    import transformers
    from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration

    from . import repo

    if transformers.__version__ != SETTINGS["transformers"]:
        raise SystemExit(f"FAULT transformers {transformers.__version__} != {SETTINGS['transformers']}")
    repo()
    import decode_hf_vlm as LB

    from .probe import registry_entry

    m = registry_entry(SETTINGS["registry_key"])
    if m["revision"] != SETTINGS["revision"]:
        raise SystemExit("FAULT registry revision differs from the O31 pin")
    LB.check_snapshot(m, snapshot)
    from rescap.vlm.base import dtype_kwarg

    kw = dict(attn_implementation=SETTINGS["attn"], device_map={"": device}, **dtype_kwarg(torch.bfloat16))
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(snapshot, **kw)
    info = {"base_revision": m["revision"], "adapter_sha256": None, "base_dtype": "bfloat16"}  # E5
    if adapter is not None:
        from peft import PeftModel

        info["adapter_sha256"] = check_adapter(adapter)
        model = PeftModel.from_pretrained(model, str(adapter))
    model.eval()
    processor = AutoProcessor.from_pretrained(snapshot, min_pixels=SETTINGS["min_pixels"], max_pixels=SETTINGS["max_pixels"])
    return model, processor, info
