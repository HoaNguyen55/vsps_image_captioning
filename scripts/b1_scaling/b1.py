#!/usr/bin/env python3
"""Paper B, B-1 (DEV CURVE): multi-seed data-scaling curve of the P1_dev recipe on KTVIC dev300.
Prereg manuscript/prereg/2026-10-28_b1_scaling/PREREG.md (CC-126 W11, PI-1026ac Q7).

    python scripts/b1_scaling/b1.py --selftest                      CPU, synthetic data only (.venv: no kit B, no scipy)
    python scripts/b1_scaling/b1.py --selftest-kit                  CPU, kit-B smoke, java stubbed (venv-c1score)
    python scripts/b1_scaling/b1.py lists --out F                   laptop: the pinned id lists (ids only)
    python scripts/b1_scaling/b1.py check                           prereg folder and code pins
    python scripts/b1_scaling/b1.py ids --dir D                     the five ids files from the pinned lists
    python scripts/b1_scaling/b1.py sft --dir D                     the sft.jsonl pins (L3-L5 registered, L1/L2 once)
    python scripts/b1_scaling/b1.py guard --head H                  M3 only: host, idle GPU, C-EN isolation, locks
    python scripts/b1_scaling/b1.py lock --path P                   take this experiment's lock (O_EXCL)
    python scripts/b1_scaling/b1.py left --used F --marker M        seconds left under the 20 GPU-h cap, 0 = STOP
    python scripts/b1_scaling/b1.py step0 --redecode R --n2 N       >= 95% identical captions or exit 1 (counts only)
    python scripts/b1_scaling/b1.py score --dir O --kit-b K --out L CPU (venv-c1score): kit-B stripped CIDEr-D per image
    python scripts/b1_scaling/b1.py decide --ledger L --out D       CPU: the registered rules, once

Points: levels L1-L5 = 216, 433, 867, 1734, 3469 training images (nested prefixes of S5's one seeded permutation;
L3/L4 are S5's f25/f50, L5 the whole split), seeds 42, 43, 44, all retrained on M3. Primary P-B1 (S5 prereg l.61):
pooled common slope b of stripped CIDEr-D on log2(N) with seed fixed effects; image bootstrap B = 2000,
default_rng(0), one index matrix for every CI; FUND_EXTERNAL_IMAGE_DATA if CI_lo(b) > +1, CLOSE_DATA_VOLUME_LEVERS if
b < +1, INCONCLUSIVE otherwise. No caption is printed or written by this file.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]

import scaling_probe as SP  # noqa: E402  S5's subsets, fit, decide, object counts, unchanged
from rl_reward import syllables  # noqa: E402
from train_rl import read_ids, schedule  # noqa: E402

PDIR = ROOT / "manuscript/prereg/2026-10-28_b1_scaling"
LISTS = PDIR / "b1_lists.json"
LISTS_SHA256 = "c4926ed2f73068897fae17bc0093bb6b8c7de94ac82c0fbe2995dbf0af7b10c5"
LABEL = "DEV CURVE (KTVIC dev300, development split; not a test result)"
SEEDS = (42, 43, 44)
LEVELS = {f"L{j + 1}": SP.POOL_N // 2 ** (4 - j) for j in range(5)}  # 216, 433, 867, 1734, 3469
S5_IDS = {"L3": "f25", "L4": "f50"}  # the S5 subsets these levels must equal
SPLIT_SHA256 = "006080b455a553ca9cc5d3f514ad76bfbe67f444c9c145a5696de681a4be1a58"  # S5 data.f100 = the split file
SFT_PINS = {"L3": "c140600eee2729420a9b23cd9cd3877530510ac099ae000f42f8492a63496c20",
            "L4": "c350c296862c596691c2f407d14b77576c8aa586632a1804eedcd6bb60aa1c29",
            "L5": "971879742e85d710fc828fa526b735d0c0b6469b4988e3d5402a26fb1b666f16"}  # S5 JSON data.subsets / f100
S5_PREDS = {"L3": ("p1dev_s42_f25-dev300-short.preds.json",
                   "b0ecf307c42486d4558eb1a2cf97cad01aa6ab52292ee7627fd028fbbb5c6b43"),
            "L4": ("p1dev_s42_f50-dev300-short.preds.json",
                   "a394053d8823ae09c4885358facda7aabb6c998a0ec1c0ba405e0e29f8db551d"),
            "L5": ("p1dev_s42_redecode-dev300-short.preds.json",
                   "1e183383e91daf32f4683fbea2bdb09d24b7deba956343ca16ef332014cba84b")}  # S5 scaling.json points
N2_PREDS_SHA256 = "1e183383e91daf32f4683fbea2bdb09d24b7deba956343ca16ef332014cba84b"  # S5 step 0: 300/300 identical
LIMIT, FLOOR, PARITY, LENGTH_GAP = 1.0, 2.0, 0.95, 0.10
CAP_S, MIN_STEP_S = 20 * 3600, 60
RULE = ("FUND_EXTERNAL_IMAGE_DATA if CI_lo(b) > +1; CLOSE_DATA_VOLUME_LEVERS if b < +1; INCONCLUSIVE otherwise "
        "(no external-data spend)")  # S5 prereg l.61, verbatim (asserted against the S5 JSON by the selftest)
#: Amendment 3 (STOP-M4-3): kit B imports scipy, which the pinned .venv (7332d343) lacks; every kit-B step runs in
#: /root/venv-c1score at setup_gpu.sh H_C1 (numpy 2.2.6, scipy 1.15.3), as c2_job.sh does
SC_PY, SC_FREEZE = "/root/venv-c1score/bin/python", "4b81b6b6a549771115529e6900b9589835cdbfff0c6acf179aef53d283b744d5"
JOB = ROOT / "scripts/b1_scaling/b1_job.sh"
OUTCOMES = {"FUND_EXTERNAL_IMAGE_DATA": "PASS", "CLOSE_DATA_VOLUME_LEVERS": "FAIL", "INCONCLUSIVE": "INCONCLUSIVE"}
LOCK = Path("/root/outputs/b1_scaling/RUNNING")
#: fragments of the registered procedure (S5 §5 with the seed varied) that b1_job.sh must contain
JOB_FLAGS = ("build_gold_sft.py --annotations", "train_stage2.py --stage sft",
             "--epochs 2 --seed $S --loss-mask assistant", "NCS_DATASET=ktvic_dev",
             "evaluate.py --model qwen2.5-vl-7b", "--split dev_data.json --prompt short")
OUTPUTS = Path("/root/outputs")
TRAIN_SHA256 = "72ee9b57c350fb5f215e1f04701c515a51e5e415240e51a77c8ce00ce6316a0f"  # S5 sources: KTVIC train_data.json
#: KTVIC train ids 3589, 7511 = test 1335, 507 (byte twins); kept in training as in S5; CC-130 (amends CC-128 W9(b))
TRAIN_TEST_TWINS = {"00000003589.jpg": "bd5ea1bc723cbe731d0049d1e42a48055fbcff53f44157c701a8c4d690906261",
                    "00000007511.jpg": "dc1cd6988daf5ece6fdcacc0535e442387b0244512b7fbf288d75880e1738f9d"}
DEV_TWIN = "2004"  # dev300 image 2004 is byte-identical to train 4487 (L5 only): masked in the CC-130 sensitivity row
EXCL = "manuscript/prereg/2026-10-21_dev_pools/exclusion.json"  # its image_sha256.ktvic_test: the 558 test images
IMAGES = (".jpg", ".jpeg", ".png")
#: the code S5 pinned (S5 JSON code_at_head) that this job runs unchanged; the queue files are not used
S5_CODE = ("scripts/train_stage2.py", "scripts/build_gold_sft.py", "scripts/evaluate.py", "scripts/train_rl.py",
           "scripts/ktvic_dev_split.py", "scripts/rl_reward.py", "scripts/rl_report.py", "scripts/object_prf.py",
           "rescap/chair.py", "scripts/checkpoint_resume_hook.py")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def run_name(seed: int, level: str) -> str:
    return f"b1_s{seed}_{level}"


def ids_body(ids: list[str]) -> bytes:
    return ("\n".join(ids) + "\n").encode()


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


def locks(outputs: Path = OUTPUTS) -> list[str]:
    """Every /root/outputs/*/RUNNING lock (G-RL, B-1, C-2, any later one); none is visible from the laptop."""
    try:
        return sorted(str(p) for p in outputs.glob("*/RUNNING"))
    except OSError:
        return []


