#!/usr/bin/env python3
"""G-RL pilot: the trainer config (every pinned value), the M3/M4 host guard, the test-image refusal and the pinned id
lists and gold. Rule: manuscript/prereg/2026-10-27_grl_pilot/PILOT_RULE.md.

    python3 scripts/grl/common.py --selftest        CPU, synthetic files only

The data this pilot may read: UIT-ViIC train (the 2,402 Gate-1 ids) and val (924), and COCO-2014 instance labels of those
ids (as gold_instances.json). Nothing here opens a test split.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PDIR = ROOT / "manuscript/prereg/2026-10-27_grl_pilot"
NCS_DATA = Path(os.environ.get("NCS_DATA", "/root/ncs-data"))
UV = NCS_DATA / "datasets" / "uitviic"  # staged: images/, train_data.json (UT-2402 only), val_data.json
OUT = Path(os.environ.get("GRL_OUT", "/root/outputs/grl_pilot"))
#: every place setup_gpu.sh checks for images, plus the data root (PI-1026r: M3 holds no test images)
SCAN_ROOTS = (Path("/root/outputs"), Path("/root/queue"), NCS_DATA, Path("/root/vsps"))
MACHINES = ("m3", "m4")  # PI-1026r: the pilot runs on M3; CC-118 r3 named M4
#: C-EN on M3 (scripts/c_en/cen_fetch.py REC_DIR / STAGE_DIR; CC-119 W6, CC-120, CC-121): C-EN has priority
CEN_REC = Path("/root/outputs/c_en/fetch")
CEN_TEST_SIDE = ("coco_test", "coco_kval", "nocaps_val")
LOCK = Path("/root/outputs/grl_pilot/RUNNING")  # held by gate0.sh, gate1.sh and k2_gate0.sh for a whole run

# ------------------------------------------------------------------------------------------------ pins
PINS = {  # repo path -> sha256; checked by pinned()
    "manuscript/prereg/2026-10-21_dev_pools/exclusion.json":
        "c52a96d18925b974878ae1a970c3f9133fb3482216676fd41871eeabb68cc77f",
    "manuscript/prereg/2026-10-21_dev_pools/uitviic_val.tsv":
        "338252e13c7cc8e51c579ea7f0a81f96919bb1aebe499ce90a8e7c370742e5a4",
    "manuscript/prereg/2026-10-27_grl_pilot/ut2402.txt": "3969bfd448de7cf9e5749c40d510e25221fbc6783a4b8961b33ad5a53824ac5c",
    "manuscript/prereg/2026-10-27_grl_pilot/val924.txt": "92bb37947a12eb26189381f8ef55bf382b5356fad847ffa904250bd17e675559",
    "manuscript/prereg/2026-10-27_grl_pilot/kv5000.txt": "b7a7a89dd86f75f60dc1984613bde9048118c37bc5246e028c7b22aeb4199477",
    "manuscript/prereg/2026-10-27_grl_pilot/gold_instances.json": "42c100f5ca814698f0df60366b1c0f437e6487db0f9da1d13032dbf14303aa84",
    "data/coco_probe/coco80_vi.json": "926e08571ef6e80a7f8aae8f2b73753d6c5c54c431a750ba2b67bfaae71b540b",
    "scripts/score_coco_probe.py": "d11db7e192f689980bb2b2bb717d852d9aa339ad857ce9411fe7bdd6fe416070",
    "scripts/rl_policy.py": "7644e5676064c4495462a60d3dabc4c62933d019bcc201492120f2d9e6b51b56",  # = rl_gate_v2 pin
    "scripts/rl_reward.py": "3b18b7a3620c2511d4d13caea62f204534783e3024cac188da78d957e6a0a74b",  # = rl_gate_v2 pin
    "scripts/evaluate.py": "a68d56826d90d8a409493cd6f49007e906c6cb4f5668314edb9b8e7a632e8236",  # = rl_gate_v2 pin
    "scripts/train_stage2.py": "29312ef765e3e49e5e1efefc5ad8b88fcf33c991b1a5f3a266a910ada3d1cab4",
    "scripts/clean_supervision.py": "01f172002a607ba9ee55bccb332439f10650832cae1f64a9b74b35c48cd9c231",
    "rescap/chair.py": "e47d249ac7290070f2387d3fa8b22dac77728265ad276f55aa6520f5cbc591a3",
}
#: /root/vsps/.venv on M3 (setup_gpu.sh H_VS): torch 2.5.1+cu121, transformers 4.51.3, peft 0.21.2, bitsandbytes 0.50.2
VENV_FREEZE_SHA256 = "7332d343173e5681365cf6871671e36209c77803a1b2db70da1cc766d5c943ed"
MODELS = {  # size -> (hub id, revision, evaluate.py --model, licence)
    "7b": ("Qwen/Qwen2.5-VL-7B-Instruct", "cc594898137f460bfe9f0759e9844b3ce807cfb5", "qwen2.5-vl-7b", "Apache-2.0"),
    "3b": ("Qwen/Qwen2.5-VL-3B-Instruct", "66285546d2b821cf421d4f5eb2576359d3770cd3", "qwen2.5-vl-3b", "qwen-research"),
}
PROMPT_MODE = "detailed"  # evaluate.py PROMPTS["detailed"], every arm, sampling and decoding

# ------------------------------------------------------------------------------------------------ trainer config
CFG = {
    "seed": 0,  # pilot seed; LoRA init, schedule and sampling; not a confirmatory seed
    "lora_r": 16, "lora_alpha": 32,  # train_stage2 defaults; language tower only; 4-bit NF4 double-quant base
    "vision_tokens": 512,  # build_model's 4-bit budget (vision_tokens=0)
    "k": 8, "temperature": 1.0, "max_new_tokens": 160,  # 160 = evaluate.py's decode cap
    "images_per_step": 5, "rl_lr": 2e-5, "beta": 0.03, "micro": 1,  # CN-RLOO v3 values; micro 1 x 160 tokens
    "sft_lr": 1e-4, "sft_examples_per_step": 8, "sft_epochs": 2,  # P1 recipe values (lr, effective batch, epochs)
    "window": (0.75, 1.25),  # x median syllables of the base model's step-0 samples on train
    "repeat_ngram": 5, "repeat_max": 2,  # a word 5-gram seen 3+ times = degenerate loop
}
GATE0 = {"steps": 30, "peak_gb_stop": 23.5, "switch_7b_grl_gpuh": 35.0, "stop_3b_grl_gpuh": 25.0,  # CC-124 W6
         "cap_factor": 1.2, "pi_above_gpuh": 40.0, "greedy_images": 40, "logp_gap_max": 0.02,
         "finished_min": 0.90}  # base samples finished within 160 tokens, else TO-PI (the cap truncates the window)
GATE1 = {"sesoi_f1": 2.0, "margin_p": -1.0, "boot_b": 2000, "boot_seed": 0, "vi_drop_pp": 0.5,
         "class_tokens_x": 1.5, "hedge_rise_pp": 2.0, "list_rise_pp": 2.0, "noncoco_drop": 0.10,
         "matched_ni_sftref": -1.0, "under_moved_kl": 0.2, "kl_tail_steps": 50}
N_TRAIN, N_VAL = 2402, 924  # PI-1026u Q2: UT-2532 minus the 130 Karpathy-val ids; 2,532 reported beside it
IMG_RE = re.compile(r"\.(jpe?g|png)$", re.I)
COCO_RE = re.compile(r"(?:COCO_(?:train|val)2014_)?(\d{12})\.jpe?g$", re.I)


def sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def pinned(rel: str) -> Path:
    p = ROOT / rel
    if sha_file(p) != PINS[rel]:
        raise SystemExit(f"REFUSED: {rel} differs from its pin")
    return p


def ids(name: str) -> list[int]:
    """A pinned id list of the prereg folder (ut2402 / val924 / kv5000), sorted ints."""
    return [int(x) for x in pinned(f"manuscript/prereg/2026-10-27_grl_pilot/{name}.txt").read_text().split()]


def gold() -> dict[int, set[str]]:
    """COCO-2014 instance classes (80 categories, crowd included) of the UT-2402 and val-924 ids: the one gold of the
    reward and of the dev score (W8)."""
    g = json.loads(pinned("manuscript/prereg/2026-10-27_grl_pilot/gold_instances.json").read_text())
    return {int(k): set(v) for k, v in g["gold"].items()}


SHA64 = re.compile(r"\b[0-9a-f]{64}\b")


def cen_test_shas(rec: Path = CEN_REC, gpu_host: bool | None = None) -> set[str]:
    """CC-124 W3 (CC-119 W19, training side): the image sha256s of C-EN's three test-side hash records (Karpathy
    test, Karpathy val, NoCaps val). On a GPU host (M3/M4) a missing record is REFUSED; elsewhere it is empty."""
    if gpu_host is None:
        gpu_host = Path("/root/.vsps_machine_id").is_file()
    out: set[str] = set()
    for s in CEN_TEST_SIDE:
        p = rec / f"{s}.sha256.tsv"
        if not p.is_file():
            if gpu_host:
                raise SystemExit(f"REFUSED: C-EN record {p} is missing; the training-side sha check needs it")
            continue
        out |= set(SHA64.findall(p.read_text()))
    return out


def refused_sets() -> tuple[set[int], set[str]]:
    """COCO ids and image sha256s that must not exist on the machine: every exclusion.json id and sha, all of
    Karpathy val (the 130 UT ids in it are out of the Gate-1 pool, PI-1026u Q2, so none is ever staged), and every
    image sha of C-EN's test-side records, so a UT-train byte copy of a test image (CC-122) is refused too."""
    ex = json.loads(pinned("manuscript/prereg/2026-10-21_dev_pools/exclusion.json").read_text())
    bad = set().union(*map(set, ex["ids"]["coco"].values())) | set(ids("kv5000"))
    return bad, set().union(*map(set, ex["image_sha256"].values())) | cen_test_shas()


