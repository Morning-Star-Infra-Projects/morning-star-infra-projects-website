#!/usr/bin/env python3
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_master_header():
    idx = ROOT / 'index.html'
    text = idx.read_text(encoding='utf-8')
    m = re.search(r'(<header\s+id="site-header"[\s\S]*?</header>)', text, flags=re.I)
    if not m:
        print('ERROR: master header not found in index.html')
        sys.exit(1)
    return m.group(1)

def normalize_paths(header_html):
    # Convert relative asset links to root-absolute (/assets/...) to avoid per-folder fixes
    header_html = re.sub(r'src\s*=\s*"\.\./assets/', 'src="/assets/', header_html)
    header_html = re.sub(r'src\s*=\s*"\./assets/', 'src="/assets/', header_html)
    header_html = re.sub(r'href\s*=\s*"\.\./assets/', 'href="/assets/', header_html)
    header_html = re.sub(r'href\s*=\s*"\./assets/', 'href="/assets/', header_html)
    # Also fix CSS/JS links if present
    header_html = re.sub(r'href\s*=\s*"\./assets/', 'href="/assets/', header_html)
    return header_html

def replace_header_in_file(path, master_header):
    text = path.read_text(encoding='utf-8')
    # If header already equals master, skip
    if master_header.strip() in text:
        return 'skipped'
    # Replace existing header block
    if re.search(r'<header\s+id="site-header"[\s\S]*?</header>', text, flags=re.I):
        new = re.sub(r'<header\s+id="site-header"[\s\S]*?</header>', master_header, text, flags=re.I)
        (path.with_suffix(path.suffix + '.bak')).write_text(text, encoding='utf-8')
        path.write_text(new, encoding='utf-8')
        return 'replaced'
    else:
        # Insert after opening <body> if header not found
        if '<body' in text:
            new = re.sub(r'(<body[^>]*>)', r'\1\n' + master_header, text, count=1, flags=re.I)
            (path.with_suffix(path.suffix + '.bak')).write_text(text, encoding='utf-8')
            path.write_text(new, encoding='utf-8')
            return 'inserted'
        else:
            return 'no-body'

def find_blog_html_files(root):
    files = []
    for d in root.iterdir():
        if d.is_dir() and d.name.startswith('blog-'):
            files.extend(list(d.rglob('*.html')))
    return files

def main():
    master = load_master_header()
    master = normalize_paths(master)
    files = find_blog_html_files(ROOT)
    total = len(files)
    replaced = inserted = skipped = nobody = errors = 0
    for f in files:
        try:
            res = replace_header_in_file(f, master)
            if res == 'replaced':
                replaced += 1
            elif res == 'inserted':
                inserted += 1
            elif res == 'skipped':
                skipped += 1
            elif res == 'no-body':
                nobody += 1
        except Exception as e:
            print('ERROR', f, e)
            errors += 1

    print('Summary:')
    print(' Total blog files scanned:', total)
    print(' Replaced headers:', replaced)
    print(' Inserted headers where missing:', inserted)
    print(' Skipped (already matching):', skipped)
    print(' Files with no <body> to insert into:', nobody)
    print(' Errors:', errors)

if __name__ == "__main__":
    main()
