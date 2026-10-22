#!/usr/bin/env python3
"""PTB-style punctuation removal as a scoring protocol row (Paper B, Sections 3.3-3.4; CC-088 B-1, POST_HOC).

pycocoevalcap's PTBTokenizer drops every token in its PUNCTUATIONS list before BLEU/ROUGE/CIDEr are computed.
Vietnamese pipelines replace that tokenizer with a word segmenter and so lose the removal. This script scores the
same outputs under two protocols, on candidates and references alike:
  P0   RDRSegmenter (VnCoreNLP-1.2) + lowercase: the protocol of the committed scores;
  PTB  P0, then every token in PTB_PUNCTUATIONS (pycocoevalcap 1.2, tokenizer/ptbtokenizer.py) removed.
KTVIC test: CIDEr-D x100 of the outputs as written, with trailing punctuation stripped, and with one "." appended
(the punctuation audit's three variants), k = 1..5 first references; BLEU-4 and ROUGE-L at k = 5; the paired image
bootstrap of the P1-R minus zero-shot gap. XM3600 test (the three short runs): CIDEr-D as is and with a period
appended where missing, and the fine-tuned minus zero-shot gaps. Writes scores and counts only.

    NCS_DATA=/path/to/ncs-data python scripts/kit_b/ptb_protocol.py --out ptb_protocol.json
    python scripts/kit_b/ptb_protocol.py --selftest        # no data needed
Needs $NCS_DATA/datasets/{ktvic,xm3600}/test_data.json, $NCS_DATA/vncorenlp/ and the outputs
$NCS_DATA/results/<system>.preds.json and $NCS_DATA/results/xm3600/<run>.preds.json. Scorer and segmenter come from
scripts/kit_b/protocol_pilot.py; it reads no other file.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import unicodedata
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import protocol_pilot as E4  # noqa: E402

DATA = Path(os.environ.get("NCS_DATA", Path.home() / "ncs-data"))
# verbatim from pycocoevalcap 1.2 (wheel sha256 083ed7910f1aec000b0a237ef6665f74edf19954204d0b1cbdb8399ed132228d),
# pycocoevalcap/tokenizer/ptbtokenizer.py
PTB_PUNCTUATIONS = ["''", "'", "``", "`", "-LRB-", "-RRB-", "-LCB-", "-RCB-",
                    ".", "?", "!", ",", ":", "-", "--", "...", ";"]
KTVIC_SYSTEMS = ["p1assist_s42-short", "p1ep4_s42-short", "fuse2_s42-short", "zeroshot-short"]
XM_RUNS = ["xm3600_zeroshot-short", "xm3600_p1_s43-short", "xm3600_fuse2_s42-short"]
B_BOOT, SEED = 2000, 42


def ptb(seg: str) -> str:
    return " ".join(w for w in seg.split() if w not in PTB_PUNCTUATIONS)


def is_punct_tok(tok: str) -> bool:
    return bool(tok) and all(unicodedata.category(ch).startswith("P") for ch in tok)


def strip_trailing(toks: list[str]) -> list[str]:
    out = list(toks)
    while out and is_punct_tok(out[-1]):
        out.pop()
    return out


def variants(seg: str) -> dict[str, str]:
    t = seg.split()
    s = strip_trailing(t)
    return {"as_written": " ".join(t), "strip": " ".join(s), "add_period": " ".join(s + ["."])}


def per_image(refs, hyps):
    return E4.Cider(refs).per_image(hyps)


def boot_diff(a: np.ndarray, b: np.ndarray) -> dict:
    rng = np.random.default_rng(SEED)
    idx = rng.integers(0, len(a), size=(B_BOOT, len(a)))
    d = (a[idx] - b[idx]).mean(1)
    return {"est": round(float((a - b).mean()), 4), "ci95": [round(float(np.percentile(d, 2.5)), 4),
                                                           round(float(np.percentile(d, 97.5)), 4)]}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_refs(path: Path) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for a in json.loads(path.read_text(encoding="utf-8"))["annotations"]:
        if a.get("caption") and a["caption"].strip():
            out.setdefault(str(a["image_id"]), []).append(a["caption"].strip())
    return out


def load_preds(path: Path) -> dict[str, str]:
    d = json.loads(path.read_text(encoding="utf-8"))
    return {str(k): ((v[0] if isinstance(v, list) else v) or "").strip() for k, v in d.items()}


def token_counts(texts: list[str]) -> dict:
    toks = [w for t in texts for w in t.split()]
    removed = sum(w in PTB_PUNCTUATIONS for w in toks)
    residual = sorted({w for w in toks if is_punct_tok(w) and w not in PTB_PUNCTUATIONS})
    return {"tokens": len(toks), "ptb_removed_tokens": removed, "residual_punct_token_types": len(residual),
            "residual_punct_tokens": sum(1 for w in toks if is_punct_tok(w) and w not in PTB_PUNCTUATIONS)}


def ktvic(inputs: dict) -> dict:
    p = DATA / "datasets/ktvic/test_data.json"
    inputs["ktvic_test_data"] = sha(p)
    refs_raw = load_refs(p)
    ids = sorted(refs_raw)
    preds = {}
    for s in KTVIC_SYSTEMS:
        f = DATA / "results" / f"{s}.preds.json"
        inputs[f.name] = sha(f)
        preds[s] = load_preds(f)
    flat = [r for i in ids for r in refs_raw[i]] + [preds[s][i] for s in KTVIC_SYSTEMS for i in ids]
    seg = [x.lower() for x in E4.rdr(flat)]
    it = iter(seg)
    refs = {i: [next(it) for _ in refs_raw[i]] for i in ids}
    hyps = {s: {i: next(it) for i in ids} for s in KTVIC_SYSTEMS}
    out = {"n_images": len(ids), "n_refs": sum(map(len, refs.values())),
           "token_counts": {"references": token_counts([r for i in ids for r in refs[i]]),
                            **{s: token_counts([hyps[s][i] for i in ids]) for s in KTVIC_SYSTEMS}},
           "systems": {}}
    per5 = {}
    for s in KTVIC_SYSTEMS:
        var = {i: variants(hyps[s][i]) for i in ids}
        row = {}
        for proto, f in (("P0", lambda x: x), ("PTB", ptb)):
            fk = {}
            for k in range(1, 6):
                rk = {i: [f(r) for r in refs[i][:k]] for i in ids}
                sc = E4.Cider(rk)
                fk[f"k={k}"] = {v: round(float(sc.per_image({i: f(var[i][v]) for i in ids}).mean()), 4)
                                for v in ("as_written", "strip", "add_period")}
                fk[f"k={k}"]["d_add_minus_strip"] = round(fk[f"k={k}"]["add_period"] - fk[f"k={k}"]["strip"], 4)
            r5 = {i: [f(r) for r in refs[i]] for i in ids}
            h5 = {i: f(var[i]["as_written"]) for i in ids}
            row[proto] = {"first_k": fk, "BLEU-4_as_written_k5": round(E4.bleu4(r5, h5), 4),
                          "ROUGE-L_as_written_k5": round(E4.rouge_l(r5, h5), 4)}
            per5[(s, proto)] = E4.Cider(r5).per_image(h5)
        out["systems"][s] = row
    out["gap_p1assist_s42_minus_zeroshot_as_written_k5"] = {
        proto: boot_diff(per5[("p1assist_s42-short", proto)], per5[("zeroshot-short", proto)]) for proto in ("P0", "PTB")}
    return out


def xm3600(inputs: dict) -> dict:
    p = DATA / "datasets/xm3600/test_data.json"
    inputs["xm3600_test_data"] = sha(p)
    refs_raw = load_refs(p)
    ids = sorted(refs_raw)
    preds = {}
    for r in XM_RUNS:
        f = DATA / "results/xm3600" / f"{r}.preds.json"
        inputs[f.name] = sha(f)
        preds[r] = load_preds(f)
    flat = [c for i in ids for c in refs_raw[i]] + [preds[r][i] for r in XM_RUNS for i in ids]
    seg = [x.lower() for x in E4.rdr(flat)]
    it = iter(seg)
    refs = {i: [next(it) for _ in refs_raw[i]] for i in ids}
    hyps = {r: {i: next(it) for i in ids} for r in XM_RUNS}
    out = {"n_images": len(ids), "runs": {}, "gaps_vs_zeroshot_as_is": {}}
    per = {}
    for proto, f in (("P0", lambda x: x), ("PTB", ptb)):
        sc = E4.Cider({i: [f(c) for c in refs[i]] for i in ids})
        for r in XM_RUNS:
            def app(t):
                toks = t.split()
                return " ".join(toks if toks and is_punct_tok(toks[-1]) else toks + ["."])
            a = sc.per_image({i: f(hyps[r][i]) for i in ids})
            b = sc.per_image({i: f(app(hyps[r][i])) for i in ids})
            per[(r, proto)] = a
            out["runs"].setdefault(r, {})[proto] = {"as_is": round(float(a.mean()), 4),
                                                    "append_period": round(float(b.mean()), 4),
                                                    "d_append_minus_as_is": round(float(b.mean() - a.mean()), 4)}
        for r in XM_RUNS[1:]:
            out["gaps_vs_zeroshot_as_is"].setdefault(r, {})[proto] = boot_diff(per[(r, proto)], per[(XM_RUNS[0], proto)])
    return out


def selftest() -> None:
    assert ptb("một con chó . , đang chạy -- ...") == "một con chó đang chạy"
    assert ptb("a ( b ) / c") == "a ( b ) / c"  # literal list only; "(" is "-LRB-" in PTB's own output
    assert variants("x y .") == {"as_written": "x y .", "strip": "x y", "add_period": "x y ."}
    refs = {"1": ["x y z w", "x y z v"], "2": ["p q r s", "p q r t"]}
    plain = {"1": "x y z w", "2": "p q r s"}
    dotted = {i: h + " ." for i, h in plain.items()}
    assert per_image(refs, dotted).mean() < per_image(refs, plain).mean()  # P0: a period the refs never use costs
    pr = {i: [ptb(r) for r in v] for i, v in refs.items()}
    assert np.allclose(per_image(pr, {i: ptb(h) for i, h in dotted.items()}), per_image(pr, plain))  # PTB: no cost
    print("selftest ok")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    inputs: dict = {}
    res = {"label": "POST_HOC (CC-088 B-1); registered verdicts unchanged",
           "ptb_punctuations": PTB_PUNCTUATIONS, "bootstrap": {"B": B_BOOT, "seed": SEED},
           "ktvic_test": ktvic(inputs), "xm3600_test": xm3600(inputs)}
    res["inputs_sha256"] = inputs
    res["script_sha256"] = sha(Path(__file__))
    text = json.dumps(res, indent=1, ensure_ascii=False) + "\n"
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
