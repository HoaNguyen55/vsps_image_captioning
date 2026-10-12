#!/usr/bin/env python
"""Pre-registered Vietnamese caption diagnostics (R6 N1): person-reference level, plural marking, frame/morpheme
rates and culture-term recall by train-frequency band, per caption file.

    NCS_DATA=data python scripts/vi_diagnostics.py --split dev --preds p1dev-dev300-short.json rl-dev300-short.json
    NCS_DATA=data python scripts/vi_diagnostics.py --split test --preds data/results/p1-gold-short.preds.json
    NCS_DATA=data python scripts/vi_diagnostics.py --build-lists   # rewrite the frozen lists (train minus dev300)

The word lists in manuscript/prereg/2026-10-12_vietnamese_diagnostics/ are ANALYSIS lists, never labels: they only
select which surface strings are counted. Their counts and bands come from the KTVIC TRAIN references of the images
outside data/splits/ktvic_dev300.txt. Use --split dev for any go/no-go decision; --split test only for reporting.

Rates over the split's images (one caption per image; text lowercased, NFC, KTVIC old-style tone placement):
  person_bare / person_gendered / person_age   among captions naming a person, the share that is bare "người" only /
                                               has a gendered term / has an age-graded term (person_terms.tsv)
  q_<term>      occurrences per caption of each plural or quantity marker (quantifiers.tsv; longest match first)
  f_<marker>    occurrences per caption of each frame marker; init_<word>: share of captions starting with it
  cult_recall_<band>  over (image, term) pairs that >= 2 of the image's 5 references name: share the caption names
  cult_precision      share of the caption's culture-term mentions that at least one reference names
"refs" reports the same per-caption rates for the references themselves (culture rates omitted: self-inflated).
With two or more --preds files, each later file is compared with the first: difference and its 95% percentile CI
over a paired bootstrap of images (B = 2000, numpy seed 0).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = Path(os.environ.get("NCS_DATA", ROOT / "data"))
LISTS = ROOT / "manuscript" / "prereg" / "2026-10-12_vietnamese_diagnostics"
DEV = ROOT / "data" / "splits" / "ktvic_dev300.txt"
BANDS = (("head", 50), ("mid", 10), ("tail", 1))
B_BOOT = 2000

#: Candidate inventories (a priori, general Vietnamese lexicology). --build-lists keeps the train-attested ones.
CANDIDATES = {
    "person_terms": {
        "gendered": ["phụ nữ", "đàn ông", "đàn bà"],
        "age_graded": ["cô gái", "chàng trai", "thiếu nữ", "em bé", "bé gái", "bé trai", "cậu bé", "cô bé", "đứa trẻ",
                       "đứa bé", "trẻ em", "trẻ con", "thanh niên", "bạn trẻ", "học sinh", "cụ ông", "cụ bà", "ông cụ",
                       "bà cụ", "ông lão", "bà lão", "người già", "người cao tuổi"],
    },
    "quantifiers": ["những", "nhiều", "một vài", "các", "một số", "vài"],
    "frames": ["của", "sự xuất hiện", "đang", "xuất hiện"],
    "culture_terms": {
        "clothing": ["áo dài", "nón lá", "áo bà ba", "khăn rằn", "áo tứ thân", "khăn vấn", "khăn đóng", "nón quai thao",
                     "áo yếm", "nón bảo hiểm", "mũ bảo hiểm"],
        "transport": ["xe máy", "xích lô", "xe ôm", "xuồng", "ghe", "thuyền thúng", "đò", "xe ba gác", "xe lam",
                      "thuyền rồng"],
        "food": ["bánh mì", "phở", "bún", "bánh chưng", "bánh tét", "bánh xèo", "nem", "chả giò", "gỏi cuốn", "cà phê",
                 "trà đá", "chè", "xôi", "hủ tiếu", "cơm tấm", "bánh cuốn", "mì quảng", "nước mắm", "bánh bao",
                 "bánh trung thu", "mứt", "bánh", "trà sữa", "sinh tố", "mía", "dừa"],
        "commerce": ["chợ", "chợ nổi", "chợ đêm", "quán", "quán cóc", "sạp", "gánh hàng", "hàng rong", "quang gánh",
                     "đòn gánh", "tạp hoá", "vỉa hè", "hẻm", "phố cổ", "phố đi bộ", "gian hàng", "quầy hàng"],
        "religion_heritage": ["chùa", "đình", "đền", "miếu", "lăng", "bát hương", "lư hương", "nhang", "bàn thờ",
                              "tượng phật", "phật", "tháp chuông", "cổng tam quan", "văn miếu", "nhà thờ", "bia đá",
                              "di tích", "bảo tàng", "hoàng thành", "thành cổ"],
        "festival": ["tết", "hoa mai", "hoa đào", "câu đối", "lồng đèn", "đèn lồng", "múa lân", "ông địa", "trung thu",
                     "hoa đăng", "đèn trời", "lì xì", "giáng sinh", "lễ hội"],
        "rural": ["ruộng", "lúa", "ruộng bậc thang", "trâu", "mái tranh", "cầu khỉ", "lũy tre", "rơm", "nông dân",
                  "cánh đồng"],
        "state_people": ["bộ đội", "đồng chí", "công an", "cờ đỏ sao vàng", "cờ tổ quốc", "chân dung bác", "bác hồ",
                         "lá cờ", "cờ"],
    },
}
INITIAL = ("có", "ở", "một", "đây")
_TONE = {"òa": "oà", "óa": "oá", "ỏa": "oả", "õa": "oã", "ọa": "oạ", "òe": "oè", "óe": "oé", "ỏe": "oẻ", "õe": "oẽ",
         "ọe": "oẹ", "ùy": "uỳ", "úy": "uý", "ủy": "uỷ", "ũy": "uỹ", "ụy": "uỵ"}
_TONE_RE = re.compile("(" + "|".join(_TONE) + r")(?![^\W\d_])")
_WORD = re.compile(r"[^\W\d_]+")


def syllables(text: str) -> list[str]:
    """Lowercase NFC syllables with KTVIC's old-style tone placement (hóa -> hoá); punctuation and digits dropped."""
    text = _TONE_RE.sub(lambda m: _TONE[m.group(1)], unicodedata.normalize("NFC", text.lower()))
    return _WORD.findall(text)


