#!/usr/bin/env python3
"""Paper C stage 1 (EXPLORATORY / DEV): the object guard, checked by a different VLM. Design DESIGN.md §5.

An object is *neighbour-only* when the caption names it (rescap matcher v2), the image's own zero-shot caption does
not, and one of the examples shown with the image does. Each neighbour-only (image, class) is put to a verifier of
a different VLM with S2's protocol (prereg 2026-10-18_tier3_S2: its English question, class map and P(yes) rule):
s = P(yes | image) - P(yes | no image). Classes with s < tau are deleted by the deterministic rule of delete().

  python scripts/c_stage1/guard.py --selftest                                                    CPU, no data
  python scripts/c_stage1/guard.py items --runs P.preds.json ... --zs Z.preds.json --lists L --out items.jsonl
  python scripts/c_stage1/guard.py score --items I --generator G --lists L [--snapshot DIR] --out cache.jsonl  GPU
The verifier of qwen25vl_7b is S2's own instrument (xv_ef1.verifier, InternVL3-8B 853e3a79, S2's transformers
4.51.3 venv); the verifier of internvl3_8b is Qwen3-VL-8B (B-N1 snapshot, B-N1 venv), asked the same question.
Writes ids, class names and probabilities only.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
import tempfile
from itertools import groupby
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import decode_icl as C  # noqa: E402
import rl_reward  # noqa: E402  function_end (scripts/ is on the path via decode_icl)
from rescap.chair import _NOT_OBJECTS, _NOUNS, objects_in  # noqa: E402  matcher v2
from rescap.svp.matching import canonical  # noqa: E402

lb = C.lb
S2 = "manuscript/prereg/2026-10-18_tier3_S2.json"
PINS = {S2: "ac6404b6a0715deb351eae8fdeb9aea990415298ea3c8beaab2ab5d109a73db3",
        "scripts/xv_ef1.py": "c3c34667cfd0fe2f7798c81f09b3fb3019647ef60a29dc20e0aa55f0725c5e0e"}
VERIFIER = {"qwen25vl_7b": "internvl3_s2", "internvl3_8b": "qwen3vl_8b"}
VLM_LINE = {"qwen25vl_7b": "qwen-vl", "qwen3vl_8b": "qwen-vl", "internvl3_8b": "internvl", "internvl3_s2": "internvl"}
# the LLMs overlap: InternVL3-8B is built on Qwen2.5-7B, and Qwen3-VL is in the Qwen line (DESIGN §5)
TAUS = (-math.inf, 0.0, 0.1, 0.2, 0.3, math.inf)  # -inf: no guard; +inf: delete every neighbour-only class
SPLIT = re.compile(r"(\s*[,;]\s*|\s+(?:và|cùng với|bên cạnh|cạnh|gần|phía trước|phía sau|trước|sau|trên|dưới|trong)"
                   r"\s+)")
END = re.compile(r"[.!?…]+$")


def s2() -> dict:
    p = C.ROOT / S2
    if lb.sha256_file(p) != PINS[S2]:
        raise SystemExit(f"{S2}: not the committed S2 registration")
    return json.loads(p.read_text(encoding="utf-8"))


def key(o: str) -> str:
    return canonical(o) or o


def classes(text: str) -> list[str]:
    """Distinct classes in order of first mention (matcher v2)."""
    return list(dict.fromkeys(objects_in(text)))


def neighbour_only(caption: str, zs_caption: str, shown: list[str]) -> list[str]:
    zs = {key(o) for o in objects_in(zs_caption)}
    ex = {key(o) for c in shown for o in objects_in(c)}
    return [o for o in classes(caption) if key(o) not in zs and key(o) in ex]


def delete(caption: str, rejected: set[str], zs_caption: str) -> tuple[str, str]:
    """(caption, how). The caption is cut into units at commas, semicolons, `và`, `cùng với` and the locative
    prepositions of SPLIT; every unit that names a rejected class is dropped with the separator before it, and the end
    punctuation is kept. If the first unit (the subject) names one, or the result ends on a function word or names any
    class set other than the original minus the rejected ones, the image's zero-shot caption is used."""
    rej = {key(o) for o in rejected}
    if not rej:
        return caption, "kept"
    body = caption.strip()
    m = END.search(body)
    end, body = (m.group(), body[:m.start()]) if m else ("", body)
    parts = SPLIT.split(body)
    units = list(zip([""] + parts[1::2], parts[0::2]))
    drop = [bool({key(o) for o in objects_in(u)} & rej) for _s, u in units]
    if drop[0]:  # the first unit holds the subject: dropping it leaves a fragment
        return zs_caption, "fallback"
    out = "".join(s + u for (s, u), d in zip(units, drop) if not d).strip()
    want = {key(o) for o in objects_in(caption)} - rej
    if not out or {key(o) for o in objects_in(out)} != want or rl_reward.function_end(out):
        return zs_caption, "fallback"
    return out + end, "deleted"


