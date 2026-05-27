// layout-loader.js
// Fetch and inject centralized header and footer into pages.
(function(){
  function runScripts(container){
    var scripts = container.querySelectorAll('script');
    scripts.forEach(function(old){
      var script = document.createElement('script');
      // copy attributes
      for(var i=0;i<old.attributes.length;i++){
        var attr = old.attributes[i];
        script.setAttribute(attr.name, attr.value);
      }
      // inline content
      if(old.textContent) script.textContent = old.textContent;
      old.parentNode.replaceChild(script, old);
    });
  }

  function loadInto(selector, url){
    return fetch(url, {cache:'no-store'}).then(function(resp){
      if(!resp.ok) throw new Error('Failed to load ' + url);
      return resp.text();
    }).then(function(html){
      var container = document.querySelector(selector);
      if(!container) return;
      container.innerHTML = html;
      runScripts(container);
    }).catch(function(err){
      console.error('layout-loader error:', err);
    });
  }

  // wait until DOM ready
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', function(){
      loadInto('#header-container', '/components/header.html');
      loadInto('#footer-container', '/components/footer.html');
    });
  } else {
    loadInto('#header-container', '/components/header.html');
    loadInto('#footer-container', '/components/footer.html');
  }

})();
