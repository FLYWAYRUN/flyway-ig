# -*- coding: utf-8 -*-
import asyncio, os
from playwright.async_api import async_playwright
FONTS = open('fonts.css', encoding='utf-8').read()

PAGE = """<!doctype html><meta charset="utf-8"><style>
%s
*{margin:0;padding:0}html,body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{width:640px;height:640px;overflow:hidden}
.a{width:640px;height:640px;display:flex;align-items:center;justify-content:center;background:%s}
</style><body><div class="a">%s</div></body>"""

INK, VOLT = '#08090B', '#D4FF36'

def chev(fill, w=5):  # single bold chevron, points up
    return ('<svg width="360" height="360" viewBox="0 0 100 100">'
            '<path d="M14 68 L50 30 L86 68" fill="none" stroke="%s" '
            'stroke-width="13" stroke-linecap="square" stroke-linejoin="miter"/></svg>' % fill)

def stack(fill):      # three chevrons = formation / speed
    p = ''.join('<path d="M16 %d L50 %d L84 %d" fill="none" stroke="%s" stroke-width="10" '
                'stroke-linecap="square" stroke-linejoin="miter" opacity="%s"/>'
                % (72+i*0, 72, 72, fill, o) for i, o in [(0,'1')])
    rows = ''
    for i, (y, op) in enumerate([(84,'0.28'),(64,'0.6'),(44,'1')]):
        rows += ('<path d="M16 %d L50 %d L84 %d" fill="none" stroke="%s" stroke-width="10" '
                 'stroke-linecap="square" stroke-linejoin="miter" opacity="%s"/>'
                 % (y, y-26, y, fill, op))
    return '<svg width="380" height="380" viewBox="0 0 100 100">%s</svg>' % rows

def flock(fill):      # V formation of birds
    pts = [(50,34),(36,46),(64,46),(22,58),(78,58),(8,70),(92,70)]
    b = ''.join('<path d="M%s %s l-7 7 M%s %s l7 7" stroke="%s" stroke-width="5.5" '
                'fill="none" stroke-linecap="round"/>' % (x,y,x,y,fill) for x,y in pts)
    return '<svg width="400" height="400" viewBox="0 0 100 100">%s</svg>' % b

def letter(col, bg):
    return ('<div style="font-family:Anton;font-size:400px;color:%s;line-height:1;'
            'margin-top:-18px">F</div>' % col)

def arc(fill):        # the route line from the deck
    return ('<svg width="420" height="420" viewBox="0 0 100 100">'
            '<path d="M10 76 C 30 72, 44 60, 58 46 S 80 26, 90 20" fill="none" stroke="%s" '
            'stroke-width="9" stroke-linecap="round"/>'
            '<circle cx="10" cy="76" r="7.5" fill="%s"/>'
            '<circle cx="90" cy="20" r="9" fill="%s"/></svg>' % (fill, fill, fill))

OPTS = [
 ('a1_chevron_volt',  INK,  chev(VOLT)),
 ('a2_chevron_ink',   VOLT, chev(INK)),
 ('a3_stack_volt',    INK,  stack(VOLT)),
 ('a4_flock_volt',    INK,  flock(VOLT)),
 ('a5_F_volt',        VOLT, letter(INK, VOLT)),
 ('a6_arc_volt',      INK,  arc(VOLT)),
]

async def main():
    os.makedirs('avatars', exist_ok=True)
    async with async_playwright() as p:
        br = await p.chromium.launch(args=['--font-render-hinting=none'])
        pg = await br.new_page(viewport={'width':640,'height':640})
        for name, bg, body in OPTS:
            open('avatars/_t.html','w',encoding='utf-8').write(PAGE % (FONTS, bg, body))
            await pg.goto('file:///home/claude/flyway/avatars/_t.html')
            await pg.wait_for_timeout(500)
            await pg.screenshot(path=f'avatars/{name}.png')
            print(' ', name)
        os.remove('avatars/_t.html')
        await br.close()
asyncio.run(main())
