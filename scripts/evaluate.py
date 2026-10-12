#!/usr/bin/env python
"""Score captions against KTVIC test and print a table comparable to the paper's.

    # score a file of predictions
    python scripts/evaluate.py --predictions preds.json --prompt detailed --name "VSPS-D"

    # generate with a model, then score
    python scripts/evaluate.py --model qwen2.5-vl-7b --prompt short --name "Qwen zero-shot"
    python scripts/evaluate.py --model qwen2.5-vl-7b --adapter ~/ncs-data/runs/dpo --prompt detailed

    # another dataset laid out like KTVIC under $NCS_DATA/datasets
    NCS_DATASET=uitviic python scripts/evaluate.py --model qwen2.5-vl-7b --prompt short --name uitviic_zeroshot-short

`--predictions` takes `{image_id: "caption"}` or `{image_id: ["caption"]}`.

**Two things here exist to stop a wrong table being printed.**

*Scale.* `pycocoevalcap` returns CIDEr on its raw scale -- a perfect prediction
scores about 3.4 -- while every published KTVIC number is ×100. GRIT's 136.0 is
1.36 raw. Reporting the raw figure beside theirs would understate us by two
orders of magnitude, and reporting theirs beside our raw one would do the
reverse. Everything is converted once, here, and the column says which scale it
is in.

*Tokenization.* Vietnamese metrics depend on the segmenter, and only
RDRSegmenter reproduces KTVIC's own `segment_caption` (100% against
underthesea's 82.6%, ). The segmenter and its version are printed with the
scores and written into the results file, because a Vietnamese n-gram score
without them cannot be checked by anyone.

**Generation and scoring do not share a process.** RDRSegmenter runs on the JVM
through `jnius`, and starting a JVM in a process that has already initialised
CUDA deadlocks -- observed here as an evaluation stopping dead on
`Loading Word Segmentation model` after captioning all 150 images, while the
identical scoring code ran in 0.3 s in a process that had never touched the GPU.
Predictions are therefore written to disk the moment generation ends, and
scoring re-executes this script with `--predictions`. The GPU work survives any
scoring failure, which it did not before: three runs were lost to this.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

DATA = Path(os.environ.get("NCS_DATA", Path.home() / "ncs-data"))
#: The dataset every split name refers to: KTVIC, unless NCS_DATASET names another
#: directory under DATA/datasets with the same layout (e.g. `uitviic`). Read here so
#: the scoring subprocess and every script importing KTVIC/references follow it.
KTVIC = DATA / "datasets" / os.environ.get("NCS_DATASET", "ktvic")
#: Two prompts, because the reference style decides what a metric can reward.
#: KTVIC references are ONE short sentence (~12 words); a detailed caption is
#: 8x longer and CIDEr's length penalty removes it entirely. Which prompt was
#: used therefore has to travel with the number.
PROMPTS = {
    "detailed": "Mô tả chi tiết bức ảnh này bằng tiếng Việt.",
    "short": (
        "Mô tả bức ảnh này bằng MỘT câu tiếng Việt ngắn gọn, "
        "giống chú thích ảnh. Không liệt kê, không giải thích."
    ),
    # length-matched control for the two-sentence detailed output of reference-fusion SFT
    "two": (
        "Mô tả bức ảnh này bằng HAI câu tiếng Việt ngắn gọn, "
        "giống chú thích ảnh. Không liệt kê, không giải thích."
    ),
    # instructed-zero-shot baseline: the steelman for the question "is a clever
    # prompt enough?"; every constraint of the main system is stated explicitly in the prompt.
    "instructed": (
        "Mô tả chi tiết bức ảnh này bằng tiếng Việt. CHỈ nêu những gì thấy "
        "rõ ràng trong ảnh, không suy đoán. Nếu không chắc giới tính của "
        "người trong ảnh, dùng từ trung tính \"người\". Không đoán màu sắc "
        "khi không nhìn rõ. Không dùng từ rào đón như \"có vẻ\", \"dường như\"."
    ),
    # English replication on the same images (scripts/crosslingual_gap.py): a `-<mode>_en` result is
    # scored as English -- PTB tokenizer, SPICE, CHAIR over the 80 COCO classes (chair_en).
    "short_en": "Describe this image in ONE short English sentence, like a caption. Do not list items or explain.",
    "detailed_en": "Describe this image in detail in English.",
}
PROMPT = PROMPTS["detailed"]

#: pycocoevalcap's raw scale -> the ×100 convention every KTVIC number uses.
PUBLISHED_SCALE = 100.0
SCALED = ("BLEU-1", "BLEU-2", "BLEU-3", "BLEU-4", "METEOR", "ROUGE-L", "CIDEr", "SPICE")


def resolve_prompt(flag: str | None, predictions: str | None) -> str:
    """The prompt style a score belongs to: `--prompt`, else the `-<mode>` suffix
    of the predictions file name. Refuses when neither says, or when they disagree.

    A silent default here once scored short captions as `detailed`: METEOR was
    skipped and the results file recorded the wrong `prompt_style`.
    """
    named = None
    if predictions:
        stem = Path(predictions).name.split(".")[0]
        named = next((m for m in PROMPTS if stem.endswith(f"-{m}")), None)
    if flag and named and flag != named:
        raise SystemExit(f"--prompt {flag} contradicts the file name {predictions!r} ({named})")
    if flag or named:
        return flag or named
    raise SystemExit("--prompt is required (it cannot be read from the predictions file name)")


def _self_check() -> None:
    assert resolve_prompt(None, "x/zeroshot-short.preds.json") == "short"
    assert resolve_prompt(None, "main_s44re-detailed.preds.json") == "detailed"
    assert resolve_prompt("short", "roundA-short.preds.json") == "short"
    assert resolve_prompt("short", "preds.json") == "short"
    assert resolve_prompt(None, "x/uitviic_en_p1_s42-short_en.preds.json") == "short_en"
    assert resolve_prompt(None, "coco_en_zeroshot-detailed_en.preds.json") == "detailed_en"
    c = chair_en({"1": "A dog and a man on a motor bike near a hot dog stand."},
                 {"1": ["A man rides a motorcycle.", "A person with a dog."]})
    assert (c.n_mentions, c.n_hallucinated_mentions, dict(c.top_hallucinated)) == (4, 1, {"hot dog": 1}), c
    for flag, path in ((None, "preds.json"), ("detailed", "a-short.preds.json"), (None, None)):
        try:
            resolve_prompt(flag, path)
        except SystemExit:
            continue
        raise AssertionError((flag, path))
    assert model_id(None) == model_id("qwen2.5-vl-7b") == "Qwen/Qwen2.5-VL-7B-Instruct"
    assert model_id("qwen2.5-vl-3b") == "Qwen/Qwen2.5-VL-3B-Instruct"
    import tempfile

    with tempfile.TemporaryDirectory() as adapter:
        (Path(adapter) / "adapter_config.json").write_text(
            json.dumps({"base_model_name_or_path": model_id("qwen2.5-vl-3b")}), encoding="utf-8")
        check_adapter_base(adapter, model_id("qwen2.5-vl-3b"))
        try:
            check_adapter_base(adapter, model_id(None))
            raise AssertionError("a 3B adapter was accepted on the 7B")
        except SystemExit as refused:
            assert "Qwen2.5-VL-3B-Instruct" in str(refused)
    print("self-check ok")


def chair_en(predictions: dict[str, str], references: dict[str, list[str]]):
    """rescap.chair's CHAIR for English captions: mentions are the 80 COCO classes (score_coco_probe.en_classes,
    Rohrbach's synonyms) and gold is what the references name, so like CHAIR-vi it is an UPPER BOUND."""
    import score_coco_probe as sc
    from rescap.chair import ChairResult

    syn = sc.load_synonyms()
    result = ChairResult(notes=["English: 80 COCO classes (score_coco_probe.en_classes); gold drawn from "
                                "the reference captions, an UPPER BOUND"])
    for image_id, caption in predictions.items():
        gold = set().union(*(sc.en_classes(r, syn) for r in references[image_id]))
        mentioned = sorted(sc.en_classes(caption, syn))
        invented = [c for c in mentioned if c not in gold]
        result.n_captions += 1
        result.n_mentions += len(mentioned)
        result.n_hallucinated_mentions += len(invented)
        result.n_captions_with_hallucination += bool(invented)
        result.top_hallucinated.update(invented)
        result.per_caption.append({"image_id": image_id, "n_mentions": len(mentioned), "hallucinated": invented})
    return result


