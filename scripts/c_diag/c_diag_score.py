#!/usr/bin/env python3
"""C-DIAG laptop scorer (Paper C; prereg C_DIAG_PREREG_DRAFT_v1_2.md afbb61fb + CC-299r3 R1-R8; §10.2 item 4).

    PY=~/.venvs/c_pvr/bin/python;  PYC=~/.venvs/c_pvr_cider/bin/python   (cider only: pycocoevalcap via the kit pin)
    $PY  -X utf8 -I -B scripts/c_diag/c_diag_score.py gate  --pull P --sums SHA256SUMS_gate|SHA256SUMS_gate-only[_stop]
         --sums-sha H --labels L --labels-sha H --gate-sha H --res R [--deleted-utc T]         (§4.2-4.3; S1 verdict)
    $PYC -X utf8 -I -B scripts/c_diag/c_diag_score.py cider --pull P --sums SHA256SUMS_main --sums-sha H --res R    (§3.3)
    $PY  -X utf8 -I -B scripts/c_diag/c_diag_score.py score --pull P --sums SHA256SUMS_main[_stop] --sums-sha H --labels L
         --labels-sha H --cider R/cider_vi.json --cider-sha H --res R                 (S4: §3.3, §4.4, §5.3, §6)
Pulled host files are opened only by (path, sha) from the pulled SUMS file, whose own sha is an argument (the tier-1
records() form; listed as a reading in READINGS.md). Every number carries LABEL; no caption, demonstration or label
text is printed. §4.5 is not here: it is c_diag_t1table.py.
"""
from __future__ import annotations

import argparse
import calendar
import json
import os
import re
import sys
import time
import unicodedata
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(os.path.abspath(__file__)).parent  # unresolved: the mutant suite runs scratch copies
sys.path.insert(0, str(HERE))
import c_diag as D  # noqa: E402
import c_diag_gpu as H  # noqa: E402  arm masks (filt_masks, ctl_masks): the host's own functions, reused

B_REPS, ALPHA = 10_000, 0.05  # §6.1, §6.3
SEED_GATE, SEED_BOOT, SEED_PERM = 20261109, 20261108, 20261110  # §4.2, §6.1, §6.1 [W4]
SESOI_P, DELTA_C, DELTA_R, FLAG_PTS, EMPTY_FLAG = 2.0, 2.0, 2.0, 5.0, 0.05  # §6.2, §3.3
V = {"k_pt": 0.40, "k_lo": 0.20, "no_p": 0.40, "no_a": 0.40, "sup_p": 0.50, "unc": 0.20, "blind": 0.20}  # §4.3
GUARDS = ("GF", "GC", "GB")
P_STATES = ("GF", "GC", "GB", "UP", "UPs", "DOWN", "NS")
LABELS = {  # §6.4 summary label text (verbatim)
    "S1": "filtering raised object precision beyond count-matched removal",
    "S2": "precision rose; a recall or CIDEr-VI cost is not excluded",
    "S3": "precision rose; not shown beyond count-matched removal",
    "S3c": "precision rose; not shown beyond count-matched removal; a recall or CIDEr-VI cost is not excluded",
    "S4": "precision rose (x [CI]); a rise of SESOI_P is not shown",
    "S4c": "precision rose (x [CI]); a rise of SESOI_P is not shown; a recall or CIDEr-VI cost is not excluded",
    "S5": "filtering lowered object precision", "S6": "no change in object precision shown"}
GUARD_TEXT = {"GF": "VI-script guard FAIL (filt)", "GC": "VI-script guard FAIL (comparator)",
              "GB": "VI-script guard FAIL (filt); VI-script guard FAIL (comparator)"}  # S0: guard label(s), verbatim
NB4 = ("NB-4: ctl matches counts, not tokens, and can remove obj propositions beyond CAP = 32 that filt cannot "
       "reach; see verifier.cap_hits")
XM, OV = "xm_test2500", "ov_dev_b"
XM_VI_FULL = "101d24ad98e9dec43625ee425fa1b49aa1bde98f9609945bf5dd4424fef1dacc"  # §2.4 W5 release_sha256


class BlockFault(Exception):
    """§6.1 / §8.4: > 1 % undefined replicates; final for that block (a data-degeneracy FAULT)."""


# ---------------------------------------------------------------------------------------------- inputs
def pulled(pull: Path, name: str, h: str) -> dict:
    """{rel: sha} of the pulled SUMS file; its own sha must be the argument. These become allow-list entries."""
    p = pull / name
    b = p.read_bytes()
    if D.sha(b) != h:
        D.fault(f"{name} differs from --sums-sha")
    out = {}
    for x in b.decode().splitlines():
        hh, _, rel = x.partition("  ")
        if not re.fullmatch(r"[0-9a-f]{64}", hh) or not rel or rel in out or ".." in rel.split("/") or \
                rel.startswith("/"):  # CC-307 N2: an absolute path would discard the pull dir
            D.fault(f"{name}: malformed or repeated line")
        out[rel] = hh
    return out


def setup(a, cmd: str, extra: dict | None = None) -> tuple[dict, D.S0]:
    sums = {}
    allow = dict(extra or {})
    if getattr(a, "labels", None):
        allow[a.labels] = a.labels_sha
    allow[str(Path(a.pull) / a.sums)] = a.sums_sha
    D.GUARD.add(Path(a.pull) / a.sums, a.sums_sha)
    D.GUARD.install()
    sums = pulled(Path(a.pull), a.sums, a.sums_sha)
    allow.update({str(Path(a.pull) / r): h for r, h in sums.items()})
    keys = {"gate": D.SUBCMD["gate-sample"], "cider": ("lists", "xm_refs", "ov_refs") + tuple(
        k for k in D.B if k.startswith("pred|")), "score": D.SUBCMD["manifest"]}[cmd]
    D.SUBCMD[f"score:{cmd}"] = keys
    D.allow(f"score:{cmd}", allow, [a.res])
    return sums, D.S0(Path(a.labels) if getattr(a, "labels", None) else None)


