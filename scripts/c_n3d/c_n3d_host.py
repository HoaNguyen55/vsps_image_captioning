"""C-N3D host side: pins (step 2), the custody check (step 2a) and the one run (step 4). Rented host only.

Layout: --root holds the PUSH LIST at its repository-relative paths (PUSH_LIST.sha256: the 62 data and list files of
COMPUTE v3 §2.1, then the CODE and RESOURCES of CLOSURE.sha256, erratum 1 E2); --data is $NCS_DATA with the pinned
reference, memory, Flickr30K and VnCoreNLP files. Every host entry point refuses unless VSPS_MACHINE_ID is set.
"""
from __future__ import annotations

import csv
import json
import os
import statistics
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

import c_n3d as N

HERE = Path(__file__).resolve().parent
PUSH = HERE / "PUSH_LIST.sha256"
ATTR_OUT = ".session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out"
C2_OUT = ".session_backup/machines/M3/root/outputs/c_stage2/runs"
T1_OUT = ".session_backup/machines/M1/root/outputs/c_t1/out"
LISTS = ("manuscript/prereg/2026-10-22_c_stage1/lists.json",
         "5c479f03e8be544f4cd12b5d997b5dc92b6c622df061760cd02f6ba82f6b4371")
OV_TSV = ("manuscript/prereg/2026-10-25_c_test/ov_test_files.tsv",
          "99d4fc49cc8283d1555d37b975cca5a32598ea0ec571d8bef8cf811df2c33695")
CARVE_ORDER = ("manuscript/prereg/2026-11-18_c_conf/c_conf_carve_order.json",
               "8e11bad51c77adc54c05b91a86f7b6f5a1f2d0e9032f06faf80f05e438d42850")
F30K_LISTS = ("manuscript/prereg/2026-10-30_c_t1/c_t1_f30k_lists.json",
              "eebcd95b78b1dc98398550b1f89fea5622e8cbd9f20ad6b07b0d9292ba745968")
ATTR_LISTS = "scripts/c_attr/c_attr_lists.json"
JAR = ("vncorenlp/VnCoreNLP-1.2.jar", "9e2811cdbc2ddfc71d04be5dc36e185c88dcd1ad4d5d69e4ff2e1369dccf7793")
F30K_CSV = ("data/flickr30k/flickr_annotations_30k.csv",
            "395990db603ab8bafd5c7ab2746b22058bb1e75b78b3eb56ad755931364ac137")       # erratum 1 E4
DATA_PINS = {  # $NCS_DATA-relative (prereg v3 §4; erratum 1 E1, E4); every one checked at step 2 [CC-511 W2]
    "datasets/openviic/uit-openviic-annotation-dev.json":
        "550cfe06b06084976e81286531f7f4e52bea717e29004c699ccaf1e48919bdff",
    "datasets/c_xm_dev500/xm_dev500_data.json": "0da82355b65ab284fe55fc0d3c4101090301767347a02721890556618ca4905f",
    "datasets/ktvic/train_data.json": "72ee9b57c350fb5f215e1f04701c515a51e5e415240e51a77c8ce00ce6316a0f",
    "datasets/openviic/uit-openviic-annotation-train.json":
        "d757520e76b8490df6c7275c2beb8b3ecef0342635a436bea8c3cfd07eb49df0",
    F30K_CSV[0]: F30K_CSV[1],
    JAR[0]: JAR[1],
}
OIV7 = {"labels": ("data/xm3600/oiv7_labels.json", "bac3953a511a9793c22e928a29b68ae05dbf9654502abcbe7b64fd9f6d74c8b2"),
        "desc": ("data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv",
                 "84a4373a0efb7fd6d93fe19b0e7ceb6c1b855c233d13b9b78a9a33655c9fdce3")}
SRC = {"ov_dev_b": "openviic", "xm_dev500": "xm3600"}
WALL_CAP_H = 4.0   # COMPUTE v3 §1 "4.0 CPU-h wall"; host_selftest.sh also kills at 4 h [CC-511 W4]
SR3_LABEL = "A1 not met; batched decode; descriptive; zero-shot reference = the batched stage-2 zs caption (erratum 1 E6)"
SEARCH = (".", "scripts", "scripts/lb", "scripts/c_attr", "scripts/c_stage1", "scripts/c_stage2", "scripts/c_en",
          "scripts/kit_b")   # probe.py and closure.py use the same order


