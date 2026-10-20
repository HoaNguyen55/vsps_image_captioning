#!/usr/bin/env python3
"""B-F1 scorer (Paper B, PD-22) for manuscript/prereg/2026-10-20_b_f1_final_stack.json: the single final KTVIC test
look of P1 + the S1 seed-consensus MBR-3. Every constant, threshold and rule is read from that registration.

    score_b_f1.py gate   OUT.json   pins, then the self-check that reproduces the S1 gate from S1's dev outputs;
                                    reads no test output
    score_b_f1.py dryrun OUT.json   SYNTHETIC references, decodes and provenance through admission, the selection,
                                    evaluate.py, F0 and every verdict branch
    score_b_f1.py run    OUT.json --gate G.json --outputs DIR
                                    the one scoring; only with this file and G.json (its all-PASS gate) at HEAD
    score_b_f1.py check  OUT.json --view V.json             (the job, on the decode host, before decoding) records
                                    machine_id and card; one GPU >= the registered GB, venv,
                                    base, adapters, test images; writes the caption-free view V of test_data.json
    score_b_f1.py stamp  DIR NAME MEMBER --view V.json --check C.json   (the job, after each decode) sidecar and
                                    provenance, carrying the check's machine_id and card
gate, dryrun and run need NCS_DATA (KTVIC under datasets/ktvic), VNCORENLP_DIR, JAVA_HOME (a JDK, for jnius) and java
on PATH. B_F1_STAGE=<dir> lets gate and dryrun read the four uncommitted B-F1 files of STAGED from that folder (records
name their committed paths); run refuses it. Writes numbers, ids, hashes and verdicts, never a caption. Outputs are
never overwritten.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from importlib.metadata import version
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
ROOT = Path(subprocess.run(["git", "-C", str(HERE.parent), "rev-parse", "--show-toplevel"], capture_output=True,
                           text=True, check=True).stdout.strip())
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
PREREG = ("manuscript/prereg/2026-10-20_b_f1_final_stack.json",
          "60a5cf68e9d52a3ca1589b54ed5ac73b44ba803bb1807a5862d0ae41201364c9")
MD, ADDENDUM = "manuscript/prereg/2026-10-20_b_f1_final_stack.md", "manuscript/prereg/2026-10-20_b_f1_instrument.json"
SCORER, JOB = "scripts/b_f1/score_b_f1.py", "scripts/queue/jobs/b_f1_ktvic_test_decode.sh"
STAGED = (PREREG[0], MD, ADDENDUM, JOB)
SEEDS = ("s42", "s43", "s44")  # S1's order: MBR ties go to the lower seed
TEST, TRAIN, VIEW = "data/datasets/ktvic/test_data.json", "data/datasets/ktvic/train_data.json", "ktvic_test_images_only.json"
SIGN = r"PASS if ci95_lo > 0; FAIL if point <= 0; else INCONCLUSIVE"  # the registered sign_gt_0 sentence (B-N1 §6)
SEEN: dict[str, str] = {}  # every input read, with its sha256


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    """sha256 of a file read in 16 MiB blocks (the base shards are several GB)."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 24), b""):
            h.update(block)
    return h.hexdigest()


