#!/usr/bin/env python3
"""Paper A dev assumption checks D1-D5: manuscript/prereg/2026-11-06_a_dchecks/A_DCHECKS_PLAN_v3.md (03c0b975),
CC-266r3 (GO 87, binding readings 6a-6c, N1''-N4''), PI-1106c. Post hoc, descriptive, development data only.

  selftest [--out F]  synthetic data only; asserts the code pins only        -> data/results/a_dchecks/selftest.json
  dryrun              asserts every input sha, prints the planned work and the plan §6 CPU estimate; computes nothing,
                      writes nothing
  freeze              S0.1-2: id lists, the pinned builder run unchanged (sha bd362951)  -> data/results/a_dchecks/freeze/
  gate                S0.3-5: anchors, kernel gate, S0.4 record; computes no D statistic -> data/results/a_dchecks/gate.json
  run                 refuses unless this script and the plan equal their HEAD blobs; D1, D5, D2, D3, D4(b), D4(a)
                      under the 6 CPU-h / 4 h wall cap                       -> data/results/a_dchecks/dchecks_result.json

  OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2 nice -n 15 ~/.venvs/vsps_h1/bin/python -I -B <this file> run

Every subcommand asserts its input shas (PINS, full sha256) before it imports or reads anything, and FAULTs (exit 2)
otherwise. Outputs hold counts, rates, slopes, ids (freeze only) and shas, never caption text; nothing is printed from a
caption.

Fixed readings (the code read rules on them):
- Linear metrics are P, R, micro-F1 (MU) and caption CHAIR (CH). Instance CHAIR is omitted: every matcher returns
  class sets, no repeat counts (plan §2). So m_lin = sum over cells of 4 x (systems + 1).
- D4(a) family sizes (CC-266r3 6a, N1''): m = evaluable cells x 3 T statistics (mixed F1, P, R); m_sd = evaluable
  cells (single-draw two-sided KS at 0.05/m_sd). W-50 arm U counts once (compound rule). Both are written to S0.
- D3 one-sided bootstrap p for H0: de <= 0 is p = (1 + #{de* <= 0}) / (B + 1); the upper bound is the
  100 (1 - 0.05/m) percentile of de*. FAIL = Holm (alpha 0.05 over the m evaluable increments) rejects; it takes
  precedence. PASS = not FAIL and upper <= 0.01. UNDERPOWERED = the rest (CC-266r3 6b, N2'').
- D4(a) detectable size at m = 48, S = 100 is 0.073 (plan l.210 says 0.072; erratum N3'').
- D4(a) applies the rate bound and the one-sided KS each at 0.05/m per T statistic (2m tests); both are reported; the
  family-wise false-FAIL bound is <= 0.10 (N4'').
- D5 uses arm L's C_i (label gold) for the gold share; the all-mention share needs no gold (the plan names no arm).
- Images per set x family: the score_g2b clean rule over every system of the family (is_clean, caption present).
- p50.draw is called on all ids of a set in id order (as p50x does); statistics use the scored images only.
- A D1 linear FAIL and a D4(a) single-draw FAIL are implementation faults: the run stops (later checks NOT_RUN).
- D4(b) box weight a_c = largest bbox w*h of class c over the image area, floored at 1e-9 (a zero-area box).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from statistics import NormalDist

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PLAN = "manuscript/prereg/2026-11-06_a_dchecks/A_DCHECKS_PLAN_v3.md"
OUT = "data/results/a_dchecks"
SELF = "scripts/a_dchecks/a_dchecks.py"

# ------------------------------------------------------------------------------------------------ constants (plan §2-§6)
BASE_SEED = 20261106
OFF = {"check": {"D1": 1000, "D2": 2000, "D3": 3000, "D4b": 4000, "D4a": 5000, "D5": 6000, "W50": 7000,
                 "calib": 8000, "speed": 9000, "gate": 10000},
       "set": {"coco": 100, "xm": 200, "uit": 300}, "fam": {"F1": 10, "F2": 20}, "arm": {"L": 1, "U": 2},
       "world": {"real": 0, "W50": 50000}}
B_D1, B_BOOT, B_NULL, N_W, W_BATCHES = 10_000, 2_000, 1_000, 10_000, 10
S_D4A, S_D4A_LOW, S_D4B, N_CALIB = 200, 100, 100, 5
SESOI, D2_HALF, D1_SLOPE_TOL, D5_MIN, ALPHA, BUDGETS, MIN_N5 = 0.01, 0.5, 0.5, 0.80, 0.05, (2, 3, 5), 100
CAP_CPU_S, CAP_WALL_S = 6 * 3600, 4 * 3600
ORDER = ("D1", "D5", "D2", "D3", "D4b", "D4a")
LINEAR = ("P", "R", "MU", "CH")
T_STATS = ("F", "P", "R")
N_SIMREFS = 50
CHUNK = 6_000_000  # elements of the (replicates x draws x slots) block per kernel call
F2_SCORED = {"xm": 537, "uit": 209}  # plan §1 table
RESULT_READ_NOTES = (  # CC-271 N10 (rulings 2, 3; CC-266r3 N3'', N4'')
    "Instance CHAIR omitted: the matchers return class sets (instance CHAIR = 1 - P); 4 linear metrics, m_lin = 280 "
    "on the plan layout.",
    "D5 shares use arm L's C_i (label gold); the all-mention share needs no gold.",
    "Erratum N3'': D4(a) detectable size at m = 48, S = 100 is 0.073 (plan l.210 says 0.072).",
    "N4'': D4(a) applies the rate bound and the KS each at 0.05/m per T statistic (2m tests); family-wise false-FAIL "
    "bound <= 0.10.")
OUTPUTS_BEYOND_S6 = ("data/results/a_dchecks/gate_anchors/ (r4_repro.json, g2b_selfcheck.json)",
                     "data/results/a_dchecks/run_record/STARTED.json",
                     "data/results/a_dchecks/freeze/freeze.failed_<utc>.json (only after a failed freeze)")  # CC-271 N6

C5, TF, VCD = "data/results/coco5000/", "data/results/coco_transfer_full5000/", "data/results/coco5000_vcd/"
G2 = ".session_backup/2026-10-20/g2b_score/outputs/g2b_q3_"
FAMILIES = {
    ("coco", "F1"): [C5 + f"{m}.shard0of1.jsonl" for m in ("distill-detailed", "distill-short", "zeroshot-detailed",
                                                         "zeroshot-short")]
    + [TF + f"{m}.shard0of1.jsonl" for m in ("fuse2_s42-detailed", "fuse2_s42-short", "p1_s43-detailed", "p1_s43-short")]
    + [VCD + "zeroshot-detailed.shard0of1.jsonl"],
    ("xm", "F1"): [f"data/results/xm3600/xm3600_{m}-{q}.preds.json" for m in ("fuse2_s42", "p1_s43", "zeroshot")
                   for q in ("detailed", "short")],
    ("xm", "F2"): [G2 + f"xm600-{q}-{t}.preds.json" for q in ("short", "detailed") for t in ("T0", "T05", "T08")],
    ("uit", "F1"): [f"data/results/uitviic/uitviic_{m}-{q}.preds.json" for m in ("fuse2_s42", "p1_s43", "zeroshot")
                    for q in ("detailed", "short")]
    + [f"data/results/uitviic_ind_test/uitviic_{m}-{q}.preds.json" for m in ("fuse2_s42", "p1_s42")
       for q in ("detailed", "short")],
    ("uit", "F2"): [G2 + f"uv231-{q}-{t}.preds.json" for q in ("short", "detailed") for t in ("T0", "T05", "T08")],
}
ARMS = {"coco": ("L", "U"), "xm": ("L",), "uit": ("L", "U")}
CELLS = tuple((s, f, a) for (s, f) in FAMILIES for a in ARMS[s])  # D1, D3; D4(a) per world
D2_K = {"coco": 5, "uit": 5, "xm": 2}
MANIFEST5000 = "data/coco_probe/manifest_full5000.json"
GOLD5000 = ".session_backup/2026-10-26/a_full5000/instance_gold_full5000.json"
BUILDER = "scripts/paperA/a_w4/eval/build_instance_gold_full5000.py"
CHECK_COCO_FULL = "scripts/paperA/a_w4/eval/check_coco_full.py"
R4 = ".session_backup/2026-10-26/a_full5000/out/r4_full5000_all9.json"
SCAR_RESULT = "data/results/scar/scar_null_result.json"
INSTANCES = "data/datasets/coco_probe/annotations/instances_val2014.json"
R4_CELLS = ("inst", "refs1_firstk", "refs1_randk", "refs5_firstk")

PINS = {
    ".session_backup/2026-10-13/decisions/PD-23.txt": "3c719a6b64edef4f34d05595c99fb6b8dfdb8cf1b92bdc9081e8502779e17369",
    ".session_backup/2026-10-14/r11_litmaps/L1/check_coco.json": "cb21dd257f93a794fa7933c39a994a15825e95f705bdf3dd3e5cc1ad273593aa",
    ".session_backup/2026-10-14/r11_litmaps/L1/scripts/check_mstar.py": "6e2c0042ac44fe3e111fd88bc4783cf12c73a54ae938ee0d1802222b3048fb95",
    ".session_backup/2026-10-14/r11_verify/c2_n1_uitviic_mstar.json": "bed1dc259aefe32fbb5a966e807022ccff9dc56cc90fc9f405ca45a152e7780b",
    ".session_backup/2026-10-14/r12_verify/evaluate_xm3600_predictions.py": "dc00c4567de688448594f73570e4e9da2c2905cb135361b1bbf5d5fae10000ca",
    ".session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json": "0b2b3aa5e1a3f532e62e836c2b8011a46c811f7c01aaed4711aa9eae9a133dbf",
    G2 + "uv231-detailed-T0.preds.json": "2a92344baddc53c2e3974a701a973b8e1be0f44bcf780376851d812f27dcdeec",
    G2 + "uv231-detailed-T05.preds.json": "3bef57a29456f81cbce0b9c839c45100112132a7ee6a8eafd57d7ed724b57420",
    G2 + "uv231-detailed-T08.preds.json": "d994c6961bf1b6343df239fbbc1ada63a4665a2a2790065d9fa5d0fe398f3fcd",
    G2 + "uv231-short-T0.preds.json": "7553ab1b58e481201ac99fdcc773c2f58ce59485b06aac709c7b31a4711828ee",
    G2 + "uv231-short-T05.preds.json": "fcde78a819df6f31cd782080bf55b09c624aa4dbe32735c431b02cfbb952d14f",
    G2 + "uv231-short-T08.preds.json": "4839f485665cdb45fd4ddac53ce172b8e108192243fff06b4c488f681a559a23",
    G2 + "xm600-detailed-T0.preds.json": "a66647d12140858e8c013fdce6133949c4b97179d91acc92c413608bf0a560df",
    G2 + "xm600-detailed-T05.preds.json": "3e6189d627affaec4e327b1eb3ac1a55a3b76cbc8ae5001dc3c63de9c6baa9ee",
    G2 + "xm600-detailed-T08.preds.json": "944668eb32fb4a76209837f394bf6cd62a3245d8ac467e715105b3953dd2e751",
    G2 + "xm600-short-T0.preds.json": "82b6ef5fdb9bc98a34e07b9a68e99b1403277d275285fe6df54864d319f57e5e",
    G2 + "xm600-short-T05.preds.json": "522819dfe54dc8a9e191b9ddf88c0df6edb3a1bda6e9a1c4932533c273e1ae76",
    G2 + "xm600-short-T08.preds.json": "71b168e7909913fe2f95c63727be1f9a664dea5b8271a82357aae15d61f698fc",
    GOLD5000: "bd36295146e505454f5110e817841d8300a024265c1f2cba2aade854119183f7",
    R4: "332da8b6264c9c05232e5ef70cd864a0fe7ce58480e99aee558b1115a5c793af",
    "data/coco_probe/chair_synonyms.txt": "b685537b36fe21b791c87151b96a991ceb582edff19f3da204dcc7a7905502f2",
    "data/coco_probe/coco80_vi.json": "926e08571ef6e80a7f8aae8f2b73753d6c5c54c431a750ba2b67bfaae71b540b",
    "data/coco_probe/instance_gold.json": "963af2c6cc71e7a5e32c2f8f1ca6a0f1ef0a1f02dadf40926ddb05eebd04f81e",
    "data/coco_probe/manifest.json": "931e572ec8ea5eadf4c49aafcc062a837429b4e6bcc1f96fc0ec0ee1ecaa7e35",
    MANIFEST5000: "699769100c572675dfc4ae9f2a45f01bf387c4b1d67e9019feafc8c14fc88f7e",
    INSTANCES: "e1b4d1bc54906827b1a029981b1c77f2088bd4462569b7615db7929070c3ab47",
    "data/datasets/karpathy/dataset_coco.json": "2fd999220673258012acfb411a4e7e66af7d488050b2519b0badcc49b7600b8d",
    "data/datasets/uitviic/test_data.json": "54abc0fb068ad1108d7d57b21328d4d68bcf8f41aa168f80ec7c275fb4ac8214",
    "data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv": "84a4373a0efb7fd6d93fe19b0e7ceb6c1b855c233d13b9b78a9a33655c9fdce3",
    "data/datasets/xm3600/test_data.json": "0a613214f95605ff137879f70cb84f8160172c28a650317766ac4a1d9c3b72e8",
    C5 + "distill-detailed.shard0of1.jsonl": "6453bfd5a2f7667d0cc879d3e4ca359553b9bda994760d227785da141ec001fd",
    C5 + "distill-short.shard0of1.jsonl": "12ab5a6e2b707068a48f2247832bcd125559a291ea8f265946e9031d3ccef1b0",
    C5 + "zeroshot-detailed.shard0of1.jsonl": "96e15f40cead64a993ff01ba2392857b1dae16155661ffddd7f2bac3af54365a",
    C5 + "zeroshot-short.shard0of1.jsonl": "15ca56156796605c02397d13c60047bc6260d34ac65b8cc54f7651d71717feba",
    VCD + "zeroshot-detailed.shard0of1.jsonl": "d6173e34823383202298ea7dc00afdd92604277a70bff5a9f1d93e1173396bbd",
    "data/results/coco_transfer/fuse2_s42-detailed.shard0of1.jsonl": "87d1ee42f87f7ad11da5f8cb41cfef652de44340368d11a841e975d756439cc8",
    "data/results/coco_transfer/fuse2_s42-short.shard0of1.jsonl": "f2285267dd58b3214cf3974a4c6f7d52c1de46113e96cc6a68171fe95d6475b0",
    "data/results/coco_transfer/p1_s43-detailed.shard0of1.jsonl": "64ac2c9e9c2cfa3cacf9f8ac2675a2b2145a324d6aeb27c0119e166b489fa301",
    "data/results/coco_transfer/p1_s43-short.shard0of1.jsonl": "6f1be27242a0eff45e07c1ad3548a1149dc65b9bae4065294b6fb06faca4cf9d",
    TF + "fuse2_s42-detailed.shard0of1.jsonl": "f205805a7ab12cbd93c9ef6e240772fff7ac237e559cae57916b6191c85ce257",
    TF + "fuse2_s42-short.shard0of1.jsonl": "cd947944d3cf578bbffdc40ca9ae920f9595511e9ee395f06585bcd1db6fbd2f",
    TF + "p1_s43-detailed.shard0of1.jsonl": "b12fbeb91e9023c2872db3b03724e7b9ecdfe264b1bb0a3928fb5e4028d1befd",
    TF + "p1_s43-short.shard0of1.jsonl": "b0dbbdc50af75a77fa3da2808018faf0b7c26b52db3a86fbdf333da601cfbb24",
    "data/results/g2b/g2b_score.json": "68be2b7a0904027ccb6723129fe86cc10c4976a9e59fbc7862251fe715090824",
    "data/results/g2b/g2b_score.json.sha256": "6b85e46584ffe504ad153800f6e1feedf0f51a16bee62f8e0d5c724e83570e31",
    SCAR_RESULT: "242fc04ed80893307aaf93350bb885864d66ea06c9531691da642bcc3e2f6c0b",
    "data/results/uitviic/uitviic_fuse2_s42-detailed.preds.json": "82f34b94cf50e788f3bfb6d024141f2fc211c1bd311813748784030148b5670e",
    "data/results/uitviic/uitviic_fuse2_s42-short.preds.json": "42122e7ada5a04ba512543f05a02a8aac077f16b3d9b2cb93de67733d68b7142",
    "data/results/uitviic/uitviic_p1_s43-detailed.preds.json": "46cb0033cb222222b957a6e06d8269117819f1b8628c8ea0a2565a831b4e1196",
    "data/results/uitviic/uitviic_p1_s43-short.preds.json": "42ad49eebac92c8167721f629d4bbed75b284ac7efaa941482c4235611610d22",
    "data/results/uitviic/uitviic_zeroshot-detailed.preds.json": "0589973c264b9de43da7e63f40b19ba267a3d08e272c75f51f106cad764828d9",
    "data/results/uitviic/uitviic_zeroshot-short.preds.json": "76361ccde3db90b9eaa8cf0bf2b7bb055f3535a013626de3dae924bce59baea8",
    "data/results/uitviic_ind_test/uitviic_fuse2_s42-detailed.preds.json": "c7757cc734137a291bfa073d4fed31946f4351481c40c901e1fb27823113c4de",
    "data/results/uitviic_ind_test/uitviic_fuse2_s42-short.preds.json": "ebf68bca65b4009937b4e7b902892a9b6391551fc84ddd38dc981bdbfff7a8e2",
    "data/results/uitviic_ind_test/uitviic_p1_s42-detailed.preds.json": "56aac8a6e8733c4287443ea353bdee13c0716b4a9817c45779545310d01573db",
    "data/results/uitviic_ind_test/uitviic_p1_s42-short.preds.json": "94b87b4933d8dd7bf9f6108a2eeedd7fc0c8dd62f5b51313a182bc90db9444f7",
    "data/results/xm3600/xm3600_fuse2_s42-detailed.preds.json": "b941181c7b118c73fdac8f3f66797beee9d07891096a98927b1aa30f36b31203",
    "data/results/xm3600/xm3600_fuse2_s42-short.preds.json": "426c2d8140a912d17d296dddfcaa807aa93b5e673d3ee8fd5dea6c44885a2943",
    "data/results/xm3600/xm3600_p1_s43-detailed.preds.json": "296a26bfe17635afe61ab28ba16fae40714577b4981b96786cc021700410c7e2",
    "data/results/xm3600/xm3600_p1_s43-short.preds.json": "1150a046e63470c09268f0045b7b4976b6cad2a571453873277a9fc82fd2aad9",
    "data/results/xm3600/xm3600_zeroshot-detailed.preds.json": "47db3b9d279508e89f0332482c3e268a119186af9e0cbf6426cc85ce1a52a32f",
    "data/results/xm3600/xm3600_zeroshot-short.preds.json": "1f3573324772c67de3eebcdef326f84a39ecbe7fd705ceb5dd4e6863a0d73d4c",
    "data/uitviic/instance_gold.json": "278d15b97e3eeb9496a0282bb91deb365117becf24d174fbb1e0507203b12ea4",
    "data/xm3600/oiv7_labels.json": "bac3953a511a9793c22e928a29b68ae05dbf9654502abcbe7b64fd9f6d74c8b2",
    "data/xm3600/vi_oiv7_map.json": "27f2b1ca3f2bf47d43c8f00e8409472c8d571eb720d47b8107a1c77bd208d16a",
    "data/xm3600_subset.txt": "f5ab86c7f3126ab6683e97b769e462aa149ca22b081a889d0a0027904d503952",
    "manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.json": "c506bc777b483f5097561d2894a535f33e5e9e27745af07c0f979fbac5560055",
    PLAN: "03c0b97542116e983097d8456f77073b9398a0e5e542c5543797102279f1adbb",
    "rescap/__init__.py": "b712bea4d66e5e2e0f0cec1624ab244a025560ecc5d86f96cada2e0160a4890f",
    "rescap/chair.py": "e47d249ac7290070f2387d3fa8b22dac77728265ad276f55aa6520f5cbc591a3",
    "rescap/metrics.py": "e0296ec528b87f4d1b31165cbb45deee5453783fd7dad783f248869e596bf960",
    "rescap/repro.py": "723200190818cd61a56527e6a0a1596b95f9d1ed1ebc0cabe1b29135cf03b70d",
    "rescap/svp/__init__.py": "5b7f52920de75cf59bde0ae657e292a876efc63292ca6db6a4d085bb9fec1424",
    "rescap/svp/entailment.py": "4462f44df80faa0adc620d98aa5d8bbb307243d450e9aee4801bb17a3a06db23",
    "rescap/svp/matching.py": "a9253060131aacfca8eaab9a4b2c473c487db96a7c1222f0b8e31f9f61b24003",
    "rescap/vi/__init__.py": "f898963e95fec7d9fb236295649404815634a1d949bfd74cd7c3b90ed493bf6c",
    "rescap/vi/classifier.py": "966cdab1fed8471ac57d225698e63f1e2a055435a5d669e9cca10eed703fed16",
    "rescap/vi/color.py": "242fc46f68ecb06c8eefde23350481d99e60566b3da64ab90cfa79db38fd3875",
    "rescap/vi/lexicon.py": "fbc945f2247418275144ac75b893f7c51f8951b9ea42018680d433775dd79eb9",
    "rescap/vlm/__init__.py": "13de9854599acedd32ea1798ea1acc475703fcd3aa4eb4dd715dc8eadcd632cd",
    "rescap/vlm/base.py": "e8fee5bc5b729534af67c6e462a27f0d83ba611f18ff8e3f2717b11eb393ae93",
    "rescap/vlm/mock.py": "33793de01b4f2790964342b1af2d4c2de18d793ae4693608283992475ed62ce7",
    "rescap/vlm/registry.py": "6c261406bde3d34a73f77ce961aff7d241e2a440ba75e154fccf3ae8d4a70297",
    "rescap/vocab.py": "c9143b2d973fc48a2231335844cd91ab702329c0b1aabb802884225e155967ec",
    "scripts/clean_supervision.py": "01f172002a607ba9ee55bccb332439f10650832cae1f64a9b74b35c48cd9c231",
    "scripts/g2b/score_g2b.py": "66c665c7a71d3b97abbf89fd5bf13871910449ad1c053ff5fb0b18663e3e7ae5",
    BUILDER: "dc0d1f52bffd1804797169b493f3828a3d8f4d823113bc7bd0f11ee31d18f30e",
    CHECK_COCO_FULL: "adb3b936b9621430d5415ce7cf805e935216dd8b8c55ec016d25f7111e0080e2",
    "scripts/pascal50s/p50.py": "2387ca05ae8a57304a5f696c4e2f73d29297d03ccc23debb416269dc7a676d31",
    "scripts/pascal50s/p50x.py": "3f562e878ed793f4b3cae84dd93373b10d82564d162cb399ab16e03ccf8825c2",
    "scripts/person_uncap.py": "d16b19f6597f84597db7865dea4058f0bb1fecf914d71d34d6406d66283fa5bb",
    "scripts/scar/scar_null.py": "b0e3825eaa48ba496ec2723010e6125a0c4d8abbf1d5aa3fcf0b3a6dfd94bb3b",
    "scripts/score_coco_probe.py": "d11db7e192f689980bb2b2bb717d852d9aa339ad857ce9411fe7bdd6fe416070",
    "scripts/xm3600_oiv7.py": "9a79403f4fc38609282d40082ab7f878133edca8aff9e0dc2462db467b7193f0",
}
# imported modules and the files they read at import (score_coco_probe: lexicon, synonyms; scar_null: PD-23)
CODE_PINS = tuple(p for p in PINS if p.startswith(("rescap/", "scripts/")) and p not in (BUILDER, CHECK_COCO_FULL)) + (
    "data/coco_probe/coco80_vi.json", "data/coco_probe/chair_synonyms.txt",
    ".session_backup/2026-10-13/decisions/PD-23.txt")


class Fault(SystemExit):
    def __init__(self, msg: str):
        super().__init__(2)
        self.msg = msg

    def __str__(self) -> str:
        return f"FAULT: {self.msg}"


class CapReached(Exception):
    pass


# ------------------------------------------------------------------------------------------------ pins and libraries
def sha_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def assert_pins(paths) -> dict:
    """Hash every path before anything reads it; any difference or missing file is a FAULT."""
    if os.environ.get("RESCAP_RAW_TONE") == "1":
        raise Fault("RESCAP_RAW_TONE=1 changes the pinned matcher")
    bad = []
    for p in paths:
        f = ROOT / p
        got = sha_file(f) if f.is_file() else None
        if got != PINS[p]:
            bad.append(f"{p}: {got} != {PINS[p]}")
    if bad:
        raise Fault("input sha mismatch: " + "; ".join(bad))
    return {p: PINS[p] for p in paths}


def load_libs() -> dict:
    """Imports after the pin check; every repo module loaded must be pinned (fail-closed)."""
    sys.path[:0] = [str(ROOT), str(ROOT / "scripts"), str(ROOT / "scripts/g2b"), str(ROOT / "scripts/pascal50s"),
                    str(ROOT / "scripts/scar")]
    import p50  # noqa: E402
    import p50x  # noqa: E402
    import scar_null  # noqa: E402
    import score_g2b  # noqa: E402
    from scipy import stats  # noqa: E402
    for name, mod in list(sys.modules.items()):
        f = getattr(mod, "__file__", None)
        if name == "__main__" or not f:
            continue
        rp = Path(f).resolve()
        if rp.is_relative_to(ROOT) and str(rp.relative_to(ROOT)) not in PINS:
            raise Fault(f"imported repo module is not pinned: {rp.relative_to(ROOT)}")
    return {"g": score_g2b, "p50": p50, "p50x": p50x, "sn": scar_null, "stats": stats}


def jload(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def write_json(rel: str, obj) -> str:
    out = ROOT / rel
    if not out.resolve().is_relative_to(ROOT / OUT):
        raise Fault(f"refused: output outside {OUT}: {rel}")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return sha_file(out)


def seed(check: str, st: str = "coco", fam: str = "F1", arm: str = "L", world: str = "real", extra: int = 0) -> int:
    return BASE_SEED + OFF["check"][check] + OFF["set"][st] + OFF["fam"][fam] + OFF["arm"][arm] + \
        OFF["world"][world] + 100_000 * extra


def git_blob_sha(rel: str) -> str | None:
    r = subprocess.run(["git", "-C", str(ROOT), "show", f"HEAD:{rel}"], capture_output=True)
    return hashlib.sha256(r.stdout).hexdigest() if r.returncode == 0 else None


def env_guard() -> None:
    """Plan §6: laptop, -I, 2 threads, nice 15."""
    bad = [k for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS") if os.environ.get(k) != "2"]
    if bad or not sys.flags.isolated or os.getpriority(os.PRIO_PROCESS, 0) < 15:
        raise Fault(f"run conditions (plan §6) not met: threads {bad}, isolated {sys.flags.isolated}, "
                    f"nice {os.getpriority(os.PRIO_PROCESS, 0)}")


# ------------------------------------------------------------------------------------------------ budget and order
class Budget:
    """6 CPU-h or 4 h wall in total, whichever first (plan §6); cpu0/wall0 carry the S0 time."""

    def __init__(self, cpu_cap=CAP_CPU_S, wall_cap=CAP_WALL_S, cpu0=0.0, wall0=0.0, clock=None):
        self.clock = clock or (lambda: (time.process_time() + os.times().children_user + os.times().children_system,
                                        time.monotonic()))
        self.cpu_cap, self.wall_cap = cpu_cap, wall_cap
        c, w = self.clock()
        self.c0, self.w0 = c - cpu0, w - wall0

    def used(self) -> tuple[float, float]:
        c, w = self.clock()
        return c - self.c0, w - self.w0

    def left(self) -> tuple[float, float]:
        c, w = self.used()
        return self.cpu_cap - c, self.wall_cap - w

    def check(self) -> None:
        c, w = self.used()
        if c >= self.cpu_cap or w >= self.wall_cap:
            raise CapReached(f"cpu {c:.0f} s, wall {w:.0f} s")


def run_checks(steps: list, budget: Budget, res: dict | None = None) -> dict:
    """Plan §6 stop rule: at the cap the running check and every later check are NOT_RUN; any other exception or
    FAULT inside a step makes that step FAULT and every later step NOT_RUN; a step may also request a stop
    (implementation fault). Results already finished are kept in `res` (filled in place). Nothing is resumed."""
    res = {} if res is None else res
    stop = None
    for name, fn in steps:
        if stop:
            res[name] = {"label": "NOT_RUN", "reason": stop}
            continue
        try:
            budget.check()
            res[name] = fn()
        except CapReached as e:
            res[name] = {"label": "NOT_RUN", "reason": f"cap reached during {name} ({e})"}
            stop = f"cap reached during {name}"
        except (Exception, SystemExit) as e:  # noqa: BLE001  (B1: a FAULT or error is recorded, never escapes)
            res[name] = {"label": "FAULT", "reason": f"{type(e).__name__}: {str(e)[:300]}"}
            stop = f"FAULT during {name}"
        else:
            if res[name].get("stop"):
                stop = res[name]["stop"]
    return res


def claim_start(marker: Path, rec: dict) -> None:
    """One attempt only (CC-271 B1): the marker is created exclusively before any data is loaded; if it exists the
    run is refused, so neither the one-pass rule nor the cap can be reset by starting again."""
    marker.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(marker, "x", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, indent=1) + "\n")
    except FileExistsError:
        raise Fault(f"refused: {marker.name} exists (one attempt; a resume needs a new plan version)") from None


def run_attempt(marker: Path, start_rec: dict, prepare, budget: Budget, write_result) -> dict:
    """Claim the attempt, build the steps, run them, and write the result in a finally whatever happens (CC-271 B1).
    prepare() -> (steps, meta). A failure before the first check leaves every check NOT_RUN with the FAULT named."""
    claim_start(marker, start_rec)
    res, meta, fault = {}, {}, None
    try:
        steps, meta = prepare()
        run_checks(steps, budget, res)
    except BaseException as e:  # noqa: BLE001  (recorded below, then re-raised if not an ordinary error)
        fault = f"{type(e).__name__}: {str(e)[:300]}"
        if not isinstance(e, (Exception, SystemExit)):
            raise
    finally:
        for n in ORDER:
            res.setdefault(n, {"label": "NOT_RUN", "reason": f"FAULT or interruption before {n}: {fault}"})
        cpu, wall = budget.used()
        write_result({**meta, "checks": res, "fault_outside_steps": fault, "cpu_s_total": cpu, "wall_s_total": wall})
    return res


class SLock:
    """D4(a): S is fixed before any p-value and never changed after one (plan §4 D4(a))."""

    def __init__(self):
        self.S, self.p_seen = None, False

    def fix(self, S: int) -> None:
        if self.p_seen:
            raise Fault("S changed after a p-value was computed")
        self.S = S

    def decide(self, obs: float, null: np.ndarray) -> tuple[str, float]:
        if self.S is None:
            raise Fault("p-value requested before S was fixed")
        self.p_seen = True
        return decide(obs, null)


def decide(obs: float, null: np.ndarray) -> tuple[str, float]:
    """p50x.salience rule: PASS iff obs < interpolated 2.5th percentile; FAIL iff obs >= median;
    p = (1 + #{null <= obs}) / (B + 1)."""
    lo, med, hi = (float(np.percentile(null, q)) for q in (2.5, 50, 97.5))
    v = "NOT_EVALUABLE" if lo == hi or not np.isfinite(obs) else "PASS" if obs < lo else \
        "FAIL" if obs >= med else "INCONCLUSIVE"
    return v, float((1 + (null <= obs).sum()) / (len(null) + 1))


def levels(world: str, arm: str) -> tuple[int, ...]:
    """Arm L: level 1 only. Arm U at the real K = 5: level 1 only (level 5 = C_i, degenerate null). Levels {1, 5}
    with g.compound only in W-50 arm U (plan §2, §4 D4(a))."""
    return (1, 5) if world == "W50" and arm == "U" else (1,)


def shared_null(world: str, arm: str) -> bool:
    """One null per cell (B = 1,000) where q_i^(j) is a fixed reference size: W-real and W-50 arm L. W-50 arm U
    redraws the null per simulation at both levels (N2, N-B2)."""
    return not (world == "W50" and arm == "U")


# ------------------------------------------------------------------------------------------------ cells and kernel
def coco_complete(ids: list[str], gold: dict) -> list[set]:
    """COCO C_i from instance_gold_full5000.json, indexed directly: a missing id raises (fail-closed, plan §1 B1 iv)."""
    try:
        return [set(gold[i]["coco"]) for i in ids]
    except KeyError as e:
        raise Fault(f"COCO gold has no entry for id {e}") from None


def make_cell(name: str, comp: list[set], ments: list[list[set]], refs: list[list[set]], use) -> dict:
    """Integer class slots: slot t = (image seg[t], class cls[t]) for c in sorted(C_i), images in id order."""
    comp_s = [sorted(c) for c in comp]
    N = len(comp_s)
    ell = np.array([len(c) for c in comp_s], np.int64)
    start = np.concatenate([[0], np.cumsum(ell)])
    seg = np.repeat(np.arange(N), ell)
    cls = [c for cs in comp_s for c in cs]
    S = len(cls)
    K = np.array([len(r) for r in refs], np.int64)
    H = np.array([[c in m[i] for c, i in zip(cls, seg)] for m in ments], float).reshape(len(ments), S)
    M = np.array([[len(x) for x in m] for m in ments], float)
    Zref = np.array([[bool(k < K[i] and c in refs[i][k]) for c, i in zip(cls, seg)] for k in range(int(K.max()))],
                    float).reshape(int(K.max()), S)
    return {"name": name, "N": N, "S": S, "ell": ell, "start": start, "seg": seg, "pos": np.arange(S) - start[seg],
            "cls": cls, "H": H, "M": M, "K": K, "Zref": Zref, "use": np.asarray(use, float), "comp": [set(c) for c in comp],
            "ments": ments}


def segsum(cell: dict, X) -> np.ndarray:
    X = np.asarray(X, float)
    C = np.concatenate([np.zeros(X.shape[:-1] + (1,)), np.cumsum(X, -1)], -1)
    return C[..., cell["start"][1:]] - C[..., cell["start"][:-1]]


def lin_stats(g, cell: dict, Z, q, w) -> dict:
    """Metrics of plan §2 at slot values Z (..., S) with gold sizes q (..., N) and image weights w (N,): P, R, mixed F1
    (F), micro-F1 (MU), caption CHAIR (CH), each (..., systems); score_g2b.scores conventions (R nan without gold
    images, F 0 when P + R is not positive)."""
    seg, H, Mi = cell["seg"], cell["H"], cell["M"]
    Hw = H * w[seg]
    msum = Mi @ w
    Hm = np.divide(Hw, Mi[:, seg], out=np.zeros_like(Hw), where=H > 0)
    q = np.asarray(q, float)
    invq = np.divide(1.0, q, out=np.zeros(q.shape), where=q > 0)
    tp = Z @ Hw.T
    rn = (Z * invq[..., seg]) @ Hw.T
    nh = ((q > 0) * w).sum(-1)[..., None]
    sq = (q * w).sum(-1)[..., None]
    P = g.div(tp, msum, 0.0)
    R = g.div(rn, nh, np.nan)
    with np.errstate(invalid="ignore"):
        F = g.div(2 * P * R, P + R, 0.0)
    return {"P": P, "R": R, "F": F, "MU": g.div(2 * tp, msum + sq, 0.0),
            "CH": (((Mi > 0) @ w) - Z @ Hm.T) / w.sum(), "lm": np.log(msum / w.sum())}


def beta(g, lm, V) -> np.ndarray:
    """OLS slope (x100) over systems of V (..., systems) on lm = ln M."""
    V = np.asarray(V, float)
    return g.ols(lm[:, None], 100 * V.reshape(-1, V.shape[-1]).T).reshape(V.shape[:-1])


def ranks_from_keys(cell: dict, keys: np.ndarray) -> np.ndarray:
    """Rank of every slot within its image by ascending key (ties never matter: q never reaches an inf key)."""
    order = np.lexsort((keys, np.broadcast_to(cell["seg"], keys.shape)), axis=-1)
    r = np.empty(keys.shape, np.int64)
    np.put_along_axis(r, order, np.broadcast_to(cell["pos"], keys.shape), -1)
    return r


def ranks_p50x_stream(cell: dict, rng, n_rep: int) -> np.ndarray:
    """The permutations p50x.null_slopes / scar_null.null_slopes draw from `rng`, as slot ranks (kernel gate)."""
    r = np.empty((n_rep, cell["S"]), np.int64)
    for b in range(n_rep):
        for i in range(cell["N"]):
            p = rng.permutation(int(cell["ell"][i]))
            r[b, cell["start"][i] + p] = np.arange(len(p))
    return r


def T_from_ranks(g, cell: dict, ranks: np.ndarray, q: np.ndarray, w, metrics=T_STATS) -> dict:
    """Nested null: draw j keeps the first q_i^(j) of the replicate's permutation; statistic = slope of the J-draw
    mean of each metric (mixed F1 averages F per draw, as score_g2b.scores)."""
    Z = (ranks[:, None, :] < q[:, cell["seg"]][None]).astype(float)
    st = lin_stats(g, cell, Z, q, w)
    return {m: beta(g, st["lm"], st[m].mean(1)) for m in metrics}


NULL_CALLS = {"n": 0}


def null_stats(g, cell: dict, specs: dict, w, rng, n_rep: int, domain=None, a=None, budget=None) -> dict:
    """{name: (q (J, N), metrics)} -> {name: {metric: (n_rep,)}} on shared ranks per replicate. Uniform keys, or keys
    -ln(u)/a_c (weighted, without replacement); slots outside `domain` never enter (W-50 arm U)."""
    NULL_CALLS["n"] += 1
    out = {k: {m: np.empty(n_rep) for m in ms} for k, (q, ms) in specs.items()}
    J = max(q.shape[0] for q, _ in specs.values())
    step = max(1, CHUNK // (J * max(cell["S"], 1)))
    for s0 in range(0, n_rep, step):
        b = min(step, n_rep - s0)
        u = 1.0 - rng.random((b, cell["S"]))
        keys = u if a is None else -np.log(u) / a
        if domain is not None:
            keys[:, ~domain] = np.inf
        r = ranks_from_keys(cell, keys)
        for k, (q, ms) in specs.items():
            for m, v in T_from_ranks(g, cell, r, q, w, ms).items():
                out[k][m][s0:s0 + b] = v
        if budget:
            budget.check()
    return out


def draw_q(cell: dict, Zk: np.ndarray, d: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Gold of draw j = reference d[j, i] of image i: slot values (J, S) and sizes (J, N)."""
    Z = Zk[d[:, cell["seg"]], np.arange(cell["S"])]
    return Z, segsum(cell, Z).round()


def draw_q5(cell: dict, Zk: np.ndarray, d5: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Level 5: union of the 5 drawn references; d5 (J, N, 5)."""
    Z = Zk[d5[:, cell["seg"], :], np.arange(cell["S"])[:, None]].max(-1)
    return Z, segsum(cell, Z).round()


def evaluable(cell: dict, qJ: np.ndarray, arm: str) -> tuple[bool, str]:
    """No evaluable images or systems -> NOT_EVALUABLE (plan §2). p50x ev(): every system mentions something and
    >= 2 distinct M. Arm L: X5's rule sum l_i >= 2 * sum q_i (mean over draws), else NOT_EVALUABLE."""
    u = cell["use"] > 0
    if not u.any():
        return False, "no scored image"
    Mm = cell["M"][:, u].mean(1)
    if not np.all(Mm > 0) or len({round(float(x), 12) for x in Mm}) < 2:
        return False, "a system mentions nothing or fewer than 2 distinct M"
    sl = float(cell["ell"][u].sum())
    if sl == 0:
        return False, "empty complete gold"
    if arm == "L" and sl < 2 * float(qJ[:, u].sum(1).mean()):
        return False, "sum l_i < 2 * sum q_i (X5 rule)"
    return True, ""


# ------------------------------------------------------------------------------------------------ rules (pure)
def inv(p: float) -> float:
    return NormalDist().inv_cdf(p)


def d1_sizes(nsys_per_cell: list[int]) -> tuple[int, int]:
    """m_lin = number of linear z's (4 metrics x (systems + 1 slope) per cell); m_mix = per-system mixed-F1 tests."""
    return sum(len(LINEAR) * (n + 1) for n in nsys_per_cell), sum(nsys_per_cell)


def d1_rule(z_lin: list[float], mix_gap: list[float], mix_se: list[float], slope_err: list[float], m_lin: int,
            m_mix: int) -> dict:
    t_lin, t_mix = inv(1 - 0.025 / m_lin), inv(1 - 0.05 / m_mix)
    zmax = float(np.max(np.abs(z_lin)))
    mix_ok = all(gp >= -t_mix * se for gp, se in zip(mix_gap, mix_se))
    slope_ok = all(abs(e) <= D1_SLOPE_TOL for e in slope_err)
    return {"threshold_linear": t_lin, "max_abs_z": zmax, "linear": "PASS" if zmax <= t_lin else "FAIL",
            "threshold_mixed": t_mix, "mixed_per_system_ok": mix_ok, "mixed_slope_ok": slope_ok,
            "mixed": "PASS" if mix_ok and slope_ok else "FAIL"}


def zstat(closed: float, mean: float, se: float) -> float:
    """z of closed form vs MC mean; a difference within float precision (1e-12, e.g. a metric constant under the null
    because a system names every class of C_i) is exact, z = 0."""
    d = closed - mean
    if abs(d) <= 1e-12:
        return 0.0
    return d / se if se > 0 else float(np.sign(d) * np.inf)


def boot_p2(b: np.ndarray) -> float:
    """Two-sided bootstrap p of 0."""
    return float(min(1.0, 2 * min(1 + (b <= 0).sum(), 1 + (b >= 0).sum()) / (len(b) + 1)))


def d2_labels(tests: dict, holm) -> dict:
    """tests: {key: {"p", "half", "g_obs"}} -> label per key. Holm rejection = FAIL; else half > 0.5|g_obs| =
    UNDERPOWERED; else PASS."""
    rej = holm({k: t["p"] for k, t in tests.items()}, ALPHA)
    return {k: "FAIL" if rej[k] else "UNDERPOWERED" if t["half"] > D2_HALF * abs(t["g_obs"]) else "PASS"
            for k, t in tests.items()}


def d3_p(b: np.ndarray) -> float:
    """One-sided bootstrap p for H0: de <= 0 (N2''): (1 + #{de* <= 0}) / (B + 1)."""
    return float((1 + (b <= 0).sum()) / (len(b) + 1))


def d3_labels(boots: dict, m: int, holm) -> dict:
    """FAIL (Holm rejects H0: de <= 0) takes precedence; PASS = not FAIL and upper (1 - 0.05/m) <= SESOI;
    UNDERPOWERED otherwise. Disjoint and exhaustive."""
    rej = holm({k: d3_p(b) for k, b in boots.items()}, ALPHA)
    out = {}
    for k, b in boots.items():
        up = float(np.percentile(b, 100 * (1 - ALPHA / m)))
        out[k] = {"p_one_sided": d3_p(b), "upper": up, "holm_rejects": bool(rej[k]),
                  "label": "FAIL" if rej[k] else "PASS" if up <= SESOI else "UNDERPOWERED"}
    return out


def t2_sets_ok(evaluable_by_set: dict) -> bool:
    """Plan §2: a check counts toward T2 only if every set it names has at least one evaluable cell."""
    return bool(evaluable_by_set) and all(any(v) for v in evaluable_by_set.values())


def ev_by_set(cells: dict, arms=("L", "U")) -> dict:
    return {st: [c["evaluable"] for (s, _, a), c in cells.items() if s == st and a in arms] for st in ARMS}


def d1_verdict(rule: dict) -> dict:
    out = {"label": "PASS" if rule["linear"] == rule["mixed"] == "PASS" else "FAIL"}
    if rule["linear"] == "FAIL":
        out["stop"] = "D1 linear FAIL: implementation fault (plan D1)"
    return out


def d4a_verdict(labels: list[str], sd_labels: list[str]) -> dict:
    out = {"label": "PASS" if labels and all(x == "PASS" for x in labels) else "FAIL",
           "single_draw_label": "PASS" if all(x == "PASS" for x in sd_labels) else "FAIL"}
    if out["single_draw_label"] == "FAIL":
        out["stop"] = "D4(a) single-draw FAIL: implementation fault (plan D4(a))"
    return out


def overall(labels: list[str]) -> str:
    return "FAIL" if "FAIL" in labels else "PASS" if labels and all(x == "PASS" for x in labels) else "UNDERPOWERED"


def d5_rule(lower_gold: float, lower_all: float) -> str:
    """On the 2.5th percentile of the two-sided 95% percentile CI, never the point estimate."""
    return "ALLOWED" if lower_gold >= D5_MIN and lower_all >= D5_MIN else "PREFIX_ONLY"


def d4a_sizes(n_cells: int) -> tuple[int, int]:
    """m = cells x 3 T statistics; m_sd = cells (CC-266r3 6a)."""
    return 3 * n_cells, n_cells


def d4a_bound(S: int, m: int) -> float:
    return 0.025 + inv(1 - 0.05 / m) * np.sqrt(0.025 * 0.975 / S)


def ks_smaller(stats, p) -> float:
    """One-sided KS: alternative = p stochastically smaller than U(0, 1) (empirical CDF above the diagonal)."""
    return float(stats.kstest(p, "uniform", alternative="greater").pvalue)


def d4a_rule(rate: float, ks_p: float, S: int, m: int) -> str:
    return "PASS" if rate <= d4a_bound(S, m) and ks_p >= 0.05 / m else "FAIL"


def d4a_sd_rule(ks2_p: float, m_sd: int) -> str:
    return "PASS" if ks2_p >= 0.05 / m_sd else "FAIL"


def d4b_rule(G: float, b_delta: float, se_sim: float, se_w: float) -> str:
    return "PASS" if abs(G - b_delta) <= 2 * np.sqrt(se_sim ** 2 + se_w ** 2) else "FAIL"


def prefix_classes(caption: str, fn, budgets=BUDGETS) -> dict:
    """Shortest word-boundary prefix whose re-matched class set reaches b, per budget (absent if never reached)."""
    out = {}
    for m in re.finditer(r"\S+", caption):
        s = fn(caption[:m.end()])
        for b in budgets:
            if b not in out and len(s) >= b:
                out[b] = s
        if len(out) == len(budgets):
            break
    return out


# ------------------------------------------------------------------------------------------------ data (real)
def load_family(L: dict, st: str, fam: str, ids: list[str], fn) -> dict:
    g = L["g"]
    systems = FAMILIES[(st, fam)]
    caps = {s: g.read_captions(ROOT / s) for s in systems}
    for s, c in caps.items():
        if not set(ids) <= set(c) or not all(isinstance(k, str) for k in c):
            raise Fault(f"{s}: does not cover every id with str keys")
    use = np.array([all(g.is_clean(caps[s][i], "vi") for s in systems) for i in ids], float)
    return {"set": st, "fam": fam, "systems": systems, "caps": caps, "fn": fn, "use": use,
            "ments": [g.mentions(caps[s], ids, fn) for s in systems]}


def load_sets(L: dict) -> dict:
    g = L["g"]
    out = {}
    ids = [str(i) for i in sorted(int(m["cocoid"]) for m in jload(MANIFEST5000)["images"])]
    kr = g.karpathy_refs({int(i) for i in ids})
    if any(len(kr[int(i)]) < 5 for i in ids):
        raise Fault("a COCO image has fewer than 5 references")
    refs = [[g.sc.en_classes(s, g.SYN) for s in kr[int(i)][:5]] for i in ids]
    out["coco"] = {"ids": ids, "refs": refs, "L": coco_complete(ids, jload(GOLD5000)), "fn": g.MATCH["coco80"]["vi"]}
    u = g.uitviic_context()
    lx = u["lexicons"]["coco80"]
    out["uit"] = {"ids": u["ids"], "refs": lx["refs"], "L": lx["complete"], "fn": g.MATCH["coco80"]["vi"]}
    x = g.xm3600_context()
    lx = x["lexicons"]["objects_in"]
    out["xm"] = {"ids": x["ids"], "refs": lx["refs"], "L": [{c for c, v in s.items() if v == "present"}
                                                             for s in lx["oiv7"]], "fn": g.MATCH["objects_in"]["vi"]}
    for st, d in out.items():
        d["U"] = [set().union(*r) for r in d["refs"]]
        d["draws"] = L["p50"].draw([len(r) for r in d["refs"]])
        d["d1"] = np.array([[t[0] for t in sub] for sub in d["draws"][1]], np.int64)
        d["fams"] = {f: load_family(L, st, f, d["ids"], d["fn"]) for (s, f) in FAMILIES if s == st}
    return out


def build_cells(sets: dict) -> dict:
    cells = {}
    for st, fam, arm in CELLS:
        d, f = sets[st], sets[st]["fams"][fam]
        refs = d["refs"] if arm == "U" else [[r & c for r in rs] for rs, c in zip(d["refs"], d["L"])]
        c = make_cell(f"{st}/{fam}/{arm}", d[arm], f["ments"], refs, f["use"])
        c["d1"] = d["d1"]
        c["qref"] = segsum(c, c["Zref"]).round()
        c["qJ"] = draw_q(c, c["Zref"], c["d1"])[1]
        c["q1"] = c["qref"][:1]
        c["evaluable"], c["why"] = evaluable(c, c["qJ"], arm)
        cells[(st, fam, arm)] = c
    return cells


# ------------------------------------------------------------------------------------------------ D1
def d1_cell(L: dict, cell: dict, rng, n_rep: int, budget=None) -> dict:
    g, w, seg, ell = L["g"], cell["use"], cell["seg"], np.maximum(cell["ell"], 1)
    specs = {"single": cell["q1"], "T20": cell["qJ"]}
    vals = {t: {m: np.empty((n_rep, cell["H"].shape[0])) for m in (*LINEAR, "F")} for t in specs}
    step = max(1, CHUNK // (cell["qJ"].shape[0] * max(cell["S"], 1)))
    for s0 in range(0, n_rep, step):
        b = min(step, n_rep - s0)
        r = ranks_from_keys(cell, rng.random((b, cell["S"])))  # one permutation per replicate, shared by both
        for t, q in specs.items():
            st = lin_stats(g, cell, (r[:, None, :] < q[:, seg][None]).astype(float), q, w)
            for m in vals[t]:
                vals[t][m][s0:s0 + b] = st[m].mean(1)
        if budget:
            budget.check()
    out = {}
    for tag, q in specs.items():
        cl = lin_stats(g, cell, (q / ell)[:, seg], q, w)
        plug = g.div(2 * cl["P"] * cl["R"], cl["P"] + cl["R"], 0.0).mean(0)
        lm, vals_t = cl["lm"], vals[tag]
        rec = {}
        for m in LINEAR:
            closed = cl[m].mean(0)
            mean, se = vals_t[m].mean(0), vals_t[m].std(0, ddof=1) / np.sqrt(n_rep)
            sl = beta(g, lm, vals_t[m])
            z = [zstat(a, b_, c) for a, b_, c in zip(closed, mean, se)]
            z.append(zstat(float(beta(g, lm, closed)), float(sl.mean()), float(sl.std(ddof=1) / np.sqrt(n_rep))))
            rec[m] = {"closed": closed.tolist(), "mc_mean": mean.tolist(), "mc_se": se.tolist(), "z": z,
                      "slope_closed": float(beta(g, lm, closed)), "slope_mc_mean": float(sl.mean())}
        fm, fse = vals_t["F"].mean(0), vals_t["F"].std(0, ddof=1) / np.sqrt(n_rep)
        fsl = beta(g, lm, vals_t["F"])
        rec["F"] = {"plugin": plug.tolist(), "mc_mean": fm.tolist(), "mc_se": fse.tolist(),
                    "gap_plugin_minus_mc": (plug - fm).tolist(), "slope_plugin": float(beta(g, lm, plug)),
                    "slope_mc_mean": float(fsl.mean()), "slope_err": float(beta(g, lm, plug) - fsl.mean())}
        out[tag] = rec
    return out


def run_d1(L: dict, cells: dict, sizes: dict, budget) -> dict:
    recs, zl, gap, se, serr = {}, [], [], [], []
    for (st, fam, arm), c in cells.items():
        if not c["evaluable"]:
            recs[c["name"]] = {"label": "NOT_EVALUABLE", "reason": c["why"]}
            continue
        r = d1_cell(L, c, np.random.default_rng(seed("D1", st, fam, arm)), B_D1, budget)
        recs[c["name"]] = r
        s = r["single"]
        zl += [z for m in LINEAR for z in s[m]["z"]]
        gap += s["F"]["gap_plugin_minus_mc"]
        se += s["F"]["mc_se"]
        serr.append(s["F"]["slope_err"])
    if len(zl) != sizes["m_lin"] or len(gap) != sizes["m_mix"]:
        raise Fault(f"D1 family sizes differ from S0: {len(zl)}/{sizes['m_lin']}, {len(gap)}/{sizes['m_mix']}")
    rule = d1_rule(zl, gap, se, serr, sizes["m_lin"], sizes["m_mix"])
    return {"cells": recs, "m_lin": sizes["m_lin"], "m_mix": sizes["m_mix"], **rule, **d1_verdict(rule),
            "t2_sets_ok": t2_sets_ok(ev_by_set(cells)),
            "note": "rules on the single-draw statistic (reference 1); T20 (p50.draw, J = 20) reported beside"}


# ------------------------------------------------------------------------------------------------ D2
def boot_weights(n: int, rng, B: int = B_BOOT) -> np.ndarray:
    """Row 0 = point estimate; rows 1..B = image bootstrap multiplicities (score_g2b style)."""
    return np.vstack([np.ones(n), rng.multinomial(n, np.full(n, 1.0 / n), size=B)]).astype(float)


def d2_cell(L: dict, cell: dict, kmax: int, Wb: np.ndarray) -> dict:
    """Per-k D^(k) = beta(f(Q^(k))) - beta(f(w_hat^(-k))) for P and micro-F1 (R descriptive); w_hat^(-k) is the share
    of the other K_i - 1 references naming c. Wb (B+1, n_scored)."""
    g, seg = L["g"], cell["seg"]
    idx = np.flatnonzero(cell["use"] > 0)
    Z, H = cell["Zref"], cell["H"]
    Kslot = cell["K"][seg].astype(float)
    tot = Z.sum(0)
    WM = Wb @ cell["M"][:, idx].T
    lm = np.log(WM / Wb.sum(1)[:, None])
    sl = lambda V: g.ols(lm.T, 100 * V.T)  # noqa: E731  (slope per bootstrap column)
    per_k = {}
    for k in range(kmax):
        what = (tot - Z[k]) / (Kslot - 1)
        qk = segsum(cell, Z[k])[idx]
        rho = (segsum(cell, Z[k]) / np.maximum(cell["ell"], 1))[seg]
        tp = {v: segsum(cell, H * x)[:, idx] for v, x in (("obs", Z[k]), ("hat", what), ("rho", rho))}
        invq = np.divide(1.0, qk, out=np.zeros(len(qk)), where=qk > 0)
        has = Wb @ (qk > 0)
        val = {}
        for v, t in tp.items():
            val[("P", v)] = sl((Wb @ t.T) / WM)
            val[("MU", v)] = sl(2 * (Wb @ t.T) / (WM + (Wb @ qk)[:, None]))
            val[("R", v)] = sl((Wb @ (t * invq).T) / has[:, None])
        per_k[k] = {m: {"D": val[(m, "obs")] - val[(m, "hat")], "g_obs": float(val[(m, "obs")][0] - val[(m, "rho")][0])}
                    for m in ("P", "MU", "R")}
    D = {m: np.stack([per_k[k][m]["D"] for k in range(kmax)]) for m in ("P", "MU", "R")}
    rec = {}
    for k in range(kmax):
        for m in ("P", "MU", "R"):
            d = D[m][k]
            lo, hi = (float(np.percentile(d[1:], q)) for q in (2.5, 97.5))
            rec[f"k{k + 1}|{m}"] = {"D": float(d[0]), "ci95": [lo, hi], "half": (hi - lo) / 2, "p": boot_p2(d[1:]),
                                   "g_obs": per_k[k][m]["g_obs"]}
    rec["guard_mean_k_D_P"] = float(D["P"][:, 0].mean())
    return rec


def run_d2(L: dict, cells: dict, budget) -> dict:
    tests, recs = {}, {}
    for (st, fam, arm), c in cells.items():
        if arm != "L":
            continue
        if not c["evaluable"]:
            recs[c["name"]] = {"label": "NOT_EVALUABLE", "reason": c["why"]}
            continue
        n = int((c["use"] > 0).sum())
        r = d2_cell(L, c, D2_K[st], boot_weights(n, np.random.default_rng(seed("D2", st, fam, arm))))
        recs[c["name"]] = r
        tests.update({f"{c['name']}|{k}": v for k, v in r.items() if k.endswith(("|P", "|MU"))})
        budget.check()
    lab = d2_labels(tests, L["p50x"].holm)
    return {"cells": recs, "n_tests": len(tests), "labels": lab, "label": overall(list(lab.values())),
            "t2_sets_ok": t2_sets_ok(ev_by_set(cells, ("L",))),
            "note": "R descriptive only (1/q weights bias D under A1); Holm over k x set x family x metric (P, MU)"}


# ------------------------------------------------------------------------------------------------ D3
def delta_hat(cell: dict) -> np.ndarray:
    """delta_ic = w_ic - mean_k rho_i^(k), w = share of all K_i references naming c (slot vector; sums to 0 per image)."""
    w = cell["Zref"].sum(0) / cell["K"][cell["seg"]]
    return w - (segsum(cell, w) / np.maximum(cell["ell"], 1))[cell["seg"]]


def prefix_table(fam: dict, ids: list[str], keep: list[int], budget=None) -> dict:
    """(system index, image index) -> {b: class set} for the scored images whose full output reaches 5 classes."""
    out = {}
    for s in keep:
        caps, ment = fam["caps"][fam["systems"][s]], fam["ments"][s]
        for n, i in enumerate(ids):
            if fam["use"][n] > 0 and len(ment[n]) >= 5:
                pc = prefix_classes(caps[i], fam["fn"])
                out[(s, n)] = {b: pc.get(b, ment[n]) for b in BUDGETS} | {"missing": len(pc) < len(BUDGETS)}
        if budget:
            budget.check()
    return out


def d3_kept(fam: dict) -> list[int]:
    return [s for s, m in enumerate(fam["ments"]) if sum(1 for n, x in enumerate(m)
                                                          if fam["use"][n] > 0 and len(x) >= 5) >= MIN_N5]


def d3_cell(L: dict, cell: dict, pref: dict, keep: list[int], Wb: np.ndarray) -> dict:
    p50x = L["p50x"]
    idx = np.flatnonzero(cell["use"] > 0)
    dh = delta_hat(cell)
    e = (segsum(cell, cell["H"] * dh)[:, idx].sum(1)) / cell["M"][:, idx].sum(1)
    x = np.log(cell["M"][:, idx].mean(1))
    res = {"a": {"e": e.tolist(), "x": x.tolist(), "kendall_tau": float(p50x.tau_b(x, e))}}
    if not keep:
        return res | {"b": {"label": "NOT_EVALUABLE", "reason": f"no system with >= {MIN_N5} images reaching 5"}}
    pos = {n: j for j, n in enumerate(idx)}
    dmap: list[dict] = [{} for _ in range(cell["N"])]
    for c, i, v in zip(cell["cls"], cell["seg"], dh):
        dmap[i][c] = v
    A = {k: np.zeros((len(keep), len(idx))) for k in ("D2", "D3", "D5", "T2", "T3", "T5", "add23", "out23", "add35",
                                                     "out35", "viol")}
    for si, s in enumerate(keep):
        for (s_, n), pc in pref.items():
            if s_ != s:
                continue
            j, C = pos[n], cell["comp"][n]
            for b in BUDGETS:
                A[f"D{b}"][si, j] = sum(dmap[n].get(c, 0.0) for c in pc[b] & C)
                A[f"T{b}"][si, j] = len(pc[b])
            for a_, b_ in ((2, 3), (3, 5)):
                add = pc[b_] - pc[a_]
                A[f"add{a_}{b_}"][si, j], A[f"out{a_}{b_}"][si, j] = len(add), len(add - C)
            A["viol"][si, j] = float(pc["missing"] or not (pc[2] <= pc[3] <= pc[5]))

    def incs(mask):
        eb = {b: (Wb @ (A[f"D{b}"] * mask).sum(0)) / (Wb @ (A[f"T{b}"] * mask).sum(0)) for b in BUDGETS}
        return eb, {"2->3": eb[3] - eb[2], "3->5": eb[5] - eb[3]}

    eb, de = incs(np.ones_like(A["viol"]))
    _, de_s = incs(1 - A["viol"])
    return res | {"b": {"systems_kept": list(keep), "e_budget": {b: float(v[0]) for b, v in eb.items()},
                        "e_negative": {b: bool(v[0] < 0) for b, v in eb.items()},
                        "boot": de, "point": {k: float(v[0]) for k, v in de.items()},
                        "sensitivity_without_violations": {k: float(v[0]) for k, v in de_s.items()},
                        "nesting_violations": int(A["viol"].sum()),
                        "regime_d_share_outside": {k: float(A[f"out{k[0]}{k[3]}"].sum() / max(A[f"add{k[0]}{k[3]}"].sum(), 1))
                                                   for k in ("2->3", "3->5")}}}


def run_d3(L: dict, sets: dict, cells: dict, sizes: dict, budget) -> dict:
    recs, boots = {}, {}
    pref_cache = {}
    for (st, fam, arm), c in cells.items():
        f = sets[st]["fams"][fam]
        keep = d3_kept(f)
        if not c["evaluable"]:
            recs[c["name"]] = {"label": "NOT_EVALUABLE", "reason": c["why"]}
            continue
        if (st, fam) not in pref_cache:
            pref_cache[(st, fam)] = prefix_table(f, sets[st]["ids"], keep, budget)
        n = int((c["use"] > 0).sum())
        r = d3_cell(L, c, pref_cache[(st, fam)], keep, boot_weights(n, np.random.default_rng(seed("D3", st, fam, arm))))
        if "boot" in r["b"]:
            for k, v in r["b"].pop("boot").items():
                boots[f"{c['name']}|{k}"] = v[1:]
        recs[c["name"]] = r
        budget.check()
    if len(boots) != sizes["m_d3"]:
        raise Fault(f"D3 evaluable increments {len(boots)} differ from S0 m = {sizes['m_d3']}")
    lab = d3_labels(boots, sizes["m_d3"], L["p50x"].holm) if boots else {}
    sets_ok = t2_sets_ok(ev_by_set(cells))
    return {"cells": recs, "m": sizes["m_d3"], "increments": lab, "sesoi": SESOI, "t2_sets_ok": sets_ok,
            "label": overall([v["label"] for v in lab.values()]) if lab else "NOT_EVALUABLE",
            "counts_toward_T2": sets_ok and bool(lab) and all(v["label"] == "PASS" for v in lab.values())}


# ------------------------------------------------------------------------------------------------ D5
def d5_pairs(systems: list[str]) -> list[tuple[str, str]]:
    return [(s, s.replace("-short", "-detailed", 1)) for s in systems
            if "-short" in s and s.replace("-short", "-detailed", 1) in systems]


def d5_pair(Sm: list[set], Dm: list[set], comp: list[set], idx: np.ndarray, Wb: np.ndarray) -> dict:
    a1 = np.array([len(Sm[i] & Dm[i] & comp[i]) for i in idx], float)
    b1 = np.array([len(Sm[i] & comp[i]) for i in idx], float)
    a2 = np.array([len(Sm[i] & Dm[i]) for i in idx], float)
    b2 = np.array([len(Sm[i]) for i in idx], float)
    if b1.sum() == 0 or b2.sum() == 0:
        return {"label": "NOT_EVALUABLE", "reason": "empty denominator"}
    with np.errstate(invalid="ignore", divide="ignore"):
        s1, s2 = (Wb @ a1) / (Wb @ b1), (Wb @ a2) / (Wb @ b2)
    lo1, lo2 = float(np.nanpercentile(s1[1:], 2.5)), float(np.nanpercentile(s2[1:], 2.5))
    return {"share_gold": float(s1[0]), "share_all": float(s2[0]), "lower_gold": lo1, "lower_all": lo2,
            "label": d5_rule(lo1, lo2)}


def run_d5(L: dict, sets: dict, budget) -> dict:
    recs = {}
    for (st, fam), systems in FAMILIES.items():
        f, comp = sets[st]["fams"][fam], sets[st]["L"]
        idx = np.flatnonzero(f["use"] > 0)
        for n, (s, d) in enumerate(d5_pairs(systems)):
            Wb = boot_weights(len(idx), np.random.default_rng(seed("D5", st, fam, "L", extra=n)))
            recs[f"{st}/{fam}|{Path(s).name}"] = d5_pair(f["ments"][systems.index(s)], f["ments"][systems.index(d)],
                                                         comp, idx, Wb)
        budget.check()
    ev = {st: [v["label"] != "NOT_EVALUABLE" for k, v in recs.items() if k.startswith(f"{st}/")] for st in ARMS}
    return {"pairs": recs, "n_pairs": len(recs), "label": "DESCRIPTIVE", "t2_sets_ok": t2_sets_ok(ev),
            "rule": "lower 2.5th percentile >= 0.80 for both shares -> reading (c) ALLOWED for the pair"}


# ------------------------------------------------------------------------------------------------ D4(a), D4(b)
def sim_refs(cell: dict, sizes: np.ndarray, rng, a=None, domain=None) -> np.ndarray:
    """One simulated world: reference k of image i is an independent subset of C_i of size sizes[k, i], uniform or
    weighted by a_c without replacement (keys -ln(u)/a_c). (Kx, S) 0/1."""
    u = 1.0 - rng.random((sizes.shape[0], cell["S"]))
    keys = u if a is None else -np.log(u) / a
    if domain is not None:
        keys[:, ~domain] = np.inf
    return (ranks_from_keys(cell, keys) < sizes[:, cell["seg"]]).astype(float)


def obs_T(g, cell: dict, Z: np.ndarray, q: np.ndarray, w, metrics=T_STATS) -> dict:
    st = lin_stats(g, cell, Z[None], q, w)
    return {m: float(beta(g, st["lm"], st[m].mean(1))[0]) for m in metrics}


def d4a_world(L: dict, cell: dict, world: str, st: str, fam: str, arm: str) -> dict:
    """Fixed parts of one D4(a) cell: reference sizes, draws (level 1 and, for W-50, level 5)."""
    if world == "real":
        sizes, d1, d5 = cell["qref"], cell["d1"], None
    else:
        rng = np.random.default_rng(seed("W50", st, fam, arm))
        real = [cell["qref"][:cell["K"][i], i] for i in range(cell["N"])]
        sizes = np.array([rng.choice(r, N_SIMREFS, replace=True) for r in real], float).T
        dr = L["p50"].draw([N_SIMREFS] * cell["N"])
        d1 = np.array([[t[0] for t in sub] for sub in dr[1]], np.int64)
        d5 = np.array([list(sub) for sub in dr[5]], np.int64)
    return {"sizes": sizes, "d1": d1, "d5": d5, "levels": levels(world, arm), "shared": shared_null(world, arm)}


def d4a_sim(L: dict, cell: dict, W: dict, rng, null_rng=None, budget=None) -> dict:
    """One simulation: observed T (F, P, R) per level and the single-draw F; for W-50 arm U also the nulls of this
    simulation (redrawn at both levels, complete gold = union of the simulated references)."""
    g, w = L["g"], cell["use"]
    Zk = sim_refs(cell, W["sizes"], rng)
    Z1, q1 = draw_q(cell, Zk, W["d1"])
    o = {"T1": obs_T(g, cell, Z1, q1, w), "single": obs_T(g, cell, Zk[:1], W["sizes"][:1], w, ("F",))}
    if 5 in W["levels"]:
        Z5, q5 = draw_q5(cell, Zk, W["d5"])
        o["T5"] = obs_T(g, cell, Z5, q5, w)
    if not W["shared"] and null_rng is not None:
        dom = Zk.max(0) > 0
        o["null"] = null_stats(g, cell, {"T1": (q1, T_STATS), "single": (W["sizes"][:1], ("F",))}, w, null_rng, B_NULL,
                               domain=dom, budget=budget)
        if 5 in W["levels"]:
            o["null"] |= null_stats(g, cell, {"T5": (q5, T_STATS)}, w, null_rng, B_NULL, domain=dom, budget=budget)
    return o


def d4a_decisions(L: dict, lock: SLock, o: dict, null: dict, lev: tuple) -> dict:
    out = {}
    for m in T_STATS:
        parts = [lock.decide(o[f"T{k}"][m], null[f"T{k}"][m]) for k in lev]
        rej = L["g"].compound([v for v, _ in parts]) == "PASS" if len(lev) > 1 else parts[0][0] == "PASS"
        out[m] = (rej, max(p for _, p in parts))
    out["single"] = lock.decide(o["single"]["F"], null["single"]["F"])[1]
    return out


def run_d4a(L: dict, cells: dict, sizes: dict, budget, lock: SLock | None = None, S_override=None) -> dict:
    g, stats = L["g"], L["stats"]
    lock = lock or SLock()
    plan = []
    for world in ("real", "W50"):
        for (st, fam, arm), c in cells.items():
            if c["evaluable"]:
                plan.append((world, st, fam, arm, c, d4a_world(L, c, world, st, fam, arm)))
    m, m_sd = d4a_sizes(len(plan))
    if (m, m_sd) != (sizes["m_d4a"], sizes["m_sd"]):
        raise Fault(f"D4(a) sizes {m}, {m_sd} differ from S0 {sizes['m_d4a']}, {sizes['m_sd']}")
    shared, per_sim = {}, {}
    for world, st, fam, arm, c, W in plan:  # shared nulls and the 5 timing simulations (no p-value computed)
        key = f"{world}|{c['name']}"
        if W["shared"]:
            if 5 in W["levels"]:
                raise Fault("a shared null at level 5")
            qfix = W["sizes"][W["d1"], np.arange(c["N"])]  # q_i^(j) = size of the drawn reference, fixed
            shared[key] = null_stats(g, c, {"T1": (qfix, T_STATS), "single": (W["sizes"][:1], ("F",))}, c["use"],
                                     np.random.default_rng(seed("D4a", st, fam, arm, world)), B_NULL, budget=budget)
        rng = np.random.default_rng(seed("calib", st, fam, arm, world))
        c0, w0 = budget.used()
        for _ in range(N_CALIB):
            d4a_sim(L, c, W, rng, rng, budget)
        c1, w1 = budget.used()
        per_sim[key] = {"cpu_s": (c1 - c0) / N_CALIB, "wall_s": (w1 - w0) / N_CALIB}
    proj = {k: sum(v[k] for v in per_sim.values()) * S_D4A for k in ("cpu_s", "wall_s")}
    cpu_left, wall_left = budget.left()
    S = S_override or (S_D4A if proj["cpu_s"] <= cpu_left and proj["wall_s"] <= wall_left else S_D4A_LOW)
    lock.fix(S)
    recs, labels, sd_labels = {}, [], []
    for world, st, fam, arm, c, W in plan:
        key = f"{world}|{c['name']}"
        rng = np.random.default_rng(seed("D4a", st, fam, arm, world, extra=1))
        rej = {mm: [] for mm in T_STATS}
        ps = {mm: [] for mm in T_STATS}
        p_sd = []
        for _ in range(S):
            o = d4a_sim(L, c, W, rng, rng, budget)
            dec = d4a_decisions(L, lock, o, shared[key] if W["shared"] else o["null"], W["levels"])
            for mm in T_STATS:
                rej[mm].append(dec[mm][0])
                ps[mm].append(dec[mm][1])
            p_sd.append(dec["single"])
            budget.check()
        r = {}
        for mm in T_STATS:
            rate, ksp = float(np.mean(rej[mm])), ks_smaller(stats, np.array(ps[mm]))
            r[mm] = {"rejection_rate": rate, "bound": d4a_bound(S, m), "ks_one_sided_p": ksp,
                     "label": d4a_rule(rate, ksp, S, m)}
            labels.append(r[mm]["label"])
        ks2 = float(stats.kstest(np.array(p_sd), "uniform").pvalue)
        r["single_draw"] = {"ks_two_sided_p": ks2, "label": d4a_sd_rule(ks2, m_sd)}
        sd_labels.append(r["single_draw"]["label"])
        recs[key] = r | {"levels": list(W["levels"]), "shared_null": W["shared"]}
    return {"S": S, "projected_at_S200": proj, "timing_per_sim_discarded": per_sim, "m": m, "m_sd": m_sd, "cells": recs,
            **d4a_verdict(labels, sd_labels), "t2_sets_ok": t2_sets_ok(ev_by_set(cells)),
            "wording": "the 20-draw statistic on development data (simulated references at the real K and sizes, "
                      "level 1; 50 simulated references, levels 1 and 5)",
            "disclosure": "PASCAL-50S outputs cannot be re-checked per image; this is an analogue on development data.",
            "note_N4": "rate bound and KS each at 0.05/m per T statistic (2m tests); family-wise false-FAIL <= 0.10"}


def box_weights(cell: dict, ids: list[str]) -> np.ndarray:
    inst = jload(INSTANCES)
    cat = {c["id"]: c["name"] for c in inst["categories"]}
    area = {r["id"]: r["width"] * r["height"] for r in inst["images"]}
    want = {int(i) for i in ids}
    best: dict = {}
    for a in inst["annotations"]:
        if a["image_id"] in want:
            k = (a["image_id"], cat[a["category_id"]])
            best[k] = max(best.get(k, 0.0), a["bbox"][2] * a["bbox"][3] / area[a["image_id"]])
    return np.array([max(best[(int(ids[i]), c)], 1e-9) for c, i in zip(cell["cls"], cell["seg"])])


def d4b(L: dict, cell: dict, a: np.ndarray, rng, n_sim=S_D4B, n_w=N_W, batches=W_BATCHES, budget=None) -> dict:
    """Salience-correlated thinning (simulated references, not gold): G_bar = mean_s [T_P(sim) - T_P(rho)] against
    beta_delta (delta = w - rho, w from n_w weighted draws in `batches` batches); power = PASS rate of T (mixed F1)."""
    g, w, seg, ell = L["g"], cell["use"], cell["seg"], np.maximum(cell["ell"], 1)
    qJ, d1, sizes = cell["qJ"], cell["d1"], cell["qref"]
    lm = lin_stats(g, cell, np.zeros((1, cell["S"])), qJ[:1], w)["lm"]
    msum = cell["M"] @ w
    bd = []
    for _ in range(batches):
        r = ranks_from_keys(cell, -np.log(1.0 - rng.random((n_w // batches, cell["S"]))) / a)
        dl = np.mean([(r < qJ[j, seg]).mean(0) - (qJ[j] / ell)[seg] for j in range(qJ.shape[0])], 0)
        bd.append(float(beta(g, lm, ((cell["H"] * w[seg]) @ dl) / msum)))
        if budget:
            budget.check()
    b_delta, se_w = float(np.mean(bd)), float(np.std(bd, ddof=1) / np.sqrt(batches))
    tp_rho = obs_T(g, cell, (qJ / ell)[:, seg], qJ, w, ("P",))["P"]
    null = null_stats(g, cell, {"T1": (qJ, ("F",))}, w, rng, B_NULL, budget=budget)["T1"]["F"]
    G, rej = [], []
    for _ in range(n_sim):
        Zk = sim_refs(cell, sizes, rng, a=a)
        Z1, q1 = draw_q(cell, Zk, d1)
        o = obs_T(g, cell, Z1, q1, w, ("P", "F"))
        G.append(o["P"] - tp_rho)
        rej.append(decide(o["F"], null)[0] == "PASS")
        if budget:
            budget.check()
    Gb, se_sim = float(np.mean(G)), float(np.std(G, ddof=1) / np.sqrt(n_sim))
    return {"G_bar": Gb, "se_sim": se_sim, "beta_delta": b_delta, "se_w": se_w, "S": n_sim,
            "power_T_mixed": float(np.mean(rej)), "sign_G": int(np.sign(Gb)), "label": d4b_rule(Gb, b_delta, se_sim, se_w),
            "wording": "simulated references (not gold); no sentence about real-reference salience"}


# ------------------------------------------------------------------------------------------------ S0 helpers
def s0_sizes(sets: dict, cells: dict) -> dict:
    ev = [k for k, c in cells.items() if c["evaluable"]]
    m_lin, m_mix = d1_sizes([cells[k]["H"].shape[0] for k in ev])
    m_d3 = 2 * sum(1 for (st, fam, arm) in ev if d3_kept(sets[st]["fams"][fam]))
    m_d4a, m_sd = d4a_sizes(2 * len(ev))
    n_d2 = sum(D2_K[st] * 2 for (st, fam, arm) in ev if arm == "L")
    return {"m_lin": m_lin, "m_mix": m_mix, "n_d2_tests": n_d2, "m_d3": m_d3, "m_d4a": m_d4a, "m_sd": m_sd,
            "n_d5_pairs": sum(len(d5_pairs(v)) for v in FAMILIES.values())}


def kernel_parity(L: dict, cell: dict, golds: list[list[set]], rng_seed: int, n_rep: int) -> dict:
    """Kernel T (mixed F1) under the permutations of p50x.null_slopes / scar_null.null_slopes (same stream)."""
    g, p50x, sn = L["g"], L["p50x"], L["sn"]
    idx = np.flatnonzero(cell["use"] > 0)
    ks = [[len(x & c) for x, c in zip(gs, cell["comp"])] for gs in golds]
    a = p50x.null_slopes(g, cell["comp"], ks, cell["ments"], idx, np.random.default_rng(rng_seed), n_rep)
    st = {"comp": cell["comp"], "golds": {"x": golds}, "ments": cell["ments"], "idx": idx}
    b = sn.null_slopes(st, "x", np.random.default_rng(rng_seed), n_rep, 1e-9)
    k = T_from_ranks(g, cell, ranks_p50x_stream(cell, np.random.default_rng(rng_seed), n_rep), np.array(ks, float),
                     cell["use"], ("F",))["F"]
    return {"max_abs_diff_p50x": float(np.max(np.abs(a - k))), "max_abs_diff_scar_null": float(np.max(np.abs(b - k))),
            "ok": bool(np.max(np.abs(a - k)) <= 1e-12 and np.max(np.abs(b - k)) <= 1e-12)}


# ------------------------------------------------------------------------------------------------ subcommands
def timing() -> dict:
    t = os.times()
    return {"cpu_s": time.process_time() + t.children_user + t.children_system}


def freeze() -> int:
    env_guard()
    t0, c0 = time.monotonic(), timing()["cpu_s"]
    pins = assert_pins(list(PINS))
    old = ROOT / OUT / "freeze/freeze.json"
    if old.exists():  # CC-271 N3: a passed freeze is final; a failed one is kept renamed and S0.1-2 is redone
        if json.loads(old.read_text(encoding="utf-8")).get("pass"):
            raise Fault("refused: freeze/freeze.json exists with pass = true (S0 is frozen once)")
        old.rename(old.with_name(f"freeze.failed_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}.json"))
    ids = {"coco5000_ids.txt": [str(i) for i in sorted(int(m["cocoid"]) for m in jload(MANIFEST5000)["images"])],
           "xm3600_600_ids.txt": sorted((ROOT / "data/xm3600_subset.txt").read_text().split()),
           "uitviic231_ids.txt": sorted({str(a["image_id"]) for a in jload("data/datasets/uitviic/test_data.json")[
               "annotations"] if a.get("caption")}, key=int)}
    shas = {}
    for name, lst in ids.items():
        p = ROOT / OUT / "freeze" / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("\n".join(lst) + "\n", encoding="utf-8")
        shas[name] = sha_file(p)
    gold = ROOT / OUT / "freeze/instance_gold_full5000.json"
    r = subprocess.run([sys.executable, "-I", str(ROOT / BUILDER), str(gold)], capture_output=True, text=True)
    got = sha_file(gold) if gold.exists() else None
    ok = r.returncode == 0 and got == PINS[GOLD5000] and len(ids["coco5000_ids.txt"]) == 5000 and \
        len(ids["xm3600_600_ids.txt"]) == 600 and len(ids["uitviic231_ids.txt"]) == 231
    rec = {"schema": "vsps.a_dchecks.freeze.v1", "script_sha256": sha_file(Path(__file__)), "plan_sha256": PINS[PLAN],
           "id_lists_sha256": shas, "n_ids": {k: len(v) for k, v in ids.items()}, "builder_rc": r.returncode,
           "builder_stdout": r.stdout.strip()[-300:], "gold_sha256": got, "gold_expected": PINS[GOLD5000],
           "pins_asserted": len(pins), "pass": ok,
           "cpu_s": timing()["cpu_s"] - c0, "wall_s": time.monotonic() - t0}
    print(json.dumps({"freeze": "PASS" if ok else "FAIL", "sha256": write_json(f"{OUT}/freeze/freeze.json", rec)}))
    return 0 if ok else 1


def gate() -> int:
    env_guard()
    t0, c0 = time.monotonic(), timing()["cpu_s"]
    assert_pins(list(PINS))
    fz = jload(f"{OUT}/freeze/freeze.json")
    gold = ROOT / OUT / "freeze/instance_gold_full5000.json"
    if not fz["pass"] or sha_file(gold) != PINS[GOLD5000] or fz["script_sha256"] != sha_file(Path(__file__)) or \
            any(sha_file(ROOT / OUT / "freeze" / k) != v for k, v in fz["id_lists_sha256"].items()):
        raise Fault("freeze record missing, failed, changed, or written by another script version")
    L = load_libs()
    g, sn = L["g"], L["sn"]
    anchors = {}
    # S0.3 (a) r4 via check_coco_full.py, argv all9full (W4_TOPUP_NOTE l.126)
    rep = ROOT / OUT / "gate_anchors/r4_repro.json"
    rep.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([sys.executable, "-I", str(ROOT / CHECK_COCO_FULL), str(ROOT / MANIFEST5000), str(gold),
                        "all9full", str(rep)], capture_output=True, text=True)
    r4 = jload(R4)
    got = json.loads(rep.read_text()) if rep.exists() else {"gold": {}}
    anchors["r4_check_coco_full"] = {"rc": r.returncode, "cells": {c: got["gold"].get(c) == r4["gold"][c]
                                                                    for c in R4_CELLS}}
    anchors["r4_check_coco_full"]["ok"] = r.returncode == 0 and all(anchors["r4_check_coco_full"]["cells"].values())
    # (b) the same cells through the a_dchecks COCO context (all 5,000 images, no clean rule, as r4)
    sets = load_sets(L)
    d = sets["coco"]
    f = d["fams"]["F1"]
    n = len(d["ids"])
    rng = np.random.default_rng(1)  # check_coco_full stream: W first, then refs1_randk
    rng.multinomial(n, np.full(n, 1 / n), size=500)
    randk = [[set().union(*[d["refs"][i][j] for j in rng.choice(len(d["refs"][i]), 1, replace=False)])
              for i in range(n)] for _ in range(20)]
    var = {"inst": [d["L"]], "refs1_firstk": [[r[0] for r in d["refs"]]], "refs1_randk": randk,
           "refs5_firstk": [[set().union(*r[:5]) for r in d["refs"]]]}
    one, idx = np.ones((1, n)), np.arange(n)
    ctx = {}
    for cname, golds in var.items():
        sl = [g.scores(g.rows(m, golds), idx, one) for m in f["ments"]]
        mine = float(g.stat_slope(sl, 1e-9)[0])
        med = float(np.median([float(s["M"][0]) for s in sl]))
        ctx[cname] = {"slope": round(mine, 2), "median_M": round(med, 2),
                      "ok": round(mine, 2) == r4["gold"][cname]["slope"] and round(med, 2) == r4["gold"][cname]["median_M"]}
    anchors["r4_a_dchecks_context"] = {"cells": ctx, "ok": all(v["ok"] for v in ctx.values())}
    # (c) check_coco.json (2,500), c2_n1 all_10, xm3600_full_verdict v2: score_g2b.selfcheck unchanged
    rc = g.selfcheck(ROOT / OUT / "gate_anchors/g2b_selfcheck.json")
    anchors["g2b_selfcheck"] = {"rc": rc, "ok": rc == 0}
    # (d) scar_null_result observed cells for xm600, uv231 and s75
    reg, res = g.jload(g.PREREG), jload(SCAR_RESULT)["results"]
    lang = {x["run_id"]: ("en" if x["prompt_mode"].endswith("_en") else "vi") for x in reg["runs"]}
    floor = reg["design_constants"]["tp_floor"]["value"]
    scar = {}
    for name in ("uv231", "xm600"):
        lad = reg["families"][name]["LADDER"]
        ds = g.Dataset(reg, name, {x: g.read_captions(sn.OUTPUTS / f"{x}.preds.json") for x in lad}, lang)
        lx = next(iter(ds.lex))
        lex = ds.lex[lx]
        comp = [set(c) for c in lex["complete"]] if "complete" in lex else \
            [{c for c, v in s.items() if v == "present"} for s in lex["oiv7"]]
        ments, ix = [ds.ment(s, lx) for s in lad], ds.clean_index(lad, True)
        for lev in sn.LEVELS:
            v = sn.slope(ments, sn.intersect(ds.variants[lx][lev], comp), ix, floor)
            scar[f"{name}/{lev}"] = v == res[f"{name}/{lev}"]["observed_intersection_slope"]
    x = g.xm3600_context()["lexicons"]["objects_in"]
    comp = [{c for c, v in s.items() if v == "present"} for s in x["oiv7"]]
    xs = sets["xm"]["fams"]["F1"]  # s75 systems in scar_null order: sorted xm3600/*.preds.json
    ments = [xs["ments"][xs["systems"].index(s)] for s in sorted(xs["systems"])]
    for lev, golds in (("refs1_randk", sn.s75_randk(x["refs"])), ("refs_all", g.gold_variants(x, None)["refs_all"])):
        v = sn.slope(ments, sn.intersect(golds, comp), np.arange(len(comp)), floor)
        scar[f"s75/{lev}"] = v == res[f"s75/{lev}"]["observed_intersection_slope"]
    anchors["scar_observed"] = {"cells": scar, "ok": all(scar.values())}
    # kernel gate: synthetic (selftest) and 5 replicates of each real cell, against p50x and scar_null
    cells = build_cells(sets)
    kg = {}
    for (st, fam, arm), c in cells.items():
        refs = sets[st]["refs"]
        golds = [[refs[i][int(c["d1"][j, i])] & c["comp"][i] for i in range(c["N"])] for j in range(c["d1"].shape[0])]
        kg[c["name"]] = kernel_parity(L, c, golds, seed("gate", st, fam, arm), 5)
    st_ok = selftest_core(L)["pass"]
    # S0.4 record
    speed, n5, ev = {}, {}, {}
    for (st, fam, arm), c in cells.items():
        t1 = time.monotonic()
        null_stats(g, c, {"T1": (c["qJ"], T_STATS)}, c["use"], np.random.default_rng(seed("speed", st, fam, arm)), 100)
        speed[c["name"]] = (time.monotonic() - t1) / 100
        fm = sets[st]["fams"][fam]
        n5[c["name"]] = {Path(s).name: int(sum(1 for i, m in enumerate(fm["ments"][k]) if fm["use"][i] > 0 and len(m) >= 5))
                         for k, s in enumerate(fm["systems"])}
        ev[c["name"]] = {"evaluable": c["evaluable"], "reason": c["why"], "n_scored": int((c["use"] > 0).sum()),
                         "n_slots": c["S"]}
    sizes = s0_sizes(sets, cells)
    counts_ok = all(int(sets[st]["fams"]["F2"]["use"].sum()) == n for st, n in F2_SCORED.items())
    try:  # CC-271 N2: loaded ids = frozen id lists
        assert_frozen_ids(sets)
        ids_ok = True
    except Fault:
        ids_ok = False
    bw = box_weights(cells[("coco", "F1", "L")], sets["coco"]["ids"])  # CC-271 N4: D4(b) input path, no D statistic
    bw_rec = {"n_slots": int(bw.size), "n_floored_1e-9": int((bw == 1e-9).sum()), "all_finite": bool(np.isfinite(bw).all()),
              "ok": bool(np.isfinite(bw).all() and bw.size == cells[("coco", "F1", "L")]["S"])}
    # S0.5 re-hash every input (and the 61 scar_null_result input pins)
    assert_pins(list(PINS))
    scar_pins = jload(SCAR_RESULT)["pins"]
    rehash = all(sha_file(ROOT / p) == v["sha256"] for p, v in scar_pins.items())
    ok = all(a["ok"] for a in anchors.values()) and all(v["ok"] for v in kg.values()) and st_ok and counts_ok and \
        rehash and ids_ok and bw_rec["ok"]
    rec = {"schema": "vsps.a_dchecks.gate.v1", "script_sha256": sha_file(Path(__file__)), "plan_sha256": PINS[PLAN],
           "statistics_computed": "anchors and kernel parity only; no D statistic", "anchors": anchors,
           "kernel_gate": kg, "selftest_core_pass": st_ok, "kernel_s_per_replicate_J20": speed,
           "n5_per_system_and_arm": n5, "cells": ev, "family_sizes": sizes, "f2_scored_counts_ok": counts_ok,
           "scar_result_pins_rehash_ok": rehash, "frozen_ids_ok": ids_ok, "box_weights": bw_rec,
           "outputs_beyond_plan_s6": list(OUTPUTS_BEYOND_S6), "n_pins": len(PINS), "pass": ok,
           "cpu_s": timing()["cpu_s"] - c0, "wall_s": time.monotonic() - t0}
    print(json.dumps({"gate": "PASS" if ok else "FAIL", "sha256": write_json(f"{OUT}/gate.json", rec)}))
    return 0 if ok else 1


def run() -> int:
    env_guard()
    assert_pins(list(PINS))
    for rel in (SELF, PLAN):
        if git_blob_sha(rel) != sha_file(ROOT / rel):
            raise Fault(f"refused: {rel} differs from its HEAD blob")
    if (ROOT / OUT / "dchecks_result.json").exists():
        raise Fault("refused: dchecks_result.json exists (one pass; a resume needs a new plan version)")
    gt, fz = jload(f"{OUT}/gate.json"), jload(f"{OUT}/freeze/freeze.json")
    if not (gt["pass"] and fz["pass"] and gt["script_sha256"] == sha_file(Path(__file__))):
        raise Fault("refused: S0 gate missing, failed, or from another script version")
    budget = Budget(cpu0=fz["cpu_s"] + gt["cpu_s"], wall0=fz["wall_s"] + gt["wall_s"])
    head = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    base = {"schema": "vsps.a_dchecks.result.v1", "status": "POST_HOC descriptive; development data; no verdict on any "
            "registered prediction", "script_sha256": sha_file(Path(__file__)), "plan_sha256": PINS[PLAN],
            "gate_sha256": sha_file(ROOT / OUT / "gate.json"), "head": head, "order": list(ORDER),
            "result_read_notes": RESULT_READ_NOTES}

    def prepare():
        L = load_libs()
        sets = load_sets(L)
        assert_frozen_ids(sets)
        cells = build_cells(sets)
        sizes = s0_sizes(sets, cells)
        if sizes != gt["family_sizes"]:
            raise Fault(f"family sizes differ from S0: {sizes} != {gt['family_sizes']}")
        coco_L = cells[("coco", "F1", "L")]
        steps = [("D1", lambda: run_d1(L, cells, sizes, budget)), ("D5", lambda: run_d5(L, sets, budget)),
                 ("D2", lambda: run_d2(L, cells, budget)), ("D3", lambda: run_d3(L, sets, cells, sizes, budget)),
                 ("D4b", lambda: d4b(L, coco_L, box_weights(coco_L, sets["coco"]["ids"]),
                                     np.random.default_rng(seed("D4b")), budget=budget) | {"t2_sets_ok": True}
                  if coco_L["evaluable"] else {"label": "NOT_EVALUABLE", "reason": coco_L["why"], "t2_sets_ok": False}),
                 ("D4a", lambda: run_d4a(L, cells, sizes, budget))]
        return steps, {"family_sizes": sizes}

    def write_result(rec):
        rec = base | rec
        print(json.dumps({"result_sha256": write_json(f"{OUT}/dchecks_result.json", rec),
                          "labels": {k: v.get("label") for k, v in rec["checks"].items()}}))
        write_json(f"{OUT}/run_record/timing.json", {"head": head, "cpu_s_total": rec["cpu_s_total"],
                                                     "wall_s_total": rec["wall_s_total"], "cap_cpu_s": CAP_CPU_S,
                                                     "cap_wall_s": CAP_WALL_S})

    start = {"head": head, "script_sha256": base["script_sha256"], "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                                                                       time.gmtime())}
    res = run_attempt(ROOT / OUT / "run_record/STARTED.json", start, prepare, budget, write_result)
    return 0 if all(v["label"] not in ("FAULT", "NOT_RUN") for v in res.values()) else 1


def assert_frozen_ids(sets: dict) -> None:
    """CC-271 N2: the ids the checks load equal the frozen id lists (5,000 / 600 / 231)."""
    for st, name in (("coco", "coco5000_ids.txt"), ("xm", "xm3600_600_ids.txt"), ("uit", "uitviic231_ids.txt")):
        frozen = (ROOT / OUT / "freeze" / name).read_text(encoding="utf-8").split()
        if sets[st]["ids"] != frozen:
            raise Fault(f"{st}: loaded ids differ from freeze/{name}")


def dryrun() -> int:
    pins = assert_pins(list(PINS))
    est = {"S0": 20, "D1": 15, "D2": 10, "D3": 30, "D4b": 30, "D4a": 60, "D5": 5}
    plan = {
        "pins_asserted": len(pins), "plan_sha256": PINS[PLAN], "order": list(ORDER),
        "cells_D1_D3": [f"{s}/{f}/{a}" for s, f, a in CELLS],
        "systems_per_family": {f"{s}/{f}": len(v) for (s, f), v in FAMILIES.items()},
        "D1": f"B = {B_D1} uniform q-subsets per cell, linear {LINEAR} + mixed F1; single draw (ref 1) ruled, T20 beside",
        "D2": f"arm L cells, k = 1..K (COCO/UIT 5, XM 2), P and micro-F1 in Holm, R descriptive, {B_BOOT} resamples",
        "D3": f"(a) Kendall tau; (b) prefix budgets {BUDGETS}, systems with >= {MIN_N5} images reaching 5, SESOI {SESOI}",
        "D4a": f"worlds real + W50 x {len(CELLS)} cells, null B = {B_NULL}, S = {S_D4A} (or {S_D4A_LOW} after timing)",
        "D4b": f"COCO-5000 arm L F1, S = {S_D4B}, w from {N_W} weighted draws in {W_BATCHES} batches",
        "D5": f"{sum(len(d5_pairs(v)) for v in FAMILIES.values())} short/detailed pairs, lower 2.5th pct >= {D5_MIN}",
        "cap": "6 CPU-h or 4 h wall; NOT_RUN for the running and every later check",
        "cpu_estimate_min_plan_s6": est, "cpu_estimate_total_h": round(sum(est.values()) / 60, 2),
        "kernel_speed": "unmeasured until S0.4 (gate)",
        "run_would_refuse_now": [r for r in (SELF, PLAN) if git_blob_sha(r) != sha_file(ROOT / r)],
        "outputs": [f"{OUT}/freeze/", f"{OUT}/gate.json", f"{OUT}/selftest.json", f"{OUT}/dchecks_result.json",
                    f"{OUT}/run_record/"], "outputs_beyond_plan_s6": list(OUTPUTS_BEYOND_S6),
        "result_read_notes": list(RESULT_READ_NOTES)}
    print(json.dumps(plan, indent=1))
    return 0


# ------------------------------------------------------------------------------------------------ selftest
def synth(rng, N=60, nsys=5, K=5, vocab=14) -> dict:
    """Synthetic set: salience-ordered C_i, references favouring the first class, nested growing mentions with
    hallucinations, one image with empty C_i."""
    words = [f"c{j:02d}" for j in range(vocab)]
    comp = [list(rng.choice(words, int(rng.integers(1, 6)), replace=False)) for _ in range(N)]
    comp[3] = []
    refs = [[{c for t, c in enumerate(cs) if rng.random() < (0.9 if t == 0 else 0.2)}
             | ({words[-1]} if rng.random() < 0.2 else set()) for _ in range(K)] for cs in comp]
    ments = [[set(cs[:1 + s]) | ({words[(s + n) % vocab]} if s >= 2 and n % 3 else set()) for n, cs in enumerate(comp)]
             for s in range(nsys)]
    return {"comp": [set(c) for c in comp], "refs": refs, "ments": ments, "N": N}


def synth_cell(L: dict, rng, arm="L", **kw) -> dict:
    s = synth(rng, **kw)
    comp = s["comp"] if arm == "L" else [set().union(*r) for r in s["refs"]]
    refs = [[r & c for r in rs] for rs, c in zip(s["refs"], comp)]
    c = make_cell("synth", comp, s["ments"], refs, np.ones(s["N"]))
    c["d1"] = np.array([[t[0] for t in sub] for sub in L["p50"].draw([len(r) for r in refs])[1]], np.int64)
    c["qref"] = segsum(c, c["Zref"]).round()
    c["qJ"], c["q1"] = draw_q(c, c["Zref"], c["d1"])[1], c["qref"][:1]
    c["evaluable"], c["why"] = evaluable(c, c["qJ"], arm)
    return c


def selftest_core(L: dict) -> dict:
    g, p50x, stats = L["g"], L["p50x"], L["stats"]
    checks: dict[str, bool] = {}

    def check(name, fn):
        try:
            checks[name] = bool(fn())
        except (Exception, SystemExit) as e:  # noqa: BLE001  (a raised check or FAULT is a failed check, named)
            checks[name] = False
            checks[f"{name} [raised {type(e).__name__}: {str(e)[:80]}]"] = False

    rng = np.random.default_rng(7)
    cell = synth_cell(L, rng)
    w = cell["use"]

    # Thm N.1: exact enumeration of the null on a tiny cell; every linear metric and slope equals the closed form
    def thm_n1():
        import itertools
        comp = [{"a", "b", "c"}, {"a", "d"}, {"e"}, set()]
        ments = [[{"a"}, {"d"}, set(), {"x"}], [{"a", "b", "x"}, {"a", "d"}, {"e"}, {"y"}], [{"a", "b", "c", "y"},
                 {"a", "d", "z"}, {"e", "x"}, {"x", "y"}]]
        q = np.array([[2, 1, 1, 0]], float)
        c = make_cell("tiny", comp, ments, [[x] for x in comp], np.ones(4))
        subs = [list(itertools.combinations(range(int(c["ell"][i])), int(q[0, i]))) for i in range(4)]
        acc = []
        for combo in itertools.product(*subs):
            Z = np.zeros(c["S"])
            for i, sub in enumerate(combo):
                Z[c["start"][i] + np.array(sub, int)] = 1
            acc.append(lin_stats(g, c, Z[None], q, c["use"]))
        cl = lin_stats(g, c, (q / np.maximum(c["ell"], 1))[:, c["seg"]], q, c["use"])
        return all(np.allclose(np.mean([a[m] for a in acc], 0), cl[m], atol=1e-12, rtol=0) and
                   abs(np.mean([beta(g, a["lm"], a[m]) for a in acc]) - beta(g, cl["lm"], cl[m])[0]) < 1e-12
                   for m in LINEAR)
    check("Thm N.1: exact null mean of P, R, MU, CH and their slopes = closed form (enumeration)", thm_n1)

    def scores_parity():
        Z, q = draw_q(cell, cell["Zref"], cell["d1"][:1])
        golds = [[{c for c, z in zip(cell["cls"][cell["start"][i]:cell["start"][i + 1]],
                                     Z[0, cell["start"][i]:cell["start"][i + 1]]) if z} for i in range(cell["N"])]]
        mine = lin_stats(g, cell, Z, q, w)
        idx, one = np.arange(cell["N"]), np.ones((1, cell["N"]))
        ref = [g.scores(g.rows(m, golds), idx, one) for m in cell["ments"]]
        return all(np.allclose(mine[k][0], [r[k][0] for r in ref], atol=1e-12) for k in ("P", "R", "F"))
    check("lin_stats P, R, mixed F1 = score_g2b.scores on the same gold", scores_parity)

    def kernel():
        golds = [[(cell_refs[i][int(cell["d1"][j, i])] & cell["comp"][i]) for i in range(cell["N"])] for j in range(20)]
        return kernel_parity(L, cell, golds, 11, 6)["ok"]
    cell_refs = [[{c for c, z in zip(cell["cls"][cell["start"][i]:cell["start"][i + 1]],
                                     cell["Zref"][k, cell["start"][i]:cell["start"][i + 1]]) if z}
                  for k in range(int(cell["K"][i]))] for i in range(cell["N"])]
    check("kernel = p50x.null_slopes = scar_null.null_slopes under shared permutations (1e-12)", kernel)

    def decide_parity():
        golds = [[(cell_refs[i][int(cell["d1"][j, i])]) for i in range(cell["N"])] for j in range(20)]
        r = p50x.salience(g, cell["ments"], golds, cell["comp"], np.arange(cell["N"]), np.random.default_rng(5), 40, True)
        ks = np.array([[len(x & c) for x, c in zip(gs, cell["comp"])] for gs in golds], float)
        null = T_from_ranks(g, cell, ranks_p50x_stream(cell, np.random.default_rng(5), 40), ks, w, ("F",))["F"]
        obs = obs_T(g, cell, draw_q(cell, cell["Zref"], cell["d1"])[0], cell["qJ"], w, ("F",))["F"]
        v, p = decide(obs, null)
        return v == r["verdict"] and p == r["p_one_sided"] and abs(obs - r["observed"]) < 1e-12
    check("decide() and the observed T reproduce p50x.salience (verdict, p, observed)", decide_parity)

    # N.5(c) step identity, check_v2 E1 / E2: theory arithmetic only, labelled math-only (CC-271 N5)
    def n5c():
        r = np.random.default_rng(3)
        D, tau, d, t, qp = r.normal(size=20000), r.uniform(1, 9, 20000), r.normal(size=20000), r.uniform(.1, 5, 20000), \
            r.uniform(0, 5, 20000)
        p_ok = np.all(((D + d) / (tau + t) <= D / tau + 1e-12) == (d / t <= D / tau + 1e-12))
        mu_ok = np.all(((D + d) / (tau + t + qp) <= D / (tau + qp) + 1e-12) == (d / t <= D / (tau + qp) + 1e-12))
        return p_ok and mu_ok
    check("math-only (no production code), N.5(c): e_P step <=> d/t <= D/tau; micro-F1 d/t <= D/(tau + q+) (20,000 cases)", n5c)
    check("math-only (no production code), check_v2 E1: t_S < 0 flips the precision-type equivalence", lambda: (-0.4 / -5 <= 1 / 10)
          and (1 - 0.4) / (10 - 5) > 1 / 10)
    check("math-only (no production code), check_v2 E2: a newly covered image with excess +0.5 raises caption-CHAIR excess 0 -> 0.25",
          lambda: (0 / 1) / 2 == 0 and (0 / 1 + 0.5 / 1) / 2 == 0.25)

    # D1: family sizes, rule branches, end-to-end on synthetic data
    lay = [9, 9, 6, 6, 10, 10, 6, 6]
    check("D1 m_lin = 4 x (systems + 1) per cell, m_mix = systems (N-B1)", lambda: d1_sizes(lay) == (280, 62))
    check("D1 rule: max|z| 3.2 passes at m_lin = 280 (would fail at m = cells)",
          lambda: d1_rule([3.2, -1.0], [0.0], [1.0], [0.1], 280, 62)["linear"] == "PASS"
          and d1_rule([4.0], [0.0], [1.0], [0.1], 280, 62)["linear"] == "FAIL")
    check("D1 rule: mixed per-system one-sided bound and the 0.5-point slope tolerance",
          lambda: d1_rule([0], [-5.0], [1.0], [0.1], 280, 62)["mixed"] == "FAIL"
          and d1_rule([0], [-2.0], [1.0], [0.1], 280, 62)["mixed"] == "PASS"
          and d1_rule([0], [0.0], [1.0], [0.6], 280, 62)["mixed"] == "FAIL")
    check("zstat: zero SE gives 0 for an exact match and inf otherwise",
          lambda: zstat(1.0, 1.0, 0.0) == 0.0 and np.isinf(zstat(1.0, 0.9, 0.0)))

    def d1_e2e():
        r = d1_cell(L, cell, np.random.default_rng(2), 3000)["single"]
        z = [x for m in LINEAR for x in r[m]["z"]]
        m_lin, m_mix = d1_sizes([cell["H"].shape[0]])
        return d1_rule(z, r["F"]["gap_plugin_minus_mc"], r["F"]["mc_se"], [r["F"]["slope_err"]], m_lin,
                       m_mix)["linear"] == "PASS"
    check("D1 end to end: the exact closed form passes the linear rule on synthetic data", d1_e2e)

    # D2
    def d2():
        r = d2_cell(L, cell, 5, boot_weights(cell["N"], np.random.default_rng(4), 200))
        per = [r[f"k{k}|P"]["D"] for k in range(1, 6)]
        return abs(r["guard_mean_k_D_P"]) < 1e-10 and max(abs(x) for x in per) > 1e-3 and len(set(np.round(per, 9))) > 1
    check("D2: per-k D^(k) nonzero and distinct; mean_k D for P = 0 (guard only, B3)", d2)
    holm = p50x.holm
    check("D2 labels: Holm rejection FAIL; wide CI UNDERPOWERED; else PASS",
          lambda: d2_labels({"a": {"p": 0.001, "half": 0.1, "g_obs": 1.0}, "b": {"p": 0.5, "half": 0.6, "g_obs": 1.0},
                             "c": {"p": 0.5, "half": 0.4, "g_obs": 1.0}}, holm) == {"a": "FAIL", "b": "UNDERPOWERED",
                                                                                     "c": "PASS"})
    check("two-sided bootstrap p", lambda: boot_p2(np.array([1.0, 2, 3])) == 0.5 and boot_p2(np.array([-1.0, 1])) == 1.0)

    # D3
    def d3_rules():
        r = np.random.default_rng(9)
        B = 2000
        cases = {"pass": r.normal(-0.02, 0.005, B), "under": r.normal(0.0, 0.02, B), "fail": r.normal(0.05, 0.005, B),
                 "overlap": r.uniform(0.002, 0.008, B)}
        lab = d3_labels(cases, 4, holm)
        disjoint = all((v["label"] == "FAIL") == v["holm_rejects"] for v in lab.values())
        return [lab[k]["label"] for k in ("pass", "under", "fail", "overlap")] == ["PASS", "UNDERPOWERED", "FAIL",
                                                                                   "FAIL"] and disjoint and \
            lab["overlap"]["upper"] <= SESOI
    check("D3 labels: PASS / UNDERPOWERED (no SESOI pass) / FAIL; Holm-level overlap (upper <= 0.01) is FAIL", d3_rules)
    check("D3 p rule (N2''): (1 + #{de* <= 0}) / (B + 1)", lambda: d3_p(np.array([-1.0, 0.0, 1.0, 2.0])) == 3 / 5)
    check("D3 labels exhaustive and single-valued on random grids", lambda: all(
        d3_labels({"x": np.random.default_rng(s).normal(np.random.default_rng(s).uniform(-.03, .03), .01, 500)}, 3,
                  holm)["x"]["label"] in ("PASS", "FAIL", "UNDERPOWERED") for s in range(40)))

    def prefix():
        fn = lambda s: {x for x in s.split() if x.startswith("c")}  # noqa: E731
        pc = prefix_classes("c1 a c2  b c3 c4 d c5 c6", fn)
        nonmono = lambda s: {x for x in s.split() if x.startswith("c")} - ({"c1"} if "no" in s.split() else set())  # noqa: E731
        pv = prefix_classes("c1 c2 no c3 c4 c5", nonmono)
        return pc == {2: {"c1", "c2"}, 3: {"c1", "c2", "c3"}, 5: {"c1", "c2", "c3", "c4", "c5"}} and \
            not pv[2] <= pv[3]
    check("D3(b): shortest word-boundary prefix per budget; a non-nested prefix is visible", prefix)

    def d3_cell_run():
        r_ = np.random.default_rng(12)
        N, words = 150, [f"c{j:02d}" for j in range(20)]
        comp = [list(r_.choice(words[:15], int(r_.integers(3, 9)), replace=False)) for _ in range(N)]
        ments = [[set(cs[:s + 1]) | {words[15 + (n + s) % 5]} for n, cs in enumerate(comp)] for s in range(6)]
        refs = [[{cs[0]} | {c for c in cs[1:] if r_.random() < 0.3} for _ in range(5)] for cs in comp]
        ids = list(map(str, range(N)))
        fam = {"systems": [f"s{k}" for k in range(6)], "ments": ments, "use": np.ones(N), "fn": lambda x: set(x.split()),
               "caps": {f"s{k}": dict(zip(ids, [" ".join(sorted(m)) for m in ments[k]])) for k in range(6)}}
        keep = d3_kept(fam)
        c = make_cell("d3", [set(x) for x in comp], ments, refs, np.ones(N))
        r = d3_cell(L, c, prefix_table(fam, ids, keep), keep, boot_weights(N, np.random.default_rng(1), 100))
        return keep == [3, 4, 5] and set(r["b"]["boot"]) == {"2->3", "3->5"} and r["b"]["nesting_violations"] == 0 \
            and np.isfinite(r["a"]["kendall_tau"])
    check("D3(b) end to end: systems below 100 images reaching 5 dropped; two increments", d3_cell_run)

    # D5
    def d5():
        Wb = boot_weights(100, np.random.default_rng(0), 400)
        near = d5_pair([{"a"}] * 100, [{"a"}] * 82 + [set()] * 18, [{"a", "b"}] * 100, np.arange(100), Wb)
        far = d5_pair([{"a"}] * 100, [{"a"}] * 99 + [set()], [{"a", "b"}] * 100, np.arange(100), Wb)
        return d5_rule(0.81, 0.85) == "ALLOWED" and d5_rule(0.79, 0.95) == "PREFIX_ONLY" and \
            near["share_gold"] >= D5_MIN > near["lower_gold"] and near["label"] == "PREFIX_ONLY" and far["label"] == "ALLOWED"
    check("D5 rule on the lower bound, never the point estimate (point 0.82, lower < 0.80 -> PREFIX_ONLY)", d5)
    check("D5 pairs: same-model short/detailed only; 18 pairs in the plan's families",
          lambda: sum(len(d5_pairs(v)) for v in FAMILIES.values()) == 18 and
          all(VCD not in s for v in FAMILIES.values() for p in d5_pairs(v) for s in p))

    # D4(a): levels, sharing, sizes, rules, KS direction, null redraws
    check("levels: arm L 1 only; arm U at real K = 5 level 1 only; W-50 arm U {1, 5}",
          lambda: levels("real", "L") == (1,) and levels("real", "U") == (1,) and levels("W50", "L") == (1,)
          and levels("W50", "U") == (1, 5))
    check("shared null only where q is a fixed reference size (not W-50 arm U)",
          lambda: shared_null("real", "L") and shared_null("real", "U") and shared_null("W50", "L")
          and not shared_null("W50", "U"))
    check("D4(a) m = 48, m_sd = 16 on the plan layout (N1'')", lambda: d4a_sizes(2 * len(CELLS)) == (48, 16))
    check("D4(a) bound 0.059 at S = 200 and 0.073 at S = 100, m = 48 (N3'')",
          lambda: round(d4a_bound(200, 48), 3) == 0.059 and round(d4a_bound(100, 48), 3) == 0.073)
    check("D4(a) rule: rate above bound FAIL; KS rejection FAIL; else PASS; single-draw KS at 0.05/m_sd",
          lambda: d4a_rule(0.07, 0.5, 200, 48) == "FAIL" and d4a_rule(0.02, 0.0001, 200, 48) == "FAIL"
          and d4a_rule(0.02, 0.5, 200, 48) == "PASS" and d4a_sd_rule(0.002, 16) == "FAIL"
          and d4a_sd_rule(0.004, 16) == "PASS")

    def ks_dir():
        r = np.random.default_rng(8)
        return ks_smaller(stats, r.beta(0.5, 1, 400)) < 0.001 and ks_smaller(stats, r.uniform(size=400)) > 0.01 \
            and ks_smaller(stats, r.beta(2, 1, 400)) > 0.01
    check("one-sided KS rejects p smaller than U(0,1), not uniform or larger p", ks_dir)

    def slock():
        lk = SLock()
        lk.fix(200)
        lk.decide(0.0, np.arange(10.0))
        try:
            lk.fix(100)
        except Fault:
            return lk.S == 200
        return False
    check("S cannot change after a p-value", slock)

    def d4a_mini():
        cu = synth_cell(L, np.random.default_rng(21), arm="U", N=30)
        cells_ = {("uit", "F2", "U"): cu}
        NULL_CALLS["n"] = 0
        W = d4a_world(L, cu, "W50", "uit", "F2", "U")
        o = d4a_sim(L, cu, W, np.random.default_rng(0), np.random.default_rng(1))
        sub_ok = NULL_CALLS["n"] == 2 and {"T1", "T5", "single"} <= set(o["null"])
        sizes_ok = all(set(W["sizes"][:, i]) <= set(cu["qref"][:cu["K"][i], i]) for i in range(cu["N"]))
        Zk = sim_refs(cu, cu["qref"], np.random.default_rng(3))
        exact = np.array_equal(segsum(cu, Zk).round(), cu["qref"])
        r = run_d4a(L, cells_, {"m_d4a": 6, "m_sd": 2}, Budget(), S_override=3)
        return sub_ok and sizes_ok and exact and r["S"] == 3 and set(r["cells"]) == {"real|synth", "W50|synth"} and \
            r["cells"]["W50|synth"]["levels"] == [1, 5] and not r["cells"]["W50|synth"]["shared_null"]
    check("D4(a): W-50 arm U redraws nulls per simulation at both levels; sizes from real sizes; exact sizes", d4a_mini)

    def wdraw():
        c = make_cell("w", [{"a", "b"}], [[{"a"}], [{"a", "b"}]], [[{"a"}]], np.ones(1))
        Zk = sim_refs(c, np.ones((20000, 1)), np.random.default_rng(0), a=np.array([3.0, 1.0]))
        return abs(Zk[:, 0].mean() - 0.75) < 0.01 and np.all(Zk.sum(1) == 1)
    check("weighted draw without replacement: P(first of a = (3, 1), q = 1) = 0.75", wdraw)
    check("D4(b) rule: inside 2 sqrt(SE_sim^2 + SE_w^2) PASS, outside FAIL",
          lambda: d4b_rule(1.0, 1.05, 0.03, 0.01) == "PASS" and d4b_rule(1.0, 1.1, 0.03, 0.01) == "FAIL")

    def d4b_mini():
        r = d4b(L, cell, np.linspace(0.1, 1, cell["S"]), np.random.default_rng(5), n_sim=8, n_w=400, batches=4)
        return r["label"] in ("PASS", "FAIL") and np.isfinite(r["G_bar"]) and np.isfinite(r["beta_delta"])
    check("D4(b) end to end on synthetic data", d4b_mini)

    # fail-closed COCO gold, evaluability, seeds, cap
    def coco_fail():
        try:
            coco_complete(["1", "2"], {"1": {"coco": ["dog"]}})
        except Fault:
            return coco_complete(["1"], {"1": {"coco": ["dog"]}}) == [{"dog"}]
        return False
    check("COCO context fail-closed: a missing id is a FAULT, never .get(i, {})", coco_fail)
    check("evaluability: one distinct M or the X5 rule -> NOT_EVALUABLE", lambda: not evaluable(
        make_cell("e", [{"a"}, {"b"}], [[{"a"}, {"b"}], [{"a"}, {"b"}]], [[{"a"}], [{"b"}]], np.ones(2)),
        np.array([[1.0, 1.0]]), "U")[0] and not evaluable(cell, cell["ell"][None].astype(float), "L")[0]
        and evaluable(cell, cell["qJ"], "L")[0])
    check("seeds: distinct across checks, sets, families, arms and worlds", lambda: len({
        seed(c, s, f, a, wd) for c in OFF["check"] for s in OFF["set"] for f in OFF["fam"] for a in OFF["arm"]
        for wd in OFF["world"]}) == len(OFF["check"]) * 3 * 2 * 2 * 2)

    def decide_branches():
        null = np.arange(100.0)  # 2.5th pct 2.475, median 49.5
        return decide(0.0, np.ones(50))[0] == "NOT_EVALUABLE" and decide(1.0, null) == ("PASS", 3 / 101) and \
            decide(60.0, null)[0] == "FAIL" and decide(49.5, null)[0] == "FAIL" and decide(10.0, null)[0] == "INCONCLUSIVE"
    check("decide(): NOT_EVALUABLE / PASS / FAIL (at or above median) / INCONCLUSIVE, p = (1 + #{null <= obs})/(B + 1)",
          decide_branches)

    def compound():
        lk = SLock()
        lk.fix(10)
        null = np.arange(100.0)
        nl = {"T1": {m: null for m in T_STATS}, "T5": {m: null for m in T_STATS}, "single": {"F": null}}
        o = lambda a, b: {"T1": {m: a for m in T_STATS}, "T5": {m: b for m in T_STATS}, "single": {"F": 50.0}}  # noqa: E731
        mixed, both = d4a_decisions(L, lk, o(0.0, 60.0), nl, (1, 5)), d4a_decisions(L, lk, o(0.0, 1.0), nl, (1, 5))
        one = d4a_decisions(L, lk, o(0.0, 60.0), nl, (1,))
        return mixed["F"] == (False, 62 / 101) and both["F"] == (True, 3 / 101) and one["F"] == (True, 2 / 101) and \
            mixed["single"] == 52 / 101
    check("D4(a) compound (W-50 arm U): rejection only if both levels PASS; p = max over levels", compound)
    check("stop decisions: D1 linear FAIL and D4(a) single-draw FAIL stop the run; other FAILs do not",
          lambda: d1_verdict({"linear": "FAIL", "mixed": "PASS"}) == {"label": "FAIL", "stop": d1_verdict(
              {"linear": "FAIL", "mixed": "PASS"})["stop"]} and "stop" in d1_verdict({"linear": "FAIL", "mixed": "PASS"})
          and d1_verdict({"linear": "PASS", "mixed": "FAIL"}) == {"label": "FAIL"}
          and d1_verdict({"linear": "PASS", "mixed": "PASS"}) == {"label": "PASS"}
          and "stop" in d4a_verdict(["PASS"], ["FAIL"]) and d4a_verdict(["FAIL"], ["PASS"]) == {
              "label": "FAIL", "single_draw_label": "PASS"} and d4a_verdict(["PASS"], ["PASS"])["label"] == "PASS")
    check("T2 set rule: every named set needs >= 1 evaluable cell",
          lambda: not t2_sets_ok({"coco": [True], "xm": [False]}) and t2_sets_ok({"coco": [True, False], "xm": [True]})
          and not t2_sets_ok({}))

    def ranks():
        r = ranks_from_keys(cell, np.random.default_rng(6).random((50, cell["S"])))
        keys = np.random.default_rng(6).random((50, cell["S"]))
        ok = True
        for i in range(cell["N"]):
            a, b = cell["start"][i], cell["start"][i + 1]
            ok &= bool(np.all(np.sort(r[:, a:b], 1) == np.arange(b - a)) and
                       np.all(np.argsort(np.argsort(keys[:, a:b], 1), 1) == r[:, a:b]))
        return ok
    check("ranks_from_keys: per-image ranks are a permutation ordered by key (production null path)", ranks)

    def cap():
        t = {"c": 0.0}

        def clock():
            t["c"] += 10.0
            return t["c"], t["c"]
        bd = Budget(cpu_cap=100.0, wall_cap=1e9, clock=clock)
        ran = []

        def step(n, k):
            def f():
                ran.append(n)
                for _ in range(k):
                    bd.check()
                return {"label": "PASS"}
            return f
        res = run_checks([(n, step(n, 3)) for n in ORDER], bd)
        stop = run_checks([("D1", lambda: {"label": "FAIL", "stop": "fault"}), ("D5", step("x", 0))],
                          Budget(clock=lambda: (0.0, 0.0)))
        return [res[n]["label"] for n in ORDER] == ["PASS", "PASS", "NOT_RUN", "NOT_RUN", "NOT_RUN", "NOT_RUN"] and \
            ran == ["D1", "D5", "D2"] and stop["D5"]["label"] == "NOT_RUN"
    check("cap: the running check and every later check are NOT_RUN; a fault stop propagates", cap)

    def attempt():
        import tempfile

        def boom(exc):
            def f():
                raise exc
            return f
        with tempfile.TemporaryDirectory() as tmp:
            out: list = []
            bd = Budget(clock=lambda: (0.0, 0.0))
            steps = [("D1", lambda: {"label": "PASS"}), ("D5", boom(ValueError("x"))), ("D2", lambda: {"label": "PASS"}),
                     ("D3", lambda: {"label": "PASS"}), ("D4b", lambda: {"label": "PASS"}), ("D4a", lambda: {"label": "PASS"})]
            res = run_attempt(Path(tmp) / "a/STARTED.json", {"t": 1}, lambda: (steps, {"m": 1}), bd, out.append)
            labels = [res[n]["label"] for n in ORDER]
            try:
                run_attempt(Path(tmp) / "a/STARTED.json", {"t": 2}, lambda: (steps, {}), bd, out.append)
                second_refused = False
            except Fault:
                second_refused = True
            r2 = run_attempt(Path(tmp) / "b/STARTED.json", {}, boom(Fault("load")), bd, out.append)
            r3 = run_checks([("D1", boom(Fault("in step"))), ("D5", lambda: {"label": "PASS"})], bd)
        return labels == ["PASS", "FAULT", "NOT_RUN", "NOT_RUN", "NOT_RUN", "NOT_RUN"] and second_refused and \
            len(out) == 2 and out[0]["m"] == 1 and out[0]["checks"]["D1"]["label"] == "PASS" and \
            all(v["label"] == "NOT_RUN" for v in r2.values()) and out[1]["fault_outside_steps"] and \
            r3["D1"]["label"] == "FAULT" and r3["D5"]["label"] == "NOT_RUN"
    check("B1: a raising step is FAULT, later NOT_RUN, earlier kept; result written in finally; a second start is "
          "refused", attempt)
    return {"checks": checks, "pass": all(checks.values()), "n_checks": len(checks)}


def selftest(out: str) -> int:
    assert_pins(list(CODE_PINS))
    L = load_libs()
    r = selftest_core(L)
    rec = {"schema": "vsps.a_dchecks.selftest.v1", "script_sha256": sha_file(Path(__file__)), **r}
    p = Path(out)
    if not p.is_absolute():
        p = ROOT / p
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    bad = [k for k, v in r["checks"].items() if not v]
    print("\n".join(("PASS " if v else "FAIL ") + k for k, v in r["checks"].items()))
    print("selftest ok" if r["pass"] else f"selftest FAILED: {len(bad)}")
    return 0 if r["pass"] else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=("selftest", "dryrun", "freeze", "gate", "run"))
    ap.add_argument("--out", default=f"{OUT}/selftest.json")
    a = ap.parse_args()
    try:
        return {"selftest": lambda: selftest(a.out), "dryrun": dryrun, "freeze": freeze, "gate": gate,
                "run": run}[a.mode]()
    except Fault as e:
        print(str(e), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
