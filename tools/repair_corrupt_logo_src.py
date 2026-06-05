import re
from pathlib import Path
root = Path(r"c:\Users\PRABHAKAR\OneDrive\Documents\hehe-3-backup")
pat_double = re.compile(r'src="/assets/images/[^\">\s]*\s+alt=', re.IGNORECASE)
pat_single = re.compile(r"src='/assets/images/[^\'>\s]*\s+alt=", re.IGNORECASE)
updated = []
for p in root.rglob('*.html'):
    try:
        s = p.read_text(encoding='utf-8')
    except Exception:
        continue
    orig = s
    s = pat_double.sub('src="/assets/images/Morning-Star-Infra-Projects-Header-Logo.jpeg" alt=', s)
    s = pat_single.sub("src='/assets/images/Morning-Star-Infra-Projects-Header-Logo.jpeg' alt=", s)
    if s != orig:
        p.write_text(s, encoding='utf-8')
        updated.append(str(p.relative_to(root)))
print('Fixed files:')
for f in updated:
    print(f)
