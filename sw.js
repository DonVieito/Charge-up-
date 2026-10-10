// Charge Up 0.9: intentionally no caching while debugging map and GPS.
self.addEventListener('install',()=>self.skipWaiting());
self.addEventListener('activate',event=>event.waitUntil((async()=>{for(const key of await caches.keys())if(key.startsWith('charge-up-'))await caches.delete(key);await self.clients.claim();})()));
