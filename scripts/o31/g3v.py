"""G3v (ERRATUM_O31_5 G-5, CODE_NEEDS C22): registered tier-1 V-COCO probes on P-a, host GPU, right after the G3 decodes.

    $PY -I -B g3v.py run --family vintern|internvl3 --preds S0.preds.json --items UIT.tsv --images DIR --snapshot SNAP --out ROOT
    $PY -I -B g3v.py status --out ROOT

One job, one launch clock (ROOT/launch.json), cap 1 h, whatever K1 shows. Each family runs in its own venv as
probe.py requires (vintern 4.51.3, internvl3 4.57.6) under the same clock. Counts and shas only in the log.
"""
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, os.environ.get("O31_SRC", str(Path(__file__).resolve().parent / "src")))  # O31_SRC: mutant runs only

from o31 import decode, probe, vcoco  # noqa: E402


def cmd_run(a) -> int:
    items = decode.read_items(a.items)
    if len(items) != vcoco.UIT_TEST_N:
        raise SystemExit(f"REFUSED G3v probes the {vcoco.UIT_TEST_N} UIT-ViIC test images of S0's G3 decode")
    preds = vcoco.read_decode(a.preds, items)
    vcoco.check_images(items, a.images, vcoco.uit_test_shas())
    work, units = vcoco.pa_work(preds, items)
    a.out.mkdir(parents=True, exist_ok=True)
    rec = {"n_images": len(units), "n_propositions": sum(len(u["classes"]) for u in units),
           "preds_sha256": hashlib.sha256(a.preds.read_bytes()).hexdigest(),
           "items_sha256": hashlib.sha256(a.items.read_bytes()).hexdigest()}
    (a.out / "pa_inputs.json").write_text(json.dumps(rec) + "\n")
    (a.out / "pa_units.json").write_text(json.dumps(units) + "\n")  # image ids and class names only
    fn, info = probe.load(a.family, a.snapshot)
    (a.out / f"model_{a.family}.json").write_text(json.dumps(info) + "\n")
    from PIL import Image

    return vcoco.run_family(fn, work, a.out, a.family, lambda n: Image.open(a.images / n).convert("RGB"))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--family", choices=vcoco.FAMILIES, required=True)
    r.add_argument("--preds", type=Path, required=True)
    r.add_argument("--items", type=Path, required=True)
    r.add_argument("--images", type=Path, required=True)
    r.add_argument("--snapshot", type=Path, required=True)
    r.add_argument("--out", type=Path, required=True)
    s = sub.add_parser("status")
    s.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    if a.cmd == "status":
        print(json.dumps(vcoco.status(a.out)))
        return 0
    return cmd_run(a)


if __name__ == "__main__":
    sys.exit(main())
