#!/usr/bin/env python3
"""Dev-only zero-shot candidate pools (PD-31; design note manuscript/prereg/2026-10-21_dev_pools/DESIGN.md).
EXPLORATORY / DEV: no registered claim may be made from these pools without a prereg.

Models, revisions, per-file snapshot pins, venv, processor kwargs, batch size, prompts (sha-checked against
scripts/evaluate.py PROMPTS) and new tokens are read from the committed B-N1 registration (PINS below); loading,
batching, resume and the greedy call are the committed LB decoder's (scripts/lb/decode_hf_vlm.py), imported unchanged.
Added here: the sampled pools (N per image at each T) with a per-image seed, the dev manifests and the test-set refusal.

  python scripts/dev_pools/generate.py --selftest                 CPU: pins, runs, refusal, seeds, resume, schema
  python scripts/dev_pools/generate.py --list-runs [--dataset D]
  python scripts/dev_pools/generate.py --check-inputs --model K --snapshot DIR
  python scripts/dev_pools/generate.py --run-id R --snapshot DIR --out-dir DIR
        greedy: <R>.preds.json; sampled: <R>.samples.jsonl; each with a <file>.sha256 sidecar
Images: $NCS_DATA/datasets/<image_dir>/<file>, each checked against its manifest sha256 and refused if it is in the
exclusion list (any registered or used test set). Environment: VSPS_MACHINE_ID, VSPS_JOB_SHA256, VSPS_VENV_FREEZE_SHA256.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import socket
import sys
import tempfile
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "scripts/evaluate.py").exists())
sys.path[:0] = [str(ROOT), str(ROOT / "scripts/lb")]
import decode_hf_vlm as lb  # noqa: E402  committed LB decoder (pinned by the B-N1 registration), reused unchanged

SCHEMA = "vsps.dev_pools.v1"
LABEL = "EXPLORATORY / DEV"
DESIGN_DIR = "manuscript/prereg/2026-10-21_dev_pools"
PINS = {  # path -> sha256; every input this generator reads from the repo
    "manuscript/prereg/2026-10-19_b_n1_vi_leaderboard.json": "9ff02dc259258de1add426abd02131f2122e3476a81f9a076066ed6d74906134",
    "scripts/lb/decode_hf_vlm.py": "e2de18811e2ffeb61ed72cb2399d41123e9a8f6ccd73a5ec35f778dcbe2f5ac4",
    f"{DESIGN_DIR}/exclusion.json": "c52a96d18925b974878ae1a970c3f9133fb3482216676fd41871eeabb68cc77f",
    f"{DESIGN_DIR}/ktvic_dev299.tsv": "a4ac7fdbd904f2205845705f5235b9748225a83a07854b58e59a755b85e4186e",
    f"{DESIGN_DIR}/uitviic_val.tsv": "338252e13c7cc8e51c579ea7f0a81f96919bb1aebe499ce90a8e7c370742e5a4",
}
B_N1 = "manuscript/prereg/2026-10-19_b_n1_vi_leaderboard.json"
MODELS = ("qwen25vl_7b", "qwen3vl_8b")
MODES = ("short", "detailed")
DATASETS = {  # name -> manifest, image folder under $NCS_DATA/datasets, id namespace, n images
    "ktvic_dev299": {"manifest": f"{DESIGN_DIR}/ktvic_dev299.tsv", "image_dir": "ktvic/images", "ns": "ktvic", "n": 299},
    "uitviic_val": {"manifest": f"{DESIGN_DIR}/uitviic_val.tsv", "image_dir": "uitviic/images", "ns": "coco", "n": 924},
}
SAMPLING = {"n": 8, "temperatures": (0.7, 1.0), "top_p": 0.95, "top_k": 0, "seed": 42}  # top_p/top_k: e5_sample, G2-B


def pinned(rel: str) -> Path:
    p = ROOT / rel
    if lb.sha256_file(p) != PINS[rel]:
        raise SystemExit(f"{rel}: sha256 differs from the pin in {Path(__file__).name}")
    return p


def registration() -> dict:
    pinned("scripts/lb/decode_hf_vlm.py")
    return lb.load_prereg(pinned(B_N1))


def runs(dataset: str | None = None) -> list[dict]:
    """Per (dataset, model, prompt): greedy, then N samples at each T."""
    out = []
    for ds in DATASETS if dataset is None else (dataset,):
        for m in MODELS:
            for mode in MODES:
                out.append({"run_id": f"dp_{m}_{ds}-{mode}-T0", "dataset": ds, "model": m, "prompt_mode": mode,
                            "temperature": 0.0, "n": 1})
                for t in SAMPLING["temperatures"]:
                    out.append({"run_id": f"dp_{m}_{ds}-{mode}-T{t:.1f}x{SAMPLING['n']}".replace(".", ""),
                                "dataset": ds, "model": m, "prompt_mode": mode, "temperature": t, "n": SAMPLING["n"]})
    return out


def run_spec(run_id: str) -> dict:
    for r in runs():
        if r["run_id"] == run_id:
            return r
    raise SystemExit(f"{run_id}: not a dev-pool run")


def image_seed(run: dict, image_id: str) -> int:
    """Seed of one image's samples: independent of order, batching and resume."""
    key = f"{SAMPLING['seed']}|{run['model']}|{run['prompt_mode']}|{run['temperature']}|{run['dataset']}|{image_id}"
    return int(hashlib.sha256(key.encode()).hexdigest()[:8], 16)


