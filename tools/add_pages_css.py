#!/usr/bin/env python3
import glob
from pathlib import Path

root = Path(__file__).resolve().parents[1]
pattern = root / 'pages' / 'blog' / '*.html'
files = list(glob.glob(str(pattern)))
modified = 0
for fp in files:
    p = Path(fp)
    s = p.read_text(encoding='utf-8')
    # For blog article pages, components.css should be linked; insert pages.css after it if missing
    if 'assets/css/pages.css' in s:
        continue
    s2 = s.replace('<link rel="stylesheet" href="../../assets/css/components.css">',
                   '<link rel="stylesheet" href="../../assets/css/components.css">\n  <link rel="stylesheet" href="../../assets/css/pages.css">')
    if s2 != s:
        p.write_text(s2, encoding='utf-8')
        modified += 1
# Update blog index
blog_index = root / 'pages' / 'blog.html'
if blog_index.exists():
    s = blog_index.read_text(encoding='utf-8')
    if 'assets/css/pages.css' not in s:
        s = s.replace('<link rel="stylesheet" href="../assets/css/components.css">',
                      '<link rel="stylesheet" href="../assets/css/components.css">\n<link rel="stylesheet" href="../assets/css/pages.css">')
        blog_index.write_text(s, encoding='utf-8')
        modified += 1

print(f"Inserted pages.css into {modified} files")
