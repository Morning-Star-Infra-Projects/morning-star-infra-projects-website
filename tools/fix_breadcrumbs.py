import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

def process_file(path):
    s = path.read_text(encoding='utf-8')
    original = s
    # Keep only the first <nav ... class="breadcrumb" ...>...</nav> occurrence and remove any others
    nav_pattern = re.compile(r'(<nav\b[^>]*\bclass=["\']breadcrumb["\'][^>]*>.*?<\/nav>)', flags=re.S|re.I)
    counter = { 'i': 0 }
    def _keep_first(m):
        counter['i'] += 1
        return m.group(1) if counter['i'] == 1 else ''
    s = nav_pattern.sub(_keep_first, s)
    # Ensure only one ld+json BreadcrumbList in head: keep first occurrence
    scripts = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>.*?</script>', s, flags=re.S|re.I)
    if len(scripts) > 1:
        first = scripts[0]
        # remove all and reinsert first where the head tag opens
        s = re.sub(r'<script[^>]*type="application/ld\+json"[^>]*>.*?</script>', '', s, flags=re.S|re.I)
        s = s.replace('<head>', '<head>\n' + first, 1)
    # Collapse multiple blank lines
    s = re.sub(r'\n{3,}', '\n\n', s)
    # Remove empty container wrappers directly before main (common minified patterns)
    s = re.sub(r'<div class="container">\s*</div>\s*', '', s)

    if s != original:
        path.write_text(s, encoding='utf-8')
        return True
    return False


def main():
    modified = []
    for pattern in ['blog-*/*.html', 'pages/*.html']:
        for p in sorted(ROOT.glob(pattern)):
            if p.is_file():
                changed = process_file(p)
                if changed:
                    modified.append(str(p.relative_to(ROOT)))
    print('Modified files:')
    for m in modified:
        print('-', m)

if __name__ == '__main__':
    main()
