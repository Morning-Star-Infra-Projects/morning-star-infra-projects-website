Image rename suggestions
========================

This helper scans `assets/images` and suggests SEO-friendly filenames in CSV format.

Usage:

```powershell
node scripts/generate-image-rename-suggestions.js > image-rename-suggestions.csv
```

Review the CSV, then apply renames carefully. Renaming files requires updating all references in your HTML/CSS/JS.

If you want, I can (a) run the suggestions and update references across the repo, or (b) produce a patch with renamed files and updated links — tell me which.
