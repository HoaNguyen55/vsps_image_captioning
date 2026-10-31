#!/usr/bin/env python3
"""VSPS-J M0: Vintern-1B-v3_5 single-probe yes/no-logit detection recall, cross-lingual
(manuscript/prereg/2026-10-31_vsps_j_m0/PREREG.md). Zero-shot (arm A) vs 2-shot (arm B) on M-HalDetect val.

    python3 -I scripts/vsps_j_m0/m0.py selftest        CPU, no weights, no data (needs numpy + torch)
    python3 -I scripts/vsps_j_m0/m0.py plan            laptop: custody, counts, demos, smoke pins -> prereg folder (ids only)
    python3 -I scripts/vsps_j_m0/m0.py probe --data D --images I --model SNAP --out O [--device cuda] [--smoke-n 50]
    python3 -I scripts/vsps_j_m0/m0.py score --data D --out O --res R.json     laptop, after the probe run

No M-HalDetect text is written to the repo: the plan holds ids, labels, counts and text sha256 only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import re
import statistics
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(Path(__file__).resolve().parent)]  # -I drops both; trusted repo code
PDIR = ROOT / "manuscript/prereg/2026-10-31_vsps_j_m0"
PLAN = PDIR / "m0_plan.json"
MH = ".session_backup/2026-10-19/HL_human_labels/dl_mhaldetect"
PIN = {  # A-N3 pins (CC-207 W3/W4) and custody inputs
    "val_raw.json": "2cbc7942f2ceafb0312f4f41b79390fe600605ffda9a9591fd2346213d0389af",
    "train_raw.json": "03b088d113d94e6f7ebd939fe2040d9fb968f26878b088da77ed8d885ae17624",
    "overlap": "fd97a3b0259b8f1463afa180eebdc93ab5fce7373e58fd51c1eb0fa33a157a32",
    "karpathy": "2fd999220673258012acfb411a4e7e66af7d488050b2519b0badcc49b7600b8d",
    "at3_list": "5aaa479fa57f9749ecd1258ae7a9f91d8b0e9b322ea1fd4418a5f91b1354db26",
    "at3_ids": "b0aefdb4a61c8099369d7f42a5625ab5aa83ec310a9f28f04bc2f00102727215",
    "kv4224_ids": "86d9386324e8cb34c4c7216e494b21da0cbcfe458702952b9ce261a9f608f8f9",
    "exclusion": "c52a96d18925b974878ae1a970c3f9133fb3482216676fd41871eeabb68cc77f",
    "ut2532": "288340b8ff7a3ca675f78c7e88bafad09c68f37a182b6c9ec0f4b786f5cb3a88",
}
EXCLUSION = ROOT / "manuscript/prereg/2026-10-21_dev_pools/exclusion.json"
UT2532 = ROOT / "manuscript/prereg/2026-10-27_grl_pilot/ut2532.txt"
MODEL = {"name": "vintern-1b", "repo": "5CD-AI/Vintern-1B-v3_5", "revision": "b98f263eab246eb5269ade64edbdca8a887dc44d",
         "files": {"model.safetensors": "296a16a6bf28e6d3f0fb9298deba70b3cfa1d7519f4aa326e2f862bf2e63be05",
                   "modeling_internvl_chat.py": "4935c1f1d205167150d4449cbaf4bf340d8d5d0fd96ca97be5d15b26d489ead1",
                   "conversation.py": "7e457a0fc08304deeb386ed1932e9db88dfbca888e0649ff76d488ae6c8aebfe",
                   "config.json": "1c9ddcbef42ce4c672fefeb6c217be0ba05429f91ef1e3401cdb78eda17533fb"},
         "max_tiles": 4}
SEED, CAP_H, MASS_FLOOR, TEXT_OK, EQUIV_TOL = 20261031, 5.0, 0.5, 0.9, 1e-3  # m0_stats.SEED is the same value (selftest)
N_PROJ, SMOKE_SEGS, DEMO_WORDS = 50, 2, (5, 30)
ELIGIBLE = ("ACCURATE", "INACCURATE")
GEN_CFG = {"max_new_tokens": 1, "do_sample": False, "num_beams": 1, "repetition_penalty": 1.05}
YES_NO = ("có", "không")

# Claim-type keyword rule (PREREG section 5), first match wins: count > attribute > relation > object.
_W = lambda *w: re.compile(r"\b(" + "|".join(w) + r")\b")  # noqa: E731
TYPE_RULES = (
    ("count", _W(r"\d+", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
                 "twelve", "dozen", "dozens", "couple", "pair", "several", "few", "many", "multiple", "numerous",
                 "single", "both", "lone", "group", "groups")),
    ("attribute", _W("red", "blue", "green", "yellow", "white", "black", "brown", "gray", "grey", "orange", "pink",
                     "purple", "silver", "gold", "golden", "colorful", "colored", "dark", "light", "bright", "large",
                     "small", "big", "little", "tall", "short", "long", "tiny", "huge", "wooden", "metal", "plastic",
                     "glass", "stone", "brick", "old", "young", "new", "empty", "full", "open", "closed", "wet",
                     "striped", "round", "square")),
    ("relation", _W("on", "under", "above", "below", "behind", "beside", "near", "between", "inside", "next to",
                    "in front of", "on top of", "across", "along", "against", "holding", "riding", "carrying",
                    "wearing", "using", "eating", "playing", "watching", "looking at", "sitting", "standing",
                    "walking", "lying", "leaning", "hanging", "parked")),
)


def claim_type(span: str) -> str:
    s = span.lower()
    return next((name for name, rx in TYPE_RULES if rx.search(s)), "object")


def question(span: str) -> str:
    """Span-to-question rule (W1): English span inside the Vietnamese co/khong template; no MT."""
    s = re.sub(r"\s+", " ", span).strip().rstrip(".,;:!?").strip()
    return f'Có đúng là "{s}" không'


def instruct(q: str) -> str:
    """Byte-identical to VinternAdapter.yes_no_logit(instruct=True)."""
    return f"{q.rstrip('?')}? Chỉ trả lời 'có' hoặc 'không'."


def chat_args(q: str, demo_qa: list, demo_n: list, query_n: int):
    """(history, question, num_patches_list) for the pinned chat() (modeling_internvl_chat.py l.252-284).
    0 demos: exactly what yes_no_logit passes (history None, auto num_patches_list). With demos: chat() does not
    prepend <image> when history is set, so every turn carries its own; placeholders fill in order demo1, demo2, query."""
    if not demo_qa:
        return None, f"<image>\n{instruct(q)}", None
    history = [(f"<image>\n{instruct(dq)}", da) for dq, da in demo_qa]
    return history, f"<image>\n{instruct(q)}", [*demo_n, query_n]


def sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def sha_text(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def image_id(name: str) -> int:
    return int(re.search(r"(\d+)\.jpg$", name).group(1))


def load(data: Path, name: str) -> list:
    p = data / name
    if sha_file(p) != PIN[name]:
        raise SystemExit(f"FAULT {p}: sha256 is not the A-N3 pin")
    return json.loads(p.read_text(encoding="utf-8"))


def segments(records: list) -> tuple[list, Counter]:
    """Eligible = label ACCURATE/INACCURATE with >= 1 word character. Returns (segments, excluded counts)."""
    out, excl = [], Counter()
    for r, rec in enumerate(records):
        if not rec["annotations"]:
            excl["record_without_spans"] += 1
        for s, a in enumerate(rec["annotations"]):
            if a["label"] not in ELIGIBLE:
                excl[a["label"]] += 1
            elif not re.search(r"\w", a["text"]):
                excl["no_word_character_" + a["label"]] += 1
            else:
                out.append({"rec": r, "seg": s, "image": image_id(rec["image"]), "label": a["label"],
                            "y": int(a["label"] == "INACCURATE"), "type": claim_type(a["text"]), "text": a["text"]})
    return out, excl


# ------------------------------------------------------------------------------------------------ custody (W4)
def custody_sets(val: set, train: set, owned: set, refused: set, ksplit: dict) -> dict:
    """owned = other owners' images (A-T3 3,232, KV-4,224, UIT-ViIC train pool UT-2532): never decoded (PORTFOLIO
    l.185, M0 is registered later). refused = exclusion.json id lists (spent evaluation sets, incl. Karpathy test):
    probed for the full split (CC-207 W4) but held out of every operating-point choice, and out of demos and smoke."""
    drop = (val | train) & owned
    probe = val - drop
    ktest = {i for i in probe if ksplit.get(i) == "test"}
    held = (probe & refused) | ktest
    return {"drop": drop, "probe": probe, "ktest": ktest, "held": held, "op": probe - held,
            "demo_pool": train - val - drop - refused - {i for i in train if ksplit.get(i) == "test"}}


def refused_sets() -> tuple[dict, set]:
    """exclusion.json: ({source: COCO ids}, every listed image sha256)."""
    if sha_file(EXCLUSION) != PIN["exclusion"]:
        raise SystemExit("FAULT exclusion.json pin")
    ex = json.loads(EXCLUSION.read_text(encoding="utf-8"))
    return ({k: {int(i) for i in v} for k, v in ex["ids"]["coco"].items()},
            set().union(*map(set, ex["image_sha256"].values())))


def ut2532() -> set:
    if sha_file(UT2532) != PIN["ut2532"]:
        raise SystemExit("FAULT ut2532.txt pin")
    return {int(x) for x in UT2532.read_text().split()}


def kv4224() -> set:
    """KV-4,224 rebuilt with scripts/grl/id_counts.py's own counts() on its pinned inputs (main() is not called:
    it rewrites the GRL folder). Checked against the MT4 PREREG ids pin."""
    sys.path.insert(0, str(ROOT / "scripts/grl"))
    import id_counts as ic
    for rel, want in ic.INPUTS.items():
        if sha_file(ROOT / rel) != want:
            raise SystemExit(f"FAULT {rel}: not the id_counts pin")
    ld = lambda rel: json.loads((ROOT / rel).read_text(encoding="utf-8"))  # noqa: E731
    ex = ld("manuscript/prereg/2026-10-21_dev_pools/exclusion.json")["ids"]["coco"]
    uv = {s: ld(f"data/datasets/uitviic/{s}_data.json") for s in ("train", "val")}
    tr, va = ({int(i["id"]) for i in uv[s]["images"]} for s in ("train", "val"))
    ks = {int(i["cocoid"]): i["split"] for i in ld("data/datasets/karpathy/dataset_coco.json")["images"]}
    gt = ld(".session_backup/2026-10-14/r12_verify/gt_cache.json")
    touched = {int(k) for k in (*gt["refs"], *gt["inst"],
                                *ld(".session_backup/2026-10-19/HL_human_labels/a_n3_instance_gold.json"))}
    cen = {k: {int(r.split("\t")[0]) for r in (ROOT / f"manuscript/prereg/2026-10-27_c_en/cen_coco_{k}.tsv")
                                          .read_text().splitlines()[1:]} for k in ("kval", "test")}
    got, pools = ic.counts(tr, va, ks, ex, touched, cen)
    kv = pools["kv_pool_a_excluded"]
    if got["kv_pool_a_excluded"] != 4224 or ic.sha_ids(kv) != PIN["kv4224_ids"]:
        raise SystemExit("FAULT KV-4,224 rebuild does not match its pin")
    return kv


def at3_ids() -> set:
    p = ROOT / "manuscript/prereg/2026-10-30_a_t3/r9/a_t3_testlist_r9_drop_all.json"
    L = json.loads(p.read_bytes())
    if sha_file(p) != PIN["at3_list"] or sha_text("\n".join(L["ids"]) + "\n") != PIN["at3_ids"] or L["n"] != 3232:
        raise SystemExit("FAULT A-T3 list is not the CC-197 r9 list")
    return {int(i) for i in L["ids"]}


def pick_demos(train_segs: list, pool: set) -> list:
    """One ACCURATE and one INACCURATE train segment from two different pool images, 5-30 words, by SEED;
    order of the two shuffled by SEED. Never retrieved per query (C owns retrieval ICL)."""
    cand = sorted((s for s in train_segs if s["image"] in pool
                   and DEMO_WORDS[0] <= len(s["text"].split()) <= DEMO_WORDS[1]), key=lambda s: (s["rec"], s["seg"]))
    random.Random(SEED).shuffle(cand)
    acc = next(s for s in cand if s["label"] == "ACCURATE")
    inacc = next(s for s in cand if s["label"] == "INACCURATE" and s["image"] != acc["image"])
    demos = [acc, inacc]
    random.Random(SEED + 1).shuffle(demos)
    return demos


def pick_smoke(train_segs: list, pool: set, n_img: int) -> list:
    imgs = sorted({s["image"] for s in train_segs if s["image"] in pool})
    chosen = sorted(random.Random(SEED + 2).sample(imgs, n_img))
    by = {i: sorted((s for s in train_segs if s["image"] == i), key=lambda s: (s["rec"], s["seg"])) for i in chosen}
    rng = random.Random(SEED + 3)
    return [s for i in chosen for s in rng.sample(by[i], min(SMOKE_SEGS, len(by[i])))]


def image_order(imgs: set) -> list:
    order = sorted(imgs)
    random.Random(SEED + 4).shuffle(order)
    return order


def write_ids(name: str, ids) -> str:
    p = PDIR / name
    p.write_text("".join(f"{i}\n" for i in sorted(ids)), encoding="utf-8")
    return sha_file(p)


def cmd_plan(_args) -> int:
    data = ROOT / MH
    val, train = load(data, "val_raw.json"), load(data, "train_raw.json")
    ov = ROOT / "data/an3/mhaldetect_overlap.json"
    if sha_file(ov) != PIN["overlap"]:
        raise SystemExit("FAULT mhaldetect_overlap.json is not the A-N3 file")
    kp = ROOT / "data/datasets/karpathy/dataset_coco.json"
    if sha_file(kp) != PIN["karpathy"]:
        raise SystemExit("FAULT Karpathy file pin")
    ksplit = {int(i["cocoid"]): i["split"] for i in json.loads(kp.read_text(encoding="utf-8"))["images"]}
    vimg, timg = {image_id(r["image"]) for r in val}, {image_id(r["image"]) for r in train}
    owners = {"a_t3_3232": at3_ids(), "kv4224": kv4224(), "uitviic_train_pool_ut2532": ut2532()}
    ref = refused_sets()[0]
    C = custody_sets(vimg, timg, set().union(*owners.values()), set().union(*ref.values()), ksplit)
    an3 = json.loads(ov.read_text())["mhaldetect"]
    vsplit = Counter(ksplit.get(i) for i in vimg)
    tsplit = Counter(ksplit.get(i) for i in timg)
    if (dict(vsplit) != an3["val"]["karpathy_split"] or dict(tsplit) != an3["train"]["karpathy_split"]
            or len(vimg & timg) != an3["train_val_image_overlap"]):
        raise SystemExit("FAULT Karpathy split recount differs from data/an3/mhaldetect_overlap.json")
    vsegs, vex = segments(val)
    tsegs, _ = segments(train)
    probe_segs = [s for s in vsegs if s["image"] in C["probe"]]
    demos = pick_demos(tsegs, C["demo_pool"])
    smoke_pool = C["demo_pool"] - {d["image"] for d in demos}
    smoke = pick_smoke(tsegs, smoke_pool, N_PROJ)
    order = image_order(C["probe"])
    raw_labels = Counter(a["label"] for r in val for a in r["annotations"])
    by = lambda segs: {t: dict(Counter(s["label"] for s in segs if s["type"] == t))  # noqa: E731
                       for t in ("count", "attribute", "relation", "object")}
    fetch = sorted({f"COCO_val2014_{i:012d}.jpg" for i in C["probe"] | {d["image"] for d in demos}
                    | {s["image"] for s in smoke}})
    plan = {
        "_what": "VSPS-J M0 plan: ids, labels, counts and text sha256 only; no M-HalDetect text",
        "seed": SEED, "pins": PIN, "model": MODEL,
        "val": {"records": len(val), "images": len(vimg), "segments_by_label": dict(raw_labels),
                "label_eligible": sum(raw_labels[k] for k in ELIGIBLE), "probe_eligible": len(vsegs),
                "excluded": dict(vex), "karpathy_split": dict(vsplit)},
        "train": {"records": len(train), "images": len(timg), "karpathy_split": dict(tsplit)},
        "custody": {"train_val_image_overlap": len(vimg & timg),
                    "owned_never_decoded": {k: {"val": len(vimg & v), "train": len(timg & v)} for k, v in owners.items()},
                    "exclusion_json_ids": {k: {"val": len(vimg & v), "train": len(timg & v)} for k, v in ref.items()},
                    "dropped_val_images": len(C["drop"] & vimg), "dropped_train_images": len(C["drop"] & timg),
                    "probe_images": len(C["probe"]), "probe_segments": len(probe_segs),
                    "karpathy_test_in_probe": len(C["ktest"]), "held_out_of_selection": len(C["held"]),
                    "op_images": len(C["op"]),
                    "op_segments": sum(s["image"] in C["op"] for s in probe_segs),
                    "op_inaccurate": sum(s["y"] for s in probe_segs if s["image"] in C["op"]),
                    "probe_inaccurate": sum(s["y"] for s in probe_segs), "demo_pool_images": len(C["demo_pool"])},
        "claim_types_probe": by(probe_segs),
        "demos": [{"rec": d["rec"], "seg": d["seg"], "image": d["image"], "label": d["label"],
                   "answer": "Có." if d["label"] == "ACCURATE" else "Không.", "words": len(d["text"].split()),
                   "text_sha256": sha_text(d["text"])} for d in demos],
        "smoke": [{"rec": s["rec"], "seg": s["seg"], "image": s["image"]} for s in smoke],
        "image_order_sha256": sha_text("".join(f"{i}\n" for i in order)),
        "fetch_images": len(fetch),
        "id_lists": {
            "dev_touched_ids.txt": write_ids("dev_touched_ids.txt", vimg | timg),
            "val_ids.txt": write_ids("val_ids.txt", vimg),
            "train_ids.txt": write_ids("train_ids.txt", timg),
            "karpathy_test_val_ids.txt": write_ids("karpathy_test_val_ids.txt", C["ktest"]),
            "selection_excluded_ids.txt": write_ids("selection_excluded_ids.txt", C["held"]),
            "dropped_ids.txt": write_ids("dropped_ids.txt", C["drop"]),
            "fetch_images.txt": None},
    }
    (PDIR / "fetch_images.txt").write_text("".join(f"{n}\n" for n in fetch), encoding="utf-8")
    plan["id_lists"]["fetch_images.txt"] = sha_file(PDIR / "fetch_images.txt")
    PLAN.write_text(json.dumps(plan, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: plan[k] for k in ("val", "train", "custody")}, indent=1))
    return 0


# ------------------------------------------------------------------------------------------------ probe (GPU)
def probe(ad, pv, q: str, demos: tuple = ()) -> tuple[str, float, float]:
    """One greedy step through the pinned chat(); returns (text, P(yes), yes+no first-token mass).
    Same prompt, config and P(yes) rule as VinternAdapter.yes_no_logit, plus demo turns and the raw mass.
    demos: ((pixel_values, question, answer), ...)."""
    import torch

    lm = ad._model.language_model
    cap: dict = {}
    original = lm.generate

    def generate(*a, **k):
        k.update(output_scores=True, return_dict_in_generate=True)
        out = original(*a, **k)
        cap["scores"] = out.scores
        return out.sequences

    history, quest, npl = chat_args(q, [(d[1], d[2]) for d in demos], [d[0].shape[0] for d in demos], pv.shape[0])
    pixel = torch.cat([*(d[0] for d in demos), pv]) if demos else pv
    lm.generate = generate
    try:
        text = ad._model.chat(ad._tokenizer, pixel, quest, dict(GEN_CFG), history=history, num_patches_list=npl)
    finally:
        lm.generate = original
    probs = torch.softmax(cap["scores"][0][0].float(), dim=-1)
    yes, no = ad._yes_no_ids()
    py, pn = probs[yes].sum().item(), probs[no].sum().item()
    mass = py + pn
    return str(text).strip(), (py / mass if mass > 0 else float("nan")), mass


def text_ok(t: str) -> bool:
    """The one decoded token is a co/khong first token ("c", "kh", "có", ...) or the full word."""
    t = t.strip().lower()
    return bool(t) and any(w.startswith(t) or t.startswith(w) for w in YES_NO)


def demo_pixels(image, dtype, device):
    """Demo images at one 448 tile (no thumbnail): 256 image tokens each, so the 2-shot prompt adds 512 tokens
    to the query's registry tiling (max_tiles 4). Same InternVL transform as the adapter."""
    import torch

    from rescap.vlm.vintern import _build_transform, _dynamic_preprocess

    tiles = _dynamic_preprocess(image, max_num=1, image_size=448, use_thumbnail=True)
    t = _build_transform(448)
    return torch.stack([t(x) for x in tiles]).to(getattr(torch, dtype)).to(device)


