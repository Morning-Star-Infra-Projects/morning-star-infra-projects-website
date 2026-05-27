import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[1]
errors = []
for pattern in ['blog-*/*.html','pages/*.html']:
    for p in sorted(ROOT.glob(pattern)):
        s = p.read_text(encoding='utf-8')
        # count unique nav elements that include breadcrumb (class or aria-label)
        count = len(re.findall(r'<nav\b[^>]*\b(breadcrumb|aria-label=["\']Breadcrumb["\'])[^>]*>', s, flags=re.I))
        if count != 1:
            errors.append((str(p.relative_to(ROOT)), count))
print('Files with breadcrumb count != 1:')
for f,c in errors:
    print(f, c)
print('Total checked:', sum(1 for _ in ROOT.glob('blog-*/*.html')) + sum(1 for _ in ROOT.glob('pages/*.html')))