def find_terms(sylls: list[str], terms: list[str]) -> list[str]:
    """Non-overlapping occurrences, longest term first, scanning left to right."""
    keys = sorted({tuple(t.split()) for t in terms}, key=len, reverse=True)
    found, i = [], 0
    while i < len(sylls):
        hit = next((k for k in keys if tuple(sylls[i:i + len(k)]) == k), None)
        if hit:
            found.append(" ".join(hit))
            i += len(hit)
        else:
            i += 1
    return found


def read_tsv(name: str) -> list[dict[str, str]]:
    lines = [ln for ln in (LISTS / name).read_text(encoding="utf-8").splitlines() if ln and not ln.startswith("#")]
    head = lines[0].split("\t")
    return [dict(zip(head, ln.split("\t"))) for ln in lines[1:]]


def load_lists() -> dict:
    person = read_tsv("person_terms.tsv")
    return {"gendered": [r["term"] for r in person if r["class"] == "gendered"],
            "age_graded": [r["term"] for r in person if r["class"] == "age_graded"],
            "quantifiers": [r["term"] for r in read_tsv("quantifiers.tsv")],
            "frames": [r["term"] for r in read_tsv("frames.tsv")],
            "culture": {r["term"]: r["band"] for r in read_tsv("culture_terms.tsv")}}


