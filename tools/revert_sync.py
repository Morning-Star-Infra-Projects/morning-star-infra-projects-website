#!/usr/bin/env python3
"""
revert_sync.py

Restores any files that were backed up with the .orig.bak suffix by
`sync_header_footer.py`. It will overwrite the current file with the backup
and remove the backup file. It also removes the report file if present.

Usage: python tools/revert_sync.py
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
backups = list(ROOT.rglob('*.orig.bak'))
if not backups:
    print('No .orig.bak files found. Nothing to revert.')
    sys.exit(0)
restored = []
for b in backups:
    orig = b.with_suffix('')
    try:
        data = b.read_text(encoding='utf-8')
        orig.write_text(data, encoding='utf-8')
        b.unlink()
        restored.append(str(orig.relative_to(ROOT)))
    except Exception as e:
        print('Failed to restore', b, e)

report = ROOT / 'tools' / 'sync_header_footer_report.json'
if report.exists():
    try:
        report.unlink()
        print('Removed report:', report)
    except:
        pass

print('Restored files:')
for r in restored:
    print('-', r)
