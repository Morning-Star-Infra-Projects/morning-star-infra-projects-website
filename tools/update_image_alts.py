#!/usr/bin/env python3
"""
Scan HTML files in the workspace and add/standardize `alt` attributes for <img> tags.
Requires: beautifulsoup4

Usage:
  pip install beautifulsoup4
  python tools/update_image_alts.py

This script makes in-place edits and creates a .bak backup for each modified file.
"""
import os
from bs4 import BeautifulSoup

ROOT = os.path.join(os.path.dirname(__file__), '..')
ROOT = os.path.abspath(ROOT)

def friendly_from_filename(src):
    if not src:
        return ''
    name = os.path.basename(src.split('?')[0]).split('.')[0]
    name = name.replace('-', ' ').replace('_', ' ').strip()
    return name

def standardize_logo_alt(alt):
    return 'Morning Star Infra Projects logo'

def process_file(path):
    changed = False
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')

    # page title for context
    title_tag = soup.find('h1') or soup.find('title')
    page_title = title_tag.get_text(strip=True) if title_tag else ''

    for img in soup.find_all('img'):
        src = img.get('src') or ''
        alt = img.get('alt')
        # Standardize footer/logo images
        if 'logo' in (src or '').lower() or (alt and 'logo' in alt.lower()):
            desired = standardize_logo_alt(alt)
            if alt != desired:
                img['alt'] = desired
                changed = True
            continue

        if alt and alt.strip():
            # leave existing alt (assumed intentionally set)
            continue

        # Build a friendly alt
        if 'article-hero' in (img.get('class') or []):
            if page_title:
                new_alt = f"{page_title} — Morning Star Infra Projects"
            else:
                new_alt = friendly_from_filename(src)
        else:
            friendly = friendly_from_filename(src)
            if friendly:
                # add location tag for local pages when relevant
                if 'home' in path.lower() or 'index' in path.lower():
                    new_alt = f"{friendly} — Morning Star Infra Projects, Chennai"
                else:
                    new_alt = f"{friendly} — Morning Star Infra Projects"
            else:
                new_alt = 'Morning Star Infra Projects image'

        img['alt'] = new_alt
        changed = True

    if changed:
        bak = path + '.bak'
        with open(bak, 'w', encoding='utf-8') as f:
            f.write(html)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print('Updated:', path)

def main():
    exts = ('.html', '.htm')
    for root, dirs, files in os.walk(ROOT):
        # skip node_modules, .git and assets/images binary folder
        if '/.git' in root or '\\\.git' in root:
            continue
        for fname in files:
            if fname.lower().endswith(exts):
                path = os.path.join(root, fname)
                process_file(path)

if __name__ == '__main__':
    main()
