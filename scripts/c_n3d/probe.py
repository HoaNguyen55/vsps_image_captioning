"""Import every instrument module of the run from ROOT and call each instrument on synthetic strings (no input data).

  python3 -I -B probe.py ROOT NCS_DATA --trace OUT      (closure.py: audit hook, list opened and loaded files)
  python3 -I -B probe.py ROOT NCS_DATA --pins PUSH_LIST  (host `closure` mode: every loaded module under ROOT on it)

Used twice: by closure.py on the run repository with an audit hook (TRACE_OUT lists every file under ROOT that was
opened and every module file loaded), and by `host_selftest.sh closure ROOT` on a tree built from the PUSH LIST only.
NCS_DATA must hold only vncorenlp/ (the pinned jar and segmenter models): the toy scorer needs them.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT, DATA = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
OPENED: set[str] = set()


def hook(event, args):
    if event == "open" and args and isinstance(args[0], (str, bytes, os.PathLike)):
        p = os.fsdecode(args[0])
        if p.startswith(str(ROOT)):
            OPENED.add(p)


MODE, ARG = (sys.argv[3], Path(sys.argv[4])) if len(sys.argv) > 4 else (None, None)
if MODE == "--trace":
    sys.addaudithook(hook)
os.environ["NCS_DATA"] = str(DATA)
os.chdir(ROOT)
for d in (".", "scripts", "scripts/lb", "scripts/c_attr", "scripts/c_stage1", "scripts/c_stage2", "scripts/c_en",
          "scripts/kit_b"):  # c_n3d_host.paths order
    sys.path.insert(0, str(ROOT / d))

import c_attr  # noqa: E402,F401
import c_attr_score as CS  # noqa: E402
import cen_score as CE  # noqa: E402
import decode_icl as C  # noqa: E402
import guard as G  # noqa: E402
import rl_reward as R  # noqa: E402
import score as S1  # noqa: E402,F401
import score2  # noqa: E402,F401
import score_coco_probe as SC  # noqa: E402
import stage2  # noqa: E402,F401
import xm3600_oiv7 as XO  # noqa: E402
from rescap import chair as CH  # noqa: E402

vi = ["chó tím xổm ghế sofa đỏ rực lúc trưa", "ba ông lão dắt xe máy cũ qua kênh xanh", "mèo mướp chó con chơi đàn"]
out = {"classes": [G.classes(t) for t in vi], "key": [G.key(o) for t in vi for o in G.classes(t)],
       "neighbour_only": G.neighbour_only(vi[2], vi[0], [vi[1], "mèo mướp lim dim"]),
       "syllables": R.syllables(vi[1]), "copy_stat": R.copy_stat(R.syllables(vi[0]), [R.syllables(vi[2])])[0],
       "gold": sorted(CH._gold_objects(vi)), "shown": C.shown({"openviic": "a", "ktvic": "b"}, "openviic"),
       "en_classes": sorted(SC.en_classes("purple dog couch cat sky", SC.load_synonyms())),
       "vmap_size": len(XO.resolve_map(ROOT / "data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv"))}
import c_n3d as N  # noqa: E402  CC-511 W6: the run's neighbour-only rule equals guard.neighbour_only
vin = N.vi_instruments()
cases = [(vi[2], vi[0], [vi[1], "mèo mướp lim dim"]), (vi[1], vi[2], [vi[0]]), (vi[0], "", [vi[0], vi[2]]),
         ("chó mèo xe máy tím rịm", "chó tím", ["mèo mướp", "xe máy cũ", "chó tím"])]
if [vin.neighbour_only(*c) for c in cases] != [G.neighbour_only(*c) for c in cases]:
    raise SystemExit("STOP: Instruments.neighbour_only differs from guard.neighbour_only")
out["neighbour_only_equal"] = len(cases)
score = CS.kit_scorer(CS.KIT)
out["kit_cider"] = score({"a": vi[0], "b": vi[1]}, {"a": [vi[0], vi[2]], "b": [vi[1], vi[2]]}).round(3).tolist()
tok, cider = CE.ptb_cider()
g = tok({"a": ["purple dog couch sky", "dog sky"], "b": ["three bikes grass hum", "grass hum"]})
out["ptb_cider"] = cider(g, tok({"a": ["purple dog couch sky"], "b": ["cat hum"]})).round(3).tolist()
mods = sorted({str(Path(m.__file__).resolve()) for m in list(sys.modules.values())
               if getattr(m, "__file__", None) and str(Path(m.__file__).resolve()).startswith(str(ROOT))})
if MODE == "--pins":
    import c_n3d_host as H
    out["modules_pinned"] = H.module_pin_check(ROOT, ARG)
if MODE == "--trace":
    ARG.write_text(json.dumps({"opened": sorted(OPENED), "modules": mods}, indent=0) + "\n")
print(json.dumps({k: (v if k in ("kit_cider", "ptb_cider", "vmap_size", "copy_stat", "modules_pinned") else "ok")
                  for k, v in out.items()}))
print("probe: ok")
