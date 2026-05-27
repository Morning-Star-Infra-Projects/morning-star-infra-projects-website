/* animations.js — Scroll Reveal & Image Blur-Up */

'use strict';

// IntersectionObserver for .reveal elements
(function initReveal() {
  if (!('IntersectionObserver' in window)) {
    document.querySelectorAll('.reveal').forEach(el => el.classList.add('in-view'));
    return;
  }
  const obs = new IntersectionObserver(function(entries) {
    entries.forEach(function(e) {
      if (e.isIntersecting) { e.target.classList.add('in-view'); obs.unobserve(e.target); }
    });
  }, { root: null, rootMargin: '0px 0px -10% 0px', threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach(el => obs.observe(el));
})();

// Blur-up helper for hero and division tab images
(function initBlurUp() {
  try {
    const imgs = document.querySelectorAll('.hero-bg img, .div-tab-bg img, .hero-split-right img, .div-tab-media img');
    imgs.forEach(img => {
      if (img.complete && img.naturalWidth) {
        img.classList.add('loaded');
      } else {
        img.addEventListener('load',  () => img.classList.add('loaded'), { once: true });
        img.addEventListener('error', () => img.classList.add('loaded'), { once: true });
      }
    });
  } catch(e) { console.warn('blur-up init failed', e); }
})();

// Showcase carousel removed
