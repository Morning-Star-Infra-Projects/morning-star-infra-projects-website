#!/usr/bin/env python3
"""
extend_blogs.py
Generate N additional SEO blog pages and update pages/blog.html
Run from workspace root.
"""
import os, re, random
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = ROOT / 'pages'
BLOG_DIR = PAGES_DIR / 'blog'
CSS_PATH = ROOT / 'assets' / 'css' / 'blog.generated.css'

os.makedirs(BLOG_DIR, exist_ok=True)

# load existing entries
existing = []
for p in sorted(BLOG_DIR.glob('*.html')):
    existing.append(p.name)

EXISTING_SLUGS = {p.stem for p in BLOG_DIR.glob('*.html')}

# utilities

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s-]", '', s)
    s = re.sub(r"[\s-]+", '-', s).strip('-')
    return s

random.seed(2026)

PRIMARY = 'Morning Star Infra Projects'
LOC = ['Chennai', 'Tamil Nadu', 'India']
SERVICES = [
    'Construction Company', 'Home Builders', 'Building Contractors', 'Architects', 'Infrastructure Company',
    'Commercial Construction', 'Industrial Construction', 'Interior Fitouts', 'Structural Engineers', 'Civil Engineering Company'
]
INTENTS = [
    'Best', 'Top', 'How to Choose', 'Affordable', 'Trusted', 'Leading', 'Modern', 'Top-Rated', 'Compare', 'Who Is the Best', 'Why Hire'
]
LONGTAIL_TEMPLATES = [
    '{prefix} {service} in {loc}',
    '{prefix} {service} near me in {loc}',
    '{prefix} {service} {loc} for {focus}',
    '{prefix} {service} in {loc}: {angle}',
    '{question} {service} in {loc}',
]
FOCUS = ['residential projects', 'commercial projects', 'industrial warehouses', 'luxury homes', 'budget homes', 'PEB buildings', 'retrofitting services', 'structural planning']
ANGLE = ['pricing guide', 'what to expect', 'quality checklist', 'timeline & costs', 'materials & standards']
QUESTIONS = ['Who is the best', 'Which is the top', 'How to find the best', 'Where to hire the best']

# target number of new pages
N = 500

# gather base pool for titles to avoid duplicates
base_titles = [
    'Sustainable Construction Practices in Chennai',
    'How Morning Star Ensures Structural Safety in Chennai',
    'Cost Breakdown: Building a Home in Chennai',
    'Renovation vs Rebuild: Advice for Chennai Homeowners',
    'Turnkey Interior Fitouts — Chennai Case Studies',
    'Industrial Warehouse Construction: Chennai Checklist',
    'PEB Buildings in Tamil Nadu — Benefits & Costs',
    'Retrofitting Heritage Buildings in Chennai',
    'Choosing Materials for Coastal Chennai Projects',
    'Site Supervision Tips for Homeowners in Chennai'
]

# ensure uniqueness
new_titles = []
attempts = 0
while len(new_titles) < N and attempts < N * 10:
    attempts += 1
    tmpl = random.choice(LONGTAIL_TEMPLATES)
    prefix = random.choice(INTENTS)
    service = random.choice(SERVICES + ['building design', 'structural planning', 'site supervision'])
    loc = random.choice(LOC)
    focus = random.choice(FOCUS)
    angle = random.choice(ANGLE)
    question = random.choice(QUESTIONS)
    title = tmpl.format(prefix=prefix, service=service, loc=loc, focus=focus, angle=angle, question=question)
    # sometimes use base titles
    if random.random() < 0.06:
        title = random.choice(base_titles)
    if title not in new_titles:
        slug = slugify(title)
        if slug in EXISTING_SLUGS:
            # tweak
            title = f"{title} — {random.choice(['Morning Star','Chennai'])}"
            slug = slugify(title)
        if slug in EXISTING_SLUGS or slug in {slugify(t) for t in new_titles}:
            continue
        new_titles.append(title)

