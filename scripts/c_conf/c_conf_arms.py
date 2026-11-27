#!/usr/bin/env python3
"""C-CONF list builder, part 2 (CPU): block 0 (the carve from the pinned order, the arm lists of OV-carve, K0 and K0 on
the first-look form), the perm diagnostics with the refill gate, and T0 (the arm lists of OV-test under the token,
K0-T, the refill gate). Registration draft manuscript/directions/C_CONFIRM_PREREG_DRAFT_2026-11-16_v3.md (final, 18e61111; drafted on b3c4e405)
§2, §5.1 (ii) and (iii), §5.3, §6.2 steps 0.1-0.3, §6.5 T0, §10.1 G0 / G0b / G4, §11.1 row 1. DRAFT on synthetic
fixtures under CC-438 FP-7: no study data, no host run, no token, no commit before a GO.

A new file beside c_conf_lists.py (part 1, the carve order, pinned c774f1a4 and left byte-identical). The rules are
those of scripts/c_attr/c_attr_lists.py (494a0e56), reused: eligible and rand_draw (c_conf.py = c_attr.py), sattolo
(c_attr_lists, unchanged), perm_list (c_attr_lists plus the own-cluster filter). New: own-cluster removal by id in every
arm (OV-carve), the byte-twin donor rule (§2), the near sets for LMCap, the shot assert (ii), the near-copy part of
(iii) (w25.rule = C1 or C2 or C3 over the owners' feature caches, as c_pvr_run.flag), K0 / K0-T comparators on ret,
rand d0 and perm p1 only (no fix arm in C-CONF).

  python -I -B scripts/c_conf/c_conf_arms.py envcheck              block 0's interpreter (venv-cenfeat): rc 3 if not
  python -I -B scripts/c_conf/c_conf_arms.py block0 --out c_conf_carve.json --lists-out lists_ov_carve.json   G0
  python -I -B scripts/c_conf/c_conf_arms.py diag --lists lists_ov_carve.json --out diag.json          rc 3 = G0b
  python -I -B scripts/c_conf/c_conf_arms.py t0 --token T [--decision D] --dir STAGE --out lists_ov_test.json [--dry-run]
Lists and reports hold cluster ids, image ids (file names), image sha256, counts and shares only. No caption is read;
the OpenViIC training annotation is read for the reference counts of the carve (counts only).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import c_conf as A  # noqa: E402  (imports C's pinned modules unchanged)

sys.path[:0] = [str(A.ROOT / "scripts" / d) for d in ("c_attr", "c_pvr", "w25", "grl")]
import c_attr_lists as AL  # noqa: E402  sattolo, RANK_KEEP, REFILL_GATE (unchanged)

BM, C, sha = A.BM, A.C, A.sha
N_EX, NEAR = BM.N_EX, BM.NEAR_COS
CARVE_N = 2000  # §5.1: the first 2,000 survivors of the order
#: pinned inputs of block 0 (§5.1, §6.2, §6.4a); REGDIR is set at the registration commit, as the job's REG
REGDIR = A.ROOT / "manuscript/prereg/2026-11-18_c_conf"
ORDER = (REGDIR / "c_conf_carve_order.json", "8e11bad51c77adc54c05b91a86f7b6f5a1f2d0e9032f06faf80f05e438d42850")
ORDER_RUN = (REGDIR / "c_conf_carve_order.run.txt", "4bc2da456a3ef4200b227b5d9b41e2cfc818fc484585a95540f0281ca65bb5e1")
PVR = A.ROOT / "manuscript/prereg/2026-11-02_c_pvr_tier1"
OWNERS = (PVR / "c_pvr_owners.json", "0cf330d39ae4a24b1e95841fbb16f617d405a9d4ffca9747498ef33657f3b086")
OWNER_FEATS = (PVR / "c_pvr_owner_feats.json", "8f707edd3c30180d05a597bd7867a278605e3c9f3cdfc93ebc8544b98d7b50f9")
VIHAL = A.ROOT / "manuscript/prereg/2026-11-10_vihal_set"
VIHAL_SUMS = {VIHAL / "SHA256SUMS_v1_1": "dc0079672b3affb07415ee2968443f832f291e8cdc2c15f8928511627ba36f84",
              VIHAL / "ids/SHA256SUMS": "402a7a246804506af0d259c130c8b68d956b6e1dd41b867b719a3d782dfda22a"}  # Q19
EX_DEV_B = (A.CS2 / "ex_ov_dev_b.json", "072b17d14d89aa21110794be27168cf4ef4212a569a4d55d54c5acf1de7e5a41")  # N8
PARITY = {A.HOST / "outputs/c_attr_b1/out/at_qwen25vl_7b_ov_dev_b-ret-k8-first-T1-mvi-b1.preds.json":
          "f7298a01b94044eb9d416b34cbd9986fd34b350350543bce295ead7677f2829f",
          A.HOST / "c_attr_score/led/ovb.jsonl": "f79ea6a9c59157216fdf1662ce320c35a1befe48a87cfb36a174a7cfef0244f8"}
SSCD = (A.lb.DATA / "models/sscd_disc_mixup.torchscript.pt",
        "9f26bd4c848cc19b73d2ae92eea6e04886f61a7b764ceb7a13aeee62e6a6db56")  # W25 RULE §2
OWNER_DIR = A.lb.DATA / "c_conf_owners"  # the owners' caches, each staged alone by name and checked by its sha256
KT_TRAIN = ("datasets/ktvic/train_data.json", "72ee9b57c350fb5f215e1f04701c515a51e5e415240e51a77c8ce00ce6316a0f")
B_OWN = (".session_backup/2026-11-02/b_pa1/b_pa1_owners.json",
         "ae4b663064588a8a19dcd0c01a34284229b40c6de90cd24c88d098b7600b71b2")  # ids of the 'select' owners
#: §5.1 (iii) near-copy owners as registered (18e61111 l.146, CC-450 X1 in J2's text): only these. The four register
#: owners come through their caches; the ViHal and KTVIC dev300 lists (no register key, no cache) are featurised from
#: the KTVIC images. No file of any other owner may be in OWNER_DIR (G0): that also keeps the OV-test cache off the host.
NEAR_OWNERS = ("h_bdt1_739", "ktvic_dev299", "openviic_dev_c1", "refused_ktvic_dup")
ID_OWNERS = ("vihal_pool", "vihal_survivors", "vihal_removed", "ktvic_dev300")  # c_conf_lists.ktvic_owner_ids keys
KT_IMAGES = A.lb.DATA / "datasets/ktvic/images"  # the register's dir of the KTVIC owners
#: the sha256 of record of those KTVIC images (I1): hashed on the laptop by c_conf_ktvic_hash.py, training ids only
KT_HASHES = (HERE / "c_conf_ktvic_owner_images.sha256",
             "0b487fc851edbf059873023d4dbfa16db5f54844b3e931d72615e15f40387dde")


def read_pinned(p: Path, want: str) -> bytes:
    data = Path(p).read_bytes()
    if hashlib.sha256(data).hexdigest() != want:
        raise SystemExit(f"G0: {p} differs from its pin {want[:8]}")
    return data


# ------------------------------------------------------------------------------------------------ rules
def perm_list(donor_rank: list[int], row_q: np.ndarray, own_col: int) -> tuple[list[int], int]:
    """c_attr_lists.perm_list with q's own cluster removed by id: the first N_EX clusters of the donor's eligible
    ranking at cosine < NEAR to q and not q's own cluster; refills = those taken from beyond the donor's first N_EX."""
    keep = [c for c in donor_rank[:N_EX] if row_q[c] < NEAR and c != own_col]
    refill = [c for c in donor_rank[N_EX:] if row_q[c] < NEAR and c != own_col][:N_EX - len(keep)]
    if len(keep) + len(refill) < N_EX:
        raise SystemExit("perm: the kept donor ranking is too short to refill (raise RANK_KEEP)")
    return keep + refill, len(refill)


def donors(ds: str, p: int, qids: list[str], sha: dict) -> tuple[list[int], int]:
    """§2: pi_p by Sattolo over the set's order; if pi_p(q) is q's byte twin, the donor is the next entry after the
    twin (cyclic) that is neither q nor a twin of q. Returns the donor positions and the number of replacements."""
    pi, n, out, rep = AL.sattolo(ds, p, len(qids)), len(qids), [], 0
    for i in range(n):
        d = pi[i]
        if sha[qids[d]] == sha[qids[i]]:
            d = next(x % n for x in range(d + 1, d + n) if x % n != i and sha[qids[x % n]] != sha[qids[i]])
            rep += 1
        out.append(d)
    return out, rep


def build(ds: str, mk: list[str], mv: np.ndarray, qids: list[str], qv: np.ndarray, sha: dict,
          own: dict | None = None) -> tuple[dict, dict]:
    """(ids-only lists, diagnostics) of one set; rows of qv in the set's order. own = {image id: its own cluster}
    (OV-carve): removed by id from every arm and asserted absent."""
    cos = qv @ mv.T
    col = {c: n for n, c in enumerate(mk)}
    own_col = [col[own[q]] if own else -1 for q in qids]
    out = {"set": ds, "ids": qids, "sha": {q: sha[q] for q in qids}, "ret": {}, "rand": {str(d): {} for d in A.DRAWS},
           "perm": {}, "donor": {}, "near": {}, **({"own": own} if own else {})}
    ranks = []
    for n, (q, row) in enumerate(zip(qids, cos)):
        ok = [int(j) for j in A.eligible(row, mk) if j != own_col[n]]
        ranks.append(ok[:AL.RANK_KEEP])
        out["ret"][q] = [mk[j] for j in ok[:N_EX]]
        names = [mk[j] for j in ok]
        for d in A.DRAWS:
            out["rand"][str(d)][q] = A.rand_draw(ds, q, names, d)
        out["near"][q] = sorted(mk[j] for j in np.flatnonzero(row >= NEAR))
    diag = {}
    for p in A.PERMS:
        dn, rep = donors(ds, p, qids, out["sha"])
        out["perm"][str(p)], out["donor"][str(p)], refills = {}, {}, 0
        for n, q in enumerate(qids):
            lst, r = perm_list(ranks[dn[n]], cos[n], own_col[n])
            out["perm"][str(p)][q], out["donor"][str(p)][q] = [mk[j] for j in lst], qids[dn[n]]
            refills += r
        d = {"refill_share_8": round(refills / (N_EX * len(qids)), 6), "twin_replacements": rep}
        for k in (4, 8):
            d[f"overlap_with_ret_{k}"] = round(float(np.mean(
                [len(set(out["perm"][str(p)][q][:k]) & set(out["ret"][q][:k])) / k for q in qids])), 6)
        diag[f"p{p}"] = d
    if own:
        seen = [q for q in qids if own[q] in out["ret"][q]
                or any(own[q] in v[q] for v in (*out["rand"].values(), *out["perm"].values()))]
        if seen:
            raise SystemExit(f"G0: {len(seen)} carve queries see their own cluster in an arm")
    out["diag"] = diag
    return out, diag


def carve_shots(ds: str, mk: list[str], cos: np.ndarray, own_cols: list[int]) -> list[str]:
    """§5.1 (ii): the LMCap shots of OV-carve, drawn on the full query-by-memory cosine matrix with no own-cluster
    masking, then the asserts: every carve query's cosine to its own cluster is >= the near cut, and no shot is a
    carve cluster. A failure is G0."""
    shots = A.lmcap_shots(ds, mk, cos)
    if any(cos[n, c] < NEAR for n, c in enumerate(own_cols)) or set(shots) & {mk[c] for c in own_cols}:
        raise SystemExit("G0 (§5.1 (ii)): a carve query is below the near cut to its own cluster, or a shot is a carve "
                         "cluster")
    return shots


def parity(built: dict, ret_ref: dict, rand_ref: dict, perm_ref: dict | None = None) -> dict:
    """K0 / K0-T: counts and failing ids only. Stored ret lists may hold [cluster, cosine] pairs (first-look form)."""
    ids = built["ids"]
    rep = {"n": len(ids)}
    refs = {"ret": (built["ret"], {q: [x[0] if isinstance(x, list) else x for x in v] for q, v in ret_ref.items()}),
            "rand_d0": (built["rand"]["0"], rand_ref)}
    if perm_ref is not None:
        refs["perm_p1"] = (built["perm"]["1"], perm_ref)
    for k, (mine, ref) in refs.items():
        bad = [q for q in ids if mine[q] != ref.get(q)]
        rep[f"{k}_equal"], rep[f"{k}_failing_ids"] = len(ids) - len(bad), bad[:10]
    rep["pass"] = all(rep[f"{k}_equal"] == len(ids) for k in refs)
    return rep


def near_copy(order: list, pool: dict, owners: dict, rule) -> tuple[list, dict]:
    """§5.1 (iii), near-copy part: a pool image is out when rule(pool, owner) excludes it for some owner (C1 or C2 or
    C3: w25.rule with build_memory.near, as c_pvr_run.flag). The carve is the first CARVE_N survivors of the order."""
    hit, per = set(), {}
    for k, y in sorted(owners.items()):
        r = rule(pool, y)
        per[k] = {c: int(v.sum()) for c, v in r.items()}
        hit |= {pool["ids"][i] for i in np.flatnonzero(r["excluded"])}
    keep = [r for r in order if r[0] not in hit]
    if len(keep) < CARVE_N:
        raise SystemExit(f"STOP at block 0 (§5.1): {len(keep)} pool images after (iii), fewer than {CARVE_N}")
    return keep[:CARVE_N], {"near_copy_hits": len(hit), "per_owner": per, "final_pool": len(keep)}


# ------------------------------------------------------------------------------------------------ inputs (host)
def owner_table() -> tuple[dict, dict]:
    """({owner: {cache: sha256}} compared at block 0, {owner: why not compared}): the four register owners of §5.1
    (iii) by the owner-feats manifest; every other register owner is listed as not compared. G0 if OWNER_DIR holds any
    file that is not one of those four caches (no cache of another owner reaches the rehearsal host)."""
    ow = json.loads(read_pinned(*OWNERS))["owners"]
    man = json.loads(read_pinned(*OWNER_FEATS))["owners"]
    if any(ow[k]["status"] != "compute" for k in NEAR_OWNERS):
        raise SystemExit("G0: a near-copy owner of §5.1 (iii) is not a compute owner of the register")
    cmp = {k: {man[k]["cache"]: man[k]["sha256"]} for k in NEAR_OWNERS}
    allowed = {x for c in cmp.values() for n in c for x in (n, n + ".sha256")}  # a cache and its sidecar
    stray = [p for p in OWNER_DIR.iterdir() if p.name not in allowed] if OWNER_DIR.is_dir() else []
    if stray:
        raise SystemExit(f"G0 (§5.1 (iii)): {len(stray)} files in {OWNER_DIR} are not caches of the near-copy owners")
    return cmp, {k: "not a near-copy owner of §5.1 (iii)" for k in sorted(set(ow) - set(NEAR_OWNERS))}


def record_check(files: list[str], shas: list[str], rec: dict) -> None:
    """§10.3 (l.454): every featurised owner image is in the pinned hash list at its sha256; a missing or differing
    row is G0."""
    bad = sum(rec.get(n) != h for n, h in zip(files, shas))
    if bad:
        raise SystemExit(f"G0 (§10.3): {bad} KTVIC owner images missing from or differing from the pinned hash list")


def ktvic_test_free() -> int:
    """Binding 1 (KTVIC test never staged): every file in KT_IMAGES is a KTVIC training image by the pinned
    training annotation; G0 otherwise. Returns the file count."""
    train = {im["filename"] for im in json.loads(read_pinned(A.lb.DATA / KT_TRAIN[0], KT_TRAIN[1]))["images"]}
    have = [p.name for p in KT_IMAGES.iterdir()] if KT_IMAGES.is_dir() else []
    extra = sum(n not in train for n in have)
    if extra:
        raise SystemExit(f"G0 (binding 1): {extra} files in {KT_IMAGES} are not KTVIC training images")
    return len(have)


def id_sides(W, CPR) -> dict:
    """§5.1 (iii): the ViHal pool, survivors and removed list and KTVIC dev300 (ids by the pinned
    c_conf_lists.ktvic_owner_ids at their sha256), featurised from the KTVIC images as the pool is (no cache exists),
    each image checked against its sha256 of record in KT_HASHES before its features are used."""
    import c_conf_lists as CLB

    lists = {k: sorted(v) for k, v in CLB.ktvic_owner_ids(A.ROOT, CLB.INPUTS).items() if k in ID_OWNERS}
    union = sorted(set().union(*lists.values()))
    files = [CPR.fname("ktvic", i, KT_IMAGES) for i in union]
    f = BM.features([KT_IMAGES / n for n in files], W.ok_sscd(SSCD[0]))
    if f["unreadable"]:
        raise SystemExit(f"G0: {len(f['unreadable'])} KTVIC images of the ViHal / dev300 owners unreadable")
    rec = {n: h for h, n in (ln.split(maxsplit=1) for ln in read_pinned(*KT_HASHES).decode("utf-8").splitlines())}
    record_check(files, f["sha"], rec)
    pos = {i: n for n, i in enumerate(union)}
    return {k: {**BM.subset(f, [pos[i] for i in v]), "ids": v} for k, v in lists.items()}


def block0_inputs() -> dict[Path, str]:
    """Step 0.1: every block-0 input with its pin (c_conf.py inputs --block0 prints the verdicts)."""
    files = {ORDER[0]: ORDER[1], ORDER_RUN[0]: ORDER_RUN[1], OWNERS[0]: OWNERS[1], OWNER_FEATS[0]: OWNER_FEATS[1],
             A.CL: A.C.LISTS_SHA256, A.ATTR_LISTS: A.ATTR_LISTS_SHA256, A.CS1 / A.MEM_EMB[0]: A.MEM_EMB[1],
             A.CS2 / A.DEV_EMB[0]: A.DEV_EMB[1], EX_DEV_B[0]: EX_DEV_B[1], SSCD[0]: SSCD[1],
             A.lb.DATA / A.OV_TRAIN_ANN[0]: A.OV_TRAIN_ANN[1], A.lb.DATA / KT_TRAIN[0]: KT_TRAIN[1],
             A.ROOT / B_OWN[0]: B_OWN[1], KT_HASHES[0]: KT_HASHES[1], **VIHAL_SUMS, **PARITY}
    for caches in owner_table()[0].values():
        files |= {OWNER_DIR / n: h for n, h in caches.items()}
    import c_conf_lists as CLB  # the ViHal and dev300 id lists of §5.1 (iii), at the pins of the order builder

    files |= {A.ROOT / r: h for r, h in CLB.INPUTS.items() if r.startswith(CLB.VIHAL) or r == "data/splits/ktvic_dev300.txt"}
    return files


def owner_sides(W, ids_of) -> tuple[dict, dict]:
    """The compared owners' feature rows (w25.load at their sha256), selected by id where the register says so."""
    cmp, skip = owner_table()
    ow = json.loads(read_pinned(*OWNERS))["owners"]
    sides = {}
    for k, caches in cmp.items():
        y = W.concat([W.load(OWNER_DIR / n, h) for n, h in sorted(caches.items())])
        ids, sel = [str(i) for i in y["ids"]], ow[k].get("select")
        idx = list(range(len(ids)))
        if sel:
            want = set(ids_of(read_pinned(A.ROOT / sel[0], sel[1]), sel[2]))
            idx = [i for i, x in enumerate(ids) if x in want]
        if len(idx) != ow[k]["n"]:
            raise SystemExit(f"G0: owner {k}: {len(idx)} feature rows, not n = {ow[k]['n']}")
        sides[k] = {**BM.subset(y, idx), "ids": [ids[i] for i in idx]}
    return sides, skip