def guarded(caption: str, zs_caption: str, shown: list[str], score: dict, tau: float) -> tuple[str, list, list, str]:
    """(caption after the guard, neighbour-only classes, rejected classes, how) at threshold tau."""
    no = neighbour_only(caption, zs_caption, shown)
    rej = [o for o in no if tau == math.inf or (tau > -math.inf and score[o] < tau)]
    out, how = delete(caption, set(rej), zs_caption)
    return out, no, rej, how


# ------------------------------------------------------------------------------------------------ zero-shot inputs
DP_REUSE_SHA256 = "5280baa49a6901fd862f7c376fc71d060477deea5235569afacca649f0378ded"  # dp_qwen25vl_7b dev299 short T0


def zs_ok(prov: dict, file_sha: str, model: str, ds: str) -> None:
    """A zero-shot input is C's own zs run, or the dev-pool greedy file whose model, prompt, cap and set match."""
    reg = C.registration()
    m = reg["models"][model]
    same = (prov["hub_id"], prov["revision"], prov["prompt_text_sha256"], prov["max_new_tokens"],
            prov["generate_kwargs"], prov["dataset"], prov["packages"]) == (
        m["hub_id"], m["revision"], C.ZS_PROMPT_SHA256, 60, {"max_new_tokens": 60, "do_sample": False, "num_beams": 1},
        ds, reg["venv"]["packages"])
    own = prov.get("c_schema") == C.SCHEMA and prov["spec"]["arm"] == "zs"
    reuse = file_sha == DP_REUSE_SHA256 and prov.get("manifest_sha256") == C.PINS[C.DEV299]
    if not (same and (own or reuse)):
        raise SystemExit(f"{prov.get('run_id')}: not a matching zero-shot input for {model} on {ds}")


def read_preds(path: Path) -> dict:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    d["_sha256"] = lb.sha256_file(Path(path))
    return d


# ------------------------------------------------------------------------------------------------ items (CPU)
def items(runs: list[dict], zs: dict, caps: dict) -> list[dict]:
    """Unique neighbour-only (dataset, image, class) of the runs, which share one generator, set and zero-shot."""
    out = {}
    for r in runs:
        src = C.DATASETS[r["dataset"]]["src"]
        for i, cap in r["predictions"].items():
            for o in neighbour_only(cap, zs["predictions"][i], [C.shown(caps[c], src) for c in r["exemplars"][i]]):
                out[(r["dataset"], i, o)] = {"dataset": r["dataset"], "image_id": i, "class": o}
    return [out[k] for k in sorted(out)]


