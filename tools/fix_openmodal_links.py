#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
PAT = re.compile(r'<a\s+([^>]*?)onclick\s*=\s*("|\')\s*openModal\s*\(\s*\)\s*;?\s*("|\')([^>]*)>', re.IGNORECASE)

def fix_text(text: str) -> str:
    def repl(m):
        before = m.group(1) or ''
        after = m.group(4) or ''
        # if an href already present, just keep it and add return false
        if re.search(r'href\s*=\s*("|\')', before+after, re.IGNORECASE):
            return f'<a {before}onclick="openModal();return false;"{after}>'
        return f'<a {before}href="#quote" onclick="openModal();return false;"{after}>'
    return PAT.sub(repl, text)

def process_file(p: Path):
    s = p.read_text(encoding='utf-8')
    ns = fix_text(s)
    if ns != s:
        bak = p.with_suffix(p.suffix + '.bak')
        if not bak.exists():
            bak.write_text(s, encoding='utf-8')
        p.write_text(ns, encoding='utf-8')
        return True
    return False

def main():
    htmls = list(ROOT.rglob('*.html'))
    changed = []
    for f in htmls:
        try:
            if process_file(f):
                changed.append(str(f.relative_to(ROOT)))
        except Exception as e:
            print('ERROR', f, e)
    print('Scanned HTML files:', len(htmls))
    print('Files modified:', len(changed))
    for c in changed:
        print(c)

if __name__ == '__main__':
    main()
