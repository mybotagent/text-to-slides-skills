#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

function loadPptxGen() {
  try {
    return require("pptxgenjs");
  } catch (error) {
    if (process.env.NODE_PATH) {
      try {
        return require(path.join(process.env.NODE_PATH, "pptxgenjs"));
      } catch (_) {
        // Fall through to the actionable error below.
      }
    }
    console.error("Missing dependency: pptxgenjs. Set NODE_PATH to a node_modules directory containing pptxgenjs.");
    console.error(`Original error: ${error.message}`);
    process.exit(1);
  }
}

function parseArgs(argv) {
  const args = { deckJson: null, output: "deck.pptx", noTitle: false };
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--output" || arg === "-o") args.output = argv[++i];
    else if (arg === "--no-title-slide") args.noTitle = true;
    else if (!args.deckJson) args.deckJson = arg;
    else throw new Error(`Unknown argument: ${arg}`);
  }
  if (!args.deckJson) throw new Error("Usage: build_pptx.cjs deck.json --output deck.pptx");
  return args;
}

function palette(theme) {
  if (theme === "dark") {
    return { bg: "111827", fg: "F9FAFB", muted: "CBD5E1", accent: "E11D48", line: "334155" };
  }
  return { bg: "F8FAFC", fg: "111827", muted: "64748B", accent: "C0392B", line: "CBD5E1" };
}

function addFooter(slide, source, colors) {
  if (!source) return;
  slide.addText(source, {
    x: 0.55,
    y: 7.08,
    w: 11.8,
    h: 0.18,
    fontFace: "Aptos",
    fontSize: 8,
    color: colors.muted,
    margin: 0,
    fit: "shrink",
  });
}

function addTitleSlide(pptx, deck, colors) {
  const slide = pptx.addSlide();
  slide.background = { color: colors.bg };
  slide.addShape(pptx.ShapeType.line, { x: 0.65, y: 1.1, w: 1.0, h: 0, line: { color: colors.accent, width: 3 } });
  slide.addText(deck.title || "Untitled Deck", {
    x: 0.65,
    y: 1.45,
    w: 11.5,
    h: 1.2,
    fontFace: "Aptos Display",
    fontSize: 34,
    bold: true,
    color: colors.fg,
    fit: "shrink",
    margin: 0,
  });
  if (deck.subtitle) {
    slide.addText(deck.subtitle, {
      x: 0.67,
      y: 2.75,
      w: 10.5,
      h: 0.5,
      fontFace: "Aptos",
      fontSize: 18,
      color: colors.muted,
      margin: 0,
      fit: "shrink",
    });
  }
  addFooter(slide, deck.source, colors);
}

function addContentSlide(pptx, slideData, deck, colors, number) {
  const slide = pptx.addSlide();
  slide.background = { color: colors.bg };
  slide.addText(String(slideData.section || "").toUpperCase(), {
    x: 0.62,
    y: 0.35,
    w: 7.0,
    h: 0.22,
    fontFace: "Aptos",
    fontSize: 8,
    bold: true,
    color: colors.accent,
    charSpace: 0.6,
    margin: 0,
    fit: "shrink",
  });
  slide.addText(slideData.title || "", {
    x: 0.6,
    y: 0.72,
    w: 11.8,
    h: 0.95,
    fontFace: "Aptos Display",
    fontSize: 28,
    bold: true,
    color: colors.fg,
    fit: "shrink",
    margin: 0,
  });
  slide.addShape(pptx.ShapeType.line, { x: 0.6, y: 1.82, w: 12.0, h: 0, line: { color: colors.line, width: 0.75 } });

  const bullets = (slideData.bullets || []).slice(0, 6);
  const runs = bullets.map((bullet) => ({
    text: String(bullet),
    options: { bullet: { type: "ul" }, breakLine: true },
  }));
  if (runs.length) {
    slide.addText(runs, {
      x: 0.92,
      y: 2.18,
      w: 11.0,
      h: 4.45,
      fontFace: "Aptos",
      fontSize: bullets.length > 4 ? 18 : 21,
      color: colors.fg,
      paraSpaceAfterPt: 8,
      fit: "shrink",
      valign: "top",
      margin: 0.04,
    });
  }

  slide.addText(String(number).padStart(2, "0"), {
    x: 12.15,
    y: 6.95,
    w: 0.5,
    h: 0.2,
    fontFace: "Aptos",
    fontSize: 8,
    color: colors.muted,
    align: "right",
    margin: 0,
  });
  addFooter(slide, deck.source, colors);
  if (slideData.notes) slide.addNotes(String(slideData.notes));
}

async function main() {
  const args = parseArgs(process.argv);
  const pptxgen = loadPptxGen();
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_WIDE";
  pptx.author = "Codex";
  pptx.subject = "Text to PPT";
  pptx.company = "OpenAI";
  pptx.lang = "ko-KR";
  pptx.theme = { headFontFace: "Aptos Display", bodyFontFace: "Aptos", lang: "ko-KR" };

  const deck = JSON.parse(fs.readFileSync(path.resolve(args.deckJson), "utf8"));
  const colors = palette(deck.theme);
  if (!args.noTitle) addTitleSlide(pptx, deck, colors);
  (deck.slides || []).forEach((slide, index) => addContentSlide(pptx, slide, deck, colors, index + 1));

  fs.mkdirSync(path.dirname(path.resolve(args.output)), { recursive: true });
  await pptx.writeFile({ fileName: args.output });
  console.log(`Wrote ${args.output} with ${pptx._slides.length} slides`);
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
