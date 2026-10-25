#!/usr/bin/env python3
"""Paper E' H2 flip-budget precheck (EXPLORATORY / DEV-PRECHECK, CC-098, CC-101; not confirmatory).
Note: manuscript/prereg/2026-10-25_h2_precheck/PRECHECK_NOTE.md.

Under greedy decoding, VCD-type contrastive decoding (adaptive plausibility, beta >= 0.1) can change a token only where
the head set V_head = {v : p(v) >= beta * max p} has >= 2 members; once one token changes, everything after it may
change. The precheck measures the deletion ceiling: the object-F1 gain from removing every changeable wrong mention,
recall held fixed. It is not an upper bound on CD's F1 gain.

  python scripts/h2_precheck/flipbudget.py --selftest                                         CPU, no data
  NCS_DATA=data python scripts/h2_precheck/flipbudget.py ceiling --pilot-runs P --lists L --labels OIV7 --desc CSV \
      --out J                                                                  CPU, local only: step 0, before any GPU
  python scripts/h2_precheck/flipbudget.py decode --model M --snapshot DIR --lists L --out-dir D        GPU
  NCS_DATA=data python scripts/h2_precheck/flipbudget.py score --runs-dir D --lists L --labels OIV7 --desc CSV \
      --pilot-runs P --out J                                                                  CPU, local only
Decode = the E' pilot's arm D (B-N1 short Vietnamese prompt, greedy, 60 new tokens, same batch slices) on the same two
dev sets, keeping per step |V_head| at beta = 0.1 on the processed scores and on the raw logits, the top-2
log-probability gap, and each token's end offset in the caption. Caption text stays in output files; it is never
printed or committed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(ROOT / "scripts/eprime_pilot"), str(ROOT / "scripts/c_stage2")]
import decode_pilot as DP  # noqa: E402  pilot sets, refusals, arm-D prompt and output schema
import score_pilot as SP  # noqa: E402  the pilot's object rows, F1, bootstrap CI

C, S2, lb = DP.C, DP.S2, DP.lb
LABEL = "EXPLORATORY / DEV-PRECHECK (CC-098, CC-101, H2), not confirmatory"
SCHEMA = "vsps.h2_precheck.v2"
NOTE = "manuscript/prereg/2026-10-25_h2_precheck/PRECHECK_NOTE.md"
BETA = 0.1  # VCD's adaptive plausibility constraint
SESOI = 2.0  # object F1 points, CC-098's pilot gain
B, SEED = 2000, 0
KINDS = {"ktvic_dev299": "ktvic", "xm_dev300": "xm"}
WORD = re.compile(r"\S+")


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


# ------------------------------------------------------------------------------------------------ decode (GPU)
def head_stats(scores, beta: float = BETA):
    """scores: (batch, vocab) logits of one step -> (|V_head|, top-2 log-prob gap) per row."""
    import torch

    lp = torch.log_softmax(scores.float(), -1)
    top = lp.topk(2, -1).values
    n_head = (lp >= top[:, :1] + float(np.log(beta))).sum(-1)
    return n_head.tolist(), (top[:, 0] - top[:, 1]).tolist()


def char_ends(decode, toks: list[int]) -> list[int]:
    """End offset of every token in decode(toks).strip(); monotone, clipped (a split UTF-8 byte may lag by a char)."""
    full = decode(toks)
    lead, n = len(full) - len(full.lstrip()), len(full.strip())
    out, last = [], 0
    for k in range(len(toks)):
        last = max(last, min(n, max(0, len(decode(toks[:k + 1])) - lead)))
        out.append(last)
    return out


def make_generate(proc, net, n_new: int, folder: Path, sink: Path):
    """lb.make_generate with the per-step scores and raw logits kept; steps go to `sink`, one fsynced record per
    slice, each written after a newline so a torn record cannot swallow the next one."""
    import torch
    from PIL import Image

    eos = net.generation_config.eos_token_id
    eos = set(eos if isinstance(eos, list) else [eos])
    dec = lambda t: proc.decode(t, skip_special_tokens=True)  # noqa: E731

    def generate(sl, texts):
        imgs = []
        for _i, f, h in sl:
            if lb.sha256_file(folder / f) != h:
                raise SystemExit(f"{folder / f}: sha256 differs from the manifest")
            imgs.append(Image.open(folder / f).convert("RGB"))
        msgs = [[{"role": "user", "content": [{"type": "image", "image": im}, {"type": "text", "text": t}]}]
                for im, t in zip(imgs, texts, strict=True)]
        enc = proc.apply_chat_template(msgs, add_generation_prompt=True, tokenize=True, return_dict=True,
                                       return_tensors="pt", padding=True).to(net.device, net.dtype)
        with torch.no_grad():
            g = net.generate(**enc, max_new_tokens=n_new, do_sample=False, num_beams=1,
                             return_dict_in_generate=True, output_scores=True, output_logits=True)
        proc_s = [head_stats(s) for s in g.scores]  # per step: ([n_head per row], [gap per row])
        raw_s = [head_stats(s)[0] for s in g.logits]
        out, steps = [], {}
        for r, row in enumerate(g.sequences[:, enc["input_ids"].shape[1]:].tolist()):
            n = next((k + 1 for k, t in enumerate(row) if t in eos), None)
            toks = row[:n or len(row)]
            cap = dec(toks).strip()
            out.append((cap, n or len(row), n is None))
            steps[sl[r][0]] = {"cap": sha(cap), "eos": n is not None,
                               "nh": [proc_s[k][0][r] for k in range(len(toks))],
                               "nh_raw": [raw_s[k][r] for k in range(len(toks))],
                               "gap": [round(proc_s[k][1][r], 4) for k in range(len(toks))],
                               "end": char_ends(dec, toks)}
        with sink.open("a", encoding="utf-8") as fh:
            fh.write("\n" + json.dumps(steps))
            fh.flush()
            os.fsync(fh.fileno())
        return out

    return generate


def read_steps(sink: Path, caps: dict[str, str]) -> dict:
    """{image id: steps}: per id the first record whose caption sha equals the caption in preds.json (ties go to the
    batched decode, which comes before run_arm's solo parity decodes). Torn and blank lines are skipped."""
    want = {i: sha(c) for i, c in caps.items()}
    got: dict = {}
    for line in sink.read_text(encoding="utf-8").split("\n"):
        try:
            rec = json.loads(line) if line.strip() else {}
        except json.JSONDecodeError:
            continue
        for i, st in rec.items():
            if i in want and i not in got and st.get("cap") == want[i]:
                got[i] = st
    if set(got) != set(want):
        raise SystemExit(f"{sink}: no matching steps record for {len(set(want) - set(got))} images")
    return got


def decode_model(model: str, snapshot: Path, lists_path: Path, out_dir: Path) -> None:
    lists = C.load_lists(lists_path)
    reg = C.registration()
    m = reg["models"][model]
    if lb.packages() != reg["venv"]["packages"]:
        raise SystemExit(f"package versions {lb.packages()} differ from the B-N1 venv")
    lb.check_snapshot(m, snapshot)
    plan = {ds: DP.manifest(ds, lists) for ds in DP.SETS}  # the pilot's sets and refusals, before the model loads
    if any(DP.check_disjoint(plan, lists).values()):
        raise SystemExit("REFUSED: an image is in a C or A test set")
    S2.check_folder("xm_dev500", lists)
    zs, n_new = lb.prompt_text(reg, "short"), reg["decode"]["max_new_tokens"]["short"]
    if DP.sha(zs) != C.ZS_PROMPT_SHA256:
        raise SystemExit("the arm-D prompt differs from its pin")
    out_dir.mkdir(parents=True, exist_ok=True)
    proc, net = lb.load(m, snapshot, "cuda:0")
    ctx = {"m": m, "model": model, "zs": zs, "n_new": n_new, "reg_sha": C.PINS[C.B_N1], "packages": lb.packages(),
           "note_sha256": lb.sha256_file(ROOT / NOTE), "gen_cfg": net.generation_config.to_diff_dict(),
           "decoder_sha256": lb.sha256_file(Path(__file__)), "prompt_sha": {"d": C.ZS_PROMPT_SHA256}}
    for ds, items in plan.items():
        rid = f"h2_{model}_{ds}-d"
        out, sink = out_dir / f"{rid}.preds.json", out_dir / f"{rid}.steps.jsonl"
        gen = make_generate(proc, net, n_new, lb.DATA / "datasets" / DP.SETS[ds]["image_dir"], sink)
        caps = DP.run_arm(rid, "d", ds, items, DP.prompts("d", [i for i, _f, _h in items], None, zs), gen, ctx, out)
        read_steps(sink, caps)
        print(f"done {model} {ds}")


# ------------------------------------------------------------------------------------------------ locate (CPU)
def removes(s: str, k: int, e: int, w: str, words: list, extract) -> bool:
    """Blanking s[k:e] removes exactly one w from extract() on a window of the occurrence plus up to 2 words a side."""
    idx = [n for n, (a, b) in enumerate(words) if a < e and b > k]
    lo, hi = words[max(idx[0] - 2, 0)][0], words[min(idx[-1] + 2, len(words) - 1)][1]
    win, blank = s[lo:hi], s[lo:k] + " " * (e - k) + s[e:hi]
    return extract(win).count(w) - extract(blank).count(w) == 1


def spans(caption: str, mentions: list[str], norm, extract) -> list[tuple[int, int] | None]:
    """Character span of each distinct mention (first-occurrence order): the first whole-word occurrence of norm(w),
    left to right, whose blanking removes the mention (so `xe` in `xe máy` or `cây` in `xanh lá cây` is passed over)."""
    s = norm(caption.lower())
    if len(s) != len(caption):
        return [None] * len(mentions)
    words = [(m.start(), m.end()) for m in WORD.finditer(s)]
    out, pos = [], 0
    for w in mentions:
        t, k, hit = norm(w), pos, None
        while hit is None and (k := s.find(t, k)) >= 0:
            e = k + len(t)
            whole = (k == 0 or not s[k - 1].isalnum()) and (e == len(s) or not s[e].isalnum())
            if whole and removes(s, k, e, w, words, extract):
                hit = (k, e)
            k += 1
        out.append(hit)
        pos = hit[1] if hit else pos
    return out


def flags(step: dict, sp: list, unlocated: bool = True) -> tuple[list[bool], list[bool]]:
    """Per mention: (own) a token of the mention is changeable; (cascade) any token up to the mention's last is.
    A step is changeable if |V_head| >= 2 on the processed scores or on the raw logits. A zero-width token right after
    a mention token belongs to the mention, EOS never. An unlocated mention counts as `unlocated` under both."""
    end = step["end"]
    starts = [0] + end[:-1]
    flip = [max(a, b) >= 2 for a, b in zip(step["nh"], step["nh_raw"], strict=True)]
    last = len(end) - 1 if step["eos"] else len(end)
    own, casc = [], []
    for s in sp:
        if s is None:
            own.append(unlocated)
            casc.append(unlocated)
            continue
        tok = [k for k, (a, b) in enumerate(zip(starts, end)) if a < s[1] and b > s[0]]
        k = max(tok) + 1 if tok else len(end)
        while k < len(end) and k != last and starts[k] == end[k]:
            tok.append(k)
            k += 1
        own.append(any(flip[k] for k in tok))
        casc.append(any(flip[: max(tok) + 1]) if tok else any(flip))
    return own, casc


# ------------------------------------------------------------------------------------------------ bounds (CPU)
def wrong(kind: str, w: str, ref) -> bool:
    return w not in ref if kind == "ktvic" else ref.get(w) == "absent"


def oracle(kind: str, ment: list[list[str]], ref: list, fl: list[list[bool]]) -> list[list[str]]:
    """Each caption with every changeable wrong mention removed and nothing else changed (recall held fixed)."""
    return [[w for w, f in zip(m, f_) if not (f and wrong(kind, w, r))] for m, r, f_ in zip(ment, ref, fl, strict=True)]


def rows(kind: str, ment: list, ref: list, tools: dict) -> np.ndarray:
    return SP.rows_of(kind, ment, ref, XO=tools.get("XO"), classes=tools.get("classes"))


def mentions(caps: list[str], tools: dict) -> list[list[str]]:
    return [SP.distinct(c, tools["extract"]) for c in caps]


def ceiling_cell(kind: str, caps: list[str], ref: list, tools: dict) -> dict:
    """Step 0 (W1): every wrong mention removed."""
    ment = mentions(caps, tools)
    return {"x": {"greedy": rows(kind, ment, ref, tools),
                  "ceiling": rows(kind, oracle(kind, ment, ref, [[True] * len(m) for m in ment]), ref, tools)}}


def share(f: list[bool], sel: list[bool]) -> float:
    return round(100 * sum(a for a, s in zip(f, sel) if s) / max(sum(sel), 1), 2)


def cell(kind: str, caps: list[str], steps: list[dict], ref: list, tools: dict) -> dict:
    ment = mentions(caps, tools)
    sp = [spans(c, m, tools["norm"], tools["extract"]) for c, m in zip(caps, ment)]
    x = {"greedy": rows(kind, ment, ref, tools),
         "ceiling": rows(kind, oracle(kind, ment, ref, [[True] * len(m) for m in ment]), ref, tools)}
    fl = {}
    for u, tag in ((True, ""), (False, "_unloc0")):
        own, casc = zip(*(flags(st, s, u) for st, s in zip(steps, sp))) if caps else ((), ())
        x["own" + tag], x["cascade" + tag] = (rows(kind, oracle(kind, ment, ref, f), ref, tools) for f in (own, casc))
        fl[tag] = ([f for f_ in own for f in f_], [f for f_ in casc for f in f_])
    w = [wrong(kind, a, r) for m, r in zip(ment, ref) for a in m]
    multi = [len(a.split()) > 1 for m in ment for a in m]
    fo, fc = fl[""]
    nh = [v for st in steps for v in st["nh"]]
    nr = [v for st in steps for v in st["nh_raw"]]
    pct = lambda v: round(100 * float(np.mean([a >= 2 for a in v])), 2) if v else 0.0  # noqa: E731
    stats = {"images": len(caps), "mentions": len(w), "wrong": sum(w), "unlocated": sum(s is None for p in sp for s in p),
             "steps": len(nh), "steps_head2_pct": pct(nh), "steps_head2_raw_pct": pct(nr),
             "wrong_changeable_own_pct": share(fo, w), "wrong_changeable_cascade_pct": share(fc, w),
             "right_changeable_own_pct": share(fo, [not a for a in w]),
             "wrong_changeable_own_pct_single": share(fo, [a and not m_ for a, m_ in zip(w, multi)]),
             "wrong_changeable_own_pct_multi": share(fo, [a and m_ for a, m_ in zip(w, multi)]),
             "wrong_changeable_cascade_pct_single": share(fc, [a and not m_ for a, m_ in zip(w, multi)]),
             "wrong_changeable_cascade_pct_multi": share(fc, [a and m_ for a, m_ in zip(w, multi)]),
             "wrong_single": sum(a and not m_ for a, m_ in zip(w, multi)), "wrong_multi": sum(a and m_ for a, m_ in zip(w, multi)),
             "first_changeable_step_median": float(np.median([next(
                 (k for k, (a, b) in enumerate(zip(st["nh"], st["nh_raw"])) if max(a, b) >= 2), len(st["nh"]))
                 for st in steps])) if steps else 0.0,
             "greedy_f1": round(SP.point(x["greedy"]), 3)}
    return {"x": x, "stats": stats}


def summarise(cells: dict, idx: dict, keys: tuple) -> dict:
    """Bound - greedy F1 (points x100) per key: pooled = mean over the cells, by_model = mean over a model's sets,
    paired image bootstrap CI."""
    res = {}
    for key in keys:
        draws = [SP.f1(c["x"][key], idx[s]) - SP.f1(c["x"]["greedy"], idx[s]) for (_m, s), c in cells.items()]
        pts = {(m, s): SP.point(c["x"][key]) - SP.point(c["x"]["greedy"]) for (m, s), c in cells.items()}
        models = sorted({m for m, _s in cells})
        res[key] = {"d": round(float(np.mean(list(pts.values()))), 3), "ci95": SP.ci(np.mean(draws, axis=0)),
                    "by_model": {m: round(float(np.mean([v for (mm, _s), v in pts.items() if mm == m])), 3) for m in models},
                    "by_cell": {f"{m}|{s}": round(v, 3) for (m, s), v in pts.items()}}
    return res


def verdict(own: float, cascade: float) -> str:
    return "STOP" if cascade < SESOI else "GO-own" if own >= SESOI else "GO-cascade-only"


def decide(res: dict, stats: dict) -> dict:
    """STOP iff the pooled cascade bound < SESOI: deleting every hallucination reachable at beta 0.1 cannot reach the
    SESOI. GO (GO-own or GO-cascade-only) means not ruled out, never evidence for H2. Unlocated mentions count as
    changeable for the verdict; if counting them as not changeable gives another verdict, or a cell has no step with
    |V_head| >= 2 on the processed scores, the result goes to the judge (TO-JUDGE)."""
    v = verdict(res["own"]["d"], res["cascade"]["d"])
    v0 = verdict(res["own_unloc0"]["d"], res["cascade_unloc0"]["d"])
    dead = sorted(c for c, s in stats.items() if s["steps_head2_pct"] == 0)
    out = {"verdict": "TO-JUDGE" if dead or v != v0 else v, "verdict_unlocated_changeable": v,
           "verdict_unlocated_not_changeable": v0, "cells_without_changeable_steps": dead,
           "cascade_bound": res["cascade"]["d"], "own_bound": res["own"]["d"], "sesoi": SESOI,
           "report_only_models": sorted(m for m, b in res["cascade"]["by_model"].items() if b < SESOI)}
    return out


# ------------------------------------------------------------------------------------------------ local commands
def tools_and_refs(a, lists: dict) -> tuple[dict, dict, dict, dict]:
    if os.environ.get("VSPS_MACHINE_ID"):
        raise SystemExit("scoring uses OIV7 labels and runs locally only; VSPS_MACHINE_ID is set")
    import score as S
    import xm3600_oiv7 as XO
    from rescap import chair as CH

    plan = {ds: DP.manifest(ds, lists) for ds in DP.SETS}
    ids = {ds: [i for i, _f, _h in rows_] for ds, rows_ in plan.items()}
    kt = S.references("ktvic_dev299", lists)
    labels = json.loads(Path(a.labels).read_text(encoding="utf-8"))
    vmap = XO.resolve_map(a.desc)
    st = XO.statuses(vmap, {i: labels[i] for i in ids["xm_dev300"] if i in labels})
    ref = {"ktvic_dev299": [CH._gold_objects(kt[i]) for i in ids["ktvic_dev299"]],
           "xm_dev300": [st.get(i, {}) for i in ids["xm_dev300"]]}
    tools = {"extract": CH.objects_in, "norm": CH.norm_tone, "XO": XO, "classes": set(vmap)}
    n = {"ktvic_dev299": len(ids["ktvic_dev299"]), "xm_dev300": len(ids["xm_dev300"]),
         "xm_dev300_labelled": sum(bool(r) for r in ref["xm_dev300"])}
    return plan, ids, ref, tools | {"n": n}


def preds(path: Path, ids: list[str]) -> list[str]:
    d = json.loads(path.read_text(encoding="utf-8"))
    if d.get("pilot_schema") != DP.SCHEMA or list(d["predictions"]) != ids or d["max_new_tokens"] != 60:
        raise SystemExit(f"{path.name}: not an arm-D output of exactly this set")
    return [d["predictions"][i] for i in ids]


def resample(ids: dict) -> dict:
    rng = np.random.default_rng(SEED)
    return {ds: rng.integers(0, len(ids[ds]), (B, len(ids[ds]))) for ds in DP.SETS}


def cmd_ceiling(a) -> None:
    """W1: the 0-GPU ceiling on the pilot's mirrored arm D. STOP (no GPU) iff the pooled ceiling < SESOI."""
    lists = C.load_lists(a.lists)
    _plan, ids, ref, tools = tools_and_refs(a, lists)
    cells = {(m, ds): ceiling_cell(KINDS[ds], preds(a.pilot_runs / f"ep_{m}_{ds}-d.preds.json", ids[ds]), ref[ds], tools)
             for m in DP.MODELS for ds in DP.SETS}
    res = summarise(cells, resample(ids), ("ceiling",))
    out = {"label": LABEL, "schema": SCHEMA, "step": "0 (CPU, CC-101 W1)", "n": tools["n"], "ceiling": res["ceiling"],
           "decision": "STOP" if res["ceiling"]["d"] < SESOI else "PROCEED", "sesoi": SESOI,
           "inputs": {"lists_sha256": lb.sha256_file(a.lists), "labels_sha256": lb.sha256_file(a.labels),
                      "pilot_runs_sha256": {p.name: lb.sha256_file(p) for p in sorted(a.pilot_runs.glob("ep_*-d.preds.json"))}}}
    Path(a.out).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"ceiling": res["ceiling"]["d"], "ci95": res["ceiling"]["ci95"], "decision": out["decision"]}))