def token_check(ad) -> dict:
    yes, no = ad._yes_no_ids()
    dec = lambda ids: [ad._tokenizer.decode([i]).strip().lower() for i in ids]  # noqa: E731
    ok = (bool(yes) and bool(no) and not set(yes) & set(no)
          and all(d and YES_NO[0].startswith(d) for d in dec(yes)) and all(d and YES_NO[1].startswith(d) for d in dec(no)))
    return {"yes_ids": yes, "no_ids": no, "yes_dec": dec(yes), "no_dec": dec(no), "ok": ok}


def smoke_verdict(rows: list, equiv: list) -> dict:
    """W2 smoke rule. Arm A fails -> FAULT (run stops); arm B fails -> arm B dropped, never a model swap."""
    res = {}
    for arm in ("A", "B"):
        r = [x for x in rows if x["arm"] == arm]
        fin = bool(r) and all(math.isfinite(x["p_yes"]) for x in r)
        res[arm] = {"n": len(r), "finite": fin,
                    "median_mass": statistics.median(x["mass"] for x in r) if r else 0.0,
                    "text_ok_share": sum(text_ok(x["text"]) for x in r) / len(r) if r else 0.0}
        res[arm]["ok"] = fin and res[arm]["median_mass"] >= MASS_FLOOR and res[arm]["text_ok_share"] >= TEXT_OK
    res["equiv_max_abs"] = max(equiv) if equiv else float("nan")
    res["equiv_ok"] = bool(equiv) and max(equiv) <= EQUIV_TOL
    res["A"]["ok"] = res["A"]["ok"] and res["equiv_ok"]
    return res