def caption_counts(text: str, lists: dict) -> dict[str, float]:
    s = syllables(text)
    named = bool(find_terms(s, lists["gendered"]) or find_terms(s, lists["age_graded"]))
    out = {"has_person": float(named or "người" in s), "bare": float("người" in s and not named),
           "gendered": float(bool(find_terms(s, lists["gendered"]))),
           "age": float(bool(find_terms(s, lists["age_graded"])))}
    q, f = Counter(find_terms(s, lists["quantifiers"])), Counter(find_terms(s, lists["frames"]))
    out.update({f"q_{t}": float(q[t]) for t in lists["quantifiers"]})
    out.update({f"f_{t}": float(f[t]) for t in lists["frames"]})
    out.update({f"init_{w}": float(bool(s) and s[0] == w) for w in INITIAL})
    return out


def image_counts(caption: str, refs: list[str], lists: dict) -> dict[str, float]:
    """Per-image numerators and denominators; corpus rates are ratios of sums, so the bootstrap resamples images."""
    out = caption_counts(caption, lists)
    per_ref = [caption_counts(r, lists) for r in refs]
    specific = out["gendered"] or out["age"]
    out["cons_spec_n"] = float(sum(r["gendered"] or r["age"] for r in per_ref) >= 3)
    out["cons_spec_hit"] = float(out["cons_spec_n"] and specific)
    out["cons_bare_n"] = float(sum(r["bare"] for r in per_ref) >= 3)
    out["cons_bare_hit"] = float(out["cons_bare_n"] and out["bare"])
    out["cons_nhung_n"] = float(sum(r["q_những"] > 0 for r in per_ref) >= 2) if "những" in lists["quantifiers"] else 0.0
    out["cons_nhung_hit"] = float(out["cons_nhung_n"] and out.get("q_những", 0) > 0)
    culture = list(lists["culture"])
    mentioned = set(find_terms(syllables(caption), culture))
    ref_sets = [set(find_terms(syllables(r), culture)) for r in refs]
    shared = Counter(t for rs in ref_sets for t in rs)
    for band, _ in BANDS:
        targets = [t for t, k in shared.items() if k >= 2 and lists["culture"][t] == band]
        out[f"cult_n_{band}"] = float(len(targets))
        out[f"cult_hit_{band}"] = float(sum(t in mentioned for t in targets))
    out["cult_mentions"] = float(len(mentioned))
    out["cult_mentions_in_refs"] = float(sum(any(t in rs for rs in ref_sets) for t in mentioned))
    return out


def to_matrix(rows: list[dict[str, float]]) -> tuple[list[str], np.ndarray]:
    keys = list(rows[0])
    return keys, np.array([[r[k] for k in keys] for r in rows])


def ratio(num: float, den: float) -> float:
    return float(num / den) if den else float("nan")


def rates(keys: list[str], m: np.ndarray) -> dict[str, float]:
    col = dict(zip(keys, m.sum(0)))
    out = {f"person_{k}": ratio(col[k], col["has_person"]) for k in ("bare", "gendered", "age")}
    out["person_mention_share"] = ratio(col["has_person"], len(m))
    out.update({k: ratio(col[k], len(m)) for k in keys if k.startswith(("q_", "f_", "init_"))})
    for name in ("spec", "bare", "nhung"):
        out[f"cons_{name}_recall"] = ratio(col[f"cons_{name}_hit"], col[f"cons_{name}_n"])
        out[f"cons_{name}_images"] = float(col[f"cons_{name}_n"])
    for band, _ in BANDS:
        out[f"cult_recall_{band}"] = ratio(col[f"cult_hit_{band}"], col[f"cult_n_{band}"])
        out[f"cult_targets_{band}"] = float(col[f"cult_n_{band}"])
    hits = sum(col[f"cult_hit_{b}"] for b, _ in BANDS)
    out["cult_recall_all"] = ratio(hits, sum(col[f"cult_n_{b}"] for b, _ in BANDS))
    out["cult_precision"] = ratio(col["cult_mentions_in_refs"], col["cult_mentions"])
    return out