def cen_sessions(names: list[str] | None = None) -> list[str]:
    """tmux sessions of C-EN (cen_chain.sh names them cen<step>)."""
    if names is None:
        r = subprocess.run(["tmux", "ls", "-F", "#S"], capture_output=True, text=True)
        names = r.stdout.split() if r.returncode == 0 else []
    return [n for n in names if n.startswith("cen")]


def isolation(outputs: Path = OUTPUTS, names: list[str] | None = None, tmux: str | None = None) -> list[str]:
    """Reasons this job may not start: outside tmux, a C-EN tmux session, or any experiment lock."""
    tmux = os.environ.get("TMUX", "") if tmux is None else tmux
    bad = [] if tmux else ["not inside a tmux session (cen_chain.sh refuses while one exists)"]
    bad += [f"C-EN tmux session {n}" for n in cen_sessions(names)]
    return bad + [f"lock {p} exists" for p in locks(outputs)]


def take_lock(path: Path, outputs: Path = OUTPUTS, names: list[str] | None = None, tmux: str | None = None) -> None:
    bad = isolation(outputs, names, tmux)
    if bad:
        raise SystemExit("REFUSED: " + "; ".join(bad))
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)  # a race with another job fails here, never overwrites
    os.write(fd, f"{sys.argv[0]} pid {os.getppid()}\n".encode())
    os.close(fd)


def twin_ok(p: Path, h: str, data: Path) -> bool:
    """CC-130: a test-sha file is exempt only as a named train twin, at its name, under data/ktvic/images."""
    return p.parent == data / "ktvic/images" and TRAIN_TEST_TWINS.get(p.name) == h


def ktvic_test_files(data: Path, test_sha: set[str]) -> list[str]:
    """Files under data/ktvic*/ named test*, or images whose sha256 is a KTVIC test image's (exclusion.json), except
    the two named train twins (TRAIN_TEST_TWINS) at their names under data/ktvic/images."""
    out = []
    for d in sorted(data.glob("ktvic*")):
        for p in sorted(d.rglob("*")):
            if not p.is_file():
                continue
            h = SP.sha256(p) if p.suffix.lower() in IMAGES else None
            if p.name.startswith("test") or (h in test_sha and not twin_ok(p, h, data)):
                out.append(str(p))
    return out


def cmd_guard(a) -> None:
    """M3 or M4 (PI-1026ai), idle GPU, committed HEAD and a clean tree (grl common.host_ok); on M3 common.m3_clear,
    on M4 no cen_ set staged and no C-EN process; no KTVIC test file or image under $NCS_DATA/datasets (the two
    named twins excepted), and isolation() minus this job's lock."""
    sys.path.insert(0, str(ROOT / "scripts/grl"))
    import common as K

    mid = K.host_ok(a.head)
    if mid == "m3":
        K.m3_clear()
    elif mid == "m4":  # PI-1026ai: dev-only M4 holds no C-EN data; still no cen_ set staged and no C-EN process
        staged = [s for s in K.CEN_TEST_SIDE if (K.NCS_DATA / "datasets" / f"cen_{s}").exists()]
        busy = subprocess.run(["pgrep", "-f", "scripts/c_en/"], capture_output=True, text=True).stdout.split()
        if staged or busy:
            raise SystemExit(f"REFUSED: C-EN trace on M4: staged {staged}, processes {busy}")
    else:
        raise SystemExit("REFUSED: B-1 runs on M3 or M4 only (PI-1026ac Q7, PI-1026ai)")
    excl = json.loads(K.pinned(EXCL).read_text(encoding="utf-8"))["image_sha256"]["ktvic_test"]
    test = ktvic_test_files(SP.DATA / "datasets", set(excl))
    others = [x for x in isolation() if x != f"lock {LOCK} exists"]
    if test or others:
        raise SystemExit(f"REFUSED: {test or others}")
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


