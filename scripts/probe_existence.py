#!/usr/bin/env python
"""E2: does Qwen2.5-VL-7B's internal state know which proposed objects exist?

    python scripts/probe_existence.py extract --records <stage1 dir> --images <dir> --out probe.npz --limit 500
    python scripts/probe_existence.py score --records <stage1 dir> --feats probe.npz

`extract` (GPU) asks "Trong ảnh có X không?" for every lexicon object named in an
image's Stage-1 propositions, once with the image and once without it, and keeps the
last-token hidden state at a few layers plus P(có) from the next-token logits.
The no-image pass is the prior-leakage control: a probe that scores as well without
the image is reading the object prior, not the picture.

`score` (CPU) fits a logistic probe per layer with 5-fold cross-validation grouped by
image, against y = object named by any reference caption, and compares AUROC with
Vintern's stored self-consistency votes and the stored-signal reranker features.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

LAYERS = (8, 16, 20, 24, 28)
QUESTION = "Trong ảnh có {} không? Chỉ trả lời 'có' hoặc 'không'."


def candidates(records: Path, limit: int) -> list[tuple[dict, list[str]]]:
    from rescap.chair import objects_in

    out = []
    for f in sorted(records.glob("*.json"))[:limit]:
        r = json.loads(f.read_text(encoding="utf-8"))
        objs = sorted({o for p in r["propositions"] for o in objects_in(p["text_vi"])})
        if objs:
            out.append((r, objs))
    return out


def extract(args) -> None:
    import torch
    from PIL import Image
    from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration

    from rescap.vlm.base import dtype_kwarg

    mid = "Qwen/Qwen2.5-VL-7B-Instruct"
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        mid, attn_implementation="sdpa", device_map={"": 0}, **dtype_kwarg(torch.bfloat16)).eval()
    proc = AutoProcessor.from_pretrained(mid, min_pixels=256 * 784, max_pixels=512 * 784)
    tok = proc.tokenizer
    yes = [tok.encode(w, add_special_tokens=False)[0] for w in ("có", "Có")]
    no = [tok.encode(w, add_special_tokens=False)[0] for w in ("không", "Không")]

    @torch.no_grad()
    def ask(image, obj):
        content = ([{"type": "image"}] if image is not None else []) + [
            {"type": "text", "text": QUESTION.format(obj)}]
        text = proc.apply_chat_template([{"role": "user", "content": content}],
                                        add_generation_prompt=True)
        inputs = proc(text=[text], images=[image] if image is not None else None,
                      return_tensors="pt").to(0)
        o = model(**inputs, output_hidden_states=True)
        p = o.logits[0, -1].float().softmax(-1)
        p_yes = (p[yes].sum() / (p[yes].sum() + p[no].sum())).item()
        return np.stack([o.hidden_states[L][0, -1].float().cpu().numpy() for L in LAYERS]), p_yes

    meta, h_img, h_txt, py_img, py_txt = [], [], [], [], []
    items = candidates(Path(args.records), args.limit)
    for n, (r, objs) in enumerate(items, 1):
        image = Image.open(Path(args.images) / r["file_name"]).convert("RGB")
        for obj in objs:
            a, pa = ask(image, obj)
            b, pb = ask(None, obj)
            meta.append(f"{r['image_id']}|{obj}")
            h_img.append(a.astype(np.float16)); h_txt.append(b.astype(np.float16))
            py_img.append(pa); py_txt.append(pb)
        if n % 25 == 0:
            print(f"  {n}/{len(items)} images, {len(meta)} queries", flush=True)
    np.savez_compressed(args.out, meta=np.array(meta), h_img=np.stack(h_img), h_txt=np.stack(h_txt),
                        py_img=np.array(py_img), py_txt=np.array(py_txt), layers=np.array(LAYERS))
    print(f"saved {len(meta)} queries -> {args.out}")


def vintern_yes(r: dict) -> dict[str, float]:
    """Highest share of 'có' votes among affirming probes that name each object."""
    from rescap.chair import objects_in

    best: dict[str, float] = {}
    for p in r["propositions"]:
        probes = [x for x in (p.get("evidence") or {}).get("probes") or [] if x["polarity"] == "affirms"]
        if not probes:
            continue
        s = probes[0]["samples"]
        y = sum(x.strip().lower().startswith("có") for x in s) / max(len(s), 1)
        for o in objects_in(p["text_vi"]):
            best[o] = max(best.get(o, 0.0), y)
    return best


def score(args) -> None:
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import GroupKFold
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    from rescap.chair import objects_in

    d = np.load(args.feats)
    meta = [m.split("|", 1) for m in d["meta"]]
    recs = {}
    for f in Path(args.records).glob("*.json"):
        r = json.loads(f.read_text(encoding="utf-8"))
        recs[r["image_id"]] = r
    gold = {i: set().union(*[set(objects_in(c)) for c in recs[i]["reference_captions"]]) for i, _ in meta}
    vy = {i: vintern_yes(recs[i]) for i in {i for i, _ in meta}}
    y = np.array([o in gold[i] for i, o in meta], dtype=int)
    groups = np.array([i for i, _ in meta])
    print(f"{len(y)} queries over {len(set(groups))} images, positive rate {y.mean():.3f}")

    def cv(X):
        s = np.zeros(len(y))
        for tr, te in GroupKFold(5).split(X, y, groups):
            m = make_pipeline(StandardScaler(), LogisticRegression(C=args.C, max_iter=3000))
            s[te] = m.fit(X[tr], y[tr]).predict_proba(X[te])[:, 1]
        return s

    def prior_feature():
        # class prior fitted out of fold, so it cannot see the held-out image's label
        s = np.zeros(len(y))
        objs = np.array([o for _, o in meta])
        for tr, te in GroupKFold(5).split(objs, y, groups):
            pos, cnt = {}, {}
            for o, t in zip(objs[tr], y[tr]):
                pos[o] = pos.get(o, 0) + t; cnt[o] = cnt.get(o, 0) + 1
            s[te] = [(pos.get(o, 0) + 1) / (cnt.get(o, 0) + 3) for o in objs[te]]
        return s

    auc = lambda s: roc_auc_score(y, s)
    v = np.array([vy[i].get(o, 0.5) for i, o in meta])
    prior = prior_feature()
    print(f"  Vintern K=5 yes-share        AUROC {auc(v):.3f}")
    print(f"  class prior (out of fold)    AUROC {auc(prior):.3f}")
    print(f"  Qwen P(có) with image        AUROC {auc(d['py_img']):.3f}   without image {auc(d['py_txt']):.3f}")
    best = None
    for k, L in enumerate(d["layers"]):
        si = cv(d["h_img"][:, k].astype(np.float32))
        st = cv(d["h_txt"][:, k].astype(np.float32))
        print(f"  probe layer {L:2d}: with image AUROC {auc(si):.3f}   without image {auc(st):.3f}")
        if best is None or auc(si) > auc(best[1]):
            best = (L, si)
    L, si = best
    both = cv(np.column_stack([si, v, prior]))
    base = cv(np.column_stack([v, prior]))
    print(f"  Vintern + prior              AUROC {auc(base):.3f}")
    print(f"  probe(L{L}) + Vintern + prior AUROC {auc(both):.3f}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("extract")
    e.add_argument("--records", required=True)
    e.add_argument("--images", required=True)
    e.add_argument("--out", required=True)
    e.add_argument("--limit", type=int, default=500)
    s = sub.add_parser("score")
    s.add_argument("--records", required=True)
    s.add_argument("--feats", required=True)
    s.add_argument("--C", type=float, default=0.05)
    args = ap.parse_args()
    extract(args) if args.cmd == "extract" else score(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