def cmd_items(a) -> None:
    lists = C.load_lists(a.lists)
    runs, zs = [read_preds(p) for p in a.runs], read_preds(a.zs)
    if len({(r["model"], r["dataset"]) for r in runs + [zs]}) != 1:
        raise SystemExit("items: one generator and one set per call")
    zs_ok(zs, zs["_sha256"], zs["model"], zs["dataset"])
    rows = items(runs, zs, C.memory_captions(lists))
    Path(a.out).write_text("".join(json.dumps({**r, "generator": zs["model"]}) + "\n" for r in rows),
                           encoding="utf-8")
    print(f"{len(rows)} neighbour-only items")


# ------------------------------------------------------------------------------------------------ score (GPU)
def s2_verifier(reg: dict):
    """S2's instrument, unchanged: xv_ef1.verifier on the pinned InternVL3-8B, its README image loader and settings."""
    import torch
    import torchvision.transforms as T
    import transformers
    from huggingface_hub import snapshot_download
    from torchvision.transforms.functional import InterpolationMode

    import xv_ef1

    if lb.sha256_file(C.ROOT / "scripts/xv_ef1.py") != PINS["scripts/xv_ef1.py"]:
        raise SystemExit("scripts/xv_ef1.py differs from the committed S2 instrument")
    if transformers.__version__ != reg["machines"]["venv"]["transformers"]:
        raise SystemExit(f"S2's verifier runs under transformers {reg['machines']['venv']['transformers']}")
    v, img = reg["models"]["verifier"], reg["verifier_protocol"]["image_preprocessing"]
    snap = Path(snapshot_download(v["id"], revision=v["revision"]))
    for name, h in v["shards_sha256"].items():
        if lb.sha256_file(snap / name) != h:
            raise SystemExit(f"{name} is not the registered shard")
    xv_ef1.same_as_readme(snap / "README.md", v["licence"]["readme_sha256"])
    ask, about = xv_ef1.verifier(v, torch)
    load_image = xv_ef1.readme_loader(torch, T, InterpolationMode)

    def load(path):
        return load_image(path, input_size=img["input_size"], max_num=img["max_num"]).to(torch.bfloat16).cuda()

    return load, (lambda q, px: ask(xv_ef1.IMAGE + q if px is not None else q, px)), {**about, "id": v["id"],
                                                                                       "revision": v["revision"]}


def hf_verifier(m: dict, snapshot: Path):
    """S2's P(yes) rule through the model's own chat template: one forward pass, next-token probabilities at the
    answer position, P(Yes + yes) / (P(Yes + yes) + P(No + no)); without an image, the text-only message."""
    import torch
    from PIL import Image

    proc, net = lb.load(m, snapshot, "cuda:0")
    tok = proc.tokenizer
    yes = [tok.encode(w, add_special_tokens=False)[0] for w in ("Yes", "yes")]
    no = [tok.encode(w, add_special_tokens=False)[0] for w in ("No", "no")]
    mass: list[float] = []

    def ask(question, image) -> float:
        content = ([{"type": "image", "image": image}] if image is not None else []) + [
            {"type": "text", "text": question}]
        enc = proc.apply_chat_template([[{"role": "user", "content": content}]], add_generation_prompt=True,
                                       tokenize=True, return_dict=True, return_tensors="pt",
                                       padding=True).to(net.device, net.dtype)
        with torch.no_grad():
            p = net(**enc).logits[0, -1].float().softmax(-1)
        mass.append(float(p[yes].sum() + p[no].sum()))
        answer_position_check(mass)
        return float(p[yes].sum() / (p[yes].sum() + p[no].sum()))

    return (lambda path: Image.open(path).convert("RGB")), ask, {"yes_token_ids": yes, "no_token_ids": no,
                                                                 "id": m["hub_id"], "revision": m["revision"],
                                                                 "yes_no_mass": mass}