def jpull(a, sums: dict, rel: str):
    if rel not in sums:
        return None
    return json.loads((Path(a.pull) / rel).read_text("utf-8"))


def jsonl(a, sums: dict, rel: str, key: str) -> dict | None:
    if rel not in sums:
        return None
    b = (Path(a.pull) / rel).read_bytes()
    if b and not b.endswith(b"\n"):
        D.fault(f"{rel}: torn last line")
    out = {}
    for x in b.decode("utf-8").splitlines():
        r = json.loads(x)
        if r[key] in out:
            D.fault(f"{rel}: repeated {key}")
        out[r[key]] = r
    return out


# ---------------------------------------------------------------------------------------------- statistics
def kappa(a, b, c, d):
    """§4.2: Cohen's κ on {REJECTED, SUPPORTED} x {absent, present}; a = R-absent, b = R-present, c = S-absent,
    d = S-present. Undefined (nan) when a row or column is empty or p_e = 1."""
    a, b, c, d = (np.asarray(x, float) for x in (a, b, c, d))
    n = a + b + c + d
    with np.errstate(divide="ignore", invalid="ignore"):
        pe = ((a + b) * (a + c) + (c + d) * (b + d)) / n ** 2
        k = ((a + d) / n - pe) / (1 - pe)
    empty = (a + b == 0) | (c + d == 0) | (a + c == 0) | (b + d == 0) | (pe >= 1)
    return np.where(empty, np.nan, k)


def wmat(idx: np.ndarray, n: int) -> np.ndarray:
    """Per-replicate resample counts (B x n), so replicate sums are W @ column (exact integers)."""
    W = np.zeros((idx.shape[0], n), np.int32)
    for r in range(idx.shape[0]):
        W[r] = np.bincount(idx[r], minlength=n)
    return W


class Boot:
    """Columns (one value per image, rows in sorted id order) -> point sums and replicate sums (one W per set)."""

    def __init__(self, cols: dict, W: np.ndarray):
        self.k = {name: j for j, name in enumerate(cols)}
        R = np.column_stack([np.asarray(v, float) for v in cols.values()])
        self.pt, self.T = R.sum(0), W @ R

    def __call__(self, name):
        return self.pt[self.k[name]], self.T[:, self.k[name]]


def est(get, fn, strict: bool = True) -> dict:
    """fn(S), S(name) -> sums. Percentile 95 % CI (2.5 / 97.5) from the replicates; undefined replicates dropped and
    counted; > 1 % = BlockFault (§6.1), unless strict=False (descriptive odds rows, flagged)."""
    with np.errstate(divide="ignore", invalid="ignore"):
        pt = float(fn(lambda k: get(k)[0]))
        reps = np.asarray(fn(lambda k: get(k)[1]), float)
    ok = np.isfinite(reps)
    if strict and (~ok).sum() > 0.01 * len(reps):
        raise BlockFault(f"{int((~ok).sum())} undefined replicates (> 1 %)")
    out = {"point": pt if np.isfinite(pt) else None, "dropped": int((~ok).sum()),
           "ci": [float(np.percentile(reps[ok], 2.5)), float(np.percentile(reps[ok], 97.5))] if ok.any() else None}
    if (~ok).sum() > 0.01 * len(reps):
        out["note"] = "> 1 % undefined replicates; descriptive"
    return out


def perm_p(hp_a, hm_a, hp_b, hm_b, swaps: np.ndarray) -> float:
    """§6.1 [W4, R1]: per image independently, with probability 1/2, the two arms' (present, absent) counts swap;
    p = (1 + #{|Δ_perm| >= |Δ̂|}) / (R + 1), two-sided, floor 1/(R + 1). H0 (R1): the joint distribution of the per-image
    count pairs is invariant under every swap pattern (images independent, arms exchangeable within an image)."""
    hp_a, hm_a, hp_b, hm_b = (np.asarray(x, np.int64) for x in (hp_a, hm_a, hp_b, hm_b))
    dp, dm = swaps @ (hp_b - hp_a), swaps @ (hm_b - hm_a)
    pa, ma, pb, mb = hp_a.sum() + dp, hm_a.sum() + dm, hp_b.sum() - dp, hm_b.sum() - dm
    with np.errstate(divide="ignore", invalid="ignore"):
        d = 100 * pa / (pa + ma) - 100 * pb / (pb + mb)
    d0 = 100 * hp_a.sum() / (hp_a.sum() + hm_a.sum()) - 100 * hp_b.sum() / (hp_b.sum() + hm_b.sum())
    return float((1 + int((np.abs(d) >= abs(d0) - 1e-9).sum())) / (len(swaps) + 1))


def holm(ps: dict) -> dict:
    """§6.3: Holm step-down at α = 0.05 over the family {name: p}; m = len(ps). -> {name: (reject, adjusted p)}."""
    order = sorted(ps, key=lambda k: (ps[k], k))
    m, out, run, stopped = len(ps), {}, 0.0, False
    for j, k in enumerate(order):
        run = max(run, min(1.0, (m - j) * ps[k]))
        stopped = stopped or ps[k] > ALPHA / (m - j)
        out[k] = (not stopped, run)
    return out


# ---------------------------------------------------------------------------------------------- Appendix D
def p_state(guard: str, reject: bool, point: float, lo: float, hi: float) -> str:
    """§6.4 per-contrast P_obj state, first matching row (D.1)."""
    if guard in GUARDS:
        return guard
    if reject and point >= SESOI_P and lo > 0:
        return "UP"
    if reject and point > 0 and lo > 0:
        return "UPs"
    if reject and point < 0 and hi < 0:
        return "DOWN"
    return "NS"


