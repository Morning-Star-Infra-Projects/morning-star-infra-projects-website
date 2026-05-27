#!/usr/bin/env python3
"""Resolve and fix related-posts links in blog HTML files.
For anchors inside div.related-posts:
- If href is external or starts with #, skip.
- Try resolving href relative to the blog file. If the file exists, replace href with absolute '/<relpath>'.
- Else, search the workspace for the basename; if found, replace with absolute '/<relpath>'.
- Create .bak backups for changed files.
"""
from pathlib import Path
from bs4 import BeautifulSoup

root = Path(__file__).resolve().parent.parent
blog_files = sorted(root.glob('blog-*/*.html'))
all_html = {p.relative_to(root).as_posix(): p for p in root.rglob('**/*.html')}
name_index = {}
for rel, p in all_html.items():
    name_index.setdefault(p.name, []).append(p)

updated = []
for f in blog_files:
    text = f.read_text(encoding='utf-8')
    soup = BeautifulSoup(text, 'html.parser')
    changed = False
    for div in soup.select('div.related-posts'):
        for a in div.find_all('a', href=True):
            href = a['href'].strip()
            if href.startswith(('http://','https://','#')):
                continue
            # Try resolve relative to file
            candidate = (f.parent / href).resolve() if href else None
            if candidate and candidate.exists() and candidate.suffix=='.html':
                rel = candidate.relative_to(root).as_posix()
                new_href = '/' + rel
                if a['href'] != new_href:
                    a['href'] = new_href
                    changed = True
                continue
            # If href starts with '/', check if file exists as-is
            if href.startswith('/'):
                try:
                    p = (root / href.lstrip('/')).resolve()
                    if p.exists():
                        continue
                except Exception:
                    pass
            # Try by basename lookup (strip any ./ or ../)
            from pathlib import PurePosixPath
            basename = PurePosixPath(href.split('?')[0].split('#')[0]).name
            matches = name_index.get(basename, [])
            if matches:
                target = matches[0]
                rel = target.relative_to(root).as_posix()
                new_href = '/' + rel
                if a['href'] != new_href:
                    a['href'] = new_href
                    changed = True
                continue
            # Fuzzy search: any file that endswith basename
            found = None
            for relpath, p in all_html.items():
                if relpath.endswith('/' + basename) or relpath==basename:
                    found = p
                    break
            if found:
                rel = found.relative_to(root).as_posix()
                new_href = '/' + rel
                if a['href'] != new_href:
                    a['href'] = new_href
                    changed = True
                continue
            # As a last resort, map common section names to /pages/
            mapping = {
                'home-construction.html':'/pages/home-construction.html',
                'commercial-and-industrial.html':'/pages/commercial-and-industrial.html',
                'interior-fitouts.html':'/pages/interior-fitouts.html',
                'structural-repair.html':'/pages/structural-repair.html',
                'contact.html':'/pages/contact.html',
                'blog.html':'/pages/blog.html'
            }
            key = basename.lower()
            if key in mapping:
                if a['href'] != mapping[key]:
                    a['href'] = mapping[key]
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
