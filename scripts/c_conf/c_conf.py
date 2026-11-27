#!/usr/bin/env python3
"""Paper C, C-CONF host decoder, token guard and ledger writer (registration draft
manuscript/directions/C_CONFIRM_PREREG_DRAFT_2026-11-16_v3.md 18e61111 (drafted on b3c4e405), §2, §4, §5.2, §5.4, §6.4 item 5, §6.5, §7.1,
§10.3, §11.1 row 2). DRAFT on synthetic fixtures under CC-438 FP-7: no study data, no host run, no token, no commit
before a GO. A copy of scripts/c_attr/c_attr.py (a3bd7b93) with the listed changes only (read them as
scripts/c_conf/C_CONF_VS_C_ATTR.diff):
  - sets ov_carve, ov_test and ov_dev_b (D1 and the dry run) only; every other set is refused (§5.4);
  - arms zs, ret, rand d0-d2, perm p1-p2 and LMCap ri / rand / perm; no fix, ret_img, rand_img, X2 mask or copy bound;
  - batch size 1 always (binding 6); every backbone at tau = -inf (binding 10); k, order and tail = the backbone's ret;
  - the token guard: admit() is the one admission (the scorer's four-field rule, c_conf_score.token_ok) and ov_gate()
    the one gate that every reader of an OV-test name or byte calls first; a backbone the token does not list is refused;
  - the truncated-file rule of the first look for the three named OV-test files (ctest.t6, imported after the token);
  - example ids from the C-CONF list files (c_conf_arms.py; OV-dev-B from the pinned c_attr_lists.json);
  - LMCap: the query's own cluster (OV-carve) is skipped by id, beside the shots and the near cut;
  - run ids with the prefix cc_ (LMCap ids carry no '-b1': LMCap is one query per call); D1 = '-fwd50' vs '-rev50';
  - the ledger writer for c_conf_score.py (one tau = -inf row per run and scored set; ids only; kit B via the scorer);
  - inputs (block-0 step 0.1), token (G3; --names-only for the dry run of Q21) and stagecheck (§6.4a at T0).
Removed from the source: Flickr30K split and stores, the SigLIP2 embed, X1 draws, plan1b / plan3, select, summary, t2,
dupcheck, extract, vicheck, cfg, memfiles, fetch, pinsok, t1check, the C-T2 / C-ATTR self-tests, lock / left.
Labels: rehearsal "TIER 2 / DEV-CONFIRM (C-CONF), OV-CARVE"; test "TIER 3 / TEST (C-CONF), SECOND LOOK AT OV-TEST".

  python scripts/c_conf/c_conf.py guard --datasets D --roots R...                       custody (§5.4), every mode
  python scripts/c_conf/c_conf.py token --token T [--decision D] [--names-only]        G3; rc 0 iff the token verifies
  python scripts/c_conf/c_conf.py inputs --block0                                       step 0.1 (sha256 of every input)
  python scripts/c_conf/c_conf.py decode --model M --set S --arm A [--k --order --tpl --draw] --batch1 ...   GPU
  python scripts/c_conf/c_conf.py lmcap --set S --variant ri|rand|perm --batch1 ...                        GPU
  python scripts/c_conf/c_conf.py compare --name N --set ov_dev_b --new F --old F --d1 --out O [--dry-run]  D1
  python scripts/c_conf/c_conf.py stagecheck --token T --dir D [--dry-run]              T0: staged files vs §6.4a
Host paths are fixed under the job's root HOST = $NCS_DATA/.. (/root, or the dry-run sandbox); the arm-list file of a
set is found beside the job's output folder (arm_lists_path). Outputs hold captions and are never committed; ledgers
hold ids and numbers only. Nothing here prints a caption. LMCap is a re-implementation of the LMCap recipe by this
study, not the authors' code.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "scripts" / d) for d in ("c_stage1", "c_stage2", "c_en", "lb", "b1_scaling", "c_test")]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_memory as BM  # noqa: E402  seed, NEAR_COS, N_EX (C's example rule), unchanged
import c_conf_score as CS  # noqa: E402  token_ok, scored_sets, kit_scorer, labels (numpy only at import)
import decode_icl as C  # noqa: E402  Vietnamese template, shown(), memory captions, manifests

lb = C.lb
PDIR = ROOT / "manuscript/prereg/2026-10-30_c_t1"
REG = PDIR / "c_t1_registry.json"
LISTS = PDIR / "c_t1_f30k_lists.json"  # Flickr30K names, refused always (§5.4)
CL = ROOT / "manuscript/prereg/2026-10-22_c_stage1/lists.json"
SCHEMA = "vsps.c_conf.v1"
LABEL = {"ov_carve": CS.LABEL_R, "ov_test": CS.LABEL_T, "ov_dev_b": "D1 / DRY RUN (C-CONF), OV-DEV-B, NEVER SCORED"}
ATTR = ROOT / "scripts/c_attr"
ATTR_LISTS = ATTR / "c_attr_lists.json"  # OV-dev-B lists (K0 reproduces them); pinned by its sidecar
ATTR_LISTS_SHA256 = "8a2b977f9caf37f40bcc2a1b43e5b0c362b99d875ef28bc9640cccf2f9487cd5"  # §6.4a
PERMS, DRAWS, REDECODE_N = (1, 2), (0, 1, 2), 50  # §2: perm p1-p2, rand d0-d2; §9 D1: the first 50 OV-dev-B items
OLD = ("qwen25vl_7b", "internvl3_8b")
CFG = {"qwen25vl_7b": (8, "first", "T1"), "internvl3_8b": (4, "last", "T2"), "aya_vision_8b": (4, "last", "T1")}  # §3
TAU = {m: "-inf" for m in CS.BACKBONES}  # binding 10: no deletion step for any backbone
SETS = {"ov_carve": "vi", "ov_test": "vi", "ov_dev_b": "vi"}  # §5.4: every other set name is refused
SRC = "openviic"  # the three sets are OpenViIC images: the shown caption is the cluster's OpenViIC copy if it has one
LANG_NAME = {"vi": "vietnamese"}
LMCAP_K, LMCAP_N, LMCAP_BEAM, LMCAP_NEW = 4, 3, 3, 40  # Ramos et al. 2023 §3 and App. D
SKIP_RUNS = ("-smoke", "-rev50", "-fwd50")  # D1 and dry-run files are never scored
#: host layout (§10.3): HOST is the job's root (/root, or the dry-run sandbox: the job sets NCS_DATA=$R/ncs-data)
HOST = lb.DATA.parent
CS1, CS2 = HOST / "outputs/c_stage1", HOST / "outputs/c_stage2"
MEM_EMB = ("emb.npz", "59e65f6f6432af97504c59c72fa07b644acbff26938e1365473fad659421f7c0")  # §4, in CS1
DEV_EMB = ("emb_ov_dev_b.npz", "5ad23a678650ae736243a45c39915aaf795a5a46721fd855f67d155945bc8c95")  # in CS2
OV_TRAIN_ANN = ("datasets/openviic/uit-openviic-annotation-train.json",
                "d757520e76b8490df6c7275c2beb8b3ecef0342635a436bea8c3cfd07eb49df0")  # carve references (§5.1)
XGLM, MCLIP = lb.DATA / "models/c_t1_xglm_2_9b", lb.DATA / "models/c_t1_mclip_h14"
MEM_FILES = lb.DATA / "datasets/c_t1_mem/memfiles_vi.json"  # {cid: [path under datasets/, sha256]}: LMCap shot images
#: OV-test on the host (§6.4a, §10.3): nothing before the token; T0 files, then the scoring files
OV_STAGE = HOST / "c_conf_ov_test"
STAGE_T0 = {"emb_ov_test.npz": "644b9200b5237df6bea8803a6d2b3ecbe0a15f443a647f48dad1411e262d7ebf",
            "ex_ov_test.json": "4b33f1ab15870d6f9bf292bbad9f070ba55815e77ae8dda1259b60e93b8dd2d7"}
STAGE_SCORE = {"uit-openviic-annotation-test.json": "66af01bac79af9e197f934ba3628477d5324506092d9a13dfd35330596310b16",
               "ledger_ov_test_1941.jsonl": "50878193f1cfc473786ca86e4cc5eb59f13720faa9d97ea52206dd36c0daa154",
               "ledger_ov_test_2001.jsonl": "5e04d267a461b093af1b996dd21d8ee9a1b30ac2e5029978eba7b431f40f1b54"}
PANEL = ("ktvic_openviic_refs.json", "4eb02cc43841bae4f844ee74d4c01b58e677dc8d6abafdd998c9f5b5706f725d")  # T0 count only
DECISION_NAME = "C_CONF_REHEARSAL_DECISION.json"  # looked up beside the token when --decision is not given
ADMITTED: dict | None = None  # the token verified by admit() in this process; nothing else sets it


def sha(p: Path) -> str:
    return lb.sha256_file(Path(p))


def pinned_file(p: Path, want: str) -> Path:
    if not Path(p).is_file() or sha(p) != want:
        raise SystemExit(f"REFUSED: {p} is missing or differs from its pin {want[:8]}")
    return Path(p)


# ------------------------------------------------------------------------------------------------ token (G3)
def admit(token, decision=None) -> dict:
    """§6.4 item 5 and G3: the one admission for OV-test. The scorer's rule (c_conf_score.token_ok: exactly the four
    fields, field 1 = the sha256 of the rehearsal decision file, backbones = the claims that entered, a licensed look,
    both LOG ids present); the decision file is --decision or the registered name beside the token."""
    global ADMITTED
    if not token:
        raise SystemExit("REFUSED: OV-test needs the token of §6.4 item 5 (G3)")
    dec = Path(decision) if decision else Path(token).parent / DECISION_NAME
    ADMITTED = CS.token_ok(Path(token), dec)
    return ADMITTED


def ov_gate(backbone: str | None = None) -> dict:
    """Every reader of an OV-test name or byte calls this first. Refused unless admit() verified a token in this
    process; a backbone the token does not list is refused (LMCap, the positive control, carries no claim: None)."""
    if ADMITTED is None:
        raise SystemExit("REFUSED: no OV-test name or byte without a verified token (§5.4, G3)")
    if backbone is not None and backbone not in ADMITTED["backbones"]:
        raise SystemExit(f"REFUSED: {backbone} is not in the token's backbones (§6.4 item 5)")
    return ADMITTED


def staged(name: str, pins: dict, folder: Path | None = None) -> Path:
    """One staged OV-test file at its §6.4a sha256 (after the token)."""
    ov_gate()
    return pinned_file((folder or OV_STAGE) / name, pins[name])


def ov_items(clists: dict) -> list[tuple[str, str, str]]:
    """[(name, name, sha256)] of OV-test, 2,001 entries in the pinned TSV order (first look's ctest.ov_rows: 1,997
    distinct sha256, the 1,930/28/42/1 extensions, all inside lists.json refuse). ctest is imported after the gate:
    its import hashes the pinned TSV and the 1,941 list."""
    ov_gate()
    import ctest as CT

    return CT.ov_rows(clists)


def t6(paths: list[Path], call, log: Path):
    """§5.2: the first look's decode rule for the three named truncated files (ctest.t6: strict first; a retry of those
    three only; any other failure is a JOB STOP), around one image-opening call on OV-test."""
    ov_gate()
    import ctest as CT

    return CT.t6("decode", paths, call, log)


# ------------------------------------------------------------------------------------------------ Flickr30K names
def load_lists() -> dict:
    d = json.loads(LISTS.read_text(encoding="utf-8"))
    bad = set(d["carve"]) & (set(d["refuse"]["val"]) | set(d["refuse"]["test"]))
    if bad or set(d["carve"]) & set(d["memory"]):
        raise SystemExit(f"{LISTS}: not a clean tier-1 split")
    return d


# ------------------------------------------------------------------------------------------------ examples
def eligible(row: np.ndarray, cids: list[str]) -> list[int]:
    """C's rule (build_memory.exemplars): clusters by cosine, ties by id, never one at cosine >= NEAR_COS."""
    return [j for j in np.lexsort((cids, -row)) if row[j] < BM.NEAR_COS]


