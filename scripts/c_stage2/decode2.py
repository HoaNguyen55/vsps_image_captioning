#!/usr/bin/env python3
"""Paper C stage 2 (STAGE 2 / DEV-B, ONE LOOK): query embeddings, example lists and decodes of the frozen runs.
Prereg manuscript/prereg/2026-10-22_c_stage2/PREREG.md §4, §5.1-§5.2, §12 items 4-6 and 14.

  python scripts/c_stage2/decode2.py --selftest                                                     CPU, no data
  python scripts/c_stage2/decode2.py embed --set S --lists L --emb1 E1 --snapshot DIR --revision REV --out Q  GPU
  python scripts/c_stage2/decode2.py exemplars --set S --lists L --emb1 E1 --emb Q --out X                   CPU
  python scripts/c_stage2/decode2.py decode --run-ids R ... --snapshot DIR --lists L --exemplars X --out-dir D GPU
Only the stage-2 query images are embedded; the memory vectors are the stage-1 ones (emb.npz, pinned). Examples
follow build_memory.exemplars unchanged (seeds paperC|rand|<set>|<id> and paperC|fix|<set>, near cut 0.92). The
image-blind arm sends the frozen ret prompt and examples through the model's text-only path: no image is passed.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import stage2 as S2  # noqa: E402  pins, sets, refusal (checks the stage-1 shas first)

C, lb = S2.C, S2.lb
import build_memory as BM  # noqa: E402  stage-1 module, sha-checked by stage2


def load_emb1(path: Path) -> tuple[list[str], np.ndarray, dict]:
    """The stage-1 memory vectors (keys without '|'), pinned by sha256."""
    if S2.sha_file(path) != S2.EMB1_SHA256:
        raise SystemExit(f"{path}: not the stage-1 embeddings {S2.EMB1_SHA256[:8]}")
    z = np.load(path)
    keys = [str(k) for k in z["keys"]]
    mem = [n for n, k in enumerate(keys) if "|" not in k]
    return [keys[n] for n in mem], z["vecs"][mem], json.loads(str(z["meta"]))


# ------------------------------------------------------------------------------------------------ embed (GPU)
def cmd_embed(a) -> None:
    import torch
    from PIL import Image
    from transformers import AutoModel, AutoProcessor

    lists = C.load_lists(a.lists)
    rows = S2.manifest2(a.set, lists)
    S2.check_folder(a.set, lists)
    _k, _v, meta1 = load_emb1(a.emb1)
    snap = {p.name: S2.sha_file(p) for p in sorted(Path(a.snapshot).iterdir()) if p.is_file()}
    if a.revision != meta1["revision"] or snap != meta1["snapshot_sha256"]:
        raise SystemExit("SigLIP2 revision or snapshot differs from the stage-1 embeddings")
    BM.need_licence(BM.card_licence(Path(a.snapshot) / "README.md"), f"{BM.SIGLIP2} model card")
    folder = lb.DATA / "datasets" / S2.SETS[a.set]["image_dir"]
    proc = AutoProcessor.from_pretrained(a.snapshot)
    net = AutoModel.from_pretrained(a.snapshot, torch_dtype=torch.float16).eval().cuda()
    vecs = []
    for lo in range(0, len(rows), 64):  # fp16, batch 64: as stage 1
        ims = []
        for _i, f, h in rows[lo:lo + 64]:
            if S2.sha_file(folder / f) != h:
                raise SystemExit(f"{folder / f}: sha256 differs from lists.json")
            ims.append(Image.open(folder / f).convert("RGB"))
        with torch.no_grad():
            v = net.get_image_features(**proc(images=ims, return_tensors="pt").to("cuda", torch.float16)).float()
        vecs.append(torch.nn.functional.normalize(v, dim=-1).cpu().numpy())
    meta = {**{k: meta1[k] for k in ("model", "revision", "licence", "readme_sha256", "snapshot_sha256")},
            "set": a.set, "lists_sha256": S2.sha_file(a.lists), "stage1_emb_sha256": S2.EMB1_SHA256,
            "prereg_sha256": S2.PINS[S2.PREREG], "label": S2.LABEL}
    np.savez(a.out, keys=np.array([f"{a.set}|{i}" for i, _f, _h in rows]), vecs=np.concatenate(vecs),
             meta=json.dumps(meta))
    Path(str(a.out) + ".sha256").write_text(f"{S2.sha_file(Path(a.out))}  {Path(a.out).name}\n")


# ------------------------------------------------------------------------------------------------ exemplars (CPU)
def build_exemplars(ds: str, mem_keys: list[str], mem_vecs: np.ndarray, q_keys: list[str], q_vecs: np.ndarray) -> dict:
    """build_memory.exemplars on the stage-1 memory and one stage-2 set, plus the J8 dose-response tertile cuts of
    the set's nearest-eligible-cluster cosine (fixed here, before any stage-2 caption exists)."""
    ex = BM.exemplars(mem_keys + q_keys, np.concatenate([mem_vecs, q_vecs]))
    top1 = [ex["ret"][ds][k.split("|", 1)[1]][0][1] for k in q_keys]
    return {**ex, "dose_tertile_cuts": {ds: [float(x) for x in np.quantile(top1, [1 / 3, 2 / 3])]}}