def left(used: Path, marker: Path, cap_s: int = CAP_S) -> int:
    """Seconds left under the cap (sum of the second column of `used`); 0 once the CAP_STOP marker exists or fewer
    than MIN_STEP_S remain. A cap stop is final: no GPU step starts after it."""
    if marker.exists():
        return 0
    s = used_seconds(used)
    rest = int(cap_s - s)
    return rest if rest >= MIN_STEP_S else 0


# ------------------------------------------------------------------------------------------------ lists, pins
def make_lists() -> dict:
    """The five nested levels from S5's rule (train_rl.schedule(pool, 3469, 42) prefixes); L3/L4 equal S5's
    registered f25/f50 ids, L5 is the split file itself (its build reproduces the n2 gold_p1dev, S5 sources)."""
    if gpu_host():
        raise SystemExit("lists is built on the laptop only")
    pool = read_ids(ROOT / SP.POOL)
    order, dev = schedule(pool, len(pool), SP.SEED), set(read_ids(ROOT / SP.DEV))
    s5 = json.loads(SP.PREREG.read_text(encoding="utf-8"))["data"]["subsets"]
    levels = {}
    for lv, n in LEVELS.items():
        ids = pool if lv == "L5" else order[:n]
        body = (ROOT / SP.POOL).read_bytes() if lv == "L5" else ids_body(ids)
        if len(ids) != n or dev & set(ids):
            raise SystemExit(f"{lv}: wrong size or holds dev300 images")
        if lv in S5_IDS and (ids != s5[S5_IDS[lv]]["ids"] or sha_bytes(body) != s5[S5_IDS[lv]]["ids_sha256"]):
            raise SystemExit(f"{lv}: not S5's {S5_IDS[lv]}")
        if lv == "L5" and sha_bytes(body) != SPLIT_SHA256:
            raise SystemExit("L5: not the split file")
        levels[lv] = {"n": n, "file": f"ktvic_train_minus_dev300_{lv}_s42.txt", "ids_sha256": sha_bytes(body),
                      "ids": ids}
    for a, b in zip(list(levels)[:-1], list(levels)[1:]):
        if not set(levels[a]["ids"]) < set(levels[b]["ids"]):
            raise SystemExit(f"{a} is not nested in {b}")
    return {"label": LABEL, "rule": f"prefixes of train_rl.schedule(ids of {SP.POOL}, {SP.POOL_N}, {SP.SEED}); sizes "
            f"{SP.POOL_N} // 2**(5 - j), j = 1..5; L5 = the split file", "pool_sha256": SPLIT_SHA256,
            "s5_prereg_sha256": SP.PREREG_SHA256[SP.PREREG], "levels": levels}


def load_kit(kit_b: Path):
    """(protocol_pilot, punctuation_audit) of kit B through c_stage1's sha-pinned loader, and the protocol-card jar."""
    sys.path.insert(0, str(ROOT / "scripts/c_stage1"))
    import score as S1  # c_stage1's kit-B loader, unchanged

    E4, PA = S1.kit(kit_b)
    if SP.sha256(E4.VNC / "VnCoreNLP-1.2.jar") != S1.JAR_SHA256:
        raise SystemExit("VnCoreNLP jar is not Paper B's protocol-card jar")
    return E4, PA, {f: SP.sha256(Path(kit_b) / f) for f in S1.KIT_B}


def kit_smoke(E4, PA) -> float:
    """CC-128 W5: RDRSegmenter (java) and Cider run on one synthetic pair before any GPU step; returns its score."""
    texts = ["zq7 vx2 kp9 lm3 .", "bw4 hn8 dc6 yt1 .", "zq7 vx2 kp9 rt5", "bw4 hn8 qq2 yt1"]
    seg = [x.lower() for x in E4.rdr(texts)]
    got = E4.Cider({"zq0": [seg[0]], "zq1": [seg[1]]}).per_image(
        {f"zq{j}": " ".join(PA.strip_trailing_punct_tokens(seg[2 + j].split())) for j in range(2)})
    if len(got) != 2 or not np.all(np.isfinite(got)) or got.min() <= 0:
        raise SystemExit(f"kit B smoke failed: {got}")
    return float(got.min())


