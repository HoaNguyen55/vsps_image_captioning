#!/usr/bin/env python3
"""Decode LLaVA-1.5-7B-family checkpoints on a fixed COCO image-ID list (harness for N9 and the E1 K2 placebo).

Rebuilds the original LLaVA-1.5 inference path of haotian-liu/LLaVA (llava/eval/model_vqa.py: conv "llava_v1",
tokenizer_image_token, process_images with image_aspect_ratio "pad", batch-decode + strip) inside transformers'
LlavaForConditionalGeneration, so one venv serves every checkpoint, including two stacked LoRAs and LoRA on the
vision tower.

  --base   REPO@COMMIT  original-format full LLaVA checkpoint (LlavaLlamaForCausalLM): language model, mm_projector,
                        tokenizer. Examples: liuhaotian/llava-v1.5-7b, openbmb/RLAIF-V-7B.
  --vision REPO@COMMIT  the CLIP tower that the LLaVA codebase loads at run time (openai/clip-vit-large-patch14-336),
                        with its image processor. Vision weights saved inside --base are NOT used (the LLaVA builder
                        ignores them too); their max |difference| from --vision is recorded.
  --lora   REPO@COMMIT  repeatable, applied in the given order. Original-format LLaVA LoRA folder: adapter_config.json,
                        adapter_model.{safetensors,bin}, optional non_lora_trainables.bin. non_lora_trainables are
                        loaded first, then each LoRA pair is merged, W += (lora_alpha / r) * B @ A, on language-model,
                        projector and vision-tower modules.
  --drop-vision-lora    skip the vision-tower LoRA modules of every --lora. This reproduces the LLaVA builder, which
                        delay-loads the vision tower, so PeftModel never sees those modules (e.g. POVID's own
                        povid_infer.py). Skipped modules are counted in the output.
Every tensor of the HF model must be written by the loader (coverage check). The HF vocabulary is padded from 32,000 to
32,064 for the <image> token (id 32000); the extra rows are zeroed and their logits suppressed at generation.
All repos are pinned (40-hex commit). The output JSON records the commit and sha256 of every file read, the image list
and its sha256, the sha256 of every image, and one caption per image.
Needs: torch, transformers (tested 4.51.3), huggingface_hub, safetensors, sentencepiece, protobuf, Pillow.

GPU run:
  python3 scripts/lvlm/decode_llava.py --label NAME --out OUT.json \\
      --image-ids data/coco_probe/chair500_ids.txt --image-dir DIR \\
      --base liuhaotian/llava-v1.5-7b@<40-hex> --vision openai/clip-vit-large-patch14-336@<40-hex> \\
      [--lora REPO@<40-hex> ...] [--drop-vision-lora] [--do-sample --temperature T --top-p P --top-k K --seed S] \\
      --max-new-tokens 512 --batch-size 8
  Resumable: finished batches are appended to OUT.json.partial.jsonl and skipped on restart (same configuration only).
  Batches are fixed slices of the id list, so a resumed run decodes the same batches with the same seeds.
CPU self-test (no GPU, no network): python3 scripts/lvlm/decode_llava.py --selftest
  Pure-Python checks always run; tensor checks and a tiny random LLaVA end-to-end run need torch + transformers.
"""
import argparse, contextlib, hashlib, io, json, os, re, subprocess, sys, time
from pathlib import Path

SCHEMA = 'vsps.decode_llava.v1'
SYSTEM = ("A chat between a curious human and an artificial intelligence assistant. "
          "The assistant gives helpful, detailed, and polite answers to the human's questions.")
QUESTION = 'Please describe this image in detail.'
PROMPT = SYSTEM + ' USER: <image>\n' + QUESTION + ' ASSISTANT:'   # conv_llava_v1.get_prompt(), LLaVA model_vqa.py
N_VOCAB = 32000          # original LLaVA-1.5 / Vicuna vocabulary
HF_VOCAB = 32064         # padded HF vocabulary (llava-hf layout); id 32000 = <image>
IMAGE_TOKEN = 32000
PIN_RE = re.compile(r'^([A-Za-z0-9][\w.-]*/[\w.-]+)@([0-9a-f]{40})$')
LORA_RE = re.compile(r'^base_model\.model\.(?P<mod>.+)\.lora_(?P<ab>[AB])(?:\.default)?\.weight$')
LAYOUTS = {  # transformers <= 4.51 (A) and >= 4.52 (B) parameter names of LlavaForConditionalGeneration
    'A': {'lm': 'language_model.model.', 'head': 'language_model.lm_head.weight', 'proj': 'multi_modal_projector.',
          'vis': 'vision_tower.'},
    'B': {'lm': 'model.language_model.', 'head': 'lm_head.weight', 'proj': 'model.multi_modal_projector.',
          'vis': 'model.vision_tower.'},
}
BASE_FIELDS = {'architectures': ['LlavaLlamaForCausalLM'], 'mm_projector_type': 'mlp2x_gelu',
               'mm_vision_select_layer': -2, 'mm_vision_select_feature': 'patch', 'image_aspect_ratio': 'pad',
               'mm_use_im_start_end': False, 'mm_use_im_patch_token': False, 'vocab_size': N_VOCAB}
MM_FIELDS = ('mm_projector_type', 'mm_vision_select_layer', 'mm_vision_select_feature', 'image_aspect_ratio',
             'mm_use_im_start_end', 'mm_use_im_patch_token')


# ---------------------------------------------------------------- pure-Python helpers
def pin(s):
    m = PIN_RE.match(s)
    if not m:
        raise argparse.ArgumentTypeError(f'{s!r}: expected REPO@<40-hex commit>')
    return {'repo': m.group(1), 'revision': m.group(2)}