# ------------------------------------------------------------------------------------------------ host guard
def host_ok(expect_head: str | None, mid_file: Path = Path("/root/.vsps_machine_id")) -> str:
    """M3 or M4, an idle GPU, and (if given) the committed HEAD with a clean tracked tree. Returns the machine id."""
    mid = mid_file.read_text().strip().lower() if mid_file.is_file() else ""
    if mid not in MACHINES:
        raise SystemExit(f"REFUSED: {mid_file} is {mid or 'missing'!r}, not one of {MACHINES}")
    apps = subprocess.run(["nvidia-smi", "--query-compute-apps=pid", "--format=csv,noheader"],
                          capture_output=True, text=True)
    if apps.returncode != 0 or apps.stdout.strip():
        raise SystemExit("REFUSED: the GPU is not idle (never concurrent with another job, e.g. a C-EN test decode)")
    if expect_head:
        head = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        clean = subprocess.run(["git", "-C", str(ROOT), "diff", "--quiet", "HEAD", "--"]).returncode == 0
        if head != expect_head or not clean:
            raise SystemExit(f"REFUSED: HEAD {head[:8]} is not {expect_head[:8]}, or tracked files differ from HEAD")
    return mid


def scan(roots, bad_ids: set[int], bad_sha: set[str], skip=("/root/vsps/.venv",)) -> int:
    """Refuse (SystemExit) if any image file under `roots` is a test image or cannot be identified. An image is
    identified only by a COCO id in its file name; a non-COCO name (KTVIC, XM3600, NoCaps, ...) is refused because
    it cannot be shown to be a non-test image. Every image is hashed against exclusion.json's image_sha256. C-EN's
    memory images (COCO train/restval minus the refused ids) pass. Returns the number of images seen."""
    seen = 0
    for root in roots:
        for dirpath, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if not os.path.join(dirpath, d).startswith(skip)]
            for f in files:
                if not IMG_RE.search(f):
                    continue
                p, m = Path(dirpath) / f, COCO_RE.search(f)
                if m is None:
                    raise SystemExit(f"REFUSED: unidentifiable image {p} (not a COCO file name)")
                if int(m.group(1)) in bad_ids:
                    raise SystemExit(f"REFUSED: test image {p} (refused COCO id)")
                if sha_file(p) in bad_sha:  # ponytail: hashes every image (~1-2 min for C-EN's 112k); fine per stage
                    raise SystemExit(f"REFUSED: test image {p} (refused sha256)")
                seen += 1
    return seen


