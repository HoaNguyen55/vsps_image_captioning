#!/usr/bin/env python3
"""C-PVR-T1 laptop scorer for the S16 result read (Paper C; S11 v1.3 §15; CC-270 N14; plan S10 / S16). Round 3 of
the CC-293 code read (CC-293r2 NEXT_ROUND 82; readings and hunk map in SCORE_READINGS.md); not GO until that read.
It computes, from the pulled tier-1 outputs, in this order:
  1. the prereg v1.2 (8282874) registered numbers: P_obj^VI, the primary PVR − A8 contrast, the §5.2 Holm family,
     and the §12 decisions (SESOI_P, headroom, the §6.3 variant as amended by T1-GUARD v3 (f5c6741), go / stop),
     with the §5.5 bootstrap (unit = image, paired, B = 10,000, percentile 95 %, seed 20261102, e2b.py boot form);
  2. the T1-REP v4 (0e9793f3, 4124ef3) reports: §1 verifier table, §2 odds identity, §4 A0 contrasts and the HW-*
     headline, §5 'cây' sensitivity (c_pvr_cay.py), §6 descriptives, §7 base rates;
  3. after 1-2 are written, C-M1 / C-M2 of T1-ANALYSIS v1.1 (59b6eae5, f5cc716) through c_pvr_cm.py.

    PY=~/.venvs/c_pvr/bin/python       (numpy 2.5.4, CPython 3.12: T1-ANALYSIS §2.1, §6)
    $PY -I -B scripts/c_pvr/c_pvr_score.py selftest              synthetic worlds in a temp dir; no data is opened
    $PY -I -B scripts/c_pvr/c_pvr_score.py score --tier 1 --out $PULL/final/c_pvr_out --sums SHA256SUMS_tier1
        --build $O --tman $TMAN --cap CAP.json --a1-decomp $W/a1_decomp --res DIR
        (--cider F --cider-sha H | --no-cider REASON) [--emb SET=QNPZ,DNPZ ...] [--no-segment] [--rerun-of OPS-id]
    The command name is a stated Q-SPLIT extension (CC-293 Ruling 5): prereg §11 / T1-ANALYSIS §1 say c_pvr.py,
    PINS-A §12 says c_pvr_run.py; both are pinned in the running host's H, so this third file carries it.

Inputs are opened only by `score`. Every pulled jsonl is checked against the pulled SHA256SUMS, the manifests against
TMAN (c_pvr_watch.query_ids form), the gold and code against their pins. c_pvr.py, c_pvr_run.py, c_pvr_gpu.py and
xm3600_oiv7.py are imported unchanged behind their shas (Q-SPLIT (i)-(ii)); no shared constant has a second value.
No caption, demonstration or label text is printed; the records hold numbers, ids and the fixed sentences only.
Every output carries LABEL and "dev, in-sample (XM3600-vi)". Tier 1 has no PASS.
A FAULT is a SystemExit and stops the whole run (C-M2 too). This is accepted (CC-293 Ruling 9, N12): the only
T1-REP §2 FAULT, the c′ identity, is exact on integers (Fractions) and cannot fire; the other FAULTs are integrity
FAULTs that void every number. Integrity FAULTs fire before any output is written.
"""
from __future__ import annotations

import argparse
import functools
import hashlib
import importlib.util
import json
import math
import os
import re
import sys
import tempfile
import time
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
CODE = {  # imported only after these match; c_pvr_gpu.load() then checks c_pvr.py a503644a and c_pvr_run.py 0c80ee68
    "scripts/c_pvr_gpu/c_pvr_gpu.py": "9a9c6eb57ee09575a1c69604fa48c506fe8c64d747754b6f8d9c1ced12a1a260",
    "scripts/c_pvr_gpu/c_pvr_manifest.py": "bb7c6c9a34f857a29e57d99bd71cc2c428246c7730b1f66c3f516213f32b96bb",
    "scripts/xm3600_oiv7.py": "9a79403f4fc38609282d40082ab7f878133edca8aff9e0dc2462db467b7193f0",
    "scripts/c_pvr/c_pvr_cay.py": "129ae59d6f548dfd0283268416d4fed094b7bd6a27818e9b01218b944edac113",
    "scripts/c_pvr/c_pvr_cm.py": "b119b098c0d7885e5bb8cfc8e1a18ef031ef64c8ff933376ebbbb49f7e5ae765",
    "scripts/c_pvr/gates.py": "3bced05e7f718377b34837cfb3f6d6539fb8aafc28bc5f8818e5d7be4ccdf897",  # WANT_B (N6)
}
GOLD = {"labels": ("data/xm3600/oiv7_labels.json", "bac3953a511a9793c22e928a29b68ae05dbf9654502abcbe7b64fd9f6d74c8b2"),
        "desc": ("data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv",
                 "84a4373a0efb7fd6d93fe19b0e7ceb6c1b855c233d13b9b78a9a33655c9fdce3")}  # prereg §2.3
APPENDIX = ("manuscript/prereg/2026-11-02_c_pvr_tier1/T1_ANALYSIS_APPENDIX_v1_1.md",
            "59b6eae5ea6c105fe0f78677a6bec1becad7ee7c48f6d075545bd17ff53e5634")  # §9.4: any other sha = POST_HOC
G = CP = XO = CAY = CM = GT = None

# registered values (prereg v1.2; T1-GUARD v3; S11 v1.3 §10.3; T1-REP v4)
SESOI_FLOOR, SESOI_FRAC, HEADROOM = 1.0, 0.25, 2.0  # §12 (i), (ii); points
DELTA_R, DELTA_C, FLAG_PTS, VI_GUARD = 2.0, 2.0, 5.0, 0.95  # §6.3 / §5.3 δ_R, T1-GUARD δ_C, §5.7 (a), (b)
DEGRADE = 0.5  # S11 v1.3 §10.3: M > 50 % of N decomp_fail on a set = systematic -> that set's A8 / S2 DEGRADED
VARIANTS = ("PVR-drop", "PVR-keep")
FAMILY = ("A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A9", "A10", "A11")  # §5.2: A12 and cut arms out
XM = "xm3600_vi"
GUARD_SETS = ("ktvic_explore", "openviic_explore")  # T1-GUARD G1, strata drawn in this order from one generator
DEMO_ARMS = ("A1", "A7", "PVR-drop", "PVR-keep")
DEV = "dev, in-sample (XM3600-vi)"


def fault(msg: str):
    raise SystemExit(f"FAULT: {msg}")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def load(root: Path = ROOT) -> None:
    global G, CP, XO, CAY, CM, GT
    for rel, h in CODE.items():
        if sha((root / rel).read_bytes()) != h:
            fault(f"{rel} differs from its pin {h[:8]} (Q-SPLIT (ii)); nothing is imported")
    sys.path.insert(0, str(root / "scripts/c_pvr_gpu"))
    import c_pvr_gpu as G  # noqa: E402  SETS, arms, OUT_KEYS, guard, norm_ids; load() pins c_pvr and c_pvr_run
    G.load(root)
    CP = G.CP
    spec = importlib.util.spec_from_file_location("xm3600_oiv7", root / "scripts/xm3600_oiv7.py")
    XO = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(XO)  # resolve_map / status / statuses (prereg §2.1); its MAP is CP's pinned vi_map
    import c_pvr_cay as CAY  # noqa: E402  (scripts/c_pvr is on sys.path after G.load)
    import c_pvr_cm as CM  # noqa: E402
    import gates as GT  # noqa: E402  stdlib-only at import; WANT_B = the committed manifest targets (l.728-733)
    if CM.SEED != CP.BOOT_SEEDS[0]:  # Q-SPLIT (i): one bootstrap seed (prereg §5.5)
        fault("c_pvr_cm.SEED differs from c_pvr.BOOT_SEEDS[0]")


def safe(p) -> Path:
    return CP.refuse(G.guard(p))


def pinned(root: Path, rel: str, h: str) -> bytes:
    b = safe(root / rel).read_bytes()
    if sha(b) != h:
        fault(f"{rel} differs from its pin {h[:8]}")
    return b


# ---------------------------------------------------------------------------------------------- inputs
def manifests(build: Path, tman: str) -> dict:
    """{set: manifest} from the sealed laptop build, each file checked against MANIFEST.sha256 = TMAN."""
    man = safe(build / "MANIFEST.sha256").read_bytes()
    if sha(man) != tman:
        fault("MANIFEST.sha256 differs from --tman")
    want = {p: h for h, p in (x.split("  ", 1) for x in man.decode().splitlines())}
    out = {}
    for s in G.SETS:
        b = safe(build / "manifest" / f"{s}.json").read_bytes()
        if want.get(f"manifest/{s}.json") != sha(b):
            fault(f"manifest/{s}.json differs from MANIFEST.sha256")
        out[s] = json.loads(b)
        if (out[s].get("label"), out[s].get("set")) != (CP.LABEL, s):
            fault(f"manifest/{s}.json label/set mismatch")
    return out


def sums_of(p: Path) -> dict:
    out = {}
    for x in safe(p).read_text().splitlines():
        h, _, rel = x.partition("  ")
        if not re.fullmatch(r"[0-9a-f]{64}", h) or not rel or rel in out:
            fault(f"{p.name}: malformed or repeated line")
        out[rel] = h
    return out


def records(out: Path, sums: dict, s: str, arm: str, ids: set) -> dict | None:
    """One (set, arm) output: sha = the pulled SUMS line, LF-terminated, whitelisted keys, unique ids inside the
    manifest (T1-ANALYSIS §9.1 items 1, 4)."""
    rel = f"out/{s}.{arm}.jsonl"
    p = safe(out / rel)
    if not p.exists():
        if rel in sums:
            fault(f"{rel} is in the SUMS file but absent")
        return None
    b = p.read_bytes()
    if sums.get(rel) != sha(b):
        fault(f"{rel} differs from its SUMS line")
    if b and not b.endswith(b"\n"):
        fault(f"{rel}: torn last line")
    d = {}
    for x in b.decode("utf-8").splitlines():
        r = json.loads(x)
        if set(r) - G.OUT_KEYS or (r.get("set"), r.get("arm")) != (s, arm):
            fault(f"{rel}: a record has other keys or another set / arm")
        if r["id"] in d:
            fault(f"{rel}: image id duplicated")
        d[r["id"]] = r
    if bad := set(d) - ids:
        fault(f"{rel}: {len(bad)} ids are not manifest query ids")
    return d


def a1_degraded(d: Path) -> dict:
    """S11 v1.3 §10.3: {set: (N decomposed, M decomp_fail, DEGRADED)} from W/a1_decomp, sha-checked."""
    man = safe(d / "MANIFEST.sha256").read_text()
    want = {n: h for h, n in (x.split("  ", 1) for x in man.splitlines())}
    out = {}
    for name, h in want.items():
        b = safe(d / name).read_bytes()
        if sha(b) != h:
            fault(f"a1_decomp/{name} differs from its MANIFEST line")
        dec = json.loads(b)
        m = sum("decomp_fail" in x for x in dec.values())
        out[name.removesuffix(".json")] = {"N": len(dec), "M": m, "DEGRADED": m > DEGRADE * len(dec)}
    return out


def gold(root: Path, labels: Path, desc: Path, pins: bool = True) -> dict:
    """{image: {class: present | absent}} by the registered status() rule (prereg §3.1); unknown is omitted."""
    if pins:
        for k, p in (("labels", labels), ("desc", desc)):
            if sha(safe(p).read_bytes()) != GOLD[k][1]:
                fault(f"{p.name} differs from its pin {GOLD[k][1][:8]}")
    CP.pinned(root, "vi_map")
    vmap = XO.resolve_map(safe(desc))
    lab = {k: v for k, v in json.loads(safe(labels).read_text("utf-8")).items() if not k.startswith("_")}
    return XO.statuses(vmap, lab)


def mention_fns(root: Path) -> dict:
    """'' = the scorer of record (objects_in, raw_tone=False, the 69 keys, each class once per caption; prereg §3.1);
    'cay' = the T1-REP §5 sensitivity scorer. Both cached on the text."""
    chair, lexicon = CP.rescap_mods(root)
    keys = frozenset(k for k in json.loads(CP.pinned(root, "vi_map").read_text("utf-8")) if not k.startswith("_"))
    nouns, k = list(lexicon.NOUN_CLASSIFIER), CAY.classifier_set(lexicon.NOUN_CLASSIFIER)

    @functools.lru_cache(maxsize=None)
    def primary(text: str) -> frozenset:
        return frozenset(chair.objects_in(text)) & keys

    @functools.lru_cache(maxsize=None)
    def cay(text: str) -> frozenset:
        return frozenset(CAY.apply(set(primary(text)), text, nouns, k)[0])

    return {"": primary, "cay": cay}


# ---------------------------------------------------------------------------------------------- shared 'removed' helper
def masks_of(arm: str, qid: str, rec: dict) -> list | None:
    """The removal masks an arm applied to A1's top-K demonstrations: PVR-drop / PVR-keep their saved masks; A7 the
    laptop rebuild CP.a7_masks(id, PVR-drop's saved masks), the call and seed the host used (c_pvr_gpu l.581, l.664-666;
    PINS-A §2.7; T1-ANALYSIS §2.1); A1 None (nothing removed). rec = {arm: that image's record}."""
    if arm == "A1":
        return None
    if arm == "A7":
        return CP.a7_masks(qid, rec["PVR-drop"]["masks"])
    return rec[arm]["masks"]


def survival(dcs: list[dict], masks: list | None, mention) -> list[dict]:
    """T1-REP v4 §2 "removed" (l.107-110): a proposition counts as removed iff its mapped mention is no longer in the
    demonstration after span deletion, sentence drop and the dropping of emptied demonstrations, so collateral removals
    count. The unit is (demonstration d, class c), c a map key carried by an object proposition of d, once per
    demonstration (T1-REP §1, T1-ANALYSIS §3). (d, c) survives iff c is in mention(CP.rebuild(d, mask)); an emptied
    demonstration (None) keeps nothing. This is the ONE helper the T1-REP §2 counts and C-M1 both use (CC-292 Ruling
    12, N5; CC-292r2 W3). Per demonstration: units, kept, created (a class in the rebuilt text that was no unit of d,
    expected 0, counted), out (a proposition class that `mention` does not score on the original text: 0 under the
    scorer of record; the 'cây' classes the sensitivity scorer ignores), emptied."""
    out = []
    for n, dc in enumerate(dcs):
        carried = {c for p in dc["props"] if p["kind"] == "obj" for c in p["classes"]}
        units = carried & mention(dc["text"])
        t = dc["text"] if masks is None else CP.rebuild(dc, masks[n])
        found = set() if t is None else set(mention(t))
        out.append({"units": units, "kept": units & found, "created": set() if masks is None else found - units,
                    "out": carried - units, "emptied": t is None})
    return out


