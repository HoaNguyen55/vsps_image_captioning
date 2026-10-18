#!/usr/bin/env python
"""M3 CM-DPO with the SFT anchor (--anchor-sft) or the A-KL token KL (--token-kl), on train_stage2.run_dpo unchanged.

    python scripts/train_stage2_anchor.py --prereg-arm A --stage dpo --data DIR --adapter RUN --out OUT --epochs 1 \\
        --beta 0.1 --lr 5e-6 --grad-accum 8 --anchor-sft 1.0 --seed 42 [--dry-run]
    python scripts/train_stage2_anchor.py --prereg-arm AKL ... --lr 2.5e-6 --token-kl 0.4 [--dry-run]
    python scripts/train_stage2_anchor.py --selftest     # CPU (torch, datasets): a toy model through the real run_dpo

Why a wrapper (decision D-W13-4; S3 instrument addendum): train_stage2.py is registered byte for byte by the S1 and S5
preregs, so it is imported and never edited; every train_stage2 argument passes through to its own parser. run_dpo
looks up build_model, to_chat and sequence_logprob in its module when it runs, and this file wraps them for that call:
  - to_chat(processor, row, "chosen") records the pair's row;
  - the policy's chosen pass (the first sequence_logprob call with gradients on after that) first back-propagates
    coef x term / grad_accum. Gradients add, so this is run_dpo's loss plus coef x term.
    --anchor-sft (M3 §4): term = model(**VLCollator(processor, assistant_only=True)([to_chat(processor, row,
      "ref")])).loss, the response-only CE on the image's first human caption. No NLL on the chosen caption.
    --token-kl (A-KL, R14-2 P-1): term = the sum over the chosen response's tokens of KL(pi_SFT || pi_theta) over the
      vocabulary, pi_SFT = the frozen ref_sft adapter (HALVA's L_d in llava/train/halva_trainer.py: summed over tokens
      and vocabulary, divided by the batch size).
  - the DPO reference must be pi_SFT (the ref_sft adapter loaded): a base-anchored run is refused.
Checkpoints: run_dpo has none and the committed hook patches only the HF Trainer. So every RESCAP_SAVE_STEPS (200)
optimizer steps this file writes OUT/checkpoint-<step>: the trainable weights, the AdamW state, the RNG states and the
per-pair log. It mirrors each one to RESCAP_MIRROR_ROOT/<OUT name> (/root/outputs/runs) and keeps RESCAP_SAVE_LIMIT
(2), as the hook does for SFT. A rerun with the same arguments resumes from the newest checkpoint: weights and AdamW
state are restored, and the first step x grad_accum pairs of the same seeded shuffle are skipped.
OUT/resume_manifest.json lists resumed_from_step in the hook's format. Outputs: run_dpo's adapter and metrics.jsonl,
plus OUT/pairs_log.jsonl (per pair: image, type, term, margin) and OUT/train_summary.json (ordering accuracy over
every pair, the regulariser, peak reserved memory, the gradient check, provenance).
"""
from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import sys
import tempfile
import zlib
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent), str(HERE)]

import checkpoint_resume_hook as hook  # noqa: E402  (imported for its helpers; it installs nothing for this argv)
import train_stage2 as T  # noqa: E402
from s3_gate import AKL, DPO, DRY_GB, DRY_PAIRS, _raises, _sha, _write_once  # noqa: E402

RUN_KEYS = ("data", "adapter", "base_model", "beta", "lr", "grad_accum", "epochs", "seed", "anchor_sft", "token_kl",
            "limit", "pair_types", "vision_tokens", "force_4bit", "no_4bit", "use_8bit")


def token_kl(model, batch):
    """HALVA's L_d on one batch: KL(pi_SFT || pi_theta) over the vocabulary, summed over the response tokens."""
    import torch

    inputs = {k: v for k, v in batch.items() if k != "labels"}
    mask = batch["labels"][:, 1:] != -100
    with torch.no_grad():
        model.set_adapter("ref_sft")
        ref = model(**inputs).logits[:, :-1][mask].float().log_softmax(-1)
        model.set_adapter("default")
    pol = model(**inputs).logits[:, :-1][mask].float().log_softmax(-1)
    return (ref.exp() * (ref - pol)).sum() / batch["labels"].shape[0]