def cmd_exemplars(a) -> None:
    lists = C.load_lists(a.lists)
    rows = S2.manifest2(a.set, lists)
    mk, mv, _meta1 = load_emb1(a.emb1)
    z = np.load(a.emb)
    meta = json.loads(str(z["meta"]))
    qk = [str(k) for k in z["keys"]]
    if (meta["set"], meta["lists_sha256"], meta["stage1_emb_sha256"]) != (a.set, S2.sha_file(a.lists),
                                                                           S2.EMB1_SHA256) or \
            qk != [f"{a.set}|{i}" for i, _f, _h in rows]:
        raise SystemExit(f"{a.emb}: not the {a.set} query embeddings of this lists.json")
    ex = build_exemplars(a.set, mk, mv, qk, z["vecs"])
    out = {"design_sha256": C.PINS[C.DESIGN], "lists_sha256": meta["lists_sha256"], "label": S2.LABEL,
           "c_schema": S2.SCHEMA, "prereg_sha256": S2.PINS[S2.PREREG], "set": a.set,
           "emb_sha256": {"stage1": S2.EMB1_SHA256, a.set: S2.sha_file(Path(a.emb))}, "near_cos": BM.NEAR_COS, **ex}
    Path(a.out).write_text(json.dumps(out) + "\n", encoding="utf-8")
    Path(str(a.out) + ".sha256").write_text(f"{S2.sha_file(Path(a.out))}  {Path(a.out).name}\n")
    print(json.dumps({"set": a.set, "dose_tertile_cuts": out["dose_tertile_cuts"][a.set],
                      "n_cut_images": sum(v > 0 for v in ex["n_cut"][a.set].values())}))


# ------------------------------------------------------------------------------------------------ decode (GPU)
def text_only_generate(proc, net, n_new: int):
    """C-c: the model's text-only path. The chat message holds the text alone; no image is read or passed."""
    import torch

    eos = net.generation_config.eos_token_id
    eos = set(eos if isinstance(eos, list) else [eos])

    def generate(sl, texts):
        msgs = [[{"role": "user", "content": [{"type": "text", "text": t}]}] for t in texts]
        enc = proc.apply_chat_template(msgs, add_generation_prompt=True, tokenize=True, return_dict=True,
                                       return_tensors="pt", padding=True).to(net.device)
        with torch.no_grad():
            ids = net.generate(**enc, max_new_tokens=n_new, do_sample=False, num_beams=1)
        out = []
        for row in ids[:, enc["input_ids"].shape[1]:].tolist():  # the same read-out as lb.make_generate
            n = next((k + 1 for k, t in enumerate(row) if t in eos), None)
            out.append((proc.decode(row[:n or len(row)], skip_special_tokens=True).strip(), n or len(row), n is None))
        return out

    return generate


