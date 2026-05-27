from pathlib import Path
from playwright.sync_api import sync_playwright

PAGES = [
    "index.html",
    "blog-3/how-to-find-the-best-industrial-construction-in-chennai.html",
    "blog-1/affordable-architects-india-for-peb-buildings.html",
    "blog-4/top-rated-structural-engineers-in-chennai.html",
    "blog-5/top-rated-structural-planning-in-india-pricing-guide.html",
    "blog-6/which-is-the-top-interior-fitouts-in-chennai.html",
    "blog-3/how-to-find-the-best-infrastructure-company-in-chennai.html",
]

OUTPUT_DIR = Path("screenshots")
OUTPUT_DIR.mkdir(exist_ok=True)

VIEWPORTS = {
    "mobile": 375,
    "tablet": 768,
    "desktop": 1200,
}

base = Path(__file__).resolve().parent.parent

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    for rel in PAGES:
        path = base / rel
        if not path.exists():
            print(f"Skipping missing: {rel}")
            continue
        url = f"file:///{path.as_posix()}"
        for name, w in VIEWPORTS.items():
            page.set_viewport_size({"width": w, "height": 900})
            page.goto(url)
            page.wait_for_timeout(600)
            safe_name = rel.replace('/', '_')
            out = OUTPUT_DIR / f"{safe_name}_{name}.png"
            page.screenshot(path=str(out), full_page=True)
            print(f"Saved {out}")

    browser.close()