def _grad_stats(params) -> dict:
    with_grad = [p for p in params if p.grad is not None]
    norm = math.sqrt(sum(float(p.grad.float().pow(2).sum()) for p in with_grad))
    return {"params": len(params), "with_grad": len(with_grad), "grad_norm": norm, "pass": bool(with_grad) and norm > 0}


def latest_checkpoint(out: Path, mirror: Path) -> Path | None:
    """The newest complete checkpoint-<step> in OUT, else in its mirror (the hook's resume order)."""
    for d in (out, mirror):
        done = [p for p in hook._sorted_checkpoints(d) if (p / "state.json").is_file()]
        if done:
            return done[-1]
    return None


class Run:
    """The state the wrappers share during one train_stage2.run_dpo call."""

    def __init__(self, args, dry: bool = False):
        self.args, self.out, self.dry = args, Path(args.out), dry
        self.mirror = Path(os.environ.get("RESCAP_MIRROR_ROOT", "/root/outputs/runs")) / self.out.name
        self.save_steps = int(os.environ.get("RESCAP_SAVE_STEPS", "200"))
        self.save_limit = int(os.environ.get("RESCAP_SAVE_LIMIT", "2"))
        self.coef = args.anchor_sft or args.token_kl
        self.key = {"args": {k: getattr(args, k) for k in RUN_KEYS}, "data_sha256": _sha(Path(args.data) / "dpo.jsonl")}
        self.model = self.processor = self.collate = self.row = self.orig_to_chat = None
        self.records: list[dict] = []
        self.calls: list = []
        self.step, self.resumed, self.grad_check, self.skipping = 0, [], {}, False
        self.ckpt = latest_checkpoint(self.out, self.mirror)

    def trainable(self) -> dict:
        return {n: p for n, p in self.model.named_parameters() if p.requires_grad}

    def build_model(self, orig):
        def wrapped(args, **kw):
            model, processor = orig(args, **kw)
            if not getattr(args, "_has_ref_adapter", False):
                raise SystemExit("the DPO reference must be pi_SFT (the ref_sft adapter): refusing a base-anchored run")
            self.model = model
            return model, processor
        return wrapped

    def to_chat(self, processor, row, response_key):
        if response_key == "chosen" and not self.skipping:
            if self.row is not None:
                raise SystemExit("a pair was collated before the previous pair's policy pass: the anchor would drift")
            self.row, self.processor = row, processor
        return self.orig_to_chat(processor, row, response_key)

    def sequence_logprob(self, orig):
        def wrapped(model, batch, labels):
            import torch

            if torch.is_grad_enabled() and self.row is not None:  # the policy's chosen pass of a new pair
                self.regularise(model)
            out = orig(model, batch, labels)
            self.calls.append(out.detach())
            if len(self.calls) == 4:  # policy chosen, policy rejected, reference chosen, reference rejected
                pc, pr, rc, rr = self.calls
                self.records[-1]["margin"] = float(((pc - rc) - (pr - rr)).mean())  # run_dpo's own float32 arithmetic
                self.calls = []
            return out
        return wrapped

    def regularise(self, model) -> None:
        import torch

        row, self.row = self.row, None
        if self.collate is None:
            self.collate = T.VLCollator(self.processor, assistant_only=True)
        key = "ref" if self.args.anchor_sft else "chosen"
        device = next(model.parameters()).device
        batch = {k: v.to(device) for k, v in self.collate([self.orig_to_chat(self.processor, row, key)]).items()}
        term = model(**batch).loss if self.args.anchor_sft else token_kl(model, batch)
        if not torch.isfinite(term):
            raise SystemExit(f"non-finite regulariser {term.item()} on image {row.get('image_id')}: stopping before "
                             "it reaches the weights")
        (self.coef * term / self.args.grad_accum).backward()
        if not self.grad_check:
            self.grad_check["after_first_regulariser"] = _grad_stats(list(self.trainable().values()))
        self.records.append({"image_id": row.get("image_id"), "pair_type": row.get("pair_type", "?"),
                             "term": term.item()})

    def attach(self, opt, params) -> None:
        """Called once run_dpo has built its AdamW: check what it optimises, and resume from a checkpoint."""
        import torch

        named = self.trainable()
        if [id(p) for p in params] != [id(p) for p in named.values()]:
            raise SystemExit("the optimizer does not hold exactly the trainable (default adapter) weights")
        if self.ckpt is not None:
            state = json.loads((self.ckpt / "state.json").read_text(encoding="utf-8"))
            if state["key"] != self.key:
                raise SystemExit(f"{self.ckpt} belongs to another run (data, adapter or settings differ)")
            weights = torch.load(self.ckpt / "trainable.pt", map_location="cpu", weights_only=True)
            if weights.keys() != named.keys():
                raise SystemExit(f"{self.ckpt}: its weights are not this model's trainable parameters")
            with torch.no_grad():
                for n, p in named.items():
                    p.copy_(weights[n])
            opt.load_state_dict(torch.load(self.ckpt / "optimizer.pt", map_location="cpu", weights_only=True))
            rng = torch.load(self.ckpt / "rng.pt", weights_only=True)
            torch.set_rng_state(rng["cpu"])
            if rng["cuda"]:
                torch.cuda.set_rng_state_all(rng["cuda"])
            self.step, self.records = state["step"], state["records"]
            self.resumed = state["resumed_from_step"] + [self.step]
            print(f"  resumed from {self.ckpt}: step {self.step}, {len(self.records)} pairs done", flush=True)
        self.manifest()

    def manifest(self) -> None:
        meta = dict(hook.provenance_metadata(None), resumed_from_step=self.resumed, output_dir=str(self.out),
                    save_steps=self.save_steps, save_total_limit=self.save_limit,
                    train_stage2_anchor_sha256=_sha(Path(__file__)))
        (self.out / "resume_manifest.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                                                       encoding="utf-8")

    def on_step(self, opt) -> None:
        self.step += 1
        if self.step % self.save_steps == 0:
            self.save(opt)

    def save(self, opt) -> None:
        import torch

        name = f"checkpoint-{self.step}"
        tmp = self.out / f".{name}.tmp"
        if tmp.exists():
            shutil.rmtree(tmp)
        tmp.mkdir(parents=True)
        torch.save({n: p.detach().cpu() for n, p in self.trainable().items()}, tmp / "trainable.pt")
        torch.save(opt.state_dict(), tmp / "optimizer.pt")
        torch.save({"cpu": torch.get_rng_state(),
                    "cuda": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else []}, tmp / "rng.pt")
        (tmp / "state.json").write_text(json.dumps({"step": self.step, "key": self.key, "records": self.records,
                                                    "resumed_from_step": self.resumed}), encoding="utf-8")
        tmp.rename(self.out / name)  # complete or absent: a crash mid-save leaves only the .tmp
        self.mirror.mkdir(parents=True, exist_ok=True)
        if (self.mirror / name).exists():
            shutil.rmtree(self.mirror / name)
        shutil.copytree(self.out / name, self.mirror / name)
        shutil.copy2(self.out / "resume_manifest.json", self.mirror / "resume_manifest.json")
        for d in (self.out, self.mirror):
            for old in hook._sorted_checkpoints(d)[:-self.save_limit]:
                shutil.rmtree(old)
        print(f"  {name} saved and mirrored to {self.mirror}", flush=True)

    @contextmanager
    def installed(self):
        """train_stage2's three helpers and torch's AdamW / DataLoader, wrapped for the duration of run_dpo."""
        import torch

        run = self

        class AdamW(torch.optim.AdamW):
            def __init__(self, params, **kw):
                params = list(params)
                super().__init__(params, **kw)
                run.attach(self, params)

            def step(self, closure=None):
                run.grad_check.setdefault("at_first_step", _grad_stats(self.param_groups[0]["params"]))
                loss = super().step(closure)
                run.on_step(self)
                return loss

        class DataLoader(torch.utils.data.DataLoader):
            def __iter__(self):  # resume: the same seeded shuffle, minus the pairs the checkpoint trained on
                it = super().__iter__()
                run.skipping = True
                for _ in range(run.step * run.args.grad_accum):
                    next(it)
                run.skipping = False
                yield from it

        saved = (T.build_model, T.to_chat, T.sequence_logprob, torch.optim.AdamW, torch.utils.data.DataLoader)
        self.orig_to_chat = T.to_chat
        T.build_model, T.to_chat, T.sequence_logprob = (self.build_model(T.build_model), self.to_chat,
                                                        self.sequence_logprob(T.sequence_logprob))
        torch.optim.AdamW, torch.utils.data.DataLoader = AdamW, DataLoader
        try:
            yield
        finally:
            T.build_model, T.to_chat, T.sequence_logprob, torch.optim.AdamW, torch.utils.data.DataLoader = saved

    def finish(self) -> dict:
        import torch

        per_type: dict[str, list[int]] = {}
        for r in self.records:
            t = per_type.setdefault(r["pair_type"].split(":")[0], [0, 0])
            t[0], t[1] = t[0] + 1, t[1] + (r["margin"] > 0)
        terms = [r["term"] for r in self.records]
        summary = {
            "regulariser": "anchor_sft" if self.args.anchor_sft else "token_kl", "coef": self.coef,
            "pairs": len(self.records), "optimizer_steps": self.step, "term_first": terms[0],
            "term_mean": sum(terms) / len(terms),
            "ordering_accuracy": sum(r["margin"] > 0 for r in self.records) / len(self.records),
            "ordering_accuracy_per_pair_type": {k: c / n for k, (n, c) in sorted(per_type.items())},
            "peak_reserved_gb": torch.cuda.max_memory_reserved() / 1e9 if torch.cuda.is_available() else None,
            "gradient_check": self.grad_check, "resumed_from_step": self.resumed, "run_key": self.key,
            "reference_policy": "pi_sft (the ref_sft adapter)",
            "provenance": dict(hook.provenance_metadata(None), resumed_from_step=self.resumed,
                               train_stage2_anchor_sha256=_sha(Path(__file__)))}
        if self.dry:  # the registered dry run: gradients flow and the reserved peak stays within the card's budget
            summary["dry_run"] = {"pairs": DRY_PAIRS, "peak_reserved_gb_max": DRY_GB, "pass": bool(
                len(self.records) == DRY_PAIRS and self.grad_check and all(g["pass"] for g in self.grad_check.values())
                and summary["peak_reserved_gb"] is not None and summary["peak_reserved_gb"] <= DRY_GB)}
        _write_once(self.out / "pairs_log.jsonl", "".join(json.dumps(r) + "\n" for r in self.records))
        _write_once(self.out / "train_summary.json", json.dumps(summary, ensure_ascii=False, indent=1) + "\n")
        return summary


def _registered(args, arm: str, dry: bool) -> None:
    """--prereg-arm: the arm's registered settings, and the S3 registration check (code, constants, inputs)."""
    import s3_gate

    want = DPO if arm == "A" else AKL
    got = {k: getattr(args, k) for k in want}
    if got != want or args.pair_types or (args.limit and not dry):
        raise SystemExit(f"--prereg-arm {arm}: {got} (limit {args.limit}, pair types {args.pair_types!r}) is not the "
                         f"registered {want}")
    s3_gate.check()


def train(args, ours, run_dpo) -> int:
    if bool(args.anchor_sft) == bool(args.token_kl):
        raise SystemExit("exactly one of --anchor-sft and --token-kl")
    if args.epochs != 1:
        raise SystemExit("this wrapper resumes mid-epoch, so it runs the registered 1-epoch DPO only")
    if ours.dry_run:
        if args.limit not in (0, DRY_PAIRS):
            raise SystemExit(f"--dry-run is the registered {DRY_PAIRS}-pair run")
        args.limit = DRY_PAIRS
    if ours.prereg_arm:
        _registered(args, ours.prereg_arm, ours.dry_run)
    if (Path(args.out) / "train_summary.json").exists():
        raise SystemExit(f"{args.out} holds a finished run: refusing to overwrite it (write a _v2)")
    run = Run(args, ours.dry_run)
    with run.installed():
        rc = run_dpo(args)
    summary = run.finish()
    if "dry_run" not in summary:
        return rc
    print(f"  dry run: {summary['dry_run']} - gradient check {summary['gradient_check']}, peak reserved "
          f"{summary['peak_reserved_gb']} GB, ordering accuracy {summary['ordering_accuracy']:.3f}", flush=True)
    return 0 if summary["dry_run"]["pass"] else 1


def _refuse_sft(args) -> int:
    raise SystemExit("train_stage2_anchor.py runs DPO only: train SFT with scripts/train_stage2.py")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, allow_abbrev=False,
                                 epilog="Every other argument goes to train_stage2.py's own parser.")
    ap.add_argument("--anchor-sft", type=float, default=0.0, help="ALPHA x the response-only CE on row['ref']")
    ap.add_argument("--token-kl", type=float, default=0.0, help="ALPHA x the token KL to pi_SFT on the chosen response")
    ap.add_argument("--prereg-arm", choices=("A", "AKL"), help="assert the arm's registered settings and the S3 check")
    ap.add_argument("--dry-run", action="store_true", help=f"the registered {DRY_PAIRS}-pair dry run; exit 1 unless "
                                                            f"gradients flow and peak reserved <= {DRY_GB} GB")
    ap.add_argument("--selftest", action="store_true")
    ours, rest = ap.parse_known_args(argv)
    if ours.selftest:
        selftest()
        return 0
    orig_dpo, orig_sft, orig_argv = T.run_dpo, T.run_sft, sys.argv

    def run_dpo(args) -> int:
        args.anchor_sft, args.token_kl = ours.anchor_sft, ours.token_kl
        return train(args, ours, orig_dpo)

    T.run_dpo, T.run_sft, sys.argv = run_dpo, _refuse_sft, [orig_argv[0], *rest]
    try:
        return T.main()
    finally:
        T.run_dpo, T.run_sft, sys.argv = orig_dpo, orig_sft, orig_argv


