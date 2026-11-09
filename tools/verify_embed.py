from pathlib import Path
import hashlib,json
from playwright.sync_api import sync_playwright
root=Path.cwd();out=root/'verification'
html=out/'readme-embed.html'
html.write_text('<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0;background:#0d1117}img{display:block;width:100%;height:auto}</style></head><body><img src="../surya.svg" alt="Surya Narayanaa and ASCII rose"></body></html>',encoding='utf-8')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 page=b.new_page(viewport={'width':1100,'height':900});page.goto(html.as_uri());page.wait_for_function('document.images[0].complete && document.images[0].naturalWidth>0');page.wait_for_timeout(6500)
 page.locator('img').screenshot(path=str(out/'readme-image-embed.png'))
 print(page.evaluate('({loaded:document.images[0].complete,width:document.images[0].naturalWidth,height:document.images[0].naturalHeight})'))
 b.close()
print('SVG SHA256:',hashlib.sha256((root/'surya.svg').read_bytes()).hexdigest())
