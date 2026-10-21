# 4 The measuring instrument and its protocol card

<!-- Draft 2026-10-15; rebuilt 2026-10-20 under PD-24 (a): the ladder design (old 4.3), the second backbone (old 4.4), the freeze/M3 paragraph (old sec4:79) and the deviations table (old 4.6) moved to supplementary_B.md (S2, S3, S8). Training recipe shared with the FAIR 2026 conference version (cited, not re-claimed). -->

## 4.1 Systems

The audit needs a system whose differences from other systems are known. All systems share one backbone, Qwen2.5-VL-7B-Instruct (Bai et al., 2025a), and one fine-tuning recipe, the QLoRA recipe of the FAIR conference version (4-bit NF4, LoRA rank 16, α 32, learning rate 10⁻⁴, effective batch 8, two epochs, 512 visual tokens)<!-- src: literature: FAIR 2026 §IV-B (recipe as published) -->. Two prompts are used, a *short* prompt (one sentence) and a *detailed* prompt. Decoding is greedy unless stated. Systems differ only in their training targets or loss mask. The main text uses four:

| System | Training targets per training image | Loss |
|---|---|---|
| Zero-shot | none | — |
| P1 | the first reference in file order, short prompt | prompt and response (legacy mask) |
| **P1-R (response-only P1; main system)** | as P1 | response tokens only |
| fuse2 | P1's short row, plus one detailed-prompt row joining the consensual reference and the reference that adds the most new objects, each closed with a period | legacy |

**Which P1.** "P1-R" always means the response-only system, and "P1" alone always means the legacy-mask system; we give the seed each time. P1-R (seed 42) is the system of the punctuation audit (Section 3.3), the v3 sensitivity (Section 3.5) and Section 5.1. P1 (legacy mask) is the system of the segmentation audit (Section 3.4, seed 42), the XM3600 period shift and the UIT-ViIC analyses (Sections 3.3, 3.5 and 5.2, seed 43), Table 5.1's P1 row (three seeds) and the second panel (Section 5.3, seed 42).<!-- R2 N-M6: source keys p1assist_* = P1-R; p1-gold / p1_s43 / p1_s44 / transfer_p1_s43 = legacy P1 (manifest keys of sec3:30-56, sec5:13, 29, 43). -->

The systems used only by the supplementary tests are listed in Supplementary S1. QLoRA (Dettmers et al., 2023) and LoRA (Hu et al., 2021) are as in the FAIR version.

P1-R is the system we report as our KTVIC baseline. It is P1 with the loss restricted to the response tokens: under the legacy mask the instruction text and the assistant header stay in the loss. The fusion targets are built from human references only. Every object in a fused target was written by an annotator, and the greedy step stops when no reference adds a new object.

The P1 short target uses slot 0 of the single-writer sequence. Slot 0 is the first caption typed and names fewer objects than later slots, so P1-family counts are lower than those of systems trained on consensual or fused targets. We disclose this whenever the two are compared.

## 4.2 Protocol card

Every KTVIC score in this paper uses the following protocol unless a section says otherwise.

| Item | Setting |
|---|---|
| Test set | KTVIC official test, 558 images, 5 references each |
| Segmenter | RDRSegmenter, VnCoreNLP 1.2 (jar SHA-256 9e2811cdbc2ddfc71d04be5dc36e185c88dcd1ad4d5d69e4ff2e1369dccf7793)<!-- src: data/results/b_n2/b_n2_run.json :: env.VnCoreNLP-1.2.jar --> ; the same segmenter on candidates and references |
| n-gram metrics | pycocoevalcap: BLEU-4, ROUGE-L, CIDEr-D, all ×100 |
| Punctuation | none removed or added; candidates and references scored as written (Section 3.3 reports the stripped variant) |
| Decoding | greedy, one caption per image per prompt |
| Object matcher | v2 (tone-normalised); v1 and v3 as sensitivity |
| Object P / R / F1 | precision micro-averaged over mentions; recall macro-averaged over images with non-empty gold; F1 their harmonic mean; gold = union of the image's references |
| Uncertainty | paired bootstrap over images; image-clustered when seeds are pooled |
| Seeds | 42, 43, 44 |

A fill-in copy of this card ships with the kit (Section 3.7). Scoring runs as a separate process from generation. The scorer version and the SHA-256 value of every committed result file are listed in the number manifest; the predictions themselves are not released (Section 3.7).

## 4.3 Reproducibility gates

**Software and hardware.** Training and decoding used transformers 4.51.3 and trl 0.19.1, both pinned because newer releases change how the adapters load, with PyTorch built for CUDA 12.1 and with peft and bitsandbytes for 4-bit loading; the kit's `requirements.txt` lists them. Scoring used Python 3.12.3 with pycocoevalcap 1.2 and py_vncorenlp 0.1.4<!-- src: code/requirements.txt (archived) :: transformers==4.51.3 ; trl==0.19.1 ; data/results/b_n2/b_n2_run.json :: env.python ; env.pycocoevalcap ; env.py_vncorenlp -->. One QLoRA training run of P1 or fuse2 takes about 2 GPU-hours on one 24 GB GPU of the RTX 4090 class, and inference fits on the same GPU<!-- src: README.md (repository) :: "0. Hardware requirements" ; "Phase 1b — QLoRA-SFT (4-bit NF4 base, ~2 h per run on an RTX 4090)" -->. Decoding is greedy, so it needs no sampling seed; the sampled pools of the supplement record their seeds. Some runs were made on rented GPUs, and runs 56–58 had to be rerun after a machine failure; the reruns were not compared with the lost originals (Supplementary S2.1). We give no total compute figure.<!-- R2 R3-M1 (OPEN -> fixed with the pins; total GPU-h disclosed as not given). -->

Two checks guard the main number. Both cover scoring only: they show that the committed predictions are scored deterministically, not that training or decoding reproduces.

**Second machine.** A second machine checked out the repository at a fixed commit, rescored the committed P1-R seed-42 predictions, and reproduced the committed result file byte for byte. Its CIDEr-D, 148.66, equals the committed value<!-- src: .session_backup/2026-10-14/r12_verify/g1_repro_gate_machine2.json :: metric_comparisons.CIDEr.rescored_value -->.

**Live segmenter.** All three P1-R seeds were rescored with a live VnCoreNLP 1.2 run. CIDEr-D, BLEU-4 and ROUGE-L match the committed files on every seed. Eight of the nine differences are exactly zero, and the ninth (CIDEr-D, seed 44) is 2.8 × 10⁻¹⁴, one unit in the last place of the stored float. The gate's verdict is PASS<!-- src: .session_backup/2026-10-15/paperA_keys/cider_3seed_g1_rescore_check.json :: per_seed|p1assist_s4{2,3,4}-short|{CIDEr,BLEU4,ROUGEL}_abs_diff (p1assist_s44-short.CIDEr_abs_diff = 2.842170943040401e-14; all others 0.0) ; verdict -->.
