import re
from pathlib import Path
root = Path(r"c:\Users\PRABHAKAR\OneDrive\Documents\hehe-3-backup")
pat = re.compile(r'src=(["\'])/assets/images/[^"\'>\s]*\s+', re.IGNORECASE)
updated = []
for p in root.rglob('*.html'):
    try:
        s = p.read_text(encoding='utf-8')
    except Exception:
        continue
    orig = s
    s = pat.sub(lambda m: f'src={m.group(1)}/assets/images/Morning-Star-Infra-Projects-Header-Logo.jpeg ', s)
    if s != orig:
        p.write_text(s, encoding='utf-8')
        updated.append(str(p.relative_to(root)))
print('Fixed files:')
for f in updated:
    print(f)