def dev_b(mk: list[str], mv: np.ndarray, clists: dict) -> dict:
    """K0 and K0 on the first-look form (N8) on OV-dev-B, built in the mode T0 uses (stored vectors, manifest order)."""
    import stage2 as S2

    rows = S2.manifest2("ov_dev_b", clists)
    qids = [i for i, _f, _h in rows]
    built, _d = build("ov_dev_b", mk, mv, qids, A.query_vectors("ov_dev_b", qids, {}), {i: h for i, _f, h in rows})
    st = A.attr_ex("ov_dev_b")
    ex = json.loads(read_pinned(*EX_DEV_B))
    return {"K0": parity(built, st["ret"], st["rand"]["0"], st["perm"]["1"]),
            "K0_first_look_form": parity(built, ex["ret"]["ov_dev_b"], ex["rand"]["ov_dev_b"])}


def write_new(p: Path, obj, side: bool = False) -> str:
    data = json.dumps(obj, separators=(",", ":")) + "\n"
    with open(p, "x", encoding="utf-8") as f:
        f.write(data)
    if side:
        with open(str(p) + ".sha256", "x", encoding="utf-8") as f:
            f.write(f"{sha(p)}  {Path(p).name}\n")
    return sha(p)


# ------------------------------------------------------------------------------------------------ commands
def cmd_block0(a) -> None:
    """§6.2 step 0.2: the pinned order and its run record by sha256; the near-copy part of (iii) over the whole order;
    the carve (first 2,000 survivors, then sorted by cluster id); lists of every arm on OV-carve with the shots and
    their asserts; K0 and K0 on the first-look form. Any failure is G0 and writes no list file."""
    import c_pvr_run as CPR
    import w25 as W

    for p in (a.out, a.lists_out):
        if Path(p).exists():
            raise SystemExit(f"{p} exists; block 0 never overwrites")
    ktvic_test_free()
    order = json.loads(read_pinned(*ORDER))
    run_record = read_pinned(*ORDER_RUN)
    clists = C.load_lists(A.CL)
    mk, mv = A.mem_vectors()
    owners, skipped = owner_sides(W, CPR.ids_of)
    owners |= id_sides(W, CPR)
    paths = [A.lb.DATA / "datasets/openviic/images" / f for _c, f, _h in order]
    pool = BM.features(paths, W.ok_sscd(SSCD[0]))
    if pool["unreadable"] or pool["sha"] != [h for _c, _f, h in order]:
        raise SystemExit(f"G0: {len(pool['unreadable'])} pool images unreadable or a pool sha256 differs from the order")
    pool["ids"] = [c for c, _f, _h in order]
    carve, counts = near_copy(order, pool, owners, lambda q, y: W.rule(q, y, BM.near))
    names = {f for _c, f, _h in carve}
    overlap = {k: len(names & set(y["ids"])) + len({c for c, _f, _h in carve} & set(y["ids"])) for k, y in owners.items()}
    if any(overlap.values()):
        raise SystemExit(f"G0: the carve meets an exclusion list by id: {sorted(k for k, v in overlap.items() if v)}")
    carve = sorted(carve)  # §5.1: order of the set = sorted by cluster id
    qids, own = [f for _c, f, _h in carve], {f: c for c, f, _h in carve}
    col = {c: n for n, c in enumerate(mk)}
    qv = mv[[col[c] for c, _f, _h in carve]]
    built, diag = build("ov_carve", mk, mv, qids, qv, {f: h for _c, f, h in carve}, own)
    built["shots"] = carve_shots("ov_carve", mk, qv @ mv.T, [col[c] for c, _f, _h in carve])
    k0 = dev_b(mk, mv, clists)
    n_mem = len(clists["memory"])
    rec = {"label": A.LABEL["ov_carve"], "ids": qids, "rows": carve, "order_sha256": ORDER[1],
           "order_run_record_sha256": ORDER_RUN[1], "run_record_lines": len(run_record.splitlines()),
           "counts": {**counts, "order": len(order), "carve": len(carve), "shot_overlap": 0,
                      "share_of_memory_clusters": {"order": len(order) / n_mem, "final_pool": counts["final_pool"] / n_mem}},
           "owners_not_compared": skipped, "zero_overlap_by_id": overlap, "shots": built["shots"], "k0": k0,
           "diag": diag}
    print(json.dumps({k: v for k, v in rec["counts"].items() if k != "per_owner"}))
    print(json.dumps({"per_owner": counts["per_owner"], "not_compared": sorted(skipped)}))
    print(json.dumps({k: {x: y for x, y in v.items() if not x.endswith("failing_ids")} for k, v in k0.items()}))
    if not all(v["pass"] for v in k0.values()):
        raise SystemExit("G0: K0 or K0 on the first-look form fails; no list file written (STOP, no GPU step)")
    print(f"c_conf_carve.json sha256 {write_new(Path(a.out), rec, side=True)}")
    print(f"lists_ov_carve.json sha256 {write_new(Path(a.lists_out), built, side=True)}")