# create entries list combining existing and new
existing_entries = []
for p in sorted(BLOG_DIR.glob('*.html')):
    existing_entries.append({'filename': p.name, 'title': None})

new_entries = []
start_id = len(existing_entries) + 1
for i, title in enumerate(new_titles, start=start_id):
    slug = slugify(title)
    filename = f"{slug}.html"
    path = BLOG_DIR / filename
    new_entries.append({'id': i, 'title': title, 'slug': slug, 'filename': filename, 'path': path})

# helper to generate paragraph
PARA_POOL = [
    'Our engineering team in Chennai focuses on durable materials and transparent costing so homeowners can make informed decisions.',
    'We combine post-graduate structural engineering with practical site supervision to ensure timelines and budgets are respected.',
    'Every project is governed by a transparent BOQ and milestone payments to reduce ambiguity and build trust.',
    'Material choices follow IS codes and manufacturer certifications — ensuring long-term performance in coastal Chennai climates.',
    'Our project managers provide weekly photo updates and a single point of contact to simplify communication.'
]

def generate_paragraph(seed, target_words=140):
    random.seed(seed)
    parts = []
    while sum(len(p.split()) for p in parts) < target_words:
        parts.append(random.choice(PARA_POOL))
    return ' '.join(parts)

# header/footer snippets (match existing pattern)
HEADER_SNIPPET = '''<!doctype html>
<html lang="en-IN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <link rel="stylesheet" href="../assets/css/main.min.css">
  <link rel="stylesheet" href="../assets/css/components.css">
  <link rel="stylesheet" href="../assets/css/blog.generated.css">
'''
FOOTER_SNIPPET = '''\n  <footer id="site-footer">\n    <div class="container">\n      <div class="footer-grid">\n        <div class="footer-brand">\n          <p>Morning Star Infra Projects — Chennai-based civil engineering & construction.</p>\n        </div>\n      </div>\n    </div>\n  </footer>\n</body>\n</html>'''

# write pages
all_entries = []
# collect existing titles if possible by reading file title
for p in sorted(BLOG_DIR.glob('*.html')):
    try:
        txt = p.read_text(encoding='utf-8')
        m = re.search(r'<h1>(.*?)</h1>', txt)
        title = m.group(1).strip() if m else p.stem.replace('-', ' ').title()
    except Exception:
        title = p.stem.replace('-', ' ').title()
    all_entries.append({'filename': p.name, 'title': title, 'slug': p.stem})

