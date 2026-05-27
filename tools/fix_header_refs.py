#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
html_files = list(ROOT.rglob('*.html'))
changed = []

for p in html_files:
    if p.name.endswith('.bak'):
        continue
    s = p.read_text(encoding='utf-8')
    orig = s
    # Replace any Morning-Star-Infra-Projects-Header-Logo*.webp -> .jpeg
    s = re.sub(r'Morning-Star-Infra-Projects-Header-Logo(\-\d+)?\.webp', 'Morning-Star-Infra-Projects-Header-Logo.jpeg', s)
    # Also replace possible logos/ path variant
    s = re.sub(r'logos/Morning-Star-Infra-Projects-Header-Logo\.webp', 'Morning-Star-Infra-Projects-Header-Logo.jpeg', s)

    if s != orig:
        bak = p.with_suffix(p.suffix + '.bak')
        if not bak.exists():
            bak.write_text(orig, encoding='utf-8')
        p.write_text(s, encoding='utf-8')
        changed.append(str(p.relative_to(ROOT)))

if changed:
    print('Updated header refs in:')
    for c in changed:
        print('-', c)
else:
    print('No header ref changes needed.')