def rand_draw(ds: str, qid: str, ok: list[str], d: int) -> list[str]:
    """Draw 0 is C's rand list exactly; draw d >= 1 seeds the same generator with the draw index appended."""
    s = BM.seed("rand", ds, qid) if d == 0 else BM.seed("rand", ds, qid, f"d{d}")
    return random.Random(s).sample(sorted(ok), BM.N_EX)


def example_ids(arm: str, k: int, order: str | None, qid: str, ex: dict, draw: int) -> list[str]:
    """ex = one set's lists (ids only). perm takes the k-prefix and the order rule of ret (§2)."""
    if arm in ("ret", "perm"):
        ids = ex["perm"][str(draw)][qid][:k] if arm == "perm" else ex["ret"][qid][:k]
        return ids[::-1] if order == "last" else ids
    if arm == "rand":
        return ex["rand"][str(draw)][qid][:k]
    return []


def attr_ex(ds: str) -> dict:
    """OV-dev-B's lists from the pinned C-ATTR list file (its sha256 is that of §6.4a and of its sidecar)."""
    want = (ATTR_LISTS.parent / (ATTR_LISTS.name + ".sha256")).read_text().split()[0]
    if sha(ATTR_LISTS) != want or want != ATTR_LISTS_SHA256:
        raise SystemExit(f"{ATTR_LISTS}: sha256 differs from its sidecar or from §6.4a")
    return json.loads(ATTR_LISTS.read_text(encoding="utf-8"))["sets"][ds]


def arm_lists_path(ds: str, out_dir: Path) -> Path:
    """The C-CONF list file of a set, beside the job's output folder O = out_dir/..: OV-carve from block 0
    (outputs/c_conf_b0[_dry]/lists_ov_carve.json, the suffix following O's), OV-test from T0 (O/lists_ov_test.json)."""
    o = Path(out_dir).parent
    if ds == "ov_carve":
        return o.parent / ("c_conf_b0" + ("_dry" if o.name.endswith("_dry") else "")) / "lists_ov_carve.json"
    return o / "lists_ov_test.json"