def compare(base: list[dict], other: list[dict]) -> dict[str, list[float]]:
    """other - base per rate: point and 95% percentile CI over a paired bootstrap of images."""
    keys, a = to_matrix(base)
    _, b = to_matrix(other)
    ra, rb = rates(keys, a), rates(keys, b)
    point = {k: rb[k] - ra[k] for k in ra}
    rng = np.random.default_rng(0)
    boots = {k: [] for k in point}
    for _ in range(B_BOOT):
        idx = rng.integers(0, len(a), len(a))
        sa, sb = rates(keys, a[idx]), rates(keys, b[idx])
        for k in point:
            boots[k].append(sb[k] - sa[k])
    out = {}
    for k, v in boots.items():
        v = np.array(v)
        lo, hi = (float("nan"),) * 2 if np.isnan(v).all() else np.nanpercentile(v, [2.5, 97.5])
        out[k] = [round(point[k], 4), round(float(lo), 4), round(float(hi), 4)]
    return out


def references(split: str) -> dict[str, list[str]]:
    """{image id: raw captions}; split = test, dev (train images in DEV) or train_minus_dev."""
    name = "test_data.json" if split == "test" else "train_data.json"
    refs: dict[str, list[str]] = {}
    for a in json.loads((DATA / "datasets" / "ktvic" / name).read_text(encoding="utf-8"))["annotations"]:
        if a.get("caption"):
            refs.setdefault(str(a["image_id"]), []).append(a["caption"])
    if split == "test":
        return refs
    dev = set(DEV.read_text(encoding="utf-8").split())
    return {i: v for i, v in refs.items() if (i in dev) == (split == "dev")}


