#!/usr/bin/env python3
"""B-FECERT (Paper B, LRE): the front-end certificate, the held-out front-end check, the first scoring of other groups'
released outputs, front-end identification (FE-ID) and the human preference arm. Registration
manuscript/prereg/2026-11-12_b_fecert/B_FECERT_PREREG_v1_1.md (sha256 736b7e6a...; CC-350, CC-353); labelling plan
B_PREF_LABELLING_PLAN_v1_1.md (59ae449b...). The family is scripts/b_fecert/family.py.

One stage per call, in the registered order (§9): F, C, G, 1, pin, 2a, 2b, 3, H. Every stage after F needs --prev = the
sha256 of the previous stage's file, and that file's LOG pin line in --log (b_pa1.pin_line form); 2a also needs the pin
line of DEV.json + NC.json and the GATE2.json line and refuses if any RESULT*.json exists; 2b needs the V.json line.

  python -I -B scripts/b_fecert/b_fecert.py selftest                         synthetic fixtures in a temp dir only
  NCS_DATA=D python -I -B scripts/b_fecert/b_fecert.py F  --work W --pyvi-wheel P --uts-wheel U
  ... C  --work W --log L --prev <FAMILY.json> --baselines B --b2-score S
  ... G  --work W --log L --prev <CENSUS.json> --fl FL --baselines B
  ... 1  --work W --log L --prev <GATE2.json> --baselines B
  ... pin --work W --prev <DEV.json> --nc <NC.json> --pins P
  ... 2a --work W --log L --prev <DEV.json> --fl FL --baselines B
  ... 2b --work W --log L --prev <V.json> --fl FL --baselines B
  ... 3  --work W --log L --prev <RESULT.json> --fl FL --baselines B (--printed PRINTED.json | --k-print)
  ... H  --work W --log L --prev <FEID.json> --labels DIR

Outputs and stdout hold names, counts, labels, scores and sha256 only; no caption or reference text is written or
printed. CPU only, on the host named at the code read (PI-1111j; CC-353 4(e)).
"""
from __future__ import annotations

import argparse
import contextlib
import functools
import hashlib
import importlib.metadata
import inspect
import io
import json
import os
import platform
import random
import re
import shutil
import subprocess
import sys
import time
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import beta, binomtest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(HERE), str(ROOT / "scripts/kit_b"), str(ROOT / "scripts/b2_external"), str(ROOT / "scripts/b_pa1"),
                str(ROOT / "tools/obj_rater")]
import family as FM  # noqa: E402
from build_pairs import tok_diff  # noqa: E402  plan §2.1 token difference: one helper for both tools (CC-361 NB6)
import protocol_pilot as E4  # noqa: E402  rdr, Cider, bleu4, rouge_l, ngrams (§12: reused unchanged)
import ptb_protocol as PT  # noqa: E402  load_refs, load_preds (§12: reused unchanged)
import b2  # noqa: E402  parse, norm_id, sha_file, git_blob (B-2 parser and hashes)
import b2_controls as BC  # noqa: E402  THESIS: git blob pins of the two KTVIC baseline files (CC-092)
from b_pa1 import pin_line  # noqa: E402  §12: the pin-line pattern of scripts/b_pa1/b_pa1.py

REG = "manuscript/prereg/2026-11-12_b_fecert/B_FECERT_PREREG_v1_1.md"
REG_SHA = "736b7e6a8ea2007270a3329db7ad6a09197c4804c9bc3821ea6bd4ceb5a61aa0"
LOG = ROOT / ".session_backup/2026-10-13/decisions/LOG.md"

# ------------------------------------------------------------------------------------------------ registered values
SEED, B = 20261112, 10_000  # §3.1
SEED_PLANT = 20261113  # §5.3
Z_NEAR, N_MIN = 4.0, 59  # §6.1
CP_ALPHA, R_MAX = 0.05, 0.05  # §6.1: one-sided 95% Clopper-Pearson against 0.05
NFL_MIN, KFL_MIN, KFL_SHARE = 10, 3, 0.10  # §6.2
FL20 = 20  # §10 K-FL20
PLANT_MIN = 12  # §6.4, §10 K-plant
GREPRO_TOL = 0.01  # §9 stage F, B_KAPPA §5.1
GATE = {"coverage": 0.95, "unknown": 0.05, "dup": 0.01, "empty": 0.01, "refcopy": 0.05, "diacritic": 0.50,
        "overlap": 0.95}  # §4.3
EPS = 10.0  # plan §2.2
H_P_MIN, H_U_MIN, H_P_POWER = 40, 100, 47  # plan §7, §5.2
KAPPA_LABEL, KAPPA_MIN = 0.40, 0.20  # plan §5.4
H_SEED, H_BOOT = 20261112, 2000  # plan §5.4
K_PRINT, K_TIME = "2026-11-15T05:00:00Z", "2026-11-16T05:00:00Z"  # §10: 12:00 VN
PYVI_VERSION, JAR_SHA, PILOT_SHA = "0.1.1", "9e2811cd", "6aee4282"  # §2.2
# §2.2 l.114 "the release installed on the host before the code read": underthesea 9.5.0 from its wheel (round-2 host
# record host_checks_r2/; CC-361 D6). A different release, no wheel record or no signature is a FAULT.
UTS_VERSION, UTS_WHEEL_SHA = "9.5.0", "81400f41b75ceff6f80c52b4ad043806c80f5899ec555d8e6374d468a59bce56"
# r* environment (§6.3, K-coco; CC-361 D7): pycocoevalcap 1.2 through rescap/metrics.py at this sha, Java at this version
COCO_VERSION, RESCAP_SHA = "1.2", "e0296ec528b87f4d1b31165cbb45deee5453783fd7dad783f248869e596bf960"
JAVA_VERSION = "21.0.13.0.3"  # `java -version` on the host of the round-2 records
P3_SCOPE = ("BLEU-1", "BLEU-2", "BLEU-3", "BLEU-4", "METEOR", "ROUGE-L", "CIDEr-D")  # §6.3
# §5.1 "every printed metric m", as ruled by CC-361 1(e)/D12: a non-r* member is held to these four (BLEU-1 from the
# per-image counts); METEOR has no member-specific scorer, so it is excluded for non-r* members (forced; disclosed).
# r* is held to every printed metric. The planted check stays on the three metrics of §5.3.
ID_METRICS = ("BLEU-1", "BLEU-4", "ROUGE-L", "CIDEr-D")
PLANT_METRICS = ("CIDEr-D", "BLEU-4", "ROUGE-L")  # §5.3: what PLANT_PRINTED holds (one decimal)
# §5.2 PRINTED.json, read in its pinned layout (CC-361 D1): PIN-1112-b-fecert-printed (CC-354).
PRINTED_SHA = "2a962a2ba09403cd2444c28b428b9809072b6a9155b152d58706f9e860040c47"
PRINTED_SYSTEMS = {  # (source, system as printed) -> file name here; None = no released output here (§4.1, §5.5)
    ("KTVIC", "1) ResNet101 / LSTM"): "ktvic_resnetlstm", ("KTVIC", "2) ViT / Transformer"): "ktvic_vittrans",
    ("KTVIC", "3) GRIT / GRIT"): None, ("K2", "b16-small"): None, ("K2", "l14-large"): None, ("K2", "h14-large"): None}
# §6.3 scope names: the printed "CIDEr" is the in-scope CIDEr-D, "ROUGE" and "ROUGE-L" are ROUGE-L
PRINTED_METRICS = {"BLEU-1": "BLEU-1", "BLEU-4": "BLEU-4", "METEOR": "METEOR", "ROUGE": "ROUGE-L", "ROUGE-L": "ROUGE-L",
                   "CIDEr": "CIDEr-D"}
EXPECT = {"systems": 73, "families": 26, "scored": 67}  # B_KAPPA §4.1, §4.3, §5.1
S_FILES = [f"{s}-short" for s in (  # B_KAPPA §4.2, the E4 seen set S, in the registered order
    "p1assist_s42 p1assist_s43 p1assist_s44 p1-gold p1_s43 p1_s44 p1mask_s42 mr5assist_s42 fuse2_s42 fuse2_s43 "
    "fuse2_s44 tags_fuse2_s42 tags_p1_s43 e5_s42 e5dpo_s42 p1_s43mbr fuse2_s42mbr zeroshot tags_zeroshot vcd main_s42 "
    "vsps official p2-noverif4090").split()]
BASE = {"ktvic_resnetlstm": "result_resnetlstm.json", "ktvic_vittrans": "result_vittrans.json"}  # §4.1
BASE_BLOBS = {k: v[1] for k, v in BC.THESIS["files"].items()}
FN_RE = re.compile(r"([0-9]{11})\.(jpg|jpeg|png)")  # plan §9 pair_server item 2 (CC-350 W6)
F0N = FM.name(FM.F0)

# §4.2 groups. Paths are relative to --fl (host layout in READ_PACKAGE.md); "KTVIC" and "UIT" name this project's files.
LOC, VAN = "loc110504/VietnameseSportImageCaptioning", "vanngthi/ViECAP-Image-Captioning-Vietnamese/annotations"
GEN = f"{LOC}/notebooks/4_models/generated_captions"
GROUPS = {
    "G1": {"repo": "loc110504", "refs": f"{LOC}/data/uit_test/captions.txt",
           "files": {f"X4{x}": f"fetched/X4{x}/uit_generated_captions.txt" for x in "abcde"}},
    "G2": {"repo": "loc110504", "refs": f"{LOC}/data/capydata_ic/test/captions.txt",
           "files": {f"G2_{s}": f"{GEN}/{s}/us_generated_captions.txt"
                     for s in ("cnn_lstm", "cnn_lstm_attention", "cnn_t5", "qwen2", "vit_t5")}},
    "G3": {"repo": "vanngthi", "refs": f"{VAN}/uit_viic_original_gt.json",
           "files": {"X3_original": "fetched/X3/uit_viic_original_pred.json",
                     "X3_detect": "fetched/X3/uit_viic_detect_pred.json"}},
    "G4": {"repo": "vanngthi", "refs": f"{VAN}/flickr_original_gt.json",
           "files": {"X3_flickr_original": f"{VAN}/flickr_original_pred.json",
                     "X3_flickr_detect": f"{VAN}/flickr_detect_pred.json"}},
    "G5": {"repo": "trannam710", "refs": "UIT",
           "files": {"X1": "fetched/X1/caption_results.json", "X2": "fetched/X2/caption_results.json"}},
    "G6": {"repo": "SuperCoolGuy855", "refs": "KTVIC", "files": {"K2": "fetched/K2/results.xlsx"}, "with_baselines": 1},
}
# Provenance of every FL file (CC-361 D9), by its path under --fl: fetched/ files by the git blob pinned in b2.A_SYSTEMS
# (the B-2 fetch), the other output files by ~/b_fecert_fetch/MANIFEST.tsv (ff1afb4e), the reference files by CC-354 3(d).
FETCH_BLOBS = {f"fetched/{s['sid']}/{Path(r).name}": b for s in b2.A_SYSTEMS for r, b in s["files"].items()}
MANIFEST_SHA = {
    f"{GEN}/cnn_lstm/us_generated_captions.txt": "2620f0f0d61c0af8b33058be5bd96e2327e150200bc54b27258c26a0a83620f7",
    f"{GEN}/cnn_lstm_attention/us_generated_captions.txt": "e41a994df7c0f53c44ab2df2a3b3e3481acc35e274626edf35d61e1895ed7e27",
    f"{GEN}/cnn_t5/us_generated_captions.txt": "fd5673b996785515fdb558dd7925e4d8da969a3674e22c064554d33ff8324bc1",
    f"{GEN}/qwen2/us_generated_captions.txt": "b335fd52b4a5840d04f24ca99b77db9d288f301d63075f464c63f5ff24425d36",
    f"{GEN}/vit_t5/us_generated_captions.txt": "e0c36022118fa75a87c40bf66e1dfda432f22804b480cf3f1533f6128ec1baad",
    f"{VAN}/flickr_original_pred.json": "51d58b2deb5ec33dc2149fe548792dbf722b189c26118a926c079dfc8b8a481f",
    f"{VAN}/flickr_detect_pred.json": "f1b8a4b67ad36f23eee3342202c8134782106207bdd0105b3e7996c1fde04e2e"}
REF_SHA = {"G1": "609af61acf511689c353dc66dd8bc2eee182cd0ea38315a74844e155f20536a2",
           "G2": "ac9cab7dedc78f13294cc35a594cebc75a6de8cc17fdb43b77003b157454f33e",
           "G3": "2acef66e45218cc200e0a950e488959bdeb8e3a8e44722e45370ef6dcdf9745a",
           "G4": "f02cf2b91d6305d1d70c18ba5d5038af69fe178c0b89a67c3af1a9b950cf3502"}


class Fault(Exception):
    """A FAULT stops the chain; a re-run after a fix needs a judge line (§9)."""


def set_data(root) -> None:
    global DATA, REFS, RES, SIDE, UIT
    DATA = Path(root)
    REFS, RES, UIT = DATA / "datasets/ktvic/test_data.json", DATA / "results", DATA / "datasets/uitviic/test_data.json"
    SIDE = RES / "tone_norm/ktvic_side_by_side.json"


set_data(E4.DATA)  # $NCS_DATA, the layout of protocol_pilot.py


def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


sha = b2.sha_file


