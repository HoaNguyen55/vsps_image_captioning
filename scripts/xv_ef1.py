#!/usr/bin/env python
"""XV-EF1 (Tier-3 S2, GPU_JOB_PLAN_v1 T3.1): InternVL3-8B as an existence scorer on the dev300 pool, gate G0, and the
dev readout of the UPE-MBR rule with the verifier's P(yes) as its evidence term.

Pre-registration manuscript/prereg/2026-10-18_tier3_S2.{md,json} (commit a68fb66); the instrument addendum
manuscript/prereg/2026-10-18_tier3_S2_instrument.json pins this file and scripts/queue/jobs/t3_1_s2_xvef1_g0.sh.

    python scripts/xv_ef1.py score --out DIR       # GPU: P(yes) with and without the image, the 1,306 N13 items
    python scripts/xv_ef1.py analyse --cache DIR/p_v.jsonl --sha-file SHA --out DIR  # CPU: G0; readout if it passes
    NCS_DATA=$PWD/data python scripts/xv_ef1.py --selftest   # CPU, synthetic: each verdict once each way

Every mode first refuses to run unless the prereg is the one the addendum pins and the code, the inputs and the
constants it registers are as registered. dev300 only. Writes numbers, class names, pool indices and file hashes:
never a caption, a reference or panel text.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import inspect
import json
import os
import re
import sys
import tempfile
import time
from itertools import groupby
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import object_prf  # noqa: E402
import plan_f1 as PF  # noqa: E402
import rl_reward  # noqa: E402
import upe_mbr as U  # noqa: E402
from checkpoint_resume_hook import provenance_metadata  # noqa: E402
from evaluate import KTVIC, file_names, references  # noqa: E402

JOB = "t3_1_s2_xvef1_g0"
PREREG = ROOT / "manuscript" / "prereg" / "2026-10-18_tier3_S2.json"
ADDENDUM = PREREG.with_name("2026-10-18_tier3_S2_instrument.json")
NEW_FILES = ("scripts/xv_ef1.py", f"scripts/queue/jobs/{JOB}.sh")  # the two files the addendum pins
TRAIN_JSON = "data/datasets/ktvic/train_data.json"  # the registered path; read where evaluate.py reads it ($NCS_DATA)
DEV_SPLIT, REST_SPLIT = "data/splits/ktvic_dev300.txt", "data/splits/ktvic_train_minus_dev300.txt"
T_FILE = "data/results/upe/upe_temperature.txt"
ROUNDED = ("P_ktvic5", "R_ktvic5", "F1_ktvic5", "F1_panel")  # registered to 3 decimals (p1dev_reference_dev300)
README = ".session_backup/2026-10-18/paperA_tasks/P3/hf_meta/internvl3_8b_README_853e3a7.md"  # the selftest's copy
README_DEFS = ("IMAGENET_MEAN", "IMAGENET_STD", "find_closest_aspect_ratio", "dynamic_preprocess", "build_transform",
               "load_image")
IMAGE = "<image>\n"

# The image code of the InternVL3-8B README at the pinned revision, its comments dropped. same_as_readme() refuses to
# run unless these definitions and readme_loader()'s two are the README's own, as code (layout and comments aside).
IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


def find_closest_aspect_ratio(aspect_ratio, target_ratios, width, height, image_size):
    best_ratio_diff = float('inf')
    best_ratio = (1, 1)
    area = width * height
    for ratio in target_ratios:
        target_aspect_ratio = ratio[0] / ratio[1]
        ratio_diff = abs(aspect_ratio - target_aspect_ratio)
        if ratio_diff < best_ratio_diff:
            best_ratio_diff = ratio_diff
            best_ratio = ratio
        elif ratio_diff == best_ratio_diff:
            if area > 0.5 * image_size * image_size * ratio[0] * ratio[1]:
                best_ratio = ratio
    return best_ratio


def dynamic_preprocess(image, min_num=1, max_num=12, image_size=448, use_thumbnail=False):
    orig_width, orig_height = image.size
    aspect_ratio = orig_width / orig_height
    target_ratios = set(
        (i, j) for n in range(min_num, max_num + 1) for i in range(1, n + 1) for j in range(1, n + 1) if
        i * j <= max_num and i * j >= min_num)
    target_ratios = sorted(target_ratios, key=lambda x: x[0] * x[1])
    target_aspect_ratio = find_closest_aspect_ratio(
        aspect_ratio, target_ratios, orig_width, orig_height, image_size)
    target_width = image_size * target_aspect_ratio[0]
    target_height = image_size * target_aspect_ratio[1]
    blocks = target_aspect_ratio[0] * target_aspect_ratio[1]
    resized_img = image.resize((target_width, target_height))
    processed_images = []
    for i in range(blocks):
        box = (
            (i % (target_width // image_size)) * image_size,
            (i // (target_width // image_size)) * image_size,
            ((i % (target_width // image_size)) + 1) * image_size,
            ((i // (target_width // image_size)) + 1) * image_size
        )
        split_img = resized_img.crop(box)
        processed_images.append(split_img)
    assert len(processed_images) == blocks
    if use_thumbnail and len(processed_images) != 1:
        thumbnail_img = image.resize((image_size, image_size))
        processed_images.append(thumbnail_img)
    return processed_images


def readme_loader(torch, T, InterpolationMode):
    """The README's load_image, bound to the modules it uses (only the GPU mode imports them; checks pass None)."""

    def build_transform(input_size):
        MEAN, STD = IMAGENET_MEAN, IMAGENET_STD
        transform = T.Compose([
            T.Lambda(lambda img: img.convert('RGB') if img.mode != 'RGB' else img),
            T.Resize((input_size, input_size), interpolation=InterpolationMode.BICUBIC),
            T.ToTensor(),
            T.Normalize(mean=MEAN, std=STD)
        ])
        return transform

    def load_image(image_file, input_size=448, max_num=12):
        image = Image.open(image_file).convert('RGB')
        transform = build_transform(input_size=input_size)
        images = dynamic_preprocess(image, image_size=input_size, use_thumbnail=True, max_num=max_num)
        pixel_values = [transform(image) for image in images]
        pixel_values = torch.stack(pixel_values)
        return pixel_values

    return load_image


