#!/usr/bin/env python3
"""L1-b (DEV-EXPLORE, ViTextVQA dev half E only): does a training-free, image-verified re-rank of the diacritic
marks of an LVLM's own answer cut diacritic-only errors? Each syllable of the first-pass answer gets a closed,
rule-generated set of mark variants (same base letters, đ never changed); the backbone scores every variant answer by
its own teacher-forced log-likelihood given the real image and given the grey image; the laptop picks one config
from a pre-fixed grid and scores it once against the human gold. Rule: manuscript/prereg/2026-10-29_l1b/PREREG.md.

    python3 scripts/l1b/l1b.py --selftest                         CPU; synthetic text; tiny random model if torch is in
    python3 -P scripts/l1b/l1b.py build --l1a-stage DIR --stage DIR    laptop CPU, once: split + l1b_split.json + stage
    python  scripts/l1b/l1b.py guard --head H --stage DIR         M2 (machine id m4): host, GPU, HEAD, gates, stage
    python  scripts/l1b/l1b.py lock --path P | left --used F --marker M
    python  scripts/l1b/l1b.py snap|fetch --model K [--snapshot DIR]
    python  scripts/l1b/l1b.py decode --model K --stage DIR --snapshot DIR --out-dir DIR    non-Qwen base answers, E
    python  scripts/l1b/l1b.py rerank --model K --stage DIR --snapshot DIR --base FILE --out-dir DIR
    python3 scripts/l1b/l1b.py score --out-dir DIR                laptop CPU, once (DIR = the pulled M2 out/)

No gold answer is staged on M2 or written by this file; `score` writes ids, counts and numbers only.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import os
import re
import shutil
import sys
import tempfile
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "scripts/l1a")]
import l1a  # noqa: E402  pinned (SHA256SUMS); its own sys.path setup brings b1, grl/common, lb, g2b

PDIR = ROOT / "manuscript/prereg/2026-10-29_l1b"
PREREG, PREREG_SHA256 = PDIR / "PREREG.md", "b6034c4a51a6f92280c0cac57511e77d08462aed202f86ee551b36ad755c53c7"  # finalised (CC-168b F1)
L1B_REG, L1B_REG_SHA256 = PDIR / "l1b_registry.json", "cd210a7ca0f85b10c6f9ee95f8b737284f5029ef5f05c84d1ee760d18e7b96e3"  # finalised
SPLIT, SPLIT_SHA256 = PDIR / "l1b_split.json", "b749f7202bc2085052392f05a04da6b5c9080e47a5b23e2beee9c70a23c69f51"  # written once by `build`, pinned
GATES = PDIR / "GATES.json"  # G1 / G3 LOG ids, filled by the gatekeeper; the guard refuses while either is empty
OUT = ROOT / ".session_backup/2026-10-29/l1b/decide.json"
L1A_PREDS = ROOT / ".session_backup/machines/M2/root/outputs/l1a/preds"
L1A_IMG_SHA = {"qwen25vl_7b": "ebfddfa7ddde895ce4d66005be2a082314f48d325e7055d1332a5feaa3841645",
               "qwen3vl_8b": "c4cf7cab497da4ca1c1d8d6a0ec5e07880a7e44ad737bb1a803fef81a3b36f14",
               "internvl3_8b": "9cc4db1841248a526329d213c315dd496fa832ee6d9b9f5e6125f6f7fd4dd23e"}  # OPS-1029q
REUSE_DEC = {"idefics3_8b": ("ec3f8478e1f28b02460318e8435bf53160bd09b81cce252669da00370b3b4426",
                             "d312c12899d9d10eccaf6197dd3f3b9bd429ea07d42194af819b9d56c69026a6")}  # AMENDMENT_1 §4: (preds sha, l1b.py sha that wrote it)
QWEN = tuple(L1A_IMG_SHA)
NONQWEN = ("gemma3_4b", "idefics3_8b")  # both run in this order; score uses the first assessable (PREREG §3)
MODELS = QWEN + NONQWEN
CAP_S = 8 * 3600
SALT = "l1b-split-2026-10-29"
MAX_VAR, MAX_CAND = 108, 256  # per syllable, per answer (PREREG §4.2)
PARITY_N, PARITY_K, PARITY_TOL = 4, 8, 2.0  # items, candidates, nats (PREREG §4.4; tol 0.25 -> 2.0 by AMENDMENT_1)
ALPHA, TAU = (0.0, 0.5, 1.0), (0.0, 0.5, 1.0, 2.0)
SESOI, STRONG, PRIOR_MARGIN, HARM = 1.0, 2.0, 0.5, 0.25  # EM points; harm = flips to wrong / flips to right
NQ_MIN_EM, NQ_MIN_DIAC = 0.20, 30

# ------------------------------------------------------------------------------------------------ orthography
VOWEL_OPT = {"a": "aâă", "e": "eê", "o": "oôơ", "u": "uư", "i": "i", "y": "y"}
BASE_OF = {c: b for b, opts in VOWEL_OPT.items() for c in opts}
TONE_CH = ("", "̀", "́", "̉", "̃", "̣")  # none, huyền, sắc, hỏi, ngã, nặng
STOP_TONES = ("́", "̣")  # a syllable ending in p, t, c, ch takes only sắc or nặng
MARKED = set("âăêôơư")


def strip_tone(ch: str) -> str:
    return unicodedata.normalize("NFC", "".join(c for c in unicodedata.normalize("NFD", ch) if c not in TONE_CH[1:]))


def tone_pos(letters: list[str]) -> int | None:
    """Index of the letter that carries the tone (old style, the gold's majority: hòa, thủy). letters: lowercase NFC,
    no tone. qu- and gi- + vowel count as consonants."""
    v = [i for i, c in enumerate(letters) if c in BASE_OF]
    if v and v[0] == 1 and letters[0] == "q" and letters[1] == "u":
        v = v[1:]
    if len(v) > 1 and v[0] == 1 and letters[0] == "g" and letters[1] == "i":
        v = v[1:]
    if not v:
        return None
    mk = [i for i in v if letters[i] in MARKED]
    if mk:
        return mk[-1]
    if len(v) == 1:
        return v[0]
    if v[-1] < len(letters) - 1:  # a final consonant follows the vowel cluster
        return v[-1]
    return v[1] if len(v) == 3 else v[0]


def variants(syl: str) -> list[str]:
    """The closed candidate set of one syllable (PREREG §4.2): every vowel-mark choice on its vowel letters x 6 tones,
    the stop-final tone rule applied, rendered with the fixed tone placement and the syllable's own letter case,
    one form per l1a.sig signature, the syllable's own signature removed. [] for digits, no vowel, or > MAX_VAR."""
    s = unicodedata.normalize("NFC", syl)
    low = [strip_tone(c) for c in s.lower()]
    if any(len(c) != 1 or c.isdigit() for c in low) or tone_pos([BASE_OF.get(c, c) for c in low]) is None:
        return []  # AMENDMENT_1: a bare qu- (u is the consonant glide) has no tone-bearing vowel either
    opts = [VOWEL_OPT[BASE_OF[c]] if c in BASE_OF else c for c in low]
    stop = "".join(low).endswith(("p", "t", "c", "ch"))
    tones = STOP_TONES if stop else TONE_CH
    own, seen, out = l1a.sig(s.lower()), set(), []
    combos = list(itertools.product(*opts))
    if len(combos) * len(tones) > MAX_VAR:
        return []
    for combo in combos:
        k = tone_pos(list(combo))
        for t in tones:
            w = list(combo)
            if t:
                w[k] = unicodedata.normalize("NFC", w[k] + t)
            w = [x.upper() if o.isupper() else x for x, o in zip(w, s)]
            v = "".join(w)
            g = l1a.sig(v.lower())
            if g != own and g not in seen:
                seen.add(g)
                out.append(v)
    return out


def candidates(pred: str) -> tuple[str, list[tuple[int, int, int, str]]]:
    """(base, [(syllable index, start, end, variant answer)]): the NFC first-pass answer and every answer that differs
    from it in the marks of exactly one syllable; syllables are taken in order until MAX_CAND would be passed."""
    base = unicodedata.normalize("NFC", pred)
    out = []
    for k, m in enumerate(l1a.TOK.finditer(base)):
        vs = variants(m.group())
        if len(out) + len(vs) > MAX_CAND:
            break
        out += [(k, m.start(), m.end(), base[:m.start()] + v + base[m.end():]) for v in vs]
    return base, out


def n_truncated(base: str, cands: list) -> int:
    """Syllables with variants left unchanged by the MAX_CAND cap (PREREG §4.2; CC-168 W14)."""
    used = {c[0] for c in cands}
    return sum(1 for k, m in enumerate(l1a.TOK.finditer(base)) if k not in used and variants(m.group()))


def cand_sha(base: str, cands: list) -> str:
    return hashlib.sha256(json.dumps([base] + [c[3] for c in cands], ensure_ascii=False).encode()).hexdigest()


def choose(base: str, cands: list, img: list, grey: list, alpha: float, tau: float, text_only: bool = False) -> str:
    """Per syllable independently: the variant with the largest gain over the first-pass answer, applied if the gain
    exceeds tau. gain = d(img) - alpha * d(grey); text_only (the T baseline): gain = d(grey). Index 0 = base."""
    best: dict[int, tuple[float, int, int, str]] = {}
    for j, (k, s, e, ans) in enumerate(cands, 1):
        g = grey[j] - grey[0] if text_only else (img[j] - img[0]) - alpha * (grey[j] - grey[0])
        if g > tau and (k not in best or g > best[k][0]):
            best[k] = (g, s, e, ans[s:e + len(ans) - len(base)])
    out = base
    for _g, s, e, v in sorted(best.values(), key=lambda x: -x[1]):
        out = out[:s] + v + out[e:]
    return out


# ------------------------------------------------------------------------------------------------ split (laptop)
def clusters(files: list[str], feats: list[tuple]) -> list[list[str]]:
    """Union-find over within-dev pairs under the W25 union (C1 sha, C2 hash <= 10 and SSCD >= 0.5, C3 SSCD > 0.75)."""
    import numpy as np

    from match_openviic import hamming

    par = list(range(len(files)))

    def root(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i

    ph = np.array([f[1] for f in feats], np.uint64)
    dh = np.array([f[2] for f in feats], np.uint64)
    emb = np.stack([f[5] for f in feats])
    for i, f in enumerate(feats):
        hp = np.minimum(hamming(np.array([f[1]], np.uint64), ph), hamming(np.array([f[3]], np.uint64), ph))[0]
        hd = np.minimum(hamming(np.array([f[2]], np.uint64), dh), hamming(np.array([f[4]], np.uint64), dh))[0]
        sim = emb @ f[5]
        hit = (np.minimum(hp, hd) <= l1a.HASH_MAX) & (sim >= l1a.SSCD_MIN) | (sim > l1a.SSCD_COPY)
        hit |= np.array([g[0] == f[0] for g in feats])
        for j in np.flatnonzero(hit):
            par[root(int(j))] = root(i)
    groups: dict[int, list[str]] = {}
    for i, f in enumerate(files):
        groups.setdefault(root(i), []).append(f)
    return sorted((sorted(g, key=lambda x: int(x[:-4])) for g in groups.values()), key=lambda g: int(g[0][:-4]))


def side(key: str, bit: int = 0) -> int:
    """0 = E (explore), 1 = C (confirm) for bit 0; bit 1 gives the cross-fit halves inside E."""
    return int(hashlib.sha256(f"{SALT}:{key}".encode()).hexdigest()[:8], 16) >> bit & 1


def cmd_build(a) -> None:
    import torch

    if SPLIT.exists():
        raise SystemExit(f"{SPLIT} exists; the split is built once")
    if a.stage.exists():
        raise SystemExit(f"{a.stage} exists")
    lists = l1a.pinned_lists()
    want = lists["dev"]["image_sha256"]
    if l1a.sha(l1a.SSCD_PT) != l1a.SSCD_SHA:
        raise SystemExit("SSCD weights differ from their pin")
    torch.set_num_threads(os.cpu_count() or 1)
    model = torch.jit.load(str(l1a.SSCD_PT)).eval()
    files = sorted(want, key=lambda f: int(f[:-4]))
    feats = []
    for f in files:
        p = a.l1a_stage / "images" / f
        if l1a.sha(p) != want[f]:
            raise SystemExit(f"{p}: sha differs from l1a_lists.json")
        feats.append(l1a.nd_features(p.read_bytes(), model))
    if any(x is None for x in feats):
        raise SystemExit("FAULT: an unreadable dev image")
    cl = clusters(files, feats)
    e_files = {f for g in cl if side(g[0]) == 0 for f in g}
    rows = l1a.read_questions(a.l1a_stage, lists)
    e_rows = [r for r in rows if r["file"] in e_files]
    strat = set(lists["dev"]["mark_bearing_stratum"])
    (a.stage / "images").mkdir(parents=True)
    for f in sorted(e_files):
        shutil.copyfile(a.l1a_stage / "images" / f, a.stage / "images" / f)
    shutil.copyfile(a.l1a_stage / "grey.png", a.stage / "grey.png")
    (a.stage / "questions.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in e_rows),
                                             encoding="utf-8")
    (a.stage / "preds").mkdir()
    for m, h in L1A_IMG_SHA.items():
        src = L1A_PREDS / f"l1a_{m}_img.preds.json"
        if l1a.sha(src) != h:
            raise SystemExit(f"{src}: sha differs from OPS-1029q")
        shutil.copyfile(src, a.stage / "preds" / src.name)
    e_ids = [str(r["qa_id"]) for r in e_rows]
    rec = {"schema": "vsps.l1b_split.v1", "salt": SALT, "rule": "W25 union within the 1,520 kept dev images -> "
           "clusters; a cluster goes to E iff bit 0 of sha256(salt:first file) is 0; E1/E2 by bit 1 (cross-fit)",
           "lists_sha256": l1a.LISTS_SHA256, "sscd_sha256": l1a.SSCD_SHA, "n_clusters": len(cl),
           "n_multi_image_clusters": sum(len(g) > 1 for g in cl), "largest_cluster": max(map(len, cl)),
           "E": {"n_images": len(e_files), "n_qa": len(e_ids), "n_stratum": sum(int(i) in strat for i in e_ids),
                 "files": sorted(e_files, key=lambda x: int(x[:-4])), "qa_ids_in_order": e_ids,
                 "e1_files": sorted((f for g in cl if side(g[0]) == 0 and side(g[0], 1) == 0 for f in g),
                                    key=lambda x: int(x[:-4]))},
           "C": {"n_images": len(files) - len(e_files), "n_qa": len(rows) - len(e_ids),
                 "files": sorted(set(files) - e_files, key=lambda x: int(x[:-4]))},
           "stage": {"questions_sha256": l1a.sha(a.stage / "questions.jsonl"),
                     "grey_png_sha256": lists["stage"]["grey_png_sha256"], "preds_sha256": L1A_IMG_SHA}}
    SPLIT.write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {SPLIT} {l1a.sha(SPLIT)}: clusters {len(cl)}, E {len(e_files)} img / {len(e_ids)} QA, "
          f"C {rec['C']['n_images']} img / {rec['C']['n_qa']} QA; stage {a.stage}")


# ------------------------------------------------------------------------------------------------ M2 side
def check_pin(path: Path, pin: str | None) -> None:
    if pin is None or not path.is_file() or l1a.sha(path) != pin:
        raise SystemExit(f"{path} is not pinned or differs from its pin")


def pinned(path: Path, pin: str | None) -> dict:
    check_pin(path, pin)
    return json.loads(path.read_text(encoding="utf-8"))


def gates_open(keys: tuple[str, ...] = ("G1", "G3")) -> list[str]:
    """CC-165 r4 / CC-168 W3: no L1-b GPU step before G1 (W7 sweep) and G3 (ViTextVQA terms) are closed by a LOG
    line; G3_gemma (the human click-accept of the Gemma Terms) gates gemma3_4b only."""
    g = json.loads(GATES.read_text(encoding="utf-8")) if GATES.is_file() else {}
    return [k for k in keys if not re.fullmatch(r"(OPS|CC|PI)-\d{4}[A-Za-z0-9-]*", str(g.get(k) or ""))]


def pins_complete(m: dict) -> bool:
    """Every pinned file has a real hash (gated repos hide LFS sha256 until access is granted; CC-168 W1)."""
    return all(re.fullmatch(r"[0-9a-f]{64}" if f["kind"] == "sha256" else r"[0-9a-f]{40}", str(f["hash"] or ""))
               for f in m["files"].values())


def nonqwen_ok(key: str) -> list[str]:
    """Why a non-Qwen backbone may not be fetched or run (empty = allowed). gemma3_4b needs G3_gemma and full pins."""
    m = pinned(L1B_REG, L1B_REG_SHA256)["models"][key]
    why = [] if pins_complete(m) else ["pins incomplete"]
    return why + ([f"gate {g} open" for g in gates_open(("G3_gemma",))] if key == "gemma3_4b" else [])


def stage_problems(stage: Path, split: dict, ncs: Path) -> list[str]:
    """Exactly the E images at their l1a shas, grey.png, questions.jsonl (E rows, no answers), preds/ (3 L1-a img
    preds); no C or train image, no zip, no test file anywhere under NCS_DATA."""
    want = {f: l1a.pinned_lists()["dev"]["image_sha256"][f] for f in split["E"]["files"]}
    have = {p.name for p in (stage / "images").iterdir()} if (stage / "images").is_dir() else set()
    bad = [] if have == set(want) else [f"images: {len(have - set(want))} extra, {len(set(want) - have)} missing"]
    if not bad:
        bad += [f"image {f} sha" for f, h in want.items() if l1a.sha(stage / "images" / f) != h]
    top = {p.name for p in stage.iterdir()} if stage.is_dir() else set()
    if top != {"images", "grey.png", "questions.jsonl", "preds"}:
        bad.append(f"stage top level {sorted(top)}")
    for f, h in (("grey.png", split["stage"]["grey_png_sha256"]), ("questions.jsonl", split["stage"]["questions_sha256"])):
        if not (stage / f).is_file() or l1a.sha(stage / f) != h:
            bad.append(f"{f} sha")
    pr = {p.name for p in (stage / "preds").iterdir()} if (stage / "preds").is_dir() else set()
    if pr != {f"l1a_{m}_img.preds.json" for m in QWEN}:
        bad.append(f"preds {sorted(pr)}")
    bad += [f"preds {m}" for m, h in split["stage"]["preds_sha256"].items()
            if (stage / "preds" / f"l1a_{m}_img.preds.json").is_file()
            and l1a.sha(stage / "preds" / f"l1a_{m}_img.preds.json") != h]
    lists = l1a.pinned_lists()["dev"]["image_sha256"]
    c_sha = {lists[f] for f in split["C"]["files"]}
    for p in ncs.rglob("*"):
        n = p.name.lower()
        if "vitextvqa" in n and (n.endswith(".zip") or "test" in n or "train" in n) or n == "st_images":
            bad.append(f"forbidden {p}")
        elif n.endswith((".jpg", ".jpeg", ".png")) and p.is_file() and l1a.sha(p) in c_sha:
            bad.append(f"C image {p}")  # CC-168 W12: a confirm-half image anywhere under NCS_DATA
    return bad


def cmd_guard(a) -> None:
    import b1
    import common as K

    if K.host_ok(a.head) != l1a.ROLE:
        raise SystemExit(f"REFUSED: L1-b runs only where /root/.vsps_machine_id is {l1a.ROLE} (M2)")
    check_pin(PREREG, PREREG_SHA256)
    bad = [f"gate {g} open" for g in gates_open()]
    bad += stage_problems(a.stage, pinned(SPLIT, SPLIT_SHA256), Path(os.environ.get("NCS_DATA", "/root/ncs-data")))
    lock = Path(os.environ.get("L1B_LOCK", "/root/outputs/l1b/RUNNING"))
    bad += [x for x in b1.isolation() if x != f"lock {lock} exists"]
    if bad:
        raise SystemExit(f"REFUSED: {bad[:5]}")
    print("guard ok")


def model_spec(key: str) -> dict:
    if key in QWEN:
        return l1a.registry()["models"][key]
    if nonqwen_ok(key):
        raise SystemExit(f"REFUSED {key}: {nonqwen_ok(key)}")
    return pinned(L1B_REG, L1B_REG_SHA256)["models"][key]


def snap_dir(key: str) -> Path:
    return l1a.snap_dir(key) if key in QWEN else Path(f"/root/ncs-data/models/l1b_{key}")


def cmd_fetch(a) -> None:
    import decode_hf_vlm as D
    from huggingface_hub import snapshot_download

    m = model_spec(a.model)
    snapshot_download(m["hub_id"], revision=m["revision"], local_dir=a.snapshot, allow_patterns=sorted(m["files"]))
    print(f"{a.model}: {D.check_snapshot(m, a.snapshot)} pinned files ok")


def load_checked(key: str, snapshot: Path):
    import decode_hf_vlm as D

    if l1a.sha(Path(D.__file__)) != l1a.LB_DECODER_SHA256:
        raise SystemExit("scripts/lb/decode_hf_vlm.py differs from its pin")
    if D.packages() != l1a.registry()["venv"]["packages"]:
        raise SystemExit(f"packages {D.packages()} differ from the B-N1 registry venv")
    m = model_spec(key)
    D.check_snapshot(m, snapshot)
    return m, *D.load(m, snapshot, "cuda:0")


def e_rows(stage: Path) -> list[dict]:
    split = pinned(SPLIT, SPLIT_SHA256)
    rows = [json.loads(x) for x in (stage / "questions.jsonl").read_text(encoding="utf-8").splitlines()]
    if l1a.sha(stage / "questions.jsonl") != split["stage"]["questions_sha256"] or \
            [str(r["qa_id"]) for r in rows] != split["E"]["qa_ids_in_order"]:
        raise SystemExit("questions.jsonl differs from l1b_split.json")
    return rows


def write_json(out: Path, body: dict) -> None:
    tmp = out.with_name(out.name + ".tmp")
    tmp.write_text(json.dumps(body, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    tmp.replace(out)
    Path(str(out) + ".sha256").write_text(f"{l1a.sha(out)}  {out.name}\n", encoding="utf-8")


def prov(key: str, m: dict) -> dict:
    import decode_hf_vlm as D
    import torch

    return {"model": key, "hub_id": m["hub_id"], "revision": m["revision"], "l1b_sha256": l1a.sha(Path(__file__)),
            "split_sha256": SPLIT_SHA256, "prereg_sha256": PREREG_SHA256,
            "prompt_sha256": hashlib.sha256(l1a.PROMPT.encode()).hexdigest(), "packages": D.packages(),
            "machine_id": os.environ.get("VSPS_MACHINE_ID"), "git_head": D.git("rev-parse", "HEAD"),
            "job_sha256": os.environ.get("VSPS_JOB_SHA256"), "gpu": torch.cuda.get_device_name(0)}


def cmd_decode(a) -> None:
    """The non-Qwen backbone's first-pass answers on E: l1a's pinned prompt, greedy, 48 new tokens, the decode harness."""
    import decode_hf_vlm as D

    if a.model not in NONQWEN:
        raise SystemExit("the Qwen-family first passes are the L1-a img preds (no re-decode)")
    rows = e_rows(a.stage)
    m, proc, net = load_checked(a.model, a.snapshot)
    items = l1a.items_for(rows, "img", "")
    gen = l1a.with_questions(D.make_generate(proc, net, l1a.PROMPT, l1a.MAX_NEW, a.stage), rows)
    rid = f"l1b_{a.model}_img"
    out = a.out_dir / f"{rid}.preds.json"
    kw = {"max_new_tokens": l1a.MAX_NEW, "do_sample": False, "num_beams": 1}
    key = D.run_key(l1a.sha(Path(__file__)), {"run_id": rid, "split": SPLIT_SHA256}, m, kw, l1a.PROMPT, items)
    res = D.decode_slices(items, m["batch_size"], gen, Path(str(out) + ".partial.jsonl"), key)
    write_json(out, {"schema": "vsps.l1b_decode.v1", **prov(a.model, m), "generate_kwargs": kw, "n": len(res),
                     "generation_config": net.generation_config.to_diff_dict(),
                     "predictions": {r["image_id"]: r["caption"] for r in res},
                     "hit_max": {r["image_id"]: r["hit_max"] for r in res}})
    print(f"wrote {out}")


def encode(proc, net, image, text: str):
    msgs = [[{"role": "user", "content": [{"type": "image", "image": image}, {"type": "text", "text": text}]}]]
    return proc.apply_chat_template(msgs, add_generation_prompt=True, tokenize=True, return_dict=True,
                                    return_tensors="pt").to(net.device, net.dtype)


def score_full(net, enc, cont: list[int]) -> float:
    """Reference: one forward of prefix + continuation, no cache (the parity check)."""
    import torch

    P = enc["input_ids"].shape[1]
    x = dict(enc)
    tail = torch.tensor([cont], device=net.device)
    for k, v in enc.items():
        if torch.is_tensor(v) and v.dim() == 2 and v.shape == enc["input_ids"].shape:
            pad = tail if k == "input_ids" else torch.ones_like(tail) if k == "attention_mask" else torch.zeros_like(tail)
            x[k] = torch.cat([v, pad.to(v.dtype)], 1)
    with torch.no_grad():
        lp = net(**x, use_cache=False).logits[0, P - 1:-1].float().log_softmax(-1)
    return float(lp[torch.arange(len(cont)), tail[0]].sum())


def score_cached(net, enc, conts: list[list[int]], batch: int) -> list[float]:
    """Sum log p(continuation | image, prompt): one prefill, then the continuations in batches on a copy of the
    prefix cache (right-padded; padding sits after every scored token, so it is never attended by them)."""
    import torch

    P = enc["input_ids"].shape[1]
    with torch.no_grad():
        o = net(**enc, use_cache=True)
    first, cache = o.logits[0, -1].float().log_softmax(-1), o.past_key_values
    inner = next((x for x in (getattr(net, "model", None), net) if getattr(x, "rope_deltas", None) is not None), None)
    rd = inner.rope_deltas if inner is not None else None  # Qwen M-RoPE prefix state (1, 1); None for 1-D RoPE models
    out = []
    for i in range(0, len(conts), batch):
        ch = conts[i:i + batch]
        L, B = max(map(len, ch)), len(ch)
        ids = torch.tensor([c + [c[-1]] * (L - len(c)) for c in ch], device=net.device)
        c = copy.deepcopy(cache)
        c.batch_repeat_interleave(B)
        if rd is not None:  # AMENDMENT_1: expand with the cache (transformers 4.57.6 qwen2_5_vl repeats a (1, 1) delta on dim 1)
            inner.rope_deltas = rd.repeat_interleave(B, 0)
        with torch.no_grad():
            lp = net(input_ids=ids, attention_mask=torch.ones(B, P + L, dtype=torch.long, device=net.device),
                     past_key_values=c, cache_position=torch.arange(P, P + L, device=net.device),
                     use_cache=True).logits.float().log_softmax(-1)
        for b, cc in enumerate(ch):
            s = first[cc[0]] + sum(lp[b, t - 1, cc[t]] for t in range(1, len(cc)))
            out.append(float(s))
        del c, lp
    return out


def load_base(path: Path, key: str, e_ids: list[str]) -> dict[str, str]:
    """First-pass answers on E: the L1-a img preds (Qwen family; sha-pinned) or the l1b decode (non-Qwen)."""
    side_ = Path(str(path) + ".sha256")
    if key in QWEN:
        if l1a.sha(path) != L1A_IMG_SHA[key]:
            raise SystemExit(f"{path}: sha differs from OPS-1029q")
    elif not side_.exists() or side_.read_text().split()[0] != l1a.sha(path):
        raise SystemExit(f"{path}: sha256 sidecar missing or differs")
    p = json.loads(path.read_text(encoding="utf-8"))["predictions"]
    if not set(e_ids) <= set(p):
        raise SystemExit(f"{path}: E items missing")
    return {i: p[i] for i in e_ids}


def cmd_rerank(a) -> None:
    """Per E item: the variant answers' log-likelihoods with the real image and with the grey image (index 0 = the
    first-pass answer). Resumable per item (fsynced jsonl, same run key). A parity failure on the first items writes
    PARITY_FAIL and exits 3: the backbone is NOT_ASSESSABLE (PREREG §4.4), never silently re-run another way."""
    import torch
    from PIL import Image

    rows = e_rows(a.stage)
    ids = [str(r["qa_id"]) for r in rows]
    base = load_base(a.base, a.model, ids)
    m, proc, net = load_checked(a.model, a.snapshot)
    bs = pinned(L1B_REG, L1B_REG_SHA256)["cand_batch"][a.model]
    tok = proc.tokenizer
    grey = Image.open(a.stage / "grey.png").convert("RGB")
    out = a.out_dir / f"l1b_{a.model}_rerank.jsonl"
    key = hashlib.sha256(json.dumps([l1a.sha(Path(__file__)), SPLIT_SHA256, l1a.sha(a.base), m["revision"], bs])
                         .encode()).hexdigest()
    done, lines = set(), []
    if out.exists():
        lines = out.read_text(encoding="utf-8").splitlines()
        if not lines or json.loads(lines[0]).get("key") != key:
            raise SystemExit(f"{out}: run key differs; never mixed")
        good = []
        for x in lines[1:]:
            try:
                good.append(json.loads(x))
            except json.JSONDecodeError:
                break  # torn last line
        done = {g["qa_id"] for g in good}
        out.write_text("".join(json.dumps(g, ensure_ascii=False) + "\n" for g in [json.loads(lines[0])] + good),
                       encoding="utf-8")
    else:
        out.write_text(json.dumps({"key": key, **prov(a.model, m)}) + "\n", encoding="utf-8")
    t_par = []
    with out.open("a", encoding="utf-8") as fh:
        for n, r in enumerate(rows):
            q = str(r["qa_id"])
            if q in done and n >= PARITY_N:
                continue
            b, cands = candidates(base[q])
            conts = [tok(s, add_special_tokens=False)["input_ids"] or [tok.eos_token_id] for s in [b] + [c[3] for c in cands]]
            img = Image.open(a.stage / "images" / r["file"]).convert("RGB")
            text = l1a.PROMPT.format(q=r["question"])
            sc = {}
            for arm, im in (("img", img), ("grey", grey)):
                enc = encode(proc, net, im, text)
                sc[arm] = score_cached(net, enc, conts, bs)
                if n < PARITY_N and arm == "img":
                    ref = [score_full(net, enc, c) for c in conts[:PARITY_K]]
                    t_par.append(max(abs(x - y) for x, y in zip(ref, sc[arm])))
            if n == PARITY_N - 1 and max(t_par) > PARITY_TOL:
                (a.out_dir / f"l1b_{a.model}_PARITY_FAIL.json").write_text(json.dumps({"max_abs_nats": t_par}) + "\n")
                raise SystemExit(3)
            if q in done:
                continue
            fh.write(json.dumps({"qa_id": q, "n": len(cands), "cand_sha256": cand_sha(b, cands), "img": sc["img"],
                                 "grey": sc["grey"]}) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
            if n % 200 == 0:
                print(f"{n}/{len(rows)} {torch.cuda.max_memory_allocated() / 2**30:.1f} GiB", flush=True)
    (a.out_dir / f"l1b_{a.model}_parity.json").write_text(json.dumps({"max_abs_nats": t_par, "tol": PARITY_TOL}) + "\n")
    Path(str(out) + ".sha256").write_text(f"{l1a.sha(out)}  {out.name}\n", encoding="utf-8")
    print(f"wrote {out}")


# ------------------------------------------------------------------------------------------------ score (laptop)
def em(gold: str, pred: str, view: str = "contained") -> bool:
    return l1a.classify(gold, pred, view)["cls"] == "correct"


def oracle_ok(gold: str, base: str, cands: list) -> bool:
    """Descriptive ceiling: the base answer is diac (contained) and every syllable that differs in the best window has
    the gold signature among its candidates (gold used as an oracle; never a selection input)."""
    r = l1a.classify(gold, base)
    if r["cls"] != "diac":
        return False
    P = [l1a.sig(t) for t in l1a.tokens(base)]
    j = next(j for j in range(len(P)) if P[j:j + len(r["win"])] == r["win"])
    G = [l1a.sig(t) for t in l1a.tokens(gold)]
    have = {(k, l1a.sig(c[3][c[1]:c[2] + len(c[3]) - len(base)].lower())) for c in cands for k in [c[0]]}
    return all(G[i] == P[j + i] or (j + i, G[i]) in have for i in range(len(G)))


def outcome(rows: dict[str, dict]) -> tuple[str, str]:
    """PREREG §6, clauses in order. rows: backbone -> {assessable, nonqwen, d, lo, d_text, flips_bad, flips_good}."""
    ok = {k: r for k, r in rows.items() if r["assessable"]}
    if len(ok) < 3 or not any(r["nonqwen"] for r in ok.values()):
        return "NO_VERDICT", f"{len(ok)} assessable, non-Qwen assessable: {any(r['nonqwen'] for r in ok.values())}"
    fail = [k for k, r in ok.items() if r["d"] < SESOI or r["lo"] <= 0]
    if len(fail) >= 2:
        return "KILL", f"dEM < {SESOI} or CI_lo <= 0 on {fail}"

    def passes(r, thr):
        return r["d"] >= thr and r["lo"] > 0 and r["flips_bad"] <= HARM * r["flips_good"]

    for thr, name in ((STRONG, "GO_STRONG"), (SESOI, "GO")):
        win = [k for k, r in ok.items() if passes(r, thr)]
        if len(win) >= 3 and any(ok[k]["nonqwen"] for k in win):
            img = [k for k in win if ok[k]["d"] - ok[k]["d_text"] >= PRIOR_MARGIN]
            if len(img) >= 3 and any(ok[k]["nonqwen"] for k in img):
                return name, f"dEM >= {thr}, CI_lo > 0, harm guard and image margin on {img}"
            return "PRIOR_ONLY", f"{name} gains on {win} but dEM - dEM(T*) < {PRIOR_MARGIN} on {sorted(set(win) - set(img))}"
    return "INCONCLUSIVE", "neither KILL nor GO; judge"


def check_prov(head: dict, o: Path, f: Path, l1b_sha: str | None = None) -> None:
    """CC-168 W4b: the GPU file was written by the pinned l1b.py / job under this prereg and split (l1b_sha: the
    l1b.py sha a pinned reused file was written by, AMENDMENT_1 §4)."""
    start = {Path(x.split()[1]).name: x.split()[0] for x in (o / "code_at_start.sha256").read_text().splitlines()}
    want = {"split_sha256": SPLIT_SHA256, "prereg_sha256": PREREG_SHA256, "l1b_sha256": l1b_sha or start.get("l1b.py"),
            "job_sha256": start.get("l1b_job.sh")}
    bad = {k: head.get(k) for k, v in want.items() if v is None or head.get(k) != v}
    if bad or start.get("l1b.py") != l1a.sha(Path(__file__)):
        raise SystemExit(f"{f}: provenance differs {bad}")


def cmd_score(a) -> None:
    import numpy as np

    if OUT.exists():
        raise SystemExit(f"{OUT} exists; scored once")
    check_pin(PREREG, PREREG_SHA256)
    split = pinned(SPLIT, SPLIT_SHA256)
    dv = l1a.load_src("dev")
    gold = {str(x["id"]): x["answers"][0] for x in dv["annotations"]}
    img_of = {str(x["id"]): x["image_id"] for x in dv["annotations"]}
    ids = split["E"]["qa_ids_in_order"]
    strat = {str(i) for i in l1a.pinned_lists()["dev"]["mark_bearing_stratum"]}
    e1 = set(split["E"]["e1_files"])
    fn = {str(i["id"]): i["filename"] for i in dv["images"]}
    fold = np.array([fn[str(img_of[i])] in e1 for i in ids])
    imgs = sorted({img_of[i] for i in ids})
    idx = np.array([imgs.index(img_of[i]) for i in ids])
    rng = np.random.default_rng(l1a.SEED).integers(0, len(imgs), (l1a.B, len(imgs)))
    configs = [("M", al, t) for al in ALPHA for t in TAU] + [("T", None, t) for t in TAU]
    per, meta, cs_all = {}, {}, {}
    for k in MODELS:
        bp = L1A_PREDS / f"l1a_{k}_img.preds.json" if k in QWEN else a.out_dir / f"l1b_{k}_img.preds.json"
        rp = a.out_dir / f"l1b_{k}_rerank.jsonl"
        if not bp.exists() or not rp.exists() or (a.out_dir / f"l1b_{k}_PARITY_FAIL.json").exists():
            meta[k] = {"assessable": False, "why": "missing or parity fail"}
            continue
        side_ = Path(str(rp) + ".sha256")
        if not side_.exists() and (a.out_dir.parent / "CAP_STOP.json").exists():
            meta[k] = {"assessable": False, "why": "incomplete (cap stop)"}  # CC-168 W4a
            continue
        if not side_.exists() or side_.read_text().split()[0] != l1a.sha(rp):
            raise SystemExit(f"{rp}: sidecar missing or differs (and no CAP_STOP.json)")
        lines = rp.read_text(encoding="utf-8").splitlines()
        check_prov(json.loads(lines[0]), a.out_dir.parent, rp)
        if k in NONQWEN:
            pin = REUSE_DEC.get(k, ("", ""))
            check_prov(json.loads(bp.read_text(encoding="utf-8")), a.out_dir.parent, bp,
                       pin[1] if l1a.sha(bp) == pin[0] else None)
        rr = {x["qa_id"]: x for x in map(json.loads, lines[1:])}
        base = load_base(bp, k, ids)
        if set(rr) != set(ids):
            meta[k] = {"assessable": False, "why": f"rerank n {len(rr)} != {len(ids)}"}
            continue
        cs = {}
        for i in ids:
            b, c = candidates(base[i])
            if cand_sha(b, c) != rr[i]["cand_sha256"]:
                raise SystemExit(f"{k} {i}: candidate list differs from the GPU side")
            cs[i] = (b, c)
        base_ok = np.array([em(gold[i], cs[i][0]) for i in ids])
        diac0 = sum(i in strat and l1a.classify(gold[i], cs[i][0])["cls"] == "diac" for i in ids)
        hm = json.loads(bp.read_text(encoding="utf-8")).get("hit_max", {})
        m = {"nonqwen": k in NONQWEN, "n": len(ids), "base_em": float(base_ok.mean()),
             "empty": float(np.mean([not l1a.tokens(cs[i][0]) for i in ids])),
             "hit_max": float(np.mean([bool(hm.get(i)) for i in ids])), "diac_stratum_base": int(diac0),
             "n_cands_mean": float(np.mean([len(cs[i][1]) for i in ids])),
             "n_no_cands": sum(not cs[i][1] for i in ids),
             "n_truncated_answers": sum(n_truncated(*cs[i]) > 0 for i in ids),
             "oracle_em": float(np.mean([base_ok[n] or oracle_ok(gold[i], *cs[i]) for n, i in enumerate(ids)]))}
        m["assessable"] = m["empty"] <= 0.2 and m["hit_max"] <= 0.05 and (
            k in QWEN or (m["base_em"] >= NQ_MIN_EM and diac0 >= NQ_MIN_DIAC))
        meta[k] = m
        per[k] = {}
        for cfg in configs:
            out = [choose(*cs[i], rr[i]["img"], rr[i]["grey"], cfg[1] or 0.0, cfg[2], cfg[0] == "T") for i in ids]
            per[k][cfg] = (np.array([em(gold[i], o) for i, o in zip(ids, out)]),
                           np.array([em(gold[i], o, "strict") for i, o in zip(ids, out)]),
                           sum(i in strat and l1a.classify(gold[i], o)["cls"] == "diac" for i, o in zip(ids, out)))
        per[k]["base_strict"] = np.array([em(gold[i], cs[i][0], "strict") for i in ids])
        per[k]["base"] = base_ok
        cs_all[k] = cs
    nq = [k for k in NONQWEN if meta.get(k, {}).get("assessable")][:1]  # the primary if assessable, else the fallback
    use = [k for k in QWEN if meta[k].get("assessable")] + nq

    def d_em(k, cfg, mask=None):
        mask = np.ones(len(ids), bool) if mask is None else mask
        return 100 * (per[k][cfg][0][mask].mean() - per[k]["base"][mask].mean())

    def pick(kind, mask=None):  # PREREG §5.3: max mean dEM over the used backbones; ties -> smaller alpha, larger tau
        cand = [c for c in configs if c[0] == kind]
        return max(cand, key=lambda c: (round(float(np.mean([d_em(k, c, mask) for k in use])), 9) if use else 0,
                                        -(c[1] or 0), c[2]))

    w, wt = (pick("M"), pick("T")) if use else (None, None)
    rows, res = {}, {}
    one = np.ones(len(ids))
    for k in MODELS:
        if k not in use:
            continue
        mo, ms, md = per[k][w]
        pt, lo, hi = l1a.boot_diff(mo.astype(float), one, per[k]["base"].astype(float), one, idx, rng)
        cross = []
        for f in (True, False):  # cross-fit: select on one E half, evaluate on the other (descriptive)
            c = pick("M", fold == f)
            cross.append(d_em(k, c, fold != f))
        rows[k] = {"assessable": True, "nonqwen": k in NONQWEN, "d": 100 * pt, "lo": 100 * lo,
                   "d_text": d_em(k, wt), "flips_good": int((mo & ~per[k]["base"]).sum()),
                   "flips_bad": int((~mo & per[k]["base"]).sum())}
        res[k] = {**meta[k], **rows[k], "hi": 100 * hi, "d_strict": 100 * (ms.mean() - per[k]["base_strict"].mean()),
                  "diac_stratum_method": int(md),
                  "diac_reduction": 1 - md / meta[k]["diac_stratum_base"] if meta[k]["diac_stratum_base"] else None,
                  "ceiling_markblind_minus_base": 100 * float(np.mean([
                      l1a.classify(gold[i], cs_all[k][i][0])["cls"] != "base" for i in ids]) - per[k]["base"].mean()),
                  "crossfit_d": cross,
                  "grid": {f"{c[0]}:{c[1]}:{c[2]}": d_em(k, c) for c in configs}}
    for k in MODELS:
        if k not in use:
            res[k] = meta.get(k, {"assessable": False})
            rows[k] = {"assessable": False, "nonqwen": k in NONQWEN}
    oc, why = outcome({k: r for k, r in rows.items() if k in use or not r["assessable"]})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"schema": "vsps.l1b_decide.v1", "prereg_sha256": PREREG_SHA256,
                               "split_sha256": SPLIT_SHA256, "outcome": oc, "reason": why,
                               "selected": {"M": list(w) if w else None, "T": list(wt) if wt else None},
                               "nonqwen_used": nq, "n_E": len(ids), "backbones": res}, indent=1) + "\n",
                   encoding="utf-8")
    print(f"wrote {OUT} {l1a.sha(OUT)}: {oc} ({why})")


# ------------------------------------------------------------------------------------------------ selftest
def selftest() -> None:
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

    sigs = lambda vs: {l1a.sig(v.lower()) for v in vs}
    check("tone placement: hoa + huyền -> hòa (old style, open oa)", "hòa" in variants("hoa"))
    check("tone placement: toan + sắc -> toán (final consonant)", "toán" in variants("toan"))
    check("tone placement: qu is a consonant (quã)", "quã" in variants("qua"))
    check("tone placement: gi + vowel (già)", "già" in variants("gia"))
    check("tone placement: ươ takes it on ơ (người)", "người" in variants("nguoi"))
    check("tone placement: three vowels -> middle (ngoài)", "ngoài" in variants("ngoai"))
    v = variants("ban")
    check("tones x vowel marks: ban -> bàn, bán, bạn, bân, bằn (all distinct signatures)",
          {"bàn", "bán", "bạn", "bân", "bằn"} <= set(v) and len(sigs(v)) == len(v) == 3 * 6 - 1)
    check("own signature removed", l1a.sig("ban") not in sigs(v) and l1a.sig("bàn") not in sigs(variants("bàn")))
    check("stop-final rule: bat takes only sắc / nặng", all(l1a.sig(x)[2] in ("sac", "nang") for x in variants("bat"))
          and len(variants("bat")) == 3 * 2)
    check("case kept: Ban -> Bàn", "Bàn" in variants("Ban") and all(x[0] == "B" for x in variants("Ban")))
    check("đ is never changed (base letter)", all("đ" in x for x in variants("đi")) and not any(
        "d" == x[0] for x in variants("đi")))
    check("digits and vowel-less syllables get no candidates", variants("12a") == [] and variants("str") == [])
    check("bare qu- has no tone-bearing vowel: no candidates (AMENDMENT_1)",
          variants("qu") == variants("Qư") == [] and "quà" in variants("qua") and "gì" in variants("gi"))
    check("NFD input = NFC input", variants(unicodedata.normalize("NFD", "hòa")) == variants("hòa"))
    b, c = candidates("Đó là bàn.")
    check("candidates: one syllable changed at a time, punctuation kept",
          b == "Đó là bàn." and all(x[3].endswith(".") and len(l1a.tokens(x[3])) == 3 for x in c)
          and {x[0] for x in c} == {0, 1, 2})
    big = candidates(" ".join(["nguoi"] * 40))[1]
    check("MAX_CAND: whole syllables only, never over 256", len(big) <= MAX_CAND and len({x[0] for x in big}) > 1)
    # choose: index 0 = base, gains per syllable
    b, c = "ban an", [(0, 0, 3, "bàn an"), (0, 0, 3, "bán an"), (1, 4, 6, "ban ăn")]
    check("choose: best variant per syllable over tau", choose(b, c, [0, 2, 1, 3], [0, 0, 0, 0], 0, 0.5) == "bàn ăn")
    check("choose: tau blocks small gains", choose(b, c, [0, 0.4, 0.1, 0.3], [0, 0, 0, 0], 0, 0.5) == b)
    check("choose: alpha subtracts the grey (prior) gain", choose(b, c, [0, 2, 1, 0], [0, 2, 0, 0], 1.0, 0.5) == "bán an")
    check("choose: T uses only the grey gain", choose(b, c, [0, 9, 0, 0], [0, 0, 1, 0], 0, 0.5, True) == "bán an")
    check("choose: a variant of different length keeps the rest intact",
          choose("a nguoi b", [(1, 2, 7, "a người b")], [0, 1], [0, 0], 0, 0) == "a người b")
    # outcome, both directions
    R = lambda d, lo, nq=False, dt=0.0, bad=0, good=10: {"assessable": True, "nonqwen": nq, "d": d, "lo": lo,
                                                          "d_text": dt, "flips_bad": bad, "flips_good": good}
    check("KILL: two backbones under SESOI", outcome({"a": R(0.5, 0.1), "b": R(0.9, 0.2), "c": R(3, 1),
                                                      "g": R(3, 1, True)})[0] == "KILL")
    check("KILL: CI_lo <= 0 counts as a failure", outcome({"a": R(1.5, 0), "b": R(1.2, -0.1), "c": R(3, 1),
                                                           "g": R(3, 1, True)})[0] == "KILL")
    check("GO_STRONG: >= 2 on 3 incl. non-Qwen", outcome({"a": R(2.5, 1), "b": R(0.5, 0.1), "c": R(2.1, 0.5),
                                                          "g": R(2.2, 0.4, True)})[0] == "GO_STRONG")
    check("GO: >= 1 on 3 incl. non-Qwen", outcome({"a": R(1.5, 0.2), "b": R(1.1, 0.1), "c": R(2.5, 1),
                                                   "g": R(1.2, 0.1, True)})[0] == "GO")
    check("GO needs the non-Qwen backbone among the passes", outcome({"a": R(1.5, 0.2), "b": R(1.1, 0.1),
                                                                      "c": R(2.5, 1), "g": R(1.2, 0.1, True, bad=9)})[0]
          == "INCONCLUSIVE")
    check("PRIOR_ONLY: the text-only baseline gets the same gain", outcome(
        {"a": R(1.5, 0.2, dt=1.4), "b": R(1.1, 0.1, dt=1.0), "c": R(2.5, 1), "g": R(1.2, 0.1, True, 1.0)})[0]
        == "PRIOR_ONLY")
    check("harm guard: flips to wrong > 25% of flips to right blocks a pass", outcome(
        {"a": R(1.5, 0.2, bad=3), "b": R(1.1, 0.1, bad=3), "c": R(2.5, 1), "g": R(1.2, 0.1, True)})[0]
        == "INCONCLUSIVE")
    check("NO_VERDICT without an assessable non-Qwen backbone", outcome(
        {"a": R(3, 1), "b": R(3, 1), "c": R(3, 1), "g": {"assessable": False, "nonqwen": True}})[0] == "NO_VERDICT")
    # oracle
    check("oracle: diac base with the gold variant in the set", oracle_ok("bàn", "ban", candidates("ban")[1]))
    check("oracle: a base error is never reachable", not oracle_ok("bàn", "bút", candidates("bút")[1]))
    # split
    check("split side is deterministic and salted", side("123.jpg") == side("123.jpg") and
          len({side(f"{i}.jpg") for i in range(20)}) == 2)
    with tempfile.TemporaryDirectory() as t:
        g = Path(t) / "GATES.json"
        global GATES
        keep, GATES = GATES, g
        try:
            check("gates: missing file -> both open", gates_open() == ["G1", "G3"])
            g.write_text(json.dumps({"G1": "OPS-1030a", "G3": ""}))
            check("gates: an empty G3 stays open", gates_open() == ["G3"])
            g.write_text(json.dumps({"G1": "OPS-1030a", "G3": "PI-1030b"}))
            check("gates: both LOG ids -> closed", gates_open() == [])
            check("gates: G3_gemma empty -> gemma gated", gates_open(("G3_gemma",)) == ["G3_gemma"])
            g.write_text(json.dumps({"G1": "OPS-1030a", "G3": "PI-1029l", "G3_gemma": "PI-1030c"}))
            check("gates: G3_gemma filled -> gemma allowed", gates_open(("G3_gemma",)) == [])
        finally:
            GATES = keep
    check("pins: a null or masked LFS hash is incomplete", not pins_complete(
        {"files": {"w": {"kind": "sha256", "hash": None}, "c": {"kind": "git_blob", "hash": "0" * 40}}}) and
        not pins_complete({"files": {"w": {"kind": "sha256", "hash": "*" * 64}}}) and
        pins_complete({"files": {"w": {"kind": "sha256", "hash": "a" * 64}}}))
    check("n_truncated: syllables past the cap are counted", n_truncated(*candidates(" ".join(["nguoi"] * 40))) > 0
          and n_truncated(*candidates("ban an")) == 0)
    refused("check_pin refuses an unset pin", lambda: check_pin(PREREG, None))
    refused("check_pin refuses a wrong pin", lambda: check_pin(PREREG, "0" * 64))
    try:
        import numpy as np

        feats = [("s1", 0, 0, 0, 0, np.array([1.0, 0])), ("s2", 2**63, 2**63, 2**63, 2**63, np.array([0.99, 0.141])),
                 ("s3", 2**62, 2**62, 2**62, 2**62, np.array([0, 1.0]))]
        check("clusters: an SSCD copy joins its pair, an unrelated image stays alone",
              clusters(["1.jpg", "2.jpg", "3.jpg"], feats) == [["1.jpg", "2.jpg"], ["3.jpg"]])
    except ImportError:
        print("SKIP clusters: numpy not installed")
    ok += selftest_score()
    ok += selftest_tiny()
    print("\n".join("PASS " + n for n in ok) + f"\n{len(ok)} ok")


def cmd_nqok(a) -> None:
    why = nonqwen_ok(a.model)
    print(f"{a.model}: {why or 'ok'}")
    sys.exit(1 if why else 0)


def selftest_score() -> list[str]:
    """CC-168 W5: cmd_score end to end on synthetic gold, preds and rerank rows (temp dir; module pins patched and
    restored). Image scores favour the gold variant, grey scores are flat: expect GO_STRONG, M* = (0, 2), T* no gain,
    and no answer string in decide.json."""
    try:
        import numpy  # noqa: F401
    except ImportError:
        print("SKIP score end to end: numpy not installed")
        return []
    import types

    g = globals()
    keep = {k: g[k] for k in ("PREREG", "PREREG_SHA256", "SPLIT", "SPLIT_SHA256", "OUT", "L1A_PREDS", "L1A_IMG_SHA",
                              "REUSE_DEC")}
    keep_l1a = (l1a.load_src, l1a.pinned_lists)
    golds = ["bàn ăn", "người", "xôi gấc", "12"]
    strip = lambda x: "".join(c for c in unicodedata.normalize("NFD", x) if not unicodedata.combining(c))
    ids = [str(i) for i in range(1, 81)]
    gold = {i: golds[n % 4] for n, i in enumerate(ids)}
    base = {i: strip(gold[i]) if n % 2 == 0 else gold[i] for n, i in enumerate(ids)}
    img_of = {i: 1000 + n // 2 for n, i in enumerate(ids)}
    files = {v: f"{v}.jpg" for v in img_of.values()}
    def run(mods, tweak=None, twice=False):
        """Synthetic outputs for `mods`, then tweak(tmp) if given, then cmd_score; returns (decide, text, refused)."""
        try:
            with tempfile.TemporaryDirectory() as t:
                t = Path(t)
                (t / "out").mkdir()
                (t / "l1a").mkdir()
                pre = t / "PREREG.md"
                pre.write_text("synthetic\n")
                sp = t / "split.json"
                sp.write_text(json.dumps({"E": {"qa_ids_in_order": ids,
                                                "e1_files": [files[v] for v in sorted(files)[:20]]}}))
                job = t / "l1b_job.sh"
                job.write_text("#\n")
                (t / "code_at_start.sha256").write_text(f"{l1a.sha(Path(__file__))}  scripts/l1b/l1b.py\n"
                                                         f"{l1a.sha(job)}  scripts/l1b/l1b_job.sh\n")
                head = {"split_sha256": l1a.sha(sp), "prereg_sha256": l1a.sha(pre),
                        "l1b_sha256": l1a.sha(Path(__file__)), "job_sha256": l1a.sha(job)}
                g.update(PREREG=pre, PREREG_SHA256=l1a.sha(pre), SPLIT=sp, SPLIT_SHA256=l1a.sha(sp),
                         OUT=t / "decide.json", L1A_PREDS=t / "l1a", L1A_IMG_SHA={})
                l1a.load_src = lambda name: {"annotations": [{"id": int(i), "image_id": img_of[i], "answers": [gold[i]]}
                                                             for i in ids],
                                             "images": [{"id": v, "filename": f} for v, f in files.items()]}
                l1a.pinned_lists = lambda: {"dev": {"mark_bearing_stratum": [int(i) for i in ids if gold[i] != "12"]}}
                for k in mods:
                    body = {**head, "predictions": base, "hit_max": {}}
                    bp = (t / "l1a" / f"l1a_{k}_img.preds.json") if k in QWEN else (t / "out" / f"l1b_{k}_img.preds.json")
                    bp.write_text(json.dumps(body, ensure_ascii=False))
                    Path(str(bp) + ".sha256").write_text(f"{l1a.sha(bp)}  x\n")
                    if k in QWEN:
                        L1A_IMG_SHA[k] = l1a.sha(bp)
                    rows = [json.dumps(head)]
                    for i in ids:
                        b, c = candidates(base[i])
                        G = [l1a.sig(x) for x in l1a.tokens(gold[i])]
                        img = [0.0] + [5.0 if l1a.sig(x[3][x[1]:x[2]].lower()) == G[x[0]] else -1.0 for x in c]
                        rows.append(json.dumps({"qa_id": i, "n": len(c), "cand_sha256": cand_sha(b, c), "img": img,
                                                "grey": [0.0] * len(img)}))
                    rp = t / "out" / f"l1b_{k}_rerank.jsonl"
                    rp.write_text("\n".join(rows) + "\n")
                    Path(str(rp) + ".sha256").write_text(f"{l1a.sha(rp)}  x\n")
                if tweak:
                    tweak(t)
                cmd_score(types.SimpleNamespace(out_dir=t / "out"))
                d = json.loads((t / "decide.json").read_text(encoding="utf-8"))
                txt = (t / "decide.json").read_text(encoding="utf-8")
                again = False
                if twice:
                    try:
                        cmd_score(types.SimpleNamespace(out_dir=t / "out"))
                    except SystemExit:
                        again = True
                return d, txt, again
        finally:
            g.update(keep)
            l1a.load_src, l1a.pinned_lists = keep_l1a

    def refuses(tweak) -> bool:
        try:
            run(MODELS[:4], tweak)
        except SystemExit:
            return True
        return False

    rp7 = lambda t: t / "out" / "l1b_qwen25vl_7b_rerank.jsonl"
    no_side = lambda t: Path(str(rp7(t)) + ".sha256").unlink()

    def cap_stop(t):
        no_side(t)
        (t / "CAP_STOP.json").write_text("{}\n")

    def bad_head(t):  # header l1b_sha256 differs from code_at_start; sidecar rewritten so only provenance differs
        lines = rp7(t).read_text(encoding="utf-8").splitlines()
        lines[0] = json.dumps({**json.loads(lines[0]), "l1b_sha256": "0" * 64})
        rp7(t).write_text("\n".join(lines) + "\n")
        Path(str(rp7(t)) + ".sha256").write_text(f"{l1a.sha(rp7(t))}  x\n")

    d, txt, again = run(MODELS[:4], twice=True)
    b7 = d["backbones"]["qwen25vl_7b"]
    if not (d["outcome"] == "GO_STRONG" and d["selected"]["M"] == ["M", 0.0, 2.0] and d["nonqwen_used"] == ["gemma3_4b"]
            and abs(b7["d"] - 50.0) < 1e-9 and b7["d_text"] == 0 and b7["flips_bad"] == 0 and len(b7["crossfit_d"]) == 2
            and not d["backbones"]["idefics3_8b"]["assessable"] and again
            and not any(x in txt for x in golds[:3] + [strip(x) for x in golds[:3]])):
        raise AssertionError(f"score end to end: {d['outcome']} {d['selected']} {b7.get('d')}")
    d2 = run(QWEN + ("idefics3_8b",))[0]  # CC-168b W19: gemma skipped, idefics3 in use (the path of this run)
    if not (d2["outcome"] == "GO_STRONG" and d2["nonqwen_used"] == ["idefics3_8b"]
            and not d2["backbones"]["gemma3_4b"]["assessable"] and d2["backbones"]["idefics3_8b"]["assessable"]):
        raise AssertionError(f"score without gemma: {d2['outcome']} {d2['nonqwen_used']}")
    d3 = run(MODELS[:4], cap_stop)[0]
    if d3["backbones"]["qwen25vl_7b"].get("why") != "incomplete (cap stop)":
        raise AssertionError("score: a missing sidecar under CAP_STOP.json is not NOT_ASSESSABLE")
    if not (refuses(no_side) and refuses(bad_head)):
        raise AssertionError("score: missing sidecar without CAP_STOP.json, or a header sha mismatch, not refused")

    def old_dec(t, pin_it):  # AMENDMENT_1 §4: the idefics3 decode was written by an earlier l1b.py
        bp = t / "out" / "l1b_idefics3_8b_img.preds.json"
        bp.write_text(json.dumps({**json.loads(bp.read_text(encoding="utf-8")), "l1b_sha256": "1" * 64}))
        Path(str(bp) + ".sha256").write_text(f"{l1a.sha(bp)}  x\n")
        g["REUSE_DEC"] = {"idefics3_8b": (l1a.sha(bp) if pin_it else "2" * 64, "1" * 64)}

    d4 = run(QWEN + ("idefics3_8b",), lambda t: old_dec(t, True))[0]
    try:
        run(QWEN + ("idefics3_8b",), lambda t: old_dec(t, False))
        unpinned = False
    except SystemExit:
        unpinned = True
    if not (d4["nonqwen_used"] == ["idefics3_8b"] and unpinned):
        raise AssertionError("score: the pinned reused decode is not accepted, or an unpinned old decode is not refused")
    return ["score end to end (synthetic): GO_STRONG, M* = (alpha 0, tau 2) by the tie rule, T* no gain, dEM 50.0, "
            "cross-fit rows, idefics3 absent -> not assessable, second run refused, no answer text in decide.json",
            "score without gemma (W19): idefics3_8b is the non-Qwen backbone in use, gemma not assessable",
            "score W4a/W4b (W19): sidecar missing + CAP_STOP -> incomplete; without CAP_STOP or with a header l1b sha "
            "mismatch -> refused",
            "score AMENDMENT_1 §4: a decode by an earlier l1b.py is accepted only when its sha and writer sha are pinned"]


def selftest_tiny() -> list[str]:
    """score_cached == score_full on a tiny random LLaVA (decode_hf_vlm's selftest pattern); skipped without torch."""
    try:
        import torch
        import transformers as tf
        from PIL import Image
        from tokenizers import Tokenizer, models, pre_tokenizers
    except ImportError:
        print("SKIP tiny model: torch/transformers not installed")
        return []
    torch.manual_seed(0)
    words = ["<unk>", "<pad>", "<s>", "</s>", "<image>", "USER:", "ASSISTANT:"] + [f"w{i}" for i in range(57)]
    tk = Tokenizer(models.WordLevel({w: i for i, w in enumerate(words)}, unk_token="<unk>"))
    tk.pre_tokenizer = pre_tokenizers.WhitespaceSplit()
    tok = tf.PreTrainedTokenizerFast(tokenizer_object=tk, unk_token="<unk>", pad_token="<pad>", bos_token="<s>",
                                     eos_token="</s>", additional_special_tokens=["<image>"],
                                     model_input_names=["input_ids", "attention_mask"])
    tpl = ("{% for m in messages %}USER: {% for c in m['content'] %}{% if c['type'] == 'image' %}<image> {% else %}"
           "{{ c['text'] }} {% endif %}{% endfor %}{% endfor %}{% if add_generation_prompt %}ASSISTANT:{% endif %}")
    proc = tf.LlavaProcessor(image_processor=tf.CLIPImageProcessor(size={"shortest_edge": 28},
                                                                     crop_size={"height": 28, "width": 28}),
                             tokenizer=tok, patch_size=14, vision_feature_select_strategy="default",
                             chat_template=tpl, num_additional_image_tokens=1)
    cfg = tf.LlavaConfig(
        vision_config=tf.CLIPVisionConfig(hidden_size=16, intermediate_size=32, num_hidden_layers=2,
                                          num_attention_heads=2, image_size=28, patch_size=14, projection_dim=16),
        text_config=tf.LlamaConfig(vocab_size=len(words), hidden_size=32, intermediate_size=64, num_hidden_layers=2,
                                   num_attention_heads=4, num_key_value_heads=2, max_position_embeddings=256,
                                   pad_token_id=1, bos_token_id=2, eos_token_id=3),
        image_token_index=4, vision_feature_select_strategy="default", vision_feature_layer=-1)
    net = tf.LlavaForConditionalGeneration(cfg).eval()
    enc = encode(proc, net, Image.new("RGB", (40, 30), (90, 120, 200)), "w5 w6 w7")
    conts = [[10, 11, 12], [13], [14, 15, 16, 17, 18], [10, 11, 20]]
    full = [score_full(net, enc, c) for c in conts]
    cached = score_cached(net, enc, conts, 3)
    if max(abs(x - y) for x, y in zip(full, cached)) > 1e-4:
        raise AssertionError(f"cached {cached} != full {full}")
    # AMENDMENT_1: Qwen2.5-VL M-RoPE (rope_deltas = -2 here) on a batch-repeated cache; crashes without the expansion
    qcfg = tf.Qwen2_5_VLConfig(
        vocab_size=64, hidden_size=32, intermediate_size=64, num_hidden_layers=2, num_attention_heads=4,
        num_key_value_heads=2, max_position_embeddings=256, rope_scaling={"type": "mrope", "mrope_section": [2, 1, 1]},
        vision_config={"depth": 1, "hidden_size": 16, "intermediate_size": 32, "num_heads": 2, "out_hidden_size": 32,
                       "patch_size": 2, "spatial_merge_size": 2, "temporal_patch_size": 2, "in_channels": 3,
                       "window_size": 4, "fullatt_block_indexes": [0]},
        image_token_id=60, video_token_id=63, vision_start_token_id=61, vision_end_token_id=62)
    qnet = tf.Qwen2_5_VLForConditionalGeneration(qcfg).eval()
    ids = [5, 6, 61] + [60] * 4 + [62, 7, 8]
    qenc = {"input_ids": torch.tensor([ids]), "attention_mask": torch.ones(1, len(ids), dtype=torch.long),
            "pixel_values": torch.randn(16, 24), "image_grid_thw": torch.tensor([[1, 4, 4]])}
    full = [score_full(qnet, qenc, c) for c in conts]
    cached = score_cached(qnet, qenc, conts, 3)
    if max(abs(x - y) for x, y in zip(full, cached)) > 1e-4:
        raise AssertionError(f"Qwen2.5-VL cached {cached} != full {full}")
    return ["tiny LLaVA: cached prefix + right-padded batches (3+1) = full forward, 4 continuations, < 1e-4 nats",
            f"tiny Qwen2.5-VL (transformers {tf.__version__}): M-RoPE rope_deltas expanded with the cache, batches "
            "(3+1) = full forward, < 1e-4 nats (AMENDMENT_1)"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("build")
    p.add_argument("--l1a-stage", type=Path, required=True)
    p.add_argument("--stage", type=Path, required=True)
    p = sub.add_parser("guard")
    p.add_argument("--head", required=True)
    p.add_argument("--stage", type=Path, required=True)
    p = sub.add_parser("lock")
    p.add_argument("--path", type=Path, required=True)
    p = sub.add_parser("left")
    p.add_argument("--used", type=Path, required=True)
    p.add_argument("--marker", type=Path, required=True)
    for name in ("snap", "fetch", "decode", "rerank"):
        p = sub.add_parser(name)
        p.add_argument("--model", choices=MODELS, required=True)
        if name != "snap":
            p.add_argument("--snapshot", type=Path, required=True)
        if name in ("decode", "rerank"):
            p.add_argument("--stage", type=Path, required=True)
            p.add_argument("--out-dir", type=Path, required=True)
        if name == "rerank":
            p.add_argument("--base", type=Path, required=True)
    p = sub.add_parser("nqok")
    p.add_argument("--model", choices=NONQWEN, required=True)
    p = sub.add_parser("score")
    p.add_argument("--out-dir", type=Path, required=True)
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
     "snap": lambda: print(snap_dir(a.model)), "fetch": lambda: cmd_fetch(a), "decode": lambda: cmd_decode(a),
     "rerank": lambda: cmd_rerank(a), "score": lambda: cmd_score(a), "nqok": lambda: cmd_nqok(a)}.get(a.cmd, ap.print_help)()


if __name__ == "__main__":
    main()