def projection_h(elapsed_h: float, rem: dict, med: dict) -> float:
    """CC-206 binding form, per arm: elapsed + remaining probes x median s/probe (val images 2-50)."""
    return elapsed_h + sum(rem[a] * med[a] for a in rem) / 3600


def append(fh, row: dict) -> None:
    fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def check_model(snap: Path) -> None:
    """The pinned config.json's auto_map names the repo, not the folder, so transformers resolves the remote code
    through the cache's refs/main even for a local path. Load by repo id, offline, with refs/main = the pin."""
    if snap.name != MODEL["revision"]:
        raise SystemExit(f"FAULT model snapshot dir is not revision {MODEL['revision']}")
    ref = snap.parent.parent / "refs" / "main"
    if os.environ.get("HF_HUB_OFFLINE") != "1" or not ref.is_file() or ref.read_text().strip() != MODEL["revision"]:
        raise SystemExit("FAULT need HF_HUB_OFFLINE=1 and refs/main = the pinned revision")
    for f, want in MODEL["files"].items():
        if sha_file(snap / f) != want:
            raise SystemExit(f"FAULT {f}: sha256 differs from the pin")


def sha_refused(shas: dict, refused_sha: set, held: set) -> list:
    """exclusion.json's image_sha256 rule: a fetched image whose bytes are listed is refused unless its id is already
    held out by id (Karpathy test / exclusion lists). Returns the offending ids (expected none)."""
    return sorted(i for i, h in shas.items() if h in refused_sha and i not in held)


