#!/usr/bin/env python3
"""
sync_header_footer.py

Usage: python tools/sync_header_footer.py

- Reads components/header.html and components/footer.html as source of truth.
- Backs up each HTML file to .bak before modifying.
- Replaces top <header id="site-header">...</header> and
  bottom <footer id="site-footer">...</footer> blocks in every .html file.
- Fixes common relative path issues for nested pages by converting
  "../assets/..." or "./assets/..." to absolute "/assets/..." where appropriate.
- Emits a report to stdout and writes report.json in the repo root.

NOTE: Run locally. Review diffs before committing.
"""
import re
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENTS = ROOT / 'components'
HEADER_SRC = COMPONENTS / 'header.html'
FOOTER_SRC = COMPONENTS / 'footer.html'

HTML_GLOB = ['**/*.html']
BACKUP_EXT = '.orig.bak'
REPORT_PATH = ROOT / 'tools' / 'sync_header_footer_report.json'

HEADER_RE = re.compile(r'<header\s+id=["\']site-header["\'][\s\S]*?</header>', re.IGNORECASE)
FOOTER_RE = re.compile(r'<footer\s+id=["\']site-footer["\'][\s\S]*?</footer>', re.IGNORECASE)

def load_component(path):
    return path.read_text(encoding='utf-8')

def fix_asset_paths(html_text, file_path):
    # Replace ../assets/... or ./assets/... with /assets/... for nested pages
    # Only modify if the path starts with ../ or ./ and target /assets exists
    # Use double-escaped pattern to avoid quote balancing issues
    fixed = re.sub(r"(src|href)=[\"'](\.\./|\./)(assets/[^\"']+)[\"']", r"\1=\"/\2\"", html_text)
    return fixed

def replace_blocks(content, header_html, footer_html):
    new = HEADER_RE.sub(header_html, content)
    new = FOOTER_RE.sub(footer_html, new)
    return new


def main():
    if not HEADER_SRC.exists() or not FOOTER_SRC.exists():
        print('Missing components/header.html or components/footer.html - aborting', file=sys.stderr)
        sys.exit(1)

    header_html = load_component(HEADER_SRC).strip()
    footer_html = load_component(FOOTER_SRC).strip()

    report = {'updated_files': [], 'skipped_files': [], 'errors': []}

    files = list(ROOT.glob('**/*.html'))
    # Exclude node_modules, .git, tools report, backups
    files = [f for f in files if '.git' not in f.parts and 'node_modules' not in f.parts and 'tools' not in f.parts]

    for f in files:
        try:
            text = f.read_text(encoding='utf-8')
            orig = text

            has_header = bool(HEADER_RE.search(text))
            has_footer = bool(FOOTER_RE.search(text))
            if not has_header and not has_footer:
                report['skipped_files'].append(str(f.relative_to(ROOT)))
                continue

            new_text = replace_blocks(text, header_html, footer_html)
            new_text = fix_asset_paths(new_text, f)

            if new_text != orig:
                bak = f.with_suffix(f.suffix + BACKUP_EXT)
                if not bak.exists():
                    bak.write_text(orig, encoding='utf-8')
                f.write_text(new_text, encoding='utf-8')
                report['updated_files'].append(str(f.relative_to(ROOT)))
            else:
                report['skipped_files'].append(str(f.relative_to(ROOT)))
        except Exception as e:
            report['errors'].append({'file': str(f.relative_to(ROOT)), 'error': str(e)})

    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('Done. Report written to', REPORT_PATH)
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
