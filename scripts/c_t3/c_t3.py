#!/usr/bin/env python3
"""Paper C, tier 3 (TEST, one look, C-T3) on Flickr30K Karpathy test. A copy of scripts/c_t2/c_t2.py (sha256 6113844a)
with the minimal change for manuscript/prereg/2026-10-31_c_t3/PREREG.md: f30k_test is admitted (SETS, extract, store,
items_of, embed) and nothing in Flickr30K is refused by name any more; on f30k_test only the frozen tier-3 runs can be
decoded (T3_RUN_IDS: no rand arm, no smoke); outputs go to /root/outputs/c_t3, cap 2.5 GPU-h; store, score and t3 refuse
a GPU host (CC-196 Codex fix 1); the `t3` command applies Holm over the tier-2 family (T2_DECISION e29bbe8a). Read the
change as `diff scripts/c_t2/c_t2.py scripts/c_t3/c_t3.py`. Tier-1/2 commands are kept and are not used by the C-T3 job.
The test-side near-duplicate pass is scripts/c_t3/c_t3_neardup.py (W25 RULE §3, PI-1030f).

  python3 scripts/c_t3/c_t3.py --selftest                                              CPU, synthetic only
  python3 scripts/c_t3/c_t3.py store --csv F --what test_refs --out P                  laptop, outside the repo
  python3 scripts/c_t3/c_t3.py draws --mem-emb E --query-emb Q --set S [--ex X] --out O CPU: example lists
  python  scripts/c_t3/c_t3.py embed --set S --images DIR --snapshot DIR --out O       GPU: SigLIP2 vectors
  python  scripts/c_t3/c_t3.py decode --model M --set S --arm A [--memory coco] ...   GPU
  python  scripts/c_t3/c_t3.py lmcap --set S --variant ri ...                           GPU: LMCap re-implementation
  python3 scripts/c_t3/c_t3.py t2 --ledger L --carve-ledger T1 [--exclude D] --out O    laptop: tier-2 decision (kept)
  python3 scripts/c_t3/c_t3.py t3 --ledger L --t2-decision J [--exclude N] --out O     laptop: tier-3 decision, once
Outputs hold captions and are never committed; ledgers and the summary hold ids and numbers only. Nothing here
prints a caption. The pinned C modules (decode_icl, build_memory, stage2, cen_decode, the LB decoder) are imported
unchanged; nothing in them is edited.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
import random
from statistics import NormalDist
import sys
import tempfile
import unicodedata
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "scripts" / d) for d in ("c_stage1", "c_stage2", "c_en", "lb", "b1_scaling")]
sys.path.insert(0, str(ROOT / "scripts"))
import build_memory as BM  # noqa: E402  seed, NEAR_COS, N_EX (C's example rule), unchanged
import decode_icl as C  # noqa: E402  Vietnamese template, shown(), memory captions, manifests
import cen_decode as D  # noqa: E402  English template (direct translation of C's)

lb = C.lb
PDIR = ROOT / "manuscript/prereg/2026-10-30_c_t1"
REG = PDIR / "c_t1_registry.json"
LISTS = PDIR / "c_t1_f30k_lists.json"
LABEL, SCHEMA = "TIER 3 / TEST, ONE LOOK (C-T3)", "vsps.c_t1.v1"  # schema kept: same record layout as tier 1
CAP_S = int(2.5 * 3600)  # C-T3 PREREG §5: tier-2 measured seconds of the kept arms x 1000/1014 = 1.86 h, +34%
SESOI = 2.0  # C's registered value, both languages (C-EN reused it); a planning value, see PREREG §9
DRAWS = (0, 1, 2)  # X1: draw 0 is C's own rand rule, unchanged
F30K_CSV_SHA256 = "395990db603ab8bafd5c7ab2746b22058bb1e75b78b3eb56ad755931364ac137"  # nlphuji/flickr30k @2b239bef
F30K_COUNTS = {"train": 29000, "val": 1014, "test": 1000}
CARVE_N, CARVE_SALT = 1000, "c-t1-f30k-carve-2026-10-30"
THIRD = ("aya_vision_8b", "gemma3_4b", "idefics3_8b")  # fallback order (§6)
OLD = ("qwen25vl_7b", "internvl3_8b")
VI_ASSESS_MIN = 0.95  # share of zero-shot captions with a Vietnamese letter or tone mark (§6.2)
VI_LETTERS = set("ăâđêôơư")
VI_TONES = {"̀", "́", "̃", "̉", "̣"}
SETS = {"ktvic_dev299": "vi", "ov_dev_b": "vi", "f30k_carve": "en", "f30k_val": "en", "f30k_test": "en"}
F30K = {"f30k_carve": "carve", "f30k_val": "val", "f30k_test": "test"}  # set -> part of c_t1_f30k_lists.json
LANG_NAME = {"vi": "vietnamese", "en": "english"}
LMCAP_K, LMCAP_N, LMCAP_BEAM, LMCAP_NEW = 4, 3, 3, 40  # Ramos et al. 2023 §3 and App. D
SEL_RULE = {"pcm_vs_zs_min": -1.0, "verbatim_max": 0.05, "hit_max_max": 0.02}  # C's stage-A rule, tau = -inf
SEL_GRID = [(k, o, "T1") for k in (2, 4, 8) for o in ("first", "last")] + [(4, "last", "T2")]
BOOT, BOOT_SEED = 2000, 0
DEFAULT_MEM = {"vi": "vi", "en": "coco"}
#: C's stage-2 OV-dev-B decodes, reused as rows and as zs_by (CC-172 W3); restored from the backup, sha-pinned
C2_DIR = "/root/outputs/c_stage2/runs"
C2_RUNS = {"c2_qwen25vl_7b_ov_dev_b-zs.preds.json": "5bf37a77d9883f91441956a01042a69861d94d46a9daec3d479eb7f1ab7e3fc3",
           "c2_qwen25vl_7b_ov_dev_b-ret-k8-first-T1.preds.json": "9fa11f7bc552be6310f8ffa9526bcc375352ced54b45ef2cb8085ec87902c03a",
           "c2_qwen25vl_7b_ov_dev_b-rand-k8-T1.preds.json": "53ce8591417cbffe2d6d9368eb5bfd46b123ce695d8cdd6e936faadf7b7118a1",
           "c2_internvl3_8b_ov_dev_b-zs.preds.json": "745c3bd736db2a1bae491d57a8bb2047bd183e7c249bdfb0dc24b649fb0fcb7f",
           "c2_internvl3_8b_ov_dev_b-ret-k4-last-T2.preds.json": "b05d9163aa9a85356d23d9ff50612750c1bbbf8022fed6caf9cb0476c35002fb",
           "c2_internvl3_8b_ov_dev_b-rand-k4-T2.preds.json": "991d289bb43b1bcb935e3717aede594147ba533da723501ae473f9af87f43a5b"}
C2_LEDGER_SHA256 = "be716482c6f934e975bdbc58927cfc42a4c0ff589c9c5f95affd67c03eac0938"  # stage-2 ledger, parity gate only
C2_PARITY_TOL = 1e-4
#: GPU-h per block at measured rates (PREREG §5); the job stops in this order when the cap binds
BLOCKS = {"V1_claims": 1.04, "V2_zs": 0.82}  # C-T3: tier-2 gpu_seconds.tsv x 1000/1014, rand rows left out
T1_CARVE_LEDGER_SHA256 = "4ced15b41c3efabfd6d69722a8c2008c8287597f69fc3a5ce18a4d4ab01b5615"  # carve_coco.jsonl, pooled
#: the five §8 NOMINATE claims (CC-191 r4): (claim, backbone, comparator key); nothing else is a claim at tier 2
T2_CLAIMS = (("E1", "aya_vision_8b", "aya_vision_8b|rand_d0"), ("E2", "qwen25vl_7b", "qwen25vl_7b|rand_d0"),
             ("E3", "aya_vision_8b", "lmcap_ri|lmcap"), ("E3", "internvl3_8b", "lmcap_ri|lmcap"),
             ("E3", "qwen25vl_7b", "lmcap_ri|lmcap"))
T2_MARGIN_P, TEST_N = 0.98, 1000
#: C-T3: the tier-2 decision (anchored in manuscript/prereg/2026-10-30_c_t2/T2_DECISION.sha256) and its family
T2_DECISION_SHA256 = "e29bbe8a6f9e62ec566fb2d52f4519042294be0d515e5c385181b084795a7c40"
T3_CLAIMS = (("E3 aya_vision_8b: ret-lmcap_ri", "aya_vision_8b"), ("E3 internvl3_8b: ret-lmcap_ri", "internvl3_8b"),
             ("E3 qwen25vl_7b: ret-lmcap_ri", "qwen25vl_7b"))
ALPHA = 0.05  # Holm over the family (C-T1 PREREG §8)
#: the only runs that may exist on f30k_test: the frozen tier-1/2 configurations (C-T2 PREREG §4), no rand, no smoke
T3_RUN_IDS = frozenset({"t3_lmcap-ri_f30k_test-mcoco", "t3_aya_vision_8b_f30k_test-ret-k4-last-T1-mcoco",
                        "t3_qwen25vl_7b_f30k_test-ret-k8-first-T1-mcoco", "t3_internvl3_8b_f30k_test-ret-k4-last-T2-mcoco",
                        "t3_aya_vision_8b_f30k_test-zs", "t3_qwen25vl_7b_f30k_test-zs", "t3_internvl3_8b_f30k_test-zs"})


def sha(p: Path) -> str:
    return lb.sha256_file(Path(p))


def gpu_host() -> bool:
    return D.M.gpu_host()  # C-EN's rule (env or machine-id file; an unreadable /root is not a GPU host)


# ------------------------------------------------------------------------------------------------ Flickr30K split
def f30k_rows(csv_path: Path) -> list[tuple[str, str]]:
    """[(split, filename)] of the pinned annotation file. Caption columns are never kept."""
    if sha(csv_path) != F30K_CSV_SHA256:
        raise SystemExit(f"{csv_path}: not the pinned Flickr30K annotation file")
    with open(csv_path, newline="", encoding="utf-8") as f:
        return [(r["split"], r["filename"]) for r in csv.DictReader(f)]


def f30k_split(rows: list[tuple[str, str]], counts: dict = F30K_COUNTS, n: int = CARVE_N) -> dict:
    """Tier 1 = a 1,000-image carve of train (smallest salted sha256 of the file name); the rest of train is the X5
    memory; val (tier 2) and test (tier 3) are refused in tier 1."""
    by = {s: sorted(f for t, f in rows if t == s) for s in counts}
    if {s: len(v) for s, v in by.items()} != counts or len({f for _s, f in rows}) != len(rows):
        raise SystemExit(f"Flickr30K split counts {({s: len(v) for s, v in by.items()})} are not {counts}")
    order = sorted(by["train"], key=lambda f: hashlib.sha256(f"{CARVE_SALT}|{f}".encode()).hexdigest())
    carve = sorted(order[:n])
    return {"carve": carve, "memory": sorted(order[n:]), "refuse": {"val": by["val"], "test": by["test"]}}


def cmd_lists(a) -> None:
    if gpu_host():
        raise SystemExit("lists is built on the laptop only")
    sp = f30k_split(f30k_rows(a.csv))
    rec = {"schema": SCHEMA, "label": LABEL, "csv_sha256": F30K_CSV_SHA256, "salt": CARVE_SALT,
           "counts": {"carve": len(sp["carve"]), "memory": len(sp["memory"]), **{k: len(v) for k, v in sp["refuse"].items()}},
           **sp}
    LISTS.write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(rec["counts"]))


def load_lists() -> dict:
    d = json.loads(LISTS.read_text(encoding="utf-8"))
    bad = set(d["carve"]) & (set(d["refuse"]["val"]) | set(d["refuse"]["test"]))
    if d.get("csv_sha256") != F30K_CSV_SHA256 or bad or set(d["carve"]) & set(d["memory"]):
        raise SystemExit(f"{LISTS}: not a clean tier-1 split")
    return d


def f30k_names(part: str, lists: dict) -> list[str]:
    """File names of one part. Tier 3 admits test (kept under 'refuse' in the pinned tier-1 list file, as val)."""
    if part not in ("carve", "memory", "val", "test"):
        raise SystemExit(f"REFUSED: Flickr30K {part} is not a listed part")
    return lists["refuse"][part] if part in ("val", "test") else lists[part]


def cmd_store(a) -> None:
    """Caption stores for the laptop only, never in the repo: the carve's or val's references, or the X5 memory's first
    caption. Test rows (and every row outside the asked part) are dropped as the file is read."""
    if Path(a.out).resolve().is_relative_to(ROOT):
        raise SystemExit("REFUSED: a caption store is never written inside the repository")
    laptop_only("store")
    lists = load_lists()
    part = {"carve_refs": "carve", "val_refs": "val", "test_refs": "test", "f30k_memory": "memory"}[a.what]
    keep, split = set(f30k_names(part, lists)), part if part in ("val", "test") else "train"
    if sha(a.csv) != F30K_CSV_SHA256:
        raise SystemExit("not the pinned csv")
    out = {}
    with open(a.csv, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["split"] != split or r["filename"] not in keep:
                continue
            refs = json.loads(r["raw"])
            out[r["filename"]] = refs[0] if part == "memory" else refs
    if len(out) != len(keep):
        raise SystemExit("store: rows missing")
    Path(a.out).write_text(json.dumps(out, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{a.what}: {len(out)} rows, sha256 {sha(a.out)}")


# ------------------------------------------------------------------------------------------------ examples (X1)
def eligible(row: np.ndarray, cids: list[str]) -> list[int]:
    """C's rule (build_memory.exemplars): clusters by cosine, ties by id, never one at cosine >= NEAR_COS."""
    return [j for j in np.lexsort((cids, -row)) if row[j] < BM.NEAR_COS]


def rand_draw(ds: str, qid: str, ok: list[str], d: int) -> list[str]:
    """Draw 0 is C's rand list exactly; draw d >= 1 seeds the same generator with the draw index appended."""
    s = BM.seed("rand", ds, qid) if d == 0 else BM.seed("rand", ds, qid, f"d{d}")
    return random.Random(s).sample(sorted(ok), BM.N_EX)


def draws(ds: str, mem_keys: list[str], mem_vecs: np.ndarray, q_ids: list[str], q_vecs: np.ndarray) -> dict:
    """{'ret': {qid: [[cid, cos]...]}, 'rand': {d: {qid: [cid...]}}} for one query set and one memory."""
    out = {"ret": {}, "rand": {str(d): {} for d in DRAWS}}
    cos = q_vecs @ mem_vecs.T
    for qid, row in zip(q_ids, cos):
        ok = eligible(row, mem_keys)
        out["ret"][qid] = [[mem_keys[j], round(float(row[j]), 6)] for j in ok[:BM.N_EX]]
        names = [mem_keys[j] for j in ok]
        for d in DRAWS:
            out["rand"][str(d)][qid] = rand_draw(ds, qid, names, d)
    return out