STOP = "STOP"  # marker file in --out; written by every non-zero probe exit (CC-208 W1)


def stop_reasons(out: Path) -> list:
    """Recorded stops that make a run final: the STOP marker, a smoke FAULT, a projection with "stop": true."""
    why = [f"marker {STOP}"] if (out / STOP).exists() else []
    for name, key in (("smoke.json", "fault"), ("projection_pre_val.json", "stop"), ("projection.json", "stop")):
        f = out / name
        if f.is_file() and json.loads(f.read_text(encoding="utf-8")).get(key):
            why.append(f"{name} {key}: true")
    return why


def refuse_if_stopped(out: Path) -> None:
    """A stopped run is never resumed (PREREG 7.2). A crash with no marker and no stop record may resume."""
    why = stop_reasons(out)
    if why:
        raise SystemExit(f"REFUSED: run stopped ({'; '.join(why)}); amend, never resume")


def halt(out: Path, rc: int, reason: str, n_img: int | None = None) -> int:
    (out / STOP).write_text(json.dumps({"rc": rc, "reason": reason, "time": time.time(), "n_img": n_img}) + "\n")
    print(reason)
    return rc


def check_scorable(out: Path) -> list:
    """Score only a run with no stop record, a probes file equal to its .sha256 and only finite P(yes)."""
    refuse_if_stopped(out)
    pf, sf = out / "probes.jsonl", out / "probes.jsonl.sha256"
    if not sf.is_file() or sf.read_text().split()[0] != sha_file(pf):
        raise SystemExit("REFUSED: probes.jsonl does not match probes.jsonl.sha256")
    rows = [json.loads(x) for x in pf.read_text(encoding="utf-8").splitlines()]
    bad = sum(not math.isfinite(r["p_yes"]) for r in rows)
    if bad:
        raise SystemExit(f"REFUSED: {bad} non-finite P(yes) rows")
    return rows


