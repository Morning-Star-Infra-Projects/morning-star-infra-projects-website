import re
from pathlib import Path
root = Path(r"c:\Users\PRABHAKAR\OneDrive\Documents\hehe-3-backup")
pattern = re.compile(r'(src=")(?:(?:\.{1,3}\/)?assets\/images\/)?(Morning-Star-Infra-Projects-Header-Logo(?:[-_\d]*?)\.(?:webp|jpeg|jpg))(")', re.IGNORECASE)
files = list(root.rglob('*.html'))
changed = []
for f in files:
    s = f.read_text(encoding='utf8')
    new = pattern.sub(r'\1/asset' + 's/images/\2\3', s)
    # Ensure logo img is wrapped in <a href="/">...</a>
    # If img exists without enclosing <a, wrap it.
    def wrap_anchor(match):
        img = match.group(0)
        if re.search(r'<a[^>]*>\s*' + re.escape(img), new):
            return img
        return '<a href="/">' + img + '</a>'
    new = re.sub(r'<img[^>]*Morning-Star-Infra-Projects-Header-Logo[^>]*>', wrap_anchor, new, flags=re.IGNORECASE)
    if new != s:
        f.write_text(new, encoding='utf8')
        changed.append(str(f.relative_to(root)))
print('Updated files:', len(changed))
for c in changed:
    print(c)
