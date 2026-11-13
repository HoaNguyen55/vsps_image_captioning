#!/usr/bin/env python
"""Build the blind pairwise-preference assignment of Paper B (B_PREF_LABELLING_PLAN_v1_1.md §2.4, §3.1, §9).

Unit: one KTVIC test image and two display-normalised captions of it from two own -short files. Strata P, U, C come
from the stage-1 table PAIR_CANDIDATES.json (file names and d values, no text); this script re-checks each candidate and
stops on any disagreement, then draws with seed 20261112 in the order written in PAIR_READ_PACKAGE.md.

Outputs (in --out, never under /mnt or ~/vsps_labels/, never overwritten): assignment.json and practice.json (served;
caption text, no file name, stratum, score or role), key.json (private), ITEMS_MANIFEST.tsv (qid, image id), BUILD.json
(counts, sha256 of every input and output). stdout carries counts only.

qid = sha256(SALT|SEED|part|image|a|b)[:12] with SALT = secrets.token_hex(16) made at build time and kept only in
key.json (plan addendum B_PREF_PLAN_ADDENDUM_SALT_v1.md; CC-361 D15). Image files are not opened here (the rented host
has no KTVIC images); pair_server.py checks on the laptop that every served image exists (CC-361 D14).

    python3 -I -B tools/obj_rater/build_pairs.py --out ~/vsps_labels_b/b_pref --candidates PAIR_CANDIDATES.json \
        --candidates-sha <sha256 of PAIR_CANDIDATES.json from its pin line> --preds-dir data/results \
        --test-json data/datasets/ktvic/test_data.json
    python3 -I -B tools/obj_rater/build_pairs.py --selftest      # synthetic fixtures in a temp dir only
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import math
import random
import re
import secrets
import shutil
import sys
import tempfile
import unicodedata
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from pair_server import BUILD_RECORD, INSTRUCTIONS_VI_SHA256, check_start, instructions_block, refuse_dir, sha  # noqa: E402

SEED, EPS = 20261112, 10.0
FIX_SALT = "5a17" * 8  # the self-test's fixed salt (equal fixture shas across two processes); never used on real files
QUOTA = {"P": 100, "U": 160, "C": 40}  # CC-350 N2
N_REPEAT, MIN_GAP, N_PRACTICE = 30, 100, 8
WS = "\t\n\x0b\x0c\r \x85\xa0 " + "".join(map(chr, range(0x2000, 0x200B))) + "    　"  # 25
FINAL = ".!?…;:,"  # B_KAPPA §2.2 final-punctuation set
WS_RUN = re.compile("[" + WS + "]+")
IMG_NAME = re.compile(r"[0-9]{11}\.(jpg|jpeg|png)")
LABELS = {"A": "Chú thích A tốt hơn", "B": "Chú thích B tốt hơn", "T": "Ngang nhau", "X": "Không đánh giá được"}


def display(t: str) -> str:
    """Plan §3.1: N (NFC, '_' to space, whitespace runs to one space, trim), final run stripped, first letter upper."""
    t = WS_RUN.sub(" ", unicodedata.normalize("NFC", t).replace("_", " ")).strip(WS)
    t = t.rstrip(FINAL + WS)
    return t[0].upper() + t[1:] if t and t[0].isalpha() else t


def tok_diff(x: str, y: str) -> int:
    cx, cy = Counter(x.lower().split(" ")), Counter(y.lower().split(" "))
    return sum(((cx - cy) + (cy - cx)).values())


def stratum_of(c: dict) -> str | None:
    syl, word, pk = c["d_syl"], c["d_word"], c["d_pk"]

    def flip(x: float, y: float) -> bool:
        return abs(x) >= EPS and abs(y) >= EPS and (x > 0) != (y > 0)

    p, u = flip(pk, word), flip(syl, word)
    if p != u:
        return "P" if p else "U"
    if all(abs(x) >= EPS for x in (syl, word, pk)) and len({x > 0 for x in (syl, word, pk)}) == 1:
        return "C"
    return None


def qid(salt: str, part: str, i: str, a: str, b: str) -> str:
    """Plan §9 qid pattern with the per-build secret salt in front (addendum B_PREF_PLAN_ADDENDUM_SALT_v1; D15)."""
    return hashlib.sha256(f"{salt}|{SEED}|{part}|{i}|{a}|{b}".encode()).hexdigest()[:12]


CAND_FIELDS = {"a", "b", "stratum", "d_syl", "d_word", "d_pk"}  # one candidate as stage 1 writes it (CC-361 D3)


def load_inputs(cand_path: Path, preds_dir: Path, test_json: Path, cand_sha: str) -> tuple[dict, dict, dict, dict]:
    if sha(cand_path) != cand_sha:  # the sha256 logged at the stage pin (CC-361 NB9)
        raise SystemExit("STOP: PAIR_CANDIDATES.json differs from the sha256 passed (--candidates-sha)")
    cand = json.loads(cand_path.read_text(encoding="utf-8"))
    if cand.get("epsilon") != EPS or set(cand.get("eligible_images", ())) != set(QUOTA) or not isinstance(cand.get("images"), dict):
        raise SystemExit("STOP: PAIR_CANDIDATES.json is not {epsilon: 10.0, eligible_images, images} (CC-361 D3)")
    if any(set(c) != CAND_FIELDS for cs in cand["images"].values() for c in cs):
        raise SystemExit("STOP: a candidate is not {a, b, stratum, d_syl, d_word, d_pk} (CC-361 D3)")
    test = json.loads(test_json.read_text(encoding="utf-8"))
    fname = {str(im["id"]): im["filename"] for im in test["images"]}  # 'annotations' is never read
    names = sorted({c[k] for cs in cand["images"].values() for c in cs for k in ("a", "b")})
    preds, in_sha = {}, {cand_path.name: sha(cand_path), test_json.name: sha(test_json)}
    for n in names:
        if not re.fullmatch(r"[A-Za-z0-9_.]+(-[A-Za-z0-9_.]+)*-short", n):
            raise SystemExit("STOP: a candidate names a file that is not an own -short file")
        f = preds_dir / f"{n}.preds.json"
        preds[n] = {str(k): (v[0] if isinstance(v, list) else v) or "" for k, v in json.loads(f.read_text(encoding="utf-8")).items()}
        in_sha[f.name] = sha(f)
    cands = {}
    for i, cs in cand["images"].items():
        if not (i.isdigit() and i in fname and IMG_NAME.fullmatch(fname[i])):
            raise SystemExit("STOP: a candidate image is not a KTVIC test image named [0-9]{11}.(jpg|jpeg|png)")
        seen = set()
        for c in cs:
            pair = frozenset((c["a"], c["b"]))
            if len(pair) != 2 or pair in seen or c["stratum"] not in QUOTA or stratum_of(c) != c["stratum"]:
                raise SystemExit("STOP: a candidate repeats, pairs a file with itself, or its stratum disagrees with its d values")
            seen.add(pair)
            ta, tb = display(preds[c["a"]].get(i, "")), display(preds[c["b"]].get(i, ""))
            if not (ta and tb and tok_diff(ta, tb) >= 2):
                raise SystemExit("STOP: a candidate has an empty display text or differs in fewer than 2 tokens")
        cands[i] = sorted(cs, key=lambda c: (c["a"], c["b"]))
    return cands, preds, fname, in_sha


def build(out: Path, cand_path: Path, preds_dir: Path, test_json: Path, cand_sha: str, salt: str | None = None) -> dict:
    """salt: None on real files (a fresh secret); the self-tests inject a fixed one."""
    refuse_dir(out)
    if out.exists():
        raise SystemExit("STOP: refusing to overwrite an existing --out")
    salt = salt or secrets.token_hex(16)
    cands, preds, fname, in_sha = load_inputs(cand_path, preds_dir, test_json, cand_sha)
    in_sha["build_pairs.py"] = sha(Path(__file__))
    rng = random.Random(SEED)
    elig = {s: sorted((i for i, cs in cands.items() if any(c["stratum"] == s for c in cs)), key=int) for s in QUOTA}
    drawn, pool_n, used = {}, {}, set()
    for s in QUOTA:  # step 3: P, then U, then C, each from the images not yet drawn
        pool = [i for i in elig[s] if i not in used]
        pool_n[s] = len(pool)
        drawn[s] = sorted(rng.sample(pool, min(QUOTA[s], len(pool))), key=int)
        used |= set(drawn[s])
    pairs = [(s, i, rng.choice([c for c in cands[i] if c["stratum"] == s])) for s in QUOTA for i in drawn[s]]  # step 4
    main = [{"s": s, "i": i, "c": c, "a_left": rng.random() < 0.5, "part": "main"} for s, i, c in pairs]  # step 6
    rng.shuffle(main)  # step 7
    pool = main[:max(0, len(main) - MIN_GAP + 1)]  # step 8: only a first showing that can be followed 100 screens later
    seq = list(main)
    for m in rng.sample(pool, min(N_REPEAT, len(pool))):
        f = next(k for k, x in enumerate(seq) if x is m)
        seq.insert(rng.randint(f + MIN_GAP, len(seq)), {**m, "a_left": not m["a_left"], "part": "repeat"})
    p_pool = sorted((i for i, cs in cands.items() if cs and i not in used), key=int)  # step 9
    practice = []
    for i in sorted(rng.sample(p_pool, min(N_PRACTICE, len(p_pool))), key=int):
        c = rng.choice(cands[i])
        practice.append({"s": c["stratum"], "i": i, "c": c, "a_left": rng.random() < 0.5, "part": "practice"})

    key = {}

    def screen(x: dict) -> dict:
        i, c = x["i"], x["c"]
        left, right = (c["a"], c["b"]) if x["a_left"] else (c["b"], c["a"])
        q = qid(salt, x["part"], i, c["a"], c["b"])
        if q in key:
            raise SystemExit("STOP: qid collision")
        key[q] = {"image": i, "part": x["part"], "stratum": x["s"], "a": c["a"], "b": c["b"], "file_left": left,
                  "file_right": right, "d_syl": c["d_syl"], "d_word": c["d_word"], "d_pk": c["d_pk"],
                  "repeat_of": qid(salt, "main", i, c["a"], c["b"]) if x["part"] == "repeat" else None}
        return {"sid": q, "image": f"images/{fname[i]}",
                "q": [{"qid": q, "a": display(preds[left][i]), "b": display(preds[right][i])}]}

    screens, p_screens = [screen(x) for x in seq], [screen(x) for x in practice]
    meta = {"name": "b_pref", "seed": SEED, "labels": LABELS, "n_screens": len(screens)}
    out.mkdir(parents=True)
    files = {"assignment.json": {"meta": meta, "screens": screens},
             "practice.json": {"meta": {**meta, "name": "b_pref_practice", "n_screens": len(p_screens)}, "screens": p_screens},
             "key.json": {"salt": salt, "items": key}}  # the salt lives only here (committed after the closing line)
    for name, obj in files.items():
        (out / name).write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=1), encoding="utf-8")
    (out / "ITEMS_MANIFEST.tsv").write_text("qid\timage_id\n" + "".join(f"{q}\t{v['image']}\n" for q, v in sorted(key.items())),
                                            encoding="utf-8")
    counts = {"eligible_images": {s: len(elig[s]) for s in QUOTA}, "pool_after_earlier_draws": pool_n,
              "drawn": {s: len(drawn[s]) for s in QUOTA}, "shortfall": {s: max(0, QUOTA[s] - len(drawn[s])) for s in QUOTA},
              "main_pairs": len(main), "repeats": len(seq) - len(main), "repeat_pool": len(pool), "screens": len(seq),
              "practice_screens": len(practice), "main_a_left": sum(m["a_left"] for m in main)}
    rec = {"counts": counts, "inputs_sha256": in_sha,
           "outputs_sha256": {n: sha(out / n) for n in (*files, "ITEMS_MANIFEST.tsv")}}
    (out / BUILD_RECORD).write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    return rec


# ------------------------------------------------------------------------------------------- selftest (synthetic)

SYS = [f"s{k}_s42-short" for k in range(1, 7)]
D = {"P": (12.0, 20.0, -15.0), "U": (-20.0, 15.0, 11.0), "C": (12.0, 13.0, 14.0)}  # (d_syl, d_word, d_pk)


def _fixture(fx: Path) -> dict:
    ids = [str(k) for k in range(1000, 1400)]
    ext = {i: ("png" if int(i) % 10 == 0 else "jpeg" if int(i) % 10 == 1 else "jpg") for i in ids}
    fname = {i: f"{int(i):011d}.{ext[i]}" for i in ids}
    (fx / "ds" / "images").mkdir(parents=True)
    for i in ids:
        (fx / "ds" / "images" / fname[i]).write_bytes(b"")
    (fx / "ds" / "test_data.json").write_text(json.dumps({"images": [{"id": int(i), "filename": fname[i]} for i in ids],
                                                          "annotations": [{"image_id": int(i), "caption": "SENTINELREF"} for i in ids]}))
    (fx / "preds").mkdir()
    for n in SYS:
        cap = {i: f"capword{n[1]} con_mèo  đen ngồi{i}{n[1]} ." for i in ids}
        (fx / "preds" / f"{n}.preds.json").write_text(json.dumps(cap, ensure_ascii=False), encoding="utf-8")
    ranges = {"P": range(1000, 1120), "U": range(1100, 1300), "C": range(1290, 1320)}  # overlaps; C short of 40
    files = {"P": [(0, 1), (2, 3)], "U": [(0, 2), (1, 3)], "C": [(4, 5)]}
    cand: dict[str, list] = {str(k): [] for k in range(1320, 1400)}  # listed with no candidate: never drawn
    for s, r in ranges.items():
        for k in r:
            for a, b in files[s]:
                cand.setdefault(str(k), []).append({"a": SYS[a], "b": SYS[b], "stratum": s,
                                                    **dict(zip(("d_syl", "d_word", "d_pk"), D[s]))})
    _write_cand(fx / "cand.json", cand)
    return {"fname": fname, "cand": cand}


def _write_cand(p: Path, cand: dict) -> str:
    elig = {s: sum(any(c["stratum"] == s for c in cs) for cs in cand.values()) for s in QUOTA}
    p.write_text(json.dumps({"epsilon": EPS, "eligible_images": elig, "images": cand}), encoding="utf-8")
    return sha(p)


def selftest() -> int:
    n_ok = 0

    def check(cond: bool, what: str) -> None:
        nonlocal n_ok
        if not cond:
            raise SystemExit(f"SELFTEST FAIL: {what}")
        n_ok += 1
        print(f"ok {n_ok:2d} {what}")

    def stops(fn) -> bool:
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                fn()
        except SystemExit as e:
            return str(e).startswith("STOP")
        except Exception:  # noqa: BLE001  a crash is not a refusal: the check FAILs by name (round 2b, mutant R5)
            return False
        return False

    check(display("  con_mèo   đen ngồi .!… ") == "Con mèo đen ngồi" and display("đi?") == "Đi"
          and display(unicodedata.normalize("NFD", "hoà.")) == "Hoà" and display("\"x\".") == "\"x\""
          and display("a,b. c") == "A,b. c" and display(" .. ") == "" and display("\x1cx") == "\x1cx",
          "display normalisation on toy strings (NFC, '_', 25 White_Space only, final run, first letter)")
    check(stratum_of(dict(zip(("d_syl", "d_word", "d_pk"), D["P"]))) == "P" and stratum_of(dict(zip(("d_syl", "d_word", "d_pk"), D["U"]))) == "U"
          and stratum_of(dict(zip(("d_syl", "d_word", "d_pk"), D["C"]))) == "C"
          and stratum_of({"d_syl": -12.0, "d_word": 20.0, "d_pk": -15.0}) is None
          and stratum_of({"d_syl": 12.0, "d_word": 9.9, "d_pk": -15.0}) is None, "strata from d values at epsilon 10 (P, U, C, both flips, below margin)")

    with tempfile.TemporaryDirectory() as td:
        fx = Path(td)
        F = _fixture(fx)
        args = (fx / "cand.json", fx / "preds", fx / "ds" / "test_data.json", sha(fx / "cand.json"), FIX_SALT)
        check(stops(lambda: build(Path("/mnt/never_b_pref_selftest"), *args)), "refuses an --out under /mnt")
        check(stops(lambda: build(Path.home() / "vsps_labels" / "never_b_pref_selftest", *args)), "refuses an --out under ~/vsps_labels/")
        (fx / "exists").mkdir()
        check(stops(lambda: build(fx / "exists", *args)), "refuses to overwrite an existing --out")

        def bad(mut, tag: str) -> bool:
            c = json.loads(json.dumps(F["cand"]))
            mut(c)
            p = fx / f"cand_{tag}.json"
            h = _write_cand(p, c)
            return stops(lambda: build(fx / f"o_{tag}", p, fx / "preds", fx / "ds" / "test_data.json", h, FIX_SALT)) \
                and not (fx / f"o_{tag}").exists()

        check(bad(lambda c: c["1000"][0].update(stratum="U"), "strat"), "stops when a stratum disagrees with its d values")
        check(bad(lambda c: c["1000"][0].update(b=c["1000"][0]["a"]), "self"), "stops on a file paired with itself")
        check(bad(lambda c: c["1000"][0].update(a="s1_s42-detailed"), "mode"), "stops on a file that is not -short")
        check(bad(lambda c: c.update({"999": c["1000"]}), "img"), "stops on an image outside the test file")
        check(bad(lambda c: c["1000"][0].update(dword=c["1000"][0].pop("d_word")), "field"),
              "stops on a candidate field outside {a, b, stratum, d_syl, d_word, d_pk} (D3)")
        check(stops(lambda: build(fx / "o_sha", *args[:3], "0" * 64, FIX_SALT)),
              "stops when PAIR_CANDIDATES.json differs from --candidates-sha (NB9)")
        (fx / "preds" / f"{SYS[1]}.preds.json").write_text(json.dumps({"1000": "capword1 con mèo đen ngồi10001"}), encoding="utf-8")
        check(stops(lambda: build(fx / "o_tok", *args)), "stops when display texts differ in fewer than 2 tokens")
        _fixture(fx / "re")
        shutil.rmtree(fx / "re" / "ds" / "images")  # D14: the build host has no images; the build must not need them
        args = (fx / "re" / "cand.json", fx / "re" / "preds", fx / "re" / "ds" / "test_data.json", sha(fx / "re" / "cand.json"))

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rec = build(fx / "o1", *args, FIX_SALT)
            print(json.dumps(rec["counts"]))
        o1 = fx / "o1"
        kj = json.loads((o1 / "key.json").read_text(encoding="utf-8"))
        check(set(kj) == {"salt", "items"} and kj["salt"] == FIX_SALT, "key.json = {salt, items}; the injected salt (D15)")
        key = kj["items"]
        asg = json.loads((o1 / "assignment.json").read_text(encoding="utf-8"))
        prac = json.loads((o1 / "practice.json").read_text(encoding="utf-8"))
        c = rec["counts"]
        main = {q: v for q, v in key.items() if v["part"] == "main"}
        by_s = Counter(v["stratum"] for v in main.values())
        check(by_s == Counter(P=100, U=160, C=c["pool_after_earlier_draws"]["C"]) and c["shortfall"]["C"] == 40 - by_s["C"] > 0
              and c["shortfall"]["P"] == c["shortfall"]["U"] == 0, f"quotas P 100, U 160; C shortfall takes all ({dict(by_s)})")
        imgs = [v["image"] for v in main.values()] + [v["image"] for v in key.values() if v["part"] == "practice"]
        check(len(imgs) == len(set(imgs)), "one pair per image; images disjoint across strata and practice")
        check(all(any(x["stratum"] == v["stratum"] and {x["a"], x["b"]} == {v["file_left"], v["file_right"]}
                      for x in F["cand"][v["image"]]) for v in key.values()), "every pair is a candidate of its own stratum")
        n = len(main)
        check(abs(c["main_a_left"] - n / 2) <= 3 * math.sqrt(n) / 2 and c["main_a_left"] == sum(v["file_left"] == v["a"] for v in main.values()),
              f"left/right balance within 3 sd ({c['main_a_left']}/{n} with file a on the left)")
        pos = {s["sid"]: k for k, s in enumerate(asg["screens"])}
        reps = [v | {"q": q} for q, v in key.items() if v["part"] == "repeat"]
        check(len(reps) == N_REPEAT and all(key[r["repeat_of"]]["file_left"] == r["file_right"] and pos[r["q"]] - pos[r["repeat_of"]] >= MIN_GAP
                                             for r in reps), "30 repeats, sides swapped, each >= 100 screens after its first showing")
        all_q = [q["qid"] for s in asg["screens"] + prac["screens"] for q in s["q"]]
        check(len(all_q) == len(set(all_q)) == len(key) and all(q == qid(FIX_SALT, v["part"], v["image"], v["a"], v["b"])
                                                                for q, v in key.items())
              and all(v["repeat_of"] == qid(FIX_SALT, "main", v["image"], v["a"], v["b"]) for v in key.values() if v["part"] == "repeat")
              and not any(q == hashlib.sha256(f"{SEED}|{v['part']}|{v['image']}|{v['a']}|{v['b']}".encode()).hexdigest()[:12]
                          for q, v in key.items()),
              "qids unique across assignment and practice; qid = sha256(SALT|SEED|part|image|a|b)[:12], never unsalted (D15)")
        served = (o1 / "assignment.json").read_text(encoding="utf-8") + (o1 / "practice.json").read_text(encoding="utf-8")
        check(all(set(s) == {"sid", "image", "q"} and [set(q) for q in s["q"]] == [{"qid", "a", "b"}] for s in asg["screens"] + prac["screens"])
              and set(asg["meta"]) == {"name", "seed", "labels", "n_screens"}
              and not any(t in served for t in ["-short", "s42", "stratum", "d_syl", "d_word", "d_pk", "repeat", "part", "SENTINELREF"]),
              "served files: no file name, stratum, score, role or reference; one q per screen")
        preds = {nm: json.loads((fx / "re" / "preds" / f"{nm}.preds.json").read_text(encoding="utf-8")) for nm in SYS}
        check(all(q["a"] == display(preds[key[q["qid"]]["file_left"]][key[q["qid"]]["image"]])
                  and q["b"] == display(preds[key[q["qid"]]["file_right"]][key[q["qid"]]["image"]])
                  for s in asg["screens"] + prac["screens"] for q in s["q"]), "served captions = display text of the keyed left and right files")
        check(len(prac["screens"]) == N_PRACTICE and {v["image"] for v in key.values() if v["part"] == "practice"}.isdisjoint(
            v["image"] for v in main.values()), "8 practice pairs from images not drawn for the main set")
        paths = [s["image"] for s in asg["screens"] + prac["screens"]]
        check(all(p.startswith("images/") and IMG_NAME.fullmatch(p.split("/")[1]) and p.split("/")[1] in F["fname"].values()
                  for p in paths) and {p.rsplit(".", 1)[1] for p in paths} == {"jpg", "jpeg", "png"},
              "built with no images folder; every image path in the regex and in test_data.json; .jpg, .jpeg, .png drawn (D14)")
        private = buf.getvalue() + "".join((o1 / x).read_text(encoding="utf-8") for x in ("key.json", BUILD_RECORD, "ITEMS_MANIFEST.tsv"))
        check("capword" not in private and "mèo" not in private and "SENTINELREF" not in private,
              "no caption or reference text in key.json, BUILD.json, the manifest or stdout")
        public = served + buf.getvalue() + "".join((o1 / x).read_text(encoding="utf-8") for x in (BUILD_RECORD, "ITEMS_MANIFEST.tsv"))
        check(FIX_SALT not in public, "the salt is only in key.json: not served, not in BUILD.json, the manifest or stdout (D15)")
        man = (o1 / "ITEMS_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()
        check(man[0] == "qid\timage_id" and sorted(man[1:]) == man[1:] and {r.split("\t")[0] for r in man[1:]} == set(key)
              and all(len(r.split("\t")) == 2 for r in man), "ITEMS_MANIFEST.tsv: qid and image id only, every qid")
        check(rec["outputs_sha256"] == {x: sha(o1 / x) for x in rec["outputs_sha256"]} and len(rec["outputs_sha256"]) == 4
              and all(f"{nm}.preds.json" in rec["inputs_sha256"] for nm in SYS), "BUILD.json holds every input and output sha256")
        with contextlib.redirect_stdout(io.StringIO()):
            build(fx / "o2", *args, FIX_SALT)
            build(fx / "o3", *args)
            build(fx / "o4", *args)
        check(sorted(x.name for x in o1.iterdir()) == sorted(x.name for x in (fx / "o2").iterdir())
              and all((o1 / x.name).read_bytes() == (fx / "o2" / x.name).read_bytes() for x in o1.iterdir()),
              "determinism: two builds with the same salt byte-equal")
        k3, k4 = (json.loads((fx / o / "key.json").read_text(encoding="utf-8")) for o in ("o3", "o4"))
        check(len(k3["salt"]) == 32 and k3["salt"] != k4["salt"] and set(k3["items"]).isdisjoint(k4["items"]),
              "with no injected salt each build draws a fresh 128-bit secret (D15)")

        # pair_server, in process (no socket): the laptop side of the D14 check, the D16 instruction block, NB5 refusals
        _fixture(fx / "srv")
        imgs_dir = fx / "srv" / "ds" / "images"
        start = lambda d, port=8792, who="PI", root=fx: check_start(d, port, imgs_dir, who, root)  # noqa: E731
        check(not stops(lambda: start(o1)), "pair_server starts on the built fixture with the real pair.html (D16, D14, NB5)")
        served_types, page = start(o1)
        check(served_types[F["fname"]["1000"]] == "image/png" and served_types[F["fname"]["1001"]] == "image/jpeg"
              and served_types[F["fname"]["1002"]] == "image/jpeg", "pair_server: .png as image/png, .jpeg/.jpg as image/jpeg")
        check(page == (HERE / "pair.html").read_bytes() and instructions_block(page) is not None
              and hashlib.sha256(instructions_block(page)).hexdigest() == INSTRUCTIONS_VI_SHA256,
              "pair.html carries the registered Vietnamese block byte for byte (45d59b54; D16)")
        for old, new in (("Trước hết", "Trước hét"), ("20 giây", "20 giay")):  # one character each: item 2, line 7
            alt = fx / "alt.html"
            alt.write_bytes(page.replace(old.encode(), new.encode(), 1))
            check(page.count(old.encode()) == 1 and stops(lambda: check_start(o1, 8792, imgs_dir, "PI", fx, alt)),
                  f"pair_server refuses a page whose instruction block differs by one character ('{new}'; D16)")
        check(stops(lambda: start(o1, 8790)) and stops(lambda: start(o1, 8791)), "pair_server refuses ports 8790 and 8791")
        check(stops(lambda: start(Path("/mnt/never_b_pref"), root=Path("/mnt")))
              and stops(lambda: start(Path.home() / "vsps_labels" / "never_b_pref", root=Path.home()))
              and stops(lambda: start(o1, root=fx / "elsewhere")),
              "pair_server refuses a --dir under /mnt or ~/vsps_labels/, or outside ~/vsps_labels_b/ (NB5)")
        check(stops(lambda: start(o1, who="R3")) and stops(lambda: start(o1, who="pi")), "pair_server: --annotator PI or R2 only (NB5)")
        gone = imgs_dir / F["fname"][next(v["image"] for v in key.values())]
        gone.rename(gone.with_suffix(".moved"))
        check(stops(lambda: start(o1)), "pair_server refuses to start when a served image is missing on the laptop (D14)")
        gone.with_suffix(".moved").rename(gone)
        (o1 / "key.json").write_bytes((o1 / "key.json").read_bytes() + b"\n")
        check(stops(lambda: start(o1)), "pair_server refuses to start when key.json differs from BUILD.json")
        for fname in ("assignment.json", "key.json"):  # compare across two processes
            print(f"fixture sha256 {fname} {sha(fx / 'o2' / fname)}")
    print(f"SELFTEST PASS {n_ok}/{n_ok}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--candidates", help="PAIR_CANDIDATES.json from FE-CERT stage 1")
    ap.add_argument("--candidates-sha", help="its sha256 as logged on the stage pin line (CC-361 NB9)")
    ap.add_argument("--preds-dir", help="folder holding <name>.preds.json of the own -short files")
    ap.add_argument("--test-json", help="data/datasets/ktvic/test_data.json (no images needed here; CC-361 D14)")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.out and a.candidates and a.candidates_sha and a.preds_dir and a.test_json):
        ap.error("--out, --candidates, --candidates-sha, --preds-dir and --test-json are required")
    rec = build(Path(a.out).expanduser(), Path(a.candidates), Path(a.preds_dir), Path(a.test_json), a.candidates_sha)
    print(json.dumps(rec["counts"], ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
