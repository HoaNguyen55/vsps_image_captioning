#!/usr/bin/env python
"""CPU half of CN-RLOO (scripts/train_rl.py): reward, copy statistic and RLOO advantage. Reports: rl_report.py.

    python scripts/rl_reward.py --self-check        # needs JAVA_HOME: the segmenter worker is checked too

Reward: word-level CIDEr-D tokenised as evaluate.py does (RDRSegmenter, lowercase) with pycocoevalcap's arithmetic
(n=4, sigma 6, clipping, x10), but with document frequencies fixed from every reference set of the split (pycocoevalcap
recomputes them from whatever it scores) and an end token on each reference and on each FINISHED rollout (SacreEOS,
arXiv 2305.12254). Without it, dropping the last word raises CIDEr-D on ~30% of KTVIC images (B1 pilot, sec. 2.7);
a rollout cut off by max_new_tokens gets no end token.

Copy statistic m(c): the max over the image's references of the word-level similarity 1 - edit/max(len) and of
single-reference BLEU-4, on segmented words without punctuation. A rollout with m(c) >= tau is a regurgitated
reference: its advantage is 0 and it is left out of the leave-one-out baseline. tau is the 99th percentile of m over
k rollouts on the dev images, which the SFT policy never trained on (rl_report.py --g0 writes it). ">=", not ">":
exact copies occur on unseen images too (~0.9% of test samples, B1 sec. 2.8), so tau can be exactly 1.0, and ">"
would then mask nothing.
"""
from __future__ import annotations

import math
import multiprocessing as mp
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

SPLIT = "train_data.json"
EOS = "<eos>"
#: Syllables a complete Vietnamese caption does not end on (B1 pilot): a fragment cut before its head noun.
FUNCTION_END = {"của", "và", "với", "ở", "trên", "trong", "một", "các", "những", "có", "đang", "là", "cho", "tại",
                "bên"}


def _serve(conn) -> None:
    """Worker loop: segment each list of texts exactly as evaluate.py does (RDRSegmenter, then lowercase)."""
    from rescap.metrics import _rdrsegmenter

    segment = _rdrsegmenter()[0]
    while True:
        try:
            texts = conn.recv()
        except EOFError:  # the parent exited and closed its end: this is the shutdown signal
            return
        conn.send([segment(t.strip()).lower() if t.strip() else "" for t in texts])


class Segmenter:
    """RDRSegmenter in a spawned worker process, with a cache. It runs on a JVM through jnius, and a JVM started in a
    process that has initialised CUDA deadlocks (evaluate.py's docstring); spawn, not fork, keeps the worker CUDA-free."""

    def __init__(self) -> None:
        ctx = mp.get_context("spawn")
        self.conn, child = ctx.Pipe()
        self.proc = ctx.Process(target=_serve, args=(child,), daemon=True)
        self.proc.start()
        self.cache: dict[str, str] = {}

    def __call__(self, texts: list[str]) -> list[str]:
        todo = sorted(set(texts) - self.cache.keys())
        if todo:
            self.conn.send(todo)
            self.cache.update(zip(todo, self.conn.recv()))
        return [self.cache[t] for t in texts]


def ngrams(words: list[str], n: int = 4) -> Counter:
    """1..n-gram counts, in pycocoevalcap's precook order."""
    return Counter(tuple(words[i:i + k]) for k in range(1, n + 1) for i in range(len(words) - k + 1))


class CiderD:
    """pycocoevalcap's CIDEr-D with document frequencies fixed from `corpus` (one list of reference token lists per
    image). Scored on the corpus it was built from, it equals pycocoevalcap's per-image scores (checked in _check)."""

    def __init__(self, corpus: list[list[list[str]]], sigma: float = 6.0, n: int = 4) -> None:
        self.n, self.sigma = n, sigma
        self.df: Counter = Counter()
        for refs in corpus:
            self.df.update({g for r in refs for g in ngrams(r, n)})
        self.ref_len = float(np.log(float(len(corpus))))

    def _vec(self, words: list[str]) -> tuple[list[dict], list[float], int]:
        vec, norm, length = [{} for _ in range(self.n)], [0.0] * self.n, 0
        for g, tf in ngrams(words, self.n).items():
            k = len(g) - 1
            vec[k][g] = v = float(tf) * (self.ref_len - float(np.log(max(1.0, self.df[g]))))
            norm[k] += v * v
            length += tf if k == 1 else 0  # pycocoevalcap counts bigrams here, and so must we
        return vec, [math.sqrt(x) for x in norm], length

    def score(self, cand: list[str], refs: list[list[str]]) -> float:
        vh, nh, lh = self._vec(cand)
        total = [0.0] * self.n
        for ref in refs:
            vr, nr, lr = self._vec(ref)
            penalty = math.e ** (-(float(lh - lr) ** 2) / (2 * self.sigma ** 2))
            for k in range(self.n):
                val = sum(min(v, vr[k].get(g, 0.0)) * vr[k].get(g, 0.0) for g, v in vh[k].items())
                if nh[k] != 0 and nr[k] != 0:
                    val /= nh[k] * nr[k]
                total[k] += val * penalty
        return sum(total) / self.n / len(refs) * 10.0


