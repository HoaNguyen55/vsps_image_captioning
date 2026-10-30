# Updates the TOC in Word, saves *_word.docx (move it over the original), exports the PDF.
# Paths are literal: the $MyInvocation-based version stalled Word under COM.
$w = New-Object -ComObject Word.Application
$w.DisplayAlerts = 0
$d = $w.Documents.Open("D:\vsps_image_captioning\manuscript\ncs_proposal\DeCuong_NCS_LHU_2026-10_v7.docx")
$d.TablesOfContents.Item(1).Update()
$d.SaveAs2("D:\vsps_image_captioning\manuscript\ncs_proposal\DeCuong_NCS_LHU_2026-10_v7_word.docx", 16)
$d.ExportAsFixedFormat("D:\vsps_image_captioning\manuscript\ncs_proposal\DeCuong_NCS_LHU_2026-10_v7.pdf", 17)
$d.Close(0); $w.Quit()
