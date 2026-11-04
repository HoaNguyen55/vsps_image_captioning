#!/usr/bin/env python3
"""C-PVR-T1 run stage (Paper C, PVR): owners, lists and the pixel W25 step (prereg PREREG_DRAFT_v1_2 §4.1, §5.6, §7,
§8, §9.1 step 8; CC-236 Q-SPLIT (i)-(iv); run document W25_PIXEL_RUN_DRAFT v0, rulings R1a-R1e, R6).

Interpreter (R1a): ~/.venvs/c_stage1_lists (torch, Pillow, imagehash; the RULE §2 cenfeat freeze). c_pvr.py imports
only the stdlib at module level, so its constants import here without spaCy or rapidfuzz (asserted by the selftest).

    $FT -I -B scripts/c_pvr/c_pvr_run.py selftest [--root R]       CPU, synthetic fixtures, sockets raise
    $FT -I -B scripts/c_pvr/c_pvr_run.py owners --run-sha H         c_pvr_owners.json from HEAD (once)
    $FT -I -B scripts/c_pvr/c_pvr_run.py lists --run-sha H          c_pvr_lists.json (once; ids, keys, lengths)
    $FT -I -B scripts/c_pvr/c_pvr_run.py owner-feats --run-sha H --owners-sha O --sscd PT --in DIR [--owner K]
                                                                    laptop CPU, local files: 'compute' owner caches,
                                                                    then the once-only c_pvr_owner_feats.json
    $FT -I -B scripts/c_pvr/c_pvr_run.py w25 --host laptop --run-sha H --pause-tag T --owners-sha O --feats-sha F
                                         --sscd PT --in DIR

Every subcommand first checks the sha of each imported repo file (CODE), then imports c_pvr, gates, w25 and
build_memory unchanged and uses their constants and functions; no shared constant has a second value here. `w25`
fingerprints (pHash, dHash, mirrored hashes, SSCD, sha256) the G-A remaining NoCaps-test ids and the OpenViVQA-dev
images in tmpfs batches of at most 512 and compares them with the owners' cached fingerprints under RULE §3. No label,
caption, question or answer is read: pixels, ids, keys and container lengths only. Label: TIER 1 / DEV-EXPLORE.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import io
import json
import multiprocessing
import os
import re
import shutil
import signal
import socket
import stat
import subprocess
import sys
import time
import zipfile
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

T0 = time.time()  # process start (module import precedes argv parsing); the pause line must be stamped before it
ROOT = Path(__file__).resolve().parents[2]
PDIR = "manuscript/prereg/2026-11-02_c_pvr_tier1"
PORTFOLIO = "manuscript/directions/PORTFOLIO_3Y_2026-10-29.md"
SELF_REL = "scripts/c_pvr/c_pvr_run.py"
CODE = {  # Q-SPLIT (ii) and the unchanged W25 code closure (draft §2.1); hashed before any of them is imported
    "scripts/c_pvr/c_pvr.py": "8f10bd6097eb60a56e7f4e4bef9cd5d716fbebaa94ee15e4a7cca139caece120",
    "scripts/c_pvr/gates.py": "3bced05e7f718377b34837cfb3f6d6539fb8aafc28bc5f8818e5d7be4ccdf897",
    "scripts/w25/w25.py": "d6d127807929c0534e6140d77831b682e3a7202484fa074d56229e0d091316c0",
    "scripts/c_stage1/build_memory.py": "e771b92df9096e286e8d5de207d3adafe49c8e5e59eab276978b0236cc0eeab9",
    "scripts/c_en/cen_fetch.py": "e51918e958ad86e832dd34fbf5ed86d2f7fc13cf41b602dfe537afa43af4c673",
    "scripts/match_openviic.py": "c0d9dd30e3222ab6542a7e1acfbb9bd3899e4b6db5c896b0adc4d805c1005a8b",
    "scripts/c_stage1/decode_icl.py": "fa5a251160d4fd4fb0cd130af33614283863a84e6ed7905f3da81bb6255010db",
    "scripts/lb/decode_hf_vlm.py": "e2de18811e2ffeb61ed72cb2399d41123e9a8f6ccd73a5ec35f778dcbe2f5ac4",
    "scripts/g2b/decode_qwen3vl.py": "8a855ef483c933621776099b6f9de3b60c4fbfaaf706bb40c74e7d84d9dfb5e5",
    "scripts/grl/common.py": "bbe7ee61f659b1a7bfc3cab418d83ed779b76187107708fef2d8ab44df0ad23a",
}
CP = G = W = BM = np = None  # c_pvr, gates, w25, build_memory, numpy: bound by load() after CODE verifies

SHM, LOCK = Path("/dev/shm/c_pvr_w25"), Path("/dev/shm/c_pvr_w25.lock")  # prereg §8, §8.2
LOST_CAP = {"nocaps_test": 10, "ovqa_dev": 1}  # prereg §8.1: more than this many lost is a FAULT
WALL = 24 * 3600  # prereg §8.3 NB-W25STOP
OVQA_ZIP = "dev-images.zip"
OVQA_RULE = (f"{PDIR}/ovqa_count_rule.json", "c7136a5fd7b092703de06cdaca88519a96810cba28553f06869807a710637115")
OWNERS_FILE, LISTS_FILE = f"{PDIR}/c_pvr_owners.json", f"{PDIR}/c_pvr_lists.json"
OUTS = ("w25_flagged_ids.txt", "w25_lost_ids.txt", "w25_ovqa_out_ids.txt", "w25_f30k_join_ids.txt",
        "w25_counts.json")  # counts last
OWN_BARRED = re.compile(r"gb_intermediate\.json|nocaps_\w*image_info|nocaps_\w*captions", re.I)  # on top of both
FAULT_ERR = re.compile(r"status \d+|redirected|not a JPEG body")  # cen_fetch.get l.242-245 -> FAULT (prereg §8.1)
LOST_ERR = re.compile(r"[A-Za-z_]\w*")  # cen_fetch.get l.248-249: an exception class name -> lost
W25_RX = re.compile(r"(?<![\w-])W25(?![\w-])")
NAME_RX = re.compile(r"[\w][\w.-]{0,127}")  # an OpenViVQA dev image name usable as a tmpfs file name
LIST_RX = re.compile(r"^manuscript/prereg/.+\.(?:txt|tsv|json)$")
SCHEMA = "vsps.c_pvr.owners.v1"
RULE_TEXT = "RULE §3 (289c0a59): C1 byte-identical OR C2 min(pHash,dHash)<=10 AND SSCD>=0.5 OR C3 SSCD>0.75"
T_A_N = 1070  # prereg §4.1 [proposal]: T_A = OpenViVQA dev size, first by sha256(id + "c_pvr_TA")


def fault(msg: str):
    raise SystemExit(f"FAULT: {msg}")


class Stop(SystemExit):
    """prereg §8.3: the 24 h stop; features already made are kept, Q-custody goes to the PI."""


# ---------------------------------------------------------------------------------------------- load and pins
def code_bad(root: Path) -> list[str]:
    """CODE files whose bytes differ from their pins (hashed before import; nothing else is loaded yet)."""
    return [rel for rel, sha in CODE.items()
            if not (root / rel).is_file() or hashlib.sha256((root / rel).read_bytes()).hexdigest() != sha]


def load(root: Path) -> None:
    global CP, G, W, BM, np
    if bad := code_bad(root):
        fault(f"{bad} differ from their pins (Q-SPLIT (ii)); nothing is imported")
    sys.path[:0] = [str(root / "scripts/c_pvr"), str(root / "scripts/w25")]
    import c_pvr as CP  # noqa: E402  OI_TEST_URL, LABEL, SEALED, refuse/BARRED, OVQA_*, curl_argv, ovqa_count
    import gates as G  # noqa: E402  write_new, foreign_jobs, STAMP, PINS_B, oi_rows, pinned, FLICKR_W3, GB_SIGS
    import numpy as np  # noqa: E402
    import w25 as W  # noqa: E402  load, concat, rule, ok_sscd, xm_shas, BATCH, KEYS, F (cen_fetch)
    BM = W.bm()  # build_memory: features (retry_truncated stays False, R1d), near, subset, MO
    me = Path(__file__).resolve()
    stray = sorted(m.__name__ for m in list(sys.modules.values())
                   if (f := getattr(m, "__file__", None)) and Path(f).resolve() != me
                   and Path(f).resolve().is_relative_to(root.resolve())
                   and str(Path(f).resolve().relative_to(root.resolve())) not in CODE)
    if stray:
        fault(f"repo modules outside the pinned closure were imported: {stray}")


def refuse(p) -> Path:
    """c_pvr.refuse and gates.refuse unchanged, plus the G-B sealed file and NoCaps info/caption files."""
    CP.refuse(p)
    G.refuse(p)
    if OWN_BARRED.search(str(p)):
        raise SystemExit(f"REFUSED: {p} (sealed G-B file or NoCaps info/caption file)")
    return Path(p)


def sha(p) -> str:
    return CP.sha_file(refuse(p))


def alog(sealed: Path, action: str, path, digest: str) -> None:
    """An ACCESS_LOG.tsv row in the c_pvr/gates format, fsynced; own writer because both pinned writers hard-code
    their tool name in the second field."""
    with open(sealed / "ACCESS_LOG.tsv", "a") as f:
        f.write(f"{CP.utc()}\tc_pvr_run.py\t{action}\t{path}\t{digest}\n")
        f.flush()
        os.fsync(f.fileno())


def write_new(p: Path, data: bytes, mode: int, check_mode: bool = False) -> str:
    try:
        return G.write_new(refuse(p), data, mode, check_mode)
    except G.GBAbort:
        fault(f"{p}: write failed or exists (one write)")


def integrity(root: Path, run_sha: str) -> None:
    """--run-sha equals this file and its single SHA256SUMS line; every SUMS line verifies (gb_integrity pattern)."""
    if CP.sha_file(Path(__file__)) != run_sha:
        fault("--run-sha differs from sha256 of this c_pvr_run.py")
    lines = (root / "scripts/c_pvr/SHA256SUMS").read_text().splitlines()
    if not all(re.fullmatch(r"[0-9a-f]{64}  \S+", x) for x in lines):
        fault("SHA256SUMS has a malformed line")
    if [x.split()[0] for x in lines if x.split()[1] == SELF_REL] != [run_sha]:
        fault("SHA256SUMS has no single c_pvr_run.py line equal to --run-sha (gatekeeper commit first)")
    if bad := [x.split()[1] for x in lines if sha(root / x.split()[1]) != x.split()[0]]:
        fault(f"SHA256SUMS: {bad} do not verify")


# ---------------------------------------------------------------------------------------------- owners (§7.1, R6)
NOWHERE = "held nowhere: no image or feature cache on any C host (B R5 G4: listed, covered on arrival; not a stop)"
CEN = {"feats_nocaps_val.npz": "b69dac29b4dd07e759d1ff2fc38cb5d716cbe31ddb34c4233ff8f8667b8acba6",
       "feats_coco_test.npz": "2bc3b83ea4116603a041559d35e156f11005c44a910f29100439658593d45934",
       "feats_coco_kval.npz": "9783f7a669aa1b0a6df8e8a78aa3586fb7009f376d8151442ac3acc7da580a7e",
       "feats_memory.npz": "caf4a62199fccfe903e3a553a3717673d62a32ae07a2e289c2a706d70132e437"}  # C-EN SUMS_feats
GAP = {"c7_coco_gap_val2014.npz": "72b1de15618c4e53ad099666257d5810f263e159e32256df2f5599297bef7a3d"}  # LOG l.1317
COCO4 = {k: v for k, v in {**CEN, **GAP}.items() if k != "feats_nocaps_val.npz"}  # one id space, 0 shared ids
CACHE_SPACE = {**{k: "coco" for k in COCO4}, "feats_nocaps_val.npz": "oi", "oiv7_val.npz": "oi", "feats_ut.npz": "coco",
               "uitviic_test.npz": "coco", "t2.npz": "coco", "c7_a_t3_val2017.npz": "coco", "ktvic_test.npz": "ktvic",
               "openviic_test.npz": "openviic", "c7_pascal50s_a.npz": "pascal"}  # B1: a select never mixes spaces
B_OWN = (".session_backup/2026-11-02/b_pa1/b_pa1_owners.json",
         "ae4b663064588a8a19dcd0c01a34284229b40c6de90cd24c88d098b7600b71b2")  # B's frozen owners file (LOG l.1150)
B_RULES = ("manuscript/prereg/2026-11-01_b_pa1_tier1/b_pa1_r5_rules.json",
           "6c5e7282b7f6098b7d49eab3336451b114c48cc8ef5431640a3e632ad6219531")  # B's R5 overlay (untracked; by sha)
_P = "manuscript/prereg/"


def cached(n: int, caches: dict, select: tuple | None = None, note: str = "") -> dict:
    return {"status": "cached", "n": n, "caches": caches, "select": list(select) if select else None, "note": note}


def b_sel(n: int, key: str, note: str = "") -> dict:
    """A COCO owner selected by id from B's frozen owners file (CC-245 Ruling 8) over the four COCO caches."""
    return cached(n, dict(COCO4), (*B_OWN, f"owners/{key}/ids"), note)


def compute(n: int, source: tuple, folder: str, name: str, note: str = "") -> dict:
    """Featured by `owner-feats` from local files (laptop CPU), listed in its once-only manifest."""
    return {"status": "compute", "n": n, "source": list(source), "dir": folder, "name": name, "note": note}


def deferred(reason: str) -> dict:
    return {"status": "deferred", "reason": reason}


OWNERS = {  # every earlier owner of prereg §7.1 / PORTFOLIO §2.3 / prereg lists at HEAD; shas = laptop bytes 11-03
    "nocaps_val_4500": cached(4500, {"feats_nocaps_val.npz": CEN["feats_nocaps_val.npz"]},
                              note="C-EN; includes the 43 XM3600 rows"),
    "oiv7_val_41164": cached(41164, {"oiv7_val.npz": "2ca7e2f56bc3695dc4be13f10d4511881e4460d6d0815c27a6ab1220d8e7c5bb"},
                             note="W25-K1 input: L2-P1 36,707 + NoCaps val 4,457"),
    "karpathy_test_5000": cached(5000, {"feats_coco_test.npz": CEN["feats_coco_test.npz"]}, note="KT-C, M0 probes 91"),
    "kv5000": cached(5000, {"feats_coco_kval.npz": CEN["feats_coco_kval.npz"]}, note="superset of KV-4,224"),
    "ut2402": cached(2402, {"feats_ut.npz": "17d3ebf07ebf95bcd0c8bf123ff65fb8f2df65c52cd4e17ac492e05976b98c1d"}),
    "uitviic_test_231": cached(231, {"uitviic_test.npz":
                                     "4f4784903fb0164309a3b1b6b3ba4fbaa9c09da6c4be5294a6c43f75581ff95f"}),
    "ktvic_test_558": cached(558, {"ktvic_test.npz": "cd985050fd2042b87049410334a05a6406b4363d69c05a45e6ed28ccae86702d"}),
    "openviic_test_2001": cached(2001, {"openviic_test.npz":
                                        "f4c79b825a1b62256dfac15b6ce59bce1054b83386ab4d5d932ac3c4e73d360e"}),
    "t2_2000": cached(2000, {"t2.npz": "98f61bae0c8e03c389db3563a5e6fbec7aa1a6f531a38d027f7c5ed54aba4268"}),
    "a_t3_val2017": cached(5000, {"c7_a_t3_val2017.npz":
                                  "95144514c601007b512528e7478140f3df9a91885ef40027dd4f6e3136a2ce80"}),
    "coco_gap_val2014_734": cached(734, dict(GAP)),
    "pascal50s_a": cached(1000, {"c7_pascal50s_a.npz":
                                 "00ef39757bb11fa2ac0333ba7b5304a855f41fc91dca39ee8349c4b6337b0c94"}),
    "uitviic_val_924": b_sel(924, "uitviic_val_924"),
    "m0_dev_touched_3454": b_sel(3454, "m0_dev_touched_3454", "61 ids sit only in the gap cache"),
    "coco_restval_b4": b_sel(30504, "coco_restval_b4"),
    "uitviic_train_pool": b_sel(2695, "uitviic_train_pool"),
    **{f"refused_{k}": b_sel(n, f"refused_{k}", "exclusion.json refused list")
       for k, n in (("chair500", 500), ("coco2500", 2500), ("cv295", 295), ("pope500", 500))},
    "xm3600_all": compute(3600, (f"{PDIR}/xm3600_all_ids.txt",
                                 "1bd00f466afc196ab51a6b86d3c1a5b6ea1e553393362b98199aa892287e1922", None),
                          "data/datasets/xm3600/images", "jpg"),
    "vitextvqa_dev": compute(1520, (_P + "2026-10-29_l1a/l1a_lists.json",
                                    "ac5ed047dc013cb642a325b491994d516ff8ee187c26f30fa47c0b62057e0087",
                                    "dev/image_sha256"), "data/datasets/l1a_vitextvqa_dev/images", "file",
                             "the L1a-spent dev images (N10: n from the pinned list, not the json's 1,676)"),
    "ktvic_dev299": compute(299, (_P + "2026-10-21_dev_pools/ktvic_dev299.tsv",
                                  "a4ac7fdbd904f2205845705f5235b9748225a83a07854b58e59a755b85e4186e", None),
                            "data/datasets/ktvic/images", "ktvic"),
    "refused_ktvic_dup": compute(1, (_P + "2026-10-21_dev_pools/exclusion.json",
                                     "c52a96d18925b974878ae1a970c3f9133fb3482216676fd41871eeabb68cc77f",
                                     "ids/ktvic/ktvic_dev_near_duplicate_of_test"), "data/datasets/ktvic/images",
                                 "ktvic"),
    "h_bdt1_739": compute(739, (_P + "2026-10-30_bd_t1/bd_t1_lists.json",
                                "b6bbce8f2fa1934c76dcc6005a2d69ff196e8686aa0bd9cc2614d5603b985a17", "H/ids+T2/ids"),
                          "data/datasets/ktvic/images", "ktvic", "C's 'B's H' = BD-T1 H + T2 (PI-1103aa, CC-245 Q1)"),
    "openviic_dev_c1": compute(1836, (_P + "2026-10-22_c_stage1/lists.json",
                                      "5c479f03e8be544f4cd12b5d997b5dc92b6c622df061760cd02f6ba82f6b4371",
                                      "sets/ov_dev_a+sets/ov_dev_b"), "data/datasets/openviic/images", "file",
                               "C stage-1 spent OpenViIC dev A/B"),
    "flickr30k_c_t3_carve": {"status": "id_join", "n": 1000,
                             "source": [_P + "2026-10-30_c_t1/c_t1_f30k_lists.json",
                                        "eebcd95b78b1dc98398550b1f89fea5622e8cbd9f20ad6b07b0d9292ba745968", "carve"],
                             "note": "spent at C-T3 tier 3 (LOG l.982); Flickr photo id join via gates.landing_ids; "
                                     "hits reported beside n_e_power, not in it (CC-245 Ruling 9)"},
    "ade20k_val": deferred(NOWHERE + "; the M1 copy was lost 10-29"),
    "a_t1_dev_ade20k": deferred(NOWHERE + "; A-T1 D1/D2 dev drawn from ADE20K train"),
    "vitextvqa_test": deferred("no test id list held (the images may sit in ViTextVQA_images.zip); B R5 G4"),
    "b_pa1_dev_contacts": deferred("not yet written (B v3.1 §3, N11); an owner for later passes; B R5 G4"),
    **{k: deferred(NOWHERE) for k in ("amber_generative", "mtvqa_test", "textvqa_textcaps_val", "vintext_test",
                                      "viocrvqa_test", "visignvqa_test", "vindr_cxr_test", "vizwiz_val",
                                      "longcap_polaris_docci_thumb_composite_vapr")},
}
SELF = "self: C's own one-look or conditional set (the query side, never an owner of itself)"
LATER = ("skip: §2.3 owner B5 (unregistered) at HEAD; Paper B v3.1 (5ff00c9, 11-02 07:11 +07) if the pending hunk "
         "lands; both later than C 8282874 (11-02 05:48 +07), so B drops the overlap")
