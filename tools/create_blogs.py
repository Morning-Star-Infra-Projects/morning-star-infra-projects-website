#!/usr/bin/env python3
"""
create_blogs.py
Generates 100 SEO-optimized blog pages (HTML) and updates pages/blog.html with cards.
Run from workspace root.
"""
import os
import re
import random
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PAGES_DIR = os.path.join(ROOT, 'pages')
BLOG_DIR = os.path.join(PAGES_DIR, 'blog')
CSS_PATH = os.path.join(ROOT, 'assets', 'css', 'blog.generated.css')

os.makedirs(BLOG_DIR, exist_ok=True)

# Utilities

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s-]", '', s)
    s = re.sub(r"[\s-]+", '-', s).strip('-')
    return s

# Title generator: create a diverse set of 100 search-intent titles
PRIMARY = 'Morning Star Infra Projects'
LOC = ['Chennai', 'Tamil Nadu', 'India']
SERVICES = [
    'Construction Company', 'Home Builders', 'Building Contractors', 'Architects', 'Infrastructure Company',
    'Commercial Construction', 'Industrial Construction', 'Interior Fitouts', 'Structural Engineers', 'Civil Engineering Company'
]
INTENTS = [
    'Best', 'Top', 'How to Choose', 'Affordable', 'Trusted', 'Leading', 'Modern', 'Top-Rated', 'Compare', 'Who Is the Best'
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

random.seed(42)

titles = []
# start with some of the user's examples to anchor keywords
seed_examples = [
    'Best Construction Company in Chennai',
    'Top Infrastructure Company in Chennai',
    'Who Is the Best Construction Company in Chennai',
    'Affordable Construction Services in Chennai',
    'Top Building Contractors Near Me',
    'Modern Home Construction Company in Chennai',
    'Commercial Construction Experts in Chennai',
    'Industrial Infrastructure Company Chennai',
    'Best Architects in Chennai for Modern Homes',
    'Top Architectural Design Company in Chennai',
    'Best Infrastructure Designers in Chennai',
    'Top Civil Engineering Company in Chennai',
    'How to Choose a Construction Company in Chennai',
    'Best Residential Construction Company Near Me',
    'Trusted Construction Company in India',
    'Best Home Builders in Chennai',
    'Best Construction Companies for Commercial Projects',
    'Leading Infrastructure Developers in Chennai',
    'Top Architects for Luxury Home Design',
    'Best Structural Planning Company Chennai',
    'Construction Company with Modern Design Solutions',
    'Premium Building Construction Services Chennai',
    'Smart Infrastructure Solutions in Chennai',
    'Reliable Civil Contractors in Chennai',
    'Top-Rated Building Designers in Chennai'
]
for t in seed_examples:
    titles.append(t)

# generate until 100
while len(titles) < 100:
    tmpl = random.choice(LONGTAIL_TEMPLATES)
    prefix = random.choice(INTENTS)
    service = random.choice(SERVICES)
    loc = random.choice(LOC)
    focus = random.choice(FOCUS)
    angle = random.choice(ANGLE)
    question = random.choice(QUESTIONS)
    title = tmpl.format(prefix=prefix, service=service, loc=loc, focus=focus, angle=angle, question=question)
    # Clean duplicates and ensure variety
    if title not in titles:
        titles.append(title)

# Trim to 100
titles = titles[:100]

# Helper to create article HTML

def make_meta(title, slug, focus_keyword):
    meta_title = (title if len(title) <= 60 else title[:57] + '...')
    meta_desc = f"{title} — Expert insights by Morning Star Infra Projects. Learn costs, process, and why choose us."[:157]
    return meta_title, meta_desc

# small reusable header/footer to match site
HEADER_SNIPPET = '''<!doctype html>
<html lang="en-IN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <link rel="stylesheet" href="../assets/css/main.min.css">
  <link rel="stylesheet" href="../assets/css/components.css">
  <link rel="stylesheet" href="../assets/css/blog.generated.css">
'''
FOOTER_SNIPPET = '''
  <footer id="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <p>Morning Star Infra Projects — Chennai-based civil engineering & construction.</p>
        </div>
      </div>
    </div>
  </footer>
</body>
</html>'''

# Write CSS
css_content = '''
/* blog.generated.css - minimal styles for cards and article layout */
.blog-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:24px; }
@media(max-width:900px){ .blog-grid{grid-template-columns:1fr} }
.blog-card{ background:#fff;border-radius:12px;box-shadow:0 8px 20px rgba(10,31,68,.06); overflow:hidden; display:flex; flex-direction:column; }
.blog-card img{ width:100%; height:180px; object-fit:cover }
.blog-card-body{ padding:18px }
.blog-card-title{ font-size:1.05rem; margin:6px 0 }
.blog-tag{ font-weight:700; color:var(--primary); font-size:.8rem }
.blog-meta{ display:flex; gap:12px; align-items:center; margin-top:12px }
.article-hero{ width:100%; height:360px; object-fit:cover; border-radius:8px; }
.article-content{ max-width:900px; margin:18px auto; padding:0 18px }
.breadcrumb{ font-size:.95rem; margin-top:8px }
.related-posts{ display:flex; gap:12px; flex-wrap:wrap }
.related-posts a{ display:block; padding:10px 12px; background:var(--white); border-radius:8px; box-shadow:0 6px 18px rgba(10,31,68,.04) }
.faq-item{ margin-bottom:12px }
'''
with open(CSS_PATH, 'w', encoding='utf-8') as f:
    f.write(css_content)

# Precompute slugs
entries = []
for i, title in enumerate(titles, start=1):
    slug = slugify(title)
    filename = f"{slug}.html"
    path = os.path.join(BLOG_DIR, filename)
    entries.append({'title': title, 'slug': slug, 'filename': filename, 'path': path, 'id': i})

# Generate content for each entry

def generate_paragraph(seed, target_words=150):
    random.seed(seed)
    parts = []
    while sum(len(p.split()) for p in parts) < target_words:
        a = random.choice([
            'Our engineering team in Chennai focuses on durable materials and transparent costing so homeowners can make informed decisions.',
            'We combine post-graduate structural engineering with practical site supervision to ensure timelines and budgets are respected.',
            'Every project is governed by a transparent BOQ and milestone payments to reduce ambiguity and build trust.',
            'Material choices follow IS codes and manufacturer certifications — ensuring long-term performance in coastal Chennai climates.',
            'Our project managers provide weekly photo updates and a single point of contact to simplify communication.'
        ])
        parts.append(a)
    return ' '.join(parts)

for entry in entries:
    title = entry['title']
    slug = entry['slug']
    filename = entry['filename']
    path = entry['path']
    focus_keyword = title.split(' — ')[0]
    meta_title, meta_desc = make_meta(title, slug, focus_keyword)
    date = datetime.now().strftime('%B %Y')
    # compose article body by sections until approx 1400 words
    words_needed = random.randint(1250, 1600)
    # sections: intro, industry, benefits, why choose, detailed, expertise, process, tech, case examples, tips, conclusion
    sections = ['Introduction', 'Industry Overview', 'Benefits', 'Why Choose Morning Star Infra Projects', 'Detailed Explanation', 'Project Expertise', 'Construction Process', 'Modern Technologies Used', 'Case Examples', 'Practical Tips', 'Conclusion']
    html_sections = []
    accumulated = 0
    seed_base = entry['id']
    for idx, sec in enumerate(sections):
        # estimate 100-170 words per section
        tw = max(100, int(words_needed/len(sections) * (0.8 + random.random()*0.6)))
        p = generate_paragraph(seed_base + idx, target_words=tw)
        accumulated += len(p.split())
        html_sections.append({'sec': sec, 'p': p})
        if accumulated >= words_needed:
            break
    # FAQs 5-7
    num_faq = random.randint(5,7)
    faqs = []
    for q_i in range(num_faq):
        q = random.choice([
            'What is the typical timeline for a residential build in Chennai?',
            'How do you ensure material quality on site?',
            'Do you handle CMDA/DTCP approvals?',
            'What warranty do you provide for structural works?',
            'Can you provide turnkey interior fitouts?',
            'How are change requests handled during construction?',
            'Do you offer sustainable / green building options?'
        ])
        a = 'We start with a diagnostic and a transparent BOQ; our answers are tailored per project — typically we provide clear milestone-based timelines and warranty terms as part of the signed agreement.'
        faqs.append({'q': q, 'a': a})
    # related posts: pick 3 other entries
    related = [e for e in entries if e['slug'] != slug]
    random.shuffle(related)
    related = related[:3]

    # build HTML
    article_html = [HEADER_SNIPPET]
    article_html.append(f'  <title>{meta_title} | Morning Star Infra Projects</title>')
    article_html.append(f'  <meta name="description" content="{meta_desc}">')
    article_html.append('</head>\n<body>')
    # breadcrumb
    article_html.append('<nav class="breadcrumb"><div class="container"><a href="../index.html">Home</a> › <a href="../pages/blog.html">Blog</a> › <span aria-current="page">{}</span></div></nav>'.format(title))
    # hero image
    img_src = '../assets/images/hero_brand-800.webp'
    article_html.append(f'<main class="article-content"><header><h1>{title}</h1><div class="article-meta">📅 {date} • {random.randint(6,12)} min read</div><img class="article-hero" src="{img_src}" alt="{title} — Morning Star Infra Projects" loading="lazy"></header>')
    for s in html_sections:
        article_html.append(f'<section><h2>{s["sec"]}</h2><p>{s["p"]}</p></section>')
    # CTA
    article_html.append('<section class="cta" style="text-align:center;margin:28px 0;padding:18px;background:linear-gradient(90deg,var(--primary),var(--navy));color:white;border-radius:12px"><h3>Ready to discuss your project?</h3><p>Contact Morning Star Infra Projects for a free site assessment and transparent quote.</p><p><a class="btn-primary" href="../pages/home-construction.html">Request a Free Quote</a> <a class="btn-secondary" href="../pages/contact.html">Contact Us</a></p></section>')
    # FAQ
    article_html.append('<section><h2>Frequently Asked Questions</h2>')
    for faq in faqs:
        article_html.append(f'<div class="faq-item"><strong>{faq["q"]}</strong><p>{faq["a"]}</p></div>')
    article_html.append('</section>')
    # Related posts
    article_html.append('<section><h2>Related Posts</h2><div class="related-posts">')
    for r in related:
        article_html.append(f'<a href="{r["filename"]}">{r["title"]}</a>')
    article_html.append('</div></section>')
    # internal links
    article_html.append('<nav class="internal-links">')
    article_html.append('<a href="../index.html">Home</a> | <a href="../pages/our-story.html">About Us</a> | <a href="../pages/home-construction.html">Projects</a> | <a href="../pages/contact.html">Contact</a> | <a href="../pages/home-construction.html">Services</a>')
    article_html.append('</nav>')
    article_html.append(FOOTER_SNIPPET)

    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(article_html))

