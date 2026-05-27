from pathlib import Path
ROOT=Path('.')
for i in range(1,10):
    p=ROOT/'pages'/'blog'/f'part-{i}'
    if p.exists():
        files=list(p.glob('*.html'))
        print(p, '->', len(files), 'files')