def blob(commit: str, rel: str) -> bytes | None:
    r = subprocess.run(["git", "-C", str(ROOT), "cat-file", "blob", f"{commit}:{rel}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def pinned(rel: str, want: str | None = None, head: bool = True) -> bytes:
    """Bytes of repo file `rel` (a STAGED file from $B_F1_STAGE when set), refused unless its sha256 is the pin
    `want` (if given) and, if `head` and not staged, it equals its blob at HEAD."""
    stage = os.environ.get("B_F1_STAGE")
    staged = bool(stage) and rel in STAGED
    path = Path(stage) / Path(rel).name if staged else ROOT / rel
    if not path.is_file():
        raise SystemExit(f"PROVENANCE FAIL: {rel} is absent")
    data = path.read_bytes()
    if head and not staged and data != blob("HEAD", rel) or want and sha(data) != want:
        raise SystemExit(f"PROVENANCE FAIL: {rel} (sha256 {sha(data)}) differs from its pin or from its blob at HEAD")
    SEEN[rel] = sha(data)
    return data


def ncs_file(rel: str) -> Path:
    """Where a registered data/datasets file is read: under $NCS_DATA."""
    return Path(os.environ["NCS_DATA"]) / rel.removeprefix("data/")


def load() -> tuple[dict, dict]:
    """The registration and the constants this scorer uses; refused if a registered sentence reads otherwise."""
    P = json.loads(pinned(*PREREG))
    pr, sc_, se = P["primary"], P["self_check"], P["secondaries"]
    if pr["verdict_rule"]["text"] != SIGN or pr["ci"]["rng"] != f"numpy default_rng({pr['ci']['seed']})" or \
            VIEW not in P["decode"]["outputs"]["also"] or P["variant"]["seed_order"] != list(SEEDS):
        raise SystemExit("REFUSED: the registered verdict rule or bootstrap reads differently from this scorer")
    s1_seed = re.fullmatch(r"numpy default_rng\((\d+)\)", sc_["s1_bootstrap"]["rng"])
    cfg = {"B": pr["ci"]["B"], "seed": pr["ci"]["seed"], "level": float(pr["ci"]["level"].rstrip("%")),
           "tol": pr["f0"]["tolerance"], "n": pr["n_images"], "k2": se["K2"]["threshold_pp"],
           "B_s1": sc_["s1_bootstrap"]["B"], "seed_s1": int(s1_seed[1]), "n_clean": P["test_set"]["clean"]["n"],
           "members": dict(zip(SEEDS, P["members_order"], strict=True)),
           "names": P["decode"]["outputs"]["names"] | {"mbr": P["variant"]["mbr_name"]},
           "object_claims_allowed": se["count_matched_primary_registered"] and se["panel_side_registered"]}
    return P, cfg


def pin_all(P: dict) -> dict:
    """Every frozen file the registration marks gate_pins, at its sha256 (and at HEAD when it is in git)."""
    for f in P["frozen_files"]:
        if f["gate_pins"]:
            data = (ncs_file(f["path"]).read_bytes() if f["path"].startswith("data/datasets/") else
                    pinned(f["path"], f["sha256"], head=not f["git"].startswith("not in git")))
            if sha(data) != f["sha256"]:
                raise SystemExit(f"PROVENANCE FAIL: {f['path']} differs from its pin")
            SEEN[f["path"]] = f["sha256"]
    return {f["path"]: f["sha256"] for f in P["frozen_files"] if f["gate_pins"]}


def modules():
    """The committed S1 code path (pinned in frozen_files before import)."""
    import evaluate as ev
    import object_prf as op
    import rl_report as rp
    import rl_reward as rr
    import seed_consensus as sc
    from rescap.chair import objects_in

    if ev.KTVIC.name != "ktvic":
        raise SystemExit("REFUSED: NCS_DATASET is set; KTVIC test is scored only from datasets/ktvic")
    return ev, op, rp, rr, sc, objects_in


def env() -> dict:
    vdir = Path(os.environ.get("VNCORENLP_DIR", ""))
    return {"python": sys.version.split()[0], **{p: version(p) for p in ("numpy", "pycocoevalcap", "py_vncorenlp",
                                                                        "pyjnius")},
            **{f: sha((vdir / f).read_bytes()) for f in ("VnCoreNLP-1.2.jar", "models/wordsegmenter/wordsegmenter.rdr")
               if (vdir / f).is_file()}}


# ------------------------------------------------------------------------------------------- the S1 code path
def selector(M, reward, rest: list[str]):
    """seed_consensus.mbr's selection lines on any ids: medoid by CiderD with the document frequencies of the
    references of `rest` (train minus dev300), words from the reward's Segmenter, ties to the lower seed."""
    _, _, _, rr, sc, _ = M
    cider = rr.CiderD([reward.refs[j] for j in rest])

    def pick(caps: dict, ids: list[str]) -> list[str]:
        toks = {s: [t.split() for t in reward.seg([caps[s][i] for i in ids])] for s in SEEDS}
        return [SEEDS[sc.medoid([toks[s][n] for s in SEEDS], cider)] for n in range(len(ids))]
    return pick


def mbr_bytes(caps: dict, ids: list[str], pick: list[str]) -> bytes:
    """The MBR prediction file exactly as seed_consensus.mbr writes it."""
    return json.dumps({i: caps[s][i] for i, s in zip(ids, pick, strict=True)}, ensure_ascii=False,
                      indent=1).encode("utf-8")


def s1_rows(S: dict, G: dict, per: dict, dv: dict, dch: dict, sel: dict) -> list[dict]:
    """The registered self-check comparisons, from recomputed values `per`, `dv`, `dch` and `sel`."""
    e, r = S["expect"], {"D": S["expect"]["decimals"]["D_MBR"], "C": S["expect"]["decimals"]["dCHAIR_i"]}
    rows = [{"check": f"per-image CIDEr-D {k} equals gate.json", "ok": per[k].tolist() == G["per_image_cider_x100"][k]}
            for k in sorted(S["s1_results"])]
    rows += [{"check": "D_MBR equals gate.json", "ok": dv["mbr"] == G["D_cider_x100_mean_lo_hi"]["mbr"],
              "value": dv["mbr"]},
             {"check": "dCHAIR_i (MBR) equals gate.json", "ok": dch["mbr"] == G["dCHAIR_i_points"]["mbr"],
              "value": dch["mbr"]},
             {"check": "D_MBR at the quoted decimals", "ok": [round(x, r["D"]) for x in dv["mbr"]] == e["D_MBR"]},
             {"check": "dCHAIR_i at the quoted decimals", "ok": round(dch["mbr"], r["C"]) == e["dCHAIR_i"]},
             {"check": "MBR picks equal S1's picked_member", "ok": sel["picks_equal"]},
             {"check": "MBR prediction bytes equal S1's file", "ok": sel["bytes_equal"]}]
    return rows


def self_check(P: dict, cfg: dict, M, seg) -> list[dict]:
    """Reproduce the S1 gate from S1's dev outputs through the code this scorer uses on test; reads no test file."""
    ev, _, rp, rr, sc, _ = M
    S = P["self_check"]
    d = ROOT / S["s1_outputs_dir"]
    if sc.BOOT != {"seed": cfg["seed_s1"], "b": cfg["B_s1"]}:
        raise SystemExit("REFUSED: seed_consensus.BOOT is not S1's registered bootstrap")
    reg = sc.load_prereg()
    dev, rest = sc.split_ids(reg)
    reward = rr.Reward(ev.references("train_data.json"), seg)  # dev300 is part of KTVIC train
    per, chair, caps = {}, {}, {}
    for k in sorted(S["s1_results"]):
        ids, caps[k], per[k] = rp.dev_scores(str(d / S["s1_results"][k]), reward)  # asserts the 1e-6 F0
        if ids != dev:
            raise SystemExit(f"{k}: not exactly the dev300 images")
        chair[k] = 100 * json.loads((d / S["s1_results"][k]).read_text(encoding="utf-8"))["chair"]["CHAIR_i"]
    dv, dch = sc.variant_deltas(per, chair)
    G = json.loads((d / "gate.json").read_text(encoding="utf-8"))
    sel = json.loads((d / "p1dev_mbr3_selection.json").read_text(encoding="utf-8"))
    pick = selector(M, reward, rest)(caps, dev)
    got = mbr_bytes(caps, dev, pick)
    rows = s1_rows(S, G, per, dv, dch, {"picks_equal": pick == sel["picked_member"],
                                        "bytes_equal": sha(got) == SEEN[f"{S['s1_outputs_dir']}/p1dev_mbr3-dev300-short"
                                                                         ".preds.json"] == sel["preds_sha256"]})
    void = json.loads((d / "s1_void_check.json").read_text(encoding="utf-8"))["void"]
    t3v = json.loads((ROOT / S["t3v"]["path"]).read_text(encoding="utf-8"))["overall"]["S1"]
    return rows + [{"check": "S1 not void", "ok": void is False}, {"check": "T-3V: S1 VERIFIED", "ok": t3v == "VERIFIED"},
                   {"check": "S1 carried MBR", "ok": (G["verdict"], G["carried"]) == (
                       P["variant"]["carried_by"]["keys"]["verdict"], P["variant"]["carried_by"]["keys"]["carried"])}]


def gate_body(P: dict, cfg: dict, M, seg) -> dict:
    pins = pin_all(P)
    add, job = json.loads(pinned(ADDENDUM)), pinned(JOB)
    inst = {"prereg_sha256": add.get("prereg_sha256") == PREREG[1],
            "prereg_md_sha256": add.get("prereg_md_sha256") == sha(pinned(MD)),
            "new_files": add.get("new_files") == {SCORER: sha(HERE.read_bytes()), JOB: sha(job)},
            "no_deviations": add.get("deviations") == []}
    rows = self_check(P, cfg, M, seg)
    return {"pins": pins, "instrument": inst, "self_check": rows,
            "all_pass": all(inst.values()) and all(r["ok"] for r in rows), "test_outputs_read": False}


# ------------------------------------------------------------------------------------------- the machine side
def check(P: dict, out: Path, view: Path) -> int:
    """On the decode host before any decode: B-F1 files at HEAD, adapters, base snapshot, venv, one GPU with the
    registered memory (machine_id and card recorded), test images; then
    the caption-free view of test_data.json (written once, verified when it exists)."""
    import socket

    import torch
    import transformers
    from huggingface_hub import constants
    import peft

    rows, d, ncs = [], P["decode"], Path(os.environ["NCS_DATA"])
    for rel in (*STAGED, SCORER, "scripts/evaluate.py", "scripts/checkpoint_resume_hook.py", P["test_set"]["primary"]["ids"]):
        rows.append({"check": f"{rel} committed, unmodified at HEAD", "ok": (ROOT / rel).read_bytes() == blob("HEAD", rel)})
    add = json.loads((ROOT / ADDENDUM).read_text(encoding="utf-8"))
    F = {f["path"]: f["sha256"] for f in P["frozen_files"]}
    rows += [{"check": "addendum pins this scorer, the job and the prereg", "ok": add["new_files"] == {
        SCORER: sha(HERE.read_bytes()), JOB: sha((ROOT / JOB).read_bytes())} and add["prereg_sha256"] == PREREG[1]},
             {"check": "evaluate.py and the hook at their pins", "ok": all(
                 sha((ROOT / f).read_bytes()) == F[f] for f in ("scripts/evaluate.py", "scripts/checkpoint_resume_hook.py"))},
             {"check": "test_data.json at its pin", "ok": sha(ncs_file(TEST).read_bytes()) == F[TEST]}]
    for m, a in sorted(P["members"].items()):
        for f, k in (("adapter_model.safetensors", "adapter_sha256"), ("adapter_config.json", "adapter_config_sha256")):
            p = ncs / "runs" / m / f
            rows.append({"check": f"{m}/{f}", "ok": p.is_file() and sha_file(p) == a[k]})
    repo = Path(constants.HF_HUB_CACHE) / f"models--{d['base']['id'].replace('/', '--')}"
    ref = (repo / "refs" / "main").read_text(encoding="utf-8").strip() if (repo / "refs" / "main").is_file() else None
    rows.append({"check": "base refs/main", "ok": ref == d["base"]["revision"]})
    for name, want in sorted(d["base"]["shards_sha256"].items()):
        shard = repo / "snapshots" / d["base"]["revision"] / name
        rows.append({"check": f"base {name}", "ok": shard.is_file() and sha_file(shard) == want})
    n_gpu = torch.cuda.device_count()
    gpu = torch.cuda.get_device_name(0) if n_gpu else ""
    mem = torch.cuda.get_device_properties(0).total_memory if n_gpu else 0
    have = {"torch": torch.__version__, "transformers": transformers.__version__, "peft": peft.__version__}
    rows += [{"check": "one GPU with the registered memory", "ok": n_gpu == d["machine"]["n_gpus"] and
              mem >= d["machine"]["min_gpu_memory_gb"] * 10 ** 9, "n_gpus": n_gpu, "gpu_memory_bytes": mem},
             {"check": "venv versions", "ok": have == d["venv"], **have},
             {"check": "env", "ok": "NCS_DATASET" not in os.environ and os.environ.get("HF_HUB_OFFLINE") == "1"}]
    tsv = [x.split("\t") for x in (ROOT / P["test_set"]["primary"]["ids"]).read_text(encoding="utf-8").splitlines()]
    images = ncs / "datasets" / "ktvic" / "images"
    rows.append({"check": "every test image at its manifest sha256", "ok": all(
        (images / f).is_file() and sha((images / f).read_bytes()) == h for _, f, h in tsv)})
    data = json.loads(ncs_file(TEST).read_text(encoding="utf-8"))  # images and ids only leave this function
    names = {str(x.get("id", x.get("image_id"))): x.get("file_name") or x.get("filename") for x in data["images"]}
    scored = {str(a["image_id"]) for a in data["annotations"] if a.get("caption")}
    want = json.dumps({"images": data["images"]}, ensure_ascii=False).encode("utf-8")
    rows.append({"check": "view ids = manifest ids = referenced ids", "ok": names == {i: f for i, f, _ in tsv}
                 and set(names) == scored and len(names) == P["test_set"]["primary"]["n"]})
    if not view.exists() and all(r["ok"] for r in rows):
        with open(view, "xb") as fh:
            fh.write(want)
    rows.append({"check": "view is the images list of test_data.json", "ok": view.is_file() and view.read_bytes() == want})
    bad = [r["check"] for r in rows if not r["ok"]]
    with open(out, "x", encoding="utf-8") as fh:
        json.dump({"pass": not bad, "failed": bad, "machine_id": socket.gethostname(), "card": gpu, "checks": rows,
                   "view_sha256": sha(want)}, fh, indent=1)
    print("check PASS" if not bad else f"check FAIL: {bad}")
    return 1 if bad else 0


def stamp(odir: Path, name: str, member: str, view: Path, check_file: Path, base_id: str, meta=None) -> dict:
    """The .sha256 sidecar and the provenance JSON of one decode (written once), with the card recorded by `check`;
    `meta` is the hook's provenance_metadata (machine_id, git_head_sha, hook and train_stage2 sha256, ...)."""
    if meta is None:
        from checkpoint_resume_hook import provenance_metadata as meta
    f, ncs = odir / f"{name}.preds.json", Path(os.environ["NCS_DATA"])
    raw, adir = f.read_bytes(), ncs / "runs" / member
    head = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--", *STAGED, SCORER], capture_output=True,
                           text=True).stdout.strip()
    from huggingface_hub import constants

    rev = Path(constants.HF_HUB_CACHE) / f"models--{base_id.replace('/', '--')}" / "refs" / "main"
    prov = {**meta(adir), "git_head_sha": head, "git_dirty": bool(dirty), "member": member, "preds_file": f.name,
            "preds_sha256": sha(raw), "n_predictions": len(json.loads(raw)),
            "preds_mtime_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(f.stat().st_mtime)),
            "adapter_sha256": sha_file(adir / "adapter_model.safetensors"),
            "adapter_config_sha256": sha((adir / "adapter_config.json").read_bytes()),
            "job_sha256": os.environ.get("B_F1_JOB_SHA256"), "scorer_sha256": sha(HERE.read_bytes()),
            "evaluate_sha256": sha((ROOT / "scripts/evaluate.py").read_bytes()),
            "base_revision": rev.read_text(encoding="utf-8").strip() if rev.is_file() else None,
            "test_data_sha256": sha(ncs_file(TEST).read_bytes()), "view_file": view.name,
            "view_sha256": sha(view.read_bytes()), "check_file": check_file.name,
            "check_sha256": sha(check_file.read_bytes()), "card": json.loads(check_file.read_text(encoding="utf-8"))["card"]}
    with open(odir / f"{name}.provenance.json", "x", encoding="utf-8") as fh:
        json.dump(prov, fh, indent=1)
    with open(odir / f"{name}.preds.json.sha256", "x", encoding="utf-8") as fh:
        fh.write(f"{prov['preds_sha256']}  {f.name}\n")
    return prov


# ------------------------------------------------------------------------------------------- the one look
def admit(P: dict, cfg: dict, odir: Path, ids: list[str], add: dict, git: bool = True) -> tuple[dict, dict]:
    """Captions of the three members, refused (K-PROV, K-COV) unless every sidecar, checksum and provenance field is
    the registered one, and all three carry the machine_id and card of one passing check (the machine rule, CC-042);
    with `git`, the decode's commit carries this registration and followed its commit."""
    F = {f["path"]: f["sha256"] for f in P["frozen_files"]}
    sums = {Path(p).name: h for h, p in (x.split("  ", 1) for x in (odir / "SHA256SUMS").read_text(
        encoding="utf-8").splitlines())}
    view = (odir / VIEW).read_bytes()
    caps, facts, bad, hosts = {}, {}, {}, set()
    added = subprocess.run(["git", "-C", str(ROOT), "log", "--diff-filter=A", "--format=%cI", "--", PREREG[0]],
                           capture_output=True, text=True).stdout.split()
    for s, m in cfg["members"].items():
        name = cfg["names"][m]
        raw = (odir / f"{name}.preds.json").read_bytes()
        SEEN[f"outputs/{name}.preds.json"] = sha(raw)
        prov = json.loads((odir / f"{name}.provenance.json").read_text(encoding="utf-8"))
        chk = odir / str(prov.get("check_file"))
        ck = json.loads(chk.read_text(encoding="utf-8")) if chk.is_file() else {}
        want = {"machine_id": ck.get("machine_id"), "card": ck.get("card"), "check_sha256": sums.get(chk.name),
                "member": m, "preds_sha256": sha(raw),
                "adapter_sha256": P["members"][m]["adapter_sha256"],
                "adapter_config_sha256": P["members"][m]["adapter_config_sha256"],
                "job_sha256": add["new_files"][JOB], "scorer_sha256": add["new_files"][SCORER],
                "evaluate_sha256": F["scripts/evaluate.py"], "base_revision": P["decode"]["base"]["revision"],
                "test_data_sha256": F[TEST], "view_file": VIEW, "view_sha256": sha(view), "git_dirty": False}
        why = [k for k, v in want.items() if prov.get(k) != v or v is None]
        why += [] if ck.get("pass") is True else ["check did not pass"]
        hosts.add((prov.get("machine_id"), prov.get("card")))
        side = (odir / f"{name}.preds.json.sha256").read_text(encoding="utf-8").split()
        why += [] if side == [sha(raw), f"{name}.preds.json"] else ["sha256 sidecar"]
        why += [] if sums.get(f"{name}.preds.json") == sha(raw) else ["SHA256SUMS"]
        if git:
            c = prov.get("git_head_sha") or ""
            why += [f"commit {c[:7]} lacks {r}" for r in (PREREG[0], ADDENDUM, JOB, SCORER) if not re.fullmatch(
                "[0-9a-f]{40}", c) or blob(c, r) is None or blob(c, r) != blob("HEAD", r)]
            why += [] if added and datetime.fromisoformat(added[-1]) < datetime.fromisoformat(
                prov["preds_mtime_utc"].replace("Z", "+00:00")) else ["decoded before the registration commit"]
        if why:
            bad[name] = why
            continue
        caps[s] = {str(k): v for k, v in json.loads(raw).items()}
        if sorted(caps[s]) != ids:
            bad[name] = [f"K-COV: {len(set(ids) - set(caps[s]))} test ids without a prediction"]
        facts[name] = {k: prov[k] for k in ("machine_id", "card", "git_head_sha", "preds_sha256", "preds_mtime_utc",
                                           "adapter_sha256", "job_sha256", "n_predictions")}
    if len(hosts) > 1:
        bad["machine rule"] = ["the three decodes do not share one machine_id and card"]
    if bad:
        raise SystemExit(f"REFUSED (K-PROV / K-COV): {json.dumps(bad, sort_keys=True)}")
    return caps, facts


def evaluate_py(preds: Path, name: str, tmp: Path, ncs: Path) -> Path:
    """scripts/evaluate.py, unchanged, on `preds` in a fresh process (the protocol card); its table is not shown."""
    out = tmp / f"{name}.json"
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "evaluate.py"), "--predictions", str(preds), "--split",
                        "test_data.json", "--prompt", "short", "--name", name, "--out", str(out)],
                       capture_output=True, encoding="utf-8", errors="replace", env={**os.environ, "NCS_DATA": str(ncs)})
    if r.returncode or not out.is_file():
        raise SystemExit(f"K-F0: scripts/evaluate.py failed on {name} (rc {r.returncode})")
    return out


