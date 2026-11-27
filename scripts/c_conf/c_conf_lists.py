"""C-CONF list builder, part 1: the carve order (registration draft v0.3, section 5.1 "Draw"). CPU, ids only.

    order = random.Random(BM.seed("carve", "ov_train", "c0")).sample(sorted(P1), len(P1))

Base: the memory clusters of lists.json with exactly one member, an OpenViIC image. P1 = base minus (i) every
OpenViIC file named in the _pairs block of the panel file, minus (iii) the id matches of the owner lists (KTVIC
owners reach OpenViIC files only through _pairs, so they fall inside (i); the OpenViIC owner is matched by file
name). The near-copy part of (iii) and the first 2,000 survivors are block 0's work, not this file's.

Reads only the files of INPUTS, each checked against its pinned sha256. Of the panel file it parses only the
_provenance and _pairs blocks, read in CHUNK-character steps from the start of the file; the caption blocks come
after _pairs and are never parsed (at most CHUNK characters past _pairs are read into memory and dropped). An audit
hook records every file the process opens; the run refuses to finish if a data file outside INPUTS was opened.
Writes one file: a JSON list of [cluster id, file name, image sha256], in order, and nothing else.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "c_stage1"))

OPENED: list[str] = []
sys.addaudithook(lambda ev, args: OPENED.append(str(args[0])) if ev == "open" and isinstance(args[0], (str, Path)) else None)

import build_memory as BM  # noqa: E402  seed(), the registered seed function

CHUNK = 4096
PANEL = "data/ktvic_openviic_refs.json"
LISTS = "manuscript/prereg/2026-10-22_c_stage1/lists.json"
OWNERS = "manuscript/prereg/2026-11-02_c_pvr_tier1/c_pvr_owners.json"
VIHAL = "manuscript/prereg/2026-11-10_vihal_set/ids/"
INPUTS = {
    LISTS: "5c479f03e8be544f4cd12b5d997b5dc92b6c622df061760cd02f6ba82f6b4371",
    PANEL: "4eb02cc43841bae4f844ee74d4c01b58e677dc8d6abafdd998c9f5b5706f725d",
    OWNERS: "0cf330d39ae4a24b1e95841fbb16f617d405a9d4ffca9747498ef33657f3b086",
    VIHAL + "pool_trainonly_2153_ids.txt": "b85f0c040f05aebe4f605613a2947ee48684444ae2e7d86716411c3423663277",
    VIHAL + "survivors_ordered.tsv": "995ce8c3817b5d20713ca5957794abf15a220ba051c1e3827cf4346c62a3783c",
    VIHAL + "removed_ids.txt": "b34f5b7b3ed01e6fb9e9ac1984dbc836a15500f6fc9e5e82583d5cf7d5e9a3a2",
    "manuscript/prereg/2026-10-30_bd_t1/bd_t1_lists.json": "b6bbce8f2fa1934c76dcc6005a2d69ff196e8686aa0bd9cc2614d5603b985a17",
    "data/splits/ktvic_dev300.txt": "cee024f8bb76846b1623e36d1861caccc4d13874db87544213a1f18f3de6898c",
    "manuscript/prereg/2026-10-21_dev_pools/ktvic_dev299.tsv": "a4ac7fdbd904f2205845705f5235b9748225a83a07854b58e59a755b85e4186e",
    "manuscript/prereg/2026-10-21_dev_pools/exclusion.json": "c52a96d18925b974878ae1a970c3f9133fb3482216676fd41871eeabb68cc77f",
}
# Every owner of the register, by how its ids can meet an OpenViIC training file. A new owner stops the run.
KTVIC_OWNERS = {"h_bdt1_739", "ktvic_dev299", "refused_ktvic_dup", "ktvic_test_558"}
OPENVIIC_OWNERS = {"openviic_dev_c1", "openviic_test_2001"}
OTHER_OWNERS = {  # other datasets: no id can equal an OpenViIC file; the near-copy part of block 0 covers them
    "a_t1_dev_ade20k", "a_t3_val2017", "ade20k_val", "amber_generative", "b_pa1_dev_contacts", "coco_gap_val2014_734",
    "coco_restval_b4", "flickr30k_c_t3_carve", "karpathy_test_5000", "kv5000", "longcap_polaris_docci_thumb_composite_vapr",
    "m0_dev_touched_3454", "mtvqa_test", "nocaps_val_4500", "oiv7_val_41164", "pascal50s_a", "refused_chair500",
    "refused_coco2500", "refused_cv295", "refused_pope500", "t2_2000", "textvqa_textcaps_val", "uitviic_test_231",
    "uitviic_train_pool", "uitviic_val_924", "ut2402", "vindr_cxr_test", "vintext_test", "viocrvqa_test",
    "visignvqa_test", "vitextvqa_dev", "vitextvqa_test", "vizwiz_val", "xm3600_all"}
REGISTERED = {"base": 5926, "after_i": 5925, "i_file": "00000001628.jpg"}  # draft v0.3 section 5.1 (i)


def read_checked(root: Path, rel: str, pins: dict) -> bytes:
    data = (root / rel).read_bytes()
    got = hashlib.sha256(data).hexdigest()
    assert got == pins[rel], f"sha256 of {rel} is {got}, pinned {pins[rel]}"
    return data


def pairs_block(path: Path, chunk: int = CHUNK) -> tuple[dict, int]:
    """Parse {"_provenance": ..., "_pairs": ...} from the start of the file; return _pairs and the characters read
    past its end. Nothing after _pairs is parsed."""
    dec, ws, buf = json.JSONDecoder(), re.compile(r"\s*"), ""
    with open(path, encoding="utf-8") as f:
        while True:
            try:
                pos = ws.match(buf, 1).end()
                assert buf[0] == "{"
                vals = []
                for want in ("_provenance", "_pairs"):
                    key, pos = dec.raw_decode(buf, pos)
                    assert key == want, f"panel key {key!r} where {want!r} was expected"
                    pos = ws.match(buf, pos).end()
                    if buf[pos] != ":":
                        raise json.JSONDecodeError("colon", buf, pos)
                    val, pos = dec.raw_decode(buf, ws.match(buf, pos + 1).end())
                    vals.append(val)
                    if want == "_provenance":
                        pos = ws.match(buf, pos).end()
                        if buf[pos] != ",":
                            raise json.JSONDecodeError("comma", buf, pos)
                        pos = ws.match(buf, pos + 1).end()
                return vals[1], len(buf) - pos
            except (json.JSONDecodeError, IndexError):
                more = f.read(chunk)
                assert more, "panel file ended before the _pairs block closed"
                buf += more


def ktvic_owner_ids(root: Path, pins: dict) -> dict[str, set[str]]:
    txt = lambda rel: read_checked(root, rel, pins).decode("utf-8")  # noqa: E731
    bd = json.loads(txt("manuscript/prereg/2026-10-30_bd_t1/bd_t1_lists.json"))
    ex = json.loads(txt("manuscript/prereg/2026-10-21_dev_pools/exclusion.json"))
    return {
        "vihal_pool": set(txt(VIHAL + "pool_trainonly_2153_ids.txt").split()),
        "vihal_survivors": {r.split("\t")[1] for r in txt(VIHAL + "survivors_ordered.tsv").splitlines()[1:] if r.strip()},
        "vihal_removed": set(txt(VIHAL + "removed_ids.txt").split()),
        "bd_t1_H": set(bd["H"]["ids"]), "bd_t1_T2": set(bd["T2"]["ids"]),
        "ktvic_dev300": set(txt("data/splits/ktvic_dev300.txt").split()),
        "ktvic_dev299": {r.split("\t")[0] for r in txt("manuscript/prereg/2026-10-21_dev_pools/ktvic_dev299.tsv").splitlines() if r.strip()},
        "refused_ktvic_dup": set(ex["ids"]["ktvic"]["ktvic_dev_near_duplicate_of_test"]),
    }


def build(root: Path, pins: dict = INPUTS, registered: dict | None = REGISTERED) -> tuple[list, dict]:
    lists = json.loads(read_checked(root, LISTS, pins))
    owners = json.loads(read_checked(root, OWNERS, pins))["owners"]
    assert set(owners) == KTVIC_OWNERS | OPENVIIC_OWNERS | OTHER_OWNERS, "owners register differs from this file's table"
    read_checked(root, PANEL, pins)  # sha256 over the bytes; not parsed here
    pairs, over = pairs_block(root / PANEL)
    assert over <= CHUNK
    copies = {e[0] for split in pairs.values() for entries in split.values() for e in entries}

    base = {c["cid"]: c["members"][0] for c in lists["memory"] if len(c["members"]) == 1 and c["members"][0][0] == "openviic"}
    out_i = {cid for cid, m in base.items() if m[2] in copies}
    counts = {"base": len(base), "removed_i": len(out_i), "after_i": len(base) - len(out_i), "panel_chars_read_past_pairs": over}
    name_of = {cid: m[2] for cid, m in base.items()}
    if registered:
        assert counts["base"] == registered["base"] and counts["after_i"] == registered["after_i"], counts
        assert registered["i_file"] in {name_of[c] for c in out_i}

    out_iii = set()
    for owner, ids in ktvic_owner_ids(root, pins).items():
        names = {e[0] for i in ids for e in pairs["train"].get(i, [])}
        hit = {cid for cid, n in name_of.items() if n in names}
        assert hit <= out_i, f"{owner}: an id match outside (i)"
        counts[f"iii_id_{owner}"] = f"{len(ids)} ids, {len(hit)} base matches, all inside (i)"
    ov_dev = {s[0] for k in ("ov_dev_a", "ov_dev_b") for s in lists["sets"][k]}
    hit = {cid for cid, n in name_of.items() if n in ov_dev}
    out_iii |= hit - out_i
    counts["iii_id_openviic_dev_c1"] = f"{len(ov_dev)} files, {len(hit)} base matches"

    p1 = sorted(set(base) - out_i - out_iii)
    counts["P1"] = len(p1)
    order = random.Random(BM.seed("carve", "ov_train", "c0")).sample(p1, len(p1))
    return [[cid, base[cid][2], base[cid][3]] for cid in order], counts


def opened_data_files() -> list[Path]:
    """Files under the repository that the process has opened so far, Python source excluded."""
    return sorted({p for p in map(lambda x: Path(x).resolve(), OPENED) if ROOT in p.parents and p.suffix not in (".py", ".pyc")})


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", required=True, help="new file for the order; refused if it exists")
    out = Path(ap.parse_args().out)
    side = Path(str(out) + ".sha256")
    assert not out.exists() and not side.exists(), f"{out} exists; this builder never overwrites"
    rows, counts = build(ROOT)
    opened = opened_data_files()
    for k, v in counts.items():
        print(f"{k}: {v}")
    print("files opened under the repository (not .py):", *opened, sep="\n  ")
    extra = [p for p in opened if p not in {(ROOT / k).resolve() for k in INPUTS}]
    assert not extra, f"opened outside INPUTS, nothing written: {extra}"
    data = (json.dumps(rows, separators=(",", ":")) + "\n").encode("utf-8")
    sha = hashlib.sha256(data).hexdigest()
    with open(out, "xb") as f:
        f.write(data)
    with open(side, "x", encoding="utf-8") as f:
        f.write(f"{sha}  {out.name}\n")
    print(f"order rows: {len(rows)}\norder sha256: {sha}  {out}")


if __name__ == "__main__":
    main()
