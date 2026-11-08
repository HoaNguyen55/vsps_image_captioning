#!/usr/bin/env python3
"""CIDEr-VI producer for the C-PVR-T1 guard (Paper C; CIDER_VI_PIN_v1.md; CC-293 Ruling 4). DRAFT, not judge-read.
It writes the per-image file that `c_pvr_score.py score --cider F --cider-sha H` consumes (as written, the gating
column) and its trailing-punctuation-stripped twin (descriptive only), then prints a record of shas and counts.

    PY=~/.venvs/c_pvr_cider/bin/python     (scripts/c_pvr/requirements_c_pvr_cider.lock: numpy 2.5.4, scipy 1.18.1,
                                            pycocoevalcap 1.2; CPython 3.12.3; JDK 21 + VnCoreNLP 62bbc58f as c_pvr)
    $PY -I -B scripts/c_pvr/c_pvr_cider_vi.py selftest     synthetic text in a temp dir; no data file is opened
    $PY -I -B scripts/c_pvr/c_pvr_cider_vi.py mutants      each mutant must make the selftest fail
    $PY -I -B scripts/c_pvr/c_pvr_cider_vi.py score --out $PULL/final/c_pvr_out --sums SHA256SUMS_tier1 --build $O
        --tman $TMAN --res DIR

Form (pin §2-§5): kit_b protocol_pilot.Cider 6aee4282 (pycocoevalcap CIDEr-D: n = 4, σ = 6, ×100) with its default
DF, i.e. the references of the scored images only, one Cider per source set (T1-GUARD G-7). Text, the same for
references and captions: CP.clean (NFC, whitespace runs -> one space) -> CP.rdr (VnCoreNLP-1.2 wseg, pinned) -> words
joined by one space -> str.lower(). As written keeps every punctuation token. Stripped applies
punctuation_audit.strip_trailing_punct_tokens to the caption tokens only; references and DF are unchanged.
Every integrity check runs before the segmenter. No caption or reference text is printed or written.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
GPU = ("scripts/c_pvr_gpu/c_pvr_gpu.py", "9a9c6eb57ee09575a1c69604fa48c506fe8c64d747754b6f8d9c1ced12a1a260")
KIT = {"protocol_pilot": ("scripts/kit_b/protocol_pilot.py",  # c_stage1/score.py KIT_B
                          "6aee428207a2d1a045cd72d054e26a2e2ac8d9c2e414cb0c161e3b95dffd92bf"),
       "punctuation_audit": ("scripts/kit_b/punctuation_audit.py",
                             "a7e8024030f56cbff07124278cd631964b7b1197607426d7212fd665b6c2f9b1")}
XM_REFS = ("data/datasets/xm3600/full_data.json",  # W25 RULE.md; prereg v1.2 §2.4; b_pa1 xm3600_all
           "101d24ad98e9dec43625ee425fa1b49aa1bde98f9609945bf5dd4424fef1dacc")
JDK = "21.0.12.1"  # PINS-A §4.2 l.225 and A6; requirements_c_pvr.lock (CC-294 W1: asserted, not only recorded)
XM, GUARD, VARIANTS = "xm3600_vi", ("ktvic_explore", "openviic_explore"), ("PVR-drop", "PVR-keep")
ARMS = {XM: ("A0", "A1", *VARIANTS), **{s: ("A1", *VARIANTS) for s in GUARD}}  # CC-293 Ruling 4 (d); cider_in need
G = CP = CR = E4 = PA = CODE_ROOT = None


def fault(msg: str):
    raise SystemExit(f"FAULT: {msg}")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def load(root: Path) -> None:
    """c_pvr_gpu behind its sha, then its own load() (c_pvr.py a503644a, c_pvr_run.py 0c80ee68); rescap chair and
    lexicon behind their c_pvr pins; then the two kit files behind theirs, protocol_pilot first so the kit's own
    `import protocol_pilot` finds the checked module. sys.path is restored after the kit."""
    global G, CP, CR, E4, PA, CODE_ROOT
    CODE_ROOT = root
    if sha((root / GPU[0]).read_bytes()) != GPU[1]:
        fault(f"{GPU[0]} differs from its pin {GPU[1][:8]}")
    sys.path.insert(0, str(root / "scripts/c_pvr_gpu"))
    import c_pvr_gpu as G  # noqa: E402
    G.load(root)
    CP, CR = G.CP, G.CR
    CP.rescap_mods(root)  # the kit imports rescap.chair.norm_tone
    saved = list(sys.path)
    for name, (rel, h) in KIT.items():
        if sha((root / rel).read_bytes()) != h:
            fault(f"{rel} differs from its pin {h[:8]}")
        spec = importlib.util.spec_from_file_location(name, root / rel)
        m = sys.modules[name] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
    sys.path[:] = saved
    E4, PA = sys.modules["protocol_pilot"], sys.modules["punctuation_audit"]


def safe(p) -> Path:
    return CP.refuse(G.guard(p))


def ref_pins() -> dict:
    return {XM: XM_REFS, "ktvic_explore": CR.LISTS_IN["ktvic_test"], "openviic_explore": CR.LISTS_IN["openviic_test"]}


def jdk() -> dict:
    """CC-294 W1: the java that CP.rdr runs (bare `java` from PATH, c_pvr.py l.69) must report JDK; recorded with the
    VnCoreNLP pins, which CP.rdr re-hashes on every call."""
    exe = shutil.which("java") or "java"
    lines = subprocess.run([exe, "-version"], capture_output=True, text=True).stderr.strip().splitlines()
    line = lines[0] if lines else ""
    if f'"{JDK}"' not in line:
        fault(f"java -version reports {line!r}, not {JDK} (pin §3); nothing is written")
    return {"java": exe, "realpath": os.path.realpath(exe), "version": lines, "vnc_dir": str(CP.VNC_DIR),
            "vnc_pins": dict(CP.VNC_PINS)}


# ---------------------------------------------------------------------------------------------- inputs
def manifests(build: Path, tman: str) -> dict:
    """c_pvr_score.manifests form: MANIFEST.sha256 = TMAN, then each manifest/<set>.json against it."""
    man = safe(build / "MANIFEST.sha256").read_bytes()
    if sha(man) != tman:
        fault("MANIFEST.sha256 differs from --tman")
    want = {p: h for h, p in (x.split("  ", 1) for x in man.decode().splitlines())}
    out = {}
    for s in ARMS:
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
        if len(h) != 64 or not rel or rel in out:
            fault(f"{p.name}: malformed or repeated line")
        out[rel] = h
    return out


def captions(out: Path, sums: dict, s: str, a: str, ids: set) -> dict:
    """{id: caption} of one (set, arm): the SUMS line, LF end, whitelisted keys, unique ids, and complete. A partial
    or absent arm writes no CIDEr-VI file (pin §6)."""
    rel = f"out/{s}.{a}.jsonl"
    p = safe(out / rel)
    if rel not in sums or not p.exists():
        fault(f"{rel} absent or not in the SUMS file; no CIDEr-VI file is written")
    b = p.read_bytes()
    if sha(b) != sums[rel]:
        fault(f"{rel} differs from its SUMS line")
    if b and not b.endswith(b"\n"):
        fault(f"{rel}: torn last line")
    d = {}
    for x in b.decode("utf-8").splitlines():
        r = json.loads(x)
        if (set(r) - G.OUT_KEYS or (r.get("set"), r.get("arm")) != (s, a) or r["id"] in d
                or type(r.get("caption")) is not str):
            fault(f"{rel}: a record has other keys, another set / arm, a repeated id or no caption string")
        d[r["id"]] = r["caption"]
    if set(d) != ids:
        fault(f"{rel}: {len(set(d) & ids)} of {len(ids)} manifest ids, {len(set(d) - ids)} others; "
              "no CIDEr-VI file is written")
    return d


def references(s: str, b: bytes, ids: list[str]) -> dict:
    """{manifest id: references} of one set, in sorted id order. Only the manifest ids are kept, so the kit's default
    DF is the references of the scored images (G-7). Field names: c_stage1/score.py references, protocol_pilot main."""
    j = json.loads(b)
    if s == "openviic_explore":
        allr = {k: list(v["captions"]) for k, v in j.items()}
    else:  # KTVIC test_data.json and XM3600 full_data.json: annotations[].image_id / .caption; KTVIC id = str(int)
        allr = {}
        for a in j["annotations"]:
            allr.setdefault(str(a["image_id"]), []).append(a["caption"])
    if miss := [i for i in ids if not allr.get(i)]:
        fault(f"{s}: {len(miss)} manifest ids without a reference")
    return {i: allr[i] for i in sorted(ids)}


# ---------------------------------------------------------------------------------------------- text and score
def tok(texts: list[str]) -> list[str]:
    """Pin §3: CP.clean -> CP.rdr -> one space between words -> str.lower(); one RDR pass over the distinct texts."""
    cl = [CP.clean(t) for t in texts]
    if any(CP.MARK in t for t in cl):
        fault("a text holds the RDR batch marker")
    uniq = sorted(set(cl))
    seg = dict(zip(uniq, (" ".join(w).lower() for w in CP.rdr(uniq))))
    return [seg[t] for t in cl]


def nfc(t: str) -> str:
    return unicodedata.normalize("NFC", t)


def strip(t: str) -> str:
    return " ".join(PA.strip_trailing_punct_tokens(t.split()))


def col(C, h: dict) -> dict:
    return dict(zip(C.ids, map(float, C.per_image(h))))  # per_image runs in C.ids (sorted) order


def cider(refs: dict, hyps: dict) -> tuple[dict, dict]:
    """One kit Cider per source set (G-7: DF over these refs, never pooled); {arm: {id: score}} as written, stripped."""
    C = E4.Cider(refs)
    return ({a: col(C, h) for a, h in hyps.items()},
            {a: col(C, {i: strip(t) for i, t in h.items()}) for a, h in hyps.items()})


def descriptive(S: dict) -> dict:
    """Pin §5: the stripped column, points only; never gating."""
    def m(s, a, b):
        return float(np.mean([S[s][a][i] - S[s][b][i] for i in S[s][b]]))
    out = {s: {f"{v} - A1": m(s, v, "A1") for v in VARIANTS} for s in ARMS}
    out[XM]["A1 - A0"] = m(XM, "A1", "A0")
    n = {s: len(S[s]["A1"]) for s in GUARD}
    out["G1_pooled"] = {f"{v} - A1": sum(out[s][f"{v} - A1"] * n[s] for s in GUARD) / sum(n.values()) for v in VARIANTS}
    return {"label": "stripped column, descriptive, never gating (CIDER_VI_PIN_v1 §5)", **out}


def in_range(d: dict) -> None:
    """Every score in [0, 1000], inclusive (CC-294 N5): 1000 = a caption equal to every reference; NaN fails."""
    if bad := sum(not (0.0 <= v <= 1000.0) for arms in d.values() for c in arms.values() for v in c.values()):
        fault(f"{bad} CIDEr-VI values outside [0, 1000]; nothing is written")


def write_new(p: Path, d: dict) -> str:
    b = (json.dumps(d, sort_keys=True, allow_nan=False) + "\n").encode()
    with open(safe(p), "xb") as f:
        f.write(b)
    return sha(b)


def score(x, data: Path, pins: dict | None = None) -> dict:
    """data: the root the reference paths of `pins` resolve against (the repo for a real run)."""
    pins = pins or ref_pins()
    env = jdk()
    Ms = manifests(x.build, x.tman)
    sums = sums_of(x.out / x.sums)
    ids = {s: [q["id"] for q in Ms[s]["queries"]] for s in ARMS}
    if bad := {s: sum(not CR.half(i) for i in ids[s]) for s in GUARD if not all(map(CR.half, ids[s]))}:
        fault(f"confirm-half ids in a guard manifest (prereg §4.2): {bad}")
    raw = {s: references(s, G.pinned_bytes(data / pins[s][0], pins[s][1]), ids[s]) for s in ARMS}
    caps = {s: {a: captions(x.out, sums, s, a, set(ids[s])) for a in arms} for s, arms in ARMS.items()}
    texts = [t for s in ARMS for rs in raw[s].values() for t in rs] + [
        t for s in ARMS for a in ARMS[s] for t in caps[s][a].values()]
    seg = dict(zip(texts, tok(texts)))
    W, S = {}, {}
    for s, arms in ARMS.items():
        W[s], S[s] = cider({i: [seg[r] for r in rs] for i, rs in raw[s].items()},
                           {a: {i: seg[c] for i, c in caps[s][a].items()} for a in arms})
    in_range(W)
    in_range(S)
    x.res.mkdir(parents=True, exist_ok=True)
    rec = {"label": CP.LABEL, "what": "per-image CIDEr-VI (CIDER_VI_PIN_v1)", "python": sys.version.split()[0],
           "numpy": np.__version__, "jdk": env, "tman": x.tman, "sums_sha256": sha(safe(x.out / x.sums).read_bytes()),
           "code_sha256": {**{r: sha((CODE_ROOT / r).read_bytes()) for r in (GPU[0], *(k[0] for k in KIT.values()))},
                           "scripts/c_pvr/c_pvr_cider_vi.py": sha(Path(__file__).read_bytes())},
           "refs": {s: {"path": p, "sha256": h} for s, (p, h) in pins.items()},
           "n": {s: len(v) for s, v in ids.items()},
           "files": {"as_written (gating; --cider)": {"path": "cider_vi.json",
                                                      "sha256": write_new(x.res / "cider_vi.json", W)},
                     "stripped (descriptive)": {"path": "cider_vi_stripped.json",
                                                "sha256": write_new(x.res / "cider_vi_stripped.json", S)}},
           "counts": {f"{s}.{a}": {"empty_after_clean": sum(not CP.clean(c) for c in caps[s][a].values()),
                                   "changed_by_nfc": sum(nfc(c) != c for c in caps[s][a].values()),
                                   "with_underscore": sum("_" in c for c in caps[s][a].values()),
                                   "trailing_punct_stripped": sum(strip(seg[c]) != seg[c] for c in caps[s][a].values())}
                      for s in ARMS for a in ARMS[s]},
           "refs_with_underscore": {s: sum("_" in r for rs in raw[s].values() for r in rs) for s in ARMS},
           "refs_changed_by_nfc": {s: sum(nfc(r) != r for rs in raw[s].values() for r in rs) for s in ARMS},
           "stripped_descriptive": descriptive(S)}
    write_new(x.res / "cider_vi_record.json", rec)
    return rec


# ---------------------------------------------------------------------------------------------- selftest
def _must(frag: str, fn, *a) -> None:
    try:
        fn(*a)
    except SystemExit as e:
        assert frag in str(e), (frag, str(e))
        return
    raise AssertionError(f"no FAULT: {frag}")


def _pyco(refs: dict, hyps: dict) -> dict:
    """pycocoevalcap 1.2 CiderScorer (the G-6 SD-basis scorer) on tokenized text, ×100, DF over exactly these refs."""
    from pycocoevalcap.cider.cider_scorer import CiderScorer
    sc, ids = CiderScorer(n=4, sigma=6.0), sorted(refs)
    for i in ids:
        sc += (hyps[i], refs[i])
    return dict(zip(ids, (float(v) * 100.0 for v in sc.compute_score()[1])))


def _close(a: dict, b: dict) -> bool:
    return a.keys() == b.keys() and all(np.isclose(a[k], b[k], rtol=1e-12, atol=1e-9) for k in a)


def _st_equal() -> None:
    g = np.random.default_rng(7)
    voc = [f"w{k}" for k in range(9)] + ["con_mèo", ".", ","]
    sent = lambda: " ".join(g.choice(voc, int(g.integers(1, 14))))  # noqa: E731
    refs = {f"i{k:02d}": [sent() for _ in range(int(g.integers(1, 6)))] for k in range(60)} | {"zz": ["q1 q2 q3 q4 q5"]}
    hyps = {i: sent() for i in refs} | {"i00": "", "i01": refs["i01"][0], "zz": "q1 q2 q3 q4 q5"}
    got = col(E4.Cider(refs), hyps)
    assert _close(got, _pyco(refs, hyps)), "kit Cider = pycocoevalcap CiderScorer ×100"
    assert abs(got["zz"] - 1000.0) < 1e-9 and got["i00"] == 0.0, "1000 is attainable (one unique reference, copied)"
    in_range({XM: {"A1": {"a": 0.0, "b": 1000.0}}})
    for bad in (1000.0 + 1e-9, -1e-12, float("nan")):
        _must("outside [0, 1000]", in_range, {XM: {"A1": {"a": bad}}})


def _st_tok() -> None:
    a = "Bảy chiếc ô tím xếp dọc bờ tường ẩm ."
    n = "Anh Trần Minh Khoa ngồi trên ghế ."
    t = tok([a, unicodedata.normalize("NFD", a), " Bảy  chiếc ô tím\nxếp dọc bờ tường ẩm . ", "Hai người đàn ông", n,
             "Đèn Straße xanh ."])
    assert t[0] == t[1] == t[2] == "bảy chiếc ô tím xếp dọc bờ tường ẩm .", "NFC, whitespace, lower case"
    assert t[3] == "hai người đàn_ông", "RDR words kept whole"
    cased, low = (" ".join(w) for w in CP.rdr([n, n.lower()]))
    assert t[4] == cased.lower() != low, "RDR on the cased text, then lower case (lower-first segments differently)"
    assert t[5] == "đèn straße xanh .", "str.lower, not casefold"
    assert strip("một con mèo . !") == "một con mèo" and strip("a . b") == "a . b", "trailing punctuation only"
    _must("batch marker", tok, [f"x {CP.MARK} y"])


VOC = (", một hai con mèo chó người đàn ông phụ nữ đang nằm ngồi đứng trên dưới cạnh ghế bàn cửa sổ quả bóng "
       "màu đỏ xanh chiếc xe đạp cây hoa").split()
NFD_TEXT = unicodedata.normalize("NFD", "Hai quả bóng đỏ .")


def _world(base: Path, g, kt_bad: bool = False, partial: bool = False):
    """A synthetic pulled run: manifests (TMAN), outputs + SUMS, and three reference files with extra images.
    xm3600_vi.PVR-drop holds two captions empty after clean; xm3600_vi.A0 one NFD caption; one XM reference is NFD."""
    sent = lambda: (" ".join(g.choice(VOC, int(g.integers(2, 12)))).capitalize()  # noqa: E731
                    + str(g.choice([" .", ".", "!", "", " . ."])))

    def exp(n: int, want: bool = True) -> list[str]:
        return [i for i in map(str, range(1, 400)) if CR.half(i) == want][:n]
    kt = exp(12)
    ids = {XM: [f"{j:016x}" for j in range(1, 15)], "ktvic_explore": kt,
           "openviic_explore": [k for k in (f"{j:011d}.jpg" for j in range(1, 400)) if CR.half(k)][:9]}
    extra = {XM: ["ffffffffffffff00"], "ktvic_explore": exp(3, False),
             "openviic_explore": [k for k in (f"{j:011d}.png" for j in range(1, 400)) if not CR.half(k)][:3]}
    if kt_bad:
        ids["ktvic_explore"] = kt[:-1] + extra["ktvic_explore"][:1]
    for d in ("manifest", "pull/out", "data"):
        (base / d).mkdir(parents=True)
    man = ""
    for s, v in ids.items():
        q = [{"id": i} for i in reversed(v)]  # manifest order != sorted order
        b = json.dumps({"label": CP.LABEL, "set": s, "queries": q}).encode()
        (base / "manifest" / f"{s}.json").write_bytes(b)
        man += f"{sha(b)}  manifest/{s}.json\n"
    (base / "MANIFEST.sha256").write_text(man)
    allr = {s: {i: [sent() for _ in range(int(g.integers(1, 5)))] for i in ids[s] + extra[s]} for s in ids}
    allr[XM][ids[XM][4]][0] = NFD_TEXT  # j = 4: A1 does not copy it (A1 copies at j % 3 == 0)
    files = {XM: {"images": [], "annotations": [{"image_id": i, "caption": c}
                                                for i, rs in allr[XM].items() for c in rs]},
             "ktvic_explore": {"annotations": [{"image_id": int(i), "caption": c, "segment_caption": "x"}
                                               for i, rs in allr["ktvic_explore"].items() for c in rs]},
             "openviic_explore": {k: {"captions": rs} for k, rs in allr["openviic_explore"].items()}}
    pins = {}
    for s, j in files.items():
        p = base / "data" / f"{s}_refs.json"
        p.write_text(json.dumps(j, ensure_ascii=False), encoding="utf-8")
        pins[s] = (p.relative_to(base).as_posix(), sha(p.read_bytes()))
    special = {(XM, "PVR-drop"): {ids[XM][0]: "", ids[XM][1]: " \n "}, (XM, "A0"): {ids[XM][2]: NFD_TEXT}}
    sums, caps = "", {}
    for s, arms in ARMS.items():
        for a in arms:
            caps[(s, a)] = {i: allr[s][i][0] if a == "A1" and j % 3 == 0 else sent() for j, i in enumerate(ids[s])}
            caps[(s, a)].update(special.get((s, a), {}))
            keep = ids[s][:-1] if partial and (s, a) == ("ktvic_explore", "PVR-keep") else ids[s]
            rows = "".join(json.dumps({"utc": "t", "set": s, "arm": a, "id": i, "caption": caps[(s, a)][i]},
                                      ensure_ascii=False) + "\n" for i in reversed(keep))
            (base / "pull/out" / f"{s}.{a}.jsonl").write_text(rows, encoding="utf-8")
            sums += f"{sha(rows.encode())}  out/{s}.{a}.jsonl\n"
    (base / "pull" / "SHA256SUMS_tier1").write_text(sums)  # c_pvr_out layout: SUMS beside out/
    x = argparse.Namespace(out=base / "pull", sums="SHA256SUMS_tier1", build=base, tman=sha(man.encode()),
                           res=base / "res")
    return x, pins, {s: {i: allr[s][i] for i in ids[s]} for s in ids}, caps


def _st_world(tmp: Path) -> None:
    x, pins, refs, caps = _world(tmp / "w1", np.random.default_rng(3))
    rec = score(x, tmp / "w1", pins)
    W = json.loads((x.res / "cider_vi.json").read_bytes())
    S = json.loads((x.res / "cider_vi_stripped.json").read_bytes())
    need = {(XM, "A0")} | {(s, a) for s in (XM, *GUARD) for a in ("A1", *VARIANTS)}  # c_pvr_score 1e15ce7a cider_in
    assert {(s, a) for s in W for a in W[s]} == need == {(s, a) for s in S for a in S[s]}, "the cider_in arms, no more"
    assert sha((x.res / "cider_vi.json").read_bytes()) == rec["files"]["as_written (gating; --cider)"]["sha256"]
    j = rec["jdk"]
    assert f'"{JDK}"' in j["version"][0] and j["vnc_pins"] == CP.VNC_PINS and j["java"] == shutil.which("java")
    allt = [r for v in refs.values() for rs in v.values() for r in rs] + [c for v in caps.values() for c in v.values()]
    T = dict(zip(allt, tok(allt)))
    for s in ARMS:
        rt = {i: [T[r] for r in rs] for i, rs in refs[s].items()}
        for a in ARMS[s]:
            ht = {i: T[c] for i, c in caps[(s, a)].items()}
            assert set(W[s][a]) == set(refs[s]), "exactly the manifest ids"
            assert _close(W[s][a], _pyco(rt, ht)), f"{s}.{a} as written = pycocoevalcap, DF over the scored refs"
            assert _close(S[s][a], _pyco(rt, {i: strip(t) for i, t in ht.items()})), f"{s}.{a} stripped: captions only"
    assert any(W[s][a] != S[s][a] for s in ARMS for a in ARMS[s]), "the stripped column differs somewhere"
    assert any(v > 0 for v in W[XM]["A1"].values()), "A1 copies some references"
    e = [i for i, c in caps[(XM, "PVR-drop")].items() if not CP.clean(c)]
    assert len(e) == 2 and all(W[XM]["PVR-drop"][i] == S[XM]["PVR-drop"][i] == 0.0 for i in e), "empty kept, scores 0"
    cnt = {k: (v["empty_after_clean"], v["changed_by_nfc"]) for k, v in rec["counts"].items()}
    assert cnt == {f"{s}.{a}": (2 * (f"{s}.{a}" == f"{XM}.PVR-drop"), int(f"{s}.{a}" == f"{XM}.A0"))
                   for s in ARMS for a in ARMS[s]}, "empty and NFC counts"
    assert rec["refs_changed_by_nfc"] == {s: int(s == XM) for s in ARMS}, "NFC count on references"
    d = rec["stripped_descriptive"]
    for s in ARMS:  # expected values from S itself, not from d
        for v in VARIANTS:
            assert np.isclose(d[s][f"{v} - A1"], np.mean([S[s][v][i] - S[s]["A1"][i] for i in S[s]["A1"]]))
    assert np.isclose(d[XM]["A1 - A0"], np.mean([S[XM]["A1"][i] - S[XM]["A0"][i] for i in S[XM]["A0"]]))
    for v in VARIANTS:
        num = sum(S[s][v][i] - S[s]["A1"][i] for s in GUARD for i in S[s]["A1"])
        assert np.isclose(d["G1_pooled"][f"{v} - A1"], num / sum(len(S[s]["A1"]) for s in GUARD)), "G1 image-weighted"
    try:
        score(x, tmp / "w1", pins)
        raise AssertionError("an existing output file was overwritten")
    except FileExistsError:
        pass


def _resum(x, rel: str, b: bytes, fix: bool = True) -> None:
    """Rewrite a pulled file; fix = also rewrite its SUMS line."""
    (x.out / rel).write_bytes(b)
    if fix:
        L = (x.out / x.sums).read_text().splitlines()
        (x.out / x.sums).write_text("".join((f"{sha(b)}  {rel}" if r.endswith(f"  {rel}") else r) + "\n" for r in L))


def _reman(x, s: str, M: dict):
    """Rewrite manifest/<s>.json and MANIFEST.sha256; returns x with the new TMAN."""
    (x.build / "manifest" / f"{s}.json").write_bytes(json.dumps(M).encode())
    man = "".join(f"{sha((x.build / 'manifest' / f'{t}.json').read_bytes())}  manifest/{t}.json\n" for t in ARMS)
    (x.build / "MANIFEST.sha256").write_text(man)
    return argparse.Namespace(**{**vars(x), "tman": sha(man.encode())})


def _custody(x, case: str):
    """One CC-294 N1 corruption of a fresh world; returns the namespace to score."""
    rel = f"out/{XM}.A1.jsonl"
    b = (x.out / rel).read_bytes()
    rows = [json.loads(r) for r in b.decode().splitlines()]
    dump = lambda rs: "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rs).encode()  # noqa: E731
    if case == "sums_mismatch":
        _resum(x, rel, dump([{**rows[0], "caption": rows[0]["caption"] + " x"}] + rows[1:]), fix=False)
    elif case == "torn":
        _resum(x, rel, b[:-1])
    elif case == "manifest_sha":
        p = x.build / "manifest" / "ktvic_explore.json"
        p.write_bytes(p.read_bytes() + b" ")
    elif case == "label_set":
        return _reman(x, XM, {**json.loads((x.build / "manifest" / f"{XM}.json").read_bytes()), "label": "other"})
    elif case == "extra_key":
        _resum(x, rel, dump([{**rows[0], "extra": 1}] + rows[1:]))
    elif case == "set_arm":
        _resum(x, rel, dump([{**rows[0], "arm": "A2"}] + rows[1:]))
    elif case == "dup_id":
        _resum(x, rel, dump(rows[:1] + rows))
    elif case == "sums_repeat":
        p = x.out / x.sums
        p.write_text(p.read_text() + p.read_text().splitlines()[0] + "\n")
    return x


CUSTODY = {"sums_mismatch": "differs from its SUMS line", "torn": "torn last line",
           "manifest_sha": "differs from MANIFEST.sha256", "label_set": "label/set mismatch",
           "extra_key": "a record has other keys", "set_arm": "a record has other keys",
           "dup_id": "a record has other keys", "sums_repeat": "malformed or repeated line"}


def _st_faults(tmp: Path) -> None:
    x, pins, _, _ = _world(tmp / "f1", np.random.default_rng(4), kt_bad=True)
    _must("confirm-half ids", score, x, tmp / "f1", pins)
    x, pins, _, _ = _world(tmp / "f2", np.random.default_rng(4), partial=True)
    _must("no CIDEr-VI file is written", score, x, tmp / "f2", pins)
    x, pins, _, _ = _world(tmp / "f3", np.random.default_rng(4))
    _must("differs from its pin", score, x, tmp / "f3", {**pins, XM: (pins[XM][0], "0" * 64)})
    _must("differs from --tman", score, argparse.Namespace(**{**vars(x), "tman": "0" * 64}), tmp / "f3", pins)
    j = json.loads((tmp / "f3" / pins[XM][0]).read_bytes())
    j["annotations"] = [a for a in j["annotations"] if a["image_id"] != f"{1:016x}"]
    (tmp / "f3" / "data" / "cut.json").write_text(json.dumps(j))
    cut = ("data/cut.json", sha((tmp / "f3" / "data" / "cut.json").read_bytes()))
    _must("without a reference", score, x, tmp / "f3", {**pins, XM: cut})
    shim = tmp / "jdk_shim"  # a stand-in java first on PATH (CC-294 W1)
    shim.mkdir()
    (shim / "java").write_text("#!/bin/sh\necho 'openjdk version \"21.0.13\" 2026-10-20' >&2\n")
    (shim / "java").chmod(0o755)
    path = os.environ["PATH"]
    os.environ["PATH"] = f"{shim}{os.pathsep}{path}"
    try:
        _must("not 21.0.12.1", score, x, tmp / "f3", pins)
    finally:
        os.environ["PATH"] = path
    assert not (x.res / "cider_vi.json").exists(), "a FAULT writes nothing"
    for k, (case, frag) in enumerate(CUSTODY.items()):
        xc, pc, _, _ = _world(tmp / f"c{k}", np.random.default_rng(5))
        _must(frag, score, _custody(xc, case), tmp / f"c{k}", pc)


def selftest(root: Path) -> int:
    load(root)
    _st_equal()
    _st_tok()
    with tempfile.TemporaryDirectory() as t:
        _st_world(Path(t))
        _st_faults(Path(t))
    print(f"selftest ok (kit = pycocoevalcap; text route; 3-set world; {6 + len(CUSTODY)} FAULT cases; range)")
    return 0


def mutants(root: Path) -> int:
    """Each mutant edits one spot of the code above the MUTANTS table; the mutated file's selftest must fail."""
    src = Path(__file__).read_text(encoding="utf-8")
    body, sep, tail = src.partition("\nMUTANTS = (")
    alive = []
    with tempfile.TemporaryDirectory() as t:
        for name, old, new in MUTANTS:
            assert body.count(old) == 1, f"{name}: the target is not unique"
            p = Path(t) / "c_pvr_cider_vi.py"
            p.write_text(body.replace(old, new) + sep + tail, encoding="utf-8")
            r = subprocess.run([sys.executable, "-I", "-B", str(p), "selftest", "--root", str(root)],
                               capture_output=True, text=True)
            if r.returncode == 0:
                alive.append(name)
    print(f"mutants {len(MUTANTS)}: killed {len(MUTANTS) - len(alive)}, survived {alive}")
    return 1 if alive else 0


