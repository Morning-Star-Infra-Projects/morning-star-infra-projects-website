import re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]

report = []

def check_file(p):
    s = p.read_text(encoding='utf-8')
    issues = []
    # duplicate IDs
    ids = re.findall(r'id=["\']([^"\']+)["\']', s)
    dup_ids = {i:ids.count(i) for i in set(ids) if ids.count(i)>1}
    if dup_ids:
        issues.append(f'Duplicate IDs: {dup_ids}')
    # tag balance checks
    tags = ['div','nav','section','header','main','article','footer','ul','li','ol']
    for t in tags:
        open_count = len(re.findall(r'<%s\b' % t, s, flags=re.I))
        close_count = len(re.findall(r'</%s>' % t, s, flags=re.I))
        if open_count != close_count:
            issues.append(f'Unbalanced <{t}> tags: open={open_count} close={close_count}')
    # empty containers
    empty_containers = len(re.findall(r'<div[^>]*class=["\'][^"\']*container[^"\']*["\'][^>]*>\s*</div>', s, flags=re.I))
    if empty_containers:
        issues.append(f'Empty container wrappers: {empty_containers}')
    # leftover compact breadcrumb separators
    if '›' in s and 'breadcrumb-list' not in s:
        issues.append('Found compact breadcrumb separators (›)')
    return issues

all_files = list(sorted(ROOT.glob('blog-*/*.html')))+list(sorted(ROOT.glob('pages/*.html')))
for p in all_files:
    issues = check_file(p)
    if issues:
        report.append((str(p.relative_to(ROOT)), issues))

out = []
out.append('Audit report for blog pages and pages:')
for f,issues in report:
    out.append(f'\nFile: {f}')
    for it in issues:
        out.append(' - ' + it)

out_text = '\n'.join(out)
print(out_text)
open('tools/audit_report.txt','w',encoding='utf-8').write(out_text)
