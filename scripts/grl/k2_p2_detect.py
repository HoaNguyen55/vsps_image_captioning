#!/usr/bin/env python3
"""K2 P2 detector pass (K2_GATE0_RULE.md §6c): Grounding DINO-T presence sets D(img) over
COCO-80 on UIT-ViIC val 924 (CC-136P W1, W8-W10, W12, W15). A dev pilot input; the decision is k2_p2.py's.

    python3 scripts/grl/k2_p2_detect.py --selftest                 CPU, synthetic logits (numpy only, no torch)
    python3 scripts/grl/k2_p2_detect.py fetch                      M3 CPU: the pinned weights and BERT files, sha-asserted
    /root/venv-gd/bin/python scripts/grl/k2_p2_detect.py smoke --out SMOKE.json   M3 GPU: 2 UT-2402 train images (W12)
    /root/venv-gd/bin/python scripts/grl/k2_p2_detect.py run --out P2_DETECT.json   M3 GPU (timeout 1800 s in k2_p2.sh)

Rule (W1): demo/inference_on_a_image.py at 856dde2, l.117-133, given-phrase mode: the span-normalised positive map
(create_positive_map_from_span) times the sigmoid token logits gives a class x query score; class c is in D(img) iff
some query scores > 0.30 (the argparse default, l.162). util/inference.predict()'s max-token rule (0.35 in
predict_with_caption) is not used. D at 0.35 is written beside it, descriptive only.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE)]
import common as K  # noqa: E402

#: COCO-2014 instance categories in category-id order (the category_dict order of demo/test_ap_on_coco.py)
COCO80 = (
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light",
    "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant",
    "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
    "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle",
    "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
    "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table", "toilet",
    "tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
    "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush")
PROMPT = " . ".join(COCO80) + " ."  # = test_ap_on_coco.py l.174 = build_captions_and_token_span(COCO80, True)[0]
BOX_T, BOX_T_DESC, MAX_TEXT_LEN = 0.30, 0.35, 256

# ------------------------------------------------------------------------------------------------ pins (CC-136P W8)
GD_COMMIT = "856dde20aee659246248e20734ef9ba5214f5e44"
GD_SRC = Path("/root/GroundingDINO")  # outside common.SCAN_ROOTS: the repo's own .asset images would fail the scan
GD_CFG = "groundingdino/config/GroundingDINO_SwinT_OGC.py"
TORCH, CUDA, TRANSFORMERS = "2.5.1+cu121", "12.1", "4.44.2"  # W8; torchvision 0.20.1+cu121 beside torch
#: W9: checkpoint keys the model does not have; named, anything else is a fault (the smoke run confirms the set)
UNEXPECTED_OK = frozenset({"label_enc.weight", "bert.embeddings.position_ids"})
MODELS = K.NCS_DATA / "models"
WEIGHTS = MODELS / "groundingdino-swint-ogc" / "groundingdino_swint_ogc.pth"
BERT = MODELS / "bert-base-uncased-86b5e09"
HF_GD = "https://huggingface.co/ShilongLiu/GroundingDINO/resolve/a94c9b567a2a374598f05c584e96798a170c56fb/"
HF_BERT = "https://huggingface.co/google-bert/bert-base-uncased/resolve/86b5e0934494bd15c9632b12f734a8a67f723594/"
FILES = {  # local path -> (url, sha256); fetched once, sha-asserted on every use
    WEIGHTS: (HF_GD + "groundingdino_swint_ogc.pth", "3b3ca2563c77c69f651d7bd133e97139c186df06231157a64c507099c52bc799"),
    BERT / "model.safetensors": (HF_BERT + "model.safetensors",
                                 "68d45e234eb4a928074dfd868cead0219ab85354cc53d20e772753c6bb9169d3"),
    BERT / "config.json": (HF_BERT + "config.json", "7160e1553ad2ca51d8c1cb066be533db31826e12d173824c1bb0cb1a4f187d20"),
    BERT / "tokenizer.json": (HF_BERT + "tokenizer.json",
                              "ce64fce797c24f68df90b40a3f74f579b336a493db14bd583fd520ea0d8c9a98"),
    BERT / "tokenizer_config.json": (HF_BERT + "tokenizer_config.json",
                                     "a025160ef0431f1a392f6f050c1310f4c5d9fb6f275932dbccba73c4d214bf10"),
    BERT / "vocab.txt": (HF_BERT + "vocab.txt", "07eced375cec144d27c900241f3e339478dec958f92fddbc551f295c992038a3"),
}


def files_ok(files: dict = FILES, bert: Path = BERT) -> None:
    """W8: every pinned file matches its sha256, and the BERT dir holds no other weight file (so the load is the
    pinned safetensors and nothing else)."""
    for p, (_, want) in files.items():
        if not p.is_file() or K.sha_file(p) != want:
            raise SystemExit(f"FAULT: {p} is missing or differs from its pin")
    extra = sorted({f.name for f in bert.iterdir()} - {p.name for p in files if p.parent == bert})
    if extra:
        raise SystemExit(f"FAULT: unpinned files in {bert}: {extra}")


def fetch(files: dict = FILES, bert: Path = BERT, get=K.fetch) -> None:
    """Download each absent pinned file, assert its sha256 in memory, then write it by tmp + os.replace."""
    import hashlib

    for p, (url, want) in files.items():
        if p.is_file():
            continue
        data = get(url)
        if hashlib.sha256(data).hexdigest() != want:
            raise SystemExit(f"FAULT: {url} does not match its pinned sha256")
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(p.suffix + ".part")
        tmp.write_bytes(data)
        os.replace(tmp, p)
    files_ok(files, bert)


# ------------------------------------------------------------------------------------------------ the rule
def class_scores(prob: np.ndarray, posmap: np.ndarray) -> np.ndarray:
    """Given-phrase mode (inference_on_a_image.py l.124): positive_maps @ logits.T, then the max over queries.
    prob: (n_queries, 256) sigmoid token logits; posmap: (80, 256) span-normalised rows. Returns (80,)."""
    return (posmap.astype(np.float64) @ prob.astype(np.float64).T).max(1)


def present(scores: np.ndarray, thr: float) -> list[str]:
    """l.132: filt_mask = logit_phr > box_threshold; a class is present if any query passes."""
    return [c for c, s in zip(COCO80, scores) if s > thr]


def prompt_ok(names, prompt: str, n_tokens: int, posmap: np.ndarray) -> None:
    """W9: no '/' in a name (build_captions_and_token_span calls random.choice on one), the prompt is the
    deterministic join, it tokenises to <= 256 tokens, and every one of the 80 spans landed in the map (a span whose
    char_to_token is None is silently dropped upstream)."""
    if any("/" in n for n in names) or len(set(names)) != 80 or prompt != " . ".join(names) + " .":
        raise SystemExit("FAULT: the 80 names or the prompt are not the registered ones")
    if n_tokens > MAX_TEXT_LEN:
        raise SystemExit(f"FAULT: the prompt is {n_tokens} tokens > {MAX_TEXT_LEN}")
    if posmap.shape != (80, MAX_TEXT_LEN) or not (posmap.sum(1) > 0.5).all():
        raise SystemExit("FAULT: a class span is outside the 256-token map")


# ------------------------------------------------------------------------------------------------ GPU pass
def gd_commit_ok(src: Path = GD_SRC) -> None:
    head = subprocess.run(["git", "-C", str(src), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    clean = subprocess.run(["git", "-C", str(src), "diff", "--quiet", "HEAD", "--"]).returncode == 0
    if head != GD_COMMIT or not clean:
        raise SystemExit(f"FAULT: {src} is not a clean checkout of {GD_COMMIT[:8]}")


def keys_ok(missing: list[str], unexpected: list[str]) -> None:
    """W9: the checkpoint fills every model key, and the only extra keys are the pinned, named ones."""
    if missing or set(unexpected) - UNEXPECTED_OK:
        raise SystemExit(f"FAULT: load_state_dict missing {sorted(missing)[:5]}, unexpected "
                         f"{sorted(set(unexpected) - UNEXPECTED_OK)[:5]} (W9)")


def freeze_ok(v: str | None) -> str:
    """W8: k2_p2.sh passes the venv-gd freeze it asserted against the OPS-recorded value; None is a fault."""
    if not v or len(v) != 64 or set(v) - set("0123456789abcdef"):
        raise SystemExit("FAULT: GD_FREEZE_SHA256 is not set to a sha256 (W8)")
    return v


def load_detector():
    """The pinned model on the GPU with every W8/W9 assert. Returns (model, caption, posmap, meta, calls)."""
    import torch
    import transformers

    if torch.__version__ != TORCH or torch.version.cuda != CUDA or transformers.__version__ != TRANSFORMERS \
            or not torch.cuda.is_available():
        raise SystemExit(f"FAULT: torch {torch.__version__} / CUDA {torch.version.cuda} / transformers "
                         f"{transformers.__version__}, not {TORCH} / {CUDA} / {TRANSFORMERS} on a GPU (W8)")
    freeze = freeze_ok(os.environ.get("GD_FREEZE_SHA256"))
    gd_commit_ok()
    files_ok()
    from groundingdino import _C  # noqa: F401  W9: fail hard; upstream swallows this ImportError
    import groundingdino.models.GroundingDINO.ms_deform_attn as msda
    from groundingdino.models import build_model
    from groundingdino.util.slconfig import SLConfig
    from groundingdino.util.utils import clean_state_dict
    from groundingdino.util.vl_utils import build_captions_and_token_span, create_positive_map_from_span

    calls = [0]
    cuda_apply = msda.MultiScaleDeformableAttnFunction.apply

    def counted(*a):
        calls[0] += 1
        return cuda_apply(*a)

    msda.MultiScaleDeformableAttnFunction.apply = counted  # W9: l.330 falls back to pytorch silently if not CUDA
    t0 = time.time()
    args = SLConfig.fromfile(str(GD_SRC / GD_CFG))
    args.device, args.text_encoder_type = "cuda", str(BERT)  # W8: local pinned snapshot, no Hub name at run time
    model = build_model(args)
    res = model.load_state_dict(clean_state_dict(torch.load(str(WEIGHTS), map_location="cpu")["model"]), strict=False)
    keys_ok(res.missing_keys, res.unexpected_keys)
    model = model.eval().to("cuda")
    if model.training or any(p.dtype != torch.float32 for p in model.parameters()):
        raise SystemExit("FAULT: the model is not in eval mode with fp32 weights (W9)")
    caption, spans = build_captions_and_token_span(list(COCO80), True)
    tok = model.tokenizer(caption)
    posmap = create_positive_map_from_span(tok, [spans[c] for c in COCO80]).numpy()
    prompt_ok(COCO80, caption, len(tok["input_ids"]), posmap)
    meta = {"pins": {"gd_commit": GD_COMMIT, "torch": torch.__version__, "cuda": torch.version.cuda,
                     "transformers": transformers.__version__, "files": {str(p): w for p, (_, w) in FILES.items()},
                     "venv_gd_freeze_sha256": freeze},
            "load_state_dict_unexpected": sorted(res.unexpected_keys), "prompt": caption,
            "prompt_tokens": len(tok["input_ids"]), "load_s": round(time.time() - t0, 2),
            "gpu": torch.cuda.get_device_name(0)}
    return model, caption, posmap, meta, calls


def images(kind: str) -> list[tuple[int, Path, str]]:
    """(id, staged path, pinned sha256): val-924 from uitviic_val.tsv, or the smoke's first 2 UT-2402 train ids from
    the staging list (never a val image)."""
    if kind == "val":
        rows = [r.split("\t") for r in K.pinned("manuscript/prereg/2026-10-21_dev_pools/uitviic_val.tsv")
                .read_text().splitlines()]
        val = {int(r[0]): (r[1], r[2]) for r in rows}
        return [(i, K.UV / "images" / val[i][0], val[i][1]) for i in K.ids("val924")]
    sha = {f: h for h, f in (x.split("  ") for x in (K.UV / "images.sha256").read_text().splitlines())}
    return [(i, K.UV / "images" / f"{i:012d}.jpg", sha[f"{i:012d}.jpg"]) for i in K.ids("ut2402")[:2]]


def run(out: Path, kind: str) -> None:
    """kind 'val': the P2 pass, D(img) for val-924. kind 'smoke' (W12): 2 UT-2402 train images, the asserts and the
    run figures only; no D is kept (not a look)."""
    if out.exists():
        raise SystemExit(f"REFUSED: {out} exists")
    import torch
    from groundingdino.util.inference import load_image

    todo = images(kind)
    for _, p, want in todo:
        if K.sha_file(p) != want:
            raise SystemExit(f"FAULT: staged image {p.name} differs from its pinned sha256")
    model, caption, posmap, meta, calls = load_detector()
    d30, d35, smax, t_img = {}, {}, {}, []
    torch.cuda.reset_peak_memory_stats()
    for i, p, _ in todo:
        t1 = time.time()
        _, image = load_image(str(p))  # = inference_on_a_image.py l.58-70: RandomResize([800], 1333), ToTensor, Normalize
        with torch.no_grad():
            o = model(image[None].to("cuda"), captions=[caption])  # batch 1
        s = class_scores(o["pred_logits"].sigmoid()[0].float().cpu().numpy(), posmap)
        t_img.append(time.time() - t1)
        if calls[0] == 0:
            raise SystemExit("FAULT: MultiScaleDeformableAttention CUDA op not used (CPU fallback, W9)")
        d30[str(i)], d35[str(i)], smax[str(i)] = present(s, BOX_T), present(s, BOX_T_DESC), [round(float(x), 4) for x in s]
    rec = {"schema": f"vsps.k2.p2_detect.{kind}.v1", "label": "K2 P2 dev pilot detector pass (§6c); TARGET CEILING ONLY",
           "rule": "inference_on_a_image.py l.117-133 given-phrase mode, box_threshold 0.30 (l.162)",
           "n_images": len(todo), "classes": list(COCO80), **meta, "msda_cuda_calls": calls[0],
           "s_per_image": round(float(np.mean(t_img)), 4),
           "peak_gpu_mem_gib": round(torch.cuda.max_memory_reserved() / 2**30, 3)}
    if kind == "val":
        rec |= {"D_0.30": d30, "D_0.35_descriptive": d35, "class_max_score": smax}
    tmp = out.with_suffix(".part")
    tmp.write_text(json.dumps(rec, indent=1) + "\n")
    os.replace(tmp, out)
    print(json.dumps({k: rec[k] for k in ("n_images", "s_per_image", "prompt_tokens", "msda_cuda_calls")}))


# ------------------------------------------------------------------------------------------------ selftest
def span_map(spans: list[list[int]], width: int = MAX_TEXT_LEN) -> np.ndarray:
    """Synthetic stand-in for create_positive_map_from_span: token index lists -> rows normalised to sum 1."""
    m = np.zeros((len(spans), width))
    for j, toks in enumerate(spans):
        m[j, toks] = 1
    return m / (m.sum(1, keepdims=True) + 1e-6)


def selftest() -> None:
    import tempfile

    assert len(COCO80) == 80 and len(set(COCO80)) == 80 and not any("/" in c for c in COCO80)
    gold = set().union(*map(set, json.loads(K.pinned(
        "manuscript/prereg/2026-10-27_grl_pilot/gold_instances.json").read_text())["gold"].values()))
    assert gold <= set(COCO80), gold - set(COCO80)
    # span-mean rule: class 0 one token (0.31), class 1 two tokens (0.60, 0.20 -> mean 0.40), on different queries
    spans = [[1], [3, 4]] + [[6 + k] for k in range(78)]
    pm = span_map(spans)
    prob = np.zeros((900, MAX_TEXT_LEN))
    prob[7, 1], prob[2, 3], prob[2, 4] = 0.31, 0.60, 0.20
    s = class_scores(prob, pm)
    assert abs(s[0] - 0.31) < 1e-4 and abs(s[1] - 0.40) < 1e-4 and s[2:].max() == 0, s[:3]
    assert present(s, BOX_T) == ["person", "bicycle"] and present(s, BOX_T_DESC) == ["bicycle"]
    prob[2, 4] = 0.0  # mean 0.30: a max-token rule (0.60 > 0.35) would keep it; the span rule drops it (miss bias, W1)
    assert present(class_scores(prob, pm), BOX_T) == ["person"]
    prob[7, 1] = 0.30  # strictly greater than the threshold
    assert present(class_scores(prob, pm), BOX_T) == []
    # W15 mutation: predict()'s max-token rule (max over all tokens, here over the span) on the same tensor would keep
    # the two-token class at 0.60; the registered span mean (0.30) must not, so the mutant is caught
    max_token = lambda pr, m: np.array([pr[:, m[c] > 0].max() for c in range(len(m))])  # noqa: E731
    assert present(max_token(prob, pm), BOX_T) == ["bicycle"] != present(class_scores(prob, pm), BOX_T)
    keys_ok([], ["label_enc.weight"])
    for bad in ((["transformer.x"], []), ([], ["head.extra"])):
        try:
            keys_ok(*bad)
        except SystemExit as e:
            assert "FAULT" in str(e), e
        else:
            raise AssertionError(f"keys_ok accepted {bad}")
    assert freeze_ok("a" * 64) == "a" * 64
    for bad in (None, "", "a" * 63, "G" * 64):
        try:
            freeze_ok(bad)
        except SystemExit as e:
            assert "GD_FREEZE_SHA256" in str(e), e
        else:
            raise AssertionError(f"freeze_ok accepted {bad!r}")
    prompt_ok(COCO80, PROMPT, 195, pm)
    for bad in ((COCO80[:79] + ("a/b",), " . ".join(COCO80[:79] + ("a/b",)) + " .", 195, pm),
                (COCO80, PROMPT, 257, pm), (COCO80, PROMPT, 195, np.vstack([pm[:79], np.zeros((1, 256))]))):
        try:
            prompt_ok(*bad)
        except SystemExit as e:
            assert "FAULT" in str(e), e
        else:
            raise AssertionError("prompt_ok accepted a bad prompt")
    with tempfile.TemporaryDirectory() as t:
        b = Path(t) / "bert"
        blob = {b / "model.safetensors": b"w", b / "vocab.txt": b"v"}
        import hashlib

        files = {p: ("http://x/" + p.name, hashlib.sha256(d).hexdigest()) for p, d in blob.items()}
        fetch(files, b, get=lambda url: blob[b / url.rsplit("/", 1)[1]])
        files_ok(files, b)
        (b / "pytorch_model.bin").write_bytes(b"other")
        for f in (lambda: files_ok(files, b), lambda: fetch({b / "x": ("http://x/x", "0" * 64)}, b, get=lambda u: b"y")):
            try:
                f()
            except SystemExit as e:
                assert "FAULT" in str(e), e
            else:
                raise AssertionError("an unpinned or mismatched file was accepted")
    print("k2_p2_detect selftest ok")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", nargs="?", choices=("fetch", "run", "smoke"))
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.selftest:
        selftest()
    elif a.cmd == "fetch":
        fetch()
    elif a.cmd in ("run", "smoke"):
        run(Path(a.out), "val" if a.cmd == "run" else "smoke")
    else:
        ap.error("give --selftest, fetch or run")
    return 0


if __name__ == "__main__":
    sys.exit(main())