def load_preds(path: str) -> dict[str, str]:
    """A preds.json ({id: caption or [caption]}) or an evaluate.py --out report (its "predictions")."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    raw = raw.get("predictions", raw)
    return {str(k): v[0] if isinstance(v, list) else v for k, v in raw.items()}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def band_of(n: int) -> str:
    return next(b for b, lo in BANDS if n >= lo)


def build_lists() -> None:
    """Write the frozen lists: candidates attested in KTVIC train references outside dev300, with train counts."""
    refs = references("train_minus_dev")
    sylls = [syllables(c) for cs in refs.values() for c in cs]
    pos0 = [syllables(cs[0]) for cs in refs.values()]
    LISTS.mkdir(parents=True, exist_ok=True)
    head = (f"# ANALYSIS LIST, NEVER LABELS. Train-derived: KTVIC train references of the {len(refs)} images outside "
            f"data/splits/ktvic_dev300.txt ({len(sylls)} captions). Built by scripts/vi_diagnostics.py --build-lists.\n")
    pc = CANDIDATES["person_terms"]
    pool = pc["gendered"] + pc["age_graded"]
    per_person = Counter(t for s in sylls for t in set(find_terms(s, pool)))
    (LISTS / "person_terms.tsv").write_text(head + "term\tclass\ttrain_captions\n" + "".join(
        f"{t}\t{cls}\t{per_person[t]}\n" for cls in ("gendered", "age_graded") for t in pc[cls] if per_person[t]),
        encoding="utf-8")
    for name in ("quantifiers", "frames"):
        terms = CANDIDATES[name]
        per = Counter(t for s in sylls for t in find_terms(s, terms))
        per0 = Counter(t for s in pos0 for t in find_terms(s, terms))
        (LISTS / f"{name}.tsv").write_text(head + "term\ttrain_rate_per_caption\ttrain_rate_position0\n" + "".join(
            f"{t}\t{per[t] / len(sylls):.4f}\t{per0[t] / len(pos0):.4f}\n" for t in terms if per[t]), encoding="utf-8")
    cul = {t: cat for cat, ts in CANDIDATES["culture_terms"].items() for t in ts}
    counts = Counter(t for s in sylls for t in set(find_terms(s, list(cul))))
    (LISTS / "culture_terms.tsv").write_text(
        head + "# band by train_captions: head >= 50, mid 10-49, tail 1-9; unattested candidates dropped\n"
        + "term\tcategory\ttrain_captions\tband\n"
        + "".join(f"{t}\t{cul[t]}\t{counts[t]}\t{band_of(counts[t])}\n" for t in cul if counts[t]), encoding="utf-8")
    for f in sorted(LISTS.glob("*.tsv")):
        print(f"  {f.name}: sha256 {sha256(f)}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--split", choices=("dev", "test"), default="dev")
    ap.add_argument("--preds", nargs="*", default=[])
    ap.add_argument("--build-lists", action="store_true")
    ap.add_argument("--out", help="write the JSON report here")
    args = ap.parse_args()
    if args.build_lists:
        build_lists()
        return 0
    lists, refs = load_lists(), references(args.split)
    ids = sorted(refs, key=int)
    report = {"split": args.split, "n_images": len(ids), "script_sha256": sha256(Path(__file__)),
              "lists_sha256": {f.name: sha256(f) for f in sorted(LISTS.glob("*.tsv"))}, "systems": {}, "compare": {}}
    keys, m = to_matrix([image_counts(r, refs[i], lists) for i in ids for r in refs[i]])
    report["refs"] = {k: round(v, 4) for k, v in rates(keys, m).items() if not k.startswith(("cult_", "cons_"))}
    rows = {}
    for path in args.preds:
        preds = load_preds(path)
        missing = [i for i in ids if i not in preds]
        if missing:
            raise SystemExit(f"{path}: no prediction for {len(missing)} of {len(ids)} {args.split} images")
        rows[path] = [image_counts(preds[i], refs[i], lists) for i in ids]
        report["systems"][path] = {k: round(v, 4) for k, v in rates(*to_matrix(rows[path])).items()}
    for path in args.preds[1:]:
        report["compare"][f"{path} - {args.preds[0]}"] = compare(rows[args.preds[0]], rows[path])
    text = json.dumps(report, ensure_ascii=False, indent=1)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


def _check() -> None:
    assert syllables("Có MỘT cô gái, đang hóa trang.") == ["có", "một", "cô", "gái", "đang", "hoá", "trang"]
    assert find_terms(syllables("có một vài người và vài con chó"), ["vài", "một vài"]) == ["một vài", "vài"]
    lists = {"gendered": ["phụ nữ"], "age_graded": ["cô gái"], "quantifiers": ["những", "nhiều"],
             "frames": ["của", "đang"], "culture": {"nón lá": "head", "xuồng": "tail"}}
    bare = caption_counts("có nhiều người đang đi", lists)
    assert bare["bare"] == 1 and bare["gendered"] == 0 and bare["q_nhiều"] == 1 and bare["f_đang"] == 1
    assert caption_counts("có một người phụ nữ", lists)["bare"] == 0
    assert caption_counts("hai cô gái đội nón lá", lists)["age"] == 1
    refs = ["cô gái đội nón lá", "một người đội nón lá", "có chiếc xuồng", "nón lá", "cô gái"]
    row = image_counts("hai cô gái đội nón lá", refs, lists)
    assert row["cult_n_head"] == 1 and row["cult_hit_head"] == 1 and row["cult_n_tail"] == 0
    r = rates(*to_matrix([row]))
    assert r["cult_recall_head"] == 1.0 and r["cult_precision"] == 1.0 and r["person_age"] == 1.0
    assert row["cons_spec_n"] == 0 and np.isnan(r["cons_spec_recall"])
    crowd = ["có nhiều người", "những người đang đi", "có những người", "một cô gái", "người đi bộ"]
    cr = image_counts("có nhiều người đang đi", crowd, lists)
    assert cr["cons_bare_n"] == 1 and cr["cons_bare_hit"] == 1 and cr["cons_nhung_n"] == 1 and cr["cons_nhung_hit"] == 0
    girls = image_counts("hai cô gái", ["cô gái", "hai cô gái", "cô gái cười", "người", "người"], lists)
    assert girls["cons_spec_n"] == 1 and girls["cons_spec_hit"] == 1
    diffs = compare([row, row | bare], [row, row | bare])
    assert all(v == [0.0, 0.0, 0.0] for v in diffs.values() if not np.isnan(v[0]))
    assert np.isnan(diffs["cult_recall_tail"][0])


if __name__ == "__main__":
    _check()
    sys.exit(main())