def example_spec(s: dict) -> dict:
    """The image-blind arm shows the frozen ret examples, in the ret order."""
    return {**s, "arm": "ret"} if s["arm"] == "blind" else s


def decode_runs(run_ids: list[str], snapshot: Path, lists_path: Path, ex_path: Path, out_dir: Path) -> None:
    g = S2.grid(S2.frozen())
    missing = [r for r in run_ids if r not in g]
    if missing:
        raise SystemExit(f"{missing[0]}: not a stage-2 run")
    specs = [g[r] for r in run_ids]
    if len({(s["model"], s["dataset"]) for s in specs}) != 1:
        raise SystemExit("one model and one set per process")
    lists = C.load_lists(lists_path)
    ex = C.load_exemplars(ex_path, lists_path)
    if ex.get("set") != specs[0]["dataset"]:
        raise SystemExit(f"{ex_path}: not the example lists of {specs[0]['dataset']}")
    reg = C.registration()
    m = reg["models"][specs[0]["model"]]
    if lb.packages() != reg["venv"]["packages"]:
        raise SystemExit(f"package versions {lb.packages()} differ from the B-N1 venv")
    lb.check_snapshot(m, snapshot)
    outs = [out_dir / f"{s['run_id']}.preds.json" for s in specs]
    if any(o.exists() for o in outs):
        raise SystemExit("an output exists; a run is decoded once")
    plan = []
    for s in specs:  # every refusal before the model loads
        items = S2.manifest2(s["dataset"], lists)
        plan.append((s, items, C.check_exemplars(items, example_spec(s), ex, lists)))
    S2.check_folder(specs[0]["dataset"], lists)
    ctx = {"caps": C.memory_captions(lists), "zs": lb.prompt_text(reg, "short"), "m": m, "ex_path": ex_path,
           "n_new": reg["decode"]["max_new_tokens"]["short"]}
    ctx["proc"], ctx["net"] = lb.load(m, snapshot, "cuda:0")
    for (s, items, exids), out in zip(plan, outs):
        decode_one(s, items, exids, out, ctx)


def prompts(s: dict, items: list, exids: dict, caps: dict, zs: str) -> dict[str, str]:
    src = C.DATASETS[s["dataset"]]["src"]
    return {i: zs if s["arm"] == "zs" else C.prompt(s["tpl"], [C.shown(caps[c], src) for c in exids[i]])
            for i, _f, _h in items}


