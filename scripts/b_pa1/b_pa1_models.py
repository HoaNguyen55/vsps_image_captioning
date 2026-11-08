#!/usr/bin/env python3
"""B-PA1-T1 HB-T1 model adapters and the host selftest (T1-T7, T9 of B_RUN_DOC §8.2). TIER 1 / DEV-EXPLORE (B-PA1-T1).
DRAFT, not read. Host GPU only: imported by b_pa1_gpu.py inside a block step or by `b_pa1_gpu.py hostcheck`; it is
never run on the laptop (no model, no GPU there). Every adapter follows its pinned model card's own snippet, with
pure greedy decoding (registry `decode`; reading 11). Loads are offline from the sha-checked snapshot only
(b_pa1_gpu.Models.snap); every torch.load runs with weights_only=True. Imports must work under both venvs
(transformers 4.53.3 main, 4.45.2 legacy), so every transformers import is inside its adapter.
"""
from __future__ import annotations

import gc
import json
import math
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import b_pa1_gpu as G  # noqa: E402

DEV = "cuda"


def T():  # noqa: N802
    import torch
    return torch


def weights_only_guard(torch) -> None:
    """As c_pvr_gpu.weights_only_guard: an explicit weights_only=False is a FAULT."""
    orig = getattr(torch.load, "_b_pa1_orig", torch.load)

    def load_wo(*a, **k):
        if k.get("weights_only", True) is not True:
            G.fault("torch.load called with weights_only != True")
        k["weights_only"] = True
        return orig(*a, **k)

    load_wo._b_pa1_orig = orig
    torch.load = load_wo
    torch.serialization.load = load_wo


def dtype(reg: dict, key: str):
    return getattr(T(), reg["models"][key]["dtype"])


def gen_kw(reg: dict) -> dict:
    d = reg["decode"]
    return {"max_new_tokens": d["max_new_tokens"], "do_sample": False, "num_beams": 1,
            "repetition_penalty": d["repetition_penalty"]}


def greedy(model, reg: dict) -> None:
    """Pure greedy whatever the model's generation_config.json says (MiniCPM's chat() passes no do_sample)."""
    gc_ = getattr(model, "generation_config", None)
    if gc_ is not None:
        gc_.do_sample, gc_.num_beams, gc_.repetition_penalty = False, 1, reg["decode"]["repetition_penalty"]
        for k in ("temperature", "top_p", "top_k"):
            if hasattr(gc_, k):
                setattr(gc_, k, None)


def free(obj) -> None:
    obj.__dict__.clear()
    gc.collect()
    T().cuda.empty_cache()


def n_params(model) -> int:
    return sum(p.numel() for p in model.parameters())


def decode_settings(model, reg: dict) -> dict:
    """CC-295 N6: what this captioner's generate() gets (gen_kw) and what its generation_config holds after greedy()."""
    gc_ = getattr(model, "generation_config", None)
    keys = ("do_sample", "num_beams", "repetition_penalty", "temperature", "top_p", "top_k", "max_new_tokens")
    return {"gen_kw": gen_kw(reg), "generation_config": {k: getattr(gc_, k, None) for k in keys} if gc_ else None}


# ---------------------------------------------------------------------------------------------- captioners
class Cap:
    def __init__(self, key: str, reg: dict, snap: Path):
        self.key, self.reg, self.snap, self.dt = key, reg, snap, dtype(reg, key)
        weights_only_guard(T())
        self.load()
        greedy(self.model, reg)

    def __call__(self, image, prompt: str) -> tuple[str, int]:
        with T().inference_mode():
            return self.gen(image, prompt)


class QwenVL(Cap):
    def load(self):
        from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
        self.proc = AutoProcessor.from_pretrained(self.snap, local_files_only=True)
        self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            self.snap, torch_dtype=self.dt, local_files_only=True).to(DEV).eval()

    def inputs(self, image, prompt):
        msgs = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": prompt}]}]
        text = self.proc.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        return self.proc(text=[text], images=[image], return_tensors="pt").to(DEV)

    def gen(self, image, prompt):
        inp = self.inputs(image, prompt)
        new = self.model.generate(**inp, **gen_kw(self.reg))[0, inp["input_ids"].shape[1]:]
        return self.proc.decode(new, skip_special_tokens=True).strip(), len(new)


