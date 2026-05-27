#!/usr/bin/env python3
"""Fix logo image paths in blog HTML files.
Replaces occurrences of './assets/images/' and "./assets/images/" with '/assets/images/'
Creates a .bak backup for each changed file.
"""
import glob
from pathlib import Path

root = Path(__file__).resolve().parent.parent
changed = []
files = sorted(root.glob('blog-*/*.html'))
for f in files:
    text = f.read_text(encoding='utf-8')
    new = text.replace("./assets/images/", "/assets/images/")
    new = new.replace("'./assets/images/", "'/assets/images/")
    new = new.replace('"./assets/images/', '"/assets/images/')
    # Also fix srcset that might start with ./assets without images/ (defensive)
    new = new.replace("./assets/", "/assets/")
    new = new.replace("'./assets/", "'/assets/")
    new = new.replace('"./assets/', '"/assets/')
    if new != text:
        bak = f.with_suffix(f.suffix + '.bak')
        if not bak.exists():
            bak.write_text(text, encoding='utf-8')
        f.write_text(new, encoding='utf-8')
        changed.append(f.relative_to(root))

print(f"Processed {len(files)} files, updated {len(changed)} files.")
for p in changed:
    print(p)
