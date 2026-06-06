// divisions-fix.js — robust mobile touch handling for division cards
(function(){
  'use strict';

  function navigateToTab(href) {
    try {
      const url = new URL(href, window.location.href);
      window.location.href = url.href;
    } catch (err) { /* ignore invalid URLs */ }
  }

  function init() {
    const track = document.getElementById('division-track');
    if (!track) return;

    // Small movement threshold (px) to distinguish taps from scrolls/drags
    const THRESHOLD = 10;

    // Track active pointers (support multiple touches defensively)
    const pointers = new Map();

    function clearPointer(id) {
      pointers.delete(id);
      // remove dragging marker after a short delay to allow events to settle
      setTimeout(() => track.classList.remove('is-dragging'), 40);
    }

    function onPointerDown(e) {
      if (window.innerWidth > 768) return;
      const tab = e.target && e.target.closest ? e.target.closest('.div-tab') : null;
      if (!tab) return;
      const id = (typeof e.pointerId !== 'undefined') ? e.pointerId : 'mouse';
      pointers.set(id, { startX: e.clientX, startY: e.clientY, moved: false, target: tab, startTime: Date.now() });
      try { if (e.target.setPointerCapture) e.target.setPointerCapture(e.pointerId); } catch (err){}
    }

    function onPointerMove(e) {
      const id = (typeof e.pointerId !== 'undefined') ? e.pointerId : 'mouse';
      const st = pointers.get(id);
      if (!st) return;
      const dx = Math.abs(e.clientX - st.startX);
      const dy = Math.abs(e.clientY - st.startY);
      if (!st.moved && (dx > THRESHOLD || dy > THRESHOLD)) {
        st.moved = true;
        track.classList.add('is-dragging');
      }
    }

    function onPointerUp(e) {
      if (window.innerWidth > 768) return;
      const id = (typeof e.pointerId !== 'undefined') ? e.pointerId : 'mouse';
      const st = pointers.get(id);
      if (!st) return clearPointer(id);
      const href = st.target && st.target.getAttribute ? st.target.getAttribute('href') : null;
      const moved = st.moved;
      clearPointer(id);
      try { if (e.target.releasePointerCapture) e.target.releasePointerCapture(e.pointerId); } catch (err){}
      if (moved) return; // user was scrolling/dragging — do not navigate
      if (href) navigateToTab(href);
    }

    function onPointerCancel(e) {
      const id = (typeof e.pointerId !== 'undefined') ? e.pointerId : 'mouse';
      clearPointer(id);
    }

    function onClick(e) {
      if (window.innerWidth > 768) return;
      // If a drag was recently detected, prevent the click from triggering navigation
      if (track.classList.contains('is-dragging')) {
        e.preventDefault(); e.stopImmediatePropagation();
        return;
      }
      // If this was a genuine tap/click on a tab, ensure navigation (some browsers
      // may not follow anchors when touch handlers are active). Perform navigation
      // via the same helper used elsewhere to be consistent.
      const tab = e.target && e.target.closest ? e.target.closest('.div-tab') : null;
      if (tab && tab.getAttribute) {
        const href = tab.getAttribute('href');
        if (href) {
          e.preventDefault(); e.stopImmediatePropagation();
          navigateToTab(href);
        }
      }
    }

    // Pointer events preferred
    if (window.PointerEvent) {
      track.addEventListener('pointerdown', onPointerDown, { capture: true });
      track.addEventListener('pointermove', onPointerMove, { capture: true, passive: true });
      track.addEventListener('pointerup', onPointerUp, { capture: true });
      track.addEventListener('pointercancel', onPointerCancel, { capture: true });
    } else {
      // Touch fallback
      let touchState = null;
      track.addEventListener('touchstart', function(e){
        if (window.innerWidth > 768) return;
        const t = e.changedTouches[0];
        if (!t) return;
        const tab = t.target && t.target.closest ? t.target.closest('.div-tab') : null;
        if (!tab) return;
        touchState = { id: t.identifier, startX: t.clientX, startY: t.clientY, moved: false, target: tab, startTime: Date.now() };
      }, { capture: true });

      track.addEventListener('touchmove', function(e){
        if (!touchState) return;
        const t = Array.from(e.changedTouches).find(tt => tt.identifier === touchState.id);
        if (!t) return;
        const dx = Math.abs(t.clientX - touchState.startX);
        const dy = Math.abs(t.clientY - touchState.startY);
        if (!touchState.moved && (dx > THRESHOLD || dy > THRESHOLD)) {
          touchState.moved = true;
          track.classList.add('is-dragging');
        }
      }, { capture: true, passive: true });

      track.addEventListener('touchend', function(e){
        if (!touchState) return;
        const t = Array.from(e.changedTouches).find(tt => tt.identifier === touchState.id);
        if (!t) { touchState = null; track.classList.remove('is-dragging'); return; }
        if (touchState.moved) { touchState = null; track.classList.remove('is-dragging'); return; }
        const href = touchState.target && touchState.target.getAttribute ? touchState.target.getAttribute('href') : null;
        touchState = null; track.classList.remove('is-dragging'); if (href) navigateToTab(href);
      }, { capture: true });

      track.addEventListener('touchcancel', function(){ touchState = null; track.classList.remove('is-dragging'); }, { capture: true });
    }

    // Always intercept clicks during/after drags to avoid accidental activation
    track.addEventListener('click', onClick, { capture: true });

    // Keyboard accessibility: allow Enter/Space to activate
    track.addEventListener('keydown', function(e){
      if (e.key === 'Enter' || e.key === ' ') {
        const tab = e.target && e.target.closest ? e.target.closest('.div-tab') : null;
        if (tab && tab.getAttribute('href')) navigateToTab(tab.getAttribute('href'));
      }
    }, true);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();

})();
