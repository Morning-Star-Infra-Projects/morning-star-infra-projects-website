import re
from pathlib import Path
root = Path(r"c:\Users\PRABHAKAR\OneDrive\Documents\hehe-3-backup")
pattern_src = re.compile(r'(<img[^>]*?)src=("|\')(?:(?:\.{1,3}/)?assets/images/)?(Morning-Star-Infra-Projects-Header-Logo(?:[-_\d]*?)\.(?:webp|jpeg|jpg))("|\')', re.IGNORECASE)
pattern_wrap = re.compile(r'(?i)(?:<a[^>]*href=("|\')/?("|\')?[^>]*>\s*)?(<img[^>]*?Morning-Star-Infra-Projects-Header-Logo[^>]*?>)(\s*</a>)?')
updated_files = []
for p in root.rglob('*.html'):
    try:
        s = p.read_text(encoding='utf-8')
    except Exception:
        continue
    orig = s
    s = pattern_src.sub(lambda m: f"{m.group(1)}src=\"/assets/images/{m.group(3)}\"", s)
    s = pattern_wrap.sub(lambda m: f"<a href=\"/\">{m.group(3)}</a>", s)
    if s != orig:
        p.write_text(s, encoding='utf-8')
        updated_files.append(str(p.relative_to(root)))
print("Updated files:")
for f in updated_files:
    print(f)