def m3_clear(rec: Path = CEN_REC, stage: Path = NCS_DATA / "datasets", busy=None) -> dict:
    """CC-119 W6 / CC-120 / CC-121: C-EN's three test-side hash records are complete (so its hash pass is over), no
    protected set is staged (cen_<set>/ is deleted by C-EN after its decode), and no C-EN process is running."""
    missing = [s for s in CEN_TEST_SIDE if not (rec / f"{s}.done.json").is_file()]
    if missing:
        raise SystemExit(f"REFUSED: C-EN test-side hash pass not complete ({missing}); C-EN has priority")
    staged = [s for s in CEN_TEST_SIDE if (stage / f"cen_{s}").exists()]
    if staged:
        raise SystemExit(f"REFUSED: protected C-EN set(s) staged on this machine: {staged}")
    if busy is None:
        busy = subprocess.run(["pgrep", "-f", "scripts/c_en/"], capture_output=True, text=True).stdout.split()
    if busy:
        raise SystemExit(f"REFUSED: a C-EN process is running (pids {busy}); C-EN has priority")
    return {"cen_hash_records": {s: sha_file(rec / f"{s}.done.json") for s in CEN_TEST_SIDE}}


def guard(expect_head: str | None) -> dict:
    """Run before every GPU stage: host, C-EN isolation, then the test-image scan. Also no UIT-ViIC test file under
    the data root."""
    mid = host_ok(expect_head)
    iso = m3_clear()
    if any(UV.rglob("test*")):
        raise SystemExit(f"REFUSED: a UIT-ViIC test file exists under {UV}")
    bad_ids, bad_sha = refused_sets()
    n = scan(SCAN_ROOTS, bad_ids, bad_sha)
    return {"machine_id": mid, "images_scanned": n, **iso}


