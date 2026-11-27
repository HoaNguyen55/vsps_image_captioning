"""DRY-N3D bundle generator (CC-511e6 ruling 4 (a), (b)). SYNTHETIC ONLY; laptop, ext4.

Reads only STRUCTURE from the real pinned inputs (data.tar of the N3D stage, every member sha-checked against
PUSH_LIST.sha256 / DATA_PINS): file names, JSON keys, spec dicts, run_id, id sets and their order, per-image list
lengths, the exemplar id lists, the reference counts per image, the CSV columns and split/filename/id rows, and the
list files themselves (ids only, copied unchanged). Every caption string is replaced by a seeded synthetic string;
nothing read from a caption, prediction or score is written or printed (only counts go to READ_RECORD.json).

  python -I -B make_bundle.py build --code C --closure K --data-tar D --vnc-tar V --out B
  python -I -B make_bundle.py scan --data-tar D --out B     counts-only 6/8-gram check, bundle vs the real captions
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import random
import re
import shutil
import sys
import tarfile
import unicodedata
from pathlib import Path

SEED = 20261127
# separators: a synthetic token opens, closes and cuts every caption into chunks of <= 5 words, so no 6-gram of a
# synthetic caption can be free of a token that no real caption holds (ruling 4 (b))
SEPS = ["qzx" + str(i) for i in range(10)]
VI_CLS = ["chó", "mèo", "chim", "ngựa",
          "voi", "khỉ", "xe đạp",
          "xe máy", "ô tô",
          "xe buýt", "xe tải",
          "thuyền", "máy bay",
          "ghế", "túi", "mũ", "giày",
          "điện thoại", "bát", "ly",
          "nhà", "cây", "hoa", "núi",
          "sông", "áo", "quần", "sách",
          "dao", "đĩa"]
VI_FILL = ["một", "hai", "đang", "đứng",
           "ngồi", "màu", "đỏ", "xanh",
           "trắng", "lớn", "nhỏ", "đẹp",
           "rất", "nhiều", "những", "ở",
           "phía", "bên", "trái", "phải"]
EN_CLS = ["dog", "cat", "horse", "cow", "sheep",
          "bird", "elephant", "bear", "zebra",
          "giraffe", "car", "bus", "truck",
          "boat", "train", "bicycle", "airplane",
          "umbrella", "bench", "chair", "cup",
          "bottle", "clock", "book", "pizza"]
EN_FILL = ["a", "the", "on", "with",
           "near", "small", "big", "red",
           "white", "standing", "sitting", "of",
           "two", "old", "young", "green"]
COPY_KEYS = {"schema", "c_schema", "run_id", "spec", "model", "dataset", "lang", "exemplars"}
SRC = {"ov_dev_b": "openviic", "xm_dev500": "xm3600"}
OUT_DIRS = ("/outputs/c_attr_b1/out/", "/outputs/c_stage2/runs/", "/outputs/c_t1/out/")
TOK = re.compile(r"\w+")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def caption(rng: random.Random, fill: list, classes: list, n_chunks: int) -> str:
    """Chunks of 2-5 words (a class phrase plus filler), each chunk between two separator tokens."""
    cls, chunks = list(classes), []
    while len(chunks) < n_chunks or cls:
        t = cls.pop().split() if cls else []
        want = rng.randint(max(2, len(t)), 5)
        while len(t) < want:
            t.append(rng.choice(fill))
        chunks.append(" ".join(t[:5]))
    out = [rng.choice(SEPS)]
    for c in chunks:
        out += [c, rng.choice(SEPS)]
    return " ".join(out)


def blank(x):
    """Same type and shape, no content (keys kept): the fields H.run never reads."""
    if isinstance(x, dict):
        return {k: blank(v) for k, v in x.items()}
    if isinstance(x, list):
        return [blank(v) for v in x]
    if isinstance(x, bool):
        return False
    if isinstance(x, int):
        return 0
    if isinstance(x, float):
        return 0.0
    if isinstance(x, str):
        return "synthetic"
    return x


class Real:
    """The real data.tar, read member by member, each member sha-checked against its pin; a record of what was read."""

    def __init__(self, tar: Path, push: dict, data_pins: dict):
        self.t, self.rec = tarfile.open(tar), {}
        self.pins = {f"root/{p}": h for p, h in push.items()} | {f"ncs-data/{p}": h for p, h in data_pins.items()}

    def raw(self, name: str) -> bytes:
        b = self.t.extractfile(name).read()
        if sha_bytes(b) != self.pins[name]:
            raise SystemExit(f"STOP: {name} is not as pinned")
        return b

    def json(self, name: str, note: dict):
        self.rec[name] = {"sha256": self.pins[name], **note}
        return json.loads(self.raw(name))

    def names(self) -> list[str]:
        return [m.name for m in self.t.getmembers() if m.isfile()]


def load_modules(code: Path, closure: Path):
    sys.path.insert(0, str(code))
    import c_n3d_host as H
    H.paths(closure)
    import decode_icl as C
    import guard as G
    import score_coco_probe as SC
    return H, C, G, SC


def check_vocab(G, SC) -> dict:
    """>= 20 matcher classes per language; no filler or separator is a class (ruling 4 (a))."""
    syn = SC.load_synonyms()
    vi = {G.key(o) for w in VI_CLS for o in G.classes(w)}
    en = {o for w in EN_CLS for o in SC.en_classes(w, syn)}
    bad = [w for w in VI_FILL + SEPS if G.classes(w)] + [w for w in EN_FILL + SEPS if SC.en_classes(w, syn)]
    if len(vi) < 20 or len(en) < 20 or bad:
        raise SystemExit(f"STOP: vocabulary: vi {len(vi)} en {len(en)} non-class hits {bad}")
    return {"vi_matcher_classes": len(vi), "en_matcher_classes": len(en)}


def write(path: Path, data: bytes) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return sha_bytes(data)


def dumps(x) -> bytes:
    return json.dumps(x, ensure_ascii=False).encode("utf-8")


def build(a) -> None:
    out = Path(a.out)
    if out.exists():
        raise SystemExit(f"REFUSED: {out} exists")
    H, C, G, SC = load_modules(Path(a.code), Path(a.closure))
    push = H.N.push_list(H.PUSH)
    real = Real(Path(a.data_tar), push, dict(H.DATA_PINS))
    rng = random.Random(SEED)
    rec = {"vocabulary": check_vocab(G, SC)}
    root, data = out / "root", out / "ncs-data"
    new_push, new_pins = dict(push), dict(H.DATA_PINS)

    # 1. code closure (git archive e9a5898 + the untracked OIV7 class CSV), unchanged, sha-checked against PUSH_LIST
    for p in Path(a.closure).rglob("*"):
        if p.is_file():
            rel = p.relative_to(a.closure).as_posix()
            if push.get(rel) != write(root / rel, p.read_bytes()):
                raise SystemExit(f"STOP: closure file {rel} not as pinned")
    with tarfile.open(a.vnc_tar) as v:
        v.extractall(out, filter="data")
    if sha_bytes((data / H.JAR[0]).read_bytes()) != H.JAR[1]:
        raise SystemExit("STOP: jar")

    # 2. list files and other non-caption root files: copied unchanged (ids only)
    preds = []
    for n in real.names():
        if not n.startswith("root/"):
            continue
        if n.endswith(".preds.json") and any(d in n for d in OUT_DIRS):
            preds.append(n)
            continue
        b = real.raw(n)
        write(out / n, b)
        real.rec[n] = {"sha256": real.pins[n], "copied_unchanged": True, "bytes": len(b)}
    lists = json.loads((root / H.LISTS[0]).read_text(encoding="utf-8"))
    f30k = json.loads((root / H.F30K_LISTS[0]).read_text(encoding="utf-8"))

    # 3. memory sources (KTVIC train, OpenViIC train): ids and counts kept, captions synthetic
    kt = real.json("ncs-data/datasets/ktvic/train_data.json", {"keys": ["images", "annotations"]})
    for an in kt["annotations"]:
        an["caption"] = caption(rng, VI_FILL, rng.sample(VI_CLS, rng.randint(1, 3)), rng.randint(1, 3))
        an["segment_caption"] = an["caption"]
    kt["images"] = [{"id": i["id"], "filename": i["filename"]} for i in kt["images"]]
    real.rec["ncs-data/datasets/ktvic/train_data.json"].update(n_images=len(kt["images"]), n_ann=len(kt["annotations"]))
    ovt = real.json("ncs-data/datasets/openviic/uit-openviic-annotation-train.json", {"keys": "file name -> captions"})
    for k, v in ovt.items():
        ovt[k] = {"captions": [caption(rng, VI_FILL, rng.sample(VI_CLS, rng.randint(1, 3)), rng.randint(1, 3))
                               for _ in v["captions"]]}
    real.rec["ncs-data/datasets/openviic/uit-openviic-annotation-train.json"].update(
        n_keys=len(ovt), n_captions=sum(len(v["captions"]) for v in ovt.values()))
    for rel, obj in (("datasets/ktvic/train_data.json", kt), ("datasets/openviic/uit-openviic-annotation-train.json", ovt)):
        new_pins[rel] = write(data / rel, dumps(obj))
    del kt, ovt
    caps = C.memory_captions(lists, data)          # the closure's own code builds the shown captions (synthetic)

    # 4. Vietnamese references: per image 3 gold classes; counts as found
    gold = {}
    ovd = real.json("ncs-data/datasets/openviic/uit-openviic-annotation-dev.json", {"keys": "file name -> captions"})
    for k, v in ovd.items():
        g = gold[k] = rng.sample(VI_CLS, 3)
        ovd[k] = {"captions": [caption(rng, VI_FILL, rng.sample(g, rng.randint(1, 2)), rng.randint(2, 4))
                               for _ in v["captions"]]}
    real.rec["ncs-data/datasets/openviic/uit-openviic-annotation-dev.json"].update(
        n_keys=len(ovd), n_captions=sum(len(v["captions"]) for v in ovd.values()))
    xm = real.json("ncs-data/datasets/c_xm_dev500/xm_dev500_data.json", {"keys": ["images", "annotations"]})
    xm["images"] = [{"id": i["id"], "filename": i["filename"]} for i in xm["images"]]
    for i in xm["images"]:
        gold[i["id"]] = rng.sample(VI_CLS, 3)
    xm["annotations"] = [{"id": an["id"], "image_id": an["image_id"],
                          "caption": caption(rng, VI_FILL, rng.sample(gold[an["image_id"]], rng.randint(1, 2)),
                                             rng.randint(2, 4))} for an in xm["annotations"]]
    real.rec["ncs-data/datasets/c_xm_dev500/xm_dev500_data.json"].update(n_images=len(xm["images"]),
                                                                       n_ann=len(xm["annotations"]))
    refs = {k: v["captions"] for k, v in ovd.items()}
    for an in xm["annotations"]:
        refs.setdefault(an["image_id"], []).append(an["caption"])
    new_pins["datasets/openviic/uit-openviic-annotation-dev.json"] = write(
        data / "datasets/openviic/uit-openviic-annotation-dev.json", dumps(ovd))
    new_pins["datasets/c_xm_dev500/xm_dev500_data.json"] = write(data / "datasets/c_xm_dev500/xm_dev500_data.json",
                                                                 dumps(xm))

    # 5. Flickr30K CSV: columns and split/filename/id rows kept; raw = as many synthetic captions as found
    f = io.TextIOWrapper(real.t.extractfile("ncs-data/" + H.F30K_CSV[0]), encoding="utf-8", newline="")
    real.raw("ncs-data/" + H.F30K_CSV[0])          # pin check of the member
    rd = csv.DictReader(f)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=rd.fieldnames, lineterminator="\n")
    w.writeheader()
    n_rows, en_gold = 0, {}
    for r in rd:
        g = en_gold[r["filename"]] = rng.sample(EN_CLS, 3)
        r["raw"] = json.dumps([caption(rng, EN_FILL, rng.sample(g, rng.randint(1, 2)), rng.randint(2, 4))
                               for _ in json.loads(r["raw"])])
        w.writerow(r)
        n_rows += 1
    real.rec["ncs-data/" + H.F30K_CSV[0]] = {"sha256": H.F30K_CSV[1], "columns": rd.fieldnames, "rows": n_rows}
    new_pins[H.F30K_CSV[0]] = write(data / H.F30K_CSV[0], buf.getvalue().encode("utf-8"))
    en_refs = {}
    for r in csv.DictReader(io.StringIO(buf.getvalue())):
        if r["split"] == "train" and r["filename"] in set(f30k["carve"]):
            en_refs[r["filename"]] = json.loads(r["raw"])

    # 6. decode files: keys kept; spec, run_id, ids, exemplar lists copied; predictions synthetic; the rest blanked
    for n in sorted(preds):
        r = real.json(n, {})
        ids = list(r["predictions"])
        s = r.get("dataset")
        en = "/c_t1/" in n
        new = {}
        for i in ids:
            g = en_gold[i] if en else gold[i]
            fill, pool = (EN_FILL, EN_CLS) if en else (VI_FILL, VI_CLS)
            if r["spec"]["arm"] == "zs":
                new[i] = caption(rng, fill, rng.sample(g, 2) + rng.sample(pool, 1), rng.randint(2, 4))
                continue
            shown = [] if en else [C.shown(caps[x], SRC[s]) for x in r["exemplars"][i]]
            u = rng.random()
            if u < 0.30:
                new[i] = rng.choice(en_refs[i] if en else refs[i])                  # near-reference: |d| large
            elif u < 0.42 and shown:
                new[i] = shown[0]                                                     # a copy: CP
            else:
                cls = rng.sample(g, rng.randint(0, 2)) + rng.sample(pool, 1)
                if shown:                                                             # a shown-only class: BO
                    cls += [o for o in G.classes(rng.choice(shown)) if G.key(o) not in {G.key(x) for x in g}][:1]
                new[i] = caption(rng, fill, cls, rng.choice((1, 2, 3, 5, 7)))         # lengths vary: LN; a dropped zs class: ZL
        body = {}
        for k, v in r.items():
            body[k] = v if k in COPY_KEYS else new if k == "predictions" else blank(v)
        if "label" in body:
            body["label"] = "SYNTHETIC DRY-N3D bundle (CC-511e6 ruling 4)"
        real.rec[n].update(keys=list(r), n_ids=len(ids), arm=r["spec"]["arm"],
                           exemplar_lens=sorted({len(x) for x in r.get("exemplars", {}).values()}))
        new_push[n[len("root/"):]] = write(out / n, dumps(body))

    # 7. pins of the bundle, marker, read record
    (out / "PUSH_LIST.sha256").write_text(
        "# DRY-N3D SYNTHETIC push list: the real paths; synthetic shas for the rewritten files\n"
        + "".join(f"{h}  {p}\n" for p, h in new_push.items()), encoding="utf-8")
    (out / "DATA_PINS.json").write_text(json.dumps(new_pins, indent=1) + "\n", encoding="utf-8")
    (out / "SYNTHETIC").write_text("DRY-N3D synthetic bundle; no real caption, prediction or score (CC-511e6 4(a))\n")
    changed = sorted(p for p in push if new_push[p] != push[p])
    rec.update(seed=SEED, files_read=real.rec, push_rewritten=changed, n_push=len(new_push),
               data_pins_rewritten=sorted(k for k in new_pins if new_pins[k] != H.DATA_PINS[k]))
    (out / "READ_RECORD.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"bundle written: {len(new_push)} push entries, {len(changed)} rewritten; read record READ_RECORD.json")


# ------------------------------------------------------------------------------------------------ scan (4 (b))
def toks(s: str) -> list[str]:
    return TOK.findall(unicodedata.normalize("NFC", s).lower())


def captions(n: str, x) -> list[str]:
    """The caption strings of one file: predictions, references, memory captions, the CSV raw lists."""
    if n.endswith(".preds.json"):
        return list(x["predictions"].values())
    if isinstance(x, list):                                       # one CSV raw list
        return x
    if "annotations" in x:
        return [an[k] for an in x["annotations"] for k in ("caption", "segment_caption") if k in an]
    return [c for v in x.values() for c in v["captions"]]


def other_strings(x, key="", depth=0):
    """(top-level key, string) of the non-caption fields of a decode file (copied structure or blanked)."""
    if isinstance(x, str):
        yield key, x
    elif isinstance(x, dict):
        for k, v in x.items():
            if not (depth == 0 and k == "predictions"):
                yield from other_strings(v, k if depth == 0 else key, depth + 1)
    elif isinstance(x, list):
        for v in x:
            yield from other_strings(v, key, depth + 1)


def grams(t: list, n: int) -> set:
    return {tuple(t[i:i + n]) for i in range(len(t) - n + 1)}


def caption_strings(tree: Path | tarfile.TarFile, names: list[str]):
    """Every string of the caption-bearing files (decode files, references, memory sources, the CSV raw lists)."""
    for n in names:
        b = tree.extractfile(n).read() if isinstance(tree, tarfile.TarFile) else (tree / n).read_bytes()
        if n.endswith(".csv"):
            for r in csv.DictReader(io.StringIO(b.decode("utf-8"))):
                yield n, json.loads(r["raw"])
        else:
            yield n, json.loads(b)


def scan(a) -> None:
    """Counts only: shared 6/8-grams between the bundle's caption strings and the real ones (every caption-bearing
    file); one real caption of >= 8 tokens per source must hit itself (positive control). The non-caption strings
    of the decode files (copied run_id/spec/ids, blanked fields) are counted apart, by top-level key."""
    t = tarfile.open(a.data_tar)
    names = [m.name for m in t.getmembers() if m.isfile() and (m.name.startswith("ncs-data/") and
             (m.name.endswith(".json") or m.name.endswith(".csv")) or m.name.endswith(".preds.json"))]
    real, other_real = {6: set(), 8: set()}, {6: set(), 8: set()}
    controls = {}
    for n, x in caption_strings(t, names):
        for s in captions(n, x):
            tk = toks(s)
            if len(tk) >= 8 and n not in controls:
                controls[n] = tk
            for k in real:
                real[k] |= grams(tk, k)
        if n.endswith(".preds.json"):
            for _k, s in other_strings(x):
                for k in other_real:
                    other_real[k] |= grams(toks(s), k)
    ctl = {n: (len(grams(c, 8) & real[8]) > 0) and (len(grams(c, 6) & real[6]) > 0) for n, c in controls.items()}
    print(f"real sources {len(names)}; positive controls hit: {sum(ctl.values())}/{len(names)}")
    bad = sum(not v for v in ctl.values()) + (len(controls) != len(names))
    anyreal = {k: real[k] | other_real[k] for k in real}
    tot, n_str, other = {6: 0, 8: 0}, 0, {}
    for n, x in caption_strings(Path(a.out), names):
        for s in captions(n, x):
            tk = toks(s)
            n_str += 1
            for k in tot:
                tot[k] += len(grams(tk, k) & anyreal[k])
        if n.endswith(".preds.json"):
            for key, s in other_strings(x):
                h = len(grams(toks(s), 6) & anyreal[6])
                if h:
                    other[key] = other.get(key, 0) + h
    print(f"bundle caption strings {n_str}; shared with any real string: 8-grams {tot[8]}, 6-grams {tot[6]}")
    print(f"non-caption decode-file strings sharing 6-grams, by top-level key (copied structure): {other}")
    bad += tot[6] + tot[8] + sum(v for k, v in other.items() if k not in COPY_KEYS)
    print("BUNDLE SCAN", "FAIL" if bad else "PASS")
    sys.exit(1 if bad else 0)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    for k in ("code", "closure", "data-tar", "vnc-tar", "out"):
        b.add_argument(f"--{k}", required=True)
    s = sub.add_parser("scan")
    for k in ("data-tar", "out"):
        s.add_argument(f"--{k}", required=True)
    a = ap.parse_args()
    build(a) if a.cmd == "build" else scan(a)


if __name__ == "__main__":
    main()