def jload(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def write_once(path: Path, obj) -> str:
    if path.exists():
        raise SystemExit(f"REFUSED: {path.name} exists; a stage runs once")
    text = obj if isinstance(obj, str) else json.dumps(obj, indent=1, ensure_ascii=False, default=float) + "\n"
    path.write_text(text, encoding="utf-8")
    return sha(path)


def prev_ok(work: Path, fname: str, prev: str | None, log: Path | None, *also) -> None:
    """§9: a stage starts only with the sha256 of the previous stage's file and that file's LOG line."""
    p = work / fname
    if not prev or not p.is_file() or sha(p) != prev:
        raise SystemExit(f"REFUSED: {fname} is not the file whose sha256 was passed (--prev); registered order (§9)")
    if log is not None and not pin_line(log, prev, fname, *also):
        raise SystemExit(f"REFUSED: no LOG pin line for {fname} {prev[:8]}; registered order (§9)")


def logged(log: Path, path: Path) -> None:
    if not path.is_file() or not pin_line(log, sha(path), path.name):
        raise SystemExit(f"REFUSED: {path.name} has no LOG pin line with its sha256 (§9)")


def inputs(work: Path, log: Path, names) -> dict:
    """§9 l.333 (CC-361 D8): every work file a stage reads carries a LOG pin line with its current sha256, and
    test_data.json still has the sha256 recorded in FAMILY.json. Returns {name: sha256} for the stage record."""
    for n in names:
        logged(log, work / n)
    if sha(REFS) != jload(work / "FAMILY.json")["refs_sha256"]:
        raise Fault("test_data.json differs from its sha256 in FAMILY.json (§9)")
    return {n: sha(work / n) for n in names}


# ------------------------------------------------------------------------------------------------ systems and files
def names() -> list[str]:
    return sorted(jload(SIDE)["systems"])


def stratum(n: str) -> str:
    return n.rsplit("-", 1)[1]


def family(n: str) -> str:
    """B_KAPPA §4.3: drop the mode suffix, a trailing mbr or selffuse, _s42/_s43/_s44; p1-gold -> p1, seed4x -> seed."""
    s = re.sub(r"_s4[234]$", "", re.sub(r"_?(mbr|selffuse)$", "", n.rsplit("-", 1)[0]))
    return {"p1-gold": "p1", "seed43": "seed", "seed44": "seed"}.get(s, s)


def load_base(d: Path, n: str) -> dict[str, str]:
    return {str(r["image_id"]): r["caption"] for r in jload(d / BASE[n])}  # b2_controls.py l.350-351 form


def systems(work: Path) -> list[dict]:
    """SYSTEMS.tsv, bound by the sha256 that CENSUS.json records (CENSUS.json itself is logged; CC-361 D8)."""
    if sha(work / "SYSTEMS.tsv") != jload(work / "CENSUS.json")["systems_tsv_sha256"]:
        raise Fault("SYSTEMS.tsv differs from its sha256 in CENSUS.json (§9)")
    rows = [ln.split("\t") for ln in (work / "SYSTEMS.tsv").read_text(encoding="utf-8").splitlines()[1:]]
    return [dict(zip(("name", "stratum", "family", "sha256", "git_blob", "role"), r)) for r in rows]


def ktvic_texts(work: Path, base: Path, which=None) -> dict[str, dict[str, str]]:
    """Own and baseline outputs by name, each sha256-checked against SYSTEMS.tsv (§9: inputs by sha)."""
    out = {}
    for s in systems(work):
        if which is not None and s["name"] not in which:
            continue
        p = base / BASE[s["name"]] if s["role"] == "baseline" else RES / f"{s['name']}.preds.json"
        if sha(p) != s["sha256"]:
            raise Fault(f"{s['name']}: sha256 differs from SYSTEMS.tsv")
        out[s["name"]] = load_base(base, s["name"]) if s["role"] == "baseline" else PT.load_preds(p)
    return out


def image_files() -> dict[str, str]:
    """Image file per KTVIC test id from test_data.json :: images (plan §2.1, CC-350 W6): never '<id>.jpg'."""
    out = {}
    for im in jload(REFS)["images"]:
        fn = im.get("filename")  # the one key both tools read (build_pairs.load_inputs; CC-361 D3)
        if not isinstance(fn, str) or not FN_RE.fullmatch(fn):
            raise Fault("a KTVIC test image file name is outside the route regex")
        out[str(im["id"])] = fn
    return out


def nid(x) -> str:
    return b2.norm_id(str(x).split("#")[0])


def provenance(rel: str, p: Path) -> None:
    """CC-361 D9: an FL output file must equal its fetch record (git blob for fetched/, else MANIFEST.tsv sha256)."""
    ok = b2.git_blob(p.read_bytes()) == FETCH_BLOBS[rel] if rel in FETCH_BLOBS else sha(p) == MANIFEST_SHA.get(rel)
    if not ok:
        raise Fault(f"{rel}: differs from its fetch record (CC-361 D9)")


def group_refs(g: str, fl: Path) -> tuple[dict[str, list[str]], str | None]:
    """The group's reference file by normalised id, and its sha256; ({}, None) when it is not on the host (then no
    file of the group is admitted). G1-G4 must equal the reference file frozen by CC-354 3(d), else FAULT (CC-361 D9).
    An id with more reference rows than the others (one uit_test id has 10, CC-354 N4) keeps all its rows, in file
    order; no row is dropped or merged."""
    src = GROUPS[g]["refs"]
    p = {"KTVIC": REFS, "UIT": UIT}.get(src, fl / src)
    if not p.is_file():
        return {}, None
    if g in REF_SHA and sha(p) != REF_SHA[g]:
        raise Fault(f"{g}: the reference file differs from CC-354 3(d) (CC-361 D9)")
    if src in ("KTVIC", "UIT"):
        return {nid(k): v for k, v in PT.load_refs(p).items()}, sha(p)
    out: dict[str, list[str]] = {}
    for i, c in b2.parse(p):
        if c.strip():
            out.setdefault(nid(i), []).append(c.strip())
    return out, sha(p)


# ------------------------------------------------------------------------------------------------ §4.3 gate v2
def viet(c: str) -> bool:
    """A letter with a Vietnamese diacritic: a tone mark or vowel modifier in its NFD, or đ / Đ."""
    return any(ch in "đĐ" or any(m in FM.TONES or m in FM.MODS for m in unicodedata.normalize("NFD", ch)[1:])
               for ch in c)


def gate2(rows, refs: dict[str, list[str]]) -> tuple[dict, dict[str, str]]:
    """Rules 1-6 of §4.3 on parsed rows [(id, caption)] or None (rule 1 failed). Counts only."""
    if rows is None:
        return {"admitted": False, "reasons": ["1 parse"]}, {}
    n = len(rows)
    ids = [nid(i) for i, _ in rows]
    preds: dict[str, str] = {}
    for i, c in zip(ids, (c for _, c in rows)):
        if i in refs and i not in preds:  # unknown ids dropped; first occurrence kept
            preds[i] = c
    own = {i: {FM.n_step(r).casefold() for r in refs[i]} for i in preds}
    v = {"rows": n, "coverage": len(preds) / max(1, len(refs)),
         "unknown": sum(i not in refs for i in ids) / max(1, n),
         "dup": (n - len(set(ids))) / max(1, n),
         "empty": sum(not c.strip() for _, c in rows) / max(1, n),
         "refcopy": sum(FM.n_step(c).casefold() in own[i] for i, c in preds.items()) / max(1, len(preds)),
         "diacritic": sum(viet(c) for c in preds.values()) / max(1, len(preds))}
    bad = [k for k, ok in (("2 coverage", v["coverage"] >= GATE["coverage"]), ("2 unknown", v["unknown"] <= GATE["unknown"]),
                           ("3 dup", v["dup"] <= GATE["dup"]), ("4 empty", v["empty"] <= GATE["empty"]),
                           ("5 refcopy", v["refcopy"] <= GATE["refcopy"]), ("6 diacritic", v["diacritic"] >= GATE["diacritic"]))
           if not ok]
    v.update(admitted=not bad, reasons=bad)
    return v, (preds if not bad else {})


def parse_or_none(p: Path):
    try:
        return b2.parse(p)
    except Exception:  # rule 1 (§4.3): no repair, never aligned by position
        return None


def fl_inputs(fl: Path, base: Path) -> dict:
    """Every FL file of §4.2 through the gate: {group: {"refs", "refs_sha256", "files": {name: (rec, preds, path)}}}.
    Each output file is provenance-checked and parsed first; the group's references are loaded only when an output
    parsed (so the UIT-ViIC test references of G5 are never opened for unparseable outputs; CC-361 NB3)."""
    out = {}
    for g, spec in GROUPS.items():
        rows = {}
        for n, rel in spec["files"].items():
            p = fl / rel
            if p.is_file():
                provenance(rel, p)
            rows[n] = (parse_or_none(p) if p.is_file() else None, p)
        parsed = spec.get("with_baselines") or any(r is not None for r, _ in rows.values())
        refs, rsha = group_refs(g, fl) if parsed else ({}, None)
        files = {}
        for n, (r, p) in rows.items():
            if not p.is_file() or (r is not None and not refs):
                rec, preds = {"admitted": False, "reasons": ["missing: the file or its reference file is not on the host"]}, {}
            else:
                rec, preds = gate2(r, refs)
            files[n] = (rec, preds, p)
        if spec.get("with_baselines"):
            for n in BASE:
                rec, preds = gate2(list(load_base(base, n).items()), refs)
                files[n] = (rec, preds, base / BASE[n])
        out[g] = {"refs": refs, "refs_sha256": rsha, "files": files}
    return out


def fl_comps(fin: dict) -> list[dict]:
    """§4.3: a comparison of two admitted files of one group is formed when their covered id sets overlap in at least
    95% of the reference file's ids; it is scored on that intersection. The baseline pair is in D, not in FL."""
    out = []
    for g, d in fin.items():
        ok = sorted(n for n, (rec, _, _) in d["files"].items() if rec["admitted"])
        for k, a in enumerate(ok):
            for b_ in ok[k + 1:]:
                if a in BASE and b_ in BASE:
                    continue
                ids = sorted(set(d["files"][a][1]) & set(d["files"][b_][1]))
                out.append({"id": f"FL:{g}:{a}|{b_}", "set": "FL", "group": g, "repo": GROUPS[g]["repo"], "a": a,
                            "b": b_, "n": len(ids), "ids_sha256": hashlib.sha256("\n".join(ids).encode()).hexdigest(),
                            "formed": len(ids) >= GATE["overlap"] * len(d["refs"]), "classes": {}})
    return out


# ------------------------------------------------------------------------------------------------ §3 scoring and bootstrap
@functools.lru_cache(maxsize=None)
def boot_W(n: int, seed: int = SEED) -> np.ndarray:
    """§3.1: B draws of the image indices; W[b, j] = how often image j is drawn in draw b (numpy default_rng)."""
    idx = np.random.default_rng(seed).integers(0, n, (B, n))
    W = np.zeros((B, n))
    np.add.at(W, (np.arange(B)[:, None], idx), 1.0)
    return W


def stats(d: np.ndarray, W: np.ndarray) -> list[float]:
    """§3.1: D, the 2.5th and 97.5th percentiles of the paired image-bootstrap D (two-sided 95%), and sd_boot."""
    boot = W @ d / len(d)
    lo, hi = np.percentile(boot, [2.5, 97.5])
    return [float(d.mean()), float(lo), float(hi), float(boot.std(ddof=1))]


def bleu_img(refs: list[str], hyp: str) -> list[int]:
    """Per-image counts of E4.bleu4 ('closest'), so that corpus BLEU-4 can be resampled over images; the self-test
    checks bleu_corpus(sum) == E4.bleu4."""
    h, maxc, lens = hyp.split(), defaultdict(int), []
    for r in refs:
        lens.append(len(r.split()))
        for g, c in E4.ngrams(r).items():
            maxc[g] = max(maxc[g], c)
    corr = [0] * 4
    for g, c in E4.ngrams(hyp).items():
        corr[len(g) - 1] += min(maxc.get(g, 0), c)
    return corr + [max(0, len(h) - k) for k in range(4)] + [len(h), min((abs(x - len(h)), x) for x in lens)[1]]


def bleu_corpus(S: np.ndarray, n: int = 4) -> np.ndarray:
    """Corpus BLEU-n (n = 4, or n = 1 for the FE-ID BLEU-1 of CC-361 D12) from summed bleu_img counts."""
    tiny, small = 1e-15, 1e-9
    b = np.prod((S[..., 0:n] + tiny) / (S[..., 4:4 + n] + small), axis=-1) ** (1 / n)
    ratio = (S[..., 8] + tiny) / (S[..., 9] + small)
    return 100 * np.where(ratio < 1, b * np.exp(1 - 1 / ratio), b)


def bleu_stats(sa: np.ndarray, sb: np.ndarray, W: np.ndarray) -> list[float]:
    boot = bleu_corpus(W @ sa) - bleu_corpus(W @ sb)
    lo, hi = np.percentile(boot, [2.5, 97.5])
    return [float(bleu_corpus(sa.sum(0)) - bleu_corpus(sb.sum(0))), float(lo), float(hi), float(boot.std(ddof=1))]


def scorer(tk: FM.Tok, refs: dict, ids: list[str], texts: dict):
    """per_fn for run_list: member -> per-image CIDEr-D, ROUGE-L, BLEU counts and token keys of every file on ids,
    the member applied to outputs and references alike (§2.3 'matched'); df from the references of ids (§3.1)."""
    def per(m):
        R = {i: [tk.side(r, "matched", m, True) for r in refs[i]] for i in ids}
        cid = E4.Cider(R)
        out = {"_refs": FM.key(["\t".join(R[i]) for i in ids])}
        for f, t in texts.items():
            H = {i: tk.side(t[i], "matched", m, False) for i in ids}
            out[f] = {"cider": cid.per_image(H), "rouge": np.array([E4.rouge_l({i: R[i]}, {i: H[i]}) for i in ids]),
                      "bleu": np.array([bleu_img(R[i], H[i]) for i in ids], float), "key": FM.key([H[i] for i in ids])}
        return out
    return per


def run_list(ids: list[str], comps: list[dict], mems, per_fn) -> None:
    W = boot_W(len(ids))  # one index matrix per image list, shared by every member and comparison (§3.1)
    for m in mems:
        per = per_fn(m)
        for c in comps:
            add_class(c, m, per[c["a"]], per[c["b"]], per["_refs"], W)


def add_class(c: dict, m, pa: dict, pb: dict, kr: str, W) -> None:
    k = f"{pa['key']}|{pb['key']}|{kr}"  # §2.5: one class = identical tokens of both files and the references
    cl = c["classes"].setdefault(k, {"members": []})
    cl["members"].append(FM.name(m))
    if "cider" not in cl:
        cl["cider"] = stats(pa["cider"] - pb["cider"], W)
        cl["rouge"] = stats(pa["rouge"] - pb["rouge"], W)
        cl["bleu"] = bleu_stats(pa["bleu"], pb["bleu"], W)


# ------------------------------------------------------------------------------------------------ §3.2 decision rule
def sig(s) -> int:
    return 1 if s[1] > 0 else -1 if s[2] < 0 else 0


def zval(s) -> float:
    return abs(s[0]) / s[3] if s[3] > 0 else (float("inf") if abs(s[0]) > 1e-9 else 0.0)


def certify(c: dict, G: set, metric: str = "cider") -> dict | None:
    """§3.2 over the classes of family G (a class is in G when one of its members is)."""
    cls = [cl for cl in c["classes"].values() if G & set(cl["members"])]
    if not cls:
        return None
    sg = [sig(cl[metric]) for cl in cls]
    f0 = [s for cl, s in zip(cls, sg) if F0N in cl["members"] and F0N in G]
    s0 = f0[0] if f0 else 0
    if all(s == 1 for s in sg):
        v, cert = "CERTIFIED (a > b)", 1
    elif all(s == -1 for s in sg):
        v, cert = "CERTIFIED (b > a)", -1
    else:
        v, cert = ("REVERSED" if 1 in sg and -1 in sg else "FRAGILE" if any(sg) else "NULL-STABLE"), 0
    nominal = s0 or (1 if sg.count(1) > sg.count(-1) else -1 if sg.count(-1) > sg.count(1) else 0)
    brk = [cl for cl, s in zip(cls, sg) if s != nominal] if not cert and nominal else []
    lv = Counter(x for cl in brk for mn in cl["members"] if mn in G for x in mn.split("."))
    Ds = [cl[metric][0] for cl in cls if abs(cl[metric][0]) > 1e-9]
    return {"verdict": v, "certified": cert, "fragile": not cert and any(sg), "nominal": nominal,
            "sig_f0": s0 if f0 else None, "changed": bool(f0) and s0 != 0 and not cert, "classes": len(cls),
            "breaking": {"classes": len(brk), "levels": dict(sorted(lv.items()))},
            "point_flip": any(D > 0 for D in Ds) and any(D < 0 for D in Ds),
            "z_min": min(zval(cl[metric]) for cl in cls)}


def counts(comps: list[dict], G: set, metric: str = "cider") -> dict:
    vs = [v for v in (certify(c, G, metric) for c in comps) if v]
    n_sig = sum(v["sig_f0"] not in (None, 0) for v in vs)
    k = sum(v["changed"] for v in vs)
    return {"comparisons": len(vs), "CERTIFIED": sum(bool(v["certified"]) for v in vs),
            "FRAGILE": sum(v["fragile"] for v in vs), "REVERSED": sum(v["verdict"] == "REVERSED" for v in vs),
            "NULL-STABLE": sum(v["verdict"] == "NULL-STABLE" for v in vs), "significant_under_f0": n_sig,
            "CHANGED": k, "CHANGED_share": k / n_sig if n_sig else None,  # §3.2: denominator = significant under f0
            "point_flips": sum(v["point_flip"] for v in vs),
            "breaking_levels": dict(sum((Counter(v["breaking"]["levels"]) for v in vs), Counter()))}


def held_break(c: dict, s: int, H: set) -> tuple[bool, bool]:
    """§6.1: break = the certified direction s is not significant under at least one class of H; reversal =
    significant the other way, or a point-sign flip against s, under a class of H."""
    cls = [cl["cider"] for cl in c["classes"].values() if H & set(cl["members"])]
    brk = any(sig(x) != s for x in cls)
    rev = any(sig(x) == -s or (s * x[0] < 0 and abs(x[0]) > 1e-9) for x in cls)
    return brk, rev


def verdict_set(cert: list[tuple[str, float]]) -> tuple[list[str], str]:
    """§6.1: V = the certified comparisons with z_min <= 4; if |V| < 59, V = all of them."""
    near = [i for i, z in cert if z <= Z_NEAR]
    return (near, "near-margin z_min <= 4") if len(near) >= N_MIN else ([i for i, _ in cert], "fallback: all of Cert")


def cp_upper(k: int, n: int) -> float:
    return 1.0 if k >= n else float(beta.ppf(1 - CP_ALPHA, k + 1, n - k))


def cp_lower(k: int, n: int) -> float:
    return 0.0 if k <= 0 else float(beta.ppf(CP_ALPHA, k, n - k + 1))


def p1_rule(n: int, breaks: int, held_empty: bool) -> dict:
    """§6.1 Rule; §10 K-N; F_held empty (census or K-unit) -> NOT_EVALUABLE."""
    up, lo = cp_upper(breaks, n), cp_lower(breaks, n)
    if held_empty or n < N_MIN:
        lab = "NOT_EVALUABLE"
    elif up <= R_MAX:
        lab = "PASS"
    elif lo > R_MAX:
        lab = "FAIL"
    else:
        lab = "INCONCLUSIVE"
    return {"label": lab, "N": n, "breaks": breaks, "r": breaks / n if n else None, "cp_upper_95": up, "cp_lower_95": lo}


def p2_rule(n: int, k: int) -> str:
    """§6.2."""
    if n < NFL_MIN:
        return "NOT_EVALUABLE"
    return "SUPPORTED" if k >= KFL_MIN and k / n >= KFL_SHARE else "NOT SUPPORTED"


def nc_rule(comps: list[dict], syl: set, other: set) -> dict:
    """§6.1 NC (CC-350 W1): on D, certificates over the syl members, the verdict-set rule of P1, breaks under rdr/pyvi."""
    cert = [(c, v) for c in comps if (v := certify(c, syl)) and v["certified"]]
    V, rule = verdict_set([(c["id"], v["z_min"]) for c, v in cert])
    Vs = set(V)
    br = sum(held_break(c, v["certified"], other)[0] for c, v in cert if c["id"] in Vs)
    r = br / len(V) if V else None
    status = ("NOT_EVALUABLE: sensitivity not measured" if len(V) < N_MIN else
              "LOW-SENSITIVITY" if r <= R_MAX else "sensitive")
    return {"cert_NC": len(cert), "V_NC": len(V), "rule": rule, "breaks": br, "r_NC": r, "status": status}


def auc(pos: list[float], neg: list[float]) -> float | None:
    """Mann-Whitney AUC that a CHANGED comparison has the smaller f0 margin (§6.6 FE-PRED)."""
    if not pos or not neg:
        return None
    return sum((p < q) + 0.5 * (p == q) for p in pos for q in neg) / (len(pos) * len(neg))


# ------------------------------------------------------------------------------------------------ §5 FE-ID
def tol(p: str) -> float:
    """§5.1: half a unit of the last printed digit, + 1e-9."""
    d = len(p.split(".")[1]) if "." in p else 0
    return 0.5 * 10 ** (-d) + 1e-9


def reproduces(s: dict, printed: dict) -> bool:
    return all(s.get(m) is not None and abs(s[m] - float(p)) <= tol(p) for m, p in printed.items())


def identify(printed: dict, sc: dict, keys: dict) -> dict:
    """§5.1: classes by token identity; IDENTIFIED (one reproducing class), AMBIGUOUS (two or more), OUTSIDE (none);
    margin = smallest max-metric distance between the reproducing class and any other class (printed scale).
    A non-r* class is held to the printed metrics of ID_METRICS, the r* class to every printed metric (CC-361 D12)."""
    pm = {m: p for m, p in printed.items() if m in ID_METRICS}
    if not pm:
        return {"label": "no printed metric that the members compute", "classes": 0, "reproducing": [],
                "margin": None, "nearest_distance": None}
    want = lambda c: printed if c[0] == FM.name(FM.RSTAR) else pm  # noqa: E731
    cls = [sorted(c) for c in FM.classes(keys)]
    rep = [c for c in cls if reproduces(sc[c[0]], want(c))]
    gap = lambda x, y: float("inf") if x is None or y is None else abs(x - y)  # noqa: E731  r* may lack a metric
    dist = lambda x, y: max(gap(sc[x].get(m), sc[y].get(m)) for m in pm)  # noqa: E731
    lab = "IDENTIFIED" if len(rep) == 1 else "AMBIGUOUS" if rep else "OUTSIDE"
    margin = min((dist(rep[0][0], c[0]) for c in cls if c is not rep[0]), default=None) if len(rep) == 1 else None
    nearest = min(max(gap(sc[c[0]].get(m), float(p)) for m, p in want(c).items()) for c in cls)
    return {"label": lab, "classes": len(cls), "reproducing": rep, "margin": margin, "nearest_distance": nearest}


def check_plants(ident: dict, key: dict) -> dict:
    """§6.4 (CC-350 W2): a wrong recovery (IDENTIFIED with a class without the true member) is a FAULT, not a FAIL."""
    wrong = [n for n, r in ident.items() if r["label"] == "IDENTIFIED" and key[n] not in r["reproducing"][0]]
    if wrong:
        raise Fault(f"P4 method check: wrong recovery on {len(wrong)} planted case(s); stage 3 stops (§6.4)")
    c = Counter(r["label"] for r in ident.values())
    return {"IDENTIFIED": c["IDENTIFIED"], "AMBIGUOUS": c["AMBIGUOUS"], "OUTSIDE": c["OUTSIDE"],
            "margins": {n: r["margin"] for n, r in ident.items()},
            "identification": "NOT_EVALUABLE (K-plant)" if c["IDENTIFIED"] < PLANT_MIN else "evaluable"}


def rstar_real(refs: dict, hyps: dict) -> dict:
    """r*: pycocoevalcap 1.2 through rescap.metrics.CaptionMetrics (PTB tokeniser, Bleu(4), METEOR, Rouge, Cider; the
    scorers of COCOEvalCap.evaluate without SPICE), both sides as released (no N step, underscores kept), x100."""
    from rescap.metrics import CaptionMetrics
    cm = CaptionMetrics(language="en", use_meteor=True, use_spice=False, tokenize=True)
    s = cm.compute({i: refs[i] for i in hyps}, {i: [h] for i, h in hyps.items()})
    if any("PTB tokenizer unavailable" in w for w in cm.warnings):
        return {}
    ren = {"CIDEr": "CIDEr-D"}
    return {ren.get(k, k): (100 * v if isinstance(v, float) else None) for k, v in s.items()
            if ren.get(k, k) in P3_SCOPE}


RSTAR = rstar_real


def fe_table(tk: FM.Tok, refs: dict, ids: list[str], hyp: dict, pool: list) -> tuple[dict, dict]:
    """Scores (ID_METRICS for non-r* members, every r* metric for r*) and token keys of one output file under each entry of F+ (§5.1)."""
    sc, keys, cid = {}, {}, {}
    for e in pool:
        n = FM.name(e)
        if e == FM.RSTAR:
            sc[n], keys[n] = RSTAR({i: refs[i] for i in ids}, {i: hyp[i] for i in ids}), "r*"
            continue
        way, m = e
        R = {i: [tk.side(r, way, m, True) for r in refs[i]] for i in ids}
        H = {i: tk.side(hyp[i], way, m, False) for i in ids}
        kr = FM.key(["\t".join(R[i]) for i in ids])
        if kr not in cid:
            cid[kr] = E4.Cider(R)
        S = np.array([bleu_img(R[i], H[i]) for i in ids], float).sum(0)  # BLEU-1 from the per-image counts (D12)
        sc[n] = {"CIDEr-D": float(cid[kr].per_image(H).mean()), "BLEU-1": float(bleu_corpus(S, 1)),
                 "BLEU-4": E4.bleu4(R, H), "ROUGE-L": E4.rouge_l(R, H)}
        keys[n] = f"{FM.key([H[i] for i in ids])}|{kr}"
    return sc, keys


def k_coco() -> tuple[bool, list[str], dict]:
    """§6.3, §10 K-coco: r* on a toy fixture (no data) before any baseline is scored. A failing metric is dropped;
    CIDEr-D or BLEU-4 failing means P3 NOT RUN."""
    toy_r = {"1": ["a dog runs on the grass", "a dog on grass"], "2": ["two cats sit on a red sofa", "cats on a sofa"]}
    try:
        got = RSTAR(toy_r, {"1": "a dog runs on grass", "2": "two cats on a sofa"})
    except ImportError as e:  # an environment fault, never a K-coco drop (CC-361 D7)
        raise Fault(f"r*: rescap or pycocoevalcap does not import ({type(e).__name__})") from None
    except Exception:  # scorer-level failure on the toy fixture: K-coco
        got = {}
    dropped = [m for m in P3_SCOPE if got.get(m) is None]
    return ("CIDEr-D" not in dropped and "BLEU-4" not in dropped), dropped, got


def p3_rule(printed: dict, rs: dict, dropped: list[str]) -> dict:
    """§6.3 (CC-350 W3). printed {baseline: {metric: str}}; rs {baseline: r* scores}. The registered prediction is P3a
    on M_new (in-scope printed metrics other than CIDEr-D and BLEU-4); the CIDEr-D/BLEU-4 part is POST HOC."""
    scope = [m for m in P3_SCOPE if m not in dropped]
    rows = {b: {m: {"printed": p, "rstar": rs[b].get(m), "reproduced": reproduces(rs[b], {m: p}),
                    "distance": None if rs[b].get(m) is None else abs(rs[b][m] - float(p))}
                for m, p in printed[b].items() if m in scope} for b in printed}
    m_new = sorted({m for b in rows for m in rows[b]} - {"CIDEr-D", "BLEU-4"})
    old = {b: {m: r for m, r in rows[b].items() if m in ("CIDEr-D", "BLEU-4")} for b in rows}
    if not m_new:
        lab = "no registered label (M_new empty); CIDEr-D and BLEU-4 reproduction by r* is POST HOC"
    else:
        lab = ("SUPPORTED" if all(rows[b][m]["reproduced"] for b in rows for m in m_new if m in rows[b])
               else "NOT SUPPORTED")
    return {"label": lab, "evidence": "REGISTERED PREDICTION, DEVELOPMENT DATA (M_new only)", "M_new": m_new,
            "M_new_rows": {b: {m: rows[b][m] for m in m_new if m in rows[b]} for b in rows},
            "cider_bleu4_POST_HOC": old, "not_used": {b: sorted(set(printed[b]) - set(scope)) for b in printed}}


# ------------------------------------------------------------------------------------------------ plan §2 candidates
def display(t: str) -> str:
    """Plan §3.1: N, the final-punctuation run removed (κ step 5), the first character upper-cased if a letter."""
    d = FM.p_pre(FM.n_step(t), "pf")
    return d[:1].upper() + d[1:] if d[:1].isalpha() else d


def pair_stratum(ds: float, dw: float, dp: float) -> str | None:
    """Plan §2.3 with ε = 10 (§2.2): P punctuation flip, U unit flip, C control; at most one."""
    big = lambda *x: all(abs(v) >= EPS for v in x)  # noqa: E731
    pf = big(dp, dw) and (dp > 0) != (dw > 0)
    uf = big(ds, dw) and (ds > 0) != (dw > 0)
    if pf and not uf:
        return "P"
    if uf and not pf:
        return "U"
    if big(ds, dw, dp) and (ds > 0) == (dw > 0) == (dp > 0):
        return "C"
    return None


M_SYL, M_WORD, M_PK = ("syl", "tw", "pa", "cf"), ("rdr", "tw", "pa", "cf"), FM.F0  # plan §2.2


CAND_FIELDS = ("a", "b", "stratum", "d_syl", "d_word", "d_pk")  # the PAIR_CANDIDATES contract of build_pairs.py (D3)


def candidates(texts: dict, fams: dict, ids: list[str], per: dict) -> dict:
    """Plan §2.1-§2.4 step 1: per image, the candidates by file names and the three d values; no text. Written in the
    contract build_pairs.load_inputs reads (CC-361 D3): {epsilon, eligible_images, images: {id: [{a, b, stratum, d_syl,
    d_word, d_pk}]}}; image file names come from test_data.json :: images[].filename in both tools."""
    short = sorted(n for n in texts if stratum(n) == "short")
    disp = {n: {i: display(texts[n][i]) for i in ids} for n in short}
    images, elig = {}, Counter()
    for j, i in enumerate(ids):
        cs = []
        for k, a in enumerate(short):
            for b_ in short[k + 1:]:
                da, db = disp[a][i], disp[b_][i]
                if fams[a] == fams[b_] or not da or not db or tok_diff(da, db) < 2:
                    continue
                d = [float(per[m][a][j] - per[m][b_][j]) for m in (M_SYL, M_WORD, M_PK)]
                s = pair_stratum(*d)
                if s:
                    cs.append(dict(zip(CAND_FIELDS, (a, b_, s, *d))))
        elig.update({c["stratum"] for c in cs})
        images[i] = cs
    return {"epsilon": EPS, "eligible_images": {s: elig[s] for s in "PUC"}, "images": images}


# ------------------------------------------------------------------------------------------------ plan §5 human arm
def kappa(x: list, y: list) -> float | None:
    cats = sorted(set(x) | set(y), key=str)
    if not x:
        return None
    po = sum(a == b for a, b in zip(x, y)) / len(x)
    pe = sum((x.count(c) / len(x)) * (y.count(c) / len(y)) for c in cats)
    return (po - pe) / (1 - pe) if pe < 1 else None


def ac1(x: list, y: list, cats=("a", "b", "tie")) -> float | None:
    if not x:
        return None
    pa = sum(a == b for a, b in zip(x, y)) / len(x)
    pe = sum(p * (1 - p) for p in ((x.count(c) + y.count(c)) / (2 * len(x)) for c in cats)) / (len(cats) - 1)
    return (pa - pe) / (1 - pe) if pe < 1 else None


def cp_two(k: int, n: int, conf: float) -> list[float]:
    a = (1 - conf) / 2
    return [0.0 if k == 0 else float(beta.ppf(a, k, n - k + 1)), 1.0 if k == n else float(beta.ppf(1 - a, k + 1, n - k))]


def last_labels(p: Path) -> dict[str, str]:
    out = {}
    if p.is_file():
        for ln in p.read_text(encoding="utf-8").splitlines():
            r = json.loads(ln)
            out[r["qid"]] = r["label"]  # the server's rule: the last line for a qid wins (plan §5.1)
    return out


KEY_FIELDS = {"image", "part", "stratum", "a", "b", "file_left", "file_right", "d_syl", "d_word", "d_pk", "repeat_of"}


def key_items(key: dict) -> dict:
    """key.json as build_pairs.py writes it (CC-361 D4/D15): {"salt", "items": {qid: KEY_FIELDS}}; else FAULT."""
    items = key.get("items") if isinstance(key, dict) else None
    if not isinstance(items, dict) or any(set(k) != KEY_FIELDS for k in items.values()):
        raise Fault("key.json is not in the build_pairs.py contract (CC-361 D4)")
    return items


def ident(k: dict, lab: str | None) -> str | None:
    """Screen side -> caption identity (plan §5.1): A = file_left, B = file_right; T tie; X cannot."""
    if lab in ("A", "B"):
        return "a" if (k["file_left"] if lab == "A" else k["file_right"]) == k["a"] else "b"
    return {"T": "tie", "X": "cannot"}.get(lab)


def rated_both(ans: dict, qs: list) -> list:
    """Plan §5.4: the pairs both raters answered with neither choosing cannot; one definition for the kappa gate and
    the agreement rows (CC-361 D11)."""
    return [q for q in qs if all(ans[r][q] not in (None, "cannot") for r in ("PI", "R2"))]


def human(key: dict, labs: dict, elig: dict) -> dict:
    """Plan §5, §7: decisive consensus, H-P (one-sided) and H-U (two-sided) exact binomial, Holm at 0.05, kappa rule.
    key = key_items(key.json): main = part 'main', repeats = part 'repeat', practice never used (CC-361 D4)."""
    main = sorted(q for q, k in key.items() if k["part"] == "main")
    two = "R2" in labs and all(q in labs["R2"] for q in main)
    raters = ("PI", "R2") if two else ("PI",)
    ans = {r: {q: ident(key[q], labs.get(r, {}).get(q)) for q in main} for r in raters}
    hi = {q: "a" if key[q]["d_word"] > 0 else "b" for q in main}
    why, dec = Counter(), {}
    for q in main:
        a = [ans[r][q] for r in raters]
        if all(x == a[0] for x in a) and a[0] in ("a", "b"):
            dec[q] = a[0]
        else:
            why["missing" if None in a else "cannot" if "cannot" in a else "tie" if "tie" in a else "split"] += 1
    rows = {}
    for s in "PUC":
        qs = [q for q in dec if key[q]["stratum"] == s]
        k = sum(dec[q] == hi[q] for q in qs)
        rows[s] = {"n_dec": len(qs), "k_word": k, "q": k / len(qs) if qs else None, "ci95": cp_two(k, len(qs), 0.95)}
    pP = binomtest(rows["P"]["k_word"], rows["P"]["n_dec"], 0.5, alternative="greater").pvalue if rows["P"]["n_dec"] else 1.0
    pU = binomtest(rows["U"]["k_word"], rows["U"]["n_dec"], 0.5).pvalue if rows["U"]["n_dec"] else 1.0
    rej = holm({"H-P": pP, "H-U": pU})
    if not two:
        gate = "single rater"
    else:
        both = rated_both(ans, main)
        kap = kappa([ans["PI"][q] for q in both], [ans["R2"][q] for q in both])
        gate = ("labels" if kap is not None and kap >= KAPPA_LABEL else
                "low inter-rater agreement" if kap is not None and kap >= KAPPA_MIN else "NOT_EVALUABLE")
    nP, nU = rows["P"]["n_dec"], rows["U"]["n_dec"]
    if elig["P"] < H_P_MIN:
        hp = "NOT_EVALUABLE"
    else:
        hp = "SUPPORTED" if rej["H-P"] else "NOT SUPPORTED" if nP >= H_P_POWER else "UNDERPOWERED"
    if elig["U"] < H_U_MIN:
        hu = "NOT_EVALUABLE"
    elif rej["H-U"]:
        hu = "WORD AGREES MORE" if rows["U"]["q"] > 0.5 else "SYLLABLE AGREES MORE"
    else:
        lo, up = cp_two(rows["U"]["k_word"], nU, 0.90)
        hu = "EQUIVALENT within ±0.10" if nU and 0.40 <= lo and up <= 0.60 else "INCONCLUSIVE"
    out = {"raters": list(raters), "gate": gate, "not_decisive": dict(why), "strata": rows, "p": {"H-P": pP, "H-U": pU},
           "holm_rejected": rej, "H-P": hp if gate == "labels" else gate, "H-U": hu if gate == "labels" else gate}
    out.update(agreement(key, labs, main, raters, ans, dec, hi))
    return out


def holm(p: dict, alpha: float = 0.05) -> dict:
    order = sorted(p, key=p.get)
    rej, go = {}, True
    for j, h in enumerate(order):
        go = go and p[h] <= alpha / (len(order) - j)
        rej[h] = go
    return rej


def agreement(key, labs, main, raters, ans, dec, hi) -> dict:
    """Plan §5.4-§5.5 rows beside the hypotheses (no verdict)."""
    out = {"tie_cannot_rates": {r: {x: sum(ans[r][q] == x for q in main) / max(1, len(main)) for x in ("tie", "cannot")}
                                for r in raters}}
    if len(raters) == 2:
        both = rated_both(ans, main)
        x, y = [ans["PI"][q] for q in both], [ans["R2"][q] for q in both]
        rng = np.random.default_rng(H_SEED)
        bs = [kappa([x[j] for j in ix], [y[j] for j in ix]) for ix in rng.integers(0, len(both), (H_BOOT, len(both)))] if both else []
        bs = [v for v in bs if v is not None]
        dd = [j for j in range(len(both)) if x[j] in ("a", "b") and y[j] in ("a", "b")]
        out["inter_rater"] = {"n": len(both), "kappa": kappa(x, y), "kappa_ci95": list(np.percentile(bs, [2.5, 97.5])) if bs else None,
                              "raw": sum(a == b for a, b in zip(x, y)) / max(1, len(x)), "ac1": ac1(x, y),
                              "kappa_two_category": kappa([x[j] for j in dd], [y[j] for j in dd]),
                              "kappa_per_stratum": {s: kappa([x[j] for j, q in enumerate(both) if key[q]["stratum"] == s],
                                                             [y[j] for j, q in enumerate(both) if key[q]["stratum"] == s]) for s in "PUC"}}
    reps = sorted(q for q, k in key.items() if k["part"] == "repeat")
    within = {}
    for r in raters:
        pr = [(ident(key[q], labs[r].get(q)), ans[r].get(key[q]["repeat_of"])) for q in reps]
        pr = [(u, v) for u, v in pr if u not in (None, "cannot") and v not in (None, "cannot")]
        within[r] = {"n": len(pr), "raw": sum(u == v for u, v in pr) / max(1, len(pr)),
                     "kappa": kappa([u for u, _ in pr], [v for _, v in pr])}
    out["within_rater"] = within
    alone = {}
    for r in raters:
        row = {}
        for s, alt in (("P", "greater"), ("U", "two-sided")):
            qs = [q for q in main if key[q]["stratum"] == s and ans[r][q] in ("a", "b")]
            k = sum(ans[r][q] == hi[q] for q in qs)
            row[s] = {"n": len(qs), "k_word": k, "p": binomtest(k, len(qs), 0.5, alternative=alt).pvalue if qs else None}
        alone[r] = row
    out["rater_alone"] = alone
    bins = {}
    for s in "PUC":
        qs = [q for q in dec if key[q]["stratum"] == s]
        if qs:
            med = float(np.median([abs(key[q]["d_word"]) for q in qs]))
            lo = [q for q in qs if abs(key[q]["d_word"]) <= med]
            up = [q for q in qs if abs(key[q]["d_word"]) > med]
            bins[s] = {"below_or_at_median": [sum(dec[q] == hi[q] for q in lo), len(lo)],
                       "above_median": [sum(dec[q] == hi[q] for q in up), len(up)]}
    out["margin_bins"] = bins
    return out


# ------------------------------------------------------------------------------------------------ environment (§2.6 F2)
def env_record(a) -> dict:
    jar = E4.VNC / "VnCoreNLP-1.2.jar"
    rec = {"python": platform.python_version(), "unidata_version": unicodedata.unidata_version,
           "jar_sha256": sha(jar) if jar.is_file() else None,
           "protocol_pilot_sha256": sha(Path(E4.__file__)), "numpy": np.__version__}
    for pkg in ("pyvi", "underthesea", "pycocoevalcap"):
        try:
            rec[pkg] = importlib.metadata.version(pkg)
        except importlib.metadata.PackageNotFoundError:
            rec[pkg] = None
    for pkg, w in (("pyvi", a.pyvi_wheel), ("underthesea", a.uts_wheel)):
        rec[f"{pkg}_wheel"] = {"name": Path(w).name, "sha256": sha(w)} if w and Path(w).is_file() else None
    try:  # §2.2 l.114: the call form is checked on the installed release (CC-361 D6)
        from underthesea import word_tokenize
        rec["underthesea_signature"] = str(inspect.signature(word_tokenize))
    except Exception:  # noqa: BLE001  absent or broken: env_check makes it a FAULT
        rec["underthesea_signature"] = None
    try:  # r* (CC-361 D7)
        import pycocoevalcap  # noqa: F401
        import rescap.metrics as RM
        rec["rstar_import"], rec["rescap_metrics_sha256"] = True, sha(Path(RM.__file__))
    except ImportError:
        rec["rstar_import"], rec["rescap_metrics_sha256"] = False, None
    rec["java"] = java_version()
    return rec


def java_version() -> str | None:
    try:
        r = subprocess.run(["java", "-version"], capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.SubprocessError):
        return None
    m = re.search(r'version "([^"]+)"', r.stderr)
    return m.group(1) if r.returncode == 0 and m else None


def rstar_check(rec: dict) -> None:
    """§6.3, §10 K-coco (CC-361 D7): a missing rescap or pycocoevalcap, pycocoevalcap other than 1.2, rescap/metrics.py
    off its pin or Java off its pin is a FAULT before any score; only a scorer-level failure on the toy fixture
    follows K-coco."""
    if (not rec["rstar_import"] or rec["pycocoevalcap"] != COCO_VERSION or rec["rescap_metrics_sha256"] != RESCAP_SHA
            or rec["java"] != JAVA_VERSION):
        raise Fault("the r* environment differs from its pins: rescap/pycocoevalcap import, pycocoevalcap 1.2, "
                    "rescap/metrics.py sha256, Java version (CC-361 D7)")


def env_check(rec: dict) -> None:
    """§2.2: the jar and protocol_pilot.py at their pins; pyvi equal to 0.1.1; underthesea present at the recorded
    release with its wheel sha256 and signature (else FAULT, never a K-unit drop; CC-361 D6); wheels named by version;
    the r* environment (rstar_check)."""
    if not (rec["jar_sha256"] or "").startswith(JAR_SHA) or not rec["protocol_pilot_sha256"].startswith(PILOT_SHA):
        raise Fault("the VnCoreNLP jar or protocol_pilot.py differs from its pin (§2.2)")
    if rec["pyvi"] != PYVI_VERSION:
        raise Fault(f"pyvi on the host is not {PYVI_VERSION} (§2.2)")
    if (rec["underthesea"] != UTS_VERSION or (rec["underthesea_wheel"] or {}).get("sha256") != UTS_WHEEL_SHA
            or not rec["underthesea_signature"]):
        raise Fault(f"underthesea is absent, not {UTS_VERSION}, without its wheel record or without a signature (§2.2)")
    for pkg in ("pyvi", "underthesea"):
        w = rec[f"{pkg}_wheel"]
        if not w or f"-{rec[pkg]}-" not in w["name"]:
            raise Fault(f"{pkg}: the wheel recorded is not the installed release (§2.2)")
    rstar_check(rec)


def code_shas() -> dict:
    mods = (Path(__file__), Path(FM.__file__), Path(E4.__file__), Path(PT.__file__), Path(b2.__file__), Path(BC.__file__),
            Path(sys.modules[pin_line.__module__].__file__), Path(sys.modules[tok_diff.__module__].__file__))
    return {str(p.resolve().relative_to(ROOT)) if ROOT in p.resolve().parents else p.name: sha(p) for p in mods}


def unit_sets(fam: dict, cen: dict) -> tuple[list[str], list[str]]:
    """F_dev and F_held units after K-unit (FAMILY.json) and the segmenter census (CENSUS.json, CC-353 N4)."""
    drop = set(fam["units_dropped"])
    dev = [u for u in FM.DEV_UNITS if u not in drop]
    held = [u for u in FM.HELD_UNITS if u not in drop]
    if cen["uts_moved_to_dev"]:
        dev, held = dev + held, []
    return dev, held


SEG = None  # the self-test injects stub units here


# ------------------------------------------------------------------------------------------------ stages
def grepro(got: dict, committed: dict) -> list[dict]:
    """§9 stage F: f0 reproduces the committed CIDEr-D within 0.01; a mismatch on a seen file is a FAULT. Coded reading
    (a), all 67 are seen (§9 l.182, l.339, l.359): any mismatch is a FAULT. CC-361 D13 is open (PI Q2; default (a));
    reading (b) of B_KAPPA §5.1 is not coded."""
    rows = [{"name": n, "abs_diff": abs(got[n] - committed[n]), "ok": abs(got[n] - committed[n]) <= GREPRO_TOL}
            for n in sorted(committed)]
    if not all(r["ok"] for r in rows):
        raise Fault(f"G-repro: f0 does not reproduce {sum(not r['ok'] for r in rows)} committed score(s) (K-rdr)")
    return rows


def st_F(a, rec: dict) -> dict:
    env = env_record(a)
    env_check(env)
    refs = PT.load_refs(REFS)
    ids = sorted(refs)
    flat = [r for i in ids for r in refs[i]]
    try:  # F3 on the toy strings first, then F1: a unit that raises is a FAULT, never a K-unit drop (CC-361 D6)
        f3 = {u: FM.f3(u, SEG) for u in ("rdr", "pyvi", "uts")}
        f1 = {u: FM.f1(u, flat, SEG) for u in ("rdr", "pyvi", "uts")}
    except Exception as e:  # noqa: BLE001
        raise Fault(f"a word unit raised in F3/F1 ({type(e).__name__}) (§2.6)") from None
    if f1["rdr"]["dropped"]:
        raise Fault("F1 fails for rdr (K-rdr)")
    dropped = [u for u in ("pyvi", "uts") if f1[u]["dropped"]]  # K-unit, before any score
    tk = FM.Tok(SEG)
    scored = {n: RES / f"{n}.json" for n in names() if (RES / f"{n}.json").is_file()}
    if len(scored) != EXPECT["scored"]:
        raise Fault(f"{len(scored)} committed score files, not {EXPECT['scored']}")
    committed = {n: float(jload(p)["results"][0]["scores_scaled_x100"]["CIDEr"]) for n, p in scored.items()}
    hyps = {n: PT.load_preds(RES / f"{n}.preds.json") for n in scored}
    tk.prime(flat + [h[i] for h in hyps.values() for i in ids], [FM.F0])
    R = {i: [tk.side(r, "matched", FM.F0, True) for r in refs[i]] for i in ids}
    cid = E4.Cider(R)
    got = {n: float(cid.per_image({i: tk.side(h[i], "matched", FM.F0, False) for i in ids}).mean())
           for n, h in hyps.items()}
    rec.update(env=env, F1=f1, units_dropped=dropped, F3=f3, G_repro=grepro(got, committed),
               no_committed_score=sorted(set(names()) - set(scored)), refs_sha256=sha(REFS), n_images=len(ids), n_refs=len(flat),
               family={"F": len(FM.F), "F_dev": len(FM.F_DEV), "F_held": len(FM.F_HELD), "F_plus": len(FM.FPLUS)})
    return {"FAMILY.json": rec}


def census(own: dict, b2dir: Path | None) -> dict:
    """Stage C census (CC-353 N4): the `segmenter` of every stored result row of the own files and every `segmenter`
    value or protocol column name in the b2_external score files; no score is read."""
    found = {}
    for n, p in own.items():
        found[n] = sorted({str(r.get("segmenter")) for r in jload(p).get("results", [])})

    def walk(o, acc):  # segmenter values, and the names of numeric fields (b2 protocol columns such as CIDEr_PYVI)
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "segmenter":
                    acc.add(str(v))
                elif isinstance(v, (int, float)):
                    acc.add(str(k))
                walk(v, acc)
        elif isinstance(o, list):
            for v in o:
                walk(v, acc)
    b2files = sorted(b2dir.rglob("*.json")) if b2dir is not None and b2dir.is_dir() else []
    if not b2files:  # CC-361 D10: a file, a missing or an empty folder would skip the census silently
        raise Fault("--b2-score must be a directory holding at least one *.json (stage C census)")
    b2sha = {}
    for p in b2files:
        acc = set()
        walk(jload(p), acc)
        found[f"b2_external/{p.relative_to(b2dir)}"] = sorted(acc)
        b2sha[f"b2_external/{p.relative_to(b2dir)}"] = sha(p)
    toks = [(f, s.lower()) for f, ss in found.items() for s in ss]
    uts = sorted({f for f, s in toks if "underthesea" in s or s.endswith("_uts")})
    char = sorted({f for f, s in toks if "char" in s or s.endswith("_chr")})
    return {"segmenter_census": found, "b2_score_sha256": b2sha, "underthesea_hits": uts, "uts_moved_to_dev": bool(uts),
            "character_unit_hits_logged_only": char}


def st_C(a, rec: dict) -> dict:
    ns = names()
    fams = {n: family(n) for n in ns}
    if len(ns) != EXPECT["systems"] or len(set(fams.values())) != EXPECT["families"]:
        raise Fault(f"{len(ns)} systems / {len(set(fams.values()))} families, not {EXPECT['systems']} / {EXPECT['families']}")
    lines = ["name\tstratum\tfamily\tsha256\tgit_blob\trole"]
    types = {}
    for n in ns:
        p = RES / f"{n}.preds.json"
        types[n] = dict(Counter(type(v).__name__ for v in jload(p).values()))
        lines.append(f"{n}\t{stratum(n)}\t{fams[n]}\t{sha(p)}\t{b2.git_blob(p.read_bytes())}\town")
    for n, f in BASE.items():
        p = Path(a.baselines) / f
        if b2.git_blob(p.read_bytes()) != BASE_BLOBS[n]:
            raise Fault(f"{n}: git blob differs from thesis-code 1a8d105 (CC-092 R1)")
        lines.append(f"{n}\tbaseline\t{n}\t{sha(p)}\t{BASE_BLOBS[n]}\tbaseline")
    D = [f"D:{x}|{y}" for k, x in enumerate(ns) for y in ns[k + 1:] if stratum(x) == stratum(y) and fams[x] != fams[y]]
    D.append("D:ktvic_resnetlstm|ktvic_vittrans")  # §4.1
    cen = census({n: RES / f"{n}.json" for n in ns if (RES / f"{n}.json").is_file()}, Path(a.b2_score) if a.b2_score else None)
    tsv = "\n".join(lines) + "\n"
    rec.update(cen, value_types=types, D=D, D_size=len(D), strata=dict(Counter(stratum(n) for n in ns)),
               families=len(set(fams.values())), systems_tsv_sha256=hashlib.sha256(tsv.encode("utf-8")).hexdigest())
    return {"SYSTEMS.tsv": tsv, "CENSUS.json": rec}


def st_G(a, rec: dict) -> dict:
    fin = fl_inputs(Path(a.fl), Path(a.baselines))
    files = {f"{g}/{n}": {**r, "sha256": sha(p) if p.is_file() else None, "group": g}
             for g, d in fin.items() for n, (r, _, p) in d["files"].items()}
    comps = [{k: v for k, v in c.items() if k != "classes"} for c in fl_comps(fin)]
    rec.update(files=files, refs_sha256={g: d["refs_sha256"] for g, d in fin.items()}, comparisons=comps,
               formed=sum(c["formed"] for c in comps),
               K_FL20=sum(c["formed"] for c in comps) < FL20, label="structure only; no score (§4.3)")
    return {"GATE2.json": rec}


def ktvic_comps(D: list[str]) -> list[dict]:
    return [{"id": c, "set": "D", "a": c[2:].split("|")[0], "b": c.split("|")[1], "classes": {}} for c in D]


def st_1(a, rec: dict, work: Path) -> dict:
    dev, held = unit_sets(jload(work / "FAMILY.json"), cen := jload(work / "CENSUS.json"))
    refs = PT.load_refs(REFS)
    ids = sorted(refs)
    texts = ktvic_texts(work, Path(a.baselines))
    if any(set(t) != set(ids) for t in texts.values()):
        raise Fault("an own or baseline file does not cover the KTVIC test ids")
    comps = ktvic_comps(cen["D"])
    mems = FM.members(dev)  # F_dev only before the pin (§9)
    tk = FM.Tok(SEG)
    tk.prime([r for i in ids for r in refs[i]] + [t[i] for t in texts.values() for i in ids], mems)
    run_list(ids, comps, mems, scorer(tk, refs, ids, texts))
    G = {FM.name(m) for m in mems}
    syl = {FM.name(m) for m in FM.members(("syl",))}
    other = {FM.name(m) for m in FM.members(("rdr", "pyvi"))}
    short = {n: t for n, t in texts.items() if n not in BASE and stratum(n) == "short"}
    per = {m: {n: v["cider"] for n, v in scorer(tk, refs, ids, short)(m).items() if n != "_refs"} for m in (M_SYL, M_WORD, M_PK)}
    fams = {s["name"]: s["family"] for s in systems(work)}
    image_files()  # every KTVIC test image name inside the route regex (CC-350 W6), else FAULT
    pairs = candidates(short, fams, ids, per)
    dev_rec = {**rec, "label": "DEVELOPMENT", "units_dev": dev, "units_held": held, "members": sorted(G),
               "counts_F_dev": counts(comps, G), "comparisons": comps}
    nc = {**rec, "label": "SENSITIVITY CONTROL (§6.1 NC)", **nc_rule(comps, syl, other)}
    return {"DEV.json": dev_rec, "NC.json": nc, "PAIR_CANDIDATES.json": {**rec, **pairs}}


def st_pin(a, work: Path) -> None:
    """§9 pin: read-only (444) copies of DEV.json and NC.json, and the LOG line text for the coordinator."""
    prev_ok(work, "DEV.json", a.prev, None)
    prev_ok(work, "NC.json", a.nc, None)
    pins = Path(a.pins)
    pins.mkdir(parents=True, exist_ok=True)
    for f in ("DEV.json", "NC.json"):
        if (pins / f).exists():
            raise SystemExit(f"REFUSED: {pins / f} exists")
        shutil.copy2(work / f, pins / f)
        os.chmod(pins / f, 0o444)
        if sha(pins / f) != sha(work / f):
            raise Fault(f"pin copy of {f} differs")
    pc = sha(work / "PAIR_CANDIDATES.json")  # logged at the pin; build_pairs --candidates-sha checks it (CC-361 NB9)
    print(f"PIN: log one line '<date -u> OPS-<id>-pin: DEV.json {a.prev} NC.json {a.nc} PAIR_CANDIDATES.json {pc}', "
          "then STOP")


def fl_texts(fin: dict, c: dict) -> tuple[list[str], dict, dict]:
    d = fin[c["group"]]
    ids = sorted(set(d["files"][c["a"]][1]) & set(d["files"][c["b"]][1]))
    if hashlib.sha256("\n".join(ids).encode()).hexdigest() != c["ids_sha256"]:
        raise Fault(f"{c['id']}: the intersection differs from GATE2.json")
    return ids, d["refs"], {n: d["files"][n][1] for n in (c["a"], c["b"])}


def score_fl(fin: dict, comps: list[dict], mems, tk: FM.Tok) -> None:
    lists = defaultdict(list)
    for c in comps:
        lists[c["ids_sha256"]].append(c)
    for cs in lists.values():
        ids, refs, _ = fl_texts(fin, cs[0])
        texts = {}
        for c in cs:
            texts.update(fl_texts(fin, c)[2])
        tk.prime([r for i in ids for r in refs[i]] + [t[i] for t in texts.values() for i in ids], mems)
        run_list(ids, cs, mems, scorer(tk, {i: refs[i] for i in ids}, ids, texts))


def gate_files(fin: dict, gate: dict) -> None:
    """2a, 2b, 3: every FL file and reference file still equals GATE2.json (CC-361 D9)."""
    for g, d in fin.items():
        if d["refs_sha256"] != gate["refs_sha256"][g]:
            raise Fault(f"{g}: the reference file differs from GATE2.json")
        for n, (r, _, p) in d["files"].items():
            want = gate["files"][f"{g}/{n}"]
            if (sha(p) if p.is_file() else None) != want["sha256"] or r["admitted"] != want["admitted"]:
                raise Fault(f"{g}/{n}: differs from GATE2.json")


def st_2a(a, rec: dict, work: Path) -> dict:
    gate = jload(work / "GATE2.json")
    dv = jload(work / "DEV.json")
    fin = fl_inputs(Path(a.fl), Path(a.baselines))
    gate_files(fin, gate)
    fl = [{**c, "classes": {}} for c in gate["comparisons"] if c["formed"]]
    mems = FM.members(dv["units_dev"])
    score_fl(fin, fl, mems, FM.Tok(SEG))
    G = set(dv["members"])
    cert = [(c["id"], v["z_min"]) for c in dv["comparisons"] + fl if (v := certify(c, G)) and v["certified"]]
    V, rule = verdict_set(cert)
    rec.update(label="FIRST SCORING OF RELEASED OUTPUTS (FL, F_dev only)", V=V, N=len(V), rule=rule,
               cert_dev=len(cert), cert_dev_FL=sum(i.startswith("FL:") for i, _ in cert), fl=fl,
               counts_FL_F_dev=counts(fl, G))
    return {"V.json": rec}


def st_2b(a, rec: dict, work: Path) -> dict:
    dv, vj, nc = jload(work / "DEV.json"), jload(work / "V.json"), jload(work / "NC.json")
    dev, held = dv["units_dev"], dv["units_held"]
    D, FL = dv["comparisons"], vj["fl"]
    mems = FM.members(held) + FM.F_CHR
    refs = PT.load_refs(REFS)
    ids = sorted(refs)
    texts = ktvic_texts(work, Path(a.baselines))
    tk = FM.Tok(SEG)
    tk.prime([r for i in ids for r in refs[i]] + [t[i] for t in texts.values() for i in ids], mems)
    run_list(ids, D, mems, scorer(tk, refs, ids, texts))
    fin = fl_inputs(Path(a.fl), Path(a.baselines))
    gate_files(fin, jload(work / "GATE2.json"))
    score_fl(fin, FL, mems, tk)
    Gd = set(dv["members"])
    Gh = {FM.name(m) for m in FM.members(held)}
    Gc = {FM.name(m) for m in FM.F_CHR}
    GF = Gd | Gh
    allc = {c["id"]: c for c in D + FL}
    vd = {i: certify(c, Gd) for i, c in allc.items()}

    def p1_over(sel, H):
        bk = [held_break(allc[i], vd[i]["certified"], H) for i in sel]
        return sum(b for b, _ in bk), sum(r for _, r in bk)
    br, rev = p1_over(vj["V"], Gh)
    p1 = {**p1_rule(len(vj["V"]), br, not Gh), "reversals": rev, "evidence": "REGISTERED PREDICTION",
          "verdict_set_rule": vj["rule"], "NC": nc["status"]}
    if nc["status"].startswith("NOT_EVALUABLE"):
        p1["words"] = "sensitivity not measured"
    elif nc["status"] == "LOW-SENSITIVITY":
        p1["LOW-SENSITIVITY"] = ("a one-unit family was broken by the other development units in at most 5% of its "
                                 "near-margin certificates, so the held-out check had little room to fail")
    cert_all = [i for i in allc if vd[i] and vd[i]["certified"]]
    flc = [i for i in cert_all if i.startswith("FL:")]
    fb = p1_over(flc, Gh)[0]
    beside = {"FL_row": {"n": len(flc), "breaks": fb, "cp_lower_95": cp_lower(fb, len(flc)),
                         "cp_upper_95": cp_upper(fb, len(flc)), "state_beside_P1": cp_lower(fb, len(flc)) > R_MAX},
              "all_Cert_dev": dict(zip(("breaks", "reversals"), p1_over(cert_all, Gh)), n=len(cert_all)),
              "D_only": dict(zip(("breaks", "reversals"), p1_over([i for i in cert_all if i.startswith("D:")], Gh))),
              "FL_only": dict(zip(("breaks", "reversals"), p1_over(flc, Gh))),
              "with_chr_DESCRIPTIVE": dict(zip(("breaks", "reversals"), p1_over(vj["V"], Gh | Gc)), N=len(vj["V"]))}
    vF = {i: certify(c, GF) for i, c in allc.items()}
    fl_ids = [c["id"] for c in FL]
    n_fl = sum(vF[i]["sig_f0"] not in (None, 0) for i in fl_ids)
    k_fl = sum(vF[i]["changed"] for i in fl_ids)
    repos = sorted({c["repo"] for c in FL})
    per_repo = {r: [sum(vF[c["id"]]["sig_f0"] not in (None, 0) for c in FL if c["repo"] == r),
                    sum(vF[c["id"]]["changed"] for c in FL if c["repo"] == r)] for r in repos}
    loo = {r: {"n": n_fl - per_repo[r][0], "k": k_fl - per_repo[r][1]} for r in repos}
    p2 = {"label": p2_rule(n_fl, k_fl), "evidence": "REGISTERED PREDICTION", "n_FL": n_fl, "k_FL": k_fl,
          "per_repository_n_k": per_repo, "leave_one_repository_out": loo,
          "K_FL20_descriptive": len(FL) < FL20}
    z0 = {i: zval(next(cl["cider"] for cl in c["classes"].values() if F0N in cl["members"])) for i, c in allc.items()}
    sig0 = [i for i in allc if vF[i]["sig_f0"] not in (None, 0)]
    no_ck = {m for m in GF if not m.endswith(".ck")}
    no_pk = {m for m in GF if ".pk." not in m}
    rec.update(P1=p1, P1_beside=beside, P2=p2,
               counts={"FL_over_F": counts(FL, GF), "FL_over_F_dev": counts(FL, Gd),
                       "D_over_F_DEVELOPMENT": counts(D, GF), "D_over_F_dev_DEVELOPMENT": counts(D, Gd),
                       "F_held_HELD-OUT_FRONT_END": counts(D + FL, Gh)},
               secondary={"FE_PRED_AUC": auc([z0[i] for i in allc if vF[i]["changed"]],  # §6.6 as registered: D ∪ FL
                                             [z0[i] for i in allc if not vF[i]["changed"]]),
                          "FE_PRED_AUC_f0_significant_EXTRA": auc([z0[i] for i in sig0 if vF[i]["changed"]],
                                                                  [z0[i] for i in sig0 if not vF[i]["changed"]]),
                          "BLEU-4_over_F": counts(D + FL, GF, "bleu"), "ROUGE-L_over_F": counts(D + FL, GF, "rouge"),
                          "F_without_ck": counts(D + FL, no_ck), "F_with_chr_DESCRIPTIVE": counts(D + FL, GF | Gc),
                          "F_without_pk": counts(D + FL, no_pk),
                          "English_control": "NOT RUN (no English output files named at the code read; §6.6, Q13)"},
               comparisons=[{"id": i, "a": c["a"], "b": c["b"], "set": c["set"], "repo": c.get("repo"),
                             "D_f0": next(cl["cider"][0] for cl in c["classes"].values() if F0N in cl["members"]),
                             "F": vF[i]["verdict"], "F_dev": vd[i]["verdict"], "changed_F": vF[i]["changed"]}
                            for i, c in allc.items()],
               units={"dev": dev, "held": held}, label_D="DEVELOPMENT", label_FL="FIRST SCORING OF RELEASED OUTPUTS")
    return {"RESULT.json": rec}


def st_3(a, rec: dict, work: Path) -> dict:
    fam = jload(work / "FAMILY.json")
    gate = jload(work / "GATE2.json")
    res = jload(work / "RESULT.json")
    env = env_record(a)
    rstar_check(env)  # CC-361 D7: before K-coco and before any score
    ok, dropped, _ = k_coco()  # before any baseline is scored (§6.3)
    drop_units = set(fam["units_dropped"])
    r_in = ok and not set(ID_METRICS) & set(dropped)  # r* enters F+ only if it computes every identification metric
    pool = [e for e in FM.FPLUS if (e == FM.RSTAR and r_in) or (e != FM.RSTAR and e[1][0] not in drop_units)]
    printed = printed_entries(Path(a.printed)) if a.printed else []
    by_file = {}
    for e in printed:
        if e.get("file") and e["file"] not in by_file:
            by_file[e["file"]] = e
    refs = PT.load_refs(REFS)
    ids = sorted(refs)
    own = ktvic_texts(work, Path(a.baselines), set(S_FILES) | set(BASE))
    if any(n not in own for n in S_FILES):
        raise Fault("a file of the seen set S is not in SYSTEMS.tsv (B_KAPPA §4.2)")
    fin = fl_inputs(Path(a.fl), Path(a.baselines))
    gate_files(fin, gate)
    targets = {}  # file -> (refs, ids, outputs) for every file FE-ID scores
    for f in by_file:
        if f in BASE:
            targets[f] = (refs, ids, own[f])
        g = next((g for g, d in fin.items() if f not in BASE and f in d["files"] and d["files"][f][0]["admitted"]), None)
        if g:
            h = fin[g]["files"][f][1]
            targets[f] = (fin[g]["refs"], sorted(h), h)
    tk = FM.Tok(SEG)
    mems = sorted({e[1] for e in pool if e != FM.RSTAR})
    tk.prime([r for i in ids for r in refs[i]] + [own[n][i] for n in own for i in ids], mems)
    for r_, i_, h_ in targets.values():
        tk.prime([r for i in i_ for r in r_[i]] + [h_[i] for i in i_], mems)
    # §5.3 planted check: score, draw, write PLANT_KEY / PLANT_PRINTED, identify from PLANT_PRINTED only, then compare
    tab = {n: fe_table(tk, refs, ids, own[n], pool) for n in S_FILES}
    rng = random.Random(SEED_PLANT)
    names_pool = sorted(FM.name(e) for e in pool)
    key = {n: rng.choice(names_pool) for n in S_FILES}
    pp = {n: {m: f"{tab[n][0][key[n]][m]:.1f}" for m in PLANT_METRICS} for n in S_FILES}
    write_once(work / "PLANT_KEY.json", {**rec, "key": key})
    write_once(work / "PLANT_PRINTED.json", {**rec, "printed": pp})
    shown = jload(work / "PLANT_PRINTED.json")["printed"]
    ident_p = {n: identify(shown[n], *tab[n]) for n in S_FILES}
    p4 = {**check_plants(ident_p, jload(work / "PLANT_KEY.json")["key"]), "label": "METHOD CHECK (§6.4)"}
    # FE-ID on every file with a printed value (baselines, admitted FL files); P3 on the baselines
    out, f0s = {}, {}
    for f in by_file:
        if f not in targets:
            out[f] = {"label": "not admitted (GATE2.json) or not released"}
            continue
        sc, keys = fe_table(tk, *targets[f], pool)
        pm = {m: p for m, p in by_file[f]["metrics"].items() if m in P3_SCOPE}
        out[f] = {**identify(pm, sc, keys), "printed_used": {"members": sorted(set(pm) & set(ID_METRICS)), "r*": sorted(pm)},
                  "METEOR_excluded_for_members": "METEOR" in pm}  # forced: no member-specific METEOR (CC-361 D12, NB13)
        if p4["identification"] != "evaluable":
            out[f]["label"] = "NOT_EVALUABLE (K-plant): reproduction table only"
        out[f]["P3b_matched_F_reproducing_CIDEr-D_POST_HOC"] = sorted(
            FM.name(m) for m in FM.F if FM.name(m) in sc and "CIDEr-D" in pm and reproduces(sc[FM.name(m)], {"CIDEr-D": pm["CIDEr-D"]}))
        f0s[f] = sc[F0N]["CIDEr-D"]
    pb = {b: dict(by_file[b]["metrics"]) for b in BASE if b in by_file}
    if not ok:
        p3 = {"label": "NOT RUN (K-coco)", "dropped": dropped}
    elif len(pb) < len(BASE):
        p3 = {"label": "NOT RUN (K-print: PRINTED.json lacks a baseline or was not logged)"}
    else:
        rs = {b: RSTAR({i: refs[i] for i in ids}, {i: own[b][i] for i in ids}) for b in pb}
        p3 = {**p3_rule(pb, rs, dropped), "dropped_K_coco": dropped, "identification": {b: out[b]["label"] for b in pb},
              "margin": {b: out[b]["margin"] for b in pb}}
    rec.update(env_rstar={k: env[k] for k in ("python", "pycocoevalcap", "rescap_metrics_sha256", "java", "rstar_import")},
               printed_sha256=sha(Path(a.printed)) if a.printed else None, P3=p3, P4=p4, plants={n: {k: v for k, v in r.items() if k != "reproducing"} for n, r in ident_p.items()},
               fe_id=out, printed_comparisons=printed_census(printed, res["comparisons"], f0s, gate), pool=len(pool),
               rstar_in_pool=r_in, label="FE-ID (§5); KTVIC CIDEr-D/BLEU-4 reproduction is POST HOC (O3)")
    return {"FEID.json": rec}


def printed_entries(p: Path) -> list[dict]:
    """§5.2 PRINTED.json in its pinned layout (CC-361 D1): sha256 asserted (the file is never edited); values.{source}[]
    {system, metric_as_printed, value_as_printed} mapped by PRINTED_SYSTEMS and PRINTED_METRICS; the decimals come from
    value_as_printed (a string). An unmapped system or metric, or a metric printed twice for one system, is a FAULT.
    Returns [{source, system, file, metrics: {in-scope name: value_as_printed}}] in file order."""
    if sha(p) != PRINTED_SHA:
        raise Fault("PRINTED.json differs from its pin (PIN-1112-b-fecert-printed)")
    by: dict = {}
    for src, rows in jload(p)["values"].items():
        for r in rows:
            k = (src, r["system"])
            if k not in PRINTED_SYSTEMS or r["metric_as_printed"] not in PRINTED_METRICS:
                raise Fault("PRINTED.json: a system or metric outside the registered map (CC-361 D1)")
            e = by.setdefault(k, {"source": src, "system": r["system"], "file": PRINTED_SYSTEMS.get(k), "metrics": {}})
            m = PRINTED_METRICS[r["metric_as_printed"]]
            if m in e["metrics"] or not isinstance(r["value_as_printed"], str):
                raise Fault("PRINTED.json: a metric printed twice for one system, or a value that is not a string")
            e["metrics"][m] = r["value_as_printed"]
    return list(by.values())


def printed_census(entries: list, comps: list, f0s: dict, gate: dict) -> dict:
    """§5.5 (DESCRIPTIVE): every pair of systems one source prints side by side; re-scorable, one-sided or neither."""
    adm = set(BASE) | {k.split("/")[1] for k, v in gate["files"].items() if v["admitted"]}
    by_pair = {frozenset((c["a"], c["b"])): c for c in comps}
    src = defaultdict(list)
    for e in entries:
        src[e["source"]].append(e)
    rows, n, k, m = [], 0, 0, 0
    for s, es in src.items():
        for j, x in enumerate(es):
            for y in es[j + 1:]:
                fx, fy = x.get("file") if x.get("file") in adm else None, y.get("file") if y.get("file") in adm else None
                px, py = x["metrics"].get("CIDEr-D"), y["metrics"].get("CIDEr-D")
                row = {"source": s, "x": x["system"], "y": y["system"]}
                c = by_pair.get(frozenset((fx, fy))) if fx and fy else None
                if c and px and py:
                    d0 = c["D_f0"] if c["a"] == fx else -c["D_f0"]
                    flip = (float(px) - float(py)) * d0 < 0
                    row.update(kind="re-scorable", printed_gap=float(px) - float(py), f0_gap=d0, order_changes=flip,
                               certificate_F=c["F"])
                    n, k, m = n + 1, k + flip, m + (not c["F"].startswith("CERTIFIED"))
                elif (fx or fy) and px and py:
                    rel, other = (fx, py) if fx else (fy, px)
                    row.update(kind="one-sided", gap_released_f0_minus_other_printed=(f0s[rel] - float(other)) if rel in f0s else None,
                               note="one side re-scored; the other side's pipeline unknown")
                else:
                    row.update(kind="neither")
                rows.append(row)
    return {"label": "DESCRIPTIVE", "n_rescorable": n, "order_changes_under_f0": k, "not_certified_over_F": m, "pairs": rows}


def st_H(a, rec: dict, work: Path) -> dict:
    d = Path(a.labels)
    files = [d / "key.json", d / "labels_PI.jsonl"] + ([d / "labels_R2.jsonl"] if (d / "labels_R2.jsonl").is_file() else [])
    also = [t for p in files[1:] for t in (sha(p), p.name)]
    if not pin_line(Path(a.log), sha(files[0]), files[0].name, *also):
        raise SystemExit("REFUSED: no closing LOG line with the hashes of key.json and the label files (plan §6)")
    key = key_items(jload(files[0]))
    labs = {p.name[len("labels_"):-len(".jsonl")]: last_labels(p) for p in files[1:]}
    elig = jload(work / "PAIR_CANDIDATES.json")["eligible_images"]
    if set(elig) != set("PUC"):
        raise Fault("PAIR_CANDIDATES.json is not in the build_pairs.py contract (CC-361 D3)")
    rec.update(inputs={p.name: sha(p) for p in files}, **human(key, labs, elig),
               label="new human judgements on previously analysed captions (plan §1)")
    return {"HUMAN.json": rec}


PREV = {"C": "FAMILY.json", "G": "CENSUS.json", "1": "GATE2.json", "2a": "DEV.json", "2b": "V.json",
        "3": "RESULT.json", "H": "FEID.json"}
INPUTS = {  # the other work files each stage reads (PREV is checked by prev_ok), each against its LOG pin line (CC-361 D8)
    "C": (), "G": ("FAMILY.json",), "1": ("FAMILY.json", "CENSUS.json"),
    "2a": ("FAMILY.json", "GATE2.json", "NC.json"),  # §4.3: GATE2.json logged before any FL score
    "2b": ("FAMILY.json", "CENSUS.json", "GATE2.json", "DEV.json", "NC.json"),
    "3": ("FAMILY.json", "CENSUS.json", "GATE2.json"), "H": ("FAMILY.json", "PAIR_CANDIDATES.json")}


def run(a) -> None:
    work = Path(a.work)
    work.mkdir(parents=True, exist_ok=True)
    if now() > K_TIME:
        raise SystemExit("REFUSED: K-time (§10): the stage is NOT RUN")
    if a.stage == "pin":
        return st_pin(a, work)
    log = Path(a.log) if a.stage != "F" else None
    if a.stage in PREV:
        prev_ok(work, PREV[a.stage], a.prev, log)
    if a.stage == "2a":
        if not pin_line(log, sha(work / "NC.json"), "NC.json", a.prev, "DEV.json"):
            raise SystemExit("REFUSED: no pin line with DEV.json and NC.json (§9: held-out and FL only after the pin)")
        if any(work.glob("RESULT*.json")):
            raise SystemExit("REFUSED: a RESULT*.json exists before stage 2a (§9)")
    if a.stage == "3":
        if a.printed:
            logged(log, Path(a.printed))
        elif not (a.k_print and now() > K_PRINT):
            raise SystemExit("REFUSED: PRINTED.json is not logged; --k-print only after 2026-11-15 12:00 VN (§10)")
    rec = {"registration": REG, "registration_sha256": REG_SHA, "stage": a.stage, "prev_sha256": a.prev,
           "utc_start": now(), "code_sha256": code_shas()}
    if a.stage in INPUTS:
        rec["inputs_sha256"] = {PREV[a.stage]: a.prev, **inputs(work, log, INPUTS[a.stage])}
    fn = {"F": lambda: st_F(a, rec), "C": lambda: st_C(a, rec), "G": lambda: st_G(a, rec), "1": lambda: st_1(a, rec, work),
          "2a": lambda: st_2a(a, rec, work), "2b": lambda: st_2b(a, rec, work), "3": lambda: st_3(a, rec, work),
          "H": lambda: st_H(a, rec, work)}[a.stage]
    outs = fn()
    if now() > K_TIME:
        raise Fault("K-time (§10): the stage finished after 2026-11-16 12:00 VN; NOT RUN")
    for f, o in outs.items():
        if isinstance(o, dict):
            o["utc_end"] = now()
        print(f"STAGE {a.stage}: {f} sha256 {write_once(work / f, o)}")
    print("write the sha256 above to the LOG as a pin line, then STOP")


# ------------------------------------------------------------------------------------------------ self-test
# Synthetic fixtures only, in a temp dir: stub word units and a stub r*, no system output, reference or fetched file.
# Each check runs under its own name: an AssertionError, Fault or SystemExit is FAIL, any other exception is CRASH.
CHECKS: list = []
MARK = "zqxv"  # one syllable in every synthetic caption and reference; no output or stdout may contain it
VOC = ["con chó", "con mèo", "bãi cỏ", "Hà Nội", "chiếc xe", "người đàn ông"]
OWN = ["p1_s42-short", "p1_s43-short", "fuse2_s42-short", "zeroshot-short", "p1_s42-detailed", "zeroshot-detailed"]


def check(fn):
    CHECKS.append(fn)
    return fn


def _join(pairs):
    """Stub word unit: whitespace split, then the listed syllable pairs (case-sensitive) joined with '_'."""
    def seg(ts):
        out = []
        for t in ts:
            w, res, k = t.split(), [], 0
            while k < len(w):
                if k + 1 < len(w) and (w[k], w[k + 1]) in pairs:
                    res.append(f"{w[k]}_{w[k + 1]}")
                    k += 2
                else:
                    res.append(w[k])
                    k += 1
            out.append(res)
        return out
    return seg


STUB = {"syl": FM.SEG["syl"], "chr": FM.SEG["chr"], "rdr": _join({("con", "chó"), ("Hà", "Nội"), ("bãi", "cỏ")}),
        "pyvi": _join({("bãi", "cỏ"), ("con", "mèo")}), "uts": _join({("chiếc", "xe"), ("đàn", "ông")})}


def _rstar_stub(refs, hyps):
    R = {i: [" ".join(r.split()) for r in refs[i]] for i in hyps}
    H = {i: " ".join(hyps[i].split()) for i in hyps}
    b4 = E4.bleu4(R, H)
    return {"BLEU-1": b4 / 2, "BLEU-2": None, "BLEU-3": None, "BLEU-4": b4, "METEOR": None,
            "ROUGE-L": E4.rouge_l(R, H), "CIDEr-D": float(E4.Cider(R).per_image(H).mean())}


def _env_stub(a) -> dict:
    return {"python": "3", "unidata_version": unicodedata.unidata_version, "jar_sha256": JAR_SHA + "0" * 56,
            "protocol_pilot_sha256": PILOT_SHA + "0" * 56, "pyvi": PYVI_VERSION, "underthesea": UTS_VERSION,
            "pycocoevalcap": COCO_VERSION, "pyvi_wheel": {"name": "pyvi-0.1.1-py2.py3-none-any.whl", "sha256": "0" * 64},
            "underthesea_wheel": {"name": f"underthesea-{UTS_VERSION}-py3-none-any.whl", "sha256": UTS_WHEEL_SHA},
            "underthesea_signature": "(sentence, format=None)", "rstar_import": True,
            "rescap_metrics_sha256": RESCAP_SHA, "java": JAVA_VERSION}


def _ref(i, j):
    return f"{MARK} {VOC[i % 6]} đang chạy trên {VOC[(i + j + 1) % 6]}."


def _cap(n, i):
    return {"p1_s42-short": _ref(i, 0), "p1_s43-short": _ref(i, 1).rstrip(".").lower(),
            "fuse2_s42-short": f"{MARK} {VOC[(i + 2) % 6]} trên {VOC[i % 6]}",
            "zeroshot-short": f"{MARK} Một bức ảnh có {VOC[(i + 3) % 6]} và cây.",
            "p1_s42-detailed": _ref(i, 0) + " Trời hôm nay đẹp.",
            "zeroshot-detailed": f"{MARK} ảnh chụp {VOC[(i + 1) % 6]} ở xa."}[n]


def _dump(p: Path, o) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False), encoding="utf-8")


