from pathlib import Path
ROOT=Path('.')
for i in range(1,10):
    p=ROOT/'pages'/'blog'/f'blog-{i}'
    if p.exists():
        print(p, '->', len(list(p.glob('*.html'))), 'files')
