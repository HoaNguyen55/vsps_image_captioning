#!/usr/bin/env python
"""VSPS-J E2b W25 pass for ledger line 2 (AMENDMENT_1_DRAFT_v1_2.md section D, commit 348b088; CC-223r3 R-a / R-b).

    <venv-cenfeat> -I scripts/vsps_j_e2b/e2b_w25.py feats --images I --sscd PT --out /root/e2b_w25/feats_mh769.npz
                                                                       M8, CPU: the 769 staged probe images
    <c_stage1_lists venv> -I scripts/vsps_j_e2b/e2b_w25.py decide --feats F --out-dir O     laptop, one look
    <c_stage1_lists venv> -I scripts/vsps_j_e2b/e2b_w25.py selftest                         CPU, synthetic features

Features and the rule are scripts/w25/w25.py's, unchanged: build_memory.features / near, rule = C1 | C2 | C3.
Custody: feats reads only the 769 staged images and writes features (ids, hashes, SSCD descriptors, file sha256).
decide reads the owner caches as image features only, and parses ids/keys via m0.kv4224(), m0.ut2532() and
m0.refused_sets(); no text or label value is printed or used. No owner-side id is printed or written: counts only
(PI-1101o). The drop / hold lists hold E2b probe-image ids only.
feats writes only under /root/e2b_w25/ (NB-3; features, no text), pulled by hand with its sha. decide's one-look
guard is per --out-dir: the OPS line records the single decide run and its output shas (NB-3). The OPS lines also
record the git blob shas of the reused w25.py, build_memory.py, common.py and cen_fetch.py (NB-7).
"""
from __future__ import annotations

import argparse
import json
import signal
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent / "w25")]
import e2b  # noqa: E402  plan, M0 id lists, check_images
import m0  # noqa: E402  kv4224, ut2532, refused_sets, image_id, sha_file

ROOT = e2b.ROOT
CEN = ROOT / ".session_backup/machines/M1/root/outputs/c_en"  # laptop mirrors (AMENDMENT_1 D.1)
K1 = Path.home() / "vsps_w25k1"
OTHER = {  # owner group: (laptop path, sha256 pin)  D.1
    "ut2402": (ROOT / ".session_backup/machines/M1/root/outputs/w25/feats_ut.npz",
               "17d3ebf07ebf95bcd0c8bf123ff65fb8f2df65c52cd4e17ac492e05976b98c1d"),
    "uitviic_test": (K1 / "uitviic_test.npz", "4f4784903fb0164309a3b1b6b3ba4fbaa9c09da6c4be5294a6c43f75581ff95f"),
    "oiv7_val": (K1 / "oiv7_val.npz", "2ca7e2f56bc3695dc4be13f10d4511881e4460d6d0815c27a6ab1220d8e7c5bb"),
    "karpathy_test": (CEN / "feats_coco_test.npz", "2bc3b83ea4116603a041559d35e156f11005c44a910f29100439658593d45934"),
    "ktvic_test": (K1 / "ktvic_test.npz", "cd985050fd2042b87049410334a05a6406b4363d69c05a45e6ed28ccae86702d"),
    "openviic_test": (K1 / "openviic_test.npz", "f4c79b825a1b62256dfac15b6ce59bce1054b83386ab4d5d932ac3c4e73d360e"),
    "cen_memory": (CEN / "feats_memory.npz", "caf4a62199fccfe903e3a553a3717673d62a32ae07a2e289c2a706d70132e437"),
}
# dispositions on a C1|C2|C3 match of an image of the 663 (D.1, CC-223r3 R-a / R-b); precedence drop > hold > count
DROP = ("kv4224", "kv_ut2532_Ra", "ut2402", "nocaps_val", "uitviic_test", "oiv7_val")
HOLD = ("karpathy_test", "kv_refused_Rb", "ktvic_test", "openviic_test")
COUNT = ("kv_a_touched", "cen_memory")
KV_SPLIT_N = {"kv4224": 4224, "kv_ut2532_Ra": 130, "kv_refused_Rb": 130, "kv_a_touched": 516}
COCO_ID = {*KV_SPLIT_N, "ut2402", "uitviic_test", "karpathy_test", "cen_memory"}  # owners keyed by COCO image id
N_CTRL, N_NOCAPS, CAP_H = 91, 4457, 0.5
OUT_DIR = Path("/root/e2b_w25")  # NB-3: the only place feats writes
OUT_FILES = ("e2b_w25_decide.json", "e2b_w25_lists.json")


