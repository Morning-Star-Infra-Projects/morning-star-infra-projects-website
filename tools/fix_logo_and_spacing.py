#!/usr/bin/env python3
"""
fix_logo_and_spacing.py
Fixes incorrect logo src/srcset paths in pages/blog.html and pages/blog/*.html
Also adds top padding to the blog index main container for spacing under header.
"""
import os
import re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BLOG_INDEX = os.path.join(ROOT, 'pages', 'blog.html')
ART_DIR = os.path.join(ROOT, 'pages', 'blog')

def fix_blog_index(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
    orig = s
    # Fix srcset that had a './assets' part
    s = s.replace('srcset="../assets/images/morning-star-logo-72.webp 72w, ./assets/images/morning-star-logo-144.webp 144w',
                  'srcset="../assets/images/morning-star-logo-72.webp 72w, ../assets/images/morning-star-logo-144.webp 144w')
    # Fix img src if absolute
    s = s.replace('img src="/assets/images/morning-star-logo-72.webp"', 'img src="../assets/images/morning-star-logo-72.webp"')
    # Also fix any './assets/images' occurrences to '../assets/images' in header
    s = s.replace('srcset="./assets/images/', 'srcset="../assets/images/')
    s = s.replace('src="./assets/images/', 'src="../assets/images/')
    # Add top padding to main.container (if not present)
    s = re.sub(r'<main class="container">', '<main class="container" style="padding-top:28px">', s, count=1)
    if s != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(s)
        print('Patched', path)
    else:
        print('No changes for', path)

def fix_article(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
    orig = s
    # Replace any srcset occurrences that use './assets' with '../../assets'
    s = s.replace('srcset="../../assets/images/morning-star-logo-72.webp 72w, ./assets/images/morning-star-logo-144.webp 144w',
                  'srcset="../../assets/images/morning-star-logo-72.webp 72w, ../../assets/images/morning-star-logo-144.webp 144w')
    s = s.replace('srcset="./assets/images/', 'srcset="../../assets/images/')
    s = s.replace('src="../assets/images/morning-star-logo-72.webp"', 'src="../../assets/images/morning-star-logo-72.webp"')
    s = s.replace('src="/assets/images/morning-star-logo-72.webp"', 'src="../../assets/images/morning-star-logo-72.webp"')
    # Fix any remaining './assets' occurrences
    s = s.replace('src="./assets/images/', 'src="../../assets/images/')
    s = s.replace('srcset="./assets/images/', 'srcset="../../assets/images/')
    if s != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(s)
        print('Patched', path)
    else:
        print('No changes for', path)

fix_blog_index(BLOG_INDEX)
for fname in os.listdir(ART_DIR):
    if fname.endswith('.html'):
        fix_article(os.path.join(ART_DIR, fname))
print('Logo path and spacing fixes complete')