def cmd_probe(args) -> int:
    from PIL import Image
    from rescap.vlm.registry import get_vlm

    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    train = load(args.data, "train_raw.json")
    check_model(args.model)
    out = args.out
    if out.resolve().is_relative_to(ROOT):
        raise SystemExit("REFUSED --out inside the repo")
    out.mkdir(parents=True, exist_ok=True)
    refuse_if_stopped(out)  # before the model loads
    launch = out / "launch.json"
    if not launch.exists():
        launch.write_text(json.dumps({"t0": time.time(), "device": args.device}))
    ad = get_vlm(MODEL["name"], model_id=MODEL["repo"], device=args.device,
                 dtype="bfloat16" if args.device == "cuda" else "float32").load()
    if ad.max_tiles != MODEL["max_tiles"]:
        raise SystemExit("FAULT max_tiles is not the registry value 4")
    img = lambda iid: Image.open(args.images / f"COCO_val2014_{iid:012d}.jpg").convert("RGB")  # noqa: E731
    names = (PDIR / "fetch_images.txt").read_text().split()
    held = {int(x) for x in (PDIR / "selection_excluded_ids.txt").read_text().split()}
    present = [n for n in names if (args.images / n).is_file()]  # the job asserts all are present before this
    bad = sha_refused({image_id(n): sha_file(args.images / n) for n in present}, refused_sets()[1], held)
    if bad:
        raise SystemExit(f"FAULT {len(bad)} fetched images match exclusion.json image_sha256: {bad[:5]}")
    tsegs = {(s["rec"], s["seg"]): s for s in segments(train)[0]}
    demos = tuple((demo_pixels(img(d["image"]), ad.dtype, ad.device), question(tsegs[(d["rec"], d["seg"])]["text"]), d["answer"])
                  for d in plan["demos"])
    for d in plan["demos"]:
        if sha_text(tsegs[(d["rec"], d["seg"])]["text"]) != d["text_sha256"]:
            raise SystemExit("FAULT demo text sha differs from the plan")

    smoke_f = out / "smoke.json"
    if not smoke_f.exists():
        smoke_f.write_text(json.dumps(run_smoke(ad, plan["smoke"][: args.smoke_n * SMOKE_SEGS], tsegs, img, demos),
                                      indent=1, ensure_ascii=False))
    v = json.loads(smoke_f.read_text())
    if v["fault"]:
        return halt(out, 2, "FAULT smoke (arm A / tokens / equivalence); see smoke.json")
    if args.smoke_only:
        print(json.dumps(v, ensure_ascii=False))
        return 0
    return run_val(ad, load(args.data, "val_raw.json"), img, demos, v, out)