def rows(f: dict, idx: list) -> dict:
    """The feature rows idx of a w25.load() dict."""
    import w25

    return {"ids": [f["ids"][i] for i in idx], "sha": [f["sha"][i] for i in idx],
            **{k: f[k][idx] for k in w25.KEYS}, "unreadable": []}


def split_kv(kv: dict, kv4224: set, ut2532: set, refused: set) -> dict:
    """NB-4 (i): KV-4,224 and the R-a (UT-2,532 ∩ KV-5,000) / R-b (exclusion.json-refused ∩ KV-5,000) / A-touched
    id lists of the KV-5,000 cache, built by id before any C1/C2/C3."""
    ids = [int(i) for i in kv["ids"]]
    sets = {"kv4224": kv4224 & set(ids), "kv_ut2532_Ra": ut2532 & set(ids), "kv_refused_Rb": refused & set(ids)}
    if sum(map(len, sets.values())) != len(set().union(*sets.values())):
        raise SystemExit("FAULT KV-5,000 split: KV-4,224, R-a and R-b overlap")
    sets["kv_a_touched"] = set(ids) - set().union(*sets.values())
    return {g: rows(kv, [j for j, i in enumerate(ids) if i in s]) for g, s in sets.items()}


def control(ids: list, hit_k2, ctrl: set, k2_ids: set) -> None:
    """D.3 positive control, run first: every Karpathy-test image of the 769 has a cache row and is flagged by
    C1|C2|C3 against the Karpathy-test cache (91/91). A FAULT raises before any outcome is computed or printed."""
    print(json.dumps({"positive_control_cache_rows": f"{len(ctrl & k2_ids)}/{len(ctrl)}"}))  # D.3: printed first
    if len(ctrl & k2_ids) != len(ctrl):
        raise SystemExit(f"FAULT positive control: {len(ctrl & k2_ids)}/{len(ctrl)} have a cache row; to a judge")
    flagged = sum(bool(h) for i, h in zip(ids, hit_k2) if i in ctrl)
    if flagged != len(ctrl):
        raise SystemExit(f"FAULT positive control: {flagged}/{len(ctrl)} flagged; no outcome, re-run under a diff-read note")


def dispose(ids: list, hits: dict, held: set) -> dict:
    """Images outside the held set only (D.3 scope); the most restrictive disposition wins: drop > hold > count."""
    out: dict = {"drop": [], "hold": [], "count": []}
    for j, i in enumerate(ids):
        if i in held:
            continue
        for kind, groups in (("drop", DROP), ("hold", HOLD), ("count", COUNT)):
            if any(hits[g][j] for g in groups):
                out[kind].append(i)
                break
    return {k: sorted(v) for k, v in out.items()}


def decide_core(x: dict, owners: dict, held: set, ctrl: set, rule) -> dict:
    """owners: {group: features} for every group of DROP + HOLD + COUNT. rule(x, y) -> w25.rule dict."""
    import numpy as np

    ids = [int(i) for i in x["ids"]]
    k2 = owners["karpathy_test"]
    control(ids, rule(x, k2)["excluded"], ctrl, {int(i) for i in k2["ids"]})  # NB-4 (iv): first
    per = {g: rule(x, owners[g]) for g in DROP + HOLD + COUNT}
    lists = dispose(ids, {g: r["excluded"] for g, r in per.items()}, held)
    in_held = np.array([i in held for i in ids])
    counts = {g: {k: {"held_106": int((v & in_held).sum()), "selection_663": int((v & ~in_held).sum())}
                  for k, v in r.items()} for g, r in per.items()}
    idl = {g: (len(set(ids) & {int(i) for i in owners[g]["ids"]}) if g in COCO_ID else None) for g in per}
    return {"positive_control": f"{len(ctrl)}/{len(ctrl)}", "id_level_in_769": idl,  # NB-4 (v): kv4224 entry
            "kv5000_ids_in_769": sum(idl[g] for g in KV_SPLIT_N),
            "kv5000_minus_4224_matches_663": {"R-a drop": counts["kv_ut2532_Ra"]["excluded"]["selection_663"],
                                              "R-b hold": counts["kv_refused_Rb"]["excluded"]["selection_663"],
                                              "A-touched count": counts["kv_a_touched"]["excluded"]["selection_663"]},
            "per_owner": counts, "n": {k: len(v) for k, v in lists.items()}, "lists": lists}


