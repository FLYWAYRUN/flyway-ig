# -*- coding: utf-8 -*-
"""content.py -> docs/img/*.png  + docs/index.html contact sheet."""
import asyncio, os, sys, json, datetime
from playwright.async_api import async_playwright
import tpl, content
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'art'))
import photoposter as poster

HERE = os.path.dirname(os.path.abspath(__file__))
IMG  = os.path.join(HERE, 'docs', 'img')

async def main():
    os.makedirs(IMG, exist_ok=True)
    async with async_playwright() as p:
        br = await p.chromium.launch(args=['--font-render-hinting=none'])
        pg = await br.new_page(viewport={'width':1080,'height':1350}, device_scale_factor=1)
        tmp = os.path.join(IMG, '_tmp.html')
        for post in content.POSTS:
            if post['type'] == 'art':
                post = dict(post, art=poster.make(
                    post.get('art_kind', 'tall'),
                    os.path.join(HERE, 'build', f"bg_{post['id']}.png"),
                    seed=int(post['id']) * 7 + 4))
            open(tmp,'w',encoding='utf-8').write(tpl.render(post))
            await pg.goto('file://' + tmp)
            await pg.wait_for_timeout(700)
            await pg.screenshot(path=os.path.join(IMG, post['id'] + '.png'))
            print('  rendered', post['id'])
        os.remove(tmp)
        await br.close()

    # contact sheet so you can eyeball the grid at the Pages URL
    tiles = ''.join(
        '<a href="img/%s.png"><img src="img/%s.png" loading="lazy"></a>' % (p['id'], p['id'])
        for p in content.POSTS)
    open(os.path.join(HERE,'docs','index.html'),'w',encoding='utf-8').write(
        '<!doctype html><meta charset=utf-8><title>Flyway assets</title>'
        '<style>body{margin:0;background:#111;display:grid;'
        'grid-template-columns:repeat(3,1fr);gap:4px}img{width:100%;display:block}</style>'
        + tiles)

    # seed schedule.json without clobbering posts already sent
    sp = os.path.join(HERE, 'schedule.json')
    old = {}
    if os.path.exists(sp):
        old = {r['id']: r for r in json.load(open(sp, encoding='utf-8'))}
    rows = []
    for p in content.POSTS:
        prev = old.get(p['id'], {})
        rows.append({
            'id': p['id'],
            'when': prev.get('when', ''),          # "2026-11-04 19:00"  (KST, blank = hold)
            'status': prev.get('status', 'draft'), # draft | ready | posted
            'media_id': prev.get('media_id', ''),
            'caption': p['caption'],
        })
    json.dump(rows, open(sp,'w',encoding='utf-8'), ensure_ascii=False, indent=2)
    print('schedule.json:', len(rows), 'rows')

asyncio.run(main())