class Gemma(Cap):
    def load(self):
        from transformers import AutoProcessor
        if self.reg["models"][self.key]["adapter"] == "gemma3n":
            from transformers import Gemma3nForConditionalGeneration as C
        else:
            from transformers import Gemma3ForConditionalGeneration as C
        self.proc = AutoProcessor.from_pretrained(self.snap, local_files_only=True)
        self.model = C.from_pretrained(self.snap, torch_dtype=self.dt, local_files_only=True).to(DEV).eval()

    def gen(self, image, prompt):
        msgs = [{"role": "user", "content": [{"type": "image", "image": image}, {"type": "text", "text": prompt}]}]
        inp = self.proc.apply_chat_template(msgs, add_generation_prompt=True, tokenize=True, return_dict=True,
                                            return_tensors="pt").to(DEV, dtype=self.dt)
        new = self.model.generate(**inp, **gen_kw(self.reg))[0, inp["input_ids"].shape[-1]:]
        return self.proc.decode(new, skip_special_tokens=True).strip(), len(new)


class Llava(Cap):
    def load(self):
        from transformers import AutoProcessor, LlavaForConditionalGeneration
        self.proc = AutoProcessor.from_pretrained(self.snap, local_files_only=True)
        self.model = LlavaForConditionalGeneration.from_pretrained(
            self.snap, torch_dtype=self.dt, local_files_only=True).to(DEV).eval()

    def gen(self, image, prompt):
        conv = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": prompt}]}]
        text = self.proc.apply_chat_template(conv, add_generation_prompt=True)
        inp = self.proc(images=image, text=text, return_tensors="pt").to(DEV, self.dt)
        new = self.model.generate(**inp, **gen_kw(self.reg))[0, inp["input_ids"].shape[1]:]
        return self.proc.decode(new, skip_special_tokens=True).strip(), len(new)


class Blip2(Cap):
    """mBLIP has no chat template; its card prompts with the plain instruction (reading 12)."""

    def load(self):
        from transformers import Blip2ForConditionalGeneration, Blip2Processor
        self.proc = Blip2Processor.from_pretrained(self.snap, local_files_only=True)
        self.model = Blip2ForConditionalGeneration.from_pretrained(
            self.snap, torch_dtype=self.dt, local_files_only=True).to(DEV).eval()

    def gen(self, image, prompt):
        inp = self.proc(image, prompt, return_tensors="pt").to(DEV, self.dt)
        out = self.model.generate(**inp, **gen_kw(self.reg))[0]
        return self.proc.decode(out, skip_special_tokens=True).strip(), len(out) - 1  # mT0: decoder start token