def verifier_labels(dcs: list[dict], rd: dict, rk: dict) -> tuple[list[list[str]], bool]:
    """T1-REP §1 needs one verifier label per proposition; the records keep masks and per-image counts only. PVR-drop
    deletes REJECTED ∪ UNCERTAIN and PVR-keep REJECTED (CP.pvr_masks), with one prompt, greedy decoding, one order and
    one cap, so if both runs gave the same answers: REJECTED = keep mask, UNCERTAIN = drop mask and not keep mask,
    else SUPPORTED. ok is False unless keep ⊆ drop, overflow (index >= CAP) is UNCERTAIN, and BOTH records' counts
    equal that reading (yes, no, maybe + parse_fail + cap_hits); a False image voids the table (not a FAULT)."""
    md, mk = sum(rd["masks"], []), sum(rk["masks"], [])
    lab = ["REJECTED" if k else "UNCERTAIN" if d else "SUPPORTED" for d, k in zip(md, mk)]
    want = (lab.count("SUPPORTED"), lab.count("REJECTED"), lab.count("UNCERTAIN"), max(0, len(lab) - CP.CAP))
    ok = (len(md) == len(mk) and not any(k and not d for d, k in zip(md, mk))
          and all(x == "UNCERTAIN" for x in lab[CP.CAP:])
          and all((r["yes"], r["no"], r["maybe"] + r["parse_fail"] + r["cap_hits"], r["cap_hits"]) == want for r in (rd, rk)))
    return CP.split_back(dcs, lab), ok


def unit_label(dc: dict, labs: list[str], c: str) -> str:
    """[reading] a class carried by several propositions of one demonstration takes the first one's label."""
    return next(lab for p, lab in zip(dc["props"], labs) if p["kind"] == "obj" and c in p["classes"])


# ---------------------------------------------------------------------------------------------- bootstrap
class Boot:
    """One per-image column table per set (rows in sorted image-id order) and ONE e2b.boot call: one W for every
    statistic of that set (prereg §5.5; T1-ANALYSIS §6). get(name) -> (point sum, replicate sums)."""

    def __init__(self, cols: dict, boot):
        self.idx = {k: j for j, k in enumerate(cols)}
        R = np.column_stack([np.asarray(v, float) for v in cols.values()])
        self.pt, self.T = R.sum(0), boot(R)

    def __call__(self, k):
        return self.pt[self.idx[k]], self.T[:, self.idx[k]]

    def has(self, *ks) -> bool:
        return all(k in self.idx for k in ks)


def est(get, fn, contrast: bool = False, strict: bool = True) -> dict:
    """fn(S), S(name) -> sums. Point from the point sums, percentile CI from the replicates; undefined replicates are
    dropped and counted, more than 1 % dropped = FAULT (prereg §5.5). [reading] strict=False (the T1-REP §1 table
    and the §6 strata / type rates, descriptive) counts the drops and raises no FAULT. contrast: the §5.2 p."""
    with np.errstate(divide="ignore", invalid="ignore"):
        pt, reps = float(fn(lambda k: get(k)[0])), np.asarray(fn(lambda k: get(k)[1]), float)
    ok = np.isfinite(reps)
    if strict and ((~ok).sum() > 0.01 * len(reps) or not np.isfinite(pt)):
        fault(f"more than 1 % undefined bootstrap replicates ({int((~ok).sum())}) or no point, prereg §5.5")
    out = {"point": pt if np.isfinite(pt) else None, "ci": CM.pct(reps[ok]) if ok.any() else None,
           "dropped": int((~ok).sum())}
    if (~ok).sum() > 0.01 * len(reps):  # only reachable when strict=False (CC-293 N3)
        out["note"] = "> 1 % undefined replicates, prereg §5.5; descriptive"
    if contrast:
        out["p"] = CM.p2(reps[ok])
    return out


def sfx(a: str, sc: str = "") -> str:
    return f"|{a}|{sc}" if sc else f"|{a}"


P = lambda a, sc="": lambda S: 100 * S("Hp" + sfx(a, sc)) / (S("Hp" + sfx(a, sc)) + S("Hm" + sfx(a, sc)))  # noqa: E731
PW = lambda a, sc="": lambda S: 100 * S("Hp" + sfx(a, sc)) / S("n" + sfx(a, sc))  # noqa: E731  unknown = wrong
RO = lambda a, sc="": lambda S: 100 * S("Hp" + sfx(a, sc)) / S("Ppairs")  # noqa: E731  R_obj^VI
CHS = lambda a, sc="": lambda S: 100 * S("CHs" + sfx(a, sc)) / S("one")  # noqa: E731  CHAIR_s^VI
VS = lambda a, sc="": lambda S: 100 * (S("Hp" + sfx(a, sc)) + S("Hm" + sfx(a, sc))) / S("n" + sfx(a, sc))  # noqa: E731
D = lambda m, a, b, sc="": lambda S: m(a, sc)(S) - m(b, sc)(S)  # noqa: E731


# ---------------------------------------------------------------------------------------------- XM3600-vi tables
def xm_columns(M: dict, R: dict, st: dict, mfn: dict, arms: list[str], cider: dict | None, chair,
               seg: dict | None) -> tuple[dict, dict]:
    """Per-image columns on XM3600-vi (prereg §3.1-§3.2 counts; T1-REP §1, §2 units; T1-ANALYSIS §3 rows) and the
    side counts. R = {arm: {id: record}} of the complete arms; T1-ANALYSIS §9.1 item 3 checks raise a FAULT.
    seg = RDRSegmenter tokens {"demo": {id: toks}, "cap": {(arm, id): toks}} or None (--no-segment)."""
    Q = {q["id"]: q for q in M["queries"]}
    ids = sorted(Q)
    cols, side = defaultdict(list), Counter()
    demo = all(a in arms for a in DEMO_ARMS)
    for i in ids:
        si = st.get(i, {})
        stat = lambda c, si=si: si.get(c, "unknown")
        cols["one"].append(1)
        cols["Ppairs"].append(sum(v == "present" for v in si.values()))
        unk = {}
        for a in arms:
            cap = R[a][i]["caption"]
            for sc, fn in mfn.items():
                m = fn(cap)
                hp, hm = sum(stat(c) == "present" for c in m), sum(stat(c) == "absent" for c in m)
                for k, v in (("Hp", hp), ("Hm", hm), ("U", len(m) - hp - hm), ("n", len(m)), ("CHs", int(hm > 0))):
                    cols[k + sfx(a, sc)].append(v)
                side[f"cay_ignored|{a}"] += sc == "cay" and len(m) < len(mfn[""](cap))
            unk[a] = {c for c in mfn[""](cap) if stat(c) == "unknown"}
            if cider and a in cider.get(XM, {}):
                cols[f"C|{a}"].append(cider[XM][a][i])
            if a in (*VARIANTS, "A8"):  # T1-REP §6 item 15: ΔP_obj^VI by Vietnamese feature (caption mentions)
                fc = cap_feats(cap, mfn[""](cap), chair, None if seg is None else seg["cap"].get((a, i)), side, a)
                for f in FEATS:
                    for h, s0 in (("Hp", "present"), ("Hm", "absent")):
                        cols[f"FC|{f}|{h}|{a}"].append(sum(stat(c) == s0 for c in fc[f]))
        for v in VARIANTS:  # C-M2 per-image rows (T1-ANALYSIS §5.2)
            if v in arms and "A8" in arms:
                cols[f"SP|{v}"].append(len(unk[v] - unk["A8"]))
                cols[f"S8|{v}"].append(len(unk["A8"] - unk[v]))
                cols[f"Sb|{v}"].append(len(unk[v] & unk["A8"]))
        if "A1" in arms:  # T1-REP §6 item 8 mention-count strata by A1's caption
            k1 = min(len(mfn[""](R["A1"][i]["caption"])), 3)
            for k in range(4):
                cols[f"ms{k}"].append(int(k1 == k))
                for a in (*VARIANTS, "A8"):
                    if a in arms:
                        for h in ("Hp", "Hm"):
                            cols[f"ms{k}:{h}|{a}"].append(cols[f"{h}|{a}"][-1] * (k1 == k))
        for a in ("PVR-drop", "PVR-keep", "A8"):  # verifier counts (T1-REP §1 shares, §6 item 8)
            if a in arms:
                for k in ("yes", "maybe", "no", "parse_fail", "cap_hits", "calls"):
                    cols[f"V|{a}|{k}"].append(R[a][i][k])
        if not demo:
            continue
        rec = {a: R[a][i] for a in DEMO_ARMS}
        dids = [str(x) for x in Q[i]["ranked"][:CP.K]]
        if any(rec[a]["demo_ids"] != dids for a in DEMO_ARMS):
            fault(f"demo_ids differ from the manifest ranked[:{CP.K}] (image {i})")
        dcs = [M["demos"][d] for d in dids]
        for a in ("PVR-drop", "PVR-keep"):
            ms = rec[a]["masks"]
            if [len(m) for m in ms] != [len(dc["props"]) for dc in dcs] or any(type(x) is not bool for m in ms for x in m):
                fault(f"{a} masks do not match the manifest props in shape (image {i})")
        for sc, fn in mfn.items():
            base = survival(dcs, None, fn)
            for k, s0 in (("Dm", "absent"), ("Dp", "present"), ("Du", "unknown")):
                cols[f"{k}|A1" + (f"|{sc}" if sc else "")].append(sum(stat(c) == s0 for u in base for c in u["units"]))
            side[f"out|{sc}"] += sum(len(u["out"]) for u in base)
            for a in ("A7", "PVR-drop", "PVR-keep"):
                sv = survival(dcs, masks_of(a, i, rec), fn)
                if sc == "" and sum(u["emptied"] for u in sv) != rec[a]["emptied"]:
                    fault(f"recomputed emptied differs from the saved {a} emptied (image {i})")
                for k, s0 in (("Dm", "absent"), ("Dp", "present")):
                    cols[f"{k}|{a}" + (f"|{sc}" if sc else "")].append(sum(stat(c) == s0 for u in sv for c in u["kept"]))
                side[f"created|{a}|{sc}"] += sum(len(u["created"]) for u in sv)
        side["decomp_fail_demos"] += sum("decomp_fail" in dc for dc in dcs)
        d1, dv = cols["Dm|A1"][-1], cols["Dm|PVR-drop"][-1]  # T1-ANALYSIS §4.5 strata by D⁻_A1
        dh = cols["Hm|A7"][-1] - cols["Hm|PVR-drop"][-1]
        for k in range(4):
            sel = int(min(d1, 3) == k)
            cols[f"st{k}"].append(sel)
            cols[f"st{k}:dHm"].append(dh * sel)
            cols[f"st{k}:dDm"].append((cols["Dm|A7"][-1] - dv) * sel)
        labs, ok = verifier_labels(dcs, rec["PVR-drop"], rec["PVR-keep"])
        side["label_mismatch_images"] += not ok
        cell = Counter()
        for dc, lab, md, mk, did in zip(dcs, labs, rec["PVR-drop"]["masks"], rec["PVR-keep"]["masks"], dids):
            for c in {c for p in dc["props"] if p["kind"] == "obj" for c in p["classes"]} & mfn[""](dc["text"]):
                cell[f"T|{unit_label(dc, lab, c)}|{stat(c)}"] += 1
                carry = [j for j, p in enumerate(dc["props"]) if p["kind"] == "obj" and c in p["classes"]]
                side["unit_label_conflicts"] += len({lab[j] for j in carry}) > 1  # CC-293 N9
                cell[f"UN|{stat(c)}"] += 1  # N2: each run read alone (no cross-run reconstruction)
                cell[f"KR|{stat(c)}"] += mk[carry[0]]
                cell[f"DS|{stat(c)}"] += not md[carry[0]]
            toks = None if seg is None else seg["demo"].get(did)
            side["demo_split_unavailable"] += seg is not None and toks is None
            for p, x in zip(dc["props"], lab):
                for tag in (f"K|{p['kind']}", *(f"F|{f}" for f in features(dc, p, chair.norm_tone, toks))):
                    cell[f"{tag}|n"] += 1
                    cell[f"{tag}|{x}"] += 1
        for lab in ("REJECTED", "UNCERTAIN", "SUPPORTED"):
            for s0 in ("absent", "present", "unknown"):
                cols[f"T|{lab}|{s0}"].append(cell[f"T|{lab}|{s0}"])
            for tag in TAGS:
                cols[f"{tag}|{lab}"].append(cell[f"{tag}|{lab}"])
        for tag in TAGS:
            cols[f"{tag}|n"].append(cell[f"{tag}|n"])
        for k in ("UN|absent", "UN|present", "KR|absent", "KR|present", "DS|present"):
            cols[k].append(cell[k])
    return dict(cols), side


CLF = ("con", "cái", "chiếc", "cây")  # T1-REP §6 item 15 classifier + noun phrases
CLF_RX = re.compile(r"(?<!\w)(?:" + "|".join(CLF) + r") $")
FEATS = ("classifier", "tone", "split")
TAGS = ("K|obj", "K|text", *(f"F|{f}" for f in FEATS))


def span_feats(t: str, a: int, b: int, norm, toks) -> set:
    """T1-REP §6 item 15 features of one mention span [a, b) of the lower-cased text t: 'classifier' = right after
    one of CLF; 'tone' = written with old-style tone placement (norm_tone moves it and merges no tones); 'split' = a
    compound the rule-based segmenter splits, i.e. the mention covers more than one RDRSegmenter word (CP.cover on the
    decomposer's own token spans). toks None = no segmenter tokens: 'split' is not decided."""
    out = set()
    if CLF_RX.search(t[:a]):
        out.add("classifier")
    if norm(t[a:b]) != t[a:b]:
        out.add("tone")
    if toks is not None and " " in t[a:b]:
        i0, i1 = CP.cover(toks, a, b)
        out |= {"split"} if i1 - i0 > 1 else set()
    return out


def features(dc: dict, p: dict, norm, toks=None) -> list[str]:
    """The item 15 features of a demonstration's object proposition (union over its mentions)."""
    if p["kind"] != "obj":
        return []
    t = dc["text"].lower()
    return sorted(set().union(*(span_feats(t, a, b, norm, toks) for a, b in p["mentions"])) if p["mentions"] else set())


def cap_feats(cap: str, m: frozenset, chair, toks, side: Counter, a: str) -> dict:
    """{feature: the caption's mapped classes with that feature on at least one of their mentions}. A caption whose
    mentions CP.vi_mentions cannot locate is counted and adds no class to any feature (descriptive)."""
    out = {f: set() for f in FEATS}
    try:
        ments = CP.vi_mentions(cap.replace("_", " "), chair)
    except SystemExit:
        side[f"cap_feat_unlocated|{a}"] += 1
        return out
    t = cap.lower()
    side[f"cap_split_unavailable|{a}"] += toks is None and any(" " in n for n, _, _ in ments if n in m)
    for n, x, y in ments:
        if n in m:
            for f in span_feats(t, x, y, chair.norm_tone, toks):
                out[f].add(n)
    return out


