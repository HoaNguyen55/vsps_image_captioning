#!/usr/bin/env python3
"""B-PA1-T1 W25 code of R5 (manuscript/prereg/2026-11-01_b_pa1_tier1/AMENDMENT_R5_DRAFT_v1_2.md, sha 9cb21917, commit
3091bf6; §A.1-§A.4, §A.7, §D.2, §D.5; CC-224r3 Ruling 3 C3(a)). TIER 1 / DEV-EXPLORE (B-PA1-T1). Rule = W25 RULE §3
(RULE.md 289c0a59) through w25.rule and build_memory.features / near, unchanged. Ids, features and counts only; no id
is printed and no image pair is ever shown to anyone.

    $PY b_pa1_w25.py selftest                     CPU, synthetic fixtures (torch + imagehash: the W25-K1 laptop venv)
    python3 b_pa1_w25.py rules --out F            §A.7 overlay from R5 §A.2 + §A.4 at HEAD; ids-free
    $PY b_pa1_w25.py coverage --out-dir D         C3, laptop: COCO owner ids vs the cache ids; gap id lists
    $FT b_pa1_w25.py feats --frame T --images I --sscd PT --parts P --blocks N    C4: frame blocks of 500 (M8 or laptop)
    $FT b_pa1_w25.py parity --frame T --images I --sscd PT --parts P              C4, laptop: §D.2 n = 50; P/parity.json
    $FT b_pa1_w25.py recompute --list L --name N --owners O,.. --sscd PT --out NPZ (--images I | --fetch)
                                                     C7: owner features (laptop: --images; M1 slot: --fetch, E-13)
    $PY b_pa1_w25.py decide --frame T --parts P --out-dir D [--extra MANIFEST]    C5, laptop, new out-dir only

T = the frame file of `b_pa1.py slices frame`. Owner caches never leave the laptop (§A.1); only part files leave M8.
decide never overwrites: if `slices pick` finds < 4,000 survivors, C4 features more blocks and a logged decide runs into
a new out-dir (an earlier block's result cannot change: each frame image is compared with the caches only).
coverage and decide refuse unless the owners file (ae4b6630) and the overlay are at their pins and the overlay sha is
on a LOG pin line (CC-224r3 C3; CC-226 NB-1: b_pa1.pin_line). decide also needs the parts' §D.2 parity record
(CC-226 NB-2) and takes a C7 cache only from --extra with its own LOG pin line (CC-226 W1(b)).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent / "w25")]
import b_pa1 as B  # noqa: E402  LABEL, COCO, IC, checked, read_repo, read_frame, write_new, must_refuse
import w25  # noqa: E402  rule, load, save, concat, KEYS, ok_sscd, xm_ids, bm; also F = cen_fetch, K = grl/common

F, K, IC = w25.F, w25.K, B.IC
R5_REL = "manuscript/prereg/2026-11-01_b_pa1_tier1/AMENDMENT_R5_DRAFT_v1_2.md"
R5_SHA = "9cb21917866bb5f7551a3a8118c9e52a2417747a63ddfe238bde7e5062e85423"  # CC-224r3, commit 3091bf6
OWNERS = K.ROOT / ".session_backup/2026-11-02/b_pa1/b_pa1_owners.json"
OWNERS_SHA = "ae4b663064588a8a19dcd0c01a34284229b40c6de90cd24c88d098b7600b71b2"  # OPS-1102b-owners, frozen (NB8)
RULES = K.ROOT / "manuscript/prereg/2026-11-01_b_pa1_tier1/b_pa1_r5_rules.json"
RULES_SHA = "6c5e7282b7f6098b7d49eab3336451b114c48cc8ef5431640a3e632ad6219531"  # `rules`, 2026-11-02
LOG = K.ROOT / ".session_backup/2026-10-13/decisions/LOG.md"
BLOCK, PARITY_N, PARITY_COS = B.BLOCK, 50, 0.9999  # v3.1 l.253; R5 §D.2
PARITY = "parity.json"  # CC-226 NB-2: written by `parity` beside the part files, required by decide
#: R5 §A.2 (c) for a C7 cache: build_memory and its matcher at their HEAD shas (w25 SHA256SUMS; C-EN pins), SSCD
#: 9f26bd4c, pip freeze 1a639a50 (cenfeat_venv_freeze.txt = the W25-K1 laptop venv c_stage1_lists, LOG l.938 (a))
EXPECT = {"build_memory_sha256": "e771b92df9096e286e8d5de207d3adafe49c8e5e59eab276978b0236cc0eeab9",
          "match_openviic_sha256": "c0d9dd30e3222ab6542a7e1acfbb9bd3899e4b6db5c896b0adc4d805c1005a8b",
          "sscd_sha256": w25.SSCD_SHA,
          "freeze_sha256": "1a639a50adf550c50c6dfe284146e279b2a2bf2a716ade743e9eb357ccbf0778"}
COCO_DIRS = {"coco2014": ("train2014", "val2014"), "train2014": ("train2014",), "val2014": ("val2014",),
             "val2017": ("val2017",)}  # R5 E-13: public COCO archive, per file
SHM = Path("/dev/shm/b_pa1_c7")  # C7 --fetch: the only place fetched bytes exist (W25 RULE §5 pattern)
MID = Path("/root/.vsps_machine_id")  # host id file; "m3" on M1
JUDGED = re.compile(r"truncated-judged=CC-[0-9A-Za-z-]+")  # a C7 pin token when truncated > 0 (CC-226r2 Ruling 3(b))
M1 = ".session_backup/machines/M1/root/outputs"
#: R5 §A.2 cells expanded for `rules`: full sha (src holds it in full; it must start with the R5 prefix), the rows a
#: cache is used with (must appear in its R5 coverage cell), COCO-id keyed or not; K4 drops its 43 XM3600 rows (w25)
CACHE = {
    "K1": {"path": f"{M1}/c_en/feats_coco_kval.npz", "src": "scripts/w25/w25.py", "n": 5000, "coco": True,
           "sha256": "9783f7a669aa1b0a6df8e8a78aa3586fb7009f376d8151442ac3acc7da580a7e"},
    "K2": {"path": f"{M1}/c_en/feats_coco_test.npz", "src": "LOG", "n": 5000, "coco": True,
           "sha256": "2bc3b83ea4116603a041559d35e156f11005c44a910f29100439658593d45934"},
    "K3": {"path": f"{M1}/c_en/feats_memory.npz", "src": "scripts/c_t3/c_t3_neardup.py", "n": 112320, "coco": True,
           "sha256": "caf4a62199fccfe903e3a553a3717673d62a32ae07a2e289c2a706d70132e437"},
    "K4": {"path": f"{M1}/c_en/feats_nocaps_val.npz", "src": "scripts/w25/w25.py", "n": 4457, "coco": False,
           "drop_xm": True, "sha256": "b69dac29b4dd07e759d1ff2fc38cb5d716cbe31ddb34c4233ff8f8667b8acba6"},
    "K5": {"path": f"{M1}/w25/feats_ut.npz", "src": "manuscript/prereg/2026-10-28_k2_gate1/w25_decide.json",
           "n": 2402, "coco": True, "sha256": "17d3ebf07ebf95bcd0c8bf123ff65fb8f2df65c52cd4e17ac492e05976b98c1d"},
    **{k: {"path": f"~/vsps_w25k1/{name}.npz", "src": "manuscript/prereg/2026-10-30_mt4_k1k6/w25k1_decide.json",
           "n": n, "coco": k == "K8", "sha256": sha}
       for k, name, n, sha in (
           ("K6", "oiv7_val", 41164, "2ca7e2f56bc3695dc4be13f10d4511881e4460d6d0815c27a6ab1220d8e7c5bb"),
           ("K7", "ktvic_test", 558, "cd985050fd2042b87049410334a05a6406b4363d69c05a45e6ed28ccae86702d"),
           ("K8", "uitviic_test", 231, "4f4784903fb0164309a3b1b6b3ba4fbaa9c09da6c4be5294a6c43f75581ff95f"),
           ("K9", "openviic_test", 2001, "f4c79b825a1b62256dfac15b6ce59bce1054b83386ab4d5d932ac3c4e73d360e"))},
}
CEN_LIST = {"K1": "coco_kval", "K2": "coco_test", "K3": "memory"}  # C3: the committed C-EN id lists (cen_*.tsv)
BASE = ("K1", "K2", "K3")  # R5 §A.2 COCO-id coverage rule: covered(O) = O ∩ (K1, K2, K3), plus the owner's own cache


# ------------------------------------------------------------------------------------------------ pins
def sha_bytes(b: bytes) -> str:
    return F.sha_bytes(b)


def pinned_doc(p: Path, sha: str) -> dict:
    if not p.is_file() or K.sha_file(p) != sha:
        raise SystemExit(f"REFUSED: {p.name} is missing or not at its pin {sha[:8]}")
    return json.loads(p.read_bytes())


def load_pinned(owners: Path, owners_sha: str, rules: Path, rules_sha: str, log: Path) -> tuple[dict, dict]:
    """CC-224r3 C3: owners file and overlay at their shas, the overlay sha on a LOG line, the overlay made from R5
    for this owners file and naming exactly its owners (plus the conditional c rows)."""
    doc = pinned_doc(owners, owners_sha)
    if not B.pin_line(log, rules_sha, rules.name):
        raise SystemExit(f"REFUSED: no LOG line pins {rules.name} at {rules_sha[:8]}")
    ru = pinned_doc(rules, rules_sha)
    if ru["source"]["sha256"] != R5_SHA or ru["owners_file"]["sha256"] != owners_sha or \
            {k for k, o in ru["owners"].items() if o["row"].isdigit()} != set(doc["owners"]):
        raise SystemExit("REFUSED: the overlay is not R5's for this owners file")
    return doc, ru


def cache_path(c: dict) -> Path:
    p = Path(c["path"]).expanduser()
    return p if p.is_absolute() else K.ROOT / p


def usable(c: dict, log: Path) -> bool:
    """R5 §A.2 (a): K2 only from its gatekeeper LOG pin line (CC-224 W7); the others are pinned in committed files."""
    return c["src"] != "LOG" or B.pin_line(log, c["sha256"], Path(c["path"]).name)


# ------------------------------------------------------------------------------------------------ overlay (§A.7)
def table(text: str, sec: str, first: str, width: int) -> dict[str, list[str]]:
    """Rows of the table in R5 section `sec`, keyed by the first token of the first cell; cells verbatim."""
    if f"\n### {sec} " not in text:
        raise SystemExit(f"REFUSED: R5 has no §{sec}")
    rows = {}
    for r in text.split(f"\n### {sec} ", 1)[1].split("\n### ", 1)[0].splitlines():
        c = [x.strip() for x in r.split("|")[1:-1]]
        if not r.startswith("| ") or not re.fullmatch(first, c[0].split()[0]):
            continue
        if len(c) != width or c[0].split()[0] in rows:
            raise SystemExit(f"REFUSED: R5 §{sec} row {c[0].split()[0]} is not a {width}-cell row, or repeats")
        rows[c[0].split()[0]] = c
    return rows


def overlay(text: str, owner_keys, cache: dict = CACHE) -> dict:
    """§A.7: owner key -> rule, spent line, feature source (verbatim §A.4 cells) and the K caches it names; every
    K cache of §A.2 with its path, full sha and rows, each checked against its R5 cell. Ids-free."""
    ca, ow = table(text, "A.2", r"K\d", 5), table(text, "A.4", r"\d+|c\d", 8)
    if set(ca) != set(cache):
        raise SystemExit(f"REFUSED: R5 §A.2 caches {sorted(ca)} are not {sorted(cache)}")
    caches = {}
    for k, c in ca.items():
        e, path_r5, pre = cache[k], re.findall(r"`([^`]+)`", c[0])[0], c[1].strip("`")
        tail = path_r5.removeprefix("...")
        if len(pre) != 8 or not e["sha256"].startswith(pre) or f"{e['n']:,}" not in c[3] or \
                not (e["path"] == path_r5 or (tail != path_r5 and e["path"].endswith(tail))):
            raise SystemExit(f"REFUSED: {k} differs from its R5 §A.2 cell (path, sha prefix or rows)")
        caches[k] = {**e, "drop_xm": e.get("drop_xm", False), "path_r5": path_r5, "sha256_r5": pre, "pin": c[2],
                     "coverage": c[3], "fn_env": c[4]}
    owners, row = {}, {}
    for k, c in ow.items():
        key = c[1].strip("`") if k.isdigit() else k
        ks, gs = sorted(set(re.findall(r"\bK[1-9]\b", c[5]))), sorted(set(re.findall(r"\bG[1-4]\b", c[7])))
        if not gs and (m := re.fullmatch(r"as #(\d+)", c[7])) and m[1] in row:  # "as #2": that earlier row's rules
            gs = row[m[1]]["rules"]
        if not (gs or c[4].startswith("exempt")) or set(ks) - set(caches) or key in owners:  # W3 owner: no rule
            raise SystemExit(f"REFUSED: R5 §A.4 row {k}: no rule, an unknown cache, or a repeated owner")
        owners[key] = row[k] = {"row": k, "name": c[1], "status": c[2], "id_space": c[3], "gate1": c[4],
                                "feature_source": c[5], "spent_line": c[6], "rule": c[7], "caches": ks, "rules": gs}
    if {k for k, o in owners.items() if o["row"].isdigit()} != set(owner_keys):
        raise SystemExit("REFUSED: R5 §A.4 owners are not the owners file's")
    return {"schema": "vsps.b_pa1.r5_rules.v1", "tier": B.LABEL, "caches": caches, "owners": owners,
            "source": {"path": R5_REL, "sha256": R5_SHA, "sections": ["A.2", "A.4"]},
            "owners_file": {"path": str(OWNERS.relative_to(K.ROOT)), "sha256": OWNERS_SHA},
            "note": "ids-free machine copy of R5 §A.2/§A.4; the binding text is R5 (CC-224r3 Ruling 5)"}


def overlay_bytes(doc: dict) -> bytes:
    return (json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()


def cmd_rules(a) -> None:
    text = B.read_repo(R5_REL, R5_SHA).decode()
    keys = json.loads(B.checked(OWNERS.read_bytes(), OWNERS.name, OWNERS_SHA))["owners"]
    for k, e in CACHE.items():  # each full sha where R5 §A.2 (a) pins it: committed at HEAD, or K2's LOG line
        if not (usable(e, LOG) if e["src"] == "LOG" else e["sha256"] in B.read_repo(e["src"], None).decode()):
            raise SystemExit(f"REFUSED: {k} full sha is not in {e['src']}")
    data = overlay_bytes(overlay(text, keys))
    B.write_new(a.out, data)
    doc = json.loads(data)
    print(json.dumps({"tier": B.LABEL, "sha256": sha_bytes(data), "caches": len(doc["caches"]),
                      "owners": len(doc["owners"])}))


# ------------------------------------------------------------------------------------------------ C3 coverage
def coco_ids(c: dict, listed: set | None = None) -> set[int]:
    """COCO ids with a readable feature row: the npz `ids` and `unreadable` keys only, after the sha (no feature value
    is read); their number must be the R5 rows; inside the committed C-EN list where the cache has one."""
    p = cache_path(c)
    if K.sha_file(p) != c["sha256"]:
        raise SystemExit(f"FAULT: {p.name} differs from its pin {c['sha256'][:8]}")
    with np.load(p) as z:
        ids = {int(i) for i in z["ids"].tolist()} - {int(i) for i in z["unreadable"].tolist()}
    if len(ids) != c["n"] or (listed is not None and not ids <= listed):
        raise SystemExit(f"FAULT: {p.name}: {len(ids)} readable ids, not the {c['n']} of its record and list")
    return ids


def coverage(doc: dict, ru: dict, ids_of: dict[str, set]) -> tuple[dict, dict]:
    """R5 §A.2: covered(O) = O ∩ ids of K1-K3 and of the COCO caches §A.4 names for O; gap(O) = the rest. A cache
    missing from ids_of (unusable) covers nothing, so its ids fall in the gap (fail closed)."""
    rec, gaps = {}, {}
    for k, o in sorted(doc["owners"].items()):
        if o["id_space"] != B.COCO or o["status"] != "held":
            continue
        if len(o["ids"]) != o["n"] or IC.sha_ids(o["ids"]) != o["ids_sha256"]:
            raise SystemExit(f"REFUSED: owner {k} ids differ from its ids_sha256")
        ks = sorted(set(BASE + tuple(ru["owners"][k]["caches"])) & set(ids_of))
        gaps[k] = sorted(set(o["ids"]) - set().union(*(ids_of[c] for c in ks)))
        rec[k] = {"n": o["n"], "covered": o["n"] - len(gaps[k]), "gap": len(gaps[k]), "caches": ks,
                  "gap_sha256": IC.sha_ids(gaps[k]), "rule": ru["owners"][k]["rule"]}
    return rec, gaps


def run_coverage(out: Path, owners: Path, owners_sha: str, rules: Path, rules_sha: str, log: Path, lists) -> dict:
    if out.exists():
        raise SystemExit(f"REFUSED: {out} exists")
    doc, ru = load_pinned(owners, owners_sha, rules, rules_sha, log)
    ids_of = {k: coco_ids(c, lists(k) if k in CEN_LIST else None) for k, c in sorted(ru["caches"].items())
              if c["coco"] and usable(c, log)}
    rec, gaps = coverage(doc, ru, ids_of)
    out.mkdir(parents=True, exist_ok=False)
    for k, g in gaps.items():  # gap_<owner>.txt bytes = IC.sha_ids input, so its file sha is gap_sha256
        B.write_new(out / f"gap_{k}.txt", "".join(f"{i}\n" for i in g).encode())
    data = (json.dumps({"schema": "vsps.b_pa1.w25_coverage.v1", "tier": B.LABEL, "owners": rec,
                        "caches_used": sorted(ids_of), "owners_sha256": owners_sha, "rules_sha256": rules_sha,
                        "utc": F.utc()}, sort_keys=True, indent=1) + "\n").encode()
    B.write_new(out / "coverage.json", data)
    return {"tier": B.LABEL, "coverage_sha256": sha_bytes(data), "caches_used": sorted(ids_of),
            "owners": {k: [r["n"], r["covered"], r["gap"], r["gap_sha256"][:8]] for k, r in rec.items()}}


def cmd_coverage(a) -> None:
    lists = lambda k: {r[0] for r in F.load_list(CEN_LIST[k])}  # noqa: E731  sha via the C-EN SHA256SUMS
    print(json.dumps(run_coverage(Path(a.out_dir), OWNERS, OWNERS_SHA, RULES, RULES_SHA, LOG, lists)))


# ------------------------------------------------------------------------------------------------ C4 block-W feats
def outside_repo(p: Path) -> Path:
    p = p.resolve()
    if p == K.ROOT or K.ROOT in p.parents:
        raise SystemExit(f"REFUSED: {p} is inside the repository; feature files are never committed")
    p.mkdir(parents=True, exist_ok=True)
    return p


def feats_blocks(frame: Path, images: Path, sscd: str, parts: Path, blocks: int, workers: int = 4, features=None,
                 block: int = BLOCK) -> None:
    """R5 §D.2: the first `blocks` blocks of the frame, in slice order; one part file per block by tmp + rename; a
    rerun skips finished parts. A missing or unreadable frame image is a FAULT (never a silent survivor)."""
    features = features or w25.bm().features
    fb = frame.read_bytes()
    rows, fsha, parts = B.read_frame(fb), sha_bytes(fb), outside_repo(parts)
    for n in range(blocks):
        out, blk = parts / f"part_{n:04d}.npz", rows[n * block:(n + 1) * block]
        if out.exists() or not blk:
            continue
        paths = [images / f for _, f in blk]
        if lost := sum(not p.is_file() for p in paths):
            raise SystemExit(f"FAULT: block {n}: {lost} frame image(s) not staged")
        f = features(paths, sscd, workers=workers)
        if f["unreadable"]:
            raise SystemExit(f"FAULT: block {n}: {len(f['unreadable'])} frame image(s) cannot be hashed")
        tmp = parts / f".part_{n:04d}.npz"
        w25.save(tmp, [i for i, _ in blk], f, frame_sha256=fsha, block=n, truncated=len(f["truncated"]), utc=F.utc())
        tmp.rename(out)
        print(json.dumps({"part": n, "n": len(blk)}), flush=True)


def part_meta(p: Path) -> dict:
    with np.load(p) as z:
        return json.loads(str(z["meta"]))


def parity(ref: dict, new: dict, n: int = PARITY_N) -> dict:
    """R5 §D.2: the first n frame images featured here equal block 0 of the part files: file sha and the four hashes
    exactly, SSCD cosine >= 0.9999 on every row; else FAULT."""
    x, y = ref["sscd"][:n], new["sscd"]
    same = new["ids"] == ref["ids"][:n] and new["sha"] == ref["sha"][:n] and \
        all(np.array_equal(ref[k][:n], new[k]) for k in w25.KEYS[:4])
    cos = (x * y).sum(1) / (np.linalg.norm(x, axis=1) * np.linalg.norm(y, axis=1))
    rec = {"n": len(new["ids"]), "hashes_equal": bool(same), "sscd_cos_min": float(cos.min())}
    if len(new["ids"]) != n or not same or not (cos >= PARITY_COS).all():
        raise SystemExit(f"FAULT: block-W feature parity failed {rec}")
    return rec


def write_parity(parts: Path, fsha: str, rec: dict) -> None:
    """CC-226 NB-2: the §D.2 pass, bound to this frame and to these part files' block 0; never overwritten."""
    B.write_new(parts / PARITY, (json.dumps({"tier": B.LABEL, "frame_sha256": fsha, "part_0000_sha256": K.sha_file(
        parts / "part_0000.npz"), **rec}, sort_keys=True) + "\n").encode())