def summary(fr: str, fc: str, r_ok: bool, c_ok: bool) -> str:
    """§6.4 backbone summary label on XM-test2500 (D.2)."""
    if fr in GUARDS:
        return "S0"
    if fr == "DOWN":
        return "S5"
    if fr == "NS":
        return "S6"
    ok = r_ok and c_ok
    if fr == "UPs":
        return "S4" if ok else "S4c"
    if fc in ("UP", "UPs"):
        return "S1" if ok else "S2"
    return "S3" if ok else "S3c"


def harm_state(lo: float, hi: float, delta: float, prefix: str) -> str:
    """§6.4 C1-C4 (CIDEr-VI, δ_C) / R1-R4 (R_obj^VI, δ_R) on the CI of filt - comparator."""
    return prefix + ("1" if hi < 0 and lo <= -delta else "2" if hi < 0 else "3" if lo <= -delta else "4")


def guard_of(vi: dict, a: str, b: str) -> str:
    """GF: filt's VI-script share < 0.95; GC: the comparator's; GB: both (both labels printed, CC-298 Ruling 3)."""
    fa, fb = vi[a] < D.VI_GUARD, vi[b] < D.VI_GUARD
    return "GB" if fa and fb else "GF" if fa else "GC" if fb else "OK"


# ---------------------------------------------------------------------------------------------- gate (§4.2-4.3)
def gate_table(units: list[dict], status: list[dict], rows: dict) -> dict:
    """One verifier's §4.2 measures: N_P / N_A denominators include UNCERTAIN and parse failures; κ on R / S only."""
    st = {s["u"]: s["status"] for s in status}
    n = Counter()
    for u in units:
        r = rows[u["u"]]
        s = st[u["u"]]
        n[s] += 1
        n[f"{r['label']}|{s}"] += 1
        n[f"blind:{r['blind_label']}|{s}"] += 1
        n["parse_fail"] += r["parse_fail"]
        n["blind_parse_fail"] += r["blind_parse_fail"]
    NP, NA = n["present"], n["absent"]
    k = float(kappa(n["REJECTED|absent"], n["REJECTED|present"], n["SUPPORTED|absent"], n["SUPPORTED|present"]))
    kb = float(kappa(*(n[f"blind:{x}"] for x in ("REJECTED|absent", "REJECTED|present", "SUPPORTED|absent",
                                                    "SUPPORTED|present"))))
    return {"N_P": NP, "N_A": NA, "no_rate_present": n["REJECTED|present"] / NP, "no_rate_absent": n["REJECTED|absent"] / NA,
            "supported_share_present": n["SUPPORTED|present"] / NP,
            "uncertain_share": (n["UNCERTAIN|present"] + n["UNCERTAIN|absent"]) / (NP + NA),
            "parse_fail": n["parse_fail"], "blind_parse_fail": n["blind_parse_fail"],
            "kappa": None if np.isnan(k) else k, "kappa_blind": None if np.isnan(kb) else kb,
            "kappa_excluded_uncertain": n["UNCERTAIN|present"] + n["UNCERTAIN|absent"],
            "cells": {x: n[x] for x in sorted(n) if "|" in x}}


def kappa_ci(units: list[dict], status: list[dict], rows: dict) -> dict:
    """§4.2 κ CI: percentile bootstrap over query clusters, B = 10,000, default_rng(20261109), idx over the sorted
    n_q gate queries with >= 1 unit [NB-1]; undefined replicates dropped and counted; > 1 % = gate FAULT."""
    st = {s["u"]: s["status"] for s in status}
    qs = sorted({u["qid"] for u in units})
    Q = np.zeros((len(qs), 4))
    pos = {q: i for i, q in enumerate(qs)}
    cell = {("REJECTED", "absent"): 0, ("REJECTED", "present"): 1, ("SUPPORTED", "absent"): 2, ("SUPPORTED", "present"): 3}
    for u in units:
        j = cell.get((rows[u["u"]]["label"], st[u["u"]]))
        if j is not None:
            Q[pos[u["qid"]], j] += 1
    rng = np.random.default_rng(SEED_GATE)
    idx = rng.integers(0, len(qs), size=(B_REPS, len(qs)))
    T = wmat(idx, len(qs)) @ Q
    reps = kappa(*T.T)
    ok = np.isfinite(reps)
    out = {"n_q": len(qs), "dropped": int((~ok).sum()),
           "ci": [float(np.percentile(reps[ok], 2.5)), float(np.percentile(reps[ok], 97.5))] if ok.any() else None}
    out["fault"] = bool((~ok).sum() > 0.01 * B_REPS)
    return out


def verdict(t: dict, ci: dict) -> dict:
    """§4.3 PASS rule, all five; undefined κ = V1 FAIL; undefined κ_blind = 0 for V5; V2-V5 on point values."""
    if ci["fault"]:
        return {"status": "gate FAULT (degenerate κ)", "pass": False}
    k = t["kappa"]
    vs = {"V1": k is not None and k >= V["k_pt"] and ci["ci"] is not None and ci["ci"][0] >= V["k_lo"],
          "V2": t["no_rate_present"] <= V["no_p"] and t["no_rate_absent"] >= V["no_a"],
          "V3": t["supported_share_present"] >= V["sup_p"],
          "V4": t["uncertain_share"] <= V["unc"],
          "V5": k is not None and k - (t["kappa_blind"] if t["kappa_blind"] is not None else 0.0) >= V["blind"]}
    return {"status": "PASS" if all(vs.values()) else "FAIL", "pass": all(vs.values()), **vs}