def generate_kwargs(reg: dict, run: dict) -> dict:
    n_new = reg["decode"]["max_new_tokens"][run["prompt_mode"]]
    if run["n"] == 1:
        return {"max_new_tokens": n_new, "do_sample": False, "num_beams": 1}
    return {"max_new_tokens": n_new, "do_sample": True, "temperature": run["temperature"], "top_p": SAMPLING["top_p"],
            "top_k": SAMPLING["top_k"], "num_return_sequences": run["n"]}


# ------------------------------------------------------------------------------------------------ images
def exclusion() -> tuple[dict[str, set[str]], set[str]]:
    ex = json.loads(pinned(f"{DESIGN_DIR}/exclusion.json").read_text(encoding="utf-8"))
    ids = {ns: {str(x) for v in sets.values() for x in v} for ns, sets in ex["ids"].items()}
    return ids, {h for v in ex["image_sha256"].values() for h in v}


def refuse_test_images(rows: list[tuple[str, str, str]], ns: str, ex_ids: dict, ex_sha: set) -> None:
    bad = [i for i, _, h in rows if i in ex_ids.get(ns, set()) or h in ex_sha]
    if bad:
        raise SystemExit(f"REFUSED: {len(bad)} test-set image(s) in the input, e.g. {bad[:3]}")


def manifest(ds: str) -> list[tuple[str, str, str]]:
    spec = DATASETS[ds]
    rows = [tuple(x.split("\t")) for x in pinned(spec["manifest"]).read_text(encoding="utf-8").splitlines()]
    if len(rows) != spec["n"] or len({r[0] for r in rows}) != len(rows) or any(len(r) != 3 for r in rows):
        raise SystemExit(f"{spec['manifest']}: not {spec['n']} distinct (id, file, sha256) rows")
    refuse_test_images(rows, spec["ns"], *exclusion())
    return rows


# ------------------------------------------------------------------------------------------------ outputs
PROV_FIELDS = ("schema", "label", "run_id", "model", "hub_id", "revision", "dataset", "manifest_sha256",
               "exclusion_sha256", "prompt_mode", "prompt_text_sha256", "max_new_tokens", "temperature",
               "sequences_per_image", "generate_kwargs", "seed_rule", "batch_size", "machine_id", "card", "git_head",
               "git_dirty", "inputs_sha256", "packages", "n_images", "started_utc", "finished_utc")