MUTANTS = (
    ("df_extra_doc", "C = E4.Cider(refs)", "C = E4.Cider(refs, df_refs=[*refs.values(), ['x']])"),
    ("sigma_inf", "C = E4.Cider(refs)", "C = E4.Cider(refs, sigma=float('inf'))"),
    ("scale_x10", "map(float, C.per_image(h))", "(float(v) / 10 for v in C.per_image(h))"),
    ("manifest_order", "zip(C.ids, map", "zip(list(h), map"),
    ("no_lower", '(" ".join(w).lower() for w', '(" ".join(w) for w'),
    ("no_nfc", "cl = [CP.clean(t) for t in texts]", 'cl = [" ".join(t.split()) for t in texts]'),
    ("strip_refs", "C = E4.Cider(refs)", "C = E4.Cider({i: [strip(r) for r in rs] for i, rs in refs.items()})"),
    ("strip_as_written", "({a: col(C, h) for a, h", "({a: col(C, {i: strip(t) for i, t in h.items()}) for a, h"),
    ("no_A0", 'ARMS = {XM: ("A0", "A1", *VARIANTS)', 'ARMS = {XM: ("A1", *VARIANTS)'),
    ("no_half_check", "if not all(map(CR.half, ids[s]))}", "if False}"),
    ("partial_ok", "if set(d) != ids:", "if not set(d) <= ids:"),
    ("refs_unfiltered", "return {i: allr[i] for i in sorted(ids)}", "return {i: allr[i] for i in sorted(allr)}"),
    ("strip_all_punct", "PA.strip_trailing_punct_tokens(t.split())",
     "[w for w in t.split() if not PA.is_punct_tok(w)]"),
    ("no_jdk_check", "if f'\"{JDK}\"' not in line:", "if False:"),  # CC-294 W1
    ("jdk_skipped", "    env = jdk()\n", "    env = {}\n"),
    ("range_exclusive", "0.0 <= v <= 1000.0", "0.0 < v < 1000.0"),  # CC-294 N5
    ("no_sums_check", "if sha(b) != sums[rel]:", "if False:"),  # CC-294 N1, the judge's hand forms
    ("no_torn", 'if b and not b.endswith(b"\\n"):', "if False:"),
    ("no_manifest_sha", 'if want.get(f"manifest/{s}.json") != sha(b):', "if False:"),
    ("no_label_check", "!= (CP.LABEL, s):", '!= (out[s].get("label"), s):'),
    ("no_keys_check", "set(r) - G.OUT_KEYS or ", ""),
    ("no_setarm_check", '(r.get("set"), r.get("arm")) != (s, a) or ', ""),
    ("dup_ids_ok", ' or r["id"] in d', ""),
    ("sums_repeat_ok", " or rel in out:", ":"),
    ("empty_dropped", 'd[r["id"]] = r["caption"]', 'd[r["id"]] = r["caption"] or "x"'),  # CC-294 N2
    ("strip_desc_as_written", 'out = {s: {f"{v} - A1": m(s, v, "A1")', 'out = {s: {f"{v} - A1": 0.0 * m(s, v, "A1")'),
    ("lower_first", "for w in CP.rdr(uniq))))", "for w in CP.rdr([u.lower() for u in uniq]))))"),  # CC-294 N6
    ("casefold", '" ".join(w).lower() for w', '" ".join(w).casefold() for w'),
)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sp = ap.add_subparsers(dest="cmd", required=True)
    for c in ("selftest", "mutants"):
        sp.add_parser(c).add_argument("--root", type=Path, default=ROOT)
    s = sp.add_parser("score")
    for k in ("out", "build", "res"):
        s.add_argument(f"--{k}", type=Path, required=True)
    s.add_argument("--sums", required=True, help="SHA256SUMS_tier1 (S11 §13)")
    s.add_argument("--tman", required=True)
    a = ap.parse_args()
    if a.cmd == "selftest":
        return selftest(a.root)
    if a.cmd == "mutants":
        return mutants(a.root)
    load(ROOT)
    print(json.dumps(score(a, ROOT), indent=1, sort_keys=True, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
