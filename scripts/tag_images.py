#!/usr/bin/env python
"""Off-the-shelf object tags per KTVIC image, in Vietnamese, for the tags-in-prompt baseline.

    python scripts/tag_images.py --out $NCS_DATA/results/tags_gdino.json
    python scripts/evaluate.py --model qwen2.5-vl-7b --tags $NCS_DATA/results/tags_gdino.json ...

Tagger: Grounding DINO (IDEA-Research/grounding-dino-base) through HF transformers,
queried with the 80 COCO class names. Chosen over RAM++ because it needs no new
package (RAM++ ships as a git-only repo with its own timm/fairscale pins) and because
the repo's only English->Vietnamese lexicon is `data/coco_probe/coco80_vi.json`:
RAM++'s 4.5k open tags would mostly be dropped for want of a translation anyway.
Each detected class is written as the first Vietnamese entry of that lexicon.

Output: {image_id: ["người", "xe máy", ...]} ordered by detector confidence.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from evaluate import KTVIC, file_names, references  # noqa: E402

LEXICON = ROOT / "data" / "coco_probe" / "coco80_vi.json"
MODEL = "IDEA-Research/grounding-dino-base"


def to_class(label: str, classes: list[str]) -> str | None:
    """Grounding DINO returns the prompt phrase(s) its box matched; map back to one COCO class."""
    label = label.strip()
    if label in classes:
        return label
    hits = [c for c in classes if c in label]
    return max(hits, key=len) if hits else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--split", default="test_data.json")
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--box-threshold", type=float, default=0.35)
    ap.add_argument("--text-threshold", type=float, default=0.25)
    args = ap.parse_args()

    import torch
    from PIL import Image
    from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor

    vi = {k: v[0] for k, v in json.loads(LEXICON.read_text(encoding="utf-8")).items()
          if not k.startswith("_")}
    classes = list(vi)
    # Two prompts of 40 classes: all 80 overflow Grounding DINO's 256-token text limit.
    chunks = [". ".join(classes[i:i + 40]) + "." for i in range(0, len(classes), 40)]

    proc = AutoProcessor.from_pretrained(MODEL)
    model = AutoModelForZeroShotObjectDetection.from_pretrained(MODEL).to("cuda").eval()
    names = file_names(args.split)
    ids = sorted(references(args.split))[: args.limit or None]

    out: dict[str, list[str]] = {}
    for n, image_id in enumerate(ids, 1):
        image = Image.open(KTVIC / "images" / names[image_id]).convert("RGB")
        best: dict[str, float] = {}
        for text in chunks:
            inputs = proc(images=image, text=text, return_tensors="pt").to("cuda")
            with torch.no_grad():
                outputs = model(**inputs)
            r = proc.post_process_grounded_object_detection(
                outputs, inputs.input_ids, threshold=args.box_threshold,
                text_threshold=args.text_threshold, target_sizes=[image.size[::-1]])[0]
            for label, score in zip(r.get("text_labels", r["labels"]), r["scores"].tolist()):
                c = to_class(label, classes)
                if c:
                    best[c] = max(best.get(c, 0.0), score)
        out[image_id] = [vi[c] for c in sorted(best, key=best.get, reverse=True)]
        if n % 50 == 0 or n == len(ids):
            print(f"  [{n}/{len(ids)}] {image_id}: {', '.join(out[image_id])}", flush=True)

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {args.out}: {sum(map(len, out.values())) / len(out):.2f} tags/image")
    return 0


if __name__ == "__main__":
    sys.exit(main())