def parity_ok(parts: Path, fsha: str, part0_sha: str) -> str:
    p = parts / PARITY
    r = json.loads(p.read_bytes()) if p.is_file() else {}
    if r.get("frame_sha256") != fsha or r.get("part_0000_sha256") != part0_sha or r.get("hashes_equal") is not True \
            or not r.get("sscd_cos_min", 0) >= PARITY_COS:
        raise SystemExit("REFUSED: no §D.2 parity record for these part files (b_pa1_w25.py parity)")
    return K.sha_file(p)


def cmd_feats(a) -> None:
    feats_blocks(Path(a.frame), Path(a.images), w25.ok_sscd(Path(a.sscd)), Path(a.parts), a.blocks, a.workers)


def cmd_parity(a) -> None:
    fb, p0 = Path(a.frame).read_bytes(), Path(a.parts) / "part_0000.npz"
    if part_meta(p0)["frame_sha256"] != sha_bytes(fb):
        raise SystemExit("REFUSED: part_0000 is not of this frame")
    rows = B.read_frame(fb)[:PARITY_N]
    f = w25.bm().features([Path(a.images) / r[1] for r in rows], w25.ok_sscd(Path(a.sscd)), workers=a.workers)
    new = {"ids": [r[0] for r in rows], "sha": f["sha"], **{k: f[k] for k in w25.KEYS}}
    rec = parity(w25.load(p0), new)
    write_parity(Path(a.parts), sha_bytes(fb), rec)
    print(json.dumps({"tier": B.LABEL, "parity": rec}))


