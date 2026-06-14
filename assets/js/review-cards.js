// review-cards.js — make entire review cards clickable and accessible
document.addEventListener('DOMContentLoaded', function(){
  const cards = document.querySelectorAll('.ms-review-card');
  cards.forEach(card => {
    const url = card.getAttribute('data-google-url') || card.querySelector('.btn-google')?.getAttribute('href');
    if(!url) return;
    // Click handler
    card.addEventListener('click', (e)=>{
      // Ignore clicks on links that already open
      const target = e.target.closest('a');
      if(target && target.classList.contains('btn-google')) return;
      window.open(url, '_blank', 'noopener');
    });
    // Keyboard support
    card.addEventListener('keydown', (e)=>{
      if(e.key==="Enter" || e.key===" "){
        e.preventDefault();
        window.open(url, '_blank', 'noopener');
      }
    });
    // Ensure the visible google button opens the same url
    const btn = card.querySelector('.btn-google');
    if(btn){
      btn.addEventListener('click',(e)=>{e.stopPropagation();});
      btn.setAttribute('href', url);
      btn.setAttribute('target','_blank');
      btn.setAttribute('rel','noopener noreferrer');
    }
  });
});
