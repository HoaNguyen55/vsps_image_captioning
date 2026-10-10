"""Build FAIR_VSPS_v11_talk.pptx from a copy of v10, applying the slide audit (REVIEW_PHASES_v10.md, D + H).

v10 is only read; every change below edits run text, table cells, notes, or adds a small shape
styled like its neighbours (fonts/colours from build_talk.py).
"""
import copy
import os
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_CONNECTOR
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_talk import ACCENT, LABEL, SOFT, arrow, textbox  # noqa: E402

ROOT = os.path.join(HERE, "..")
SRC = os.path.join(ROOT, "FAIR_VSPS_v10_talk.pptx")
OUT = os.path.join(ROOT, "FAIR_VSPS_v11_talk.pptx")
NB = " "


def shape(slide, sid):
    return next(s for s in slide.shapes if s.shape_id == sid)


def set_runs(para, texts):
    """Write texts into the paragraph's existing runs; clone the last run if more texts are needed."""
    runs = para.runs
    while len(runs) < len(texts):
        para._p.insert(para._p.index(runs[-1]._r) + 1, copy.deepcopy(runs[-1]._r))
        runs = para.runs
    for run, text in zip(runs, texts):
        run.text = text
    for run in runs[len(texts):]:
        para._p.remove(run._r)


def set_text(sh, k, *texts):
    set_runs(sh.text_frame.paragraphs[k], list(texts))


def add_para(tf, src_k, texts, size=None, color=None, bold=None):
    """Append a copy of paragraph src_k with new run texts (optionally restyled)."""
    new = copy.deepcopy(tf.paragraphs[src_k]._p)
    tf._txBody.append(new)
    para = tf.paragraphs[-1]
    set_runs(para, texts)
    for run in para.runs:
        if size:
            run.font.size = Pt(size)
        if color is not None:
            run.font.color.rgb = color
        if bold is not None:
            run.font.bold = bold
    return para


def drop_paras_after(tf, k):
    for para in tf.paragraphs[k + 1:]:
        tf._txBody.remove(para._p)


def cell(table, r, c, *texts):
    set_runs(table.cell(r, c).text_frame.paragraphs[0], list(texts))


def place(sh, x=None, y=None, w=None, h=None):
    if x is not None:
        sh.left = Inches(x)
    if y is not None:
        sh.top = Inches(y)
    if w is not None:
        sh.width = Inches(w)
    if h is not None:
        sh.height = Inches(h)


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text.strip()


def size(sh, pt):
    for para in sh.text_frame.paragraphs:
        for run in para.runs:
            run.font.size = Pt(pt)


def drop_exit_animations(slide):
    """Remove exit effects so every build step stays visible (shapes no longer share one spot)."""
    timing = slide._element.find(qn("p:timing"))
    for ctn in list(timing.iter(qn("p:cTn"))):
        if ctn.get("presetClass") != "exit":
            continue
        par = ctn.getparent()
        lst = par.getparent()
        lst.remove(par)
        while len(lst) == 0 and lst.tag == qn("p:childTnLst"):  # prune emptied click groups
            par = lst.getparent().getparent()
            lst = par.getparent()
            lst.remove(par)


def font_tb(slide, xywh, paras, pt, color, **style):
    """Montserrat text box (build_talk.textbox); style: bold, align, italic."""
    italic = style.pop("italic", False)
    tb = textbox(slide, *xywh, paras, size=pt, color=color, **style)
    for para in tb.text_frame.paragraphs:
        for run in para.runs:
            run.font.italic = italic
    return tb