# ---------------------------------------------------------------- selftest: a toy model through the real run_dpo
class _Tok:
    """Whitespace tokenizer, id = a fixed function of the word ("<|im_start|>assistant" is one token, as the header
    must be); 0 is padding and 2 the image placeholder."""

    pad_token_id, eos_token_id, size = 0, 1, 97

    def word(self, w: str) -> int:
        return 2 if w == "<img>" else 3 + zlib.crc32(w.encode()) % (self.size - 3)

    def ids(self, text: str) -> list[int]:
        return [self.word(w) for w in text.split()]

    def __call__(self, text: str, add_special_tokens: bool = False) -> dict:
        return {"input_ids": self.ids(text)}

    def convert_tokens_to_ids(self, token: str) -> int:
        return self.word(token)


class _Proc:
    """Chat template and batching like Qwen2.5-VL's processor: the image placeholder expands only in __call__, so
    the legacy mask (prompt measured before the expansion) leaves prompt tokens in the loss and assistant_only not."""

    image_token, n_image_tokens = "<img>", 3

    def __init__(self):
        self.tokenizer = _Tok()

    def apply_chat_template(self, messages, tokenize=False, add_generation_prompt=False) -> str:
        text = f"<|im_start|>user <img> {messages[0]['content'][1]['text']} <|im_end|> <|im_start|>assistant\n"
        return text + (f"{messages[1]['content'][0]['text']} <|im_end|>" if len(messages) > 1 else "")

    def __call__(self, text, images, return_tensors="pt", padding=True) -> dict:
        import torch

        seqs = [[i for w in s.split() for i in ([2] * self.n_image_tokens if w == "<img>" else [self.tokenizer.word(w)])]
                for s in text]
        n = max(map(len, seqs))
        ids = torch.tensor([s + [0] * (n - len(s)) for s in seqs])
        return {"input_ids": ids, "attention_mask": (ids != 0).long()}

    def save_pretrained(self, d) -> None:
        (Path(d) / "toy_processor.txt").write_text("toy", encoding="utf-8")


