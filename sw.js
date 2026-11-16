// Vỏ app Trinh thám TCX: giữ sẵn phần vỏ để mở nhanh; nội dung thật luôn lấy mới từ web.
const VO = 'trinh-tham-v4', TEP = ['./', './index.html', './manifest.webmanifest', './icon-192.png', './icon-512.png', './icon-180.png', './be.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(VO).then(c => c.addAll(TEP))); self.skipWaiting(); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== VO).map(k => caches.delete(k))))); self.clients.claim(); });
self.addEventListener('fetch', e => {
  const u = new URL(e.request.url);
  if (u.origin !== location.origin) return;
  e.respondWith(fetch(e.request).then(r => { const c = r.clone(); caches.open(VO).then(x => x.put(e.request, c)); return r; }).catch(() => caches.match(e.request).then(r => r || caches.match('./index.html'))));
});
