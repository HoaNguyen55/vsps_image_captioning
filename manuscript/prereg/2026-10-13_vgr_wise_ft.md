# Pre-registration: VGR Step 0 (WiSE-FT on `fuse2_s42`) and Vocabulary-Gap Rehearsal gate (judge D10 (iii) + user U-001)

Status: frozen 2026-10-14 before any output of `59_wise_ft_s42.sh` or any VGR SFT run exists. Written on branch
`paper-v10` at `ba351f8`. The gatekeeper commits this file and
`manuscript/prereg/2026-10-13_vgr_wise_ft_jobs/59_wise_ft_s42.sh` before `59_wise_ft_s42.sh` is queued.

Authority:
- Judge decision **D10 (iii)**: VGR ranked #2 on the COCO arm at 78% confidence ("YES, staged: WiSE-FT baseline first,
  futility rule").
- User decision **U-001** (2026-10-13, resolving D10's <80% item): run Step 0 (WiSE-FT weight-space interpolation on
  `fuse2_s42` at $\alpha \in \{0.5, 0.75\}$ on UIT-ViIC val + KTVIC test) first, and gate VGR SFT on the pre-registered
  futility rule.

Source of the mechanism, vocabulary-gap analysis, and kill rules K1-K4: `manuscript/research_r9/C6_multitask_data/REPORT.txt`
sections 1.3, 3(e1), and 4 (P-C6-1).

## 1. Mechanism and zero-edit implementation (frozen)

Fine-tuning `Qwen/Qwen2.5-VL-7B-Instruct` on KTVIC (`fuse2_s42`) raises recall on the 7 COCO classes that KTVIC names
$\ge 200$ times (`51.2% -> 57.7%` in short mode), while eroding recall on the 73 classes KTVIC names $< 200$ times
(`32.9% -> 26.3%` on $<20$, `31.0% -> 24.3%` on `20-199`; C6 section 1.3, `p7.log`). Restoring the base VLM's naming on
those 73 classes without changing frequent-class behavior gives a vocabulary-restoration hybrid bound of
`+5.45 [+4.48, +6.39]` F1 on the 2,500-image COCO probe (`59.4 -> 64.9`; C6 `p8.log`).

Before spending ~9 GPU-h on Vocabulary-Gap Rehearsal (VGR) SFT, Step 0 tests whether simple weight-space interpolation
between the base VLM $W_0$ and the fine-tuned adapter $W_{\text{fuse2}}$ (WiSE-FT; Wortsman et al., CVPR 2022) already
recovers most of this bound.

Because `fuse2_s42` is a LoRA adapter with `r = 16`, `lora_alpha = 32`, `bias = "none"`, and `modules_to_save = null`:

$$W(\alpha) = (1 - \alpha) W_0 + \alpha \left(W_0 + \frac{\text{lora\_alpha}_0}{r} B A\right) = W_0 + \frac{\alpha \cdot \text{lora\_alpha}_0}{r} B A$$

Weight-space interpolation at $\alpha \in \{0.5, 0.75\}$ is therefore **mathematically identical** to keeping the exact
`fuse2_s42/adapter_model.safetensors` weights (`4dd674ab...`) and setting `lora_alpha` in `adapter_config.json` to:
- `lora_alpha = 16` for $\alpha = 0.5$ (`fuse2_s42_wise05`);
- `lora_alpha = 24` for $\alpha = 0.75$ (`fuse2_s42_wise075`).

This requires **zero edits** to frozen `scripts/evaluate.py` (`a68d5682...`).

## 2. Instrument (frozen)

| file | sha256 | role |
|---|---|---|
| scripts/evaluate.py | a68d56826d90d8a409493cd6f49007e906c6cb4f5668314edb9b8e7a632e8236 | caption generation and n-gram / CHAIR evaluation |
| scripts/object_prf.py | 6b711280d70b780d596414896d832738da58f1b079015dee888605d1ba350adc | object P/R/F1 and paired bootstrap (`B=5000`, seed 0) |
| scripts/score_coco_probe.py | f8cc96bce34388f28388f7b1e873fbdfbe662503c4a56b9bdcaca5df1ff9290f | COCO-80 Vietnamese matcher v2 (frozen `ba351f8` blob; Phase 2 tone-norm rescoring also reported per D11(ii)) |
| rescap/chair.py | fd1d012398cae5d1984bb4effdf18919e157f1c770b8a13adbb070a8b659ec6b | KTVIC 113-class matcher (frozen `ba351f8` blob; Phase 2 tone-norm rescoring also reported per D11(ii)) |
| data/coco_probe/coco80_vi.json | 926e08571ef6e80a7f8aae8f2b73753d6c5c54c431a750ba2b67bfaae71b540b | Vietnamese COCO-80 lexicon |
| data/uitviic/instance_gold.json | 278d15b97e3eeb9496a0282bb91deb365117becf24d174fbb1e0507203b12ea4 | human COCO-2014 instance classes for UIT-ViIC splits |
| data/results/fuse2_s42-short.json | 70b007f9992a337d33fe10c3710f2ad2c773f564743d69a6ca8874a2e30739cb | KTVIC test baseline ($\alpha=1.0$, short CIDEr-D 143.9) |
| data/results/fuse2_s42-detailed.json | d2e5c6451527589b127615daccd7e08119423dea2a7d61a9f2f320d2cd0a200c | KTVIC test baseline ($\alpha=1.0$, detailed) |
| runs/fuse2_s42/adapter_model.safetensors | 4dd674ab85ca2bb957594460cde28916ce6c643bf3e08a8e6d7489ccd643d857 | frozen `fuse2_s42` adapter weights |
| runs/fuse2_s42/adapter_config.json | 93f042284aea64fcdf831590c592a7459849632dcb3ee4448b379177b7a298c5 | frozen `fuse2_s42` adapter config (`r=16, lora_alpha=32`) |
| 2026-10-13_vgr_wise_ft_jobs/59_wise_ft_s42.sh | bb4b1d6d064384c23a2ad25819e50352608de4fceb8573327de7777af6c0a32e | Step-0 execution and futility gate script |