def _toy_model(vocab: int = _Tok.size, dim: int = 6):
    """Causal toy LM, logits(t) = head(mean embedding of tokens <= t), heads "default" (trainable) and "ref_sft"."""
    import torch

    class Toy(torch.nn.Module):
        def __init__(self):
            super().__init__()
            g = torch.Generator().manual_seed(0)
            self.emb = torch.nn.Embedding(vocab, dim)
            self.heads = torch.nn.ModuleDict({"default": torch.nn.Linear(dim, vocab), "ref_sft": torch.nn.Linear(dim, vocab)})
            with torch.no_grad():
                self.emb.weight.copy_(torch.randn(vocab, dim, generator=g))
                for p, q in zip(self.heads["ref_sft"].parameters(), self.heads["default"].parameters()):
                    p.copy_(torch.randn(p.shape, generator=g))
                    q.copy_(p + 0.3 * torch.randn(p.shape, generator=g))  # policy != reference: KL and margins move
            self.emb.weight.requires_grad_(False)
            self.heads["ref_sft"].requires_grad_(False)
            self.active = "default"

        def set_adapter(self, name: str) -> None:
            self.active = name

        def forward(self, input_ids, attention_mask=None, labels=None, **_):
            h = self.emb(input_ids).cumsum(1) / torch.arange(1, input_ids.shape[1] + 1)[None, :, None]
            logits = self.heads[self.active](h)
            loss = None if labels is None else torch.nn.functional.cross_entropy(
                logits[:, :-1].reshape(-1, vocab), labels[:, 1:].reshape(-1), ignore_index=-100)
            return SimpleNamespace(logits=logits, loss=loss)

        def save_pretrained(self, d) -> None:
            torch.save(self.heads["default"].state_dict(), Path(d) / "toy_adapter.pt")

    return Toy()


