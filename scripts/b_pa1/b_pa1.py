#!/usr/bin/env python3
"""B-PA1-T1 owners builder (manuscript/prereg/2026-11-01_b_pa1_tier1/PREREG_DRAFT_v3_1.md, sha e9b30ca7, commit
5ff00c9; §5.3, §5.4; CC-217r3 NB5, NB8, NB11). TIER 1 / DEV-EXPLORE (B-PA1-T1). Laptop CPU, stdlib only, ids only.

    python3 -I scripts/b_pa1/b_pa1.py selftest            synthetic fixtures in memory: no repo data, no git
    python3 -I scripts/b_pa1/b_pa1.py owners --out F      b_pa1_owners.json (O_EXCL); only after the NB8 LOG line

`owners` reads every tracked source with `git show HEAD:` (never the working tree, which other agents edit) and the
untracked data files from disk at their pins. From a json that also holds captions it takes only the named id field of
each record (CAP_KEYS refused), and every id must match ID_RE, so no caption text reaches stdout or the output. The
owner names come from PORTFOLIO_3Y §2.3 at HEAD: every ledger row must map to an owner or a stated skip, and every
mapped row must still be there, else REFUSED (never a closed list). `id_first` is the §5.3 rule (CC-217r3 B-new-1).
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "grl"))  # -I drops the script folder; common and id_counts are stdlib only
import common as K  # noqa: E402  ROOT, COCO_RE, IMG_RE
import id_counts as IC  # noqa: E402  INPUTS (pins), counts(), check(), EXPECT, sha_ids()

LABEL = "TIER 1 / DEV-EXPLORE (B-PA1-T1)"
PREREG = "manuscript/prereg/2026-11-01_b_pa1_tier1/PREREG_DRAFT_v3_1.md"
PREREG_SHA = "e9b30ca74678a06b5d3bcc028cccf1231ccb390919a9516d1188b3e7cfa366fb"
PORTFOLIO = "manuscript/directions/PORTFOLIO_3Y_2026-10-29.md"
IC_REL, IC_SHA = "scripts/grl/id_counts.py", "0c590058a908c0683366e385b70c68ca77b4ff80902b7a1398f216ce6e55d859"
K_REL, K_SHA = "scripts/grl/common.py", "bbe7ee61f659b1a7bfc3cab418d83ed779b76187107708fef2d8ab44df0ad23a"
KV4224_SHA = "86d9386324e8cb34c4c7216e494b21da0cbcfe458702952b9ce261a9f608f8f9"  # MT4 PREREG §1 (CC-153 W10)
EX, EX_SHA = "manuscript/prereg/2026-10-21_dev_pools/exclusion.json", IC.INPUTS[
    "manuscript/prereg/2026-10-21_dev_pools/exclusion.json"]
#: record fields that hold or lead to caption, label or annotation text; never a path step or a field taken
CAP_KEYS = frozenset({"caption", "captions", "sentences", "sentids", "raw", "tokens", "annotations", "refs",
                      "references", "text", "label", "labels", "question", "questions", "answer", "answers"})
ID_RE = re.compile(r"[A-Za-z0-9_\-]{1,64}")
COCO, UNRESOLVED = "coco", "unresolved"
W8 = "W8 deferred W25 owner (§5.4): covered later against b_pa1_dev_contacts.json when it arrives; not a stop"
R5 = ("held nowhere: R5 fixes before any feature pass either a W8 deferred owner or a W16(a) 'not clean (a)' stop "
      "(CC-217r3 NB5); id_first refuses while this owner is COCO or unresolved")


# ------------------------------------------------------------------------------------------------ reading
def checked(b: bytes, rel: str, pin: str | None) -> bytes:
    if pin and hashlib.sha256(b).hexdigest() != pin:
        raise SystemExit(f"REFUSED: {rel} differs from its pin {pin[:8]}")
    return b


def read_repo(rel: str, pin: str | None) -> bytes:
    """HEAD bytes of a tracked file; an untracked file only from disk and only with a pin."""
    r = subprocess.run(["git", "-C", str(K.ROOT), "show", f"HEAD:{rel}"], capture_output=True)
    if r.returncode == 0:
        return checked(r.stdout, rel, pin)
    if not pin:
        raise SystemExit(f"REFUSED: {rel} is not committed at HEAD and has no pin")
    return checked((K.ROOT / rel).read_bytes(), rel, pin)


def no_cap(*keys) -> None:
    if bad := set(keys) & CAP_KEYS:
        raise SystemExit(f"REFUSED: caption/label field {sorted(bad)} requested")


def lines(col: int = 0, header: bool = False):
    return lambda b: [r.split("\t")[col] for r in b.decode().splitlines()[header:] if r.strip()]


def jpath(*keys, col: int | None = None):
    """A list reached by key steps (none may be a caption key); col takes one column of list rows."""
    no_cap(*keys)

    def f(b):
        o = json.loads(b)
        for k in keys:
            o = o[k]
        return [r if col is None else r[col] for r in o]
    return f


def pick(lst: str, *keys, where: tuple[str, str] | None = None):
    """Only the named non-caption fields of each record of o[lst]; the loader parses the rest, nothing reads it."""
    no_cap(lst, *keys, *(where[:1] if where else ()))

    def f(b):
        rows = [r for r in json.loads(b)[lst] if where is None or r[where[0]] == where[1]]
        return [r[keys[0]] if len(keys) == 1 else tuple(r[k] for k in keys) for r in rows]
    return f


def norm(space: str, x) -> int | str:
    """An id: COCO ids as ints (digit string or COCO file name, common.COCO_RE); else the file stem, ID_RE only."""
    if space == COCO:
        if type(x) is int and x >= 0:
            return x
        s = str(x)
        if s.isdigit():
            return int(s)
        if m := K.COCO_RE.fullmatch(Path(s).name):
            return int(m.group(1))
        raise SystemExit(f"REFUSED: a COCO-space entry is not a COCO id or file name ({len(s)} chars)")
    s = K.IMG_RE.sub("", str(x))
    if not ID_RE.fullmatch(s):
        raise SystemExit(f"REFUSED: a {space} entry is not an id ({len(s)} chars)")
    return s


# ------------------------------------------------------------------------------------------------ owners
def held(space: str, rel: str, pin: str, ex, n: int, **kw) -> dict:
    """An owner read from one pinned file; n = its distinct ids, from the counts already recorded for that list."""
    return {"space": space, "source": rel, "pin": pin, "n": n, "get": lambda read: ex(read(rel, pin)), **kw}


def nowhere(space: str, n: int | None, rule: str = R5, **kw) -> dict:
    return {"space": space, "n": n, "rule": rule, "status": "deferred" if rule == W8 else "held-nowhere", **kw}


def kv4224(read) -> list[int]:
    """KV-4,224 (kv4224.txt is not at HEAD): id_counts.counts() kv_pool_a_excluded over its pinned INPUTS, keys only;
    every id_counts count is checked, and the list must equal the MT4 PREREG §1 sha_ids pin."""
    b = {rel: read(rel, pin) for rel, pin in IC.INPUTS.items()}
    uv = {s: set(pick("images", "id")(b[f"data/datasets/uitviic/{s}_data.json"])) for s in ("train", "val")}
    kp = {int(c): s for c, s in pick("images", "cocoid", "split")(b["data/datasets/karpathy/dataset_coco.json"])}
    gt = json.loads(b[".session_backup/2026-10-14/r12_verify/gt_cache.json"])  # dict keys only, values never read
    touched = {int(k) for k in (*gt["refs"].keys(), *gt["inst"].keys(), *json.loads(
        b[".session_backup/2026-10-19/HL_human_labels/a_n3_instance_gold.json"]).keys())}
    cen = {k: {int(i) for i in lines(header=True)(b[f"manuscript/prereg/2026-10-27_c_en/cen_coco_{k}.tsv"])}
           for k in ("kval", "test")}
    got, pools = IC.counts({int(i) for i in uv["train"]}, {int(i) for i in uv["val"]}, kp,
                           json.loads(b[EX])["ids"]["coco"], touched, cen)
    IC.check(got, IC.EXPECT)
    if IC.sha_ids(pools["kv_pool_a_excluded"]) != KV4224_SHA:
        raise SystemExit("REFUSED: derived KV-4,224 differs from the MT4 PREREG §1 pin 86d93863")
    return sorted(pools["kv_pool_a_excluded"])


M0, GRL = "manuscript/prereg/2026-10-31_vsps_j_m0/", "manuscript/prereg/2026-10-27_grl_pilot/"
OWNERS = {  # PORTFOLIO §2.3 at HEAD + prereg §5.4 "at least" list; shas = HEAD bytes on 2026-11-02 (prefixes as cited)
    "kv4224_mt4": {"space": COCO, "source": f"{IC_REL} kv_pool_a_excluded", "pin": IC_SHA, "n": 4224, "get": kv4224,
                   "note": "kv4224.txt not at HEAD; derived, ids_sha256 = MT4 PREREG §1 pin"},
    "karpathy_test_5000": held(COCO, EX, EX_SHA, jpath("ids", "coco", "coco_karpathy_test"), n=5000),
    "m0_karpathy_test_probes_91": held(COCO, M0 + "karpathy_test_val_ids.txt",
                                      "88e40e3cd2ae6dd3bf3c1f514a085cb61a36b503abde298d57a1bb2bc8acd7fb", lines(),
                                      n=91),
    "m0_dev_touched_3454": held(COCO, M0 + "dev_touched_ids.txt",
                                "91db7e2fbb3d479f79ed19fca4aa100399730910cd7511f832576350f26f9b63", lines(), n=3454),
    "a_t3_val2017": held(COCO, "manuscript/prereg/2026-10-30_a_t3/val2017_ids.txt",
                         "ea37cee007069bde6d45a67186cc6c2591d0c6d7effd3c481996b6b367e060b6", lines(), n=5000,
                         features="held nowhere (never the laptop, §5.4): R5 fixes W8 deferred owner or W16(a) "
                                  "'not clean (a)' stop (CC-217r3 NB5)"),
    "uitviic_test_231": held(COCO, EX, EX_SHA, jpath("ids", "coco", "uitviic_test"), n=231),
    "uitviic_val_924": held(COCO, GRL + "val924.txt", K.PINS[GRL + "val924.txt"], lines(), n=924),
    "uitviic_train_pool": held(COCO, "data/datasets/uitviic/train_data.json",
                               IC.INPUTS["data/datasets/uitviic/train_data.json"], pick("images", "id"), n=2695),
    "ut2402": held(COCO, GRL + "ut2402.txt", K.PINS[GRL + "ut2402.txt"], lines(), n=2402),
    "coco_restval_b4": held(COCO, "data/datasets/karpathy/dataset_coco.json",
                            IC.INPUTS["data/datasets/karpathy/dataset_coco.json"],
                            pick("images", "cocoid", where=("split", "restval")), n=30504),
    **{f"refused_{k}": held(COCO, EX, EX_SHA, jpath("ids", "coco", k), n=n, note="exclusion.json refused list")
       for k, n in (("coco2500", 2500), ("cv295", 295), ("chair500", 500), ("pope500", 500))},
    **{k: nowhere(UNRESOLVED, None, note="PORTFOLIO §2.3 dev-only (spent) line") for k in ("longcap", "thumb", "vapr")},
    "docci": nowhere("docci", None, note="PORTFOLIO §2.3 dev-only (spent) line"),
    "xm3600_all": held("openimages", "data/datasets/xm3600/full_data.json",
                       "101d24ad98e9dec43625ee425fa1b49aa1bde98f9609945bf5dd4424fef1dacc", pick("images", "id"),
                       n=3600),
    "xm600_a": held("openimages", EX, EX_SHA, jpath("ids", "xm3600", "xm600_test_data_json"), n=600),
    "xm_test2500_c": held("openimages", "manuscript/prereg/2026-10-22_c_stage1/lists.json",
                          "5c479f03e8be544f4cd12b5d997b5dc92b6c622df061760cd02f6ba82f6b4371",
                          jpath("sets", "xm_test2500", col=0), n=2500),
    "oiv7_val": held("openimages", "manuscript/prereg/2026-10-28_w25_neardup/oiv7_val_ids.txt",
                     "4b7a1813487dc5d74a5bd4aca7c36d0f6d2d3042d9cc6cf4091180dc473eabb0", lines(), n=41620,
                     note="all 41,620; the L2-P1 ledger set is this minus the 456 XM ids"),
    "nocaps_val": held("openimages", "manuscript/prereg/2026-10-27_c_en/cen_nocaps_val.tsv",
                       "6add90eb421523cdd65f47a8f9789f9342421b2b28169dc013f863f1edd0dfac", lines(1, header=True),
                       n=4500),
    "nocaps_test_c": nowhere("openimages", 10600, W8),
    "textvqa_textcaps_val": nowhere("openimages", None),
    "ov_test_c": held("openviic", "manuscript/prereg/2026-10-25_c_test/ov_test_files.tsv",
                      "99d4fc49cc8283d1555d37b975cca5a32598ea0ec571d8bef8cf811df2c33695", lines(), n=2001),
    "ktvic_test_558": held("ktvic", EX, EX_SHA, jpath("ids", "ktvic", "ktvic_test"), n=558),
    "refused_ktvic_dev_near_duplicate_of_test": held("ktvic", EX, EX_SHA,
                                                     jpath("ids", "ktvic", "ktvic_dev_near_duplicate_of_test"), n=1),
    "h500": nowhere("ktvic", 500, note="no list built at HEAD; ledger owner B, prereg l.302 lists it with A's tests"),
    "flickr30k_test_c": held("flickr30k", "manuscript/prereg/2026-10-30_c_t1/c_t1_f30k_lists.json",
                             "eebcd95b78b1dc98398550b1f89fea5622e8cbd9f20ad6b07b0d9292ba745968",
                             jpath("refuse", "test"), n=1000),
    "pascal50s_a": held("pascal_voc2008", "scripts/pascal50s/p50_1000_ids.txt",
                        "a8539efbc785e6ce9b977f7f8fc977adb039f4cc52bb1c437c4980c26c034cb4", lines(), n=1000),
    "ade20k_val_a": nowhere("ade20k", 2000),
    "amber_generative": nowhere(UNRESOLVED, 1004),
    "openvivqa_dev_c": nowhere("openvivqa", 1070, W8),
    "vitextvqa_test": nowhere("vitextvqa", None),
    "mtvqa_test": nowhere("mtvqa", None),
    "vintext_test": nowhere("vintext", None),
    "viocrvqa_test": nowhere("viocrvqa", None),
    "visignvqa_test": nowhere("visignvqa", None),
    "vindr_cxr_test": nowhere("vindr_cxr", 3000),
    "vizwiz_val": nowhere("vizwiz", 7750),
    "b_pa1_dev_contacts": {"space": "mixed", "n": None, "status": "not-yet-written", "exempt": "W3",
                           "rule": "§3, N11: B's own dev contacts; an owner for every later W25 pass, not this one"},
}
NB5_SKIP = "skip: CC-217r3 NB5, stale C owner name dropped (C refreshed to NoCaps test, OpenViVQA dev)"
LEDGER = {  # PORTFOLIO §2.3 table row (first cell, verbatim at HEAD) -> owner key, or a skip with its reason
    "PASCAL-50S": "pascal50s_a",
    "KV-4,224 (COCO Karpathy val)": "kv4224_mt4",
    "ViTextCaps test": NB5_SKIP,
    "NoCaps test (10,600; EvalAI)": "nocaps_test_c",
    "OpenViVQA dev (1,070 images / 3,545 QA)": "openvivqa_dev_c",
    "VieCap4H private test": NB5_SKIP,
    "Flickr30K Karpathy test": "flickr30k_test_c",
    "H = 500 KTVIC-train ∩ OV-train-only": "h500",
    "ADE20K SceneParsing val (2,000) + LN-ADE val": "ade20k_val_a",
    "AMBER generative (1,004)": "amber_generative",
    "OIV7 val − 456 XM ids (41,164)": "oiv7_val",
    "COCO Karpathy restval (about 30.5k) + VG relations": "coco_restval_b4",
    "Objects365 v2 val": "skip: B's own one-look set, sealed in tiers 1-2 (§3); never its own owner (W3)",
    "ViTextVQA test (about 10k QA)": "vitextvqa_test",
    "MTVQA test vi/fr/de/it": "mtvqa_test",
    "TextVQA val / TextCaps val": "textvqa_textcaps_val",
    "VinText test": "vintext_test",
    "ViOCRVQA test": "viocrvqa_test",
    "ViSignVQA test": "visignvqa_test",
    "VinDr-CXR test (3,000)": "vindr_cxr_test",
    "VizWiz val (7,750)": "vizwiz_val",
    "UIT-ViIC train pool": "uitviic_train_pool",
}


def ledger_rows(text: str) -> list[str]:
    """First cells of the PORTFOLIO §2.3 table (header dropped)."""
    if "\n### 2.3 " not in text:
        raise SystemExit("REFUSED: PORTFOLIO has no §2.3")
    sec = text.split("\n### 2.3 ", 1)[1].split("\n### ", 1)[0]
    return [r.split("|")[1].strip() for r in sec.splitlines() if r.startswith("| ")][1:]


def walk_keys(o) -> set[str]:
    if isinstance(o, dict):
        return set(o).union(*map(walk_keys, o.values()))
    return set().union(*map(walk_keys, o)) if isinstance(o, list) else set()


def build(owners: dict, ledger: dict, read) -> bytes:
    rows = ledger_rows(read(PORTFOLIO, None).decode())
    if set(rows) != set(ledger) or len(rows) != len(set(rows)):
        raise SystemExit(f"REFUSED: PORTFOLIO §2.3 rows changed; unmapped {sorted(set(rows) - set(ledger))}, "
                         f"gone {sorted(set(ledger) - set(rows))}")
    if bad := [v for v in ledger.values() if not v.startswith("skip:") and v not in owners]:
        raise SystemExit(f"REFUSED: ledger maps to unknown owners {bad}")
    out = {}
    for k in sorted(owners):
        o, rec = owners[k], {"id_space": owners[k]["space"]}
        if "get" in o:
            ids = sorted({norm(o["space"], x) for x in o["get"](read)})
            if len(ids) != o["n"]:
                raise SystemExit(f"REFUSED: owner {k} has {len(ids)} distinct ids, expected {o['n']}")
            rec.update(status="held", source=o["source"], source_sha256=o["pin"], n=len(ids), ids=ids,
                       ids_sha256=IC.sha_ids(ids))
        else:
            rec.update(status=o["status"], n=o["n"], rule=o["rule"])
        rec.update({x: o[x] for x in ("features", "exempt", "note") if x in o})
        out[k] = rec
    doc = {"schema": "vsps.b_pa1.owners.v1", "tier": LABEL,
           "prereg": {"path": PREREG, "sha256": hashlib.sha256(read(PREREG, PREREG_SHA)).hexdigest()},
           "portfolio": {"path": PORTFOLIO, "sha256": hashlib.sha256(read(PORTFOLIO, None)).hexdigest()},
           "ledger": ledger, "owners": out}
    if bad := walk_keys(doc) & CAP_KEYS:
        raise SystemExit(f"REFUSED: caption key {sorted(bad)} in the output")
    return (json.dumps(doc, sort_keys=True, separators=(",", ":")) + "\n").encode()


def id_first(doc: dict, names) -> tuple[list, list]:
    """§5.3/§5.4 id-first rule (CC-217r3 B-new-1): ids or COCO file names of Composite-COCO or Polaris-test-COCO
    against every COCO-id-space owner of b_pa1_owners.json, on the laptop, before any image is staged. A's
    Composite/Polaris lists are no owners here (W3). Returns (survivors, excluded). W16(a): a COCO or unresolved owner
    held nowhere refuses."""
    pool: set = set()
    for k, o in sorted(doc["owners"].items()):
        if o.get("exempt") or o["id_space"] not in (COCO, UNRESOLVED) or o["status"] == "deferred":
            continue
        if o["status"] != "held":
            raise SystemExit(f"NOT CLEAN (a): owner {k} ({o['id_space']}) is held nowhere; the R5 rule comes first")
        if len(o["ids"]) != o["n"] or IC.sha_ids(o["ids"]) != o["ids_sha256"]:
            raise SystemExit(f"REFUSED: owner {k} ids differ from its ids_sha256")
        pool.update(o["ids"])
    cand = {norm(COCO, x) for x in names}
    return sorted(cand - pool), sorted(cand & pool)


def cmd_owners(a) -> int:
    for m, rel, pin in ((K, K_REL, K_SHA), (IC, IC_REL, IC_SHA)):  # the imported helpers, at their HEAD shas
        checked(Path(m.__file__).read_bytes(), rel, pin)
    data = build(OWNERS, LEDGER, read_repo)
    fd = os.open(a.out, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(fd, "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    doc = json.loads(data)
    print(json.dumps({"tier": LABEL, "sha256": hashlib.sha256(data).hexdigest(),
                      "owners": {k: [o["status"], o["n"]] for k, o in doc["owners"].items()}}))
    return 0


# ------------------------------------------------------------------------------------------------ slices (C6)
SALT, BLOCK, SLICE_N = "b-pa1-o365-slice|", 500, 2000  # v3.1 §5.2 l.252-254
FRAME_PATCHES = ("patch0", "patch1")  # v3.1 §5.2 O7
PATCH_RE = re.compile(r"patch\d+")
LOG = K.ROOT / ".session_backup/2026-10-13/decisions/LOG.md"
ANN_NAME = "zhiyuan_objv2_train.json"  # R6: the train annotation file; never the sealed val json (CC-226 W2)
#: CC-226r2 W3: a pin is only a gatekeeper line laid out as LOG l.1171 / l.1196: "<UTC stamp> OPS-<id>-pin: ..."
PIN_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z OPS-[0-9A-Za-z-]+-pin: ")


def delimited(t) -> re.Pattern:
    """A token (str, or a re.Pattern for a family such as truncated-judged=CC-<id>) that stands alone on the line:
    whitespace or the line's start / end on both sides, so missing=1 never matches missing=10, nor a sha a longer
    hex."""
    return re.compile(rf"(?<!\S)(?:{t.pattern if isinstance(t, re.Pattern) else re.escape(t)})(?!\S)")


def pin_line(log: Path, sha: str, name: str, *also) -> bool:
    """One LOG pin line (PIN_RE at the line start) carries the file name, the full sha and every `also` token, each
    delimited. Judges and narrative lines cite B shas by 8-character prefix and never match (CC-226r2 W3)."""
    if len(sha) != 64 or not log.is_file():
        return False
    toks = [delimited(t) for t in (sha, name, *also)]
    return any(PIN_RE.search(ln) and all(t.search(ln) for t in toks)
               for ln in log.read_text(encoding="utf-8").splitlines())


def plain(i, f) -> bool:
    """A non-negative int id and a relative '/' file name with no '..' part and no tab or newline."""
    return (type(i) is int and i >= 0 and type(f) is str and bool(f) and not f.startswith("/")
            and ".." not in f.split("/") and "\t" not in f and "\n" not in f)


def frame_of(fh) -> tuple[list[tuple[int, str]], dict]:
    """v3.1 §5.2: the sampling frame in slice order. ijson streams `images[]` and only `id` and `file_name` of each
    record are kept; `annotations[]` is never built. Frame = the images in patch0 or patch1 (a file-name path part);
    all images if no file name has a patch part; REFUSED if only some do. Order = ascending sha256(SALT + file_name)."""
    import ijson  # R2: version pinned in the venv freeze; the rest of b_pa1.py stays stdlib

    rows = []
    for im in ijson.items(fh, "images.item"):
        if not plain(i := im.get("id"), f := im.get("file_name")):
            raise SystemExit("REFUSED: an images[] record has no plain int id or relative file_name")
        rows.append((i, f))
    tags = [[p for p in f.split("/") if PATCH_RE.fullmatch(p)] for _, f in rows]
    patched = sum(map(bool, tags))
    if not rows or any(len(t) > 1 for t in tags) or 0 < patched < len(rows):
        raise SystemExit(f"REFUSED: patch parts unclear ({patched} of {len(rows)} file names have one)")
    keep = [r for r, t in zip(rows, tags) if not patched or t[0] in FRAME_PATCHES]
    if not keep or len({i for i, _ in keep}) != len(keep) or len({f for _, f in keep}) != len(keep):
        raise SystemExit("REFUSED: the frame is empty or repeats an id or a file_name")
    keep.sort(key=lambda r: hashlib.sha256((SALT + r[1]).encode()).hexdigest())
    return keep, {"n_images": len(rows), "n_frame": len(keep), "patched": bool(patched)}


def read_frame(b: bytes) -> list[tuple[int, str]]:
    """The frame file of `slices frame` (id TAB file_name per line, slice order); also read by b_pa1_w25.py."""
    rows = [r.split("\t") for r in b.decode().splitlines()]
    if any(len(r) != 2 or not r[0].isdigit() or not plain(int(r[0]), r[1]) for r in rows) or \
            len({r[0] for r in rows}) != len(rows):
        raise SystemExit("REFUSED: not a frame file (id TAB relative file_name, ids distinct)")
    return [(int(i), f) for i, f in rows]


def cut(frame: list, frame_sha: str, rec: dict, excluded: bytes, n: int = SLICE_N, block: int = BLOCK) -> dict:
    """v3.1 §5.2: slice A = the first n W25 survivors along the frame order, slice B = the next n, from the C5 decide
    record of this frame (b_pa1_w25.py decide); disjoint by construction (frame ids are distinct)."""
    if rec.get("frame_sha256") != frame_sha or rec.get("excluded_sha256") != hashlib.sha256(excluded).hexdigest():
        raise SystemExit("REFUSED: the decide record is not of this frame or of this exclusion list")
    gone = {int(x) for x in excluded.split()}
    surv = [i for i, _ in frame[:rec["n_frame_decided"]] if i not in gone]
    if len(surv) < 2 * n:
        raise SystemExit(f"REFUSED: {len(surv)} W25 survivors in the decided blocks, {2 * n} needed; feature more "
                         "blocks (C4)")
    last = [i for i, _ in frame].index(surv[2 * n - 1])
    return {"slice_a": surv[:n], "slice_b": surv[n:2 * n], "n_blocks_used": last // block + 1}


def missing_members(frame: list, tars: list[Path]) -> dict:
    """CC-226 NB-6, names only: frame file names whose last two parts (patchN/file) are no file member of the patch
    tars. Member headers are listed; no member is extracted or read."""
    import tarfile

    have = set()
    for t in tars:
        with tarfile.open(t, "r:*") as tf:
            have |= {"/".join(m.name.split("/")[-2:]) for m in tf if m.isfile()}
    return {"n_frame": len(frame), "n_members": len(have),
            "missing": sum("/".join(f.split("/")[-2:]) not in have for _, f in frame)}


def write_new(p: Path, data: bytes) -> None:
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(fd, "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())


def cmd_slices(a, log: Path = LOG) -> int:
    if a.op == "selftest":
        return slices_selftest()
    sha = lambda b: hashlib.sha256(b).hexdigest()  # noqa: E731
    if a.op == "frame":  # R6: the file name, its sha = --ann-sha, and that sha on a LOG pin line (CC-226 W2)
        if a.ann.name != ANN_NAME or K.sha_file(a.ann) != a.ann_sha or not pin_line(log, a.ann_sha, ANN_NAME):
            raise SystemExit(f"REFUSED: not the R6-pinned {ANN_NAME} (name, --ann-sha, LOG pin line)")
        with open(a.ann, "rb") as fh:
            rows, rec = frame_of(fh)
        data = "".join(f"{i}\t{f}\n" for i, f in rows).encode()
        write_new(a.out, data)
        print(json.dumps({"tier": LABEL, **rec, "sha256": sha(data)}))
        return 0
    if a.op == "members":
        rec = missing_members(read_frame(a.frame.read_bytes()), a.tar)
        print(json.dumps({"tier": LABEL, **rec}))
        if rec["missing"]:
            raise SystemExit(f"FAULT: {rec['missing']} frame file names are no tar member; to a judge before block W")
        return 0
    fb, db = a.frame.read_bytes(), (a.decide / "w25_decide.json").read_bytes()
    # CC-226 W1(c), CC-226r2 Ruling 3(a)(ii): the gatekeeper writes this 'P6 met' pin only when every G3 owner has 0
    # residual gap (C3 gap minus its ids readable in a pinned C7 cache) or a one-judge ruling covers the residual.
    if not pin_line(log, sha(db), "w25_decide.json", "P6 met"):
        raise SystemExit("REFUSED: no LOG pin line says 'P6 met' for this w25_decide.json")
    lists = cut(read_frame(fb), sha(fb), json.loads(db), (a.decide / "w25_excluded_ids.txt").read_bytes())
    data = (json.dumps({"schema": "vsps.b_pa1.lists.v1", "tier": LABEL, "frame_sha256": sha(fb),
                        "decide_sha256": sha(db), **lists}, sort_keys=True, separators=(",", ":")) + "\n").encode()
    write_new(a.out, data)
    print(json.dumps({"tier": LABEL, "slice_a": len(lists["slice_a"]), "slice_b": len(lists["slice_b"]),
                      "n_blocks_used": lists["n_blocks_used"], "sha256": sha(data)}))
    return 0


# ------------------------------------------------------------------------------------------------ selftest
def must_refuse(fn, word: str) -> None:
    try:
        fn()
    except SystemExit as e:
        assert word in str(e), e
    else:
        raise AssertionError(f"accepted; expected {word}")


def selftest() -> int:
    sent = "SENTINEL caption xyzzy"
    sha = lambda b: hashlib.sha256(b).hexdigest()  # noqa: E731
    port = ("# P\n### 2.3 Test-set ledger\n\n| Set | Gold |\n|---|---|\n| KV | x |\n| Own | x |\n| Txt | x |\n\n"
            "### 2.4 next\n").encode()
    files = {PORTFOLIO: port, PREREG: b"prereg\n", "kv.txt": b"9\n3\n1\n",
             "ex.json": json.dumps({"ids": {"coco": {"t": [7, 3]}, "ktvic": {"t": ["5"]}}}).encode(),
             "cap.json": json.dumps({"images": [{"id": 11, "split": "a"}, {"id": 12, "split": "b"}],
                                     "annotations": [{"image_id": 11, "caption": sent}]}).encode(),
             "rows.json": json.dumps({"sets": {"s": [["0a1b", "0a1b.jpg", "f" * 64]]}}).encode(),
             "lead.json": json.dumps({"images": [{"id": 1, "note": sent}]}).encode()}
    pins = {k: sha(v) for k, v in files.items()}

    def fx_read(fs):  # the fixture prereg stands in for the registered one, at its own pin
        return lambda rel, pin: checked(fs[rel], rel, pins[PREREG] if rel == PREREG else pin)

    def spec(order=1):
        s = {"kv": held(COCO, "kv.txt", pins["kv.txt"], lines(), n=3),
             "ex_coco": held(COCO, "ex.json", pins["ex.json"], jpath("ids", "coco", "t"), n=2),
             "ex_ktvic": held("ktvic", "ex.json", pins["ex.json"], jpath("ids", "ktvic", "t"), n=1),
             "cap": held(COCO, "cap.json", pins["cap.json"], pick("images", "id", where=("split", "a")), n=1),
             "rows": held("openimages", "rows.json", pins["rows.json"], jpath("sets", "s", col=0), n=1),
             "far": nowhere("openvivqa", 10, W8),
             "own": {"space": COCO, "n": None, "status": "not-yet-written", "exempt": "W3", "rule": "r"}}
        return dict(list(s.items())[::order])
    led = {"KV": "kv", "Own": "own", "Txt": "skip: test"}

    # determinism: owner order, ledger order and source line order never change the bytes; canonical form
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        a = build(spec(), led, fx_read(files))
        b = build(spec(-1), dict(reversed(led.items())), fx_read(files))
    doc = json.loads(a)
    assert a == b == (json.dumps(doc, sort_keys=True, separators=(",", ":")) + "\n").encode(), "determinism"
    assert doc["owners"]["kv"]["ids"] == [1, 3, 9] and doc["owners"]["cap"]["ids"] == [11], doc["owners"]
    assert doc["owners"]["ex_ktvic"]["ids"] == ["5"] and doc["owners"]["rows"]["ids"] == ["0a1b"]
    assert doc["owners"]["kv"]["ids_sha256"] == IC.sha_ids([1, 3, 9]) and doc["owners"]["far"]["status"] == "deferred"
    perm = files | {"kv.txt": b"3\n1\n9\n"}
    c = json.loads(build(spec() | {"kv": held(COCO, "kv.txt", sha(perm["kv.txt"]), lines(), n=3)}, led, fx_read(perm)))
    c["owners"]["kv"]["source_sha256"] = pins["kv.txt"]
    assert c == doc, "source line order"

    # no caption: the sentinel never reaches stdout or the bytes; caption keys and non-id values are refused
    assert sent.encode() not in a and sent not in buf.getvalue() and "xyzzy" not in buf.getvalue()
    for bad in (lambda: pick("annotations", "image_id"), lambda: pick("images", "caption"),
                lambda: jpath("annotations", "x"), lambda: pick("images", "id", where=("caption", "x"))):
        must_refuse(bad, "caption")
    leak = spec() | {"lead": held(COCO, "lead.json", pins["lead.json"], pick("images", "note"), n=1)}
    must_refuse(lambda: build(leak, led, fx_read(files)), "not a COCO id")
    leak2 = spec() | {"lead": held("x", "lead.json", pins["lead.json"], pick("images", "note"), n=1)}
    must_refuse(lambda: build(leak2, led, fx_read(files)), "not an id")

    # pins and the ledger fail closed
    must_refuse(lambda: build(spec(), led, fx_read(files | {"kv.txt": b"1\n"})), "differs from its pin")
    must_refuse(lambda: build(spec(), led, fx_read(files | {PREREG: b"x"})), "differs from its pin")
    must_refuse(lambda: build(spec(), {"KV": "kv", "Own": "own"}, fx_read(files)), "unmapped ['Txt']")
    must_refuse(lambda: build(spec(), led | {"Gone": "kv"}, fx_read(files)), "gone ['Gone']")
    must_refuse(lambda: build(spec(), led | {"Txt": "nobody"}, fx_read(files)), "unknown owners")
    must_refuse(lambda: build(spec() | {"kv": held(COCO, "kv.txt", pins["kv.txt"], lines(), n=4)}, led,
                              fx_read(files)), "3 distinct ids, expected 4")
    must_refuse(lambda: build(spec() | {"captions": nowhere(COCO, 1, W8)}, led, fx_read(files)), "caption key")
    assert all(v.startswith("skip:") or v in OWNERS for v in LEDGER.values()), "LEDGER -> OWNERS"
    assert not any(o.get("space") == COCO and o.get("status") == "held-nowhere" for o in OWNERS.values())

    # id-first (§5.3): COCO ids and file names match COCO owners only; a KTVIC "5" and the exempt owner never match
    surv, drop = id_first(doc, [1, "3", "COCO_val2014_000000000011.jpg", "000000000007.jpg", 5, 12, 40])
    assert drop == [1, 3, 7, 11] and surv == [5, 12, 40], (surv, drop)
    own = json.loads(a)
    own["owners"]["own"].update(status="held", ids=[40], n=1, ids_sha256=IC.sha_ids([40]))
    assert id_first(own, [40]) == ([40], []), "W3 exempt owner matched"
    must_refuse(lambda: id_first(doc, ["Flickr_123.jpg"]), "not a COCO id")
    tam = json.loads(a)
    tam["owners"]["kv"]["ids"] = [1, 3, 8]
    must_refuse(lambda: id_first(tam, [1]), "differ from its ids_sha256")

    # held nowhere: a COCO or unresolved owner refuses (W16(a)); a W8 deferred owner does not
    for space in (COCO, UNRESOLVED):
        hn = json.loads(build(spec() | {"gap": nowhere(space, 5)}, led, fx_read(files)))
        assert hn["owners"]["gap"]["status"] == "held-nowhere" and hn["owners"]["gap"]["rule"] == R5
        must_refuse(lambda: id_first(hn, [1]), "NOT CLEAN (a)")
    w8 = json.loads(build(spec() | {"gap": nowhere(COCO, 5, W8)}, led, fx_read(files)))
    assert id_first(w8, [2]) == ([2], [])
    print(json.dumps({"tier": LABEL, "selftest": "ok", "checks": ["determinism", "no-caption", "pins-ledger",
                                                                 "id-first", "held-nowhere"]}))
    return 0


T_UTC = "2026-11-02T08:00:00Z"  # selftest stamp


def pin_cases(name: str, sha: str, *also: str) -> tuple[str, list[str]]:
    """Selftest LOG lines (CC-226r2 W3): one gatekeeper pin, and lines that carry PIN, the name, the full sha and every
    token but are no pin: CC format, non-pin OPS id, pin id not at the line start, narrative, non-OPS -pin id."""
    body = " ".join((name, sha, *also))
    return f"{T_UTC} OPS-9-pin: PIN {body}", [
        f"{T_UTC} | CC-999 | {body} is NOT a PIN; P6 met? no | NEXT_ROUND",
        f"{T_UTC} OPS-9-decide: PIN {body}",
        f"| {T_UTC} OPS-9-pin: PIN {body}",
        f"CC-999: OPS-9-pin: PIN {body}",
        f"{T_UTC} OPS-9-step1: extracted {body}; R6 PIN to follow",
        f"{T_UTC} CC-9-pin: PIN {body}"]


def slices_selftest() -> int:
    import tempfile
    from types import SimpleNamespace as NS

    sent = "SENTINEL caption xyzzy"
    order = lambda fs: sorted(fs, key=lambda f: hashlib.sha256(("b-pa1-o365-slice|" + f).encode()).hexdigest())  # noqa
    ims = [{"id": 1, "file_name": "images/v1/patch0/a.jpg", "height": 9},
           {"id": 2, "file_name": "images/v1/patch1/b.jpg"}, {"id": 3, "file_name": "images/v2/patch2/c.jpg"},
           {"id": 4, "file_name": "images/v1/patch0/d.jpg"}]
    ann = {"annotations": [{"image_id": 1, "note": sent}], "images": ims, "categories": [{"id": 1, "name": sent}]}
    js = lambda o: io.BytesIO(json.dumps(o).encode())  # noqa: E731

    # frame: patch0/patch1 only, slice order, annotations[] and categories[] never reach the output
    rows, rec = frame_of(js(ann))
    assert [f for _, f in rows] == order([im["file_name"] for im in ims if "patch2" not in im["file_name"]]), rows
    assert rec == {"n_images": 4, "n_frame": 3, "patched": True} and {i for i, _ in rows} == {1, 2, 4}
    flat = [{"id": i, "file_name": f"o_{i}.jpg"} for i in (5, 6)]
    assert frame_of(js({"images": flat}))[1]["n_frame"] == 2, "no patch parts: all images"
    for bad, word in (([*ims, *flat], "patch parts unclear"), ([{"id": 7, "file_name": "x/patch0/patch1/e.jpg"}],
                      "patch parts unclear"), ([{"id": "7", "file_name": "patch0/e.jpg"}], "no plain int id"),
                      ([{"id": 7, "file_name": "/patch0/e.jpg"}], "no plain int id"),
                      ([{"id": 7, "file_name": "patch0/../e.jpg"}], "no plain int id"),
                      ([{"id": 7, "file_name": "patch0/e\t.jpg"}], "no plain int id"),
                      ([{"id": 7, "file_name": "patch0/e.jpg"}, {"id": 8, "file_name": "patch0/e.jpg"}], "repeats"),
                      ([{"id": 7, "file_name": "patch2/e.jpg"}], "empty")):
        must_refuse(lambda: frame_of(js({"images": bad})), word)
    for bad in (b"1\tpatch0/a.jpg\n1\tpatch0/b.jpg\n", b"x\ta.jpg\n", b"1\t/a.jpg\n", b"1\n"):
        must_refuse(lambda: read_frame(bad), "not a frame file")

    with tempfile.TemporaryDirectory() as d:  # the frame command: R6 name, sha and LOG pin; new file only; no sentinel
        d = Path(d)
        ann_p, val_p, log = d / ANN_NAME, d / "zhiyuan_objv2_val.json", d / "LOG.md"
        for p in (ann_p, val_p):
            p.write_bytes(json.dumps(ann).encode())
        good = K.sha_file(ann_p)
        fr_cmd = lambda p=ann_p, s=good: cmd_slices(NS(op="frame", ann=p, ann_sha=s, out=d / "f.tsv"), log)  # noqa
        pin_ok, no_pins = pin_cases(ANN_NAME, good)
        for bad in [*no_pins, pin_cases(val_p.name, good)[0]]:  # right sha, no pin line naming the train json
            log.write_text(bad + "\n")
            must_refuse(lambda: fr_cmd(), "R6")
        log.write_text(pin_ok + "\n")
        must_refuse(lambda: fr_cmd(s="0" * 64), "R6")
        must_refuse(lambda: fr_cmd(p=val_p), "R6")  # the val json, even at a pinned sha
        other = d / "other" / ANN_NAME  # the right name and a pinned --ann-sha, but other bytes
        other.parent.mkdir()
        other.write_bytes(json.dumps({"images": flat}).encode())
        must_refuse(lambda: fr_cmd(p=other), "R6")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            fr_cmd()
        out = (d / "f.tsv").read_bytes()
        assert read_frame(out) == rows and sent not in buf.getvalue() and sent.encode() not in out
        with contextlib.suppress(FileExistsError):
            fr_cmd()
            raise AssertionError("the frame file was overwritten")
        assert pin_line(log, good, ANN_NAME) and not pin_line(log, good[:8], ANN_NAME)
        assert pin_line(d / "x", good, ANN_NAME) is False
        (d / "l1171.md").write_text(f"2026-11-02T04:14:56Z OPS-1102b-k2-pin: gatekeeper LOG pin x.npz {good}\n")
        assert pin_line(d / "l1171.md", good, "x.npz"), "the LOG l.1171 pin form"
        # delimited tokens: a longer token, a prefix of a longer hex, or punctuation glued on never counts
        ok_line = f"{T_UTC} OPS-9-pin: PIN x.npz {good} n=1 missing=1 P6 met"
        dl = d / "delim.md"
        dl.write_text(ok_line + "\n")
        assert pin_line(dl, good, "x.npz", "n=1", "missing=1", "P6 met")
        for old, new in ((" missing=1", " missing=10"), (" n=1", " n=10"), (good, good + "0"), (good, good + ","),
                         (good, "0" + good), (" x.npz", " xx.npz"), (" x.npz", " x.npz;"), ("P6 met", "P6 met?")):
            dl.write_text(ok_line.replace(old, new) + "\n")
            assert not pin_line(dl, good, "x.npz", "n=1", "missing=1", "P6 met"), new
        dl.write_text(f"{T_UTC} OPS-9-pin: PIN x.npz {good[:8]}\n")  # a short sha standing alone is no pin (S20)
        assert not pin_line(dl, good[:8], "x.npz")
        jd = re.compile(r"truncated-judged=CC-[0-9A-Za-z-]+")
        for tok, want in (("truncated-judged=CC-227", True), ("truncated-judged=CC-", False),
                          ("truncated-judged=CC-227,", False), ("xtruncated-judged=CC-227", False)):
            dl.write_text(f"{ok_line} {tok}\n")
            assert pin_line(dl, good, "x.npz", jd) is want, tok

        # NB-6: frame names vs tar member names, names only
        import tarfile
        for t, names in (("p0.tar.gz", ["images/v1/patch0/a.jpg", "images/v1/patch0/d.jpg"]),
                         ("p1.tar", ["x/patch1/b.jpg"])):
            with tarfile.open(d / t, "w:gz" if t.endswith("gz") else "w") as tf:
                for n_ in names:
                    tf.addfile(tarfile.TarInfo(n_))
        assert missing_members(rows, [d / "p0.tar.gz", d / "p1.tar"]) == {"n_frame": 3, "n_members": 3, "missing": 0}
        assert missing_members(rows, [d / "p0.tar.gz"])["missing"] == 1
        with contextlib.redirect_stdout(io.StringIO()):
            must_refuse(lambda: cmd_slices(NS(op="members", frame=d / "f.tsv", tar=[d / "p1.tar"])), "no tar member")

        # pick (CC-226 W1(c)): only a decide whose sha is on a 'P6 met' pin line
        dd = d / "dec"
        dd.mkdir()
        ex = b"1\n"
        dec = {"frame_sha256": K.sha_file(d / "f.tsv"), "excluded_sha256": hashlib.sha256(ex).hexdigest(),
               "n_frame_decided": 3}
        (dd / "w25_excluded_ids.txt").write_bytes(ex)
        (dd / "w25_decide.json").write_text(json.dumps(dec))
        dsha = K.sha_file(dd / "w25_decide.json")
        pk = lambda o: cmd_slices(NS(op="pick", frame=d / "f.tsv", decide=dd, out=d / o), log)  # noqa: E731
        must_refuse(lambda: pk("l1.json"), "P6 met")
        p6_ok, p6_bad = pin_cases("w25_decide.json", dsha, "P6 met")
        for bad in [*p6_bad, pin_cases("w25_decide.json", dsha)[0], pin_cases("decide", dsha, "P6 met")[0]]:
            log.write_text(bad + "\n")  # + a pin without 'P6 met', and one without the file name
            must_refuse(lambda: pk("l1.json"), "P6 met")
        log.write_text(p6_ok + "\n")
        must_refuse(lambda: pk("l1.json"), "feature more blocks")  # pinned; 2 survivors < 2 x 2000

    # cut: blocks of 2, slices of 2; survivors in frame order, only inside the decided blocks
    fr = [(i, f"patch0/{i}.jpg") for i in (10, 11, 12, 13, 14, 15, 16)]
    fsha, ex = "f" * 64, b"11\n14\n"
    rec = {"frame_sha256": fsha, "excluded_sha256": hashlib.sha256(ex).hexdigest(), "n_frame_decided": 6}
    got = cut(fr, fsha, rec, ex, n=2, block=2)
    assert got == {"slice_a": [10, 12], "slice_b": [13, 15], "n_blocks_used": 3}, got
    must_refuse(lambda: cut(fr, fsha, rec | {"n_frame_decided": 4}, ex, n=2, block=2), "feature more blocks")
    must_refuse(lambda: cut(fr, "e" * 64, rec, ex, n=2, block=2), "not of this frame")
    must_refuse(lambda: cut(fr, fsha, rec, b"11\n", n=2, block=2), "not of this frame")
    print(json.dumps({"tier": LABEL, "selftest": "slices ok", "checks": ["frame-patches-order", "no-annotation-text",
                                                                        "frame-guards", "R6-pin", "members",
                                                                        "pick-P6-pin", "cut"]}))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("selftest")
    sp.add_parser("owners").add_argument("--out", type=Path, required=True, help="new file; never overwritten")
    sl = sp.add_parser("slices", help="C6 (R5 §D.5): frame | members | pick | selftest; needs ijson").add_subparsers(
        dest="op", required=True)
    sl.add_parser("selftest")
    fr = sl.add_parser("frame")
    fr.add_argument("--ann", type=Path, required=True, help="Objects365 v2 train annotation json")
    fr.add_argument("--ann-sha", required=True, help="its R6 LOG pin")
    mb = sl.add_parser("members", help="NB-6: frame names vs patch tar member names (names only)")
    mb.add_argument("--frame", type=Path, required=True)
    mb.add_argument("--tar", type=Path, action="append", required=True)
    pk = sl.add_parser("pick")
    pk.add_argument("--frame", type=Path, required=True)
    pk.add_argument("--decide", type=Path, required=True, help="the b_pa1_w25.py decide out-dir")
    for p in (fr, pk):
        p.add_argument("--out", type=Path, required=True, help="new file; never overwritten")
    a = ap.parse_args()
    if a.cmd == "slices":
        return cmd_slices(a)
    return selftest() if a.cmd == "selftest" else cmd_owners(a)


if __name__ == "__main__":
    sys.exit(main())
