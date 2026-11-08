# B-PA1-T1: substantive pre-data amendment of the lineage rule (PREREG_DRAFT_v3_1.md §4.1 N6) for Gemma-3n, DRAFT v1.2

Status: **DRAFT v1.2, not read, not registered.**
- This is a substantive pre-data amendment of a registered family rule. PI-1108e Q1 named it an erratum, and the file
  name keeps that word (CC-295r2 E6).
- Drafted 2026-11-08 (`date -u`) under PI-1108e Q1 ("Có, thêm erratum"; LOG l.1852), CC-295 W6 / Ruling 10a,
  CC-295r2 Rulings 10-14 (E1-E8) and CC-295r3 Ruling 11 (E9: two line citations and the l.160-162 quote corrected; nothing
  else changes).
- It needs a full read at the irreversible tier before the B code commit `H_B`.
- v1 (`ERRATUM_LINEAGE_GEMMA3N_v1.md`, 50841c55) and v1.1 (`ERRATUM_LINEAGE_GEMMA3N_v1_1.md`, eea9d377) are kept
  unchanged and are never committed.

## 1. The rule change (v3.1 §4.1 N6, l.160-162)

**Registered text (l.160-162, e9b30ca7), verbatim:**

> **Lineage resolver (N6):** the model card first, then the model's technical report or paper. `config.json` confirms
> the architecture only, never the weight initialisation. A lineage that neither source determines counts as a
> **clash** with every other model, and the next candidate is taken.

**New text:**
1. **Source order:** the model card first, then the model's technical report or paper, then **the developer's
   official model documentation**. The vendor documentation comes last (E1). It is read only where both the card and
   the report or paper are silent on a lineage, so no lineage that the card or a report already resolves can change.
2. **Inference rule for the third source (E2):** if that documentation presents the vision encoder as a new encoder
   series, and states no initialisation from another series, the encoder is its own V line.
3. **Unchanged:**
   - `config.json` confirms the architecture only;
   - the versions-of-one-series rule;
   - "Distillation teachers outside the series are recorded but do not merge lineages" (l.155-156);
   - every other source rule.

## 2. What it overrides (E4)

**Registered lines on Gemma-3n:**
- v3.1 l.181, the desk table: "MobileNet-V5-300M (J2 desk check in CC-217; confirm by the resolver at pin) / Gemma".
- l.186: the Rule-S assignment on paper uses MobileNet-V5/Gemma.
- l.608, the N6 row: "Gemma-3n MobileNet-V5-300M written in, confirmed at pin".
- l.636, O4: "MobileNet-V5-300M per CC-217 desk check; resolver at pin; undetermined = clash (90)".
- CC-217 N6: "config.json shows the architecture, not the weight initialisation; name the resolver (card or tech
  report). Undetermined lineage counts as a clash".

**What happened at pin:** the card names no vision encoder, and no technical report exists (CC-295 item 7). Under N6 as
registered, O4's contingency "undetermined = clash (90)" would apply.

**The override:** for Gemma-3n-E4B-it **only**, this amendment overrides that O4 contingency. Its lineage is resolved by
the third source under rule 2. For every other model, O4 and N6 apply as registered.

## 3. Effect

**Gemma-3n-E4B-it** (candidate 5, rev c1221e9c62e34a43ab7ffacd1be0ea71f126ef10):
- V = **MobileNet-V5**, its own line, by rule 2: the guide calls it "a new, highly efficient vision encoder" and names
  no initialisation.
- "An advanced foundation of MobileNet-V4 blocks" describes architecture. If MobileNet-V5 counted as the same series as
  MobileNet-V4 under the versions rule, nothing would change, because no other model in the walk is a MobileNet.
- L = Gemma (card `base_model: google/gemma-3n-E4B`; Gemma ≡ Gemma 3n, l.158).

**Other models:** no lineage changes, by construction of rule 1.
- The card or a report resolves every other model of the walk and the verifier: CC-295 Ruling 10c and the registry
  source strings.
- In particular, Gemma-3-4B, Phi-3.5-vision, LLaVA-1.5 and the Qwen2.5-VL verifier take V from a report, and that stays
  so.

**Walk:**
- The five V lines become InternViT, EVA-CLIP, MobileNet-V5, SigLIP and CLIP.
- Expected walk {2, 3, 5, 6} if the gate passes; without this amendment, {2, 3, 6 or 7, one of 8-10} (CC-295r2 Ruling 12).
- One more disjoint family lowers the PA3 risk [est.].

**Shared L with candidate 7:** Gemma-3n shares L = Gemma with candidate 7, Gemma-3-4B-it. If 5 is accepted, 7 clashes on
L ("accepted:gemma3n_e4b"), so 7 can no longer stand in for 6 (MiniCPM-V-4).

**Registry:** this is the one switch in `scripts/b_pa1/b_pa1_registry.json`. `models.gemma3n_e4b.lineage.V` is
"MobileNet-V5". Without this amendment it is `V_without_erratum` = "undetermined", and the walk skips Gemma-3n as
"lineage".

## 4. When the lineage freezes (E5)

- V is fixed at the gatekeeper pin line of this file, which comes before any gate result.
- A MobileNet-V5 or Gemma-3n technical report that appears later, and names an initialisation, is recorded in the audit
  column (the registry source string and the v3.1 §4.2 table). It is never applied: not in tier 1, not in tier 2, not
  in tier 3. The accepted set that tier 1 fixes carries forward unchanged.

## 5. Why it is pre-data

- No gate result, caption, rate or score of any B candidate exists. No Gemma-3n output appears in LOG.md or
  WORKFLOW_LOG.md (CC-295r2 item 11). Block S has not run, and no B rental has happened.
- The registered intent was already MobileNet-V5 (l.181, l.186, l.608, CC-217 N6). What changed after v3.1 concerns
  documentation only: the card is silent and no report exists. This file fills a source gap; it does not react to a
  result.
- The walk order (§4.3) and every other family rule stay as registered. No candidate is added.
- The effect on the walk is disclosed in §3, and it follows from the source rule alone.

## 6. Sources (E3, E7)

**Google Developers Blog, "Introducing Gemma 3n: The developer guide", dated 2025-06-26**
(developers.googleblog.com/en/introducing-gemma-3n-developer-guide/). Retrieved 2026-11-08 (UTC):
- "a new, highly efficient vision encoder, MobileNet-V5-300M".
- "An advanced foundation of MobileNet-V4 blocks".
- The full distillation sentence: "Benefiting from novel architectural designs and advanced distillation techniques,
  MobileNet-V5-300M substantially outperforms the baseline SoViT in Gemma 3 (trained with SigLip, no distillation)".
  - **Reading:** SigLIP is named only for the Gemma 3 baseline (SoViT) that MobileNet-V5 is compared with. It is not
    named as a teacher or an initialisation of MobileNet-V5, and no teacher is named.
  - Even a SigLIP teacher would not merge lineages (l.155-156). So this sentence does not tie Gemma-3n to the SigLIP
    line of candidates 6 and 7.
- "Look out for our upcoming MobileNet-V5 technical report". No such report exists at drafting; a web search on
  2026-11-08 found none (CC-295r2 item 10).

**ai.google.dev/gemma/docs/gemma-3n.** Retrieved 2026-11-08 (UTC); the page shows no date:
- "High-performance MobileNet-V5 encoder". No initialisation is stated.

**Model card, `google/gemma-3n-E4B-it` at c1221e9c:** names no vision encoder.

**`config.json` at c1221e9c:** `vision_config.architecture` = `mobilenetv5_300m_enc`. By N6 this confirms the
architecture only.