# ------------------------------------------------------------------------------------------------ C7 owner recompute
def read_list(b: bytes) -> list[tuple[str, str]]:
    """C7 id list: id TAB (relative image path | COCO space); ids are strings (hex XM3600 ids included)."""
    rows = [r.split("\t") for r in b.decode().splitlines()]
    if not rows or any(len(r) != 2 or not B.ID_RE.fullmatch(r[0]) or not B.plain(0, r[1]) for r in rows) or \
            len({r[0] for r in rows}) != len(rows):
        raise SystemExit("REFUSED: not a C7 list (id TAB relative path or COCO space, ids distinct)")
    return [(i, x) for i, x in rows]


def coco_urls(i: str, space: str) -> list[str]:
    """E-13: the public COCO archive file URLs of one COCO id, in the order tried (no zip, CC-224r3 NB-13)."""
    if space not in COCO_DIRS or not i.isdigit():
        raise SystemExit("REFUSED: a --fetch row is not a COCO id with space coco2014, train2014, val2014 or val2017")
    return [F.COCO_URL.format(filepath=d, file=f"COCO_{d}_{int(i):012d}.jpg" if d.endswith("2014") else
                              f"{int(i):012d}.jpg") for d in COCO_DIRS[space]]


def fetch_set(rows: list[tuple[str, str]], folder: Path, get=F.get) -> tuple[list[tuple[str, Path]], int]:
    """E-13 fetch step: each image per file into the tmpfs folder; an image no URL returns is counted, never fatal."""
    folder.mkdir(parents=True, exist_ok=False)
    got, lost = [], 0
    for i, space in rows:
        for url in coco_urls(i, space):
            if (b := get(url)[0]) is not None:
                (folder / f"{i}.jpg").write_bytes(b)
                got.append((i, folder / f"{i}.jpg"))
                break
        else:
            lost += 1
    return got, lost