def arm_ex(ds: str, out_dir: Path) -> dict:
    """The set's example lists: OV-dev-B from c_attr_lists.json; OV-carve and OV-test from the C-CONF list file,
    checked against its sidecar (its sha256 is logged at block 0 / T0)."""
    if ds == "ov_dev_b":
        return attr_ex(ds)
    if ds == "ov_test":
        ov_gate()
    p = arm_lists_path(ds, out_dir)
    side = Path(str(p) + ".sha256")
    if not p.is_file() or not side.is_file() or sha(p) != side.read_text().split()[0]:
        raise SystemExit(f"REFUSED: {p} is missing or differs from its sidecar")
    ex = json.loads(p.read_text(encoding="utf-8"))
    if ex.get("set") != ds:
        raise SystemExit(f"{p}: not the lists of {ds}")
    return ex


def run_id_of(a) -> str:
    """Unique per model, set, arm, k, order, template, draw / permutation, and D1 mode; '-b1' always (binding 6)."""
    tagd = {"rand": "d", "perm": "p"}.get(a.arm)
    return f"cc_{a.model}_{a.set}-{a.arm}" + (f"-k{a.k}-{a.order or ''}-{a.tpl}" if a.arm != "zs" else "") \
        + (f"-{tagd}{a.draw}" if tagd else "") + (f"-m{a.memory}" if a.arm != "zs" else "") + "-b1" \
        + (f"-{a.redecode}" if a.redecode else "") + ("-smoke" if a.limit else "")


def lmcap_run_id(a) -> str:
    """LMCap run id (one query per generate call, so no '-b1'); the D1 modes in the order of run_id_of."""
    return f"cc_lmcap-{a.variant}_{a.set}-m{a.memory}" + (f"-{a.redecode}" if a.redecode else "") \
        + ("-smoke" if a.limit else "")


def d1_ref(run_id: str) -> str:
    """§9 D1: the reference of a forward decode is this host's reversed-order decode of the same 50 items."""
    if not run_id.endswith("-fwd50"):
        raise SystemExit(f"{run_id}: not a D1 decode")
    return run_id[: -len("-fwd50")] + "-rev50"


def batch_of(a) -> int:
    """Binding 6 (§4): batch size 1 for every decode."""
    if not a.batch1:
        raise SystemExit("REFUSED: batch size 1 only (§4, binding 6): add --batch1")
    return 1


# ------------------------------------------------------------------------------------------------ prompts
def lmcap_block(caps: list[str], lang: str) -> str:
    """One block of LMCap's template (Ramos et al. 2023, App. D), XGLM's </s> between retrieved captions."""
    return ("I am an intelligent image captioning bot. Similar images have the following captions: "
            + " ".join(c.strip() + "</s>" for c in caps)
            + f" A creative short caption I can generate to describe this image in {LANG_NAME[lang]} is:")


def lmcap_prompt(shots: list[tuple[list[str], str]], query_caps: list[str], lang: str) -> str:
    """N fixed shots (retrieved captions, the shot's own caption) then the query block."""
    if len(shots) != LMCAP_N or any(len(c) != LMCAP_K for c, _y in shots) or len(query_caps) != LMCAP_K:
        raise SystemExit("LMCap prompt: not N = 3 shots with K = 4 captions each")
    return "".join(f"{lmcap_block(c, lang)} {y.strip()}</s> " for c, y in shots) + lmcap_block(query_caps, lang)


# ------------------------------------------------------------------------------------------------ registry
def registry() -> dict:
    return json.loads(REG.read_text(encoding="utf-8"))


def model_spec(key: str) -> dict:
    """B-N1 block for the two C backbones; c_t1_registry for Aya; the L1-b registry (sha-pinned) for the others."""
    reg = registry()
    if key in OLD:
        return lb.load_prereg(C.pinned(C.B_N1))["models"][key]
    if key in reg["models"]:
        return reg["models"][key]
    ref = reg["borrowed"][key]
    p = ROOT / ref["registry"]
    if sha(p) != ref["registry_sha256"]:
        raise SystemExit(f"{p}: sha256 differs from c_t1_registry")
    return json.loads(p.read_text(encoding="utf-8"))["models"][key]


def pins_open(m: dict) -> list[str]:
    """Pinned files whose hash is still null (gated LFS hashes; filled from the authenticated tree API first)."""
    return sorted(k for k, v in m.get("files", {}).items() if not v.get("hash"))


# ------------------------------------------------------------------------------------------------ GPU decode
def items_of(ds: str, a) -> list[tuple[str, str, str]]:
    """[(id, file, sha256)]: OV-dev-B by stage 2's carve-out; OV-test by the pinned TSV, after the gate; OV-carve by
    its list file, every row passing C's refusal of test and dev-B images."""
    if ds not in SETS:
        raise SystemExit(f"REFUSED: {ds} is not a set of C-CONF (§5.4)")
    clists = C.load_lists(a.c_lists)
    if ds == "ov_test":
        return ov_items(clists)
    if ds == "ov_dev_b":
        import stage2 as S2
        return S2.manifest2(ds, clists)
    ex = arm_ex(ds, a.out_dir)
    rows = [(i, i, ex["sha"][i]) for i in ex["ids"]]
    C.refuse_rows(rows, SRC, *C.refused(clists))
    return rows


def img_folder(ds: str, a) -> Path:
    """OV-test from the stage folder (after the gate); OV-carve and OV-dev-B from the OpenViIC images under --images."""
    if ds == "ov_test":
        ov_gate()
        return OV_STAGE / "images"
    return Path(a.images) / "openviic/images"


def skeleton(text: str) -> str:
    """A3 (§9): the prompt without its example lines; equal across the arms of one template."""
    return "\n".join(x for x in text.split("\n") if not x.startswith(C.LINE.split("{")[0]))


def memory_text(a):
    """(captions, shown): C's memory captions read from $NCS_DATA (decode_icl.memory_captions), shown with C's
    own-dataset rule for OpenViIC queries."""
    caps = C.memory_captions(C.load_lists(a.c_lists))
    return caps, lambda c: C.shown(caps[c], SRC)


def lmcap_shots(ds: str, mem_keys: list[str], cos: np.ndarray) -> list[str]:
    """LMCap's N fixed shots: N clusters drawn once per set (seeded) among those below C's near cut for every query."""
    safe = sorted(mem_keys[j] for j in np.flatnonzero(cos.max(0) < BM.NEAR_COS))
    return random.Random(BM.seed("lmcap_shots", ds)).sample(safe, LMCAP_N)


def lmcap_skip(qid: str, shots, near: dict, own: dict) -> set[str]:
    """Clusters never shown to q by LMCap's retrieval: the shots, q's SigLIP2 near cut and, on OV-carve, q's own
    cluster by id (§2; §11.1 row 1)."""
    return set(shots) | near[qid] | ({own[qid]} if qid in own else set())


