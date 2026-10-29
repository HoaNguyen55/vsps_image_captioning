#!/usr/bin/env python3
"""L1-a (DEV ONLY): how often do open LVLMs make diacritic-only errors when they read Vietnamese text in images, and in
which mark classes? ViTextVQA dev (5,155 QA, 1,676 images), 4 pinned backbones, a real-image arm and a grey-image
(image removed) arm. Rule: manuscript/prereg/2026-10-29_l1a/RULE_DRAFT.md (to be renamed RULE.md and pinned).

    python3 scripts/l1a/l1a.py --selftest                         CPU, synthetic data only
    python3 -P scripts/l1a/l1a.py build --stage DIR               laptop CPU, once: l1a_lists.json (ids, shas, counts)
                                                                  in the repo; DIR (new; outside the repo or under
                                                                  the gitignored data/datasets) gets the
                                                                  1,676 dev images, grey.png, questions.jsonl
    python  scripts/l1a/l1a.py guard --head H --stage DIR         M2 (machine id m4): host, GPU, HEAD, staged set
    python  scripts/l1a/l1a.py lock --path P                      B-1's O_EXCL lock (tmux, no other lock)
    python  scripts/l1a/l1a.py left --used F --marker M           seconds left under the 12 GPU-h cap, 0 = STOP
    python  scripts/l1a/l1a.py snap --model K                     the model's snapshot dir on M2
    python  scripts/l1a/l1a.py fetch --model K --snapshot DIR     download the pinned files (CPU, network)
    python  scripts/l1a/l1a.py decode --model K --arm img|grey --stage DIR --snapshot DIR --out-dir DIR
    python3 scripts/l1a/l1a.py score --preds DIR                  laptop CPU, once, after RULE.md is pinned

No question or answer text is printed or written into the repo by this file. `build` writes questions (never
answers) only into --stage, which must be outside the repo; `score` writes ids, counts and numbers only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import unicodedata
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts"), str(ROOT / "scripts/b1_scaling"), str(ROOT / "scripts/grl"),
                str(ROOT / "scripts/lb"), str(ROOT / "scripts/g2b")]

PDIR = ROOT / "manuscript/prereg/2026-10-29_l1a"
LISTS = PDIR / "l1a_lists.json"
LISTS_SHA256 = "ac5ed047dc013cb642a325b491994d516ff8ee187c26f30fa47c0b62057e0087"  # build output 2026-10-29, RULE 2
RULE, RULE_SHA256 = PDIR / "RULE.md", "724060a5fe1f62dc3b4fca9e4557e442bd67745b6afd7d1282cf3a3f11f6492c"  # CC-165 W3; LOG after the diff read
RAW = ROOT / "data/datasets/vitextvqa_raw"
SRC = {"train": ("ViTextVQA_train.json", "915f569fc9848b424c75cb16133b82730aa0ec47947a46d5a311675484e638b5"),
       "dev": ("ViTextVQA_dev.json", "c6ab6a7babceb5928e393ec4cc7461c68b35f4fb19ec1a39e9366318be876b81"),
       "zip": ("ViTextVQA_images.zip", "39420475263f38892c5abceed5b4886beec707526f9e05a12e2ecd39a0d0e0b3")}  # OPS-1029l
REG = ROOT / "manuscript/prereg/2026-10-19_b_n1_vi_leaderboard.json"  # B-N1 model registry, reused unchanged
REG_SHA256 = "9ff02dc259258de1add426abd02131f2122e3476a81f9a076066ed6d74906134"
LB_DECODER_SHA256 = "e2de18811e2ffeb61ed72cb2399d41123e9a8f6ccd73a5ec35f778dcbe2f5ac4"  # scripts/lb/decode_hf_vlm.py
CHAIR_SHA256 = "e47d249ac7290070f2387d3fa8b22dac77728265ad276f55aa6520f5cbc591a3"  # rescap/chair.py (norm_tone, _TONE)
MODELS = ("qwen25vl_7b", "qwen3vl_8b", "internvl3_8b", "qwen25vl_3b")  # GPU order (RULE §4)
ARMS = ("img", "grey")
N_DEV_QA, N_DEV_IMG = 5155, 1676
MAX_NEW = 48
PROMPT = ("Dựa vào chữ xuất hiện trong ảnh, hãy trả lời câu hỏi sau. Chỉ ghi câu trả lời ngắn gọn, "
          "không giải thích.\nCâu hỏi: {q}")
GREY = (128, 128, 128), (512, 512)  # RGB, size: 512 x 512 = the registry's min_pixels, so no upscale
CAP_S = 12 * 3600
ROLE = "m4"
FILE_RE = re.compile(r"^\d{1,6}\.jpg$")
KILL, STRONG, STRONG_LO = 0.10, 0.20, 0.10  # RULE §6
PRIOR_FLAG = 0.10
B, SEED, NULL_SEED = 2000, 0, 1
SCOPE = ("open LVLMs with Qwen-family LMs (4/4; InternVL3-8B text_config qwen2); InternVL reads one 448x448 tile, "
         "the Qwen models 0.26-1.05 MP; a non-Qwen-LM backbone is required before L1-b (CC-165 W4)")
NULL_FLAG = 0.05  # RULE §6.2: a null diac share at or above this goes to the judge
OUT = ROOT / ".session_backup/2026-10-29/l1a/decide.json"

# ------------------------------------------------------------------------------------------------ orthography
#: NFD combining marks of Vietnamese, classified by code point, never by position (RULE §5.1)
TONES = {"̀": "huyen", "́": "sac", "̃": "nga", "̉": "hoi", "̣": "nang"}
VOWEL = {"̂": "circ", "̆": "breve", "̛": "horn"}
TOK = re.compile(r"(?:[^\W_]|[\u0300-\u036f])+")  # stray combining marks stay inside the syllable


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with Path(p).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def tokens(s: str) -> list[str]:
    """NFC, lowercase, letter/digit runs; punctuation and whitespace separate syllables and are dropped."""
    return TOK.findall(unicodedata.normalize("NFC", s).lower())


def sig(tok: str) -> tuple[str, tuple, str]:
    """(skeleton, vowel marks as (base index, mark), tone). The tone is position-free, so old and new placement
    (hòa / hoà) give one signature. đ does not decompose under NFD and stays a base letter."""
    base, vm, tone = [], [], []
    for ch in unicodedata.normalize("NFD", tok):
        if ch in TONES:
            tone.append(TONES[ch])
        elif ch in VOWEL:
            vm.append((len(base) - 1, VOWEL[ch]))
        elif unicodedata.combining(ch):
            vm.append((len(base) - 1, f"U+{ord(ch):04X}"))
        else:
            base.append(ch)
    return "".join(base), tuple(sorted(vm)), "+".join(sorted(tone)) or "none"


def marked(sigs: list) -> bool:
    return any(v or t != "none" for _, v, t in sigs)


def mark_diffs(g: list, p: list) -> list[tuple]:
    """Per syllable of a skeleton-equal window: (gold sig, pred sig) where marks differ."""
    return [(a, b) for a, b in zip(g, p) if a != b]


def classify(gold: str, pred: str, view: str = "contained") -> dict:
    """RULE §5.2. strict: the whole prediction against the gold. contained: the best window of len(gold) syllables
    in the prediction (a correct window wins; else the skeleton-equal window with the fewest differing syllables,
    first on ties). Classes: correct, diac (skeleton right, marks wrong), base (anything else; empty = base)."""
    G, P = [sig(t) for t in tokens(gold)], [sig(t) for t in tokens(pred)]
    if not G:
        raise ValueError("empty gold")
    n = len(G)
    wins = [P] if view == "strict" else [P[j:j + n] for j in range(len(P) - n + 1)]
    sk = [w for w in wins if len(w) == n and [s[0] for s in w] == [s[0] for s in G]]
    if any(w == G for w in sk):
        return {"cls": "correct", "win": G}
    if sk:
        w = min(sk, key=lambda w: len(mark_diffs(G, w)))
        d = mark_diffs(G, w)
        tone = any(a[2] != b[2] for a, b in d)
        vow = any(a[1] != b[1] for a, b in d)
        return {"cls": "diac", "sub": "both" if tone and vow else "tone" if tone else "vowel", "win": w,
                "diffs": d, "dropped_all": marked(G) and not marked(w)}
    return {"cls": "base", "empty": not P, "win": None}


def units(s: str) -> list[tuple[str, str]]:
    """Character units of an NFC string after norm_tone: (base char, its marks)."""
    from rescap.chair import norm_tone

    out: list[list] = []
    for ch in unicodedata.normalize("NFD", norm_tone(s)):
        if unicodedata.combining(ch) and out:
            out[-1][1] += ch
        else:
            out.append([ch, ""])
    return [(b, "".join(sorted(m))) for b, m in out]


def char_ops(g: list, p: list) -> tuple[int, int]:
    """(base edits, mark substitutions) on one optimal Levenshtein path; ties prefer base edits (conservative)."""
    prev = [(j, j, 0) for j in range(len(p) + 1)]  # (cost, base edits, mark substitutions)
    for i in range(1, len(g) + 1):
        cur = [(i, i, 0)]
        for j in range(1, len(p) + 1):
            a, b = g[i - 1], p[j - 1]
            c = [(prev[j][0] + 1, prev[j][1] + 1, prev[j][2]), (cur[j - 1][0] + 1, cur[j - 1][1] + 1, cur[j - 1][2])]
            d = prev[j - 1]
            if a == b:
                c.append(d)
            elif a[0] == b[0]:
                c.append((d[0] + 1, d[1], d[2] + 1))
            else:
                c.append((d[0] + 1, d[1] + 1, d[2]))
            cur.append(min(c, key=lambda x: (x[0], x[2])))
        prev = cur
    return prev[-1][1], prev[-1][2]


def char_level(gold: str, pred: str) -> dict:
    """RULE §5.3: on the pred window of len(gold) syllables with the fewest character edits (whole pred if shorter)."""
    gt, pt = tokens(gold), tokens(pred)
    n = len(gt)
    wins = [pt[j:j + n] for j in range(max(1, len(pt) - n + 1))]
    g = units(" ".join(gt))
    best = min((char_ops(g, units(" ".join(w))) for w in wins), key=lambda x: (x[0] + x[1], x[1]))
    return {"n": len(g), "base": best[0], "mark": best[1]}


# ------------------------------------------------------------------------------------------------ build (laptop)
def load_src(name: str, raw: Path = RAW) -> dict:
    f, pin = SRC[name]
    p = raw / f
    if sha(p) != pin:
        raise SystemExit(f"{p}: sha256 differs from OPS-1029l")
    return json.loads(p.read_text(encoding="utf-8"))


def noise_floor(answers: list[str]) -> dict:
    """Gold mark-noise counts (RULE §2.4): old / new tone placement on open oa/oe/uy, >1 tone in a syllable, other
    combining marks. Counts only."""
    from rescap.chair import _TONE

    old, new = set(_TONE), set(_TONE.values())
    toks = [t for a in answers for t in tokens(a)]
    end = lambda t, s: t.endswith(tuple(s))
    return {"answers": len(answers), "syllables": len(toks),
            "old_style_open_cluster": sum(end(t, old) for t in toks),
            "new_style_open_cluster": sum(end(t, new) for t in toks),
            "multi_tone_syllables": sum("+" in sig(t)[2] for t in toks),
            "other_combining": sum(any(m.startswith("U+") for _, m in sig(t)[1]) for t in toks),
            "answers_without_marks": sum(not marked([sig(t) for t in tokens(a)]) for a in answers)}


def grey_png(path: Path) -> None:
    from PIL import Image

    Image.new("RGB", GREY[1], GREY[0]).save(path, format="PNG", optimize=False)


def extract(zf: zipfile.ZipFile, files: list[str], dest: Path) -> dict[str, str]:
    """Only the named members st_images/<file>, read one by one into an empty dir; no extractall."""
    out = {}
    for f in files:
        if not FILE_RE.match(f):
            raise SystemExit(f"refused member name {f!r}")
        data = zf.read(f"st_images/{f}")
        (dest / f).write_bytes(data)
        out[f] = hashlib.sha256(data).hexdigest()
    return out


def build(stage: Path, raw: Path | None = None, flagged: frozenset = frozenset()) -> dict:
    """Laptop, once. stage must be a new empty directory outside the repo. flagged: dev files excluded by the W1
    near-duplicate pass (never staged; their QA leave every count)."""
    src = raw or RAW
    stage = stage.resolve()
    if (ROOT in stage.parents or stage == ROOT) and ROOT / "data/datasets" not in stage.parents:
        raise SystemExit("--stage must be outside the repo or under the gitignored data/datasets (question text)")
    if stage.exists() and any(stage.iterdir()):
        raise SystemExit(f"{stage} is not empty")
    tr, dv = load_src("train", src), load_src("dev", src)
    (stage / "images").mkdir(parents=True, exist_ok=True)
    zp = src / SRC["zip"][0]
    if sha(zp) != SRC["zip"][1]:
        raise SystemExit(f"{zp}: sha256 differs from OPS-1029l")
    fname = {im["id"]: im["filename"] for im in dv["images"] if im["filename"] not in flagged}
    dropped = [a["id"] for a in dv["annotations"] if a["image_id"] not in fname]
    with zipfile.ZipFile(zp) as zf:
        img_sha = extract(zf, sorted(fname.values(), key=lambda f: int(f[:-4])), stage / "images")
    grey_png(stage / "grey.png")
    qa, excluded, stratum = [], [], []
    with (stage / "questions.jsonl").open("w", encoding="utf-8") as fh:
        for a in dv["annotations"]:
            if a["image_id"] not in fname:
                continue
            f = fname[a["image_id"]]
            fh.write(json.dumps({"qa_id": a["id"], "image_id": a["image_id"], "file": f, "image_sha256": img_sha[f],
                                 "question": a["question"]}, ensure_ascii=False) + "\n")
            qa.append(a["id"])
            g = tokens(a["answers"][0])
            if not g:
                excluded.append(a["id"])
            elif marked([sig(t) for t in g]):
                stratum.append(a["id"])
    lists = {
        "schema": "vsps.l1a_lists.v1",
        "sources": {k: {"file": f, "sha256": s} for k, (f, s) in SRC.items()},
        "dev": {"n_qa": len(qa), "n_images": len(fname), "qa_ids_in_order": qa,
                "qa_ids_sha256": hashlib.sha256(json.dumps(qa).encode()).hexdigest(),
                "image_sha256": dict(sorted(img_sha.items(), key=lambda kv: int(kv[0][:-4]))),
                "excluded_empty_gold": excluded, "mark_bearing_stratum": stratum,
                "excluded_neardup": dropped, "excluded_neardup_files": sorted(flagged),
                "answers_per_question": sorted({len(a["answers"]) for a in dv["annotations"]})},
        "train_dev_disjoint": {"image_ids": not ({i["id"] for i in tr["images"]} & set(fname)),
                               "filenames": not ({i["filename"] for i in tr["images"]} & set(fname.values()))},
        "gold_noise_floor": {"train": noise_floor([x for a in tr["annotations"] for x in a["answers"]]),
                             "dev": noise_floor([x for a in dv["annotations"] for x in a["answers"]])},
        "stage": {"questions_sha256": sha(stage / "questions.jsonl"), "grey_png_sha256": sha(stage / "grey.png"),
                  "prompt_sha256": hashlib.sha256(PROMPT.encode()).hexdigest(), "max_new_tokens": MAX_NEW},
    }
    if (len(qa) + len(dropped), len(fname) + len(flagged)) != (N_DEV_QA, N_DEV_IMG) and raw is None:
        raise SystemExit(f"dev counts {len(qa)}+{len(dropped)}/{len(fname)}+{len(flagged)} differ from "
                         f"{N_DEV_QA}/{N_DEV_IMG}")
    return lists


def cmd_build(a) -> None:
    if LISTS.exists():
        raise SystemExit(f"{LISTS} exists; build runs once")
    if not ND.exists():
        raise SystemExit(f"{ND} missing: the W1 near-duplicate pass runs before the build (CC-165)")
    lists = build(a.stage, flagged=frozenset(json.loads(ND.read_text(encoding="utf-8"))["flagged_dev_files"]))
    PDIR.mkdir(parents=True, exist_ok=True)
    LISTS.write_text(json.dumps(lists, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {LISTS} {sha(LISTS)}; stage {a.stage}: {lists['dev']['n_images']} images, "
          f"{lists['dev']['n_qa']} questions, stratum {len(lists['dev']['mark_bearing_stratum'])}")


# ------------------------------------------------------------------------------------------------ W1 near-dup (laptop)
ND = PDIR / "neardup.json"
SSCD_PT = ROOT / ".session_backup/2026-10-22/c_stage1/sscd_disc_mixup.torchscript.pt"
SSCD_SHA = "9f26bd4c848cc19b73d2ae92eea6e04886f61a7b764ceb7a13aeee62e6a6db56"  # = w25.SSCD_SHA
HASH_MAX, SSCD_MIN, SSCD_COPY = 10, 0.5, 0.75  # W25 RULE §3: C2 = hash <= 10 and SSCD >= 0.5; C3 = SSCD > 0.75
MAX_UNREADABLE = 3  # 0.1% of the 3,353 other members (W25's MAX_LOST share); more is a FAULT


def nd_features(data: bytes, model) -> tuple | None:
    """match_openviic._features / _mirror_hashes on bytes in memory (load_image's draft + exif_transpose), so a
    non-dev image is never written to disk. None if unreadable."""
    import io

    import imagehash
    import torch
    from PIL import Image, ImageOps

    import match_openviic as MO

    try:
        im = Image.open(io.BytesIO(data))
        im.draft("RGB", (MO.SSCD_SHORT_SIDE, MO.SSCD_SHORT_SIDE))
        im = ImageOps.exif_transpose(im).convert("RGB")
    except Exception:  # noqa: BLE001  unreadable: counted, never matched
        return None
    m = ImageOps.mirror(im)
    h = lambda f, x: int(str(f(x)), 16)
    with torch.inference_mode():
        e = model(torch.from_numpy(MO.sscd_input(im))[None])[0].numpy()
    return (hashlib.sha256(data).hexdigest(), h(imagehash.phash, im), h(imagehash.dhash, im),
            h(imagehash.phash, m), h(imagehash.dhash, m), e)


def nd_flags(dev: list[tuple], oth: list[tuple]) -> list[dict]:
    """Per dev image: C1 equal sha, C2 min(pHash, dHash) <= 10 (dev mirrored hashes count) and SSCD >= 0.5,
    C3 SSCD > 0.75, against any other member (W25 RULE §3 union)."""
    import numpy as np

    from match_openviic import hamming

    col = lambda rows, k, t: np.array([r[k] for r in rows], t)
    osha, oph, odh = {r[0] for r in oth}, col(oth, 1, np.uint64), col(oth, 2, np.uint64)
    oe = np.stack([r[5] for r in oth])
    out = []
    for r in dev:
        ph = np.minimum(hamming(np.array([r[1]], np.uint64), oph), hamming(np.array([r[3]], np.uint64), oph))[0]
        dh = np.minimum(hamming(np.array([r[2]], np.uint64), odh), hamming(np.array([r[4]], np.uint64), odh))[0]
        sim = oe @ r[5]
        c = {"C1": r[0] in osha, "C2": bool(((np.minimum(ph, dh) <= HASH_MAX) & (sim >= SSCD_MIN)).any()),
             "C3": bool((sim > SSCD_COPY).any()), "max_sscd": float(sim.max()), "min_hash": int(np.minimum(ph, dh).min())}
        out.append(c)
    return out


def cmd_neardup(a) -> None:
    """CC-165 W1: the 1,676 staged dev images against the zip members that are neither train nor dev (read in
    memory, never written); test.json is never opened. Writes neardup.json (dev filenames, counts; no other name)."""
    import numpy as np
    import torch

    if ND.exists():
        raise SystemExit(f"{ND} exists; the pass runs once")
    if sha(SSCD_PT) != SSCD_SHA:
        raise SystemExit("SSCD weights differ from 9f26bd4c")
    torch.set_num_threads(os.cpu_count() or 1)
    model = torch.jit.load(str(SSCD_PT)).eval()
    tr, dv = load_src("train"), load_src("dev")
    dev = sorted({i["filename"] for i in dv["images"]}, key=lambda f: int(f[:-4]))
    known = set(dev) | {i["filename"] for i in tr["images"]}
    stage = a.stage / "images"
    df = [nd_features((stage / f).read_bytes(), model) for f in dev]
    if any(x is None for x in df):
        raise SystemExit("FAULT: an unreadable dev image")
    oth, bad, n = [], 0, 0
    with zipfile.ZipFile(RAW / SRC["zip"][0]) as zf:
        for m in zf.namelist():
            f = m.rsplit("/", 1)[-1]
            if m.endswith("/") or f in known:
                continue
            n += 1
            x = nd_features(zf.read(m), model)
            bad += x is None
            if x is not None:
                oth.append(x)
    if bad > MAX_UNREADABLE:
        raise SystemExit(f"FAULT: {bad} unreadable other members")
    fl = nd_flags(df, oth)
    hit = [(f, c) for f, c in zip(dev, fl) if c["C1"] or c["C2"] or c["C3"]]
    rec = {"schema": "vsps.l1a_neardup.v1", "rule": "excluded = C1 or C2 or C3 (W25 RULE §3), dev vs other members",
           "sscd_sha256": SSCD_SHA, "zip_sha256": SRC["zip"][1], "n_dev": len(dev), "n_other": n,
           "n_other_unreadable": bad,
           "counts": {k: sum(c[k] for _, c in hit) for k in ("C1", "C2", "C3")}, "n_flagged": len(hit),
           "flagged_dev_files": {f: c for f, c in hit},
           "max_sscd_quantiles": [float(x) for x in np.quantile([c["max_sscd"] for c in fl], [0.5, 0.9, 0.99, 1])]}
    PDIR.mkdir(parents=True, exist_ok=True)
    ND.write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {ND} {sha(ND)}: other {n} (unreadable {bad}), flagged {len(hit)} {rec['counts']}")


def pinned_lists() -> dict:
    if LISTS_SHA256 is None or sha(LISTS) != LISTS_SHA256:
        raise SystemExit("l1a_lists.json is not pinned (LISTS_SHA256) or differs from its pin")
    return json.loads(LISTS.read_text(encoding="utf-8"))


# ------------------------------------------------------------------------------------------------ M2 side
def stage_problems(stage: Path, lists: dict, ncs: Path) -> list[str]:
    """RULE §8: the staged dir holds exactly the 1,676 dev images at their shas, grey.png and questions.jsonl at
    their pins, nothing else; no zip and no ViTextVQA test file anywhere under NCS_DATA."""
    bad = []
    want = lists["dev"]["image_sha256"]
    have = {p.name for p in (stage / "images").iterdir()} if (stage / "images").is_dir() else set()
    if have != set(want):
        bad.append(f"images: {len(have - set(want))} extra, {len(set(want) - have)} missing")
    else:
        bad += [f"image {f} sha" for f, h in want.items() if sha(stage / "images" / f) != h]
    top = {p.name for p in stage.iterdir()} if stage.is_dir() else set()
    if top != {"images", "grey.png", "questions.jsonl"}:
        bad.append(f"stage top level {sorted(top)}")
    for f, k in (("grey.png", "grey_png_sha256"), ("questions.jsonl", "questions_sha256")):
        if (stage / f).is_file() and sha(stage / f) != lists["stage"][k]:
            bad.append(f"{f} sha")
    for p in ncs.rglob("*"):
        n = p.name.lower()
        if "vitextvqa" in n and (n.endswith(".zip") or "test" in n) or n == "st_images":
            bad.append(f"forbidden {p}")
    return bad


def cmd_guard(a) -> None:
    import b1
    import common as K

    if K.host_ok(a.head) != ROLE:
        raise SystemExit(f"REFUSED: L1-a runs only where /root/.vsps_machine_id is {ROLE} (M2)")
    bad = stage_problems(a.stage, pinned_lists(), Path(os.environ.get("NCS_DATA", "/root/ncs-data")))
    lock = Path(os.environ.get("L1A_LOCK", "/root/outputs/l1a/RUNNING"))
    bad += [x for x in b1.isolation() if x != f"lock {lock} exists"]
    if bad:
        raise SystemExit(f"REFUSED: {bad[:5]}")
    print("guard ok")


def registry() -> dict:
    if sha(REG) != REG_SHA256:
        raise SystemExit(f"{REG}: sha256 differs from its pin")
    return json.loads(REG.read_text(encoding="utf-8"))


def snap_dir(key: str) -> Path:
    """Where setup_gpu.sh put the model (HF cache or local_dir); qwen25vl_3b is fetched by the job."""
    m = registry()["models"][key]
    if key == "qwen3vl_8b":
        return Path("/root/ncs-data/models/Qwen3-VL-8B-Instruct-0c351dd")
    if key == "qwen25vl_3b":
        return Path("/root/ncs-data/models/l1a_qwen25vl_3b")
    from huggingface_hub import constants
    return Path(constants.HF_HUB_CACHE) / f"models--{m['hub_id'].replace('/', '--')}" / "snapshots" / m["revision"]


def read_questions(stage: Path, lists: dict) -> list[dict]:
    if sha(stage / "questions.jsonl") != lists["stage"]["questions_sha256"]:
        raise SystemExit("questions.jsonl differs from its pin")
    rows = [json.loads(x) for x in (stage / "questions.jsonl").read_text(encoding="utf-8").splitlines()]
    if [r["qa_id"] for r in rows] != lists["dev"]["qa_ids_in_order"]:
        raise SystemExit("questions.jsonl order differs from l1a_lists.json")
    return rows


def items_for(rows: list[dict], arm: str, grey_sha: str) -> list[tuple[str, str, str]]:
    if arm == "img":
        return [(str(r["qa_id"]), f"images/{r['file']}", r["image_sha256"]) for r in rows]
    return [(str(r["qa_id"]), "grey.png", grey_sha) for r in rows]


def with_questions(base_gen, rows: list[dict]):
    """decode_hf_vlm.make_generate's generate(sl, texts) with the pinned prompt filled per QA id."""
    q = {str(r["qa_id"]): r["question"] for r in rows}
    return lambda sl: base_gen(sl, texts=[PROMPT.format(q=q[i]) for i, _, _ in sl])


def cmd_decode(a) -> None:
    import decode_hf_vlm as D

    if sha(Path(D.__file__)) != LB_DECODER_SHA256:
        raise SystemExit("scripts/lb/decode_hf_vlm.py differs from its pin")
    lists, reg = pinned_lists(), registry()
    m = reg["models"][a.model]
    if D.packages() != reg["venv"]["packages"]:
        raise SystemExit(f"packages {D.packages()} differ from the registry")
    D.check_snapshot(m, a.snapshot)
    rows = read_questions(a.stage, lists)
    items = items_for(rows, a.arm, lists["stage"]["grey_png_sha256"])
    started = D.utc()
    proc, net = D.load(m, a.snapshot, "cuda:0")
    gen = with_questions(D.make_generate(proc, net, PROMPT, MAX_NEW, a.stage), rows)
    rid = f"l1a_{a.model}_{a.arm}"
    out = a.out_dir / f"{rid}.preds.json"
    part = Path(str(out) + ".partial.jsonl")
    resumed = part.exists()
    kw = {"max_new_tokens": MAX_NEW, "do_sample": False, "num_beams": 1}
    key = D.run_key(sha(Path(__file__)), {"run_id": rid, "questions": lists["stage"]["questions_sha256"]}, m, kw,
                    PROMPT, items)
    res = D.decode_slices(items, m["batch_size"], gen, part, key)
    import torch
    body = {"schema": "vsps.l1a_decode.v1", "run_id": rid, "model": a.model, "arm": a.arm, "hub_id": m["hub_id"],
            "revision": m["revision"], "registry_sha256": REG_SHA256, "l1a_sha256": sha(Path(__file__)),
            "lists_sha256": LISTS_SHA256, "questions_sha256": lists["stage"]["questions_sha256"],
            "prompt_sha256": hashlib.sha256(PROMPT.encode()).hexdigest(), "generate_kwargs": kw,
            "batch_size": m["batch_size"], "processor_kwargs": m["processor_kwargs"], "packages": D.packages(),
            "generation_config": net.generation_config.to_diff_dict(), "machine_id": os.environ.get("VSPS_MACHINE_ID"),
            "git_head": D.git("rev-parse", "HEAD"), "job_sha256": os.environ.get("VSPS_JOB_SHA256"),
            "gpu": torch.cuda.get_device_name(0), "resumed": resumed, "started_utc": started, "finished_utc": D.utc(),
            "n": len(res), "predictions": {r["image_id"]: r["caption"] for r in res},
            "n_tokens": {r["image_id"]: r["n_tokens"] for r in res}, "hit_max": {r["image_id"]: r["hit_max"] for r in res}}
    tmp = out.with_name(out.name + ".tmp")
    tmp.write_text(json.dumps(body, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    tmp.replace(out)
    Path(str(out) + ".sha256").write_text(f"{sha(out)}  {out.name}\n", encoding="utf-8")
    print(f"wrote {out}")


def cmd_fetch(a) -> None:
    import decode_hf_vlm as D
    from huggingface_hub import snapshot_download

    m = registry()["models"][a.model]
    snapshot_download(m["hub_id"], revision=m["revision"], local_dir=a.snapshot, allow_patterns=sorted(m["files"]))
    print(f"{a.model}: {D.check_snapshot(m, a.snapshot)} pinned files ok")


# ------------------------------------------------------------------------------------------------ score (laptop)
def boot_ratio(num, den, img_idx, rng_idx) -> tuple[float, float, float]:
    """Point and 95% percentile CI of sum(num)/sum(den), resampling images (clusters) with one shared matrix."""
    import numpy as np

    if not np.sum(den):
        return float("nan"), float("nan"), float("nan")
    num, den = np.bincount(img_idx, num), np.bincount(img_idx, den)
    n_b, d_b = num[rng_idx].sum(1), den[rng_idx].sum(1)
    r = np.divide(n_b, d_b, out=np.full(len(n_b), np.nan), where=d_b > 0)
    pt = num.sum() / den.sum() if den.sum() else float("nan")
    return float(pt), float(np.nanpercentile(r, 2.5)), float(np.nanpercentile(r, 97.5))


def boot_diff(n1, d1, n2, d2, img_idx, rng_idx) -> tuple[float, float, float]:
    """sum(n1)/sum(d1) - sum(n2)/sum(d2): point and 95% percentile CI, both ratios drawn with the same matrix."""
    import numpy as np

    if not (np.sum(d1) and np.sum(d2)):
        return float("nan"), float("nan"), float("nan")
    b = [np.bincount(img_idx, x, minlength=rng_idx.max() + 1) for x in (n1, d1, n2, d2)]
    s = [x[rng_idx].sum(1) for x in b]
    with np.errstate(invalid="ignore", divide="ignore"):
        r = s[0] / s[1] - s[2] / s[3]
    return float(b[0].sum() / b[1].sum() - b[2].sum() / b[3].sum()), float(np.nanpercentile(r, 2.5)), \
        float(np.nanpercentile(r, 97.5))


def verdict(rows: dict[str, dict]) -> tuple[str, str]:
    """RULE §6, clauses in order. rows: backbone -> {assessable, share, lo, hi} of the chance-corrected share
    (CC-165 W2)."""
    ok = {k: r for k, r in rows.items() if r["assessable"]}
    if len(ok) < 3:
        return "NO_VERDICT", f"{len(ok)} assessable backbones (< 3); judge"
    if all(r["share"] < KILL for r in ok.values()):
        hi = [k for k, r in ok.items() if r["hi"] >= KILL]
        return "KILL", "chance-corrected diacritic-only share < 10% on every assessable backbone" + (
            f"; CI reaches 10% for {hi} (judge reads)" if hi else "")
    if all(r["share"] >= STRONG and r["lo"] >= STRONG_LO for r in ok.values()):
        return "PROCEED_STRONG", ("chance-corrected share >= 20% and CI_lo >= 10% on every assessable backbone "
                                  "(fix clause untested)")
    return "PROCEED", "chance-corrected share >= 10% on at least one assessable backbone"


def score_backbone(gold: dict, img_of: dict, preds: dict, hit: dict, ids: list, stratum: set, rng_idx,
                   img_index: dict, grey: dict | None) -> dict:
    import numpy as np
    from collections import Counter

    res = {q: classify(gold[q], preds[q]) for q in ids}
    strict = {q: classify(gold[q], preds[q], "strict")["cls"] for q in ids}
    wrong = {q for q in ids if res[q]["cls"] != "correct"}
    diac = {q for q in wrong if res[q]["cls"] == "diac"}
    ii = np.array([img_index[img_of[q]] for q in ids])

    def share(sel: set, num: set, den: set) -> dict:
        n = np.array([q in num and q in sel for q in ids], float)
        d = np.array([q in den and q in sel for q in ids], float)
        pt, lo, hi = boot_ratio(n, d, ii, rng_idx)
        return {"share": pt, "lo": lo, "hi": hi, "n_num": int(n.sum()), "n_den": int(d.sum())}

    allq = set(ids)
    cl = {q: char_level(gold[q], preds[q]) for q in wrong}
    skel = lambda s: " ".join(sig(t)[0] for t in tokens(s))
    near = {q for q in wrong if res[q]["cls"] == "diac" or char_level(skel(gold[q]), skel(preds[q]))["base"] <= 2}
    tone_cm, vow_cm = Counter(), Counter()
    for q in diac & stratum:
        for g, p in res[q]["diffs"]:
            if g[2] != p[2]:
                tone_cm[f"{g[2]}>{p[2]}"] += 1
            gv, pv = dict((i, m) for i, m in g[1]), dict((i, m) for i, m in p[1])
            for i in sorted(set(gv) | set(pv)):
                if gv.get(i) != pv.get(i):
                    vow_cm[f"{gv.get(i, 'none')}>{pv.get(i, 'none')}"] += 1
    sw = {q for q in ids if strict[q] != "correct"}
    out = {
        "n": len(ids), "contained_em": 1 - len(wrong) / len(ids), "strict_em": 1 - len(sw) / len(ids),
        "mark_blind_em": (len(ids) - len(wrong) + len(diac)) / len(ids),
        "empty_rate": sum(not tokens(preds[q]) for q in ids) / len(ids),
        "hit_max_rate": sum(bool(hit.get(q)) for q in ids) / len(ids),
        "primary": share(stratum, diac, wrong),
        "all_items": share(allq, diac, wrong),
        "near_miss_denominator_inflated": share(allq, diac, near),
        "strict_view": share(stratum, {q for q in ids if strict[q] == "diac"}, sw),
        "diac_subclass": dict(Counter(res[q]["sub"] for q in diac & stratum)),
        "diac_all_marks_dropped": sum(res[q]["dropped_all"] for q in diac & stratum),
        "tone_confusion": dict(sorted(tone_cm.items())), "vowel_mark_confusion": dict(sorted(vow_cm.items())),
        "char_level_wrong_stratum": {k: sum(cl[q][k] for q in wrong & stratum) for k in ("n", "base", "mark")},
    }
    c = out["char_level_wrong_stratum"]
    c["mark_share_of_edits"] = c["mark"] / (c["mark"] + c["base"]) if c["mark"] + c["base"] else None
    out["assessable"] = out["empty_rate"] <= 0.20 and out["hit_max_rate"] <= 0.05
    if grey is not None:
        gc = {q for q in ids if classify(gold[q], grey[q])["cls"] == "correct"}
        out["grey_contained_em"] = len(gc) / len(ids)
        out["grey_contained_em_stratum"] = len(gc & stratum) / max(1, len(stratum))
        out["prior_flag"] = out["grey_contained_em"] >= PRIOR_FLAG
        keep = allq - gc
        out["primary_minus_grey_correct"] = share(stratum & keep, diac, wrong)
    glen = {q: min(len(tokens(gold[q])), 3) for q in ids}
    out["primary_by_gold_syllables"] = {k: share({q for q in stratum if glen.get(q) == k}, diac, wrong)
                                        for k in (1, 2, 3)}  # row (f); 3 = 3 or more
    out["primary_minus_1_syllable_gold"] = share({q for q in stratum if glen.get(q) != 1}, diac, wrong)
    nl = null_share(gold, img_of, preds, [q for q in ids if q in stratum])  # row (g)
    nc = nl.pop("by_item")
    out["mismatched_gold_null"] = nl
    ind = lambda f: np.array([f(q) for q in ids], float)
    pt, lo, hi = boot_diff(ind(lambda q: q in diac and q in stratum), ind(lambda q: q in wrong and q in stratum),
                           ind(lambda q: nc.get(q) == "diac"), ind(lambda q: q in nc and nc[q] != "correct"),
                           ii, rng_idx)
    out["corrected"] = {"share": pt, "lo": lo, "hi": hi, "rule": "primary share - row (g) null share (CC-165 W2)"}
    fold = lambda x: unicodedata.normalize("NFC", x).lower().replace("đ", "d")
    dd = {q for q in wrong if res[q]["cls"] == "base" and classify(fold(gold[q]), fold(preds[q]))["cls"] != "base"}
    out["d_stroke_only_base_errors"] = {"all": len(dd), "stratum": len(dd & stratum)}  # CC-165 W5: đ <-> d
    return out


def null_share(gold: dict, img_of: dict, preds: dict, st: list) -> dict:
    """RULE §6.2 (g): each prediction against the gold of another stratum item (a seeded derangement: shuffle, then
    pair each item with the next one, cyclic); pairs from the same image are skipped. The diac share of the wrong
    pairs is the chance rate at which the contained view finds a same-skeleton window in an unrelated answer."""
    import numpy as np

    order = [st[k] for k in np.random.default_rng(NULL_SEED).permutation(len(st))]
    pairs = [(q, order[(k + 1) % len(order)]) for k, q in enumerate(order)]
    pairs = [(q, g) for q, g in pairs if img_of[q] != img_of[g]]
    cls = {q: classify(gold[g], preds[q])["cls"] for q, g in pairs}
    wrong = sum(c != "correct" for c in cls.values())
    diac = sum(c == "diac" for c in cls.values())
    return {"pairs": len(pairs), "wrong": wrong, "diac": diac, "share": diac / wrong if wrong else None,
            "by_item": cls}


def load_preds(d: Path, model: str, arm: str, lists: dict) -> dict | None:
    p = d / f"l1a_{model}_{arm}.preds.json"
    if not p.exists():
        return None
    side = Path(str(p) + ".sha256")
    if not side.exists() or side.read_text().split()[0] != sha(p):
        raise SystemExit(f"{p}: sha256 sidecar missing or differs")
    x = json.loads(p.read_text(encoding="utf-8"))
    want = {"lists_sha256": LISTS_SHA256, "prompt_sha256": hashlib.sha256(PROMPT.encode()).hexdigest(),
            "registry_sha256": REG_SHA256, "questions_sha256": lists["stage"]["questions_sha256"], "n": lists["dev"]["n_qa"]}
    bad = {k: x.get(k) for k, v in want.items() if x.get(k) != v}
    if bad:
        raise SystemExit(f"{p}: provenance differs {bad}")
    return x


def cmd_score(a) -> None:
    import numpy as np

    if RULE_SHA256 is None or sha(RULE) != RULE_SHA256:
        raise SystemExit("RULE.md is not pinned (RULE_SHA256) or differs from its pin")
    if sha(ROOT / "rescap/chair.py") != CHAIR_SHA256:
        raise SystemExit("rescap/chair.py (norm_tone) differs from its pin")
    if OUT.exists():
        raise SystemExit(f"{OUT} exists; score runs once")
    lists = pinned_lists()
    dv = load_src("dev")
    excl = set(lists["dev"]["excluded_empty_gold"])
    gold = {str(x["id"]): x["answers"][0] for x in dv["annotations"] if x["id"] not in excl}
    img_of = {str(x["id"]): x["image_id"] for x in dv["annotations"]}
    ids = [str(q) for q in lists["dev"]["qa_ids_in_order"] if q not in excl]
    stratum = {str(q) for q in lists["dev"]["mark_bearing_stratum"]}
    imgs = sorted({img_of[q] for q in ids})
    img_index = {im: k for k, im in enumerate(imgs)}
    rng_idx = np.random.default_rng(SEED).integers(0, len(imgs), (B, len(imgs)))
    rows = {}
    for m in MODELS:
        p = load_preds(a.preds, m, "img", lists)
        if p is None:
            rows[m] = {"assessable": False, "missing": True}
            continue
        g = load_preds(a.preds, m, "grey", lists)
        rows[m] = score_backbone(gold, img_of, p["predictions"], p["hit_max"], ids, stratum, rng_idx, img_index,
                                 None if g is None else g["predictions"])
    prim = {m: {"assessable": r["assessable"], **({k: r["corrected"][k] for k in ("share", "lo", "hi")}
                                                   if "corrected" in r else {})} for m, r in rows.items()}
    out, why = verdict(prim)
    no1 = {m: {"assessable": r["assessable"], **({k: r["primary_minus_1_syllable_gold"][k] for k in ("share", "lo", "hi")}
                                                  if "primary" in r else {})} for m, r in rows.items()}
    flags = [f"{m}: mismatched-gold null diac share {r['mismatched_gold_null']['share']:.3f} >= {NULL_FLAG}"
             for m, r in rows.items() if "primary" in r and (r["mismatched_gold_null"]["share"] or 0) >= NULL_FLAG]
    raw = {m: {"assessable": r["assessable"], **({k: r["primary"][k] for k in ("share", "lo", "hi")}
                                                  if "primary" in r else {})} for m, r in rows.items()}
    if verdict(no1)[0] != verdict(raw)[0]:
        flags.append(f"uncorrected: dropping 1-syllable golds gives {verdict(no1)[0]}, not {verdict(raw)[0]}")
    flags += [f"{m}: prior_flag (grey EM >= {PRIOR_FLAG})" for m, r in rows.items() if r.get("prior_flag")]
    if any("primary_minus_grey_correct" in r and r["assessable"] and
           (r["primary"]["share"] < KILL) != (r["primary_minus_grey_correct"]["share"] < KILL) for r in rows.values()):
        flags.append("row (e) moves a backbone across 10%")
    ok = [m for m in MODELS if rows[m]["assessable"]]
    rank = lambda k: sorted(ok, key=lambda m: -rows[m][k])
    dec = {"schema": "vsps.l1a_decide.v1", "rule_sha256": RULE_SHA256, "lists_sha256": LISTS_SHA256,
           "outcome": out, "reason": why, "scope": SCOPE, "outcome_uncorrected_descriptive": verdict(raw)[0],
           "excluded_neardup_qa": len(lists["dev"].get("excluded_neardup", [])), "judge_flags": flags, "n_items": len(ids),
           "n_stratum": len(stratum & set(ids)),
           "ranking": {"contained_em": rank("contained_em"), "mark_blind_em": rank("mark_blind_em"),
                       "changes": rank("contained_em") != rank("mark_blind_em")},
           "backbones": rows}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(dec, indent=1) + "\n", encoding="utf-8")
    print(f"{out}: {why}\nwrote {OUT} {sha(OUT)}")


# ------------------------------------------------------------------------------------------------ selftest
def selftest() -> None:
    import numpy as np

    ok: list[str] = []

    def check(name, cond):
        if not cond:
            raise AssertionError(name)
        ok.append(name)

    def refused(name, fn):
        try:
            fn()
        except SystemExit:
            ok.append(name)
            return
        raise AssertionError(name)

    # orthography (synthetic syllables, not dataset text)
    check("NFD: ệ = e + dot below + circumflex, classified by code point", sig("ệ") == ("e", ((0, "circ"),), "nang"))
    check("tone placement is position-free: hòa == hoà", sig("hòa") == sig("hoà"))
    check("đ stays a base letter (đa vs da is a base error)", sig("đa")[0] != sig("da")[0]
          and classify("đa", "da")["cls"] == "base")
    check("a stray combining mark stays in its syllable (mark order free)",
          classify("ế", "e\u0301\u0302")["cls"] == "correct")
    check("NFD input equals NFC input", classify("mười", unicodedata.normalize("NFD", "Mười"))["cls"] == "correct")
    check("tone-only", classify("bán", "bàn")["sub"] == "tone")
    check("vowel-mark-only", classify("tôm", "tơm")["sub"] == "vowel")
    check("both", classify("mười", "muối")["sub"] == "both")
    r = classify("xôi gấc", "xoi gac")
    check("all marks dropped is diac, flagged", r["cls"] == "diac" and r["dropped_all"])
    check("contained: a correct window inside a longer answer", classify("xôi gấc", "đó là xôi gấc.")["cls"] == "correct")
    check("strict: the same answer is wrong (base)", classify("xôi gấc", "đó là xôi gấc.", "strict")["cls"] == "base")
    check("contained: correct window wins over an earlier diac window",
          classify("bán", "bàn và bán")["cls"] == "correct")
    check("disclosed: a 1-syllable gold is diac inside a long unrelated answer with a same-skeleton syllable",
          classify("gấc", "biển ghi số nhà và chữ gác ở dưới")["cls"] == "diac"
          and classify("gấc", "biển ghi số nhà và chữ gác ở dưới", "strict")["cls"] == "base")
    check("contained: diac window inside a longer answer", classify("xôi gấc", "là xôi gầc")["sub"] == "tone")
    check("punctuation and case ignored", classify("số 12", "Số 12!")["cls"] == "correct")
    check("empty prediction is base, flagged empty", classify("bán", "")["cls"] == "base" and classify("bán", "")["empty"])
    check("base error", classify("bán", "bút")["cls"] == "base")
    try:
        classify("...", "x")
        raise AssertionError("empty gold accepted")
    except ValueError:
        ok.append("empty gold refused")
    check("char ops: one mark substitution", char_ops(units("bán"), units("bàn")) == (0, 1))
    check("char ops: base substitution", char_ops(units("bán"), units("bún"))[0] == 1)
    check("char ops: old/new placement costs nothing", char_ops(units("hòa"), units("hoà")) == (0, 0))
    check("char ops: insertion counted as base", char_ops(units("ba"), units("bao")) == (1, 0))
    check("char level uses the best window", char_level("xôi gấc", "đây là xôi gầc") == {"n": 7, "base": 0, "mark": 1})
    nf = noise_floor(["lòa xa", "hoà", "mua", "12"])
    check("noise floor counts old/new placement and unmarked answers",
          nf["old_style_open_cluster"] == 1 and nf["new_style_open_cluster"] == 1 and nf["answers_without_marks"] == 2)
    # bootstrap and verdict
    rng = np.random.default_rng(0).integers(0, 4, (200, 4))
    pt, lo, hi = boot_ratio(np.array([1., 0, 1, 0, 0]), np.array([1., 1, 1, 1, 0]), np.array([0, 0, 1, 2, 3]), rng)
    check("cluster bootstrap ratio: point and ordered CI", pt == 0.5 and lo <= pt <= hi)
    R = lambda s, lo=0.0, hi=1.0, a=True: {"assessable": a, "share": s, "lo": lo, "hi": hi}
    check("KILL: < 10% on every assessable backbone", verdict({k: R(0.05, 0.02, 0.08) for k in "abcd"})[0] == "KILL")
    check("KILL reports a CI reaching 10%", "judge" in verdict({k: R(0.09, 0.05, 0.12) for k in "abcd"})[1])
    check("PROCEED: one backbone >= 10%", verdict({"a": R(0.12), "b": R(0.05), "c": R(0.05), "d": R(0.05)})[0]
          == "PROCEED")
    check("PROCEED_STRONG needs CI_lo >= 10% everywhere", verdict({k: R(0.25, 0.12) for k in "abcd"})[0]
          == "PROCEED_STRONG" and verdict({k: R(0.25, 0.08) for k in "abcd"})[0] == "PROCEED")
    check("non-assessable backbones do not count", verdict({"a": R(0.5, a=False), "b": R(0.05), "c": R(0.05),
                                                            "d": R(0.05)})[0] == "KILL")
    m = np.random.default_rng(0).integers(0, 100, (500, 100))
    ii = np.arange(100)
    one = lambda k: np.array([1.0] * k + [0.0] * (100 - k))
    c = boot_diff(one(12), one(100), one(7), one(100), ii, m)
    check("W2: raw 12% on a 7% null corrects to 5% -> KILL (an artifact is not PROCEED)",
          abs(c[0] - 0.05) < 1e-12 and c[1] <= c[0] <= c[2]
          and verdict({k: R(*c) for k in "abcd"})[0] == "KILL")
    c = boot_diff(one(40), one(100), one(2), one(100), ii, m)
    check("W2: raw 40% on a 2% null corrects to 38% -> PROCEED_STRONG",
          abs(c[0] - 0.38) < 1e-12 and verdict({k: R(*c) for k in "abcd"})[0] == "PROCEED_STRONG")
    check("NO_VERDICT under 3 assessable", verdict({"a": R(0.5), "b": R(0.5), "c": R(0.5, a=False)})[0]
          == "NO_VERDICT")
    # scoring end to end on synthetic gold/preds
    gold = {"1": "bán", "2": "xôi gấc", "3": "12", "4": "tôm"}
    img_of = {"1": 0, "2": 0, "3": 1, "4": 2}
    preds = {"1": "bàn", "2": "xôi gấc", "3": "13", "4": "tom"}
    grey = {"1": "bán", "2": "x", "3": "x", "4": "x"}
    s = score_backbone(gold, img_of, preds, {}, list(gold), {"1", "2", "4"},
                       np.random.default_rng(0).integers(0, 3, (50, 3)), {0: 0, 1: 1, 2: 2}, grey)
    check("score: primary share over the mark-bearing stratum = 2/2, all items 2/3",
          s["primary"]["share"] == 1.0 and abs(s["all_items"]["share"] - 2 / 3) < 1e-12)
    check("score: subclasses, tone confusion, grey prior and its sensitivity row",
          s["diac_subclass"] == {"tone": 1, "vowel": 1} and s["tone_confusion"] == {"sac>huyen": 1}
          and s["grey_contained_em"] == 0.25 and s["primary_minus_grey_correct"]["n_den"] == 1)
    check("score: corrected share and the d-stroke count present",
          "corrected" in s and s["d_stroke_only_base_errors"] == {"all": 0, "stratum": 0})
    dd = score_backbone({"1": "đá", "2": "bán"}, {"1": 0, "2": 1}, {"1": "da", "2": "bán"}, {}, ["1", "2"], {"1", "2"},
                        np.random.default_rng(0).integers(0, 2, (20, 2)), {0: 0, 1: 1}, None)
    check("W5: đá vs da is base and counted as a d-stroke error", dd["d_stroke_only_base_errors"]["stratum"] == 1)
    check("score: rows (f) by gold length and (g) mismatched-gold null present",
          s["primary_by_gold_syllables"][1]["n_den"] == 2 and s["mismatched_gold_null"]["pairs"] >= 1)
    nl = null_share({"1": "bán", "2": "gấc", "3": "tôm"}, {"1": 0, "2": 1, "3": 2},
                    {"1": "gác", "2": "bàn", "3": "x"}, ["1", "2", "3"])
    check("null: a derangement pairs every item with another image's gold", nl["pairs"] == 3 and nl["wrong"] == 3)
    # prompt, decode wrapper, items
    rows = [{"qa_id": 7, "file": "3.jpg", "image_sha256": "h", "question": "câu?"}]
    seen = []
    gen = with_questions(lambda sl, texts: seen.extend(texts) or [("a", 1, False)] * len(sl), rows)
    gen(items_for(rows, "img", "g"))
    check("each QA gets the pinned prompt with its own question", seen == [PROMPT.format(q="câu?")])
    check("grey arm points every QA at grey.png", items_for(rows, "grey", "g") == [("7", "grey.png", "g")])
    # build on a synthetic raw dir, staging guard
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        (t / "raw").mkdir()
        tr = {"images": [{"id": 0, "filename": "0.jpg"}], "annotations": [
            {"id": 1, "image_id": 0, "question": "q", "answers": ["bán"]}]}
        dv = {"images": [{"id": 5, "filename": "5.jpg"}, {"id": 6, "filename": "6.jpg"}], "annotations": [
            {"id": 9, "image_id": 5, "question": "q", "answers": ["gấc"]},
            {"id": 10, "image_id": 6, "question": "q", "answers": ["12"]},
            {"id": 11, "image_id": 6, "question": "q", "answers": ["..."]}]}
        (t / "raw/tr.json").write_text(json.dumps(tr))
        (t / "raw/dv.json").write_text(json.dumps(dv))
        with zipfile.ZipFile(t / "raw/z.zip", "w") as z:
            for n in ("0", "5", "6", "77"):
                z.writestr(f"st_images/{n}.jpg", f"img{n}")
        global SRC
        keep = SRC
        SRC = {"train": ("tr.json", sha(t / "raw/tr.json")), "dev": ("dv.json", sha(t / "raw/dv.json")),
               "zip": ("z.zip", sha(t / "raw/z.zip"))}
        try:
            refused("build refuses a stage inside the repo", lambda: build(ROOT / "scripts/x_l1a_stage", t / "raw"))
            L = build(t / "stage", t / "raw")
            Lx = build(t / "stage_x", t / "raw", frozenset({"6.jpg"}))
            check("W1: a flagged dev image is not staged and its QA leave every list",
                  sorted(p.name for p in (t / "stage_x/images").iterdir()) == ["5.jpg"]
                  and Lx["dev"]["qa_ids_in_order"] == [9] and Lx["dev"]["excluded_neardup"] == [10, 11])
            names = sorted(p.name for p in (t / "stage/images").iterdir())
            check("build extracts only the dev images by name (no train, no other split)", names == ["5.jpg", "6.jpg"])
            q = (t / "stage/questions.jsonl").read_text()
            check("questions.jsonl has no answer field", '"answers"' not in q and "gấc" not in q)
            check("stratum and exclusions from gold only", L["dev"]["mark_bearing_stratum"] == [9]
                  and L["dev"]["excluded_empty_gold"] == [11])
            check("train/dev disjointness recorded", all(L["train_dev_disjoint"].values()))
            refused("build refuses a non-empty stage", lambda: build(t / "stage", t / "raw"))
            with zipfile.ZipFile(t / "raw/z.zip") as z:
                refused("member names other than <digits>.jpg are refused", lambda: extract(z, ["../a.jpg"], t))
            ncs = t / "ncs"
            (ncs / "datasets").mkdir(parents=True)
            check("staged set passes", stage_problems(t / "stage", L, ncs) == [])
            (t / "stage/images/77.jpg").write_text("x")
            check("an extra image is refused", stage_problems(t / "stage", L, ncs) != [])
            (t / "stage/images/77.jpg").unlink()
            (ncs / "datasets/ViTextVQA_test.json").write_text("{}")
            check("a ViTextVQA test file under NCS_DATA is refused", stage_problems(t / "stage", L, ncs) != [])
            (ncs / "datasets/ViTextVQA_test.json").unlink()
            (ncs / "ViTextVQA_images.zip").write_text("")
            check("a ViTextVQA zip under NCS_DATA is refused", stage_problems(t / "stage", L, ncs) != [])
        finally:
            SRC = keep
        # cap arithmetic (B-1's accounting, 12 GPU-h cap)
        import b1
        u = t / "used.tsv"
        u.write_text("a start 0\na 40000\n")
        check("cap: 12 GPU-h minus used", b1.left(u, t / "M", CAP_S) == CAP_S - 40000)
        (t / "M").write_text("{}")
        check("cap: a CAP_STOP marker is final", b1.left(u, t / "M", CAP_S) == 0)
    check("prompt has one {q} slot and fits the 48-token answer budget", PROMPT.count("{q}") == 1 and MAX_NEW == 48)
    print("\n".join("PASS " + n for n in ok) + f"\nselftest ok ({len(ok)} checks)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("build")
    p.add_argument("--stage", type=Path, required=True)
    p = sub.add_parser("guard")
    p.add_argument("--head", required=True)
    p.add_argument("--stage", type=Path, required=True)
    p = sub.add_parser("lock")
    p.add_argument("--path", type=Path, required=True)
    p = sub.add_parser("left")
    p.add_argument("--used", type=Path, required=True)
    p.add_argument("--marker", type=Path, required=True)
    p = sub.add_parser("snap")
    p.add_argument("--model", choices=MODELS, required=True)
    p = sub.add_parser("fetch")
    p.add_argument("--model", choices=MODELS, required=True)
    p.add_argument("--snapshot", type=Path, required=True)
    p = sub.add_parser("decode")
    p.add_argument("--model", choices=MODELS, required=True)
    p.add_argument("--arm", choices=ARMS, required=True)
    p.add_argument("--stage", type=Path, required=True)
    p.add_argument("--snapshot", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    p = sub.add_parser("neardup")
    p.add_argument("--stage", type=Path, required=True)
    p = sub.add_parser("score")
    p.add_argument("--preds", type=Path, required=True)
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    def lock():
        import b1
        b1.take_lock(a.path)

    def left():
        import b1
        print(b1.left(a.used, a.marker, CAP_S))

    {"build": lambda: cmd_build(a), "guard": lambda: cmd_guard(a), "lock": lock, "left": left,
     "snap": lambda: print(snap_dir(a.model)), "neardup": lambda: cmd_neardup(a), "fetch": lambda: cmd_fetch(a), "decode": lambda: cmd_decode(a),
     "score": lambda: cmd_score(a)}.get(a.cmd, ap.print_help)()


if __name__ == "__main__":
    main()