def seg_toks(texts: list[str], segment, norm) -> list:
    """RDRSegmenter token spans per text by decompose_vi's RDR / align path without its clean() step (CP.rdr on the
    '_'-free text, then CP.align; CC-293r2 N-C), one batch, then text by text after a batch failure; None where a text
    cannot be segmented or aligned. A pin mismatch of the segmenter files still aborts (PINS-A §4.2 rule 9)."""
    seen = [t.replace("_", " ") for t in texts]
    try:
        words = segment(seen)
    except (SystemExit, Exception) as e:
        if "differs from its pin" in str(e):
            raise
        words = [None] * len(seen)
    out = []
    for u, w in zip(seen, words):
        try:
            w = segment([u])[0] if w is None else w
            out.append(CP.align(u, w, lambda x: norm(x.lower())))
        except (SystemExit, Exception) as e:
            if "differs from its pin" in str(e):
                raise
            out.append(None)
    return out


# ---------------------------------------------------------------------------------------------- registered numbers
def decide(p: dict, var: dict, no_cider: str | None = None) -> dict:
    """prereg §12 (i)-(iv) with §6.3 (iii) as amended by T1-GUARD G-1, mechanically. p: point P_obj^VI of A1, A12;
    var[v]: P (point P_obj^VI), dR_lo (CI low of ΔR_obj^VI(v − A1)), dC_lo (CI low of the pooled-G1 ΔCIDEr-VI(v − A1)
    or None under --no-cider), dA8 (point ΔP_obj^VI(v − A8)). no_cider = the --no-cider reason (CC-293r2 W4)."""
    sesoi = max(SESOI_FLOOR, SESOI_FRAC * (p["A12"] - p["A1"]))
    out = {"label": DEV, "SESOI_P": sesoi, "headroom": p["A12"] - p["A1"], "headroom_stop": p["A12"] - p["A1"] < HEADROOM}
    passes = {v: {"dR": var[v]["dR_lo"] > -DELTA_R, "dC": None if var[v]["dC_lo"] is None else var[v]["dC_lo"] > -DELTA_C}
              for v in VARIANTS}
    out["passes"] = passes
    if any(x["dC"] is None for x in passes.values()):  # W4: δ_C cannot be tested, so (iii) and (iv) are not decided
        out["variant"], out["variant_status"] = None, f"NOT_DECIDED: no CIDEr-VI input ({no_cider})"
    else:
        ok = [v for v in VARIANTS if passes[v]["dR"] and passes[v]["dC"]]
        if not ok:
            out["variant"], out["variant_status"] = None, "STOP: neither variant passes δ_C and δ_R (§6.3)"
        elif len(ok) == 1:
            out["variant"], out["variant_status"] = ok[0], "the only variant that passes δ_C and δ_R"
        elif abs(var["PVR-drop"]["P"] - var["PVR-keep"]["P"]) < sesoi / 2:
            out["variant"], out["variant_status"] = "PVR-drop", "both pass; |ΔP_obj^VI| < SESOI_P / 2: PVR-drop"
        else:
            out["variant"] = max(VARIANTS, key=lambda v: var[v]["P"])
            out["variant_status"] = "both pass; the higher dev P_obj^VI"
    v = out["variant"]
    out["go_rule"] = None if v is None else var[v]["dA8"] >= sesoi  # §12 (iv), point estimate
    out["decision"] = ("STOP (headroom, §12 ii)" if out["headroom_stop"] else
                       "NOT_DECIDED (§6.3 variant: no CIDEr-VI input)" if out["variant_status"].startswith("NOT_DECIDED") else
                       "STOP (§6.3 variant)" if v is None else
                       "GO to tier 2 (§12 iv)" if out["go_rule"] else "STOP (§12 iv go rule)")
    return out


HW = {
    "HW-2": "With this datastore (KTVIC and OpenViIC training captions), unverified retrieved demonstrations lowered "
            "object precision (P_obj^VI) below zero-shot captioning (A1 − A0 = {a1a0}).",
    "HW-1a": "Verifying retrieved demonstrations before use raised object precision (P_obj^VI) above post-hoc correction "
             "with the same verifier (PVR − A8 = {pa8}), but was not shown to raise P_obj^VI above zero-shot captioning "
             "(PVR − A0 = {pa0}).",
    "HW-1b": "Verifying retrieved demonstrations before use was not shown to raise object precision (P_obj^VI) above "
             "post-hoc correction with the same verifier (PVR − A8 = {pa8}) or above zero-shot captioning (PVR − A0 = "
             "{pa0}).",
    "HW-La": "Verifying retrieved demonstrations before use raised object precision (P_obj^VI) above post-hoc correction "
             "with the same verifier (PVR − A8 = {pa8}), but lowered it below zero-shot captioning (PVR − A0 = {pa0}).",
    "HW-Lb": "Verifying retrieved demonstrations before use was not shown to raise object precision (P_obj^VI) above "
             "post-hoc correction with the same verifier (PVR − A8 = {pa8}), and lowered it below zero-shot captioning "
             "(PVR − A0 = {pa0}).",
    "harm": "With this datastore, unverified retrieval lowered P_obj^VI below zero-shot captioning, and verification "
            "{verb} that loss (PVR − A1 = {pa1}).",
    "HW-3": "With this datastore (KTVIC and OpenViIC training captions), verifying retrieved demonstrations before use "
            "raised object precision (P_obj^VI) above both post-hoc correction with the same verifier (PVR − A8 = "
            "{pa8}) and zero-shot captioning (PVR − A0 = {pa0}).",  # [reading] the datastore named in it (CC-293 N7)
    "HW-0": "Verifying retrieved demonstrations before use raised object precision (P_obj^VI) above zero-shot captioning "
            "(PVR − A0 = {pa0}) but was not shown to raise it above post-hoc correction with the same verifier (PVR − A8 "
            "= {pa8}).",
}


def xci(e: dict) -> str:
    return f"{e['point']:.2f} [{e['ci'][0]:.2f}, {e['ci'][1]:.2f}]"


def headline(a1a0: dict, pa0: dict, pa8: dict, pa1: dict, rule: bool) -> dict:
    """T1-REP §4: exactly one of HW-0 / 1a / 1b / La / Lb / 3, chosen mechanically; HW-2 whenever its condition holds,
    and the harm clause after HW-1a / 1b / La / Lb only if HW-2 holds. 'the rule' at tier 1 = §12 (iv)."""
    case = "L" if pa0["ci"][1] < 0 else "R" if pa0["ci"][0] > 0 else "N"
    hw = {("N", True): "HW-1a", ("N", False): "HW-1b", ("L", True): "HW-La", ("L", False): "HW-Lb",
          ("R", True): "HW-3", ("R", False): "HW-0"}[case, rule]
    g = {"a1a0": xci(a1a0), "pa0": xci(pa0), "pa8": xci(pa8), "pa1": xci(pa1)}
    hw2 = a1a0["ci"][1] < 0
    out = {"label": DEV, "case": case, "rule": rule, "sentence_id": hw, "sentence": HW[hw].format(**g), "HW-2": None}
    if hw == "HW-3":
        out["tier1_label"] = "dev go (§12 iv)"  # never PASS at tier 1 (T1-REP §4)
    if hw2:
        out["HW-2"] = HW["HW-2"].format(**g)
        if hw not in ("HW-3", "HW-0"):
            out["sentence"] += " " + HW["harm"].format(verb="reduced" if pa1["ci"][0] > 0 else "was not shown to reduce", **g)
    return out


def variant_block(v: str, get, arms: list[str], status: dict, seg_ok: bool) -> dict:
    """Everything keyed by one PVR variant on XM3600-vi (both are always computed; decide() marks the selected).
    status = {arm: status} on XM3600-vi; an arm that is not complete is no result (CC-293 Ruling 7, item 24)."""
    b = {"primary": est(get, D(P, v, "A8"), True), "primary_cay": est(get, D(P, v, "A8", "cay"), True),
         "unknown_wrong": est(get, D(PW, v, "A8"), True), "dR_A1": est(get, D(RO, v, "A1")),
         "dR_A8": est(get, D(RO, v, "A8")), "dCHAIR_s_A8": est(get, D(CHS, v, "A8"))}
    fam = [a for a in FAMILY if a in arms]
    ps = {a: est(get, D(P, v, a), True) for a in fam}
    rej = CM.holm([ps[a]["p"] for a in fam])
    left = {a: status.get(a, "absent") for a in FAMILY if a not in fam}
    b["holm"] = {"members": fam, "rows": {a: {**ps[a], "holm_reject": r} for a, r in zip(fam, rej)},
                 "cut": sorted(a for a, x in left.items() if x.startswith("cut")),
                 "partial": {a: x for a, x in left.items() if x.startswith("partial")},
                 "absent": sorted(a for a, x in left.items() if x == "absent")}
    b["key_secondaries"] = {a: b["holm"]["rows"].get(a) for a in ("A4", "A9")}  # T1-REP R-2
    vs = {a: est(get, VS(a)) for a in (v, "A8")}
    b["flag_5_7a"] = abs(vs[v]["point"] - vs["A8"]["point"]) > FLAG_PTS
    b["strata_A1_mentions"] = {k: est(get, dp_in(k, v), strict=False) for k in range(4)} if get.has(
        f"ms0:Hp|{v}", "ms0:Hp|A8") else "NOT_COMPUTED: A1 is incomplete"
    for a in ("A0", "A1"):
        b[f"d_{a}"] = est(get, D(P, v, a)) if a in arms else f"NOT_COMPUTED: {a} is {status.get(a, 'absent')}"
    b["dP_by_feature"] = {f: est(get, D(PF(f), v, "A8"), strict=False) if f != "split" or seg_ok else NO_SPLIT
                          for f in FEATS}  # T1-REP §6 item 15, caption mentions with the feature
    b["dP_by_type"] = {"obj": "= primary: every mapped caption mention is an object mention (prereg §3.1)",
                       "text": NO_TEXT}
    b["dCIDEr_xm_A1"] = est(get, lambda S: (S(f"C|{v}") - S("C|A1")) / S("one")) if get.has(f"C|{v}", "C|A1") else (
        "NOT_COMPUTED: no CIDEr-VI input (see inputs.cider)")  # descriptive (T1-GUARD G-4)
    return b


PF = lambda f: lambda a, sc="": lambda S: 100 * S(f"FC|{f}|Hp|{a}") / (S(f"FC|{f}|Hp|{a}") + S(f"FC|{f}|Hm|{a}"))  # noqa: E731
NO_SPLIT = ("NOT_COMPUTED: --no-segment. 'compounds the rule-based segmenter splits' (T1-REP §6 item 15) needs "
            "RDRSegmenter tokens, which no record or manifest stores")
NO_TEXT = ("NOT_COMPUTED: P_obj^VI is defined on mapped object mentions only (prereg §3.1: \"objects_in(caption, "
           "raw_tone=False) -> lexicon classes; keep the 69 keys\"); scene-text propositions carry no class, and "
           "T1-REP §1 states \"Attribute, relation, count and scene-text propositions cannot be validated with existing "
           "gold\"")


def dp_in(k: int, v: str):
    """ΔP_obj^VI(v − A8) among images whose A1 caption has k mapped mentions (k = 3: three or more)."""
    p = lambda a: lambda S: 100 * S(f"ms{k}:Hp|{a}") / (S(f"ms{k}:Hp|{a}") + S(f"ms{k}:Hm|{a}"))  # noqa: E731
    return lambda S: p(v)(S) - p("A8")(S)


def identity(get, sc: str) -> dict | None:
    """T1-REP §2 on XM3600-vi: c, ρ, φ, OR, c′ for PVR-drop, PVR-keep and A7 with CIs; OR_PVR-drop / OR_A7 (the
    selectivity measure) and OR_PVR-keep / OR_A7 ("not count-matched"); the analytic pool-level null; the unknown
    share. c′ from (c, ρ, φ) must equal c′ counted, in exact integers, else FAULT."""
    t = (lambda k: k + (f"|{sc}" if sc else ""))
    if not get.has(t("Dm|A1"), t("Dm|A7")):
        return None
    na, npr, nu = (int(get(t(k))[0]) for k in ("Dm|A1", "Dp|A1", "Du|A1"))
    out = {"N_A": na, "N_P": npr, "unknown": nu, "unknown_share": 100 * nu / max(1, na + npr + nu),
           "c": est(get, lambda S: S(t("Dm|A1")) / (S(t("Dm|A1")) + S(t("Dp|A1")))), "arms": {}}
    from fractions import Fraction as F
    for a in ("PVR-drop", "PVR-keep", "A7"):
        ka, kp = (int(get(t(f"{k}|{a}"))[0]) for k in ("Dm", "Dp"))
        if not (na and npr and ka and kp):  # the identity needs 0 < c < 1, ρ < 1, φ < 1
            out["arms"][a] = {"defined": False}
            continue
        c, r1, f1 = F(na, na + npr), F(ka, na), F(kp, npr)  # c, 1 − ρ, 1 − φ
        if c * r1 / (c * r1 + (1 - c) * f1) != F(ka, ka + kp):
            fault(f"T1-REP §2 c′ identity differs from c′ counted ({a}, scorer {sc or 'of record'})")
        rem = (na - ka) + (npr - kp)
        out["arms"][a] = {
            "rho": est(get, lambda S, a=a: 1 - S(t(f"Dm|{a}")) / S(t("Dm|A1"))),
            "phi": est(get, lambda S, a=a: 1 - S(t(f"Dp|{a}")) / S(t("Dp|A1"))),
            "OR": est(get, lambda S, a=a: (S(t(f"Dm|{a}")) / S(t("Dm|A1"))) / (S(t(f"Dp|{a}")) / S(t("Dp|A1")))),
            "c_prime": est(get, lambda S, a=a: S(t(f"Dm|{a}")) / (S(t(f"Dm|{a}")) + S(t(f"Dp|{a}")))),
            "null": {"rho": rem / (na + npr), "phi": rem / (na + npr), "OR": 1.0, "c_prime": na / (na + npr)}}
    if all(out["arms"][a].get("defined", True) for a in out["arms"]):
        orr = lambda a: lambda S: (S(t(f"Dm|{a}")) / S(t("Dm|A1"))) / (S(t(f"Dp|{a}")) / S(t("Dp|A1")))  # noqa: E731
        out["OR_PVR-drop/OR_A7"] = est(get, lambda S: orr("PVR-drop")(S) / orr("A7")(S))
        out["OR_PVR-keep/OR_A7"] = {**est(get, lambda S: orr("PVR-keep")(S) / orr("A7")(S)), "label": "not count-matched"}
    return out


