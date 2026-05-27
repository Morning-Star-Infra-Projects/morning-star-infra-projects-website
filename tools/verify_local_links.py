#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
import urllib.request
import urllib.error

root = Path(__file__).resolve().parent.parent
blog_files = sorted(root.glob('blog-*/*.html'))
urls = set()
for f in blog_files[:50]:
    text = f.read_text(encoding='utf-8')
    soup = BeautifulSoup(text, 'html.parser')
    for a in soup.select('div.related-posts a[href]'):
        href = a['href'].strip()
        if href.startswith(('http://','https://')):
            urls.add(href)
        elif href.startswith('/'):
            urls.add('http://localhost:8080' + href)
        else:
            # relative
            rel = (f.parent / href).relative_to(root).as_posix()
            urls.add('http://localhost:8080/' + rel)

print(f'Will check {len(urls)} URLs (first 100):')
for u in list(urls)[:100]:
    try:
        req = urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as r:
            code = r.getcode()
            if code!=200:
                print('BAD', code, u)
    except urllib.error.HTTPError as e:
        print('HTTPERR', e.code, u)
    except Exception as e:
        print('ERR', type(e).__name__, u)
