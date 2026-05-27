#!/usr/bin/env python3
from pathlib import Path
import shutil
import re

ROOT = Path(__file__).resolve().parents[1]
BLOG_DIR = ROOT / 'pages' / 'blog'

# Find part folders
parts = sorted([p for p in BLOG_DIR.iterdir() if p.is_dir() and p.name.startswith('part-')])
if not parts:
    print('No part-* folders found; nothing to rename')
    raise SystemExit(0)

renames = []
for p in parts:
    num = p.name.split('-',1)[1]
    new_name = f'blog-{num}'
    new_path = BLOG_DIR / new_name
    if new_path.exists():
        print(f'Skipping {p} because {new_path} already exists')
        continue
    shutil.move(str(p), str(new_path))
    renames.append((p.name, new_name))
    print(f'Renamed {p.name} -> {new_name}')

# Update hrefs in pages/*.html and other files referencing blog/part-
href_re = re.compile(r'href=("|\')blog/(part-(\d+)/(?:[^"\']+\.html))("|\')')
updated_files = []
for f in ROOT.rglob('*.html'):
    # skip inside blog folders themselves
    if str(f).startswith(str(BLOG_DIR)):
        continue
    s = f.read_text(encoding='utf-8')
    if 'href="blog/part-' not in s and "href='blog/part-" not in s:
        continue
    def repl(m):
        quote = m.group(1)
        whole = m.group(2)  # part-#/slug.html
        part = m.group(3)
        new = f'blog/blog-{part}/{whole.split('/',1)[1]}'
        return f'href={quote}{new}{quote}'
    s2 = href_re.sub(repl, s)
    if s2 != s:
        f.write_text(s2, encoding='utf-8')
        updated_files.append(str(f.relative_to(ROOT)))

print('Updated links in', len(updated_files), 'files')
for u in updated_files:
    print(' -', u)

print('Done')
