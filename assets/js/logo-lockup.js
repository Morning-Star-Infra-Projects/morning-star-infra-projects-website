(function(){
  function updateLogoLockups(){
    document.querySelectorAll('.logo-text').forEach(function(container){
      var main = container.querySelector('.logo-main');
      var sub = container.querySelector('.logo-sub');
      if(!main || !sub) return;

      // Reset
      sub.style.letterSpacing = '';
      sub.style.width = '';

      var mainRect = main.getBoundingClientRect();
      var mainW = Math.round(mainRect.width);
      var subNaturalW = Math.round(sub.getBoundingClientRect().width);
      var text = sub.textContent || '';
      var gaps = Math.max(text.length - 1, 1);
      var neededTotal = mainW - subNaturalW;
      var perGap = neededTotal / gaps;
      var clamped = Math.max(Math.min(perGap, 30), -6);

      sub.style.letterSpacing = clamped + 'px';
      sub.style.width = mainW + 'px';
      container.style.setProperty('--logo-main-w', mainW + 'px');

      var footerBrand = container.closest('.footer-brand');
      if(footerBrand){
        var parentRect = footerBrand.getBoundingClientRect();
        var offset = Math.round(mainRect.left - parentRect.left);
        footerBrand.style.setProperty('--footer-logo-w', mainW + 'px');
        footerBrand.style.setProperty('--logo-text-offset', offset + 'px');
        var logoIcon = footerBrand.querySelector('.logo-icon');
        if(logoIcon){
          var iconRect = logoIcon.getBoundingClientRect();
          var iconOffset = Math.round(iconRect.left - parentRect.left);
          footerBrand.style.setProperty('--logo-paragraph-offset', iconOffset + 'px');
        }
      }
    });
  }

  window.addEventListener('load', updateLogoLockups);
  window.addEventListener('resize', function(){ requestAnimationFrame(updateLogoLockups); });
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', updateLogoLockups);
  else updateLogoLockups();

  var obs = new MutationObserver(function(){ updateLogoLockups(); });
  document.querySelectorAll('.logo-text').forEach(function(node){ obs.observe(node, { childList:true, subtree:true, characterData:true }); });
})();
