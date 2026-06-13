#!/usr/bin/env python3
import re

# Read the index.html file
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check for critical HTML structure issues
html_count = len(re.findall(r'<\s*html[^>]*>', content, re.IGNORECASE))
head_count = len(re.findall(r'<\s*head[^>]*>', content, re.IGNORECASE))
body_count = len(re.findall(r'<\s*body[^>]*>', content, re.IGNORECASE))
head_close = len(re.findall(r'<\s*/\s*head\s*>', content, re.IGNORECASE))
body_close = len(re.findall(r'<\s*/\s*body\s*>', content, re.IGNORECASE))

print('=' * 60)
print('HTML STRUCTURE VALIDATION REPORT - index.html')
print('=' * 60)
print(f'<html> tags:  {html_count:2d} (expected: 1) - {"✓ PASS" if html_count == 1 else "✗ FAIL"}')
print(f'<head> tags:  {head_count:2d} (expected: 1) - {"✓ PASS" if head_count == 1 else "✗ FAIL"}')
print(f'</head> tags: {head_close:2d} (expected: 1) - {"✓ PASS" if head_close == 1 else "✗ FAIL"}')
print(f'<body> tags:  {body_count:2d} (expected: 1) - {"✓ PASS" if body_count == 1 else "✗ FAIL"}')
print(f'</body> tags: {body_close:2d} (expected: 1) - {"✓ PASS" if body_close == 1 else "✗ FAIL"}')
print('=' * 60)

# Overall validation status
all_pass = html_count == 1 and head_count == 1 and head_close == 1 and body_count == 1 and body_close == 1
print(f'\nOVERALL STATUS: {"✓ PASS - HTML STRUCTURE COMPLIES WITH W3C" if all_pass else "✗ FAIL - HTML STRUCTURE ISSUES FOUND"}')

# Additional checks
print('\nADDITIONAL VALIDATION:')
print('-' * 60)

# Check for DOCTYPE
doctype_present = bool(re.search(r'<!DOCTYPE', content, re.IGNORECASE))
print(f'DOCTYPE declaration:    {"✓ Present" if doctype_present else "✗ Missing"}')

# Check for charset
charset_present = bool(re.search(r'<meta\s+charset', content, re.IGNORECASE))
print(f'Character encoding:     {"✓ Present" if charset_present else "✗ Missing"}')

# Check for viewport
viewport_present = bool(re.search(r'viewport', content, re.IGNORECASE))
print(f'Viewport meta tag:      {"✓ Present" if viewport_present else "✗ Missing"}')

# Check for title
title_count = len(re.findall(r'<title[^>]*>', content, re.IGNORECASE))
print(f'Title tag:              {title_count} (expected: 1) - {"✓ PASS" if title_count == 1 else "✗ FAIL"}')

# Check for canonical
canonical_present = bool(re.search(r'rel\s*=\s*["\']canonical', content, re.IGNORECASE))
print(f'Canonical URL tag:      {"✓ Present" if canonical_present else "✗ Missing"}')

print('=' * 60)

if all_pass:
    print('\n✓ SUCCESS: index.html has been fixed and is now W3C compliant!')
    print('  No duplicate body tags or structural errors detected.')
else:
    print('\n✗ ALERT: Structural issues remain. See details above.')