# ----------------------------------------------------------------------------------------------- registration checks
def need(ok: bool, what: str) -> None:
    """Stop: a registered condition does not hold."""
    if not ok:
        raise SystemExit(f"xv_ef1 refuses to run: {what}")


def sha(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 24), b""):
            h.update(chunk)
    return h.hexdigest()


def check(prereg: Path = PREREG, addendum: Path = ADDENDUM) -> tuple[dict, dict]:
    """(registration, inputs seen): the addendum pins this script, the job file and the prereg, with no deviation;
    the prereg's code_at_head and the job's inputs are as registered, and so are its constants; SystemExit otherwise."""
    pin = json.loads(addendum.read_text(encoding="utf-8"))
    need(pin["new_files"] == {rel: sha(ROOT / rel) for rel in NEW_FILES} and pin["deviations"] == [],
         "the addendum does not pin this script and job file, or lists a deviation")
    need(sha(prereg) == pin["prereg_sha256"] and sha(prereg.with_suffix(".md")) == pin["prereg_md_sha256"],
         "the prereg is not the one the addendum pins")
    reg = json.loads(prereg.read_text(encoding="utf-8"))
    for rel, h in reg["code_at_head"].items():
        need(sha(ROOT / rel) == h, f"{rel} differs from the registered code")
    spec = reg["data"]
    reads = {*spec["splits"], *(v["path"] for v in spec["pool"].values() if isinstance(v, dict)), spec["panel"]["path"],
             T_FILE}
    need(reads <= set(reg["inputs_sha256"]), "an input this job reads has no registered sha256")
    seen = {"verified": [], "absent_not_read_by_this_job": []}
    for rel, h in reg["inputs_sha256"].items():
        path = KTVIC / "train_data.json" if rel == TRAIN_JSON else ROOT / rel
        if rel not in reads and not path.is_file():  # a source of a registered number, kept in the local backup only
            seen["absent_not_read_by_this_job"].append(rel)
            continue
        need(path.is_file() and sha(path) == h, f"input {rel} is missing or differs from the registration")
        seen["verified"].append(rel)
    constants(reg)
    return reg, seen


def constants(reg: dict) -> None:
    """The registered constants are the ones the committed code holds."""
    from rescap import chair

    vp, ci, src, spec = reg["verifier_protocol"], reg["analysis"]["ci"], reg["sources"], reg["data"]
    img, loader = vp["image_preprocessing"], readme_loader(None, None, None)

    def defaults(fn) -> dict:
        return {k: p.default for k, p in inspect.signature(fn).parameters.items()}

    tstar = (ROOT / T_FILE).read_text(encoding="utf-8").strip()
    returnable = {o for k, o in chair._NOUNS.items() if k not in chair._NOT_OBJECTS}
    checks = {
        "job, dev300 only": reg["job"]["job_name"] == JOB and spec["test_split_read"] is False,
        "UPE constants": reg["upe_constants"] == {"LAM": U.LAM, "M": U.M, "MARGIN": U.MARGIN, "EG": U.EG,
                                                  "RETRIEVE": U.RETRIEVE, "K_SAMPLES": U.K_SAMPLES},
        "COUNT grid": reg["count_grid_min_max_n"] == [min(U.COUNT_GRID), max(U.COUNT_GRID), len(U.COUNT_GRID)],
        "12 samples per image": spec["pool"]["samples_per_image"] == len(PF.TEMPS) * PF.N_PER_T
        and PF.N_PER_T == U.K_SAMPLES,
        "T* 0.5": tstar == src["upe.T_star"]["value"] == PF.T_STAR == PF.TEMPS[0]
        and f"samples_T{tstar}" in spec["pool"],
        "object_prf.paired": src["object_prf.paired.defaults"]["value"].items() <= defaults(object_prf.paired).items(),
        "rl_reward.boot": src["rl_reward.boot.defaults"]["value"].items() <= defaults(rl_reward.boot).items(),
        "bootstrap": ci["B"] == src["bootstrap.B"]["value"] == defaults(rl_reward.boot)["b"]
        and ci["rng"] == f"numpy default_rng({src['bootstrap.seed']['value']})",
        "class map": set(vp["english_class_map"]) == returnable and len(returnable) == vp["n_classes_in_map"],
        "with-image prompt": vp["with_image"] == f"{IMAGE!r} + question",
        "image settings": [img["min_num"], img["input_size"], img["max_num"]]
        == [defaults(dynamic_preprocess)["min_num"], defaults(loader)["input_size"], defaults(loader)["max_num"]]
        and img["use_thumbnail"] is True and "use_thumbnail=True" in inspect.getsource(loader),
        "matcher v2 on KTVIC": os.environ.get("RESCAP_RAW_TONE") != "1" and KTVIC.name == "ktvic",
    }
    bad = [k for k, ok in checks.items() if not ok]
    need(not bad, f"registered constants differ from the code: {bad}")


