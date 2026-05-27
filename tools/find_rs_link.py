import glob
from pathlib import Path
files=glob.glob('pages/*.html')
found=[]
for f in files:
    s=Path(f).read_text(encoding='utf-8')
    if 'class="rs-link"' in s:
        found.append(f)
for f in found:
    print(f)
print('Count:',len(found))
