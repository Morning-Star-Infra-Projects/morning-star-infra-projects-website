#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def fix_file(path: Path):
    text = path.read_text(encoding='utf-8')
    orig = text

    # Patterns to fix when file is inside a blog-* folder
    # Replace href="index.html" -> href="../index.html" (and single quotes)
    text = re.sub(r'(?i)href=(\")index\.html(\")', r'href="../index.html"', text)
    text = re.sub(r"(?i)href=(\')index\.html(\')", r"href='../index.html'", text)

    # src="assets/..." -> src="../assets/..." and fix double slashes
    text = re.sub(r'(?i)src=(\")\.?\.?//+assets/', 'src="../assets/', text)
    text = re.sub(r"(?i)src=(\')\.?\.?//+assets/", "src='../assets/", text)
    text = re.sub(r'(?i)src=(\")assets/','src="../assets/', text)
    text = re.sub(r"(?i)src=(\')assets/","src='../assets/", text)

    # href to pages/ -> ../pages/
    text = re.sub(r'(?i)href=(\")pages/','href="../pages/', text)
    text = re.sub(r"(?i)href=(\')pages/","href='../pages/", text)

    # Links to other blog folders should be ../blog-x/... when linking from a blog file
    text = re.sub(r'(?i)href=(\")(blog-\d/)', r'href="../\2', text)
    text = re.sub(r"(?i)href=(\')(blog-\d/)", r"href='../\2", text)

    # Normalize any ../our-story.html or our-story.html -> ../pages/our-story.html
    text = re.sub(r'(?i)href=(\")(?:\.\./)?our-story\.html(\")', r'href="../pages/our-story.html"', text)
    text = re.sub(r"(?i)href=(\')(?:\.\./)?our-story\.html(\')", r"href='../pages/our-story.html'", text)
    text = re.sub(r'(?i)href=(\")(?:\.\./)?our-team\.html(\")', r'href="../pages/our-team.html"', text)
    text = re.sub(r"(?i)href=(\')(?:\.\./)?our-team\.html(\')", r"href='../pages/our-team.html'", text)

    # Fix links that reference blog files without ../ prefix in various attributes (src/href)
    text = re.sub(r'(?i)(src|href)=(\")(\.{0,2}/)?(blog-\d/)', lambda m: f'{m.group(1)}="../{m.group(4)}', text)
    text = re.sub(r"(?i)(src|href)=(\')(\.{0,2}/)?(blog-\d/)", lambda m: f"{m.group(1)}='../{m.group(4)}", text)

    # Replace double slashes like ..//assets -> ../assets
    text = text.replace('..//assets','../assets')

    # Replace inline fixed px sizes (logo icons) width:44px;height:44px -> width:2.75rem;height:2.75rem
    text = re.sub(r'width:44px;height:44px', 'width:2.75rem;height:2.75rem', text)
    text = re.sub(r'width:44px; height:44px', 'width:2.75rem; height:2.75rem', text)

    # Convert bare ../<page>.html to ../pages/<page>.html for known page targets
    for p in ('home-construction.html','commercial-and-industrial.html','interior-fitouts.html','structural-repair.html','certifications.html'):
        pattern = r'(?i)(href\s*=\s*["\'])\.\./' + re.escape(p) + r'(["\'])'
        repl = r"\1../pages/" + p + r"\2"
        text = re.sub(pattern, repl, text)

    # Replace ../blog.html -> ../pages/blog.html
    text = re.sub(r'(?i)(href\s*=\s*["\'])\.\./blog\.html(["\'])', r"\1../pages/blog.html\2", text)

    # Replace legacy hero image references to available hero images
    text = text.replace('../assets/images/hero_brand-800.webp', '../assets/images/hero-Morning-Star-Infra-Projects-Home.webp')

    if text != orig:
        bak = path.with_suffix(path.suffix + '.bak')
        if not bak.exists():
            bak.write_text(orig, encoding='utf-8')
        path.write_text(text, encoding='utf-8')
        print(f'Patched: {path}')

def main():
    for i in range(1,7):
        folder = ROOT / f'blog-{i}'
        if not folder.exists():
            continue
        for file in folder.rglob('*.html'):
            fix_file(file)

if __name__ == '__main__':
    main()
