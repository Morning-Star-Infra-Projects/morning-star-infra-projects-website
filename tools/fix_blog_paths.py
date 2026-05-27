#!/usr/bin/env python3
"""
fix_blog_paths.py
Adjusts CSS and asset links so the blog index and article pages reference the correct relative paths.
- pages/blog.html: uses ../assets/... and ./ for other pages
- pages/blog/*.html: uses ../../assets/... and ../ for other pages
"""
import os
import re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PAGES_DIR = os.path.join(ROOT, 'pages')
BLOG_DIR = os.path.join(PAGES_DIR, 'blog')
BLOG_INDEX = os.path.join(PAGES_DIR, 'blog.html')

def fix_index(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
    orig = s
    # CSS links -> ../assets/
    s = re.sub(r'href="/assets/', 'href="../assets/', s)
    s = re.sub(r'src="/assets/', 'src="../assets/', s)
    # header image srcset that used ./assets -> ../assets
    s = s.replace('srcset="./assets/images/', 'srcset="../assets/images/')
    s = s.replace('src="./assets/images/', 'src="../assets/images/')
    # root page links -> relative within pages/
    s = s.replace('href="/index.html"', 'href="../index.html"')
    s = s.replace('href="/pages/', 'href="')
    s = s.replace('href="/pages', 'href="')
    s = s.replace("href=\"/pages/blog.html\"", "href=\"blog.html\"")
    # ensure card links are correct (they should be blog/xxx.html)
    if s != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(s)
        print('Fixed', path)
    else:
        print('No changes for', path)

def fix_article(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
    orig = s
    # CSS links -> ../../assets/
    s = re.sub(r'href="/assets/', 'href="../../assets/', s)
    s = re.sub(r'src="/assets/', 'src="../../assets/', s)
    # header/logo references
    s = s.replace('srcset="./assets/images/', 'srcset="../../assets/images/')
    s = s.replace('src="/assets/images/', 'src="../../assets/images/')
    s = s.replace('src="../assets/images/', 'src="../../assets/images/')
    # links to index and pages -> relative from pages/blog/
    s = s.replace('href="/index.html"', 'href="../../index.html"')
    s = s.replace('href="/pages/', 'href="../')
    s = s.replace('href="/pages', 'href="../')
    # links to blog index -> ../blog.html or ../blog.html
    s = s.replace('href="/pages/blog.html"', 'href="../blog.html"')
    # adjust related post links that point to filename
    s = re.sub(r'href="blog/(.*?)"', r'href="\1"', s)
    # adjust image src in article body if root-relative
    s = s.replace('src="/assets/images/', 'src="../../assets/images/')
    if s != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(s)
        print('Fixed', path)
    else:
        print('No changes for', path)

fix_index(BLOG_INDEX)
for fname in os.listdir(BLOG_DIR):
    if fname.endswith('.html'):
        fix_article(os.path.join(BLOG_DIR, fname))
print('Path fixes complete')