def cmd_draws(a) -> None:
    m, q = np.load(a.mem_emb), np.load(a.query_emb)
    mk = [str(k) for k in m["keys"] if "|" not in str(k)]
    mv = np.asarray(m["vecs"], np.float32)[[n for n, k in enumerate(m["keys"]) if "|" not in str(k)]]
    qk = [str(k) for k in q["keys"] if str(k).startswith(a.set + "|")]
    qv = np.asarray(q["vecs"], np.float32)[[n for n, k in enumerate(q["keys"]) if str(k).startswith(a.set + "|")]]
    qids = [k.split("|", 1)[1] for k in qk]
    res = draws(a.set, mk, mv, qids, qv)
    if a.ex:  # parity: draw 0 and ret must equal the committed example file (C's own lists)
        ex = json.loads(Path(a.ex).read_text(encoding="utf-8"))
        bad = [i for i in qids if ex["rand"][a.set][i] != res["rand"]["0"][i]
               or [c for c, _x in ex["ret"][a.set][i]] != [c for c, _x in res["ret"][i]]]
        if bad:
            raise SystemExit(f"PARITY FAIL: {len(bad)} of {len(qids)} images differ from {a.ex}")
        print(f"parity ok: draw 0 and ret equal {Path(a.ex).name} on {len(qids)} images")
    rec = {"schema": SCHEMA, "label": LABEL, "set": a.set, "mem_emb_sha256": sha(a.mem_emb),
           "query_emb_sha256": sha(a.query_emb), "near_cos": BM.NEAR_COS, **res}
    Path(a.out).write_text(json.dumps(rec) + "\n", encoding="utf-8")
    Path(str(a.out) + ".sha256").write_text(f"{sha(a.out)}  {Path(a.out).name}\n")


# ------------------------------------------------------------------------------------------------ prompts
def text_prompt(lang: str, tpl: str, caps: list[str]) -> str:
    return C.prompt(tpl, caps) if lang == "vi" else D.prompt(tpl, caps)


def rices_content(lang: str, tpl: str, ex_images: list, caps: list[str], query) -> list[dict]:
    """Interleaved demonstrations (Flamingo / OpenFlamingo RICES format) with C's own template text: header, then
    each example as image + its caption line, then the query image and the tail. Same examples, same k, same order
    as the text-only arm; only the example images are added."""
    hdr, line, tails = (C.HEADER, C.LINE, C.TAILS) if lang == "vi" else (D.HEADER, D.LINE, D.TAILS)
    out = [{"type": "text", "text": hdr}]
    for n, (im, c) in enumerate(zip(ex_images, caps, strict=True), 1):
        out += [{"type": "image", "image": im}, {"type": "text", "text": line.format(i=n, caption=c)}]
    return out + [{"type": "image", "image": query}, {"type": "text", "text": tails[tpl]}]


def lmcap_block(caps: list[str], lang: str) -> str:
    """One block of LMCap's template (Ramos et al. 2023, App. D), XGLM's </s> between retrieved captions."""
    return ("I am an intelligent image captioning bot. Similar images have the following captions: "
            + " ".join(c.strip() + "</s>" for c in caps)
            + f" A creative short caption I can generate to describe this image in {LANG_NAME[lang]} is:")


def lmcap_prompt(shots: list[tuple[list[str], str]], query_caps: list[str], lang: str) -> str:
    """N fixed shots (retrieved captions, the shot's own caption) then the query block."""
    if len(shots) != LMCAP_N or any(len(c) != LMCAP_K for c, _y in shots) or len(query_caps) != LMCAP_K:
        raise SystemExit("LMCap prompt: not N = 3 shots with K = 4 captions each")
    return "".join(f"{lmcap_block(c, lang)} {y.strip()}</s> " for c, y in shots) + lmcap_block(query_caps, lang)


def vi_assessable(captions: list[str]) -> float:
    """Share of captions holding a Vietnamese-only letter or a Vietnamese tone mark."""
    def vi(t: str) -> bool:
        n = unicodedata.normalize("NFD", t.lower())
        return bool(set(t.lower()) & VI_LETTERS) or any(ch in VI_TONES for ch in n)
    return float(np.mean([vi(c) for c in captions])) if captions else 0.0


# ------------------------------------------------------------------------------------------------ registry
def registry() -> dict:
    return json.loads(REG.read_text(encoding="utf-8"))


def model_spec(key: str) -> dict:
    """B-N1 block for the two C backbones; c_t1_registry for Aya; the L1-b registry (sha-pinned) for the others."""
    reg = registry()
    if key in OLD:
        return lb.load_prereg(C.pinned(C.B_N1))["models"][key]
    if key in reg["models"]:
        return reg["models"][key]
    ref = reg["borrowed"][key]
    p = ROOT / ref["registry"]
    if sha(p) != ref["registry_sha256"]:
        raise SystemExit(f"{p}: sha256 differs from c_t1_registry")
    return json.loads(p.read_text(encoding="utf-8"))["models"][key]


def pins_open(m: dict) -> list[str]:
    """Pinned files whose hash is still null (gated LFS hashes; filled from the authenticated tree API first)."""
    return sorted(k for k, v in m.get("files", {}).items() if not v.get("hash"))


# ------------------------------------------------------------------------------------------------ GPU decode
def items_of(ds: str, a) -> list[tuple[str, str, str]]:
    """[(id, file, sha256)]; refused for any Flickr30K test file and for C's refused images."""
    if ds in F30K:
        names = f30k_names(F30K[ds], load_lists())
        man = json.loads(Path(a.manifest).read_text(encoding="utf-8"))  # {file: sha256}, written at staging
        if set(man) != set(names):
            raise SystemExit(f"REFUSED: the staged {ds} is not the {len(names)} listed files")
        return [(f, f, man[f]) for f in names]
    import stage2 as S2
    clists = C.load_lists(a.c_lists)
    return C.manifest(ds, clists) if ds == "ktvic_dev299" else S2.manifest2(ds, clists)


def img_folder(ds: str, a) -> Path:
    """--images is $NCS_DATA/datasets for the Vietnamese sets (C's image_dir under it) and the carve folder itself."""
    if ds in F30K:
        return Path(a.images)
    import stage2 as S2
    return Path(a.images) / (C.DATASETS.get(ds) or S2.SETS[ds])["image_dir"]


def example_ids(arm: str, k: int, order: str | None, qid: str, ex: dict, draw: int) -> list[str]:
    if arm in ("ret", "ret_img"):
        ids = [c for c, _x in ex["ret"][qid][:k]]
        return ids[::-1] if order == "last" else ids
    if arm == "rand":
        return ex["rand"][str(draw)][qid][:k]
    return []


def memory_text(a, lang: str):
    """(captions, shown): memory 'vi' = C's memory captions read from $NCS_DATA (decode_icl.memory_captions), shown
    with C's own-dataset rule; 'coco' / 'f30k' = a caption store {cluster id: caption} outside the repo."""
    if a.memory == "vi":
        caps = C.memory_captions(C.load_lists(a.c_lists))
        src = "openviic" if a.set == "ov_dev_b" else "ktvic"
        return caps, lambda c: C.shown(caps[c], src)
    caps = json.loads(Path(a.captions).read_text(encoding="utf-8"))
    return caps, lambda c: caps[c]


def lmcap_shots(ds: str, mem_keys: list[str], cos: np.ndarray) -> list[str]:
    """LMCap's N fixed shots: N clusters drawn once per set (seeded) among those below C's near cut for every query."""
    safe = sorted(mem_keys[j] for j in np.flatnonzero(cos.max(0) < BM.NEAR_COS))
    return random.Random(BM.seed("lmcap_shots", ds)).sample(safe, LMCAP_N)


def cmd_decode(a) -> None:
    import decode_hf_vlm as LB

    lang = SETS[a.set]
    m = model_spec(a.model)
    if pins_open(m):
        raise SystemExit(f"{a.model}: pins open {pins_open(m)}; fill them from the authenticated tree API first")
    LB.check_snapshot(m, a.snapshot)
    items = items_of(a.set, a)
    ex = json.loads(Path(a.ex).read_text(encoding="utf-8")) if a.arm != "zs" else {}
    caps, shown = memory_text(a, lang) if a.arm != "zs" else ({}, None)
    run_id = f"t3_{a.model}_{a.set}-{a.arm}" + (f"-k{a.k}-{a.order or ''}-{a.tpl}" if a.arm != "zs" else "") \
        + (f"-d{a.draw}" if a.arm == "rand" else "") + (f"-m{a.memory}" if a.arm != "zs" else "") \
        + ("-smoke" if a.limit else "")
    t3_allowed(a.set, run_id)
    if a.limit:  # W-d smoke (N7): the first images only, timing; never scored
        items = items[:a.limit]
    out = Path(a.out_dir) / f"{run_id}.preds.json"
    if out.exists():
        raise SystemExit(f"{out} exists; a run is decoded once")
    exids = {i: example_ids(a.arm, a.k, a.order, i, ex, a.draw) for i, _f, _h in items}
    zs_text = (lb.prompt_text(lb.load_prereg(C.pinned(C.B_N1)), "short") if lang == "vi" else D.zs_prompt())
    texts = {i: zs_text if a.arm == "zs" else text_prompt(lang, a.tpl, [shown(c) for c in exids[i]]) for i in exids}
    if a.arm == "ret_img":  # N3: the sha covers the interleaved text parts (images as a placeholder)
        texts = {i: "\x1e".join(x.get("text", "<image>") for x in rices_content(
            lang, a.tpl, [None] * len(exids[i]), [shown(c) for c in exids[i]], None)) for i in exids}
    proc, net = LB.load(m, a.snapshot, "cuda:0")
    folder = img_folder(a.set, a)
    if a.arm == "ret_img":
        gen = rices_generate(proc, net, lang, a.tpl, folder, Path(a.mem_images), exids, shown, a.mem_files)
        batch = 1
    else:
        g = LB.make_generate(proc, net, None, D.N_NEW, folder)
        gen, batch = (lambda sl: g(sl, [texts[i] for i, _f, _h in sl])), m["batch_size"]
    rows = LB.decode_slices(items, batch, gen, out.with_name(out.name + ".partial.jsonl"), run_id)
    rec = {"schema": SCHEMA, "label": LABEL, "run_id": run_id, "model": a.model, "dataset": a.set, "lang": lang,
           "spec": {"arm": "ret" if a.arm == "ret_img" else a.arm, "img_examples": a.arm == "ret_img",
                    "k": 0 if a.arm == "zs" else a.k, "order": a.order, "tpl": a.tpl, "draw": a.draw,
                    "memory": None if a.arm == "zs" else a.memory},
           "hub_id": m["hub_id"], "revision": m["revision"], "c_t1_sha256": sha(Path(__file__)),
           "ex_sha256": sha(a.ex) if a.arm != "zs" else None, "exemplars": exids,
           "predictions": {r["image_id"]: r["caption"] for r in rows},
           "hit_max": {r["image_id"]: r["hit_max"] for r in rows}, "n_tokens": {r["image_id"]: r["n_tokens"] for r in rows},
           "prompt_sha256": {i: C.sha(t) for i, t in texts.items()}, "utc": lb.utc()}
    out.write_text(json.dumps(rec, ensure_ascii=False) + "\n", encoding="utf-8")
    Path(str(out) + ".sha256").write_text(f"{sha(out)}  {out.name}\n")
    print(f"{run_id}: {len(rows)} images")


def rices_generate(proc, net, lang, tpl, folder, mem_folder, exids, shown, mem_files_path):
    """Batch-1 generation with interleaved example images (memory cluster representatives, sha-checked)."""
    import torch
    from PIL import Image

    files = json.loads(Path(mem_files_path).read_text(encoding="utf-8"))  # {cid: [file, sha256]}
    eos = net.generation_config.eos_token_id
    eos = set(eos if isinstance(eos, list) else [eos])

    def img(p: Path, h: str):
        if sha(p) != h:
            raise SystemExit(f"{p}: sha256 differs from the manifest")
        return Image.open(p).convert("RGB")

    def generate(sl):
        out = []
        for i, f, h in sl:
            exs = [img(mem_folder / files[c][0], files[c][1]) for c in exids[i]]
            content = rices_content(lang, tpl, exs, [shown(c) for c in exids[i]], img(folder / f, h))
            enc = proc.apply_chat_template([[{"role": "user", "content": content}]], add_generation_prompt=True,
                                           tokenize=True, return_dict=True, return_tensors="pt",
                                           padding=True).to(net.device, net.dtype)
            with torch.no_grad():
                ids = net.generate(**enc, max_new_tokens=D.N_NEW, do_sample=False, num_beams=1)
            row = ids[0, enc["input_ids"].shape[1]:].tolist()
            n = next((k + 1 for k, t in enumerate(row) if t in eos), None)
            out.append((proc.decode(row[:n or len(row)], skip_special_tokens=True).strip(), n or len(row), n is None))
        return out

    return generate


def cmd_embed(a) -> None:
    """SigLIP2 vectors (C's embedder and settings, build_memory.cmd_embed) for the carve, val or the X5 memory."""
    import torch
    from PIL import Image
    from transformers import AutoModel, AutoProcessor

    lists = load_lists()
    man = json.loads(Path(a.manifest).read_text(encoding="utf-8"))
    names = f30k_names(F30K.get(a.set, "memory"), lists)
    if set(man) != set(names):
        raise SystemExit("REFUSED: the staged files are not the listed ones")
    proc = AutoProcessor.from_pretrained(a.snapshot)
    net = AutoModel.from_pretrained(a.snapshot, torch_dtype=torch.float16).eval().cuda()
    vecs = []
    for lo in range(0, len(names), 64):
        ims = []
        for f in names[lo:lo + 64]:
            if sha(Path(a.images) / f) != man[f]:
                raise SystemExit(f"{f}: sha256 differs from the manifest")
            ims.append(Image.open(Path(a.images) / f).convert("RGB"))
        with torch.no_grad():
            v = net.get_image_features(**proc(images=ims, return_tensors="pt").to("cuda", torch.float16)).float()
        vecs.append(torch.nn.functional.normalize(v, dim=-1).cpu().numpy())
    keys = [f"{a.set}|{f}" for f in names] if a.set in F30K else names
    np.savez(a.out, keys=np.array(keys), vecs=np.concatenate(vecs),
             meta=json.dumps({"model": BM.SIGLIP2, "label": LABEL, "manifest_sha256": sha(a.manifest)}))
    Path(str(a.out) + ".sha256").write_text(f"{sha(a.out)}  {Path(a.out).name}\n")