def _toy_build(args, for_training: bool = True):
    args._has_ref_adapter = True
    return _toy_model(), _Proc()


def _pairs(n: int) -> list[dict]:
    words = ["chó", "mèo", "xe", "bàn", "ghế", "sông", "thuyền", "đường"]
    return [{"image_id": str(i), "file_name": f"{i}.jpg", "prompt": "mô tả ảnh", "pair_type": f"cm_k{1 + i % 2}",
             "chosen": f"một {words[i % 8]} đang ở {words[(i + 1) % 8]}", "rejected": f"một {words[(i + 3) % 8]} ở đó",
             "ref": f"hai {words[(i + 5) % 8]} và {words[(i + 2) % 8]}"} for i in range(n)]


def _hand(model, proc, row: dict, key: str, assistant_only: bool, head: str):
    """Per-position log-probs of one row's chat and the positions in the loss, by the masking rule itself."""
    import torch

    msgs = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": row["prompt"]}]},
            {"role": "assistant", "content": [{"type": "text", "text": row[key]}]}]
    ids = proc(text=[proc.apply_chat_template(msgs)], images=[None])["input_ids"][0].tolist()
    header = proc.tokenizer.word("<|im_start|>assistant")
    start = (len(ids) - ids[::-1].index(header) if assistant_only
             else len(proc.tokenizer(proc.apply_chat_template(msgs[:1], add_generation_prompt=True))["input_ids"]))
    pos = [t for t in range(start, len(ids)) if ids[t] != 2]
    model.set_adapter(head)
    logp = torch.log_softmax(model(input_ids=torch.tensor([ids])).logits[0].float(), -1)
    model.set_adapter("default")
    return logp, ids, pos


