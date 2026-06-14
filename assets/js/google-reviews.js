// Client-side widget to load cached reviews from /data/reviews.json and render into elements with class 'auto-reviews'
(function(){
  async function loadReviews(){
    const urls = ['/data/reviews.json','/data/reviews.sample.json'];
    let reviews = null;
    for(const u of urls){
      try{
        const r = await fetch(u,{cache:'no-store'});
        if(!r.ok) continue;
        reviews = await r.json();
        if(Array.isArray(reviews) && reviews.length) break;
      }catch(e){continue}
    }
    if(!reviews || !reviews.length) return;
    const containers = document.querySelectorAll('.auto-reviews');
    containers.forEach((c,idx)=>{
      const rv = reviews[idx % reviews.length];
      const html = `
        <blockquote class="review-text">${rv.text || rv.review || rv.reviewBody || ''}</blockquote>
        <div class="review-meta">${rv.author_name || rv.author || rv.author.name || ''} <span class="review-rating">${(rv.rating||rv.reviewRating?.ratingValue)||''}</span></div>
      `;
      c.innerHTML = html;
      c.setAttribute('data-populated','true');
    });
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', loadReviews); else loadReviews();
})();
