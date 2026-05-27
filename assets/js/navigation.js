/* navigation.js — MPA Navigation & UI Logic
   Morning Star Infra Projects
   Handles: hamburger menu, header scroll shadow, mobile menu close on link click,
            active nav link highlighting.
   Does NOT intercept or prevent any <a href> navigation — links work natively.
   Note: openModal / closeModal are defined in main.min.js (from forms.js merge). */

'use strict';

(function () {

  // ── DOM refs ────────────────────────────────────────────────────────────────
  var hamburger  = document.getElementById('hamburger');
  var mobileMenu = document.getElementById('mobile-menu');
  var siteHeader = document.getElementById('site-header');

  // ── Hamburger toggle ────────────────────────────────────────────────────────────────────────────
  if (hamburger && mobileMenu) {
    // Defensive: ensure button is enabled and clickable
    try { hamburger.disabled = false; } catch (e) {}
    // Ensure visible stacking so it receives touch/clicks
    if (hamburger.style) { hamburger.style.zIndex = hamburger.style.zIndex || '1202'; hamburger.style.position = hamburger.style.position || 'relative'; }

    var toggleMenu = function () {
      var isOpen = mobileMenu.classList.toggle('open');
      // Visual state for hamburger (X animation)
      hamburger.classList.toggle('is-active', isOpen);
      hamburger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      mobileMenu.setAttribute('aria-hidden', isOpen ? 'false' : 'true');
      // Lock background scroll while menu is open
      document.body.classList.toggle('menu-open', isOpen);
    };

    hamburger.addEventListener('click', function (e) { e.preventDefault(); toggleMenu(); });
    // Some mobile browsers are more responsive to touchstart
    hamburger.addEventListener('touchstart', function (e) { e.preventDefault(); toggleMenu(); }, { passive: false });
  }

  // ── Close mobile menu when any mobile link is clicked ────────────────────────────────────
  if (mobileMenu) {
    mobileMenu.addEventListener('click', function (e) {
      var link = e.target.closest('a');
      if (link) {
        mobileMenu.classList.remove('open');
        if (hamburger) {
          hamburger.classList.remove('is-active');
          hamburger.setAttribute('aria-expanded', 'false');
        }
        mobileMenu.setAttribute('aria-hidden', 'true');
      }
    });
    // Close when clicking outside the menu
    document.addEventListener('click', function (e) {
      if (!mobileMenu.classList.contains('open')) return;
      var within = e.target.closest && (e.target.closest('#mobile-menu') || e.target.closest('#hamburger'));
      if (!within) {
        mobileMenu.classList.remove('open');
        if (hamburger) {
          hamburger.classList.remove('is-active');
          hamburger.setAttribute('aria-expanded', 'false');
        }
        mobileMenu.setAttribute('aria-hidden', 'true');
      }
    });
    // Close on Escape key
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && mobileMenu.classList.contains('open')) {
        mobileMenu.classList.remove('open');
        if (hamburger) {
          hamburger.classList.remove('is-active');
          hamburger.setAttribute('aria-expanded', 'false');
        }
        mobileMenu.setAttribute('aria-hidden', 'true');
      }
    });
    // Close when resizing to desktop (>= 769px)
    window.addEventListener('resize', function () {
      if (window.innerWidth >= 769 && mobileMenu.classList.contains('open')) {
        mobileMenu.classList.remove('open');
        if (hamburger) {
          hamburger.classList.remove('is-active');
          hamburger.setAttribute('aria-expanded', 'false');
        }
        mobileMenu.setAttribute('aria-hidden', 'true');
      }
    });
  }

  // ── Header scroll shadow ────────────────────────────────────────────────────
  if (siteHeader) {
    window.addEventListener('scroll', function () {
      siteHeader.classList.toggle('scrolled', window.scrollY > 20);
    }, { passive: true });
  }

  // ── Active nav link: highlight the link matching the current page ───────────
  var currentFile = window.location.pathname.replace(/^.*\//, '') || 'index.html';
  document.querySelectorAll('.nav-link, .drop-link, .mob-link').forEach(function (el) {
    var href = (el.getAttribute('href') || '').replace(/^.*\//, '');
    if (href && href === currentFile) {
      el.classList.add('active');
    }
  });

  // ── Dynamic header height: set CSS variable --hdr-h so pages reserve space
  function updateHeaderHeight(){
    var hdr = document.getElementById('site-header');
    if(!hdr) return;
    try{
      var h = Math.ceil(hdr.getBoundingClientRect().height);
      // set both variables so CSS and main content offset stay in sync
      document.documentElement.style.setProperty('--hdr-h', h + 'px');
      document.documentElement.style.setProperty('--header-height', h + 'px');
    }catch(e){ /* ignore */ }
  }
  // Run on load + resize
  window.addEventListener('load', updateHeaderHeight);
  window.addEventListener('resize', updateHeaderHeight);
  // Observe header changes (mobile menu toggles, logo swaps)
  if (window.MutationObserver){
    var _hdr = document.getElementById('site-header');
    if (_hdr){
      var obs = new MutationObserver(function(){ updateHeaderHeight(); });
      obs.observe(_hdr, { childList: true, subtree: true, attributes: true });
    }
  }

})();
