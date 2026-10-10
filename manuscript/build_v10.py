"""Build FAIR v10 from the v9 source (FAIR_28.08.26_v7_EN_IEEE.docx).

Applies the must-fix and should-fix items of REVIEW_PHASES_v10.md and the must-cite
additions of novelty/00_TONG_HOP.md. Text inside [[...]] still needs author
confirmation and is highlighted yellow.

    python3 build_v10.py <v9.docx> <v10.docx>
"""
import copy
import re
import sys

import docx
from docx.enum.text import WD_COLOR_INDEX
from docx.oxml.ns import qn

SRC, DST = sys.argv[1:3]
d = docx.Document(SRC)
P = d.paragraphs
REF_START = next(k for k, p in enumerate(P) if p.text.strip() == "References")
BODY = P[:REF_START]


def _set_runs(p, start, end, new):
    """Replace characters [start, end) of p.text by editing w:t nodes only, so drawings, fields and
    other run content (e.g. anchored figures) survive; new text keeps the first touched run's format."""
    T = qn("w:t")
    pos, first = 0, None
    for t in p._p.iter(T):
        txt = t.text or ""
        a, b = pos, pos + len(txt)
        pos = b
        if b <= start or a >= end:
            continue
        lo, hi = max(start, a) - a, min(end, b) - a
        if first is None:
            first = t
            head, tail = txt[:lo], txt[hi:]
            t.text = head
        else:
            t.text = txt[:lo] + txt[hi:]
        t.set(qn("xml:space"), "preserve")
    assert first is not None
    run_el = first.getparent()
    parts = [x for x in re.split(r"(\[\[.*?\]\])", new) if x] + [tail]
    anchor = run_el
    for k, part in enumerate(parts):
        pending = part.startswith("[[")
        el = copy.deepcopy(run_el)
        for child in list(el):
            if child.tag != qn("w:rPr"):
                el.remove(child)
        anchor.addnext(el)
        run = docx.text.run.Run(el, p)
        run.text = part[2:-2] if pending else part
        if k < len(parts) - 1:
            run.font.highlight_color = WD_COLOR_INDEX.YELLOW if pending else None
        anchor = el


def _wt(p):
    return "".join(t.text or "" for t in p._p.iter(qn("w:t")))


def sub(old, new, paras=BODY):
    hits = [p for p in paras if old in _wt(p)]
    assert len(hits) == 1, (old[:60], len(hits))
    p = hits[0]
    i = _wt(p).index(old)
    _set_runs(p, i, i + len(old), new)


# Shift old [19]-[26] to [24]-[31] first; the new [19]-[23] are cited below and inserted after [18].
for p in BODY:
    for t in p._p.iter(qn("w:t")):
        if t.text:
            t.text = re.sub(r"\[(\d+)\]", lambda m: f"[{int(m.group(1)) + 5}]" if int(m.group(1)) >= 19 else m.group(0), t.text)


# ---------------------------------------------------------------- authors
sub("hoanguyen@bos-semi.com", "nguyenleh760@gmail.com")

# ---------------------------------------------------------------- abstract
sub("verification runs only during data construction, so inference is a single pass.",
    "verification runs only during data construction, so the deployed model captions in a single pass.")

# ---------------------------------------------------------------- contributions (narrowed, novelty check)
sub("(1) a supervision-construction method in which proposition-level verification controls data quality "
    "instead of correcting outputs after generation; (2) a three-state verification design with "
    "neutralization that separates refuted from under-evidenced content and keeps the part still supported "
    "by the image;",
    "(1) a supervision-construction method that builds each SFT target from typed propositions verified "
    "against the image, without gold captions, every span tracing to a proposition and its verdict; (2) a "
    "three-state verification design whose UNCERTAIN state is neutralized to its still-supported part "
    "instead of being discarded;")

# ---------------------------------------------------------------- related work (new refs [19]-[23])
sub("VSPS instead builds SFT targets from verified visual propositions.",
    "VSPS instead builds SFT targets from verified visual propositions. HalluciDoctor [19] and Image "
    "Textualization [20] also clean SFT data offline, but delete content failing a binary check and let an "
    "LLM rewrite the rest.")
sub("VSPS differs in turning verification verdicts into SFT data, with the uncertain state represented and "
    "handled explicitly.",
    "RLAIF-V [21] turns verified claims into preference pairs, and SENTINEL [22] drops objects marked "
    "uncertain from preference training. VSPS composes SFT targets from three-state verdicts and "
    "neutralizes the uncertain state, for gender saying \"person\" when evidence is weak [23], "
    "selectively.")

