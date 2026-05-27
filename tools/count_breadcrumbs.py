import re, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
files=list(sorted(ROOT.glob('blog-*/*.html')))+list(sorted(ROOT.glob('pages/*.html')))
count=0
files_with=[]
for p in files:
    s=p.read_text(encoding='utf-8')
    if re.search(r'<nav\b[^>]*\bclass=["\']breadcrumb["\']',s,re.I):
        count+=1
        files_with.append(str(p.relative_to(ROOT)))
print(count)
for f in files_with[:20]:
    print('-',f)
open('tools/count_breadcrumbs_output.txt','w',encoding='utf-8').write('\n'.join([str(count)]+files_with))
