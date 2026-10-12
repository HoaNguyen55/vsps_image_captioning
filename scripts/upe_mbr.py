#!/usr/bin/env python
"""UPE-MBR (Unseen-Panel Expected-object-F1 MBR), a decode-time rule, and its pre-registered scoring (judge D9).

Pre-registration: manuscript/prereg/2026-10-13_upe_mbr.md (frozen constants, the T* rule, predictions F1-F3, kills).

Rule, per image, over one adapter's pool [greedy, s_1, .., s_6]; it reads no reference of the image it captions:
  U(c)   = mean_{j != c} CIDEr-D(c, pool_j) + CIDEr-D(c, refs of the RETRIEVE train images whose 1-2-gram TF-IDF is
           closest to the greedy caption) + LAM * 10 * EF1(c)
  EF1(c) = 2 * sum_{o in M(c)} q_o / (|M(c)| + EG),  q_o = 1 - (1 - v_o)^M,  v_o = share of the OTHER pool captions
           naming class o (expected object F1 against an unseen panel of about M describers naming EG classes)
  The greedy caption is kept unless max U - U(greedy) > MARGIN.
CIDEr-D is rl_reward.CiderD (word level, RDRSegmenter + lowercase) with document frequencies from the selection
references: KTVIC train minus dev300 on dev, all KTVIC train on test, UIT-ViIC train on UIT-ViIC. Classes are those of
each dataset's object metric: rescap.chair.objects_in (KTVIC, 113-entry lexicon), score_coco_probe.vi_objects
(UIT-ViIC, COCO-80, matcher v2). Controls on the same pool, base and margin: COUNT (q_o = 1, no evidence; lam on the
0..3 grid matched to UPE's classes per caption) and LEX (K2's lexicon object F1 against the other pool captions,
lam = LAM_LEX, matched to UPE's dev KTVIC cost in T3 p12). Paired over images, B - A: CIDEr-D with rl_reward.boot,
objects with object_prf.paired, CHAIR_i with rescap.chair; pooled = rows of all seeds or splits concatenated.

    python scripts/upe_mbr.py choose-t --greedy DEV.preds.json --samples 0.5=S05.jsonl 0.8=S08.jsonl --out R.json \\
        --t-file upe_temperature.txt
    python scripts/upe_mbr.py ktvic --system s42 G42.preds.json S42.jsonl [--system ...] --out R.json
    NCS_DATASET=uitviic python scripts/upe_mbr.py uitviic --split test G.preds.json S.jsonl --split val ... --out R.json
    python scripts/upe_mbr.py --self-check

Writes numbers, image counts and file hashes only: never a reference, panel or generated caption.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from object_prf import image_counts, paired  # noqa: E402
from rl_reward import CiderD, boot  # noqa: E402

LAM, M, MARGIN, EG, RETRIEVE, K_SAMPLES = 2.0, 5, 0.5, 6.0, 10, 6  # frozen (pre-registration)
LAM_LEX = 0.7
COUNT_GRID = [round(0.05 * i, 2) for i in range(61)]
KTVIC_COST = -3.0  # the T* rule's bound on the dev change in KTVIC CIDEr-D (x100)
DEV = ROOT / "data" / "splits" / "ktvic_dev300.txt"
PANEL = ROOT / "data" / "ktvic_openviic_refs.json"
EXACT = lambda c: {c}  # noqa: E731  (object_prf's flat class space: no hypernym credit)


# ----------------------------------------------------------------------------------------------- the rule
def tfidf_knn(docs: dict[str, list[list[str]]]):
    """k nearest train images by cosine of 1-2-gram TF-IDF over their pooled references (B4's caption retrieval)."""
    def bag(t):
        return Counter(t) + Counter(zip(t, t[1:]))
    doc = {j: sum((bag(r) for r in rs), Counter()) for j, rs in docs.items()}
    df = Counter(g for d in doc.values() for g in d)
    idf, unk = {g: math.log((len(doc) + 1) / (c + 1)) for g, c in df.items()}, math.log(len(doc) + 1)

    def vec(b):
        v = {g: tf * idf.get(g, unk) for g, tf in b.items()}
        nm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {g: x / nm for g, x in v.items()}
    post = defaultdict(list)
    for j, d in doc.items():
        for g, x in vec(d).items():
            post[g].append((j, x))

    def knn(tokens: list[str], k: int) -> list[str]:
        s = Counter()
        for g, x in vec(bag(tokens)).items():
            for j, y in post.get(g, ()):
                s[j] += x * y
        return [j for j, _ in sorted(s.items(), key=lambda t: (-t[1], t[0]))[:k]]
    return knn


def evidence_terms(classes: list[frozenset]) -> tuple[list[float], list[float]]:
    """(EF1, COUNT) of every pool caption: EF1 with q_o = 1 - (1 - v_o)^M, COUNT with q_o = 1."""
    ef, cnt = [], []
    for k, m in enumerate(classes):
        others = classes[:k] + classes[k + 1:]
        s = sum(1 - (1 - sum(o in x for x in others) / len(others)) ** M for o in m)
        ef.append(2 * s / (len(m) + EG))
        cnt.append(2 * len(m) / (len(m) + EG))
    return ef, cnt


def lex_term(cand: str, others: list[str]) -> float:
    """K2's lexicon object F1 (research_kg K2 sec. 3) with the other pool captions as pseudo-references."""
    from rescap.chair import _ancestors, _gold_objects, objects_in
    from rescap.svp.matching import canonical

    def cls(t):
        return {canonical(o) or o for o in objects_in(t)}
    c, base, gold = cls(cand), set().union(*(cls(r) for r in others)), _gold_objects(others)
    if not c or not base:
        return float(not c and not base)
    p = sum(o in gold for o in c) / len(c)
    r = sum(b in c or bool((_ancestors(b) - {b}) & c) for b in base) / len(base)
    return 0.0 if p + r == 0 else 2 * p * r / (p + r)


def utilities(pool_tok, pool_cls, train_tok, pool_raw=None) -> dict[str, np.ndarray]:
    """(N, K) arrays: base = self-MBR + retrieval CIDEr-D; E = EF1; C = COUNT; L = LEX (when pool_raw is given)."""
    cd, knn = CiderD(list(train_tok.values())), tfidf_knn(train_tok)
    N, K = len(pool_tok), len(pool_tok[0])
    out = {x: np.zeros((N, K)) for x in ("base", "E", "C", "L")}
    for n in range(N):
        toks = pool_tok[n]
        refs = [r for j in knn(toks[0], RETRIEVE) for r in train_tok[j]]
        for k in range(K):
            out["base"][n, k] = np.mean([cd.score(toks[k], [toks[j]]) for j in range(K) if j != k]) \
                + cd.score(toks[k], refs)
        out["E"][n], out["C"][n] = evidence_terms(pool_cls[n])
        if pool_raw is not None:
            out["L"][n] = [lex_term(pool_raw[n][k], pool_raw[n][:k] + pool_raw[n][k + 1:]) for k in range(K)]
    return out


def pick(base: np.ndarray, term: np.ndarray, lam: float) -> np.ndarray:
    """Pool index per image: argmax of base + lam * 10 * term, the greedy caption (0) unless it gains > MARGIN."""
    U = base + lam * 10 * term
    best = U.argmax(1)
    return np.where(U[np.arange(len(U)), best] - U[:, 0] > MARGIN, best, 0)


def count_matched(u: dict, pool_cls, target: np.ndarray) -> tuple[float, np.ndarray]:
    """COUNT control whose mean classes per caption is closest to `target`'s picks (ties: the smaller lam)."""
    n_cls = np.array([[len(c) for c in row] for row in pool_cls])
    goal = n_cls[np.arange(len(target)), target].mean()
    lam = min(COUNT_GRID, key=lambda x: abs(n_cls[np.arange(len(n_cls)), pick(u["base"], u["C"], x)].mean() - goal))
    return lam, pick(u["base"], u["C"], lam)


def t_star(summ: dict[str, tuple[float, float]]) -> str:
    """T* from {T: (dev panel object F1 change, dev KTVIC CIDEr-D change)} of UPE vs greedy: the highest F1 change among
    the T whose KTVIC change is >= KTVIC_COST (a tie within 0.05 goes to the higher KTVIC change, then the lower T);
    if no T is eligible, the T with the highest KTVIC change."""
    ok = {t: v for t, v in summ.items() if v[1] >= KTVIC_COST}
    if not ok:
        return max(summ, key=lambda t: (summ[t][1], -float(t)))
    top = max(v[0] for v in ok.values())
    return max((t for t, v in ok.items() if v[0] >= top - 0.05), key=lambda t: (ok[t][1], -float(t)))


# ----------------------------------------------------------------------------------------------- data and scores
def sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_pool(greedy: str, samples: str, ids: list[str]) -> list[list[str]]:
    """pool[n] = [greedy caption, K_SAMPLES samples] of ids[n]; exits unless every image has all of them."""
    g = {str(k): (v[0] if isinstance(v, list) else v) or "" for k, v in
         json.loads(Path(greedy).read_text(encoding="utf-8")).items()}
    lines = Path(samples).read_text(encoding="utf-8").splitlines()
    rows = {str(r["image_id"]): r["samples"] for r in map(json.loads, lines)}
    bad = [i for i in ids if i not in g or len(rows.get(i, [])) != K_SAMPLES]
    if bad:
        raise SystemExit(f"{samples}: {len(bad)} of {len(ids)} images lack the greedy caption or {K_SAMPLES} samples")
    return [[g[i]] + rows[i] for i in ids]


def segmenter():
    from rl_reward import Segmenter
    seg = Segmenter()
    return lambda texts: [s.split() for s in seg(list(texts))]


def tok_groups(tok, groups: dict[str, list[str]]) -> dict[str, list[list[str]]]:
    """Segment every group's texts in one call to the segmenter worker."""
    flat = iter(tok([t for k in groups for t in groups[k]]))
    return {k: [next(flat) for _ in groups[k]] for k in groups}


class Scorer:
    """Every pool caption's views: CIDEr-D x100 against `refs` (DF from them, as evaluate.py), object rows against
    each gold in `golds` ({name: [frozenset per image]}), and the pool's tokens and classes for the rule."""

    def __init__(self, pool, ids, refs, golds, tok, cls):
        N, K = len(pool), len(pool[0])
        flat = tok([c for row in pool for c in row])
        self.tok = [flat[n * K:(n + 1) * K] for n in range(N)]
        self.cls = [[cls(c) for c in row] for row in pool]
        rt = tok_groups(tok, {i: refs[i] for i in ids})
        cd = CiderD([rt[i] for i in ids])
        self.cider = np.array([[100 * cd.score(self.tok[n][k], rt[i]) for k in range(K)] for n, i in enumerate(ids)])
        self.rows = {g: [[image_counts(set(self.cls[n][k]), set(gold[n]), EXACT) for k in range(K)] for n in range(N)]
                     for g, gold in golds.items()}

    def picked(self, gold: str, pk: np.ndarray) -> list[tuple]:
        return [self.rows[gold][n][pk[n]] for n in range(len(pk))]


def obj(rows_a, rows_b) -> dict:
    return {k: [float(x) for x in v] for k, v in paired(rows_a, rows_b, n=5000).items()}


def chair_counts(captions: dict[str, str], refs: dict[str, list[str]]) -> np.ndarray:
    """(n_mentions, hallucinated) per caption against `refs` (CHAIR-vi), in the order of `captions`."""
    from rescap.chair import chair
    res = chair(captions, {i: refs[i] for i in captions}, strict_ids=False)
    by = {str(d["image_id"]): d for d in res.per_caption}
    return np.array([(by[i]["n_mentions"], len(by[i]["hallucinated"])) for i in captions], float)


def chair_delta(a: np.ndarray, b: np.ndarray) -> float:
    return float(100 * (b[:, 1].sum() / max(b[:, 0].sum(), 1) - a[:, 1].sum() / max(a[:, 0].sum(), 1)))


def compare(view_k: Scorer, view_p, pk_a, pk_b, golds_k=(), pos=None) -> dict:
    """B - A: the dataset's CIDEr-D and objects, and the panel's (view_p over the panel images at `pos`)."""
    a = np.arange(len(pk_a))
    out = {"cider": boot(view_k.cider[a, pk_b] - view_k.cider[a, pk_a]), "switched": float(np.mean(pk_b != pk_a))}
    for g in golds_k:
        out[f"obj_{g}"] = obj(view_k.picked(g, pk_a), view_k.picked(g, pk_b))
    if view_p is not None:
        b = np.arange(len(pos))
        out["panel_cider"] = boot(view_p.cider[b, pk_b[pos]] - view_p.cider[b, pk_a[pos]])
        out["panel_obj"] = obj(view_p.picked("panel", pk_a[pos]), view_p.picked("panel", pk_b[pos]))
    return out


# ----------------------------------------------------------------------------------------------- modes
def ktvic_views(pool, ids, refs, panel, tok):
    """(KTVIC view, panel view, panel positions) of one KTVIC pool."""
    from rescap.chair import objects_in

    def cls(t):
        return frozenset(objects_in(t))
    pos = np.array([n for n, i in enumerate(ids) if panel.get(i)])
    pids = [ids[n] for n in pos]
    vk = Scorer(pool, ids, refs, {"ktvic": [frozenset().union(*map(cls, refs[i])) for i in ids]}, tok, cls)
    vp = Scorer([pool[n] for n in pos], pids, panel, {"panel": [frozenset().union(*map(cls, panel[i])) for i in pids]},
                tok, cls)
    return vk, vp, pos


def choose_t(args) -> dict:
    """Step B: UPE vs greedy at each dev temperature, T* by t_star(), and R0 (plain KTVIC CIDEr-D selection reading the
    5 dev references, the F4 protocol) for the temperature reading."""
    from evaluate import references
    from ktvic_dev_split import DEV_MD5
    assert hashlib.md5(DEV.read_bytes()).hexdigest() == DEV_MD5, "dev300 file differs from the pinned md5"
    ids = sorted(DEV.read_text(encoding="utf-8").split())
    tr = references("train_data.json")
    train = {j: rs for j, rs in tr.items() if j not in set(ids)}
    assert len(ids) == 300 and len(train) == 3469, (len(ids), len(train))
    panel = json.loads(PANEL.read_text(encoding="utf-8"))["train"]
    tok = segmenter()
    train_tok = tok_groups(tok, train)
    res, summ = {"inputs": {"greedy": sha(args.greedy)}}, {}
    for spec in args.samples:
        T, path = spec.split("=", 1)
        res["inputs"][f"T{T}"] = sha(path)
        pool = load_pool(args.greedy, path, ids)
        vk, vp, pos = ktvic_views(pool, ids, {i: tr[i] for i in ids}, panel, tok)
        u = utilities(vk.tok, vk.cls, train_tok)
        g0, upe, r0 = np.zeros(len(ids), int), pick(u["base"], u["E"], LAM), vk.cider.argmax(1)
        caps = [{i: pool[n][p[n]] for n, i in enumerate(ids)} for p in (g0, upe)]
        res[f"T{T}"] = {"greedy_cider_x100": float(vk.cider[:, 0].mean()),
                        "upe_vs_greedy": compare(vk, vp, g0, upe, ("ktvic",), pos),
                        "r0_vs_greedy": compare(vk, vp, g0, r0, (), pos),
                        "chair_i_ktvic_delta": chair_delta(*(chair_counts(c, tr) for c in caps)),
                        "classes_per_caption": [float(np.mean([len(vk.cls[n][k]) for n, k in enumerate(p)]))
                                                for p in (g0, upe)]}
        d = res[f"T{T}"]["upe_vs_greedy"]
        summ[T] = (d["panel_obj"]["F1"][0], d["cider"][0])
    T = t_star(summ)
    res["t_star"] = {"T": T, "rule": "max dev panel object F1 change with dev KTVIC CIDEr-D change >= -3",
                     "summary": {t: list(v) for t, v in summ.items()}}
    r0 = res["T0.8"]["r0_vs_greedy"]["panel_cider"] if "T0.8" in res else None
    res["temperature_reading"] = None if r0 is None else {"r0_panel_cider_T0.8": r0,
                                                          "f4_temperature_dependent": bool(r0[1] > 0)}
    if args.t_file:
        Path(args.t_file).write_text(T + "\n", encoding="utf-8")
    return res


def ktvic(args) -> dict:
    """Step E: F1 and F3 on KTVIC test, per seed and pooled; the kill rules."""
    from evaluate import references
    te, tr = references("test_data.json"), references("train_data.json")
    ids = sorted(te)
    assert len(ids) == 558 and len(tr) == 3769, (len(ids), len(tr))
    panel = json.loads(PANEL.read_text(encoding="utf-8"))["test"]
    tok = segmenter()
    train_tok = tok_groups(tok, tr)
    res, rows, kills = {"inputs": {}}, defaultdict(list), 0
    for name, greedy, samples in args.system:
        res["inputs"][name] = {"greedy": sha(greedy), "samples": sha(samples)}
        pool = load_pool(greedy, samples, ids)
        vk, vp, pos = ktvic_views(pool, ids, te, panel, tok)
        u = utilities(vk.tok, vk.cls, train_tok, pool)
        g0, upe, lex = np.zeros(len(ids), int), pick(u["base"], u["E"], LAM), pick(u["base"], u["L"], LAM_LEX)
        lam_c, cnt = count_matched(u, vk.cls, upe)
        ch = [chair_counts({i: pool[n][p[n]] for n, i in enumerate(ids)}, te) for p in (g0, upe)]
        r = res[name] = {"vs_greedy": compare(vk, vp, g0, upe, ("ktvic",), pos),
                         "vs_count": compare(vk, vp, cnt, upe, (), pos), "vs_lex": compare(vk, vp, lex, upe, (), pos),
                         "count_lam": lam_c, "chair_i_ktvic_delta": chair_delta(*ch)}
        kills += r["vs_count"]["panel_obj"]["P"][1] <= 0 <= r["vs_count"]["panel_obj"]["P"][2]
        for key, p in (("g", g0), ("u", upe), ("l", lex)):
            rows[key] += vp.picked("panel", p[pos])
        rows["dk"] += list(vk.cider[np.arange(len(ids)), upe] - vk.cider[:, 0])
        rows["ch_g"].append(ch[0])
        rows["ch_u"].append(ch[1])
    pg, pl = obj(rows["g"], rows["u"]), obj(rows["l"], rows["u"])
    dk, dch = boot(rows["dk"]), chair_delta(np.vstack(rows["ch_g"]), np.vstack(rows["ch_u"]))
    res["pooled"] = {"panel_obj_vs_greedy": pg, "panel_obj_vs_lex": pl, "cider_vs_greedy": dk,
                     "chair_i_ktvic_delta": dch}
    res["verdict"] = {"F1a": pg["F1"][0] >= 2.5 and pg["F1"][1] > 0 and pg["P"][0] >= -1.5 and dk[0] >= -3.0,
                      "F1b": pl["F1"][0] >= 0.8 and pl["F1"][1] > 0,
                      "F3": dch >= -0.5,
                      "kill_panel_F1_ci_contains_0": pg["F1"][1] <= 0 <= pg["F1"][2],
                      "kill_count_control_equal_on_2_of_3_seeds": kills >= 2}
    return res


def uitviic(args) -> dict:
    """Step F: F2 on UIT-ViIC val + test against COCO instance labels; the kill rule."""
    import score_coco_probe as sc
    from evaluate import KTVIC, references
    assert KTVIC.name == "uitviic", "run with NCS_DATASET=uitviic"
    tr = references("train_data.json")
    inst = json.loads((ROOT / "data" / "uitviic" / "instance_gold.json").read_text(encoding="utf-8"))
    vt = sc.load_vi_terms()

    def cls(t):
        return frozenset(sc.vi_objects(t, vt))
    tok = segmenter()
    train_tok = tok_groups(tok, tr)
    res, rows = {"inputs": {}}, defaultdict(list)
    for split, greedy, samples in args.split:
        refs = references(f"{split}_data.json")
        ids = sorted(refs)
        res["inputs"][split] = {"greedy": sha(greedy), "samples": sha(samples), "images": len(ids)}
        pool = load_pool(greedy, samples, ids)
        v = Scorer(pool, ids, refs, {"inst": [frozenset(inst[i]["coco"]) for i in ids]}, tok, cls)
        u = utilities(v.tok, v.cls, train_tok)
        g0, upe = np.zeros(len(ids), int), pick(u["base"], u["E"], LAM)
        lam_c, cnt = count_matched(u, v.cls, upe)
        res[split] = {"vs_greedy": compare(v, None, g0, upe, ("inst",)),
                      "vs_count": compare(v, None, cnt, upe, ("inst",)), "count_lam": lam_c}
        for key, p in (("g", g0), ("u", upe), ("c", cnt)):
            rows[key] += v.picked("inst", p)
    pg, pc = obj(rows["g"], rows["u"]), obj(rows["c"], rows["u"])
    res["pooled"] = {"inst_vs_greedy": pg, "inst_vs_count": pc}
    res["verdict"] = {"F2": pg["R"][0] >= 2.0 and pg["R"][1] > 0 and pg["P"][0] >= -1.0 and pc["P"][0] >= 1.0,
                      "kill_instance_P_falls_more_than_1": pg["P"][0] < -1.0}
    return res


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--self-check", action="store_true")
    sub = ap.add_subparsers(dest="mode")
    c = sub.add_parser("choose-t", help="step B: T* on dev300 and the F4 temperature reading")
    c.add_argument("--greedy", required=True)
    c.add_argument("--samples", nargs="+", required=True, metavar="T=JSONL")
    c.add_argument("--out", required=True)
    c.add_argument("--t-file")
    k = sub.add_parser("ktvic", help="step E: F1 and F3 on KTVIC test (P1-assist seeds)")
    k.add_argument("--system", nargs=3, action="append", required=True, metavar=("NAME", "GREEDY", "SAMPLES"))
    k.add_argument("--out", required=True)
    u = sub.add_parser("uitviic", help="step F: F2 on UIT-ViIC val + test (NCS_DATASET=uitviic)")
    u.add_argument("--split", nargs=3, action="append", required=True, metavar=("SPLIT", "GREEDY", "SAMPLES"))
    u.add_argument("--out", required=True)
    return ap


def main() -> int:
    ap = build_parser()
    args = ap.parse_args()
    if args.self_check:
        _check()
        print("upe_mbr self-check ok")
        return 0
    if args.mode is None:
        ap.error("a mode (choose-t, ktvic, uitviic) or --self-check")
    res = {"choose-t": choose_t, "ktvic": ktvic, "uitviic": uitviic}[args.mode](args)
    res["frozen"] = {"LAM": LAM, "M": M, "MARGIN": MARGIN, "EG": EG, "RETRIEVE": RETRIEVE, "K_SAMPLES": K_SAMPLES,
                     "LAM_LEX": LAM_LEX, "script_sha256": sha(__file__)}
    text = json.dumps(res, indent=1, default=float)
    Path(args.out).write_text(text, encoding="utf-8")
    print(text)
    return 0


def _check() -> None:
    a, ab, b = frozenset({"a"}), frozenset({"a", "b"}), frozenset()
    ef, cnt = evidence_terms([a, ab, b])
    assert abs(ef[0] - 2 * (1 - 0.5 ** M) / (1 + EG)) < 1e-12 and ef[2] == 0.0 and abs(cnt[1] - 4 / (2 + EG)) < 1e-12
    assert abs(ef[1] - 2 * (1 - 0.5 ** M) / (2 + EG)) < 1e-12  # b is named by no other caption: q = 0
    base = np.array([[1.0, 1.4, 0.0], [1.0, 1.6, 0.0]])
    assert pick(base, np.zeros((2, 3)), LAM).tolist() == [0, 1]  # gain 0.4 <= MARGIN keeps greedy
    assert pick(base, np.array([[0, 0.01, 0], [0, 0, 0]]), LAM).tolist() == [1, 1]
    u = {"base": np.zeros((2, 2)), "C": np.array([[0.0, 0.5], [0.0, 0.5]])}
    lam, cnt_pick = count_matched(u, [[a, ab], [a, ab]], np.array([1, 1]))
    assert cnt_pick.tolist() == [1, 1] and lam == 0.15, lam  # 0.15 * 10 * 0.5 is the first gain > MARGIN
    assert t_star({"0.5": (3.0, -1.0), "0.8": (4.0, -2.0)}) == "0.8"
    assert t_star({"0.5": (3.0, -1.0), "0.8": (4.0, -3.5)}) == "0.5"
    assert t_star({"0.5": (3.98, 1.0), "0.8": (4.0, -2.0)}) == "0.5"  # tie within 0.05: higher KTVIC change
    assert t_star({"0.5": (3.0, -5.0), "0.8": (4.0, -4.0)}) == "0.8"  # none eligible: smaller cost
    assert tfidf_knn({"1": [["con", "chó"]], "2": [["con", "mèo", "trắng"]], "3": [["xe"]]})(["con", "mèo"], 1) == ["2"]
    tmp = Path(__import__("tempfile").mkdtemp())
    (tmp / "g.json").write_text(json.dumps({"1": "x", "2": ["y"]}), encoding="utf-8")
    (tmp / "s.jsonl").write_text(json.dumps({"image_id": "1", "samples": ["s"] * K_SAMPLES}) + "\n", encoding="utf-8")
    assert load_pool(str(tmp / "g.json"), str(tmp / "s.jsonl"), ["1"]) == [["x"] + ["s"] * K_SAMPLES]
    try:
        load_pool(str(tmp / "g.json"), str(tmp / "s.jsonl"), ["1", "2"])
    except SystemExit as e:
        assert "1 of 2 images lack" in str(e), e
    else:
        raise AssertionError("an image without samples must stop the run")
    tok = lambda texts: [t.split() for t in texts]  # noqa: E731
    assert tok_groups(tok, {"x": ["a b", "c"], "y": ["d"]}) == {"x": [["a", "b"], ["c"]], "y": [["d"]]}
    pool = [["con chó chạy", "con chó", "con mèo"], ["xe máy đỏ", "xe máy", "con mèo"]]
    refs = {"1": ["con chó chạy trên cỏ"], "2": ["xe máy đỏ trên đường"]}
    v = Scorer(pool, ["1", "2"], refs, {"g": [frozenset({"chó"}), frozenset()]}, tok,
               lambda t: frozenset(w for w in t.split() if w in {"chó", "mèo"}))
    assert v.cider.shape == (2, 3) and v.cider[0, 0] > v.cider[0, 2] > 0
    assert v.picked("g", np.array([2, 0]))[0][:2] == (0, 1) and v.picked("g", np.array([0, 0]))[0][:2] == (1, 1)


if __name__ == "__main__":
    sys.exit(main())