def method_name(idn: dict | None, a7: dict | None) -> dict:
    """T1-REP §1: 'verification' iff (i) the 95 % CI of OR_V / OR_A7 lies wholly below 1 and (ii) V > A7 on P_obj^VI,
    Holm-significant, with V = PVR-drop at tier 1 (A7 follows it, PINS-A l.158-159); otherwise 'filtering'. [reading]
    (ii) uses the §5.2 family with PVR = PVR-drop, whichever variant §6.3 selects."""
    r1 = bool(idn and "OR_PVR-drop/OR_A7" in idn and idn["OR_PVR-drop/OR_A7"]["ci"][1] < 1)
    r2 = bool(a7 and a7["point"] > 0 and a7["holm_reject"])
    return {"rule_i": r1, "rule_ii": r2, "name": "verification" if r1 and r2 else "filtering",
            "family": "PVR-drop vs the §5.2 members"}


def s1_table(get, side: Counter) -> dict:
    """T1-REP §1 verifier-validity table (XM3600-vi; PVR-drop / PVR-keep labels as verifier_labels reads them)."""
    if not get.has("T|REJECTED|absent"):
        return {"status": "NOT_COMPUTED (a demonstration arm is incomplete)"}
    cells = {f"{lab} x {s0}": int(get(f"T|{lab}|{s0}")[0]) for lab in ("SUPPORTED", "UNCERTAIN", "REJECTED")
             for s0 in ("present", "absent", "unknown")}
    out = {"label": DEV, "cells": cells, "label_mismatch_images": side["label_mismatch_images"],
           "unit_label_conflicts": side["unit_label_conflicts"], "disclosure": SWAP}
    e = functools.partial(est, get, strict=False)
    if side["label_mismatch_images"]:  # CC-293 N2, fixed before data: each run read alone, exact, no κ
        S_ = lambda k: lambda S: S(k)  # noqa: E731
        return {**out, "cells_status": "reconstructed cells, not valid: the PVR-drop and PVR-keep verifier counts "
                                       "disagree on some images", "status": "FALLBACK (per-run statistics)",
                "precision_REJECTED_absent_keep_run": e(lambda S: S_("KR|absent")(S) / (S_("KR|absent")(S) + S_("KR|present")(S))),
                "recall_REJECTED_absent_keep_run": e(lambda S: S_("KR|absent")(S) / S_("UN|absent")(S)),
                "SUPPORTED_share_present_drop_run": e(lambda S: S_("DS|present")(S) / S_("UN|present")(S)),
                "kappa": "NOT_COMPUTABLE: needs one label per unit across both runs"}
    T = lambda lab, s0: lambda S: S(f"T|{lab}|{s0}")  # noqa: E731
    rej_a, rej_p, sup_a, sup_p = T("REJECTED", "absent"), T("REJECTED", "present"), T("SUPPORTED", "absent"), T("SUPPORTED", "present")
    all_s = lambda s0: lambda S: sum(S(f"T|{lab}|{s0}") for lab in ("SUPPORTED", "UNCERTAIN", "REJECTED"))  # noqa: E731

    def kappa(S):
        a, b, c, d = rej_a(S), rej_p(S), sup_a(S), sup_p(S)
        n = a + b + c + d
        pe = ((a + b) * (a + c) + (c + d) * (b + d)) / n ** 2
        return ((a + d) / n - pe) / (1 - pe)

    out.update(status="OK", precision_REJECTED_absent=e(lambda S: rej_a(S) / (rej_a(S) + rej_p(S))),
               recall_REJECTED_absent=e(lambda S: rej_a(S) / all_s("absent")(S)),
               SUPPORTED_share_present=e(lambda S: sup_p(S) / all_s("present")(S)), kappa=e(kappa),
               kappa_excluded={"UNCERTAIN": sum(v for k, v in cells.items() if k.startswith("UNCERTAIN")),
                               "unknown": sum(v for k, v in cells.items() if k.endswith("unknown"))})
    return out


SWAP = ("the per-image count check cannot see swaps that leave the counts equal (a proposition UNCERTAIN in the drop "
        "run and REJECTED in the keep run, with another the other way round)")


def shares(get, a: str) -> dict:
    """Per-arm verifier shares over its propositions (calls + cap_hits) and calls (T1-REP §1; prereg §6.3)."""
    V = lambda k: lambda S: S(f"V|{a}|{k}")  # noqa: E731
    n = lambda S: V("calls")(S) + V("cap_hits")(S)  # noqa: E731
    return {"yes_share": est(get, lambda S: V("yes")(S) / n(S)), "no_share": est(get, lambda S: V("no")(S) / n(S)),
            "UNCERTAIN_share": est(get, lambda S: (V("maybe")(S) + V("parse_fail")(S) + V("cap_hits")(S)) / n(S)),
            "parse_fail_share": est(get, lambda S: V("parse_fail")(S) / V("calls")(S)),
            "totals": {k: int(get(f"V|{a}|{k}")[0]) for k in ("yes", "maybe", "no", "parse_fail", "cap_hits", "calls")}}


def rates(get, tag: str) -> dict | None:
    if not get.has(f"{tag}|n") or not get(f"{tag}|n")[0]:
        return None
    return {lab: est(get, lambda S, lab=lab: S(f"{tag}|{lab}") / S(f"{tag}|n"), strict=False) for lab in ("REJECTED", "UNCERTAIN")}


# ---------------------------------------------------------------------------------------------- descriptives (T1-REP §6)
TONES = "̣̀́̃̉"  # grave, acute, tilde, hook above, dot below
VOWELS = "aăâeêioôơuưy"
VI_LETTERS = sorted(set("abcdeghiklmnopqrstuvxyđăâêôơư") | {unicodedata.normalize("NFC", v + t) for v in VOWELS for t in TONES})
VI_TOKEN = re.compile("[" + "".join(VI_LETTERS) + "]+")  # item 9, pinned here: Vietnamese letters, no f j w z
VI_SPECIFIC = re.compile("[" + "".join(c for c in VI_LETTERS if c not in "abcdeghiklmnopqrstuvxy") + "]")  # §5.7(b)


def tokens(text: str) -> list[str]:
    """NFC, lower case, every punctuation character removed, whitespace split (item 9 'syllables')."""
    s = "".join(ch for ch in unicodedata.normalize("NFC", text).lower() if not unicodedata.category(ch).startswith("P"))
    return s.split()


def text_stats(caps: list[str], finish: list[str]) -> dict:
    """T1-REP §6 item 9 and the prereg §5.7(b) VI-script share, deterministic and non-AI."""
    tk = [tokens(c) for c in caps]
    flat = [t for x in tk for t in x]
    grams = lambda n: [tuple(x[j:j + n]) for x in tk for j in range(len(x) - n + 1)]  # noqa: E731
    g1, g2 = grams(1), grams(2)
    gen = [f for f in finish if f != "a8"]  # A8 copies A1's caption and decodes nothing
    return {"n": len(caps), "vi_token_share": len([t for t in flat if VI_TOKEN.fullmatch(t)]) / max(1, len(flat)),
            "vi_script_share": sum(bool(VI_SPECIFIC.search(unicodedata.normalize("NFC", c).lower())) for c in caps) / max(1, len(caps)),
            "empty_share": sum(not c.strip() for c in caps) / max(1, len(caps)),
            "repeated_3gram_share": sum(max(Counter(zip(x, x[1:], x[2:])).values(), default=0) > 1 for x in tk) / max(1, len(caps)),
            "mean_syllables": len(flat) / max(1, len(caps)),
            "distinct_1": len(set(g1)) / max(1, len(g1)), "distinct_2": len(set(g2)) / max(1, len(g2)),
            "truncation_share": None if not gen else sum(f == "length" for f in gen) / len(gen)}


def wall(rows: list[dict]) -> float | None:
    """[reading] seconds per image from the records' utc stamps (1 s resolution): (last − first) / (n − 1)."""
    t = sorted(time.mktime(time.strptime(r["utc"], "%Y-%m-%dT%H:%M:%SZ")) for r in rows)
    return (t[-1] - t[0]) / (len(t) - 1) if len(t) > 1 else None


def set_report(s: str, M: dict, R: dict, status: dict, mfn: dict, decompose) -> dict:
    """Per arm on one set: item 7 counts that need no label, item 8 calls / cap hits / wall clock, item 9, the cây
    ignore count, the emptied-demonstration share (T1-REP §4) and the segmenter failure rate."""
    lang = G.SETS[s][1]
    out = {}
    for a, st_ in status.items():
        if st_ != "complete":
            out[a] = {"status": st_, "n": len(R.get(a) or {})}
            continue
        rows = [R[a][q["id"]] for q in sorted(M["queries"], key=lambda q: q["id"])]
        caps = [r["caption"] for r in rows]
        e = {"status": "complete", **text_stats(caps, [r["finish"] for r in rows]), "sec_per_image": wall(rows)}
        for k in ("calls", "cap_hits"):
            if k in rows[0]:
                e[f"mean_{k}"] = sum(r[k] for r in rows) / len(rows)
        if isinstance(rows[0].get("emptied"), int) and not isinstance(rows[0].get("emptied"), bool):
            e["emptied_demo_share"] = sum(r["emptied"] for r in rows) / (CP.K * len(rows))
        if a in ("A8", "S2"):
            e["empty_caption_share"] = e["empty_share"]
        if lang == "vi":
            m = [mfn[""](c) for c in caps]
            e["mapped_mentions"] = sum(map(len, m))
            e["mentions_per_caption"] = e["mapped_mentions"] / len(caps)
            e["cay_ignored"] = sum(len(mfn["cay"](c)) < len(x) for c, x in zip(caps, m))
            e["segmenter_fail_rate"] = (sum("decomp_fail" in d for d in decompose(caps)) / len(caps) if decompose else
                                        "NOT_COMPUTED: --no-segment (the run needs VnCoreNLP, PINS-A §4.2)")
        else:
            e["segmenter_fail_rate"] = "n/a: RDRSegmenter is the Vietnamese segmenter (English set)"
        out[a] = e
    return out


def similarity(M: dict, qnpz: Path, dnpz: Path) -> dict:
    """T1-REP §4: SigLIP retrieval cosine of each query with its ranked[:K] demonstrations (quantiles per rank)."""
    import c_pvr_manifest as MAN  # noqa: E402  emb(): L2-normalised rows by id, npz sha (bb7c6c9a)
    qs = sorted(M["queries"], key=lambda q: q["id"])
    qv, qh = MAN.emb(safe(qnpz), [q["id"] for q in qs])
    did = sorted({str(x) for q in qs for x in q["ranked"][:CP.K]})
    dv, dh = MAN.emb(safe(dnpz), did)
    row = {d: j for j, d in enumerate(did)}
    cos = np.array([[float(qv[n] @ dv[row[str(x)]]) for x in q["ranked"][:CP.K]] for n, q in enumerate(qs)])
    return {"qnpz_sha256": qh, "dnpz_sha256": dh, "quantiles_0_25_50_75_100": {
        f"rank{r + 1}": [float(x) for x in np.percentile(cos[:, r], [0, 25, 50, 75, 100])] for r in range(cos.shape[1])}}


# ---------------------------------------------------------------------------------------------- CIDEr-VI guard
def guard_g1(cider: dict, ids: dict, v: str) -> dict:
    """T1-GUARD G-1 on G1 = KTVIC explore ∪ OpenViIC explore: image-weighted mean of the per-image ΔCIDEr-VI(v − A1),
    each image scored within its own source set (the input's job, G-7), bootstrap stratified by source set. [reading]
    the strata are drawn in GUARD_SETS order from ONE generator seeded 20261102 (two generators on one seed would
    draw dependent strata). Passes δ_C iff the CI lower bound > −2.0."""
    d = [np.array([cider[s][v][i] - cider[s]["A1"][i] for i in ids[s]], float) for s in GUARD_SETS]
    rng, n = np.random.default_rng(CM.SEED), sum(map(len, d))
    ws = [rng.multinomial(len(x), [1 / len(x)] * len(x), size=CM.B) @ x for x in d]  # per-stratum replicate sums
    reps = sum(ws) / n
    lo, hi = CM.pct(reps)
    return {"n": n, "point": float(sum(x.sum() for x in d) / n), "ci": [lo, hi], "passes": lo > -DELTA_C,
            "per_set": {s: {"n": len(x), "point": float(x.mean()), "ci": CM.pct(w / len(x)), "label": "descriptive"}
                        for s, x, w in zip(GUARD_SETS, d, ws)}}  # T1-GUARD §2.1: per-set Δ with CIs, same replicates


def cider_in(p: Path, h: str, ids: dict) -> dict:
    b = safe(p).read_bytes()
    if sha(b) != h:
        fault("--cider differs from --cider-sha")
    c = json.loads(b)
    need = [(XM, "A0")] + [(s, a) for s in (XM, *GUARD_SETS) for a in ("A1", *VARIANTS)]  # A0: T1-REP §4 A1 − A0
    if missing := [f"{s}.{a}" for s, a in need if a not in c.get(s, {})]:
        fault(f"--cider lacks {missing}")
    for s, arms in c.items():
        for a, v in arms.items():
            if s not in ids or set(v) != set(ids[s]):
                fault(f"--cider: {s}.{a} does not cover exactly the manifest ids")
            if not all(type(y) in (int, float) and math.isfinite(y) and 0 <= y <= 1000 for y in v.values()):
                fault(f"--cider: {s}.{a} holds a non-finite value or one outside [0, 1000] (CIDEr-D x100; CC-293r2 N-H)")
    return c