def defs(body: list) -> dict:
    """Function definitions and single-name assignments among the statements `body`, by name."""
    found = {}
    for node in body:
        if isinstance(node, ast.FunctionDef):
            found[node.name] = node
        elif isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            found[node.targets[0].id] = node
    return found


def same_as_readme(readme: Path, readme_sha256: str) -> None:
    """The image code above is the registered README's, as code."""
    need(sha(readme) == readme_sha256, f"{readme} is not the registered README")
    text = readme.read_text(encoding="utf-8")
    block = next(b for b in re.findall(r"```python\n(.*?)```", text, re.S) if "def load_image(" in b)
    here = ast.parse(Path(__file__).read_text(encoding="utf-8")).body
    loader = next(n for n in here if isinstance(n, ast.FunctionDef) and n.name == "readme_loader")
    theirs, ours = defs(ast.parse(block).body), {**defs(here), **defs(loader.body)}
    need(all(ast.dump(theirs[k]) == ast.dump(ours[k]) for k in README_DEFS), "the image code differs from the README's")


# ----------------------------------------------------------------------------------------------- data, cache, outputs
def dev(reg: dict) -> dict:
    """dev300 ids and references, the train-minus-dev300 references, and the registered pools with their items:
    key (image_id, class), img (position in ids), y (class in ktvic5 gold), cell (round(k v) * 2 + g, k samples)."""
    sp = reg["data"]["splits"]
    ids, rest = (sorted((ROOT / rel).read_text(encoding="utf-8").split()) for rel in (DEV_SPLIT, REST_SPLIT))
    tr = references("train_data.json")
    train = {j: rs for j, rs in tr.items() if j not in set(ids)}
    need(len(ids) == sp[DEV_SPLIT]["n_images"] and len(rest) == sp[REST_SPLIT]["n_images"] and set(train) == set(rest),
         "dev300 and train minus dev300")
    pool = reg["data"]["pool"]
    rows = PF.pools(ROOT / pool["greedy"]["path"], [ROOT / pool[f"samples_T{t}"]["path"] for t in PF.TEMPS], ids)
    gold, prior = [frozenset().union(*map(PF.objs, tr[i])) for i in ids], PF.class_prior(tr)
    out = {"ids": ids, "refs": {i: tr[i] for i in ids}, "train": train, "pool7": [r[:1 + PF.N_PER_T] for r in rows]}
    for name, pools in (("N13", rows), ("N7_T0.5", out["pool7"])):
        img, names, x = PF.items(pools, prior)
        y, _ = PF.labels(img, names, gold)
        want = reg["data"]["items"][name]
        need([len(y), int(y.sum()), len(set(img.tolist()))]
             == [want["n_items"], want["n_positive"], want["n_images_with_items"]], f"{name} item counts")
        out[name] = {"key": [(ids[n], o) for n, o in zip(img, names)], "img": img, "y": y,
                     "cell": np.round((len(pools[0]) - 1) * x[:, 1]).astype(int) * 2 + x[:, 2].astype(int)}
    return out


def read_rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line] if path.exists() else []


def fill(cache: Path, keys: list, vp: dict, load, ask) -> int:
    """Append {image_id, class, np, p_with, p_without} for each item the cache lacks (a stopped job resumes)."""
    done = {(r["image_id"], r["class"]) for r in read_rows(cache)}
    todo = [k for k in keys if k not in done]
    with cache.open("a", encoding="utf-8") as f:
        for i, group in groupby(todo, key=lambda k: k[0]):
            pixels = load(i)
            for _, o in group:
                phrase = vp["english_class_map"][o]
                q = vp["question_template"].format(np=phrase)
                row = {"image_id": i, "class": o, "np": phrase,
                       "p_with": ask(IMAGE + q, pixels), "p_without": ask(q, None)}
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
                f.flush()
                done.add((i, o))
                if len(done) % 100 == 0:
                    print(f"{len(done)}/{len(keys)} items scored", flush=True)
    return len(todo)


def cached(cache: Path, keys: list) -> dict:
    """{(image_id, class): (p_with, p_without)}; exits unless the cache is one valid row per registered item."""
    rows = read_rows(cache)
    p = {(r["image_id"], r["class"]): (r["p_with"], r["p_without"]) for r in rows}
    need(len(rows) == len(p) == len(keys) and set(p) == set(keys), f"{cache} is not one row per N13 item")
    need(all(0 <= x <= 1 for pair in p.values() for x in pair), f"{cache} holds a score outside [0, 1]")
    return p