def cmd_gate(a) -> dict:
    sums, s = setup(a, "gate")
    lad = D.ladder(D.gate_units(s))
    if "fault" in lad:
        D.fault(lad["fault"])
    units = D.host_units(lad["units"])
    if D.sha(D.dump(units)) != a.gate_sha:
        D.fault("the recomputed gate sample differs from --gate-sha (the Stage-0 gate_units.json)")
    status = [{"u": n, "status": x["status"]} for n, x in enumerate(lad["units"])]
    gate_only = a.sums.startswith("SHA256SUMS_gate-only")
    rec = {"label": D.LABEL, "branch": "gate-only" if gate_only else "main", "rung": lad["rung"], "supply": lad["supply"],
           "gate_sha256": a.gate_sha, "sums": a.sums, "verifiers": {}}
    if gate_only:  # R2-W1 (d): the host is deleted after the pull and before the verdict is computed
        log = (Path(a.pull) / "logs/job.log").read_text("utf-8") if "logs/job.log" in sums else ""
        end = [x[:20] for x in log.splitlines() if " JOB DONE gate-only" in x or " CAP STOP " in x]
        if not a.deleted_utc or not end or calendar.timegm(time.strptime(a.deleted_utc, "%Y-%m-%dT%H:%M:%SZ")) < \
                calendar.timegm(time.strptime(end[-1], "%Y-%m-%dT%H:%M:%SZ")):
            D.fault("gate-only branch: --deleted-utc (the logged machine delete, after the gate pull) is required "
                    "before the verdict (R2-W1 (d))")
        rec["deleted_utc"] = a.deleted_utc
    stop = a.sums.endswith("_stop")
    for m in D.BACKBONES:
        rows = jsonl(a, sums, f"out/gate.{m}.jsonl", "u")
        if stop or rows is None or set(rows) != {u["u"] for u in units}:
            rec["verifiers"][m] = {"status": "incomplete"}  # §8.4 / R3: no partial number
            continue
        t, ci = gate_table(units, status, rows), kappa_ci(units, status, rows)
        rec["verifiers"][m] = {**t, "kappa_ci": ci, **verdict(t, ci)}
    if gate_only and any(v["status"] == "incomplete" for v in rec["verifiers"].values()):  # R3 [J1 N-7]
        rec["verifiers"] = {m: {"status": "incomplete (gate-only branch: whole branch incomplete, R3)"} for m in D.BACKBONES}
    rec["pass"] = [m for m, v in rec["verifiers"].items() if v.get("pass")]
    h = D.write_new(Path(a.res) / "gate_verdict.json", rec)
    D.say({"step": "gate", "verdict_sha256": h, "pass": rec["pass"],
           "status": {m: v["status"] for m, v in rec["verifiers"].items()},
           "VERDICT.json": None if gate_only else {"pass": rec["pass"], "verdict_sha256": h}})
    return rec


# ---------------------------------------------------------------------------------------------- CIDEr-VI (§3.3)
def cv_mod():
    if "c_pvr_cider_vi" not in sys.modules:
        rel = "scripts/c_pvr/c_pvr_cider_vi.py"
        if D.sha((D.ROOT / rel).read_bytes()) != D.CODE[rel]:
            D.fault(f"{rel} differs from its pin 3401b46c")
        import importlib.util
        spec = importlib.util.spec_from_file_location("c_pvr_cider_vi", D.ROOT / rel)
        m = sys.modules["c_pvr_cider_vi"] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        m.load(D.ROOT)  # c_pvr_gpu, c_pvr, kit protocol_pilot + punctuation_audit behind their pins (pin §2)
    return sys.modules["c_pvr_cider_vi"]


def references(s: D.S0) -> dict:
    """§2.4: XM-test2500 from the pre-filtered staging file only (2,500 keys, release 101d24ad); OV-dev-B from the dev
    file, OV-dev-A parsed and dropped. Read as ctest.references_t / stage2.references2."""
    xm = json.loads(D.path("xm_refs").read_text("utf-8"))
    ids = {r[0] for r in s.rows(XM)}
    if xm.get("release_sha256") != XM_VI_FULL or {str(i["id"]) for i in xm["images"]} != ids:
        D.fault("xm_test2500_data.json: not the 2,500 XM-test2500 keys of release 101d24ad (§2.4 W5)")
    out = {XM: {}}
    for x in xm["annotations"]:
        out[XM].setdefault(str(x["image_id"]), []).append(x["caption"])
    ov = json.loads(D.path("ov_refs").read_text("utf-8"))
    ob = {r[0] for r in s.rows(OV)}
    if set(ov) != {r[0] for r in s.lists["sets"]["ov_dev_a"]} | ob:
        D.fault("uit-openviic-annotation-dev.json: not the 1,836-key OV-dev-A ∪ OV-dev-B file")
    out[OV] = {f: [c.strip() for c in ov[f]["captions"]] for f in sorted(ob)}
    del ov
    if set(out[XM]) != ids:
        D.fault("an XM-test2500 image has no reference")
    return out


def complete_block(sums: dict, b: str, ds: str) -> bool:
    """§8.4: a block is complete iff every arm's decode file and its texts record are in the pulled SUMS; a partial
    block (cap stop mid-block) is never opened, by cider or score (CC-307 W3)."""
    return all(r in sums for r in [f"out/decode.{b}.{ds}.{arm}.json" for arm in D.ARMS[ds]] + [f"out/texts.{b}.{ds}.json"])


def hyps(a, sums: dict, s: D.S0) -> dict:
    """{set: {run: {id: caption}}}: the arms of complete blocks only, and their CC-212 ret / rand originals (parity)."""
    out = {XM: {}, OV: {}}
    for b in D.BACKBONES:
        for ds in D.ARMS:
            if not complete_block(sums, b, ds):
                continue
            for arm in D.ARMS[ds]:
                d = jpull(a, sums, f"out/decode.{b}.{ds}.{arm}.json")
                if set(d["predictions"]) != {r[0] for r in s.rows(ds)}:
                    D.fault(f"{b} {ds} {arm}: a decode file does not hold exactly the set's ids")
                out[ds][f"{b}|{arm}"] = d["predictions"]
            for arm in ("ret", "rand"):
                out[ds][f"{b}|orig_{arm}"] = D.preds(b, ds, arm)["predictions"]
    return out