def make_feats(images: Path, want: dict, sscd: str, out: Path, workers: int) -> str:
    """Features of exactly the wanted staged images (D8), rows in image-id order, written by tmp + rename."""
    import w25

    if out.exists():
        raise SystemExit(f"REFUSED: {out} exists")
    e2b.check_images(images, want)
    names = sorted(want, key=m0.image_id)
    f = w25.bm().features([images / n for n in names], sscd, workers=workers)
    if f["unreadable"]:
        raise SystemExit(f"FAULT {len(f['unreadable'])} unreadable probe images")
    tmp = out.with_name(out.stem + ".tmp.npz")
    w25.save(tmp, [m0.image_id(n) for n in names], f, set="mh769", truncated=len(f.get("truncated", [])),
             utc=w25.F.utc())
    tmp.rename(out)
    return m0.sha_file(out)


def cmd_feats(a) -> int:
    import w25

    if a.out.resolve().parent != OUT_DIR:
        raise SystemExit(f"REFUSED --out outside {OUT_DIR}/ (NB-3)")
    want = json.loads(e2b.PLAN.read_text(encoding="utf-8"))["probe_images"]

    def cap(*_a):  # CC-225 Ruling 3(5): no outcome; re-run once under the §F protocol
        raise SystemExit(f"CAP_STOP: feature step over {CAP_H} h wall; operator FAULT, to a judge")
    signal.signal(signal.SIGALRM, cap)
    signal.alarm(int(CAP_H * 3600))
    sha = make_feats(a.images, want, w25.ok_sscd(a.sscd), a.out, a.workers)  # exactly the 769 plan images
    signal.alarm(0)
    print(json.dumps({"n": len(want), "feats_mh769.npz sha256": sha}))
    return 0


def cmd_decide(a) -> int:
    import w25

    if any((a.out_dir / n).exists() for n in OUT_FILES):
        raise SystemExit("REFUSED: decide output exists (one look)")
    want = sorted(m0.image_id(f) for f in json.loads(e2b.PLAN.read_text(encoding="utf-8"))["probe_images"])
    x = w25.load(a.feats)
    if [int(i) for i in x["ids"]] != want or x["unreadable"]:
        raise SystemExit("FAULT feats_mh769.npz is not the 769 plan images, all readable")
    L = e2b.lists()
    held, ctrl = L["selection_excluded_ids.txt"], L["karpathy_test_val_ids.txt"]
    if len(ctrl) != N_CTRL or not ctrl <= held <= set(want):
        raise SystemExit("FAULT M0 lists: the 91 Karpathy-test images are not inside the 106 held of the 769")
    kv = w25.load(CEN / "feats_coco_kval.npz", w25.CEN_FEATS["coco_kval"])
    if sorted(int(i) for i in kv["ids"]) != w25.K.ids("kv5000"):
        raise SystemExit("FAULT the KV cache is not KV-5,000")
    owners = split_kv(kv, m0.kv4224(), m0.ut2532(), set().union(*m0.refused_sets()[0].values()))
    if {g: len(f["ids"]) for g, f in owners.items()} != KV_SPLIT_N:
        raise SystemExit("FAULT KV-5,000 split is not 4,224 / 130 / 130 / 516")
    noc = w25.load(CEN / "feats_nocaps_val.npz", w25.CEN_FEATS["nocaps_val"])
    oid, xm = {r[0]: r[1][:-4] for r in w25.F.load_list("nocaps_val")}, w25.xm_ids()
    owners["nocaps_val"] = rows(noc, [j for j, n in enumerate(noc["ids"]) if oid[n] not in xm])  # RULE.md l.19
    if len(owners["nocaps_val"]["ids"]) != N_NOCAPS:
        raise SystemExit("FAULT NoCaps val is not 4,457 rows after the XM3600 drop")
    owners |= {g: w25.load(p, sha) for g, (p, sha) in OTHER.items()}
    rec = decide_core(x, owners, held, ctrl, lambda u, y: w25.rule(u, y, w25.bm().near))
    lists = rec.pop("lists")
    rec |= {"label": e2b.LABEL, "rule": "C1 sha-equal | C2 min(pHash, dHash) <= 10 and SSCD >= 0.5 | C3 SSCD > 0.75",
            "inputs_sha256": {"feats_mh769": m0.sha_file(a.feats), "kv5000": w25.CEN_FEATS["coco_kval"],
                              "nocaps_val": w25.CEN_FEATS["nocaps_val"], **{g: s for g, (_p, s) in OTHER.items()},
                              "kv4224_ids": m0.PIN["kv4224_ids"]}, "utc": w25.F.utc()}
    a.out_dir.mkdir(parents=True, exist_ok=True)
    for name, obj in zip(OUT_FILES, (rec, {"drop": lists["drop"], "hold": lists["hold"]})):
        tmp = a.out_dir / (name + ".tmp")
        tmp.write_text(json.dumps(obj, indent=1) + "\n")
        tmp.rename(a.out_dir / name)
    print(json.dumps({k: rec[k] for k in ("positive_control", "id_level_in_769", "kv5000_ids_in_769",
                                          "kv5000_minus_4224_matches_663", "n")}, indent=1))
    print(json.dumps({n: m0.sha_file(a.out_dir / n) for n in OUT_FILES}))
    return 0


