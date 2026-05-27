from pathlib import Path
ROOT=Path('.')
for f in ROOT.rglob('*.html'):
    s=f.read_text(encoding='utf-8')
    if 'blog-' in s and 'href' in s:
        if 'blog/blog-' in s or 'pages/blog/blog-' in s:
            print(f, 'contains blog/blog- or pages/blog/blog-')
        # find href occurrences
        for line_no, line in enumerate(s.splitlines(), start=1):
            if 'href' in line and 'blog-' in line:
                print(f'{f}:{line_no}: {line.strip()}')