LEDGER = {  # PORTFOLIO §2.3 table row (first cell, verbatim at HEAD) -> owner key, self or skip
    "PASCAL-50S": "pascal50s_a",
    "KV-4,224 (COCO Karpathy val)": "kv5000",
    "ViTextCaps test": SELF,
    "NoCaps test (10,600; EvalAI)": SELF,
    "OpenViVQA dev (1,070 images / 3,545 QA)": SELF,
    "VieCap4H private test": SELF,
    "Flickr30K Karpathy test": SELF,
    "H = 500 KTVIC-train ∩ OV-train-only": "h_bdt1_739",
    "ADE20K SceneParsing val (2,000) + LN-ADE val": "ade20k_val",
    "AMBER generative (1,004)": "amber_generative",
    "OIV7 val − 456 XM ids − 4,457 NoCaps val ids (36,707)": "oiv7_val_41164",
    "COCO Karpathy restval (about 30.5k) + VG relations": "coco_restval_b4",
    "Objects365 v2 val": LATER,
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
SPENT = {  # PORTFOLIO §2.3 prose entries (each must occur in §2.3 at HEAD) -> owner keys
    "XM3600 (all)": ["xm3600_all"], "UIT-ViIC test and val": ["uitviic_test_231", "uitviic_val_924"],
    "KTVIC test": ["ktvic_test_558"], "OV-test": ["openviic_test_2001"], "COCO Karpathy test": ["karpathy_test_5000"],
    "nocaps val (C tier-2 dev-confirm rehearsal": ["nocaps_val_4500"],
    "LongCap/Polaris/DOCCI/THumB/Composite/VaPR": ["longcap_polaris_docci_thumb_composite_vapr"],
    "VSPS-J M0 dev-touched": ["m0_dev_touched_3454"], "VSPS-J M0 probes 91 Karpathy-test images": ["karpathy_test_5000"],
    "E1a decodes all 231 UIT-ViIC test images": ["uitviic_test_231"], "T2-2000": ["t2_2000"],
    "A-T3 val2017 593": ["a_t3_val2017"], "UT-2,402": ["ut2402"],
}
EXTRA = {"vitextvqa_dev": "prereg §7.1, §4.3 (proxy earlier owner)",
         "coco_gap_val2014_734": "W25 draft §1.3 (B's C7 cache, LOG l.1317); an extra owner only flags more"}
B_MAP = {  # B R5 owners (b_pa1_r5_rules.json) -> C owner key, self or skip (CC-245 B2 cross-check)
    "a_t3_val2017": "a_t3_val2017", "ade20k_val_a": "ade20k_val", "amber_generative": "amber_generative",
    "b_pa1_dev_contacts": "b_pa1_dev_contacts", "c1": SELF, "c2": SELF, "coco_restval_b4": "coco_restval_b4",
    "docci": "longcap_polaris_docci_thumb_composite_vapr",
    "flickr30k_test_c": "flickr30k_c_t3_carve",  # B's row cites LOG l.982 = the C-T3 carve
    "h500": "h_bdt1_739",
    "karpathy_test_5000": "karpathy_test_5000", "ktvic_test_558": "ktvic_test_558", "kv4224_mt4": "kv5000",
    "longcap": "longcap_polaris_docci_thumb_composite_vapr", "m0_dev_touched_3454": "m0_dev_touched_3454",
    "m0_karpathy_test_probes_91": "karpathy_test_5000", "mtvqa_test": "mtvqa_test", "nocaps_test_c": SELF,
    "nocaps_val": "nocaps_val_4500", "oiv7_val": "oiv7_val_41164", "openvivqa_dev_c": SELF,
    "ov_test_c": "openviic_test_2001", "pascal50s_a": "pascal50s_a", "refused_chair500": "refused_chair500",
    "refused_coco2500": "refused_coco2500", "refused_cv295": "refused_cv295", "refused_pope500": "refused_pope500",
    "refused_ktvic_dev_near_duplicate_of_test": "refused_ktvic_dup", "textvqa_textcaps_val": "textvqa_textcaps_val",
    "thumb": "longcap_polaris_docci_thumb_composite_vapr", "uitviic_test_231": "uitviic_test_231",
    "uitviic_train_pool": "uitviic_train_pool", "uitviic_val_924": "uitviic_val_924", "ut2402": "ut2402",
    "vapr": "longcap_polaris_docci_thumb_composite_vapr", "vindr_cxr_test": "vindr_cxr_test",
    "vintext_test": "vintext_test", "viocrvqa_test": "viocrvqa_test", "visignvqa_test": "visignvqa_test",
    "vitextvqa_test": "vitextvqa_test", "vizwiz_val": "vizwiz_val", "xm3600_all": "xm3600_all",
    "xm600_a": "xm3600_all", "xm_test2500_c": "xm3600_all"}
_NOT = "skip: not an image id list"
_REC = "skip: a record (gate, manifest, prediction, score, count or scan file), not an owner list; not hashed"
_TRAIN = "skip: training-side pools or levels (not a one-look or spent set)"
_S35 = "skip: training pools; their dev300 gate = ktvic_dev299 ∪ refused_ktvic_dup (owners)"
_RECORDS = """:2026-10-12_ladder_predictions 2026-10-14_b1_qwen3vl_predictions 2026-10-14_xm3600_predictions
2026-10-15_q2_longcap_arena 2026-10-15_q4_vapr_count_control 2026-10-18_g2b_qwen3vl_ladder
2026-10-18_n9_count_matched_leaderboard 2026-10-18_never_committed_frozen_files 2026-10-18_tier3_S1
2026-10-18_tier3_S1_instrument 2026-10-18_tier3_S2 2026-10-18_tier3_S2_instrument 2026-10-18_tier3_S3_amendment1
2026-10-18_tier3_S3_instrument 2026-10-18_tier3_S5_instrument 2026-10-19_a_n2_lvlm_gold_ladder
2026-10-19_a_n3_criterion_mhaldetect 2026-10-19_an1_g2b_addendum 2026-10-19_b_n1_vi_leaderboard
2026-10-19_b_n2_leakage_did_prereg_v2 2026-10-20_b_f1_final_stack 2026-10-20_b_f1_instrument
2026-10-19_a_n2_record/:a_n2_dryrun_synthetic a_n2_gate
2026-10-19_a_n3_record/:a_n3_dryrun_synthetic a_n3_gate
2026-10-19_an1_stage1/:ADDENDUM_DRAFT MANIFEST MANIFEST_v2 dryrun_stage1_standins dryrun_stage1_standins_v2
 stage1_diagnostic stage1_results
2026-10-19_b_n1_record/:b_n1_dryrun_synthetic b_n1_gate
2026-10-19_b_n2_record/:b_n2_absence_check b_n2_absence_check_stage1 b_n2_dryrun_synthetic b_n2_gate
2026-10-20_b_f1_record/:b_f1_dryrun_synthetic b_f1_gate
2026-10-21_n_f1_bracket/:MANIFEST gate run_record selftest
2026-10-21_n_m3_caphit/:MANIFEST gate selftest verify_out
2026-10-21_scar_null/:MANIFEST gate selftest
2026-10-22_c_stage2/:frozen_config
2026-10-26_b_posthoc/:c3_dryrun_synthetic
2026-10-27_c_en/:lists_record_coco lists_record_nocaps
2026-10-27_grl_pilot/:gold_instances id_counts
2026-10-28_k2_gate1/:w25_decide
2026-10-29_b_d0/:d0_decide
2026-10-29_b_r1/:d0_reread
2026-10-29_l1b/:GATES l1b_registry
2026-10-30_a_t3/:a_t3_registry a_t3_w2_dev_drops a_t3_w3_gate
2026-10-30_a_t3/r9/:a_t3_w2_posctl a_t3_w2_test_drops prep_report
2026-10-30_bd_t1/:bd_t1_sscd
2026-10-30_c_t1/:c_t1_registry
2026-10-30_mt4_k1k6/:GATES caps power_planning t1_select t2_decide w25k1_decide
2026-10-31_vsps_j_e1e2/:e1e2_plan
2026-10-31_vsps_j_m0/:m0_plan
2026-11-01_vsps_j_e2b_tier1/:e2b_w25_decide
2026-11-02_c_pvr_tier1/:G_C1_record G_C2_record g_c2_provenance ga_counts gb_counts llava_mix665k.scan
 mblip_capfilt_raw.scan mblip_mix_v1.scan mblip_mix_v2.scan ovqa_count_rule ovqa_pin"""


def _records(text: str) -> dict:
    out = {}
    for block in re.split(r"\n(?=[^ \n]*:)", text):
        d, _, names = block.partition(":")
        out |= {f"{_P}{d}{n}.json": _REC for n in names.split()}
    return out


LISTS = {  # every *.txt / *.tsv / *.json under manuscript/prereg at HEAD -> owner key(s), self or skip (B2)
    _P + "2026-10-12_frontier_invariance_V4.txt": _NOT + " (prereg text)",
    **{f"{_P}2026-10-12_vietnamese_diagnostics/{n}.tsv": _NOT + " (term table)"
       for n in ("culture_terms", "frames", "person_terms", "quantifiers")},
    _P + "2026-10-21_dev_pools/ktvic_dev299.tsv": "ktvic_dev299",
    _P + "2026-10-21_dev_pools/uitviic_val.tsv": "uitviic_val_924",
    _P + "2026-10-21_dev_pools/exclusion.json": ["ktvic_test_558", "refused_ktvic_dup", "uitviic_test_231",
                                                 "refused_cv295", "refused_coco2500", "karpathy_test_5000",
                                                 "refused_chair500", "refused_pope500", "xm3600_all"],
    _P + "2026-10-22_c_stage1/lists.json": ["openviic_dev_c1", "xm3600_all"],
    _P + "2026-10-22_c_stage2/ov_test_dev299_neardup_files.txt": "openviic_test_2001",
    _P + "2026-10-22_e_stage1/e_dev_a_pair_images.tsv": "xm3600_all",
    _P + "2026-10-22_e_stage1/e_split.json": "xm3600_all",
    _P + "2026-10-23_eprime_pilot/xm_dev300.tsv": "xm3600_all",
    _P + "2026-10-25_c_test/ov_test_files.tsv": "openviic_test_2001",
    _P + "2026-10-25_c_test/ov_test_primary1941.txt": "openviic_test_2001",
    _P + "2026-10-25_c_test/xm_test2500_threeref108.txt": "xm3600_all",
    _P + "2026-10-27_c_en/cen_coco_kval.tsv": "kv5000",
    _P + "2026-10-27_c_en/cen_coco_test.tsv": "karpathy_test_5000",
    _P + "2026-10-27_c_en/cen_memory_allowed.tsv": "skip: D-EN, C's own datastore; prereg §7.3 count (c), never an owner",
    _P + "2026-10-27_c_en/cen_nocaps_val.tsv": "nocaps_val_4500",
    _P + "2026-10-27_c_en/cen_nocaps_vg1000.txt": "nocaps_val_4500",
    _P + "2026-10-27_c_en/cenfeat_venv_freeze.txt": _NOT + " (pip freeze)",
    _P + "2026-10-27_grl_pilot/kv5000.txt": "kv5000",
    _P + "2026-10-27_grl_pilot/ut2402.txt": "ut2402",
    _P + "2026-10-27_grl_pilot/ut2532.txt": ["ut2402", "kv5000"],
    _P + "2026-10-27_grl_pilot/val924.txt": "uitviic_val_924",
    _P + "2026-10-28_k2_gate1/w25_excluded_ids.txt": "ut2402",
    _P + "2026-10-28_w25_neardup/oiv7_val_ids.txt": "oiv7_val_41164",
    _P + "2026-10-28_w25_neardup/xm3600_in_oiv7_val_ids.txt": "xm3600_all",
    _P + "2026-10-18_tier3_S3.json": _S35,
    _P + "2026-10-18_tier3_S5.json": _S35,
    _P + "2026-10-30_mt4_k1k6/k1k6_lists.json": "skip: record; its ids sit in t2_ids.txt (owner t2_2000)",
    _P + "2026-11-01_vsps_j_e2b_tier1/e2b_w25_lists.json": "skip: record; its ids sit in the COCO owners",
    **{_P + p: _TRAIN for p in ("2026-10-28_b1_scaling/b1_lists.json", "2026-10-28_c2_ablation/c2_memory_subsets.json",
                                "2026-10-29_b_r1/r1_lists.json")},
    **{_P + f"2026-10-29_{p}.json": "vitextvqa_dev" for p in ("l1a/l1a_lists", "l1a/neardup", "l1b/l1b_split")},
    _P + "2026-10-30_a_t1/a_t1_lists.json": "a_t1_dev_ade20k",
    _P + "2026-10-30_a_t3/a_t3_lists.json": "coco_restval_b4",
    **{f"{_P}2026-10-30_a_t3/r9/{n}.txt": "a_t3_val2017"
       for n in ("decoded_any_a1precheck", "decoded_any_an3", "decoded_any_full", "dev_test", "w2_test",
                 "flickr_ids")},  # flickr_ids.txt holds 6 COCO val2017 ids (an A-T3 drop file), not Flickr ids
    _P + "2026-10-30_a_t3/r9/a_t3_testlist_r9_drop_all.json": "a_t3_val2017",
    _P + "2026-10-30_a_t3/val2017_ids.txt": "a_t3_val2017",
    _P + "2026-10-30_bd_t1/bd_t1_lists.json": "h_bdt1_739",
    _P + "2026-10-30_c_t1/c_t1_f30k_lists.json": ["flickr30k_c_t3_carve", SELF],
    _P + "2026-10-30_mt4_k1k6/t2_ids.txt": "t2_2000",
    _P + "2026-10-30_mt4_k1k6/t2_gold.json": "t2_2000",
    _P + "2026-10-30_mt4_k1k6/w25k1_excluded_keys.txt": "skip: W25-K1 output (excluded training keys), not a set",
    **{f"{_P}2026-10-31_vsps_j_m0/{n}.txt": "m0_dev_touched_3454"
       for n in ("dev_touched_ids", "dropped_ids", "fetch_images", "selection_excluded_ids", "train_ids", "val_ids")},
    _P + "2026-10-31_vsps_j_m0/karpathy_test_val_ids.txt": "karpathy_test_5000",
    _P + "2026-11-01_vsps_j_e2b_tier1/e2b_plan.json": "m0_dev_touched_3454",
    _P + "2026-11-02_c_pvr_tier1/ga_remaining_ids.txt": SELF,
    _P + "2026-11-02_c_pvr_tier1/xm3600_all_ids.txt": "xm3600_all",
    **_records(_RECORDS),
}
STATUSES = ("cached", "compute", "deferred", "id_join")
OWN_RX = re.compile(r"(?:self|skip): ")


def ledger(text: str) -> tuple[str, list[str]]:
    """PORTFOLIO §2.3 section text and its table's first cells (header dropped)."""
    if "\n### 2.3 " not in text:
        fault("PORTFOLIO has no §2.3")
    sec = text.split("\n### 2.3 ", 1)[1].split("\n### ", 1)[0]
    return sec, [r.split("|")[1].strip() for r in sec.splitlines() if r.startswith("| ")][1:]


def id_lines(b: bytes) -> list[str]:
    return [x.split("\t")[0] for x in b.decode("utf-8").splitlines() if x.strip() and not x.startswith("#")]


def ids_of(b: bytes, jpath: str | None) -> list[str]:
    """Ids of a pinned list: column 1 of a text list, or json paths joined by '+' (dict -> keys; [id, ...] -> id).
    No other field of the record is read."""
    if jpath is None:
        return id_lines(b)
    d, out = json.loads(b), []
    for path in jpath.split("+"):
        v = d
        for k in path.split("/"):
            v = v[k]
        out += [str(x[0] if isinstance(x, list) else x) for x in (list(v) if isinstance(v, dict) else v)]
    return out


def pinned_ids(read, src: list) -> list[str]:
    rel, want, jpath = src
    b = read(rel)
    if G.sha_bytes(b) != want:
        fault(f"{rel} differs from its pin {want[:8]}")
    return ids_of(b, jpath)


def owner_ok(k: str, o: dict, disk) -> None:
    st = o.get("status")
    if st not in STATUSES:
        fault(f"owner {k}: status {st!r} is not one of {STATUSES} (R6)")
    if st == "deferred" and not o.get("reason"):
        fault(f"owner {k}: deferred without a reason (R6)")
    if st in ("compute", "id_join") and len(set(pinned_ids(disk, o["source"]))) != o["n"]:
        fault(f"owner {k}: its source list does not hold n = {o['n']} distinct ids")
    if st != "cached":
        return
    if not o["caches"] or not all(re.fullmatch(r"[0-9a-f]{64}", h) for h in o["caches"].values()) or o["n"] < 1:
        fault(f"owner {k}: a cached owner needs caches with full sha256 values and n >= 1")
    if len({CACHE_SPACE.get(c) for c in o["caches"]}) != 1 or None in {CACHE_SPACE.get(c) for c in o["caches"]}:
        fault(f"owner {k}: its caches are not of one known id space (CC-245 B1)")
    if o["select"] and len(set(pinned_ids(disk, o["select"]))) != o["n"]:
        fault(f"owner {k}: select list does not hold n = {o['n']} distinct ids")


def mapped(v) -> list[str]:
    return v if isinstance(v, list) else [v]


def build_owners(read, ls, head: str, reg: tuple | None = None, disk=None) -> bytes:
    """R6 at HEAD: every §2.3 row, listed prose entry, prereg list (.txt/.tsv/.json) and B R5 owner maps to an owner or
    a stated self/skip; every owner is cached, compute, deferred or id_join; nothing dangles. Never a closed list."""
    owners, ldg, lists, spent, extra, bmap, brules = reg or (OWNERS, LEDGER, LISTS, SPENT, EXTRA, B_MAP, B_RULES)
    disk = disk or read
    port = read(PORTFOLIO)
    sec, rows = ledger(port.decode("utf-8"))
    if sorted(rows) != sorted(ldg) or len(rows) != len(set(rows)):
        fault(f"PORTFOLIO §2.3 rows changed; unmapped {sorted(set(rows) - set(ldg))}, gone {sorted(set(ldg) - set(rows))}")
    have = sorted(x for x in ls() if LIST_RX.search(x))
    if have != sorted(lists):
        fault(f"prereg lists changed; unmapped {sorted(set(have) - set(lists))}, gone {sorted(set(lists) - set(have))}")
    if miss := [p for p in spent if p not in sec]:
        fault(f"PORTFOLIO §2.3 no longer names {miss}")
    b = disk(brules[0])
    if G.sha_bytes(b) != brules[1] or sorted(json.loads(b)["owners"]) != sorted(bmap):
        fault("B R5 owners differ from the pinned overlay or from B_MAP (CC-245 B2)")
    refs = {*ldg.values(), *(x for v in lists.values() for x in mapped(v)), *(k for v in spent.values() for k in v),
            *extra, *bmap.values()}
    dangling = sorted(v for v in refs if v not in owners and not OWN_RX.match(v))
    orphans = sorted(set(owners) - refs)
    if dangling or orphans:
        fault(f"owner registry: dangling {dangling}, orphans {orphans}")
    for k in sorted(owners):
        owner_ok(k, owners[k], disk)
    doc = {"schema": SCHEMA, "label": CP.LABEL, "head": head, "rule": "prereg §7.1-§7.2, R6, CC-245",
           "portfolio": {"path": PORTFOLIO, "blob_sha256": G.sha_bytes(port)}, "ledger": ldg, "spent": spent,
           "extra": extra, "b_r5_map": bmap, "b_r5_overlay": {"path": brules[0], "sha256": brules[1]},
           "b_owners_file": {"path": B_OWN[0], "sha256": B_OWN[1]},
           "lists": {p: {"to": v, **({} if all(OWN_RX.match(x) for x in mapped(v)) else {"sha256": G.sha_bytes(read(p))})}
                     for p, v in sorted(lists.items())}, "owners": owners}
    return G.jdump(doc)


def git(root: Path, *a: str) -> bytes:
    r = subprocess.run(["git", "-C", str(root), *a], capture_output=True)
    if r.returncode:
        fault(f"git {a[0]} failed")
    return r.stdout


def disk_reader(root: Path):
    return lambda rel: refuse(root / rel).read_bytes()


def cmd_owners(root: Path, sealed: Path) -> None:
    head = git(root, "rev-parse", "HEAD").decode().strip()
    data = build_owners(lambda rel: git(root, "show", f"HEAD:{rel}"),
                        lambda: git(root, "ls-tree", "-r", "--name-only", "HEAD", "manuscript/prereg").decode().split(
                            "\n"), head, disk=disk_reader(root))
    h = write_new(root / OWNERS_FILE, data, 0o444)
    alog(sealed, "owners write", OWNERS_FILE, h)
    st = Counter(o["status"] for o in json.loads(data)["owners"].values())
    print(json.dumps({"label": CP.LABEL, "owners_sha256": h, "head": head, "status": dict(st)}, sort_keys=True))


# ---------------------------------------------------------------------------------------------- lists (§4.1-§4.2, §7.4)
LISTS_IN = {  # pinned inputs; None = not on the laptop yet: `lists` FAULTs before writing anything
    "ktvic_test": ("data/datasets/ktvic/test_data.json",
                   "cc22ec6a8883773cb23c87ad5b64925f5a53c21982117274b53621f454e7ebbf"),
    "openviic_test": ("data/datasets/openviic/uit-openviic-annotation-test.json",
                      "66af01bac79af9e197f934ba3628477d5324506092d9a13dfd35330596310b16"),
    "vitextvqa_dev": ("data/datasets/vitextvqa_raw/ViTextVQA_dev.json",
                      "c6ab6a7babceb5928e393ec4cc7461c68b35f4fb19ec1a39e9366318be876b81"),
    "ktvic_train": ("data/datasets/ktvic/train_data.json",
                    "72ee9b57c350fb5f215e1f04701c515a51e5e415240e51a77c8ce00ce6316a0f"),
    "openviic_train": ("data/datasets/openviic/uit-openviic-annotation-train.json",
                       "d757520e76b8490df6c7275c2beb8b3ecef0342635a436bea8c3cfd07eb49df0"),
    "copy_map": ("data/ktvic_openviic_refs.json", "4eb02cc43841bae4f844ee74d4c01b58e677dc8d6abafdd998c9f5b5706f725d"),
    "textcaps_train": ("data/splits/textcaps_train_ids.txt",  # TextCaps train ids, 21,953 (CC-247; LOG OPS-1104c-textcaps-pin)
                       "2da2b395ef508be19098c2f558c27da3cb93e873528ba6bb82d94a549037e4b8"),
}
DVI_KT = ("h_bdt1_739", "ktvic_dev299", "refused_ktvic_dup")  # KTVIC-train owners leaving D-VI (B3; PI-1103aa)
DVI_OV = ("openviic_dev_c1",)  # OpenViIC-file owners: a KTVIC image copied to one of them leaves D-VI too
KT_ID, OV_KEY = re.compile(r"[1-9]\d*"), re.compile(r"\d{11}\.(?:jpg|jpeg|png|JPG|PNG)")  # 11-digit stem + its own extension


def half(i: str) -> bool:
    """prereg §4.2 NB-PARITYBIT: explore (tier 1) iff the last hex digit of sha256(id + 'c_pvr') is even."""
    return int(hashlib.sha256((i + "c_pvr").encode("utf-8")).hexdigest()[-1], 16) % 2 == 0


def split_counts(ids: list[str], n: int, what: str) -> dict:
    if len(ids) != n or len(set(ids)) != n:
        fault(f"{what}: {len(set(ids))} distinct ids, not {n}")
    e = sum(map(half, ids))
    return {"explore": e, "confirm": n - e}


def kt_ids(images: list) -> list[str]:
    """KTVIC native id (CC-245 Ruling 11): str of the integer images[].id, no padding."""
    if not all(type(r["id"]) is int for r in images):
        fault("a KTVIC image id is not an int")
    return [str(r["id"]) for r in images]


def ov_keys(d: dict) -> list[str]:
    """OpenViIC native id: the json top-level key as-is (11 digits + the file's own extension: .jpg, .jpeg, .png,
    .JPG or .PNG, as the train and test jsons hold them)."""
    if not all(OV_KEY.fullmatch(k) for k in d):
        fault("an OpenViIC key is not an 11-digit image file name")
    return list(d)


SPLITS = {"train", "dev", "test", "uncaptioned"}  # copy-map entry splits (4eb02cc4)


def copy_graph(pairs: dict, kt_train: set, kt_test: set) -> dict:
    """The KTVIC<->OpenViIC copy map as an undirected graph (CC-245r2 B3a/B3b). Every entry of _pairs.train and
    _pairs.test is [OpenViIC file, split, int, int, float]; only e[0] and e[1] are read (the shape is asserted)."""
    if set(pairs["test"]) != kt_test or not set(pairs["train"]) <= kt_train:
        fault("copy map keys are not the KTVIC test ids / a subset of the KTVIC train ids")
    adj: dict = {}
    for split in ("train", "test"):
        for k, es in pairs[split].items():
            for e in es:
                if len(e) != 5 or not isinstance(e[0], str) or not OV_KEY.fullmatch(e[0]) or e[1] not in SPLITS:
                    fault("a copy-map entry is not [11-digit image file, split, int, int, float]")
                adj.setdefault(("k", k), set()).add(("o", e[0]))
                adj.setdefault(("o", e[0]), set()).add(("k", k))
    return adj


def reach(adj: dict, seeds: set) -> set:
    """The closure: every node in a component that holds a seed."""
    seen, frontier = set(seeds), list(seeds)
    while frontier:
        nxt = {m for n in frontier for m in adj.get(n, ()) if m not in seen}
        seen |= nxt
        frontier = list(nxt)
    return seen


def dvi(kr_ids: set, ovr: set, kt_test: set, ov_test: set, pairs: dict, kt_own: dict, ov_own: set) -> dict:
    """D-VI = (KTVIC train ∪ OpenViIC train) minus every image in a copy-map component seeded by an owner image on
    either side: KTVIC-side owners, every KTVIC test id, the OpenViIC owner files and the OpenViIC test keys
    (prereg §7.4; CC-245 B3, CC-245r2 B3b). Counts per source are kept apart, plus the distinct union."""
    adj = copy_graph(pairs, kr_ids, kt_test)
    if bad := sorted(k for k, v in kt_own.items() if not v <= kr_ids):
        fault(f"{bad}: ids that are not KTVIC train image ids")
    src = {"ktvic_owners": {("k", i) for v in kt_own.values() for i in v}, "ktvic_test_side": {("k", i) for i in kt_test},
           "openviic_owners": {("o", f) for f in ov_own | ov_test}}
    side = lambda nodes: {"ktvic_train": len({i for t, i in nodes if t == "k"} & kr_ids),  # noqa: E731
                          "openviic_train": len({f for t, f in nodes if t == "o"} & ovr)}
    seeds = set().union(*src.values())
    gone = reach(adj, seeds)
    one_hop = seeds | {m for n in seeds for m in adj.get(n, ())}
    kept_kt, kept_ov = kr_ids - {i for t, i in gone if t == "k"}, ovr - {f for t, f in gone if t == "o"}
    return {"kept_kt": kept_kt, "kept_ov": kept_ov, "counts": {
        "removed": side(gone), "removed_by_source": {k: side(reach(adj, v)) for k, v in src.items()},
        "removed_hop_only": side(gone - one_hop), "ktvic_owner_ids": {k: len(v) for k, v in kt_own.items()},
        "ktvic_owner_ids_distinct": len(set().union(*kt_own.values()))}}


def build_lists(root: Path, pins: dict, owners: dict) -> dict:
    """Counts from keys, ids and container lengths only; no caption, question or answer field is accessed."""
    if miss := sorted(k for k, v in pins.items() if v is None):
        fault(f"lists: inputs not pinned {miss}; c_pvr_lists.json is not written")

    def get(k: str) -> bytes:
        rel, want = pins[k]
        if sha(root / rel) != want:
            fault(f"{rel} differs from its pin {want[:8]}")
        return (root / rel).read_bytes()

    disk = disk_reader(root)
    kt, kr = json.loads(get("ktvic_test")), json.loads(get("ktvic_train"))
    ov_test, ov_train = json.loads(get("openviic_test")), json.loads(get("openviic_train"))
    kt_test = kt_ids(kt["images"])
    halves = {"ktvic_test": split_counts(kt_test, 558, "KTVIC test"),
              "openviic_test": split_counts(ov_keys(ov_test), 2001, "OpenViIC test")}
    d = dvi(set(kt_ids(kr["images"])), set(ov_keys(ov_train)), set(kt_test), set(ov_keys(ov_test)),
            json.loads(get("copy_map"))["_pairs"], {k: set(pinned_ids(disk, owners[k]["source"])) for k in DVI_KT},
            set().union(*(pinned_ids(disk, owners[k]["source"]) for k in DVI_OV)))
    tc = id_lines(get("textcaps_train"))
    t_a = sorted(tc, key=lambda i: (hashlib.sha256((i + "c_pvr_TA").encode("utf-8")).hexdigest(), i))[:T_A_N]
    if len(set(tc)) != len(tc) or len(t_a) != T_A_N:
        fault("TextCaps train ids are not distinct or fewer than T_A")
    keep_kt, keep_ov = d["kept_kt"], d["kept_ov"]
    return {"label": CP.LABEL, "utc": CP.utc(), "inputs": {k: v[1] for k, v in pins.items()},
            "halves": halves, "vitextvqa_dev_images": len({str(r["id"]) for r in json.loads(get("vitextvqa_dev"))["images"]}),
            "d_vi": {"ktvic_train_images": len(keep_kt), "openviic_train_images": len(keep_ov), **d["counts"],
                     "ktvic_train_captions": sum(str(a["image_id"]) in keep_kt for a in kr["annotations"]),
                     "openviic_train_captions": sum(len(ov_train[f]["captions"]) for f in keep_ov)},
            "t_a_ids": t_a, "d_tc_images_before_w25": len(set(tc) - set(t_a)),
            "t_b": "empty (C_DIRECTION_v4_1 l.187, l.348; CC-214r3 W6; CC-245 Ruling 10)"}


def cmd_lists(root: Path, sealed: Path, pins: dict = LISTS_IN, owners: dict = OWNERS) -> None:
    rec = build_lists(root, pins, owners)
    h = write_new(root / LISTS_FILE, G.jdump(rec), 0o444)
    alog(sealed, "lists write", LISTS_FILE, h)
    print(json.dumps({k: v for k, v in rec.items() if k != "t_a_ids"} | {"sha256": h}, sort_keys=True))


# ---------------------------------------------------------------------------------------------- tenancy (§8.2)
def pause_w25(log: Path, tag: str, t0: float) -> str | None:
    """gates.pause_ok with W25 in place of its hard-coded G-B (gates.py l.989): the tag, as a whole token, is in
    exactly one LOG line, stamped by date -u before this process, naming W25 and the pause."""
    if not re.fullmatch(r"OPS-[0-9A-Za-z][0-9A-Za-z-]*", tag):
        return "--pause-tag is not an OPS-... token"
    rx = re.compile(r"(?<![\w-])" + re.escape(tag) + r"(?![\w-])")
    hits = [x for x in refuse(log).read_text(encoding="utf-8").splitlines() if rx.search(x)]
    if len(hits) != 1:
        return f"the pause tag is in {len(hits)} LOG lines, not exactly one"
    m = G.STAMP.match(hits[0])
    if not m or datetime.fromisoformat(m.group(1) + "+00:00").timestamp() >= t0:
        return "the pause line has no date -u stamp earlier than this process"
    if not W25_RX.search(hits[0]) or not re.search(r"(?i)\bpause", hits[0]):
        return "the pause line does not name W25 and the pause"
    return None


def tenancy(env: dict, tag: str, lockfd: int | None = None) -> str | None:
    """prereg §8.2 steps 1-4, before the window and again before every batch."""
    if why := pause_w25(env["log"], tag, env["t0"]):
        return why
    if G.foreign_jobs(env["proc"], os.getpid()):
        return "a foreign *_job.sh process is live"
    if not env["backup"].is_file() or b"/dev/shm" in env["backup"].read_bytes():
        return "gpu_backup.sh is missing or names /dev/shm"
    if lockfd is not None:
        try:
            a, b, s = os.fstat(lockfd), os.lstat(env["lock"]), os.lstat(env["shm"])
        except OSError:
            return "the lock file or the tmpfs dir is gone"
        if (a.st_dev, a.st_ino) != (b.st_dev, b.st_ino):
            return "the lock file was replaced"
        if not stat.S_ISDIR(s.st_mode) or s.st_mode & 0o777 != 0o700 or s.st_uid != os.getuid():
            return "the tmpfs dir is not a mode-0700 dir of this uid"
    return None


def tag_used(sealed: Path, tag: str) -> bool:
    """A 'w25 start' row already carries sha256(tag): a resume needs a new pause line (prereg §8.3). Only the
    action and path fields are read; the concrete tag itself is never written outside its LOG line."""
    p, h = sealed / "ACCESS_LOG.tsv", hashlib.sha256(tag.encode()).hexdigest()
    return p.exists() and any(x.split("\t")[2:4] == ["w25 start", h] for x in p.read_text().splitlines())


# ---------------------------------------------------------------------------------------------- inputs
def query_ids(env: dict) -> list[str]:
    """prereg §8: every ga_remaining id must be in the official OI test list, else FAULT before any request."""
    rem = G.pinned(env["root"], "ga_rem", env["pins_b"]).read_text().split()
    if len(rem) != env["n_remain"] or len(set(rem)) != len(rem):
        fault(f"ga_remaining_ids.txt is not {env['n_remain']} unique ids")
    oi = {r[0] for r in G.oi_rows(refuse(env["ga"] / G.OIL["name"]), env["strict"])}
    if bad := [i for i in rem if i not in oi]:
        fault(f"{len(bad)} ids are outside the official OI test list; no request is made")
    return sorted(rem)


def frozen(env: dict, key: str, schema: str) -> dict:
    """A once-only json whose sha is given on the command line and named in a LOG line before use."""
    p, want = env[key], env[f"{key}_sha"]
    if sha(p) != want:
        fault(f"{p.name} differs from --{key}-sha")
    if want not in refuse(env["log"]).read_text(encoding="utf-8"):
        fault(f"no LOG line names the {key} sha (it is frozen before use)")
    doc = json.loads(p.read_text())
    if doc.get("schema") != schema:
        fault(f"{p.name} has another schema")
    return doc


def owners_load(env: dict) -> tuple[dict, dict, list]:
    """Comparison owners (cached, and compute rows through the owner-feats manifest), id-join owners, deferred."""
    ow = frozen(env, "owners", SCHEMA)["owners"]
    if bad := sorted(k for k, o in ow.items() if o.get("status") not in STATUSES):
        fault(f"owners {bad} have no R6 status")
    cmp = {k: o for k, o in ow.items() if o["status"] == "cached"}
    if todo := {k: o for k, o in ow.items() if o["status"] == "compute"}:
        man = frozen(env, "feats", FEATS_SCHEMA)
        if man["owners_sha256"] != env["owners_sha"]:
            fault("the owner-feats manifest belongs to another owners file")
        for k, o in todo.items():
            m = man["owners"].get(k)
            if not m or m["n"] != o["n"] or m["source_sha256"] != o["source"][1]:
                fault(f"owner {k} is 'compute' and not in the owner-feats manifest as registered (R6)")
            cmp[k] = cached(o["n"], {m["cache"]: m["sha256"]})
    for k, o in cmp.items():
        for name, want in o["caches"].items():
            if not (env["in"] / name).is_file() or sha(env["in"] / name) != want:
                fault(f"owner {k}: staged cache {name} is missing or differs from {want[:8]}")
    return (cmp, {k: o for k, o in ow.items() if o["status"] == "id_join"},
            sorted(k for k, o in ow.items() if o["status"] == "deferred"))


def owner_feats(env: dict, o: dict) -> dict:
    """One owner's comparison side: its staged caches (w25.load at their shas), whole, or selected by id within one
    id space where every selected id has exactly one row (CC-245 B1)."""
    if o["select"] and (len({CACHE_SPACE.get(c) for c in o["caches"]}) != 1 or not set(o["caches"]) <= set(CACHE_SPACE)):
        fault(f"select over caches {sorted(o['caches'])} that are not of one known id space")
    y = W.concat([W.load(refuse(env["in"] / n), h) for n, h in sorted(o["caches"].items())])
    ids = [str(i) for i in y["ids"]]
    if o["select"]:
        sel = set(pinned_ids(disk_reader(env["root"]), o["select"]))
        idx = [i for i, x in enumerate(ids) if x in sel]
        cnt = Counter(ids[i] for i in idx)
        if set(cnt) != sel or any(v != 1 for v in cnt.values()):
            fault(f"select {o['select'][2]}: {len(sel - set(cnt))} ids without a row, "
                  f"{sum(v != 1 for v in cnt.values())} with more than one")
        if len(idx) != o["n"]:
            fault(f"select {o['select'][2]}: {len(idx)} rows, not n = {o['n']}")
        return {**BM.subset(y, idx), "ids": [ids[i] for i in idx]}
    if len(ids) != o["n"]:
        fault(f"owner caches {sorted(o['caches'])} hold {len(ids)} rows, not {o['n']}")
    return {**y, "ids": ids}


def join_hits(env: dict, q: list[str], o: dict) -> list[str]:
    """CC-245 Ruling 9: Flickr photo ids of a spent Flickr30K set -> kept OI test ids, via the pinned
    gates.landing_ids on the OI test list's URL columns (prereg §7.2 rule 4; zero pixels)."""
    photos = {Path(x).stem for x in pinned_ids(disk_reader(env["root"]), o["source"])}
    if not all(x.isdigit() for x in photos) or len(photos) != o["n"]:
        fault("the Flickr30K join list does not hold n distinct Flickr photo ids")
    by = G.landing_ids(G.oi_rows(refuse(env["ga"] / G.OIL["name"]), env["strict"]), set(q))
    return sorted(set().union(*(by[p] for p in photos & set(by))))


# ---------------------------------------------------------------------------------------------- owner-feats (Ruling 8)
FEATS_FILE, FEATS_SCHEMA = f"{PDIR}/c_pvr_owner_feats.json", "vsps.c_pvr.owner_feats.v1"


def no_sockets() -> None:
    def no_net(*a, **k):
        raise OSError("c_pvr_run: network disabled")

    socket.socket, socket.create_connection = no_net, no_net  # type: ignore[assignment,misc]


def fname(rule: str, i: str, folder: Path) -> str:
    """KTVIC files carry their own extension (.jpg, .jpeg, .png): exactly one '<11-digit id>.*' file must exist."""
    if rule == "ktvic" and KT_ID.fullmatch(i):
        hit = sorted(folder.glob(f"{int(i):011d}.*"))
        if len(hit) != 1:
            fault(f"KTVIC id {i}: {len(hit)} files, not exactly one")
        return hit[0].name
    if rule == "jpg" and NAME_RX.fullmatch(i):
        return f"{i}.jpg"
    if rule == "file" and NAME_RX.fullmatch(i):
        return i
    fault(f"id {i[:24]!r} does not fit the {rule!r} file-name rule")


def owner_feats_cmd(env: dict, run_sha: str, only: str | None = None) -> dict:
    """Laptop CPU, local files only, sockets refused: one cache per 'compute' owner (write_new 0o400, one ACCESS_LOG
    row each), then, once all exist, the once-only manifest whose sha goes in a LOG line before w25 (Ruling 8)."""
    ow = frozen(env, "owners", SCHEMA)["owners"]
    rows = {k: o for k, o in ow.items() if o.get("status") == "compute"}
    if only is not None and only not in rows:
        fault(f"{only} is not a 'compute' owner")
    if str(env["in"].resolve()).startswith("/mnt/"):
        fault("the owner caches must sit on the WSL ext4 home")
    env["in"].mkdir(mode=0o700, parents=True, exist_ok=True)
    sscd, disk = env["sscd_ok"](refuse(env["sscd"])), disk_reader(env["root"])
    for k, o in sorted(rows.items()):
        p = env["in"] / f"of_{k}.npz"
        if p.exists() or only not in (None, k):
            continue
        ids = pinned_ids(disk, o["source"])
        if len(ids) != o["n"] or len(set(ids)) != o["n"]:
            fault(f"{k}: the source list does not hold n = {o['n']} distinct ids")
        paths = [env["root"] / o["dir"] / fname(o["name"], i, env["root"] / o["dir"]) for i in ids]
        if miss := [x for x in paths if not x.is_file()]:
            fault(f"{k}: {len(miss)} image files are missing")
        f = env["features"]([refuse(x) for x in paths], sscd, workers=env["workers"], retry_truncated=False)
        if f["unreadable"]:
            fault(f"{k}: {len(f['unreadable'])} images cannot be featured")
        buf = io.BytesIO()
        np.savez(buf, ids=np.array(ids, dtype=str), sha=np.array(f["sha"]), **{x: f[x] for x in W.KEYS},
                 unreadable=np.zeros(0, np.int64), meta=np.array(json.dumps({"owner": k, "source": o["source"][1],
                                                                              "run_sha256": run_sha})))
        alog(env["sealed"], "owner-feats write", p.name, write_new(p, buf.getvalue(), 0o400, check_mode=True))
    done = {k: env["in"] / f"of_{k}.npz" for k in rows}
    if all(p.exists() for p in done.values()) and not os.path.lexists(env["feats"]):
        rec = {"schema": FEATS_SCHEMA, "label": CP.LABEL, "owners_sha256": env["owners_sha"], "run_sha256": run_sha,
               "sscd_sha256": sha(env["sscd"]), "owners": {k: {"cache": p.name, "sha256": sha(p), "n": rows[k]["n"],
                                                               "source_sha256": rows[k]["source"][1]}
                                                           for k, p in sorted(done.items())}}
        h = write_new(env["feats"], G.jdump(rec), 0o444)
        alog(env["sealed"], "owner-feats manifest", env["feats"].name, h)
        return rec
    return {"written": sorted(k for k, p in done.items() if p.exists()), "manifest": False}


# ---------------------------------------------------------------------------------------------- fetch and features
def classify(b, err: str) -> str:
    """prereg §8.1 table over cen_fetch.get's return value (after its three tries)."""
    if b is not None and err == "":
        return "fetched"
    if b is None and FAULT_ERR.fullmatch(err):
        return "fault"
    if b is None and LOST_ERR.fullmatch(err):
        return "lost"
    return "fault"


def put(folder: Path, name: str, b: bytes, xm: set) -> Path:
    """One body into tmpfs; a body whose sha256 is an XM3600 image is never written (w25.fetch_batch rule)."""
    if G.sha_bytes(b) in xm:
        fault(f"{name} is an XM3600 image by sha256; not written (NB-SHAREFUSE)")
    p = folder / name
    with open(os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "wb") as f:
        f.write(b)
    return p


def stage_nocaps(env: dict, st: dict, ids: list[str], folder: Path) -> tuple[list, dict]:
    folder.mkdir(mode=0o700)
    pairs, lost = [], {}
    ex = ThreadPoolExecutor(env["fetchers"])
    try:
        for i, (b, err) in zip(ids, ex.map(lambda x: env["get"](CP.OI_TEST_URL.format(file=f"{x}.jpg")), ids)):
            cls = classify(b, err)
            if cls == "fault":
                fault(f"OI test {i}: get returned {err!r} (prereg §8.1: FAULT, no substitute source)")
            if cls == "lost":
                lost[i] = f"fetch {err}"
                continue
            pairs.append((i, put(folder, f"{i}.jpg", b, st["xm"])))
    finally:
        ex.shutdown(wait=True, cancel_futures=True)
    return pairs, lost


def stage_ovqa(env: dict, st: dict, names: list[str], folder: Path) -> tuple[list, dict]:
    folder.mkdir(mode=0o700)
    with zipfile.ZipFile(st["zip"]) as z:
        pairs = [(n, put(folder, n, z.read(st["members"][n]), st["xm"])) for n in names]
    return pairs, {}


def featurize(env: dict, st: dict, pairs: list) -> tuple[dict, list, dict, list]:
    """build_memory.features with retry_truncated=False (R1d): an undecodable or truncated body is lost, never
    retried. The decode error class is read from match_openviic._features while the bytes are still in tmpfs."""
    f = env["features"]([p for _, p in pairs], st["sscd"], workers=env["workers"], retry_truncated=False)
    bad = set(f["unreadable"])
    lost, trunc = {}, []
    for i in sorted(bad):
        msg = BM.MO._features(str(pairs[i][1]))[1]
        msg = msg if isinstance(msg, str) else "unknown"
        lost[pairs[i][0]] = "decode " + msg.split(":")[0]
        trunc += [pairs[i][0]] if "truncated" in msg else []
    keep = [i for i in range(len(pairs)) if i not in bad]
    return f, keep, lost, trunc


def drop(env: dict, folder: Path, what: str) -> None:
    """Unlink a tmpfs folder and log the deletion (utc, folder, file count) in w25_deletions.log (prereg §8)."""
    n = sum(len(fs) for _, _, fs in os.walk(folder))
    shutil.rmtree(folder, ignore_errors=True)
    if os.path.lexists(folder):
        fault(f"{folder} could not be deleted")
    with open(env["dlog"], "a") as fh:
        fh.write(f"{CP.utc()}\tdeleted\t{folder}\t{n} files\t{what}\n")
        fh.flush()
        os.fsync(fh.fileno())


def ids_sha(ids: list[str]) -> str:
    return G.sha_bytes("\n".join(ids).encode("utf-8"))


def write_part(env: dict, part: Path, pairs: list, f: dict, keep: list, meta: dict) -> None:
    buf = io.BytesIO()
    np.savez(buf, ids=np.array([pairs[i][0] for i in keep], dtype=str), sha=np.array([f["sha"][i] for i in keep]),
             **{k: f[k][keep] for k in W.KEYS}, unreadable=np.zeros(0, np.int64), meta=np.array(json.dumps(meta)))
    write_new(part, buf.getvalue(), 0o400, check_mode=True)


def read_part(part: Path, kind: str, ids: list[str], run_sha: str) -> tuple[dict, dict]:
    z = np.load(refuse(part))
    meta = json.loads(str(z["meta"]))
    if meta["set"] != kind or meta["batch_sha256"] != ids_sha(ids) or meta["run_sha256"] != run_sha:
        fault(f"{part.name} does not belong to this batch, set or c_pvr_run.py sha; no resume")
    return W.load(part), meta


def batches(items: list[str], n: int) -> list[list[str]]:
    return [items[i:i + n] for i in range(0, len(items), n)]


def guard(env: dict, st: dict) -> None:
    if env["clock"]() >= st["deadline"]:
        raise Stop("STOP: the 24 h wall-clock stop is reached (prereg §8.3); features are kept; Q-custody -> PI")
    if why := tenancy(env, st["tag"], st["lockfd"]):
        fault(f"tenancy: {why}; window aborted")


def project(env: dict, st: dict, t: float, n: int) -> None:
    """prereg §8.3: after the first batch of this process, project the end of the rest and stop if it passes the
    deadline that was fixed at first start."""
    if st["projected"]:
        return
    st["projected"] = True
    el = env["clock"]() - t
    end = t + el * st["todo"] / n
    alog(env["sealed"], "w25 projection", f"{el:.1f}s/{n}", f"{end - st['deadline'] + WALL:.0f}")
    print(f"projection: first batch {n} images in {el:.1f} s; projected end at {end - st['deadline'] + WALL:.0f} s"
          f" of the {WALL} s window", flush=True)
    if end > st["deadline"]:
        raise Stop("STOP: the first-batch projection exceeds the 24 h stop (prereg §8.3); Q-custody -> PI")


def run_set(env: dict, st: dict, kind: str, items: list[str], stage) -> dict:
    """One part per batch (a rerun verifies and skips finished parts). Each batch is in tmpfs only from its bytes to
    its features, then unlinked and logged; the lost cap is checked after every batch (prereg §8.1)."""
    lost = {}
    for n, ids in enumerate(batches(items, env["batch"])):
        part = env["work"] / "parts" / f"{kind}_{n:04d}.npz"
        if part.exists():
            lost.update(read_part(part, kind, ids, st["run"])[1]["lost"])
            continue
        guard(env, st)
        t, folder = env["clock"](), st["shm"] / f"{kind}_b{n:04d}"
        try:
            pairs, gone = stage(env, st, ids, folder)
            f, keep, dec, trunc = featurize(env, st, pairs)
        finally:
            drop(env, folder, f"after {kind}_{n:04d}")
        lost |= gone | dec
        write_part(env, part, pairs, f, keep, {"set": kind, "n": len(ids), "batch_sha256": ids_sha(ids),
                                               "lost": gone | dec, "truncated": trunc, "run_sha256": st["run"],
                                               "utc": CP.utc()})
        print(f"{kind} part {n:04d}: {len(keep)} featured, {len(gone | dec)} lost", flush=True)
        if len(lost) > LOST_CAP[kind]:
            fault(f"{kind}: {len(lost)} images lost (> {LOST_CAP[kind]}, prereg §8.1); w25 stops -> PI")
        project(env, st, t, len(ids))
    return lost


def ovqa_names(env: dict) -> list[str]:
    """The dev image names (the one string field allowed, CC-237 (vi)), taken as c_pvr.ovqa_count l.902-904 does."""
    rule_p = refuse(env["root"] / env["rule"][0])
    if sha(rule_p) != env["rule"][1]:
        fault("the OpenViVQA counting rule differs from its LOG-line sha (ovqa_names)")
    r = json.loads(rule_p.read_text())[CP.OVQA_DEV]
    ims, fld = CP.ovqa_load(env["ovqa"], env["sealed"], CP.OVQA_DEV)[r["images"]], r["image_names"]
    names = [Path(x).name for x in (list(ims.values()) if fld == "values" else [x[fld.split(":", 1)[1]] for x in ims])]
    if len(set(names)) != CP.OVQA_COUNTS[CP.OVQA_DEV][0] or not all(NAME_RX.fullmatch(x) for x in names):
        fault("OpenViVQA dev names are not the pinned number of distinct plain file names")
    return sorted(names)


def ovqa_zip(env: dict, st: dict) -> dict:
    """R1e: dev-images.zip into tmpfs only, (size, sha256) = OVQA_DEV_ZIP before its central directory is read,
    then the pinned c_pvr.ovqa_count identity check (c). The zip is unlinked with the ovqa tmpfs folder."""
    d = st["shm"] / "ovqa"
    d.mkdir(mode=0o700)
    part, z = d / f"{OVQA_ZIP}.part", d / OVQA_ZIP
    rc = env["runner"](CP.curl_argv(OVQA_ZIP, part))
    n, s256, _ = CP.blob_hashes(part) if part.exists() else (-1, "", "")
    if rc or (n, s256) != CP.OVQA_DEV_ZIP:
        fault(f"{OVQA_ZIP}: rc {rc}, size {n}, sha256 {s256[:8]} differ from the LFS pin")
    os.replace(part, z)
    got = CP.ovqa_count(env["ovqa"], env["sealed"], refuse(env["root"] / env["rule"][0]), env["rule"][1], z)
    with zipfile.ZipFile(z) as zf:
        members = {}
        for m in (m for m in zf.namelist() if not m.endswith("/")):
            if Path(m).name in members:
                fault(f"{OVQA_ZIP} has two members named {Path(m).name}")
            members[Path(m).name] = m
    st.update(zip=z, members=members)
    return got


def deadline(env: dict) -> float:
    p = env["work"] / "deadline"
    if not p.exists():
        write_new(p, f"{env['clock']() + WALL:.0f}\n".encode(), 0o400, check_mode=True)
    return float(p.read_text())


# ---------------------------------------------------------------------------------------------- decide (one look)
def collect(env: dict, kind: str, items: list[str], run_sha: str) -> tuple[dict, dict, list]:
    fs, lost, trunc = [], {}, []
    for n, ids in enumerate(batches(items, env["batch"])):
        p = env["work"] / "parts" / f"{kind}_{n:04d}.npz"
        if not p.exists():
            fault(f"{p.name} is missing; decide needs every part")
        f, meta = read_part(p, kind, ids, run_sha)
        fs.append(f)
        lost.update(meta["lost"])
        trunc += meta["truncated"]
    return W.concat(fs), lost, trunc


def flag(q: dict, owners: dict) -> tuple[set, dict]:
    hit, per = set(), {}
    for k, y in owners.items():
        r = W.rule(q, y, BM.near)
        per[k] = {c: int(v.sum()) for c, v in r.items()}
        hit |= {q["ids"][i] for i in r["excluded"].nonzero()[0]}
    return hit, per


def decide(env: dict, pre: dict, sets: dict, run_sha: str, ident: dict) -> dict:
    ys, joins = pre["ys"], pre["joins"]
    rec = {"label": CP.LABEL, "utc": CP.utc(), "rule": RULE_TEXT, "run_sha256": run_sha, "code_sha256": CODE,
           "owners_sha256": env["owners_sha"], "ga_remaining_sha256": env["pins_b"]["ga_rem"][1],
           "sscd_sha256": W.SSCD_SHA, "lost_cap": LOST_CAP, "owners_compared": sorted(ys), "ovqa_identity_c": ident,
           "owners_deferred": pre["deferred"], "feats_sha256": env.get("feats_sha")}
    out = {}
    for kind, items in sets.items():
        q, lost, trunc = collect(env, kind, items, run_sha)
        hit, per = flag(q, ys)
        gone = hit | set(lost)
        rec[kind] = {"queried": len(items), "featured": len(q["ids"]), "lost": len(lost),
                     "lost_by_class": dict(Counter(lost.values())), "truncated": len(trunc), "flagged": len(hit),
                     "flagged_by_owner": per, "flagged_or_lost": len(gone),
                     "flickr_w3_in_flagged_or_lost": len(gone & set(G.FLICKR_W3))}
        out[kind] = (hit, lost, gone)
    rec["n_e_power_inputs"] = {"w25_flagged": rec["nocaps_test"]["flagged"], "lost": rec["nocaps_test"]["lost"]}
    hits = set().union(*joins.values())
    rec["id_join_beside_n_e_power"] = {  # CC-245 Ruling 9: leaves local metrics, never enters n_e_power here
        "by_owner": {k: len(v) for k, v in joins.items()}, "hits": len(hits),
        "hits_also_flagged_or_lost": len(hits & out["nocaps_test"][2])}
    files = dict(zip(OUTS, (out["nocaps_test"][0], out["nocaps_test"][1], out["ovqa_dev"][2], hits)))
    for name, ids in files.items():
        write_new(env["out"] / name, G.ids_bytes(ids), 0o444)
    h = write_new(env["out"] / OUTS[-1], G.jdump(rec), 0o444)
    alog(env["sealed"], "w25 decide", OUTS[-1], h)
    return rec


# ---------------------------------------------------------------------------------------------- w25 (§8)
def sig_handler(me: int):
    def on_sig(signum, frame):
        if os.getpid() != me:  # a build_memory Pool worker forked inside the window: plain exit, no trap
            os._exit(128 + signum)
        raise SystemExit(f"ABORT: signal {signum}")

    return on_sig


def decided(sealed: Path) -> bool:
    """N2: an ACCESS_LOG 'w25 decide' row (the outputs sit on /mnt/d, where 0o444 is not enforced)."""
    p = sealed / "ACCESS_LOG.tsv"
    return p.exists() and any(x.split("\t")[2:3] == ["w25 decide"] for x in p.read_text().splitlines())


def w25_pre(env: dict) -> dict:
    """Everything that can FAULT before the window: outputs absent, owners closed, staged and loaded (N2), ids,
    the Flickr30K id join, SSCD, XM shas."""
    if any(os.path.lexists(env["out"] / x) for x in OUTS) or decided(env["sealed"]):
        fault("a W25 output or 'w25 decide' row exists; decide is one look")
    if str(env["in"].resolve()).startswith("/mnt/") or str(env["work"].resolve()).startswith("/mnt/"):
        fault("the staged inputs and the feature parts must sit on the WSL ext4 home")
    cmp, joins, dfr = owners_load(env)
    ys = {k: owner_feats(env, o) for k, o in sorted(cmp.items())}
    q = query_ids(env)  # every id checked against the OI test list before the first request (prereg §8)
    return {"ys": ys, "joins": {k: set(join_hits(env, q, o)) for k, o in joins.items()}, "deferred": dfr, "q": q,
            "sscd": env["sscd_ok"](refuse(env["sscd"])), "xm": env["xm"]()}


def w25(env: dict, tag: str, run_sha: str) -> dict:
    pre = w25_pre(env)
    q, sscd, xm = pre["q"], pre["sscd"], pre["xm"]
    if why := tenancy(env, tag):
        fault(f"tenancy: {why}; w25 does not start")
    if tag_used(env["sealed"], tag):
        fault("this pause tag already opened a window; a resume needs a new pause line (prereg §8.3)")
    lockfd = os.open(env["lock"], os.O_RDWR | os.O_CREAT, 0o600)
    try:
        fcntl.flock(lockfd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if os.path.lexists(env["shm"]):
            fault(f"{env['shm']} exists (residue of an earlier window); it is left for a human")
        env["shm"].mkdir(mode=0o700)
        os.chmod(env["shm"], 0o700)
    except OSError:
        os.close(lockfd)
        fault("tenancy: the W25 lock is held; w25 does not start")
    except BaseException:
        os.close(lockfd)
        raise
    old, on_sig = {s: signal.getsignal(s) for s in G.GB_SIGS}, sig_handler(os.getpid())
    st = {"tag": tag, "lockfd": lockfd, "run": run_sha, "shm": env["shm"], "xm": xm,
          "sscd": sscd, "projected": False}
    done, why = "w25 abort", "-"
    try:
        for s in G.GB_SIGS:
            signal.signal(s, on_sig)
        (env["work"] / "parts").mkdir(mode=0o700, parents=True, exist_ok=True)
        st["deadline"] = deadline(env)
        alog(env["sealed"], "w25 start", hashlib.sha256(tag.encode()).hexdigest(), run_sha)
        names = ovqa_names(env)
        sets = {"nocaps_test": q, "ovqa_dev": names}
        st["todo"] = sum(len(b) for k, v in sets.items() for n, b in enumerate(batches(v, env["batch"]))
                         if not (env["work"] / "parts" / f"{k}_{n:04d}.npz").exists())
        run_set(env, st, "nocaps_test", q, stage_nocaps)
        ident_p = env["work"] / "ovqa_identity_c.json"
        if not all((env["work"] / "parts" / f"ovqa_dev_{n:04d}.npz").exists()
                   for n in range(len(batches(names, env["batch"])))):
            ident = ovqa_zip(env, st)
            if not ident_p.exists():
                write_new(ident_p, G.jdump(ident), 0o400, check_mode=True)
            run_set(env, st, "ovqa_dev", names, stage_ovqa)
            drop(env, st["shm"] / "ovqa", "after ovqa_dev (dev-images.zip and batches)")
        if not ident_p.exists():
            fault("the OpenViVQA identity record (c) is missing")
        rec = decide(env, pre, sets, run_sha, json.loads(ident_p.read_text()))
        done = "w25 end"
        return rec
    except BaseException as e:
        why = str(e).split(":")[0][:16] if isinstance(e, SystemExit) else type(e).__name__
        raise
    finally:
        for s in G.GB_SIGS:
            signal.signal(s, signal.SIG_IGN)
        try:
            drop(env, env["shm"], "trap: window exit")
        finally:
            alog(env["sealed"], done, why, run_sha)
            for s in G.GB_SIGS:
                signal.signal(s, old[s])
            os.close(lockfd)


def curl(argv) -> int:
    return subprocess.run(argv, stdin=subprocess.DEVNULL, env=G.CURL_ENV).returncode


def real_env(root: Path, x) -> dict:
    sealed = CP.SEALED
    return {"root": root, "ga": G.GA, "sealed": sealed, "work": sealed / "w25", "dlog": sealed / "w25_deletions.log",
            "ovqa": sealed / "ovqa", "out": root / PDIR, "owners": root / OWNERS_FILE, "shm": SHM, "lock": LOCK,
            "log": root / G.GB_LOG, "backup": Path.home() / ".config/vsps/gpu_backup.sh", "proc": Path("/proc"),
            "t0": T0, "clock": time.time, "strict": True, "pins_b": G.PINS_B, "n_remain": G.GB_REMAINING,
            "batch": W.BATCH, "in": Path(x.inp), "sscd": Path(x.sscd), "sscd_ok": W.ok_sscd, "xm": W.xm_shas,
            "get": W.F.get, "runner": curl, "features": BM.features, "workers": 4, "fetchers": 16,
            "rule": OVQA_RULE, "owners_sha": x.owners_sha, "feats": root / FEATS_FILE,
            "feats_sha": getattr(x, "feats_sha", None)}


# ---------------------------------------------------------------------------------------------- selftest
def _must(msg: str, fn, *a, **k):
    try:
        fn(*a, **k)
    except SystemExit as e:
        assert msg in str(e), (msg, str(e))
        return e
    raise AssertionError(f"expected {msg!r}")


def _st_static(root: Path) -> None:
    import ast

    assert "spacy" not in sys.modules and "rapidfuzz" not in sys.modules  # R1a: constants import without them
    src = Path(__file__).read_text("utf-8")
    shared = {"OI_TEST_URL", "LABEL", "SEALED", "BARRED", "CAP", "OVQA_URL", "OVQA_REV", "OVQA_DEV_ZIP", "OVQA_JSON",
              "OVQA_COUNTS", "OVQA_DEV", "STAMP", "FLICKR_W3", "GB_SIGS", "PINS_B", "BATCH", "KEYS"}
    tree = ast.parse(src)
    tops = {t.id for n in tree.body if isinstance(n, (ast.Assign, ast.AnnAssign))
            for t in (n.targets if isinstance(n, ast.Assign) else [n.target]) if isinstance(t, ast.Name)}
    assert not tops & shared, tops & shared  # Q-SPLIT (i): no second value of a shared constant
    rest = "".join(ast.get_source_segment(src, n) for n in tree.body if getattr(n, "name", "") != "_st_static")
    assert "open-images-dataset" not in rest and "huggingface.co" not in rest  # no second URL value either
    assert CP.OI_TEST_URL == G.OI_TEST_URL == "https://open-images-dataset.s3.amazonaws.com/test/{file}"  # v1.3 l.133
    for p in ("x/oidv7-test-annotations-human-imagelabels.csv", "/dev/shm/c_pvr_gb/a", "a/gb_intermediate.json",
              "a/nocaps_val_4500_captions.json", "a/nocaps_test_image_info.json", "a/labels.csv", "a/captions_x.json"):
        _must("REFUSED", refuse, p)
    assert code_bad(root) == []
    assert LOST_CAP == {"nocaps_test": 10, "ovqa_dev": 1} and WALL == 86400
    ns = argparse.Namespace(inp="/i", sscd="/s.pt", owners_sha="o", feats_sha="f")
    e = real_env(root, ns)
    want = {"ga": G.GA, "sealed": CP.SEALED, "work": CP.SEALED / "w25", "dlog": CP.SEALED / "w25_deletions.log",
            "ovqa": CP.SEALED / "ovqa", "out": root / PDIR, "owners": root / OWNERS_FILE,
            "shm": Path("/dev/shm/c_pvr_w25"), "lock": Path("/dev/shm/c_pvr_w25.lock"),
            "log": root / ".session_backup/2026-10-13/decisions/LOG.md", "proc": Path("/proc"), "strict": True,
            "backup": Path.home() / ".config/vsps/gpu_backup.sh", "n_remain": 10496, "batch": 512,
            "rule": OVQA_RULE, "in": Path("/i"), "sscd": Path("/s.pt"), "owners_sha": "o", "t0": T0,
            "feats": root / "manuscript/prereg/2026-11-02_c_pvr_tier1/c_pvr_owner_feats.json", "feats_sha": "f"}
    assert all(e[k] == v for k, v in want.items()), [k for k, v in want.items() if e[k] != v]
    assert e["pins_b"] is G.PINS_B and e["get"] is W.F.get and e["features"] is BM.features
    assert e["xm"] is W.xm_shas and e["sscd_ok"] is W.ok_sscd and e["runner"] is curl and e["clock"] is time.time


def _st_classify() -> None:
    for b, err, want in ((b"\xff\xd8x", "", "fetched"), (None, "status 403", "fault"), (None, "redirected", "fault"),
                         (None, "not a JPEG body", "fault"), (None, "HTTPError", "lost"), (None, "TimeoutError", "lost"),
                         (None, "", "fault"), (None, "status 4x", "fault"), (b"x", "HTTPError", "fault"),
                         (None, "URLError: x", "fault")):
        assert classify(b, err) == want, (b, err, classify(b, err))
    import urllib.error

    F, keep = W.F, W.F.OPEN

    class R:
        def __init__(self, body, url, status):
            self.body, self.url, self.status = body, url, status

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return self.body

        def geturl(self):
            return self.url

    def opener(kind):
        def o(url, timeout):
            if kind == "404":
                raise urllib.error.HTTPError(url, 404, "nf", {}, None)
            return {"ok": R(b"\xff\xd8\xff", url, 200), "403": R(b"x", url, 403), "redir": R(b"\xff\xd8", url + "?", 200),
                    "html": R(b"<html>", url, 200)}[kind]
        return o

    try:  # the real cen_fetch.get with its opener replaced: classify reads get's actual strings
        for kind, want in (("ok", "fetched"), ("404", "lost"), ("403", "fault"), ("redir", "fault"), ("html", "fault")):
            F.OPEN = opener(kind)
            assert classify(*F.get("https://h/x.jpg")) == want, kind
    finally:
        F.OPEN = keep


def _st_tenancy(base: Path) -> None:
    log, proc, backup = base / "LOG.md", base / "proc", base / "gpu_backup.sh"
    proc.mkdir()
    backup.write_text("rsync m1:/root ~/x\n")
    lines = ["2026-01-01T00:00:00Z OPS-1-w25pause: W25 window pause of every other laptop job",
             "2026-01-01T00:00:00Z OPS-2: W25 window, no word", "2026-01-01T00:00:00Z OPS-3 pause of G-B only",
             "2099-01-01T00:00:00Z OPS-4 W25 pause", "OPS-5 W25 pause (no stamp)", "2026-01-01T00:00Z OPS-6 W25 pause",
             "2026-01-01T00:00:00Z OPS-7 W25 pause", "2026-01-01T00:00:00Z again OPS-7",
             "2026-01-01T00:00:00Z OPS-8 W25-K1 pause"]
    log.write_text("\n".join(lines) + "\n", "utf-8")
    t0 = time.time()
    assert pause_w25(log, "OPS-1-w25pause", t0) is None and pause_w25(log, "OPS-6", t0) is None
    for tag, why in (("OPS-1", "in 0 LOG"), ("OPS-2", "does not name W25"), ("OPS-3", "does not name W25"),
                     ("OPS-4", "earlier than"), ("OPS-5", "earlier than"), ("OPS-7", "in 2 LOG"), ("x", "not an OPS"),
                     ("OPS-8", "does not name W25"), ("OPS-", "not an OPS")):
        assert why in (pause_w25(log, tag, t0) or ""), (tag, pause_w25(log, tag, t0))
    shm, lock = base / "shm", base / "lock"
    env = {"log": log, "proc": proc, "backup": backup, "t0": t0, "shm": shm, "lock": lock}
    assert tenancy(env, "OPS-1-w25pause") is None and "pause tag" in tenancy(env, "OPS-1")
    (proc / "77").mkdir()
    (proc / "77/cmdline").write_bytes(b"bash\0/x/b_job.sh\0")
    assert "foreign" in tenancy(env, "OPS-1-w25pause")
    (proc / "77/cmdline").write_bytes(b"bash\0/x/b_job.sh.txt\0")
    backup.write_text("x /dev/shm/y\n")
    assert "gpu_backup" in tenancy(env, "OPS-1-w25pause")
    backup.unlink()
    assert "gpu_backup" in tenancy(env, "OPS-1-w25pause")
    backup.write_text("ok\n")
    fd = os.open(lock, os.O_RDWR | os.O_CREAT, 0o600)
    assert "gone" in tenancy(env, "OPS-1-w25pause", fd)
    shm.mkdir(mode=0o700)
    os.chmod(shm, 0o700)
    assert tenancy(env, "OPS-1-w25pause", fd) is None
    os.chmod(shm, 0o755)
    assert "mode-0700" in tenancy(env, "OPS-1-w25pause", fd)
    os.chmod(shm, 0o700)
    lock.unlink()
    lock.write_text("")
    assert "replaced" in tenancy(env, "OPS-1-w25pause", fd)
    os.close(fd)
    (base / "ACCESS_LOG.tsv").write_text(f"t\tc_pvr_run.py\tw25 start\t{hashlib.sha256(b'OPS-9').hexdigest()}\tr\n")
    assert tag_used(base, "OPS-9") and not tag_used(base, "OPS-1-w25pause")


def _st_owners() -> None:
    port = ("# P\n\n### 2.3 Test-set ledger\n\n| Set | Gold |\n|---|---|\n| Alpha | x |\n| Beta (1) | y |\n\n"
            "**Dev-only (spent):** Gamma all, Delta.\n\n### 2.4 Next\n| Omega | z |\n").encode()
    rules = json.dumps({"owners": {"bo1": {}, "bo2": {}}}).encode()
    files = {PORTFOLIO: port, "manuscript/prereg/a/one.txt": b"x\n", "manuscript/prereg/b/two.tsv": b"#h\n1\n",
             "manuscript/prereg/b/x.json": b"{}", "s/sel.txt": b"1\n2\n", "s/c.txt": b"7\n8\n9\n",
             "s/j.json": json.dumps({"carve": ["1.jpg", "2.jpg"]}).encode(), "b/rules.json": rules}
    ls = ["manuscript/prereg/a/one.txt", "manuscript/prereg/b/two.tsv", "manuscript/prereg/b/x.json",
          "manuscript/prereg/a/SHA256SUMS", "manuscript/prereg/a/p.md", ""]
    sh = {k: G.sha_bytes(v) for k, v in files.items()}
    good = {"own_a": cached(2, {"feats_memory.npz": "0" * 64}, ("s/sel.txt", sh["s/sel.txt"], None)),
            "own_b": deferred("held nowhere"), "own_c": compute(3, ("s/c.txt", sh["s/c.txt"], None), "d", "jpg"),
            "own_j": {"status": "id_join", "n": 2, "source": ["s/j.json", sh["s/j.json"], "carve"]}}
    reg = (good, {"Alpha": "own_a", "Beta (1)": SELF},
           {"manuscript/prereg/a/one.txt": "own_b", "manuscript/prereg/b/two.tsv": "skip: terms",
            "manuscript/prereg/b/x.json": ["own_j", SELF]}, {"Gamma all": ["own_c"]}, {"own_a": "extra"},
           {"bo1": "own_a", "bo2": SELF}, ("b/rules.json", sh["b/rules.json"]))
    read = files.__getitem__
    doc = json.loads(build_owners(read, lambda: ls, "h0", reg))
    assert doc["schema"] == SCHEMA and doc["head"] == "h0" and set(doc["owners"]) == set(good)
    assert doc["lists"]["manuscript/prereg/b/x.json"] == {"to": ["own_j", SELF], "sha256": G.sha_bytes(b"{}")}
    assert doc["lists"]["manuscript/prereg/b/two.tsv"] == {"to": "skip: terms"}  # a skipped list is not hashed
    assert doc["portfolio"]["blob_sha256"] == G.sha_bytes(port) and doc["b_r5_map"] == reg[5]
    assert doc["b_r5_overlay"] == {"path": "b/rules.json", "sha256": sh["b/rules.json"]}
    assert doc["b_owners_file"] == {"path": B_OWN[0], "sha256": B_OWN[1]}

    def bad(msg, **ch):
        r = list(reg)
        for i, v in ch.items():
            r[int(i[1:])] = v
        _must(msg, build_owners, read, lambda: ls, "h0", tuple(r))

    bad("unmapped ['Beta (1)']", r1={"Alpha": "own_a"})
    bad("gone ['Zeta']", r1={**reg[1], "Zeta": "own_a"})
    bad("unmapped ['manuscript/prereg/b/x.json']", r2={k: v for k, v in reg[2].items() if not k.endswith("json")})
    bad("gone ['manuscript/prereg/c.txt']", r2={**reg[2], "manuscript/prereg/c.txt": "own_b"})
    bad("no longer names ['Omega']", r3={**reg[3], "Omega": ["own_c"]})
    bad("dangling ['own_x']", r4={"own_x": "e", "own_a": "e"})
    bad("dangling ['own_y']", r2={**reg[2], "manuscript/prereg/b/x.json": ["own_j", "own_y"]})
    bad("dangling ['own_w']", r5={"bo1": "own_w", "bo2": SELF})
    bad("orphans ['own_z']", r0={**good, "own_z": deferred("r")})
    bad("B R5 owners differ", r5={"bo1": "own_a"})
    bad("B R5 owners differ", r6=("b/rules.json", "0" * 64))
    bad("status 'out_of_scope'", r0={**good, "own_b": {"status": "out_of_scope", "reason": "r"}})
    bad("deferred without a reason", r0={**good, "own_b": deferred("")})
    bad("does not hold n = 2", r0={**good, "own_c": compute(2, ("s/c.txt", sh["s/c.txt"], None), "d", "jpg")})
    bad("does not hold n = 3", r0={**good, "own_j": {**good["own_j"], "n": 3}})
    bad("differs from its pin", r0={**good, "own_c": compute(3, ("s/c.txt", "0" * 64, None), "d", "jpg")})
    bad("full sha256", r0={**good, "own_a": cached(2, {"feats_memory.npz": "0" * 63})})
    bad("full sha256", r0={**good, "own_a": cached(0, {"feats_memory.npz": "0" * 64})})
    bad("full sha256", r0={**good, "own_a": cached(2, {})})
    bad("one known id space", r0={**good, "own_a": cached(2, {"feats_memory.npz": "0" * 64,
                                                               "feats_nocaps_val.npz": "0" * 64})})
    bad("one known id space", r0={**good, "own_a": cached(2, {"own.npz": "0" * 64})})
    bad("select list does not hold", r0={**good, "own_a": cached(3, {"feats_memory.npz": "0" * 64},
                                                                 ("s/sel.txt", sh["s/sel.txt"], None))})
    _must("no §2.3", build_owners, {**files, PORTFOLIO: b"# P\n"}.__getitem__, lambda: ls, "h0", reg)
    assert ledger(port.decode())[1] == ["Alpha", "Beta (1)"]
    assert ids_of(b'{"a": {"b": [["x", 1], "y"], "c": {"k1": 0}}}', "a/b+a/c") == ["x", "y", "k1"]
    assert ids_of(b"#h\n1\tq\n\n2\n", None) == ["1", "2"]
    refs = {*LEDGER.values(), *(x for v in LISTS.values() for x in mapped(v)), *(k for v in SPENT.values() for k in v),
            *EXTRA, *B_MAP.values()}
    assert set(OWNERS) <= refs and all(v in OWNERS or OWN_RX.match(v) for v in refs)
    assert len(B_MAP) == 44 and B_MAP["h500"] == "h_bdt1_739" and B_MAP["flickr30k_test_c"] == "flickr30k_c_t3_carve"
    assert len(_records(_RECORDS)) == 91 and all(k.endswith(".json") and "/ " not in k for k in _records(_RECORDS))
    assert len(LISTS) == 155 and all(LIST_RX.search(k) for k in LISTS)
    assert all(o["status"] in STATUSES for o in OWNERS.values())


def _st_lists(base: Path) -> None:
    root = base / "lroot"
    ovf = lambda i: f"{i:011d}.jpg"  # noqa: E731
    e5 = lambda f, sp="train": [f, sp, 0, 0, 0.0]  # noqa: E731  the real 5-field copy-map entry, synthetic values
    test_pairs = {str(i): [] for i in range(1001, 1559)}
    test_pairs["1001"] = [e5(ovf(5105)), e5("00000005107.png")]  # KTVIC-test copies in OpenViIC train (B3b)
    files = {"kt.json": {"images": [{"id": i, "filename": "x"} for i in range(1001, 1559)], "annotations": []},
             "ov.json": {ovf(i): {"captions": ["c"]} for i in range(2001)},
             "vt.json": {"images": [{"id": i} for i in range(5)] + [{"id": 4}]},
             "kr.json": {"images": [{"id": i} for i in range(1, 13)],
                         "annotations": [{"image_id": 1 + i % 12} for i in range(36)]},
             "or.json": {**{ovf(i): {"captions": ["c", "d"]} for i in range(5100, 5107)},
                         "00000005107.png": {"captions": ["c", "d"]}},
             "map.json": {"_pairs": {"train": {"1": [e5(ovf(5100))], "5": [e5(ovf(5101))], "6": [e5(ovf(3), "test")],
                                               "7": [e5(ovf(3001), "dev")], "8": [e5(ovf(5102))],
                                               "9": [e5(ovf(5100)), e5(ovf(5104), "uncaptioned")],
                                               "10": [e5(ovf(5103))], "11": [e5("00000005107.png")]},
                                     "test": test_pairs}},
             "h.json": {"H": {"ids": ["1", "2"]}, "T2": {"ids": ["3"]}},
             "ex.json": {"ids": {"ktvic": {"d": ["4"]}}},
             "c1.json": {"sets": {"a": [[ovf(3001), ovf(3001), "s"]], "b": [[ovf(3002), ovf(3002), "s"]]}}}
    root.mkdir()
    pins = {}
    for name, d in files.items():
        (root / name).write_text(json.dumps(d))
        pins[name] = (name, G.sha_bytes((root / name).read_bytes()))
    tc = [f"t{i}" for i in range(1075)]
    for name, body in (("dev.tsv", "5\t00000000005.jpg\n"), ("tc.txt", "\n".join(tc) + "\n")):
        (root / name).write_text(body)
        pins[name] = (name, G.sha_bytes(body.encode()))
    owners = {"h_bdt1_739": {"source": [*pins["h.json"], "H/ids+T2/ids"]},
              "ktvic_dev299": {"source": [*pins["dev.tsv"], None]},
              "refused_ktvic_dup": {"source": [*pins["ex.json"], "ids/ktvic/d"]},
              "openviic_dev_c1": {"source": [*pins["c1.json"], "sets/a+sets/b"]}}
    p = {"ktvic_test": pins["kt.json"], "openviic_test": pins["ov.json"], "vitextvqa_dev": pins["vt.json"],
         "ktvic_train": pins["kr.json"], "openviic_train": pins["or.json"], "copy_map": pins["map.json"],
         "textcaps_train": pins["tc.txt"]}
    rec = build_lists(root, p, owners)
    kt = [str(i) for i in range(1001, 1559)]
    assert rec["halves"]["ktvic_test"] == {"explore": sum(map(half, kt)), "confirm": 558 - sum(map(half, kt))}
    assert 0 < rec["halves"]["ktvic_test"]["explore"] < 558 and rec["vitextvqa_dev_images"] == 5
    assert [half(str(i)) for i in range(24)] == [int(hashlib.sha256(f"{i}c_pvr".encode()).hexdigest()[-1], 16) % 2 == 0
                                                 for i in range(24)]
    kv = lambda k, o: {"ktvic_train": k, "openviic_train": o}  # noqa: E731
    assert rec["d_vi"] == {  # 9 via owner 1's file 5100 (a hop), 11 via test id 1001's file (a hop), 5104 via 9
        "ktvic_train_images": 3, "openviic_train_images": 3, "removed": kv(9, 5),
        "removed_by_source": {"ktvic_owners": kv(6, 3), "ktvic_test_side": kv(1, 2), "openviic_owners": kv(2, 0)},
        "removed_hop_only": kv(2, 1), "ktvic_owner_ids": {"h_bdt1_739": 3, "ktvic_dev299": 1, "refused_ktvic_dup": 1},
        "ktvic_owner_ids_distinct": 5, "ktvic_train_captions": 9, "openviic_train_captions": 6}, rec["d_vi"]
    mp = files["map.json"]["_pairs"]
    for name, bad_map, msg in (
            ("m1", {**mp, "train": {**mp["train"], "8": [[ovf(5102), "train", 0, 0]]}}, "copy-map entry is not"),
            ("m2", {**mp, "train": {**mp["train"], "8": [e5(ovf(5102), "val")]}}, "copy-map entry is not"),
            ("m3", {**mp, "train": {**mp["train"], "8": [e5("x.jpg")]}}, "copy-map entry is not"),
            ("m4", {**mp, "train": {**mp["train"], "8": [[5102, "train", 0, 0, 0.0]]}}, "copy-map entry is not"),
            ("m5", {**mp, "test": {k: v for k, v in mp["test"].items() if k != "1558"}}, "copy map keys"),
            ("m6", {**mp, "train": {**mp["train"], "99": []}}, "copy map keys")):
        (root / f"{name}.json").write_text(json.dumps({"_pairs": bad_map}))
        _must(msg, build_lists, root, {**p, "copy_map": (f"{name}.json", G.sha_bytes((root / f"{name}.json").read_bytes()))},
              owners)
    want_ta = sorted(tc, key=lambda i: hashlib.sha256((i + "c_pvr_TA").encode()).hexdigest())[:1070]
    assert rec["t_a_ids"] == want_ta and len(want_ta) == 1070 and rec["d_tc_images_before_w25"] == 5
    _must("inputs not pinned ['textcaps_train']", build_lists, root, {**p, "textcaps_train": None}, owners)
    _must("differs from its pin", build_lists, root, {**p, "ktvic_test": ("kt.json", "0" * 64)}, owners)
    (root / "ex2.json").write_text(json.dumps({"ids": {"ktvic": {"d": ["99"]}}}))
    _must("['refused_ktvic_dup']: ids that are not KTVIC train", build_lists, root, p, {
        **owners, "refused_ktvic_dup": {"source": ["ex2.json", G.sha_bytes((root / "ex2.json").read_bytes()),
                                                   "ids/ktvic/d"]}})
    for name, d, msg in (("kt2.json", {"images": [{"id": 1}] * 558}, "not 558"),
                         ("kt3.json", {"images": [{"id": str(i)} for i in range(1001, 1559)]}, "not an int"),
                         ("ov2.json", {f"x{i}.jpg": {} for i in range(2001)}, "not an 11-digit")):
        (root / name).write_text(json.dumps(d))
        key = "openviic_test" if name.startswith("ov") else "ktvic_test"
        _must(msg, build_lists, root, {**p, key: (name, G.sha_bytes((root / name).read_bytes()))}, owners)
    (root / "tc2.txt").write_text("a\nb\n")
    _must("fewer than T_A", build_lists, root, {**p, "textcaps_train": ("tc2.txt", G.sha_bytes(b"a\nb\n"))}, owners)
    (root / PDIR).mkdir(parents=True)
    (base / "lsealed").mkdir()
    cmd_lists(root, base / "lsealed", p, owners)
    assert (root / LISTS_FILE).stat().st_mode & 0o777 == 0o444 and json.loads((root / LISTS_FILE).read_text())["t_a_ids"]
    assert (base / "lsealed/ACCESS_LOG.tsv").read_text().split("\t")[2] == "lists write"
    _must("one write", cmd_lists, root, base / "lsealed", p, owners)
    assert set(LISTS_IN) == set(p) and [k for k, v in LISTS_IN.items() if v is None] == []
    assert all(OWNERS[k]["status"] == "compute" for k in DVI_KT + DVI_OV)


def _hex(n: int) -> str:
    return f"{n:016x}"


def _jpeg(seed: int, rgb: tuple, side: int = 64) -> bytes:
    """Noise around one colour: the dummy SSCD separates the fixture colours (cosine < 0.5, asserted below)."""
    from PIL import Image

    rng = np.random.default_rng(seed)
    px = np.clip(np.array(rgb) + rng.integers(-25, 26, (side, side + 16, 3)), 0, 255).astype(np.uint8)
    b = io.BytesIO()
    Image.fromarray(px).save(b, "JPEG", quality=90)
    return b.getvalue()


def _sscd(base: Path) -> Path:
    import torch

    class Net(torch.nn.Module):  # dummy SSCD (w25.py selftest): 512-d unit vector of pooled colour statistics
        def forward(self, x):
            v = torch.cat([x.mean((2, 3)), x.std((2, 3))], 1).repeat(1, 86)[:, :512]
            return v / (v * v).sum(1, keepdim=True).sqrt()

    p = base / "dummy_sscd.pt"
    torch.jit.script(Net()).save(str(p))
    return p


def _log(w: dict, line: str) -> None:
    with open(w["base"] / "LOG.md", "a", encoding="utf-8") as f:
        f.write(f"2026-01-01T00:00:00Z {line}\n")


def _world(base: Path, imgs: dict) -> dict:
    """Static part of a synthetic W25 world: repo root, owner caches, frozen owners file, owner-feats caches and
    manifest (through owner_feats_cmd), LOG, proc, backup, sealed dir."""
    root, inp, sealed = base / "root", base / "in", base / "sealed"
    for d in (root, inp, base / "proc", base / "src", root / "imgs"):
        d.mkdir()
    sealed.mkdir(mode=0o700)
    sscd = _sscd(base)
    src = [base / "src/a.jpg", base / "src/b.jpg"]
    for p, k in zip(src, "AB"):
        p.write_bytes(imgs[k])
    f = BM.features(src, str(sscd), workers=1)
    for i, k in enumerate("ab"):
        W.save(inp / f"own_{k}.npz", [f"o{k}"], {"sha": [f["sha"][i]], **{x: f[x][[i]] for x in W.KEYS},
                                                   "unreadable": []}, set=k)
    sc = {k: CP.sha_file(inp / f"own_{k}.npz") for k in "ab"}
    (root / "imgs/c1.jpg").write_bytes(imgs["E"])
    (root / "imgs/00000000007.jpg").write_bytes(imgs["Y"])
    for name, body in (("sel.txt", "ob\n"), ("comp.txt", "c1\n"), ("comp2.txt", "7\n"),
                       ("carve.json", json.dumps({"carve": ["777.jpg", "888.jpg"]})),
                       ("rule.json", json.dumps({
                           CP.OVQA_DEV: {"images": "images", "qa": "annotations", "image_names": "values"},
                           "vlsp2023_train_data.json": {"images": "images", "qa": "annotations"},
                           "vlsp2023_test_data.json": {"images": None, "qa": "annotations"}}))):
        (root / name).write_text(body)
    h = {n: CP.sha_file(root / n) for n in ("sel.txt", "comp.txt", "comp2.txt", "carve.json")}
    doc = {"schema": SCHEMA, "owners": {
        "whole": cached(1, {"own_a.npz": sc["a"]}),
        "sel": cached(1, {"own_a.npz": sc["a"], "own_b.npz": sc["b"]}, ("sel.txt", h["sel.txt"], None)),
        "comp": compute(1, ("comp.txt", h["comp.txt"], None), "imgs", "jpg"),
        "comp2": compute(1, ("comp2.txt", h["comp2.txt"], None), "imgs", "ktvic"),
        "carve": {"status": "id_join", "n": 2, "source": ["carve.json", h["carve.json"], "carve"]},
        "far": deferred("held nowhere")}}
    (root / "owners.json").write_bytes(G.jdump(doc))
    osha = CP.sha_file(root / "owners.json")
    (base / "LOG.md").write_text("", "utf-8")
    w = {"base": base, "root": root, "sscd": sscd, "owners_sha": osha, "doc": doc, "n_tag": 0}
    _log(w, f"OPS-own owners frozen {osha}")
    (base / "backup.sh").write_text("rsync m1:/root ~/b\n")
    env = {"root": root, "owners": root / "owners.json", "owners_sha": osha, "log": base / "LOG.md", "in": inp,
           "sscd": sscd, "sscd_ok": str, "features": BM.features, "workers": 1, "sealed": sealed,
           "feats": root / "owner_feats.json", "feats_sha": None}
    run = CP.sha_file(Path(__file__))
    assert owner_feats_cmd(env, run, "comp2") == {"written": ["comp2"], "manifest": False}
    _must("is not a 'compute' owner", owner_feats_cmd, env, run, "whole")
    rec = owner_feats_cmd(env, run)
    assert set(rec["owners"]) == {"comp", "comp2"} and rec["owners"]["comp"]["cache"] == "of_comp.npz"
    assert (inp / "of_comp.npz").stat().st_mode & 0o777 == 0o400 and env["feats"].stat().st_mode & 0o777 == 0o444
    assert W.load(inp / "of_comp2.npz")["ids"] == ["7"]
    rows = [x.split("\t")[2:4] for x in (sealed / "ACCESS_LOG.tsv").read_text().splitlines()]
    assert rows == [["owner-feats write", "of_comp2.npz"], ["owner-feats write", "of_comp.npz"],
                    ["owner-feats manifest", "owner_feats.json"]], rows
    assert owner_feats_cmd(env, run) == {"written": ["comp", "comp2"], "manifest": False}
    w["feats_sha"] = CP.sha_file(env["feats"])
    _log(w, f"OPS-feats owner-feats manifest {w['feats_sha']}")
    (sealed / "ACCESS_LOG.tsv").unlink()
    return w


def _tag(w: dict) -> str:
    w["n_tag"] += 1
    tag = f"OPS-st{w['n_tag']}"
    _log(w, f"{tag}: W25 window, pause of every other laptop job")
    return tag


def _ovqa(w: dict, sealed: Path, ov: dict, dup: bool = False) -> bytes:
    """OpenViVQA fixture: 3 json files through the pinned c_pvr.ovqa_fetch, and a zip whose pin is patched in."""
    nq = len(ov) + 1
    data = {CP.OVQA_DEV: {"images": {str(k): n for k, n in enumerate(sorted(ov))},
                          "annotations": {str(k): {"image_id": 0} for k in range(nq)}},
            "vlsp2023_train_data.json": {"images": {"0": "t", "1": "u"}, "annotations": [0, 1]},
            "vlsp2023_test_data.json": {"annotations": [0]}}
    blobs = {k: json.dumps(v).encode() for k, v in data.items()}
    spec = {k: (len(b), hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()) for k, b in blobs.items()}
    CP.OVQA_COUNTS = {CP.OVQA_DEV: (len(ov), nq), "vlsp2023_train_data.json": (2, 2), "vlsp2023_test_data.json": (1, 1)}
    CP.ovqa_fetch(sealed / "ovqa", sealed, spec, lambda n, p: p.write_bytes(blobs[n]) and 0)
    zb = io.BytesIO()
    with zipfile.ZipFile(zb, "w") as z:
        z.writestr("dev-images/", b"")
        for n, b in ov.items():
            z.writestr(f"dev-images/{n}", b)
        if dup:
            z.writestr(f"other/{sorted(ov)[0]}", b"x")
    zp = w["base"] / "src/zip.bin"
    zp.write_bytes(zb.getvalue())
    CP.OVQA_DEV_ZIP = CP.blob_hashes(zp)[:2]
    return zb.getvalue()


def _fresh(w: dict, noc: dict, ov: dict, oi_drop: tuple = (), dup: bool = False) -> tuple[dict, list]:  # noqa: C901
    """Mutable part: G-A ids, OI list, OpenViVQA files; every earlier run's outputs, parts and logs removed."""
    base, root = w["base"], w["root"]
    for d in ("work", "out", "shm", "ga", "sealed/ovqa"):
        shutil.rmtree(base / d, ignore_errors=True)
    for f in ("dlog", "sealed/ACCESS_LOG.tsv"):
        (base / f).unlink(missing_ok=True)
    for d in ("out", "ga"):
        (base / d).mkdir()
    ids = sorted(noc)
    (root / "ga.txt").write_text("".join(f"{i}\n" for i in ids))
    with open(base / "ga" / G.OIL["name"], "w", newline="", encoding="utf-8") as f:
        f.write(",".join(G.OI_HEADER) + "\n")
        for i in sorted(set(ids) - set(oi_drop)):  # _hex(16) lands on Flickr photo 777 (the id-join fixture)
            land = "https://www.flickr.com/photos/u/777/" if i == _hex(16) else ""
            f.write(",".join([i, "test", "", land] + [""] * 8) + "\n")
    zbytes, calls, ticks = _ovqa(w, base / "sealed", ov, dup), [], iter(range(10 ** 9))

    def get(url):
        calls.append(url)
        return noc[url.rsplit("/", 1)[1][:-4]]

    def runner(argv):
        calls.append(argv)
        Path(argv[argv.index("-o") + 1]).write_bytes(zbytes)
        return 0

    env = {"root": root, "ga": base / "ga", "sealed": base / "sealed", "work": base / "work", "dlog": base / "dlog",
           "ovqa": base / "sealed/ovqa", "out": base / "out", "owners": root / "owners.json", "shm": base / "shm",
           "lock": base / "lock", "log": base / "LOG.md", "backup": base / "backup.sh", "proc": base / "proc",
           "t0": time.time(), "clock": lambda: 1.0e9 + next(ticks), "strict": False,
           "pins_b": {"ga_rem": ("ga.txt", CP.sha_file(root / "ga.txt"))}, "n_remain": len(ids), "batch": 3,
           "in": base / "in", "sscd": w["sscd"], "sscd_ok": str, "xm": set, "get": get, "runner": runner,
           "features": BM.features, "workers": 1, "fetchers": 2, "rule": ("rule.json", CP.sha_file(root / "rule.json")),
           "owners_sha": w["owners_sha"], "feats": root / "owner_feats.json", "feats_sha": w["feats_sha"]}
    assert all(v.resolve().is_relative_to(base.resolve()) for v in env.values() if isinstance(v, Path))
    return env, calls


def _go(env: dict, tag: str) -> dict:
    return w25(env, tag, CP.sha_file(Path(__file__)))


def _alog(env: dict) -> list[str]:
    p = env["sealed"] / "ACCESS_LOG.tsv"
    rows = [x.split("\t") for x in p.read_text().splitlines()] if p.exists() else []
    return [r[2] for r in rows if r[1] == "c_pvr_run.py"] + [r[2] for r in rows if r[2] == "ovqa-pin read keys/lengths"]


def _abort(env: dict) -> str:
    rows = [x.split("\t") for x in (env["sealed"] / "ACCESS_LOG.tsv").read_text().splitlines()]
    return [r[3] for r in rows if r[2] == "w25 abort"][-1]


def _st_w25_good(w: dict, imgs: dict) -> None:
    lost9 = {x: (None, "HTTPError") for x in [_hex(16 + i) for i in range(8)] + [G.FLICKR_W3[0]]}
    noc = {_hex(1): (imgs["A"], ""), _hex(2): (imgs["T"], ""), _hex(3): (imgs["E"], ""), **lost9}
    env, calls = _fresh(w, noc, {"w.jpg": imgs["A2"], "x.jpg": imgs["A"], "y.jpg": imgs["B"], "z.jpg": imgs["Z"]})
    rec = _go(env, _tag(w))
    nt, ov = rec["nocaps_test"], rec["ovqa_dev"]
    assert (nt["queried"], nt["featured"], nt["lost"], nt["truncated"], nt["flagged"]) == (12, 2, 10, 1, 2), nt
    assert nt["flagged_by_owner"]["comp"]["C1_C2_registered"] == 1 and nt["flagged_by_owner"]["comp2"]["excluded"] == 0
    assert nt["lost_by_class"] == {"fetch HTTPError": 9, "decode OSError": 1}, nt["lost_by_class"]
    assert nt["flagged_by_owner"]["whole"]["C1_C2_registered"] == 1 and nt["flagged_by_owner"]["sel"]["excluded"] == 0
    assert (ov["featured"], ov["lost"], ov["flagged"], ov["flagged_or_lost"]) == (3, 1, 3, 4), ov
    assert ov["flagged_by_owner"]["sel"]["excluded"] == 1 and ov["flagged_by_owner"]["whole"] == {
        "C1_C2_registered": 1, "C3_sscd_0.75": 2, "excluded": 2, "report_sscd_0.5": 2}, ov["flagged_by_owner"]
    assert rec["owners_compared"] == ["comp", "comp2", "sel", "whole"] and rec["ovqa_identity_c"]["dev_names_in_zip"] == 4
    assert rec["n_e_power_inputs"] == {"w25_flagged": 2, "lost": 10} and rec["owners_sha256"] == env["owners_sha"]
    assert rec["id_join_beside_n_e_power"] == {"by_owner": {"carve": 1}, "hits": 1, "hits_also_flagged_or_lost": 1}
    assert rec["owners_deferred"] == ["far"] and rec["feats_sha256"] == env["feats_sha"]
    assert nt["flickr_w3_in_flagged_or_lost"] == 1 and ov["flickr_w3_in_flagged_or_lost"] == 0
    o = env["out"]
    assert (o / "w25_flagged_ids.txt").read_text() == f"{_hex(1)}\n{_hex(3)}\n"  # _hex(3): the compute owner
    assert (o / "w25_f30k_join_ids.txt").read_text() == f"{_hex(16)}\n"
    assert (o / "w25_lost_ids.txt").read_text() == "".join(f"{i}\n" for i in sorted([_hex(2), *lost9]))
    assert (o / "w25_ovqa_out_ids.txt").read_text() == "w.jpg\nx.jpg\ny.jpg\nz.jpg\n"  # w: C3 only
    assert all((o / x).stat().st_mode & 0o777 == 0o444 for x in OUTS)
    assert json.loads((o / "w25_counts.json").read_text()) == rec
    urls = [c for c in calls if isinstance(c, str)]
    assert sorted(urls) == sorted(CP.OI_TEST_URL.format(file=f"{i}.jpg") for i in noc)
    argv = [c for c in calls if isinstance(c, list)]
    assert len(argv) == 1 and argv[0][0] == "curl" and argv[0][-1] == CP.OVQA_URL.format(rev=CP.OVQA_REV, name=OVQA_ZIP)
    assert not os.path.lexists(env["shm"]) and not list(w["base"].rglob(OVQA_ZIP))
    dl = env["dlog"].read_text().splitlines()
    assert [x.split("\t")[3] for x in dl] == ["3 files", "0 files", "0 files", "0 files", "3 files", "1 files",
                                               "1 files", "0 files"], dl
    assert "nocaps_test_b0000" in dl[0] and "trap" in dl[-1] and "after ovqa_dev" in dl[-2]
    assert _alog(env) == ["w25 start", "w25 projection", "w25 decide", "w25 end"] + ["ovqa-pin read keys/lengths"] * 5
    parts = sorted((env["work"] / "parts").iterdir())
    assert [p.name for p in parts] == [f"nocaps_test_{n:04d}.npz" for n in range(4)] + [f"ovqa_dev_{n:04d}.npz"
                                                                                         for n in range(2)]
    assert all(p.stat().st_mode & 0o777 == 0o400 for p in parts)
    _must("a W25 output", _go, env, _tag(w))
    for x in OUTS:
        (o / x).chmod(0o644)
        (o / x).unlink()
    _must("'w25 decide' row exists", _go, env, _tag(w))  # N2: the row binds even when the outputs are gone
    assert len([c for c in calls if isinstance(c, str)]) == 12
    q, lost, trunc = collect(env, "nocaps_test", sorted(noc), CP.sha_file(Path(__file__)))
    assert len(q["ids"]) == 2 and trunc == [_hex(2)]
    _must("does not belong", read_part, parts[0], "nocaps_test", sorted(noc)[:3], "0" * 64)
    _must("does not belong", read_part, parts[0], "ovqa_dev", sorted(noc)[:3], CP.sha_file(Path(__file__)))
    _must("does not belong", read_part, parts[0], "nocaps_test", sorted(noc)[3:6], CP.sha_file(Path(__file__)))
    parts[1].chmod(0o600)
    parts[1].unlink()
    _must("decide needs every part", collect, env, "nocaps_test", sorted(noc), CP.sha_file(Path(__file__)))


def _st_w25_resume(w: dict, imgs: dict) -> None:
    noc = {_hex(1): (imgs["A"], ""), _hex(3): (imgs["E"], ""), _hex(4): (imgs["E"], ""), _hex(5): (imgs["Y"], "")}
    env, calls = _fresh(w, noc, {"x.jpg": imgs["Y"]})
    n = [0]

    def boom_at(k):
        def f(*a, **kw):
            n[0] += 1
            if n[0] == k:
                raise SystemExit("boom")
            return BM.features(*a, **kw)
        return f

    parts = lambda: sorted(p.name for p in (env["work"] / "parts").iterdir())  # noqa: E731
    env["features"], tag = boom_at(2), _tag(w)  # nocaps batch 1
    _must("boom", _go, env, tag)
    assert not os.path.lexists(env["shm"]) and _abort(env) == "boom" and parts() == ["nocaps_test_0000.npz"]
    _must("already opened a window", _go, env, tag)
    n[0], env["features"] = 0, boom_at(2)  # this process: nocaps batch 1, then ovqa batch 0 fails
    _must("boom", _go, env, _tag(w))
    ident = env["work"] / "ovqa_identity_c.json"
    assert parts() == ["nocaps_test_0000.npz", "nocaps_test_0001.npz"] and ident.exists()
    env["features"] = BM.features
    shutil.rmtree(env["out"])
    env["out"].write_text("not a dir")
    _must("write failed or exists", _go, env, _tag(w))  # decide fails after every part exists
    env["out"].unlink()
    env["out"].mkdir()
    assert parts()[-1] == "ovqa_dev_0000.npz" and len([c for c in calls if isinstance(c, list)]) == 2
    ib = ident.read_bytes()
    ident.chmod(0o600)
    ident.unlink()
    _must("identity record (c) is missing", _go, env, _tag(w))
    ident.write_bytes(ib)
    rec = _go(env, _tag(w))
    assert rec["nocaps_test"]["featured"] == 4 and rec["nocaps_test"]["flagged"] == 4  # A, E (comp) x2, Y (comp2)
    assert len([c for c in calls if isinstance(c, list)]) == 2, "dev-images.zip was fetched with every ovqa part done"
    assert sorted(c.rsplit("/", 1)[1] for c in calls if isinstance(c, str)) == sorted(
        f"{i}.jpg" for i in [_hex(1), _hex(3), _hex(4)] + [_hex(5)] * 2), "a finished part was fetched again"


def _st_w25_faults(w: dict, imgs: dict) -> None:
    ok = {_hex(1): (imgs["E"], ""), _hex(3): (imgs["Y"], "")}
    ov = {"y.jpg": imgs["Y"]}
    for err in ("status 403", "redirected", "not a JPEG body", ""):
        env, calls = _fresh(w, {**ok, _hex(2): (None, err)}, ov)
        _must("prereg §8.1: FAULT", _go, env, _tag(w))
        assert not os.path.lexists(env["shm"]) and _abort(env) == "FAULT" and not list(env["out"].iterdir())
    env, calls = _fresh(w, ok, ov, oi_drop=(_hex(3),))
    _must("outside the official OI test list", _go, env, _tag(w))
    assert calls == [] and _alog(env) == [] and not os.path.lexists(env["shm"])
    env, calls = _fresh(w, {**ok, **{_hex(16 + i): (None, "TimeoutError") for i in range(11)}}, ov)
    _must("nocaps_test: 11 images lost", _go, env, _tag(w))
    assert len(list((env["work"] / "parts").iterdir())) == 5 and not os.path.lexists(env["shm"])
    env, calls = _fresh(w, ok, {"y.jpg": imgs["Y"], "z1.jpg": imgs["Z"], "z2.jpg": imgs["Z"][:-1]})
    _must("ovqa_dev: 2 images lost", _go, env, _tag(w))
    env, calls = _fresh(w, ok, ov)
    env["xm"] = lambda: {G.sha_bytes(imgs["Y"])}
    _must("XM3600 image by sha256", _go, env, _tag(w))
    env, calls = _fresh(w, {_hex(1): (imgs["E"], "")}, {"y.jpg": imgs["Y"]})
    env["xm"] = lambda: {G.sha_bytes(imgs["Y"])}
    _must("XM3600 image by sha256", _go, env, _tag(w))
    env, calls = _fresh(w, ok, ov)
    env["runner"] = lambda argv: Path(argv[argv.index("-o") + 1]).write_bytes(b"PK") and 0
    _must("differ from the LFS pin", _go, env, _tag(w))
    env, calls = _fresh(w, ok, ov)
    r0 = env["runner"]
    env["runner"] = lambda argv: r0(argv) or 22
    _must("rc 22", _go, env, _tag(w))
    env, calls = _fresh(w, ok, ov, dup=True)
    _must("two members named y.jpg", _go, env, _tag(w))
    env, calls = _fresh(w, ok, ov)
    _must("is not 3 unique ids", _go, {**env, "n_remain": 3}, _tag(w))
    _must("LOG-line sha (ovqa_names)", _go, {**env, "rule": (env["rule"][0], "0" * 64)}, _tag(w))
    CP.OVQA_COUNTS = {**CP.OVQA_COUNTS, CP.OVQA_DEV: (2, 2)}
    _must("plain file names", _go, env, _tag(w))
    env, calls = _fresh(w, ok, {"bad name.jpg": imgs["Y"]})
    _must("plain file names", _go, env, _tag(w))
    assert calls == []


def _st_w25_window(w: dict, imgs: dict) -> None:
    ok, ov = {_hex(1): (imgs["E"], ""), _hex(3): (imgs["Y"], "")}, {"y.jpg": imgs["Y"]}
    env, calls = _fresh(w, ok, ov)
    env["shm"].mkdir(mode=0o700)
    fd = os.open(env["lock"], os.O_RDWR | os.O_CREAT, 0o600)
    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    _must("the W25 lock is held", _go, env, _tag(w))
    assert env["shm"].is_dir() and calls == []
    os.close(fd)
    _must("residue of an earlier window", _go, env, _tag(w))
    assert env["shm"].is_dir() and calls == [] and _alog(env) == []
    env, calls = _fresh(w, ok, ov)
    _must("tenancy: the pause tag is in 0", _go, env, "OPS-never")
    _must("does not name W25", _go, env, "OPS-own")
    _must("exclusion pin", _go, {**env, "xm": lambda: fault("exclusion pin")}, _tag(w))
    sel = w["root"] / "sel.txt"
    sel.write_text("oa\n")
    _must("sel.txt differs from its pin", _go, env, _tag(w))  # N2: owner rows load before any pixel moves
    sel.write_text("ob\n")
    assert calls == [] and not os.path.lexists(env["shm"]) and _alog(env) == []
    for k, v, msg in (("owners_sha", "0" * 64, "differs from --owners-sha"), ("in", Path("/mnt/c_pvr_st_never"),
                                                                              "WSL ext4 home"),
                      ("sscd_ok", lambda p: fault("SSCD weights differ"), "SSCD weights differ")):
        e2 = {**env, k: v}
        _must(msg, _go, e2, _tag(w))
    (env["out"] / "w25_counts.json").write_text("{}")
    _must("a W25 output", _go, env, _tag(w))
    env, calls = _fresh(w, {**ok, _hex(4): (imgs["A"], ""), _hex(5): (imgs["A"], "")}, ov)
    k = iter(range(10 ** 9))
    env["clock"] = lambda: 1.0e9 + 50000 * next(k)
    _must("projection exceeds the 24 h stop", _go, env, _tag(w))
    assert [p.name for p in (env["work"] / "parts").iterdir()] == ["nocaps_test_0000.npz"]
    assert "w25 projection" in _alog(env) and not os.path.lexists(env["shm"]) and _abort(env) == "STOP"
    env, calls = _fresh(w, ok, ov)
    (env["work"]).mkdir()
    (env["work"] / "deadline").write_text("5\n")
    _must("wall-clock stop is reached", _go, env, _tag(w))
    assert calls == [] and not os.path.lexists(env["shm"])
    env, calls = _fresh(w, {**ok, _hex(4): (imgs["A"], ""), _hex(5): (imgs["A"], "")}, ov)

    def job(*a, **kw):
        (w["base"] / "proc/91").mkdir(exist_ok=True)
        (w["base"] / "proc/91/cmdline").write_bytes(b"bash\0c_pvr_job.sh\0")
        return BM.features(*a, **kw)

    env["features"] = job
    _must("tenancy: a foreign *_job.sh", _go, env, _tag(w))
    shutil.rmtree(w["base"] / "proc/91")
    env, calls = _fresh(w, ok, ov)
    signal.signal(signal.SIGTERM, signal.SIG_DFL)
    before = signal.getsignal(signal.SIGTERM)
    env["features"] = lambda *a, **kw: os.kill(os.getpid(), signal.SIGTERM) or BM.features(*a, **kw)
    _must("ABORT: signal 15", _go, env, _tag(w))
    assert signal.getsignal(signal.SIGTERM) is before and not os.path.lexists(env["shm"])
    assert _abort(env) == "ABORT"


def _frz(w: dict, env: dict, name: str, doc: dict, key: str = "owners") -> dict:
    """A variant owners/manifest file, frozen in the fixture LOG; returns the env that points at it."""
    p = w["base"] / name
    p.write_bytes(G.jdump(doc))
    _log(w, f"OPS-x {key} {CP.sha_file(p)}")
    return {**env, key: p, f"{key}_sha": CP.sha_file(p)}


def _st_w25_owners(w: dict, imgs: dict) -> None:
    env, _ = _fresh(w, {_hex(1): (None, "HTTPError"), _hex(16): (None, "HTTPError")}, {"y.jpg": b"\xff\xd8"})
    doc = json.loads(json.dumps(w["doc"]))
    o = doc["owners"]
    cmp, joins, dfr = owners_load(env)
    assert sorted(cmp) == ["comp", "comp2", "sel", "whole"] and list(joins) == ["carve"] and dfr == ["far"]
    assert cmp["comp"]["caches"] == {"of_comp.npz": CP.sha_file(env["in"] / "of_comp.npz")}
    assert owner_feats(env, o["whole"])["ids"] == ["oa"] and owner_feats(env, o["sel"])["ids"] == ["ob"]
    _must("hold 1 rows, not 2", owner_feats, env, {**o["whole"], "n": 2})
    _must("1 rows, not n = 2", owner_feats, env, {**o["sel"], "n": 2})
    shutil.copyfile(env["in"] / "own_b.npz", env["in"] / "own_b2.npz")
    CACHE_SPACE["own_b2.npz"] = "fx"
    try:  # B1: a selected id with two rows (here: the same cache staged twice) is a FAULT, never a silent pass
        _must("1 with more than one", owner_feats, env, {**o["sel"], "caches": {
            **o["sel"]["caches"], "own_b2.npz": CP.sha_file(env["in"] / "own_b2.npz")}})
    finally:
        CACHE_SPACE.pop("own_b2.npz")
    _must("not of one known id space", owner_feats, env, {**o["sel"], "caches": {**o["sel"]["caches"],
                                                                                 "own_c.npz": "0" * 64}})
    _must("not of one known id space", owner_feats, env, {**o["sel"], "caches": {"own_z.npz": "0" * 64,
                                                                                 "own_y.npz": "0" * 64}})
    (w["root"] / "sel2.txt").write_text("ob\nzz\n")
    _must("1 ids without a row", owner_feats, env, {**o["sel"], "select": ["sel2.txt", CP.sha_file(
        w["root"] / "sel2.txt"), None]})
    _must("differs from its pin", owner_feats, env, {**o["sel"], "select": ["sel.txt", "0" * 64, None]})
    assert join_hits({**env, "root": w["root"]}, [_hex(16), _hex(17)], o["carve"]) == [_hex(16)]
    (w["root"] / "carve2.json").write_text(json.dumps({"carve": ["777.jpg", "x8.jpg"]}))
    _must("n distinct Flickr photo ids", join_hits, env, [_hex(16)], {**o["carve"], "source": [
        "carve2.json", CP.sha_file(w["root"] / "carve2.json"), "carve"]})
    _must("n distinct Flickr photo ids", join_hits, env, [_hex(16)], {**o["carve"], "n": 3})
    man = json.loads(env["feats"].read_text())
    for i, (ch, msg) in enumerate(((None, "not in the owner-feats manifest"),
                                   ({"x": {"status": "held"}}, "no R6 status"),
                                   ({"whole": cached(1, {"own_a.npz": "0" * 64})}, "differs from 0000"),
                                   ({"y": cached(1, {"own_q.npz": "0" * 64})}, "own_q.npz is missing"))):
        owners = {**o, "comp3": compute(1, o["comp"]["source"], "imgs", "jpg")} if ch is None else {**o, **ch}
        e = _frz(w, env, f"ow_{i}.json", {**doc, "owners": owners})
        _must(msg, owners_load, _frz(w, e, f"ow_man_{i}.json", {**man, "owners_sha256": e["owners_sha"]}, "feats"))
    for i, (m, msg) in enumerate((({**man, "owners_sha256": "0" * 64}, "another owners file"),
                                  ({**man, "owners": {**man["owners"], "comp": {**man["owners"]["comp"], "n": 2}}},
                                   "not in the owner-feats manifest"),
                                  ({**man, "owners": {**man["owners"], "comp": {**man["owners"]["comp"],
                                                                                "source_sha256": "0" * 64}}},
                                   "not in the owner-feats manifest"),
                                  ({**man, "owners": {**man["owners"], "comp": {**man["owners"]["comp"],
                                                                                "sha256": "0" * 64}}},
                                   "of_comp.npz is missing or differs"),
                                  ({**man, "schema": "x"}, "another schema"))):
        _must(msg, owners_load, _frz(w, env, f"man_{i}.json", m, "feats"))
    p = w["base"] / "owners_unlogged.json"
    p.write_bytes(G.jdump({**doc, "schema": "x"}))
    _must("no LOG line names the owners sha", owners_load, {**env, "owners": p, "owners_sha": CP.sha_file(p)})
    _must("another schema", owners_load, _frz(w, env, "ow_schema.json", {**doc, "schema": "x"}))
    _must("differs from --owners-sha", owners_load, {**env, "owners_sha": "0" * 64})
    _st_owner_feats_faults(w, env, doc, imgs)


def _st_owner_feats_faults(w: dict, env: dict, doc: dict, imgs: dict) -> None:
    run, base = CP.sha_file(Path(__file__)), w["base"]
    (w["root"] / "imgs/bad.jpg").write_bytes(imgs["T"])  # truncated: never retried (R1d), so a FAULT
    for i, (row, msg) in enumerate((
            (compute(1, ("comp.txt", CP.sha_file(w["root"] / "comp.txt"), None), "imgs", "ktvic"), "file-name rule"),
            (compute(2, ("comp.txt", CP.sha_file(w["root"] / "comp.txt"), None), "imgs", "jpg"), "n = 2 distinct"),
            (compute(1, ("comp2.txt", CP.sha_file(w["root"] / "comp2.txt"), None), "imgs", "jpg"), "1 image files"),
            (compute(1, ("bad.txt", None, None), "imgs", "file"), "cannot be featured"))):
        if row["source"][0] == "bad.txt":
            (w["root"] / "bad.txt").write_text("bad.jpg\n")
            row["source"][1] = CP.sha_file(w["root"] / "bad.txt")
        e = _frz(w, {**env, "in": base / f"in_f{i}", "feats": base / f"feats_f{i}.json"}, f"of_{i}.json",
                 {**doc, "owners": {"k": row}})
        _must(msg, owner_feats_cmd, e, run)
        assert not os.path.lexists(e["feats"])
    _must("WSL ext4 home", owner_feats_cmd, {**env, "in": Path("/mnt/c_pvr_st_never")}, run)
    d = w["root"] / "imgs"
    (d / "00000000008.png").write_bytes(b"x")
    (d / "00000000009.png").write_bytes(b"x")
    (d / "00000000009.jpeg").write_bytes(b"x")
    assert fname("ktvic", "7", d) == "00000000007.jpg" and fname("ktvic", "8", d) == "00000000008.png"
    assert fname("jpg", "ab", d) == "ab.jpg" and fname("file", "a.png", d) == "a.png"
    _must("2 files, not exactly one", fname, "ktvic", "9", d)
    _must("0 files, not exactly one", fname, "ktvic", "10", d)
    for rule, i in (("ktvic", "07"), ("ktvic", "x"), ("jpg", "../x"), ("file", "a/b"), ("other", "1")):
        _must("file-name rule", fname, rule, i, d)


def _st_w25(base: Path) -> None:
    keep = (CP.OVQA_COUNTS, CP.OVQA_DEV_ZIP)
    CACHE_SPACE.update({"own_a.npz": "fx", "own_b.npz": "fx", "own_c.npz": "fy"})
    try:
        t = _jpeg(5, (90, 90, 90), side=160)
        imgs = {"A": _jpeg(1, (200, 30, 30)), "A2": _jpeg(9, (200, 30, 30)), "B": _jpeg(2, (30, 200, 30)), "E": _jpeg(3, (30, 30, 200)),
                "Y": _jpeg(4, (200, 200, 30)), "T": t[:len(t) * 3 // 5], "Z": b"\xff\xd8\xff\xe0" + bytes(200)}
        (base / "w").mkdir()
        w = _world(base / "w", imgs)
        _st_w25_good(w, imgs)
        _st_w25_resume(w, imgs)
        _st_w25_faults(w, imgs)
        _st_w25_window(w, imgs)
        _st_w25_owners(w, imgs)
    finally:
        CP.OVQA_COUNTS, CP.OVQA_DEV_ZIP = keep
        for k in ("own_a.npz", "own_b.npz", "own_c.npz"):
            CACHE_SPACE.pop(k)


def _st_integrity(base: Path) -> None:
    root = base / "iroot"
    (root / "scripts/c_pvr").mkdir(parents=True)
    me = CP.sha_file(Path(__file__))
    shutil.copyfile(Path(__file__), root / SELF_REL)
    (root / "x.txt").write_text("x\n")
    sums = root / "scripts/c_pvr/SHA256SUMS"
    good = f"{me}  {SELF_REL}\n" + G.sha_bytes(b"x\n") + "  x.txt\n"
    sums.write_text(good)
    integrity(root, me)
    _must("--run-sha differs", integrity, root, "0" * 64)
    for body, msg in ((good + "zz\n", "malformed"), (good.replace(f"{me}  ", "0" * 64 + "  ", 1), "no single"),
                      (good + f"{me}  {SELF_REL}\n", "no single"), (good.replace("  x.txt", "  scripts/c_pvr/c_pvr_run.py"
                                                                                   , 1), "no single")):
        sums.write_text(body)
        _must(msg, integrity, root, me)
    sums.write_text(good)
    (root / "x.txt").write_text("y\n")
    _must("do not verify", integrity, root, me)
    assert curl(["/bin/sh", "-c", 'test -z "$HOME" && test "$PATH" = /usr/bin:/bin']) == 0 and curl(["/bin/false"])


def _st_load_cli(base: Path, root: Path) -> None:
    import types

    (base / "empty").mkdir()
    _must("differ from their pins", load, base / "empty")
    m = types.ModuleType("zz_c_pvr_stray")
    m.__file__ = str(root / "scripts/zz_stray.py")
    sys.modules[m.__name__] = m
    try:
        _must("outside the pinned closure", load, root)
    finally:
        del sys.modules[m.__name__]
    load(root)
    keep = os._exit  # no fork here: a fork of this multi-threaded process may deadlock (CC-245 Ruling 6)

    def fake_exit(code):
        raise SystemExit(f"exit {code}")

    os._exit = fake_exit
    try:
        _must("exit 143", sig_handler(-1), 15, None)  # a forked feature worker exits plainly, no trap
    finally:
        os._exit = keep
    _must("ABORT: signal 15", sig_handler(os.getpid()), 15, None)
    fake = base / "fake_root"
    for rel in CODE:
        (fake / rel).parent.mkdir(parents=True, exist_ok=True)
        (fake / rel).symlink_to(root / rel)
    me = [sys.executable, "-I", "-B", str(Path(__file__)), "--root", str(fake)]
    r = subprocess.run(me + ["w25", "--host", "m1", "--run-sha", "x", "--pause-tag", "x", "--owners-sha", "x",
                             "--sscd", "x", "--in", "x"], capture_output=True, text=True)
    assert r.returncode == 2 and "invalid choice" in r.stderr, r.stderr[-300:]
    r = subprocess.run(me + ["owners", "--run-sha", "0" * 64], capture_output=True, text=True)
    assert r.returncode == 1 and "--run-sha differs" in r.stderr, r.stderr[-300:]


def selftest(root: Path) -> None:
    import faulthandler
    import tempfile
    import urllib.request

    faulthandler.dump_traceback_later(300, exit=True)  # N8: a hang leaves a stack, never a silent 600 s timeout
    assert multiprocessing.get_start_method(allow_none=True) == "spawn", "main() must set a non-fork start method"

    no_sockets()
    try:
        urllib.request.urlopen("http://example.invalid/", timeout=1)
    except OSError as e:
        assert "network disabled" in str(e), e
    else:
        raise AssertionError("a socket opened")
    _st_static(root)
    _st_classify()
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        assert not str(base.resolve()).startswith(("/mnt/", "/dev/shm")), "selftest scratch must be ext4"
        _st_tenancy(base)
        _st_owners()
        _st_lists(base)
        _st_integrity(base)
        _st_load_cli(base, root)
        _st_w25(base)
    faulthandler.cancel_dump_traceback_later()
    print(f"selftest ok  {CP.LABEL}  c_pvr_run.py {CP.sha_file(Path(__file__))}  c_pvr.py {CODE[next(iter(CODE))]}")


# ---------------------------------------------------------------------------------------------- cli
def main() -> None:
    # PI-1104c PQ5 = C (CC-250 Ruling 5): build_memory.features' Pool starts its workers by fork+exec, never by a
    # bare fork of this process after torch threads exist; workers stay children of this pid (W25_RUN_DOC §6A H4)
    multiprocessing.set_start_method("spawn")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=ROOT, help="repo root (the mutant harness runs copies)")
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("selftest").add_argument("--root", type=Path, default=argparse.SUPPRESS)
    for c in ("owners", "lists", "owner-feats", "w25"):
        sp.add_parser(c).add_argument("--run-sha", required=True)
    for c in ("owner-feats", "w25"):
        for a in ("--owners-sha", "--sscd"):
            sp.choices[c].add_argument(a, required=True)
        sp.choices[c].add_argument("--in", dest="inp", required=True, help="ext4 dir of the owner caches")
    sp.choices["owner-feats"].add_argument("--owner", help="only this 'compute' owner (default: every one)")
    w = sp.choices["w25"]
    w.add_argument("--host", choices=("laptop",), required=True)  # prereg §8: the named custody host
    for a in ("--pause-tag", "--feats-sha"):
        w.add_argument(a, required=True)
    x = ap.parse_args()
    root = x.root.resolve()
    load(root)
    if x.cmd == "selftest":
        return selftest(root)
    integrity(root, x.run_sha)
    if str(CP.SEALED.resolve()).startswith("/mnt/"):
        fault(f"{CP.SEALED} must sit on the WSL ext4 home")
    CP.SEALED.mkdir(mode=0o700, parents=True, exist_ok=True)
    if x.cmd == "owners":
        return cmd_owners(root, CP.SEALED)
    if x.cmd == "lists":
        return cmd_lists(root, CP.SEALED)
    if x.cmd == "owner-feats":
        no_sockets()
        return print(json.dumps(owner_feats_cmd(real_env(root, x), x.run_sha, x.owner), indent=1, sort_keys=True))
    print(json.dumps(w25(real_env(root, x), x.pause_tag, x.run_sha), indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