# ---------------------------------------------------------------------------------------------- the run
def score(x, boot, decompose, pins: bool = True, segment=None) -> tuple[dict, dict]:
    """Registered numbers and T1-REP reports first (written before C-M1 / C-M2, T1-ANALYSIS §1), then the analyses.
    decompose / segment: CP.decompose_vi / CP.rdr, or None (--no-segment: every product of them is NOT_COMPUTED)."""
    CP.raw_tone_unset()  # prereg §3.1 N4; T1-ANALYSIS §9.1 item 2
    if bool(x.cider) == bool(x.no_cider) or bool(x.cider) != bool(x.cider_sha):  # CC-293r2 W4 (a): never a silent drop
        fault("give exactly one of --cider (with --cider-sha) or --no-cider REASON")
    if x.no_cider and Path(x.sums).name == "SHA256SUMS_tier1":  # W4 (b): a JOB DONE pull waits for the CIDEr-VI pin
        fault("--no-cider under a JOB DONE pull (SHA256SUMS_tier1): S16 waits for the CIDEr-VI pin (CC-293 Ruling 4)")
    if sys.version_info[:2] != (3, 12):
        fault(f"CPython {sys.version.split()[0]}: the A7 rebuild rests on 3.12 (T1-ANALYSIS §9.1 item 10)")
    Ms = manifests(x.build, x.tman)
    sums = sums_of(x.out / x.sums)
    capj = json.loads(safe(x.cap).read_bytes())
    cut = set(capj.get("cuts", []))
    known = {f"out/{s}.{a}.jsonl" for s, (_, _, arms) in G.SETS.items() for a in arms}
    ids_logs = {f"out/logs/{s}.{a}.ids.jsonl" for s, (_, _, arms) in G.SETS.items() for a in arms}  # c_pvr_gpu l.684
    if bad := sorted(k for k in sums if k.startswith("out/") and k not in known | ids_logs):
        fault(f"SUMS lists outputs of no registered (set, arm): {bad[:3]}")
    if bad := [k for k in sorted(ids_logs & set(sums)) if CP.sha_file(x.out / k) != sums[k]]:  # hashed, never parsed
        fault(f"ids-only logs differ from their SUMS lines: {bad[:3]}")
    ids = {s: sorted(q["id"] for q in M["queries"]) for s, M in Ms.items()}
    R, status = {}, {}
    for s, (_, _, arms) in G.SETS.items():
        R[s], status[s] = {}, {}
        for a in arms:
            r = records(x.out, sums, s, a, set(ids[s]))
            if a in cut:
                if r is not None:
                    fault(f"{s}.{a} was cut by CAP.json but has an output")
                status[s][a] = "cut by the registered cap rule (T1-REP §9)"
            elif r is None:
                status[s][a] = "absent"
            else:
                R[s][a] = r
                status[s][a] = "complete" if len(r) == len(ids[s]) else f"partial ({len(r)} of {len(ids[s])})"
    if Path(x.sums).name == "SHA256SUMS_tier1":  # JOB DONE (S11 §13): every uncut arm is complete (CC-293 N4)
        if bad := [f"{s}.{a}: {v}" for s in status for a, v in status[s].items() if v == "absent" or v.startswith("partial")]:
            fault(f"JOB DONE pull with incomplete uncut arms: {bad[:3]}")
    st = gold(x.root, x.labels, x.desc, pins)
    mfn = mention_fns(x.root)
    a1d = a1_degraded(x.a1_decomp)
    cider = cider_in(x.cider, x.cider_sha, ids) if x.cider else None
    res = {"label": CP.LABEL, "tier": 1, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "sys_version": sys.version, "numpy": np.__version__, "B": CM.B, "seed": CM.SEED,
           "code_sha256": {rel: sha((x.root / rel).read_bytes()) for rel in (*CODE, "scripts/c_pvr/c_pvr.py",
                                                                             "scripts/c_pvr/c_pvr_run.py", Path(__file__).relative_to(x.root).as_posix())},
           "inputs": {"tman": x.tman, "sums_sha256": sha(safe(x.out / x.sums).read_bytes()),
                      "cap_sha256": sha(safe(x.cap).read_bytes()),
                      "cider": {"sha256": x.cider_sha} if x.cider else {"no_cider": x.no_cider}},
           "status": status, "cut": sorted(cut), "a1_decomp": a1d}
    if x.rerun_of:  # T1-ANALYSIS §9.1: every number of a re-run carries the stamp (CC-293 N10)
        if not re.fullmatch(r"OPS-[A-Za-z0-9_.:-]+", x.rerun_of):
            fault("--rerun-of is not an OPS id")
        res["rerun"] = f"re-run after FAULT {x.rerun_of}, code {sha(Path(__file__).read_bytes())}"
        res["label"] += f"; {res['rerun']}"
    res["sets"] = {s: set_report(s, Ms[s], R[s], status[s], mfn, decompose if G.SETS[s][1] == "vi" else None)
                   for s in G.SETS}
    res["similarity"] = {s: similarity(Ms[s], Path(q), Path(d)) for s, q, d in (re.fullmatch(
        r"([a-z0-9_]+)=([^,]+),(.+)", e).groups() for e in x.emb)} if x.emb else (
        "NOT_COMPUTED: no --emb input (T1-REP §4 SigLIP similarity needs the query and datastore npz)")
    arms = [a for a, v in status[XM].items() if v == "complete"]
    chair = CP.rescap_mods(x.root)[0]
    seg = None
    if segment:  # item 15 'split': the demonstrations A1 retrieves and the captions of the variants and A8
        dd = sorted({str(d) for q in Ms[XM]["queries"] for d in q["ranked"][:CP.K]})
        ck = [(a, i) for a in (*VARIANTS, "A8") if a in arms for i in ids[XM]]
        tk = seg_toks([Ms[XM]["demos"][d]["text"] for d in dd] + [R[XM][a][i]["caption"] for a, i in ck], segment,
                      chair.norm_tone)
        seg = {"demo": dict(zip(dd, tk)), "cap": dict(zip(ck, tk[len(dd):]))}
    cols, side = xm_columns(Ms[XM], R[XM], st, mfn, arms, cider, chair, seg)
    get = Boot(cols, boot)
    xm = {"label": DEV, "arms": {}, "side_counts": dict(side), "base_rate": {
        **GT.WANT_B["image_class_pairs"], "present_share_verified_pairs": GT.WANT_B["image_class_pairs"]["present"] / sum(
            GT.WANT_B["image_class_pairs"].values()), "source": "prereg §3.3 l.311 = gates.py WANT_B (committed manifest)"}}
    for a in arms:
        xm["arms"][a] = {sc or "of_record": {"P_obj": est(get, P(a, sc)), "P_obj_wrong": est(get, PW(a, sc)),
                                             "R_obj": est(get, RO(a, sc)), "CHAIR_s": est(get, CHS(a, sc)),
                                             "verifiable_share": est(get, VS(a, sc)),
                                             "counts": {k: int(get(k + sfx(a, sc))[0]) for k in ("Hp", "Hm", "U", "n")}}
                         for sc in mfn}
        xm["arms"][a]["of_record"]["CHAIR_i"] = 100 - xm["arms"][a]["of_record"]["P_obj"]["point"]
    need = {"A1", "A8", "A12", *VARIANTS}
    if missing := sorted(need - set(arms)):
        xm["decisions"] = {"decision": f"NOT_DECIDED: {missing} incomplete on {XM} (S16 full panel)"}
    else:
        xm["variants"] = {v: variant_block(v, get, arms, status[XM], seg is not None) for v in VARIANTS}
        dC = {v: guard_g1(cider, ids, v) if cider else None for v in VARIANTS}
        xm["guard_G1"] = dC if cider else f"NOT_COMPUTED: no CIDEr-VI input ({x.no_cider})"
        Pt = lambda a: xm["arms"][a]["of_record"]["P_obj"]["point"]  # noqa: E731
        dec = decide({"A1": Pt("A1"), "A12": Pt("A12")},
                     {v: {"P": Pt(v), "dR_lo": xm["variants"][v]["dR_A1"]["ci"][0], "dA8": xm["variants"][v]["primary"]["point"],
                          "dC_lo": dC[v]["ci"][0] if dC[v] else None} for v in VARIANTS}, x.no_cider)
        xm["decisions"] = dec
        a1a0 = est(get, D(P, "A1", "A0")) if "A0" in arms else None
        na0 = f"NOT_COMPUTED: A0 is {status[XM].get('A0')}"
        xm["A1_minus_A0"] = {"P_obj": a1a0 or na0, "R_obj": est(get, D(RO, "A1", "A0")) if a1a0 else na0,
                             "CIDEr": est(get, lambda S: (S("C|A1") - S("C|A0")) / S("one")) if get.has("C|A1", "C|A0") else
                             f"NOT_COMPUTED: no CIDEr-VI input ({x.no_cider})"}
        xm["A12_minus_A1"] = est(get, D(P, "A12", "A1"))
        xm["A8_recall_loss_vs_A1"] = est(get, D(RO, "A8", "A1"))
        xm["base_P_R"] = {a: {k: xm["arms"][a]["of_record"][k]["point"] for k in ("P_obj", "R_obj")} for a in ("A0", "A1") if a in arms}
        xm["base_P_R"].update(delta_R=DELTA_R, SESOI_P=dec["SESOI_P"])
        for v in VARIANTS:
            vb = xm["variants"][v]
            vb["selected"] = dec["variant"] == v
            vb["vi_script_guard"] = {a: res["sets"][XM][a]["vi_script_share"] >= VI_GUARD for a in (v, "A8")}
            vb["primary_label"] = ("VI-guard FAIL (§5.7 b, PVR)" if not vb["vi_script_guard"][v] else
                                   "VI-guard INCONCLUSIVE (§5.7 b, A8)" if not vb["vi_script_guard"]["A8"] else DEV)
            if a1d.get(XM, {}).get("DEGRADED"):
                vb["primary_label"] += "; A8 DEGRADED (S11 §10.3)"
            vb["headline"] = headline(a1a0, vb["d_A0"], vb["primary"], vb["d_A1"], vb["primary"]["point"] >= dec[
                "SESOI_P"]) if a1a0 else na0
        xm["s1_verifier_table"] = s1_table(get, side)
        xm["verifier_shares"] = {a: shares(get, a) for a in ("PVR-drop", "PVR-keep", "A8")}  # A8 = output side
        xm["by_type"] = {t: NO_SPLIT if t == "F|split" and seg is None else rates(get, t) or "NOT_COMPUTED: no such "
                         "proposition among A1's top-K demonstrations" for t in TAGS}
        xm["s2_identity"] = {sc or "of_record": identity(get, sc) or "NOT_COMPUTED: a demonstration arm is incomplete"
                             for sc in mfn}
        xm["method_name"] = method_name(xm["s2_identity"]["of_record"], xm["variants"]["PVR-drop"]["holm"]["rows"].get("A7"))
    path = x.res / "score_tier1.json"
    write_new(path, CP.jdump(res | {XM: xm}))
    cm = cm_stage(get, xm, {a: len(ids[XM]) - len(R[XM].get(a, {})) for a in G.SETS[XM][2]}, arms, x.root, res)
    if x.rerun_of:
        cm.update(rerun=res["rerun"], label=f"{cm['label']}; {res['rerun']}")
        for e in cm["main_text"]:
            e["label"] += f"; {res['rerun']}"
    write_new(x.res / "cm_tier1.json", CP.jdump(cm))
    return res | {XM: xm}, cm


def cm_stage(get, xm: dict, missing: dict, arms: list, root: Path, res: dict) -> dict:
    """T1-ANALYSIS: inputs taken from the written S16 record (G1's OR CI, the §6.3 variant, DEGRADED, §5.7 b) and
    the same Boot (one W). §9.1 checks against T1-REP §2 and the S16 P values are made here first."""
    post_hoc = sha((root / APPENDIX[0]).read_bytes()) != APPENDIX[1]
    dec = xm.get("decisions", {})
    if "variant_status" not in dec or dec["variant_status"].startswith("NOT_DECIDED"):  # T1-ANALYSIS §1 order (W4 d)
        why = f"§12 decisions not final ({dec.get('variant_status') or dec.get('decision')}); T1-ANALYSIS §1 order"
        return {"label": CP.LABEL, "appendix_sha256": APPENDIX[1], "post_hoc": post_hoc, "sys_version": sys.version,
                "C-M1": {"label": "NOT_RUN", "reason": why}, "C-M2": {"label": "NOT_RUN", "reason": why},
                "main_text": [], "supplement_lines": [f"C-M1 not computed: NOT_RUN {why}", f"C-M2 not computed: NOT_RUN {why}"]}
    missing = {a: m for a, m in missing.items() if m}  # §9.2: ids without a record (cut arms are never A1 / A7 / PVR / A8)
    idn = (xm.get("s2_identity") or {}).get("of_record")
    idn = idn if isinstance(idn, dict) else None
    orr = idn.get("OR_PVR-drop/OR_A7") if idn else None
    t1f = None if orr else "T1-REP §2 not computed"
    if orr:
        for k, a, s0 in (("N_A", "A1", "Dm"), ("N_P", "A1", "Dp")):  # T1-ANALYSIS §3 equality checks (§9.1 item 5)
            if int(get(f"{s0}|{a}")[0]) != idn[k]:
                fault(f"T1-ANALYSIS §3: Σ {s0}_{a} differs from T1-REP §2 {k}")
        for a in arms:  # §9.1 item 6
            hp, hm = get(f"Hp|{a}")[0], get(f"Hm|{a}")[0]
            if abs(100 * hp / (hp + hm) - xm["arms"][a]["of_record"]["P_obj"]["point"]) > 1e-9:
                fault(f"T1-ANALYSIS §9.1 item 6: P_obj^VI({a}) differs from the S16 value")
    v = dec.get("variant")
    vb = xm.get("variants", {}).get(v or "PVR-drop", {})
    return {"label": CP.LABEL, "appendix_sha256": APPENDIX[1], "post_hoc": post_hoc, "sys_version": sys.version,
            **CM.analyse(get, orr, variant=v, missing=missing,
                         degraded=bool(res["a1_decomp"].get(XM, {}).get("DEGRADED")),
                         inconclusive="INCONCLUSIVE" in vb.get("primary_label", ""), post_hoc=post_hoc,
                         t1rep_fault=t1f, arms=[a for a in arms if get.has(f"n|{a}")])}


def write_new(p: Path, b: bytes) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "xb") as f:  # a re-run after a FAULT writes to a new --res (T1-ANALYSIS §9.1)
        f.write(b)


# ---------------------------------------------------------------------------------------------- selftest
VI_CAPS = ["một con chó nằm cạnh cái ghế.", "hai người đi xe máy trên đường.", "một cây dù đỏ và một con mèo.",
           "mèo vàng ở ghế, gốc cây.", "đàn ông giữ cây bút.", "xe máy đỏ đỗ gần nhà.",
           "", "con chó và con mèo chơi trong nhà."]
EN_CAPS = ["a dog on a chair.", "two people ride a motorbike.", "a red umbrella."]


def _dc(text: str, spans: list[tuple[str, list[str]]], chair) -> dict:
    """A synthetic decomposition in the c_pvr.py shape: nouns = every objects_in mention, props = the given spans."""
    ments = CP.vi_mentions(text, chair)
    props = []
    for frag, classes in spans:
        a = text.index(frag)
        b = a + len(frag)
        ms = [[x, y] for n, x, y in ments if a <= x and y <= b and n in classes]
        props.append({"kind": "obj" if classes else "text", "classes": classes, "mentions": ms, "start": a, "end": b,
                      "text": CP.proposition(frag)})
    CP.check_props(props)
    sents = [[m.start(), m.end()] for m in re.finditer(r"[^.!?]+[.!?]?", text) if m.group().strip()]
    sents = [[a + len(text[a:b]) - len(text[a:b].lstrip()), b] for a, b in sents]
    return {"text": text, "sents": sents, "nouns": [[x, y] for _, x, y in ments], "props": props}