def recorded(cache: Path, sha_file: Path) -> str:
    """The cache's sha256, which must already be in the job's sha file: it is recorded before any AUROC (prereg §5)."""
    h = sha(cache)
    need(h in sha_file.read_text(encoding="utf-8"),
         f"the sha256 of {cache} is not in {sha_file}: record it before any AUROC")
    return h


def write(path: Path, obj: dict) -> Path:
    """obj as JSON at path, or at path_v2, _v3, ... when it exists: an output is never overwritten."""
    target, k = path, 2
    while target.exists():
        target, k = path.with_name(f"{path.stem}_v{k}{path.suffix}"), k + 1
    target.write_text(json.dumps(obj, indent=1, ensure_ascii=False, default=float) + "\n", encoding="utf-8")
    return target


def stamp(seen: dict, **fields) -> dict:
    """What every result JSON records: the hook's provenance (machine_id, git_head_sha, hook sha) and the pins."""
    return {"job": JOB, **provenance_metadata(), "prereg_sha256": sha(PREREG), "addendum_sha256": sha(ADDENDUM),
            "script_sha256": sha(__file__), "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "inputs": seen,
            **fields}


# ----------------------------------------------------------------------------------------------- GPU: the verifier
def verifier(v: dict, torch):
    """(ask, about): ask(question, pixel_values or None) = P(yes) / (P(yes) + P(no)) at the first answer position of
    the prompt model.chat builds, P(yes) summing the next-token probabilities of 'Yes' and 'yes' (P(no): 'No', 'no')."""
    from transformers import AutoModel, AutoTokenizer

    model = AutoModel.from_pretrained(v["id"], revision=v["revision"], torch_dtype=torch.bfloat16,
                                      low_cpu_mem_usage=True, use_flash_attn=False,
                                      trust_remote_code=True).eval().cuda()
    tok = AutoTokenizer.from_pretrained(v["id"], revision=v["revision"], trust_remote_code=True, use_fast=False)
    yes = [tok.encode(w, add_special_tokens=False)[0] for w in ("Yes", "yes")]
    no = [tok.encode(w, add_special_tokens=False)[0] for w in ("No", "no")]
    generate, logits = model.generate, []

    def one_step(**kw):
        out = generate(**kw, output_logits=True, return_dict_in_generate=True)
        logits.append(out.logits[0][0].float())
        return out.sequences

    model.generate = one_step  # model.chat builds its own prompt and calls this: one greedy step, raw logits kept

    def ask(question, pixel_values) -> float:
        model.chat(tok, pixel_values, question, {"max_new_tokens": 1, "do_sample": False})
        prob = logits.pop().softmax(-1)
        return float(prob[yes].sum() / (prob[yes].sum() + prob[no].sum()))

    return ask, {"yes_token_ids": yes, "no_token_ids": no, "template": model.template,
                 "num_image_token": model.num_image_token}


def score(args) -> None:
    """GPU: the pinned verifier (shards and README checked first), then the cache filled for every N13 item."""
    import torch
    import torchvision.transforms as T
    import transformers
    from huggingface_hub import snapshot_download
    from torchvision.transforms.functional import InterpolationMode

    reg, seen = check()
    v, vp = reg["models"]["verifier"], reg["verifier_protocol"]
    dv, t0 = dev(reg), time.time()
    snap = Path(snapshot_download(v["id"], revision=v["revision"]))
    for name, h in v["shards_sha256"].items():
        need(sha(snap / name) == h, f"{name} is not the registered shard")
    same_as_readme(snap / "README.md", v["licence"]["readme_sha256"])
    ask, about = verifier(v, torch)
    load_image, names = readme_loader(torch, T, InterpolationMode), file_names("train_data.json")
    img = vp["image_preprocessing"]

    def load(i):
        pixels = load_image(KTVIC / "images" / names[i], input_size=img["input_size"], max_num=img["max_num"])
        return pixels.to(torch.bfloat16).cuda()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    cache = out / "p_v.jsonl"
    new = fill(cache, dv["N13"]["key"], vp, load, ask)
    model = {"id": v["id"], "revision": v["revision"], "shards_sha256_verified": v["shards_sha256"],
             "readme_sha256_verified": v["licence"]["readme_sha256"], "licence": v["licence"],
             "remote_code_sha256": {f.name: sha(f) for f in sorted(snap.glob("*.py"))}, **about}
    rep = stamp(seen, verifier=model, items=len(dv["N13"]["key"]), scored_this_run=new, cache=cache.name,
                cache_sha256=sha(cache), seconds=round(time.time() - t0), device=torch.cuda.get_device_name(0),
                versions={"torch": torch.__version__, "transformers": transformers.__version__})
    print(write(out / "score.json", rep))