# ---------------------------------------------------------------- III-A
sub("Phase 1 builds supervision from verified propositions on the training images, without using their "
    "gold captions, and fine-tunes the model; Phase 2 deploys only the fine-tuned model, so generation, "
    "verification, selection, and rendering never run at inference.",
    "Phase 1 runs offline on the training images: it first builds the supervision store D_VSPS from "
    "verified propositions, without using their gold captions (Section III-B), and then fine-tunes "
    "Qwen2.5-VL-7B on it with QLoRA (Section III-C). Phase 2 deploys only the fine-tuned model, so "
    "proposition generation, verification, neutralization, selection, and rendering never run at "
    "inference.")

# ---------------------------------------------------------------- III-B-4 budgets
sub("(B_short = 2, B_detailed = 9, chosen on a grid over the same verdicts, Section IV-E4)",
    "(B_detailed = 9, compared on the same verdicts [[on the KTVIC test split]], Section IV-E4; the short "
    "target takes the first two SUPPORTED propositions of the detailed selection)")

# ---------------------------------------------------------------- III-C
sub("a data-level distillation with no teacher logits or extra loss term.",
    "so the construction pipeline acts as a data-level teacher, with no teacher logits, KL term, or extra "
    "loss term.")

# ---------------------------------------------------------------- IV-A
sub("69 for screening the construction pipeline, and the 558 test images for evaluation; gold training "
    "captions are never used to build VSPS supervision, and no test image is processed in Phase 1.",
    "69 held-out training images only to compare pipeline variants (no SFT or reported metric), and the 558 test images for evaluation; gold "
    "training captions are never used to build VSPS supervision, and no test image contributes to the "
    "supervision data or to fine-tuning.")

# ---------------------------------------------------------------- IV-B
sub("serves as generator G, constrained-LM renderer, and fine-tuned model; Vintern-1B [8] is the verifier V.",
    "serves (frozen) as generator G, colour cross-checker, and constrained-LM renderer, and the same "
    "backbone with a LoRA adapter is the fine-tuned model; Vintern-1B [8] is the verifier V.")
sub("Building the Phase-1 records for 3,700 images took about 30 GPU-hours on one RTX 4090, a one-time cost.",
    "Building the supervision-construction records for 3,700 images took about 88 GPU-hours (median 80 s "
    "per image), run as four parallel shards in about 24 h, a one-time cost.")
sub("using transformers 4.51.3 on one RTX 4090 (24 GB).",
    "using transformers 4.51.3 on one RTX 4090 (24 GB); there is no validation split, and the "
    "final adapter is evaluated.")

# ---------------------------------------------------------------- IV-D
sub("Untrained VSPS runs the full construction pipeline, verifier included, on each test image and outputs "
    "its template rendering without SFT;",
    "Untrained VSPS runs the construction pipeline, verifier included, on each test image at evaluation "
    "time and outputs its template rendering without SFT (hedged, budget 5), never entering D_VSPS;")

# ---------------------------------------------------------------- IV-E4
sub("Settings were measured on the same verdicts:",
    "Settings were compared on the same verdicts[[ and scored on the KTVIC test split, so they are "
    "sensitivity analyses rather than held-out tuning]]:")

# ---------------------------------------------------------------- IV-E7 audit + cost
sub("re-labeled 244 machine-SUPPORTED propositions from the training records (at most three per image)",
    "re-labeled 244 machine-SUPPORTED propositions from the Untrained VSPS run on 83 test images (at "
    "most three per image)")
sub("The rejection rate bounds the precision of the supervision but",
    "The rejection rate indirectly bounds the precision of the supervision but")
sub("The construction pipeline costs about 29 s per image (30 GPU-hours over 3,700 images), fifteen times "
    "more, which is why its behaviour is distilled into a single-pass model: Untrained VSPS reaches similar "
    "factuality (1.51 vs. 1.57 hallucinated objects)",
    "The construction pipeline costs about 80 s of GPU time per image (median; 88 GPU-hours over 3,700 "
    "images), about forty times the detailed-mode latency, which is why its outputs are used offline as "
    "training targets for a single-pass model: Untrained VSPS reaches similar factuality under its own "
    "rendering settings (1.51 vs. 1.57 hallucinated objects)")

# ---------------------------------------------------------------- Fig. 3 caption
sub("(B) Phase-1 verdicts of the verifier and a human judge.",
    "(B) verdicts of the verifier (Untrained VSPS run on a test image) and of a human judge.")

# ---------------------------------------------------------------- conclusion + H2
sub("and qualifying propositions are selected and rendered into data, while the fine-tuned model captions "
    "in a single pass.",
    "and qualifying propositions are selected and rendered into SFT data offline; at deployment only the "
    "fine-tuned model runs, in a single pass.")
sub("share the Qwen language-model family, so their errors may correlate.",
    "share the Qwen language-model family, and the generator itself cross-checks colour propositions, so "
    "their errors may correlate.")