def f0(M, result: Path, reward, ids: list[str], tol: float) -> tuple[dict, np.ndarray | None]:
    """F0 of one system: rdrsegmenter word level, exactly the test ids, per-image mean = corpus value (rl_report's
    1e-6 assert and the registered tolerance)."""
    rp = M[2]
    res = json.loads(result.read_text(encoding="utf-8"))
    row = next(r for r in res["results"] if r["tokenization"] == "word-level")
    out = {"corpus_CIDEr_x100": row["scores_scaled_x100"]["CIDEr"], "segmenter": row["segmenter"],
           "result_sha256": sha(result.read_bytes())}
    try:
        got, _, per = rp.dev_scores(str(result), reward)
    except AssertionError:
        return out | {"pass": False, "why": "rl_report.dev_scores: per-image mean differs from the corpus value"}, None
    diff = abs(float(per.mean()) - out["corpus_CIDEr_x100"])
    ok = row["segmenter"] == "rdrsegmenter" and got == ids and diff < tol
    return out | {"mean_per_image_x100": float(per.mean()), "abs_diff": diff, "pass": ok}, per


def verdict_sign(point: float, lo: float) -> str:
    """sign_gt_0 as registered (B-N1 §6)."""
    return "PASS" if lo > 0 else "FAIL" if point <= 0 else "INCONCLUSIVE"