def _demos(chair) -> dict:
    return {"d1": _dc("Một con chó nằm trên ghế. Một con mèo ngồi.", [("Một con chó", ["chó"]), ("trên ghế", ["ghế"]),
                                                                       ("Một con mèo", ["mèo"])], chair),
            "d2": _dc("Con chó đen chạy. Con chó trắng ngủ cạnh nhà.", [("Con chó đen", ["chó"]),
                                                                      ("Con chó trắng", ["chó"]), ("cạnh nhà", ["nhà"])], chair),
            "d3": _dc("Hôm nay vui. Một người đi xe máy.", [("Một người", ["người"]), ("đi xe máy", ["xe máy"])], chair),
            "d4": _dc("Cây dù đỏ cạnh con mèo.", [("Cây", ["cây"]), ("cạnh con mèo", ["mèo"])], chair),
            "d5": {"text": "Con chó ngủ.", "sents": [[0, 12]], "nouns": [], "props": [], "decomp_fail": "synthetic"},
            "d6": _dc("Hai con mèo và một cái ghế.", [("Hai con mèo", ["mèo"]), ("một cái ghế", ["ghế"])], chair),
            "d7": _dc("Một chiếc xe máy cạnh nhà.", [("Một chiếc xe máy", ["xe máy"]), ("cạnh nhà", ["nhà"])], chair),
            "d8": _dc("Một đàn ông đứng cạnh xe buýt.", [("Một đàn ông", ["đàn ông"]), ("cạnh xe buýt", ["xe buýt"])], chair)}


def _st_helper(mfn, chair) -> None:
    """The four clauses of T1-REP §2 'removed' (CC-292 N5), the A7 rebuild and created units."""
    dm = _demos(chair)
    m = mfn[""]
    span = survival([dm["d1"]], [[False, True, False]], m)[0]  # clause 1: 'trên ghế' deleted, 'chó' keeps sentence 1
    t1 = CP.rebuild(dm["d1"], [False, True, False])
    assert span["kept"] == {"chó", "mèo"} and span["units"] == {"chó", "ghế", "mèo"} and "nằm" in t1, "span deletion"
    sent = survival([dm["d1"]], [[False, False, True]], m)[0]  # clause 2: sentence 2 loses its only noun and goes
    assert sent["kept"] == {"chó", "ghế"} and "ngồi" not in CP.rebuild(dm["d1"], [False, False, True]), "sentence drop"
    emp = survival([dm["d3"]], [[True, True]], m)[0]  # clause 3: every proposition dropped -> emptied
    assert emp["emptied"] and emp["kept"] == set() and CP.rebuild(dm["d3"], [True, True], emptied=False), "emptied demonstration"
    other = survival([dm["d2"]], [[True, False, False]], m)[0]  # clause 4: chó kept through the second proposition
    assert other["kept"] == {"chó", "nhà"}, "kept through another proposition"
    cr = survival([dm["d5"]], [[]], m)[0]
    assert cr["units"] == set() and cr["created"] == {"chó"}, "created unit of a decomp_fail demonstration"
    a1 = survival([dm["d1"]], None, m)[0]
    assert a1["kept"] == a1["units"] and a1["created"] == set(), "A1 keeps every unit"
    cay = survival([dm["d4"]], None, mfn["cay"])[0]
    assert cay["units"] == {"mèo"} and cay["out"] == {"cây"} and survival([dm["d4"]], None, m)[0]["out"] == set(), "cây scope"
    d9 = _dc("Cây dù đỏ cạnh con mèo.", [("Cây", ["cây"]), ("dù đỏ", []), ("cạnh con mèo", ["mèo"])], chair)
    made = survival([d9], [[False, True, False]], mfn["cay"])[0]  # 'dù' deleted: the 'cây' left is no longer ignored
    assert made["units"] == {"mèo"} and made["created"] == {"cây"} and made["kept"] == {"mèo"}, "created vs units (CC-293 N1)"
    pv = [[True, False, True], [False, True, False]]
    rec = {"PVR-drop": {"masks": pv}}
    a7 = masks_of("A7", "img1", rec)
    assert a7 == CP.a7_masks("img1", pv) and [sum(x) for x in a7] == [2, 1] and masks_of("A1", "img1", rec) is None, "A7 rebuild"


def _st_feats(chair) -> None:
    """Item 15 span features: classifier word boundary, tone placement, and segmenter splits on real token spans."""
    t = "một chiếc xe máy cạnh đàn ông và hai con tòa nhà bacon chó"
    toks = CP.align(t, t.replace("xe máy", "xe_máy").split(), lambda x: chair.norm_tone(x.lower()))
    f = lambda w: span_feats(t, t.index(w), t.index(w) + len(w), chair.norm_tone, toks)  # noqa: E731
    assert f("xe máy") == {"classifier"} and f("đàn ông") == {"split"} and f("tòa nhà") == {"classifier", "tone", "split"}, "features"
    assert f("chó") == set() and span_feats(t, t.index("đàn ông"), t.index("đàn ông") + 7, chair.norm_tone, None) == set(), "no toks"


def _st_fc(mfn, chair) -> None:
    """Item 15 caption-feature columns on one synthetic image (CC-293r2 N-B), and seg_toks's fallbacks."""
    ver = {"yes": 0, "maybe": 0, "no": 0, "parse_fail": 0, "cap_hits": 0, "calls": 0}
    R = {a: {"q1": {"caption": c, **ver}} for a, c in (("PVR-drop", "con chó và mèo."), ("PVR-keep", "chó và mèo."),
                                                         ("A8", "con mèo."))}
    cols, side = xm_columns({"queries": [{"id": "q1", "ranked": []}], "demos": {}}, R, {"q1": {"chó": "present", "mèo": "absent"}},
                            mfn, [*VARIANTS, "A8"], None, chair, None)
    assert [cols[f"FC|classifier|{h}|{a}"] for a in (*VARIANTS, "A8") for h in ("Hp", "Hm")] == [[1], [0], [0], [0], [0], [1]], "FC"
    S = lambda k: sum(cols[k])  # noqa: E731
    assert PF("classifier")("PVR-drop")(S) == 100.0 and PF("classifier")("A8")(S) == 0.0, "PF = Hp / (Hp + Hm)"
    pin = lambda texts: (_ for _ in ()).throw(SystemExit("FAULT: VnCoreNLP-1.2.jar differs from its pin 9e2811cd"))  # noqa: E731
    try:
        seg_toks(["một con chó"], pin, chair.norm_tone)
        raise AssertionError("a segmenter pin FAULT must not be swallowed")
    except SystemExit as e:
        assert "differs from its pin" in str(e), "pin FAULT re-raised"
    calls = []
    flaky = lambda texts: (calls.append(len(texts)), texts[0].split() if len(texts) == 1 else 1 / 0)[1]  # noqa: E731
    out = seg_toks(["một con chó", "hai con mèo"], flaky, chair.norm_tone)
    assert calls == [2, 1, 1] and all(t is not None for t in out), "batch failure -> text by text"
    assert seg_toks(["một con"], lambda texts: [["khác"]], chair.norm_tone) == [None], "an unaligned text gives None"
    caps = {"PVR-drop": "đàn ông và con chó.", "PVR-keep": "đàn ông.", "A8": "con mèo con."}
    words = {"PVR-drop": ["đàn_ông", "và", "con", "chó."], "PVR-keep": ["đàn", "ông."], "A8": ["con", "mèo", "con."]}
    seg = {"demo": {}, "cap": {(a, "q1"): CP.align(c, words[a], lambda x: chair.norm_tone(x.lower())) for a, c in caps.items()}}
    cols2, side2 = xm_columns({"queries": [{"id": "q1", "ranked": []}], "demos": {}},
                              {a: {"q1": {"caption": c, **ver}} for a, c in caps.items()},
                              {"q1": {"đàn ông": "present", "chó": "present", "mèo": "absent"}}, mfn, [*VARIANTS, "A8"], None,
                              chair, seg)
    assert cols2["FC|split|Hp|PVR-drop"] == [0] and cols2["FC|split|Hp|PVR-keep"] == [1], "each caption's own tokens"
    assert not any(v for k, v in side2.items() if k.startswith("cap_split_unavailable")), "tokens found per arm"


def _st_labels() -> None:
    dcs = [{"props": [{}] * 3}, {"props": [{}] * 2}]
    md, mk = [[True, True, False], [False, True]], [[True, False, False], [False, False]]
    rd = {"masks": md, "yes": 2, "no": 1, "maybe": 1, "parse_fail": 1, "cap_hits": 0}
    rk = {**rd, "masks": mk}
    labs, ok = verifier_labels(dcs, rd, rk)
    assert ok and labs == [["REJECTED", "UNCERTAIN", "SUPPORTED"], ["SUPPORTED", "UNCERTAIN"]], "label reconstruction"
    assert not verifier_labels(dcs, rd, {**rk, "no": 0, "maybe": 2})[1], "label counts must agree"
    assert not verifier_labels(dcs, rd, {**rk, "masks": [[True, False, True], [False, False]]})[1], "keep within drop"
    two = {"props": [{"kind": "obj", "classes": ["chó"]}, {"kind": "text", "classes": []}, {"kind": "obj", "classes": ["chó"]}]}
    assert unit_label(two, ["UNCERTAIN", "REJECTED", "REJECTED"], "chó") == "UNCERTAIN", "first proposition's label"


def _st_decide() -> None:
    base = {"P": 50.0, "dR_lo": -1.0, "dC_lo": -1.0, "dA8": 3.0}
    d = decide({"A1": 40.0, "A12": 60.0}, {"PVR-drop": base, "PVR-keep": {**base, "P": 51.0}})
    assert d["SESOI_P"] == 5.0 and d["variant"] == "PVR-drop" and d["go_rule"] is False and d["decision"].startswith("STOP (§12 iv"), "tie -> drop"
    d = decide({"A1": 40.0, "A12": 41.0}, {"PVR-drop": base, "PVR-keep": {**base, "P": 55.0}})
    assert d["SESOI_P"] == 1.0 and d["headroom_stop"] and d["variant"] == "PVR-keep" and d["decision"] == "STOP (headroom, §12 ii)", "floor + headroom"
    d = decide({"A1": 40.0, "A12": 44.0}, {"PVR-drop": {**base, "dR_lo": -2.5}, "PVR-keep": {**base, "P": 49.0}})
    assert d["variant"] == "PVR-keep" and d["go_rule"] and d["decision"] == "GO to tier 2 (§12 iv)", "only keep passes"
    d = decide({"A1": 40.0, "A12": 44.0}, {"PVR-drop": {**base, "dC_lo": -2.0}, "PVR-keep": {**base, "dR_lo": -2.0}})
    assert d["variant"] is None and d["decision"] == "STOP (§6.3 variant)", "none passes (bounds are strict)"
    d = decide({"A1": 40.0, "A12": 44.0}, {"PVR-drop": {**base, "dC_lo": None}, "PVR-keep": base})
    assert d["variant"] is None and d["variant_status"].startswith("NOT_DECIDED: no CIDEr-VI input") and d[
        "decision"] == "NOT_DECIDED (§6.3 variant: no CIDEr-VI input)" and d["go_rule"] is None, "no CIDEr-VI input (W4)"
    d = decide({"A1": 40.0, "A12": 41.0}, {"PVR-drop": {**base, "dC_lo": None}, "PVR-keep": base}, "cap stop")
    assert d["decision"] == "STOP (headroom, §12 ii)" and d["variant_status"].endswith("(cap stop)"), "headroom first (W4)"
    d = decide({"A1": 40.0, "A12": 60.0}, {"PVR-drop": base, "PVR-keep": {**base, "P": 53.0}})
    assert d["variant"] == "PVR-keep", "SESOI_P / 2 <= |ΔP| < SESOI_P: the higher variant"
    d = decide({"A1": 40.0, "A12": 42.0}, {"PVR-drop": {**base, "dA8": 1.0}, "PVR-keep": {**base, "P": 49.0}})
    assert not d["headroom_stop"] and d["go_rule"] and d["decision"] == "GO to tier 2 (§12 iv)", "boundaries: 2.0 and SESOI_P"


def _st_headline() -> None:
    e = lambda p, lo, hi: {"point": p, "ci": [lo, hi]}  # noqa: E731
    h = headline(e(-2, -3, -1), e(-1, -2, -0.5), e(2, 1, 3), e(1.0, 0.5, 2), True)
    assert h["sentence_id"] == "HW-La" and h["HW-2"] and "verification reduced that loss" in h["sentence"], "La + harm"
    h = headline(e(-2, -3, -1), e(0.1, -1, 1), e(0.5, -1, 2), e(0.5, -0.2, 1), False)
    assert h["sentence_id"] == "HW-1b" and "was not shown to reduce" in h["sentence"], "1b + harm not shown"
    h = headline(e(1, -1, 2), e(2, 1, 3), e(2, 1, 3), e(1, 0.2, 2), True)
    assert h["sentence_id"] == "HW-3" and h["HW-2"] is None and h["tier1_label"] == "dev go (§12 iv)", "HW-3"
    assert h["sentence"].startswith("With this datastore (KTVIC and OpenViIC training captions), verifying"), "HW-3 datastore"
    h = headline(e(-2, -3, -1), e(2, 1, 3), e(0.2, -1, 1), e(1, 0.2, 2), False)
    assert h["sentence_id"] == "HW-0" and h["HW-2"] and "verification" not in h["sentence"], "HW-0, no harm clause"
    h = headline(e(-1, -2, 0.5), e(0, -1, 1), e(2, 1, 3), e(0, -1, 1), True)
    assert h["sentence_id"] == "HW-1a" and h["HW-2"] is None and "loss" not in h["sentence"], "HW-1a; HW-2 needs CI < 0"
    assert headline(e(1, -1, 2), e(-2, -3, -1), e(0, -1, 1), e(0, -1, 1), False)["sentence_id"] == "HW-Lb", "HW-Lb"


def _st_text() -> None:
    s = text_stats(["Một con chó, con chó.", "a fox jumps", ""], ["eos", "length", "other"])
    assert s["empty_share"] == 1 / 3 and s["truncation_share"] == 1 / 3 and s["repeated_3gram_share"] == 0, "item 9 shares"
    assert abs(s["vi_token_share"] - 6 / 8) < 1e-12 and abs(s["vi_script_share"] - 1 / 3) < 1e-12, "VI letters (no f j w z)"
    assert s["distinct_1"] == 6 / 8 and s["mean_syllables"] == 8 / 3, "distinct-1 and length"
    assert text_stats(["con chó con chó con chó"], ["a8"])["repeated_3gram_share"] == 1.0, "repeated 3-gram"
    assert text_stats(["x"], ["a8"])["truncation_share"] is None, "A8 decodes nothing"
    assert VI_SPECIFIC.search("é") and not VI_SPECIFIC.search("abc") and VI_TOKEN.fullmatch("người") and not VI_TOKEN.fullmatch("fw"), "regexes"


