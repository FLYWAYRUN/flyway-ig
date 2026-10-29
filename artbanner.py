# -*- coding: utf-8 -*-
import asyncio
from playwright.async_api import async_playwright
FONTS = open('fonts.css', encoding='utf-8').read()
S = 'file:///tmp/claude-0/-home-claude/2e17bfd3-42bc-5136-bb78-767ebae6d1f2/scratchpad'
OUT = '/tmp/claude-0/-home-claude/2e17bfd3-42bc-5136-bb78-767ebae6d1f2/scratchpad'

SHELL = """<!doctype html><meta charset="utf-8"><style>
%s
*{margin:0;padding:0;box-sizing:border-box}
:root{--ink:#08090B;--volt:#D4FF36;--paper:#F2F2EE}
html,body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{width:%spx;height:%spx;overflow:hidden;font-family:'Inter','Helvetica Neue',Arial,sans-serif;-webkit-font-smoothing:antialiased}
.w{position:relative;width:%spx;height:%spx;overflow:hidden;background:var(--volt)}
.art{position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover}
.ct{position:absolute;inset:0;padding:%s;display:flex;flex-direction:column}
.dx{font-family:'Anton',sans-serif;text-transform:uppercase;line-height:.9;letter-spacing:.012em}
.dx2{font-family:'Bebas',sans-serif;text-transform:uppercase;line-height:1;letter-spacing:.05em}
.mono{font-family:'Liberation Mono',monospace;text-transform:uppercase;letter-spacing:.22em}
.sp{margin-top:auto}
.rule{height:6px;background:var(--ink);display:block}
</style><body>%s</body>"""

CHEV = ('<svg width="52" height="52" viewBox="0 0 100 100"><path d="M14 68 L50 30 L86 68" '
        'fill="none" stroke="#08090B" stroke-width="13" stroke-linecap="square"/></svg>')

WIDE = """<div class="w">
  <img class="art" src="%s/art_wide.png">
  <div class="ct">
    <div style="display:flex;align-items:center;gap:20px">
      %s<div class="mono" style="font-size:17px;color:rgba(0,0,0,.62)">Seoul &middot; Spring 2027</div>
    </div>
    <div class="sp"></div>
    <div class="dx" style="font-size:186px;color:var(--ink)">Flyway</div>
    <span class="rule" style="width:102px;margin:32px 0 26px"></span>
    <div class="dx2" style="font-size:48px;color:var(--ink)">Runners migrate too.</div>
    <div style="font-size:22px;color:rgba(0,0,0,.70);margin-top:16px;max-width:620px;line-height:1.5">
      Seasonal run trips along the East Asian flyway.</div>
    <div class="sp"></div>
    <div class="mono" style="font-size:15px;color:rgba(0,0,0,.58)">
      Bangkok &rarr; Seoul &nbsp;&middot;&nbsp; The first flight</div>
  </div></div>""" % (S, CHEV)

TALL = """<div class="w">
  <img class="art" src="%s/art_tall.png">
  <div class="ct">
    <div class="mono" style="font-size:19px;color:rgba(0,0,0,.62)">Run Trip 01 &middot; Seoul</div>
    <div style="height:56px"></div>
    <div class="dx" style="font-size:132px;color:var(--ink)">Runners<br>migrate<br>too.</div>
    <span class="rule" style="width:64px;margin:36px 0 28px"></span>
    <div style="font-size:26px;color:rgba(0,0,0,.74);line-height:1.5;max-width:760px">
      Fifty million bodies move along this corridor every season.<br>
      We built a running trip on the same line.</div>
    <div class="sp"></div>
    <div style="display:flex;justify-content:space-between;align-items:center;
                border-top:2px solid rgba(0,0,0,.26);padding-top:26px">
      <div class="dx" style="font-size:26px;letter-spacing:.14em;color:var(--ink)">Flyway</div>
      <div class="mono" style="font-size:16px;color:rgba(0,0,0,.62)">April 2027</div>
    </div>
  </div></div>""" % S

JOBS = [('FLYWAY_art_wide.png', 1920, 800,  '68px 84px',      WIDE),
        ('FLYWAY_art_post.png', 1080, 1350, '78px 72px 72px', TALL)]

async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch(args=['--font-render-hinting=none'])
        for name,w,h,pad,body in JOBS:
            pg = await br.new_page(viewport={'width':w,'height':h})
            open('/tmp/claude-0/-home-claude/2e17bfd3-42bc-5136-bb78-767ebae6d1f2/scratchpad/_a.html',
                 'w',encoding='utf-8').write(SHELL % (FONTS,w,h,w,h,pad,body))
            await pg.goto(f'{S}/_a.html'); await pg.wait_for_timeout(1100)
            await pg.screenshot(path=f'{OUT}/{name}'); await pg.close()
            print(' ', name)
        await br.close()
asyncio.run(main())
