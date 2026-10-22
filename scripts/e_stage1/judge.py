#!/usr/bin/env python3
"""Paper E stage 1 (EXPLORATORY / DEV), GPU steps on M3: zero-shot captions of E-dev-A, the per-object judge cache,
the whole-caption judge cache and the embedding baselines. Design DESIGN.md §4-§5.

  python scripts/e_stage1/judge.py --selftest                                                        CPU, no data
  python scripts/e_stage1/judge.py decode  --model K --snapshot DIR --split S --captions C --images DIR --out-dir D
  python scripts/e_stage1/judge.py objects --judge J [--snapshot DIR] --split S --items I --images DIR --out-dir D
  python scripts/e_stage1/judge.py whole   --judge J --lang vi --snapshot DIR --split S --captions C --images DIR --out-dir D
  python scripts/e_stage1/judge.py embed   --siglip DIR --siglip-revision REV --split S --captions C --images DIR --out-dir D
Reused unchanged: the LB decoder (B-N1 models, `short` prompt), Paper C's guard (hf_verifier, s2_verifier and fill:
P(yes) = P(Yes+yes) / (P(Yes+yes) + P(No+no)) at the answer position, with and without the image, the no-image pass
once per question) and S2's English question. Inputs are E-dev-A files only (pairs.py); this script never opens the
OIV7 labels or an XM3600 annotation file. Writes ids, class names, caption ids and numbers; decode writes captions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e_lists as L  # noqa: E402
import guard  # noqa: E402  Paper C's verifiers and cache filler, imported unchanged
from pairs import DS, english_map, read_jsonl  # noqa: E402

C, lb = L.C, L.C.lb
SCHEMA = "vsps.e_stage1.v1"
MODELS = ("qwen25vl_3b", "qwen25vl_7b", "qwen3vl_8b", "internvl3_8b")  # B-N1 generators, zero-shot `short`
JUDGES = {"qwen25vl_7b": ("en", "vi"), "qwen3vl_8b": ("en", "vi"), "internvl3_s2": ("en",)}  # question languages
WHOLE_JUDGES = ("qwen25vl_7b", "qwen3vl_8b", "internvl3_s2")  # the last runs only within the cap (DESIGN §8)
VI_QUESTION = "Trong ảnh có {np} không? Trả lời có hoặc không."  # pope_vi.PROMPTS["vi"], placeholder renamed
VI_WORDS = (("có", "Có"), ("không", "Không"))  # probe_existence.ask's answer words
WHOLE = 'Does the following caption describe the image correctly? Caption: "{np}" Answer yes or no.'  # this design


def question(lang: str) -> str:
    return guard.s2()["verifier_protocol"]["question_template"] if lang == "en" else VI_QUESTION


def gpu_start(a) -> dict:
    """Every GPU mode: GPU pins only (never the labels file), test gold and XM3600 annotations absent from this host,
    the pinned split, and an image folder holding E-dev-A images only."""
    L.design(local=False)
    L.m3_clean(lb.DATA)
    split = L.load_split(a.split)
    folder_only_dev_a(Path(a.images), split)
    return split


def folder_only_dev_a(images: Path, split: dict) -> None:
    allow = {f: h for _i, f, h in split["sets"][DS]}
    bad = [p.name for p in sorted(images.iterdir())
           if not p.is_file() or p.name not in allow or lb.sha256_file(p) != allow[p.name]]
    if bad:
        raise SystemExit(f"REFUSED: {images} holds {len(bad)} file(s) that are not E-dev-A images, e.g. {bad[:3]}")


def image_paths(ids, split: dict, images: Path) -> dict:
    """{(DS, id): (path, sha)}; refused unless every image is an E-dev-A image (e_lists.check_images)."""
    return {(DS, i): (Path(images) / f, h) for i, (f, h) in L.check_images(sorted(set(ids)), split).items()}


def checked(load):
    def run(path_sha):
        path, h = path_sha
        if lb.sha256_file(path) != h:
            raise SystemExit(f"{path}: sha256 differs from the split")
        return load(path)
    return run


# ------------------------------------------------------------------------------------------------ verifiers
def retarget(ask, about: dict, tok, words) -> None:
    """Point guard.hf_verifier's answer-token lists at other words, in place: ask and the answer-position check read
    these very lists (checked through ask's closure), so the rule is unchanged and guard.py is not edited."""
    yes, no = about["yes_token_ids"], about["no_token_ids"]
    cells = [c.cell_contents for c in ask.__closure__ or ()]
    if not (any(x is yes for x in cells) and any(x is no for x in cells)):
        raise SystemExit("the verifier does not read its answer tokens from these lists")
    ids = [[tok.encode(w, add_special_tokens=False)[0] for w in ws] for ws in words]
    if len(set(ids[0] + ids[1])) != 4:
        raise SystemExit(f"answer words {words} share a first token")
    yes[:], no[:] = ids
    about["yes_no_mass"].clear()  # the median-mass check runs again on the first 20 questions in the new words


def verifier(judge: str, snapshot: Path | None):
    """(load, ask, about, tokenizer or None)."""
    if judge == "internvl3_s2":  # S2's instrument, S2's transformers 4.51.3 venv; English question only
        load, ask, about = guard.s2_verifier(guard.s2())
        return load, ask, about, None
    from transformers import AutoTokenizer

    reg = C.registration()
    m = reg["models"][judge]
    if lb.packages() != reg["venv"]["packages"]:
        raise SystemExit(f"{judge} runs in the B-N1 venv")
    lb.check_snapshot(m, snapshot)
    load, ask, about = guard.hf_verifier(m, snapshot)
    tok = AutoTokenizer.from_pretrained(snapshot)
    if [tok.encode(w, add_special_tokens=False)[0] for w in ("Yes", "yes")] != about["yes_token_ids"]:
        raise SystemExit("the tokenizer differs from the verifier's")
    return load, ask, about, tok


def write_about(path: Path, about: dict, **extra) -> None:
    about = dict(about)
    mass = sorted(about.pop("yes_no_mass", []))
    about["yes_no_mass_median"] = mass[len(mass) // 2] if mass else None
    path.write_text(json.dumps({**about, **extra, "label": L.LABEL, "design_sha256": L.DESIGN_SHA256,
                                "split_sha256": L.SPLIT_SHA256, "guard_sha256": lb.sha256_file(Path(guard.__file__)),
                                "machine_id": os.environ.get("VSPS_MACHINE_ID")}, default=str) + "\n")


def cmd_objects(a) -> None:
    split = gpu_start(a)
    todo = read_jsonl(a.items)
    paths = image_paths({t["image_id"] for t in todo}, split, a.images)
    load, ask, about, tok = verifier(a.judge, a.snapshot)
    out = Path(a.out_dir)
    for lang in JUDGES[a.judge]:
        if lang == "vi":
            retarget(ask, about, tok, VI_WORDS)
        names = english_map() if lang == "en" else {t["class"]: t["class"] for t in todo}
        vp = {"question_template": question(lang), "english_class_map": names}
        n = guard.fill(out / f"obj_{a.judge}_{lang}.jsonl", todo, paths, (checked(load), ask), vp, a.judge)
        write_about(out / f"obj_{a.judge}_{lang}.about.json", about, judge=a.judge, lang=lang, new_rows=n,
                    items_sha256=lb.sha256_file(Path(a.items)))


def whole_todo(caps: list[dict]) -> tuple[list[dict], dict]:
    """One item per caption (its id in the `class` slot), so guard.fill asks P(yes) with the image and once without."""
    todo = [{"dataset": DS, "image_id": r["image_id"], "class": r["cid"]}
            for r in sorted(caps, key=lambda r: (r["image_id"], r["cid"]))]
    return todo, {"question_template": WHOLE, "english_class_map": {r["cid"]: r["text"] for r in caps}}


def cmd_whole(a) -> None:
    split = gpu_start(a)
    caps = [r for r in read_jsonl(a.captions) if a.lang in ("all", r["lang"])]  # Vietnamese first (DESIGN §8)
    paths = image_paths({r["image_id"] for r in caps}, split, a.images)
    load, ask, about, _tok = verifier(a.judge, a.snapshot)
    todo, vp = whole_todo(caps)
    n = guard.fill(Path(a.out_dir) / f"whole_{a.judge}.jsonl", todo, paths, (checked(load), ask), vp, a.judge)
    write_about(Path(a.out_dir) / f"whole_{a.judge}.about.json", about, judge=a.judge, new_rows=n,
                captions_sha256=lb.sha256_file(Path(a.captions)))


# ------------------------------------------------------------------------------------------------ embeddings
def cmd_embed(a) -> None:
    """Global image-text cosine: SigLIP2 (Paper C's snapshot, revision passed and recorded) and the multilingual CLIP
    of scripts/clip_score.py (open_clip MODEL / PRETRAINED, fp32)."""
    import open_clip
    import torch
    from PIL import Image
    from transformers import AutoModel, AutoProcessor

    import clip_score

    split = gpu_start(a)
    caps = read_jsonl(a.captions)
    paths = image_paths({r["image_id"] for r in caps}, split, a.images)
    load = checked(lambda p: Image.open(p).convert("RGB"))
    sp = AutoProcessor.from_pretrained(a.siglip)
    sm = AutoModel.from_pretrained(a.siglip, torch_dtype=torch.float16).eval().cuda()
    cm, _t, cpre = open_clip.create_model_and_transforms(clip_score.MODEL, pretrained=clip_score.PRETRAINED)
    cm, ctok = cm.float().eval().cuda(), open_clip.get_tokenizer(clip_score.MODEL)
    norm = lambda x: torch.nn.functional.normalize(x.float(), dim=-1)  # noqa: E731
    rows = []
    with torch.no_grad():
        for (_ds, i), ps in sorted(paths.items()):
            im = load(ps)
            mine = [r for r in caps if r["image_id"] == i]
            texts = [r["text"] for r in mine]
            si = norm(sm.get_image_features(**sp(images=im, return_tensors="pt").to("cuda", torch.float16)))
            st = norm(sm.get_text_features(**sp(text=texts, padding="max_length", max_length=64, truncation=True,
                                                return_tensors="pt").to("cuda")))
            ci = norm(cm.encode_image(cpre(im)[None].cuda()))
            ct = norm(cm.encode_text(ctok(texts).cuda()))
            rows += [{"cid": r["cid"], "image_id": i, "siglip2_cos": float(s), "mclip_cos": float(c)}
                     for r, s, c in zip(mine, (st @ si.T)[:, 0].tolist(), (ct @ ci.T)[:, 0].tolist())]
    out = Path(a.out_dir) / "embed.jsonl"
    out.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    write_about(Path(str(out) + ".about.json"), {}, siglip_revision=a.siglip_revision, mclip=[
        clip_score.MODEL, clip_score.PRETRAINED], captions_sha256=lb.sha256_file(Path(a.captions)))


# ------------------------------------------------------------------------------------------------ zero-shot decode
def cmd_decode(a) -> None:
    import torch

    split = gpu_start(a)
    want = sorted({r["image_id"] for r in read_jsonl(a.captions)})
    files = L.check_images(want, split)
    rows = [(i, *files[i]) for i in want]
    reg = C.registration()
    m = reg["models"][a.model]
    if lb.packages() != reg["venv"]["packages"]:
        raise SystemExit("decoding runs in the B-N1 venv")
    lb.check_snapshot(m, a.snapshot)
    run_id = f"e1_{a.model}_{DS}-short"
    out = Path(a.out_dir) / f"{run_id}.preds.json"
    if out.exists():
        raise SystemExit(f"{out} exists; a run is decoded once")
    prompt, n_new = lb.prompt_text(reg, "short"), reg["decode"]["max_new_tokens"]["short"]
    kw = {"max_new_tokens": n_new, "do_sample": False, "num_beams": 1}
    proc, net = lb.load(m, a.snapshot, "cuda:0")
    part = Path(str(out) + ".partial.jsonl")
    resumed, started = part.exists(), lb.utc()
    key = lb.run_key(L.DESIGN_SHA256, {"run_id": run_id, "split_sha256": L.SPLIT_SHA256}, m, kw, prompt, rows)
    res = lb.decode_slices(rows, m["batch_size"], lb.make_generate(proc, net, prompt, n_new, Path(a.images)), part,
                           key)
    status = lb.git("status", "--porcelain", "--untracked-files=no")
    prov = {k: None for k in lb.PROV_FIELDS} | {
        "schema": lb.SCHEMA, "e_schema": SCHEMA, "label": L.LABEL, "design_sha256": L.DESIGN_SHA256,
        "split_sha256": L.SPLIT_SHA256, "prereg_id": "B-N1 model blocks (no registration for stage 1)",
        "prereg_sha256": C.PINS[C.B_N1], "decoder_sha256": C.PINS["scripts/lb/decode_hf_vlm.py"],
        "wrapper_sha256": lb.sha256_file(Path(__file__)), "run_id": run_id, "model": a.model, "hub_id": m["hub_id"],
        "revision": m["revision"], "dataset": DS, "prompt_mode": "short", "prompt_text_sha256": C.ZS_PROMPT_SHA256,
        "manifest_sha256": hashlib.sha256(json.dumps(rows).encode()).hexdigest(), "max_new_tokens": n_new,
        "batch_size": m["batch_size"], "dtype": m["dtype"], "attn_implementation": m["attn_implementation"],
        "processor_kwargs": m["processor_kwargs"], "generation_config": net.generation_config.to_diff_dict(),
        "machine_id": os.environ.get("VSPS_MACHINE_ID"), "git_head": lb.git("rev-parse", "HEAD"),
        "git_dirty": None if status is None else bool(status), "job_sha256": os.environ.get("VSPS_JOB_SHA256"),
        "venv_freeze_sha256": os.environ.get("VSPS_VENV_FREEZE_SHA256"), "packages": lb.packages(),
        "n_images": len(rows), "parity_slice0": {"n": 0, "identical": 0}, "resumed": resumed, "started_utc": started,
        "finished_utc": lb.utc(), "gpu": torch.cuda.get_device_name(0), "generate_kwargs": kw}
    lb.write_output(out, prov, res)
    print(f"wrote {out}")


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def selftest() -> None:
    import pope_vi

    assert VI_QUESTION == pope_vi.PROMPTS["vi"].replace("{name}", "{np}")
    assert question("en") == "Is there {np} in the image? Answer yes or no."
    assert set(MODELS) <= set(C.registration()["models"]) and {"qwen25vl_7b", "qwen3vl_8b"} <= set(
        C.registration()["models"])

    def fake_verifier():  # shaped like guard.hf_verifier: ask reads the very lists returned in `about`
        yes, no, mass = [0, 1], [2, 3], []
        p = [0.30, 0.10, 0.05, 0.05, 0.40, 0.10]

        def ask(_q, _px):
            mass.append(sum(p[t] for t in yes + no))
            return sum(p[t] for t in yes) / (sum(p[t] for t in yes) + sum(p[t] for t in no))
        return ask, {"yes_token_ids": yes, "no_token_ids": no, "yes_no_mass": mass}

    class Tok:
        ids = {"có": [4, 9], "Có": [5], "không": [2, 7], "Không": [3], "Yes": [0], "yes": [1]}

        def encode(self, w, add_special_tokens=False):
            return self.ids[w]

    ask, about = fake_verifier()
    assert abs(ask("q", None) - 0.8) < 1e-9 and len(about["yes_no_mass"]) == 1
    retarget(ask, about, Tok(), VI_WORDS)
    assert about["yes_token_ids"] == [4, 5] and not about["yes_no_mass"]
    assert abs(ask("q", None) - 0.5 / 0.6) < 1e-9, "ask now reads P(có + Có) against P(không + Không)"
    ask2, about2 = fake_verifier()
    copy = {**about2, "yes_token_ids": list(about2["yes_token_ids"])}
    assert C.refuses(lambda: retarget(ask2, copy, Tok(), VI_WORDS)), "lists the verifier does not read: refused"
    assert C.refuses(lambda: retarget(ask2, about2, Tok(), (("Yes", "yes"), ("Yes", "có")))), "shared tokens refused"
    caps = [{"cid": f"vi|d1|r0|{t}", "image_id": "d1", "text": f"chuỗi thử nghiệm giả {t}"} for t in ("a", "b")]
    todo, vp = whole_todo(caps)
    calls = []

    def ask3(q, px):
        calls.append((q, px))
        return 0.9 if px is not None else 0.4
    with tempfile.TemporaryDirectory() as tmp:
        n = guard.fill(Path(tmp) / "w.jsonl", todo, {(DS, "d1"): "px"}, (lambda p: p, ask3), vp, "j")
        rows = read_jsonl(Path(tmp) / "w.jsonl")
    assert n == 2 and len(calls) == 4 and all(abs(r["p_with"] - r["p_without"] - 0.5) < 1e-9 for r in rows)
    assert calls[0][0] == WHOLE.format(np="chuỗi thử nghiệm giả a"), "the caption goes into the whole-caption question"
    xm = sorted(json.loads(C.pinned(C.EXCL).read_text(encoding="utf-8"))["image_sha256"]["xm3600_all_images"])
    fake = {"refuse_image_sha256": [], "sets": {"e_dev_a": [["d1", "d1.jpg", xm[0]]]}}
    assert image_paths(["d1"], fake, Path("/i")) == {(DS, "d1"): (Path("/i/d1.jpg"), xm[0])}
    assert C.refuses(lambda: image_paths(["d1", "t9"], fake, Path("/i"))), "an image outside E-dev-A is refused"
    with tempfile.TemporaryDirectory() as tmp:
        img = Path(tmp)
        (img / "s.json").write_text("{}")
        assert C.refuses(lambda: L.load_split(img / "s.json")), "a split other than the pinned e_split.json is refused"
        assert C.refuses(lambda: L.load_split(img / "s.json", None)), "no GPU step while the split is unpinned"
        (img / "s.json").unlink()
        (img / "d1.jpg").write_bytes(b"synthetic")
        ok = {"sets": {DS: [["d1", "d1.jpg", lb.sha256_file(img / "d1.jpg")]]}}
        folder_only_dev_a(img, ok)
        (img / "x.jpg").write_bytes(b"other")
        assert C.refuses(lambda: folder_only_dev_a(img, ok)), "a folder with a non-E-dev-A file is refused"
    print("selftest ok: questions, answer-word retarget and its refusals, whole-caption cache, E-dev-A refusal, "
          "image-folder check")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    parsers = {n: sub.add_parser(n) for n in ("decode", "objects", "whole", "embed")}
    for n, p in parsers.items():
        for x in ("--split", "--images", "--out-dir"):
            p.add_argument(x, type=Path, required=True)
        p.add_argument("--items" if n == "objects" else "--captions", type=Path, required=True)
        if n != "embed":
            p.add_argument("--snapshot", type=Path)
    parsers["decode"].add_argument("--model", choices=MODELS, required=True)
    parsers["objects"].add_argument("--judge", choices=sorted(JUDGES), required=True)
    parsers["whole"].add_argument("--judge", choices=WHOLE_JUDGES, required=True)
    parsers["whole"].add_argument("--lang", choices=("vi", "en", "all"), default="vi")
    parsers["embed"].add_argument("--siglip", type=Path, required=True)
    parsers["embed"].add_argument("--siglip-revision", required=True)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    {"decode": cmd_decode, "objects": cmd_objects, "whole": cmd_whole, "embed": cmd_embed}.get(
        a.cmd, lambda _a: ap.error("mode?"))(a)


if __name__ == "__main__":
    main()