def host_only() -> None:
    if not os.environ.get("VSPS_MACHINE_ID"):
        raise SystemExit("REFUSED: host steps run on the rented host only (VSPS_MACHINE_ID unset)")


def paths(root: Path) -> None:
    for p in SEARCH:
        sys.path.insert(0, str(root / p))


class Clock:
    """Wall clock from the start of the run; a STOP past the cap (the 4 h kill in host_selftest.sh is the backstop)."""

    def __init__(self, cap_h: float = WALL_CAP_H, now=time.monotonic):
        self.now, self.t0, self.cap = now, now(), cap_h * 3600

    def check(self, where: str) -> float:
        h = (self.now() - self.t0) / 3600
        if h * 3600 > self.cap:
            raise SystemExit(f"STOP: the 4.0 h wall cap passed at {where}")
        return h


# ------------------------------------------------------------------------------------------------ step 2 + 2a
def pinned_json(root: Path, rel_sha: tuple[str, str]):
    return json.loads(N.read_pinned(root / rel_sha[0], rel_sha[1]))


def data_pins(data: Path) -> dict:
    """Every $NCS_DATA pin, the jar included; the segmenter model files are recorded (CC-511 W2)."""
    bad = [r for r, h in DATA_PINS.items() if not (data / r).is_file() or N.sha(data / r) != h]
    if bad:
        raise SystemExit(f"STOP: $NCS_DATA pins missing or not as pinned: {bad}")
    seg = data / "vncorenlp/models/wordsegmenter"
    return {"data_pins": "ok", "segmenter_models": {p.name: N.sha(p) for p in sorted(seg.iterdir()) if p.is_file()}}


def jar_constant(root: Path) -> None:
    """The stage-1 scorer's own jar constant equals the registered jar pin."""
    paths(root)
    import score as S
    if S.JAR_SHA256 != JAR[1]:
        raise SystemExit("STOP: score.JAR_SHA256 is not the registered VnCoreNLP-1.2 jar pin")


def custody(root: Path, data: Path) -> dict:
    """Step 2 (PUSH LIST and every $NCS_DATA pin), then 2a (R2 intersections, counts only)."""
    host_only()
    N.check_push(root, N.push_list(PUSH))
    rec = data_pins(data)
    jar_constant(root)
    lists = pinned_json(root, LISTS)
    tsv = N.read_pinned(root / OV_TSV[0], OV_TSV[1]).decode("utf-8")
    counts = N.custody_counts(lists, tsv, pinned_json(root, CARVE_ORDER), pinned_json(root, F30K_LISTS))
    print(json.dumps({"custody_counts": counts, **rec}, sort_keys=True))
    N.custody_gate(counts)
    print("custody: all counts 0")
    return {"custody_counts": counts, **rec}


def module_pin_check(root: Path, push: Path = PUSH) -> int:
    """Every loaded module file under --root is on the PUSH LIST with an equal sha256 (erratum 1 E2)."""
    pins, rootr = N.push_list(push), str(root.resolve())
    files = {str(Path(m.__file__).resolve()) for m in list(sys.modules.values()) if getattr(m, "__file__", None)}
    bad = []
    for f in sorted(x for x in files if x.startswith(rootr + os.sep)):
        rel = os.path.relpath(f, rootr)
        if pins.get(rel) != N.sha(Path(f)):
            bad.append(rel)
    if bad:
        raise SystemExit(f"STOP: {len(bad)} loaded modules not on the PUSH LIST as pinned, e.g. {bad[:3]}")
    return len([x for x in files if x.startswith(rootr + os.sep)])


# ------------------------------------------------------------------------------------------------ loaders and wiring
def load_run(p: Path) -> dict:
    r = json.loads(p.read_text(encoding="utf-8"))
    r["_sha256"] = N.sha(p)
    return r


def arm_of(name: str) -> str | None:
    """Arm of a batch-1 file name; perm and re-decode files are never matched (hash-only, never pushed)."""
    if "-perm-" in name or "fwd50" in name or not name.endswith("-b1.preds.json"):
        return None
    if "-zs-" in name:
        return "zs"
    if "-ret-" in name:
        return "ret"
    return next((f"rand_d{d}" for d in range(3) if "-rand-" in name and f"-d{d}-" in name), None)