def content(tokens: list[str]) -> list[str]:
    """Segmented tokens without the punctuation ones (what the copy statistic compares)."""
    return [t for t in tokens if any(ch.isalnum() for ch in t)]


def lev(a: list[str], b: list[str]) -> int:
    """Word-level Levenshtein distance."""
    d = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        prev, d[0] = d[0], i
        for j, y in enumerate(b, 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (x != y))
    return d[-1]


def bleu4(c: list[str], r: list[str]) -> float:
    """Sentence BLEU-4 of c against the single reference r, unsmoothed (0 when an n-gram order has no match)."""
    if not c:
        return 0.0
    cc, rc, logp = ngrams(c), ngrams(r), 0.0
    for k in range(1, 5):
        hit = sum(min(v, rc[g]) for g, v in cc.items() if len(g) == k)
        if not hit:
            return 0.0
        logp += math.log(hit / sum(v for g, v in cc.items() if len(g) == k)) / 4
    return min(1.0, math.exp(1 - len(r) / len(c))) * math.exp(logp)


def copy_stat(c: list[str], refs: list[list[str]]) -> tuple[float, int]:
    """m(c) = max over references of max(1 - edit/max(len), single-reference BLEU-4), and the smallest edit distance."""
    dist = [lev(c, r) for r in refs]
    m = max(max(1.0 - d / max(len(c), len(r), 1), bleu4(c, r)) for d, r in zip(dist, refs))
    return m, min(dist)


def rloo(rewards, copy) -> np.ndarray:
    """r_i - mean(r_j, j != i) over the non-copies, no std normalisation (Dr. GRPO, arXiv 2503.20783); copies get 0
    and sit in nobody's baseline. A group with fewer than two non-copies has no baseline: all zero."""
    r, keep = np.asarray(rewards, float), ~np.asarray(copy, bool)
    adv, n = np.zeros_like(r), int(keep.sum())
    if n > 1:
        adv[keep] = r[keep] - (r[keep].sum() - r[keep]) / (n - 1)
    return adv


def syllables(text: str) -> list[str]:
    return re.sub(r"[.,;:!?]", " ", text.lower()).split()


def function_end(text: str) -> bool:
    s = syllables(text)
    return bool(s) and s[-1] in FUNCTION_END


def boot(x, seed: int = 0, b: int = 2000) -> list[float]:
    """Mean and 95% percentile bootstrap interval over images (paired when x is a per-image difference)."""
    x = np.asarray(x, float)
    m = x[np.random.default_rng(seed).integers(0, len(x), (b, len(x)))].mean(1)
    return [float(x.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))]


class Reward:
    """EOS-aware word-level CIDEr-D (df from every reference set in `refs`) and the copy statistic, per image."""

    def __init__(self, refs: dict[str, list[str]], seg, sigma: float = 6.0) -> None:
        self.seg = seg
        ids = sorted(refs)
        flat = iter(seg([r for i in ids for r in refs[i]]))
        self.refs = {i: [next(flat).split() for _ in refs[i]] for i in ids}
        self.eos_refs = {i: [r + [EOS] for r in rs] for i, rs in self.refs.items()}
        self.cider = CiderD(list(self.eos_refs.values()), sigma)

    def __call__(self, image_id: str, texts: list[str], finished) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """(reward, m, smallest word edit distance to a reference) per caption; finished[j]: caption j ended with
        the model's EOS token."""
        toks = [s.split() for s in self.seg(texts)]
        words = [content(r) for r in self.refs[image_id]]
        r = [self.cider.score(t + [EOS] * bool(f), self.eos_refs[image_id]) for t, f in zip(toks, finished)]
        m, dist = zip(*(copy_stat(content(t), words) for t in toks))
        return np.array(r), np.array(m), np.array(dist)


def replica_gap(reward: Reward, captions: dict) -> float:
    """Judge D1 C3 (ii): the reward's CIDEr-D with df from the whole split and no end token, against pycocoevalcap run
    on the whole split, per image, on these captions (largest absolute difference)."""
    from pycocoevalcap.cider.cider import Cider

    every = sorted(reward.refs)
    gts = {i: [" ".join(r) for r in reward.refs[i]] for i in every}
    seg = dict(zip(captions, reward.seg(list(captions.values()))))
    per = dict(zip(every, Cider().compute_score(gts, {i: [seg.get(i, gts[i][0])] for i in every})[1]))
    replica = CiderD(list(reward.refs.values()))
    return max(abs(replica.score(seg[i].split(), reward.refs[i]) - per[i]) for i in captions)


