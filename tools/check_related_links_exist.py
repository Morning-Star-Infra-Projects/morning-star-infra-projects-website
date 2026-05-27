#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup

root = Path(__file__).resolve().parent.parent
blog_files = sorted(root.glob('blog-*/*.html'))
missing = []
for f in blog_files:
    text = f.read_text(encoding='utf-8')
    soup = BeautifulSoup(text, 'html.parser')
    for div in soup.select('div.related-posts'):
        for a in div.find_all('a', href=True):
            href = a['href'].strip()
            if href.startswith(('http://','https://','#')):
                continue
            if href.startswith('/'):
                target = root / href.lstrip('/')
            else:
                target = (f.parent / href).resolve()
            if not target.exists():
                missing.append((f.relative_to(root).as_posix(), href))

print(f"Checked {len(blog_files)} files, found {len(missing)} broken related links.")
for f, href in missing[:200]:
    print(f, '->', href)
