#!/usr/bin/env python3
"""G2-B decoder: Qwen3-VL-8B-Instruct zero-shot captions for one run registered in
manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.json (Paper A Section 7.6; committed in 0932ba1).

Every setting is read from the committed prereg JSON: the run (dataset, prompt mode, temperature, captions per image),
the decoding block (pixels, dtype, attention, new tokens) and the design constants (top_p, top_k, seed). There is no
other option, so a run cannot drift from the registration.

  python scripts/g2b/decode_qwen3vl.py --selftest            CPU only: prereg, prompts, resume, output schema
  python scripts/g2b/decode_qwen3vl.py --list-runs           the registered run ids, in queue order
  python scripts/g2b/decode_qwen3vl.py --check-inputs --snapshot DIR --out-dir DIR
        package versions, the snapshot's SHA256SUMS, pinned id lists and dataset files, prompts; writes (or, if it
        exists, re-checks) <out-dir>/<set>_images.sha256 for the images every run decodes
  python scripts/g2b/decode_qwen3vl.py --run-id RUN --snapshot DIR --out-dir DIR
        writes <out-dir>/<RUN>.preds.json (one caption per image) or <RUN>.samples.jsonl (a sample pool), each with a
        <file>.sha256 sidecar

Resumable: decoded images go to <output>.partial.jsonl and are skipped on restart (same run key only). A sampled run
seeds torch once, before its first image; the CUDA generator state after each image is stored with the image, so a
resumed run continues the same random stream. Images are read from $NCS_DATA/datasets/{coco_probe/val2014, uitviic/
images, xm3600/images}. Environment: VSPS_MACHINE_ID, VSPS_JOB_SHA256 and VSPS_VENV_FREEZE_SHA256 (set by the job).
"""
from __future__ import annotations

import argparse
import ast
import base64
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PREREG = ROOT / "manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.json"
SCHEMA = "vsps.g2b_decode.v1"
DATA = Path(os.environ.get("NCS_DATA", "/root/ncs-data"))
IMAGE_DIRS = {"cv295": "coco_probe/val2014", "uv231": "uitviic/images", "xm600": "xm3600/images"}
TEST_JSON = {"uv231": "data/datasets/uitviic/test_data.json", "xm600": "data/datasets/xm3600/test_data.json"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def load_prereg(path: Path = PREREG) -> dict:
    reg = json.loads(path.read_text(encoding="utf-8"))
    if reg.get("statement") != "registered before any G2-B output":
        raise SystemExit(f"{path}: not the G2-B registration")
    return reg


def pins(reg: dict) -> dict[str, str]:
    """path -> sha256 of every file the prereg pins (instruments and data)."""
    ff = reg["frozen_files"]
    return {r["path"]: r["sha256"] for r in ff["instruments"] + ff["data"]}


def run_spec(reg: dict, run_id: str) -> dict:
    for r in reg["runs"]:
        if r["run_id"] == run_id:
            return r
    raise SystemExit(f"{run_id}: not a registered run")


def prompt_text(reg: dict, mode: str, evaluate_py: Path = ROOT / "scripts/evaluate.py") -> str:
    """PROMPTS[mode] read from scripts/evaluate.py without importing it; its sha256 must equal the prereg's."""
    tree = ast.parse(evaluate_py.read_text(encoding="utf-8"))
    table = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                 and any(getattr(t, "id", "") == "PROMPTS" for t in n.targets))
    text = table[mode]
    if hashlib.sha256(text.encode("utf-8")).hexdigest() != reg["decode"]["prompts"][mode]["text_sha256"]:
        raise SystemExit(f"prompt {mode!r} differs from the registration")
    return text


def generation_kwargs(reg: dict, run: dict) -> dict:
    """The registered generate() keywords of a run (decode.greedy / decode.sampled)."""
    n = reg["decode"]["max_new_tokens"][run["prompt_mode"]]
    if run["temperature"] == 0:
        return {"max_new_tokens": n, "do_sample": False}
    dc = reg["design_constants"]
    return {"max_new_tokens": n, "do_sample": True, "temperature": run["temperature"], "top_p": dc["top_p"]["value"],
            "top_k": dc["top_k"]["value"], "num_return_sequences": run["sequences_per_image"]}