# ---------------------------------------------------------------- references
REFS = P[REF_START + 1:]
NEW = [
    'Q. Yu et al., "HalluciDoctor: Mitigating hallucinatory toxicity in visual instruction data," in Proc. '
    'IEEE/CVF CVPR, 2024.',
    'R. Pi et al., "Image Textualization: An automatic framework for generating rich and detailed image '
    'descriptions," in Proc. NeurIPS Datasets and Benchmarks Track, 2024.',
    'T. Yu et al., "RLAIF-V: Open-source AI feedback leads to super GPT-4V trustworthiness," in Proc. '
    'IEEE/CVF CVPR, 2025.',
    'S. Peng et al., "Mitigating object hallucinations via sentence-level early '
    'intervention," in Proc. IEEE/CVF ICCV, 2025.',
    'K. Burns et al., "Women also snowboard: Overcoming '
    'bias in captioning models," in Proc. ECCV, Springer, 2018.',
]
anchor = REFS[17]._p
for t in NEW:
    el = copy.deepcopy(REFS[17]._p)
    anchor.addnext(el)
    para = docx.text.paragraph.Paragraph(el, REFS[17]._parent)
    for r in para.runs[1:]:
        r._r.getparent().remove(r._r)
    para.runs[0].text = t
    anchor = el
sub("Signal Processing: Image Communication, p. 117430, 2025.",
    "Signal Processing: Image Communication, vol. 140, p. 117430, 2026.", paras=REFS)

# ---------------------------------------------------------------- length: keep 8 pages after the new refs
sub("Every configuration trained from the SFT adapter with 4-bit QLoRA degraded it: at 150 steps (β = 0.03) "
    "short-mode CIDEr fell from 16.3 to 9.7, and at 500 steps (β = 0.05) to 6.5, with hedges per caption "
    "rising from 0.01 to 1.74 and CJK characters in 41.4% of detailed captions (0.7% before); 1,626 steps "
    "(β = 0.10) behaved alike, also on an independent hardware chain. Three mechanisms are measurable: hedge "
    "saturation, since pairs ranking hedged above asserted statements teach the model to insert có vẻ "
    "(\"seems\") unconditionally; multilingual leakage under a weak KL constraint at 4-bit; and phrase "
    "repetition.",
    "Every 4-bit QLoRA configuration degraded the SFT adapter: short-mode CIDEr fell from 16.3 to 9.7 "
    "(150 steps, β = 0.03) and 6.5 (500 steps, β = 0.05), hedges per caption rose from 0.01 to 1.74, and "
    "41.4% of detailed captions contained CJK characters (0.7% before); 1,626 steps (β = 0.10) behaved "
    "alike. The causes are hedge saturation (có vẻ, \"seems\", inserted unconditionally), multilingual "
    "leakage under a weak KL constraint, and phrase repetition.")
sub("Three questions are kept apart: whether annotators agree, whether the verifier agrees with humans, and "
    "whether captions are good. ", "")
sub("Future work follows the same map: heterogeneous multi-verifier consensus with relation-specific ceilings "
    "or region-grounded verification (H1, H2); proposition-level metrics for attributes, relations, and counts "
    "(H3); further languages (H4); coverage recovery through additional proposition rounds (H5), the main open "
    "problem; and wider constrained-LM rendering of the supervision (H6).",
    "Future work: multi-verifier consensus or region-grounded verification (H1, H2), proposition-level "
    "metrics (H3), more languages (H4), coverage recovery (H5), and wider constrained-LM rendering (H6).")
sub("The noise is spread over 3,617 images, and further cleaning barely changes the outcome (1.15 vs. 1.20 "
    "hallucinated objects for VSPS-Base and VSPS-Clean).", "")
sub("Advances in Neural Information Processing Systems, vol. 36, pp. 10088–10115, 2023.",
    "in Proc. NeurIPS, 2023.", paras=REFS)
sub("in Findings of the Association for Computational Linguistics: EMNLP 2024, 2024.",
    "in Findings of EMNLP, 2024.", paras=REFS)
sub("Self-Correction and Instructed zero-shot were not run on COCO for compute reasons. ", "")
sub(" They illustrate, not replace, the quantitative results.", "")
sub("Qualitative KTVIC cases (Vietnamese with English glosses):", "Qualitative KTVIC cases:")
for a, b in [
    ("V.-Q. Nguyen, M. Suganuma, and T. Okatani,", "V.-Q. Nguyen et al.,"),
    ("R. Vedantam, C. L. Zitnick, and D. Parikh,", "R. Vedantam et al.,"),
    ("in Proc. 42nd Int. Conf. Machine Learning (ICML), PMLR, pp. 33815–33832, 2025.", "in Proc. ICML, 2025."),
    ("in Proc. ECCV, Springer, 2022.", "in Proc. ECCV, 2022."),
    ("in Proc. Int. Conf. Computational Collective Intelligence (ICCCI), Springer, 2020.", "in Proc. ICCCI, 2020."),
]:
    sub(a, b, paras=REFS)

d.save(DST)
print("saved", DST)
