#!/usr/bin/env python3
"""Fix Related Posts links in blog HTML files.
- For anchors inside div.related-posts, if href is a bare filename (no leading /, ./, ../, http, or #), locate the file in the workspace and replace href with absolute path '/<found_relative_path>'.
- Creates .bak backups for modified files.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import sys

root = Path(__file__).resolve().parent.parent
blog_files = sorted(root.glob('blog-*/*.html'))
all_html = {p.name: p for p in root.rglob('**/*.html')}
updated = []

for f in blog_files:
    text = f.read_text(encoding='utf-8')
    soup = BeautifulSoup(text, 'html.parser')
    changed = False
    for div in soup.select('div.related-posts'):
        for a in div.find_all('a', href=True):
            href = a['href'].strip()
            if href.startswith(('/', './', '../', '#')) or href.startswith('http'):
                continue
            # href is a bare filename; try to find it in workspace
            target = all_html.get(href)
            if not target:
                # try matching by basename if href contains query? strip params
                basename = href.split('?')[0].split('#')[0]
                target = all_html.get(basename)
            if target:
                # compute workspace-relative path
                rel = target.relative_to(root).as_posix()
                new_href = '/' + rel
                if a['href'] != new_href:
                    a['href'] = new_href
                    changed = True
            else:
                # attempt fuzzy search
                matches = list(root.rglob(href))
                if not matches:
                    matches = list(root.rglob('*' + href))
                if matches:
                    target = matches[0]
                    rel = target.relative_to(root).as_posix()
                    new_href = '/' + rel
                    a['href'] = new_href
                    changed = True
    if changed:
        bak = f.with_suffix(f.suffix + '.bak')
        if not bak.exists():
            bak.write_text(text, encoding='utf-8')
        f.write_text(str(soup), encoding='utf-8')
        updated.append(f.relative_to(root))

print(f"Processed {len(blog_files)} blog files, updated {len(updated)} files.")
for p in updated:
    print(p)