def check(machine: bool = False, job: Path | None = None, kit_b: Path | None = None) -> dict:
    """The prereg folder's SHA256SUMS (every line), the lists at their pin, S5's pinned code unchanged; machine: the
    base snapshot (S5's shard sha256, HF_HUB_OFFLINE=1), the n2 p1dev_s42 adapter for Step 0 and KTVIC
    train_data.json; job: the job file carries the registered procedure and no unregistered flag (S5's
    JOB_FORBIDDEN, which holds the test split); kit_b: the scorer loads (before any GPU step)."""
    for line in (PDIR / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        h, name = line.split(maxsplit=1)
        if SP.sha256(PDIR / name) != h:
            raise SystemExit(f"{name}: differs from the prereg SHA256SUMS")
    if SP.sha256(LISTS) != LISTS_SHA256:
        raise SystemExit("b1_lists.json differs from its pin")
    SP.verify(SP.PREREG_SHA256)
    P = json.loads(SP.PREREG.read_text(encoding="utf-8"))
    SP.verify({ROOT / f: P["code_at_head"][f] for f in S5_CODE})
    if machine:
        f100 = P["models"]["f100"]
        run = SP.DATA / "runs" / f100["adapter"]
        SP.verify(SP.base_snapshot(P["models"]["base"]) | {run / "adapter_model.safetensors": f100["adapter_sha256"],
                                                            SP.DATA / "datasets/ktvic/train_data.json": TRAIN_SHA256})
    if kit_b is not None:
        kit_smoke(*load_kit(kit_b)[:2])
    if job is not None:
        text = job.read_text(encoding="utf-8")
        missing = [f for f in JOB_FLAGS if f not in text]
        forbidden = [f for f in SP.JOB_FORBIDDEN if f in text]
        if missing or forbidden:
            raise SystemExit(f"{job.name}: registered fragments missing {missing}, unregistered flags {forbidden}")
    return json.loads(LISTS.read_text(encoding="utf-8"))


def write_ids(L: dict, d: Path) -> None:
    d.mkdir(parents=True, exist_ok=True)
    for lv, x in L["levels"].items():
        body = (ROOT / SP.POOL).read_bytes() if lv == "L5" else ids_body(x["ids"])
        if sha_bytes(body) != x["ids_sha256"]:
            raise SystemExit(f"{lv}: ids differ from the pinned list")
        SP.write_once(d / x["file"], body)


def check_sft(d: Path) -> dict:
    """sft.jsonl of each level built by build_gold_sft.py --images-file: L3-L5 must equal S5's registered sha256;
    L1/L2 are recorded once (sft_L1_L2.sha256, write-once, before any training) and must stay equal."""
    got = {lv: SP.sha256(d / f"gold_b1_{lv}/sft.jsonl") for lv in LEVELS}
    bad = {lv: got[lv] for lv, h in SFT_PINS.items() if got[lv] != h}
    if bad:
        raise SystemExit(f"sft.jsonl differs from S5's registered sha256: {bad}")
    SP.write_once(d / "sft_L1_L2.sha256", "".join(f"{got[lv]}  gold_b1_{lv}/sft.jsonl\n" for lv in ("L1", "L2"))
                  .encode())
    return got


def step0(redecode: Path, n2: Path) -> dict:
    """Step 0: p1dev_s42 re-decoded on M3 against the registered n2 decode; counts only."""
    if SP.sha256(n2) != N2_PREDS_SHA256:
        raise SystemExit(f"{n2}: not the registered n2 dev300 preds")
    a, b = SP.rl_report._preds(str(redecode)), SP.rl_report._preds(str(n2))
    if sorted(a) != sorted(b) or len(a) != SP.DEV_N:
        raise SystemExit("step 0: not the same 300 dev images")
    same = sum(a[i] == b[i] for i in a)
    rec = {"identical": same, "n": len(a), "share": same / len(a), "passed": same / len(a) >= PARITY}
    print(json.dumps(rec))
    return rec


# ------------------------------------------------------------------------------------------------ score (M3, CPU)
def dev_preds(result: Path) -> dict[str, str]:
    """An evaluate.py dev300 short-prompt result's predictions (never a test split)."""
    res = json.loads(result.read_text(encoding="utf-8"))
    if (res["split"], res["prompt_style"], res["n_images"]) != ("dev_data.json", "short", SP.DEV_N):
        raise SystemExit(f"{result.name}: not a short-prompt dev300 decode")
    return SP.rl_report._preds(str(result.with_suffix(".preds.json")))


def plan(o: Path) -> dict[str, dict]:
    """Every scored file: 15 points, the zero-shot point, S5's three preds (look at existing dev preds)."""
    out = {run_name(s, lv): {"kind": "point", "seed": s, "level": lv, "N": n,
                             "result": o / f"{run_name(s, lv)}-dev300-short.json"}
           for s in SEEDS for lv, n in LEVELS.items()}
    out["b1_zeroshot"] = {"kind": "zeroshot", "N": 0, "result": o / "b1_zeroshot-dev300-short.json"}
    for lv, (f, h) in S5_PREDS.items():
        out[f"s5_{lv}"] = {"kind": "s5", "seed": 42, "level": lv, "N": LEVELS[lv], "preds": o / "s5_preds" / f,
                           "sha256": h}
    return out


def score_rows(preds: dict[str, dict[str, str]], gt: dict[str, list[str]], E4, PA) -> dict[str, dict]:
    """Per file: per-image CIDEr-D as written and with its final punctuation stripped (kit B, RDRSegmenter, df from
    the dev300 references), object rows and CHAIR counts (scaling_probe.object_counts), mean syllables."""
    ids = sorted(gt)
    texts = sorted({c for p in preds.values() for c in p.values()} | {r for rs in gt.values() for r in rs})
    seg = dict(zip(texts, (s.lower() for s in E4.rdr(texts))))
    cider = E4.Cider({i: [seg[x] for x in gt[i]] for i in ids})
    out = {}
    for name, p in preds.items():
        if sorted(p) != ids:
            raise SystemExit(f"{name}: not the dev300 images")
        s = cider.per_image({i: " ".join(PA.strip_trailing_punct_tokens(seg[p[i]].split())) for i in ids})
        w = cider.per_image({i: seg[p[i]] for i in ids})
        oc = SP.object_counts(p, gt)
        out[name] = {"ids": ids, "cider_s": s.round(4).tolist(), "cider_w_mean": float(w.mean()),
                     "obj_rows": [list(r) for r in oc["rows"]], "mentions": oc["mentions"].tolist(),
                     "halluc": oc["halluc"].tolist(),
                     "mean_syllables": float(np.mean([len(syllables(p[i])) for i in ids]))}
    return out


def cmd_score(a) -> None:
    if a.out.exists():
        raise SystemExit(f"{a.out} exists; scoring runs once")
    E4, PA, kit_sha = load_kit(a.kit_b)
    pl, preds = plan(a.dir), {}
    for name, x in pl.items():
        if x["kind"] == "s5":
            if SP.sha256(x["preds"]) != x["sha256"]:
                raise SystemExit(f"{x['preds']}: not S5's preds")
            preds[name] = SP.rl_report._preds(str(x["preds"]))
        elif x["result"].exists():
            preds[name] = dev_preds(x["result"])
    rows = score_rows(preds, SP.dev_refs(), E4, PA)
    meta = {k: {kk: str(vv) for kk, vv in v.items()} for k, v in pl.items()}
    a.out.write_text(json.dumps({"label": LABEL, "plan": meta, "rows": rows, "kit_b": kit_sha}) + "\n",
                     encoding="utf-8")
    print(f"scored {len(rows)} of {len(pl)} files")


# ------------------------------------------------------------------------------------------------ decide (CPU)
def fe_slope(x: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """Common slope with seed fixed effects on a balanced grid: Y (S, L, ...) over the same x (L,) for every seed;
    equals the mean of the per-seed OLS slopes."""
    xc = x - x.mean()
    return np.tensordot(xc, Y - Y.mean(1, keepdims=True), axes=([0], [1])).mean(0) / (xc @ xc)


def seed_slopes(x: np.ndarray, Y: np.ndarray) -> np.ndarray:
    xc = x - x.mean()
    return np.tensordot(xc, Y - Y.mean(1, keepdims=True), axes=([0], [1])) / (xc @ xc)


def fe_quad(x: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """c of y = a_s + b x + c x^2 (seed fixed effects), Y (S, L, ...): OLS on the within-seed demeaned design."""
    X = np.stack([x - x.mean(), x ** 2 - (x ** 2).mean()], 1)
    Yc = Y - Y.mean(1, keepdims=True)
    pinv = np.linalg.pinv(np.concatenate([X] * Y.shape[0]))
    flat = Yc.reshape(Y.shape[0] * Y.shape[1], -1)
    return (pinv @ flat)[1].reshape(Y.shape[2:])


def ci(draws: np.ndarray) -> list[float]:
    return [float(x) for x in np.percentile(draws, [2.5, 97.5])]


def decide(led: dict, draws: int = SP.B) -> dict:
    """The registered rules on the scored ledger (§7). Seeds with all five levels enter the fit; P-B1 has a verdict
    only with >= 2 complete seeds. The zero-shot and S5 rows never enter the fit."""
    rows = led["rows"]
    n = SP.DEV_N
    idx = np.random.default_rng(SP.BOOT_SEED).integers(0, n, (draws, n))  # registered: draws = SP.B = 2000
    x = np.log2(list(LEVELS.values()))
    complete = [s for s in SEEDS if all(run_name(s, lv) in rows for lv in LEVELS)]
    cid = {k: np.array(v["cider_s"], float) for k, v in rows.items()}
    point = {k: float(v.mean()) for k, v in cid.items()}
    out = {"label": LABEL, "complete_seeds": complete, "points": {k: {"cider_s": point[k], "cider_w": v["cider_w_mean"],
           "mean_syllables": v["mean_syllables"]} for k, v in rows.items()},
           "bootstrap": {"B": draws, "rng": f"numpy default_rng({SP.BOOT_SEED})", "n_images": n,
                         "paired": "one index matrix for every point and every CI"}}
    if "b1_zeroshot" in rows:
        out["zeroshot"] = {"cider_s": point["b1_zeroshot"], "use": "plotted, not fitted"}
    if len(complete) < 2:
        out["P-B1"] = {"verdict": "NO VERDICT", "why": f"{len(complete)} complete seed(s); the rule needs >= 2"}
    else:
        Y = np.array([[point[run_name(s, lv)] for lv in LEVELS] for s in complete])
        D = np.array([[cid[run_name(s, lv)][idx].mean(1) for lv in LEVELS] for s in complete])  # (S, L, B)
        b, bd = float(fe_slope(x, Y)), fe_slope(x, D)
        lo, hi = ci(bd)
        v = SP.decide(b, lo)
        bs, bsd = seed_slopes(x, Y), seed_slopes(x, D)
        tq = {1: 12.706, 2: 4.303}.get(len(bs) - 1)  # two-sided 95% t quantiles for df = 1, 2
        top = Y[:, 4] - Y[:, 3]
        out["P-B1"] = {"b": b, "ci95": [lo, hi], "outcome": v, "verdict": OUTCOMES[v], "rule": RULE,
                       "proposal_use": {"floor": FLOOR, "met": OUTCOMES[v] == "PASS" and b >= FLOOR,
                                        "note": "floor set after S5's +9.40 was seen; it is not the primary rule"}}
        out["P-B1-seed"] = {"b_s": dict(zip(map(str, complete), bs.tolist())), "min": float(bs.min()),
                            "max": float(bs.max()), "stable": bool(bs.min() > LIMIT),
                            "b_s_ci95": {str(s): ci(d) for s, d in zip(complete, bsd)},
                            "t_interval_95": [float(bs.mean() - tq * bs.std(ddof=1) / np.sqrt(len(bs))),
                                              float(bs.mean() + tq * bs.std(ddof=1) / np.sqrt(len(bs)))]}
        out["curvature"] = {"c": float(fe_quad(x, Y[..., None])[0]), "ci95": ci(fe_quad(x, D)),
                            "b_top_L4_L5": float(top.mean()), "b_top_ci95": ci((D[:, 4] - D[:, 3]).mean(0))}
        out["length"] = {str(s): {"rel_gap_L1_L5": g, "not_separated_from_length": g > LENGTH_GAP} for s, g in (
            (s, abs(rows[run_name(s, "L1")]["mean_syllables"] - rows[run_name(s, "L5")]["mean_syllables"])
             / rows[run_name(s, "L5")]["mean_syllables"]) for s in complete)}
        out["objects"] = objects(rows, complete, x, idx)
    out["replication"] = replication(cid, point, idx)
    out["sensitivity_minus_dev_twin"] = sensitivity(rows, cid, complete, x, idx)
    return out


def sensitivity(rows: dict, cid: dict, complete: list[int], x: np.ndarray, idx: np.ndarray) -> dict:
    """CC-130 W5, registered, descriptive (no rule, no verdict): dev300 minus image 2004 (byte twin of L5 train image
    4487). Each point mean is over the other 299 images; each bootstrap replicate is the registered index matrix row
    with the draws of image 2004 dropped. The same mask on the two replication rows."""
    ids = {tuple(v["ids"]) for v in rows.values() if "ids" in v}
    if len(ids) != 1 or DEV_TWIN not in next(iter(ids)):
        return {"computable": False, "why": "the rows do not carry one common id list holding image 2004"}
    j = list(next(iter(ids))).index(DEV_TWIN)
    keep, M = np.arange(SP.DEV_N) != j, idx != j
    point = {k: float(v[keep].mean()) for k, v in cid.items()}
    out = {"label": "dev300 minus image 2004 (byte twin of L5 train image 4487; CC-130)", "n_images": int(keep.sum()),
           "use": "descriptive; no rule, no verdict"}
    if len(complete) >= 2:
        Y = np.array([[point[run_name(s, lv)] for lv in LEVELS] for s in complete])
        D = np.array([[(cid[run_name(s, lv)][idx] * M).sum(1) / M.sum(1) for lv in LEVELS] for s in complete])
        b, (lo, hi) = float(fe_slope(x, Y)), ci(fe_slope(x, D))
        out["pooled"] = {"b": b, "ci95": [lo, hi], "s5_rule_applied_descriptively": OUTCOMES[SP.decide(b, lo)]}
    out["replication"] = replication(cid, point, idx, M)
    return out


def objects(rows: dict, complete: list[int], x: np.ndarray, idx: np.ndarray) -> dict:
    """F1 (exact classes) and CHAIR_i slopes, pooled with seed fixed effects, image CIs; reported, never gating."""
    full, draws = {}, {}
    for s in complete:
        for lv in LEVELS:
            r = rows[run_name(s, lv)]
            m = {"rows": [tuple(o) for o in r["obj_rows"]], "mentions": np.array(r["mentions"]),
                 "halluc": np.array(r["halluc"]), "cider": np.zeros(len(r["mentions"]))}
            full[s, lv], draws[s, lv] = SP.corpus(m, np.arange(SP.DEV_N)[None]), SP.corpus(m, idx)
    out = {}
    for k in ("F1", "CHAIR_i"):
        Y = np.array([[full[s, lv][k][0] for lv in LEVELS] for s in complete])
        D = np.array([[draws[s, lv][k] for lv in LEVELS] for s in complete])
        out[k] = {"b": float(fe_slope(x, Y)), "ci95": ci(fe_slope(x, D))}
    out["F1"]["s5_prediction_hit"] = bool(SP.PRED["F1"][0] <= out["F1"]["b"] <= SP.PRED["F1"][1])
    return out


def replication(cid: dict, point: dict, idx: np.ndarray, M: np.ndarray | None = None) -> dict:
    """Descriptive: S5's three preds re-scored with kit B (a look at existing dev preds) and the new seed-42 L3-L5
    slope, each with its image CI from the same index matrix. No rule."""
    x3 = np.log2([LEVELS[lv] for lv in ("L3", "L4", "L5")])
    out = {}
    for tag, names in (("s5_rescored_kit_b", [f"s5_{lv}" for lv in ("L3", "L4", "L5")]),
                       ("m3_seed42_L3_L5", [run_name(42, lv) for lv in ("L3", "L4", "L5")])):
        if all(k in cid for k in names):
            b = float(SP.ols(x3, [point[k] for k in names])[1])
            draws = SP.ols(x3, np.stack([cid[k][idx].mean(1) if M is None else (cid[k][idx] * M).sum(1) / M.sum(1)
                                         for k in names]))[1]
            out[tag] = {"b": b, "ci95": ci(draws)}
    return out


def cmd_decide(a) -> None:
    if a.out.exists():
        raise SystemExit(f"{a.out} exists; decide runs once")
    led = json.loads(a.ledger.read_text(encoding="utf-8"))
    res = decide(led) | {"ledger_sha256": SP.sha256(a.ledger), "code_sha256": SP.sha256(Path(__file__))}
    a.out.write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: res.get(k) for k in ("label", "complete_seeds", "P-B1")}, indent=1))


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def refused(fn, *args) -> bool:
    try:
        fn(*args)
    except SystemExit:
        return True
    return False


