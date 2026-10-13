#!/usr/bin/env python
"""S0 zero-shot object-truth screen for Qwen3-VL-8B-Instruct (judge D10 (iii)).

Pre-registration: manuscript/prereg/2026-10-13_s0_qwen3vl.md.

Subcommands:
  subsets    Build data/coco_probe/manifest_s0_detailed1000.json (1,000 images, seed 0) and
             data/coco_probe/probe_val2017_ids.txt (295 probe cocoids in COCO val2017).
  preflight  CPU-only check of the separate venv (transformers >= 4.57), model class, config
             architectures, shard sizes, SHA256SUMS, processor + chat template on 3 probe
             images (vision tokens in [256, 1024]), meta-device state_dict key match against
             model.safetensors.index.json, images, comparators, POPE files and annotations.
  verdict    Score COCO short (2,500) and detailed (1,000) against Qwen2.5-VL-7B zero-shot
             with paired bootstrap (B = 5000), val2017 and clean-Vietnamese qualifiers,
             POPE-vi / RePOPE-vi descriptive deltas, and the pre-registered PASS/KILL + G4 branch.

    python scripts/s0_screen.py --self-check
    python scripts/s0_screen.py subsets
    python scripts/s0_screen.py preflight --weights $NCS_DATA/models/Qwen3-VL-8B-Instruct-0c351dd \\
        --images-dir $NCS_DATA/datasets/coco_probe/val2014
    python scripts/s0_screen.py verdict --cand-coco-dir $NCS_DATA/results/s0_qwen3vl \\
        --cand-pope $NCS_DATA/results/s0_qwen3vl/pope_vi/qwen3vl8b_zs-vi.jsonl \\
        --out $NCS_DATA/results/s0_qwen3vl/s0_verdict.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import struct
import sys
import unicodedata
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import score_coco_probe as sc  # noqa: E402
from abs_halluc import CJK  # noqa: E402
from coco_probe import BACKBONES, read_jsonl  # noqa: E402
from evaluate import PROMPTS  # noqa: E402
from object_prf import coco_gold, image_counts, paired, scores  # noqa: E402
from pope_vi import SPLITS, load as load_pope, metrics as pope_metrics, obj_of, parse as parse_pope  # noqa: E402
from rescap.vlm.mock import looks_vietnamese  # noqa: E402

MANIFEST_2500 = sc.PROBE_DATA / "manifest.json"
MANIFEST_1000 = sc.PROBE_DATA / "manifest_s0_detailed1000.json"
VAL2017_IDS = sc.PROBE_DATA / "probe_val2017_ids.txt"
VAL2017_NAMES_BACKUP = ROOT / ".session_backup/2026-10-13/research_r9/C8_backbone/s0/val2017_names.txt"
VAL2017_ZIP_URL = "http://images.cocodataset.org/zips/val2017.zip"

MODEL_KEY = "qwen3-vl-8b"
HUB_ID = "Qwen/Qwen3-VL-8B-Instruct"
REVISION = "0c351dd01ed87e9c1b53cbc748cba10e6187ff3b"
SHARDS: dict[str, tuple[int, str]] = {
    "model-00001-of-00004.safetensors": (
        4902275944, "d5d0aef0eb170fc7453a296c43c0849a56f510555d3588e4fd662bb35490aefa"),
    "model-00002-of-00004.safetensors": (
        4915962496, "8be88fb5501e4d5719a6d4cc212e6a13480330e74f3e8c77daa1a68f199106b5"),
    "model-00003-of-00004.safetensors": (
        4999831048, "83de00eafe6e0d57ccd009dbcf71c9974d74df2f016c27afb7e95aafd16b2192"),
    "model-00004-of-00004.safetensors": (
        2716270024, "0a88b98e9f96270973f567e6a2c103ede6ccdf915ca3075e21c755604d0377a5"),
}
RATIO_BAND = (0.85, 1.15)
F1_BAR = {"short": 1.5, "detailed": 2.0}
BOOT_N = 5000
EXACT = lambda c: {c}  # noqa: E731

#: Syllable-final oa/oe/uy old->new tone placement for the descriptive v2+tone report (judge D10 (iv)(a)).
_TONE_MAP = {
    "òa": "oà", "óa": "oá", "ỏa": "oả", "õa": "oã", "ọa": "oạ",
    "òe": "oè", "óe": "oé", "ỏe": "oẻ", "õe": "oẽ", "ọe": "oẹ",
    "ùy": "uỳ", "úy": "uý", "ủy": "uỷ", "ũy": "uỹ", "ụy": "uỵ",
}
_TONE_RE = re.compile("(" + "|".join(_TONE_MAP) + rf")(?![{sc._LETTER}])")


def norm_tone(text: str) -> str:
    """NFC + syllable-final oa/oe/uy normalised to new-style placement (tòa -> toà, hỏa -> hoả, thủy -> thuỷ)."""
    return _TONE_RE.sub(lambda m: _TONE_MAP[m.group(0)], unicodedata.normalize("NFC", text))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fetch_val2017_ids() -> set[int]:
    """Read the 5,000 val2017 image ids from val2017.zip's central directory via HTTP range (~0.5 MB)."""
    def get(rng: tuple[int, int]):
        req = urllib.request.Request(
            VAL2017_ZIP_URL, headers={"User-Agent": "r9-c8", "Range": f"bytes={rng[0]}-{rng[1]}"})
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.read(), r.headers

    _, hdr = get((0, 0))
    size = int(hdr["Content-Range"].split("/")[1])
    tail, _ = get((size - 65536, size - 1))
    i = tail.rfind(b"PK\x05\x06")
    assert i >= 0, "no end-of-central-directory record in val2017.zip"
    n_entries, cd_size, cd_off = struct.unpack("<HII", tail[i + 10: i + 20])
    cd, _ = get((cd_off, cd_off + cd_size - 1))
    ids: set[int] = set()
    p = 0
    while p < len(cd):
        assert cd[p: p + 4] == b"PK\x01\x02", p
        nlen, elen, clen = struct.unpack("<HHH", cd[p + 28: p + 34])
        name = cd[p + 46: p + 46 + nlen].decode()
        if name.endswith(".jpg"):
            ids.add(int(Path(name).stem))
        p += 46 + nlen + elen + clen
    assert len(ids) == 5000, len(ids)
    return ids


