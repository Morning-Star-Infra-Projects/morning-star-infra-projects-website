#!/usr/bin/env python3
import re
import glob
from pathlib import Path

root = Path(__file__).resolve().parents[1]
pattern = root / 'pages' / 'blog' / '*.html'
files = list(glob.glob(str(pattern)))
changed = 0
nav_old_re = re.compile(r'<a href="\.\./index.html">Home</a> \| <a href="\.\./pages/our-story.html">About Us</a> \| <a href="\.\./pages/home-construction.html">Projects</a> \| <a href="\.\./pages/contact.html">Contact</a> \| <a href="\.\./pages/home-construction.html">Services</a>')
new_nav = ('<a href="../index.html">Home</a> | '
           '<a href="../our-story.html">Our Story</a> | '
           '<a href="../our-team.html">Our Team</a> | '
           '<a href="../home-construction.html">Home Construction</a> | '
           '<a href="../commercial-and-industrial.html">Commercial &amp; Industrial</a> | '
           '<a href="../interior-fitouts.html">Interior Fitouts</a> | '
           '<a href="../structural-repair.html">Structural Repair</a> | '
           '<a href="../certifications.html">Certifications</a> | '
           '<a href="../blog.html">Blog</a>')

# Related links to append (3 pages)
append_links = [
    '<a href="../home-construction.html">Home Construction</a>',
    '<a href="../commercial-and-industrial.html">Commercial &amp; Industrial</a>',
    '<a href="../interior-fitouts.html">Interior Fitouts</a>'
]

for fp in files:
    p = Path(fp)
    s = p.read_text(encoding='utf-8')
    s2 = s
    # Replace internal nav if present
    if nav_old_re.search(s2):
        s2 = nav_old_re.sub(new_nav, s2)
    # Append related links if related-posts block exists
    def append_related(match):
        block = match.group(0)
        # count existing anchors
        anchors = re.findall(r'<a [^>]+>', block)
        # if append_links already present, skip
        for link in append_links:
            if link in block:
                continue
            # insert before closing </div>
            block = block.replace('</div>', '\n' + link + '\n</div>', 1)
        return block
    s2 = re.sub(r'<div class="related-posts">.*?</div>', append_related, s2, flags=re.S)
    if s2 != s:
        p.write_text(s2, encoding='utf-8')
        changed += 1

print(f"Processed {len(files)} files, modified: {changed}")
