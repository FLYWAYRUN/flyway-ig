# -*- coding: utf-8 -*-
FONTS = open(__file__.rsplit('/',1)[0] + '/fonts.css', encoding='utf-8').read()

BASE = """<!doctype html><meta charset="utf-8"><style>
%s
*{margin:0;padding:0;box-sizing:border-box}
:root{--ink:#08090B;--panel:#111419;--paper:#F2F2EE;--volt:#D4FF36;
      --flare:#FF4B1F;--grey:#7D838F;--edge:rgba(255,255,255,.10)}
html,body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{width:1080px;height:1350px;background:var(--ink);color:var(--paper);
     font-family:'Inter',sans-serif;-webkit-font-smoothing:antialiased;overflow:hidden}
.card{width:1080px;height:1350px;position:relative;display:flex;flex-direction:column;
      padding:78px 72px 72px;background:var(--ink)}
.card.lite{background:var(--paper);color:var(--ink)}
.card.volt{background:var(--volt);color:var(--ink)}
.dx{font-family:'Anton',sans-serif;font-weight:400;text-transform:uppercase;
    line-height:.92;letter-spacing:.012em}
.dx2{font-family:'Bebas',sans-serif;font-weight:400;text-transform:uppercase;
     line-height:.98;letter-spacing:.04em}
.mono{font-family:'Liberation Mono',monospace;font-size:19px;letter-spacing:.22em;
      text-transform:uppercase;color:var(--grey)}
.lite .mono{color:#8A8F99} .volt .mono{color:rgba(0,0,0,.55)}
.mono.v{color:var(--volt)} .lite .mono.v{color:#5E7A00} .volt .mono.v{color:rgba(0,0,0,.78)}
.wm{font-family:'Anton',sans-serif;font-size:24px;letter-spacing:.14em;
    text-transform:uppercase;color:var(--paper)}
.lite .wm{color:var(--ink)} .volt .wm{color:var(--ink)}
.rule{width:58px;height:5px;background:var(--volt);display:block}
.lite .rule,.volt .rule{background:var(--ink)}
.sub{font-size:27px;line-height:1.5;color:#A8AEB8;max-width:820px}
.lite .sub{color:#5C626C} .volt .sub{color:rgba(0,0,0,.68)}
.spacer{margin-top:auto}
.brand{display:flex;justify-content:space-between;align-items:center;
       border-top:1px solid var(--edge);padding-top:26px}
.lite .brand{border-color:#D5D5CD} .volt .brand{border-color:rgba(0,0,0,.18)}
.pan{background:var(--panel);border:1px solid var(--edge);border-radius:4px;padding:34px}
.lite .pan{background:#fff;border-color:#DCDCD4}
.kv{display:grid;grid-template-columns:150px 1fr;gap:16px 26px;font-size:25px}
.kv dt{font-family:'Liberation Mono',monospace;font-size:16px;letter-spacing:.16em;
       text-transform:uppercase;color:var(--grey);padding-top:5px}
.kv dd{color:#DCDFE4} .lite .kv dd{color:#23272E}
</style><body>%s</body>"""

def brand(right):
    return ('<div class="brand"><div class="wm">Flyway</div>'
            '<div class="mono v">%s</div></div>' % right)

def t_statement(d):
    return BASE % (FONTS, (
      '<div class="card %s"><div class="mono v">%s</div><div class="spacer"></div>'
      '<h1 class="dx" style="font-size:%spx">%s</h1>'
      '<span class="rule" style="margin:44px 0 34px"></span>'
      '<div class="sub">%s</div><div class="spacer"></div>%s</div>'
    ) % (d.get('theme',''), d['eyebrow'], d.get('size',132), d['head'], d['sub'],
         brand(d.get('foot','Run Trip &middot; 2027'))))