def fake_ledger(slope: float, spread: float, seeds=SEEDS, seed_shift=(0.0, 1.0, -1.0)) -> dict:
    """Synthetic per-image CIDEr-D: c_i + slope * log2(N) + shift_s + d_i (L - 3), d alternating +-spread (mean 0,
    so every seed's full-sample slope is exactly slope); one object row and CHAIR counts per point."""
    x = dict(zip(LEVELS, np.log2(list(LEVELS.values()))))
    c = 100 + 3 * (np.arange(SP.DEV_N) % 5)
    d = spread * np.where(np.arange(SP.DEV_N) % 2, -1, 1)
    rows = {}
    for s, sh in zip(seeds, seed_shift):
        for j, lv in enumerate(LEVELS):
            rows[run_name(s, lv)] = {"cider_s": (c + slope * x[lv] + sh + d * (j - 2)).tolist(), "cider_w_mean": 0.0,
                                     "obj_rows": [[j + 1, j + 2, j + 1, 0.5, 0.5, 0.5]] * SP.DEV_N,
                                     "mentions": [3] * SP.DEV_N, "halluc": [j % 2] * SP.DEV_N,
                                     "mean_syllables": 10.0 + 0.1 * j}
    rows["b1_zeroshot"] = {**rows[run_name(seeds[0], "L1")], "cider_s": [5.0] * SP.DEV_N}
    ids = sorted([DEV_TWIN] + [f"zq{i:03d}" for i in range(SP.DEV_N - 1)])
    for r in rows.values():
        r["ids"] = ids
    return {"rows": rows}