def statistics(P: dict, cfg: dict, M, per: dict, res: dict, caps: dict, gold: dict, ids: list[str],
               clean: list[str]) -> dict:
    """The primary, the prediction check, K2, K3 and the descriptive readouts, from per-image CIDEr-D `per`, the
    evaluate.py results `res` and the captions `caps` of s42, s43, s44 and mbr."""
    _, op, _, rr, sc, objects_in = M
    q = (100 - cfg["level"]) / 2
    d = per["mbr"] - sum(per[s] for s in SEEDS) / len(SEEDS)
    D = rr.boot(d, cfg["seed"], cfg["B"])
    idx = np.random.default_rng(cfg["seed"]).integers(0, len(ids), (cfg["B"], len(ids)))  # rl_reward.boot's draws
    if [float(np.percentile(d[idx].mean(1), x)) for x in (q, 100 - q)] != D[1:]:
        raise AssertionError("the K3 draws are not the primary's draws")
    stats = {k: {x: v for x, v in sc.system_stats(res[k], caps[k], gold, {}).items() if not x.endswith("_panel")}
             for k in (*SEEDS, "mbr")}
    mean = {x: sum(stats[s][x] for s in SEEDS) / len(SEEDS) for x in stats["mbr"]}
    delta = {x: stats["mbr"][x] - mean[x] for x in mean}
    rows = {k: [op.image_counts(set(objects_in(caps[k][i])), gold[i], sc._exact) for i in ids] for k in stats}
    df1 = [op.scores([rows["mbr"][j] for j in b])["F1"] - sum(op.scores([rows[s][j] for j in b])["F1"]
                                                            for s in SEEDS) / len(SEEDS) for b in idx]
    k3 = [delta["F1_ktvic5"], *(float(np.percentile(df1, x)) for x in (q, 100 - q))]
    readout = {"dCIDEr": D[0], "dBLEU4": delta["BLEU4"], "dF1": delta["F1_ktvic5"], "dCHAIRi_points": delta["CHAIR_i"],
               "dmentions": delta["mentions_per_caption"]}
    pos = {i: n for n, i in enumerate(ids)}
    cd = d[[pos[i] for i in clean]]
    member_cider = [stats[s]["CIDEr"] for s in SEEDS]
    return {
        "primary": {"D_MBR_x100_mean_lo_hi": D, "verdict": verdict_sign(D[0], D[1]),
                    "rule": P["primary"]["verdict_rule"]["text"], "n_images": len(ids), "B": cfg["B"],
                    "rng": P["primary"]["ci"]["rng"]},
        "prediction_check": {"values": readout, "inside": sc.predictions_hold(readout, P["prediction_check"]["values"]),
                             "use": P["prediction_check"]["use"]},
        "K2": {"text": P["secondaries"]["K2"]["text"], "dCHAIR_i_points": delta["CHAIR_i"],
               "fires": delta["CHAIR_i"] > cfg["k2"], "reported_as": "harm" if delta["CHAIR_i"] > cfg["k2"] else "no harm"},
        "K3": {"text": P["secondaries"]["K3"]["text"], "dF1_ktvic5_mean_lo_hi": k3, "fires": k3[2] < 0,
               "reported_as": "negative" if k3[2] < 0 else "not a negative"},
        "objects": {"claims_allowed": cfg["object_claims_allowed"],
                    "status": "may enter a claim" if cfg["object_claims_allowed"] else "descriptive only"},
        "clean_subset": {"n": len(clean), "D_MBR_x100_mean_lo_hi": rr.boot(cd, cfg["seed"], cfg["B"]),
                         "role": P["test_set"]["clean"]["role"]},
        "systems": stats, "member_mean": mean, "deltas_vs_member_mean": delta,
        "members_cider_spread": {"values": dict(zip(SEEDS, member_cider, strict=True)),
                                 "range": max(member_cider) - min(member_cider)},
        "all_three_members_agree_share": float(np.mean([len({caps[s][i] for s in SEEDS}) == 1 for i in ids])),
        "absolute_cider_note": P["primary"]["absolute_cider"]}


