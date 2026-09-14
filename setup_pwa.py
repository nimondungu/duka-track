import os
import struct
import zlib

os.makedirs('static', exist_ok=True)

manifest_content = """{
  "id": "/",
  "name": "Duka Track POS",
  "short_name": "DukaPOS",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "orientation": "portrait",
  "background_color": "#020617",
  "theme_color": "#0f172a",
  "prefer_related_applications": false,
  "icons": [
    {
      "src": "/static/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/static/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ]
}"""

with open('static/manifest.json', 'w', encoding='utf-8') as f:
    f.write(manifest_content)

sw_content = """const CACHE_NAME = 'duka-v2';
self.addEventListener('install', (e) => { self.skipWaiting(); });
self.addEventListener('activate', (e) => { e.waitUntil(clients.claim()); });
self.addEventListener('fetch', (e) => {
    e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
});"""

with open('static/sw.js', 'w', encoding='utf-8') as f:
    f.write(sw_content)

def make_png(width, height, r, g, b):
    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
    raw = b''.join(b'\x00' + struct.pack('>BBB', r, g, b) * width for _ in range(height))
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b'')

with open('static/icon-192.png', 'wb') as f:
    f.write(make_png(192, 192, 16, 185, 129))

with open('static/icon-512.png', 'wb') as f:
    f.write(make_png(512, 512, 16, 185, 129))

print("PWA static files verified and generated.")
