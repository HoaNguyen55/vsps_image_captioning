#!/usr/bin/env python
"""Build SFT data from KTVIC's GOLD CAPTIONS — the P1 baseline.

    python scripts/build_gold_sft.py \\
        --annotations ~/ncs-data/datasets/ktvic/train_data.json \\
        --out ~/ncs-data/stage2_gold

Why this exists: the most natural reviewer question is *"there are 3,769
images with human-written captions — why not SFT directly on those?"*. The
paper must have a number to answer with. The honest, pre-registered prediction
is that gold-SFT may BEAT distillation on concise-mode CIDEr (it learns the
exact reference style); what it cannot learn is detail + guardedness, and
Table 2 measures exactly that.

For a fair comparison with the distillation branch (same images, same epochs,
same prompt):

* ONE caption per image (the first caption in file order — KTVIC does not
  mark a "primary" caption), not all ~5 — the distillation branch likewise
  has only one answer per image per style.
* The prompt is the EXACT short evaluation prompt (`PROMPT_SHORT` from
  build_dpo_data.py) — the model is asked at scoring time just as at
  training time.
* NO detailed variant: a gold caption is a single sentence; inventing a
  detailed style from it would be fabricating data. In detailed mode this
  model answers with whatever it retains from pretraining — and that is
  precisely the measurement.

`dpo.jsonl` is not produced: gold captions carry no verdicts, so no
preference pairs exist — running `train_stage2.py --stage sft` is enough.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_dpo_data import PROMPT, PROMPT_SHORT  # the same prompts, not re-typed by hand

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rescap.chair import objects_in


def consensual(captions: list[str]) -> str:
    """The caption naming the most objects that another annotator also names."""
    objs = [set(objects_in(c)) for c in captions]
    shared = lambda i: sum(any(o in objs[j] for j in range(len(objs)) if j != i) for o in objs[i])
    return captions[max(range(len(captions)), key=lambda i: (shared(i), -i))]


def fused(captions: list[str], k: int) -> str:
    """Start from the consensual caption, then add up to k-1 captions, each the one
    contributing the most objects not yet named; a caption adding none is not used.
    Every object in the result was written by an annotator, so fusion adds coverage
    without adding content nobody saw."""
    first = consensual(captions)
    chosen, named = [first], set(objects_in(first))
    rest = [c for c in captions if c != first]
    while len(chosen) < k and rest:
        best = max(rest, key=lambda c: len(set(objects_in(c)) - named))
        if not set(objects_in(best)) - named:
            break
        chosen.append(best); named |= set(objects_in(best)); rest.remove(best)
    return " ".join(c if c.rstrip().endswith((".", "!", "?")) else c.rstrip() + "." for c in chosen)


def halves(image_ids, seed: int) -> tuple[list[str], list[str]]:
    """Seeded split of images into two disjoint halves A/B (cross-fitting: a model trained
    on one half samples captions on the other, images it has never seen)."""
    ids = sorted(image_ids)
    random.Random(seed).shuffle(ids)
    return sorted(ids[: len(ids) // 2]), sorted(ids[len(ids) // 2:])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--annotations", required=True,
                        help="KTVIC's train_data.json")
    parser.add_argument("--out", required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--select", choices=("first", "consensus", "all"), default="first",
                        help="short-row caption: file order (P1), the most consensual one, or every caption (multi-reference SFT)")
    parser.add_argument("--fuse", type=int, default=1,
                        help="k > 1 adds a detailed-prompt row fusing up to k captions per image")
    parser.add_argument("--images-file", default=None,
                        help="keep only the image_ids listed in this file (one per line)")
    parser.add_argument("--write-halves", default=None, metavar="DIR",
                        help="write DIR/A.txt and DIR/B.txt (seeded split of the captioned images) and exit")
    parser.add_argument("--limit", type=int, default=0,
                        help="limit the number of images (0 = all) — for quick trials only")
    args = parser.parse_args()

    data = json.loads(Path(args.annotations).expanduser().read_text(encoding="utf-8"))
    file_names = {
        str(img.get("id", img.get("image_id"))): img.get("file_name") or img.get("filename")
        for img in data.get("images", [])
    }

    captions: dict[str, list[str]] = {}
    n_captions = 0
    for ann in data.get("annotations", []):
        image_id = str(ann["image_id"])
        caption = (ann.get("caption") or "").strip()
        if not caption:
            continue
        n_captions += 1
        captions.setdefault(image_id, []).append(caption)

    if args.write_halves:
        dst = Path(args.write_halves).expanduser()
        dst.mkdir(parents=True, exist_ok=True)
        for name, part in zip("AB", halves(captions, args.seed)):
            (dst / f"{name}.txt").write_text("\n".join(part) + "\n", encoding="utf-8")
            print(f"  {len(part)} images -> {dst / name}.txt")
        return 0
    if args.images_file:
        keep = set(Path(args.images_file).expanduser().read_text(encoding="utf-8").split())
        captions = {i: cs for i, cs in captions.items() if i in keep}
        n_captions = sum(map(len, captions.values()))
        if not captions:
            sys.exit(f"no captioned image of {args.annotations} is listed in {args.images_file}")

    pick = (lambda cs: cs[0]) if args.select != "consensus" else consensual
    rows = []
    for image_id, cs in sorted(captions.items()):
        if not file_names.get(image_id):
            continue
        base = {"image_id": image_id, "file_name": file_names[image_id]}
        for c in (cs if args.select == "all" else [pick(cs)]):
            rows.append({**base, "prompt": PROMPT_SHORT, "response": c, "variant": "gold"})
        if args.fuse > 1:
            rows.append({**base, "prompt": PROMPT, "response": fused(cs, args.fuse),
                         "variant": f"gold_fused{args.fuse}"})
    dropped = len(captions) - len({r["image_id"] for r in rows})
    if args.limit:
        rows = rows[: args.limit]

    rng = random.Random(args.seed)
    rng.shuffle(rows)

    dst = Path(args.out).expanduser()
    dst.mkdir(parents=True, exist_ok=True)
    with (dst / "sft.jsonl").open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    report = {
        "source": str(args.annotations), "seed": args.seed, "images_file": args.images_file,
        "baseline": "gold_sft (P1, )",
        "images_with_caption": len(captions),
        "captions_total": n_captions,
        "captions_used": len(rows),
        "policy": (f"short row: {args.select} caption, PROMPT_SHORT; "
                   + (f"detailed row: up to {args.fuse} fused captions, PROMPT" if args.fuse > 1
                      else "no detailed variant")),
        "dropped_no_file_name": dropped,
    }
    (dst / "_build_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"  {len(rows)} gold-SFT examples (from {n_captions} captions / "
          f"{len(captions)} images, select={args.select}, fuse={args.fuse})")
    if dropped:
        print(f"  ⚠ {dropped} images dropped because file_name could not be resolved")
    print(f"  -> {dst/'sft.jsonl'}\n"
          f"  run: train_stage2.py --stage sft --data {dst} --epochs 2")
    return 0


def _check() -> None:
    cs = ["một người đàn ông đứng.", "một người đàn ông và con chó", "con chó cạnh chiếc xe máy"]
    assert consensual(cs) == cs[1]
    assert fused(cs, 2) == "một người đàn ông và con chó. con chó cạnh chiếc xe máy.", fused(cs, 2)
    assert fused(cs[:1], 3) == cs[0]
    ids = [str(i) for i in range(101)]
    a, b = halves(ids, 42)
    assert not set(a) & set(b) and sorted(a + b) == sorted(ids) and abs(len(a) - len(b)) <= 1
    assert (a, b) == halves(reversed(ids), 42) and a != halves(ids, 43)[0]


if __name__ == "__main__":
    _check()
    sys.exit(main())