def t_stat(d):
    return BASE % (FONTS, (
      '<div class="card %s"><div class="mono v">%s</div><div class="spacer"></div>'
      '<div class="dx" style="font-size:%spx;color:%s">%s</div>'
      '<div class="mono" style="margin-top:34px;font-size:22px">%s</div>'
      '<span class="rule" style="margin:44px 0 32px"></span>'
      '<div class="sub">%s</div><div class="spacer"></div>%s</div>'
    ) % (d.get('theme',''), d['eyebrow'], d.get('size',300), d.get('color','var(--volt)'),
         d['value'], d['label'], d['sub'], brand(d.get('foot','Run Trip &middot; 2027'))))

def t_compare(d):
    a, b = d['a'], d['b']
    return BASE % (FONTS, (
      '<div class="card"><div class="mono v">%s</div><div class="spacer"></div>'
      '<div style="display:flex;flex-direction:column;gap:30px">'
      '<div class="pan" style="border-left:6px solid var(--flare)">'
      '<div class="mono" style="font-size:20px">%s</div>'
      '<div class="dx" style="font-size:168px;color:var(--flare);margin-top:14px">%s</div>'
      '<div class="sub" style="font-size:23px;margin-top:10px">%s</div></div>'
      '<div class="pan" style="border-left:6px solid var(--volt)">'
      '<div class="mono v" style="font-size:20px">%s</div>'
      '<div class="dx" style="font-size:168px;color:var(--volt);margin-top:14px">%s</div>'
      '<div class="sub" style="font-size:23px;margin-top:10px">%s</div></div></div>'
      '<div class="sub" style="margin-top:40px">%s</div>'
      '<div class="spacer"></div>%s</div>'
    ) % (d['eyebrow'], a['label'], a['value'], a['note'], b['label'], b['value'], b['note'],
         d['sub'], brand(d.get('foot','Run Trip &middot; 2027'))))

def t_route(d):
    rows = ''.join('<dt>%s</dt><dd>%s</dd>' % (k, v) for k, v in d['rows'])
    return BASE % (FONTS, (
      '<div class="card"><div class="mono v">%s</div>'
      '<h1 class="dx" style="font-size:88px;margin-top:30px">%s</h1>'
      '<div class="dx2" style="font-size:46px;color:var(--volt);margin-top:20px">%s</div>'
      '<div style="margin-top:46px">%s</div>'
      '<dl class="kv" style="margin-top:50px">%s</dl>'
      '<div class="spacer"></div>%s</div>'
    ) % (d['eyebrow'], d['head'], d['name'], d['svg'], rows,
         brand(d.get('foot','Run Trip &middot; 2027'))))

def t_art(d):
    """Headline over a generated runner poster. d['art'] = absolute file path."""
    return BASE % (FONTS, (
      '<div class="card" style="padding:0;background:#D4FF36">'
      '<img src="file://%s" style="position:absolute;inset:0;width:100%%;height:100%%;'
      'object-fit:cover">'
      '<div style="position:absolute;inset:0;padding:78px 72px 72px;display:flex;'
      'flex-direction:column">'
      '<div class="mono" style="color:rgba(0,0,0,.62)">%s</div>'
      '<div style="height:52px"></div>'
      '<h1 class="dx" style="font-size:%spx;color:#08090B">%s</h1>'
      '<span class="rule" style="width:64px;height:6px;background:#08090B;margin:34px 0 26px"></span>'
      '<div style="font-size:26px;color:rgba(0,0,0,.74);line-height:1.5;max-width:780px">%s</div>'
      '<div class="spacer"></div>'
      '<div style="display:flex;justify-content:space-between;align-items:center;'
      'border-top:2px solid rgba(0,0,0,.26);padding-top:26px">'
      '<div class="dx" style="font-size:26px;letter-spacing:.14em;color:#08090B">Flyway</div>'
      '<div class="mono" style="font-size:16px;color:rgba(0,0,0,.62)">%s</div>'
      '</div></div></div>'
    ) % (d['art'], d['eyebrow'], d.get('size', 128), d['head'], d['sub'],
         d.get('foot', 'Run Trip &middot; 2027')))

T = {'statement': t_statement, 'stat': t_stat, 'compare': t_compare,
     'route': t_route, 'art': t_art}
def render(post): return T[post['type']](post)