def cmd_lmcap(a) -> None:
    """LMCap re-implementation (no licence on the authors' code, so not run): M-CLIP xlm-roberta-large-ViT-H-14
    image-to-caption retrieval over the same memory (variant ri) or C's own top-4 retrieved clusters (variant se),
    N = 3 fixed shots, XGLM-2.9B, beam 3, 3 candidates re-ranked by M-CLIP image-text similarity."""
    import open_clip
    import torch
    from PIL import Image
    from transformers import AutoTokenizer, XGLMForCausalLM

    run_id = f"t3_lmcap-{a.variant}_{a.set}-m{a.memory}" + ("-smoke" if a.limit else "")
    t3_allowed(a.set, run_id)  # before any model load or decode
    reg, lang = registry(), SETS[a.set]
    for key, snap in (("xglm_2_9b", a.xglm), ("mclip_h14", a.mclip)):
        lb.check_snapshot(reg["models"][key], snap)
    items = items_of(a.set, a)
    ex = json.loads(Path(a.ex).read_text(encoding="utf-8"))
    caps, shown = memory_text(a, lang)
    m, q = np.load(a.mem_emb), np.load(a.query_emb)  # SigLIP2: C's near cut applies to LMCap's retrieval too
    sk = [str(k) for k in m["keys"] if "|" not in str(k)]
    sv = np.asarray(m["vecs"], np.float32)[[n for n, k in enumerate(m["keys"]) if "|" not in str(k)]]
    qpos = {str(k).split("|", 1)[1]: n for n, k in enumerate(q["keys"]) if str(k).startswith(a.set + "|")}
    scos = np.asarray(q["vecs"], np.float32)[[qpos[i] for i, _f, _h in items]] @ sv.T
    if sorted(sk) != sorted(caps):
        raise SystemExit("LMCap: the embedded memory is not the caption memory")
    mkeys = sorted(caps)
    clip, _p, pre = open_clip.create_model_and_transforms(
        "xlm-roberta-large-ViT-H-14", pretrained=str(Path(a.mclip) / "open_clip_pytorch_model.bin"))
    clip = clip.eval().half().cuda()
    tok = open_clip.get_tokenizer("xlm-roberta-large-ViT-H-14")

    def enc_text(texts):
        out = []
        for lo in range(0, len(texts), 256):
            with torch.no_grad():
                out.append(torch.nn.functional.normalize(clip.encode_text(tok(texts[lo:lo + 256]).cuda()).float(), dim=-1))
        return torch.cat(out)

    def enc_img(paths):
        with torch.no_grad():
            x = torch.stack([pre(Image.open(p).convert("RGB")) for p in paths]).half().cuda()
            return torch.nn.functional.normalize(clip.encode_image(x).float(), dim=-1)

    mtext = enc_text([shown(c) for c in mkeys])
    shot_ids = lmcap_shots(a.set, sk, scos)
    files = json.loads(Path(a.mem_files).read_text(encoding="utf-8"))  # {cid: [file, sha256]}
    for c in shot_ids:
        if sha(Path(a.mem_images) / files[c][0]) != files[c][1]:
            raise SystemExit(f"shot {c}: sha256 differs")
    shot_imgs = enc_img([Path(a.mem_images) / files[c][0] for c in shot_ids])

    def retrieve(v, skip: set[str]) -> list[str]:
        sc = (mtext @ v).cpu().numpy()
        return [mkeys[j] for j in np.lexsort((mkeys, -sc)) if mkeys[j] not in skip][:LMCAP_K]

    shots = [([shown(c) for c in retrieve(v, {s})], shown(s)) for s, v in zip(shot_ids, shot_imgs)]
    xt = AutoTokenizer.from_pretrained(a.xglm)
    xm = XGLMForCausalLM.from_pretrained(a.xglm, torch_dtype=torch.float16).eval().cuda()
    preds, exids, hitmax = {}, {}, {}
    if a.limit:
        items, scos = items[:a.limit], scos[:a.limit]
    folder = img_folder(a.set, a)
    for row, (i, f, h) in zip(scos, items):
        if sha(folder / f) != h:
            raise SystemExit(f"{f}: sha256 differs from the manifest")
        v = enc_img([folder / f])[0]
        if a.variant == "se":  # C's own top-4 retrieved clusters, nearest first
            q = [c for c, _x in ex["ret"][i][:LMCAP_K]]
        else:  # ri: M-CLIP image-to-caption retrieval; never a shot, never a cluster at SigLIP2 cosine >= NEAR_COS
            q = retrieve(v, set(shot_ids) | {sk[j] for j in np.flatnonzero(row >= BM.NEAR_COS)})
        exids[i] = q
        enc = xt(lmcap_prompt(shots, [shown(c) for c in q], lang), return_tensors="pt").to("cuda")
        with torch.no_grad():
            g = xm.generate(**enc, num_beams=LMCAP_BEAM, num_return_sequences=LMCAP_BEAM, max_new_tokens=LMCAP_NEW,
                            do_sample=False, eos_token_id=xt.eos_token_id)
        gen = [r[enc["input_ids"].shape[1]:].tolist() for r in g]
        cands = [xt.decode(r, skip_special_tokens=True).strip() for r in gen]
        best = int(torch.argmax(enc_text(cands) @ v))
        preds[i] = cands[best]
        hitmax[i] = xt.eos_token_id not in gen[best] and len(gen[best]) >= LMCAP_NEW  # N4
    out = Path(a.out_dir) / f"{run_id}.preds.json"
    rec = {"schema": SCHEMA, "label": LABEL, "run_id": run_id, "model": f"lmcap_{a.variant}", "dataset": a.set,
           "lang": lang, "spec": {"arm": "lmcap", "k": LMCAP_K, "n_shots": LMCAP_N, "beam": LMCAP_BEAM,
                                  "variant": a.variant, "memory": a.memory},
           "c_t1_sha256": sha(Path(__file__)), "ex_sha256": sha(a.ex), "exemplars": exids, "predictions": preds,
           "hit_max": hitmax, "shots": shot_ids, "utc": lb.utc()}
    out.write_text(json.dumps(rec, ensure_ascii=False) + "\n", encoding="utf-8")
    Path(str(out) + ".sha256").write_text(f"{sha(out)}  {out.name}\n")


def cmd_memfiles(a) -> None:
    """{cluster id: [path under the images root, sha256]} of each cluster's first member (laptop; ids and hashes only).
    Vietnamese: C's lists.json memory (root $NCS_DATA/datasets); English: C-EN's cen_memory.json (root = its images)."""
    if a.memory == "vi":
        folder = {"ktvic": "ktvic/images", "openviic": "openviic/images"}
        mem = C.load_lists(a.c_lists)["memory"]
        out = {m["cid"]: [f"{folder[m['members'][0][0]]}/{m['members'][0][2]}", m["members"][0][3]] for m in mem}
    else:
        mem = json.loads(Path(a.cen_memory).read_text(encoding="utf-8"))["memory"]
        out = {m["cid"]: [m["members"][0][1], m["members"][0][2]] for m in mem}
    Path(a.out).write_text(json.dumps(out) + "\n", encoding="utf-8")
    print(f"{len(out)} clusters, sha256 {sha(a.out)}")


def cmd_vicheck(a) -> None:
    """rc 3 when a backbone's zero-shot captions are not Vietnamese often enough (§6.2): next backbone in order."""
    r = json.loads(Path(a.preds).read_text(encoding="utf-8"))
    share = vi_assessable(list(r["predictions"].values()))
    print(f"{r['model']}: Vietnamese share {share:.3f} (min {VI_ASSESS_MIN})")
    sys.exit(0 if share >= VI_ASSESS_MIN else 3)


def cmd_cfg(a) -> None:
    c = json.loads(Path(a.file).read_text(encoding="utf-8"))
    print(c["k"], c["order"], c["tpl"])


# ------------------------------------------------------------------------------------------------ custody, fetch
MACHINE_ID = Path("/root/.vsps_machine_id")
FETCHABLE = ("aya_vision_8b", "gemma3_4b", "idefics3_8b", "xglm_2_9b", "mclip_h14", "xlm_roberta_large")


def machine_id() -> str:
    try:
        return MACHINE_ID.read_text().strip().lower()
    except OSError:
        return ""


def laptop_only(what: str) -> None:
    """CC-196 Codex fix 1: references and scores are never handled on a GPU host."""
    if machine_id() in ("m3", "m4"):
        raise SystemExit(f"REFUSED: {what} runs on the laptop only")


def t3_allowed(ds: str, run_id: str) -> None:
    """On f30k_test only the frozen tier-3 runs exist (no rand arm, no other k/order/template, no smoke)."""
    if ds == "f30k_test" and run_id not in T3_RUN_IDS:
        raise SystemExit(f"REFUSED: {run_id} is not a registered tier-3 run")


def extract_want(lists: dict) -> dict[str, set[str]]:
    """C-T3: only the 1,000 test members (carve, memory and val were extracted at tiers 1-2)."""
    want = {"test": set(f30k_names("test", lists))}
    other = set(lists["carve"]) | set(lists["memory"]) | set(lists["refuse"]["val"])
    if want["test"] & other or len(want["test"]) != F30K_COUNTS["test"]:
        raise SystemExit("REFUSED: the test list is not the 1,000 test files or touches another part")
    return want


def cmd_extract(a) -> None:
    """W4, on M1 (role m3) only, CPU: open the pinned zip, copy the 1,000 test files by list into one test-only .tar
    under c_t3_f30k_test/images/, write manifest_test.json {file: sha256}. Train and val members are never read."""
    import tarfile
    import zipfile

    if machine_id() != "m3":
        raise SystemExit("REFUSED: the Flickr30K zip is opened only on M1 (role m3)")
    if sha(a.zip) != registry()["data"]["flickr30k"]["flickr30k-images.zip"]:
        raise SystemExit(f"{a.zip}: not the pinned zip")
    want = extract_want(load_lists())
    with zipfile.ZipFile(a.zip) as z:  # N-c: a wanted name occurs once
        names = [Path(i.filename).name for i in z.infolist() if not i.is_dir()]
    dup = {n for n in names if n in want["test"] and names.count(n) > 1} if len(names) != len(set(names)) else set()
    if dup:
        raise SystemExit(f"extract: {len(dup)} wanted names occur twice in the zip")
    man = {"test": {}}
    with zipfile.ZipFile(a.zip) as z, tarfile.open(a.out, "w") as t:
        for info in z.infolist():
            name = Path(info.filename).name
            part = next((k for k, v in want.items() if name in v), None)
            if part is None or info.is_dir():
                continue  # train, val and anything else: never read
            data = z.read(info)
            man[part][name] = hashlib.sha256(data).hexdigest()
            ti = tarfile.TarInfo(f"c_t3_f30k_{part}/images/{name}")
            ti.size = len(data)
            t.addfile(ti, io.BytesIO(data))
    if {k: len(v) for k, v in man.items()} != {k: len(v) for k, v in want.items()}:
        raise SystemExit("extract: files missing from the zip")
    for k, v in man.items():
        Path(a.out).with_name(f"manifest_{k}.json").write_text(json.dumps(v, sort_keys=True) + "\n")
    print(f"tar {sha(a.out)}; test {len(man['test'])}")


#: AMENDMENT_1 read isolation (job on M1, role m3, beside test-side files): the only $NCS_DATA/datasets dirs the job
#: may read, the other $NCS_DATA dirs it may read, and the commands that run under the open() audit hook.
ISO_DATASETS = ("ktvic", "openviic", "c_t1_f30k_carve", "c_t1_f30k_memory", "cen_memory", "c_t1_mem", "c_t2_f30k_val",
                "c_t3_f30k_test")
ISO_NCS = ("models", "vncorenlp")
ISO_CMDS = ("draws", "embed", "decode", "lmcap", "score", "select", "vicheck", "memcheck", "t1check", "pinsok", "cfg",
            "dupcheck")
ARCHIVES = (".zip", ".tar", ".tar.gz", ".tgz", ".7z")  # plus any ".tar.*" (N6)
RESTORED = PDIR / "RESTORED_SHA256"


def refused_names() -> set[str]:
    return set()  # C-T3: test is the evaluated set; other one-look sets stay out by the datasets/outputs allow-lists


def iso_config(ncs: Path, outputs: Path, restored: list[str], refused: set[str]) -> dict:
    rp = os.path.realpath
    return {"ncs": rp(ncs), "outputs": rp(outputs), "refused": refused,
            "ncs_ok": [rp(Path(ncs) / "datasets" / d) for d in ISO_DATASETS] + [rp(Path(ncs) / d) for d in ISO_NCS],
            "out_ok": [rp(Path(outputs) / "c_t3")], "files_ok": {rp(f) for f in restored}}


def iso_default() -> dict:
    files = [ln.split(maxsplit=1)[1] for ln in RESTORED.read_text().splitlines() if ln.strip()]
    return iso_config(lb.DATA, Path("/root/outputs"), files, refused_names())


def is_archive(name: str) -> bool:
    return name.endswith(ARCHIVES) or ".tar." in name


def _under(p: str, root: str) -> bool:
    return p == root or p.startswith(root.rstrip("/") + "/")


def iso_denied(path, cfg: dict) -> str | None:
    """Why the job may not open this path (None = allowed). Symlinks are resolved first."""
    asked = os.fsdecode(path)
    p = os.path.realpath(asked)
    names = {os.path.basename(asked), os.path.basename(p)}  # CC-176 W2: the name as requested and as resolved
    if names & cfg["refused"]:
        return "a Flickr30K test file name"
    if any(is_archive(n) for n in names):
        return "an archive"
    if _under(p, cfg["ncs"]) and not any(_under(p, r) for r in cfg["ncs_ok"]):
        return "outside the staged $NCS_DATA dirs"
    if _under(p, cfg["outputs"]) and p not in cfg["files_ok"] and not any(_under(p, r) for r in cfg["out_ok"]):
        return "outside /root/outputs/c_t3 and the restored files"
    return None


def iso_install(cfg: dict) -> None:
    """AMENDMENT_1: every Python-level open() (builtins, io, os.open) of a denied path raises PermissionError.
    Ceiling: native-code opens (safetensors, tokenizers) and child processes are not seen; they only get model
    paths from the registry, and the guard scans those dirs."""
    def hook(event, args):
        if event == "open" and isinstance(args[0], (str, bytes, os.PathLike)):
            why = iso_denied(args[0], cfg)
            if why:
                raise PermissionError(f"C-T1 isolation (AMENDMENT_1): {os.fsdecode(args[0])}: {why}")
    sys.addaudithook(hook)


def guard_problems(roots: list[Path], refused: set[str], cfg: dict | None = None,
                   datasets: Path | None = None) -> list[str]:
    """W4 (CC-170 W9 style): no archive, no Flickr30K zip tree, no Flickr30K test file name in the job's readable
    roots; AMENDMENT_1: no symlink that resolves to a denied path, and $NCS_DATA/datasets holds only C-T1's dirs."""
    bad = [str(datasets / n) for n in sorted(os.listdir(datasets)) if n not in ISO_DATASETS] if datasets else []
    for r in roots:
        for dirpath, dirs, files in os.walk(r):
            for n in dirs + files:
                q = Path(dirpath) / n
                if is_archive(n) or n.startswith("flickr30k-images") or n in refused:
                    bad.append(str(q))
                elif cfg and q.is_symlink() and iso_denied(q, cfg):
                    bad.append(f"{q} -> {os.path.realpath(q)}")
    return bad