# ----------------------------------------------------------------------------------------------- CPU: G0 and readout
def pool_stats(s: np.ndarray, it: dict, idx: np.ndarray) -> dict:
    """The four registered statistics of s (columns p_with, p_without) on one pool's items, with image-clustered
    percentile 95% CIs over the draws idx (B x images), and the item and pair counts per (votes, greedy) cell."""
    from knn_prior_eval import cell_auc

    cell, y = it["cell"], it["y"]

    def four(j) -> dict:
        return {"A_within": cell_auc(s[j, 0], cell[j], y[j]), "A_noimg": PF.auroc(s[j, 1], y[j]),
                "cell_auc_noimg": cell_auc(s[j, 1], cell[j], y[j]), "auroc_with": PF.auroc(s[j, 0], y[j])}

    by = [np.flatnonzero(it["img"] == n) for n in range(idx.shape[1])]
    point, draws = four(np.arange(len(y))), [four(np.concatenate([by[n] for n in row])) for row in idx]
    stats = {k: {"point": v, "ci95": np.percentile([d[k] for d in draws], [2.5, 97.5]).tolist()}
             for k, v in point.items()}
    cells = {}
    for c in np.unique(cell):
        pos, n = int(y[cell == c].sum()), int((cell == c).sum())
        cells[str(c)] = {"votes": int(c) // 2, "greedy": int(c) % 2, "items": n, "pos": pos, "neg": n - pos,
                         "pairs": pos * (n - pos)}
    return {"n_items": len(y), "n_pos": int(y.sum()), **stats, "per_cell": cells}


def gate(reg: dict, a_within: float, a_noimg: float) -> str:
    """G0 on point estimates: PASS iff A_within >= the registered minimum and A_noimg <= the registered maximum."""
    g = reg["gate"]
    return "PASS" if a_within >= g["within_cell_auroc_min"] and a_noimg <= g["no_image_auroc_max"] else "KILL"


def g0(reg: dict, dv: dict, p: dict, idx: np.ndarray) -> dict:
    """§6.2: the gate on N13's point estimates; every statistic of both pools reported with its CI."""
    pools = {k: pool_stats(np.array([p[key] for key in dv[k]["key"]], float), dv[k], idx) for k in ("N13", "N7_T0.5")}
    a_w, a_n = pools["N13"]["A_within"]["point"], pools["N13"]["A_noimg"]["point"]
    return {"A_within": a_w, "A_noimg": a_n, "rule": reg["gate"]["rule"], "verdict": gate(reg, a_w, a_n),
            "pools": pools}


def prior_leak(reg: dict, d: float, d_noimg: float) -> bool:
    """Kill: dF1(XV-EF1 - COUNT) > 0 and the no-image arm's dF1 against its own COUNT is >= the registered 70% of it."""
    return d > 0 and d_noimg >= reg["sources"]["kill.prior_leak_pct"]["value"] / 100 * d


def carried(reg: dict, e: dict, leak: bool) -> bool:
    """The carry rule on dev point estimates (G0 has passed: there is no readout otherwise)."""
    t = reg["carry_rule"]["thresholds"]
    return (not leak and e["dF1_vs_COUNT"] >= t["dF1_vs_COUNT_min"]
            and e["dCHAIRi_vs_COUNT_x100"] <= t["dCHAIRi_vs_COUNT_x100_max"]
            and e["dCIDEr_vs_greedy_x100"] >= t["dCIDEr_vs_greedy_min"]
            and e["panel_dF1_vs_COUNT"] >= t["panel_dF1_vs_COUNT_min"])


def endpoints(arm: dict) -> dict:
    """One arm's registered endpoints (point estimates), with dP, dR and the share of images switched from greedy."""
    vs_c, vs_g = arm["vs_COUNT"], arm["vs_greedy"]
    return {"dF1_vs_COUNT": vs_c["obj_ktvic"]["F1"][0], "dP_vs_COUNT": vs_c["obj_ktvic"]["P"][0],
            "dR_vs_COUNT": vs_c["obj_ktvic"]["R"][0], "dCHAIRi_vs_COUNT_x100": arm["dCHAIRi_vs_COUNT_x100"][0],
            "dCIDEr_vs_greedy_x100": vs_g["cider"][0], "panel_dF1_vs_COUNT": vs_c["panel_obj"]["F1"][0],
            "switched_from_greedy": vs_g["switched"]}


def reproduces(registered: dict, measured: dict) -> None:
    """The scorer gives P1_dev greedy's registered dev300 numbers (the 3-decimal ones to 3 decimals)."""
    off = [k for k, x in measured.items()
           if not (round(x, 3) == registered[k] if k in ROUNDED else abs(x - registered[k]) < 1e-6)]
    need(not off, f"the scorer does not reproduce the registered greedy numbers {off}")