def parse_args(argv):
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('--selftest', action='store_true')
    p.add_argument('--label')
    p.add_argument('--out', type=Path)
    p.add_argument('--image-ids', type=Path)
    p.add_argument('--image-dir', type=Path)
    p.add_argument('--base', type=pin)
    p.add_argument('--vision', type=pin)
    p.add_argument('--lora', type=pin, action='append', default=[])
    p.add_argument('--drop-vision-lora', action='store_true')
    p.add_argument('--do-sample', action='store_true')
    p.add_argument('--temperature', type=float)
    p.add_argument('--top-p', type=float)
    p.add_argument('--top-k', type=int)
    p.add_argument('--seed', type=int)
    p.add_argument('--max-new-tokens', type=int, default=512)
    p.add_argument('--batch-size', type=int, default=8)
    p.add_argument('--dtype', choices=['float16'], default='float16')
    p.add_argument('--limit', type=int, help='debug only: first N ids; recorded in the output')
    a = p.parse_args(argv)
    if a.selftest:
        return a
    missing = [n for n in ('label', 'out', 'image_ids', 'image_dir', 'base', 'vision') if getattr(a, n) is None]
    if missing:
        p.error('missing: ' + ', '.join('--' + n.replace('_', '-') for n in missing))
    samp = {n: getattr(a, n) for n in ('temperature', 'top_p', 'top_k', 'seed')}
    if a.do_sample and any(v is None for v in samp.values()):
        p.error('--do-sample needs explicit --temperature, --top-p, --top-k and --seed (no hidden defaults)')
    if not a.do_sample and any(v is not None for v in samp.values()):
        p.error('--temperature/--top-p/--top-k/--seed are only valid with --do-sample (greedy otherwise)')
    if a.drop_vision_lora and not a.lora:
        p.error('--drop-vision-lora needs at least one --lora')
    if a.max_new_tokens < 1 or a.batch_size < 1:
        p.error('--max-new-tokens and --batch-size must be >= 1')
    return a


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 23), b''):
            h.update(b)
    return h.hexdigest()


def read_ids(path):
    ids = [int(x) for x in Path(path).read_text().split()]
    if len(set(ids)) != len(ids):
        raise ValueError(f'{path}: duplicate image ids')
    return ids


def image_file(image_dir, i):
    for name in (f'COCO_val2014_{i:012d}.jpg', f'{i:012d}.jpg'):
        f = Path(image_dir) / name
        if f.is_file():
            return f
    raise FileNotFoundError(f'image {i} not in {image_dir} (COCO_val2014_%012d.jpg or %012d.jpg)')