def mem_vectors() -> tuple[list[str], np.ndarray]:
    """The memory's SigLIP2 vectors (§4, pinned), one per cluster (keys without '|')."""
    z = np.load(pinned_file(CS1 / MEM_EMB[0], MEM_EMB[1]))
    keys = [str(k) for k in z["keys"]]
    idx = [n for n, k in enumerate(keys) if "|" not in k]
    return [keys[n] for n in idx], np.asarray(z["vecs"], np.float32)[idx]


def query_vectors(ds: str, ids: list[str], ex: dict, folder: Path | None = None) -> np.ndarray:
    """Rows in the order of ids: OV-dev-B from stage 2's vectors; OV-carve = the memory vector of the query's own
    one-member cluster; OV-test = the first look's stored vectors (no SigLIP2 run over OV-test), after the gate."""
    if ds == "ov_carve":
        mk, mv = mem_vectors()
        col = {c: n for n, c in enumerate(mk)}
        return mv[[col[ex["own"][i]] for i in ids]]
    if ds == "ov_test":
        z = np.load(staged("emb_ov_test.npz", STAGE_T0, folder))
    else:
        z = np.load(pinned_file(CS2 / DEV_EMB[0], DEV_EMB[1]))
    pos = {str(k): n for n, k in enumerate(z["keys"])}
    if any(f"{ds}|{i}" not in pos for i in ids):
        raise SystemExit(f"{ds}: the query vectors do not cover the set")
    return np.asarray(z["vecs"], np.float32)[[pos[f"{ds}|{i}"] for i in ids]]


def check_decode(a) -> int:
    """Refusals before anything is read: batch size 1; the token for OV-test and a listed backbone; the registered k,
    order and tail of the backbone's ret for ret, rand and perm (§4); registered draws; D1 on OV-dev-B ret only."""
    batch = batch_of(a)
    if a.set == "ov_test":
        admit(a.token, a.decision)
        ov_gate(a.model)
    if a.arm != "zs" and (a.k, a.order, a.tpl) != CFG[a.model]:
        raise SystemExit(f"REFUSED: {a.arm} of {a.model} uses k, order, tail {CFG[a.model]} (§4)")
    if a.draw not in {"perm": PERMS, "rand": DRAWS}.get(a.arm, (0,)):
        raise SystemExit(f"{a.arm}: draw {a.draw} is not registered")
    if a.redecode and (a.set, a.arm) != ("ov_dev_b", "ret"):
        raise SystemExit("REFUSED: D1 decodes the first 50 OV-dev-B ret items only (§9)")
    return batch


def cmd_decode(a) -> None:
    batch = check_decode(a)
    run_id = run_id_of(a)
    out = Path(a.out_dir) / f"{run_id}.preds.json"
    if out.exists():
        raise SystemExit(f"{out} exists; a run is decoded once")
    if a.dry_run and a.set == "ov_test":  # §6.5 dry run: the token and the backbone pass; no OV-test byte exists
        print(f"DRY {run_id}: token admitted for {a.model}; no OV-test byte in a dry run; stop before the lists")
        return
    import decode_hf_vlm as LB

    m = model_spec(a.model)
    if pins_open(m):
        raise SystemExit(f"{a.model}: pins open {pins_open(m)}; fill them from the authenticated tree API first")
    if a.dry_run:  # PI-1109g dry run: nothing is loaded
        print(f"DRY: snapshot check of {a.model} skipped")
    else:
        LB.check_snapshot(m, a.snapshot)
    items = items_of(a.set, a)
    ex = arm_ex(a.set, a.out_dir) if a.arm != "zs" else {}
    caps, shown = memory_text(a) if a.arm != "zs" else ({}, None)
    if a.redecode:  # D1: the first 50 items at batch size 1, stored (fwd50) or reversed (rev50) order
        items = items[:REDECODE_N][::-1 if a.redecode == "rev50" else 1]
    if a.limit:  # dry-run smoke: the first images only, never scored
        items = items[:a.limit]
    exids = {i: example_ids(a.arm, a.k, a.order, i, ex, a.draw) for i, _f, _h in items}
    zs_text = lb.prompt_text(lb.load_prereg(C.pinned(C.B_N1)), "short")
    texts = {i: zs_text if a.arm == "zs" else C.prompt(a.tpl, [shown(c) for c in exids[i]]) for i in exids}
    if a.arm != "zs" and {skeleton(t) for t in texts.values()} != {skeleton(C.prompt(a.tpl, []))}:
        raise SystemExit("A3: the prompt differs from the template outside the example block")  # §9 A3, STOP
    if a.dry_run:
        print(f"DRY {run_id}: {len(items)} items, examples and prompts built; stop before the model load")
        return
    import cen_decode as D  # N_NEW = 60 (§4), the value C-ATTR decoded with

    t0 = time.time()
    proc, net = LB.load(m, a.snapshot, "cuda:0")
    t1 = time.time()  # model load and decode seconds kept apart (§10.2: r_b excludes the load)
    folder = img_folder(a.set, a)
    g = LB.make_generate(proc, net, None, D.N_NEW, folder)
    log = out.with_name(f"t6_retry_{run_id}.jsonl")

    def gen(sl):
        call = lambda: g(sl, [texts[i] for i, _f, _h in sl])  # noqa: E731
        return t6([folder / f for _i, f, _h in sl], call, log) if a.set == "ov_test" else call()
    rows = LB.decode_slices(items, batch, gen, out.with_name(out.name + ".partial.jsonl"), run_id)
    timing = {"load_s": t1 - t0, "decode_s": time.time() - t1, "n": len(rows)}  # a resumed run under-counts decode_s
    rec = {"schema": SCHEMA, "label": LABEL[a.set], "run_id": run_id, "model": a.model, "dataset": a.set, "lang": "vi",
           "spec": {"arm": a.arm, "k": 0 if a.arm == "zs" else a.k, "order": a.order, "tpl": a.tpl, "draw": a.draw,
                    "memory": None if a.arm == "zs" else a.memory, "tau": TAU[a.model], "redecode": a.redecode,
                    "batch_size": batch},
           "hub_id": m["hub_id"], "revision": m["revision"], "c_conf_sha256": sha(Path(__file__)),
           "ex_sha256": sha(ATTR_LISTS if a.set == "ov_dev_b" else arm_lists_path(a.set, a.out_dir))
           if a.arm != "zs" else None, "exemplars": exids,
           "predictions": {r["image_id"]: r["caption"] for r in rows},
           "hit_max": {r["image_id"]: r["hit_max"] for r in rows}, "n_tokens": {r["image_id"]: r["n_tokens"] for r in rows},
           "prompt_sha256": {i: C.sha(t) for i, t in texts.items()}, "timing": timing, "utc": lb.utc()}
    out.write_text(json.dumps(rec, ensure_ascii=False) + "\n", encoding="utf-8")
    Path(str(out) + ".sha256").write_text(f"{sha(out)}  {out.name}\n")
    print(f"{run_id}: {len(rows)} images")


