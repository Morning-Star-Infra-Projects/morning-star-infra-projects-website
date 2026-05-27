
# ============================================================
# rollout-header-footer.ps1
# Apply header/footer upgrades to all pages/*.html files
# ============================================================

$pagesDir = "c:\Users\PRABHAKAR\OneDrive\Documents\HEHE-2\pages"
$files = Get-ChildItem -Path $pagesDir -Filter "*.html" |
         Where-Object { $_.Name -notin @("contact.html") }

$topStrip = @'
<!-- TOP CONTACT STRIP (desktop only) -->
<div id="top-strip">
  <div class="top-strip-inner">
    <span>&#128205; Chennai, Tamil Nadu</span>
    <a href="tel:+918098889984">&#128222; +91-8098889984</a>
    <a href="mailto:morningstarinfra@gmail.com">&#9993; morningstarinfra@gmail.com</a>
    <a href="https://wa.me/918098889984" target="_blank" rel="noopener noreferrer">&#128172; WhatsApp</a>
  </div>
</div>
'@

$mobileMenuPages = @'
<div aria-hidden="true" class="mobile-menu" id="mobile-menu">
  <span class="mob-section-label">Pages</span>
  <a class="mob-link" href="../index.html">Home</a>
  <a class="mob-link" href="our-story.html">Our Story</a>
  <a class="mob-link" href="our-team.html">Our Team</a>
  <a class="mob-link" href="certifications.html">Certifications</a>
  <a class="mob-link" href="blog.html">Blog</a>
  <hr class="mob-divider">
  <span class="mob-section-label">Divisions</span>
  <a class="mob-link" href="home-construction.html">&#127968; Home Construction</a>
  <a class="mob-link" href="commercial-and-industrial.html">&#127981; Commercial &amp; Industrial</a>
  <a class="mob-link" href="interior-fitouts.html">&#128715; Interior Fitouts</a>
  <a class="mob-link" href="structural-repair.html">&#128295; Structural Repair</a>
  <hr class="mob-divider">
  <span class="mob-section-label">Contact</span>
  <a class="mob-cta" href="tel:+918098889984"><i data-lucide="phone" style="width:1em;height:1em"></i> Call Now &#8212; +91-8098889984</a>
</div>
'@

$trustAndAreas = @'
<!-- TRUST BADGES -->
<div class="footer-trust">
  <div class="footer-trust-item">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
    Post-Graduate Engineers
  </div>
  <div class="footer-trust-item">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
    Form B &amp; Form C Authority
  </div>
  <div class="footer-trust-item">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
    Licensed Structural Consultants
  </div>
  <div class="footer-trust-item">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
    NDT Certified
  </div>
  <div class="footer-trust-item">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
    Transparent Pricing Guarantee
  </div>
</div>
<!-- SERVICE AREAS -->
<div class="footer-trust" style="border-top:1px solid rgba(255,255,255,.05);padding-top:14px;margin-top:0">
  <div style="width:100%;font-size:.7rem;font-weight:700;letter-spacing:.12em;color:rgba(255,255,255,.4);text-transform:uppercase;margin-bottom:6px">Service Areas</div>
  <div class="footer-seo-links" style="border:none;padding:0;margin:0">
    <a href="home-construction.html">Home Construction Chennai</a>
    <a href="home-construction.html">Construction in Anna Nagar</a>
    <a href="home-construction.html">Construction in Velachery</a>
    <a href="home-construction.html">Construction in OMR</a>
    <a href="home-construction.html">Construction in Tambaram</a>
    <a href="structural-repair.html">Structural Repair Chennai</a>
    <a href="interior-fitouts.html">Interior Designers Chennai</a>
    <a href="commercial-and-industrial.html">Commercial Construction Chennai</a>
  </div>
</div>
<!-- FOOTER BOTTOM -->
'@

$results = @()

foreach ($file in $files) {
    $name = $file.Name
    $path = $file.FullName
    $content = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
    $changed = $false

    # 1. Top contact strip — insert before <header id="site-header">
    if ($content -notmatch 'id="top-strip"') {
        $content = $content -replace '(<header id="site-header">)', "$topStrip`$1"
        $changed = $true
        Write-Host "[$name] + top-strip"
    }

    # 2. Get Free Quote nav CTA — insert after Blog link, before </nav>
    if ($content -notmatch 'nav-quote-cta') {
        $content = $content -replace '(<a class="nav-link" href="blog\.html">Blog</a>)\s*\r?\n\s*(</nav>)', '$1
<button class="nav-quote-cta" onclick="openModal()">&#10022; Get Free Quote</button>
$2'
        $changed = $true
        Write-Host "[$name] + nav-quote-cta"
    }

    # 3. Replace mobile menu div (entire block from open to close)
    if ($content -notmatch 'mob-section-label') {
        # Match from opening of mobile-menu div to its closing div tag
        $content = $content -replace '(?s)<div aria-hidden="true" class="mobile-menu" id="mobile-menu">.*?</div>(?=\s*\r?\n\s*</header>)', $mobileMenuPages
        $changed = $true
        Write-Host "[$name] + grouped mobile menu"
    }

    # 4. Trust badges + service areas — insert before <div class="footer-bottom">
    if ($content -notmatch 'footer-trust') {
        $content = $content -replace '<div class="footer-bottom">', $trustAndAreas + '<div class="footer-bottom">'
        $changed = $true
        Write-Host "[$name] + trust badges + service areas"
    }

    if ($changed) {
        [System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::UTF8)
        $results += "UPDATED: $name"
    } else {
        $results += "SKIPPED: $name (already up to date)"
    }
}

Write-Host "`n=== ROLLOUT COMPLETE ==="
$results | ForEach-Object { Write-Host $_ }