def cmd_guard(a) -> None:
    bad = guard_problems([Path(x) for x in a.roots], refused_names(), iso_default(),
                         Path(a.datasets) if a.datasets else None)
    if bad:
        raise SystemExit(f"REFUSED: {len(bad)} forbidden paths, e.g. {bad[:3]}")
    print("guard ok")


def cmd_memcheck(a) -> None:
    """W10: every memfiles entry exists under its root with its sha256 (before any GPU step)."""
    files = json.loads(Path(a.mem_files).read_text(encoding="utf-8"))
    bad = [c for c, (f, h) in files.items() if not (Path(a.root) / f).is_file() or sha(Path(a.root) / f) != h]
    if bad:
        raise SystemExit(f"memcheck: {len(bad)} of {len(files)} example images missing or changed")
    print(f"memcheck ok: {len(files)} images")


def snap_ok(key: str, snap: Path) -> bool:
    return not pins_open(model_spec(key)) and (Path(snap) / ".c_t1_ok").is_file()


def cmd_fetch(a) -> None:
    """W9: pinned revision, every registry file checked, then the .c_t1_ok marker. rc 3 while pins are open."""
    import decode_hf_vlm as LB
    from huggingface_hub import snapshot_download

    m = model_spec(a.model)
    if pins_open(m):
        print(f"{a.model}: pins open {pins_open(m)}: skipped, never fetched")
        sys.exit(3)
    if a.model == "xlm_roberta_large":  # open_clip loads it by name from the HF cache (HF_HUB_OFFLINE=1)
        snap = Path(snapshot_download(m["hub_id"], revision=m["revision"], allow_patterns=sorted(m["files"])))
    else:
        snap = Path(snapshot_download(m["hub_id"], revision=m["revision"], local_dir=a.snapshot,
                                      allow_patterns=sorted(m["files"])))
    LB.check_snapshot(m, snap)
    (Path(a.snapshot) / ".c_t1_ok").write_text(lb.utc() + "\n")
    print(f"{a.model}: {len(m['files'])} pinned files ok")


def cmd_pinsok(a) -> None:
    ok = snap_ok(a.model, a.snapshot)
    print(f"{a.model}: {'ok' if ok else 'pins open or snapshot not fetched: SKIP'}")
    sys.exit(0 if ok else 3)


def cmd_t1check(a) -> None:
    """W8: venv-t1 imports open_clip and builds M-CLIP offline from the pinned files (CPU, not charged)."""
    import open_clip
    from huggingface_hub import snapshot_download
    import decode_hf_vlm as LB

    reg = registry()
    LB.check_snapshot(reg["models"]["mclip_h14"], a.mclip)
    xr = reg["models"]["xlm_roberta_large"]
    LB.check_snapshot(xr, Path(snapshot_download(xr["hub_id"], revision=xr["revision"], local_files_only=True)))
    open_clip.create_model_and_transforms(reg["models"]["mclip_h14"]["open_clip_name"],
                                          pretrained=str(Path(a.mclip) / "open_clip_pytorch_model.bin"))
    print("venv-t1 ok: open_clip", open_clip.__version__)


# ------------------------------------------------------------------------------------------------ X2 masking
def masked(caption: str, shown: list[str], n: int = 3) -> str:
    """X2: the caption with every token removed that sits in a word n-gram also present in a shown example."""
    toks = caption.lower().split()
    grams = {tuple(t[j:j + n]) for s in shown for t in [s.lower().split()] for j in range(len(t) - n + 1)}
    drop = set()
    for j in range(len(toks) - n + 1):
        if tuple(toks[j:j + n]) in grams:
            drop.update(range(j, j + n))
    return " ".join(t for j, t in enumerate(toks) if j not in drop)


# ------------------------------------------------------------------------------------------------ score
def tag(r: dict) -> dict:
    """Ledger fields that name a run beyond C's (arm, k, order, tpl)."""
    sp = r["spec"]
    return {"draw": sp.get("draw", 0), "img_examples": bool(sp.get("img_examples")), "memory": sp.get("memory"),
            "lmcap_variant": sp.get("variant")}


def cmd_score(a) -> None:
    """Vietnamese: C's stage-1 scorer (score_set, unchanged; kit B, RDRSegmenter, stripped CIDEr-D) for model runs, the
    stage-2 plain_row for LMCap and the X2 masked variants. English: C-EN's PTB CIDEr-D (pycocoevalcap 1.2) with df
    over the carve's own references. Rows hold ids and numbers only."""
    import guard as G
    import score as S
    import score2 as S2s

    laptop_only("score")
    lang = SETS[a.set]
    runs = [json.loads(Path(p).read_text(encoding="utf-8")) | {"_sha256": sha(p)} for p in a.runs]
    if any(r["dataset"] != a.set or r.get("schema") != SCHEMA for r in runs):
        raise SystemExit("score: a run is not a C-T1 output of this set")
    if any(r["run_id"].endswith("-smoke") for r in runs):
        raise SystemExit("score: smoke runs are never scored")
    c2 = c2_runs(Path(a.c2_dir)) if a.c2_dir else []
    if c2 and a.set != "ov_dev_b":
        raise SystemExit("score: C's stage-2 runs belong to ov_dev_b")
    runs += c2
    if a.memory and any(r["spec"].get("memory") != a.memory for r in runs if r["spec"]["arm"] != "zs"):
        raise SystemExit("score: one memory per score call (its caption store serves X2)")
    model_runs = [r for r in runs if r["spec"]["arm"] != "lmcap"]
    zs_by = {r["model"]: r for r in model_runs if r["spec"]["arm"] == "zs"}
    rows = []
    if lang == "vi":
        import stage2 as ST2
        E4, PA, PTB = S2s.kit2(a.kit_b)
        clists = C.load_lists(a.c_lists)
        caps = C.memory_captions(clists)
        refs = S.references(a.set, clists) if a.set == "ktvic_dev299" else ST2.references2(a.set, clists)
        for m in zs_by:
            G.VERIFIER.setdefault(m, "none")  # new backbones run deletion-free: no verifier, tau = -inf only
        ctx = {"cache": {}, "caps": caps, "segment": E4.rdr, "E4": E4, "PA": PA, "PTB": PTB}
        others = [r for r in model_runs if r["spec"]["arm"] != "zs"]
        for b in S.score_set(a.set, others, zs_by, refs, ctx):
            r = next(x for x in model_runs if x["run_id"] == b["run_id"])
            rows.append({**b, **tag(r)})
        src = "openviic" if a.set == "ov_dev_b" else "ktvic"
        store = json.loads(Path(a.captions).read_text(encoding="utf-8")) if a.captions else {}

        def shown_of(r: dict, c: str) -> str:  # LMCap-ri on OV-dev-B with C-EN's English COCO memory (N6)
            return C.shown(caps[c], src) if r["spec"].get("memory", "vi") == "vi" else store[c]
        texts = sorted({c for r in runs for c in r["predictions"].values()} | {x for v in refs.values() for x in v})
        seg = dict(zip(texts, (t.lower() for t in E4.rdr(texts))))
        for r in runs:
            head = {"dataset": a.set, "run_id": r["run_id"], "arm": r["spec"]["arm"], "k": r["spec"]["k"]}
            if r["spec"]["arm"] == "lmcap":
                rows.append({**plain_row(S2s, head, r["predictions"], refs, ctx, seg), "model": r["model"], **tag(r)})
            if r["spec"]["arm"] != "zs":  # X2
                mc = {i: masked(c, [shown_of(r, x) for x in r["exemplars"][i]]) or "."
                      for i, c in r["predictions"].items()}  # N1
                rows.append({**plain_row(S2s, head, mc, refs, ctx, seg), "model": r["model"], "variant": "masked3", **tag(r)})
    else:
        import cen_score as CS
        tokenize, cider = CS.ptb_cider()
        refs = json.loads(Path(a.refs).read_text(encoding="utf-8"))
        caps = json.loads(Path(a.captions).read_text(encoding="utf-8")) if a.captions else {}
        ids = sorted(refs)
        gts = tokenize({i: refs[i] for i in ids})
        for r in runs:
            if sorted(r["predictions"]) != ids:
                raise SystemExit(f"{r['run_id']}: not the carve")
            variants = [("plain", r["predictions"])]
            if r["spec"]["arm"] != "zs":
                variants.append(("masked3", {i: masked(c, [caps[x] for x in r["exemplars"][i]]) or "."
                                             for i, c in r["predictions"].items()}))
            for v, capt in variants:
                res = tokenize({i: [capt[i]] for i in ids})
                sc = cider(gts, {i: res[i] for i in ids})
                rows.append({"dataset": a.set, "run_id": r["run_id"], "model": r["model"], "arm": r["spec"]["arm"],
                             "k": r["spec"]["k"], "tau": "-inf", "variant": v, "n": len(ids),
                             "cider_ptb": float(sc.mean()), "hit_max_rate": float(np.mean([r["hit_max"][i] for i in ids])),
                             "per_image": {"ids": ids, "cider_ptb": sc.round(4).tolist()}, **tag(r)})
    if c2:
        c2_parity(rows, Path(a.c2_ledger))
    stamp = {"label": LABEL, "c_t1_sha256": sha(Path(__file__)), "utc": lb.utc()}
    with Path(a.ledger).open("a", encoding="utf-8") as f:
        f.writelines(json.dumps({**r, **stamp}, ensure_ascii=False) + "\n" for r in rows)
    print(f"appended {len(rows)} rows to {a.ledger}")


def c2_runs(folder: Path) -> list[dict]:
    """C's six stage-2 OV-dev-B run files (schema vsps.lb_decode.v1), sha-pinned, as C-T1 run dicts (draw 0, vi)."""
    out = []
    for name, h in C2_RUNS.items():
        p = folder / name
        if sha(p) != h:
            raise SystemExit(f"{p}: not C's pinned stage-2 run")
        r = json.loads(p.read_text(encoding="utf-8"))
        out.append({**r, "_sha256": h, "schema": SCHEMA, "c2_source": name,
                    "spec": {**r["spec"], "draw": 0, "memory": "vi", "img_examples": False}})
    return out


def c2_parity(rows: list[dict], ledger: Path) -> None:
    """W3 gate: C-T1's re-score of C's stage-2 runs equals the stage-2 ledger (tau -inf, per-image cider_s)."""
    if sha(ledger) != C2_LEDGER_SHA256:
        raise SystemExit(f"{ledger}: not the stage-2 ledger")
    old = {r["run_id"]: r for x in ledger.read_text(encoding="utf-8").splitlines() if x.strip()
           for r in [json.loads(x)] if r.get("tau") == "-inf" and r.get("variant") is None and r.get("model")}
    n = 0
    for r in rows:
        if r["run_id"] in old and r.get("variant") is None and r.get("tau") == "-inf":
            a, b = np.array(r["per_image"]["cider_s"]), np.array(old[r["run_id"]]["per_image"]["cider_s"])
            if r["per_image"]["ids"] != old[r["run_id"]]["per_image"]["ids"] or np.abs(a - b).max() > C2_PARITY_TOL:
                raise SystemExit(f"PARITY FAIL: {r['run_id']} re-score differs from the stage-2 ledger")
            n += 1
    if n != len(C2_RUNS):
        raise SystemExit(f"PARITY FAIL: {n} of {len(C2_RUNS)} stage-2 runs matched")
    print(f"stage-2 parity ok: {n} runs")


def plain_row(S2s, head: dict, capt: dict, refs: dict, ctx: dict, seg: dict) -> dict:
    """score2.plain_row (CIDEr-D as written, stripped and PTB, CHAIR_i) with any missing segmentation added."""
    miss = sorted({c for c in capt.values() if c not in seg})
    if miss:
        seg.update(zip(miss, (t.lower() for t in ctx["segment"](miss))))
    return S2s.plain_row(head, capt, refs, ctx, seg)


# ------------------------------------------------------------------------------------------------ selection
def select(rows: list[dict]) -> dict | None:
    """C's stage-A rule (stage-1 DESIGN l.272-278) at tau = -inf: the highest stripped CIDEr-D among the 7 ret runs
    meeting all three constraints; ties to the smaller k, then 'last', then T1. None eligible: the backbone FAILS
    selection (None), and the job moves to the next backbone in order."""
    cands = [r for r in rows if r["arm"] == "ret" and r["tau"] == "-inf" and r.get("variant") is None]
    if len(cands) != len(SEL_GRID):
        raise SystemExit(f"select: {len(cands)} ret rows, not {len(SEL_GRID)}")
    ok = [r for r in cands if r["pcm_vs_zs"] >= SEL_RULE["pcm_vs_zs_min"] and r["hit_max_rate"] <= SEL_RULE["hit_max_max"]
          and r["verbatim_share"] is not None and r["verbatim_share"] <= SEL_RULE["verbatim_max"]]
    if not ok:
        return None
    best = min(ok, key=lambda r: (-round(r["cider_s"], 6), r["k"], r["order"] != "last", r["tpl"] != "T1"))
    return {"k": best["k"], "order": best["order"], "tpl": best["tpl"], "tau": "-inf", "run_id": best["run_id"],
            "rule": SEL_RULE}


# ------------------------------------------------------------------------------------------------ summary
def boot_idx(n: int) -> np.ndarray:
    return np.random.default_rng(BOOT_SEED).integers(0, n, (BOOT, n))


def contrast(a: np.ndarray, b: np.ndarray) -> dict:
    """Paired per-image difference, percentile bootstrap over images (C's B = 2,000, seed 0)."""
    x = np.asarray(a, float) - np.asarray(b, float)
    lo, hi = np.percentile(x[boot_idx(len(x))].mean(1), [2.5, 97.5])
    return {"d": float(x.mean()), "lo": float(lo), "hi": float(hi), "n": len(x), "se": float(x.std(ddof=1) / math.sqrt(len(x)))}


def contrast_draws(ret: np.ndarray, rands: list[np.ndarray]) -> dict:
    """X1: ret minus the mean over rand draws, bootstrap over images; between-draw SD of the mean contrast."""
    r = contrast(ret, np.mean(rands, axis=0))
    per = [float(np.mean(np.asarray(ret) - np.asarray(z))) for z in rands]
    return {**r, "per_draw": per, "between_draw_sd": float(np.std(per, ddof=1)) if len(per) > 1 else None}


