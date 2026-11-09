from pathlib import Path
import json
from playwright.sync_api import sync_playwright
root=Path.cwd();out=root/'verification'
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 page=browser.new_page(viewport={'width':1100,'height':800},device_scale_factor=1)
 page.set_content('<html><head><style>html,body{margin:0;background:#0d1117}svg{display:block;width:100%;height:auto}</style></head><body>'+ (root/'surya.svg').read_text()+'</body></html>');page.wait_for_load_state('load')
 stats={}
 for time in (0,1.5,3.5,6.2,9.8,10,11.5,16.2):
  page.evaluate('(t)=>{document.querySelector("svg").pauseAnimations();document.querySelector("svg").setCurrentTime(t)}',time)
  page.locator('svg').screenshot(path=str(out/f'browser-{time}.png'))
  stats[str(time)]=page.evaluate('Array.from(document.querySelectorAll("mask path")).map(p=>getComputedStyle(p).strokeDashoffset)')
 assert stats['0']==stats['10'], 'Every pen must reset at the cycle boundary'
 assert stats['1.5']==stats['11.5'], 'The second cycle must retain the writing order'
 assert stats['6.2']==stats['9.8']==stats['16.2']==['0px']*8, 'The completed name must hold and complete again'
 page.set_viewport_size({'width':390,'height':800});page.locator('svg').screenshot(path=str(out/'browser-mobile.png'))
 (out/'animation-check.json').write_text(json.dumps(stats,indent=2))
 print(json.dumps(stats))
 browser.close()
