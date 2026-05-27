#!/usr/bin/env python3
from pathlib import Path
import re
p = Path('pages/blog.html')
s = p.read_text(encoding='utf-8')
# Remove any <span class="blog-tag">...</span> inside the file
s2 = re.sub(r"\n\s*<span class=\"blog-tag\">.*?</span>", '', s)
if s2 != s:
    p.write_text(s2, encoding='utf-8')
    print('Removed blog-tag spans')
else:
    print('No changes made')
