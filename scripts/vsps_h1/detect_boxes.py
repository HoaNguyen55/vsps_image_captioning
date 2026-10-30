#!/usr/bin/env python
"""Run GroundingDINO and OWLv2 on KTVIC TRAIN images with the vi_en_map prompts (VSPS H1).

    python scripts/vsps_h1/detect_boxes.py --records <stage-1 dir> --images data/datasets/ktvic/images \
        --out <boxes.jsonl> [--limit 5] [--device auto]

One jsonl line per image:
    {"image_id", "file_name", "size": [w, h], "seconds", "device", "config_sha256", "map_sha256",
     "prompts": {prompt: {"gdino": [[x, y, w, h, score], ...], "owlv2": [...]}},
     "entities": {entity_id: prompt or null}}
Boxes are [x, y, w, h] in ABSOLUTE pixels (the schema format `verify.as_box` reads),
converted from the detectors' corner output in `xyxy_to_xywh` only. Repos and revisions
are written into every line's "pins"; thresholds are pinned by config_sha256.

Custody: every image must be in KTVIC train_data.json and absent from test_data.json,
and --out must be outside the repo, or the run stops. A killed run resumes: an image
is skipped only if its line has the same config sha, map sha and device as this run;
any other line in --out stops the run (CC-198 W1). GPU when available, else CPU.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


CONFIG = json.loads((HERE / "config.json").read_text(encoding="utf-8"))


def xyxy_to_xywh(box) -> list[float]:
    x1, y1, x2, y2 = (float(v) for v in box)
    return [round(x1, 2), round(y1, 2), round(x2 - x1, 2), round(y2 - y1, 2)]


def train_only_ids(ktvic: Path) -> set[str]:
    def names(split: str) -> set[str]:
        return {i["filename"] for i in json.loads((ktvic / f"{split}_data.json").read_text())["images"]}
    train, test = names("train"), names("test")
    return train - test


def gdino_label_to_prompt(label: str, prompts: list[str]) -> str | None:
    """GroundingDINO returns the matched phrase tokens, which can be a fragment or a merge."""
    label = " ".join(label.lower().split())
    if label in prompts:
        return label
    words = set(label.split())
    best = max(prompts, key=lambda p: len(words & set(p.split())), default=None)
    return best if best is not None and words & set(best.split()) else None


def parse_line(line: str) -> dict | None:
    """A line cut short by a killed run is dropped; the image is detected again."""
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        return None


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_lines(path: Path, config_sha: str, map_sha: str, device: str | None = None) -> dict[str, dict]:
    """image_id -> line. STOP on a line from another config or map, or from another device
    (`device=None`: all lines must share one device)."""
    lines = {}
    if not path.exists():
        return lines
    for d in filter(None, map(parse_line, path.read_text(encoding="utf-8").splitlines())):
        if (d.get("config_sha256"), d.get("map_sha256")) != (config_sha, map_sha):
            raise SystemExit(f"CONFIG STOP: {path} line {d.get('image_id')} has another config/map sha")
        device = device or d.get("device")
        if d.get("device") != device:
            raise SystemExit(f"CONFIG STOP: {path} mixes devices ({d.get('device')} vs {device})")
        lines[d["image_id"]] = d
    return lines


def keep_top(boxes: list[list[float]]) -> list[list[float]]:
    return sorted(boxes, key=lambda b: -b[4])[: CONFIG["max_boxes_per_prompt"]]


class Detectors:
    def __init__(self, device: str):
        import torch
        from transformers import (AutoModelForZeroShotObjectDetection, AutoProcessor,
                                  Owlv2ForObjectDetection, Owlv2Processor)

        self.torch = torch
        self.device = device
        g, o = CONFIG["detectors"]["gdino"], CONFIG["detectors"]["owlv2"]
        self.g_proc = AutoProcessor.from_pretrained(g["repo"], revision=g["revision"])
        self.g_model = AutoModelForZeroShotObjectDetection.from_pretrained(g["repo"], revision=g["revision"]).to(device).eval()
        self.o_proc = Owlv2Processor.from_pretrained(o["repo"], revision=o["revision"])
        self.o_model = Owlv2ForObjectDetection.from_pretrained(o["repo"], revision=o["revision"]).to(device).eval()

    def gdino(self, image, prompts: list[str]) -> dict[str, list[list[float]]]:
        cfg = CONFIG["detectors"]["gdino"]
        out: dict[str, list[list[float]]] = {p: [] for p in prompts}
        step = CONFIG["gdino_prompts_per_call"]
        for i in range(0, len(prompts), step):
            chunk = prompts[i:i + step]
            inputs = self.g_proc(images=image, text=". ".join(chunk) + ".", return_tensors="pt").to(self.device)
            with self.torch.no_grad():
                raw = self.g_model(**inputs)
            res = self.g_proc.post_process_grounded_object_detection(
                raw, inputs.input_ids, threshold=cfg["box_threshold"], text_threshold=cfg["text_threshold"],
                target_sizes=[(image.height, image.width)])[0]
            for box, score, label in zip(res["boxes"].tolist(), res["scores"].tolist(), res["text_labels"]):
                prompt = gdino_label_to_prompt(label, chunk)
                if prompt is not None:
                    out[prompt].append(xyxy_to_xywh(box) + [round(score, 4)])
        return {p: keep_top(b) for p, b in out.items()}

    def owlv2(self, image, prompts: list[str]) -> dict[str, list[list[float]]]:
        cfg = CONFIG["detectors"]["owlv2"]
        inputs = self.o_proc(text=[[f"a photo of a {p}" for p in prompts]], images=image, return_tensors="pt").to(self.device)
        with self.torch.no_grad():
            raw = self.o_model(**inputs)
        # transformers scales by max(h, w) itself (OWLv2 pads to a square, bottom/right), so pass the real (h, w).
        res = self.o_proc.post_process_grounded_object_detection(
            raw, threshold=cfg["box_threshold"], target_sizes=[(image.height, image.width)])[0]
        out: dict[str, list[list[float]]] = {p: [] for p in prompts}
        for box, score, idx in zip(res["boxes"].tolist(), res["scores"].tolist(), res["labels"].tolist()):
            x, y, w, h = xyxy_to_xywh(box)
            # clip to the real image: padding sits right/bottom
            w, h = min(w, image.width - x), min(h, image.height - y)
            if w > 0 and h > 0:
                out[prompts[idx]].append([x, y, round(w, 2), round(h, 2), round(score, 4)])
        return {p: keep_top(b) for p, b in out.items()}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--records", required=True, type=Path)
    ap.add_argument("--images", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--map", type=Path, default=HERE / "vi_en_map.json")
    ap.add_argument("--ktvic", type=Path, default=ROOT / "data" / "datasets" / "ktvic")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--device", default="auto")
    args = ap.parse_args()

    from PIL import Image
    import torch

    if args.out.resolve().is_relative_to(ROOT):
        raise SystemExit("CUSTODY STOP: --out is inside the repo")
    device = ("cuda" if torch.cuda.is_available() else "cpu") if args.device == "auto" else args.device
    vi_en = json.loads(args.map.read_text(encoding="utf-8"))["map"]
    config_sha, map_sha = file_sha(HERE / "config.json"), file_sha(args.map)
    allowed = train_only_ids(args.ktvic)
    files = sorted(args.records.glob("*.json"))[: args.limit or None]
    done = read_lines(args.out, config_sha, map_sha, device)
    det = Detectors(device)
    pins = {k: {"repo": v["repo"], "revision": v["revision"]} for k, v in CONFIG["detectors"].items()}
    with args.out.open("a", encoding="utf-8") as fh:
        for f in files:
            rec = json.loads(f.read_text(encoding="utf-8"))
            if rec["file_name"] not in allowed:
                raise SystemExit(f"CUSTODY STOP: {rec['file_name']} is not a train-only KTVIC image")
            if rec["image_id"] in done:
                continue
            ents = {e["id"]: vi_en.get(str(e.get("category_vi") or "")) for e in rec["entities"]}
            prompts = sorted({p for p in ents.values() if p})
            t0 = time.time()
            image = Image.open(args.images / rec["file_name"]).convert("RGB")
            g = det.gdino(image, prompts) if prompts else {}
            o = det.owlv2(image, prompts) if prompts else {}
            line = {"image_id": rec["image_id"], "file_name": rec["file_name"], "size": [image.width, image.height],
                    "device": device, "seconds": round(time.time() - t0, 3), "pins": pins,
                    "config_sha256": config_sha, "map_sha256": map_sha,
                    "prompts": {p: {"gdino": g[p], "owlv2": o[p]} for p in prompts}, "entities": ents}
            fh.write(json.dumps(line, ensure_ascii=False) + "\n")
            fh.flush()
            print(f"{rec['file_name']} {len(prompts)} prompts {line['seconds']}s", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
