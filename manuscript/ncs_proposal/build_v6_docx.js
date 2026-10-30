// v6: build_v5_docx.js pointed at DeCuong_NCS_LHU_2026-10_v6.md, with NĐ 30/2020 Phụ lục I typography:
// 6 pt after each paragraph, page number centred in the top margin (13 pt), none on page 1.
// Run: NODE_PATH=<dir with node_modules/docx> node build_v6_docx.js
// Then render_v6_word.ps1 updates the table of contents in Word and exports the PDF.
// Source markup: # / ## / ### headings, "- " bullets ("  - " level 2), pipe tables,
// **bold**, *italic*, [@key; @key] citations (IEEE numbers by first use),
// {{placeholder}} (highlighted), and :: directives (cover, sp, pagebreak, toc,
// caption, widths, tablefont, sign, references, ref).
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow,
  TableCell, WidthType, ShadingType, BorderStyle, Header, PageNumber, TableOfContents,
  LevelFormat, PageBreak, ImageRun,
} = require("docx");

const SRC = path.join(__dirname, "DeCuong_NCS_LHU_2026-10_v6.md");
const OUT = path.join(__dirname, "DeCuong_NCS_LHU_2026-10_v6.docx");
const FONT = "Times New Roman";
const CM = 567;
const BODY_LINE = 312; // 1.3 line spacing

const lines = fs.readFileSync(SRC, "utf8").split(/\r?\n/);

// ---- references: definitions, numbering by first citation -----------------
const refText = new Map();
for (const l of lines) {
  const m = l.match(/^::ref (\S+) \| (.+)$/);
  if (m) {
    if (refText.has(m[1])) throw new Error(`duplicate ref ${m[1]}`);
    refText.set(m[1], m[2]);
  }
}
const refNum = new Map();
for (const l of lines) {
  if (l.startsWith("::ref ")) continue;
  for (const m of l.matchAll(/\[@([^\]]+)\]/g)) {
    for (const k of m[1].split(";").map((s) => s.trim().replace(/^@/, ""))) {
      if (!refText.has(k)) throw new Error(`cited key without ::ref: ${k}`);
      if (!refNum.has(k)) refNum.set(k, refNum.size + 1);
    }
  }
}
const uncited = [...refText.keys()].filter((k) => !refNum.has(k));
if (uncited.length) throw new Error(`refs never cited: ${uncited.join(", ")}`);

function citeLabel(inner) {
  const nums = [...new Set(inner.split(";").map((s) => refNum.get(s.trim().replace(/^@/, ""))))]
    .sort((a, b) => a - b);
  const parts = [];
  for (let i = 0; i < nums.length; ) {
    let j = i;
    while (j + 1 < nums.length && nums[j + 1] === nums[j] + 1) j++;
    if (j - i >= 2) parts.push(`[${nums[i]}]–[${nums[j]}]`);
    else for (let t = i; t <= j; t++) parts.push(`[${nums[t]}]`);
    i = j + 1;
  }
  return parts.join(", ");
}

// ---- inline markup ----------------------------------------------------------
function runs(text, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|\[@[^\]]+\]|\{\{[^}]+\}\})/g;
  let last = 0;
  for (const m of text.matchAll(re)) {
    if (m.index > last) out.push(new TextRun({ ...base, text: text.slice(last, m.index) }));
    const t = m[0];
    if (t.startsWith("**")) out.push(...runs(t.slice(2, -2), { ...base, bold: true }));
    else if (t.startsWith("[@")) out.push(new TextRun({ ...base, text: citeLabel(t.slice(2, -1)) }));
    else if (t.startsWith("{{")) out.push(new TextRun({ ...base, text: `[${t.slice(2, -2)}]`, highlight: "yellow" }));
    else out.push(new TextRun({ ...base, text: t.slice(1, -1), italics: !base.italics }));
    last = m.index + t.length;
  }
  if (last < text.length) out.push(new TextRun({ ...base, text: text.slice(last) }));
  return out;
}

const bodyPara = (text) =>
  new Paragraph({
    children: runs(text),
    alignment: AlignmentType.JUSTIFIED,
    indent: { firstLine: CM },
    spacing: { after: 120, line: BODY_LINE },
  });

// ---- tables -----------------------------------------------------------------
const border = { style: BorderStyle.SINGLE, size: 4, color: "000000" };
const borders = { top: border, bottom: border, left: border, right: border };