def cmd_lmcap(a) -> None:
    """LMCap re-implementation (no licence on the authors' code, so not run): M-CLIP xlm-roberta-large-ViT-H-14
    image-to-caption retrieval over the same memory (ri), the first 4 non-shot clusters of q's rand d0 list (rand), or
    the donor's retrieval (perm, p = 1); N = 3 fixed shots, XGLM-2.9B, beam 3, 3 candidates re-ranked by M-CLIP
    image-text similarity. Refusals and the dry run come before the GPU imports."""
    t0 = time.time()
    reg = registry()
    batch_of(a)
    if a.set == "ov_test":
        admit(a.token, a.decision)
        ov_gate()
    if a.redecode and (a.variant, a.set) != ("ri", "ov_dev_b"):
        raise SystemExit("REFUSED: LMCap D1 re-decodes lmcap_ri on the first 50 OV-dev-B items only (§9)")
    run_id = lmcap_run_id(a)
    out = Path(a.out_dir) / f"{run_id}.preds.json"
    if out.exists():
        raise SystemExit(f"{out} exists; a run is decoded once")
    if a.dry_run and a.set == "ov_test":
        print(f"DRY {run_id}: token admitted; no OV-test byte in a dry run; stop before the lists")
        return
    if a.dry_run:
        print("DRY: snapshot checks of xglm_2_9b and mclip_h14 skipped")
    else:
        for key, snap in (("xglm_2_9b", XGLM), ("mclip_h14", MCLIP)):
            lb.check_snapshot(reg["models"][key], snap)
    items = items_of(a.set, a)
    ex = arm_ex(a.set, a.out_dir)
    caps, shown = memory_text(a)
    sk, sv = mem_vectors()  # SigLIP2: C's near cut applies to LMCap's retrieval too
    ids = [i for i, _f, _h in items]
    scos = query_vectors(a.set, ids, ex) @ sv.T
    if sorted(sk) != sorted(caps):
        raise SystemExit("LMCap: the embedded memory is not the caption memory")
    shot_ids = lmcap_shots(a.set, sk, scos)  # the full set, no own-cluster masking (§5.1 (ii))
    if ex.get("shots", shot_ids) != shot_ids:
        raise SystemExit("LMCap: the shots differ from the list file's (§5.1 (ii))")
    own = ex.get("own", {})
    near = {i: {sk[j] for j in np.flatnonzero(row >= BM.NEAR_COS)} for row, i in zip(scos, ids)}
    if a.dry_run:
        print(f"DRY {run_id}: {len(items)} items, memory and lists checked; stop before the model load")
        return
    import open_clip
    import torch
    from PIL import Image
    from transformers import AutoTokenizer, XGLMForCausalLM

    mkeys = sorted(caps)
    clip, _p, pre = open_clip.create_model_and_transforms(
        "xlm-roberta-large-ViT-H-14", pretrained=str(MCLIP / "open_clip_pytorch_model.bin"))
    clip = clip.eval().half().cuda()
    tok = open_clip.get_tokenizer("xlm-roberta-large-ViT-H-14")

    def enc_text(texts):
        out = []
        for lo in range(0, len(texts), 256):
            with torch.no_grad():
                out.append(torch.nn.functional.normalize(clip.encode_text(tok(texts[lo:lo + 256]).cuda()).float(), dim=-1))
        return torch.cat(out)

    def enc_img(paths):
        with torch.no_grad():
            x = torch.stack([pre(Image.open(p).convert("RGB")) for p in paths]).half().cuda()
            return torch.nn.functional.normalize(clip.encode_image(x).float(), dim=-1)

    mtext = enc_text([shown(c) for c in mkeys])
    files = json.loads(MEM_FILES.read_text(encoding="utf-8"))  # {cid: [file, sha256]}
    for c in shot_ids:
        if sha(lb.DATA / "datasets" / files[c][0]) != files[c][1]:
            raise SystemExit(f"shot {c}: sha256 differs")
    shot_imgs = enc_img([lb.DATA / "datasets" / files[c][0] for c in shot_ids])

    def retrieve(v, skip: set[str]) -> list[str]:  # LMCap's ranking, the first K not skipped
        sc = (mtext @ v).cpu().numpy()
        return [mkeys[j] for j in np.lexsort((mkeys, -sc)) if mkeys[j] not in skip][:LMCAP_K]

    shots = [([shown(c) for c in retrieve(v, {s})], shown(s)) for s, v in zip(shot_ids, shot_imgs)]
    xt = AutoTokenizer.from_pretrained(XGLM)
    xm = XGLMForCausalLM.from_pretrained(XGLM, torch_dtype=torch.float16).eval().cuda()
    preds, exids, hitmax = {}, {}, {}
    file_of = {i: (f, h) for i, f, h in items}
    if a.redecode:  # D1: the first 50 items, stored (fwd50) or reversed (rev50) order
        items = items[:REDECODE_N][::-1 if a.redecode == "rev50" else 1]
    if a.limit:
        items = items[:a.limit]
    folder = img_folder(a.set, a)
    log = out.with_name(f"t6_retry_{run_id}.jsonl")

    def img_vec(i):
        f, h = file_of[i]
        if sha(folder / f) != h:
            raise SystemExit(f"{f}: sha256 differs from the manifest")
        call = lambda: enc_img([folder / f])[0]  # noqa: E731
        return t6([folder / f], call, log) if a.set == "ov_test" else call()
    perm_q = {}
    if a.variant == "perm":  # A2 (§9): the lmcap_perm lists are written and hashed before any decode
        for i, _f, _h in items:
            d = ex["donor"]["1"][i]
            perm_q[i] = retrieve(img_vec(d), lmcap_skip(d, shot_ids, near, own) | lmcap_skip(i, shot_ids, near, own))
        pl = Path(a.out_dir) / f"{run_id}.lists.json"
        pl.write_text(json.dumps({"label": LABEL[a.set], "perm_query_ids": perm_q}) + "\n", encoding="utf-8")
        Path(str(pl) + ".sha256").write_text(f"{sha(pl)}  {pl.name}\n")
        print(f"lmcap_perm lists {pl.name} sha256 {sha(pl)}", flush=True)
    t1 = time.time()  # load (models, memory text, shots, perm lists) and decode seconds kept apart
    for i, f, h in items:
        v = img_vec(i)
        q = perm_q[i] if a.variant == "perm" else lmcap_query(a.variant, i, ex, set(shot_ids),
                                                               retrieve(v, lmcap_skip(i, shot_ids, near, own)))
        exids[i] = q
        enc = xt(lmcap_prompt(shots, [shown(c) for c in q], "vi"), return_tensors="pt").to("cuda")
        with torch.no_grad():
            g = xm.generate(**enc, num_beams=LMCAP_BEAM, num_return_sequences=LMCAP_BEAM, max_new_tokens=LMCAP_NEW,
                            do_sample=False, eos_token_id=xt.eos_token_id)
        gen = [r[enc["input_ids"].shape[1]:].tolist() for r in g]
        cands = [xt.decode(r, skip_special_tokens=True).strip() for r in gen]
        best = int(torch.argmax(enc_text(cands) @ v))
        preds[i] = cands[best]
        hitmax[i] = xt.eos_token_id not in gen[best] and len(gen[best]) >= LMCAP_NEW  # N4
    timing = {"load_s": t1 - t0, "decode_s": time.time() - t1, "n": len(preds)}
    rec = {"schema": SCHEMA, "label": LABEL[a.set], "run_id": run_id, "model": "lmcap", "dataset": a.set, "lang": "vi",
           "spec": {"arm": "lmcap", "k": LMCAP_K, "n_shots": LMCAP_N, "beam": LMCAP_BEAM, "variant": a.variant,
                    "memory": a.memory, "redecode": a.redecode, "batch_size": 1},
           "c_conf_sha256": sha(Path(__file__)),
           "ex_sha256": sha(ATTR_LISTS if a.set == "ov_dev_b" else arm_lists_path(a.set, a.out_dir)),
           "exemplars": exids, "predictions": preds, "hit_max": hitmax, "shots": shot_ids, "timing": timing,
           "utc": lb.utc()}
    out.write_text(json.dumps(rec, ensure_ascii=False) + "\n", encoding="utf-8")
    Path(str(out) + ".sha256").write_text(f"{sha(out)}  {out.name}\n")