def references(split: str) -> dict[str, list[str]]:
    data = json.loads((KTVIC / split).read_text(encoding="utf-8"))
    refs: dict[str, list[str]] = {}
    for ann in data.get("annotations", []):
        if ann.get("caption"):
            refs.setdefault(str(ann["image_id"]), []).append(ann["caption"])
    return refs


def file_names(split: str) -> dict[str, str]:
    data = json.loads((KTVIC / split).read_text(encoding="utf-8"))
    return {
        str(img.get("id", img.get("image_id"))): img.get("file_name") or img.get("filename")
        for img in data.get("images", [])
    }


def model_id(name: str | None) -> str:
    """HF id of a `--model` short name (rescap/vlm/registry.py); None is the 7B main backbone."""
    from rescap.vlm import get_vlm

    return get_vlm(name or "qwen2.5-vl-7b").model_id


def check_adapter_base(adapter: str, base_id: str) -> None:
    """Refuse an adapter trained on another backbone, before a 15 GB load.

    PEFT records the base in adapter_config.json. Without this a 3B adapter on the 7B
    dies inside PEFT as a wall of size mismatches, and a wrong `--model` with no
    adapter would score the wrong backbone under the requested name.
    """
    base = json.loads((Path(adapter) / "adapter_config.json").read_text(
        encoding="utf-8")).get("base_model_name_or_path")
    if base != base_id:
        raise SystemExit(f"adapter {adapter} was trained on {base}, not {base_id}")


