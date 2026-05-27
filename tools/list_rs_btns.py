import glob
from pathlib import Path
files=glob.glob('pages/*.html')
modified=[]
for f in files:
    s=Path(f).read_text(encoding='utf-8')
    if 'class="rs-btn"' in s:
        modified.append(f)
for m in modified:
    print(m)
print('Count:',len(modified))
