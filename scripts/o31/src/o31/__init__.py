"""O31 (Objective 3.1, RQ8) code: verifier combiner, COCO-80 mentions, store rebuild, K0 gate, metrics, W4 overlap.

Design: manuscript/prereg/2026-11-27_o31/ PREREG_DRAFT_O31_v3.md (3d49435) + ERRATUM_O31_1.md (91108b81, 3319dd7). Never imports or runs e2b_1c.py,
test_e2b_1c.py or e2b_1c_mutants.py (CC-244r2 Ruling 3).

Reused VSPS code is imported from the repo snapshot at $VSPS_REPO, unchanged, after a sha256 check of every
file named in REUSED. A mismatch refuses (the repo is shared with another tool, INC-1027a).
"""
from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # the repo is read-only for this package; -I implies -E, so set it here too

HERE = Path(__file__).resolve().parent
REPO = Path(os.environ.get("VSPS_REPO", "/mnt/d/vsps_image_captioning"))

#: file -> sha256 of every repo file this package imports, reads or replicates; all clean in git at 3319dd7 (and unchanged at 561ac69).
REUSED = {
    "scripts/score_coco_probe.py": "d11db7e192f689980bb2b2bb717d852d9aa339ad857ce9411fe7bdd6fe416070",
    "rescap/chair.py": "e47d249ac7290070f2387d3fa8b22dac77728265ad276f55aa6520f5cbc591a3",
    "rescap/vi/lexicon.py": "fbc945f2247418275144ac75b893f7c51f8951b9ea42018680d433775dd79eb9",
    "scripts/recall_funnel.py": "6313f1b2a73f4de2028f1150aec1b85bbb7c714e32177cf092d89292258b986a",
    "scripts/build_dpo_data.py": "9ef1e8fc82be5e670d2820219292586025ae297a9bfecca035083465ac70d36c",
    "scripts/person_uncap.py": "d16b19f6597f84597db7865dea4058f0bb1fecf914d71d34d6406d66283fa5bb",
    "rescap/pipeline/select.py": "dbab6da9c67b05c2505fa504213df12ee1c503982ef3bfde0634dc3a97372d8e",
    "rescap/pipeline/realize.py": "e9f69f6022e202c6fe273582e3bc1c991f5ba1c2d073099913d3d8b61bade92e",
    "rescap/pipeline/verify.py": "e1ce16829a512a837d727b2d3a411076d9c8a7052ba88e94d3fd7e67aad44b45",
    "rescap/pipeline/generate.py": "5e859821f4f671ce6506aa1c2609710990ede6b88e085ba37c85cbe6303b2ebd",
    "scripts/c_stage1/build_memory.py": "e771b92df9096e286e8d5de207d3adafe49c8e5e59eab276978b0236cc0eeab9",
    "scripts/match_openviic.py": "c0d9dd30e3222ab6542a7e1acfbb9bd3899e4b6db5c896b0adc4d805c1005a8b",
    "scripts/w25/w25.py": "d6d127807929c0534e6140d77831b682e3a7202484fa074d56229e0d091316c0",
    "scripts/c_en/cen_fetch.py": "e51918e958ad86e832dd34fbf5ed86d2f7fc13cf41b602dfe537afa43af4c673",
    "scripts/grl/common.py": "bbe7ee61f659b1a7bfc3cab418d83ed779b76187107708fef2d8ab44df0ad23a",
    "scripts/train_stage2.py": "29312ef765e3e49e5e1efefc5ad8b88fcf33c991b1a5f3a266a910ada3d1cab4",
    "data/coco_probe/chair_synonyms.txt": "b685537b36fe21b791c87151b96a991ceb582edff19f3da204dcc7a7905502f2",
    "data/coco_probe/coco80_vi.json": "926e08571ef6e80a7f8aae8f2b73753d6c5c54c431a750ba2b67bfaae71b540b",
    # W2 (CC-504): the rest of the runtime import closure (full test suite + run_k0 through the real builder)
    "rescap/__init__.py": "b712bea4d66e5e2e0f0cec1624ab244a025560ecc5d86f96cada2e0160a4890f",
    "rescap/metrics.py": "e0296ec528b87f4d1b31165cbb45deee5453783fd7dad783f248869e596bf960",
    "rescap/repro.py": "723200190818cd61a56527e6a0a1596b95f9d1ed1ebc0cabe1b29135cf03b70d",
    "rescap/vocab.py": "c9143b2d973fc48a2231335844cd91ab702329c0b1aabb802884225e155967ec",
    "rescap/svp/__init__.py": "5b7f52920de75cf59bde0ae657e292a876efc63292ca6db6a4d085bb9fec1424",
    "rescap/svp/entailment.py": "4462f44df80faa0adc620d98aa5d8bbb307243d450e9aee4801bb17a3a06db23",
    "rescap/svp/matching.py": "a9253060131aacfca8eaab9a4b2c473c487db96a7c1222f0b8e31f9f61b24003",
    "rescap/vi/__init__.py": "f898963e95fec7d9fb236295649404815634a1d949bfd74cd7c3b90ed493bf6c",
    "rescap/vi/classifier.py": "966cdab1fed8471ac57d225698e63f1e2a055435a5d669e9cca10eed703fed16",
    "rescap/vi/color.py": "242fc46f68ecb06c8eefde23350481d99e60566b3da64ab90cfa79db38fd3875",
    "rescap/vlm/__init__.py": "13de9854599acedd32ea1798ea1acc475703fcd3aa4eb4dd715dc8eadcd632cd",
    "rescap/vlm/base.py": "e8fee5bc5b729534af67c6e462a27f0d83ba611f18ff8e3f2717b11eb393ae93",
    "rescap/vlm/mock.py": "33793de01b4f2790964342b1af2d4c2de18d793ae4693608283992475ed62ce7",
    "rescap/vlm/registry.py": "6c261406bde3d34a73f77ce961aff7d241e2a440ba75e154fccf3ae8d4a70297",
    "scripts/c_stage1/decode_icl.py": "fa5a251160d4fd4fb0cd130af33614283863a84e6ed7905f3da81bb6255010db",
    "scripts/g2b/decode_qwen3vl.py": "8a855ef483c933621776099b6f9de3b60c4fbfaaf706bb40c74e7d84d9dfb5e5",
    "scripts/lb/decode_hf_vlm.py": "e2de18811e2ffeb61ed72cb2399d41123e9a8f6ccd73a5ec35f778dcbe2f5ac4",
    "scripts/vsps_j_m0/m0.py": "5d3c02f414bd5743d437ec399e07431b4d38d970b16b901c52a9a657505ef7b2",  # E3 string; G1 m0.probe
    # G1/G2 probe runner and student decoder (host paths)
    "rescap/vlm/vintern.py": "dbde92aae0d73275c347e76ce045285c9ad5862e64d84564eb73a223b8cf1096",
    "rescap/vlm/qwen_vl.py": "0990c54a930337a6f4e7ac38a9cc2d32259f60caf868417776b18ad3ed3930a7",
    "scripts/evaluate.py": "a68d56826d90d8a409493cd6f49007e906c6cb4f5668314edb9b8e7a632e8236",  # read: settings
    "manuscript/prereg/2026-10-19_b_n1_vi_leaderboard.json": "9ff02dc259258de1add426abd02131f2122e3476a81f9a076066ed6d74906134",
    "manuscript/prereg/2026-10-31_vsps_j_m0/dev_touched_ids.txt": "91db7e2fbb3d479f79ed19fca4aa100399730910cd7511f832576350f26f9b63",
    "manuscript/prereg/2026-10-31_vsps_j_m0/fetch_images.txt": "7f148c8e515bf567f811da84a1e327a6e05d20a85e2939f5088fa1a45a359a3c",
    "manuscript/prereg/2026-10-31_vsps_j_m0/karpathy_test_val_ids.txt": "88e40e3cd2ae6dd3bf3c1f514a085cb61a36b503abde298d57a1bb2bc8acd7fb",
    "manuscript/prereg/2026-10-21_dev_pools/exclusion.json": "c52a96d18925b974878ae1a970c3f9133fb3482216676fd41871eeabb68cc77f",
    # g12c (CC-519 W2, W3): G1 stage-1 wrapper and the §3.5 launcher
    "scripts/generate_stage1.py": "ad965ceb077106e03e2c49026d122e7a5aed76b0e76b1443f18636e7174637b2",
    "configs/main.env": "2ea67f5fe8fa13d98e4c65b5d5d4cf5892ac779222ba40195c8e9cb03440aeca",  # read: FAIR stage-1 flags
    "scripts/grl/id_counts.py": "0c590058a908c0683366e385b70c68ca77b4ff80902b7a1398f216ce6e55d859",  # m0.kv4224 (laptop)
    "data/lb/sets/ktvic_test.tsv": "456243c0cfc82b0c3cc4ad52c694e11b4d9702f3ca14cd8103c3a82cd74a90eb",
    "data/lb/sets/uitviic_test.tsv": "dbadc28724d7a07b599325cd996084934d76e6c4c6a885e64e8de333d6a6665b",
    "manuscript/prereg/2026-10-27_c_en/cen_coco_test.tsv": "67555b281d87b01a0f742214da552be0f7c4f4977f543db98a9acd2901787eb1",
    "data/screening/val_manifest.json": "79f3628c156c955698afb66393f4a3e2496c82c78427d603d19887fde6e18790",  # F3
}
COCO80_VI = REPO / "data/coco_probe/coco80_vi.json"  # the tracked repo file, read through its sha pin
COCO80_VI_SHA = REUSED["data/coco_probe/coco80_vi.json"]
FORBIDDEN = ("e2b_1c", "test_e2b_1c", "e2b_1c_mutants")


def sha_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def repo() -> Path:
    """Check every REUSED file's sha256, then put the repo's import roots on sys.path (once)."""
    if getattr(repo, "_done", False):
        return REPO
    bad = [f for f, s in REUSED.items() if not (REPO / f).is_file() or sha_file(REPO / f) != s]
    if bad:
        raise SystemExit(f"FAULT reused repo files missing or changed under {REPO}: {bad}")
    roots = [REPO, REPO / "scripts", REPO / "scripts/c_stage1", REPO / "scripts/w25", REPO / "scripts/vsps_j_m0",
             REPO / "scripts/lb"]
    sys.path[:0] = [str(r) for r in roots if str(r) not in sys.path]
    repo._done = True
    return REPO


def no_forbidden() -> None:
    """CC-244r2 Ruling 3: refuse if the parked E2b code was ever imported in this process."""
    hit = [m for m in sys.modules if m.rsplit(".", 1)[-1] in FORBIDDEN]
    if hit:
        raise SystemExit(f"FAULT forbidden module imported: {hit}")
