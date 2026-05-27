"""auto_fix_site.py
Performs automated fixes across HTML files:
- Convert leading-root local links ("/assets/...", "/index.html") to relative paths
- Insert canonical link if missing (based on BASE_URL)
- Add meta description if missing (generic fallback)
- Promote first <h2> or <h3> to <h1> if no <h1> present
- Replace inline icon size "width:15px;height:15px" -> "width:1em;height:1em"
Backs up original file as .bak before writing.
"""
import re
from pathlib import Path

ROOT = Path('.').resolve()
BASE_URL = 'https://www.morningstarinfra.com'
html_files = list(ROOT.rglob('*.html'))

link_re = re.compile(r'(href|src)=(["\'])(/[^"\']+)(["\'])')
icon_px_re = re.compile(r'width\s*:\s*15px\s*;?\s*height\s*:\s*15px', re.I)

for f in sorted(html_files):
    text = f.read_text(encoding='utf-8', errors='ignore')
    orig = text
    changed = False
    # Convert root-absolute local links to relative
    def repl_link(m):
        attr, q1, target, q2 = m.groups()
        if target.startswith('/http') or target.startswith('//'):
            return m.group(0)
        # build absolute path
        tgt_abs = (ROOT / target.lstrip('/')).resolve()
        try:
            rel = tgt_abs.relative_to(f.parent).as_posix()
        except Exception:
            # fallback: compute relative path
            rel = Path(tgt_abs).relative_to(ROOT).as_posix()
            # prefix with appropriate ../s
            rel = Path(rel).as_posix()
        return f"{attr}={q1}{rel}{q2}"
    text2 = link_re.sub(repl_link, text)
    if text2 != text:
        text = text2
        changed = True
    # Insert canonical if missing
    if '<link rel="canonical"' not in text.lower():
        # determine path
        relpath = f.relative_to(ROOT).as_posix()
        url = BASE_URL + ('/' + relpath if relpath != 'index.html' else '/')
        # insert before </head>
        if '</head>' in text.lower():
            text = re.sub(r'</head>', f'  <link rel="canonical" href="{url}">\n</head>', text, flags=re.I)
            changed = True
    # Add meta description if missing
    if 'meta name="description"' not in text.lower():
        desc = 'Premium construction and engineering services in Chennai. Morning Star Infra Projects.'
        if '</head>' in text.lower():
            text = re.sub(r'</head>', f'  <meta name="description" content="{desc}">\n</head>', text, flags=re.I)
            changed = True
    # Promote first h2/h3 to h1 if no h1
    if re.search(r'<h1\b', text, re.I) is None:
        m = re.search(r'<h2\b([^>]*)>(.*?)</h2>', text, re.I|re.S)
        if not m:
            m = re.search(r'<h3\b([^>]*)>(.*?)</h3>', text, re.I|re.S)
        if m:
            old = m.group(0)
            new = re.sub(r'^<h[23]', '<h1', old)
            new = re.sub(r'</h[23]>$', '</h1>', new)
            text = text.replace(old, new, 1)
            changed = True
    # Normalize small icon inline px sizes
    text3 = icon_px_re.sub('width:1em;height:1em', text)
    if text3 != text:
        text = text3
        changed = True
    if changed and text != orig:
        bak = f.with_suffix(f.suffix + '.bak')
        if not bak.exists():
            f.write_text(text, encoding='utf-8')
            bak.write_text(orig, encoding='utf-8')
            print('Patched:', f)
        else:
            # already backed up; just write
            f.write_text(text, encoding='utf-8')
            print('Updated (backup exists):', f)
print('auto_fix_site done')
