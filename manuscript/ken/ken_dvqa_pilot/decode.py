#!/usr/bin/env python3
"""Deterministic Zero-Shot Decoder for DrivingVQA Pilot P1, P2, P3 (CC-104 F1, F2, F4, F6, F8, F10, R4).

Models (pinned B-N1 snapshots on M4, venv-lb 685ffe2a):
  - qwen25vl_7b : Qwen/Qwen2.5-VL-7B-Instruct @ cc594898137f460bfe9f0759e9844b3ce807cfb5 (28 layers; P2 layers 14..21)
  - internvl3_8b: OpenGVLab/InternVL3-8B-hf   @ 259a3b64a14623c0ec91a045cb43f7c5af5fa6af (32 layers; P2 layers 16..23)

Arms:
  Stage A (always run):
    - P1-Blind   (dev1000, n=1000, text-only, QP-A prompt, max_new_tokens=16)
    - P1-Full    (dev1000, n=1000, full image I_i, QP-A prompt, max_new_tokens=16)
    - P1-Oracle  (dev1000, n=1000, full image I_i + 50%-expanded gold crops without text labels, max_new_tokens=16)
    - P3-SelfCap (dev500,  n=500,  Step 1: full image -> scene caption max_new_tokens=60;
                                   Step 2: text-only caption + QP-A -> answer max_new_tokens=16)
  Stage B (run ONLY if decide_pilot.json reports P1_verdict == "GO"):
    - P2-Grid    (dev1000, n=1000, full image I_i + K=4 uniform 2x2 quadrants resized to 448x448, max_new_tokens=16)
    - P2-AttCrop (dev1000, n=1000, full image I_i + K=4 cross-attention crops [0.25 W_p x 0.25 H_p window, stride 1,
                                   NMS IoU 0.3, expanded 50%, resized to 448x448], eager attention, max_new_tokens=16)

Usage:
  python3 scripts/ken_dvqa_pilot/decode.py --selftest
  python3 scripts/ken_dvqa_pilot/decode.py --stage P1 --model qwen25vl_7b --snapshot /path/to/snap --dvqa-dir /path/to/dvqa --out-dir /path/to/out
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = next(
    (p for p in HERE.parents if (p / "manuscript/ken/drivingvqa_dev500_ids.tsv").exists()),
    HERE.parents[2],
)

PROMPTS_JSON_PATH = HERE / "prompts.json"
PROMPTS_JSON_SHA256 = "c8fb51d993cc123c21c120868ef8eb7b9a760ab9adf8ee6293ba2360ce28e854"
PROMPT_SHAS = {
    "qa_direct_prompt": "6321df1eca893c2f45bf0a7c49648b2134e14c2fb731bae3096e8a0dd69ba1f5",
    "p3_caption_prompt": "8354e25cd84b4b81b9f60f79944b58edc0cde7b7a6200dec7a4a5a9c3e83a5b1",
    "p3_qa_from_caption_prompt": "59dd04fbb0e42537622ab919738469f00c7444b94cdb931b35e453e131a85d51",
}

DEV500_TSV = ROOT / "manuscript/ken/drivingvqa_dev500_ids.tsv"
DEV500_SHA256 = "9896af1186ddd6a5806095ba696851b5aef512079f5d0813cff3f7f4fae9c4ce"
DEV1000_TSV = ROOT / "manuscript/ken/drivingvqa_dev1000_ids.tsv"
DEV1000_SHA256 = "636e04775153ef9cb879a7620d195fcaa7e86894ead73b008c8f95b47e268dec"
TRAIN_JSON_SHA256 = "4a204e3fa7516db313ceeb91ac989919979e31da20e484bc5f4018c261bd483d"

MODELS = {
    "qwen25vl_7b": {
        "hub_id": "Qwen/Qwen2.5-VL-7B-Instruct",
        "revision": "cc594898137f460bfe9f0759e9844b3ce807cfb5",
        "num_layers": 28,
        "p2_att_layers": tuple(range(14, 22)),  # 0-indexed layers 14..21 inclusive (middle-to-late 8 layers)
        "dtype": "bfloat16",
        "stage_a_attn": "sdpa",
        "stage_b_attn": "eager",
    },
    "internvl3_8b": {
        "hub_id": "OpenGVLab/InternVL3-8B-hf",
        "revision": "259a3b64a14623c0ec91a045cb43f7c5af5fa6af",
        "num_layers": 32,
        "p2_att_layers": tuple(range(16, 24)),  # 0-indexed layers 16..23 inclusive (middle-to-late 8 layers)
        "dtype": "bfloat16",
        "stage_a_attn": "sdpa",
        "stage_b_attn": "eager",
    },
}

# P2 frozen hyperparameters (CC-104 F6)
TILE_SIZE = 448
WINDOW_RATIO = 0.25
WINDOW_STRIDE = 1
NMS_IOU_THRESHOLD = 0.30
TOP_K_CROPS = 4


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_pinned_prompts(path: Path = PROMPTS_JSON_PATH) -> dict:
    if not path.is_file():
        raise SystemExit(f"REFUSED: missing prompts.json at {path}")
    if sha256_file(path) != PROMPTS_JSON_SHA256:
        raise SystemExit(f"REFUSED: prompts.json SHA-256 mismatch at {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    for key, exp_sha in sorted(PROMPT_SHAS.items()):
        tpl = data[key]["template"]
        got_sha = sha256_text(tpl)
        if got_sha != exp_sha or data[key]["template_sha256"] != exp_sha:
            raise SystemExit(f"REFUSED: template SHA-256 mismatch for {key}: {got_sha} != {exp_sha}")
    return data


def load_manifest_ids(tsv_path: Path, expected_sha: str, expected_n: int) -> list[str]:
    if not tsv_path.is_file():
        raise SystemExit(f"REFUSED: missing manifest {tsv_path}")
    if sha256_file(tsv_path) != expected_sha:
        raise SystemExit(f"REFUSED: manifest SHA-256 mismatch for {tsv_path}")
    lines = tsv_path.read_text(encoding="utf-8").splitlines()[1:]
    ids = [line.split("\t")[0].strip() for line in lines if line.strip()]
    if len(ids) != expected_n or len(set(ids)) != expected_n:
        raise SystemExit(f"REFUSED: manifest {tsv_path} does not have {expected_n} unique IDs")
    return ids


def format_question_and_options(item: dict) -> tuple[str, str]:
    q = item["questions"]
    if isinstance(q, list):
        q_str = " | ".join(str(sub).strip() for sub in q)
    else:
        q_str = str(q).strip()
    opts = item["possible_answers"]
    opt_str = "{" + ", ".join(f"{k}: {str(opts[k]).strip()}" for k in sorted(opts.keys())) + "}"
    return q_str, opt_str


def build_qa_prompt(item: dict, prompts_cfg: dict) -> str:
    q_str, opt_str = format_question_and_options(item)
    tpl = prompts_cfg["qa_direct_prompt"]["template"]
    return tpl.format(question=q_str, options=opt_str)


def build_p3_step2_prompt(item: dict, caption: str, prompts_cfg: dict) -> str:
    q_str, opt_str = format_question_and_options(item)
    tpl = prompts_cfg["p3_qa_from_caption_prompt"]["template"]
    return tpl.format(caption=caption.strip(), question=q_str, options=opt_str)


def expand_bbox_50pct(bbox_xywh: list[float] | tuple[float, ...], img_size_wh: list[int] | tuple[int, int]) -> list[float]:
    """Corbiere et al. (2025) Sec. 4.2 & PILOT_NOTE Sec. 3: expand (x, y, w, h) by 50% around center and clip to [0, W]x[0, H]."""
    x, y, w, h = (float(v) for v in bbox_xywh)
    W, H = float(img_size_wh[0]), float(img_size_wh[1])
    x1 = max(0.0, x - 0.25 * w)
    y1 = max(0.0, y - 0.25 * h)
    x2 = min(W, x + 1.25 * w)
    y2 = min(H, y + 1.25 * h)
    if x2 <= x1:
        x2 = min(W, x1 + 1.0)
    if y2 <= y1:
        y2 = min(H, y1 + 1.0)
    return [round(x1, 4), round(y1, 4), round(x2, 4), round(y2, 4)]


def extract_gold_boxes_xywh(item: dict) -> list[list[float]]:
    """Extract gold bounding boxes [x, y, w, h] from `relevant_entities` WITHOUT entity labels (no text leakage)."""
    boxes: list[list[float]] = []
    for ent in item.get("relevant_entities", []):
        if isinstance(ent, dict):
            for _label, bbox in sorted(ent.items()):
                if isinstance(bbox, (list, tuple)) and len(bbox) == 4:
                    boxes.append([float(v) for v in bbox])
    return boxes


def crop_xyxy_pil(img, box_xyxy: list[float], resize_to: tuple[int, int] | None = None):
    from PIL import Image

    W, H = img.size
    x1 = max(0, min(W - 1, int(round(box_xyxy[0]))))
    y1 = max(0, min(H - 1, int(round(box_xyxy[1]))))
    x2 = max(x1 + 1, min(W, int(round(box_xyxy[2]))))
    y2 = max(y1 + 1, min(H, int(round(box_xyxy[3]))))
    crop = img.crop((x1, y1, x2, y2))
    if resize_to is not None:
        crop = crop.resize(resize_to, resample=Image.Resampling.BICUBIC)
    return crop


def make_anyres4_quadrant_boxes(img_size_wh: tuple[int, int]) -> list[list[float]]:
    """Uniform 2x2 AnyRes-4 quadrant boxes [x1, y1, x2, y2] in deterministic order (TL, TR, BL, BR)."""
    W, H = float(img_size_wh[0]), float(img_size_wh[1])
    mx, my = W / 2.0, H / 2.0
    return [
        [0.0, 0.0, mx, my],
        [mx, 0.0, W, my],
        [0.0, my, mx, H],
        [mx, my, W, H],
    ]


def box_iou_xyxy(box_a: list[float], box_b: list[float]) -> float:
    ix1 = max(box_a[0], box_b[0])
    iy1 = max(box_a[1], box_b[1])
    ix2 = min(box_a[2], box_b[2])
    iy2 = min(box_a[3], box_b[3])
    iw = max(0.0, ix2 - ix1)
    ih = max(0.0, iy2 - iy1)
    inter = iw * ih
    if inter <= 0.0:
        return 0.0
    area_a = max(0.0, box_a[2] - box_a[0]) * max(0.0, box_a[3] - box_a[1])
    area_b = max(0.0, box_b[2] - box_b[0]) * max(0.0, box_b[3] - box_b[1])
    denom = area_a + area_b - inter
    return float(inter / denom) if denom > 0.0 else 0.0


def select_top_k_attention_crops(
    att_map_2d: np.ndarray,
    img_size_wh: tuple[int, int],
    window_ratio: float = WINDOW_RATIO,
    stride: int = WINDOW_STRIDE,
    nms_iou: float = NMS_IOU_THRESHOLD,
    top_k: int = TOP_K_CROPS,
) -> list[list[float]]:
    """CC-104 F6 frozen P2-AttCrop window selector:
    1. Sliding window of size (ceil(0.25 * W_p), ceil(0.25 * H_p)), stride 1 patch over `att_map_2d` (H_p, W_p).
    2. Score each window by sum of attention weights; tie-break deterministically by (-score, r, c).
    3. Greedy NMS with IoU threshold 0.3 in unexpanded image coordinates to pick K=4 windows.
    4. Expand each selected window by 50% around its center and clip to [0, W] x [0, H].
    Returns K=4 boxes in [x1, y1, x2, y2] image coordinates.
    """
    if att_map_2d.ndim != 2:
        raise ValueError(f"Expected 2D attention map (H_p, W_p), got shape {att_map_2d.shape}")
    Hp, Wp = int(att_map_2d.shape[0]), int(att_map_2d.shape[1])
    W, H = float(img_size_wh[0]), float(img_size_wh[1])
    win_h = max(1, int(math.ceil(window_ratio * Hp)))
    win_w = max(1, int(math.ceil(window_ratio * Wp)))

    candidates: list[tuple[float, int, int, list[float], list[float]]] = []
    for r in range(0, max(1, Hp - win_h + 1), max(1, stride)):
        for c in range(0, max(1, Wp - win_w + 1), max(1, stride)):
            score = float(np.sum(att_map_2d[r : r + win_h, c : c + win_w]))
            x = c * (W / float(Wp))
            y = r * (H / float(Hp))
            w = win_w * (W / float(Wp))
            h = win_h * (H / float(Hp))
            raw_xyxy = [x, y, x + w, y + h]
            raw_xywh = [x, y, w, h]
            candidates.append((score, r, c, raw_xyxy, raw_xywh))

    # Sort deterministically: highest score first, then row r ascending, then col c ascending
    candidates.sort(key=lambda item: (-round(item[0], 10), item[1], item[2]))

    selected_xywh: list[list[float]] = []
    selected_xyxy: list[list[float]] = []
    deferred_xywh: list[list[float]] = []

    for _score, _r, _c, raw_xyxy, raw_xywh in candidates:
        if len(selected_xywh) >= top_k:
            break
        if all(box_iou_xyxy(raw_xyxy, kept) < nms_iou for kept in selected_xyxy):
            selected_xyxy.append(raw_xyxy)
            selected_xywh.append(raw_xywh)
        else:
            deferred_xywh.append(raw_xywh)

    for raw_xywh in deferred_xywh:
        if len(selected_xywh) >= top_k:
            break
        selected_xywh.append(raw_xywh)

    while len(selected_xywh) < top_k:
        selected_xywh.append([0.0, 0.0, W, H])

    return [expand_bbox_50pct(xywh, img_size_wh) for xywh in selected_xywh[:top_k]]


def build_chat_message(images: list, text: str) -> list[dict]:
    """Build standard HF multimodal chat message; when `images` is empty, passes text only (image-blind / Step 2)."""
    content = [{"type": "image", "image": im} for im in images]
    content.append({"type": "text", "text": text})
    return [{"role": "user", "content": content}]


def extract_cross_attention_grid_from_tensors(
    layer_attentions: list,
    layer_indices: tuple[int, ...],
    vis_token_indices: list[int],
    query_token_indices: list[int],
    grid_hw: tuple[int, int],
) -> np.ndarray:
    """Compute head-averaged and layer-averaged cross-attention from `query_token_indices` to `vis_token_indices`
    across `layer_indices`, reshaped to `grid_hw = (H_p, W_p)`.
    Each element of `layer_attentions` has shape (1, num_heads, seq_len, seq_len) as numpy array or torch.Tensor.
    """
    Hp, Wp = int(grid_hw[0]), int(grid_hw[1])
    n_vis = Hp * Wp
    if len(vis_token_indices) < n_vis or not query_token_indices:
        return np.ones((Hp, Wp), dtype=np.float64) / float(max(1, n_vis))

    vis_idx = np.asarray(vis_token_indices[:n_vis], dtype=np.int64)
    q_idx = np.asarray(query_token_indices, dtype=np.int64)
    accum = np.zeros(n_vis, dtype=np.float64)

    for l_idx in layer_indices:
        att = layer_attentions[l_idx]
        if hasattr(att, "detach"):
            att_np = att[0].detach().float().cpu().numpy()
        else:
            att_np = np.asarray(att[0], dtype=np.float64)
        # att_np shape: (num_heads, seq_len, seq_len) -> slice query rows and visual columns
        sub = att_np[:, q_idx, :][:, :, vis_idx]
        accum += np.mean(sub, axis=(0, 1))

    accum /= float(len(layer_indices))
    return accum.reshape((Hp, Wp))


def load_hf_model(model_key: str, snapshot: Path, attn_impl: str, device: str = "cuda:0"):
    import torch
    import transformers

    if model_key not in MODELS:
        raise SystemExit(f"REFUSED: unknown model {model_key}")
    m = MODELS[model_key]
    dtype = getattr(torch, m["dtype"])
    proc = transformers.AutoProcessor.from_pretrained(snapshot, trust_remote_code=False)
    if hasattr(proc, "tokenizer") and proc.tokenizer is not None:
        proc.tokenizer.padding_side = "left"
    net = transformers.AutoModelForImageTextToText.from_pretrained(
        snapshot,
        trust_remote_code=False,
        attn_implementation=attn_impl,
        torch_dtype=dtype,
        device_map={"": device} if device != "cpu" else None,
    ).eval()
    return proc, net


def generate_single(proc, net, images: list, prompt_text: str, max_new_tokens: int) -> tuple[str, int, bool]:
    import torch

    msg = [build_chat_message(images, prompt_text)]
    enc = proc.apply_chat_template(
        msg,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
        padding=True,
    )
    enc = {k: (v.to(net.device, net.dtype) if hasattr(v, "dtype") and v.dtype.is_floating_point else v.to(net.device))
           for k, v in enc.items() if hasattr(v, "to")}
    eos = net.generation_config.eos_token_id
    eos_set = set(eos if isinstance(eos, list) else [eos])
    with torch.no_grad():
        out_ids = net.generate(**enc, max_new_tokens=max_new_tokens, do_sample=False, num_beams=1)
    row = out_ids[0, enc["input_ids"].shape[1] :].tolist()
    stop_pos = next((k + 1 for k, tok in enumerate(row) if tok in eos_set), None)
    n_tok = stop_pos or len(row)
    hit_max = stop_pos is None and len(row) >= max_new_tokens
    text = proc.decode(row[:n_tok], skip_special_tokens=True).strip()
    return text, int(n_tok), bool(hit_max)


def compute_model_attention_crops(proc, net, model_key: str, full_img, prompt_text: str) -> list[list[float]]:
    """Run one forward pass with `output_attentions=True` (eager attention) to extract the 2D patch relevance map
    and select K=4 50%-expanded boxes per CC-104 F6."""
    import torch

    m = MODELS[model_key]
    msg = [build_chat_message([full_img], prompt_text)]
    enc = proc.apply_chat_template(
        msg,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    )
    enc_dev = {
        k: (v.to(net.device, net.dtype) if hasattr(v, "dtype") and v.dtype.is_floating_point else v.to(net.device))
        for k, v in enc.items() if hasattr(v, "to")
    }
    with torch.no_grad():
        out = net(**enc_dev, output_attentions=True, use_cache=False)

    input_ids = enc["input_ids"][0].tolist()
    # Identify visual token positions vs trailing text query token positions
    if "image_grid_thw" in enc:
        thw = enc["image_grid_thw"][0].tolist()
        merge = getattr(getattr(proc, "image_processor", None), "merge_size", 2)
        Hp = max(1, int(thw[1]) // int(merge))
        Wp = max(1, int(thw[2]) // int(merge))
    else:
        Hp, Wp = 16, 16

    n_vis = Hp * Wp
    # Heuristic-free lookup of image token ID from processor/config when present
    img_token_id = getattr( net.config, "image_token_id", None) or getattr(net.config, "image_token_index", None)
    if img_token_id is not None and img_token_id in input_ids:
        vis_indices = [idx for idx, tid in enumerate(input_ids) if tid == img_token_id]
        if len(vis_indices) >= n_vis:
            vis_indices = vis_indices[:n_vis]
        else:
            Hp = max(1, int(math.isqrt(len(vis_indices))))
            Wp = max(1, len(vis_indices) // Hp)
            vis_indices = vis_indices[: Hp * Wp]
        last_vis = vis_indices[-1]
        query_indices = [idx for idx in range(last_vis + 1, len(input_ids))]
    else:
        vis_indices = list(range(1, min(len(input_ids) - 1, n_vis + 1)))
        Hp = max(1, int(math.isqrt(len(vis_indices))))
        Wp = max(1, len(vis_indices) // Hp)
        vis_indices = vis_indices[: Hp * Wp]
        query_indices = list(range(vis_indices[-1] + 1, len(input_ids)))

    att_2d = extract_cross_attention_grid_from_tensors(
        layer_attentions=out.attentions,
        layer_indices=m["p2_att_layers"],
        vis_token_indices=vis_indices,
        query_token_indices=query_indices,
        grid_hw=(Hp, Wp),
    )
    return select_top_k_attention_crops(att_2d, full_img.size)


def load_existing_jsonl(path: Path) -> dict[str, dict]:
    if not path.is_file():
        return {}
    done: dict[str, dict] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
            done[str(rec["sample_id"])] = rec
        except json.JSONDecodeError:
            continue
    return done


def run_stage_decode(
    stage: str,
    model_key: str,
    snapshot: Path,
    dvqa_dir: Path,
    out_dir: Path,
    device: str = "cuda:0",
) -> None:
    from PIL import Image

    prompts_cfg = load_pinned_prompts()
    train_json_path = dvqa_dir / "train.json"
    if not train_json_path.is_file() or sha256_file(train_json_path) != TRAIN_JSON_SHA256:
        raise SystemExit(f"REFUSED: invalid or missing train.json at {train_json_path}")
    train_data = json.loads(train_json_path.read_text(encoding="utf-8"))

    dev500_ids = load_manifest_ids(DEV500_TSV, DEV500_SHA256, 500)
    dev1000_ids = load_manifest_ids(DEV1000_TSV, DEV1000_SHA256, 1000)

    out_dir.mkdir(parents=True, exist_ok=True)
    m = MODELS[model_key]
    attn_impl = m["stage_b_attn"] if stage == "P2" else m["stage_a_attn"]
    proc, net = load_hf_model(model_key, snapshot, attn_impl=attn_impl, device=device)

    if stage == "P1":
        for arm in ("P1-Blind", "P1-Full", "P1-Oracle"):
            out_file = out_dir / f"{arm}_{model_key}.preds.jsonl"
            done = load_existing_jsonl(out_file)
            with out_file.open("a", encoding="utf-8") as fh:
                for sid in dev1000_ids:
                    if sid in done:
                        continue
                    item = train_data[sid]
                    q_prompt = build_qa_prompt(item, prompts_cfg)
                    img_path = dvqa_dir / item["img_filename"]
                    if arm == "P1-Blind":
                        imgs = []
                    elif arm == "P1-Full":
                        imgs = [Image.open(img_path).convert("RGB")]
                    else:
                        full_im = Image.open(img_path).convert("RGB")
                        gold_boxes = extract_gold_boxes_xywh(item)
                        crops = [
                            crop_xyxy_pil(full_im, expand_bbox_50pct(b, item["img_size"]), resize_to=(TILE_SIZE, TILE_SIZE))
                            for b in gold_boxes
                        ]
                        imgs = [full_im] + crops
                    raw_out, n_tok, hit_max = generate_single(
                        proc, net, imgs, q_prompt, max_new_tokens=prompts_cfg["qa_direct_prompt"]["max_new_tokens"]
                    )
                    rec = {
                        "sample_id": sid,
                        "img_filename": item["img_filename"],
                        "arm": arm,
                        "model": model_key,
                        "revision": m["revision"],
                        "raw_output": raw_out,
                        "n_tokens": n_tok,
                        "hit_max": hit_max,
                    }
                    fh.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")
                    fh.flush()
                    os.fsync(fh.fileno())

    elif stage == "P3":
        cap_file = out_dir / f"P3-SelfCap_{model_key}.captions.jsonl"
        pred_file = out_dir / f"P3-SelfCap_{model_key}.preds.jsonl"
        done_caps = load_existing_jsonl(cap_file)
        cap_prompt = prompts_cfg["p3_caption_prompt"]["template"]
        cap_max_tok = prompts_cfg["p3_caption_prompt"]["max_new_tokens"]

        with cap_file.open("a", encoding="utf-8") as fh_cap:
            for sid in dev500_ids:
                if sid in done_caps:
                    continue
                item = train_data[sid]
                img_path = dvqa_dir / item["img_filename"]
                full_im = Image.open(img_path).convert("RGB")
                cap_text, n_tok, hit_max = generate_single(proc, net, [full_im], cap_prompt, max_new_tokens=cap_max_tok)
                rec_cap = {
                    "sample_id": sid,
                    "img_filename": item["img_filename"],
                    "arm": "P3-SelfCap-Step1",
                    "model": model_key,
                    "revision": m["revision"],
                    "caption": cap_text,
                    "n_tokens": n_tok,
                    "hit_max": hit_max,
                }
                fh_cap.write(json.dumps(rec_cap, ensure_ascii=False, sort_keys=True) + "\n")
                fh_cap.flush()
                os.fsync(fh_cap.fileno())
                done_caps[sid] = rec_cap

        done_preds = load_existing_jsonl(pred_file)
        with pred_file.open("a", encoding="utf-8") as fh_pred:
            for sid in dev500_ids:
                if sid in done_preds:
                    continue
                item = train_data[sid]
                cap_text = done_caps[sid]["caption"]
                qa_prompt = build_p3_step2_prompt(item, cap_text, prompts_cfg)
                # Step 2 is strictly text-only (no image passed)
                raw_out, n_tok, hit_max = generate_single(
                    proc, net, [], qa_prompt, max_new_tokens=prompts_cfg["p3_qa_from_caption_prompt"]["max_new_tokens"]
                )
                rec_pred = {
                    "sample_id": sid,
                    "img_filename": item["img_filename"],
                    "arm": "P3-SelfCap",
                    "model": model_key,
                    "revision": m["revision"],
                    "caption": cap_text,
                    "raw_output": raw_out,
                    "n_tokens": n_tok,
                    "hit_max": hit_max,
                }
                fh_pred.write(json.dumps(rec_pred, ensure_ascii=False, sort_keys=True) + "\n")
                fh_pred.flush()
                os.fsync(fh_pred.fileno())

    elif stage == "P2":
        for arm in ("P2-Grid", "P2-AttCrop"):
            out_file = out_dir / f"{arm}_{model_key}.preds.jsonl"
            done = load_existing_jsonl(out_file)
            with out_file.open("a", encoding="utf-8") as fh:
                for sid in dev1000_ids:
                    if sid in done:
                        continue
                    item = train_data[sid]
                    q_prompt = build_qa_prompt(item, prompts_cfg)
                    img_path = dvqa_dir / item["img_filename"]
                    full_im = Image.open(img_path).convert("RGB")
                    if arm == "P2-Grid":
                        boxes_xyxy = make_anyres4_quadrant_boxes(full_im.size)
                    else:
                        boxes_xyxy = compute_model_attention_crops(proc, net, model_key, full_im, q_prompt)
                    tiles = [crop_xyxy_pil(full_im, b, resize_to=(TILE_SIZE, TILE_SIZE)) for b in boxes_xyxy]
                    raw_out, n_tok, hit_max = generate_single(
                        proc,
                        net,
                        [full_im] + tiles,
                        q_prompt,
                        max_new_tokens=prompts_cfg["qa_direct_prompt"]["max_new_tokens"],
                    )
                    rec = {
                        "sample_id": sid,
                        "img_filename": item["img_filename"],
                        "arm": arm,
                        "model": model_key,
                        "revision": m["revision"],
                        "crop_boxes_xyxy": boxes_xyxy,
                        "tile_size": [TILE_SIZE, TILE_SIZE],
                        "raw_output": raw_out,
                        "n_tokens": n_tok,
                        "hit_max": hit_max,
                    }
                    fh.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")
                    fh.flush()
                    os.fsync(fh.fileno())
    else:
        raise SystemExit(f"REFUSED: unknown stage {stage}")


def selftest() -> None:
    from PIL import Image

    # 1. Verify pinned prompts.json and template SHA-256s
    prompts_cfg = load_pinned_prompts()
    assert prompts_cfg["qa_direct_prompt"]["max_new_tokens"] == 16
    assert prompts_cfg["p3_caption_prompt"]["max_new_tokens"] == 60
    assert prompts_cfg["p3_qa_from_caption_prompt"]["max_new_tokens"] == 16

    # 2. Verify manifest pins
    dev500_ids = load_manifest_ids(DEV500_TSV, DEV500_SHA256, 500)
    dev1000_ids = load_manifest_ids(DEV1000_TSV, DEV1000_SHA256, 1000)
    assert dev1000_ids[:500] == dev500_ids

    # 3. Verify 50% bbox expansion and image boundary clipping
    assert expand_bbox_50pct([100.0, 200.0, 40.0, 60.0], [1500, 863]) == [90.0, 185.0, 150.0, 275.0]
    assert expand_bbox_50pct([2.0, 3.0, 20.0, 40.0], [100, 100]) == [0.0, 0.0, 27.0, 53.0]
    assert expand_bbox_50pct([90.0, 85.0, 20.0, 30.0], [100, 100]) == [85.0, 77.5, 100.0, 100.0]

    # 4. Verify gold box extraction without text labels
    sample_item = {
        "questions": ["I monitor the pedestrian:", "I prepare to stop:"],
        "possible_answers": {"B": "right", "A": "left", "D": "No", "C": "Yes"},
        "relevant_entities": [
            {"pedestrian": [284.17, 274.3, 31.37, 84.98]},
            {"stop sign": [400.0, 100.0, 50.0, 50.0]},
        ],
        "img_size": [1500, 863],
    }
    q_prompt = build_qa_prompt(sample_item, prompts_cfg)
    assert "Options: {A: left, B: right, C: Yes, D: No}" in q_prompt
    assert "stop sign" not in q_prompt and "284.17" not in q_prompt
    gold_boxes = extract_gold_boxes_xywh(sample_item)
    assert len(gold_boxes) == 2 and gold_boxes[0] == [284.17, 274.3, 31.37, 84.98]

    # 5. Verify P1-Blind and P3-Step2 build text-only messages (0 images)
    msg_blind = build_chat_message([], q_prompt)
    assert len(msg_blind[0]["content"]) == 1 and msg_blind[0]["content"][0]["type"] == "text"

    # 6. Verify P2-Grid AnyRes-4 quadrants and P2-AttCrop sliding window + NMS + 448x448 resize
    synth_img = Image.new("RGB", (1500, 863), color=(128, 128, 128))
    quad_boxes = make_anyres4_quadrant_boxes(synth_img.size)
    assert len(quad_boxes) == 4
    grid_tiles = [crop_xyxy_pil(synth_img, b, resize_to=(TILE_SIZE, TILE_SIZE)) for b in quad_boxes]
    assert all(t.size == (448, 448) for t in grid_tiles)

    # Synthetic 16x16 attention grid with two distinct peaks
    rng = np.random.default_rng(0)
    fake_layers = [rng.uniform(0.0, 0.01, size=(1, 4, 270, 270)).astype(np.float32) for _ in range(32)]
    for l_idx in range(14, 24):
        # Boost patch token 10 (top-left region) and patch token 200 (bottom-right region)
        fake_layers[l_idx][:, :, 260:, 10] += 0.50
        fake_layers[l_idx][:, :, 260:, 200] += 0.40

    att_grid = extract_cross_attention_grid_from_tensors(
        layer_attentions=fake_layers,
        layer_indices=MODELS["qwen25vl_7b"]["p2_att_layers"],
        vis_token_indices=list(range(1, 257)),
        query_token_indices=list(range(257, 270)),
        grid_hw=(16, 16),
    )
    att_crops_xyxy = select_top_k_attention_crops(att_grid, synth_img.size)
    assert len(att_crops_xyxy) == 4
    att_tiles = [crop_xyxy_pil(synth_img, b, resize_to=(TILE_SIZE, TILE_SIZE)) for b in att_crops_xyxy]
    assert all(t.size == (448, 448) for t in att_tiles)

    print(json.dumps({
        "script": "decode.py",
        "selftest": "OK",
        "p2_att_crops_sample_xyxy": att_crops_xyxy,
        "prompts_sha256": PROMPTS_JSON_SHA256,
        "qwen_p2_layers": list(MODELS["qwen25vl_7b"]["p2_att_layers"]),
        "internvl3_p2_layers": list(MODELS["internvl3_8b"]["p2_att_layers"]),
    }, sort_keys=True))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--stage", choices=["P1", "P2", "P3"], default="P1")
    ap.add_argument("--model", choices=sorted(MODELS.keys()), default="qwen25vl_7b")
    ap.add_argument("--snapshot", type=Path, default=None)
    ap.add_argument("--dvqa-dir", type=Path, default=Path("/root/dvqa_pilot"))
    ap.add_argument("--out-dir", type=Path, default=Path(".session_backup/2026-10-26/dvqa_pilot/runs"))
    ap.add_argument("--device", type=str, default="cuda:0")
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return

    if args.snapshot is None:
        raise SystemExit("REFUSED: --snapshot is required for GPU decoding")
    run_stage_decode(
        stage=args.stage,
        model_key=args.model,
        snapshot=args.snapshot,
        dvqa_dir=args.dvqa_dir,
        out_dir=args.out_dir,
        device=args.device,
    )


if __name__ == "__main__":
    main()
