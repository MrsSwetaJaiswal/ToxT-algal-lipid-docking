// Convert SUPPLEMENTARY.md into SUPPLEMENTARY.docx.
// Generic-enough markdown -> docx renderer for this one file: headings,
// paragraphs (bold/italic/code inline), blockquotes, pipe tables, images
// (single or grouped side-by-side when consecutive), hr, numbered lists.
// Run: node build_supplementary_docx.js
const fs = require("fs");
const path = require("path");
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        ImageRun, AlignmentType, HeadingLevel, BorderStyle,
        WidthType, ShadingType, PageBreak } = require("docx");

const SRC = "SUPPLEMENTARY.md";
const OUT = "SUPPLEMENTARY.docx";
const CW = 9360; // content width, twips (US Letter, 1" margins)
const border = { style: BorderStyle.SINGLE, size: 1, color: "BBBBBB" };
const borders = { top: border, bottom: border, left: border, right: border };
const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

function pngSize(file) {
  const buf = fs.readFileSync(file);
  // PNG: 8-byte signature, then IHDR chunk with width/height as big-endian uint32 at offset 16/20
  const width = buf.readUInt32BE(16);
  const height = buf.readUInt32BE(20);
  return { width, height };
}

function scaledDims(file, maxWpx) {
  const { width, height } = pngSize(file);
  const w = Math.min(width, maxWpx);
  const h = Math.round(height * (w / width));
  return { w, h };
}

// ---- inline markdown (bold/italic/code) -> TextRun[] ----
function inline(text, baseOpts = {}) {
  const runs = [];
  // tokenize on **bold**, `code`, *italic* (non-nested, good enough here)
  const re = /(\*\*.+?\*\*|`.+?`|\*[^*]+?\*)/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) runs.push(new TextRun({ text: text.slice(last, m.index), ...baseOpts }));
    const tok = m[0];
    if (tok.startsWith("**")) {
      runs.push(new TextRun({ text: tok.slice(2, -2), bold: true, ...baseOpts }));
    } else if (tok.startsWith("`")) {
      runs.push(new TextRun({ text: tok.slice(1, -1), font: "Consolas", size: 19, ...baseOpts }));
    } else {
      runs.push(new TextRun({ text: tok.slice(1, -1), italics: true, ...baseOpts }));
    }
    last = re.lastIndex;
  }
  if (last < text.length) runs.push(new TextRun({ text: text.slice(last), ...baseOpts }));
  if (runs.length === 0) runs.push(new TextRun({ text: "", ...baseOpts }));
  return runs;
}

function P(text, opts = {}) {
  return new Paragraph({
    spacing: { after: opts.after ?? 120, line: 276 },
    alignment: opts.justify ? AlignmentType.JUSTIFIED : (opts.center ? AlignmentType.CENTER : undefined),
    indent: opts.indent ? { left: opts.indent } : undefined,
    children: inline(text, { italics: opts.italic, size: opts.size, color: opts.color }),
  });
}

function H(text, level) {
  return new Paragraph({ heading: level, pageBreakBefore: !!level && level === HeadingLevel.HEADING_1,
    children: inline(text) });
}

function cell(text, w, { head = false } = {}) {
  return new TableCell({
    borders, width: { size: w, type: WidthType.DXA },
    shading: head ? { fill: "1F4E79", type: ShadingType.CLEAR } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({ children: inline(String(text), { bold: head, color: head ? "FFFFFF" : undefined, size: 18 }) })],
  });
}

function mdTable(headerRow, rows) {
  const n = headerRow.length;
  const w = Math.floor(CW / n);
  const widths = new Array(n).fill(w);
  const trs = [new TableRow({ tableHeader: true, children: headerRow.map((t, i) => cell(t, widths[i], { head: true })) })];
  rows.forEach(r => trs.push(new TableRow({ children: r.map((t, i) => cell(t, widths[i])) })));
  return new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: widths, rows: trs });
}