def _build(data: Path, fl: Path, base: Path, b2d: Path) -> None:
    ids, ext = range(1, 7), ["jpg", "png", "jpeg", "jpg", "jpg", "jpg"]
    kt = data / "datasets/ktvic/test_data.json"
    _dump(kt, {"images": [{"id": i, "filename": f"{i:011d}.{e}"} for i, e in zip(ids, ext)],
               "annotations": [{"image_id": i, "id": 10 * i + j, "caption": _ref(i, j)} for i in ids for j in range(2)]})
    _dump(data / "results/tone_norm/ktvic_side_by_side.json", {"systems": {n: {} for n in OWN}})
    refs = PT.load_refs(kt)
    f0 = lambda t: " ".join(w.casefold() for w in STUB["rdr"]([FM.n_step(t)])[0])  # noqa: E731  P0 written apart
    R = {i: [f0(r) for r in v] for i, v in refs.items()}
    for k, n in enumerate(OWN):
        preds = {str(i): _cap(n, i) for i in ids}
        _dump(data / f"results/{n}.preds.json", preds)
        if k < 4:
            cid = float(E4.Cider(R).per_image({i: f0(c) for i, c in preds.items()}).mean())
            _dump(data / f"results/{n}.json", {"results": [{"segmenter": "rdrsegmenter",
                                                            "scores_scaled_x100": {"CIDEr": cid}}]})
    for n, f in BASE.items():
        verb = "nằm" if "res" in n else "chạy"
        _dump(base / f, [{"image_id": i, "caption": f"{MARK} con_chó {verb} trên bãi_cỏ"} for i in ids])
    globals()["BASE_BLOBS"] = {n: b2.git_blob((base / f).read_bytes()) for n, f in BASE.items()}
    uid = [f"{100 + i:012d}.jpg" for i in ids]
    g1 = fl / GROUPS["G1"]["refs"]
    g1.parent.mkdir(parents=True)
    g1.write_text("".join(f"{u}\t{_ref(i, j)}\n" for i, u in zip(ids, uid) for j in range(2)), encoding="utf-8")
    for x, f in (("a", lambda i: _cap("fuse2_s42-short", i)), ("b", lambda i: _cap("zeroshot-short", i)),
                 ("c", lambda i: f"{MARK} a dog on the grass")):
        p = fl / GROUPS["G1"]["files"][f"X4{x}"]
        p.parent.mkdir(parents=True)
        p.write_text("".join(f"{u}\t{f(i)}\n" for i, u in zip(ids, uid)), encoding="utf-8")
    vid = [f"{200 + i:012d}.jpg" for i in ids]
    _dump(fl / GROUPS["G3"]["refs"], {"images": [{"id": v} for v in vid], "annotations": [
        {"image_id": v, "id": 10 * i + j, "caption": _ref(i + 1, j)} for i, v in zip(ids, vid) for j in range(2)]})
    for n, f in (("X3_original", lambda i: _ref(i + 1, 0)[:-1]), ("X3_detect", lambda i: f"{MARK} {VOC[(i + 4) % 6]} gần đó")):
        _dump(fl / GROUPS["G3"]["files"][n], [{"image_id": v, "caption": f(i)} for i, v in zip(ids, vid)])
    _dump(fl / GROUPS["G5"]["files"]["X1"], [{"Caption pred": f"{MARK} chó", "Caption": f"{MARK} chó"}])
    _dump(b2d / "scores.json", {"rows": {"K1": {"CIDEr_P0": 1.0, "CIDEr_PYVI": 2.0}}})
    # provenance pins of the synthetic FL files (the real ones are b2.A_SYSTEMS, MANIFEST.tsv and CC-354 3(d))
    globals()["FETCH_BLOBS"] = {rel: b2.git_blob((fl / rel).read_bytes()) for g in GROUPS.values()
                                for rel in g["files"].values() if rel.startswith("fetched/") and (fl / rel).is_file()}
    globals()["MANIFEST_SHA"] = {}
    globals()["REF_SHA"] = {"G1": sha(g1), "G3": sha(fl / GROUPS["G3"]["refs"])}


