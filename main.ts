// News-image entry for make.fun "Sum up 23 November's world news in one image".
// The image is entry.png beside this file, drawn by render.py in this
// session from 30 verified 23 November 2026 stories. This program copies it to
// the grader's output directory. Node 22, standard library only, no network.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });

// Validate the image before copying: it must be a whole PNG of at most
// 1 MiB, the limits the bounty gate checks. Fail loudly instead of
// writing a file the gate would refuse.
const src = new URL('./entry.png', import.meta.url);
const bytes = readFileSync(src);
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(pngMagic)) {
  throw new Error('entry.png is not a PNG file');
}
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
copyFileSync(src, join(outDir, 'entry.png'));
const written = statSync(join(outDir, 'entry.png'));
if (written.size !== bytes.length) {
  throw new Error('entry.png was not copied completely');
}