function makeTable(rows, widthsCm, fontPt) {
  const ncol = rows[0].length;
  const widths = widthsCm
    ? widthsCm.map((w) => Math.round(w * CM))
    : Array(ncol).fill(Math.floor((16 * CM) / ncol));
  const total = widths.reduce((a, b) => a + b, 0);
  const wide = ncol > 6;
  return new Table({
    width: { size: total, type: WidthType.DXA },
    columnWidths: widths,
    rows: rows.map((cells, ri) =>
      new TableRow({
        tableHeader: ri === 0,
        cantSplit: true,
        children: cells.map((c, ci) =>
          new TableCell({
            borders,
            width: { size: widths[ci], type: WidthType.DXA },
            shading: ri === 0 ? { fill: "D9D9D9", type: ShadingType.CLEAR, color: "auto" } : undefined,
            margins: { top: 40, bottom: 40, left: wide ? 40 : 90, right: wide ? 40 : 90 },
            children: [
              new Paragraph({
                alignment:
                  ri === 0 || (ci > 0 && (wide || c.length < 28)) ? AlignmentType.CENTER : AlignmentType.LEFT,
                spacing: { before: 0, after: 0, line: 260 },
                keepNext: ri < rows.length - 1,
                children: runs(c, { size: fontPt * 2, bold: ri === 0 ? true : undefined }),
              }),
            ],
          })
        ),
      })
    ),
  });
}

// ---- main pass --------------------------------------------------------------
const children = [];
let widths = null;
let tableFont = 12;
let mode = null; // "cover" | "sign"
let tableRows = null;

function flushTable() {
  if (!tableRows) return;
  children.push(makeTable(tableRows, widths, tableFont));
  children.push(new Paragraph({ spacing: { after: 60 }, children: [] }));
  tableRows = null;
  widths = null;
  tableFont = 12;
}

function styledLine(l) {
  const m = l.match(/^\[([a-z]+)(\d*)\] (.*)$/);
  if (!m) throw new Error(`bad cover/sign line: ${l}`);
  const [, flags, size, text] = m;
  const align = flags.includes("c") ? AlignmentType.CENTER : AlignmentType.LEFT;
  const indent = flags.includes("r") ? { left: 6.5 * CM } : flags.includes("l") ? { left: 2 * CM } : undefined;
  return new Paragraph({
    alignment: flags.includes("r") ? AlignmentType.CENTER : align,
    indent,
    spacing: { after: 60, line: BODY_LINE },
    children: runs(text, {
      size: (Number(size) || 13) * 2,
      bold: flags.includes("b") || undefined,
      italics: flags.includes("i") || undefined,
    }),
  });
}