def cmd_diag(a) -> None:
    """Step 0.3: perm diagnostics and the refill gate (rc 3 = a share above 0.10: G0b), the reference-count
    distribution of the carve (counts only)."""
    p = Path(a.lists)
    if sha(p) != Path(str(p) + ".sha256").read_text().split()[0]:
        raise SystemExit(f"{p}: differs from its sidecar")
    lst = json.loads(p.read_text(encoding="utf-8"))
    res = {"set": lst["set"], "lists_sha256": sha(p), "perm": lst["diag"], "refill_gate": AL.REFILL_GATE}
    if lst["set"] == "ov_carve":
        ann = json.loads(A.pinned_file(A.lb.DATA / A.OV_TRAIN_ANN[0], A.OV_TRAIN_ANN[1]).read_text(encoding="utf-8"))
        res["reference_counts"] = dict(sorted(Counter(len(ann[i]["captions"]) for i in lst["ids"]).items()))
    over = [k for k, v in lst["diag"].items() if v["refill_share_8"] > AL.REFILL_GATE]
    res["gate"] = "G0b STOP" if over else "pass"
    Path(a.out).write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(res))
    sys.exit(3 if over else 0)


def cmd_t0(a) -> None:
    """§6.5 T0 under the token (the look has begun): lists of every arm on OV-test from the first look's stored vectors
    (2,001, TSV order, byte-twin donor rule), K0-T (ret and rand d0 equal the stored example file, 2,001 / 2,001; G4),
    the refill gate (G0b), the LMCap shots of ov_test, and the counts of §5.1 and §5.3 printed."""
    A.admit(a.token, a.decision)
    A.ov_gate()
    if a.dry_run:
        print("DRY t0: token admitted; no OV-test byte in a dry run; lists not built")
        return
    if Path(a.out).exists():
        raise SystemExit(f"{a.out} exists; T0 never overwrites")
    d = Path(a.dir)
    rows = A.ov_items(C.load_lists(A.CL))
    qids, sh = [n for _i, n, _h in rows], {n: h for _i, n, h in rows}
    mk, mv = A.mem_vectors()
    qv = A.query_vectors("ov_test", qids, {}, d)
    built, diag = build("ov_test", mk, mv, qids, qv, sh)
    ex = json.loads(A.staged("ex_ov_test.json", A.STAGE_T0, d).read_text(encoding="utf-8"))
    k0t = parity(built, ex["ret"]["ov_test"], ex["rand"]["ov_test"])
    built["shots"] = A.lmcap_shots("ov_test", mk, qv @ mv.T)
    half = A.CS.scored_sets(A.ROOT)["ov_test_confirm"]
    counts = {"n": len(qids), "distinct_sha256": len(set(sh.values())), "confirm_half_primary": len(half),
              "twin_replacements": {k: v["twin_replacements"] for k, v in diag.items()}}
    panel = d / A.PANEL[0]
    if panel.is_file():
        import c_conf_lists as CLB
        pairs, _over = CLB.pairs_block(A.pinned_file(panel, A.PANEL[1]))
        copies = {e[0] for split in pairs.values() for entries in split.values() for e in entries}
        counts["share_with_ktvic_copy_in_pairs"] = len(set(qids) & copies) / len(qids)
    rep = {"label": A.LABEL["ov_test"], "K0_T": k0t, "diag": diag, "counts": counts}
    print(json.dumps({"K0_T": {k: v for k, v in k0t.items() if not k.endswith("failing_ids")}, "counts": counts}))
    Path(str(a.out) + ".t0_report.json").write_text(json.dumps(rep, indent=1) + "\n", encoding="utf-8")
    if not k0t["pass"]:
        raise SystemExit("G4: K0-T fails; the look has been used; every OV-test row is NOT RUN")
    if any(v["refill_share_8"] > AL.REFILL_GATE for v in diag.values()):
        raise SystemExit("G0b: refill share above 0.10 on ov_test; STOP before any decode (the look has been used)")
    print(f"lists_ov_test.json sha256 {write_new(Path(a.out), built, side=True)}")