def _check() -> None:
    from pycocoevalcap.cider.cider import Cider

    refs = {"1": ["con chó chạy trên bãi cỏ xanh", "một con chó đang chạy trên cỏ", "con chó nhỏ chạy trên bãi cỏ"],
            "2": ["hai người đi xe máy trên đường", "có hai người đang đi xe máy", "người đàn ông chở bạn trên xe"],
            "3": ["một chiếc thuyền trên sông", "chiếc thuyền nhỏ trên dòng sông", "thuyền đang di chuyển trên sông"]}
    cands = {"1": "con chó chạy trên cỏ", "2": "hai người đi xe máy", "3": "một chiếc xe trên đường"}
    _, per = Cider().compute_score(refs, {i: [c] for i, c in cands.items()})
    mine = CiderD([[r.split() for r in refs[i]] for i in refs])
    for n, i in enumerate(refs):
        assert abs(mine.score(cands[i].split(), [r.split() for r in refs[i]]) - per[n]) < 1e-9, (i, per[n])
    # EOS: a rollout cut by max_new_tokens earns no end-token credit, and the end token widens the margin by which a
    # complete caption beats its truncation (the loophole the plain reward leaves open)
    R = Reward(refs, seg=lambda texts: [t.lower() for t in texts])
    full, cut = "con chó chạy trên bãi cỏ", "con chó chạy trên bãi"
    r_fin, r_unf = R("1", [full, full], [True, False])[0]
    assert r_fin > r_unf, (r_fin, r_unf)
    eos_gap = float(np.subtract(*R("1", [full, cut], [True, True])[0]))
    plain = CiderD([[r.split() for r in rs] for rs in refs.values()])
    plain_gap = plain.score(full.split(), R.refs["1"]) - plain.score(cut.split(), R.refs["1"])
    assert eos_gap > plain_gap, (eos_gap, plain_gap)
    assert replica_gap(R, {"1": full, "3": "một chiếc xe trên đường"}) < 1e-12
    # copy statistic
    ref = ["con_chó", "chạy", "trên", "bãi_cỏ", "xanh"]
    assert copy_stat(content("con_chó chạy trên bãi_cỏ xanh .".split()), [ref]) == (1.0, 0)
    assert lev(["con_chó", "nhảy", "trên", "bãi_cỏ", "xanh"], ref) == 1 and lev([], ref) == 5
    assert copy_stat(["con_chó", "nhảy", "trên", "bãi_cỏ", "xanh"], [ref])[0] == 0.8
    assert bleu4(ref, ref) == 1.0 and bleu4(ref[:3], ref) == 0.0 and bleu4([], ref) == 0.0
    assert abs(bleu4(ref + ["đẹp"], ref) - math.exp(sum(math.log(x) for x in (5 / 6, 4 / 5, 3 / 4, 2 / 3)) / 4)) < 1e-12
    assert copy_stat(["hai", "chiếc", "thuyền"], [ref]) == (0.0, 5) and copy_stat([], [ref]) == (0.0, 5)
    _, m, dist = R("1", ["Con chó chạy trên bãi cỏ xanh", "con chó chạy"], [True, True])
    assert m[0] == 1.0 and dist.tolist() == [0, 4] and abs(m[1] - 3 / 7) < 1e-12
    # RLOO with masked copies
    assert np.allclose(rloo([1, 2, 3, 4], [0, 0, 1, 0]), [-2, -0.5, 0, 2.5])
    assert np.allclose(rloo([1, 2, 3, 4], [0, 0, 0, 0]), [1 - 3, 2 - 8 / 3, 3 - 7 / 3, 4 - 2])
    assert np.allclose(rloo([5, 1, 1], [0, 1, 1]), 0) and np.allclose(rloo([5, 1], [1, 1]), 0)
    assert abs(rloo([0.3, 1.7, 2.2, 0.1, 4.0], [0, 1, 0, 0, 0]).sum()) < 1e-12
    assert function_end("một con chó đang.") and not function_end("một con chó") and not function_end("")
    assert boot(np.ones(7)) == [1.0, 1.0, 1.0]
    _check_segmenter()
    print("rl_reward self-check ok")


def _check_segmenter() -> None:
    """The worker reproduces KTVIC's own `segment_caption` (what evaluate.py relies on) and caches."""
    import json

    from evaluate import KTVIC

    anns = json.loads((KTVIC / SPLIT).read_text(encoding="utf-8"))["annotations"][:40]
    seg = Segmenter()
    caps = [a["caption"] for a in anns]
    assert seg(caps) == [a["segment_caption"].lower() for a in anns]
    assert seg(caps[:1] + [""]) == [anns[0]["segment_caption"].lower(), ""] and len(seg.cache) == len(set(caps)) + 1


if __name__ == "__main__":
    if sys.argv[1:] != ["--self-check"]:
        sys.exit(__doc__)
    _check()
