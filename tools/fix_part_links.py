#!/usr/bin/env python3
from pathlib import Path
import re
ROOT=Path('.').resolve()
pattern = re.compile(r'(?P<q>href=)(?P<quote>["\'])(?:pages/)?blog/part-(?P<part>\d+)/(?!/)(?P<rest>[^"\']+)(?P=quote)')
changed=[]
for f in ROOT.rglob('*.html'):
    s=f.read_text(encoding='utf-8')
    new=s
    def repl(m):
        quote = m.group('quote')
        part = m.group('part')
        rest = m.group('rest')
        # if file inside pages folder, path from pages -> root is ../
        try:
            rel = f.relative_to(ROOT)
        except Exception:
            rel = f
        if 'pages' in rel.parts:
            return f'href={quote}../blog-{part}/{rest}{quote}'
        return f'href={quote}blog-{part}/{rest}{quote}'
    new = pattern.sub(repl, s)
    if new != s:
        f.write_text(new, encoding='utf-8')
        changed.append(str(f.relative_to(ROOT)))
print('Updated', len(changed), 'files')
for c in changed:
    print(' -', c)