def cmd_score(a) -> None:
    lists = C.load_lists(a.lists)
    _plan, ids, ref, tools = tools_and_refs(a, lists)
    cells, stats, parity, pilot_f1 = {}, {}, {}, {}
    for m in DP.MODELS:
        for ds in DP.SETS:
            rid = f"h2_{m}_{ds}-d"
            caps = preds(a.runs_dir / f"{rid}.preds.json", ids[ds])
            steps = read_steps(a.runs_dir / f"{rid}.steps.jsonl", dict(zip(ids[ds], caps)))
            c = cell(KINDS[ds], caps, [steps[i] for i in ids[ds]], ref[ds], tools)
            pilot = preds(a.pilot_runs / f"ep_{m}_{ds}-d.preds.json", ids[ds])
            key = f"{m}|{ds}"
            cells[m, ds], stats[key] = c, c["stats"]
            parity[key] = round(100 * float(np.mean([x == y for x, y in zip(caps, pilot)])), 2)
            pilot_f1[key] = round(SP.point(rows(KINDS[ds], mentions(pilot, tools), ref[ds], tools)), 3)
    res = summarise(cells, resample(ids), ("ceiling", "own", "cascade", "own_unloc0", "cascade_unloc0"))
    out = {"label": LABEL, "schema": SCHEMA, "beta": BETA, "draws": B, "seed": SEED, "n": tools["n"], "bounds": res,
           "stats": stats, "decision": decide(res, stats), "parity_with_pilot_d_pct": parity,
           "rebuild_not_faithful": sorted(k for k, v in parity.items() if v < 95), "pilot_d_f1": pilot_f1,
           "inputs": {"lists_sha256": lb.sha256_file(a.lists), "labels_sha256": lb.sha256_file(a.labels),
                      "runs_sha256": {p.name: lb.sha256_file(p) for p in sorted(a.runs_dir.glob("h2_*"))}}}
    Path(a.out).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"decision": out["decision"], "parity": parity}))


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def selftest() -> None:
    from rescap import chair as CH

    try:  # head set: beta = 0.1 keeps tokens with p >= 0.1 * p_max
        import torch
        n, gap = head_stats(torch.log(torch.tensor([[0.5, 0.04, 0.46], [0.9, 0.05, 0.05]])))
        assert n == [2, 1] and abs(gap[0] - float(np.log(0.5 / 0.46))) < 1e-5, (n, gap)
    except ImportError:
        print("(torch absent: head_stats not tested here; the job's selftest runs it in venv-lb)")
    # char ends: monotone, stripped, a lagging partial byte does not move an end backwards
    pieces = {(): "", (1,): " a", (1, 2): " ab", (1, 2, 3): " ab�", (1, 2, 3, 4): " abc"}
    assert char_ends(lambda t: pieces[tuple(t)], [1, 2, 3, 4]) == [1, 2, 3, 3]
    # spans with the real matcher (W3): tone-normalised search, compounds and colour phrases passed over
    norm, ext = CH.norm_tone, CH.objects_in
    loc = lambda c: spans(c, SP.distinct(c, ext), norm, ext)  # noqa: E731
    # test captions are made up and shorter than 6 words (the commit gate's 6-gram caption scan)
    c2 = "xe máy và xe"
    assert SP.distinct(c2, ext) == ["xe máy", "xe"] and loc(c2) == [(0, 6), (10, 12)], loc(c2)
    c3 = "áo xanh lá cây, cây"
    m3 = SP.distinct(c3, ext)
    assert m3 == ["áo", "cây"] and loc(c3)[1] == (c3.rindex("cây"), len(c3)), (m3, loc(c3))
    c4 = "người đàn ông, người"
    m4 = SP.distinct(c4, ext)
    assert loc(c4)[m4.index("người")] == (c4.rindex("người"), len(c4)), (m4, loc(c4))
    old = lambda t: t.replace("toà", "tòa")  # noqa: E731  a lexicon key in the old tone style
    c5 = "một tòa nhà cao"
    assert spans(c5, [old("toà nhà")], norm, lambda t: [old(w) for w in ext(t)]) == [(4, 11)]
    assert spans("bóng", ["bò"], norm, ext) == [None]
    # flags: own vs cascade, raw-logit head set, zero-width completion token, EOS excluded, unlocated both ways
    step = {"nh": [1, 2, 1, 1], "nh_raw": [1, 1, 1, 1], "end": [3, 7, 10, 14], "eos": False}
    assert flags(step, [(0, 3), (8, 10), None]) == ([False, False, True], [False, True, True])
    assert flags(step, [None], unlocated=False) == ([False], [False])
    assert flags({**step, "nh": [1] * 4, "nh_raw": [1, 1, 2, 1]}, [(8, 10)]) == ([True], [True]), "raw head set"
    zw = {"nh": [1, 1, 2, 1], "nh_raw": [1] * 4, "end": [3, 6, 6, 9], "eos": True}  # token 2: zero-width completion
    assert flags(zw, [(4, 6)]) == ([True], [True]), "a zero-width token completing the mention belongs to it"
    eos = {"nh": [1, 1, 2], "nh_raw": [1] * 3, "end": [3, 6, 6], "eos": True}  # token 2 is EOS
    assert flags(eos, [(4, 6)]) == ([False], [False]), "EOS never belongs to a mention"
    # oracle: only changeable wrong mentions go
    assert oracle("ktvic", [["a", "b", "c"]], [{"a"}], [[True, True, False]]) == [["a", "c"]]
    assert oracle("xm", [["a", "b"]], [{"a": "present", "b": "absent"}], [[True, True]]) == [["a"]]
    # a toy cell: the wrong mention after an early flip is removable under the cascade bound only
    toy = {"extract": str.split, "norm": lambda s: s}
    caps = ["a z"] * 30
    st0 = {"cap": sha("a z"), "eos": True, "nh_raw": [1] * 4, "end": [1, 2, 3, 3]}
    c0 = cell("ktvic", caps, [{**st0, "nh": [1, 1, 1, 2]}] * 30, [{"a"}] * 30, toy)  # only EOS changeable
    c1_ = cell("ktvic", caps, [{**st0, "nh": [2, 1, 1, 1]}] * 30, [{"a"}] * 30, toy)  # first token changeable
    idx = {"s": np.random.default_rng(0).integers(0, 30, (B, 30))}
    keys = ("ceiling", "own", "cascade", "own_unloc0", "cascade_unloc0")
    r0, r1 = summarise({("m", "s"): c0}, idx, keys), summarise({("m", "s"): c1_}, idx, keys)
    assert r0["cascade"]["d"] == 0 and r0["own"]["d"] == 0 and r0["ceiling"]["d"] > SESOI
    assert decide(r0, {"m|s": c0["stats"]})["verdict"] == "STOP"
    d1 = decide(r1, {"m|s": c1_["stats"]})
    assert r1["cascade"]["d"] > SESOI and r1["own"]["d"] == 0 and d1["verdict"] == "GO-cascade-only", d1
    assert c1_["stats"]["wrong_changeable_cascade_pct"] == 100 and c1_["stats"]["wrong_changeable_own_pct"] == 0
    # the rule: labels, report-only models, TO-JUDGE on a verdict flip or a dead head set
    b = lambda own, cas, o0=None, c0_=None, bm=None: {  # noqa: E731
        "own": {"d": own}, "cascade": {"d": cas, "by_model": bm or {"m1": cas, "m2": cas}},
        "own_unloc0": {"d": own if o0 is None else o0}, "cascade_unloc0": {"d": cas if c0_ is None else c0_}}
    live = {"c": {"steps_head2_pct": 5.0}}
    assert decide(b(2.0, 3.0), live)["verdict"] == "GO-own" and decide(b(1.9, 2.0), live)["verdict"] == "GO-cascade-only"
    assert decide(b(0, 1.99), live)["verdict"] == "STOP"
    assert decide(b(0, 3.0, c0_=1.0), live)["verdict"] == "TO-JUDGE", "verdict differs with unlocated not changeable"
    assert decide(b(0, 3.0), {"c": {"steps_head2_pct": 0.0}})["verdict"] == "TO-JUDGE", "dead head set"
    assert decide(b(0, 3.0, bm={"m1": 5.0, "m2": 1.0}), live)["report_only_models"] == ["m2"]
    # steps file (W4): caption-sha match, first matching record wins, torn and blank lines skipped
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "s.jsonl"
        rec = lambda c, tag: {"cap": sha(c), "tag": tag}  # noqa: E731
        p.write_text("\n" + json.dumps({"i1": rec("old", 0)}) + "\n" + json.dumps({"i1": rec("x", 1), "i2": rec("y", 1)})
                     + "\n" + '{"i3": {"ca' + "\n" + json.dumps({"i1": rec("x", 2), "i3": rec("z", 2)}) + "\n\n",
                     encoding="utf-8")
        got = read_steps(p, {"i1": "x", "i2": "y", "i3": "z"})
        assert {i: s["tag"] for i, s in got.items()} == {"i1": 1, "i2": 1, "i3": 2}, got
        assert C.refuses(lambda: read_steps(p, {"i1": "x", "i4": "w"})), "an id without a matching record refuses"
    print("selftest ok: head set, char ends, real-matcher spans, own/cascade/raw/zero-width/EOS flags, oracle, "
          "ceiling, GO-own/GO-cascade-only/STOP/TO-JUDGE rule, steps file")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("decode")
    p.add_argument("--model", choices=DP.MODELS, required=True)
    p.add_argument("--snapshot", type=Path, required=True)
    p.add_argument("--lists", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    for name in ("ceiling", "score"):
        q = sub.add_parser(name)
        if name == "score":
            q.add_argument("--runs-dir", type=Path, required=True)
        q.add_argument("--pilot-runs", type=Path, required=True, help="the E' pilot's mirrored runs/ (arm D)")
        q.add_argument("--lists", type=Path, required=True)
        q.add_argument("--labels", type=Path, required=True, help="data/xm3600/oiv7_labels.json (local)")
        q.add_argument("--desc", type=Path, required=True, help="oidv7-class-descriptions.csv")
        q.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    cmds = {"decode": lambda: decode_model(a.model, a.snapshot, a.lists, a.out_dir), "ceiling": lambda: cmd_ceiling(a),
            "score": lambda: cmd_score(a)}
    if a.cmd not in cmds:
        ap.error("decode, ceiling, score or --selftest")
    cmds[a.cmd]()


if __name__ == "__main__":
    main()
