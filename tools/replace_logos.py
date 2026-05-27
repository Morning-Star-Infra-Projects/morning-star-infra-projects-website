#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

html_files = list(ROOT.rglob('*.html'))
changed = []

def replace_header(match):
    group = match.group(1) or ''
    return f"Morning-Star-Infra-Projects-Header-Logo{group}.webp"

def replace_footer(match):
    group = match.group(1) or ''
    return f"Morning-Star-Infra-Projects-Footer-Logo{group}.webp"

for p in html_files:
    if p.name.endswith('.bak'):
        continue
    s = p.read_text(encoding='utf-8')
    orig = s
    # header logo variants (morning-star-logo, morning-star-logo-72, -144, etc.)
    s = re.sub(r'morning-star-logo(\-\d+)?\.webp', replace_header, s)
    # footer logo variants
    s = re.sub(r'footer-logo(\-\d+)?\.webp', replace_footer, s)

    if s != orig:
        bak = p.with_suffix(p.suffix + '.bak')
        if not bak.exists():
            bak.write_text(orig, encoding='utf-8')
        p.write_text(s, encoding='utf-8')
        changed.append(str(p.relative_to(ROOT)))

if changed:
    print('Updated files:')
    for c in changed:
        print('-', c)
else:
    print('No replacements necessary.')
