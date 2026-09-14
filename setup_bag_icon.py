import os

os.makedirs('static', exist_ok=True)

svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <rect width="512" height="512" rx="128" fill="#00885a"/>
  <!-- Bag Handle -->
  <path d="M160 192 C 160 110, 352 110, 352 192 L 304 192 C 304 146, 208 146, 208 192 Z" fill="#ffffff"/>
  <!-- Bag Body -->
  <path d="M 120 200 C 102 200, 96 214, 100 236 L 126 400 C 130 424, 148 440, 172 440 L 340 440 C 364 440, 382 424, 386 400 L 412 236 C 416 214, 410 200, 392 200 Z" fill="#ffffff"/>
</svg>"""

with open('static/app_icon.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)

manifest_content = """{
  "id": "/",
  "name": "Duka Track POS",
  "short_name": "DukaPOS",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "orientation": "portrait",
  "background_color": "#020617",
  "theme_color": "#00885a",
  "prefer_related_applications": false,
  "icons": [
    {
      "src": "/static/app_icon.svg",
      "sizes": "any",
      "type": "image/svg+xml",
      "purpose": "any maskable"
    },
    {
      "src": "/static/app_icon.svg",
      "sizes": "192x192 512x512",
      "type": "image/svg+xml",
      "purpose": "any maskable"
    }
  ]
}"""

with open('static/manifest.json', 'w', encoding='utf-8') as f:
    f.write(manifest_content)

sw_content = """const CACHE_NAME = 'duka-v3';
self.addEventListener('install', (e) => { self.skipWaiting(); });
self.addEventListener('activate', (e) => { e.waitUntil(clients.claim()); });
self.addEventListener('fetch', (e) => {
    e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
});"""

with open('static/sw.js', 'w', encoding='utf-8') as f:
    f.write(sw_content)

print("Bag icon, manifest, and service worker configured.")
