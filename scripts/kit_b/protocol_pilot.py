#!/usr/bin/env python
"""E4 CPU pilot: re-score committed KTVIC short-caption outputs under Vietnamese protocol variants.

Scorers re-implement pycocoevalcap Bleu(4) ('closest'), Rouge (beta 1.2) and Cider (CIDEr-D, n=4, sigma=6,
df over the scored refs, x10) line for line; --check asserts they reproduce committed numbers.
RDRSegmenter = VnCoreNLP-1.2 CLI fed through pipes (OpenViIC text never touches disk). Writes scores only.

Paper B, Sections 3.4 and 4.2 (segmentation and scorer sensitivity).
    NCS_DATA=/path/to/ncs-data python scripts/kit_b/protocol_pilot.py --out pilot_results.json [--systems A B ...]
    NCS_DATA=/path/to/ncs-data python scripts/kit_b/protocol_pilot.py --check   # the authors' p1-gold-short outputs only
Needs $NCS_DATA/datasets/ktvic/, $NCS_DATA/vncorenlp/VnCoreNLP-1.2.jar (with its models/; obtained by the reader),
system outputs as $NCS_DATA/results/<system>-short.preds.json ({image_id: caption}), and pyvi for protocol P3.
Optional, used only if present: $NCS_DATA/ktvic_openviic_refs.json (OpenViIC captions of KTVIC test images, built
by the reader with scripts/match_openviic.py; protocol P12) and $NCS_DATA/legacy/ (published KTVIC baselines' outputs).
Copied from the authors' protocol_pilot.py (sha256 387194159c466754f17cde53c502e40bf072159c4851ccbadbddc865a3621936);
changes: data paths read from $NCS_DATA, the output path is an argument, and the optional inputs are skipped if absent.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import kendalltau

CODE = Path(__file__).resolve().parents[2]
DATA = Path(os.environ.get("NCS_DATA", Path.home() / "ncs-data"))
VNC = DATA / "vncorenlp"
LEGACY = DATA / "legacy"
RES = DATA / "results"
sys.path.insert(0, str(CODE))
from rescap.chair import norm_tone  # noqa: E402

SYSTEMS = ("p1assist_s42 p1assist_s43 p1assist_s44 p1-gold p1_s43 p1_s44 p1mask_s42 mr5assist_s42 fuse2_s42 "
           "fuse2_s43 fuse2_s44 tags_fuse2_s42 tags_p1_s43 e5_s42 e5dpo_s42 p1_s43mbr fuse2_s42mbr zeroshot "
           "tags_zeroshot vcd main_s42 vsps official p2-noverif4090").split()
MARK = "XQZSEPQX"
PUNCT = re.compile(r"([^\w\s])")


def rdr(texts: list[str]) -> list[str]:
    """VnCoreNLP-1.2 RDRSegmenter over pipes; one marker line between texts keeps the alignment."""
    inp = f"\n{MARK}\n".join(" ".join(t.split()) for t in texts) + "\n"
    out = subprocess.run(["nice", "-n", "19", "java", "-Xmx700m", "-XX:+UseSerialGC", "-XX:ActiveProcessorCount=1",
                          "-jar", "VnCoreNLP-1.2.jar", "-fin", "/dev/stdin", "-fout", "/dev/stdout",
                          "-annotators", "wseg"], input=inp, capture_output=True, text=True, cwd=VNC, check=True).stdout
    segs, cur = [], []
    for line in out.splitlines():
        cols = line.split("\t")
        if len(cols) > 2 and cols[0].isdigit():
            if cols[1] == MARK:
                segs.append(" ".join(cur))
                cur = []
            else:
                cur.append(cols[1])
    segs.append(" ".join(cur))
    if len(segs) != len(texts):
        raise RuntimeError(f"RDR alignment lost: {len(segs)} != {len(texts)}")
    return segs


def ngrams(s: str, n: int = 4) -> dict:
    w = s.split()
    c = defaultdict(int)
    for k in range(1, n + 1):
        for i in range(len(w) - k + 1):
            c[tuple(w[i:i + k])] += 1
    return c


class Cider:
    """pycocoevalcap CiderScorer (CIDEr-D). df_refs: refs used for document frequency (default: the scored refs)."""

    def __init__(self, refs: dict[str, list[str]], sigma: float = 6.0, df_refs: list[list[str]] | None = None):
        self.sigma = sigma
        self.ids = sorted(refs)
        df_src = df_refs if df_refs is not None else [refs[i] for i in self.ids]
        self.df = defaultdict(float)
        for rs in df_src:
            for g in {g for r in rs for g in ngrams(r)}:
                self.df[g] += 1
        self.ref_len = np.log(float(len(df_src)))
        self.rvec = {i: [self.vec(ngrams(r)) for r in refs[i]] for i in self.ids}

    def vec(self, cnts):
        v, norm, length = [defaultdict(float) for _ in range(4)], [0.0] * 4, 0
        for g, tf in cnts.items():
            n = len(g) - 1
            v[n][g] = float(tf) * (self.ref_len - np.log(max(1.0, self.df[g])))
            norm[n] += v[n][g] ** 2
            if n == 1:  # pycocoevalcap quirk: "length" counts bigrams
                length += tf
        return v, [np.sqrt(x) for x in norm], length

    def per_image(self, hyps: dict[str, str]) -> np.ndarray:
        out = []
        for i in self.ids:
            vh, nh, lh = self.vec(ngrams(hyps[i]))
            tot = np.zeros(4)
            for vr, nr, lr in self.rvec[i]:
                pen = 1.0 if math.isinf(self.sigma) else np.e ** (-(float(lh - lr) ** 2) / (2 * self.sigma ** 2))
                for n in range(4):
                    val = sum(min(c, vr[n][g]) * vr[n][g] for g, c in vh[n].items())
                    if nh[n] != 0 and nr[n] != 0:
                        val /= nh[n] * nr[n]
                    tot[n] += val * pen
            out.append(np.mean(tot) / len(self.rvec[i]) * 10.0)
        return np.array(out) * 100.0


def bleu4(refs: dict[str, list[str]], hyps: dict[str, str]) -> float:
    """pycocoevalcap Bleu(4).compute_score(option='closest'), corpus BLEU-4."""
    tiny, small = 1e-15, 1e-9
    guess, correct, tl, rl = [0] * 4, [0] * 4, 0, 0
    for i in refs:
        h = hyps[i].split()
        maxc = defaultdict(int)
        lens = []
        for r in refs[i]:
            lens.append(len(r.split()))
            for g, c in ngrams(r).items():
                maxc[g] = max(maxc[g], c)
        for g, c in ngrams(hyps[i]).items():
            correct[len(g) - 1] += min(maxc.get(g, 0), c)
        for k in range(4):
            guess[k] += max(0, len(h) - k)
        tl += len(h)
        rl += min((abs(x - len(h)), x) for x in lens)[1]
    b = 1.0
    for k in range(4):
        b *= (correct[k] + tiny) / (guess[k] + small)
    b = b ** 0.25
    ratio = (tl + tiny) / (rl + small)
    return 100 * (b * math.exp(1 - 1 / ratio) if ratio < 1 else b)


def rouge_l(refs: dict[str, list[str]], hyps: dict[str, str]) -> float:
    def lcs(a, b):
        prev = [0] * (len(b) + 1)
        for x in a:
            cur = [0]
            for j, y in enumerate(b):
                cur.append(prev[j] + 1 if x == y else max(prev[j + 1], cur[j]))
            prev = cur
        return prev[-1]

    scores = []
    for i in refs:
        c = hyps[i].split(" ")
        p, r = [], []
        for ref in refs[i]:
            t = ref.split(" ")
            m = lcs(t, c)
            p.append(m / len(c))
            r.append(m / len(t))
        pm, rm = max(p), max(r)
        scores.append(((1 + 1.44) * pm * rm) / (rm + 1.44 * pm) if pm and rm else 0.0)
    return 100 * float(np.mean(scores))


def load_systems(systems: list[str]) -> dict[str, dict[str, str]]:
    sysd = {}
    for s in systems:
        raw = json.loads((RES / f"{s}-short.preds.json").read_text(encoding="utf-8"))
        sysd[s] = {str(k): (v[0] if isinstance(v, list) else v) for k, v in raw.items()}
    for s, f in (("ktvic_resnetlstm", "resnetlstm"), ("ktvic_vittrans", "vittrans")):
        if not (LEGACY / f"thesis_simple_evaluate_result_{f}.json").exists():
            continue
        rows = json.loads((LEGACY / f"thesis_simple_evaluate_result_{f}.json").read_text(encoding="utf-8"))
        sysd[s] = {str(r["image_id"]): r["caption"].replace("_", " ") for r in rows}
    return sysd


def main(out_path: Path, systems: list[str]) -> int:
    test = json.loads((DATA / "datasets/ktvic/test_data.json").read_text(encoding="utf-8"))
    refs_raw, refs_seg = defaultdict(list), defaultdict(list)
    for a in test["annotations"]:
        refs_raw[str(a["image_id"])].append(a["caption"])
        refs_seg[str(a["image_id"])].append(a["segment_caption"])
    ids = sorted(refs_raw)
    train = json.loads((DATA / "datasets/ktvic/train_data.json").read_text(encoding="utf-8"))
    tr = defaultdict(list)
    for a in train["annotations"]:
        tr[a["image_id"]].append(a["segment_caption"].lower())
    ov_file = DATA / "ktvic_openviic_refs.json"
    ov = json.loads(ov_file.read_text(encoding="utf-8"))["test"] if ov_file.exists() else {}
    ov_ids = sorted(i for i in ov if i in refs_raw)
    sysd = load_systems(systems)
    names = list(sysd)

    # ---- one RDR pass over everything that needs it (texts held in memory only)
    jobs = []  # (key, text)
    for s in names:
        for i in ids:
            jobs.append((("h", s, i), sysd[s][i]))
            jobs.append((("ht", s, i), norm_tone(sysd[s][i])))
    for i in ids:
        for k, r in enumerate(refs_raw[i]):
            jobs.append((("r", i, k), r))
            jobs.append((("rt", i, k), norm_tone(r)))
    for i in ov_ids:
        for k, r in enumerate(ov[i]):
            jobs.append((("o", i, k), r))
    seg = dict(zip([k for k, _ in jobs], rdr([t for _, t in jobs])))
    del jobs
    ref_match = sum(seg[("r", i, k)] == refs_seg[i][k] for i in ids for k in range(len(refs_raw[i])))
    n_refs = sum(len(refs_raw[i]) for i in ids)
    tone_changed = {"refs_raw": sum(norm_tone(r) != r for i in ids for r in refs_raw[i]),
                    "preds_raw": {s: sum(norm_tone(sysd[s][i]) != sysd[s][i] for i in ids) for s in names},
                    "rdr_changes_under_tone_norm": sum(seg[("ht", s, i)] != seg[("h", s, i)] for s in names for i in ids)}

    from pyvi import ViTokenizer
    low = str.lower
    rm_p = lambda t: " ".join(w for w in t.split() if not PUNCT.fullmatch(w))  # noqa: E731
    syl_p = lambda t: " ".join(PUNCT.sub(r" \1 ", t).split()).lower()  # noqa: E731

    # ---- protocols: (refs dict, hyp fn(system, id) -> str, cider kwargs)
    R = {
        "rdr": {i: [low(seg[("r", i, k)]) for k in range(len(refs_raw[i]))] for i in ids},
        "rdr_case": {i: [seg[("r", i, k)] for k in range(len(refs_raw[i]))] for i in ids},
        "rdr_tone": {i: [low(seg[("rt", i, k)]) for k in range(len(refs_raw[i]))] for i in ids},
        "syl_raw": {i: [r.strip().lower() for r in refs_raw[i]] for i in ids},
        "syl_raw_tone": {i: [norm_tone(r.strip().lower()) for r in refs_raw[i]] for i in ids},
        "syl_punct": {i: [syl_p(r) for r in refs_raw[i]] for i in ids},
        "pyvi": {i: [low(ViTokenizer.tokenize(r)) for r in refs_raw[i]] for i in ids},
    }
    R["rdr_nopunct"] = {i: [rm_p(r) for r in R["rdr"][i]] for i in ids}
    H = {
        "rdr": lambda s, i: low(seg[("h", s, i)]),
        "rdr_case": lambda s, i: seg[("h", s, i)],
        "rdr_tone": lambda s, i: low(seg[("ht", s, i)]),
        "syl_raw": lambda s, i: sysd[s][i].strip().lower(),
        "syl_raw_tone": lambda s, i: norm_tone(sysd[s][i].strip().lower()),
        "syl_punct": lambda s, i: syl_p(sysd[s][i]),
        "pyvi": lambda s, i: low(ViTokenizer.tokenize(sysd[s][i])),
        "rdr_nopunct": lambda s, i: rm_p(low(seg[("h", s, i)])),
    }
    protocols = {  # name: (refs, hyp-key, cider kwargs)
        "P0_official_rdr": (R["rdr"], "rdr", {}),
        "P1_syllable_raw(evaluate.py --also-syllable)": (R["syl_raw"], "syl_raw", {}),
        "P2_syllable_punct_split": (R["syl_punct"], "syl_punct", {}),
        "P3_pyvi_word": (R["pyvi"], "pyvi", {}),
        "P4_T3bug_rdr_hyp_vs_raw_refs": (R["syl_raw"], "rdr", {}),
        "P5_rdr_case_sensitive": (R["rdr_case"], "rdr_case", {}),
        "P6_rdr_tone_norm": (R["rdr_tone"], "rdr_tone", {}),
        "P6b_syllable_raw_tone_norm": (R["syl_raw_tone"], "syl_raw_tone", {}),
        "P7_rdr_strip_punct": (R["rdr_nopunct"], "rdr_nopunct", {}),
        "P8_rdr_sigma_inf(no_LP)": (R["rdr"], "rdr", {"sigma": float("inf")}),
        "P9_rdr_train_IDF": (R["rdr"], "rdr", {"df_refs": list(tr.values())}),
    }
    hyps = {hk: {s: {i: H[hk](s, i) for i in ids} for s in names} for hk in H}

    res = {"n_images": len(ids), "systems": names, "rdr_ref_vs_segment_caption_match": [ref_match, n_refs],
           "tone_norm_changes": tone_changed, "protocols": {}}
    per_img = {}
    for p, (refs, hk, kw) in protocols.items():
        sc = Cider(refs, **kw)
        per_img[p] = np.array([sc.per_image(hyps[hk][s]) for s in names])
        row = {"CIDEr": dict(zip(names, per_img[p].mean(1).round(2).tolist()))}
        if not kw:
            row["BLEU-4"] = {s: round(bleu4(refs, hyps[hk][s]), 2) for s in names}
            row["ROUGE-L"] = {s: round(rouge_l(refs, hyps[hk][s]), 2) for s in names}
        res["protocols"][p] = row
        print(p, {s: row["CIDEr"][s] for s in names[:4]}, flush=True)

    # reference-set protocols on official RDR tokens: leave-one-out (4 refs) and single ref, mean over the 5 subsets
    for k_keep, tag in ((4, "P10_rdr_4refs_mean_LOO"), (1, "P11_rdr_1ref_mean")):
        mats = []
        for j in range(5):
            sub = {i: ([r for q, r in enumerate(R["rdr"][i]) if q != j] if k_keep == 4 else [R["rdr"][i][j]]) for i in ids}
            sc = Cider(sub)
            mats.append(np.array([sc.per_image(hyps["rdr"][s]) for s in names]))
        per_img[tag] = np.mean(mats, axis=0)
        res["protocols"][tag] = {"CIDEr": dict(zip(names, per_img[tag].mean(1).round(2).tolist()))}
    # independent panel: OpenViIC refs (all available, RDR) vs KTVIC refs on the same images
    if ov_ids:
        pos = [ids.index(i) for i in ov_ids]
        sc = Cider({i: [low(seg[("o", i, k)]) for k in range(len(ov[i]))] for i in ov_ids})
        hsub = {s: {i: hyps["rdr"][s][i] for i in ov_ids} for s in names}
        per_img["P12_rdr_OpenViIC_refs(555)"] = np.array([sc.per_image(hsub[s]) for s in names])
        sc = Cider({i: R["rdr"][i] for i in ov_ids})
        per_img["P12ref_rdr_KTVIC_refs_same555"] = np.array([sc.per_image(hsub[s]) for s in names])
        for tag in ("P12_rdr_OpenViIC_refs(555)", "P12ref_rdr_KTVIC_refs_same555"):
            res["protocols"][tag] = {"CIDEr": dict(zip(names, per_img[tag].mean(1).round(2).tolist()))}

    # ---- ranking analysis: Kendall tau-b vs P0 (all systems; fine-tuned cluster = P0 CIDEr >= 120)
    p0 = per_img["P0_official_rdr"].mean(1)
    ft = [n for n, v in enumerate(p0) if v >= 120]
    rng = np.random.default_rng(42)
    idx = rng.integers(0, len(ids), size=(2000, len(ids)))
    idx555 = rng.integers(0, len(ov_ids), size=(2000, len(ov_ids))) if ov_ids else None

    def boot_sig(mat, ix):
        m = np.stack([row[ix].mean(1) for row in mat])  # systems x B
        sig = {}
        for a in range(len(names)):
            for b in range(a + 1, len(names)):
                d = m[a] - m[b]
                lo, hi = np.percentile(d, [2.5, 97.5])
                sig[(a, b)] = 1 if lo > 0 else (-1 if hi < 0 else 0)
        return sig

    sig0 = boot_sig(per_img["P0_official_rdr"], idx)
    rank = {}
    for p, mat in per_img.items():
        v = mat.mean(1)
        base = per_img["P12ref_rdr_KTVIC_refs_same555"].mean(1) if p.startswith("P12_") else p0
        sig = boot_sig(mat, idx555 if p.startswith("P12") else idx)
        pairs = [(a, b) for a in range(len(names)) for b in range(a + 1, len(names))]
        ft_pairs = [(a, b) for a, b in pairs if a in ft and b in ft]
        flips = [(a, b) for a, b in ft_pairs if np.sign(v[a] - v[b]) != np.sign(base[a] - base[b])]
        sig_flips = [(a, b) for a, b in ft_pairs if sig0[(a, b)] != 0 and sig[(a, b)] == -sig0[(a, b)]]
        lost = [(a, b) for a, b in ft_pairs if sig0[(a, b)] != 0 and sig[(a, b)] == 0]
        gained = [(a, b) for a, b in ft_pairs if sig0[(a, b)] == 0 and sig[(a, b)] != 0]
        rank[p] = {"tau_all": round(kendalltau(base, v).statistic, 3),
                   "tau_finetuned": round(kendalltau(base[ft], v[ft]).statistic, 3),
                   "ft_pair_order_flips": len(flips), "ft_pairs": len(ft_pairs),
                   "ft_sig_pairs_under_P0": sum(1 for q in ft_pairs if sig0[q] != 0),
                   "ft_sig_reversed": len(sig_flips), "ft_sig_lost": len(lost), "ft_sig_gained": len(gained),
                   "flip_examples": [f"{names[a]} vs {names[b]}" for a, b in flips[:6]],
                   "range_ft_score": [round(float(v[ft].min()), 2), round(float(v[ft].max()), 2)]}
    res["ranking"] = rank
    res["finetuned_cluster"] = [names[n] for n in ft]
    out_path.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", out_path)
    return 0


def check() -> None:
    """Reproduce committed numbers: p1-gold-short word 149.79/45.55/64.24, syllable 165.43/48.05/64.25."""
    test = json.loads((DATA / "datasets/ktvic/test_data.json").read_text(encoding="utf-8"))
    refs_raw = defaultdict(list)
    for a in test["annotations"]:
        refs_raw[str(a["image_id"])].append(a["caption"])
    ids = sorted(refs_raw)
    hyp = {str(k): v for k, v in json.loads((RES / "p1-gold-short.preds.json").read_text(encoding="utf-8")).items()}
    flat = [hyp[i] for i in ids] + [r for i in ids for r in refs_raw[i]]
    s = rdr(flat)
    hw = {i: s[n].lower() for n, i in enumerate(ids)}
    it = iter(s[len(ids):])
    rw = {i: [next(it).lower() for _ in refs_raw[i]] for i in ids}
    got = (round(float(Cider(rw).per_image(hw).mean()), 2), round(bleu4(rw, hw), 2), round(rouge_l(rw, hw), 2))
    hs = {i: hyp[i].strip().lower() for i in ids}
    rs = {i: [r.strip().lower() for r in refs_raw[i]] for i in ids}
    got_s = (round(float(Cider(rs).per_image(hs).mean()), 2), round(bleu4(rs, hs), 2), round(rouge_l(rs, hs), 2))
    print("word", got, "syllable", got_s)
    assert got == (149.79, 45.55, 64.24) and got_s == (165.43, 48.05, 64.25), (got, got_s)
    print("check ok")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="reproduce the committed p1-gold-short scores")
    ap.add_argument("--out", type=Path, default=Path("pilot_results.json"))
    ap.add_argument("--systems", nargs="+", default=SYSTEMS, help="stems of $NCS_DATA/results/<stem>-short.preds.json")
    a = ap.parse_args()
    sys.exit(check() if a.check else main(a.out, a.systems))
