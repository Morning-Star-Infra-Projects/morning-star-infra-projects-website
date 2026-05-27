"""fix_viewport.py
Scan all HTML files and normalize the viewport meta tag to:
<meta name="viewport" content="width=device-width, initial-scale=1.0">

Usage: python tools/fix_viewport.py
"""
import re
from pathlib import Path

ROOT = Path('.').resolve()

pattern = re.compile(r'<meta\s+name=["\']viewport["\']\s+content=["\'].*?["\']\s*/?>', re.IGNORECASE)
replacement = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'

html_files = list(ROOT.rglob('*.html'))
changed = 0
for p in html_files:
    text = p.read_text(encoding='utf-8')
    if 'name="viewport"' in text or "name='viewport'" in text:
        new_text = pattern.sub(replacement, text)
        if new_text != text:
            p.write_text(new_text, encoding='utf-8')
            changed += 1
            print(f'Updated: {p}')

print(f'Done. Files changed: {changed}')
