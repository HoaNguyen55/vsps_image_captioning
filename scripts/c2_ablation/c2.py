#!/usr/bin/env python3
"""Paper C, C-2 (DEV-B MECHANISM, NON-CONFIRMATORY): memory-size (AB-M), k (AB-K) and guard-threshold (AB-tau)
ablations on OV-dev-B (925). Prereg manuscript/prereg/2026-10-28_c2_ablation/PREREG.md (CC-126 W12, PI-1026ac Q8).

The stage-2 modules are imported unchanged; their sha256 must match the stage-2 SHA256SUMS before any import.

  python scripts/c2_ablation/c2.py --selftest                                                  CPU, synthetic only
  python scripts/c2_ablation/c2.py subsets --lists L --out F              laptop: the nested 10% / 30% cluster ids
  python scripts/c2_ablation/c2.py check                                  prereg folder and subset pins
  python scripts/c2_ablation/c2.py runs [--ablation M|K] [--model M]      ca_ run ids of the registered grid
  python scripts/c2_ablation/c2.py guard --head H                         M3 only: host, idle GPU, C-EN, locks
  python scripts/c2_ablation/c2.py lock --path P                          take this experiment's lock (O_EXCL)
  python scripts/c2_ablation/c2.py left --used F --marker M               seconds for the next GPU step, 0 = STOP
  python scripts/c2_ablation/c2.py replay --l2 F --decide-ov F --out J    CPU: the four stage-2 rows, before any decode
  python scripts/c2_ablation/c2.py exemplars --pct P --lists L --emb1 E1 --emb Q --out X          CPU (M3)
  python scripts/c2_ablation/c2.py decode --run-ids R ... --snapshot DIR --lists L --s2 D --out-dir D [--parity]  GPU
  python scripts/c2_ablation/c2.py items --runs R ... --s2 D --lists L --out I                    CPU
  python scripts/c2_ablation/c2.py verify --items I --s2 D --lists L --snapshot DIR --out CACHE   GPU
  python scripts/c2_ablation/c2.py score --runs R ... --s2 D --cache C --lists L --kit-b K --ledger F  CPU (M3)
  python scripts/c2_ablation/c2.py decide --l2 F --ledger F --s2 D --out D                        CPU, once
Every output path on a GPU host lies under /root/outputs/c2_ablation/. No caption is printed or written to a ledger.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
S2_SUMS = ROOT / "manuscript/prereg/2026-10-22_c_stage2/SHA256SUMS"


def sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def check_sums(sums: Path, prefix: str = "") -> dict[str, str]:
    """Every line of a SHA256SUMS (paths from the repo root) whose path starts with prefix must verify."""
    out = {}
    for line in sums.read_text(encoding="utf-8").splitlines():
        h, rel = line.split(maxsplit=1)
        if rel.startswith(prefix):
            if sha_file(ROOT / rel) != h:
                raise SystemExit(f"{rel}: differs from {sums.relative_to(ROOT)}")
            out[rel] = h
    return out


check_sums(S2_SUMS, "scripts/c_stage2/")
sys.path.insert(0, str(ROOT / "scripts/c_stage2"))
import decide2 as DC2  # noqa: E402  stage-2 modules, unchanged (stage2 checks the stage-1 shas)
import decode2 as D2  # noqa: E402
import guard2 as G2  # noqa: E402
import score2 as SC2  # noqa: E402
import stage2 as S2  # noqa: E402

C, G, lb, BM, S = S2.C, S2.G, S2.lb, D2.BM, DC2.S
LABEL = "C-2 / DEV-B MECHANISM, NON-CONFIRMATORY"
SCHEMA = "vsps.c2_ablation.v1"
PDIR = "manuscript/prereg/2026-10-28_c2_ablation"
SUBSETS = ROOT / PDIR / "c2_memory_subsets.json"
SUBSETS_SHA256 = "ae5f67319c1063c10574feda68e6fecdd88ed3045876d5d1710a0ede034715f0"
DS, N_IMG, N_CLUSTERS = "ov_dev_b", 925, 8190
PCTS = {10: 819, 30: 2457}  # floor(8190 x pct / 100), nested prefixes of one seeded permutation
SUBSET_SEED = ("ablation", "memory", "0")  # BM.seed -> paperC|ablation|memory|0
K_NEW = {"qwen25vl_7b": (2, 4), "internvl3_8b": (2, 8)}  # the frozen k (8 / 4) is the stage-2 row
SESOI = 2.0
PARITY_N, PARITY_MIN = 52, 0.95  # the first 13 / 26 whole batches (b = 4 / 2), as C test's E4 (CC-103a X3)
SOFT_S, HARD_S, MIN_STEP_S = 5 * 3600, 6 * 3600, 60
OUT_ROOT = Path("/root/outputs/c2_ablation")
OUTPUTS = Path("/root/outputs")
LOCK = OUT_ROOT / "RUNNING"
#: stage-2 outputs this experiment reads, pinned (outputs/c_stage2/SHA256SUMS on M3 lists them; the ledger and the
#: decide file are the run record's, C_STAGE2_RUN_RECORD.md)
L2_SHA256 = "be716482c6f934e975bdbc58927cfc42a4c0ff589c9c5f95affd67c03eac0938"
DECIDE_OV_SHA256 = "92fdbf0e59beb836b441dd2e8e847898e37425dba7d29da8f5265f802c284a4b"
EX2 = ("ex_ov_dev_b.json", "072b17d14d89aa21110794be27168cf4ef4212a569a4d55d54c5acf1de7e5a41")
EMB2 = ("emb_ov_dev_b.npz", "5ad23a678650ae736243a45c39915aaf795a5a46721fd855f67d155945bc8c95")
CACHE2 = "guard/ov_dev_b_internvl3_8b.cache.jsonl"
#: registered stage-2 values (C Table 11/13; K16 C2 l.29) the replay must reproduce to 2 dp before any decode
REPLAY = {"pooled": (6.04, 4.54, 7.58), "qwen25vl_7b": (9.67, 7.68, 11.72), "internvl3_8b": (2.41, 0.57, 4.26),
          "internvl3_8b_tau_-inf": (5.36, 3.53, 7.12)}
TAU_FINITE = ("0.00", "0.10", "0.20", "0.30")
SEEN_TAUS = ("-inf", "0.10")  # the only tau rows of InternVL3 anyone has read (stage 2, Table 13)


def replay_keep(r: dict) -> bool:
    """CC-128 W7: InternVL3 rows at tau -inf / 0.10 and Qwen rows at -inf only (Qwen's tau rows are never loaded)."""
    return (r["model"] == "internvl3_8b" and r["tau"] in SEEN_TAUS) or (r["model"] == "qwen25vl_7b"
                                                                         and r["tau"] == "-inf")


def out_ok(p: Path | str) -> Path:
    """On a GPU host, a C-2 output outside /root/outputs/c2_ablation/ is refused (as ctest.out_ok)."""
    p = Path(p)
    if os.environ.get("VSPS_MACHINE_ID") and not p.resolve().is_relative_to(OUT_ROOT):
        raise SystemExit(f"REFUSED: {p} is not under {OUT_ROOT}")
    return p


# ------------------------------------------------------------------------------------------------ host, locks, cap
def gpu_host(mid: Path = Path("/root/.vsps_machine_id")) -> bool:
    """The env first, then the machine-id file; an OSError on the path (the laptop cannot traverse /root) is not a
    GPU host (C-EN amendment 1)."""
    if os.environ.get("VSPS_MACHINE_ID"):
        return True
    try:
        return mid.exists()
    except OSError:
        return False


def isolation(outputs: Path = OUTPUTS, names: list[str] | None = None, tmux: str | None = None) -> list[str]:
    """Reasons this job may not start: outside tmux, a C-EN (cen*) tmux session, or any /root/outputs/*/RUNNING
    lock (G-RL, B-1, C-2). Non-raising where /root is not traversable."""
    tmux = os.environ.get("TMUX", "") if tmux is None else tmux
    if names is None:
        r = subprocess.run(["tmux", "ls", "-F", "#S"], capture_output=True, text=True)
        names = r.stdout.split() if r.returncode == 0 else []
    try:
        found = sorted(str(p) for p in outputs.glob("*/RUNNING"))
    except OSError:
        found = []
    bad = [] if tmux else ["not inside a tmux session (cen_chain.sh refuses while one exists)"]
    return bad + [f"C-EN tmux session {n}" for n in names if n.startswith("cen")] + [f"lock {p} exists" for p in found]


def take_lock(path: Path, outputs: Path = OUTPUTS, names: list[str] | None = None, tmux: str | None = None) -> None:
    bad = isolation(outputs, names, tmux)
    if bad:
        raise SystemExit("REFUSED: " + "; ".join(bad))
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    os.write(fd, f"{sys.argv[0]} pid {os.getppid()}\n".encode())
    os.close(fd)


def cmd_guard(a) -> None:
    """M3 only, idle GPU, committed HEAD and a clean tree (grl common.host_ok), C-EN not running and no protected
    C-EN set staged (common.m3_clear), and isolation() minus this job's own lock."""
    sys.path.insert(0, str(ROOT / "scripts/grl"))
    import common as K

    if K.host_ok(a.head) != "m3":
        raise SystemExit("REFUSED: C-2 runs on M3 only")
    K.m3_clear()
    others = [x for x in isolation() if x != f"lock {LOCK} exists"]
    if others:
        raise SystemExit(f"REFUSED: {others}")
    print("guard ok")


def used_seconds(used: Path, now: float | None = None) -> float:
    """GPU seconds in gpu_seconds.tsv. A step writes `NAME start EPOCH` before it runs and `NAME SECONDS` after it
    returns (CC-128 W6). A start with no end line after it (a reboot or kill mid-step) is charged from its EPOCH to
    the next start line, or to now if it is the last line, so a reboot cannot undercount the cap."""
    if not used.exists():
        return 0.0
    lines = [x.split() for x in used.read_text().splitlines() if x.strip()]
    total, open_t = 0.0, None
    for p in lines:
        if len(p) == 3 and p[1] == "start":
            if open_t is not None:
                total += float(p[2]) - open_t
            open_t = float(p[2])
        else:
            total += float(p[1])
            open_t = None
    if open_t is not None:
        total += (time.time() if now is None else now) - open_t
    return total


def left(used: Path, marker: Path) -> int:
    """Timeout for the next GPU step: HARD_S minus the GPU seconds used, if fewer than SOFT_S are used; else 0
    (no new GPU step after 5 GPU-h; a running step is killed at 6). A CAP_STOP marker is final."""
    if marker.exists():
        return 0
    s = used_seconds(used)
    rest = int(HARD_S - s)
    return rest if s < SOFT_S and rest >= MIN_STEP_S else 0


# ------------------------------------------------------------------------------------------------ subsets, grid
def make_subsets(lists: dict) -> dict:
    """10% and 30% of the 8,190 memory clusters: prefixes of one permutation of the sorted cluster ids by
    random.Random(BM.seed('ablation', 'memory', '0')), so 10% c 30% c 100%. Source composition per subset."""
    cids = sorted(m["cid"] for m in lists["memory"])
    if len(cids) != N_CLUSTERS:
        raise SystemExit(f"lists.json: {len(cids)} clusters, not {N_CLUSTERS}")
    order = random.Random(BM.seed(*SUBSET_SEED)).sample(cids, len(cids))
    srcs = {m["cid"]: tuple(sorted({x[0] for x in m["members"]})) for m in lists["memory"]}

    def comp(ids):
        out: dict[str, int] = {}
        for c in ids:
            out["+".join(srcs[c])] = out.get("+".join(srcs[c]), 0) + 1
        return dict(sorted(out.items()))

    subs = {str(p): sorted(order[:n]) for p, n in PCTS.items()}
    return {"label": LABEL, "rule": "prefixes of random.Random(build_memory.seed('ablation', 'memory', '0'))"
            ".sample(sorted cluster ids, 8190); 10% = 819, 30% = 2457 (floor)", "lists_sha256": C.LISTS_SHA256,
            "composition": {"100": comp(cids)} | {p: comp(v) for p, v in subs.items()},
            "subsets": {p: {"n": len(v), "sha256": hashlib.sha256(json.dumps(v).encode()).hexdigest(), "cids": v}
                        for p, v in subs.items()}}


def load_subsets() -> dict:
    if sha_file(SUBSETS) != SUBSETS_SHA256:
        raise SystemExit(f"{SUBSETS.name}: differs from its pin")
    return json.loads(SUBSETS.read_text(encoding="utf-8"))


def check() -> dict:
    """The prereg folder's SHA256SUMS (paths relative to the folder) and the subsets at their pin."""
    for line in (ROOT / PDIR / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        h, name = line.split(maxsplit=1)
        if sha_file(ROOT / PDIR / name) != h:
            raise SystemExit(f"{name}: differs from the prereg SHA256SUMS")
    return load_subsets()


def spec_c2(cfg: dict, model: str, arm: str, k: int | None = None, pct: int = 100) -> dict:
    """S2.spec with k overridden and the ca_ prefix; pct < 100 marks the memory subset (ret only)."""
    c = {**cfg, "models": {**cfg["models"], model: {**cfg["models"][model], "k": k or cfg["models"][model]["k"]}}}
    s = S2.spec(c, DS, model, arm)
    rid = "ca_" + s["run_id"].removeprefix("c2_") + (f"-m{pct}" if pct != 100 else "")
    return {**s, "run_id": rid, "memory_pct": pct, "c2_ablation": "M" if pct != 100 else "K"}


def grid(cfg: dict) -> dict[str, dict]:
    """AB-M: ret at 10% and 30% for both backbones (rand shared: the stage-2 100% row, CC-126 W12). AB-K: ret and
    rand at the new k of each backbone, 100% memory. 12 runs, priority order."""
    out = [spec_c2(cfg, m, "ret", pct=p) for m in C.MODELS for p in PCTS]
    out += [spec_c2(cfg, m, arm, k=k) for m in C.MODELS for k in K_NEW[m] for arm in ("ret", "rand")]
    return {s["run_id"]: s for s in out}


# ------------------------------------------------------------------------------------------------ stage-2 inputs
def s2_file(d: Path, rel: str) -> Path:
    """A stage-2 output on M3, verified against outputs/c_stage2/SHA256SUMS."""
    sums = dict(reversed(x.split(maxsplit=1)) for x in (d / "SHA256SUMS").read_text().splitlines())
    if sums.get(rel) is None or sha_file(d / rel) != sums[rel]:
        raise SystemExit(f"{d / rel}: not the stage-2 output in its SHA256SUMS")
    return d / rel


def s2_run(d: Path, cfg: dict, model: str, arm: str) -> Path:
    return s2_file(d, f"runs/{DC2.rid(cfg, DS, model, arm)}.preds.json")


def load_l2(path: Path, keep) -> list[dict]:
    """Stage-2 ledger rows of OV-dev-B that `keep(row)` accepts; every other row is dropped as it is read."""
    if sha_file(path) != L2_SHA256:
        raise SystemExit(f"{path}: not the stage-2 ledger be716482")
    rows = []
    for x in path.read_text(encoding="utf-8").splitlines():
        r = json.loads(x)
        if r["dataset"] == DS and keep(r):
            rows.append(r)
    return S.latest(rows)


# ------------------------------------------------------------------------------------------------ replay (CPU)
def replay(rows: list[dict], cfg: dict, decide_ov: dict | None) -> dict:
    """The four stage-2 rows C-2 builds on, recomputed from L2 (decide2.gate, unchanged) and asserted equal to the
    registered values at 2 dp, and the frozen-tau ones to decide_ov.json exactly. rows hold tau -inf / 0.10 only."""
    if not all(replay_keep(r) for r in rows):
        raise SystemExit("replay: an archived tau row was passed in")
    g = DC2.gate(rows, cfg, DS)
    ret, rand = (DC2.get(rows, DC2.rid(cfg, DS, "internvl3_8b", a), "-inf") for a in ("ret", "rand"))
    got = {"pooled": g["pooled_vs_rand"], **{m: g["per_model"][m]["vs_rand"] for m in C.MODELS},
           "internvl3_8b_tau_-inf": S.boot(DC2.cider_diff(ret, rand))}
    bad = {k: [round(v[x], 2) for x in ("d", "lo", "hi")] for k, v in got.items()
           if tuple(round(v[x], 2) for x in ("d", "lo", "hi")) != REPLAY[k]}
    if decide_ov is not None:
        dg = decide_ov["ov_dev_b"]["gate"]
        want = {"pooled": dg["pooled_vs_rand"], **{m: dg["per_model"][m]["vs_rand"] for m in C.MODELS}}
        bad |= {f"{k} (decide_ov.json)": [got[k][x] for x in ("d", "lo", "hi")] for k, v in want.items()
                if any(got[k][x] != v[x] for x in ("d", "lo", "hi"))}
    if bad:
        raise SystemExit(f"REPLAY FAILED (STOP before any decode): {bad}")
    return {"replayed": got, "registered": REPLAY, "passed": True}


def cmd_replay(a) -> None:
    cfg = S2.frozen()
    rows = load_l2(a.l2, replay_keep)
    if sha_file(a.decide_ov) != DECIDE_OV_SHA256:
        raise SystemExit(f"{a.decide_ov}: not decide_ov.json 92fdbf0e")
    rec = replay(rows, cfg, json.loads(a.decide_ov.read_text(encoding="utf-8"))) | {"l2_sha256": L2_SHA256,
                                                                                   "utc": lb.utc()}
    out_ok(a.out).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print("replay ok: the four stage-2 rows reproduce")


# ------------------------------------------------------------------------------------------------ exemplars (CPU)
def cmd_exemplars(a) -> None:
    """build_memory.exemplars (via decode2.build_exemplars, unchanged) on the pct% memory subset: only `ret` is
    used; the near cut 0.92 and the tie rule are unchanged. The stage-2 query vectors are reused (pinned)."""
    out = out_ok(a.out)
    sub = load_subsets()["subsets"][str(a.pct)]
    lists = C.load_lists(a.lists)
    mk, mv, _meta1 = D2.load_emb1(a.emb1)
    if sha_file(a.emb) != EMB2[1]:
        raise SystemExit(f"{a.emb}: not the stage-2 OV-dev-B query vectors {EMB2[1][:8]}")
    z = np.load(a.emb)
    qk = [str(k) for k in z["keys"]]
    if qk != [f"{DS}|{i}" for i, _f, _h in S2.manifest2(DS, lists)]:
        raise SystemExit(f"{a.emb}: not the OV-dev-B query order")
    keep = set(sub["cids"])
    pick = [n for n, k in enumerate(mk) if k in keep]
    if len(pick) != sub["n"]:
        raise SystemExit("memory subset: a cluster id has no stage-1 vector")
    ex = D2.build_exemplars(DS, [mk[n] for n in pick], mv[pick], qk, z["vecs"])
    body = {"design_sha256": C.PINS[C.DESIGN], "lists_sha256": C.LISTS_SHA256, "label": LABEL, "c_schema": SCHEMA,
            "set": DS, "memory_pct": a.pct, "subset_sha256": sub["sha256"], "arms_used": ["ret"],
            "emb_sha256": {"stage1": S2.EMB1_SHA256, DS: EMB2[1]}, "near_cos": BM.NEAR_COS, **ex}
    out.write_text(json.dumps(body) + "\n", encoding="utf-8")
    Path(str(out) + ".sha256").write_text(f"{sha_file(out)}  {out.name}\n")


def exemplars_for(s: dict, s2: Path, exdir: Path, lists_path: Path) -> tuple[Path, dict]:
    path = s2_file(s2, EX2[0]) if s["memory_pct"] == 100 else exdir / f"ex_m{s['memory_pct']}.json"
    if s["memory_pct"] == 100 and sha_file(path) != EX2[1]:
        raise SystemExit(f"{path}: not the stage-2 example lists {EX2[1][:8]}")
    ex = C.load_exemplars(path, lists_path)
    if ex.get("set") != DS or (s["memory_pct"] != 100 and (ex.get("c_schema"), ex.get("memory_pct")) != (
            SCHEMA, s["memory_pct"])):
        raise SystemExit(f"{path}: not the example lists of {s['run_id']}")
    return path, ex


# ------------------------------------------------------------------------------------------------ decode (GPU)
def load_ctx(model: str, snapshot: Path, lists: dict) -> dict:
    reg = C.registration()
    m = reg["models"][model]
    if lb.packages() != reg["venv"]["packages"]:
        raise SystemExit(f"package versions {lb.packages()} differ from the B-N1 venv")
    lb.check_snapshot(m, snapshot)
    ctx = {"caps": C.memory_captions(lists), "zs": lb.prompt_text(reg, "short"), "m": m,
           "n_new": reg["decode"]["max_new_tokens"]["short"]}
    ctx["proc"], ctx["net"] = lb.load(m, snapshot, "cuda:0")
    return ctx


def decode_one_c2(s: dict, items: list, exids: dict, out: Path, ctx: dict, ex_path: Path) -> dict:
    """decode2.decode_one (image arms) with the C-2 provenance; returns {id: caption} and the prompt shas."""
    import torch

    proc, net, m, zs, n_new = (ctx[k] for k in ("proc", "net", "m", "zs", "n_new"))
    started = lb.utc()
    texts = D2.prompts(s, items, exids, ctx["caps"], zs)
    base = lb.make_generate(proc, net, zs, n_new, lb.DATA / "datasets" / C.DATASETS[DS]["image_dir"])

    def gen(sl):
        return base(sl, [texts[i] for i, _f, _h in sl])

    kw = {"max_new_tokens": n_new, "do_sample": False, "num_beams": 1}
    tsha = {i: C.sha(t) for i, t in texts.items()}
    part = Path(str(out) + ".partial.jsonl")
    resumed = part.exists()
    rows = lb.decode_slices(items, m["batch_size"], gen, part,
                            lb.run_key(C.PINS[C.B_N1], s, m, kw, json.dumps(tsha, sort_keys=True), items))
    status = lb.git("status", "--porcelain", "--untracked-files=no")
    prov = {"schema": lb.SCHEMA, "c_schema": SCHEMA, "label": LABEL, "design": C.DESIGN,
            "design_sha256": C.PINS[C.DESIGN], "c_prereg": f"{PDIR}/PREREG.md",
            "c_prereg_sha256": sha_file(ROOT / PDIR / "PREREG.md"), "frozen_config_sha256": S2.PINS[S2.FROZEN],
            "prereg_id": "B-N1 model blocks (decoder registration)", "prereg_sha256": C.PINS[C.B_N1],
            "decoder_sha256": C.PINS["scripts/lb/decode_hf_vlm.py"], "wrapper_sha256": sha_file(Path(__file__)),
            "run_id": s["run_id"], "spec": s, "model": s["model"], "hub_id": m["hub_id"], "revision": m["revision"],
            "dataset": DS, "image_input": True, "prompt_mode": f"icl-{s['tpl']}", "prompt_text_sha256":
            C.TEMPLATE_SHA256, "prompt_sha256_per_image": tsha, "exemplars": exids,
            "manifest_sha256": C.sha(json.dumps(items)), "lists_sha256": C.LISTS_SHA256,
            "exemplars_sha256": sha_file(ex_path), "max_new_tokens": n_new, "batch_size": m["batch_size"],
            "dtype": m["dtype"], "attn_implementation": m["attn_implementation"],
            "processor_kwargs": m["processor_kwargs"], "generation_config": net.generation_config.to_diff_dict(),
            "machine_id": os.environ.get("VSPS_MACHINE_ID"), "git_head": lb.git("rev-parse", "HEAD"),
            "git_dirty": None if status is None else bool(status), "job_sha256": os.environ.get("VSPS_JOB_SHA256"),
            "venv_freeze_sha256": os.environ.get("VSPS_VENV_FREEZE_SHA256"), "packages": lb.packages(),
            "n_images": len(items), "resumed": resumed, "started_utc": started, "finished_utc": lb.utc(),
            "gpu": torch.cuda.get_device_name(0), "cuda": torch.version.cuda, "generate_kwargs": kw}
    lb.write_output(out, prov, rows)
    print(f"wrote {out.name}")
    return {r["image_id"]: r["caption"] for r in rows} | {"_prompt_sha": tsha}


def parity(model: str, ctx: dict, s2: Path, lists: dict, lists_path: Path, out_dir: Path) -> dict:
    """The frozen ret run re-decodes the first PARITY_N OV-dev-B images through this path; >= 95% captions and
    100% prompt sha256 identical to the stage-2 preds, else STOP. Counts only are written."""
    cfg = S2.frozen()
    s = {**S2.spec(cfg, DS, model, "ret")}
    rec_path = out_ok(out_dir / f"parity_{model}.json")
    if rec_path.exists():
        rec = json.loads(rec_path.read_text())
        if not rec["passed"]:
            raise SystemExit("PARITY FAILED earlier: back to the judge")
        return rec
    ref = G.read_preds(s2_run(s2, cfg, model, "ret"))
    ex_path, ex = exemplars_for({"memory_pct": 100}, s2, out_dir, lists_path)
    items = S2.manifest2(DS, lists)[:PARITY_N]
    exids = C.check_exemplars(items, s, ex, lists)
    got = decode_one_c2({**s, "run_id": f"ca_parity_{s['run_id']}"}, items, exids,
                        out_ok(out_dir / f"ca_parity_{model}.preds.json"), ctx, ex_path)
    same = sum(got[i] == ref["predictions"][i] for i, _f, _h in items)
    prompts = all(got["_prompt_sha"][i] == ref["prompt_sha256_per_image"][i] for i, _f, _h in items)
    rec = {"model": model, "n": len(items), "identical": same, "share": same / len(items),
           "prompts_identical": prompts, "passed": prompts and same / len(items) >= PARITY_MIN, "utc": lb.utc()}
    rec_path.write_text(json.dumps(rec) + "\n", encoding="utf-8")
    print(json.dumps({k: rec[k] for k in ("model", "n", "identical", "prompts_identical", "passed")}))
    if not rec["passed"]:
        raise SystemExit("PARITY FAILED: the decode path is not faithful; STOP, back to the judge")
    return rec


def cmd_decode(a) -> None:
    g = grid(S2.frozen())
    if any(r not in g for r in a.run_ids):
        raise SystemExit(f"{next(r for r in a.run_ids if r not in g)}: not a C-2 run")
    specs = [g[r] for r in a.run_ids]
    if len({s["model"] for s in specs}) != 1:
        raise SystemExit("one model per process")
    lists = C.load_lists(a.lists)
    outs = [out_ok(a.out_dir / f"{s['run_id']}.preds.json") for s in specs]
    if any(o.exists() for o in outs):
        raise SystemExit("an output exists; a run is decoded once")
    items = S2.manifest2(DS, lists)
    plan = []
    for s in specs:  # every refusal before the model loads
        ex_path, ex = exemplars_for(s, a.s2, a.out_dir, a.lists)
        plan.append((s, ex_path, C.check_exemplars(items, s, ex, lists)))
    ctx = load_ctx(specs[0]["model"], a.snapshot, lists)
    if a.parity:
        parity(specs[0]["model"], ctx, a.s2, lists, a.lists, a.out_dir)
    for (s, ex_path, exids), out in zip(plan, outs):
        decode_one_c2(s, items, exids, out, ctx, ex_path)


# ------------------------------------------------------------------------------------------------ guard (InternVL3)
def c2_runs(paths: list[Path]) -> list[dict]:
    g = grid(S2.frozen())
    runs = [G.read_preds(p) for p in paths]
    if any(r["run_id"] not in g or r.get("c_schema") != SCHEMA for r in runs):
        raise SystemExit("not C-2 outputs")
    return runs


def cmd_items(a) -> None:
    """Neighbour-only items of InternVL3's C-2 runs (guard.items, unchanged) against its stage-2 zero-shot."""
    cfg = S2.frozen()
    runs = c2_runs(a.runs)
    if {r["model"] for r in runs} != {"internvl3_8b"}:
        raise SystemExit("REFUSED: only InternVL3 (frozen tau 0.10) gets a verifier pass")
    zs = G.read_preds(s2_run(a.s2, cfg, "internvl3_8b", "zs"))
    rows = G.items(runs, zs, C.memory_captions(C.load_lists(a.lists)))
    out_ok(a.out).write_text("".join(json.dumps({**r, "generator": "internvl3_8b"}) + "\n" for r in rows),
                             encoding="utf-8")
    print(f"{len(rows)} neighbour-only items")


def cmd_verify(a) -> None:
    """Qwen3-VL-8B on the items (guard.hf_verifier / guard.fill, unchanged). The cache starts as a copy of the
    stage-2 InternVL3 cache (sha-checked), so an (image, class) item verified at stage 2 is not asked again."""
    out = out_ok(a.out)
    if not out.exists():
        shutil.copyfile(s2_file(a.s2, CACHE2), out)
    lists = C.load_lists(a.lists)
    todo = [json.loads(x) for x in Path(a.items).read_text(encoding="utf-8").splitlines() if x]
    paths = G2.item_paths(todo, DS, lists)  # refuses an item image outside the OV-dev-B manifest
    reg = C.registration()
    if lb.packages() != reg["venv"]["packages"]:
        raise SystemExit("the Qwen3-VL verifier runs in the B-N1 venv")
    verifier = G.VERIFIER["internvl3_8b"]
    lb.check_snapshot(reg["models"][verifier], a.snapshot)
    load, ask, about = G.hf_verifier(reg["models"][verifier], a.snapshot)

    def checked(path_sha):
        path, h = path_sha
        if lb.sha256_file(path) != h:
            raise SystemExit(f"{path}: sha256 differs from the manifest")
        return load(path)

    try:
        n = G.fill(out, todo, paths, (checked, ask), G.s2()["verifier_protocol"], verifier)
    except SystemExit as e:  # the Qwen3-VL answer-position stop is registered and final (PREREG §8)
        if "not the answer position" not in str(e):
            raise
        (out.parent / "VERIFIER_STOP.json").write_text(json.dumps({"stop": str(e), "utc": lb.utc()}) + "\n")
        print("REGISTERED VERIFIER STOP")
        sys.exit(3)
    mass = sorted(about.pop("yes_no_mass", []))
    Path(str(out) + ".about.json").write_text(json.dumps({**about, "yes_no_mass_median": mass[len(mass) // 2] if mass
                                                          else None, "verifier": verifier, "label": LABEL,
                                                          "new_rows": n, "packages": lb.packages()}) + "\n")


# ------------------------------------------------------------------------------------------------ score (CPU, M3)
def cmd_score(a) -> None:
    """score2.set_rows (stage-1 score_set + the stage-2 extras, unchanged) on the C-2 runs against both stage-2
    zero-shot runs; only the ca_ rows are kept (the zs and NN rows are stage 2's and already in L2)."""
    cfg = S2.frozen()
    lists = C.load_lists(a.lists)
    E4, PA, PTB = SC2.kit2(a.kit_b)
    if lb.sha256_file(E4.VNC / "VnCoreNLP-1.2.jar") != S.JAR_SHA256:
        raise SystemExit(f"{E4.VNC}/VnCoreNLP-1.2.jar is not the jar of Paper B's protocol card")
    runs = c2_runs(a.runs)
    zs_by = {m: G.read_preds(s2_run(a.s2, cfg, m, "zs")) for m in C.MODELS}
    ex2 = C.load_exemplars(s2_file(a.s2, EX2[0]), a.lists)
    ctx = {"cache": S.load_cache([a.cache]), "caps": C.memory_captions(lists), "segment": E4.rdr, "E4": E4,
           "PA": PA, "PTB": PTB, "ex": ex2, "cfg": cfg,
           "inputs": {"lists_sha256": lb.sha256_file(a.lists), "cache_sha256": {a.cache.name: sha_file(a.cache)}}}
    rows = [r for r in SC2.set_rows(DS, runs, zs_by, S2.references2(DS, lists), ctx) if r["run_id"].startswith("ca_")]
    stamp = {"label": LABEL, "c_schema": SCHEMA, "c_prereg_sha256": sha_file(ROOT / PDIR / "PREREG.md"),
             "frozen_config_sha256": S2.PINS[S2.FROZEN], "utc": lb.utc()}
    with out_ok(a.ledger).open("a", encoding="utf-8") as f:
        f.writelines(json.dumps({**r, **stamp}, ensure_ascii=False) + "\n" for r in rows)
    print(f"appended {len(rows)} rows to {a.ledger}")


# ------------------------------------------------------------------------------------------------ decide (CPU)
def tau_of(cfg: dict, m: str) -> str:
    return cfg["models"][m]["tau"]


def row_or_none(rows: list[dict], run_id: str, tau: str) -> dict | None:
    hit = [r for r in rows if r["run_id"] == run_id and r["tau"] == tau]
    return hit[0] if len(hit) == 1 else None


def ab_m(l2: list[dict], c2: list[dict], cfg: dict) -> dict:
    """P-M. Delta_m(p) = ret_p - rand_100 at the frozen tau (shared stage-2 rand, CC-126 W12); pooled = mean of the
    per-image differences over the backbones. DiD = Delta(10) - Delta(100) = ret_10 - ret_100 (identity asserted).
    M1: CI_hi(DiD) < 0; M2: DiD <= -SESOI; M3: Delta(10) <= Delta(30) <= Delta(100) (points).
    HOLDS = M1 and M2 and M3; FAILED = not M1; PARTIAL otherwise; INCOMPLETE if a run is missing. Per-backbone rows
    (and InternVL3's at tau -inf) are reported for every run that exists."""
    per, d = {}, {}
    for m in C.MODELS:
        t = tau_of(cfg, m)
        rand = DC2.get(l2, DC2.rid(cfg, DS, m, "rand"), t)
        ret = {100: DC2.get(l2, DC2.rid(cfg, DS, m, "ret"), t)}
        ret |= {p: r for p in PCTS if (r := row_or_none(c2, spec_c2(cfg, m, "ret", pct=p)["run_id"], t))}
        d[m] = {p: DC2.cider_diff(r, rand) for p, r in ret.items()}
        per[m] = {"delta": {p: S.boot(x) for p, x in d[m].items()}, "src_share": {p: r.get("src_share")
                                                                                  for p, r in ret.items()}}
        if 10 in ret:
            did = DC2.cider_diff(ret[10], ret[100])
            assert np.allclose(did, d[m][10] - d[m][100])
            per[m]["did"] = S.boot(did)
        if m == "internvl3_8b":
            rand0 = DC2.get(l2, DC2.rid(cfg, DS, m, "rand"), "-inf")
            r0 = {100: DC2.get(l2, DC2.rid(cfg, DS, m, "ret"), "-inf")}
            r0 |= {p: r for p in PCTS if (r := row_or_none(c2, spec_c2(cfg, m, "ret", pct=p)["run_id"], "-inf"))}
            per[m]["delta_tau_-inf"] = {p: S.boot(DC2.cider_diff(r, rand0)) for p, r in r0.items()}
    out = {"per_model": per}
    if any(set(d[m]) != {10, 30, 100} for m in C.MODELS):
        return out | {"outcome": "INCOMPLETE", "incomplete": "a memory-subset run is missing"}
    pooled = {p: S.boot(np.mean([d[m][p] for m in C.MODELS], axis=0)) for p in (10, 30, 100)}
    did = S.boot(np.mean([d[m][10] - d[m][100] for m in C.MODELS], axis=0))
    m1, m2 = did["hi"] < 0, did["d"] <= -SESOI
    m3 = pooled[10]["d"] <= pooled[30]["d"] <= pooled[100]["d"]
    return out | {"pooled": pooled, "did_pooled": did, "M1_ci_hi_lt_0": m1, "M2_did_le_minus_sesoi": m2,
                  "M3_monotone_points": m3, "outcome": "HOLDS" if m1 and m2 and m3 else "FAILED" if not m1
                  else "PARTIAL"}


def ab_k(l2: list[dict], c2: list[dict], cfg: dict) -> dict:
    """P-K, Qwen2.5-VL only (label: shaped by stage-A dev299 selection). Delta(k) = ret_k - rand_k at tau -inf.
    K1: Delta(2) <= Delta(4) <= Delta(8) (points); K2: Delta(8) - Delta(2) >= +SESOI; K3: its CI_lo > 0.
    HOLDS iff all three; INCOMPLETE if a Qwen k run is missing. InternVL3 rows at tau 0.10, no prediction. Every k
    whose ret and rand both exist is reported. copy4_memory is against the full memory's 4-grams (score_set)."""
    out = {}
    for m in C.MODELS:
        t, k0 = tau_of(cfg, m), cfg["models"][m]["k"]
        row = {k0: {a: DC2.get(l2, DC2.rid(cfg, DS, m, a), t) for a in ("ret", "rand")}}
        for k in K_NEW[m]:
            got = {a: row_or_none(c2, spec_c2(cfg, m, a, k=k)["run_id"], t) for a in ("ret", "rand")}
            if all(got.values()):
                row[k] = got
        row = dict(sorted(row.items()))
        d = {k: DC2.cider_diff(v["ret"], v["rand"]) for k, v in row.items()}
        out[m] = {"delta": {k: S.boot(v) for k, v in d.items()},
                  "style": {k: {a: v[a]["style"] for a in v} for k, v in row.items()},
                  "copy4_memory": {k: v["ret"]["copy4_memory"] for k, v in row.items()},
                  "verbatim_share": {k: v["ret"]["verbatim_share"] for k, v in row.items()}}
        if m != "qwen25vl_7b":
            continue
        if set(d) != {2, 4, 8}:
            out["P-K"] = {"outcome": "INCOMPLETE", "incomplete": "a Qwen k run is missing",
                          "label": "shaped by stage-A dev299 selection"}
            continue
        did = S.boot(d[8] - d[2])
        k1 = out[m]["delta"][2]["d"] <= out[m]["delta"][4]["d"] <= out[m]["delta"][8]["d"]
        out["P-K"] = {"did_8_minus_2": did, "K1_monotone_points": k1, "K2_did_ge_sesoi": did["d"] >= SESOI,
                      "K3_ci_lo_gt_0": did["lo"] > 0, "label": "shaped by stage-A dev299 selection",
                      "outcome": "HOLDS" if k1 and did["d"] >= SESOI and did["lo"] > 0 else "NOT HELD"}
    return out


def ab_tau(l2tau: list[dict], cfg: dict) -> dict:
    """P-tau on InternVL3's stage-2 ret and rand decodes (L2 rows, CPU). Delta(tau) = ret_tau - rand_tau.
    (i) Delta non-increasing over -inf, 0.00, 0.10, 0.20, 0.30, +inf (points, ties allowed); (ii) deletion cost on
    ret more negative than on rand at every finite tau: mean(ret_tau - ret_-inf) < mean(rand_tau - rand_-inf)
    (points); (iii) CI_lo(Delta(+inf)) <= 0. The -inf and 0.10 rows must equal the replay."""
    m = "internvl3_8b"
    ret, rand = ({t: DC2.get(l2tau, DC2.rid(cfg, DS, m, a), t) for t in S2.TAUS} for a in ("ret", "rand"))
    delta = {t: S.boot(DC2.cider_diff(ret[t], rand[t])) for t in S2.TAUS}
    for t, k in (("-inf", "internvl3_8b_tau_-inf"), ("0.10", "internvl3_8b")):
        if tuple(round(delta[t][x], 2) for x in ("d", "lo", "hi")) != REPLAY[k]:
            raise SystemExit(f"AB-tau: the tau {t} row differs from the replay")
    cost = {t: {a: S.boot(DC2.cider_diff(r[t], r["-inf"])) for a, r in (("ret", ret), ("rand", rand))}
            for t in TAU_FINITE}
    pts = [delta[t]["d"] for t in S2.TAUS]
    i = all(b <= a for a, b in zip(pts, pts[1:]))
    ii = all(cost[t]["ret"]["d"] < cost[t]["rand"]["d"] for t in TAU_FINITE)
    iii = delta["inf"]["lo"] <= 0
    rates = {t: {a: {k: r[t].get(k) for k in ("neighbour_only_rate", "rejected_per_image", "fallback_rate",
                                                "deleted_rate", "np", "np_sum_m")} for a, r in (("ret", ret),
                                                                                              ("rand", rand))}
             for t in S2.TAUS}
    return {"delta": delta, "cost": cost, "i_monotone": i, "ii_cost_ret_lt_rand": ii, "iii_inf_ci_lo_le_0": iii,
            "outcome": "HOLDS" if i and ii and iii else "NOT HELD", "guard_rates": rates}


def safe(fn, *a) -> dict:
    try:
        return fn(*a)
    except SystemExit as e:
        return {"outcome": "INCOMPLETE", "incomplete": str(e)}


def decide(l2: list[dict], c2: list[dict], cfg: dict, extra: dict | None = None) -> dict:
    """The registered rules (PREREG §7). A missing run makes its prediction INCOMPLETE (not judged); the rows that
    exist are still reported."""
    m, k = safe(ab_m, l2, c2, cfg), safe(ab_k, l2, c2, cfg)
    t = safe(ab_tau, [r for r in l2 if r["model"] == "internvl3_8b" and r["arm"] in ("ret", "rand")
                      and r["k"] == cfg["models"]["internvl3_8b"]["k"]], cfg)
    rz = {mm: DC2.cider_diff(DC2.get(l2, DC2.rid(cfg, DS, mm, "rand"), tau_of(cfg, mm)),
                             DC2.get(l2, DC2.rid(cfg, DS, mm, "zs"))) for mm in C.MODELS}
    style = {**{mm: S.boot(x) for mm, x in rz.items()}, "pooled": S.boot(np.mean(list(rz.values()), axis=0))}
    explains = (t.get("i_monotone") is True and t.get("ii_cost_ret_lt_rand") is True
                and m.get("outcome") in ("HOLDS", "PARTIAL"))
    return {"label": LABEL, "set": DS, "n_images": N_IMG, "AB-M": m, "AB-K": k, "AB-tau": t,
            "rand_minus_zs_100": style, "section6_explains_backbone_dependence": explains,
            "not_in_abstract": "no C-2 row enters C's abstract or contributions (CC-126 W12)", **(extra or {})}


def cmd_decide(a) -> None:
    out = out_ok(a.out)
    if out.exists():
        raise SystemExit(f"{out} exists; decide runs once (one look)")
    cfg = S2.frozen()
    want = {DC2.rid(cfg, DS, m, x) for m in C.MODELS for x in ("ret", "rand", "zs")}
    l2 = load_l2(a.l2, lambda r: r["run_id"] in want and (r["model"] == "internvl3_8b" or r["tau"] == "-inf"))
    c2 = S.latest([json.loads(x) for x in a.ledger.read_text(encoding="utf-8").splitlines() if x])
    cos = {}
    for p in (10, 30, 100):
        path = s2_file(a.s2, EX2[0]) if p == 100 else out.parent / f"ex_m{p}.json"
        if path.exists():
            ex = json.loads(path.read_text(encoding="utf-8"))["ret"][DS]
            cos[p] = float(np.mean([v[0][1] for v in ex.values()]))
    res = decide(l2, c2, cfg, {"mean_top1_cos": cos, "subsets": {p: {k: v for k, v in x.items() if k != "cids"}
                                                                 for p, x in load_subsets()["subsets"].items()},
                               "composition": load_subsets()["composition"],
                               "inputs": {"l2_sha256": L2_SHA256, "ledger_sha256": sha_file(a.ledger),
                                          "code_sha256": sha_file(Path(__file__))}})
    out.write_text(json.dumps(res, indent=1, default=str) + "\n", encoding="utf-8")
    print(json.dumps({k: res[k].get("outcome") if isinstance(res[k], dict) else res[k]
                      for k in ("AB-M", "AB-tau", "section6_explains_backbone_dependence")}, indent=1))


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def refused(fn, *args) -> bool:
    try:
        fn(*args)
    except SystemExit:
        return True
    return False


def fake_row(run_id: str, model: str, arm: str, k: int, tau: str, vals: np.ndarray) -> dict:
    return {"run_id": run_id, "dataset": DS, "model": model, "arm": arm, "k": k, "tau": tau,
            "per_image": {"ids": [f"zq{i:04d}" for i in range(len(vals))], "cider_s": vals.round(4).tolist()},
            "style": {"mean_syllables": 9.0}, "copy4_memory": 0.1, "verbatim_share": 0.0, "src_share": 0.99,
            "neighbour_only_rate": 0.1, "rejected_per_image": 0.1, "fallback_rate": 0.0, "deleted_rate": 0.1,
            "np": 50.0, "np_sum_m": 10}


def fake_ledgers(cfg: dict, gain: float = 6.0, shrink: float = 4.0, kslope: float = 2.0, tau_drop: float = 1.5,
                 n: int = 200) -> tuple[list[dict], list[dict]]:
    """Synthetic L2 (stage-2 ids, InternVL3 at every tau) and C-2 ledgers. One per-image noise e_i (mean 0) runs
    through every row, so each paired difference is exact. At the frozen tau: ret_p - ret_100 = -shrink (p = 10),
    -shrink / 2 (p = 30); Qwen Delta(k) = Delta(8) - kslope * log2(8 / k); InternVL3 Delta(tau) = gain - tau_drop * j
    for the j-th tau."""
    e = np.where(np.arange(n) % 2, 1.0, -1.0) * (np.arange(n) % 7)
    base = 50 + e
    l2, c2 = [], []
    for m in C.MODELS:
        t, k0 = tau_of(cfg, m), cfg["models"][m]["k"]
        taus = S2.TAUS if m == "internvl3_8b" else ("-inf",)
        rows = {}
        for j, tau in enumerate(taus):
            drop = tau_drop * j if m == "internvl3_8b" else 0.0
            rows[tau] = (base - 0.5 * j, base - 0.5 * j + gain - drop)
            l2.append(fake_row(DC2.rid(cfg, DS, m, "rand"), m, "rand", k0, tau, rows[tau][0]))
            l2.append(fake_row(DC2.rid(cfg, DS, m, "ret"), m, "ret", k0, tau, rows[tau][1]))
        l2.append(fake_row(DC2.rid(cfg, DS, m, "zs"), m, "zs", 0, "-inf", base - 3))
        rand0, ret0 = rows[t]
        for p, f in ((10, 1.0), (30, 0.5)):
            rid = spec_c2(cfg, m, "ret", pct=p)["run_id"]
            c2 += [fake_row(rid, m, "ret", k0, tau, rows[tau][1] - shrink * f) for tau in sorted({t, "-inf"})]
        for k in K_NEW[m]:
            ks = kslope * np.log2(k0 / k) if m == "qwen25vl_7b" else 0.0
            c2.append(fake_row(spec_c2(cfg, m, "rand", k=k)["run_id"], m, "rand", k, t, rand0 + 1))
            c2.append(fake_row(spec_c2(cfg, m, "ret", k=k)["run_id"], m, "ret", k, t, ret0 + 1 - ks))
    return l2, c2


def set_replay(rows: list[dict], cfg: dict) -> dict:
    """Selftest only: REPLAY constants equal to what rows give (decide2.gate on rows at the seen taus)."""
    g = DC2.gate(rows, cfg, DS) if any(r["arm"] == "fix" for r in rows) else None
    d = {"internvl3_8b_tau_-inf": S.boot(DC2.cider_diff(*(DC2.get(rows, DC2.rid(cfg, DS, "internvl3_8b", x), "-inf")
                                                           for x in ("ret", "rand")))),
         "internvl3_8b": S.boot(DC2.cider_diff(*(DC2.get(rows, DC2.rid(cfg, DS, "internvl3_8b", x), "0.10")
                                                  for x in ("ret", "rand"))))}
    if g:
        d |= {"pooled": g["pooled_vs_rand"], **{m: g["per_model"][m]["vs_rand"] for m in C.MODELS}}
    REPLAY.update({k: tuple(round(v[x], 2) for x in ("d", "lo", "hi")) for k, v in d.items()})
    return g


def selftest() -> None:
    cfg = S2.frozen()
    g = grid(cfg)
    assert len(g) == 12 and all(r.startswith("ca_") for r in g)
    assert sum(s["memory_pct"] != 100 for s in g.values()) == 4 and not any(s["arm"] == "fix" for s in g.values())
    assert {(s["model"], s["k"], s["arm"]) for s in g.values() if s["memory_pct"] == 100} == {
        (m, k, a) for m in C.MODELS for k in K_NEW[m] for a in ("ret", "rand")}
    assert spec_c2(cfg, "qwen25vl_7b", "ret", pct=10)["run_id"] == "ca_qwen25vl_7b_ov_dev_b-ret-k8-first-T1-m10"
    # subsets: nested, sized, deterministic, seeded, composition sums
    lists = {"memory": [{"cid": f"m{i:05d}", "members": [["openviic" if i % 3 else "ktvic", str(i), "f", "h"]]}
                        for i in range(N_CLUSTERS)]}
    a, b = make_subsets(lists), make_subsets(lists)
    sub = {p: set(v["cids"]) for p, v in a["subsets"].items()}
    assert a == b and sub["10"] < sub["30"] and [len(sub["10"]), len(sub["30"])] == list(PCTS.values())
    assert sum(a["composition"]["30"].values()) == 2457 and sum(a["composition"]["100"].values()) == N_CLUSTERS
    assert BM.seed(*SUBSET_SEED) != BM.seed("rand", DS, "x")
    old = dict(REPLAY)
    try:
        # replay on decide2's own synthetic stage-2 ledger: passes at its values, refuses C's (other) values, a
        # changed decide_ov.json value, and any archived tau row
        fl = [r for r in DC2.fake_ledger(cfg, gain=5.0) if r["dataset"] == DS]
        seen = [r for r in fl if r["model"] and replay_keep(r)]
        assert not any(r["model"] == "qwen25vl_7b" and r["tau"] != "-inf" for r in seen)
        assert refused(replay, seen, cfg, None)
        gate = set_replay(seen, cfg)
        dov = {"ov_dev_b": {"gate": json.loads(json.dumps(gate))}}
        assert replay(seen, cfg, dov)["passed"]
        dov["ov_dev_b"]["gate"]["pooled_vs_rand"]["lo"] += 1e-9
        assert refused(replay, seen, cfg, dov) and refused(replay, fl, cfg, None)
        REPLAY.clear()
        REPLAY.update(old)
        # decide: each prediction comes out both ways from the data; AB-tau needs the replay rows to match
        l2, c2 = fake_ledgers(cfg)
        t = decide(l2, c2, cfg)["AB-tau"]
        assert t["outcome"] == "INCOMPLETE" and "replay" in t["incomplete"]
        set_replay([r for r in l2 if replay_keep(r)], cfg)
        out = decide(l2, c2, cfg)
        assert out["AB-M"]["outcome"] == "HOLDS" and abs(out["AB-M"]["did_pooled"]["d"] + 4.0) < 1e-9
        assert out["AB-K"]["P-K"]["outcome"] == "HOLDS" and abs(out["AB-K"]["P-K"]["did_8_minus_2"]["d"] - 4.0) < 1e-9
        tt = out["AB-tau"]
        assert tt["i_monotone"] and tt["ii_cost_ret_lt_rand"] and tt["iii_inf_ci_lo_le_0"] and tt["outcome"] == "HOLDS"
        assert out["section6_explains_backbone_dependence"] is True
        assert decide(*fake_ledgers(cfg, shrink=1.0), cfg)["AB-M"]["outcome"] == "PARTIAL"  # detected, below SESOI
        failed = decide(*fake_ledgers(cfg, shrink=-1.0), cfg)
        assert failed["AB-M"]["outcome"] == "FAILED" and failed["section6_explains_backbone_dependence"] is False
        assert decide(*fake_ledgers(cfg, kslope=0.5), cfg)["AB-K"]["P-K"]["outcome"] == "NOT HELD"
        l2s, c2s = fake_ledgers(cfg, tau_drop=0.2)  # gain 6 - 1.0 at +inf: CI_lo > 0, so (iii) fails
        set_replay([r for r in l2s if replay_keep(r)], cfg)
        ts = decide(l2s, c2s, cfg)
        assert not ts["AB-tau"]["iii_inf_ci_lo_le_0"] and ts["AB-tau"]["outcome"] == "NOT HELD"
        assert ts["section6_explains_backbone_dependence"] is True  # (i) and (ii) hold, P-M holds
        l2r, c2r = fake_ledgers(cfg, tau_drop=-0.5)  # the gain grows with tau: (i) and (ii) fail
        set_replay([r for r in l2r if replay_keep(r)], cfg)
        tr = decide(l2r, c2r, cfg)
        assert not tr["AB-tau"]["i_monotone"] and tr["section6_explains_backbone_dependence"] is False
    finally:
        REPLAY.clear()
        REPLAY.update(old)
    # a missing C-2 row makes its ablation INCOMPLETE, never a verdict
    short = [r for r in c2 if not (r["run_id"].endswith("-m30") and r["model"] == "internvl3_8b")]
    part = decide(l2, short, cfg)
    assert part["AB-M"]["outcome"] == "INCOMPLETE" and set(part["AB-M"]["per_model"]["qwen25vl_7b"]["delta"]) == {
        10, 30, 100} and set(part["AB-M"]["per_model"]["internvl3_8b"]["delta"]) == {10, 100}
    assert set(part["AB-M"]["per_model"]["internvl3_8b"]["delta_tau_-inf"]) == {10, 100}
    noq = decide(l2, [r for r in c2 if r["run_id"] != spec_c2(cfg, "qwen25vl_7b", "rand", k=2)["run_id"]], cfg)
    assert noq["AB-K"]["P-K"]["outcome"] == "INCOMPLETE" and set(noq["AB-K"]["qwen25vl_7b"]["delta"]) == {4, 8}
    assert "pooled" in part["rand_minus_zs_100"]
    selftest_host()
    print("c2 self-test ok")


def selftest_host() -> None:
    class Raising(type(Path())):
        def exists(self, **kw):
            raise PermissionError("not traversable")

        def glob(self, *a, **kw):
            raise PermissionError("not traversable")

    env = os.environ.pop("VSPS_MACHINE_ID", None)
    try:
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            assert gpu_host(Raising(t / "mid")) is False and gpu_host(t / "missing") is False
            (t / "mid").write_text("m3\n")
            assert gpu_host(t / "mid") is True
            out = t / "outputs"
            out.mkdir()
            assert isolation(out, [], "") == ["not inside a tmux session (cen_chain.sh refuses while one exists)"]
            assert isolation(out, ["cennocaps"], "x") == ["C-EN tmux session cennocaps"]
            assert isolation(Raising(t / "nope"), [], "x") == []
            take_lock(out / "c2_ablation/RUNNING", out, [], "x")
            assert refused(take_lock, out / "c2_ablation/RUNNING", out, [], "x")
            (out / "c2_ablation/RUNNING").unlink()
            (out / "b1_scaling").mkdir()
            (out / "b1_scaling/RUNNING").write_text("b1\n")
            assert refused(take_lock, out / "c2_ablation/RUNNING", out, [], "x")
            used, mark = t / "gpu_seconds.tsv", t / "CAP_STOP"
            used.write_text("dec start 1000\ndec 50\ndec start 2000\n")
            assert used_seconds(used, now=2600) == 650  # the open start is charged to now
            used.write_text("dec start 1000\ndec start 1300\ndec 20\n")
            assert used_seconds(used, now=9999) == 320  # an unmatched start is charged to the next start
            used.unlink()
            assert left(used, mark) == HARD_S
            used.write_text(f"dec {SOFT_S - 1}\n")
            assert left(used, mark) == HARD_S - SOFT_S + 1
            used.write_text(f"dec {SOFT_S}\n")
            assert left(used, mark) == 0
            used.write_text("dec 5\n")
            mark.write_text("stop\n")
            assert left(used, mark) == 0
    finally:
        if env is not None:
            os.environ["VSPS_MACHINE_ID"] = env


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("subsets")
    p.add_argument("--lists", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    sub.add_parser("check")
    p = sub.add_parser("runs")
    p.add_argument("--ablation", choices=("M", "K"))
    p.add_argument("--model", choices=C.MODELS)
    p = sub.add_parser("guard")
    p.add_argument("--head", required=True)
    p = sub.add_parser("lock")
    p.add_argument("--path", type=Path, default=LOCK)
    p = sub.add_parser("left")
    p.add_argument("--used", type=Path, required=True)
    p.add_argument("--marker", type=Path, required=True)
    p = sub.add_parser("replay")
    for f in ("--l2", "--decide-ov", "--out"):
        p.add_argument(f, type=Path, required=True)
    p = sub.add_parser("exemplars")
    p.add_argument("--pct", type=int, choices=tuple(PCTS), required=True)
    for f in ("--lists", "--emb1", "--emb", "--out"):
        p.add_argument(f, type=Path, required=True)
    p = sub.add_parser("decode")
    p.add_argument("--run-ids", nargs="+", required=True)
    p.add_argument("--parity", action="store_true")
    for f in ("--snapshot", "--lists", "--s2", "--out-dir"):
        p.add_argument(f, type=Path, required=True)
    p = sub.add_parser("items")
    p.add_argument("--runs", type=Path, nargs="+", required=True)
    for f in ("--s2", "--lists", "--out"):
        p.add_argument(f, type=Path, required=True)
    p = sub.add_parser("verify")
    for f in ("--items", "--s2", "--lists", "--snapshot", "--out"):
        p.add_argument(f, type=Path, required=True)
    p = sub.add_parser("score")
    p.add_argument("--runs", type=Path, nargs="+", required=True)
    for f in ("--s2", "--cache", "--lists", "--kit-b", "--ledger"):
        p.add_argument(f, type=Path, required=True)
    p = sub.add_parser("decide")
    for f in ("--l2", "--ledger", "--s2", "--out"):
        p.add_argument(f, type=Path, required=True)
    a = ap.parse_args()
    if a.selftest:
        selftest()
    elif a.cmd == "subsets":
        if gpu_host():
            raise SystemExit("subsets is built on the laptop only")
        a.out.write_text(json.dumps(make_subsets(C.load_lists(a.lists)), indent=1) + "\n", encoding="utf-8")
        print(f"{sha_file(a.out)}  {a.out.name}")
    elif a.cmd == "check":
        check()
        print("c2 check ok")
    elif a.cmd == "runs":
        print(" ".join(r for r, s in grid(S2.frozen()).items() if (a.ablation in (None, s["c2_ablation"]))
                       and a.model in (None, s["model"])))
    else:
        {"guard": cmd_guard, "lock": lambda x: take_lock(x.path), "replay": cmd_replay, "exemplars": cmd_exemplars,
         "decode": cmd_decode, "items": cmd_items, "verify": cmd_verify, "score": cmd_score,
         "decide": cmd_decide, "left": lambda x: print(left(x.used, x.marker))}.get(a.cmd, lambda _x: ap.error(
             "a subcommand or --selftest is required"))(a)


if __name__ == "__main__":
    main()