def lmcap_query(variant: str, qid: str, ex: dict, shots: set[str], retrieved: list[str]) -> list[str]:
    """The query block's K cluster ids. ri: LMCap's own M-CLIP retrieval (passed in); rand (lmcap_rand, a
    re-implementation of the LMCap recipe by this study): the first K clusters of q's rand draw-0 list that are not a
    shot cluster, no retrieved cluster kept (§2)."""
    if variant == "rand":
        return [c for c in ex["rand"]["0"][qid] if c not in shots][:LMCAP_K]
    return retrieved


# ------------------------------------------------------------------------------------------------ custody
MACHINE_ID = Path("/root/.vsps_machine_id")


def machine_id() -> str:
    try:
        return MACHINE_ID.read_text().strip().lower()
    except OSError:
        return ""


#: the only $NCS_DATA/datasets dirs the job may read, the other $NCS_DATA dirs it may read, the commands under the
#: open() audit hook, and the output dirs it may open
ISO_DATASETS = ("ktvic", "openviic", "c_t1_mem")
ISO_NCS = ("models", "vncorenlp", "c_conf_owners")
ISO_CMDS = ("decode", "lmcap", "compare", "stagecheck", "inputs")
ISO_OUT = ("c_conf_b0", "c_conf_r", "c_conf_t", "c_conf_b0_dry", "c_conf_r_dry", "c_conf_t_dry", "c_stage1",
           "c_stage2", "c_attr_b1")
ARCHIVES = (".zip", ".tar", ".tar.gz", ".tgz", ".7z")  # plus any ".tar.*" (N6)
RESTORED = ATTR / "STORED_SHA256"  # the stored runs and vectors of C and C-ATTR, pinned by their sidecars


def refused_names(clists: dict | None = None, f30k: dict | None = None, admitted: bool = False) -> set[str]:
    """§5.4: the XM-test2500 names and the Flickr30K test and val names, always; the OpenViIC test files (stage-1
    refusal minus the OV-dev-B carve-out) unless a token was admitted."""
    cl = clists or C.load_lists(CL)
    fl = f30k or load_lists()
    out = set(fl["refuse"]["test"]) | set(fl["refuse"]["val"]) | {r[1] for r in cl["sets"]["xm_test2500"]}
    return out if admitted else out | (set(cl["refuse"]["openviic_files"]) - {r[1] for r in cl["sets"]["ov_dev_b"]})


def iso_config(ncs: Path, outputs: Path, restored: list[str], refused: set[str], kt_pins: dict | None = None) -> dict:
    rp = os.path.realpath
    return {"ncs": rp(ncs), "outputs": rp(outputs), "refused": refused,
            "kt_images": rp(Path(ncs) / "datasets" / "ktvic" / "images"), "kt_pins": kt_pins or {},
            "ncs_ok": [rp(Path(ncs) / "datasets" / d) for d in ISO_DATASETS] + [rp(Path(ncs) / d) for d in ISO_NCS],
            "out_ok": [rp(Path(outputs) / d) for d in ISO_OUT],
            "files_ok": {rp(f) for f in restored}}


def iso_default(admitted: bool = False, kt_pins: dict | None = None) -> dict:
    files = [ln.split(maxsplit=1)[1] for ln in RESTORED.read_text().splitlines() if ln.strip()]
    return iso_config(lb.DATA, HOST / "outputs", files, refused_names(admitted=admitted), kt_pins)


def kt_pins_of_record() -> dict:
    """CC-466 W1: {name: sha256} of the pinned W2 list (c_conf_ktvic_owner_images.sha256), read by the guard only.
    Imported here, not at module level: c_conf_arms imports this module."""
    import c_conf_arms as AR
    return {n: h for h, n in (ln.split(maxsplit=1) for ln in
            AR.read_pinned(*AR.KT_HASHES).decode("utf-8").splitlines() if ln.strip())}


def kt_pinned(q: Path, cfg: dict | None) -> bool:
    """CC-466: a KTVIC training image whose base name equals a refused OpenViIC name passes the guard only as a
    regular file directly in $NCS_DATA/datasets/ktvic/images, under its own name, at its sha256 row of the pinned
    W2 list (c_conf_ktvic_owner_images.sha256). Everywhere else the name stays refused."""
    if not cfg or not cfg.get("kt_pins") or q.is_symlink() or not q.is_file():
        return False
    if os.path.dirname(os.path.realpath(q)) != cfg["kt_images"] or os.path.realpath(q) != os.path.abspath(q):
        return False
    want = cfg["kt_pins"].get(q.name)
    return want is not None and sha(q) == want


def is_archive(name: str) -> bool:
    return name.endswith(ARCHIVES) or ".tar." in name


def _under(p: str, root: str) -> bool:
    return p == root or p.startswith(root.rstrip("/") + "/")


def iso_denied(path, cfg: dict) -> str | None:
    """Why the job may not open this path (None = allowed). Symlinks are resolved first."""
    asked = os.fsdecode(path)
    p = os.path.realpath(asked)
    names = {os.path.basename(asked), os.path.basename(p)}  # CC-176 W2: the name as requested and as resolved
    if names & cfg["refused"]:
        return "a refused file name (§5.4)"
    if any(is_archive(n) for n in names):
        return "an archive"
    if _under(p, cfg["ncs"]) and not any(_under(p, r) for r in cfg["ncs_ok"]):
        return "outside the staged $NCS_DATA dirs"
    if _under(p, cfg["outputs"]) and p not in cfg["files_ok"] and not any(_under(p, r) for r in cfg["out_ok"]):
        return "outside the C-CONF output dirs and the restored files"
    return None


def iso_install(cfg: dict) -> None:
    """Every Python-level open() (builtins, io, os.open) of a denied path raises PermissionError. Ceiling: native-code
    opens (safetensors, tokenizers) and child processes are not seen; they only get model paths from the registry,
    and the guard scans those dirs."""
    def hook(event, args):
        if event == "open" and isinstance(args[0], (str, bytes, os.PathLike)):
            why = iso_denied(args[0], cfg)
            if why:
                raise PermissionError(f"C-CONF isolation: {os.fsdecode(args[0])}: {why}")
    sys.addaudithook(hook)


