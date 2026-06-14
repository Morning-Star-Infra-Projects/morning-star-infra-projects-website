// blog.js - handles FAQ accordion, counters and simple UI interactions
document.addEventListener('DOMContentLoaded', function(){
  // FAQ accordion
  document.querySelectorAll('.faq-question').forEach(q=>{
    q.addEventListener('click', ()=>{
      const item = q.parentElement;
      const open = item.classList.toggle('open');
      const ans = item.querySelector('.faq-answer');
      if(open){
        ans.style.display='block';
      } else {
        ans.style.display='none';
      }
    });
  });

  // Simple counter animation
  function animateCounters(){
    document.querySelectorAll('.metric .num').forEach(el=>{
      const target = Number(el.getAttribute('data-target'))||0;
      let cur = 0; const step = Math.max(1,Math.floor(target/80));
      const id = setInterval(()=>{
        cur += step; if(cur>=target){el.textContent = target; clearInterval(id);} else el.textContent = cur;
      },12);
    });
  }
  // Trigger when visible
  const obs = new IntersectionObserver(entries=>{
    entries.forEach(e=>{ if(e.isIntersecting){ animateCounters(); obs.disconnect(); } });
  },{threshold:0.3});
  const metrics = document.querySelector('.trust-metrics'); if(metrics) obs.observe(metrics);

  // FAQ search
  const search = document.getElementById('faq-search');
  if(search){
    search.addEventListener('input', ()=>{
      const q = search.value.toLowerCase();
      document.querySelectorAll('.faq-item').forEach(item=>{
        const txt = item.textContent.toLowerCase();
        item.style.display = txt.includes(q)?'block':'none';
      });
    });
  }
});