def pcm_contrast(a: tuple, b: tuple) -> dict:
    """X3: count-matched precision vs zero-shot (C's pcm_vs_zs = 100 (sum tp - sum tp_zs) / sum k), ret minus rand,
    bootstrap over images of the two ratios. a, b: (tp, tp_zs, k) per image, existing reference gold only."""
    def pcm(t, idx):
        tp, tz, k = (np.asarray(x, float)[idx] for x in t)
        return 100 * (tp.sum(-1) - tz.sum(-1)) / np.maximum(k.sum(-1), 1)
    n = len(a[0])
    d = pcm(a, np.arange(n)) - pcm(b, np.arange(n))
    bs = pcm(a, boot_idx(n)) - pcm(b, boot_idx(n))
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return {"d": float(d), "lo": float(lo), "hi": float(hi), "n": n}


def advance(c: dict, sesoi: float = SESOI) -> str:
    """Tier-1 label of a candidate tier-2 claim: NOMINATE iff the 95% CI lower bound >= SESOI; WATCH iff only the
    point is >= SESOI; DROP otherwise."""
    return "NOMINATE" if c["lo"] >= sesoi else "WATCH" if c["d"] >= sesoi else "DROP"


def phi(z: float) -> float:
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def p_pass(c: dict, sesoi: float = SESOI, m: int = 1) -> float:
    """Planning value: P(point >= SESOI and the one-sided test passes at alpha 0.05 / m at the same n), normal
    approximation; Bonferroni on Holm's first step (CC-172a W12); joint = Frechet LOWER bound max(0, P1 + P2 - 1)
    (CC-172 W7, CC-171 W1)."""
    if c["se"] == 0:
        return float(c["d"] >= sesoi and c["d"] > 0)
    crit = NormalDist().inv_cdf(1 - 0.05 / m)
    return float(max(0.0, phi((c["d"] - sesoi) / c["se"]) + phi(c["d"] / c["se"] - crit) - 1))


def summarize(per: dict[str, np.ndarray], kill_key: str | None = "qwen25vl_7b", pcm: dict | None = None,
              confirm: bool = True) -> dict:
    """per: {'<model>|<arm>': per-image decision column} on one set (aligned ids). Candidate claims: <m> ret-rand,
    <m> ret-lmcap_ri; descriptive: ret_img-ret, memswap. Kill gate: if Qwen's ret-rand point < 0, every retrieval
    claim on this set is DROPPED (OpenFlamingo's Flickr-30K reversal)."""
    out = {}
    models = sorted({k.split("|")[0] for k in per if not k.startswith("lmcap")})
    killed = kill_key is not None and f"{kill_key}|ret" in per and f"{kill_key}|rand_d0" in per and \
        contrast(per[f"{kill_key}|ret"], per[f"{kill_key}|rand_d0"])["d"] < 0
    for m in models:
        ret = per.get(f"{m}|ret")
        if ret is None:
            continue
        if f"{m}|rand_d0" in per:
            c = contrast(ret, per[f"{m}|rand_d0"])
            out[f"{m}: ret-rand"] = {**c, "label": "DROP (kill gate)" if killed else advance(c), "p_pass_plan": p_pass(c)}
        rands = [per[f"{m}|rand_d{d}"] for d in DRAWS if f"{m}|rand_d{d}" in per]
        if len(rands) > 1:
            out[f"{m}: ret-rand (X1, {len(rands)} draws)"] = contrast_draws(ret, rands)
        if "lmcap_ri|lmcap" in per:
            c = contrast(ret, per["lmcap_ri|lmcap"])
            out[f"{m}: ret-lmcap_ri"] = {**c, "label": advance(c), "p_pass_plan": p_pass(c)}
        for k, name in ((f"{m}|ret_img", "ret_img-ret (RICES, descriptive)"), (f"{m}|ret_f30k", "memswap f30k-coco")):
            if k in per:
                out[f"{m}: {name}"] = contrast(per[k], ret)
        if f"{m}|ret_m3" in per and f"{m}|rand_d0_m3" in per:
            out[f"{m}: ret-rand masked3 (X2, descriptive)"] = contrast(per[f"{m}|ret_m3"], per[f"{m}|rand_d0_m3"])
        if pcm and f"{m}|ret" in pcm and f"{m}|rand_d0" in pcm:
            out[f"{m}: pcm ret-rand (X3, descriptive)"] = pcm_contrast(pcm[f"{m}|ret"], pcm[f"{m}|rand_d0"])
    m_nom = max(1, sum(v.get("label") == "NOMINATE" for v in out.values()))
    for v in out.values():  # W12: planning P at m = 1 and at m = the number of nominated claims
        if "p_pass_plan" in v and v.get("se") is not None:
            v["p_pass_plan"] = {"m1": p_pass(v), f"m{m_nom}": p_pass(v, m=m_nom)}
    if not confirm:  # N2: no unspent Vietnamese test set; labels never apply
        for v in out.values():
            if "label" in v:
                v["label"], v["p_pass_plan"] = "DESCRIPTIVE", None
    return {"killed": bool(killed), "contrasts": out}


def cmd_select(a) -> None:
    rows = [json.loads(x) for x in Path(a.ledger).read_text(encoding="utf-8").splitlines() if x.strip()]
    rows = [r for r in rows if r.get("model") == a.model and r["dataset"] == "ktvic_dev299"]
    sel = select(rows)
    if sel is None:
        print(f"{a.model}: no ret run meets C's stage-A constraints: FAILS selection")
        sys.exit(3)
    rec = {"schema": SCHEMA, "label": LABEL, "model": a.model, **sel}
    Path(a.out).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(rec))


def set_columns(rows: list[dict], ds: str, lang: str) -> tuple[dict, dict, list | None]:
    """({'<model>|<arm>': per-image decision column}, X3 tuples, image ids) of one set, from ledger rows."""
    col = "cider_s" if lang == "vi" else "cider_ptb"
    per, pcm, ids0 = {}, {}, None
    for r in rows:
        if r.get("dataset") != ds or r.get("tau", "-inf") != "-inf" or r.get("variant", "plain") not in ("plain", "masked3") \
                or not r.get("model") or r.get("arm") in ("nn_top1", "nn_cons", "fix", "blind"):
            continue
        arm = r["arm"] + (f"_d{r.get('draw') or 0}" if r["arm"] == "rand" else "") \
            + ("_img" if r.get("img_examples") else "") \
            + (f"_{r['memory']}" if r.get("memory") not in (None, DEFAULT_MEM[lang]) else "") \
            + ("_m3" if r.get("variant") == "masked3" else "")
        key = f"{r['model']}|{arm}"
        ids = r["per_image"]["ids"]
        ids0 = ids0 or ids
        if ids != ids0:
            raise SystemExit(f"{r['run_id']}: image order differs within {ds}")
        if key in per:
            raise SystemExit(f"summary: two ledger rows for {key} on {ds}")
        per[key] = np.array(r["per_image"][col], float)
        if "tp_cm" in r["per_image"]:
            pcm[key] = tuple(r["per_image"][x] for x in ("tp_cm", "tp_cm_zs", "k_cm"))
    return per, pcm, ids0


def read_ledgers(paths: list) -> list[dict]:
    return [json.loads(x) for p in paths for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]


def cmd_summary(a) -> None:
    rows = read_ledgers(a.ledger)
    res = {"schema": SCHEMA, "label": LABEL, "sesoi": SESOI, "sets": {}}
    for ds, lang in SETS.items():
        if ds in ("ktvic_dev299", "f30k_val", "f30k_test"):  # selection set (W3); val by `t2`, test by `t3` only
            continue
        per, pcm, _ids = set_columns(rows, ds, lang)
        if per:
            res["sets"][ds] = summarize(per, "qwen25vl_7b" if lang == "en" else None, pcm, confirm=lang == "en")
            res["sets"][ds]["confirmatory"] = lang == "en"  # Vietnamese: no unspent test set, rows stay dev-only
    Path(a.out).write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({ds: {k: v.get("label") for k, v in s["contrasts"].items()} for ds, s in res["sets"].items()}))


# ------------------------------------------------------------------------------------------------ C-T2 (tier 2)
def exact_dups(val_man: dict, mem_files: dict, carve_man: dict) -> dict:
    """PI-1030f (dev = exact sha/id only): val files whose sha256 equals a COCO memory example image (members[0]), a
    carve image, or an earlier val file. 'exclude' feeds the dedup row printed beside the full-set decision."""
    mem, carve, seen = {h for _f, h in mem_files.values()}, set(carve_man.values()), set()
    out = {"memory": [], "carve": [], "within_val": []}
    for f in sorted(val_man):
        h = val_man[f]
        if h in mem:
            out["memory"].append(f)
        if h in carve:
            out["carve"].append(f)
        if h in seen:
            out["within_val"].append(f)
        seen.add(h)
    return {**out, "exclude": sorted({f for v in out.values() for f in v})}


def cmd_dupcheck(a) -> None:
    val_man = json.loads(Path(a.manifest).read_text(encoding="utf-8"))
    if set(val_man) != set(f30k_names("val", load_lists())):
        raise SystemExit("REFUSED: the manifest is not the 1,014 val files")
    res = exact_dups(val_man, json.loads(Path(a.mem_files).read_text(encoding="utf-8")),
                     json.loads(Path(a.carve_manifest).read_text(encoding="utf-8")))
    Path(a.out).write_text(json.dumps({"label": LABEL, "rule": "PI-1030f exact sha256", **res}, indent=1) + "\n")
    print(json.dumps({k: len(v) for k, v in res.items()}))


def t2_decide(val: dict, carve: dict) -> dict:
    """C-T1 PREREG §8 at tier 2. val PASS = point >= SESOI and 95% CI lower bound > 0 (B = 2,000, seed 0). P(PASS on
    test, n = 1,000) from the pooled carve + val per-image differences (Frechet lower bound, Bonferroni on Holm's first
    step) at m = the number of claims passing val, computed once (CC-191 r5). Tier-3 family = val PASS (which holds
    the margin's point >= SESOI) and P >= 0.98. A claim whose arms were not decoded is NOT RUN and never enters."""
    claims = {}
    for e, m, comp in T2_CLAIMS:
        name, ret = f"{e} {m}: ret-{'lmcap_ri' if comp.startswith('lmcap') else 'rand'}", f"{m}|ret"
        if ret not in val or comp not in val:
            claims[name] = {"status": "NOT RUN", "family": False}
            continue
        v = contrast(val[ret], val[comp])
        x = np.concatenate([val[ret] - val[comp], carve[ret] - carve[comp]])
        pooled = {"d": float(x.mean()), "sd": float(x.std(ddof=1)), "n": len(x),
                  "se": float(x.std(ddof=1) / math.sqrt(TEST_N))}
        claims[name] = {"val": v, "val_pass": bool(v["d"] >= SESOI and v["lo"] > 0), "pooled": pooled}
    m_plan = max(1, sum(c.get("val_pass", False) for c in claims.values()))
    for c in claims.values():
        if "pooled" in c:
            c["p_test"] = p_pass(c["pooled"], m=m_plan)
            c["family"] = c["val_pass"] and c["p_test"] >= T2_MARGIN_P
            c["status"] = "TIER-3 FAMILY" if c["family"] else "VAL PASS, NO MARGIN" if c["val_pass"] else "VAL FAIL"
    desc = {}  # W2: E3 is always printed beside zs - lmcap_ri; descriptive only
    for m in sorted({m for _e, m, _c in T2_CLAIMS}):
        for k, (x, y) in {f"{m}: zs-lmcap_ri": ("zs", None), f"{m}: ret-zs": ("ret", "zs")}.items():
            a, b = f"{m}|{x}", "lmcap_ri|lmcap" if y is None else f"{m}|{y}"
            if a in val and b in val:
                desc[k] = contrast(val[a], val[b])
    family = [k for k, c in claims.items() if c["family"]]
    return {"claims": claims, "m_plan": m_plan, "family": family, "m_holm": len(family), "descriptive": desc}


def cmd_t2(a) -> None:
    if sha(a.carve_ledger) != T1_CARVE_LEDGER_SHA256:
        raise SystemExit(f"{a.carve_ledger}: not the tier-1 carve ledger 4ced15b4")
    carve, _p, _i = set_columns(read_ledgers([a.carve_ledger]), "f30k_carve", "en")
    val, _p, ids = set_columns(read_ledgers(a.ledger), "f30k_val", "en")
    if not ids or sorted(ids) != sorted(f30k_names("val", load_lists())):
        raise SystemExit("t2: the val ledger is not all 1,014 val images")
    res = {"schema": SCHEMA, "label": LABEL, "sesoi": SESOI, "margin_p": T2_MARGIN_P, "carve_ledger_sha256":
           T1_CARVE_LEDGER_SHA256, "val_ledger_sha256": [sha(p) for p in a.ledger], "full": t2_decide(val, carve)}
    if a.exclude:  # PI-1030f: the decision stays on all 1,014; the dedup row is printed beside it
        drop = set(json.loads(Path(a.exclude).read_text(encoding="utf-8"))["exclude"])
        keep = np.array([i not in drop for i in ids])
        if not keep.all():
            res["dedup_beside"] = {"n_excluded": int((~keep).sum()),
                                   **t2_decide({k: v[keep] for k, v in val.items()}, carve)}
    Path(a.out).write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"family": res["full"]["family"], "m_plan": res["full"]["m_plan"],
                      "status": {k: c["status"] for k, c in res["full"]["claims"].items()}}))


# ------------------------------------------------------------------------------------------------ C-T3 (tier 3)
def p_one_sided(x: np.ndarray) -> float:
    """One-sided bootstrap p for mean <= 0 (CC-196 W7): (1 + #{bootstrap means <= 0}) / (B + 1), B = 2,000, seed 0,
    the same index matrix as `contrast`."""
    return float((1 + (x[boot_idx(len(x))].mean(1) <= 0).sum()) / (BOOT + 1))


def holm_adjusted(ps: dict[str, float]) -> dict[str, float]:
    """Holm step-down adjusted p: the j-th smallest gets max over k <= j of min(1, (m - k + 1) p_(k))."""
    out, run = {}, 0.0
    for j, k in enumerate(sorted(ps, key=lambda k: (ps[k], k))):
        run = max(run, min(1.0, (len(ps) - j) * ps[k]))
        out[k] = run
    return out


def t3_decide(test: dict) -> dict:
    """C-T1 PREREG §8 at tier 3: Holm over the family (m = 3, fixed by T2_DECISION) at alpha 0.05; a claim PASSes iff
    point >= SESOI AND its Holm-adjusted one-sided p < 0.05. A claim with a missing arm is NOT RUN and enters Holm
    with p = 1 (m stays 3). W2: zs - lmcap_ri and ret - zs per backbone, descriptive."""
    claims, ps = {}, {}
    for name, m in T3_CLAIMS:
        ret, comp = f"{m}|ret", "lmcap_ri|lmcap"
        if ret not in test or comp not in test:
            claims[name], ps[name] = {"status": "NOT RUN"}, 1.0
            continue
        claims[name] = {"test": contrast(test[ret], test[comp])}
        ps[name] = claims[name]["p_one_sided"] = p_one_sided(np.asarray(test[ret], float) - np.asarray(test[comp], float))
    adj = holm_adjusted(ps)
    for name, c in claims.items():
        c["p_holm"] = adj[name]
        if "test" in c:
            c["status"] = ("TEST FAIL (point < +2.0)" if c["test"]["d"] < SESOI else
                           "TEST FAIL (Holm p >= 0.05)" if adj[name] >= ALPHA else "TEST PASS")
    desc = {}
    for _n, m in T3_CLAIMS:
        for k, (x, y) in {f"{m}: zs-lmcap_ri": (f"{m}|zs", "lmcap_ri|lmcap"), f"{m}: ret-zs": (f"{m}|ret", f"{m}|zs")}.items():
            if x in test and y in test:
                desc[k] = contrast(test[x], test[y])
    return {"claims": claims, "m_holm": len(T3_CLAIMS), "alpha": ALPHA, "descriptive": desc}