_W: dict = {}


def world() -> dict:
    """The registered chain F -> H once on the synthetic files, with every refusal tried on a copy of the work dir."""
    if "err" in _W:
        raise _W["err"]
    if "root" not in _W:
        import tempfile
        _W.update(root=Path(tempfile.mkdtemp(prefix="b_fecert_selftest_")), refused={}, out=io.StringIO())
        try:
            with contextlib.redirect_stdout(_W["out"]):
                _chain(_W["root"], _W["refused"])
        except BaseException as e:  # a stage that stops here stops every check that reads the chain
            _W["err"] = e
            raise
    return _W


def _chain(root: Path, refused: dict) -> None:
    data, fl, base, b2d, W, lab = (root / x for x in ("data", "fl", "base", "b2", "work", "labels"))
    logf, printed = root / "LOG.md", root / "PRINTED.json"
    _build(data, fl, base, b2d)
    set_data(data)
    logf.write_text("2026-11-13T00:00:00Z OPS-T0: chain start\n", encoding="utf-8")

    def ns(stage, **kw):
        d = dict(stage=stage, work=str(W), log=str(logf), prev=None, nc=None, pins=str(root / "pins"), fl=str(fl),
                 baselines=str(base), b2_score=str(b2d), printed=None, labels=None, pyvi_wheel=None, uts_wheel=None,
                 k_print=False)
        d.update(kw)
        return argparse.Namespace(**d)

    def pin(*files):
        with open(logf, "a", encoding="utf-8") as fh:
            fh.write("2026-11-13T01:00:00Z OPS-T1-pin: " + " ".join(f"{f.name} {sha(f)}" for f in files) + "\n")

    def alt_log(drop: str, extra: str = "") -> Path:
        p = root / f"log_{len(list(root.glob('log_*')))}.md"
        keep = [ln for ln in logf.read_text(encoding="utf-8").splitlines(True) if drop not in ln]
        p.write_text("".join(keep) + extra, encoding="utf-8")
        return p

    def attempt(name, stage, log=None, setup=None, **kw):
        cp = root / f"try_{name}"
        shutil.copytree(W, cp)
        if setup:
            setup(cp)
        try:
            run(ns(stage, work=str(cp), log=str(log or logf), **kw))
            refused[name] = False
        except SystemExit as e:
            refused[name] = "REFUSED" in str(e)
        except Exception:
            refused[name] = False

    run(ns("F"))
    pf = sha(W / "FAMILY.json")
    attempt("C_no_log_line", "C", prev=pf)
    pin(W / "FAMILY.json")
    attempt("C_bad_prev", "C", prev=pf, setup=lambda cp: (cp / "FAMILY.json").write_text("{}"))  # logged sha, other bytes
    real_now = globals()["now"]
    globals()["now"] = lambda: "2026-11-17T00:00:00Z"
    try:
        attempt("C_k_time", "C", prev=pf)
    finally:
        globals()["now"] = real_now
    run(ns("C", prev=pf))
    pin(W / "CENSUS.json")
    run(ns("G", prev=sha(W / "CENSUS.json")))
    pin(W / "GATE2.json")
    run(ns("1", prev=sha(W / "GATE2.json")))
    dv, nc = sha(W / "DEV.json"), sha(W / "NC.json")
    run(ns("pin", prev=dv, nc=nc))
    attempt("2a_no_pin", "2a", prev=dv, log=alt_log("NC.json", f"2026-11-13T01:00:00Z OPS-T2-pin: DEV.json {dv}\n"
                                                    f"2026-11-13T01:00:00Z OPS-T3-pin: NC.json {nc}\n"))  # not one line
    pin(W / "DEV.json", W / "NC.json", W / "PAIR_CANDIDATES.json")
    attempt("2a_no_gate2_line", "2a", prev=dv, log=alt_log("GATE2.json"))
    attempt("2a_result_exists", "2a", prev=dv, setup=lambda cp: (cp / "RESULT_old.json").write_text("{}"))
    run(ns("2a", prev=dv))
    attempt("2b_no_V_line", "2b", prev=sha(W / "V.json"))
    pin(W / "V.json")
    attempt("2b_dev_altered", "2b", prev=sha(W / "V.json"),  # D8: a work file changed after its pin line
            setup=lambda cp: (cp / "DEV.json").write_text((W / "DEV.json").read_text(encoding="utf-8") + " ", encoding="utf-8"))
    run(ns("2b", prev=sha(W / "V.json")))
    pin(W / "RESULT.json")
    _dump(printed, _printed_fixture(base))  # D1: synthetic numbers in the pinned 2a962a2b layout
    globals()["PRINTED_SHA"] = sha(printed)
    attempt("3_no_printed", "3", prev=sha(W / "RESULT.json"))
    pin(printed)
    run(ns("3", prev=sha(W / "RESULT.json"), printed=str(printed)))
    pin(W / "FEID.json")
    # D5: the stage-1 PAIR_CANDIDATES.json -> build_pairs.build -> synthetic labels -> stage H
    import build_pairs as BP
    with contextlib.redirect_stdout(io.StringIO()):
        BP.build(lab, W / "PAIR_CANDIDATES.json", data / "results", data / "datasets/ktvic/test_data.json",
                 sha(W / "PAIR_CANDIDATES.json"), salt="5a17" * 8)
    items = jload(lab / "key.json")["items"]
    first = min((q for q, v in items.items() if v["part"] == "main"), default=None)
    for r in ("PI", "R2"):
        (lab / f"labels_{r}.jsonl").write_text("".join(
            json.dumps({"qid": q, "label": "B" if r == "R2" and q == first else "A"}) + "\n"
            for q, v in sorted(items.items()) if v["part"] != "practice"), encoding="utf-8")
    attempt("H_no_closing", "H", prev=sha(W / "FEID.json"), labels=str(lab))
    pin(lab / "key.json", lab / "labels_PI.jsonl", lab / "labels_R2.jsonl")
    run(ns("H", prev=sha(W / "FEID.json"), labels=str(lab)))


