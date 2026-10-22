"""'cây' classifier-noun audit (Paper B, Section 3.5): counts only, no caption text printed.

Every 'cây' that the v2 matcher (rescap.chair.objects_in) maps to the class "tree" is classified by the next token:
a classifier use (cây + a noun in scripts/nap.py CLASSIFIED["cây"], e.g. cây cột, cây cầu), the compound cây xăng,
or another use. Reports counts for the KTVIC references and the given systems' outputs, and how stripping the
classifier uses would change the "tree" TP/FP/FN on the test split.

    NCS_DATA=/path/to/ncs-data python scripts/kit_b/cay_audit.py --out cay_audit.json [--systems A B ...]

Needs $NCS_DATA/datasets/ktvic/{train,test}_data.json and system outputs $NCS_DATA/results/<system>.preds.json.
Copied from the authors' cay_audit.py (sha256 8ac3641fc765a696108ab2534f14733054c7eb07bd1ba0436d0ffe9dba7556a4);
changes: data paths read from $NCS_DATA, systems and output path are arguments, and the authors' internal count
assertions are dropped.
"""
from __future__ import annotations
import argparse, ast, json, os, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = Path(os.environ.get("NCS_DATA", Path.home() / "ncs-data"))
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]

from rescap.chair import _NOT_OBJECTS, _NOUNS, _TOKEN, _ancestors, _strip_colour_phrases, norm_tone, objects_in
# CLASSIFIED is read from scripts/nap.py without importing it: nap.py's imports need the CHAIR synonym list
# (data/coco_probe/chair_synonyms.txt), which this audit does not use.
_NAP = ast.parse((ROOT / "scripts/nap.py").read_text(encoding="utf-8"))
CLASSIFIED = next(ast.literal_eval(n.value) for n in _NAP.body
                  if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "CLASSIFIED")

# Classifier-use nouns after 'cây' from nap.py CLASSIFIED["cây"] + RESUME.md step 7 extras
CLASSIFIER_NOUNS = set(CLASSIFIED["cây"]) | {"kim", "sào"}
EXOCENTRIC_CAY = {"xăng"}  # 'cây xăng' = gas station

def scan_caption(text: str) -> dict:
    """Replicate objects_in scan; inspect every 1-token 'cây' match and its following token(s)."""
    tokens = [t for t in _TOKEN.findall(_strip_colour_phrases(norm_tone(text.lower())))]
    i = 0
    total_cay = 0
    cay_cau = 0
    classifier_hits = Counter()
    exocentric_hits = Counter()
    other_next = Counter()
    non_classifier_cay = 0
    while i < len(tokens):
        hit = None
        for length in (3, 2, 1):
            if i + length > len(tokens):
                continue
            cand = " ".join(tokens[i : i + length])
            if cand in _NOUNS and cand not in _NOT_OBJECTS:
                hit = (_NOUNS[cand], length)
                break
        if hit:
            if hit[0] == "cây" and hit[1] == 1:
                total_cay += 1
                n1 = tokens[i + 1] if i + 1 < len(tokens) else "<EOS>"
                n2 = " ".join(tokens[i + 1 : i + 3]) if i + 2 < len(tokens) else ""
                if n2 in CLASSIFIER_NOUNS:
                    classifier_hits[n2] += 1
                elif n1 in CLASSIFIER_NOUNS:
                    classifier_hits[n1] += 1
                    if n1 == "cầu":
                        cay_cau += 1
                elif n1 in EXOCENTRIC_CAY:
                    exocentric_hits[n1] += 1
                else:
                    non_classifier_cay += 1
                    other_next[n1] += 1
            i += hit[1]
        else:
            i += 1
    return {
        "total_cay_tokens": total_cay,
        "cay_cau_tokens": cay_cau,
        "classifier_cay_tokens": sum(classifier_hits.values()),
        "exocentric_cay_tokens": sum(exocentric_hits.values()),
        "tree_or_other_cay_tokens": non_classifier_cay,
        "classifier_breakdown": dict(classifier_hits.most_common()),
        "exocentric_breakdown": dict(exocentric_hits.most_common()),
        "top_other_next_tokens": dict(other_next.most_common(10)),
    }