def selftest() -> int:
    """Synthetic features through w25.rule / build_memory.near unchanged; checks control-first, R-a / R-b,
    precedence, the KV split by id, and that no owner-only id reaches the record."""
    import contextlib
    import io

    import numpy as np

    import w25

    rng = np.random.default_rng(0)

    def feats(ids, base=None, take=()):
        n = len(ids)
        f = {"ids": list(ids), "sha": [f"s{rng.integers(1 << 62)}" for _ in ids], "unreadable": []}
        for k in ("phash", "dhash", "phash_m", "dhash_m"):
            f[k] = rng.integers(0, 2**63, n, dtype=np.uint64)
        v = rng.normal(size=(n, 512)).astype(np.float32)
        f["sscd"] = v / np.linalg.norm(v, axis=1, keepdims=True)
        for j, src in take:  # row j becomes a byte copy (C1) of base row src
            f["sha"][j] = base["sha"][src]
            for k in w25.KEYS:
                f[k][j] = base[k][src]
        return f

    x = feats(range(1, 9))  # 1 = control (held), 2..8 = the selection set
    held, ctrl = {1}, {1}
    owner_only = 999001
    o = {g: feats([owner_only]) for g in DROP + HOLD + COUNT}
    o["karpathy_test"] = feats([1, 2, 3, owner_only], x, [(0, 0), (1, 1), (2, 2)])
    o["kv4224"] = feats([2, owner_only], x, [(0, 1)])          # 2: drop beats the Karpathy hold
    o["kv_refused_Rb"] = feats([6], x, [(0, 5)])               # 6: R-b hold beats the A-touched count
    o["kv_a_touched"] = feats([4, 6], x, [(0, 3), (1, 5)])     # 4: count only
    o["cen_memory"] = feats([5], x, [(0, 4)])                  # 5: count only
    o["kv_ut2532_Ra"] = feats([7], x, [(0, 6)])                # 7: R-a drop
    near = w25.bm().near
    rule = lambda u, y: w25.rule(u, y, near)  # noqa: E731
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rec = decide_core(x, o, held, ctrl, rule)
    assert buf.getvalue().splitlines()[0] == '{"positive_control_cache_rows": "1/1"}', buf.getvalue()  # NB-3: first
    assert rec["lists"] == {"drop": [2, 7], "hold": [3, 6], "count": [4, 5]}, rec["lists"]
    assert rec["kv5000_minus_4224_matches_663"] == {"R-a drop": 1, "R-b hold": 1, "A-touched count": 2}, rec
    assert str(owner_only) not in json.dumps({k: v for k, v in rec.items() if k != "lists"})
    bad = dict(o, karpathy_test=feats([1, owner_only]))  # the control image has a row but no match
    for owners, msg in ((bad, "flagged"), (dict(o, karpathy_test=feats([owner_only])), "cache row")):
        calls: list = []
        try:
            decide_core(x, owners, held, ctrl, lambda u, y: calls.append(y) or rule(u, y))
        except SystemExit as e:
            assert "FAULT positive control" in str(e) and msg in str(e), e
        else:
            raise AssertionError("positive-control FAULT not raised")
        assert calls == [owners["karpathy_test"]], "the control must run first and stop every other comparison"
    kv = feats(range(1, 11))
    sp = split_kv(kv, {1, 2, 3, 4}, {5, 6}, {7})
    assert {g: sorted(f["ids"]) for g, f in sp.items()} == {"kv4224": [1, 2, 3, 4], "kv_ut2532_Ra": [5, 6],
                                                            "kv_refused_Rb": [7], "kv_a_touched": [8, 9, 10]}
    feats_to_decide(rule)
    try:  # NB-3: feats writes only under /root/e2b_w25/
        cmd_feats(argparse.Namespace(out=Path("/tmp/feats_mh769.npz")))
    except SystemExit as e:
        assert "outside /root/e2b_w25" in str(e), e
    else:
        raise AssertionError("feats accepted an --out outside /root/e2b_w25/")
    print("e2b_w25 selftest ok")


