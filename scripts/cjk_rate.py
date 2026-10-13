#!/usr/bin/env python3
"""CJK-rate audit across prediction files and COCO shard JSONLs (judge D10 (iv)(b)).

    python3 scripts/cjk_rate.py --results data/results --out data/results/cjk_rate.json
    python3 scripts/cjk_rate.py --self-check

Writes counts, percentages, and image IDs (`cjk_ids`) only — never caption text.
Regex = `clean_supervision.CJK_RE` (CJK radicals/symbols, Hiragana, Katakana, CJK unified
ideographs, Hangul syllables, CJK compatibility ideographs, halfwidth/fullwidth forms).

Sensitivity-row definition (D10 (iv)(b)):
  A system's sensitivity-row score is computed by the same evaluation script on the subset
  of images where its own caption contains no CJK match (`image_id not in cjk_ids`).
  Paired deltas between two systems use the intersection of their CJK-free image sets
  (where neither caption has a CJK match; `object_prf._vs_table` already intersects IDs).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from clean_supervision import CJK_RE as CJK  # noqa: E402


def _caption_str(val) -> str:
    if isinstance(val, list):
        return (val[0] if val else "") or ""
    return val or ""


def score_mapping(preds: dict[str, str]) -> dict:
    """Return {n_captions, cjk_captions, cjk_pct, cjk_ids} for {id: caption}; never stores text."""
    n = len(preds)
    cjk_ids = sorted(
        (str(k) for k, v in preds.items() if CJK.search(_caption_str(v))),
        key=lambda x: (0, int(x)) if x.isdigit() else (1, x),
    )
    n_cjk = len(cjk_ids)
    return {
        "n_captions": n,
        "cjk_captions": n_cjk,
        "cjk_pct": round(100.0 * n_cjk / n, 1) if n else 0.0,
        "cjk_ids": cjk_ids,
    }


def scan_results(results_dir: Path) -> dict:
    ktvic: dict[str, dict] = {}
    for f in sorted(results_dir.glob("*.preds.json")):
        name = f.name.removesuffix(".preds.json")
        preds = json.loads(f.read_text(encoding="utf-8"))
        ktvic[name] = score_mapping(preds)

    uitviic: dict[str, dict] = {}
    uit_dir = results_dir / "uitviic"
    if uit_dir.is_dir():
        for f in sorted(uit_dir.glob("*.preds.json")):
            name = f.name.removesuffix(".preds.json")
            preds = json.loads(f.read_text(encoding="utf-8"))
            uitviic[name] = score_mapping(preds)

    group_a: dict[str, dict] = {}
    ga_dir = results_dir / "group_a"
    if ga_dir.is_dir():
        for f in sorted(ga_dir.glob("*.json")):
            data = json.loads(f.read_text(encoding="utf-8"))
            if isinstance(data, dict) and isinstance(data.get("predictions"), dict):
                group_a[f.stem] = score_mapping(data["predictions"])

    coco_shards: dict[str, dict] = {}
    shard_groups: dict[str, list[Path]] = {}
    for f in sorted(results_dir.glob("*/*.shard*.jsonl")):
        prefix = f.name.split(".shard", 1)[0]
        key = f"{f.parent.name}/{prefix}"
        shard_groups.setdefault(key, []).append(f)
    for key, files in sorted(shard_groups.items()):
        merged: dict[str, str] = {}
        for f in files:
            for line in f.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                row = json.loads(line)
                cid = str(row.get("cocoid", row.get("image_id")))
                merged[cid] = _caption_str(row.get("caption", ""))
        coco_shards[key] = score_mapping(merged)

    return {
        "regex": CJK.pattern,
        "regex_source": "scripts/clean_supervision.py:CJK_RE",
        "sensitivity_rule": (
            "Score each system with the same scorer on the subset of images where its own caption "
            "has no CJK match (id not in cjk_ids); paired deltas use images where neither caption has CJK."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "ktvic": ktvic,
        "uitviic": uitviic,
        "group_a": group_a,
        "coco_shards": coco_shards,
    }


def _check() -> None:
    assert CJK.search("một chiếc bàn") is None
    assert CJK.search("một cái thìa羹") is not None
    assert CJK.search("câu có dấu chấm câu 。") is not None
    assert CJK.search("かな") is not None and CJK.search("한글") is not None
    sample = {"10": "một chiếc xe máy", "2": "một tòa nhà 高", "3": ["không có gì"]}
    r = score_mapping(sample)
    assert r == {"n_captions": 3, "cjk_captions": 1, "cjk_pct": 33.3, "cjk_ids": ["2"]}, r


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results", default="data/results")
    ap.add_argument("--out", default="data/results/cjk_rate.json")
    ap.add_argument("--self-check", action="store_true")
    args = ap.parse_args()
    if args.self_check:
        print("cjk_rate _check ok")
        return 0

    out_data = scan_results(Path(args.results).expanduser())
    out_path = Path(args.out).expanduser()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"wrote {out_path} (ktvic={len(out_data['ktvic'])}, uitviic={len(out_data['uitviic'])}, "
        f"group_a={len(out_data['group_a'])}, coco_shards={len(out_data['coco_shards'])})"
    )
    return 0


if __name__ == "__main__":
    _check()
    sys.exit(main())
