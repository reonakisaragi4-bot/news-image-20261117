// news-image-20261117: copy the entry image to the output directory.
// Node 22, standard library only. The image is the poster drawn by
// draw_poster.py (a one-image summary of Tuesday 17 November 2026 news).
// The copy is byte-for-byte, so repeated runs produce identical output.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

// Resolve paths from this file's own directory, not the process working
// directory: the grader runs `node /bot/main.ts` from an arbitrary cwd,
// so a bare relative "entry.png" would not be found there.
const here = fileURLToPath(new URL(".", import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
if (!existsSync(src)) {
  throw new Error("entry.png not found beside main.ts");
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, "entry.png"));
console.log("wrote", join(outDir, "entry.png"));