function imageRow(files, maxTotalWpx = 540) {
  const n = files.length;
  const perW = Math.floor(maxTotalWpx / n);
  const cells = files.map(f => {
    const { w, h } = scaledDims(f, perW);
    return new TableCell({
      borders: noBorders, width: { size: Math.floor(CW / n), type: WidthType.DXA },
      margins: { top: 40, bottom: 40, left: 40, right: 40 },
      children: [new Paragraph({ alignment: AlignmentType.CENTER,
        children: [new ImageRun({ type: "png", data: fs.readFileSync(f),
          transformation: { width: w, height: h },
          altText: { title: path.basename(f), description: path.basename(f), name: path.basename(f) } })] })],
    });
  });
  return new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: cells.map(() => Math.floor(CW / n)), rows: [new TableRow({ children: cells })] });
}

// ---- markdown block parser ----
const lines = fs.readFileSync(SRC, "utf-8").split(/\r?\n/);
const kids = [];
let i = 0;

function isTableSep(l) { return /^\|?[\s:|-]+\|?$/.test(l) && l.includes("-"); }
function splitRow(l) {
  return l.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map(s => s.trim());
}

while (i < lines.length) {
  let line = lines[i];

  if (line.trim() === "") { i++; continue; }
  if (line.trim() === "---") { i++; continue; } // hr -- spacing handled by heading pageBreakBefore

  // headings
  let m;
  if ((m = /^# (.+)/.exec(line))) { kids.push(H(m[1], HeadingLevel.TITLE)); i++; continue; }
  if ((m = /^## (.+)/.exec(line))) { kids.push(H(m[1], HeadingLevel.HEADING_1)); i++; continue; }
  if ((m = /^### (.+)/.exec(line))) { kids.push(H(m[1], HeadingLevel.HEADING_2)); i++; continue; }

  // blockquote (collect consecutive > lines into one italic block)
  if (line.startsWith(">")) {
    const buf = [];
    while (i < lines.length && lines[i].startsWith(">")) {
      buf.push(lines[i].replace(/^>\s?/, ""));
      i++;
    }
    kids.push(P(buf.join(" "), { italic: true, indent: 360, color: "555555" }));
    continue;
  }

  // markdown table
  if (line.trim().startsWith("|") && i + 1 < lines.length && isTableSep(lines[i + 1])) {
    const header = splitRow(line);
    i += 2;
    const rows = [];
    while (i < lines.length && lines[i].trim().startsWith("|")) {
      rows.push(splitRow(lines[i]));
      i++;
    }
    kids.push(mdTable(header, rows));
    kids.push(P("", { after: 120 }));
    continue;
  }

  // image line(s) -- group consecutive image-only lines side by side
  if (/^!\[.*?\]\(.+?\)$/.test(line.trim())) {
    const files = [];
    while (i < lines.length && /^!\[.*?\]\(.+?\)$/.test(lines[i].trim())) {
      const mm = /^!\[.*?\]\((.+?)\)$/.exec(lines[i].trim());
      const f = mm[1];
      if (fs.existsSync(f)) files.push(f); else console.warn("missing image:", f);
      i++;
    }
    if (files.length) {
      // batch in groups of up to 3 per row
      for (let k = 0; k < files.length; k += 3) {
        kids.push(imageRow(files.slice(k, k + 3)));
      }
      kids.push(P("", { after: 160 }));
    }
    continue;
  }

  // numbered list item
  if ((m = /^(\d+)\. (.+)/.exec(line))) {
    kids.push(P(m[1] + ". " + m[2], { after: 80 }));
    i++;
    continue;
  }

  // plain paragraph (collect until blank line for word-wrap friendliness)
  {
    const buf = [line];
    i++;
    while (i < lines.length && lines[i].trim() !== "" && !/^#{1,3} /.test(lines[i]) &&
           lines[i].trim() !== "---" && !lines[i].trim().startsWith("|") &&
           !lines[i].startsWith(">") && !/^!\[.*?\]\(.+?\)$/.test(lines[i].trim()) &&
           !/^\d+\. /.test(lines[i])) {
      buf.push(lines[i]);
      i++;
    }
    kids.push(P(buf.join(" "), { justify: true }));
  }
}

const doc = new Document({
  sections: [{
    properties: { page: { margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    children: kids,
  }],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT, buf);
  console.log("Wrote", OUT, "(" + buf.length + " bytes)");
});