def readout(reg: dict, dv: dict, p: dict, tok, panel: dict, idx: np.ndarray, expect: dict | None = None) -> dict:
    """§6.3 on N7_T0.5: XV-EF1 (q_o = p_with) and XV-EF1-noimg (p_without), each against its own count-matched COUNT
    and against greedy; then the prior-leak kill and the carry rule."""
    ids, pool, refs = dv["ids"], dv["pool7"], dv["refs"]
    vk, vp, pos = U.ktvic_views(pool, ids, refs, panel, tok)
    need(len(pos) == reg["data"]["panel"]["dev_images_with_panel"], "dev images with a panel")
    g0_pk = np.zeros(len(ids), int)

    def chair_rows(pk):
        return U.chair_counts({i: pool[n][pk[n]] for n, i in enumerate(ids)}, refs)

    def per_caption(pk) -> float:
        return float(np.mean([len(vk.cls[n][k]) for n, k in enumerate(pk)]))

    gk, gp = object_prf.scores(vk.picked("ktvic", g0_pk)), object_prf.scores(vp.picked("panel", g0_pk[pos]))
    gc = chair_rows(g0_pk)
    greedy = {"CIDEr_D_x100": float(vk.cider[:, 0].mean()), "CHAIR_i": float(gc[:, 1].sum() / gc[:, 0].sum()),
              "mentions_per_caption": float(gc[:, 0].sum() / len(ids)), "P_ktvic5": gk["P"], "R_ktvic5": gk["R"],
              "F1_ktvic5": gk["F1"], "F1_panel": gp["F1"]}
    if expect is not None:
        reproduces(expect, greedy)
    u = U.utilities(vk.tok, vk.cls, U.tok_groups(tok, dv["train"]))
    arms = {}
    for name, col in (("XV-EF1", 0), ("XV-EF1-noimg", 1)):
        ef1 = np.array([[2 * sum(p[i, o][col] for o in m) / (len(m) + U.EG) for m in row]
                        for i, row in zip(ids, vk.cls)])
        pk = U.pick(u["base"], ef1, U.LAM)
        lam, cnt = U.count_matched(u, vk.cls, pk)
        a, b = chair_rows(cnt), chair_rows(pk)
        chair_ci = np.percentile([U.chair_delta(a[j], b[j]) for j in idx], [2.5, 97.5]).tolist()
        arm = {"count_lam": lam, "vs_COUNT": U.compare(vk, vp, cnt, pk, ("ktvic",), pos),
               "vs_greedy": U.compare(vk, vp, g0_pk, pk, ("ktvic",), pos),
               "dCHAIRi_vs_COUNT_x100": [U.chair_delta(a, b), *chair_ci],
               "classes_per_caption": {"rule": per_caption(pk), "COUNT": per_caption(cnt),
                                       "greedy": per_caption(g0_pk)},
               "picks": {"rule": pk.tolist(), "COUNT": cnt.tolist()}}
        arms[name] = {"endpoints": endpoints(arm), **arm}
    e, e0 = arms["XV-EF1"]["endpoints"], arms["XV-EF1-noimg"]["endpoints"]
    leak = prior_leak(reg, e["dF1_vs_COUNT"], e0["dF1_vs_COUNT"])
    carry = carried(reg, e, leak)
    return {"greedy": greedy, "arms": arms, "prior_leak_kill": leak, "carried": carry,
            "verdict": "CARRIED" if carry else ("KILL (prior leak)" if leak else "NOT CARRIED"),
            "rules": {"kill": reg["kill_rules"][1], "carry": reg["carry_rule"]["rule"]}}


def analyse(args) -> None:
    """CPU: G0 from a cache whose sha256 is already in the job's sha file; the dev readout only if G0 passes."""
    reg, seen = check()
    cache, out = Path(args.cache), Path(args.out)
    h = recorded(cache, Path(args.sha_file))
    dv = dev(reg)
    p, n = cached(cache, dv["N13"]["key"]), len(dv["ids"])
    rng = np.random.default_rng(reg["sources"]["bootstrap.seed"]["value"])
    idx = rng.integers(0, n, (reg["analysis"]["ci"]["B"], n))  # one image resample for every CI
    gate0 = g0(reg, dv, p, idx)
    print(write(out / "g0.json", stamp(seen, cache_sha256=h, G0=gate0)), gate0["verdict"])
    if gate0["verdict"] == "PASS":
        panel = json.loads((ROOT / reg["data"]["panel"]["path"]).read_text(encoding="utf-8"))["train"]
        r = readout(reg, dv, p, U.segmenter(), panel, idx, expect=reg["p1dev_reference_dev300"])
        print(write(out / "readout.json", stamp(seen, cache_sha256=h, G0_verdict=gate0["verdict"], readout=r)),
              r["verdict"])


# ----------------------------------------------------------------------------------------------- selftest (CPU)
def refused(fn, *args) -> str:
    """The message fn(*args) stops with; AssertionError when it runs instead."""
    try:
        fn(*args)
    except SystemExit as stop:
        return str(stop)
    raise AssertionError(f"{fn.__name__} ran where it must refuse")


def _refusals(tmp: Path) -> None:
    def variant(edit, pins=None) -> tuple[Path, Path]:
        reg = json.loads(PREREG.read_text(encoding="utf-8"))
        edit(reg)
        pre, add = tmp / PREREG.name, tmp / ADDENDUM.name
        pre.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
        pre.with_suffix(".md").write_bytes(PREREG.with_suffix(".md").read_bytes())
        pin = {"new_files": pins or {rel: sha(ROOT / rel) for rel in NEW_FILES}, "deviations": [],
               "prereg_sha256": sha(pre), "prereg_md_sha256": sha(pre.with_suffix(".md"))}
        add.write_text(json.dumps(pin), encoding="utf-8")
        return pre, add

    assert "does not pin this script" in refused(check, *variant(lambda r: None, {NEW_FILES[0]: ""}))
    assert "UPE constants" in refused(check, *variant(lambda r: r["upe_constants"].update(LAM=2.5)))
    assert "class map" in refused(check, *variant(lambda r: r["verifier_protocol"]["english_class_map"].pop("chó")))
    upe = "scripts/upe_mbr.py"
    assert upe in refused(check, *variant(lambda r: r["code_at_head"].update({upe: ""})))
    assert DEV_SPLIT in refused(check, *variant(lambda r: r["inputs_sha256"].update({DEV_SPLIT: ""})))
    assert "addendum pins" in refused(check, PREREG, variant(lambda r: None)[1])