def answer_position_check(mass: list[float], n: int = 20, floor: float = 0.5) -> None:
    """After n questions, the yes + no tokens must hold a median >= floor of the next-token mass; otherwise the
    position read is not the answer position and the renormalised P(yes) means nothing."""
    if len(mass) == n and sorted(mass)[n // 2] < floor:
        raise SystemExit(f"median yes+no mass {sorted(mass)[n // 2]:.3f} < {floor}: not the answer position")


def fill(cache: Path, todo: list[dict], paths: dict, probe: tuple, vp: dict, verifier: str) -> int:
    """Append one row per item the cache lacks; P(yes | no image) is asked once per class. Resumes after a stop.
    probe = (load(path) -> pixels, ask(question, pixels or None) -> P(yes))."""
    load, ask = probe
    rows = [json.loads(x) for x in cache.read_text(encoding="utf-8").splitlines() if x] if cache.exists() else []
    done = {(r["dataset"], r["image_id"], r["class"]) for r in rows}
    p_no = {r["class"]: r["p_without"] for r in rows}
    new = [t for t in todo if (t["dataset"], t["image_id"], t["class"]) not in done]
    with cache.open("a", encoding="utf-8") as f:
        for (ds, i), group in groupby(new, key=lambda t: (t["dataset"], t["image_id"])):
            px = load(paths[(ds, i)])
            for t in group:
                q = vp["question_template"].format(np=vp["english_class_map"][t["class"]])
                if t["class"] not in p_no:
                    p_no[t["class"]] = ask(q, None)
                f.write(json.dumps({**t, "verifier": verifier, "p_with": ask(q, px),
                                    "p_without": p_no[t["class"]]}) + "\n")
                f.flush()
    return len(new)


def cmd_score(a) -> None:
    reg2 = s2()
    lists = C.load_lists(a.lists)
    todo = [json.loads(x) for x in Path(a.items).read_text(encoding="utf-8").splitlines() if x]
    if {t["generator"] for t in todo} != {a.generator}:
        raise SystemExit("the items were not made for this generator")
    paths = {}
    for ds in {t["dataset"] for t in todo}:  # every item image must be a stage-1 dev image (refusal re-run)
        folder = lb.DATA / "datasets" / C.DATASETS[ds]["image_dir"]
        for i, f, h in C.manifest(ds, lists):
            paths[(ds, i)] = (folder / f, h)
    if any((t["dataset"], t["image_id"]) not in paths for t in todo):
        raise SystemExit("REFUSED: an item image is not in a stage-1 dev manifest")
    verifier = VERIFIER[a.generator]
    if verifier == "internvl3_s2":
        load, ask, about = s2_verifier(reg2)
    else:
        reg = C.registration()
        if lb.packages() != reg["venv"]["packages"]:
            raise SystemExit("the Qwen3-VL verifier runs in the B-N1 venv")
        lb.check_snapshot(reg["models"][verifier], a.snapshot)
        load, ask, about = hf_verifier(reg["models"][verifier], a.snapshot)

    def checked(path_sha):
        path, h = path_sha
        if lb.sha256_file(path) != h:
            raise SystemExit(f"{path}: sha256 differs from the manifest")
        return load(path)

    n = fill(Path(a.out), todo, paths, (checked, ask), reg2["verifier_protocol"], verifier)
    if "yes_no_mass" in about:
        mass = sorted(about.pop("yes_no_mass"))
        about["yes_no_mass_median"] = mass[len(mass) // 2] if mass else None
    Path(str(a.out) + ".about.json").write_text(json.dumps({**about, "verifier": verifier, "label": C.LABEL,
                                                            "design_sha256": C.PINS[C.DESIGN],
                                                            "packages": lb.packages(), "new_rows": n}) + "\n")


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def selftest() -> None:
    vp = s2()["verifier_protocol"]
    returnable = {o for k, o in _NOUNS.items() if k not in _NOT_OBJECTS}
    assert set(vp["english_class_map"]) == returnable, "S2's class map covers every class the matcher returns"
    assert all(VLM_LINE[g] != VLM_LINE[v] for g, v in VERIFIER.items()), "the verifier is a different VLM"
    # sentences written for this test, not dataset captions
    cap = "chuỗi đàn ông số một bên cạnh âm xe máy giả kỹ trên âm đường giả vắng."
    shown = ["chiếc xe máy sơn đỏ đậu trước nhà"]
    zs = "người đàn ông râu bạc trên đường phố"
    assert neighbour_only(cap, zs, shown) == ["xe máy"]
    assert neighbour_only(cap, "người đàn ông", ["con chó"]) == [], "not shown, so not neighbour-only"
    assert delete(cap, {"xe máy"}, "zs") == ("chuỗi đàn ông số một trên âm đường giả vắng.", "deleted")
    assert delete("hai con chó và một cái bàn", {"bàn"}, "zs") == ("hai con chó", "deleted")
    assert delete("cái bàn và hai con chó", {"bàn"}, "zs") == ("zs", "fallback"), "the subject is never cut"
    assert delete("chiếc xe máy", {"xe máy"}, "zs") == ("zs", "fallback"), "nothing left"
    assert delete("con chó nằm cạnh xe máy và cái bàn", {"chó"}, "zs") == ("zs", "fallback")
    assert delete(cap, set(), "zs") == (cap, "kept")
    for c in (cap, "hai con chó, một cái bàn; ba cái ghế trong phòng"):
        for o in classes(c):
            out, how = delete(c, {o}, "zs")
            assert how == "fallback" or {key(x) for x in objects_in(out)} == {key(x) for x in objects_in(c)} - {key(o)}
    assert C.refuses(lambda: answer_position_check([0.1] * 20)) and not C.refuses(lambda: answer_position_check(
        [0.9] * 20)), "the answer-position check"
    sc = {"xe máy": 0.15}
    assert guarded(cap, zs, shown, sc, 0.1)[2] == [] and guarded(cap, zs, shown, sc, 0.2)[2] == ["xe máy"]
    assert guarded(cap, zs, shown, {}, -math.inf)[2] == [] and guarded(cap, zs, shown, {}, math.inf)[2] == ["xe máy"]
    calls = []

    def ask(q, px):
        calls.append(px is None)
        return 0.25 if px is None else 0.75

    todo = [{"dataset": "ov_dev_a", "image_id": i, "class": o, "generator": "g"} for i in ("a", "b") for o in
            ("chó", "bàn")]
    paths = {("ov_dev_a", i): i for i in ("a", "b")}
    with tempfile.TemporaryDirectory() as tmp:
        cache = Path(tmp) / "c.jsonl"
        assert fill(cache, todo[:3], paths, (lambda p: p, ask), vp, "v") == 3
        assert fill(cache, todo, paths, (lambda p: p, ask), vp, "v") == 1, "resume scores only the missing item"
        rows = [json.loads(x) for x in cache.read_text().splitlines()]
        assert len(rows) == 4 and sum(calls) == 2, "P(yes | no image) once per class"
        assert all(r["p_with"] - r["p_without"] == 0.5 for r in rows)
    print("selftest ok: class map, different-VLM verifiers, neighbour-only, deletion invariant and fallback, "
          "thresholds, cache")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("items")
    p.add_argument("--runs", nargs="+", type=Path, required=True)
    p.add_argument("--zs", type=Path, required=True)
    p.add_argument("--lists", type=Path, required=True)
    p.add_argument("--out", required=True)
    p = sub.add_parser("score")
    p.add_argument("--items", required=True)
    p.add_argument("--generator", choices=sorted(VERIFIER), required=True)
    p.add_argument("--lists", type=Path, required=True)
    p.add_argument("--snapshot", type=Path, help="Qwen3-VL-8B snapshot (verifier of internvl3_8b)")
    p.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    {"items": cmd_items, "score": cmd_score}.get(a.cmd, lambda _a: ap.error("mode?"))(a)


if __name__ == "__main__":
    main()