def look(P: dict, cfg: dict, M, seg, caps: dict, files: dict, train_refs: dict, rest: list[str], test_refs: dict,
         clean: list[str], ncs: Path, tmp: Path) -> dict:
    """Selection, then evaluate.py on the three members and the MBR, F0, and (only if F0 holds) the statistics."""
    _, _, _, rr, _, objects_in = M
    ids = sorted(test_refs)
    pick = selector(M, rr.Reward(train_refs, seg), rest)(caps, ids)
    mbr = tmp / f"{cfg['names']['mbr']}.preds.json"
    mbr.write_bytes(mbr_bytes(caps, ids, pick))
    systems = {**files, "mbr": mbr}
    reward = rr.Reward(test_refs, seg)
    out = {"selection": {"picked_member": pick, "picked_counts": {s: pick.count(s) for s in SEEDS},
                         "mbr_preds_sha256": sha(mbr.read_bytes()), "df_images": len(rest)}, "F0": {}}
    per, res = {}, {}
    for k in (*SEEDS, "mbr"):
        result = evaluate_py(systems[k], Path(systems[k]).name.removesuffix(".preds.json"), tmp, ncs)
        out["F0"][k], per[k] = f0(M, result, reward, ids, cfg["tol"])
        res[k] = json.loads(result.read_text(encoding="utf-8"))
    out["K_F0_fired"] = not all(x["pass"] for x in out["F0"].values())
    if out["K_F0_fired"]:
        return out | {"statistics": "not computed (K-F0)"}
    gold = {i: set().union(*(objects_in(r) for r in test_refs[i])) for i in ids}
    all_caps = {**caps, "mbr": {i: caps[s][i] for i, s in zip(ids, pick, strict=True)}}
    return out | statistics(P, cfg, M, per, res, all_caps, gold, ids, clean) | {
        "test_ids": ids, "per_image_cider_x100": {k: per[k].tolist() for k in per}}