def build_subsets(val2017_names: Path | None = None) -> dict:
    """Build manifest_s0_detailed1000.json and probe_val2017_ids.txt deterministically."""
    man = json.loads(MANIFEST_2500.read_text(encoding="utf-8"))
    imgs = sorted(man["images"], key=lambda x: x["cocoid"])
    assert len(imgs) == 2500, len(imgs)
    det_imgs = sorted(random.Random(0).sample(imgs, 1000), key=lambda x: x["cocoid"])
    det_man = {
        "source": man["source"],
        "pool": len(imgs),
        "n": 1000,
        "seed": 0,
        "sampler": "random.Random(0).sample(sorted(manifest['images'], key=lambda x: x['cocoid']), 1000), sorted by cocoid",
        "image_url_pattern": man["image_url_pattern"],
        "note": "S0 zero-shot detailed screen subset (1,000 of the 2,500 COCO probe images, judge D10 (iii)).",
        "images": det_imgs,
    }
    MANIFEST_1000.write_text(json.dumps(det_man, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    src = val2017_names or VAL2017_NAMES_BACKUP
    if src and src.exists():
        v17_all = {int(Path(line.strip()).stem) for line in src.read_text(encoding="utf-8").splitlines() if line.strip()}
        assert len(v17_all) == 5000, len(v17_all)
        probe_v17 = sorted({x["cocoid"] for x in imgs} & v17_all)
    elif VAL2017_IDS.exists():
        probe_v17 = sorted(int(x) for x in VAL2017_IDS.read_text(encoding="utf-8").split())
    else:
        v17_all = _fetch_val2017_ids()
        probe_v17 = sorted({x["cocoid"] for x in imgs} & v17_all)

    det_v17 = sorted({x["cocoid"] for x in det_imgs} & set(probe_v17))
    assert len(probe_v17) == 295 and len(det_v17) == 121, (len(probe_v17), len(det_v17))
    VAL2017_IDS.write_text("\n".join(str(i) for i in probe_v17) + "\n", encoding="utf-8")
    return {
        "manifest_s0_detailed1000": {"path": str(MANIFEST_1000), "n": len(det_imgs), "sha256": sha256(MANIFEST_1000)},
        "probe_val2017_ids": {
            "path": str(VAL2017_IDS), "n_short": len(probe_v17), "n_detailed1000": len(det_v17),
            "sha256": sha256(VAL2017_IDS),
        },
    }


def _ver_tuple(v: str) -> tuple[int, int]:
    parts = re.findall(r"\d+", v)
    return (int(parts[0]), int(parts[1])) if len(parts) >= 2 else (0, 0)


def run_preflight(args) -> dict:
    """CPU-only preflight check before the S0 GPU job runs."""
    import torch
    import transformers
    from PIL import Image
    from transformers import AutoConfig, AutoProcessor

    ver = transformers.__version__
    if _ver_tuple(ver) < (4, 57):
        raise SystemExit(f"transformers >= 4.57 required for {MODEL_KEY}, got {ver}")
    hub_id, cls_name, px = BACKBONES[args.model]
    if not hasattr(transformers, cls_name):
        raise SystemExit(f"transformers {ver} has no class {cls_name}")
    cls = getattr(transformers, cls_name)

    weights = Path(args.weights)
    cfg_path = weights / "config.json"
    if not cfg_path.exists():
        raise SystemExit(f"missing {cfg_path}")
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    if cfg.get("architectures") != [cls_name]:
        raise SystemExit(f"config.json architectures {cfg.get('architectures')} != [{cls_name!r}]")

    for shard, (want_size, _) in SHARDS.items():
        p = weights / shard
        if not p.exists() or p.stat().st_size != want_size:
            got = p.stat().st_size if p.exists() else None
            raise SystemExit(f"shard {shard}: size {got} != {want_size}")

    sums_path = weights / "SHA256SUMS"
    if not sums_path.exists():
        raise SystemExit(f"missing {sums_path}")
    sums: dict[str, str] = {}
    for line in sums_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            digest, fname = line.strip().split(None, 1)
            fname = fname.lstrip("*")
            if not (weights / fname).exists():
                raise SystemExit(f"SHA256SUMS lists missing file {fname}")
            sums[fname] = digest
    for shard, (_, want_sha) in SHARDS.items():
        if sums.get(shard) != want_sha:
            raise SystemExit(f"SHA256SUMS {shard}: {sums.get(shard)} != {want_sha}")

    idx_path = weights / "model.safetensors.index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    idx_keys = set(idx["weight_map"].keys())
    idx_shards = set(idx["weight_map"].values())
    if idx_shards != set(SHARDS.keys()):
        raise SystemExit(f"index shards {sorted(idx_shards)} != {sorted(SHARDS)}")
    with torch.device("meta"):
        meta_cfg = AutoConfig.from_pretrained(str(weights))
        meta_model = cls(meta_cfg)
    meta_keys = set(meta_model.state_dict().keys())
    if meta_keys != idx_keys:
        raise SystemExit(
            f"meta state_dict mismatch: only_in_meta={sorted(meta_keys - idx_keys)[:5]}, "
            f"only_in_index={sorted(idx_keys - meta_keys)[:5]}")

    man2500 = json.loads(MANIFEST_2500.read_text(encoding="utf-8"))["images"]
    man1000 = json.loads(MANIFEST_1000.read_text(encoding="utf-8"))["images"]
    v17_ids = [int(x) for x in VAL2017_IDS.read_text(encoding="utf-8").split()]
    ids2500 = {x["cocoid"] for x in man2500}
    ids1000 = {x["cocoid"] for x in man1000}
    assert len(ids2500) == 2500 and len(ids1000) == 1000 and ids1000 <= ids2500
    assert len(v17_ids) == 295 and set(v17_ids) <= ids2500 and len(set(v17_ids) & ids1000) == 121

    images_dir = Path(args.images_dir)
    missing_probe = [x["filename"] for x in man2500 if not (images_dir / x["filename"]).exists()]
    if missing_probe:
        raise SystemExit(f"{len(missing_probe)} probe images missing in {images_dir}, e.g. {missing_probe[:3]}")

    pope_dir = Path(args.pope_dir)
    pope_qs = [q for s in SPLITS for q in load_pope(pope_dir, "pope", s)]
    for s in SPLITS:
        load_pope(pope_dir, "repope", s)
    pope_asked = {(q["image"], obj_of(q["text"])) for q in pope_qs}
    assert len(pope_asked) == 5127, len(pope_asked)
    missing_pope_imgs = sorted({q["image"] for q in pope_qs if not (images_dir / q["image"]).exists()})
    if missing_pope_imgs:
        raise SystemExit(f"{len(missing_pope_imgs)} POPE images missing in {images_dir}, e.g. {missing_pope_imgs[:3]}")

    base_coco = Path(args.base_coco_dir)
    for mode, want_ids in (("short", ids2500), ("detailed", ids1000)):
        f = base_coco / f"zeroshot-{mode}.shard0of1.jsonl"
        got = {r["cocoid"] for r in read_jsonl(f)}
        if not want_ids <= got:
            raise SystemExit(f"baseline {f} lacks {len(want_ids - got)} cocoids for {mode}")

    base_pope = Path(args.base_pope)
    got_pope = {(r["image"], r["object"]) for r in read_jsonl(base_pope)}
    if len(got_pope) != 5127:
        raise SystemExit(f"baseline {base_pope} has {len(got_pope)} != 5127 answers")

    for ann_file in (sc.ANN / "instances_val2014.json", sc.KARPATHY):
        if not ann_file.exists():
            raise SystemExit(f"missing annotation file {ann_file}")

    processor = AutoProcessor.from_pretrained(str(weights), min_pixels=256 * px, max_pixels=1024 * px)
    img_tok_id = cfg["image_token_id"]
    vis_tokens = []
    for item in sorted(man2500, key=lambda x: x["cocoid"])[:3]:
        im = Image.open(images_dir / item["filename"]).convert("RGB")
        messages = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": PROMPTS["short"]}]}]
        text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = processor(text=[text], images=[im], return_tensors="pt")
        n_vis = int((inputs["input_ids"] == img_tok_id).sum().item())
        if not (256 <= n_vis <= 1024):
            raise SystemExit(f"{item['filename']}: vision tokens {n_vis} outside [256, 1024]")
        vis_tokens.append({"cocoid": item["cocoid"], "vision_tokens": n_vis, "seq_len": int(inputs["input_ids"].shape[1])})

    return {
        "status": "ok",
        "transformers_version": ver,
        "torch_version": torch.__version__,
        "cuda_touched": False,
        "model_class": cls_name,
        "weights": str(weights),
        "sha256sums_sha256": sha256(sums_path),
        "meta_state_dict_keys": len(meta_keys),
        "probe_images_checked": vis_tokens,
    }


def _load_coco_captions(preds_dir: Path, system: str, mode: str, want: list[int]) -> dict[int, str]:
    rows: dict[int, str] = {}
    for f in sorted(preds_dir.glob(f"{system}-{mode}.shard*.jsonl")):
        for r in read_jsonl(f):
            rows[int(r["cocoid"])] = r["caption"]
    missing = [i for i in want if i not in rows]
    if missing:
        raise SystemExit(f"{preds_dir}/{system}-{mode}: missing {len(missing)} of {len(want)} images (e.g. {missing[:5]})")
    return {i: rows[i] for i in want}


def decide_mode(mode: str, mpc_base: float, mpc_cand: float, d_inst: dict, d_union: dict, d_salient: dict) -> dict:
    """Apply the pre-registered S0 mode pass rule to precomputed paired bootstrap deltas."""
    ratio = mpc_cand / mpc_base if mpc_base else float("inf")
    in_band = RATIO_BAND[0] <= ratio <= RATIO_BAND[1]
    bar = F1_BAR[mode]
    f1_pt, f1_lo, f1_hi, _ = d_inst["F1"]
    dp_u_pt, dp_u_lo, dp_u_hi, _ = d_union["P"]
    dr_s_pt, dr_s_lo, dr_s_hi, _ = d_salient["R"]
    if in_band:
        f1_ok = bool(f1_pt >= bar and f1_lo > 0.0)
        absent_not_higher = bool(dp_u_hi >= 0.0)  # absent_share = 100 - P_union => d(absent) = -dP_union
        passed = bool(f1_ok and absent_not_higher)
        branch = "in_band"
    else:
        f1_ok = False
        absent_not_higher = bool(dp_u_hi >= 0.0)
        passed = bool(dp_u_lo > 0.0 and dr_s_lo > 0.0)
        branch = "style_confounded"
    return {
        "pass": passed,
        "branch": branch,
        "style_confounded": not in_band,
        "mentions_per_caption_base": mpc_base,
        "mentions_per_caption_cand": mpc_cand,
        "mentions_ratio": ratio,
        "ratio_band": list(RATIO_BAND),
        "f1_bar": bar,
        "in_band_f1_ok": f1_ok,
        "in_band_absent_not_significantly_higher": absent_not_higher,
        "style_confounded_dp_union_ci_lo_gt_0": bool(dp_u_lo > 0.0),
        "style_confounded_dr_salient_ci_lo_gt_0": bool(dr_s_lo > 0.0),
        "d_absent_share_point": -dp_u_pt,
        "d_absent_share_ci": [-dp_u_hi, -dp_u_lo],
    }


def qualifier_flag(full_df1_pt: float, sub_df1: tuple[float, float, float, float]) -> dict:
    """True when the subset dF1 95% CI includes 0 AND its point estimate is < half the full-set point estimate."""
    pt, lo, hi, p = sub_df1
    ci_includes_0 = bool(lo <= 0.0 <= hi)
    below_half = bool(pt < 0.5 * full_df1_pt)
    return {
        "dF1": [float(pt), float(lo), float(hi), float(p)],
        "ci_includes_0": ci_includes_0,
        "point_below_half_full": below_half,
        "flagged": bool(ci_includes_0 and below_half),
    }


def _fmt_paired(d: dict) -> dict:
    return {k: [float(x) for x in v] for k, v in d.items()}


def _score_subset(ids: list[int], m_base: dict[int, set[str]], m_cand: dict[int, set[str]],
                  inst: dict[int, set[str]], ref: dict[int, set[str]], mode: str) -> dict:
    g_inst = {i: inst[i] for i in ids}
    g_union = {i: inst[i] | ref[i] for i in ids}
    g_sal = {i: inst[i] & ref[i] for i in ids}

    rows_i_a = [image_counts(m_base[i], g_inst[i], EXACT) for i in ids]
    rows_i_b = [image_counts(m_cand[i], g_inst[i], EXACT) for i in ids]
    rows_u_a = [image_counts(m_base[i], g_union[i], EXACT) for i in ids]
    rows_u_b = [image_counts(m_cand[i], g_union[i], EXACT) for i in ids]
    rows_s_a = [image_counts(m_base[i], g_sal[i], EXACT) for i in ids]
    rows_s_b = [image_counts(m_cand[i], g_sal[i], EXACT) for i in ids]

    si_a, si_b = scores(rows_i_a), scores(rows_i_b)
    su_a, su_b = scores(rows_u_a), scores(rows_u_b)
    ss_a, ss_b = scores(rows_s_a), scores(rows_s_b)

    d_inst = _fmt_paired(paired(rows_i_a, rows_i_b, n=BOOT_N, seed=0))
    d_union = _fmt_paired(paired(rows_u_a, rows_u_b, n=BOOT_N, seed=0))
    d_sal = _fmt_paired(paired(rows_s_a, rows_s_b, n=BOOT_N, seed=0))

    mpc_a = sum(len(m_base[i]) for i in ids) / len(ids)
    mpc_b = sum(len(m_cand[i]) for i in ids) / len(ids)
    dec = decide_mode(mode, mpc_a, mpc_b, d_inst, d_union, d_sal)
    return {
        "n_images": len(ids),
        "base": {
            "mentions_per_caption": mpc_a,
            "instances_only": {k: si_a[k] for k in ("P", "R", "F1")},
            "instances_plus_refs_P": su_a["P"],
            "absent_share_pct": 100.0 - su_a["P"],
            "salient_R": ss_a["R"],
        },
        "cand": {
            "mentions_per_caption": mpc_b,
            "instances_only": {k: si_b[k] for k in ("P", "R", "F1")},
            "instances_plus_refs_P": su_b["P"],
            "absent_share_pct": 100.0 - su_b["P"],
            "salient_R": ss_b["R"],
        },
        "paired_cand_minus_base": {
            "instances_only": d_inst,
            "instances_plus_refs": d_union,
            "salient_instances": d_sal,
        },
        "decision": dec,
    }


def _vi_terms_tone() -> list[tuple[str, str]]:
    from rescap.vi.lexicon import CLASSIFIERS

    def head(term: str) -> str:
        first, _, rest = term.partition(" ")
        return rest if rest and first in CLASSIFIERS else term

    d = json.loads((sc.PROBE_DATA / "coco80_vi.json").read_text(encoding="utf-8"))
    pairs = []
    for cls, terms in d.items():
        if cls.startswith("_"):
            continue
        for t in terms:
            if isinstance(t, str) and not t.startswith("_rui_ro"):
                pairs.append((norm_tone(t.lower()), cls))
    return sorted(pairs, key=lambda x: (-len(head(x[0])), -len(x[0])))


def vi_objects_tone(caption: str, vi_terms_tone) -> set[str]:
    text = norm_tone(caption.lower())
    for pattern, repl in sc.LEX_V2:
        text = re.sub(pattern, repl, text)
    return sc.vi_classes(text, vi_terms_tone)


def _score_pope(pope_dir: Path, base_jsonl: Path, cand_jsonl: Path) -> dict:
    qs = {s: load_pope(pope_dir, "pope", s) for s in SPLITS}
    labels = {
        "POPE": {s: {q["question_id"]: q["label"] for q in qs[s]} for s in SPLITS},
        "RePOPE": {s: {q["question_id"]: q["label"] for q in load_pope(pope_dir, "repope", s)} for s in SPLITS},
    }
    out = {}
    for tag, path in (("base", base_jsonl), ("cand", cand_jsonl)):
        reply = {(r["image"], r["object"]): parse_pope(r["answer"]) for r in read_jsonl(path)}
        if len(reply) != 5127:
            raise SystemExit(f"{path}: expected 5127 answers, got {len(reply)}")
        by_which = {}
        for which, lab in labels.items():
            splits = {}
            for s in SPLITS:
                asked = [((q["image"], obj_of(q["text"])), lab[s][q["question_id"]])
                         for q in qs[s] if q["question_id"] in lab[s]]
                splits[s] = pope_metrics([(reply[k], l) for k, l in asked])
            by_which[which] = {
                "splits": splits,
                "mean_F1": sum(splits[s]["F1"] for s in SPLITS) / len(SPLITS),
                "mean_acc": sum(splits[s]["acc"] for s in SPLITS) / len(SPLITS),
                "mean_P": sum(splits[s]["P"] for s in SPLITS) / len(SPLITS),
                "mean_R": sum(splits[s]["R"] for s in SPLITS) / len(SPLITS),
                "mean_yes": sum(splits[s]["yes"] for s in SPLITS) / len(SPLITS),
                "total_unparsed": sum(splits[s]["unparsed"] for s in SPLITS),
            }
        out[tag] = by_which
    out["delta_cand_minus_base"] = {
        which: {
            "mean_F1": out["cand"][which]["mean_F1"] - out["base"][which]["mean_F1"],
            "mean_P": out["cand"][which]["mean_P"] - out["base"][which]["mean_P"],
            "mean_R": out["cand"][which]["mean_R"] - out["base"][which]["mean_R"],
            "per_split_F1": {
                s: out["cand"][which]["splits"][s]["F1"] - out["base"][which]["splits"][s]["F1"] for s in SPLITS
            },
        }
        for which in ("POPE", "RePOPE")
    }
    return out


def run_verdict(args) -> dict:
    """Compute the pre-registered S0 verdict on COCO short (2,500) + detailed (1,000) and descriptive POPE-vi."""
    vi_terms = sc.load_vi_terms()
    vi_terms_t = _vi_terms_tone()
    inst, ref = coco_gold(MANIFEST_2500)
    v17_set = {int(x) for x in VAL2017_IDS.read_text(encoding="utf-8").split()}
    ids_by_mode = {
        "short": sorted(x["cocoid"] for x in json.loads(MANIFEST_2500.read_text(encoding="utf-8"))["images"]),
        "detailed": sorted(x["cocoid"] for x in json.loads(MANIFEST_1000.read_text(encoding="utf-8"))["images"]),
    }
    assert len(ids_by_mode["short"]) == 2500 and len(ids_by_mode["detailed"]) == 1000

    base_dir = Path(args.base_coco_dir)
    cand_dir = Path(args.cand_coco_dir)
    modes_out = {}
    modes_tone_out = {}

    for mode, ids in ids_by_mode.items():
        cap_a = _load_coco_captions(base_dir, args.base_name, mode, ids)
        cap_b = _load_coco_captions(cand_dir, args.cand_name, mode, ids)

        m_a = {i: sc.vi_objects(cap_a[i], vi_terms, "v2") for i in ids}
        m_b = {i: sc.vi_objects(cap_b[i], vi_terms, "v2") for i in ids}
        main_block = _score_subset(ids, m_a, m_b, inst, ref, mode)

        v17_ids = [i for i in ids if i in v17_set]
        rows_v17_a = [image_counts(m_a[i], inst[i], EXACT) for i in v17_ids]
        rows_v17_b = [image_counts(m_b[i], inst[i], EXACT) for i in v17_ids]
        d_v17 = _fmt_paired(paired(rows_v17_a, rows_v17_b, n=BOOT_N, seed=0))
        contam = qualifier_flag(main_block["paired_cand_minus_base"]["instances_only"]["F1"][0], d_v17["F1"])
        contam["n_images"] = len(v17_ids)
        contam["d_instances_only"] = d_v17

        clean_ids = [
            i for i in ids
            if looks_vietnamese(cap_a[i]) and not CJK.search(cap_a[i])
            and looks_vietnamese(cap_b[i]) and not CJK.search(cap_b[i])
        ]
        if clean_ids:
            rows_cl_a = [image_counts(m_a[i], inst[i], EXACT) for i in clean_ids]
            rows_cl_b = [image_counts(m_b[i], inst[i], EXACT) for i in clean_ids]
            d_cl = _fmt_paired(paired(rows_cl_a, rows_cl_b, n=BOOT_N, seed=0))
            lang_q = qualifier_flag(main_block["paired_cand_minus_base"]["instances_only"]["F1"][0], d_cl["F1"])
            lang_q["d_instances_only"] = d_cl
        else:
            lang_q = {"dF1": [0.0, 0.0, 0.0, 1.0], "ci_includes_0": True, "point_below_half_full": False, "flagged": False}
        lang_q["n_images"] = len(clean_ids)

        lang_stats = {}
        for tag, caps in (("base", cap_a), ("cand", cap_b)):
            n_vi = sum(looks_vietnamese(caps[i]) for i in ids)
            n_cjk = sum(bool(CJK.search(caps[i])) for i in ids)
            lang_stats[tag] = {
                "vietnamese_captions": n_vi,
                "vietnamese_share_pct": 100.0 * n_vi / len(ids),
                "cjk_captions": n_cjk,
                "cjk_rate_pct": 100.0 * n_cjk / len(ids),
            }

        main_block["language"] = lang_stats
        main_block["qualifiers"] = {
            "contamination_driven": contam,
            "language_driven": lang_q,
        }
        modes_out[mode] = main_block

        # Descriptive side-by-side under D10 (iv)(a) tone-mark normalisation (v2+tone)
        mt_a = {i: vi_objects_tone(cap_a[i], vi_terms_t) for i in ids}
        mt_b = {i: vi_objects_tone(cap_b[i], vi_terms_t) for i in ids}
        modes_tone_out[mode] = _score_subset(ids, mt_a, mt_b, inst, ref, mode)

    pope_block = _score_pope(Path(args.pope_dir), Path(args.base_pope), Path(args.cand_pope))
    s0_pass = bool(modes_out["short"]["decision"]["pass"] or modes_out["detailed"]["decision"]["pass"])
    res = {
        "model": {"key": MODEL_KEY, "hub_id": HUB_ID, "revision": REVISION, "cand_name": args.cand_name},
        "matcher_frozen": "v2",
        "modes": modes_out,
        "modes_v2_tone_descriptive": modes_tone_out,
        "pope_vi_descriptive": pope_block,
        "verdict": {
            "short_pass": modes_out["short"]["decision"]["pass"],
            "detailed_pass": modes_out["detailed"]["decision"]["pass"],
            "s0_pass": s0_pass,
            "outcome": "PASS" if s0_pass else "KILL",
            "g4_branch": (
                "PASS: run C8 G1 (1-seed dev-split P1 adapter vs p1dev_s42, ~4.2 GPU-h) in place of 57/58"
                if s0_pass else
                "KILL: keep Qwen2.5-VL-7B; run 57/58 (Qwen2.5-VL-3B) as planned and disclose qwen-research licence"
            ),
        },
        "script_sha256": sha256(Path(__file__)),
    }
    return res


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--self-check", action="store_true")
    sub = ap.add_subparsers(dest="cmd")

    s = sub.add_parser("subsets", help="build manifest_s0_detailed1000.json and probe_val2017_ids.txt")
    s.add_argument("--val2017-names", default=None)

    p = sub.add_parser("preflight", help="CPU-only preflight check before GPU inference")
    p.add_argument("--model", default=MODEL_KEY, choices=sorted(BACKBONES))
    p.add_argument("--weights", default=str(sc.NCS_DATA / "models" / "Qwen3-VL-8B-Instruct-0c351dd"))
    p.add_argument("--images-dir", default=str(sc.NCS_DATA / "datasets" / "coco_probe" / "val2014"))
    p.add_argument("--pope-dir", default=str(sc.NCS_DATA / "datasets" / "pope"))
    p.add_argument("--base-coco-dir", default=str(ROOT / "data" / "results" / "coco5000"))
    p.add_argument("--base-pope", default=str(sc.NCS_DATA / "results" / "pope_vi" / "zeroshot-vi.jsonl"))
    p.add_argument("--out", default=None)

    v = sub.add_parser("verdict", help="compute pre-registered PASS/KILL verdict and qualifiers")
    v.add_argument("--base-coco-dir", default=str(ROOT / "data" / "results" / "coco5000"))
    v.add_argument("--cand-coco-dir", required=True)
    v.add_argument("--base-name", default="zeroshot")
    v.add_argument("--cand-name", default="qwen3vl8b_zs")
    v.add_argument("--pope-dir", default=str(sc.NCS_DATA / "datasets" / "pope"))
    v.add_argument("--base-pope", default=str(sc.NCS_DATA / "results" / "pope_vi" / "zeroshot-vi.jsonl"))
    v.add_argument("--cand-pope", required=True)
    v.add_argument("--out", required=True)
    return ap


def _check() -> None:
    # 1. In-band pass & fail branches
    ok_short = decide_mode(
        "short", 1.20, 1.20,
        {"F1": (1.6, 0.3, 2.9, 0.01)}, {"P": (-0.2, -1.1, 0.4, 0.5)}, {"R": (1.0, -0.2, 2.2, 0.1)},
    )
    assert ok_short["pass"] and ok_short["branch"] == "in_band" and not ok_short["style_confounded"]

    fail_bar = decide_mode(
        "detailed", 2.20, 2.20,
        {"F1": (1.9, 0.5, 3.3, 0.01)}, {"P": (0.1, -0.5, 0.7, 0.5)}, {"R": (1.5, 0.2, 2.8, 0.02)},
    )
    assert not fail_bar["pass"] and not fail_bar["in_band_f1_ok"]

    fail_ci = decide_mode(
        "detailed", 2.20, 2.20,
        {"F1": (2.3, -0.1, 4.7, 0.06)}, {"P": (0.1, -0.5, 0.7, 0.5)}, {"R": (1.5, 0.2, 2.8, 0.02)},
    )
    assert not fail_ci["pass"] and not fail_ci["in_band_f1_ok"]

    fail_absent = decide_mode(
        "short", 1.20, 1.30,
        {"F1": (2.0, 0.8, 3.2, 0.002)}, {"P": (-1.5, -2.8, -0.2, 0.01)}, {"R": (2.5, 1.0, 4.0, 0.001)},
    )
    assert not fail_absent["pass"] and not fail_absent["in_band_absent_not_significantly_higher"]

    # 2. Style-confounded (outside [0.85, 1.15]) pass & fail branches
    sc_pass = decide_mode(
        "detailed", 2.00, 2.40,  # ratio 1.20 > 1.15
        {"F1": (3.0, 1.5, 4.5, 0.001)}, {"P": (1.2, 0.2, 2.2, 0.02)}, {"R": (2.0, 0.5, 3.5, 0.01)},
    )
    assert sc_pass["style_confounded"] and sc_pass["pass"] and sc_pass["branch"] == "style_confounded"

    sc_fail = decide_mode(
        "detailed", 2.00, 2.40,
        {"F1": (4.0, 2.5, 5.5, 0.0002)}, {"P": (0.8, -0.1, 1.7, 0.08)}, {"R": (3.0, 1.5, 4.5, 0.001)},
    )
    assert sc_fail["style_confounded"] and not sc_fail["pass"]

    # 3. Qualifiers (contamination-driven / language-driven)
    assert qualifier_flag(2.4, (0.8, -1.2, 2.8, 0.4))["flagged"] is True
    assert qualifier_flag(2.4, (1.5, -0.5, 3.5, 0.15))["flagged"] is False  # point >= half
    assert qualifier_flag(2.4, (1.0, 0.1, 1.9, 0.03))["flagged"] is False   # CI excludes 0

    # 4. Tone normalisation helper
    vt_t = _vi_terms_tone()
    assert norm_tone("một tòa nhà") == "một toà nhà"
    assert vi_objects_tone("Một đoàn tàu hỏa chạy qua.", vt_t) == {"train"}
    assert vi_objects_tone("Một đoàn tàu hoả chạy qua.", vt_t) == {"train"}

    # 5. Subset files if built
    if MANIFEST_1000.exists() and VAL2017_IDS.exists():
        m2500 = [x["cocoid"] for x in json.loads(MANIFEST_2500.read_text(encoding="utf-8"))["images"]]
        m1000 = [x["cocoid"] for x in json.loads(MANIFEST_1000.read_text(encoding="utf-8"))["images"]]
        v17 = [int(x) for x in VAL2017_IDS.read_text(encoding="utf-8").split()]
        assert m1000 == sorted(m1000) and len(m1000) == 1000 and set(m1000) <= set(m2500)
        assert v17 == sorted(v17) and len(v17) == 295 and len(set(v17) & set(m1000)) == 121


def main() -> int:
    ap = build_parser()
    args = ap.parse_args()
    if args.self_check:
        _check()
        print("s0_screen self-check ok")
        return 0
    if args.cmd == "subsets":
        res = build_subsets(Path(args.val2017_names) if args.val2017_names else None)
        _check()
        print(json.dumps(res, indent=1))
        return 0
    if args.cmd == "preflight":
        _check()
        res = run_preflight(args)
        text = json.dumps(res, indent=1)
        if args.out:
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(text)
        return 0
    if args.cmd == "verdict":
        _check()
        res = run_verdict(args)
        text = json.dumps(res, indent=1)
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(text)
        return 0
    ap.error("specify a subcommand (subsets, preflight, verdict) or --self-check")
    return 1


if __name__ == "__main__":
    sys.exit(main())
