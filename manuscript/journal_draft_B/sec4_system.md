# 4 The measuring instrument and its protocol card

<!-- Draft 2026-10-15; rebuilt 2026-10-20 under PD-24 (a): the ladder design (old 4.3), the second backbone (old 4.4), the freeze/M3 paragraph (old sec4:79) and the deviations table (old 4.6) moved to supplementary_B.md (S2, S3, S8). Training recipe shared with the FAIR 2026 conference version (cited, not re-claimed). -->

## 4.1 Systems

The audit needs a system whose differences from other systems are known. All systems share one backbone, Qwen2.5-VL-7B-Instruct (Bai, Chen, et al., 2025), and one fine-tuning recipe, the QLoRA recipe of the FAIR conference version (4-bit NF4, LoRA rank 16, α 32, learning rate 10⁻⁴, effective batch 8, two epochs, 512 visual tokens)<!-- src: literature: FAIR 2026 §IV-B (recipe as published) -->. Two prompts are used, a *short* prompt (one sentence) and a *detailed* prompt. Decoding is greedy unless stated. Systems differ only in their training targets, their loss mask or, in Sections 5.4–5.5, their training-set size. The main text uses four systems and two adapter families (Table 4.1).

**Table 4.1.** The systems of the main text: training targets per training image and the tokens that enter the training loss.

| System | Training targets per training image | Loss |
|-----|--------------|-------|
| Zero-shot | none | — |
| P1 | the first reference in file order, short prompt | prompt and response (legacy mask) |
| **P1-R (response-only P1; main system)** | as P1 | response tokens only |
| fuse2 | P1's short row, plus one detailed-prompt row joining the consensual reference and the reference that adds the most new objects, each closed with a period | legacy |
| Training-set-size adapters (Section 5.4; three seeds × five sizes) | as P1-R (the first KTVIC reference), on nested subsets of the 3,469 training images outside dev300 | response tokens only |
| Reverse-direction adapters (Section 5.5; two seeds × three sizes) | one UIT-OpenViIC caption of the same image (the first in a fixed order; k = 1, as in the forward direction), on nested subsets of 2,262 eligible KTVIC training images | response tokens only |
<!-- BD item 13 (R1 M8): adapter rows added; src manuscript/prereg/2026-10-28_b1_scaling/PREREG.md l.58 (--loss-mask assistant, build_gold_sft default --select first) ; manuscript/prereg/2026-10-29_b_r1/RULE.md §2.1-2.4, §2 item 4 (k = 1, first element of the O pool), l.55 (--loss-mask assistant) -->

**Which P1.** "P1-R" always means the response-only system, and "P1" alone always means the legacy-mask system; we give the seed each time. P1-R (seed 42) is the system of the punctuation audit (Section 3.3), the v3 sensitivity (Section 3.5) and Section 5.1. P1 (legacy mask) is the system of the segmentation audit (Section 3.4, seed 42), the XM3600 period shift and the UIT-ViIC analyses (Sections 3.3, 3.5 and 5.2, seed 43), Table 5.1's P1 row (three seeds) and the second panel (Section 5.3, seed 42).<!-- R2 N-M6: source keys p1assist_* = P1-R; p1-gold / p1_s43 / p1_s44 / transfer_p1_s43 = legacy P1 (manifest keys of sec3:30-56, sec5:13, 29, 43). -->