def cmd_cider(a) -> dict:
    sums, s = setup(a, "cider")
    CV = cv_mod()
    env = CV.jdk()
    refs, hy = references(s), hyps(a, sums, s)
    texts = [t for ds in refs for rs in refs[ds].values() for t in rs] + [t for ds in hy for h in hy[ds].values()
                                                                           for t in h.values()]
    seg = dict(zip(texts, CV.tok(texts)))
    W, S = {}, {}
    for ds in refs:
        W[ds], S[ds] = CV.cider({i: [seg[r] for r in rs] for i, rs in refs[ds].items()},
                                {k: {i: seg[c] for i, c in h.items()} for k, h in hy[ds].items()})
    CV.in_range(W)
    CV.in_range(S)
    res = Path(a.res)
    rec = {"label": D.LABEL, "route": "CIDER_VI_PIN_v1_1 §2-§6 via c_pvr_cider_vi.tok / cider (3401b46c)", "jdk": env,
           "as_written": D.write_new(res / "cider_vi.json", {"label": D.LABEL, "as_written": W, "stripped": S}),
           "n": {ds: len(refs[ds]) for ds in refs}, "runs": {ds: sorted(hy[ds]) for ds in hy}}
    D.write_new(res / "cider_vi_record.json", rec)
    D.say({"step": "cider", "cider_sha256": rec["as_written"], "runs": rec["runs"]})
    return rec


# ---------------------------------------------------------------------------------------------- S4 score
def ordered(text: str, chair, keys) -> list[str]:
    """Distinct matched classes in order of first mention (ΔP_cm, supplement l.762)."""
    return [c for c in dict.fromkeys(chair.objects_in(text, raw_tone=False)) if c in keys]


def pcm(of: list[str], orr: list[str], sti: dict) -> tuple[int, int, int]:
    """[N20] count-matched precision (supplement l.762, `ret` in place of `zs`): k = min(|M(filt)|, |M(ret)|); tp =
    present among the first k classes of each caption, against the OI labels. -> (tp_filt, tp_ret, k)."""
    k = min(len(of), len(orr))
    return sum(sti.get(c) == "present" for c in of[:k]), sum(sti.get(c) == "present" for c in orr[:k]), k


def survival(dcs: list[dict], masks, mention) -> list[tuple[set, set]]:
    """T1-REP v4 §2 'removed' (the c_pvr_score.survival form): unit (d, c) survives iff c is still found in
    rebuild(d, mask); an emptied demonstration keeps nothing. -> [(units, kept)] per demonstration."""
    out = []
    for n, dc in enumerate(dcs):
        units = D.obj_units(dc, mention)
        t = dc["text"] if masks is None else D.CP.rebuild(dc, masks[n])
        out.append((units, units & (set() if t is None else set(mention(t)))))
    return out


def text_cols(caps: dict, ids: list, st: dict | None, mention, chair, keys) -> dict:
    cols = {k: [] for k in ("Hp", "Hm", "n", "vi", "empty", "syl")}
    PS = D.score_mod()
    for i in ids:
        c = caps[i]
        m = mention(c)
        s = (st or {}).get(i, {})
        cols["Hp"].append(sum(s.get(x) == "present" for x in m))
        cols["Hm"].append(sum(s.get(x) == "absent" for x in m))
        cols["n"].append(len(m))
        cols["vi"].append(int(bool(PS.VI_SPECIFIC.search(unicodedata.normalize("NFC", c).lower()))))
        cols["empty"].append(int(not c.strip()))
        cols["syl"].append(len(PS.tokens(c)))
    return cols