def run_smoke(ad, pins: list, tsegs: dict, img, demos: tuple) -> dict:
    """Section 7.1: train smoke segments, both arms, plus yes_no_logit equivalence on the first 5."""
    tok = token_check(ad)
    rows, equiv = [], []
    for k, sp in enumerate(pins):
        s = tsegs[(sp["rec"], sp["seg"])]
        im = img(s["image"])
        pv, q = ad._pixel_values(im), question(s["text"])
        for arm, dm in (("A", ()), ("B", demos)):
            t = time.perf_counter()
            try:
                text, p, m = probe(ad, pv, q, dm)
            except Exception as e:  # arm B unsupported -> dropped (W2); arm A -> FAULT in smoke_verdict
                text, p, m = f"EXC {type(e).__name__}", float("nan"), 0.0
            rows.append({"arm": arm, "p_yes": p, "mass": m, "text": text, "sec": time.perf_counter() - t})
        if k < 5:
            equiv.append(abs(ad.yes_no_logit(im, q)[1] - rows[-2]["p_yes"]))
    v = smoke_verdict(rows, equiv)
    v.update(token=tok, arm_b_dropped=not v["B"]["ok"], fault=not (v["A"]["ok"] and tok["ok"]),
             sec_median={a: statistics.median(r["sec"] for r in rows if r["arm"] == a) for a in "AB"})
    return v


