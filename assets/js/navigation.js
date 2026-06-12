/* navigation.js — MPA Navigation & UI Logic
   Morning Star Infra Projects
   Handles: hamburger menu, header scroll shadow, mobile menu close on link click,
            active nav link highlighting.
   Does NOT intercept or prevent any <a href> navigation — links work natively.
   Note: openModal / closeModal are defined in main.min.js (from forms.js merge). */

'use strict';

(function () {

  // Single init guard to prevent duplicate event binding per header instance
  function initHeaderBehavior() {
    var siteHeader = document.getElementById('site-header');
    if (!siteHeader) return;
    if (siteHeader.dataset.navInitialized === '1') return;

    var hamburger  = document.getElementById('hamburger');
    var mobileMenu = document.getElementById('mobile-menu');

    // Hamburger toggle
    if (hamburger && mobileMenu) {
      try { hamburger.disabled = false; } catch (e) {}
      if (hamburger.style) { hamburger.style.zIndex = hamburger.style.zIndex || '1202'; hamburger.style.position = hamburger.style.position || 'relative'; }

      var toggleMenu = function () {
        var isOpen = mobileMenu.classList.toggle('open');
        hamburger.classList.toggle('is-active', isOpen);
        hamburger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        mobileMenu.setAttribute('aria-hidden', isOpen ? 'false' : 'true');
        document.body.classList.toggle('menu-open', isOpen);
      };

      hamburger.addEventListener('click', function (e) { e.preventDefault(); toggleMenu(); });
      hamburger.addEventListener('touchstart', function (e) { e.preventDefault(); toggleMenu(); }, { passive: false });
    }

    // Close mobile menu when any mobile link is clicked
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

    // Header scroll shadow
    window.addEventListener('scroll', function () {
      siteHeader.classList.toggle('scrolled', window.scrollY > 20);
    }, { passive: true });

    // Active nav link highlighting
    function highlightActiveLinks(){
      // remove previous active states first
      document.querySelectorAll('.nav-link.active, .drop-link.active, .mob-link.active').forEach(function(el){ el.classList.remove('active'); });
      var currentPath = window.location.pathname.toLowerCase();

      function setActiveByData(page){
        var nodes = document.querySelectorAll('[data-page="' + page + '"]');
        nodes.forEach(function(n){ n.classList.add('active'); });
      }

      // Home: exact root or index.html only
      if (currentPath === '/' || currentPath === '' || currentPath === '/index.html' || currentPath.endsWith('/index.html')){
        setActiveByData('home');
        return;
      }

      // Blog
      if (currentPath.indexOf('/blog/') !== -1 || currentPath.indexOf('/blog.html') !== -1){ setActiveByData('blog'); return; }

      // Our Story
      if (currentPath.indexOf('our-story') !== -1){ setActiveByData('story'); return; }

      // Our Team
      if (currentPath.indexOf('our-team') !== -1){ setActiveByData('team'); return; }

      // Certifications
      if (currentPath.indexOf('certifications') !== -1){ setActiveByData('certifications'); return; }

      // Divisions (mark specific drop-link and trigger)
      if (currentPath.indexOf('/home-construction') !== -1 || currentPath.indexOf('/commercial-and-industrial') !== -1 || currentPath.indexOf('/interior-fitouts') !== -1 || currentPath.indexOf('/structural-repair') !== -1){
        document.querySelectorAll('.nav-drop-menu a').forEach(function(a){
          try{
            var href = (a.getAttribute('href')||'').toLowerCase();
            if(href && currentPath.indexOf(href.replace(/^.*\//,'')) !== -1) a.classList.add('active');
          }catch(e){}
        });
        var dropTrigger = document.querySelector('.nav-drop-trigger'); if(dropTrigger) dropTrigger.classList.add('active');
        return;
      }

      // Fallback: exact filename match
      var file = currentPath.replace(/^.*\//,'');
      if(file){
        document.querySelectorAll('.nav-link, .drop-link, .mob-link').forEach(function(el){
          var h = (el.getAttribute('href')||'').split('?')[0].split('#')[0].replace(/^.*\//,'').toLowerCase();
          if(h && h === file) el.classList.add('active');
        });
      }
    }
    highlightActiveLinks();

    // Sync dropdown trigger aria-expanded with hover/focus state for accessibility
    function syncDropdownAria(){
      document.querySelectorAll('.nav-dropdown').forEach(function(dropdown){
        var trigger = dropdown.querySelector('.nav-drop-trigger');
        if(!trigger) return;

        var setExpanded = function(value){
          trigger.setAttribute('aria-expanded', value ? 'true' : 'false');
        };

        dropdown.addEventListener('mouseenter', function(){ setExpanded(true); });
        dropdown.addEventListener('mouseleave', function(){ setExpanded(false); });
        dropdown.addEventListener('focusin', function(){ setExpanded(true); });
        dropdown.addEventListener('focusout', function(e){
          if(!dropdown.contains(e.relatedTarget)) setExpanded(false);
        });
      });
    }
    syncDropdownAria();

    // Dynamic header height: set CSS variable --hdr-h
    function updateHeaderHeight(){
      var hdr = document.getElementById('site-header');
      if(!hdr) return;
      try{
        var h = Math.ceil(hdr.getBoundingClientRect().height);
        document.documentElement.style.setProperty('--hdr-h', h + 'px');
        document.documentElement.style.setProperty('--header-height', h + 'px');
      }catch(e){ /* ignore */ }
    }
    // Debounce helper
    function debounce(fn, wait){ var t; return function(){ var args = arguments; clearTimeout(t); t = setTimeout(function(){ fn.apply(null, args); }, wait); }; }
    window.addEventListener('load', updateHeaderHeight);
    window.addEventListener('resize', debounce(updateHeaderHeight, 120));
    // Use ResizeObserver when available to minimize layout thrash
    var hdrEl = document.getElementById('site-header');
    if (hdrEl && 'ResizeObserver' in window){
      try{
        var ro = new ResizeObserver(debounce(updateHeaderHeight, 120));
        ro.observe(hdrEl);
      }catch(e){ /* ignore */ }
    } else if (window.MutationObserver){
      var _hdr = document.getElementById('site-header');
      if (_hdr){
        var obs = new MutationObserver(debounce(function(){ updateHeaderHeight(); }, 120));
        obs.observe(_hdr, { childList: true, subtree: true, attributes: true });
      }
    }

    // mark initialized
    siteHeader.dataset.navInitialized = '1';
  }

  // Initialize when DOM is ready
  document.addEventListener('DOMContentLoaded', function(){ initHeaderBehavior(); });
  // Also ensure init after full load in case header modified by other scripts
  window.addEventListener('load', function(){ initHeaderBehavior(); });

  // Allow external tools to trigger initialization when header/footer injected
  window.addEventListener('site:header:ready', function(){ initHeaderBehavior(); });

})();
