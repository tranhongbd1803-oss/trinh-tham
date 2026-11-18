// App đã chuyển sang https://trinh-tham-tcx.pages.dev — vỏ cũ tự gỡ bộ nhớ đệm.
self.addEventListener('install', function () { self.skipWaiting(); });
self.addEventListener('activate', function (e) { e.waitUntil(caches.keys().then(function (ks) { return Promise.all(ks.map(function (k) { return caches.delete(k); })); }).then(function () { return self.registration.unregister(); })); });
