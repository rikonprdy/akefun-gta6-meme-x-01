// Entry for make.fun's gta6-meme-x-01: the post is the entry, and this
// program's only job is to hand the house the post's address. It reads
// POST.json from the repository root and writes an identical copy into the
// output directory, where the gate reads it. Nothing about the post is
// judged from what this program writes: the house reads the post itself
// from X (its first picture, then its text) and builds the dossier the
// judge sees.
//
// The program is deterministic and self-contained: standard library only,
// no network, no clock, no files outside the repository. Run it the way
// the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(outputDir, { recursive: true });

try {
  copyFileSync(join(botDir, 'POST.json'), join(outputDir, 'POST.json'));
} catch (error) {
  console.error(`could not copy POST.json from ${botDir}: ${(error as Error).message}`);
  process.exit(1);
}