def guard_problems(roots: list[Path], refused: set[str], cfg: dict | None = None,
                   datasets: Path | None = None) -> list[str]:
    """No archive and no refused file name in the job's readable roots; no symlink that resolves to a denied path;
    $NCS_DATA/datasets holds only C-CONF's dirs."""
    bad = [str(datasets / n) for n in sorted(os.listdir(datasets)) if n not in ISO_DATASETS] if datasets else []
    for r in roots:
        for dirpath, dirs, files in os.walk(r):
            for n in dirs + files:
                q = Path(dirpath) / n
                if is_archive(n) or n.startswith("flickr30k-images") or (n in refused and not kt_pinned(q, cfg)):
                    bad.append(str(q))
                elif cfg and q.is_symlink() and iso_denied(q, cfg):
                    bad.append(f"{q} -> {os.path.realpath(q)}")
    return bad


def cmd_guard(a) -> None:
    bad = guard_problems([Path(x) for x in a.roots], refused_names(), iso_default(kt_pins=kt_pins_of_record()),
                         Path(a.datasets) if a.datasets else None)
    if bad:
        raise SystemExit(f"REFUSED: {len(bad)} forbidden paths, e.g. {bad[:3]}")
    print("guard ok")


def cmd_token(a) -> None:
    """G3 at preflight; --names-only (Q21): the OV-test inputs of §6.4a by name and pin only, none present yet."""
    t = admit(a.token, a.decision)
    if a.names_only:
        names = {**STAGE_T0, **STAGE_SCORE, PANEL[0]: PANEL[1]}
        bad = [n for n, h in names.items() if len(h) != 64 or (OV_STAGE / n).exists()]
        if OV_STAGE.exists() or bad:
            raise SystemExit(f"REFUSED: {len(bad)} §6.4a names unpinned or present, or {OV_STAGE} exists before T0")
        print(f"names ok: {len(names)} §6.4a files and images/<the 2,001 TSV names>, none on this host yet")
    print(f"token ok: backbones {' '.join(t['backbones'])}")


def cmd_stagecheck(a) -> None:
    """T0 (§6.4a, §6.5): the stage folder holds exactly the T0 files at their sha256 (the panel file optionally, for a
    count of T0) and images/ with every TSV name at its TSV sha256; the annotation and the first look's ledgers come
    at the scoring step only. A mismatch here is inside the look (the job records LOOK_STOP)."""
    admit(a.token, a.decision)
    ov_gate()
    if a.dry_run:
        print(f"DRY stagecheck: token admitted; {len(STAGE_T0)} files and images/ expected; nothing staged in a dry run")
        return
    d = Path(a.dir)
    if d.resolve() != OV_STAGE.resolve():
        raise SystemExit(f"REFUSED: the decoders read OV-test from {OV_STAGE}, not {d}")
    rows = ov_items(C.load_lists(CL))
    want = {**STAGE_T0, PANEL[0]: PANEL[1], **{f"images/{f}": h for _i, f, h in rows}}
    have = {str(p.relative_to(d)) for p in d.rglob("*") if p.is_file()}
    extra, missing = have - set(want), set(want) - {PANEL[0]} - have
    bad = [n for n in sorted(have & set(want)) if sha(d / n) != want[n]]
    print(f"stagecheck: {len(have)} files; {len(extra)} unexpected, {len(missing)} missing, {len(bad)} differ")
    if extra or missing or bad:
        raise SystemExit("STAGE CHECK FAIL (§6.4a): the staged OV-test files are not the files of record")


# ------------------------------------------------------------------------------------------------ score
def score_refs(ds: str, clists: dict, ids: list[str] | None = None) -> dict[str, list[str]]:
    """References: OV-dev-B by stage 2's reader; OV-test from the staged test annotation (sha256 of the first look's
    record), read as the first look read it (ctest.references_t); OV-carve from the pinned OpenViIC training
    annotation, captions as released."""
    if ds == "ov_dev_b":
        import stage2 as ST2
        return ST2.references2(ds, clists)
    if ds == "ov_test":
        names = [f for _i, f, _h in ov_items(clists)]
        d = json.loads(staged("uit-openviic-annotation-test.json", STAGE_SCORE).read_text(encoding="utf-8"))
        if set(d) != set(names):
            raise SystemExit("the staged OV-test annotation is not the 2,001 files")
        return {f: [c.strip() for c in d[f]["captions"]] for f in names}
    ann = json.loads(pinned_file(lb.DATA / OV_TRAIN_ANN[0], OV_TRAIN_ANN[1]).read_text(encoding="utf-8"))
    return {f: [c.strip() for c in ann[f]["captions"]] for f in ids}


def ledger_rows(runs: list[dict], ds: str, scored: str, ids: list[str], refs: dict, score) -> list[dict]:
    """One tau = -inf row per run on one scored set, ids sorted, stripped CIDEr-D per image with document
    frequencies over this scored set's references (§7.1). LMCap rows: model 'lmcap', arm lmcap_<variant>."""
    ids = sorted(ids)
    rows = []
    for r in runs:
        if not set(ids) <= set(r["predictions"]):
            raise SystemExit(f"{r['run_id']}: does not cover the {len(ids)} images of {scored}")
        s = np.asarray(score({i: r["predictions"][i] for i in ids}, {i: refs[i] for i in ids}), float)
        lm = r["model"] == "lmcap"
        rows.append({"run_id": r["run_id"], "dataset": ds, "scored_set": scored, "model": r["model"],
                     "arm": f"lmcap_{r['spec']['variant']}" if lm else r["spec"]["arm"],
                     "draw": None if lm else int(r["spec"]["draw"]), "tau": "-inf", "variant": None, "n": len(ids),
                     "cider_s": float(s.mean()), "per_image": {"ids": ids, "cider_s": s.tolist()},
                     "run_sha256": r["_sha256"]})
    return rows


def score_runs(a) -> list[dict]:
    """Refusals before any reference is read: OV-test needs the token; runs of this schema and set only; no D1 or
    dry-run file; every backbone run at tau = -inf (binding 10)."""
    if a.set == "ov_test":
        admit(a.token, getattr(a, "decision", None))
        ov_gate()
    if a.set not in ("ov_carve", "ov_test"):
        raise SystemExit(f"REFUSED: C-CONF scores OV-carve and OV-test only, not {a.set} (§7.1)")
    runs = [json.loads(Path(p).read_text(encoding="utf-8")) | {"_sha256": sha(p)} for p in a.runs]
    if any(r.get("schema") != SCHEMA or r.get("dataset") != a.set for r in runs):
        raise SystemExit("score: a run is not a C-CONF output of this set")
    if any(r["run_id"].endswith(SKIP_RUNS) for r in runs):
        raise SystemExit("score: D1 and dry-run files are never scored")
    if any(r["model"] != "lmcap" and r["spec"].get("tau") != TAU[r["model"]] for r in runs):
        raise SystemExit("score: a backbone run is not at tau = -inf (binding 10)")
    return runs