def _printed_fixture(base: Path) -> dict:
    """PRINTED.json layout of the pin 2a962a2b (values.{KTVIC,K2}[] {system, metric_as_printed, value_as_printed}), with
    the registered system and metric strings and synthetic numbers (the baselines' from the stub r*)."""
    refs = PT.load_refs(REFS)
    rows = {"KTVIC": [], "K2": []}
    for (src, sysname), f in PRINTED_SYSTEMS.items():
        if f:
            h = load_base(base, f)
            s = _rstar_stub(refs, {i: h[i] for i in sorted(refs)})
            vals = {"BLEU-1": f"{s['BLEU-1']:.1f}", "BLEU-4": f"{s['BLEU-4']:.1f}", "METEOR": "27.5",
                    "ROUGE": f"{s['ROUGE-L']:.1f}", "CIDEr": f"{s['CIDEr-D']:.1f}"}
        elif src == "KTVIC":
            vals = {"BLEU-1": "74.7", "BLEU-4": "40.6", "METEOR": "36.6", "ROUGE": "59.7", "CIDEr": "136.0"}
        else:
            vals = {"BLEU-1": "68.94", "BLEU-4": "34.81", "CIDEr": "98.50", "METEOR": "53.73", "ROUGE-L": "60.56"}
        rows[src] += [{"system": sysname, "metric_as_printed": m, "value_as_printed": v, "value": float(v),
                       "decimals": len(v.split(".")[1])} for m, v in vals.items()]
    return {"schema": "vsps.b_fecert.printed.v1", "sources": [], "values": rows}


