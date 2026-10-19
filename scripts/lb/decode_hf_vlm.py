#!/usr/bin/env python3
"""LB generic decoder (A-N2, Paper A; B-N1, Paper B): zero-shot captions from an open, HF-native VLM through
AutoProcessor + AutoModelForImageTextToText and the model's own chat template, for one run of a registration JSON.

Every setting comes from the registration (--prereg): the model registry (hub id @ revision, dtype, attention, batch
size, processor kwargs, the hash of every snapshot file), the run (model, set, prompt mode), the new tokens per prompt
mode, the prompt (scripts/evaluate.py PROMPTS, sha-checked) and the image set (a sha-pinned manifest of image id, file
and image sha256, in registered order). Greedy: do_sample=False, num_beams=1; every other generation setting comes
from the snapshot's generation_config.json and is recorded. trust_remote_code is always False. The registration pins
this file (decoder.sha256); a run refuses to start if the decoder's own sha256 differs (KD).

  python decode_hf_vlm.py --selftest [--prereg P]          CPU: pins, slices, resume, schema; tiny random model
  python decode_hf_vlm.py --prereg P --models               model keys, in queue order
  python decode_hf_vlm.py --prereg P --list-runs [--model K]
  python decode_hf_vlm.py --prereg P --fetch K --snapshot DIR          download the pinned files (network)
  python decode_hf_vlm.py --prereg P --check-snapshot K --snapshot DIR
  python decode_hf_vlm.py --prereg P --run-id R --snapshot DIR --out-dir DIR
        writes <out-dir>/<R>.preds.json and its .sha256 sidecar

Batches are fixed slices of the manifest order (slice k = items[kB:(k+1)B], B = the model's registered batch size),
so an image is always decoded with the same neighbours. Resumable: each finished slice is one fsynced line of
<output>.partial.jsonl; a restart skips finished slices (same run key only) and drops a torn last line. Slice 0 is
also decoded at batch size 1 and the number of identical captions is recorded (harness parity; no gate).
Images: $NCS_DATA/datasets/<image_dir>/<file>, each checked against the manifest sha256 before it is decoded.
Environment: VSPS_MACHINE_ID, VSPS_JOB_SHA256 and VSPS_VENV_FREEZE_SHA256 (set by the job).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "scripts/evaluate.py").exists())
sys.path[:0] = [str(ROOT), str(ROOT / "scripts/g2b")]
from decode_qwen3vl import prompt_text, sha256_file, utc  # noqa: E402  pinned G2-B helpers, reused unchanged

SCHEMA = "vsps.lb_decode.v1"
PREREG_SCHEMA = "vsps.lb_prereg.v1"
DATA = Path(os.environ.get("NCS_DATA", "/root/ncs-data"))
PROV_FIELDS = ("schema", "prereg_id", "prereg_sha256", "decoder_sha256", "run_id", "model", "hub_id", "revision",
               "dataset", "prompt_mode", "prompt_text_sha256", "manifest_sha256", "max_new_tokens", "batch_size",
               "dtype", "attn_implementation", "processor_kwargs", "generation_config", "machine_id", "git_head",
               "git_dirty", "job_sha256", "venv_freeze_sha256", "packages", "n_images", "parity_slice0", "resumed",
               "started_utc", "finished_utc")


def quiet(*_a, **_k) -> None:
    pass


# ------------------------------------------------------------------------------------------------ registration
def load_prereg(path: Path) -> dict:
    reg = json.loads(Path(path).read_text(encoding="utf-8"))
    if reg.get("schema") != PREREG_SCHEMA:
        raise SystemExit(f"{path}: not an LB registration")
    ids = [r["run_id"] for r in reg["runs"]]
    if len(ids) != len(set(ids)):
        raise SystemExit(f"{path}: duplicate run ids")
    for r in reg["runs"]:
        if r["model"] not in reg["models"] or r["dataset"] not in reg["datasets"] \
                or r["prompt_mode"] not in reg["decode"]["max_new_tokens"]:
            raise SystemExit(f"{path}: run {r['run_id']} names an unregistered model, set or prompt mode")
    for mode in {r["prompt_mode"] for r in reg["runs"]}:
        prompt_text(reg, mode)
    return reg


def run_spec(reg: dict, run_id: str) -> dict:
    for r in reg["runs"]:
        if r["run_id"] == run_id:
            return r
    raise SystemExit(f"{run_id}: not a registered run")


def git_blob_sha1(path: Path) -> str:
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def check_snapshot(model: dict, snapshot: Path) -> int:
    """Every pinned file exists in the snapshot with its registered hash (LFS files: sha256; others: git blob sha1)."""
    bad = []
    for rel, pin in model["files"].items():
        p = Path(snapshot) / rel
        got = None if not p.is_file() else sha256_file(p) if pin["kind"] == "sha256" else git_blob_sha1(p)
        if got != pin["hash"]:
            bad.append(rel)
    if bad:
        raise SystemExit(f"{snapshot}: {len(bad)} pinned file(s) missing or changed, e.g. {bad[:3]}")
    return len(model["files"])


def manifest_items(reg: dict, ds: str) -> list[tuple[str, str, str]]:
    """[(image id, file, image sha256)] of a set in registered order, from its sha-pinned manifest (TSV)."""
    spec = reg["datasets"][ds]
    path = ROOT / spec["manifest"]["path"]
    if sha256_file(path) != spec["manifest"]["sha256"]:
        raise SystemExit(f"{path}: sha256 differs from the registration")
    rows = [tuple(line.split("\t")) for line in path.read_text(encoding="utf-8").splitlines()]
    if len(rows) != spec["n_images"] or len({r[0] for r in rows}) != len(rows) or any(len(r) != 3 for r in rows):
        raise SystemExit(f"{path}: not {spec['n_images']} distinct (id, file, sha256) rows")
    return rows


# ------------------------------------------------------------------------------------------------ decoding loop
def slices(items: list, b: int) -> list[list]:
    return [items[k:k + b] for k in range(0, len(items), b)]


def run_key(reg_sha: str, run: dict, model: dict, kwargs: dict, prompt: str, items: list) -> str:
    return hashlib.sha256(json.dumps([reg_sha, run, model, kwargs, prompt, items], sort_keys=True).encode()).hexdigest()


def open_partial(part: Path, key: str) -> dict[int, list[dict]]:
    """Finished slices of a partial file; a torn last line (a crash during its write) is dropped."""
    if not part.exists():
        part.write_text(json.dumps({"run_key": key}) + "\n", encoding="utf-8")
        return {}
    lines = part.read_text(encoding="utf-8").splitlines()
    if not lines or json.loads(lines[0]).get("run_key") != key:
        raise SystemExit(f"{part} belongs to another configuration; move it away to restart")
    done: dict[int, list[dict]] = {}
    for n, line in enumerate(lines[1:], 1):
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            if n != len(lines) - 1:
                raise SystemExit(f"{part}: corrupt line {n}") from None
            part.write_text("\n".join(lines[:n]) + "\n", encoding="utf-8")
            break
        done[rec["slice"]] = rec["rows"]
    return done


def decode_slices(items, batch: int, generate, part: Path, key: str, log=print) -> list[dict]:
    """generate([(id, file, sha)]) -> [(caption, n_tokens, hit_max)]; one fsynced partial line per finished slice."""
    done = open_partial(part, key)
    sl = slices(items, batch)
    with part.open("a", encoding="utf-8") as fh:
        for k, s in enumerate(sl):
            if k in done:
                if [r["image_id"] for r in done[k]] != [i for i, _, _ in s]:
                    raise SystemExit(f"{part}: slice {k} holds other images")
                continue
            rows = [{"image_id": i, "image_file": f, "image_sha256": h, "caption": c, "n_tokens": n, "hit_max": m}
                    for (i, f, h), (c, n, m) in zip(s, generate(s), strict=True)]
            fh.write(json.dumps({"slice": k, "rows": rows}, ensure_ascii=False) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
            done[k] = rows
            log(f"slice {k + 1}/{len(sl)}", flush=True)
    return [r for k in range(len(sl)) for r in done[k]]


def validate_output(text: str) -> None:
    d = json.loads(text)
    caps = d.get("predictions", {})
    missing = [k for k in PROV_FIELDS if k not in d]
    ok = all(isinstance(c, str) for c in caps.values())
    if missing or not ok or len(caps) != d.get("n_images") or d.get("schema") != SCHEMA:
        raise SystemExit(f"output fails its schema: missing {missing}, captions ok {ok}, n {len(caps)}")


def write_output(out: Path, prov: dict, rows: list[dict]) -> None:
    body = {**prov, **{k: {r["image_id"]: r[src] for r in rows} for k, src in (
        ("predictions", "caption"), ("image_sha256", "image_sha256"), ("n_tokens", "n_tokens"), ("hit_max", "hit_max"))}}
    text = json.dumps(body, ensure_ascii=False, indent=1) + "\n"
    validate_output(text)
    tmp = out.with_name(out.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(out)
    Path(str(out) + ".sha256").write_text(f"{sha256_file(out)}  {out.name}\n", encoding="utf-8")


# ------------------------------------------------------------------------------------------------ model
def load(model: dict, snapshot: Path, device: str):
    import torch
    import transformers
    from rescap.vlm.base import dtype_kwarg

    proc = transformers.AutoProcessor.from_pretrained(snapshot, trust_remote_code=False, **model["processor_kwargs"])
    proc.tokenizer.padding_side = "left"
    extra = {} if device == "cpu" else {"device_map": {"": device}}
    net = transformers.AutoModelForImageTextToText.from_pretrained(
        snapshot, trust_remote_code=False, attn_implementation=model["attn_implementation"],
        **dtype_kwarg(getattr(torch, model["dtype"])), **extra).eval()
    return proc, net


def make_generate(proc, net, prompt: str, n_new: int, folder: Path):
    import torch
    from PIL import Image

    eos = net.generation_config.eos_token_id
    eos = set(eos if isinstance(eos, list) else [eos])

    def generate(sl, texts=None):
        imgs = []
        for _i, f, h in sl:
            if sha256_file(folder / f) != h:
                raise SystemExit(f"{folder / f}: sha256 differs from the manifest")
            imgs.append(Image.open(folder / f).convert("RGB"))
        msgs = [[{"role": "user", "content": [{"type": "image", "image": im}, {"type": "text", "text": t}]}]
                for im, t in zip(imgs, texts or [prompt] * len(imgs), strict=True)]
        enc = proc.apply_chat_template(msgs, add_generation_prompt=True, tokenize=True, return_dict=True,
                                       return_tensors="pt", padding=True).to(net.device, net.dtype)
        with torch.no_grad():
            ids = net.generate(**enc, max_new_tokens=n_new, do_sample=False, num_beams=1)
        out = []
        for row in ids[:, enc["input_ids"].shape[1]:].tolist():
            n = next((k + 1 for k, t in enumerate(row) if t in eos), None)
            out.append((proc.decode(row[:n or len(row)], skip_special_tokens=True).strip(), n or len(row), n is None))
        return out

    return generate


# ------------------------------------------------------------------------------------------------ GPU run
def packages() -> dict:
    import accelerate
    import torch
    import torchvision
    import transformers
    return {"torch": torch.__version__, "torchvision": torchvision.__version__,
            "transformers": transformers.__version__, "accelerate": accelerate.__version__}


def git(*a) -> str | None:
    r = subprocess.run(["git", "--no-optional-locks", "-C", str(ROOT), *a], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def fetch(reg: dict, key: str, snapshot: Path) -> None:
    from huggingface_hub import snapshot_download

    m = reg["models"][key]
    snapshot_download(m["hub_id"], revision=m["revision"], local_dir=snapshot, allow_patterns=sorted(m["files"]))
    print(f"{key}: {check_snapshot(m, snapshot)} pinned files ok")


def decode_run(reg: dict, reg_path: Path, run_id: str, snapshot: Path, out_dir: Path) -> None:
    import torch

    started = utc()
    if sha256_file(Path(__file__)) != reg["decoder"]["sha256"]:
        raise SystemExit("this decoder's sha256 differs from the registration's decoder pin (KD)")
    run = run_spec(reg, run_id)
    m = reg["models"][run["model"]]
    if packages() != reg["venv"]["packages"]:
        raise SystemExit(f"package versions {packages()} differ from the registration (KD)")
    check_snapshot(m, snapshot)
    prompt = prompt_text(reg, run["prompt_mode"])
    n_new = reg["decode"]["max_new_tokens"][run["prompt_mode"]]
    items = manifest_items(reg, run["dataset"])
    proc, net = load(m, snapshot, "cuda:0")
    gen = make_generate(proc, net, prompt, n_new, DATA / "datasets" / reg["datasets"][run["dataset"]]["image_dir"])
    out = out_dir / f"{run_id}.preds.json"
    part = Path(str(out) + ".partial.jsonl")
    resumed = part.exists()
    kw = {"max_new_tokens": n_new, "do_sample": False, "num_beams": 1}
    rows = decode_slices(items, m["batch_size"], gen, part, run_key(sha256_file(reg_path), run, m, kw, prompt, items))
    solo = [gen([it])[0][0] for it in items[:m["batch_size"]]] if m["batch_size"] > 1 else []
    status = git("status", "--porcelain", "--untracked-files=no")
    prov = {"schema": SCHEMA, "prereg_id": reg["prereg_id"], "prereg_sha256": sha256_file(reg_path),
            "decoder_sha256": sha256_file(Path(__file__)), "run_id": run_id, "model": run["model"],
            "hub_id": m["hub_id"], "revision": m["revision"], "dataset": run["dataset"],
            "prompt_mode": run["prompt_mode"], "prompt_text_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            "manifest_sha256": reg["datasets"][run["dataset"]]["manifest"]["sha256"], "max_new_tokens": n_new,
            "batch_size": m["batch_size"], "dtype": m["dtype"], "attn_implementation": m["attn_implementation"],
            "processor_kwargs": m["processor_kwargs"], "generation_config": net.generation_config.to_diff_dict(),
            "machine_id": os.environ.get("VSPS_MACHINE_ID"), "git_head": git("rev-parse", "HEAD"),
            "git_dirty": None if status is None else bool(status), "job_sha256": os.environ.get("VSPS_JOB_SHA256"),
            "venv_freeze_sha256": os.environ.get("VSPS_VENV_FREEZE_SHA256"), "packages": packages(),
            "n_images": len(items), "resumed": resumed, "started_utc": started, "finished_utc": utc(),
            "parity_slice0": {"n": len(solo), "identical": sum(a == r["caption"] for a, r in zip(solo, rows))},
            "gpu": torch.cuda.get_device_name(0), "cuda": torch.version.cuda, "generate_kwargs": kw}
    write_output(out, prov, rows)
    print(f"wrote {out}")


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def selftest(reg_path: Path | None) -> None:
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

    if reg_path:
        reg = load_prereg(reg_path)
        check("registration: runs, prompts (sha vs evaluate.py), models and sets consistent", bool(reg["runs"]))
        check("registration: every model pinned to a 40-hex revision with file hashes, no remote code",
              all(len(m["revision"]) == 40 and m["files"] and not m.get("trust_remote_code")
                  for m in reg["models"].values()))
        check("registration: its decoder pin equals this file's sha256",
              sha256_file(Path(__file__)) == reg["decoder"]["sha256"])
    en = "Describe this image in detail in English."
    check("prompt read from scripts/evaluate.py PROMPTS", prompt_text(
        {"decode": {"prompts": {"detailed_en": {"text_sha256": hashlib.sha256(en.encode()).hexdigest()}}}},
        "detailed_en") == en)
    refused("a changed prompt is refused",
            lambda: prompt_text({"decode": {"prompts": {"short": {"text_sha256": "0" * 64}}}}, "short"))
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        (t / "e").write_bytes(b"")
        check("git blob sha1 of the empty blob", git_blob_sha1(t / "e") == "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391")
        (t / "s").mkdir()
        (t / "s/a.json").write_text("{}")
        (t / "s/w.safetensors").write_bytes(b"x" * 9)
        mod = {"files": {"a.json": {"kind": "git_blob", "hash": git_blob_sha1(t / "s/a.json")},
                         "w.safetensors": {"kind": "sha256", "hash": sha256_file(t / "s/w.safetensors")}}}
        check("snapshot pins pass", check_snapshot(mod, t / "s") == 2)
        (t / "s/w.safetensors").write_bytes(b"y" * 9)
        refused("snapshot check catches a changed weight file", lambda: check_snapshot(mod, t / "s"))
        items = [(str(i), f"{i}.jpg", "h") for i in range(7)]
        check("fixed slices 3+3+1", [len(s) for s in slices(items, 3)] == [3, 3, 1])
        calls: list = []

        def gen(sl):
            calls.append([i for i, _, _ in sl])
            return [(f"cap {i}", 3, False) for i, _, _ in sl]

        one = decode_slices(items, 3, gen, t / "a.partial.jsonl", "k", log=quiet)

        def gen_stop(sl):
            if sl[0][0] == "3":
                raise KeyboardInterrupt
            return gen(sl)

        part = t / "b.partial.jsonl"
        try:
            decode_slices(items, 3, gen_stop, part, "k", log=quiet)
        except KeyboardInterrupt:
            pass
        with part.open("a") as fh:
            fh.write('{"slice": 1, "ro')
        calls.clear()
        two = decode_slices(items, 3, gen, part, "k", log=quiet)
        check("interrupted + resumed run equals one pass; torn line dropped; finished slices not re-decoded",
              two == one and calls == [["3", "4", "5"], ["6"]])
        refused("a foreign partial file is refused", lambda: open_partial(part, "other"))
        prov = {k: None for k in PROV_FIELDS} | {"schema": SCHEMA, "n_images": len(items)}
        write_output(t / "x.preds.json", prov, one)
        check("output schema and sha256 sidecar", (t / "x.preds.json.sha256").read_text().split()[0]
              == sha256_file(t / "x.preds.json"))
        refused("schema rejects a missing caption", lambda: validate_output(json.dumps(prov | {"predictions": {}})))
    try:
        import torch  # noqa: F401
        import transformers  # noqa: F401
    except ImportError:
        print("\n".join("PASS " + n for n in ok) + "\nSKIP tiny model: torch/transformers not installed")
        return
    ok += selftest_tiny()
    print("\n".join("PASS " + n for n in ok) + "\nselftest ok")


def selftest_tiny() -> list[str]:
    """A tiny random LLaVA saved to disk and loaded through the real path (Auto classes, chat template, decode)."""
    import torch
    import transformers as tf
    from PIL import Image
    from tokenizers import Tokenizer, models, pre_tokenizers

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
    out = []
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        net = tf.LlavaForConditionalGeneration(cfg)
        net.generation_config.pad_token_id, net.generation_config.eos_token_id = 1, 3
        net.save_pretrained(t / "snap")
        proc.save_pretrained(t / "snap")
        spec = {"processor_kwargs": {}, "attn_implementation": "sdpa", "dtype": "float32"}
        p2, n2 = load(spec, t / "snap", "cpu")
        if type(n2).__name__ != "LlavaForConditionalGeneration" or p2.tokenizer.padding_side != "left":
            raise AssertionError("Auto classes did not resolve the saved tiny LLaVA with left padding")
        out.append("tiny LLaVA loads through AutoProcessor + AutoModelForImageTextToText (left padding)")
        (t / "img").mkdir()
        items = []
        for i in range(5):
            Image.new("RGB", (40 + 9 * i, 30 + 5 * i), (50 * i, 120, 200 - 40 * i)).save(t / f"img/{i}.png")
            items.append((str(i), f"{i}.png", sha256_file(t / f"img/{i}.png")))
        gen = make_generate(p2, n2, "w5 w6 w7", 6, t / "img")
        solo = [gen([it])[0] for it in items]
        batched = decode_slices(items, 3, gen, t / "r.partial.jsonl", "k", log=quiet)
        if [(r["caption"], r["n_tokens"], r["hit_max"]) for r in batched] != solo or not any(c for c, _, _ in solo):
            raise AssertionError("greedy batch 3 differs from batch 1")
        out.append("greedy: fixed slices of 3 (3+2) give the batch-1 captions, token counts and truncation flags")
        texts = ["w9", "w9 w10 w11 w12 w13", "w14 w15"]
        if gen(items[:3], texts) != [gen([it], [x])[0] for it, x in zip(items[:3], texts)]:
            raise AssertionError("left-padded batch differs from batch 1")
        out.append("greedy: a left-padded batch (prompts of 1, 5 and 2 words) gives the batch-1 captions")
        if gen(items[:3]) != gen(items[:3]):
            raise AssertionError("greedy decoding not deterministic")
        out.append("greedy decoding is deterministic")
        bad = [(items[0][0], items[0][1], "0" * 64)]
        try:
            gen(bad)
            raise AssertionError("a changed image was decoded")
        except SystemExit:
            out.append("an image whose sha256 differs from the manifest is refused")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--prereg", type=Path)
    ap.add_argument("--models", action="store_true")
    ap.add_argument("--list-runs", action="store_true")
    ap.add_argument("--model")
    ap.add_argument("--fetch")
    ap.add_argument("--check-snapshot")
    ap.add_argument("--run-id")
    ap.add_argument("--snapshot", type=Path)
    ap.add_argument("--out-dir", type=Path)
    a = ap.parse_args()
    if a.selftest:
        return selftest(a.prereg)
    if not a.prereg:
        ap.error("--prereg is required")
    reg = load_prereg(a.prereg)
    if a.models:
        print("\n".join(reg["models"]))
    elif a.list_runs:
        print("\n".join(r["run_id"] for r in reg["runs"] if a.model in (None, r["model"])))
    elif a.fetch:
        fetch(reg, a.fetch, a.snapshot)
    elif a.check_snapshot:
        print(f"{a.check_snapshot}: {check_snapshot(reg['models'][a.check_snapshot], a.snapshot)} pinned files ok")
    elif a.run_id:
        decode_run(reg, a.prereg, a.run_id, a.snapshot, a.out_dir)
    else:
        ap.error("choose --selftest, --models, --list-runs, --fetch, --check-snapshot or --run-id")


if __name__ == "__main__":
    main()