def _st_est() -> None:
    reps = np.r_[np.ones(980), np.full(20, np.nan)]
    get = lambda k: (1.0, reps)  # noqa: E731
    soft = est(get, lambda S: S("x"), strict=False)
    assert soft["dropped"] == 20 and soft["note"].startswith("> 1 % undefined"), "drops counted, N3 note"
    try:
        est(get, lambda S: S("x"))
        raise AssertionError("2 % undefined replicates must FAULT (prereg §5.5)")
    except SystemExit as e:
        assert str(e).startswith("FAULT"), "prereg §5.5"
    ok = np.r_[np.ones(990), np.full(10, np.nan)]
    e = est(lambda k: (1.0, ok), lambda S: S("x"), contrast=True)
    assert e["dropped"] == 10 and e["p"] == 0.0 and e["ci"] == [1.0, 1.0], "1 % is allowed"
    o = {"OR_PVR-drop/OR_A7": {"ci": [0.5, 0.99]}}
    yes = {"point": 1.0, "holm_reject": True}
    assert method_name(o, yes)["name"] == "verification", "rules (i) and (ii)"
    assert method_name({"OR_PVR-drop/OR_A7": {"ci": [0.5, 1.0]}}, yes)["name"] == "filtering", "(i) CI wholly below 1"
    assert method_name(o, {**yes, "holm_reject": False})["name"] == "filtering", "(ii) Holm"
    assert method_name(o, {**yes, "point": -1.0})["name"] == "filtering", "(ii) direction V > A7"


def _st_guard() -> None:
    ids = {s: [f"{s}{j}" for j in range(n)] for s, n in zip(GUARD_SETS, (30, 90))}
    g = np.random.default_rng(5)
    cider = {s: {"A1": {i: 50.0 for i in ids[s]}, "PVR-drop": {i: 50.0 + g.normal(0, 3) for i in ids[s]},
                 "PVR-keep": {i: 45.0 + g.normal(0, 3) for i in ids[s]}} for s in GUARD_SETS}
    a, b = guard_g1(cider, ids, "PVR-drop"), guard_g1(cider, ids, "PVR-keep")
    assert a["passes"] and not b["passes"] and a["n"] == 120 and abs(b["point"] + 5) < 1.5, "δ_C on pooled G1"
    assert guard_g1(cider, ids, "PVR-drop") == a, "deterministic"
    flat = {s: {"A1": {i: 0.0 for i in ids[s]}, "PVR-drop": {i: -10.0 * (s == "ktvic_explore") for i in ids[s]}}
            for s in GUARD_SETS}
    fl = guard_g1(flat, ids, "PVR-drop")
    assert fl["ci"] == [-2.5, -2.5], "stratified: the source weights stay fixed"
    assert fl["per_set"]["ktvic_explore"]["ci"] == [-10.0, -10.0] and fl["per_set"]["openviic_explore"]["ci"] == [0.0, 0.0], "per-set CIs"
    noisy = {s: {"A1": {i: 0.0 for i in ids[s]}, "PVR-drop": {i: -1.5 + (8.0 if j % 2 else -8.0) for j, i in enumerate(ids[s])}}
             for s in GUARD_SETS}
    nz = guard_g1(noisy, ids, "PVR-drop")
    assert abs(nz["point"] + 1.5) < 1e-12 and nz["ci"][0] < -DELTA_C and not nz["passes"], "δ_C on the CI lower bound"


def _world(base: Path, chair, mfn, cut=("A10",), tweak=None) -> argparse.Namespace:
    """A synthetic pulled run: manifests (TMAN), outputs + SUMS, CAP.json, a1_decomp, labels and class names."""
    g = np.random.default_rng(11)
    dm = _demos(chair)
    dids = list(dm)
    names = sorted({n for v in json.loads((ROOT / "data/xm3600/vi_oiv7_map.json").read_text("utf-8")).values()
                    if isinstance(v, dict) for n in v.get("pos", []) + v.get("neg", [])})
    base.mkdir(parents=True)
    desc = base / "desc.csv"
    desc.write_text("".join(f"/m/x{j},{n}\n" for j, n in enumerate(names)), "utf-8")
    vmap = XO.resolve_map(desc)
    build, out = base / "build", base / "pull"
    (build / "manifest").mkdir(parents=True)
    (out / "out" / "logs").mkdir(parents=True)  # the real pull layout: outputs, ids-only logs, job logs
    labels, sums, man = {}, {}, []
    for s, (_, lang, arms) in G.SETS.items():
        n = 40 if s == XM else 4
        qs = [{"id": f"{s[:2]}{j:03d}", "image": "x.jpg", "image_sha256": "0" * 64,
               "ranked": [*(dids[(j + k) % 7] for k in range(3)), "d8", *(dids[(j + k) % 7] for k in range(3, 6))]}
              for j in range(n)]  # d8 sits at rank 4 only, so a top-3 slice would miss it (CC-293r2 N-B)
        M = {"label": CP.LABEL, "set": s, "datastore": G.SETS[s][0], "queries": qs, "demos": dm}
        b = json.dumps(M, ensure_ascii=False).encode()
        (build / "manifest" / f"{s}.json").write_bytes(b)
        man.append(f"{sha(b)}  manifest/{s}.json\n")
        for q in qs:
            if s == XM:
                labels[q["id"]] = {"pos": sorted(g.choice(sorted(vmap["chó"]["pos"] | vmap["ghế"]["pos"] | vmap["người"]["pos"]), 1)),
                                   "neg": sorted(g.choice(sorted(vmap["mèo"]["neg"] | vmap["xe máy"]["neg"] | vmap["cây"]["neg"]), 2))}
        for a in sorted(arms, key=lambda a: a != "PVR-drop"):  # A7 reads PVR-drop's masks
            if a in cut:
                continue
            rows = []
            for j, q in enumerate(qs):
                i, ds = q["id"], [str(x) for x in q["ranked"][:CP.K]]
                r = {"utc": f"2026-11-08T0{j % 10}:00:{j % 60:02d}Z", "set": s, "arm": a, "id": i, "tpl": "t",
                     "finish": "a8" if a in ("A8", "S2") else "length" if j % 9 == 0 else "eos",
                     "caption": (VI_CAPS if lang == "vi" else EN_CAPS)[(j * 3 + {"A8": 5}.get(a, 2 if a in VARIANTS else len(a))) % (len(VI_CAPS) if lang == "vi" else len(EN_CAPS))],
                     "demo_ids": [] if a in ("A0", "A8") else ds}
                if a in ("PVR-drop", "PVR-keep", "A8"):
                    lab = [("SUPPORTED", "UNCERTAIN", "REJECTED")[(j + k) % 3] for k in range(sum(len(dm[d]["props"]) for d in ds))]
                    gone = {"PVR-drop": {"REJECTED", "UNCERTAIN"}, "PVR-keep": {"REJECTED"}, "A8": set()}[a]
                    masks = CP.split_back([dm[d] for d in ds], [x in gone for x in lab])
                    r.update(calls=len(lab), cap_hits=0, parse_fail=lab.count("UNCERTAIN") // 2, yes=lab.count("SUPPORTED"),
                             no=lab.count("REJECTED"), maybe=lab.count("UNCERTAIN") - lab.count("UNCERTAIN") // 2)
                    if a == "A8":
                        r["emptied"] = False
                    else:
                        r.update(masks=masks, emptied=CP.demos_after([dm[d] for d in ds], masks)[1])
                rows.append(r)
            if a == "A7":
                pv = {r["id"]: r["masks"] for r in (json.loads(x) for x in (out / "out" / f"{s}.PVR-drop.jsonl").read_text().splitlines())}
                for r in rows:
                    r["emptied"] = CP.demos_after([dm[d] for d in r["demo_ids"]], CP.a7_masks(r["id"], pv[r["id"]]))[1]
            if tweak:
                tweak(s, a, rows)
            b = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows).encode()
            (out / "out" / f"{s}.{a}.jsonl").write_bytes(b)
            sums[f"out/{s}.{a}.jsonl"] = sha(b)
            lg = "".join(json.dumps({k: r[k] for k in ("utc", "set", "arm", "id")}, sort_keys=True) + "\n" for r in rows).encode()
            (out / "out" / "logs" / f"{s}.{a}.ids.jsonl").write_bytes(lg)
            sums[f"out/logs/{s}.{a}.ids.jsonl"] = sha(lg)
    (build / "MANIFEST.sha256").write_text("".join(man))
    (out / "logs").mkdir()
    (out / "logs" / "job.log").write_bytes(b"synthetic\n")
    sums["logs/job.log"] = sha(b"synthetic\n")
    (out / "SUMS").write_text("".join(f"{h}  {k}\n" for k, h in sorted(sums.items())))
    (base / "labels.json").write_text(json.dumps(labels), "utf-8")
    (base / "cap.json").write_text(json.dumps({"decision": "RUN", "arms": [], "cuts": list(cut)}))
    a1 = base / "a1d"
    a1.mkdir()
    mm = []
    for s in G.SETS:
        bad = {"t_a": 4, "ktvic_explore": 3, "openviic_explore": 2}.get(s, 0)  # 2 of 4 = 50 %: not above it
        dec = {f"{s[:2]}{j:03d}": ({"decomp_fail": "x"} if j < bad else {}) for j in range(40 if s == XM else 4)}
        b = json.dumps(dec).encode()
        (a1 / f"{s}.json").write_bytes(b)
        mm.append(f"{sha(b)}  {s}.json\n")
    (a1 / "MANIFEST.sha256").write_text("".join(mm))
    ns = argparse.Namespace(root=ROOT, build=build, tman=sha((build / "MANIFEST.sha256").read_bytes()), out=out,
                            sums="SUMS", cap=base / "cap.json", a1_decomp=a1, labels=base / "labels.json", desc=desc,
                            cider=None, cider_sha=None, no_cider="selftest world without CIDEr-VI", emb=[], res=base / "res",
                            rerun_of=None)
    return ns


def _cider_file(base: Path, x) -> None:
    Ms = manifests(x.build, x.tman)
    g = np.random.default_rng(2)
    c = {s: {a: {q["id"]: float(40 + g.normal(0, 2) + (a == "PVR-keep") * -6) for q in Ms[s]["queries"]}
             for a in ("A0", "A1", "A8", *VARIANTS)} for s in (XM, *GUARD_SETS)}
    p = base / "cider.json"
    p.write_text(json.dumps(c))
    x.cider, x.cider_sha, x.no_cider = p, sha(p.read_bytes()), None


