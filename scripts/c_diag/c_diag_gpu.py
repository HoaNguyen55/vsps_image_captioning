#!/usr/bin/env python3
"""C-DIAG host code (Paper C; prereg C_DIAG_PREREG_DRAFT_v1_2.md afbb61fb + CC-299r3 R1-R8; §10.2 item 2). Runs on HD-1
only through c_diag_job.sh, in the CC-212 decode venv (B-N1 packages), except `cap`, `left`, `next`, `project` and
`wipe` (stdlib; also the laptop selftest).

    $PY -X utf8 -I -B scripts/c_diag/c_diag_gpu.py fetch     --model M --snapshot S             (setup; pinned revision only)
    $PY -X utf8 -I -B scripts/c_diag/c_diag_gpu.py hostcheck --model M --snapshot S --hd HD --out O
    $PY -X utf8 -I -B scripts/c_diag/c_diag_gpu.py gate      --model M --snapshot S --hd HD --out O     (§4.1: image + blind)
    $PY -X utf8 -I -B scripts/c_diag/c_diag_gpu.py run       --model M --snapshot S --hd HD --out O     (S2/S3: per set not
                                                     cut: verify -> texts -> decode rand, ret, filt[, ctl]; one load)
    $PY -X utf8 -I -B scripts/c_diag/c_diag_gpu.py cap       --out O --branch main|gate-only --rate R --rent-utc T --freeze H
    $PY -X utf8 -I -B scripts/c_diag/c_diag_gpu.py left|next|project --out O ...      cap ledger, next step, projection + cuts
    $PY -X utf8 -I -B scripts/c_diag/c_diag_gpu.py wipe      --dir HD --log L
Outputs (O/out) hold ids, labels, masks, counts and the query captions only; logs hold ids and counts. Demonstration
text never leaves /dev/shm/c_diag_hd. A FAULT exits 9 (final for the job), a crash exits 1 (the job retries a step
up to 3 attempts, §8.4), the cap's timeout 124.
"""
from __future__ import annotations

import argparse
import calendar
import hashlib
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(os.path.abspath(__file__)).parent  # unresolved: the mutant suite runs scratch copies
sys.path.insert(0, str(HERE))
import c_diag as D  # noqa: E402  constants, pins, deny backstop, plan / hour_cap

ROOT = D.ROOT
FAULT_RC = 9
PROGRESS_N = 100  # §8.3 [N2]: re-project after the first 100 queries of every verify and decode stage
P = {}  # {"ver_3way.txt": text}, read by sha (CC-299r3 NB-C2: CP.prompts would open all nine prompt files)


def fault(msg: str):
    raise SystemExit(f"FAULT: {msg}")


def jload(p: Path):
    return json.loads(Path(p).read_text("utf-8"))


def now() -> float:
    return time.time()


# ---------------------------------------------------------------------------------------------- host guard
def host_guard() -> None:
    """Appendix C: the host never opens a label, status, reference or test-role file. The repo copy holds no data/
    (checked by the job); any open under it, or matching the §2.3 backstop, is a FAULT. Ceiling: native opens."""
    data = os.path.abspath(ROOT / "data")

    def hook(ev, args):
        if ev == "open" and isinstance(args[0], (str, bytes, os.PathLike)):
            p = os.path.abspath(os.fsdecode(args[0]))
            why = D.deny(p) or ("repo data/" if D.under(p, [data]) else None)
            if why:
                raise SystemExit(f"FAULT: host open refused: {p} ({why})")
    sys.addaudithook(hook)