@check
def family_enumeration():
    assert (len(FM.F_DEV), len(FM.F_HELD), len(FM.F), len(FM.FPLUS)) == (54, 18, 72, 271)
    assert FM.F0 in FM.F_DEV and all(len(m) == 4 and m[0] != "chr" for m in FM.F)
    assert {m[0] for m in FM.F_DEV} == {"syl", "rdr", "pyvi"} and {m[0] for m in FM.F_HELD} == {"uts"}
    assert Counter(e[0] for e in FM.FPLUS) == {"matched": 90, "out": 90, "ref": 90, "rstar": 1}
    assert len(FM.WS) == 25 and FM.FINAL == frozenset(".!?…;:,")  # B_KAPPA §2.2


@check
def tone_domain():
    nfc = lambda s: unicodedata.normalize("NFC", s)  # noqa: E731
    for s, lv, want in (("hòa", "tm", "hoà"), ("hoà", "tf", "hòa"), ("HÒA", "tm", "HOÀ"), ("khỏe", "tm", "khoẻ"),
                        ("thủy", "tm", "thuỷ"), ("ủy", "tm", "uỷ"), ("hòa bình.", "tm", "hoà bình."), ("hòa", "tw", "hòa"),
                        ("hoàn", "tm", "hoàn"), ("hòan", "tf", "hòan"), ("quý", "tf", "quý"), ("qúy", "tm", "qúy"),
                        ("thuế", "tf", "thuế"), ("ngoài", "tm", "ngoài"), ("hoa", "tf", "hoa"), ("hoàbình", "tf", "hoàbình")):
        assert FM.tone(nfc(s), lv) == nfc(want), (s, lv)
    assert FM.tone(unicodedata.normalize("NFD", "hòa"), "tm") == nfc("hoà")


@check
def toy_tokens():
    tk, nfc = FM.Tok(STUB), (lambda s: unicodedata.normalize("NFC", s))
    assert FM.n_step(" Hà_Nội\u00a0 đẹp\t") == "Hà Nội đẹp"
    t = "Hà Nội đẹp."
    assert tk.tokens(t, ("rdr", "tw", "pk", "cf")) == ["hà_nội", "đẹp."]
    assert tk.tokens(t, ("rdr", "tw", "pk", "ck")) == ["Hà_Nội", "đẹp."]
    assert tk.tokens(t, ("rdr", "tw", "pa", "cf")) == ["hà_nội", "đẹp"]
    assert tk.tokens(t, ("rdr", "tw", "pf", "cf")) == ["hà_nội", "đẹp"]
    assert tk.tokens("xe, máy ...", ("syl", "tw", "pa", "ck")) == ["xe", "máy"]
    assert tk.tokens("xe, máy ...", ("syl", "tw", "pf", "ck")) == ["xe,", "máy"]
    assert tk.tokens("hòa bình", ("syl", "tm", "pk", "ck")) == [nfc("hoà"), "bình"]
    assert tk.tokens("ab c", ("chr", "tw", "pk", "ck")) == ["a", "b", "c"]
    m = ("syl", "tw", "pa", "cf")
    assert tk.side("Con CHÓ.", "out", m, True) == "Con CHÓ." and tk.side("Con CHÓ.", "out", m, False) == "con chó"


