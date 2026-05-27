from pathlib import Path
import re
ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / 'pages'
for file in PAGES.glob('*.html'):
    text = file.read_text(encoding='utf-8')
    orig = text
    # Replace hero_brand-800.webp references
    text = text.replace('../assets/images/hero_brand-800.webp', '../assets/images/hero-Morning-Star-Infra-Projects-Home.webp')
    text = text.replace('/assets/images/hero_brand-800.webp', '../assets/images/hero-Morning-Star-Infra-Projects-Home.webp')
    # Remove local font preload lines
    text = re.sub(r'<link[^>]*href=["\'](?:/)?fonts/inter\.woff2["\'][^>]*>\s*', '', text, flags=re.I)
    # Normalize header logo src/srcset to ../assets
    text = re.sub(r'srcset=["\']/?assets/images/([^"\']+)["\']', r'srcset="../assets/images/\1"', text)
    text = re.sub(r'src=["\']/?assets/images/([^"\']+)["\']', r'src="../assets/images/\1"', text)
    # Ensure header logo link points to ../index.html
    text = re.sub(r'href=["\']index\.html["\']', 'href="../index.html"', text)
    if text != orig:
        bak = file.with_suffix(file.suffix + '.bak')
        if not bak.exists():
            bak.write_text(orig, encoding='utf-8')
        file.write_text(text, encoding='utf-8')
        print('Patched', file)
print('Done')