# ---------------------------------------------------------------------------------------------- arm texts (laptop-tested)
def verify_image(dcs: list[dict], ask) -> tuple[list[list[str]], dict]:
    """§3.2 [W9 (a)]: only obj propositions are asked, in rank order (demonstration rank 1 first, left to right), the
    first CAP = 32 per image (c_pvr.verify); text propositions are never asked. Per proposition: SUPPORTED /
    UNCERTAIN / REJECTED, CAP (an obj beyond the cap, never asked) or TEXT."""
    flat = [(n, j) for n, dc in enumerate(dcs) for j, p in enumerate(dc["props"]) if p["kind"] == "obj"]
    labs, st = D.CP.verify([dcs[n]["props"][j] for n, j in flat], ask, "filt")
    out = [["TEXT"] * len(dc["props"]) for dc in dcs]
    for x, ((n, j), lab) in enumerate(zip(flat, labs)):
        out[n][j] = "CAP" if x >= D.CP.CAP else lab
    return out, st


def filt_masks(labels: list[list[str]]) -> list[list[bool]]:
    """§3.2: remove REJECTED obj propositions only; UNCERTAIN, parse failures (UNCERTAIN) and CAP stay."""
    return [[lab == "REJECTED" for lab in d] for d in labels]


def ctl_masks(qid: str, dcs: list[dict], fm: list[list[bool]]) -> list[list[bool]]:
    """§5.1 [N4, W9 (a)]: c_pvr.a7_masks(image_id, obj-only masks) unchanged, mapped back; seed arm_rng("A7", id);
    drawn among every obj proposition of a demonstration, those beyond CAP included (NB-4)."""
    obj = [[j for j, p in enumerate(dc["props"]) if p["kind"] == "obj"] for dc in dcs]
    a7 = D.CP.a7_masks(qid, [[m[j] for j in o] for m, o in zip(fm, obj)])
    out = [[False] * len(dc["props"]) for dc in dcs]
    for n, (o, sel) in enumerate(zip(obj, a7)):
        for j, s in zip(o, sel):
            out[n][j] = s
    return out


def prompt_order(w: dict, xs: list) -> list:
    """ret ids are kept in rank order; the prompt shows them in the frozen order (InternVL3 'last' = reversed)."""
    return xs[::-1] if w["order"] == "last" else list(xs)


def arm_prompt(w: dict, arm: str, qid: str, zs: str, labels=None) -> tuple[str, dict]:
    """§5.1: (prompt text, counts). rand / ret = CC-212's prompt; filt / ctl = ret after span deletion
    (c_pvr.demos_after; an emptied demonstration is dropped, never back-filled); all emptied -> zero-shot `short`."""
    if arm in ("rand", "ret"):
        ids = w["rand"][qid] if arm == "rand" else prompt_order(w, w["ret"][qid])
        return D.C.prompt(w["tpl"], [w["shown"][c] for c in ids]), {"n_demos": len(ids), "emptied": 0, "removed": 0}
    dcs = [w["dc"][c] for c in w["ret"][qid]]
    fm = filt_masks(labels)
    m = fm if arm == "filt" else ctl_masks(qid, dcs, fm)
    kept, emptied = D.CP.demos_after(prompt_order(w, dcs), prompt_order(w, m))
    info = {"n_demos": len(kept), "emptied": emptied, "removed": sum(map(sum, m)), "fallback": not kept}
    return (D.C.prompt(w["tpl"], kept) if kept else zs), info


def text_only(proc, net, n_new: int):
    """The image-blind pass (§4.1): the model's text-only chat path (CC-212 guard.py hf_verifier / decode2 pattern)."""
    import torch

    eos = net.generation_config.eos_token_id
    eos = set(eos if isinstance(eos, list) else [eos])

    def generate(texts):
        msgs = [[{"role": "user", "content": [{"type": "text", "text": t}]}] for t in texts]
        enc = proc.apply_chat_template(msgs, add_generation_prompt=True, tokenize=True, return_dict=True,
                                       return_tensors="pt", padding=True).to(net.device)
        with torch.no_grad():
            ids = net.generate(**enc, max_new_tokens=n_new, do_sample=False, num_beams=1)
        out = []
        for row in ids[:, enc["input_ids"].shape[1]:].tolist():
            n = next((k + 1 for k, t in enumerate(row) if t in eos), None)
            out.append(proc.decode(row[:n or len(row)], skip_special_tokens=True).strip())
        return out
    return generate