def load_model(args):
    """Qwen2.5-VL `args.model` (default 7B; + `args.adapter`) in eval mode, and its processor."""
    import torch
    from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration

    from rescap.vlm.base import dtype_kwarg

    base_id = model_id(getattr(args, "model", None))  # e5_sample's args have no --model
    if args.adapter:
        check_adapter_base(args.adapter, base_id)
    P = 28 * 28
    load_kw = dict(attn_implementation="sdpa", device_map={"": 0},
                   **dtype_kwarg(torch.bfloat16))
    if args.four_bit:
        from transformers import BitsAndBytesConfig

        load_kw["quantization_config"] = BitsAndBytesConfig(
            load_in_4bit=True, bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16, bnb_4bit_use_double_quant=True)

    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(base_id, **load_kw)
    if args.adapter:
        from peft import PeftModel

        model = PeftModel.from_pretrained(model, args.adapter)
        print(f"  adapter: {args.adapter}")
    model.eval()
    processor = AutoProcessor.from_pretrained(
        base_id, min_pixels=256 * P, max_pixels=args.max_vision_tokens * P)
    return model, processor


def generate(args, image_ids: list[str]) -> dict[str, list[str]]:
    """Caption each image with the model under test."""
    import torch
    from PIL import Image

    names = file_names(args.split)
    model, processor = load_model(args)
    out: dict[str, list[str]] = {}
    # Tags-in-prompt baseline: {image_id: [Vietnamese object names]} from scripts/tag_images.py.
    tags = json.loads(Path(args.tags).read_text(encoding="utf-8")) if args.tags else {}
    started = time.time()
    for n, image_id in enumerate(image_ids, 1):
        image = Image.open(KTVIC / "images" / names[image_id]).convert("RGB")
        prompt = args.prompt_text
        if tags.get(image_id):
            prompt += " Các đối tượng có thể có trong ảnh: " + ", ".join(tags[image_id]) + "."
        messages = [{"role": "user", "content": [
            {"type": "image"}, {"type": "text", "text": prompt}]}]
        text = processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True)
        inputs = processor(text=[text], images=[image], return_tensors="pt").to(model.device)
        with torch.no_grad():
            ids = model.generate(**inputs, max_new_tokens=args.max_new_tokens,
                                 do_sample=False)
        trimmed = ids[:, inputs.input_ids.shape[1]:]
        out[image_id] = [processor.batch_decode(
            trimmed, skip_special_tokens=True)[0].strip()]
        if n % 25 == 0 or n == len(image_ids):
            rate = (time.time() - started) / n
            print(f"  [{n}/{len(image_ids)}] {rate:.2f}s/image  "
                  f"~{(len(image_ids)-n)*rate/60:.0f} min left", flush=True)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", default="test_data.json")
    parser.add_argument("--predictions", default=None)
    parser.add_argument("--model", default=None,
                        help="backbone short name from rescap/vlm/registry.py: qwen2.5-vl-7b or qwen2.5-vl-3b")
    parser.add_argument("--adapter", default=None)
    parser.add_argument("--name", default="system")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--max-new-tokens", type=int, default=160)
    parser.add_argument("--max-vision-tokens", type=int, default=512)
    parser.add_argument("--four-bit", action="store_true")
    parser.add_argument("--tags", default=None,
                        help="JSON {image_id: [vi tags]} appended to the prompt (scripts/tag_images.py)")
    parser.add_argument(
        "--prompt", default=None, choices=sorted(PROMPTS),
        help=("`short` matches the KTVIC reference style (one sentence); "
              "`detailed` is what the paper actually wants to generate. "
              "Required unless the predictions file name ends in -<mode>"),
    )
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument(
        "--score-here", action="store_true",
        help="score inside this very process (used internally once --predictions exists)",
    )
    parser.add_argument("--out", default=None)
    parser.add_argument("--segmenter", default="rdrsegmenter")
    parser.add_argument(
        "--also-syllable", action="store_true",
        help="add a syllable-level (whitespace) table for the appendix",
    )
    args = parser.parse_args()
    if args.self_check:
        _self_check()
        return 0
    args.prompt = resolve_prompt(args.prompt, args.predictions)
    args.prompt_text = PROMPTS[args.prompt]

    refs = references(args.split)
    # A split with no captions at all (coco_vi: COCO has no Vietnamese references) is captioned, never scored.
    image_ids = sorted(refs or file_names(args.split))
    if args.limit:
        image_ids = image_ids[: args.limit]
    print(f"{args.split}: {len(image_ids)} images")

    if args.predictions:
        if not refs:
            raise SystemExit(f"{KTVIC.name}/{args.split} has no reference captions: nothing to score")
        raw = json.loads(Path(args.predictions).read_text(encoding="utf-8"))
        preds = {str(k): (v if isinstance(v, list) else [v]) for k, v in raw.items()}
    elif args.model:
        preds = generate(args, image_ids)
        # Written before anything else can fail. Generation is the expensive
        # half and it must not be repeated because scoring broke.
        pred_path = Path(args.out or DATA / "results" /
                         f"{args.name.replace(' ', '_')}.json").with_suffix(".preds.json")
        pred_path.parent.mkdir(parents=True, exist_ok=True)
        pred_path.write_text(
            json.dumps({i: preds[i][0] for i in image_ids}, ensure_ascii=False, indent=1),
            encoding="utf-8")
        print(f"\n  saved predictions -> {pred_path}")
        if not refs:
            print("  no reference captions in this split: predictions only, nothing scored")
            return 0

        if not args.score_here:
            # A fresh interpreter, so the JVM starts in a process with no CUDA
            # context. See the module docstring.
            import subprocess

            argv = [sys.executable, __file__, "--predictions", str(pred_path),
                    "--name", args.name, "--split", args.split,
                    "--segmenter", args.segmenter, "--prompt", args.prompt,
                    "--score-here"]
            if args.limit:
                argv += ["--limit", str(args.limit)]
            if args.also_syllable:
                argv += ["--also-syllable"]
            if args.out:
                argv += ["--out", args.out]
            print(f"  scoring in a separate process (the JVM does not share one with CUDA)…\n")
            return subprocess.call(argv)
    else:
        raise SystemExit("need --predictions or --model")

    missing = [i for i in image_ids if i not in preds]
    if missing:
        # Scoring only the images a model happened to caption would report a
        # number for an easier subset than the one everyone else reports on.
        raise SystemExit(
            f"missing predictions for {len(missing)} / {len(image_ids)} images "
            f"(e.g. {missing[:3]}). No subset scoring — the number would not be "
            f"comparable to GRIT's 558 images."
        )

    from rescap.metrics import CaptionMetrics

    gt = {i: refs[i] for i in image_ids}
    rows = []
    english = args.prompt.endswith("_en")
    modes = [("word-level", args.segmenter)]
    if args.also_syllable:
        modes.append(("syllable (whitespace)", "whitespace"))
    if english:
        modes = [("PTB", "ptb")]

    for label, segmenter in modes:
        # `tokenize` stays True for both: syllable level is a segmenter that
        # happens to be the identity, not an absence of tokenization. Passing
        # tokenize=False skips the step that turns the aligned structures into
        # plain strings, and the scorers then hang on dicts.
        # METEOR runs a JVM over a pipe: pycocoevalcap writes ALL lines before
        # reading — 558 DETAILED captions overflow the pipe buffer and deadlock
        # (measured 19/08: scoring short passes, scoring detailed hangs identically
        # on two different machines). Short captions still get METEOR normally.
        use_meteor = not args.prompt.startswith("detailed")
        scorer = CaptionMetrics(language="en" if english else "vi", use_meteor=use_meteor,
                                use_spice=english, tokenize=True, segmenter=segmenter)
        scores = scorer.compute(gt, {i: preds[i] for i in image_ids})
        if use_meteor and scores.get("METEOR") is None:
            raise SystemExit("METEOR was requested but not computed; refusing to write a "
                             "table without it:\n  " + "\n  ".join(scorer.warnings))
        if not use_meteor:
            scorer.warnings.append("METEOR not computed: detailed captions deadlock "
                                   "pycocoevalcap's METEOR pipe")
        scaled = {k: (v * PUBLISHED_SCALE if k in SCALED and isinstance(v, float) else v)
                  for k, v in scores.items()}
        # scorer.segmenter, NOT the loop variable: when VnCoreNLP is absent, the
        # scorer renames itself "...!whitespace-fallback" and that name must follow
        # the scores into the JSON — writing the requested name instead would let a
        # fallback score masquerade as a proper one, and no later audit could catch it.
        rows.append({"tokenization": label, "segmenter": scorer.segmenter,
                     "scores_scaled_x100": scaled, "scores_raw": scores,
                     "warnings": list(scorer.warnings)})

    print(f"\n{'='*72}\n  {args.name}   ({len(image_ids)} images, ×100 scale as KTVIC publishes)\n{'='*72}")
    header = f"  {'metric':<12}" + "".join(f"{r['tokenization']:>24}" for r in rows)
    print(header + "\n  " + "-" * (len(header) - 2))
    for key in ("BLEU-1", "BLEU-4", "METEOR", "ROUGE-L", "CIDEr") + (("SPICE",) if english else ()):
        line = f"  {key:<12}"
        for r in rows:
            v = r["scores_scaled_x100"].get(key)
            line += f"{v:>24.1f}" if isinstance(v, float) else f"{'n/a':>24}"
        print(line)
    # CHAIR alongside the n-gram table, because the two disagree about what a
    # long caption is worth and a reader needs to see both at once. It is a
    # RELATIVE measure here: gold comes from the reference captions, so an
    # object no annotator mentioned counts as invented (`rescap/chair.py`).
    from rescap.chair import chair

    captions = {i: preds[i][0] for i in image_ids}
    chair_result = chair_en(captions, gt) if english else chair(captions, gt, strict_ids=False)
    print(f"\n  object hallucination (CHAIR — gold drawn from captions, an UPPER BOUND):")
    print(f"    CHAIR_s {chair_result.chair_s*100:>5.1f}%   "
          f"CHAIR_i {chair_result.chair_i*100:>5.1f}%   "
          f"{chair_result.mentions_per_caption:.2f} objects/caption")
    top = ", ".join(f"{k}({v})" for k, v in chair_result.top_hallucinated.most_common(6))
    print(f"    most invented: {top}")
    print(f"    ⚠ CHAIR_s scales with caption LENGTH — only compare systems "
          f"of the SAME length ")

    if KTVIC.name == "ktvic":
        print(f"\n  reference — GRIT (KTVIC Table 3, same 558 images):")
        # Source: KTVIC paper (arXiv 2401.08100), Table 3, row "3) GRIT".
        print(f"    CIDEr 136.0 · BLEU-1 74.7 · BLEU-4 40.6 · METEOR 36.6 · ROUGE-L 59.7")
    for r in rows:
        for w in r["warnings"]:
            print(f"  ! {w}")

    out = Path(args.out or DATA / "results" / f"{args.name.replace(' ', '_')}.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "name": args.name, "split": args.split, "n_images": len(image_ids),
        "prompt_style": args.prompt, "prompt": args.prompt_text,
        "adapter": args.adapter, "model": args.model,
        "scale": "x100 (as KTVIC's published numbers)",
        "results": rows,
        "chair": chair_result.as_dict(),
        "predictions": {i: preds[i][0] for i in image_ids},
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
