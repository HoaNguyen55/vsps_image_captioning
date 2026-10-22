#!/usr/bin/env python3
"""Four post hoc controls for Paper B (CC-088 B-2 a-d; POST_HOC, registered verdicts unchanged).

  slotnull   (a) Section 3.2: the adjacent-doubleton share against a permutation null that keeps every image's
                 per-slot mention counts and every object's number of naming references (curveball swaps of the
                 per-image object x slot matrix).
  overlap    (b) Section 3.6: KTVIC test images with a UIT-OpenViIC copy over a grid of SSCD and Hamming
                 thresholds, from an existing feature cache (scripts/c_stage1/build_memory.py; never recomputed).
  panels     (c) Section 5.3: syllable n-gram overlap within the KTVIC panel, within the OpenViIC panel and
                 between them on the same images, with a mismatched-image baseline.
  baselines  (d) Section 3.3: punctuation, segmentation and PTB-list counts and CIDEr-D (P0 / PTB) of the two
                 published KTVIC baselines' outputs (pacman-ctm/thesis-code @1a8d105), passed by path.
Every output holds counts, rates and scores only: no caption, n-gram or per-image record is stored or printed.

    NCS_DATA=/path/to/ncs-data python scripts/kit_b/b2_controls.py slotnull --out slot_null.json
    NCS_DATA=... python scripts/kit_b/b2_controls.py overlap --cache FEAT_CACHE --sscd sscd_disc_mixup.torchscript.pt --out o.json
    NCS_DATA=... python scripts/kit_b/b2_controls.py panels --openviic-refs ktvic_openviic_refs.json --out p.json
    NCS_DATA=... python scripts/kit_b/b2_controls.py baselines --resnetlstm result_resnetlstm.json \\
        --vittrans result_vittrans.json --accessed 2026-10-22T10:31:09Z --out b.json
    python scripts/kit_b/b2_controls.py --selftest        # synthetic data only
Imports, unchanged: exchangeability_audit (load_coco_json_sets, audit_k5), protocol_pilot (rdr, Cider),
ptb_protocol (ptb, token_counts, is_punct_tok, load_refs), scripts/match_openviic.py (hamming) and rescap.chair.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
import tempfile
import unicodedata
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import exchangeability_audit as EX  # noqa: E402
import ptb_protocol as PT  # noqa: E402
from ptb_protocol import E4  # noqa: E402  protocol_pilot

DATA = EX.DATA
LABEL = "POST_HOC (CC-088 B-2 {}); registered verdicts unchanged; aggregates only"
B_BOOT, SEED = 1000, 0


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git_blob(p: Path) -> str:
    data = p.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def ci(a) -> list[float]:
    return [round(float(np.percentile(a, 2.5)), 4), round(float(np.percentile(a, 97.5)), 4)]


# ---------------------------------------------------------------- (a) slot-rate-preserving null
def to_rows(sets: list[set]) -> list[set[int]]:
    """Per image: object -> set of slots naming it (the rows of the object x slot matrix)."""
    objs = sorted(set().union(*sets))
    return [{r for r in range(len(sets)) if o in sets[r]} for o in objs]


def curveball(rows: list[set[int]], rng: random.Random, trades: int) -> None:
    """In place: `trades` curveball trades; row sizes and per-slot counts are invariant (Strona et al., 2014)."""
    if len(rows) < 2:
        return
    for _ in range(trades):
        a, b = rng.sample(range(len(rows)), 2)
        only_a, only_b = rows[a] - rows[b], rows[b] - rows[a]
        if not only_a or not only_b:
            continue
        pool = sorted(only_a | only_b)
        rng.shuffle(pool)
        common = rows[a] & rows[b]
        rows[a], rows[b] = common | set(pool[:len(only_a)]), common | set(pool[len(only_a):])


def stats(images: list[list[set[int]]], k: int = 5) -> tuple[float, float]:
    """(adjacent-doubleton share, lag-1 Jaccard minus mean of lags 2-4) as audit_k5 pools them."""
    adj = dbl = 0
    js, jn = np.zeros(k - 1), np.zeros(k - 1)
    for rows in images:
        for s in rows:
            if len(s) == 2:
                dbl += 1
                lo, hi = sorted(s)
                adj += hi - lo == 1
        slots = [{o for o, s in enumerate(rows) if r in s} for r in range(k)]
        for a in range(k):
            for b in range(a + 1, k):
                u = slots[a] | slots[b]
                if u:
                    js[b - a - 1] += len(slots[a] & slots[b]) / len(u)
                    jn[b - a - 1] += 1
    jac = js / np.maximum(jn, 1)
    return adj / max(dbl, 1), float(jac[0] - jac[1:].mean())


def slot_null(per_image: list[list[set]], draws: int, seed: int, burn: int = 50, thin: int = 5) -> dict:
    rng = random.Random(seed)
    images = [to_rows(s) for s in per_image]
    obs = stats(images)
    for rows in images:
        curveball(rows, rng, burn * len(rows))
    null = []
    for _ in range(draws):
        for rows in images:
            curveball(rows, rng, thin * len(rows))
        null.append(stats(images))
    null = np.array(null)
    out = {"images": len(images), "doubletons": sum(len(s) == 2 for rows in images for s in rows)}
    for j, name in enumerate(("adjacent_share", "jac_lag1_minus_mean_lag2to4")):
        ge = int((null[:, j] >= obs[j]).sum())
        out[name] = {"observed": round(obs[j], 4), "null_mean": round(float(null[:, j].mean()), 4),
                     "null_ci95": ci(null[:, j]), "null_max": round(float(null[:, j].max()), 4),
                     "draws_ge_observed": ge, "p_one_sided": round((ge + 1) / (draws + 1), 4)}
    return out


def cmd_slotnull(a) -> dict:
    from rescap.chair import objects_in

    fn = lambda c: set(objects_in(c))  # noqa: E731
    dev = DATA / "splits/ktvic_dev300.txt"
    jobs = [("ktvic_test_objects_in", DATA / "datasets/ktvic/test_data.json", None),
            ("ktvic_train_objects_in", DATA / "datasets/ktvic/train_data.json", None)]
    if dev.exists():
        jobs.append(("ktvic_dev300_objects_in", DATA / "datasets/ktvic/train_data.json",
                     set(dev.read_text("utf-8").split())))
    res = {"label": LABEL.format("a"), "draws": a.draws, "seed": a.seed, "burn_in_trades_per_row": 50,
           "trades_per_row_between_draws": 5,
           "null": "per image, uniform over object x slot matrices with the observed row sums (references naming "
                   "each object) and column sums (objects named by each slot); curveball trades", "splits": {}}
    for name, path, sub in jobs:
        ex5, _, _ = EX.load_coco_json_sets(path, fn, 5, sub)
        ref = EX.audit_k5(name, ex5, seed=0)
        r = slot_null(ex5, a.draws, a.seed)
        r["reproduces_audit_k5"] = (r["adjacent_share"]["observed"] == ref["adjacent_share"]
                                    and r["doubletons"] == ref["total_doubletons"]
                                    and r["jac_lag1_minus_mean_lag2to4"]["observed"] == ref["jac_lag1_minus_mean_lag2to4"])
        res["splits"][name] = r
        print(name, json.dumps(r), flush=True)
    return res


# ---------------------------------------------------------------- (b) overlap over a threshold grid
HASHES, SSCDS = (6, 8, 10), (0.5, 0.6, 0.7, 0.8)


def cache_key(paths: list[Path], sscd: Path) -> str:
    """build_memory.features' cache key: image sha256s in order, then the SSCD weights' sha256."""
    return hashlib.sha256(("|".join(map(sha256, paths)) + sha256(sscd)).encode()).hexdigest()[:16]


def overlap_counts(kt: dict, ov: dict, ov_split: np.ndarray) -> dict:
    from match_openviic import hamming

    ph = np.minimum(hamming(kt["phash"], ov["phash"]), hamming(kt["phash_m"], ov["phash"]))
    dh = np.minimum(hamming(kt["dhash"], ov["dhash"]), hamming(kt["dhash_m"], ov["dhash"]))
    hd = np.minimum(ph, dh)
    sim = np.nan_to_num(kt["sscd"]) @ np.nan_to_num(ov["sscd"]).T
    train = ov_split == "train"
    grid = {}
    for h in HASHES:
        for s in SSCDS:
            m = (hd <= h) & (sim >= s)
            grid[f"hamming_le_{h}_sscd_ge_{round(s * 100):03d}"] = {"any_split": int(m.any(1).sum()), "train": int(m[:, train].any(1).sum()),
                                              **{f"{sp}_copy": int(m[:, ov_split == sp].any(1).sum())
                                                 for sp in ("dev", "test")}}
    sscd_only = {f"sscd_ge_{round(s * 100):03d}": {"any_split": int((sim >= s).any(1).sum()), "train": int((sim[:, train] >= s).any(1).sum())}
                 for s in SSCDS}
    hash_only = {f"hamming_le_{h}": {"any_split": int((hd <= h).any(1).sum()), "train": int((hd[:, train] <= h).any(1).sum())}
                 for h in HASHES}
    return {"n_ktvic_test": len(kt["sscd"]), "n_openviic_captioned": len(ov["sscd"]),
            "grid": grid, "sscd_only": sscd_only, "hash_only": hash_only}


def cmd_overlap(a) -> dict:
    ds = DATA / "datasets"
    kt_files = [ds / "ktvic/images" / i["filename"]
                for i in json.loads((ds / "ktvic/test_data.json").read_text(encoding="utf-8"))["images"]]
    groups = {"kt_test": kt_files}
    for sp in ("train", "dev", "test"):
        names = sorted(json.loads((ds / f"openviic/uit-openviic-annotation-{sp}.json").read_text(encoding="utf-8")))
        groups[f"ov_{sp}"] = [ds / "openviic/images" / n for n in names]
    feats, keys = {}, {}
    for g, paths in groups.items():
        keys[g] = cache_key(paths, a.sscd)
        f = a.cache / f"feat_{keys[g]}.npz"
        if not f.exists():
            raise SystemExit(f"{g}: no cached features {f.name}; this script never recomputes them")
        feats[g] = dict(np.load(f))
        assert len(feats[g]["sscd"]) == len(paths), g
    ov = {k: np.concatenate([feats[f"ov_{sp}"][k] for sp in ("train", "dev", "test")])
          for k in ("phash", "dhash", "sscd")}
    split = np.array([sp for sp in ("train", "dev", "test") for _ in groups[f"ov_{sp}"]])
    res = {"label": LABEL.format("b"), "cache_keys": keys, "sscd_weights_sha256": sha256(a.sscd),
           "rule": "match = min(pHash, dHash Hamming; KTVIC direct or mirrored) <= h and SSCD cosine >= s "
                   "(scripts/match_openviic.py is_match); registered rule h = 10, s = 0.5",
           "scope": "captioned OpenViIC images only (train/dev/test annotation keys); the release's uncaptioned "
                    "files are not in the cache",
           "unreadable_openviic": {sp: int(len(feats[f'ov_{sp}']['unreadable'])) for sp in ("train", "dev", "test")},
           **overlap_counts(feats["kt_test"], ov, split)}
    reg = res["grid"]["hamming_le_10_sscd_ge_050"]
    res["gate_registered_rule_reproduces_555_401"] = reg["any_split"] == 555 and reg["train"] == 401
    res["gate_viclip_ot_rule_reproduces_401"] = res["sscd_only"]["sscd_ge_080"]["train"] == 401
    print(json.dumps(res, indent=1))
    if not (res["gate_registered_rule_reproduces_555_401"] and res["gate_viclip_ot_rule_reproduces_401"]):
        raise SystemExit("registered counts not reproduced from the cache: STOP")
    return res


# ---------------------------------------------------------------- (c) n-gram overlap of the two panels
def syllables(text: str) -> list[str]:
    from rescap.chair import norm_tone

    return re.sub(r"[^\w\s]", " ", norm_tone(unicodedata.normalize("NFC", text)).lower()).split()


def grams(toks: list[str], n: int) -> set:
    return {tuple(toks[i:i + n]) for i in range(len(toks) - n + 1)}


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a | b else 0.0


def mean_pair(xs: list[list[set]], ys: list[list[set]] | None, n: int) -> float:
    """Mean n-gram-set Jaccard over caption pairs: all pairs within xs (ys None) or every x-y pair."""
    if ys is None:
        v = [jaccard(xs[i][n - 1], xs[j][n - 1]) for i in range(len(xs)) for j in range(i + 1, len(xs))]
    else:
        v = [jaccard(x[n - 1], y[n - 1]) for x in xs for y in ys]
    return float(np.mean(v)) if v else float("nan")


def panel_overlap(kt: dict[str, list[str]], ov: dict[str, list[str]], seed: int = SEED) -> dict:
    ids = sorted(i for i in ov if i in kt and len(ov[i]) >= 2)
    tok = {("k", i): [syllables(c) for c in kt[i]] for i in ids} | {("o", i): [syllables(c) for c in ov[i]] for i in ids}
    g = {key: [[grams(t, n) for n in range(1, 5)] for t in v] for key, v in tok.items()}
    rng = np.random.default_rng(seed)
    while True:  # derangement: each image's KTVIC panel against another image's OpenViIC panel
        perm = rng.permutation(len(ids))
        if not (perm == np.arange(len(ids))).any():
            break
    per = {"within_ktvic": [], "within_openviic": [], "cross_same_image": [], "cross_mismatched_image": []}
    for j, i in enumerate(ids):
        other = ids[perm[j]]
        per["within_ktvic"].append([mean_pair(g[("k", i)], None, n) for n in range(1, 5)])
        per["within_openviic"].append([mean_pair(g[("o", i)], None, n) for n in range(1, 5)])
        per["cross_same_image"].append([mean_pair(g[("k", i)], g[("o", i)], n) for n in range(1, 5)])
        per["cross_mismatched_image"].append([mean_pair(g[("k", i)], g[("o", other)], n) for n in range(1, 5)])
    per = {k: np.array(v) for k, v in per.items()}
    idx = rng.integers(0, len(ids), size=(B_BOOT, len(ids)))
    out = {"images": len(ids), "ktvic_captions": sum(len(kt[i]) for i in ids),
           "openviic_captions": sum(len(ov[i]) for i in ids),
           "mean_syllables_per_caption": {
               "ktvic": round(float(np.mean([len(t) for i in ids for t in tok[("k", i)]])), 3),
               "openviic": round(float(np.mean([len(t) for i in ids for t in tok[("o", i)]])), 3)},
           "mean_pairwise_jaccard": {}, "differences": {}}
    for n in range(1, 5):
        c = n - 1
        out["mean_pairwise_jaccard"][f"n={n}"] = {
            k: {"est": round(float(v[:, c].mean()), 4), "ci95": ci(v[idx, c].mean(1))} for k, v in per.items()}
        out["differences"][f"n={n}"] = {
            name: {"est": round(float((per[x][:, c] - per[y][:, c]).mean()), 4),
                   "ci95": ci((per[x][idx, c] - per[y][idx, c]).mean(1))}
            for name, x, y in (("within_ktvic_minus_cross", "within_ktvic", "cross_same_image"),
                               ("within_openviic_minus_cross", "within_openviic", "cross_same_image"),
                               ("cross_minus_mismatched", "cross_same_image", "cross_mismatched_image"))}
    norm = {key: [" ".join(t) for t in v] for key, v in tok.items()}
    g8 = {key: [grams(t, 8) for t in v] for key, v in tok.items()}
    out["ktvic_refs_identical_to_an_openviic_caption"] = sum(c in set(norm[("o", i)]) for i in ids for c in norm[("k", i)])
    out["ktvic_refs_sharing_an_8gram_with_the_openviic_panel"] = sum(
        bool(x & set().union(*g8[("o", i)])) for i in ids for x in g8[("k", i)])
    out["derangement_seed"], out["bootstrap"] = seed, {"B": B_BOOT, "seed": seed, "unit": "image"}
    return out


def cmd_panels(a) -> dict:
    kt = PT.load_refs(DATA / "datasets/ktvic/test_data.json")
    ov = json.loads(a.openviic_refs.read_text(encoding="utf-8"))["test"]
    res = {"label": LABEL.format("c"), "inputs_sha256": {"ktvic_test_data": sha256(DATA / "datasets/ktvic/test_data.json"),
                                                         "openviic_refs": sha256(a.openviic_refs)},
           "tokens": "syllables: NFC, rescap.chair.norm_tone, lower-cased, non-word characters removed",
           "measure": "Jaccard index of the two captions' n-gram sets; mean over pairs per image, then over images",
           **panel_overlap(kt, ov)}
    print(json.dumps(res, indent=1))
    return res


# ---------------------------------------------------------------- (d) the published baselines
THESIS = {"repository": "https://github.com/pacman-ctm/thesis-code", "commit": "1a8d1052d25ac92fbf886546e056ddd94141d2f0",
          "files": {"ktvic_resnetlstm": ("simple_evaluate/result_resnetlstm.json", "ad64a1156e9b203bba9c90eb3c27198e90aeee7c"),
                    "ktvic_vittrans": ("simple_evaluate/result_vittrans.json", "75f90f089e2fb18777f22c7b1609ba9efa2e0df2")},
          "terms": "no licence file (GitHub API license null); used with the permission of the repository's author "
                   "(personal communication, 2026-10-21); aggregate statistics only; outputs not redistributed"}


def published_counts(caps: list[str]) -> dict:
    toks = [w for c in caps for w in c.split()]
    punct = Counter(ch for c in caps for ch in c if unicodedata.category(ch).startswith("P") and ch != "_")
    return {"captions": len(caps), "whitespace_tokens": len(toks),
            "underscore_joined_tokens": sum("_" in w for w in toks),
            "captions_with_underscore": sum("_" in c for c in caps),
            "punctuation_characters_by_symbol": dict(sorted(punct.items())),
            "punctuation_only_tokens": sum(PT.is_punct_tok(w) for w in toks),
            "end_period_captions": sum(c.rstrip().endswith(".") for c in caps),
            "end_any_punctuation_captions": sum(bool(c.rstrip()) and PT.is_punct_tok(c.rstrip()[-1]) for c in caps)}


def baseline_audit(preds: dict[str, dict[str, str]], refs_raw: dict[str, list[str]]) -> dict:
    ids = sorted(refs_raw)
    names = list(preds)
    flat = [r for i in ids for r in refs_raw[i]] + [preds[s][i].replace("_", " ") for s in names for i in ids]
    it = iter(x.lower() for x in E4.rdr(flat))
    refs = {i: [next(it) for _ in refs_raw[i]] for i in ids}
    hyps = {s: {i: next(it) for i in ids} for s in names}
    out = {}
    for s in names:
        seg = [hyps[s][i] for i in ids]
        row = {"as_published": published_counts([preds[s][i] for i in ids]),
               "after_underscore_to_space_then_rdr": {
                   **PT.token_counts(seg), "end_period_captions": sum(t.split()[-1:] == ["."] for t in seg),
                   "captions_resegmented_as_published": sum(t == " ".join(preds[s][i].lower().split())
                                                            for t, i in zip(seg, ids))}}
        row["cider_d_x100_k5"] = {proto: round(float(E4.Cider({i: [f(r) for r in refs[i]] for i in ids})
                                                       .per_image({i: f(hyps[s][i]) for i in ids}).mean()), 4)
                                  for proto, f in (("P0", lambda x: x), ("PTB", PT.ptb))}
        out[s] = row
    return out


def cmd_baselines(a) -> dict:
    prov = {**{k: v for k, v in THESIS.items() if k != "files"}, "accessed_utc": a.accessed, "files": {}}
    preds = {}
    for name, path in (("ktvic_resnetlstm", a.resnetlstm), ("ktvic_vittrans", a.vittrans)):
        rel, blob = THESIS["files"][name]
        got = git_blob(path)
        prov["files"][name] = {"path": rel, "git_blob_sha1": got, "expected_blob": blob, "sha256": sha256(path)}
        if got != blob:
            raise SystemExit(f"{name}: blob {got} != {blob}: STOP, back to the judge (CC-092 R1)")
        rows = json.loads(path.read_text(encoding="utf-8"))
        preds[name] = {str(r["image_id"]): r["caption"] for r in rows}
    refs = PT.load_refs(DATA / "datasets/ktvic/test_data.json")
    assert all(set(p) == set(refs) for p in preds.values()), "image ids differ from KTVIC test"
    res = {"label": LABEL.format("d"), "provenance": prov,
           "references": "KTVIC test references from our own copy (sha256 below), not the thesis repo's test_data.json",
           "inputs_sha256": {"ktvic_test_data": sha256(DATA / "datasets/ktvic/test_data.json")},
           "segmentation_rule": "as published (underscore-joined), then '_' -> ' ' and RDRSegmenter (E4's rule); "
                                "RDR is never applied to the underscored text (CC-092 R5)",
           "ptb_punctuations": PT.PTB_PUNCTUATIONS,
           "p4_ktvic_t3_row": "not recomputed; see E4 pilot_results.json protocols.P4_T3bug_rdr_hyp_vs_raw_refs",
           "systems": baseline_audit(preds, refs)}
    print(json.dumps(res, indent=1, ensure_ascii=False))
    return res


# ---------------------------------------------------------------- selftest and CLI
def selftest() -> None:
    rng = random.Random(1)
    rows = [{0, 1}, {2}, {3, 4}, {1, 2, 3}, {0}]
    sizes, cols = [len(r) for r in rows], Counter(c for r in rows for c in r)
    curveball(rows, rng, 500)
    assert [len(r) for r in rows] == sizes and Counter(c for r in rows for c in r) == cols  # margins kept
    chain = [[{"a"}, {"a"}, {"b"}, {"b"}, {"c"}]] * 40
    assert stats([to_rows(s) for s in chain])[0] == 1.0 == EX.audit_k5("chain", chain)["adjacent_share"]
    r = slot_null([[{"a", "x"}, {"a"}, {"b"}, {"b", "x"}, {"c"}]] * 30, draws=50, seed=0)
    assert r["adjacent_share"]["observed"] == round(2 / 3, 4) and 0 < r["adjacent_share"]["null_mean"] < 2 / 3, r
    kt = {"1": ["aa bb cc dd ee ff gg hh"] * 5, "2": ["pp qq rr ss tt uu vv ww"] * 5}  # synthetic tokens only
    ov = {"1": ["bb cc dd zz yy", "aa xx"], "2": ["qq rr ss", "pp xx tt"]}
    p = panel_overlap(kt, ov)
    m = p["mean_pairwise_jaccard"]["n=1"]
    assert m["within_ktvic"]["est"] == 1.0 and m["cross_same_image"]["est"] > m["cross_mismatched_image"]["est"], p
    assert p["ktvic_refs_identical_to_an_openviic_caption"] == 0
    c = published_counts(["aa bb_cc .", "dd ee_ff_gg, hh"])
    assert (c["underscore_joined_tokens"], c["end_period_captions"], c["punctuation_characters_by_symbol"]) == (2, 1, {",": 1, ".": 1})
    with tempfile.NamedTemporaryFile() as f:
        assert git_blob(Path(f.name)) == "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"  # git's empty blob
    a = np.array([0b1011], np.uint64)
    kt_f = {"phash": a, "dhash": a, "phash_m": a, "dhash_m": a, "sscd": np.array([[1.0, 0.0]], np.float32)}
    ov_f = {"phash": np.array([0b1011, 0], np.uint64), "dhash": np.array([0b1011, 0], np.uint64),
            "sscd": np.array([[0.9, 0.1], [0.0, 1.0]], np.float32)}
    o = overlap_counts(kt_f, ov_f, np.array(["dev", "train"]))
    assert o["grid"]["hamming_le_10_sscd_ge_080"] == {"any_split": 1, "train": 0, "dev_copy": 1, "test_copy": 0}, o
    print("selftest ok")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("slotnull")
    s.add_argument("--draws", type=int, default=1000)
    s.add_argument("--seed", type=int, default=SEED)
    o = sub.add_parser("overlap")
    o.add_argument("--cache", type=Path, required=True, help="build_memory.py --cache folder (feat_*.npz)")
    o.add_argument("--sscd", type=Path, required=True, help="sscd_disc_mixup.torchscript.pt (its sha256 keys the cache)")
    p = sub.add_parser("panels")
    p.add_argument("--openviic-refs", type=Path, required=True, help="scripts/match_openviic.py match output")
    b = sub.add_parser("baselines")
    b.add_argument("--resnetlstm", type=Path, required=True)
    b.add_argument("--vittrans", type=Path, required=True)
    b.add_argument("--accessed", required=True, help="UTC time the two files were fetched")
    for q in (s, o, p, b):
        q.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.cmd:
        ap.error("a subcommand or --selftest is required")
    res = {"slotnull": cmd_slotnull, "overlap": cmd_overlap, "panels": cmd_panels, "baselines": cmd_baselines}[a.cmd](a)
    res["script_sha256"] = sha256(Path(__file__))
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
