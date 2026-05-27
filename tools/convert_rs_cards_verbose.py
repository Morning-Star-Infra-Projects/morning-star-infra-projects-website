#!/usr/bin/env python3
import re
import glob
from pathlib import Path

root = Path(__file__).resolve().parents[1]
pattern = root / 'pages' / '*.html'
files = list(glob.glob(str(pattern)))
changed = []
rs_re = re.compile(r'<a\s+href="(?P<href>[^"]+)"\s+class="rs-card">(?P<body>.*?)<span class="rs-link">(?P<label>.*?)</span>\s*</a>', re.S)
for fp in files:
    p = Path(fp)
    s = p.read_text(encoding='utf-8')
    if 'rs-card' not in s:
        continue
    def repl(m):
        href = m.group('href')
        body = m.group('body')
        label = m.group('label')
        body = body.rstrip()
        return f'<div class="rs-card">{body}\n        <a class="rs-btn" href="{href}">{label}</a>\n      </div>'
    s2 = rs_re.sub(repl, s)
    if s2 != s:
        p.write_text(s2, encoding='utf-8')
        changed.append(fp)
for c in changed:
    print(c)
print('Modified:', len(changed))