def cmd_t3(a) -> None:
    laptop_only("t3")
    if Path(a.out).exists():  # CC-202 W2: the single-look decision is written once
        raise SystemExit(f"REFUSED: {a.out} exists; t3 runs once")
    if sha(a.t2_decision) != T2_DECISION_SHA256:
        raise SystemExit(f"{a.t2_decision}: not the tier-2 decision e29bbe8a")
    t2 = json.loads(Path(a.t2_decision).read_text(encoding="utf-8"))["full"]
    if sorted(t2["family"]) != sorted(n for n, _m in T3_CLAIMS) or t2["m_holm"] != len(T3_CLAIMS):
        raise SystemExit("t3: the tier-2 family is not T3_CLAIMS")
    rows = read_ledgers(a.ledger)
    bad = sorted({r.get("run_id") for r in rows if r.get("dataset") == "f30k_test"} - T3_RUN_IDS)
    if bad:
        raise SystemExit(f"t3: ledger rows of unregistered runs {bad[:3]}")
    test, _p, ids = set_columns(rows, "f30k_test", "en")
    if not ids or sorted(ids) != sorted(f30k_names("test", load_lists())):
        raise SystemExit("t3: the test ledger is not all 1,000 test images")
    res = {"schema": SCHEMA, "label": LABEL, "sesoi": SESOI, "t2_decision_sha256": T2_DECISION_SHA256,
           "test_ledger_sha256": [sha(p) for p in a.ledger], "full": t3_decide(test)}
    if a.exclude:  # PI-1030f test = full near-dup: the decision stays on all 1,000; the dedup row is printed beside it
        drop = set(json.loads(Path(a.exclude).read_text(encoding="utf-8"))["exclude"])
        keep = np.array([i not in drop for i in ids])
        res["neardup_sha256"] = sha(a.exclude)  # CC-202 W2: the row is always written, n_excluded 0 included
        res["dedup_beside"] = {"n_excluded": int((~keep).sum()), **t3_decide({k: v[keep] for k, v in test.items()})}
    Path(a.out).write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: c["status"] for k, c in res["full"]["claims"].items()}))


# ------------------------------------------------------------------------------------------------ self-test
def selftest() -> None:
    ok = []
    # split: counts, salted carve, val/test never in carve or memory, no caption column kept
    rows = [("train", f"t{n}.jpg") for n in range(30)] + [("val", f"v{n}.jpg") for n in range(4)] + \
        [("test", f"s{n}.jpg") for n in range(3)]
    sp = f30k_split(rows, {"train": 30, "val": 4, "test": 3}, 10)
    assert len(sp["carve"]) == 10 and len(sp["memory"]) == 20 and not set(sp["carve"]) & set(sp["memory"])
    assert not (set(sp["carve"]) | set(sp["memory"])) & {f for t, f in rows if t != "train"}
    assert sp == f30k_split(list(reversed(rows)), {"train": 30, "val": 4, "test": 3}, 10), "order-free"
    try:
        f30k_split(rows[:-1], {"train": 30, "val": 4, "test": 3}, 10)
        raise AssertionError("count check")
    except SystemExit:
        pass
    ok.append("split")
    # X1 draws: draw 0 = C's rule (build_memory.exemplars), draws differ and are deterministic, near cut kept
    rng = np.random.default_rng(1)
    mv = rng.normal(size=(40, 8)).astype(np.float32)
    mv /= np.linalg.norm(mv, axis=1, keepdims=True)
    qv = mv[:3].copy()  # each query is a copy of a memory cluster: cosine 1 -> cut
    mk = [f"m{n:05d}" for n in range(40)]
    ds = "ktvic_dev299"
    ref = BM.exemplars(mk + [f"{ds}|q{n}" for n in range(3)], np.concatenate([mv, qv]))
    res = draws(ds, mk, mv, [f"q{n}" for n in range(3)], qv)
    for n in range(3):
        q = f"q{n}"
        assert res["rand"]["0"][q] == ref["rand"][ds][q], "draw 0 parity with build_memory.exemplars"
        assert [c for c, _x in res["ret"][q]] == [c for c, _x in ref["ret"][ds][q]], "ret parity"
        assert mk[n] not in res["ret"][q] and all(mk[n] not in res["rand"][d][q] for d in res["rand"]), "near cut"
        assert len({tuple(res["rand"][d][q]) for d in res["rand"]}) == 3, "draws differ"
    assert draws(ds, mk, mv, ["q0"], qv[:1])["rand"]["2"]["q0"] == res["rand"]["2"]["q0"], "deterministic"
    ok.append("X1 draws (draw-0 parity with C's rule)")
    # prompts
    caps = ["a", "b", "c", "d"]
    p = lmcap_prompt([(caps, "y1"), (caps, "y2"), (caps, "y3")], caps, "vi")
    assert p.count("I am an intelligent image captioning bot.") == 4 and p.count("</s>") == 4 * 4 + 3
    assert p.endswith("describe this image in vietnamese is:") and " y2</s> " in p
    try:
        lmcap_prompt([(caps, "y")], caps, "vi")
        raise AssertionError("N check")
    except SystemExit:
        pass
    cont = rices_content("vi", "T1", ["I1", "I2"], ["x", "y"], "Q")
    assert [c["type"] for c in cont] == ["text", "image", "text", "image", "text", "image", "text"]
    assert cont[-2]["image"] == "Q" and cont[0]["text"] == C.HEADER and cont[-1]["text"] == C.TAILS["T1"]
    assert cont[2]["text"] == C.LINE.format(i=1, caption="x")
    assert text_prompt("vi", "T1", ["x"]) == C.prompt("T1", ["x"]) and text_prompt("en", "T2", ["x"]) == D.prompt("T2", ["x"])
    assert C.template_sha() == C.TEMPLATE_SHA256 and D.template_sha() == D.EN_TEMPLATE_SHA256, "templates unchanged"
    ok.append("prompts (LMCap App. D, RICES interleave, C/C-EN templates unchanged)")
    assert vi_assessable(["một con mèo", "a cat", "con cá"]) == 2 / 3 and vi_assessable(["Đi"]) == 1.0
    ok.append("Vietnamese check")
    # X2 masking
    assert masked("a man rides a red horse", ["the man rides a red bike"]) == "a horse"
    assert masked("x y", ["x y z"]) == "x y", "short captions untouched"
    ok.append("X2 masking")
    # selection
    base = {"arm": "ret", "tau": "-inf", "tpl": "T1", "pcm_vs_zs": 0.0, "verbatim_share": 0.0, "hit_max_rate": 0.0}
    sel = [{**base, "k": k, "order": o, "tpl": t, "run_id": f"r{k}{o}{t}", "cider_s": 30.0} for k, o, t in SEL_GRID]
    sel[5]["cider_s"] = 40.0  # k8 last
    sel[4]["cider_s"] = 45.0
    sel[4]["pcm_vs_zs"] = -2.0  # k8 first: best CIDEr but breaks the precision constraint
    s = select(sel)
    assert (s["k"], s["order"]) == (8, "last") and "constraint_relaxed" not in s
    tie = select([{**r, "cider_s": 30.0, "pcm_vs_zs": 0.0} for r in sel])
    assert (tie["k"], tie["order"], tie["tpl"]) == (2, "last", "T1"), "ties: smaller k, then last, then T1 (DESIGN l.272)"
    t4 = select([{**r, "cider_s": 30.0 + (r["k"] == 4)} for r in sel])
    assert (t4["k"], t4["order"], t4["tpl"]) == (4, "last", "T1"), "k4 last: T1 before T2"
    assert select([{**r, "hit_max_rate": 0.5} for r in sel]) is None, "none eligible: the backbone fails"
    assert select([{**r, "verbatim_share": None} for r in sel]) is None, "unknown copy share is not eligible"
    ok.append("third-backbone selection (C's stage-A rule, W1)")
    # contrasts and labels
    n = 1000
    rng = np.random.default_rng(2)
    rand = rng.normal(30, 10, n)
    ret = rand + 5 + rng.normal(0, 5, n)
    c = contrast(ret, rand)
    assert 4.3 < c["d"] < 5.7 and c["lo"] < c["d"] < c["hi"] and advance(c) == "NOMINATE" and p_pass(c) > 0.98
    for cc in ({"d": 3.0, "se": 1.0}, {"d": 2.2, "se": 0.5}, {"d": 6.0, "se": 1.5}):
        p1, p2 = phi((cc["d"] - SESOI) / cc["se"]), phi(cc["d"] / cc["se"] - NormalDist().inv_cdf(0.95))
        assert p_pass(cc) <= min(p1, p2) + 1e-12 and p_pass(cc) >= 0, "Frechet lower bound (W7)"
        assert p_pass(cc, m=1) >= p_pass(cc, m=2) >= p_pass(cc, m=4), "P falls as the family grows (W12)"
    assert p_pass({"d": 2.8, "se": 0.6}, m=3) < p_pass({"d": 2.8, "se": 0.6}, m=1)
    assert advance({"d": 2.5, "lo": 1.0}) == "WATCH" and advance({"d": 1.0, "lo": -1.0}) == "DROP"
    x1 = contrast_draws(ret, [rand, rand + 1, rand - 1])
    assert abs(x1["d"] - c["d"]) < 1e-9 and abs(x1["between_draw_sd"] - 1.0) < 1e-9
    per = {"qwen25vl_7b|ret": rand - 1, "qwen25vl_7b|rand_d0": rand, "aya_vision_8b|ret": ret,
           "aya_vision_8b|rand_d0": rand, "lmcap_ri|lmcap": rand - 10}
    sm = summarize(per)
    assert sm["killed"] and sm["contrasts"]["aya_vision_8b: ret-rand"]["label"] == "DROP (kill gate)"
    assert sm["contrasts"]["aya_vision_8b: ret-lmcap_ri"]["label"] == "NOMINATE", "baseline claims survive the gate"
    assert not summarize({**per, "qwen25vl_7b|ret": ret})["killed"]
    tri_a = ([1] * 50, [0] * 50, [2] * 50)
    tri_b = ([1] * 25 + [0] * 25, [0] * 50, [2] * 50)
    x3 = pcm_contrast(tri_a, tri_b)
    assert abs(x3["d"] - 25.0) < 1e-9 and x3["lo"] <= 25.0 <= x3["hi"]
    ok.append("contrasts, X1 folding, X3 precision, advance labels, kill gate")
    # budget and registry
    assert sum(BLOCKS.values()) * 1.25 <= CAP_S / 3600 + 1e-9, "block estimates + 25% fit the 20 GPU-h cap"
    reg = registry()
    assert set(reg["models"]) >= {"aya_vision_8b", "xglm_2_9b", "mclip_h14"} and set(reg["borrowed"]) == {"gemma3_4b", "idefics3_8b"}
    for key in ("aya_vision_8b", "xglm_2_9b", "mclip_h14", "xlm_roberta_large", "gemma3_4b", "idefics3_8b"):
        hs = [v["hash"] for v in model_spec(key)["files"].values() if v["kind"] == "sha256"]
        filled = [h for h in hs if h]
        assert not filled or (len(filled) == len(hs) and all(len(h) == 64 and int(h, 16) >= 0 for h in hs)), \
            f"{key}: sha256 pins are all null or all 64-hex (W2)"
    assert not any(pins_open(reg["models"][k]) for k in ("xglm_2_9b", "mclip_h14", "xlm_roberta_large"))
    assert not pins_open(model_spec("idefics3_8b")), "borrowed L1-b pins resolve and are complete"
    ok.append("budget, registry pins")
    # store refuses the repo; summary writes ids and numbers only
    with tempfile.TemporaryDirectory() as tmp:
        led = Path(tmp) / "l.jsonl"
        ids = [f"i{n}" for n in range(n)]
        mk_row = lambda m, arm, v, **kw: {"dataset": "f30k_carve", "model": m, "arm": arm, "tau": "-inf",
                                          "run_id": f"{m}-{arm}", "per_image": {"ids": ids, "cider_ptb": list(v)}, **kw}
        led.write_text("".join(json.dumps(r) + "\n" for r in [
            mk_row("qwen25vl_7b", "ret", ret), mk_row("qwen25vl_7b", "rand", rand, draw=0),
            mk_row("qwen25vl_7b", "rand", rand + 1, draw=1), mk_row("qwen25vl_7b", "ret", ret + 1, img_examples=True)]))
        out = Path(tmp) / "s.json"
        cmd_summary(argparse.Namespace(ledger=[led], out=out))
        s = json.loads(out.read_text())["sets"]["f30k_carve"]
        assert s["confirmatory"] and s["contrasts"]["qwen25vl_7b: ret-rand"]["label"] == "NOMINATE"
        assert "qwen25vl_7b: ret-rand (X1, 2 draws)" in s["contrasts"] and "qwen25vl_7b: ret_img-ret (RICES, descriptive)" in s["contrasts"]
        try:
            cmd_store(argparse.Namespace(out=ROOT / "x.json", csv=None, what="carve_refs"))
            raise AssertionError("store inside the repo")
        except SystemExit as e:
            assert "REFUSED" in str(e)
        kt = Path(tmp) / "kt.jsonl"  # the selection set's 7 ret rows never reach the summary (W3)
        kt.write_text("".join(json.dumps({**mk_row("aya_vision_8b", "ret", ret), "dataset": "ktvic_dev299",
                                          "per_image": {"ids": ids, "cider_s": list(ret)}}) + "\n" for _ in range(7)))
        cmd_summary(argparse.Namespace(ledger=[led, kt], out=out))
        assert "ktvic_dev299" not in json.loads(out.read_text())["sets"]
        vi = Path(tmp) / "vi.jsonl"  # Vietnamese rows: DESCRIPTIVE labels, nn/fix rows ignored
        vi.write_text("".join(json.dumps({**mk_row(m, arm, v, **kw), "dataset": "ov_dev_b",
                                          "per_image": {"ids": ids, "cider_s": list(v)}}) + "\n" for m, arm, v, kw in [
            ("qwen25vl_7b", "ret", ret, {}), ("qwen25vl_7b", "rand", rand, {}), (None, "nn_cons", rand, {"k": 4}),
            (None, "nn_cons", rand, {"k": 8}), ("qwen25vl_7b", "fix", rand, {})]))
        cmd_summary(argparse.Namespace(ledger=[vi], out=out))
        sv = json.loads(out.read_text())["sets"]["ov_dev_b"]
        assert not sv["confirmatory"] and sv["contrasts"]["qwen25vl_7b: ret-rand"]["label"] == "DESCRIPTIVE"
        # C's stage-2 run files admitted only by pin, converted to draw 0 / memory vi
        c2d = Path(tmp) / "c2"
        c2d.mkdir()
        fake = {}
        for name in C2_RUNS:
            f = c2d / name
            f.write_text(json.dumps({"schema": "vsps.lb_decode.v1", "run_id": name.split(".")[0], "dataset": "ov_dev_b",
                                     "model": name.split("_ov_")[0][3:], "spec": {"arm": "zs", "k": 0},
                                     "predictions": {}, "exemplars": {}, "hit_max": {}}))
            fake[name] = sha(f)
        saved = dict(C2_RUNS)
        try:
            C2_RUNS.update(fake)
            got = c2_runs(c2d)
            assert len(got) == 6 and all(r["schema"] == SCHEMA and r["spec"]["draw"] == 0 for r in got)
            C2_RUNS[next(iter(C2_RUNS))] = "0" * 64
            try:
                c2_runs(c2d)
                raise AssertionError("c2 pin")
            except SystemExit:
                pass
        finally:
            C2_RUNS.clear()
            C2_RUNS.update(saved)
        # W4 guard
        g = Path(tmp) / "g"
        (g / "x").mkdir(parents=True)
        (g / "x" / "ok.jpg").write_text("")
        assert guard_problems([g], {"v1.jpg"}) == []
        for bad_name in ("a.zip", "a.tar", "v1.jpg", "flickr30k-images"):
            (g / "x" / bad_name).write_text("")
            assert guard_problems([g], {"v1.jpg"}), bad_name
            (g / "x" / bad_name).unlink()
        # AMENDMENT_1 isolation: deny rules, symlink escapes, extra datasets dirs, and the open() hook in a child
        ncs, outs = Path(tmp) / "ncs", Path(tmp) / "out"
        for d in ("datasets/c_t1_f30k_carve/images", "f30k_raw", "ade20k_raw", "models/m"):
            (ncs / d).mkdir(parents=True)
        for d in ("c_t3", "c_t2", "c_en", "c_test"):
            (outs / d).mkdir(parents=True)
        files = {"carve_img": ncs / "datasets/c_t1_f30k_carve/images/t1.jpg", "model": ncs / "models/m/w.bin",
                 "restored": outs / "c_en/cen_memory_emb.npz", "own_output": outs / "c_t3/a.json",
                 "elsewhere": Path(tmp) / "elsewhere.txt", "f30k_zip": ncs / "f30k_raw/flickr30k-images.zip",
                 "f30k_raw": ncs / "f30k_raw/x.jpg", "ade20k": ncs / "ade20k_raw/y.png",
                 "test_side": outs / "c_en/emb_coco_test.npz", "c_test": outs / "c_test/a.json",
                 "val_name": ncs / "models/m/v1.jpg", "archive": outs / "c_t3/x.tar", "tier1_output": outs / "c_t2/a.json"}
        allowed = {"carve_img", "model", "restored", "own_output", "elsewhere"}
        for f in files.values():
            f.write_text("x")
        link = ncs / "datasets/c_t1_f30k_carve/images/esc.jpg"
        link.symlink_to(files["f30k_raw"])
        named = {"named_val": ncs / "datasets/c_t1_f30k_carve/images/v1.jpg",
                 "named_zip": ncs / "datasets/c_t1_f30k_carve/images/flickr30k-images.zip"}
        for f in named.values():  # CC-176 W2: a refused or archive name that points to an allowed file
            f.symlink_to(files["carve_img"])
        cfg = iso_config(ncs, outs, [str(files["restored"])], {"v1.jpg"})
        for k, f in files.items():
            assert (iso_denied(f, cfg) is None) == (k in allowed), k
        assert iso_denied(link, cfg), "a symlink into a denied dir is denied"
        assert all(iso_denied(f, cfg) for f in named.values()), "a denied name is denied even if it resolves to an allowed file"
        assert iso_denied(outs / "c_t2/x.tar.zst", cfg) and iso_denied(outs / "c_t2/x.7z", cfg), "N6 archive forms"
        (ncs / "datasets/extra").mkdir()
        gp = guard_problems([ncs / "datasets/c_t1_f30k_carve"], {"v1.jpg"}, cfg, ncs / "datasets")
        assert any("esc.jpg" in x for x in gp) and any(x.endswith("extra") for x in gp), gp
        probe = {k: str(f) for k, f in files.items()} | {"link": str(link)} | {k: str(f) for k, f in named.items()}
        child = (f"import json, os, sys; sys.argv = ['x']; sys.path.insert(0, {str(Path(__file__).parent)!r})\n"
                 "import c_t3 as T\n"
                 f"T.iso_install(T.iso_config({str(ncs)!r}, {str(outs)!r}, [{str(files['restored'])!r}], {{'v1.jpg'}}))\n"
                 "res = {}\n"
                 "for k, p in json.loads(sys.stdin.read()).items():\n"
                 "    for how, fn in (('open', lambda: open(p).read()), ('os.open', lambda: os.close(os.open(p, os.O_RDONLY)))):\n"
                 "        try:\n            fn(); res[k + ' ' + how] = 'read'\n"
                 "        except PermissionError:\n            res[k + ' ' + how] = 'refused'\n"
                 "print(json.dumps(res))\n")
        import subprocess
        r = subprocess.run([sys.executable, "-c", child], input=json.dumps(probe), capture_output=True, text=True)
        assert r.returncode == 0, r.stderr[-500:]
        want = {f"{k} {h}": "read" if k in allowed else "refused" for k in probe for h in ("open", "os.open")}
        assert json.loads(r.stdout) == want, "the hook refuses exactly the denied paths"
        live = iso_default()  # the real config: other one-look files are denied, the staged ones are not
        lists = load_lists()  # C-T3: no Flickr30K name is refused; test is read from c_t3_f30k_test only
        assert len(live["files_ok"]) == 6 and live["refused"] == set()
        v0, t0 = f30k_names("val", lists)[0], f30k_names("test", lists)[0]
        assert iso_denied(f"/root/ncs-data/datasets/c_t2_f30k_val/images/{v0}", live) is None, "a val image is readable"
        assert iso_denied(f"/root/ncs-data/datasets/c_t3_f30k_test/images/{t0}", live) is None, "a test image is readable"
        for p in (f"/root/ncs-data/f30k_raw/{t0}", "/root/outputs/c_t1/out/x.json", "/root/outputs/c_t2/out/x.json"):
            assert iso_denied(p, live), p
        for p in ("/root/ncs-data/f30k_raw/flickr30k-images.zip", "/root/ncs-data/ade20k_raw/ADEChallengeData2016.zip",
                  "/root/ncs-data/datasets/c_test/x.jpg", "/root/outputs/c_test/x.json",
                  "/root/outputs/c_en/emb_coco_test.npz", "/root/outputs/c_stage2/runs/x.json"):
            assert iso_denied(p, live), p
        for p in ("/root/ncs-data/datasets/c_t1_f30k_carve/images/a.jpg", "/root/outputs/c_en/cen_memory_emb.npz",
                  "/root/outputs/c_t3/out/x.json", "/root/ncs-data/models/c_t1_xglm_2_9b/config.json"):
            assert iso_denied(p, live) is None, p
    ok.append("summary end to end (dev299 skipped, VI descriptive), C2 pins, guard, store refusal")
    ok.append("AMENDMENT_1 isolation (deny rules, symlink escape, datasets allow-list, open/os.open hook in a child)")
    selftest_t2(ok)
    selftest_t3(ok)
    print("selftest ok: " + "; ".join(ok))


