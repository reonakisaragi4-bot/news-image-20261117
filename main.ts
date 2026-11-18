// news-image-20261117: copy the entry image to the output directory.
// Node 22, standard library only. The image is the poster drawn by
// draw_poster.py (a one-image summary of Tuesday 17 November 2026 news).
// The copy is byte-for-byte, so repeated runs produce identical output.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
if (!existsSync("entry.png")) {
  throw new Error("entry.png not found beside main.ts");
}
mkdirSync(outDir, { recursive: true });
copyFileSync("entry.png", join(outDir, "entry.png"));
console.log("wrote", join(outDir, "entry.png"));
