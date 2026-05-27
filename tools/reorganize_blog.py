#!/usr/bin/env python3
import math
from pathlib import Path
import shutil
import re

ROOT = Path(__file__).resolve().parents[1]
BLOG_DIR = ROOT / 'pages' / 'blog'
INDEX = ROOT / 'pages' / 'blog.html'
PAGES_DIR = ROOT / 'pages'
CHUNK = 100

html_files = sorted([p for p in BLOG_DIR.glob('*.html')])
if not html_files:
    print('No blog files found in', BLOG_DIR)
    raise SystemExit(0)

chunks = [html_files[i:i+CHUNK] for i in range(0, len(html_files), CHUNK)]
print(f'Found {len(html_files)} blog pages; will create {len(chunks)} folder(s)')

# Move files into part-N folders
for idx, chunk in enumerate(chunks, start=1):
    part = BLOG_DIR / f'part-{idx}'
    part.mkdir(exist_ok=True)
    for p in chunk:
        dest = part / p.name
        shutil.move(str(p), str(dest))
print('Moved files into part folders')

# Update hrefs in pages/blog.html (index) and any other pages under pages/ that link to blog/slug.html
href_re = re.compile(r'href=("|\')blog/([^"\']+\.html)("|\')')
# Helper: find which part a filename now resides in
def find_part(filename):
    for idx in range(1, len(chunks)+1):
        candidate = BLOG_DIR / f'part-{idx}' / filename
        if candidate.exists():
            return f'part-{idx}'
    return None

updated_files = []
for page in PAGES_DIR.glob('*.html'):
    s = page.read_text(encoding='utf-8')
    if 'href="blog/' not in s and "href='blog/" not in s:
        continue
    def repl(m):
        quote = m.group(1)
        fname = m.group(2)
        part = find_part(fname)
        if not part:
            return m.group(0)
        return f'href={quote}blog/{part}/{fname}{quote}'
    s2 = href_re.sub(repl, s)
    if s2 != s:
        page.write_text(s2, encoding='utf-8')
        updated_files.append(str(page.relative_to(ROOT)))

print('Updated links in pages:', len(updated_files))
for u in updated_files:
    print(' -', u)

# Update any other files in repo that contain href="pages/blog/..." or href="blog/..." inside other folders
# Search workspace for href="pages/blog/ or href="blog/ (but avoid assets)
for f in ROOT.rglob('*.html'):
    if str(f).startswith(str(BLOG_DIR)):
        continue
    s = f.read_text(encoding='utf-8')
    if 'href="pages/blog/' in s or "href='pages/blog/" in s:
        s2 = s.replace('href="pages/blog/', 'href="pages/blog/')
        # no-op but keep placeholder for future expansions

print('Done')
