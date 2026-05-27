from pathlib import Path
ROOT=Path('.')
found=0
for f in ROOT.rglob('*.html'):
    s=f.read_text(encoding='utf-8')
    if 'part-' in s:
        print(f)
        found+=1
print('Found files containing part-:', found)