SRC_PINS = {"train_data.json": "441d22d29eb7aa12d32d49e330778a4a918c3a9413c23294a9daec92a238d110",  # = id_counts
             "val_data.json": "fee7d116683670ef5ce14f405594aa73bb08dd1bdbf1f2cdc3f9e01bbfa9b044"}


def fetch(url: str, tries: int = 3) -> bytes:
    import time
    import urllib.request

    for n in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return r.read()
        except OSError:
            time.sleep(5 * (n + 1))
    raise SystemExit(f"fetch failed after {tries} tries: {url}")


def stage(src: Path, get=fetch, workers: int = 16) -> dict:
    """Stage UT-2402 + val-924 under UV: the train file cut to those ids (the 163 refused and 130 Karpathy-val ids never reach the
    machine), the val file unchanged, every image fetched from its own `coco_url`, hashed in memory, refused if its
    sha256 is in exclusion.json (or, for val, differs from uitviic_val.tsv), then written by tmp + os.replace.
    Idempotent: an existing image whose sha256 passes is kept. src holds the two release files (pinned shas)."""
    import concurrent.futures as cf

    for f, want in SRC_PINS.items():
        if sha_file(src / f) != want:
            raise SystemExit(f"REFUSED: {src / f} differs from its pin")
    ut, val = set(ids("ut2402")), set(ids("val924"))
    tr, va = (json.loads((src / f).read_text(encoding="utf-8")) for f in SRC_PINS)
    tr = {"images": [i for i in tr["images"] if int(i["id"]) in ut],
          "annotations": [a for a in tr["annotations"] if int(a["image_id"]) in ut]}
    if {int(i["id"]) for i in tr["images"]} != ut or {int(i["id"]) for i in va["images"]} != val:
        raise SystemExit("REFUSED: the release files do not hold exactly UT-2402 and val-924")
    vsha = {int(r.split("\t")[0]): r.split("\t")[2] for r in
            pinned("manuscript/prereg/2026-10-21_dev_pools/uitviic_val.tsv").read_text().splitlines()}
    _, bad_sha = refused_sets()
    (UV / "images").mkdir(parents=True, exist_ok=True)

    def one(im: dict) -> tuple[str, str]:
        f, url, i = im["file_name"], im["coco_url"], int(im["id"])
        if f != f"{i:012d}.jpg" or not url.startswith(("http://", "https://")) or not url.endswith("/" + f):
            raise SystemExit(f"REFUSED: id {i}: file name or url is not the release's rule")
        dst = UV / "images" / f
        data = dst.read_bytes() if dst.is_file() else get(url)
        h = hashlib.sha256(data).hexdigest()
        if h in bad_sha or (i in val and h != vsha[i]):
            raise SystemExit(f"REFUSED: id {i}: sha256 is a test image's or differs from uitviic_val.tsv")
        if not dst.is_file():
            tmp = dst.with_suffix(".part")
            tmp.write_bytes(data)
            os.replace(tmp, dst)
        return h, f

    with cf.ThreadPoolExecutor(workers) as ex:
        rows = sorted(ex.map(one, tr["images"] + va["images"]), key=lambda r: r[1])
    for name, d in (("train_data.json", tr), ("val_data.json", va)):
        tmp = UV / (name + ".part")
        tmp.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        os.replace(tmp, UV / name)
    (UV / "images.sha256").write_text("".join(f"{h}  {f}\n" for h, f in rows))
    return {"images": len(rows), "train_ids": len(ut), "val_ids": len(val),
            "images_sha256_list": sha_file(UV / "images.sha256")}