# ---------------------------------------------------------------------------------------------- rows on disk
class Out:
    """Append-only jsonl, one fsynced line per record; a torn last line (crash mid-write) is dropped on reopen."""

    def __init__(self, p: Path, key: str):
        self.p, self.done = p, {}
        if p.exists():
            lines = p.read_text("utf-8").splitlines()
            for n, x in enumerate(lines):
                try:
                    r = json.loads(x)
                except json.JSONDecodeError:
                    if n != len(lines) - 1:
                        fault(f"{p.name}: corrupt line {n}")
                    p.write_text("".join(y + "\n" for y in lines[:n]), "utf-8")
                    break
                if r[key] in self.done:
                    fault(f"{p.name}: repeated {key}")
                self.done[r[key]] = r
        self.key = key

    def add(self, r: dict) -> None:
        with open(self.p, "a", encoding="utf-8") as f:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
            f.flush()
            os.fsync(f.fileno())
        self.done[r[self.key]] = r


def write_atomic(p: Path, obj) -> None:
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=1) + "\n", "utf-8")
    tmp.replace(p)


# ---------------------------------------------------------------------------------------------- cap ledger (§8.3-8.4)
def cap_rec(o: Path) -> dict:
    c = jload(o / "CAP.json")
    if c.get("label") != D.LABEL or c["branch"] not in ("main", "gate-only"):
        fault("CAP.json is not a C-DIAG cap record")
    return c


def left(o: Path, t: float | None = None) -> int:
    """Seconds left = cap - elapsed BILLED time (from the rental stamp, not job time) - 0.5 h for pull and delete."""
    c = cap_rec(o)
    return int(c["cap_h"] * 3600 - D.PULL_H * 3600 - ((t or now()) - c["rent_epoch"]))


def cuts(o: Path) -> list[str]:
    return jload(o / "CUTS.json")["cuts"] if (o / "CUTS.json").exists() else []


def done(o: Path, st: str) -> bool:
    return (o / "logs" / f"done.{st}").exists()


def mark(o: Path, st: str) -> None:
    (o / "logs" / f"done.{st}").write_text(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) + "\n", "utf-8")


def phases(w: dict) -> list[str]:
    b, ds = w["backbone"], w["set"]
    return [f"verify.{b}.{ds}", f"texts.{b}.{ds}", *(f"decode.{b}.{ds}.{a}" for a in D.ARMS[ds])]


def work_of(hd: Path, b: str, ds: str) -> dict | None:
    p = hd / f"work.{b}.{ds}.json"
    return jload(p) if p.exists() else None


def calls_of(w: dict) -> int:
    return sum(min(sum(p["kind"] == "obj" for c in w["ret"][q] for p in w["dc"][c]["props"]), D.CAP)
               for q in w["ret"])


def rate(o: Path, model: str, kind: str, ds: str) -> float:
    """Measured s per unit of (model, kind, set), else of (model, kind) on any set, else the §8.1 planning rate."""
    found = {}
    files = sorted((o / "logs").glob(f"rate.{kind}.{model}.*.json"))
    if kind == "verify" and not files:  # §8.3 first run: the measured gate rate (with image) stands in for verify
        files = sorted((o / "logs").glob(f"rate.gate.{model}.*.json"))
    for p in files:
        r = jload(p)
        if r["n"] > 0:
            found[r["set"]] = r["sec"] / r["n"]
    if ds in found:
        return found[ds]
    if found:
        return max(found.values())
    return D.RATE_V[model] if kind in ("verify", "gate") else D.RATE_D[(model, ds)]