def _expected(rows: list[dict], kind: str, beta: float, alpha: float, ga: int) -> tuple[list, dict]:
    """Hand-derived gradients of sum over pairs of [-logsigmoid(beta * margin) + alpha * term] / ga, and each term."""
    import torch

    model, proc = _toy_model(), _Proc()
    total, terms = 0.0, {}
    for r in rows:
        seq = {}
        for key in ("chosen", "rejected"):
            for head in ("default", "ref_sft"):
                lp, ids, pos = _hand(model, proc, r, key, False, head)
                seq[key, head] = sum(lp[t - 1, ids[t]] for t in pos)
        margin = (seq["chosen", "default"] - seq["chosen", "ref_sft"].detach()) - (
            seq["rejected", "default"] - seq["rejected", "ref_sft"].detach())
        if kind == "anchor":
            lp, ids, pos = _hand(model, proc, r, "ref", True, "default")
            term = -sum(lp[t - 1, ids[t]] for t in pos) / len(pos)
        else:
            pol, ids, pos = _hand(model, proc, r, "chosen", True, "default")
            ref = _hand(model, proc, r, "chosen", True, "ref_sft")[0].detach()
            term = sum((ref[t - 1].exp() * (ref[t - 1] - pol[t - 1])).sum() for t in pos)
        terms[r["image_id"]] = (float(term), float(margin))
        total = total + (-torch.nn.functional.logsigmoid(beta * margin) + alpha * term) / ga
    total.backward()
    return [p.grad.clone() for p in model.heads["default"].parameters()], terms