def b1_runs(root: Path, m: str, s: str) -> dict[str, dict]:
    out = {}
    for p in sorted((root / ATTR_OUT).glob(f"at_{m}_{s}-*.preds.json")):
        arm = arm_of(p.name)
        if arm is None:
            continue
        if arm in out:
            raise SystemExit(f"STOP: duplicate batch-1 arm {arm} ({m} {s})")
        out[arm] = load_run(p)
    if set(out) != {"zs", "ret", "rand_d0", "rand_d1", "rand_d2"}:
        raise SystemExit(f"STOP: {m} {s}: arms {sorted(out)}")
    return out


def check_exemplars(runs: dict, ex: dict, A) -> None:
    """The shown lists the runs carry equal the pinned c_attr_lists.json rule (A.example_ids)."""
    for arm, r in runs.items():
        if arm == "zs":
            continue
        sp, d = r["spec"], int(arm[-1]) if arm.startswith("rand") else 0
        bad = sum(r["exemplars"][q] != A.example_ids(sp["arm"], sp["k"], sp.get("order"), q, ex, d) for q in r["predictions"])
        if bad:
            raise SystemExit(f"STOP: {r['run_id']}: {bad} shown lists differ from c_attr_lists.json")


def status_fn(key, gold: set, verified: dict | None, tally: dict | None):
    """'present' / 'absent' of a class: the verified OIV7 status where it decides (XM-dev500), else the reference
    union. tally counts class decisions of the primary flag pass only (N1); None for recomputations."""
    def st(o: str) -> str:
        v = None if verified is None else verified.get(o, verified.get(key(o)))
        how = "verified" if v in ("present", "absent") else "reference"
        if tally is not None:
            tally[how] += 1
        if how == "verified":
            return v
        return "present" if key(o) in gold else "absent"
    return st


def flag_arrays(inst, ids, runs, zs, shown, statuses, med, ln_rel=N.LN_REL) -> dict[str, dict]:
    """Flags of every arm: its own shown list (shown(run, id)), the same backbone's zs caption."""
    out = {}
    for arm, r in runs.items():
        fl = [N.flags_of(inst, r["predictions"][i], zs["predictions"][i], shown(r, i), statuses[i], med[i], ln_rel)
              for i in ids]
        out[arm] = {f: np.array([x[f] for x in fl]) for f in N.FLAGS}
    return out


def cell_of(sc: dict, fl: dict, rand: str = "d0") -> N.Cell:
    """d = ret - rand d0 (or the R = 3 mean, SR1); e = rand d1 - rand d2; f_d1 from rand d1 (prereg §5)."""
    base = sc["rand_d0"] if rand == "d0" else np.mean([sc[f"rand_d{d}"] for d in range(3)], 0)
    return N.Cell(d=sc["ret"] - base, e=sc["rand_d1"] - sc["rand_d2"], f_ret=fl["ret"], f_d0=fl["rand_d0"],
                  f_d1=fl["rand_d1"], f_d2=fl["rand_d2"])


def family_rows(analyses: dict) -> list[dict]:
    """The six primary rows: OV-dev-B, Qwen2.5-VL-7B then InternVL3-8B, H1-H3 each (prereg §6)."""
    rows = []
    for m in N.FAMILY_MODELS:
        a = analyses[("ov_dev_b", m)]
        rows += [N.h_row(h, a["_pt"], a["_boot"]) | {"model": m, "set": "ov_dev_b"} for h in ("H1", "H2", "H3")]
    return rows


def parity(key, value: float, table: dict, what: str) -> None:
    """E5 gate: prints the cell only, never a value (CC-511 N2)."""
    if abs(value - table[key]) > N.PARITY_TOL:
        raise SystemExit(f"STOP: parity {what} {key[0]} {key[1]}")


def t8_length(inst, runs: dict, ids: list, fl: dict) -> dict:
    """SR5: T8's rule |len(treatment) - len(comparison)| / len(comparison) > 0.10 as the LN flag."""
    ln = {a: np.array([inst.length(r["predictions"][i]) for i in ids], float) for a, r in runs.items()}

    def rel(a, b):
        return np.abs(ln[a] - ln[b]) / np.maximum(ln[b], 1) > 0.10
    out = {a: dict(v) for a, v in fl.items()}
    out["ret"]["LN"], out["rand_d0"]["LN"] = rel("ret", "rand_d0"), rel("rand_d0", "ret")
    out["rand_d1"]["LN"], out["rand_d2"]["LN"] = rel("rand_d1", "rand_d2"), rel("rand_d2", "rand_d1")
    return out