def selftest() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        (t / "a").mkdir()
        ok = t / "a" / "000000000005.jpg"
        ok.write_bytes(b"five")
        assert scan([t], {9}, set()) == 1
        (t / "a" / "COCO_val2014_000000000009.jpg").write_bytes(b"nine")
        try:
            scan([t], {9}, set())
        except SystemExit as e:
            assert "refused COCO id" in str(e), e
        else:
            raise AssertionError("refused id accepted")
        (t / "a" / "COCO_val2014_000000000009.jpg").unlink()
        try:
            scan([t], set(), {hashlib.sha256(b"five").hexdigest()})
        except SystemExit as e:
            assert "refused sha256" in str(e), e
        else:
            raise AssertionError("sha refusal")
        (t / "a" / "0f1e2d3c4b5a6978.jpg").write_bytes(b"nocaps-like")
        try:
            scan([t], set(), set())
        except SystemExit as e:
            assert "unidentifiable" in str(e), e
        else:
            raise AssertionError("non-COCO image accepted")
        (t / "a" / "0f1e2d3c4b5a6978.jpg").unlink()
        (t / ".venv").mkdir()
        (t / ".venv" / "x.png").write_bytes(b"icon")
        assert scan([t], set(), set(), skip=(str(t / ".venv"),)) == 1
        mid = t / "mid"
        for val, good in (("m3\n", True), ("M4", True), ("m1", False), (None, False)):
            if val is None:
                mid.unlink()
            else:
                mid.write_text(val)
            try:
                host_ok(None, mid)
            except SystemExit as e:
                assert not good or "GPU" in str(e), (val, e)  # no GPU on the laptop: the idle check refuses
            except FileNotFoundError:  # no nvidia-smi on the laptop: the machine check already passed
                assert good, val
    assert COCO_RE.search("COCO_train2014_000000535668.jpg").group(1) == "000000535668"
    assert COCO_RE.search("000000535668.jpg") and not COCO_RE.search("535668.jpg")
    stage_selftest()
    with tempfile.TemporaryDirectory() as t:
        rec, st = Path(t) / "rec", Path(t) / "ds"
        rec.mkdir()
        st.mkdir()
        for want, setup in (("not complete", lambda: None),
                            ("staged", lambda: [(rec / f"{s}.done.json").write_text("{}") for s in CEN_TEST_SIDE]
                             and (st / "cen_coco_kval").mkdir()),
                            ("process", lambda: (st / "cen_coco_kval").rmdir())):
            setup()
            try:
                m3_clear(rec, st, busy=["123"] if want == "process" else [])
            except SystemExit as e:
                assert want in str(e), (want, e)
            else:
                raise AssertionError(f"m3_clear accepted: {want}")
        (st / "cen_memory").mkdir()  # C-EN memory images (train/restval) do not block
        assert set(m3_clear(rec, st, busy=[])["cen_hash_records"]) == set(CEN_TEST_SIDE)
        # W3: the test-side records' shas are refused on the training side; a missing record refuses on a GPU host
        h = hashlib.sha256(b"test-image").hexdigest()
        (rec / "coco_test.sha256.tsv").write_text(f"1\tCOCO_val2014_000000000001.jpg\t{h}\t123\n")
        assert cen_test_shas(rec, gpu_host=False) == {h}
        try:
            cen_test_shas(rec, gpu_host=True)
        except SystemExit as e:
            assert "missing" in str(e), e
        else:
            raise AssertionError("a missing C-EN record was accepted on a GPU host")
        for s in CEN_TEST_SIDE[1:]:
            (rec / f"{s}.sha256.tsv").write_text("")
        assert cen_test_shas(rec, gpu_host=True) == {h}
        (st / "000000000007.jpg").write_bytes(b"test-image")
        try:
            scan([st], set(), cen_test_shas(rec, gpu_host=True))
        except SystemExit as e:
            assert "refused sha256" in str(e), e
        else:
            raise AssertionError("a byte copy of a C-EN test image was accepted")
    print("common selftest ok")


