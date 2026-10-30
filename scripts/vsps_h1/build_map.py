#!/usr/bin/env python
"""Build vi_en_map.json: Vietnamese entity head noun -> English detector prompt (VSPS H1).

    python scripts/vsps_h1/build_map.py --records <dir of stage-1 *.json> [--out scripts/vsps_h1/vi_en_map.json]

The map is a fixed translation dictionary for detector PROMPTS. It is a method
component, not evidence: no label in it is a judgement about any image.

Order of the deterministic rules, first hit wins:
  1. key = NFC + lowercase + one tone placement (rescap.chair.norm_tone), leading
     quantifiers stripped (QUANTIFIERS, repeatedly);
  2. key looked up in TABLE (the hand-written table below);
  3. svp.matching.canonical(key) looked up in TABLE;
     (steps 2-4 run first on the form before quantifier stripping, then on the stripped key);
  4. key, then canonical(key), looked up as a term of data/coco_probe/coco80_vi.json
     (the existing COCO-80 Vietnamese lexicon; `_rui_ro` notes skipped) -> COCO class name;
  5. otherwise UNMAPPED: logged in the output, and the detector vote for that
     entity is UNCERTAIN (the verifier keeps its own verdict).

TABLE status: drafted by Claude (AI) on 2026-10-31 from the stage-1 head-noun
vocabulary, frequency first; reviewed by the same agent against coco80_vi.json.
Human review is optional and non-blocking (CC-198 ruling 4). Truncated
stage-1 parses (e.g. `biển quảng` from `biển quảng cáo`) are listed on purpose;
non-objects and ambiguous tokens (`xanh`, `đi`, `khác`, `giá`, `đồ`, `vật` ...)
are deliberately absent so they stay UNMAPPED.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from rescap.chair import norm_tone  # noqa: E402
from rescap.svp.matching import canonical  # noqa: E402

QUANTIFIERS = ("một số", "một nhóm", "nhóm", "nhiều", "các", "những", "số", "vài", "một", "hai", "ba",
               "bốn", "năm", "sáu", "bảy", "tám", "chín", "mười")

PERSON = "person"
TABLE: dict[str, str] = {
    # people
    "người": PERSON, "ông": "man", "đàn ông": "man", "phụ nữ": "woman", "trẻ em": "child", "đứa trẻ": "child",
    "trẻ": "child", "em bé": "baby", "bé gái": "girl", "bé trai": "boy", "cô gái": "girl", "cô gái trẻ": "girl",
    "chàng trai": "young man", "thanh niên": "young man", "nam thanh niên": "young man", "bạn trẻ": PERSON,
    "học sinh": "student", "nhân viên": PERSON, "khách hàng": PERSON, "khách": PERSON, "bán hàng": PERSON,
    "cô giáo": "woman", "công nhân": "worker", "cặp đôi": PERSON, "đôi bạn": PERSON, "nhóm người": PERSON,
    # vehicles
    "xe máy": "motorcycle", "xe đạp": "bicycle", "xe": "vehicle", "ô tô": "car", "taxi": "car", "xe tải": "truck",
    "xe buýt": "bus", "xe đẩy": "cart", "xe tăng": "tank", "thuyền": "boat", "ghe": "boat", "tàu": "ship",
    "máy bay": "airplane", "xích lô": "cyclo", "xe ba gác": "cargo tricycle", "container": "shipping container",
    # buildings and structures
    "nhà": "house", "dãy nhà": "houses", "toà nhà": "building", "cửa": "door", "cổng": "gate", "cổng đá": "stone gate",
    "cổng sắt": "iron gate", "cổng vào": "gate", "cổng thành": "gate", "cánh cổng": "gate", "cầu": "bridge",
    "tường": "wall", "tường màu": "wall", "tường đá": "stone wall", "tường gỗ": "wooden wall", "tường gạch": "brick wall",
    "tường cũ": "wall", "vách tường": "wall", "hàng rào": "fence", "dải rào": "fence", "lan can": "railing",
    "đền": "temple", "chùa": "pagoda", "tháp": "tower", "tháp truyền": "transmission tower", "mái vòm": "dome",
    "ban công": "balcony", "mái che": "awning", "mái hiên": "awning", "hành lang": "corridor", "bậc thang": "stairs",
    "bậc": "steps", "thang": "ladder", "thang nhôm": "aluminum ladder", "thang máy": "elevator", "lều": "tent",
    "khách sạn": "hotel", "sân khấu": "stage", "quầy hàng": "stall", "quầy bán": "counter", "sạp hàng": "stall",
    "hàng quán": "stall", "chợ": "market stall", "quán cà": "cafe", "hồ bơi": "swimming pool", "bể bơi": "swimming pool",
    "bể nước": "water tank", "bồn chứa": "tank", "phòng": "room", "căn phòng": "room", "trường": "school",
    "tượng": "statue", "tượng nhỏ": "statue", "tượng đá": "stone statue", "tượng ông": "statue", "tượng phật": "buddha statue",
    "tượng nữ": "statue", "mô hình": "model",
    # street furniture and signs
    "biển hiệu": "signboard", "bảng hiệu": "signboard", "biển quảng": "billboard", "bảng quảng": "billboard",
    "biển báo": "road sign", "biển thông": "sign", "bảng thông": "notice board", "bảng giá": "price board",
    "bảng": "board", "bảng menu": "menu board", "bảng chữ": "sign", "bảng tên": "name sign", "biển tên": "name sign",
    "biển số": "license plate", "cột biển": "sign pole", "biểu ngữ": "banner", "logo": "logo", "nhãn": "label",
    "nhãn giá": "price tag", "nhãn hiệu": "label", "mã qr": "qr code", "cột đèn": "lamp post", "cột điện": "utility pole",
    "cột truyền": "utility pole", "cột tín": "traffic light", "đèn tín": "traffic light", "cột": "pillar",
    "cột cờ": "flagpole", "cột đá": "stone pillar", "hàng cột": "columns", "dây điện": "power line", "dây": "wire",
    "dải phân": "road divider", "thùng rác": "trash can", "vỉa hè": "sidewalk", "đường": "road", "con đường": "road",
    # nature and scene objects
    "cây": "tree", "cối": "trees", "cây cối": "trees", "cổ thụ": "old tree", "cọ": "palm tree", "dừa": "coconut",
    "tre": "bamboo", "thông": "pine tree", "thông noel": "christmas tree", "thông nhỏ": "christmas tree",
    "phượng": "flame tree", "bàng": "tree", "xương rồng": "cactus", "hoa": "flower", "phong lan": "orchid",
    "cỏ": "grass", "cỏ khô": "hay", "cỏ cao": "tall grass", "cỏ mọc": "grass", "dải cỏ": "grass", "lá": "leaf",
    "bầu trời": "sky", "nền trời": "sky", "đám mây": "cloud", "mây": "cloud", "mặt trời": "sun", "núi": "mountain",
    "sông": "river", "dòng sông": "river", "kênh": "canal", "kênh nước": "canal", "hồ nước": "lake", "biển": "sea",
    "bãi biển": "beach", "bờ biển": "shore", "dải cát": "sand", "hòn đảo": "island", "tảng đá": "rock", "mỏm đá": "rock",
    "viên đá": "stone", "đá": "rock", "cánh đồng": "field", "khu vườn": "garden", "sân vườn": "garden",
    "khu rừng": "forest", "công viên": "park", "mặt nước": "water", "sóng": "wave", "nền đất": "ground",
    "mặt đất": "ground", "nền gạch": "tiled floor", "sàn gỗ": "wooden floor", "ánh sáng": "light",
    # animals
    "chó": "dog", "mèo": "cat", "bò": "cow", "trâu": "water buffalo", "gà": "chicken", "vịt": "duck", "chim": "bird",
    "cá": "fish", "ngựa": "horse", "voi": "elephant", "lợn": "pig", "khỉ": "monkey", "bướm": "butterfly",
    "ong": "bee", "rắn": "snake", "sư tử": "lion", "khủng long": "dinosaur", "con vật": "animal",
    # clothing and personal items
    "áo": "shirt", "quần": "pants", "váy": "dress", "mũ": "hat", "nón": "hat", "nón lá": "conical hat",
    "giày": "shoes", "dép": "sandals", "kính": "glasses", "khẩu trang": "face mask", "khăn": "scarf",
    "khăn quàng": "scarf", "cà vạt": "tie", "thắt lưng": "belt", "găng tay": "gloves", "vòng cổ": "necklace",
    "vòng tay": "bracelet", "túi": "bag", "balo": "backpack", "vali": "suitcase", "ví": "wallet", "ô": "umbrella",
    "dù": "umbrella", "mặt nạ": "mask", "tai nghe": "headphones", "đồng hồ": "clock", "mái tóc": "hair",
    # household, shop and food
    "bàn": "table", "ghế": "chair", "tủ": "cabinet", "tủ lạnh": "refrigerator", "kệ": "shelf", "kệ hàng": "shelf",
    "giá kệ": "shelf", "kệ trưng": "display shelf", "kệ siêu": "shelf", "giá đỡ": "rack", "bục": "podium",
    "bục phát": "podium", "bục trưng": "display stand", "thảm": "carpet", "gối": "pillow", "gương": "mirror",
    "chiếu": "mat", "tranh": "painting", "bức tranh": "painting", "ảnh": "photo", "khung hình": "picture frame",
    "đèn": "lamp", "đèn lồng": "lantern", "dải đèn": "string lights", "hàng đèn": "lights", "đèn trần": "ceiling light",
    "đèn led": "led light", "đèn chiếu": "spotlight", "đèn treo": "pendant lamp", "đèn trang": "decorative light",
    "đèn tre": "lantern", "nến": "candle", "quạt": "fan", "quạt điện": "electric fan", "quạt trần": "ceiling fan",
    "máy lạnh": "air conditioner", "tivi": "television", "màn hình": "screen", "máy tính": "computer",
    "laptop": "laptop", "điện thoại": "phone", "micro": "microphone", "loa": "speaker", "máy in": "printer",
    "máy quay": "camera", "guitar": "guitar", "cờ": "flag", "lá cờ": "flag", "hàng cờ": "flags", "dải cờ": "flags",
    "cờ việt": "flag", "dải dây": "string", "dải băng": "ribbon", "sách": "book", "báo": "newspaper", "sổ": "notebook",
    "bút": "pen", "giấy": "paper", "khăn giấy": "tissue", "hộp": "box", "hộp giấy": "cardboard box",
    "hộp quà": "gift box", "hộp bánh": "box", "hộp sữa": "milk carton", "thùng": "box", "thùng giấy": "cardboard box",
    "thùng nhựa": "plastic bin", "thùng hàng": "box", "bao": "sack", "bao tải": "sack", "bao gạo": "rice sack",
    "bao bì": "package", "gói": "package", "bịch": "bag", "giỏ": "basket", "giỏ mua": "shopping basket",
    "giỏ hàng": "shopping basket", "giỏ nhựa": "basket", "rổ": "basket", "cân": "scale", "bát": "bowl",
    "tô phở": "bowl", "tô mì": "bowl", "chén": "bowl", "đĩa": "plate", "cốc": "cup", "ly": "glass", "chai": "bottle",
    "chai nước": "bottle", "chai dầu": "bottle", "bình nước": "water bottle", "bình": "vase", "bình gốm": "vase",
    "bình hoa": "vase", "lọ": "jar", "bình trà": "teapot", "lon": "can", "nồi": "pot", "chảo": "pan",
    "chảo nấu": "pan", "thìa": "spoon", "muỗng": "spoon", "đũa": "chopsticks", "dao": "knife", "chậu": "pot",
    "bồn rửa": "sink", "vòi nước": "faucet", "vòi phun": "fountain", "bình chữa": "fire extinguisher",
    "bình xịt": "spray bottle", "maniqui": "mannequin", "maniquí": "mannequin", "chổi": "broom", "lưới": "net",
    "dây thừng": "rope", "bóng": "ball", "quả": "fruit", "cam": "orange", "chuối": "banana", "dưa hấu": "watermelon",
    "dưa chuột": "cucumber", "cà chua": "tomato", "ớt": "chili pepper", "bắp": "corn", "bắp cải": "cabbage",
    "rau": "vegetables", "loại rau": "vegetables", "thịt": "meat", "miếng thịt": "meat", "bánh": "cake",
    "bánh mì": "bread", "bánh ngọt": "cake", "buồm": "sail", "bánh lái": "steering wheel", "cọc neo": "mooring post",
    "mái chèo": "oar", "sản phẩm": "product", "hộp sản": "product box", "hộp thực": "food box",
}


def key_of(head_noun: str) -> str:
    s = norm_tone(" ".join(str(head_noun).lower().split()))
    stripped = True
    while stripped:
        stripped = False
        for q in QUANTIFIERS:
            if s.startswith(q + " "):
                s, stripped = s[len(q) + 1:], True
    return s


def coco_terms() -> dict[str, str]:
    raw = json.loads((ROOT / "data" / "coco_probe" / "coco80_vi.json").read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for cls, terms in raw.items():
        if cls.startswith("_"):
            continue
        for t in terms:
            if isinstance(t, str) and not t.startswith("_rui_ro"):
                out.setdefault(norm_tone(t.lower()), cls)
    return out


def map_noun(head_noun: str, table: dict[str, str], coco: dict[str, str]) -> tuple[str | None, str]:
    """(English prompt or None, rule that fired). The unstripped form is tried first, so a noun
    that starts with a number word (`ba lô` = backpack) is not read as a quantifier."""
    for key in dict.fromkeys((norm_tone(" ".join(str(head_noun).lower().split())), key_of(head_noun))):
        canon = canonical(key)
        for rule, lookup, k in (("table", table, key), ("table_canonical", table, canon),
                                ("coco80", coco, key), ("coco80_canonical", coco, canon)):
            if k and k in lookup:
                return lookup[k], rule
    return None, "unmapped"


#: Map entries whose Vietnamese noun has a second common reading (CC-198 W5). Kept; disclosed.
AMBIGUOUS = {"bóng": "ball / shadow / light bulb", "quả": "fruit / any round thing", "xe": "any vehicle",
             "biển": "sea / sign (KTVIC often means a sign)", "cam": "orange (fruit) / orange (colour)"}

#: Why a table prompt differs from the coco80_vi.json class for the same noun.
COCO80_DIFF_REASON = ("Open-vocabulary prompts name the noun itself: gendered/age person nouns keep man/woman/"
                      "child/girl/baby instead of COCO 'person' (the gender ceiling still caps them); plain English "
                      "replaces COCO class labels (table, phone, television, ball, bottle, ship, computer).")


def lexicon_coverage(mentions: Counter, table: dict[str, str], coco: dict[str, str]) -> dict:
    """The 113 CHAIR-vi lexicon nouns: resolvable by the rules, and as head-noun types in the records (after key_of)."""
    from rescap.vi.lexicon import NOUN_CLASSIFIER

    lex = {norm_tone(n) for n in NOUN_CLASSIFIER}
    by_key: Counter[str] = Counter()
    for noun, n in mentions.items():
        by_key[key_of(noun)] += n
    resolvable = {n for n in lex if map_noun(n, table, coco)[0]}
    present = {n for n in lex if by_key[n]}
    return {"n_lexicon": len(lex), "resolvable_by_rules": len(resolvable),
            "present_mapped": len(present & resolvable), "present_unmapped": sorted(present - resolvable),
            "absent_as_head_noun": len(lex - present)}


def coco80_crosscheck(table: dict[str, str], coco: dict[str, str]) -> dict:
    """Both ways: lexicon nouns that are coco80_vi terms, and every coco80_vi term through the map."""
    from rescap.vi.lexicon import NOUN_CLASSIFIER

    differ = {}
    agree = only_coco = 0
    for term, cls in sorted(coco.items()):
        prompt, rule = map_noun(term, table, coco)
        if rule.startswith("coco80"):
            only_coco += 1
        elif prompt == cls:
            agree += 1
        else:
            differ[term] = [prompt, cls]
    lex_in_coco = sorted(norm_tone(n) for n in NOUN_CLASSIFIER if norm_tone(n) in coco)
    return {"coco80_terms": len(coco), "table_agrees": agree, "table_differs": differ,
            "resolved_by_coco80_rule": only_coco, "lexicon_nouns_in_coco80": len(lex_in_coco),
            "lexicon_nouns_differing": sorted(t for t in lex_in_coco if t in differ),
            "differ_reason": COCO80_DIFF_REASON, "ambiguous_entries": AMBIGUOUS}


def build(records_dir: Path) -> dict:
    table = {norm_tone(k): v for k, v in TABLE.items()}
    coco = coco_terms()
    mentions: Counter[str] = Counter()
    for f in sorted(records_dir.glob("*.json")):
        rec = json.loads(f.read_text(encoding="utf-8"))
        for e in rec.get("entities") or []:
            mentions[str(e.get("category_vi") or "")] += 1
    mapping, rules, unmapped = {}, Counter(), {}
    for noun, n in mentions.most_common():
        prompt, rule = map_noun(noun, table, coco)
        rules[rule] += n
        if prompt is None:
            unmapped[noun] = n
        else:
            mapping[noun] = prompt
    total = sum(mentions.values())
    return {
        "lexicon_coverage": lexicon_coverage(mentions, table, coco),
        "coco80_crosscheck": coco80_crosscheck(table, coco),
        "_doc": "VSPS H1 Vietnamese head noun -> English detector prompt. Built by build_map.py; "
                "a prompt dictionary (method component), not evidence. Unmapped nouns get detector vote UNCERTAIN.",
        "table_sha256": hashlib.sha256(json.dumps(TABLE, ensure_ascii=False, sort_keys=True).encode()).hexdigest(),
        "n_noun_types": len(mentions), "n_mentions": total,
        "n_unmapped_types": len(unmapped), "unmapped_mention_share": round(sum(unmapped.values()) / total, 4),
        "mentions_by_rule": dict(rules),
        "map": mapping, "unmapped": unmapped,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--records", required=True, type=Path)
    ap.add_argument("--out", type=Path, default=Path(__file__).with_name("vi_en_map.json"))
    args = ap.parse_args()
    out = build(args.records)
    if not out["n_mentions"]:
        raise SystemExit(f"no entities under {args.records}")
    args.out.write_text(json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{out['n_noun_types']} noun types, {out['n_mentions']} mentions; unmapped "
          f"{out['n_unmapped_types']} types = {100 * out['unmapped_mention_share']:.1f}% of mentions -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