def selftest_t2(ok: list) -> None:
    """C-T3 admission (test admitted, only from its own staged list), the kept tier-2 rule, the exact-sha check."""
    lists = load_lists()
    val, test = f30k_names("val", lists), f30k_names("test", lists)
    assert len(val) == 1014 and len(test) == 1000 and set(F30K) == {"f30k_carve", "f30k_val", "f30k_test"}
    try:
        f30k_names("train", lists)
        raise AssertionError("train must be refused")
    except SystemExit as e:
        assert "REFUSED" in str(e)
    assert extract_want(lists) == {"test": set(test)} and not extract_want(lists)["test"] & set(val)
    try:
        extract_want({**lists, "refuse": {"val": val, "test": test[1:] + val[:1]}})
        raise AssertionError("extract must refuse a test list that holds a val name")
    except SystemExit as e:
        assert "REFUSED" in str(e), e
    with tempfile.TemporaryDirectory() as tmp:
        man = Path(tmp) / "m.json"
        man.write_text(json.dumps({f: "0" * 64 for f in test}))
        assert len(items_of("f30k_test", argparse.Namespace(manifest=man))) == 1000
        man.write_text(json.dumps({f: "0" * 64 for f in test[1:] + val[:1]}))
        try:
            items_of("f30k_test", argparse.Namespace(manifest=man))
            raise AssertionError("a staged val file must be refused as test")
        except SystemExit as e:
            assert "REFUSED" in str(e)
        g = Path(tmp) / "g"
        g.mkdir()
        (g / test[0]).write_text("")
        assert guard_problems([g], refused_names()) == [], "a test image passes the guard at tier 3"
        led = Path(tmp) / "v.jsonl"
        led.write_text("".join(json.dumps({"dataset": ds, "model": "qwen25vl_7b", "arm": "ret", "tau": "-inf",
                                           "run_id": "x", "per_image": {"ids": ids, "cider_ptb": [1.0] * len(ids)}}) + "\n"
                               for ds, ids in (("f30k_val", val), ("f30k_test", test))))
        cmd_summary(argparse.Namespace(ledger=[led], out=Path(tmp) / "s.json"))
        assert not {"f30k_val", "f30k_test"} & set(json.loads((Path(tmp) / "s.json").read_text())["sets"])
    ok.append("C-T3 admission: test admitted from its 1,000-name list only (names, extract, items_of, guard), "
              "summary skips val and test")
    # decision rule (§8 + CC-191 r5): five claims only, val PASS, single-pass m, margin, NOT RUN, W2 rows
    rng = np.random.default_rng(3)
    nv, nc = 1014, 1000

    def arms(n: int, shift: dict) -> dict:
        b = rng.normal(40, 10, n)
        return {k: b + s + rng.normal(0, 5, n) for k, s in shift.items()}
    shift = {"aya_vision_8b|ret": 6, "aya_vision_8b|rand_d0": 0, "qwen25vl_7b|ret": 1, "qwen25vl_7b|rand_d0": 0,
             "internvl3_8b|ret": 40, "internvl3_8b|rand_d0": 41, "lmcap_ri|lmcap": -30, "aya_vision_8b|zs": -40,
             "qwen25vl_7b|zs": -10, "internvl3_8b|zs": 35}
    v, c = arms(nv, shift), arms(nc, shift)
    r = t2_decide(v, c)
    assert len(r["claims"]) == 5 and not any(k.startswith(("E1 internvl3", "E2 internvl3")) or "internvl3_8b: ret-rand" in k
                                             for k in r["claims"]), "InternVL3 ret-rand is never a claim (W4)"
    assert r["claims"]["E2 qwen25vl_7b: ret-rand"]["status"] == "VAL FAIL" and r["m_plan"] == 4 and r["m_holm"] == 4
    assert r["claims"]["E1 aya_vision_8b: ret-rand"]["pooled"]["n"] == nv + nc
    assert {"aya_vision_8b: zs-lmcap_ri", "internvl3_8b: zs-lmcap_ri", "qwen25vl_7b: zs-lmcap_ri"} <= set(r["descriptive"])
    v2 = {**v, "qwen25vl_7b|ret": v["qwen25vl_7b|rand_d0"] + 2.2 + np.tile([6.0, -6.0], nv // 2)}  # val PASS, thin margin
    c2 = {**c, "qwen25vl_7b|ret": c["qwen25vl_7b|rand_d0"] + 2.2 + np.tile([6.0, -6.0], nc // 2)}
    r2 = t2_decide(v2, c2)
    q = r2["claims"]["E2 qwen25vl_7b: ret-rand"]
    assert q["val_pass"] and q["p_test"] < 0.98 and q["status"] == "VAL PASS, NO MARGIN" and r2["m_plan"] == 5
    assert r2["m_holm"] == 4 and abs(q["p_test"] - p_pass(q["pooled"], m=5)) < 1e-12, "m = val passes, one pass"
    r3 = t2_decide({k: x for k, x in v.items() if k != "aya_vision_8b|rand_d0"}, c)
    assert r3["claims"]["E1 aya_vision_8b: ret-rand"] == {"status": "NOT RUN", "family": False} and r3["m_plan"] == 3
    d = exact_dups({"a": "h1", "b": "h2", "c": "h1", "d": "h9"}, {"x": ["f", "h2"]}, {"e": "h9"})
    assert d == {"memory": ["b"], "carve": ["d"], "within_val": ["c"], "exclude": ["b", "c", "d"]}
    with tempfile.TemporaryDirectory() as tmp:  # cmd_t2 end to end with a stand-in carve ledger pin
        def rows(ds: str, ids: list, cols: dict) -> str:
            out = []
            for k, x in cols.items():
                mdl, arm = k.split("|")
                out.append(json.dumps({"dataset": ds, "model": mdl, "arm": arm.split("_")[0], "tau": "-inf",
                                       "draw": 0, "run_id": f"{ds}-{k}", "variant": "plain",
                                       "per_image": {"ids": ids, "cider_ptb": list(x)}}))
            return "\n".join(out) + "\n"
        cl, vl, ex, out = (Path(tmp) / n for n in ("c.jsonl", "v.jsonl", "x.json", "t2.json"))
        cl.write_text(rows("f30k_carve", [f"c{n}" for n in range(nc)], c))
        vl.write_text(rows("f30k_val", val, v))
        ex.write_text(json.dumps({"exclude": val[:14]}))
        saved = T1_CARVE_LEDGER_SHA256
        try:
            globals()["T1_CARVE_LEDGER_SHA256"] = sha(cl)
            cmd_t2(argparse.Namespace(carve_ledger=cl, ledger=[vl], exclude=ex, out=out))
        finally:
            globals()["T1_CARVE_LEDGER_SHA256"] = saved
        res = json.loads(out.read_text())
        assert res["full"]["m_holm"] == 4 and res["dedup_beside"]["n_excluded"] == 14
        assert res["dedup_beside"]["claims"]["E1 aya_vision_8b: ret-rand"]["val"]["n"] == 1000
        try:
            cmd_t2(argparse.Namespace(carve_ledger=cl, ledger=[vl], exclude=None, out=out))
            raise AssertionError("carve ledger pin")
        except SystemExit as e:
            assert "4ced15b4" in str(e), e
    ok.append("C-T2 decision (5 claims, val PASS, single-pass m, 0.98 margin, NOT RUN, W2 rows, W4), dupcheck, t2 CLI")


def selftest_t3(ok: list) -> None:
    """C-T3: registered runs only on test, one-sided bootstrap p, Holm, statuses, the dedup row, pins, laptop-only."""
    for rid in T3_RUN_IDS:
        t3_allowed("f30k_test", rid)
    for rid in ("t3_aya_vision_8b_f30k_test-rand-k4--T1-d0-mcoco", "t3_qwen25vl_7b_f30k_test-rand-k8--T1-d0-mcoco",
                "t3_aya_vision_8b_f30k_test-ret-k8-last-T1-mcoco", "t3_lmcap-ri_f30k_test-mcoco-smoke",
                "t3_aya_vision_8b_f30k_test-zs-smoke", "t3_lmcap-se_f30k_test-mcoco"):
        try:
            t3_allowed("f30k_test", rid)
            raise AssertionError(f"{rid} must be refused on test")
        except SystemExit as e:
            assert "REFUSED" in str(e)
    t3_allowed("f30k_val", "t3_aya_vision_8b_f30k_val-rand-k4--T1-d0-mcoco")
    assert len(T3_RUN_IDS) == 7 and not any("rand" in r for r in T3_RUN_IDS), "E1/E2 never touch test"
    rng = np.random.default_rng(4)
    assert p_one_sided(rng.normal(5, 1, 1000)) == 1 / (BOOT + 1) and 0.4 < p_one_sided((z := rng.normal(0, 1, 1000)) - z.mean()) < 0.6
    h = holm_adjusted({"a": 0.01, "b": 0.02, "c": 0.04})
    assert all(abs(h[k] - v) < 1e-12 for k, v in {"a": 0.03, "b": 0.04, "c": 0.04}.items())
    h = holm_adjusted({"a": 0.03, "b": 0.01, "c": 0.5})
    assert all(abs(h[k] - v) < 1e-12 for k, v in {"b": 0.03, "a": 0.06, "c": 0.5}.items()), "step-down, monotone"
    n = TEST_N
    base = rng.normal(40, 10, n)
    test = {"lmcap_ri|lmcap": base, "aya_vision_8b|ret": base + 25 + rng.normal(0, 5, n),
            "internvl3_8b|ret": base + 1.5 + rng.normal(0, 1, n), "qwen25vl_7b|ret": base + 2.5 + np.tile([60.0, -60.0], n // 2),
            "aya_vision_8b|zs": base - 10, "internvl3_8b|zs": base + 1, "qwen25vl_7b|zs": base + 1}
    r = t3_decide(test)
    st = {k: c["status"] for k, c in r["claims"].items()}
    assert st == {"E3 aya_vision_8b: ret-lmcap_ri": "TEST PASS", "E3 internvl3_8b: ret-lmcap_ri": "TEST FAIL (point < +2.0)",
                  "E3 qwen25vl_7b: ret-lmcap_ri": "TEST FAIL (Holm p >= 0.05)"}, st
    assert r["m_holm"] == 3 and len(r["descriptive"]) == 6
    r2 = t3_decide({k: v for k, v in test.items() if k != "qwen25vl_7b|ret"})
    q = r2["claims"]["E3 qwen25vl_7b: ret-lmcap_ri"]
    assert q == {"status": "NOT RUN", "p_holm": 1.0} and r2["m_holm"] == 3, "NOT RUN keeps m = 3 with p = 1"
    lists = load_lists()
    ids = f30k_names("test", lists)
    with tempfile.TemporaryDirectory() as tmp:
        def row(key: str, x: np.ndarray, rid: str) -> str:
            mdl, arm = key.split("|")
            return json.dumps({"dataset": "f30k_test", "model": mdl, "arm": arm, "tau": "-inf", "variant": "plain",
                               "run_id": rid, "per_image": {"ids": ids, "cider_ptb": list(x)}}) + "\n"
        rid = {"lmcap_ri|lmcap": "t3_lmcap-ri_f30k_test-mcoco"} | {
            f"{m}|ret": next(i for i in T3_RUN_IDS if i.startswith(f"t3_{m}_") and "-ret-" in i) for _n, m in T3_CLAIMS} | {
            f"{m}|zs": f"t3_{m}_f30k_test-zs" for _n, m in T3_CLAIMS}
        led, t2, ex, out = (Path(tmp) / x for x in ("t.jsonl", "t2.json", "nd.json", "t3.json"))
        led.write_text("".join(row(k, v, rid[k]) for k, v in test.items()))
        t2.write_text(json.dumps({"full": {"family": [n for n, _m in T3_CLAIMS], "m_holm": 3}}))
        ex.write_text(json.dumps({"exclude": ids[:10]}))
        saved, saved_mid = T2_DECISION_SHA256, MACHINE_ID
        try:  # the job runs this selftest on M1: the laptop-only check is tested separately below
            globals()["MACHINE_ID"] = Path(tmp) / "absent"
            globals()["T2_DECISION_SHA256"] = sha(t2)
            cmd_t3(argparse.Namespace(ledger=[led], t2_decision=t2, exclude=ex, out=out))
            res = json.loads(out.read_text())
            assert res["dedup_beside"]["n_excluded"] == 10 and res["full"]["claims"][T3_CLAIMS[0][0]]["test"]["n"] == 1000
            assert res["dedup_beside"]["claims"][T3_CLAIMS[0][0]]["test"]["n"] == 990
            try:  # W2: an existing decision is never overwritten
                cmd_t3(argparse.Namespace(ledger=[led], t2_decision=t2, exclude=ex, out=out))
                raise AssertionError("existing --out")
            except SystemExit as e:
                assert "exists" in str(e), e
            ex.write_text(json.dumps({"exclude": []}))
            out0 = Path(tmp) / "t3_0.json"
            cmd_t3(argparse.Namespace(ledger=[led], t2_decision=t2, exclude=ex, out=out0))
            r0 = json.loads(out0.read_text())
            assert r0["dedup_beside"]["n_excluded"] == 0 and r0["dedup_beside"]["claims"] == r0["full"]["claims"], "W2"
            out = Path(tmp) / "never.json"  # the refusal cases below must fail before any write
            for bad, why in ((row("aya_vision_8b|rand", base, "t3_aya_vision_8b_f30k_test-rand-k4--T1-d0-mcoco"), "unregistered"),
                             (None, "not all 1,000")):
                led2 = Path(tmp) / "b.jsonl"
                led2.write_text(led.read_text() + bad if bad else led.read_text().replace(ids[0], "x.jpg"))
                try:
                    cmd_t3(argparse.Namespace(ledger=[led2], t2_decision=t2, exclude=None, out=out))
                    raise AssertionError(why)
                except SystemExit as e:
                    assert why in str(e), e
            t2.write_text(json.dumps({"full": {"family": [T3_CLAIMS[0][0]], "m_holm": 1}}))
            globals()["T2_DECISION_SHA256"] = sha(t2)
            try:
                cmd_t3(argparse.Namespace(ledger=[led], t2_decision=t2, exclude=None, out=out))
                raise AssertionError("family pin")
            except SystemExit as e:
                assert "T3_CLAIMS" in str(e), e
        finally:
            globals()["T2_DECISION_SHA256"] = saved
        try:
            globals()["MACHINE_ID"] = Path(tmp) / "absent"
            cmd_t3(argparse.Namespace(ledger=[led], t2_decision=t2, exclude=None, out=out))
            raise AssertionError("T2_DECISION pin")
        except SystemExit as e:
            assert "e29bbe8a" in str(e), e
        finally:
            globals()["MACHINE_ID"] = saved_mid
        assert not out.exists(), "refusals wrote nothing"
        mid = Path(tmp) / "mid"
        mid.write_text("m3\n")
        try:
            globals()["MACHINE_ID"] = mid
            for what in ("store", "score", "t3"):
                try:
                    laptop_only(what)
                    raise AssertionError(f"{what} on a GPU host")
                except SystemExit as e:
                    assert "laptop only" in str(e)
        finally:
            globals()["MACHINE_ID"] = saved_mid
    ok.append("C-T3 decision (registered runs only, bootstrap p +1, Holm m = 3, PASS/FAIL/NOT RUN, dedup beside, "
              "T2_DECISION and family pins, laptop-only store/score/t3, write-once out, dedup row always written)")


# ------------------------------------------------------------------------------------------------ CLI
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("lists")
    p.add_argument("--csv", type=Path, required=True)
    p = sub.add_parser("store")
    p.add_argument("--csv", type=Path, required=True)
    p.add_argument("--what", choices=("carve_refs", "val_refs", "test_refs", "f30k_memory"), required=True)
    p.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("draws")
    for k in ("mem_emb", "query_emb", "out"):
        p.add_argument("--" + k.replace("_", "-"), type=Path, required=True)
    p.add_argument("--set", choices=sorted(SETS), required=True)
    p.add_argument("--ex", type=Path, help="C's committed example file: draw-0 and ret parity check")
    p = sub.add_parser("embed")
    p.add_argument("--set", choices=("f30k_carve", "f30k_val", "f30k_test", "f30k_memory"), required=True)
    for k in ("images", "snapshot", "manifest", "out"):
        p.add_argument("--" + k, type=Path, required=True)
    for name in ("decode", "lmcap"):
        p = sub.add_parser(name)
        p.add_argument("--set", choices=sorted(SETS), required=True)
        for k in ("images", "out_dir", "captions", "ex", "manifest", "c_lists", "mem_images", "mem_files"):
            p.add_argument("--" + k.replace("_", "-"), type=Path)
        p.add_argument("--memory", choices=("vi", "coco", "f30k"), default="vi")
        p.add_argument("--limit", type=int, default=0, help="W-d smoke: first N images only, never scored")
        if name == "decode":
            p.add_argument("--model", choices=OLD + THIRD, required=True)
            p.add_argument("--snapshot", type=Path, required=True)
            p.add_argument("--arm", choices=("zs", "ret", "rand", "ret_img"), required=True)
            p.add_argument("--k", type=int, default=0)
            p.add_argument("--order", choices=("first", "last"))
            p.add_argument("--tpl", choices=("T1", "T2"))
            p.add_argument("--draw", type=int, choices=DRAWS, default=0)
        else:
            p.add_argument("--variant", choices=("ri", "se"), required=True)
            p.add_argument("--xglm", type=Path, required=True)
            p.add_argument("--mclip", type=Path, required=True)
            p.add_argument("--mem-emb", type=Path, required=True)
            p.add_argument("--query-emb", type=Path, required=True)
    p = sub.add_parser("score")
    p.add_argument("--set", choices=sorted(SETS), required=True)
    p.add_argument("--runs", type=Path, nargs="+", required=True)
    p.add_argument("--ledger", type=Path, required=True)
    for k in ("kit_b", "c_lists", "refs", "captions", "c2_dir", "c2_ledger"):
        p.add_argument("--" + k.replace("_", "-"), type=Path)
    p.add_argument("--memory", choices=("vi", "coco", "f30k"), default=None)
    p = sub.add_parser("extract")
    p.add_argument("--zip", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("guard")
    p.add_argument("--roots", nargs="+", required=True)
    p.add_argument("--datasets", type=Path, help="AMENDMENT_1: $NCS_DATA/datasets may hold only C-T1's staged dirs")
    p = sub.add_parser("memcheck")
    p.add_argument("--mem-files", type=Path, required=True)
    p.add_argument("--root", type=Path, required=True)
    for name in ("fetch", "pinsok"):
        p = sub.add_parser(name)
        p.add_argument("--model", choices=FETCHABLE, required=True)
        p.add_argument("--snapshot", type=Path, required=True)
    p = sub.add_parser("t1check")
    p.add_argument("--mclip", type=Path, required=True)
    p = sub.add_parser("memfiles")
    p.add_argument("--memory", choices=("vi", "coco"), required=True)
    p.add_argument("--c-lists", type=Path)
    p.add_argument("--cen-memory", type=Path)
    p.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("vicheck")
    p.add_argument("--preds", type=Path, required=True)
    p = sub.add_parser("cfg")
    p.add_argument("--file", type=Path, required=True)
    p = sub.add_parser("select")
    p.add_argument("--ledger", type=Path, required=True)
    p.add_argument("--model", choices=THIRD, required=True)
    p.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("summary")
    p.add_argument("--ledger", type=Path, nargs="+", required=True)
    p.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("t2")
    p.add_argument("--ledger", type=Path, nargs="+", required=True)
    p.add_argument("--carve-ledger", type=Path, required=True)
    p.add_argument("--exclude", type=Path, help="dupcheck.json: PI-1030f row printed beside the full decision")
    p.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("t3")
    p.add_argument("--ledger", type=Path, nargs="+", required=True)
    p.add_argument("--t2-decision", type=Path, required=True)
    p.add_argument("--exclude", type=Path, help="neardup.json: PI-1030f row printed beside the full decision")
    p.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("dupcheck")
    for k in ("manifest", "mem_files", "carve_manifest", "out"):
        p.add_argument("--" + k.replace("_", "-"), type=Path, required=True)
    for name in ("lock", "left"):
        p = sub.add_parser(name)
        p.add_argument("--path", type=Path)
        p.add_argument("--used", type=Path)
        p.add_argument("--marker", type=Path)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.cmd in ISO_CMDS and machine_id() in ("m3", "m4"):  # AMENDMENT_1: on a GPU host, always under the hook
        iso_install(iso_default())

    def lock():
        import b1
        b1.take_lock(a.path)

    def left():
        import b1
        print(b1.left(a.used, a.marker, CAP_S))

    {"lists": lambda: cmd_lists(a), "store": lambda: cmd_store(a), "draws": lambda: cmd_draws(a),
     "embed": lambda: cmd_embed(a), "decode": lambda: cmd_decode(a), "lmcap": lambda: cmd_lmcap(a),
     "score": lambda: cmd_score(a), "memfiles": lambda: cmd_memfiles(a), "vicheck": lambda: cmd_vicheck(a),
     "cfg": lambda: cmd_cfg(a), "extract": lambda: cmd_extract(a), "guard": lambda: cmd_guard(a),
     "memcheck": lambda: cmd_memcheck(a), "fetch": lambda: cmd_fetch(a), "pinsok": lambda: cmd_pinsok(a),
     "t1check": lambda: cmd_t1check(a), "select": lambda: cmd_select(a), "summary": lambda: cmd_summary(a), "t2": lambda: cmd_t2(a), "t3": lambda: cmd_t3(a),
     "dupcheck": lambda: cmd_dupcheck(a), "lock": lock, "left": left
     }.get(a.cmd, ap.print_help)()


if __name__ == "__main__":
    main()
