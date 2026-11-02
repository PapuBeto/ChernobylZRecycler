import json
from pathlib import Path
from PIL import Image

root = Path('.')
assets = root/'src/main/resources/assets/chernobylz_recycler'
items = json.load(open('tools/items.json', encoding='utf-8'))
ids = [r['id'] for r in items['resources']] + [c['id'] for c in items['components']] + [o['id'] for o in items['objects']]

scale = 4
cell = 16*scale + 4
cols = 13
rows = (len(ids)+cols-1)//cols
sheet = Image.new('RGBA', (cols*cell, rows*cell), (36,38,40,255))
for i, item_id in enumerate(ids):
    p = assets/'textures/item'/f'{item_id}.png'
    if not p.exists():
        continue
    icon = Image.open(p).convert('RGBA').resize((16*scale,16*scale), Image.NEAREST)
    x = (i%cols)*cell + 2
    y = (i//cols)*cell + 2
    sheet.alpha_composite(icon, (x,y))
sheet.save('docs/preview_items.png')

gui = Image.open(assets/'textures/gui/recycler.png').convert('RGBA').resize((176*2,166*2), Image.NEAREST)
gui.save('docs/preview_gui.png')

block = Image.new('RGBA',(3*16*8+16, 16*8+8),(30,30,30,255))
for i,name in enumerate(['recycler_side.png','recycler_top.png','recycler_front.png']):
    tex = Image.open(assets/'textures/block'/name).convert('RGBA').resize((16*8,16*8), Image.NEAREST)
    block.alpha_composite(tex,(i*(16*8+8),4))
block.save('docs/preview_block.png')
print('previews ok', len(ids))
