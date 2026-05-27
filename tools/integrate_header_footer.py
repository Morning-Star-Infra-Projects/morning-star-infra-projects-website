#!/usr/bin/env python3
"""
integrate_header_footer.py
Injects site's header and footer (from root index.html) into pages/blog.html and all files under pages/blog/.
Converts asset and page links to root-relative paths for consistency.
"""
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INDEX = os.path.join(ROOT, 'index.html')
PAGES_DIR = os.path.join(ROOT, 'pages')
BLOG_DIR = os.path.join(PAGES_DIR, 'blog')
BLOG_INDEX = os.path.join(PAGES_DIR, 'blog.html')

with open(INDEX, 'r', encoding='utf-8') as f:
    idx = f.read()

# extract header and footer
header_match = re.search(r'(<header[^>]*id="site-header"[\s\S]*?</header>)', idx, re.I)
footer_match = re.search(r'(<footer[^>]*id="site-footer"[\s\S]*?</footer>)', idx, re.I)
if not header_match or not footer_match:
    print('Header or footer not found in index.html')
    raise SystemExit(1)
header_html = header_match.group(1)
footer_html = footer_match.group(1)

# normalize to root-relative paths
def normalize_paths(html):
    html = re.sub(r'href="\./assets/', 'href="/assets/', html)
    html = re.sub(r'src="\./assets/', 'src="/assets/', html)
    html = re.sub(r'href="assets/', 'href="/assets/', html)
    html = re.sub(r'src="assets/', 'src="/assets/', html)
    html = re.sub(r'href="\.\./assets/', 'href="/assets/', html)
    html = re.sub(r'src="\.\./assets/', 'src="/assets/', html)
    # pages
    html = re.sub(r'href="pages/', 'href="/pages/', html)
    html = re.sub(r'href="\.\./pages/', 'href="/pages/', html)
    # index
    html = re.sub(r'href="index.html"', 'href="/index.html"', html)
    html = re.sub(r'href="\.\./index.html"', 'href="/index.html"', html)
    # favicon
    html = re.sub(r'href="\./favicon/', 'href="/favicon/', html)
    html = re.sub(r'href="favicon/', 'href="/favicon/', html)
    # other relative src
    html = re.sub(r'src="\./', 'src="/', html)
    html = re.sub(r'href="\./', 'href="/', html)
    return html

header_html = normalize_paths(header_html)
footer_html = normalize_paths(footer_html)

# function to process a single html file

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content
    # normalize head assets to root-relative
    content = re.sub(r'href="\.{1,2}/assets/', 'href="/assets/', content)
    content = re.sub(r'src="\.{1,2}/assets/', 'src="/assets/', content)
    content = re.sub(r'href="\.{1,2}/favicon/', 'href="/favicon/', content)
    # insert or replace header
    if re.search(r'<header[^>]*id="site-header"', content):
        content = re.sub(r'<header[^>]*id="site-header"[\s\S]*?</header>', header_html, content, flags=re.I)
    else:
        # insert header after <body>
        content = re.sub(r'(<body[^>]*>)', r"\1\n" + header_html, content, flags=re.I)
    # replace footer
    if re.search(r'<footer[^>]*id="site-footer"', content):
        content = re.sub(r'<footer[^>]*id="site-footer"[\s\S]*?</footer>', footer_html, content, flags=re.I)
    else:
        # insert footer before </body>
        content = re.sub(r'(</body>)', footer_html + r"\n\1", content, flags=re.I)
    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Updated', path)
    else:
        print('No changes for', path)

# process blog index and all articles
process_file(BLOG_INDEX)
for fname in os.listdir(BLOG_DIR):
    if fname.lower().endswith('.html'):
        process_file(os.path.join(BLOG_DIR, fname))

print('Header/footer integration complete')
