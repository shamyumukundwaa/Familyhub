const CACHE_NAME = 'familyhub-v1';
const ASSETS = [
  '/',
  '/index.html',
  '/parent.html',
  '/child.html',
  '/style.css',
  '/manifest.json',
  'https://googleapis.com'
];
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS);
    })
  );
});
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    })
  );
});

self.addEventListener('fetch', (e) => {
 
  if (e.request.url.includes('/auth/') || e.request.url.includes('localhost:8000')) {
    return;
  }

  e.respondWith(
    fetch(e.request)
      .then((response) => {
        const resClone = response.clone();
        caches.open(CACHE_NAME).then((cache) => {
          cache.put(e.request, resClone);
        });
        return response;
      })
      .catch(() => caches.match(e.request)) 
  );
});
