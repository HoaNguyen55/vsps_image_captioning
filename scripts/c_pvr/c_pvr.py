#!/usr/bin/env python3
"""C-PVR-T1 tier-1 core (Paper C, PVR). Prereg manuscript/prereg/2026-11-02_c_pvr_tier1/PREREG_DRAFT_v1_2.md
(8282874), amendment CC-222 v1.3, design rulings CC-234; pinned by PINS-A. G-A / G-C2 live in gates.py.

Interpreter: the C venv of requirements_c_pvr.lock (spaCy, rapidfuzz); python -I always.

    python -I -B scripts/c_pvr/c_pvr.py selftest [--root R]     CPU, synthetic fixtures, sockets raise, no weights/data
    python -I scripts/c_pvr/c_pvr.py header                   the pinned decode header (generation dicts, prompts, cap)
    python -I scripts/c_pvr/c_pvr.py en-map [--write]         build en_oiv7_map.json from vi_oiv7_map.json (N13)
    python -I scripts/c_pvr/c_pvr.py decompose --lang vi|en   JSON list of captions on stdin -> decompositions
    python -I scripts/c_pvr/c_pvr.py ovqa-pin fetch           NB-OVQA: 3 json at the pinned revision, sealed custody
    python -I scripts/c_pvr/c_pvr.py ovqa-pin skeleton        key names, types and container lengths only
    python -I scripts/c_pvr/c_pvr.py ovqa-pin count --rule F --rule-sha H [--dev-zip Z]   lengths-only identity check

Label on every output: TIER 1 / DEV-EXPLORE (C-PVR-T1). Model code (mBLIP) runs only on the GPU host through
c_pvr_job.sh; LLaVA decode is refused until its code commit is pinned. No question or answer string of OpenViVQA is
read, printed or stored here.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import random
import re
import socket
import subprocess
import sys
import tempfile
import time
import unicodedata
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LABEL = "TIER 1 / DEV-EXPLORE (C-PVR-T1)"
SEALED = Path.home() / ".vsps_sealed" / "c_pvr"  # WSL ext4 home; never /mnt/d, data/, the repo or a backup path
VNC_DIR = Path(os.environ.get("VNCORENLP_DIR", Path.home() / "c_pvr_tools" / "vncorenlp"))
OI_TEST_URL = "https://open-images-dataset.s3.amazonaws.com/test/{file}"  # B3: byte-equal to gates.py l.66

# ---------------------------------------------------------------------------------------------- pins (PINS-A)
PROMPT_SHAS = {  # PINS-A §2.1/§2.2 (VI, verifier) and W4 (EN = lmms-eval nocaps default prompt)
    "cap_vi_0.txt": "f6e05b0b7510a1bf5c8a00b203a81f077f28bd5b59a5fc25d5afeead9e618feb",
    "cap_vi_k.txt": "2653672de35c932dc2b3a088053dd7965a679eabb12f4cf4a363a89d31f9c42d",
    "demo_line.txt": "c068abccda584d10e3cf1e56b053fe6d107487b9276b9153608b57c4994af128",
    "cap_en_0.txt": "494392f0754c0f3adc0e644463073c8730ea4f39ed6ac640634195c3b76e84c2",
    "cap_en_k.txt": "7c4b0dfba310bafc1e21bfeab78856ead7e2d3591c2b2d674c4a6a1f8c2f1a7c",
    "ver_3way.txt": "bcb9230851622e5d9afa98f0765bf2bffd05b4b4ba37aa8bd0508d300881313d",
}
REPO_PINS = {  # prereg §2.3 (registered) and this file's own data files
    "vi_map": ("data/xm3600/vi_oiv7_map.json", "27f2b1ca3f2bf47d43c8f00e8409472c8d571eb720d47b8107a1c77bd208d16a"),
    "chair": ("rescap/chair.py", "e47d249ac7290070f2387d3fa8b22dac77728265ad276f55aa6520f5cbc591a3"),
    "lexicon": ("rescap/vi/lexicon.py", "fbc945f2247418275144ac75b893f7c51f8951b9ea42018680d433775dd79eb9"),
    "proxy_regex": ("scripts/c_pvr/proxy_regex.txt",
                    "c7839aa46bb8eadcfef593ca36ef65cebce92cb39ca55d6807648278fee8e222"),
}
EN_MAP = "scripts/c_pvr/en_oiv7_map.json"  # rebuilt byte-equal by the selftest; sha in PINS-A
VNC_PINS = {  # VnCoreNLP github 62bbc58f; jar = B protocol pin (b2.py l.1084), rdr = B n2 gate record
    "VnCoreNLP-1.2.jar": "9e2811cdbc2ddfc71d04be5dc36e185c88dcd1ad4d5d69e4ff2e1369dccf7793",
    "models/wordsegmenter/wordsegmenter.rdr": "9e62f96bd93e37a24f364238e8d8ae986fa5dad6dbc9f4eae622ab3651b7fa06",
    "models/wordsegmenter/vi-vocab": "0a47c5b55bbce163029d37730a67b9479740388695c29c106c112b815613eaa5",
}
JAVA = ["java", "-Xmx700m", "-XX:+UseSerialGC", "-XX:ActiveProcessorCount=1", "-jar", "VnCoreNLP-1.2.jar",
        "-fin", "/dev/stdin", "-fout", "/dev/stdout", "-annotators", "wseg"]
LIB_VERSIONS = {"spacy": "3.8.18", "en_core_web_sm": "3.8.0", "rapidfuzz": "3.14.6"}
MBLIP = {"repo": "Gregor/mblip-bloomz-7b", "revision": "4d95b91d56fcdce86504c951a28f016b15e219a1", "files": {
    "model-00001-of-00002.safetensors": "44be39143faaddf0b43e45f61f1d15a2804f0397e542e3c87b922a11b91a4c16",
    "model-00002-of-00002.safetensors": "19dcdb305a64144c84cb9f924cf760e4577f7c4233d37048e63f89df5f9e95d6",
    "tokenizer.json": "17a208233d2ee8d8c83b23bc214df737c44806a1919f444e89b31e586cd956ba",
    "config.json": "39cac8ff4edd7c57f6514e105fede0d42d939ac7b40bf795a91646d23bc7b7a9"}}
LLAVA = {"repo": "liuhaotian/llava-v1.5-7b", "revision": "4481d270cc22fd5c4d1bb5df129622006ccd9234",
         "conv": "A chat between a curious human and an artificial intelligence assistant. The assistant gives "
                 "helpful, detailed, and polite answers to the human's questions. USER: <image>\n{prompt} ASSISTANT:"}

# ---------------------------------------------------------------------------------------------- design (CC-234)
K = 4  # prereg §5.1
A3_TOP = 7  # A3: sample k in top-7
CAP = 32  # J-C: verifier calls per image, one value for PVR, A8, S1, S2
SEEDS = {"A2": 20262002, "A3": 20262003, "A7": 20262007}  # [proposal]; outside the bootstrap streams below
BOOT_SEEDS = range(20261102, 20261604)  # prereg §5.5-5.6: 20261102, 20261103, 20261104 + r (r < 500)
A8_INPUT = "A1"  # v3 l.201 "Tạo caption bằng A1"
A8_DELETE = "rejected"  # v3 l.201 (registered); "coupled" only if the PI answers Q-A8 so
MAX_NEW = {"caption": 64, "verify": 8}  # J-T
DTYPE = "bfloat16"  # [proposal]; batch size 1 (padding changes greedy output)
GEN_BASE = {"do_sample": False, "num_beams": 1, "num_beam_groups": 1, "num_return_sequences": 1,
            "temperature": None, "top_k": None, "top_p": None, "typical_p": None, "repetition_penalty": 1.0,
            "no_repeat_ngram_size": 0, "encoder_no_repeat_ngram_size": 0, "length_penalty": 1.0,
            "diversity_penalty": 0.0, "min_new_tokens": 0, "early_stopping": False, "use_cache": True,
            "bad_words_ids": None, "forced_bos_token_id": None, "forced_eos_token_id": None,
            "renormalize_logits": False, "output_scores": False, "return_dict_in_generate": False}
LABELS = {"yes": "SUPPORTED", "maybe": "UNCERTAIN", "no": "REJECTED"}  # mBLIP Table 8: entail/neutral/contra
NEAR = 0.5  # v3 §7.4
VI_DELIM = {"và", "cùng", "còn", "nhưng", "trong khi"}  # [proposal] clause words that end a chunk
VI_SIZE = {"lớn", "nhỏ", "to", "cao", "thấp", "dài", "ngắn"}  # [proposal]; colours come from rescap.vi.lexicon
PUNCT_DELIM = set(",;:")
SENT_END = set(".!?")
MARK = "XQZSEPQX"  # batch separator line (scripts/kit_b/protocol_pilot.py pattern)

OVQA_REV = "cc85c24c863afb05b5a52f68950f9ba6b69975cf"
OVQA_URL = "https://huggingface.co/datasets/uitnlp/OpenViVQA-dataset/resolve/{rev}/{name}"
OVQA_JSON = {"vlsp2023_dev_data.json": (762438, "415ddd8b6fbb01f2c5d9b8fa0b2554fd9149992d"),
             "vlsp2023_test_data.json": (2500527, "0ae3f6982b42391a985d9b5fe454ab482aa5bb4d"),
             "vlsp2023_train_data.json": (6596293, "dae982c1463f49708c976d5de4dae453cd5eb266")}
OVQA_DEV = "vlsp2023_dev_data.json"
OVQA_COUNTS = {"vlsp2023_dev_data.json": (1070, 3545), "vlsp2023_train_data.json": (9129, 30833),
               "vlsp2023_test_data.json": (1000, 14035)}  # C_TEST l.28 (11-01 scratchpad count); (images, QA)
OVQA_DEV_ZIP = (165039269, "ff6a0e878bd0718425b3bf7e0455322111dc6e1ea2410cfd3eb7703216580f06")
BARRED = re.compile(r"oidv7-[^/]*-annotations|/dev/shm/c_pvr_gb|nocaps_val_4500_captions\.json", re.I)


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def fault(msg: str):
    raise SystemExit(f"FAULT: {msg}")


def refuse(p) -> Path:
    if BARRED.search(str(p)):
        raise SystemExit(f"REFUSED: {p} (prereg §9.6 / §11 barred path)")
    return Path(p)


def sha_file(p: Path, algo: str = "sha256") -> str:
    h = hashlib.new(algo)
    with open(refuse(p), "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def pinned(root: Path, key: str) -> Path:
    rel, sha = REPO_PINS[key]
    if sha_file(root / rel) != sha:
        fault(f"{rel} differs from its pin {sha[:8]}")
    return root / rel


def raw_tone_unset() -> None:
    if os.environ.get("RESCAP_RAW_TONE") is not None:  # N4: chair.py l.74, l.168 read it
        fault("RESCAP_RAW_TONE is set")


def clean(s: str) -> str:
    """NFC, newlines and whitespace runs -> one space, trimmed (prereg §6.4 table, first rows)."""
    return " ".join(unicodedata.normalize("NFC", s).split())


def jdump(o) -> bytes:
    return (json.dumps(o, sort_keys=True, ensure_ascii=False, indent=1) + "\n").encode()


def access_log(sealed: Path, action: str, path, sha: str) -> None:
    with open(sealed / "ACCESS_LOG.tsv", "a") as f:
        f.write(f"{utc()}\tc_pvr.py\t{action}\t{path}\t{sha}\n")


# ---------------------------------------------------------------------------------------------- prompts
def prompts(root: Path) -> dict:
    out = {}
    for name, sha in PROMPT_SHAS.items():
        b = (root / "scripts/c_pvr/prompts" / name).read_bytes()
        if hashlib.sha256(b).hexdigest() != sha:
            fault(f"prompt {name} differs from its pin {sha[:8]}")
        out[name] = b.decode("utf-8")
    return out


def render(P: dict, demos: list[str], lang: str) -> str:
    """PINS-A §2.1 rules 1-4: <= k lines, '{i}. {caption}', numbered 1..n; n = 0 -> zero-shot template."""
    if len(demos) > K:
        fault(f"{len(demos)} demonstrations > k = {K}")
    if not demos:
        return P[f"cap_{lang}_0.txt"]
    block = "\n".join(P["demo_line.txt"].replace("{i}", str(i)).replace("{caption}", clean(d))
                      for i, d in enumerate(demos, 1))
    return P[f"cap_{lang}_k.txt"].replace("{demos}", block)


def proposition(text: str) -> str:
    """CC-234 item 3: the exact {proposition} string = span text after clean(); '"' -> "'" (fixed quote rule)."""
    return clean(text).replace('"', "'")


def ver_prompt(P: dict, text: str) -> str:
    return P["ver_3way.txt"].replace("{proposition}", proposition(text))


def llava_prompt(text: str) -> str:
    return LLAVA["conv"].replace("{prompt}", text)


# ---------------------------------------------------------------------------------------------- verifier
FIRST_RUN = re.compile(r"[a-z]+")


def parse_label(ans: str) -> tuple[str, bool]:
    """PINS-A §2.3: NFC, casefold, first maximal ASCII-letter run; yes/maybe/no; anything else = UNCERTAIN and a
    parse failure (prereg §6.3). No fuzzy match, no second call."""
    m = FIRST_RUN.search(unicodedata.normalize("NFC", ans).casefold())
    lab = LABELS.get(m.group(0)) if m else None
    return (lab, False) if lab else ("UNCERTAIN", True)


def verify(props: list[dict], ask, arm: str) -> tuple[list[str], dict]:
    """J-C: props in their fixed order; the first CAP are asked, the rest are UNCERTAIN unverified (cap_hits)."""
    labels = []
    st = {"arm": arm, "calls": 0, "cap_hits": 0, "parse_fail": 0, "yes": 0, "maybe": 0, "no": 0}
    for j, p in enumerate(props):
        if j >= CAP:
            labels.append("UNCERTAIN")
            st["cap_hits"] += 1
            continue
        lab, bad = parse_label(ask(p["text"]))
        st["calls"] += 1
        if bad:
            st["parse_fail"] += 1
        else:
            st[{"SUPPORTED": "yes", "UNCERTAIN": "maybe", "REJECTED": "no"}[lab]] += 1
        labels.append(lab)
    return labels, st


def split_back(dcs: list[dict], flat: list) -> list[list]:
    out, i = [], 0
    for dc in dcs:
        out.append(flat[i:i + len(dc["props"])])
        i += len(dc["props"])
    return out


def pvr_masks(dcs: list[dict], ask, variant: str) -> tuple[list[list[bool]], dict]:
    """PVR-drop deletes REJECTED and UNCERTAIN, PVR-keep REJECTED only (prereg §6.3). One call budget per image
    over the demonstrations in rank order (demonstration 1 first, left to right)."""
    labels, st = verify([p for dc in dcs for p in dc["props"]], ask, f"PVR-{variant}")
    gone = {"drop": {"REJECTED", "UNCERTAIN"}, "keep": {"REJECTED"}}[variant]
    return split_back(dcs, [lab in gone for lab in labels]), st


def a8_mask(labels: list[str], rule: str = A8_DELETE) -> list[bool]:
    gone = {"rejected": {"REJECTED"}, "coupled": {"REJECTED", "UNCERTAIN"}}[rule]
    return [lab in gone for lab in labels]


def a8_caption(captions: dict, decompose_one, ask) -> tuple[str, dict]:
    """A8: the A1 caption (v3 l.201), same decomposer, same verifier prompt, same cap; output span deletion."""
    dc = decompose_one(captions[A8_INPUT])
    labels, st = verify(dc["props"], ask, "A8")
    out = rebuild(dc, a8_mask(labels))
    st["emptied"] = out is None
    return out or "", st


# ---------------------------------------------------------------------------------------------- arms
def arm_rng(arm: str, image_id: str) -> random.Random:
    """One generator per (arm seed, image id): str seeding is sha512-based, so no hash seed and no order effect."""
    return random.Random(f"{SEEDS[arm]}|{image_id}")


def pick(arm: str, image_id: str, ranked: list, datastore: list) -> list:
    """Demonstration ids per arm. ranked = retrieval order (rank 1 first, J-O); A2 and A3 keep their draw order."""
    if arm == "A0":
        return []
    if arm == "A2":
        return arm_rng("A2", image_id).sample(sorted(datastore), K)
    if arm == "A3":
        return arm_rng("A3", image_id).sample(list(ranked[:A3_TOP]), K)
    return list(ranked[:K])


def a7_masks(image_id: str, pvr: list[list[bool]]) -> list[list[bool]]:
    """Count-matched random drop, matched per demonstration (so the emptied count matches PVR's too, v3 §5.4)."""
    rng = arm_rng("A7", image_id)
    out = []
    for m in pvr:
        hit = set(rng.sample(range(len(m)), sum(m)))
        out.append([j in hit for j in range(len(m))])
    return out


def a12_masks(dcs: list[dict], status) -> list[list[bool]]:
    """Oracle (dev only): delete object propositions whose class the existing human labels call absent."""
    return [[p["kind"] == "obj" and any(status(c) == "absent" for c in p["classes"]) for p in dc["props"]]
            for dc in dcs]


def demos_after(dcs: list[dict], masks: list[list[bool]]) -> tuple[list[str], int]:
    """Span deletion per demonstration; an emptied demonstration is dropped, never back-filled (prereg §6.4)."""
    kept = [rebuild(dc, m) for dc, m in zip(dcs, masks)]
    return [t for t in kept if t is not None], sum(t is None for t in kept)


def a11_text(dc: dict) -> str | None:
    """A11: delete the extractor's spans (v3 §7.2), same reassembly; never 'emptied' by proposition count."""
    spans = [{"start": s, "end": e} for s, e, _ in extract(dc["text"])]
    return rebuild({**dc, "props": spans}, [True] * len(spans), emptied=False)


# ---------------------------------------------------------------------------------------------- reassembly
TIDY = (
    (re.compile(r"\s+"), " "),
    (re.compile(r"\s+([.,;:!?])"), r"\1"),
    (re.compile(r"([,;:])(?:\s*[,;:])+"), r"\1"),
    (re.compile(r"[,;:]\s*([.!?])"), r"\1"),
    (re.compile(r"^[\s,;:.!?]+"), ""),
    (re.compile(r"[\s,;:]+$"), ""),
)


def tidy(s: str) -> str:
    for rx, rep in TIDY:
        s = rx.sub(rep, s)
    return s.strip()


def rebuild(dc: dict, drop: list[bool], emptied: bool = True) -> str | None:
    """v3 §5.4: delete each dropped span; a sentence with a cut and no noun left goes; fixed whitespace/punctuation
    table. None = emptied demonstration (every proposition dropped, or nothing left)."""
    props = dc["props"]
    if emptied and props and all(drop):
        return None
    gone = [(p["start"], p["end"]) for p, d in zip(props, drop) if d]
    t, out = dc["text"], []
    for s, e in dc["sents"]:
        cut = [(max(a, s), min(b, e)) for a, b in gone if a < e and b > s]
        alive = [(a, b) for a, b in dc["nouns"] if s <= a and b <= e and not any(x <= a and b <= y for x, y in cut)]
        if cut and not alive:
            continue
        chars = list(t[s:e])
        for a, b in cut:
            chars[a - s:b - s] = [" "] * (b - a)
        piece = tidy("".join(chars))
        if piece:
            out.append(piece)
    return " ".join(out) or None


# ---------------------------------------------------------------------------------------------- decomposers
def build_props(text: str, toks: list, units: list, chunk: list, right) -> list[dict]:
    """One proposition per mapped mention: every token since the previous span (or the chunk start) in the same
    chunk, the mention, then the right extension. chunk[i] = -1 marks a delimiter token (never inside a span)."""
    props, floor = [], 0
    for n, (classes, ms, i0, i1) in enumerate(units):
        if i0 < floor or chunk[i0] < 0:
            continue
        nxt = units[n + 1][2] if n + 1 < len(units) else len(toks)
        a = i0
        while a > floor and chunk[a - 1] == chunk[i0]:
            a -= 1
        b = max(min(right(i1), nxt), i1)
        props.append({"kind": "obj", "classes": classes, "mentions": ms, "start": toks[a][0], "end": toks[b - 1][1],
                      "text": proposition(text[toks[a][0]:toks[b - 1][1]])})
        floor = b
    return props


def merge_units(units: list) -> list:
    """B2 rule [proposal]: mentions whose token ranges overlap (two objects inside one segmenter word, e.g.
    'quần_áo') become ONE proposition carrying every class; it is verified once and its label applies to all."""
    out = []
    for cls, ms, i0, i1 in sorted(units, key=lambda u: (u[2], u[3])):
        if out and i0 < out[-1][3]:
            c, m, j0, j1 = out[-1]
            out[-1] = (c + cls, m + ms, j0, max(j1, i1))
        else:
            out.append((cls, ms, i0, i1))
    return out


def check_props(props: list[dict]) -> None:
    """Invariants (CC-236 B2): every object proposition contains each of its mentions; spans are ordered and
    pairwise disjoint."""
    for p in props:
        if p["kind"] == "obj" and not all(p["start"] <= a and b <= p["end"] for a, b in p["mentions"]):
            fault("a proposition does not contain its mention")
    if any(p["end"] > q["start"] or p["start"] >= p["end"] for p, q in zip(props, props[1:])):
        fault("propositions overlap or are out of order")


def add_text_props(text: str, props: list[dict], spans: list) -> list[dict]:
    props += [{"kind": "text", "classes": [], "mentions": [], "start": s, "end": e, "text": proposition(x)}
              for s, e, x in spans]
    return sorted(props, key=lambda p: (p["start"], p["end"]))


def chunks(toks: list, delim, spans: list) -> list[int]:
    """Chunk id per token; delimiters and tokens inside an extractor span (scene text) get -1."""
    out, cid = [], 0
    for i, (s, e, _) in enumerate(toks):
        if delim(i) or any(a < e and s < b for a, b, _ in spans):
            cid += 1
            out.append(-1)
        else:
            out.append(cid)
    return out


def rdr(texts: list[str], vnc: Path = VNC_DIR) -> list[list[str]]:
    """VnCoreNLP-1.2 RDRSegmenter (wseg) over pipes, one marker line between texts; jar and models sha-checked."""
    for rel, sha in VNC_PINS.items():
        if sha_file(vnc / rel) != sha:
            fault(f"{vnc / rel} differs from its pin {sha[:8]}")
    inp = f"\n{MARK}\n".join(texts) + "\n"
    out = subprocess.run(JAVA, input=inp, capture_output=True, text=True, cwd=vnc, check=True).stdout
    segs, cur = [], []
    for line in out.splitlines():
        cols = line.split("\t")
        if len(cols) > 2 and cols[0].isdigit():
            if cols[1] == MARK:
                segs.append(cur)
                cur = []
            else:
                cur.append(cols[1])
    segs.append(cur)
    if len(segs) != len(texts):
        fault(f"RDR alignment lost: {len(segs)} != {len(texts)}")
    return segs


def align(text: str, words: list[str], fold=str.lower) -> list[tuple[int, int, str]]:
    """Segmenter syllables -> character offsets. B1: RDRSegmenter rewrites old-style tone placement (tòa -> toà),
    so both sides are compared after `fold` (lowercase + rescap norm_tone, length-preserving). The FAULT text never
    carries caption words."""
    toks, c = [], 0
    for w in words:
        start = None
        for syl in w.split("_"):
            while c < len(text) and text[c].isspace():
                c += 1
            if len(fold(syl)) != len(syl) or fold(text[c:c + len(syl)]) != fold(syl):
                fault("a segmenter token does not align with the caption")
            start = c if start is None else start
            c += len(syl)
        toks.append((start, c, w.replace("_", " ").lower()))
    return toks


def rescap_mods(root: Path):
    for k in ("chair", "lexicon"):
        pinned(root, k)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    import rescap.chair as chair
    from rescap.vi import lexicon
    return chair, lexicon


def vi_mentions(text: str, chair) -> list[tuple[str, int, int]]:
    """objects_in (the outcome instrument) located in the caption: same-length tone/case normalisation, colour
    phrases masked as objects_in strips them, then a left-to-right search at word boundaries."""
    s = chair.norm_tone(text.lower())
    if len(s) != len(text):
        fault("case/tone normalisation changed the caption length")
    for ph in chair._COLOUR_PHRASES:
        s = s.replace(ph, " " * len(ph))
    found, c = [], 0
    # ponytail: sequential search can land on a non-object use of the same noun earlier in the caption
    # (e.g. 'người' inside 'người ta'); a token-level port of objects_in is the upgrade if that shows up.
    for noun in chair.objects_in(text):
        rx = re.compile(r"(?<!\w)" + r"\s+".join(map(re.escape, chair.norm_tone(noun).split())) + r"(?!\w)")
        m = rx.search(s, c)
        if not m:
            fault("an objects_in mention is not located")
        found.append((noun, m.start(), m.end()))
        c = m.end()
    return found


def cover(toks: list, a: int, b: int) -> tuple[int, int]:
    i0 = next(i for i, t in enumerate(toks) if t[1] > a)
    i1 = max(i for i, t in enumerate(toks) if t[0] < b) + 1
    return i0, i1


def sentences(toks: list, ends) -> list[list[int]]:
    out, s0 = [], None
    for i, (s, e, w) in enumerate(toks):
        s0 = s if s0 is None else s0
        if ends(i):
            out.append([s0, e])
            s0 = None
    if s0 is not None:
        out.append([s0, toks[-1][1]])
    return out


def decompose_vi(texts: list[str], root: Path = ROOT, vnc: Path = VNC_DIR) -> list[dict]:
    raw_tone_unset()
    chair, lexicon = rescap_mods(root)
    keys = {k for k in json.loads(pinned(root, "vi_map").read_text("utf-8")) if not k.startswith("_")}
    attr = set(lexicon.COLORS) | {"màu"} | VI_SIZE
    texts = [clean(t) for t in texts]
    seen = [t.replace("_", " ") for t in texts]  # '_' is RDR's word joiner; same length, offsets unchanged
    try:
        segs = rdr(seen, vnc)
    except (SystemExit, subprocess.CalledProcessError):
        segs = [None] * len(seen)  # batch lost: segment caption by caption, so one bad caption costs only itself
    out = []
    for t, u, words in zip(texts, seen, segs):
        try:
            words = rdr([u], vnc)[0] if words is None else words
            out.append(_decompose_vi_one(t, u, words, chair, keys, attr))
        except SystemExit as e:
            if "differs from its pin" in str(e):
                raise
            out.append(decomp_fail(t, str(e)))
        except Exception as e:  # e.g. the java call; the reason names no caption word
            out.append(decomp_fail(t, type(e).__name__))
    return out


def decomp_fail(t: str, why: str) -> dict:
    """W1 [proposal]: a caption that cannot be decomposed gets zero propositions, is kept whole in every arm and is
    counted per arm and set as decomp_fail (reported beside P_obj^VI, not a gate). The reason never holds caption
    text: it is the FAULT message of this file, which names no caption word."""
    return {"text": t, "sents": [[0, len(t)]] if t else [], "nouns": [], "props": [], "decomp_fail": why}


def _decompose_vi_one(t: str, u: str, words: list[str], chair, keys: set, attr: set) -> dict:
    toks = align(u, words, lambda x: chair.norm_tone(x.lower()))
    if not toks:
        return {"text": t, "sents": [], "nouns": [], "props": []}
    spans = scene_spans(t)
    ch = chunks(toks, lambda i: toks[i][2] in PUNCT_DELIM | SENT_END | VI_DELIM, spans)
    ments = vi_mentions(u, chair)
    units = merge_units([([noun], [[a, b]], *cover(toks, a, b)) for noun, a, b in ments if noun in keys])
    low = chair.norm_tone(u.lower())
    phrase_end = {}  # W2: a multi-word colour phrase right after an object stays with it ('áo màu xanh lá cây')
    for i, (s0, _, _) in enumerate(toks):
        for ph in chair._COLOUR_PHRASES:
            if low.startswith(ph, s0):
                j = next((j for j in range(i, len(toks)) if toks[j][1] == s0 + len(ph)), None)
                if j is not None and all(ch[x] == ch[i] for x in range(i, j + 1)):
                    phrase_end[i] = max(phrase_end.get(i, 0), j + 1)

    def right(i):
        while i < len(toks) and ch[i] == ch[i - 1]:
            if toks[i][2] in attr:
                i += 1
            elif i in phrase_end:
                i = phrase_end[i]
            else:
                break
        return i

    props = add_text_props(t, build_props(t, toks, units, ch, right), spans)
    check_props(props)
    return {"text": t, "sents": sentences(toks, lambda i: toks[i][2] in SENT_END),
            "nouns": [[a, b] for _, a, b in ments], "props": props}


def spacy_nlp():
    import spacy
    nlp = spacy.load("en_core_web_sm")
    got = {"spacy": spacy.__version__, "en_core_web_sm": nlp.meta["version"]}
    if any(got[k] != LIB_VERSIONS[k] for k in got):
        fault(f"spaCy versions {got} differ from the lock")
    return nlp


def en_forms(root: Path) -> dict[str, str]:
    d = json.loads((root / EN_MAP).read_text("utf-8"))
    return {f: k for k, v in d["classes"].items() for f in v["en"]}


def decompose_en(texts: list[str], root: Path = ROOT, nlp=None) -> list[dict]:
    nlp = nlp or spacy_nlp()
    forms = en_forms(root)
    width = max(len(f.split()) for f in forms)
    out = []
    for t in (clean(x) for x in texts):
        try:
            out.append(_decompose_en_one(t, nlp, forms, width))
        except Exception as e:  # W1: one caption, counted; the reason names no caption word
            out.append(decomp_fail(t, type(e).__name__))
        except SystemExit as e:
            out.append(decomp_fail(t, str(e)))
    return out


def _decompose_en_one(t: str, nlp, forms: dict, width: int) -> dict:
    doc = nlp(t)
    toks = [(w.idx, w.idx + len(w.text), w.lower_) for w in doc]
    if not toks:
        return {"text": t, "sents": [], "nouns": [], "props": []}
    spans = scene_spans(t)
    starts = {s.start for s in doc.sents} - {0}
    ch = chunks(toks, lambda i: (doc[i].is_punct and doc[i].text in PUNCT_DELIM | SENT_END)
                or doc[i].dep_ == "cc" or i in starts, spans)
    units, i = [], 0
    while i < len(doc):
        for n in range(min(width, len(doc) - i), 0, -1):
            f = " ".join(toks[j][2] for j in range(i, i + n))
            if f in forms and doc[i + n - 1].pos_ in ("NOUN", "PROPN"):
                units.append(([forms[f]], [[toks[i][0], toks[i + n - 1][1]]], i, i + n))
                i += n
                break
        else:
            i += 1
    props = add_text_props(t, build_props(t, toks, units, ch, lambda i: i), spans)
    check_props(props)
    return {"text": t, "sents": [[s.start_char, s.end_char] for s in doc.sents],
            "nouns": [[w.idx, w.idx + len(w.text)] for w in doc if w.pos_ in ("NOUN", "PROPN")], "props": props}


# ---------------------------------------------------------------------------------------------- EN map (N13)
QUAL = re.compile(r"\s*\(.*\)$")
IRREGULAR = {"buffalo": "buffaloes", "human": "humans", "man": "men", "woman": "women", "child": "children",
             "person": "people", "goose": "geese", "knife": "knives", "mouse": "mice", "foot": "feet", "tooth": "teeth"}


def plural(form: str) -> str | None:
    """Regular English plural of the head word (the word before ' of ', else the last); None when the form is
    already plural or a plural-only noun (ends in 's' but not 'ss'/'us', or is an irregular plural)."""
    words = form.split(" ")
    h = words.index("of") - 1 if "of" in words[1:] else len(words) - 1
    w = words[h]
    if w in IRREGULAR.values() or (w.endswith("s") and not w.endswith(("ss", "us"))):
        return None
    if w in IRREGULAR:
        p = IRREGULAR[w]
    elif w.endswith("man"):
        p = w[:-3] + "men"
    elif re.search(r"(s|x|z|ch|sh)$", w):
        p = w + "es"
    elif re.search(r"[^aeiou]y$", w):
        p = w[:-1] + "ies"
    else:
        p = w + "s"
    return " ".join([*words[:h], p, *words[h + 1:]])


def build_en_map(vi: dict) -> dict:
    """[proposal, OPEN row] Mechanical lexicon: each class's OI pos display names, lowercased, qualifier in
    parentheses dropped, plus a regular plural. A form claimed by several classes goes to the class that names it
    in its own neg list, then the class with the shortest pos list, then the first in file order. pos/neg are
    copied unchanged."""
    keys = [k for k in vi if not k.startswith("_")]

    def names(lst):
        return {QUAL.sub("", n).lower() for n in lst}

    claims: dict[str, list[str]] = {}
    for k in keys:
        for f in sorted(names(vi[k]["pos"])):
            claims.setdefault(f, []).append(k)
    cls = {k: {"en": [], "pos": vi[k]["pos"], "neg": vi[k]["neg"]} for k in keys}
    for f, ks in sorted(claims.items()):
        cls[min(ks, key=lambda k: (f not in names(vi[k]["neg"]), len(vi[k]["pos"]), keys.index(k)))]["en"].append(f)
    for k in keys:
        more = {plural(f) for f in cls[k]["en"]} - {None}
        cls[k]["en"] = sorted(set(cls[k]["en"]) | {f for f in more if f not in claims})
    return {"_note": "English mention lexicon -> the 69 classes of vi_oiv7_map.json (27f2b1ca); pos/neg copied "
                     "unchanged; built by c_pvr.py en-map; P_obj^EN is descriptive, never a gate (prereg §3.4).",
            "_collisions": {f: ks for f, ks in sorted(claims.items()) if len(ks) > 1},
            "classes": cls}


def en_map_bytes(root: Path) -> bytes:
    return jdump(build_en_map(json.loads(pinned(root, "vi_map").read_text("utf-8"))))


# ---------------------------------------------------------------------------------------------- proxy (v3 §7)
QUOTE = re.compile(r'"([^"]+)"|“([^”]+)”|(?<![^\W_])\'([^\']+)\'(?![^\W_])|«([^»]+)»')
CUE = re.compile(r"(?<!\w)(?:dòng chữ|có tên|chữ|ghi)\s+([^.,;:!?\"“”«»']+)", re.I)
TOKEN = re.compile(r"\S+")
EDGE = re.compile(r"^[^\w]+|[^\w]+$")


def question_rx(root: Path) -> list[re.Pattern]:
    lines = pinned(root, "proxy_regex").read_text("utf-8").splitlines()
    return [re.compile(r"(?<!\w)(?:" + x + r")(?!\w)") for x in lines]


def is_text_question(q: str, rxs: list[re.Pattern]) -> bool:
    """v3 §7.1: question text only (never the answer or the image)."""
    qn = unicodedata.normalize("NFC", q).casefold()
    return any(rx.search(qn) for rx in rxs)


def extract(text: str, tokens: bool = True) -> list[tuple[int, int, str]]:
    """v3 §7.2 (the proxy's and A11's extractor): quoted spans (deletion span includes the quotes), spans after cue
    words cut at punctuation, tokens that are all-caps (>= 2 letters [proposal]) or contain a digit. Non-overlapping.
    tokens=False (decomposer scene-text propositions): quoted and cue spans only, so a count stays in its object
    proposition."""
    t = unicodedata.normalize("NFC", text)
    found = []
    for m in QUOTE.finditer(t):
        g = next(i for i in range(1, 5) if m.group(i) is not None)
        found.append((m.start(), m.end(), m.group(g)))
    for m in CUE.finditer(t):
        found.append((m.start(1), m.end(1), m.group(1).strip()))
    for m in TOKEN.finditer(t) if tokens else ():
        core = EDGE.sub("", m.group())
        letters = [c for c in core if c.isalpha()]
        if core and (any(c.isdigit() for c in core) or (len(letters) >= 2 and all(c.isupper() for c in letters))):
            s = m.start() + m.group().index(core)
            found.append((s, s + len(core), core))
    out = []
    for s, e, x in sorted(found, key=lambda z: (z[0], -z[1])):
        if x.strip() and not any(a < e and s < b for a, b, _ in out):
            out.append((s, e, x))
    return out


def scene_spans(text: str) -> list[tuple[int, int, str]]:
    return extract(text, tokens=False)


def norm(s: str, strip_marks: bool = False) -> str:
    """v3 §7.3: NFC -> casefold -> punctuation out, letters and digits kept -> whitespace collapsed. Diacritics are
    kept in the main rule; strip_marks is the sensitivity analysis only."""
    s = unicodedata.normalize("NFC", s).casefold()
    if strip_marks:
        s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").replace("đ", "d")
    return " ".join(re.sub(r"[^\w\s]|_", " ", s).split())


def classify(s: str, answers: list[str]) -> str:
    """v3 §7.4 on normalised strings: match (equal, or containment when the shorter has >= 3 chars); near (a shared
    token of >= 2 chars, or normalized Levenshtein similarity >= 0.5); else uncovered."""
    from rapidfuzz.distance import Levenshtein
    if any(s == a or (min(len(s), len(a)) >= 3 and (s in a or a in s)) for a in answers):
        return "match"
    st = {w for w in s.split() if len(w) >= 2}
    if any(st & {w for w in a.split() if len(w) >= 2} or Levenshtein.normalized_similarity(s, a) >= NEAR
           for a in answers):
        return "near"
    return "uncovered"


def proxy_counts(caption: str, answers: list[str], strip_marks: bool = False) -> dict:
    ans = [a for a in (norm(x, strip_marks) for x in answers) if a]
    c = {"match": 0, "near": 0, "uncovered": 0, "n_answers": len(ans)}
    for _, _, x in extract(caption):
        s = norm(x, strip_marks)
        if s:
            c[classify(s, ans)] += 1
    cap = f" {norm(caption, strip_marks)} "
    c["answers_found"] = sum(f" {a} " in cap for a in ans)
    return c


def p_text(c: dict, w: int = 1) -> float | None:
    d = c["match"] + c["near"] + w * c["uncovered"]
    return c["match"] / d if d else None


# ---------------------------------------------------------------------------------------------- models (GPU host)
def gen_config(kind: str, eos: int, pad: int) -> dict:
    return {**GEN_BASE, "max_new_tokens": MAX_NEW[kind], "eos_token_id": eos, "pad_token_id": pad}


def load_mblip(snap: Path, files: dict = MBLIP["files"]):
    """Load-time sha check of PINS-A §1, then safetensors only (the repo also holds .bin weights, W10)."""
    for f, sha in files.items():
        if sha_file(snap / f) != sha:
            fault(f"{f} differs from its pin {sha[:8]}; nothing is decoded")
    import torch
    from transformers import Blip2ForConditionalGeneration, Blip2Processor
    proc = Blip2Processor.from_pretrained(snap, local_files_only=True)
    model = Blip2ForConditionalGeneration.from_pretrained(snap, local_files_only=True, use_safetensors=True,
                                                          torch_dtype=getattr(torch, DTYPE))
    return model.eval(), proc


def generate(model, proc, image, prompt: str, kind: str) -> tuple[str, str]:
    """One image per call (batch 1). The model's own generation_config is replaced by the pinned dict, and the same
    dict is passed explicitly. Prompt ids are stripped only when the output starts with them."""
    import torch
    from transformers import GenerationConfig
    tok = proc.tokenizer
    gc = gen_config(kind, tok.eos_token_id, tok.pad_token_id)
    model.generation_config = GenerationConfig(**gc)
    x = proc(images=[image], text=[prompt], return_tensors="pt").to(model.device, getattr(torch, DTYPE))
    with torch.inference_mode():
        out = model.generate(**x, generation_config=GenerationConfig(**gc))[0].tolist()
    ids = x["input_ids"][0].tolist()
    new = out[len(ids):] if out[:len(ids)] == ids else out
    finish = "eos" if tok.eos_token_id in new else "length" if len(new) >= gc["max_new_tokens"] else "other"
    return tok.decode(new, skip_special_tokens=True).strip(), finish


def load_llava(*_):
    fault("LLaVA inference-code commit and weight format are OPEN (PINS-A §11); EN decode refused until pinned")


def header(root: Path) -> dict:
    return {"label": LABEL, "c_pvr_sha256": sha_file(Path(__file__)), "prompts": PROMPT_SHAS, "k": K, "cap": CAP,
            "seeds": SEEDS, "a8_input": A8_INPUT, "a8_delete": A8_DELETE, "dtype": DTYPE, "batch": 1,
            "mblip": {"repo": MBLIP["repo"], "revision": MBLIP["revision"]},
            "llava": {"repo": LLAVA["repo"], "revision": LLAVA["revision"]},
            "generation": {k: gen_config(k, "<tokenizer eos>", "<tokenizer pad>") for k in MAX_NEW},
            "libs": LIB_VERSIONS, "vnc": VNC_PINS, "oi_test_url": OI_TEST_URL}


# ---------------------------------------------------------------------------------------------- ovqa-pin (NB-OVQA)
def blob_hashes(p: Path) -> tuple[int, str, str]:
    """One pass: size, sha256 and git-blob SHA-1 = sha1(b'blob <size>\\0' + bytes)."""
    n = p.stat().st_size
    h2, h1 = hashlib.sha256(), hashlib.sha1(b"blob %d\0" % n)
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h2.update(c)
            h1.update(c)
    return n, h2.hexdigest(), h1.hexdigest()


def curl_argv(name: str, part: Path) -> list[str]:
    return ["curl", "-sS", "--fail", "-A", "vsps-research", "-o", str(part),
            OVQA_URL.format(rev=OVQA_REV, name=name)]


def custody(dest: Path) -> Path:
    if str(dest.resolve()).startswith("/mnt/"):
        fault(f"{dest} must sit on the WSL ext4 home (NB-OVQALOST)")
    dest.mkdir(mode=0o700, parents=True, exist_ok=True)
    if dest.stat().st_mode & 0o077:
        fault(f"{dest} is not mode 0700")
    return dest


def ovqa_fetch(dest: Path, sealed: Path, spec: dict = OVQA_JSON, get=None) -> dict:
    get = get or (lambda name, part: subprocess.run(curl_argv(name, part)).returncode)
    custody(dest)
    rec = {"label": LABEL, "revision": OVQA_REV, "files": {}}
    for name, (size, sha1) in sorted(spec.items()):
        final, part = dest / name, dest / f"{name}.part"
        if final.exists():
            fault(f"{final} exists (one download)")
        rc = get(name, part)
        n, s256, s1 = blob_hashes(part) if part.exists() else (-1, "", "")
        if rc or n != size or s1 != sha1:
            part.unlink(missing_ok=True)
            access_log(sealed, "ovqa-pin FAULT", name, f"rc={rc} size={n} sha1={s1[:8]}")
            fault(f"{name}: rc {rc}, size {n} / {size}, git-blob {s1[:8]} / {sha1[:8]}; .part unlinked")
        os.chmod(part, 0o400)
        os.replace(part, final)
        access_log(sealed, "ovqa-pin fetch", name, s256)
        rec["files"][name] = {"size": n, "sha256": s256, "git_blob_sha1": s1}
    pin = dest / "ovqa_pin.json"
    if pin.exists():
        fault(f"{pin} exists")
    pin.write_bytes(jdump(rec))
    os.chmod(pin, 0o400)
    return rec


def ovqa_load(dest: Path, sealed: Path, name: str):
    rec = json.loads((dest / "ovqa_pin.json").read_text())
    p = dest / name
    sha = sha_file(p)
    if sha != rec["files"][name]["sha256"]:
        fault(f"{name} differs from ovqa_pin.json")
    access_log(sealed, "ovqa-pin read keys/lengths", name, sha)
    return json.loads(p.read_bytes())


def shape(v, depth: int = 0) -> dict:
    """Key names (top level only), value type names and container lengths. No value, no string length."""
    out = {"type": type(v).__name__}
    if isinstance(v, (dict, list)):
        vals = list(v.values()) if isinstance(v, dict) else v
        out["len"] = len(v)
        out["value_types"] = sorted({type(x).__name__ for x in vals})
        recs = [x for x in vals if isinstance(x, dict)]
        if recs:
            f = sorted({k for r in recs for k in r})
            out["record_fields"] = f if len(f) <= 24 else len(f)
        if depth == 0 and isinstance(v, dict) and len(v) <= 16:
            out["keys"] = {k: shape(x, 1) for k, x in v.items()}
    return out


def ovqa_skeleton(dest: Path, sealed: Path) -> dict:
    return {name: shape(ovqa_load(dest, sealed, name)) for name in sorted(OVQA_JSON)}


def ovqa_count(dest: Path, sealed: Path, rule_path: Path, rule_sha: str, dev_zip: Path | None = None) -> dict:
    """The counting rule (written into a LOG line before this runs) names, per file, the top-level container of
    images and of QA. W5: lengths only; a file whose image count would need field values asserts its QA length
    only. (c): the dev image names (the one string field allowed) must be members of dev-images.zip."""
    if sha_file(rule_path) != rule_sha:
        fault("counting rule differs from the sha in its LOG line")
    rule = json.loads(rule_path.read_text())
    got = {}
    for name, (ni, nq) in sorted(OVQA_COUNTS.items()):
        d, r = ovqa_load(dest, sealed, name), rule[name]
        g = {"qa": len(d[r["qa"]])}
        if r.get("images") is not None:
            g["images"] = len(d[r["images"]])
        elif name == OVQA_DEV:
            fault("the dev rule must name its images container (1,070 is asserted)")
        if g["qa"] != nq or g.get("images", ni) != ni:
            fault(f"{name}: {g} differs from images {ni} / QA {nq}")
        got[name] = g
    if dev_zip is not None:
        d, r = ovqa_load(dest, sealed, OVQA_DEV), rule[OVQA_DEV]
        ims = d[r["images"]]
        fld = r["image_names"]
        names = list(ims.values()) if fld == "values" else [x[fld.split(":", 1)[1]] for x in ims]
        if not all(isinstance(x, str) for x in names) or len(set(names)) != OVQA_COUNTS[OVQA_DEV][0]:
            fault("dev image names are not 1,070 distinct strings")
        n, s256, _ = blob_hashes(dev_zip)
        if (n, s256) != OVQA_DEV_ZIP:
            fault("dev-images.zip differs from its LFS pin")
        with zipfile.ZipFile(dev_zip) as z:
            members = {Path(m).name for m in z.namelist() if not m.endswith("/")}
        missing = sum(Path(x).name not in members for x in names)
        if missing:
            fault(f"{missing} dev image names are not in dev-images.zip")
        got["dev_names_in_zip"] = len(names)
    return got


# ---------------------------------------------------------------------------------------------- selftest
def _must(msg: str, fn, *a, **k) -> None:
    try:
        fn(*a, **k)
    except SystemExit as e:
        assert msg in str(e), (msg, str(e))
        return
    raise AssertionError(f"expected {msg!r}")


def _lev(a: str, b: str) -> int:
    row = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        prev, row[0] = row[0], i
        for j, cb in enumerate(b, 1):
            prev, row[j] = row[j], min(row[j] + 1, row[j - 1] + 1, prev + (ca != cb))
    return row[-1]


VI_FIX = ["Một người đàn ông tí hon ôm áo tím ngáp cạnh chiếc xe đạp gỗ.",
          "Hai con chó màu cam nhảy lò cò trên mái tôn, và một con mèo đếm sao.",
          'Tấm biển ghi "PHỞ 24" trước ngôi nhà.', "2 con chó đang chạy trên cỏ.",
          "Tòa nhà cao bên cạnh dòng sông.", "Người thủy thủ khỏe mạnh đứng trên thuyền hòa bình.",
          "Chiếc xe_máy màu bạc ngủ đông.", "Ba chiếc thuyền buồm hát vang trên sông băng.",
          "Người đàn ông râu bạc thêu quần áo tím.", "Một gian hàng đổi giày dép lấy dưa.",
          "Bàn ghế nhảy múa trong phòng.", "Quần áo tự gấp mình trên dây điện.",
          "Một chiếc áo màu xanh lá cây treo trên cây.", "người người người"]
EN_FIX = ["A man in a mauve shirt juggling a bicycle, and two dogs are knitting near the volcano.",
          'A sign reads "OPEN 24" above the house.']
VI_PROPS = [["Một người đàn ông", "tí hon ôm áo tím", "ngáp cạnh chiếc xe đạp"],
            ["Hai con chó màu cam", "một con mèo"],
            ["PHỞ 24", "trước ngôi nhà"], ["2 con chó"],
            ["Tòa nhà cao", "bên cạnh dòng sông"], ["Người", "thủy thủ khỏe mạnh đứng trên thuyền"],
            ["Chiếc xe_máy màu bạc"], ["Ba chiếc thuyền buồm", "hát vang trên sông"],
            ["Người đàn ông", "râu bạc thêu quần áo tím"], ["Một gian hàng đổi giày dép"],
            ["Bàn ghế", "nhảy múa trong phòng"], ["Quần áo"],
            ["Một chiếc áo màu xanh lá cây", "treo trên cây"], ["người người", "người"]]
VI_CLASSES = {7: [["thuyền", "buồm"], ["sông"]], 8: [["đàn ông"], ["quần", "áo"]], 9: [["giày", "dép"]],
              11: [["quần", "áo"]], 12: [["áo"], ["cây"]]}
EN_PROPS = [["A man", "in a mauve shirt", "juggling a bicycle", "two dogs"], ["OPEN 24", "above the house"]]


def _st_text(P: dict) -> None:
    # 1-2 render: 4, 3 and 0 demonstrations; whitespace table; renumbering; zero-shot fallback
    four = render(P, ["a  b", "c\nd", "e", "f"], "vi")
    assert four == "Captions of similar images:\n1. a b\n2. c d\n3. e\n4. f\nCaption in Vietnamese:", four
    assert render(P, ["x", "y", "z"], "en").split("\n")[1:4] == ["1. x", "2. y", "3. z"]
    assert render(P, [], "vi") == "Caption in Vietnamese:" and render(P, [], "en") == P["cap_en_0.txt"]
    assert render(P, ["{i} {caption}"], "vi").split("\n")[1] == "1. {i} {caption}"
    _must("> k", render, P, list("abcde"), "vi")
    assert clean(unicodedata.normalize("NFD", "Phở  bò\n")) == "Phở bò"
    # 3 parser (CC-234 item 14 fixtures included)
    want = {"Yes": ("SUPPORTED", False), "yes.": ("SUPPORTED", False), " Maybe,": ("UNCERTAIN", False),
            "No": ("REJECTED", False), "": ("UNCERTAIN", True), "Có": ("UNCERTAIN", True),
            "không": ("UNCERTAIN", True), "yesno": ("UNCERTAIN", True), "The answer is yes": ("UNCERTAIN", True)}
    for a, w in want.items():
        assert parse_label(a) == w, (a, parse_label(a))
    # quote rule
    assert proposition(' a  "b" ') == "a 'b'"
    vp = ver_prompt(P, 'chữ "X"')
    assert vp == "Is it guaranteed true that \"chữ 'X'\"? Yes, no, or maybe? Answer in English:" and vp.count('"') == 2
    assert llava_prompt("Q").endswith("USER: <image>\nQ ASSISTANT:")


def _st_verify() -> None:
    props = [{"text": f"p{j}", "start": 0, "end": 1} for j in range(40)]
    asked = []

    def ask(t):
        asked.append(t)
        return ["yes", "maybe", "no", "Có"][len(asked) % 4]

    labels, st = verify(props, ask, "PVR-drop")
    assert asked == [f"p{j}" for j in range(CAP)] and st["calls"] == CAP == 32 and st["cap_hits"] == 8
    assert labels[CAP:] == ["UNCERTAIN"] * 8 and st["parse_fail"] == 8 and st["yes"] == st["maybe"] == st["no"] == 8
    # cap single source: PVR and A8 each spend exactly CAP calls on 40 propositions; the literal appears once
    dcs = [{"props": props[:10]}, {"props": props[10:]}]
    asked.clear()
    masks, st = pvr_masks(dcs, lambda t: asked.append(t) or "no", "keep")
    assert len(asked) == CAP and [len(m) for m in masks] == [10, 30] and sum(map(sum, masks)) == CAP
    asked.clear()
    dc = {"text": "x", "sents": [[0, 1]], "nouns": [], "props": props}
    out, st = a8_caption({"A0": "zero", "A1": "one"}, lambda c: {**dc, "src": c}, lambda t: asked.append(t) or "no")
    assert len(asked) == CAP and st["cap_hits"] == 8 and st["arm"] == "A8"
    tree = ast.parse(Path(__file__).read_text("utf-8"))
    n32 = sum(isinstance(n, ast.Constant) and n.value == 32 for top in tree.body
              if not (isinstance(top, ast.FunctionDef) and top.name.startswith("_st")) for n in ast.walk(top))
    assert n32 == 1, n32  # outside the selftest the cap literal exists once: CAP
    # A8 input = A1 caption; deletion switch both values; registered default
    seen = []
    a8_caption({"A0": "zero", "A1": "one"}, lambda c: seen.append(c) or {**dc, "props": []}, lambda t: "yes")
    assert seen == ["one"] and A8_INPUT == "A1" and A8_DELETE == "rejected"
    lab = ["SUPPORTED", "UNCERTAIN", "REJECTED"]
    assert a8_mask(lab) == [False, False, True] == a8_mask(lab, "rejected")
    assert a8_mask(lab, "coupled") == [False, True, True]
    d2 = [{"props": [{"text": "a"}, {"text": "b"}, {"text": "c"}]}]
    for variant, want in (("drop", [[False, True, True]]), ("keep", [[False, False, True]])):
        ans = iter(["yes", "maybe", "no"])
        assert pvr_masks(d2, lambda t, ans=ans: next(ans), variant)[0] == want, variant


def _st_arms() -> None:
    ranked, ds = [f"r{j}" for j in range(10)], [f"d{j}" for j in range(50)]
    assert pick("A1", "i1", ranked, ds) == ["r0", "r1", "r2", "r3"] and pick("A0", "i1", ranked, ds) == []
    a2, a3 = pick("A2", "i1", ranked, ds), pick("A3", "i1", ranked, ds)
    assert a2 == ["d22", "d46", "d39", "d43"] and a3 == ["r6", "r0", "r5", "r2"], (a2, a3)
    pick("A2", "other", ranked, ds)
    assert pick("A2", "i1", ranked, ds[::-1]) == a2 and pick("A3", "i1", ranked, ds) == a3  # order-free
    assert len(set(SEEDS.values())) == 3 and not set(SEEDS.values()) & set(BOOT_SEEDS)
    pvr = [[True] * 3 + [False] * 5, [True, True], [False]]
    a7 = a7_masks("i1", pvr)
    assert [sum(m) for m in a7] == [3, 2, 0] and a7 == a7_masks("i1", pvr), a7
    assert [j for j, x in enumerate(a7[0]) if x] == [3, 5, 6], a7[0]
    dcs = [{"props": [{"kind": "obj", "classes": ["chó"]}, {"kind": "text", "classes": []},
                      {"kind": "obj", "classes": ["mèo"]}, {"kind": "obj", "classes": ["quần", "áo"]}]}]
    assert a12_masks(dcs, {"chó": "absent", "mèo": "present", "quần": "present", "áo": "absent"}.get) == [
        [True, False, False, True]]


def _st_rebuild() -> None:
    def at(t, w, k=0):
        i = t.index(w, k)
        return {"start": i, "end": i + len(w)}

    t = "Một người đàn ông tí hon ôm áo tím ngáp cạnh chiếc xe đạp gỗ. Trời nắng."
    p = [at(t, "Một người đàn ông"), at(t, "tí hon ôm áo tím"), at(t, "ngáp cạnh chiếc xe đạp")]
    dc = {"text": t, "sents": [[0, t.index(".") + 1], [t.index("Trời"), len(t)]], "props": p,
          "nouns": [[at(t, w)["start"], at(t, w)["end"]] for w in ("đàn ông", "áo", "xe đạp")]}
    assert rebuild(dc, [False, True, False]) == "Một người đàn ông ngáp cạnh chiếc xe đạp gỗ. Trời nắng."
    assert rebuild(dc, [False, False, False]) == t
    assert rebuild(dc, [True, True, True]) is None
    assert rebuild(dc, [True, True, True], emptied=False) == "Trời nắng."
    t2 = "Hai con chó gầy , và một con mèo đếm sao ."
    d2 = {"text": t2, "sents": [[0, len(t2)]], "props": [at(t2, "Hai con chó gầy"), at(t2, "một con mèo")],
          "nouns": [[at(t2, w)["start"], at(t2, w)["end"]] for w in ("chó", "mèo")]}
    assert rebuild(d2, [True, False]) == "và một con mèo đếm sao."
    assert rebuild(d2, [False, True]) == "Hai con chó gầy, và đếm sao."
    assert rebuild(d2, [True, True], emptied=False) is None  # 'và đếm sao' has no noun left -> sentence dropped
    kept, n_empty = demos_after([dc, d2], [[True, True, True], [True, False]])
    assert kept == ["và một con mèo đếm sao."] and n_empty == 1  # dropped, not back-filled


def _st_decompose(root: Path, vnc: Path, nlp) -> None:
    vi = decompose_vi(VI_FIX, root, vnc)
    assert [[p["text"] for p in d["props"]] for d in vi] == VI_PROPS, [[p["text"] for p in d["props"]] for d in vi]
    assert not any("decomp_fail" in d for d in vi)
    assert [p["classes"] for p in vi[0]["props"]] == [["đàn ông"], ["áo"], ["xe đạp"]]
    for i, want in VI_CLASSES.items():
        assert [p["classes"] for p in vi[i]["props"] if p["kind"] == "obj"] == want, (i, vi[i]["props"])
    for d in vi:  # B2 invariants on every fixture, checked here as well as inside the decomposer
        for p in d["props"]:
            assert all(p["start"] <= a and b <= p["end"] for a, b in p["mentions"])
        assert all(p["end"] <= q["start"] for p, q in zip(d["props"], d["props"][1:]))
    assert rebuild(vi[8], [False, True]) == "Người đàn ông."
    assert rebuild(vi[4], [True, False]) == "bên cạnh dòng sông."
    bad = [{"kind": "obj", "mentions": [[5, 9]], "start": 0, "end": 4}]
    _must("does not contain its mention", check_props, bad)
    _must("overlap", check_props, [{"kind": "text", "mentions": [], "start": 0, "end": 6},
                                   {"kind": "text", "mentions": [], "start": 5, "end": 9}])
    check_props([{"kind": "obj", "mentions": [[2, 4]], "start": 0, "end": 4},
                 {"kind": "text", "mentions": [], "start": 4, "end": 9}])
    assert merge_units([(["a"], [[0, 1]], 0, 1), (["b"], [[2, 3]], 0, 1), (["c"], [[5, 6]], 2, 3)]) == [
        (["a", "b"], [[0, 1], [2, 3]], 0, 1), (["c"], [[5, 6]], 2, 3)]
    # W1: a caption that cannot be aligned costs only itself; kept whole; the reason holds no caption word
    real = globals()["rdr"]
    globals()["rdr"] = lambda texts, vnc=vnc: [["zzz"] if "mèo" in x else real([x], vnc)[0] for x in texts]
    try:
        two = decompose_vi(["Con mèo đếm sao.", VI_FIX[0]], root, vnc)
    finally:
        globals()["rdr"] = real
    assert two[0]["props"] == [] and "mèo" not in two[0]["decomp_fail"] and "decomp_fail" not in two[1]
    assert rebuild(two[0], []) == "Con mèo đếm sao." and len(two[1]["props"]) == 3
    assert rebuild(vi[0], [False, True, False]) == "Một người đàn ông ngáp cạnh chiếc xe đạp gỗ."
    assert rebuild(vi[2], [True, False]) == "Tấm biển ghi trước ngôi nhà."
    en = decompose_en(EN_FIX, root, nlp)
    assert [[p["text"] for p in d["props"]] for d in en] == EN_PROPS, [[p["text"] for p in d["props"]] for d in en]
    assert [p["classes"] for p in en[0]["props"]] == [["đàn ông"], ["áo"], ["xe đạp"], ["chó"]]
    assert rebuild(en[0], [False, True, False, False]) == ("A man juggling a bicycle, and two dogs are knitting "
                                                           "near the volcano.")
    os.environ["RESCAP_RAW_TONE"] = "1"
    try:
        _must("RESCAP_RAW_TONE is set", decompose_vi, VI_FIX[:1], root, vnc)
    finally:
        del os.environ["RESCAP_RAW_TONE"]
    # determinism: two fresh processes per language, byte-equal (hash randomisation differs between them)
    for lang, fx in (("vi", VI_FIX), ("en", EN_FIX)):
        runs = [subprocess.run([sys.executable, "-I", "-B", __file__, "decompose", "--lang", lang, "--root", str(root)],
                               input=json.dumps(fx), capture_output=True, text=True, check=True).stdout
                for _ in range(2)]
        assert runs[0] == runs[1] and json.loads(runs[0])[0]["props"], lang


def _st_en_map(root: Path) -> None:
    vi = json.loads(pinned(root, "vi_map").read_text("utf-8"))
    m = build_en_map(vi)
    keys = [k for k in vi if not k.startswith("_")]
    assert list(m["classes"]) == keys and len(keys) == 69
    assert all(m["classes"][k]["pos"] == vi[k]["pos"] and m["classes"][k]["neg"] == vi[k]["neg"] for k in keys)
    forms = [f for v in m["classes"].values() for f in v["en"]]
    assert len(forms) == len(set(forms))
    own = {f: k for k, v in m["classes"].items() for f in v["en"]}
    assert own["man"] == "đàn ông" and own["car"] == "ô tô" and own["men"] == "đàn ông" and own["cup"] == "ly"
    assert plural("water buffalo") == "water buffaloes" and plural("baby") == "babies" and plural("bus") == "buses"
    assert plural("human") == "humans" and plural("bird of prey") == "birds of prey" and plural("wine glass") == "wine glasses"
    assert all(plural(f) is None for f in ("jeans", "high heels", "flip-flops", "people", "moths and butterflies"))
    assert own["humans"] == "người" and not {"humen", "peoples", "jeanses", "bird of preys"} & set(own)
    assert (root / EN_MAP).read_bytes() == en_map_bytes(root), "en_oiv7_map.json is not the build output"


def _st_proxy(root: Path) -> None:
    rxs = question_rx(root)
    assert len(rxs) == 8 and unicodedata.is_normalized("NFC", (root / REPO_PINS["proxy_regex"][0]).read_text("utf-8"))
    yes = ["Dòng chữ trên biển là gì?", "Tên cửa hàng là gì?", "Biển báo ghi gì?", "Số điện thoại là bao nhiêu?"]
    no = ["Con chó màu gì?", "Có bao nhiêu người?", "Tên của anh ấy là gì?", "Giáo viên đang làm gì?"]
    assert all(is_text_question(q, rxs) for q in yes) and not any(is_text_question(q, rxs) for q in no)
    ex = extract('Biển ghi "Cà Phê" và chữ Mở cửa, số 0912 trên tường. Dòng chữ HỘI AN.')
    assert [x for _, _, x in ex] == ["Cà Phê", "Mở cửa", "0912", "HỘI AN"], ex
    assert [x for _, _, x in extract("A man's hat and the dog's bowl 'X'.")] == ["X"]
    assert norm(unicodedata.normalize("NFD", "  Phở, BÒ!! ")) == "phở bò" and norm("Phở", True) == "pho"
    assert norm("Đường_số 9") == "đường số 9"
    from rapidfuzz.distance import Levenshtein
    for a, b in (("abcd", "abxy"), ("kitten", "sitting"), ("phở", "pho"), ("abcde", "abxyz")):
        assert abs(Levenshtein.normalized_similarity(a, b) - (1 - _lev(a, b) / max(len(a), len(b)))) < 1e-12
    assert classify("ab", ["abc"]) == "near" and classify("abc", ["abcd"]) == "match"
    assert classify("ab", ["ab"]) == "match" and classify("abcd", ["abxy"]) == "near"
    assert classify("abcde", ["abxyz"]) == "uncovered" and classify("pho bo", ["bo kho"]) == "near"
    c = proxy_counts('Biển ghi "Cà Phê" và chữ ZZQQ.', ["cà phê", "phở"])
    assert c == {"match": 1, "near": 0, "uncovered": 1, "n_answers": 2, "answers_found": 1}, c
    assert p_text(c) == 0.5 and p_text(c, 0) == 1.0 and p_text({"match": 0, "near": 0, "uncovered": 0}) is None


def _st_models(root: Path) -> None:
    import types
    calls = {}

    class T(list):
        def tolist(self):
            return list(self)

    class Batch(dict):
        def to(self, *a):
            return self

    class Tok:
        eos_token_id, pad_token_id = 2, 3

        def decode(self, ids, skip_special_tokens):
            return " ".join(map(str, [i for i in ids if i not in (2, 3)]))

    class Proc:
        tokenizer = Tok()

        def __call__(self, **k):
            calls["proc"] = k
            return Batch(input_ids=T([T([9, 8])]))

    class Model:
        device = "cpu"

        def generate(self, **k):
            calls["generate"] = k
            return T([T([9, 8, 5, 6, 2])])

        def eval(self):
            return self

    class GC:
        def __init__(self, **k):
            self.k = k

    def from_pretrained(snap, **k):
        calls["load"] = k
        return Model()

    tr = types.SimpleNamespace(Blip2ForConditionalGeneration=types.SimpleNamespace(from_pretrained=from_pretrained),
                               Blip2Processor=types.SimpleNamespace(from_pretrained=lambda s, **k: Proc()),
                               GenerationConfig=GC)
    th = types.SimpleNamespace(bfloat16="bf16", inference_mode=lambda: open(os.devnull))
    old = {m: sys.modules.get(m) for m in ("transformers", "torch")}
    sys.modules.update(transformers=tr, torch=th)
    try:
        with tempfile.TemporaryDirectory() as td:
            snap = Path(td)
            (snap / "w.safetensors").write_bytes(b"w")
            _must("differs from its pin", load_mblip, snap, {"w.safetensors": "0" * 64})
            model, proc = load_mblip(snap, {"w.safetensors": hashlib.sha256(b"w").hexdigest()})
        assert calls["load"] == {"local_files_only": True, "use_safetensors": True, "torch_dtype": "bf16"}
        for kind, mx in (("caption", 64), ("verify", 8)):
            text, fin = generate(model, proc, "IMG", "prompt", kind)
            g = calls["generate"]["generation_config"].k
            assert text == "5 6" and fin == "eos" and model.generation_config.k == g
            assert g["max_new_tokens"] == mx and g["do_sample"] is False and g["num_beams"] == 1
            assert g["repetition_penalty"] == 1.0 and g["no_repeat_ngram_size"] == 0 and g["length_penalty"] == 1.0
            assert g["temperature"] is None and g["top_k"] is None and g["top_p"] is None
            assert g["num_return_sequences"] == 1 and (g["eos_token_id"], g["pad_token_id"]) == (2, 3)
            assert calls["proc"] == {"images": ["IMG"], "text": ["prompt"], "return_tensors": "pt"}
        Model.generate = lambda self, **k: T([T([5, 6, 7])])  # an output without the prompt echo is kept whole
        assert generate(model, proc, "IMG", "p", "verify") == ("5 6 7", "other")
    finally:
        for m, v in old.items():
            if v is None:
                sys.modules.pop(m, None)
            else:
                sys.modules[m] = v
    _must("EN decode refused", load_llava)


def _st_ovqa() -> None:
    assert blob_hashes.__doc__ and curl_argv("x.json", Path("/t/x.part"))[-1] == (
        "https://huggingface.co/datasets/uitnlp/OpenViVQA-dataset/resolve/"
        "cc85c24c863afb05b5a52f68950f9ba6b69975cf/x.json")
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        e = base / "empty"
        e.write_bytes(b"")
        assert blob_hashes(e)[2] == "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"  # git's empty blob
        e.write_bytes(b"test content\n")
        assert blob_hashes(e)[2] == "d670460b4b4aece5915caf5c68d12f560a9fe3e4"  # Pro Git hash-object example
        sealed = base / "sealed"
        sealed.mkdir()
        data = {"vlsp2023_dev_data.json": {"images": {str(i): f"{i}.jpg" for i in range(1070)},
                                           "annotations": {str(i): {"image_id": i % 1070} for i in range(3545)}},
                "vlsp2023_train_data.json": {"images": {str(i): "x" for i in range(9129)},
                                             "annotations": list(range(30833))},
                "vlsp2023_test_data.json": {"annotations": list(range(14035))}}
        blobs = {k: json.dumps(v).encode() for k, v in data.items()}
        spec = {k: (len(b), hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()) for k, b in blobs.items()}
        bad = {**spec, "vlsp2023_dev_data.json": (spec["vlsp2023_dev_data.json"][0], "0" * 40)}
        dest = base / "ovqa"
        _must("git-blob", ovqa_fetch, dest, sealed, bad, lambda n, p: p.write_bytes(blobs[n]) and 0)
        assert not list(dest.glob("*.part")) and "ovqa-pin FAULT" in (sealed / "ACCESS_LOG.tsv").read_text()
        _must("rc 22", ovqa_fetch, base / "o2", sealed, spec, lambda n, p: 22)
        rec = ovqa_fetch(dest, sealed, spec, lambda n, p: p.write_bytes(blobs[n]) and 0)
        assert set(rec["files"]) == set(spec) and oct(dest.stat().st_mode & 0o777) == "0o700"
        assert all((dest / k).stat().st_mode & 0o777 == 0o400 for k in spec)
        _must("one download", ovqa_fetch, dest, sealed, spec, lambda n, p: 0)
        sk = ovqa_skeleton(dest, sealed)
        assert sk["vlsp2023_dev_data.json"]["keys"]["images"] == {"type": "dict", "len": 1070,
                                                                 "value_types": ["str"]}
        assert "jpg" not in json.dumps(sk)  # no value is printed
        rule = {"vlsp2023_dev_data.json": {"images": "images", "qa": "annotations", "image_names": "values"},
                "vlsp2023_train_data.json": {"images": "images", "qa": "annotations"},
                "vlsp2023_test_data.json": {"images": None, "qa": "annotations"}}
        rp = base / "rule.json"
        rp.write_text(json.dumps(rule))
        _must("LOG line", ovqa_count, dest, sealed, rp, "0" * 64)
        zp = base / "dev-images.zip"
        with zipfile.ZipFile(zp, "w") as z:
            for i in range(1070):
                z.writestr(f"dev-images/{i}.jpg", b"")
        global OVQA_DEV_ZIP
        keep, OVQA_DEV_ZIP = OVQA_DEV_ZIP, blob_hashes(zp)[:2]
        try:
            got = ovqa_count(dest, sealed, rp, sha_file(rp), zp)
        finally:
            OVQA_DEV_ZIP = keep
        assert got == {"vlsp2023_dev_data.json": {"qa": 3545, "images": 1070}, "dev_names_in_zip": 1070,
                       "vlsp2023_train_data.json": {"qa": 30833, "images": 9129},
                       "vlsp2023_test_data.json": {"qa": 14035}}, got
        _must("dev-images.zip differs", ovqa_count, dest, sealed, rp, sha_file(rp), zp)
        rule["vlsp2023_dev_data.json"]["images"] = None
        rp.write_text(json.dumps(rule))
        _must("must name its images", ovqa_count, dest, sealed, rp, sha_file(rp))
        rule["vlsp2023_dev_data.json"]["images"] = "annotations"
        rp.write_text(json.dumps(rule))
        _must("differs from images 1070", ovqa_count, dest, sealed, rp, sha_file(rp))
        _must("must sit on the WSL ext4 home", custody, Path("/mnt/c_pvr_selftest_never/x"))


def selftest(root: Path) -> None:
    import urllib.request

    def no_net(*a, **k):
        raise OSError("selftest: network disabled")

    socket.socket, socket.create_connection = no_net, no_net  # type: ignore[assignment,misc]
    try:
        urllib.request.urlopen("http://example.invalid/", timeout=1)
    except OSError as e:
        assert "selftest: network disabled" in str(e), e
    else:
        raise AssertionError("a socket opened")
    P = prompts(root)
    with tempfile.TemporaryDirectory() as td:  # a changed byte in a prompt file or the segmenter files is a FAULT
        t = Path(td)
        (t / "scripts/c_pvr/prompts").mkdir(parents=True)
        for name, text in P.items():
            (t / "scripts/c_pvr/prompts" / name).write_text(text + ("." if name == "ver_3way.txt" else ""), "utf-8")
        _must("prompt ver_3way.txt differs", prompts, t)
        for rel in VNC_PINS:
            (t / rel).parent.mkdir(parents=True, exist_ok=True)
            (t / rel).write_bytes(b"x" if rel.endswith(".rdr") else (VNC_DIR / rel).read_bytes())
        _must("wordsegmenter.rdr differs", rdr, ["x"], t)
    _st_text(P)
    _st_verify()
    _st_arms()
    _st_rebuild()
    _st_en_map(root)
    _st_proxy(root)
    _st_decompose(root, VNC_DIR, spacy_nlp())
    _st_models(root)
    _st_ovqa()
    g = ast.parse((root / "scripts/c_pvr/gates.py").read_text("utf-8"))
    url = [n.value.value for n in g.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") ==
           "OI_TEST_URL"]
    assert url == [OI_TEST_URL], url
    for p in ("data/oidv7-test-annotations-human-imagelabels.csv", "/dev/shm/c_pvr_gb/x",
              "x/nocaps_val_4500_captions.json"):
        _must("REFUSED", refuse, p)
    import rapidfuzz
    assert rapidfuzz.__version__ == LIB_VERSIONS["rapidfuzz"], rapidfuzz.__version__
    mods = sorted((m.__name__, sha_file(Path(m.__file__))[:8]) for m in list(sys.modules.values())
                  if m.__name__.split(".")[0] == "rescap" and getattr(m, "__file__", None))
    print("rescap import closure (sha256[:8]):", " ".join(f"{n}={s}" for n, s in mods))
    print(f"selftest ok  {LABEL}  c_pvr.py {sha_file(Path(__file__))}")


# ---------------------------------------------------------------------------------------------- cli
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=ROOT, help="repo root (the mutant harness runs copies)")
    sp = ap.add_subparsers(dest="cmd", required=True)
    for c in ("selftest", "header"):
        sp.add_parser(c).add_argument("--root", type=Path, default=argparse.SUPPRESS)
    e = sp.add_parser("en-map")
    e.add_argument("--write", action="store_true")
    d = sp.add_parser("decompose")
    d.add_argument("--lang", choices=("vi", "en"), required=True)
    d.add_argument("--root", type=Path, default=argparse.SUPPRESS)
    o = sp.add_parser("ovqa-pin")
    o.add_argument("phase", choices=("fetch", "skeleton", "count"))
    o.add_argument("--rule", type=Path)
    o.add_argument("--rule-sha")
    o.add_argument("--dev-zip", type=Path)
    x = ap.parse_args()
    root = x.root.resolve()
    if x.cmd == "selftest":
        return selftest(root)
    if x.cmd == "header":
        return print(json.dumps(header(root), indent=1, sort_keys=True, ensure_ascii=False))
    if x.cmd == "en-map":
        b = en_map_bytes(root)
        if x.write:
            (root / EN_MAP).write_bytes(b)
        return print(hashlib.sha256(b).hexdigest(), EN_MAP)
    if x.cmd == "decompose":
        fn = decompose_vi if x.lang == "vi" else decompose_en
        return sys.stdout.write(json.dumps(fn(json.load(sys.stdin), root), sort_keys=True, ensure_ascii=False))
    if str(SEALED.resolve()).startswith("/mnt/"):
        fault(f"{SEALED} must sit on the WSL ext4 home")
    dest = SEALED / "ovqa"
    if x.phase == "fetch":
        SEALED.mkdir(mode=0o700, parents=True, exist_ok=True)
        print(json.dumps(ovqa_fetch(dest, SEALED), indent=1, sort_keys=True))
    elif x.phase == "skeleton":
        print(json.dumps(ovqa_skeleton(dest, SEALED), indent=1, sort_keys=True))
    else:
        if not (x.rule and x.rule_sha):
            ap.error("count needs --rule and --rule-sha (the sha in the counting-rule LOG line)")
        print(json.dumps(ovqa_count(dest, SEALED, x.rule, x.rule_sha, x.dev_zip), indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
