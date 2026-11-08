#!/usr/bin/env python3
"""B-PA1-T1 laptop interlude 2 (v3.1 §6.1 B1b, §6.3, §6.4 steps 4-5, §8.4; B_RUN_DOC §11.2). TIER 1 / DEV-EXPLORE.
DRAFT, not read. /usr/bin/python3 3.12.3 (the R3 interpreter), stdlib + repo + java (R7 VnCoreNLP), laptop only.

    python3 -I -B scripts/b_pa1/b_pa1_mid.py selftest
    ... coverage --pulled P --map M --categories C --out-dir D   (i) tokens in >= 10 slice-A captions not covered by
        a map term or the R7 stop list; (ii) Objects365 classes with no map row. Counts on stdout; lists in D only
    ... amend --coverage D/coverage.json --map M --categories C --entries E --log L   add-only, one UTC line each
    ... final --map M --categories C --log L --out-dir D2         final map = map v1 + the logged additions (O_EXCL)
    ... parity2 --map D2/b_pa1_map_final.json                     run 2 on the final map (once; logged start)
    ... htrans --pulled P --lists b_pa1_lists.json --frame F --out H   block-H input: 231 gate captions x 6 transforms

P = the pulled ~/b_pa1_out of HB-T1: only out/s/ACCEPT.json and the four out/a1decode/captions_<accepted>.jsonl are
read, each checked against the host's SHA256SUMS_s / SHA256SUMS_a1decode; never A4 captions, any A1-score output, a
reference, a box or gold (B1b). Coverage is computed from caption text and class names only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import unicodedata
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import b_pa1 as B  # noqa: E402
import b_pa1_gpu as G  # noqa: E402  scratch (selftest temp dirs, no recursive delete)
import map_v1 as MV  # noqa: E402  parity, load_inputs, r3, at, record fields, REFS, GOLD, R7, canon, sha
import score_coco_probe as sc  # noqa: E402  norm_tone, vi_classes

ROOT = B.K.ROOT
FINAL_NAME, COV_NAME, MIN_DF, GATE_N = "b_pa1_map_final.json", "coverage.json", 10, 231
VNC = ROOT / ".session_backup/machines/n2/ncs-data/vncorenlp"
STOP = MV.R7[3]
JAVA = ["java", "-Xmx700m", "-XX:+UseSerialGC", "-XX:ActiveProcessorCount=1", "-jar", "VnCoreNLP-1.2.jar",
        "-fin", "/dev/stdin", "-fout", "/dev/stdout", "-annotators", "wseg"]  # = c_pvr.JAVA
MARK = "XQXQBPA1MARKXQXQ"
_OPS = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z OPS-[0-9A-Za-z-]+-"
START2, DONE2 = re.compile(_OPS + "parity2-start: "), re.compile(_OPS + "parity2-done: ")
TRANSFORMS = ("punct", "nfd", "tone", "seg", "case", "ws")  # v3.1 §8.4, v3 §3.6 (definitions: reading 14)
LETTER = re.compile(r"[^\W\d_]")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def norm(w: str) -> str:
    """One form for map terms, tokens and stop words: NFC, lower case, underscores as spaces, rescap tone norm."""
    return sc.norm_tone(unicodedata.normalize("NFC", w).replace("_", " ").lower()).strip()


def outside_tree(d: Path, root: Path = ROOT) -> Path:
    d = d.resolve()
    if root.resolve() in d.parents and (root / ".session_backup").resolve() not in d.parents:
        raise SystemExit("REFUSED: output inside the tracked tree")
    return d


# ---------------------------------------------------------------------------------------------- inputs
def pulled_captions(p: Path) -> tuple[list[str], dict[str, list[dict]]]:
    """ACCEPT.json and the 4 accepted captioners' A1-decode files, each sha-checked against the host's SUMS."""
    def sums(name):
        return dict((ln[66:], ln[:64]) for ln in (p / name).read_text().splitlines())
    s_sums, d_sums = sums("SHA256SUMS_s"), sums("SHA256SUMS_a1decode")
    acc_b = (p / "out/s/ACCEPT.json").read_bytes()
    if s_sums.get("out/s/ACCEPT.json") != sha(acc_b):
        raise SystemExit("REFUSED: ACCEPT.json differs from SHA256SUMS_s")
    acc = json.loads(acc_b)["accepted"]
    if len(acc) != 4 or len(set(acc)) != 4:
        raise SystemExit("REFUSED: ACCEPT.json does not name 4 captioners")
    want = {f"out/a1decode/captions_{k}.jsonl" for k in acc}
    if set(d_sums) != want:
        raise SystemExit("REFUSED: SHA256SUMS_a1decode lists other files than the 4 accepted captioners' captions")
    caps = {}
    for k in acc:
        rel = f"out/a1decode/captions_{k}.jsonl"
        b = (p / rel).read_bytes()
        if sha(b) != d_sums[rel]:
            raise SystemExit(f"REFUSED: {rel} differs from SHA256SUMS_a1decode")
        caps[k] = [json.loads(x) for x in b.decode().splitlines()]
        if any(r.get("cap") != k for r in caps[k]) or len({r["id"] for r in caps[k]}) != len(caps[k]):
            raise SystemExit(f"REFUSED: {rel} rows are not one per id of {k}")
    return acc, caps


def frozen_map(mp_p: Path, log: Path) -> tuple[dict, bytes, dict, bytes]:
    """Map v1 at its freeze pin (LOG l.1334 form: map sha, map name, crosswalk name and sha on one pin line)."""
    mb, xb = mp_p.read_bytes(), (mp_p.parent / MV.XW_NAME).read_bytes()
    mp = json.loads(mb)
    if mp_p.name != MV.MAP_NAME or mp.get("crosswalk_sha256") != sha(xb) or \
            not B.pin_line(log, sha(mb), MV.MAP_NAME, MV.XW_NAME, sha(xb)):
        raise SystemExit("REFUSED: not the frozen map v1 with its crosswalk (freeze pin line)")
    return mp, mb, json.loads(xb), xb


def categories(c: Path, log: Path, mp: dict) -> dict[int, str]:
    b = c.read_bytes()
    if c.name != MV.CAT_NAME or sha(b) != mp["categories_sha256"] or not B.pin_line(log, sha(b), MV.CAT_NAME):
        raise SystemExit("REFUSED: not the R6-pinned class list map v1 was built from")
    return {x["id"]: x["name"] for x in json.loads(b)["categories"]}


def r7_files(mp: dict, root: Path = ROOT) -> None:
    for rel, s in mp["r7"].items():
        if B.K.sha_file(root / rel) != s:
            raise SystemExit(f"REFUSED: R7 file {Path(rel).name} differs from map v1's pin")


# ---------------------------------------------------------------------------------------------- R7 segmenter
def rdr(texts: list[str], vnc: Path = VNC, run=subprocess.run) -> list[list[str]]:
    """VnCoreNLP-1.2 RDRSegmenter over one pipe, a marker line between texts (as c_pvr.rdr)."""
    out = run(JAVA, input=f"\n{MARK}\n".join(texts) + "\n", capture_output=True, text=True, cwd=vnc, check=True).stdout
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
        raise SystemExit(f"FAULT: RDR alignment lost ({len(segs)} != {len(texts)})")
    return segs


def coverage(caps: dict, segs: list[list[str]], terms: set[str], stop: set[str]) -> Counter:
    """Document frequency over captions of each uncovered letter-bearing token (distinct per caption)."""
    df = Counter()
    for toks in segs:
        df.update({t for t in map(norm, toks) if LETTER.search(t) and t not in terms and t not in stop})
    return df


def listed(df: Counter) -> list[tuple[str, int]]:
    return sorted((t, n) for t, n in df.items() if n >= MIN_DF)


def cmd_coverage(a, log: Path = B.LOG, root: Path = ROOT, seg=rdr) -> int:
    out = outside_tree(a.out_dir, root)
    mp, mb, _, _ = frozen_map(a.map, log)
    names = categories(a.categories, log, mp)
    r7_files(mp, root)
    texts, tok_i = [], []
    if a.pulled:  # without --pulled: the (ii) list alone, from map v1 and the class list (D-8: drafted pre-rental)
        _, caps = pulled_captions(a.pulled)
        texts = [r["caption"] for rows in caps.values() for r in rows]
        stop = {norm(w) for w in (root / STOP).read_text(encoding="utf-8").splitlines() if w.strip()}
        terms = {norm(t["vi"]) for t in mp["terms"]}
        tok_i = listed(coverage(caps, seg(texts), terms, stop))
    mapped = {r["o365_id"] for r in mp["rows"]}
    cls_ii = sorted((i, n) for i, n in names.items() if i not in mapped)
    doc = MV.canon({"schema": "vsps.b_pa1.coverage.v1", "tier": B.LABEL, "map_sha256": sha(mb), "min_df": MIN_DF,
                    "classes_only": not a.pulled,
                    "n_captions": len(texts), "tokens_i": [{"token": t, "df": n} for t, n in tok_i],
                    "classes_ii": [{"o365_id": i, "name": n} for i, n in cls_ii],
                    "code_sha256": B.K.sha_file(Path(__file__))})
    out.mkdir()
    B.write_new(out / COV_NAME, doc)
    print(json.dumps({"tier": B.LABEL, "n_captions": len(texts), "tokens_i": len(tok_i), "classes_ii": len(cls_ii),
                      "sha256": sha(doc)}))
    return 0


# ---------------------------------------------------------------------------------------------- amendments
LOG_RE = re.compile(r"^(\S+) ADD src=(i|ii) tag=(dictionary|instrument) o365_id=(\d+) entries=([0-9a-f]{64}) "
                    r"drafter=(\S+) vi=(.+)$")
INSTRUMENT_MODE = "agent-drafted, amendment-logged"  # PI-1108e Q2 (a); b_pa1_registry.json instrument_llm.mode
DRAFTER_RE = re.compile(r"[A-Za-z0-9._:+-]{1,80}")


def log_rows(p: Path) -> list[dict]:
    if not p.exists():
        return []
    rows = []
    for ln in p.read_text(encoding="utf-8").splitlines():
        m = LOG_RE.fullmatch(ln)
        if not m:
            raise SystemExit("REFUSED: a line of the amendments log is not an ADD line")
        rows.append({"utc": m[1], "src": m[2], "tag": m[3], "o365_id": int(m[4]), "entries": m[5],
                     "drafter": m[6], "vi": json.loads(m[7])})
    return rows


def amendment_ok(doc: dict, reg: dict, log: Path) -> bool:
    """PI-1108e Q2 (a): instrument entries only in the registry's agent-drafted, amendment-logged mode, and only from
    an entries file whose provenance names the amendment file and its sha, on a LOG pin line."""
    am = (doc.get("provenance") or {}).get("amendment")
    return reg["instrument_llm"].get("mode") == INSTRUMENT_MODE and isinstance(am, dict) and \
        bool(B.pin_line(log, str(am.get("sha256", "")), str(am.get("name", ""))))


def check_entries(doc: dict, cov: dict, mp: dict, names: dict, logged: list[dict], inst_ok: bool = False) -> list[dict]:
    """Add-only (v3.1 §6.1): a new term for an (i) token, or a Vietnamese term for an (ii) class, pointing to an
    existing class; never an existing term, never a second logging of a pair. An instrument entry names its drafter
    and needs inst_ok (amendment_ok)."""
    who = doc.get("provenance")
    if not isinstance(who, dict) or not all(str(who.get(f, "")).strip() for f in ("drafter", "utc")):
        raise SystemExit("REFUSED: entries file has no provenance (drafter, utc)")
    ids = {v: k for k, v in names.items()}
    tok_i = {x["token"] for x in cov["tokens_i"]}
    cls_ii = {x["o365_id"] for x in cov["classes_ii"]}
    terms = {norm(t["vi"]) for t in mp["terms"]} | {norm(r["vi"]) for r in logged}
    seen, out = set(), []
    for e in doc["entries"]:
        if e.get("tag") not in ("dictionary", "instrument") or e.get("src") not in ("i", "ii") or \
                not str(e.get("why", "")).strip() or not str(e.get("vi", "")).strip():
            raise SystemExit("REFUSED: an entry needs vi, src i|ii, tag dictionary|instrument and a reason")
        if e.get("o365") not in ids:
            raise SystemExit("REFUSED: an entry names a class that is not in the pinned class list")
        v, cid = norm(e["vi"]), ids[e["o365"]]
        if e["src"] == "i" and v not in tok_i:
            raise SystemExit("REFUSED: an (i) entry's term is not a listed (i) token")
        if e["src"] == "ii" and cid not in cls_ii:
            raise SystemExit("REFUSED: an (ii) entry's class is not a listed (ii) class")
        if v in terms or v in seen:
            raise SystemExit("REFUSED: the term already exists in the map or the log (add-only)")
        if e["tag"] == "instrument" and not inst_ok:
            raise SystemExit("REFUSED: an instrument entry needs the registry's agent-drafted mode and a LOG-pinned "
                             "amendment named in the provenance (PI-1108e)")
        if e["tag"] == "instrument" and not DRAFTER_RE.fullmatch(str(e.get("drafter", ""))):
            raise SystemExit("REFUSED: an instrument entry names no drafter id")
        seen.add(v)
        out.append({"src": e["src"], "tag": e["tag"], "o365_id": cid, "vi": v,
                    "drafter": e["drafter"] if e["tag"] == "instrument" else "-"})
    return out


def cmd_amend(a, log: Path = B.LOG, reg_p: Path = HERE / "b_pa1_registry.json") -> int:
    mp, mb, _, _ = frozen_map(a.map, log)
    names = categories(a.categories, log, mp)
    cov_b, ent_b = a.coverage.read_bytes(), a.entries.read_bytes()
    if not B.pin_line(log, sha(ent_b), a.entries.name):
        raise SystemExit("REFUSED: the entries file's sha is not on a LOG pin line (CC-295r2 W7)")
    cov = json.loads(cov_b)
    if cov.get("map_sha256") != sha(mb):
        raise SystemExit("REFUSED: coverage.json is not of this map")
    doc = json.loads(ent_b)
    new = check_entries(doc, cov, mp, names, log_rows(a.log), amendment_ok(doc, json.loads(reg_p.read_bytes()), log))
    with open(a.log, "a", encoding="utf-8") as f:
        for e in new:
            f.write(f"{now()} ADD src={e['src']} tag={e['tag']} o365_id={e['o365_id']} entries={sha(ent_b)} "
                    f"drafter={e['drafter']} vi={json.dumps(e['vi'], ensure_ascii=False)}\n")
    print(json.dumps({"tier": B.LABEL, "added": len(new), "log_lines": len(log_rows(a.log))}))
    return 0


def final_doc(mp: dict, mb: bytes, xw: dict, rows: list[dict], log_b: bytes, code: str) -> bytes:
    to80 = {x["o365_id"]: x["coco80"] for x in xw["links"]}
    terms = mp["terms"] + [{"vi": r["vi"], "coco80": to80.get(r["o365_id"])} for r in rows]  # appended: reading 15
    rows_ = mp["rows"] + [{"vi": r["vi"], "o365_id": r["o365_id"], "tag": r["tag"]} for r in rows]
    keep = {k: mp[k] for k in ("categories_sha256", "sources", "r7", "alias_sha256", "crosswalk_sha256")}
    return MV.canon({"schema": "vsps.b_pa1.map.final", "tier": B.LABEL, **keep, "map_v1_sha256": sha(mb),
                     "amendments_log_sha256": sha(log_b), "n_added": len(rows), "code_sha256": code,
                     "terms": terms, "rows": rows_})


def cmd_final(a, log: Path = B.LOG, root: Path = ROOT) -> int:
    out = outside_tree(a.out_dir, root)
    mp, mb, xw, xb = frozen_map(a.map, log)
    categories(a.categories, log, mp)
    log_b = a.log.read_bytes() if a.log.exists() else b""
    doc = final_doc(mp, mb, xw, log_rows(a.log), log_b, B.K.sha_file(Path(__file__)))
    out.mkdir()
    B.write_new(out / MV.XW_NAME, xb)
    B.write_new(out / FINAL_NAME, doc)
    print(json.dumps({"tier": B.LABEL, "n_added": json.loads(doc)["n_added"], "final_map_sha256": sha(doc),
                      "crosswalk_sha256": sha(xb)}))
    return 0


# ---------------------------------------------------------------------------------------------- parity run 2
def cmd_parity2(a, log: Path = B.LOG, root: Path = ROOT, load=sc.load_vi_terms) -> int:
    mb, xb = a.map.read_bytes(), (a.map.parent / MV.XW_NAME).read_bytes()
    mp, msha, xsha = json.loads(mb), sha(mb), sha(xb)
    if a.map.name != FINAL_NAME or mp.get("schema") != "vsps.b_pa1.map.final" or mp.get("crosswalk_sha256") != xsha:
        raise SystemExit("REFUSED: not a final map with its crosswalk")
    lines = log.read_text(encoding="utf-8").splitlines()
    if not MV.at(lines, MV.DONE_RE, mp["map_v1_sha256"]):
        raise SystemExit("REFUSED: no parity1-done line for the map v1 this final map extends")
    freeze = (msha, FINAL_NAME, xsha, mp["map_v1_sha256"], mp["amendments_log_sha256"])
    pins = MV.at(lines, B.PIN_RE, *freeze)
    if not pins:
        raise SystemExit("REFUSED: no final-map freeze pin line (final, crosswalk, map v1, amendments-log shas)")
    if MV.r3(log, root) != mp["sources"]:
        raise SystemExit("REFUSED: matcher v2 files differ from those map v1 was built with")
    ex_b, refs_b, gold_b = ((root / r).read_bytes() for r in (B.EX, MV.REFS, MV.GOLD))
    if sha(ex_b) != B.EX_SHA:
        raise SystemExit("REFUSED: exclusion.json differs from its pin")
    here = str(a.map.parent.resolve())
    starts = MV.at(lines, START2, msha, xsha, sha(refs_b), sha(gold_b), B.EX_SHA, here)
    if len(starts) != 1 or starts[0] < min(pins):
        raise SystemExit("REFUSED: need exactly one parity2-start line, after the final-map freeze pin")
    if MV.at(lines, DONE2, msha):
        raise SystemExit("REFUSED: parity run 2 is already done for this map")
    refs, gold = MV.load_inputs(json.loads(ex_b)["ids"]["coco"]["uitviic_test"], refs_b, gold_b)
    p = MV.parity(refs, gold, load(), mp, json.loads(xb))
    data = MV.canon({**MV.record(p), "run": "parity2"})
    fd = os.open(a.map.parent / "parity2.json", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(fd, "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    sys.stdout.write(data.decode())
    return 0


# ---------------------------------------------------------------------------------------------- H transforms (§8.4)
_TONES = {"oa": "àáảãạ", "oe": "èéẻẽẹ", "uy": "ỳýỷỹỵ"}
_OLD_NEW = {}
for _cl, _ts in _TONES.items():
    _base = {"oa": "òóỏõọ", "oe": "òóỏõọ", "uy": "ùúủũụ"}[_cl]
    for _o, _n in zip(_base, _ts):
        _OLD_NEW[_o + _cl[1]] = _cl[0] + _n  # e.g. "òa" -> "oà"


def tone_flip(t: str) -> str:
    """Old <-> new tone placement in the open oa/oe/uy clusters: new -> old where any new-style cluster occurs,
    else old -> new; only where the cluster ends the syllable (hoà/hòa, not hoàng)."""
    t = unicodedata.normalize("NFC", t)
    pairs = list(_OLD_NEW.items())
    new_style = [(n, o) for o, n in pairs]
    for frm_to in (new_style, pairs):
        out, hit = t, False
        for frm, to in frm_to:
            for f_, t_ in ((frm, to), (frm.capitalize(), to.capitalize())):  # "quý" keeps its y: qu- is a consonant
                rx = re.compile((r"(?<![qQ])" if frm[-1] in "yỳýỷỹỵ" else "") + re.escape(f_) + r"(?![^\W\d_])")
                out, n = rx.subn(t_, out)
                hit |= n > 0
        if hit:
            return out
    return t


def seg_join(text: str, words: list[str]) -> str:
    """The R7 word segmentation: the caption with the whitespace between the syllables of one R7 word replaced by
    '_'; every other character kept (RDRSegmenter rewrites old-style tone placement, so syllables match after norm)."""
    out, c = list(text), 0
    for w in words:
        prev = None
        for syl in w.split("_"):
            while c < len(text) and text[c].isspace():
                c += 1
            if norm(text[c:c + len(syl)]) != norm(syl):
                raise SystemExit("FAULT: a segmenter token does not align with the caption")
            if prev is not None:
                out[prev:c] = ["_"] + [""] * (c - prev - 1) if c > prev else out[prev:c]
            c += len(syl)
            prev = c
    return "".join(out)


def transform(t: str, kind: str, words: list[str] | None = None) -> str:
    if kind == "punct":
        s = t.rstrip()
        return s.rstrip(".!?…").rstrip() if s and s[-1] in ".!?…" else s + "."
    if kind == "nfd":
        return unicodedata.normalize("NFD", t) if unicodedata.normalize("NFC", t) == t else unicodedata.normalize("NFC", t)
    if kind == "tone":
        return tone_flip(t)
    if kind == "seg":
        return seg_join(t, words)
    if kind == "case":
        return t.lower() if t != t.lower() else t[:1].upper() + t[1:]
    if kind == "ws":
        return "  ".join(t.split()) + " "
    raise SystemExit(f"unknown transform {kind}")


def h_pick(file_name: str, accepted: list[str], salt: str = "b-pa1-h2|") -> str:
    """v3.1 §8.4: captioner = argmin over the 4 of sha256(salt + file_name + '|' + captioner id); id = registry key."""
    return min(accepted, key=lambda c: hashlib.sha256((salt + file_name + "|" + c).encode()).hexdigest())


def cmd_htrans(a, seg=rdr) -> int:
    acc, caps = pulled_captions(a.pulled)
    lists = json.loads(a.lists.read_bytes())
    fr = dict(B.read_frame(a.frame.read_bytes()))
    if lists.get("schema") != "vsps.b_pa1.lists.v1" or lists.get("frame_sha256") != B.K.sha_file(a.frame):
        raise SystemExit("REFUSED: lists file is not of this frame")
    by = {k: {r["id"]: r["caption"] for r in rows} for k, rows in caps.items()}
    gate = lists["slice_a"][:GATE_N]
    pick = [(i, h_pick(fr[i], acc)) for i in gate]
    texts = [by[c][i] for i, c in pick]
    words = seg(texts)
    rows = [{"id": i, "cap": c, "tr": k, "text": transform(t, k, w)} for (i, c), t, w in zip(pick, texts, words)
            for k in TRANSFORMS]
    data = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows).encode()
    B.write_new(a.out, data)
    print(json.dumps({"tier": B.LABEL, "rows": len(rows), "changed": sum(r["text"] != t for r, t in zip(
        rows, [x for x in texts for _ in TRANSFORMS])), "sha256": sha(data)}))
    return 0


# ---------------------------------------------------------------------------------------------- selftest
def fake_seg(compounds: set[str]):
    """Stand-in for RDRSegmenter: whitespace syllables, adjacent pairs in `compounds` joined by '_'."""
    def seg(texts):
        out = []
        for t in texts:
            syl, toks, i = t.replace(".", " .").split(), [], 0
            while i < len(syl):
                if i + 1 < len(syl) and f"{syl[i]} {syl[i + 1]}".lower() in compounds:
                    toks.append(f"{syl[i]}_{syl[i + 1]}")
                    i += 2
                else:
                    toks.append(syl[i])
                    i += 1
            out.append(toks)
        return out
    return seg


def selftest() -> int:  # noqa: C901
    import contextlib
    import io
    from types import SimpleNamespace as NS
    global now
    refuse = B.must_refuse

    # transforms (reading 14)
    assert transform("Một con mèo.", "punct") == "Một con mèo" and transform("Một con mèo", "punct") == "Một con mèo."
    assert transform("mèo", "nfd") == unicodedata.normalize("NFD", "mèo") and transform(transform("mèo", "nfd"), "nfd") == "mèo"
    assert tone_flip("hòa bình") == "hoà bình" and tone_flip("hoà bình") == "hòa bình" and tone_flip("Thủy") == "Thuỷ"
    assert tone_flip("quý") == "quý" and tone_flip("hoàng") == "hoàng" and tone_flip("Hòa và thuỷ") == "Hòa và thủy"
    assert tone_flip("con mèo") == "con mèo"
    assert transform("Một Con", "case") == "một con" and transform("một con", "case") == "Một con"
    assert transform("một  con mèo", "ws") == "một  con  mèo "
    assert seg_join("Một con mèo đen.", ["Một", "con_mèo", "đen", "."]) == "Một con_mèo đen."
    assert seg_join("Hòa  bình", ["Hoà_bình"]) == "Hòa_bình"
    refuse(lambda: seg_join("con chó", ["con_mèo"]), "align")
    assert transform("Con mèo", "seg", ["Con_mèo"]) == "Con_mèo"
    acc4 = ["k_a", "k_b", "k_c", "k_d"]
    for j in range(40):
        fnm = f"images/v1/patch0/x{j}.jpg"
        want = min(acc4, key=lambda c: hashlib.sha256(f"b-pa1-h2|{fnm}|{c}".encode()).hexdigest())
        assert h_pick(fnm, acc4) == want == h_pick(fnm, acc4[::-1])

    with G.scratch() as td:
        d = Path(td)
        log, root = d / "LOG.md", d / "repo"
        cats = [{"id": 1, "name": "Cat"}, {"id": 2, "name": "Dog"}, {"id": 3, "name": "Kettle"}, {"id": 4, "name": "Car"}]
        catp = d / MV.CAT_NAME
        catp.write_bytes(json.dumps({"categories": cats}).encode())
        r7 = {}
        for rel in MV.R7:
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_bytes(rel.encode())
            r7[rel] = B.K.sha_file(root / rel)
        (root / STOP).write_text("là\nmột\ncủa\n", encoding="utf-8")
        r7[STOP] = B.K.sha_file(root / STOP)
        xw = MV.canon({"links": [{"o365_id": 1, "coco80": "cat", "tag": "dictionary"},
                                 {"o365_id": 2, "coco80": "dog", "tag": "dictionary"},
                                 {"o365_id": 4, "coco80": "car", "tag": "dictionary"}]})
        mp = {"schema": "vsps.b_pa1.map.v1", "categories_sha256": sha(catp.read_bytes()), "sources": {"s": "x"},
              "r7": r7, "alias_sha256": "a" * 64, "crosswalk_sha256": sha(xw),
              "terms": [{"vi": "mèo", "coco80": "cat"}, {"vi": "chó", "coco80": "dog"}],
              "rows": [{"vi": "mèo", "o365_id": 1, "tag": "dictionary"}, {"vi": "chó", "o365_id": 2, "tag": "dictionary"}]}
        mdir = d / "map1"
        mdir.mkdir()
        (mdir / MV.XW_NAME).write_bytes(xw)
        (mdir / MV.MAP_NAME).write_bytes(MV.canon(mp))
        msha = B.K.sha_file(mdir / MV.MAP_NAME)
        pins = [B.pin_cases(MV.MAP_NAME, msha, MV.XW_NAME, sha(xw))[0], B.pin_cases(MV.CAT_NAME, mp["categories_sha256"])[0]]
        put = lambda *ls: log.write_text("\n".join(ls) + "\n")  # noqa: E731
        put(*pins)

        # the pulled host dir: 4 accepted, 12 captions each
        P = d / "pulled"
        (P / "out/s").mkdir(parents=True)
        (P / "out/a1decode").mkdir(parents=True)
        acc = json.dumps({"accepted": acc4}).encode()
        (P / "out/s/ACCEPT.json").write_bytes(acc)
        caps = ["Một con mèo đen ngồi trên ấm đun nước.", "Một chiếc ô tô và con chó.", "Con mèo là của bé, con mèo."]
        ids = list(range(100, 112))
        for k in acc4:
            (P / f"out/a1decode/captions_{k}.jsonl").write_text(
                "".join(json.dumps({"id": i, "cap": k, "caption": caps[i % 3]}, ensure_ascii=False) + "\n" for i in ids),
                encoding="utf-8")

        def sums():
            (P / "SHA256SUMS_s").write_text(f"{sha(acc)}  out/s/ACCEPT.json\n")
            (P / "SHA256SUMS_a1decode").write_text("".join(
                f"{B.K.sha_file(p)}  out/a1decode/{p.name}\n" for p in sorted((P / "out/a1decode").iterdir())))
        sums()
        seg = fake_seg({"ấm đun", "ô tô", "con mèo"})
        cv = lambda o="cov": cmd_coverage(NS(map=mdir / MV.MAP_NAME, categories=catp, pulled=P, out_dir=d / o), log, root, seg)  # noqa
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            assert cv() == 0
        cov = json.loads((d / "cov" / COV_NAME).read_bytes())
        # 48 captions; df: "con_mèo" 32 (mèo in a term? no: "con mèo" != "mèo"), "ấm_đun" 16, "ô_tô" 16, "đen" 16 ...
        toks = {x["token"]: x["df"] for x in cov["tokens_i"]}
        assert toks["con mèo"] == 32 and toks["ô tô"] == 16 and toks["ấm đun"] == 16 and "là" not in toks, toks
        assert "chó" not in toks and toks["con"] == 16 and "." not in toks and all(n >= 10 for n in toks.values())
        assert listed(Counter({"a": 10, "b": 9, "c": 11})) == [("a", 10), ("c", 11)]
        assert [x["o365_id"] for x in cov["classes_ii"]] == [3, 4] and cov["n_captions"] == 48
        assert not cov["classes_only"]
        with contextlib.redirect_stdout(io.StringIO()):
            cmd_coverage(NS(map=mdir / MV.MAP_NAME, categories=catp, pulled=None, out_dir=d / "cov_ii"), log, root,
                         lambda t: 1 / 0)
        c2 = json.loads((d / "cov_ii" / COV_NAME).read_bytes())
        assert c2["classes_only"] and c2["tokens_i"] == [] and c2["classes_ii"] == cov["classes_ii"]
        assert "Một con mèo" not in buf.getvalue() and "mèo" not in buf.getvalue(), "caption text on stdout"
        refuse(lambda: cmd_coverage(NS(map=mdir / MV.MAP_NAME, categories=catp, pulled=P, out_dir=root / "x"), log,
                                    root, seg), "tracked tree")
        assert not (root / "x").exists()
        (P / "out/s/ACCEPT.json").write_bytes(json.dumps({"accepted": acc4[::-1]}).encode())
        refuse(cv, "SHA256SUMS_s")
        (P / "out/s/ACCEPT.json").write_bytes(acc)
        (P / "out/a1decode/captions_k_e.jsonl").write_text("")
        sums()
        refuse(cv, "other files")
        (P / "out/a1decode/captions_k_e.jsonl").unlink()
        sums()
        (P / "out/a1decode/captions_k_a.jsonl").open("a").write("{}\n")
        refuse(cv, "differs from SHA256SUMS")
        sums()
        refuse(cv, "one per id")
        (P / f"out/a1decode/captions_k_a.jsonl").write_text(
            "".join(json.dumps({"id": i, "cap": "k_a", "caption": caps[i % 3]}, ensure_ascii=False) + "\n" for i in ids),
            encoding="utf-8")
        sums()
        put(pins[1])
        refuse(cv, "freeze pin")
        put(*pins)
        (root / MV.R7[0]).write_bytes(b"changed")
        refuse(cv, "R7 file")
        (root / MV.R7[0]).write_bytes(MV.R7[0].encode())
        catp2 = d / "o2" / MV.CAT_NAME
        catp2.parent.mkdir()
        catp2.write_bytes(json.dumps({"categories": cats[:3]}).encode())
        refuse(lambda: cmd_coverage(NS(map=mdir / MV.MAP_NAME, categories=catp2, pulled=P, out_dir=d / "c2"), log,
                                    root, seg), "class list")

        # amendments: add-only, listed sources only, provenance, one UTC line each
        alog = d / "b_pa1_map_amendments.log"
        amd = d / "AMENDMENT_STEP4_FIXTURE.md"
        amd.write_text("fixture amendment\n")
        AM = {"name": amd.name, "sha256": B.K.sha_file(amd)}

        def ent(es, prov=True, amend=AM, pin=True):
            pv = {"drafter": "fixture", "utc": B.T_UTC, **({"amendment": amend} if amend else {})}
            (d / "e.json").write_text(json.dumps({**({"provenance": pv} if prov else {}), "entries": es},
                                                 ensure_ascii=False), encoding="utf-8")
            if pin:
                with open(log, "a", encoding="utf-8") as f:
                    f.write(B.pin_cases("e.json", B.K.sha_file(d / "e.json"))[0] + "\n")
            return d / "e.json"
        regp = d / "reg.json"
        regp.write_text(json.dumps({"instrument_llm": {"mode": INSTRUMENT_MODE}}))
        am = lambda e, rp=regp: cmd_amend(NS(map=mdir / MV.MAP_NAME, categories=catp, coverage=d / "cov" / COV_NAME,  # noqa
                                             entries=e, log=alog), log, rp)
        E = lambda vi, o, src="i", tag="instrument": {"vi": vi, "o365": o, "src": src, "tag": tag, "why": "main sense",  # noqa
                                                      **({"drafter": "claude-opus-5-5"} if tag == "instrument" else {})}
        assert json.loads((HERE / "b_pa1_registry.json").read_bytes())["instrument_llm"]["mode"] == INSTRUMENT_MODE
        put(*pins, B.pin_cases(amd.name, AM["sha256"])[0])
        refuse(lambda: am(ent([E("ô tô", "Car")], pin=False)), "not on a LOG pin line")  # W7: amendment pinned, file not
        with open(log, "a", encoding="utf-8") as f:
            f.write("\n".join(B.pin_cases("e.json", B.K.sha_file(d / "e.json"))[1]) + "\n")
        refuse(lambda: am(d / "e.json"), "not on a LOG pin line")  # W7: look-alike lines are no pin
        refuse(lambda: am(ent([E("ô tô", "Car")], amend=None)), "LOG-pinned amendment")
        refuse(lambda: am(ent([E("ô tô", "Car")], amend={**AM, "sha256": "0" * 64})), "LOG-pinned amendment")
        regp2 = d / "reg2.json"
        regp2.write_text(json.dumps({"instrument_llm": {"mode": "none"}}))
        refuse(lambda: am(ent([E("ô tô", "Car")]), regp2), "agent-drafted mode")
        refuse(lambda: am(ent([{**E("ô tô", "Car"), "drafter": "a b"}])), "drafter")
        refuse(lambda: am(ent([{k: v for k, v in E("ô tô", "Car").items() if k != "drafter"}])), "drafter")
        now = lambda: B.T_UTC  # noqa: E731
        for es, word in (([E("ô tô", "Car")], None), ([E("ấm đun", "Kettle", tag="gold")], "tag"),
                         ([E("xe", "Car")], "(i) token"), ([E("con mèo", "Cat", src="ii")], "(ii) class"),
                         ([E("mèo", "Car", src="ii")], "already exists"), ([E("ấm đun", "Teapot")], "class list"),
                         ([E("ấm đun", "Kettle"), E("Ấm đun", "Kettle")], "already exists")):
            if word:
                refuse(lambda: am(ent(es)), word)
            else:
                with contextlib.redirect_stdout(io.StringIO()):
                    am(ent(es))
        refuse(lambda: am(ent([E("ấm đun", "Kettle", tag="dictionary")], prov=False)), "has no provenance")
        cov_other = d / "cov_other.json"
        cov_other.write_text(json.dumps({**cov, "map_sha256": "0" * 64}), encoding="utf-8")
        refuse(lambda: cmd_amend(NS(map=mdir / MV.MAP_NAME, categories=catp, coverage=cov_other,
                                    entries=ent([E("ấm đun", "Kettle")]), log=alog), log), "not of this map")
        refuse(lambda: am(ent([E("ô tô", "Car")])), "already exists")  # logged once already
        with contextlib.redirect_stdout(io.StringIO()):
            am(ent([E("ấm đun", "Kettle", src="ii", tag="dictionary")]))
        lr = log_rows(alog)
        assert [(r["vi"], r["o365_id"], r["src"], r["tag"], r["drafter"]) for r in lr] == [
            ("ô tô", 4, "i", "instrument", "claude-opus-5-5"), ("ấm đun", 3, "ii", "dictionary", "-")], lr
        assert all(r["utc"] == B.T_UTC for r in lr) and len(alog.read_text().splitlines()) == 2
        bad_log = d / "bad.log"
        bad_log.write_text("2026 EDIT x\n")
        refuse(lambda: log_rows(bad_log), "not an ADD line")

        # final map: v1 + appended additions, crosswalk byte-equal, once
        fin = lambda o="fin": cmd_final(NS(map=mdir / MV.MAP_NAME, categories=catp, log=alog, out_dir=d / o), log)  # noqa
        with contextlib.redirect_stdout(io.StringIO()):
            fin()
        fd_ = json.loads((d / "fin" / FINAL_NAME).read_bytes())
        assert [t["vi"] for t in fd_["terms"]] == ["mèo", "chó", "ô tô", "ấm đun"] and fd_["terms"][3]["coco80"] is None
        assert fd_["rows"][:2] == mp["rows"] and fd_["rows"][2:] == [{"vi": "ô tô", "o365_id": 4, "tag": "instrument"},
                                                                   {"vi": "ấm đun", "o365_id": 3, "tag": "dictionary"}]
        assert (d / "fin" / MV.XW_NAME).read_bytes() == xw and fd_["map_v1_sha256"] == msha
        assert fd_["amendments_log_sha256"] == B.K.sha_file(alog) and fd_["sources"] == mp["sources"]
        try:
            fin()
            raise AssertionError("final map built twice into one dir")
        except FileExistsError:
            pass

        # htrans: 231 gate ids of slice A in slice order, one caption each by the salted pick, 6 transforms
        fr = [(1000 + j, f"images/v1/patch0/f{j}.jpg") for j in range(300)]
        frb = "".join(f"{i}\t{f}\n" for i, f in fr).encode()
        (d / "frame.tsv").write_bytes(frb)
        sa = [i for i, _ in fr][:250]
        (d / "lists.json").write_text(json.dumps({"schema": "vsps.b_pa1.lists.v1", "frame_sha256": sha(frb),
                                                  "slice_a": sa, "slice_b": []}))
        for k in acc4:
            (P / f"out/a1decode/captions_{k}.jsonl").write_text("".join(json.dumps(
                {"id": i, "cap": k, "caption": f"Con mèo {k[-1]}."}, ensure_ascii=False) + "\n" for i in sa),
                encoding="utf-8")
        sums()
        with contextlib.redirect_stdout(io.StringIO()):
            cmd_htrans(NS(pulled=P, lists=d / "lists.json", frame=d / "frame.tsv", out=d / "h.jsonl"),
                       fake_seg({"con mèo"}))
        hr = [json.loads(x) for x in (d / "h.jsonl").read_text(encoding="utf-8").splitlines()]
        assert len(hr) == 231 * 6 and [r["id"] for r in hr[::6]] == sa[:231]
        fn = dict(fr)
        assert all(r["cap"] == h_pick(fn[r["id"]], acc4) for r in hr)
        assert {r["tr"] for r in hr} == set(TRANSFORMS) and hr[3]["text"].startswith("Con_mèo")
        (d / "lists.json").write_text(json.dumps({"schema": "vsps.b_pa1.lists.v1", "frame_sha256": "0" * 64,
                                                  "slice_a": sa}))
        refuse(lambda: cmd_htrans(NS(pulled=P, lists=d / "lists.json", frame=d / "frame.tsv", out=d / "h2.jsonl"),
                                  fake_seg(set())), "not of this frame")

        # parity run 2: fixture root and LOG, as map_v1's selftest; real REFS / GOLD are never read here
        for rel in (*MV.SRC, B.EX, MV.REFS, MV.GOLD):
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_bytes(rel.encode())
        N = MV.N_IMAGES
        (root / B.EX).write_bytes(json.dumps({"ids": {"coco": {"uitviic_test": list(range(1, N + 1))}}}).encode())
        anns = [{"image_id": i, "caption": "con mèo và ô tô"} for i in range(1, N + 1)]
        (root / MV.REFS).write_bytes(json.dumps({"annotations": anns}).encode())
        (root / MV.GOLD).write_bytes(json.dumps({str(i): {"coco": ["cat"]} for i in range(1, N + 1)}).encode())
        rels = sorted({Path(m.__file__).resolve().relative_to(ROOT.resolve()).as_posix()
                       for m in list(sys.modules.values()) if getattr(m, "__file__", None)
                       and (ROOT / "rescap").resolve() in Path(m.__file__).resolve().parents})
        r3pins = [B.pin_cases(r, B.K.sha_file(ROOT / r))[0] for r in rels] + \
                 [B.pin_cases(r, B.K.sha_file(root / r))[0] for r in MV.SRC]
        fmap = d / "fin" / FINAL_NAME
        fdoc = json.loads(fmap.read_bytes())
        put(*r3pins)
        fdoc["sources"] = MV.r3(log, root)
        fmap.unlink()
        fmap.write_bytes(MV.canon(fdoc))
        fsha = B.K.sha_file(fmap)
        fz = B.pin_cases(FINAL_NAME, fsha, sha(xw), msha, fdoc["amendments_log_sha256"])
        p1 = f"{B.T_UTC} OPS-9-parity1-done: {msha} rc 0"
        real_ex = B.EX_SHA
        B.EX_SHA = sha((root / B.EX).read_bytes())
        here = str(fmap.parent.resolve())
        st2 = f"{B.T_UTC} OPS-9-parity2-start: {fsha} {sha(xw)} {B.K.sha_file(root / MV.REFS)} " \
              f"{B.K.sha_file(root / MV.GOLD)} {B.EX_SHA} {here}"
        vt = [("mèo", "cat"), ("ô tô", "car")]
        pr = lambda: cmd_parity2(NS(map=fmap), log, root, lambda: vt)  # noqa: E731
        try:
            put(*r3pins, fz[0], st2)
            refuse(pr, "parity1-done")
            for bad in fz[1]:
                put(*r3pins, p1, bad, st2)
                refuse(pr, "freeze pin")
            put(*r3pins, p1, fz[0])
            refuse(pr, "parity2-start")
            put(*r3pins, p1, st2, fz[0])
            refuse(pr, "parity2-start")
            put(*r3pins, p1, fz[0], st2, st2)
            refuse(pr, "parity2-start")
            put(*r3pins, p1, fz[0], st2, f"{B.T_UTC} OPS-9-parity2-done: {fsha}")
            refuse(pr, "already done")
            put(*r3pins[1:], p1, fz[0], st2)
            refuse(pr, "no LOG pin line")
            put(*r3pins, p1, fz[0], st2)
            refuse(lambda: cmd_parity2(NS(map=mdir / MV.MAP_NAME), log, root, lambda: vt), "not a final map")
            with contextlib.redirect_stdout(io.StringIO()) as b2:
                assert pr() == 0
            rec = json.loads((fmap.parent / "parity2.json").read_bytes())
            assert rec["run"] == "parity2" and set(rec) == set(MV.record({"delta": 0, "delta_macro": 0, **{
                k: 0 for k in MV.DROPS}})) and b2.getvalue().encode() == (fmap.parent / "parity2.json").read_bytes()
            assert rec["abs_delta_micro_gt_2"] is False and rec["delta_micro_points"] == 0.0, rec
            try:
                pr()
                raise AssertionError("parity run 2 ran twice")
            except FileExistsError:
                pass
        finally:
            B.EX_SHA = real_ex
    print(json.dumps({"tier": B.LABEL, "selftest": "b_pa1_mid ok", "checks": [
        "transforms", "tone-flip", "seg-join", "h-pick", "coverage-df", "coverage-guards", "no-caption-stdout",
        "amend-entries-pin", "amend-add-only", "amend-log", "final-map", "final-once", "htrans", "parity2-guards", "parity2-once"]}))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("selftest")
    cv, am, fi = sp.add_parser("coverage"), sp.add_parser("amend"), sp.add_parser("final")
    for p in (cv, am, fi):
        p.add_argument("--map", type=Path, required=True, help=f"the frozen {MV.MAP_NAME}")
        p.add_argument("--categories", type=Path, required=True, help=MV.CAT_NAME)
    cv.add_argument("--pulled", type=Path, help="the pulled ~/b_pa1_out; omit for the (ii) list alone")
    cv.add_argument("--out-dir", type=Path, required=True)
    am.add_argument("--coverage", type=Path, required=True)
    am.add_argument("--entries", type=Path, required=True)
    for p in (am, fi):
        p.add_argument("--log", type=Path, required=True, help="b_pa1_map_amendments.log (add-only)")
    fi.add_argument("--out-dir", type=Path, required=True)
    sp.add_parser("parity2").add_argument("--map", type=Path, required=True)
    ht = sp.add_parser("htrans")
    ht.add_argument("--pulled", type=Path, required=True)
    ht.add_argument("--lists", type=Path, required=True)
    ht.add_argument("--frame", type=Path, required=True)
    ht.add_argument("--out", type=Path, required=True, help="new file")
    a = ap.parse_args()
    return {"selftest": lambda: selftest(), "coverage": lambda: cmd_coverage(a), "amend": lambda: cmd_amend(a),
            "final": lambda: cmd_final(a), "parity2": lambda: cmd_parity2(a), "htrans": lambda: cmd_htrans(a)}[a.cmd]()


if __name__ == "__main__":
    sys.exit(main())