def feats_to_decide(rule) -> None:
    """W3 (AMENDMENT_1 §D "a CPU selftest on synthetic images"): synthetic JPEGs -> make_feats -> w25.load ->
    decide_core, end to end. The dummy SSCD net and the JPEG writer are copied unchanged from scripts/w25/w25.py
    selftest (l.317-327; w25.py is pinned, so they are not factored out there)."""
    import io
    import tempfile

    import numpy as np
    import torch
    from PIL import Image

    import w25

    rng = np.random.default_rng(1)
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)

        class Net(torch.nn.Module):  # dummy SSCD: 512-d unit vector of pooled colour statistics
            def forward(self, x):
                v = torch.cat([x.mean((2, 3)), x.std((2, 3))], 1).repeat(1, 86)[:, :512]
                return v / (v * v).sum(1, keepdim=True).sqrt()

        pt = d / "dummy.pt"
        torch.jit.script(Net()).save(str(pt))

        def jpeg(im) -> bytes:
            b = io.BytesIO()
            im.save(b, "JPEG", quality=90)
            return b.getvalue()

        colours = ((230, 20, 20), (20, 230, 20), (20, 20, 230), (230, 230, 20), (230, 20, 230))  # distinct for the dummy net
        body = [jpeg(Image.fromarray(np.clip(rng.normal(c, 20, (300, 400, 3)), 0, 255).astype(np.uint8)))
                for c in colours]
        own, pro = d / "owners", d / "probe"
        own.mkdir()
        pro.mkdir()
        for k in range(3):  # owner images: 0 -> a KV-4,224 image, 1 -> a Karpathy-test image, 2 -> the control's
            (own / f"o{k}.jpg").write_bytes(body[k])
        of = w25.bm().features([own / f"o{k}.jpg" for k in range(3)], str(pt), workers=1)
        of["ids"] = [9001, 9002, 100]
        # probe images: 100 = control (held, byte copy of o2), 101 copy of o0, 102 copy of o1, 103 and 104 unrelated
        probe = {100: body[2], 101: body[0], 102: body[1], 103: body[3], 104: body[4]}
        for i, b in probe.items():
            (pro / f"COCO_val2014_{i:012d}.jpg").write_bytes(b)
        want = {f"COCO_val2014_{i:012d}.jpg": m0.sha_file(pro / f"COCO_val2014_{i:012d}.jpg") for i in probe}
        out = d / "feats.npz"
        sha = make_feats(pro, want, str(pt), out, 1)
        x = w25.load(out)
        assert x["ids"] == sorted(probe) and sha == m0.sha_file(out) and not x["unreadable"], x["ids"]
        assert x["sha"] == [want[f"COCO_val2014_{i:012d}.jpg"] for i in sorted(probe)]  # rows aligned with ids
        for bad, msg in ((lambda: make_feats(pro, want, str(pt), out, 1), "exists"),):
            try:
                bad()
            except SystemExit as e:
                assert msg in str(e), e
            else:
                raise AssertionError("make_feats overwrote an existing output")
        (pro / "extra.jpg").write_bytes(body[0])
        try:
            make_feats(pro, want, str(pt), d / "f2.npz", 1)
        except SystemExit as e:
            assert "extra" in str(e), e
        else:
            raise AssertionError("an extra staged image was accepted")
        empty = rows(of, [])
        owners = {g: empty for g in DROP + HOLD + COUNT}
        owners["kv4224"] = rows(of, [0])
        owners["karpathy_test"] = rows(of, [1, 2])
        rec = decide_core(x, owners, {100}, {100}, rule)
        assert rec["lists"] == {"drop": [101], "hold": [102], "count": []}, rec["lists"]
        assert rec["per_owner"]["kv4224"]["C1_C2_registered"]["selection_663"] == 1  # the byte copy is C1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("selftest")
    f = sp.add_parser("feats")
    f.add_argument("--images", type=Path, required=True, help="the 769 staged probe images (under /root/.cache/)")
    f.add_argument("--sscd", type=Path, required=True, help="sscd_disc_mixup.torchscript.pt (9f26bd4c)")
    f.add_argument("--out", type=Path, required=True)
    f.add_argument("--workers", type=int, default=6)
    d = sp.add_parser("decide")
    d.add_argument("--feats", type=Path, required=True, help="the pulled feats_mh769.npz")
    d.add_argument("--out-dir", type=Path, required=True)
    a = ap.parse_args()
    return {"selftest": lambda _a: selftest(), "feats": cmd_feats, "decide": cmd_decide}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
