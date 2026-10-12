#!/usr/bin/env python
"""Multilingual CLIPScore / RefCLIPScore + BERTScore on KTVIC test preds.

    python scripts/clip_score.py ~/ncs-data/results/*.preds.json [--limit 2]

CLIP: open_clip `xlm-roberta-large-ViT-H-14` / `frozen_laion5b_s13b_b90k`
(MLAION, Gomes et al. NAACL'25 Findings) — the same model for vi and en.
Hessel et al. 2021: CLIP-S = w·max(cos(c, v), 0), w = 2.5;
RefCLIP-S = harmonic mean of CLIP-S and max(max_r cos(c, r), 0). No
"A photo depicts" prefix (it is English). Text past 77 tokens is truncated,
so for detailed captions we also score each sentence (min and mean).
BERTScore: xlm-roberta-large (layer 17 default), multi-ref = best ref, raw (no
vi baseline rescale), P/R/F reported separately (P falls, R rises with length).

Writes data/results/metrics_v2/<stem>.clip.json and <stem>.bert.json;
`python scripts/metrics_v2.py table` merges them.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from metrics_v2 import full_split, write  # noqa: E402
from score_ci import load_preds  # noqa: E402

MODEL, PRETRAINED, W = "xlm-roberta-large-ViT-H-14", "frozen_laion5b_s13b_b90k", 2.5


def clip_s(cos):
    """CLIP-S = w·max(cos, 0)."""
    return W * max(cos, 0.0)


def ref_clip_s(cos_img, cos_refs):
    """Harmonic mean of CLIP-S and max(max_r cos, 0); 0 if either is 0."""
    a, b = clip_s(cos_img), max(max(cos_refs), 0.0)
    return 2 * a * b / (a + b) if a + b > 0 else 0.0


def sentences(text: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.!?;])\s+", text.strip()) if s.strip(" .")] or [text]


def _check() -> None:
    assert clip_s(0.4) == 1.0 and clip_s(-0.3) == 0.0
    assert abs(ref_clip_s(0.4, [0.2, 0.6, -1]) - 2 * 1.0 * 0.6 / 1.6) < 1e-12
    assert ref_clip_s(-0.1, [0.5]) == 0.0
    assert sentences("Một con chó. Nó chạy!  ") == ["Một con chó.", "Nó chạy!"]


class Clip:
    def __init__(self, device):
        import open_clip
        import torch

        self.torch, self.device = torch, device
        # fp32 on every device: under precision="fp16" open_clip's HF text tower (XLM-R) keeps some fp32
        # layers and the first attention matmul fails on mixed dtypes. ~5 GB of VRAM, the job runs alone.
        self.model, _, self.prep = open_clip.create_model_and_transforms(
            MODEL, pretrained=PRETRAINED, device=device, precision="fp32")
        self.model.eval()
        self.tok = open_clip.get_tokenizer(MODEL)

    def _norm(self, x):
        return (x / x.norm(dim=-1, keepdim=True)).float().cpu()

    def text(self, texts, bs=64):
        with self.torch.no_grad():
            return self.torch.cat([self._norm(self.model.encode_text(self.tok(texts[i:i + bs]).to(self.device)))
                                   for i in range(0, len(texts), bs)])

    def images(self, paths, bs=32):
        from PIL import Image

        out = []
        with self.torch.no_grad():
            for i in range(0, len(paths), bs):
                x = self.torch.stack([self.prep(Image.open(p).convert("RGB")) for p in paths[i:i + bs]])
                out.append(self._norm(self.model.encode_image(x.to(self.device))))
        return self.torch.cat(out)


def main() -> int:
    _check()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("preds", nargs="+")
    ap.add_argument("--split", default="test_data.json")
    ap.add_argument("--limit", type=int, default=0, help="smoke test: first N images, prints only, writes nothing")
    ap.add_argument("--skip-bert", action="store_true")
    args = ap.parse_args()

    from evaluate import KTVIC, file_names, references

    refs, names = references(args.split), file_names(args.split)
    ids = sorted(refs)[: args.limit or None]
    import torch

    device = "cuda" if torch.cuda.is_available() else "cpu"  # CPU = smoke test only
    clip = Clip(device)
    img = dict(zip(ids, clip.images([KTVIC / "images" / names[i] for i in ids])))
    flat = [(i, r) for i in ids for r in refs[i]]
    ref_emb = clip.text([r for _, r in flat])
    ref_by_id: dict[str, list] = {}
    for (i, _), e in zip(flat, ref_emb):
        ref_by_id.setdefault(i, []).append(e)

    if not args.skip_bert:
        from bert_score import BERTScorer

        bert = BERTScorer(model_type="xlm-roberta-large", device=device)

    for path in args.preds:
        preds = load_preds(path)
        if not args.limit and full_split(refs, preds, path) is None:
            continue
        caps = [preds[i][0] for i in ids]
        cap_emb = clip.text(caps)
        sents = [sentences(c) for c in caps]
        sent_emb = iter(clip.text([s for ss in sents for s in ss]))
        per = {"CLIP-S": {}, "RefCLIP-S": {}, "CLIP-S_sent_min": {}, "CLIP-S_sent_mean": {}}
        for i, e, ss in zip(ids, cap_emb, sents):
            cos_img = float(e @ img[i])
            per["CLIP-S"][i] = clip_s(cos_img)
            per["RefCLIP-S"][i] = ref_clip_s(cos_img, [float(e @ r) for r in ref_by_id[i]])
            sc = [clip_s(float(next(sent_emb) @ img[i])) for _ in ss]
            per["CLIP-S_sent_min"][i], per["CLIP-S_sent_mean"][i] = min(sc), sum(sc) / len(sc)
        stem = Path(path).name.removesuffix(".preds.json")
        if args.limit:
            print(stem, {m: [round(v, 3) for v in d.values()] for m, d in per.items()})
        else:
            write(stem, "clip", per, {"model": f"{MODEL}/{PRETRAINED}", "w": W})
        if args.skip_bert:
            continue
        p, r, f = bert.score(caps, [refs[i] for i in ids])
        bper = {f"BERT-{k}": dict(zip(ids, map(float, v))) for k, v in (("P", p), ("R", r), ("F", f))}
        if args.limit:
            print(stem, {m: [round(v, 3) for v in d.values()] for m, d in bper.items()})
        else:
            write(stem, "bert", bper, {"model": "xlm-roberta-large", "rescale": False})
    return 0


if __name__ == "__main__":
    sys.exit(main())
