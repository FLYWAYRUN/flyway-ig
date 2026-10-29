# -*- coding: utf-8 -*-
import asyncio, os
from playwright.async_api import async_playwright
FONTS = open('fonts.css', encoding='utf-8').read()
P = 'file:///home/claude/photos'

SHELL = """<!doctype html><meta charset="utf-8"><style>
%s
*{margin:0;padding:0;box-sizing:border-box}
:root{--ink:#08090B;--paper:#F2F2EE;--volt:#D4FF36;--grey:#7D838F}
html,body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{width:%spx;height:%spx;overflow:hidden;background:var(--ink);
     font-family:'Inter',sans-serif;-webkit-font-smoothing:antialiased}
.w{position:relative;width:%spx;height:%spx;overflow:hidden}
.ph{position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover;
    object-position:%s;filter:brightness(.74) contrast(1.06)}
.sc{position:absolute;inset:0}
.ct{position:absolute;inset:0;padding:%s;display:flex;flex-direction:column}
.dx{font-family:'Anton',sans-serif;text-transform:uppercase;line-height:.9;letter-spacing:.012em}
.dx2{font-family:'Bebas',sans-serif;text-transform:uppercase;line-height:1;letter-spacing:.05em}
.mono{font-family:'Liberation Mono',monospace;text-transform:uppercase;letter-spacing:.22em;color:#AEB4BE}
.sp{margin-top:auto}
.rule{height:5px;background:var(--volt);display:block}
</style><body>%s</body>"""

def chevron(size, col='#D4FF36', w=13):
    return ('<svg width="%s" height="%s" viewBox="0 0 100 100"><path d="M14 68 L50 30 L86 68" '
            'fill="none" stroke="%s" stroke-width="%s" stroke-linecap="square"/></svg>'
            % (size, size, col, w))

# ── wide hero 1920x800 ─────────────────────────────────────
WIDE = """<div class="w">
  <img class="ph" src="%s/t_city.jpg">
  <div class="sc" style="background:linear-gradient(100deg,
      rgba(8,9,11,.96) 0%%, rgba(8,9,11,.80) 34%%, rgba(8,9,11,.18) 70%%, rgba(8,9,11,.42) 100%%)"></div>
  <div class="sc" style="background:linear-gradient(0deg,rgba(8,9,11,.85) 0%%,rgba(8,9,11,0) 38%%)"></div>
  <div class="ct">
    <div style="display:flex;align-items:center;gap:22px">
      %s
      <div class="mono" style="font-size:17px">Seoul &middot; Spring 2027</div>
    </div>
    <div class="sp"></div>
    <div class="dx" style="font-size:178px;color:var(--paper)">Flyway</div>
    <span class="rule" style="width:96px;margin:34px 0 26px"></span>
    <div class="dx2" style="font-size:46px;color:var(--paper);max-width:900px">
      Runners migrate too.</div>
    <div style="font-size:22px;color:#AEB4BE;margin-top:18px;max-width:760px;line-height:1.5">
      Seasonal run trips along the East Asian flyway.<br>
      Three mornings on the roads Seoul actually runs.</div>
    <div class="sp"></div>
    <div class="mono" style="font-size:15px">Bangkok &rarr; Seoul &nbsp;&middot;&nbsp; The first flight</div>
  </div></div>""" % (P, chevron(54))

# ── instagram 1080x1350 ────────────────────────────────────
IG = """<div class="w">
  <img class="ph" src="%s/t_city.jpg">
  <div class="sc" style="background:linear-gradient(0deg,
      rgba(8,9,11,.97) 0%%, rgba(8,9,11,.82) 26%%, rgba(8,9,11,.10) 58%%, rgba(8,9,11,.55) 100%%)"></div>
  <div class="ct">
    <div class="mono" style="font-size:19px;color:#D4FF36">Seoul &middot; the real roads</div>
    <div class="sp"></div>
    <div class="dx" style="font-size:124px;color:var(--paper)">Seoul<br>runs here.</div>
    <span class="rule" style="width:58px;margin:36px 0 28px"></span>
    <div style="font-size:26px;color:#C2C8D2;line-height:1.5;max-width:800px">
      Not the guidebook route. The backstreets the city&rsquo;s own crews run,
      and a Korean pacer on every one of them.</div>
    <div style="margin-top:46px;display:flex;justify-content:space-between;align-items:center;
                border-top:1px solid rgba(255,255,255,.14);padding-top:26px">
      <div class="dx" style="font-size:24px;letter-spacing:.14em;color:var(--paper)">Flyway</div>
      <div class="mono" style="font-size:16px;color:#D4FF36">Run Trip &middot; 2027</div>
    </div>
  </div></div>""" % P

# ── band layout: landscape photo on top, type on solid ink below ──
RIVER = """<div class="w" style="display:flex;flex-direction:column;background:var(--ink)">
  <div style="position:relative;height:720px;flex:none;overflow:hidden">
    <img src="%s/t_river.jpg" style="position:absolute;inset:0;width:100%%;height:100%%;
         object-fit:cover;object-position:50%% 62%%;filter:brightness(1.04) contrast(1.04)">
    <div style="position:absolute;inset:0;background:linear-gradient(0deg,
         rgba(8,9,11,.55) 0%%, rgba(8,9,11,0) 34%%)"></div>
    <div style="position:absolute;inset:0;background:linear-gradient(180deg,
         rgba(8,9,11,.78) 0%%, rgba(8,9,11,0) 20%%)"></div>
    <div style="position:absolute;top:44px;left:72px" class="mono"
         >Session 01 &middot; Han river</div>
  </div>
  <div style="flex:1;padding:54px 72px 72px;display:flex;flex-direction:column">
    <div class="dx" style="font-size:106px;color:var(--paper)">Flat. Fast.<br>No lights.</div>
    <span class="rule" style="width:58px;margin:32px 0 26px"></span>
    <div style="font-size:25px;color:#AEB4BE;line-height:1.5;max-width:860px">
      Six kilometres of riverside with nothing to dodge and not one traffic light.
      The one you run at a conversation pace.</div>
    <div class="sp"></div>
    <div style="display:flex;justify-content:space-between;align-items:center;
                border-top:1px solid rgba(255,255,255,.14);padding-top:26px">
      <div class="dx" style="font-size:24px;letter-spacing:.14em;color:var(--paper)">Flyway</div>
      <div class="mono" style="font-size:16px;color:#D4FF36">Run Trip &middot; 2027</div>
    </div>
  </div></div>""" % P

JOBS = [('FLYWAY_banner_wide.png',  1920, 800,  '50% 42%', '70px 86px',      WIDE),
        ('FLYWAY_post_city.png',    1080, 1350, '56% 38%', '78px 72px 72px', IG),
        ('FLYWAY_post_river.png',   1080, 1350, '50% 50%', '0',               RIVER)]

async def main():
    out = '/tmp/claude-0/-home-claude/2e17bfd3-42bc-5136-bb78-767ebae6d1f2/scratchpad'
    async with async_playwright() as p:
        br = await p.chromium.launch(args=['--font-render-hinting=none'])
        for name, w, h, pos, pad, body in JOBS:
            pg = await br.new_page(viewport={'width':w,'height':h})
            html = SHELL % (FONTS, w, h, w, h, pos, pad, body)
            open('/home/claude/photos/_b.html','w',encoding='utf-8').write(html)
            await pg.goto('file:///home/claude/photos/_b.html')
            await pg.wait_for_timeout(1200)
            await pg.screenshot(path=f'{out}/{name}')
            await pg.close()
            print(' ', name, w, 'x', h)
        await br.close()
asyncio.run(main())