def _cache(reg: dict, tmp: Path) -> None:
    vp, cache, keys = reg["verifier_protocol"], tmp / "p_v.jsonl", [("1", "chó"), ("1", "mèo"), ("2", "xe")]
    loaded, asked = [], []

    def load(i):
        loaded.append(i)
        return f"pixels of {i}"

    def ask(question, pixels) -> float:
        asked.append((question, pixels))
        return 0.9 if pixels else 0.4

    first = {"image_id": "1", "class": "chó", "np": "a dog", "p_with": 0.9, "p_without": 0.4}
    cache.write_text(json.dumps(first) + "\n", encoding="utf-8")
    assert fill(cache, keys, vp, load, ask) == 2 and loaded == ["1", "2"], loaded  # a resumed job skips scored items
    cat = vp["question_template"].format(np="a cat")
    assert asked[:2] == [(IMAGE + cat, "pixels of 1"), (cat, None)] and cat.startswith("Is there a cat"), asked
    assert cached(cache, keys) == {k: (0.9, 0.4) for k in keys}
    assert "one row per" in refused(cached, cache, keys[:2])
    sha_file = tmp / "job.sha256"
    sha_file.write_text("", encoding="utf-8")
    assert "before any AUROC" in refused(recorded, cache, sha_file)
    sha_file.write_text(f"{sha(cache)}  p_v.jsonl\n", encoding="utf-8")
    assert recorded(cache, sha_file) == sha(cache)
    kept = write(tmp / "g0.json", {"n": 1})
    assert write(tmp / "g0.json", {"n": 2}).name == "g0_v2.json" and json.loads(kept.read_text())["n"] == 1


def _readme(reg: dict, tmp: Path) -> None:
    readme, h = ROOT / README, reg["models"]["verifier"]["licence"]["readme_sha256"]
    same_as_readme(readme, h)
    edited = tmp / "README.md"
    text = readme.read_text(encoding="utf-8")
    edited.write_text(text.replace("i * j <= max_num", "i * j < max_num"), encoding="utf-8")
    assert "differs from the README" in refused(same_as_readme, edited, sha(edited))
    assert "not the registered README" in refused(same_as_readme, edited, h)
    sizes = ((448, 448), (1000, 500), (1600, 1200))
    tiles = [len(dynamic_preprocess(Image.new("RGB", wh), max_num=12, use_thumbnail=True)) for wh in sizes]
    assert tiles == [1, 3, 13], tiles  # one tile and no thumbnail; 2 + 1; 4 x 3 + 1


def _gate(reg: dict) -> None:
    """G0 on synthetic items whose positive rate rises with the cell: a score that sees the image separates items
    inside a cell, a prior only separates cells. A_within must be within-cell and A_noimg marginal."""
    rng = np.random.default_rng(1)
    img, cell = np.repeat(np.arange(40), 6), rng.integers(0, 4, 240)
    y = (rng.random(240) < 0.15 + 0.23 * cell).astype(float)
    sees, prior, noise = 0.6 * y + 0.4 * rng.random(240), cell / 3, rng.random(240)
    it, idx = {"img": img, "y": y, "cell": cell}, np.random.default_rng(0).integers(0, 40, (200, 40))
    verdicts = []
    for s in (np.c_[sees, noise], np.c_[noise, noise], np.c_[prior, noise], np.c_[sees, prior]):
        st = pool_stats(s, it, idx)
        assert st["A_within"]["ci95"][0] <= st["A_within"]["ci95"][1] and st["n_items"] == 240
        assert sum(c["items"] for c in st["per_cell"].values()) == 240
        verdicts.append(gate(reg, st["A_within"]["point"], st["A_noimg"]["point"]))
    assert verdicts == ["PASS", "KILL", "KILL", "KILL"], verdicts  # PASS; A_within at chance; a prior; a prior leak
    keys = [("n13", j) for j in range(240)] + [("n7", j) for j in range(240)]
    p = dict(zip(keys, [(a, b) for a, b in np.c_[sees, noise]] + [(a, b) for a, b in np.c_[noise, noise]]))
    dv = {"N13": {**it, "key": keys[:240]}, "N7_T0.5": {**it, "key": keys[240:]}}
    res = g0(reg, dv, p, idx)  # the gate reads N13 (informative here), not N7_T0.5 (noise)
    assert res["verdict"] == "PASS" and res["A_within"] == res["pools"]["N13"]["A_within"]["point"]
    assert [gate(reg, *a) for a in ((0.58, 0.6), (0.5799, 0.5), (0.7, 0.6001))] == ["PASS", "KILL", "KILL"]
    assert prior_leak(reg, 1.0, 0.7) and not prior_leak(reg, 1.0, 0.69) and not prior_leak(reg, -0.2, 0.5)
    edge = {"dF1_vs_COUNT": 0.5, "dCHAIRi_vs_COUNT_x100": -1.0, "dCIDEr_vs_greedy_x100": -2.0,
            "panel_dF1_vs_COUNT": -0.5}  # every carry threshold met exactly: carried; one step past any one: not
    assert carried(reg, edge, False) and not carried(reg, edge, True)
    for k, x in (("dF1_vs_COUNT", 0.49), ("dCHAIRi_vs_COUNT_x100", -0.99), ("dCIDEr_vs_greedy_x100", -2.01),
                 ("panel_dF1_vs_COUNT", -0.51)):
        assert not carried(reg, {**edge, k: x}, False), k


