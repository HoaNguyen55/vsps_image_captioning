#!/usr/bin/env python
"""Build the annotation sheet for the exhaustive human object gold on KTVIC test (plan B1).

    NCS_DATA=$PWD/data python scripts/object_gold_sample.py --out-dir data/object_gold

300 of the 558 KTVIC test images, seed 42, stratified by the number of reference-derived
object classes (the gold of scripts/object_prf.py) into bins <=1, 2, 3, 4, 5, 6, >=7 with
proportional allocation (largest remainder). No image is excluded: all 558 test images
are eligible, including the 3 whose references name no lexicon object.

Writes:
  annotate.html  -- self-contained checkbox sheet; each annotator opens it, types a name,
                    ticks classes, then "Tải file JSON" -> annot_<name>.json
  thumbs/        -- 800 px copies of the images (annotate.html reads them by file name)
  sample.json    -- seed, image ids, file names, stratum, class list

Classes are the object lexicon of rescap/chair.py (113 entries, `ảnh` is never extracted)
folded to one checkbox per canonical form: svp.matching.canonical plus the four exact
synonyms in SYNONYMS, i.e. 101 checkboxes. Ticks are entered by people only.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from rescap.chair import _NOT_OBJECTS  # noqa: E402
from rescap.svp.matching import canonical  # noqa: E402
from rescap.vi.lexicon import NOUN_CLASSIFIER  # noqa: E402

#: Exact synonyms canonical() leaves apart; applied to annotations and captions alike.
SYNONYMS = {"dù": "ô", "căn phòng": "phòng", "dòng sông": "sông", "sạp hàng": "quầy hàng"}

GROUPS = {
    "Người": ["người", "phụ nữ", "đàn ông", "cô gái", "cô gái trẻ", "chàng trai", "thanh niên",
              "nam thanh niên", "bạn trẻ", "bạn", "cặp đôi", "trẻ em", "đứa trẻ", "em bé",
              "bé gái", "bé trai", "học sinh", "công nhân"],
    "Động vật": ["chó", "mèo", "gà", "vịt", "chim", "cá", "bò", "trâu", "lợn", "ngựa", "voi",
                 "khỉ", "rắn", "ong", "bướm", "vật"],
    "Phương tiện": ["xe", "xe máy", "xe đạp", "ô tô", "xe buýt", "xe tải", "xe tăng", "xe ba gác",
                    "xe đẩy", "xích lô", "thuyền", "tàu", "máy bay", "buồm", "mái chèo",
                    "bánh lái", "cọc neo"],
    "Trang phục, đồ cá nhân": ["áo", "quần", "mũ", "nón lá", "giày", "dép", "kính", "túi", "ô",
                               "đồng hồ", "điện thoại"],
    "Đồ vật": ["bàn", "ghế", "bát", "đĩa", "cốc", "dao", "bút", "sách", "báo", "tranh", "mô hình",
               "bóng", "chổi", "cửa", "biển báo", "biển hiệu", "quả", "hoa", "đồ"],
    "Cảnh, công trình": ["bầu trời", "mặt trời", "ánh sáng", "núi", "sông", "cây", "khu rừng",
                         "cánh đồng", "bãi biển", "tảng đá", "mỏm đá", "đường", "vỉa hè", "cầu",
                         "nhà", "dãy nhà", "phòng", "trường", "chợ", "quầy hàng"],
}
BINS = ((0, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 99))


def class_key(noun: str) -> str:
    """The checkbox a lexicon noun belongs to."""
    c = canonical(noun) or noun
    return SYNONYMS.get(c, c)


def surface_forms() -> dict[str, list[str]]:
    """checkbox -> lexicon nouns that land on it."""
    out: dict[str, list[str]] = defaultdict(list)
    for noun in sorted(NOUN_CLASSIFIER):
        if noun not in _NOT_OBJECTS:
            out[class_key(noun)].append(noun)
    return dict(out)


CLASSES = sorted(surface_forms())
_grouped = [c for g in GROUPS.values() for c in g]
assert sorted(_grouped) == CLASSES, set(_grouped) ^ set(CLASSES)


def stratified_sample(counts: dict[str, int], n: int, seed: int) -> dict[str, int]:
    """image_id -> bin index; proportional allocation, largest remainder, seeded draw per bin."""
    members: dict[int, list[str]] = defaultdict(list)
    for image_id, k in sorted(counts.items(), key=lambda kv: int(kv[0])):
        members[next(b for b, (lo, hi) in enumerate(BINS) if lo <= k <= hi)].append(image_id)
    exact = {b: n * len(m) / len(counts) for b, m in members.items()}
    take = {b: int(x) for b, x in exact.items()}
    for b in sorted(exact, key=lambda b: (take[b] - exact[b], b))[: n - sum(take.values())]:
        take[b] += 1
    rng = random.Random(seed)
    return {i: b for b in sorted(members) for i in rng.sample(members[b], take[b])}


HTML = """<!doctype html><html lang="vi"><head><meta charset="utf-8">
<title>Gán nhãn vật thể KTVIC</title><style>
body{font-family:system-ui,sans-serif;margin:0;display:flex;height:100vh}
#left{flex:1.2;padding:12px;overflow:auto}#right{flex:1;padding:12px;overflow:auto;border-left:1px solid #ccc}
img{max-width:100%;max-height:78vh}fieldset{margin:0 0 8px;padding:4px 8px}legend{font-weight:bold}
label{display:inline-block;min-width:9.5em;margin:2px 0}textarea{width:100%;height:4em}
small{color:#666}.done{color:green}button{margin:2px}
</style></head><body>
<div id="left"><div><b id="pos"></b> <span id="file"></span> <span id="st"></span></div><img id="img"></div>
<div id="right">
 <div>Người gán: <input id="who" size="10"> <button id="dl">Tải file JSON</button>
  <input type="file" id="load" accept=".json"> <small id="prog"></small></div>
 <form id="f"></form>
 <div><b>Vật thể khác</b> <small>(không có trong danh sách, cách nhau bởi dấu phẩy)</small>
 <textarea id="other"></textarea></div>
 <button id="prev">&larr; Trước</button><button id="next">Lưu &amp; tiếp &rarr;</button>
 <small>Hướng dẫn: .paper_work/OBJECT_GOLD_PROTOCOL.md</small>
</div><script>
const S=__SAMPLE__;let i=0,A={};
const who=document.getElementById('who'),f=document.getElementById('f'),other=document.getElementById('other');
for(const[g,cs]of Object.entries(S.groups)){const fs=document.createElement('fieldset');
 fs.innerHTML='<legend>'+g+'</legend>'+cs.map(c=>'<label><input type=checkbox value="'+c+'"> '+c+
 (S.forms[c].filter(x=>x!==c).length?' <small>('+S.forms[c].filter(x=>x!==c).join(', ')+')</small>':'')+'</label>').join('');f.appendChild(fs)}
const key=()=>'objgold_'+who.value.trim();
function persist(){try{localStorage.setItem(key(),JSON.stringify(A));localStorage.setItem('objgold_who',who.value)}catch(e){}}
function save(done){const id=S.images[i].id;
 A[id]={classes:[...f.querySelectorAll('input:checked')].map(x=>x.value),other:other.value.trim(),done:done||(A[id]||{}).done||false};persist()}
function show(){const im=S.images[i],a=A[im.id]||{classes:[],other:''};
 document.getElementById('img').src='thumbs/'+im.file;document.getElementById('pos').textContent=(i+1)+'/'+S.images.length;
 document.getElementById('file').textContent=im.file;document.getElementById('st').innerHTML=a.done?'<span class=done>&#10003; đã xong</span>':'';
 f.querySelectorAll('input').forEach(x=>x.checked=a.classes.includes(x.value));other.value=a.other;
 document.getElementById('prog').textContent=Object.values(A).filter(x=>x.done).length+' ảnh đã xong'}
function go(d,done){save(done);i=Math.max(0,Math.min(S.images.length-1,i+d));show()}
document.getElementById('next').onclick=()=>go(1,true);document.getElementById('prev').onclick=()=>go(-1,false);
who.onchange=()=>{try{A=JSON.parse(localStorage.getItem(key())||'{}')}catch(e){A={}}show()};
document.getElementById('dl').onclick=()=>{save(false);if(!who.value.trim()){alert('Nhập tên người gán');return}
 const b=new Blob([JSON.stringify({annotator:who.value.trim(),seed:S.seed,labels:A},null,1)],{type:'application/json'});
 const u=document.createElement('a');u.href=URL.createObjectURL(b);u.download='annot_'+who.value.trim()+'.json';u.click()};
document.getElementById('load').onchange=e=>{const r=new FileReader();r.onload=()=>{const d=JSON.parse(r.result);
 who.value=d.annotator;A=d.labels;persist();show()};r.readAsText(e.target.files[0])};
try{who.value=localStorage.getItem('objgold_who')||''}catch(e){}who.onchange();
</script></body></html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-dir", default=str(ROOT / "data" / "object_gold"))
    ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--split", default="test_data.json")
    args = ap.parse_args()

    from PIL import Image

    from evaluate import KTVIC, file_names, references
    from rescap.chair import objects_in

    refs = references(args.split)
    counts = {k: len(set().union(*[set(objects_in(r)) for r in rs])) for k, rs in refs.items()}
    picked = stratified_sample(counts, args.n, args.seed)
    names = file_names(args.split)
    out = Path(args.out_dir)
    (out / "thumbs").mkdir(parents=True, exist_ok=True)
    missing = []
    for image_id in picked:
        src = KTVIC / "images" / names[image_id]
        if not src.exists():
            missing.append(names[image_id])
            continue
        im = Image.open(src).convert("RGB")
        im.thumbnail((800, 800))
        im.save(out / "thumbs" / names[image_id], quality=88)

    order = sorted(picked, key=int)
    random.Random(args.seed).shuffle(order)
    sample = {
        "seed": args.seed, "split": args.split, "n_eligible": len(counts), "excluded": [],
        "bins": [list(b) for b in BINS],
        "images": [{"id": i, "file": names[i], "stratum": picked[i], "ref_objects": counts[i]} for i in order],
        "classes": CLASSES, "groups": GROUPS, "forms": surface_forms(), "synonyms": SYNONYMS,
    }
    (out / "sample.json").write_text(json.dumps(sample, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "annotate.html").write_text(HTML.replace("__SAMPLE__", json.dumps(sample, ensure_ascii=False)),
                                       encoding="utf-8")
    per_bin = defaultdict(lambda: [0, 0])
    for k in counts.values():
        per_bin[next(b for b, (lo, hi) in enumerate(BINS) if lo <= k <= hi)][0] += 1
    for b in picked.values():
        per_bin[b][1] += 1
    print(f"{len(picked)} of {len(counts)} test images (seed {args.seed}, none excluded), {len(CLASSES)} classes"
          f" -> {out}/annotate.html (+ sample.json, thumbs/)")
    for b, (lo, hi) in enumerate(BINS):
        label = f"{lo}" if lo == hi else (f"<={hi}" if lo == 0 else f">={lo}")
        print(f"  ref objects {label:>4s}: {per_bin[b][1]:3d} / {per_bin[b][0]:3d}")
    if missing:
        print(f"  ! {len(missing)} images not found under {KTVIC / 'images'}: {missing[:5]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