def _st_world(tmp: Path, mfn, chair, boot) -> None:
    fake = lambda caps: [{"decomp_fail": "x"} if not c else {} for c in caps]  # noqa: E731  decomposer stand-in
    segf = lambda texts: [t.replace("xe máy", "xe_máy").split() for t in texts]  # noqa: E731  RDR stand-in: joins one compound
    x = _world(tmp / "w1", chair, mfn)
    _cider_file(tmp / "w1", x)
    res, cm = score(x, boot, fake, pins=False, segment=segf)
    xm = res[XM]
    vb = xm["variants"]["PVR-drop"]
    assert isinstance(xm["by_type"]["F|split"], dict) and isinstance(vb["dP_by_feature"]["split"], dict), "item 15 split"
    assert vb["dP_by_type"]["text"].startswith("NOT_COMPUTED") and "ci" in xm["guard_G1"]["PVR-drop"]["per_set"]["ktvic_explore"], "W2"
    assert res["similarity"].startswith("NOT_COMPUTED") and "cut" in vb["holm"] and "partial" in vb["holm"], "no silent drop-outs"
    assert xm["s1_verifier_table"]["unit_label_conflicts"] > 0, "N9 count: d2 carries 'chó' in two propositions"
    sp = {k: v for k, v in xm["side_counts"].items() if k.startswith(("cap_split_unavailable", "demo_split_unavailable"))}
    assert len(sp) == 4 and not any(sp.values()), "every demonstration and caption has segmenter tokens (N-B)"
    assert res["status"][XM]["A10"].startswith("cut by") and "A10" in xm["variants"]["PVR-drop"]["holm"]["cut"], "cut arm"
    assert xm["variants"]["PVR-drop"]["holm"]["members"] == ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A9", "A11"], "Holm members"
    assert [res["a1_decomp"][s]["DEGRADED"] for s in ("t_a", "ktvic_explore", "openviic_explore", XM)] == [
        True, True, False, False], "DEGRADED: M > 50 % of N"
    a1r = xm["arms"]["A1"]["of_record"]
    c = a1r["counts"]
    assert a1r["P_obj"]["point"] == 100 * c["Hp"] / (c["Hp"] + c["Hm"]) and a1r["P_obj_wrong"]["point"] == 100 * c["Hp"] / c["n"], "P rules"
    pv = xm["arms"]["PVR-drop"]["of_record"]["P_obj"]["point"] - xm["arms"]["A8"]["of_record"]["P_obj"]["point"]
    pw = xm["arms"]["PVR-drop"]["of_record"]["P_obj_wrong"]["point"] - xm["arms"]["A8"]["of_record"]["P_obj_wrong"]["point"]
    assert abs(xm["variants"]["PVR-drop"]["primary"]["point"] - pv) < 1e-12 and abs(pv - pw) > 1e-6, "primary: unknown out"
    assert res["B"] == 10_000 and res["seed"] == 20261102, "prereg §5.5 settings"
    a1 = xm["arms"]["A1"]["of_record"]["counts"]
    assert a1["Hp"] + a1["Hm"] + a1["U"] == a1["n"] and xm["arms"]["A1"]["of_record"]["P_obj"]["dropped"] == 0, "counts"
    assert xm["s1_verifier_table"]["status"] == "OK" and sum(xm["s1_verifier_table"]["cells"].values()) > 0, "§1 table"
    idn = xm["s2_identity"]["of_record"]
    assert "OR_PVR-drop/OR_A7" in idn and idn["OR_PVR-keep/OR_A7"]["label"] == "not count-matched", "§2 ratios"
    assert xm["side_counts"]["out|"] == 0 and xm["side_counts"]["out|cay"] > 0, "cây scope on units"
    assert xm["side_counts"]["created|PVR-drop|"] > 0, "decomp_fail demonstrations create units, counted"
    assert any(e["sentence_id"].startswith("HW") for e in (xm["variants"][v]["headline"] for v in VARIANTS)), "headline"
    assert xm["decisions"]["variant"] in VARIANTS and xm["guard_G1"]["PVR-keep"]["passes"] is False, "variant via G1"
    assert res["sets"][XM]["A1"]["segmenter_fail_rate"] == 5 / 40 and res["sets"]["kt_c"]["S3"]["segmenter_fail_rate"].startswith("n/a"), "segmenter"
    assert res["sets"][XM]["A1"]["cay_ignored"] > 0 and xm["method_name"]["name"] in ("verification", "filtering"), "cây + name"
    assert cm["C-M1"]["label"] in ("IDENTIFIED", "NOT_IDENTIFIED (G1)", "NOT_IDENTIFIED (G2)") and not cm["post_hoc"], "C-M1 ran"
    assert cm["C-M2"]["pvr"] == xm["decisions"]["variant"] and "per_arm" in cm["C-M2"], "C-M2 ran"
    assert (tmp / "w1/res/score_tier1.json").exists() and (tmp / "w1/res/cm_tier1.json").exists(), "written"
    try:
        score(x, boot, fake, pins=False)
        raise AssertionError("an existing --res must be refused")
    except FileExistsError:
        pass
    x2 = _world(tmp / "w2", chair, mfn)
    res2, cm2 = score(x2, boot, None, pins=False)
    assert res2[XM]["by_type"]["F|split"] == NO_SPLIT == res2[XM]["variants"]["PVR-keep"]["dP_by_feature"]["split"], "split reason"
    assert res2["sets"][XM]["A1"]["segmenter_fail_rate"].startswith("NOT_COMPUTED"), "segmenter reason"
    assert res2[XM]["decisions"]["variant_status"].startswith("NOT_DECIDED") and not cm2["main_text"], "no CIDEr input"
    assert res2[XM]["decisions"]["decision"] == "STOP (headroom, §12 ii)", "W4: a headroom STOP still comes first"
    assert res2["inputs"]["cider"] == {"no_cider": "selftest world without CIDEr-VI"}, "W4 (a) reason recorded"
    assert cm2["C-M1"]["label"] == cm2["C-M2"]["label"] == "NOT_RUN" and "not final" in cm2["C-M2"]["reason"], "§1 order"
    faults = {
        "emptied": lambda s, a, rows: s == XM and a == "PVR-drop" and rows[0].update(emptied=rows[0]["emptied"] + 1),
        "demo_ids": lambda s, a, rows: s == XM and a == "A7" and rows[1].update(demo_ids=rows[1]["demo_ids"][::-1]),
        "shape": lambda s, a, rows: s == XM and a == "PVR-keep" and rows[2]["masks"][0].append(False),
        "dup": lambda s, a, rows: s == "kt_c" and a == "S1" and rows.append(dict(rows[0])),
        "keys": lambda s, a, rows: s == XM and a == "A3" and rows[0].update(prompt="x"),
    }
    for n, tw in faults.items():
        xf = _world(tmp / f"f_{n}", chair, mfn, tweak=tw)
        try:
            score(xf, boot, None, pins=False)
            raise AssertionError(f"FAULT {n} not raised")
        except SystemExit as e:
            assert str(e).startswith("FAULT"), n
    xt = _world(tmp / "f_torn", chair, mfn)
    p = xt.out / "out" / f"{XM}.A2.jsonl"
    p.write_bytes(p.read_bytes()[:-1])
    (xt.out / "SUMS").write_text("".join(f"{sha(p.read_bytes()) if k == f'out/{XM}.A2.jsonl' else h}  {k}\n"
                                         for k, h in sums_of(xt.out / "SUMS").items()))
    xm_ = _world(tmp / "f_tman", chair, mfn)
    xm_.tman = "0" * 64
    xj = _world(tmp / "f_nc_done", chair, mfn)
    (xj.out / "SHA256SUMS_tier1").write_bytes((xj.out / "SUMS").read_bytes())
    xj.sums = "SHA256SUMS_tier1"
    xn = _world(tmp / "f_neither", chair, mfn)
    xn.no_cider = None
    xb = _world(tmp / "f_both", chair, mfn)
    _cider_file(tmp / "f_both", xb)
    xb.no_cider = "both given"
    xq = _world(tmp / "f_nosha", chair, mfn)
    _cider_file(tmp / "f_nosha", xq)
    xq.cider_sha = None
    bad_c = {}
    for tag, val in (("nan", float("nan")), ("big", 1000.5), ("neg", -0.1), ("bool", True)):
        bad_c[tag] = _world(tmp / f"f_c_{tag}", chair, mfn)
        _cider_file(tmp / f"f_c_{tag}", bad_c[tag])
        c = json.loads(bad_c[tag].cider.read_text())
        c["openviic_explore"]["PVR-keep"][next(iter(c["openviic_explore"]["PVR-keep"]))] = val
        bad_c[tag].cider.write_text(json.dumps(c))
        bad_c[tag].cider_sha = sha(bad_c[tag].cider.read_bytes())
    xc = _world(tmp / "f_cut", chair, mfn, cut=())
    xc.cap.write_text(json.dumps({"decision": "RUN", "arms": [], "cuts": ["A10"]}))
    xs = _world(tmp / "f_sums", chair, mfn)
    xa = _world(tmp / "f_a0", chair, mfn)
    _cider_file(tmp / "f_a0", xa)
    c = json.loads(xa.cider.read_text())
    del c[XM]["A0"]
    xa.cider.write_text(json.dumps(c))
    xa.cider_sha = sha(xa.cider.read_bytes())
    xu = _world(tmp / "f_unreg_log", chair, mfn)  # an ids-log name of no registered (set, arm) still FAULTs
    (xu.out / "out" / "logs" / f"{XM}.A99.ids.jsonl").write_bytes(b"{}\n")
    with open(xu.out / "SUMS", "a") as f:
        f.write(f"{sha(b'{}' + bytes([10]))}  out/logs/{XM}.A99.ids.jsonl\n")
    xg = _world(tmp / "f_log_sha", chair, mfn)  # an ids-log whose bytes no longer match its SUMS line
    (xg.out / "out" / "logs" / f"{XM}.A2.ids.jsonl").write_bytes(b"{}\n")
    xd = _world(tmp / "f_done", chair, mfn, tweak=lambda s, a, rows: s == XM and a == "A3" and rows.pop())
    _cider_file(tmp / "f_done", xd)  # with CIDEr-VI input, so the N4 completeness check is the one that fires
    (xd.out / "SHA256SUMS_tier1").write_bytes((xd.out / "SUMS").read_bytes())
    xd.sums = "SHA256SUMS_tier1"
    xr = _world(tmp / "f_rerun", chair, mfn)
    xr.rerun_of = "not an id"
    p = xs.out / "out" / f"{XM}.A2.jsonl"
    p.write_bytes(p.read_bytes().replace(b'"eos"', b'"length"', 1))
    xp = _world(tmp / "w3", chair, mfn, tweak=lambda s, a, rows: s == XM and a == "A7" and rows.pop())
    _cider_file(tmp / "w3", xp)
    res3, cm3 = score(xp, boot, None, pins=False)
    assert res3["status"][XM]["A7"].startswith("partial") and cm3["C-M1"] == {"label": "NOT_RUN", "missing": {"A7": 1}}, "§9.2 NOT_RUN"
    assert "A7" not in res3[XM]["variants"]["PVR-drop"]["holm"]["members"], "an incomplete arm leaves the family"
    WHY = {"unregistered_log": "no registered (set, arm)", "ids_log_sha": "ids-only logs differ", "job_done_partial": "incomplete uncut arms", "no_cider_job_done": "--no-cider under a JOB DONE pull",
           "neither_cider_flag": "exactly one", "both_cider_flags": "exactly one", "cider_without_sha": "exactly one",
           "cider_no_A0": "lacks", **{f"cider_{t}": "non-finite value or one outside" for t in bad_c}}
    for name, fn in (("sums", lambda: score(xs, boot, None, pins=False)), ("torn", lambda: score(xt, boot, None, pins=False)),
                     ("unregistered_log", lambda: score(xu, boot, None, pins=False)), ("ids_log_sha", lambda: score(xg, boot, None, pins=False)),
                     ("tman", lambda: score(xm_, boot, None, pins=False)), ("cut_with_output", lambda: score(xc, boot, None, pins=False)),
                     ("job_done_partial", lambda: score(xd, boot, None, pins=False)), ("cider_no_A0", lambda: score(xa, boot, None, pins=False)), ("rerun_id", lambda: score(xr, boot, None, pins=False)),
                     ("no_cider_job_done", lambda: score(xj, boot, None, pins=False)), ("neither_cider_flag", lambda: score(xn, boot, None, pins=False)),
                     ("both_cider_flags", lambda: score(xb, boot, None, pins=False)), ("cider_without_sha", lambda: score(xq, boot, None, pins=False)),
                     *((f"cider_{t}", lambda w=w: score(w, boot, None, pins=False)) for t, w in bad_c.items()),
                     ("raw_tone", lambda: (os.environ.__setitem__("RESCAP_RAW_TONE", "0"), score(_world(tmp / "f_rt", chair, mfn), boot, None, pins=False)))):
        try:
            fn()
            raise AssertionError(f"FAULT {name} not raised")
        except SystemExit as e:
            assert str(e).startswith("FAULT") and WHY.get(name, "") in str(e), (name, str(e)[:120])
        finally:
            os.environ.pop("RESCAP_RAW_TONE", None)
    xl = _world(tmp / "w4", chair, mfn, tweak=lambda s, a, rows: s == XM and a == "PVR-keep" and rows[0].update(no=rows[0]["no"] + 1))
    xl.rerun_of = "OPS-1108c-selftest"
    r4, c4 = score(xl, boot, None, pins=False)
    t4 = r4[XM]["s1_verifier_table"]
    assert t4["status"].startswith("FALLBACK") and t4["kappa"].startswith("NOT_COMPUTABLE") and t4["cells_status"].startswith(
        "reconstructed") and "precision_REJECTED_absent_keep_run" in t4, "N2 §1 fallback"
    t1 = xm["s1_verifier_table"]  # same masks in w1: each run read alone equals the reconstruction's cells there
    assert all(abs(t4[k + r]["point"] - t1[k]["point"]) < 1e-12 for k, r in (
        ("precision_REJECTED_absent", "_keep_run"), ("recall_REJECTED_absent", "_keep_run"),
        ("SUPPORTED_share_present", "_drop_run"))), "N2 per-run statistics"
    assert r4["rerun"].startswith("re-run after FAULT OPS-1108c-selftest, code ") and r4["rerun"] in c4["label"], "N10 stamp"
    global APPENDIX
    keep, APPENDIX = APPENDIX, (APPENDIX[0], "0" * 64)  # any other appendix sha = POST_HOC (T1-ANALYSIS §9.4)
    try:
        xh = _world(tmp / "w5", chair, mfn)
        _cider_file(tmp / "w5", xh)
        _, c5 = score(xh, boot, None, pins=False)
    finally:
        APPENDIX = keep
    txt = (xh.res / "cm_tier1.json").read_text("utf-8")
    assert c5["post_hoc"] and c5["C-M1"]["label"] == c5["C-M2"]["label"] == "POST_HOC" and not c5["main_text"], "POST_HOC"
    oracle = re.compile(r'IDENTIFIED|E1_|OVERID_|SIGN_|PLACEBO_|"K[1-5]"|INCONCLUSIVE|DEGRADED')  # independent of CM.LABELS
    assert not oracle.search(txt) and '"case"' not in txt and '"kappa_minus"' in txt, "CC-293 W1: no label in the written record"
    top = lambda s, a, rows: s == XM and a == "A12" and [r.update(caption="con chó, cái ghế, người.") for r in rows]  # noqa: E731
    x6 = _world(tmp / "w6", chair, mfn, tweak=top)  # W4 (e): a cap-stop pull, no CIDEr-VI input, no headroom STOP
    (x6.out / "SHA256SUMS_tier1_cap").write_bytes((x6.out / "SUMS").read_bytes())
    x6.sums, x6.no_cider = "SHA256SUMS_tier1_cap", "cap stop: the CIDEr-VI producer refuses partial arms"
    r6, c6 = score(x6, boot, None, pins=False)
    d6, v6 = r6[XM]["decisions"], r6[XM]["variants"]["PVR-drop"]
    assert not d6["headroom_stop"] and d6["decision"] == "NOT_DECIDED (§6.3 variant: no CIDEr-VI input)", "W4 (c) decision"
    assert d6["variant"] is None and d6["go_rule"] is None and d6["variant_status"].endswith(f"({x6.no_cider})"), "W4 (c) status"
    assert r6[XM]["arms"]["A1"]["of_record"]["P_obj"]["point"] is not None and v6["primary"]["ci"] and v6["holm"]["rows"], "W4 registered"
    assert all(r6[XM][k].startswith("NOT_COMPUTED") for k in ("guard_G1",)) and v6["dCIDEr_xm_A1"].startswith("NOT_COMPUTED") \
        and r6[XM]["A1_minus_A0"]["CIDEr"].startswith("NOT_COMPUTED"), "W4 (c) CIDEr items"
    assert c6["C-M1"]["label"] == c6["C-M2"]["label"] == "NOT_RUN" and len(c6["supplement_lines"]) == 2, "W4 (d)"


def selftest(root: Path = ROOT) -> None:
    load(root)
    os.environ.pop("RESCAP_RAW_TONE", None)
    chair, _ = CP.rescap_mods(root)
    mfn = mention_fns(root)
    boot = CM.boot_fn(root)
    with tempfile.TemporaryDirectory(prefix="c_pvr_score_st_") as t:
        cases = {"helper_four_clauses": lambda: _st_helper(mfn, chair), "verifier_labels": _st_labels,
                 "features": lambda: _st_feats(chair), "feature_columns": lambda: _st_fc(mfn, chair), "decide_branches": _st_decide, "headline_cases": _st_headline, "text_stats": _st_text, "est_and_name": _st_est,
                 "guard_G1": _st_guard, "world": lambda: _st_world(Path(t), mfn, chair, boot)}
        for name, fn in cases.items():
            try:
                fn()
            except (Exception, SystemExit) as e:  # a crash inside a named case is that case's failure
                raise SystemExit(f"selftest FAILED: {name} ({type(e).__name__}: {e})")
    print(f"c_pvr_score selftest ok ({len(cases)} cases)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("selftest")
    s = sp.add_parser("score")
    s.add_argument("--tier", type=int, choices=[1], required=True)
    for k in ("out", "build", "cap", "a1_decomp", "res"):
        s.add_argument(f"--{k.replace('_', '-')}", type=Path, required=True)
    s.add_argument("--sums", required=True, help="SHA256SUMS_tier1, or SHA256SUMS_tier1_cap after a cap stop (S11 §13)")
    s.add_argument("--tman", required=True)
    s.add_argument("--cider", type=Path, help="per-image CIDEr-VI {set: {arm: {id: score}}} from the pinned producer")
    s.add_argument("--cider-sha")
    s.add_argument("--no-cider", metavar="REASON", help="cap-stop or STOP pull only: §6.3 (iii), §12 (iv) NOT_DECIDED")
    s.add_argument("--emb", action="append", default=[], help="SET=QUERY_NPZ,DEMO_NPZ (T1-REP §4 similarity)")
    s.add_argument("--no-segment", action="store_true")
    s.add_argument("--rerun-of", help="OPS id of the FAULT this run follows (T1-ANALYSIS §9.1)")
    a = ap.parse_args()
    if a.cmd == "selftest":
        return selftest()
    load()
    a.root, a.labels, a.desc = ROOT, ROOT / GOLD["labels"][0], ROOT / GOLD["desc"][0]
    dec = None if a.no_segment else (lambda caps: CP.decompose_vi(caps, ROOT))
    res, cm = score(a, CM.boot_fn(), dec, segment=None if a.no_segment else CP.rdr)
    xm = res[XM]
    print(f"{CP.LABEL}: {xm.get('decisions', {}).get('decision')}; C-M1 {cm['C-M1']['label']}; C-M2 {cm['C-M2']['label']} "
          f"-> {a.res}")


if __name__ == "__main__":
    main()