def _readout(reg: dict) -> None:
    """The §6.3 path on a synthetic pool, whitespace tokens: greedy names a true and an invented animal, three samples
    name the two true ones. A verifier that sees the image picks those, COUNT cannot tell the two captions apart."""
    animals = ["chó", "mèo", "gà", "bò", "ngựa", "voi", "vịt", "lợn"]
    ids, refs, pool, panel, sure = [], {}, [], {}, {}
    for n in range(24):
        i, (t1, t2, f) = str(n + 1), (animals[n % 8], animals[(n + 3) % 8], animals[(n + 5) % 8])
        g, a = f"một con {t1} và một con {f} trên bãi cỏ", f"một con {t1} và một con {t2} trên bãi cỏ"
        ids.append(i)
        pool.append([g, a, g, a, g, a, g])
        refs[i] = [a, f"con {t1} và con {t2} đứng trên cỏ", f"một con {t2} cạnh một con {t1}",
                   f"con {t1} chơi với con {t2} trên cỏ", f"hai con {t1} và {t2} trên bãi cỏ"]
        panel[i] = [f"con {t2} và con {t1} trên cỏ"]
        sure.update({(i, o): (0.95 if o != f else 0.05, 0.5) for o in (t1, t2, f)})
    train = {f"t{k}": [f"một con {animals[k % 8]} và một con {animals[(k + 1) % 8]} trên bãi cỏ"] * 5
             for k in range(16)}
    dv = {"ids": ids, "refs": refs, "pool7": pool, "train": train}
    reg = {**reg, "data": {**reg["data"], "panel": {**reg["data"]["panel"], "dev_images_with_panel": len(ids)}}}
    idx = np.random.default_rng(0).integers(0, len(ids), (200, len(ids)))

    def tok(texts):
        return [t.lower().split() for t in texts]

    runs = [readout(reg, dv, q, tok, panel, idx) for q in
            (sure, {k: (w, w) for k, (w, _) in sure.items()}, {k: (0.5, 0.5) for k in sure})]
    assert [r["verdict"] for r in runs] == ["CARRIED", "KILL (prior leak)", "NOT CARRIED"], [r["verdict"] for r in runs]
    measured = runs[0]["greedy"]
    exact = {k: round(x, 3) if k in ROUNDED else x for k, x in measured.items()}
    reproduces(exact, measured)
    for k, step in (("F1_ktvic5", 0.01), ("CIDEr_D_x100", 1e-3)):
        assert k in refused(readout, reg, dv, sure, tok, panel, idx, {**exact, k: exact[k] + step}), k


def selftest() -> None:
    """CPU only, no JVM: the registration checks and their refusals, the real dev300 items, the cache, the README
    image code, and G0, the prior-leak kill and the carry rule each way, on synthetic scores and a synthetic pool."""
    reg, _ = check()
    dv = dev(reg)  # the real dev300 pools: the registered item counts, and every N7_T0.5 item is an N13 item
    assert set(dv["N7_T0.5"]["key"]) <= set(dv["N13"]["key"]) and len(dv["pool7"][0]) == 1 + U.K_SAMPLES
    items = reg["data"]["items"]
    fewer = {**reg, "data": {**reg["data"], "items": {**items, "N13": {**items["N13"], "n_items": 1305}}}}
    assert "N13 item counts" in refused(dev, fewer)
    with tempfile.TemporaryDirectory() as tmp:
        _refusals(Path(tmp))
        _cache(reg, Path(tmp))
        _readme(reg, Path(tmp))
    _gate(reg)
    _readout(reg)
    print("xv_ef1 selftest ok")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="mode")
    sub.add_parser("score", help="GPU: fill DIR/p_v.jsonl").add_argument("--out", required=True)
    a = sub.add_parser("analyse", help="CPU: G0, then the dev readout if G0 passes")
    for flag in ("--cache", "--sha-file", "--out"):
        a.add_argument(flag, required=True)
    args = ap.parse_args()
    if args.selftest:
        selftest()
    elif args.mode:
        {"score": score, "analyse": analyse}[args.mode](args)
    else:
        ap.error("a mode (score, analyse) or --selftest")
    return 0


if __name__ == "__main__":
    sys.exit(main())