def block_xm(b: str, R: dict, Wx: np.ndarray, swaps, st: dict, s: D.S0, verify: dict, cider: dict, ids: list,
             mention, chair, keys) -> dict:
    """XM-test2500 numbers of one backbone (§3.3, §4.4, §6.4-6.5)."""
    arms = list(D.ARMS[XM])
    tc = {a: text_cols(R[a], ids, st, mention, chair, keys) for a in arms + ["orig_ret", "orig_rand"]}
    cols = {"one": [1] * len(ids), "Ppairs": [sum(v == "present" for v in st.get(i, {}).values()) for i in ids]}
    for a, t in tc.items():
        for k, v in t.items():
            cols[f"{k}|{a}"] = v
        for kind in ("as_written", "stripped"):
            cols[f"C{kind[0]}|{a}"] = [cider[kind][XM][f"{b}|{a}"][i] for i in ids]
    # ΔP_cm (N20) and the verifier / in-situ columns (§4.4)
    dec = s.decomp([XM])
    tp_f, tp_r, kk = [], [], []
    insitu = Counter()
    for i in ids:
        sti = st.get(i, {})
        f, r, k = pcm(ordered(R["filt"][i], chair, keys), ordered(R["ret"][i], chair, keys), sti)
        tp_f.append(f)
        tp_r.append(r)
        kk.append(k)
        cids = s.ranked(XM, i)[:D.BACKBONES[b]["k"]]
        dcs = [dec[("xm3600", c)] for c in cids]
        labels = verify[i]["labels"]
        fm = H.filt_masks(labels)
        cm = H.ctl_masks(i, dcs, fm)
        zc = int(verify[i]["cap_hits"] == 0)
        for tag, masks in (("ret", None), ("filt", fm), ("ctl", cm)):
            sv = survival(dcs, masks, mention)
            for kind, s0 in (("Dm", "absent"), ("Dp", "present")):
                v = sum(sti.get(c, "unknown") == s0 for u, kept in sv for c in (u if masks is None else kept))
                cols.setdefault(f"{kind}|{tag}", []).append(v)
                cols.setdefault(f"{kind}|{tag}|zc", []).append(v * zc)
        cols.setdefault("zc", []).append(zc)
        for k2 in ("calls", "cap_hits", "parse_fail"):
            cols.setdefault(f"V|{k2}", []).append(verify[i][k2])
        for dc, lab in zip(dcs, labels):
            for c in D.obj_units(dc, mention):
                j = next(j for j, p in enumerate(dc["props"]) if p["kind"] == "obj" and c in p["classes"])
                if lab[j] == "CAP":
                    insitu["not_asked"] += 1
                    continue
                insitu[f"{lab[j]}|{sti.get(c, 'unknown')}"] += 1
    cols.update({"tpf": tp_f, "tpr": tp_r, "kcm": kk})
    G = Boot(cols, Wx)
    vi = {a: G(f"vi|{a}")[0] / len(ids) for a in tc}
    P = lambda a: lambda S: 100 * S(f"Hp|{a}") / (S(f"Hp|{a}") + S(f"Hm|{a}"))  # noqa: E731
    out = {"arms": {}, "contrasts": {}, "harm": {}}
    for a in tc:
        out["arms"][a] = {
            "P_obj": est(G, P(a)), "P_obj_wrong": est(G, lambda S, a=a: 100 * S(f"Hp|{a}") / S(f"n|{a}")),
            "R_obj": est(G, lambda S, a=a: 100 * S(f"Hp|{a}") / S("Ppairs")),
            "CHAIR_i": est(G, lambda S, a=a: 100 - P(a)(S)),
            "CIDEr_VI": {k: est(G, lambda S, a=a, k=k: S(f"C{k[0]}|{a}") / S("one")) for k in ("as_written", "stripped")},
            "mentions_per_caption": G(f"n|{a}")[0] / len(ids),
            "verifiable_mention_share": 100 * (G(f"Hp|{a}")[0] + G(f"Hm|{a}")[0]) / max(1, G(f"n|{a}")[0]),
            "vi_script_share": vi[a], "empty_share": G(f"empty|{a}")[0] / len(ids),
            "mean_syllables": G(f"syl|{a}")[0] / len(ids)}
        out["arms"][a]["empty_flag"] = out["arms"][a]["empty_share"] > EMPTY_FLAG
    flag = abs(out["arms"]["filt"]["verifiable_mention_share"] - out["arms"]["ret"]["verifiable_mention_share"])
    out["mention_share_flag"] = flag > FLAG_PTS
    for x in ("ret", "ctl", "rand"):  # the Holm family members of this backbone (§6.3)
        e = est(G, lambda S, x=x: P("filt")(S) - P(x)(S))
        p = perm_p(cols["Hp|filt"], cols["Hm|filt"], cols[f"Hp|{x}"], cols[f"Hm|{x}"], swaps)
        out["contrasts"][f"filt-{x}"] = {**e, "p": p, "guard": guard_of(vi, "filt", x)}
    for kind, (cfun, delta, pre) in {"CIDEr_VI": (lambda S, a: S(f"Ca|{a}") / S("one"), DELTA_C, "C"),
                                     "R_obj": (lambda S, a: 100 * S(f"Hp|{a}") / S("Ppairs"), DELTA_R, "R")}.items():
        e = est(G, lambda S: cfun(S, "filt") - cfun(S, "ret"))
        g = guard_of(vi, "filt", "ret")
        out["harm"][kind] = {**e, "state": g if g != "OK" else harm_state(*e["ci"], delta, pre)}
    out["harm"]["C_ok"] = out["harm"]["CIDEr_VI"]["state"] in ("C2", "C4")
    out["harm"]["R_ok"] = out["harm"]["R_obj"]["state"] in ("R2", "R4")
    es = est(G, lambda S: S("Cs|filt") / S("one") - S("Cs|ret") / S("one"))
    g = guard_of(vi, "filt", "ret")
    out["harm"]["CIDEr_VI_stripped"] = {**es, "state": g if g != "OK" else harm_state(*es["ci"], DELTA_C, "C")}
    out["harm"]["CIDEr_VI"]["punctuation_dependent"] = out["harm"]["CIDEr_VI_stripped"]["state"] != \
        out["harm"]["CIDEr_VI"]["state"]  # §3.3: the as-written state carries the flag
    out["contrasts"]["filt-ctl"]["disclosure"] = NB4
    out["dP_cm"] = est(G, lambda S: 100 * (S("tpf") - S("tpr")) / S("kcm"))
    out["parity"] = {a: {"P_obj": est(G, lambda S, a=a: P(a)(S) - P(f"orig_{a}")(S)),
                         "CIDEr_VI": est(G, lambda S, a=a: S(f"Ca|{a}") / S("one") - S(f"Ca|orig_{a}") / S("one"))}
                     for a in ("ret", "rand")}
    out["insitu"] = insitu_table(insitu, G)
    out["verifier"] = {k: int(G(f"V|{k}")[0]) for k in ("calls", "cap_hits", "parse_fail")}
    out["verifier"]["cap_hit_images"] = len(ids) - int(G("zc")[0])
    out["verifier"]["parse_fail_share"] = out["verifier"]["parse_fail"] / max(1, out["verifier"]["calls"])
    return out


def insitu_table(cells: Counter, G: Boot) -> dict:
    """§4.4: the T1-REP v4 §1 3 x 3 table (with unknown) over every obj unit asked, the §4.2 measures (descriptive),
    and the T1-REP v4 §2 odds identity with image-bootstrap CIs, on all images and on zero-cap-hit images [R2-W10 (d)]."""
    c = lambda lab, s: cells[f"{lab}|{s}"]  # noqa: E731
    npr = sum(c(x, "present") for x in ("SUPPORTED", "UNCERTAIN", "REJECTED"))
    nab = sum(c(x, "absent") for x in ("SUPPORTED", "UNCERTAIN", "REJECTED"))
    k = kappa(c("REJECTED", "absent"), c("REJECTED", "present"), c("SUPPORTED", "absent"), c("SUPPORTED", "present"))
    out = {"cells": {x: cells[x] for x in sorted(cells)}, "kappa": None if np.isnan(k) else float(k),
           "no_rate_present": c("REJECTED", "present") / npr if npr else None,
           "no_rate_absent": c("REJECTED", "absent") / nab if nab else None,
           "supported_share_present": c("SUPPORTED", "present") / npr if npr else None, "odds": {}}
    for z in ("", "|zc"):
        o = {}
        for a in ("filt", "ctl"):
            o[a] = {"rho": est(G, lambda S, a=a: 1 - S(f"Dm|{a}{z}") / S(f"Dm|ret{z}"), strict=False),
                    "phi": est(G, lambda S, a=a: 1 - S(f"Dp|{a}{z}") / S(f"Dp|ret{z}"), strict=False),
                    "OR": est(G, lambda S, a=a: (S(f"Dm|{a}{z}") / S(f"Dm|ret{z}")) / (S(f"Dp|{a}{z}") / S(f"Dp|ret{z}")),
                              strict=False)}
        orr = lambda a: lambda S: (S(f"Dm|{a}{z}") / S(f"Dm|ret{z}")) / (S(f"Dp|{a}{z}") / S(f"Dp|ret{z}"))  # noqa: E731
        o["OR_filt/OR_ctl"] = est(G, lambda S: orr("filt")(S) / orr("ctl")(S), strict=False)
        out["odds"]["zero_cap_hit_images (exact selectivity ratio)" if z else "all_images"] = o
    return out