def expand2square(img, background):
    """LLaVA mm_utils.expand2square (image_aspect_ratio 'pad')."""
    from PIL import Image
    w, h = img.size
    if w == h:
        return img
    side = max(w, h)
    out = Image.new(img.mode, (side, side), background)
    out.paste(img, (0, (w - h) // 2) if w > h else ((h - w) // 2, 0))
    return out


def prompt_template_ids(tokenize, bos_id):
    """LLaVA tokenizer_image_token(PROMPT): BOS + chunk0[1:] + [-200] + chunk1[1:] (-200 = LLaVA IMAGE_TOKEN_INDEX)."""
    chunks = [tokenize(c) for c in PROMPT.split('<image>')]
    assert len(chunks) == 2 and chunks[0][0] == bos_id and chunks[1][0] == bos_id, 'expected a BOS-prefixed tokenizer'
    return [bos_id] + chunks[0][1:] + [-200] + chunks[1][1:]


def image_input_ids(template, n_image_tokens):
    """The LLaVA template with its single image placeholder expanded to n_image_tokens <image> ids (HF Llava input)."""
    assert template.count(-200) == 1
    i = template.index(-200)
    return template[:i] + [IMAGE_TOKEN] * n_image_tokens + template[i + 1:]


def orig_to_hf(key, layout):
    """Original LLaVA parameter name -> HF LlavaForConditionalGeneration name; None for rotary inv_freq buffers."""
    L = LAYOUTS[layout]
    if key.endswith('rotary_emb.inv_freq'):
        return None
    if key == 'lm_head.weight':
        return L['head']
    if key.startswith('model.mm_projector.'):
        idx, rest = key[len('model.mm_projector.'):].split('.', 1)
        return L['proj'] + {'0': 'linear_1', '2': 'linear_2'}[idx] + '.' + rest
    if key.startswith('model.vision_tower.vision_tower.'):
        return L['vis'] + key[len('model.vision_tower.vision_tower.'):]
    if key.startswith('model.') and not key.startswith('model.vision_tower'):
        return L['lm'] + key[len('model.'):]
    raise KeyError(f'unmapped original LLaVA key {key!r}')


def lora_pairs(keys):
    """{module: {'A': key, 'B': key}} from adapter keys; any other adapter key is an error (DoRA, bias, embeddings)."""
    pairs = {}
    for k in keys:
        m = LORA_RE.match(k)
        if not m:
            raise KeyError(f'unsupported adapter key {k!r}')
        pairs.setdefault(m.group('mod'), {})[m.group('ab')] = k
    bad = [m for m, d in pairs.items() if set(d) != {'A', 'B'}]
    if bad:
        raise KeyError(f'incomplete LoRA pairs: {bad[:3]}')
    return pairs


def lora_scale(cfg):
    if cfg.get('peft_type') != 'LORA' or cfg.get('use_rslora') or cfg.get('use_dora') or cfg.get('fan_in_fan_out') \
            or cfg.get('bias', 'none') != 'none' or cfg.get('modules_to_save'):
        raise ValueError(f'unsupported adapter_config: {cfg}')
    return cfg['lora_alpha'] / cfg['r']


def component(hf_key, layout):
    L = LAYOUTS[layout]
    return 'vision' if hf_key.startswith(L['vis']) else 'projector' if hf_key.startswith(L['proj']) else 'language_model'


REQUIRED = {
    'top': {'schema': str, 'label': str, 'created_utc': str, 'script': dict, 'provenance': dict, 'model': dict,
            'decoding': dict, 'images': dict, 'preds': list},
    'decoding': {'prompt': str, 'do_sample': bool, 'max_new_tokens': int, 'batch_size': int, 'num_beams': int},
    'images': {'id_list_path': str, 'id_list_sha256': str, 'n_ids': int, 'n_decoded': int},
    'pred': {'image_id': int, 'image_file': str, 'image_sha256': str, 'caption': str, 'n_new_tokens': int,
             'hit_max_new_tokens': bool},
}


def validate_output(d):
    def need(obj, spec, where):
        for k, t in spec.items():
            if not isinstance(obj.get(k), t):
                raise ValueError(f'{where}.{k}: expected {t.__name__}, got {type(obj.get(k)).__name__}')
    need(d, REQUIRED['top'], 'out')
    if d['schema'] != SCHEMA:
        raise ValueError('schema mismatch')
    need(d['decoding'], REQUIRED['decoding'], 'decoding')
    need(d['images'], REQUIRED['images'], 'images')
    for i, r in enumerate(d['preds']):
        need(r, REQUIRED['pred'], f'preds[{i}]')
    ids = [r['image_id'] for r in d['preds']]
    if len(ids) != len(set(ids)) or len(ids) != d['images']['n_decoded']:
        raise ValueError('preds: duplicate ids or count != images.n_decoded')
    for k in ('base', 'vision', 'loras', 'drop_vision_lora', 'files_sha256'):
        if k not in d['model']:
            raise ValueError(f'model.{k} missing')
    return True


# ---------------------------------------------------------------- tensor helpers (torch)
def build_config(base_cfg, clip_vision_cfg):
    """LlavaConfig from the --base config.json (text dims) and the CLIP vision config; no skeleton weights."""
    from transformers import LlamaConfig, LlavaConfig
    bad = {k: base_cfg.get(k) for k, v in BASE_FIELDS.items() if base_cfg.get(k) != v}
    if bad:
        raise ValueError(f'--base is not an original LLaVA-1.5 checkpoint: {bad}')
    text = LlamaConfig(
        vocab_size=HF_VOCAB, hidden_size=base_cfg['hidden_size'], intermediate_size=base_cfg['intermediate_size'],
        num_hidden_layers=base_cfg['num_hidden_layers'], num_attention_heads=base_cfg['num_attention_heads'],
        num_key_value_heads=base_cfg.get('num_key_value_heads', base_cfg['num_attention_heads']),
        hidden_act=base_cfg.get('hidden_act', 'silu'), max_position_embeddings=base_cfg['max_position_embeddings'],
        rms_norm_eps=base_cfg['rms_norm_eps'], rope_theta=base_cfg.get('rope_theta', 10000.0),
        rope_scaling=base_cfg.get('rope_scaling'), tie_word_embeddings=False, bos_token_id=1, eos_token_id=2,
        pad_token_id=0)
    return LlavaConfig(vision_config=clip_vision_cfg, text_config=text, image_token_index=IMAGE_TOKEN,
                       projector_hidden_act='gelu', vision_feature_layer=base_cfg['mm_vision_select_layer'],
                       vision_feature_select_strategy='default', tie_word_embeddings=False, vocab_size=HF_VOCAB)


class Loader:
    """Writes tensors into a LlavaForConditionalGeneration and keeps the coverage / provenance record."""

    def __init__(self, model):
        import torch
        self.torch = torch
        self.sd = model.state_dict()
        self.layout = 'A' if 'language_model.lm_head.weight' in self.sd else 'B'
        L = LAYOUTS[self.layout]
        if L['head'] not in self.sd:
            raise RuntimeError('unknown LlavaForConditionalGeneration layout')
        if self.sd[L['head']].data_ptr() == self.sd[L['lm'] + 'embed_tokens.weight'].data_ptr():
            raise RuntimeError('lm_head is tied to embed_tokens')
        self.written = set()
        self.log = {'vision_saved_in_base_max_abs_diff': None, 'non_lora_loaded': [], 'lora_merged': []}

    def put(self, hf_key, t):
        p = self.sd[hf_key]
        t = t.to(device=p.device, dtype=p.dtype)
        if t.shape == p.shape:
            p.copy_(t)
        elif hf_key.endswith(('embed_tokens.weight', 'lm_head.weight')) and t.shape[1:] == p.shape[1:] \
                and t.shape[0] == N_VOCAB and p.shape[0] == HF_VOCAB:
            p[:N_VOCAB].copy_(t)
            p[N_VOCAB:].zero_()
        else:
            raise ValueError(f'{hf_key}: shape {tuple(t.shape)} != {tuple(p.shape)}')
        self.written.add(hf_key)

    def load_vision(self, tensors):
        vis = LAYOUTS[self.layout]['vis']
        for k, t in tensors:
            if not k.startswith('vision_model.'):
                continue                      # CLIP text tower, projections, logit_scale
            hk = vis + k
            if hk not in self.sd:
                if k.endswith('position_ids'):
                    continue                  # non-persistent buffer in current transformers
                raise KeyError(f'vision key {k!r} has no target')
            self.put(hk, t)

    def load_base(self, tensors):
        worst = None
        for k, t in tensors:
            hk = orig_to_hf(k, self.layout)
            if hk is None:
                continue
            if hk not in self.sd:
                raise KeyError(f'{k!r} -> {hk!r} not in model')
            if k.startswith('model.vision_tower.'):
                if hk not in self.written:
                    raise RuntimeError('load --vision before --base')
                d = (self.sd[hk].float() - t.to(self.sd[hk].device).float()).abs().max().item()
                worst = d if worst is None else max(worst, d)
                continue                      # not used, as in the LLaVA builder
            self.put(hk, t)
        self.log['vision_saved_in_base_max_abs_diff'] = worst

    def check_coverage(self):
        missing = sorted(set(self.sd) - self.written)
        if missing:
            raise RuntimeError(f'{len(missing)} model tensors not loaded, e.g. {missing[:5]}')

    def load_non_lora(self, tensors, tag):
        n = 0
        for k, t in tensors:
            k2 = k[len('base_model.model.'):] if k.startswith('base_model.model.') else k
            hk = orig_to_hf(k2, self.layout)
            if hk is None or hk not in self.sd:
                raise KeyError(f'non_lora key {k!r} has no target')
            self.put(hk, t)
            n += 1
        self.log['non_lora_loaded'].append({'lora': tag, 'n_tensors': n})

    def merge_lora(self, adapter, scale, tag, drop_vision=False):
        torch = self.torch
        merged, skipped = {}, {}
        for mod, ab in lora_pairs(list(adapter)).items():
            hk = orig_to_hf(mod + '.weight', self.layout)
            if hk is None or hk not in self.sd:
                raise KeyError(f'LoRA module {mod!r} has no target')
            c = component(hk, self.layout)
            if drop_vision and c == 'vision':
                skipped[c] = skipped.get(c, 0) + 1
                continue
            W = self.sd[hk]
            A = adapter[ab['A']].to(W.device, torch.float32)
            B = adapter[ab['B']].to(W.device, torch.float32)
            delta = (B @ A) * scale
            if delta.shape != W.shape:
                raise ValueError(f'{mod}: LoRA delta {tuple(delta.shape)} != weight {tuple(W.shape)}')
            W.copy_((W.float() + delta).to(W.dtype))
            merged[c] = merged.get(c, 0) + 1
        self.log['lora_merged'].append({'lora': tag, 'scale': scale, 'modules_by_component': merged,
                                        'skipped_by_component': skipped})


class SuppressExtraVocab:
    """Logits processor: ids >= 32000 do not exist in the original model."""

    def __call__(self, input_ids, scores):
        scores[:, N_VOCAB:] = -float('inf')
        return scores


def generate_batch(model, ids_row, pixel_values, args, eos_id, batch_start):
    """One generate() call for len(pixel_values) images that share the same prompt ids (so no padding is needed)."""
    import torch
    from transformers import GenerationConfig, LogitsProcessorList
    n = pixel_values.shape[0]
    param = next(model.parameters())
    input_ids = torch.tensor([ids_row] * n, dtype=torch.long, device=param.device)
    gen = dict(max_new_tokens=args.max_new_tokens, num_beams=1, do_sample=bool(args.do_sample),
               eos_token_id=eos_id, pad_token_id=0, use_cache=True)
    if args.do_sample:
        gen.update(temperature=args.temperature, top_p=args.top_p, top_k=args.top_k)
        torch.manual_seed(args.seed * 1_000_003 + batch_start)       # per batch: resume-safe and batch-local
    with torch.inference_mode():
        out = model.generate(input_ids=input_ids, attention_mask=torch.ones_like(input_ids),
                             pixel_values=pixel_values.to(param.device, param.dtype),
                             generation_config=GenerationConfig(**gen),
                             logits_processor=LogitsProcessorList([SuppressExtraVocab()]))
    rows = []
    for seq in out[:, input_ids.shape[1]:].tolist():
        cut = seq.index(eos_id) if eos_id in seq else len(seq)
        rows.append((seq[:cut], cut + (1 if cut < len(seq) else 0), cut == len(seq)))
    return rows


def run_decoding(model, tok_decode, ids_row, eos_id, proc, items, args, done, sink, open_image):
    """items: [(image_id, file name, sha256, source)], decoded in fixed slices of batch_size; sink(rows) stores them."""
    import torch
    bg = tuple(int(x * 255) for x in proc.image_mean)
    for s in range(0, len(items), args.batch_size):
        chunk = items[s:s + args.batch_size]
        n_done = sum(it[0] in done for it in chunk)
        if n_done == len(chunk):
            continue
        if n_done:
            raise RuntimeError(f'batch at {s} is partly done: the partial file is inconsistent')
        pix = torch.stack([proc.preprocess(expand2square(open_image(src), bg), return_tensors='pt')['pixel_values'][0]
                           for _, _, _, src in chunk])
        rows = generate_batch(model, ids_row, pix, args, eos_id, s)
        sink([{'image_id': i, 'image_file': f, 'image_sha256': h, 'caption': tok_decode(toks).strip(),
               'n_new_tokens': n, 'hit_max_new_tokens': hit}
              for (i, f, h, _), (toks, n, hit) in zip(chunk, rows)])


# ---------------------------------------------------------------- real run (GPU)
def snapshot(spec, patterns):
    from huggingface_hub import snapshot_download
    path = Path(snapshot_download(spec['repo'], revision=spec['revision'], allow_patterns=patterns))
    if path.name != spec['revision']:
        raise RuntimeError(f'{spec["repo"]}: snapshot {path.name} != requested {spec["revision"]}')
    return path


def tensors_from(files):
    import torch
    for f in files:
        if f.suffix == '.safetensors':
            from safetensors import safe_open
            with safe_open(str(f), framework='pt') as h:
                for k in h.keys():
                    yield k, h.get_tensor(k)
        else:
            try:
                sd = torch.load(f, map_location='cpu', weights_only=True, mmap=True)
            except RuntimeError:
                sd = torch.load(f, map_location='cpu', weights_only=True)
            yield from sd.items()
            del sd


def weight_files(folder):
    for idx in ('model.safetensors.index.json', 'pytorch_model.bin.index.json'):
        if (folder / idx).is_file():
            return [folder / f for f in sorted(set(json.loads((folder / idx).read_text())['weight_map'].values()))]
    for one in ('model.safetensors', 'pytorch_model.bin'):
        if (folder / one).is_file():
            return [folder / one]
    raise FileNotFoundError(f'no weights in {folder}')


def provenance():
    here = Path(__file__).resolve().parent

    def git(*a):
        try:
            return subprocess.run(['git', '--no-optional-locks', '-C', str(here), *a], capture_output=True, text=True,
                                  check=True).stdout.strip()
        except Exception:
            return None
    status = git('status', '--porcelain', '--untracked-files=no')
    return {'git_head': git('rev-parse', 'HEAD'), 'git_dirty': None if status is None else bool(status),
            'machine_id': os.environ.get('VSPS_MACHINE_ID')}


def main(args):
    for mod in ('sentencepiece', 'google.protobuf'):    # the slow LlamaTokenizer with legacy=False needs both
        try:
            __import__(mod)
        except ImportError:
            sys.exit(f'missing dependency {mod}: pip install sentencepiece protobuf')
    import torch, transformers
    from transformers import CLIPConfig, CLIPImageProcessor, LlamaTokenizer, LlavaForConditionalGeneration
    from PIL import Image
    t0 = time.time()
    created = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    files = {}

    def rec(repo, folder, f):
        files[f'{repo}/{f.relative_to(folder)}'] = sha256_file(f)
        return f

    vis_dir = snapshot(args.vision, ['config.json', 'preprocessor_config.json', 'pytorch_model.bin'])
    base_dir = snapshot(args.base, ['config.json', 'generation_config.json', 'model*.safetensors', 'pytorch_model*.bin',
                                    '*.index.json', 'tokenizer.model', 'tokenizer_config.json',
                                    'special_tokens_map.json'])
    lora_dirs = [snapshot(s, ['adapter_config.json', 'adapter_model.safetensors', 'adapter_model.bin',
                              'non_lora_trainables.bin', 'config.json']) for s in args.lora]

    base_cfg = json.loads(rec(args.base['repo'], base_dir, base_dir / 'config.json').read_text())
    if base_cfg.get('mm_vision_tower') != args.vision['repo']:
        raise ValueError(f'--base expects vision tower {base_cfg.get("mm_vision_tower")}, got {args.vision["repo"]}')
    for spec, d in zip(args.lora, lora_dirs):
        lcfg = json.loads(rec(spec['repo'], d, d / 'config.json').read_text()) if (d / 'config.json').is_file() else {}
        diff = {k: (lcfg.get(k), base_cfg.get(k)) for k in MM_FIELDS if lcfg and lcfg.get(k) != base_cfg.get(k)}
        if diff:
            raise ValueError(f'{spec["repo"]}: multimodal config differs from --base: {diff}')
    rec(args.vision['repo'], vis_dir, vis_dir / 'config.json')
    rec(args.vision['repo'], vis_dir, vis_dir / 'preprocessor_config.json')
    cfg = build_config(base_cfg, CLIPConfig.from_pretrained(vis_dir).vision_config)
    proc = CLIPImageProcessor.from_pretrained(vis_dir)
    tok = LlamaTokenizer.from_pretrained(base_dir)            # slow tokenizer, as the LLaVA builder (use_fast=False)
    for f in ('tokenizer.model', 'tokenizer_config.json', 'special_tokens_map.json'):
        if (base_dir / f).is_file():
            rec(args.base['repo'], base_dir, base_dir / f)
    if (tok.bos_token_id, tok.eos_token_id, len(tok)) != (1, 2, N_VOCAB):
        raise ValueError(f'unexpected tokenizer: bos {tok.bos_token_id}, eos {tok.eos_token_id}, size {len(tok)}')

    dtype = getattr(torch, args.dtype)
    with torch.device('cuda'):
        model = LlavaForConditionalGeneration._from_config(cfg, torch_dtype=dtype)
    model.eval()
    if any(p.device.type != 'cuda' for p in model.parameters()):
        raise RuntimeError('model not on cuda')
    ld = Loader(model)
    with torch.no_grad():
        ld.load_vision(tensors_from([rec(args.vision['repo'], vis_dir, vis_dir / 'pytorch_model.bin')]))
        ld.load_base(tensors_from([rec(args.base['repo'], base_dir, f) for f in weight_files(base_dir)]))
        ld.check_coverage()
        for spec, d in zip(args.lora, lora_dirs):
            tag = f'{spec["repo"]}@{spec["revision"]}'
            acfg = json.loads(rec(spec['repo'], d, d / 'adapter_config.json').read_text())
            if (d / 'non_lora_trainables.bin').is_file():
                ld.load_non_lora(tensors_from([rec(spec['repo'], d, d / 'non_lora_trainables.bin')]), tag)
            wf = d / 'adapter_model.safetensors' if (d / 'adapter_model.safetensors').is_file() else d / 'adapter_model.bin'
            ld.merge_lora(dict(tensors_from([rec(spec['repo'], d, wf)])), lora_scale(acfg), tag, args.drop_vision_lora)

    n_img_tok = (cfg.vision_config.image_size // cfg.vision_config.patch_size) ** 2
    template = prompt_template_ids(lambda c: tok(c).input_ids, tok.bos_token_id)
    ids_row = image_input_ids(template, n_img_tok)
    all_ids = read_ids(args.image_ids)
    ids = all_ids[:args.limit] if args.limit else all_ids
    items = []
    for i in ids:
        f = image_file(args.image_dir, i)
        items.append((i, f.name, sha256_file(f), f))

    decoding = {'prompt': PROMPT, 'conv_template': 'llava_v1', 'question': QUESTION, 'do_sample': bool(args.do_sample),
                'temperature': args.temperature, 'top_p': args.top_p, 'top_k': args.top_k, 'seed': args.seed,
                'seed_rule': 'torch.manual_seed(seed * 1000003 + index of the first image of the batch)' if args.do_sample else None,
                'max_new_tokens': args.max_new_tokens, 'num_beams': 1, 'batch_size': args.batch_size, 'dtype': args.dtype,
                'image_preprocess': 'expand2square(background = image_mean * 255) then CLIPImageProcessor.preprocess',
                'suppressed_token_ids': [N_VOCAB, HF_VOCAB - 1], 'n_image_tokens': n_img_tok,
                'prompt_template_ids': template,
                'prompt_template_ids_sha256': hashlib.sha256(json.dumps(template).encode()).hexdigest()}
    model_rec = {'base': args.base, 'vision': args.vision, 'loras': args.lora, 'drop_vision_lora': args.drop_vision_lora,
                 'layout': ld.layout, **ld.log, 'files_sha256': files}
    run_key = hashlib.sha256(json.dumps([model_rec, decoding, str(args.image_ids), ids], sort_keys=True).encode()).hexdigest()

    part = Path(str(args.out) + '.partial.jsonl')
    done = {}
    if part.is_file():
        lines = part.read_text().splitlines()
        if not lines or json.loads(lines[0]).get('run_key') != run_key:
            raise RuntimeError(f'{part} belongs to a different configuration; move it away to restart')
        for line in lines[1:]:
            r = json.loads(line)
            done[r['image_id']] = r
    else:
        part.write_text(json.dumps({'run_key': run_key}) + '\n')

    def sink(rows):
        with part.open('a') as fh:
            for r in rows:
                fh.write(json.dumps(r) + '\n')
                done[r['image_id']] = r
            fh.flush()
            os.fsync(fh.fileno())
        print(f'{len(done)}/{len(items)} images', flush=True)

    t1 = time.time()
    run_decoding(model, lambda t: tok.decode(t, skip_special_tokens=True), ids_row, tok.eos_token_id, proc, items, args,
                 done, sink, lambda f: Image.open(f).convert('RGB'))
    out = {'schema': SCHEMA, 'label': args.label, 'created_utc': created,
           'finished_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
           'script': {'path': 'scripts/lvlm/decode_llava.py', 'sha256': sha256_file(__file__)},
           'provenance': {**provenance(), 'argv': sys.argv[1:], 'python': sys.version.split()[0],
                          'torch': torch.__version__, 'transformers': transformers.__version__,
                          'cuda': torch.version.cuda, 'gpu': torch.cuda.get_device_name(0),
                          'seconds_load': round(t1 - t0, 1), 'seconds_decode': round(time.time() - t1, 1)},
           'model': model_rec, 'decoding': decoding,
           'images': {'id_list_path': str(args.image_ids), 'id_list_sha256': sha256_file(args.image_ids),
                      'n_ids': len(all_ids), 'limit': args.limit, 'n_decoded': len(items),
                      'image_dir': str(args.image_dir),
                      'image_sha256_digest': hashlib.sha256(''.join(h for _, _, h, _ in items).encode()).hexdigest()},
           'preds': [done[i] for i, _, _, _ in items]}
    validate_output(out)
    tmp = Path(str(args.out) + '.tmp')
    tmp.write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
    tmp.replace(args.out)
    Path(str(args.out) + '.sha256').write_text(f'{sha256_file(args.out)}  {Path(args.out).name}\n')
    print(f'wrote {args.out}')


# ---------------------------------------------------------------- self-test (CPU, offline)
def selftest():
    ok = []

    def check(name, cond):
        if not cond:
            raise AssertionError(name)
        ok.append(name)

    def rejected(name, fn, exc):
        try:
            with contextlib.redirect_stderr(io.StringIO()):
                fn()
        except exc:
            ok.append(name)
            return
        raise AssertionError(name)

    r = '0123456789abcdef0123456789abcdef01234567'
    run = ['--label', 'x', '--out', 'o.json', '--image-ids', 'i.txt', '--image-dir', 'd', '--base', f'a/b@{r}',
           '--vision', f'c/d@{r}']
    a = parse_args(run + ['--lora', f'e/f@{r}', '--lora', f'g/h@{r}', '--drop-vision-lora'])
    check('args: greedy run, two LoRAs kept in order', not a.do_sample and [x['repo'] for x in a.lora] == ['e/f', 'g/h']
          and a.drop_vision_lora and a.max_new_tokens == 512 and a.base == {'repo': 'a/b', 'revision': r})
    a = parse_args(run + ['--do-sample', '--temperature', '1.0', '--top-p', '1.0', '--top-k', '0', '--seed', '1'])
    check('args: sampling run', a.do_sample and (a.temperature, a.top_p, a.top_k, a.seed) == (1.0, 1.0, 0, 1))
    for name, bad in (('unpinned revision', ['--base', 'a/b@main']), ('sampling without all settings', ['--do-sample', '--temperature', '1']),
                      ('sampling settings without --do-sample', ['--temperature', '1']),
                      ('--drop-vision-lora without --lora', ['--drop-vision-lora'])):
        rejected(f'args rejected: {name}', lambda bad=bad: parse_args(run + bad), SystemExit)
    rejected('args rejected: missing required', lambda: parse_args(['--label', 'x']), SystemExit)

    check('prompt = LLaVA conv llava_v1', PROMPT == "A chat between a curious human and an artificial intelligence "
          "assistant. The assistant gives helpful, detailed, and polite answers to the human's questions. "
          "USER: <image>\nPlease describe this image in detail. ASSISTANT:")
    fake = lambda s: [1] + [3 + (sum(map(ord, w)) % 31000) for w in s.split()]
    tpl = prompt_template_ids(fake, 1)
    c0, c1 = fake(PROMPT.split('<image>')[0]), fake(PROMPT.split('<image>')[1])
    check('tokenizer_image_token layout', tpl == [1] + c0[1:] + [-200] + c1[1:]
          and image_input_ids(tpl, 4) == [1] + c0[1:] + [IMAGE_TOKEN] * 4 + c1[1:])

    try:
        from PIL import Image
        bg = (122, 116, 104)
        wide = expand2square(Image.new('RGB', (40, 20), (255, 0, 0)), bg)
        tall = expand2square(Image.new('RGB', (10, 30), (0, 255, 0)), bg)
        check('expand2square wide', wide.size == (40, 40) and wide.getpixel((0, 0)) == bg and wide.getpixel((0, 10)) == (255, 0, 0))
        check('expand2square tall', tall.size == (30, 30) and tall.getpixel((0, 0)) == bg and tall.getpixel((10, 0)) == (0, 255, 0))
    except ImportError:
        ok.append('SKIP expand2square (Pillow not importable)')

    for lay in 'AB':
        L = LAYOUTS[lay]
        check(f'key map layout {lay}', orig_to_hf('model.layers.3.self_attn.q_proj.weight', lay) == L['lm'] + 'layers.3.self_attn.q_proj.weight'
              and orig_to_hf('model.embed_tokens.weight', lay) == L['lm'] + 'embed_tokens.weight'
              and orig_to_hf('lm_head.weight', lay) == L['head']
              and orig_to_hf('model.mm_projector.2.bias', lay) == L['proj'] + 'linear_2.bias'
              and orig_to_hf('model.vision_tower.vision_tower.vision_model.post_layernorm.weight', lay) == L['vis'] + 'vision_model.post_layernorm.weight'
              and orig_to_hf('model.layers.0.self_attn.rotary_emb.inv_freq', lay) is None)
    rejected('key map rejects foreign keys', lambda: orig_to_hf('text_model.encoder.layers.0.mlp.fc1.weight', 'A'), KeyError)
    p = lora_pairs(['base_model.model.model.layers.0.mlp.up_proj.lora_A.weight',
                    'base_model.model.model.layers.0.mlp.up_proj.lora_B.default.weight'])
    check('LoRA pairs', list(p) == ['model.layers.0.mlp.up_proj'])
    rejected('LoRA rejects DoRA magnitude keys', lambda: lora_pairs(['base_model.model.model.layers.0.mlp.up_proj.lora_magnitude_vector']), KeyError)
    rejected('LoRA rejects an unpaired A', lambda: lora_pairs(['base_model.model.model.layers.0.mlp.up_proj.lora_A.weight']), KeyError)
    check('LoRA scale', lora_scale({'peft_type': 'LORA', 'r': 128, 'lora_alpha': 256, 'bias': 'none'}) == 2.0)
    rejected('LoRA rejects rsLoRA', lambda: lora_scale({'peft_type': 'LORA', 'r': 8, 'lora_alpha': 16, 'use_rslora': True}), ValueError)

    fake_out = {'schema': SCHEMA, 'label': 't', 'created_utc': 'x', 'script': {}, 'provenance': {},
                'model': {'base': {}, 'vision': {}, 'loras': [], 'drop_vision_lora': False, 'files_sha256': {}},
                'decoding': {'prompt': PROMPT, 'do_sample': False, 'max_new_tokens': 512, 'batch_size': 8, 'num_beams': 1},
                'images': {'id_list_path': 'i', 'id_list_sha256': 'h', 'n_ids': 2, 'n_decoded': 2},
                'preds': [{'image_id': i, 'image_file': 'f', 'image_sha256': 'h', 'caption': 'c', 'n_new_tokens': 3,
                           'hit_max_new_tokens': False} for i in (1, 2)]}
    check('output schema accepts a valid record', validate_output(fake_out))
    fake_out['preds'][1]['image_id'] = 1
    rejected('output schema rejects duplicate ids', lambda: validate_output(fake_out), ValueError)

    try:
        import torch, transformers  # noqa: F401
    except ImportError:
        print('\n'.join('PASS ' + n for n in ok))
        print('SKIP tensor checks and tiny end-to-end run: torch/transformers not installed')
        return 0
    ok += selftest_tiny(torch)
    print('\n'.join('PASS ' + n for n in ok))
    return 0


def selftest_tiny(torch):
    """Tiny random LLaVA: synthetic original-format checkpoints through the real loader, then batched decoding."""
    from transformers import CLIPImageProcessor, CLIPVisionConfig, LlavaForConditionalGeneration
    from PIL import Image
    torch.manual_seed(0)
    base_cfg = dict(BASE_FIELDS, hidden_size=16, intermediate_size=32, num_hidden_layers=2, num_attention_heads=2,
                    num_key_value_heads=2, max_position_embeddings=1024, rms_norm_eps=1e-5)
    vcfg = CLIPVisionConfig(hidden_size=8, intermediate_size=16, num_hidden_layers=2, num_attention_heads=2,
                            image_size=336, patch_size=14, projection_dim=8)
    cfg = build_config(base_cfg, vcfg)
    new = lambda: LlavaForConditionalGeneration._from_config(cfg, torch_dtype=torch.float32).eval()
    ref = new()
    sd = ref.state_dict()
    lay = 'A' if 'language_model.lm_head.weight' in sd else 'B'
    L = LAYOUTS[lay]
    inv = {}                                  # HF key -> original key, built by inverting orig_to_hf
    for k in sd:
        if k.startswith(L['vis']):
            continue
        if k == L['head']:
            inv[k] = 'lm_head.weight'
        elif k.startswith(L['proj']):
            idx = {'linear_1': '0', 'linear_2': '2'}[k[len(L['proj']):].split('.')[0]]
            inv[k] = f'model.mm_projector.{idx}.' + k.split('.')[-1]
        else:
            inv[k] = 'model.' + k[len(L['lm']):]
    base = {o: (sd[h][:N_VOCAB].clone() if h.endswith(('embed_tokens.weight', 'lm_head.weight')) else sd[h].clone())
            for h, o in inv.items()}
    base['model.layers.0.self_attn.rotary_emb.inv_freq'] = torch.zeros(4)
    clip = {k[len(L['vis']):]: v.clone() for k, v in sd.items() if k.startswith(L['vis'])}
    clip['text_model.embeddings.token_embedding.weight'] = torch.zeros(2, 2)
    base.update({'model.vision_tower.vision_tower.' + k: v + 0.5 for k, v in clip.items() if k.startswith('vision_model.')})
    lmod = ['model.layers.1.self_attn.q_proj', 'model.mm_projector.0',
            'model.vision_tower.vision_tower.vision_model.encoder.layers.0.self_attn.out_proj']
    adapter = {}
    for mm in lmod:
        W = sd[orig_to_hf(mm + '.weight', lay)]
        adapter[f'base_model.model.{mm}.lora_A.weight'] = torch.randn(2, W.shape[1])
        adapter[f'base_model.model.{mm}.lora_B.weight'] = torch.randn(W.shape[0], 2)
    non_lora = {'base_model.model.model.mm_projector.2.bias': torch.randn_like(sd[L['proj'] + 'linear_2.bias'])}
    want = lambda mm: sd[orig_to_hf(mm + '.weight', lay)] + 1.5 * (adapter[f'base_model.model.{mm}.lora_B.weight']
                                                                     @ adapter[f'base_model.model.{mm}.lora_A.weight'])
    out = []
    with torch.no_grad():
        m = new()
        ld = Loader(m)
        try:
            ld.load_base(base.items())
            raise AssertionError('base loaded before vision')
        except RuntimeError:
            out.append('loader refuses --base before --vision')
        ld.load_vision(clip.items())
        ld.load_base(base.items())
        ld.check_coverage()
        got = m.state_dict()
        same = all(torch.equal(got[k][:N_VOCAB], sd[k][:N_VOCAB]) if k.endswith(('embed_tokens.weight', 'lm_head.weight'))
                   else torch.equal(got[k], sd[k]) for k in sd)
        extra_zero = all(got[k][N_VOCAB:].abs().sum() == 0 for k in (L['head'], L['lm'] + 'embed_tokens.weight'))
        if not (same and extra_zero and abs(ld.log['vision_saved_in_base_max_abs_diff'] - 0.5) < 1e-6):
            raise AssertionError('base/vision load mismatch')
        out.append('loader: base + vision reproduce the reference exactly; saved vision weights ignored, diff logged')
        ld.load_non_lora(non_lora.items(), 'x')
        ld.merge_lora(adapter, 1.5, 'x')
        got = m.state_dict()
        if not all(torch.allclose(got[orig_to_hf(mm + '.weight', lay)], want(mm), atol=1e-6) for mm in lmod) or \
                not torch.equal(got[L['proj'] + 'linear_2.bias'], non_lora['base_model.model.model.mm_projector.2.bias']) or \
                ld.log['lora_merged'][0]['modules_by_component'] != {'language_model': 1, 'projector': 1, 'vision': 1}:
            raise AssertionError('LoRA / non_lora merge mismatch')
        out.append('loader: non_lora + LoRA merge (language model, projector, vision) match W + s*B@A')

        m2 = new()
        ld2 = Loader(m2)
        ld2.load_vision(clip.items())
        ld2.load_base(base.items())
        ld2.merge_lora(adapter, 1.5, 'x', drop_vision=True)
        got2 = m2.state_dict()
        vk = orig_to_hf(lmod[2] + '.weight', lay)
        if not (torch.equal(got2[vk], sd[vk]) and torch.allclose(got2[orig_to_hf(lmod[0] + '.weight', lay)], want(lmod[0]), atol=1e-6)
                and ld2.log['lora_merged'][0]['skipped_by_component'] == {'vision': 1}):
            raise AssertionError('--drop-vision-lora mismatch')
        out.append('loader: --drop-vision-lora leaves the vision tower untouched and merges the rest')

        bad = Loader(new())
        bad.load_vision(clip.items())
        bad.load_base([(k, v) for k, v in base.items() if 'layers.1.mlp' not in k])
        try:
            bad.check_coverage()
            raise AssertionError('coverage gap not detected')
        except RuntimeError:
            out.append('loader: coverage check catches a missing tensor')

    proc = CLIPImageProcessor(size={'shortest_edge': 336}, crop_size={'height': 336, 'width': 336}, resample=3)
    ids_row = image_input_ids(prompt_template_ids(fake_tok := (lambda s: [1] + [3 + (sum(map(ord, w)) % 31000) for w in s.split()]), 1),
                              (336 // 14) ** 2)
    imgs = {100 + i: Image.new('RGB', (64 + 16 * i, 48), (40 * i, 90, 200 - 30 * i)) for i in range(3)}
    items = [(i, f'{i:012d}.jpg', 'h', i) for i in imgs]
    decode = lambda t: ' '.join(map(str, t))

    def run(bs, sample=False, seed=None, done=None):
        args = argparse.Namespace(batch_size=bs, max_new_tokens=6, do_sample=sample, temperature=1.0 if sample else None,
                                  top_p=1.0 if sample else None, top_k=0 if sample else None, seed=seed)
        rows, done = [], ({} if done is None else done)
        run_decoding(m, decode, ids_row, 2, proc, items, args, done, lambda rs: (rows.extend(rs), done.update({r['image_id']: r for r in rs})),
                     lambda src: imgs[src])
        return rows

    g1, g3 = run(1), run(3)
    if [x['caption'] for x in g1] != [x['caption'] for x in g3] or len(g1) != 3:
        raise AssertionError('batched greedy differs from batch size 1')
    out.append('decoding: greedy batch 3 == batch 1 (shared prompt, no padding)')
    s1, s1b, s2 = run(2, True, 1), run(2, True, 1), run(2, True, 2)
    if [x['caption'] for x in s1] != [x['caption'] for x in s1b]:
        raise AssertionError('sampling not reproducible for a fixed seed')
    resumed = run(2, True, 1, done={s1[0]['image_id']: s1[0], s1[1]['image_id']: s1[1]})
    if [x['caption'] for x in resumed] != [x['caption'] for x in s1[2:]]:
        raise AssertionError('resume changed the remaining batch')
    out.append('decoding: sampling reproducible for a fixed seed, also after a resume' +
               ('' if [x['caption'] for x in s1] != [x['caption'] for x in s2] else ' (seeds 1 and 2 gave equal text)'))
    if any(t >= N_VOCAB for x in g1 + s1 for t in map(int, x['caption'].split() or [0])):
        raise AssertionError('suppressed vocabulary generated')
    out.append('decoding: no token id >= 32000 generated')
    return out


if __name__ == '__main__':
    a = parse_args(sys.argv[1:])
    sys.exit(selftest() if a.selftest else main(a))
