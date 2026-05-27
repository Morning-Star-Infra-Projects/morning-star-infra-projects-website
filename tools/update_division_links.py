#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
patterns = [
    # href variants -> canonical path
    (re.compile(r'href=("|\')(?:\.\./)?pages?/home-construction\.html("|\')', re.IGNORECASE), 'href="/residential/"'),
    (re.compile(r'href=("|\')pages?/home-construction\.html("|\')', re.IGNORECASE), 'href="/residential/"'),
    (re.compile(r'href=("|\')(?:\.\./)?pages?/interior-fitouts\.html("|\')', re.IGNORECASE), 'href="/interiors/"'),
    (re.compile(r'href=("|\')pages?/interior-fitouts\.html("|\')', re.IGNORECASE), 'href="/interiors/"'),
    (re.compile(r'href=("|\')(?:\.\./)?pages?/structural-repair\.html("|\')', re.IGNORECASE), 'href="/structural/"'),
    (re.compile(r'href=("|\')pages?/structural-repair\.html("|\')', re.IGNORECASE), 'href="/structural/"'),
    (re.compile(r'href=("|\')(?:\.\./)?pages?/commercial-and-industrial\.html("|\')', re.IGNORECASE), 'href="/industrial/"'),
    (re.compile(r'href=("|\')pages?/commercial-and-industrial\.html("|\')', re.IGNORECASE), 'href="/industrial/"'),
    # some filenames without pages/ prefix
    (re.compile(r'href=("|\')(?:\.\./)?home-construction\.html("|\')', re.IGNORECASE), 'href="/residential/"'),
    (re.compile(r'href=("|\')(?:\.\./)?interior-fitouts\.html("|\')', re.IGNORECASE), 'href="/interiors/"'),
    (re.compile(r'href=("|\')(?:\.\./)?structural-repair\.html("|\')', re.IGNORECASE), 'href="/structural/"'),
    (re.compile(r'href=("|\')(?:\.\./)?commercial-and-industrial\.html("|\')', re.IGNORECASE), 'href="/industrial/"'),
]

text_replacements = [
    (re.compile(r'Structural Repair\s*&\s*Retrofitting', re.IGNORECASE), 'Structural Repair'),
]

def process_file(path: Path):
    text = path.read_text(encoding='utf-8')
    orig = text
    for pat, repl in patterns:
        text = pat.sub(repl, text)
    for pat, repl in text_replacements:
        text = pat.sub(repl, text)
    if text != orig:
        bak = path.with_suffix(path.suffix + '.bak')
        if not bak.exists():
            bak.write_text(orig, encoding='utf-8')
        path.write_text(text, encoding='utf-8')
        return True
    return False

def main():
    html_files = list(ROOT.rglob('*.html'))
    changed = []
    for f in html_files:
        try:
            if process_file(f):
                changed.append(str(f.relative_to(ROOT)))
        except Exception as e:
            print(f'ERROR {f}: {e}')
    print(f'Scanned HTML files: {len(html_files)}')
    print(f'Files modified: {len(changed)}')
    for c in changed:
        print(c)

if __name__ == '__main__':
    main()
