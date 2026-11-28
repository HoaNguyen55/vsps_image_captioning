"""O31 §3.5 overlap pass launcher (prereg v3 §3.5, ERRATUM_O31_1 E13, ERRATUM_O31_2 E2). `$PY -I -B s35.py <cmd>`,
VSPS_REPO = the pinned snapshot. Runs before the first of G1 and G2. Descriptors and ids only; nothing is decoded.

  feats  (PI's PC) --set pool|ktvic_test|uit_test|karpathy_test --images DIR --sscd PT [--train TRAIN_JSON]
         [--workers N] --out NPZ          pool needs --train (KTVIC train_data.json, pin 72ee9b57)
  kv     (laptop)  --kval feats_coco_kval.npz --out NPZ     KV-4,224 rows of C-EN's KV features (pin 9783f7a6)
  pass   (laptop)  --feats DIR (pool.npz ktvic_test.npz uit_test.npz karpathy_test.npz tier3.npz) --out DIR
         -> w4_pass.json (removed ids, counts, input shas) and exclude_p1.txt (twins + part (a) hits; P1 --exclude)
The PC's feature files come to the laptop home by the O-H7 copy (sha-checked) before `pass`.
"""
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, os.environ.get("O31_SRC", str(Path(__file__).resolve().parent / "src")))  # O31_SRC: tests only

from o31 import overlap, stage1  # noqa: E402


def cmd_feats(a) -> int:
    train = None
    if a.set == "pool":
        if a.train is None or hashlib.sha256(a.train.read_bytes()).hexdigest() != stage1.KTVIC_TRAIN_SHA:
            raise SystemExit("REFUSED pool needs --train, the pinned KTVIC train_data.json (72ee9b57)")
        train = [{"file_name": i.get("file_name") or i.get("filename")}
                 for i in json.loads(a.train.read_text(encoding="utf-8"))["images"]]
    print(json.dumps(overlap.feats(a.set, overlap.set_rows(a.set, train), a.images, a.sscd, a.out, a.workers)))
    return 0


def cmd_kv(a) -> int:
    print(json.dumps(overlap.kv_feats(a.kval, a.out)))
    return 0


def cmd_pass(a) -> int:
    rec = overlap.run_pass({k: a.feats / f"{k}.npz" for k in overlap.EXPECT_N}, a.out)
    print(json.dumps({"removed": {k: len(v) for k, v in rec["removed"].items()}, "n_exclude_p1": rec["n_exclude_p1"],
                      "exclude_p1_sha256": rec["exclude_p1_sha256"]}))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("feats")
    f.add_argument("--set", choices=("pool", "ktvic_test", "uit_test", "karpathy_test"), required=True)
    f.add_argument("--images", type=Path, required=True)
    f.add_argument("--sscd", type=Path, required=True)
    f.add_argument("--train", type=Path)
    f.add_argument("--workers", type=int, default=4)
    f.add_argument("--out", type=Path, required=True)
    k = sub.add_parser("kv")
    k.add_argument("--kval", type=Path, required=True)
    k.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("pass")
    p.add_argument("--feats", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    return {"feats": cmd_feats, "kv": cmd_kv, "pass": cmd_pass}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