def block_ov(b: str, R: dict, Wo: np.ndarray, cider: dict, ids: list, mention, chair, keys) -> dict:
    """OV-dev-B, per backbone: CIDEr-VI per arm and the C1-C4 states of filt - ret and filt - rand (descriptive)."""
    arms = list(D.ARMS[OV])
    tc = {a: text_cols(R[a], ids, None, mention, chair, keys) for a in arms + ["orig_ret", "orig_rand"]}
    cols = {"one": [1] * len(ids)}
    for a, t in tc.items():
        cols[f"vi|{a}"], cols[f"empty|{a}"], cols[f"syl|{a}"] = t["vi"], t["empty"], t["syl"]
        for kind in ("as_written", "stripped"):
            cols[f"C{kind[0]}|{a}"] = [cider[kind][OV][f"{b}|{a}"][i] for i in ids]
    G = Boot(cols, Wo)
    vi = {a: G(f"vi|{a}")[0] / len(ids) for a in tc}
    out = {"arms": {a: {"CIDEr_VI": {k: est(G, lambda S, a=a, k=k: S(f"C{k[0]}|{a}") / S("one"))
                                     for k in ("as_written", "stripped")}, "vi_script_share": vi[a],
                        "empty_share": G(f"empty|{a}")[0] / len(ids), "mean_syllables": G(f"syl|{a}")[0] / len(ids)}
                    for a in tc}, "states": {}}
    for x in ("ret", "rand"):
        e = est(G, lambda S, x=x: S("Ca|filt") / S("one") - S(f"Ca|{x}") / S("one"))
        g = guard_of(vi, "filt", x)
        es = est(G, lambda S, x=x: S("Cs|filt") / S("one") - S(f"Cs|{x}") / S("one"))
        st_w, st_s = (g if g != "OK" else harm_state(*e["ci"], DELTA_C, "C")), (
            g if g != "OK" else harm_state(*es["ci"], DELTA_C, "C"))
        out["states"][f"filt-{x}"] = {**e, "state": st_w, "stripped": {**es, "state": st_s},
                                      "punctuation_dependent": st_w != st_s, "label": "descriptive"}
    out["parity"] = {a: est(G, lambda S, a=a: S(f"Ca|{a}") / S("one") - S(f"Ca|orig_{a}") / S("one"))
                     for a in ("ret", "rand")}
    return out


def arm_counts(a, sums: dict, b: str, ds: str) -> dict:
    """§3.3 / §6.5: fallback share (every demonstration emptied -> zero-shot), emptied-demonstration share, obj
    propositions removed per image, per arm (the host's texts record: ids and counts only)."""
    t = jpull(a, sums, f"out/texts.{b}.{ds}.json")["arms"]
    k = D.BACKBONES[b]["k"]
    return {arm: {"fallback_share": sum(bool(v.get("fallback")) for v in t[arm].values()) / len(t[arm]),
                  "emptied_demo_share": sum(v["emptied"] for v in t[arm].values()) / (k * len(t[arm])),
                  "removed_per_image": sum(v["removed"] for v in t[arm].values()) / len(t[arm])} for arm in t}


def byte_equal(R: dict, orig: dict, computable: bool):
    """§5.3 item 1: share of captions whose sha256 equals CC-212's; 'not computable' under DC2 / NB-6."""
    if not computable:
        return "not computable (CC-212 batch grouping not reconstructed, DC2)"
    return sum(D.sha(R[i].encode()) == D.sha(orig[i].encode()) for i in orig) / len(orig)


