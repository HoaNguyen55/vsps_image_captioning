"""G3v (ERRATUM_O31_5 G-5; CODE_NEEDS C22): the registered tier-1 V-COCO probes on P-a.

P-a: one entity proposition per COCO-80 class that S0's G3 decode of UIT-ViIC test 231 mentions
(extract.entity_propositions, first-mention order), each asked with the §4.1 Q+ template (FAIR's
rescap.pipeline.verify.build_questions for an entity, unchanged) on the matched Vietnamese phrase (E-B5).
Vintern and InternVL3 tables through probe.probe_job, unchanged, as one job G3v with its own launch.json clock
(root/launch.json, shared by the two family folders), cap 1 h (G-5); G3v runs whatever K1 shows (G-5). A K4 stop
makes the registered tier-1 V-COCO row NOT RUN (CC-525r2 NB8). Question texts stay in the host tables; logs print
counts only.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from . import extract, probe, repo
from .verify import qkey

JOB = "G3v"
G3V_CAP_H = 1.0  # G-5: planned 0.12 GPU-hours, cap ceil(1.3 x 0.12) = 1 h
FAMILIES = ("vintern", "internvl3")
UIT_TEST_N = 231  # G-1: the registered UIT-ViIC test list


def q_plus(phrase: str) -> str:
    """§4.1 Q+ for an entity proposition whose subject is the matched phrase."""
    repo()
    from rescap.pipeline.verify import build_questions

    return build_questions({"type": "entity", "subject": {"text_vi": phrase}})[0]


def read_decode(preds_path: Path, items: list[tuple[str, str, str]]) -> dict:
    """S0's G3 decode: preds.json must equal its .sha256 sidecar and hold exactly the items' image ids."""
    preds_path = Path(preds_path)
    side = Path(str(preds_path) + ".sha256")
    line = side.read_text().split() if side.exists() else []
    if not line or line[0] != hashlib.sha256(preds_path.read_bytes()).hexdigest():
        raise SystemExit("REFUSED preds.json differs from its .sha256 sidecar")
    preds = json.loads(preds_path.read_text(encoding="utf-8"))
    if set(preds) != {iid for iid, _f, _h in items}:
        raise SystemExit("REFUSED the decode's image ids differ from the items list")
    return preds


def pa_work(preds: dict, items: list[tuple[str, str, str]]) -> tuple[list, list]:
    """(probe work list [(file, [(qkey, Q+)])] in file-name order, units [{image, image_id, classes}])."""
    work, units = [], []
    for iid, fname, _h in sorted(items, key=lambda it: it[1]):
        props = extract.entity_propositions(preds[iid])
        qs = [(qkey(q), q) for q in (q_plus(p["text_vi"]) for p in props)]
        if len({k for k, _q in qs}) != len(qs):
            raise SystemExit(f"FAULT two P-a propositions of {fname} share one question")
        work.append((fname, qs))
        units.append({"image": fname, "image_id": iid, "classes": [p["cls"] for p in props]})
    return work, units


def check_images(items: list[tuple[str, str, str]], folder: Path, allowed: set) -> None:
    """Every image's bytes equal the items sha, and every sha is a UIT-ViIC test image of exclusion.json."""
    for _iid, f, h in items:
        got = hashlib.sha256((Path(folder) / f).read_bytes()).hexdigest()
        if got != h or got not in allowed:
            raise SystemExit(f"FAULT {f} is not the registered UIT-ViIC test image the decode used")


def uit_test_shas() -> set:
    root = repo()
    ex = json.loads((root / "manuscript/prereg/2026-10-21_dev_pools/exclusion.json").read_text(encoding="utf-8"))
    return set(ex["image_sha256"]["uitviic_test"])


def clock(root: Path) -> float:
    """G3v's one launch clock: root/launch.json, copied into each family folder; any other clock is refused."""
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    lf = root / "launch.json"
    if lf.exists():
        rec = json.loads(lf.read_text())
        if rec.get("job") != JOB:
            raise SystemExit(f"REFUSED {lf} is the clock of job {rec.get('job')!r}, not {JOB}")
    else:
        rec = {"t0": time.time(), "job": JOB, "cap_h": G3V_CAP_H}
        lf.write_text(json.dumps(rec) + "\n")
    for f in FAMILIES:
        fl = root / f / "launch.json"
        if fl.exists():
            if json.loads(fl.read_text()).get("t0") != rec["t0"]:
                raise SystemExit(f"REFUSED {fl} holds a second launch clock")
        else:
            fl.parent.mkdir(parents=True, exist_ok=True)
            fl.write_text(json.dumps({"t0": rec["t0"], "family": f, "job": JOB}) + "\n")
    return rec["t0"]


def run_family(probe_fn, work: list, root: Path, family: str, load_image) -> int:
    """One family's pass inside G3v (G-5: whatever K1 shows). The cap is checked before the family starts and inside
    probe_job's pass; a cap stop is a K4 stop of G3v alone."""
    if family not in FAMILIES:
        raise SystemExit(f"REFUSED family {family!r}")
    t0 = clock(root)
    out = Path(root) / family
    if (time.time() - t0) / 3600 > G3V_CAP_H:
        return probe.halt(out, 4, f"CAP_STOP before {family}: G3v cap {G3V_CAP_H} h")
    return probe.probe_job(probe_fn, work, out, family, load_image, cap_h=G3V_CAP_H)


def status(root: Path) -> dict:
    """Per family DONE / NOT RUN (a STOP: K4 or a fault) / INCOMPLETE; the registered tier-1 V-COCO row is NOT RUN if
    either family stopped."""
    st = {}
    for f in FAMILIES:
        d = Path(root) / f
        st[f] = "NOT RUN" if (d / probe.STOP).exists() else "DONE" if (d / "probes.jsonl.sha256").exists() \
            else "INCOMPLETE"
    vals = set(st.values())
    st["row"] = "NOT RUN" if "NOT RUN" in vals else "DONE" if vals == {"DONE"} else "INCOMPLETE"
    return st
