from pathlib import Path

replacements = {
    'â€”': '—',
    'â€¦': '…',
    'â†’': '→',
    'â€º': '›',
    'Â©': '©',
    'â‚¹': '₹',
    'Ã©': 'é',
    'DÃ©cor': 'Décor',
    'Ã—': '×',
    'â€“': '–',
    'â€˜': '‘',
    'â€™': '’',
    'â€œ': '“',
    'â€': '”',
    'â”€': '─',
    'Â ': ' ',
    'Â': '',
    'â€º': '›',
    'â„¢': '™',
}
root = Path('.')
count_files = 0
count_replacements = 0
for p in sorted(root.rglob('*.html')):
    text = p.read_text(encoding='utf-8', errors='replace')
    new_text = text
    for bad, good in replacements.items():
        new_text = new_text.replace(bad, good)
    if new_text != text:
        p.write_text(new_text, encoding='utf-8')
        count_files += 1
        count_replacements += sum(text.count(bad) for bad in replacements)
print(f'processed {count_files} files, {count_replacements} replacement candidates')