def decode_one(s: dict, items: list, exids: dict, out: Path, ctx: dict) -> None:
    import torch

    proc, net, m, zs, n_new = (ctx[k] for k in ("proc", "net", "m", "zs", "n_new"))
    started = lb.utc()
    texts = prompts(s, items, exids, ctx["caps"], zs)
    folder = lb.DATA / "datasets" / C.DATASETS[s["dataset"]]["image_dir"]
    base = text_only_generate(proc, net, n_new) if s["arm"] == "blind" else lb.make_generate(proc, net, zs, n_new,
                                                                                             folder)

    def gen(sl):
        return base(sl, [texts[i] for i, _f, _h in sl])

    kw = {"max_new_tokens": n_new, "do_sample": False, "num_beams": 1}
    tsha = {i: C.sha(t) for i, t in texts.items()}
    part = Path(str(out) + ".partial.jsonl")
    resumed = part.exists()
    key = lb.run_key(C.PINS[C.B_N1], s, m, kw, json.dumps(tsha, sort_keys=True), items)
    rows = lb.decode_slices(items, m["batch_size"], gen, part, key)
    solo = [gen([it])[0][0] for it in items[:m["batch_size"]]] if m["batch_size"] > 1 else []
    status = lb.git("status", "--porcelain", "--untracked-files=no")
    prov = {"schema": lb.SCHEMA, "c_schema": S2.SCHEMA, "label": S2.LABEL, "design": C.DESIGN,
            "design_sha256": C.PINS[C.DESIGN], "c_prereg": S2.PREREG, "c_prereg_sha256": S2.PINS[S2.PREREG],
            "frozen_config_sha256": S2.PINS[S2.FROZEN],
            "prereg_id": "B-N1 model blocks (decoder registration)", "prereg_sha256": C.PINS[C.B_N1],
            "decoder_sha256": C.PINS["scripts/lb/decode_hf_vlm.py"], "wrapper_sha256": S2.sha_file(Path(__file__)),
            "run_id": s["run_id"], "spec": s, "model": s["model"], "hub_id": m["hub_id"], "revision": m["revision"],
            "dataset": s["dataset"], "image_input": s["arm"] != "blind",
            "prompt_mode": "short" if s["arm"] == "zs" else f"icl-{s['tpl']}",
            "prompt_text_sha256": C.ZS_PROMPT_SHA256 if s["arm"] == "zs" else C.TEMPLATE_SHA256,
            "prompt_sha256_per_image": tsha, "exemplars": exids, "manifest_sha256": C.sha(json.dumps(items)),
            "lists_sha256": C.LISTS_SHA256, "exemplars_sha256": S2.sha_file(ctx["ex_path"]), "max_new_tokens": n_new,
            "batch_size": m["batch_size"], "dtype": m["dtype"], "attn_implementation": m["attn_implementation"],
            "processor_kwargs": m["processor_kwargs"], "generation_config": net.generation_config.to_diff_dict(),
            "machine_id": os.environ.get("VSPS_MACHINE_ID"), "git_head": lb.git("rev-parse", "HEAD"),
            "git_dirty": None if status is None else bool(status), "job_sha256": os.environ.get("VSPS_JOB_SHA256"),
            "venv_freeze_sha256": os.environ.get("VSPS_VENV_FREEZE_SHA256"), "packages": lb.packages(),
            "n_images": len(items), "resumed": resumed, "started_utc": started, "finished_utc": lb.utc(),
            "parity_slice0": {"n": len(solo), "identical": sum(a == r["caption"] for a, r in zip(solo, rows))},
            "gpu": torch.cuda.get_device_name(0), "cuda": torch.version.cuda, "generate_kwargs": kw}
    lb.write_output(out, prov, rows)
    print(f"wrote {out}")


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def selftest() -> None:
    import torch

    cfg = S2.frozen()
    g = S2.grid(cfg)
    # examples: build_memory.exemplars on synthetic vectors, a stage-2 set name, an XM query
    rng = np.random.default_rng(0)
    mk = [f"m{n:05d}" for n in range(12)]
    mv = rng.normal(size=(12, 16)).astype(np.float32)
    qk = ["xm_dev500|q1", "xm_dev500|q2"]
    qv = rng.normal(size=(2, 16)).astype(np.float32)
    qv[0] = mv[0] + 1e-3  # m00000 is a near copy of q1
    mv /= np.linalg.norm(mv, axis=1, keepdims=True)
    qv /= np.linalg.norm(qv, axis=1, keepdims=True)
    ex = build_exemplars("xm_dev500", mk, mv, qk, qv)
    assert "m00000" not in [c for c, _x in ex["ret"]["xm_dev500"]["q1"]] and len(ex["fix"]["xm_dev500"]) == BM.N_EX
    lo, hi = ex["dose_tertile_cuts"]["xm_dev500"]
    assert lo <= hi and ex == build_exemplars("xm_dev500", mk, mv, qk, qv), "deterministic"
    caps = {"m0": {"ktvic": "w1 w2", "openviic": "w3 w4"}, "m1": {"ktvic": "w5 w6"}}
    assert C.shown(caps["m0"], "xm3600") == "w1 w2", "an XM query gets the first member's caption"
    assert C.shown(caps["m0"], "openviic") == "w3 w4"
    # prompts: the blind arm shows the ret examples in the ret order
    ret, blind = (g[f"c2_qwen25vl_7b_ov_dev_b-{t}"] for t in ("ret-k8-first-T1", "blind-k8-first-T1"))
    assert example_spec(blind) == {**blind, "arm": "ret"} and example_spec(ret) == ret
    items = [("a", "a.jpg", "0" * 64)]
    assert prompts(ret, items, {"a": ["m1", "m0"]}, caps, "Z") == prompts(blind, items, {"a": ["m1", "m0"]}, caps, "Z")
    assert prompts(g["c2_qwen25vl_7b_ov_dev_b-zs"], items, {"a": []}, caps, "Z") == {"a": "Z"}

    # the image-blind generate passes no image to the model
    seen = []

    class Enc(dict):
        def to(self, *_a):
            return self

    class Proc:
        def apply_chat_template(self, msgs, **_k):
            seen.extend(c for m in msgs for c in m[0]["content"])
            return Enc(input_ids=torch.zeros((len(msgs), 3), dtype=torch.long))

        def decode(self, row, skip_special_tokens=True):
            return " ".join(f"w{t}" for t in row)

    class Net:
        device = "cpu"
        generation_config = type("GC", (), {"eos_token_id": 9})()

        def generate(self, input_ids, **_k):
            return torch.cat([input_ids, torch.tensor([[5, 9, 7]] * len(input_ids))], 1)

    out = text_only_generate(Proc(), Net(), 60)([("a", "a.jpg", "0" * 64)], ["w1 w2"])
    assert out == [("w5 w9", 2, False)] and all(c["type"] == "text" for c in seen) and "image" not in str(seen)
    with tempfile.TemporaryDirectory() as tmp:
        assert C.refuses(lambda: decode_runs(["c1_qwen25vl_7b_ov_dev_a-zs"], Path(tmp), Path(tmp), Path(tmp),
                                             Path(tmp))), "a stage-1 run id is not a stage-2 run"
        assert C.refuses(lambda: decode_runs([ret["run_id"], g["c2_internvl3_8b_ov_dev_b-zs"]["run_id"]], Path(tmp),
                                             Path(tmp), Path(tmp), Path(tmp))), "one model per process"
        (Path(tmp) / "x.npz").write_bytes(b"x")
        assert C.refuses(lambda: load_emb1(Path(tmp) / "x.npz")), "only the stage-1 embeddings are memory vectors"
    print("selftest ok: examples (stage-1 rule, XM first member, near cut, tertile cuts), blind prompts and "
          "text-only path, run refusal, pinned stage-1 embeddings")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    for name in ("embed", "exemplars"):
        p = sub.add_parser(name)
        p.add_argument("--set", choices=sorted(S2.SETS), required=True)
        p.add_argument("--lists", type=Path, required=True)
        p.add_argument("--emb1", type=Path, required=True, help="the stage-1 emb.npz")
        p.add_argument("--out", required=True)
        if name == "embed":
            p.add_argument("--snapshot", type=Path, required=True)
            p.add_argument("--revision", required=True)
        else:
            p.add_argument("--emb", type=Path, required=True, help="this set's query embeddings")
    p = sub.add_parser("decode")
    p.add_argument("--run-ids", nargs="+", required=True)
    p.add_argument("--snapshot", type=Path, required=True)
    p.add_argument("--lists", type=Path, required=True)
    p.add_argument("--exemplars", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.cmd == "decode":
        return decode_runs(a.run_ids, a.snapshot, a.lists, a.exemplars, a.out_dir)
    {"embed": cmd_embed, "exemplars": cmd_exemplars}.get(a.cmd, lambda _a: ap.error("mode?"))(a)


if __name__ == "__main__":
    main()