def cmd_k0dev(_a) -> None:
    """§6.2 N8 in T0's own mode (CC-454 B4): K0 and K0 on the first-look form on OV-dev-B, run by T0's
    interpreter on the test host before T0_READY. No OV-test byte; rc 3 if either fails (no look spent)."""
    mk, mv = A.mem_vectors()
    k0 = dev_b(mk, mv, C.load_lists(A.CL))
    print(json.dumps({k: {x: y for x, y in v.items() if not x.endswith("failing_ids")} for k, v in k0.items()}))
    sys.exit(0 if all(v["pass"] for v in k0.values()) else 3)


def cmd_envcheck(_a) -> None:
    """Block 0's interpreter (venv-cenfeat, freeze 1a639a50; coordinator decision I5): the modules of the feature pass
    import (rc 3 if not), as w25.cmd_imports. Run by the job before block 0, in a dry run too."""
    try:
        import imagehash  # noqa: F401
        import torch  # noqa: F401
        from PIL import Image  # noqa: F401

        import c_conf_lists  # noqa: F401
        import c_pvr_run  # noqa: F401
        import w25  # noqa: F401
    except Exception as e:  # noqa: BLE001 - any failure is a clean STOP before work
        print(f"IMPORT CHECK FAILED: {type(e).__name__}: {e}")
        sys.exit(3)
    print("block-0 imports ok")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("envcheck")
    sub.add_parser("k0dev")
    p = sub.add_parser("block0")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--lists-out", type=Path, required=True)
    p = sub.add_parser("diag")
    p.add_argument("--lists", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("t0")
    p.add_argument("--token", type=Path, required=True)
    p.add_argument("--decision", type=Path, help=f"default: {A.DECISION_NAME} beside the token")
    p.add_argument("--dir", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    {"envcheck": cmd_envcheck, "k0dev": cmd_k0dev, "block0": cmd_block0, "diag": cmd_diag, "t0": cmd_t0}[a.cmd](a)


if __name__ == "__main__":
    main()