def project(o: Path, hd: Path, models: list[str], t: float | None = None) -> dict:
    """§8.3 [N2] form: elapsed billed time + rate x work left + pending loads + 0.5 h. On excess, the highest
    not-yet-started block in the cut order is removed, repeatedly; cuts are sticky (CUTS.json, read before each
    block). Never cut: the gate and the first XM-test2500 block of the run (§8.3)."""
    c = cap_rec(o)
    got = cuts(o)
    blocks = [k for k in D.ORDER if k[0] in models and "|".join(k) not in got and work_of(hd, *k)]
    never = next((k for k in blocks if k[1] == "xm_test2500"), None)
    elapsed = ((t or now()) - c["rent_epoch"]) / 3600

    def need(k) -> float:
        w = work_of(hd, *k)
        b, ds = k
        h = 0.0
        for st in phases(w):
            if done(o, st):
                continue
            kind = st.split(".")[0]
            n_done = jload(o / "logs" / f"rate.{st}.json")["n"] if (o / "logs" / f"rate.{st}.json").exists() else 0
            total = calls_of(w) if kind == "verify" else 0 if kind == "texts" else len(w["items"])
            h += max(0, total - n_done) * rate(o, b, "verify" if kind == "verify" else "decode", ds) / 3600
        return h

    def started(k) -> bool:
        return any(done(o, st) or (o / "logs" / f"rate.{st}.json").exists() for st in phases(work_of(hd, *k)))

    def proj(ks) -> float:
        pending = {b for b, _ds in ks if not any(started(x) for x in ks if x[0] == b)}
        return elapsed + sum(need(k) for k in ks) + len(pending) * D.LOAD_H + D.PULL_H
    new = []
    while proj(blocks) > c["cap_h"]:
        nxt = next((k for k in D.CUT_ORDER if k in blocks and k != never and not started(k)), None)
        if nxt is None:
            break  # §8.3: only the running block or never-cut blocks are left; a cap stop is then final
        new.append("|".join(nxt))
        blocks.remove(nxt)
    if new:
        write_atomic(o / "CUTS.json", {"label": D.LABEL, "cuts": got + new, "utc": time.strftime(
            "%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    return {"projection_h": proj(blocks), "cap_h": c["cap_h"], "new_cuts": new, "cuts": got + new}


def next_step(o: Path, hd: Path, mode: str, models: list[str]) -> str | None:
    """The job's next step: gate.<model> (gate mode), else run.<model> while that model has a block not done and not
    cut. Nothing in the gate-only branch beyond the gate (R2-W1 (d))."""
    c = cap_rec(o)
    if mode == "gate":
        return next((f"gate.{m}" for m in D.BACKBONES if not done(o, f"gate.{m}")), None)
    if c["branch"] == "gate-only":
        fault("the gate-only branch runs no S2 / S3 (R2-W1 (d))")
    for b in [m for m in D.BACKBONES if m in models]:
        for k in [k for k in D.ORDER if k[0] == b]:
            w = work_of(hd, *k)
            if w and "|".join(k) not in cuts(o) and not all(done(o, st) for st in phases(w)):
                return f"run.{b}"
    return None


# ---------------------------------------------------------------------------------------------- GPU subcommands
def model(b: str, snapshot: Path):
    reg = D.REG
    m = reg["models"][b]
    if (m["hub_id"], m["revision"]) != (D.BACKBONES[b]["hub_id"], D.BACKBONES[b]["revision"]):
        fault(f"{b}: B-N1 pin differs from §7")
    if D.C.lb.packages() != reg["venv"]["packages"]:
        fault(f"package versions {D.C.lb.packages()} differ from the CC-212 (B-N1) venv")
    D.C.lb.check_snapshot(m, snapshot)
    proc, net = D.C.lb.load(m, snapshot, "cuda:0")
    return reg, m, proc, net


def asker(proc, net, folder: Path, item):
    gen = D.C.lb.make_generate(proc, net, "", D.CP.MAX_NEW["verify"], folder)  # greedy, 8 new tokens, batch 1, bf16
    return lambda text: gen([tuple(item)], [D.CP.ver_prompt(P, text)])[0][0]


def progress(o: Path, st: str, b: str, ds: str, n: int, sec: float) -> None:
    write_atomic(o / "logs" / f"rate.{st}.json", {"step": st, "model": b, "set": ds, "n": n, "sec": sec})


def cmd_gate(a) -> None:
    """S1 (§4.1-4.2): every gate unit with its query image, then image-blind; labels only (no answer text kept)."""
    units = jload(a.hd / "gate_units.json")
    _reg, _m, proc, net = model(a.model, a.snapshot)
    blind = text_only(proc, net, D.CP.MAX_NEW["verify"])
    out = Out(a.out / "out" / f"gate.{a.model}.jsonl", "u")
    n0 = len(out.done)
    t_img = 0.0
    for u in units:
        if u["u"] in out.done:
            continue
        item = (u["qid"], u["file"], u["image_sha256"])
        t0 = now()
        lab, bad = D.CP.parse_label(asker(proc, net, a.hd / "img" / "xm_dev500", item)(u["text"]))
        t_img += now() - t0
        blab, bbad = D.CP.parse_label(blind([D.CP.ver_prompt(P, u["text"])])[0])
        out.add({"u": u["u"], "qid": u["qid"], "label": lab, "parse_fail": bad, "blind_label": blab,
                 "blind_parse_fail": bbad})
    progress(a.out, f"gate.{a.model}.xm_dev500", a.model, "xm_dev500", len(units) - n0, t_img)  # with-image passes


def run_block(a, w: dict, proc, net, reg, m) -> None:
    b, ds = w["backbone"], w["set"]
    zs = D.ZS
    if D.C.sha(zs) != w["zs_sha256"] or D.C.sha(zs) != D.C.ZS_PROMPT_SHA256:
        fault("zero-shot prompt differs from CC-212's short prompt (8870589c)")
    folder = a.hd / "img" / ds
    st = f"verify.{b}.{ds}"
    vo = Out(a.out / "out" / f"verify.{b}.{ds}.jsonl", "id")
    if not done(a.out, st):
        t0, n0 = now(), len(vo.done)
        for i, (q, f, h) in enumerate(w["items"]):
            if q in vo.done:
                continue
            labels, cnt = verify_image([w["dc"][c] for c in w["ret"][q]], asker(proc, net, folder, (q, f, h)))
            vo.add({"id": q, "labels": labels, **{k: cnt[k] for k in ("calls", "cap_hits", "parse_fail", "yes",
                                                                       "maybe", "no")}})
            if len(vo.done) - n0 == PROGRESS_N:  # §8.3 [N2]
                progress(a.out, st, b, ds, sum(r["calls"] for r in vo.done.values()), now() - t0)
                project(a.out, a.hd, a.models)
        progress(a.out, st, b, ds, sum(r["calls"] for r in vo.done.values()), now() - t0)
        mark(a.out, st)
    lab = {q: r["labels"] for q, r in vo.done.items()}
    if set(lab) != {q for q, _f, _h in w["items"]}:
        fault(f"{st}: not every image verified")
    st = f"texts.{b}.{ds}"
    tp = a.out / "out" / f"texts.{b}.{ds}.json"
    texts = {arm: {q: arm_prompt(w, arm, q, zs, lab[q]) for q, _f, _h in w["items"]} for arm in D.ARMS[ds]}
    for arm in ("rand", "ret"):
        if {q: D.C.sha(t) for q, (t, _i) in texts[arm].items()} != w["prompt_sha256"][arm]:
            fault(f"{b} {ds} {arm}: host prompt differs from CC-212's (§5.3)")
    rec = {arm: {q: {**i, "prompt_sha256": D.C.sha(t)} for q, (t, i) in texts[arm].items()} for arm in D.ARMS[ds]}
    if not done(a.out, st):
        write_atomic(tp, {"label": D.LABEL, "backbone": b, "set": ds, "arms": rec})
        mark(a.out, st)
    elif jload(tp)["arms"] != rec:
        fault(f"{st}: recomputed texts differ from the record")
    n_new = reg["decode"]["max_new_tokens"]["short"]
    gen = D.C.lb.make_generate(proc, net, zs, n_new, folder)
    kw = {"max_new_tokens": n_new, "do_sample": False, "num_beams": 1}
    for arm in D.ARMS[ds]:
        st = f"decode.{b}.{ds}.{arm}"
        if done(a.out, st):
            continue
        txt = {q: t for q, (t, _i) in texts[arm].items()}
        t0, n = now(), [0]

        def log(*_x, **_k):
            n[0] += 1
            if n[0] * m["batch_size"] == PROGRESS_N:
                progress(a.out, st, b, ds, PROGRESS_N, now() - t0)
                project(a.out, a.hd, a.models)
        part = a.out / "out" / f"{st}.partial.jsonl"
        key = D.C.lb.run_key(D.PREREG[1], {"step": st}, m, kw, json.dumps({q: D.C.sha(t) for q, t in txt.items()},
                                                                          sort_keys=True), w["items"])
        rows = D.C.lb.decode_slices([tuple(x) for x in w["items"]], m["batch_size"],
                                    lambda sl: gen(sl, [txt[i] for i, _f, _h in sl]), part, key, log)
        write_atomic(a.out / "out" / f"{st}.json", {
            "label": D.LABEL, "backbone": b, "set": ds, "arm": arm, "revision": m["revision"],
            "batch_size": m["batch_size"], "generate_kwargs": kw, "packages": D.C.lb.packages(),
            "predictions": {r["image_id"]: r["caption"] for r in rows},
            "n_tokens": {r["image_id"]: r["n_tokens"] for r in rows}, "hit_max": {r["image_id"]: r["hit_max"] for r in rows},
            "decode_order": [r["image_id"] for r in rows], **{k: {q: v[k] for q, v in rec[arm].items()}
                                                              for k in ("prompt_sha256", "n_demos", "emptied")}})
        progress(a.out, st, b, ds, len(rows), now() - t0)
        mark(a.out, st)


def cmd_run(a) -> None:
    """S2/S3 for one backbone (§5.2 order within it), one model load: each set not cut and not done."""
    blocks = [k for k in D.ORDER if k[0] == a.model and work_of(a.hd, *k)]
    reg, m, proc, net = model(a.model, a.snapshot)
    for k in blocks:
        w = work_of(a.hd, *k)
        if "|".join(k) in cuts(a.out) and not any(done(a.out, st) for st in phases(w)):
            continue  # a cut block never starts (§8.3)
        run_block(a, w, proc, net, reg, m)


def cmd_hostcheck(a) -> None:
    """§7 [N16]: GPU, packages, pinned snapshot, and the VRAM peak of the backbone at a full k-demonstration prompt."""
    import torch

    reg, m, proc, net = model(a.model, a.snapshot)
    units = jload(a.hd / "gate_units.json")
    k = D.BACKBONES[a.model]["k"]
    w = next((work_of(a.hd, *x) for x in D.ORDER if x[0] == a.model and work_of(a.hd, *x)), None)
    if w:
        q, f, h = w["items"][0]
        text, item, folder = arm_prompt(w, "ret", q, "", None)[0], (q, f, h), a.hd / "img" / w["set"]
    else:  # gate-only branch: a k-demonstration prompt from gate proposition texts (no demonstration file on HD)
        text = D.C.prompt(D.BACKBONES[a.model]["tpl"], [u["text"] for u in units[:k]])
        u = units[0]
        item, folder = (u["qid"], u["file"], u["image_sha256"]), a.hd / "img" / "xm_dev500"
    torch.cuda.reset_peak_memory_stats()
    D.C.lb.make_generate(proc, net, text, reg["decode"]["max_new_tokens"]["short"], folder)([item], [text])
    rec = {"label": D.LABEL, "model": a.model, "revision": m["revision"], "gpu": torch.cuda.get_device_name(0),
           "packages": D.C.lb.packages(), "vram_peak_bytes": int(torch.cuda.max_memory_allocated()),
           "k": k, "freeze_sha256": os.environ.get("C_DIAG_FREEZE"), "code": os.environ.get("C_DIAG_CODE")}
    write_atomic(a.out / f"HOSTCHECK_{a.model}.json", rec)
    print(json.dumps({k2: rec[k2] for k2 in ("model", "gpu", "vram_peak_bytes")}))


def cmd_cap(a) -> None:
    """CAP.json, written once at rental (coordinator): branch, offer rate, rental stamp, hour cap (§8.3), freeze."""
    p = a.out / "CAP.json"
    if p.exists():
        fault("CAP.json exists; it is written once")
    t = calendar.timegm(time.strptime(a.rent_utc, "%Y-%m-%dT%H:%M:%SZ"))
    gate_only = a.branch == "gate-only"
    rec = {"label": D.LABEL, "branch": a.branch, "rate": a.rate, "rent_utc": a.rent_utc, "rent_epoch": t,
           "cap_h": D.hour_cap(a.rate, gate_only), "freeze_sha256": a.freeze}
    with open(p, "x", encoding="utf-8") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")
    print(json.dumps(rec, sort_keys=True))


def cmd_wipe(a) -> int:
    """Appendix C 6: delete every tmpfs file by name (c_pvr_gpu.wipe, no recursive delete) and log the counts."""
    if hashlib.sha256((ROOT / "scripts/c_pvr_gpu/c_pvr_gpu.py").read_bytes()).hexdigest() != \
            D.CODE["scripts/c_pvr_gpu/c_pvr_gpu.py"]:
        fault("c_pvr_gpu.py differs from its pin 9a9c6eb5")
    sys.path.insert(0, str(ROOT / "scripts/c_pvr_gpu"))
    import c_pvr_gpu as G  # noqa: E402  wipe() is stdlib-only

    return G.wipe(Path(a.dir), Path(a.log))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for c in ("fetch", "hostcheck", "gate", "run", "cap", "left", "next", "project", "wipe"):
        p = sub.add_parser(c)
        p.add_argument("--out", type=Path)
        p.add_argument("--hd", type=Path, default=Path("/dev/shm/c_diag_hd"))
        p.add_argument("--model", choices=sorted(D.BACKBONES))
        p.add_argument("--models", nargs="*", default=[])
        p.add_argument("--snapshot", type=Path)
        p.add_argument("--mode", choices=("gate", "main"))
        p.add_argument("--branch", choices=("main", "gate-only"))
        p.add_argument("--rate", type=float)
        p.add_argument("--rent-utc")
        p.add_argument("--freeze")
        p.add_argument("--dir")
        p.add_argument("--log")
    a = ap.parse_args()
    ledger = {"wipe": lambda: cmd_wipe(a), "cap": lambda: cmd_cap(a),  # stdlib only: no model code is imported
              "left": lambda: print(max(0, left(a.out))),
              "next": lambda: print(next_step(a.out, a.hd, a.mode, a.models) or ""),
              "project": lambda: print(json.dumps(project(a.out, a.hd, a.models)))}
    if a.cmd in ledger:
        return ledger[a.cmd]() or 0
    D.load()
    b = (ROOT / "scripts/c_pvr/prompts/ver_3way.txt").read_bytes()
    if hashlib.sha256(b).hexdigest() != D.CODE["scripts/c_pvr/prompts/ver_3way.txt"]:
        fault("ver_3way.txt differs from its pin bcb92308")
    P["ver_3way.txt"] = b.decode("utf-8")
    if a.cmd == "fetch":  # §7: once, by the pinned revision, then shard-checked (lb.fetch -> check_snapshot)
        D.C.lb.fetch(D.REG, a.model, a.snapshot)
        return 0
    host_guard()
    {"hostcheck": cmd_hostcheck, "gate": cmd_gate, "run": cmd_run}[a.cmd](a)
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit as e:
        if isinstance(e.code, str) and e.code.startswith("FAULT"):
            print(e.code, file=sys.stderr)
            sys.exit(FAULT_RC)
        raise
