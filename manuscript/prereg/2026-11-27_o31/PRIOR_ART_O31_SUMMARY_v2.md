# Prior-art summary for O31, v2 (searches 2026-11-27; corrected per CC-501 N5; v1 = 312be885)

## Search log
- **Budget:** 25 searches against a cap of 25. The log is `search/QUERIES.tsv`: 16 Semantic Scholar searches through the shared `s2get.sh` queue and 9 OpenAlex searches with the key read at call time.
- **Empty searches:** queries 22 and 23 returned 0 results. They still count toward the cap.
- **Abstract lookups (not searches):** 11 by-id fetches, kept in `search/ids/`. One id, 2604.06165 (HaloProbe), was not found.
- **Contact:** no contact e-mail was sent. The user agent was `vsps-research`.
- **Depth of reading:** every row is read from the abstract only, or from the title only where the TSV says so. No full text was read. Each TAKEN or PARTLY TAKEN call must be re-checked on the full text before the FAIR 2027 draft.

## Verdicts per idea

| Idea | Status | Closest work |
|---|---|---|
| Cut hallucination without "saying less" in detailed captions | **TAKEN** (English, RL; dense labels are model-made with human spot checks in 2609.35294) | Beyond Saying Less 2609.35294; ClaimDiff-RL 2605.20278; BalCapRL 2605.07394; FeedQuill 2503.07906 |
| Fine-tune on verified or filtered model-written captions | **PARTLY TAKEN** | FAIR 2026 (ours); HalluciDoctor 2311.13614; SENTINEL 2507.12455 (detector cross-check, preference pairs); KnowAda 2411.09018 |
| Per-span roles: mask the uncertain, unlearn the refuted (D2) | **PARTLY TAKEN** | EFUF 2402.09801 (unlearning); Mask-DPO 2503.02846 (masking); SCAPO in 2609.35294 (subsentence credit) |
| Count-matched preference pairs (D3) | **PARTLY TAKEN** in its parts | HSA-DPO (AAAI 2025); Mask-DPO; SENTINEL. Deferred to FAIR 2029 under Table 2 |
| Cross-family open-VLM verifier (OR-accept / AND-reject) | **PARTLY TAKEN**; a design detail, not a claim | FeedQuill 2503.07906 (open-VLM ensemble verifier) |
| Operating point as a hallucination–coverage dial | **PARTLY TAKEN** | ClaimDiff-RL 2605.20278 (tunable operating points via RL rewards) |
| (i) the verifier operating point is fixed by a registered pre-SFT gate on supervision coverage, before any SFT; (ii) the supervision → student transfer slopes are measured across operating points under data-level SFT only; (iii) the setting is Vietnamese, no RL, no new labels, one 24 GB GPU, with confirmation on instance gold (CC-501 ruling 1(b)). The single-probe cross-family OR-accept / AND-reject rule is a design detail, not a claim (FeedQuill already ensembles open VLMs). | **NEW** as far as these 25 searches and the CC-501 reading show | Nearest: Beyond Saying Less (same goal and same Qwen2.5-VL-7B base, but on-policy RL with model-made DOPA labels plus human spot checks; no SFT arm, no transfer-slope analysis) |
| Vietnamese captioning with hallucination-aware fine-tuning | **NEW apart from our own FAIR 2026 and MT4** | No third-party work found (LaVy, Vintern and a TALLIP VLM paper do not address hallucination) |

## Implications
- **Full text before the FAIR 2027 draft (N5):** read the full text of the top five: 2609.35294, 2605.20278, 2503.07906, 2402.09801 (EFUF), 2507.12455 (SENTINEL). CC-501 read the first three as abstract + HTML.
- **What the paper can claim.** It cannot claim the trade-off framing or span-level credit. Its claim must be the gate and the transfer mechanism, in a low-resource setting with no new labels.
- **Reading before the FAIR 2027 draft:**
  - 2610.23610 ("Not Every Mention Is a Claim"). It may touch Paper A's territory, so check it against A's boundary.
  - the EMNLP 2026 "Self-Correction Can Amplify Hallucinations" paper, for FAIR 2028.
- **Comparators the proposal asks for:** VCD and Woodpecker. FAIR already ran VCD on KTVIC. EFUF is a natural loss-level comparator for D2 if D2 runs.
