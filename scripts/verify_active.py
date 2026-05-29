import re
import os
from urllib.parse import urlparse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PAGES = [
    os.path.join(ROOT, 'index.html'),
    os.path.join(ROOT, 'pages', 'blog.html'),
    os.path.join(ROOT, 'blog-1', 'affordable-construction-services-in-chennai.html'),
    os.path.join(ROOT, 'blog-2', 'how-to-choose-architects-near-me-in-tamil-nadu.html') if os.path.exists(os.path.join(ROOT,'blog-2','how-to-choose-architects-near-me-in-tamil-nadu.html')) else None,
    os.path.join(ROOT, 'blog-3', 'how-to-find-the-best-structural-engineers-in-tamil-nadu.html') if os.path.exists(os.path.join(ROOT,'blog-3','how-to-find-the-best-structural-engineers-in-tamil-nadu.html')) else None,
    os.path.join(ROOT, 'pages', 'home-construction.html'),
    os.path.join(ROOT, 'pages', 'commercial-and-industrial.html'),
    os.path.join(ROOT, 'pages', 'structural-repair.html'),
    os.path.join(ROOT, 'pages', 'interior-fitouts.html'),
]
PAGES = [p for p in PAGES if p]

ALIAS_MAP = {
    '/residential': '/pages/home-construction',
    '/industrial':  '/pages/commercial-and-industrial',
    '/interiors':   '/pages/interior-fitouts',
    '/structural':  '/pages/structural-repair'
}


def normalize(p):
    if not p: return ''
    # strip domain
    up = urlparse(p)
    path = up.path if up.path else p
    # ensure leading slash
    if not path.startswith('/'):
        path = '/' + path
    # remove index.html
    path = re.sub(r'/index\.html$', '', path, flags=re.I)
    # remove trailing .html for matching flexibility
    path = re.sub(r'\.html$', '', path, flags=re.I)
    if len(path) > 1:
        path = re.sub(r'/$', '', path)
    return path or '/'


def resolve_alias(p):
    return ALIAS_MAP.get(p, p)


def extract_nav(html):
    # get nav block
    m = re.search(r'<nav[^>]*class="[^"]*hdr-nav[^"]*"[^>]*>(.*?)</nav>', html, re.S)
    nav = m.group(1) if m else ''
    # mobile menu
    m2 = re.search(r'<div[^>]*id="mobile-menu"[^>]*>(.*?)</div>', html, re.S)
    mob = m2.group(1) if m2 else ''
    return nav, mob


def find_links(block):
    # return list of (tag, classes, href, text)
    links = []
    for a in re.finditer(r'<a\s+([^>]*?)>(.*?)</a>', block, re.S):
        attrs = a.group(1)
        text = re.sub('<[^>]+>', '', a.group(2)).strip()
        href_m = re.search(r'href\s*=\s*"([^"]+)"', attrs)
        href = href_m.group(1) if href_m else ''
        cls_m = re.search(r'class\s*=\s*"([^"]+)"', attrs)
        classes = cls_m.group(1) if cls_m else ''
        links.append((classes, href, text))
    return links


def page_path_from_file(filepath, html):
    # prefer canonical link
    m = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', html)
    if m:
        return normalize(urlparse(m.group(1)).path)
    # else derive from file path relative to root
    rel = os.path.relpath(filepath, ROOT).replace('\\','/')
    return normalize('/' + rel)


for p in PAGES:
    html = open(p, 'r', encoding='utf-8').read()
    nav, mob = extract_nav(html)
    nav_links = find_links(nav)
    mob_links = find_links(mob)
    current = page_path_from_file(p, html)
    path_resolved = resolve_alias(current)
    print('\nPage:', os.path.relpath(p, ROOT), '-> path=', current)
    # Simulate initial loop
    matched = False
    for cls, href, txt in nav_links + mob_links:
        hp = normalize(href)
        hp_res = resolve_alias(hp)
        if not hp: continue
        if hp == current or hp_res == current or current == hp or current.startswith(hp + '/') or current.startswith(hp_res + '/') or hp_res == path_resolved:
            print('  MATCH initial: link=', href, 'classes=', cls, 'text=', txt)
            matched = True
            # if drop-link, also show that trigger would be set
            if 'drop-link' in cls:
                print('    -> drop-link matched, parent trigger will be highlighted')
            break
    if not matched:
        # check blog grouping
        is_blog = re.search(r'(^|/)blog-\d+/', current + '/') or current.startswith('/blog') or current in ['/pages/blog','/pages/blog.html','/blog']
        if is_blog:
            print('  MATCH blog grouping -> Blog nav will be highlighted')
            matched = True
    if not matched:
        # check drop menu
        drop_links = re.findall(r'<div class="nav-drop-menu">(.*?)</div>', nav, re.S)
        found = False
        if drop_links:
            for block in drop_links:
                for cls, href, txt in find_links(block):
                    dh = normalize(href)
                    dh_res = resolve_alias(dh)
                    if dh == current or dh_res == current or current.startswith(dh + '/') or current.startswith(dh_res + '/') or current.find(dh) >= 0:
                        print('  MATCH dropMenu: child=', href, '-> parent trigger will be active')
                        found = True
                        break
                if found: break
        if not found:
            # other heuristics
            if re.search(r'our-story|story|our-team|team', current):
                print('  MATCH about grouping')
            elif re.search(r'projects|project-', current):
                print('  MATCH projects grouping')
            elif re.search(r'careers|career', current):
                print('  MATCH careers grouping')
            elif re.search(r'contact', current):
                print('  MATCH contact grouping')
            else:
                print('  NO MATCH found (fallback to Home if root)')

print('\nDone')