def stage_selftest() -> None:
    """stage() on two synthetic release files (train 1, 2 with 2 refused; val 3) with the pins swapped for the test."""
    import tempfile

    g, h = globals(), lambda b: hashlib.sha256(b).hexdigest()  # noqa: E731
    keep = {k: g[k] for k in ("UV", "SRC_PINS", "ids", "pinned", "refused_sets")}
    blob = {1: b"img-1", 2: b"img-2", 3: b"img-3"}
    im = lambda i: {"id": i, "file_name": f"{i:012d}.jpg", "coco_url": f"http://h/x/{i:012d}.jpg"}  # noqa: E731
    try:
        with tempfile.TemporaryDirectory() as t:
            t, src = Path(t), Path(t) / "src"
            src.mkdir()
            (src / "train_data.json").write_text(json.dumps({"images": [im(1), im(2)], "annotations": [
                {"image_id": 1, "id": 10}, {"image_id": 2, "id": 11}]}))
            (src / "val_data.json").write_text(json.dumps({"images": [im(3)], "annotations": []}))
            (t / "val.tsv").write_text(f"3\t{3:012d}.jpg\t{h(blob[3])}\n")
            g.update(UV=t / "uv", SRC_PINS={f: sha_file(src / f) for f in ("train_data.json", "val_data.json")},
                     ids=lambda n: {"ut2402": [1], "val924": [3]}[n], pinned=lambda _rel: t / "val.tsv",
                     refused_sets=lambda: ({2}, set()))
            get = lambda url: blob[int(url[-16:-4])]  # noqa: E731
            r = stage(src, get, workers=2)
            assert r["images"] == 2 and not (t / "uv/images/000000000002.jpg").exists(), r
            assert json.loads((t / "uv/train_data.json").read_text())["annotations"] == [{"image_id": 1, "id": 10}]
            assert stage(src, get, workers=2) == r  # idempotent
            (t / "bad.tsv").write_text(f"3\t{3:012d}.jpg\t{h(b'other')}\n")
            for bad in ({"refused_sets": lambda: ({2}, {h(blob[1])})}, {"pinned": lambda _rel: t / "bad.tsv"}):
                for f in (t / "uv/images").iterdir():
                    f.unlink()
                g.update(bad)
                try:
                    stage(src, get, workers=2)
                except SystemExit as e:
                    assert "REFUSED" in str(e), e
                else:
                    raise AssertionError(f"stage accepted {list(bad)}")
                g.update(refused_sets=lambda: ({2}, set()), pinned=lambda _rel: t / "val.tsv")
    finally:
        g.update(keep)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    elif sys.argv[1:2] == ["guard"]:  # guard [EXPECT_HEAD]
        print(json.dumps(guard(sys.argv[2] if len(sys.argv) > 2 else None)))
    elif sys.argv[1:2] == ["stage"]:  # stage [SRC_DIR]
        print(json.dumps(stage(Path(sys.argv[2]) if len(sys.argv) > 2 else UV / "src")))
    else:
        sys.exit(__doc__)