def dataset_items(reg: dict, ds: str, data: Path = DATA, root: Path = ROOT) -> list[tuple[str, str]]:
    """[(image_id, file name)] in the registered id order; pinned files are checked against the prereg."""
    pin = pins(reg)

    def checked(rel: str, path: Path) -> Path:
        if sha256_file(path) != pin[rel]:
            raise SystemExit(f"{path}: sha256 differs from the prereg pin of {rel}")
        return path

    if ds == "cv295":
        ids = checked("data/coco_probe/probe_val2017_ids.txt", root / "data/coco_probe/probe_val2017_ids.txt")
        man = checked("data/coco_probe/manifest.json", root / "data/coco_probe/manifest.json")
        names = {str(i["cocoid"]): i["filename"] for i in json.loads(man.read_text(encoding="utf-8"))["images"]}
        return [(i, names[i]) for i in sorted(ids.read_text(encoding="utf-8").split(), key=int)]
    d = json.loads(checked(TEST_JSON[ds], data / TEST_JSON[ds].removeprefix("data/")).read_text(encoding="utf-8"))
    if ds == "uv231":
        return sorted(((str(i["id"]), i["file_name"]) for i in d["images"]), key=lambda x: int(x[0]))
    subset = checked("data/xm3600_subset.txt", root / "data/xm3600_subset.txt").read_text(encoding="utf-8").split()
    items = sorted((str(i["id"]), i["filename"]) for i in d["images"])
    if sorted(subset) != [i for i, _ in items]:
        raise SystemExit("XM3600 test_data.json ids differ from data/xm3600_subset.txt")
    return items


def image_list_path(out_dir: Path, ds: str) -> Path:
    return out_dir / f"{ds}_images.sha256"


def write_or_check_image_list(out_dir: Path, ds: str, items: list[tuple[str, str]], data: Path = DATA) -> int:
    """sha256 of every image of a set: written once, re-checked on every later call."""
    folder = data / "datasets" / IMAGE_DIRS[ds]
    text = "".join(f"{sha256_file(folder / f)}  {f}\n" for _, f in items)
    path = image_list_path(out_dir, ds)
    if path.exists():
        if path.read_text(encoding="utf-8") != text:
            raise SystemExit(f"{path}: images changed since the list was written")
    else:
        tmp = path.with_suffix(".tmp")
        tmp.write_text(text, encoding="utf-8")
        tmp.replace(path)
    return len(items)


# ------------------------------------------------------------------------------------------------ decoding loop
def run_key(reg_sha: str, run: dict, kwargs: dict, prompt: str, items: list) -> str:
    return hashlib.sha256(json.dumps([reg_sha, run, kwargs, prompt, items], sort_keys=True).encode()).hexdigest()


def open_partial(part: Path, key: str) -> list[dict]:
    if not part.exists():
        part.write_text(json.dumps({"run_key": key}) + "\n", encoding="utf-8")
        return []
    lines = part.read_text(encoding="utf-8").splitlines()
    if not lines or json.loads(lines[0]).get("run_key") != key:
        raise SystemExit(f"{part} belongs to another configuration; move it away to restart")
    return [json.loads(x) for x in lines[1:]]


def decode_items(items, image_sha, generate, part: Path, key: str, rng: dict | None, log=print) -> list[dict]:
    """items: [(id, file)]; generate(id, file) -> (captions, n_tokens); rng: {seed(), get(), set(state)} or None."""
    done = open_partial(part, key)
    got = {r["image_id"]: r for r in done}
    if rng is not None:
        if done:
            rng["set"](base64.b64decode(done[-1]["rng_after"]))
        else:
            rng["seed"]()
    with part.open("a", encoding="utf-8") as fh:
        for n, (i, f) in enumerate(items, 1):
            if i in got:
                continue
            caps, ntok = generate(i, f)
            row = {"image_id": i, "image_file": f, "image_sha256": image_sha[f], "captions": caps, "n_tokens": ntok,
                   "rng_after": base64.b64encode(rng["get"]()).decode() if rng is not None else None}
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
            got[i] = row
            if n % 25 == 0 or n == len(items):
                log(f"{n}/{len(items)} images", flush=True)
    return [got[i] for i, _ in items]