def build():
    prs = Presentation(SRC)
    S = [None] + list(prs.slides)

    # 1 -- email; data-level distillation in notes
    set_text(shape(S[1], 182), 2, "nguyenleh760@gmail.com")
    notes(S[1], """
Tôi xin trình bày nghiên cứu VSPS — Verified Structured Proposition Synthesis, một phương pháp xây dựng dữ liệu giám sát từ các mệnh đề có cấu trúc đã được kiểm chứng, nhằm giảm hiện tượng ảo giác trong mô tả ảnh tiếng Việt.
Điểm chính của phương pháp là: thực hiện kiểm chứng trong giai đoạn xây dựng dữ liệu, sau đó đưa kết quả kiểm chứng vào mô hình gián tiếp qua dữ liệu SFT: chưng cất ở mức dữ liệu, không dùng logit mô hình thầy, không thêm hàm mất mát. Bộ kiểm chứng không tham gia hàm mất mát.
""")

    # 2 -- coloured words are outside the references, not necessarily wrong
    font_tb(S[2], (1.96, 6.27, 9.42, 0.32), ["Tô màu: CHAIR tính là ngoài tham chiếu, không nhất thiết sai"],
            12.5, LABEL, align=PP_ALIGN.CENTER, italic=True)
    notes(S[2], """
Động lực của nghiên cứu xuất phát từ một vấn đề khá rõ khi chúng tôi thử mô tả ảnh chi tiết. Ví dụ ở ảnh số 706, mô hình có thể sinh ra những đối tượng hoặc chi tiết không được xác nhận theo cách đánh giá dựa trên reference.
Các từ tô màu là những từ CHAIR tính là ngoài tham chiếu, không nhất thiết sai: chiếc túi thực ra có trong ảnh. Vì thế CHAIR trên KTVIC là cận trên.
""")

    # 3 -- decimal comma
    set_text(shape(S[3], 216), 0, "4,26")

    # 4 -- decimal comma; denominator of the gender metric
    set_text(shape(S[4], 235), 0, "46,9%")
    sh = shape(S[4], 236)
    set_text(sh, 0, sh.text_frame.paragraphs[0].runs[0].text, " ",
             "mô tả zero-shot dùng danh từ có giới tính mà không câu tham chiếu nào dùng "
             "(23/49 ảnh có dấu hiệu giới tính, tập thử thách 50 ảnh)")
    for sid in (235, 236):
        sh = shape(S[4], sid)
        place(sh, y=sh.top / 914400 - 0.08)
    notes(S[4], """
Không chỉ đối tượng, chúng tôi còn quan sát vấn đề với các thuộc tính như giới tính và màu sắc.
Tuy nhiên, cần phân biệt rõ: con số 46,9% không phải độ chính xác nhận diện giới tính. Đây là tỷ lệ mô tả dùng danh từ có giới tính mà không câu tham chiếu nào của ảnh dùng, tính trên tập thử thách 50 ảnh, trong đó 49 ảnh có dấu hiệu giới tính: 23/49 ảnh.
Vì vậy, bài toán không đơn giản là làm cho mô hình “nhìn thấy vật thể”, mà cần một cơ chế biến bằng chứng thị giác thành dữ liệu supervision có cấu trúc.
""")

    # 5 -- question box no longer hides the "Hạn chế" row
    tbl = shape(S[5], 248)
    tbl.table.rows[1].height = Inches(1.2)
    tbl.table.rows[2].height = Inches(1.2)
    place(shape(S[5], 249), y=5.08, h=1.75)
    place(shape(S[5], 250), y=5.20)
    notes(S[5], S[5].notes_slide.notes_text_frame.text + "\n"
          "VSPS thuộc nhóm dữ liệu: không đổi kiến trúc, không thêm loss, không thêm bước nào lúc suy luận.")

    # 6 -- Phase 1 = data construction + fine-tuning; 1A/1B; only this model is deployed
    s6 = S[6]
    hdr = shape(s6, 261)
    set_text(hdr, 0, "Pha 1 · Xây dựng dữ liệu + tinh chỉnh")
    add_para(hdr.text_frame, 0, ["(một lần, offline)"], size=14, bold=False)
    hdr.text_frame.paragraphs[0].runs[0].font.size = Pt(16)
    place(hdr, y=2.12, h=0.75)
    # column 1 boxes re-spaced so 1A/1B have room for two lines
    place(shape(s6, 265), y=3.83, h=0.75)
    t1a = shape(s6, 266)
    set_text(t1a, 0, "1A · Dựng dữ liệu VSPS")
    add_para(t1a.text_frame, 0, ["4 bước, có kiểm chứng"], size=14, color=SOFT, bold=False)
    place(t1a, y=3.86, h=0.70)
    size(t1a, 17)
    t1a.text_frame.paragraphs[1].runs[0].font.size = Pt(14)
    place(shape(s6, 267), y=4.58, h=0.22)
    place(shape(s6, 268), y=4.80, h=0.75)
    t1b = shape(s6, 269)
    set_text(t1b, 0, "1B · Tinh chỉnh QLoRA-SFT")
    add_para(t1b.text_frame, 0, ["Qwen2.5-VL-7B · loss SFT chuẩn"], size=14, color=SOFT)
    size(t1b, 17)
    t1b.text_frame.paragraphs[1].runs[0].font.size = Pt(14)
    place(t1b, y=4.83, h=0.70)
    place(shape(s6, 270), y=5.55, h=0.22)
    place(shape(s6, 271), y=5.77, h=0.50)
    place(shape(s6, 272), y=5.78)
    # Phase-2 notes under "Mô tả một lượt"
    dep = shape(s6, 282)
    set_text(dep, 0, "ngắn hoặc chi tiết")
    set_text(dep, 1, "một lượt greedy")
    set_text(dep, 2, "không kiểm chứng")
    add_para(dep.text_frame, 2, ["không truy hồi"])
    add_para(dep.text_frame, 2, ["không hậu xử lý"])
    size(dep, 13)
    # arrow Phase 1 model -> Phase 2 model, with its label
    src = shape(s6, 264)._element.spPr.find(qn("a:ln"))
    con = s6.shapes.add_connector(MSO_CONNECTOR.ELBOW, Inches(4.15), Inches(6.02), Inches(4.51), Inches(4.10))
    ln = con.line._get_or_add_ln()
    ln.getparent().replace(ln, copy.deepcopy(src))
    con.line.color.rgb = ACCENT
    font_tb(s6, (0.72, 6.27, 3.49, 0.30), ["chỉ mô hình này được triển khai ↗"], 12, ACCENT,
            bold=True, align=PP_ALIGN.RIGHT)
    # data column
    data = shape(s6, 285)
    set_text(data, 2, "Pha 1: 3.700 ảnh · 69 ảnh thử pipeline (không SFT, không đánh giá)")
    set_text(data, 3, "Không dùng: ảnh test, câu tham chiếu gốc")
    set_text(data, 5, "COCO-2014: 5.000 ảnh, không dùng để SFT")
    place(shape(s6, 284), h=2.50)
    chain = shape(s6, 286)
    set_text(chain, 0, "Bằng chứng thị giác → Mệnh đề đã kiểm chứng → Mô tả giám sát → SFT → Mô tả một lượt")
    size(chain, 17)
    place(chain, y=6.62)
    notes(s6, """
Ý tưởng chính của VSPS là chuyển bước kiểm chứng từ lúc suy luận sang lúc xây dựng dữ liệu huấn luyện.
Pha 1 chạy một lần, offline, và gồm hai việc nối tiếp: dựng dữ liệu xong rồi mới tinh chỉnh. Ở bước 1A, từ ảnh huấn luyện, bốn bước có kiểm chứng tạo ra kho 7.177 mẫu giám sát trên 3.617 ảnh. Ở bước 1B, QLoRA-SFT tinh chỉnh Qwen2.5-VL-7B với hàm mất mát SFT chuẩn và chỉ đọc kho này.
Đầu ra Pha 1 là adapter LoRA trên Qwen2.5-VL-7B, và chỉ mô hình này được triển khai.
Sang Pha 2, khi có một ảnh mới, chúng tôi chỉ đưa ảnh đó vào mô hình đã tinh chỉnh và mô tả trong một lượt greedy.
Lúc triển khai không gọi Vintern-1B, không sinh hay chọn mệnh đề: không kiểm chứng, không truy hồi và không hậu xử lý.
Với KTVIC, chúng tôi có 4.327 ảnh và 21.635 câu mô tả. Pha 1 dùng 3.700 ảnh huấn luyện; 69 ảnh huấn luyện khác chỉ dùng để thử pipeline, không dùng để SFT hay đánh giá. Ảnh test và câu tham chiếu gốc không được dùng để dựng dữ liệu. COCO-2014 với 5.000 ảnh chỉ dùng để đánh giá, không dùng để SFT.
Vì vậy, có thể tóm tắt VSPS bằng chuỗi:
Bằng chứng thị giác → Mệnh đề đã kiểm chứng → Mô tả giám sát → SFT → Mô tả một lượt.
""")

    # 7 -- model roles, budgets, output store
    s7 = S[7]
    set_text(shape(s7, 292), 0, "Pha 1A · Bốn bước dựng dữ liệu giám sát")
    set_text(shape(s7, 296), 1, "Qwen2.5-VL-7B (bộ sinh) · 5 loại · ~52/ảnh")
    set_text(shape(s7, 300), 1, "Vintern-1B (bộ kiểm chứng, chỉ ở Pha 1)")
    set_text(shape(s7, 308), 1, "tối đa 2 (ngắn) / 9 (chi tiết) mệnh đề")
    for sid in (296, 300, 304, 308):
        shape(s7, sid).text_frame.paragraphs[1].runs[0].font.size = Pt(16)
    out_box = copy.deepcopy(shape(s7, 306)._element)
    s7.shapes._spTree.append(out_box)
    ob = s7.shapes[-1]
    out_box.find(qn("p:nvSpPr")).find(qn("p:cNvPr")).set("id", "9001")
    place(ob, x=9.70, y=5.82, w=3.25, h=1.11)
    ob.line.color.rgb = ACCENT
    arrow(s7, 9.40, 6.37, 9.70, 6.37)
    tb = font_tb(s7, (9.76, 5.88, 3.13, 1.03), ["Kho 7.177 mẫu / 3.617 ảnh"], 14, ACCENT,
                 bold=True, anchor=MSO_ANCHOR.MIDDLE)
    add_para(tb.text_frame, 0, ["chạy một lần, offline → sau đó mới QLoRA-SFT"], size=12, color=LABEL, bold=False)
    notes(s7, """
Sau khi đã thấy ý tưởng tổng thể, tôi đi vào bốn bước của bước 1A: xây dựng dữ liệu giám sát.
Bước một, từ ảnh huấn luyện, chúng tôi dùng Qwen2.5-VL-7B làm bộ sinh để sinh và chuẩn hóa các mệnh đề. Đây là cùng backbone với mô hình sẽ được tinh chỉnh, nhưng ở đây chỉ chạy suy luận để sinh dữ liệu. Mỗi ảnh có khoảng 52 mệnh đề, thuộc năm loại: thực thể, thuộc tính, hành động, số lượng và quan hệ.
Bước hai, các mệnh đề được kiểm chứng bằng Vintern-1B, đóng vai trò bộ kiểm chứng và chỉ dùng ở Pha 1.
Bước ba, với những thông tin chưa chắc chắn, chúng tôi không nhất thiết loại bỏ toàn bộ mệnh đề mà thực hiện trung hòa phần không chắc, giữ lại phần thông tin vẫn có bằng chứng.
Bước bốn, chúng tôi chọn các mệnh đề phù hợp rồi chuyển chúng thành mô tả tiếng Việt: tối đa 2 mệnh đề cho mô tả ngắn và 9 mệnh đề cho mô tả chi tiết.
Kết quả là kho 7.177 mẫu trên 3.617 ảnh, chạy một lần, offline; sau đó mới QLoRA-SFT.
""")

    # 8 -- per-branch aggregation (5 + 5), ceiling rules, colour cross-check by the generator
    s8 = S[8]
    set_text(shape(s8, 314), 0, "Pha 1A · Dữ liệu giám sát · Bước 2")
    agg = shape(s8, 339)
    set_text(agg, 0, "Tổng hợp từng nhánh (5 + 5) → ", "3 trạng thái")
    set_text(agg, 1, "Luật trần chỉ hạ mức")
    add_para(agg.text_frame, 1, ["Màu: hỏi thêm bộ sinh Qwen2.5-VL-7B, bất đồng → không chắc chắn"])
    size(agg, 13)
    for run in agg.text_frame.paragraphs[0].runs:
        run.font.size = Pt(17)
    place(shape(s8, 338), y=6.15, h=0.88)
    place(agg, y=6.15, h=0.88)
    notes(s8, """
Tôi nói rõ hơn về bước 2, kiểm chứng ba trạng thái.
Ví dụ, với mệnh đề “một chiếc thuyền”, hệ thống không chỉ hỏi một câu “Trong ảnh có chiếc thuyền không?”.
Chúng tôi dùng cả câu khẳng định và câu phủ định, mỗi câu hỏi bộ kiểm chứng Vintern-1B 5 lần.
Năm câu trả lời của mỗi nhánh được tổng hợp riêng, theo cực đa số và mức đồng thuận; sau đó hai nhánh mới được kết hợp thành ba trạng thái.
ĐƯỢC HỖ TRỢ đòi hỏi nhánh khẳng định dứt khoát và ổn định: chỉ một câu trả lời lệch ở nhánh khẳng định là đã thành KHÔNG CHẮC CHẮN. Nếu đa số “có” ở cả hai nhánh, tức là đồng ý với bất cứ câu hỏi nào, mệnh đề cũng là KHÔNG CHẮC CHẮN.
Nếu câu khẳng định bị đáp “không” ổn định, hoặc chỉ câu phủ định được đáp “có”, mệnh đề BỊ BÁC BỎ.
Sau đó, luật trần chỉ có thể hạ mức: số đếm lớn hơn năm, mệnh đề bộ sinh đánh dấu là suy luận, và danh từ có giới tính khi không có dấu hiệu rõ đều bị giới hạn ở KHÔNG CHẮC CHẮN; quan hệ không gian cũng vậy.
Riêng mệnh đề về màu sắc, chúng tôi hỏi thêm bộ sinh Qwen2.5-VL-7B; nếu hai mô hình bất đồng ở câu khẳng định thì hạ xuống KHÔNG CHẮC CHẮN, ở 2.518 trên 10.626 mệnh đề được kiểm tra chéo.
Mục tiêu ở đây là không biến một bằng chứng yếu thành một khẳng định chắc chắn.
""")

    # 9 -- what 461 -> 83 counts; offline neutralization; drop numbers not in the paper
    s9 = S[9]
    set_text(shape(s9, 348), 0, "Pha 1A · Ba trạng thái và trung hòa")
    set_text(shape(s9, 364), 0, "mệnh đề được giữ lại nhờ trung hòa (offline, dùng lại câu trả lời đã lưu)")
    place(shape(s9, 364), w=5.30)
    set_text(shape(s9, 366), 0, "ảnh huấn luyện không còn mệnh đề dùng được (trước → sau trung hòa)")
    notes(s9, """
Ở bước 3, KHÔNG CHẮC CHẮN không có nghĩa là sai. Với danh từ có giới tính không rõ, chúng tôi trung hòa: ví dụ “một người phụ nữ mặc áo đỏ” thành “một người mặc áo đỏ”, khi áo và màu vẫn có bằng chứng.
Bước trung hòa chạy offline: nó dùng lại các câu trả lời đã lưu, không hỏi lại mô hình nào, và chỉ áp dụng khi bằng chứng còn lại nhất trí 5/5.
11.769 mệnh đề được giữ lại nhờ trung hòa, trong đó có 3.276 thực thể người, trên 2.351 ảnh. Đây là các mệnh đề KHÔNG CHẮC CHẮN được phục hồi sau trung hòa, không phải mệnh đề bộ kiểm chứng gán ĐƯỢC HỖ TRỢ ngay từ đầu.
461 → 83: số ảnh huấn luyện không còn mệnh đề dùng được giảm từ 461 trước trung hòa xuống 83 sau trung hòa. Nếu không trung hòa, luật trần giới tính đã xóa toàn bộ nội dung về người ở 74% ảnh huấn luyện có người.
Các số chi tiết theo từng trạng thái lấy từ record Pha 1 công bố trong repo.
""")

    # 10 -- challenge-set denominator; define P2
    s10 = S[10]
    t10 = shape(s10, 374).table
    cell(t10, 3, 0, "Danh từ có giới tính ngoài tham chiếu (50 ảnh thử thách) ↓")
    for c, frac in ((1, "(23/49)"), (3, "(2/49)")):
        para = add_para(t10.cell(3, c).text_frame, 0, [frac], size=11)
        para.runs[0].font.bold = False
    for r, h in ((0, 0.55), (1, 0.62), (2, 0.48), (3, 0.95), (4, 0.48)):
        t10.rows[r].height = Inches(h)
    font_tb(s10, (1.03, 6.20, 11.5, 0.32),
            ["P2: cùng Qwen2.5-VL-7B + QLoRA-SFT, dữ liệu chưa kiểm chứng · "
             "các chỉ số khác tính trên 558 ảnh test"], 12, LABEL)
    notes(s10, """
Bây giờ tôi chuyển sang kết quả chính trên 558 ảnh test của KTVIC, chế độ chi tiết.
Với zero-shot, trung bình có 4,26 đối tượng ảo giác trên mỗi mô tả. P2 giảm xuống 2,05, còn VSPS giảm tiếp xuống 1,57.
Tương tự, CHAIRs giảm từ 98,0% xuống 79,2%.
Danh từ có giới tính ngoài tham chiếu được đo trên tập thử thách 50 ảnh, trong đó 49 ảnh có dấu hiệu giới tính: tỷ lệ giảm từ 46,9%, tức 23/49, xuống 4,1%, tức 2/49.
Số đối tượng được mô tả cũng giảm, từ 6,54 xuống 3,13 đối tượng mỗi mô tả. Một phần mức giảm là do nói ít hơn, nhưng CHAIRi theo lần nhắc vẫn giảm từ 65,1 xuống 50,1%, và ở độ phủ gần như P2, 3,80 so với 3,13 đối tượng, VSPS vẫn ít ảo giác hơn: 1,57 so với 2,05.
P2 dùng cùng Qwen2.5-VL-7B và cùng công thức QLoRA-SFT; khác biệt duy nhất là P2 học trên mô tả ứng viên chưa kiểm chứng, còn VSPS học trên dữ liệu đã kiểm chứng.
""")

    # 11 -- passes per image, COCO caveat, the two result boxes no longer overlap
    s11 = S[11]
    t11 = shape(s11, 392).table
    for r, name, note in ((2, "VCD", f" (lúc suy luận, 2{NB}lượt/ảnh)"),
                          (3, "Tự sửa lỗi", f" (2{NB}lượt/ảnh)"), (5, "VSPS", f" (1{NB}lượt/ảnh)")):
        cell(t11, r, 0, name, note)
        t11.cell(r, 0).text_frame.paragraphs[0].runs[1].font.size = Pt(14)
    place(shape(s11, 389), y=4.55, h=0.85)           # box: instructed zero-shot
    place(shape(s11, 395), x=1.20, y=4.74, w=5.80)
    place(shape(s11, 393), x=7.00, y=4.58, w=5.45)
    place(shape(s11, 399), y=5.50, h=0.85)           # box: VSPS
    place(shape(s11, 401), x=1.20, y=5.69, w=5.80)
    place(shape(s11, 400), x=7.00, y=5.53, w=5.45)
    for sid in (393, 400):
        sh = shape(s11, sid)
        sh.text_frame.paragraphs[0].alignment = PP_ALIGN.RIGHT
        size(sh, 32)
    set_text(shape(s11, 401), 0, "VSPS (dữ liệu đã kiểm chứng)")
    font_tb(s11, (1.03, 6.43, 11.57, 0.32),
            ["COCO: ngoài miền SFT, có thể nằm trong dữ liệu tiền huấn luyện; "
             "không chứng minh khái quát đa ngôn ngữ"], 12, LABEL, italic=True)
    drop_exit_animations(s11)
    notes(s11, """
Bảng này so VSPS với các phương pháp giảm ảo giác trên cùng backbone. VCD và Tự sửa lỗi can thiệp lúc suy luận và theo thiết kế cần hai lượt cho mỗi ảnh; VSPS chỉ cần một lượt. Chúng tôi không so độ trễ trực tiếp vì chưa đo cùng giao thức; số lượt là theo thiết kế.
Khi đưa toàn bộ quy tắc VSPS vào câu lệnh, ảo giác chỉ giảm 7%, từ 4,26 xuống 3,97; còn VSPS giảm 63,1%, xuống 1,57.
Điều này cho thấy việc chuyển kết quả kiểm chứng thành dữ liệu SFT có tác động lớn hơn so với chỉ đưa các quy tắc vào câu lệnh.
Chúng tôi tiếp tục đánh giá trên toàn bộ 5.000 ảnh test Karpathy của COCO-2014, không dùng tập này để SFT.
VSPS đạt 0,17 đối tượng ảo giác trên mỗi mô tả và CHAIRs 15,4%. COCO nằm ngoài miền SFT nhưng có thể đã nằm trong dữ liệu tiền huấn luyện của backbone, nên không phải ảnh chưa từng thấy, và kết quả này không chứng minh khả năng khái quát đa ngôn ngữ.
""")

    # 12 -- COCO precision/recall/F1; VSPS = mean of 3 seeds
    s12 = S[12]
    set_text(shape(s12, 414), 0,
             "KTVIC, chế độ chi tiết, % · VSPS: trung bình 3 seed · độ chính xác = precision, độ bao phủ = recall")
    place(shape(s12, 414), w=7.0)
    tb = font_tb(s12, (8.15, 4.75, 4.5, 0.80), ["COCO: P 80,5 → 88,2 · R 63,3 → 45,9"], 15, SOFT)
    add_para(tb.text_frame, 0, ["F1 70,9 → 60,4"], color=ACCENT, bold=True)
    notes(s12, """
Tuy nhiên, VSPS có một cái giá rõ ràng.
Trên KTVIC, độ chính xác tăng từ 31,6 lên 41,9%, nhưng độ bao phủ giảm từ 57,1 xuống 37,1%; các số của VSPS là trung bình 3 seed.
F1 giảm nhẹ trên KTVIC, từ 40,7 xuống 39,3, nhưng trên COCO giảm rõ: độ chính xác tăng từ 80,5 lên 88,2, độ bao phủ giảm từ 63,3 xuống 45,9, và F1 giảm từ 70,9 xuống 60,4.
Độ dài caption cũng giảm rất mạnh, từ 117 xuống 34 từ mỗi mô tả.
Mô hình học được phong cách thận trọng từ dữ liệu; lúc triển khai không có gì kiểm chứng lại.
Với bài toán hỗ trợ người khiếm thị, chúng tôi cho rằng đây là một trade-off đáng cân nhắc, bởi một khẳng định sai có thể gây hại hơn việc bỏ sót một chi tiết.
Tuy nhiên, đây vẫn là một vấn đề mở vì chúng tôi muốn tăng coverage mà không làm hallucination tăng trở lại.
""")

    # 13 -- zero-shot comparison wording, audit source, the two verdict lines no longer overlap
    s13 = S[13]
    set_text(shape(s13, 424), 0, "Chấm mô tả (đầu ra Pha 2) · 2 người chấm, thang 1–5")
    audit = shape(s13, 428)
    set_text(audit, 0, "Người gán nhãn độc lập xem lại 244 mệnh đề mà bộ kiểm chứng gán "
             "ĐƯỢC HỖ TRỢ (khi chạy pipeline trên 83 ảnh test)")
    audit.text_frame.paragraphs[0].alignment = PP_ALIGN.LEFT
    size(audit, 13)
    place(audit, w=4.45)
    p2 = shape(s13, 426)
    place(p2, x=1.21, y=5.52, w=10.92, h=0.45)
    size(p2, 20)
    zs = shape(s13, 437)
    set_text(zs, 0, "So với zero-shot: VSPS ", "không", " được chấm trung thực hơn (3,91 so với 4,17; "
             "p = 0,12; tốt hơn ở 16 ảnh, kém ở 24); kém hơn về độ đầy đủ và trôi chảy")
    place(zs, x=1.21, y=5.95, w=10.92, h=0.95)
    size(zs, 20)
    drop_exit_animations(s13)
    notes(s13, """
Ngoài các metric tự động, hai người chấm bản ngữ, không phải tác giả, chấm độc lập mô tả chi tiết của zero-shot, P2 và VSPS trên 50 ảnh test, tức 150 mô tả, theo thang điểm từ 1 đến 5. Đây là đầu ra Pha 2.
Zero-shot đạt 4,17 về độ trung thực, 4,47 về độ đầy đủ và 4,29 về độ trôi chảy.
VSPS đạt lần lượt 3,91; 2,64 và 3,17.
So với P2, VSPS tốt hơn ở cả ba tiêu chí.
So với zero-shot, VSPS không được chấm trung thực hơn: 3,91 so với 4,17, p = 0,12; tốt hơn ở 16 ảnh, kém ở 24. VSPS cũng kém hơn rõ về độ đầy đủ và độ trôi chảy.
Có hai lý do: CHAIR trên KTVIC phạt cả vật có thật mà tham chiếu không nhắc, còn người chấm thì không; và câu ghép theo khuôn mẫu làm giảm độ trôi chảy.
Chúng tôi cũng thực hiện một đánh giá khác: một người gán nhãn độc lập, không phải tác giả, xem lại 244 mệnh đề mà bộ kiểm chứng gán ĐƯỢC HỖ TRỢ khi chạy pipeline trên 83 ảnh test, tối đa ba mệnh đề mỗi ảnh. Đây không phải dữ liệu huấn luyện.
Người gán nhãn xác nhận 63,1%, bác bỏ 25,4%, và 11,5% chưa thể kết luận.
Kết quả này cho thấy bộ kiểm chứng hiện tại chưa hoàn hảo. Đây cũng là một trong những giới hạn lớn nhất của VSPS.
""")

    # 14 -- six limitations grouped in four; constrained-LM already used for 650/3,560; summary
    s14 = S[14]
    t14 = shape(s14, 445).table
    cell(t14, 0, 0, "Hạn chế (H1–H6, gộp 4 nhóm)")
    cell(t14, 1, 0, "Phụ thuộc bộ kiểm chứng: người rà soát bác bỏ 25,4% mệnh đề bộ kiểm chứng gán "
         f"ĐƯỢC HỖ TRỢ; bộ sinh và bộ kiểm chứng cùng họ mô hình ngôn ngữ Qwen, lỗi có thể tương{NB}quan")
    cell(t14, 4, 1, f"Mở rộng LM có ràng buộc (hiện 650/3.560), thay câu ghép theo khuôn{NB}mẫu")
    summ = shape(s14, 446)
    set_text(summ, 0, "Tóm lại: ", "VSPS giảm mạnh ảo giác đối tượng trên KTVIC và COCO, đổi lại độ bao phủ "
             "giảm; người chấm xác nhận lợi ích so với SFT chưa kiểm chứng, nhưng chưa thấy VSPS trung thực "
             "hơn zero-shot")
    size(summ, 14)
    place(summ, y=6.70, h=0.55)
    set_text(shape(s14, 449), 0, f"“một chiếc thuyền”, “hai chiếc thuyền”: bộ kiểm chứng gán ĐƯỢC HỖ TRỢ, "
             f"người rà soát bác{NB}bỏ")
    notes(s14, """
Bài báo nêu sáu hạn chế, từ H1 đến H6; ở đây tôi gộp thành bốn nhóm.
Thứ nhất, VSPS phụ thuộc vào chất lượng của bộ kiểm chứng. Trong đợt rà soát thủ công, 25,4% mệnh đề bộ kiểm chứng gán ĐƯỢC HỖ TRỢ bị con người bác bỏ. Ngoài ra, bộ sinh và bộ kiểm chứng cùng họ mô hình ngôn ngữ Qwen, nên lỗi có thể tương quan.
Thứ hai, các metric hiện tại còn khá hẹp, chủ yếu tập trung vào object hallucination và danh từ giới tính; CHAIR trên KTVIC là cận trên, và chúng tôi mới đánh giá trên KTVIC và COCO.
Thứ ba, độ bao phủ giảm khá mạnh: từ 57,1 xuống 37,1% trên KTVIC và từ 63,3 xuống 45,9% trên COCO.
Thứ tư, độ trôi chảy cũng thấp hơn, 3,17 so với 4,29, một phần do câu huấn luyện ghép theo khuôn mẫu.
Vì vậy, hướng phát triển tiếp theo là sử dụng nhiều bộ kiểm chứng khác loại, kết hợp kiểm chứng với vùng ảnh, xây dựng metric ở mức proposition, đồng thời tìm cách tăng coverage mà không làm hallucination tăng trở lại.
Chúng tôi cũng muốn mở rộng nhánh mô hình ngôn ngữ có ràng buộc, hiện mới dùng cho 650 trên 3.560 mô tả chi tiết, để câu huấn luyện tự nhiên hơn.
Tóm lại, VSPS giảm mạnh ảo giác đối tượng trên KTVIC và COCO, đổi lại độ bao phủ giảm; người chấm xác nhận lợi ích so với SFT chưa kiểm chứng, nhưng chưa thấy VSPS trung thực hơn zero-shot.
""")

    # 15 -- email
    set_text(shape(S[15], 457), 3, "Email: ", "nguyenleh760@gmail.com")

    # 16 -- no "cửa hàng" claim; Phase-2 verbatim label
    s16 = S[16]
    set_text(shape(s16, 466), 0, "KTVIC #706 · đầu ra Pha 2, nguyên văn")
    place(shape(s16, 466), x=0.92, w=5.64)
    set_text(shape(s16, 467), 1, "Ngoài tham chiếu theo CHAIR: “cửa”, “túi” (túi có trong ảnh); danh từ “cô” "
             f"không có trong tham chiếu (tham chiếu viết “cô{NB}gái”)")
    notes(s16, """
Ví dụ A là đầu ra Pha 2, trích nguyên văn. Zero-shot dùng danh từ “cô”, trong khi các câu tham chiếu viết “cô gái”; chỉ số giới tính so khớp theo dạng từ nên tính đây là danh từ có giới tính ngoài tham chiếu. VSPS dùng danh từ trung tính “một người”.
Theo CHAIR, “cửa” và “túi” nằm ngoài tham chiếu, dù túi thực ra có trong ảnh.
Chỉ số giới tính không đo độ đúng giới tính thực.
""")

    # 17 -- test image, not Phase 1 / not a deployed output
    s17 = S[17]
    set_text(shape(s17, 474), 0, "Ví dụ B: một lỗi của bộ kiểm chứng (ảnh test)")
    set_text(shape(s17, 477), 0, "KTVIC #2921 · ảnh test")
    body = shape(s17, 478)
    set_text(body, 0, "Pipeline chạy trên ảnh test, không phải đầu ra triển khai: bộ kiểm chứng gán ĐƯỢC HỖ TRỢ "
             f"cho cả ba mệnh đề; người rà soát bác bỏ hai (nằm trong 25,4% bị bác{NB}bỏ)")
    set_text(body, 1, "Hành động: “một chiếc thuyền nhỏ một người đang ngồi trên thuyền, cầm một thanh gậy” — "
             f"bộ kiểm chứng: ĐƯỢC{NB}HỖ{NB}TRỢ · người: xác{NB}nhận")
    set_text(body, 2, f"Thực thể: “một chiếc thuyền” — bộ kiểm chứng: ĐƯỢC{NB}HỖ{NB}TRỢ · người: ", f"bác{NB}bỏ")
    set_text(body, 3, f"Số lượng: “hai chiếc thuyền” — bộ kiểm chứng: ĐƯỢC{NB}HỖ{NB}TRỢ · người: ", f"bác{NB}bỏ")
    notes(s17, """
Ví dụ B là ảnh test #2921, lấy từ lần chạy pipeline dựng dữ liệu trên ảnh test, không phải đầu ra triển khai. Bộ kiểm chứng gán ĐƯỢC HỖ TRỢ cho cả ba mệnh đề; người gán nhãn xác nhận mệnh đề hành động nhưng bác bỏ “một chiếc thuyền” và “hai chiếc thuyền”, vì ảnh có nhiều hơn hai chiếc thuyền.
Lỗi kiểu này cũng có trong dữ liệu giám sát; lúc triển khai không có bộ kiểm chứng nào chạy.
""")

    prs.save(OUT)
    print("saved", OUT)


if __name__ == "__main__":
    build()