The systems used only by the supplementary tests are listed in Supplementary S1. Our protocol findings come from systems trained on all 3,769 KTVIC training images (P1 seed 42: count not recorded, see Supplement S1). Only the supplement's dev-gated levers, the final test (Supplement S7) and the training-set-size studies of Sections 5.4–5.5 (nested subsets of the 3,469 images outside dev300) used the 300-image carve, which existed before them, was drawn with a fixed seed, and is disclosed here (Section 3.1; Supplementary Table S1.1 gives every system's count).<!-- src: CC-109 W6 (the ruling's sentence; "B's" rendered as "Our" for the paper) ; CC-109 W1 --> QLoRA (Dettmers et al., 2023) and LoRA (Hu et al., 2021) are as in the FAIR version.<!-- CC-145 pass-3: restored verbatim (CC-109 W6 sentence). -->

P1-R is the system we report as our KTVIC baseline. It is P1 with the loss restricted to the response tokens: under the legacy mask the instruction text and the assistant header stay in the loss. The fusion targets are built from human references only. Every object in a fused target was written by an annotator, and the greedy step stops when no reference adds a new object.

The P1 short target uses slot 0 of the single-writer sequence. Slot 0 is the first caption typed and names fewer objects than later slots, so P1-family counts are lower than those of systems trained on consensual or fused targets. We disclose this whenever the two are compared.

## 4.2 Protocol card

Every KTVIC score in this paper uses the following protocol (Table 4.2) unless a section says otherwise.

**Table 4.2.** The protocol card: the scoring settings behind every KTVIC score in this paper unless a section says otherwise.

| Item | Setting |
|----|--------------------|
| Test set | KTVIC official test, 558 images, 5 references each |
| Segmenter | RDRSegmenter, VnCoreNLP 1.2 (jar SHA-256 9e2811cdbc2ddfc71d04be5dc36e185c88dcd1ad4d5d69e4ff2e1369dccf7793)<!-- src: data/results/b_n2/b_n2_run.json :: env.VnCoreNLP-1.2.jar --> ; the same segmenter on candidates and references |
| n-gram metrics | pycocoevalcap: BLEU-4, ROUGE-L, CIDEr-D, all ×100 |
| Punctuation | none removed or added (protocol P0): RDRSegmenter replaces the PTB tokenizer, so punctuation is scored as written on candidates and references. Section 3.3 also reports the stripped and appended variants and, post hoc, PTB-style removal |
| Decoding | greedy, one caption per image per prompt |
| Object matcher | v2 (tone-normalised); v1 and v3 as sensitivity |
| Object P / R / F1 | precision micro-averaged over mentions; recall macro-averaged over images with non-empty gold; F1 their harmonic mean; gold = union of the image's references |
| Uncertainty | paired percentile bootstrap over images; when seeds are pooled, slopes carry seed fixed effects and only images are resampled, so the intervals are conditional on the trained adapters and do not include seed-to-seed variance |
| Two-panel development scoring (Sections 5.4–5.5 only) | the 187 dev300 images with an OpenViIC training-split copy; k = min(5, available) references per panel and image (mean 4.42); CIDEr-D document frequencies computed per panel over the 187 images; trailing punctuation stripped from candidates; CIDEr-D without the length penalty (σ = ∞) reported beside each gap, and co-primary in the reverse-direction rule |<!-- BD items 3, 9 (R1 M7, R3 M6/m4, R4 m7): src scripts/b_d0/d0.py l.203-205 as read 2026-10-29 (current file sha256 0d87a953; the decided run's script hash in d0_decide provenance is 89f102c2, so the lines were read in a later revision of the script) (strip_trailing_punct_tokens; one E4.Cider per panel over the 187 ids) ; d0_decide.json 15dd925f :: descriptive.panel.mean_k ; bootstrap.* ; manuscript/prereg/2026-10-29_b_r1/RULE.md §5 l.123-128, l.200 (sigma = inf co-primary for GO_BOTH) -->
| Seeds | 42, 43, 44 |

With per-panel document frequencies, each panel's IDF weights rest on the 187 images' captions only and are noisy; the log-scale gap of Section 5.4 corrects for the panels' different score levels but not for their different IDF weights. A fill-in copy of this card ships with the kit (Section 3.7). Scoring runs as a separate process from generation. The scorer version and the SHA-256 value of every committed result file are listed in the number manifest; the predictions themselves are not released (Section 3.7).

## 4.3 Reproducibility gates

**Software and hardware.** Training and inference fit on a single 24 GB NVIDIA RTX 3090; decoding is greedy. Supplementary S15 gives the pinned software versions and the run history.<!-- src: as Supplementary S15 (GPU field: .session_backup/machines/O-2308423/root/outputs/t3_2_s1_seed_consensus/check.json :: gpu ; .session_backup/machines/M3/root/outputs/b_f1_ktvic_test/check.json :: card). CC-145 J6 (2026-10-28): paragraph moved verbatim to Supplementary S15. -->

Two checks guard the main number. Both cover scoring only: they show that the committed predictions are scored deterministically, not that training or decoding reproduces.

**Second machine.** A second machine checked out the repository at a fixed commit, rescored the committed P1-R seed-42 predictions, and reproduced the committed result file byte for byte. Its CIDEr-D, 148.66, equals the committed value<!-- src: .session_backup/2026-10-14/r12_verify/g1_repro_gate_machine2.json :: metric_comparisons.CIDEr.rescored_value -->.

**Live segmenter.** All three P1-R seeds were rescored with a live VnCoreNLP 1.2 run. CIDEr-D, BLEU-4 and ROUGE-L match the committed files on every seed. Eight of the nine differences are exactly zero, and the ninth (CIDEr-D, seed 44) is 2.8 × 10⁻¹⁴, one unit in the last place of the stored float. The gate's verdict is PASS<!-- src: .session_backup/2026-10-15/paperA_keys/cider_3seed_g1_rescore_check.json :: per_seed|p1assist_s4{2,3,4}-short|{CIDEr,BLEU4,ROUGEL}_abs_diff (p1assist_s44-short.CIDEr_abs_diff = 2.842170943040401e-14; all others 0.0) ; verdict -->.