def selftest() -> None:
    def decide(led, draws=200):  # selftest speed only; the registered B = 2000 is checked once below
        return globals()["decide"](led, draws)

    # the fixed-effects slope equals an explicit seed-dummy regression and the mean of per-seed slopes
    rng = np.random.default_rng(1)
    x = np.log2(list(LEVELS.values()))
    Y = rng.normal(size=(3, 5)) + np.array([[1.5], [2.5], [0.5]]) * x
    X = np.column_stack([np.tile(x, 3), np.kron(np.eye(3), np.ones((5, 1)))])
    beta = np.linalg.lstsq(X, Y.reshape(-1), rcond=None)[0]
    assert np.isclose(fe_slope(x, Y), beta[0]) and np.isclose(fe_slope(x, Y), seed_slopes(x, Y).mean())
    Xq = np.column_stack([np.tile(x, 3), np.tile(x ** 2, 3), np.kron(np.eye(3), np.ones((5, 1)))])
    assert np.isclose(fe_quad(x, Y[..., None])[0], np.linalg.lstsq(Xq, Y.reshape(-1), rcond=None)[0][1])
    # sizes and the S5 rule's three outcomes, its clause order, the floor and the seed secondary
    assert list(LEVELS.values()) == [216, 433, 867, 1734, 3469]
    assert json.loads(SP.PREREG.read_text(encoding="utf-8"))["decision_rule"]["rule"] == RULE
    seen = set()
    for slope, spread, want in ((3, 1, "PASS"), (0.5, 1, "FAIL"), (1.5, 40, "INCONCLUSIVE")):
        out = decide(fake_ledger(slope, spread))
        p = out["P-B1"]
        assert abs(p["b"] - slope) < 1e-9 and p["verdict"] == want, (slope, spread, p)
        assert p["proposal_use"]["met"] == (want == "PASS" and slope >= FLOOR)
        assert out["P-B1-seed"]["stable"] == (slope > LIMIT) and json.dumps(out) == json.dumps(
            decide(fake_ledger(slope, spread)))
        seen.add(p["verdict"])
    assert seen == set(OUTCOMES.values())
    assert decide(fake_ledger(1.5, 1))["P-B1"]["proposal_use"]["met"] is False  # PASS below the floor
    assert SP.decide(0.5, 1.5) == "FUND_EXTERNAL_IMAGE_DATA" and SP.decide(5, 0.9) == "INCONCLUSIVE"
    # CC-130 W5: the dev-twin row masks exactly image 2004
    led = fake_ledger(3, 1)
    j = led["rows"][run_name(42, "L1")]["ids"].index(DEV_TWIN)
    for s_ in SEEDS:
        led["rows"][run_name(s_, "L5")]["cider_s"][j] += 600.0  # image 2004 jumps at L5 only
    out = decide(led)
    sv = out["sensitivity_minus_dev_twin"]
    keep = np.arange(SP.DEV_N) != j
    Y = np.array([[np.mean(np.array(led["rows"][run_name(s_, lv)]["cider_s"])[keep]) for lv in LEVELS] for s_ in SEEDS])
    assert sv["n_images"] == 299 and abs(sv["pooled"]["b"] - fe_slope(np.log2(list(LEVELS.values())), Y)) < 1e-9
    assert sv["pooled"]["b"] < out["P-B1"]["b"] - 0.3  # image 2004 masked: +2 on the L5 mean, ~+0.4 on b
    assert "m3_seed42_L3_L5" in sv["replication"]
    # zero-shot is plotted, never fitted; an incomplete seed leaves the fit; < 2 complete seeds = no verdict
    led = fake_ledger(3, 1)
    b0 = decide(led)["P-B1"]["b"]
    led["rows"]["b1_zeroshot"]["cider_s"] = [500.0] * SP.DEV_N
    assert decide(led)["P-B1"]["b"] == b0 and decide(led)["zeroshot"]["use"] == "plotted, not fitted"
    del led["rows"][run_name(44, "L5")]
    out = decide(led)
    assert out["complete_seeds"] == [42, 43] and abs(out["P-B1"]["b"] - 3) < 1e-9
    del led["rows"][run_name(43, "L1")]
    assert decide(led)["P-B1"]["verdict"] == "NO VERDICT"
    # curvature: a pure quadratic is detected, a line has c = 0
    q = fake_ledger(0, 0)
    for k, r in q["rows"].items():
        if k.startswith("b1_s"):
            lv = k.split("_")[-1]
            r["cider_s"] = (np.array(r["cider_s"]) + 0.5 * np.log2(LEVELS[lv]) ** 2).tolist()
    assert abs(decide(q)["curvature"]["c"] - 0.5) < 1e-9 and abs(decide(fake_ledger(2, 1))["curvature"]["c"]) < 1e-9
    # objects: slopes are finite and the F1 prediction hit is a bool
    o = decide(fake_ledger(2, 1))["objects"]
    assert np.isfinite(o["F1"]["b"]) and np.isfinite(o["CHAIR_i"]["b"])
    assert isinstance(o["F1"]["s5_prediction_hit"], bool)
    # replication rows: the same index matrix gives the same CI on the same data
    rep = {f"s5_{lv}": np.full(SP.DEV_N, 10.0 * j) for j, lv in enumerate(("L3", "L4", "L5"))}
    r = replication(rep, {k: float(v.mean()) for k, v in rep.items()}, np.zeros((4, SP.DEV_N), int))
    assert abs(r["s5_rescored_kit_b"]["b"] - 10.0) < 0.01  # log2 steps of 867, 1734, 3469 are ~1
    full = globals()["decide"](fake_ledger(3, 1))
    assert full["bootstrap"]["B"] == SP.B == 2000 and full["P-B1"]["verdict"] == "PASS"
    selftest_host()
    job_venvs(JOB.read_text(encoding="utf-8"))
    # STOP-M4-3: this core selftest runs in .venv, which has no scipy; kit B (scipy) is --selftest-kit's, in $SC
    assert "scipy" not in sys.modules and "protocol_pilot" not in sys.modules, "core selftest loaded kit B / scipy"
    print("b1 self-test ok")