def flagged(rows: dict, s: str, m: str) -> dict:
    """CC-511 N4: every Aya-Vision OV-dev-B row carries the placebo flag."""
    return {**rows, "flag": N.AYA_FLAG} if (s, m) == ("ov_dev_b", "aya_vision_8b") else rows


# ------------------------------------------------------------------------------------------------ Vietnamese cells
def vi_cells(root: Path, data: Path, clock: Clock) -> tuple[dict, dict, dict]:
    import c_attr as A
    import c_attr_score as CS
    import decode_icl as C
    import stage2 as ST2
    import xm3600_oiv7 as XO
    from rescap import chair as CH

    module_pin_check(root)
    clists = pinned_json(root, LISTS)
    exs = json.loads((root / ATTR_LISTS).read_text(encoding="utf-8"))["sets"]
    caps = C.memory_captions(clists, data)
    score = CS.kit_scorer(CS.KIT)
    inst = N.vi_instruments()
    vmap = XO.resolve_map(root / OIV7["desc"][0])
    labels = json.loads(N.read_pinned(root / OIV7["labels"][0], OIV7["labels"][1]))
    xm_test = {r[0] for r in clists["sets"]["xm_test2500"]}
    cells, sr3, meta = {}, {}, {"gold_decided_class_level": {}}
    for s in ("ov_dev_b", "xm_dev500"):
        refs = ST2.references2(s, clists, data)
        ids = sorted(refs)
        if len(ids) != N.SET_N[s]:
            raise SystemExit(f"STOP: {s} reference keys are not the set")
        N.row_guard(ids, xm_test, "XM-test2500")
        verified = XO.statuses(vmap, {i: labels[i] for i in ids if i in labels}) if s == "xm_dev500" else None
        gold = {i: CH._gold_objects(refs[i]) for i in ids}
        med = {i: statistics.median(inst.length(x) for x in refs[i]) for i in ids}
        tally = {"verified": 0, "reference": 0}

        def statuses(t, gold=gold, verified=verified):
            return {i: status_fn(inst.key, gold[i], None if verified is None else verified.get(i, {}), t) for i in ids}

        def shown(r, i, s=s):
            return [C.shown(caps[x], SRC[s]) for x in r["exemplars"][i]]
        for m in N.MODELS:
            runs = b1_runs(root, m, s)
            if any(sorted(r["predictions"]) != ids for r in runs.values()):
                raise SystemExit(f"STOP: {m} {s}: run ids are not the set")
            check_exemplars(runs, exs[s], A)
            sc = {a: score({i: r["predictions"][i] for i in ids}, refs) for a, r in runs.items()}
            parity((s, m), float(np.mean(sc["ret"] - np.mean([sc[f"rand_d{d}"] for d in range(3)], 0))),
                   N.PARITY, "tau_sel b1")
            cells[(s, m)] = {"sc": sc, "fl": flag_arrays(inst, ids, runs, runs["zs"], shown, statuses(tally), med),
                             "runs": runs, "ids": ids, "med": med, "statuses": statuses, "shown": shown}
            clock.check(f"flags {s} {m}")
        n = tally["verified"] + tally["reference"]
        meta["gold_decided_class_level"][s] = {**tally, "share_verified": tally["verified"] / n if n else None}
        sr3.update(stage2_cells(root, s, ids, refs, score, inst, shown, statuses(None), med))
    return cells, sr3, meta