def cmd_score(a) -> dict:
    cider_path = Path(a.cider)
    sums, s = setup(a, "score", {str(cider_path): a.cider_sha})
    cider = json.loads(cider_path.read_text("utf-8"))
    st = s.status
    chair, _lex = D.CP.rescap_mods(D.ROOT)
    keys = frozenset(k for k in json.loads(D.path("vi_map").read_text("utf-8")) if not k.startswith("_"))
    mention = D.mention_fn()
    D.CP.raw_tone_unset()  # §3.3: RESCAP_RAW_TONE must be unset
    ids = {ds: sorted(r[0] for r in s.rows(ds)) for ds in D.ARMS}
    R, complete = {}, {}
    for b in D.BACKBONES:
        for ds in D.ARMS:
            complete[(b, ds)] = complete_block(sums, b, ds)  # §8.4: a partial block is never opened
            if complete[(b, ds)]:
                got = {arm: jpull(a, sums, f"out/decode.{b}.{ds}.{arm}.json") for arm in D.ARMS[ds]}
                if any(set(g["predictions"]) != set(ids[ds]) for g in got.values()):
                    D.fault(f"{b} {ds}: a decode file does not hold exactly the set's ids")
                R[(b, ds)] = {arm: g["predictions"] for arm, g in got.items()}
                for arm in ("ret", "rand"):
                    R[(b, ds)][f"orig_{arm}"] = D.preds(b, ds, arm)["predictions"]
    fam = [f"{b}|filt-{x}" for b in D.BACKBONES if complete[(b, XM)] for x in ("ret", "ctl", "rand")]
    m_rec = {"label": D.LABEL, "m": len(fam), "family": fam, "utc": D.utc(),
             "completed_blocks": ["|".join(k) for k, v in complete.items() if v]}
    D.write_new(Path(a.res) / "m_record.json", m_rec)
    D.say({"step": "m record (before any contrast, §6.3)", **m_rec})
    rng = np.random.default_rng(SEED_BOOT)  # §6.1 [N1]: idx_XM first, then idx_OV, one generator
    nx, no = len(ids[XM]), len(ids[OV])  # 2,500 and 925 (D.SETS, pinned by the selftest)
    idx_xm = rng.integers(0, nx, size=(B_REPS, nx))
    idx_ov = rng.integers(0, no, size=(B_REPS, no))
    Wx, Wo = wmat(idx_xm, nx), wmat(idx_ov, no)
    del idx_xm, idx_ov
    swaps = np.random.default_rng(SEED_PERM).integers(0, 2, size=(B_REPS, nx), dtype=np.int64)  # §6.1 [W4]
    vp = D.vi_pre(s)
    out = {"label": D.LABEL, "m": m_rec, "blocks": {}, "family": {}, "labels": {}}
    for b in D.BACKBONES:
        if complete[(b, XM)]:
            verify = jsonl(a, sums, f"out/verify.{b}.{XM}.jsonl", "id")
            try:
                blk = block_xm(b, R[(b, XM)], Wx, swaps, st, s, verify, cider, ids[XM], mention, chair, keys)
            except BlockFault as e:
                blk = {"status": f"FAULT ({e}; final for this block, §8.4)"}
            blk["arm_counts"] = arm_counts(a, sums, b, XM)
            for arm in ("ret", "rand"):
                blk.setdefault("parity", {}).setdefault(arm, {})["byte_equal_share"] = byte_equal(
                    R[(b, XM)][arm], R[(b, XM)][f"orig_{arm}"], vp[f"{b}|{XM}|{arm}"]["byte_equal_computable"])
            out["blocks"][f"{b}|{XM}"] = blk
        else:
            out["blocks"][f"{b}|{XM}"] = {"status": "incomplete (no contrast, no label, §8.4)"}
        if complete[(b, OV)]:
            try:
                blk = block_ov(b, R[(b, OV)], Wo, cider, ids[OV], mention, chair, keys)
            except BlockFault as e:
                blk = {"status": f"FAULT ({e}; final for this block, §8.4)"}
            blk["arm_counts"] = arm_counts(a, sums, b, OV)
            for arm in ("ret", "rand"):  # §5.3 item 1: one share per (backbone, set, arm) (CC-307 W2)
                blk.setdefault("byte_equal_share", {})[arm] = byte_equal(
                    R[(b, OV)][arm], R[(b, OV)][f"orig_{arm}"], vp[f"{b}|{OV}|{arm}"]["byte_equal_computable"])
            out["blocks"][f"{b}|{OV}"] = blk
        else:
            out["blocks"][f"{b}|{OV}"] = {"status": "incomplete (no contrast, no label, §8.4)"}
    ps = {}
    for k in fam:  # a FAULT block keeps its m slots at p = 1 (never a reject)
        b, c = k.split("|")
        blk = out["blocks"][f"{b}|{XM}"]
        ps[k] = blk["contrasts"][c]["p"] if "contrasts" in blk else 1.0
    hm = holm(ps)
    for k in fam:
        b, c = k.split("|")
        blk = out["blocks"][f"{b}|{XM}"]
        if "contrasts" not in blk:
            out["family"][k] = {"state": "FAULT", "holm_reject": False, "holm_p": hm[k][1]}
            continue
        e = blk["contrasts"][c]
        e.update(holm_reject=hm[k][0], holm_p=hm[k][1],
                 state=p_state(e["guard"], hm[k][0], e["point"], e["ci"][0], e["ci"][1]))
        out["family"][k] = {x: e[x] for x in ("point", "ci", "p", "holm_p", "holm_reject", "state")}
    for b in D.BACKBONES:
        blk = out["blocks"][f"{b}|{XM}"]
        if "contrasts" in blk:
            fr, fc = blk["contrasts"]["filt-ret"]["state"], blk["contrasts"]["filt-ctl"]["state"]
            lab = summary(fr, fc, blk["harm"]["R_ok"], blk["harm"]["C_ok"])
            out["labels"][b] = {"label": lab, "text": GUARD_TEXT[fr] if lab == "S0" else LABELS[lab],
                                "filt-rand": blk["contrasts"]["filt-rand"]["state"],
                                "beside": {"R_obj": blk["harm"]["R_obj"]["state"],
                                           "CIDEr_VI": blk["harm"]["CIDEr_VI"]["state"],
                                           "OV_dev_B": out["blocks"][f"{b}|{OV}"].get("states", {})}}
    h = D.write_new(Path(a.res) / "score.json", out)
    D.say({"step": "score", "score_sha256": h, "m": len(fam), "labels": {b: v["label"] for b, v in out["labels"].items()}})
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for c in ("gate", "cider", "score"):
        p = sub.add_parser(c)
        p.add_argument("--pull", required=True)
        p.add_argument("--sums", required=True)
        p.add_argument("--sums-sha", required=True)
        p.add_argument("--res", required=True)
        p.add_argument("--labels")
        p.add_argument("--labels-sha")
        p.add_argument("--gate-sha")
        p.add_argument("--deleted-utc")
        p.add_argument("--cider")
        p.add_argument("--cider-sha")
    a = ap.parse_args()
    D.load()
    D.score_mod()  # imported before the hook (VI_SPECIFIC, tokens)
    if a.cmd == "cider":
        cv_mod()
    {"gate": cmd_gate, "cider": cmd_cider, "score": cmd_score}[a.cmd](a)
    D.GUARD.done()


if __name__ == "__main__":
    main()