## 3. Step-0 protocol, $\alpha^*$ selection, and VGR futility gate (frozen)

1. **Dev split**: `UIT-ViIC val` (`val_data.json`, 924 COCO-2014 images; 66% of its instance pairs are in the 73 classes
   KTVIC names $< 200$ times).
2. **Evaluated systems on UIT-ViIC val (short mode)**:
   - `fuse2_s42` ($\alpha = 1.0$, baseline);
   - `fuse2_s42_wise075` ($\alpha = 0.75$);
   - `fuse2_s42_wise05` ($\alpha = 0.5$).
3. **Evaluated systems on KTVIC test (558 images, short and detailed modes)**:
   - `fuse2_s42_wise075` ($\alpha = 0.75$) and `fuse2_s42_wise05` ($\alpha = 0.5$), compared against existing `fuse2_s42`
     ($\alpha = 1.0$, short CIDEr-D 143.9).
4. **Dev choice of $\alpha^* \in \{0.5, 0.75\}$**:
   - Among candidates satisfying the KTVIC test short CIDEr-D guard ($\ge 140.7$, i.e. within $-3.0$ of the 3-seed
     `fuse2` mean 143.7; or all candidates if neither passes), pick $\alpha^*$ with the higher short-mode COCO-80
     instance-only F1 on `UIT-ViIC val` (ties broken toward $\alpha = 0.75$).
5. **Futility gate for VGR SFT (`D10 (iii)`)**:
   - **Skip VGR's SFT** (`futile_for_vgr_sft = True`) if the dev-chosen $\alpha^*$ already gains $\ge +3.5$ short
     instance F1 over `fuse2_s42` on `UIT-ViIC val` (under either instance-only or instance+reference gold) while keeping
     KTVIC test short CIDEr-D $\ge 140.7$, because the $+5.45$ vocabulary-restoration bound then leaves $< +2.0$ F1
     headroom for rehearsal SFT.
   - Otherwise (`futile_for_vgr_sft = False`), VGR SFT (`seed 42`) is eligible for the P3 slot under K1-K4 below (unless
     `35_e` passes before VGR starts and the coordinator resubmits P-B for the single COCO training slot per D10 (iii)).

## 4. Pre-registered VGR SFT specification and kill criteria K1-K4 (if Step 0 is not futile)

If `futile_for_vgr_sft == False` and VGR SFT runs:
- **Training mix**: `gold_fuse2/sft.jsonl` (7,538 KTVIC rows: 3,769 short + 3,769 fused-2 detailed, legacy loss mask to
  match `fuse2_s42`) plus 2,000 rehearsal tag rows from the leak-free COCO-2014 Karpathy `train+restval` pool (112,132
  images, strictly excluding all Karpathy `test` and `val` images and all UIT-ViIC `val` and `test` images; C6 `p9`).
- **Rarity threshold and sampling**: the 73 COCO-80 classes with $< 200$ mentions in KTVIC train (`out/pool.json`),
  sampled deterministically (seed 42) so every rare class appears in $\ge 25$ rehearsal images.
- **Rehearsal prompt (training only)**: `"Liệt kê các đồ vật, con vật và người có trong ảnh."`
- **Rehearsal target**: the image's human COCO-2014 instance classes ordered by total instance bounding-box area, named
  using the `coco80_vi.json` synonym most frequent in KTVIC train (else first synonym). No model-generated text.
- **Kill criteria (any one kills VGR)**:
  - **K1**: On `UIT-ViIC val` (924 images), short-mode instance-F1 gain over `fuse2_s42` is $< +2.0$ or its 95% paired
    bootstrap CI (`B=5000`, seed 0) includes $0$.
  - **K2**: Short-mode instance F1 on `UIT-ViIC val` is not above the dev-chosen WiSE-FT point $\alpha^*$ at no lower
    KTVIC test short CIDEr-D.
  - **K3**: KTVIC test short CIDEr-D $< 140.7$, or KTVIC test object F1 drops vs `fuse2_s42` with a 95% paired bootstrap
    CI excluding $0$.
  - **K4 (list leakage)**: $> 1\%$ of caption outputs on `UIT-ViIC val` or `KTVIC test` contain $\ge 4$ comma-separated
    class names or the rehearsal prompt wording.