def m1_host(mid: Path = MID) -> bool:
    """E-13: the M1 slot only (M1 = the m3-role custody host, CC-209 r1(a)); never a rental, never the laptop (where
    /root is unreadable: PermissionError -> False, CC-226r2 NB-1)."""
    try:
        return mid.is_file() and mid.read_text().strip() == "m3"
    except OSError:
        return False


def provenance(name: str, owners: list[str], list_sha: str, sscd: str, freeze: str) -> dict:
    """R5 §A.2 (b)/(c) for a C7 cache: what it covers and how it was made."""
    bm = w25.bm()
    return {"set": name, "owners": owners, "list_sha256": list_sha, "sscd_sha256": K.sha_file(Path(sscd)),
            "freeze_sha256": freeze, "build_memory_sha256": K.sha_file(Path(bm.__file__)),
            "match_openviic_sha256": K.sha_file(Path(bm.MO.__file__)), "tier": B.LABEL}


def freeze_sha() -> str:
    import subprocess

    return sha_bytes(subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, check=True).stdout)


def recompute(rows: list[tuple[str, Path]], n_listed: int, missing: int, sscd: str, out: Path, meta: dict,
              workers: int = 4, features=None, retry: bool = True) -> dict:
    """C7 (CC-226 W1(a)): build_memory.features unchanged (CC-193 truncated retry, as W25-K1's owner caches) on the
    images present; the npz meta carries the provenance, the retry flag used (CC-226r2 NB-2) and the missing /
    unreadable / truncated counts."""
    features = features or w25.bm().features
    f = features([p for _, p in rows], sscd, workers=workers, retry_truncated=retry)
    rec = {**meta, "retry_truncated": retry, "n_listed": n_listed, "n_missing": missing,
           "n_unreadable": len(f["unreadable"]), "n_truncated": len(f["truncated"]),
           "n_readable": len(rows) - len(f["unreadable"]), "utc": F.utc()}
    tmp = out.with_name(f".{out.name}")
    w25.save(tmp, [i for i, _ in rows], f, **rec)
    tmp.rename(out)
    return rec


def cmd_recompute(a, mid: Path = MID) -> None:
    lb, out = Path(a.list).read_bytes(), Path(a.out)
    rows = read_list(lb)
    if not a.images and not m1_host(mid):
        raise SystemExit("REFUSED: --fetch runs in the M1 slot only (R5 E-13)")
    outside_repo(out.parent)
    if out.exists():
        raise SystemExit(f"REFUSED: {out} exists")
    sscd = w25.ok_sscd(Path(a.sscd))
    meta = provenance(a.name, a.owners.split(","), sha_bytes(lb), sscd, freeze_sha())
    if a.images:
        have = [(i, Path(a.images) / x) for i, x in rows]
        ok = [(i, p) for i, p in have if p.is_file()]
        rec = recompute(ok, len(rows), len(rows) - len(ok), sscd, out, meta, a.workers)
    else:
        folder = SHM / a.name
        try:
            got, lost = fetch_set(rows, folder)
            rec = recompute(got, len(rows), lost, sscd, out, meta, a.workers)
        finally:
            w25.drop(folder, out.parent / "deletions.log", f"after C7 {a.name} features")
    print(json.dumps({"tier": B.LABEL, "out_sha256": K.sha_file(out), **{k: rec[k] for k in (
        "set", "n_listed", "n_missing", "n_unreadable", "n_truncated", "n_readable", "list_sha256")}}))


# ------------------------------------------------------------------------------------------------ C5 decide
def drop_xm(f: dict, oid: dict, xm: set) -> dict:
    """K4 as W25 compared it (w25.inputs): the NoCaps val rows of XM3600 images dropped by id (CC-153 r4)."""
    keep = [i for i, n in enumerate(f["ids"]) if oid[n] not in xm]
    return {"ids": [f["ids"][i] for i in keep], "sha": [f["sha"][i] for i in keep],
            **{k: f[k][keep] for k in w25.KEYS}, "unreadable": [u for u in f["unreadable"] if oid[u] not in xm]}


def nocaps_xm() -> tuple[dict, set]:
    return {r[0]: r[1][:-4] for r in F.load_list("nocaps_val")}, w25.xm_ids()


def load_cache(c: dict, log: Path, xm=nocaps_xm) -> dict:
    """A G1 cache valid under R5 §A.2: usable pin, full sha (w25.load FAULTs otherwise), the R5 rows readable."""
    if not usable(c, log):
        raise SystemExit(f"FAULT: {Path(c['path']).name} has no LOG pin line; not a valid gate-2 source (R5 §A.2)")
    f = w25.load(cache_path(c), c["sha256"])
    if c["drop_xm"]:
        f = drop_xm(f, *xm())
    if len(f["ids"]) - len(f["unreadable"]) != c["n"]:
        raise SystemExit(f"FAULT: {Path(c['path']).name}: not the {c['n']} readable rows of its R5 record")
    return f


def load_extra(c: dict, log: Path, expect: dict) -> dict:
    """CC-226 W1(b), CC-226r2 Ruling 3: a C7 cache at its full sha whose meta shows R5 §A.2 (b) and (c), with a LOG
    pin line carrying its file name, full sha, n=<readable>, listed= / missing= / unreadable= / truncated= counts and
    its id-list sha; a cache with truncated > 0 also needs 'truncated-judged=CC-' on that line (a judge read it)."""
    p = Path(c["path"]).expanduser()
    f, m = w25.load(p, c["sha256"]), part_meta(p)
    n = len(f["ids"]) - len(f["unreadable"])
    if any(m.get(k) != v for k, v in expect.items()) or n != c["n"] or m.get("n_readable") != n or \
            m.get("owners") != c["owners"] or not re.fullmatch(r"[0-9a-f]{64}", str(m.get("list_sha256"))):
        raise SystemExit(f"FAULT: {p.name}: its provenance or count is not R5 §A.2 (b)/(c) or the manifest's")
    counts = [f"{k}={m[f'n_{k}']}" for k in ("listed", "missing", "unreadable", "truncated")]
    judged = [JUDGED] if m["n_truncated"] else []
    if not B.pin_line(log, c["sha256"], p.name, f"n={n}", *counts, *judged, m["list_sha256"]):
        raise SystemExit(f"FAULT: {p.name} has no LOG pin line with its sha, n={n}, {' '.join(counts)}, list sha"
                         f"{' and truncated-judged=CC-' if judged else ''}")
    return f


def frame_feats(frame: Path, parts: Path, block: int = BLOCK) -> tuple[dict, str, list[str]]:
    """The part files of C4: blocks 0..n-1 of this frame, each with the frame's ids in order and no unreadable row."""
    fb = frame.read_bytes()
    rows, fsha, files = B.read_frame(fb), sha_bytes(fb), sorted(parts.glob("part_*.npz"))
    if not files or [p.name for p in files] != [f"part_{n:04d}.npz" for n in range(len(files))]:
        raise SystemExit("REFUSED: the part files are not blocks 0..n-1")
    fs = []
    for n, p in enumerate(files):
        f = w25.load(p)
        if part_meta(p).get("frame_sha256") != fsha or f["unreadable"] or \
                f["ids"] != [i for i, _ in rows[n * block:(n + 1) * block]]:
            raise SystemExit(f"REFUSED: {p.name} is not block {n} of this frame")
        fs.append(f)
    return w25.concat(fs), fsha, [K.sha_file(p) for p in files]


def decide(x: dict, caches: dict[str, dict], near) -> tuple[list[int], dict]:
    """W25 RULE §3 unchanged (w25.rule: C1 byte-identical OR C2 near OR C3 SSCD > 0.75; SSCD >= 0.5 reported only) of
    every frame image against every G1 cache; excluded = the union over caches."""
    per = {k: w25.rule(x, y, near) for k, y in sorted(caches.items())}
    ex = np.zeros(len(x["ids"]), bool)
    for r in per.values():
        ex |= r["excluded"]
    ids = sorted(int(i) for i, e in zip(x["ids"], ex) if e)
    return ids, {"n_frame_decided": len(x["ids"]), "n_excluded": len(ids), "n_survivors": len(x["ids"]) - len(ids),
                 "counts": {k: {c: int(v.sum()) for c, v in r.items()} for k, r in per.items()},
                 "n_compared": {k: len(y["ids"]) - len(y["unreadable"]) for k, y in caches.items()}}


