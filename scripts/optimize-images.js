const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const glob = require('glob');

// Config: adjust sizes and quality as needed
const SIZES = [1600, 1200, 800, 400];
const WEBP_QUALITY = 80;
const AVIF_QUALITY = 50;

const SRC_DIR = path.join(__dirname, '..', 'assets', 'images');
const OUT_DIR = path.join(__dirname, '..', 'assets', 'images', 'optimized');

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

async function processFile(file) {
  const rel = path.relative(SRC_DIR, file);
  const parsed = path.parse(rel);
  const destFolder = path.join(OUT_DIR, parsed.dir);
  ensureDir(destFolder);

  for (const w of SIZES) {
    const outBase = path.join(destFolder, `${parsed.name}-${w}`);
    try {
      await sharp(file)
        .resize({ width: w, withoutEnlargement: true })
        .toFile(outBase + '.jpg');
    } catch (e) {
      // ignore jpg fallback errors
    }
    await sharp(file)
      .resize({ width: w, withoutEnlargement: true })
      .webp({ quality: WEBP_QUALITY })
      .toFile(outBase + '.webp');

    await sharp(file)
      .resize({ width: w, withoutEnlargement: true })
      .avif({ quality: AVIF_QUALITY })
      .toFile(outBase + '.avif');
  }
}

async function main() {
  ensureDir(OUT_DIR);
  const patterns = [
    path.join(SRC_DIR, '**', '*.png'),
    path.join(SRC_DIR, '**', '*.jpg'),
    path.join(SRC_DIR, '**', '*.jpeg'),
    path.join(SRC_DIR, '**', '*.webp'),
    path.join(SRC_DIR, '**', '*.gif')
  ];

  const files = patterns.flatMap(p => glob.sync(p, { nodir: true }));
  console.log(`Found ${files.length} images.`);

  for (const f of files) {
    console.log('Processing', f);
    try { await processFile(f); } catch (e) { console.error('Error', f, e.message); }
  }
  console.log('Done. Optimized images are in assets/images/optimized');
}

main().catch(err => { console.error(err); process.exit(1); });