def run_val(ad, val: list, img, demos: tuple, smoke: dict, out: Path) -> int:
    """Section 8: interleaved arms per image in the fixed order, the two projection rules and the cap."""
    refuse_if_stopped(out)
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    t0 = json.loads((out / "launch.json").read_text())["t0"]
    elapsed_h = lambda: (time.time() - t0) / 3600  # noqa: E731
    arms = ("A",) if smoke["arm_b_dropped"] else ("A", "B")
    ids = lambda name: {int(x) for x in (PDIR / name).read_text().split()}  # noqa: E731
    order = image_order(ids("val_ids.txt") - ids("dropped_ids.txt"))
    if sha_text("".join(f"{i}\n" for i in order)) != plan["image_order_sha256"]:
        raise SystemExit("FAULT image order differs from the plan")
    vsegs = segments(val)[0]
    by_img: dict = {}
    for s in vsegs:
        by_img.setdefault(s["image"], []).append(s)
    pf = out / "probes.jsonl"
    done = set()
    if pf.exists():
        for line in pf.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            done.add((r["rec"], r["seg"], r["arm"]))
    total = {a: sum(len(by_img.get(i, [])) for i in order) for a in arms}
    pre_f = out / "projection_pre_val.json"
    if not pre_f.exists() and not done:  # smoke speed x full val, before any val image is decoded
        pj = projection_h(elapsed_h(), total, {a: smoke["sec_median"][a] for a in arms})
        pre_f.write_text(json.dumps({"elapsed_h": elapsed_h(), "projected_h": pj, "cap_h": CAP_H, "stop": pj > CAP_H}))
        if pj > CAP_H:
            return halt(out, 3, f"PROJECTION_STOP before val: projected {pj:.2f} GPU-h > cap {CAP_H}", 0)
    proj_f = out / "projection.json"
    with open(pf, "a", encoding="utf-8") as fh:
        for n, iid in enumerate(order, 1):
            if elapsed_h() > CAP_H:  # checked before each image is decoded
                return halt(out, 4, f"CAP_STOP before image {n}: {elapsed_h():.2f} GPU-h", n)
            todo = [(s, a) for s in by_img.get(iid, []) for a in arms if (s["rec"], s["seg"], a) not in done]
            if todo:
                pv = ad._pixel_values(img(iid))
                for s, a in todo:
                    t = time.perf_counter()
                    text, p, m = probe(ad, pv, question(s["text"]), () if a == "A" else demos)
                    row = {"rec": s["rec"], "seg": s["seg"], "image": iid, "arm": a, "n_img": n, "p_yes": p,
                           "mass": m, "text": text, "sec": time.perf_counter() - t}
                    if not math.isfinite(p):
                        append(fh, row)
                        fh.flush()
                        return halt(out, 2, f"FAULT non-finite P(yes) at rec {s['rec']} seg {s['seg']} arm {a}", n)
                    append(fh, row)
                    done.add((s["rec"], s["seg"], a))
                fh.flush()
                os.fsync(fh.fileno())
            if n == N_PROJ and not proj_f.exists():
                rows = [json.loads(x) for x in pf.read_text(encoding="utf-8").splitlines()]
                med = {a: statistics.median(r["sec"] for r in rows if r["arm"] == a and 2 <= r["n_img"] <= N_PROJ)
                       for a in arms}
                rem = {a: total[a] - sum(1 for k in done if k[2] == a) for a in arms}
                pj = projection_h(elapsed_h(), rem, med)
                proj_f.write_text(json.dumps({"elapsed_h": elapsed_h(), "median_s": med, "remaining": rem,
                                              "projected_h": pj, "cap_h": CAP_H, "stop": pj > CAP_H}))
                if pj > CAP_H:
                    return halt(out, 3, f"PROJECTION_STOP projected {pj:.2f} GPU-h > cap {CAP_H}", n)
    print(json.dumps({"status": "DONE", "elapsed_h": elapsed_h(), "probes": len(done)}))
    return 0