def run_decide(frame: Path, parts: Path, out: Path, owners: Path, owners_sha: str, rules: Path, rules_sha: str,
               log: Path, near=None, xm=nocaps_xm, block: int = BLOCK, extra: Path | None = None,
               expect: dict = EXPECT) -> dict:
    if out.exists():
        raise SystemExit(f"REFUSED: {out} exists (never overwritten)")
    doc, ru = load_pinned(owners, owners_sha, rules, rules_sha, log)
    g1 = sorted({c for o in ru["owners"].values() if "G1" in o["rules"] for c in o["caches"]})
    x, fsha, part_shas = frame_feats(frame, parts, block)
    psha = parity_ok(parts, fsha, part_shas[0])
    caches = {k: load_cache(ru["caches"][k], log, xm) for k in g1}
    man = json.loads(extra.read_bytes()) if extra else {"caches": {}}
    cov, shas = {}, {k: ru["caches"][k]["sha256"] for k in g1}
    for k, c in sorted(man["caches"].items()):
        if k in caches or not c["owners"] or not set(c["owners"]) <= set(doc["owners"]):
            raise SystemExit(f"REFUSED: manifest cache {k}: a K name, or owners not in the owners file")
        f = caches[k] = load_extra(c, log, expect)
        have = {str(i) for i in f["ids"]} - {str(i) for i in f["unreadable"]}
        cov[k] = {o: [doc["owners"][o]["n"], len({str(i) for i in doc["owners"][o].get("ids", [])} & have)]
                  for o in c["owners"]}  # [owner n, owner ids with a readable row here]
        shas[k] = c["sha256"]
    ids, rec = decide(x, caches, near or w25.bm().near)
    body = "".join(f"{i}\n" for i in ids).encode()
    rec |= {"schema": "vsps.b_pa1.w25_decide.v1", "tier": B.LABEL, "frame_sha256": fsha, "excluded_sha256":
            sha_bytes(body), "rule": "W25 RULE §3: (C1 byte-identical OR C2 min(pHash,dHash)<=10 AND SSCD>=0.5) OR "
            "C3 SSCD>0.75, against every G1 cache of the R5 overlay and every pinned C7 cache", "utc": F.utc(),
            "caches_compared": sorted(caches), "extra_owner_coverage": cov,
            "inputs_sha256": {"owners": owners_sha, "rules": rules_sha, "parts": part_shas, "parity": psha,
                              "extra_manifest": sha_bytes(extra.read_bytes()) if extra else None, **shas}}
    out.mkdir(parents=True, exist_ok=False)
    B.write_new(out / "w25_excluded_ids.txt", body)
    data = (json.dumps(rec, sort_keys=True, indent=1) + "\n").encode()
    B.write_new(out / "w25_decide.json", data)
    return {"tier": B.LABEL, **{k: rec[k] for k in ("n_frame_decided", "n_excluded", "n_survivors", "excluded_sha256")},
            "decide_sha256": sha_bytes(data)}


def cmd_decide(a) -> None:
    print(json.dumps(run_decide(Path(a.frame), Path(a.parts), Path(a.out_dir), OWNERS, OWNERS_SHA, RULES, RULES_SHA,
                                LOG, extra=Path(a.extra) if a.extra else None)))