def summarise_corpus(caps_by_img: dict[str, list[str]]) -> dict:
    tot_caps = 0
    tot_cay_tok = 0
    tot_cay_cau_tok = 0
    tot_clf_tok = 0
    tot_exo_tok = 0
    caps_with_cay = 0
    caps_with_cay_cau = 0
    caps_with_clf_cay = 0
    caps_with_only_clf_cay = 0  # caption has emitted 'cây' ONLY from classifier/exocentric use
    imgs_with_cay = 0
    imgs_with_cay_cau = 0
    imgs_with_clf_cay = 0
    imgs_with_only_clf_cay = 0  # image union has 'cây' ONLY because of classifier/exocentric use
    clf_breakdown = Counter()
    exo_breakdown = Counter()
    other_next = Counter()

    for img_id, caps in caps_by_img.items():
        img_has_cay = False
        img_has_cay_cau = False
        img_has_clf = False
        img_has_real_cay = False
        for c in caps:
            tot_caps += 1
            r = scan_caption(c)
            tot_cay_tok += r["total_cay_tokens"]
            tot_cay_cau_tok += r["cay_cau_tokens"]
            tot_clf_tok += r["classifier_cay_tokens"]
            tot_exo_tok += r["exocentric_cay_tokens"]
            clf_breakdown.update(r["classifier_breakdown"])
            exo_breakdown.update(r["exocentric_breakdown"])
            other_next.update(r["top_other_next_tokens"])
            if r["total_cay_tokens"] > 0:
                caps_with_cay += 1
                img_has_cay = True
            if r["cay_cau_tokens"] > 0:
                caps_with_cay_cau += 1
                img_has_cay_cau = True
            if r["classifier_cay_tokens"] > 0:
                caps_with_clf_cay += 1
                img_has_clf = True
            if r["tree_or_other_cay_tokens"] > 0:
                img_has_real_cay = True
            elif r["total_cay_tokens"] > 0:
                caps_with_only_clf_cay += 1
        if img_has_cay:
            imgs_with_cay += 1
        if img_has_cay_cau:
            imgs_with_cay_cau += 1
        if img_has_clf:
            imgs_with_clf_cay += 1
        if img_has_cay and not img_has_real_cay:
            imgs_with_only_clf_cay += 1

    return {
        "n_images": len(caps_by_img),
        "n_captions": tot_caps,
        "emitted_cay_tokens": tot_cay_tok,
        "cay_cau_tokens": tot_cay_cau_tok,
        "classifier_cay_tokens": tot_clf_tok,
        "exocentric_cay_xang_tokens": tot_exo_tok,
        "captions_with_cay": caps_with_cay,
        "captions_with_cay_cau": caps_with_cay_cau,
        "captions_with_classifier_cay": caps_with_clf_cay,
        "captions_where_cay_is_only_classifier_or_xang": caps_with_only_clf_cay,
        "images_with_cay": imgs_with_cay,
        "images_with_cay_cau": imgs_with_cay_cau,
        "images_with_classifier_cay": imgs_with_clf_cay,
        "images_where_cay_is_only_classifier_or_xang": imgs_with_only_clf_cay,
        "classifier_noun_breakdown": dict(clf_breakdown.most_common()),
        "exocentric_breakdown": dict(exo_breakdown.most_common()),
        "top_non_classifier_next_tokens": dict(other_next.most_common(10)),
    }

def load_ref_corpus(path: Path) -> dict[str, list[str]]:
    d = json.loads(path.read_text(encoding="utf-8"))
    by_img: dict[str, list[str]] = defaultdict(list)
    for a in d["annotations"]:
        by_img[str(a.get("image_id", a.get("id")))].append(a.get("caption") or a.get("segment_caption") or "")
    return dict(by_img)

def load_pred_corpus(path: Path) -> dict[str, list[str]]:
    d = json.loads(path.read_text(encoding="utf-8"))
    return {str(k): [(v[0] if isinstance(v, list) else v) or ""] for k, v in d.items()}

SYSTEMS = [
    "p1assist_s42-short", "p1assist_s42-detailed",
    "p1assist_s43-short", "p1assist_s43-detailed",
    "p1assist_s44-short", "p1assist_s44-detailed",
    "fuse2_s42-short", "fuse2_s42-detailed",
    "fuse2_s43-short", "fuse2_s43-detailed",
    "fuse2_s44-short", "fuse2_s44-detailed",
    "p1_s43-short", "p1_s43-detailed",
    "p1-gold-short", "p1-gold-detailed",
    "zeroshot-short", "zeroshot-detailed",
]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path, default=Path("cay_audit.json"))
    ap.add_argument("--systems", nargs="+", default=SYSTEMS)
    a = ap.parse_args()
    systems = a.systems
    ref_train = load_ref_corpus(DATA / "datasets/ktvic/train_data.json")
    ref_test = load_ref_corpus(DATA / "datasets/ktvic/test_data.json")

    corpora = {
        "ktvic_train_refs": summarise_corpus(ref_train),
        "ktvic_test_refs": summarise_corpus(ref_test),
    }

    pred_corpora = {}
    for s in systems:
        p = load_pred_corpus(DATA / "results" / f"{s}.preds.json")
        pred_corpora[s] = summarise_corpus(p)

    # Interaction between prediction classifier-'cây' and KTVIC test reference gold 'cây':
    # On how many test images does stripping classifier/exocentric 'cây' (in both gold and pred)
    # change whether 'cây' is a TP, FP, or FN?
    ref_test_info = {}
    for img_id, cs in ref_test.items():
        has_any_cay = any(scan_caption(c)["total_cay_tokens"] > 0 for c in cs)
        has_real_cay = any(scan_caption(c)["tree_or_other_cay_tokens"] > 0 for c in cs)
        ref_test_info[img_id] = (has_any_cay, has_real_cay)

    interaction = {}
    for s in systems:
        p = load_pred_corpus(DATA / "results" / f"{s}.preds.json")
        tp_old = fp_old = fn_old = 0
        tp_new = fp_new = fn_new = 0
        for img_id, cs in p.items():
            g_old, g_new = ref_test_info[img_id]
            r = scan_caption(cs[0])
            m_old = r["total_cay_tokens"] > 0
            m_new = r["tree_or_other_cay_tokens"] > 0
            tp_old += (m_old and g_old)
            fp_old += (m_old and not g_old)
            fn_old += (not m_old and g_old)
            tp_new += (m_new and g_new)
            fp_new += (m_new and not g_new)
            fn_new += (not m_new and g_new)
        interaction[s] = {
            "old_cay_tp_fp_fn": [tp_old, fp_old, fn_old],
            "stripped_cay_tp_fp_fn": [tp_new, fp_new, fn_new],
            "delta_tp_fp_fn": [tp_new - tp_old, fp_new - fp_old, fn_new - fn_old],
        }

    report = {
        "references": corpora,
        "predictions": pred_corpora,
        "test_tp_fp_fn_impact_if_classifier_cay_stripped": interaction,
    }
    a.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("cay_audit ok; wrote", a.out)

if __name__ == "__main__":
    main()