def cmd_score(args) -> int:
    import numpy as np
    from m0_stats import T_A, auroc, bootstrap, decide, prec_at_recall, rp, stats

    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    val = load(args.data, "val_raw.json")
    smoke = json.loads((args.out / "smoke.json").read_text())
    arms = ("A",) if smoke["arm_b_dropped"] else ("A", "B")
    drop = {int(x) for x in (PDIR / "dropped_ids.txt").read_text().split()}
    held = {int(x) for x in (PDIR / "selection_excluded_ids.txt").read_text().split()}
    segs = [s for s in segments(val)[0] if s["image"] not in drop]
    P = {(r["rec"], r["seg"], r["arm"]): r["p_yes"] for r in check_scorable(args.out)}
    missing = [(s["rec"], s["seg"], a) for s in segs for a in arms if (s["rec"], s["seg"], a) not in P]
    if missing or len(segs) != plan["custody"]["probe_segments"]:
        raise SystemExit(f"INCOMPLETE: {len(missing)} probes missing; no score on a partial run")
    y = np.array([s["y"] for s in segs])
    img = np.array([s["image"] for s in segs])
    typ = np.array([s["type"] for s in segs])
    pA = np.array([P[(s["rec"], s["seg"], "A")] for s in segs])
    pB = np.array([P[(s["rec"], s["seg"], "B")] for s in segs]) if "B" in arms else None
    op = np.array([i not in held for i in img])
    sub = lambda a, m: None if a is None else a[m]  # noqa: E731
    point = stats(pA[op], sub(pB, op), y[op])
    ci = bootstrap(pA[op], sub(pB, op), y[op], img[op])
    res = {"selection_set": {"images": int(len(np.unique(img[op]))), "segments": int(op.sum()), "inaccurate": int(y[op].sum())},
           "point": point, "ci95": ci, "decision": decide(point, ci),
           "prec_at_R80": {"A": prec_at_recall(pA[op], y[op])}}
    if pB is not None:
        res["prec_at_R80"]["B"] = prec_at_recall(pB[op], y[op])
    flags = {"A": pA < T_A}
    if pB is not None and point["tau_B"] is not None:
        flags["B"] = pB <= point["tau_B"]
    res["per_type_recall_selection"] = {
        a: {t: {"n_inaccurate": int(y[op & (typ == t)].sum()), "recall": rp(f[op & (typ == t)], y[op & (typ == t)])[0]}
            for t in ("count", "attribute", "relation", "object")} for a, f in flags.items()}
    res["full_split_same_thresholds"] = {
        "images": int(len(np.unique(img))), "segments": len(segs), "inaccurate": int(y.sum()),
        **{f"{k}_{a}": v for a, f in flags.items() for k, v in zip(("R", "P"), rp(f, y))},
        "AUROC_A": auroc(pA, y), **({"AUROC_B": auroc(pB, y)} if pB is not None else {})}
    res["note"] = "Recall is against human-marked Inaccurate spans; unmarked text defaults to Accurate (bias: PREREG section 2)."
    args.res.write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"point": point, "ci95": ci, "decision": res["decision"]}, indent=1))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("selftest")
    sp.add_parser("plan")
    p = sp.add_parser("probe")
    p.add_argument("--data", type=Path, required=True, help="folder with val_raw.json and train_raw.json (A-N3 pins)")
    p.add_argument("--images", type=Path, required=True)
    p.add_argument("--model", type=Path, required=True, help="HF snapshot dir named by the pinned revision")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--device", default="cuda")
    p.add_argument("--smoke-n", type=int, default=N_PROJ, help="smoke images (<= 50); the GPU run uses 50")
    p.add_argument("--smoke-only", action="store_true")
    s = sp.add_parser("score")
    s.add_argument("--data", type=Path, required=True)
    s.add_argument("--out", type=Path, required=True, help="the probe run folder")
    s.add_argument("--res", type=Path, required=True)
    a = ap.parse_args()
    if a.cmd == "selftest":
        import test_m0

        test_m0.main()
        return 0
    return {"plan": cmd_plan, "probe": cmd_probe, "score": cmd_score}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
