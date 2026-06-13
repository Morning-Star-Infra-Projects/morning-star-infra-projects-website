from pathlib import Path
import re

BOOTSTRAP_PAT = re.compile(r'[âÃÂ]')
MAL_PAT = re.compile(r'â€”|â€¦|Â©|â‚¹|â†’|â€º|Ã©|DÃ©cor|Ã—|â€“|â€˜|â€™|â€œ|â€|â”€|â„¢')

root = Path('.')
processed = 0
fixed_files = []
for p in sorted(root.rglob('*.html')):
    b = p.read_bytes()
    try:
        text = b.decode('utf-8')
    except Exception:
        text = b.decode('utf-8', errors='replace')
    if not BOOTSTRAP_PAT.search(text):
        continue
    # attempt double-encoding repair: encode as latin-1 then decode utf-8
    try:
        repaired = text.encode('latin-1', errors='replace').decode('utf-8', errors='replace')
    except Exception:
        repaired = text
    orig_count = len(MAL_PAT.findall(text))
    repaired_count = len(MAL_PAT.findall(repaired))
    processed += 1
    if repaired != text and repaired_count < orig_count:
        bak = p.with_name(p.name + '.bak')
        if not bak.exists():
            bak.write_bytes(b)
        p.write_text(repaired, encoding='utf-8')
        fixed_files.append((str(p), orig_count, repaired_count))

print(f'processed files with suspect sequences: {processed}')
print(f'fixed files: {len(fixed_files)}')
for fn, before, after in fixed_files:
    print(fn, '->', before, '->', after)
