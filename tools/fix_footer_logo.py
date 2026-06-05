import re
from pathlib import Path
root = Path(r"c:\Users\PRABHAKAR\OneDrive\Documents\hehe-3-backup")
# Replace any src referencing footer logo variants or broken src with absolute path
pat_src = re.compile(r'src=("|\')?(?:\.\./|\./)?assets/images/(?:Morning-Star-Infra-Projects-)?(?:Footer-Logo|footer-logo)[^"\'\s>]*', re.IGNORECASE)
# Fix picture/source srcset too
pat_srcset = re.compile(r'srcset=("|\')?(?:\.\./|\./)?assets/images/(?:Morning-Star-Infra-Projects-)?(?:Footer-Logo|footer-logo)[^"\']*', re.IGNORECASE)
updated = []
for p in root.rglob('*.html'):
    try:
        s = p.read_text(encoding='utf-8')
    except Exception:
        continue
    orig = s
    s = pat_srcset.sub('srcset="/assets/images/Morning-Star-Infra-Projects-Footer-Logo.webp"', s)
    s = pat_src.sub('src="/assets/images/Morning-Star-Infra-Projects-Footer-Logo.webp"', s)
    if s != orig:
        p.write_text(s, encoding='utf-8')
        updated.append(str(p.relative_to(root)))
print('Updated files:')
for f in updated:
    print(f)