def stage2_cells(root, s, ids, refs, score, inst, shown, stt, med) -> dict:
    """SR3: stored batched stage-2 zs / ret / rand d0 (Qwen2.5-VL, InternVL3 as written); a parity miss makes the
    cell NOT RUN instead of stopping the primary rows (CC-511 N3)."""
    import decode_icl as C
    ex = json.loads((root / f".session_backup/machines/M3/root/outputs/c_stage2/ex_{s}.json").read_text(encoding="utf-8"))
    out = {}
    for m in N.FAMILY_MODELS:
        runs = {}
        for p in sorted((root / C2_OUT).glob(f"c2_{m}_{s}-*.preds.json")):
            arm = next((a for a in ("zs", "ret", "rand") if f"-{a}" in p.name), None)
            if arm and "-blind-" not in p.name and "-fix-" not in p.name:
                runs[arm] = load_run(p)
        if set(runs) != {"zs", "ret", "rand"}:
            raise SystemExit(f"STOP: SR3 {m} {s}: arms {sorted(runs)}")
        for r in runs.values():
            if "exemplars" not in r and r["spec"]["arm"] != "zs":
                r["exemplars"] = {q: C.exemplar_ids({**r["spec"], "dataset": s}, q, ex) for q in ids}
        sc = {a: score({i: r["predictions"][i] for i in ids}, refs) for a, r in runs.items()}
        try:
            parity((s, m), float(np.mean(sc["ret"] - sc["rand"])), N.PARITY_SR3, "SR3 stage-2 d0")
        except SystemExit as e:
            out[(s, m)] = f"NOT RUN (parity): {e}"
            continue
        fl = flag_arrays(inst, ids, {"ret": runs["ret"], "rand_d0": runs["rand"]}, runs["zs"], shown, stt, med)
        out[(s, m)] = N.Cell(d=sc["ret"] - sc["rand"], e=None, f_ret=fl["ret"], f_d0=fl["rand_d0"], f_d1=None, f_d2=None)
    return out


# ------------------------------------------------------------------------------------------------ English (carve)
def en_flags(inst, runs: dict, ids: list, gold: dict, med: dict) -> dict:
    """ZL and LN only (erratum 1 E3): no copy statistic and no shown list; BO and CP are placeholders printed as
    NOT RUN by english_public, never as numbers."""
    out = {}
    for a in ("ret", "rand_d0"):
        rows = [N.flags_zl_ln(inst, runs[a]["predictions"][i], runs["zs"]["predictions"][i],
                              lambda o, i=i: "present" if inst.key(o) in gold[i] else "absent", med[i]) for i in ids]
        z = np.zeros(len(ids), bool)
        out[a] = {"BO": z, "CP": z, "ZL": np.array([x["ZL"] for x in rows]), "LN": np.array([x["LN"] for x in rows])}
    return out


