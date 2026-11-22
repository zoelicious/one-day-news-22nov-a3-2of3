// Agent 3 entry for news-image-20261122, round 2: "Sunday 22 November 2026".
// The front page is rendered ahead of time by gen_image.py into the
// entry.png sitting next to this file. This program's only job is to
// hand that exact file to the grader.
//
// The output directory is taken verbatim from MAKEFUN_OUTPUT_DIR; it
// is never joined onto the repository path and never defaults to a
// relative "entry.png", because the grader runs node from a different
// working directory and a relative path would not resolve there.
// The source is located from import.meta.url, so this file works no
// matter where the process starts.
import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const entryUrl = new URL("./entry.png", import.meta.url);
const entryPath = entryUrl.pathname;
const destPath = join(outDir, "entry.png");

const bytes = statSync(entryPath).size;
if (bytes === 0 || bytes > 1048576) {
  throw new Error(`entry.png has unexpected size: ${bytes} bytes`);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(entryPath, destPath);
console.log(`entry.png (${bytes} bytes) -> ${destPath}`);
