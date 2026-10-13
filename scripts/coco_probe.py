#!/usr/bin/env python
""" (NC log) — cross-lingual generalisation probe on COCO-2014 (Karpathy test, 2,500 images).

    # zero-shot, both modes
    python scripts/coco_probe.py --images-dir /root/coco_images --out-dir /root/probe_out
    # distilled system
    python scripts/coco_probe.py --adapter /root/off4090_sft_slim ...
    # any other adapter: output files are named after --name (p1_s43-short.shard0of1.jsonl, ...)
    python scripts/coco_probe.py --adapter $NCS_DATA/runs/p1_s43 --name p1_s43 ...
    # split across 2 machines
    ... --shard 0 --of 2   |   ... --shard 1 --of 2

Generates VIETNAMESE captions on COCO images with the EXACT evaluate.py
configuration (bf16, sdpa, min/max_pixels, greedy, 60/160-token caps) —
measuring the real system of Tables 1/2, not a demo configuration. Designed
after generate_stage1.py: resumable (one jsonl line per image, images already
present are skipped) and shards need no coordination.

Scoring does NOT happen here — score_coco_probe.py runs on the local machine
with instances_val2014 + reference captions (gold = union, registered in the
NC log).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from evaluate import PROMPTS  # noqa: E402  — same prompts as Tables 1/2

P = 28 * 28
MAX_NEW = {"short": 60, "detailed": 160}
#: --model -> (hub id, transformers class, pixels per vision token). Every backbone gets the same 256-1,024
#: vision-token budget. qwen3-vl-8b needs transformers >= 4.57, so it runs from its own venv (S0, judge D10 (iii)).
DEFAULT = "qwen2.5-vl-7b"
BACKBONES = {DEFAULT: ("Qwen/Qwen2.5-VL-7B-Instruct", "Qwen2_5_VLForConditionalGeneration", P),
             "qwen3-vl-8b": ("Qwen/Qwen3-VL-8B-Instruct", "Qwen3VLForConditionalGeneration", 32 * 32)}


def stem(name: str | None, adapter: str | None, backbone: str) -> str:
    """Output file stem. Another backbone must be named, so it never writes into the 7B zero-shot files."""
    if backbone != DEFAULT and not name:
        raise SystemExit(f"--name is required with --model {backbone}")
    return name or ("distill" if adapter else "zeroshot")


def load_model(adapter: str | None, backbone: str = DEFAULT, weights: str | None = None):
    """`backbone` (+ `adapter`, merged) in eval mode and its processor; `weights` = a local pinned snapshot of it."""
    import torch
    import transformers
    from transformers import AutoProcessor

    from rescap.vlm.base import dtype_kwarg

    hub_id, cls, px = BACKBONES[backbone]
    src = weights or hub_id
    model = getattr(transformers, cls).from_pretrained(
        src, attn_implementation="sdpa",
        device_map={"": 0}, **dtype_kwarg(torch.bfloat16))
    if adapter:
        from peft import PeftModel

        model = PeftModel.from_pretrained(model, adapter)
        # Merge the adapter into the weights: same W+BA computation, drops the
        # per-token PEFT overhead (measured: 11.8s/image unmerged vs ~5.8s merged
        # in detailed mode). Declared in the artifact: distill captions come from
        # the MERGED adapter — mathematically equivalent, greedy as before.
        model = model.merge_and_unload()
    model.eval()
    processor = AutoProcessor.from_pretrained(src, min_pixels=256 * px, max_pixels=1024 * px)
    return model, processor


def read_jsonl(path: Path, repair: bool = False) -> list[dict]:
    """Complete rows of a resumable jsonl output. With `repair` (the writer, before appending),
    a last line cut short by a killed run is also cut from the file."""
    if not path.exists():
        return []
    raw = path.read_text(encoding="utf-8")
    if repair and raw and not raw.endswith("\n"):
        path.write_text(raw[: raw.rfind("\n") + 1], encoding="utf-8")
    return [json.loads(line) for line in raw.splitlines()[: raw.count("\n")]]


def generate(model, processor, image, prompt: str, max_new_tokens: int) -> str:
    """Greedy reply of the model to one image and one text prompt."""
    import torch

    messages = [{"role": "user", "content": [
        {"type": "image"}, {"type": "text", "text": prompt}]}]
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = processor(text=[text], images=[image], return_tensors="pt").to(model.device)
    with torch.no_grad():
        ids = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
    return processor.batch_decode(
        ids[:, inputs["input_ids"].shape[1]:], skip_special_tokens=True)[0].strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", default="data/coco_probe/manifest.json")
    ap.add_argument("--images-dir", required=True)
    ap.add_argument("--adapter", default=None, help="leave empty = zero-shot")
    ap.add_argument("--name", default=None,
                    help="output file stem, e.g. p1_s43 (default: distill with --adapter, else zeroshot)")
    ap.add_argument("--modes", default="short,detailed")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--of", type=int, default=1)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--model", default=DEFAULT, choices=sorted(BACKBONES))
    ap.add_argument("--weights", default=None, help="local pinned snapshot of --model (default: its hub id)")
    args = ap.parse_args()

    from PIL import Image

    system = stem(args.name, args.adapter, args.model)
    man = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    images = sorted(man["images"], key=lambda x: x["cocoid"])[args.shard:: args.of]
    if args.limit:
        images = images[: args.limit]
    out_root = Path(args.out_dir)
    out_root.mkdir(parents=True, exist_ok=True)

    model, processor = load_model(args.adapter, args.model, args.weights)
    modes = [m.strip() for m in args.modes.split(",") if m.strip()]

    for mode in modes:
        out = out_root / f"{system}-{mode}.shard{args.shard}of{args.of}.jsonl"
        done = {r["cocoid"] for r in read_jsonl(out, repair=True)}
        todo = [i for i in images if i["cocoid"] not in done]
        print(f"[{system}/{mode}] {len(done)} already present, {len(todo)} to generate", flush=True)
        t0 = time.time()
        with out.open("a", encoding="utf-8") as fh:
            for k, img in enumerate(todo):
                path = Path(args.images_dir) / img["filename"]
                image = Image.open(path).convert("RGB")
                caption = generate(model, processor, image, PROMPTS[mode], MAX_NEW[mode])
                fh.write(json.dumps({"cocoid": img["cocoid"], "caption": caption},
                                    ensure_ascii=False) + "\n")
                fh.flush()
                if (k + 1) % 50 == 0:
                    rate = (time.time() - t0) / (k + 1)
                    print(f"  {k+1}/{len(todo)} · {rate:.2f}s/image · "
                          f"~{rate*(len(todo)-k-1)/60:.0f} min left", flush=True)
        print(f"[{system}/{mode}] DONE → {out}", flush=True)
    return 0


def _check() -> None:
    # the default backbone keeps the exact pre-switch load (hub id, class, 28-px tokens)
    assert BACKBONES[DEFAULT] == ("Qwen/Qwen2.5-VL-7B-Instruct", "Qwen2_5_VLForConditionalGeneration", 28 * 28)
    assert BACKBONES["qwen3-vl-8b"][2] == (16 * 2) ** 2  # patch 16 x spatial merge 2
    assert stem(None, None, DEFAULT) == "zeroshot" and stem(None, "a", DEFAULT) == "distill"
    assert stem("q3", None, "qwen3-vl-8b") == "q3"
    try:
        stem(None, None, "qwen3-vl-8b")
        raise AssertionError("an unnamed second backbone would overwrite the 7B zero-shot files")
    except SystemExit:
        pass


if __name__ == "__main__":
    _check()
    sys.exit(main())
