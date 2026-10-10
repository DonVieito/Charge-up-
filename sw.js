// Charge Up 1.2: no offline cache for dynamic charging locations.
self.addEventListener('install',()=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
