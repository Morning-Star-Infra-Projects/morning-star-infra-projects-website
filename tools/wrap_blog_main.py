#!/usr/bin/env python3
import glob
import io
from pathlib import Path

root = Path(__file__).resolve().parents[1]
pattern = root / 'pages' / 'blog' / '*.html'
files = list(glob.glob(str(pattern)))
modified = 0
skipped = 0
for fp in files:
    p = Path(fp)
    s = p.read_text(encoding='utf-8')
    main_start = s.find('<main class="article-content"')
    if main_start == -1:
        skipped += 1
        continue
    main_open_end = s.find('>', main_start)
    if main_open_end == -1:
        skipped += 1
        continue
    main_close = s.rfind('</main>')
    if main_close == -1 or main_close <= main_open_end:
        # If there's no closing </main>, try to insert before the footer
        footer_pos = s.find('<footer id="site-footer"')
        if footer_pos == -1:
            skipped += 1
            continue
        main_close = footer_pos
    main_inner = s[main_open_end+1:main_close]
    if '<div class="container"' in main_inner:
        skipped += 1
        continue
    # insert opening container after opening main tag
    s2 = s[:main_open_end+1] + '\n<div class="container">' + s[main_open_end+1:main_close] + '\n</div>' + s[main_close:]
    p.write_text(s2, encoding='utf-8')
    modified += 1
print(f"Processed {len(files)} files: modified={modified}, skipped={skipped}")
