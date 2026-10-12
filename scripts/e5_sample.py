#!/usr/bin/env python
"""E5, step 1 (GPU): sample N detailed captions per KTVIC train image from base + adapter.

    python scripts/e5_sample.py --adapter $NCS_DATA/runs/fuse2_s42 --out e5_samples.jsonl \\
        --limit 1500 --n 6 --probe /root/probe500.npz

One jsonl row per image: image_id, file_name, samples[N], and with --probe also
p_exist{object: score} for every lexicon object a sample mentions that NO reference
caption names. The score is the E2 hidden-state probe (layer 24, "Trong ảnh có X
không?"), refit here on the E2 features and applied to features taken from the
BASE model (adapter disabled), because that is the model the probe was fitted on.
Images used to fit the probe are excluded from sampling: on them the probe has seen
the very labels it would be asked about.

The output is appended and resumable: rerunning skips image_ids already written.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from evaluate import KTVIC, PROMPTS, file_names, load_model, references  # noqa: E402
from probe_existence import LAYERS, ask  # noqa: E402

PROBE_LAYER = 24
SPLIT = "train_data.json"


def fit_probe(path: str, gold: dict[str, set[str]]):
    """Logistic probe on the E2 features, label = object named by any reference (as in E2)."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    d = np.load(path)
    meta = [m.split("|", 1) for m in d["meta"]]
    y = np.array([o in gold.get(i, set()) for i, o in meta], dtype=int)
    k = list(d["layers"]).index(PROBE_LAYER)
    probe = make_pipeline(StandardScaler(), LogisticRegression(C=0.05, max_iter=3000))
    probe.fit(d["h_img"][:, k].astype(np.float32), y)
    print(f"probe: layer {PROBE_LAYER}, {len(y)} queries, positive rate {y.mean():.3f}", flush=True)
    return probe, {i for i, _ in meta}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--adapter", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit", type=int, default=1500, help="0 = every eligible image")
    ap.add_argument("--images-file", default=None,
                    help="sample only image_ids listed here (one per line), e.g. the half the adapter did not train on")
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--temperature", type=float, default=0.8)
    ap.add_argument("--top-p", type=float, default=0.95)
    ap.add_argument("--max-new-tokens", type=int, default=160)
    ap.add_argument("--max-vision-tokens", type=int, default=512)
    ap.add_argument("--four-bit", action="store_true")
    ap.add_argument("--probe", default=None, help="E2 features (probe500.npz); enables p_exist")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--split", default=SPLIT)
    ap.add_argument("--prompt", default="detailed", choices=sorted(PROMPTS))
    args = ap.parse_args()

    import torch
    from PIL import Image

    from rescap.chair import objects_in

    refs = references(args.split)
    names = file_names(args.split)
    gold = {i: set().union(*[set(objects_in(c)) for c in cs]) for i, cs in refs.items()}
    probe, probe_ids = fit_probe(args.probe, gold) if args.probe else (None, set())

    keep = set(Path(args.images_file).read_text(encoding="utf-8").split()) if args.images_file else None
    pool = sorted(i for i in refs if names.get(i) and i not in probe_ids and (keep is None or i in keep))
    if not pool:
        sys.exit("no eligible image to sample")
    ids = sorted(random.Random(args.seed).sample(pool, args.limit)) if 0 < args.limit < len(pool) else pool
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out.exists():
        done = {json.loads(line)["image_id"] for line in out.read_text(encoding="utf-8").splitlines()}
    todo = [i for i in ids if i not in done]
    print(f"{len(ids)} images ({len(pool)} eligible), {len(done)} already done, {len(todo)} to go", flush=True)

    args.adapter = str(Path(args.adapter).expanduser())
    model, proc = load_model(args)
    torch.manual_seed(args.seed)
    k = LAYERS.index(PROBE_LAYER)
    prompt = proc.apply_chat_template(
        [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": PROMPTS[args.prompt]}]}],
        tokenize=False, add_generation_prompt=True)

    with out.open("a", encoding="utf-8") as fh:
        for n, image_id in enumerate(todo, 1):
            image = Image.open(KTVIC / "images" / names[image_id]).convert("RGB")
            inputs = proc(text=[prompt], images=[image], return_tensors="pt").to(model.device)
            with torch.no_grad():
                # top_k=0 explicitly: Qwen's generation_config otherwise leaves sampling near-greedy
                seqs = model.generate(**inputs, do_sample=True, temperature=args.temperature,
                                      top_p=args.top_p, top_k=0, num_return_sequences=args.n,
                                      max_new_tokens=args.max_new_tokens)
            samples = [s.strip() for s in proc.batch_decode(
                seqs[:, inputs.input_ids.shape[1]:], skip_special_tokens=True)]
            row = {"image_id": image_id, "file_name": names[image_id], "samples": samples}
            if probe is not None:
                extra = sorted({o for s in samples for o in objects_in(s)} - gold[image_id])
                if extra:
                    with model.disable_adapter():
                        h = np.stack([ask(model, proc, image, o)[0][k] for o in extra])
                    row["p_exist"] = dict(zip(extra, probe.predict_proba(h)[:, 1].round(4).tolist()))
                else:
                    row["p_exist"] = {}
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            fh.flush()
            if n % 25 == 0 or n == len(todo):
                print(f"  {n}/{len(todo)}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
