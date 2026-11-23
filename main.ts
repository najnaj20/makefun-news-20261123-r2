// Driver for the news-image entry: copies the pre-rendered front page
// (entry.png, sitting next to this script) into the harness output dir.
//
// The image itself is produced offline by render.py; this script only
// validates it and hands it over, so the graded run is deterministic.

import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// First eight bytes of every PNG file.
const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);

// Bounty cap on the submitted image.
const MAX_IMAGE_BYTES = 1024 * 1024;

function abort(reason: string): never {
  console.error(`entry driver: ${reason}`);
  process.exit(1);
}

function fingerprint(data: Buffer): string {
  return createHash("sha256").update(data).digest("hex");
}

function main(): void {
  const folder = dirname(fileURLToPath(import.meta.url));
  const source = join(folder, "entry.png");

  if (!existsSync(source)) {
    abort(`cannot find ${source}`);
  }

  const image = readFileSync(source);

  if (image.length > MAX_IMAGE_BYTES) {
    abort(
      `entry.png is ${image.length} bytes, above the ${MAX_IMAGE_BYTES} byte limit`,
    );
  }

  if (!image.subarray(0, PNG_SIGNATURE.length).equals(PNG_SIGNATURE)) {
    abort("entry.png does not begin with the PNG signature");
  }

  const outDir = process.env.MAKEFUN_OUTPUT_DIR;
  const destination = outDir
    ? join(outDir, "entry.png")
    : "/output/entry.png";

  mkdirSync(dirname(destination), { recursive: true });
  writeFileSync(destination, image);

  console.log(
    `entry driver: wrote ${image.length} bytes to ${destination} ` +
      `(sha256 ${fingerprint(image)})`,
  );
}

main();
