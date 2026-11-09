"""Compose the original ASCII pixels into a seamless signature-and-rose scene."""
from pathlib import Path
from PIL import Image, ImageStat
import math, base64, copy, xml.etree.ElementTree as E
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
N='http://www.w3.org/2000/svg';E.register_namespace('',N)
def t(x):return '{'+N+'}'+x
source=Image.open(ROOT/'rose.png').convert('RGB')
W,H=2884,1760;rose_x=W-source.width
scene=Image.new('RGB',(W,H),'black')
# The reference's glyph lattice repeats every 24 pixels horizontally and 8 vertically.
# Sample only its empty margins. Preserve every source pixel, including antialiasing,
# varied glyphs, and the changing red field. The rose itself remains untouched.
for y in range(0,H,8):
 # Preserve the original row and glyph phase. Reuse its continuous field rather
 # than alternating margin banks. Replace only tiles occupied by the source rose.
 tiles=[]
 for sx in range(0,1224,24):
  tile=source.crop((sx,y,sx+24,y+8))
  rr,gg,bb=ImageStat.Stat(tile).mean
  pixels=np.asarray(tile).astype(int)
  gray=(pixels[:,:,0]>6) & (np.abs(pixels[:,:,0]-pixels[:,:,1])<=3) & (np.abs(pixels[:,:,1]-pixels[:,:,2])<=3)
  valid=(rr-gg>10) and not gray.any()
  tiles.append((sx,tile,valid))
 available=[tile for tile in tiles if tile[2]]
 if not available:raise RuntimeError('No source background on row '+str(y))
 for x in range(0,rose_x,24):
  sx=(x-rose_x)%1224
  chosen=tiles[sx//24]
  if not chosen[2]:chosen=min(available,key=lambda tile:abs(tile[0]-sx))
  scene.paste(chosen[1],(x,y))
scene.paste(source,(rose_x,0))
(ROOT/'assets').mkdir(exist_ok=True)
scene.save(ROOT/'assets/scene-texture.png',optimize=True)
original=E.parse(ROOT/'tools/handwriting-source.svg').getroot()
r=E.Element(t('svg'),{'viewBox':f'0 0 {W} {H}','width':str(W),'height':str(H),'role':'img','aria-labelledby':'title description'})
E.SubElement(r,t('title'),{'id':'title'}).text='Surya Narayanaa'
E.SubElement(r,t('desc'),{'id':'description'}).text='Surya Narayanaa written in cursive beside the original ASCII rose. Its original red character texture continues across the full composition.'
d=E.SubElement(r,t('defs'))
E.SubElement(d,t('image'),{'id':'scene','width':str(W),'height':str(H),'href':'data:image/png;base64,'+base64.b64encode((ROOT/'assets/scene-texture.png').read_bytes()).decode()})
f=E.SubElement(d,t('filter'),{'id':'charcoal','color-interpolation-filters':'sRGB','x':'0','y':'0','width':'1','height':'1'})
E.SubElement(f,t('feColorMatrix'),{'type':'matrix','values':'.16 0 0 0 0 .16 0 0 0 0 .16 0 0 0 0 0 0 0 1 0'})
E.SubElement(r,t('use'),{'href':'#scene'})
for i,(scale,tx,ty) in enumerate(((1.35,50,205),(1.08,-90,430))):
 matrix=f'translate({tx} {ty}) scale({scale})'
 mask=copy.deepcopy(original.find(f'.//*[@id="handwriting-{i}"]'))
 mask.set('x','0');mask.set('y','0');mask.set('width',str(W));mask.set('height',str(H))
 mask.find(t('g')).set('transform',matrix);d.append(mask)
 clip=copy.deepcopy(original.find(f'.//*[@id="lettering-{i}"]'))
 path=clip.find(t('path'));path.set('transform',matrix+' '+path.get('transform'));d.append(clip)
 g=E.SubElement(r,t('g'),{'id':f'signature-line-{i}','mask':f'url(#handwriting-{i})'})
 outline=copy.deepcopy(path);outline.set('fill','#000');outline.set('stroke','#000');outline.set('stroke-width','3');outline.set('stroke-linejoin','round');g.append(outline)
 c=E.SubElement(g,t('g'),{'clip-path':f'url(#lettering-{i})'})
 E.SubElement(c,t('rect'),{'width':str(W),'height':str(H),'fill':'#000'})
 E.SubElement(c,t('use'),{'href':'#scene','filter':'url(#charcoal)'})
E.indent(r);E.ElementTree(r).write(ROOT/'surya.svg',encoding='unicode')
assert len(r.findall('.//'+t('animate')))==8
assert scene.crop((rose_x,0,W,H)).tobytes()==source.tobytes()
print('Built continuous original-pixel texture; original rose pixels preserved exactly; eight handwriting pen paths retained.')