class InternVL(Cap):
    """Card snippet: dynamic 448 tiles, max_num 12, thumbnail, ImageNet mean/std, model.chat('<image>\\n' + q)."""

    def load(self):
        from transformers import AutoModel, AutoTokenizer
        self.model = AutoModel.from_pretrained(self.snap, torch_dtype=self.dt, trust_remote_code=True,
                                               local_files_only=True, use_flash_attn=False).eval().to(DEV)
        self.tok = AutoTokenizer.from_pretrained(self.snap, trust_remote_code=True, use_fast=False,
                                                 local_files_only=True)

    def pixels(self, image, size=448, max_num=12):
        import torchvision.transforms as TT
        from torchvision.transforms.functional import InterpolationMode
        tf = TT.Compose([TT.Resize((size, size), interpolation=InterpolationMode.BICUBIC), TT.ToTensor(),
                         TT.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))])
        w, h = image.size
        ratios = sorted({(i, j) for n in range(1, max_num + 1) for i in range(1, n + 1) for j in range(1, n + 1)
                         if i * j <= max_num}, key=lambda x: x[0] * x[1])
        best, diff = (1, 1), float("inf")
        for r in ratios:  # find_closest_aspect_ratio of the card, verbatim logic
            d = abs(w / h - r[0] / r[1])
            if d < diff:
                best, diff = r, d
            elif d == diff and w * h > 0.5 * size * size * r[0] * r[1]:
                best = r
        tw, th = size * best[0], size * best[1]
        im = image.resize((tw, th))
        tiles = [im.crop(((i % (tw // size)) * size, (i // (tw // size)) * size,
                          (i % (tw // size) + 1) * size, (i // (tw // size) + 1) * size))
                 for i in range(best[0] * best[1])]
        if len(tiles) != 1:
            tiles.append(image.resize((size, size)))
        return T().stack([tf(t) for t in tiles]).to(self.dt).to(DEV)

    def gen(self, image, prompt):
        resp = self.model.chat(self.tok, self.pixels(image), "<image>\n" + prompt, dict(gen_kw(self.reg)))
        return resp.strip(), len(self.tok(resp, add_special_tokens=False).input_ids)


class MiniCPM(Cap):
    def load(self):
        from transformers import AutoModel, AutoTokenizer
        self.model = AutoModel.from_pretrained(self.snap, trust_remote_code=True, attn_implementation="sdpa",
                                               torch_dtype=self.dt, local_files_only=True).eval().to(DEV)
        self.tok = AutoTokenizer.from_pretrained(self.snap, trust_remote_code=True, local_files_only=True)

    def gen(self, image, prompt):
        k = gen_kw(self.reg)  # chat(sampling=False) would default to num_beams 3, repetition_penalty 1.2
        resp = self.model.chat(msgs=[{"role": "user", "content": [image, prompt]}], tokenizer=self.tok,
                               sampling=False, max_new_tokens=k["max_new_tokens"], num_beams=1,
                               repetition_penalty=k["repetition_penalty"])
        return resp.strip(), len(self.tok(resp, add_special_tokens=False).input_ids)


class Phi3V(Cap):
    """Card: num_crops 16 for a single frame (reading 13); eager attention (no flash_attn on the host)."""

    def load(self):
        from transformers import AutoModelForCausalLM, AutoProcessor
        self.model = AutoModelForCausalLM.from_pretrained(self.snap, trust_remote_code=True, torch_dtype=self.dt,
                                                          _attn_implementation="eager",
                                                          local_files_only=True).to(DEV).eval()
        self.proc = AutoProcessor.from_pretrained(self.snap, trust_remote_code=True, num_crops=16,
                                                  local_files_only=True)

    def gen(self, image, prompt):
        msgs = [{"role": "user", "content": "<|image_1|>\n" + prompt}]
        text = self.proc.tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        inp = self.proc(text, [image], return_tensors="pt").to(DEV)
        new = self.model.generate(**inp, eos_token_id=self.proc.tokenizer.eos_token_id,
                                  **gen_kw(self.reg))[0, inp["input_ids"].shape[1]:]
        return self.proc.decode(new, skip_special_tokens=True).strip(), len(new)


class Molmo(Cap):
    def load(self):
        from transformers import AutoModelForCausalLM, AutoProcessor
        self.proc = AutoProcessor.from_pretrained(self.snap, trust_remote_code=True, local_files_only=True)
        self.model = AutoModelForCausalLM.from_pretrained(self.snap, trust_remote_code=True, torch_dtype=self.dt,
                                                          local_files_only=True).to(DEV).eval()

    def gen(self, image, prompt):
        from transformers import GenerationConfig
        inp = {k: v.to(DEV).unsqueeze(0) for k, v in self.proc.process(images=[image], text=prompt).items()}
        inp["images"] = inp["images"].to(self.dt)
        k = gen_kw(self.reg)
        gc_ = GenerationConfig(max_new_tokens=k["max_new_tokens"], do_sample=False, num_beams=1,
                               repetition_penalty=k["repetition_penalty"], stop_strings="<|endoftext|>")
        with T().autocast(DEV, dtype=self.dt):
            out = self.model.generate_from_batch(inp, gc_, tokenizer=self.proc.tokenizer)
        new = out[0, inp["input_ids"].size(1):]
        return self.proc.tokenizer.decode(new, skip_special_tokens=True).strip(), len(new)


ADAPTERS = {"qwen2_5_vl": QwenVL, "gemma3": Gemma, "gemma3n": Gemma, "llava": Llava, "blip2": Blip2,
            "internvl": InternVL, "minicpm": MiniCPM, "phi3v": Phi3V, "molmo": Molmo}


def captioner(key: str, reg: dict, snap: Path):
    m = reg["models"][key]
    if m["role"] not in ("candidate", "a4", "verifier") or not m["download"]:
        G.fault(f"{key} is not a downloaded captioner")
    return ADAPTERS[m["adapter"]](key, reg, snap)


# ---------------------------------------------------------------------------------------------- decomposer, scorer, clip
class Decomposer:
    def __init__(self, reg: dict, snap: Path):
        from transformers import AutoModelForCausalLM, AutoTokenizer
        weights_only_guard(T())
        k = reg["decomposer"]
        self.reg, self.tok = reg, AutoTokenizer.from_pretrained(snap, local_files_only=True, padding_side="left")
        self.model = AutoModelForCausalLM.from_pretrained(snap, torch_dtype=dtype(reg, k),
                                                          local_files_only=True).to(DEV).eval()
        greedy(self.model, reg)

    def __call__(self, prompts: list[str]) -> list[tuple[str, int]]:
        d = self.reg["decomposer_decode"]
        texts = [self.tok.apply_chat_template([{"role": "user", "content": p}], tokenize=False,
                                              add_generation_prompt=True) for p in prompts]
        enc = self.tok(texts, return_tensors="pt", padding=True).to(DEV)
        with T().inference_mode():
            out = self.model.generate(**enc, max_new_tokens=d["max_new_tokens"], do_sample=False, num_beams=1,
                                      repetition_penalty=d["repetition_penalty"], pad_token_id=self.tok.pad_token_id)
        new = out[:, enc["input_ids"].shape[1]:]
        n = (new != self.tok.pad_token_id).sum(dim=1).tolist()
        return list(zip(self.tok.batch_decode(new, skip_special_tokens=True), n))


class Scorer(QwenVL):
    """The verifier = the same-backbone judge (§7.1): one forward pass, softmax at the first answer position."""

    def __init__(self, reg: dict, snap: Path):
        super().__init__(reg["verifier"], reg, snap)
        self.enc = lambda w: self.proc.tokenizer.encode(w, add_special_tokens=False)

    def yn(self, lang: str):
        return G.yn_sets(self.enc, self.reg["token_words"][lang])

    def digits(self) -> list[int]:
        return G.digit_ids(self.enc, self.reg["digits"])

    def probs(self, image, prompt: str, ids) -> tuple[dict, int]:
        with T().inference_mode():
            logits = self.model(**self.inputs(image, prompt)).logits[0, -1].float()
            p = T().softmax(logits, dim=-1)
            return {i: p[i].item() for i in ids}, int(p.argmax().item())


class Clip:
    """M-CLIP XLM-R + ViT-H/14 as C-T1 (c_pvr_gpu.load_mclip): open_clip, fp32, XLM-R tokenizer BY NAME offline."""

    def __init__(self, reg: dict, snap: Path, xlmr: Path):
        import open_clip
        weights_only_guard(T())
        from huggingface_hub import try_to_load_from_cache
        for f in reg["models"]["xlmr"]["files"]:
            got = try_to_load_from_cache(reg["models"]["xlmr"]["repo"], f)
            if not isinstance(got, str) or Path(got).parent.resolve() != xlmr.resolve():
                G.fault(f"xlm-roberta-large {f} does not resolve BY NAME to the pinned snapshot")
        name = reg["clip_open_clip_name"]
        self.model, _, self.pre = open_clip.create_model_and_transforms(
            name, pretrained=str(snap / "open_clip_pytorch_model.bin"), precision="fp32")
        self.model = self.model.eval().to(DEV)
        self.tokz = open_clip.get_tokenizer(name)

    def __call__(self, image, text: str) -> tuple[float, bool]:
        torch = T()
        with torch.inference_mode():
            v = torch.nn.functional.normalize(self.model.encode_image(self.pre(image).unsqueeze(0).to(DEV)).float(), dim=-1)
            t = torch.nn.functional.normalize(self.model.encode_text(self.tokz([text]).to(DEV)).float(), dim=-1)
        return float((t @ v[0])[0]), len(self.tokz.tokenizer(text)["input_ids"]) > self.tokz.context_length


def decomposer(reg, snap):
    return Decomposer(reg, snap)


def scorer(reg, snap):
    return Scorer(reg, snap)


def clip(reg, snap, xlmr):
    return Clip(reg, snap, xlmr)


# ---------------------------------------------------------------------------------------------- host selftest
SYN_CAPTION = "Một hình chữ nhật đỏ đứng cạnh một hình tròn lam trên nền trắng."  # invented, NGRAM-scanned


def synthetic_image():
    from PIL import Image, ImageDraw
    im = Image.new("RGB", (448, 336), "white")
    d = ImageDraw.Draw(im)
    d.rectangle((40, 60, 200, 260), fill="red")
    d.ellipse((240, 80, 400, 240), fill="blue")
    return im


def vram(torch) -> dict:
    return {"allocated_gib": round(torch.cuda.memory_allocated() / 2 ** 30, 3),
            "peak_gib": round(torch.cuda.max_memory_allocated() / 2 ** 30, 3)}


def hostcheck(reg: dict, venv: str) -> int:
    """T1 GPU; T2 pinned load + params; T3 captioner echo; T4 Y/N sets; T5 digits; T6 M-CLIP; T7 one model at a
    time with a 1.5 GiB margin; T9 is the ids-only rule of b_pa1_gpu.rec_ok (selftest). T8 runs in b_pa1_job.sh."""
    torch, M = T(), G.Models(reg)
    total = torch.cuda.get_device_properties(0).total_memory / 2 ** 30
    name = torch.cuda.get_device_name(0)
    if torch.cuda.device_count() != 1 or "3090" not in name or total < 23:
        G.fault(f"T1: not one 24 GB RTX 3090 ({torch.cuda.device_count()} x {name}, {total:.1f} GiB)")
    img, rec = synthetic_image(), {"tier": G.B.LABEL, "venv": venv, "utc": G.utc(), "gpu": name,
                                   "total_gib": round(total, 2), "freeze": os.environ.get("B_PA1_FREEZE", ""), "gpu_uuid": os.environ.get("B_PA1_GPU", ""),
                                   "code": os.environ.get("B_PA1_CODE", ""), "models": {}}
    margin = 1.5

    def guard_load():
        if torch.cuda.memory_allocated() / 2 ** 30 > margin:
            G.fault("T7: GPU memory not released before the next load")
        torch.cuda.reset_peak_memory_stats()

    def peak_ok(key):
        v = vram(torch)
        if v["peak_gib"] + margin > total:
            G.fault(f"T7: {key} peak {v['peak_gib']} GiB + {margin} > {total:.1f}")
        return v
    prompt = reg["prompts"]["captioner"]["text"]
    for key, m in reg["models"].items():
        if m["venv"] != venv or not m["download"] or (m["role"] not in ("candidate", "a4") and key != reg["a4_first"]):
            continue
        guard_load()
        t0 = time.time()
        c = M.captioner(key)
        text, n_new = c(img, prompt)
        if not text or prompt[:24] in text:
            G.fault(f"T3: {key} gave an empty caption or echoed the prompt")
        rec["models"][key] = {"params": n_params(c.model), "safetensors_total": m["safetensors_total"],
                              "rule_s": m["safetensors_total"] <= reg["rule_s_max_params"], "chars": len(text),
                              "n_new": n_new, "vn": G.is_vn(text), "load_and_one_caption_sec": round(time.time() - t0, 1),
                              "decode": decode_settings(c.model, reg), **peak_ok(key)}
        M.free(c)
    if venv == "main":
        guard_load()
        d = M.decomposer()
        props, parse = G.props_of(d([G.render(reg["prompts"]["d1"]["text"], caption=SYN_CAPTION)])[0][0],
                                  reg["prop_types"])
        rec["models"][reg["decomposer"]] = {"params": n_params(d.model), "parse": parse, "n_props": len(props),
                                            **peak_ok("decomposer")}
        if parse == "fail":
            G.fault("decomposer output on the synthetic caption does not parse")
        M.free(d)
        guard_load()
        s = M.scorer()
        y_vi, n_vi = s.yn("vi")
        y_en, n_en = s.yn("en")
        dig = s.digits()  # T5
        sub, top = s.probs(img, G.render(reg["prompts"]["v1"]["text"], prop="Có hình tròn lam."),
                           y_vi | n_vi)
        yp = G.yes_prob(sub, top, y_vi, n_vi)
        ev = G.digit_ev(*s.probs(img, G.render(reg["prompts"]["jb"]["text"], caption=SYN_CAPTION), dig), dig)
        if yp["p_yes"] is None or not math.isfinite(yp["p_yes"]) or ev["ev"] is None:
            G.fault("T4/T5: verifier probabilities not finite")
        rec["models"][reg["verifier"]] = {"params": n_params(s.model), **peak_ok("verifier")}
        rec["t1_config_draft"] = {"verifier": reg["verifier"], "Y_vi": sorted(y_vi), "N_vi": sorted(n_vi),
                                  "Y_en": sorted(y_en), "N_en": sorted(n_en), "digits": dig,
                                  "words": {lang: {w: {"n_tokens": len(s.enc(w)), "first": s.proc.tokenizer.decode(
                                      [s.enc(w)[0]])} for side in ("Y", "N") for w in reg["token_words"][lang][side]}
                                      for lang in ("vi", "en")},
                                  "digit_tokens": [s.proc.tokenizer.decode([i]) for i in dig]}  # CC-295 N6
        M.free(s)
        guard_load()
        cl = M.clip()
        cos, _ = cl(img, SYN_CAPTION)
        if not math.isfinite(cos):
            G.fault("T6: M-CLIP cosine not finite")
        rec["models"]["mclip"] = {"cos_finite": True, "w": reg["clip_w"], **peak_ok("mclip")}
        M.free(cl)
    out = G.O() / f"HOSTCHECK_{venv}.json"
    out.write_text(json.dumps(rec, sort_keys=True, ensure_ascii=False) + "\n")
    print(json.dumps({"hostcheck": venv, "models": sorted(rec["models"])}))
    return 0