print(f"Generated {len(entries)} blog pages in {BLOG_DIR}")

# Update pages/blog.html to include cards for each article
BLOG_INDEX = os.path.join(PAGES_DIR, 'blog.html')

card_html = []
for e in entries:
    excerpt = ' '.join(generate_paragraph(e['id'], target_words=40).split()[:30]) + '...'
    card = f'''<article class="blog-card">
  <img src="../assets/images/hero_brand-800.webp" alt="{e['title']}" loading="lazy">
  <div class="blog-card-body">
    <span class="blog-tag">BLOG</span>
    <h3 class="blog-card-title"><a href="blog/{e['filename']}">{e['title']}</a></h3>
    <p>{excerpt}</p>
    <div class="blog-meta"><span>📅 {datetime.now().strftime('%b %Y')}</span><a class="blog-read-more" href="blog/{e['filename']}">Read →</a></div>
  </div>
</article>'''
    card_html.append(card)

index_html = f'''<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="../assets/css/main.min.css">
<link rel="stylesheet" href="../assets/css/components.css">
<link rel="stylesheet" href="../assets/css/blog.generated.css">
<title>Blog | Morning Star Infra Projects</title>
<meta name="description" content="Construction guides and case studies from Morning Star Infra Projects in Chennai">
</head>
<body>
<header><!-- minimal header omitted for brevity --></header>
<main class="container">
  <h1>Morning Star Blog — Construction Guides & Case Studies</h1>
  <div class="blog-grid">
    {'\n'.join(card_html)}
  </div>
</main>
<footer></footer>
</body>
</html>'''

with open(BLOG_INDEX, 'w', encoding='utf-8') as f:
    f.write(index_html)

print('Updated pages/blog.html')
''