def _run(tmp: Path, name: str, rows: list[dict], extra: list[str], ga: int) -> Path:
    data = tmp / f"data_{name}"
    if not data.exists():
        data.mkdir()
        (data / "dpo.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    out = tmp / name
    main(["--stage", "dpo", "--data", str(data), "--adapter", "toy", "--out", str(out), "--epochs", "1", "--beta", "0.1",
          "--lr", "0.05", "--grad-accum", str(ga), "--seed", "42", *extra])
    return out


def selftest() -> None:
    """Anchor CE and token KL against hand-derived values and gradients, through the real run_dpo; resume equivalence."""
    import torch

    saved = (T.build_model, T.image_for, torch.nn.utils.clip_grad_norm_, os.environ.get("RESCAP_MIRROR_ROOT"),
             os.environ.get("RESCAP_SAVE_STEPS"))
    captured: list = []

    def clip(params, max_norm, *a, **k):
        params = list(params)
        captured.append([p.grad.detach().clone() for p in params])
        return saved[2](params, max_norm, *a, **k)

    T.build_model, T.image_for, torch.nn.utils.clip_grad_norm_ = _toy_build, (lambda row: None), clip
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            os.environ["RESCAP_MIRROR_ROOT"] = str(tmp / "mirror")
            rows = _pairs(4)
            for kind, flag, alpha in (("anchor", "--anchor-sft", 1.0), ("kl", "--token-kl", 0.4)):
                captured.clear()
                out = _run(tmp, kind, rows, [flag, str(alpha)], ga=4)  # one optimizer step over the 4 pairs
                want, terms = _expected(rows, kind, 0.1, alpha, 4)
                assert all(torch.allclose(g, w, atol=1e-6, rtol=1e-5) for g, w in zip(captured[0], want)), kind
                log = [json.loads(x) for x in (out / "pairs_log.jsonl").read_text(encoding="utf-8").splitlines()]
                for r in log:
                    t, m = terms[r["image_id"]]
                    assert abs(r["term"] - t) < 1e-5 and abs(r["margin"] - m) < 1e-4, (kind, r, t, m)
                summary = json.loads((out / "train_summary.json").read_text(encoding="utf-8"))
                own = [json.loads(x) for x in (out / "metrics.jsonl").read_text(encoding="utf-8").splitlines()][-1]
                for k, v in own["summary_per_pair_type"].items():  # run_dpo's own count agrees with the log's
                    assert abs(summary["ordering_accuracy_per_pair_type"][k] - v["ordering_accuracy"]) < 1e-12
                assert summary["pairs"] == 4 and summary["optimizer_steps"] == 1 and own["reference_policy"] == "pi_sft"
                assert all(g["pass"] for g in summary["gradient_check"].values())
            _selftest_resume(tmp)
            _selftest_dry(tmp)
            _selftest_refusals(tmp, rows)
    finally:
        T.build_model, T.image_for, torch.nn.utils.clip_grad_norm_ = saved[:3]
        for k, v in (("RESCAP_MIRROR_ROOT", saved[3]), ("RESCAP_SAVE_STEPS", saved[4])):
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    print("train_stage2_anchor selftest ok: anchor CE and token KL (values and gradients) through run_dpo, resume, "
          "dry run, refusals")


def _selftest_resume(tmp: Path) -> None:
    """A run stopped after its step-2 checkpoint and rerun ends with the uninterrupted run's weights and log."""
    import torch

    os.environ["RESCAP_SAVE_STEPS"] = "1"
    rows = _pairs(8)
    full = _run(tmp, "full", rows, ["--anchor-sft", "1.0"], ga=2)
    orig, calls = T.sequence_logprob, [0]

    def crash(model, batch, labels):
        calls[0] += 1
        if calls[0] > 16:  # pair 5's first pass: after the step-2 checkpoint
            raise RuntimeError("simulated machine loss")
        return orig(model, batch, labels)

    T.sequence_logprob = crash
    try:
        assert _raises(lambda: _run(tmp, "cut", rows, ["--anchor-sft", "1.0"], ga=2), RuntimeError), "no crash"
    finally:
        T.sequence_logprob = orig
    cut = _run(tmp, "cut", rows, ["--anchor-sft", "1.0"], ga=2)
    a, b = (torch.load(d / "toy_adapter.pt", weights_only=True) for d in (full, cut))
    assert all(torch.equal(a[k], b[k]) for k in a), "resumed weights differ from the uninterrupted run"
    assert (full / "pairs_log.jsonl").read_text(encoding="utf-8") == (cut / "pairs_log.jsonl").read_text(encoding="utf-8")
    assert json.loads((cut / "resume_manifest.json").read_text(encoding="utf-8"))["resumed_from_step"] == [2]
    for d in (cut, tmp / "mirror" / "cut"):
        assert [p.name for p in hook._sorted_checkpoints(d)] == ["checkpoint-3", "checkpoint-4"], d
    os.environ["RESCAP_SAVE_STEPS"] = "200"


def _selftest_dry(tmp: Path) -> None:
    """--dry-run trains the registered 20 pairs; its recorded pass and exit code follow the rule on any card."""
    data = tmp / "data_dry"
    data.mkdir()
    (data / "dpo.jsonl").write_text("".join(json.dumps(r) + "\n" for r in _pairs(24)), encoding="utf-8")
    rc = main(["--stage", "dpo", "--data", str(data), "--adapter", "toy", "--out", str(tmp / "dry"), "--epochs", "1",
               "--lr", "0.05", "--grad-accum", "8", "--anchor-sft", "1.0", "--dry-run"])
    s = json.loads((tmp / "dry" / "train_summary.json").read_text(encoding="utf-8"))
    peak_ok = s["peak_reserved_gb"] is not None and s["peak_reserved_gb"] <= DRY_GB  # None without a GPU
    assert s["pairs"] == DRY_PAIRS and s["optimizer_steps"] == 2 and s["dry_run"]["pass"] == peak_ok
    assert rc == (0 if peak_ok else 1)


def _selftest_refusals(tmp: Path, rows: list[dict]) -> None:
    """A finished run, two regularisers, a base-anchored reference and SFT are all refused."""
    def refused(name: str, extra: list[str]) -> bool:
        return _raises(lambda: _run(tmp, name, rows, extra, ga=4), SystemExit)

    assert refused("anchor", ["--anchor-sft", "1.0"])  # finished: never overwritten
    assert refused("both", ["--anchor-sft", "1.0", "--token-kl", "0.4"])

    def no_ref(args, for_training=True):
        model, proc = _toy_build(args)
        args._has_ref_adapter = False
        return model, proc

    T.build_model = no_ref
    try:
        assert refused("noref", ["--anchor-sft", "1.0"])
    finally:
        T.build_model = _toy_build
    assert _raises(lambda: main(["--stage", "sft", "--data", str(tmp), "--out", str(tmp / "sft")]), SystemExit)


if __name__ == "__main__":
    sys.exit(main())
