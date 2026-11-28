"""Verifier probe runner for G1 (Vintern-1B-v3_5) and G2 (InternVL3-8B), prereg v3 §4.1 + ERRATUM_O31_1 E2/E3.

Score per probe: s = p(yes) / (p(yes) + p(no)) at the answer position; yes/no sets = the first tokens of
{Có, có, " Có", " có"} / {Không, không, " Không", " không"} (VinternAdapter._yes_no_ids). The question is the
recorded stage-1 question (Q+ text) wrapped by m0.instruct, byte-identical to E1b.

- vintern (G1): E1b's procedure unchanged: m0.check_model + rescap get_vlm("vintern-1b") + m0.probe, batch 1, every
  unique Vintern question of a record (e1e2.vintern_questions), transformers 4.51.3 (m0 PREREG §1).
- internvl3 (G2): OpenGVLab/InternVL3-8B-hf @ 259a3b64 (the E2b pin, B-N1 registry 9ff02dc2), loaded by
  decode_hf_vlm.load unchanged; one forward pass, softmax at the last position; Q+ only (erratum E3). This class needs
  transformers >= 4.52 (E2b ran it in venv-lb, transformers 4.57.6); 4.51.3 cannot load it.
- Batch: 1 for both families. Vintern as E1b. InternVL3 by ERRATUM_O31_G2: on the registered 24 GB GPU the batch-8
  pass of the ERRATUM_O31_2 E4 rule cannot be computed, so its condition cannot be met. probe_job keeps that parity
  path (PROBE_TOL = m0.EQUIV_TOL 1e-3, first 50 images) for a family whose "batch" holds 8; no registered family does.
- Output: shards of SHARD_IMAGES images; a shard is written to *.partial, renamed when complete and its sha256 is
  appended to SHARDS.sha256; a rerun skips verified shards and resumes the partial one. finalize() writes the E3
  table probes.jsonl (+ .sha256). Non-finite s, a STOP marker or the cap -> STOP. Logs print counts only.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import statistics
import time
from pathlib import Path

from . import repo
from .verify import FAIR_MODEL, MASS_FLOOR, SMOKE_N, affirmative_key, qkey

YES_WORDS = ("Có", "có", " Có", " có")
NO_WORDS = ("Không", "không", " Không", " không")
YES_NO = ("có", "không")  # m0.YES_NO
PROBE_TOL, PARITY_IMAGES, BATCHES = 1e-3, 50, (1, 8)
SHARD_IMAGES = 100
STOP = "STOP.json"
FAMILIES = {
    "vintern": {"repo": FAIR_MODEL, "revision": "b98f263eab246eb5269ade64edbdca8a887dc44d", "transformers": "4.51.3",
                "questions": "all", "batch": (1,), "cap_h": 3.5},
    "internvl3": {"repo": "OpenGVLab/InternVL3-8B-hf", "revision": "259a3b64a14623c0ec91a045cb43f7c5af5fa6af",
                  "registry_key": "internvl3_8b", "transformers": "4.57.6", "questions": "q_plus", "batch": (1,),
                  "cap_h": 48.0},  # ERRATUM_O31_G2: batch 1 (E4 clarified); G2 cap 48 h from launch.json t0 (E7)
}
REGISTRY = "manuscript/prereg/2026-10-19_b_n1_vi_leaderboard.json"  # B-N1, sha 9ff02dc2 (E2b's pin source)
TOUCHED_SHA = "91db7e2fbb3d479f79ed19fca4aa100399730910cd7511f832576350f26f9b63"  # m0 dev_touched_ids.txt (e1e2 PIN)


def instruct(q: str) -> str:
    """m0.instruct, byte-identical to VinternAdapter.yes_no_logit(instruct=True)."""
    return f"{q.rstrip('?')}? Chỉ trả lời 'có' hoặc 'không'."


# ------------------------------------------------------------------ work list
def work(records: list[dict], family: str) -> list[tuple[str, list[tuple[str, str]]]]:
    """[(image file name, [(qkey, question)])] in file-name order. vintern: every unique Vintern question of the record,
    first occurrence kept (e1e2.vintern_questions); internvl3: each proposition's Q+ (erratum E3), unique per image."""
    mode = FAMILIES[family]["questions"]
    out = []
    for r in sorted(records, key=lambda x: x["file_name"]):
        qs: dict[str, str] = {}
        for p in r["propositions"]:
            if mode == "all":
                for q in (p.get("evidence") or {}).get("probes") or []:
                    if str(q.get("model", "")) == FAIR_MODEL and q.get("question_vi"):
                        qs.setdefault(qkey(q["question_vi"]), q["question_vi"])
            else:
                k = affirmative_key(p)
                if k is not None:
                    q = next(x["question_vi"] for x in p["evidence"]["probes"]
                             if str(x.get("model", "")) == FAIR_MODEL and x.get("question_vi"))
                    qs.setdefault(k, q)
        out.append((r["file_name"], list(qs.items())))
    return out