def cmd_score(a) -> None:
    """The ledger of one scored set (c_conf_score.score_runs): kit B through the scorer's kit_scorer, ids from the
    scorer's scored_sets (OV-test) or the runs themselves (OV-carve); written once (open 'x')."""
    runs = score_runs(a)
    if a.set == "ov_test":
        want = CS.scored_sets(ROOT)[a.scored_set]
        if isinstance(want, str):
            raise SystemExit(f"{a.scored_set}: {want}")
    else:
        want = sorted(runs[0]["predictions"]) if runs else []
        if a.scored_set != "ov_carve" or any(sorted(r["predictions"]) != want for r in runs):
            raise SystemExit("score: the OV-carve runs are not on one image set")
    rows = ledger_rows(runs, a.set, a.scored_set, want, score_refs(a.set, C.load_lists(CL), want), CS.kit_scorer(a.kit_b))
    stamp = {"label": LABEL[a.set], "c_conf_sha256": sha(Path(__file__)), "utc": lb.utc()}
    with open(a.ledger, "x", encoding="utf-8") as f:
        f.writelines(json.dumps({**r, **stamp}, ensure_ascii=False) + "\n" for r in rows)
    print(f"wrote {len(rows)} rows to {a.ledger}")


def differing(new: dict, old: dict, ids: list[str]) -> list[str]:
    """D1 (§9): ids whose captions are not identical strings (or missing). Never returns a caption."""
    return [i for i in ids if i not in new["predictions"] or new["predictions"][i] != old["predictions"].get(i)]


def cmd_compare(a) -> None:
    """rc 0 when the first 50 manifest items are identical strings, rc 3 otherwise; prints counts and ids only."""
    ids = [i for i, _f, _h in items_of(a.set, a)][:REDECODE_N]
    if a.dry_run:
        print(f"DRY compare {a.name}: {len(ids)} ids; rc 3")
        sys.exit(3)
    new = json.loads(Path(a.new).read_text(encoding="utf-8"))
    old = json.loads(Path(a.old).read_text(encoding="utf-8"))
    if a.d1 and (old.get("run_id") != d1_ref(new.get("run_id", ""))
                 or new["spec"]["batch_size"] != 1 or old["spec"]["batch_size"] != 1):
        raise SystemExit("REFUSED: D1 compares a forward batch-1 decode with this host's rev50 decode only")
    bad = differing(new, old, ids)
    rec = {"label": "D1 (C-CONF)", "check": a.name, "n": len(ids), "identical": len(ids) - len(bad),
           "failing_ids": bad, "new_sha256": sha(a.new), "old_sha256": sha(a.old), "utc": lb.utc()}
    Path(a.out).write_text(json.dumps(rec) + "\n", encoding="utf-8")
    print(f"{a.name}: {rec['identical']}/{rec['n']} identical; failing ids {bad}")
    sys.exit(3 if bad else 0)


def cmd_inputs(a) -> None:
    """Block-0 step 0.1: every input at its pin (paths and verdicts only); the table is c_conf_arms.block0_inputs."""
    import c_conf_arms as AR

    bad = 0
    for p, want in AR.block0_inputs().items():
        got = "missing" if not Path(p).is_file() else "ok" if sha(p) == want else "DIFFERS"
        bad += got != "ok"
        print(f"{got} {p}")
    if bad:
        raise SystemExit(f"G0: {bad} block-0 inputs missing or differing from their pins (§6.2 step 0.1)")
    print("inputs ok")


# ------------------------------------------------------------------------------------------------ CLI
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("decode", "lmcap"):
        p = sub.add_parser(name)
        p.add_argument("--set", choices=sorted(SETS), required=True)
        p.add_argument("--images", type=Path, default=lb.DATA / "datasets")
        p.add_argument("--out-dir", type=Path, required=True)
        p.add_argument("--c-lists", type=Path, default=CL)
        p.add_argument("--memory", choices=("vi",), default="vi")
        p.add_argument("--batch1", action="store_true", help="required: batch size 1 (binding 6)")
        p.add_argument("--token", type=Path)
        p.add_argument("--decision", type=Path, help=f"default: {DECISION_NAME} beside the token")
        p.add_argument("--redecode", choices=("rev50", "fwd50"), help="D1: first 50 OV-dev-B items, never scored")
        p.add_argument("--limit", type=int, default=0, help="dry-run smoke: first N images only, never scored")
        p.add_argument("--dry-run", action="store_true", help="stop before the model load")
        if name == "decode":
            p.add_argument("--model", choices=CS.BACKBONES, required=True)
            p.add_argument("--snapshot", type=Path, required=True)
            p.add_argument("--arm", choices=("zs", "ret", "rand", "perm"), required=True)
            p.add_argument("--k", type=int, default=0)
            p.add_argument("--order", choices=("first", "last"))
            p.add_argument("--tpl", choices=("T1", "T2"))
            p.add_argument("--draw", type=int, choices=sorted(set(DRAWS) | set(PERMS)), default=0)
        else:
            p.add_argument("--variant", choices=("ri", "rand", "perm"), required=True)
    p = sub.add_parser("compare")
    p.add_argument("--name", required=True)
    p.add_argument("--set", choices=("ov_dev_b",), required=True)
    p.add_argument("--new", type=Path, required=True)
    p.add_argument("--old", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--c-lists", type=Path, default=CL)
    p.add_argument("--d1", action="store_true", help="--old must be the D1 reference of --new (d1_ref)")
    p.add_argument("--dry-run", action="store_true")
    p = sub.add_parser("guard")
    p.add_argument("--roots", nargs="+", required=True)
    p.add_argument("--datasets", type=Path, help="$NCS_DATA/datasets may hold only C-CONF's staged dirs")
    for name in ("token", "stagecheck"):
        p = sub.add_parser(name)
        p.add_argument("--token", type=Path, required=True)
        p.add_argument("--decision", type=Path, help=f"default: {DECISION_NAME} beside the token")
        if name == "token":
            p.add_argument("--names-only", action="store_true", help="Q21: §6.4a OV-test inputs by name only")
        else:
            p.add_argument("--dir", type=Path, required=True)
            p.add_argument("--dry-run", action="store_true")
    p = sub.add_parser("inputs")
    p.add_argument("--block0", action="store_true", required=True)
    a = ap.parse_args()
    if a.cmd in ISO_CMDS and machine_id() in ("h1", "h2"):  # on a GPU host, always under the hook
        if getattr(a, "set", None) == "ov_test" or a.cmd == "stagecheck":
            admit(a.token, a.decision)
        iso_install(iso_default(admitted=ADMITTED is not None))
    {"decode": cmd_decode, "lmcap": cmd_lmcap, "compare": cmd_compare, "guard": cmd_guard, "token": cmd_token,
     "stagecheck": cmd_stagecheck, "inputs": cmd_inputs}[a.cmd](a)


if __name__ == "__main__":
    main()
