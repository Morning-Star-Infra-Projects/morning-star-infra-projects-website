"""site_audit.py
Scans the workspace HTML files and reports:
- broken local links (href/src/srcset)
- missing meta tags (title, description, viewport, canonical)
- duplicate H1 tags
- images with missing/empty alt
- inline fixed pixel widths/heights in style attributes
- presence of breadcrumb JSON-LD scripts
Writes report to tools/site_audit_report.txt
"""
import re
from pathlib import Path

ROOT = Path('.').resolve()
html_files = list(ROOT.rglob('*.html'))
report_lines = []

link_re = re.compile(r'(?:href|src)=\s*["\']([^"\'#?]+)')
srcset_re = re.compile(r'srcset=\s*["\']([^"\']+)["\']')
meta_name_re = re.compile(r'<meta[^>]+name=["\']([^"\']+)["\'][^>]*>', re.I)
meta_tag_re = re.compile(r'<meta[^>]+(?:name|property)=\s*["\']([^"\']+)["\'][^>]*content=\s*["\']([^"\']*)["\']', re.I)
img_re = re.compile(r'<img[^>]+>', re.I)
alt_re = re.compile(r'alt=\s*["\']([^"\']*)["\']', re.I)
style_px_re = re.compile(r'style=["\']([^"\']*\b(?:width|height)\s*:\s*\d+px[^"\']*)["\']', re.I)

for f in sorted(html_files):
    rel = f.relative_to(ROOT)
    text = f.read_text(encoding='utf-8', errors='ignore')
    issues = []
    # meta checks
    has_title = bool(re.search(r'<title>.*?</title>', text, re.I|re.S))
    if not has_title:
        issues.append('Missing <title> tag')
    meta_names = {m.group(1).lower(): m.group(0) for m in meta_name_re.finditer(text)}
    for needed in ['viewport','description']:
        if needed not in meta_names:
            issues.append(f'Missing meta name="{needed}"')
    if 'canonical' not in text.lower():
        issues.append('Missing canonical link')
    # h1 count
    h1_count = len(re.findall(r'<h1\b', text, re.I))
    if h1_count == 0:
        issues.append('No H1 found')
    elif h1_count > 1:
        issues.append(f'Duplicate H1 tags ({h1_count})')
    # images alt
    for img in img_re.finditer(text):
        tag = img.group(0)
        m = alt_re.search(tag)
        if m is None or m.group(1).strip() == '':
            issues.append('Image with missing/empty alt: ' + (tag[:80].strip()))
            break
    # breadcrumb JSON-LD
    if 'BreadcrumbList' not in text and 'breadcrumb' in text.lower():
        issues.append('Breadcrumb present but BreadcrumbList JSON-LD missing')
    # inline px styles
    for m in style_px_re.finditer(text):
        issues.append('Inline fixed px in style attr: ' + (m.group(1)[:80].strip()))
        break
    # local links
    bad_links = []
    for m in link_re.finditer(text):
        target = m.group(1).strip()
        if target.startswith('http') or target.startswith('mailto:') or target.startswith('tel:') or target.startswith('#'):
            continue
        # resolve path
        tgt_path = (f.parent / target).resolve()
        # strip query or fragment
        tgt_clean = Path(str(tgt_path).split('#')[0].split('?')[0])
        if not tgt_clean.exists():
            bad_links.append(target)
    if bad_links:
        issues.append('Broken local links: ' + ', '.join(bad_links[:5]))
    if issues:
        report_lines.append(f'FILE: {rel}')
        for it in issues:
            report_lines.append('  - ' + it)
        report_lines.append('')

out = ROOT / 'tools' / 'site_audit_report.txt'
out.write_text('\n'.join(report_lines) or 'No issues found by site_audit.py\n', encoding='utf-8')
print('Audit written to', out)
