const STATIC_CACHE = "morning-static-v7";
const DYNAMIC_CACHE = "morning-dynamic-v7";

const STATIC_ASSETS = [
  "/",
  "/index.html",
  "/assets/css/critical.css",
  "/assets/css/style.css",
  "/assets/css/header.css",
  "/assets/css/footer.css",
  "/assets/css/pages.css",
  "/assets/css/animations.css",
  "/assets/css/responsive.css",
  "/assets/js/utilities.js",
  "/assets/js/navigation.js",
  "/assets/js/forms.js",
  "/assets/js/animations.js",
  "/assets/js/sliders.js",
  "/assets/js/main.js",
  "/404.html",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.map((key) => {
        if (key !== STATIC_CACHE && key !== DYNAMIC_CACHE) return caches.delete(key);
      }))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  if (req.destination === "document")  { event.respondWith(networkFirst(req)); return; }
  if (req.destination === "image")     { event.respondWith(cacheFirst(req)); return; }
  if (req.destination === "style" || req.destination === "script") { event.respondWith(staleWhileRevalidate(req)); return; }
  event.respondWith(staleWhileRevalidate(req));
});

async function cacheFirst(req) {
  const cached = await caches.match(req);
  if (cached) return cached;
  const fresh = await fetch(req);
  if (fresh.ok) { const cache = await caches.open(DYNAMIC_CACHE); cache.put(req, fresh.clone()); }
  return fresh;
}

async function networkFirst(req) {
  try {
    const fresh = await fetch(req);
    if (fresh.ok) { const cache = await caches.open(DYNAMIC_CACHE); cache.put(req, fresh.clone()); }
    return fresh;
  } catch(err) { return caches.match(req); }
}

async function staleWhileRevalidate(req) {
  const cache = await caches.open(DYNAMIC_CACHE);
  const cached = await cache.match(req);
  const networkFetch = fetch(req).then((fresh) => { if (fresh.ok) cache.put(req, fresh.clone()); return fresh; });
  return cached || networkFetch;
}