def en_cells(root: Path, data: Path) -> dict:
    import cen_score as CE
    f30k = pinned_json(root, F30K_LISTS)
    keep, refused = set(f30k["carve"]), set(f30k["refuse"]["val"]) | set(f30k["refuse"]["test"])
    refs = {}
    with open(data / F30K_CSV[0], newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["split"] == "train" and r["filename"] in keep:   # R1: no other row is parsed into a row
                refs[r["filename"]] = json.loads(r["raw"])
    ids = sorted(refs)
    if len(ids) != N.SET_N["f30k_carve"]:
        raise SystemExit("STOP: carve references are not the 1,000 carve images")
    N.row_guard(ids, refused, "Flickr30K val/test")
    tokenize, cider = CE.ptb_cider()
    gts = tokenize({i: refs[i] for i in ids})
    inst = N.en_instruments()
    gold = {i: set().union(*(set(inst.classes(x)) for x in refs[i])) for i in ids}
    med = {i: statistics.median(inst.length(x) for x in refs[i]) for i in ids}
    out = {}
    for m in N.MODELS:
        runs = {}
        for p in sorted((root / T1_OUT).glob(f"t1_{m}_f30k_carve-*.preds.json")):
            n = p.name
            if "ret_img" in n or "-mf30k" in n:
                continue
            arm = "zs" if n.endswith("-zs.preds.json") else "ret" if "-ret-" in n else "rand_d0" if "-d0-" in n else None
            if arm:
                runs[arm] = load_run(p)
        if set(runs) != {"zs", "ret", "rand_d0"}:
            raise SystemExit(f"STOP: English {m}: arms {sorted(runs)}")
        sc = {}
        for a, r in runs.items():
            if sorted(r["predictions"]) != ids:
                raise SystemExit(f"STOP: {r['run_id']}: not the carve")
            res = tokenize({i: [r["predictions"][i]] for i in ids})
            sc[a] = np.asarray(cider(gts, {i: res[i] for i in ids}), float)
        parity(("f30k_carve", m), float(np.mean(sc["ret"] - sc["rand_d0"])), N.PARITY, "English carve d0")
        fl = en_flags(inst, runs, ids, gold, med)
        out[m] = N.Cell(d=sc["ret"] - sc["rand_d0"], e=None, f_ret=fl["ret"], f_d0=fl["rand_d0"], f_d1=None, f_d2=None)
    return out


# ------------------------------------------------------------------------------------------------ step 4
def run(root: Path, data: Path, out: Path) -> None:
    host_only()
    if out.exists():
        raise SystemExit(f"REFUSED: {out} exists; the run is made once")
    clock, t_cpu = Clock(), time.process_time()
    rec0 = custody(root, data)
    st = subprocess.run([sys.executable, "-I", "-B", str(HERE / "test_c_n3d.py")], capture_output=True, text=True)
    if st.returncode:
        raise SystemExit(f"STOP: selftests or mutants failed\n{st.stdout[-2000:]}{st.stderr[-2000:]}")
    paths(root)
    os.environ["NCS_DATA"] = str(data)
    idx = N.index_matrices()
    cells, sr3, meta = vi_cells(root, data, clock)
    analyses, rows, sens = {}, {}, {}
    for (s, m), c in cells.items():
        a = analyses[(s, m)] = N.analyse(cell_of(c["sc"], c["fl"]), idx[s])
        rows[f"{s}|{m}"] = flagged(N.public(a), s, m)
        if s != "ov_dev_b" or m not in N.FAMILY_MODELS:
            if a["decidable"]:
                rows[f"{s}|{m}"]["h_rows_no_rule"] = [N.h_row(h, a["_pt"], a["_boot"]) for h in ("H1", "H2", "H3")]
        inst = N.vi_instruments()
        sv = {"SR1_rand_mean_d0_d2": N.analyse(cell_of(c["sc"], c["fl"], rand="mean"), idx[s]),
              "SR2_M5": N.analyse(cell_of(c["sc"], c["fl"]), idx[s], m=5.0),
              "SR2_M15": N.analyse(cell_of(c["sc"], c["fl"]), idx[s], m=15.0),
              "SR5_T8_length": N.analyse(cell_of(c["sc"], t8_length(inst, c["runs"], c["ids"], c["fl"])), idx[s]),
              "SR6_reversed_precedence": N.analyse(cell_of(c["sc"], c["fl"]), idx[s], prec=N.PREC_REV)}
        for rel in (0.10, 0.40):
            fl = flag_arrays(inst, c["ids"], c["runs"], c["runs"]["zs"], c["shown"], c["statuses"](None), c["med"], rel)
            sv[f"SR4_LN_{rel:.2f}"] = N.analyse(cell_of(c["sc"], fl), idx[s])
        sens[f"{s}|{m}"] = {k: flagged(N.public(v), s, m) for k, v in sv.items()}
        clock.check(f"sensitivity {s} {m}")
    verdicts = N.family_verdicts(family_rows(analyses))
    for (s, m), c in sr3.items():
        sens[f"{s}|{m}"]["SR3_stored_batched"] = c if isinstance(c, str) else \
            N.public(N.analyse(c, idx[s])) | {"label": SR3_LABEL}
    clock.check("SR3")
    en = {m: N.english_public(N.analyse(c, idx["f30k_carve"])) for m, c in en_cells(root, data).items()}
    wall_h = clock.check("English")
    n_mod = module_pin_check(root)
    rec = {"label": N.LABEL, "set_note_ov_dev_b": N.H_NOTE, **rec0, "parity": "ok", "family": verdicts,
           "rows": rows, "sensitivity": sens, "english": en, **meta, "modules_checked": n_mod,
           "inputs": N.push_list(PUSH), "data_pins": DATA_PINS,
           "code": {p.name: N.sha(p) for p in sorted(HERE.glob("*.py"))}, "seed": N.SEED, "B": N.B,
           "cpu_h_parent": (time.process_time() - t_cpu) / 3600, "wall_h": wall_h,
           "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    tmp = out.with_name(out.name + ".partial")
    tmp.write_text(json.dumps(rec, ensure_ascii=False, indent=1, default=float) + "\n", encoding="utf-8")
    os.replace(tmp, out)
    print(f"wrote {out.name} sha256 {N.sha(out)}")
