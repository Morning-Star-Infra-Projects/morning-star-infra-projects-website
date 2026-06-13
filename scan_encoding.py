#!/usr/bin/env python3
import os
import re

# Patterns for double-encoded UTF-8 mojibake
patterns = {
    'em_dash': r'â€"',          # em-dash (—)
    'ellipsis': r'â€¦',         # ellipsis (…)
    'copyright': r'Â©',         # copyright (©)
    'accented_e': r'Ã©',        # é
    'accented_a': r'Ã¡',        # á
    'accented_i': r'Ã®',        # î
    'accented_o': r'Ã´',        # ô
    'accented_u': r'Ã»',        # û
    'trademark': r'â„¢',        # ™
    'apostrophe': r'â€™',       # '
    'left_quote': r'â€œ',       # "
    'right_quote': r'â€\x9d',   # "
    'rupee': r'â‚¹',            # ₹
}

html_files = []
for root, dirs, files in os.walk('.'):
    if '.git' not in root and 'node_modules' not in root:
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))

print(f"Scanning {len(html_files)} HTML files...\n")

issues_found = {}
for filepath in sorted(html_files):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        file_issues = {}
        for pattern_name, pattern in patterns.items():
            matches = list(re.finditer(pattern, content))
            if matches:
                file_issues[pattern_name] = len(matches)
        
        if file_issues:
            issues_found[filepath] = file_issues
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

if issues_found:
    print("=" * 70)
    print("ENCODING ISSUES DETECTED\n")
    for filepath, issues in sorted(issues_found.items()):
        print(f"File: {filepath}")
        for pattern_name, count in issues.items():
            print(f"  - {pattern_name}: {count} occurrence(s)")
        print()
else:
    print("=" * 70)
    print("✓ CLEAN SCAN: No double-encoded UTF-8 mojibake found")
    print("\nAll HTML files are properly encoded with valid UTF-8 characters.")
    print("=" * 70)