for (const raw of lines) {
  const l = raw.replace(/\s+$/, "");
  if (l.startsWith("|")) {
    const cells = l.slice(1, -1).split("|").map((s) => s.trim());
    if (cells.every((c) => /^-+$/.test(c))) continue;
    (tableRows ||= []).push(cells);
    continue;
  }
  flushTable();
  if (l === "::cover" || l === "::sign") { mode = l.slice(2); continue; }
  if (l === "::endcover" || l === "::endsign") { mode = null; continue; }
  if (l.startsWith("::sp ")) {
    children.push(new Paragraph({ spacing: { before: Number(l.slice(5)), after: 0 }, children: [] }));
    continue;
  }
  if (mode && l) { children.push(styledLine(l)); continue; }
  if (!l || l.startsWith("::ref ")) continue;
  if (l === "::pagebreak") { children.push(new Paragraph({ children: [new PageBreak()] })); continue; }
  if (l.startsWith("::tochead ")) {
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, pageBreakBefore: true, spacing: { after: 200 },
      children: [new TextRun({ text: l.slice(10), bold: true, size: 28 })] }));
    continue;
  }
  if (l === "::toc") {
    children.push(new TableOfContents("Mục lục", { hyperlink: true, headingStyleRange: "1-2" }));
    continue;
  }
  if (l.startsWith("::widths ")) { widths = l.slice(9).split(",").map(Number); continue; }
  if (l.startsWith("::tablefont ")) { tableFont = Number(l.slice(12)); continue; }
  if (l.startsWith("::caption ")) {
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true,
      spacing: { before: 120, after: 80, line: 276 }, children: runs(l.slice(10), { bold: true, size: 24 }) }));
    continue;
  }
  if (l === "::references") {
    [...refNum.entries()].sort((a, b) => a[1] - b[1]).forEach(([k, n]) =>
      children.push(new Paragraph({
        alignment: AlignmentType.JUSTIFIED,
        indent: { left: 680, hanging: 680 },
        spacing: { after: 40, line: 240 },
        children: runs(`[${n}]\t${refText.get(k)}`, { size: 24 }),
        tabStops: [{ type: "left", position: 680 }],
      }))
    );
    continue;
  }
  if (l.startsWith("::image ")) {
    const [file, wcm, caption] = l.slice(8).split("|").map((x) => x.trim());
    const buf = fs.readFileSync(path.join(path.dirname(SRC), file));
    const svgPath = path.join(path.dirname(SRC), file.replace(/\.png$/, ".svg"));
    const w = Math.round(Number(wcm) * 37.8); // cm -> px at 96 dpi
    const h = Math.round(w * buf.readUInt32BE(20) / buf.readUInt32BE(16)); // PNG IHDR height/width
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 120, after: 60 },
      children: [new ImageRun(fs.existsSync(svgPath)
        // Same-name SVG: Word keeps it as vectors in the PDF (a PNG gets downsampled); PNG is the fallback.
        ? { type: "svg", data: fs.readFileSync(svgPath), fallback: { type: "png", data: buf }, transformation: { width: w, height: h } }
        : { type: "png", data: buf, transformation: { width: w, height: h } })] }));
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160, line: BODY_LINE },
      children: runs(caption, { italics: true, size: 24 }) }));
    continue;
  }
  if (l.startsWith("::")) throw new Error(`unknown directive: ${l}`);
  const h = l.match(/^(#{1,3}) (.*)$/);
  if (h) {
    const level = [HeadingLevel.HEADING_1, HeadingLevel.HEADING_2, HeadingLevel.HEADING_3][h[1].length - 1];
    children.push(new Paragraph({ heading: level, children: runs(h[2]) }));
    continue;
  }
  const b = l.match(/^( *)- (.*)$/);
  if (b) {
    children.push(new Paragraph({
      numbering: { reference: "dash", level: b[1].length >= 2 ? 1 : 0 },
      alignment: AlignmentType.JUSTIFIED,
      spacing: { after: 120, line: BODY_LINE },
      children: runs(b[2]),
    }));
    continue;
  }
  children.push(bodyPara(l));
}
flushTable();

const heading = (id, name, level, extra = {}) => ({
  id, name, basedOn: "Normal", next: "Normal", quickFormat: true,
  run: { font: FONT, size: 26, bold: true, color: "000000", ...extra },
  paragraph: { keepNext: true, keepLines: true, outlineLevel: level,
    spacing: { before: level === 0 ? 240 : 160, after: 100, line: BODY_LINE } },
});

const doc = new Document({
  creator: "Nguyễn Lê Minh Hòa",
  title: "Bài luận dự định nghiên cứu dự tuyển tiến sĩ",
  styles: {
    default: { document: { run: { font: FONT, size: 26 }, paragraph: { spacing: { line: BODY_LINE } } } },
    paragraphStyles: [
      heading("Heading1", "Heading 1", 0),
      heading("Heading2", "Heading 2", 1),
      heading("Heading3", "Heading 3", 2, { italics: true }),
      { id: "TOC1", name: "toc 1", basedOn: "Normal", next: "Normal",
        paragraph: { spacing: { before: 40, after: 0, line: 240 } }, run: { font: FONT, bold: true } },
      { id: "TOC2", name: "toc 2", basedOn: "Normal", next: "Normal",
        paragraph: { spacing: { before: 0, after: 0, line: 240 }, indent: { left: 400 } }, run: { font: FONT } },
    ],
  },
  numbering: {
    config: [{
      reference: "dash",
      levels: [
        { level: 0, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 900, hanging: 333 } }, run: { font: FONT } } },
        { level: 1, format: LevelFormat.BULLET, text: "+", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 1440, hanging: 360 } }, run: { font: FONT } } },
      ],
    }],
  },
  sections: [{
    properties: {
      titlePage: true,
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: 2 * CM, bottom: 2 * CM, left: 3 * CM, right: 2 * CM, header: CM },
      },
    },
    headers: {
      first: new Header({ children: [new Paragraph({ children: [] })] }),
      default: new Header({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
        children: [new TextRun({ children: [PageNumber.CURRENT], size: 26 })] })] }),
    },
    children,
  }],
});

// Word downsamples pictures to its default ppi on PDF export unless the document opts out.
const JSZip = require("jszip");
Packer.toBuffer(doc).then(async (raw) => {
  const zip = await JSZip.loadAsync(raw);
  const settings = await zip.file("word/settings.xml").async("string");
  zip.file("word/settings.xml", settings.replace("</w:settings>", "<w:doNotAutoCompressPictures/></w:settings>"));
  const buf = await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" });
  fs.writeFileSync(OUT, buf);
  console.log(`wrote ${OUT}: ${refNum.size} references`);
});