def job_venvs(text: str) -> None:
    """Amendment 3: every kit-B step of the job (check --kit-b, --selftest-kit, score) runs under $SC, the scoring
    venv, after its freeze check; the core selftest, check --machine and the GPU steps stay in .venv."""
    lines = [x.strip() for x in text.splitlines() if not x.lstrip().startswith("#")]
    assert f"SC={SC_PY}" in text and f"SC_FREEZE={SC_FREEZE}" in text
    fz = next((j for j, x in enumerate(lines) if '"$(/root/venv-c1score/bin/pip freeze' in x and "$SC_FREEZE" in x), -1)
    assert fz >= 0, "no scoring-venv freeze check in the job"
    kit = [j for j, x in enumerate(lines) if "$B1" in x and any(k in x for k in ("--kit-b", "--selftest-kit", " score "))]
    assert len(kit) >= 3 and all("$SC $B1" in lines[j] and "python $B1" not in lines[j] and j > fz for j in kit), kit
    assert any("python $B1 --selftest " in x for x in lines)  # the core selftest, in .venv


def selftest_kit() -> None:
    """kit-B smoke on the pinned kit's Cider and stripper, with the java segmenter stubbed (the job runs the real one
    in check --kit-b), then score_rows on synthetic text; venv-c1score only (kit B imports scipy)."""
    sys.path.insert(0, str(ROOT / "scripts/c_stage1"))
    import score as S1

    E4, PA = S1.kit(ROOT / "scripts/kit_b")

    class Stub:
        Cider = E4.Cider

        @staticmethod
        def rdr(texts):
            return list(texts)

    assert kit_smoke(Stub, PA) > 0
    gt = {"zq0": ["zq7 vx2 kp9 lm3 .", "zq7 vx2 kp9 ."], "zq1": ["bw4 hn8 dc6 yt1 .", "bw4 hn8 ."]}
    rows = score_rows({"p": {"zq0": "zq7 vx2 kp9 .", "zq1": "bw4 hn8 dc6 ."}}, gt, Stub, PA)
    assert rows["p"]["ids"] == ["zq0", "zq1"] and min(rows["p"]["cider_s"]) > 0
    print("b1 kit self-test ok")