@check
def f1_rule():
    refs = [f"con chó số {k}" for k in range(200)]
    assert FM.f1("rdr", refs, STUB) == {"unit": "rdr", "strings": 200, "failed": 0, "aligned": True,
                                         "whitespace_fallback": False, "dropped": False}
    bad = lambda n: (lambda ts: [[] if k < n else s for k, s in enumerate(STUB["rdr"](ts))])  # noqa: E731
    assert not FM.f1("rdr", refs, {"rdr": bad(1)})["dropped"]  # 0.5% failed: kept
    assert FM.f1("rdr", refs, {"rdr": bad(2)})["dropped"]  # 1%: dropped
    assert FM.f1("syl", refs, STUB)["whitespace_fallback"] and FM.f1("syl", refs, STUB)["dropped"]

    def crash(ts):
        raise OSError("unit down")
    try:  # D6: a unit that raises is not a string failure (stage F makes it a FAULT)
        FM.f1("uts", refs, {"uts": crash})
    except OSError:
        pass
    else:
        raise AssertionError("a raising unit must not come back as a K-unit drop (CC-361 D6)")
    assert [x["addition"] for x in FM.f3("rdr", STUB)] == [False] * 5 + [True] * 4  # NB7


@check
def matched_scoring():
    refs = {"1": ["Con CHÓ chạy.", "Một Con CHÓ"], "2": ["Con Mèo nằm.", "Con Mèo"]}
    texts = {"x": {"1": "con chó chạy.", "2": "con mèo nằm."}}
    got = scorer(FM.Tok(STUB), refs, ["1", "2"], texts)(("syl", "tw", "pk", "cf"))["x"]["cider"]
    nfc = lambda s: unicodedata.normalize("NFC", s)  # noqa: E731
    R = {i: [nfc(" ".join(w.casefold() for w in r.split())) for r in refs[i]] for i in refs}
    assert np.allclose(got, E4.Cider(R).per_image({i: nfc(h) for i, h in texts["x"].items()}))


@check
def bootstrap_ref():
    d = np.array([3.0, -1.0, 2.0, 0.5, -2.0, 4.0, 1.0])
    ref = d[np.random.default_rng(SEED).integers(0, len(d), (B, len(d)))].mean(1)
    lo, hi = np.percentile(ref, [2.5, 97.5])
    s = stats(d, boot_W(len(d)))
    assert abs(s[0] - d.mean()) < 1e-12 and abs(s[1] - lo) < 1e-9 and abs(s[2] - hi) < 1e-9
    assert abs(s[3] - ref.std(ddof=1)) < 1e-9 and np.all(boot_W(len(d)).sum(1) == len(d))


def _stub_per(arrs: dict):
    def per(m):
        a, ka = arrs[m]
        mk = lambda x, k: {"cider": x, "rouge": x, "bleu": np.ones((len(x), 10)), "key": k}  # noqa: E731
        return {"_refs": "r", "a": mk(a, ka), "b": mk(np.zeros_like(a), "kb")}
    return per


@check
def same_draws():
    d = np.array([3.0, -1.0, 2.0, 0.5, -2.0, 4.0, 1.0])
    m1, m2 = ("syl", "tw", "pk", "cf"), ("syl", "tm", "pk", "cf")
    c = {"id": "t", "a": "a", "b": "b", "classes": {}}
    run_list([str(k) for k in range(7)], [c], [m1, m2], _stub_per({m1: (d, "k1"), m2: (d + 3.0, "k2")}))
    s1, s2 = c["classes"]["k1|kb|r"]["cider"], c["classes"]["k2|kb|r"]["cider"]
    assert abs(s2[1] - s1[1] - 3.0) < 1e-9 and abs(s2[2] - s1[2] - 3.0) < 1e-9


@check
def merge_by_tokens():
    d = np.array([3.0, -1.0, 2.0, 0.5, -2.0, 4.0, 1.0])
    m1, m2, m3 = ("syl", "tw", "pk", "cf"), ("syl", "tm", "pk", "cf"), ("syl", "tf", "pk", "cf")
    c = {"id": "t", "a": "a", "b": "b", "classes": {}}
    run_list([str(k) for k in range(7)], [c], [m1, m2, m3], _stub_per({m1: (d, "k1"), m2: (d.copy(), "k2"), m3: (d + 1, "k1")}))
    got = sorted(sorted(cl["members"]) for cl in c["classes"].values())
    assert got == [sorted([FM.name(m1), FM.name(m3)]), [FM.name(m2)]]


@check
def bleu_counts():
    R = {"1": ["a b c d e", "a b c x"], "2": ["p q r s", "p q t"], "3": ["x y z w v u"]}
    H = {"1": "a b c d", "2": "p q r s t", "3": "x y"}
    S = np.array([bleu_img(R[i], H[i]) for i in sorted(R)], float)
    assert abs(float(bleu_corpus(S.sum(0))) - E4.bleu4(R, H)) < 1e-9
    # BLEU-1 by hand (D12): 4 + 5 + 2 matched of 4 + 5 + 2 hypothesis words; 'closest' reference lengths 4 + 4 + 6 = 14
    assert abs(float(bleu_corpus(S.sum(0), 1)) - 100 * np.exp(1 - 14 / 11)) < 1e-6


def _comp(cid, cls):
    return {"id": cid, "classes": {f"k{j}": {"members": ms, "cider": s} for j, (ms, s) in enumerate(cls)}}


@check
def certificate_cases():
    oth = "syl.tw.pk.cf"
    pos, neg, nul = [2.0, 1.0, 3.0, 0.5], [-2.0, -3.0, -1.0, 0.5], [0.2, -0.5, 0.9, 0.35]
    cs = [_comp("c1", [([F0N], pos), ([oth], pos)]), _comp("c2", [([F0N], pos), ([oth], nul)]),
          _comp("c3", [([F0N], pos), ([oth], neg)]), _comp("c4", [([F0N], nul), ([oth], nul)]),
          _comp("c5", [([F0N], nul), ([oth], pos)])]
    G = {F0N, oth}
    v = [certify(c, G) for c in cs]
    assert [x["verdict"] for x in v] == ["CERTIFIED (a > b)", "FRAGILE", "REVERSED", "NULL-STABLE", "FRAGILE"]
    assert [x["changed"] for x in v] == [False, True, True, False, False]
    assert v[2]["point_flip"] and not v[0]["point_flip"]
    assert v[1]["breaking"] == {"classes": 1, "levels": {"cf": 1, "pk": 1, "syl": 1, "tw": 1}}
    k = counts(cs, G)
    assert (k["CERTIFIED"], k["FRAGILE"], k["REVERSED"], k["NULL-STABLE"]) == (1, 3, 1, 1)
    assert k["significant_under_f0"] == 3 and k["CHANGED"] == 2 and abs(k["CHANGED_share"] - 2 / 3) < 1e-12
    assert certify(_comp("c6", [([F0N], neg), ([oth], neg)]), G)["verdict"] == "CERTIFIED (b > a)"
    assert certify(cs[0], {"uts.tw.pk.cf"}) is None


@check
def near_margin():
    V, rule = verdict_set([(f"c{k}", 4.0) for k in range(59)] + [("far", 9.0)])
    assert rule.startswith("near-margin") and len(V) == 59 and "far" not in V
    V, rule = verdict_set([(f"c{k}", 4.0) for k in range(58)] + [(f"f{k}", 9.0) for k in range(10)])
    assert rule.startswith("fallback") and len(V) == 68
    assert certify(_comp("z", [([F0N], [8.0, 6.0, 10.0, 2.0])]), {F0N})["z_min"] == 4.0


@check
def cp_points():
    assert abs(cp_upper(0, 59) - 0.0495076) < 2e-6 and abs(cp_upper(0, 58) - 0.0503393) < 2e-6  # 1 - 0.05^(1/n)
    assert abs(cp_upper(1, 2) - 0.95 ** 0.5) < 1e-9 and abs(cp_lower(10, 10) - 0.7411344) < 2e-6  # 0.05^(1/10)
    assert cp_lower(0, 10) == 0.0 and cp_upper(5, 5) == 1.0


@check
def p1_labels():
    got = [p1_rule(n, k, e)["label"] for n, k, e in ((59, 0, False), (58, 0, False), (100, 20, False), (100, 3, False),
                                                      (100, 0, True))]
    assert got == ["PASS", "NOT_EVALUABLE", "FAIL", "INCONCLUSIVE", "NOT_EVALUABLE"]


@check
def p2_labels():
    got = [p2_rule(n, k) for n, k in ((9, 9), (10, 3), (10, 2), (30, 3), (31, 3))]
    assert got == ["NOT_EVALUABLE", "SUPPORTED", "NOT SUPPORTED", "SUPPORTED", "NOT SUPPORTED"]


@check
def nc_check():
    syl, rdr = "syl.tw.pk.cf", "rdr.tw.pk.cf"
    pos, nul = [2.0, 1.0, 3.0, 1.0], [0.2, -0.5, 0.9, 0.35]
    mk = lambda k, brk: _comp(f"d{k}", [([syl], pos), ([rdr], nul if brk else pos)])  # noqa: E731
    r = nc_rule([mk(k, k < 10) for k in range(60)], {syl}, {rdr})
    assert (r["V_NC"], r["breaks"], r["status"]) == (60, 10, "sensitive")
    assert nc_rule([mk(k, k < 2) for k in range(60)], {syl}, {rdr})["status"] == "LOW-SENSITIVITY"
    assert nc_rule([mk(k, False) for k in range(58)], {syl}, {rdr})["status"].startswith("NOT_EVALUABLE")


@check
def f_held_empty():
    dev, held = unit_sets({"units_dropped": ["uts"]}, {"uts_moved_to_dev": False})
    assert held == [] and p1_rule(100, 0, not held)["label"] == "NOT_EVALUABLE"
    assert unit_sets({"units_dropped": ["pyvi"]}, {"uts_moved_to_dev": False}) == (["syl", "rdr"], ["uts"])


@check
def census_uts():
    import tempfile
    d = Path(tempfile.mkdtemp(prefix="b_fecert_census_"))
    _dump(d / "a.json", {"results": [{"segmenter": "rdrsegmenter"}, {"segmenter": "whitespace"}]})
    _dump(d / "b.json", {"results": [{"segmenter": "underthesea"}]})
    _dump(d / "b2/scores.json", {"rows": {"K1": {"CIDEr_P0": 1.0, "CIDEr_PYVI": 2.0}}})
    c = census({"a": d / "a.json"}, d / "b2")
    c2 = census({"a": d / "a.json", "b": d / "b.json"}, d / "b2")
    assert not c["uts_moved_to_dev"] and c2["uts_moved_to_dev"] and c2["underthesea_hits"] == ["b"]
    assert unit_sets({"units_dropped": []}, c2) == (["syl", "rdr", "pyvi", "uts"], [])
    assert unit_sets({"units_dropped": []}, c) == (["syl", "rdr", "pyvi"], ["uts"])
    _dump(d / "b2/s2.json", {"rows": {"K9": {"CIDEr_UTS": 1.0}}})
    c3 = census({"a": d / "a.json"}, d / "b2")
    assert c3["uts_moved_to_dev"] and c3["b2_score_sha256"]["b2_external/s2.json"] == sha(d / "b2/s2.json")
    shutil.rmtree(d)


@check
def census_b2dir():
    """D10: --b2-score must be a directory holding at least one *.json; a file, an empty folder or none is a FAULT."""
    import tempfile
    d = Path(tempfile.mkdtemp(prefix="b_fecert_census_"))
    try:
        _dump(d / "a.json", {"results": [{"segmenter": "rdrsegmenter"}]})
        _dump(d / "b2/scores.json", {"rows": {"K1": {"CIDEr_UTS": 1.0}}})
        (d / "empty").mkdir()
        for bad in (d / "b2/scores.json", d / "empty", None):
            try:
                census({"a": d / "a.json"}, bad)
            except Fault:
                continue
            raise AssertionError(f"census accepted --b2-score {bad}")
    finally:
        shutil.rmtree(d)


@check
def gate_rules():
    refs = {str(k): [f"con chó số {k}"] for k in range(100)}
    good = [(str(k), f"một con chó {k}") for k in range(100)]
    assert gate2(good, refs)[0]["admitted"] and gate2(good[:95], refs)[0]["admitted"]
    cases = {"2 coverage": good[:94], "2 unknown": good + [(f"u{k}", "chó") for k in range(6)],
             "3 dup": good + good[:2], "4 empty": good[:98] + [("98", ""), ("99", "")],
             "5 refcopy": [(str(k), f"CON CHÓ SỐ {k}") for k in range(6)] + good[6:],
             "6 diacritic": [(str(k), "a dog") for k in range(100)]}
    for why, rows in cases.items():
        v = gate2(rows, refs)[0]
        assert not v["admitted"] and why in v["reasons"], why
    assert gate2(None, refs)[0]["reasons"] == ["1 parse"]
    files = lambda lo, hi: {"X4a": ({"admitted": True}, {str(k): "c" for k in range(97)}, None),  # noqa: E731
                            "X4b": ({"admitted": True}, {str(k): "c" for k in range(lo, hi)}, None)}
    c = fl_comps({"G1": {"refs": refs, "files": files(3, 100)}})
    assert len(c) == 1 and c[0]["n"] == 94 and not c[0]["formed"]
    assert fl_comps({"G1": {"refs": refs, "files": files(2, 100)}})[0]["formed"]


@check
def fe_id_tolerance():
    assert reproduces({"CIDEr-D": 21.84}, {"CIDEr-D": "21.8"}) and not reproduces({"CIDEr-D": 21.86}, {"CIDEr-D": "21.8"})
    assert reproduces({"BLEU-4": 15.4}, {"BLEU-4": "15"}) and not reproduces({"BLEU-4": None}, {"BLEU-4": "15"})


@check
def identify_labels():
    sc = {"x": {"CIDEr-D": 21.80}, "y": {"CIDEr-D": 21.80}, "z": {"CIDEr-D": 25.0}, "w": {"CIDEr-D": 21.83}}
    keys = {"x": "k1", "y": "k1", "z": "k2", "w": "k3"}
    assert identify({"CIDEr-D": "21.8"}, sc, keys)["label"] == "AMBIGUOUS"
    r = identify({"CIDEr-D": "25.0"}, sc, keys)
    assert r["label"] == "IDENTIFIED" and r["reproducing"] == [["z"]] and abs(r["margin"] - 3.17) < 1e-9
    r = identify({"CIDEr-D": "30.0"}, sc, keys)
    assert r["label"] == "OUTSIDE" and abs(r["nearest_distance"] - 5.0) < 1e-9
    # D12: BLEU-1 separates two classes that CIDEr-D, BLEU-4 and ROUGE-L cannot; METEOR binds r* only
    s2 = {"x": {"CIDEr-D": 21.8, "BLEU-4": 15.5, "ROUGE-L": 42.3, "BLEU-1": 53.0},
          "y": {"CIDEr-D": 21.8, "BLEU-4": 15.5, "ROUGE-L": 42.3, "BLEU-1": 49.0},
          "r*": {"CIDEr-D": 21.8, "BLEU-4": 15.5, "ROUGE-L": 42.3, "BLEU-1": 53.0, "METEOR": 20.0}}
    pr = {"CIDEr-D": "21.8", "BLEU-4": "15.5", "ROUGE-L": "42.3", "BLEU-1": "53.0", "METEOR": "27.5"}
    r = identify(pr, s2, {"x": "k1", "y": "k2", "r*": "r*"})
    assert r["label"] == "IDENTIFIED" and r["reproducing"] == [["x"]] and abs(r["margin"]) < 1e-9  # r* equal on the 4


@check
def p4_fault():
    rep = lambda lab, cls: {"label": lab, "reproducing": cls, "margin": None}  # noqa: E731
    good = {f"s{k}": rep("IDENTIFIED", [[f"m{k}", "other"]]) for k in range(12)}
    key = {f"s{k}": f"m{k}" for k in range(12)}
    assert check_plants(good, key)["identification"] == "evaluable"
    assert check_plants({**good, "s11": rep("AMBIGUOUS", [["m11"], ["x"]])}, key)["identification"].startswith("NOT_EVAL")
    try:
        check_plants({**good, "s3": rep("IDENTIFIED", [["wrong"]])}, key)
    except Fault:
        return
    raise AssertionError("a planted wrong recovery must be a FAULT (§6.4)")


@check
def p3_labels():
    pr = {"b1": {"CIDEr-D": "21.8", "BLEU-4": "15.5", "BLEU-1": "50.0", "METEOR": "20.0", "SPICE": "5.0"},
          "b2": {"CIDEr-D": "36.8", "BLEU-4": "19.3", "BLEU-1": "55.0"}}
    rs = {"b1": {"CIDEr-D": 30.0, "BLEU-4": 15.5, "BLEU-1": 50.02, "METEOR": None},
          "b2": {"CIDEr-D": 36.8, "BLEU-4": 19.3, "BLEU-1": 54.97}}
    r = p3_rule(pr, rs, ["METEOR"])
    assert r["label"] == "SUPPORTED" and r["M_new"] == ["BLEU-1"] and r["not_used"]["b1"] == ["METEOR", "SPICE"]
    assert p3_rule(pr, {**rs, "b2": {**rs["b2"], "BLEU-1": 55.2}}, ["METEOR"])["label"] == "NOT SUPPORTED"
    r = p3_rule({"b1": {"CIDEr-D": "21.8", "BLEU-4": "15.5"}}, {"b1": rs["b1"]}, [])
    assert r["label"].startswith("no registered label") and r["M_new"] == []