def write_output(out: Path, prov: dict, rows: list[dict], pool: bool) -> None:
    if pool:
        text = json.dumps(prov, ensure_ascii=False) + "\n" + "".join(
            json.dumps({"image_id": r["image_id"], "samples": r["captions"], "image_sha256": r["image_sha256"],
                        "n_tokens": r["n_tokens"]}, ensure_ascii=False) + "\n" for r in rows)
    else:
        body = {**prov, "predictions": {r["image_id"]: r["captions"][0] for r in rows},
                "image_sha256": {r["image_id"]: r["image_sha256"] for r in rows},
                "n_tokens": {r["image_id"]: r["n_tokens"][0] for r in rows}}
        text = json.dumps(body, ensure_ascii=False, indent=1) + "\n"
    validate_output(text, pool, prov["n_images"])
    tmp = out.with_name(out.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(out)
    Path(str(out) + ".sha256").write_text(f"{sha256_file(out)}  {out.name}\n", encoding="utf-8")


PROV_FIELDS = ("schema", "prereg_id", "run_id", "machine_id", "git_head", "hook_sha256", "job_sha256",
               "venv_freeze_sha256", "backbone", "revision", "dataset", "prompt_mode", "temperature", "top_p",
               "top_k", "seed", "max_new_tokens", "sequences_per_image", "n_images", "started_utc", "finished_utc")


def validate_output(text: str, pool: bool, n_images: int) -> None:
    if pool:
        lines = text.splitlines()
        prov, rows = json.loads(lines[0]), [json.loads(x) for x in lines[1:]]
        caps = [r["samples"] for r in rows]
        ok = all(isinstance(c, list) and len(c) == prov["sequences_per_image"] for c in caps)
    else:
        prov = json.loads(text)
        caps = list(prov["predictions"].values())
        ok = all(isinstance(c, str) for c in caps)
    missing = [k for k in PROV_FIELDS if k not in prov]
    if missing or not ok or len(caps) != n_images or prov["schema"] != SCHEMA:
        raise SystemExit(f"output fails its schema: missing {missing}, captions ok {ok}, n {len(caps)}/{n_images}")


def provenance(reg: dict, run: dict, kwargs: dict, n_images: int, started: str) -> dict:
    def git(*a):
        r = subprocess.run(["git", "--no-optional-locks", "-C", str(ROOT), *a], capture_output=True, text=True)
        return r.stdout.strip() if r.returncode == 0 else None
    hook = ROOT / "scripts/checkpoint_resume_hook.py"
    sampled = kwargs["do_sample"]
    status = git("status", "--porcelain", "--untracked-files=no")
    return {"schema": SCHEMA, "prereg_id": reg["prereg_id"], "prereg_sha256": sha256_file(PREREG),
            "decoder_sha256": sha256_file(Path(__file__)), "run_id": run["run_id"],
            "machine_id": os.environ.get("VSPS_MACHINE_ID"), "git_head": git("rev-parse", "HEAD"),
            "git_dirty": None if status is None else bool(status),
            "hook_sha256": sha256_file(hook) if hook.exists() else None,
            "job_sha256": os.environ.get("VSPS_JOB_SHA256"),
            "venv_freeze_sha256": os.environ.get("VSPS_VENV_FREEZE_SHA256"),
            "backbone": reg["model"]["hub_id"], "revision": reg["model"]["revision"], "dataset": run["dataset"],
            "prompt_mode": run["prompt_mode"], "temperature": run["temperature"],
            "top_p": kwargs.get("top_p") if sampled else None, "top_k": kwargs.get("top_k") if sampled else None,
            "seed": reg["design_constants"]["sampling_seed"]["value"] if sampled else None,
            "max_new_tokens": kwargs["max_new_tokens"], "sequences_per_image": run["sequences_per_image"],
            "n_images": n_images, "started_utc": started, "finished_utc": None, "generate_kwargs": kwargs}


# ------------------------------------------------------------------------------------------------ GPU
def check_packages(reg: dict) -> dict:
    import accelerate
    import torch
    import torchvision
    import transformers
    have = {"torch": torch.__version__, "torchvision": torchvision.__version__,
            "transformers": transformers.__version__, "accelerate": accelerate.__version__}
    want = reg["model"]["venv"]["packages"]
    if have != want:
        raise SystemExit(f"package versions {have} differ from the registration {want} (KD)")
    return have


def check_snapshot(reg: dict, snapshot: Path) -> str:
    """The snapshot's SHA256SUMS must be the pinned one (the job runs sha256sum -c on the files)."""
    cm = reg["model"]["checksum_manifest"]
    got = sha256_file(snapshot / "SHA256SUMS")
    if got != cm["sha256"]:
        raise SystemExit(f"{snapshot}/SHA256SUMS sha256 {got} differs from the pin {cm['sha256']}")
    return got


def check_inputs(reg: dict, snapshot: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    report = {"packages": check_packages(reg), "SHA256SUMS": check_snapshot(reg, snapshot), "images": {}}
    for mode in reg["decode"]["prompts"]:
        prompt_text(reg, mode)
    for ds in IMAGE_DIRS:
        report["images"][ds] = write_or_check_image_list(out_dir, ds, dataset_items(reg, ds))
    print(json.dumps(report, indent=1))


def decode_run(reg: dict, run_id: str, snapshot: Path, out_dir: Path) -> None:
    import torch
    import transformers
    from PIL import Image

    sys.path.insert(0, str(ROOT))
    from rescap.vlm.base import dtype_kwarg

    started = utc()
    run = run_spec(reg, run_id)
    check_packages(reg)
    check_snapshot(reg, snapshot)
    kwargs = generation_kwargs(reg, run)
    prompt = prompt_text(reg, run["prompt_mode"])
    items = dataset_items(reg, run["dataset"])
    listed = image_list_path(out_dir, run["dataset"])
    if not listed.exists():
        raise SystemExit(f"{listed} missing: run --check-inputs first")
    image_sha = {f: h for h, f in (line.split("  ", 1) for line in listed.read_text(encoding="utf-8").splitlines())}
    folder = DATA / "datasets" / IMAGE_DIRS[run["dataset"]]
    m = reg["model"]
    model = getattr(transformers, m["model_class"]).from_pretrained(
        snapshot, attn_implementation=m["attn_implementation"], device_map={"": 0},
        **dtype_kwarg(getattr(torch, m["dtype"])))
    model.eval()
    proc = transformers.AutoProcessor.from_pretrained(snapshot, min_pixels=m["min_pixels"], max_pixels=m["max_pixels"])
    pad = proc.tokenizer.pad_token_id
    msgs = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": prompt}]}]
    text = proc.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)

    def generate(_i, f):
        path = folder / f
        if sha256_file(path) != image_sha[f]:
            raise SystemExit(f"{path}: image changed since {listed.name}")
        inputs = proc(text=[text], images=[Image.open(path).convert("RGB")], return_tensors="pt").to(model.device)
        with torch.no_grad():
            ids = model.generate(**inputs, **kwargs)
        new = ids[:, inputs["input_ids"].shape[1]:]
        return ([c.strip() for c in proc.batch_decode(new, skip_special_tokens=True)],
                [int((row != pad).sum()) for row in new])

    rng = None
    if kwargs["do_sample"]:
        seed = reg["design_constants"]["sampling_seed"]["value"]
        rng = {"seed": lambda: torch.manual_seed(seed), "get": lambda: torch.cuda.get_rng_state().numpy().tobytes(),
               "set": lambda b: torch.cuda.set_rng_state(torch.frombuffer(bytearray(b), dtype=torch.uint8))}
    pool = run["sequences_per_image"] > 1
    out = out_dir / f"{run_id}.{'samples.jsonl' if pool else 'preds.json'}"
    part = Path(str(out) + ".partial.jsonl")
    reg_sha = sha256_file(PREREG)
    resumed = part.exists()
    rows = decode_items(items, image_sha, generate, part, run_key(reg_sha, run, kwargs, prompt, items), rng)
    prov = provenance(reg, run, kwargs, len(items), started)
    prov.update({"finished_utc": utc(), "resumed": resumed, "gpu": torch.cuda.get_device_name(0),
                 "cuda": torch.version.cuda, "packages": check_packages(reg), "snapshot_SHA256SUMS": check_snapshot(
                     reg, snapshot), "prompt_text_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
                 "image_list_sha256": sha256_file(listed)})
    write_output(out, prov, rows, pool)
    print(f"wrote {out}")


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def selftest() -> None:
    reg = load_prereg()
    ids = [r["run_id"] for r in reg["runs"]]
    assert len(ids) == len(set(ids)) == 23, "23 distinct registered runs"
    for mode in reg["decode"]["prompts"]:
        assert prompt_text(reg, mode)
    for r in reg["runs"]:
        kw = generation_kwargs(reg, r)
        assert kw["max_new_tokens"] == reg["decode"]["max_new_tokens"][r["prompt_mode"]]
        if r["temperature"] == 0:
            assert kw == {"max_new_tokens": kw["max_new_tokens"], "do_sample": False}
        else:
            for k in ("top_p", "top_k"):
                assert f"{k}={kw[k]}" in reg["decode"]["sampled"], k
            assert kw["num_return_sequences"] == r["sequences_per_image"]
    try:
        prompt_text({"decode": {"prompts": {"short": {"text_sha256": "0" * 64}}}}, "short")
        raise AssertionError("a changed prompt must be refused")
    except SystemExit:
        pass
    _selftest_resume(reg)
    print("selftest ok")


def _selftest_resume(reg: dict) -> None:
    """Interrupted + resumed decoding equals one uninterrupted pass; a foreign partial file is refused."""
    items = [(str(i), f"{i}.jpg") for i in range(5)]
    image_sha = {f: hashlib.sha256(f.encode()).hexdigest() for _, f in items}
    run = next(r for r in reg["runs"] if r["sequences_per_image"] > 1)
    state = {"s": 0}
    rng = {"seed": lambda: state.update(s=7), "get": lambda: state["s"].to_bytes(8, "big"),
           "set": lambda b: state.update(s=int.from_bytes(b, "big"))}

    def gen(i, _f):
        state["s"] = (state["s"] * 31 + 1) % 1000003
        return [f"cap {i} {state['s']} {k}" for k in range(run["sequences_per_image"])], [3] * run["sequences_per_image"]

    with tempfile.TemporaryDirectory() as tmp:
        one = decode_items(items, image_sha, gen, Path(tmp) / "a.partial.jsonl", "k", rng, log=lambda *a, **k: None)

        class Stop(Exception):
            pass

        calls = {"n": 0}

        def gen_stop(i, f):
            calls["n"] += 1
            if calls["n"] == 3:
                raise Stop
            return gen(i, f)

        part = Path(tmp) / "b.partial.jsonl"
        try:
            decode_items(items, image_sha, gen_stop, part, "k", rng, log=lambda *a, **k: None)
        except Stop:
            pass
        two = decode_items(items, image_sha, gen, part, "k", rng, log=lambda *a, **k: None)
        assert [r["captions"] for r in one] == [r["captions"] for r in two], "resume must continue the stream"
        try:
            open_partial(part, "other")
            raise AssertionError("a foreign partial file must be refused")
        except SystemExit:
            pass
        prov = {k: None for k in PROV_FIELDS} | {"schema": SCHEMA, "n_images": len(items),
                                                  "sequences_per_image": run["sequences_per_image"]}
        write_output(Path(tmp) / "x.samples.jsonl", prov, two, pool=True)
        write_output(Path(tmp) / "y.preds.json", prov | {"sequences_per_image": 1}, two, pool=False)
        assert (Path(tmp) / "y.preds.json.sha256").read_text().split()[0] == sha256_file(Path(tmp) / "y.preds.json")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--list-runs", action="store_true")
    ap.add_argument("--check-inputs", action="store_true")
    ap.add_argument("--run-id")
    ap.add_argument("--snapshot", type=Path)
    ap.add_argument("--out-dir", type=Path)
    a = ap.parse_args()
    if a.selftest:
        selftest()
    elif a.list_runs:
        print("\n".join(r["run_id"] for r in load_prereg()["runs"]))
    elif a.check_inputs:
        check_inputs(load_prereg(), a.snapshot, a.out_dir)
    elif a.run_id:
        decode_run(load_prereg(), a.run_id, a.snapshot, a.out_dir)
    else:
        ap.error("choose --selftest, --list-runs, --check-inputs or --run-id")


if __name__ == "__main__":
    main()