# ------------------------------------------------------------------------------------------------ selftest
def selftest() -> None:
    import contextlib
    import io
    import tempfile
    from types import SimpleNamespace

    import torch
    from PIL import Image

    BM, refuse = w25.bm(), B.must_refuse
    rng = np.random.default_rng(0)
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)

        class Net(torch.nn.Module):  # dummy SSCD (as w25 selftest): 512-d unit vector of pooled colour statistics
            def forward(self, x):
                v = torch.cat([x.mean((2, 3)), x.std((2, 3))], 1).repeat(1, 86)[:, :512]
                return v / (v * v).sum(1, keepdim=True).sqrt()

        pt = str(d / "dummy.pt")
        torch.jit.script(Net()).save(pt)
        imgs = d / "o365"
        (imgs / "patch0").mkdir(parents=True)
        for i, k in enumerate("abcd"):  # a, b, c: one colour channel each (distinct dummy SSCD); d: grey
            px = np.zeros((120, 160, 3), np.uint8)
            if i < 3:
                px[..., i] = rng.integers(0, 255, (120, 160))
            else:
                px[:] = rng.integers(0, 255, (120, 160, 1))
            Image.fromarray(px).save(imgs / f"patch0/{k}.jpg", quality=90)
        frame = d / "frame.tsv"
        frame.write_bytes(b"".join(f"{100 + i}\tpatch0/{k}.jpg\n".encode() for i, k in enumerate("abcd")))

        # C4: blocks of 2, resume skips a finished part, staging and readability FAULT, never inside the repo
        calls = []
        fx = lambda p, s, workers: calls.append(len(p)) or BM.features(p, s, workers=1)  # noqa: E731
        parts = d / "parts"
        with contextlib.redirect_stdout(io.StringIO()):
            feats_blocks(frame, imgs, pt, parts, 1, features=fx, block=2)
            feats_blocks(frame, imgs, pt, parts, 3, features=fx, block=2)
        assert calls == [2, 2] and sorted(p.name for p in parts.iterdir()) == ["part_0000.npz", "part_0001.npz"]
        assert part_meta(parts / "part_0001.npz")["frame_sha256"] == K.sha_file(frame)
        assert part_meta(parts / "part_0001.npz")["truncated"] == 0  # CC-226 NB-4
        p0 = w25.load(parts / "part_0000.npz")
        assert p0["ids"] == [100, 101] and not p0["unreadable"]
        refuse(lambda: feats_blocks(frame, d / "none", pt, d / "p2", 1, features=fx, block=2), "not staged")
        bad = d / "bad"
        (bad / "patch0").mkdir(parents=True)
        for k in "ab":
            (bad / f"patch0/{k}.jpg").write_bytes(b"not a jpeg")
        with contextlib.redirect_stderr(io.StringIO()):
            refuse(lambda: feats_blocks(frame, bad, pt, d / "p3", 1, features=fx, block=2), "cannot be hashed")
        refuse(lambda: feats_blocks(frame, imgs, pt, K.ROOT / "x_parts", 1, features=fx, block=2), "inside the repo")
        refuse(lambda: B.read_frame(b"1\t../a.jpg\n"), "not a frame file")

        # C4 parity (§D.2): same features pass; one moved SSCD row fails
        new = {k: (v[:2] if k != "ids" else v[:2]) for k, v in p0.items() if k != "unreadable"}
        assert parity(p0, new, n=2)["hashes_equal"]
        moved = {**new, "sscd": new["sscd"] * np.array([[1.0], [-1.0]], np.float32)}
        refuse(lambda: parity(p0, moved, n=2), "parity failed")
        refuse(lambda: parity(p0, {**new, "sha": ["x", "y"]}, n=2), "parity failed")
        fsha = K.sha_file(frame)  # CC-226 NB-2: the record binds frame and block 0; decide refuses without it
        refuse(lambda: parity_ok(parts, fsha, K.sha_file(parts / "part_0000.npz")), "parity record")
        write_parity(parts, fsha, parity(p0, new, n=2))
        assert parity_ok(parts, fsha, K.sha_file(parts / "part_0000.npz")) == K.sha_file(parts / PARITY)
        refuse(lambda: parity_ok(parts, fsha, "0" * 64), "parity record")
        refuse(lambda: parity_ok(parts, "0" * 64, K.sha_file(parts / "part_0000.npz")), "parity record")
        with contextlib.suppress(FileExistsError):
            write_parity(parts, fsha, {})
            raise AssertionError("the parity record was overwritten")

        # C7 (CC-226 W1(a)): string/hex ids, missing and unreadable counted; provenance in the meta
        (imgs / "junk.jpg").write_bytes(b"not a jpeg")
        lb = b"k1\tpatch0/c.jpg\nc0ffee\tpatch0/gone.jpg\nfeed\tjunk.jpg\n"
        rows7 = [(i, imgs / x) for i, x in read_list(lb)]
        ok7 = [(i, q) for i, q in rows7 if q.is_file()]
        meta7 = provenance("r1", ["own_k"], sha_bytes(lb), pt, "f" * 64)
        r1 = d / "c7" / "r1.npz"
        r1.parent.mkdir()
        with contextlib.redirect_stderr(io.StringIO()):
            rec7 = recompute(ok7, 3, 1, pt, r1, meta7, features=lambda q, s_, workers, retry_truncated:
                             BM.features(q, s_, workers=1, retry_truncated=retry_truncated))
        assert {k: rec7[k] for k in ("n_listed", "n_missing", "n_unreadable", "n_readable", "n_truncated")} == \
            {"n_listed": 3, "n_missing": 1, "n_unreadable": 1, "n_readable": 1, "n_truncated": 0}, rec7
        flags = []  # CC-226r2 NB-2: the meta records the retry flag actually passed to features
        stub = lambda q, s_, workers, retry_truncated: flags.append(retry_truncated) or {  # noqa: E731
            **BM.features(q, s_, workers=1), "truncated": [(0, 5)]}
        rt = d / "c7" / "rt.npz"  # one truncated-retried image, retry off: recorded as used
        recompute(ok7[:1], 1, 0, pt, rt, provenance("rt", ["own_k"], sha_bytes(lb), pt, "f" * 64), features=stub,
                  retry=False)
        assert flags == [False] and part_meta(rt)["retry_truncated"] is False and part_meta(rt)["n_truncated"] == 1
        assert rec7["retry_truncated"] is True and part_meta(r1)["retry_truncated"] is True
        z7 = w25.load(r1)
        assert z7["ids"] == ["k1", "feed"] and z7["unreadable"] == ["feed"] and part_meta(r1)["list_sha256"] == \
            sha_bytes(lb) and part_meta(r1)["build_memory_sha256"] == EXPECT["build_memory_sha256"]
        for bad7 in (b"a\tx.jpg\na\ty.jpg\n", b"a\t../x.jpg\n", b"a b\tx.jpg\n", b""):
            refuse(lambda: read_list(bad7), "not a C7 list")
        assert len(freeze_sha()) == 64
        (d / "mid").write_text("m3\n")
        (d / "mid4").write_text("m4\n")
        assert m1_host(d / "mid") and not m1_host(d / "mid4") and not m1_host(d / "none")

        class Deny:  # the laptop: /root unreadable
            def is_file(self):
                raise PermissionError("/root")
        assert not m1_host(Deny())
        lf = d / "c7" / "list.tsv"
        lf.write_bytes(b"5\tcoco2014\n")
        rc = lambda out, images=None, mid=d / "mid": cmd_recompute(SimpleNamespace(  # noqa: E731
            list=str(lf), out=str(out), images=images, fetch=images is None, name="rf", owners="own_k", sscd=pt,
            workers=1), mid)
        for m_ in (d / "mid4", d / "none", Deny()):  # call site (CC-226r2 NB-1): --fetch off M1 refused first
            refuse(lambda: rc(d / "c7" / "rf.npz", mid=m_), "M1 slot")
        lf.write_bytes(b"k1\tpatch0/c.jpg\n")
        refuse(lambda: rc(K.ROOT / "x_c7.npz", images=str(imgs)), "inside the repository")  # NB-3 (J2)
        urls, body = [], (imgs / "patch0/d.jpg").read_bytes()
        get = lambda u: urls.append(u) or ((body, "") if u.endswith(("val2014_000000000005.jpg",  # noqa: E731
                                                                     "val2017/000000000006.jpg")) else (None, "404"))
        got7, lost7 = fetch_set(read_list(b"5\tcoco2014\n6\tval2017\n7\tcoco2014\n"), d / "shm" / "r2", get)
        assert [i for i, _ in got7] == ["5", "6"] and lost7 == 1 and len(urls) == 5, urls
        assert urls[0].endswith("/train2014/COCO_train2014_000000000005.jpg") and "cocodataset.org" in urls[0]
        w25.drop(d / "shm" / "r2", d / "deletions.log", "after C7 r2")
        assert "(2 files)" in (d / "deletions.log").read_text() and not (d / "shm" / "r2").exists()
        refuse(lambda: coco_urls("abc", "coco2014"), "COCO id")
        refuse(lambda: coco_urls("5", "train2017"), "COCO id")
        assert [u.rsplit("/", 2)[1:] for u in coco_urls("5", "val2014")] == [["val2014", "COCO_val2014_000000000005.jpg"]]
        assert [u.rsplit("/", 2)[1:] for u in coco_urls("5", "train2014")] == [["train2014", "COCO_train2014_000000000005.jpg"]]

        # caches: K1 holds frame image a (C1 byte copy); K2 an SSCD-only copy of b (C3); K3 a far row, 1 unreadable
        fa = BM.features([imgs / "patch0/a.jpg"], pt, workers=1)
        w25.save(d / "k1.npz", [7], fa)
        y = w25.load(parts / "part_0000.npz")
        far = ~np.uint64(0)
        k2 = {"sha": ["s2"], **{k: np.array([far], np.uint64) for k in w25.KEYS[:4]}, "sscd": y["sscd"][1:2],
              "unreadable": []}
        w25.save(d / "k2.npz", [5], k2)
        k3 = {"sha": ["s3", "s4"], **{k: np.array([far, 0], np.uint64) for k in w25.KEYS[:4]},
              "sscd": -y["sscd"][:2], "unreadable": [1]}
        w25.save(d / "k3.npz", [8, 9], k3)
        cache = {k: {"path": str(d / f"{k.lower()}.npz"), "src": src, "n": n, "coco": True,
                     "sha256": K.sha_file(d / f"{k.lower()}.npz")} for k, src, n in
                 (("K1", "x.py", 1), ("K2", "LOG", 1), ("K3", "y.py", 1))}

        # overlay (§A.7) from a small R5 text: verbatim cells, K and G tokens, every guard
        def r5(cache=cache, k1_rows="1 image", owners_rows=""):
            a2 = "".join(f"| {k} `{c['path'] if k != 'K2' else '.../k2.npz'}` | `{c['sha256'][:8]}` | pin {k} | "
                         f"{k1_rows if k == 'K1' else '1 image'} | env |\n" for k, c in cache.items())
            return ("# R5\n### A.2 When\n\n| cache | sha256 | pin | coverage | fn |\n|---|---|---|---|---|\n"
                    + a2 + "\n### A.3 Pre\n\n### A.4 Owner table\n\n"
                    "| # | owner | status | space | g1 | source | spent | rule |\n"
                    "|---|---|---|---|---|---|---|---|\n| 1 | own_a | held (3) | coco | pool | K1 | — | G1 |\n"
                    "| 2 | own_b | held (3) | coco | pool | K1 ∪ K2 ∪ K3 by id; gap → M1 slot | none | "
                    "G1; gap **G3** |\n"
                    "| 3 | own_k | held (1) | ktvic | n/a | K2 by id | — | as #2 |\n" + owners_rows +
                    "| 4 | own_x | not yet written | mixed | exempt (W3) | — | — | owner for every later pass |\n"
                    "| c1 | X test (conditional) | builder: skipped | — | n/a | none | — | G4 conditional |\n"
                    "\n### A.5 Slots\n")
        okeys = ["own_a", "own_b", "own_k", "own_x"]
        ov = overlay(r5(), okeys, cache)
        assert overlay_bytes(ov) == overlay_bytes(overlay(r5(), okeys[::-1], dict(reversed(cache.items()))))
        assert ov["owners"]["own_b"]["caches"] == ["K1", "K2", "K3"] and ov["owners"]["own_b"]["rules"] == ["G1", "G3"]
        assert ov["owners"]["c1"]["rules"] == ["G4"] and ov["caches"]["K2"]["path_r5"] == ".../k2.npz"
        assert ov["owners"]["own_k"]["rules"] == ["G1", "G3"] and ov["owners"]["own_k"]["rule"] == "as #2"
        assert '"ids"' not in overlay_bytes(ov).decode()
        assert ov["owners"]["own_x"]["rules"] == [] and ov["owners"]["own_x"]["caches"] == []
        refuse(lambda: overlay(r5(), okeys[:2], cache), "not the owners file's")
        refuse(lambda: overlay(r5(k1_rows="2 images"), okeys, cache), "differs from its R5")
        refuse(lambda: overlay(r5(), okeys, cache | {"K1": {**cache["K1"], "sha256": "0" * 64}}), "differs from its R5")
        refuse(lambda: overlay(r5(), okeys, cache | {"K2": {**cache["K2"], "path": "/x/other.npz"}}), "differs from")
        refuse(lambda: overlay(r5(), okeys, {k: cache[k] for k in ("K1", "K2")}), "are not")
        refuse(lambda: overlay(r5(owners_rows="| 5 | own_z | held | coco | pool | K7 | — | G1 |\n"), okeys, cache),
               "unknown cache")
        refuse(lambda: overlay(r5(owners_rows="| 5 | own_z | held | coco | pool | K1 | — | none |\n"), okeys, cache),
               "no rule")
        refuse(lambda: overlay(r5(owners_rows="| 5 | own_z | held | coco | pool | K1 | — | as #9 |\n"), okeys, cache),
               "no rule")
        refuse(lambda: overlay(r5(owners_rows="| 5 | own_z | coco | pool | K1 | — | G1 |\n"), okeys, cache), "cell")

        rules = d / "b_pa1_r5_rules.json"
        owners = {"own_a": [1, 2, 5, 8], "own_b": [5, 7, 9], "own_k": ["k1"]}  # own_a names K1 only
        odoc = {"owners": {k: {"id_space": "ktvic" if k == "own_k" else B.COCO, "status": "held", "n": len(v),
                               "ids": v, "ids_sha256": IC.sha_ids(v)} for k, v in owners.items()}}
        odoc["owners"]["own_x"] = {"id_space": "mixed", "status": "not-yet-written", "n": None, "exempt": "W3"}
        own = d / "owners.json"
        own.write_bytes(json.dumps(odoc).encode())
        osha = K.sha_file(own)
        rules.write_bytes(overlay_bytes(ov | {"owners_file": {"path": "o.json", "sha256": osha}}))
        rsha = K.sha_file(rules)
        log = d / "LOG.md"
        k2_line = f"2026-11-02T04:14:56Z OPS-1102b-k2-pin: gatekeeper LOG pin k2.npz {cache['K2']['sha256']}\n"
        log.write_text(f"{B.T_UTC} OPS-1-pin: PIN {rules.name} {rsha}\n" + k2_line)
        nolog = d / "LOG0.md"
        nolog.write_text(f"{B.T_UTC} OPS-1-pin: PIN {rules.name} {rsha}\n"
                         f"{B.T_UTC} | CC-226 | narrative: k2.npz {cache['K2']['sha256']}\n")  # no pin line

        # pins (CC-224r3 C3): owners file, overlay and its LOG line fail closed
        assert load_pinned(own, osha, rules, rsha, log)[1]["owners"]["own_a"]["rule"] == "G1"
        refuse(lambda: load_pinned(own, "0" * 64, rules, rsha, log), "not at its pin")
        refuse(lambda: load_pinned(own, osha, rules, "0" * 64, log), "no LOG line")
        refuse(lambda: load_pinned(own, osha, d / "missing.json", rsha, log), "no LOG line")
        refuse(lambda: load_pinned(own, osha, rules, rsha, d / "noLOG.md"), "no LOG line")
        narr = d / "LOGn.md"  # CC-226 NB-1: a narrative line with name and full sha is no pin
        narr.write_text(f"2026 CC-226 | read {rules.name} {rsha}\n")
        refuse(lambda: load_pinned(own, osha, rules, rsha, narr), "no LOG line")
        wl = d / "LOGw3.md"  # CC-226r2 W3: lines with PIN, name and full sha that are no gatekeeper pin
        for bad in B.pin_cases(rules.name, rsha)[1]:
            wl.write_text(bad + "\n" + k2_line)
            refuse(lambda: load_pinned(own, osha, rules, rsha, wl), "no LOG line")
        for bad in B.pin_cases("k2.npz", cache["K2"]["sha256"])[1]:
            wl.write_text(bad + "\n")
            assert not usable(ov["caches"]["K2"], wl), bad
        wl.write_text(B.pin_cases("k2.npz", cache["K2"]["sha256"])[0] + "\n")
        assert usable(ov["caches"]["K2"], wl)
        wl.write_text(k2_line.replace(cache["K2"]["sha256"], cache["K2"]["sha256"] + ","))  # LOG l.1171: sha + ","
        assert not usable(ov["caches"]["K2"], wl), "a sha with punctuation glued on is no pin"
        rules3 = d / "r3" / rules.name  # CC-226 NB-3 J6: an overlay not made from R5 9cb21917
        rules3.parent.mkdir()
        rules3.write_bytes(overlay_bytes(ov | {"owners_file": {"path": "o.json", "sha256": osha},
                                               "source": {**ov["source"], "sha256": "0" * 64}}))
        log3 = d / "LOG3.md"
        log3.write_text(f"{B.T_UTC} OPS-3-pin: PIN {rules.name} {K.sha_file(rules3)}\n")
        refuse(lambda: load_pinned(own, osha, rules3, K.sha_file(rules3), log3), "not R5's")
        odoc2 = {"owners": {**odoc["owners"], "own_new": odoc["owners"]["own_a"]}}
        own2 = d / "owners2.json"
        own2.write_bytes(json.dumps(odoc2).encode())
        rules2 = d / "r2" / rules.name
        rules2.parent.mkdir()
        rules2.write_bytes(overlay_bytes(ov | {"owners_file": {"path": "o.json", "sha256": K.sha_file(own2)}}))
        log2 = d / "LOG2.md"
        log2.write_text(f"{B.T_UTC} OPS-2-pin: PIN {rules.name} {K.sha_file(rules2)}\n")
        refuse(lambda: load_pinned(own2, K.sha_file(own2), rules2, K.sha_file(rules2), log2), "not R5's")

        # C3 coverage: ids of readable rows only; K2 only with its LOG pin; lists; owner ids sha; gap files
        lst = {"K1": {7}, "K2": {5}, "K3": {8, 9}}
        cov = lambda out, lg=log, ls=lst: run_coverage(out, own, osha, rules, rsha, lg, lambda k: ls[k])  # noqa
        got = cov(d / "cov")
        assert got["owners"] == {"own_a": [4, 2, 2, IC.sha_ids([1, 2])[:8]],  # 5, 8: K2, K3 by the §A.2 base (J7)
                                 "own_b": [3, 2, 1, IC.sha_ids([9])[:8]]}, got  # 9 = K3's unreadable row
        assert (d / "cov/gap_own_b.txt").read_text() == "9\n" and "own_k" not in got["owners"]
        assert K.sha_file(d / "cov/gap_own_a.txt") == IC.sha_ids([1, 2])
        got = cov(d / "cov2", nolog)  # no K2 LOG pin line: K2's id 5 falls in the gap
        assert got["owners"]["own_b"][2] == 2 and got["owners"]["own_a"][2] == 3, got  # own_a gap 1, 2, 5
        assert got["caches_used"] == ["K1", "K3"], got
        refuse(lambda: cov(d / "cov"), "exists")  # mkdir exist_ok=False: FileExistsError
        refuse(lambda: cov(d / "cov3", ls={**lst, "K3": {9}}), "readable ids")
        refuse(lambda: coco_ids({**ov["caches"]["K3"], "n": 2}), "readable ids")
        refuse(lambda: coco_ids({**ov["caches"]["K3"], "sha256": "0" * 64}), "differs from its pin")
        tam = {"owners": {**odoc["owners"], "own_a": {**odoc["owners"]["own_a"], "ids": [1, 2, 4, 8]}}}
        refuse(lambda: coverage(tam, ov, {}), "ids_sha256")

        # C5 decide: a -> K1 by C1, b -> K2 by C3, c and d survive; one look; every input pinned
        dec = lambda out, lg=log, fr=frame, pa=parts: run_decide(fr, pa, out, own, osha, rules, rsha, lg,  # noqa
                                                                 block=2)
        got = dec(d / "dec")
        rec = json.loads((d / "dec/w25_decide.json").read_text())
        assert (d / "dec/w25_excluded_ids.txt").read_text() == "100\n101\n" and got["n_survivors"] == 2, got
        assert rec["counts"]["K1"]["C1_C2_registered"] == 1 and rec["counts"]["K2"]["C3_sscd_0.75"] == 1, rec
        assert rec["counts"]["K3"]["excluded"] == 0 and rec["n_compared"] == {"K1": 1, "K2": 1, "K3": 1}
        assert got["excluded_sha256"] == K.sha_file(d / "dec/w25_excluded_ids.txt")
        assert B.cut(B.read_frame(frame.read_bytes()), K.sha_file(frame), rec,
                     (d / "dec/w25_excluded_ids.txt").read_bytes(), n=1, block=2)["slice_b"] == [103]
        refuse(lambda: dec(d / "dec"), "never overwritten")
        refuse(lambda: dec(d / "dec2", nolog), "no LOG pin line")
        refuse(lambda: run_decide(frame, parts, d / "dec3", own, "0" * 64, rules, rsha, log, block=2), "its pin")
        refuse(lambda: run_decide(frame, parts, d / "dec3", own, osha, rules, "0" * 64, log, block=2), "no LOG line")
        fr2 = d / "frame2.tsv"
        fr2.write_bytes(frame.read_bytes() + b"104\tpatch0/e.jpg\n")
        refuse(lambda: dec(d / "dec3", fr=fr2), "not block 0")
        forged = d / "forged"  # right frame sha in the meta, wrong ids
        forged.mkdir()
        w25.save(forged / "part_0000.npz", [100, 111], {**p0, "unreadable": []}, frame_sha256=K.sha_file(frame))
        refuse(lambda: dec(d / "dec3", pa=forged), "not block 0")
        gap = d / "gap"
        gap.mkdir()
        (gap / "part_0001.npz").write_bytes((parts / "part_0001.npz").read_bytes())
        refuse(lambda: dec(d / "dec3", pa=gap), "not blocks 0..n-1")
        nopar = d / "nopar"
        nopar.mkdir()
        for q in parts.glob("part_*.npz"):
            (nopar / q.name).write_bytes(q.read_bytes())
        refuse(lambda: dec(d / "dec3", pa=nopar), "parity record")
        assert not (d / "dec3").exists(), "a refused decide left its out-dir"

        # C5 with a C7 cache (CC-226 W1(b)): manifest + LOG pin line (sha, name, n=, list sha) + provenance
        man = d / "extra.json"
        mrec = {"path": str(r1), "sha256": K.sha_file(r1), "n": 1, "owners": ["own_k"]}
        man.write_text(json.dumps({"caches": {"R1": mrec}}))
        exp = {**EXPECT, "sscd_sha256": K.sha_file(Path(pt)), "freeze_sha256": "f" * 64}
        dx = lambda out, lg=log, e=exp, m=man: run_decide(frame, parts, out, own, osha, rules, rsha, lg,  # noqa
                                                          block=2, extra=m, expect=e)
        refuse(lambda: dx(d / "dx"), "no LOG pin line with its sha")
        logx = d / "LOGx.md"
        base = log.read_text()
        toks = ["n=1", "listed=3", "missing=1", "unreadable=1", "truncated=0", sha_bytes(lb)]
        for i_ in range(len(toks)):  # each count token and the list sha are required (CC-226r2 Ruling 3(a)(i))
            logx.write_text(base + B.pin_cases("r1.npz", mrec["sha256"], *toks[:i_], *toks[i_ + 1:])[0] + "\n")
            refuse(lambda: dx(d / "dx", logx), "no LOG pin line with its sha")
        good_x = B.pin_cases("r1.npz", mrec["sha256"], *toks)[0]
        for old in ["r1.npz", mrec["sha256"], *toks]:  # each token delimited: a longer one never counts
            logx.write_text(base + good_x.replace(f" {old}", f" {old}0") + "\n")
            refuse(lambda: dx(d / "dx", logx), "no LOG pin line with its sha")
        for bad in B.pin_cases("r1.npz", mrec["sha256"], *toks)[1]:  # W3 forms
            logx.write_text(base + bad + "\n")
            refuse(lambda: dx(d / "dx", logx), "no LOG pin line with its sha")
        logx.write_text(base + B.pin_cases("r1.npz", mrec["sha256"], *toks)[0] + "\n")
        refuse(lambda: dx(d / "dx", logx, {**exp, "freeze_sha256": EXPECT["freeze_sha256"]}), "provenance")
        for bad_m in ({**mrec, "sha256": "0" * 64}, {**mrec, "n": 2}, {**mrec, "owners": ["own_a"]}):
            man.write_text(json.dumps({"caches": {"R1": bad_m}}))
            refuse(lambda: dx(d / "dx", logx), "r1.npz")
        for bad_m in ({"K1": mrec}, {"R1": {**mrec, "owners": ["own_q"]}}):
            man.write_text(json.dumps({"caches": bad_m}))
            refuse(lambda: dx(d / "dx", logx), "manifest cache")
        man.write_text(json.dumps({"caches": {"R1": mrec}}))
        gx = dx(d / "dx", logx)
        rx = json.loads((d / "dx/w25_decide.json").read_text())
        assert (d / "dx/w25_excluded_ids.txt").read_text() == "100\n101\n102\n" and gx["n_survivors"] == 1, gx
        assert rx["caches_compared"] == ["K1", "K2", "K3", "R1"] and rx["extra_owner_coverage"] == \
            {"R1": {"own_k": [1, 1]}} and rx["inputs_sha256"]["R1"] == mrec["sha256"], rx
        mt = {"path": str(rt), "sha256": K.sha_file(rt), "n": 1, "owners": ["own_k"]}  # truncated > 0: judge first
        tt = ["n=1", "listed=1", "missing=0", "unreadable=0", "truncated=1", sha_bytes(lb)]
        logx.write_text(B.pin_cases("rt.npz", mt["sha256"], *tt)[0] + "\n")
        refuse(lambda: load_extra(mt, logx, exp), "truncated-judged=CC-")
        for tok in ("truncated-judged=CC-", "truncated-judged=CC-227;"):
            logx.write_text(B.pin_cases("rt.npz", mt["sha256"], *tt, tok)[0] + "\n")
            refuse(lambda: load_extra(mt, logx, exp), "truncated-judged=CC-")
        logx.write_text(B.pin_cases("rt.npz", mt["sha256"], *tt, "truncated-judged=CC-227")[0] + "\n")
        assert load_extra(mt, logx, exp)["ids"] == ["k1"]
        rg = d / "c7" / "rg.npz"  # NB-3 (J5): a list sha that is not 64 hex
        with contextlib.redirect_stderr(io.StringIO()):
            recompute(ok7[:1], 1, 0, pt, rg, provenance("rg", ["own_k"], "g" * 64, pt, "f" * 64),
                      features=lambda q, s_, workers, retry_truncated: BM.features(q, s_, workers=1))
        mg = {"path": str(rg), "sha256": K.sha_file(rg), "n": 1, "owners": ["own_k"]}
        logx.write_text(B.pin_cases("rg.npz", mg["sha256"], "n=1", "listed=1", "missing=0", "unreadable=0",
                                    "truncated=0", "g" * 64)[0] + "\n")
        refuse(lambda: load_extra(mg, logx, exp), "provenance")
        oid, xm = {7: "a", 8: "x"}, {"x"}
        k = {**w25.load(d / "k3.npz"), "ids": [7, 8], "unreadable": []}
        assert drop_xm(k, oid, xm)["ids"] == [7] and drop_xm(k, oid, xm)["sscd"].shape == (1, 512)
        c4 = {**ov["caches"]["K3"], "drop_xm": True}
        refuse(lambda: load_cache(c4, log, lambda: ({8: "x", 9: "y"}, {"x"})), "readable rows")
        assert load_cache({**c4, "n": 0}, log, lambda: ({8: "x", 9: "y"}, {"x"}))["ids"] == [9]
    print(json.dumps({"tier": B.LABEL, "selftest": "ok", "checks": ["C4-feats", "C4-parity-record", "C7-recompute",
                                                                     "overlay", "pins", "C3-coverage", "C5-decide",
                                                                     "C5-extra"]}))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("selftest")
    sp.add_parser("rules").add_argument("--out", type=Path, required=True, help="new file; never overwritten")
    sp.add_parser("coverage").add_argument("--out-dir", required=True, help="new directory")
    fe, pa, de = sp.add_parser("feats"), sp.add_parser("parity"), sp.add_parser("decide")
    for p in (fe, pa, de):
        p.add_argument("--frame", required=True)
        p.add_argument("--parts", required=True)
    for p in (fe, pa):
        p.add_argument("--images", required=True)
        p.add_argument("--sscd", required=True)
        p.add_argument("--workers", type=int, default=4)
    fe.add_argument("--blocks", type=int, required=True)
    de.add_argument("--out-dir", required=True, help="new directory, never overwritten")
    de.add_argument("--extra", help="manifest of pinned C7 caches {caches: {name: {path, sha256, n, owners}}}")
    rc = sp.add_parser("recompute")
    for f in ("--list", "--name", "--owners", "--sscd", "--out"):
        rc.add_argument(f, required=True)
    rc.add_argument("--workers", type=int, default=4)
    src = rc.add_mutually_exclusive_group(required=True)
    src.add_argument("--images", help="laptop: list rows are id TAB path under this folder")
    src.add_argument("--fetch", action="store_true", help="M1 slot: list rows are id TAB coco2014|train2014|val2014|val2017 (E-13)")
    a = ap.parse_args()
    if a.cmd == "selftest":
        return selftest()
    {"rules": cmd_rules, "coverage": cmd_coverage, "feats": cmd_feats, "parity": cmd_parity,
     "recompute": cmd_recompute, "decide": cmd_decide}[a.cmd](a)


if __name__ == "__main__":
    main()
