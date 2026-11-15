#!/usr/bin/env bash
# Run the number, citation and forbidden-string checks on every part. Exit 0 only when all pass.
cd /mnt/d/vsps_image_captioning || exit 2
R=manuscript/bao_cao_khoa_hoc_2026-11-14; K="python3 -I $R/checks/check_part.py"
A=/mnt/d/vsps_papers/vsps-paperA-spic/paper; B=/mnt/d/vsps_papers/vsps-paperB-lre/paper; C=/mnt/d/vsps_papers/vsps-paperC-tallip/paper_v1_analysis
T=manuscript/conf_taimma_2027; rc=0
$K $R/parts/A_report.md --src $A/*.md $A/number_manifest.tsv $A/figs/CAPTIONS.md $A/figs/VALUES.json ${A_EXTRA:-} --bib $A/paperA.bib $A/paperA_manual.bib --allow $R/parts/A_report.allow.tsv || rc=1
$K $R/parts/B_report.md --src $B/*.md $B/number_manifest_B.tsv ${B_EXTRA:-$B/../prereg/2026-10-28_b1_scaling/PREREG.md $B/../prereg/2026-10-28_d_extrap/PREREG.md} --bib $B/paperB.bib --allow $R/parts/B_report.allow.tsv || rc=1
$K $R/parts/C_report.md --src $C/*.md $C/number_manifest_C.tsv ${C_EXTRA:-$C/../prereg/2026-10-25_c_test/PREREG.md $C/../prereg/2026-10-22_c_stage2/PREREG.md} --bib $C/paperC.bib --allow $R/parts/C_report.allow.tsv || rc=1
$K $R/parts/D_taimma_report.md --src $T/draft_v1/paper.md $T/draft_v1/number_manifest_TAIMMA.tsv $T/draft_v1/CHECKS.md $T/draft_v1/DRAFT_NOTES.md $T/draft_v1/PARAGRAPH_SOURCES.tsv $T/WRITING_PLAN_C_TAIMMA_v1.md manuscript/cfp/TAIMMA_CONF_2026-11-13.md $C/*.md ${D_EXTRA:-} --bib $C/paperC.bib --allow $R/parts/D_taimma_report.allow.tsv || rc=1
$K $R/parts/E_tinh_trang.md --src manuscript/KE_HOACH_SAU_GAN_NHAN_2026-11-14.md manuscript/GOAL_HIEN_TAI.md $A/sec7_verbosity_sign.md --allow $R/parts/E_tinh_trang.allow.tsv || rc=1
$K $R/parts/00_mo_dau.md --src $R/parts/A_report.md $R/parts/B_report.md $R/parts/C_report.md $R/parts/D_taimma_report.md $R/parts/E_tinh_trang.md --allow $R/parts/00_mo_dau.allow.tsv || rc=1
echo "ALL PARTS rc=$rc"; exit $rc