def selftest_host() -> None:
    """Host guard, locks and cap on synthetic paths: a raising, missing and readable machine-id path; isolation
    outside tmux, with a C-EN session, with another lock; the O_EXCL lock; the cap arithmetic and its marker."""
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
            (out / "grl_pilot").mkdir(parents=True)
            assert isolation(out, [], "") == ["not inside a tmux session (cen_chain.sh refuses while one exists)"]
            assert isolation(out, ["cencoco", "other"], "x") == ["C-EN tmux session cencoco"]
            assert isolation(Raising(t / "nope"), [], "x") == []
            take_lock(out / "b1_scaling/RUNNING", out, [], "x")
            assert refused(take_lock, out / "b1_scaling/RUNNING", out, [], "x")
            assert isolation(out, [], "x") == [f"lock {out / 'b1_scaling/RUNNING'} exists"]
            (out / "b1_scaling/RUNNING").unlink()
            (out / "grl_pilot/RUNNING").write_text("pilot\n")
            assert refused(take_lock, out / "b1_scaling/RUNNING", out, [], "x")
            used, mark = t / "gpu_seconds.tsv", t / "CAP_STOP"
            used.write_text("train start 1000\ntrain 50\ntrain start 2000\n")
            assert used_seconds(used, now=2600) == 650  # the open start is charged to now
            used.write_text("train start 1000\ntrain start 1300\ntrain 20\n")
            assert used_seconds(used, now=9999) == 320  # an unmatched start is charged to the next start
            used.unlink()
            assert left(used, mark) == CAP_S
            used.write_text(f"train {CAP_S - 100}\n")
            assert left(used, mark) == 100
            used.write_text(f"train {CAP_S - 30}\n")
            assert left(used, mark) == 0
            used.write_text("train 5\n")
            mark.write_text("stop\n")
            assert left(used, mark) == 0
            kt = t / "datasets/ktvic/images"
            kt.mkdir(parents=True)
            (kt / "a.jpg").write_bytes(b"zq7 vx2")
            assert ktvic_test_files(t / "datasets", set()) == []
            assert ktvic_test_files(t / "datasets", {sha_bytes(b"zq7 vx2")}) == [str(kt / "a.jpg")]
            (kt.parent / "test_split.json").write_text("{}")
            assert len(ktvic_test_files(t / "datasets", set())) == 1
            (kt.parent / "test_split.json").unlink()
            # CC-130 W1: the named twin passes only at its name under ktvic/images, with its pinned sha
            twin = "00000003589.jpg"
            (kt / twin).write_bytes(b"zq9 twin bytes")
            th = sha_bytes(b"zq9 twin bytes")
            saved = dict(TRAIN_TEST_TWINS)
            TRAIN_TEST_TWINS[twin] = th
            try:
                assert ktvic_test_files(t / "datasets", {th}) == []
                (kt / "00000001335.jpg").write_bytes(b"zq9 twin bytes")  # the test name, same bytes
                assert ktvic_test_files(t / "datasets", {th}) == [str(kt / "00000001335.jpg")]
                (kt / "00000001335.jpg").unlink()
                other = t / "datasets/ktvic_dev/images"
                other.mkdir(parents=True)
                (other / twin).write_bytes(b"zq9 twin bytes")  # the twin name in another directory
                assert ktvic_test_files(t / "datasets", {th}) == [str(other / twin)]
            finally:
                TRAIN_TEST_TWINS.clear()
                TRAIN_TEST_TWINS.update(saved)
    finally:
        if env is not None:
            os.environ["VSPS_MACHINE_ID"] = env


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--selftest-kit", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("lists")
    p.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("check")
    p.add_argument("--machine", action="store_true")
    p.add_argument("--job", type=Path)
    p.add_argument("--kit-b", type=Path)
    p = sub.add_parser("ids")
    p.add_argument("--dir", type=Path, required=True)
    p = sub.add_parser("sft")
    p.add_argument("--dir", type=Path, required=True)
    p = sub.add_parser("guard")
    p.add_argument("--head", required=True)
    p = sub.add_parser("lock")
    p.add_argument("--path", type=Path, default=LOCK)
    p = sub.add_parser("left")
    p.add_argument("--used", type=Path, required=True)
    p.add_argument("--marker", type=Path, required=True)
    p = sub.add_parser("step0")
    p.add_argument("--redecode", type=Path, required=True)
    p.add_argument("--n2", type=Path, required=True)
    p = sub.add_parser("score")
    p.add_argument("--dir", type=Path, required=True)
    p.add_argument("--kit-b", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("decide")
    p.add_argument("--ledger", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return
    if a.selftest_kit:
        selftest_kit()
        return
    handlers = {
        "lists": lambda: (SP.write_once(a.out, (json.dumps(make_lists(), indent=1) + "\n").encode()),
                          print(f"{SP.sha256(a.out)}  {a.out.name}")),
        "check": lambda: (check(a.machine, a.job, a.kit_b), print("b1 check ok")),
        "ids": lambda: write_ids(check(), a.dir),
        "sft": lambda: print(json.dumps(check_sft(a.dir))),
        "guard": lambda: cmd_guard(a),
        "lock": lambda: take_lock(a.path),
        "left": lambda: print(left(a.used, a.marker)),
        "step0": lambda: step0(a.redecode, a.n2)["passed"] or sys.exit(1),
        "score": lambda: cmd_score(a),
        "decide": lambda: cmd_decide(a),
    }
    if a.cmd not in handlers:
        ap.error("a subcommand or --selftest is required")
    handlers[a.cmd]()

if __name__ == "__main__":
    main()