@check
def pair_strata():
    got = [pair_stratum(*d) for d in ((12, -11, -15), (-13, -12, 12), (11, 11, 11), (12, -9.5, -15), (12, -12, 12))]
    assert got == ["U", "P", "C", None, None]
    assert display("  con chó chạy ... ") == "Con chó chạy" and display("đẹp.") == "Đẹp" and display("3 con.") == "3 con"
    assert tok_diff("Con chó chạy", "con chó nằm") == 2 and tok_diff("con chó", "Con Chó") == 0


@check
def kappa_hand():
    x, y = ["a", "a", "b", "tie"], ["a", "b", "b", "tie"]
    assert abs(kappa(x, y) - 0.4375 / 0.6875) < 1e-12 and abs(ac1(x, y) - 0.421875 / 0.671875) < 1e-12
    assert holm({"x": 0.02, "y": 0.04}) == {"x": True, "y": True} and holm({"x": 0.03, "y": 0.04}) == {"x": False, "y": False}


def _hkey(rows):
    return {q: {"image": q, "part": "main", "stratum": s, "a": "fa", "b": "fb", "file_left": "fa", "file_right": "fb",
                "d_syl": -dw, "d_word": dw, "d_pk": dw, "repeat_of": None} for q, s, dw in rows}


@check
def h_labels():
    key = _hkey([(f"p{k}", "P", 12.0) for k in range(47)] + [(f"u{k}", "U", 12.0 if k % 2 else -12.0) for k in range(100)])
    lab = {q: "A" if q.startswith("u") or int(q[1:]) < 5 else "B" for q in key}  # P: 5 of 47 with m_word; U: 50 of 100
    r = human(key, {"PI": lab, "R2": lab}, {"P": 50, "U": 120, "C": 0})
    assert r["gate"] == "labels" and r["H-P"] == "NOT SUPPORTED" and r["H-U"] == "EQUIVALENT within ±0.10"
    assert human(key, {"PI": lab}, {"P": 50, "U": 120, "C": 0})["H-P"] == "single rater"
    key3 = _hkey([(f"p{k}", "P", 12.0) for k in range(10)] + [(f"u{k}", "U", 12.0) for k in range(100)])
    lab3 = {q: "A" if q.startswith("u") or int(q[1:]) < 5 else "B" for q in key3}
    r = human(key3, {"PI": lab3, "R2": lab3}, {"P": 50, "U": 99, "C": 0})
    assert r["H-P"] == "UNDERPOWERED" and r["H-U"] == "NOT_EVALUABLE"
    assert human(key3, {"PI": lab3, "R2": lab3}, {"P": 50, "U": 120, "C": 0})["H-U"] == "WORD AGREES MORE"


@check
def kappa_gate():
    """D11: the kappa gate and the inter-rater rows exclude cannot AND missing answers, by one definition."""
    key = _hkey([(f"p{k}", "P", 12.0 if k % 2 else -12.0) for k in range(10)])
    r2 = {q: "A" if int(q[1:]) % 3 else "B" for q in key}
    pi = {q: v for q, v in r2.items() if q not in ("p0", "p1")}  # PI missed two screens; R2 answered all
    r = human(key, {"PI": pi, "R2": r2}, {"P": 50, "U": 0, "C": 0})
    assert r["raters"] == ["PI", "R2"] and r["gate"] == "labels"
    assert r["inter_rater"]["n"] == 8 and abs(r["inter_rater"]["kappa"] - 1.0) < 1e-12


@check
def g_repro():
    """Coded reading (a) (CC-361 D13 open; PI Q2 default): any mismatch among the scored files is a FAULT, a file of the
    seen set S or not."""
    assert all(r["ok"] for r in grepro({"a": 149.795, "b": 10.0}, {"a": 149.79, "b": 10.0}))
    for n in ("a", S_FILES[0]):  # 'a' is not in S
        try:
            grepro({n: 149.84}, {n: 149.79})
        except Fault:
            continue
        raise AssertionError(f"a G-repro mismatch of 0.05 on {n} must be a FAULT")


@check
def env_pins():
    good = _env_stub(None)
    env_check(good)
    for bad in ({"pyvi": "0.1.2", "pyvi_wheel": {"name": "pyvi-0.1.2-py3-none-any.whl"}}, {"jar_sha256": "0" * 64},
                {"underthesea_wheel": {"name": "underthesea-6.9.0-py3-none-any.whl"}},
                {"underthesea": None, "underthesea_wheel": None},  # D6
                {"underthesea": "9.4.0", "underthesea_wheel": {"name": "underthesea-9.4.0-py3-none-any.whl",
                                                              "sha256": UTS_WHEEL_SHA}},
                {"underthesea_wheel": {"name": f"underthesea-{UTS_VERSION}-py3-none-any.whl", "sha256": "0" * 64}},
                {"underthesea_signature": None},
                {"rstar_import": False}, {"pycocoevalcap": "1.3"}, {"pycocoevalcap": None},  # D7
                {"rescap_metrics_sha256": "0" * 64}, {"java": None}, {"java": "17.0.1"}):
        try:
            env_check({**good, **bad})
        except Fault:
            continue
        raise AssertionError(f"env_check accepted {sorted(bad)}")


@check
def pipeline():
    w = world()["root"] / "work"
    for f in ("FAMILY.json", "SYSTEMS.tsv", "CENSUS.json", "GATE2.json", "DEV.json", "NC.json", "PAIR_CANDIDATES.json",
              "V.json", "RESULT.json", "PLANT_KEY.json", "PLANT_PRINTED.json", "FEID.json", "HUMAN.json"):
        assert (w / f).is_file(), f
    g = jload(w / "GATE2.json")
    assert g["formed"] == 2 and g["files"]["G1/X4c"]["reasons"] == ["6 diacritic"] and not g["files"]["G5/X1"]["admitted"]
    assert jload(w / "CENSUS.json")["D_size"] == 7
    r = jload(w / "RESULT.json")
    assert r["P1"]["label"] == "NOT_EVALUABLE" and r["P2"]["label"] == "NOT_EVALUABLE"
    p3 = jload(w / "FEID.json")["P3"]
    assert p3["label"] == "SUPPORTED" and p3["M_new"] == ["BLEU-1", "ROUGE-L"]
    assert jload(w / "FAMILY.json")["no_committed_score"] == ["p1_s42-detailed", "zeroshot-detailed"]
    assert all(os.stat(p).st_mode & 0o777 == 0o444 for p in (world()["root"] / "pins").iterdir())


@check
def stage_order():
    rf = world()["refused"]
    assert rf["C_bad_prev"] and rf["C_no_log_line"]


@check
def gate_2a_pin():
    assert world()["refused"]["2a_no_pin"]


@check
def gate_2a_gate2():
    assert world()["refused"]["2a_no_gate2_line"]


@check
def gate_2a_result():
    assert world()["refused"]["2a_result_exists"]


@check
def gate_2b_V():
    assert world()["refused"]["2b_no_V_line"]


@check
def k_time():
    assert world()["refused"]["C_k_time"]


@check
def k_print():
    assert world()["refused"]["3_no_printed"]


@check
def h_closing():
    assert world()["refused"]["H_no_closing"]


@check
def dev_no_heldout():
    dv = jload(world()["root"] / "work/DEV.json")
    assert set(dv["members"]) == {FM.name(m) for m in FM.F_DEV}
    assert all(set(cl["members"]) <= set(dv["members"]) for c in dv["comparisons"] for cl in c["classes"].values())


@check
def image_route():
    world()
    assert image_files() == {str(i): f"{i:011d}.{e}" for i, e in zip(range(1, 7), ["jpg", "png", "jpeg", "jpg", "jpg", "jpg"])}
    assert not FN_RE.fullmatch("00000000001.gif") and not FN_RE.fullmatch("1.jpg")


@check
def pairs_integration():
    """D3/D5: stage 1's PAIR_CANDIDATES.json -> build_pairs.build -> synthetic labels -> stage H, on the chain."""
    w = world()["root"]
    pc = jload(w / "work/PAIR_CANDIDATES.json")
    assert pc["epsilon"] == EPS and set(pc["eligible_images"]) == set("PUC")
    assert all(set(c) == set(CAND_FIELDS) for cs in pc["images"].values() for c in cs)
    items = jload(w / "labels/key.json")["items"]
    main = [q for q, v in items.items() if v["part"] == "main"]
    h = jload(w / "work/HUMAN.json")
    assert main and h["raters"] == ["PI", "R2"]
    assert sum(r["n_dec"] for r in h["strata"].values()) + sum(h["not_decisive"].values()) == len(main)
    assert h["not_decisive"] == {"split": 1} and h["inter_rater"]["n"] == len(main)


@check
def key_contract():
    """D4/D15 on the 400-image fixture of build_pairs.py: main = part 'main' (practice never), repeats = part 'repeat',
    sides from file_left/file_right, salted qids, and a FAULT on a key outside the contract."""
    import tempfile
    import build_pairs as BP
    with tempfile.TemporaryDirectory() as td:
        fx = Path(td)
        BP._fixture(fx)
        args = (fx / "cand.json", fx / "preds", fx / "ds" / "test_data.json", sha(fx / "cand.json"))
        with contextlib.redirect_stdout(io.StringIO()):
            BP.build(fx / "o1", *args, salt="5a17" * 8)
            BP.build(fx / "o2", *args)
            BP.build(fx / "o3", *args)
        key = jload(fx / "o1/key.json")
        k2, k3 = (jload(fx / f"{o}/key.json") for o in ("o2", "o3"))
        elig = jload(fx / "cand.json")
    items = key_items(key)
    assert key["salt"] == "5a17" * 8 and all(q == BP.qid(key["salt"], v["part"], v["image"], v["a"], v["b"])
                                              for q, v in items.items())
    assert k2["salt"] != k3["salt"] and set(k2["items"]).isdisjoint(k3["items"])  # a fresh secret salt per build
    parts = Counter(v["part"] for v in items.values())
    assert parts["repeat"] == 30 and parts["practice"] == 8 and parts["main"] > 0
    # both raters always pick the screen side that shows caption a: correct side mapping gives "a" on every pair, a
    # swapped mapping gives "b" on every pair, so the word-agreement count tells the two apart whatever the side balance
    labs = {r: {q: "A" if v["file_left"] == v["a"] else "B" for q, v in items.items() if v["part"] != "practice"}
            for r in ("PI", "R2")}
    r = human(items, labs, {s: sum(any(c["stratum"] == s for c in cs) for cs in elig["images"].values()) for s in "PUC"})
    assert r["raters"] == ["PI", "R2"] and sum(x["n_dec"] for x in r["strata"].values()) == parts["main"]
    pos = sum(v["d_word"] > 0 for v in items.values() if v["part"] == "main")
    assert pos != parts["main"] - pos  # so that a swap (count = main - pos) cannot pass
    assert sum(x["k_word"] for x in r["strata"].values()) == pos
    assert r["within_rater"]["PI"]["n"] == 30 and r["within_rater"]["PI"]["raw"] == 1.0  # side swap undone
    bad = {"salt": "x", "items": {q: {**v, "left": v["file_left"]} for q, v in items.items()}}
    try:
        key_items(bad)
    except Fault:
        return
    raise AssertionError("a key.json with a field outside the contract must be a FAULT")


@check
def no_text():
    w = world()
    assert MARK in (w["root"] / "data/datasets/ktvic/test_data.json").read_text(encoding="utf-8")
    outs = [p for d in ("work", "pins") for p in (w["root"] / d).rglob("*") if p.is_file()]
    outs += [p for d in w["root"].glob("try_*") for p in d.rglob("*") if p.is_file()]
    assert outs and not any(MARK in p.read_text(encoding="utf-8") for p in outs)
    assert MARK not in w["out"].getvalue()


@check
def k_coco_import():
    """D7: an ImportError of rescap or pycocoevalcap is a FAULT, not a K-coco drop."""
    global RSTAR
    keep = RSTAR

    def gone(refs, hyps):
        raise ImportError("pycocoevalcap")
    RSTAR = gone
    try:
        k_coco()
    except Fault:
        return
    finally:
        RSTAR = keep
    raise AssertionError("an r* ImportError must be a FAULT (CC-361 D7)")


@check
def printed_adapter():
    """D1: the pinned layout read as is; registered maps; decimals as printed; unmapped system or metric = FAULT."""
    import tempfile
    world()
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "PRINTED.json"
        fx = _printed_fixture(world()["root"] / "base")
        _dump(p, fx)
        keep = globals()["PRINTED_SHA"]
        globals()["PRINTED_SHA"] = sha(p)
        try:
            es = printed_entries(p)
            assert [(e["source"], e["file"]) for e in es] == [
                ("KTVIC", "ktvic_resnetlstm"), ("KTVIC", "ktvic_vittrans"), ("KTVIC", None), ("K2", None), ("K2", None),
                ("K2", None)]
            assert set(es[2]["metrics"]) == {"BLEU-1", "BLEU-4", "METEOR", "ROUGE-L", "CIDEr-D"}
            assert es[3]["metrics"]["CIDEr-D"] == "98.50" and tol(es[3]["metrics"]["CIDEr-D"]) < 0.0051
            for change in ({"system": "4) New / Model"}, {"metric_as_printed": "SPICE"}):
                bad = json.loads(json.dumps(fx))
                bad["values"]["KTVIC"][0].update(change)
                _dump(p, bad)
                globals()["PRINTED_SHA"] = sha(p)
                try:
                    printed_entries(p)
                except Fault:
                    continue
                raise AssertionError(f"PRINTED.json with {change} must be a FAULT")
            _dump(p, fx)
            globals()["PRINTED_SHA"] = "0" * 64
            try:
                printed_entries(p)
            except Fault:
                return
            raise AssertionError("a PRINTED.json off its pin must be a FAULT")
        finally:
            globals()["PRINTED_SHA"] = keep


@check
def inputs_logged():
    """D8: a work file changed after its LOG line is refused in every stage; test_data.json is re-checked against
    FAMILY.json; SYSTEMS.tsv is bound by CENSUS.json."""
    import tempfile
    assert world()["refused"]["2b_dev_altered"]
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        _dump(d / "FAMILY.json", {"refs_sha256": "0" * 64})
        log = d / "LOG.md"
        log.write_text(f"2026-11-13T01:00:00Z OPS-T9-pin: FAMILY.json {sha(d / 'FAMILY.json')}\n", encoding="utf-8")
        try:
            inputs(d, log, ("FAMILY.json",))
        except Fault:
            pass
        else:
            raise AssertionError("test_data.json off its FAMILY.json sha256 must be a FAULT")
        (d / "SYSTEMS.tsv").write_text("name\n", encoding="utf-8")
        _dump(d / "CENSUS.json", {"systems_tsv_sha256": "0" * 64})
        try:
            systems(d)
        except Fault:
            return
        raise AssertionError("SYSTEMS.tsv off its CENSUS.json sha256 must be a FAULT")


@check
def fl_provenance():
    """D9: an FL output off its fetch record, or a reference file off CC-354 3(d), is a FAULT; GATE2.json records the
    reference shas and 2a/2b/3 re-check them."""
    w = world()["root"]
    g = jload(w / "work/GATE2.json")
    assert g["refs_sha256"]["G1"] == REF_SHA["G1"] and g["refs_sha256"]["G5"] is None
    rel = GROUPS["G1"]["files"]["X4a"]
    keep = dict(FETCH_BLOBS)
    try:
        FETCH_BLOBS[rel] = "0" * 40
        try:
            provenance(rel, w / "fl" / rel)
        except Fault:
            pass
        else:
            raise AssertionError("an FL output off its fetch blob must be a FAULT")
    finally:
        FETCH_BLOBS.clear()
        FETCH_BLOBS.update(keep)
    keep = dict(REF_SHA)
    try:
        REF_SHA["G1"] = "0" * 64
        try:
            group_refs("G1", w / "fl")
        except Fault:
            pass
        else:
            raise AssertionError("a reference file off CC-354 3(d) must be a FAULT")
    finally:
        REF_SHA.update(keep)
    fin = fl_inputs(w / "fl", w / "base")
    gate_files(fin, g)
    try:
        gate_files(fin, {**g, "refs_sha256": {**g["refs_sha256"], "G3": "0" * 64}})
    except Fault:
        return
    raise AssertionError("a reference file differing from GATE2.json must be a FAULT")


def selftest() -> int:
    global SEG, RSTAR, env_record, now
    SEG, RSTAR, env_record = STUB, _rstar_stub, _env_stub
    now = lambda: "2026-11-13T02:00:00Z"  # noqa: E731  a fixed clock inside K-time and after K-print is not reached
    EXPECT.update(systems=6, families=3, scored=4)
    S_FILES[:] = [n for n in OWN if n.endswith("-short")]
    res = {}
    for fn in CHECKS:
        try:
            fn()
            res[fn.__name__] = "ok"
        except (AssertionError, Fault, SystemExit):
            res[fn.__name__] = "FAIL"
        except Exception as e:  # noqa: BLE001  any other exception is a crash, never a kill
            res[fn.__name__] = f"CRASH ({type(e).__name__})"
    for n, r in res.items():
        print(f"SELFTEST {r.split()[0]} {n}{r[5:] if r.startswith('CRASH') else ''}")
    if "root" in _W:
        shutil.rmtree(_W["root"])
    c = Counter(r.split()[0] for r in res.values())
    print(f"selftest: {c['ok']} ok, {c['FAIL']} FAIL, {c['CRASH']} CRASH of {len(res)} checks")
    return 1 if c["FAIL"] else 2 if c["CRASH"] else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("stage", choices=["selftest", "F", "C", "G", "1", "pin", "2a", "2b", "3", "H"])
    for o in ("--work", "--log", "--prev", "--nc", "--pins", "--fl", "--baselines", "--b2-score", "--printed",
              "--labels", "--pyvi-wheel", "--uts-wheel"):
        ap.add_argument(o)
    ap.add_argument("--k-print", action="store_true", help="PRINTED.json not logged by the K-print deadline (§10)")
    a = ap.parse_args()
    if a.stage == "selftest":
        return selftest()
    if a.stage not in ("F", "pin") and not a.log:
        a.log = str(LOG)
    try:
        run(a)
    except Fault as e:
        print(f"FAULT: {e}")
        return 3
    except Exception as e:  # noqa: BLE001  the type only, so no caption text can echo (CC-361 NB4)
        print(f"ERROR: {type(e).__name__}")
        return 4
    return 0


if __name__ == "__main__":
    sys.exit(main())
