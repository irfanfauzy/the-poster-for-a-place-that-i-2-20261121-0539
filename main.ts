// VELDRIA — The City That Sails at Dusk
// Entry program for the make.fun poster competition
// (the-poster-for-a-place-that-i-2-20261121-0539).
//
// The artwork: a 1024x1024 poster of Veldria, a harbour city that sails
// at dusk — lantern-lit ships, a violet-orange sky, and the skyline
// reflected in the water. It was rendered by draw_poster.py (Pillow,
// standard library only) and bundled as entry.png next to this script.
//
// This program's only job is to deliver that file, intact, into the
// grader's output folder: verify it is really a PNG, keep it under the
// size limit, copy it, and prove the copy is byte-identical by reading
// it back and comparing every byte. It makes no network calls and uses
// only the Node standard library, so it runs anywhere Node 22+ is
// installed, from any working directory.

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// PNG files always start with these eight magic bytes.
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

// Maximum allowed size of the bundled poster: 1 MiB.
const MAX_BYTES = 1_048_576;

const OUTPUT_FILE = "entry.png";

// The bundled poster lives next to this script, so resolve it from the
// script's own location rather than the working directory.
const scriptDir = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(scriptDir, OUTPUT_FILE);

// The grader tells us where to write via MAKEFUN_OUTPUT_DIR;
// fall back to /output when it is not set.
const outputDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const outputPath = join(outputDir, OUTPUT_FILE);

function fail(message: string): never {
  throw new Error(message);
}

// --- Verify the bundled file before copying ---------------------------

const stats = statSync(sourcePath);
if (stats.size > MAX_BYTES) {
  fail(
    `Bundled poster is ${stats.size} bytes, over the ${MAX_BYTES} byte limit.`,
  );
}

const source = readFileSync(sourcePath);
if (!source.subarray(0, PNG_MAGIC.length).equals(PNG_MAGIC)) {
  fail("Bundled entry.png is not a PNG (magic bytes do not match).");
}

// --- Copy it into the output folder ------------------------------------

mkdirSync(outputDir, { recursive: true });
copyFileSync(sourcePath, outputPath);

// --- Read the copy back and compare byte for byte ----------------------

const written = readFileSync(outputPath);
if (!written.equals(source)) {
  fail(`Output ${outputPath} does not match the bundled poster byte for byte.`);
}

console.log(
  `Wrote ${outputPath} (${written.length} bytes) — verified PNG, byte-identical to bundled ${OUTPUT_FILE}.`,
);