# create new files
for e in new_entries:
    title = e['title']
    filename = e['filename']
    path = e['path']
    date = datetime.now().strftime('%B %Y')
    # sections
    sections = ['Introduction', 'Industry Overview', 'Benefits', 'Why Choose Morning Star Infra Projects', 'Detailed Explanation', 'Project Expertise', 'Construction Process', 'Modern Technologies Used', 'Case Examples', 'Practical Tips', 'Conclusion']
    html_sections = []
    for idx, sec in enumerate(sections):
        p = generate_paragraph(e['id'] + idx, target_words= max(100, random.randint(120,180)))
        html_sections.append({'sec': sec, 'p': p})
    faqs = [
        ('What is the typical timeline for a residential build in Chennai?', 'We start with a diagnostic and a transparent BOQ; our answers are tailored per project.'),
        ('How do you ensure material quality on site?', 'We follow IS codes and inspect materials on delivery and at installation.'),
        ('Do you handle approvals?', 'We assist with approvals and coordinate with authorities.'),
    ]
    # related: pick 3 random from existing + new
    pool = all_entries + new_entries
    pool_titles = [x for x in pool if x.get('filename') != filename]
    random.shuffle(pool_titles)
    related = pool_titles[:3]
    # build html
    article_html = [HEADER_SNIPPET]
    article_html.append(f'  <title>{title} | Morning Star Infra Projects</title>')
    article_html.append(f'  <meta name="description" content="{title} — Expert insights by Morning Star Infra Projects in Chennai">')
    article_html.append('</head>\n<body>')
    article_html.append(f'<nav class="breadcrumb"><div class="container"><a href="../index.html">Home</a> › <a href="../blog.html">Blog</a> › <span aria-current="page">{title}</span></div></nav>')
    img_src = '../assets/images/hero_brand-800.webp'
    article_html.append(f'<main class="article-content"><header><h1>{title}</h1><img class="article-hero" src="{img_src}" alt="{title} — Morning Star Infra Projects" loading="lazy"></header>')
    for s in html_sections:
        article_html.append(f'<section><h2>{s['sec']}</h2><p>{s['p']}</p></section>')
    article_html.append('<section class="cta" style="text-align:center;margin:28px 0;padding:18px;background:linear-gradient(90deg,var(--primary),var(--navy));color:white;border-radius:12px"><h3>Ready to discuss your project?</h3><p>Contact Morning Star Infra Projects for a free site assessment and transparent quote.</p><p><a class="btn-primary" href="../pages/home-construction.html">Request a Free Quote</a> <a class="btn-secondary" href="../pages/contact.html">Contact Us</a></p></section>')
    article_html.append('<section><h2>Frequently Asked Questions</h2>')
    for q,a in faqs:
        article_html.append(f'<div class="faq-item"><strong>{q}</strong><p>{a}</p></div>')
    article_html.append('</section>')
    article_html.append('<section><h2>Related Posts</h2><div class="related-posts">')
    for r in related:
        # related may be dicts with different keys
        if isinstance(r, dict):
            fname = r.get('filename') or r.get('filename')
            t = r.get('title') or r.get('title')
            article_html.append(f'<a href="{fname}">{t}</a>')
    article_html.append('</div></section>')
    article_html.append('<nav class="internal-links">')
    article_html.append('<a href="../index.html">Home</a> | <a href="../pages/our-story.html">About Us</a> | <a href="../pages/home-construction.html">Projects</a> | <a href="../pages/contact.html">Contact</a> | <a href="../pages/home-construction.html">Services</a>')
    article_html.append('</nav>')
    article_html.append(FOOTER_SNIPPET)
    try:
        path.write_text('\n'.join(article_html), encoding='utf-8')
        all_entries.append({'filename': filename, 'title': title, 'slug': e['slug']})
    except Exception as ex:
        print('Failed to write', path, ex)

print(f'Created {len(new_entries)} new blog pages')

# regenerate blog index with all entries
cards = []
for i,entry in enumerate(all_entries, start=1):
    title = entry['title']
    fname = entry['filename']
    excerpt = generate_paragraph(i, target_words=40).split()[:30]
    excerpt = ' '.join(excerpt) + '...'
    card = f'''<article class="blog-card">\n  <img src="../assets/images/hero_brand-800.webp" alt="{title}" loading="lazy">\n  <div class="blog-card-body">\n    <span class="blog-tag">BLOG</span>\n    <h3 class="blog-card-title"><a href="blog/{fname}">{title}</a></h3>\n    <p>{excerpt}</p>\n  </div>\n</article>'''
    cards.append(card)

index_html = f'''<!doctype html>\n<html lang="en-IN">\n<head>\n<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n<link rel="stylesheet" href="../assets/css/main.min.css">\n<link rel="stylesheet" href="../assets/css/components.css">\n<link rel="stylesheet" href="../assets/css/blog.generated.css">\n<title>Blog | Morning Star Infra Projects</title>\n<meta name="description" content="Construction guides and case studies from Morning Star Infra Projects in Chennai">\n</head>\n<body>\n<header><!-- minimal header omitted for brevity --></header>\n<main id=\"blog-index\" class="container" style="padding-top:calc(var(--hdr-h) + 16px)">\n  <h1>Morning Star Blog — Construction Guides & Case Studies</h1>\n  <div class="blog-grid">\n    {'\n'.join(cards)}\n  </div>\n</main>\n<footer></footer>\n</body>\n</html>'''

(BLOG_INDEX := PAGES_DIR / 'blog.html').write_text(index_html, encoding='utf-8')
print('Updated pages/blog.html with total entries:', len(all_entries))