# ------------------------------------------------------------------ tokens and the HF probe
def yes_no_ids(tokenizer) -> tuple[list[int], list[int]]:
    def first(words):
        return sorted({tokenizer.encode(w, add_special_tokens=False)[0] for w in words})
    return first(YES_WORDS), first(NO_WORDS)


def token_ok(tokenizer, yes: list[int], no: list[int]) -> bool:
    """m0.token_check rule: non-empty, disjoint, and every id decodes to a prefix of có / không."""
    dec = lambda ids: [tokenizer.decode([i]).strip().lower() for i in ids]  # noqa: E731
    return (bool(yes) and bool(no) and not set(yes) & set(no)
            and all(d and YES_NO[0].startswith(d) for d in dec(yes)) and all(d and YES_NO[1].startswith(d) for d in dec(no)))


def make_hf_probe(proc, net):
    """probe(images, questions) -> [(s, mass, top_token, n_tok)]: one forward pass on a left-padded batch, softmax over
    the vocabulary at the last position (= one greedy step, as E2b's make_probe)."""
    import torch

    tok = getattr(proc, "tokenizer", proc)
    tok.padding_side = "left"
    yes, no = yes_no_ids(tok)
    if not token_ok(tok, yes, no):
        raise SystemExit("FAULT yes/no first tokens do not decode to có / không prefixes")

    def probe(images, questions):
        msgs = [[{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": instruct(q)}]}] for q in questions]
        texts = [proc.apply_chat_template(m, tokenize=False, add_generation_prompt=True) for m in msgs]
        enc = proc(text=texts, images=list(images), return_tensors="pt", padding=True).to(net.device, net.dtype)
        with torch.no_grad():
            pr = torch.softmax(net(**enc).logits[:, -1].float(), dim=-1)
        py, pn = pr[:, yes].sum(-1).tolist(), pr[:, no].sum(-1).tolist()
        top = [tok.decode([i]).strip() for i in pr.argmax(-1).tolist()]
        n_tok = enc["attention_mask"].sum(-1).tolist()
        return [(a / (a + b) if a + b > 0 else float("nan"), a + b, t, int(n)) for a, b, t, n in zip(py, pn, top, n_tok)]
    return probe


def vintern_probe(ad):
    """E1b's probe, unchanged: m0.probe on the adapter's pixel values, batch 1 (one-image pixel cache as e1e2)."""
    repo()
    import m0

    cache: dict = {}

    def probe(images, questions):
        out = []
        for im, q in zip(images, questions):
            if cache.get("id") is not im:
                cache.update(id=im, pv=ad._pixel_values(im))
            text, p, mass = m0.probe(ad, cache["pv"], q)
            out.append((p, mass, text, None))
        return out
    return probe


# ------------------------------------------------------------------ smoke and batch parity
def smoke(rows: list[dict]) -> dict:
    """First 20 probes: finite s, median yes+no mass >= 0.5 (verify.smoke_ok rule)."""
    first = rows[:SMOKE_N]
    masses = [r["mass"] for r in first]
    ok = len(first) == SMOKE_N and all(math.isfinite(r["p_yes"]) for r in first) and \
        statistics.median(masses) >= MASS_FLOOR
    return {"n": len(first), "median_mass": statistics.median(masses) if masses else None, "ok": ok}


def batch_parity(b1: list[dict], bb: list[dict], n_images: int) -> dict:
    """Batch > 1 only if the same (image, q) pairs from >= 50 images agree: |s_b - s_1| <= 1e-3 and equal top token."""
    k1, kb = {(r["image"], r["q"]): r for r in b1}, {(r["image"], r["q"]): r for r in bb}
    bad = [k for k in k1 if k not in kb or abs(k1[k]["p_yes"] - kb[k]["p_yes"]) > PROBE_TOL or k1[k]["top"] != kb[k]["top"]]
    ok = n_images >= PARITY_IMAGES and k1.keys() == kb.keys() and not bad
    max_d = max((abs(k1[k]["p_yes"] - kb[k]["p_yes"]) for k in k1 if k in kb), default=None)
    return {"ok": ok, "n_images": n_images, "n_probes": len(k1), "n_bad": len(bad), "max_abs_diff": max_d}


# ------------------------------------------------------------------ resumable sharded pass
def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sha_lines(items) -> str:
    """sha256 of the items, one per line (e1e2.sha_lines form)."""
    return hashlib.sha256("".join(f"{x}\n" for x in items).encode()).hexdigest()


def _stopped(out: Path) -> None:
    if (out / STOP).exists():
        raise SystemExit(f"REFUSED: {out / STOP} exists; no resume without a ruling")


def halt(out: Path, rc: int, reason: str) -> int:
    (out / STOP).write_text(json.dumps({"rc": rc, "reason": reason, "time": time.time()}) + "\n")
    print(reason)
    return rc


def done_shards(out: Path) -> dict[int, str]:
    """{shard: sha} from SHARDS.sha256, each re-checked against its file (a mismatch is a FAULT)."""
    f = out / "SHARDS.sha256"
    got = {}
    for line in f.read_text().splitlines() if f.exists() else []:
        sha, name = line.split()
        if _sha(out / name) != sha:
            raise SystemExit(f"FAULT {name}: sha256 differs from SHARDS.sha256")
        got[int(name.split("_")[1].split(".")[0])] = sha
    return got


def run_pass(probe, items: list, out: Path, batch: int, load_image, cap_h: float, t0: float | None = None,
             shard_images: int = SHARD_IMAGES) -> int:
    """items = work(); probe(images, questions) -> [(s, mass, top, n_tok)]. Returns 0 when every shard is complete."""
    out.mkdir(parents=True, exist_ok=True)
    _stopped(out)
    t0 = t0 if t0 is not None else time.time()
    done = done_shards(out)
    for k in range(0, (len(items) + shard_images - 1) // shard_images):
        if k in done:
            continue
        part = out / f"shard_{k:05d}.jsonl.partial"
        have = {(r["image"], r["q"]) for r in map(json.loads, part.read_text(encoding="utf-8").splitlines())} \
            if part.exists() else set()
        with open(part, "a", encoding="utf-8") as fh:
            for name, qs in items[k * shard_images:(k + 1) * shard_images]:
                if (time.time() - t0) / 3600 > cap_h:
                    return halt(out, 4, f"CAP_STOP in shard {k}")
                todo = [(key, q) for key, q in qs if (name, key) not in have]
                if not todo:
                    continue
                im = load_image(name)
                for i in range(0, len(todo), batch):
                    sl = todo[i:i + batch]
                    t = time.perf_counter()
                    res = probe([im] * len(sl), [q for _k, q in sl])
                    sec = (time.perf_counter() - t) / len(sl)
                    for (key, _q), (s, mass, top, n_tok) in zip(sl, res):
                        fh.write(json.dumps({"image": name, "q": key, "p_yes": s, "mass": mass, "top": top,
                                            "n_tok": n_tok, "batch": batch, "sec": sec}, ensure_ascii=False) + "\n")
                        if not math.isfinite(s):
                            fh.flush()
                            return halt(out, 2, f"FAULT non-finite s in shard {k}")
                fh.flush()
                os.fsync(fh.fileno())
        final = out / f"shard_{k:05d}.jsonl"
        part.replace(final)
        with open(out / "SHARDS.sha256", "a", encoding="utf-8") as fh:
            fh.write(f"{_sha(final)}  {final.name}\n")
        print(f"shard {k}: {sum(len(q) for _n, q in items[k * shard_images:(k + 1) * shard_images])} probes; "
              f"elapsed {(time.time() - t0) / 3600:.2f} h")
    return 0


def finalize(items: list, out: Path, shard_images: int = SHARD_IMAGES) -> dict:
    """probes.jsonl (E3 table rows: image, q, p_yes + recorded fields) from the verified shards, in work order;
    every work pair exactly once, all s finite; writes probes.jsonl.sha256."""
    _stopped(out)
    n_shards = (len(items) + shard_images - 1) // shard_images
    done = done_shards(out)
    if set(done) != set(range(n_shards)):
        raise SystemExit(f"INCOMPLETE: {n_shards - len(done)} shard(s) missing")
    rows = [json.loads(x) for k in range(n_shards) for x in (out / f"shard_{k:05d}.jsonl").read_text(encoding="utf-8").splitlines()]
    want = [(n, key) for n, qs in items for key, _q in qs]
    got = [(r["image"], r["q"]) for r in rows]
    if sorted(got) != sorted(want) or len(set(got)) != len(got):
        raise SystemExit("FAULT probe rows are not exactly the work pairs")
    if not all(math.isfinite(r["p_yes"]) for r in rows):
        raise SystemExit("FAULT non-finite s")
    pf = out / "probes.jsonl"
    pf.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    (out / "probes.jsonl.sha256").write_text(f"{_sha(pf)}  probes.jsonl\n")
    return {"rows": len(rows), "images": len(items), "sha256": _sha(pf)}


def probe_rows(probe, items: list, batch: int, load_image) -> list[dict]:
    """In-memory rows of `items` at a given batch (smoke and parity phase)."""
    rows = []
    for name, qs in items:
        im = load_image(name)
        for i in range(0, len(qs), batch):
            sl = qs[i:i + batch]
            for (key, _q), (s, mass, top, n_tok) in zip(sl, probe([im] * len(sl), [q for _k, q in sl])):
                rows.append({"image": name, "q": key, "p_yes": s, "mass": mass, "top": top, "n_tok": n_tok})
    return rows


def probe_job(probe, items: list, out: Path, family: str, load_image, cap_h: float | None = None) -> int:
    """G1/G2 job: smoke + batch parity on the first 50 images (once, smoke.json), the sharded pass at the chosen
    batch, then finalize. The cap clock starts at launch.json t0 and survives resumes."""
    out.mkdir(parents=True, exist_ok=True)
    _stopped(out)
    lf = out / "launch.json"
    if not lf.exists():
        lf.write_text(json.dumps({"t0": time.time(), "family": family, "images": len(items),
                                  "probes": sum(len(q) for _n, q in items)}) + "\n")
    t0 = json.loads(lf.read_text())["t0"]
    sf = out / "smoke.json"
    if not sf.exists():
        head = items[:PARITY_IMAGES]
        rows1 = probe_rows(probe, head, 1, load_image)
        rec = {"smoke": smoke(rows1), "batch": 1}
        if 8 in FAMILIES[family]["batch"]:
            rec["parity"] = batch_parity(rows1, probe_rows(probe, head, 8, load_image), len(head))
            rec["batch"] = 8 if rec["parity"]["ok"] else 1
        sf.write_text(json.dumps(rec) + "\n")
    rec = json.loads(sf.read_text())
    if not rec["smoke"]["ok"]:
        return halt(out, 2, "FAULT smoke (finite s, median yes+no mass >= 0.5 over the first 20 probes)")
    rc = run_pass(probe, items, out, rec["batch"], load_image, cap_h if cap_h is not None else FAMILIES[family]["cap_h"], t0)
    if rc:
        return rc
    f = finalize(items, out)
    print(json.dumps({"status": "DONE", "rows": f["rows"], "images": f["images"], "batch": rec["batch"],
                      "elapsed_h": (time.time() - t0) / 3600}))
    return 0


# ------------------------------------------------------------------ inputs
def records(dirs: list[Path], exclude: Path | None) -> list[dict]:
    drop = set(exclude.read_text(encoding="utf-8").split()) if exclude else set()
    recs = [json.loads(p.read_text(encoding="utf-8")) for d in dirs for p in sorted(d.glob("*.json"))
            if not p.name.startswith("_")]
    names = [r["file_name"] for r in recs]
    if len(set(names)) != len(names):
        raise SystemExit("FAULT duplicate file names across record folders")
    return [r for r in recs if r["file_name"] not in drop]


def g2_inputs(dirs: list[Path], exclude: Path | None) -> None:
    """ERRATUM_O31_2 E4: G2 is one job over every pool image with records, after G1: the record folders hold all
    3,769 KTVIC-train images (the 3,700 plus G1's 69) and the exclude file holds both byte twins."""
    from .stage1 import N_TRAIN, TWINS

    n = sum(1 for d in dirs for p in d.glob("*.json") if not p.name.startswith("_"))
    drop = set(exclude.read_text(encoding="utf-8").split()) if exclude else set()
    if n != N_TRAIN or not set(TWINS) <= drop:
        raise SystemExit(f"REFUSED G2 needs all {N_TRAIN} records (3,700 + G1's 69) and the twins excluded; got {n}")


M0_DIR = "manuscript/prereg/2026-10-31_vsps_j_m0"
SMOKE_NAME = re.compile(r"COCO_val2014_(\d{12})\.jpg")


def refused_shas() -> set:
    """Every image_sha256 group of exclusion.json (pinned c52a96d1): KTVIC test, UIT-ViIC test, CHAIR-500, CV-295,
    XM3600."""
    root = repo()
    ex = json.loads((root / "manuscript/prereg/2026-10-21_dev_pools/exclusion.json").read_text(encoding="utf-8"))
    return {h for v in ex["image_sha256"].values() for h in v}


def explored(names: list[str], folder: Path, refused: set | None = None, m0_dir: Path | None = None) -> None:
    """H-G custody: exactly 5 COCO val2014 file names that M0 fetched (fetch_images.txt) and touched (dev_touched_ids),
    none in COCO Karpathy test (O31 tier 2; karpathy_test_val_ids.txt) and none whose bytes are in exclusion.json.
    m0_dir (tests only) replaces the pinned M0 folder; the touched list is sha-checked either way."""
    root = repo()
    d = m0_dir or root / M0_DIR
    if _sha(d / "dev_touched_ids.txt") != TOUCHED_SHA:
        raise SystemExit("FAULT dev_touched_ids.txt sha differs from the pin")
    touched = {int(x) for x in (d / "dev_touched_ids.txt").read_text().split()}
    fetched = set((d / "fetch_images.txt").read_text().split())
    kar = {int(x) for x in (d / "karpathy_test_val_ids.txt").read_text().split()}
    refused = refused_shas() if refused is None else refused
    bad = []
    for n in names:
        m = SMOKE_NAME.fullmatch(n)
        if not m or n not in fetched or int(m.group(1)) not in touched or int(m.group(1)) in kar \
                or _sha(folder / n) in refused:
            bad.append(n)
    if bad or len(names) != 5 or len(set(names)) != 5:
        raise SystemExit(f"REFUSED smoke images must be 5 distinct explored M-HalDetect val images; refused: {bad}")


# ------------------------------------------------------------------ host loaders (GPU; not run on the laptop)
def registry_entry(key: str) -> dict:
    root = repo()
    reg = json.loads((root / REGISTRY).read_text(encoding="utf-8"))
    return reg["models"][key]


def check_env(family: str) -> None:
    import transformers

    if transformers.__version__ != FAMILIES[family]["transformers"]:
        raise SystemExit(f"FAULT {family} needs transformers {FAMILIES[family]['transformers']}, "
                         f"found {transformers.__version__}")


def load(family: str, snapshot: Path, device: str = "cuda"):  # pragma: no cover - host GPU
    """(probe function, info) for a family, from a pinned snapshot."""
    check_env(family)
    repo()
    if family == "vintern":
        import m0
        from rescap.vlm.registry import get_vlm

        m0.check_model(snapshot)
        ad = get_vlm(m0.MODEL["name"], model_id=FAIR_MODEL, device=device,
                     dtype="bfloat16" if device == "cuda" else "float32").load()
        if ad.max_tiles != m0.MODEL["max_tiles"]:
            raise SystemExit("FAULT max_tiles is not the registry value 4")
        tok = m0.token_check(ad)
        if not tok["ok"]:
            raise SystemExit("FAULT Vintern yes/no token check")
        return vintern_probe(ad), {"files": m0.MODEL["files"], "revision": m0.MODEL["revision"]}
    import decode_hf_vlm as LB

    m = registry_entry(FAMILIES[family]["registry_key"])
    if m["revision"] != FAMILIES[family]["revision"]:
        raise SystemExit("FAULT registry revision differs from the O31 pin")
    LB.check_snapshot(m, snapshot)
    proc, net = LB.load(m, snapshot, "cuda:0" if device == "cuda" else device)
    return make_hf_probe(proc, net), {"revision": m["revision"], "n_files": len(m["files"])}