def validate(text: str, pool: bool) -> None:
    if pool:
        lines = text.splitlines()
        prov, rows = json.loads(lines[0]), [json.loads(x) for x in lines[1:]]
        ok = all(len(r["samples"]) == prov["sequences_per_image"] and all(isinstance(c, str) for c in r["samples"])
                 for r in rows)
        n = len(rows)
    else:
        prov = json.loads(text)
        ok, n = all(isinstance(c, str) for c in prov["predictions"].values()), len(prov["predictions"])
    missing = [k for k in PROV_FIELDS if k not in prov]
    if missing or not ok or n != prov["n_images"] or prov["schema"] != SCHEMA or prov["label"] != LABEL:
        raise SystemExit(f"output fails its schema: missing {missing}, captions ok {ok}, n {n}/{prov['n_images']}")


def write(out: Path, prov: dict, rows: list[dict], pool: bool) -> None:
    if pool:
        text = json.dumps(prov, ensure_ascii=False) + "\n" + "".join(json.dumps(
            {"image_id": r["image_id"], "image_sha256": r["image_sha256"], "seed": r["seed"], "samples": r["caption"],
             "n_tokens": r["n_tokens"], "hit_max": r["hit_max"]}, ensure_ascii=False) + "\n" for r in rows)
    else:
        text = json.dumps({**prov, **{k: {r["image_id"]: r[src] for r in rows} for k, src in (
            ("predictions", "caption"), ("image_sha256", "image_sha256"), ("n_tokens", "n_tokens"),
            ("hit_max", "hit_max"))}}, ensure_ascii=False, indent=1) + "\n"
    validate(text, pool)
    if out.exists():
        raise SystemExit(f"{out} exists; outputs are never overwritten")
    tmp = out.with_name(out.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(out)
    Path(str(out) + ".sha256").write_text(f"{lb.sha256_file(out)}  {out.name}\n", encoding="utf-8")


# ------------------------------------------------------------------------------------------------ GPU
def make_sampler(proc, net, prompt: str, kwargs: dict, folder: Path, run: dict):
    """One image per call, N sequences; torch seeded per image (image_seed), so resume needs no RNG state."""
    import torch
    from PIL import Image

    eos = net.generation_config.eos_token_id
    eos = set(eos if isinstance(eos, list) else [eos])

    def generate(sl):
        (i, f, h), = sl
        if lb.sha256_file(folder / f) != h:
            raise SystemExit(f"{folder / f}: sha256 differs from the manifest")
        msgs = [[{"role": "user", "content": [{"type": "image", "image": Image.open(folder / f).convert("RGB")},
                                              {"type": "text", "text": prompt}]}]]
        enc = proc.apply_chat_template(msgs, add_generation_prompt=True, tokenize=True, return_dict=True,
                                       return_tensors="pt", padding=True).to(net.device, net.dtype)
        torch.manual_seed(image_seed(run, i))
        with torch.no_grad():
            ids = net.generate(**enc, **kwargs)
        caps, toks, hit = [], [], []
        for row in ids[:, enc["input_ids"].shape[1]:].tolist():
            n = next((k + 1 for k, t in enumerate(row) if t in eos), None)
            caps.append(proc.decode(row[:n or len(row)], skip_special_tokens=True).strip())
            toks.append(n or len(row))
            hit.append(n is None)
        return [(caps, toks, hit)]

    return generate


def check_inputs(key: str, snapshot: Path) -> None:
    reg = registration()
    if lb.packages() != reg["venv"]["packages"]:
        raise SystemExit(f"package versions {lb.packages()} differ from the B-N1 venv {reg['venv']['packages']}")
    report = {"packages": lb.packages(), "snapshot_files_ok": lb.check_snapshot(reg["models"][key], snapshot)}
    for mode in MODES:
        lb.prompt_text(reg, mode)
    for ds, spec in DATASETS.items():
        folder = lb.DATA / "datasets" / spec["image_dir"]
        rows = manifest(ds)
        report[ds] = {"n": len(rows), "on_disk_sha_ok": sum(
            (folder / f).is_file() and lb.sha256_file(folder / f) == h for _, f, h in rows)}
    print(json.dumps(report, indent=1))


def decode_run(run_id: str, snapshot: Path, out_dir: Path) -> None:
    import torch

    started = lb.utc()
    reg = registration()
    run = run_spec(run_id)
    m = reg["models"][run["model"]]
    if lb.packages() != reg["venv"]["packages"]:
        raise SystemExit(f"package versions {lb.packages()} differ from the B-N1 venv (KD)")
    lb.check_snapshot(m, snapshot)
    prompt = lb.prompt_text(reg, run["prompt_mode"])
    kwargs = generate_kwargs(reg, run)
    items = manifest(run["dataset"])
    folder = lb.DATA / "datasets" / DATASETS[run["dataset"]]["image_dir"]
    pool = run["n"] > 1
    out = out_dir / f"{run_id}.{'samples.jsonl' if pool else 'preds.json'}"
    if out.exists():
        raise SystemExit(f"{out} exists; a run is decoded once")
    proc, net = lb.load(m, snapshot, "cuda:0")
    if pool:
        gen, batch = make_sampler(proc, net, prompt, kwargs, folder, run), 1
    else:
        gen, batch = lb.make_generate(proc, net, prompt, kwargs["max_new_tokens"], folder), m["batch_size"]
    part = Path(str(out) + ".partial.jsonl")
    resumed = part.exists()
    key = lb.run_key(PINS[B_N1], run, m, kwargs, prompt, items)
    rows = lb.decode_slices(items, batch, gen, part, key)
    for r in rows:
        r["seed"] = image_seed(run, r["image_id"]) if pool else None
    status = lb.git("status", "--porcelain", "--untracked-files=no")
    prov = {"schema": SCHEMA, "label": LABEL, "design": f"{DESIGN_DIR}/DESIGN.md", "run_id": run_id,
            "model": run["model"], "hub_id": m["hub_id"], "revision": m["revision"], "dataset": run["dataset"],
            "manifest_sha256": PINS[DATASETS[run["dataset"]]["manifest"]],
            "exclusion_sha256": PINS[f"{DESIGN_DIR}/exclusion.json"], "prompt_mode": run["prompt_mode"],
            "prompt_text_sha256": hashlib.sha256(prompt.encode()).hexdigest(), "max_new_tokens": kwargs["max_new_tokens"],
            "temperature": run["temperature"], "sequences_per_image": run["n"], "generate_kwargs": kwargs,
            "seed_rule": f"torch.manual_seed(int(sha256('{SAMPLING['seed']}|model|mode|T|dataset|image_id')[:8], 16)) "
                         "before each image" if pool else None,
            "batch_size": batch, "dtype": m["dtype"], "attn_implementation": m["attn_implementation"],
            "processor_kwargs": m["processor_kwargs"], "generation_config": net.generation_config.to_diff_dict(),
            "machine_id": os.environ.get("VSPS_MACHINE_ID") or socket.gethostname(),
            "card": torch.cuda.get_device_name(0), "cuda": torch.version.cuda, "git_head": lb.git("rev-parse", "HEAD"),
            "git_dirty": None if status is None else bool(status), "job_sha256": os.environ.get("VSPS_JOB_SHA256"),
            "venv_freeze_sha256": os.environ.get("VSPS_VENV_FREEZE_SHA256"),
            "generator_sha256": lb.sha256_file(Path(__file__)), "inputs_sha256": PINS, "packages": lb.packages(),
            "n_images": len(items), "resumed": resumed, "started_utc": started, "finished_utc": lb.utc()}
    write(out, prov, rows, pool)
    print(f"wrote {out}")


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def refuses(fn) -> bool:
    """True when fn() stops with SystemExit (a refusal); the refusal message is the expected outcome."""
    try:
        fn()
    except SystemExit as stop:
        return bool(str(stop))
    return False


def selftest() -> None:
    reg = registration()
    rs = runs()
    assert len(rs) == len({r["run_id"] for r in rs}) == len(DATASETS) * len(MODELS) * len(MODES) * 3
    assert {reg["decode"]["max_new_tokens"][k] for k in MODES} == {60, 160}
    assert all(k in reg["models"] for k in MODELS)
    for mode in MODES:
        assert lb.prompt_text(reg, mode)
    for r in rs:
        kw = generate_kwargs(reg, r)
        assert kw["do_sample"] == (r["n"] > 1) and kw.get("num_return_sequences", 1) == r["n"]
    for ds in DATASETS:
        manifest(ds)
    ex_ids, ex_sha = exclusion()
    for rows, ns in (([("1", "00000000001.jpg", "0" * 64)], "ktvic"),  # KTVIC test id 1
                     ([("x", "x.jpg", next(iter(ex_sha)))], "ktvic"),   # a test image's sha256
                     ([(next(iter(ex_ids["coco"])), "c.jpg", "1" * 64)], "coco")):
        assert refuses(lambda: refuse_test_images(rows, ns, ex_ids, ex_sha)), "a test-set image must be refused"
    sampled = next(r for r in rs if r["n"] > 1)
    assert image_seed(sampled, "5") == image_seed(sampled, "5") != image_seed(sampled, "6")
    assert image_seed(sampled, "5") != image_seed({**sampled, "temperature": 1.0}, "5")
    items = [(str(i), f"{i}.jpg", hashlib.sha256(str(i).encode()).hexdigest()) for i in range(4)]

    def fake(sl):
        (i, _f, _h), = sl
        rnd = image_seed(sampled, i)
        return [([f"c{i}-{rnd % (k + 7)}" for k in range(sampled["n"])], [3] * sampled["n"], [False] * sampled["n"])]

    with tempfile.TemporaryDirectory() as tmp:
        one = lb.decode_slices(items, 1, fake, Path(tmp) / "a.partial.jsonl", "k", log=lb.quiet)
        part = Path(tmp) / "b.partial.jsonl"
        lb.decode_slices(items[:2], 1, fake, part, "k", log=lb.quiet)  # an interrupted run: 2 of 4 slices
        two = lb.decode_slices(items, 1, fake, part, "k", log=lb.quiet)
        assert [r["caption"] for r in one] == [r["caption"] for r in two], "resume must give the same pool"
        for r in two:
            r["seed"] = image_seed(sampled, r["image_id"])
        prov = {k: None for k in PROV_FIELDS} | {"schema": SCHEMA, "label": LABEL, "n_images": len(items),
                                                  "sequences_per_image": sampled["n"]}
        write(Path(tmp) / "x.samples.jsonl", prov, two, pool=True)
        assert refuses(lambda: write(Path(tmp) / "x.samples.jsonl", prov, two, pool=True)), "no overwrite"
        greedy = [{**r, "caption": r["caption"][0], "n_tokens": 3, "hit_max": False} for r in two]
        write(Path(tmp) / "y.preds.json", prov | {"sequences_per_image": 1}, greedy, pool=False)
        assert (Path(tmp) / "y.preds.json.sha256").read_text().split()[0] == lb.sha256_file(Path(tmp) / "y.preds.json")
    print(f"selftest ok: {len(rs)} runs, refusal, seeds, resume, schema")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--list-runs", action="store_true")
    ap.add_argument("--dataset", choices=sorted(DATASETS))
    ap.add_argument("--check-inputs", action="store_true")
    ap.add_argument("--model", choices=MODELS)
    ap.add_argument("--run-id")
    ap.add_argument("--snapshot", type=Path)
    ap.add_argument("--out-dir", type=Path)
    a = ap.parse_args()
    if a.selftest:
        selftest()
    elif a.list_runs:
        print("\n".join(r["run_id"] for r in runs(a.dataset)))
    elif a.check_inputs and a.model and a.snapshot:
        check_inputs(a.model, a.snapshot)
    elif a.run_id and a.snapshot and a.out_dir:
        decode_run(a.run_id, a.snapshot, a.out_dir)
    else:
        ap.error("choose --selftest, --list-runs, --check-inputs --model --snapshot, or --run-id --snapshot --out-dir")


if __name__ == "__main__":
    main()
