Image optimization scripts

Two options are provided to generate optimized images (WebP + AVIF) and resized variants in `assets/images/optimized`.

1) Node.js (recommended)

Install dependencies and run:

```bash
npm init -y
npm install sharp glob
node scripts/optimize-images.js
```

This will create resized `.webp` and `.avif` files for multiple widths.

2) PowerShell + ImageMagick fallback

Run (Windows PowerShell):

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\optimize-with-imagemagick.ps1
```

This requires `magick` (ImageMagick) in PATH and supports the same output folder.

After generating optimized assets, update your HTML `srcset`/`picture` markup to prefer AVIF/WebP with fallbacks.
