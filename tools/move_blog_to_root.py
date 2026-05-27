#!/usr/bin/env python3
from pathlib import Path
import shutil
import re

ROOT = Path(__file__).resolve().parents[1]
BLOG_PARENT = ROOT / 'pages' / 'blog'

# Move blog-N folders to repo root
moved = []
for p in sorted(BLOG_PARENT.iterdir()):
    if p.is_dir() and p.name.startswith('blog-'):
        dest = ROOT / p.name
        if dest.exists():
            print(f'Skipping {p.name}: {dest} already exists')
            continue
        shutil.move(str(p), str(dest))
        moved.append(p.name)
        print('Moved', p.name, '->', dest)

# Fix links in HTML and XML files
files = list(ROOT.rglob('*.html')) + list(ROOT.rglob('*.xml'))
re_pages_blog = re.compile(r'pages/blog/blog-(\d+)/')
re_blog_blog = re.compile(r'blog/blog-(\d+)/')
changes = []
for f in files:
    # skip files that are inside old blog parent (should be empty now)
    try:
        rel = f.relative_to(ROOT)
    except Exception:
        continue
    s = f.read_text(encoding='utf-8')
    s2 = s
    # Normalize any pages/blog/blog-N/ -> blog-N/
    s2 = re_pages_blog.sub(r'blog-\1/', s2)
    # If file is inside pages/, links to blog/blog-N should be ../blog-N/
    if rel.parts[0] == 'pages':
        s2 = re_blog_blog.sub(r'../blog-\1/', s2)
    else:
        s2 = re_blog_blog.sub(r'blog-\1/', s2)
    if s2 != s:
        f.write_text(s2, encoding='utf-8')
        changes.append(str(rel))

print('Moved folders:', moved)
print('Updated files count:', len(changes))
for c in changes:
    print(' -', c)
print('Done')
