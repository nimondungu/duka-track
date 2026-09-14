import os
import zlib
import struct

os.makedirs('static', exist_ok=True)

# 1. Exact SVG matching image 1 (emerald-teal gradient + black line shopping bag)
svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <linearGradient id="bagGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#34d399"/>
      <stop offset="100%" stop-color="#10b981"/>
    </linearGradient>
  </defs>
  <!-- Rounded Squircle Background -->
  <rect width="512" height="512" rx="140" fill="url(#bagGrad)"/>
  
  <!-- Black Bag Outline matching Image 1 -->
  <!-- Handle -->
  <path d="M 210 200 C 210 135, 302 135, 302 200" 
        stroke="#020617" stroke-width="32" stroke-linecap="round" fill="none"/>
  <!-- Body -->
  <path d="M 160 210 L 352 210 L 376 390 C 378 405, 366 418, 350 418 L 162 418 C 146 418, 134 405, 136 390 Z" 
        stroke="#020617" stroke-width="32" stroke-linejoin="round" stroke-linecap="round" fill="none"/>
</svg>"""

with open('static/app_icon.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)

# 2. Update manifest.json
manifest_content = """{
  "id": "/",
  "name": "Duka Track POS",
  "short_name": "Duka Track",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "orientation": "portrait",
  "background_color": "#020617",
  "theme_color": "#10b981",
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

# 3. Increment Service Worker cache version so browser refreshes the icon immediately
sw_content = """const CACHE_NAME = 'duka-v4';
self.addEventListener('install', (e) => { self.skipWaiting(); });
self.addEventListener('activate', (e) => { e.waitUntil(clients.claim()); });
self.addEventListener('fetch', (e) => {
    e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
});"""

with open('static/sw.js', 'w', encoding='utf-8') as f:
    f.write(sw_content)

print("Exact emerald + black bag icon and manifest updated successfully!")