def run(P: dict, cfg: dict, a) -> dict:
    """The registered analysis, only from this scorer committed at HEAD with its committed all-PASS gate output."""
    if os.environ.get("B_F1_STAGE") or HERE != ROOT / SCORER:
        raise SystemExit("REFUSED: run reads only the committed copies (no B_F1_STAGE; this file at " + SCORER + ")")
    pinned(SCORER)
    rel = Path(a.gate).resolve().relative_to(ROOT).as_posix()
    G = json.loads(pinned(rel))
    if [G["mode"], G["all_pass"], G["script_sha256"], G["prereg"]["sha256"]] != ["gate", True, sha(HERE.read_bytes()),
                                                                                  PREREG[1]]:
        raise SystemExit("REFUSED: the gate file is not a committed all-PASS gate of this scorer")
    M = modules()
    from rl_reward import Segmenter
    seg = Segmenter()
    body = gate_body(P, cfg, M, seg)
    if not body["all_pass"] or [body[k] for k in ("pins", "instrument", "self_check")] != [
            G[k] for k in ("pins", "instrument", "self_check")]:
        raise SystemExit("REFUSED (K-SC): the self-check or the pins differ from the committed gate")
    ev, sc = M[0], M[4]
    test_refs = ev.references("test_data.json")
    ids = sorted(test_refs)
    clean = sorted(pinned(P["test_set"]["clean"]["path"], {f["path"]: f["sha256"] for f in P["frozen_files"]}[
        P["test_set"]["clean"]["path"]]).decode("utf-8").split())
    if len(ids) != cfg["n"] or len(clean) != cfg["n_clean"] or not set(clean) <= set(ids):
        raise SystemExit("REFUSED: the test ids or the clean list differ from the registration")
    odir = Path(a.outputs)
    caps, facts = admit(P, cfg, odir, ids, json.loads(pinned(ADDENDUM)), git=True)
    _, rest = sc.split_ids(sc.load_prereg())
    with tempfile.TemporaryDirectory() as tmp:
        files = {s: odir / f"{cfg['names'][m]}.preds.json" for s, m in cfg["members"].items()}
        res = look(P, cfg, M, seg, caps, files, ev.references("train_data.json"), rest, test_refs, clean,
                   Path(os.environ["NCS_DATA"]), Path(tmp))
    return {"gate": {"path": rel, "sha256": SEEN[rel]}, "self_check": body["self_check"], "decodes": facts, **res,
            "ledger_and_closure": {"ledger": [x["id"] for x in P["test_look_ledger"]["entries"]],
                                   "closure": P["closure"]["rule"]}}


# ------------------------------------------------------------------------------------------- dry run
def _syn(rng, words: list[str], k: int) -> str:
    return " ".join(rng.choice(words, k, replace=True).tolist())


def dryrun(P: dict, cfg: dict) -> dict:
    """SYNTHETIC: made-up ids, references, captions, adapters and provenance. Exercises stamp and admission (with
    five refusals), the S1 selection with RDRSegmenter, evaluate.py and F0 end to end, K-F0, the self-check
    comparison failing, and every verdict branch of sign_gt_0, K2, K3, the prediction check and the object rule."""
    M = modules()
    from rl_reward import Segmenter
    seg = Segmenter()
    rng = np.random.default_rng(7)
    P, Q = copy.deepcopy(P), copy.deepcopy(P)  # Q: the registration with the synthetic adapters and test data
    objs = ["người", "chó", "mèo", "bàn", "xe máy", "ghế"]
    filler = ["một", "đang", "đứng", "ngồi", "cạnh", "trên", "trong", "sân", "nhà", "đường"]
    out = {"SYNTHETIC": "made-up ids, references, captions and provenance; no KTVIC caption, reference or decode is "
                        "read"}
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        ncs, odir = tmp / "ncs", tmp / "outputs"
        (ncs / "datasets" / "ktvic").mkdir(parents=True)
        odir.mkdir()
        test_ids, train_ids = [str(100 + 3 * k) for k in range(60)], [str(900 + k) for k in range(40)]
        obj = {i: [objs[int(j)] for j in rng.choice(len(objs), 2, replace=False)] for i in test_ids + train_ids}
        refs = {i: [f"{obj[i][0]} {_syn(rng, filler, 3)} {obj[i][1]} {_syn(rng, filler, 2)}" for _ in range(5)]
                for i in test_ids + train_ids}
        for split, ids in (("test_data.json", test_ids), ("train_data.json", train_ids)):
            (ncs / "datasets" / "ktvic" / split).write_text(json.dumps({
                "images": [{"id": int(i), "filename": f"{i}.jpg"} for i in ids],
                "annotations": [{"image_id": int(i), "caption": c} for i in ids for c in refs[i]]}, ensure_ascii=False),
                encoding="utf-8")
        view = odir / VIEW
        view.write_text(json.dumps({"images": [{"id": int(i), "filename": f"{i}.jpg"} for i in test_ids]}), encoding="utf-8")
        caps = {"s42": {i: refs[i][0] for i in test_ids}, "s43": {i: refs[i][int(i) % 2] for i in test_ids},
                "s44": {i: f"{objs[int(i) % len(objs)]} {_syn(rng, filler, 4)}" for i in test_ids}}
        hf = tmp / "hf" / f"models--{P['decode']['base']['id'].replace('/', '--')}" / "refs"
        hf.mkdir(parents=True)
        (hf / "main").write_text(P["decode"]["base"]["revision"], encoding="utf-8")
        keep = {k: os.environ.get(k) for k in ("NCS_DATA", "HF_HUB_CACHE")}
        os.environ |= {"NCS_DATA": str(ncs), "HF_HUB_CACHE": str(tmp / "hf")}
        add = {"new_files": {JOB: "1" * 64, SCORER: sha(HERE.read_bytes())}}

        def synthetic_meta(_adir):  # the hook's fields, with a synthetic host instead of this one
            return {"machine_id": "synthetic-host", "resumed_from_step": []}

        chk = odir / "check.json"
        chk.write_text(json.dumps({"pass": True, "machine_id": "synthetic-host", "card": "synthetic GPU"}), encoding="utf-8")
        F = {f["path"]: f["sha256"] for f in P["frozen_files"]}
        try:
            for s, m in cfg["members"].items():
                (ncs / "runs" / m).mkdir(parents=True)
                (ncs / "runs" / m / "adapter_model.safetensors").write_bytes(m.encode())
                (ncs / "runs" / m / "adapter_config.json").write_bytes(b"{}")
                Q["members"][m] = {"adapter_sha256": sha(m.encode()), "adapter_config_sha256": sha(b"{}")}
                (odir / f"{cfg['names'][m]}.preds.json").write_text(json.dumps(caps[s], ensure_ascii=False, indent=1),
                                                                    encoding="utf-8")
                os.environ["B_F1_JOB_SHA256"] = add["new_files"][JOB]
                stamp(odir, cfg["names"][m], m, view, chk, P["decode"]["base"]["id"], meta=synthetic_meta)
            F[TEST] = sha((ncs / "datasets" / "ktvic" / "test_data.json").read_bytes())
            Q["frozen_files"] = [{"path": k, "sha256": v} for k, v in F.items()]
            (odir / "SHA256SUMS").write_text("".join(f"{sha(p.read_bytes())}  {p.name}\n" for p in sorted(odir.iterdir())),
                                             encoding="utf-8")
            caps_ok, facts = admit(Q, cfg, odir, test_ids, add, git=False)
            refusals = {}
            for label, edit in (("wrong adapter sha256", lambda p: p | {"adapter_sha256": "0" * 64}),
                                ("machine_id differs from the other decodes", lambda p: p | {"machine_id": "elsewhere"}),
                                ("wrong job sha256", lambda p: p | {"job_sha256": "2" * 64}),
                                ("dirty tree", lambda p: p | {"git_dirty": True})):
                f = odir / f"{cfg['names']['p1dev_s43']}.provenance.json"
                orig = f.read_text(encoding="utf-8")
                f.write_text(json.dumps(edit(json.loads(orig))), encoding="utf-8")
                try:
                    admit(Q, cfg, odir, test_ids, add, git=False)
                    refusals[label] = "admitted"
                except SystemExit as e:
                    refusals[label] = str(e)
                f.write_text(orig, encoding="utf-8")
            f = odir / f"{cfg['names']['p1dev_s42']}.provenance.json"
            orig = f.read_text(encoding="utf-8")  # a commit without the registration, decoded before it was made
            f.write_text(json.dumps(json.loads(orig) | {"git_head_sha": "synthetic", "preds_mtime_utc":
                                                        "2000-01-01T00:00:00Z"}), encoding="utf-8")
            try:
                admit(Q, cfg, odir, test_ids, add, git=True)
                refusals["commit lacks the registration"] = "admitted"
            except SystemExit as e:
                refusals["commit lacks the registration"] = str(e)
            f.write_text(orig, encoding="utf-8")
            short = dict(list(caps["s44"].items())[1:])
            f = odir / f"{cfg['names']['p1dev_s44']}.preds.json"
            f.write_text(json.dumps(short, ensure_ascii=False), encoding="utf-8")
            try:  # a missing id with consistent hashes: K-COV
                for x in (f"{cfg['names']['p1dev_s44']}.provenance.json", f"{cfg['names']['p1dev_s44']}.preds.json.sha256"):
                    (odir / x).rename(odir / f"{x}.orig")
                stamp(odir, cfg["names"]["p1dev_s44"], "p1dev_s44", view, chk, P["decode"]["base"]["id"], meta=synthetic_meta)
                (odir / "SHA256SUMS").write_text("".join(f"{sha(p.read_bytes())}  {p.name}\n" for p in sorted(
                    odir.iterdir()) if not p.name.endswith(".orig")), encoding="utf-8")
                admit(Q, cfg, odir, test_ids, add, git=False)
                refusals["missing test id"] = "admitted"
            except SystemExit as e:
                refusals["missing test id"] = str(e)
            assert all(v.startswith("REFUSED") for v in refusals.values()), refusals
            assert "K-COV" in refusals["missing test id"], refusals
            out["admission"] = {"admitted": sorted(facts), "refusals": refusals}

            from evaluate import references
            test_refs = references(str(ncs / "datasets" / "ktvic" / "test_data.json"))
            train_refs = references(str(ncs / "datasets" / "ktvic" / "train_data.json"))
            files = {}
            for s, m in cfg["members"].items():
                files[s] = tmp / f"{cfg['names'][m]}.preds.json"
                files[s].write_text(json.dumps(caps_ok[s], ensure_ascii=False, indent=1), encoding="utf-8")
            clean = test_ids[::3]
            e2e = look(P, cfg, M, seg, caps_ok, files, train_refs, train_ids, test_refs, clean, ncs, tmp)
            assert not e2e["K_F0_fired"] and all(x["pass"] for x in e2e["F0"].values()), e2e["F0"]
            assert e2e["primary"]["verdict"] in ("PASS", "FAIL", "INCONCLUSIVE")
            assert e2e["selection"]["picked_counts"]["s44"] < e2e["selection"]["picked_counts"]["s42"]
            out["end_to_end"] = {k: e2e[k] for k in ("selection", "F0", "K_F0_fired", "primary", "K2", "K3", "objects")}

            reward = M[3].Reward(test_refs, seg)
            res = evaluate_py(files["s42"], "tampered", tmp, ncs)
            j = json.loads(res.read_text(encoding="utf-8"))
            next(r for r in j["results"] if r["tokenization"] == "word-level")["scores_scaled_x100"]["CIDEr"] += 0.01
            res.write_text(json.dumps(j, ensure_ascii=False), encoding="utf-8")
            kf0 = f0(M, res, reward, sorted(test_refs), cfg["tol"])[0]
            assert kf0["pass"] is False, kf0
            out["K_F0_branch"] = {"pass": kf0["pass"], "why": kf0.get("why")}
        finally:
            os.environ.pop("B_F1_JOB_SHA256", None)
            for k, v in keep.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v

    G = {"per_image_cider_x100": {"mbr": [1.0]}, "D_cider_x100_mean_lo_hi": {"mbr": [2.0, 1.0, 3.0]},
         "dCHAIR_i_points": {"mbr": -0.5}}
    bad = s1_rows({"expect": {"D_MBR": [2.0, 1.0, 3.0], "dCHAIR_i": -0.5, "decimals": {"D_MBR": 4, "dCHAIR_i": 3}},
                   "s1_results": {"mbr": "x"}}, G, {"mbr": np.array([1.0])}, {"mbr": [2.0, 1.0, 3.0 + 1e-9]},
                  {"mbr": -0.5}, {"picks_equal": True, "bytes_equal": True})
    assert [r["ok"] for r in bad] == [True, False, True, True, True, True, True], bad
    out["K_SC_branch"] = {"rows": bad, "all_ok": all(r["ok"] for r in bad)}

    ids = [str(k) for k in range(80)]
    gold = {i: {objs[k % len(objs)], objs[(k + 1) % len(objs)]} for k, i in enumerate(ids)}
    full = {i: " ".join(sorted(gold[i])) for i in ids}

    def res_of(cider: float, chair: float) -> dict:
        return {"results": [{"tokenization": "word-level", "segmenter": "rdrsegmenter",
                             "scores_scaled_x100": {"CIDEr": cider, "BLEU-4": cider / 4}}],
                "chair": {"CHAIR_i": chair / 100, "mentions_per_caption": 2.0}}

    branches = {}
    base = rng.normal(120, 10, len(ids))
    for label, shift, noise, chair, mbr_caps, want in (
            ("PASS, K2 quiet, K3 quiet, predictions inside", 2.0, 0.5, 20.2, full, ("PASS", False, False)),
            ("INCONCLUSIVE, K2 fires", 0.3, 12.0, 21.5, full, ("INCONCLUSIVE", True, False)),
            ("FAIL, K3 fires", -1.5, 0.5, 20.0, {i: sorted(gold[i])[0] if k % 2 else "đường" for k, i in enumerate(ids)},
             ("FAIL", False, True))):
        z = rng.normal(0, 1, len(ids))
        per = {"s42": base, "s43": base + 1, "s44": base - 1, "mbr": base + shift + noise * (z - z.mean())}
        res = {s: res_of(float(per[s].mean()), 20.0) for s in SEEDS} | {"mbr": res_of(float(per["mbr"].mean()), chair)}
        caps = {s: full for s in SEEDS} | {"mbr": mbr_caps}
        st = statistics(P, cfg, M, per, res, caps, gold, ids, ids[::2])
        got = (st["primary"]["verdict"], st["K2"]["fires"], st["K3"]["fires"])
        assert got == want, (label, got, st["primary"], st["K3"])
        branches[label] = {"verdict": got[0], "K2": st["K2"]["reported_as"], "K3": st["K3"]["reported_as"],
                           "D": st["primary"]["D_MBR_x100_mean_lo_hi"], "dF1": st["K3"]["dF1_ktvic5_mean_lo_hi"],
                           "dCHAIR_i": st["K2"]["dCHAIR_i_points"], "predictions_inside": st["prediction_check"]["inside"],
                           "objects": st["objects"]["status"]}
    assert branches["PASS, K2 quiet, K3 quiet, predictions inside"]["predictions_inside"]["dCIDEr"] is True
    assert branches["FAIL, K3 fires"]["predictions_inside"]["dCIDEr"] is False
    allowed = statistics(P, cfg | {"object_claims_allowed": True}, M, per, res, caps, gold, ids, ids[::2])["objects"]
    assert allowed["status"] == "may enter a claim" and branches["FAIL, K3 fires"]["objects"] == "descriptive only"
    out["verdict_branches"] = branches | {"object rule with both PD-2 parts registered (counterfactual)": allowed}
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=("gate", "dryrun", "run", "check", "stamp"))
    ap.add_argument("out", help="the output JSON (gate, dryrun, run, check) or the decode folder (stamp)")
    ap.add_argument("name", nargs="?")
    ap.add_argument("member", nargs="?")
    ap.add_argument("--gate", help="run: the committed output of gate")
    ap.add_argument("--outputs", help="run: the mirrored decode folder of the job")
    ap.add_argument("--view", type=Path, help="check, stamp: the caption-free view of test_data.json")
    ap.add_argument("--check", type=Path, help="stamp: the check.json this job wrote before decoding")
    a = ap.parse_args()
    if a.mode == "stamp":
        P = json.loads(pinned(*PREREG))
        return 0 if stamp(Path(a.out), a.name, a.member, a.view, a.check, P["decode"]["base"]["id"]) else 1
    if Path(a.out).exists() or (a.mode == "run" and not (a.gate and a.outputs)):
        raise SystemExit("REFUSED: OUT exists (never overwritten), or run lacks --gate/--outputs")
    P, cfg = load()
    if a.mode == "check":
        return check(P, Path(a.out), a.view)
    head = {"id": P["prereg_id"], "mode": a.mode, "prereg": dict(zip(("path", "sha256"), PREREG)),
            "script_sha256": sha(HERE.read_bytes()), "config": cfg, "env": env()}
    if a.mode == "gate":
        M = modules()
        from rl_reward import Segmenter
        body = gate_body(P, cfg, M, Segmenter())
    else:
        body = dryrun(P, cfg) if a.mode == "dryrun" else run(P, cfg, a)
    with open(a.out, "x", encoding="utf-8") as f:  # "x": an existing output is never overwritten
        json.dump(head | body | {"inputs_sha256": dict(sorted(SEEN.items()))}, f, ensure_ascii=False, indent=1,
                  default=lambda o: o.item())
    print(json.dumps({"mode": a.mode, "all_pass": body.get("all_pass"),
                      "verdict": body.get("primary", {}).get("verdict") if a.mode == "run" else None}))
    return 0 if body.get("all_pass", True) and not body.get("K_F0_fired") else 1


if __name__ == "__main__":
    sys.exit(main())
